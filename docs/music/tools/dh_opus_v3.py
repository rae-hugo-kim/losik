"""Opus (claude): v3 calibration of slot 15, dh15-deep-meridian (Bb minor, 122).

Per docs/music/DEEP_HOUSE_SET_BRIEF.md '## v3 보정': bass, keys, pad, tex and structure
come unchanged from dh_opus_v2.compose(); only the Drums and Perc tracks are rebuilt.
Every element owns its slot (sixteenth steps 0-15 of a bar):
- Kick (PC16 Tough Kit): beats 1-4 (steps 0/4/8/12), 100-112, beat 1 accented (+6) and
  kept above beats 2-4 (106-112 vs 100-105). Kick from bar 5, out on bar 40 (as v2).
- Snare 88-100 + clap 80-92 layered on the same tick, beats 2 and 4, from bar 9.
- Closed hat: eighths with on-beat 50-62 (steps 0/4/8/12) and off-beat 74-90 on the & of 1
  and & of 3 (steps 2/10); sixteenth ghosts 40-49 only in beat 4 (steps 13/15). The & of 2
  and & of 4 belong to the open hat, so no closed hat sits there. In A2 the ride takes the
  on-beat cymbal slots. Closed hats keep v2's break strip (out in bars 37-40).
- Open hat: every bar, & of 2 and & of 4 (steps 6/14), 65-80, 180 ticks; section sets the
  brightness by velocity (intro 68, A 72, break 66, A2 76, outro 70), never by removal.
- Ride (GM 51): A2 (41-56) quarters, 68-75 on beats 1/3 and 60-67 on 2/4; bar 41's
  downbeat is the crash's (GM 49, kept from v2).
- Toms: bars 16, 36, 56, two hits in beat 4 on the sixteenth-ghost steps 13/15 (the hats
  yield them): 50->47, 50->45, 47->45.
- Shaker: removed. Perc track (PC0 SoCal) keeps congas only: a two-bar cell of four hits on
  free steps (3/11, 7/11), 70-85, A from bar 13 and A2.
- Humanize: timing +-8, velocity +-8, clamped inside each role's band so accents hold.
"""
import os
import struct
from collections import Counter

from pipeline import BAR, PPQ, SK_DIR, bt, hum_t, hum_v, seed
from pipeline import build_smf, write_smf
import dh_opus_v2
from dh_opus import CLAP, CRASH, HAT, KICK, OHAT, S16, SNARE, clamp
from dh_opus_v2 import CONGA_FROM, CONGA_HI, CONGA_LO, MARKERS, TRACKS, bar_of, section

RIDE, TOM_LO, TOM_MID, TOM_HI = 51, 45, 47, 50
HUM = 8
V2 = dh_opus_v2.SKETCHES[0]

SKETCHES = [dict(
    V2,
    pcs=(16, 38, 4, 89, 16, 0),
    # kick: (base velocity, band) — beat 1 vs beats 2-4
    kick={0: (108, (106, 112)), 1: (102, (100, 105))},
    # backbeat on beats 2/4 from bar 9: snare base by beat, clap base
    snare={1: 93, 3: 95}, clap=86, back_from=9,
    # closed hat steps -> (base velocity, band)
    hat_on=(56, (50, 62)), hat_off=(82, (74, 90)), hat_16=(45, (40, 49)),
    on_steps=(0, 4, 8, 12), off_steps=(2, 10), s16_steps=(13, 15),
    # open hat: & of 2 / & of 4, per-section base velocity, band 65-80
    oh_steps=(6, 14), oh_vel={'intro': 68, 'A': 72, 'break': 66, 'A2': 76, 'outro': 70},
    # ride in A2: beats 1/3 vs 2/4
    ride={0: (72, (68, 75)), 1: (64, (60, 67))}, ride_bars=(41, 56),
    # tom fills: bar -> [(step, pitch, velocity)] on the beat-4 sixteenth-ghost steps
    fills={16: [(13, TOM_HI, 84), (15, TOM_MID, 92)],
           36: [(13, TOM_HI, 86), (15, TOM_LO, 94)],
           56: [(13, TOM_MID, 86), (15, TOM_LO, 94)]},
    # conga two-bar cell (step, pitch, velocity), only on steps no drum owns
    conga=[[(3, CONGA_HI, 80), (11, CONGA_LO, 74)],
           [(7, CONGA_HI, 76), (11, CONGA_LO, 82)]],
    notes='Peak, v3. v2 harmony and structure untouched; Tough Kit drums split by role: '
          'kick 100-112 with a beat-1 accent, snare+clap on 2/4, closed-hat eighths '
          'strong-weak (off-beat 74-90 over on-beat 50-62) with beat-4 sixteenth ghosts, an '
          'open hat on the & of 2 and & of 4 every bar, ride quarters in A2, two-hit tom '
          'fills at bars 16/36/56, shaker gone, a sparse four-hit conga cell on SoCal.'),
]


def compose(sid):
    """Return nt, cc, pcs, n_bars, bpm, title, keysig_sf, minor."""
    sp = next((s for s in SKETCHES if s['sid'] == sid), None)
    if sp is None:
        raise ValueError('Unknown sketch: ' + sid)
    nt, cc, _, n_bars, bpm, title, sf, minor = dh_opus_v2.compose(sid)
    pcs = {i: sp['pcs'][i] for i in range(len(TRACKS))}
    nt[0], nt[5] = drums(sp, n_bars)
    return nt, cc, pcs, n_bars, bpm, title, sf, minor


def drums(sp, n_bars):
    """Drums and Perc note lists; each element on its own steps."""
    end = n_bars * BAR
    base = sp['slot'] * 100000 + 31
    dr, pc = [], []

    def note(out, tick, dur, pitch, vel):
        tick = max(0, tick)
        dur = min(dur, end - 1 - tick)
        if dur > 0:
            out.append((tick, dur, pitch, vel))

    def hv(vb):
        v, (lo, hi) = vb
        return clamp(hum_v(v, HUM), lo, hi)

    def dropped(b, part):
        return any(lo <= b <= hi and part in parts for lo, hi, parts in sp['drops'])

    for b in range(1, n_bars + 1):
        sec = section(b)
        o = bt(b)
        fill = sp['fills'].get(b, [])
        ride_on = sp['ride_bars'][0] <= b <= sp['ride_bars'][1]

        # ---- kick, backbeat, toms, crash
        seed(base + b * 10)
        if not dropped(b, 'kick'):
            for beat in range(4):
                t = hum_t(bt(b, beat), HUM)
                note(dr, max(o, t) if b == n_bars else t, 100, KICK,
                     hv(sp['kick'][0 if beat == 0 else 1]))
        if b >= sp['back_from'] and not dropped(b, 'back'):
            for beat in (1, 3):
                t = hum_t(bt(b, beat), HUM)
                note(dr, t, 110, SNARE, clamp(hum_v(sp['snare'][beat], HUM), 88, 100))
                note(dr, t, 110, CLAP, clamp(hum_v(sp['clap'], HUM), 80, 92))
        for step, pitch, v in fill:
            note(dr, hum_t(o + step * S16, HUM), 160, pitch, clamp(hum_v(v, HUM), 80, 100))
        if b == 41:
            note(dr, o, PPQ, CRASH, 80)

        # ---- cymbals: closed hat, open hat, ride
        seed(base + b * 10 + 1)
        if not dropped(b, 'hats'):
            taken = {s for s, _, _ in fill}
            grid = [(s, sp['hat_off']) for s in sp['off_steps']]
            grid += [(s, sp['hat_16']) for s in sp['s16_steps'] if s not in taken]
            if not ride_on:
                grid += [(s, sp['hat_on']) for s in sp['on_steps']]
            for step, vb in sorted(grid):
                note(dr, hum_t(o + step * S16, HUM), 50, HAT, hv(vb))
        for step in sp['oh_steps']:
            note(dr, hum_t(o + step * S16, HUM), 180, OHAT,
                 clamp(hum_v(sp['oh_vel'][sec], HUM), 65, 80))
        if ride_on:
            for beat in range(4):
                if b == 41 and beat == 0:
                    continue
                note(dr, hum_t(bt(b, beat), HUM), int(PPQ * .9), RIDE,
                     hv(sp['ride'][beat % 2]))

        # ---- perc: conga cell only (A from 13, A2)
        if sec in ('A', 'A2') and b >= CONGA_FROM:
            seed(base + b * 10 + 6)
            for step, pitch, v in sp['conga'][(b - 1) % 2]:
                note(pc, hum_t(o + step * S16, HUM), 90, pitch, clamp(hum_v(v, HUM), 70, 85))
    return dr, pc


def step_of(t):
    """(bar, sixteenth step) of a humanized tick."""
    b = bar_of(t)
    return b, round((t - bt(b)) / S16)


def rng(vs):
    return f'{min(vs)}-{max(vs)}' if vs else '-'


def chunks(buf):
    pos, out = 14, []
    while pos < len(buf):
        ln = struct.unpack('>I', buf[pos + 4:pos + 8])[0]
        out.append(buf[pos:pos + 8 + ln])
        pos += 8 + ln
    return out


def audit(sp, nt, n_bars):
    """v3 table ranges and slot ownership; FAIL flags misses."""
    dr, pc = nt[0], nt[5]

    def sel(pitches, steps=None):
        return [(t, v) for t, _, p, v in dr if p in pitches
                and (steps is None or step_of(t)[1] in steps)]

    k1 = [v for t, v in sel({KICK}, {0})]
    k234 = [v for t, v in sel({KICK}, {4, 8, 12})]
    hon = [v for t, v in sel({HAT}, {0, 4, 8, 12})]
    hoff = [v for t, v in sel({HAT}, {2, 10})]
    h16 = [v for t, v in sel({HAT}, {13, 15})]
    ohs = sel({OHAT})
    ohv = [v for _, v in ohs]
    oh_bar = Counter(bar_of(t) for t, _ in ohs)
    ohn = [oh_bar.get(b, 0) for b in range(1, n_bars + 1)]
    sn = [v for _, v in sel({SNARE})]
    cl = [v for _, v in sel({CLAP})]
    ri = sel({RIDE})
    riv = [v for _, v in ri]
    ri_bars = sorted({bar_of(t) for t, _ in ri})
    toms = sel({TOM_LO, TOM_MID, TOM_HI})
    tov = [v for _, v in toms]
    tom_slots = sorted({step_of(t) for t, _ in toms})
    cg = [v for _, _, p, v in pc]
    hat_slots = {step_of(t)[1] for t, _ in sel({HAT})}
    a2_on_hats = [t for t, _ in sel({HAT}, {0, 4, 8, 12}) if 41 <= bar_of(t) <= 56]
    kick_bars = {bar_of(t) for t, _ in sel({KICK})}
    want_toms = sorted((b, s) for b, f in sp['fills'].items() for s, _, _ in f)
    ok = (100 <= min(k1 + k234) and max(k1 + k234) <= 112 and min(k1) > max(k234)
          and 50 <= min(hon) and max(hon) <= 62 and 74 <= min(hoff) and max(hoff) <= 90
          and set(ohn) == {2} and 65 <= min(ohv) and max(ohv) <= 80
          and all(d == 180 for t, d, p, _ in dr if p == OHAT and t + 180 < n_bars * BAR)
          and 88 <= min(sn) and max(sn) <= 100 and 80 <= min(cl) and max(cl) <= 92
          and ri_bars == list(range(41, 57)) and 60 <= min(riv) and max(riv) <= 75
          and tom_slots == want_toms and not a2_on_hats and not hat_slots & {6, 14}
          and all(p in (CONGA_HI, CONGA_LO) for _, _, p, _ in pc)
          and 70 <= min(cg) and max(cg) <= 85
          and min(kick_bars) == 5 and 40 not in kick_bars)
    line = (f'  drums {"OK" if ok else "FAIL"} kick {rng(k1 + k234)} (beat1 {rng(k1)} / '
            f'2-4 {rng(k234)}) | ch on-beat {rng(hon)} off-beat {rng(hoff)} 16th {rng(h16)} | '
            f'open-hat {rng(ohv)} per-bar {min(ohn)}-{max(ohn)} | snare {rng(sn)} clap {rng(cl)} '
            f'| ride {rng(riv)} bars {ri_bars[0]}-{ri_bars[-1]} | tom {rng(tov)} at '
            f'{",".join(f"{b}.{s}" for b, s in tom_slots)} | conga {rng(cg)} n={len(cg)} '
            f'| shaker=0 | ch-hat steps {sorted(hat_slots)}')
    return ok, line


def identical(sid, nt, cc, smf):
    """Non-drum tracks (Bass, Keys, Pad, Tex) vs v2: note/CC lists and MTrk bytes."""
    nt2, cc2, pcs2, n_bars, bpm, title, sf, minor = dh_opus_v2.compose(sid)
    same_lists = all(nt[i] == nt2[i] and cc[i] == cc2[i] for i in range(1, 5))
    mem = build_smf(title, bpm, sf, minor, n_bars, TRACKS, pcs2, nt2, cc2, markers=MARKERS)
    same_mem = chunks(smf)[2:6] == chunks(mem)[2:6]
    path = os.path.join(SK_DIR, sid + '-v2.mid')
    disk = 'missing'
    if os.path.exists(path):
        with open(path, 'rb') as f:
            disk = 'identical' if chunks(smf)[2:6] == chunks(f.read())[2:6] else 'DIFFERENT'
    n = sum(len(nt[i]) for i in range(1, 5))
    ok = same_lists and same_mem and disk != 'DIFFERENT'
    return ok, (f'  v2-identity {"OK" if ok else "FAIL"} Bass/Keys/Pad/Tex note+CC lists '
                f'{"equal" if same_lists else "DIFFER"} ({n} notes) | MTrk bytes vs v2 build '
                f'{"identical" if same_mem else "DIFFERENT"} | vs {os.path.basename(path)} {disk}')


if __name__ == '__main__':
    import sys
    sk = SKETCHES[0]
    nt, cc, pcs, n_bars, bpm, title, sf, minor = compose(sk['sid'])
    smf = build_smf(title, bpm, sf, minor, n_bars, TRACKS, pcs, nt, cc, markers=MARKERS)
    print(f'slot {sk["slot"]:02d} ' + write_smf(os.path.join(SK_DIR, sk['sid'] + '-v3.mid'), smf))
    ok1, line = audit(sk, nt, n_bars)
    ok2, ident = identical(sk['sid'], nt, cc, smf)
    print(line)
    print(ident)
    print(f'  pcs Drums={pcs[0]} Perc={pcs[5]} others={[pcs[i] for i in range(1, 5)]}')
    sys.exit(0 if ok1 and ok2 else 1)
