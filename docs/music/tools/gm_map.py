"""GM program → Logic patch map, measured on the running Logic (PROMPT_GUIDELINES.md §4).

Builds small SMFs (15 melodic programs per file on channels 0–15 except 9, plus one drum-kit
track last on channel 9), imports each into Logic under the cross-session LogicLock, reads the
mixer strip patch names, and closes the imported (untitled) project without saving. Strip order
follows track order; each track, drum kits included, shows as one strip (2026-11-08 measurement).

Refuses to start a batch while any project window is open, so it never discards someone's work and
never reads a leftover project's strips. The map file is only written when every batch succeeded
with the expected strip count; any failure exits 1 and leaves the previous map untouched.

    python3 docs/music/tools/gm_map.py            # measure everything, write docs/music/gm_patch_map.json
    python3 docs/music/tools/gm_map.py --dry-run  # only write the SMFs to /private/tmp/gm_map/
"""
import argparse
import json
import os
import subprocess
import sys
import time
import unicodedata

import pipeline as P

OUT_DIR = '/private/tmp/gm_map'
MAP_PATH = os.path.join(os.path.dirname(P.SK_DIR), 'gm_patch_map.json')
MELODIC_CHANNELS = [c for c in range(16) if c != 9]
DRUM_KITS = [0, 8, 16, 24, 25, 26, 27, 28, 32, 40, 48, 56, 127]


def batches():
    programs = list(range(128))
    melodic = [programs[i:i + len(MELODIC_CHANNELS)] for i in range(0, 128, len(MELODIC_CHANNELS))]
    n = max(len(melodic), len(DRUM_KITS))
    return [(melodic[i] if i < len(melodic) else [], DRUM_KITS[i] if i < len(DRUM_KITS) else None)
            for i in range(n)]


def build(idx, melodic, kit):
    tracks, pcs, nt = [], {}, {}
    for k, pc in enumerate(melodic):
        tracks.append((f'PC{pc:03d}', MELODIC_CHANNELS[k]))
        pcs[k] = pc
        nt[k] = [(0, P.BAR, 60, 90)]
    if kit is not None:
        k = len(tracks)
        tracks.append((f'KIT{kit:03d}', 9))
        pcs[k] = kit
        nt[k] = [(0, P.PPQ, 36, 100), (P.PPQ, P.PPQ, 38, 100)]
    cc = {k: [] for k in range(len(tracks))}
    smf = P.build_smf(f'GM map {idx}', 100, 0, False, 2, tracks, pcs, nt, cc)
    path = os.path.join(OUT_DIR, f'gm_map_{idx:02d}.mid')
    P.write_smf(path, smf)
    return path


def clear_import_alerts():
    """pipeline.clear_alerts, narrowed: only message dialogs (with static text), never a standard
    window (Sound Library browser) or the Settings / Mixer windows that may already be open."""
    P.osa(f'''tell application "System Events"
tell process "{P.APP}"
repeat with w in windows
try
set n to name of w as text
set sr to subrole of w as text
if sr is not "AXStandardWindow" and (count of static texts of w) > 0 and (count of buttons of w) > 0 and not (n contains "트랙") and not (n contains "설정") and not (n contains "믹서") then
click button 1 of w
end if
end try
end repeat
end tell
end tell''')


def strips_list(raw):
    """Patch names in track order; output/master strips (named 'Stereo Out'/'Master', or shown as
    bare level numbers like '80 17 4') are dropped."""
    names = [s.strip() for s in raw.strip().strip('[]').split('] [')] if raw.startswith('[') else []
    return [n for n in names if n not in ('Stereo Out', 'Master') and not n.replace(' ', '').isdigit()]


def _windows_strict():
    """Logic window names (NFC). Unlike pipeline.windows(), a failed query raises instead of
    returning [], so "no project open" is never inferred from an error."""
    rc, out, err = P.osa(f'''tell application "System Events"
tell process "{P.APP}"
set out to ""
repeat with w in windows
set out to out & "|" & (name of w)
end repeat
return out
end tell
end tell''')
    if rc != 0:
        raise RuntimeError(f'window list failed: {err[:80]}')
    return [unicodedata.normalize('NFC', w) for w in out.split('|')[1:]]


def _imports(names):
    """Untitled project windows (main or mixer-only) — the SMF import, never a saved project."""
    return [w for w in names if w.startswith('무제') and (w.endswith('- 트랙') or w.endswith('- 믹서: 트랙'))]


def close_import():
    """Close only the untitled import without saving; titled projects are never touched."""
    for _ in range(4):
        left = _imports(_windows_strict())
        if not left:
            return True
        P.osa(f'''tell application "System Events"
tell process "{P.APP}"
set frontmost to true
perform action "AXRaise" of window "{left[0]}"
delay 0.5
keystroke "w" using command down
delay 2
{P._click_any(('저장 안 함',))}
end tell
end tell''')
        time.sleep(3)
    return not _imports(_windows_strict())


def measure(path, timeout=900):
    """Returns (raw strip string, None) or (None, error). Refuses to start while any project is
    open or while the window list cannot be read; afterwards closes only its own untitled import."""
    with P.LogicLock('vivaldi-gm-map'):
        try:
            open_projects = [w for w in _windows_strict() if w.endswith('- 트랙') or w.endswith('- 믹서: 트랙')]
        except (RuntimeError, subprocess.TimeoutExpired) as exc:
            return None, f'cannot read Logic windows, refusing to start: {exc}'
        if open_projects:
            return None, f'project already open, refusing to touch it: {open_projects}'
        subprocess.run(['open', '-a', P.APP, path], capture_output=True)
        raw, err = None, None
        try:
            t0 = time.time()
            while time.time() - t0 < timeout:
                if any(w.startswith('무제') and w.endswith('- 트랙') for w in P.windows()):
                    break
                time.sleep(5)
            else:
                err = 'import timeout'
            if err is None:
                time.sleep(3)
                clear_import_alerts()
                time.sleep(2)
                P.open_mixer()
                raw = P.mixer_strips()
                if not raw.startswith('['):
                    err = f'mixer strips unreadable: {raw[:80]!r}'
        except subprocess.TimeoutExpired as exc:
            err = f'osascript timeout: {exc.cmd[-1][:60] if exc.cmd else exc}'
        try:
            closed = close_import()
        except (RuntimeError, subprocess.TimeoutExpired) as exc:
            closed, err = False, (err + '; ' if err else '') + f'close check failed: {exc}'
        if not closed:
            err = (err + '; ' if err else '') + 'could not close the import'
        return (raw if err is None else None), err


def main(argv):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--dry-run', action='store_true', help='only write the SMFs, do not touch Logic')
    args = ap.parse_args(argv[1:])
    os.makedirs(OUT_DIR, exist_ok=True)
    plan = [(i, mel, kit, build(i, mel, kit)) for i, (mel, kit) in enumerate(batches())]
    if args.dry_run:
        for i, mel, kit, path in plan:
            print(path, mel[:1], mel[-1:], kit)
        return 0
    result = {'measured': time.strftime('%Y-%m-%dT%H:%M:%S%z'), 'melodic': {}, 'drum_kits': {}, 'raw': {}}
    for i, mel, kit, path in plan:
        raw, err = measure(path)
        name = os.path.basename(path)
        if err is None:
            names = strips_list(raw)
            expected = len(mel) + (kit is not None)
            if len(names) != expected:
                err = f'{len(names)} strips, expected {expected}: {raw}'
        if err is not None:
            print(f'{name}: FAILED {err} — map not written', flush=True)
            return 1
        result['raw'][name] = raw
        for k, pc in enumerate(mel):
            result['melodic'][str(pc)] = names[k]
        if kit is not None:
            result['drum_kits'][str(kit)] = names[len(mel):]
        print(f'{name}: {raw}', flush=True)
    with open(MAP_PATH, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=1)
    print(f'wrote {MAP_PATH}')
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
