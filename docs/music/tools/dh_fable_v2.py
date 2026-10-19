"""Fable v2 calibration: slot 14 `dh14-iron-tide` (Eb minor, 122) per DEEP_HOUSE_SET_BRIEF `## v2 보정`.

Kept from v1 (dh_fable.py): drums (kick/hat cycle/open-hat limit/backbeat+clap), bass cell,
chord loop (Ebm9 / Cm7b5-over-Eb, 1 bar each) and the top-then-bottom break shape.
Changed per the v2 table only:
  Keys  organ stabs lifted one octave into C4-C6, velocity 72-92, two longer stabs per bar,
        CC64 re-pedalled per bar.
  Pad   mandatory from bar 1, PC89 Classic Pad, 1+5+9 (Eb3 Bb3 F4), velocity 55-72.
  Tex   new track, PC4 Deluxe Classic EP: eighth-note chord-tone arpeggio cycling inside the
        chord's octave, velocity 55-70, A/A' only, CC64 per bar.
  Perc  new track on ch9: shaker (GM 82) sixteenths 38-52 + conga (63/64) two-bar cell, A/A' only.
  Form  intro 8 (pad + hats from bar 1, kick from bar 5), A 9-36, break 37-40, A2 41-56, outro 57-64.
"""
import os

from pipeline import BAR, PPQ, SK_DIR, bt, build_smf, hum_t, hum_v, seed, write_smf
from sketches import PC, mk_chord2
import dh_fable as v1

TRACKS = [('Drums', 9), ('Bass', 0), ('Keys', 1), ('Pad', 2), ('Tex', 3), ('Perc', 9)]
DRUMS, BASS, KEYS, PAD, TEX, PERC = range(6)
MARKERS = [(1, 'intro'), (9, 'A'), (37, 'break'), (41, 'A2'), (57, 'outro')]
N_BARS = 64
KICK_FROM, A_FROM, BREAK_FROM, A2_FROM, OUTRO_FROM = 5, 9, 37, 41, 57
KICK, SNARE, CLAP, HAT, OPEN_HAT, CRASH = v1.KICK, v1.SNARE, v1.CLAP, v1.HAT, v1.OPEN_HAT, v1.CRASH
SHAKER, CONGA_HI, CONGA_LO = 82, 63, 64
KEYS_LO, KEYS_HI = 60, 84       # C4..C6

_V1 = next(item for item in v1.SKETCHES if item['slot'] == 14)

SKETCHES = [
    dict(_V1, sid='dh14-iron-tide',
         # v1 voicings (54 58 61 65) / (54 58 60 63) lifted one octave: Ebm9 / Cm7b5 over Eb.
         loop=tuple((count, tuple(p + 12 for p in voicing)) for count, voicing in _V1['loop']),
         # Same stab positions as v1, lengths 0.3/0.25 -> 1.0/0.75 so the organ rings between kicks.
         keys=((0, 1.5, 1.0), (0, 3.0, 0.75), (1, 1.5, 1.0), (1, 3.25, 0.75)),
         key_v=82, held=True,
         pad=1, pad_pc=89, pad_v=63, pad_offsets=(12, 19, 26),      # Eb3 Bb3 F4 over root Eb2
         tex_pc=4, tex_v=61, tex_cycle=(0, 1, 2, 3, 2, 1, 0, 2),      # chord-tone index per eighth
         shaker_v=44,
         conga=(((1.5, CONGA_HI), (2.75, CONGA_HI), (3.5, CONGA_LO)),
                ((1.5, CONGA_HI), (2.5, CONGA_LO), (3.75, CONGA_LO))),
         conga_v=63),
]

FULL = frozenset({'kick', 'hats', 'back', 'bass', 'keys', 'pad', 'tex', 'perc'})


def active_parts(bar):
    """v1 'top-then-bottom' break compressed to 4 bars; intro layers in pad -> hats -> kick -> A."""
    if bar < A_FROM:
        return frozenset({'pad', 'hats'} | ({'kick'} if bar >= KICK_FROM else set()))
    if bar >= OUTRO_FROM:
        return frozenset({'kick', 'hats', 'back', 'bass'})
    if BREAK_FROM <= bar < A2_FROM:
        return frozenset({'hats', 'back', 'keys', 'pad'} if bar <= 38 else {'kick', 'bass'})
    return FULL


def chord_at(sp, bar):
    phase = (bar - A_FROM) % v1.loop_len(sp)
    for count, voicing in sp['loop']:
        if phase < count:
            return voicing
        phase -= count
    raise AssertionError('empty chord loop')


def compose(sid):
    """Return nt, cc, pcs, n_bars, bpm, title, keysig_sf, minor."""
    sp = next(item for item in SKETCHES if item['sid'] == sid)
    seed(22000 + sp['slot'])
    nt = {i: [] for i in range(len(TRACKS))}
    cc = {i: [] for i in range(len(TRACKS))}
    pcs = {DRUMS: 25, BASS: sp['bass_pc'], KEYS: sp['key_pc'], PAD: sp['pad_pc'], TEX: sp['tex_pc'],
           PERC: 25}
    root = mk_chord2(PC[sp['root']], 'm7')['bass']
    end = bt(N_BARS + 1)

    def add(track, bar, beat, length, pitch, velocity, jitter=6):
        start = max(bt(bar), min(bt(bar + 1) - 1, hum_t(bt(bar, beat), jitter)))
        stop = min(start + int(length * PPQ), bt(bar + 1) - 12, end - 12)
        if stop > start:
            nt[track].append((start, stop - start, pitch, velocity))

    def chord(bar, beat, length, voicing, velocity):
        before = len(nt[KEYS])
        add(KEYS, bar, beat, length, voicing[0], velocity)
        onset, duration, _, _ = nt[KEYS][before]
        for pitch in voicing[1:]:
            nt[KEYS].append((onset, duration, pitch, velocity))

    def pedal(track, bar, onset):
        cc[track].append((onset, 64, 100))
        cc[track].append((bt(bar + 1) - 8, 64, 0))

    for bar in range(1, N_BARS + 1):
        parts = active_parts(bar)
        # ---- drums: v1 recipe verbatim
        if 'kick' in parts:
            for beat in range(4):
                add(DRUMS, bar, beat, 0.18, KICK, hum_v(sp['kick_v'], 6), 7)
        if 'hats' in parts:
            opened = bar % sp['oh_every'] == 0
            for step in sp['hats'][(bar - 1) % len(sp['hats'])]:
                if opened and step == sp['oh_step']:
                    continue
                add(DRUMS, bar, step / 4, 0.10, HAT, hum_v(54 if step % 4 == 2 else 48, 8), 7)
            if opened:
                add(DRUMS, bar, sp['oh_step'] / 4, 0.20, OPEN_HAT, hum_v(49, 7), 7)
        if 'back' in parts:
            for beat in sp['back_beats']:
                add(DRUMS, bar, beat, 0.14, sp['back'], hum_v(77, 7), 7)
                onset, duration, _, _ = nt[DRUMS][-1]
                nt[DRUMS].append((onset, duration, CLAP, hum_v(55, 6)))
        if bar == A2_FROM:
            add(DRUMS, bar, 0, 0.50, CRASH, 65, 0)
        # ---- bass: v1 cell, degrees inside A/A', tonic at the DJ edges
        if 'bass' in parts:
            for beat, length, degree in sp['bass'][(bar - A_FROM) % len(sp['bass'])]:
                pitch = v1.sub_pitch(root, degree if bar < OUTRO_FROM else 'r')
                add(BASS, bar, beat, length, pitch, hum_v(sp['bass_v'], 5), 6)
        # ---- keys: two organ stabs per bar, C4-C6, re-pedalled per bar
        if 'keys' in parts:
            phase = (bar - A_FROM) % v1.loop_len(sp)
            first = len(nt[KEYS])
            for _, beat, length in (event for event in sp['keys'] if event[0] == phase):
                chord(bar, beat, length, chord_at(sp, bar),
                      hum_v(sp['key_v'] + (2 if bar >= A2_FROM else 0), 4))
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
                add(TEX, bar, step / 2, 0.48, voicing[index], hum_v(sp['tex_v'] + accent, 4), 5)
            pedal(TEX, bar, nt[TEX][first][0])
        # ---- perc: shaker sixteenths + two-bar conga cell
        if 'perc' in parts:
            for step in range(16):
                lift = 3 if step % 4 == 2 else 0
                add(PERC, bar, step / 4, 0.08, SHAKER, hum_v(sp['shaker_v'] + lift, 5), 7)
            for beat, pitch in sp['conga'][(bar - A_FROM) % len(sp['conga'])]:
                add(PERC, bar, beat, 0.12, pitch, hum_v(sp['conga_v'], 5), 7)
    return nt, cc, pcs, N_BARS, sp['bpm'], sp['title'], sp['sf'], True


def range_check(sp, nt, cc):
    """v2 table bounds plus the v1 drum/bass invariants that must not have moved."""
    def values(track, field, pitches=None):
        return [note[field] for note in nt[track] if pitches is None or note[2] in pitches]

    def bounds(items):
        return min(items), max(items)

    def first_bar(track, pitches=None):
        return min(t for t, _, p, _ in nt[track] if pitches is None or p in pitches) // BAR + 1

    kick, hat = bounds(values(DRUMS, 3, {KICK})), bounds(values(DRUMS, 3, {HAT}))
    back, bass = bounds(values(DRUMS, 3, {SNARE})), bounds(values(BASS, 2))
    keys, key_v = bounds(values(KEYS, 2)), bounds(values(KEYS, 3))
    pad_v, tex_v = bounds(values(PAD, 3)), bounds(values(TEX, 3))
    tex_p, shaker_v = bounds(values(TEX, 2)), bounds(values(PERC, 3, {SHAKER}))
    conga_v = bounds(values(PERC, 3, {CONGA_HI, CONGA_LO}))
    oh = sum(note[2] == OPEN_HAT for note in nt[DRUMS])
    stabs_per_bar = min(len({t for t, _, _, _ in nt[KEYS] if bt(bar) <= t < bt(bar + 1)})
                        for bar in range(A_FROM, OUTRO_FROM) if 'keys' in active_parts(bar))
    last_end = max(t + d for notes in nt.values() for t, d, _, _ in notes)
    firsts = dict(keys=first_bar(KEYS), pad=first_bar(PAD), tex=first_bar(TEX), perc=first_bar(PERC),
                  kick=first_bar(DRUMS, {KICK}), hat=first_bar(DRUMS, {HAT}), bass=first_bar(BASS))
    sustain_per_bar = all(sum(1 for t, c, v in cc[track] if c == 64 and v and bt(bar) <= t < bt(bar + 1)) == 1
                          for track, part in ((KEYS, 'keys'), (TEX, 'tex'))
                          for bar in range(1, N_BARS + 1) if part in active_parts(bar))
    checks = [78 <= kick[0] <= kick[1] <= 96, 40 <= hat[0] <= hat[1] <= 64,
              70 <= back[0] <= back[1] <= 85, v1.SUB_LO <= bass[0] <= bass[1] <= v1.SUB_HI,
              KEYS_LO <= keys[0] <= keys[1] <= KEYS_HI, 72 <= key_v[0] <= key_v[1] <= 92,
              stabs_per_bar >= 2, sustain_per_bar,
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
            f"stabs/bar>={stabs_per_bar} pad_vel={pad_v[0]}..{pad_v[1]} tex_vel={tex_v[0]}..{tex_v[1]} "
            f"tex_pitch={tex_p[0]}..{tex_p[1]} shaker_vel={shaker_v[0]}..{shaker_v[1]} "
            f"conga_vel={conga_v[0]}..{conga_v[1]} kick={kick[0]}..{kick[1]} hat={hat[0]}..{hat[1]} "
            f"bass={bass[0]}..{bass[1]} open_hat={oh} first_bar="
            + ' '.join(f"{name}={bar}" for name, bar in firsts.items())
            + f" last_note_end_bar={last_end / BAR:.3f}")


if __name__ == '__main__':
    os.makedirs(SK_DIR, exist_ok=True)
    for sketch in SKETCHES:
        nt, cc, pcs, n_bars, bpm, title, keysig_sf, minor = compose(sketch['sid'])
        line = range_check(sketch, nt, cc)
        smf = build_smf(title, bpm, keysig_sf, minor, n_bars, TRACKS, pcs, nt, cc, MARKERS)
        print(write_smf(os.path.join(SK_DIR, sketch['sid'] + '-v2.mid'), smf))
        print(line)
