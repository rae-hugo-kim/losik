"""Slot 1 v3: separated Tough Kit accents; all v2 pitched events unchanged."""
import os

import dh_astra_v2 as v2
from pipeline import BAR, PPQ, SK_DIR, SW, bt, build_smf, hum_t, hum_v, seed, write_smf

SKETCHES = v2.SKETCHES
TRACKS = v2.TRACKS
MARKERS = v2.MARKERS
KICK, SNARE, CLAP, HAT, OPEN_HAT, RIDE = 36, 38, 39, 42, 46, 51
TOMS = (45, 47, 50)
CONGAS = (63, 64)
FILL_BARS = (16, 36, 56)


def compose(sid):
    """Replace only v2's drum/percussion lists and their kit programs."""
    nt, cc, pcs, n_bars, bpm, title, keysig_sf, minor = v2.compose(sid)
    sp = next(item for item in SKETCHES if item['sid'] == sid)
    # Keep the return crash and original backbeat entrance as arrangement cues.
    crash = [note for note in nt[0] if note[2] == v2.v1.CRASH]
    nt[0] = crash
    nt[5] = []
    pcs[0], pcs[5] = 16, 0
    seed(32000 + sp['slot'])

    def velocity(base, low, high):
        return max(low, min(high, hum_v(base, 8)))

    def add(track, bar, beat, pitch, vel, duration=60):
        nominal = bt(bar, beat) + (SW if beat % 1 == 0.5 else 0)
        onset = max(bt(bar), hum_t(nominal, 8))
        nt[track].append((onset, duration, pitch, vel))
        return onset

    for bar in range(1, n_bars + 1):
        # The v2 sub-only break remains silent on both percussion tracks.
        if 37 <= bar <= 40:
            continue
        if bar >= 5:
            base = velocity(103, 100, 106)
            for beat in range(4):
                add(0, bar, beat, KICK, base + (6 if beat == 0 else 0), 86)
        for beat in range(4):
            add(0, bar, beat, HAT, velocity(56, 50, 62), 48)
        # Open hats replace (not double) closed hats on &2 and &4.
        for beat in (0.5, 2.5):
            add(0, bar, beat, HAT, velocity(82, 74, 90), 48)
        for beat in (1.5, 3.5):
            add(0, bar, beat, OPEN_HAT,
                velocity(74 if 41 <= bar <= 56 else 71, 65, 80), 180)
        if bar >= sp['back_start']:
            for beat in (1, 3):
                onset = add(0, bar, beat, SNARE, velocity(94, 88, 100), 67)
                nt[0].append((onset, 67, CLAP, velocity(86, 80, 92)))
        if 41 <= bar <= 56:
            for beat in range(4):
                add(0, bar, beat, RIDE, velocity(67, 60, 75), 100)
        if bar in FILL_BARS:
            # Two sixteenths leave the &4 open hat its full 180-tick tail.
            add(0, bar, 3.25, 50 if bar == 16 else 47, velocity(88, 80, 96))
            add(0, bar, 3.75, 45, velocity(94, 86, 102))
        if v2.is_a(bar):
            cell = ((0.75, 63), (2.75, 64)) if bar % 2 else ((1.75, 63),)
            for beat, pitch in cell:
                add(5, bar, beat, pitch, velocity(77, 70, 85), 72)
    nt[0].sort()
    nt[5].sort()
    return nt, cc, pcs, n_bars, bpm, title, keysig_sf, minor


def smf_chunks(smf):
    """Extract encoded tracks so equality also covers their exact MIDI bytes."""
    pos = 14
    chunks = []
    while pos < len(smf):
        size = int.from_bytes(smf[pos + 4:pos + 8], 'big') + 8
        chunks.append(smf[pos:pos + size])
        pos += size
    return chunks


def range_check(sid, result, smf):
    nt, cc, pcs, n_bars, bpm, title, keysig_sf, minor = result
    original = v2.compose(sid)
    old_nt, old_cc, old_pcs = original[:3]
    assert result[3:] == original[3:]
    assert pcs[0] == 16 and pcs[5] == 0
    assert cc == old_cc
    old_smf = build_smf(title, bpm, keysig_sf, minor, n_bars,
                        v2.TRACKS, old_pcs, old_nt, old_cc, v2.MARKERS)
    chunks, old_chunks = smf_chunks(smf), smf_chunks(old_smf)
    assert chunks[0] == old_chunks[0]
    for track in (1, 2, 3, 4):
        assert nt[track] == old_nt[track]
        assert pcs[track] == old_pcs[track]
        assert chunks[track + 1] == old_chunks[track + 1]
    assert {note[2] for note in nt[5]} == set(CONGAS)
    assert {note[2] for note in nt[0]} == {
        KICK, SNARE, CLAP, HAT, OPEN_HAT, RIDE, *TOMS, v2.v1.CRASH}
    assert all(0 <= tick < tick + duration < bt(n_bars + 1)
               for notes in nt.values() for tick, duration, _, _ in notes)

    def step(note):
        return round((note[0] % BAR) / (PPQ / 4))

    groups = {
        'kick': [n for n in nt[0] if n[2] == KICK],
        'closed-hat_on-beat': [n for n in nt[0] if n[2] == HAT and step(n) % 4 == 0],
        'closed-hat_off-beat': [n for n in nt[0] if n[2] == HAT and step(n) % 4 == 2],
        'open-hat': [n for n in nt[0] if n[2] == OPEN_HAT],
        'snare': [n for n in nt[0] if n[2] == SNARE],
        'clap': [n for n in nt[0] if n[2] == CLAP],
        'ride': [n for n in nt[0] if n[2] == RIDE],
        'tom': [n for n in nt[0] if n[2] in TOMS],
        'conga': nt[5],
    }
    bounds = ((100, 112), (50, 62), (74, 90), (65, 80),
              (88, 100), (80, 92), (60, 75), (80, 102), (70, 85))
    ranges = []
    for (name, notes), (low, high) in zip(groups.items(), bounds):
        actual = min(n[3] for n in notes), max(n[3] for n in notes)
        assert low <= actual[0] <= actual[1] <= high
        ranges.append(f'{name}={actual[0]}..{actual[1]}')
    open_counts = []
    sp = next(item for item in SKETCHES if item['sid'] == sid)
    for bar in range(1, n_bars + 1):
        notes = [n for n in nt[0] if bt(bar) <= n[0] < bt(bar + 1)]
        opened = [n for n in notes if n[2] == OPEN_HAT]
        open_counts.append(len(opened))
        if 37 <= bar <= 40:
            assert not notes
            continue
        assert len(opened) == 2
        assert {step(n) for n in opened} == {6, 14}
        assert all(n[1] == 180 for n in opened)
        hats = [n for n in notes if n[2] == HAT]
        assert {step(n) for n in hats} == {0, 2, 4, 8, 10, 12}
        kicks = [n for n in notes if n[2] == KICK]
        assert len(kicks) == (4 if bar >= 5 else 0)
        if kicks:
            assert {step(n) for n in kicks} == {0, 4, 8, 12}
            assert all(kicks[0][3] == n[3] + 6 for n in kicks[1:])
        snares = [n for n in notes if n[2] == SNARE]
        claps = [n for n in notes if n[2] == CLAP]
        assert len(snares) == len(claps) == (2 if bar >= sp['back_start'] else 0)
        assert [n[0] for n in snares] == [n[0] for n in claps]
        if snares:
            assert {step(n) for n in snares} == {4, 12}
        rides = [n for n in notes if n[2] == RIDE]
        assert len(rides) == (4 if 41 <= bar <= 56 else 0)
        toms = [n for n in notes if n[2] in TOMS]
        assert len(toms) == (2 if bar in FILL_BARS else 0)
        assert all(step(n) in (13, 15) for n in toms)
    for bar in range(1, n_bars + 1, 2):
        cell = [n for n in nt[5] if bt(bar) <= n[0] < bt(bar + 2)]
        assert len(cell) == (3 if v2.is_a(bar) else 0)
    for track in (0, 5):
        for note in nt[track]:
            bar = note[0] // BAR + 1
            beat = step(note) / 4
            nominal = bt(bar, beat) + (SW if beat % 1 == 0.5 else 0)
            assert abs(note[0] - nominal) <= 8
    return (
        f"drum-range {sid} PASS {' '.join(ranges)} "
        f"open-hat_count_per_bar={','.join(map(str, open_counts))} "
        'drums_pc=16 perc_pc=0 shaker=0 kick_accent=+6 timing=+/-8',
        f'non-drum-check {sid} PASS Bass/Keys/Pad/Tex byte-identical_to_v2=True '
        'note_lists=equal cc=equal pcs=equal encoded_tracks=equal structure=equal',
    )


if __name__ == '__main__':
    os.makedirs(SK_DIR, exist_ok=True)
    for sketch in SKETCHES:
        sid = sketch['sid']
        result = compose(sid)
        nt, cc, pcs, n_bars, bpm, title, keysig_sf, minor = result
        smf = build_smf(title, bpm, keysig_sf, minor, n_bars, TRACKS, pcs, nt, cc, MARKERS)
        lines = range_check(sid, result, smf)
        print(write_smf(os.path.join(SK_DIR, sid + '-v3.mid'), smf))
        for line in lines:
            print(line)
