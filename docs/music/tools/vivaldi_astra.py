"""Vivaldi variations by openai-codex/gpt-6-astra, 2026-10-30.
Source: Mutopia Project, Le quattro stagioni, via vivaldi_data.py.
Derivative MIDI and this arrangement: CC BY-SA 3.0.
Run: python3 -B docs/music/tools/vivaldi_astra.py
Verify existing MIDI without writes: append --check.
Verify rendered WAV without writes: append --verify-audio.
"""
import json
import os
import random
from collections import defaultdict

from pipeline import BAR, PPQ, SK_DIR, bt, build_smf, write_smf, parse_smf
from vivaldi_data import MOVEMENTS, bar_tick

MODEL = 'openai-codex/gpt-6-astra'
CREDIT = 'Mutopia Project; arrangement: Astra; CC BY-SA 3.0'
TRACKS = [('Drums', 9), ('Bass', 0), ('Keys', 1), ('Pad', 2), ('Theme', 3), ('Reprise', 4)]
# Each tuple is a deliberately chosen root, quality, and four-note voicing.
CHORDS = {
    'Emaj9': (40, 'maj9', [56, 59, 63, 66]),
    'Amaj9': (33, 'maj9', [56, 59, 61, 64]),
    'F#m9': (30, 'm9', [57, 61, 64, 68]),
    'B13': (35, '13', [57, 63, 68, 73]),
    'C#m9': (37, 'm9', [52, 56, 59, 63]),
    'G#7b9': (32, '7b9', [60, 63, 66, 69]),
    'Gm9': (31, 'm9', [58, 62, 65, 69]),
    'Cm9': (36, 'm9', [55, 58, 62, 63]),
    'Ebmaj9': (39, 'maj9', [55, 58, 62, 65]),
    'D7b9': (38, '7b9', [54, 60, 63, 69]),
    'Fmaj9': (29, 'maj9', [57, 60, 64, 67]),
    'Bbmaj9': (34, 'maj9', [57, 60, 62, 65]),
    'Dm9': (38, 'm9', [53, 57, 60, 64]),
    'C13': (36, '13', [58, 64, 69, 74]),
    'Am7': (33, 'm7', [55, 60, 64, 67]),
    'A7b9': (33, '7b9', [55, 58, 61, 64]),
    'Gm6': (31, 'm6', [55, 58, 62, 64]),
    'D9': (38, '9', [54, 60, 64, 69]),
    'Fm9': (29, 'm9', [56, 60, 63, 67]),
    'Bbm9': (34, 'm9', [56, 60, 61, 65]),
    'Dbmaj9': (37, 'maj9', [53, 56, 60, 63]),
    'C7b9': (36, '7b9', [52, 58, 61, 67]),
    'Abmaj9': (32, 'maj9', [55, 58, 60, 63]),
    'Bb13': (34, '13', [56, 62, 67, 72]),
}

# key, bpm, bars, lead PC, reprise PC, chord palette, motif (relative to tonic),
# comping offsets (quarter beats), break layers, musical identity.
PLANS = [
    (('spring', 1), 84, 64, 4, 24, ['Emaj9', 'F#m9', 'Amaj9', 'B13'],
     [4, 2, 7, 6], [0, 2.5], 'keys', '새의 반복음을 EP 당김으로 열고 나일론 응답으로 돌려줍니다.'),
    (('spring', 2), 74, 56, 24, 4, ['C#m9', 'Amaj9', 'F#m9', 'G#7b9'],
     [7, 3, 2, 0], [0.5], 'pad', '잠든 목동의 하강선을 나일론의 긴 숨과 EP 재현으로 나눕니다.'),
    (('spring', 3), 122, 96, 0, 4, ['Emaj9', 'Amaj9'],
     [7, 11, 9, 4], [0, 1.75], 'bass', '시칠리아나의 이웃음을 셔플 하우스로 바꾸고 피아노를 EP로 교대합니다.'),
    (('summer', 1), 88, 64, 4, 0, ['Gm9', 'Ebmaj9', 'Cm9', 'D7b9'],
     [0, 2, 3, 7], [0.75, 2.5], 'hats', '짧은 한숨들을 두 마디씩 묶고 그랜드가 후반을 선명하게 받습니다.'),
    (('summer', 2), 76, 56, 0, 24, ['Gm9', 'Cm9', 'D7b9', 'Ebmaj9'],
     [7, 5, 2, 3], [0, 3], 'keys', '긴 선율과 쉼을 남기고 천둥 대신 낮은 고스트 스네어로 긴장합니다.'),
    (('summer', 3), 124, 96, 80, 4, ['Gm9', 'D7b9', 'Ebmaj9', 'Cm9'],
     [0, 7, 5, 3], [0.5, 2.75], 'pad', '폭풍의 반복음을 8분 골격으로 솎고 리드 신스에서 EP로 식힙니다.'),
    (('autumn', 1), 86, 64, 24, 0, ['Fmaj9', 'Dm9', 'Bbmaj9', 'C13'],
     [4, 7, 9, 7], [0, 1.5, 3], 'bass', '수확 춤의 반복음을 나일론 붐뱁과 비대칭 킥으로 풀어냅니다.'),
    (('autumn', 2), 72, 56, 4, 0, ['Dm9', 'Gm6', 'A7b9', 'Bbmaj9'],
     [0, 7, 9, 5], [0.5, 2.75], 'pad', 'violin1의 느린 반음선을 EP로 옮기고 빈 브레이크 뒤 그랜드로 돌아옵니다.'),
    (('autumn', 3), 116, 96, 27, 4, ['Fmaj9', 'Bbmaj9', 'C13', 'Am7'],
     [0, 7, 2, 4], [0, 2.25], 'hats', '사냥의 도약을 기타 훅으로 남기되 네 박 셔플의 낮은 베이스로 누릅니다.'),
    (('winter', 1), 118, 96, 4, 80, ['Fm9', 'Dbmaj9', 'C7b9', 'Bbm9'],
     [0, 1, 0, 7], [0.25, 2.5], 'keys', '4마디부터 시작하는 떨림 주제를 EP로 제시하고 신스 재현을 대비합니다.'),
    (('winter', 2), 78, 56, 24, 4, ['Ebmaj9', 'Abmaj9', 'Cm9', 'Bb13'],
     [7, 4, 2, 0], [0, 2], 'hats', '겨울 실내의 선율을 나일론과 낮은 EP로 감싸고 마지막은 건반만 남깁니다.'),
    (('winter', 3), 120, 96, 0, 24, ['Fm9', 'Bbm9', 'Dbmaj9', 'C7b9'],
     [7, 8, 7, 3], [0.75, 3], 'bass', '빙판 위 회전음을 솎아 그랜드 셔플로 만들고 나일론 재현으로 닫습니다.'),
]
TONICS = {'spring': (64, 61, 64), 'summer': (67, 67, 67),
          'autumn': (65, 62, 65), 'winter': (65, 63, 65)}
SKETCHES = []
for index, (key, bpm, bars, lead, reprise, chords, motif, comp, brk, notes) in enumerate(PLANS):
    season, number = key
    window = (4, 12) if key == ('winter', 1) else MOVEMENTS[key]['theme']
    SKETCHES.append(dict(key=key, sid=f'vs-{season}{number}-astra',
        title=f'{season.title()} {("I", "II", "III")[number - 1]} Astra',
        genre='deep house' if bars == 96 else 'lo-fi hip hop', bpm=bpm, bars=bars,
        theme_part='violin1' if key == ('autumn', 2) else 'solo', theme_window=window,
        rhythm_ops=['syncopation', 'half-duration', 'run-thinning', 'swing'],
        notes=notes, lead=lead, reprise=reprise, chords=chords, motif=motif,
        comp=comp, break_layer=brk, tonic=TONICS[season][number - 1], index=index))


def sections(s):
    if s['bars'] == 96:
        return [(1, 'intro'), (9, 'theme'), (33, 'answer'), (49, 'break'),
                (57, 'reprise'), (81, 'answer2'), (89, 'outro')]
    if s['bars'] == 64:
        return [(1, 'intro'), (9, 'theme'), (25, 'answer'), (33, 'break'),
                (41, 'reprise'), (57, 'outro')]
    return [(1, 'intro'), (9, 'theme'), (25, 'break'), (33, 'reprise'),
            (45, 'answer2'), (49, 'outro')]


def section_at(s, bar):
    return next((start, name) for start, name in reversed(sections(s)) if start <= bar)


def phrase(s):
    """Meter conversion, monophonic skeleton, audible rhythm rewrite; no original accompaniment."""
    m = MOVEMENTS[s['key']]
    a, z = s['theme_window']
    origin, end = bar_tick(s['key'], a), bar_tick(s['key'], z + 1)
    scale = {(4, 4): 1, (3, 4): 4 / 3, (3, 8): 4 / 3, (12, 8): 2 / 3}[m['ts']]
    length = int((end - origin) * scale)
    length = ((length + BAR - 1) // BAR) * BAR
    cells = {}
    for tick, dur, pitch in m['parts'][s['theme_part']]:
        if not origin <= tick < end:
            continue
        pos = round((tick - origin) * scale / 240) * 240
        if pos >= length:
            continue
        # A single pitch from this source part; adjacent runs collapse to eighth-note anchors.
        candidate = (dur, pitch, int(dur * scale))
        if pos not in cells or candidate[:2] > cells[pos][:2]:
            cells[pos] = candidate
    pitches = sorted(p for _, p, _ in cells.values())
    octave = -12 if pitches[len(pitches)//2] >= 76 else 0
    out = []
    by_bar = defaultdict(list)
    for t, (_, p, d) in sorted(cells.items()):
        by_bar[t // BAR].append((t, d, p))
    for bar, ns in sorted(by_bar.items()):
        if s['genre'] == 'lo-fi hip hop' and len(ns) > 6:
            keep = {round(i * (len(ns) - 1) / 5) for i in range(6)}
            ns = [n for i, n in enumerate(ns) if i in keep]
        for i, (t, d, p) in enumerate(ns):
            off = t % BAR
            push = -120 if off in (480, 1440) else 0
            swing = 28 if off % 480 == 240 else 0
            # First onset is delayed on alternating bars even when a melody has only long tones.
            delay = 120 if i == 0 and bar % 2 == 0 else 0
            start = t + push + swing + delay
            if out and start <= out[-1][0]:
                start = t + swing  # Cancel anticipation rather than reverse the source pitches.
            duration = max(100, int(d * (0.5 if i % 2 == 0 else 0.85)))
            out.append((start, duration, p + octave))
    out.sort()
    return [(t, min(d, (out[i+1][0] if i+1 < len(out) else length) - t - 18), p)
            for i, (t, d, p) in enumerate(out)], length


def melody(s):
    ph, length = phrase(s)
    events = []
    for start, name in sections(s):
        stop = next((b for b, _ in sections(s) if b > start), s['bars'] + 1)
        if name in ('theme', 'reprise'):
            for base in range(bt(start), bt(stop), length):
                for t, d, p in ph:
                    at = base + t
                    if at < bt(stop):
                        events.append((at, min(d, bt(stop)-at-18), p, name))
        elif name in ('answer', 'answer2'):
            # Hand-written four-note motif, with rests and no source accompaniment.
            for bar in range(start, stop):
                i = (bar-start) % 4
                offsets = (0.5, 2.75) if i % 2 == 0 else (1.5,)
                for j, beat in enumerate(offsets):
                    p = s['tonic'] + s['motif'][(i+j) % 4]
                    events.append((bt(bar, beat), 360 if j else 540, p, name))
    return sorted(events)


def chord_for(s, bar, lead):
    """Choose from the authored palette, avoiding sustained semitone clashes with the theme."""
    preferred = (bar - 9) % len(s['chords'])
    sounding = [(p % 12, min(t+d, bt(bar+1))-max(t, bt(bar)))
                for t, d, p, _ in lead if t < bt(bar+1) and t+d > bt(bar)]
    def score(item):
        i, name = item
        root, _, voice = CHORDS[name]
        chord = {p % 12 for p in voice} | {root % 12}
        cost = sum(weight * (0 if pc in chord else 2 if any((pc-v) % 12 in (1, 11) for v in chord) else 0.7)
                   for pc, weight in sounding)
        return cost, (i-preferred) % len(s['chords'])
    return min(enumerate(s['chords']), key=score)[1] if sounding else s['chords'][preferred]


def compose(sid):
    s = next(s for s in SKETCHES if s['sid'] == sid)
    rng = random.Random(1030 + s['index'])
    house = s['genre'] == 'deep house'
    nt, cc = {i: [] for i in range(6)}, {i: [] for i in range(6)}
    pcs = {0: 16 if house else 0, 1: 38 if house else 33, 2: 4, 3: 89,
           4: s['lead'], 5: s['reprise']}
    lead = melody(s)
    jitter = 8 if house else 12
    def note(tr, t, d, p, v, lo, hi):
        t = max(0, t + rng.randint(-jitter, jitter))
        d = min(d, s['bars']*BAR-t-12)
        if d > 0:
            nt[tr].append((t, d, p, max(lo, min(hi, v+rng.randint(-8 if house else -10, 8 if house else 10)))))
    for bar in range(1, s['bars']+1):
        start, sec = section_at(s, bar)
        root, _, voice = CHORDS[chord_for(s, bar, lead)]
        isbreak, outro = sec == 'break', sec == 'outro'
        drum = bar >= 5 and not isbreak and bar <= s['bars']-4
        hats = bar >= 3 and (not isbreak or s['break_layer'] == 'hats') and bar <= s['bars']-4
        bass = bar >= 9 and (not isbreak or s['break_layer'] == 'bass') and bar <= s['bars']-4
        keys = not isbreak or s['break_layer'] == 'keys'
        pad = house or (isbreak and s['break_layer'] == 'pad')
        kicks = (0, 1, 2, 3) if house else ((0, 1.5, 2.75), (0, 2.5), (0, 1.75), (0, 2.5, 2.75))[(bar+s['index']) % 4]
        if drum:
            for k in kicks:
                low, high = ((106, 112) if k == 0 else (100, 105)) if house else ((104, 110) if k == 0 else (96, 103))
                note(0, bt(bar, k), 90, 36, high-2, low, high)
            for b in (1, 3):
                note(0, bt(bar, b), 100, 38, 94, 88 if house else 86, 100)
            if not house:
                note(0, bt(bar, 3.75), 65, 38, 45, 38, 52)
        if hats:
            for j in range(8):
                off = j % 2
                op = j in (3, 7) if house else j == 7 and bar % 4 == 0
                pitch = 46 if op else (51 if house and sec == 'reprise' and not off else 42)
                low, high = ((65, 80) if op else (60, 75) if pitch == 51 else (74, 90) if off else (50, 62)) if house else ((68, 84) if off else (48, 60))
                note(0, bt(bar, j/2)+(28 if off else 0), 180 if op else 85, pitch, (low+high)//2, low, high)
        if bass:
            places = (0.5,) if house else kicks[:-1]
            for off in places:
                note(1, bt(bar, off), 1100 if house else 600, root, 73, 60, 82)
        if keys:
            voicing = [p+12 for p in voice] if house else [p-12 if p > 72 else p for p in voice]
            for j, off in enumerate(s['comp']):
                t = bt(bar, off)
                stop = bt(bar, s['comp'][j+1]) if j+1 < len(s['comp']) else bt(bar+1)
                for p in voicing:
                    note(2, t, stop-t-70, p, 82, 72, 92)
                cc[2].extend([(max(0, t-20), 64, 0), (t+24, 64, 100), (stop-25, 64, 0)])
        if pad and not outro:
            r = root+24
            for p in (r, r+7):
                note(3, bt(bar), BAR-40, p, 62 if house else 53, 55 if house else 45, 72 if house else 60)
        if bar == start and sec == 'reprise':
            note(0, bt(bar, 0.25), 360, 49, 67, 60, 74 if house else 70)
        if house and bar+1 in [b for b, n in sections(s) if n in ('break', 'reprise', 'outro')]:
            for beat, p in ((3.25, 45), (3.75, 41)):
                note(0, bt(bar, beat), 80, p, 77, 68, 88)
    for t, d, p, sec in lead:
        tr = 5 if sec in ('reprise', 'answer2') else 4
        note(tr, t, d, p, 83 if house else 75, 72 if house else 60, 92 if house else 82)
    for tr in (4, 5):
        if pcs[tr] in (0, 4):
            for t, d, _, _ in nt[tr]:
                cc[tr].extend([(max(0, t-2), 64, 0), (t+12, 64, 90), (t+d, 64, 0)])
    for tr in (2, 4, 5):
        cc[tr].append((s['bars']*BAR-1, 64, 0))
    for tr, ns in nt.items():
        ns.sort()
        by_pitch = defaultdict(list)
        for i, n in enumerate(ns):
            by_pitch[n[2]].append(i)
        for ids in by_pitch.values():
            for a, b in zip(ids, ids[1:]):
                t, d, p, v = ns[a]
                ns[a] = (t, min(d, max(1, ns[b][0]-t-1)), p, v)
    m = MOVEMENTS[s['key']]
    return nt, cc, pcs, s['bars'], s['bpm'], s['title'], m['ks'][0], 'minor' in m['key_name']


def render(s):
    nt, cc, pcs, bars, bpm, title, sf, minor = compose(s['sid'])
    smf = build_smf(title, bpm, sf, minor, bars, TRACKS, pcs, nt, cc,
                    sections(s) + [(1, CREDIT)])
    check(s, nt, cc, smf)
    return smf


def check(s, nt, cc, smf):
    end = s['bars']*BAR
    assert abs(s['bpm']/MOVEMENTS[s['key']]['tempo_bpm']-1) >= .15
    assert all(0 <= t < t+d <= end and 0 < v <= 127 and 0 <= p <= 127
               for ns in nt.values() for t, d, p, v in ns)
    theme_bars = sum(section_at(s, b)[1] in ('theme', 'reprise') for b in range(1, s['bars']+1))
    ratio = theme_bars/s['bars']
    assert .4 <= ratio <= .6
    # Compare onset patterns after equal meter/grid normalization, BEFORE humanization.
    ph, length = phrase(s)
    assert all(d >= 60 for _, d, _ in ph), 'Rhythm shift produced a near-zero note'
    a, z = s['theme_window']
    origin = bar_tick(s['key'], a)
    m = MOVEMENTS[s['key']]
    scale = {(4, 4): 1, (3, 4): 4/3, (3, 8): 4/3, (12, 8): 2/3}[m['ts']]
    raw = sorted({round((t-origin)*scale/240)*240 for t, d, p in m['parts'][s['theme_part']]
                  if origin <= t < bar_tick(s['key'], z+1)})
    run = longest = 0
    for b in range(length//BAR):
        old = [t-b*BAR for t in raw if b*BAR <= t < (b+1)*BAR]
        new = [t-b*BAR for t, d, p in ph if b*BAR <= t < (b+1)*BAR]
        run = run+1 if old and old == new else 0
        longest = max(longest, run)
    assert longest <= 4
    for ns in nt.values():
        previous = {}
        for t, d, p, v in ns:
            assert t >= previous.get(p, -1), (s['sid'], p, t)
            previous[p] = t+d
    assert all(72 <= v <= 92 for _, _, _, v in nt[2])
    assert cc[2][-1][2] == 0
    fmt, tracks, division, parsed = parse_smf(smf)
    assert (fmt, tracks, division) == (1, 7, PPQ)
    assert sum(x['notes'] for x in parsed) == sum(map(len, nt.values()))
    bands = {str(p): [min(n[3] for n in nt[0] if n[2] == p), max(n[3] for n in nt[0] if n[2] == p)]
             for p in sorted({n[2] for n in nt[0]})}
    active = {t//BAR for t, d, p, name in melody(s) if name in ('theme', 'reprise')}
    print(f"check {s['sid']} PASS unchanged_run={longest} theme_sections={ratio:.1%} "
          f"theme_onset_bars={len(active)}/{s['bars']} drums={bands} keys=72..92 "
          f"last={max(t+d for ns in nt.values() for t,d,p,v in ns)}/{end}")


def verify_audio():
    """Read-only PCM proof: duration, both-channel peaks, sections, and note-aware dropouts."""
    import audioop
    import hashlib
    import math
    import mmap
    import re
    from pipeline import BOUNCE_DIR, PROJ_DIR
    from render_tide_variants import wave_data
    reports = []
    for s in SKETCHES:
        path = os.path.join(BOUNCE_DIR, s['sid']+'-v1.wav')
        assert os.path.isdir(os.path.join(PROJ_DIR, s['title']+' v1.logicx'))
        nt = compose(s['sid'])[0]
        seconds_per_tick = 60 / s['bpm'] / PPQ
        expected = s['bars']*BAR*seconds_per_tick
        active = []
        for a, z in sorted((t*seconds_per_tick, (t+d)*seconds_per_tick)
                           for ns in nt.values() for t,d,p,v in ns):
            if active and a <= active[-1][1]:
                active[-1][1] = max(z, active[-1][1])
            else:
                active.append([a, z])
        with open(path, 'rb') as f:
            begin, size, rate, channels, bits = wave_data(f)
            assert channels == 2 and bits == 24 and rate in (44100, 48000)
            assert size % 6 == 0 and os.fstat(f.fileno()).st_size >= begin+size, 'Truncated PCM data'
            frames = size//6
            duration = frames/rate
            # Logic includes a release tail; never accept a missing final musical bar.
            assert expected-.1 <= duration <= expected+12, (s['sid'], duration, expected)
            with mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ) as mm:
                def rms(a, z):
                    first, last = round(a*rate), min(frames, round(z*rate))
                    energy = count = 0
                    for at in range(begin+first*6, begin+last*6, 393216):
                        raw = mm[at:min(at+393216, begin+last*6)]
                        n = len(raw)//3
                        energy += audioop.rms(raw, 3)**2*n
                        count += n
                    return round(20*math.log10(max(math.sqrt(energy/count)/8388608, 1e-15)), 2)
                peaks = [0, 0]
                for at in range(begin, begin+size, 393216):
                    raw = mm[at:min(at+393216, begin+size)]
                    for ch in (0, 1):
                        peaks[ch] = max(peaks[ch], audioop.max(audioop.tomono(raw, 3, 1-ch, ch), 3))
                zeros, unexpected = [], []
                for hit in re.compile(b'\x00{6,}').finditer(mm, begin, begin+size):
                    a = (hit.start()-begin+5)//6/rate
                    z = (hit.end()-begin)//6/rate
                    if z-a >= .1:
                        zeros.append([round(a, 4), round(z, 4)])
                        if any(x < z and y > a for x, y in active):
                            unexpected.append(zeros[-1])
                levels = {}
                boundaries = {}
                for b, name in sections(s):
                    nextbar = next((x for x, _ in sections(s) if x > b), s['bars']+1)
                    a, z = bt(b)*seconds_per_tick, bt(nextbar)*seconds_per_tick
                    levels[name] = rms(a, z)
                    if b > 1:
                        boundaries[name] = round(rms(a, a+.5)-rms(max(0, a-.5), a), 2)
                report = dict(sid=s['sid'], seconds=round(duration, 3), expected_seconds=round(expected, 3),
                    sample_rate=rate, channels=channels, bits=bits,
                    peak_dbfs=[round(20*math.log10(max(x/8388608, 1e-15)), 3) for x in peaks],
                    section_rms_dbfs=levels, boundary_delta_db=boundaries,
                    zero_runs=zeros, unexpected_zero_runs=unexpected, sha256=hashlib.sha256(mm).hexdigest())
                assert max(peaks)/8388608 <= 10**(-.1/20)+1/8388608, report
                assert min(peaks)/8388608 > 10**(-70/20), ('Silent stereo channel', report)
                assert not unexpected and min(levels.values()) > -70, report
                reports.append(report)
                print(json.dumps(report, ensure_ascii=False))
    return reports


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument('--check', action='store_true')
    mode.add_argument('--verify-audio', action='store_true')
    args = parser.parse_args()
    if args.verify_audio:
        verify_audio()
        raise SystemExit(0)
    assert len(SKETCHES) == len({s['sid'] for s in SKETCHES}) == 12
    signatures = set()
    for s in SKETCHES:
        lead = melody(s)
        chords = [CHORDS[chord_for(s, bar, lead)] for bar in range(9, 25)]
        signature = tuple(((root-chords[0][0]) % 12, quality) for root, quality, _ in chords)
        assert signature not in signatures, f"Transposed harmonic clone: {s['sid']}"
        signatures.add(signature)
    print(f'normalized_16bar_harmony_signatures={len(signatures)} PASS')
    for spec in SKETCHES:
        data = render(spec)
        path = os.path.join(SK_DIR, spec['sid']+'-v1.mid')
        if args.check:
            with open(path, 'rb') as midi:
                assert midi.read() == data, f"Stale MIDI: {path}"
            print(f"{spec['sid']} deterministic MIDI PASS")
        else:
            print(write_smf(path, data))
