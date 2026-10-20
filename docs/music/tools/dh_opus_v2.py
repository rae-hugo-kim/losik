"""Opus (claude): v2 harmonic/texture layers for the ten opus slots (3, 6, ..., 30).

Per docs/music/DEEP_HOUSE_SET_BRIEF.md '## v2 보정' (first calibrated on slot 15), generalised
to all ten slots for '## v3 롤아웃'. Drums, bass cell, chord loop, key and break survivors
come from dh_opus.py (v1). What changes:
- Keys (v1 patch): the v1 voicings one octave up (inside C4-C6), velocity 72-92, every bar
  either held through or hit at least twice; CC64 catch / bar re-pedal / release kept.
- Pad (PC89 Classic Pad or PC90): from bar 1, velocity 55-72, three voices per loop chord
  (root, fifth, ninth; the half-diminished chords take their own flat fifth / seventh);
  tonic-only in the intro and the closer's outro tail, follows the loop from bar 9.
- Tex (PC16 organ, or PC4 EP where the keys are the organ/piano): eighth-note chord-tone
  arpeggio cycling three or four tones inside one octave, moving the loop's own moving
  voice, velocity 55-70, A from bar 17 and A2 only.
- Perc (drum ch9, own track): sixteenth shaker (GM 82) 38-52 from bar 9 plus a two-bar conga
  cell (GM 63/64) from bar 13, A and A2 only (v3 replaces this track).
- Structure: intro 8 (pad + hats from 1, kick from 5), A 9-36, break 37-40 (the slot's v1
  break compressed to four bars, same survivors), A2 41-56 (crash on 41), outro 57-end
  (drums + bass). Pad and keys end with bar 56; the closer (72 bars) keeps a four-bar tonic
  pad tail into its 16-bar outro and its v1 outro thinning (61-72).
"""
import os

from pipeline import BAR, PPQ, SK_DIR, SW, bt, hum_t, hum_v, seed
from pipeline import build_smf, write_smf
import dh_opus
from dh_opus import BACK, CLAP, CRASH, HAT, KICK, OHAT, RIM, S16, SNARE, clamp, m

TRACKS = [('Drums', 9), ('Bass', 0), ('Keys', 1), ('Pad', 2), ('Tex', 3), ('Perc', 9)]
MARKERS = [(1, 'intro'), (9, 'A'), (37, 'break'), (41, 'A2'), (57, 'outro')]
SHAKER, CONGA_HI, CONGA_LO = 82, 63, 64
KEYS_FROM, KEYS_LAST = 9, 56     # keys, tex and perc stop before the outro (bar 57)
TEX_FROM, SHAKER_FROM, CONGA_FROM = 17, 9, 13
PAD_VEL = {'intro_lo': 58, 'intro': 62, 'A': 66, 'break': 70, 'A2': 68, 'outro': 58}
SHAKER_ACC = {0: 40, 1: 38, 2: 50, 3: 40}
CONGA_V2 = [[(3, CONGA_HI, 60), (6, CONGA_LO, 56), (11, CONGA_HI, 54)],
            [(6, CONGA_LO, 58), (10, CONGA_HI, 52), (13, CONGA_HI, 50), (14, CONGA_LO, 56)]]
INTRO_KICK = (1, 4, {'kick'})    # kick enters on bar 5

V1 = {s['slot']: s for s in dh_opus.SKETCHES}


def v2(slot, **kw):
    sp = dict(V1[slot], keys_up=12, pad_last=56)
    sp.update(kw)
    return sp


# keys: (bar_in_cycle, beat, length_beats, velocity); chord = the one in force half a beat
#   after the attack (as v1).
# pad: three note names per loop chord. tex: tone cycle per loop chord, one octave span.
# drops: v2 structure — intro kick from 5, v1 break survivors inside 37-40.
SKETCHES = [
    v2(3, pcs=(25, 38, 4, 89, 16, 25),
       keys=[(k, b, d, v) for k in (0, 2)
             for b, d, v in ((0, 1.3, 78), (1.5, 4.3, 84))]
       + [(k, 2.5, 1.3, 76) for k in (1, 3)],
       pad=[['E3', 'B3', 'F#4'], ['A2', 'E3', 'B3']],
       tex=[['G4', 'B4', 'D5'], ['G4', 'A4', 'D5']],
       drops=[INTRO_KICK, (37, 40, {'kick_one', 'bass'})],
       break_txt='37–40 킥 1박만 + 베이스 아웃(햇·백비트·EP·패드 유지)'),
    v2(6, pcs=(25, 38, 16, 89, 4, 25),
       keys=[(k, b, d, v) for k in range(4) for b, d, v in ((0, 2.6, 84), (3.0, .9, 78))],
       pad=[['B2', 'F#3', 'C#4'], ['G2', 'D3', 'A3']],
       tex=[['D4', 'F#4', 'A4', 'C#5'], ['D4', 'F4', 'A4', 'B4']],
       drops=[INTRO_KICK, (37, 40, {'bass', 'keys', 'pad'})],
       break_txt='37–40 드럼만(베이스·오르간·패드 아웃)'),
    v2(9, pcs=(25, 33, 4, 89, 16, 25),
       keys=[(k, b, d, v) for k in (0, 2) for b, d, v in ((1.0, 2.4, 84), (3.5, .5, 74))]
       + [(k, b, d, v) for k in (1, 3) for b, d, v in ((1.0, 2.0, 80), (3.5, .45, 78))],
       pad=[['C#3', 'G#3', 'D#4'], ['G#2', 'D3', 'F#3']],
       tex=[['G#4', 'B4', 'D#5'], ['G#4', 'B4', 'D5']],
       drops=[INTRO_KICK, (37, 37, {'kick', 'back', 'hats', 'bass'}),
              (38, 38, {'kick', 'back', 'bass'}), (39, 39, {'kick', 'back'}), (40, 40, {'back'})],
       break_txt='4단 가산, 마디당 1단: 37 EP+패드 → 38 +햇 → 39 +베이스 → 40 +킥'),
    v2(12, pcs=(25, 38, 4, 89, 16, 25),
       keys=[(k, b, d, v) for k in range(4) for b, d, v in ((2.0, 1.2, 84), (3.5, 1.9, 80))],
       pad=[['G#2', 'D#3', 'A#3'], ['B2', 'F#3', 'C#4']],
       tex=[['F#4', 'A#4', 'B4', 'D#5'], ['F#4', 'A4', 'B4', 'D#5']],
       drops=[INTRO_KICK, (37, 40, {'kick_broken'})],
       break_txt='37–40 브로큰 킥 2-스텝, 나머지 유지'),
    v2(15, pcs=(25, 38, 4, 89, 16, 25),
       # v1's e-of-1 stab, then a hold
       keys=[(0, .75, .65, 86), (0, 1.5, 2.3, 80),
             (1, .75, 2.3, 84), (1, 3.25, .65, 76),
             (2, .75, .65, 86), (2, 1.5, 2.3, 80),
             (3, .75, 2.3, 84), (3, 3.25, .65, 76)],
       pad=[['Bb2', 'F3', 'C4'], ['Ab2', 'Eb3', 'Bb3']],
       tex=[['F4', 'Ab4', 'Db5'], ['Gb4', 'Ab4', 'Db5']],
       drops=[INTRO_KICK, (37, 38, {'hats'}), (39, 39, {'hats', 'bass'}),
              (40, 40, {'hats', 'bass', 'kick'})],
       break_txt='4마디 3단 감산: 37–38 햇 아웃 → 39 +베이스 아웃 → 40 +킥 아웃(스네어·EP·패드만)'),
    v2(18, pcs=(25, 38, 16, 89, 4, 25),
       keys=[(k, b, d, v) for k in (0, 2) for b, d, v in ((1.5, 2.0, 84), (3.5, .4, 76))]
       + [(k, b, d, v) for k in (1, 3) for b, d, v in ((0, 1.0, 78), (1.5, 2.3, 82))],
       pad=[['F3', 'C4', 'G4'], ['Gb3', 'Db4', 'Ab4']],
       tex=[['Ab4', 'C5', 'Eb5', 'G5'], ['Ab4', 'Bb4', 'Db5', 'Fb5']],
       drops=[INTRO_KICK, (37, 38, {'bass'}), (39, 40, {'kick', 'back', 'hats', 'bass', 'pad'})],
       break_txt='37–38 베이스 아웃 → 39–40 드럼·베이스·패드 멈추고 오르간만'),
    v2(21, pcs=(25, 38, 4, 90, 16, 25), pad_lift=3,
       keys=[(k, 0, 3.85, 86 if k % 2 == 0 else 80) for k in range(4)],
       pad=[['G2', 'D3', 'A3'], ['Db3', 'Ab3', 'Eb4']],
       tex=[['F4', 'A4', 'D5'], ['F4', 'Ab4', 'Eb5']],
       drops=[INTRO_KICK, (37, 40, {'kick', 'back', 'hats', 'keys'})],
       break_txt='37–40 서브+패드만(드럼·EP 아웃)'),
    v2(24, pcs=(25, 33, 0, 90, 16, 25),
       keys=[(k, b, d, v) for k in (0, 2) for b, d, v in ((0, 1.8, 80), (2.0, 5.8, 86))],
       pad=[['D3', 'A3', 'E4'], ['D3', 'Ab3', 'E4']],
       tex=[['F4', 'A4', 'C5'], ['F4', 'Ab4', 'C5']],
       drops=[INTRO_KICK, (37, 40, {'hats', 'back', 'keys', 'pad'})],
       break_txt='37–40 킥+서브만(햇·백비트·피아노·패드 아웃)'),
    v2(27, pcs=(25, 38, 4, 90, 16, 25),
       keys=[(k, 0, 3.8, 82) for k in (0, 2)]
       + [(k, b, d, v) for k in (1, 3) for b, d, v in ((0, 1.8, 76), (2.0, 1.8, 74))],
       pad=[['D3', 'A3', 'E4'], ['F2', 'C3', 'G3']],
       tex=[['F4', 'A4', 'C5'], ['F4', 'G4', 'C5']],
       drops=[INTRO_KICK, (37, 40, {'kick', 'hats', 'bass', 'pad'})],
       break_txt='37–40 백비트+EP만(킥·햇·베이스·패드 아웃)'),
    v2(30, pcs=(25, 38, 0, 90, 4, 25), pad_last=60,
       keys=[(k, .5, 3.3, 84) for k in (0, 2)]
       + [(k, b, d, v) for k in (1, 3) for b, d, v in ((0, 2.3, 78), (2.5, 1.3, 76))],
       pad=[['A2', 'E3', 'B3'], ['E2', 'B2', 'F#3']],
       tex=[['E4', 'G4', 'B4'], ['E4', 'F#4', 'B4']],
       drops=[INTRO_KICK, (37, 40, {'kick', 'back', 'bass'}),
              (61, 64, {'back'}), (65, 68, {'back', 'hats'}),
              (69, 71, {'back', 'hats', 'bass'}), (72, 72, {'back', 'hats', 'bass', 'kick_one'})],
       break_txt='37–40 햇+피아노+패드(킥·백비트·베이스 아웃); 아웃트로 61 백비트 → 65 햇 → '
                 '69 베이스 아웃 → 72 1박 킥 하나'),
]


def section(b):
    return ('intro' if b <= 8 else 'A' if b <= 36 else 'break' if b <= 40
            else 'A2' if b <= 56 else 'outro')


def dropped(sp, b, part):
    return any(lo <= b <= hi and part in parts for lo, hi, parts in sp['drops'])


def compose(sid):
    """Return nt, cc, pcs, n_bars, bpm, title, keysig_sf, minor."""
    sp = next((s for s in SKETCHES if s['sid'] == sid), None)
    if sp is None:
        raise ValueError('Unknown sketch: ' + sid)
    n_bars = sp['n_bars']
    end = n_bars * BAR
    pad_last = sp['pad_last']
    nt = {i: [] for i in range(len(TRACKS))}
    cc = {i: [] for i in range(len(TRACKS))}
    pcs = {i: sp['pcs'][i] for i in range(len(TRACKS))}
    cc[2].append((0, 64, 0))
    loop = sp['loop']
    cycle = sum(n for _, n in loop)
    starts, acc = [], 0
    for _, n in loop:
        starts.append(acc)
        acc += n
    tonic = loop[0][0]
    base = sp['slot'] * 100000 + 31          # same seeds as v1: drums/bass humanize identically
    tex_tones = [[m(n) for n in tones] for tones in sp['tex']]
    pad_notes = [[m(n) for n in voice] for voice in sp['pad']]

    def note(tr, tick, dur, pitch, vel):
        tick = max(0, tick)
        dur = min(dur, end - 1 - tick)
        if dur > 0:
            nt[tr].append((tick, dur, pitch, vel))

    def drop(b, part):
        return dropped(sp, b, part)

    def chord_idx(b):
        pos = (b - 1) % cycle
        return max(i for i, s in enumerate(starts) if s <= pos)

    def chord_at(b):
        return loop[chord_idx(b)][0]

    for b in range(1, n_bars + 1):
        sec = section(b)
        o = bt(b)

        # ---- drums (v1 recipe; kick from bar 5)
        seed(base + b * 10)
        if not drop(b, 'kick'):
            beats = ((0,) if drop(b, 'kick_one') else (0, 1.5) if drop(b, 'kick_broken')
                     else (0, 1, 2, 3))
            for beat in beats:
                v = clamp(hum_v(sp['kick'] + (2 if beat == 0 else -3 if beat % 2 else 0), 5), 78, 96)
                t = hum_t(bt(b, beat), 7)
                note(0, max(o, t) if b == n_bars else t, 100, KICK, v)
        kind, bvel, bfrom = sp['back']
        if b >= bfrom and not drop(b, 'back'):
            for beat in (1, 3):
                t = hum_t(bt(b, beat), 7)
                for pitch, dv in BACK[kind]:
                    lo, hi = (70, 85) if pitch != CLAP else (50, 66)
                    note(0, t, 90, pitch, clamp(hum_v(bvel + dv, 5), lo, hi))
        seed(base + b * 10 + 1)
        if not drop(b, 'hats'):
            every, ostep, ovel = sp['oh']
            steps = dict(sp['hats'])
            if b % every == 0:
                steps[ostep] = None
            for step in sorted(steps):
                shift = (SW if step % 4 == 2 else SW // 2 if step % 2 else 0) if sp['swing'] else 0
                t = hum_t(o + step * S16 + shift, 6)
                if steps[step] is None:
                    note(0, t, int(PPQ * .45), OHAT, clamp(hum_v(ovel, 4), 46, 60))
                else:
                    note(0, t, 50, HAT, clamp(hum_v(steps[step], 5), 40, 64))
        if b == 41:
            note(0, o, PPQ, CRASH, 80)

        # ---- bass (v1 cell): tonic in outro, chord root in A / break / A2
        seed(base + b * 10 + 2)
        if b >= 9 and not drop(b, 'bass'):
            root = (tonic if sec in ('intro', 'outro') else chord_at(b))['bass']
            for beat, dur, deg, v in sp['bass'][(b - 1) % len(sp['bass'])]:
                pitch = {'r': root, 'f': root - 5, 'o': root - 12}[deg]
                if pitch < 28:
                    pitch = root
                assert 28 <= pitch <= 45, (sid, b, pitch)
                stop = bt(b + 1) if drop(b + 1, 'bass') else end
                s = hum_t(bt(b, beat), 5)
                note(1, s, min(int(dur * PPQ) - 20, stop - s - 10), pitch, clamp(hum_v(v, 4), 52, 70))

        # ---- keys: octave up, 72-92; CC64 catch / bar re-pedal / release; cut at a keys drop
        seed(base + b * 10 + 3)
        if KEYS_FROM <= b <= KEYS_LAST and not drop(b, 'keys'):
            pos = (b - 1) % cycle
            lift = 4 if sec == 'A2' else -4 if sec == 'break' else 0
            for _, beat, dur, v in (ev for ev in sp['keys'] if ev[0] == pos):
                s = hum_t(bt(b, beat), 6)
                cb = (bt(b, beat) + PPQ // 2) // BAR + 1
                if cb > KEYS_LAST or drop(cb, 'keys'):
                    continue
                e = min(s + int(dur * PPQ), bt(KEYS_LAST + 1) - 1)
                nb = cb + 1
                while nb <= KEYS_LAST and bt(nb) < e:
                    if drop(nb, 'keys'):
                        e = bt(nb) - 1
                        break
                    nb += 1
                for p in chord_at(cb)['v']:
                    p += sp['keys_up']
                    assert 60 <= p <= 84, (sid, p)
                    note(2, s, e - s - 15, p, clamp(hum_v(v + lift, 4), 72, 92))
                if dur >= 1.5:
                    cc[2] += [(s, 64, 0), (s + 12, 64, 127)]
                    nb = b + 1
                    while bt(nb) < e:
                        cc[2] += [(bt(nb), 64, 0), (bt(nb) + 12, 64, 127)]
                        nb += 1
                    cc[2].append((e, 64, 0))

        # ---- pad: three voices from bar 1; tonic in intro (1-4, 5-8) and the closer's tail
        pos = (b - 1) % cycle
        if b <= 8:
            fresh, nb = b in (1, 5), (5 if b < 5 else 9)
            voice = pad_notes[0]
        elif b <= KEYS_LAST:
            fresh = b == 9 or pos in starts or drop(b - 1, 'pad')
            nb = b + 1
            while nb <= KEYS_LAST and (nb - 1) % cycle not in starts and not drop(nb, 'pad'):
                nb += 1
            voice = pad_notes[chord_idx(b)]
        else:
            fresh, nb = b == KEYS_LAST + 1, pad_last + 1
            voice = pad_notes[0]
        if b <= pad_last and fresh and not drop(b, 'pad'):
            seed(base + b * 10 + 4)
            pv = PAD_VEL['intro_lo' if b < 5 else sec] + sp.get('pad_lift', 0)
            for p in voice:
                note(3, hum_t(o, 6), bt(nb) - o - 40, p, clamp(hum_v(pv, 3), 55, 72))

        # ---- tex: eighth arpeggio, tone cycle running across bars (A from 17, A2)
        if sec in ('A', 'A2') and b >= TEX_FROM:
            seed(base + b * 10 + 5)
            tones = tex_tones[chord_idx(b)]
            for k in range(8):
                i = (b - TEX_FROM) * 8 + k
                v = (66 if k % 2 else 58) + (2 if sec == 'A2' else 0)
                note(4, hum_t(bt(b, k * .5), 5), int(PPQ * .42), tones[i % len(tones)],
                     clamp(hum_v(v, 3), 55, 70))

        # ---- perc: shaker sixteenths (A, A2) + two-bar conga cell from 13
        if sec in ('A', 'A2'):
            seed(base + b * 10 + 6)
            if b >= SHAKER_FROM:
                for step in range(16):
                    lag = 6 if step % 2 else 0
                    note(5, hum_t(o + step * S16 + lag, 4), 40, SHAKER,
                         clamp(hum_v(SHAKER_ACC[step % 4], 3), 38, 52))
            if b >= CONGA_FROM:
                for step, pitch, v in CONGA_V2[(b - 1) % 2]:
                    note(5, hum_t(o + step * S16, 6), 90, pitch, clamp(hum_v(v, 4), 48, 64))

    cc[2].append((end - 1, 64, 0))
    return nt, cc, pcs, n_bars, sp['bpm'], sp['title'], sp['sf'], True


def bar_of(t):
    """Nominal bar of a tick; humanize may pull a downbeat up to 8 ticks early."""
    return (t + 24) // BAR + 1


def first_bar(notes, pitches=None):
    ts = [t for t, _, p, _ in notes if pitches is None or p in pitches]
    return bar_of(min(ts)) if ts else None


def last_bar(notes, pitches=None):
    ts = [t + d - 1 for t, d, p, _ in notes if pitches is None or p in pitches]
    return max(ts) // BAR + 1 if ts else None


def audit(sp, nt, n_bars):
    """Bass/Keys/Pad/Tex (the layers v3 keeps) vs the v2 table and v1 bass range; FAIL flags misses."""
    bass = [p for _, _, p, _ in nt[1]]
    bv = [v for _, _, _, v in nt[1]]
    kp = [p for _, _, p, _ in nt[2]]
    kv = [v for _, _, _, v in nt[2]]
    pv = [v for _, _, _, v in nt[3]]
    pad_voices = {sum(1 for t2, _, _, _ in nt[3] if abs(t2 - t) < PPQ // 4) for t, _, _, _ in nt[3]}
    tp = [p for _, _, p, _ in nt[4]]
    tv = [v for _, _, _, v in nt[4]]
    tex_bars = {bar_of(t) for t, _, _, _ in nt[4]}
    in_a, in_a2 = set(range(9, 37)), set(range(41, 57))
    last_end = max(t + d for tr in nt.values() for t, d, _, _ in tr)
    ok = (28 <= min(bass) and max(bass) <= 45
          and 60 <= min(kp) and max(kp) <= 84 and 72 <= min(kv) and max(kv) <= 92
          and 55 <= min(pv) and max(pv) <= 72 and pad_voices == {3} and first_bar(nt[3]) == 1
          and last_bar(nt[3]) <= sp['pad_last'] and last_bar(nt[2]) <= KEYS_LAST
          and max(tp) - min(tp) <= 12 and 55 <= min(tv) and max(tv) <= 70
          and tex_bars <= in_a | in_a2 and tex_bars & in_a and tex_bars & in_a2
          and last_end <= n_bars * BAR)
    return (f'  layers {"OK" if ok else "FAIL"} bass p{min(bass)}-{max(bass)} v{min(bv)}-{max(bv)} '
            f'| keys v{min(kv)}-{max(kv)} p{min(kp)}-{max(kp)} bars {first_bar(nt[2])}-'
            f'{last_bar(nt[2])} | pad v{min(pv)}-{max(pv)} {"/".join(map(str, sorted(pad_voices)))}'
            f'-voice bars {first_bar(nt[3])}-{last_bar(nt[3])} | tex v{min(tv)}-{max(tv)} '
            f'p{min(tp)}-{max(tp)} A {min(tex_bars & in_a)}-{max(tex_bars & in_a)} '
            f'A2 {min(tex_bars & in_a2)}-{max(tex_bars & in_a2)} n={len(tex_bars)} bars')


if __name__ == '__main__':
    import sys
    want = sys.argv[1:] or [s['sid'] for s in SKETCHES]
    lines = []
    for sk in (s for s in SKETCHES if s['sid'] in want):
        nt, cc, pcs, n_bars, bpm, title, sf, minor = compose(sk['sid'])
        smf = build_smf(title, bpm, sf, minor, n_bars, TRACKS, pcs, nt, cc, markers=MARKERS)
        print(f'slot {sk["slot"]:02d} ' + write_smf(os.path.join(SK_DIR, sk['sid'] + '-v2.mid'), smf))
        lines.append(audit(sk, nt, n_bars))
        print(lines[-1])
    sys.exit(1 if any('FAIL' in ln for ln in lines) else 0)
