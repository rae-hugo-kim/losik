"""Ten third-pass lo-fi hip hop compositions (model opus); Python 3.9 stdlib.

Beat offsets are zero-based; MIDI programs are zero-based. check_set() reads
lh_astra.SKETCHES and lh_fable.SKETCHES so chord loops (rotation-insensitive),
kick cells, comping, texture beats, lead motifs and break types never repeat the
first two passes. Slot 30 is the set closer: its outro sheds drums, then bass,
leaving keys alone and one held chord in the final bar.
"""
import os
import re
from collections import Counter
from pathlib import Path

from pipeline import BAR, PPQ, SK_DIR, bt, hum_t, hum_v, seed, build_smf, write_smf
from sketches import PC, mk_chord2
import lh_astra
import lh_fable

TRACKS = [('Drums', 9), ('Bass', 0), ('Keys', 1), ('Tex', 2), ('Lead', 3)]
PAD_TRACK = ('Pad', 4)
DRUM_LAYERS = ('Kick', 'Snare', 'Hats')

# Chord tuples: name, root (sketches.PC key), bass quality for mk_chord2, four-voice jazz voicing (C3..C5).
# bass_moves: second bass note per loop bar when the kick cell has three hits:
#   '5' fifth above, '-4' fifth below, 'app' chromatic approach from below into the next bar's root.
# break_plan: ((bars, layers), ...) covering the eight break bars.
SKETCHES = [
    dict(slot=3, sid='lh03-chalk-awning', title='Chalk Awning', bpm=78, bars=56,
         key='F major', energy=2, energy_label='1–2', sf=-1, minor=False, tonic='F', swing=27,
         keys_pc=4, tex_pc=24, lead_pc=0, opener='tex', rim=False, pad=False, hat16=False,
         chords=[('Fmaj9', 'F', 'M7', (57, 60, 64, 67)),
                 ('Am7', 'A', 'm7', (55, 60, 64, 69)),
                 ('Bbmaj9', 'Bb', 'M7', (57, 60, 62, 65)),
                 ('C13sus', 'C', '7', (58, 62, 65, 69))], order=(0, 1, 2, 3),
         kicks=((0, 2.5), (0, 1.75), (0, 2.75), (0, 1.5, 2.5)),
         ghosts=((3.75,), (0.75, 3.75), (2.25,), (0.75, 3.25)),
         bass_moves=('5', '5', '5', 'app'),
         comp=((0,), (1.5, 3), (0, 2.25), (0.5,)),
         melody=((67, 69, 72), (76, 72), (74, 72, 69, 65), (67, 65)),
         lead_beats=((1, 1.5, 2.5), (0.5, 2), (0, 1, 1.5, 2.5), (0.5, 2.5)),
         tex_beats=((0.5, 1.5, 3), (2, 3.5), (0.5, 1.5, 3), (1, 2.5)), tex_order=(0, 2, 3, 1),
         break_id='drumless-trio', break_plan=((8, ('Bass', 'Keys', 'Tex')),),
         loop_text='Fmaj9–Am7–B♭maj9–C13sus, I–iii–IV–V13sus',
         motif_text='그랜드 `G4-A4-C5 / E5-C5 / D5-C5-A4-F4 / G4-F4`, 세 음으로 올라 E 에 닿은 뒤 네 음 계단으로 내려와 G–F 에서 쉽니다.',
         break_text='드럼 전부를 빼고 베이스+EP+나일론 트리오 8마디입니다.',
         notes='Nylon opens alone; EP holds bar one and answers late; grand lead climbs to E and walks down.'),
    dict(slot=6, sid='lh06-iron-teacup', title='Iron Teacup', bpm=80, bars=64,
         key='A minor', energy=2, energy_label='2', sf=0, minor=True, tonic='A', swing=29,
         keys_pc=0, tex_pc=27, lead_pc=4, opener='keys', rim=False, pad=False, hat16=False,
         chords=[('Am9', 'A', 'm7', (60, 64, 67, 71)),
                 ('G13', 'G', '7', (53, 59, 64, 69)),
                 ('Fmaj9', 'F', 'M7', (57, 60, 64, 67)),
                 ('Em7', 'E', 'm7', (55, 59, 62, 64))], order=(0, 1, 2, 3),
         kicks=((0, 1.75, 2.5), (0, 2.75), (0, 1.5, 2.75), (0, 2.5)),
         ghosts=((0.75,), (2.25, 3.75), (0.75,), (2.25, 3.25)),
         bass_moves=('-4', '5', '5', 'app'),
         comp=((0, 3.5), (0.5, 2), (0, 3.5), (1, 2.5)),
         melody=((76, 74, 71), (74, 71, 69), (72, 69, 67), (67, 71)),
         lead_beats=((0.5, 1, 2), (0.5, 1, 2), (0.5, 1, 2), (1, 2.5)),
         tex_beats=((1, 2.5), (0, 1.5, 3), (1, 2.5), (0.5, 3.5)), tex_order=(3, 1, 0, 2),
         break_id='bass-solo-buildback',
         break_plan=((2, ('Bass',)), (2, ('Bass', 'Tex')), (4, ('Bass', 'Tex', 'Snare', 'Hats'))),
         loop_text='Am9–G13–Fmaj9–Em7, 에올리안 하행 i–VII–VI–v',
         motif_text='EP `E5-D5-B4 / D5-B4-A4 / C5-A4-G4 / G4-B4`, 세 음 하강 셀을 화음 따라 한 칸씩 내린 뒤 G–B 로 되올립니다.',
         break_text='베이스 혼자 2마디 → +나일론 2마디 → +스네어·햇 4마디, 킥·그랜드는 쉽니다.',
         notes='Descending aeolian loop; three-note falling cell sequenced down, answered upward.'),
    dict(slot=9, sid='lh09-signal-orchard', title='Signal Orchard', bpm=84, bars=64,
         key='D major', energy=2, energy_label='2–3', sf=2, minor=False, tonic='D', swing=31,
         keys_pc=4, tex_pc=16, lead_pc=24, opener='keys', rim=False, pad=False, hat16=True,
         chords=[('Dmaj9', 'D', 'M7', (54, 57, 61, 64)),
                 ('A13sus', 'A', '7', (55, 59, 62, 66)),
                 ('Bm9', 'B', 'm7', (50, 54, 57, 61)),
                 ('Gmaj9', 'G', 'M7', (54, 57, 59, 62))], order=(0, 1, 2, 3),
         kicks=((0, 1.5, 2.5), (0, 2.75), (0, 1.75, 2.5), (0, 1.5)),
         ghosts=((0.75, 3.75), (2.25,), (0.75, 3.75), (2.25,)),
         bass_moves=('5', '5', '-4', '5'),
         comp=((0, 1.5, 2.5), (0.5,), (0, 1.5, 2.5), (0, 3)),
         melody=((66, 69, 71, 69), (66, 64), (71, 74, 73), (69, 66)),
         lead_beats=((0, 0.5, 1.5, 2.5), (0.5, 2), (0, 1, 2.5), (0.5, 2)),
         tex_beats=((0,), (2,), (0,), (1.5,)), tex_order=(1, 3, 2, 0),
         break_id='snare-hats-organ', break_plan=((8, ('Snare', 'Hats', 'Tex')),),
         loop_text='Dmaj9–A13sus–Bm9–Gmaj9, I–V13sus–vi–IV',
         motif_text='나일론 `F#4-A4-B4-A4 / F#4-E4 / B4-D5-C#5 / A4-F#4`, 펜타토닉 턴과 한숨 뒤 같은 턴을 B 위로 올려 F# 로 내려앉습니다.',
         break_text='킥·베이스·EP 를 빼고 스네어(고스트)+햇+오르간 홀드 8마디입니다.',
         notes='Rising into the peak: EP triple comps, organ holds, one quiet sixteenth hat per bar.'),
    dict(slot=12, sid='lh12-ember-switchyard', title='Ember Switchyard', bpm=86, bars=64,
         key='F# minor', energy=3, energy_label='3', sf=3, minor=True, tonic='F#', swing=30,
         keys_pc=0, tex_pc=4, lead_pc=24, opener='keys', rim=False, pad=False, hat16=True,
         chords=[('F#m9', 'F#', 'm7', (57, 61, 64, 68)),
                 ('Amaj9', 'A', 'M7', (56, 59, 61, 64)),
                 ('E6/9', 'E', 'M', (56, 61, 66, 71)),
                 ('B9', 'B', '7', (57, 61, 63, 66))], order=(0, 1, 2, 3),
         kicks=((0, 1.75, 2.75), (0, 1.5, 2.5), (0, 2.5, 2.75), (0, 1.75, 2.5)),
         ghosts=((0.75, 2.25), (0.75, 3.75), (2.25, 3.75), (0.75, 3.75)),
         bass_moves=('5', '-4', '5', 'app'),
         comp=((0, 0.75, 2.5), (1.5, 3), (0, 0.75, 2.5), (0.5, 2, 3.5)),
         melody=((69, 73, 76), (76, 73, 71), (68, 71, 73), (73, 69, 66)),
         lead_beats=((0.5, 1, 2.5), (0.5, 1.5, 3), (0.5, 1, 2.5), (0.5, 1.5, 2.5)),
         tex_beats=((0.5, 2, 3), (1, 2.5), (0.5, 2, 3), (1.5, 3.5)), tex_order=(2, 0, 3, 1),
         break_id='snareless-buildback',
         break_plan=((2, ('Keys', 'Bass')), (2, ('Keys', 'Bass', 'Hats')), (4, ('Keys', 'Bass', 'Hats', 'Kick'))),
         loop_text='F#m9–Amaj9–E6/9–B9, 도리안 i–III–VII–IV9',
         motif_text='나일론 `A4-C#5-E5 / E5-C#5-B4 / G#4-B4-C#5 / C#5-A4-F#4`, 1박 뒷박에서 분산화음으로 올랐다가 접어 내려옵니다.',
         break_text='그랜드+베이스 2마디 → +햇 2마디 → +킥 4마디로 되쌓고 스네어·Tex 는 37마디까지 쉽니다.',
         notes='Dorian peak with PC38 bass; and-of-one triad climbs folded back down.'),
    dict(slot=15, sid='lh15-quartz-overpass', title='Quartz Overpass', bpm=88, bars=64,
         key='C# minor', energy=3, energy_label='3', sf=4, minor=True, tonic='C#', swing=32,
         keys_pc=4, tex_pc=27, lead_pc=0, opener='tex', rim=False, pad=False, hat16=True,
         chords=[('C#m9', 'C#', 'm7', (52, 56, 59, 63)),
                 ('F#9', 'F#', '7', (52, 56, 58, 61)),
                 ('Amaj9', 'A', 'M7', (56, 59, 61, 64)),
                 ('G#7b13', 'G#', '7', (54, 60, 64, 70))], order=(0, 1, 2, 3),
         kicks=((0, 1.5, 2.75), (0, 2.5, 2.75), (0, 1.75, 2.75), (0, 1.5, 2.5)),
         ghosts=((2.25, 3.75), (0.75, 2.25), (0.75, 3.75), (2.25, 3.75)),
         bass_moves=('-4', '5', '5', 'app'),
         comp=((0, 2, 3.5), (0.75, 2.5), (0, 2, 3.5), (1.5, 2.25)),
         melody=((68, 71, 68, 64), (70, 68), (71, 73, 71, 68), (72, 68)),
         lead_beats=((0, 0.5, 1.5, 2.5), (0.5, 2), (0, 0.5, 1.5, 2.5), (0.5, 2)),
         tex_beats=((0, 1, 2.5, 3.5), (0.5, 2), (0, 1, 2.5, 3.5), (1.5, 3)), tex_order=(0, 3, 1, 2),
         break_id='drums-bass-nylon', break_plan=((8, ('Kick', 'Snare', 'Hats', 'Bass', 'Tex')),),
         loop_text='C#m9–F#9–Amaj9–G#7♭13, i–IV9(도리안)–VI–V',
         motif_text='그랜드 `G#4-B4-G#4-E4 / A#4-G#4 / B4-C#5-B4-G#4 / B#4-G#4`, 이웃음 턴을 한 칸 올려 되풀이하고 이끔음 B# 로 닫습니다.',
         break_text='키만 빼고 드럼+베이스+나일론 8마디입니다.',
         notes='Peak; nylon opens, EP enters at five; neighbour-tone turn repeated a step higher.'),
    dict(slot=18, sid='lh18-lantern-deck', title='Lantern Deck', bpm=84, bars=64,
         key='B major', energy=2, energy_label='2', sf=5, minor=False, tonic='B', swing=28,
         keys_pc=0, tex_pc=16, lead_pc=4, opener='keys', rim=False, pad=False, hat16=False,
         chords=[('Bmaj9', 'B', 'M7', (58, 61, 63, 66)),
                 ('G#m9', 'G#', 'm7', (59, 63, 66, 70)),
                 ('Emaj9', 'E', 'M7', (56, 59, 63, 66)),
                 ('Em9', 'E', 'm7', (55, 59, 62, 66))], order=(0, 1, 2, 3),
         kicks=((0, 2.75), (0, 1.5, 2.5), (0, 2.5), (0, 1.75, 2.75)),
         ghosts=((0.75, 3.75), (3.25,), (0.75, 2.25), (3.75,)),
         bass_moves=('5', '5', '5', 'app'),
         comp=((0, 2.5), (1,), (0, 2.5), (0, 1.25)),
         melody=((73, 70, 66), (68, 70, 71), (75, 71), (74, 71, 67)),
         lead_beats=((0.5, 1, 2.5), (0.5, 1.5, 3), (0, 2), (0.5, 1.5, 3)),
         tex_beats=((0.5,), (0,), (1,), (0,)), tex_order=(2, 1, 3, 0),
         break_id='keys-hats-then-kick', break_plan=((4, ('Keys', 'Hats')), (4, ('Keys', 'Hats', 'Kick'))),
         loop_text='Bmaj9–G#m9–Emaj9–Em9, I–vi–IV–iv(차용)',
         motif_text='EP `C#5-A#4-F#4 / G#4-A#4-B4 / D#5-B4 / D5-B4-G4`, 내려왔다 되오른 뒤 D#–B 모양을 단조 iv 위에서 D–B–G 로 바꿉니다.',
         break_text='그랜드+햇 4마디 → +킥 4마디, 스네어·베이스·오르간은 쉽니다.',
         notes='Drift begins: borrowed minor iv darkens the loop; organ swells under the grand.'),
    dict(slot=21, sid='lh21-ink-carousel', title='Ink Carousel', bpm=82, bars=64,
         key='Eb minor', energy=2, energy_label='2', sf=-6, minor=True, tonic='Eb', swing=27,
         keys_pc=0, tex_pc=4, lead_pc=24, opener='tex', rim=False, pad=False, hat16=False,
         chords=[('Ebm9', 'Eb', 'm7', (54, 58, 61, 65)),
                 ('Db6/9', 'Db', 'M', (53, 58, 63, 68)),
                 ('Gbmaj9', 'F#', 'M7', (58, 61, 65, 68)),
                 ('Cbmaj9', 'B', 'M7', (58, 61, 63, 66))], order=(0, 1, 2, 3),
         kicks=((0, 1.5, 2.5), (0, 1.75), (0, 2.75), (0, 1.5, 2.75)),
         ghosts=((3.25,), (0.75, 2.25), (3.75,), (0.75, 3.25)),
         bass_moves=('5', '5', '5', '-4'),
         comp=((0,), (0.5, 3), (0,), (0.5, 2)),
         melody=((70, 70, 73), (70, 68, 65), (65, 65, 68), (70, 66)),
         lead_beats=((0, 0.5, 2), (0.5, 1.5, 2.5), (0, 0.5, 2), (0.5, 2)),
         tex_beats=((1.5, 3), (0.5,), (1.5, 3), (0.5, 2.5)), tex_order=(1, 0, 2, 3),
         break_id='tex-then-tex-bass', break_plan=((4, ('Tex',)), (4, ('Tex', 'Bass'))),
         loop_text='E♭m9–D♭6/9–G♭maj9–C♭maj9, i–VII–III–VI 4도 하행',
         motif_text='나일론 `Bb4-Bb4-Db5 / Bb4-Ab4-F4 / F4-F4-Ab4 / Bb4-Gb4`, 같은 음 두 번 뒤 3도 위로 튀는 픽업을 4도 아래에서 되풀이합니다.',
         break_text='상성부 EP 만 4마디 → EP+베이스 4마디, 드럼·그랜드는 쉽니다.',
         notes='Same key as slot 20 but a falling-fourths loop, held comping and a repeated-note pickup.'),
    dict(slot=24, sid='lh24-felt-almanac', title='Felt Almanac', bpm=78, bars=56,
         key='Ab major', energy=1, energy_label='1–2', sf=-4, minor=False, tonic='Ab', swing=25,
         keys_pc=4, tex_pc=27, lead_pc=0, opener='keys', rim=False, pad=False, hat16=False,
         chords=[('Abmaj9', 'Ab', 'M7', (60, 63, 67, 70)),
                 ('Fm9', 'F', 'm7', (56, 60, 63, 67)),
                 ('Cm7', 'C', 'm7', (55, 58, 60, 63)),
                 ('Dbmaj9', 'Db', 'M7', (53, 56, 60, 63))], order=(0, 1, 2, 3),
         kicks=((0, 1.75), (0, 2.5), (0, 1.5, 2.75), (0, 2.75)),
         ghosts=((3.75,), (2.25,), (3.75,), (0.75,)),
         bass_moves=('5', '5', '5', '5'),
         comp=((0, 1.5), (0,), (2.5,), (0, 2)),
         melody=((72, 70), (68,), (67, 70), (72, 68)),
         lead_beats=((0, 2), (1,), (0.5, 2), (1, 2.5)),
         tex_beats=((1, 3), (2,), (1, 3), (0.5, 2)), tex_order=(3, 2, 0, 1),
         break_id='hats-only-band', break_plan=((8, ('Keys', 'Tex', 'Bass', 'Hats')),),
         loop_text='A♭maj9–Fm9–Cm7–D♭maj9, I–vi–iii–IV',
         motif_text='그랜드 `C5-Bb4 / Ab4 / G4-Bb4 / C5-Ab4`, 한숨 한 번과 긴 A♭ 뒤 G–B♭ 로 들어 C–A♭ 로 놓습니다.',
         break_text='킥·스네어만 빼고 햇+베이스+EP+나일론 8마디입니다.',
         notes='Cool-down begins: sparse two-note lead, EP comping thins to one hit in bar three.'),
    dict(slot=27, sid='lh27-moth-library', title='Moth Library', bpm=76, bars=56,
         key='C minor', energy=1, energy_label='1', sf=-3, minor=True, tonic='C', swing=26,
         keys_pc=0, tex_pc=24, lead_pc=4, opener='tex', rim=True, pad=True, hat16=False,
         chords=[('Cm9', 'C', 'm7', (51, 55, 58, 62)),
                 ('Ebmaj9', 'Eb', 'M7', (55, 58, 62, 65)),
                 ('Abmaj9', 'Ab', 'M7', (55, 58, 60, 63)),
                 ('Fm9', 'F', 'm7', (56, 60, 63, 67))], order=(0, 1, 2, 3),
         kicks=((0, 2.5), (0, 2.5), (0, 1.75), (0, 2.75)),
         ghosts=((2.25,), (3.75,), (2.25,), (3.75,)),
         bass_moves=('5', '5', '5', '5'),
         comp=((0,), (0, 2.5), (0,), (1,)),
         melody=((74, 70), (67,), (72, 75), (72, 68)),
         lead_beats=((1, 2.5), (0.5,), (0.5, 2), (0.5, 2)),
         tex_beats=((2.5,), (1,), (2.5,), (0.5, 2)), tex_order=(2, 3, 1, 0),
         break_id='pad-bass-then-nylon', break_plan=((4, ('Pad', 'Bass')), (4, ('Pad', 'Bass', 'Tex'))),
         loop_text='Cm9–E♭maj9–A♭maj9–Fm9, i–III–VI–iv',
         motif_text='EP `D5-Bb4 / G4 / C5-Eb5 / C5-Ab4`, 9도에서 내려와 G 하나를 두고 C–E♭ 로 들었다가 C–A♭ 로 내려놓습니다.',
         break_text='드럼·그랜드 없이 패드+베이스 4마디 → +나일론 4마디입니다.',
         notes='Energy 1 with even-bar rim and a low 1+5 pad; long-tone EP lead.'),
    dict(slot=30, sid='lh30-last-streetlamp', title='Last Streetlamp', bpm=72, bars=56,
         key='G minor', energy=1, energy_label='1', sf=-2, minor=True, tonic='G', swing=24,
         keys_pc=4, tex_pc=24, lead_pc=0, opener='keys', rim=False, pad=True, hat16=False,
         chords=[('Gm9', 'G', 'm7', (58, 62, 65, 69)),
                 ('Ebmaj9', 'Eb', 'M7', (55, 58, 62, 65)),
                 ('Am7b5', 'A', 'm7', (57, 60, 63, 67)),
                 ('D7b9', 'D', '7', (54, 60, 63, 69))], order=(0, 1, 2, 3),
         kicks=((0, 2.75), (0, 1.5), (0, 2.75), (0, 2.5)),
         ghosts=((3.75,), (0.75,), (3.75,), (2.25,)),
         bass_moves=('5', '5', '5', '5'),
         comp=((0,), (0.5,), (0, 3), (0,)),
         melody=((69, 70, 74), (67, 70), (72, 69), (66, 69)),
         lead_beats=((0.5, 1, 2.5), (0.5, 2), (0.5, 2), (1, 2.5)),
         tex_beats=((1.5,), (2.5,), (1, 3), (2,)), tex_order=(0, 1, 3, 2),
         break_id='keys-bass-pad', break_plan=((8, ('Keys', 'Bass', 'Pad')),),
         loop_text='Gm9–E♭maj9–Am7♭5–D7♭9, i–VI–iiø–V7♭9',
         motif_text='그랜드 `A4-Bb4-D5 / G4-Bb4 / C5-A4 / F#4-A4`, 9도에서 올라 D 에 닿고 메아리 뒤 이끔음 F#–A 로 집에 돌아섭니다.',
         break_text='드럼·나일론 없이 EP+베이스+저역 패드 8마디입니다.',
         notes='Closer: outro drops drums at 51, bass at 53, keys alone, final bar one held Gm9.'),
]

CLOSER_SLOT = 30


def markers(n_bars):
    return [(1, 'intro'), (9, 'A'), (25 if n_bars == 56 else 29, 'break'),
            (33 if n_bars == 56 else 37, 'A2'), (n_bars - 7, 'outro')]


def tracks_for(s):
    return TRACKS + ([PAD_TRACK] if s['pad'] else [])


def break_layers(s, offset):
    for length, layers in s['break_plan']:
        if offset < length:
            return set(layers)
        offset -= length
    raise AssertionError('break plan shorter than eight bars')


def closer_outro(s, bar):
    """Slot 30: drums+bass+keys 2 bars -> bass+keys 2 bars -> keys alone; final bar one chord."""
    outro = markers(s['bars'])[4][0]
    offset = bar - outro
    if offset < 2:
        return {'Kick', 'Snare', 'Hats', 'Bass', 'Keys'}
    if offset < 4:
        return {'Bass', 'Keys'}
    return {'Keys', 'Final'} if bar == s['bars'] else {'Keys'}


def layers_at(s, bar):
    _, _, (brk, _), (a2, _), (outro, _) = markers(s['bars'])
    if brk <= bar < a2:
        return break_layers(s, bar - brk)
    if s['slot'] == CLOSER_SLOT and bar >= outro:
        return closer_outro(s, bar)
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
    if 9 <= bar <= s['bars'] - 4:
        layers.add('Bass')
    if brk - 8 <= bar < brk or a2 <= bar < outro:
        layers.add('Lead')
    if s['pad'] and 9 <= bar < outro:
        layers.add('Pad')
    if s['energy'] == 1 and bar > s['bars'] - 4:
        layers.difference_update(DRUM_LAYERS)
    return layers


def lead_phrase(s, phase, variant):
    """A2 variant phrase: bar one breathes (drops its first note), bar three is anticipated by an eighth."""
    pitches, beats = s['melody'][phase], s['lead_beats'][phase]
    if variant and phase == 0 and len(pitches) > 1:
        pitches, beats = pitches[1:], beats[1:]
    if variant and phase == 2 and min(beats) >= 0.5:
        beats = tuple(b - 0.5 for b in beats)
    return pitches, beats


def bass_second(s, phase, root):
    move = s['bass_moves'][phase]
    if move == 'app':
        nxt = s['chords'][s['order'][(phase + 1) % 4]]
        pitch = mk_chord2(PC[nxt[1]], nxt[2])['bass'] - 1
    elif move == '-4':
        pitch = root - 5
    else:
        pitch = root + 7
    while pitch > 48:
        pitch -= 12
    while pitch < 28:
        pitch += 12
    return pitch


def compose(sid):
    s = next(s for s in SKETCHES if s['sid'] == sid)
    seed(261021 + s['slot'] * 131)
    n_tracks = len(tracks_for(s))
    nt, cc = {i: [] for i in range(n_tracks)}, {i: [] for i in range(n_tracks)}
    pcs = {0: 0, 1: 38 if s['energy'] == 3 else 33, 2: s['keys_pc'], 3: s['tex_pc'], 4: s['lead_pc']}
    if s['pad']:
        pcs[5] = 89
    a2 = markers(s['bars'])[3][0]
    swing = s['swing']

    def tick(bar, beat, swung=False):
        delay = swing if swung and beat % 1 == 0.5 else 0
        return hum_t(bt(bar, beat) + 14 + delay, 12)

    def velocity(base, low, high):
        return max(low, min(high, hum_v(base, 10)))

    def add(track, bar, when, end, pitch, vel):
        end = min(end, bt(bar + 1) - 24)
        assert when >= bt(bar) and end > when
        nt[track].append((when, end - when, pitch, vel))

    def line(track, bar, onsets, pitches, vel_fn, cap, gap=40):
        """Monophonic/chordal line: each note ends `gap` ticks before the next onset (or bar end), capped."""
        for index, when in enumerate(onsets):
            nxt = onsets[index + 1] if index + 1 < len(onsets) else bt(bar + 1)
            end = min(nxt - gap, when + cap)
            for pitch in pitches[index]:
                add(track, bar, when, end, pitch, vel_fn(index))

    for bar in range(1, s['bars'] + 1):
        phase = (bar - 1) % 4
        _, root_name, quality, chord = s['chords'][s['order'][phase]]
        layers = layers_at(s, bar)
        occupied = set()
        cell = s['kicks'][phase]
        kick_times = [tick(bar, beat) for beat in cell]

        def drum(beat, pitch, base, low, high, swung=False, dur=70):
            slot_cell = round(beat * 4)
            assert slot_cell not in occupied
            occupied.add(slot_cell)
            when = tick(bar, beat, swung)
            add(0, bar, when, when + dur, pitch, velocity(base, low, high))

        if 'Kick' in layers:
            kick_base = velocity(98 + s['energy'], 96, 104)
            for beat, when in zip(cell, kick_times):
                occupied.add(round(beat * 4))
                add(0, bar, when, when + 80, 36, kick_base + (6 if beat == 0 else 0))
        if 'Snare' in layers:
            for beat in (1, 3):
                pitch = 37 if s['rim'] and bar % 2 == 0 else 38
                drum(beat, pitch, 88 + 2 * s['energy'], 86, 100)
            for beat in s['ghosts'][phase]:
                drum(beat, 38, 45, 38, 52)
        if bar == a2:
            drum(0.5, 49, 62, 55, 70, dur=400)
        if 'Hats' in layers:
            for eighth in range(8):
                beat = eighth / 2
                if round(beat * 4) in occupied:
                    continue
                offbeat = eighth % 2 == 1
                open_hat = phase == 3 and eighth == 7
                drum(beat, 46 if open_hat else 42, 76 if offbeat else 54,
                     68 if offbeat else 48, 84 if offbeat else 60, swung=offbeat, dur=145 if open_hat else 70)
            if s['hat16']:
                drum(1.25 if phase == 3 else 3.25, 42, 45, 40, 50)
        if 'Bass' in layers:
            root = mk_chord2(PC[root_name], quality)['bass']
            pitches = [root] + [bass_second(s, phase, root)] * (len(cell) - 2)
            # Bass follows the kick but skips its last hit; each note breathes out before the next kick.
            for index, pitch in enumerate(pitches):
                end = kick_times[index + 1] - 40
                add(1, bar, kick_times[index], end, pitch, velocity(70 + s['energy'], 60, 82))
        if 'Keys' in layers:
            beats = (0,) if 'Final' in layers else s['comp'][phase]
            # The closer's last bar resolves the loop's V7b9 to one held tonic chord.
            voicing = s['chords'][0][3] if 'Final' in layers else chord
            onsets = [tick(bar, beat) for beat in beats]
            line(2, bar, onsets, [voicing] * len(onsets),
                 lambda i: velocity(82 if i == 0 else 78, 72, 92), cap=4 * PPQ, gap=50)
            cc[2].append((bt(bar), 64, 0))
            for when in onsets:
                cc[2].extend(((when - 1, 64, 0), (when + 1, 64, 100)))
            cc[2].append((bt(bar + 1) - 2, 64, 0))
        if 'Tex' in layers:
            beats = s['tex_beats'][phase]
            onsets = [tick(bar, beat, swung=True) for beat in beats]
            if s['tex_pc'] == 16:
                for when, beat in zip(onsets, beats):
                    for pitch in (chord[0], chord[2]):
                        add(3, bar, when, bt(bar, 3.8), pitch, velocity(61, 55, 72))
            else:
                # Second EP plays an octave above the keys but never above E5 (no bright top end).
                lift = 12 if s['tex_pc'] == 4 else 0
                picks = [(p + lift if p + lift <= 76 else p,)
                         for p in (chord[s['tex_order'][(i + phase) % 4]] for i in range(len(beats)))]
                line(3, bar, onsets, picks, lambda i: velocity(63, 55, 72), cap=300)
        if 'Lead' in layers:
            variant = bar >= a2 and ((bar - a2) // 4) % 2 == 1
            pitches, beats = lead_phrase(s, phase, variant)
            onsets = [tick(bar, beat, swung=True) for beat in beats]
            line(4, bar, onsets, [(p,) for p in pitches], lambda i: velocity(70 + s['energy'], 60, 82), cap=440, gap=48)
        if 'Pad' in layers:
            # Root + the chord's own fifth: the half-diminished bar takes the flat five.
            fifth = 6 if 'b5' in s['chords'][s['order'][phase]][0] else 7
            low = 48 + PC[root_name]
            if low + fifth > 60:
                low -= 12
            when = tick(bar, 0)
            for pitch in (low, low + fifth):
                add(5, bar, when, bt(bar + 1), pitch, velocity(52, 45, 60))
    for events in nt.values():
        events.sort()
    for events in cc.values():
        events.sort()
    return nt, cc, pcs, s['bars'], s['bpm'], s['title'], s['sf'], s['minor']


def event_cell(note):
    return round(((note[0] % BAR) - 14) / (PPQ / 4))


def span(values):
    return f'{min(values)}..{max(values)}' if values else '-'


def check(s, result, smf):
    nt, cc, pcs, n_bars, bpm, title, sf, minor = result
    assert (n_bars, bpm, title, sf, minor) == (s['bars'], s['bpm'], s['title'], s['sf'], s['minor'])
    assert n_bars == (56 if bpm <= 78 else 64)
    expect = {0: 0, 1: 38 if s['energy'] == 3 else 33, 2: s['keys_pc'], 3: s['tex_pc'], 4: s['lead_pc']}
    if s['pad']:
        expect[5] = 89
    assert pcs == expect
    drums = nt[0]
    kick = [n for n in drums if n[2] == 36]
    back = [n for n in drums if n[2] in (37, 38) and n[3] >= 86]
    ghost = [n for n in drums if n[2] == 38 and n[3] <= 52]
    hats_on = [n for n in drums if n[2] == 42 and event_cell(n) % 4 == 0]
    hats_off = [n for n in drums if n[2] == 42 and event_cell(n) % 4 == 2]
    hats_extra = [n for n in drums if n[2] == 42 and event_cell(n) % 2 == 1]
    opened = [n for n in drums if n[2] == 46]
    pad = nt.get(5, [])
    assert len(kick) + len(back) + len(ghost) + len(hats_on) + len(hats_off) + len(hats_extra) + \
        len(opened) + 1 == len(drums)
    for notes, lo, hi in ((kick, 96, 110), (back, 86, 100), (ghost, 38, 52),
                          (hats_on, 48, 60), (hats_off, 68, 84), (opened, 68, 84),
                          (hats_extra, 40, 50), (nt[1], 60, 82), (nt[2], 72, 92),
                          (nt[3], 55, 72), (nt[4], 60, 82), (pad, 45, 60)):
        assert all(lo <= n[3] <= hi for n in notes)
    assert hats_on and hats_off and all(event_cell(n) in (5, 13) for n in hats_extra)
    assert bool(hats_extra) == s['hat16']
    assert all(28 <= n[2] <= 48 for n in nt[1])
    assert all(48 <= n[2] <= 72 for n in nt[2])
    assert all(n[2] <= 76 for n in nt[3])
    assert all(n[2] <= 60 for n in pad)
    assert all(c <= 1 for c in Counter(n[0] // (4 * BAR) for n in opened).values())
    assert all(cell[0] == 0 and 2 <= len(cell) <= 3 and set(cell[1:]) <= {1.5, 1.75, 2.5, 2.75}
               for cell in s['kicks']) and len(set(s['kicks'])) > 1
    collisions = Counter((n[0] // BAR, event_cell(n)) for n in drums)
    assert max(collisions.values()) == 1
    overlaps = 0
    for events in nt.values():
        ends = {}
        for when, duration, pitch, _ in events:
            overlaps += int(when < ends.get(pitch, -1))
            ends[pitch] = when + duration
    assert overlaps == 0
    _, _, (brk, _), (a2, _), (outro, _) = markers(n_bars)
    lead_bars = Counter(n[0] // BAR + 1 for n in nt[4])
    assert set(lead_bars) == set(range(brk - 8, brk)) | set(range(a2, outro))
    assert max(lead_bars.values()) <= 6
    leap = max(abs(a[2] - b[2]) for a, b in zip(nt[4], nt[4][1:]))
    assert leap <= 7
    for bar in range(1, n_bars + 1):
        layers = layers_at(s, bar)
        cell = s['kicks'][(bar - 1) % 4]
        in_bar = lambda ns: [n for n in ns if n[0] // BAR + 1 == bar]
        if 'Kick' in layers:
            kicks = in_bar(kick)
            assert tuple(event_cell(n) / 4 for n in kicks) == cell
            assert all(kicks[0][3] == n[3] + 6 for n in kicks[1:])
        else:
            assert not in_bar(kick)
        if 'Snare' in layers:
            assert [event_cell(n) for n in in_bar(back)] == [4, 12]
            assert 1 <= len(in_bar(ghost)) <= 2
        else:
            assert not in_bar(back) and not in_bar(ghost)
        hats_here = in_bar([n for n in drums if n[2] in (42, 46)])
        assert bool(hats_here) == ('Hats' in layers)
        if 'Keys' in layers:
            chord_onsets = Counter(n[0] for n in in_bar(nt[2]))
            assert 1 <= len(chord_onsets) <= 3 and set(chord_onsets.values()) == {4}
            pedal = [(t, v) for t, c, v in cc[2] if c == 64 and bt(bar) <= t < bt(bar + 1)]
            assert pedal[0][1] == 0 and pedal[-1][1] == 0 and any(v == 100 for _, v in pedal)
        if 'Bass' in layers:
            bass = in_bar(nt[1])
            assert len(cell) - len(bass) in (1, 2)
            assert all(event_cell(n) / 4 in cell for n in bass)
        for track, layer in ((1, 'Bass'), (2, 'Keys'), (3, 'Tex'), (4, 'Lead')):
            assert bool(in_bar(nt[track])) == (layer in layers)
        if s['pad']:
            assert bool(in_bar(pad)) == ('Pad' in layers)
        if bar > n_bars - 4:
            assert layers <= {'Keys', 'Final', 'Kick', 'Snare', 'Hats'} and 'Keys' in layers
    closer = '-'
    if s['slot'] == CLOSER_SLOT:
        last_drum = max(n[0] for n in drums) // BAR + 1
        last_bass = max(n[0] for n in nt[1]) // BAR + 1
        final = [n for n in nt[2] if n[0] // BAR + 1 == n_bars]
        assert last_drum == outro + 1 and last_bass == outro + 3
        assert all(not [n for n in nt[t] if n[0] // BAR + 1 >= outro] for t in (3, 4, 5))
        assert len(final) == 4 and len({n[0] for n in final}) == 1 and min(n[1] for n in final) >= 3 * PPQ
        assert sorted(n[2] for n in final) == list(s['chords'][0][3])
        closer = (f'drums_end_bar={last_drum} bass_end_bar={last_bass} keys_only={outro + 4}-{n_bars} '
                  f'final_chord={[n[2] for n in final]}@{final[0][1]}t')
    jitter = [n[0] % BAR - 14 - event_cell(n) * 120 -
              (s['swing'] if n[2] in (42, 46) and event_cell(n) % 4 == 2 else 0) for n in drums]
    assert min(jitter) >= -12 and max(jitter) <= 12
    assert min(jitter) <= -10 and max(jitter) >= 10
    crashes = [n for n in drums if n[2] == 49]
    assert len(crashes) == 1 and crashes[0][0] // BAR + 1 == a2 and 55 <= crashes[0][3] <= 70
    for bar, text in markers(n_bars):
        assert bytes([0xff, 6, len(text)]) + text.encode() in smf
    last_end = max(n[0] + n[1] for notes in nt.values() for n in notes)
    assert bt(n_bars) < last_end < bt(n_bars + 1)
    describe = lambda ns: f'{len(ns)}@{span([n[3] for n in ns])}'
    print(f"check {s['sid']} PASS kick={describe(kick)} snare/rim={describe(back)} "
          f"ghost={describe(ghost)} hat_on={describe(hats_on)} hat_off={describe(hats_off)} "
          f"hat16={describe(hats_extra) if hats_extra else '-'} open={describe(opened)} swing={s['swing']} "
          f"jitter={span(jitter)} bass={span([n[2] for n in nt[1]])}@{span([n[3] for n in nt[1]])} "
          f"keys={span([n[2] for n in nt[2]])}@{span([n[3] for n in nt[2]])}/CC64=yes "
          f"tex={span([n[2] for n in nt[3]])}@{span([n[3] for n in nt[3]])} "
          f"pad={describe(pad) if pad else '-'} "
          f"lead={brk - 8}-{brk - 1},{a2}-{outro - 1}/max={max(lead_bars.values())}/leap<={leap} "
          f"overlap={overlaps} drum_cell_collisions=0 markers={markers(n_bars)} "
          f"closer={closer} last_end={last_end}/{n_bars * BAR}")


def root_signature(s):
    return tuple((PC[c[1]] - PC[s['tonic']]) % 12 for c in (s['chords'][i] for i in s['order']))


def rotations(sig):
    return {sig[i:] + sig[:i] for i in range(len(sig))}


def chord_kind(name):
    return re.sub(r'^[A-G][#b]?', '', name)


def harmony_signature(s):
    return tuple(((PC[c[1]] - PC[s['tonic']]) % 12, chord_kind(c[0])) for c in (s['chords'][i] for i in s['order']))


def motif_signature(s):
    pitches = [p for bar in s['melody'] for p in bar]
    return (tuple(b - a for a, b in zip(pitches, pitches[1:])), s['lead_beats'])


def check_set():
    prior = lh_astra.SKETCHES + lh_fable.SKETCHES
    # rainy-window, slow-room, porch-pocket, late-bus (both modes) as tonic-relative root loops.
    existing = [(2, 7, 0, 9), (5, 4, 2, 7), (0, 9, 5, 7), (0, 8, 5, 7)]
    forbidden = set().union(*(rotations(r) for r in existing + [root_signature(p) for p in prior]))
    mine = [root_signature(s) for s in SKETCHES]
    assert len(set(mine)) == 10 and not any(rotations(r) & set(mine) - {r} for r in mine)
    assert not set(mine) & forbidden
    assert len({harmony_signature(s) for s in SKETCHES}) == len({motif_signature(s) for s in SKETCHES}) == 10
    assert not {motif_signature(s) for s in SKETCHES} & {motif_signature(p) for p in prior}
    assert not {tuple(p for bar in s['melody'] for p in bar) for s in SKETCHES} & \
        {tuple(p for bar in q['melody'] for p in bar) for q in prior}
    for field in ('kicks', 'comp', 'tex_beats', 'tex_order', 'break_id', 'ghosts'):
        assert len({s[field] for s in SKETCHES}) == 10
    for field in ('kicks', 'comp', 'tex_beats', 'break_id'):
        assert not {s[field] for s in SKETCHES} & {p[field] for p in prior}
    assert len({s['break_plan'] for s in SKETCHES}) == 10
    # Bar-by-bar break arrangements: no copy of any astra/fable plan, and no layer set shared with
    # the slot directly before or after (slots 2, 4, 5, 7, ... 29 are astra/fable).
    prior_plans = {p['slot']: tuple(frozenset(mod.break_layers(p['slot'], o)) for o in range(8))
                   for mod in (lh_astra, lh_fable) for p in mod.SKETCHES}
    for s in SKETCHES:
        plan = tuple(frozenset(break_layers(s, o)) for o in range(8))
        assert plan not in prior_plans.values()
        for nb in (s['slot'] - 1, s['slot'] + 1):
            assert not set(plan) & set(prior_plans.get(nb, ()))
    for s in SKETCHES:
        assert sum(n for n, _ in s['break_plan']) == 8
        assert all(48 <= p <= 72 for c in s['chords'] for p in c[3]) and all(len(c[3]) == 4 for c in s['chords'])
        assert all(len(bar) <= 6 for bar in s['melody'])
        assert s['bpm'] <= 78 and s['bars'] == 56 or s['bpm'] >= 80 and s['bars'] == 64
    neighbours = []
    for mine_slot, their_slot in ((6, 5), (15, 16), (21, 20)):
        a = next(s for s in SKETCHES if s['slot'] == mine_slot)
        b = next(p for p in prior if p['slot'] == their_slot)
        assert a['key'] == b['key']
        assert harmony_signature(a) != harmony_signature(b) and root_signature(b) not in rotations(root_signature(a))
        assert a['comp'] != b['comp'] and motif_signature(a) != motif_signature(b) and a['melody'] != b['melody']
        assert a['break_id'] != b['break_id']
        neighbours.append(f'{mine_slot}vs{their_slot}=loop/comp/motif/break-differ')
    print('set-check PASS tracks=10 unique_harmony=10 unique_motifs=10 kick_cells=10 comp_cells=10 '
          'texture_cells=10 breaks=10 prior_loops_avoided=yes(rotation-aware) astra_fable_cells_avoided=yes '
          'break_plans_vs_prior=distinct adjacent_slot_break_layers_shared=0 '
          f'same_key_neighbours={",".join(neighbours)}')


def check_prompts():
    path = Path(__file__).resolve().parents[1] / 'suno' / 'lh_opus.md'
    blocks = re.findall(r'^## (lh[^\n]+)-v1\n\*\*Style\*\*\n`([^`]+)`\n\n\*\*Description\*\*\n```\n(.*?)\n```',
                        path.read_text(), re.M | re.S)
    assert [b[0] for b in blocks] == [s['sid'] for s in SKETCHES]
    for (sid, style, description), s in zip(blocks, SKETCHES):
        assert len(style) <= 300 and len(description) <= 1000
        assert style.endswith('instrumental')
        assert s['key'] in description and f"{s['bpm']} BPM" in description
        assert 'no vocals, lo-fi warmth, DJ-friendly intro/outro' in description
        print(f'prompt-length {sid}-v1 Style={len(style)} Description={len(description)} PASS')


if __name__ == '__main__':
    check_set()
    for sketch in SKETCHES:
        result = compose(sketch['sid'])
        nt, cc, pcs, n_bars, bpm, title, sf, minor = result
        smf = build_smf(title, bpm, sf, minor, n_bars, tracks_for(sketch), pcs, nt, cc, markers(n_bars))
        check(sketch, result, smf)
        print(write_smf(os.path.join(SK_DIR, sketch['sid'] + '-v1.mid'), smf))
    check_prompts()
