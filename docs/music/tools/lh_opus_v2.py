"""Opus v2 calibration track: slot 15 lh15-quartz-overpass (C# minor, 88 BPM, 64 bars); Python 3.9 stdlib.

Keeps v1 (lh_opus) chord loop, key, BPM, bars, kick cells, backbeat, ghosts and lead motif, and adds the
`## v2 보정 (2026-10-30)` density layers from LOFI_HIPHOP_SET_BRIEF.md:
- Bass PC38: every kick slot (one skipped on F#9) + 3rd/5th/7th passing tones + chromatic approach on 3.5,
  octave pop every second bar; the approach note rests only at each 8-bar phrase end.
- Keys PC4: three comp attacks per bar (v1 cell + 3.5), one inner voice moving inside each long segment
  (pedal re-pressed so the motion is heard), A2 voicing raised one inversion, CC11 4-bar swell.
- Keys2 PC16 (new): motif preview bars 9-10 an octave down; A2 guide-tone eighth riff under the lead and,
  in the third and fifth A2 phrases, a 2-bar answer in the lead's rests and held notes (call-and-response).
- Tex PC27: eighth arpeggio bar 1-64 with a thumb (bottom chord tone) on every beat, 4-bar velocity arch, the
  pattern flips in break/A2.
- Pad PC89: from bar 1, 1+5+9 (G#7b13 takes 1+b7+9: its b13 replaces the fifth), CC11 4-bar swell 40-80-50.
- Drums: fill on beat 4 of every fourth bar (snare roll / tom descent alternating), hat change every
  8 bars (open-hat slot moves, two extra sixteenths), ride replaces closed hats in A2, crash on the
  first bar of A, break, A2 and outro, two-bar pickup at the end of the break.
- Lead PC0: v1 motif; from the second statement grace notes and turns; phrase velocity arch; CC1 0->40
  on each phrase end. Octave repeats are left out: the brief also forbids wide lead leaps (v1 cap 7).
"""
import os
from collections import Counter

from pipeline import BAR, PPQ, SK_DIR, bt, hum_t, hum_v, seed, build_smf, write_smf
from sketches import PC
import lh_opus as v1

TRACKS = [('Drums', 9), ('Bass', 0), ('Keys', 1), ('Keys2', 2), ('Tex', 3), ('Lead', 4), ('Pad', 5)]
DRUMS, BASS, KEYS, KEYS2, TEX, LEAD, PAD = range(7)
KICK, SNARE, HAT, OHAT, RIDE, CRASH = 36, 38, 42, 46, 51, 49
TOMS = (50, 47, 45)
SCALE = {1, 3, 4, 6, 8, 9, 11, 0}  # C# natural minor + B# leading tone

V1 = next(s for s in v1.SKETCHES if s['slot'] == 15)

SKETCHES = [dict(
    V1,
    keys2_pc=16, pad_pc=89,
    # (beat, pitch) per loop chord; approach notes on 3.5 lead into the next root.
    bass=(((0, 37), (1.5, 32), (2.75, 40), (3.5, 41)),             # C#m9: C#, G# below, E, E#->F#
          ((0, 30), (0.5, 42), (2.5, 37), (3, 40), (3.5, 44)),      # F#9: F#, octave pop, C#, E, G#->A
          ((0, 33), (1.75, 40), (2.75, 37), (3.5, 31)),            # Amaj9: A, E, C#, F##->G#
          ((0, 32), (0.5, 44), (1.5, 39), (2.5, 36), (3.5, 38))),   # G#7b13: G#, octave pop, D#, B#, D->C#
    comp=((0, 2, 3.5), (0.75, 2.5, 3.5), (0, 2, 3.5), (1.5, 2.25, 3.5)),
    # Inner voice (pitch class -> semitone move) and the beats it moves on.
    keys_move=((3, -2), (8, -2), (4, 2), (4, -1)),
    keys_move_beats=((1, 2.5), (1.5, 3), (1, 2.5), (3,)),
    pad=((49, 56, 63), (42, 49, 56), (45, 52, 59), (44, 54, 58)),
    tex_a=(3, 1, 2, 4, 1, 3, 2, 4), tex_b=(4, 2, 3, 1, 2, 4, 3, 1),
    keys2_beats=(0, 0.5, 1.5, 2.5, 3, 3.5),
    keys2_riff=((56, 59, 63, 61, 59, 56), (58, 61, 56, 52, 54, 56),
                (57, 61, 59, 56, 57, 61), (60, 63, 58, 56, 54, 60)),
    # Keys2 answer (bars 3-4 of each answer group): onsets sit in the lead's rests or under its held notes.
    answer=(((2, 56), (3, 61), (3.5, 59)),
            ((1.5, 60), (3, 58), (3.5, 56))),
    answer_groups=(45, 53),
)]


def section(bar):
    return 'intro' if bar < 9 else 'A' if bar < 29 else 'break' if bar < 37 else 'A2' if bar < 57 else 'outro'


def layers_at(s, bar):
    sec = section(bar)
    layers = {'Tex', 'Pad'}
    if sec != 'break':
        layers.add('Keys')
    if bar >= 3:
        layers.add('Hats')
    if bar >= 5:
        layers.update(('Kick', 'Snare'))
    if 9 <= bar <= s['bars'] - 4:
        layers.add('Bass')
    if 21 <= bar < 29 or sec == 'A2':
        layers.add('Lead')
    if bar in (9, 10) or sec == 'A2':
        layers.add('Keys2')
    return layers


def fill_bar(s, bar):
    return (bar - 1) % 4 == 3 and 3 <= bar < s['bars']


def swell(lo, peak, end, steps=16):
    """4-bar CC11 shape sampled per beat: rise to the peak at 10/16, settle to `end`."""
    top = 10
    return [round(lo + (peak - lo) * i / top) if i <= top else
            round(peak + (end - peak) * (i - top) / (steps - 1 - top)) for i in range(steps)]


def scale_step(pitch, direction):
    p = pitch + direction
    while p % 12 not in SCALE:
        p += direction
    return p


def compose(sid):
    s = next(s for s in SKETCHES if s['sid'] == sid)
    seed(261030 + s['slot'] * 131)
    nt, cc = {i: [] for i in range(len(TRACKS))}, {i: [] for i in range(len(TRACKS))}
    pcs = {DRUMS: 0, BASS: 38, KEYS: s['keys_pc'], KEYS2: s['keys2_pc'], TEX: s['tex_pc'],
           LEAD: s['lead_pc'], PAD: s['pad_pc']}
    swing = s['swing']

    def tick(bar, beat, swung=True):
        delay = swing if swung and beat % 1 == 0.5 else 0
        return hum_t(bt(bar, beat) + 14 + delay, 12)

    def vel(base, low, high):
        return max(low, min(high, hum_v(base, 10)))

    def add(track, bar, when, end, pitch, v):
        end = min(end, bt(bar + 1) - 24)
        assert when >= bt(bar) and end > when, (track, bar, when, end)
        nt[track].append((when, end - when, pitch, v))

    def seq(track, bar, events, cap, gap):
        """events: (tick, pitch, vel) monophonic; each ends before the next onset (gap shrinks for ornaments)."""
        events = sorted(events)
        for i, (when, pitch, v) in enumerate(events):
            nxt = events[i + 1][0] if i + 1 < len(events) else bt(bar + 1)
            add(track, bar, when, min(nxt - min(gap, (nxt - when) // 4), when + cap), pitch, v)

    lead_groups = [b for b in range(1, s['bars'] + 1) if (b - 1) % 4 == 0 and 'Lead' in layers_at(s, b)]
    a2 = v1.markers(s['bars'])[3][0]
    for bar in range(1, s['bars'] + 1):
        phase = (bar - 1) % 4
        sec = section(bar)
        chord_name, root_name, _, chord = s['chords'][s['order'][phase]]
        layers = layers_at(s, bar)
        group = bar - phase
        occupied = set()
        hat_var = ((bar - 1) // 8) % 2

        def drum(beat, pitch, v, swung=False, dur=70):
            cell = round(beat * 4)
            assert cell not in occupied, (bar, beat, pitch)
            occupied.add(cell)
            when = tick(bar, beat, swung)
            add(DRUMS, bar, when, when + dur, pitch, v)

        # --- drums: crash, kick, backbeat, ghosts, fills, then hats/ride into the free cells.
        if bar in (9, 29, 37, 57):
            drum(0.5, CRASH, vel(62, 55, 70), dur=400)
        if 'Kick' in layers:
            kick_base = vel(98 + s['energy'], 96, 104)
            for beat in s['kicks'][phase]:
                drum(beat, KICK, kick_base + (6 if beat == 0 else 0), dur=80)
        fill = fill_bar(s, bar)
        if 'Snare' in layers:
            for beat in (1, 3):
                drum(beat, SNARE, vel(94, 86, 100))
            ghosts = s['ghosts'][phase]
            if fill:
                ghosts = tuple(sorted((0.75,) + tuple(g for g in ghosts if g < 3.25)))
            for beat in ghosts:
                drum(beat, SNARE, vel(45, 38, 52))
        if fill:
            if (bar // 4) % 2 == 0:
                for beat, v in ((3.25, 60), (3.5, 68), (3.75, 76)):
                    drum(beat, SNARE, vel(v, 55, 80))
            else:
                for (beat, v), pitch in zip(((3.25, 66), (3.5, 72), (3.75, 78)), TOMS):
                    drum(beat, pitch, vel(v, 62, 82), dur=110)
        if bar == 35:  # break pickup, bar one of two
            for beat, v in ((3.25, 58), (3.5, 64)):
                drum(beat, SNARE, vel(v, 55, 80))
        if bar == 36:  # break pickup, bar two: a push into the tom fill
            drum(2.75, SNARE, vel(64, 55, 80))
        if 'Hats' in layers:
            open_at = (1, 3.5) if hat_var == 0 else (2, 2.5)
            if phase == open_at[0]:
                drum(open_at[1], OHAT, vel(76, 68, 84), swung=True, dur=145)
            ride = sec == 'A2'
            for eighth in range(8):
                beat = eighth / 2
                if round(beat * 4) in occupied:
                    continue
                off = eighth % 2 == 1
                if ride:
                    drum(beat, RIDE, vel(66 if off else 58, 62 if off else 55, 70 if off else 62), swung=off, dur=120)
                else:
                    drum(beat, HAT, vel(76 if off else 54, 68 if off else 48, 84 if off else 60), swung=off)
            # 16th hats only on the e-of-2 / e-of-4 cells (5, 13), right after the backbeat so the hat
            # never runs three 16ths: one per bar in plain 8-bar blocks, both in the alternate blocks.
            sixteenths = (1.25 if phase == 3 else 3.25,) if hat_var == 0 else (1.25, 3.25)
            for beat in sixteenths if 'Snare' in layers else ():
                if round(beat * 4) not in occupied:
                    drum(beat, HAT, vel(45, 40, 50))

        # --- bass: kick slots + passing tones; the approach on 3.5 rests at 8-bar phrase ends / last bar.
        if 'Bass' in layers:
            notes = [(b, p) for b, p in s['bass'][phase]
                     if not (b == 3.5 and (bar % 8 == 0 or bar == s['bars'] - 4))]
            events = []
            for i, (beat, pitch) in enumerate(notes):
                base = 78 if beat == 0 else 74 if (phase % 2 == 1 and beat == 0.5) else 66 if beat == 3.5 else 71
                events.append((tick(bar, beat), pitch, vel(base, 60, 82)))
            seq(BASS, bar, events, cap=2 * PPQ, gap=40)

        # --- keys: comp attacks with one moving inner voice; A2 raises the bottom voice an octave.
        if 'Keys' in layers:
            voicing = tuple(sorted(p + 12 if sec in ('A2',) and p == min(chord) else p for p in chord))
            move_pc, step = s['keys_move'][phase]
            mover = next(p for p in voicing if p % 12 == move_pc)
            beats = s['comp'][phase]
            attack_ticks = [tick(bar, b) for b in beats]
            move_ticks = [tick(bar, b) for b in s['keys_move_beats'][phase]]
            cc[KEYS].append((bt(bar), 64, 0))
            soft = sec in ('intro', 'outro')
            for i, when in enumerate(attack_ticks):
                nxt = attack_ticks[i + 1] if i + 1 < len(attack_ticks) else bt(bar + 1)
                end = min(nxt - 50, when + 4 * PPQ)
                v = vel((80 if i == 0 else 76) - (3 if soft else 0), 72, 92)
                inside = [m for m in move_ticks if when < m < nxt]
                for pitch in voicing:
                    if pitch == mover and inside:
                        add(KEYS, bar, when, inside[0] - 30, pitch, v)
                        add(KEYS, bar, inside[0], end, pitch + step, vel(74, 72, 92))
                    else:
                        add(KEYS, bar, when, end, pitch, v)
                cc[KEYS].extend(((when - 1, 64, 0), (when + 1, 64, 100)))
            for m in move_ticks:
                cc[KEYS].extend(((m - 2, 64, 0), (m + 2, 64, 100)))
            cc[KEYS].append((bt(bar + 1) - 2, 64, 0))
            for i, value in enumerate(swell(88, 112, 96)[phase * 4:phase * 4 + 4]):
                cc[KEYS].append((bt(bar, i) + 4, 11, value))

        # --- Keys2: preview (9-10), A2 riff, or the 2-bar answer in the answer groups.
        if 'Keys2' in layers:
            if bar in (9, 10):
                pitches, beats = s['melody'][phase], s['lead_beats'][phase]
                events = [(tick(bar, b), p - 12, vel(64, 55, 72)) for b, p in zip(beats, pitches)]
            elif group in s['answer_groups'] and phase >= 2:
                events = [(tick(bar, b), p, vel(68, 55, 72)) for b, p in s['answer'][phase - 2]]
            else:
                events = [(tick(bar, b), p, vel(62 if i % 2 else 66, 55, 72))
                          for i, (b, p) in enumerate(zip(s['keys2_beats'], s['keys2_riff'][phase]))]
            seq(KEYS2, bar, events, cap=400, gap=40)

        # --- Tex: continuous eighth arpeggio + thumb on every beat; 4-bar velocity arch.
        if 'Tex' in layers:
            tones = sorted(chord) + [min(chord) + 12]
            pattern = s['tex_b'] if sec in ('break', 'A2') else s['tex_a']
            arch = (58, 64, 69, 62)[phase] - (4 if sec == 'outro' and bar > s['bars'] - 4 else 0)
            for eighth, idx in enumerate(pattern):
                beat = eighth / 2
                when = tick(bar, beat)
                nxt = bt(bar, beat + 0.5) + 14 + (swing if eighth % 2 == 0 else 0) - 12
                end = min(nxt - 40, when + 300)
                add(TEX, bar, when, end, tones[idx], vel(arch + (3 if eighth in (0, 4) else 0), 55, 72))
                if eighth % 2 == 0 and idx != 0:
                    add(TEX, bar, when, end, tones[0], vel(arch - 2, 55, 72))

        # --- Pad: 1+5+9 held per bar, CC11 4-bar swell 40 -> 80 -> 50.
        if 'Pad' in layers:
            when = tick(bar, 0)
            for pitch in s['pad'][phase]:
                add(PAD, bar, when, bt(bar + 1), pitch, vel(52, 45, 60))
            for i, value in enumerate(swell(40, 80, 50)[phase * 4:phase * 4 + 4]):
                cc[PAD].append((bt(bar, i) + 4, 11, value))

        # --- Lead: v1 motif (v1 A2 variant kept), ornaments from statement two.
        if 'Lead' in layers:
            k = lead_groups.index(group)
            variant = bar >= a2 and ((bar - a2) // 4) % 2 == 1
            pitches, beats = v1.lead_phrase(s, phase, variant)
            arch = (68, 73, 77, 70)[phase] + (2 if sec == 'A2' else 0)
            notes = [(b, p, arch + (2 if 0 < i < len(pitches) - 1 else 0)) for i, (b, p) in enumerate(zip(beats, pitches))]
            graces = []
            if k >= 1:
                if phase == 0 or (phase == 2 and k % 2 == 0):
                    graces.append((notes[0][0], scale_step(notes[0][1], -1)))
                elif phase == 1 and k % 2 == 1:
                    notes = notes[:1] + [(1.5, 71, arch - 4), (1.75, 70, arch - 4)] + notes[1:]
                elif phase == 2:
                    notes = notes[:2] + [(1.0, 71, arch - 3), (1.25, 69, arch - 4)] + notes[2:]
                else:
                    graces.append((notes[0][0], scale_step(notes[0][1], 1)))
            events = []
            grace_at = {b: p for b, p in graces}
            for b, p, base in notes:
                when = tick(bar, b, swung=b % 0.5 == 0)
                if b in grace_at:
                    events.append((when, grace_at[b], vel(base - 10, 60, 82)))
                    when += 60
                events.append((when, p, vel(base, 60, 82)))
            seq(LEAD, bar, events, cap=440, gap=48)
            if phase == 0:
                cc[LEAD].append((bt(bar), 1, 0))
            if phase == 3:
                # Ramp ends on beat 3.75 so the next phrase's reset at its downbeat never shares a tick.
                for i, value in enumerate((0, 8, 16, 24, 32, 40)):
                    cc[LEAD].append((bt(bar, 2 + 0.35 * i), 1, value))
    cc[LEAD].append((bt(57), 1, 0))
    for events in nt.values():
        events.sort()
    for events in cc.values():
        events.sort()
    return nt, cc, pcs, s['bars'], s['bpm'], s['title'], s['sf'], s['minor']


def bar_ranges(bars):
    bars, out = sorted(set(bars)), []
    for b in bars:
        if out and b == out[-1][1] + 1:
            out[-1][1] = b
        else:
            out.append([b, b])
    return ','.join(f'{a}-{b}' if a != b else f'{a}' for a, b in out)


def check(s, result, smf):
    nt, cc, pcs, n_bars, bpm, title, sf, minor = result
    assert (n_bars, bpm, sf, minor) == (64, 88, 4, True)
    assert pcs == {0: 0, 1: 38, 2: 4, 3: 16, 4: 27, 5: 0, 6: 89}
    bar_of = lambda n: n[0] // BAR + 1
    per_bar = Counter(bar_of(n) for notes in nt.values() for n in notes)
    density, floor = {}, {}
    for sec in ('intro', 'A', 'break', 'A2', 'outro'):
        bars = [b for b in range(1, n_bars + 1) if section(b) == sec]
        density[sec] = sum(per_bar[b] for b in bars) / len(bars)
        floor[sec] = min(per_bar[b] for b in bars)
    assert floor['A'] >= 45 and floor['A2'] >= 45 and density['intro'] >= 25 and density['break'] >= 25
    bass_bar = Counter(bar_of(n) for n in nt[BASS])
    bass_avg = {sec: sum(bass_bar[b] for b in range(1, n_bars + 1) if section(b) == sec) /
                sum(1 for b in range(1, n_bars + 1) if section(b) == sec) for sec in ('A', 'A2')}
    assert min(bass_avg.values()) >= 4
    assert all(28 <= n[2] <= 48 and 60 <= n[3] <= 82 for n in nt[BASS])
    onsets = Counter((bar_of(n), n[0]) for n in nt[KEYS])
    attacks = Counter(b for (b, _), c in onsets.items() if c >= 3)
    keys_bars = sorted({bar_of(n) for n in nt[KEYS]})
    assert min(attacks[b] for b in keys_bars) >= 3
    moves = sum(1 for c in onsets.values() if c == 1)
    assert all(48 <= n[2] <= 72 and 72 <= n[3] <= 92 for n in nt[KEYS])
    keys2_bars = {bar_of(n) for n in nt[KEYS2]}
    assert keys2_bars == {9, 10} | set(range(37, 57))
    assert max(n[2] for n in nt[KEYS2]) < min(n[2] for n in nt[LEAD])
    tex_bars = {bar_of(n) for n in nt[TEX]}
    pad_bars = {bar_of(n) for n in nt[PAD]}
    assert tex_bars == pad_bars == set(range(1, n_bars + 1))
    assert all(Counter(n[0] for n in nt[TEX] if bar_of(n) == b).__len__() == 8 for b in tex_bars)
    assert all(55 <= n[3] <= 72 for n in nt[TEX]) and all(45 <= n[3] <= 60 for n in nt[PAD])
    lead_bars = Counter(bar_of(n) for n in nt[LEAD])
    assert set(lead_bars) == set(range(21, 29)) | set(range(37, 57)) and max(lead_bars.values()) <= 6
    leap = max(abs(a[2] - b[2]) for a, b in zip(nt[LEAD], nt[LEAD][1:]))
    # Every lead bar carries the v1 motif notes in order (ornaments only add notes around them).
    a2 = v1.markers(n_bars)[3][0]
    for b in lead_bars:
        variant = b >= a2 and ((b - a2) // 4) % 2 == 1
        motif = list(v1.lead_phrase(s, (b - 1) % 4, variant)[0])
        played = iter(n[2] for n in nt[LEAD] if bar_of(n) == b)
        assert all(p in played for p in motif), b
    # Call-and-response: Keys2 answer onsets keep >= 120 ticks from any lead onset.
    answer_bars = sorted(g + o for g in s['answer_groups'] for o in (2, 3))
    lead_on = [n[0] for n in nt[LEAD]]
    answer_gap = min(abs(n[0] - t) for n in nt[KEYS2] if bar_of(n) in answer_bars for t in lead_on)
    assert answer_gap >= 120
    assert leap <= 7 and all(60 <= n[3] <= 82 for n in nt[LEAD])
    drums = nt[DRUMS]
    cells = Counter((bar_of(n), round(((n[0] % BAR) - 14) / (PPQ / 4))) for n in drums)
    assert max(cells.values()) == 1
    # Hat family (closed/open/ride) on adjacent 16th cells: longest run per bar must stay <= 2.
    hat_cells = {}
    for n in drums:
        if n[2] in (HAT, OHAT, RIDE):
            hat_cells.setdefault(bar_of(n), set()).add(round(((n[0] % BAR) - 14) / (PPQ / 4)))
    hat_run = 0
    for cells_here in hat_cells.values():
        run = 0
        for c in range(16):
            run = run + 1 if c in cells_here else 0
            hat_run = max(hat_run, run)
    assert hat_run <= 2
    hat16 = {c for cs in hat_cells.values() for c in cs if c % 2 == 1}
    assert hat16 <= {5, 13}
    fills = sorted({bar_of(n) for n in drums if n[2] in TOMS or (n[2] == SNARE and 55 <= n[3] <= 80)})
    assert set(range(4, n_bars, 4)) <= set(fills)
    ghost_bars = Counter(bar_of(n) for n in drums if n[2] == SNARE and n[3] <= 52)
    assert all(ghost_bars[b] == 2 for b in range(5, n_bars + 1))
    crashes = sorted(bar_of(n) for n in drums if n[2] == CRASH)
    assert crashes == [9, 29, 37, 57] and all(55 <= n[3] <= 70 for n in drums if n[2] == CRASH)
    rides = {bar_of(n) for n in drums if n[2] == RIDE}
    assert rides == set(range(37, 57))
    opened = Counter((bar_of(n) - 1) // 4 for n in drums if n[2] == OHAT)
    assert max(opened.values()) == 1
    cc1 = [c for c in cc[LEAD] if c[1] == 1]
    cc11 = [c for t in (KEYS, PAD) for c in cc[t] if c[1] == 11]
    cc1_same_tick = sum(c - 1 for c in Counter(t for t, _, _ in cc1).values())
    assert cc1 and max(v for _, _, v in cc1) == 40 and cc11 and cc1_same_tick == 0
    overlaps = 0
    for events in nt.values():
        ends = {}
        for when, duration, pitch, _ in events:
            overlaps += int(when < ends.get(pitch, -1))
            ends[pitch] = when + duration
    assert overlaps == 0
    for _, text in v1.markers(n_bars):
        assert bytes([0xff, 6, len(text)]) + text.encode() in smf
    last_end = max(n[0] + n[1] for notes in nt.values() for n in notes)
    assert bt(n_bars) < last_end < bt(n_bars + 1)
    dens = ' '.join(f'{k}={v:.1f}(min {floor[k]})' for k, v in density.items())
    print(f"check {s['sid']}-v2 PASS notes/bar {dens} "
          f"bass/bar A={bass_avg['A']:.2f} A2={bass_avg['A2']:.2f} "
          f"keys_attacks/bar min={min(attacks[b] for b in keys_bars)} "
          f"avg={sum(attacks[b] for b in keys_bars) / len(keys_bars):.2f} inner_moves={moves} "
          f"keys_bars={bar_ranges(keys_bars)} keys2_bars={bar_ranges(keys2_bars)} "
          f"tex_bars={bar_ranges(tex_bars)} pad_bars={bar_ranges(pad_bars)} "
          f"lead_bars={bar_ranges(lead_bars)}/max={max(lead_bars.values())}/leap<={leap}/v1_motif=all "
          f"answer_bars={','.join(map(str, answer_bars))}/gap>={answer_gap} "
          f"fill_bars={bar_ranges(fills)} ride_bars={bar_ranges(rides)} crash={crashes} "
          f"CC1={len(cc1)} CC1_same_tick=0 CC11={len(cc11)} hat_16th_run<={hat_run} "
          f"same_pitch_overlaps={overlaps} drum_cell_collisions=0 "
          f"last_end={last_end}/{n_bars * BAR}")


if __name__ == '__main__':
    for sketch in SKETCHES:
        result = compose(sketch['sid'])
        nt, cc, pcs, n_bars, bpm, title, sf, minor = result
        smf = build_smf(title, bpm, sf, minor, n_bars, TRACKS, pcs, nt, cc, v1.markers(n_bars))
        check(sketch, result, smf)
        print(write_smf(os.path.join(SK_DIR, sketch['sid'] + '-v2.mid'), smf))
