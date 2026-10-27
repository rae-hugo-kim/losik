"""Ten second-pass lo-fi hip hop compositions (model fable); Python 3.9 stdlib.

Beat offsets are zero-based; MIDI programs are zero-based. Loops, kick cells,
comping, texture, motifs and breaks are checked against lh_astra.SKETCHES so
nothing from the first pass is reused.
"""
import os
import re
from collections import Counter
from pathlib import Path

from pipeline import BAR, PPQ, SK_DIR, bt, hum_t, hum_v, seed, build_smf, write_smf
from sketches import PC, mk_chord2
import lh_astra

TRACKS = [('Drums', 9), ('Bass', 0), ('Keys', 1), ('Tex', 2), ('Lead', 3)]
PAD_TRACK = ('Pad', 4)

# Chord tuples: name, root, utility quality (bass root only), four-voice jazz voicing.
SKETCHES = [
    dict(slot=2, sid='lh02-linen-afternoon', title='Linen Afternoon', bpm=76, bars=56,
         key='D minor', energy=1, sf=-1, minor=True, tonic='D', swing=30,
         keys_pc=4, tex_pc=24, lead_pc=4, opener='tex', rim=False, pad=False,
         chords=[('Dm9', 'D', 'm7', (53, 60, 64, 69)),
                 ('Am7', 'A', 'm7', (52, 57, 60, 67)),
                 ('Bbmaj7', 'Bb', 'M7', (53, 58, 62, 69)),
                 ('Gm9', 'G', 'm7', (58, 62, 65, 69))], order=(0, 1, 2, 3),
         kicks=((0, 2.5), (0, 2.5), (0, 1.75), (0, 2.5, 2.75)),
         comp=((0,), (0, 2.5), (0,), (0, 3.5)),
         melody=((69, 65, 62), (64, 67), (65, 69, 70), (67, 65)),
         lead_beats=((1, 2, 3), (0.5, 2.5), (1, 2, 3.5), (0, 2)),
         tex_beats=((1.5,), (0.5, 3), (1.5,), (2.5,)), tex_order=(2, 0, 3, 1),
         break_id='nylon-then-keys',
         notes='Natural-minor i-v-VI-iv; nylon opens alone, EP answers off the beat.'),
    dict(slot=5, sid='lh05-tin-kettle', title='Tin Kettle', bpm=80, bars=64,
         key='A minor', energy=2, sf=0, minor=True, tonic='A', swing=27,
         keys_pc=0, tex_pc=4, lead_pc=24, opener='keys', rim=False, pad=False,
         chords=[('Am9', 'A', 'm7', (55, 59, 60, 64)),
                 ('Fmaj9', 'F', 'M7', (57, 60, 64, 67)),
                 ('Cmaj9', 'C', 'M7', (55, 59, 62, 64)),
                 ('E7b9', 'E', '7', (56, 59, 62, 65))], order=(0, 1, 2, 3),
         kicks=((0, 1.5), (0, 1.5, 2.75), (0, 2.5), (0, 1.75, 2.75)),
         comp=((1.5,), (0, 2.5), (1.5,), (0, 1.5, 3)),
         melody=((64, 67, 71), (72, 69), (67, 64, 62), (68, 65)),
         lead_beats=((0, 0.5, 1.5), (0, 2), (0.5, 1.5, 2.5), (1, 2.5)),
         tex_beats=((0.5, 1.5, 2.5), (0.5,), (1.5, 3.5), (0.5, 2)), tex_order=(0, 1, 2, 3),
         break_id='hats-bass-keys',
         notes='i-VI-III-V7b9 grand piano on the and-of-two; nylon climbs a triad then settles on G#-F.'),
    dict(slot=8, sid='lh08-cedar-ledger', title='Cedar Ledger', bpm=82, bars=64,
         key='G major', energy=2, sf=1, minor=False, tonic='G', swing=29,
         keys_pc=4, tex_pc=27, lead_pc=0, opener='keys', rim=False, pad=False,
         chords=[('Gmaj9', 'G', 'M7', (59, 62, 66, 69)),
                 ('Bm7', 'B', 'm7', (57, 59, 62, 66)),
                 ('Em9', 'E', 'm7', (55, 59, 62, 66)),
                 ('Cmaj9', 'C', 'M7', (55, 59, 62, 64))], order=(0, 1, 2, 3),
         kicks=((0, 1.75, 2.5), (0, 2.75), (0, 1.75), (0, 2.5, 2.75)),
         comp=((0, 1.5), (2,), (0, 1.5), (0.5, 2.5)),
         melody=((74, 71, 69, 66), (66, 69), (71, 74, 76), (74, 71)),
         lead_beats=((0, 1, 1.5, 2.5), (0.5, 2), (0, 1.5, 3), (0.5, 2)),
         tex_beats=((0, 2.5), (1, 3.5), (0.5,), (2,)), tex_order=(1, 3, 0, 2),
         break_id='kick-bass-keys',
         notes='I-iii-vi-IV EP; grand-piano lead falls a fifth then climbs back to the ninth.'),
    dict(slot=11, sid='lh11-velvet-circuit', title='Velvet Circuit', bpm=86, bars=64,
         key='B minor', energy=3, sf=2, minor=True, tonic='B', swing=31,
         keys_pc=0, tex_pc=16, lead_pc=4, opener='keys', rim=False, pad=False,
         chords=[('Bm9', 'B', 'm7', (54, 57, 61, 62)),
                 ('Em9', 'E', 'm7', (55, 59, 62, 66)),
                 ('Gmaj9', 'G', 'M7', (54, 59, 62, 69)),
                 ('A13', 'A', '7', (55, 61, 64, 66))], order=(0, 1, 2, 3),
         kicks=((0, 1.5, 2.75), (0, 1.5, 2.5), (0, 1.75, 2.75), (0, 2.5, 2.75)),
         comp=((0.75, 2), (0, 1.5, 3), (0.75, 2), (0, 2.5, 3.5)),
         melody=((62, 66, 69, 66), (67, 66, 64, 62), (62, 66, 67, 71), (69, 67, 66)),
         lead_beats=((0, 0.5, 1, 2), (0.5, 1, 1.5, 2.5), (0, 1, 1.5, 3), (0, 1.5, 2.5)),
         tex_beats=((0,), (1.5,), (0,), (0.5,)), tex_order=(3, 2, 1, 0),
         break_id='drums-alone-then-keys',
         notes='i-iv-VI-VII13 grand piano with organ holds; EP lead folds a D-F#-A arch into a G-F# descent.'),
    dict(slot=14, sid='lh14-brass-orchard', title='Brass Orchard', bpm=88, bars=64,
         key='E major', energy=3, sf=4, minor=False, tonic='E', swing=32,
         keys_pc=4, tex_pc=24, lead_pc=24, opener='keys', rim=False, pad=False,
         chords=[('Emaj9', 'E', 'M7', (56, 59, 63, 66)),
                 ('Amaj9', 'A', 'M7', (61, 64, 68, 71)),
                 ('G#m7', 'G#', 'm7', (54, 59, 63, 68)),
                 ('C#m9', 'C#', 'm7', (52, 56, 59, 63))], order=(0, 1, 2, 3),
         kicks=((0, 1.75, 2.5), (0, 1.5, 2.75), (0, 1.5, 2.5), (0, 1.75, 2.75)),
         comp=((0, 2.75), (1.25, 3), (0, 2.75), (0.5, 1.5, 2.5)),
         melody=((68, 71, 73, 71), (69, 68, 64), (63, 66, 68), (71, 68, 66, 64)),
         lead_beats=((0.5, 1, 2, 3), (0, 1.5, 2), (0.5, 1.5, 3), (0, 1, 2, 3)),
         tex_beats=((0.5, 1.5, 3), (0, 2), (1.5, 2.5), (0.5, 3.5)), tex_order=(2, 1, 3, 0),
         break_id='keys-bass-hats-buildback',
         notes='I-IV-iii-vi EP; nylon lead rises G#-B-C# then walks down B-G#-F#-E.'),
    dict(slot=17, sid='lh17-slate-harbour', title='Slate Harbour', bpm=86, bars=64,
         key='G# minor', energy=2, sf=5, minor=True, tonic='G#', swing=28,
         keys_pc=0, tex_pc=4, lead_pc=0, opener='tex', rim=False, pad=False,
         chords=[('G#m9', 'G#', 'm7', (59, 63, 66, 70)),
                 ('Emaj7', 'E', 'M7', (52, 59, 63, 68)),
                 ('F#13', 'F#', '7', (52, 58, 61, 63)),
                 ('D#m7', 'Eb', 'm7', (54, 58, 61, 63))], order=(0, 1, 2, 3),
         kicks=((0, 1.5, 2.5), (0, 2.75), (0, 1.5, 2.5), (0, 1.75)),
         comp=((0, 1.5, 2.75), (0,), (1.75, 3), (0, 2.5)),
         melody=((66, 68, 71), (75, 71, 68), (70, 68, 66), (66, 63)),
         lead_beats=((0, 1.5, 2), (0.5, 1.5, 3), (0, 1, 2.5), (1, 2.5)),
         tex_beats=((2.5,), (0.5, 2), (3,), (1.5, 3.5)), tex_order=(3, 0, 2, 1),
         break_id='nylon-and-bass',
         notes='i-VI-VII13-v grand piano opened by a high EP; piano lead peaks on D# and sighs to F#-D#.'),
    dict(slot=20, sid='lh20-dusk-corridor', title='Dusk Corridor', bpm=82, bars=64,
         key='Eb minor', energy=2, sf=-6, minor=True, tonic='Eb', swing=26,
         keys_pc=4, tex_pc=27, lead_pc=4, opener='keys', rim=False, pad=False,
         chords=[('Ebm9', 'Eb', 'm7', (54, 58, 61, 65)),
                 ('Gbmaj9', 'F#', 'M7', (58, 61, 65, 68)),
                 ('Abm9', 'Ab', 'm7', (56, 59, 63, 66)),
                 ('Bbm7', 'Bb', 'm7', (56, 58, 61, 65))], order=(0, 1, 2, 3),
         kicks=((0, 2.5, 2.75), (0, 1.5), (0, 2.5), (0, 1.75, 2.5)),
         comp=((0.5, 2.5), (0, 3), (0.5, 2.5), (1.5,)),
         melody=((70, 66, 65), (65, 68, 70), (71, 70, 66), (68, 65, 63)),
         lead_beats=((0.5, 1.5, 2), (0, 1, 2.5), (0.5, 1, 3), (0, 1.5, 2.5)),
         tex_beats=((0.5, 2.5), (0.5, 2.5), (1, 3), (1.5,)), tex_order=(0, 2, 1, 3),
         break_id='keys-and-bass',
         notes='i-III-iv-v EP on the off-beat; EP lead drops Bb-Gb-F and climbs back through Ab-Bb.'),
    dict(slot=23, sid='lh23-honey-transit', title='Honey Transit', bpm=80, bars=64,
         key='Db major', energy=2, sf=-5, minor=False, tonic='Db', swing=30,
         keys_pc=0, tex_pc=16, lead_pc=24, opener='keys', rim=False, pad=False,
         chords=[('Dbmaj9', 'Db', 'M7', (53, 60, 63, 68)),
                 ('Ebm9', 'Eb', 'm7', (54, 58, 61, 65)),
                 ('Gbmaj7', 'F#', 'M7', (53, 58, 61, 66)),
                 ('Ab13', 'Ab', '7', (54, 60, 63, 65))], order=(0, 1, 2, 3),
         kicks=((0, 1.75), (0, 2.5, 2.75), (0, 1.5), (0, 1.5, 2.5)),
         comp=((0, 2), (0, 1.5), (0, 2), (0.5, 2.75)),
         melody=((65, 68, 72), (70, 68, 66), (65, 70, 73), (72, 70)),
         lead_beats=((0, 1, 2), (0.5, 1.5, 2.5), (0, 1.5, 3), (0.5, 2.5)),
         tex_beats=((0,), (0,), (0.5,), (0,)), tex_order=(1, 0, 3, 2),
         break_id='drums-and-nylon',
         notes='I-ii-IV-V13 grand piano with organ; nylon lead climbs F-Ab-C and answers Bb-Ab-Gb.'),
    dict(slot=26, sid='lh26-quiet-ferry', title='Quiet Ferry', bpm=76, bars=56,
         key='F minor', energy=1, sf=-4, minor=True, tonic='F', swing=25,
         keys_pc=4, tex_pc=24, lead_pc=0, opener='tex', rim=True, pad=True,
         chords=[('Fm9', 'F', 'm7', (60, 63, 67, 68)),
                 ('Bbm9', 'Bb', 'm7', (61, 65, 68, 72))], order=(0, 1, 0, 1),
         kicks=((0, 2.75), (0, 2.75), (0, 1.5), (0, 2.75)),
         comp=((0,), (0,), (0, 1.5), (0,)),
         melody=((67, 63), (60,), (65, 68), (63,)),
         lead_beats=((0, 2), (1,), (0.5, 2), (1.5,)),
         tex_beats=((1,), (2.5,), (1,), (0.5, 3)), tex_order=(2, 3, 0, 1),
         break_id='keys-and-pad',
         notes='i-iv alternating every bar over a low pad, rootless Fm9 and Bbm9 holds; grand lead sighs G-Eb, C, F-Ab, Eb.'),
    dict(slot=29, sid='lh29-cotton-ledge', title='Cotton Ledge', bpm=74, bars=56,
         key='Bb major', energy=1, sf=-2, minor=False, tonic='Bb', swing=24,
         keys_pc=0, tex_pc=4, lead_pc=24, opener='keys', rim=True, pad=False,
         chords=[('Bbmaj9', 'Bb', 'M7', (57, 60, 62, 65)),
                 ('Cm9', 'C', 'm7', (58, 62, 63, 67)),
                 ('Ebmaj9', 'Eb', 'M7', (55, 58, 62, 65))], order=(0, 0, 1, 2),
         kicks=((0, 1.5), (0, 2.75), (0, 1.5), (0, 2.5)),
         comp=((0, 2.5), (0,), (0, 2.5), (0, 3)),
         melody=((69, 72), (74,), (70, 67), (65, 67)),
         lead_beats=((0, 1.5), (0.5,), (0, 2), (1, 2.5)),
         tex_beats=((0.5, 2), (1.5,), (0.5, 2), (3,)), tex_order=(0, 3, 1, 2),
         break_id='hats-nylon-then-keys-nylon',
         notes='I-I-ii-IV grand piano with high EP; nylon lead lifts A-C, D then rests on Bb-G, F-G.'),
]


def markers(n_bars):
    return [(1, 'intro'), (9, 'A'), (25 if n_bars == 56 else 29, 'break'),
            (33 if n_bars == 56 else 37, 'A2'), (n_bars - 7, 'outro')]


def tracks_for(s):
    return TRACKS + ([PAD_TRACK] if s['pad'] else [])


def break_layers(slot, offset):
    """Eight-bar drop arrangements; the break_id names in SKETCHES describe these."""
    if slot == 2:
        return {'Tex'} | ({'Keys'} if offset >= 4 else set())
    if slot == 5:
        return {'Hats', 'Bass', 'Keys'}
    if slot == 8:
        return {'Kick', 'Bass', 'Keys'}
    if slot == 11:
        return {'Kick', 'Snare', 'Hats'} | ({'Keys'} if offset >= 4 else set())
    if slot == 14:
        return {'Keys'} | ({'Bass'} if offset >= 2 else set()) | ({'Hats'} if offset >= 4 else set())
    if slot == 17:
        return {'Tex', 'Bass'}
    if slot == 20:
        return {'Keys', 'Bass'}
    if slot == 23:
        return {'Kick', 'Snare', 'Hats', 'Tex'}
    if slot == 26:
        return {'Keys', 'Pad'}
    return ({'Hats'} if offset < 4 else {'Keys'}) | {'Tex'}


def layers_at(s, bar):
    _, _, (brk, _), (a2, _), (outro, _) = markers(s['bars'])
    if brk <= bar < a2:
        return break_layers(s['slot'], bar - brk)
    tex_open = s['opener'] == 'tex'
    layers = set()
    if bar >= (5 if tex_open else 1):
        layers.add('Keys')
    if (1 if tex_open else 9) <= bar < outro:
        layers.add('Tex')
    if bar >= 3:
        layers.add('Hats')
    if bar >= 5:
        layers.update(('Kick', 'Snare'))
    if 9 <= bar <= s['bars'] - 4:
        layers.add('Bass')
    if brk - 8 <= bar < brk or a2 <= bar < outro:
        layers.add('Lead')
    if s['pad'] and 9 <= bar < outro:
        layers.add('Pad')
    if s['energy'] == 1 and bar > s['bars'] - 4:
        layers.difference_update(('Kick', 'Snare', 'Hats'))
    return layers


def ghost_beats(energy, phase):
    if energy == 1:
        return (3.75,)
    if energy == 2:
        return (1.25, 3.75) if phase % 2 == 0 else (0.75, 3.25)
    return (0.75, 3.75)


def lead_phrase(s, phase, variant):
    """A2 variant: bar two lands an eighth late, bar four loses its last note."""
    pitches, beats = s['melody'][phase], s['lead_beats'][phase]
    if variant and phase == 1:
        beats = tuple(b + 0.5 for b in beats)
    if variant and phase == 3 and len(pitches) > 1:
        pitches, beats = pitches[:-1], beats[:-1]
    return pitches, beats


def compose(sid):
    s = next(s for s in SKETCHES if s['sid'] == sid)
    seed(261021 + s['slot'] * 97)
    n_tracks = len(tracks_for(s))
    nt, cc = {i: [] for i in range(n_tracks)}, {i: [] for i in range(n_tracks)}
    pcs = {0: 0, 1: 38 if s['energy'] == 3 else 33, 2: s['keys_pc'], 3: s['tex_pc'], 4: s['lead_pc']}
    if s['pad']:
        pcs[5] = 89
    a2 = markers(s['bars'])[3][0]
    swing = s['swing']

    def tick(bar, beat, swung=False):
        delay = swing if swung and beat % 1 == 0.5 else 0
        return hum_t(bt(bar, beat) + 14 + delay, 12)

    def velocity(base, low, high):
        return max(low, min(high, hum_v(base, 10)))

    def add(track, bar, when, duration, pitch, vel, span_bars=1):
        end = min(when + duration, bt(bar + span_bars) - 24)
        assert when >= bt(bar) and end > when
        nt[track].append((when, end - when, pitch, vel))

    for bar in range(1, s['bars'] + 1):
        phase = (bar - 1) % 4
        name, root, quality, chord = s['chords'][s['order'][phase]]
        next_root = s['chords'][s['order'][(phase + 1) % 4]][1]
        layers = layers_at(s, bar)
        occupied = set()
        cell = s['kicks'][phase]
        kick_times = [(beat, tick(bar, beat)) for beat in cell]

        def drum(beat, pitch, base, low, high, swung=False):
            slot_cell = round(beat * 4)
            assert slot_cell not in occupied
            occupied.add(slot_cell)
            when = tick(bar, beat, swung)
            add(0, bar, when, 70 if pitch != 46 else 145, pitch, velocity(base, low, high))
            return when

        if 'Kick' in layers:
            kick_base = velocity(100 + (s['energy'] - 1), 96, 104)
            for beat, when in kick_times:
                occupied.add(round(beat * 4))
                add(0, bar, when, 90, 36, kick_base + (6 if beat == 0 else 0))
        if 'Snare' in layers:
            for beat in (1, 3):
                pitch = 37 if s['rim'] and bar % 2 == 0 else 38
                drum(beat, pitch, 92 + s['energy'], 86, 100)
            for beat in ghost_beats(s['energy'], phase):
                drum(beat, 38, 45, 38, 52)
        if bar == a2:
            drum(0.25, 49, 62, 55, 70)
        if 'Hats' in layers:
            for eighth in range(8):
                beat = eighth / 2
                if round(beat * 4) in occupied:
                    continue
                offbeat = eighth % 2 == 1
                open_hat = phase == 1 and eighth == 7
                drum(beat, 46 if open_hat else 42, 76 if offbeat else 54,
                     68 if offbeat else 48, 84 if offbeat else 60, swung=offbeat)
            if s['energy'] == 3:
                drum(1.25 if phase % 2 == 0 else 3.25, 42, 45, 40, 50)
        if 'Bass' in layers:
            bass = mk_chord2(PC[root], quality)['bass']
            add(1, bar, kick_times[0][1], 900 if len(cell) == 2 else 470, bass,
                velocity(70 + s['energy'], 60, 82))
            if len(cell) == 3:
                # Three-kick bars keep one syncopation: the last on even loop bars, the first on odd.
                beat, when = kick_times[2 if phase % 2 == 0 else 1]
                if phase == 3:
                    pitch = mk_chord2(PC[next_root], 'm')['bass'] - 5
                else:
                    pitch = bass + (7 if phase == 0 else 12)
                if pitch > 48:
                    pitch -= 12
                if pitch < 28:
                    pitch += 12
                add(1, bar, when, 205, pitch, velocity(68 + s['energy'], 60, 82))
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
                        add(3, bar, when, int((3.8 - beat) * PPQ), pitch, velocity(61, 55, 72))
                else:
                    pitch = chord[s['tex_order'][(index + phase) % 4]]
                    if s['tex_pc'] == 4:
                        pitch += 12
                    add(3, bar, when, 225, pitch, velocity(63, 55, 72))
        if 'Lead' in layers:
            variant = bar >= a2 and ((bar - a2) // 4) % 2 == 1
            pitches, beats = lead_phrase(s, phase, variant)
            for index, (beat, pitch) in enumerate(zip(beats, pitches)):
                next_beat = beats[index + 1] if index + 1 < len(beats) else 4
                duration = min(440, int((next_beat - beat) * PPQ) - 48)
                add(4, bar, tick(bar, beat, swung=True), duration, pitch, velocity(70 + s['energy'], 60, 82))
        if 'Pad' in layers and phase % 2 == 0:
            low = 48 + PC[root]
            if low > 55:
                low -= 12
            when = tick(bar, 0)
            for pitch in (low, low + 7):
                add(5, bar, when, 2 * BAR, pitch, velocity(52, 45, 60), span_bars=2)
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
    expect = {0: 0, 1: 38 if s['energy'] == 3 else 33, 2: s['keys_pc'], 3: s['tex_pc'], 4: s['lead_pc']}
    if s['pad']:
        expect[5] = 89
    assert pcs == expect
    drums = nt[0]
    kick = [n for n in drums if n[2] == 36]
    back = [n for n in drums if n[2] in (37, 38) and n[3] >= 86]
    ghost = [n for n in drums if n[2] == 38 and n[3] <= 52]
    hats_on = [n for n in drums if n[2] == 42 and event_cell(n) % 4 == 0]
    hats_off = [n for n in drums if n[2] == 42 and event_cell(n) % 4 == 2]
    hats_extra = [n for n in drums if n[2] == 42 and event_cell(n) % 2 == 1]
    opened = [n for n in drums if n[2] == 46]
    pad = nt.get(5, [])
    for notes, lo, hi in ((kick, 96, 110), (back, 86, 100), (ghost, 38, 52),
                           (hats_on, 48, 60), (hats_off, 68, 84), (opened, 68, 84),
                           (hats_extra, 40, 50), (nt[1], 60, 82), (nt[2], 72, 92),
                           (nt[3], 55, 72), (nt[4], 60, 82), (pad, 45, 60)):
        assert all(lo <= n[3] <= hi for n in notes)
    assert hats_on and hats_off and all(event_cell(n) in (5, 13) for n in hats_extra)
    assert bool(hats_extra) == (s['energy'] == 3)
    assert all(28 <= n[2] <= 48 for n in nt[1])
    assert all(48 <= n[2] <= 72 for n in nt[2])
    assert all(n[2] <= 60 for n in pad)
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
        cell = s['kicks'][(bar - 1) % 4]
        in_bar = lambda ns: [n for n in ns if n[0] // BAR + 1 == bar]
        if 'Kick' in layers:
            kicks = in_bar(kick)
            assert tuple(event_cell(n) / 4 for n in kicks) == cell
            assert all(kicks[0][3] == n[3] + 6 for n in kicks[1:])
        if 'Snare' in layers:
            assert [event_cell(n) for n in in_bar(back)] == [4, 12]
            assert 1 <= len(in_bar(ghost)) <= 2
        if 'Keys' in layers:
            chord_onsets = Counter(n[0] for n in in_bar(nt[2]))
            assert 1 <= len(chord_onsets) <= 3 and set(chord_onsets.values()) == {4}
            pedal = [(t, v) for t, c, v in cc[2] if c == 64 and bt(bar) <= t < bt(bar + 1)]
            assert pedal[0][1] == 0 and pedal[-1][1] == 0 and any(v == 100 for _, v in pedal)
        if 'Bass' in layers:
            bass = in_bar(nt[1])
            assert len(cell) - len(bass) in (1, 2)
            assert all(event_cell(n) / 4 in cell for n in bass)
        for track, layer in ((1, 'Bass'), (2, 'Keys'), (3, 'Tex'), (4, 'Lead')):
            assert bool(in_bar(nt[track])) == (layer in layers)
        if s['pad']:
            assert bool([n for n in pad if n[0] <= bt(bar) + 26 and n[0] + n[1] > bt(bar)]) == ('Pad' in layers)
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
          f"tex={span([n[2] for n in nt[3]])}@{span([n[3] for n in nt[3]])} "
          f"pad={describe(pad) if pad else '-'} "
          f"lead={brk-8}-{brk-1},{a2}-{outro-1}/max={max(lead_bars.values())} "
          f"overlap={overlaps} drum_cell_collisions=0 markers={markers(n_bars)} "
          f"last_end={last_end}/{n_bars * BAR}")


def root_signature(s):
    return tuple((PC[root] - PC[s['tonic']]) % 12 for _, root, _, _ in (s['chords'][i] for i in s['order']))


def harmony_signature(s):
    return tuple(((PC[root] - PC[s['tonic']]) % 12, name[len(root):])
                 for name, root, _, _ in (s['chords'][i] for i in s['order']))


def motif_signature(s):
    pitches = [p for bar in s['melody'] for p in bar]
    return (tuple(b - a for a, b in zip(pitches, pitches[1:])), s['lead_beats'])


def check_set():
    prior = lh_astra.SKETCHES
    # Root-function sequences of rainy-window, slow-room, porch-pocket and late-bus, plus astra's ten.
    forbidden_roots = {(2, 7, 0, 9), (5, 4, 2, 7), (0, 9, 5, 7), (0, 8, 5, 7)} | {root_signature(p) for p in prior}
    assert len({harmony_signature(s) for s in SKETCHES}) == len({motif_signature(s) for s in SKETCHES}) == 10
    assert len({root_signature(s) for s in SKETCHES}) == 10
    assert all(root_signature(s) not in forbidden_roots for s in SKETCHES)
    assert not {motif_signature(s) for s in SKETCHES} & {motif_signature(p) for p in prior}
    assert not {tuple(b for bar in s['melody'] for b in bar) for s in SKETCHES} & \
        {tuple(b for bar in p['melody'] for b in bar) for p in prior}
    for field in ('kicks', 'comp', 'tex_beats', 'tex_order', 'break_id'):
        assert len({s[field] for s in SKETCHES}) == 10
    for field in ('kicks', 'comp', 'tex_beats', 'break_id'):
        assert not {s[field] for s in SKETCHES} & {p[field] for p in prior}
    neighbours = []
    for mine, theirs in ((2, 1), (11, 10), (26, 25)):
        a = next(s for s in SKETCHES if s['slot'] == mine)
        b = next(p for p in prior if p['slot'] == theirs)
        assert a['key'] == b['key']
        assert harmony_signature(a) != harmony_signature(b) and a['comp'] != b['comp'] \
            and motif_signature(a) != motif_signature(b)
        neighbours.append(f'{mine}vs{theirs}=loop/comp/motif-differ')
    print('set-check PASS tracks=10 unique_harmony=10 unique_motifs=10 kick_cells=10 comp_cells=10 '
          'texture_cells=10 breaks=10 prior_loops_avoided=yes astra_cells_avoided=yes '
          f'same_key_neighbours={",".join(neighbours)}')


def check_prompts():
    path = Path(__file__).resolve().parents[1] / 'suno' / 'lh_fable.md'
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
        smf = build_smf(title, bpm, sf, minor, n_bars, tracks_for(sketch), pcs, nt, cc, markers(n_bars))
        check(sketch, result, smf)
        print(write_smf(os.path.join(SK_DIR, sketch['sid'] + '-v1.mid'), smf))
    check_prompts()
