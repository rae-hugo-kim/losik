"""Opus (claude): v2 calibration of slot 15, dh15-deep-meridian (Bb minor, 122).

Per docs/music/DEEP_HOUSE_SET_BRIEF.md '## v2 보정': drums, bass cell, chord loop and key
come unchanged from dh_opus.py (v1). What changes:
- Keys (EP PC4): the same Bbm11 <-> Ab7sus4 voicings one octave up (Db4-Eb5, inside
  C4-C6), velocity 72-92, two hits per bar (the v1 e-of-1 stab kept, then a 1.6-2.3 beat
  hold), CC64 catch/release kept.
- Pad (PC89 Classic Pad): from bar 1, velocity 55-72, root+fifth+ninth (Bb2 F3 C4 /
  Ab2 Eb3 Bb3); tonic-only in intro and outro tail (mix-safe), follows the loop from 9.
- Tex (PC16 Tonewheel Organ): eighth-note chord-tone arpeggio, a three-note cycle inside
  one octave (F4 Ab4 Db5 -> Gb4 Ab4 Db5: only F -> Gb moves, the loop's own moving voice),
  velocity 55-70, A from bar 17 and A2 only.
- Perc (drum ch9, own track, PC25): sixteenth shaker (GM 82) 38-52 from bar 9 plus a
  two-bar conga cell (GM 63 open high / 64 low) from bar 13, A and A2 only.
- Structure: intro 8 (pad + hats from 1, kick from 5), A 9-36, break 37-40 (the v1
  three-step strip compressed: 37-38 hats out, 39 + bass out, 40 + kick out), A2 41-56
  (crash on 41), outro 57-64 (drums + bass; the pad's tonic tail ends with bar 60).
"""
import os

from pipeline import BAR, PPQ, SK_DIR, bt, hum_t, hum_v, seed
from pipeline import build_smf, write_smf
import dh_opus
from dh_opus import BACK, CLAP, CRASH, HAT, KICK, OHAT, RIM, S16, SNARE, clamp

TRACKS = [('Drums', 9), ('Bass', 0), ('Keys', 1), ('Pad', 2), ('Tex', 3), ('Perc', 9)]
MARKERS = [(1, 'intro'), (9, 'A'), (37, 'break'), (41, 'A2'), (57, 'outro')]
SHAKER, CONGA_HI, CONGA_LO = 82, 63, 64
KEYS_FROM, KEYS_LAST = 9, 56     # keys, tex and perc stop before the outro (bar 57)
PAD_LAST = 60                    # pad's tonic tail runs four bars into the outro
TEX_FROM, SHAKER_FROM, CONGA_FROM = 17, 9, 13

V1 = next(s for s in dh_opus.SKETCHES if s['slot'] == 15)

SKETCHES = [dict(
    V1,
    pcs=(25, 38, 4, 89, 16, 25),
    # keys: (bar_in_cycle, beat, length_beats, velocity) — v1's e-of-1 stab, then a hold
    keys=[(0, .75, .65, 86), (0, 1.5, 2.3, 80),
          (1, .75, 2.3, 84), (1, 3.25, .65, 76),
          (2, .75, .65, 86), (2, 1.5, 2.3, 80),
          (3, .75, 2.3, 84), (3, 3.25, .65, 76)],
    keys_up=12,
    # pad: (root offset from the v1 pad root, fifth, ninth)
    pad_voice=(0, 7, 14),
    # tex: three-tone cycle per loop chord (index into the loop), one octave span
    tex=[['F4', 'Ab4', 'Db5'], ['Gb4', 'Ab4', 'Db5']],
    # perc: shaker accents per sixteenth step; conga two-bar cell (step, pitch, velocity)
    shaker={0: 40, 1: 38, 2: 50, 3: 40},
    conga=[[(3, CONGA_HI, 60), (6, CONGA_LO, 56), (11, CONGA_HI, 54)],
           [(6, CONGA_LO, 58), (10, CONGA_HI, 52), (13, CONGA_HI, 50), (14, CONGA_LO, 56)]],
    drops=[(1, 4, {'kick'}), (37, 38, {'hats'}), (39, 39, {'hats', 'bass'}),
           (40, 40, {'hats', 'bass', 'kick'})],
    break_txt='4마디 3단 감산: 37–38 햇 아웃 → 39 +베이스 아웃 → 40 +킥 아웃(스네어·EP·패드만)',
    notes='Peak, v2. Bbm11 <-> Ab7sus4 (i - bVII seventh-sus, only F -> Gb moves); EP an '
          'octave up with a short e-of-1 stab and a long hold every bar; three-note pad (root, '
          'fifth, ninth) from bar 1; tonewheel-organ chord-tone arpeggio cycling F-Ab-Db / '
          'Gb-Ab-Db in A and A2; shaker sixteenths and a two-bar conga cell; 8-bar intro, '
          '4-bar break stripping hats, then bass, then kick.'),
]


def section(b):
    return ('intro' if b <= 8 else 'A' if b <= 36 else 'break' if b <= 40
            else 'A2' if b <= 56 else 'outro')


def compose(sid):
    """Return nt, cc, pcs, n_bars, bpm, title, keysig_sf, minor."""
    sp = next((s for s in SKETCHES if s['sid'] == sid), None)
    if sp is None:
        raise ValueError('Unknown sketch: ' + sid)
    n_bars = sp['n_bars']
    end = n_bars * BAR
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
    tex_tones = [[dh_opus.m(n) for n in tones] for tones in sp['tex']]

    def note(tr, tick, dur, pitch, vel):
        tick = max(0, tick)
        dur = min(dur, end - 1 - tick)
        if dur > 0:
            nt[tr].append((tick, dur, pitch, vel))

    def dropped(b, part):
        return any(lo <= b <= hi and part in parts for lo, hi, parts in sp['drops'])

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
        if not dropped(b, 'kick'):
            for beat in (0, 1, 2, 3):
                v = clamp(hum_v(sp['kick'] + (2 if beat == 0 else -3 if beat % 2 else 0), 5), 78, 96)
                t = hum_t(bt(b, beat), 7)
                note(0, max(o, t) if b == n_bars else t, 100, KICK, v)
        kind, bvel, bfrom = sp['back']
        if b >= bfrom and not dropped(b, 'back'):
            for beat in (1, 3):
                t = hum_t(bt(b, beat), 7)
                for pitch, dv in BACK[kind]:
                    lo, hi = (70, 85) if pitch != CLAP else (50, 66)
                    note(0, t, 90, pitch, clamp(hum_v(bvel + dv, 5), lo, hi))
        seed(base + b * 10 + 1)
        if not dropped(b, 'hats'):
            every, ostep, ovel = sp['oh']
            steps = dict(sp['hats'])
            if b % every == 0:
                steps[ostep] = None
            for step in sorted(steps):
                t = hum_t(o + step * S16, 6)
                if steps[step] is None:
                    note(0, t, int(PPQ * .45), OHAT, clamp(hum_v(ovel, 4), 46, 60))
                else:
                    note(0, t, 50, HAT, clamp(hum_v(steps[step], 5), 40, 64))
        if b == 41:
            note(0, o, PPQ, CRASH, 80)

        # ---- bass (v1 cell): tonic in outro, chord root in A / break / A2
        seed(base + b * 10 + 2)
        if b >= 9 and not dropped(b, 'bass'):
            root = (tonic if sec in ('intro', 'outro') else chord_at(b))['bass']
            for beat, dur, deg, v in sp['bass'][(b - 1) % len(sp['bass'])]:
                pitch = {'r': root, 'f': root - 5, 'o': root - 12}[deg]
                if pitch < 28:
                    pitch = root
                assert 28 <= pitch <= 45, (sid, b, pitch)
                stop = bt(b + 1) if dropped(b + 1, 'bass') else end
                s = hum_t(bt(b, beat), 5)
                note(1, s, min(int(dur * PPQ) - 20, stop - s - 10), pitch, clamp(hum_v(v, 4), 52, 70))

        # ---- keys: octave up, 72-92, two hits per bar; CC64 catch / bar re-pedal / release
        seed(base + b * 10 + 3)
        if KEYS_FROM <= b <= KEYS_LAST and not dropped(b, 'keys'):
            pos = (b - 1) % cycle
            lift = 4 if sec == 'A2' else -4 if sec == 'break' else 0
            for _, beat, dur, v in (ev for ev in sp['keys'] if ev[0] == pos):
                s = hum_t(bt(b, beat), 6)
                cb = (bt(b, beat) + PPQ // 2) // BAR + 1
                if cb > KEYS_LAST:
                    continue
                e = min(s + int(dur * PPQ), bt(KEYS_LAST + 1) - 1)
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

        # ---- pad: root+5+9 from bar 1; tonic holds in intro (1-4, 5-8) and outro tail
        pos = (b - 1) % cycle
        if b <= 8:
            fresh, nb = b in (1, 5), (5 if b < 5 else 9)
            r = tonic['pad']
        elif b <= KEYS_LAST:
            fresh = b == 9 or pos in starts
            nb = b + 1
            while nb <= KEYS_LAST and (nb - 1) % cycle not in starts:
                nb += 1
            r = chord_at(b)['pad']
        else:
            fresh, nb = b == KEYS_LAST + 1, PAD_LAST + 1
            r = tonic['pad']
        if b <= PAD_LAST and fresh and not dropped(b, 'pad'):
            seed(base + b * 10 + 4)
            pv = {'intro': 58 if b < 5 else 62, 'A': 66, 'break': 70, 'A2': 68, 'outro': 58}[sec]
            for iv in sp['pad_voice']:
                note(3, hum_t(o, 6), bt(nb) - o - 40, r + iv, clamp(hum_v(pv, 3), 55, 72))

        # ---- tex: organ eighth arpeggio, three-tone cycle running across bars (A from 17, A2)
        if sec in ('A', 'A2') and b >= TEX_FROM:
            seed(base + b * 10 + 5)
            tones = tex_tones[chord_idx(b)]
            for k in range(8):
                i = (b - TEX_FROM) * 8 + k
                v = (66 if k % 2 else 58) + (2 if sec == 'A2' else 0)
                note(4, hum_t(bt(b, k * .5), 5), int(PPQ * .42), tones[i % 3],
                     clamp(hum_v(v, 3), 55, 70))

        # ---- perc: shaker sixteenths (A, A2) + two-bar conga cell from 13
        if sec in ('A', 'A2'):
            seed(base + b * 10 + 6)
            if b >= SHAKER_FROM:
                for step in range(16):
                    lag = 6 if step % 2 else 0
                    note(5, hum_t(o + step * S16 + lag, 4), 40, SHAKER,
                         clamp(hum_v(sp['shaker'][step % 4], 3), 38, 52))
            if b >= CONGA_FROM:
                for step, pitch, v in sp['conga'][(b - 1) % 2]:
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


def audit(nt, n_bars):
    """v1 drum/bass recipe plus the v2 table's keys/pad/tex/perc ranges; FAIL flags misses."""
    drums, perc = nt[0], nt[5]
    k = [v for _, _, p, v in drums if p == KICK]
    h = [v for _, _, p, v in drums if p == HAT]
    bk = [v for _, _, p, v in drums if p in (RIM, SNARE)]
    cl = [v for _, _, p, v in drums if p == CLAP]
    oh = sum(1 for _, _, p, _ in drums if p == OHAT)
    bass = [p for _, _, p, _ in nt[1]]
    bv = [v for _, _, _, v in nt[1]]
    kp = [p for _, _, p, _ in nt[2]]
    kv = [v for _, _, _, v in nt[2]]
    pv = [v for _, _, _, v in nt[3]]
    pad_voices = max(sum(1 for t2, _, _, _ in nt[3] if abs(t2 - t) < PPQ // 4) for t, _, _, _ in nt[3])
    tp = [p for _, _, p, _ in nt[4]]
    tv = [v for _, _, _, v in nt[4]]
    tex_bars = {bar_of(t) for t, _, _, _ in nt[4]}
    sv = [v for _, _, p, v in perc if p == SHAKER]
    cv = [v for _, _, p, v in perc if p in (CONGA_HI, CONGA_LO)]
    perc_bars = {bar_of(t) for t, _, _, _ in perc}
    in_a = set(range(9, 37)) | set(range(41, 57))
    last_end = max(t + d for tr in nt.values() for t, d, _, _ in tr)
    ok = (78 <= min(k) and max(k) <= 96 and 40 <= min(h) and max(h) <= 64
          and 70 <= min(bk) and max(bk) <= 85 and (not cl or max(cl) <= 66)
          and 28 <= min(bass) and max(bass) <= 45 and max(bv) < max(k)
          and 60 <= min(kp) and max(kp) <= 84 and 72 <= min(kv) and max(kv) <= 92
          and 55 <= min(pv) and max(pv) <= 72 and pad_voices == 3 and first_bar(nt[3]) == 1
          and max(tp) - min(tp) <= 12 and 55 <= min(tv) and max(tv) <= 70 and tex_bars <= in_a
          and 38 <= min(sv) and max(sv) <= 52 and perc_bars <= in_a
          and first_bar(drums, {KICK}) == 5 and 8 <= oh * 64 / n_bars <= 32
          and last_bar(nt[2]) <= KEYS_LAST and last_end <= n_bars * BAR)
    check = (f'  check {"OK" if ok else "FAIL"} kick {min(k)}-{max(k)} hat {min(h)}-{max(h)} '
             f'back {min(bk)}-{max(bk)} clap={len(cl)} oh={oh}/{n_bars}bars '
             f'bass {min(bass)}-{max(bass)} v{min(bv)}-{max(bv)} '
             f'last_end_bar={last_end / BAR:.3f}')
    rng = (f'  range keys v{min(kv)}-{max(kv)} p{min(kp)}-{max(kp)} bars {first_bar(nt[2])}-'
           f'{last_bar(nt[2])} | pad v{min(pv)}-{max(pv)} {pad_voices}-voice bars '
           f'{first_bar(nt[3])}-{last_bar(nt[3])} | tex v{min(tv)}-{max(tv)} p{min(tp)}-{max(tp)} '
           f'bars {first_bar(nt[4])}-{last_bar(nt[4])} | perc shaker v{min(sv)}-{max(sv)} '
           f'from {first_bar(perc, {SHAKER})}, conga v{min(cv)}-{max(cv)} from '
           f'{first_bar(perc, {CONGA_HI, CONGA_LO})}, last {last_bar(perc)} | first: hats '
           f'{first_bar(drums, {HAT})} kick {first_bar(drums, {KICK})} '
           f'bass {first_bar(nt[1])} back {first_bar(drums, {SNARE})}')
    return check, rng


if __name__ == '__main__':
    import sys
    sk = SKETCHES[0]
    nt, cc, pcs, n_bars, bpm, title, sf, minor = compose(sk['sid'])
    smf = build_smf(title, bpm, sf, minor, n_bars, TRACKS, pcs, nt, cc, markers=MARKERS)
    print(f'slot {sk["slot"]:02d} ' + write_smf(os.path.join(SK_DIR, sk['sid'] + '-v2.mid'), smf))
    check, rng = audit(nt, n_bars)
    print(check)
    print(rng)
    sys.exit(1 if 'FAIL' in check else 0)
