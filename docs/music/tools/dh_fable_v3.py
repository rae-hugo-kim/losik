"""Fable v3 calibration: slot 14 `dh14-iron-tide` per DEEP_HOUSE_SET_BRIEF `## v3 보정`.

Only the drum/percussion layer changes. Bass/Keys/Pad/Tex events, CCs, form and markers are
taken from dh_fable_v2.compose() untouched; the Drums and Perc tracks are rebuilt here.
  Drums PC16 Tough Kit:
    kick    beats 1-4, 100-112, beat-1 accent +6 (vel jitter +-3 so the table range holds)
    c.hat   eighths; on-beat 50-62 / off-beat 74-90; sixteenth ghosts only at 4e and 4a (50-62);
            no closed hat where the open hat sits
    o.hat   & of 2 and & of 4 every hats bar, 180 ticks, 65-80 brightening intro -> A -> A2
    back    snare 88-100 + clap 80-92 on beats 2 and 4
    ride    A2 only, quarters 60-75
    toms    bars 16/36/56 beat-4 fill: 2-3 hits (50/47/45) 80-96 on free sixteenths (4a-of-3, 4e, 4a)
    crash   bar 41 downbeat (as v2)
  Perc PC0 SoCal: congas only (63/64), two-bar cell of 4 hits on free sixteenth slots, 70-85.
  Shaker removed.  Timing humanize +-8 ticks on every hit.
"""
import copy
import os

from pipeline import BAR, PPQ, SK_DIR, bt, build_smf, hum_t, hum_v, seed, write_smf
import dh_fable_v2 as v2

TRACKS, MARKERS, N_BARS = v2.TRACKS, v2.MARKERS, v2.N_BARS
DRUMS, BASS, KEYS, PAD, TEX, PERC = v2.DRUMS, v2.BASS, v2.KEYS, v2.PAD, v2.TEX, v2.PERC
A2_FROM = v2.A2_FROM
KICK, SNARE, CLAP, HAT, OPEN_HAT, CRASH = 36, 38, 39, 42, 46, 49
RIDE, TOM_HI, TOM_MID, TOM_LO, CONGA_HI, CONGA_LO = 51, 50, 47, 45, 63, 64
DRUM_PC, PERC_PC = 16, 0
OPEN_HAT_BEATS = (1.5, 3.5)
OPEN_HAT_TICKS = 180
GHOST_STEPS = (13, 15)                       # 4e, 4a sixteenths
TOM_FILLS = {16: ((3.25, TOM_HI), (3.75, TOM_MID)),
             36: ((2.75, TOM_HI), (3.25, TOM_MID), (3.75, TOM_LO)),
             56: ((2.75, TOM_HI), (3.25, TOM_MID), (3.75, TOM_LO))}
MELODIC = (BASS, KEYS, PAD, TEX)

SKETCHES = [
    dict(v2.SKETCHES[0],
         kick_v=103, kick_accent=6,
         hat_on_v=56, hat_off_v=82, ghost_v=56,
         oh_v={'intro': 69, 'A': 72, 'A2': 76},
         snare_v=94, clap_v=86, ride_v=67, tom_v=88, crash_v=72,
         # Free sixteenth slots only (kick/snare on beats, hats on eighths, ghosts at 4e/4a).
         conga=(((0.75, CONGA_HI), (2.75, CONGA_LO)),
                ((0.75, CONGA_HI), (1.75, CONGA_LO))),
         conga_v=77),
]


def section(bar):
    if bar < v2.A_FROM:
        return 'intro'
    return 'A2' if bar >= A2_FROM else 'A'


def compose(sid):
    """v2 compose, then Drums/Perc rebuilt. Returns the same tuple shape as v2.compose."""
    sp = next(item for item in SKETCHES if item['sid'] == sid)
    nt, cc, pcs, n_bars, bpm, title, keysig_sf, minor = v2.compose(sid)
    pcs = {**pcs, DRUMS: DRUM_PC, PERC: PERC_PC}
    nt[DRUMS], nt[PERC] = [], []
    cc[DRUMS], cc[PERC] = [], []
    seed(23000 + sp['slot'])
    end = bt(N_BARS + 1)

    def add(track, bar, beat, ticks, pitch, velocity, jitter=8):
        start = max(bt(bar), min(bt(bar + 1) - 1, hum_t(bt(bar, beat), jitter)))
        stop = min(start + ticks, bt(bar + 1) - 12, end - 12)
        if stop > start:
            nt[track].append((start, stop - start, pitch, velocity))

    for bar in range(1, N_BARS + 1):
        parts = v2.active_parts(bar)
        fill = TOM_FILLS.get(bar, ())
        taken = {beat for beat, _ in fill}
        if 'kick' in parts:
            for beat in range(4):
                accent = sp['kick_accent'] if beat == 0 else 0
                add(DRUMS, bar, beat, 86, KICK, hum_v(sp['kick_v'] + accent, 3))
        if 'hats' in parts:
            for step in range(8):
                beat = step / 2
                if beat in OPEN_HAT_BEATS or beat in taken:
                    continue
                base = sp['hat_on_v'] if step % 2 == 0 else sp['hat_off_v']
                add(DRUMS, bar, beat, 48, HAT, hum_v(base, 6 if step % 2 == 0 else 8))
            for step in GHOST_STEPS:
                if step / 4 not in taken:
                    add(DRUMS, bar, step / 4, 40, HAT, hum_v(sp['ghost_v'], 6))
            for beat in OPEN_HAT_BEATS:
                add(DRUMS, bar, beat, OPEN_HAT_TICKS, OPEN_HAT, hum_v(sp['oh_v'][section(bar)], 4))
        if 'back' in parts:
            for beat in (1, 3):
                add(DRUMS, bar, beat, 70, SNARE, hum_v(sp['snare_v'], 6))
                onset, duration, _, _ = nt[DRUMS][-1]
                nt[DRUMS].append((onset, duration, CLAP, hum_v(sp['clap_v'], 6)))
        if 'kick' in parts and section(bar) == 'A2' and bar < v2.OUTRO_FROM:
            for beat in range(4):
                add(DRUMS, bar, beat, 200, RIDE, hum_v(sp['ride_v'], 7))
        for beat, pitch in fill:
            add(DRUMS, bar, beat, 90, pitch, hum_v(sp['tom_v'], 8))
        if bar == A2_FROM:
            add(DRUMS, bar, 0, 240, CRASH, sp['crash_v'], 0)
        if 'perc' in parts:
            for beat, pitch in sp['conga'][(bar - v2.A_FROM) % len(sp['conga'])]:
                add(PERC, bar, beat, 60, pitch, hum_v(sp['conga_v'], 6))
    return nt, cc, pcs, n_bars, bpm, title, keysig_sf, minor


def drum_report(sp, nt, cc, ref_nt, ref_cc):
    def vel(pitches, where=None):
        items = [v for t, _, p, v in nt[DRUMS] if p in pitches and (where is None or where(t))]
        return min(items), max(items)

    def on_beat(t):
        return (t % PPQ) in range(0, 60) or (t % PPQ) > PPQ - 60       # eighth on the beat (+-8 jitter)

    def off_beat(t):
        return abs((t % PPQ) - PPQ // 2) < 60

    def sixteenth(t):
        return not on_beat(t) and not off_beat(t)

    kick = vel({KICK})
    hat_on = vel({HAT}, on_beat)
    hat_off = vel({HAT}, off_beat)
    ghost = vel({HAT}, sixteenth)
    oh = vel({OPEN_HAT})
    oh_per_bar = sorted({sum(1 for t, _, p, _ in nt[DRUMS] if p == OPEN_HAT and bt(bar) <= t < bt(bar + 1))
                         for bar in range(1, N_BARS + 1) if 'hats' in v2.active_parts(bar)})
    oh_len = {d for _, d, p, _ in nt[DRUMS] if p == OPEN_HAT}
    snare, clap, ride = vel({SNARE}), vel({CLAP}), vel({RIDE})
    tom = vel({TOM_HI, TOM_MID, TOM_LO})
    conga = [v for _, _, p, v in nt[PERC] if p in (CONGA_HI, CONGA_LO)]
    conga_v = (min(conga), max(conga))
    ride_bars = {t // BAR + 1 for t, _, p, _ in nt[DRUMS] if p == RIDE}
    tom_bars = {t // BAR + 1 for t, _, p, _ in nt[DRUMS] if p in (TOM_HI, TOM_MID, TOM_LO)}
    same_melodic = all(nt[i] == ref_nt[i] and cc[i] == ref_cc[i] for i in MELODIC)
    checks = [100 <= kick[0] <= kick[1] <= 112,
              50 <= hat_on[0] <= hat_on[1] <= 62, 74 <= hat_off[0] <= hat_off[1] <= 90,
              50 <= ghost[0] <= ghost[1] <= 62,
              65 <= oh[0] <= oh[1] <= 80, oh_per_bar == [2], oh_len == {OPEN_HAT_TICKS},
              88 <= snare[0] <= snare[1] <= 100, 80 <= clap[0] <= clap[1] <= 92,
              60 <= ride[0] <= ride[1] <= 75, ride_bars == set(range(A2_FROM, v2.OUTRO_FROM)),
              80 <= tom[0] <= tom[1] <= 96, tom_bars == set(TOM_FILLS),
              70 <= conga_v[0] <= conga_v[1] <= 85,
              {p for _, _, p, _ in nt[PERC]} == {CONGA_HI, CONGA_LO},
              {p for _, _, p, _ in nt[DRUMS]} == {KICK, SNARE, CLAP, HAT, OPEN_HAT, RIDE, CRASH,
                                                  TOM_HI, TOM_MID, TOM_LO},
              same_melodic]
    assert all(checks), (sp['sid'], checks)
    return (f"drum-range {sp['sid']} PASS kick={kick[0]}..{kick[1]} chat_on={hat_on[0]}..{hat_on[1]} "
            f"chat_off={hat_off[0]}..{hat_off[1]} chat_16th={ghost[0]}..{ghost[1]} "
            f"ohat={oh[0]}..{oh[1]} ohat/bar={oh_per_bar} ohat_ticks={sorted(oh_len)} "
            f"snare={snare[0]}..{snare[1]} clap={clap[0]}..{clap[1]} ride={ride[0]}..{ride[1]} "
            f"tom={tom[0]}..{tom[1]} conga={conga_v[0]}..{conga_v[1]} "
            f"non-drum tracks identical to v2: {same_melodic}")


if __name__ == '__main__':
    os.makedirs(SK_DIR, exist_ok=True)
    for sketch in SKETCHES:
        ref_nt, ref_cc, *_ = copy.deepcopy(v2.compose(sketch['sid']))
        nt, cc, pcs, n_bars, bpm, title, keysig_sf, minor = compose(sketch['sid'])
        line = drum_report(sketch, nt, cc, ref_nt, ref_cc)
        smf = build_smf(title, bpm, keysig_sf, minor, n_bars, TRACKS, pcs, nt, cc, MARKERS)
        print(write_smf(os.path.join(SK_DIR, sketch['sid'] + '-v3.mid'), smf))
        print(line)
