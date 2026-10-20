"""Astra's ten v2 layer recipes, retaining each v1 harmony and bass cell.

The four-bar break preserves each slot's contrasting original break rooms.
Slot 1's pitched events retain the original calibration exactly.
"""
import os

import dh_astra as v1
from pipeline import BAR, PPQ, SK_DIR, SW, bt, build_smf, hum_t, hum_v, seed, write_smf
from sketches import PC, mk_chord2

TRACKS = [('Drums', 9), ('Bass', 0), ('Keys', 1), ('Pad', 2), ('Tex', 3), ('Perc', 9)]
MARKERS = [(1, 'intro'), (9, 'A'), (37, 'break'), (41, 'A2'), (57, 'outro')]
SKETCHES = [dict(sp, pad=True, key_v=80, held=True) for sp in v1.SKETCHES]
SHAKER, CONGA_HIGH, CONGA_LOW = 82, 63, 64


def is_a(bar):
    return 9 <= bar <= 36 or 41 <= bar <= 56


def active_parts(sp, bar):
    """Compress the original break into two two-bar rooms."""
    source_bar = (33, 34, 37, 38)[bar - 37] if 37 <= bar <= 40 else 1
    return v1.active_parts(sp, source_bar)

def compose(sid):
    """Return nt, cc, pcs, n_bars, bpm, title, keysig_sf, minor."""
    sp = next(item for item in SKETCHES if item['sid'] == sid)
    original, _, _, n_bars, bpm, title, keysig_sf, minor = v1.compose(sid)
    nt = {i: [] for i in range(len(TRACKS))}
    cc = {i: [] for i in range(len(TRACKS))}
    pcs = {0: 25, 1: sp['bass_pc'], 2: sp['key_pc'], 3: 89, 4: 4, 5: 25}
    for bar in range(1, n_bars + 1):
        source_bar = (bar - 8 if 33 <= bar <= 36 else
                      (33, 34, 37, 38)[bar - 37] if 37 <= bar <= 40 else bar)
        for tick, duration, pitch, velocity in original[0]:
            if bt(source_bar) <= tick < bt(source_bar + 1):
                if pitch != v1.KICK or bar >= 5:
                    nt[0].append((tick + (bar - source_bar) * BAR,
                                  duration, pitch, velocity))
        if 'bass' in active_parts(sp, bar):
            # Keep the existing cell and humanization wherever it already plays.
            bass_bar = bar if 'bass' in v1.active_parts(sp, bar) else bar - 8
            nt[1].extend((tick + (bar - bass_bar) * BAR, duration, pitch, velocity)
                         for tick, duration, pitch, velocity in original[1]
                         if bt(bass_bar) <= tick < bt(bass_bar + 1))
    nt[0].sort()
    root = mk_chord2(PC[sp['root']], 'm7')['bass']
    pad_voicing = (root + 24, root + 31, root + 38)
    seed(22000 + sp['slot'])

    def add(track, bar, beat, length, pitch, velocity, jitter=0, swing=False):
        onset = bt(bar, beat) + (SW if swing else 0)
        onset = max(bt(bar), min(bt(bar + 1) - 1, hum_t(onset, jitter)))
        stop = min(onset + int(length * PPQ), bt(bar + 1) - 12)
        nt[track].append((onset, stop - onset, pitch, velocity))

    for bar in range(1, n_bars + 1):
        parts = active_parts(sp, bar)
        if bar <= 56 and 'pad' in parts:
            velocity = hum_v(63, 7)
            for pitch in pad_voicing:
                add(3, bar, 0, 3.95, pitch, velocity)
        voicing = tuple(pitch + 12 for pitch in v1.chord_at(sp, bar))
        if 9 <= bar <= 56 and 'keys' in parts:
            velocity = hum_v(sp['key_v'] + (4 if bar >= 41 else 0), 8)
            for pitch in voicing:
                add(2, bar, 0, 3.95, pitch, velocity)
            cc[2].extend(((bt(bar), 64, 100), (bt(bar + 1) - 8, 64, 0)))
        if not is_a(bar):
            continue

        # Chord tones cycle within one octave; there is no separate lead phrase.
        texture = tuple(min(voicing) + (pitch - min(voicing)) % 12 for pitch in voicing)
        for step in range(8):
            add(4, bar, step / 2, 0.43, texture[step % len(texture)],
                hum_v(62, 7), 5, step % 2 == 1)
        cc[4].extend(((bt(bar), 64, 90), (bt(bar + 1) - 8, 64, 0)))
        for step in range(16):
            add(5, bar, step / 4, 0.09, SHAKER,
                hum_v(47 if step % 2 == 0 else 43, 5), 6, step % 4 == 2)
        congas = ((1.5, CONGA_LOW), (3.25, CONGA_HIGH)) if bar % 2 else (
            (0.75, CONGA_HIGH), (2.5, CONGA_LOW), (3.75, CONGA_HIGH))
        for beat, pitch in congas:
            add(5, bar, beat, 0.16, pitch, hum_v(47, 5), 6, beat % 1 == 0.5)
    return nt, cc, pcs, n_bars, bpm, title, keysig_sf, minor


def range_check(sp, nt, cc):
    """Assert layer bounds, entrances, and each slot's four-bar break."""
    ranges = {}
    first = {}
    for track, (name, _) in enumerate(TRACKS):
        velocities = [velocity for _, _, _, velocity in nt[track]]
        ranges[name] = (min(velocities), max(velocities))
        first[name] = min(tick for tick, _, _, _ in nt[track]) // BAR + 1
        assert all(0 <= tick < tick + duration < bt(65)
                   for tick, duration, _, _ in nt[track])
    for name, low, high in (('Keys', 72, 92), ('Pad', 55, 72),
                            ('Tex', 55, 70), ('Perc', 38, 52)):
        assert low <= ranges[name][0] <= ranges[name][1] <= high
    assert first == dict(Drums=1, Bass=9, Keys=9, Pad=1, Tex=9, Perc=9)
    assert min(t for t, _, p, _ in nt[0] if p == v1.KICK) // BAR + 1 == 5
    assert all(60 <= pitch <= 84 for _, _, pitch, _ in nt[2])
    assert {p for _, _, p, _ in nt[5]} == {SHAKER, CONGA_HIGH, CONGA_LOW}
    root = mk_chord2(PC[sp['root']], 'm7')['bass']
    for bar in range(1, 65):
        pad = [p for t, _, p, _ in nt[3] if bt(bar) <= t < bt(bar + 1)]
        assert pad == ([root + 24, root + 31, root + 38]
                       if bar <= 56 and 'pad' in active_parts(sp, bar) else [])
        keys = [n for n in nt[2] if bt(bar) <= n[0] < bt(bar + 1)]
        assert bool(keys) == (9 <= bar <= 56 and 'keys' in active_parts(sp, bar))
        for track in (4, 5):
            notes = [n for n in nt[track] if bt(bar) <= n[0] < bt(bar + 1)]
            assert bool(notes) == is_a(bar)
        if is_a(bar):
            expected = {pitch % 12 for pitch in v1.chord_at(sp, bar)}
            texture = [p for t, _, p, _ in nt[4] if bt(bar) <= t < bt(bar + 1)]
            assert {p % 12 for p in texture} == expected
            assert max(texture) - min(texture) < 12
            for track in (2, 4):
                assert (bt(bar + 1) - 8, 64, 0) in cc[track]
    assert [(t, p) for t, _, p, _ in nt[0] if p == v1.CRASH] == [(bt(41), v1.CRASH)]
    for bar in range(37, 41):
        assert all(p != v1.OPEN_HAT or 'hats' in active_parts(sp, bar)
                   for t, _, p, _ in nt[0] if bt(bar) <= t < bt(bar + 1))
    velocities = ' '.join(f'{name.lower()}_vel={ranges[name][0]}..{ranges[name][1]}'
                          for name in ('Keys', 'Pad', 'Tex', 'Perc'))
    entrances = ' '.join(f'{name.lower()}_first_bar={first[name]}' for name, _ in TRACKS)
    return f"range-check {sp['sid']} PASS {velocities} {entrances} kick_first_bar=5"


if __name__ == '__main__':
    os.makedirs(SK_DIR, exist_ok=True)
    for sketch in SKETCHES:
        nt, cc, pcs, n_bars, bpm, title, keysig_sf, minor = compose(sketch['sid'])
        line = range_check(sketch, nt, cc)
        smf = build_smf(title, bpm, keysig_sf, minor, n_bars, TRACKS, pcs, nt, cc, MARKERS)
        print(write_smf(os.path.join(SK_DIR, sketch['sid'] + '-v2.mid'), smf))
        print(line)
