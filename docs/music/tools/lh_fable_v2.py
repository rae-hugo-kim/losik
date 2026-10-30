"""Slot 14 density calibration (model fable); Python 3.9 stdlib.

Keeps lh_fable's chord loop, key, BPM, bar count, kick cells, backbeat and lead
motif for lh14-brass-orchard and layers the v2 additions from
LOFI_HIPHOP_SET_BRIEF.md: a bass line with passing tones and octave pops,
three-attack comping with inner-voice motion, a Keys2 counter-line, a nylon
arpeggio with thumb bass from bar 1 to the end, a swelling pad, fills, hat
variation per eight bars, ride for closed hats in A2, lead ornaments and
CC1/CC11 expression. Every note velocity is clamped to the brief's table (VEL).
"""
import os
from collections import Counter

from pipeline import BAR, PPQ, SK_DIR, bt, hum_t, hum_v, seed, build_smf, write_smf
from sketches import PC, mk_chord2
import lh_fable as v1

TRACKS = [('Drums', 9), ('Bass', 0), ('Keys', 1), ('Keys2', 2), ('Tex', 3), ('Lead', 4), ('Pad', 5)]
DRUMS, BASS, KEYS, KEYS2, TEX, LEAD, PAD = range(7)
KICK, SNARE, HAT, OHAT, CRASH, RIDE = 36, 38, 42, 46, 49, 51
TOMS = (48, 47, 45)
SKETCHES = [s for s in v1.SKETCHES if s['slot'] == 14]
MAJOR = (0, 2, 4, 5, 7, 9, 11)
# Velocity ranges from the brief's recipe table (v1) plus the v2 rows; fills sit between ghost and backbeat.
VEL = dict(kick=(96, 110), snare=(86, 100), ghost=(38, 52), hat_on=(48, 60), hat_off=(68, 84),
           hat16=(40, 50), ohat=(68, 84), ride=(55, 70), crash=(55, 70), fill=(56, 84),
           bass=(60, 82), keys=(72, 92), keys2=(55, 72), tex=(55, 72), lead=(60, 82), pad=(45, 60))
# Three comping attacks a bar; v1 had two on phases 0-2.
COMP = ((0, 1.5, 2.75), (0, 1.25, 3), (0, 1.5, 2.75), (0.5, 1.5, 2.5))
# A2 re-voicing: the same chord tones rearranged (bottom voice up an octave, top voice down).
A2_VOICING = {'Emaj9': (59, 63, 66, 68), 'Amaj9': (59, 61, 64, 68),
              'G#m7': (56, 59, 63, 66), 'C#m9': (52, 59, 63, 68)}
OPEN_HAT = ((1, 7), (3, 3), (1, 5), (2, 7))   # (loop phase, eighth) per eight-bar block
# Keys2 in A2: chord-tone riff on phrase bars one and two, a two-bar response on bars three and four.
# Beats interlock with the lead's onsets (motif, grace before note two, turn on bar three).
KEYS2_RIFF = (((0, 1), (1.5, 2), (2.5, 3), (3.5, 0)), ((1, 1), (3, 2), (3.5, 0)))   # (beat, voice index)
RESPONSE_BEATS = ((0, 1, 3.5), (0.5, 1.5, 2.5))
MIN_GAP = 120   # ticks between any Keys2 onset and any lead onset in the same bar


def scale_of(s):
    return {(PC[s['tonic']] + degree) % 12 for degree in MAJOR}


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
    layers = {'Keys', 'Tex', 'Pad'}
    if brk <= bar < a2:
        return layers | v1.break_layers(s['slot'], bar - brk)
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
    """Root in E1..C3 (28-40) so an octave pop stays inside the bass range."""
    return fold(24 + PC[root], 28, 40)


def bass_line(s, phase, root, quality, next_root):
    """(beat, pitch, base velocity): kick anchors, a chord tone on beat two, a chromatic
    approach into the next root, an octave pop on loop bars two and three; bar four rests after beat three."""
    cell = s['kicks'][phase]
    low = bass_root(root)
    third = low + (3 if quality == 'm7' else 4)
    fifth = low + 7
    seventh = low + (11 if quality == 'M7' else 10)
    anchors = {0: (fifth, low), 1: (third, low), 2: (fifth, low), 3: (seventh, fifth)}[phase]
    notes = [(cell[0], low, 78), (cell[1], anchors[0], 70), (cell[2], anchors[1], 72),
             (1.0, fifth if phase == 1 else third, 68)]
    if phase in (1, 2):
        notes.append((3.25, low + 12, 70))
    if phase < 3:
        notes.append((3.5, bass_root(next_root) + (1 if phase == 1 else -1), 66))
    return sorted(notes)


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
    seed(261030 + s['slot'] * 97)
    nt, cc = {i: [] for i in range(7)}, {i: [] for i in range(7)}
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
            for beat in (0.75, 2.25) if fill else v1.ghost_beats(s['energy'], phase):
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
            line = bass_line(s, phase, root, quality, next_root)
            for index, (beat, pitch, base) in enumerate(line):
                next_beat = line[index + 1][0] if index + 1 < len(line) else 4
                duration = 110 if beat == 3.25 else min(460, int((next_beat - beat) * PPQ) - 40)
                add(BASS, bar, tick(bar, beat), duration, pitch, velocity(base, 'bass'))
        if 'Keys' in layers:
            voicing = A2_VOICING[name] if in_a2 else chord
            mover, moved = moving_voice(voicing, scale)
            beats = COMP[phase]
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
                pitches, beats = s['melody'][phase], s['lead_beats'][phase]
            elif phase < 2:
                low = sorted(fold(p, 50, 62) for p in chord)
                for beat, voice in KEYS2_RIFF[phase]:
                    add(KEYS2, bar, tick(bar, beat, swung=True), 200, low[voice], velocity(62, 'keys2'))
                pitches, beats = (), ()
            else:
                # Two-bar response echoing the lead's opening bars between its notes.
                pitches, beats = s['melody'][phase - 2], RESPONSE_BEATS[phase - 2]
            for index, (beat, pitch) in enumerate(zip(beats, pitches)):
                next_beat = beats[index + 1] if index + 1 < len(beats) else 4
                add(KEYS2, bar, tick(bar, beat, swung=True), min(400, int((next_beat - beat) * PPQ) - 48),
                    pitch - 12, velocity(64, 'keys2'))
        if 'Tex' in layers:
            order = [s['tex_order'][(i + phase) % 4] for i in range(4)]
            pattern = order + [order[2], order[1], order[3], order[0]]
            base = (59, 63, 68, 61)[phase]
            for beat in (0, 2):   # thumb bass under the arpeggio
                add(TEX, bar, tick(bar, beat), 700, thumb_root(root), velocity(base - 3, 'tex'))
            for eighth in range(8):
                add(TEX, bar, tick(bar, eighth / 2, swung=True), 190, chord[pattern[eighth]], velocity(base, 'tex'))
            # Two sixteenth pluck-backs every bar: before beat two on even loop bars, before four on odd.
            pair = (3.25, 3.75) if phase % 2 else (1.25, 1.75)
            for beat, voice in zip(pair, (order[1], order[2])):
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
            # 1+5+9; a plain m7 (no ninth in the name) takes the third an octave up instead.
            for pitch in (low, low + 7, low + (15 if name.endswith('m7') else 14)):
                add(PAD, bar, when, BAR, pitch, velocity(52, 'pad'))
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
    assert pcs == {DRUMS: 0, BASS: 38, KEYS: 4, KEYS2: 0, TEX: 24, LEAD: 24, PAD: 89}
    _, (a, _), (brk, _), (a2, _), (outro, _) = v1.markers(n_bars)
    sections = (('intro', 1, a - 1), ('A', a, brk - 1), ('break', brk, a2 - 1), ('A2', a2, outro - 1),
                ('outro', outro, n_bars))
    per_bar = Counter(bar_of(n) for notes in nt.values() for n in notes)
    density = {name: sum(per_bar[b] for b in range(lo, hi + 1)) / (hi - lo + 1) for name, lo, hi in sections}
    assert density['intro'] >= 25 and density['break'] >= 25
    assert all(per_bar[b] >= 45 for b in list(range(a, brk)) + list(range(a2, outro)))
    bass_rate = {name: len([n for n in nt[BASS] if lo <= bar_of(n) <= hi]) / (hi - lo + 1)
                 for name, lo, hi in sections if name in ('A', 'A2')}
    assert min(bass_rate.values()) >= 4
    keys_rate = {name: len({(bar_of(n), n[0]) for n in nt[KEYS] if lo <= bar_of(n) <= hi}) / (hi - lo + 1)
                 for name, lo, hi in sections if name in ('A', 'A2')}
    assert min(keys_rate.values()) >= 3
    keys2_bars = {bar_of(n) for n in nt[KEYS2]}
    assert keys2_bars == {a, a + 1} | set(range(a2, outro))
    tex_bars = Counter(bar_of(n) for n in nt[TEX])
    pad_bars = Counter(bar_of(n) for n in nt[PAD])
    assert set(tex_bars) == set(pad_bars) == set(range(1, n_bars + 1))
    assert min(tex_bars.values()) >= 12 and set(pad_bars.values()) == {3}
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
    cc1 = len([c for c in cc[LEAD] if c[1] == 1])
    cc11 = len([c for track in (KEYS, PAD) for c in cc[track] if c[1] == 11])
    assert cc1 and cc11
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
    # Bass: root an octave below middle, pops exactly root + 12, range E1..C3.
    for bar in (b for b in range(1, n_bars + 1) if 'Bass' in layers_at(s, b)):
        phase = (bar - 1) % 4
        root = bass_root(s['chords'][s['order'][phase]][1])
        in_bar = [n for n in nt[BASS] if bar_of(n) == bar]
        assert v1.event_cell(in_bar[0]) == 0 and in_bar[0][2] == root
        pops = [n for n in in_bar if v1.event_cell(n) == 13]
        assert len(pops) == (1 if phase in (1, 2) else 0) and all(n[2] == root + 12 for n in pops)
    assert all(28 <= n[2] <= 48 for n in nt[BASS]) and all(48 <= n[2] <= 72 for n in nt[KEYS])
    # A2 voicings only rearrange the v1 chord tones.
    for chord_name, _, _, voicing in s['chords']:
        assert Counter(p % 12 for p in A2_VOICING[chord_name]) == Counter(p % 12 for p in voicing)
    lead_bars = Counter(bar_of(n) for n in nt[LEAD])
    assert set(lead_bars) == set(range(brk - 8, brk)) | set(range(a2, outro))
    assert max(lead_bars.values()) <= 6
    assert max(abs(x[2] - y[2]) for x, y in zip(nt[LEAD], nt[LEAD][1:])) <= 7
    assert min(n[2] for n in nt[LEAD] if n[1] > 80) > max(n[2] for n in nt[KEYS2])   # ornaments excluded
    # Keys2 never attacks together with the lead: onset gap >= MIN_GAP ticks within a bar.
    gap = min(abs(k[0] - l[0]) for k in nt[KEYS2] for l in nt[LEAD] if bar_of(k) == bar_of(l))
    assert gap >= MIN_GAP
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
    assert set(opened) == set(range(n_bars // 8))
    assert {bar_of(n) for n in groups['crash']} == {a, brk, a2, outro}
    for bar, text in v1.markers(n_bars):
        assert bytes([0xff, 6, len(text)]) + text.encode() in smf
    last_end = max(n[0] + n[1] for notes in nt.values() for n in notes)
    assert bt(n_bars) < last_end < bt(n_bars + 1)
    fmt = lambda rates: ' '.join(f'{k}={v:.1f}' for k, v in rates.items())
    a_min = min(per_bar[b] for b in list(range(a, brk)) + list(range(a2, outro)))
    print(f"check {s['sid']}-v2 PASS notes/bar {fmt(density)} (A/A2 min bar={a_min}) | bass/bar {fmt(bass_rate)} "
          f"range={min(n[2] for n in nt[BASS])}..{max(n[2] for n in nt[BASS])} pops=root+12 | "
          f"keys_attacks/bar {fmt(keys_rate)} | lead_max/bar={max(lead_bars.values())} keys2_lead_gap>={gap} | "
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
