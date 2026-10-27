"""Fable (claude): deep house set slots 2, 5, 8, ..., 29 — ten DJ tracks.

Each slot sits between an astra slot (dh_astra.py) and an opus slot (dh_opus.py)
in the same or the neighbouring key, so each loop is a bridge: it keeps the tonic
pedal of the astra slot before it and leans toward the colour the opus slot after
it opens with. Every loop's second chord is a (interval above tonic, quality)
signature that neither astra nor opus used and that is not one of the brief's
overlap-avoid progressions; bass cells, hat cycles and break arrangements are also
checked against both earlier files in `set_check`.

Bass cells: one tuple per bar of a repeating cell, (beat, beats, degree) with
zero-based beats; degree r = root, f = fifth below, o = octave below. Chords are
explicit voicings inside C3-C5. Keys: (cycle bar, beat, beats). Hats: closed-hat
sixteenth steps per bar of a repeating cycle.
"""
import os

from pipeline import BAR, PPQ, SK_DIR, SW, bt, build_smf, hum_t, hum_v, seed, write_smf
from sketches import PC, mk_chord2

TRACKS = [('Drums', 9), ('Bass', 0), ('Keys', 1)]
MARKERS = [(1, 'intro'), (17, 'A'), (33, 'break'), (41, 'A2'), (57, 'outro')]
N_BARS = 64
KICK, RIM, SNARE, CLAP, HAT, OPEN_HAT, CRASH = 36, 37, 38, 39, 42, 46, 49
SUB_LO, SUB_HI = 28, 45          # E1..A2

SKETCHES = [
    dict(slot=2, sid='dh02-ash-corridor', title='Ash Corridor', bpm=117,
         key='A minor', sf=0, root='A', energy=1,
         notes='Am9 and a ii half-diminished over the A pedal; one hat per bar, rim on beat 3 only.',
         harmony='Am9 (4 bars) / Bm7b5/A (4 bars)', signature=(2, 'm7b5'),
         loop=((4, (52, 55, 59, 60)), (4, (53, 57, 59, 62))),
         bass=(((0, 3.0, 'r'),), ((2.0, 1.75, 'r'),)), bass_pc=38, bass_v=60,
         hats=((6,), (2, 6, 14)), oh_every=4, oh_step=14, kick_v=84,
         keys=((0, 1.5, 2.25), (2, 1.5, 2.25), (3, 3.5, 0.3),
               (4, 1.5, 2.25), (6, 1.5, 2.25), (7, 3.5, 0.3)),
         key_pc=4, key_v=54, held=True,
         back=RIM, back_beats=(3,), back_start=17, clap=False, swing=False,
         break_type='hats-then-sub', pad=None),
    dict(slot=5, sid='dh05-tin-lantern', title='Tin Lantern', bpm=119,
         key='B minor', sf=2, root='B', energy=2,
         notes='Bm9 against a lydian bIII (dorian G#) every other bar; organ dub stabs.',
         harmony='Bm9 / Dmaj7(#11)/B (1 bar each)', signature=(3, 'maj7#11'),
         loop=((1, (54, 57, 61, 62)), (1, (54, 56, 61, 62))),
         bass=(((0.5, 0.3, 'r'), (1.0, 1.4, 'r')), ((0.5, 0.3, 'r'), (1.0, 1.4, 'f'))),
         bass_pc=33, bass_v=63,
         hats=((2, 5, 6, 10, 14), (2, 6, 10, 13, 14)), oh_every=3, oh_step=6, kick_v=85,
         keys=((0, 0.5, 0.35), (0, 2.75, 0.3), (1, 1.5, 0.35)),
         key_pc=16, key_v=57, held=False,
         back=RIM, back_beats=(1, 3), back_start=9, clap=False, swing=False,
         break_type='kick-hats-keys', pad=None),
    dict(slot=8, sid='dh08-slate-hallway', title='Slate Hallway', bpm=120,
         key='F# minor', sf=3, root='F#', energy=2,
         notes='F#m9 planing up to a dorian ii11 over the F# pedal; swung hats, octave-below sub.',
         harmony='F#m9 / G#m11/F# (2 bars each)', signature=(2, 'm11'),
         loop=((2, (52, 56, 57, 61)), (2, (54, 56, 59, 63))),
         bass=(((1.5, 0.4, 'r'), (2.0, 0.4, 'r'), (3.0, 1.0, 'r')),
               ((1.5, 0.4, 'r'), (2.0, 0.4, 'r'), (3.0, 0.6, 'o'))),
         bass_pc=38, bass_v=65,
         hats=((2, 4, 6, 10, 12, 14), (2, 6, 10, 14)), oh_every=2, oh_step=10, kick_v=86,
         keys=((0, 0, 1.75), (1, 2.5, 1.25), (2, 0, 1.75), (3, 2.5, 1.25)),
         key_pc=4, key_v=58, held=True,
         back=RIM, back_beats=(1, 3), back_start=9, clap=False, swing=True,
         break_type='keys-then-sub', pad=None),
    dict(slot=11, sid='dh11-cinder-arcade', title='Cinder Arcade', bpm=121,
         key='G# minor', sf=5, root='G#', energy=2,
         notes='Three bars of G#m9 then one bar of a lydian bVI over G#; piano stabs, half-time kick break.',
         harmony='G#m9 (3 bars) / Emaj7(#11)/G# (1 bar)', signature=(8, 'maj7#11'),
         loop=((3, (54, 58, 59, 63)), (1, (52, 56, 58, 63))),
         bass=(((0, 0.4, 'r'), (0.75, 0.3, 'r'), (2.5, 1.2, 'r')),
               ((0, 0.4, 'r'), (0.75, 0.3, 'r'), (3.5, 0.4, 'r'))),
         bass_pc=33, bass_v=66,
         hats=((0, 3, 6, 8, 11, 14), (0, 3, 6, 8, 11, 13, 14)), oh_every=3, oh_step=14, kick_v=87,
         keys=((0, 2.5, 0.5), (1, 2.5, 0.5), (2, 2.5, 0.5), (3, 0.5, 2.75)),
         key_pc=0, key_v=58, held=True,
         back=RIM, back_beats=(1, 3), back_start=9, clap=False, swing=False,
         break_type='half-kick-sub', pad=None),
    dict(slot=14, sid='dh14-iron-tide', title='Iron Tide', bpm=122,
         key='Eb minor', sf=-6, root='Eb', energy=3,
         notes='Peak: Ebm9 against a dorian vi half-diminished every other bar; organ stabs, top-then-bottom break.',
         harmony='Ebm9 / Cm7b5/Eb (1 bar each)', signature=(9, 'm7b5'),
         loop=((1, (54, 58, 61, 65)), (1, (54, 58, 60, 63))),
         bass=(((0, 0.6, 'r'), (1.5, 0.4, 'r'), (2.0, 0.6, 'r'), (3.5, 0.4, 'f')),
               ((0, 0.6, 'r'), (1.5, 0.4, 'r'), (2.0, 1.4, 'r'))),
         bass_pc=38, bass_v=70,
         hats=((2, 3, 4, 6, 8, 10, 11, 12, 14), (2, 4, 6, 7, 8, 10, 12, 14, 15)),
         oh_every=2, oh_step=6, kick_v=89,
         keys=((0, 1.5, 0.3), (0, 3.0, 0.25), (1, 1.5, 0.3), (1, 3.25, 0.25)),
         key_pc=16, key_v=62, held=False,
         back=SNARE, back_beats=(1, 3), back_start=9, clap=True, swing=False,
         break_type='top-then-bottom', pad=None),
    dict(slot=17, sid='dh17-coal-harbour', title='Coal Harbour', bpm=123,
         key='F minor', sf=-4, root='F', energy=3,
         notes='Peak: Fm9 and a dorian bVII major seventh over F; all-offbeat sub, drone-sub break.',
         harmony='Fm9 / Ebmaj7/F (2 bars each)', signature=(10, 'maj7'),
         loop=((2, (56, 60, 63, 67)), (2, (55, 58, 62, 63))),
         bass=(((0.5, 0.4, 'r'), (1.5, 0.4, 'r'), (2.5, 0.4, 'r'), (3.5, 0.4, 'r')),
               ((0.5, 0.4, 'r'), (1.5, 0.4, 'r'), (2.5, 1.4, 'f'))),
         bass_pc=38, bass_v=71,
         hats=((1, 2, 4, 6, 8, 9, 10, 12, 14), (2, 4, 6, 8, 10, 12, 14)),
         oh_every=2, oh_step=14, kick_v=90,
         keys=((0, 0.5, 3.25), (1, 3.5, 0.35), (2, 0.5, 3.25), (3, 3.5, 0.35)),
         key_pc=4, key_v=62, held=True,
         back=SNARE, back_beats=(1, 3), back_start=9, clap=False, swing=False,
         break_type='drone-sub-under-kit', pad=None),
    dict(slot=20, sid='dh20-wet-granite', title='Wet Granite', bpm=122,
         key='C minor', sf=-3, root='C', energy=2.5,
         notes='Peak ends: five bars of Cm9 then three of an aeolian bVI major seventh; pad from the break.',
         harmony='Cm9 (5 bars) / Abmaj7/C (3 bars)', signature=(8, 'maj7'),
         loop=((5, (51, 55, 58, 62)), (3, (51, 55, 56, 60))),
         bass=(((0, 1.5, 'r'), (2.5, 0.4, 'r'), (3.0, 0.9, 'r')),
               ((0, 1.5, 'r'), (3.0, 0.9, 'f'))),
         bass_pc=33, bass_v=68,
         hats=((2, 6, 9, 10, 13, 14), (2, 6, 10, 14)), oh_every=3, oh_step=10, kick_v=88,
         keys=((0, 0, 3.5), (2, 0, 3.5), (4, 0, 3.5), (5, 1.0, 2.75), (7, 1.0, 2.75)),
         key_pc=0, key_v=60, held=True,
         back=RIM, back_beats=(1, 3), back_start=9, clap=False, swing=False,
         break_type='rim-pad', pad=33),
    dict(slot=23, sid='dh23-paper-lantern', title='Paper Lantern', bpm=120,
         key='D minor', sf=-1, root='D', energy=2,
         notes='Drift: Dm9 opening into a bIII major ninth over D; pad from 17, swung hats, hats-and-pad break.',
         harmony='Dm9 / Fmaj9/D (4 bars each)', signature=(3, 'maj9'),
         loop=((4, (53, 57, 60, 64)), (4, (52, 55, 60, 65))),
         bass=(((1.0, 0.75, 'r'), (2.5, 1.4, 'r')), ((1.0, 0.75, 'r'), (3.5, 0.4, 'f'))),
         bass_pc=38, bass_v=64,
         hats=((2, 6, 10, 12, 14), (2, 4, 6, 10, 14)), oh_every=4, oh_step=6, kick_v=86,
         keys=((0, 2.0, 1.9), (1, 0.5, 3.25), (4, 2.0, 1.9), (5, 0.5, 3.25), (7, 3.0, 0.9)),
         key_pc=4, key_v=57, held=True,
         back=RIM, back_beats=(1, 3), back_start=9, clap=False, swing=True,
         break_type='hats-pad', pad=17),
    dict(slot=26, sid='dh26-dusk-ledger', title='Dusk Ledger', bpm=119,
         key='A minor', sf=0, root='A', energy=1.5,
         notes='Six bars of Am9 then two of a bIII six-nine over A; four-bar sub cell with a rest, kick-only break.',
         harmony='Am9 (6 bars) / C6/9/A (2 bars)', signature=(3, '6/9'),
         loop=((6, (52, 59, 60, 67)), (2, (52, 57, 62, 67))),
         bass=(((0, 1.0, 'r'), (3.5, 0.4, 'r')), ((2.5, 1.4, 'r'),),
               ((0, 1.0, 'r'), (3.5, 0.4, 'r')), ()),
         bass_pc=33, bass_v=62,
         hats=((6, 10), (2, 6, 10, 14)), oh_every=4, oh_step=10, kick_v=85,
         keys=((0, 3.5, 0.4), (2, 1.5, 0.4), (4, 3.5, 0.4), (6, 0.5, 1.4), (7, 2.5, 1.2)),
         key_pc=4, key_v=55, held=False,
         back=RIM, back_beats=(1, 3), back_start=13, clap=False, swing=False,
         break_type='kick-only', pad=None),
    dict(slot=29, sid='dh29-last-corridor', title='Last Corridor', bpm=117,
         key='A minor', sf=0, root='A', energy=1,
         notes='Seven bars of an Am11 shell then one bar of a rootless v11 with the dorian F#; hats-and-rim break.',
         harmony='Am11 (7 bars) / Em11/A (1 bar)', signature=(7, 'm11'),
         loop=((7, (55, 60, 62, 64)), (1, (55, 57, 62, 66))),
         bass=(((0, 3.9, 'r'),), ((0, 1.5, 'r'),), (), ((2.0, 1.9, 'r'),)),
         bass_pc=38, bass_v=59,
         hats=((10,), (6, 10)), oh_every=4, oh_step=14, kick_v=84,
         keys=((0, 0.5, 3.0), (4, 0.5, 3.0), (7, 0, 3.75)),
         key_pc=0, key_v=54, held=True,
         back=RIM, back_beats=(3,), back_start=17, clap=False, swing=False,
         break_type='hats-rim', pad=None),
]

FULL = frozenset({'kick', 'hats', 'back', 'bass', 'keys', 'pad'})


def active_parts(sp, bar):
    """Parts sounding in `bar`; the ten break arrangements are all explicit here."""
    if not 33 <= bar <= 40:
        return FULL
    kind, first_half = sp['break_type'], bar <= 36
    if kind == 'hats-then-sub':
        return frozenset({'hats'} if first_half else {'hats', 'bass'})
    if kind == 'kick-hats-keys':
        return frozenset({'kick', 'hats', 'keys'})
    if kind == 'keys-then-sub':
        return frozenset({'keys'} if first_half else {'bass'})
    if kind == 'half-kick-sub':
        return frozenset({'half_kick', 'bass'})
    if kind == 'top-then-bottom':
        return frozenset({'hats', 'back', 'keys'} if first_half else {'kick', 'bass'})
    if kind == 'drone-sub-under-kit':
        return frozenset({'hats', 'back', 'drone'})
    if kind == 'rim-pad':
        return frozenset({'back', 'pad'})
    if kind == 'hats-pad':
        return frozenset({'hats', 'pad'})
    if kind == 'kick-only':
        return frozenset({'kick'})
    if kind == 'hats-rim':
        return frozenset({'hats', 'back'})
    raise ValueError(kind)


def loop_len(sp):
    return sum(count for count, _ in sp['loop'])


def chord_at(sp, bar):
    phase = (bar - 17) % loop_len(sp)
    for count, voicing in sp['loop']:
        if phase < count:
            return voicing
        phase -= count
    raise AssertionError('empty chord loop')


def sub_pitch(root, degree):
    pitch = {'r': root, 'f': root - 7, 'o': root - 12}[degree]
    assert SUB_LO <= pitch <= SUB_HI, (root, degree, pitch)
    return pitch


def compose(sid):
    """Return nt, cc, pcs, n_bars, bpm, title, keysig_sf, minor."""
    sp = next(item for item in SKETCHES if item['sid'] == sid)
    seed(21000 + sp['slot'])
    count = 4 if sp['pad'] else 3
    nt = {i: [] for i in range(count)}
    cc = {i: [] for i in range(count)}
    pcs = {0: 25, 1: sp['bass_pc'], 2: sp['key_pc']}
    if sp['pad']:
        pcs[3] = 89
    root = mk_chord2(PC[sp['root']], 'm7')['bass']
    end = bt(N_BARS + 1)

    def add(track, bar, beat, length, pitch, velocity, jitter=6, swing=False):
        start = bt(bar, beat) + (SW if swing else 0)
        start = max(bt(bar), min(bt(bar + 1) - 1, hum_t(start, jitter)))
        stop = min(start + int(length * PPQ), bt(bar + 1) - 12, end - 12)
        if stop > start:
            nt[track].append((start, stop - start, pitch, velocity))

    def swung(beat):
        return sp['swing'] and beat % 1 == 0.5

    def chord(bar, beat, length, voicing, velocity):
        before = len(nt[2])
        add(2, bar, beat, length, voicing[0], velocity, 6, swung(beat))
        onset, duration, _, _ = nt[2][before]
        for pitch in voicing[1:]:
            nt[2].append((onset, duration, pitch, velocity))
        if sp['held'] and length > 0.75:
            cc[2].append((onset, 64, 100))
            cc[2].append((onset + duration, 64, 0))

    for bar in range(1, N_BARS + 1):
        parts = active_parts(sp, bar)
        kick_beats = range(4) if 'kick' in parts else (0, 2) if 'half_kick' in parts else ()
        for beat in kick_beats:
            add(0, bar, beat, 0.18, KICK, hum_v(sp['kick_v'], 6), 7)
        if 'hats' in parts:
            opened = bar % sp['oh_every'] == 0
            for step in sp['hats'][(bar - 1) % len(sp['hats'])]:
                if opened and step == sp['oh_step']:
                    continue
                add(0, bar, step / 4, 0.10, HAT, hum_v(54 if step % 4 == 2 else 48, 8), 7,
                    sp['swing'] and step % 4 == 2)
            if opened:
                add(0, bar, sp['oh_step'] / 4, 0.20, OPEN_HAT, hum_v(49, 7), 7,
                    sp['swing'] and sp['oh_step'] % 4 == 2)
        if 'back' in parts and bar >= sp['back_start']:
            for beat in sp['back_beats']:
                add(0, bar, beat, 0.14, sp['back'], hum_v(77, 7), 7)
                if sp['clap']:
                    onset, duration, _, _ = nt[0][-1]
                    nt[0].append((onset, duration, CLAP, hum_v(55, 6)))
        if bar == 41:
            add(0, bar, 0, 0.50, CRASH, 65, 0)
        if 'drone' in parts:
            add(1, bar, 0, 3.9, root, hum_v(sp['bass_v'] - 4, 3), 4)
        elif 'bass' in parts and bar >= 9:
            for beat, length, degree in sp['bass'][(bar - 9) % len(sp['bass'])]:
                # DJ edges stay on the tonic so neighbouring tracks mix cleanly.
                pitch = sub_pitch(root, degree if 17 <= bar <= 56 else 'r')
                add(1, bar, beat, length, pitch, hum_v(sp['bass_v'], 5), 6, swung(beat))
        if 'keys' in parts and 12 <= bar <= 56:
            if bar in (12, 14):
                chord(bar, 2.5 if bar == 12 else 0.5, 0.3, sp['loop'][0][1], hum_v(52, 2))
            elif bar >= 17:
                phase = (bar - 17) % loop_len(sp)
                for _, beat, length in (event for event in sp['keys'] if event[0] == phase):
                    chord(bar, beat, length, chord_at(sp, bar),
                          hum_v(sp['key_v'] + (2 if bar >= 41 else 0), 4))
        cc[2].append((bt(bar + 1) - 8, 64, 0))
        if sp['pad'] and 'pad' in parts and sp['pad'] <= bar <= 56:
            for pitch in (root + 7, root + 12):
                add(3, bar, 0, 3.90, pitch, hum_v(41, 5), 0)
    return nt, cc, pcs, N_BARS, sp['bpm'], sp['title'], sp['sf'], True


def range_check(sp, nt, cc):
    """Measure the emitted notes against the brief's recipe; bar-end values count elapsed bars."""
    def values(track, field, pitches=None):
        return [note[field] for note in nt[track] if pitches is None or note[2] in pitches]

    def bounds(items):
        return min(items), max(items)

    kick = bounds(values(0, 3, {KICK}))
    hat = bounds(values(0, 3, {HAT}))
    back = bounds(values(0, 3, {RIM, SNARE}))
    bass = bounds(values(1, 2))
    keys = bounds(values(2, 2))
    key_v = bounds(values(2, 3))
    oh = sum(note[2] == OPEN_HAT for note in nt[0])
    last_chord = max(t + d - 1 for t, d, _, _ in nt[2]) // BAR + 1
    last_end = max(t + d for notes in nt.values() for t, d, _, _ in notes)
    clap = values(0, 3, {CLAP})
    snare_onsets = {t for t, _, pitch, _ in nt[0] if pitch == SNARE}
    intro_drums = {pitch for t, _, pitch, _ in nt[0] if t < bt(9)}
    checks = [78 <= kick[0] <= kick[1] <= 96, 40 <= hat[0] <= hat[1] <= 64,
              70 <= back[0] <= back[1] <= 85, SUB_LO <= bass[0] <= bass[1] <= SUB_HI,
              48 <= keys[0] <= keys[1] <= 72, 50 <= key_v[0] <= key_v[1] <= 70,
              12 <= oh <= 32, last_chord <= 56, last_end < bt(N_BARS + 1),
              max(values(1, 3)) < kick[0],
              not clap or max(clap) < back[0],
              all(t in snare_onsets for t, _, pitch, _ in nt[0] if pitch == CLAP),
              [(t, p) for t, _, p, _ in nt[0] if p == CRASH] == [(bt(41), CRASH)],
              min(t for t, _, _, _ in nt[1]) >= bt(9),
              min(t for t, _, _, _ in nt[2]) >= bt(12),
              intro_drums <= {KICK, HAT, OPEN_HAT},
              all(t < bt(57) or value == 0 for t, control, value in cc[2] if control == 64)]
    if sp['pad']:
        checks.extend((35 <= min(values(3, 3)) <= max(values(3, 3)) <= 50,
                       max(t + d for t, d, _, _ in nt[3]) < bt(57)))
    assert all(checks), (sp['sid'], checks)
    return (f"range-check {sp['sid']} PASS kick={kick[0]}..{kick[1]} "
            f"hat={hat[0]}..{hat[1]} backbeat={back[0]}..{back[1]} "
            f"bass={bass[0]}..{bass[1]} keys={keys[0]}..{keys[1]} "
            f"key_vel={key_v[0]}..{key_v[1]} open_hat={oh} "
            f"last_chord_bar={last_chord} last_note_end_bar={last_end / BAR:.3f}")


# ---------------------------------------------------------------- set-level uniqueness
BRIEF_SIGNATURES = {(5, 'm9'), (5, '9'), (8, 'maj9'), (10, 'maj9'), (7, 'm7'), (7, '7b9')}


def _astra_cell(cell):
    return tuple(tuple((beat, length, 'f' if offset == -7 else 'r') for beat, length, offset in bar)
                 for bar in cell)


def _opus_cell(cell):
    return tuple(tuple((beat, length, degree) for beat, length, degree, _ in bar) for bar in cell)


def _opus_parts(sp, bar):
    parts = {'kick', 'back', 'hats', 'bass', 'keys', 'pad'}
    for lo, hi, dropped in sp['drops']:
        if lo <= bar <= hi:
            parts -= dropped
            if 'kick_one' in dropped or 'kick_broken' in dropped:
                parts.discard('kick')
                parts.add('kick_one' if 'kick_one' in dropped else 'half_kick')
    return frozenset(parts)


def break_shape(parts_fn):
    return tuple(parts_fn(bar) for bar in range(33, 41))


def set_check():
    import dh_astra
    import dh_opus
    signatures = [sp['signature'] for sp in SKETCHES]
    taken = {sp['signature'] for sp in dh_astra.SKETCHES} | {sp['sig'] for sp in dh_opus.SKETCHES}
    taken |= BRIEF_SIGNATURES
    assert len(set(signatures)) == 10 and not set(signatures) & taken, signatures
    voicings = [tuple(v for _, v in sp['loop']) for sp in SKETCHES]
    other_voicings = {tuple(v for _, v in sp['loop']) for sp in dh_astra.SKETCHES}
    other_voicings |= {tuple(tuple(c['v']) for c, _ in sp['loop']) for sp in dh_opus.SKETCHES}
    assert len(set(voicings)) == 10 and not set(voicings) & other_voicings
    cells = [sp['bass'] for sp in SKETCHES]
    other_cells = {_astra_cell(sp['bass']) for sp in dh_astra.SKETCHES}
    other_cells |= {_opus_cell(sp['bass']) for sp in dh_opus.SKETCHES}
    assert len(set(cells)) == 10 and not set(cells) & other_cells
    hats = [sp['hats'] for sp in SKETCHES]
    other_hats = {sp['hats'] for sp in dh_astra.SKETCHES}
    other_hats |= {(tuple(step for step, _ in sp['hats']),) for sp in dh_opus.SKETCHES}
    assert len(set(hats)) == 10 and not set(hats) & other_hats
    breaks = [break_shape(lambda bar, sp=sp: active_parts(sp, bar)) for sp in SKETCHES]
    other_breaks = {break_shape(lambda bar, sp=sp: frozenset(dh_astra.active_parts(sp, bar)))
                    for sp in dh_astra.SKETCHES}
    other_breaks |= {break_shape(lambda bar, sp=sp: _opus_parts(sp, bar)) for sp in dh_opus.SKETCHES}
    assert len(set(breaks)) == 10 and not set(breaks) & other_breaks
    assert len({sp['break_type'] for sp in SKETCHES}) == 10
    return ('set-check PASS slots=10 unique_signatures=10 unique_voicings=10 unique_bass_cells=10 '
            'unique_hat_cycles=10 unique_breaks=10 astra_overlap=0 opus_overlap=0 brief_overlap=0')


if __name__ == '__main__':
    os.makedirs(SK_DIR, exist_ok=True)
    for sketch in SKETCHES:
        nt, cc, pcs, n_bars, bpm, title, keysig_sf, minor = compose(sketch['sid'])
        line = range_check(sketch, nt, cc)
        tracks = TRACKS + ([('Pad', 2)] if sketch['pad'] else [])
        smf = build_smf(title, bpm, keysig_sf, minor, n_bars, tracks, pcs, nt, cc, MARKERS)
        print(write_smf(os.path.join(SK_DIR, sketch['sid'] + '-v1.mid'), smf))
        print(line)
    print(set_check())
