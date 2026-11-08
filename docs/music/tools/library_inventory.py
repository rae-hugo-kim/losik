"""Logic Pro sound-library inventory → docs/music/logic_library_inventory.json (+ markdown sections on stdout).

Walks the relocated library bundle and the legacy /Library trees, and records:
  packs            Package Definitions/*.plist — name, sizes, FileChecks present/total, state
  patches          every Patches/Instrument and Patches/Audio .patch (category path + name)
  sampler_presets  every Sampler .exs (bundle Plug-In Settings/Sampler, /Library Sampler Instruments, GarageBand)
  plugin_settings  preset counts per plug-in folder
  samples / loops / impulse_responses   sizes and counts
  gm_reachable     patch names that a GM program change loads (gm_patch_map.json; Korean display names mapped)
  orchestral       curated view: acoustic/orchestral folders only, with family, articulations, solo/section/unknown

Read-only, no Logic interaction. Stdout is a sequence of markdown sections (`## <name>`); the table
sections (packs, patch_counts, plugin_settings, samples, orchestral_summary, orchestral_tables) are
embedded verbatim in LOGIC_LIBRARY_INVENTORY.md, so those parts can always be rebuilt from this output.

    python3 docs/music/tools/library_inventory.py            # write JSON, print sections
    python3 docs/music/tools/library_inventory.py --no-write # sections only
"""
import collections
import json
import os
import plistlib
import re
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
MUSIC = os.path.dirname(HERE)
BUNDLE = '/Volumes/Netac 2TB/Logic Sound Library/Logic Pro Library.bundle'
LEGACY_LOGIC = '/Library/Application Support/Logic'
LEGACY_GB = '/Library/Application Support/GarageBand/Instrument Library'
GM_MAP = os.path.join(MUSIC, 'gm_patch_map.json')
OUT = os.path.join(MUSIC, 'logic_library_inventory.json')

# gm_patch_map.json records what the mixer strip DISPLAYS; a few patches display a Korean name or the
# channel-strip name instead of the patch file name. Map display name → patch file name.
GM_DISPLAY_ALIAS = {'톤휠 오르간': 'Tonewheel Organ', '어쿠스틱 기타': 'Acoustic Guitar', '하드 록': 'Hard Rock',
                    '루트 업라이트': 'Roots Upright', '(New) Horns': 'Studio Alto Sax 1',
                    '선원': 'Zen Garden'}   # Logic ko.lproj/Item.strings: InsP/Zen Garden = 선원
GM_FALLBACK = re.compile(r'^GM 기기 \d+$')

# Curated "acoustic / orchestral" view: only these library folders are scanned (synths, drum kits,
# textures are out). Family comes from the folder when the folder is homogeneous, otherwise from the
# name (word-boundary regex); MIXED folders hold several families (Studio Horns = brass + saxes).
ORCH_PATCH_ROOTS = ('Strings/', 'Brass & Woodwind/', 'z_Legacy/Orchestral/', 'z_Legacy/World/', 'Keyboard/Acoustic Piano/',
                    'Keyboard/Organ/', 'Keyboard/Mellotron/', 'Mallet/', 'Guitar/', 'Bass/')
ORCH_EXS_ROOTS = ('z_Legacy/Orchestral/', 'z_Legacy/Strings/', 'z_Legacy/Brass & Woodwinds/', 'z_Legacy/World/', 'z_Legacy/Mallet/',
                  'z_Legacy/Keyboard/Acoustic Piano/', 'z_Internal/Studio Strings/', 'z_Internal/Studio Horns/', 'z_Internal/Studio Piano/',
                  'Other Strings/', 'Mallet/', 'Keyboard/Acoustic Piano/', '09 Orchestral/', '01 Acoustic Pianos/',
                  'Sampler/Sampler Instruments/iOS Instruments/')
FOLDER_FAMILY = [
    ('z_Legacy/Orchestral/01 Woodwinds/', 'woodwinds'), ('z_Legacy/Orchestral/Woodwinds/', 'woodwinds'), ('09 Orchestral/01 Woodwinds/', 'woodwinds'),
    ('z_Legacy/Orchestral/02 Brass/', 'brass'), ('z_Legacy/Orchestral/Brass/', 'brass'), ('09 Orchestral/02 Brass/', 'brass'),
    ('z_Legacy/Orchestral/03 Percussion/', 'percussion_orch'), ('z_Legacy/Orchestral/04 Tuned Percussion/', 'percussion_orch'),
    ('z_Legacy/Orchestral/Percussion/', 'percussion_orch'), ('Mallet/', 'percussion_orch'), ('z_Legacy/Mallet/', 'percussion_orch'),
    ('z_Legacy/Orchestral/05 Keyboards/', 'keyboard_classical'), ('z_Legacy/Orchestral/07 Pipe Organ/', 'keyboard_classical'),
    ('z_Legacy/Orchestral/Keyboard/', 'keyboard_classical'), ('Keyboard/Acoustic Piano/', 'keyboard_classical'),
    ('z_Legacy/Keyboard/Acoustic Piano/', 'keyboard_classical'), ('01 Acoustic Pianos/', 'keyboard_classical'), ('z_Internal/Studio Piano/', 'keyboard_classical'),
    ('z_Legacy/Orchestral/06 Harp/', 'harp_plucked'), ('z_Legacy/Orchestral/Harp/', 'harp_plucked'), ('Guitar/', 'harp_plucked'),
    ('z_Legacy/Orchestral/09 Strings/', 'strings'), ('z_Legacy/Orchestral/Strings/', 'strings'), ('09 Orchestral/09 Strings/', 'strings'),
    ('Strings/', 'strings'), ('z_Internal/Studio Strings/', 'strings'), ('z_Legacy/Strings/', 'strings'),
    ('z_Legacy/Orchestral/10 Choir/', 'choir'), ('z_Legacy/Orchestral/Choir/', 'choir'),
    ('Keyboard/Organ/', 'organ'), ('Keyboard/Mellotron/', 'mellotron'), ('Bass/', 'bass_electric'),
    ('z_Legacy/World/', 'world'), ('Other Strings/', 'world'),
    # last-resort folder families for MIXED folders (used only when the name regex found nothing)
    ('Brass & Woodwind/Studio Horns/', 'brass'), ('z_Internal/Studio Horns/', 'brass'),
]
MIXED_FOLDERS = ('Brass & Woodwind/Studio Horns/', 'z_Internal/Studio Horns/', 'z_Legacy/Brass & Woodwinds/', 'Sampler/Sampler Instruments/iOS Instruments/')
NAME_FAMILY = [
    ('woodwinds', r'\b(flutes?|piccolo|oboe|english horn|clarinets?|bassoon|sax|saxophone|woodwinds?)\b'),
    ('brass', r'\b(trumpets?|trombones?|tuba|french horns?|horns?|brass)\b'),
    ('strings', r'\b(violins?|violas?|cellos?|double bass(es)?|contrabass|basses|strings?|arco)\b'),
    ('harp_plucked', r'\b(harp|lute|guitar|banjo)\b'),
    ('keyboard_classical', r'\b(harpsichord|celesta|piano|grand)\b'),
    ('percussion_orch', r'\b(timpani|glockenspiel|xylophone|tubular bells|crotales|marimba|vibraphone)\b'),
    ('choir', r'\b(choir|chamber|gregorian|gospel)\b'),
]
FAMILY_KO = collections.OrderedDict([
    ('strings', '현악'), ('woodwinds', '목관'), ('brass', '금관'), ('keyboard_classical', '건반 (피아노·하프시코드·첼레스타·파이프오르간)'),
    ('harp_plucked', '하프·발현 (기타 포함)'), ('percussion_orch', '타악 (선율타악 포함)'), ('choir', '합창'), ('organ', '오르간 (전자·톤휠)'),
    ('mellotron', '멜로트론'), ('world', '월드'), ('bass_electric', '일렉·업라이트 베이스'), ('other', '그 밖'),
])
# Articulation regexes (lower-case names), longest first so "Tremolo Crescendo" wins over "Tremolo"; a trailing "leg" is a legacy legato typo.
ARTICULATIONS = [(r'tremolo crescendo', 'Tremolo Crescendo'), (r'singlestrokes', 'SingleStrokes'), (r'pizzicato', 'Pizzicato'), (r'staccato', 'Staccato'),
                 (r'crescendo', 'Crescendo'), (r'tremolo', 'Tremolo'), (r'legato', 'Legato'), (r'trill 1', 'Trill 1'), (r'trill 2', 'Trill 2'),
                 (r'swells', 'Swells'), (r'sustain', 'Sustain'), (r'arco', 'Arco'), (r'\bleg$', 'Legato')]
ART_STRIP = r'\s*(Tremolo Crescendo|SingleStrokes|Pizzicato|Staccato|Crescendo|Tremolo|Legato|Trill [12]|Swells|Sustain|\(Arco\)|\(Pizzicato\)|\+|leg| iOS KB| iOS small)$'
SECTION_HINT = r'\b(violins|violas|cellos|basses|strings|flutes|clarinets|trumpets|trombones|horns|section|ensemble|choir|chamber|kit|brass|chords|dual)\b|\d-piece'
SOLO_HINT = r'\bsolo\b|\((arco|pizzicato)\)|^(violin|viola|cello|double bass|oboe|bassoon|piccolo|english horn|harp|celesta|harpsichord|timpani|tuba|trumpet|trombone|flute|clarinet)\b|single instruments'


def du_bytes(path):
    r = subprocess.run(['du', '-sk', path], capture_output=True, text=True)
    return int(r.stdout.split()[0]) * 1024 if r.returncode == 0 and r.stdout else None


def walk_ext(root, exts):
    """Relative paths of files OR bundle directories whose extension is in exts; bundles are not entered."""
    out = []
    if not os.path.isdir(root):
        return out
    for dirpath, dirnames, filenames in os.walk(root):
        hits = [d for d in dirnames if os.path.splitext(d)[1] in exts]
        for d in hits:
            out.append(os.path.relpath(os.path.join(dirpath, d), root))
            dirnames.remove(d)
        for f in filenames:
            if os.path.splitext(f)[1] in exts:
                out.append(os.path.relpath(os.path.join(dirpath, f), root))
    return sorted(out)


def packs():
    pd = os.path.join(BUNDLE, 'Application Support', 'Package Definitions')
    rows = []
    for f in sorted(os.listdir(pd)):
        if not f.endswith('.plist'):
            continue
        with open(os.path.join(pd, f), 'rb') as fh:
            d = plistlib.load(fh)
        fc = d.get('FileChecks')
        if fc:
            fcs = fc if isinstance(fc, list) else [fc]
            paths = [x if isinstance(x, str) else (x.get('Path') or x.get('path') or str(x)) for x in fcs]
            present = sum(os.path.exists(os.path.join(BUNDLE, re.sub(r'^\./|^/', '', p))) for p in paths)
            state = 'installed' if present == len(paths) else 'partial'
        else:
            present, paths, state = 0, [], 'not installed'
        rows.append(dict(id=f[:-6], name=d.get('Bundle Name', '?'), state=state, filechecks=f'{present}/{len(paths)}',
                         download_gb=round(d.get('DownloadSize', 0) / 1e9, 2), installed_gb=round(d.get('InstalledSize', 0) / 1e9, 2)))
    return rows


def classify(rel, name):
    low, path_low = name.lower(), rel.lower()
    fam = None
    if not rel.startswith(MIXED_FOLDERS):
        fam = next((k for prefix, k in FOLDER_FAMILY if rel.startswith(prefix)), None)
    if fam is None:
        fam = next((k for k, rx in NAME_FAMILY if re.search(rx, low)), None)
    if fam is None:
        fam = next((k for prefix, k in FOLDER_FAMILY if rel.startswith(prefix)), 'other')
    arts = []
    rest = low
    for rx, label in ARTICULATIONS:
        if re.search(rx, rest):
            arts.append(label)
            rest = re.sub(rx, '', rest)
    if name.endswith('+'):
        arts.append('keyswitch (+)')
    if not arts:
        arts = ['default']
    # Folder names ('Section Instruments', '3-Piece Section', '10 Choir') mark sections; plural instrument names do
    # too, but only for families where a plural means an ensemble (a pipe-organ 'Flutes' stop or a piano layered with
    # strings is not one). Mellotron tapes named after ensembles ('3 Violins', 'GC 3 Brass') keep the hint.
    folder_low = path_low.rsplit('/', 1)[0] if '/' in path_low else ''
    plural_ok = fam in ('strings', 'woodwinds', 'brass', 'choir', 'world', 'percussion_orch', 'mellotron')
    if re.search(r'\b(section|ensemble|choir|chamber)\b|\d-piece', folder_low) or (plural_ok and re.search(SECTION_HINT, low)):
        solo = 'section'
    elif re.search(SOLO_HINT, low + ' ' + path_low):
        solo = 'solo'
    else:
        solo = 'unknown'
    return dict(family=fam, articulations=arts, solo=solo)


def base_name(name):
    b = name
    for _ in range(3):
        b = re.sub(ART_STRIP, '', b).strip()
    return b


def orchestral_tables(orch):
    """Group curated entries by (family, instrument base name) → one markdown table per family."""
    grp = collections.OrderedDict()
    for x in orch:
        g = grp.setdefault((x['family'], base_name(x['name'])), dict(kinds=set(), arts=set(), solo=set(), gm=set(), where=set()))
        g['kinds'].add('패치' if x['kind'] == 'patch' else 'EXS')
        g['arts'].update(x['articulations'])
        g['solo'].add(x['solo'])
        g['gm'].update(x['gm_pcs'])
        g['where'].add(x['path'].rsplit('/', 1)[0])
    solo_ko = {'solo': '솔로', 'section': '섹션/합주', 'unknown': '미상'}
    lines = []
    for fam, ko in FAMILY_KO.items():
        rows = [(k[1], v) for k, v in grp.items() if k[0] == fam]
        if not rows:
            continue
        lines.append(f'\n**{ko}** ({len(rows)}개 악기, {sum(1 for x in orch if x["family"] == fam)}항목)\n')
        lines.append('| 악기 | 솔로/섹션 | 형태 | 주법 | GM PC | 위치 |\n|---|---|---|---|---|---|')
        order = {'solo': 0, 'section': 1, 'unknown': 2}
        for n, v in sorted(rows, key=lambda r: (min(order[s] for s in r[1]['solo']), r[0])):
            arts = ['기본' if a == 'default' else a for a in sorted(v['arts'], key=lambda a: (a != 'default', a))]
            gm = ', '.join(str(p) for p in sorted(v['gm'])) or '—'
            solo = '/'.join(solo_ko[s] for s in sorted(v['solo'], key=order.get))
            lines.append(f"| {n} | {solo} | {'·'.join(sorted(v['kinds']))} | {', '.join(arts)} | {gm} | `{'; '.join(sorted(v['where']))}` |")
    return '\n'.join(lines)


def main(argv):
    if not os.path.isdir(os.path.join(BUNDLE, 'Patches')):
        print(f'library bundle not mounted: {BUNDLE}', file=sys.stderr)
        return 2
    inv = dict(measured=time.strftime('%Y-%m-%dT%H:%M:%S%z'), bundle=BUNDLE)
    inv['logic_version'] = subprocess.run(['defaults', 'read', '/Applications/Logic Pro Creator Studio.app/Contents/Info.plist', 'CFBundleShortVersionString'],
                                          capture_output=True, text=True).stdout.strip()
    inv['bundle_bytes'] = du_bytes(BUNDLE)
    inv['packs'] = packs()

    inv['patches'] = {kind: walk_ext(os.path.join(BUNDLE, 'Patches', kind), {'.patch'}) for kind in ('Instrument', 'Audio')}
    counts = collections.OrderedDict()
    for rel in inv['patches']['Instrument']:
        parts = rel.split('/')
        cat = parts[0] if len(parts) > 1 else '(root)'
        sub = parts[1] if len(parts) > 2 else ''
        counts.setdefault(cat, collections.Counter())[sub] += 1
    inv['patch_counts'] = {c: dict(v) for c, v in counts.items()}

    inv['sampler_presets'] = {
        'bundle': walk_ext(os.path.join(BUNDLE, 'Plug-In Settings', 'Sampler'), {'.exs'}),
        'legacy_logic': walk_ext(os.path.join(LEGACY_LOGIC, 'Sampler Instruments'), {'.exs'}),
        'garageband': walk_ext(LEGACY_GB, {'.exs'}),
    }
    ps = os.path.join(BUNDLE, 'Plug-In Settings')
    inv['plugin_settings'] = {d: len(walk_ext(os.path.join(ps, d), {'.pst', '.exs', '.acp', '.aupreset', '.cst'})) for d in sorted(os.listdir(ps)) if os.path.isdir(os.path.join(ps, d))}
    smp = os.path.join(BUNDLE, 'Samples')
    inv['samples_bytes'] = {d: du_bytes(os.path.join(smp, d)) for d in sorted(os.listdir(smp)) if os.path.isdir(os.path.join(smp, d))}
    loops = os.path.join(BUNDLE, 'Apple Loops')
    inv['apple_loops'] = {d: len(walk_ext(os.path.join(loops, d), {'.caf', '.aif', '.aiff'})) for d in sorted(os.listdir(loops)) if os.path.isdir(os.path.join(loops, d))}
    inv['impulse_responses'] = len(walk_ext(os.path.join(BUNDLE, 'Impulse Responses'), {'.sdir', '.aif', '.wav', '.caf', '.SDIR'}))
    inv['legacy_library_bytes'] = {p: du_bytes(p) for p in (LEGACY_LOGIC, os.path.dirname(LEGACY_GB), '/Library/Audio/Apple Loops', '/Library/Audio/Impulse Responses') if os.path.isdir(p)}

    gm = {'melodic': {}, 'drum_kits': {}}
    if os.path.exists(GM_MAP):
        with open(GM_MAP, encoding='utf-8') as fh:
            gm = json.load(fh)
    reach = collections.defaultdict(list)
    fallback = []
    for pc, display in gm['melodic'].items():
        if GM_FALLBACK.match(display):
            fallback.append(int(pc))
            continue
        reach[GM_DISPLAY_ALIAS.get(display, display)].append(int(pc))
    inv['gm_reachable'] = {k: sorted(v) for k, v in sorted(reach.items())}
    inv['gm_fallback_pcs'] = sorted(fallback)
    inv['gm_drum_kits'] = gm['drum_kits']

    orch = []
    for rel in inv['patches']['Instrument']:
        if rel.startswith(ORCH_PATCH_ROOTS):
            name = os.path.basename(rel)[:-6]
            orch.append(dict(kind='patch', path=rel, name=name, gm_pcs=inv['gm_reachable'].get(name, []), **classify(rel, name)))
    for src, lst in inv['sampler_presets'].items():
        for rel in lst:
            if rel.startswith(ORCH_EXS_ROOTS):
                name = os.path.basename(rel)[:-4]
                orch.append(dict(kind=f'exs:{src}', path=rel, name=name, gm_pcs=[], **classify(rel, name)))
    inv['orchestral'] = orch

    if '--no-write' not in argv:
        with open(OUT, 'w', encoding='utf-8') as f:
            json.dump(inv, f, ensure_ascii=False, indent=1)
        print(f'wrote {OUT}', file=sys.stderr)

    # ---- markdown sections (embedded verbatim by LOGIC_LIBRARY_INVENTORY.md)
    gb = lambda b: f'{b / 1e9:.1f} GB' if b else '-'
    print('## meta')
    print(f"측정 {inv['measured']} · Logic {inv['logic_version']} · 번들 {gb(inv['bundle_bytes'])}")
    print('\n## packs')
    print('| 팩 | 상태 | FileChecks | 다운로드 | 설치 |\n|---|---|---|---|---|')
    for p in inv['packs']:
        print(f"| {p['name']} | {p['state']} | {p['filechecks']} | {p['download_gb']} GB | {p['installed_gb']} GB |")
    print('\n## patch_counts')
    print('| 분류 | 패치 수 | 하위 분류 (수) |\n|---|---|---|')
    for c, subs in inv['patch_counts'].items():
        ordered = sorted(subs.items(), key=lambda kv: -kv[1])
        top = ', '.join(f'{k or "(루트)"} {v}' for k, v in ordered[:6]) + (' …' if len(ordered) > 6 else '')
        print(f'| {c} | {sum(subs.values())} | {top} |')
    print(f"\nAudio 패치 {len(inv['patches']['Audio'])}개 · Sampler 프리셋 번들 {len(inv['sampler_presets']['bundle'])} / `/Library` {len(inv['sampler_presets']['legacy_logic'])} / GarageBand {len(inv['sampler_presets']['garageband'])}")
    print('\n## plugin_settings')
    print('| 플러그인 | 프리셋 수 |\n|---|---|')
    for k, v in inv['plugin_settings'].items():
        print(f'| {k} | {v} |')
    print('\n## samples')
    print('| Samples 폴더 | 크기 |\n|---|---|')
    for k, v in inv['samples_bytes'].items():
        print(f'| {k} | {gb(v)} |')
    print(f"\nApple Loops 폴더 {len(inv['apple_loops'])}개 · 루프 {sum(inv['apple_loops'].values())}개 · IR {inv['impulse_responses']}개")
    print('\n## gm')
    print(f"GM 번호로 닿는 패치 {len(inv['gm_reachable'])}종 (저품질 폴백 PC {', '.join(map(str, inv['gm_fallback_pcs']))} 제외)")
    print('\n## orchestral_summary')
    fam = collections.Counter((o['family'], o['solo']) for o in orch)
    print('| 계열 | 솔로 | 섹션/합주 | 미상 | 합계 |\n|---|---|---|---|---|')
    for f_, ko in FAMILY_KO.items():
        tot = fam[(f_, 'solo')] + fam[(f_, 'section')] + fam[(f_, 'unknown')]
        if tot:
            print(f"| {ko} | {fam[(f_, 'solo')]} | {fam[(f_, 'section')]} | {fam[(f_, 'unknown')]} | {tot} |")
    print(f'\n큐레이션 항목 합계 {len(orch)}')
    print('\n## orchestral_tables')
    print(orchestral_tables(orch))
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
