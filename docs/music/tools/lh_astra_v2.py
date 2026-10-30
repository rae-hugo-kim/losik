"""Slot 1 density calibration; retain the v1 harmony, groove and lead motif."""
import os
from collections import Counter

import lh_astra as v1
from pipeline import BAR, PPQ, SK_DIR, bt, build_smf, hum_t, hum_v, seed, write_smf
from sketches import PC, mk_chord2

SKETCHES = [s for s in v1.SKETCHES if s['slot'] == 1]
TRACKS = [('Drums', 9), ('Bass', 0), ('Keys', 1), ('Keys2', 2),
          ('Tex', 3), ('Lead', 4), ('Pad', 5)]
FILL_BARS = tuple(sorted((set(range(4, 57, 4)) - {28, 56}) | {31}))
COMP = ((0, .75, 1.5, 2.25, 3.25), (.5, 1.25, 2, 2.75, 3.5),
        (0, .75, 1.5, 2.25, 3.25), (0, .75, 1.5, 2.25, 3.25))
BASS_BEATS = ((0, .75, 1.75, 2.5, 3.5), (0, .75, 1.75, 2.75, 3.5),
              (0, .75, 1.5, 2.5, 3.5), (0, .75, 1.5, 2.5, 3.5))


def compose(sid):
    s = next(s for s in SKETCHES if s['sid'] == sid)
    original = v1.compose(sid)
    seed(261030 + s['slot'])
    nt = {i: [] for i in range(7)}
    cc = {i: [] for i in range(7)}
    pcs = {0: 0, 1: 33, 2: s['keys_pc'], 3: 0, 4: 24, 5: s['lead_pc'], 6: 89}
    # Keep the original kick/backbeat onsets, pitches and accents exactly.
    nt[0] = [n for n in original[0][0] if n[2] != 49
             and not (n[0] < bt(3) and n[2] in (42, 46))]
    nt[5] = list(original[0][4])

    def tick(bar, beat, swung=False):
        delay = s['swing'] if swung and beat % 1 == .5 else 0
        return hum_t(bt(bar, beat) + 14 + delay, 12)

    def vel(base, low, high):
        return max(low, min(high, hum_v(base, 10)))

    def add(track, bar, when, duration, pitch, velocity):
        end = min(when + duration, bt(bar + 1) - 24)
        assert bt(bar) <= when < end
        nt[track].append((when, end - when, pitch, velocity))

    for bar in range(1, s['bars'] + 1):
        phase = (bar - 1) % 4
        _, root, quality, chord = s['chords'][s['order'][phase]]
        layers = v1.layers_at(s, bar)
        a2 = 33 <= bar <= 48

        def remove_drum_cell(cell, pitches):
            nt[0][:] = [n for n in nt[0] if not
                       (n[0] // BAR + 1 == bar and v1.event_cell(n) == cell
                        and n[2] in pitches)]

        def drum(beat, pitch, base, low, high):
            add(0, bar, tick(bar, beat, pitch in (42, 46)),
                145 if pitch == 46 else 70, pitch, vel(base, low, high))

        if 'Snare' in layers:
            drum(2.25, 38, 44, 38, 52)
        if bar in (1, 9, 25, 33, 49):
            drum(.25, 49, 62, 55, 70)
        if 'Hats' in layers and bar >= 3:
            if bar % 4 == 0:
                # Move the open hat out of beat four to leave the fill room.
                remove_drum_cell(14, (42, 46))
                remove_drum_cell(2, (42, 46))
                drum(.5, 46, 74, 68, 84)
                if a2:
                    drum(3.5, 42, 74, 68, 84)
            if bar % 8 == 0:
                for beat in (1.25, 3.25):
                    drum(beat, 42, 45, 40, 50)
        if bar in FILL_BARS:
            for beat, pitch in ((3.5, 45), (3.75, 41)):
                # A2 keeps its third ride stroke; backbeat + final tom form the fill.
                if a2 and beat == 3.5:
                    continue
                remove_drum_cell(round(beat * 4), (42, 46))
                drum(beat, pitch, 65 if beat == 3.5 else 73, 55, 82)
        if a2:
            for index, note in enumerate(nt[0]):
                when, duration, pitch, velocity = note
                cell = v1.event_cell(note)
                if when // BAR + 1 == bar and pitch == 42 and cell % 2 == 0:
                    ride_velocity = (64 + round((velocity - 68) * 6 / 16)
                                     if cell % 4 == 2 else 55 + round((velocity - 48) * 5 / 12))
                    nt[0][index] = (when, duration, 51, ride_velocity)

        if 'Bass' in layers:
            root_bass = mk_chord2(PC[root], quality)['bass']
            fifth = root_bass + 7
            while fifth > 43:
                fifth -= 12
            # D uses the fifth's octave; G uses the root's octave, within E1-C3.
            pop_low = fifth if root == 'D' else root_bass - 12
            next_root = s['chords'][s['order'][bar % 4]][1]
            approach = mk_chord2(PC[next_root], 'm7')['bass'] - 1
            third = root_bass + (3 if quality == 'm7' else 4)
            if third > 48:
                third -= 12
            pitches = (root_bass, third, pop_low + (12 if bar % 2 == 0 else 0),
                       fifth, approach)
            kick_onsets = {v1.event_cell(n) / 4: n[0] for n in nt[0]
                           if n[0] // BAR + 1 == bar and n[2] == 36}
            for index, (beat, pitch) in enumerate(zip(BASS_BEATS[phase], pitches)):
                when = kick_onsets[beat] if beat in kick_onsets else tick(bar, beat, True)
                add(1, bar, when, 210 if index else 280, pitch,
                    vel(74 if index in (0, 2) else 67, 60, 82))

        # Five light, short comp attacks fill space without holding a dense block.
        voicing = tuple(sorted(chord[1:] + (chord[0] + 12,))) if a2 else chord
        for index, beat in enumerate(COMP[phase]):
            when = tick(bar, beat, True)
            duration = 190 if index % 2 else 235
            velocity = vel(80 if index in (0, 3) else 76, 72, 92)
            for pitch in voicing:
                add(2, bar, when, duration, pitch, velocity)
            cc[2].extend(((when - 1, 64, 0), (when + 1, 64, 100),
                          (when + duration, 64, 0)))
        cc[2].extend(((bt(bar), 64, 0), (bt(bar + 1) - 2, 64, 0)))

        # Eight continuous nylon notes, with a four-bar velocity arch.
        for eighth in range(8):
            pitch = chord[s['tex_order'][(eighth + phase) % 4]]
            add(4, bar, tick(bar, eighth / 2, True), 155, pitch,
                vel((57, 63, 69, 60)[phase], 55, 72))

        # Low grand-piano preview; A2 answers the lead in two-bar pairs.
        if bar in (9, 10):
            for beat, pitch in zip(s['lead_beats'][phase], s['melody'][phase]):
                add(3, bar, tick(bar, beat, True), 185, pitch - 12, vel(64, 55, 72))
        elif a2:
            low_chord = tuple(pitch - 12 if pitch >= 62 else pitch for pitch in chord)
            # Swung eighth-note replies leave room for both motif and grace attacks.
            delayed_answer = ((bar - 33) // 4) % 2
            beats = ((0, 1, 2, 2.5), (.5, 1, 2, 3.5),
                     (0, 1, 2.5, 3 if delayed_answer else 3.5),
                     (1.5, 2, 2.5 if delayed_answer else 3, 3.5))[phase]
            pitches = ((low_chord[0], low_chord[1], low_chord[2], low_chord[1])
                       if phase < 2 else tuple(reversed(low_chord)))
            for beat, pitch in zip(beats, pitches):
                add(3, bar, tick(bar, beat, True), 170,
                    pitch, vel(69 if phase >= 2 else 58, 55, 72))

        # Rearticulation once per bar keeps the pad audible beneath the picking.
        pad_root = 48 + PC[root]
        for pitch in (pad_root, pad_root + 7, pad_root + 14):
            add(6, bar, tick(bar, 0), BAR - 48, pitch, vel(51, 45, 60))
        # The pad breathes deeply; Keys retain their foreground comping level.
        for beat in range(4):
            step = phase * 4 + beat
            pad_expression = round(40 + 5 * step if step <= 8 else 80 - 30 * (step - 8) / 7)
            keys_expression = round(76 + 3 * step if step <= 8 else 100 - 16 * (step - 8) / 7)
            cc[2].append((bt(bar, beat), 11, keys_expression))
            cc[6].append((bt(bar, beat), 11, pad_expression))

    # Preserve every v1 motif note; add a short diatonic grace from repeat two.
    lead = []
    for when, duration, pitch, _ in nt[5]:
        bar = when // BAR + 1
        phase = (bar - 1) % 4
        lead.append((when, duration, pitch, vel((65, 73, 78, 67)[phase], 60, 82)))
    nt[5] = lead
    for bar in list(range(21, 25)) + list(range(37, 49)):
        second = sorted(n for n in lead if n[0] // BAR + 1 == bar)[1]
        neighbor = second[2] - (2 if (second[2] - 2) % 12 in (0, 2, 4, 5, 7, 9, 11) else 1)
        add(5, bar, second[0] - 95, 65, neighbor, vel(63, 60, 70))
    for first in (17, 21, 33, 37, 41, 45):
        cc[5].extend(((bt(first), 1, 0), (bt(first + 3, 2), 1, 20),
                      (bt(first + 3, 3.5), 1, 40), (bt(first + 4) - 2, 1, 0)))
    for events in nt.values():
        events.sort()
    for events in cc.values():
        events.sort()
    return nt, cc, pcs, s['bars'], s['bpm'], s['title'], s['sf'], s['minor']


def bar_ranges(bars):
    groups = []
    for bar in sorted(set(bars)):
        if groups and bar == groups[-1][1] + 1:
            groups[-1][1] = bar
        else:
            groups.append([bar, bar])
    return ','.join(str(a) if a == b else f'{a}-{b}' for a, b in groups)


def check(s, result, smf):
    nt, cc, pcs, bars, bpm, title, sf, minor = result
    assert (bars, bpm, title, sf, minor) == (56, 76, s['title'], -1, True)
    assert TRACKS == [('Drums', 9), ('Bass', 0), ('Keys', 1), ('Keys2', 2),
                      ('Tex', 3), ('Lead', 4), ('Pad', 5)]
    assert pcs == {0: 0, 1: 33, 2: 4, 3: 0, 4: 24, 5: 4, 6: 89}
    by_bar = {track: Counter(n[0] // BAR + 1 for n in events) for track, events in nt.items()}
    attacks = Counter(bar for bar, _ in {(n[0] // BAR + 1, n[0]) for n in nt[2]})
    sections = [(1, 8, 'intro'), (9, 24, 'A'), (25, 32, 'break'),
                (33, 48, 'A2'), (49, 56, 'outro')]
    densities, bass_densities, key_densities = [], [], []
    for start, end, name in sections:
        count = end - start + 1
        density = sum(sum(by_bar[t][b] for t in nt) for b in range(start, end + 1)) / count
        bass_density = sum(by_bar[1][b] for b in range(start, end + 1)) / count
        key_density = sum(attacks[b] for b in range(start, end + 1)) / count
        densities.append(f'{name}:{density:.2f}')
        bass_densities.append(f'{name}:{bass_density:.2f}')
        key_densities.append(f'{name}:{key_density:.2f}')
        if name != 'outro':
            assert density >= (45 if name in ('A', 'A2') else 25)
        if name in ('A', 'A2'):
            assert bass_density >= 4
            assert all(by_bar[1][b] >= 4 and attacks[b] >= 3 for b in range(start, end + 1))
    assert set(by_bar[3]) == {9, 10} | set(range(33, 49))
    assert all(by_bar[3][bar] >= 4 for bar in range(33, 49))
    for bar in range(33, 49):
        chord = s['chords'][s['order'][(bar - 1) % 4]][3]
        riff = [n for n in nt[3] if n[0] // BAR + 1 == bar]
        assert all(n[2] % 12 in {p % 12 for p in chord} for n in riff)
        cells = [v1.event_cell(n) for n in riff]
        assert all(cell % 2 == 0 for cell in cells)
        assert all(b - a >= 2 for a, b in zip(cells, cells[1:]))
        offbeats = [n for n in riff if v1.event_cell(n) % 4 == 2]
        assert offbeats
        for note in offbeats:
            beat = v1.event_cell(note) / 4
            swing_offset = note[0] - bt(bar, beat) - 14
            assert s['swing'] - 12 <= swing_offset <= s['swing'] + 12
    response_gap = min(abs(response[0] - lead[0])
                       for response in nt[3] if bt(33) <= response[0] < bt(49)
                       for lead in nt[5])
    assert response_gap >= 120
    assert set(by_bar[4]) == set(by_bar[6]) == set(range(1, 57))
    assert all(by_bar[4][b] == 8 and by_bar[6][b] == 3 for b in range(1, 57))
    assert max(n[2] for n in nt[3]) < min(n[2] for n in nt[5])
    assert all(28 <= n[2] <= 48 and 60 <= n[3] <= 82 for n in nt[1])
    assert all(48 <= n[2] <= 72 and 72 <= n[3] <= 92 for n in nt[2])
    assert all(45 <= n[3] <= 60 for n in nt[6])
    assert max(by_bar[5].values()) <= 6
    assert max(abs(a[2] - b[2]) for a, b in zip(nt[5], nt[5][1:])) <= 7
    original = v1.compose(s['sid'])[0]
    backbone = lambda events: [n for n in events if n[2] == 36 or
                              (n[2] in (37, 38) and n[3] >= 86)]
    assert backbone(nt[0]) == backbone(original[0])
    assert {(n[0], n[1], n[2]) for n in original[4]} <= {(n[0], n[1], n[2]) for n in nt[5]}
    assert max(Counter((n[0] // BAR, v1.event_cell(n)) for n in nt[0]).values()) == 1
    fills = sorted({n[0] // BAR + 1 for n in nt[0] if n[2] in (45, 41)})
    assert fills == list(FILL_BARS)
    assert 28 not in fills and 56 not in fills
    assert {bar for bar in fills if 25 <= bar <= 32} == {31, 32}
    for bar in range(1, 57):
        drums = [n for n in nt[0] if n[0] // BAR + 1 == bar]
        if 'Snare' in v1.layers_at(s, bar):
            assert sum(n[2] == 38 and 38 <= n[3] <= 52 for n in drums) == 2
        if bar % 8 == 0 and 'Hats' in v1.layers_at(s, bar):
            assert {5, 13} <= {v1.event_cell(n) for n in drums if n[2] == 42}
        if 33 <= bar <= 48:
            assert not any(n[2] == 42 and v1.event_cell(n) % 2 == 0 for n in drums)
            rides = [n for n in drums if n[2] == 51]
            assert len(rides) >= 3
            assert all(64 <= n[3] <= 70 if v1.event_cell(n) % 4 == 2
                       else 55 <= n[3] <= 60 for n in rides)
        if 25 <= bar <= 32:
            assert not any(n[2] == 36 for n in drums) and not by_bar[1][bar]
    assert {n[0] // BAR + 1 for n in nt[0] if n[2] == 49} == {1, 9, 25, 33, 49}
    for track, expected in ((2, (76, 100, 84)), (6, (40, 80, 50))):
        for first in range(1, 57, 4):
            swell = [v for t, c, v in cc[track] if c == 11 and bt(first) <= t < bt(first + 4)]
            assert (swell[0], max(swell), swell[-1]) == expected
    overlaps = 0
    for events in nt.values():
        ends = {}
        for when, duration, pitch, velocity in events:
            assert 0 <= when < when + duration < bt(57) and 0 < velocity <= 127
            overlaps += when < ends.get(pitch, -1)
            ends[pitch] = max(ends.get(pitch, -1), when + duration)
    assert overlaps == 0
    cc1 = sum(c == 1 for events in cc.values() for _, c, _ in events)
    cc11 = sum(c == 11 for events in cc.values() for _, c, _ in events)
    assert cc1 == 24 and cc11 == 448
    for bar, text in v1.markers(bars):
        assert bytes([0xff, 6, len(text)]) + text.encode() in smf
    last_end = max(n[0] + n[1] for events in nt.values() for n in events)
    assert bt(56) < last_end < bt(57)
    print(f"check {s['sid']}-v2 PASS bars={bars} notes/bar={'/'.join(densities)} "
          f"bass/bar={'/'.join(bass_densities)} keys_attacks/bar={'/'.join(key_densities)} "
          f"Keys2={bar_ranges(by_bar[3])} Tex={bar_ranges(by_bar[4])} Pad={bar_ranges(by_bar[6])} "
          f"fill_bars={','.join(map(str, fills))} CC1={cc1} CC11={cc11} "
          f"same_pitch_overlaps={overlaps} drum_cell_collisions=0 "
          f"Keys2_lead_min_onset_gap={response_gap} "
          f"v1_backbone=preserved v1_motif=preserved last_end={last_end}/{bars * BAR} "
          f"last_bar={last_end / BAR + 1:.4f}")


if __name__ == '__main__':
    for sketch in SKETCHES:
        result = compose(sketch['sid'])
        nt, cc, pcs, bars, bpm, title, sf, minor = result
        smf = build_smf(title, bpm, sf, minor, bars, TRACKS, pcs, nt, cc, v1.markers(bars))
        check(sketch, result, smf)
        print(write_smf(os.path.join(SK_DIR, sketch['sid'] + '-v2.mid'), smf))
