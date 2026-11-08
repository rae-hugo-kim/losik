"""GM program → Logic patch map, measured on the running Logic (PROMPT_GUIDELINES.md §4).

Builds small SMFs (15 melodic programs per file on channels 0–15 except 9, plus one drum-kit
track last on channel 9), imports each into Logic under the cross-session LogicLock, reads the
mixer strip patch names, and closes the project without saving. Strip order follows track order;
a multi-output drum kit expands into several strips, so the drum track is always last.

    python3 docs/music/tools/gm_map.py            # measure everything, write docs/music/gm_patch_map.json
    python3 docs/music/tools/gm_map.py --dry-run  # only write the SMFs to /private/tmp/gm_map/
"""
import json
import os
import subprocess
import sys
import time

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


def measure(path, timeout=900):
    with P.LogicLock('vivaldi-gm-map'):
        P.close_all_projects(save=False)
        subprocess.run(['open', '-a', P.APP, path], capture_output=True)
        t0 = time.time()
        while time.time() - t0 < timeout:
            if any(w.startswith('무제') and w.endswith('- 트랙') for w in P.windows()):
                break
            time.sleep(5)
        else:
            return None, 'import timeout'
        time.sleep(3)
        clear_import_alerts()
        time.sleep(2)
        P.open_mixer()
        raw = P.mixer_strips()
        P.close_all_projects(save=False)
        return raw, None


def main(argv):
    os.makedirs(OUT_DIR, exist_ok=True)
    plan = [(i, mel, kit, build(i, mel, kit)) for i, (mel, kit) in enumerate(batches())]
    if '--dry-run' in argv:
        for i, mel, kit, path in plan:
            print(path, mel[:1], mel[-1:], kit)
        return 0
    result = {'measured': time.strftime('%Y-%m-%dT%H:%M:%S%z'), 'melodic': {}, 'drum_kits': {}, 'raw': {}}
    for i, mel, kit, path in plan:
        raw, err = measure(path)
        result['raw'][os.path.basename(path)] = raw or err
        if raw is None:
            print(f'{path}: {err}', flush=True)
            continue
        names = strips_list(raw)
        for k, pc in enumerate(mel):
            result['melodic'][str(pc)] = names[k] if k < len(names) else None
        if kit is not None:
            result['drum_kits'][str(kit)] = names[len(mel):] or None
        print(f'{os.path.basename(path)}: {raw}', flush=True)
    with open(MAP_PATH, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=1)
    print(f'wrote {MAP_PATH}')
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
