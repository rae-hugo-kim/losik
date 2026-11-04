"""Slot 2 density calibration (model sonnet); Python 3.9 stdlib.

Keeps lh_fable's chord loop (Dm9-Am7-Bbmaj7-Gm9), key, BPM 76, 56 bars, kick cells, backbeat, break design
(nylon, then keys) and lead motif for lh02-linen-afternoon and layers the v2 rows of
LOFI_HIPHOP_SET_BRIEF.md (calibration 2026-10-30 plus the two 2026-11-04 rows):
- Bass PC33: root on the grid at every bar's beat one, chord tones and passing notes on eighths, chromatic
  approach into the next root on 3.5, octave pop every second bar; at most one sixteenth-position note per bar
  (the bar-three kick anticipation), never two anticipations in a row. CC7=85 at tick 0 (level row).
- Keys PC4: three comping attacks plus the inner-voice return per bar, every bar attacks beat one on the grid,
  at most one e/a attack per bar; an inner voice steps down on the last attack and returns on 3.5;
  A2 re-voices the same chord tones (one inversion / spread).
- Keys2 PC0 (new): motif preview on bars 9-10 an octave down, then in A2 a chord-tone riff under the lead on
  loop bars one/two and a two-bar answer echoing the motif on bars three/four.
- Tex PC24: nylon eighth arpeggio with a thumb on every beat and four sixteenth pluck-backs from bar 1 to 56
  (break included), 4-bar velocity arch.
- Pad PC89: 1+5+9 from bar 1, CC11 swell 40-80-50 per four bars.
- Drums: fill on beat four of every fourth bar, hat variation per eight bars (open-hat slot moves, 16th hats),
  two ghosts a bar, ride replaces closed hats in A2, crash on section starts, two-bar pickup at the break's end.
  Energy-1 outro keeps v1's drum drop on the last four bars.
- Break: v1 keeps only the nylon (then keys at offset 4); v2 adds the pad. Two layers or more, Tex throughout.
- Lead PC4: v1 motif, grace notes and a turn from the second statement, phrase velocity arch, CC1 ramp 0->40.
Every note velocity is clamped to the brief's table (VEL). The scale is D natural minor for ornaments.
"""
import os
from collections import Counter

from pipeline import BAR, PPQ, SK_DIR, bt, hum_t, hum_v, seed, build_smf, write_smf
from sketches import PC
import lh_fable as v1

TRACKS = [('Drums', 9), ('Bass', 0), ('Keys', 1), ('Keys2', 2), ('Tex', 3), ('Lead', 4), ('Pad', 5)]
DRUMS, BASS, KEYS, KEYS2, TEX, LEAD, PAD = range(7)
KICK, SNARE, HAT, OHAT, CRASH, RIDE = 36, 38, 42, 46, 49, 51
TOMS = (48, 47, 45)
SKETCHES = [s for s in v1.SKETCHES if s['slot'] == 2]
NATURAL_MINOR = (0, 2, 3, 5, 7, 8, 10)
# Velocity ranges from the brief's recipe table (v1) plus the v2 rows; fills sit between ghost and backbeat.
VEL = dict(kick=(96, 110), snare=(86, 100), ghost=(38, 52), hat_on=(48, 60), hat_off=(68, 84),
           hat16=(40, 50), ohat=(68, 84), ride=(55, 70), crash=(55, 70), fill=(56, 84),
           bass=(60, 82), keys=(72, 92), keys2=(55, 72), tex=(55, 72), lead=(60, 82), pad=(45, 60))
# Keys comping attacks per loop bar; beat one is always on the grid, only phase three carries one e/a attack.
COMP_A = ((0, 1.5, 2.5), (0, 1, 2.5), (0, 1.75, 2.5), (0, 1.5, 3))
COMP_A2 = ((0, 1, 2.5), (0, 1.5, 3), (0, 1.5, 2.5), (0, 2, 3))
# A2 re-voicing: the same chord tones rearranged (Dm9 -> Fmaj7 shape, Am7 / Bbmaj7 root position, Gm9 spread).
A2_VOICING = {'Dm9': (53, 57, 60, 64), 'Am7': (57, 60, 64, 67),
              'Bbmaj7': (58, 62, 65, 69), 'Gm9': (50, 57, 65, 70)}
# (loop phase, eighth) per eight-bar block; kick and snare cells are avoided so the open hat always lands.
OPEN_HAT = ((1, 7), (2, 7), (2, 5), (0, 3))
# Bass lines: (beat, semitones above the bar's root; None = chromatic approach into the next root).
# Beat 0 is always the root, 12 is the octave pop (loop bars two and four), only A's bar three has a 16th (1.75).
BASS_A = (((0, 0), (1, 3), (1.5, 5), (2.5, 7), (3.5, None)),
          ((0, 0), (1.5, 3), (2.5, 12), (3, 10), (3.5, None)),
          ((0, 0), (1, 4), (1.75, 7), (2.5, 11), (3.5, None)),
          ((0, 0), (1, 3), (2.5, 7), (3, 12), (3.5, None)))
BASS_A2 = (((0, 0), (1.5, 3), (2.5, 7), (3, 5), (3.5, None)),
           ((0, 0), (1, 7), (2.5, 12), (3, 10), (3.5, None)),
           ((0, 0), (1, 7), (1.75, 11), (2.5, 7), (3.5, None)),
           ((0, 0), (1.5, 7), (2.5, 3), (3, 12), (3.5, None)))
APPROACH = (1, 1, -1, -1)   # semitones from the next root: above, above, below, below
# Keys2 in A2: (beat, voice index into the chord's low voicing) riff on loop bars one and two,
# (beat, pitch) answer on bars three and four (the motif's bars one and two an octave down).
KEYS2_RIFF = (((0, 1), (0.5, 2), (2.5, 3), (3.5, 2)), ((0, 2), (1.5, 1), (2, 3), (3.5, 2)))
KEYS2_ANSWER = (((0, 57), (0.5, 53), (1.5, 50)), ((1, 52), (3, 55), (3.5, 52)))
MIN_GAP = 120   # ticks between any Keys2 onset and any lead onset in the same bar


def scale_of(s):
    return {(PC[s['tonic']] + degree) % 12 for degree in NATURAL_MINOR}


def step(pitch, direction, scale):
    pitch += direction
    while pitch % 12 not in scale:
        pitch += direction
    return pitch


def fold(pitch, low, high):
    while pitch > high:
        pitch -= 12
    while pitch < low:
        pitch += 12
    return pitch


def swell(x, low, peak, end):
    """Four-bar expression arch sampled at bar position x in [0, 4)."""
    return round(low + (peak - low) * x / 3) if x <= 3 else round(peak + (end - peak) * (x - 3))


def layers_at(s, bar):
    _, (a, _), (brk, _), (a2, _), (outro, _) = v1.markers(s['bars'])
    if brk <= bar < a2:
        # v1 drops everything but the nylon (keys join at offset four); v2 adds the pad.
        return {'Tex', 'Pad'} | v1.break_layers(s['slot'], bar - brk)
    layers = {'Keys', 'Tex', 'Pad'}
    if bar >= 3:
        layers.add('Hats')
    if bar >= 5:
        layers.update(('Kick', 'Snare'))
    if a <= bar <= s['bars'] - 4:
        layers.add('Bass')
    if brk - 8 <= bar < brk or a2 <= bar < outro:
        layers.add('Lead')
    if a <= bar < a + 2 or a2 <= bar < outro:
        layers.add('Keys2')
    if s['energy'] == 1 and bar > s['bars'] - 4:
        layers.difference_update(('Kick', 'Snare', 'Hats'))
    return layers


def fill_hits(s, bar, layers):
    """(beat, pitch, base velocity) for bar four of each phrase and the two break pickup bars."""
    _, _, (brk, _), (a2, _), _ = v1.markers(s['bars'])
    if bar == brk + 6:
        return ((3.5, SNARE, 60), (3.75, SNARE, 66))
    if bar == brk + 7:
        return ((2.5, TOMS[0], 72), (3, TOMS[1], 74), (3.5, TOMS[2], 76), (3.75, SNARE, 82))
    if bar % 4 or bar == s['bars'] or 'Kick' not in layers or brk <= bar < a2:
        return ()
    if (bar // 4) % 2:
        return ((3.5, SNARE, 70), (3.75, SNARE, 78))
    return tuple(zip((3.25, 3.5, 3.75), TOMS, (76, 74, 78)))


def bass_root(root):
    """Root in E1..C3 (28-40) so the octave pop stays inside the bass range (D2 pops to D3)."""
    return fold(24 + PC[root], 28, 40)


def bass_line(phase, root, next_root, in_a2):
    """(beat, pitch, base velocity) from the BASS tables; the approach note leans on the next root."""
    low = bass_root(root)
    notes = []
    for beat, offset in (BASS_A2 if in_a2 else BASS_A)[phase]:
        if offset is None:
            notes.append((beat, bass_root(next_root) + APPROACH[phase], 66))
        else:
            notes.append((beat, low + offset, 78 if beat == 0 else 72 if offset == 12 else 70))
    return notes


def moving_voice(voicing, scale):
    """Index of the voice that steps down on the last attack without landing next to a neighbour."""
    for index in (2, 3, 1):
        moved = step(voicing[index], -1, scale)
        if all(abs(moved - p) > 1 for i, p in enumerate(voicing) if i != index):
            return index, moved
    raise AssertionError(voicing)


def thumb_root(root):
    pitch = 48 + PC[root]
    return pitch - 12 if pitch > 55 else pitch


def compose(sid):
    s = next(s for s in SKETCHES if s['sid'] == sid)
    seed(261104 + s['slot'] * 97)
    nt, cc = {i: [] for i in range(7)}, {i: [] for i in range(7)}
    cc[BASS].append((0, 7, 85))   # 베이스 레벨 (브리프 2026-11-04)
    pcs = {DRUMS: 0, BASS: 38 if s['energy'] == 3 else 33, KEYS: s['keys_pc'],
           KEYS2: 0 if s['keys_pc'] != 0 else 4, TEX: s['tex_pc'], LEAD: s['lead_pc'], PAD: 89}
    _, (a, _), (brk, _), (a2, _), (outro, _) = v1.markers(s['bars'])
    scale = scale_of(s)
    swing = s['swing']

    def tick(bar, beat, swung=False):
        delay = swing if swung and beat % 1 == 0.5 else 0
        return hum_t(bt(bar, beat) + 14 + delay, 12)

    def velocity(base, kind):
        low, high = VEL[kind]
        return max(low, min(high, hum_v(base, 10)))

    def add(track, bar, when, duration, pitch, vel):
        end = min(when + duration, bt(bar + 1) - 24)
        assert bt(bar) <= when < end
        nt[track].append((when, end - when, pitch, vel))

    for bar in range(1, s['bars'] + 1):
        phase = (bar - 1) % 4
        name, root, quality, chord = s['chords'][s['order'][phase]]
        next_root = s['chords'][s['order'][(phase + 1) % 4]][1]
        layers = layers_at(s, bar)
        in_a2 = a2 <= bar < outro
        occupied = set()

        def drum(beat, pitch, vel, swung=False, duration=70, required=True):
            """Every drum event passes through here: one element per sixteenth cell."""
            cell = round(beat * 4)
            if cell in occupied:
                assert not required, (bar, beat, pitch)
                return
            occupied.add(cell)
            add(DRUMS, bar, tick(bar, beat, swung), duration, pitch, vel)

        if 'Kick' in layers:
            kick_base = min(VEL['kick'][1] - 6, velocity(100 + (s['energy'] - 1), 'kick'))
            for beat in s['kicks'][phase]:
                drum(beat, KICK, kick_base + (6 if beat == 0 else 0), duration=90)
        if bar in (a, brk, a2, outro):
            drum(0.25, CRASH, velocity(62, 'crash'), duration=400)
        fill = fill_hits(s, bar, layers)
        if 'Snare' in layers:
            for beat in (1, 3):
                drum(beat, SNARE, velocity(92 + s['energy'], 'snare'))
            # Two ghosts a bar: the v1 ghost on 3.75 plus one that alternates; fill bars move them off the fill.
            for beat in (0.75, 2.25) if fill else ((0.75, 3.75) if phase % 2 == 0 else (2.25, 3.75)):
                drum(beat, SNARE, velocity(45, 'ghost'))
        for beat, pitch, base in fill:
            drum(beat, pitch, velocity(base, 'fill'))
        if 'Hats' in layers:
            block = (bar - 1) // 8
            open_phase, open_eighth = OPEN_HAT[block % 4]
            # A2 replaces every closed hat with the ride; open hat and sixteenths stay.
            closed, closed_kind = (RIDE, 'ride') if in_a2 else (HAT, 'hat')
            for eighth in range(8):
                offbeat = eighth % 2 == 1
                is_open = phase == open_phase and eighth == open_eighth
                if is_open:
                    vel = velocity(76, 'ohat')
                elif closed == RIDE:
                    vel = velocity(66 if offbeat else 58, 'ride')
                else:
                    vel = velocity(76 if offbeat else 54, 'hat_off' if offbeat else 'hat_on')
                drum(eighth / 2, OHAT if is_open else closed, vel, swung=offbeat,
                     duration=145 if is_open else 120 if closed == RIDE else 70, required=False)
            # Sixteenth hats need the backbeat beside them; without a snare they would run three cells.
            if 'Snare' in layers:
                extra = (1.25, 3.25) if block % 2 else ((1.25,) if phase % 2 == 0 else (3.25,))
                for beat in extra:
                    drum(beat, HAT, velocity(45, 'hat16'), required=False)
        if 'Bass' in layers:
            line = bass_line(phase, root, next_root, in_a2)
            for index, (beat, pitch, base) in enumerate(line):
                next_beat = line[index + 1][0] if index + 1 < len(line) else 4
                add(BASS, bar, tick(bar, beat), min(460, int((next_beat - beat) * PPQ) - 40),
                    pitch, velocity(base, 'bass'))
        if 'Keys' in layers:
            voicing = A2_VOICING[name] if in_a2 else chord
            mover, moved = moving_voice(voicing, scale)
            beats = (COMP_A2 if in_a2 else COMP_A)[phase]
            for index, beat in enumerate(beats):
                when = tick(bar, beat)
                next_beat = beats[index + 1] if index + 1 < len(beats) else 3.5
                vel = velocity(82 if index == 0 else 76, 'keys')
                last = index == len(beats) - 1
                for voice, pitch in enumerate(voicing):
                    add(KEYS, bar, when, int((next_beat - beat) * PPQ) - 60,
                        moved if last and voice == mover else pitch, vel)
                cc[KEYS].extend(((when - 1, 64, 0), (when + 1, 64, 100)))
            # The moved voice returns on the last eighth: audible inner-voice motion.
            add(KEYS, bar, tick(bar, 3.5), 180, voicing[mover], velocity(74, 'keys'))
            cc[KEYS].extend(((bt(bar), 64, 0), (bt(bar + 1) - 2, 64, 0)))
            for quarter in range(4):
                cc[KEYS].append((bt(bar, quarter), 11, swell(phase + quarter / 4, 76, 100, 84)))
        if 'Keys2' in layers:
            if bar < a2:
                # Intro preview: the motif's first two bars an octave down.
                notes = [(beat, pitch - 12) for beat, pitch in zip(s['lead_beats'][phase], s['melody'][phase])]
            elif phase < 2:
                low = sorted(fold(p, 50, 62) for p in chord)
                notes = [(beat, low[voice]) for beat, voice in KEYS2_RIFF[phase]]
            else:
                notes = list(KEYS2_ANSWER[phase - 2])
            for index, (beat, pitch) in enumerate(notes):
                next_beat = notes[index + 1][0] if index + 1 < len(notes) else 4
                add(KEYS2, bar, tick(bar, beat, swung=True), min(400, int((next_beat - beat) * PPQ) - 48),
                    pitch, velocity(64, 'keys2'))
        if 'Tex' in layers:
            order = [s['tex_order'][(i + phase) % 4] for i in range(4)]
            pattern = order + [order[2], order[1], order[3], order[0]]
            base = (59, 63, 68, 61)[phase]
            for beat in range(4):   # thumb bass under the arpeggio
                add(TEX, bar, tick(bar, beat), 400, thumb_root(root), velocity(base - 3, 'tex'))
            for eighth in range(8):
                add(TEX, bar, tick(bar, eighth / 2, swung=True), 190, chord[pattern[eighth]], velocity(base, 'tex'))
            # Four sixteenth pluck-backs a bar (before beats two and four), pitches never repeat a sounding note.
            for beat, voice in zip((1.25, 1.75, 3.25, 3.75), (order[1], order[2], order[1], order[2])):
                add(TEX, bar, tick(bar, beat), 90, chord[voice], velocity(base - 5, 'tex'))
            if brk <= bar < a2 and 'Keys' not in layers:
                # Nylon alone in the break: the other four e/a cells fill in, so the arpeggio rolls in sixteenths.
                for beat, voice in zip((0.25, 0.75, 2.25, 2.75), (order[2], order[3], order[3], order[0])):
                    add(TEX, bar, tick(bar, beat), 90, chord[voice], velocity(base - 5, 'tex'))
        if 'Lead' in layers:
            first = brk - 8 if bar < brk else a2
            occurrence = (bar - first) // 4 + (2 if bar >= a2 else 0)
            variant = bar >= a2 and ((bar - a2) // 4) % 2 == 1
            pitches, beats = v1.lead_phrase(s, phase, variant)
            base = (66, 70, 76, 70)[phase] + s['energy']
            # Ornaments from the second statement: a grace before note two (phases 0, 1, 3),
            # a turn on the long note of phase 2 from the third statement; never above six notes a bar.
            grace_at = 1 if occurrence >= 1 and phase != 2 and len(beats) > 1 else None
            turn_at = 1 if occurrence >= 2 and phase == 2 else None
            if phase == 0:
                cc[LEAD].append((bt(bar), 1, 0))
            for index, (beat, pitch) in enumerate(zip(beats, pitches)):
                next_beat = beats[index + 1] if index + 1 < len(beats) else 4
                when = tick(bar, beat, swung=True)
                vel = velocity(base, 'lead')
                tail = int((next_beat - beat) * PPQ) - 48 - (90 if index + 1 == grace_at else 0)
                if index == grace_at:
                    add(LEAD, bar, when - 70, 55, step(pitch, -1, scale), velocity(base - 10, 'lead'))
                if index == turn_at:
                    add(LEAD, bar, when, 200, pitch, vel)
                    add(LEAD, bar, tick(bar, beat + 0.5, swung=True), 80, step(pitch, 1, scale), velocity(base - 6, 'lead'))
                    add(LEAD, bar, tick(bar, beat + 0.75), 80, step(pitch, -1, scale), velocity(base - 8, 'lead'))
                    add(LEAD, bar, tick(bar, beat + 1), min(440, tail - PPQ), pitch, velocity(base - 2, 'lead'))
                else:
                    add(LEAD, bar, when, min(440, tail), pitch, vel)
            if phase == 3:
                cc[LEAD].extend((bt(bar, eighth / 2), 1, 5 * (eighth + 1)) for eighth in range(8))
                cc[LEAD].append((bt(bar + 1) - 1, 1, 0))
        if 'Pad' in layers:
            low = thumb_root(root)
            when = tick(bar, 0)
            top = low + (15 if name.endswith('m7') else 14)   # 1+5+9; a plain m7 takes the third an octave up
            alone = brk <= bar < a2 and 'Keys' not in layers
            for pitch in (low, low + 7):
                add(PAD, bar, when, BAR, pitch, velocity(52, 'pad'))
            if alone:
                # Nylon-only break bars: the top voice steps up a scale degree and back each beat (inner motion).
                for beat in range(4):
                    add(PAD, bar, tick(bar, beat), PPQ - 30, step(top, 1, scale) if beat % 2 else top,
                        velocity(52, 'pad'))
            else:
                add(PAD, bar, when, BAR, top, velocity(52, 'pad'))
            for eighth in range(8):
                cc[PAD].append((bt(bar, eighth / 2), 11, swell(phase + eighth / 8, 40, 80, 50)))
    for events in nt.values():
        events.sort()
    for events in cc.values():
        events.sort()
    return nt, cc, pcs, s['bars'], s['bpm'], s['title'], s['sf'], s['minor']


def bar_of(note):
    return note[0] // BAR + 1


def ranges(bars):
    groups = []
    for bar in sorted(bars):
        if groups and groups[-1][1] == bar - 1:
            groups[-1][1] = bar
        else:
            groups.append([bar, bar])
    return ','.join(str(lo) if lo == hi else f'{lo}-{hi}' for lo, hi in groups) or '-'


def check(s, result, smf):
    nt, cc, pcs, n_bars, bpm, title, sf, minor = result
    assert (n_bars, bpm, title, sf, minor) == (s['bars'], s['bpm'], s['title'], s['sf'], s['minor'])
    assert pcs == {DRUMS: 0, BASS: 33, KEYS: 4, KEYS2: 0, TEX: 24, LEAD: 4, PAD: 89}
    _, (a, _), (brk, _), (a2, _), (outro, _) = v1.markers(n_bars)
    sections = (('intro', 1, a - 1), ('A', a, brk - 1), ('break', brk, a2 - 1), ('A2', a2, outro - 1),
                ('outro', outro, n_bars))
    per_bar = Counter(bar_of(n) for notes in nt.values() for n in notes)
    density = {name: sum(per_bar[b] for b in range(lo, hi + 1)) / (hi - lo + 1) for name, lo, hi in sections}
    # Per-bar floors: A/A2 >= 45; intro, break and outro every bar >= 25.
    floor = {name: min(per_bar[b] for b in range(lo, hi + 1)) for name, lo, hi in sections}
    floor['A/A2'] = min(per_bar[b] for b in list(range(a, brk)) + list(range(a2, outro)))
    assert floor['A/A2'] >= 45 and min(floor[k] for k in ('intro', 'break', 'outro')) >= 25, floor
    # Break keeps two layers or more, Tex throughout.
    for bar in range(brk, a2):
        assert 'Tex' in layers_at(s, bar) and len(layers_at(s, bar)) >= 2
    bass_rate = {name: len([n for n in nt[BASS] if lo <= bar_of(n) <= hi]) / (hi - lo + 1)
                 for name, lo, hi in sections if name in ('A', 'A2')}
    assert min(bass_rate.values()) >= 4
    attacks = {}
    for n in nt[KEYS]:
        attacks.setdefault((bar_of(n), n[0]), n)
    keys_rate = {name: len([k for k in attacks if lo <= k[0] <= hi]) / (hi - lo + 1)
                 for name, lo, hi in sections if name in ('A', 'A2')}
    assert min(keys_rate.values()) >= 3
    keys2_bars = {bar_of(n) for n in nt[KEYS2]}
    assert keys2_bars == {a, a + 1} | set(range(a2, outro))
    tex_bars = Counter(bar_of(n) for n in nt[TEX])
    pad_bars = Counter(bar_of(n) for n in nt[PAD])
    assert set(tex_bars) == set(pad_bars) == set(range(1, n_bars + 1))
    nylon_bars = [b for b in range(brk, a2) if 'Keys' not in layers_at(s, b)]
    assert min(tex_bars.values()) >= 12 and set(pad_bars[b] for b in pad_bars if b not in nylon_bars) == {3}
    assert all(pad_bars[b] == 6 for b in nylon_bars)   # top voice steps up and back each beat
    # Velocity table: every drum element and every pitched track inside the brief's range.
    drums = nt[DRUMS]
    kick = [n for n in drums if n[2] == KICK]
    back = [n for n in drums if n[2] == SNARE and n[3] >= 86]
    ghost = [n for n in drums if n[2] == SNARE and n[3] <= 52]
    fills = [n for n in drums if n[2] in TOMS or (n[2] == SNARE and 52 < n[3] < 86)]
    hat_on = [n for n in drums if n[2] == HAT and v1.event_cell(n) % 4 == 0]
    hat_off = [n for n in drums if n[2] == HAT and v1.event_cell(n) % 4 == 2]
    hat16 = [n for n in drums if n[2] == HAT and v1.event_cell(n) % 2 == 1]
    ride = [n for n in drums if n[2] == RIDE]
    groups = dict(kick=kick, snare=back, ghost=ghost, fill=fills, hat_on=hat_on, hat_off=hat_off, hat16=hat16,
                  ohat=[n for n in drums if n[2] == OHAT], ride=ride, crash=[n for n in drums if n[2] == CRASH],
                  bass=nt[BASS], keys=nt[KEYS], keys2=nt[KEYS2], tex=nt[TEX], lead=nt[LEAD], pad=nt[PAD])
    assert len(drums) == sum(len(groups[k]) for k in ('kick', 'snare', 'ghost', 'fill', 'hat_on', 'hat_off',
                                                       'hat16', 'ohat', 'ride', 'crash'))
    vel_span = {}
    for kind, notes in groups.items():
        assert notes, kind
        lo, hi = VEL[kind]
        assert all(lo <= n[3] <= hi for n in notes), kind
        vel_span[kind] = f'{min(n[3] for n in notes)}..{max(n[3] for n in notes)}'
    collisions = Counter((bar_of(n), v1.event_cell(n)) for n in drums)
    assert max(collisions.values()) == 1
    fill_bars = sorted({bar_of(n) for n in fills})
    assert fill_bars == sorted([b for b in range(8, n_bars, 4) if not brk <= b < a2] + [brk + 6, brk + 7])
    # Two ghosts in every bar that has a snare backbeat.
    for bar in range(1, n_bars + 1):
        if 'Snare' in layers_at(s, bar):
            assert len([n for n in ghost if bar_of(n) == bar]) == 2, bar
    cc1_events = [c for c in cc[LEAD] if c[1] == 1]
    cc1 = len(cc1_events)
    cc11 = len([c for track in (KEYS, PAD) for c in cc[track] if c[1] == 11])
    assert cc1 and cc11
    assert len({c[0] for c in cc1_events}) == cc1   # ramp never shares a tick with its reset
    # Bass level row: CC7=85 at tick 0 on the bass track only.
    assert [(t, c, v) for track in cc for t, c, v in cc[track] if c == 7] == [(0, 7, 85)] and cc[BASS][0] == (0, 7, 85)
    overlaps = 0
    for notes in nt.values():
        ends = {}
        for when, duration, pitch, _ in notes:
            overlaps += int(when < ends.get(pitch, -1))
            ends[pitch] = when + duration
    assert overlaps == 0
    for bar in range(1, n_bars + 1):
        layers = layers_at(s, bar)
        if 'Kick' in layers:
            kicks = [n for n in kick if bar_of(n) == bar]
            assert tuple(v1.event_cell(n) / 4 for n in kicks) == s['kicks'][(bar - 1) % 4]
            assert all(kicks[0][3] == n[3] + 6 for n in kicks[1:])
        if 'Snare' in layers:
            assert [v1.event_cell(n) for n in back if bar_of(n) == bar] == [4, 12]
        for track, layer in ((BASS, 'Bass'), (KEYS, 'Keys'), (LEAD, 'Lead')):
            assert bool([n for n in nt[track] if bar_of(n) == bar]) == (layer in layers)
    # Bass: root on the grid at beat one, pops exactly root + 12, range E1..D3, downbeat anchor rules.
    bass_bars = [b for b in range(1, n_bars + 1) if 'Bass' in layers_at(s, b)]
    for bar in bass_bars:
        phase = (bar - 1) % 4
        root = bass_root(s['chords'][s['order'][phase]][1])
        in_bar = [n for n in nt[BASS] if bar_of(n) == bar]
        assert v1.event_cell(in_bar[0]) == 0 and in_bar[0][2] == root
        assert len([n for n in in_bar if n[2] == root + 12]) == (1 if phase in (1, 3) else 0)
        assert len([n for n in in_bar if v1.event_cell(n) % 2]) <= 1
    assert all(28 <= n[2] <= 48 for n in nt[BASS]) and all(48 <= n[2] <= 72 for n in nt[KEYS])
    bass16 = [v1.event_cell(n) % 2 == 1 for n in nt[BASS]]
    assert not any(x and y for x, y in zip(bass16, bass16[1:]))   # no two anticipations in a row
    bass16_ratio = sum(bass16) / len(bass16)
    assert bass16_ratio <= 0.30
    # Keys downbeat anchor: beat one or three on the grid every bar, at most one e/a attack per bar.
    for bar in sorted({k[0] for k in attacks}):
        cells = [v1.event_cell(n) for k, n in attacks.items() if k[0] == bar]
        assert 0 in cells or 8 in cells, bar
        assert len([c for c in cells if c % 2]) <= 1, bar
    keys16_ratio = len([n for n in attacks.values() if v1.event_cell(n) % 2]) / len(attacks)
    assert keys16_ratio <= 0.25
    # A2 voicings only rearrange the v1 chord tones.
    for chord_name, _, _, voicing in s['chords']:
        assert Counter(p % 12 for p in A2_VOICING[chord_name]) == Counter(p % 12 for p in voicing)
    lead_bars = Counter(bar_of(n) for n in nt[LEAD])
    assert set(lead_bars) == set(range(brk - 8, brk)) | set(range(a2, outro))
    assert max(lead_bars.values()) <= 6
    assert max(abs(x[2] - y[2]) for x, y in zip(nt[LEAD], nt[LEAD][1:])) <= 7
    assert min(n[2] for n in nt[LEAD] if n[1] > 80) > max(n[2] for n in nt[KEYS2])   # ornaments excluded
    # Keys2 never attacks together with the lead (grace notes and turns included): onset gap >= MIN_GAP per bar.
    gap = min(abs(k[0] - l[0]) for k in nt[KEYS2] for l in nt[LEAD] if bar_of(k) == bar_of(l))
    assert gap >= MIN_GAP
    # Every lead bar carries the v1 motif pitches in order (ornaments only add notes around them).
    for b in lead_bars:
        variant = b >= a2 and ((b - a2) // 4) % 2 == 1
        played = iter(n[2] for n in nt[LEAD] if bar_of(n) == b)
        assert all(p in played for p in v1.lead_phrase(s, (b - 1) % 4, variant)[0]), b
    assert {bar_of(n) for n in ride} == set(range(a2, outro))
    assert not [n for n in drums if n[2] == HAT and a2 <= bar_of(n) < outro and v1.event_cell(n) % 2 == 0]
    assert min(Counter(bar_of(n) for n in ride).values()) >= 3   # closed-hat slots left free by kick, snare and ghosts
    # Hat family (closed/open/ride/16th) on adjacent sixteenth cells: longest run per bar <= 2.
    hat_run = 0
    for bar in range(1, n_bars + 1):
        cells = {v1.event_cell(n) for n in drums if bar_of(n) == bar and n[2] in (HAT, OHAT, RIDE)}
        run = 0
        for cell in range(16):
            run = run + 1 if cell in cells else 0
            hat_run = max(hat_run, run)
    assert hat_run <= 2
    opened = Counter((bar_of(n) - 1) // 8 for n in drums if n[2] == OHAT)
    hat_blocks = {(b - 1) // 8 for b in range(1, n_bars + 1) if 'Hats' in layers_at(s, b)}
    assert set(opened) == hat_blocks
    assert max(Counter((bar_of(n) - 1) // 4 for n in drums if n[2] == OHAT).values()) == 1   # <= 1 open hat per four bars
    # Sixteenth-position hats sit only on the e of beats two and four (cells 5 and 13); ride and open hat on eighths.
    hat_odd = {v1.event_cell(n) for n in drums if n[2] in (HAT, OHAT, RIDE) and v1.event_cell(n) % 2}
    assert hat_odd <= {5, 13}
    assert {bar_of(n) for n in groups['crash']} == {a, brk, a2, outro}
    for bar, text in v1.markers(n_bars):
        assert bytes([0xff, 6, len(text)]) + text.encode() in smf
    last_end = max(n[0] + n[1] for notes in nt.values() for n in notes)
    assert bt(n_bars) < last_end < bt(n_bars + 1)
    fmt = lambda rates: ' '.join(f'{k}={v:.1f}' for k, v in rates.items())
    mins = ' '.join(f"{k}={floor[k]}" for k in ('intro', 'break', 'outro'))
    print(f"check {s['sid']}-v2 PASS notes/bar {fmt(density)} (A/A2 min bar={floor['A/A2']}; per-bar min {mins}) "
          f"| bass/bar {fmt(bass_rate)} "
          f"range={min(n[2] for n in nt[BASS])}..{max(n[2] for n in nt[BASS])} pops=root+12 CC7=85@0 "
          f"bass16={bass16_ratio:.0%} | keys_attacks/bar {fmt(keys_rate)} keys16={keys16_ratio:.0%} "
          f"anchor=beat1/3 every bar | lead_max/bar={max(lead_bars.values())} keys2_lead_gap>={gap} | "
          f"keys2={ranges(keys2_bars)} tex={ranges(tex_bars)} pad={ranges(pad_bars)} ride={ranges({bar_of(n) for n in ride})} "
          f"fills={','.join(map(str, fill_bars))} CC1={cc1} CC11={cc11} "
          f"vel[{' '.join(f'{k}={v}' for k, v in vel_span.items())}] "
          f"hat_16th_run<={hat_run} drum_cell_collisions={sum(c - 1 for c in collisions.values())} overlap={overlaps} "
          f"last_end={last_end}/{n_bars * BAR}")


if __name__ == '__main__':
    for sketch in SKETCHES:
        result = compose(sketch['sid'])
        nt, cc, pcs, n_bars, bpm, title, sf, minor = result
        smf = build_smf(title, bpm, sf, minor, n_bars, TRACKS, pcs, nt, cc, v1.markers(n_bars))
        check(sketch, result, smf)
        print(write_smf(os.path.join(SK_DIR, sketch['sid'] + '-v2.mid'), smf))
