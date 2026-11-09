"""Vivaldi Four Seasons v2 — twelve theme variations in twelve genres, model opus (anthropic/claude-opus-5-5).
Python 3.9 stdlib. Plan: docs/music/vivaldi_opus_v2_plan.md, brief: docs/music/VIVALDI_BRIEF_V2.md.

Theme notes come from vivaldi_data.MOVEMENTS (Mutopia Project; this project assumes CC BY-SA 3.0, the work itself is
public domain). Every SMF carries that attribution as a copyright meta event at tick 0 of the FIRST INSTRUMENT track —
a meta in the conductor track makes Logic 12.4 add an empty track and shifts the `patches={track: ...}` numbers.

Brief §2 is enforced by construction and re-measured by check():
  1. one source voice (`theme_part`); no imitation or doubled source parts; harmony and bass are re-made;
  2. the theme rhythm is re-cut per output bar by ops that must each move a note (sync/late = ① syncopation,
     halftime-like maps = ② note values, thin/pat = ③ skeleton, swing = ④ beat division when it reaches the theme,
     plus dot and meter regroup); `rhythm_ops` must equal the measured set (an op counts from MIN_OP_BARS bars);
     a bar whose onsets are one uniform scaling + shift of its mapped source onsets counts as original rhythm, and
     runs of those are capped at 4 bars;
  3. the effective theme tempo moves >= 15 % and 3/8, 12/8 movements are regrouped into another meter;
  4. accompaniment uses only tones of the bar's chord (bass approach notes excepted), and held accompaniment layers
     never rub (minor 2nd / minor 9th) — the chord's own root -> b9 is the one exemption;
  5. the theme covers 40-60 % of the bars.
Density (brief §3): outside intro/outro a bar with a single sounding layer may not run longer than 2 bars.
Bounce range: Logic bounces up to the end of the last region on the track selected last; load_patches() leaves the
highest-numbered patch track selected, so that track must sound until the final bar (asserted in check()).

    python3 vivaldi_opus_v2.py              # compose + check, write {sid}-v2.mid, measure Suno prompts
    python3 vivaldi_opus_v2.py --check      # compose + check, compare with the MIDI on disk, write nothing
    python3 vivaldi_opus_v2.py --bounce [sid ...]   # then bounce through pipeline.produce(..., patches=...)
"""
import itertools
import json
import math
import os
import re
import struct
import sys
import time
from collections import Counter
from pathlib import Path

from pipeline import PPQ, SK_DIR, hum_t, hum_v, seed, build_smf, varlen, write_smf
import vivaldi_data as V

MODEL = 'opus'
MODEL_ID = 'anthropic/claude-opus-5-5'
ATTRIBUTION = 'Theme: A. Vivaldi, Le quattro stagioni (public domain). Source notes: Mutopia Project, CC BY-SA 3.0'
assert len(ATTRIBUTION.encode()) < 128   # pipeline.parse_smf reads meta lengths as one byte
MIN_OP_BARS = 4

NOTE = {'C': 0, 'C#': 1, 'Db': 1, 'D': 2, 'D#': 3, 'Eb': 3, 'E': 4, 'F': 5, 'F#': 6, 'Gb': 6, 'G': 7,
        'G#': 8, 'Ab': 8, 'A': 9, 'A#': 10, 'Bb': 10, 'B': 11}
# quality: (chord + tension pitch classes above the root, core tones, four-voice voicing pitch classes)
QUAL = {
    '': ((0, 4, 7), (0, 4, 7), (0, 4, 7, 0)),
    'm': ((0, 3, 7), (0, 3, 7), (0, 3, 7, 0)),
    '7': ((0, 4, 7, 10), (0, 4, 7, 10), (0, 4, 7, 10)),
    'maj7': ((0, 4, 7, 11), (0, 4, 7, 11), (0, 4, 7, 11)),
    'm7': ((0, 3, 7, 10), (0, 3, 7, 10), (0, 3, 7, 10)),
    'maj9': ((0, 4, 7, 11, 2), (0, 4, 7, 11), (4, 7, 11, 2)),
    'm9': ((0, 3, 7, 10, 2), (0, 3, 7, 10), (3, 7, 10, 2)),
    '9': ((0, 4, 7, 10, 2), (0, 4, 7, 10), (4, 7, 10, 2)),
    '13': ((0, 4, 7, 10, 2, 9), (0, 4, 10), (4, 10, 2, 9)),
    '9sus': ((0, 5, 7, 10, 2), (0, 5, 7, 10), (5, 10, 2, 7)),
    '7b9': ((0, 4, 7, 10, 1), (0, 4, 7, 10), (4, 7, 10, 1)),
    '7b13': ((0, 4, 10, 8, 1), (0, 4, 10), (4, 8, 10, 1)),
    'm7b5': ((0, 3, 6, 10), (0, 3, 6, 10), (0, 3, 6, 10)),
}


def chord(name):
    m = re.match(r'^([A-G][#b]?)(.*)$', name)
    return NOTE[m.group(1)], m.group(2)


def fifth_iv(q):
    tones = QUAL[q][0]
    return 7 if 7 in tones else 6 if 6 in tones else None


def voicing(root, q, lo, hi, prev, avoid=()):
    """Four voices from the quality's voicing pitch classes inside [lo, hi]; no minor 2nd / minor 9th between any
    pair or against `avoid` (pitches other layers already play in this bar), span <= 17. When that is impossible the
    doubled triad root, then tensions (voicing-order subsets of three, then two) are dropped. Nearest to the previous
    voicing of the same track, else to the band centre."""
    pcs = [(root + iv) % 12 for iv in QUAL[q][2]]
    unique = list(dict.fromkeys(pcs))
    tries = [pcs, unique] + [list(c) for r in (3, 2) for c in itertools.combinations(unique, r)]
    for voice_pcs in tries:
        options = [[p for p in range(lo, hi + 1) if p % 12 == pc] for pc in voice_pcs]
        cands = set()
        for combo in itertools.product(*options):
            cand = tuple(sorted(combo))
            if len(set(cand)) < len(voice_pcs) or cand[-1] - cand[0] > 17 or min(b - a for a, b in zip(cand, cand[1:])) < 2:
                continue
            if any((b - a) in (1, 13) for a, b in itertools.combinations(cand, 2)) or rubs(cand, avoid, root):
                continue
            cands.add(cand)
        if cands:
            break
    assert cands, (root, q, lo, hi)
    center = (lo + hi) / 2
    key = (lambda c: (sum(abs(a - b) for a, b in zip(c, prev)) + abs(sum(c) / len(c) - center), c)) if prev else \
        (lambda c: (abs(sum(c) / len(c) - center), c))
    return min(cands, key=key)


def degree_pc(deg, root, q):
    """Interval above the root for a chord degree name (always a chord tone of the quality)."""
    tones = QUAL[q][0]
    if deg in ('R', '8'):
        return 0
    if deg == '3':
        return 3 if 3 in tones else 4 if 4 in tones else 5
    if deg == '5':
        return fifth_iv(q) or 0
    if deg == '7':
        return 11 if 11 in tones else 10 if 10 in tones else 9 if 9 in tones else 0
    raise AssertionError(deg)


# ---------------------------------------------------------------- source -> output maps (all in quarter notes)
def map_x(mp, x, end=False):
    """Source quarters from the window's first downbeat -> output quarters. A bar-line end point belongs to the bar
    it closes (end=True), so maps whose last anchor is short of S do not stretch bar-final notes."""
    j = math.floor(x / mp['L'] + 1e-9)
    if end and j > 0 and abs(x - j * mp['L']) < 1e-9:
        j -= 1
    q = x - j * mp['L']
    pts = mp['anchors']
    for (q0, o0), (q1, o1) in zip(pts, pts[1:]):
        if q0 - 1e-9 <= q <= q1 + 1e-9:
            return j * mp['S'] + o0 + (q - q0) * (o1 - o0) / (q1 - q0)
    raise AssertionError((q, pts))


def source_notes(s, a, b):
    key = s['key']
    m = V.MOVEMENTS[key]
    t0, t1 = V.bar_tick(key, a), V.bar_tick(key, b + 1)
    lo = 0 if a == 1 else t0
    return [((t - t0) / PPQ, d / PPQ, p) for t, d, p in m['parts'][s['theme_part']] if lo <= t < t1 and d > 1]


def parse_ops(ops):
    out = []
    for op in ops:
        name, _, arg = op.partition(':')
        out.append((name, tuple(float(v) for v in arg.split(',')) if arg else ()))
    return out


def same_rhythm(src, out):
    """True when output onsets are one uniform time scaling plus one shift of the source onsets mapped into the bar
    (tempo- and offset-invariant). One-note bars count as original; 'rest' when both are empty."""
    if not src and not out:
        return 'rest'
    if len(src) != len(out):
        return False
    src, out = sorted(src), sorted(out)
    if len(src) == 1:
        return True
    scale = (out[-1] - out[0]) / (src[-1] - src[0]) if src[-1] > src[0] else None
    if not scale or scale <= 0:
        return False
    return all(abs((b - out[0]) - scale * (a - src[0])) < 1e-6 for a, b in zip(src, out))


def apply_op(notes, name, args, k, bq, raw):
    """Apply one rhythm op to output bar k in place; returns the op label it counts under."""
    label = name.replace('16', '')
    lo_b, hi_b = bq * k, bq * (k + 1)
    in_bar = [n for n in notes if lo_b - 1e-9 <= n['b'] < hi_b - 1e-9]
    if name in ('thin8', 'thin4'):
        g = 0.5 if name == 'thin8' else 1.0
        kept = {}
        for n in in_bar:
            slot = math.floor((n['b'] - lo_b) / g + 1e-9)
            if slot in kept:
                kept[slot]['e'] = max(kept[slot]['e'], n['e'])
                notes.remove(n)
                continue
            kept[slot] = n
            n['b'] = lo_b + slot * g
        if len(kept) == len(in_bar):
            label = name.replace('thin', 'snap')
    elif name in ('sync', 'sync16'):
        amt = 0.5 if name == 'sync' else 0.25
        for n in in_bar:
            if any(abs(n['b'] - lo_b - a) < 1e-6 for a in args):
                prev = [m for m in notes if m['b'] < n['b'] - 1e-6]
                if not prev or prev[-1]['b'] < n['b'] - amt - 1e-6:
                    n['b'] -= amt
    elif name in ('late', 'late16'):
        amt = 0.5 if name == 'late' else 0.25
        for n in in_bar:
            if any(abs(n['b'] - lo_b - a) < 1e-6 for a in args):
                nxt = [m for m in notes if m['b'] > n['b'] + 1e-6]
                if not nxt or nxt[0]['b'] > n['b'] + amt + 0.25 - 1e-6:
                    n['b'] += amt
                    n['e'] += amt
    elif name == 'dot':
        for n in in_bar:
            if abs((n['b'] - lo_b) % 1 - 0.5) < 1e-6:
                prev = [m for m in notes if m['b'] < n['b'] - 1e-6]
                nxt = [m for m in notes if m['b'] > n['b'] + 1e-6]
                if prev and abs(prev[-1]['b'] - (n['b'] - 0.5)) < 1e-6 and (not nxt or nxt[0]['b'] > n['b'] + 0.25 + 1e-6):
                    n['b'] += 0.25
    elif name == 'pat':
        for n in in_bar:
            notes.remove(n)
        for a in args:
            t = lo_b + a
            sounding = [m for m in raw if m['b'] <= t + 1e-6 and t < m['e'] - 1e-6]
            if sounding:
                notes.append(dict(b=t, e=t + 0.5, p=sounding[-1]['p'], legato=True))
    else:
        raise AssertionError(name)
    notes.sort(key=lambda n: n['b'])
    return label


def theme_pass(s, p):
    """One statement in output quarters (0 = downbeat of bar p['at']). Returns notes, per-bar original flags,
    output bar count, {op label: bars it changed}, fired op tokens. A token counts (and fires) in a bar only when
    the bar's result without that token differs from the result with all of the bar's tokens, so an op that a later
    op undoes is not counted."""
    mp, bq = s['mp'], s['bar_q']
    shift = s['tr'] + p['oct']
    src = source_notes(s, *p['src'])
    raw = []
    for x, d, pitch in src:
        b0, e0 = map_x(mp, x), map_x(mp, x + d, end=True)
        if mp['snap']:
            g = mp['snap']
            b0, e0 = round(b0 / g) * g, max(round(e0 / g) * g, round(b0 / g) * g + g)
        raw.append(dict(b=b0, e=e0, p=pitch + shift, legato=False))
    raw.sort(key=lambda n: n['b'])
    raw = [n for i, n in enumerate(raw) if i == 0 or n['b'] > raw[i - 1]['b'] + 1e-6]
    n_out = (p['src'][1] - p['src'][0] + 1) * mp['S'] / bq
    assert abs(n_out - round(n_out)) < 1e-9, (s['sid'], n_out)
    n_out = int(round(n_out))
    notes = [dict(n) for n in raw]
    effective, fired = {}, set()
    for k in range(n_out):
        tokens = p.get('ops_at', {}).get(k, p['ops'][k % len(p['ops'])])
        parsed = parse_ops(tokens)
        assert all(name != 'pat' for name, _ in parsed[1:]), (s['sid'], p['at'], k, 'pat must be the first op of its bar')

        def run(skip):
            state, labels = [dict(n) for n in notes], {}
            for i, (name, args) in enumerate(parsed):
                if i != skip:
                    labels[i] = apply_op(state, name, args, k, bq, raw)
            return state, labels

        full, labels = run(None)
        onsets = [(n['b'], n['p']) for n in full]
        for i, token in enumerate(tokens):
            if [(n['b'], n['p']) for n in run(i)[0]] != onsets:
                effective.setdefault(labels[i], set()).add(k)
                fired.add(token)
        notes = [n for i, n in enumerate(full) if i == 0 or n['b'] > full[i - 1]['b'] + 1e-6]
    for i, n in enumerate(notes):
        nxt = notes[i + 1]['b'] if i + 1 < len(notes) else n_out * bq
        end = nxt - 0.06 if n['legato'] else min(n['e'], nxt - 0.06)
        n['e'] = max(n['b'] + 0.15, min(end, n['b'] + 4.0, n_out * bq - 0.05))
    # reference onsets per output bar = the source onsets the map sends into that bar (correct for uneven maps too)
    ref_by_bar = {}
    for x, _, _ in src:
        ref_by_bar.setdefault(math.floor(map_x(mp, x) / bq + 1e-9), []).append(x)
    orig = []
    for k in range(n_out):
        out = [n['b'] - bq * k for n in notes if bq * k - 1e-9 <= n['b'] < bq * (k + 1) - 1e-9]
        orig.append(same_rhythm(ref_by_bar.get(k, []), out))
    return notes, orig, n_out, effective, fired


def harmonize(s, lead):
    """Chord name per bar: palette chord that best covers the lead notes of the bar (chord tones minus avoid tones),
    with a bonus for the loop chord of that bar; bars without lead take the loop."""
    bq, n_bars = s['bar_q'], s['bars']
    names, prev = [], None
    for bar in range(n_bars):
        u0, u1 = bar * bq, (bar + 1) * bq
        loop_name = s['loop'][bar % len(s['loop'])]
        w = []
        for b, e, pitch in lead:
            ov = min(e, u1) - max(b, u0)
            if ov > 0:
                strong = 1.5 if u0 <= b and abs((b - u0) % 1) < 1e-6 else 1.0
                w.append((pitch % 12, min(ov, 2.0) * strong))
        if not w:
            name = loop_name
        else:
            total = sum(x for _, x in w)
            best = None
            for cand in s['palette']:
                root, q = chord(cand)
                tones, core, _ = QUAL[q]
                score = 0.0
                for pc, x in w:
                    rel = (pc - root) % 12
                    if rel in tones:
                        score += x
                    elif (rel - 1) % 12 in core:
                        score -= 1.5 * x
                score += 0.3 * total if cand == loop_name else 0
                score += 0.1 * total if cand == prev else 0
                if best is None or score > best[0] + 1e-9:
                    best = (score, cand)
            name = best[1]
        prev = name
        names.append(name)
    return names


def clashes(s, chords, lead):
    bad = total = 0
    for b, e, pitch in lead:
        if e - b < 1 - 1e-6:
            continue
        total += 1
        root, q = chord(chords[min(len(chords) - 1, int(((b + e) / 2) // s['bar_q']))])
        tones, core, _ = QUAL[q]
        rel = (pitch - root) % 12
        bad += int(rel not in tones and (rel - 1) % 12 in core)
    return bad, total


def rubs(lows, highs, root):
    count = 0
    for x in lows:
        for y in highs:
            lo, hi = min(x, y), max(x, y)
            if hi - lo == 1 or (hi - lo == 13 and not ((lo - root) % 12 == 0 and (hi - root) % 12 == 1)):
                count += 1
    return count


# ---------------------------------------------------------------- maps and drum names
def mp(L, S, anchors, snap=None, text=''):
    return dict(L=L, S=S, anchors=tuple(anchors), snap=snap, text=text)


KICK, RIM, SNARE, CLAP, HAT, PHAT, OHAT, CRASH, RIDE, BELL = 36, 37, 38, 39, 42, 44, 46, 49, 51, 53
TLO, TMID, THI, TFL = 45, 47, 50, 43


def gm_pat(*items):
    return list(items)


# ---------------------------------------------------------------- the twelve songs
# Pattern elements: chord tracks (pos_q, dur_q, what, vel) with what in 'V' (voicing), 'Vt' (top three), 'Vb' (bottom
# two), 'A0'..'A3' (one voicing tone), a degree 'R','3','5','7','8' or a tuple of degrees, 'app' (bass approach a
# semitone below the next bar's root); drum tracks (pos_q, pitch, vel). A pattern is a list of bars, cycled by bar.
SKETCHES = []


def song(**kw):
    SKETCHES.append(kw)


# 1 ---------------------------------------------------------------- Spring I — Afro highlife
song(key=('spring', 1), sid='vs-spring1-opus', title='Spring I Opus', genre='Afro highlife',
     genre_reason='리토르넬로의 밝은 E장조와 같은 음을 세 번 두드린 뒤 도는 셀, 새소리의 활기가 하이라이프 기타 리프의 콜앤리스폰스와 맞습니다.',
     meter=(4, 4), bpm=134, bars=100, out_key='E major', sf=4, minor=False, tr=0,
     theme_part='solo', theme_window=(1, 13),
     mp=mp(4, 4, ((0, 0), (4, 4)), text='4/4 그대로(템포 +16.5%)'),
     rhythm_ops=['sync', 'dot', 'thin8'], swing=None, hum=8,
     palette=['E', 'A', 'B7', 'C#m', 'F#m7', 'E7'], loop=['E', 'A', 'B7', 'E'],
     tracks=[dict(name='Drums', ch=9, pc=0, role='drums', path='A 0 SoCal'),
             dict(name='Bass', ch=0, pc=33, role='bass', rng=(28, 50), vel=(72, 92), path='A 33 Simple Foundation'),
             dict(name='Rhythm Guitar', ch=1, pc=25, role='acc', rng=(59, 79), vel=(62, 84), path='A 25 어쿠스틱 기타'),
             dict(name='Organ', ch=2, pc=16, role='acc', rng=(52, 71), vel=(52, 68), path='A 16 톤휠 오르간'),
             dict(name='Theme Guitar', ch=3, pc=24, role='lead', vel=(70, 92), path='A 24 Classical Acoustic Guitar'),
             dict(name='Horns', ch=4, pc=61, role='lead', rng=(60, 79), vel=(70, 94), path='A 61 Sugar Hill')],
     patterns=dict(
         dr_intro=[gm_pat(*[(i / 2, HAT, 70 if i % 2 else 56) for i in range(8)], (0, BELL, 78), (1.5, BELL, 70), (2.5, BELL, 74))],
         dr_groove=[gm_pat((0, KICK, 102), (1.75, KICK, 88), (2.5, KICK, 96), (1, RIM, 82), (3, RIM, 86),
                           *[(i / 2, HAT, 72 if i % 2 else 58) for i in range(8)], (0, BELL, 76), (1.5, BELL, 70), (2.5, BELL, 72), (3.5, BELL, 66)),
                    gm_pat((0, KICK, 102), (2.5, KICK, 96), (3.25, KICK, 84), (1, RIM, 82), (3, SNARE, 90),
                           *[(i / 2, HAT, 72 if i % 2 else 58) for i in range(8)], (0, BELL, 76), (1.5, BELL, 70), (3, BELL, 72))],
         dr_break=[gm_pat((0, KICK, 96), (2.5, KICK, 86), (1, RIM, 70), (3, RIM, 72), (0, BELL, 70), (1.5, BELL, 64), (2.5, BELL, 66), (3.5, BELL, 60))],
         dr_fill=[gm_pat((0, KICK, 100), (1, RIM, 80), (2, SNARE, 84), (2.5, THI, 86), (3, TMID, 90), (3.5, TLO, 94), (3.75, TFL, 98),
                         *[(i / 2, HAT, 64) for i in range(4)])],
         dr_crash=[gm_pat((0, KICK, 104), (0, CRASH, 96), (1, RIM, 82), (2.5, KICK, 92), (3, RIM, 84), *[(i / 2, HAT, 66) for i in range(1, 8)])],
         bass=[[(0, .7, 'R', 88), (1, .45, '5', 78), (1.5, .45, '8', 80), (2.5, .45, 'R', 84), (3, .45, '3', 78), (3.5, .45, '5', 80)],
               [(0, .7, 'R', 88), (1.5, .45, '5', 80), (2, .45, '8', 78), (2.5, .45, '5', 82), (3.5, .45, 'app', 76)]],
         skank=[[(0.5, .35, 'Vt', 72), (1.5, .35, 'Vt', 74), (2.5, .35, 'Vt', 72), (3.5, .35, 'Vt', 76), (3.75, .2, 'Vt', 64)]],
         skank_sparse=[[(1.5, .35, 'Vt', 70), (3.5, .35, 'Vt', 72)]],
         organ=[[(0, 3.9, 'V', 60)]],
         horn_stab=[[(0, .3, 'Vt', 86), (1.5, .3, 'Vt', 80), (2, .3, 'Vt', 84), (3, .6, 'Vt', 88)]]),
     parts={'Drums': [(1, 4, 'dr_intro'), (5, 56, 'dr_groove'), (57, 64, 'dr_break'), (65, 96, 'dr_groove'), (97, 100, 'dr_break')],
            'Bass': [(9, 56, 'bass'), (57, 64, 'bass'), (65, 98, 'bass')],
            'Rhythm Guitar': [(5, 56, 'skank'), (57, 64, 'skank_sparse'), (65, 100, 'skank')],
            'Organ': [(9, 29, 'organ'), (34, 96, 'organ')],
            'Horns': [(30, 33, 'horn_stab'), (47, 56, 'horn_stab'), (86, 92, 'horn_stab')]},
     fills={'Drums': {16: 'dr_fill', 29: 'dr_fill', 46: 'dr_fill', 56: 'dr_fill', 64: 'dr_fill', 85: 'dr_fill', 17: 'dr_crash', 34: 'dr_crash', 65: 'dr_crash'}},
     passes=[dict(at=17, src=(1, 13), track='Theme Guitar', oct=-12, ops=[['sync:3.5'], ['dot'], ['thin8']]),
            dict(at=34, src=(1, 13), track='Horns', oct=-12, ops=[['dot'], ['sync:3.5'], ['thin8']]),
            dict(at=65, src=(1, 13), track='Theme Guitar', oct=0, ops=[['thin8'], ['sync:3.5'], ['dot']]),
            dict(at=78, src=(1, 8), track='Horns', oct=-12, ops=[['sync:3.5'], ['thin8'], ['dot']])],
     motifs=[dict(track='Theme Guitar', at=(9, 11, 13, 15, 47, 49, 51, 53, 55, 87, 89, 91), span=2,
                 notes=((0, .5, 71), (.5, .5, 73), (1, 1, 76), (2.5, .5, 73), (3, .9, 71), (4.5, .5, 68), (5, .5, 71), (5.5, 1.5, 73)))],
     markers=[(1, 'intro'), (9, 'groove'), (17, 'theme 1'), (30, 'horns'), (34, 'theme 2'), (47, 'call & response'), (57, 'break'),
              (65, 'theme 3'), (78, 'theme 4'), (86, 'shout'), (93, 'outro')],
     intro_bars=8, outro_from=93, patches={},
     notes='하이라이프: 반복음 셀을 나일론 기타가 부르고 Sugar Hill 브라스가 같은 셀로 받습니다.')

# 2 ---------------------------------------------------------------- Spring II — Bossa nova
song(key=('spring', 2), sid='vs-spring2-opus', title='Spring II Opus', genre='Bossa nova',
     genre_reason='잠든 목동의 Largo, 사각이는 점음 반주, 느긋한 C♯ 단조 선율이 보사노바의 속삭이는 기타 컴핑·플루트 선율과 같은 온도입니다.',
     meter=(4, 4), bpm=80, bars=60, out_key='C♯ minor', sf=4, minor=True, tr=0,
     theme_part='solo', theme_window=(2, 10),
     mp=mp(3, 4, ((0, 0), (1, 1.5), (2, 3), (3, 4)), snap=0.25, text='3/4 → 4/4 보사 3+3+2 재배열'),
     rhythm_ops=['regroup', 'sync', 'late', 'thin4'], swing=None, hum=7,
     palette=['C#m9', 'F#9', 'Amaj7', 'G#7b9', 'D#m7b5', 'Emaj7', 'Bmaj7'], loop=['C#m9', 'C#m9', 'D#m7b5', 'G#7b9'],
     tracks=[dict(name='Drums', ch=9, pc=0, role='drums', path='A 0 SoCal'),
             dict(name='Bass', ch=0, pc=32, role='bass', rng=(28, 50), vel=(64, 84), path='A 32 루트 업라이트'),
             dict(name='Guitar', ch=1, pc=24, role='acc', rng=(52, 72), vel=(58, 80), path='A 24 Classical Acoustic Guitar'),
             dict(name='Strings', ch=2, pc=48, role='acc', rng=(55, 76), vel=(48, 64), path='A 48 Kensington'),
             dict(name='EP', ch=3, pc=4, role='lead', vel=(62, 84), path='A 4 Deluxe Classic'),
             dict(name='Flute', ch=4, pc=73, role='lead', vel=(62, 86), path='B Flute Solo', patch='Flute Solo')],
     patterns=dict(
         dr_bossa=[gm_pat((0, KICK, 74), (1.5, KICK, 62), (2, KICK, 72), (3.5, KICK, 60), (0, RIM, 64), (0.75, RIM, 58), (1.5, RIM, 66), (2.5, RIM, 62), (3.25, RIM, 58),
                          *[(i / 2, HAT, 48 if i % 2 else 40) for i in range(8)]),
                   gm_pat((0, KICK, 74), (1.5, KICK, 62), (2, KICK, 72), (3.5, KICK, 60), (0.5, RIM, 60), (1.5, RIM, 64), (2.5, RIM, 62), (3, RIM, 58),
                          *[(i / 2, HAT, 48 if i % 2 else 40) for i in range(8)])],
         dr_light=[gm_pat((0.75, RIM, 52), (2.5, RIM, 50), *[(i / 2, HAT, 42 if i % 2 else 36) for i in range(8)])],
         bass=[[(0, 1.4, 'R', 78), (1.5, .45, '5', 70), (2, 1.4, '5', 74), (3.5, .45, 'app', 66)]],
         gtr=[[(0, .45, 'V', 70), (1, .45, 'V', 64), (1.5, .45, 'V', 68), (2.5, .45, 'V', 66), (3.5, .45, 'V', 70)],
              [(0.5, .45, 'V', 66), (1.5, .45, 'V', 70), (2, .45, 'V', 64), (3, .45, 'V', 68)]],
         strings=[[(0, 3.9, 'V', 56)]]),
     parts={'Drums': [(5, 8, 'dr_light'), (9, 51, 'dr_bossa'), (52, 56, 'dr_light')],
            'Bass': [(5, 56, 'bass')],
            'Guitar': [(1, 60, 'gtr')],
            'Strings': [(5, 17, 'strings'), (26, 60, 'strings')]},
     fills={},
     passes=[dict(at=9, src=(2, 10), track='Flute', oct=0,
                 ops=[['sync:3'], ['thin4'], ['sync:1.5'], ['thin4'], ['late:0'], [], ['sync:3'], ['late:0'], ['sync:1.5']]),
            dict(at=26, src=(2, 10), track='EP', oct=-12,
                 ops=[['late:1.5'], ['thin4'], ['sync:3'], ['late:1.5'], ['sync:3'], ['late:0'], ['late:1.5'], [], []]),
            dict(at=43, src=(2, 10), track='Flute', oct=0,
                 ops=[['sync:1.5'], ['thin4'], ['late:0', 'sync:3'], ['thin4'], ['late:1.5'], ['late:0', 'sync:3'], ['sync:1.5'], [], ['sync:3']])],
     motifs=[dict(track='EP', at=(18, 20, 22, 24), span=2,
                  notes=((0.5, 1, 64), (1.5, .5, 66), (2, 1.5, 68), (4, 1, 71), (5.5, .5, 68), (6, 1.75, 66))),
             dict(track='Flute', at=(35, 37, 39, 41), span=2,
                  notes=((0, 1.5, 76), (1.5, .5, 75), (2, 1, 73), (3.5, .5, 71), (4.5, 1.5, 68), (6, 1.75, 71))),
             dict(track='Flute', at=(57, 59), span=2,
                  notes=((0.5, 1.5, 73), (2, 1, 71), (3, 1, 68), (4.5, 3.4, 64)))],
     markers=[(1, 'intro'), (9, 'theme 1'), (18, 'interlude'), (26, 'theme 2'), (35, 'dialogue'), (43, 'theme 3'), (52, 'outro')],
     intro_bars=8, outro_from=52, patches={6: 'Flute Solo'},
     notes='보사노바: 3/4 선율을 3+3+2 로 다시 묶어 플루트가 부르고, 기타 컴핑이 2마디 보사 셀을 돕니다.')

# 3 ---------------------------------------------------------------- Spring III — Celtic slip jig
song(key=('spring', 3), sid='vs-spring3-opus', title='Spring III Opus', genre='Celtic slip jig',
     genre_reason='시칠리아나 춤의 목가적 길고–짧은 리듬과 지속음 위 춤곡이 켈틱 무곡과 같은 계열이고, 12/8 의 네 박을 9/8 슬립 지그 세 박으로 다시 묶습니다.',
     meter=(9, 8), bpm=174, bars=116, out_key='D major', sf=2, minor=False, tr=-2,
     theme_part='solo', theme_window=(1, 12),
     mp=mp(6, 9, ((0, 0), (1.5, 1.5), (3, 4.5), (4.5, 6), (6, 9)), snap=0.5, text='12/8 한 마디 → 9/8 두 마디, 둘째·넷째 점4분을 두 배로'),
     rhythm_ops=['regroup', 'sync', 'late', 'pat'], swing=None, hum=8,
     palette=['D', 'G', 'A', 'Bm', 'Em', 'A7', 'F#m'], loop=['D', 'D', 'G', 'A'],
     tracks=[dict(name='Bass', ch=0, pc=32, role='bass', rng=(28, 50), vel=(62, 82), path='A 32 루트 업라이트'),
             dict(name='Percussion', ch=9, pc=0, role='drums', path='A 0 SoCal (탐·림 보드란 대용)'),
             dict(name='Bouzouki', ch=1, pc=25, role='acc', rng=(50, 69), vel=(60, 82), path='B Irish Bouzouki', patch='Irish Bouzouki'),
             dict(name='Harp', ch=2, pc=24, role='lead', rng=(55, 79), vel=(60, 84), path='B Celtic Harp', patch='Celtic Harp'),
             dict(name='Whistle', ch=3, pc=73, role='lead', vel=(64, 88), path='B Celtic Tin Whistle', patch='Celtic Tin Whistle')],
     patterns=dict(
         perc=[gm_pat(*[x for g, acc in ((0, 96), (1.5, 76), (3, 82)) for x in ((g, TFL, acc), (g + .5, RIM, 54), (g + 1, TLO, 62))])],
         perc_soft=[gm_pat(*[x for g, acc in ((0, 72), (1.5, 58), (3, 62)) for x in ((g, TFL, acc), (g + 1, RIM, 46))])],
         bass=[[(0, 1.4, 'R', 76), (3, 1.4, '5', 70)]],
         bass_drone=[[(0, 4.4, 'R', 66)]],
         bzk=[[(0, 1.0, 'V', 74), (1.5, .45, 'Vt', 64), (2, .45, 'Vt', 66), (3, 1.0, 'V', 72), (4, .45, 'Vt', 64)]],
         bzk_open=[[(0, 4.3, 'V', 64)]],
         harp_arp=[[(i / 2, .45, 'A%d' % (i % 4 if i < 4 else (8 - i) % 4), 66) for i in range(9)]]),
     parts={'Bass': [(1, 8, 'bass_drone'), (9, 112, 'bass'), (113, 116, 'bass_drone')],
            'Percussion': [(5, 8, 'perc_soft'), (9, 108, 'perc'), (109, 112, 'perc_soft')],
            'Bouzouki': [(1, 116, 'bzk')],
            'Harp': [(41, 48, 'harp_arp'), (73, 84, 'harp_arp'), (97, 108, 'harp_arp')]},
     fills={},
     passes=[dict(at=17, src=(1, 12), track='Whistle', oct=0, ops=[['late:1.5'], ['sync:1.5']]),
            dict(at=49, src=(1, 12), track='Harp', oct=-12, ops=[['pat:0,1.5,3'], ['sync:1.5'], ['late:1.5'], ['pat:0,1,1.5,3,3.5']]),
            dict(at=85, src=(1, 6), track='Whistle', oct=0, ops=[['late:1.5'], ['pat:0,1.5,3']])],
     motifs=[dict(track='Harp', at=(9, 11, 13, 15), span=2,
                  notes=((0, 1, 74), (1, .5, 76), (1.5, 1.5, 78), (3, 1, 76), (4, .5, 74), (4.5, 1, 71), (5.5, .5, 69), (6, 1.5, 71), (7.5, 1, 74))),
             dict(track='Whistle', at=(73, 75, 77, 79, 81, 83, 97, 99, 101, 103, 105, 107), span=2,
                  notes=((0, .5, 86), (.5, .5, 85), (1, .5, 83), (1.5, 1, 81), (2.5, .5, 83), (3, 1.5, 85), (4.5, .5, 86), (5, .5, 88), (5.5, 1, 86), (6.5, .5, 85), (7, 1.5, 81))),
             dict(track='Whistle', at=(109, 111, 113, 115), span=2,
                  notes=((0, 1.5, 81), (1.5, 1.5, 78), (3, 1.5, 74), (4.5, 1.5, 76), (6, 2.9, 74)))],
     markers=[(1, 'intro'), (9, 'harp air'), (17, 'theme 1'), (41, 'turn'), (49, 'theme 2'), (73, 'jig A'), (85, 'theme 3'), (97, 'jig B'), (109, 'outro')],
     intro_bars=8, outro_from=109, patches={3: 'Irish Bouzouki', 4: 'Celtic Harp', 5: 'Celtic Tin Whistle'},
     notes='켈틱 슬립 지그: 시칠리아나를 D장조 9/8 로 옮겨 틴 휘슬이 부르고 하프가 받으며, 부주키가 드론 컴핑을 합니다.')

# 4 ---------------------------------------------------------------- Summer I — Trip-hop
song(key=('summer', 1), sid='vs-summer1-opus', title='Summer I Opus', genre='Trip-hop',
     genre_reason='무더위에 지친 나른함, 긴 쉼표 사이의 한숨 동기, 무거운 G 단조가 느리고 무거운 브레이크비트와 흐릿한 질감의 트립합과 맞습니다.',
     meter=(4, 4), bpm=84, bars=64, out_key='G minor', sf=-2, minor=True, tr=0,
     theme_part='violin1', theme_window=(1, 30),
     mp=mp(1.5, 2, ((0, 0), (0.5, 1.0), (1.0, 1.5), (1.5, 2)), snap=0.25, text='3/8 두 마디 → 4/4 한 마디, 첫 8분을 4분으로 늘려 한숨을 뒤로'),
     rhythm_ops=['regroup', 'sync', 'late', 'thin8', 'swing'], swing=(0.25, 34), hum=10,
     palette=['Gm9', 'Ebmaj7', 'Cm7', 'D7b9', 'Bbmaj7', 'Am7b5', 'Gm'], loop=['Gm9', 'Gm9', 'Ebmaj7', 'D7b9'],
     tracks=[dict(name='Drums', ch=9, pc=0, role='drums', path='A 0 SoCal'),
             dict(name='Sub Bass', ch=0, pc=39, role='bass', rng=(28, 46), vel=(70, 90), path='A 39 Taureg Moon Bass'),
             dict(name='Piano', ch=1, pc=3, role='acc', rng=(50, 72), vel=(56, 78), path='A 3 Dark Lo-Fi Piano'),
             dict(name='Strings', ch=2, pc=49, role='acc', rng=(55, 79), vel=(46, 64), path='A 49 Bloomsbury'),
             dict(name='Vibes', ch=3, pc=11, role='lead', vel=(60, 82), path='A 11 Vibraphone'),
             dict(name='Oboe', ch=4, pc=68, role='lead', vel=(60, 84), path='B Oboe', patch='Oboe')],
     patterns=dict(
         dr=[gm_pat((0, KICK, 104), (1.75, KICK, 86), (2.5, KICK, 96), (1, SNARE, 94), (3, SNARE, 98), (2.25, SNARE, 44), (3.75, SNARE, 40),
                    *[(i / 4, HAT, 52 if i % 2 else 64) for i in range(16) if i not in (4, 12)]),
             gm_pat((0, KICK, 104), (0.75, KICK, 82), (2.5, KICK, 96), (1, SNARE, 94), (3, SNARE, 98), (1.75, SNARE, 42),
                    *[(i / 4, HAT, 52 if i % 2 else 64) for i in range(16) if i not in (4, 12, 15)], (3.75, OHAT, 66))],
         dr_half=[gm_pat((0, KICK, 100), (2, SNARE, 92), *[(i / 2, HAT, 56) for i in range(8)])],
         bass=[[(0, 1.4, 'R', 84), (2.5, .9, 'R', 80), (3.5, .45, '5', 74)], [(0, 2.4, 'R', 84), (3, .9, '5', 76)]],
         piano=[[(0, 1.9, 'V', 70), (2.75, 1.1, 'Vt', 62)], [(0.5, 1.4, 'Vt', 64), (2, 1.9, 'V', 68)]],
         strings=[[(0, 3.9, 'V', 56)]]),
     parts={'Drums': [(5, 27, 'dr'), (28, 36, 'dr_half'), (37, 60, 'dr')],
            'Sub Bass': [(9, 60, 'bass')],
            'Piano': [(1, 64, 'piano')],
            'Strings': [(1, 12, 'strings'), (28, 36, 'strings'), (52, 64, 'strings')]},
     fills={},
     passes=[dict(at=13, src=(1, 30), track='Oboe', oct=0,
                 ops=[['sync:3'], ['thin8'], ['late:0'], ['sync:3'], ['late:0'], ['sync:3'], ['late:0'], ['sync:3'],
                      ['sync:1'], [], ['thin8'], ['sync:3'], ['sync:3'], ['thin8'], ['sync:3']]),
            dict(at=37, src=(1, 30), track='Vibes', oct=-12,
                 ops=[['sync:3'], ['sync:3'], ['sync:3'], ['late:0'], ['sync:3'], ['late:0'], ['sync:1'], ['sync:3'],
                      ['late:0'], [], ['sync:3'], ['sync:1'], ['sync:3'], ['thin8'], ['sync:1']])],
     motifs=[dict(track='Vibes', at=(9, 11, 29, 31, 33, 35), span=2,
                  notes=((0.5, .5, 74), (1, 1.5, 70), (3, .75, 69), (4.5, .5, 67), (5, 1, 70), (6, 1.9, 62))),
             dict(track='Oboe', at=(52, 54, 56, 58, 60, 62), span=2,
                 notes=((0, 1.5, 70), (1.5, .5, 69), (2, 2, 67), (4.5, 1, 65), (5.5, .5, 62), (6, 1.9, 67))),
             dict(track='Oboe', at=(64,), span=1, notes=((0, 3.9, 67),))],
     markers=[(1, 'intro'), (9, 'groove'), (13, 'theme 1'), (28, 'haze'), (37, 'theme 2'), (52, 'oboe coda'), (57, 'outro')],
     intro_bars=8, outro_from=57, patches={6: 'Oboe'},
     notes='트립합: 3/8 한숨 동기를 두 마디씩 4/4 로 묶어 오보에가 늘어지게 부르고, 무거운 브레이크비트가 받칩니다.')

# 5 ---------------------------------------------------------------- Summer II — Cinematic neo-classical
song(key=('summer', 2), sid='vs-summer2-opus', title='Summer II Opus', genre='Cinematic neo-classical',
     genre_reason='Adagio 독주가 멀리서 오는 천둥에 끊기는 구조가 영화음악의 피아노·현악 서사와 팀파니 천둥으로 그대로 옮겨집니다.',
     meter=(4, 4), bpm=63, bars=48, out_key='G minor', sf=-2, minor=True, tr=0,
     theme_part='solo', theme_window=(1, 8),
     mp=mp(4, 4, ((0, 0), (4, 4)), text='4/4 그대로(템포 +40%)'),
     rhythm_ops=['sync', 'late', 'pat'], swing=None, hum=7,
     palette=['Gm', 'Cm', 'Eb', 'D7', 'Bb', 'F', 'Am7b5', 'Gm9'], loop=['Gm', 'Eb', 'Cm', 'D7'],
     tracks=[dict(name='Piano', ch=0, pc=2, role='acc', rng=(43, 72), vel=(54, 78), path='A 2 Concert Grand'),
             dict(name='Strings', ch=1, pc=48, role='acc', rng=(55, 79), vel=(46, 70), path='A 48 Kensington'),
             dict(name='Cellos', ch=2, pc=42, role='bass', rng=(36, 55), vel=(56, 80), path='A 42 Studio Cellos'),
             dict(name='Timpani', ch=3, pc=47, role='acc', rng=(38, 55), vel=(40, 112), path='B Timpani', patch='Timpani'),
             dict(name='Solo Violin', ch=4, pc=40, role='lead', vel=(60, 88), path='C Violins 1 + Violin (Arco)', patch=('Violins 1', 'Violin (Arco)'))],
     patterns=dict(
         ost=[[(i / 2, .45, 'A%d' % (0, 1, 2, 3, 2, 1, 0, 1)[i], 62) for i in range(8)]],
         ost_low=[[(0, 1.9, 'Vb', 58), (2, 1.9, 'Vb', 56)]],
         strings=[[(0, 3.9, 'V', 58)]],
         strings_trem=[[(i / 4, .2, 'Vt', 48 + i * 2) for i in range(16)]],
         cello=[[(0, 1.9, 'R', 70), (2, 1.9, '5', 64)]],
         cello_hold=[[(0, 3.9, 'R', 66)]],
         thunder=[[(i / 4, .2, 'R', 40 + i * 4) for i in range(16)]],
         thunder_hit=[[(0, .9, 'R', 96), (3, .9, '5', 70)]]),
     parts={'Piano': [(1, 16, 'ost'), (17, 20, 'ost_low'), (21, 28, 'ost_low'), (29, 40, 'ost'), (41, 44, 'ost_low'), (45, 48, 'ost')],
            'Strings': [(5, 16, 'strings'), (17, 20, 'strings_trem'), (21, 40, 'strings'), (41, 44, 'strings_trem'), (45, 48, 'strings')],
            'Cellos': [(5, 16, 'cello'), (17, 20, 'cello_hold'), (21, 40, 'cello'), (41, 44, 'cello_hold'), (45, 47, 'cello')],
            'Timpani': [(12, 12, 'thunder'), (17, 20, 'thunder'), (21, 21, 'thunder_hit'), (24, 24, 'thunder'), (33, 33, 'thunder_hit'),
                        (36, 36, 'thunder'), (41, 44, 'thunder'), (45, 45, 'thunder_hit')]},
     fills={},   # bars 12/24/36 = the rest bar inside each theme pass, where the original has its thunder
     passes=[dict(at=9, src=(1, 8), track='Solo Violin', oct=0,
                 ops=[['late:0'], ['sync:2'], ['late:1'], [], ['late:2'], ['pat:0,1,2,3'], ['sync:3.5'], ['sync:1']]),
             dict(at=21, src=(1, 8), track='Piano', oct=0,
                 ops=[['sync:3.5'], ['late:0'], ['pat:0,1'], [], ['pat:0,1,2,3'], ['sync:3.5'], ['late:0'], ['late:2']]),
             dict(at=33, src=(1, 8), track='Solo Violin', oct=0,
                 ops=[['late:0', 'sync:3.5'], ['late:2'], ['late:1'], [], ['late:0'], ['pat:0,1,2,3'], ['sync:3.5'], ['late:1']])],
     motifs=[dict(track='Solo Violin', at=(29, 31), span=2,
                  notes=((0, 2, 74), (2, 1, 72), (3, 1, 70), (4, 1.5, 69), (5.5, .5, 67), (6, 1.9, 66))),
             dict(track='Solo Violin', at=(45, 47), span=2,
                  notes=((0, 2, 70), (2, 2, 69), (4, 3.9, 67)))],
     markers=[(1, 'intro'), (9, 'theme 1'), (17, 'thunder'), (21, 'theme 2'), (29, 'build'), (33, 'theme 3'), (41, 'storm'), (45, 'outro')],
     intro_bars=8, outro_from=45, patches={4: 'Timpani', 5: ('Violins 1', 'Violin (Arco)')},
     notes='시네마틱: 솔로 바이올린이 Adagio 를 부르고, 원곡의 천둥 마디는 팀파니 롤·현 트레몰로로 옮깁니다.')

# 6 ---------------------------------------------------------------- Summer III — Symphonic metal
song(key=('summer', 3), sid='vs-summer3-opus', title='Summer III Opus', genre='Symphonic metal',
     genre_reason='폭풍 프레스토의 G 연타 트레몰로와 쏟아지는 음계는 메탈의 트레몰로 피킹·더블 킥과 같은 에너지이고, 합창·현악이 폭풍의 규모를 더합니다.',
     meter=(4, 4), bpm=180, bars=136, out_key='G minor', sf=-2, minor=True, tr=0,
     theme_part='violin1', theme_window=(1, 20),
     mp=mp(3, 8, ((0, 0), (1, 3), (2, 6), (3, 8)), text='3/4 한 마디 → 4/4 두 마디, 세 박을 3+3+2 4분으로'),
     rhythm_ops=['regroup', 'pat', 'sync'], swing=None, hum=6,
     palette=['Gm', 'Eb', 'F', 'D', 'Cm', 'Bb'], loop=['Gm', 'Gm', 'Eb', 'F'],
     tracks=[dict(name='Drums', ch=9, pc=8, role='drums', path='A 8 복고풍 록'),
             dict(name='Bass', ch=0, pc=34, role='bass', rng=(28, 50), vel=(80, 100), path='A 34 Punchy Bottom'),
             dict(name='Rhythm Guitar', ch=1, pc=30, role='acc', rng=(40, 64), vel=(80, 104), path='A 30 하드 록'),
             dict(name='Lead Guitar', ch=2, pc=26, role='lead', vel=(84, 106), path='A 26 하드 록'),
             dict(name='Strings', ch=3, pc=49, role='acc', rng=(55, 79), vel=(56, 76), path='A 49 Bloomsbury'),
             dict(name='Synth Lead', ch=4, pc=81, role='lead', vel=(76, 98), path='A 81 The Final Lead'),
             dict(name='Choir', ch=5, pc=52, role='acc', rng=(55, 76), vel=(58, 80), path='B Mixed Choir', patch='Mixed Choir')],
     patterns=dict(
         dr=[gm_pat(*[(i / 2, KICK, 100 if i % 2 == 0 else 92) for i in range(8)], (1, SNARE, 106), (3, SNARE, 108),
                    *[(i / 2, RIDE, 70 if i % 2 else 80) for i in range(8)])],
         dr_crash=[gm_pat(*[(i / 2, KICK, 100 if i % 2 == 0 else 92) for i in range(8)], (1, SNARE, 106), (3, SNARE, 108), (0, CRASH, 104),
                          *[(i / 2, RIDE, 72) for i in range(1, 8)])],
         dr_half=[gm_pat((0, KICK, 104), (1.5, KICK, 94), (2, SNARE, 108), (3.5, KICK, 92), *[(i / 2, HAT, 74) for i in range(8)])],
         dr_fill=[gm_pat((0, KICK, 102), (1, SNARE, 104), (2, THI, 98), (2.5, TMID, 100), (3, TLO, 104), (3.5, TFL, 108))],
         bass=[[(i / 2, .4, 'R', 92 if i % 2 == 0 else 84) for i in range(8)]],
         bass_half=[[(0, 1.4, 'R', 96), (1.5, .4, 'R', 88), (3.5, .4, '5', 86)]],
         chug=[[(i / 2, .3, ('R', '5'), 98 if i in (0, 3, 6) else 86) for i in range(8)]],
         chug_half=[[(0, 1.4, ('R', '5', '8'), 102), (1.5, .3, ('R', '5'), 90), (3.5, .3, ('R', '5'), 92)]],
         strings=[[(0, 3.9, 'V', 66)]],
         choir=[[(0, 3.9, 'V', 70)]]),
     parts={'Drums': [(9, 56, 'dr'), (57, 64, 'dr_half'), (73, 128, 'dr')],
            'Bass': [(9, 56, 'bass'), (57, 64, 'bass_half'), (73, 128, 'bass')],
            'Rhythm Guitar': [(9, 56, 'chug'), (57, 64, 'chug_half'), (73, 128, 'chug')],
            'Strings': [(1, 136, 'strings')],
            'Choir': [(1, 8, 'choir'), (57, 72, 'choir'), (105, 136, 'choir')]},
     fills={'Drums': {16: 'dr_fill', 56: 'dr_fill', 64: 'dr_fill', 92: 'dr_fill', 104: 'dr_fill', 128: 'dr_fill',
                      9: 'dr_crash', 17: 'dr_crash', 33: 'dr_crash', 49: 'dr_crash', 73: 'dr_crash', 93: 'dr_crash', 105: 'dr_crash', 117: 'dr_crash'}},
     passes=[dict(at=17, src=(1, 20), track='Lead Guitar', oct=0,
                 ops=[['pat:0,.5,1,1.5,2,2.5,3,3.5'], ['pat:0,.75,2,2.75,3.5', 'sync:2'], ['pat:0,.5,1.5,2,3,3.5'], ['pat:0,.75,1.5,2.5,3,3.5']]),
             dict(at=73, src=(11, 20), track='Synth Lead', oct=0,
                 ops=[['pat:0,.75,1.5,2,2.75,3.5'], ['pat:0,.5,2,3,3.5', 'sync:2'], ['pat:0,.5,1,1.5,2,2.5,3,3.5'], ['pat:.5,1,1.5,2.5,3,3.5']])],
     motifs=[dict(track='Lead Guitar', at=(9, 11, 13, 15, 93, 95, 97, 99, 101, 103), span=2,
                  notes=((0, .5, 67), (.5, .5, 70), (1, .5, 74), (1.5, 1, 75), (2.5, .5, 74), (3, 1, 70), (4, .5, 72), (4.5, .5, 74), (5, 1, 75), (6, 1.9, 74))),
             dict(track='Synth Lead', at=(65, 67, 69, 71), span=2,
                  notes=((0, 2, 79), (2, 1, 77), (3, 1, 75), (4, 2, 74), (6, 1.9, 70)))],
     markers=[(1, 'intro'), (9, 'riff'), (17, 'theme 1'), (57, 'breakdown'), (65, 'choir'), (73, 'theme 2'), (93, 'solo'), (105, 'climax'), (129, 'outro')],
     intro_bars=8, outro_from=129, patches={7: 'Mixed Choir'},
     notes='심포닉 메탈: 폭풍 동기를 3+3+2 로 늘린 뒤 8분 트레몰로·갤럽으로 다시 뽑아 리드 기타가 부르고, 합창이 폭풍을 감쌉니다.')

# 7 ---------------------------------------------------------------- Autumn I — Balkan brass 7/8
song(key=('autumn', 1), sid='vs-autumn1-opus', title='Autumn I Opus', genre='Balkan brass',
     genre_reason='농부들의 춤과 취해 비틀거리는 독주가 발칸 브라스 잔치 음악과 같은 장면이고, 4/4 를 7/8(2+2+3)로 꺾어 비틀거림을 박자로 만듭니다.',
     meter=(7, 8), bpm=140, bars=120, out_key='F major', sf=-1, minor=False, tr=0,
     theme_part='violin1', theme_window=(1, 12),
     mp=mp(4, 7, ((0, 0), (1, 2), (2, 3.5), (3, 5.5), (4, 7)), snap=0.5, text='4/4 한 마디 → 7/8 두 마디(박마다 2·3 묶음 번갈아)'),
     rhythm_ops=['regroup', 'sync', 'late', 'pat'], swing=None, hum=7,
     palette=['F', 'Bb', 'C7', 'Dm', 'Gm', 'A7'], loop=['F', 'F', 'C7', 'F'],
     tracks=[dict(name='Drums', ch=9, pc=0, role='drums', path='A 0 SoCal (타판 대용)'),
             dict(name='Trumpet', ch=0, pc=56, role='lead', vel=(72, 96), path='A 56 Studio Trumpet 1'),
             dict(name='Alto Sax', ch=1, pc=65, role='lead', vel=(70, 92), path='A 65 Studio Alto Sax 2'),
             dict(name='Accordion', ch=2, pc=21, role='acc', rng=(55, 74), vel=(62, 84), path='B Polka Accordion', patch='Polka Accordion'),
             dict(name='Tuba', ch=3, pc=58, role='bass', rng=(29, 50), vel=(72, 94), path='B Tuba', patch='Tuba')],
     patterns=dict(
         dr=[gm_pat((0, KICK, 102), (1, KICK, 92), (2, KICK, 96), (0.5, SNARE, 70), (1.5, SNARE, 74), (2.5, SNARE, 78), (3, SNARE, 86),
                    *[(i / 2, HAT, 64 if i % 2 else 54) for i in range(7)])],
         dr_soft=[gm_pat((0, KICK, 92), (2, KICK, 86), (1.5, RIM, 64), (3, RIM, 70), *[(i / 2, HAT, 50) for i in range(7)])],
         tuba=[[(0, .45, 'R', 88), (1, .45, '5', 80), (2, .9, 'R', 84)], [(0, .45, 'R', 88), (1, .45, '3', 80), (2, .45, '5', 82), (3, .4, 'app', 76)]],
         acc=[[(0.5, .4, 'Vt', 74), (1.5, .4, 'Vt', 72), (2.5, .4, 'Vt', 72), (3, .4, 'Vt', 68)]],
         acc_hold=[[(0, 3.4, 'V', 68)]]),
     parts={'Drums': [(1, 8, 'dr_soft'), (9, 112, 'dr'), (113, 118, 'dr_soft')],
            'Tuba': [(1, 120, 'tuba')],
            'Accordion': [(1, 112, 'acc'), (113, 120, 'acc_hold')]},
     fills={},
     passes=[dict(at=17, src=(1, 12), track='Trumpet', oct=-12, ops=[['sync:2'], ['late:0'], ['pat:0,1,2'], ['sync:2']]),
            dict(at=49, src=(1, 12), track='Alto Sax', oct=-12, ops=[['late:0'], ['sync:2'], ['late:2'], ['pat:0,1,2']]),
            dict(at=85, src=(1, 6), track='Trumpet', oct=-12, ops=[['sync:1'], ['late:0'], ['pat:0,1,2'], ['late:0']])],
     motifs=[dict(track='Alto Sax', at=(9, 11, 13, 15, 73, 75, 77, 79, 81, 83, 97, 99, 101, 103, 105, 107, 109, 111), span=2,
                  notes=((0, .5, 72), (.5, .5, 70), (1, .5, 69), (1.5, .5, 70), (2, 1.4, 72), (3.5, .5, 74), (4, .5, 72), (4.5, .5, 70), (5, .5, 69), (5.5, 1.4, 65))),
             dict(track='Trumpet', at=(74, 76, 78, 80, 82, 98, 100, 102, 104, 106, 108, 110), span=1,
                  notes=((0, .45, 65), (.5, .45, 69), (1, .45, 72), (2, 1.4, 77)))],
     markers=[(1, 'intro'), (9, 'kolo'), (17, 'theme 1'), (41, 'accordion'), (49, 'theme 2'), (73, 'call & response'), (85, 'theme 3'), (97, 'shout'), (113, 'outro')],
     intro_bars=8, outro_from=113, patches={4: 'Polka Accordion', 5: 'Tuba'},
     notes='발칸 브라스: 춤곡 주제를 7/8 두 마디로 꺾어 트럼펫이 부르고 알토 색소폰이 받으며, 튜바·아코디언이 움-파를 합니다.')

# 8 ---------------------------------------------------------------- Autumn II — Cool jazz ballad
song(key=('autumn', 2), sid='vs-autumn2-opus', title='Autumn II Opus', genre='Cool jazz ballad',
     genre_reason='잠든 취객들의 Adagio molto 는 약음기 현의 반음계 화음과 분산화음뿐인 정지된 밤이라, 반음계 화성을 품는 쿨 재즈 발라드로 옮깁니다.',
     meter=(4, 4), bpm=88, bars=64, out_key='D minor', sf=-1, minor=True, tr=0,
     theme_part='violin1', theme_window=(4, 14),
     mp=mp(3, 4, ((0, 0), (1, 1.5), (2, 3), (3, 4)), snap=0.25, text='3/4 → 4/4 (둘째 박을 8분 늦춰 4박 안에 다시 배치)'),
     rhythm_ops=['regroup', 'sync', 'late', 'swing'], swing=(0.5, 70), hum=8,
     palette=['Dm9', 'Gm9', 'A7b13', 'Bbmaj7', 'Em7b5', 'D9', 'Ebmaj7', 'C9sus', 'E7b9'], loop=['Dm9', 'Em7b5', 'A7b13', 'Dm9'],
     tracks=[dict(name='Drums', ch=9, pc=0, role='drums', path='A 0 SoCal (브러시 대용)'),
             dict(name='Bass', ch=0, pc=32, role='bass', rng=(28, 50), vel=(62, 82), path='A 32 루트 업라이트'),
             dict(name='Piano', ch=1, pc=0, role='acc', rng=(50, 72), vel=(54, 76), path='A 0 Studio Grand'),
             dict(name='Vibes', ch=2, pc=11, role='lead', vel=(60, 82), path='A 11 Vibraphone'),
             dict(name='Tenor Sax', ch=3, pc=66, role='lead', vel=(60, 86), path='B Studio Tenor Sax 1', patch='Studio Tenor Sax 1')],
     patterns=dict(
         dr=[gm_pat((0, RIDE, 62), (1, RIDE, 58), (1.5, RIDE, 50), (2, RIDE, 62), (3, RIDE, 58), (3.5, RIDE, 50), (1, PHAT, 50), (3, PHAT, 52),
                    *[(i / 2, SNARE, 34 + (i % 2) * 4) for i in range(8)], (0, KICK, 56))],
         dr_light=[gm_pat((0, RIDE, 54), (2, RIDE, 54), (1, PHAT, 46), (3, PHAT, 46))],
         bass2=[[(0, 1.9, 'R', 76), (2, 1.9, '5', 70)]],
         walk=[[(0, .9, 'R', 76), (1, .9, '3', 70), (2, .9, '5', 72), (3, .9, 'app', 68)]],
         comp=[[(0, 1.4, 'V', 66), (2.5, 1.2, 'Vt', 60)], [(0.5, 1.9, 'V', 64), (3, .9, 'Vt', 58)]]),
     parts={'Drums': [(5, 8, 'dr_light'), (9, 57, 'dr'), (58, 60, 'dr_light')],
            'Bass': [(1, 19, 'bass2'), (20, 46, 'walk'), (47, 62, 'bass2')],
            'Piano': [(1, 64, 'comp')]},
     fills={},
     passes=[dict(at=9, src=(4, 14), track='Tenor Sax', oct=-12, ops=[[]],
                 ops_at={0: ['sync:0'], 3: ['late:1.5'], 6: ['sync:0'], 7: ['sync:3'], 9: ['late:1.5'], 10: ['sync:0']}),
            dict(at=28, src=(4, 14), track='Vibes', oct=0, ops=[[]],
                 ops_at={2: ['sync:0'], 3: ['late:1.5'], 5: ['late:0'], 6: ['sync:0'], 7: ['sync:3'], 8: ['sync:0'], 9: ['sync16:3']}),
            dict(at=47, src=(4, 14), track='Tenor Sax', oct=-12, ops=[[]],
                 ops_at={0: ['sync:0'], 3: ['sync:3'], 4: ['sync:0'], 7: ['late:1.5'], 9: ['late:1.5'], 10: ['sync:0']})],
     motifs=[dict(track='Vibes', at=(5, 7, 20, 22, 24, 26), span=2,
                  notes=((0.5, 1, 74), (1.5, .5, 72), (2, 1.5, 69), (4, 1, 65), (5, .5, 67), (5.5, 2.4, 69))),
             dict(track='Tenor Sax', at=(39, 41, 43, 45), span=2,
                  notes=((0, 1.5, 62), (1.5, .5, 64), (2, 1, 65), (3, 1, 69), (4.5, 1, 67), (5.5, .5, 65), (6, 1.9, 64))),
             dict(track='Tenor Sax', at=(59, 61, 63), span=2,
                  notes=((0.5, 1.5, 65), (2, 2, 64), (4, 3.9, 62)))],
     markers=[(1, 'intro'), (9, 'theme 1'), (20, 'piano'), (28, 'theme 2'), (39, 'sax'), (47, 'theme 3'), (58, 'outro')],
     intro_bars=8, outro_from=58, patches={5: 'Studio Tenor Sax 1'},
     notes='쿨 재즈 발라드: 반음계 상성부를 테너 색소폰이 스윙으로 부르고, 업라이트가 2비트에서 워킹으로 넘어갑니다.')

# 9 ---------------------------------------------------------------- Autumn III — Spaghetti western
song(key=('autumn', 3), sid='vs-autumn3-opus', title='Autumn III Opus', genre='Spaghetti western',
     genre_reason='사냥의 호른 부름·총성·쫓기는 짐승은 말발굽 갤럽과 트럼펫·호른 부름, 채찍 같은 타격의 서부극 음악과 같은 장면입니다.',
     meter=(4, 4), bpm=112, bars=84, out_key='D minor', sf=-1, minor=True, tr=0,
     theme_part='violin1', theme_window=(1, 24),
     mp=mp(1.5, 4, ((0, 0), (0.5, 1.5), (1.0, 3), (1.5, 4)), snap=0.25, text='3/8 → 4/4 갤럽(8분 셋을 3+3+2 4분으로)'),
     rhythm_ops=['regroup', 'sync', 'late', 'thin4'], swing=None, hum=8,
     palette=['Dm', 'F', 'Bb', 'C', 'A7', 'Gm', 'C7'], loop=['Dm', 'Dm', 'Bb', 'A7'],
     tracks=[dict(name='Drums', ch=9, pc=0, role='drums', path='A 0 SoCal'),
             dict(name='Bass', ch=0, pc=32, role='bass', rng=(28, 50), vel=(68, 90), path='A 32 루트 업라이트'),
             dict(name='Guitar', ch=1, pc=24, role='acc', rng=(50, 71), vel=(64, 88), path='A 24 Classical Acoustic Guitar'),
             dict(name='Strings', ch=2, pc=48, role='acc', rng=(55, 79), vel=(48, 70), path='A 48 Kensington'),
             dict(name='Trumpet', ch=3, pc=56, role='lead', vel=(72, 98), path='A 56 Studio Trumpet 1'),
             dict(name='Timpani', ch=4, pc=47, role='acc', rng=(38, 55), vel=(60, 110), path='B Timpani', patch='Timpani'),
             dict(name='Horns', ch=5, pc=60, role='lead', rng=(53, 72), vel=(66, 92), path='B French Horns', patch='French Horns')],
     patterns=dict(
         dr=[gm_pat((0, KICK, 96), (2, KICK, 90), *[(b + o, RIM, v) for b in range(4) for o, v in ((0, 84), (.5, 64), (.75, 70))], (1, SNARE, 86), (3, SNARE, 90))],
         dr_toms=[gm_pat(*[(b + o, TFL if b % 2 == 0 else TLO, v) for b in range(4) for o, v in ((0, 92), (.5, 70), (.75, 76))])],
         bass=[[(0, .9, 'R', 84), (1, .9, '5', 76), (2, .9, 'R', 82), (3, .9, '5', 76)]],
         gallop=[[(b + o, d, 'V', v) for b in range(4) for o, d, v in ((0, .45, 78), (.5, .2, 64), (.75, .2, 68))]],
         strings=[[(0, 3.9, 'V', 58)]],
         timp=[[(0, .9, 'R', 92), (2, .9, '5', 80)]],
         timp_roll=[[(i / 4, .2, 'R', 60 + i * 3) for i in range(16)]],
         horn_pad=[[(0, 3.9, 'Vt', 72)]]),
     parts={'Drums': [(9, 76, 'dr'), (77, 80, 'dr_toms')],
            'Bass': [(9, 80, 'bass')],
            'Guitar': [(1, 84, 'gallop')],
            'Strings': [(1, 12, 'strings'), (37, 44, 'strings'), (61, 84, 'strings')],
            'Timpani': [(1, 8, 'timp'), (12, 12, 'timp_roll'), (13, 36, 'timp'), (44, 44, 'timp_roll'), (69, 76, 'timp'), (77, 80, 'timp_roll'), (81, 84, 'timp')],
            'Horns': [(13, 36, 'horn_pad')]},
     fills={},
     passes=[dict(at=13, src=(1, 24), track='Trumpet', oct=0, ops=[['sync:3'], ['thin4'], ['thin4'], ['sync:1.5']]),
            dict(at=45, src=(1, 16), track='Horns', oct=-12, ops=[['late:0'], ['sync:3'], ['thin4'], ['sync:1.5']])],
     motifs=[dict(track='Horns', at=(37, 39, 41, 43, 69, 71, 73, 75), span=2,
                  notes=((0, 1.5, 62), (1.5, .5, 65), (2, 2, 69), (4, 1, 67), (5, 1, 65), (6, 1.9, 62))),
             dict(track='Trumpet', at=(61, 63, 65, 67), span=2,
                  notes=((0, .5, 74), (.5, .5, 74), (1, 1.5, 77), (3, 1, 76), (4, 1.5, 74), (6, 1.9, 69))),
             dict(track='Horns', at=(77, 79, 81, 83), span=2,
                  notes=((0, 2, 62), (2, 2, 65), (4, 3.9, 62)))],
     markers=[(1, 'intro'), (9, 'ride'), (13, 'theme 1'), (37, 'horn call'), (45, 'theme 2'), (61, 'duel'), (69, 'chase'), (77, 'outro')],
     intro_bars=8, outro_from=77, patches={6: 'Timpani', 7: 'French Horns'},
     notes='스파게티 웨스턴: 사냥 호른 부름을 갤럽 4/4 로 늘려 트럼펫이 부르고, 프렌치 호른 섹션이 받습니다.')

# 10 --------------------------------------------------------------- Winter I — Dark techno
song(key=('winter', 1), sid='vs-winter1-opus', title='Winter I Opus', genre='Dark techno',
     genre_reason='얼어붙어 떨리는 반복음, 발 구르기, 차가운 바람이 시퀀서 펄스·4온더플로어 킥·차가운 패드의 테크노 언어와 바로 대응합니다.',
     meter=(4, 4), bpm=128, bars=96, out_key='F minor', sf=-4, minor=True, tr=0,
     theme_part='solo', theme_window=(4, 13),
     mp=mp(4, 8, ((0, 0), (4, 8)), text='4/4 하프타임(음가 2배)'),
     rhythm_ops=['halftime', 'pat'], swing=None, hum=5,
     palette=['Fm', 'Db', 'C7b9', 'Bbm', 'Ab', 'Gm7b5', 'Fm9', 'Eb'], loop=['Fm', 'Fm', 'Db', 'C7b9'],
     tracks=[dict(name='Drums', ch=9, pc=25, role='drums', path='A 25 Drum Synth Kit'),
             dict(name='Pulse Bass', ch=0, pc=38, role='bass', rng=(36, 55), vel=(56, 74), path='A 38 Pulse Bass'),
             dict(name='Pad', ch=1, pc=94, role='acc', rng=(53, 77), vel=(52, 70), path='A 94 Tidal Space'),
             dict(name='Chords', ch=2, pc=90, role='acc', rng=(55, 76), vel=(62, 84), path='A 90 Epic Cloud Formation'),
             dict(name='Lead', ch=3, pc=80, role='lead', vel=(82, 102), path='A 80 Reverse Engineering'),
             dict(name='Celesta', ch=4, pc=8, role='lead', vel=(80, 102), path='B Celesta', patch='Celesta')],
     patterns=dict(
         dr=[gm_pat(*[(b, KICK, 92 if b == 0 else 88) for b in range(4)], (1, CLAP, 86), (3, CLAP, 88),
                    *[(b + .5, OHAT, 72) for b in range(4)], *[(b + o, HAT, 54) for b in range(4) for o in (.25, .75)])],
         dr_intro=[gm_pat(*[(b, KICK, 90) for b in range(4)], *[(b + .5, OHAT, 64) for b in range(4)])],
         dr_break=[gm_pat(*[(b + o, HAT, 50) for b in range(4) for o in (.25, .75)], (3.5, OHAT, 60))],
         dr_roll=[gm_pat(*[(b, KICK, 88) for b in range(4)], *[(i / 4, SNARE, 50 + i * 3) for i in range(16)])],
         pulse=[[(i / 4, .2, 'R' if i % 4 != 3 else '5', 84 if i % 4 == 0 else 74) for i in range(16)]],
         pulse_half=[[(i / 2, .4, 'R', 76) for i in range(8)]],
         pad=[[(0, 3.9, 'V', 60)]],
         stab=[[(0.5, .3, 'Vt', 76), (1.75, .3, 'Vt', 72), (3, .3, 'Vt', 78)]]),
     parts={'Drums': [(1, 36, 'dr_intro'), (37, 48, 'dr_break'), (49, 56, 'dr_roll'), (57, 88, 'dr'), (89, 96, 'dr_intro')],
            'Pulse Bass': [(9, 36, 'pulse'), (37, 48, 'pulse_half'), (49, 88, 'pulse')],
            'Pad': [(1, 96, 'pad')],
            'Chords': [(9, 36, 'stab'), (57, 88, 'stab')]},
     fills={'Drums': {s_: 'dr' for s_ in range(17, 37)}},
     passes=[dict(at=17, src=(4, 13), track='Lead', oct=0, ops=[['pat:0,.75,1.5,2.5,3'], ['pat:.5,1.5,2,2.75,3.5']]),
             dict(at=57, src=(4, 13), track='Celesta', oct=0, ops=[['pat:0,.5,1.5,2,3'], ['pat:.75,1.5,2.5,3.25']])],
     motifs=[dict(track='Celesta', at=(37, 39, 41, 43, 45, 47, 89, 91, 93, 95), span=2,
                  notes=((0, .5, 77), (.5, .5, 80), (1, 1, 84), (2.5, .5, 82), (3, 1, 80), (4.5, .5, 77), (5, 1, 79), (6, 1.9, 77))),
             dict(track='Lead', at=(77, 79, 81, 83, 85, 87), span=2,
                  notes=((0, .5, 72), (.5, .5, 72), (1.5, 1, 75), (3, .75, 73), (4, 1.5, 72), (6, .5, 68), (6.5, 1.25, 67)))],
     markers=[(1, 'intro'), (9, 'pulse'), (17, 'theme 1'), (37, 'breakdown'), (49, 'build'), (57, 'theme 2'), (77, 'peak'), (89, 'outro')],
     intro_bars=8, outro_from=89, patches={6: 'Celesta'},
     notes='다크 테크노: 떨리는 8분 연타를 하프타임 3+3+2 스탭으로 다시 뽑아 스퀘어 리드와 첼레스타가 부르고, 16분 펄스 베이스가 이 부딪힘을 대신합니다.')

# 11 --------------------------------------------------------------- Winter II — Neo-soul
song(key=('winter', 2), sid='vs-winter2-opus', title='Winter II Opus', genre='Neo-soul',
     genre_reason='난롯가의 따뜻한 Largo 선율과 바깥 빗소리(현 피치카토)가 따뜻한 로즈·느슨한 드럼·색소폰의 네오 소울과 같은 온도입니다.',
     meter=(4, 4), bpm=72, bars=54, out_key='E♭ major', sf=-3, minor=False, tr=0,
     theme_part='solo', theme_window=(1, 8),
     mp=mp(4, 4, ((0, 0), (4, 4)), text='4/4 그대로(템포 +57%)'),
     rhythm_ops=['sync', 'late', 'thin8', 'swing'], swing=(0.25, 32), hum=10,
     palette=['Abmaj9', 'Gm7', 'Fm9', 'Bb13', 'Ebmaj9', 'Cm9', 'Db9', 'Bb9sus'], loop=['Abmaj9', 'Gm7', 'Fm9', 'Bb13'],
     tracks=[dict(name='Drums', ch=9, pc=0, role='drums', path='A 0 SoCal'),
             dict(name='Bass', ch=0, pc=33, role='bass', rng=(28, 50), vel=(66, 86), path='A 33 Simple Foundation'),
             dict(name='Rhodes', ch=1, pc=4, role='acc', rng=(50, 74), vel=(60, 82), path='A 4 Deluxe Classic'),
             dict(name='Alto Sax', ch=2, pc=65, role='lead', vel=(62, 86), path='A 65 Studio Alto Sax 2'),
             dict(name='Piano', ch=3, pc=0, role='lead', vel=(60, 84), path='A 0 Studio Grand'),
             dict(name='Pizzicato', ch=4, pc=45, role='acc', rng=(60, 84), vel=(46, 66), path='C Violins 1 + Violin (Pizzicato)', patch=('Violins 1', 'Violin (Pizzicato)'))],
     patterns=dict(
         dr=[gm_pat((0, KICK, 98), (1.75, KICK, 84), (2.5, KICK, 92), (1, SNARE, 90), (3, SNARE, 92), (2.25, SNARE, 42), (3.75, SNARE, 40),
                    *[(i / 4, HAT, 50 if i % 2 else 62) for i in range(16) if i not in (4, 12)])],
         dr_light=[gm_pat((0, KICK, 86), (1, RIM, 70), (3, RIM, 72), *[(i / 2, HAT, 48) for i in range(8)])],
         bass=[[(0, .9, 'R', 80), (1.5, .4, '5', 72), (2.5, .9, 'R', 76), (3.5, .4, 'app', 70)], [(0, 1.4, 'R', 80), (2, .4, '3', 72), (2.75, 1.0, '5', 74)]],
         rhodes=[[(0, 1.9, 'V', 72), (2.5, 1.3, 'Vt', 66)], [(0.75, 1.1, 'V', 70), (2, 1.9, 'V', 68)]],
         pizz=[[(0, .3, 'A3', 58), (.75, .3, 'A2', 52), (1.5, .3, 'A1', 54), (2.25, .3, 'A2', 50), (3, .3, 'A3', 56), (3.5, .3, 'A0', 50)],
               [(0.25, .3, 'A2', 52), (1, .3, 'A3', 56), (1.75, .3, 'A1', 50), (2.5, .3, 'A2', 54), (3.25, .3, 'A0', 50)]]),
     parts={'Drums': [(5, 8, 'dr_light'), (9, 46, 'dr'), (47, 50, 'dr_light')],
            'Bass': [(5, 52, 'bass')],
            'Rhodes': [(1, 54, 'rhodes')],
            'Pizzicato': [(1, 8, 'pizz'), (17, 22, 'pizz'), (31, 38, 'pizz'), (47, 54, 'pizz')]},
     fills={},
     passes=[dict(at=9, src=(1, 8), track='Alto Sax', oct=-12,
                 ops=[['sync:3.5'], ['thin8', 'sync:3.5'], ['thin8'], [], ['late:2'], ['late:0'], ['thin8'], ['late:2']]),
             dict(at=23, src=(1, 8), track='Piano', oct=0,
                 ops=[['thin8', 'sync:3.5'], ['sync:3.5'], ['thin8'], ['thin8'], ['late:0'], ['late:2'], ['thin8'], ['late:2']]),
             dict(at=39, src=(1, 8), track='Alto Sax', oct=-12,
                 ops=[['sync:3.5'], ['thin8'], ['thin8'], [], ['late:0'], ['late:2'], ['thin8'], ['late:2']])],
     motifs=[dict(track='Alto Sax', at=(31, 33, 35, 37), span=2,
                  notes=((0.5, 1, 63), (1.5, .5, 65), (2, 1.5, 67), (4, 1, 70), (5, .5, 67), (5.5, 2.4, 65))),
             dict(track='Piano', at=(17, 19, 21), span=2,
                  notes=((0, .5, 75), (.5, .5, 77), (1, 1.5, 79), (3, 1, 77), (4.5, 1, 75), (6, 1.9, 72)))],
     markers=[(1, 'intro'), (9, 'theme 1'), (17, 'rain'), (23, 'theme 2'), (31, 'sax'), (39, 'theme 3'), (47, 'outro')],
     intro_bars=8, outro_from=47, patches={6: ('Violins 1', 'Violin (Pizzicato)')},
     notes='네오 소울: Largo 선율을 알토 색소폰이 16분 스윙으로 부르고, 솔로 바이올린 피치카토가 빗방울처럼 떨어집니다.')

# 12 --------------------------------------------------------------- Winter III — Tango nuevo
song(key=('winter', 3), sid='vs-winter3-opus', title='Winter III Opus', genre='Tango nuevo',
     genre_reason='얼음 위를 조심스레 걷다 미끄러지는 F 단조 알레그로가 탱고의 마르카토 반주·미끄러지는 레가토 선율·극적인 단조와 맞습니다.',
     meter=(4, 4), bpm=116, bars=88, out_key='F minor', sf=-4, minor=True, tr=0,
     theme_part='solo', theme_window=(1, 24),
     mp=mp(1.5, 4, ((0, 0), (0.5, 1.5), (0.75, 2), (1.0, 3), (1.5, 4)), snap=0.25, text='3/8 → 4/4 탱고(16분 여섯을 3+3+2 자리로)'),
     rhythm_ops=['regroup', 'sync', 'late', 'thin4'], swing=None, hum=7,
     palette=['Fm', 'Bbm', 'C7b9', 'Db', 'Gm7b5', 'Ab', 'Eb', 'C7'], loop=['Fm', 'Fm', 'C7b9', 'Fm'],
     tracks=[dict(name='Piano', ch=0, pc=0, role='acc', rng=(48, 72), vel=(62, 90), path='A 0 Studio Grand'),
             dict(name='Bass', ch=1, pc=43, role='bass', rng=(28, 50), vel=(70, 94), path='A 43 Studio Double Basses'),
             dict(name='Strings', ch=2, pc=48, role='acc', rng=(55, 79), vel=(50, 74), path='A 48 Kensington'),
             dict(name='Accordion', ch=3, pc=21, role='lead', rng=(55, 74), vel=(64, 88), path='B Polka Accordion', patch='Polka Accordion'),
             dict(name='Solo Violin', ch=4, pc=40, role='lead', vel=(64, 92), path='C Violins 1 + Violin (Arco)', patch=('Violins 1', 'Violin (Arco)'))],
     patterns=dict(
         marcato=[[(0, .45, 'V', 86), (1, .45, 'V', 74), (2, .45, 'V', 82), (3, .45, 'V', 74)]],
         three32=[[(0, .7, 'V', 86), (1.5, .7, 'V', 80), (3, .45, 'V', 82)]],
         bass=[[(0, .7, 'R', 88), (1.5, .45, '5', 80), (2, .9, 'R', 84), (3.5, .4, 'app', 76)]],
         bass332=[[(0, 1.4, 'R', 90), (1.5, 1.4, '5', 84), (3, .9, 'R', 86)]],
         strings=[[(0, 3.9, 'V', 60)]],
         strings_stab=[[(0, .4, 'Vt', 72), (1.5, .4, 'Vt', 66), (3, .4, 'Vt', 70)]],
         acc_rhythm=[[(0, .4, 'Vt', 80), (.75, .3, 'Vt', 70), (1.5, .4, 'Vt', 76), (2.5, .4, 'Vt', 74), (3, .4, 'Vt', 78)]]),
     parts={'Piano': [(1, 36, 'marcato'), (37, 44, 'three32'), (45, 72, 'marcato'), (73, 80, 'three32'), (81, 88, 'marcato')],
            'Bass': [(1, 36, 'bass'), (37, 44, 'bass332'), (45, 72, 'bass'), (73, 80, 'bass332'), (81, 87, 'bass')],
            'Strings': [(9, 36, 'strings'), (37, 44, 'strings_stab'), (61, 80, 'strings')],
            'Accordion': [(37, 44, 'acc_rhythm'), (73, 80, 'acc_rhythm')]},
     fills={},
     passes=[dict(at=13, src=(1, 24), track='Solo Violin', oct=0, ops=[['thin4'], ['sync:0'], ['late:2'], ['thin4', 'late:1']]),
            dict(at=45, src=(1, 16), track='Accordion', oct=-12, ops=[['late:2'], ['thin4'], ['sync:0'], []])],
     motifs=[dict(track='Accordion', at=(9, 11), span=2,
                  notes=((0, 1, 65), (1.5, .5, 68), (2, 1.5, 72), (4, .75, 70), (4.75, .75, 68), (5.5, 2.4, 65))),
             dict(track='Solo Violin', at=(61, 63, 65, 67, 69, 71, 73, 75, 77, 79), span=2,
                  notes=((0, 1.5, 77), (1.5, .5, 76), (2, 1, 77), (3, 1, 80), (4, 1.5, 79), (5.5, .5, 77), (6, 1.9, 72))),
             dict(track='Solo Violin', at=(81, 83, 85, 87), span=2,
                  notes=((0, 2, 72), (2, 2, 68), (4, 3.9, 65)))],
     markers=[(1, 'intro'), (9, 'bandoneon'), (13, 'theme 1'), (37, 'variacion'), (45, 'theme 2'), (61, 'violin'), (73, 'climax'), (81, 'outro')],
     intro_bars=8, outro_from=81, patches={4: 'Polka Accordion', 5: ('Violins 1', 'Violin (Arco)')},
     notes='탱고 누에보: 미끄러지는 16분 음형을 3+3+2 로 다시 놓아 솔로 바이올린이 부르고, 아코디언(반도네온 대용)이 받습니다.')


RHYTHM_OP_CLASS = {'sync': '①당김', 'late': '①당김', 'halftime': '②음가', 'x2': '②음가',
                   'thin8': '③골격', 'thin4': '③골격', 'pat': '③골격', 'swing': '④박분할', 'dot': '④박분할'}


# ---------------------------------------------------------------- compose
def lead_plan(s):
    bq = s['bar_q']
    out = {name: [] for name in [p['track'] for p in s['passes']] + [mo['track'] for mo in s['motifs']]}
    orig_by_bar, effective, fired = {}, [], []
    for p in s['passes']:
        notes, orig, n_out, eff, tokens = theme_pass(s, p)
        effective.append(eff)
        fired.append(tokens)
        base = (p['at'] - 1) * bq
        for n in notes:
            out[p['track']].append((base + n['b'], base + n['e'], n['p'], 'theme'))
        for k, flag in enumerate(orig):
            assert p['at'] + k not in orig_by_bar, ('theme passes overlap', s['sid'], p['at'] + k)
            orig_by_bar[p['at'] + k] = flag
    for mo in s['motifs']:
        for at in mo['at']:
            base = (at - 1) * bq
            for b, d, pitch in mo['notes']:
                out[mo['track']].append((base + b, base + b + d, pitch, 'motif'))
    for k in out:
        out[k].sort()
        for i, (a, b) in enumerate(zip(out[k], out[k][1:])):
            if a[1] > b[0] - 0.06:
                out[k][i] = (a[0], b[0] - 0.06, a[2], a[3])
                assert out[k][i][1] - a[0] >= 0.12, ('note squeezed', s['sid'], k, a, b)
    return out, orig_by_bar, effective, fired


def theme_offbeat_bars(s, leads):
    """Theme bars where the song's swing actually moves a theme onset (④ only counts when it reaches the theme)."""
    if not s['swing']:
        return 0
    g, bq = s['swing'][0], s['bar_q']
    bars = set()
    for notes in leads.values():
        for b, e, p, kind in notes:
            if kind == 'theme' and abs((b % (2 * g)) - g) < 1e-6:
                bars.add(int(b // bq))
    return len(bars)


def part_of(s, track, bar):
    for b0, b1, name in s['parts'].get(track, []):
        if b0 <= bar <= b1:
            fill = s['fills'].get(track, {}).get(bar)
            return fill or name
    fill = s['fills'].get(track, {}).get(bar)
    return fill


def compose(sid):
    s = next(x for x in SKETCHES if x['sid'] == sid)
    num, den = s['meter']
    bq = num * 4 / den
    s['bar_q'] = bq
    bar_ticks = int(round(bq * PPQ))
    seed(20261110 + sum(map(ord, sid)))
    leads, orig_by_bar, effective, fired = lead_plan(s)
    lead_all = [(b, e, p) for notes in leads.values() for b, e, p, _ in notes]
    chords = harmonize(s, lead_all)
    names = [t['name'] for t in s['tracks']]
    nt = {i: [] for i in range(len(names))}
    cc = {i: [] for i in range(len(names))}
    pcs = {i: t['pc'] for i, t in enumerate(s['tracks'])}
    sw = s['swing']

    def tick_of(q, drum=False):
        t = q * PPQ
        if sw and abs((q % (2 * sw[0])) - sw[0]) < 1e-6:
            t += sw[1]
        return max(0, hum_t(int(round(t)), s['hum'] if not drum else max(4, s['hum'] - 2)))

    prev_voicing = {}
    pattern_notes = {i: [] for i in range(len(names))}
    layer_pitches = {}          # bar -> pitches of the chord layers placed so far (bass excluded, like check())
    for ti, t in enumerate(s['tracks']):
        for bar in range(1, s['bars'] + 1):
            pname = part_of(s, t['name'], bar)
            if not pname:
                continue
            pat = s['patterns'][pname]
            elems = pat[(bar - 1) % len(pat)]
            b0q = (bar - 1) * bq
            end_bar = int(round(bar * bq * PPQ)) - 12
            if t['role'] == 'drums':
                for pos, pitch, v in elems:
                    when = tick_of(b0q + pos, drum=True)
                    vel = max(30, min(127, hum_v(v, 6)))
                    nt[ti].append((when, min(110, end_bar - when), pitch, vel))
                continue
            root, q = chord(chords[bar - 1])
            lo, hi = t['rng']
            if any(isinstance(e[2], str) and e[2][0] in 'VA' for e in elems):
                voic = voicing(root, q, lo, hi, prev_voicing.get(ti), layer_pitches.get(bar, ()))
                prev_voicing[ti] = voic
            for pos, dur, what, v in elems:
                if what == 'V':
                    pitches = list(voic)
                elif what == 'Vt':
                    pitches = list(voic[1:])
                elif what == 'Vb':
                    pitches = list(voic[:2])
                elif isinstance(what, str) and what.startswith('A'):
                    pitches = [voic[int(what[1]) % len(voic)]]
                else:
                    degs = what if isinstance(what, tuple) else (what,)
                    base = lo + (root - lo) % 12
                    pitches = []
                    for d in degs:
                        if d == 'app':
                            nroot, _ = chord(chords[bar % s['bars']])
                            pch = lo + (nroot - lo) % 12 - 1
                            pch = pch if pch >= lo else pch + 12
                        else:
                            pch = base + degree_pc(d, root, q) + (12 if d == '8' else 0)
                            while pch > hi:
                                pch -= 12
                        pitches.append(pch)
                when = tick_of(b0q + pos)
                vel = max(t['vel'][0], min(t['vel'][1], hum_v(v, 6)))
                dur_t = min(int(dur * PPQ), end_bar - when)
                if dur_t < 20:
                    continue
                for pch in sorted(set(pitches)):
                    nt[ti].append((when, dur_t, pch, vel))
                    pattern_notes[ti].append((when, pch))
                    if t['role'] != 'bass':
                        layer_pitches.setdefault((when + 60) // bar_ticks + 1, set()).add(pch)
    for name, notes in leads.items():
        ti = names.index(name)
        t = s['tracks'][ti]
        events = []
        for b, e, pitch, kind in notes:
            when = tick_of(b)
            end = int(round(e * PPQ))
            base = sum(t['vel']) // 2 + (4 if abs(b % bq) < 1e-6 else 0)
            events.append([when, end, pitch, max(t['vel'][0], min(t['vel'][1], hum_v(base, 6)))])
        events.sort()
        total = s['bars'] * bar_ticks
        for i, ev in enumerate(events):
            nxt = events[i + 1][0] if i + 1 < len(events) else total
            ev[1] = min(ev[1], nxt - 24, total - 10)
            assert ev[1] - ev[0] >= 24, (sid, name, ev)
        nt[ti].extend((w, e - w, p, v) for w, e, p, v in events)
    for i in nt:
        nt[i].sort()
        # same-pitch overlaps on one track (two parts meeting at a bar line): shorten the earlier note
        last = {}
        fixed = []
        for when, dur, pitch, vel in nt[i]:
            if pitch in last and fixed[last[pitch]][0] + fixed[last[pitch]][1] > when:
                w0, d0, p0, v0 = fixed[last[pitch]]
                fixed[last[pitch]] = (w0, max(10, when - w0 - 5), p0, v0)
            last[pitch] = len(fixed)
            fixed.append((when, dur, pitch, vel))
        nt[i] = fixed
    tracks = [(t['name'], t['ch']) for t in s['tracks']]
    smf = build_smf(s['title'], s['bpm'], s['sf'], s['minor'], s['bars'], tracks, pcs, nt, cc, s['markers'],
                    timesig=(num, den))
    smf = with_attribution(smf)
    meta = dict(chords=chords, leads=leads, orig=orig_by_bar, effective=effective, fired=fired,
                swing_bars=theme_offbeat_bars(s, leads), bar_ticks=bar_ticks, pattern_notes=pattern_notes)
    return smf, nt, meta


def with_attribution(smf):
    """Copyright meta (delta 0) at the start of the FIRST INSTRUMENT track (the 2nd MTrk), not the conductor track."""
    pos = 14
    assert smf[pos:pos + 4] == b'MTrk'
    pos += 8 + struct.unpack('>I', smf[pos + 4:pos + 8])[0]
    assert smf[pos:pos + 4] == b'MTrk'
    ln = struct.unpack('>I', smf[pos + 4:pos + 8])[0]
    text = ATTRIBUTION.encode()
    body = b'\x00\xff\x02' + varlen(len(text)) + text + smf[pos + 8:pos + 8 + ln]
    return smf[:pos] + b'MTrk' + struct.pack('>I', len(body)) + body + smf[pos + 8 + ln:]


# ---------------------------------------------------------------- checks
def eff_ratio(s):
    return s['bpm'] * s['mp']['L'] / s['mp']['S'] / V.MOVEMENTS[s['key']]['tempo_bpm']


def max_orig_run(s, orig_by_bar):
    run = best = 0
    for bar in range(1, s['bars'] + 1):
        flag = orig_by_bar.get(bar)
        if flag is True or (flag == 'rest' and run):
            run += 1
        else:
            run = 0
        best = max(best, run)
    return best


def op_bars(effective):
    total = Counter()
    for eff in effective:
        for name, bars in eff.items():
            total[name] += len(bars)
    return total


def ops_used(s, meta):
    # snap4/snap8 = a thin op that only quantised (nothing merged): it still feeds the original-rhythm flags but is
    # not one of the brief's ①-④ classes, so it is never declared
    used = {name for name, n in op_bars(meta['effective']).items() if n >= MIN_OP_BARS and not name.startswith('snap')}
    mp_ = s['mp']
    pts = mp_['anchors']
    uniform = all(abs(o - q * mp_['S'] / mp_['L']) < 1e-9 for q, o in pts)
    if uniform and abs(mp_['S'] / mp_['L'] - 2) < 1e-9:
        used.add('halftime')
    if not uniform:
        used.add('regroup')
    if meta['swing_bars'] >= MIN_OP_BARS:
        used.add('swing')
    return used


def span(vals):
    return f'{min(vals)}..{max(vals)}' if vals else '-'


def check(s, smf, nt, meta):
    sid, bq, n_bars = s['sid'], s['bar_q'], s['bars']
    bt_ = meta['bar_ticks']
    names = [t['name'] for t in s['tracks']]
    assert sid == f"vs-{s['key'][0]}{s['key'][1]}-{MODEL}" and s['title'].endswith(' Opus')
    seconds = n_bars * bq * 60 / s['bpm']
    assert 165 <= seconds <= 200, (sid, seconds)
    # §2-1 one source voice; window covers every pass
    assert s['theme_part'] in V.MOVEMENTS[s['key']]['parts']
    wa, wb = s['theme_window']
    assert all(wa <= p['src'][0] <= p['src'][1] <= wb for p in s['passes'])
    # §2-3 tempo/meter
    ratio_t = eff_ratio(s)
    assert abs(ratio_t - 1) >= 0.15, (sid, ratio_t)
    src_den = V.MOVEMENTS[s['key']]['ts'][1]
    if src_den == 8:
        assert s['meter'] != V.MOVEMENTS[s['key']]['ts'] and 'regroup' in ops_used(s, meta), (sid, 'compound meter not regrouped')
    # §2-2 ops: every token live, rhythm_ops == measured, >= 2 classes, original-rhythm runs <= 4
    for p, tokens in zip(s['passes'], meta['fired']):
        declared = {tk for ops in p['ops'] + list(p.get('ops_at', {}).values()) for tk in ops}
        assert declared == tokens, (sid, p['at'], 'dead op tokens', sorted(declared - tokens))
    used = ops_used(s, meta)
    assert set(s['rhythm_ops']) == used, (sid, sorted(s['rhythm_ops']), sorted(used))
    classes = {RHYTHM_OP_CLASS[o] for o in used if o in RHYTHM_OP_CLASS}
    assert len(classes) >= 2, (sid, classes)
    run = max_orig_run(s, meta['orig'])
    assert run <= 4, (sid, run)
    orig_bars = sum(1 for f in meta['orig'].values() if f is True)
    # §2-5 theme ratio
    theme_pct = 100 * len(meta['orig']) / n_bars
    assert 40 <= theme_pct <= 60, (sid, theme_pct)
    # §2-4 accompaniment chord tones (bass approach notes allowed) + no rubs between accompaniment layers
    chords = meta['chords']
    acc_tracks = [i for i, t in enumerate(s['tracks']) if t['role'] != 'drums']
    by_bar = {}
    acc_n = 0
    for i in acc_tracks:
        for when, pitch in meta['pattern_notes'][i]:
            bar = min(n_bars, (when + 60) // bt_ + 1)
            root, q = chord(chords[bar - 1])
            ok = (pitch - root) % 12 in QUAL[q][0]
            if not ok and s['tracks'][i]['role'] == 'bass':
                nroot, _ = chord(chords[bar % n_bars])
                ok = (pitch + 1 - nroot) % 12 == 0
            assert ok, (sid, names[i], bar, chords[bar - 1], pitch)
            if s['tracks'][i]['role'] != 'bass':
                by_bar.setdefault(bar, {}).setdefault(i, set()).add(pitch)
            acc_n += 1
    layer_rubs = 0
    for bar, layers in by_bar.items():
        root, _ = chord(chords[bar - 1])
        keys = sorted(layers)
        for a, b in itertools.combinations(keys, 2):
            layer_rubs += rubs(layers[a], layers[b], root)
    assert layer_rubs == 0, (sid, layer_rubs)
    lead_all = [(b, e, p) for notes in meta['leads'].values() for b, e, p, _ in notes]
    bad, longn = clashes(s, chords, lead_all)
    assert bad <= max(2, longn // 10), (sid, bad, longn)
    # density: sounding layers per bar; single-layer runs outside intro/outro <= 2
    sounding = {bar: set() for bar in range(1, n_bars + 1)}
    for i, events in nt.items():
        for when, dur, pitch, _ in events:
            for bar in range(when // bt_ + 1, min(n_bars, (when + dur - 1) // bt_ + 1) + 1):
                sounding[bar].add(i)
    run1 = best1 = 0
    for bar in range(s['intro_bars'] + 1, s['outro_from']):
        run1 = run1 + 1 if len(sounding[bar]) <= 1 else 0
        best1 = max(best1, run1)
    assert best1 <= 2, (sid, 'single-layer run', best1)
    # hygiene
    overlaps = 0
    for events in nt.values():
        ends = {}
        for when, dur, pitch, _ in events:
            assert when >= 0 and dur > 0
            overlaps += int(when < ends.get(pitch, -1))
            ends[pitch] = when + dur
    assert overlaps == 0, (sid, overlaps)
    for _, text in s['markers']:
        assert bytes([0xff, 6, len(text.encode())]) + text.encode() in smf
    # attribution sits in the first instrument track, conductor holds no text/copyright meta besides the title
    first = 14 + 8 + struct.unpack('>I', smf[18:22])[0]
    assert ATTRIBUTION.encode() in smf[first:] and ATTRIBUTION.encode() not in smf[:first]
    last_end = max(n[0] + n[1] for ev in nt.values() for n in ev)
    total = n_bars * bt_
    assert total - bt_ < last_end <= total, (sid, last_end, total)
    # bounce range: the highest-numbered patch track (selected last by load_patches) sounds into the final bar
    if s['patches']:
        assert all(names[k - 1] and s['tracks'][k - 1].get('patch') == v for k, v in s['patches'].items()), sid
        assert {k for k, t in enumerate(s['tracks'], 1) if t.get('patch')} == set(s['patches']), sid
        kmax = max(s['patches'])
        end_k = max(n[0] + n[1] for n in nt[kmax - 1])
        assert end_k > total - bt_, (sid, 'last patch track ends early', end_k, total)
    # report
    sec_txt = []
    bass_i = [i for i, t in enumerate(s['tracks']) if t['role'] == 'bass']
    marks = s['markers'] + [(n_bars + 1, 'end')]
    for (b0, name), (b1, _) in zip(marks, marks[1:]):
        nb = b1 - b0
        cnt = sum(1 for ev in nt.values() for n in ev if b0 <= n[0] // bt_ + 1 < b1)
        bcnt = sum(1 for i in bass_i for n in nt[i] if b0 <= n[0] // bt_ + 1 < b1)
        sec_txt.append(f"{name}:{cnt / nb:.1f}/b{(' bass ' + format(bcnt / nb, '.1f')) if bass_i else ''}")
    trk_txt = ' '.join(f"{names[i]}={span([n[3] for n in nt[i]])}v,{len(nt[i]) / n_bars:.1f}n/b" for i in nt)
    print(f"check {sid} PASS genre='{s['genre']}' meter={s['meter'][0]}/{s['meter'][1]} bpm={s['bpm']} bars={n_bars} "
          f"len={seconds:.1f}s key={s['out_key']} window={s['theme_part']}:{wa}-{wb} map='{s['mp']['text']}' "
          f"eff_tempo={ratio_t:.2f}x ops={sorted(used)} op_bars={dict(sorted(op_bars(meta['effective']).items()))} "
          f"theme_swing_bars={meta['swing_bars']} orig_run_max={run} orig_bars={orig_bars} "
          f"theme={len(meta['orig'])}/{n_bars}={theme_pct:.0f}% clash={bad}/{longn} acc_chord_tones={acc_n} "
          f"layer_rubs={layer_rubs} single_layer_run={best1} sections=[{' '.join(sec_txt)}] tracks=[{trk_txt}] "
          f"patches={s['patches'] or '-'} overlap={overlaps} last_end={last_end}/{total}")
    return dict(theme_pct=round(theme_pct), orig_run=run, eff=round(ratio_t, 2), seconds=seconds)


# ---------------------------------------------------------------- Suno prompts
def check_prompts(required):
    path = Path(__file__).resolve().parents[1] / 'suno' / f'vivaldi_{MODEL}_v2.md'
    if not path.exists():
        assert not required, f'suno/vivaldi_{MODEL}_v2.md is missing'
        print(f'prompt-length: suno/vivaldi_{MODEL}_v2.md not written yet')
        return
    blocks = re.findall(r'^## (vs-[^\n]+)-v2\n\*\*Style\*\*\n`([^`]+)`\n\n\*\*Description\*\*\n```\n(.*?)\n```',
                        path.read_text(), re.M | re.S)
    assert [b[0] for b in blocks] == [s['sid'] for s in SKETCHES], [b[0] for b in blocks]
    for (sid, style, description), s in zip(blocks, SKETCHES):
        assert len(style) <= 300 and len(description) <= 1000, (sid, len(style), len(description))
        assert style.endswith('instrumental'), sid
        assert not re.search(r'vivaldi|season|spring|summer|autumn|winter|four seasons', style, re.I), sid
        season, roman = s['key'][0].capitalize(), ('I', 'II', 'III')[s['key'][1] - 1]
        assert re.search(rf"variation on the theme of Vivaldi's Four Seasons, {season} {roman}(?![IV])", description), sid
        assert f"{s['bpm']} BPM" in description, sid
        print(f'prompt-length {sid}-v2 Style={len(style)} Description={len(description)} PASS')


# ---------------------------------------------------------------- bounce
RESTART_EVERY = 4


def bounce(sids, log=print):
    from pipeline import produce, restart_logic
    from bounce_dh import NoScreensaver, screen_locked
    results = {}
    with NoScreensaver():
        for n, s in enumerate(sk for sk in SKETCHES if sk['sid'] in sids):
            if n and n % RESTART_EVERY == 0:
                try:
                    restart_logic(log)
                except TimeoutError as exc:
                    log(f'    logic restart skipped: {exc}')
            mid = os.path.join(SK_DIR, f"{s['sid']}-v2.mid")
            if screen_locked():
                log(f"=== {s['sid']} ABORT screen locked")
                results[s['sid']] = {'ok': False, 'stage': 'locked'}
                break
            t0 = time.time()
            log(f"=== {s['sid']} start {time.strftime('%T')} patches={s['patches'] or '-'}")
            try:
                r = produce(s['sid'], s['title'], 'v2', mid, log=lambda m: log('    ' + m), patches=s['patches'] or None)
            except TimeoutError as exc:
                r = {'ok': False, 'stage': 'lock-timeout (대기 초과)', 'msg': str(exc)}
            except Exception as exc:          # one song's AX failure must not end the batch
                r = {'ok': False, 'stage': 'exception', 'msg': f'{type(exc).__name__}: {exc}'}
            results[s['sid']] = r
            log(f"=== {s['sid']} {'OK' if r.get('ok') else 'FAIL'} {round(time.time() - t0)}s "
                f"{json.dumps(r, ensure_ascii=False, default=str)}")
    return results


def main(argv):
    flags = {a for a in argv[1:] if a.startswith('-')}
    sids = [a for a in argv[1:] if not a.startswith('-')]
    known = [s['sid'] for s in SKETCHES]
    if flags - {'--check', '--bounce'} or flags == {'--check', '--bounce'} or (sids and '--bounce' not in flags) \
            or set(sids) - set(known):
        print('usage: vivaldi_opus_v2.py [--check | --bounce [sid ...]]', file=sys.stderr)
        return 2              # before composing: a typo must never rewrite the 12 MIDI files
    check_only = '--check' in flags
    same = 0
    for s in SKETCHES:
        smf, nt, meta = compose(s['sid'])
        check(s, smf, nt, meta)
        path = os.path.join(SK_DIR, s['sid'] + '-v2.mid')
        if check_only:
            disk = open(path, 'rb').read() if os.path.exists(path) else None
            same += disk == smf
            print(f"  --check {s['sid']}-v2.mid {'identical' if disk == smf else 'DIFFERS'}")
        else:
            print('  ' + write_smf(path, smf))
    check_prompts(required=check_only)
    if check_only:
        print(f'--check identical {same}/{len(SKETCHES)}')
        return 0 if same == len(SKETCHES) else 1
    if '--bounce' in flags:
        wanted = sids or known
        results = bounce(wanted, log=lambda m: print(m, flush=True))
        print(json.dumps({k: v.get('ok') for k, v in results.items()}))
        return 0 if results and all(v.get('ok') for v in results.values()) else 1
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
