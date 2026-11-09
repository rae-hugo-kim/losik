"""Vivaldi Four Seasons — twelve theme variations, model opus (anthropic/claude-opus-5-5). Python 3.9 stdlib.

Theme notes come from vivaldi_data.MOVEMENTS (Mutopia Project; this project assumes CC BY-SA 3.0, the work
itself is public domain). Every SMF written here carries that attribution as a copyright meta event.

Suno pass rules (VIVALDI_BRIEF.md §2) are enforced by construction and re-measured by check():
  1. one source voice only (`theme_part`); no imitation, no doubled original parts, no original bass line;
  2. the theme rhythm is re-cut per output bar — ① sync/late (anticipation or back-phrasing), ② halftime / note
     values x2, ③ thin/pat (skeleton of runs: grid snap or resampling), ④ swing (lo-fi only: house swing touches
     hats and arpeggios, never the theme), plus dot (long-short pairs) and the meter regroup. At least two of ①-④ per
     song; an op counts only when it reshaped >= MIN_OP_BARS bars, every op written into a pass must move a note in
     that pass, and `rhythm_ops` must equal the measured set. A bar is "original rhythm" when its onsets are one
     uniform time-scaling (any factor) of the source onsets mapped into it; runs of those are capped at 4 bars;
  3. meter/tempo moved: 3/4, 3/8 and 12/8 are regrouped into 4/4; the effective theme tempo differs >= 15 %;
  4. harmony is re-made from a genre palette (7th/9th/sus voicings) chosen bar by bar against the melody; keys, pad,
     Tex and bass use only that chord's tones (lo-fi bass approach notes excepted) and the held layers never rub
     (minor 2nd / minor 9th) against the keys voicing;
  5. the theme fills 40-60 % of the bars; the rest is intro/break/outro and a hand-written two-bar motif.
Genres: fast movements -> deep house (DEEP_HOUSE_SET_BRIEF v2/v3 layers + drums, 96 bars),
slow movements -> lo-fi hip hop (LOFI_HIPHOP_SET_BRIEF, 56/64 bars).

    python3 vivaldi_opus.py            # compose + check the twelve sketches, write {sid}-v1.mid, measure prompts
    python3 vivaldi_opus.py --bounce [sid ...]   # then bounce through pipeline.produce (cross-session Logic lock)
"""
import json
import itertools
import math
import os
import re
import struct
import sys
import time
from collections import Counter
from pathlib import Path

from pipeline import BAR, PPQ, SK_DIR, bt, hum_t, hum_v, seed, build_smf, varlen, write_smf
import vivaldi_data as V

MODEL_ID = 'anthropic/claude-opus-5-5'
ATTRIBUTION = 'Theme: A. Vivaldi, Le quattro stagioni (public domain). Source notes: Mutopia Project, CC BY-SA 3.0'
assert len(ATTRIBUTION.encode()) < 128   # pipeline.parse_smf reads meta lengths as one byte

NOTE = {'C': 0, 'C#': 1, 'Db': 1, 'D': 2, 'D#': 3, 'Eb': 3, 'E': 4, 'F': 5, 'F#': 6, 'Gb': 6, 'G': 7,
        'G#': 8, 'Ab': 8, 'A': 9, 'A#': 10, 'Bb': 10, 'B': 11}
# quality: (chord + tension pitch classes above the root, core tones (root/3rd/5th/7th), four-voice voicing)
QUAL = {
    'maj9': ((0, 4, 7, 11, 2), (0, 4, 7, 11), (4, 7, 11, 2)),
    'maj7': ((0, 4, 7, 11), (0, 4, 7, 11), (0, 4, 7, 11)),
    '6/9': ((0, 4, 7, 9, 2), (0, 4, 7), (4, 9, 2, 7)),
    'm9': ((0, 3, 7, 10, 2), (0, 3, 7, 10), (3, 7, 10, 2)),
    'm11': ((0, 3, 7, 10, 2, 5), (0, 3, 7, 10), (3, 10, 2, 5)),
    'm7': ((0, 3, 7, 10), (0, 3, 7, 10), (0, 3, 7, 10)),
    '9': ((0, 4, 7, 10, 2), (0, 4, 7, 10), (4, 7, 10, 2)),
    '13': ((0, 4, 7, 10, 2, 9), (0, 4, 10), (4, 10, 2, 9)),
    '9sus': ((0, 5, 7, 10, 2), (0, 5, 7, 10), (5, 10, 2, 7)),
    '7b9': ((0, 4, 7, 10, 1), (0, 4, 7, 10), (4, 7, 10, 1)),
    '7b13': ((0, 4, 10, 8, 1), (0, 4, 10), (4, 8, 10, 1)),
    'm7b5': ((0, 3, 6, 10), (0, 3, 6, 10), (0, 3, 6, 10)),
}

HOUSE_MARKERS = [(1, 'intro'), (9, 'A'), (49, 'break'), (57, 'A2'), (89, 'outro')]
HOUSE_TRACKS = [('Drums', 9), ('Bass', 0), ('Keys', 1), ('Pad', 2), ('Tex', 3), ('ThemeA', 4), ('ThemeB', 5)]
LOFI_TRACKS = [('Drums', 9), ('Bass', 0), ('Keys', 1), ('Tex', 2), ('ThemeA', 3), ('ThemeB', 4)]
LOFI_PAD = ('Pad', 5)
THEME_PCS = {0, 4, 24, 27, 80, 81}
VERIFIED_PCS = dict(Keys={0, 4, 16}, Pad={88, 89, 90}, Tex={4, 16, 24, 27})   # PROMPT_GUIDELINES.md §4
# Kick, snare, clap, closed/open hat, ride, crash, toms (GM drum map).
KICK, SNARE, CLAP, HAT, OHAT, RIDE, CRASH = 36, 38, 39, 42, 46, 51, 49
TOMS = (50, 48, 47, 45, 43, 41)


def chord(name):
    m = re.match(r'^([A-G][#b]?)(.*)$', name)
    return NOTE[m.group(1)], m.group(2)


def regroup(per_beat, beats):
    """Piecewise map repeated per source beat: per_beat = ((src_q, out_beat), ...) inside one source beat."""
    span_q, span_out = per_beat[-1]
    pts = []
    for i in range(beats):
        pts += [(i * span_q + q, i * span_out + o) for q, o in per_beat[:-1]]
    return tuple(pts) + ((beats * span_q, beats * span_out),)


# Source-bar -> output-bar maps. L = source bar length (quarters), S = output beats per source bar,
# anchors = piecewise-linear (src_q, out_beat) inside one source bar, snap = output grid (beats) or None.
MAP_HALFTIME = dict(L=4, S=8, anchors=((0, 0), (4, 8)), snap=None, text='4/4 → 4/4 하프타임(음가 2배)')
MAP_LIN = dict(L=4, S=4, anchors=((0, 0), (4, 4)), snap=None, text='4/4 → 4/4 같은 마디')
MAP_34 = dict(L=3, S=4, anchors=((0, 0), (1, 1.5), (2, 2.5), (3, 4)), snap=0.25,
              text='3/4 → 4/4 재배열(2·3박을 8분 늦춰 1박 길게)')
MAP_34_EVEN = dict(L=3, S=4, anchors=((0, 0), (3, 4)), snap=None, text='3/4 → 4/4 (마디를 4박으로 늘린 뒤 재표집)')
MAP_128 = dict(L=6, S=4, anchors=regroup(((0, 0), (0.75, 0.5), (1.0, 0.75), (1.5, 1)), 4), snap=0.25,
               text='12/8 → 4/4 (점4분 = 4분, 셋잇 장단 → 8분+16분 둘)')
MAP_38_TRESILLO = dict(L=1.5, S=2, anchors=((0, 0), (0.5, 0.75), (1.0, 1.5), (1.5, 2)), snap=0.25,
                       text='3/8 두 마디 → 4/4 한 마디, 8분 셋 → 3+3+2 (트레시요)')
MAP_38_WIDE = dict(L=1.5, S=4, anchors=((0, 0), (1.5, 3)), snap=None,
                   text='3/8 → 4/4 (8분 = 4분, 4박째 숨)')
MAP_38_SKIP = dict(L=1.5, S=4, anchors=((0, 0), (0.75, 1.5), (1.0, 2.5), (1.25, 3), (1.5, 4)), snap=None,
                   text='3/8 → 4/4 (16분 여섯 → 8분 넷 + 당긴 둘)')

RHYTHM_OP_CLASS = {'sync': '①당김', 'late': '①당김', 'halftime': '②음가2배', 'x2': '②음가2배',
                   'thin8': '③런솎기', 'thin4': '③런솎기', 'pat': '③런솎기', 'swing': '④스윙'}

SKETCHES = [
    # ------------------------------------------------------------------ SPRING
    dict(key=('spring', 1), sid='vs-spring1-opus', title='Spring I Opus', genre='house', bpm=122, bars=96,
         out_key='C♯ minor', sf=4, minor=True, tr=0, theme_part='solo', theme_window=(1, 12), mp=MAP_HALFTIME,
         rhythm_ops=['halftime', 'sync', 'dot'], hr=2,
         palette=['C#m9', 'Amaj9', 'Emaj9', 'B9sus', 'F#m9', 'G#m7'], loop=['C#m9', 'Amaj9'],
         pcs=dict(Keys=4, Pad=89, Tex=16, ThemeA=0, ThemeB=80), tex='organ',
         bass='offbeat', keys='hold', brk='drumless', swing=0, hat16=True,
         passes=[dict(at=17, src=(1, 12), track='A', oct=-12, ops=[['sync:2'], ['dot', 'sync:0']]),
                 dict(at=57, src=(1, 12), track='B', oct=0, ops=[['dot'], ['sync:1,3']])],
         motif=dict(track='A', at=(9, 11, 13, 15, 41, 43, 45, 47, 81, 83, 85, 87),
                    notes=((0.5, 1, 73), (1.5, 0.5, 71), (2, 1.5, 68), (3.5, 0.5, 71),
                           (4.5, 1, 76), (5.5, 0.5, 75), (6, 1.75, 73))),
         notes='리토르넬로 G#–G#–G# / F#–E / B 를 하프타임 그랜드로, A2 는 한 옥타브 위 스퀘어. C♯ minor 딥하우스.'),
    dict(key=('spring', 2), sid='vs-spring2-opus', title='Spring II Opus', genre='lofi', bpm=78, bars=56,
         out_key='C♯ minor', sf=4, minor=True, tr=0, theme_part='solo', theme_window=(2, 10), mp=MAP_34,
         rhythm_ops=['regroup', 'sync', 'swing'], hr=1,
         palette=['C#m9', 'F#9', 'Amaj7', 'G#7b9', 'Emaj7', 'B13', 'D#m7b5'], loop=['C#m9', 'F#9', 'Amaj7', 'G#7b9'],
         pcs=dict(Keys=0, Tex=16, ThemeA=24, ThemeB=4), pad=False, energy=1, swing=27, opener='keys',
         kicks=((0, 2.5), (0, 1.75), (0, 2.75), (0, 1.5, 2.5)), ghosts=((3.75,), (0.75,), (2.25,), (0.75, 3.25)),
         comp=((0,), (0, 2.5), (0,), (0.5, 2)), tex_beats=((0,), (0,), (0,), (0,)),
         bass_moves=('5', '5', '-4', 'app'),
         break_plan=((4, ('Keys', 'Tex')), (4, ('Keys', 'Tex', 'Hats', 'Bass'))),
         passes=[dict(at=16, src=(2, 10), track='A', oct=-12, ops=[['sync:2.5'], [], ['sync:0']]),
                 dict(at=33, src=(2, 10), track='B', oct=0, ops=[['sync:1.5'], ['late:0'], []]),
                 dict(at=42, src=(2, 8), track='A', oct=-12, ops=[[], ['sync:0,2']])],
         motif=dict(track='B', at=(25, 27, 29, 31),
                    notes=((0.5, 1, 68), (1.5, 0.5, 71), (2, 1.5, 73), (4, 1, 71), (5, 1, 64), (6.5, 1.25, 66))),
         notes='잠든 목동의 solo 선율(3/4)을 4/4 로 재배열해 나일론이 부르고, A2 는 EP. 개 짖는 viola 는 쓰지 않음.'),
    dict(key=('spring', 3), sid='vs-spring3-opus', title='Spring III Opus', genre='house', bpm=120, bars=96,
         out_key='E major', sf=4, minor=False, tr=0, theme_part='solo', theme_window=(1, 12), mp=MAP_128,
         rhythm_ops=['regroup', 'sync', 'thin8'], hr=1,
         palette=['Emaj9', 'C#m9', 'Amaj9', 'F#m9', 'B9sus', 'G#m7', 'D6/9'], loop=['Emaj9', 'Emaj9', 'C#m9', 'C#m9'],
         pcs=dict(Keys=16, Pad=90, Tex=4, ThemeA=24, ThemeB=0), tex='arp',
         bass='dub', keys='dub2', brk='nokick', swing=18, hat16=False,
         passes=[dict(at=17, src=(1, 12), track='A', oct=-12, ops=[['thin8'], ['sync:2']]),
                 dict(at=29, src=(1, 12), track='A', oct=-12, ops=[['sync:0'], ['thin8', 'sync:3']]),
                 dict(at=57, src=(1, 12), track='B', oct=0, ops=[['thin8', 'sync:1'], []]),
                 dict(at=69, src=(1, 12), track='B', oct=-12, ops=[['sync:2'], ['thin8']])],
         motif=dict(track='A', at=(9, 11, 13, 15, 41, 43, 45, 47, 81, 83, 85, 87),
                    notes=((0, 0.75, 71), (0.75, 0.75, 68), (1.5, 1, 66), (3, 0.5, 64), (3.5, 0.5, 66),
                           (4.5, 1, 68), (5.5, 0.5, 71), (6, 1.75, 73))),
         notes='시칠리아나 12/8 를 4/4 셔플 하우스로(점4분→4분). 나일론 → 그랜드로 재제시.'),
    # ------------------------------------------------------------------ SUMMER
    dict(key=('summer', 1), sid='vs-summer1-opus', title='Summer I Opus', genre='lofi', bpm=80, bars=64,
         out_key='G minor', sf=-2, minor=True, tr=0, theme_part='violin1', theme_window=(1, 30), mp=MAP_38_TRESILLO,
         rhythm_ops=['regroup', 'sync', 'swing'], hr=1,
         palette=['Gm9', 'Cm9', 'Ebmaj7', 'D7b9', 'Bbmaj7', 'Am7b5', 'F9'], loop=['Gm9', 'Cm9', 'Ebmaj7', 'D7b9'],
         pcs=dict(Keys=4, Tex=27, ThemeA=0, ThemeB=81), pad=False, energy=2, swing=29, opener='tex',
         kicks=((0, 1.75, 2.5), (0, 2.75), (0, 1.5, 2.75), (0, 2.5)), ghosts=((0.75,), (2.25, 3.75), (0.75,), (2.25,)),
         comp=((0, 3.5), (1.5,), (0, 2.5), (1,)), tex_beats=((0.5, 1.5, 3), (2, 3.5), (0.5, 2), (1, 2.5)),
         bass_moves=('5', '-4', '5', 'app'),
         break_plan=((2, ('Bass',)), (2, ('Bass', 'Tex')), (4, ('Bass', 'Tex', 'Hats', 'Snare'))),
         passes=[dict(at=13, src=(1, 30), track='A', oct=0, ops=[['sync:2'], ['late:0'], ['sync:2.75'], []]),
                 dict(at=37, src=(1, 30), track='B', oct=-12, ops=[['late:0'], ['sync:2'], [], ['sync:2.75']])],
         motif=dict(track='A', at=(9, 11, 53, 55),
                    notes=((0.5, 0.5, 74), (1, 1.5, 70), (3, 0.75, 69), (4.5, 0.5, 67), (5, 1, 70), (6, 1.75, 62))),
         notes='무더위의 한숨 동기(3/8)를 두 마디씩 묶어 3+3+2 로 늘어진 로파이. 그랜드 → 낮은 소우 리드.'),
    dict(key=('summer', 2), sid='vs-summer2-opus', title='Summer II Opus', genre='lofi', bpm=72, bars=56,
         out_key='A minor', sf=0, minor=True, tr=2, theme_part='solo', theme_window=(1, 8), mp=MAP_LIN,
         rhythm_ops=['late', 'sync', 'swing'], hr=1,
         palette=['Am9', 'Dm9', 'Fmaj7', 'E7b9', 'G13', 'Cmaj7', 'Bm7b5'], loop=['Am9', 'Fmaj7', 'Dm9', 'E7b9'],
         pcs=dict(Keys=0, Tex=16, ThemeA=4, ThemeB=24, Pad=89), pad=True, energy=1, swing=25, opener='keys',
         kicks=((0, 2.75), (0, 1.5), (0, 2.5), (0, 1.75, 2.5)), ghosts=((2.25,), (3.75,), (0.75,), (2.25, 3.75)),
         comp=((0,), (0, 3), (0.5,), (0, 2.5)), tex_beats=((0,), (2,), (0,), (0,)),
         bass_moves=('5', '5', '-4', 'app'),
         break_plan=((8, ('Keys', 'Tex', 'Pad')),),
         thunder=True,
         passes=[dict(at=17, src=(1, 8), track='A', oct=-12,
                      ops=[['late:0'], ['sync:2'], ['late:1'], [], ['late:2'], ['late:0'], ['sync:2'], ['sync:1']]),
                 dict(at=33, src=(1, 8), track='B', oct=0,
                      ops=[['sync:3.5'], ['late:0'], [], [], ['late:2'], ['sync:3.5'], ['late:0'], ['late:2']]),
                 dict(at=41, src=(1, 8), track='A', oct=-12,
                      ops=[['late:0', 'sync:3.5'], ['late:2'], ['late:1'], [], ['late:0'], ['late:2'], ['sync:3.5'], ['late:1']])],
         motif=dict(track='B', at=(25, 27, 29, 31),
                    notes=((0, 1.5, 76), (1.5, 0.5, 74), (2, 2, 72), (4.5, 1, 71), (5.5, 0.5, 69), (6, 1.75, 64))),
         notes='Adagio solo 를 A minor 로 올려 EP 가 부르고, 천둥 마디(원곡 4마디 쉼)는 탐 롤로. A2 는 나일론.'),
    dict(key=('summer', 3), sid='vs-summer3-opus', title='Summer III Opus', genre='house', bpm=124, bars=96,
         out_key='G minor', sf=-2, minor=True, tr=0, theme_part='violin1', theme_window=(1, 20), mp=MAP_34_EVEN,
         rhythm_ops=['pat', 'late', 'sync'], hr=1,
         palette=['Gm9', 'Ebmaj9', 'Cm9', 'D7b9', 'Bbmaj9', 'Am7b5', 'F6/9'], loop=['Gm9', 'Gm9', 'Ebmaj9', 'Ebmaj9'],
         pcs=dict(Keys=4, Pad=89, Tex=16, ThemeA=81, ThemeB=0), tex='organ',
         bass='syncop', keys='stab3', brk='hatsbass', swing=0, hat16=True,
         passes=[dict(at=17, src=(1, 20), track='A', oct=0, ops=[['pat:0,.75,1.5,2,2.75,3.5', 'late:0'], ['pat:0,.75,1.5,2.5,3,3.5', 'sync:2.5']]),
                 dict(at=57, src=(1, 20), track='B', oct=0, ops=[['pat:0,.5,1.5,2.5,3,3.5', 'sync:2.5'], ['pat:0,.75,1.5,2,2.75,3.5', 'late:0']])],
         motif=dict(track='B', at=(9, 11, 13, 15, 37, 39, 41, 43, 45, 47, 77, 79, 81, 83, 85, 87),
                    notes=((0, 0.75, 67), (0.75, 0.75, 70), (1.5, 2, 74), (4, 0.5, 72), (4.5, 0.5, 70),
                           (5, 1, 69), (6.5, 1.25, 62))),
         notes='폭풍 프레스토의 G 연타+하행 첫음·음계 폭포를 3+3+2 스탭으로 재표집한 G minor 딥하우스.'),
    # ------------------------------------------------------------------ AUTUMN
    dict(key=('autumn', 1), sid='vs-autumn1-opus', title='Autumn I Opus', genre='house', bpm=118, bars=96,
         out_key='D minor', sf=-1, minor=True, tr=0, theme_part='violin1', theme_window=(1, 12), mp=MAP_HALFTIME,
         rhythm_ops=['halftime', 'sync'], hr=2,
         palette=['Dm9', 'Bbmaj9', 'Gm9', 'A7b13', 'Fmaj9', 'C9sus', 'Em7b5'], loop=['Dm9', 'Bbmaj9'],
         pcs=dict(Keys=0, Pad=89, Tex=4, ThemeA=24, ThemeB=80), tex='arp',
         bass='long', keys='dub2', brk='drumless', swing=10, hat16=False,
         passes=[dict(at=17, src=(1, 12), track='A', oct=0, ops=[['sync:3'], ['sync:2']]),
                 dict(at=57, src=(1, 12), track='B', oct=-12, ops=[['sync:1'], ['sync:0'], ['sync:2']])],
         motif=dict(track='A', at=(9, 11, 13, 15, 41, 43, 45, 47, 81, 83, 85, 87),
                    notes=((0.5, 0.5, 74), (1, 1, 72), (2, 1.5, 69), (4, 0.75, 65), (4.75, 0.75, 67),
                           (5.5, 2.25, 69))),
         notes='농부의 춤 A–A–A–B♭ 이웃음 동기를 하프타임 나일론으로, D minor 로 리하모. A2 는 낮은 스퀘어.'),
    dict(key=('autumn', 2), sid='vs-autumn2-opus', title='Autumn II Opus', genre='lofi', bpm=84, bars=64,
         out_key='D minor', sf=-1, minor=True, tr=0, theme_part='violin1', theme_window=(4, 14), mp=MAP_34,
         rhythm_ops=['regroup', 'sync', 'swing'], hr=1,
         palette=['Dm9', 'Bbmaj7', 'Gm9', 'A7b13', 'D9', 'E7b9', 'Ebmaj7', 'Fmaj7'], loop=['Dm9', 'Bbmaj7', 'Gm9', 'A7b13'],
         pcs=dict(Keys=4, Tex=27, ThemeA=0, ThemeB=80, Pad=89), pad=True, energy=1, swing=31, opener='tex',
         kicks=((0, 2.5), (0, 2.75), (0, 1.75), (0, 1.5, 2.75)), ghosts=((3.25,), (0.75,), (2.25, 3.75), (0.75,)),
         comp=((0,), (0.5,), (0, 2), (1.5,)), tex_beats=((0, 0.5, 1, 1.5, 2, 2.5), (0, 0.5, 1, 1.5), (0, 0.5, 1, 1.5, 2, 2.5), (0, 1, 2)),
         bass_moves=('-4', '5', '5', 'app'),
         break_plan=((4, ('Tex', 'Pad')), (4, ('Tex', 'Pad', 'Keys', 'Bass'))),
         passes=[dict(at=18, src=(4, 14), track='A', oct=-12, ops=[[]],
                      ops_at={0: ['sync:0'], 3: ['sync:2.5'], 6: ['sync:0'], 7: ['late:1.5'], 9: ['sync:2.5']}),
                 dict(at=37, src=(4, 14), track='B', oct=0, ops=[[]],
                      ops_at={2: ['sync:0'], 3: ['late:1.5'], 8: ['sync:0'], 9: ['sync16:2.5']}),
                 dict(at=48, src=(4, 12), track='A', oct=-12, ops=[[]],
                      ops_at={0: ['sync:0'], 3: ['sync:2.5'], 4: ['sync:0'], 7: ['late:1.5']})],
         motif=dict(track='B', at=(29, 31, 33, 35),
                    notes=((0, 2, 74), (2.5, 1, 72), (4, 1.5, 69), (5.5, 0.5, 70), (6, 1.75, 69))),
         notes='잠든 술꾼들의 반음 하강 상성부(vn1)를 4/4 로 재배열, 나일론 분산화음이 하프시코드 자리를 대신함.'),
    dict(key=('autumn', 3), sid='vs-autumn3-opus', title='Autumn III Opus', genre='house', bpm=122, bars=96,
         out_key='F major', sf=-1, minor=False, tr=0, theme_part='violin1', theme_window=(1, 24), mp=MAP_38_WIDE,
         rhythm_ops=['x2', 'sync', 'snap8'], hr=1,
         palette=['Fmaj9', 'Dm9', 'Bbmaj9', 'Gm9', 'C9sus', 'Am7', 'Eb6/9'], loop=['Dm9', 'Dm9', 'Bbmaj9', 'Bbmaj9'],
         pcs=dict(Keys=4, Pad=90, Tex=16, ThemeA=0, ThemeB=80), tex='organ',
         bass='offbeat', keys='stab3', brk='nokick', swing=0, hat16=False,
         passes=[dict(at=17, src=(1, 24), track='A', oct=0, ops=[['thin8'], ['sync:2'], ['thin8', 'sync:1']]),
                 dict(at=57, src=(1, 24), track='B', oct=-12, ops=[['sync:1'], ['thin8'], ['sync:2']])],
         motif=dict(track='A', at=(9, 11, 13, 15, 41, 43, 45, 47, 81, 83, 85, 87),
                    notes=((0, 0.5, 72), (0.75, 0.75, 69), (1.5, 1.5, 65), (4, 0.5, 67), (4.5, 0.5, 69),
                           (5, 1, 72), (6.5, 1.25, 74))),
         notes='사냥 호른 F–C–F–F 를 8분=4분으로 늘리고 4박째에 숨을 넣은 F major 딥하우스. A2 는 낮은 스퀘어(호른 대역).'),
    # ------------------------------------------------------------------ WINTER
    dict(key=('winter', 1), sid='vs-winter1-opus', title='Winter I Opus', genre='house', bpm=122, bars=96,
         out_key='F minor', sf=-4, minor=True, tr=0, theme_part='solo', theme_window=(4, 13), mp=MAP_HALFTIME,
         rhythm_ops=['halftime', 'pat'], hr=2,
         palette=['Fm9', 'Dbmaj9', 'Bbm9', 'C7b9', 'Bb9', 'Abmaj7', 'Gm7b5'], loop=['Fm9', 'Fm9', 'Dbmaj9', 'C7b9'],
         pcs=dict(Keys=16, Pad=89, Tex=4, ThemeA=0, ThemeB=81), tex='arp',
         bass='long', keys='hold', brk='hatsbass', swing=0, hat16=True,
         passes=[dict(at=17, src=(4, 13), track='A', oct=0, ops=[['pat:0,.75,1.5,2.5,3'], ['pat:.5,1.5,2,2.75,3.5']]),
                 dict(at=57, src=(4, 13), track='B', oct=-12, ops=[['pat:0,.5,1.5,2,3'], ['pat:.75,1.5,2.5,3.25']])],
         motif=dict(track='A', at=(9, 11, 13, 15, 37, 39, 41, 43, 45, 47, 77, 79, 81, 83, 85, 87),
                    notes=((0, 0.5, 72), (0.5, 0.5, 72), (1.5, 1, 75), (3, 0.75, 73), (4, 1.5, 72),
                           (6, 0.5, 68), (6.5, 1.25, 67))),
         notes='떨리는 8분 연타 화음(solo/vn1 4–11)과 12–13마디 아르페지오를 하프타임 당김 스탭으로. F minor.'),
    dict(key=('winter', 2), sid='vs-winter2-opus', title='Winter II Opus', genre='lofi', bpm=76, bars=56,
         out_key='E♭ major', sf=-3, minor=False, tr=0, theme_part='solo', theme_window=(1, 8), mp=MAP_HALFTIME,
         rhythm_ops=['halftime', 'dot', 'sync', 'late', 'swing'], hr=1,
         palette=['Ebmaj9', 'Cm9', 'Abmaj9', 'Bb13', 'Fm9', 'Gm7', 'Db9', 'Bb9sus'], loop=['Ebmaj9', 'Cm9', 'Fm9', 'Bb13'],
         pcs=dict(Keys=4, Tex=24, ThemeA=0, ThemeB=80), pad=False, energy=1, swing=26, opener='tex',
         kicks=((0, 1.75), (0, 2.5), (0, 1.5, 2.75), (0, 2.75)), ghosts=((2.25,), (0.75, 3.25), (2.25,), (3.75,)),
         comp=((0, 2), (1,), (0,), (0.5, 2.5)), tex_beats=((0.5, 1.5, 2.5, 3.5), (0.5, 2.5), (0.5, 1.5, 2.5, 3.5), (1.5, 3.5)),
         bass_moves=('5', 'app', '5', '-4'),
         break_plan=((4, ('Keys',)), (4, ('Keys', 'Tex', 'Hats'))),
         passes=[dict(at=9, src=(1, 8), track='A', oct=0, ops=[['dot'], ['sync:3'], ['late:0', 'dot']], ops_at={13: ['thin4']}),
                 dict(at=33, src=(1, 8), track='B', oct=-12, ops=[['sync:1,3'], ['dot'], ['late:2']],
                      ops_at={13: ['thin4', 'sync:2']})],
         motif=dict(track='B', at=(25, 27, 29, 31),
                    notes=((0.5, 1, 70), (1.5, 0.5, 72), (2, 1.5, 74), (4, 1, 72), (5, 0.5, 70), (5.5, 2.25, 67))),
         notes='Largo 선율을 하프타임으로 늘려 16분이 8분이 되게 하고 점음표·당김으로 흔든 로파이. 나일론 피치카토(자기 화음) 위 그랜드, A2 는 부드러운 스퀘어.'),
    dict(key=('winter', 3), sid='vs-winter3-opus', title='Winter III Opus', genre='house', bpm=123, bars=96,
         out_key='E minor', sf=1, minor=True, tr=-1, theme_part='solo', theme_window=(1, 24), mp=MAP_38_SKIP,
         rhythm_ops=['regroup', 'thin4', 'sync', 'late'], hr=1,
         palette=['Em9', 'Cmaj9', 'Am9', 'B7b9', 'Gmaj9', 'F#m7b5', 'D6/9'], loop=['Em9', 'Em9', 'Cmaj9', 'B7b9'],
         pcs=dict(Keys=4, Pad=90, Tex=16, ThemeA=0, ThemeB=81), tex='organ',
         bass='syncop', keys='hold', brk='drumless', swing=12, hat16=False,
         passes=[dict(at=17, src=(1, 24), track='A', oct=0, ops=[['thin4'], ['sync:0'], ['late:3'], ['thin4', 'late:1']]),
                 dict(at=57, src=(1, 24), track='B', oct=-12, ops=[['late:3'], ['thin4'], [], ['sync:0', 'late:3']])],
         motif=dict(track='A', at=(9, 11, 13, 15, 41, 43, 45, 47, 81, 83, 85, 87),
                    notes=((0, 1, 71), (1.5, 0.5, 74), (2, 1.5, 76), (4, 0.75, 74), (4.75, 0.75, 71),
                           (5.5, 2.25, 67))),
         notes='얼음 위 미끄러짐 16분 음형(C–A♭–G–F–E–F)을 E minor 로 내려 8분+당김으로 재배열한 딥하우스.'),
]


# ---------------------------------------------------------------- theme transformation
def map_x(mp, x, end=False):
    """Source quarters (from the window's first downbeat) -> output beats. With end=True a point that falls
    exactly on a source bar line belongs to the bar it closes (its last anchor), not to the next bar's downbeat —
    otherwise maps whose last anchor is short of S (MAP_38_WIDE: 1.5 -> 3) would stretch every bar-final note."""
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
    """Theme-part notes of source bars a..b (+ the pickup when a is bar 1): (x quarters, dur quarters, pitch)."""
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
    """True when the bar's output onsets are ONE uniform time-scaling plus one shift (out = a*src + c, any a > 0, any
    c) of the source onsets that the meter map sends into that bar — a tempo- and offset-invariant view of a cover
    matcher, so a bar pushed wholesale by an 8th still counts as original. One-note bars always count as original.
    'rest' when both are empty."""
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


def theme_pass(s, p):
    """One theme statement in output beats (0 = downbeat of p['at']).
    Returns (notes, per-bar original-rhythm flags, output bars, {op label: output bars where it moved/removed a note},
    set of op tokens that changed at least one note)."""
    mp = s['mp']
    shift = s['tr'] + p['oct']
    src = source_notes(s, *p['src'])
    raw = []
    for x, d, pitch in src:
        b0, e0 = map_x(mp, x), map_x(mp, x + d, end=True)
        if mp['snap']:
            g = mp['snap']
            b0, e0 = round(b0 / g) * g, max(round(e0 / g) * g, round(b0 / g) * g + g)
        raw.append(dict(b=b0, e=e0, p=pitch + shift, x=x, legato=False))
    raw.sort(key=lambda n: n['b'])
    dedup = []
    for n in raw:
        if dedup and abs(dedup[-1]['b'] - n['b']) < 1e-6:
            continue
        dedup.append(n)
    raw = dedup
    n_out = (p['src'][1] - p['src'][0] + 1) * mp['S'] / 4
    assert n_out == int(n_out)
    n_out = int(n_out)
    notes = [dict(n) for n in raw]
    effective = {}
    fired = set()
    for k in range(n_out):
        tokens = p.get('ops_at', {}).get(k, p['ops'][k % len(p['ops'])])
        for index, (token, (name, args)) in enumerate(zip(tokens, parse_ops(tokens))):
            before = [(n['b'], n['p']) for n in notes]
            label = name.replace('16', '')
            in_bar = [n for n in notes if 4 * k - 1e-9 <= n['b'] < 4 * k + 4 - 1e-9]
            if name in ('thin8', 'thin4'):
                # Skeleton = the first note of each grid cell, moved to the cell start (never into the next bar); it
                # absorbs the span of the notes it replaces but never rings past them. Counted as ③ only when a note
                # was actually removed — a bar that is merely snapped onto the grid is reported as 'snap'.
                g = 0.5 if name == 'thin8' else 1.0
                kept = {}
                for n in in_bar:
                    slot = math.floor(n['b'] / g + 1e-9)
                    if slot in kept:
                        kept[slot]['e'] = max(kept[slot]['e'], n['e'])
                        notes.remove(n)
                        continue
                    kept[slot] = n
                    n['b'] = slot * g
                if len(kept) == len(in_bar):
                    label = name.replace('thin', 'snap')
            elif name in ('sync', 'sync16'):
                amt = 0.5 if name == 'sync' else 0.25
                for n in in_bar:
                    rel = n['b'] - 4 * k
                    if any(abs(rel - a) < 1e-6 for a in args):
                        prev = [m for m in notes if m['b'] < n['b'] - 1e-6]
                        if not prev or prev[-1]['b'] < n['b'] - amt - 1e-6:
                            n['b'] -= amt
            elif name in ('late', 'late16'):
                # Back-phrasing: the note on a listed beat arrives an 8th (16th) late, keeping its length.
                amt = 0.5 if name == 'late' else 0.25
                for n in in_bar:
                    rel = n['b'] - 4 * k
                    if any(abs(rel - a) < 1e-6 for a in args):
                        nxt = [m for m in notes if m['b'] > n['b'] + 1e-6]
                        if not nxt or nxt[0]['b'] > n['b'] + amt + 0.25 - 1e-6:
                            n['b'] += amt
                            n['e'] += amt
            elif name == 'dot':
                for n in in_bar:
                    rel = n['b'] - 4 * k
                    if abs(rel % 1 - 0.5) < 1e-6:
                        prev = [m for m in notes if m['b'] < n['b'] - 1e-6]
                        nxt = [m for m in notes if m['b'] > n['b'] + 1e-6]
                        if prev and abs(prev[-1]['b'] - (n['b'] - 0.5)) < 1e-6 and (not nxt or nxt[0]['b'] > n['b'] + 0.25 + 1e-6):
                            n['b'] += 0.25
            elif name == 'pat':
                # Resamples the mapped source, so it must come first in its bar (it would erase earlier ops).
                assert index == 0, (s['sid'], p['at'], k, 'pat must be the first op of its bar')
                for n in in_bar:
                    notes.remove(n)
                for a in args:
                    t = 4 * k + a
                    sounding = [m for m in raw if m['b'] <= t + 1e-6 and t < m['e'] - 1e-6]
                    if sounding:
                        src_note = sounding[-1]
                        notes.append(dict(b=t, e=t + 0.5, p=src_note['p'], x=src_note['x'], legato=True))
            else:
                raise AssertionError(name)
            notes.sort(key=lambda n: n['b'])
            if [(n['b'], n['p']) for n in notes] != before:
                effective.setdefault(label, set()).add(k)
                fired.add(token)
        notes = [n for i, n in enumerate(notes) if i == 0 or n['b'] > notes[i - 1]['b'] + 1e-6]
    # durations: never overlap the next onset; resampled (pat) stabs ring legato up to the next onset.
    for i, n in enumerate(notes):
        nxt = notes[i + 1]['b'] if i + 1 < len(notes) else n_out * 4
        end = nxt - 0.06 if n['legato'] else min(n['e'], nxt - 0.06)
        n['e'] = max(n['b'] + 0.15, min(end, n['b'] + 3.5, n_out * 4 - 0.05))
    span_q = 4 * mp['L'] / mp['S']          # source quarters that the meter map sends into one output bar
    orig = []
    for k in range(n_out):
        ref = [x - k * span_q for x, _, _ in src if k * span_q - 1e-9 <= x < (k + 1) * span_q - 1e-9]
        out = [n['b'] - 4 * k for n in notes if 4 * k - 1e-9 <= n['b'] < 4 * k + 4 - 1e-9]
        orig.append(same_rhythm(ref, out))
    return notes, orig, n_out, effective, fired


# ---------------------------------------------------------------- harmony
def voicing(root, q, lo, hi, prev):
    """Four voices, one per voicing pitch class, inside [lo, hi]; no minor 2nd / minor 9th between any pair,
    span <= 16; nearest to the previous voicing (voice leading) or to the band centre."""
    pcs = [(root + iv) % 12 for iv in QUAL[q][2]]
    options = [[p for p in range(lo, hi + 1) if p % 12 == pc] for pc in pcs]
    cands = []
    for combo in itertools.product(*options):
        cand = tuple(sorted(combo))
        if cand[-1] - cand[0] > 16 or min(b - a for a, b in zip(cand, cand[1:])) < 2:
            continue
        if any((b - a) in (1, 13) for a, b in itertools.combinations(cand, 2)):
            continue
        cands.append(cand)
    assert cands, (root, q, lo, hi)
    center = (lo + hi) / 2
    if prev:
        return min(cands, key=lambda c: (sum(abs(a - b) for a, b in zip(c, prev)) + abs(sum(c) / 4 - center), c))
    return min(cands, key=lambda c: (abs(sum(c) / 4 - center), c))


def harmonize(s, lead):
    """Bar-by-bar chord names. Units of s['hr'] bars; lead = [(abs_beat, end_beat, pitch)] of theme+motif notes."""
    n_bars, hr = s['bars'], s['hr']
    names = []
    prev = None
    for u in range((n_bars + hr - 1) // hr):
        u0, u1 = u * hr * 4, (u + 1) * hr * 4
        loop_name = s['loop'][u % len(s['loop'])]
        w = []
        for b, e, pitch in lead:
            ov = min(e, u1) - max(b, u0)
            if ov <= 0:
                continue
            strong = 1.5 if (u0 <= b and abs(b % 2) < 1e-6) else 1.0
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
        names += [name] * hr
    return names[:n_bars]


def clashes(chords_by_bar, lead):
    """Lead notes >= 1 beat whose pitch class is an avoid tone (semitone above a core tone) of the chord under
    most of the note (the bar of its midpoint — an anticipated note is judged against the bar it rings into)."""
    bad, total = 0, 0
    for b, e, pitch in lead:
        if e - b < 1 - 1e-6:
            continue
        total += 1
        root, q = chord(chords_by_bar[min(len(chords_by_bar) - 1, int((b + e) / 2 // 4))])
        tones, core, _ = QUAL[q]
        rel = (pitch - root) % 12
        bad += int(rel not in tones and (rel - 1) % 12 in core)
    return bad, total


def fifth_iv(q):
    """The chord's own fifth above the root (7, or 6 for m7b5), or None when the chord has no fifth (7b13)."""
    tones = QUAL[q][0]
    return 7 if 7 in tones else 6 if 6 in tones else None


def pad_ivs(q, three):
    """Pad intervals above the root from the chord itself: root + fifth (b7 when the chord has none)
    [+ natural 9th, or the chord's third when the 9th is altered or absent]."""
    tones, core, _ = QUAL[q]
    fifth = fifth_iv(q) or 10
    if not three:
        return (0, fifth)
    upper = 14 if 2 in tones else 12 + next(t for t in (3, 4) if t in core)
    return (0, fifth, upper)


def rubs(lows, highs, root):
    """Minor-2nd / minor-9th contacts between two pitch sets. The one allowed contact is the chord's own
    root -> b9 a minor 9th apart (the defining sound of a 7b9 chord)."""
    count = 0
    for x in lows:
        for y in highs:
            lo, hi = min(x, y), max(x, y)
            if hi - lo == 1 or (hi - lo == 13 and not ((lo - root) % 12 == 0 and (hi - root) % 12 == 1)):
                count += 1
    return count


def place_pad(root, q, three, top, against):
    """Pad pitches (chord-derived intervals) at the highest octave whose top voice is <= `top` and that rubs
    nothing in `against` (rubs() exempts root -> b9); falls back to dropping the upper voice, then to one octave
    lower (never below C2), and as a last resort keeps the two-voice pad at the normal octave."""
    ivs = pad_ivs(q, three)
    low = 36 + root
    while low + 12 + ivs[-1] <= top:
        low += 12
    options = [tuple(low + iv for iv in ivs), tuple(low + iv for iv in ivs[:2])]
    if low - 12 >= 36:
        options += [tuple(low - 12 + iv for iv in ivs), tuple(low - 12 + iv for iv in ivs[:2])]
    for pitches in options:
        if not rubs(pitches, against, root):
            return pitches
    return options[1]


# ---------------------------------------------------------------- arrangement helpers
def lofi_markers(n_bars):
    return [(1, 'intro'), (9, 'A'), (25 if n_bars == 56 else 29, 'break'),
            (33 if n_bars == 56 else 37, 'A2'), (n_bars - 7, 'outro')]


def markers(s):
    return HOUSE_MARKERS if s['genre'] == 'house' else lofi_markers(s['bars'])


def tracks(s):
    if s['genre'] == 'house':
        return HOUSE_TRACKS
    return LOFI_TRACKS + ([LOFI_PAD] if s['pad'] else [])


def track_index(s, name):
    return [t[0] for t in tracks(s)].index(name)


def lead_plan(s):
    """Theme passes + motif placements -> ({'A': [(abs_beat, end, pitch, kind)], 'B': [...]},
    original-rhythm flag per theme bar, per-pass {op label: output bars it changed}, per-pass fired op tokens,
    number of theme bars with an off-beat 8th onset (where lo-fi swing reaches the theme))."""
    out = {'A': [], 'B': []}
    orig_by_bar = {}
    effective, fired = [], []
    swing_bars = set()
    for p in s['passes']:
        notes, orig, n_out, eff, tokens = theme_pass(s, p)
        effective.append(eff)
        fired.append(tokens)
        base = (p['at'] - 1) * 4
        for n in notes:
            out[p['track']].append((base + n['b'], base + n['e'], n['p'], 'theme'))
            if abs(n['b'] % 1 - 0.5) < 1e-6:
                swing_bars.add(p['at'] + int(n['b'] // 4))
        for k, flag in enumerate(orig):
            assert p['at'] + k not in orig_by_bar, ('theme passes overlap', s['sid'], p['at'] + k)
            orig_by_bar[p['at'] + k] = flag
    mo = s['motif']
    for at in mo['at']:
        base = (at - 1) * 4
        for b, d, pitch in mo['notes']:
            out[mo['track']].append((base + b, base + b + d, pitch, 'motif'))
    for k in out:
        out[k].sort()
        # The earlier note yields to the next one where two placements meet (a theme pickup inside the motif's
        # last bar, or a pass whose first downbeat is anticipated into the previous pass's last bar).
        for i, (a, b) in enumerate(zip(out[k], out[k][1:])):
            if a[1] > b[0] - 0.06:
                out[k][i] = (a[0], b[0] - 0.06, a[2], a[3])
                assert out[k][i][1] - a[0] >= 0.15, ('note squeezed', s['sid'], a, b)
        for a, b in zip(out[k], out[k][1:]):
            assert a[1] <= b[0] + 1e-6, ('lead overlap', s['sid'], k, a, b)
    return out, orig_by_bar, effective, fired, len(swing_bars)



def house_layers(s, bar, theme_here):
    n = s['bars']
    if 49 <= bar < 57:
        first = bar < 53
        return {'drumless': ({'Pad', 'Keys'}, {'Pad', 'Keys', 'Hats', 'Kick'}),
                'nokick': ({'Pad', 'Keys', 'Hats', 'Back'}, {'Pad', 'Keys', 'Hats', 'Back'}),
                'hatsbass': ({'Pad', 'Hats', 'Bass'}, {'Pad', 'Hats', 'Bass', 'Keys', 'Back'})}[s['brk']][0 if first else 1]
    layers = {'Hats'}
    if bar <= n - 4:
        layers.add('Pad')
    if bar >= 5:
        layers.add('Kick')
    if bar >= 9:
        layers.update(('Back', 'Bass'))
    if 9 <= bar < 89:
        layers.add('Keys')
        # Organ Tex is one more held layer (always in A/A2); the EP arpeggio steps aside while the theme sings.
        if s['tex'] == 'organ' or not theme_here:
            layers.add('Tex')
    if 57 <= bar < 89:
        layers.add('Ride')
    return layers


def lofi_layers(s, bar):
    n = s['bars']
    _, _, (brk, _), (a2, _), (outro, _) = lofi_markers(n)
    if brk <= bar < a2:
        off = bar - brk
        for length, layers in s['break_plan']:
            if off < length:
                return set(layers)
            off -= length
        raise AssertionError('break plan shorter than eight bars')
    tex_open = s['opener'] == 'tex'
    layers = set()
    if bar >= (5 if tex_open else 1):
        layers.add('Keys')
    if (1 if tex_open else 9) <= bar < outro:
        layers.add('Tex')
    if bar >= 3:
        layers.add('Hats')
    if bar >= 5:
        layers.update(('Kick', 'Snare'))
    if 9 <= bar <= n - 4:
        layers.add('Bass')
    if s['pad'] and 9 <= bar < outro:
        layers.add('Pad')
    if s['energy'] == 1 and bar > n - 4:
        layers.difference_update(('Kick', 'Snare', 'Hats'))
    return layers


def compose(sid):
    s = next(s for s in SKETCHES if s['sid'] == sid)
    seed(271027 + sum(map(ord, sid)))
    leads, orig_by_bar, effective, fired, swing_bars = lead_plan(s)
    lead_all = [(b, e, p) for notes in leads.values() for b, e, p, _ in notes]
    chords = harmonize(s, lead_all)
    tbars = set(orig_by_bar)   # bars inside a theme statement (rests of the source phrase included)
    trs = tracks(s)
    nt = {i: [] for i in range(len(trs))}
    cc = {i: [] for i in range(len(trs))}
    pcs = {0: 16 if s['genre'] == 'house' else 0, 1: 38 if s['genre'] == 'house' else 33}
    for name in ('Keys', 'Pad', 'Tex', 'ThemeA', 'ThemeB'):
        if name in [t[0] for t in trs]:
            pcs[track_index(s, name)] = s['pcs'][name]
    meta = dict(chords=chords, leads=leads, orig=orig_by_bar, effective=effective, fired=fired, swing_bars=swing_bars)
    if s['genre'] == 'house':
        house_body(s, nt, cc, chords, tbars)
    else:
        lofi_body(s, nt, cc, chords, leads)
    lead_tracks(s, nt, leads)
    for events in nt.values():
        events.sort()
    for events in cc.values():
        events.sort()
    return (nt, cc, pcs, s['bars'], s['bpm'], s['title'], s['sf'], s['minor']), meta


def lead_tracks(s, nt, leads):
    house = s['genre'] == 'house'
    for k in ('A', 'B'):
        ti = track_index(s, 'Theme' + k)
        events = []
        for b, e, pitch, kind in leads[k]:
            when = int(round(b * PPQ))
            end = int(round(e * PPQ))
            if house:
                when = hum_t(when + 6, 6)
                base = 82 if abs(b % 4) < 1e-6 else 78
                vel = max(70, min(90, hum_v(base, 6)))
            else:
                swing = s['swing'] if abs(b % 1 - 0.5) < 1e-6 else 0
                when = hum_t(when + 14 + swing, 10)
                base = 74 if abs(b % 4) < 1e-6 else 70
                vel = max(60, min(82, hum_v(base, 7)))
            events.append([max(0, when), end, pitch, vel])
        events.sort()
        for i, ev in enumerate(events):
            nxt = events[i + 1][0] if i + 1 < len(events) else s['bars'] * BAR
            ev[1] = min(ev[1], nxt - 30, s['bars'] * BAR - 10)
            assert ev[1] - ev[0] >= 30, (s['sid'], k, ev)
        nt[ti] = [(w, end - w, pitch, vel) for w, end, pitch, vel in events]


def bass_pitch(root_pc, lo=28, hi=39):
    p = lo + (root_pc - lo) % 12
    return p if p <= hi else p - 12


def pedal(cc, ti, bar, onsets):
    cc[ti].append((bt(bar), 64, 0))
    for when in onsets:
        cc[ti].extend(((max(bt(bar), when - 1), 64, 0), (when + 1, 64, 100)))
    cc[ti].append((bt(bar + 1) - 2, 64, 0))


def house_body(s, nt, cc, chords, tbars):
    n = s['bars']
    dr, ba, ke, pa, tx = (track_index(s, x) for x in ('Drums', 'Bass', 'Keys', 'Pad', 'Tex'))
    prev_voicing = None
    sw = s['swing']

    def clamp(v, lo, hi):
        return max(lo, min(hi, v))

    def hv(v, lo, hi):
        return clamp(hum_v(v, 8), lo, hi)

    def at(bar, step, swung=True):
        shift = (sw if step % 4 == 2 else sw // 2 if step % 2 else 0) if swung else 0
        return hum_t(bt(bar) + step * (PPQ // 4) + shift, 8)

    for bar in range(1, n + 1):
        layers = house_layers(s, bar, bar in tbars)
        root, q = chord(chords[bar - 1])
        voic = voicing(root, q, 60, 84, prev_voicing)
        prev_voicing = voic
        end_bar = bt(bar + 1) - 20
        # ---- drums: kick (4otf), snare+clap layer on 2/4, closed hats, open hats on & of 2/4, ride in A2, toms, crash
        if 'Kick' in layers:
            for beat in range(4):
                t = hum_t(bt(bar, beat), 8)
                nt[dr].append((t, 100, KICK, hv(109, 106, 112) if beat == 0 else hv(102, 100, 105)))
        if 'Back' in layers:
            for beat in (1, 3):
                t = hum_t(bt(bar, beat), 8)
                nt[dr].append((t, 110, SNARE, hv(94, 88, 100)))
                nt[dr].append((t, 110, CLAP, hv(86, 80, 92)))
        fill = bar in (16, 48, 88)
        if 'Hats' in layers:
            ride = 'Ride' in layers
            for step in (0, 4, 8, 12):
                if bar == 57 and step == 0:
                    continue
                if ride:
                    nt[dr].append((hum_t(bt(bar) + step * 120, 8), int(PPQ * 0.9), RIDE, hv(68, 60, 75)))
                else:
                    nt[dr].append((at(bar, step), 50, HAT, hv(56, 50, 62)))
            for step in (2, 10):
                nt[dr].append((at(bar, step), 50, HAT, hv(82, 74, 90)))
            for step in (6, 14):
                nt[dr].append((at(bar, step), 180, OHAT, hv(72, 65, 80)))
            if s['hat16'] and not fill:
                nt[dr].append((at(bar, 13), 40, HAT, hv(50, 45, 56)))
        if fill and 'Kick' in layers:
            for step, pitch in ((13, 45), (15, 43)):
                nt[dr].append((at(bar, step, swung=False), 140, pitch, hv(90, 80, 100)))
        if bar == 57:
            nt[dr].append((bt(bar), PPQ, CRASH, 80))
        # ---- bass: sub register, style per song
        if 'Bass' in layers:
            r = bass_pitch(root)
            f = fifth_iv(q)   # the chord's own fifth (b5 on m7b5); a fifthless 7b13 repeats the root instead
            fifth_below = r if f is None else r + f - 12 if r + f - 12 >= 28 else r + f
            cells = {'offbeat': ((0.5, 0.4, r), (1.5, 0.4, r), (2.5, 0.4, r), (3.5, 0.4, fifth_below)),
                     'long': ((0, 3.0, r), (3.5, 0.4, r + 12 if r + 12 <= 45 else r)),
                     'dub': ((0, 0.9, r), (2.5, 0.45, r), (3, 0.8, fifth_below)),
                     'syncop': ((0, 0.6, r), (0.75, 0.5, r), (2.5, 1.0, fifth_below))}[s['bass']]
            for beat, dur, pitch in cells:
                t = hum_t(bt(bar, beat) + 4, 6)
                nt[ba].append((t, min(int(dur * PPQ), end_bar - t), pitch, hv(82, 74, 90)))
        # ---- keys: hold / dub2 / stab3 with CC64 per bar
        if 'Keys' in layers:
            hits = {'hold': ((0, 3.8),), 'dub2': ((0, 1.5), (2.5, 1.3)), 'stab3': ((0, 0.9), (1.5, 0.9), (3, 0.8))}[s['keys']]
            onsets = []
            for i, (beat, dur) in enumerate(hits):
                t = hum_t(bt(bar, beat) + 8, 6)
                onsets.append(t)
                for pitch in voic:
                    nt[ke].append((t, min(int(dur * PPQ), end_bar - t), pitch, hv(84 if i == 0 else 80, 72, 92)))
            pedal(cc, ke, bar, onsets)
        # ---- tex pitches: chord tones folded into C4–C5 only where the fold rubs nothing in the keys voicing
        fold = lambda p: p - 12 if p > 72 and not rubs((p - 12,), voic, root) else p
        if s['tex'] == 'arp':
            tex_pitches = sorted({fold(p) for p in voic})
        else:
            tex_pitches = sorted({fold(voic[0]), fold(voic[2])})
        # ---- pad: root + the chord's own 5th + 9th (the 3rd when the 9th is altered), from bar 1, placed so it
        # rubs nothing in the keys voicing or the Tex layer (the house v2 band tops out near A4)
        if 'Pad' in layers:
            t = hum_t(bt(bar) + 2, 4)
            for pitch in place_pad(root, q, True, 69, tuple(voic) + tuple(tex_pitches)):
                nt[pa].append((t, end_bar - t, pitch, hv(64, 55, 72)))
        # ---- tex: EP 8th arpeggio inside one octave, or organ long chord one layer more
        if 'Tex' in layers:
            if s['tex'] == 'arp':
                order = [0, 2, 1, 3, 2, 1, 3, 1] if len(tex_pitches) == 4 else [0, 1, 2, 1, 0, 2, 1, 2]
                for i in range(8):
                    t = at(bar, i * 2)
                    nt[tx].append((t, 200, tex_pitches[order[i] % len(tex_pitches)], hv(62, 55, 70)))
            else:
                t = hum_t(bt(bar, 0.5), 6)
                for pitch in tex_pitches:
                    nt[tx].append((t, bt(bar, 3.8) - t, pitch, hv(62, 55, 70)))


def lofi_body(s, nt, cc, chords, leads):
    n = s['bars']
    dr, ba, ke, tx = (track_index(s, x) for x in ('Drums', 'Bass', 'Keys', 'Tex'))
    pa = track_index(s, 'Pad') if s['pad'] else None
    a2 = lofi_markers(n)[3][0]
    swing = s['swing']
    prev_voicing = None
    thunder = set()
    if s.get('thunder'):
        for p in s['passes']:
            for k in range(p['src'][1] - p['src'][0] + 1):
                src_bar = p['src'][0] + k
                if not [1 for x, _, _ in source_notes(s, src_bar, src_bar) if x >= 0]:
                    thunder.add(p['at'] + k)

    def tick(bar, beat, swung=False):
        delay = swing if swung and abs(beat % 1 - 0.5) < 1e-6 else 0
        return hum_t(bt(bar, beat) + 14 + delay, 12)

    def velocity(base, low, high):
        return max(low, min(high, hum_v(base, 10)))

    for bar in range(1, n + 1):
        phase = (bar - 1) % 4
        root, q = chord(chords[bar - 1])
        voic = voicing(root, q, 48, 72, prev_voicing)
        prev_voicing = voic
        layers = lofi_layers(s, bar)
        end_bar = bt(bar + 1) - 24
        occupied = set()
        cell = s['kicks'][phase]
        kick_times = [tick(bar, beat) for beat in cell]

        def drum(beat, pitch, base, low, high, swung=False, dur=70):
            slot = round(beat * 4)
            assert slot not in occupied, (s['sid'], bar, beat, pitch)
            occupied.add(slot)
            when = tick(bar, beat, swung)
            nt[dr].append((when, min(dur, end_bar - when), pitch, velocity(base, low, high)))

        if 'Kick' in layers:
            kv = velocity(98 + s['energy'], 96, 104)
            for beat, when in zip(cell, kick_times):
                occupied.add(round(beat * 4))
                nt[dr].append((when, 80, KICK, kv + (6 if beat == 0 else 0)))
        if 'Snare' in layers:
            for beat in (1, 3):
                drum(beat, SNARE, 88 + 2 * s['energy'], 86, 100)
            for beat in s['ghosts'][phase]:
                drum(beat, SNARE, 45, 38, 52)
        if bar == a2:
            drum(0.5, CRASH, 62, 55, 70, dur=400)
        if bar in thunder and 'Kick' in layers:
            # Summer II: the source's silent bar (orchestral thunder) becomes a low tom roll from beat 3 (16th 8).
            for i, slot in enumerate(range(8, 16)):
                if slot in occupied:
                    continue
                drum(slot / 4, TOMS[min(5, 2 + i // 2)], 58 + i * 4, 56, 90)
        elif 'Hats' in layers:
            for eighth in range(8):
                beat = eighth / 2
                if round(beat * 4) in occupied:
                    continue
                offbeat = eighth % 2 == 1
                open_hat = phase == 3 and eighth == 7
                drum(beat, OHAT if open_hat else HAT, 76 if offbeat else 54,
                     68 if offbeat else 48, 84 if offbeat else 60, swung=offbeat, dur=145 if open_hat else 70)
        if 'Bass' in layers:
            r = bass_pitch(root, 28, 40)
            move = s['bass_moves'][phase]
            f = fifth_iv(q)   # the chord's own fifth (b5 on m7b5); a fifthless 7b13 takes the octave instead
            if move == 'app':
                nroot, _ = chord(chords[bar % n])
                second = bass_pitch(nroot, 29, 41) - 1
            elif f is None:
                second = r + 12 if r + 12 <= 48 else r
            elif move == '-4':
                second = r + f - 12 if r + f - 12 >= 28 else r + f
            else:
                second = r + f
            pitches = [r] + [second] * (len(cell) - 2)
            for i, pitch in enumerate(pitches):
                nt[ba].append((kick_times[i], kick_times[i + 1] - 40 - kick_times[i], pitch, velocity(70 + s['energy'], 60, 82)))
        if 'Keys' in layers:
            beats = s['comp'][phase]
            onsets = [tick(bar, beat) for beat in beats]
            for i, when in enumerate(onsets):
                nxt = onsets[i + 1] if i + 1 < len(onsets) else bt(bar + 1)
                for pitch in voic:
                    nt[ke].append((when, min(nxt - 50, end_bar) - when, pitch, velocity(82 if i == 0 else 78, 72, 92)))
            pedal(cc, ke, bar, onsets)
        if 'Tex' in layers:
            beats = s['tex_beats'][phase]
            onsets = [tick(bar, beat, swung=True) for beat in beats]
            if s['pcs']['Tex'] == 16:
                for pitch in (voic[0], voic[2]):
                    nt[tx].append((onsets[0], bt(bar, 3.8) - onsets[0], pitch, velocity(61, 55, 72)))
            else:
                tones = sorted(voic)
                for i, when in enumerate(onsets):
                    nxt = onsets[i + 1] if i + 1 < len(onsets) else bt(bar + 1)
                    pitch = tones[(i + phase) % 4]
                    dur = min(nxt - 40, when + 300) - when
                    nt[tx].append((when, dur, pitch if pitch <= 76 else pitch - 12, velocity(63, 55, 72)))
        if 'Pad' in layers:
            # Low root + the chord's own fifth (top <= C4), placed so it rubs nothing in the keys voicing.
            when = tick(bar, 0)
            for pitch in place_pad(root, q, False, 60, voic):
                nt[pa].append((when, end_bar - when, pitch, velocity(52, 45, 60)))


# ---------------------------------------------------------------- SMF attribution + checks
def with_attribution(smf):
    """Prepend a copyright meta event (delta 0) to the conductor track."""
    pos = 14
    assert smf[pos:pos + 4] == b'MTrk'
    ln = struct.unpack('>I', smf[pos + 4:pos + 8])[0]
    text = ATTRIBUTION.encode()
    ev = b'\x00\xff\x02' + varlen(len(text)) + text
    body = ev + smf[pos + 8:pos + 8 + ln]
    return smf[:pos] + b'MTrk' + struct.pack('>I', len(body)) + body + smf[pos + 8 + ln:]


def span(vals):
    return f'{min(vals)}..{max(vals)}' if vals else '-'


def eff_ratio(s):
    """Effective theme tempo (source quarters per minute) / source tempo."""
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


MIN_OP_BARS = 4   # a rhythm op counts toward §2-2 only when it reshaped at least this many output bars


def op_bars(effective):
    """Per-pass {op: bars} -> {op: total output bars changed across the song}."""
    total = Counter()
    for eff in effective:
        for name, bars in eff.items():
            total[name] += len(bars)
    return total


def ops_used(s, effective, swing_bars):
    """Map-level transforms + the per-bar ops that reshaped at least MIN_OP_BARS output bars + swing when it reaches
    the THEME in at least MIN_OP_BARS bars (lo-fi only: house swing touches hats/arpeggios, never the theme)."""
    used = {name for name, n in op_bars(effective).items() if n >= MIN_OP_BARS}
    if s['mp'] is MAP_HALFTIME:
        used.add('halftime')
    if s['mp'] is MAP_38_WIDE:
        used.add('x2')
    if any(s['mp'] is m for m in (MAP_34, MAP_128, MAP_38_TRESILLO, MAP_38_SKIP)):
        used.add('regroup')
    if s['genre'] == 'lofi' and swing_bars >= MIN_OP_BARS:
        used.add('swing')
    return used


def check(s, result, meta, smf):
    nt, cc, pcs, n_bars, bpm, title, sf, minor = result
    house = s['genre'] == 'house'
    assert (n_bars, bpm, title) == (s['bars'], s['bpm'], s['title'])
    assert s['sid'] == f"vs-{s['key'][0]}{s['key'][1]}-opus" and title.endswith(' Opus')
    assert n_bars == (96 if house else 56 if bpm <= 78 else 64)
    assert s['pcs']['ThemeA'] in THEME_PCS and s['pcs']['ThemeB'] in THEME_PCS
    assert s['pcs']['ThemeA'] != s['pcs']['ThemeB']
    # Every program is a PROMPT_GUIDELINES §4 verified patch (drums: Tough Kit 16 / SoCal 0).
    expect = {0: 16 if house else 0, 1: 38 if house else 33}
    assert all(pcs[i] == v for i, v in expect.items())
    assert all(pcs[track_index(s, n)] in VERIFIED_PCS[n] for n in ('Keys', 'Pad', 'Tex') if n in [t[0] for t in tracks(s)])
    # §2-1: one source voice; §2-3: tempo moved >= 15 %; §2-2: >= 2 rhythm op classes, original rhythm runs <= 4 bars.
    assert s['theme_part'] in V.MOVEMENTS[s['key']]['parts']
    wa, wb = s['theme_window']
    assert all(wa <= p['src'][0] <= p['src'][1] <= wb for p in s['passes'])
    ratio_t = eff_ratio(s)
    assert abs(ratio_t - 1) >= 0.15, (s['sid'], ratio_t)
    # Every op TOKEN (name + arguments) written into a pass must move or remove a note in that pass ...
    for p, tokens in zip(s['passes'], meta['fired']):
        declared = {t for ops in p['ops'] + list(p.get('ops_at', {}).values()) for t in ops}
        assert declared == tokens, (s['sid'], p['at'], 'dead op tokens', sorted(declared - tokens))
    # ... and `rhythm_ops` names exactly the transforms that reshaped the theme (>= MIN_OP_BARS bars each).
    used = ops_used(s, meta['effective'], meta['swing_bars'])
    assert set(s['rhythm_ops']) == used, (s['sid'], sorted(s['rhythm_ops']), sorted(used))
    classes = {RHYTHM_OP_CLASS[o] for o in used if o in RHYTHM_OP_CLASS}
    assert len(classes) >= 2, (s['sid'], classes)
    run = max_orig_run(s, meta['orig'])
    assert run <= 4, (s['sid'], run)
    orig_bars = sum(1 for f in meta['orig'].values() if f is True)
    tb = set(meta['orig'])
    theme_pct = 100 * len(tb) / n_bars
    assert 40 <= theme_pct <= 60, (s['sid'], theme_pct)
    # §2-4: harmony is chosen from the genre palette (by construction); every accompaniment note is a tone of the
    # bar's chord, except lo-fi bass approach notes a semitone below the next bar's root. The source cello/vn2/viola
    # are never read (source_notes reads parts[theme_part] only).
    def bar_of(tick):
        return min(n_bars, (tick + 60) // BAR + 1)
    acc = 0
    for name in ('Keys', 'Pad', 'Tex', 'Bass'):
        if name not in [t[0] for t in tracks(s)]:
            continue
        for when, _, pitch, _ in nt[track_index(s, name)]:
            bar = bar_of(when)
            root, q = chord(meta['chords'][bar - 1])
            ok = (pitch - root) % 12 in QUAL[q][0]
            if not ok and name == 'Bass' and not house:
                nroot, _ = chord(meta['chords'][bar % n_bars])
                ok = (pitch + 1 - nroot) % 12 == 0
            assert ok, (s['sid'], name, bar, meta['chords'][bar - 1], pitch)
            acc += 1
    # No minor 2nd / minor 9th between the held layers (Pad, Tex) and the keys voicing in any bar, except the
    # chord's own root -> b9 (see rubs()); the keys voicing itself is rub-free by construction (voicing()).
    layer_rubs = 0
    by_bar = {}
    for name in ('Keys', 'Pad', 'Tex'):
        if name in [t[0] for t in tracks(s)]:
            for when, _, pitch, _ in nt[track_index(s, name)]:
                by_bar.setdefault(bar_of(when), {}).setdefault(name, set()).add(pitch)
    for bar, layer in by_bar.items():
        root, _ = chord(meta['chords'][bar - 1])
        keys = layer.get('Keys', set())
        layer_rubs += rubs(layer.get('Pad', set()), keys | layer.get('Tex', set()), root)
        layer_rubs += rubs(layer.get('Tex', set()), keys, root)
    assert layer_rubs == 0, (s['sid'], layer_rubs)
    if 'Pad' in [t[0] for t in tracks(s)]:
        assert min(n[2] for n in nt[track_index(s, 'Pad')]) >= 36, (s['sid'], 'pad below C2')
    lead_all = [(b, e, p) for notes in meta['leads'].values() for b, e, p, _ in notes]
    bad, longn = clashes(meta['chords'], lead_all)
    assert bad <= max(2, longn // 10), (s['sid'], bad, longn)
    # Drums and layer velocity bands.
    di = track_index(s, 'Drums')
    drums = nt[di]
    sel = lambda pitches: [n for n in drums if n[2] in pitches]
    vel = lambda ns: span([n[3] for n in ns])
    kick = sel({KICK})
    if house:
        first = [n for n in kick if (n[0] + 60) % BAR < 120]
        others = [n for n in kick if n not in first]
        assert all(106 <= n[3] <= 112 for n in first) and all(100 <= n[3] <= 105 for n in others)
        assert all(88 <= n[3] <= 100 for n in sel({SNARE})) and all(80 <= n[3] <= 92 for n in sel({CLAP}))
        hats = sel({HAT})
        on = [n for n in hats if round(((n[0] % BAR)) / 120) % 4 == 0]
        off = [n for n in hats if round(((n[0] % BAR)) / 120) % 4 == 2]
        h16 = [n for n in hats if round(((n[0] % BAR)) / 120) % 2 == 1]
        assert len(on) + len(off) + len(h16) == len(hats)
        assert all(50 <= n[3] <= 62 for n in on) and all(74 <= n[3] <= 90 for n in off)
        assert all(45 <= n[3] <= 56 for n in h16) and bool(h16) == s['hat16']
        assert all(65 <= n[3] <= 80 for n in sel({OHAT})) and all(60 <= n[3] <= 75 for n in sel({RIDE}))
        assert all(80 <= n[3] <= 100 for n in sel({45, 43})) and {n[0] // BAR + 1 for n in sel({45, 43})} == {16, 48, 88}
        assert [n[0] // BAR + 1 for n in sel({CRASH})] == [57]
        assert all(28 <= n[2] <= 45 for n in nt[track_index(s, 'Bass')])
        bands = ((track_index(s, 'Keys'), 72, 92), (track_index(s, 'Pad'), 55, 72), (track_index(s, 'Tex'), 55, 70),
                 (track_index(s, 'ThemeA'), 70, 90), (track_index(s, 'ThemeB'), 70, 90), (track_index(s, 'Bass'), 74, 90))
        drum_txt = (f"kick1={vel(first)} kick={vel(others)} snare={vel(sel({SNARE}))} clap={vel(sel({CLAP}))} "
                    f"hat_on={vel(on)} hat_off={vel(off)} open={vel(sel({OHAT}))} ride={vel(sel({RIDE}))} "
                    f"tom={vel(sel({45, 43}))} crash={len(sel({CRASH}))}")
    else:
        # Lo-fi drums are classified by POSITION (16th cell after the +14 lazy offset), then held to the recipe bands.
        cell = lambda n: round(((n[0] % BAR) - 14) / 120)
        back = [n for n in sel({SNARE}) if cell(n) in (4, 12)]
        ghost = [n for n in sel({SNARE}) if cell(n) not in (4, 12)]
        assert all(86 <= n[3] <= 100 for n in back) and all(38 <= n[3] <= 52 for n in ghost)
        assert all(96 <= n[3] <= 110 for n in kick)
        hats = sel({HAT})
        on = [n for n in hats if cell(n) % 4 == 0]
        off = [n for n in hats if cell(n) % 4 == 2]
        assert len(on) + len(off) == len(hats)
        assert all(48 <= n[3] <= 60 for n in on) and all(68 <= n[3] <= 84 for n in off)
        assert all(68 <= n[3] <= 84 and cell(n) == 14 for n in sel({OHAT}))
        assert all(56 <= n[3] <= 90 for n in sel(set(TOMS)))
        crash = sel({CRASH})
        assert len(crash) == 1 and crash[0][0] // BAR + 1 == lofi_markers(n_bars)[3][0] and 55 <= crash[0][3] <= 70
        assert all(28 <= n[2] <= 48 for n in nt[track_index(s, 'Bass')])
        assert all(c <= 1 for c in Counter(n[0] // (4 * BAR) for n in sel({OHAT})).values())
        lead_counts = Counter()
        for k in ('ThemeA', 'ThemeB'):
            lead_counts.update(n[0] // BAR for n in nt[track_index(s, k)])
        assert max(lead_counts.values()) <= 6, (s['sid'], lead_counts.most_common(3))
        bands = ((track_index(s, 'Keys'), 72, 92), (track_index(s, 'Tex'), 55, 72), (track_index(s, 'Bass'), 60, 82),
                 (track_index(s, 'ThemeA'), 60, 82), (track_index(s, 'ThemeB'), 60, 82)) + \
            (((track_index(s, 'Pad'), 45, 60),) if s['pad'] else ())
        drum_txt = (f"kick={vel(kick)} snare={vel(back)} ghost={vel(ghost)} hat_on={vel(on)} hat_off={vel(off)} "
                    f"open={vel(sel({OHAT}))} toms={len(sel(set(TOMS)))} crash={len(sel({CRASH}))} swing={s['swing']}")
    for ti, lo, hi in bands:
        assert nt[ti] and all(lo <= n[3] <= hi for n in nt[ti]), (s['sid'], tracks(s)[ti][0], vel(nt[ti]))
    ki = track_index(s, 'Keys')
    assert any(c == 64 and v == 100 for _, c, v in cc[ki])
    k_lo, k_hi = (60, 84) if house else (48, 72)   # house v2: C4–C6; lo-fi: C3–C5
    assert all(k_lo <= n[2] <= k_hi for n in nt[ki]), (s['sid'], span([n[2] for n in nt[ki]]))
    # Hygiene: no same-pitch overlaps, no negative ticks, markers present, last note inside the last bar.
    overlaps = 0
    for events in nt.values():
        ends = {}
        for when, dur, pitch, _ in events:
            assert when >= 0 and dur > 0
            overlaps += int(when < ends.get(pitch, -1))
            ends[pitch] = when + dur
    assert overlaps == 0, (s['sid'], overlaps)
    for _, text in markers(s):
        assert bytes([0xff, 6, len(text)]) + text.encode() in smf
    assert ATTRIBUTION.encode() in smf
    last_end = max(n[0] + n[1] for notes in nt.values() for n in notes)
    assert bt(n_bars) < last_end <= bt(n_bars + 1)
    theme_pitch = [n[2] for k in ('ThemeA', 'ThemeB') for n in nt[track_index(s, k)]]
    print(f"check {s['sid']} PASS genre={s['genre']} bpm={bpm} bars={n_bars} key={s['out_key']} tr={s['tr']:+d} "
          f"window={s['theme_part']}:{s['theme_window'][0]}-{s['theme_window'][1]} map='{s['mp']['text']}' "
          f"eff_tempo={ratio_t:.2f}x ops={sorted(used)} op_bars={dict(sorted(op_bars(meta['effective']).items()))} "
          f"theme_swing_bars={meta['swing_bars'] if s['genre'] == 'lofi' else '-'} "
          f"orig_run_max={run} orig_bars={orig_bars} "
          f"theme={len(tb)}/{n_bars}={theme_pct:.0f}% clash={bad}/{longn} acc_chord_tones={acc} layer_rubs={layer_rubs} theme_range={span(theme_pitch)} "
          f"{drum_txt} "
          + ' '.join(f"{tracks(s)[ti][0]}={vel(nt[ti])}" for ti, _, _ in bands)
          + f" overlap={overlaps} last_end={last_end}/{n_bars * BAR}")
    return dict(theme_pct=round(theme_pct), orig_run=run, eff=round(ratio_t, 2), clash=f'{bad}/{longn}')


def progression_text(s, chords):
    """Compact bar-run text of the harmony, e.g. 'C#m9×2 Amaj9×2 …'."""
    runs = []
    for c in chords:
        if runs and runs[-1][0] == c:
            runs[-1][1] += 1
        else:
            runs.append([c, 1])
    return ' '.join(f'{c}×{k}' if k > 1 else c for c, k in runs)


def check_prompts():
    path = Path(__file__).resolve().parents[1] / 'suno' / 'vivaldi_opus.md'
    if not path.exists():
        print('prompt-length: suno/vivaldi_opus.md not written yet')
        return
    blocks = re.findall(r'^## (vs-[^\n]+)-v1\n\*\*Style\*\*\n`([^`]+)`\n\n\*\*Description\*\*\n```\n(.*?)\n```',
                        path.read_text(), re.M | re.S)
    assert [b[0] for b in blocks] == [s['sid'] for s in SKETCHES], [b[0] for b in blocks]
    for (sid, style, description), s in zip(blocks, SKETCHES):
        assert len(style) <= 300 and len(description) <= 1000, (sid, len(style), len(description))
        assert style.endswith('instrumental')
        assert not re.search(r'vivaldi|season|spring|summer|autumn|winter|four seasons', style, re.I), sid
        key_text = s['out_key'].replace('♯', '#').replace('♭', '-flat')
        assert key_text in style and key_text in description, (sid, key_text)
        season = s['key'][0].capitalize()
        assert 'variation on the theme of Vivaldi\'s Four Seasons, ' + season in description, sid
        assert f"{s['bpm']} BPM" in description, sid
        print(f'prompt-length {sid}-v1 Style={len(style)} Description={len(description)} PASS')


# ---------------------------------------------------------------- bounce (cross-session Logic lock inside produce)
RESTART_EVERY = 5


def recover_stray_bounce(sid, title, since, ver='v1', log=print):
    """produce() reports stage='file' when Logic's bounce dialog kept the folder another session bounced into last
    (2026-10-27: 11 AIFFs landed in band-fable/docs/music/sketches) — pipeline.BOUNCE_SEARCH only covers this
    worktree. Look for THIS song's AIFF in every sibling worktree's sketches folder, accept only files written since
    `since` (this attempt's start) and take the newest; then, holding the cross-session Logic lock, close the still-open
    project (it was saved before the bounce) and finish like pipeline.bounce_and_post(): move to bounces/, limiter,
    WAV, drop the AIFF, move only this song's '<title> <ver>.logicx' bundle to projects/.
    Returns the result dict, or None when no fresh AIFF exists."""
    import glob
    import shutil
    from pipeline import BOUNCE_DIR, PROJ_DIR, LogicLock, aiff_to_wav, close_all_projects, limit_aiff, wait_file_stable
    name = f'{sid}-{ver}.aif'
    worktree = Path(__file__).resolve().parents[3]
    found = glob.glob(str(worktree.parent / '*' / 'docs' / 'music' / 'sketches' / name))
    fresh = [p for p in found if os.path.getmtime(p) >= since]
    log(f'    {sid}: stray-bounce candidates {found or "none"}; fresh {fresh or "none"}')
    if not fresh:
        return None
    src = max(fresh, key=os.path.getmtime)
    if not wait_file_stable(src):
        return dict(ok=False, stage='recover', msg=f'not stable: {src}')
    with LogicLock(worktree.name):
        close_all_projects(save=False)
        aif = os.path.join(BOUNCE_DIR, name)
        shutil.move(src, aif)
        knee = limit_aiff(aif)
        wav = os.path.join(BOUNCE_DIR, f'{sid}-{ver}.wav')
        ok, err = aiff_to_wav(aif, wav)
        if not ok:
            return dict(ok=False, stage='wav', msg=err, aif=aif, recovered_from=src)
        os.remove(aif)
        bundle = os.path.join(SK_DIR, f'{title} {ver}.logicx')
        if os.path.isdir(bundle):
            dst = os.path.join(PROJ_DIR, os.path.basename(bundle))
            if os.path.exists(dst):
                shutil.rmtree(dst)
            shutil.move(bundle, dst)
    log(f'    {sid}: recovered stray bounce from {src}')
    return dict(ok=True, wav=wav, mb=os.path.getsize(wav) // 1024 // 1024, knee=knee, recovered_from=src)


def bounce(sids, log=print):
    from pipeline import produce, restart_logic
    from bounce_dh import NoScreensaver, screen_locked
    results = {}
    with NoScreensaver():
        for n, s in enumerate(sk for sk in SKETCHES if sk['sid'] in sids):
            if n and n % RESTART_EVERY == 0:
                try:
                    restart_logic(log)   # takes the same cross-session lock as produce()
                except TimeoutError as exc:
                    log(f'    logic restart skipped: {exc}')
            mid = os.path.join(SK_DIR, f"{s['sid']}-v1.mid")
            if screen_locked():
                log(f"=== {s['sid']} ABORT screen locked")
                results[s['sid']] = {'ok': False, 'stage': 'locked'}
                break
            t0 = time.time()
            log(f"=== {s['sid']} start {time.strftime('%T')}")
            try:
                r = produce(s['sid'], s['title'], 'v1', mid, log=lambda m: log('    ' + m))
            except TimeoutError as exc:
                r = {'ok': False, 'stage': 'lock-timeout', 'msg': str(exc)}
            if not r.get('ok') and r.get('stage') == 'file':
                try:
                    recovered = recover_stray_bounce(s['sid'], s['title'], t0, log=log)
                except (OSError, TimeoutError) as exc:
                    recovered = {'ok': False, 'stage': 'recover', 'msg': str(exc)}
                if recovered:
                    r = dict(recovered, strips=r.get('strips'), elapsed=r.get('elapsed'))
            results[s['sid']] = r
            log(f"=== {s['sid']} {'OK' if r.get('ok') else 'FAIL'} {round(time.time() - t0)}s "
                f"{json.dumps(r, ensure_ascii=False)}")
    return results


def main(argv):
    for s in SKETCHES:
        result, meta = compose(s['sid'])
        nt, cc, pcs, n_bars, bpm, title, sf, minor = result
        smf = with_attribution(build_smf(title, bpm, sf, minor, n_bars, tracks(s), pcs, nt, cc, markers(s)))
        check(s, result, meta, smf)
        print(f"  harmony {s['sid']}: {progression_text(s, meta['chords'])}")
        print('  ' + write_smf(os.path.join(SK_DIR, s['sid'] + '-v1.mid'), smf))
    check_prompts()
    if '--bounce' in argv:
        known = [s['sid'] for s in SKETCHES]
        wanted = [a for a in argv[1:] if a != '--bounce'] or known
        unknown = sorted(set(wanted) - set(known))
        if unknown:
            print(f'unknown sid: {unknown}; known: {known}', file=sys.stderr)
            return 2
        results = bounce(wanted, log=lambda m: print(m, flush=True))
        print(json.dumps({k: v.get('ok') for k, v in results.items()}))
        return 0 if results and all(v.get('ok') for v in results.values()) else 1
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
