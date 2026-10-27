"""Vivaldi 사계 12악장 주제 변주 — fable (anthropic/claude-fable-5-1), 2026-10-27.

원천: vivaldi_data.MOVEMENTS — Mutopia Project (CC BY-SA 3.0 전제, 작품은 퍼블릭 도메인). 이 파일이 쓰는 파생 MIDI 도 같은 출처 표기.
브리프 docs/music/VIVALDI_BRIEF.md §2 (Suno 통과 규칙): 한 성부만 · 리듬 변형 둘 이상 · 원리듬 연속 ≤ 4마디 · 박자/템포 이동 · 화성 재구성 · 주제 40~60%.

주제 처리 순서 (source 틱 → target 4/4 틱):
  extract(한 성부, 동시음은 위 음만) → thin(그리드 미만 off-grid 음을 앞 음에 흡수 = 런 솎기)
  → meter_map(4/4 그대로 · 3/4→4/4 마지막 음 4박까지 연장 · 3/8 두 마디→4/4 한 마디 "3+1" · 12/8→4/4 셔플 ×2/3)
  → halftime(×2, 선택) → vary(마디 패턴: 2·4박 8분 당김, 없으면 다운비트 8분 지연, 없으면 마디 전체 8분 지연; 패스마다 패턴 위상을
  반 바퀴 돌려 이웃 패스의 원리듬 구간이 맞닿지 않게) → 배치 → swing(lo-fi, 측정에는 들어가지 않음) → 옥타브/벨로시티.
곡 형식: lo-fi = intro 8 / A / break 8 / A2 / outro 8 (A=A2=(bars-24)/2), deep house = 96마디 v3 레시피 (1–8 / 9–48 / 49–56 / 57–88 / 89–96).
A·A2 안에서 주제 패스(길이, 트랙, 옥타브)를 순서대로 깔고 남는 마디는 자작 2마디 모티프.
점검(check): 곡 전체에서 평면 매핑과 리듬이 같은 마디의 최장 연속(스윙 제외) ≤ 4, 주제가 울리는 마디 40~60%, 벨로시티 밴드, 동일 음 겹침 0, END 안.

python3 vivaldi_fable.py            → sketches/vs-<season><n>-fable-v1.mid 12개 + 점검 줄
python3 vivaldi_fable.py vs-winter2-fable → 그 곡만
python3 vivaldi_fable.py --prompts  → suno/vivaldi_fable.md 블록 길이 측정
"""
import os
import sys

from pipeline import BAR, PPQ, SK_DIR, build_smf, hum_t, hum_v, seed, write_smf
from vivaldi_data import MOVEMENTS, bar_tick

MODEL = 'anthropic/claude-fable-5-1'
E, S = PPQ // 2, PPQ // 4
PC = {'C': 0, 'C#': 1, 'Db': 1, 'D': 2, 'D#': 3, 'Eb': 3, 'E': 4, 'F': 5, 'F#': 6, 'G': 7, 'G#': 8, 'Ab': 8, 'A': 9, 'A#': 10, 'Bb': 10, 'B': 11}
# rootless 4-voice voicings (bass carries the root) and the pitch-class scale a long melody note may sit on
# (minor chords accept both sixths — the baroque lines move between aeolian and dorian freely).
QUAL = {
    'maj9': ((4, 7, 11, 14), (0, 2, 4, 7, 9, 11)), 'maj13': ((4, 11, 14, 21), (0, 2, 4, 6, 7, 9, 11)),
    '6/9': ((4, 7, 9, 14), (0, 2, 4, 7, 9, 11)), 'm9': ((3, 7, 10, 14), (0, 2, 3, 5, 7, 8, 9, 10)),
    'm11': ((3, 10, 14, 17), (0, 2, 3, 5, 7, 8, 9, 10)), 'mM9': ((3, 7, 11, 14), (0, 2, 3, 5, 7, 8, 11)),
    '13': ((4, 10, 14, 21), (0, 2, 4, 5, 7, 9, 10)), '9': ((4, 10, 14, 19), (0, 2, 4, 5, 7, 9, 10)),
    '9sus': ((5, 10, 14, 19), (0, 2, 4, 5, 7, 9, 10)), '7b9': ((4, 10, 13, 19), (0, 1, 4, 5, 7, 8, 10)),
    '7#5': ((4, 10, 13, 20), (0, 1, 4, 6, 8, 10)),
}
MAJOR, MINOR = (0, 2, 4, 5, 7, 9, 11), (0, 2, 3, 5, 7, 8, 10)
KICK, SNARE, RIM, CLAP, HAT, OPEN_HAT, CRASH, RIDE, TOM_HI, TOM_MID, TOM_LO = 36, 38, 37, 39, 42, 46, 49, 51, 50, 47, 45

LOFI_TRACKS = [('Drums', 9), ('Bass', 0), ('Keys', 1), ('Tex', 2), ('Theme', 3), ('Theme2', 4)]
DH_TRACKS = [('Drums', 9), ('Bass', 0), ('Keys', 1), ('Pad', 2), ('Tex', 3), ('Theme', 4), ('Theme2', 5)]
DR, BS, KY = 0, 1, 2

# 리듬 변형 패턴: 마디 단위 0 = 원리듬 유지, 1 = vary() 적용. 4직·4변 (캐논 v3 선례 8직 → 더 보수적으로 4).
# 홀수 번째 패스는 패턴을 반 바퀴 돌려(위상 len/2) 앞 패스의 끝 "직" 구간과 다음 패스의 첫 "직" 구간이 맞닿지 않게 한다.
S4V4 = (0, 0, 0, 0, 1, 1, 1, 1)
S2V2 = (0, 0, 1, 1)
S3V5 = (0, 0, 0, 1, 1, 1, 1, 1)

# 브리프 §4 dict: key, sid, title, genre, bpm, bars, theme_part, theme_window(None = 데이터 기본 창), rhythm_ops, notes
# + 변환 매개변수(meter, grid, halftime, sync, swing), 화성(chords: (root, qual, bars) — 위상은 A 시작과 A2 시작(+lead_a2)에서 0),
# 주제 패스(passes_a/passes_a2: (bars, track 0|1, octave)), 악기(theme_pc: 트랙 0·1 의 PC), 장르 셀(lo-fi: kick/kick_b 홀·짝 마디 킥 셀,
# bass_iv 킥 자리별 음정; dh: bass_cell), 자작 모티프(2마디 셀: beat, dur_beats, scale degree).
SKETCHES = [
    dict(key=('spring', 1), sid='vs-spring1-fable', title='Spring I Fable', genre='dh', bpm=122, bars=96,
         theme_part='solo', theme_window=None, meter='4/4', grid=E, halftime=True, sync=S3V5, swing=0,
         tonic='E', mode=MAJOR, sf=4, minor=False,
         chords=[('B', '9sus', 1), ('E', 'maj9', 1), ('B', '9sus', 1), ('A', 'maj13', 1)],
         passes_a=[(26, 0, 0)], passes_a2=[(26, 1, 0)], theme_pc=(4, 80),
         keys_pc=4, keys_style='stab2', pad_pc=89, tex=('arp', 4, (0, 1, 2, 3, 2, 1, 0, 2)), bass_pc=38,
         bass_cell=[(0, 2.5, 0), (2.5, 0.5, 7)], oh_v=70, brk='hats-pad|hats-bass-pad',
         motif=[(0, 0.5, 4), (0.5, 0.5, 4), (1, 1, 2), (2.5, 0.5, 1), (3, 1, 0), (4.5, 0.5, 4), (5, 0.5, 5), (5.5, 1.5, 4)], motif_root=64,
         rhythm_ops=['음가 ×2 하프타임', '16분 런 솎기(8분 골격)', '2·4박 8분 당김(3직·5변; 피크업 마디 포함 4)'],
         notes='리토르넬로를 하프타임 122 로. B9sus–Emaj9–B9sus–Amaj13 덥 스탭(주제 A 음과 맞춘 루프), EP 주제 → 스퀘어 리드 재제시'),
    dict(key=('spring', 2), sid='vs-spring2-fable', title='Spring II Fable', genre='lofi', bpm=70, bars=56,
         theme_part='solo', theme_window=None, meter='3/4', grid=E, halftime=False, sync=S4V4, swing=28,
         tonic='C#', mode=MINOR, sf=4, minor=True,
         chords=[('C#', 'm9', 2), ('G#', '9', 2), ('C#', 'm9', 2), ('A', 'maj9', 2), ('G#', '7#5', 1)], lead_a2=3,
         passes_a=[(9, 0, 0), (4, 0, 0)], passes_a2=[(9, 1, -12), (4, 1, -12)], theme_pc=(4, 24),
         keys_pc=0, comp=[(0, 1.5), (2.5, 1.0)], tex=('hold', 16), bass_pc=33,
         bass_iv=(0, 7), kick=(0, 2.5), kick_b=(0, 1.75), ghosts=(3.75,), hat16=False, rim_even=False,
         brk='no-drums',
         motif=[(0, 1, 4), (1.5, 0.5, 3), (2, 1.5, 2), (4, 1, 0), (5.5, 0.5, 2), (6, 2, 1)], motif_root=73,
         rhythm_ops=['3/4→4/4 (마디 끝 음 4박까지 연장)', '2·4박 8분 당김(4직·4변)', '8분 스윙 28틱'],
         notes='Largo 를 70 붐뱁으로. 9마디 진행 C#m9×2–G#9×2–C#m9×2–Amaj9×2–G#7#5(주제 마디에 맞춤), A2 앞 모티프 3마디로 위상 정렬. 그랜드 컴핑 + 오르간 홀드'),
    dict(key=('spring', 3), sid='vs-spring3-fable', title='Spring III Fable', genre='dh', bpm=124, bars=96,
         theme_part='solo', theme_window=None, meter='12/8', grid=E, halftime=False, sync=S2V2, swing=0,
         tonic='E', mode=MAJOR, sf=4, minor=False,
         chords=[('F#', 'm11', 2), ('A', 'maj13', 1), ('B', '9sus', 1)],
         passes_a=[(12, 0, 0), (12, 0, 0)], passes_a2=[(12, 1, -12), (12, 1, -12)], theme_pc=(81, 4),
         keys_pc=4, keys_style='hold', pad_pc=90, tex=('hold', 16), bass_pc=38,
         bass_cell=[(0, 1.5, 0), (1.5, 0.5, 0), (2.5, 1.0, -5)], oh_v=74, brk='keys-pad|keys-pad-bass',
         motif=[(0, 0.67, 4), (0.67, 0.33, 5), (1, 1, 4), (2, 0.67, 2), (2.67, 0.33, 1), (3, 1, 0), (4, 2, 2), (6, 2, 4)], motif_root=64,
         rhythm_ops=['12/8→4/4 셔플(틱 ×2/3, 삼연음 8분)', '16분 솎기', '2·4박 당김(2직·2변)'],
         notes='시칠리아나를 셔플 하우스로. ii–IV–V 루프 F#m11×2–Amaj13–B9sus(주제의 A·G# 동거를 받아줌), 소우 리드 주제 → EP 한 옥타브 아래 재제시'),
    dict(key=('summer', 1), sid='vs-summer1-fable', title='Summer I Fable', genre='lofi', bpm=88, bars=64,
         theme_part='solo', theme_window=None, meter='3/8', grid=E, halftime=False, sync=S4V4, swing=26,
         tonic='G', mode=MINOR, sf=-2, minor=True,
         chords=[('G', 'm9', 1), ('D', '7b9', 1), ('Eb', 'maj9', 1), ('C', 'm9', 1)],
         passes_a=[(15, 0, 0)], passes_a2=[(15, 1, 0)], theme_pc=(24, 0),
         keys_pc=4, comp=[(0, 0.75), (1.5, 0.75), (2.5, 1.5)], tex=('hold', 16), bass_pc=33,
         bass_iv=(0, 0, -5), kick=(0, 1.5, 2.75), kick_b=(0, 2.5), ghosts=(1.25, 3.5), hat16=True, rim_even=False,
         brk='no-kick',
         motif=[(0, 0.5, 2), (0.5, 0.5, 2), (1, 1, 0), (2, 0.5, -1), (2.5, 1.5, 0), (4, 0.5, 2), (4.5, 0.5, 4), (5, 3, 3)], motif_root=67,
         rhythm_ops=['3/8 두 마디→4/4 한 마디 "3+1"(마지막 8분 연장)', '16분 솎기', '2·4박 당김(4직·4변)', '스윙 26틱'],
         notes='나른한 튜티를 3+1 8분 셀로. Gm9–D7♭9–E♭maj9–Cm9, 나일론 주제 → 그랜드 재제시. 햇 16분 e 장식'),
    dict(key=('summer', 2), sid='vs-summer2-fable', title='Summer II Fable', genre='lofi', bpm=70, bars=56,
         theme_part='solo', theme_window=None, meter='4/4', grid=E, halftime=False, sync=S4V4, swing=30,
         tonic='G', mode=MINOR, sf=-2, minor=True,
         chords=[('G', 'm9', 1), ('C', 'm11', 1), ('Eb', 'maj9', 1), ('D', '7#5', 1)],
         passes_a=[(8, 0, 0), (8, 0, 0)], passes_a2=[(8, 1, -12), (4, 1, -12)], theme_pc=(0, 4),
         keys_pc=4, comp=[(0, 2.0), (2.5, 1.0)], tex=('arp', 24, (0, 2, 1, 3, 2, 1, 0, 1)), bass_pc=33,
         bass_iv=(0, 12), kick=(0, 2.75), kick_b=(0, 1.5, 2.75), ghosts=(1.75,), hat16=False, rim_even=False,
         brk='drums-bass',
         motif=[(0, 1.5, 2), (1.5, 0.5, 1), (2, 2, 0), (4, 1, -2), (5, 1, 0), (6, 2, 2)], motif_root=67,
         rhythm_ops=['2·4박 당김(4직·4변)', '16분 솎기', '스윙 30틱', '템포 45→70'],
         notes='천둥 끊김 Adagio 를 그랜드 주제 + 나일론 아르페지오 위로. Gm9–Cm11–E♭maj9–D7#5. 주제 4마디째가 쉼이라 A 는 두 패스 전부. 브레이크는 드럼+베이스만'),
    dict(key=('summer', 3), sid='vs-summer3-fable', title='Summer III Fable', genre='dh', bpm=124, bars=96,
         theme_part='solo', theme_window=None, meter='3/4', grid=PPQ, halftime=False, sync=S3V5, swing=0,
         tonic='G', mode=MINOR, sf=-2, minor=True,
         chords=[('G', 'm11', 2), ('Eb', 'maj13', 1), ('D', '9sus', 1)],
         passes_a=[(20, 0, 0), (12, 0, 0)], passes_a2=[(20, 1, 12)], theme_pc=(4, 80),
         keys_pc=4, keys_style='dub', pad_pc=89, tex=('arp', 4, (0, 1, 2, 3, 0, 2, 1, 3)), bass_pc=38,
         bass_cell=[(0, 1.5, 0), (2.5, 0.5, 0), (3.5, 0.5, 0)], oh_v=76, brk='kick-hats-keys-pad|kick-hats-keys-pad-tex',
         motif=[(0, 0.5, 0), (0.5, 0.5, 0), (1, 0.5, 2), (1.5, 0.5, 0), (2.5, 0.5, -1), (3, 1, 0), (4, 0.5, 4), (4.5, 0.5, 3), (5, 1, 2), (6, 2, 0)], motif_root=67,
         rhythm_ops=['16분 폭풍 런을 4분 골격만', '3/4→4/4 (마디 끝 음 연장)', '2·4박 당김(3직·5변)'],
         notes='프레스토 폭풍을 4분 골격으로 솎아 124 덥 스탭 위에. Gm11–E♭maj13–D9sus, EP 주제 → 스퀘어 리드 한 옥타브 위'),
    dict(key=('autumn', 1), sid='vs-autumn1-fable', title='Autumn I Fable', genre='lofi', bpm=84, bars=64,
         theme_part='solo', theme_window=None, meter='4/4', grid=E, halftime=False, sync=S4V4, swing=28,
         tonic='F', mode=MAJOR, sf=-1, minor=False,
         chords=[('F', 'maj9', 1), ('D', 'm9', 1), ('G', 'm9', 1), ('C', '13', 1)],
         passes_a=[(12, 0, 0), (4, 0, 0)], passes_a2=[(12, 1, -12)], theme_pc=(4, 24),
         keys_pc=0, comp=[(0, 0.5), (1.5, 0.5), (2, 1.0), (3.5, 0.5)], tex=('arp', 24, (0, 1, 2, 1, 3, 2, 1, 2)), bass_pc=38,
         bass_iv=(0, 0, 7), kick=(0, 1.5, 2.5), kick_b=(0, 1.75, 2.5), ghosts=(0.75, 3.5), hat16=True, rim_even=False,
         brk='no-drums',
         motif=[(0, 0.5, 4), (0.5, 0.5, 5), (1, 1, 4), (2, 0.5, 2), (2.5, 1.5, 0), (4, 0.5, 2), (4.5, 0.5, 4), (5, 0.5, 5), (5.5, 2.5, 7)], motif_root=65,
         rhythm_ops=['템포 120→84 (−30%)', '16분 솎기', '2·4박 당김(4직·4변)', '스윙 28틱'],
         notes='춤 리토르넬로를 84 붐뱁으로. Fmaj9–Dm9–Gm9–C13 (I–vi–ii–V), 그랜드 컴핑, 펄스 베이스. EP 주제 → 나일론 한 옥타브 아래'),
    dict(key=('autumn', 2), sid='vs-autumn2-fable', title='Autumn II Fable', genre='lofi', bpm=72, bars=56,
         theme_part='violin1', theme_window=None, meter='3/4', grid=PPQ, halftime=False, sync=S2V2, swing=26,
         tonic='D', mode=MINOR, sf=-1, minor=True,
         chords=[('D', 'm9', 2), ('G', 'm9', 2), ('F', 'maj9', 1), ('Bb', '13', 1), ('D', 'm9', 1), ('D', '7b9', 1), ('G', 'm9', 1), ('A', '9sus', 1), ('D', 'maj9', 1)],
         passes_a=[(11, 0, -12)], passes_a2=[(11, 1, 0), (5, 1, 0)], theme_pc=(24, 4),
         keys_pc=4, comp=[(0, 3.0)], tex=('hold', 16), bass_pc=33,
         bass_iv=(0, -5), kick=(0, 2.5), kick_b=(0, 2.75), ghosts=(3.75,), hat16=False, rim_even=True,
         brk='no-kick',
         motif=[(0, 1, 2), (1, 1, 1), (2, 2, 0), (4, 1.5, -2), (5.5, 0.5, 0), (6, 2, 1)], motif_root=74,
         rhythm_ops=['3/4→4/4 (마디 끝 음 연장)', '2·4박 당김/다운비트 지연(2직·2변)', '스윙 26틱'],
         notes='거의 화음뿐인 Adagio — 브리프대로 violin1 의 긴 음 13개를 주제로. 그 음에 맞춘 11마디 진행 Dm9×2–Gm9×2–Fmaj9–B♭13–Dm9–D7♭9–Gm9–A9sus–Dmaj9 홀드, 짝수 마디 림, 나일론 주제 → EP'),
    dict(key=('autumn', 3), sid='vs-autumn3-fable', title='Autumn III Fable', genre='dh', bpm=122, bars=96,
         theme_part='solo', theme_window=None, meter='3/8', grid=S, halftime=False, sync=S4V4, swing=0,
         tonic='F', mode=MAJOR, sf=-1, minor=False,
         chords=[('F', '6/9', 2), ('Bb', 'maj9', 1), ('C', '9sus', 1)],
         passes_a=[(12, 0, 0), (12, 0, 0)], passes_a2=[(12, 1, 0), (12, 1, 0)], theme_pc=(80, 4),
         keys_pc=4, keys_style='stab2', pad_pc=89, tex=('hold', 16), bass_pc=38,
         bass_cell=[(0, 2.0, 0), (2.5, 0.5, 0), (3.5, 0.5, 7)], oh_v=72, brk='hats-pad|hats-bass-pad',
         motif=[(0, 0.5, 0), (0.5, 0.5, 2), (1, 0.5, 4), (1.5, 0.5, 4), (2.5, 0.5, 2), (3, 1, 0), (4, 0.5, 4), (4.5, 0.5, 2), (5, 1, 0), (6, 2, -3)], motif_root=65,
         rhythm_ops=['3/8 두 마디→4/4 한 마디 "3+1"', '32분 꾸밈 흡수(16분 그리드)', '2·4박 당김/마디 지연(4직·4변, 패스마다 위상 반전)'],
         notes='사냥 호른 콜을 3+1 셀로 122 위에. F6/9–B♭maj9–C9sus, 스퀘어 리드 주제 → EP 재제시, 오르간 롱 코드'),
    dict(key=('winter', 1), sid='vs-winter1-fable', title='Winter I Fable', genre='dh', bpm=118, bars=96,
         theme_part='solo', theme_window=(4, 12), meter='4/4', grid=E, halftime=False, sync=S4V4, swing=0,
         tonic='F', mode=MINOR, sf=-4, minor=True,
         chords=[('F', 'm11', 2), ('Db', 'maj9', 2)],
         passes_a=[(9, 0, 0), (9, 0, 0), (9, 0, 0)], passes_a2=[(9, 1, 0), (9, 1, 0)], theme_pc=(4, 81),
         keys_pc=4, keys_style='dub', pad_pc=89, tex=('arp', 16, (0, 3, 1, 2, 0, 3, 1, 2)), bass_pc=38,
         bass_cell=[(0, 3.0, 0), (3.5, 0.5, -5)], oh_v=68, brk='keys-pad|keys-pad-bass',
         motif=[(0, 0.25, 0), (0.25, 0.25, 0), (0.5, 0.25, 0), (0.75, 0.25, 0), (1, 0.5, 0), (2, 0.25, 2), (2.25, 0.25, 2), (2.5, 0.5, 2), (3, 1, 0),
                (4, 0.25, -2), (4.25, 0.25, -2), (4.5, 0.5, -2), (5, 1, 0), (6, 2, -1)], motif_root=65,
         rhythm_ops=['주제 창 4–12 (solo 진입부; 1–3 은 solo 가 쉼)', '32분 트릴 흡수(8분 그리드)', '2·4박 당김(4직·4변)', '템포 140→118'],
         notes='떨림 화음 1–3 마디는 solo 가 비어 창을 4–12 로 옮김. 떨림은 EP(Theme 트랙) 의 자작 모티프(같은 음 반복 16분)로 흉내. Fm11 ↔ D♭maj9 2코드, 9마디 패스라 둘째·셋째 패스는 다른 위상에서 시작'),
    dict(key=('winter', 2), sid='vs-winter2-fable', title='Winter II Fable', genre='lofi', bpm=68, bars=56,
         theme_part='solo', theme_window=None, meter='4/4', grid=E, halftime=False, sync=S4V4, swing=30,
         tonic='Eb', mode=MAJOR, sf=-3, minor=False,
         chords=[('Eb', 'maj9', 1), ('C', 'm9', 1), ('Ab', 'maj9', 1), ('Bb', '13', 1)],
         passes_a=[(8, 0, 0), (8, 0, 0)], passes_a2=[(8, 1, -12)], theme_pc=(4, 0),
         keys_pc=0, comp=[(0, 1.0), (2, 1.0), (3, 0.5)], tex=('arp', 24, (0, 1, 2, 3, 2, 1, 0, 1)), bass_pc=33,
         bass_iv=(0, 7, 0), kick=(0, 1.75), kick_b=(0, 1.5, 2.75), ghosts=(3.5,), hat16=True, rim_even=False,
         brk='drums-bass',
         motif=[(0, 1, 2), (1, 0.5, 4), (1.5, 0.5, 2), (2, 2, 0), (4, 1, -1), (5, 1, 0), (6, 2, 2)], motif_root=63,
         rhythm_ops=['16분 꾸밈 솎기(8분 골격)', '2·4박 당김(4직·4변)', '스윙 30틱', '템포 46→68'],
         notes='Largo 선율을 68 로. E♭maj9–Cm9–A♭maj9–B♭13, 나일론 피킹이 피치카토 대신. EP 주제 → 그랜드 한 옥타브 아래'),
    dict(key=('winter', 3), sid='vs-winter3-fable', title='Winter III Fable', genre='dh', bpm=124, bars=96,
         theme_part='solo', theme_window=None, meter='3/8', grid=E, halftime=False, sync=S4V4, swing=0,
         tonic='F', mode=MINOR, sf=-4, minor=True,
         chords=[('F', 'mM9', 2), ('F', 'm9', 1), ('Db', 'maj9', 1), ('F', 'mM9', 2)],
         passes_a=[(12, 0, 0), (12, 0, 0)], passes_a2=[(12, 1, -12), (12, 1, 0)], theme_pc=(81, 4),
         keys_pc=4, keys_style='hold', pad_pc=90, tex=('arp', 4, (0, 2, 1, 3, 2, 0, 1, 3)), bass_pc=38,
         bass_cell=[(0, 3.5, 0)], oh_v=70, brk='hats-pad|hats-bass-pad',
         motif=[(0, 0.5, 0), (0.5, 0.5, 2), (1, 0.5, 4), (1.5, 0.5, 7), (2, 1, 4), (3, 1, 2), (4, 0.5, 0), (4.5, 0.5, 2), (5, 1, 0), (6, 2, -3)], motif_root=65,
         rhythm_ops=['3/8 두 마디→4/4 한 마디 "3+1"', '16분 아르페지오 솎기(8분)', '2·4박 당김/마디 지연(4직·4변, 패스마다 위상 반전)'],
         notes='cello F 페달을 Fm(maj9) 정지 화성 6마디 루프 Fm(maj9)×2–Fm9–D♭maj9–Fm(maj9)×2 로(주제의 E 음 수용). 솔로 16분 아르페지오를 8분 3+1 로 솎음. 소우 리드 → EP 한 옥타브 아래'),
]


# ---------------------------------------------------------------- theme pipeline
def extract(s):
    """One part of the theme window, re-based so the window's first downbeat is tick 0 (pickup = negative ticks)."""
    key, m = s['key'], MOVEMENTS[s['key']]
    a, b = s['theme_window'] or m['theme']
    t0, t1 = bar_tick(key, a), bar_tick(key, b + 1)
    lo = 0 if a == 1 else t0
    notes = sorted((t - t0, d, p) for t, d, p in m['parts'][s['theme_part']] if lo <= t < t1)
    mono = {}
    for t, d, p in notes:                       # simultaneous onsets: keep the top voice
        if t not in mono or p > mono[t][1]:
            mono[t] = (d, p)
    return [(t, d, p) for t, (d, p) in sorted(mono.items())], t1 - t0


def thin(notes, grid):
    """Short off-grid notes (runs, ornaments) are absorbed by the preceding kept note; skeleton stays."""
    out = []
    for t, d, p in notes:
        if d < grid and t % grid:
            if out and out[-1][0] + out[-1][1] >= t:
                pt, pd, pp = out[-1]
                out[-1] = (pt, max(pd, t + d - pt), pp)
            continue
        out.append((t, d, p))
    return out


def meter_map(kind):
    """(map_tick, map_end): source meter → target 4/4. Notes ending on a source bar line stretch to the target bar line."""
    if kind == '12/8':
        return (lambda t: t * 2 // 3), (lambda e: e * 2 // 3)
    sb, tb = {'4/4': (BAR, BAR), '3/4': (3 * PPQ, BAR), '3/8': (3 * E, BAR // 2)}[kind]

    def mt(t):
        return (t // sb) * tb + t % sb

    def me(e):
        return (e // sb) * tb if e % sb == 0 else mt(e)
    return mt, me


def vary(notes, pattern, phase=0):
    """Per target bar flagged in `pattern` (read at bar + phase): anticipate beat-2/4 onsets by an eighth;
    failing that, delay the downbeat note; failing that, push the whole bar late by an eighth (notes that would
    cross the bar line are dropped, never overlapped onto the next downbeat)."""
    notes = sorted(notes)
    by_bar = {}
    for i, (t, d, p) in enumerate(notes):
        by_bar.setdefault(t // BAR, []).append(i)
    out, drop = list(notes), set()
    for bar, idxs in by_bar.items():
        if bar < 0 or not pattern[(bar + phase) % len(pattern)]:
            continue
        changed = False
        for i in idxs:
            t, d, p = out[i]
            if t % BAR in (PPQ, 3 * PPQ) and not (i and out[i - 1][0] >= t - E):
                out[i] = (t - E, d + E, p)
                if i and out[i - 1][0] + out[i - 1][1] > t - E:
                    pt, pd, pp = out[i - 1]
                    out[i - 1] = (pt, t - E - pt, pp)
                changed = True
        if changed:
            continue
        i = idxs[0]
        t, d, p = out[i]
        if t % BAR == 0 and d >= PPQ:
            out[i] = (t + E, d - E, p)                           # lazy downbeat
            continue
        end = (bar + 1) * BAR                                    # dense eighths: whole bar late by an eighth
        for i in idxs:
            t, d, p = out[i]
            room = end - (t + E)
            if room < 30:
                drop.add(i)
            else:
                out[i] = (t + E, min(d, room), p)
    return sorted(n for i, n in enumerate(out) if i not in drop)


def swing(notes, sw):
    return [(t + sw, max(S, d - sw), p) if t % PPQ == E else (t, d, p) for t, d, p in notes]


def theme_target(s):
    """Returns (plain, (varied phase 0, varied phase len/2), n_bars): plain = thinned + meter-mapped (+halftime)."""
    src, src_len = extract(s)
    src = thin(src, s['grid'])
    mt, me = meter_map(s['meter'])
    plain = [(mt(t), me(t + d) - mt(t), p) for t, d, p in src]
    n_bars = -(-me(src_len) // BAR)
    if s['halftime']:
        plain = [(t * 2, d * 2, p) for t, d, p in plain]
        n_bars *= 2
    varied = (vary(plain, s['sync'], 0), vary(plain, s['sync'], len(s['sync']) // 2))
    return plain, varied, n_bars


def straight_run(plain, final, covered):
    """Longest run of bars (over the whole placed song) whose onset/duration set equals the plain mapping.
    `covered` = 0-based bars inside a theme pass: a rest bar inside a pass neither counts nor breaks the run;
    any bar outside the passes (motif, break) breaks it."""
    def shape(notes):
        shp = {}
        for t, d, p in notes:
            shp.setdefault(t // BAR, set()).add((t % BAR, d))
        return shp
    a, b = shape(plain), shape(final)
    best = run = 0
    for bar in range(max(list(a) + list(b)) + 1):
        if bar not in covered:
            run = 0
            continue
        if bar not in a and bar not in b:
            continue
        if a.get(bar) == b.get(bar):
            run += 1
            best = max(best, run)
        else:
            run = 0
    return best


# ---------------------------------------------------------------- harmony helpers
def voicing(root, qual, base):
    iv, _ = QUAL[qual]
    r = base + (PC[root] - base % 12) % 12
    return [r + i for i in iv]


def chord_at(s, bar):
    """(root, qual) of a 1-based bar. The loop restarts at the A start and at the A2 start (+lead_a2), so the first
    pass of each section meets phase 0; later passes meet phase (pass offset % loop length)."""
    loop = [(r, q) for r, q, n in s['chords'] for _ in range(n)]
    fm = form(s)
    if bar < fm['a']:
        return loop[(bar - 1) % len(loop)]                    # intro plays the loop from its start (no reverse wrap)
    anchor = fm['a2'] + s.get('lead_a2', 0) if bar >= fm['a2'] else fm['a']
    return loop[(bar - anchor) % len(loop)]


def scale_pitch(s, degree, root):
    return root + 12 * (degree // 7) + s['mode'][degree % 7]


def bass_root(s, bar, lo=28, hi=48):
    root, _ = chord_at(s, bar)
    p = lo + (PC[root] - lo % 12) % 12
    return p if p <= hi else p - 12


def bass_pitch(root, iv, lo, hi):
    """Root + interval folded into [lo, hi]; an octave that would leave the range becomes the fifth above,
    a fifth below that would leave it becomes the fifth above (never a unison)."""
    p = root + iv
    if (iv == 12 and p > hi) or (iv == -5 and p < lo):
        return root + 7
    return p + 12 if p < lo else (p - 12 if p > hi else p)


def offbeat8(beat):
    """True for the swung eighth positions 0.5, 1.5, 2.5, 3.5 (sixteenth e/a positions stay straight)."""
    return beat % 1 == 0.5


# ---------------------------------------------------------------- form
def form(s):
    """Section start bars (1-based) and markers."""
    n = s['bars']
    if s['genre'] == 'dh':
        a, brk, a2, outro = 9, 49, 57, 89
    else:
        half = (n - 24) // 2
        a, brk, a2, outro = 9, 9 + half, 17 + half, n - 7
    return dict(a=a, brk=brk, a2=a2, outro=outro, end=n + 1,
                markers=[(1, 'intro'), (a, 'A'), (brk, 'break'), (a2, 'A2'), (outro, 'outro')])


def theme_plan(s, fm, variants):
    """Lay the passes into A and A2 (A2 may start with `lead_a2` motif bars). `variants` is a tuple of note lists;
    pass k (counted over the song) uses variants[k % len(variants)]. Returns (events by track, residual bars)."""
    events, covered, residual, k = {}, set(), [], 0
    for start, end, passes, lead in ((fm['a'], fm['brk'], s['passes_a'], 0), (fm['a2'], fm['outro'], s['passes_a2'], s.get('lead_a2', 0))):
        bar = start + lead
        for length, track, octave in passes:
            assert bar + length <= end, f'{s["sid"]}: pass of {length} bars does not fit {start}-{end - 1}'
            lim = (bar - 1 + length) * BAR
            for t, d, p in variants[k % len(variants)]:
                tt = (bar - 1) * BAR + t                      # a pickup lands in the preceding bar (intro / break / previous pass)
                if tt >= lim or tt < 0:
                    continue
                events.setdefault(track, []).append((tt, min(d, lim - tt), p + octave))
                if t < 0:
                    covered.add(bar - 1)                      # the pickup bar counts as original rhythm too
            covered.update(range(bar, bar + length))
            bar += length
            k += 1
        residual += [b for b in range(start, end) if b not in covered]
    return events, residual, {b - 1 for b in covered}


def sounding_bars(events):
    """1-based bars in which a theme note starts or sustains."""
    bars = set()
    for evs in events.values():
        for t, d, p in evs:
            bars.update(range(t // BAR + 1, (t + d - 1) // BAR + 2))
    return bars


def motif_events(s, bars):
    out = []
    for b in bars:
        cell = (b - 9) % 2
        for beat, dur, deg in s['motif']:
            if int(beat // 4) != cell:
                continue
            t = (b - 1) * BAR + int((beat - 4 * cell) * PPQ)
            out.append((t, int(dur * PPQ) - 20, scale_pitch(s, deg, s['motif_root'])))
    return out


# ---------------------------------------------------------------- renderers
def dedupe(notes):
    """Same-pitch overlaps are illegal for Logic's importer: shorten the earlier note, drop it when nothing is left."""
    notes = sorted(notes)
    last, drop = {}, set()
    for i, (t, d, p, v) in enumerate(notes):
        if p in last:
            j = last[p]
            pt, pd, pp, pv = notes[j]
            if pt + pd > t:
                if t - pt - 5 < 30:
                    drop.add(j)
                else:
                    notes[j] = (pt, t - pt - 5, pp, pv)
        last[p] = i
    return [n for i, n in enumerate(notes) if i not in drop]


def add_theme(nt, track, events, base_v, lo, hi, amt_t):
    for t, d, p in events:
        v = base_v + (6 if t % BAR == 0 else 0)
        nt[track].append((hum_t(t, amt_t), max(S // 2, d - 15), p, min(hi, max(lo, hum_v(v, 8)))))


def mono_clip(notes):
    """Theme tracks are one voice (brief §2-1): after humanising, a note never sounds past the next onset."""
    notes = sorted(notes)
    for i in range(len(notes) - 1):
        t, d, p, v = notes[i]
        nxt = notes[i + 1][0]
        if t + d > nxt:
            notes[i] = (t, max(10, nxt - t - 1), p, v)
    return notes


def clamp(v, lo, hi):
    return min(hi, max(lo, v))


def compose(sid):
    s = next(x for x in SKETCHES if x['sid'] == sid)
    seed(271027 + sum(ord(c) for c in sid))
    fm = form(s)
    plain, varied, n_theme = theme_target(s)
    events, residual, covered = theme_plan(s, fm, varied)
    plain_events, _, _ = theme_plan(s, fm, (plain,))
    flat = lambda ev: [n for evs in ev.values() for n in evs]
    straight = straight_run(flat(plain_events), flat(events), covered)   # measured before swing: swing is not a rhythm op here
    theme_bars = sounding_bars(events)
    if s['swing']:
        events = {k: swing(v, s['swing']) for k, v in events.items()}
    r = (compose_dh if s['genre'] == 'dh' else compose_lofi)(s, fm, events, residual)
    nt, cc, pcs, tracks = r
    end = s['bars'] * BAR
    for i in nt:
        nt[i] = dedupe([(t, min(d, end - t), p, v) for t, d, p, v in nt[i] if 0 <= t < end])
        if tracks[i][0].startswith('Theme'):
            nt[i] = mono_clip(nt[i])
    stats = dict(straight=straight, theme_bars=len(theme_bars), n_theme=n_theme, ratio=round(100 * len(theme_bars) / s['bars']))
    return nt, cc, pcs, tracks, stats


def compose_lofi(s, fm, events, residual):
    tracks = LOFI_TRACKS
    TX, TH, TH2 = 3, 4, 5
    pcs = {DR: 0, BS: s['bass_pc'], KY: s['keys_pc'], TX: s['tex'][1], TH: s['theme_pc'][0], TH2: s['theme_pc'][1]}
    nt = {i: [] for i in range(len(tracks))}
    cc = {KY: []}
    sw = s['swing']
    a, brk, a2, outro, end = fm['a'], fm['brk'], fm['a2'], fm['outro'], fm['end']

    def layers(bar):
        if bar < a:
            return {'keys', 'tex'} | ({'hats'} if bar >= 3 else set()) | ({'kick', 'snare'} if bar >= 5 else set())
        if brk <= bar < a2:
            return {'no-drums': {'keys', 'tex'}, 'no-kick': {'hats', 'snare', 'keys', 'tex', 'bass'},
                    'drums-bass': {'kick', 'snare', 'hats', 'bass'}}[s['brk']]
        if bar >= outro:
            return {'kick', 'snare', 'hats', 'keys', 'bass'} if bar < outro + 4 else {'keys'}
        return {'kick', 'snare', 'hats', 'keys', 'tex', 'bass'}

    def beat_tick(t0, b):
        return t0 + int(b * PPQ) + (sw if offbeat8(b) else 0)

    for bar in range(1, end):
        L, t0 = layers(bar), (bar - 1) * BAR
        root, qual = chord_at(s, bar)
        voice = voicing(root, qual, 44)
        # drums — SoCal boom bap (recipe bands: kick 96–110, snare 86–100, ghost 38–52, hats 48–60 / 68–84)
        if 'kick' in L:
            for b in (s['kick'] if bar % 2 else s['kick_b']):   # two cells alternate: never the same slots in every bar
                nt[DR].append((hum_t(beat_tick(t0, b), 12), 100, KICK, clamp(hum_v(105 if b == 0 else 101, 7), 96, 110)))
        if 'snare' in L:
            for b in (1, 3):
                if s['rim_even'] and bar % 2 == 0:
                    nt[DR].append((hum_t(t0 + b * PPQ, 10), 100, RIM, clamp(hum_v(93, 7), 86, 100)))
                else:
                    nt[DR].append((hum_t(t0 + b * PPQ, 10), 100, SNARE, clamp(hum_v(93, 7), 86, 100)))
            oh_bar = bar % 4 == 0
            for g in s['ghosts']:
                if (bar % 2 == 0 or len(s['ghosts']) == 1) and not (oh_bar and g == 3.5):   # the open hat owns that slot
                    nt[DR].append((hum_t(beat_tick(t0, g), 12), 80, SNARE, clamp(hum_v(45, 7), 38, 52)))
        if 'hats' in L:
            oh_bar = bar % 4 == 0
            for k in range(8):
                t = t0 + k * E + (sw if k % 2 else 0)
                if oh_bar and k == 7:
                    nt[DR].append((hum_t(t, 10), 220, OPEN_HAT, clamp(hum_v(70, 6), 64, 76)))
                else:
                    nt[DR].append((hum_t(t, 12), 90, HAT, clamp(hum_v(54, 6), 48, 60) if k % 2 == 0 else clamp(hum_v(76, 8), 68, 84)))
            if s['hat16'] and bar % 2 == 1:
                for b in (1.25, 3.25):
                    nt[DR].append((hum_t(t0 + int(b * PPQ), 10), 70, HAT, clamp(hum_v(45, 5), 40, 50)))
        if bar == a2:
            nt[DR].append((t0, 400, CRASH, 62))
        # bass — finger (or pulse) on this bar's kick slots (recipe: follow the kick, leave notes out so it breathes):
        # a two-kick bar keeps both, a three-kick even bar drops its last slot, and every bar's last note ends early. E1..C3, 60–82
        if 'bass' in L:
            r = bass_root(s, bar)
            slots = list(s['kick'] if bar % 2 else s['kick_b'])
            if bar % 2 == 0 and len(slots) > 2:
                slots = slots[:-1]
            for j, b in enumerate(slots):
                nxt = slots[j + 1] if j + 1 < len(slots) else 4.0
                dur = int((nxt - b) * PPQ) - (60 if j + 1 < len(slots) else 180)
                nt[BS].append((hum_t(beat_tick(t0, b), 8), dur, bass_pitch(r, s['bass_iv'][j % len(s['bass_iv'])], 28, 48), clamp(hum_v(72, 10), 60, 82)))
        # keys — jazz comping 72–92, CC64 per bar
        if 'keys' in L:
            hits = s['comp'] if bar < outro + 4 else [(0, 3.5)]
            pedal_up = t0 + BAR - 12
            for b, dur in hits:
                start = beat_tick(t0, b)
                length = min(int(dur * PPQ) - 20, pedal_up - 20 - start)   # a chord never hangs into the next bar's pedal
                for p in voice:
                    nt[KY].append((hum_t(start, 8), length, p, clamp(hum_v(82, 10), 72, 92)))
            cc[KY] += [(t0, 64, 127), (pedal_up, 64, 0)]
        # texture — nylon arpeggio or organ hold, 55–72
        if 'tex' in L:
            kind = s['tex'][0]
            if kind == 'arp':
                tones = voice[1:] + [voice[0] + 12]
                for k, idx in enumerate(s['tex'][2]):
                    t = t0 + k * E + (sw if k % 2 else 0)
                    nt[TX].append((hum_t(t, 10), E - 25, tones[idx], clamp(hum_v(63, 8), 55, 72)))
            else:
                for p in voice[1:]:
                    nt[TX].append((t0 + 10, BAR - 40, p + 12, clamp(hum_v(61, 6), 55, 72)))
    for track, evs in events.items():
        add_theme(nt, TH if track == 0 else TH2, evs, 70, 60, 82, 10)
    motif = swing(motif_events(s, residual + [b for b in range(5, a)]), sw)
    add_theme(nt, TH, motif, 64, 60, 82, 10)
    return nt, cc, pcs, tracks


def compose_dh(s, fm, events, residual):
    tracks = DH_TRACKS
    PD, TX, TH, TH2 = 3, 4, 5, 6
    pcs = {DR: 16, BS: s['bass_pc'], KY: s['keys_pc'], PD: s['pad_pc'], TX: s['tex'][1], TH: s['theme_pc'][0], TH2: s['theme_pc'][1]}
    nt = {i: [] for i in range(len(tracks))}
    cc = {KY: []}
    a, brk, a2, outro, end = fm['a'], fm['brk'], fm['a2'], fm['outro'], fm['end']
    first, second = s['brk'].split('|')
    brk_sets = {'hats-pad': {'hats', 'pad'}, 'hats-bass-pad': {'hats', 'bass', 'pad'},
                'keys-pad': {'keys', 'pad'}, 'keys-pad-bass': {'keys', 'pad', 'bass'},
                'kick-hats-keys-pad': {'kick', 'hats', 'keys', 'pad'}, 'kick-hats-keys-pad-tex': {'kick', 'hats', 'keys', 'pad', 'tex'}}
    fill_bars = (16, brk - 1, outro - 1)

    def layers(bar):
        if bar < a:
            return {'pad', 'hats'} | ({'kick'} if bar >= 5 else set())
        if brk <= bar < a2:
            return brk_sets[first if bar < brk + 4 else second]
        if bar >= outro:
            return {'kick', 'hats', 'back', 'bass'} | ({'pad'} if bar < outro + 4 else set())
        return {'kick', 'hats', 'back', 'bass', 'keys', 'pad', 'tex'}

    pad_hold = None
    for bar in range(1, end):
        L, t0 = layers(bar), (bar - 1) * BAR
        root, qual = chord_at(s, bar)
        voice = voicing(root, qual, 56)
        in_a2 = a2 <= bar < outro
        # drums — Tough Kit, v3 separation (kick 106–112 on one / 100–105, hats 50–62 / 74–90, open 65–80, snare 88–100, clap 80–92, ride 60–75)
        if 'kick' in L:
            for b in range(4):
                nt[DR].append((hum_t(t0 + b * PPQ, 8), 110, KICK, clamp(hum_v(109, 4), 106, 112) if b == 0 else clamp(hum_v(102, 4), 100, 105)))
        if 'hats' in L:
            for k in range(8):
                t = t0 + k * E
                if k in (3, 7):
                    nt[DR].append((hum_t(t, 8), 180, OPEN_HAT, clamp(hum_v(s['oh_v'], 5), 65, 80)))
                elif k % 2 == 0 and in_a2 and 'kick' in L:
                    nt[DR].append((hum_t(t, 8), 150, RIDE, clamp(hum_v(67, 5), 60, 75)))
                else:
                    nt[DR].append((hum_t(t, 8), 90, HAT, clamp(hum_v(56, 6), 50, 62) if k % 2 == 0 else clamp(hum_v(82, 8), 74, 90)))
            if bar % 2 == 0 and bar not in fill_bars:         # the tom fill owns the late sixteenths
                nt[DR].append((hum_t(t0 + 13 * S, 8), 70, HAT, clamp(hum_v(56, 5), 50, 62)))
        if 'back' in L:
            for b in (1, 3):
                nt[DR].append((hum_t(t0 + b * PPQ, 8), 110, SNARE, clamp(hum_v(94, 5), 88, 100)))
                nt[DR].append((hum_t(t0 + b * PPQ, 8), 110, CLAP, clamp(hum_v(86, 5), 80, 92)))
        if bar in fill_bars:
            for b, p in ((3.25, TOM_HI), (3.75, TOM_MID)) if bar != fill_bars[1] else ((2.75, TOM_HI), (3.25, TOM_MID), (3.75, TOM_LO)):
                nt[DR].append((hum_t(t0 + int(b * PPQ), 6), 140, p, hum_v(88, 5)))
        if bar == a2:
            nt[DR].append((t0, 500, CRASH, 72))
        # bass — sub E1..A2, long root + off-beat
        if 'bass' in L:
            r = bass_root(s, bar, 28, 45)
            for b, dur, iv in s['bass_cell']:
                nt[BS].append((hum_t(t0 + int(b * PPQ), 6), int(dur * PPQ) - 30, bass_pitch(r, iv, 28, 45), clamp(hum_v(90, 5), 84, 96)))
        # keys — C4..C6, 72–92, hold / 2 stabs / dub
        if 'keys' in L:
            hits = {'hold': [(0, 3.9)], 'stab2': [(0, 1.9), (2, 1.9)], 'dub': [(0.5, 0.75), (2.5, 0.75)]}[s['keys_style']]
            for b, dur in hits:
                for p in voice:
                    nt[KY].append((hum_t(t0 + int(b * PPQ), 6), int(dur * PPQ) - 20, p, clamp(hum_v(82, 8), 72, 92)))
            cc[KY] += [(t0, 64, 127), (t0 + BAR - 12, 64, 0)]
        # pad — 1+5+9 over the sub root, held per chord change, 55–72
        if 'pad' in L:
            r = bass_root(s, bar, 28, 45)
            trio = (r + 12, r + 19, r + 26)
            if pad_hold and pad_hold[1] == trio and pad_hold[2] == bar - 1:
                pad_hold[2] = bar
            else:
                if pad_hold:
                    flush_pad(nt, PD, pad_hold)
                pad_hold = [bar, trio, bar]
        elif pad_hold:
            flush_pad(nt, PD, pad_hold)
            pad_hold = None
        # texture — EP/organ arpeggio or organ long chord, 55–70
        if 'tex' in L:
            kind = s['tex'][0]
            if kind == 'arp':
                for k, idx in enumerate(s['tex'][2]):
                    nt[TX].append((hum_t(t0 + k * E, 6), E - 30, voice[idx], clamp(hum_v(62, 6), 55, 70)))
            else:
                for p in voice[1:]:
                    nt[TX].append((t0 + 10, BAR - 40, p, clamp(hum_v(61, 6), 55, 70)))
    if pad_hold:
        flush_pad(nt, PD, pad_hold)
    for track, evs in events.items():
        add_theme(nt, TH if track == 0 else TH2, evs, 80, 72, 88, 6)
    add_theme(nt, TH, motif_events(s, residual), 74, 72, 88, 6)
    return nt, cc, pcs, tracks


def flush_pad(nt, PD, hold):
    start, trio, last = hold
    t0, dur = (start - 1) * BAR, (last - start + 1) * BAR - 30
    for p in trio:
        nt[PD].append((t0 + 5, dur, p, clamp(hum_v(63, 6), 55, 72)))


# ---------------------------------------------------------------- checks
def span(vals):
    return f'{min(vals)}..{max(vals)}' if vals else '-'


def check(s, nt, cc, stats, tracks):
    """Brief §2 bounds and recipe bands. Velocities are clamped at the source, so the band lines are a report;
    straight_max / theme ratio / END / overlap are the real gates."""
    sid, n = s['sid'], s['bars']
    assert stats['straight'] <= 4, f'{sid}: {stats["straight"]} consecutive original-rhythm bars'
    assert 40 <= stats['ratio'] <= 60, f'{sid}: theme ratio {stats["ratio"]}%'
    last = max(t + d for tr in nt.values() for t, d, _, _ in tr)
    assert last <= n * BAR, f'{sid}: last note end {last} > {n * BAR}'
    v = lambda tr, pitches=None: [x[3] for x in nt[tr] if pitches is None or x[2] in pitches]
    th = {i for i, (name, _) in enumerate(tracks) if name.startswith('Theme')}
    theme_v = [x[3] for i in th for x in nt[i]]
    if s['genre'] == 'dh':
        band = (f'kick {span(v(DR, (KICK,)))} hat {span(v(DR, (HAT,)))} oh {span(v(DR, (OPEN_HAT,)))} snare {span(v(DR, (SNARE,)))} '
                f'ride {span(v(DR, (RIDE,)))} | bass {span(v(BS))} keys {span(v(KY))} pad {span(v(3))} tex {span(v(4))} theme {span(theme_v)}')
        assert all(72 <= x <= 88 for x in theme_v) and all(55 <= x <= 72 for x in v(3)) and all(84 <= x <= 96 for x in v(BS))
    else:
        snare, ghost = [x for x in v(DR, (SNARE,)) if x > 60], [x for x in v(DR, (SNARE,)) if x <= 60]
        band = (f'kick {span(v(DR, (KICK,)))} snare {span(snare)} rim {span(v(DR, (RIM,)))} ghost {span(ghost)} hat {span(v(DR, (HAT,)))} '
                f'| keys {span(v(KY))} bass {span(v(BS))} tex {span(v(3))} theme {span(theme_v)}')
        assert all(60 <= x <= 82 for x in theme_v) and all(60 <= x <= 82 for x in v(BS)) and all(86 <= x <= 100 for x in v(DR, (RIM,)))
    # keys: no chord sounds across its bar's pedal-up (CC64 leak into the next bar)
    ups = sorted(t for t, c, val in cc.get(KY, []) if c == 64 and val == 0)
    for t, d, p, _ in nt[KY]:
        nxt = next((u for u in ups if u > t), None)
        assert nxt is None or t + d <= nxt, f'{sid}: keys note at {t} sounds past pedal-up {nxt}'
    # long theme notes vs chord scale
    clashes = total = 0
    for i in th:
        for t, d, p, _ in nt[i]:
            if d < PPQ - 40:
                continue
            total += 1
            root, qual = chord_at(s, t // BAR + 1)
            if (p - PC[root]) % 12 not in QUAL[qual][1]:
                clashes += 1
    # same-pitch overlap
    for i, tr in nt.items():
        ends = {}
        for t, d, p, _ in sorted(tr):
            assert ends.get(p, -1) <= t, f'{sid}: overlap pitch {p} track {tracks[i][0]} at {t}'
            ends[p] = t + d
    # the theme tracks are monophonic (brief §2-1: one voice)
    for i in th:
        prev_end = -1
        for t, d, p, _ in sorted(nt[i]):
            assert t >= prev_end, f'{sid}: polyphony on {tracks[i][0]} at {t}'
            prev_end = max(prev_end, t + d)
    m = MOVEMENTS[s['key']]
    ratio = s['bpm'] / m['tempo_bpm'] / (2 if s['halftime'] else 1) * (1.5 if s['meter'] == '12/8' else 1)
    return (f'  straight_max={stats["straight"]} theme={stats["ratio"]}% ({stats["theme_bars"]}/{n} bars, pass={stats["n_theme"]}) '
            f'tempo {m["tempo_bpm"]}→{s["bpm"]} ×{ratio:.2f} | {band} | clashes {clashes}/{total} | last_bar={last / BAR:.1f}')


def render(sid):
    s = next(x for x in SKETCHES if x['sid'] == sid)
    nt, cc, pcs, tracks, stats = compose(sid)
    report = check(s, nt, cc, stats, tracks)                  # assert before anything is written
    smf = build_smf(s['title'], s['bpm'], s['sf'], s['minor'], s['bars'], tracks, pcs, nt, cc, form(s)['markers'])
    print(write_smf(os.path.join(SK_DIR, f'{sid}-v1.mid'), smf))
    print(report)


def check_prompts():
    """Suno 블록 길이 (공백·내부 줄바꿈 포함): Style ≤ 300, Description ≤ 1,000, 12블록 전부, 원곡 제목은 Description 에만."""
    import re
    path = os.path.join(os.path.dirname(SK_DIR), 'suno', 'vivaldi_fable.md')
    blocks = re.findall(r'^## (vs-[a-z0-9]+-fable)-v1\n\*\*Style\*\*\n`([^`]+)`\n\n\*\*Description\*\*\n```\n(.*?)\n```',
                        open(path, encoding='utf-8').read(), re.M | re.S)
    sids = [s['sid'] for s in SKETCHES]
    assert [b[0] for b in blocks] == sids, f'blocks {[b[0] for b in blocks]} != {sids}'
    for sid, style, desc in blocks:
        assert len(style) <= 300 and len(desc) <= 1000, f'{sid}: style {len(style)} desc {len(desc)}'
        assert 'Four Seasons' in desc and 'Vivaldi' not in style and 'Seasons' not in style, sid
        print(f'| {sid} | {len(style)} | {len(desc)} |')


if __name__ == '__main__':
    if sys.argv[1:] == ['--prompts']:
        check_prompts()
        sys.exit()
    want = sys.argv[1:] or [s['sid'] for s in SKETCHES]
    titles = [s['title'] for s in SKETCHES]
    assert len(set(titles)) == len(titles)
    print(f'model {MODEL}')
    for sid in want:
        render(sid)
