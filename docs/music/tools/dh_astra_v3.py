"""Astra's ten v3 tracks: v2 harmonic layers and separated Tough Kit drums."""
import os
from collections import Counter

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
        parts = v2.active_parts(sp, bar)
        if 'kick' in parts and bar >= 5:
            base = velocity(103, 100, 106)
            for beat in range(4):
                accent = base + 6 if beat == 0 else min(base, 105)
                add(0, bar, beat, KICK, accent, 86)
        if 'hats' in parts:
            for beat in range(4):
                # Consume the calibrated random draws before removing A2 hats.
                add(0, bar, beat, HAT, velocity(56, 50, 62), 48)
            # Open hats replace (not double) closed hats on &2 and &4.
            for beat in (0.5, 2.5):
                add(0, bar, beat, HAT, velocity(82, 74, 90), 48)
            for beat in (1.5, 3.5):
                add(0, bar, beat, OPEN_HAT,
                    velocity(74 if 41 <= bar <= 56 else 71, 65, 80), 180)
        if 'back' in parts and bar >= sp['back_start']:
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
    nt[0] = [note for note in nt[0]
             if not (note[2] == HAT and bt(41) <= note[0] < bt(57)
                     and round((note[0] % BAR) / (PPQ / 4)) % 4 == 0)]
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
        'kick_beat1': [n for n in nt[0] if n[2] == KICK and step(n) == 0],
        'kick_beats2-4': [n for n in nt[0] if n[2] == KICK and step(n) != 0],
        'closed-hat_on-beat': [n for n in nt[0] if n[2] == HAT and step(n) % 4 == 0],
        'closed-hat_off-beat': [n for n in nt[0] if n[2] == HAT and step(n) % 4 == 2],
        'open-hat': [n for n in nt[0] if n[2] == OPEN_HAT],
        'snare': [n for n in nt[0] if n[2] == SNARE],
        'clap': [n for n in nt[0] if n[2] == CLAP],
        'ride': [n for n in nt[0] if n[2] == RIDE],
        'tom': [n for n in nt[0] if n[2] in TOMS],
        'conga': nt[5],
    }
    bounds = ((106, 112), (100, 105), (50, 62), (74, 90), (65, 80),
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
        parts = v2.active_parts(sp, bar)
        assert len(opened) == (2 if 'hats' in parts else 0)
        if opened:
            assert {step(n) for n in opened} == {6, 14}
            assert all(n[1] == 180 for n in opened)
        hats = [n for n in notes if n[2] == HAT]
        expected_hats = ({2, 10} if 41 <= bar <= 56 else {0, 2, 4, 8, 10, 12})
        assert {step(n) for n in hats} == (expected_hats if 'hats' in parts else set())
        assert all(step(n) != 15 for n in hats)
        kicks = [n for n in notes if n[2] == KICK]
        assert len(kicks) == (4 if bar >= 5 and 'kick' in parts else 0)
        if kicks:
            assert {step(n) for n in kicks} == {0, 4, 8, 12}
            assert all(kicks[0][3] >= n[3] + 6 for n in kicks[1:])
        snares = [n for n in notes if n[2] == SNARE]
        claps = [n for n in notes if n[2] == CLAP]
        assert len(snares) == len(claps) == (
            2 if bar >= sp['back_start'] and 'back' in parts else 0)
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
    assert min(n[0] for n in nt[3]) == 0
    assert {n[0] // BAR + 1 for n in nt[4]} == {
        bar for bar in range(1, n_bars + 1) if v2.is_a(bar)}
    layer_ranges = []
    for track, low, high in ((2, 72, 92), (3, 55, 72), (4, 55, 70)):
        velocities = [n[3] for n in nt[track]]
        assert low <= min(velocities) <= max(velocities) <= high
        layer_ranges.append(f'{TRACKS[track][0]}={min(velocities)}..{max(velocities)}')
    for bar in range(1, n_bars + 1):
        parts = v2.active_parts(sp, bar)
        for track, active in ((2, 9 <= bar <= 56 and 'keys' in parts),
                              (3, bar <= 56 and 'pad' in parts)):
            notes = [n for n in nt[track] if bt(bar) <= n[0] < bt(bar + 1)]
            assert bool(notes) == active
        if v2.is_a(bar):
            texture = [n[2] for n in nt[4] if bt(bar) <= n[0] < bt(bar + 1)]
            assert max(texture) - min(texture) < 12
    total = sum(len(notes) for notes in nt.values())
    last = max(t + d for notes in nt.values() for t, d, _, _ in notes)
    return (
        f"check {sid} PASS {' '.join(ranges)} "
        f"open-hat_per_bar_outside_break=2 break={open_counts[36:40]} "
        f"ride_bars=41-56 tom_bars=16,36,56 step15_hats=0 A2_onbeat_hats=0 "
        f"pad_first_bar=1 Tex=A/A2 {' '.join(layer_ranges)} "
        f"non_drums_v2=byte-identical notes={total} last_note_end_bar={last / BAR:.3f}"
    )


def note_on_events(chunk):
    """Read emitted note-on events for an exact before/after calibration diff."""
    data = chunk[8:]
    pos = tick = 0
    events = Counter()
    while pos < len(data):
        delta = 0
        while True:
            value = data[pos]
            pos += 1
            delta = (delta << 7) | (value & 127)
            if value < 128:
                break
        tick += delta
        status = data[pos]
        if status == 0xFF:
            pos += 3 + data[pos + 2]
        elif status & 0xF0 in (0xC0, 0xD0):
            pos += 2
        else:
            if status & 0xF0 == 0x90 and data[pos + 2]:
                events[(tick, data[pos + 1], data[pos + 2])] += 1
            pos += 3
    return events


def calibration_diff(before, after):
    old, new = smf_chunks(before), smf_chunks(after)
    assert all(old[i] == new[i] for i in (0, 2, 3, 4, 5))
    changes = []
    for index, name in ((1, 'Drums'), (6, 'Perc')):
        previous, current = note_on_events(old[index]), note_on_events(new[index])
        removed, added = previous - current, current - previous
        for label, events in (('removed', removed), ('added', added)):
            pitches = Counter()
            for (_, pitch, _), count in events.items():
                pitches[pitch] += count
            changes.append(f'{name}_{label}={dict(sorted(pitches.items()))}')
    return (f"calibration-diff dh01-unlit-threshold byte_identical={before == after} "
            f"{' '.join(changes)} non_drums_and_conductor_byte_identical=True")


if __name__ == '__main__':
    calibration_path = os.path.join(SK_DIR, SKETCHES[0]['sid'] + '-v3.mid')
    with open(calibration_path, 'rb') as calibration:
        before = calibration.read()
    os.makedirs(SK_DIR, exist_ok=True)
    for sketch in SKETCHES:
        sid = sketch['sid']
        result = compose(sid)
        nt, cc, pcs, n_bars, bpm, title, keysig_sf, minor = result
        smf = build_smf(title, bpm, keysig_sf, minor, n_bars, TRACKS, pcs, nt, cc, MARKERS)
        line = range_check(sid, result, smf)
        if sketch['slot'] == 1:
            print(calibration_diff(before, smf))
        print(write_smf(os.path.join(SK_DIR, sid + '-v3.mid'), smf))
        print(line)
