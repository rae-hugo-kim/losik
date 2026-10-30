"""Fable v2 layers for all ten slots (2, 5, ..., 29) per DEEP_HOUSE_SET_BRIEF `## v2 보정`.

Kept from v1 (dh_fable.py): drums (kick/hat cycle/open-hat limit/backbeat+clap), bass cell,
chord loop, swing flag and key; the ten v1 break shapes are compressed to the four v2 break bars.
Changed per the v2 table only:
  Keys  v1 voicings lifted one octave into C4-C6, velocity 72-92, every A/A2 bar either a hold
        (>= 3 beats) or at least two stabs, CC64 re-pedalled per bar.
  Pad   mandatory from bar 1, PC89 Classic Pad, 1+5+9 over the sub root, velocity 55-72.
  Tex   new track, PC4 EP (under organ/piano keys) or PC16 organ (under EP keys): eighth-note
        chord-tone arpeggio cycling inside one octave, velocity 55-70, A/A2 only, CC64 per bar.
  Perc  new track on ch9: shaker (GM 82) sixteenths 38-52 + conga (63/64) two-bar cell, A/A2 only.
  Form  intro 8 (pad + hats from bar 1, kick from bar 5), A 9-36, break 37-40, A2 41-56, outro 57-64.
        compose(sid, n_bars=96) lays the same recipe on the '## 96마디 시험판' form: A 9-48,
        break 49-56 (each two-bar v2 break stage stretched to four: 49-52 / 53-56), A2 57-88
        (crash 57), outro 89-96. Default 64 is byte-identical to the original.
Slot 14 is the listened calibration (v2 file on disk); the other nine follow the same table.
"""
import os
from collections import namedtuple

from pipeline import BAR, PPQ, SK_DIR, SW, bt, build_smf, hum_t, hum_v, seed, write_smf
from sketches import PC, mk_chord2
import dh_fable as v1

TRACKS = [('Drums', 9), ('Bass', 0), ('Keys', 1), ('Pad', 2), ('Tex', 3), ('Perc', 9)]
DRUMS, BASS, KEYS, PAD, TEX, PERC = range(6)
MARKERS = [(1, 'intro'), (9, 'A'), (37, 'break'), (41, 'A2'), (57, 'outro')]
N_BARS = 64
KICK_FROM, A_FROM, BREAK_FROM, A2_FROM, OUTRO_FROM = 5, 9, 37, 41, 57
Form = namedtuple('Form', 'n_bars break_from a2_from outro_from markers')


def form(n_bars=N_BARS):
    """Section starts for a 64-bar slot (brief form) or its 96-bar version ('## 96마디 시험판')."""
    if n_bars not in (64, 96):
        raise ValueError(f'n_bars must be 64 or 96, got {n_bars}')
    break_from, a2_from, outro_from = (BREAK_FROM, A2_FROM, OUTRO_FROM) if n_bars == 64 else (49, 57, 89)
    return Form(n_bars, break_from, a2_from, outro_from,
                [(1, 'intro'), (A_FROM, 'A'), (break_from, 'break'), (a2_from, 'A2'), (outro_from, 'outro')])


KICK, SNARE, CLAP, HAT, OPEN_HAT, CRASH = v1.KICK, v1.SNARE, v1.CLAP, v1.HAT, v1.OPEN_HAT, v1.CRASH
SHAKER, CONGA_HI, CONGA_LO = 82, 63, 64
KEYS_LO, KEYS_HI = 60, 84       # C4..C6
HOLD_BEATS = 3.0                # a single stab this long counts as a bar hold
PAD_OFFSETS = (12, 19, 26)      # 1 + 5 + 9 over the sub root
PAD_V = {1: 60, 1.5: 60, 2: 62, 2.5: 62, 3: 63}

# Per-slot v2 layer design. keys: (cycle bar, beat, beats) — every cycle bar is a hold or >= 2 stabs.
# tex_cycle: chord-tone index per eighth; slots 23/26 skip the top voice so the arpeggio stays in an
# octave. conga: two-bar cell on sixteenth slots the v1 hats leave free.
LAYERS = {
    2: dict(keys=tuple((b, 0, 3.9) for b in (0, 1, 2, 4, 5, 6))
            + ((3, 0, 3.3), (3, 3.5, 0.4), (7, 0, 3.3), (7, 3.5, 0.4)),
            key_v=76, tex_pc=16, tex_v=59, tex_cycle=(0, 2, 1, 2, 0, 2, 1, 3),
            conga=(((1.5, CONGA_HI), (3.5, CONGA_LO)), ((1.5, CONGA_HI), (2.75, CONGA_LO)))),
    5: dict(keys=((0, 0.5, 1.0), (0, 2.75, 1.0), (1, 1.5, 1.0), (1, 3.0, 0.75)),
            key_v=78, tex_pc=4, tex_v=60, tex_cycle=(0, 1, 2, 3, 3, 2, 1, 0),
            conga=(((1.5, CONGA_HI), (2.75, CONGA_LO)), ((1.5, CONGA_HI), (3.25, CONGA_LO)))),
    8: dict(keys=((0, 0, 1.75), (0, 2.0, 1.75), (1, 0.5, 1.5), (1, 2.5, 1.25),
                  (2, 0, 1.75), (2, 2.0, 1.75), (3, 0.5, 1.5), (3, 2.5, 1.25)),
            key_v=79, tex_pc=16, tex_v=60, tex_cycle=(0, 3, 1, 2, 0, 3, 1, 2),
            conga=(((1.5, CONGA_HI), (2.75, CONGA_HI), (3.5, CONGA_LO)), ((1.5, CONGA_HI), (3.5, CONGA_LO)))),
    11: dict(keys=((0, 0.5, 1.5), (0, 2.5, 1.25), (1, 0.5, 1.5), (1, 2.5, 1.25),
                   (2, 0.5, 1.5), (2, 2.5, 1.25), (3, 0.5, 3.25)),
             key_v=79, tex_pc=4, tex_v=60, tex_cycle=(3, 2, 1, 0, 1, 2, 3, 2),
             conga=(((1.5, CONGA_HI), (2.75, CONGA_LO)), ((1.5, CONGA_HI), (2.5, CONGA_LO), (3.75, CONGA_LO)))),
    14: dict(keys=((0, 1.5, 1.0), (0, 3.0, 0.75), (1, 1.5, 1.0), (1, 3.25, 0.75)),
             key_v=82, tex_pc=4, tex_v=61, tex_cycle=(0, 1, 2, 3, 2, 1, 0, 2),
             conga=(((1.5, CONGA_HI), (2.75, CONGA_HI), (3.5, CONGA_LO)),
                    ((1.5, CONGA_HI), (2.5, CONGA_LO), (3.75, CONGA_LO)))),
    17: dict(keys=((0, 0.5, 3.25), (1, 0.5, 2.75), (1, 3.5, 0.4), (2, 0.5, 3.25), (3, 0.5, 2.75), (3, 3.5, 0.4)),
             key_v=82, tex_pc=16, tex_v=62, tex_cycle=(0, 2, 3, 2, 1, 3, 2, 1),
             conga=(((1.5, CONGA_HI), (2.75, CONGA_LO)), ((1.5, CONGA_HI), (2.25, CONGA_HI), (3.5, CONGA_LO)))),
    20: dict(keys=tuple((b, 0, 3.5) for b in range(5))
             + tuple(event for b in (5, 6, 7) for event in ((b, 0, 0.75), (b, 1.0, 2.9))),
             key_v=80, tex_pc=4, tex_v=61, tex_cycle=(0, 1, 3, 1, 2, 1, 3, 1),
             conga=(((1.5, CONGA_HI), (3.5, CONGA_LO)), ((1.5, CONGA_HI), (2.75, CONGA_LO)))),
    23: dict(keys=((0, 0, 1.75), (0, 2.0, 1.9), (1, 0.5, 3.25), (2, 0, 1.75), (2, 2.0, 1.9), (3, 0.5, 3.25),
                   (4, 0, 1.75), (4, 2.0, 1.9), (5, 0.5, 3.25), (6, 0, 1.75), (6, 2.0, 1.9),
                   (7, 0.5, 2.25), (7, 3.0, 0.9)),
             key_v=78, tex_pc=16, tex_v=60, tex_cycle=(0, 1, 2, 1, 0, 2, 1, 2),
             conga=(((1.5, CONGA_HI), (3.5, CONGA_LO)), ((1.5, CONGA_HI), (2.75, CONGA_LO)))),
    26: dict(keys=tuple(event for b in range(6) for event in ((b, 1.5, 1.0), (b, 3.5, 0.45)))
             + ((6, 0.5, 1.4), (6, 2.5, 1.2), (7, 0.5, 1.4), (7, 2.5, 1.4)),
             key_v=77, tex_pc=16, tex_v=59, tex_cycle=(0, 2, 1, 2, 0, 1, 2, 1),
             conga=(((1.5, CONGA_HI), (2.75, CONGA_LO)), ((1.5, CONGA_HI),))),
    29: dict(keys=tuple((b, 0.5, 3.3) for b in range(7)) + ((7, 0, 3.75),),
             key_v=76, tex_pc=4, tex_v=59, tex_cycle=(0, 1, 0, 2, 0, 1, 0, 3),
             conga=(((1.5, CONGA_HI), (3.5, CONGA_LO)), ((2.75, CONGA_LO),))),
}


def sketch(slot):
    base = next(item for item in v1.SKETCHES if item['slot'] == slot)
    return dict(base, **LAYERS[slot],
                loop=tuple((count, tuple(p + 12 for p in voicing)) for count, voicing in base['loop']),
                pad=1, pad_pc=89, pad_v=PAD_V[base['energy']], pad_offsets=PAD_OFFSETS,
                shaker_v=44, conga_v=63)


SKETCHES = [sketch(slot) for slot in sorted(LAYERS)]

FULL = frozenset({'kick', 'hats', 'back', 'bass', 'keys', 'pad', 'tex', 'perc'})
# v1 break shapes compressed to bars 37-38 / 39-40; the pad stays wherever the top layer stays.
BREAKS = {
    'hats-then-sub': ({'hats', 'pad'}, {'hats', 'bass', 'pad'}),
    'kick-hats-keys': ({'kick', 'hats', 'keys', 'pad'}, {'kick', 'hats', 'keys', 'pad'}),
    'keys-then-sub': ({'keys', 'pad'}, {'bass'}),
    'half-kick-sub': ({'half_kick', 'bass'}, {'half_kick', 'bass'}),
    'top-then-bottom': ({'hats', 'back', 'keys', 'pad'}, {'kick', 'bass'}),
    'drone-sub-under-kit': ({'hats', 'back', 'drone', 'pad'}, {'hats', 'back', 'drone', 'pad'}),
    'rim-pad': ({'back', 'pad'}, {'back', 'pad'}),
    'hats-pad': ({'hats', 'pad'}, {'hats', 'pad'}),
    'kick-only': ({'kick'}, {'kick'}),
    'hats-rim': ({'hats', 'back', 'pad'}, {'hats', 'back', 'pad'}),
}


def active_parts(sp, bar, n_bars=N_BARS):
    """Intro layers in pad -> hats -> kick -> A; break per the slot's v1 shape (two equal halves:
    37-38 / 39-40 at 64 bars, 49-52 / 53-56 at 96); outro drums + bass."""
    fm = form(n_bars)
    if bar < A_FROM:
        return frozenset({'pad', 'hats'} | ({'kick'} if bar >= KICK_FROM else set()))
    if bar >= fm.outro_from:
        return frozenset({'kick', 'hats', 'back', 'bass'})
    if fm.break_from <= bar < fm.a2_from:
        half = fm.break_from + (fm.a2_from - fm.break_from) // 2
        return frozenset(BREAKS[sp['break_type']][0 if bar < half else 1])
    return FULL


def chord_at(sp, bar):
    phase = (bar - A_FROM) % v1.loop_len(sp)
    for count, voicing in sp['loop']:
        if phase < count:
            return voicing
        phase -= count
    raise AssertionError('empty chord loop')


def compose(sid, n_bars=N_BARS):
    """Return nt, cc, pcs, n_bars, bpm, title, keysig_sf, minor."""
    fm = form(n_bars)
    sp = next(item for item in SKETCHES if item['sid'] == sid)
    seed(22000 + sp['slot'])
    nt = {i: [] for i in range(len(TRACKS))}
    cc = {i: [] for i in range(len(TRACKS))}
    pcs = {DRUMS: 25, BASS: sp['bass_pc'], KEYS: sp['key_pc'], PAD: sp['pad_pc'], TEX: sp['tex_pc'],
           PERC: 25}
    root = mk_chord2(PC[sp['root']], 'm7')['bass']
    end = bt(n_bars + 1)

    def add(track, bar, beat, length, pitch, velocity, jitter=6, swing=False):
        start = bt(bar, beat) + (SW if swing else 0)
        start = max(bt(bar), min(bt(bar + 1) - 1, hum_t(start, jitter)))
        stop = min(start + int(length * PPQ), bt(bar + 1) - 12, end - 12)
        if stop > start:
            nt[track].append((start, stop - start, pitch, velocity))

    def swung(beat):
        return sp['swing'] and beat % 1 == 0.5

    def chord(bar, beat, length, voicing, velocity):
        before = len(nt[KEYS])
        add(KEYS, bar, beat, length, voicing[0], velocity, 6, swung(beat))
        onset, duration, _, _ = nt[KEYS][before]
        for pitch in voicing[1:]:
            nt[KEYS].append((onset, duration, pitch, velocity))

    def pedal(track, bar, onset):
        cc[track].append((onset, 64, 100))
        cc[track].append((bt(bar + 1) - 8, 64, 0))

    for bar in range(1, n_bars + 1):
        parts = active_parts(sp, bar, n_bars)
        # ---- drums: v1 recipe verbatim
        kick_beats = range(4) if 'kick' in parts else (0, 2) if 'half_kick' in parts else ()
        for beat in kick_beats:
            add(DRUMS, bar, beat, 0.18, KICK, hum_v(sp['kick_v'], 6), 7)
        if 'hats' in parts:
            opened = bar % sp['oh_every'] == 0
            for step in sp['hats'][(bar - 1) % len(sp['hats'])]:
                if opened and step == sp['oh_step']:
                    continue
                add(DRUMS, bar, step / 4, 0.10, HAT, hum_v(54 if step % 4 == 2 else 48, 8), 7,
                    sp['swing'] and step % 4 == 2)
            if opened:
                add(DRUMS, bar, sp['oh_step'] / 4, 0.20, OPEN_HAT, hum_v(49, 7), 7,
                    sp['swing'] and sp['oh_step'] % 4 == 2)
        if 'back' in parts:
            for beat in sp['back_beats']:
                add(DRUMS, bar, beat, 0.14, sp['back'], hum_v(77, 7), 7)
                onset, duration, _, _ = nt[DRUMS][-1]
                nt[DRUMS].append((onset, duration, CLAP, hum_v(55, 6)))
        if bar == fm.a2_from:
            add(DRUMS, bar, 0, 0.50, CRASH, 65, 0)
        # ---- bass: v1 cell, degrees inside A/A2, tonic at the DJ edges; drone break holds the root
        if 'drone' in parts:
            add(BASS, bar, 0, 3.9, root, hum_v(sp['bass_v'] - 4, 3), 4)
        elif 'bass' in parts:
            for beat, length, degree in sp['bass'][(bar - A_FROM) % len(sp['bass'])]:
                pitch = v1.sub_pitch(root, degree if bar < fm.outro_from else 'r')
                add(BASS, bar, beat, length, pitch, hum_v(sp['bass_v'], 5), 6, swung(beat))
        # ---- keys: hold or >= 2 stabs per bar, C4-C6, re-pedalled per bar
        if 'keys' in parts:
            phase = (bar - A_FROM) % v1.loop_len(sp)
            first = len(nt[KEYS])
            for _, beat, length in (event for event in sp['keys'] if event[0] == phase):
                chord(bar, beat, length, chord_at(sp, bar),
                      hum_v(sp['key_v'] + (2 if bar >= fm.a2_from else 0), 4))
            pedal(KEYS, bar, nt[KEYS][first][0])
        # ---- pad: 1+5+9 from bar 1
        if 'pad' in parts:
            for offset in sp['pad_offsets']:
                add(PAD, bar, 0, 3.90, root + offset, hum_v(sp['pad_v'], 5), 0)
        # ---- tex: eighth-note chord-tone arpeggio inside the chord's octave
        if 'tex' in parts:
            voicing = chord_at(sp, bar)
            first = len(nt[TEX])
            for step, index in enumerate(sp['tex_cycle']):
                accent = 4 if step % 4 == 0 else 0
                add(TEX, bar, step / 2, 0.48, voicing[index], hum_v(sp['tex_v'] + accent, 4), 5,
                    swung(step / 2))
            pedal(TEX, bar, nt[TEX][first][0])
        # ---- perc: shaker sixteenths + two-bar conga cell
        if 'perc' in parts:
            for step in range(16):
                lift = 3 if step % 4 == 2 else 0
                add(PERC, bar, step / 4, 0.08, SHAKER, hum_v(sp['shaker_v'] + lift, 5), 7)
            for beat, pitch in sp['conga'][(bar - A_FROM) % len(sp['conga'])]:
                add(PERC, bar, beat, 0.12, pitch, hum_v(sp['conga_v'], 5), 7)
    return nt, cc, pcs, n_bars, sp['bpm'], sp['title'], sp['sf'], True


def keys_bar_coverage(sp, nt):
    """Per keys bar: number of stab onsets, or 'hold' when one stab lasts >= HOLD_BEATS."""
    cover = []
    for bar in range(A_FROM, OUTRO_FROM):
        if 'keys' not in active_parts(sp, bar):
            continue
        notes = [(t, d) for t, d, _, _ in nt[KEYS] if bt(bar) <= t < bt(bar + 1)]
        onsets = len({t for t, _ in notes})
        cover.append('hold' if onsets == 1 and max(d for _, d in notes) >= HOLD_BEATS * PPQ else onsets)
    return cover


def range_check(sp, nt, cc):
    """v2 table bounds plus the v1 drum/bass invariants that must not have moved."""
    def values(track, field, pitches=None):
        return [note[field] for note in nt[track] if pitches is None or note[2] in pitches]

    def bounds(items):
        return min(items), max(items)

    def first_bar(track, pitches=None):
        return min(t for t, _, p, _ in nt[track] if pitches is None or p in pitches) // BAR + 1

    kick, hat = bounds(values(DRUMS, 3, {KICK})), bounds(values(DRUMS, 3, {HAT}))
    back, bass = bounds(values(DRUMS, 3, {sp['back']})), bounds(values(BASS, 2))
    keys, key_v = bounds(values(KEYS, 2)), bounds(values(KEYS, 3))
    pad_v, tex_v = bounds(values(PAD, 3)), bounds(values(TEX, 3))
    tex_p, shaker_v = bounds(values(TEX, 2)), bounds(values(PERC, 3, {SHAKER}))
    conga_v = bounds(values(PERC, 3, {CONGA_HI, CONGA_LO}))
    oh = sum(note[2] == OPEN_HAT for note in nt[DRUMS])
    cover = keys_bar_coverage(sp, nt)
    last_end = max(t + d for notes in nt.values() for t, d, _, _ in notes)
    firsts = dict(keys=first_bar(KEYS), pad=first_bar(PAD), tex=first_bar(TEX), perc=first_bar(PERC),
                  kick=first_bar(DRUMS, {KICK}), hat=first_bar(DRUMS, {HAT}), bass=first_bar(BASS))
    sustain_per_bar = all(sum(1 for t, c, v in cc[track] if c == 64 and v and bt(bar) <= t < bt(bar + 1)) == 1
                          for track, part in ((KEYS, 'keys'), (TEX, 'tex'))
                          for bar in range(1, N_BARS + 1) if part in active_parts(sp, bar))
    checks = [78 <= kick[0] <= kick[1] <= 96, 40 <= hat[0] <= hat[1] <= 64,
              70 <= back[0] <= back[1] <= 85, v1.SUB_LO <= bass[0] <= bass[1] <= v1.SUB_HI,
              KEYS_LO <= keys[0] <= keys[1] <= KEYS_HI, 72 <= key_v[0] <= key_v[1] <= 92,
              all(c == 'hold' or c >= 2 for c in cover), sustain_per_bar,
              55 <= pad_v[0] <= pad_v[1] <= 72, 55 <= tex_v[0] <= tex_v[1] <= 70,
              tex_p[1] - tex_p[0] <= 12, 38 <= shaker_v[0] <= shaker_v[1] <= 52,
              max(conga_v) < back[0], 12 <= oh <= 32,
              firsts['pad'] == 1 and firsts['hat'] == 1 and firsts['kick'] == KICK_FROM,
              firsts['bass'] == firsts['keys'] == firsts['tex'] == firsts['perc'] == A_FROM,
              all(bt(OUTRO_FROM) > t + d for track in (KEYS, PAD, TEX, PERC) for t, d, _, _ in nt[track]),
              all(not (bt(BREAK_FROM) <= t < bt(A2_FROM)) for track in (TEX, PERC) for t, _, _, _ in nt[track]),
              all(t < bt(OUTRO_FROM) or value == 0 for track in (KEYS, TEX) for t, control, value in cc[track]
                  if control == 64),
              [(t, p) for t, _, p, _ in nt[DRUMS] if p == CRASH] == [(bt(A2_FROM), CRASH)],
              set(values(PERC, 2)) <= {SHAKER, CONGA_HI, CONGA_LO},
              max(values(BASS, 3)) < kick[0], last_end < bt(N_BARS + 1)]
    assert all(checks), (sp['sid'], checks)
    return (f"range-check {sp['sid']} PASS keys_vel={key_v[0]}..{key_v[1]} keys_pitch={keys[0]}..{keys[1]} "
            f"keys_bars={sorted(set(map(str, cover)))} pad_vel={pad_v[0]}..{pad_v[1]} "
            f"tex_vel={tex_v[0]}..{tex_v[1]} tex_pitch={tex_p[0]}..{tex_p[1]} "
            f"shaker_vel={shaker_v[0]}..{shaker_v[1]} conga_vel={conga_v[0]}..{conga_v[1]} "
            f"kick={kick[0]}..{kick[1]} hat={hat[0]}..{hat[1]} bass={bass[0]}..{bass[1]} open_hat={oh} "
            f"first_bar=" + ' '.join(f"{name}={bar}" for name, bar in firsts.items())
            + f" last_note_end_bar={last_end / BAR:.3f}")


if __name__ == '__main__':
    os.makedirs(SK_DIR, exist_ok=True)
    for sketch_ in SKETCHES:
        nt, cc, pcs, n_bars, bpm, title, keysig_sf, minor = compose(sketch_['sid'])
        line = range_check(sketch_, nt, cc)
        smf = build_smf(title, bpm, keysig_sf, minor, n_bars, TRACKS, pcs, nt, cc, MARKERS)
        print(write_smf(os.path.join(SK_DIR, sketch_['sid'] + '-v2.mid'), smf))
        print(line)
