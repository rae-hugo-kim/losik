"""Ten first-pass lo-fi hip hop compositions; run with Python 3.9 stdlib.

Beat offsets are zero-based; MIDI programs are zero-based. The lo-fi brief,
not the older house recipe, controls swing, dynamics and instrumentation.
"""
import os
import re
from collections import Counter
from pathlib import Path

from pipeline import BAR, PPQ, SK_DIR, SW, bt, hum_t, hum_v, seed, build_smf, write_smf
from sketches import PC, mk_chord2

TRACKS = [('Drums', 9), ('Bass', 0), ('Keys', 1), ('Tex', 2), ('Lead', 3)]

# Chord tuples: name, root, utility quality, four-voice jazz voicing.
SKETCHES = [
    dict(slot=1, sid='lh01-felt-doorway', title='Felt Doorway', bpm=76, bars=56,
         key='D minor', energy=1, sf=-1, minor=True, tonic='D', swing=28,
         keys_pc=4, tex_pc=24, lead_pc=4,
         chords=[('Dm9', 'D', 'm7', (53, 57, 60, 64)),
                 ('G13', 'G', '7', (53, 59, 64, 69))], order=(0, 0, 1, 1),
         kicks=((0, 1.75), (0, 2.75), (0, 1.5), (0, 2.5)),
         comp=((0,), (0.5,), (0,), (1.5,)),
         melody=((69, 67, 64), (65, 64, 62), (64, 67, 69), (71, 69, 67)),
         lead_beats=((0.5, 1.5, 3), (0, 1.5, 2.5), (0.5, 2, 3), (0, 1, 2.5)),
         tex_beats=((0.5, 2.5), (1.5,), (0.5, 3), (2,)), tex_order=(0, 2, 1, 3),
         break_id='keys-then-picking',
         notes='Dorian two-chord doorway; keys and hats open together; four-bar descending answer.'),
    dict(slot=4, sid='lh04-paper-saucer', title='Paper Saucer', bpm=78, bars=56,
         key='C major', energy=2, sf=0, minor=False, tonic='C', swing=26,
         keys_pc=0, tex_pc=16, lead_pc=24,
         chords=[('Cmaj7', 'C', 'M7', (52, 55, 59, 60)),
                 ('Em7', 'E', 'm7', (52, 55, 59, 62)),
                 ('Dm9', 'D', 'm7', (53, 57, 60, 64)),
                 ('G13', 'G', '7', (53, 59, 64, 69))], order=(0, 1, 2, 3),
         kicks=((0, 1.5, 2.75), (0, 2.5), (0, 1.75), (0, 1.5, 2.5)),
         comp=((0.5, 2), (0, 2.75), (1, 3), (0.5,)),
         melody=((67, 71, 69), (67, 66, 64), (65, 64, 60), (62, 64, 67)),
         lead_beats=((0, 1.5, 3), (0.5, 1.5, 3), (0, 2, 3), (0.5, 2, 3)),
         tex_beats=((0,), (0.5,), (0,), (1,)), tex_order=(1, 2, 0, 3),
         break_id='backbeat-organ',
         notes='I-iii-ii-V grand-piano comping; nylon lead has a rising third and stepwise reply.'),
    dict(slot=7, sid='lh07-moss-index', title='Moss Index', bpm=82, bars=64,
         key='E minor', energy=2, sf=1, minor=True, tonic='E', swing=30,
         keys_pc=4, tex_pc=27, lead_pc=0,
         chords=[('Em9', 'E', 'm7', (55, 59, 62, 66)),
                 ('Am7', 'A', 'm7', (55, 57, 60, 64)),
                 ('Bm7', 'B', 'm7', (54, 57, 59, 62))], order=(0, 1, 2, 0),
         kicks=((0, 2.5), (0, 1.75, 2.75), (0, 1.5), (0, 2.75)),
         comp=((0, 2.25), (0.75,), (1.5, 3), (0,)),
         melody=((71, 69, 67, 66), (64, 67, 64), (66, 69, 71), (69, 67, 66, 64)),
         lead_beats=((0, 1, 2.5, 3.5), (0.5, 2, 3), (0, 1.5, 3), (0.5, 1.5, 2.5, 3.5)),
         tex_beats=((0, 1.5, 3), (0.5, 2), (1, 2.5, 3.5), (0.5, 2.5)),
         tex_order=(3, 1, 2, 0), break_id='unplugged-duet',
         notes='Minor i-iv-v-i; a descending four-note piano bookmark rides alternating guitar gaps.'),
    dict(slot=10, sid='lh10-copper-margin', title='Copper Margin', bpm=84, bars=64,
         key='B minor', energy=3, sf=2, minor=True, tonic='B', swing=32,
         keys_pc=4, tex_pc=24, lead_pc=4,
         chords=[('Bm9', 'B', 'm7', (50, 54, 57, 61)),
                 ('Dmaj7', 'D', 'M7', (54, 57, 61, 62)),
                 ('Gmaj7', 'G', 'M7', (54, 55, 59, 62)),
                 ('F#9', 'F#', '7', (52, 58, 61, 68))], order=(0, 1, 2, 3),
         kicks=((0, 1.5, 2.5), (0, 1.75, 2.75), (0, 1.5, 2.75), (0, 1.75, 2.5)),
         comp=((0, 1.75, 3), (0.5, 2.5), (0, 2, 3.5), (1, 2.75)),
         melody=((66, 69, 73, 69), (69, 66, 64), (66, 67, 71, 69), (68, 66, 64, 66)),
         lead_beats=((0.5, 1, 2, 3.5), (0, 1.5, 3), (0.5, 1.5, 2.5, 3.5), (0, 1, 2.5, 3.5)),
         tex_beats=((0.5, 1.5, 2.5, 3.5), (0, 1.5, 3), (0.5, 2, 3), (1, 2.5)),
         tex_order=(0, 2, 3, 1), break_id='rhythm-negative',
         notes='i-III-VI-V9 peak entry; an EP minor-third ladder resolves into a dominant ninth.'),
    dict(slot=13, sid='lh13-apricot-carbon', title='Apricot Carbon', bpm=88, bars=64,
         key='A major', energy=3, sf=3, minor=False, tonic='A', swing=29,
         keys_pc=0, tex_pc=4, lead_pc=24,
         chords=[('Amaj7', 'A', 'M7', (49, 52, 56, 57)),
                 ('C#m7', 'C#', 'm7', (52, 56, 59, 61)),
                 ('F#m9', 'F#', 'm7', (57, 61, 64, 68)),
                 ('Bm9', 'B', 'm7', (50, 54, 57, 61))], order=(0, 1, 2, 3),
         kicks=((0, 1.75, 2.5), (0, 1.5), (0, 1.5, 2.75), (0, 2.5, 2.75)),
         comp=((0.25, 2), (0.5, 2, 3.5), (0, 1.5), (0.75, 2.5)),
         melody=((69, 73, 71, 69), (68, 71, 68), (69, 68, 66, 64), (66, 69, 73, 71)),
         lead_beats=((0, 1, 2.5, 3.5), (0.5, 1.5, 3), (0, 1.5, 2.5, 3.5), (0.5, 1.5, 2.5, 3.5)),
         tex_beats=((0, 2), (1, 3), (0.5, 2.5), (1.5, 3)), tex_order=(2, 0, 3, 1),
         break_id='kickless-bloom',
         notes='Warm I-iii-vi-ii at the high point; nylon turns around a repeated A-C#-B-A arch.'),
    dict(slot=16, sid='lh16-indigo-receipt', title='Indigo Receipt', bpm=86, bars=64,
         key='C# minor', energy=3, sf=4, minor=True, tonic='C#', swing=31,
         keys_pc=4, tex_pc=16, lead_pc=0,
         chords=[('C#m9', 'C#', 'm7', (52, 56, 59, 63)),
                 ('Emaj7', 'E', 'M7', (51, 52, 56, 59)),
                 ('Bmaj7', 'B', 'M7', (51, 54, 58, 59)),
                 ('G#7b13', 'G#', '7', (54, 60, 64, 70))], order=(0, 1, 2, 3),
         kicks=((0, 1.5, 2.75), (0, 1.75, 2.5), (0, 2.75), (0, 1.5, 2.5)),
         comp=((0.5, 1.75, 3.25), (0, 2.5), (1, 2.75), (0.25, 2)),
         melody=((68, 66, 63), (64, 66, 68, 71), (66, 63, 66), (68, 70, 72, 70)),
         lead_beats=((0.5, 2, 3), (0, 1, 2.5, 3.5), (0.5, 1.5, 3), (0, 1.5, 2.5, 3.5)),
         tex_beats=((0.5,), (0,), (1,), (0.25,)), tex_order=(3, 2, 1, 0),
         break_id='organ-handoff',
         notes='i-III-VII-V7b13 hinge; piano rises through E major then turns around the leading tone B#.'),
    dict(slot=19, sid='lh19-pearl-crossing', title='Pearl Crossing', bpm=84, bars=64,
         key='F# major', energy=2, sf=6, minor=False, tonic='F#', swing=27,
         keys_pc=0, tex_pc=27, lead_pc=4,
         chords=[('F#maj7', 'F#', 'M7', (53, 54, 58, 61)),
                 ('G#m9', 'G#', 'm7', (54, 59, 63, 70)),
                 ('A#m7', 'Bb', 'm7', (56, 58, 61, 65)),
                 ('Bmaj7', 'B', 'M7', (54, 58, 59, 63))], order=(0, 1, 2, 3),
         kicks=((0, 2.75), (0, 1.5, 2.5), (0, 1.75), (0, 1.5, 2.75)),
         comp=((0, 2.5), (1.25,), (0.5, 3), (1,)),
         melody=((70, 68, 65), (66, 68, 70), (73, 72, 70), (70, 66, 63)),
         lead_beats=((0.5, 1.5, 3), (0, 2, 3), (0.5, 2, 3.5), (0, 1.5, 2.5)),
         tex_beats=((1, 3), (0.5, 1.5, 2.5), (0, 2), (1.5, 3.5)),
         tex_order=(1, 3, 2, 0), break_id='snare-to-hats',
         notes='Stepwise I-ii-iii-IV drift; EP rises to C# then lets the answering phrase fall.'),
    dict(slot=22, sid='lh22-plum-platform', title='Plum Platform', bpm=80, bars=64,
         key='Bb minor', energy=2, sf=-5, minor=True, tonic='Bb', swing=28,
         keys_pc=4, tex_pc=24, lead_pc=0,
         chords=[('Bbm9', 'Bb', 'm7', (49, 53, 56, 60)),
                 ('Gbmaj7', 'F#', 'M7', (53, 58, 61, 66)),
                 ('Ab13', 'Ab', '7', (54, 60, 65, 70)),
                 ('Ebm9', 'Eb', 'm7', (54, 58, 61, 65))], order=(0, 1, 2, 3),
         kicks=((0, 1.5), (0, 2.5, 2.75), (0, 1.75, 2.5), (0, 2.75)),
         comp=((1, 2.5), (0, 3), (0.75, 2.25), (0.5,)),
         melody=((65, 68, 65), (66, 65, 61), (60, 61, 65), (65, 63, 61)),
         lead_beats=((0, 1.5, 3), (0.5, 2, 3), (0, 1, 2.5), (0.5, 1.5, 3)),
         tex_beats=((0.5, 2), (1, 3), (0, 1.5, 3), (2.5,)), tex_order=(2, 1, 3, 0),
         break_id='rhythm-to-harmony',
         notes='i-VI-VII13-iv suspended return; grand-piano F-Ab-F sigh answers downward over the minor subdominant.'),
    dict(slot=25, sid='lh25-wool-calendar', title='Wool Calendar', bpm=78, bars=56,
         key='F minor', energy=2, sf=-4, minor=True, tonic='F', swing=25,
         keys_pc=0, tex_pc=27, lead_pc=24,
         chords=[('Fm9', 'F', 'm7', (56, 60, 63, 67)),
                 ('Dbmaj7', 'Db', 'M7', (53, 56, 60, 61)),
                 ('Eb9', 'Eb', '7', (55, 58, 61, 65))], order=(0, 0, 1, 2),
         kicks=((0, 1.75), (0, 1.5), (0, 2.75), (0, 1.75, 2.5)),
         comp=((0.75,), (0, 2.75), (1.5,), (0.5, 3)),
         melody=((68, 67, 65), (63, 60, 63), (65, 68, 65), (65, 63, 61)),
         lead_beats=((0.5, 1.5, 3), (0, 2, 3), (0.5, 2, 3), (0, 1.5, 3)),
         tex_beats=((0, 2.5), (1.5,), (0.5, 3), (2,)), tex_order=(3, 0, 2, 1),
         break_id='picking-to-keys',
         notes='Two bars of i then VI-VII9; a close nylon descent softens the cooldown handoff.'),
    dict(slot=28, sid='lh28-amber-bookend', title='Amber Bookend', bpm=74, bars=56,
         key='Eb major', energy=1, sf=-3, minor=False, tonic='Eb', swing=24,
         keys_pc=4, tex_pc=16, lead_pc=0,
         chords=[('Ebmaj7', 'Eb', 'M7', (55, 58, 62, 63)),
                 ('Abmaj7', 'Ab', 'M7', (55, 56, 60, 63)),
                 ('Fm9', 'F', 'm7', (56, 60, 63, 67)),
                 ('Bb13', 'Bb', '7', (56, 62, 67, 72))], order=(0, 1, 2, 3),
         kicks=((0, 2.5), (0, 1.5), (0, 2.75), (0, 1.75)),
         comp=((0,), (1,), (0.5,), (0, 2.5)),
         melody=((67, 65, 63), (63, 60, 63), (65, 67, 65), (62, 65, 67)),
         lead_beats=((0, 1.5, 3), (0.5, 2, 3), (0, 2, 3), (0.5, 1.5, 3)),
         tex_beats=((1,), (0.5,), (0,), (1.5,)), tex_order=(0, 3, 1, 2),
         break_id='hat-dissolve',
         notes='I-IV-ii-V13 closing warmth; grand-piano descending thirds leave room for slots 29-30.'),
]


def markers(n_bars):
    return [(1, 'intro'), (9, 'A'), (25 if n_bars == 56 else 29, 'break'),
            (33 if n_bars == 56 else 37, 'A2'), (n_bars - 7, 'outro')]


def break_layers(slot, offset):
    """Actual eight-bar drop arrangements; names are also published in the log."""
    if slot == 1:
        return {'Keys'} | ({'Tex'} if offset >= 4 else set())
    if slot == 4:
        return {'Snare', 'Hats', 'Keys', 'Tex'}
    if slot == 7:
        return {'Keys', 'Tex'}
    if slot == 10:
        return {'Kick', 'Snare', 'Hats', 'Bass'}
    if slot == 13:
        return {'Snare', 'Hats', 'Keys'} | ({'Tex'} if offset >= 4 else set())
    if slot == 16:
        return ({'Keys'} if offset < 6 else set()) | ({'Tex'} if offset >= 2 else set())
    if slot == 19:
        return {'Keys', 'Tex', 'Snare' if offset < 4 else 'Hats'}
    if slot == 22:
        return {'Kick', 'Snare', 'Hats', 'Bass'} if offset < 4 else {'Keys', 'Tex'}
    if slot == 25:
        return {'Keys'} | ({'Tex'} if offset < 4 else set())
    return {'Keys'} | ({'Hats'} if offset < 4 else set())


def layers_at(s, bar):
    _, _, (brk, _), (a2, _), (outro, _) = markers(s['bars'])
    if brk <= bar < a2:
        return break_layers(s['slot'], bar - brk)
    layers = {'Keys'}
    if bar >= (1 if s['slot'] == 1 else 3):
        layers.add('Hats')
    if bar >= 5:
        layers.update(('Kick', 'Snare'))
    if 9 <= bar <= s['bars'] - 4:
        layers.add('Bass')
    if 9 <= bar < outro:
        layers.add('Tex')
    if brk - 8 <= bar < brk or a2 <= bar < outro:
        layers.add('Lead')
    if s['energy'] == 1 and bar > s['bars'] - 4:
        layers.difference_update(('Kick', 'Snare', 'Hats'))
    return layers


def compose(sid):
    s = next(s for s in SKETCHES if s['sid'] == sid)
    seed(211021 + s['slot'] * 101)
    nt, cc = {i: [] for i in range(5)}, {i: [] for i in range(5)}
    pcs = {0: 0, 1: 38 if s['energy'] == 3 else 33, 2: s['keys_pc'],
           3: s['tex_pc'], 4: s['lead_pc']}
    a2 = markers(s['bars'])[3][0]
    swing = SW + (s['swing'] - SW)

    def tick(bar, beat, swung=False):
        delay = swing if swung and beat % 1 == 0.5 else 0
        return hum_t(bt(bar, beat) + 14 + delay, 12)

    def velocity(base, low, high):
        return max(low, min(high, hum_v(base, 10)))

    def add(track, bar, when, duration, pitch, vel):
        end = min(when + duration, bt(bar + 1) - 24)
        assert when >= bt(bar) and end > when
        nt[track].append((when, end - when, pitch, vel))

    for bar in range(1, s['bars'] + 1):
        phase = (bar - 1) % 4
        name, root, quality, chord = s['chords'][s['order'][phase]]
        layers = layers_at(s, bar)
        occupied = set()
        kick_times = []

        def drum(beat, pitch, base, low, high, swung=False):
            cell = round(beat * 4)
            assert cell not in occupied
            occupied.add(cell)
            when = tick(bar, beat, swung)
            add(0, bar, when, 70 if pitch != 46 else 145, pitch, velocity(base, low, high))
            return when

        if 'Kick' in layers:
            # A shared per-bar jitter preserves the +6 downbeat accent exactly.
            kick_base = velocity(100 + (s['energy'] - 1), 96, 104)
            for beat in s['kicks'][phase]:
                when = tick(bar, beat)
                occupied.add(round(beat * 4))
                add(0, bar, when, 90, 36, kick_base + (6 if beat == 0 else 0))
                kick_times.append((beat, when))
        if 'Snare' in layers:
            for beat in (1, 3):
                pitch = 37 if s['energy'] == 1 and bar % 2 == 0 else 38
                drum(beat, pitch, 92 + s['energy'], 86, 100)
            ghosts = (0.75,) if s['energy'] == 1 else ((0.75, 2.25) if phase % 2 == 0 else (2.25, 3.75))
            for beat in ghosts:
                drum(beat, 38, 45, 38, 52)
        if bar == a2:
            # First A2 bar, second sixteenth: the crash never stacks with the kick.
            drum(0.25, 49, 62, 55, 70)
        if 'Hats' in layers:
            for eighth in range(8):
                beat = eighth / 2
                if round(beat * 4) in occupied:
                    continue
                offbeat = eighth % 2 == 1
                open_hat = bar % 4 == 0 and eighth == 7
                drum(beat, 46 if open_hat else 42, 76 if offbeat else 54,
                     68 if offbeat else 48, 84 if offbeat else 60, swung=offbeat)
            if s['energy'] == 3 and bar % 4 in (0, 1):
                drum(1.25 if phase % 2 == 0 else 3.25, 42, 45, 40, 50)
        if 'Bass' in layers:
            bass = mk_chord2(PC[root], quality)['bass']
            # Omit one kick per bar, not merely duplicate the entire kick cell.
            for index, (_, when) in enumerate(kick_times[:-1]):
                pitch = bass if index == 0 else bass + (12 if phase == 3 else 7)
                if pitch > 48:
                    pitch -= 12
                add(1, bar, when, 470 if index == 0 else 205, pitch,
                    velocity(70 + s['energy'], 60, 82))
        if 'Keys' in layers:
            beats = s['comp'][phase]
            for index, beat in enumerate(beats):
                when = tick(bar, beat)
                next_beat = beats[index + 1] if index + 1 < len(beats) else 4
                duration = int((next_beat - beat) * PPQ) - 60
                vel = velocity(82 if index == 0 else 78, 72, 92)
                for pitch in chord:
                    add(2, bar, when, duration, pitch, vel)
                cc[2].extend(((when - 1, 64, 0), (when + 1, 64, 100)))
            cc[2].extend(((bt(bar), 64, 0), (bt(bar + 1) - 2, 64, 0)))
        if 'Tex' in layers:
            for index, beat in enumerate(s['tex_beats'][phase]):
                when = tick(bar, beat, swung=True)
                if s['tex_pc'] == 16:
                    for pitch in (chord[0], chord[2]):
                        add(3, bar, when, int((3.8 - beat) * PPQ), pitch,
                            velocity(61, 55, 72))
                else:
                    pitch = chord[s['tex_order'][(index + phase) % 4]]
                    if s['tex_pc'] == 4:
                        pitch += 12
                    add(3, bar, when, 225, pitch, velocity(63, 55, 72))
        if 'Lead' in layers:
            pitches = s['melody'][phase]
            beats = s['lead_beats'][phase]
            for index, (beat, pitch) in enumerate(zip(beats, pitches)):
                # Every second A2 phrase delays the answer by an eighth, retaining pitch identity.
                if bar >= a2 and ((bar - a2) // 4) % 2 and index == len(pitches) - 1 and beat <= 3:
                    beat += 0.5
                next_beat = beats[index + 1] if index + 1 < len(beats) else 4
                duration = min(440, int((next_beat - beat) * PPQ) - 48)
                add(4, bar, tick(bar, beat, swung=True), duration, pitch,
                    velocity(70 + s['energy'], 60, 82))
    for events in nt.values():
        events.sort()
    for events in cc.values():
        events.sort()
    return nt, cc, pcs, s['bars'], s['bpm'], s['title'], s['sf'], s['minor']


def event_cell(note):
    return round(((note[0] % BAR) - 14) / (PPQ / 4))


def span(values):
    return f'{min(values)}..{max(values)}' if values else '-'


def check(s, result, smf):
    nt, cc, pcs, n_bars, bpm, title, sf, minor = result
    assert (n_bars, bpm, title, sf, minor) == (s['bars'], s['bpm'], s['title'], s['sf'], s['minor'])
    assert pcs == {0: 0, 1: 38 if s['energy'] == 3 else 33, 2: s['keys_pc'], 3: s['tex_pc'], 4: s['lead_pc']}
    drums = nt[0]
    kick = [n for n in drums if n[2] == 36]
    back = [n for n in drums if n[2] in (37, 38) and n[3] >= 86]
    ghost = [n for n in drums if n[2] == 38 and n[3] <= 52]
    hats_on = [n for n in drums if n[2] == 42 and event_cell(n) % 4 == 0]
    hats_off = [n for n in drums if n[2] == 42 and event_cell(n) % 4 == 2]
    hats_extra = [n for n in drums if n[2] == 42 and event_cell(n) % 2 == 1]
    opened = [n for n in drums if n[2] == 46]
    for notes, lo, hi in ((kick, 96, 110), (back, 86, 100), (ghost, 38, 52),
                           (hats_on, 48, 60), (hats_off, 68, 84), (opened, 68, 84),
                           (hats_extra, 40, 50), (nt[1], 60, 82), (nt[2], 72, 92),
                           (nt[3], 55, 72), (nt[4], 60, 82)):
        assert all(lo <= n[3] <= hi for n in notes)
    assert hats_on and hats_off and all(event_cell(n) in (5, 13) for n in hats_extra)
    assert all(28 <= n[2] <= 48 for n in nt[1])
    assert all(48 <= n[2] <= 72 for n in nt[2])
    assert all(n[0] in {k[0] for k in kick} for n in nt[1])
    assert all(c <= 1 for c in Counter(n[0] // (4 * BAR) for n in opened).values())
    collisions = Counter((n[0] // BAR, event_cell(n)) for n in drums)
    assert max(collisions.values()) == 1
    overlaps = 0
    for events in nt.values():
        ends = {}
        for when, duration, pitch, _ in events:
            overlaps += int(when < ends.get(pitch, -1))
            ends[pitch] = when + duration
    assert overlaps == 0
    _, _, (brk, _), (a2, _), (outro, _) = markers(n_bars)
    lead_bars = Counter(n[0] // BAR + 1 for n in nt[4])
    assert set(lead_bars) == set(range(brk - 8, brk)) | set(range(a2, outro))
    assert max(lead_bars.values()) <= 6
    assert max(abs(a[2] - b[2]) for a, b in zip(nt[4], nt[4][1:])) <= 7
    for bar in range(1, n_bars + 1):
        layers = layers_at(s, bar)
        in_bar = lambda ns: [n for n in ns if n[0] // BAR + 1 == bar]
        if 'Kick' in layers:
            cell = in_bar(kick)
            assert tuple(event_cell(n) / 4 for n in cell) == s['kicks'][(bar - 1) % 4]
            assert all(cell[0][3] == n[3] + 6 for n in cell[1:])
        if 'Snare' in layers:
            assert [event_cell(n) for n in in_bar(back)] == [4, 12]
            assert 1 <= len(in_bar(ghost)) <= 2
        if 'Keys' in layers:
            chord_onsets = Counter(n[0] for n in in_bar(nt[2]))
            assert 1 <= len(chord_onsets) <= 3 and set(chord_onsets.values()) == {4}
            pedal = [(t, v) for t, c, v in cc[2] if c == 64 and bt(bar) <= t < bt(bar + 1)]
            assert pedal[0][1] == 0 and pedal[-1][1] == 0 and any(v == 100 for _, v in pedal)
        if 'Bass' in layers:
            assert len(in_bar(kick)) - len(in_bar(nt[1])) in (1, 2)
        for track, layer in ((1, 'Bass'), (2, 'Keys'), (3, 'Tex'), (4, 'Lead')):
            assert bool(in_bar(nt[track])) == (layer in layers)
    jitter = [n[0] % BAR - 14 - event_cell(n) * 120 -
              (s['swing'] if n[2] in (42, 46) and event_cell(n) % 4 == 2 else 0) for n in drums]
    assert min(jitter) >= -12 and max(jitter) <= 12
    assert min(jitter) <= -10 and max(jitter) >= 10
    crashes = [n for n in drums if n[2] == 49]
    assert len(crashes) == 1 and crashes[0][0] // BAR + 1 == a2 and 55 <= crashes[0][3] <= 70
    for bar, text in markers(n_bars):
        assert bytes([0xff, 6, len(text)]) + text.encode() in smf
    last_end = max(n[0] + n[1] for notes in nt.values() for n in notes)
    assert bt(n_bars) < last_end < bt(n_bars + 1)
    describe = lambda ns: f'{len(ns)}@{span([n[3] for n in ns])}'
    print(f"check {s['sid']} PASS kick={describe(kick)} snare/rim={describe(back)} "
          f"ghost={describe(ghost)} hat_on={describe(hats_on)} hat_off={describe(hats_off)} "
          f"hat16={describe(hats_extra)} open={describe(opened)} swing={s['swing']} "
          f"jitter={span(jitter)} bass={span([n[2] for n in nt[1]])}@{span([n[3] for n in nt[1]])} "
          f"keys={span([n[2] for n in nt[2]])}@{span([n[3] for n in nt[2]])}/CC64=yes "
          f"lead={brk-8}-{brk-1},{a2}-{outro-1}/max={max(lead_bars.values())} "
          f"overlap={overlaps} drum_cell_collisions=0 markers={markers(n_bars)} "
          f"last_end={last_end}/{n_bars * BAR}")


def loop_signature(loop):
    """Canonical root intervals and quality families across rotations/transpositions."""
    return min(tuple(((root - rotated[0][0]) % 12, quality)
                     for root, quality in rotated)
               for offset in range(len(loop))
               for rotated in (loop[offset:] + loop[:offset],))


def check_set():
    # Import only when checking: both later passes import this module's SKETCHES.
    from lh_fable import SKETCHES as fable_sketches
    from lh_opus import SKETCHES as opus_sketches

    def signature(s):
        return loop_signature(tuple((PC[root], quality)
                                    for _, root, quality, _ in
                                    (s['chords'][i] for i in s['order'])))

    signatures = []
    motifs = []
    for s in SKETCHES:
        signatures.append(signature(s))
        pitches = [p for bar in s['melody'] for p in bar]
        motifs.append((tuple(b - a for a, b in zip(pitches, pitches[1:])), s['lead_beats']))
    assert len(set(signatures)) == len(set(motifs)) == 10
    # Quality families deliberately collapse m7/m9, maj7/maj9 and 9/13.
    # Include both late-bus variants; its major variant shares porch-pocket's loop.
    forbidden_roots = {
        loop_signature(loop) for loop in (
            ((2, 'm7'), (7, '7'), (0, 'M7'), (9, 'm7')),  # rainy-window
            ((5, 'M7'), (4, 'm7'), (2, 'm7'), (7, '7')),  # slow-room
            ((0, 'M7'), (9, 'm7'), (5, 'M7'), (7, '7')),  # porch / late-bus major
            ((0, 'm7'), (8, 'M7'), (5, 'm7'), (7, '7')),  # late-bus minor
        )
    }
    assert all(sig not in forbidden_roots for sig in signatures)
    other_signatures = {signature(s) for s in fable_sketches + opus_sketches}
    assert not set(signatures) & other_signatures
    for field in ('kicks', 'comp', 'tex_beats', 'tex_order', 'break_id'):
        assert len({s[field] for s in SKETCHES}) == 10
    print('set-check PASS tracks=10 unique_harmony=10 unique_motifs=10 kick_cells=10 comp_cells=10 texture_cells=10 breaks=10 prior_loops_avoided=yes rotation_transposition_aware=yes other_model_loops_avoided=20')


def check_prompts():
    path = Path(__file__).resolve().parents[1] / 'suno' / 'lh_astra.md'
    blocks = re.findall(r'^## (lh[^\n]+)-v1\n\*\*Style\*\*\n`([^`]+)`\n\n\*\*Description\*\*\n```\n(.*?)\n```',
                        path.read_text(), re.M | re.S)
    assert [b[0] for b in blocks] == [s['sid'] for s in SKETCHES]
    for (sid, style, description), s in zip(blocks, SKETCHES):
        assert len(style) <= 300 and len(description) <= 1000
        assert style.endswith('instrumental')
        assert s['key'] in description and f"{s['bpm']} BPM" in description
        assert 'no vocals, lo-fi warmth, DJ-friendly intro/outro' in description
        print(f'prompt-length {sid}-v1 Style={len(style)} Description={len(description)} PASS')


if __name__ == '__main__':
    check_set()
    for sketch in SKETCHES:
        result = compose(sketch['sid'])
        nt, cc, pcs, n_bars, bpm, title, sf, minor = result
        smf = build_smf(title, bpm, sf, minor, n_bars, TRACKS, pcs, nt, cc, markers(n_bars))
        check(sketch, result, smf)
        print(write_smf(os.path.join(SK_DIR, sketch['sid'] + '-v1.mid'), smf))
    check_prompts()
