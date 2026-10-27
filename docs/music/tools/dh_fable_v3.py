"""Fable v3: all ten slots (2, 5, ..., 29) per DEEP_HOUSE_SET_BRIEF `## v3 보정` + `## v3 롤아웃`.

Only the drum/percussion layer changes. Bass/Keys/Pad/Tex events, CCs, form and markers are
taken from dh_fable_v2.compose() untouched; the Drums and Perc tracks are rebuilt here.
  Drums PC16 Tough Kit:
    kick    beats 1-4; beat 1 106-112, beats 2-4 100-105 (split ranges so the accent survives
            humanize); half-kick break bars play beats 1 and 3
    c.hat   eighths; on-beat 50-62 / off-beat 74-90; one sixteenth ghost at 4e (50-62), never 4a;
            no closed hat where the open hat sits; in A2 the ride replaces the on-beat closed hats
    o.hat   & of 2 and & of 4 in every bar whose v2 design has hats (a hats-out break drops them),
            180 ticks, 65-80 brightening intro -> A -> A2
    back    snare 88-100 + clap 80-92 on beats 2 and 4
    ride    A2 only, quarters 60-75
    toms    bars 16/36/56 beat-4 fill: 2 hits (4e, 4a) or 3 (3a, 4e, 4a) by energy, 80-96
    crash   bar 41 downbeat (as v2)
    swing   slots whose v1 cell swings delay the off-beat eighths (closed and open hats) by SW
  Perc PC0 SoCal: optional congas (63/64), two-bar cell of 3-4 hits on free sixteenth slots, 70-85.
  Shaker removed.  Timing humanize +-8 ticks on every hit, velocity +-8 at most inside each range.
  --bars 96 (compose(sid, n_bars=96)) lays the slot on the '## 96마디 시험판' form via dh_fable_v2.form:
  break 49-56 (two four-bar stages), ride/crash from A2 bar 57, toms on 16/48/88 -> {sid}-v3l.mid.
  The default 64-bar output is checked byte-for-byte against {sid}-v3.mid on disk before any 96 run.
"""
import argparse
import copy
import os

from pipeline import BAR, PPQ, SK_DIR, SW, bt, build_smf, hum_t, hum_v, seed, write_smf
import dh_fable_v2 as v2

TRACKS, MARKERS, N_BARS = v2.TRACKS, v2.MARKERS, v2.N_BARS
DRUMS, BASS, KEYS, PAD, TEX, PERC = v2.DRUMS, v2.BASS, v2.KEYS, v2.PAD, v2.TEX, v2.PERC
A_FROM = v2.A_FROM
KICK, SNARE, CLAP, HAT, OPEN_HAT, CRASH = 36, 38, 39, 42, 46, 49
RIDE, TOM_HI, TOM_MID, TOM_LO, CONGA_HI, CONGA_LO = 51, 50, 47, 45, 63, 64
DRUM_PC, PERC_PC = 16, 0
KICK_ACCENT, KICK_BODY = (106, 112), (100, 105)
HAT_ON_V, HAT_OFF_V, GHOST_V = 56, 82, 56
SNARE_V, CLAP_V, RIDE_V, TOM_V, CRASH_V, CONGA_V = 94, 86, 67, 88, 72, 77
OPEN_HAT_BEATS = (1.5, 3.5)
OPEN_HAT_TICKS = 180
GHOST_BEAT = 3.25                            # 4e; 4a (step 15) would choke the & of 4 open hat
FILL_2 = ((3.25, TOM_HI), (3.75, TOM_MID))
FILL_3 = ((2.75, TOM_HI), (3.25, TOM_MID), (3.75, TOM_LO))
MELODIC = (BASS, KEYS, PAD, TEX)

# Per-slot drum colour: open-hat brightness per section, tom fill sizes at the three fill bars and
# an optional conga cell on sixteenth slots that kick, snare, hats and the 4e ghost leave free.
DRUMS_BY_SLOT = {
    2: dict(oh_v={'intro': 69, 'A': 70, 'A2': 73}, fills=(FILL_2, FILL_2, FILL_2), conga=None),
    5: dict(oh_v={'intro': 69, 'A': 72, 'A2': 75}, fills=(FILL_2, FILL_3, FILL_2),
            conga=(((0.75, CONGA_HI), (2.75, CONGA_LO)), ((1.75, CONGA_HI), (2.75, CONGA_LO)))),
    8: dict(oh_v={'intro': 69, 'A': 72, 'A2': 75}, fills=(FILL_2, FILL_3, FILL_2),
            conga=(((0.75, CONGA_HI), (1.75, CONGA_LO)), ((0.75, CONGA_HI), (2.75, CONGA_LO)))),
    11: dict(oh_v={'intro': 69, 'A': 72, 'A2': 75}, fills=(FILL_2, FILL_3, FILL_2),
             conga=(((0.25, CONGA_HI), (2.75, CONGA_LO)), ((0.25, CONGA_HI), (1.75, CONGA_LO)))),
    14: dict(oh_v={'intro': 69, 'A': 72, 'A2': 76}, fills=(FILL_2, FILL_3, FILL_3),
             conga=(((0.75, CONGA_HI), (2.75, CONGA_LO)), ((0.75, CONGA_HI), (1.75, CONGA_LO)))),
    17: dict(oh_v={'intro': 69, 'A': 72, 'A2': 76}, fills=(FILL_2, FILL_3, FILL_3),
             conga=(((0.75, CONGA_HI), (1.75, CONGA_HI), (2.75, CONGA_LO)), ((0.75, CONGA_HI),))),
    20: dict(oh_v={'intro': 69, 'A': 72, 'A2': 75}, fills=(FILL_2, FILL_3, FILL_3),
             conga=(((0.75, CONGA_HI), (2.75, CONGA_LO)), ((2.25, CONGA_LO),))),
    23: dict(oh_v={'intro': 69, 'A': 71, 'A2': 74}, fills=(FILL_2, FILL_3, FILL_2), conga=None),
    26: dict(oh_v={'intro': 69, 'A': 70, 'A2': 73}, fills=(FILL_2, FILL_2, FILL_2), conga=None),
    29: dict(oh_v={'intro': 69, 'A': 70, 'A2': 72}, fills=(FILL_2, FILL_2, FILL_2), conga=None),
}

SKETCHES = [dict(base, **DRUMS_BY_SLOT[base['slot']]) for base in v2.SKETCHES]


def section(fm, bar):
    if bar < A_FROM:
        return 'intro'
    return 'A2' if bar >= fm.a2_from else 'A'


def fill_bars(fm):
    """Tom fill bars: 16, the last A bar, the last A2 bar (16/36/56 at 64, 16/48/88 at 96)."""
    return 16, fm.break_from - 1, fm.outro_from - 1


def clamp(value, bounds):
    return min(bounds[1], max(bounds[0], value))


def compose(sid, n_bars=N_BARS):
    """v2 compose, then Drums/Perc rebuilt. Returns the same tuple shape as v2.compose."""
    fm = v2.form(n_bars)
    sp = next(item for item in SKETCHES if item['sid'] == sid)
    nt, cc, pcs, n_bars, bpm, title, keysig_sf, minor = v2.compose(sid, n_bars)
    pcs = {**pcs, DRUMS: DRUM_PC, PERC: PERC_PC}
    nt[DRUMS], nt[PERC] = [], []
    cc[DRUMS], cc[PERC] = [], []
    seed(23000 + sp['slot'])
    end = bt(n_bars + 1)
    fills = dict(zip(fill_bars(fm), sp['fills']))

    def add(track, bar, beat, ticks, pitch, velocity, jitter=8, swing=False):
        start = bt(bar, beat) + (SW if swing else 0)
        start = max(bt(bar), min(bt(bar + 1) - 1, hum_t(start, jitter)))
        stop = min(start + ticks, bt(bar + 1) - 12, end - 12)
        if stop > start:
            nt[track].append((start, stop - start, pitch, velocity))

    def swung(beat):
        return sp['swing'] and beat % 1 == 0.5

    for bar in range(1, n_bars + 1):
        parts = v2.active_parts(sp, bar, n_bars)
        fill = fills.get(bar, ())
        taken = {beat for beat, _ in fill}
        ride = 'hats' in parts and section(fm, bar) == 'A2' and bar < fm.outro_from
        kick_beats = range(4) if 'kick' in parts else (0, 2) if 'half_kick' in parts else ()
        for beat in kick_beats:
            bounds = KICK_ACCENT if beat == 0 else KICK_BODY
            add(DRUMS, bar, beat, 86, KICK, clamp(hum_v(sum(bounds) // 2, 3), bounds))
        if 'hats' in parts:
            for step in range(8):
                beat = step / 2
                if beat in OPEN_HAT_BEATS or (step % 2 == 0 and ride):
                    continue
                base, jitter = (HAT_ON_V, 6) if step % 2 == 0 else (HAT_OFF_V, 8)
                add(DRUMS, bar, beat, 48, HAT, hum_v(base, jitter), swing=swung(beat))
            if GHOST_BEAT not in taken:
                add(DRUMS, bar, GHOST_BEAT, 40, HAT, hum_v(GHOST_V, 6))
            for beat in OPEN_HAT_BEATS:
                add(DRUMS, bar, beat, OPEN_HAT_TICKS, OPEN_HAT, hum_v(sp['oh_v'][section(fm, bar)], 4),
                    swing=swung(beat))
        if 'back' in parts:
            for beat in (1, 3):
                add(DRUMS, bar, beat, 70, SNARE, hum_v(SNARE_V, 6))
                onset, duration, _, _ = nt[DRUMS][-1]
                nt[DRUMS].append((onset, duration, CLAP, hum_v(CLAP_V, 6)))
        if ride:
            for beat in range(4):
                add(DRUMS, bar, beat, 200, RIDE, hum_v(RIDE_V, 7))
        for beat, pitch in fill:
            add(DRUMS, bar, beat, 90, pitch, hum_v(TOM_V, 8))
        if bar == fm.a2_from:
            add(DRUMS, bar, 0, 240, CRASH, CRASH_V, 0)
        if 'perc' in parts and sp['conga']:
            for beat, pitch in sp['conga'][(bar - A_FROM) % len(sp['conga'])]:
                add(PERC, bar, beat, 60, pitch, hum_v(CONGA_V, 6))
    return nt, cc, pcs, n_bars, bpm, title, keysig_sf, minor


def report(sp, nt, cc, ref_nt, ref_cc, n_bars=N_BARS):
    """Drum ranges, placement rules, layer presence; asserts every brief bound."""
    fm = v2.form(n_bars)

    def vel(pitches, where=None):
        items = [v for t, _, p, v in nt[DRUMS] if p in pitches and (where is None or where(t))]
        return (min(items), max(items)) if items else None

    def within(bounds, pair):
        return pair is not None and bounds[0] <= pair[0] <= pair[1] <= bounds[1]

    def beat_pos(t):
        return t % PPQ

    def on_beat(t):
        return beat_pos(t) < 60 or beat_pos(t) > PPQ - 60                  # +-8 jitter, swing <= SW

    def off_beat(t):
        return abs(beat_pos(t) - PPQ // 2) < 60

    def bar_of(t):
        return t // BAR + 1

    def hats_bars(cond):
        return {bar for bar in range(1, n_bars + 1)
                if 'hats' in v2.active_parts(sp, bar, n_bars) and cond(bar)}

    kick1 = vel({KICK}, lambda t: t % BAR < 60)
    kick234 = vel({KICK}, lambda t: t % BAR >= 60)
    hat_on, hat_off = vel({HAT}, on_beat), vel({HAT}, off_beat)
    ghost = vel({HAT}, lambda t: not on_beat(t) and not off_beat(t))
    oh = vel({OPEN_HAT})
    oh_len = {d for _, d, p, _ in nt[DRUMS] if p == OPEN_HAT}
    oh_count = {bar: sum(1 for t, _, p, _ in nt[DRUMS] if p == OPEN_HAT and bar_of(t) == bar)
                for bar in range(1, n_bars + 1)}
    outside = hats_bars(lambda bar: not fm.break_from <= bar < fm.a2_from)
    oh_outside = sorted({oh_count[bar] for bar in outside})
    oh_break = [oh_count[bar] for bar in range(fm.break_from, fm.a2_from)]
    step15 = [t for t, _, p, _ in nt[DRUMS] if p == HAT and abs(t % BAR - int(3.75 * PPQ)) < 60]
    a2_on_hats = [t for t, _, p, _ in nt[DRUMS] if p == HAT and on_beat(t)
                  and fm.a2_from <= bar_of(t) < fm.outro_from]
    snare, clap, ride = vel({SNARE}), vel({CLAP}), vel({RIDE})
    tom = vel({TOM_HI, TOM_MID, TOM_LO})
    ride_bars = {bar_of(t) for t, _, p, _ in nt[DRUMS] if p == RIDE}
    tom_bars = {bar_of(t) for t, _, p, _ in nt[DRUMS] if p in (TOM_HI, TOM_MID, TOM_LO)}
    conga = [v for _, _, p, v in nt[PERC] if p in (CONGA_HI, CONGA_LO)]
    conga_v = (min(conga), max(conga)) if conga else None
    pad_first = min(t for t, _, _, _ in nt[PAD]) // BAR + 1
    pad_last = max(t for t, _, _, _ in nt[PAD]) // BAR + 1
    crash_bars = [bar_of(t) for t, _, p, _ in nt[DRUMS] if p == CRASH]
    tex_bars = {bar_of(t) for t, _, _, _ in nt[TEX]}
    tex_expected = {bar for bar in range(1, n_bars + 1) if 'tex' in v2.active_parts(sp, bar, n_bars)}
    key_v = (min(v for _, _, _, v in nt[KEYS]), max(v for _, _, _, v in nt[KEYS]))
    total = sum(len(notes) for notes in nt.values())
    last_end = max(t + d for notes in nt.values() for t, d, _, _ in notes)
    same_melodic = all(nt[i] == ref_nt[i] and cc[i] == ref_cc[i] for i in MELODIC)
    checks = [within(KICK_ACCENT, kick1), within(KICK_BODY, kick234),
              within((50, 62), hat_on), within((74, 90), hat_off), within((50, 62), ghost),
              within((65, 80), oh), oh_len == {OPEN_HAT_TICKS}, all(oh_count[bar] >= 1 for bar in outside),
              all(oh_count[bar] == 0 for bar in range(fm.break_from, fm.a2_from)
                  if 'hats' not in v2.active_parts(sp, bar, n_bars)),
              not step15, not a2_on_hats,
              within((88, 100), snare), within((80, 92), clap),
              within((60, 75), ride), ride_bars == set(range(fm.a2_from, fm.outro_from)),
              within((80, 96), tom), tom_bars == set(fill_bars(fm)),
              conga_v is None or within((70, 85), conga_v),
              {p for _, _, p, _ in nt[PERC]} == ({CONGA_HI, CONGA_LO} if sp['conga'] else set()),
              {KICK, SNARE, CLAP, HAT, OPEN_HAT, RIDE, CRASH, TOM_HI, TOM_MID}
              <= {p for _, _, p, _ in nt[DRUMS]}
              <= {KICK, SNARE, CLAP, HAT, OPEN_HAT, RIDE, CRASH, TOM_HI, TOM_MID, TOM_LO},
              crash_bars == [fm.a2_from], pad_first == 1, pad_last == fm.outro_from - 1,
              tex_bars == tex_expected, 72 <= key_v[0] <= key_v[1] <= 92,
              last_end < bt(n_bars + 1), same_melodic]
    assert all(checks), (sp['sid'], checks)

    def rng(pair):
        return 'none' if pair is None else f'{pair[0]}..{pair[1]}'

    return (f"v3-check {sp['sid']} PASS bars={n_bars} kick1={rng(kick1)} kick234={rng(kick234)} "
            f"chat_on={rng(hat_on)} chat_off={rng(hat_off)} chat_4e={rng(ghost)} ohat={rng(oh)} "
            f"ohat_ticks={sorted(oh_len)} ohat/bar_outside_break={oh_outside} "
            f"ohat_break_bars{fm.break_from}-{fm.a2_from - 1}={oh_break} step15_hats={len(step15)} "
            f"A2_onbeat_chats={len(a2_on_hats)} snare={rng(snare)} clap={rng(clap)} ride={rng(ride)} "
            f"ride_bars={min(ride_bars)}-{max(ride_bars)} crash_bar={crash_bars} tom={rng(tom)} "
            f"tom_bars={sorted(tom_bars)} conga={rng(conga_v)} pad_first_bar={pad_first} "
            f"pad_last_bar={pad_last} tex_bars=A+A2:{tex_bars == tex_expected} "
            f"keys_vel={key_v[0]}..{key_v[1]} notes={total} last_note_end_bar={last_end / BAR:.3f} "
            f"non-drum tracks identical to v2: {same_melodic}")


def check_64_identity():
    """Default 64-bar output of every slot must equal the {sid}-v3.mid already on disk."""
    identical = []
    for sketch in SKETCHES:
        nt, cc, pcs, n_bars, bpm, title, keysig_sf, minor = compose(sketch['sid'])
        smf = build_smf(title, bpm, keysig_sf, minor, n_bars, TRACKS, pcs, nt, cc, MARKERS)
        with open(os.path.join(SK_DIR, sketch['sid'] + '-v3.mid'), 'rb') as reference:
            identical.append(reference.read() == smf)
        print(f"64-bar-byte-identity {sketch['sid']} {identical[-1]}")
    print(f"64-bar-byte-identity {'PASS' if all(identical) else 'FAIL'} {sum(identical)}/{len(identical)}")
    assert all(identical), 'default 64-bar MIDI changed'


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Fable v3 drums; --bars 96 writes {sid}-v3l.mid.')
    parser.add_argument('--bars', type=int, choices=(64, 96), default=N_BARS)
    parser.add_argument('sids', nargs='*', help='slot ids; default all ten')
    args = parser.parse_args()
    unknown = set(args.sids) - {item['sid'] for item in SKETCHES}
    if unknown:
        parser.error(f"unknown sid(s): {', '.join(sorted(unknown))}")
    os.makedirs(SK_DIR, exist_ok=True)
    if args.bars != N_BARS:
        check_64_identity()
    fm = v2.form(args.bars)
    suffix = '-v3l.mid' if args.bars == 96 else '-v3.mid'
    for sketch in SKETCHES:
        if args.sids and sketch['sid'] not in args.sids:
            continue
        ref_nt, ref_cc, *_ = copy.deepcopy(v2.compose(sketch['sid'], args.bars))
        nt, cc, pcs, n_bars, bpm, title, keysig_sf, minor = compose(sketch['sid'], args.bars)
        line = report(sketch, nt, cc, ref_nt, ref_cc, args.bars)
        smf = build_smf(title, bpm, keysig_sf, minor, n_bars, TRACKS, pcs, nt, cc, fm.markers)
        print(write_smf(os.path.join(SK_DIR, sketch['sid'] + suffix), smf))
        print(line)
