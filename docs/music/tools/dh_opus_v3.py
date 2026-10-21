"""Opus (claude): v3 rollout — v2 layers + v3 drums for the ten opus slots (3, 6, ..., 30).

Per docs/music/DEEP_HOUSE_SET_BRIEF.md '## v3 보정' and '## v3 롤아웃': bass, keys, pad, tex
and structure come unchanged from dh_opus_v2.compose(); only the Drums and Perc tracks are
rebuilt. Every element owns its slot (sixteenth steps 0-15 of a bar):
- Kick (PC16 Tough Kit): beats 1-4 (steps 0/4/8/12), beat 1 106-112 vs beats 2-4 100-105.
  Kick from bar 5. The slot's v2 break decides the rest: 'kick_one' keeps beat 1 only,
  'kick_broken' keeps beat 1 plus the a-of-3 (step 11; v1's and-of-2 is the open hat's).
- Snare 88-100 + clap 80-92 on the same tick, beats 2 and 4, from bar 9.
- Closed hat: eighths, on-beat 50-62 (steps 0/4/8/12) and off-beat 74-90 on the & of 1 and
  & of 3 (steps 2/10); a sixteenth ghost 40-49 on step 13 only in energy-2+ slots; never on
  step 15 (it would choke the & of 4 open hat). In A2 the ride takes the on-beat slots.
  Swung slots (9, 21) keep v1's eighth swing on the cymbals and congas.
- Open hat: & of 2 and & of 4 (steps 6/14) in every bar whose closed hats play, 65-80,
  180 ticks; brightness by section velocity, lower in low-energy slots. A break (or the
  closer's outro step) that takes the hats out takes the open hat out too.
- Ride (GM 51): A2 (41-56) quarters, 68-75 on beats 1/3, 60-67 on 2/4; bar 41's downbeat
  is the crash's (GM 49).
- Toms: bars 16, 36, 56, two hits on steps 13/15 (the hat ghost yields), 80-100.
- Shaker: removed. Perc (PC0 SoCal) is a per-slot two-bar conga cell on free steps
  (1/3/5/7/9/11), 70-85, A from bar 13 and A2.
- Humanize: timing +-8, velocity +-8, clamped inside each role's band so accents hold.
- `--bars 96` (or compose(sid, n_bars=96)) lays a 64-bar slot on the '## 96마디 시험판' form
  (dh_opus_v2.on_form): ride/crash from A2 bar 57, toms on 16/48/88, break 49-56 -> {sid}-v3l.mid.
  `--bars 104` does the same for the 72-bar closer, its outro 89-104 ('## 96마디 롤아웃').
"""
import os
import struct
from collections import Counter

from pipeline import BAR, PPQ, SK_DIR, SW, bt, hum_t, hum_v, seed
from pipeline import build_smf, write_smf
import dh_opus_v2
from dh_opus import CLAP, CRASH, HAT, KICK, OHAT, S16, SNARE, clamp
from dh_opus_v2 import (CONGA_FROM, CONGA_HI, CONGA_LO, TRACKS, bar_of, dropped, first_bar,
                        form, last_bar, on_form, section)

RIDE, TOM_LO, TOM_MID, TOM_HI = 51, 45, 47, 50
HUM = 8
KICK_V = {0: (108, (106, 112)), 1: (102, (100, 105))}       # beat 1 vs beats 2-4
HAT_ON, HAT_OFF, HAT_16 = (56, (50, 62)), (82, (74, 90)), (45, (40, 49))
ON_STEPS, OFF_STEPS, OH_STEPS, CONGA_STEPS = (0, 4, 8, 12), (2, 10), (6, 14), {1, 3, 5, 7, 9, 11}
OH_VEL = {'intro': 68, 'A': 72, 'break': 66, 'A2': 76, 'outro': 70}
RIDE_V = {0: (72, (68, 75)), 1: (64, (60, 67))}
BACK_FROM = 9
E_OFF = {1: -4, 2: -2, 2.5: -1, 3: 0}                        # open hat / snare level by energy

V2 = {s['slot']: s for s in dh_opus_v2.SKETCHES}


def fill_bars(fm):
    """Tom fill bars: 16, the last A bar, the last A2 bar (16/36/56 at 64, 16/48/88 at 96)."""
    return 16, fm.brk - 1, fm.keys_last


def v3(slot, fills, conga, notes):
    """fills: three (pitch_step13, pitch_step15) pairs for the fill bars;
    conga: two-bar cell [(step, pitch, velocity)] per bar."""
    sp = V2[slot]
    return dict(sp, pcs=(16,) + sp['pcs'][1:5] + (0,), notes=notes,
                fills=[[(13, a, 84 + 2 * i), (15, c, 92 + 2 * i)] for i, (a, c) in enumerate(fills)],
                conga=conga, s16=(13,) if sp['energy'] >= 2 else ())


SKETCHES = [
    v3(3, [(TOM_HI, TOM_MID), (TOM_MID, TOM_LO), (TOM_HI, TOM_LO)],
       [[(7, CONGA_HI, 76)], [(3, CONGA_LO, 72), (11, CONGA_LO, 78)]],
       'Opener, v3. Em9 <-> A9sus4/E over an E pedal; Tough Kit split by role, no 16th '
       'ghost, open hat on the & of 2 / & of 4; break keeps one kick per bar and drops the sub.'),
    v3(6, [(TOM_MID, TOM_LO), (TOM_HI, TOM_MID), (TOM_MID, TOM_LO)],
       [[(3, CONGA_HI, 78), (9, CONGA_LO, 74)], [(7, CONGA_HI, 76), (11, CONGA_LO, 80)]],
       'Bm9 <-> G9; organ chops, EP arpeggio; break is drums only.'),
    v3(9, [(TOM_HI, TOM_LO), (TOM_HI, TOM_MID), (TOM_MID, TOM_LO)],
       [[(5, CONGA_HI, 76), (11, CONGA_LO, 80)],
        [(3, CONGA_HI, 72), (9, CONGA_LO, 78), (11, CONGA_HI, 74)]],
       'C#m11 <-> G#m7b5, swung cymbals; one-bar-per-step additive break.'),
    v3(12, [(TOM_HI, TOM_MID), (TOM_MID, TOM_LO), (TOM_HI, TOM_LO)],
       [[(1, CONGA_HI, 74), (7, CONGA_LO, 80)],
        [(5, CONGA_HI, 76), (9, CONGA_LO, 78), (11, CONGA_LO, 82)]],
       'G#m9 <-> B13; break turns the kick into a 2-step (one and the a-of-3).'),
    v3(15, [(TOM_HI, TOM_MID), (TOM_HI, TOM_LO), (TOM_MID, TOM_LO)],
       [[(3, CONGA_HI, 80), (11, CONGA_LO, 74)], [(7, CONGA_HI, 76), (11, CONGA_LO, 82)]],
       'Peak. Bbm11 <-> Ab7sus4; the calibration slot under the rollout rules (no step-15 '
       'hat, no open hat in the hats-out break bars 37-40).'),
    v3(18, [(TOM_MID, TOM_LO), (TOM_HI, TOM_LO), (TOM_HI, TOM_MID)],
       [[(3, CONGA_LO, 80), (7, CONGA_HI, 78), (11, CONGA_LO, 84)],
        [(5, CONGA_HI, 76), (9, CONGA_LO, 80)]],
       'Peak. Fm9 <-> Gb9; break drops the bass, then stops every drum for two organ bars.'),
    v3(21, [(TOM_HI, TOM_MID), (TOM_MID, TOM_LO), (TOM_HI, TOM_LO)],
       [[(9, CONGA_LO, 78)], [(3, CONGA_HI, 74), (11, CONGA_LO, 80)]],
       'Drift. Gm9 <-> Dbmaj9, swung cymbals; break is sub and pad only.'),
    v3(24, [(TOM_HI, TOM_LO), (TOM_MID, TOM_LO), (TOM_HI, TOM_MID)],
       [[(7, CONGA_HI, 76), (9, CONGA_LO, 74)], [(3, CONGA_HI, 72), (11, CONGA_LO, 80)]],
       'Dm11 <-> Dm11b5; break is kick and sub only.'),
    v3(27, [(TOM_MID, TOM_LO), (TOM_HI, TOM_MID), (TOM_MID, TOM_LO)],
       [[(11, CONGA_LO, 74)], [(7, CONGA_HI, 72)]],
       'Cooldown. Dm9 <-> Fsus2; no 16th ghost; break is snare/clap and EP only.'),
    v3(30, [(TOM_HI, TOM_MID), (TOM_MID, TOM_LO), (TOM_HI, TOM_LO)],
       [[(3, CONGA_HI, 72)], [(9, CONGA_LO, 76)]],
       'Closer, 72 bars. Am9 <-> Esus2; break keeps hats, piano and pad; the 16-bar outro '
       'thins backbeat -> hats -> bass until one kick on the one of bar 72.'),
]


def sketch(sid, n_bars=None):
    """The v3 sketch on an n_bars form, fills keyed by that form's fill bars."""
    sp = next((s for s in SKETCHES if s['sid'] == sid), None)
    if sp is None:
        raise ValueError('Unknown sketch: ' + sid)
    sp = on_form(sp, n_bars)
    return dict(sp, fills=dict(zip(fill_bars(form(sp['n_bars'])), sp['fills'])))


def compose(sid, n_bars=None):
    """Return nt, cc, pcs, n_bars, bpm, title, keysig_sf, minor."""
    sp = sketch(sid, n_bars)
    nt, cc, _, n_bars, bpm, title, sf, minor = dh_opus_v2.compose(sid, sp['n_bars'])
    pcs = {i: sp['pcs'][i] for i in range(len(TRACKS))}
    nt[0], nt[5] = drums(sp, n_bars)
    return nt, cc, pcs, n_bars, bpm, title, sf, minor


def kick_beats(sp, b):
    if dropped(sp, b, 'kick'):
        return ()
    return ((0,) if dropped(sp, b, 'kick_one') else (0, 2.75) if dropped(sp, b, 'kick_broken')
            else (0, 1, 2, 3))


def drums(sp, n_bars):
    """Drums and Perc note lists; each element on its own steps."""
    end = n_bars * BAR
    fm = form(n_bars)
    base = sp['slot'] * 100000 + 31
    off = E_OFF[sp['energy']]
    dr, pc = [], []

    def note(out, tick, dur, pitch, vel):
        tick = max(0, tick)
        dur = min(dur, end - 1 - tick)
        if dur > 0:
            out.append((tick, dur, pitch, vel))

    def hv(vb):
        v, (lo, hi) = vb
        return clamp(hum_v(v, HUM), lo, hi)

    def at(o, step):
        shift = (SW if step % 4 == 2 else SW // 2 if step % 2 else 0) if sp['swing'] else 0
        return hum_t(o + step * S16 + shift, HUM)

    for b in range(1, n_bars + 1):
        sec = section(b, fm)
        o = bt(b)
        fill = sp['fills'].get(b, [])
        ride_on = fm.a2 <= b <= fm.keys_last

        # ---- kick, backbeat, toms, crash
        seed(base + b * 10)
        for beat in kick_beats(sp, b):
            t = hum_t(bt(b, beat), HUM)
            note(dr, max(o, t) if b == n_bars else t, 100, KICK, hv(KICK_V[0 if beat == 0 else 1]))
        if b >= BACK_FROM and not dropped(sp, b, 'back'):
            for beat in (1, 3):
                t = hum_t(bt(b, beat), HUM)
                note(dr, t, 110, SNARE, clamp(hum_v(92 + beat + off // 2, HUM), 88, 100))
                note(dr, t, 110, CLAP, clamp(hum_v(86 + off // 2, HUM), 80, 92))
        for step, pitch, v in fill:
            note(dr, hum_t(o + step * S16, HUM), 160, pitch, clamp(hum_v(v, HUM), 80, 100))
        if b == fm.a2:
            note(dr, o, PPQ, CRASH, 80)

        # ---- cymbals: closed hat + open hat together (a hats-out bar loses both), ride
        seed(base + b * 10 + 1)
        if not dropped(sp, b, 'hats'):
            taken = {s for s, _, _ in fill}
            grid = [(s, HAT_OFF) for s in OFF_STEPS]
            grid += [(s, HAT_16) for s in sp['s16'] if s not in taken]
            if not ride_on:
                grid += [(s, HAT_ON) for s in ON_STEPS]
            for step, vb in sorted(grid):
                note(dr, at(o, step), 50, HAT, hv(vb))
            for step in OH_STEPS:
                note(dr, at(o, step), 180, OHAT, clamp(hum_v(OH_VEL[sec] + off, HUM), 65, 80))
        if ride_on:
            for beat in range(4):
                if b == fm.a2 and beat == 0:
                    continue
                note(dr, hum_t(bt(b, beat), HUM), int(PPQ * .9), RIDE, hv(RIDE_V[beat % 2]))

        # ---- perc: conga cell only (A from 13, A2)
        if sec in ('A', 'A2') and b >= CONGA_FROM:
            seed(base + b * 10 + 6)
            for step, pitch, v in sp['conga'][(b - 1) % 2]:
                note(pc, at(o, step), 90, pitch, clamp(hum_v(v, HUM), 70, 85))
    return dr, pc


def step_of(t):
    """(bar, sixteenth step) of a humanized tick."""
    b = bar_of(t)
    return b, round((t - bt(b)) / S16)


def rng(vs):
    return f'{min(vs)}-{max(vs)}' if vs else '-'


def spans(bars):
    """[37, 38, 39, 41] -> '37-39,41'."""
    out, bars = [], sorted(bars)
    for b in bars:
        if out and b == out[-1][1] + 1:
            out[-1][1] = b
        else:
            out.append([b, b])
    return ','.join(f'{a}' if a == z else f'{a}-{z}' for a, z in out) or '-'


def chunks(buf):
    pos, out = 14, []
    while pos < len(buf):
        ln = struct.unpack('>I', buf[pos + 4:pos + 8])[0]
        out.append(buf[pos:pos + 8 + ln])
        pos += 8 + ln
    return out


def note_ons(chunk):
    """(tick, pitch, velocity) of every note-on in an MTrk chunk built by pipeline.build_smf."""
    d, i, tick, out = chunk[8:], 0, 0, []
    while i < len(d):
        dt = 0
        while True:
            c = d[i]
            i += 1
            dt = (dt << 7) | (c & 0x7F)
            if not c & 0x80:
                break
        tick += dt
        st = d[i]
        if st == 0xFF:
            i += 3 + d[i + 2]
        elif st & 0xF0 in (0xC0, 0xD0):
            i += 2
        else:
            if st & 0xF0 == 0x90 and d[i + 2]:
                out.append((tick, d[i + 1], d[i + 2]))
            i += 3
    return out


def audit(sp, nt, n_bars):
    """Drum ranges and slot ownership vs the v3 table + rollout fixes; FAIL flags misses."""
    dr, pc = nt[0], nt[5]
    bars = range(1, n_bars + 1)
    fm = form(n_bars)
    brk = range(fm.brk, fm.a2)

    def sel(pitches, steps=None):
        return [(t, v) for t, _, p, v in dr if p in pitches
                and (steps is None or step_of(t)[1] in steps)]

    k1 = [v for t, v in sel({KICK}, {0})]
    k234 = [v for t, v in sel({KICK}, {4, 8, 12})]
    kick_slots = sorted(step_of(t) for t, _ in sel({KICK}))
    want_kick = sorted((b, int(beat * 4)) for b in bars for beat in kick_beats(sp, b))
    hon = [v for t, v in sel({HAT}, set(ON_STEPS))]
    hoff = [v for t, v in sel({HAT}, set(OFF_STEPS))]
    h16 = [v for t, v in sel({HAT}, {13})]
    hat_steps = {step_of(t)[1] for t, _ in sel({HAT})}
    a2_on = [t for t, _ in sel({HAT}, set(ON_STEPS)) if fm.a2 <= bar_of(t) <= fm.keys_last]
    ohs = sel({OHAT})
    ohv = [v for _, v in ohs]
    oh_bar = Counter(bar_of(t) for t, _ in ohs)
    hat_bars = {bar_of(t) for t, _ in sel({HAT})}
    oh_ok = all(oh_bar.get(b, 0) == (2 if b in hat_bars else 0) for b in bars)
    oh_out = [oh_bar.get(b, 0) for b in bars if b not in brk]
    oh_zero = [b for b in bars if b not in brk and not oh_bar.get(b)]
    oh_brk = [oh_bar.get(b, 0) for b in brk]
    sn = [v for _, v in sel({SNARE})]
    cl = [v for _, v in sel({CLAP})]
    want_back = {b for b in bars if b >= BACK_FROM and not dropped(sp, b, 'back')}
    back_ok = ({bar_of(t) for t, _ in sel({SNARE})} == want_back
               and sorted(t for t, _ in sel({SNARE})) == sorted(t for t, _ in sel({CLAP})))
    ri = sel({RIDE})
    riv = [v for _, v in ri]
    ri_bars = sorted({bar_of(t) for t, _ in ri})
    toms = sel({TOM_LO, TOM_MID, TOM_HI})
    tov = [v for _, v in toms]
    tom_slots = sorted({step_of(t) for t, _ in toms})
    want_toms = sorted((b, s) for b, f in sp['fills'].items() for s, _, _ in f)
    cg = [v for _, _, p, v in pc]
    cg_steps = {step_of(t)[1] for t, _, _, _ in pc}
    ok = (106 <= min(k1) and max(k1) <= 112 and 100 <= min(k234) and max(k234) <= 105
          and kick_slots == want_kick
          and 50 <= min(hon) and max(hon) <= 62 and 74 <= min(hoff) and max(hoff) <= 90
          and (not h16 or 40 <= min(h16) and max(h16) <= 49)
          and hat_steps <= set(ON_STEPS) | set(OFF_STEPS) | {13} and not a2_on
          and oh_ok and 65 <= min(ohv) and max(ohv) <= 80
          and all(d == 180 for t, d, p, _ in dr if p == OHAT and t + 180 < n_bars * BAR)
          and 88 <= min(sn) and max(sn) <= 100 and 80 <= min(cl) and max(cl) <= 92 and back_ok
          and ri_bars == list(range(fm.a2, fm.keys_last + 1))
          and 60 <= min(riv) and max(riv) <= 75
          and tom_slots == want_toms and 80 <= min(tov) and max(tov) <= 100
          and all(p in (CONGA_HI, CONGA_LO) for _, _, p, _ in pc)
          and 70 <= min(cg) and max(cg) <= 85 and cg_steps <= CONGA_STEPS)
    zero = f' (0 in hats-out {spans(oh_zero)})' if oh_zero else ''
    return ok, (f'  drums {"OK" if ok else "FAIL"} kick beat1 {rng(k1)} / 2-4 {rng(k234)} '
                f'from bar {min(t for t, _ in kick_slots)} | ch-hat on {rng(hon)} off {rng(hoff)} '
                f'16th@13 {rng(h16)} steps {sorted(hat_steps)} '
                f'step15={"PRESENT" if 15 in hat_steps else "none"} A2-on-beat={len(a2_on)} '
                f'| open-hat {rng(ohv)} per bar outside break {min(oh_out)}-{max(oh_out)}{zero}, '
                f'break {spans(brk)} {oh_brk} | snare {rng(sn)} clap {rng(cl)} bars '
                f'{spans({bar_of(t) for t, _ in sel({SNARE})})} | ride {rng(riv)} bars '
                f'{spans(ri_bars)} | tom {rng(tov)} bars {spans({b for b, _ in tom_slots})} '
                f'| conga {rng(cg)} n={len(cg)}')


def form_check(sp, nt, n_bars):
    """Section map read back from the notes: hats/bass/kick-out bars equal the slot's (stretched)
    drops (bass bars counted while sounding; the v1 cell's rest bars aside), one crash on the A2
    downbeat, Tex only in A (from 17) and A2, keys 9 to the bar before the outro, pad 1 to pad_last."""
    fm = form(n_bars)
    bars = range(1, n_bars + 1)

    def on(track, pitches=None):
        return {bar_of(t) for t, _, p, _ in nt[track] if pitches is None or p in pitches}

    hats_out = [b for b in bars if b not in on(0, {HAT})]
    rest = {b for b in range(9, n_bars + 1) if not sp['bass'][(b - 1) % len(sp['bass'])]}
    bass_on = {b for t, d, _, _ in nt[1] for b in range(bar_of(t), (t + d - 1) // BAR + 2)}
    bass_out = [b for b in range(9, n_bars + 1) if b not in bass_on | rest]
    kick_out = [b for b in bars if b not in on(0, {KICK})]
    crash = sorted(bar_of(t) for t, _, p, _ in nt[0] if p == CRASH)
    tex = on(4)
    want_tex = set(range(dh_opus_v2.TEX_FROM, fm.brk)) | set(range(fm.a2, fm.outro))
    keys = (first_bar(nt[2]), last_bar(nt[2]))
    pad = (first_bar(nt[3]), last_bar(nt[3]))
    ok = (hats_out == [b for b in bars if dropped(sp, b, 'hats')]
          and bass_out == [b for b in range(9, n_bars + 1)
                           if b not in rest and dropped(sp, b, 'bass')]
          and kick_out == [b for b in bars if dropped(sp, b, 'kick')]
          and crash == [fm.a2] and tex == want_tex
          and keys == (dh_opus_v2.KEYS_FROM, fm.keys_last) and pad == (1, sp['pad_last']))
    return ok, (f'  form {"OK" if ok else "FAIL"} {n_bars} bars markers '
                f'{" / ".join(f"{name} {b}" for b, name in fm.markers)} | hats-out '
                f'{spans(hats_out)} | bass-out {spans(bass_out)} (+{len(rest)} cell-rest bars) '
                f'| kick-out {spans(kick_out)} '
                f'| crash {spans(crash)} | tex {spans(tex)} | keys {keys[0]}-{keys[1]} '
                f'| pad {pad[0]}-{pad[1]}')


def identical(sid, nt, cc, smf, n_bars):
    """Non-drum tracks (Bass, Keys, Pad, Tex) vs a fresh v2 build: note/CC lists and MTrk bytes."""
    nt2, cc2, pcs2, n_bars, bpm, title, sf, minor = dh_opus_v2.compose(sid, n_bars)
    same_lists = all(nt[i] == nt2[i] and cc[i] == cc2[i] for i in range(1, 5))
    mem = build_smf(title, bpm, sf, minor, n_bars, TRACKS, pcs2, nt2, cc2,
                    markers=form(n_bars).markers)
    same_mem = chunks(smf)[2:6] == chunks(mem)[2:6]
    n = sum(len(nt[i]) for i in range(1, 5))
    ok = same_lists and same_mem
    return ok, (f'  v2-identity {"OK" if ok else "FAIL"} Bass/Keys/Pad/Tex note+CC lists '
                f'{"equal" if same_lists else "DIFFER"} ({n} notes) | MTrk bytes vs v2 build '
                f'{"identical" if same_mem else "DIFFERENT"}')


def drum_diff(old, new):
    """Drums/Perc note-ons by nominal (bar, step, pitch): removed / added / re-humanized."""
    names = {KICK: 'kick', SNARE: 'snare', CLAP: 'clap', HAT: 'ch-hat', OHAT: 'open-hat',
             RIDE: 'ride', CRASH: 'crash', TOM_LO: 'tom', TOM_MID: 'tom', TOM_HI: 'tom',
             CONGA_HI: 'conga', CONGA_LO: 'conga'}
    parts = []
    for idx, label in ((1, 'Drums'), (6, 'Perc')):
        a = {(step_of(t), p): (t, v) for t, p, v in note_ons(chunks(old)[idx])}
        b = {(step_of(t), p): (t, v) for t, p, v in note_ons(chunks(new)[idx])}
        gone = Counter((names[p], s) for ((_, s), p) in a.keys() - b.keys())
        gone_bars = sorted({bb for ((bb, _), _) in a.keys() - b.keys()})
        new_ = Counter((names[p], s) for ((_, s), p) in b.keys() - a.keys())
        moved = sum(1 for k in a.keys() & b.keys() if a[k] != b[k])
        parts.append(f'{label}: removed {sum(gone.values())} '
                     f'[{", ".join(f"{nm}@step{s} x{c}" for (nm, s), c in sorted(gone.items()))}]'
                     f' bars {spans(gone_bars)} | added {sum(new_.values())} | same slot, new '
                     f'tick/velocity {moved}/{len(a.keys() & b.keys())}')
    return '  diff vs on-disk v3: ' + ' || '.join(parts)


if __name__ == '__main__':
    import argparse
    import sys
    ap = argparse.ArgumentParser()
    ap.add_argument('--bars', type=int, default=None,
                    help='기본: 슬롯 원래 길이(64, 클로저 72) -> {sid}-v3.mid; 96(64마디 슬롯) 또는 '
                         '104(72마디 클로저) -> {sid}-v3l.mid')
    ap.add_argument('sids', nargs='*')
    a = ap.parse_args()
    n = a.bars
    known = {s['sid'] for s in SKETCHES}
    if set(a.sids) - known:
        ap.error(f'unknown sid: {sorted(set(a.sids) - known)}')
    if n is not None and not a.sids:
        ap.error('--bars requires explicit sids (96 for 64-bar slots, 104 for the 72-bar closer)')
    long_of = {64: 96, 72: 104}
    bad = [s['sid'] for s in SKETCHES if s['sid'] in a.sids
           and n not in (None, s['n_bars'], long_of[s['n_bars']])]
    if bad:
        ap.error(f'--bars {n} does not fit {bad} (96 for 64-bar slots, 104 for the 72-bar closer)')
    oks = []
    for sk in (s for s in SKETCHES if not a.sids or s['sid'] in a.sids):
        sp = sketch(sk['sid'], n)
        nt, cc, pcs, n_bars, bpm, title, sf, minor = compose(sk['sid'], n)
        smf = build_smf(title, bpm, sf, minor, n_bars, TRACKS, pcs, nt, cc,
                        markers=form(n_bars).markers)
        tag = 'v3' if n_bars == sk['n_bars'] else 'v3l'
        path = os.path.join(SK_DIR, f'{sk["sid"]}-{tag}.mid')
        old = None
        if os.path.exists(path):
            with open(path, 'rb') as f:
                old = f.read()
        print(f'slot {sk["slot"]:02d} ' + write_smf(path, smf))
        ok1, line = audit(sp, nt, n_bars)
        ok2, ident = identical(sk['sid'], nt, cc, smf, n_bars)
        ok3, fline = form_check(sp, nt, n_bars)
        layers = dh_opus_v2.audit(sp, nt, n_bars)
        total = sum(len(v) for v in nt.values())
        last_end = max(t + d for tr in nt.values() for t, d, _, _ in tr)
        print(line)
        print(layers)
        print(fline)
        print(ident)
        print(f'  total notes {total} | last note ends in bar {(last_end - 1) // BAR + 1}/{n_bars} '
              f'| pcs {[pcs[i] for i in range(len(TRACKS))]}')
        if old is not None:
            print(f'  on-disk {tag} bytes {"identical" if old == smf else "changed"}')
            if old != smf:
                print(drum_diff(old, smf))
        oks.append(ok1 and ok2 and ok3 and 'FAIL' not in layers)
    sys.exit(0 if all(oks) else 1)
