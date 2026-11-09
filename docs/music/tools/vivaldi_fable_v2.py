"""Vivaldi 사계 12악장 주제 변주 v2 — fable (anthropic/claude-fable-5-1), 2026-11-09.

계획: docs/music/vivaldi_fable_v2_plan.md (장르·편성·박자·BPM·마디). 브리프: docs/music/VIVALDI_BRIEF_V2.md.
원천: vivaldi_data.MOVEMENTS — Mutopia Project (CC BY-SA 3.0 전제, 작품은 퍼블릭 도메인). 모든 MIDI 의 첫 악기 트랙 틱 0 에 저작권 메타(0x02)를
넣는다(지휘 트랙에 넣으면 Logic 이 빈 트랙을 하나 더 만든다 — with_copyright 참조).

주제 파이프라인 (source 틱 → target 박자 틱):
  extract(한 성부, 동시음은 윗음) → thin(그리드 미만 off-grid 음을 앞 음에 흡수 = 런 솎기) → meter_map(계획의 박자 변환)
  → stretch(음가 ×2 또는 ×½, 선택) → vary(마디 패턴: 지정 박 8분 당김 / 다운비트 지연 / 마디 전체 지연; 홀수 패스는 패턴 위상 반 바퀴) → 배치 → swing(장르별).
점검: 곡 전체 원리듬 최장 연속(스윙 전; 온셋 없이 지속만 하는 마디도 원리듬으로 셈) ≤ 4, 울리는 마디 주제 40~60 %, 실효 템포 ±15 % 이상 또는 음가 ×2/×½,
      층 하나뿐인 구간(전주·후주 제외) 연속 ≤ 2, 1박 이상 주제 음의 코드 스케일 밖 수(보고),
      트랙별 벨로시티 범위·구간별 음/마디·베이스 음/마디, 주제 트랙 단성, 동일 음 겹침 0, 마지막 음 END 안.

python3 vivaldi_fable_v2.py            → sketches/vs-<season><n>-fable-v2.mid 12개 + 점검 줄
python3 vivaldi_fable_v2.py vs-winter2-fable
python3 vivaldi_fable_v2.py --check    → 파일을 쓰지 않고 재생성 바이트와 디스크 MIDI 를 비교
python3 vivaldi_fable_v2.py --prompts  → suno/vivaldi_fable_v2.md 블록 길이 측정
"""
import os
import struct
import sys

from pipeline import PPQ, SK_DIR, build_smf, hum_t, hum_v, seed, varlen, write_smf
from vivaldi_data import MOVEMENTS, bar_tick

MODEL = 'anthropic/claude-fable-5-1'
VER = 'v2'
COPYRIGHT = 'Theme: Vivaldi, Le quattro stagioni (Mutopia Project, CC BY-SA 3.0); arrangement 2026 band-fable (claude-fable-5-1)'
E, S = PPQ // 2, PPQ // 4
PC = {'C': 0, 'C#': 1, 'Db': 1, 'D': 2, 'D#': 3, 'Eb': 3, 'E': 4, 'F': 5, 'F#': 6, 'G': 7, 'G#': 8, 'Ab': 8, 'A': 9, 'A#': 10, 'Bb': 10, 'B': 11}
# voicing intervals above the root (root itself is the bass's job unless the voicing starts at 0) and the scale a long theme note may sit on
QUAL = {
    'maj': ((0, 4, 7, 12), (0, 2, 4, 5, 7, 9, 11)), 'm': ((0, 3, 7, 12), (0, 2, 3, 5, 7, 8, 9, 10)),
    'maj7': ((4, 7, 11, 14), (0, 2, 4, 7, 9, 11)), 'maj9': ((4, 7, 11, 14), (0, 2, 4, 7, 9, 11)), 'add9': ((0, 4, 7, 14), (0, 2, 4, 5, 7, 9, 11)),
    'm7': ((3, 7, 10, 14), (0, 2, 3, 5, 7, 8, 9, 10)), 'm9': ((3, 7, 10, 14), (0, 2, 3, 5, 7, 8, 9, 10)), 'madd9': ((0, 3, 7, 14), (0, 2, 3, 5, 7, 8, 10)),
    '7': ((4, 7, 10, 12), (0, 2, 4, 5, 7, 9, 10)), '9': ((4, 10, 14, 19), (0, 2, 4, 5, 7, 9, 10)), '9sus': ((5, 10, 14, 19), (0, 2, 4, 5, 7, 9, 10)),
    'sus': ((0, 5, 7, 12), (0, 2, 4, 5, 7, 9, 10)), '6': ((0, 4, 7, 9), (0, 2, 4, 5, 7, 9, 11)), 'mM7': ((0, 3, 7, 11), (0, 2, 3, 5, 7, 8, 11)),
}
MAJOR, MINOR = (0, 2, 4, 5, 7, 9, 11), (0, 2, 3, 5, 7, 8, 10)
KICK, SNARE, RIM, CLAP, HAT, OPEN_HAT, CRASH, RIDE, TAMB, SHAKER, CONGA_LO, CONGA_HI = 36, 38, 37, 39, 42, 46, 49, 51, 54, 70, 64, 63

S4V4 = (0, 0, 0, 0, 1, 1, 1, 1)
S3V5 = (0, 0, 0, 1, 1, 1, 1, 1)
S2V2 = (0, 0, 1, 1)

# 박자 변환: (source bar ticks, target bar ticks, '3+1' 연장 여부). None = 틱 그대로(마디 수만 바뀜).
MAPS = {'4/4': None, '3/4': None, '12/8→6/8': None, '4/4→2/4': None, '3/8→4/4': (3 * E, 2 * PPQ), '3/4→4/4': (3 * PPQ, 4 * PPQ)}

# 트랙: (이름, MIDI 채널, GM PC(경로 A) 또는 자리표시자, 패치 spec(경로 B 이름 | C (바탕 패치, EXS) | None))
SKETCHES = [
    dict(key=('spring', 1), sid='vs-spring1-fable', title='Spring I Fable', genre='chamber pop (60s baroque pop)',
         genre_reason='4/4 E장조 리토르넬로의 밝은 호출-응답을 하프시코드·현악·가벼운 드럼의 팝 코러스로',
         meter=(4, 4), bpm=96, bars=72, form=(8, 8, 8), map='4/4', theme_part='solo', theme_window=None, grid=E, antic=(PPQ, 3 * PPQ),
         sync=S3V5, swing=0, tonic='E', mode=MAJOR, sf=4, minor=False,
         tracks=[('Drums', 9, 0, None), ('Bass', 0, 33, None), ('Harpsichord', 1, 6, 'Harpsichord'), ('Strings', 2, 48, None),
                 ('Theme', 3, 56, None), ('Theme2', 4, 6, 'Harpsichord')],
         chords=[('E', 'maj', 1), ('C#', 'm7', 1), ('A', 'maj7', 1), ('B', '7', 1)],
         passes_a=[(13, 'Theme', 0), (8, 'Theme', 0)], passes_a2=[(13, 'Theme2', 12)], theme_v=((66, 86), (62, 82)),
         parts=dict(Drums=dict(kind='drums', cells=[[(0, KICK, 100), (2.5, KICK, 92), (1, SNARE, 94), (3, SNARE, 94)] + [(k / 2, HAT, 58 if k % 2 == 0 else 46) for k in range(8)],
                                                       [(0, KICK, 100), (2, KICK, 92), (1, SNARE, 94), (3, SNARE, 94), (3.5, SNARE, 50)] + [(k / 2, HAT, 58 if k % 2 == 0 else 46) for k in range(8)]],
                               every4=[(3.5, OPEN_HAT, 66)], hum=(10, 6), band=(40, 110)),
                    Bass=dict(kind='bass', cell=[(0, 1.5, 0), (1.5, 0.5, 0), (2, 1.0, 7), (3, 1.0, 0)], lo=28, hi=50, vel=(80, 8), band=(66, 94)),
                    Harpsichord=dict(kind='arp', step=E, pattern=(0, 1, 2, 3, 2, 1, 0, 2), base=52, vel=(76, 8), band=(62, 92)),
                    Strings=dict(kind='pad', base=55, vel=(58, 5), band=(50, 68)),
                    Theme=dict(kind='theme'), Theme2=dict(kind='theme')),
         intro={'Harpsichord': 1, 'Strings': 1, 'Drums': 5, 'Bass': 5}, brk={'Harpsichord', 'Strings', 'Bass'}, outro_keep=['Drums', 'Bass', 'Harpsichord'], outro_last={'Harpsichord'},
         motif=[(0, 0.5, 4), (0.5, 0.5, 4), (1, 1, 2), (2.5, 0.5, 1), (3, 1, 0), (4.5, 0.5, 4), (5, 0.5, 5), (5.5, 1.5, 4)], motif_root=76,
         rhythm_ops=['16분 런 솎기(8분 골격)', '2·4박 8분 당김(3직·5변, 패스마다 위상 반전)', '템포 115→96 (−17%)'],
         notes='E–C#m7–Amaj7–B7 팝 루프 위 하프시코드 8분 아르페지오·현악 홀드. 트럼펫 주제 → 하프시코드 한 옥타브 위 재제시'),
    dict(key=('spring', 2), sid='vs-spring2-fable', title='Spring II Fable', genre='celtic air (harp, tin whistle)',
         genre_reason='3/4 Largo 의 독주 선율과 잎 소리 반주를 하프 분산화음 위 휘슬 에어로; 3/4 를 지키고 템포만 올림',
         meter=(3, 4), bpm=84, bars=84, form=(8, 8, 8), map='3/4', stretch=2, theme_part='solo', theme_window=None, grid=E, antic=(PPQ, 2 * PPQ),
         sync=S2V2, swing=0, tonic='C#', mode=MINOR, sf=4, minor=True,
         tracks=[('Harp', 0, 46, 'Celtic Harp'), ('Cellos', 1, 42, None), ('Theme', 2, 73, 'Celtic Tin Whistle'), ('Theme2', 3, 24, None), ('Strings', 4, 48, None)],
         chords=[('C#', 'madd9', 2), ('A', 'maj7', 2), ('G#', '7', 2), ('F#', 'maj', 2), ('C#', 'madd9', 2), ('A', 'maj7', 2), ('F#', 'm7', 2), ('A', 'maj7', 2), ('C#', 'madd9', 2)],
         passes_a=[(18, 'Theme', 0), (12, 'Theme', 0)], passes_a2=[(18, 'Theme2', -12)], theme_v=((60, 82), (58, 78)),
         parts=dict(Harp=dict(kind='arp', step=E, pattern=(0, 1, 2, 3, 2, 1), base=48, vel=(66, 8), band=(52, 82)),
                    Cellos=dict(kind='bass', cell=[(0, 2.9, 0)], lo=36, hi=55, vel=(62, 6), band=(52, 74)),
                    Strings=dict(kind='pad', base=60, vel=(48, 5), band=(40, 58)),
                    Theme=dict(kind='theme'), Theme2=dict(kind='theme')),
         intro={'Harp': 1, 'Cellos': 3, 'Strings': 5}, brk={'Harp', 'Strings'}, outro_keep=['Harp', 'Cellos', 'Strings'], outro_last={'Harp'},
         motif=[(0, 1, 4), (1, 0.5, 3), (1.5, 0.5, 2), (2, 1, 0), (3, 1.5, 2), (4.5, 0.5, 1), (5, 1, 0)], motif_root=73,
         rhythm_ops=['음가 ×2 (9마디 → 18마디, 실효 템포 ×0.84)', '2·3박 8분 당김(2직·2변)', '템포 50→84'],
         notes='C#m(add9)–Amaj7–G#7–F#–C#m(add9)–Amaj7–F#m7–Amaj7–C#m(add9) 2마디씩 18마디 루프(×2 주제 18마디의 음에 맞춤). 휘슬 주제 + 머리 12마디 재제시 → 나일론 한 옥타브 아래'),
    dict(key=('spring', 3), sid='vs-spring3-fable', title='Spring III Fable', genre='tarantella (Italian folk 6/8)',
         genre_reason='12/8 시칠리아나 목가 춤을 같은 이탈리아 6/8 춤 타란텔라로; 한 마디를 6/8 두 마디로 묶고 템포를 올림',
         meter=(6, 8), bpm=168, bars=168, form=(16, 16, 16), map='12/8→6/8', theme_part='solo', theme_window=None, grid=E, antic=(3 * E,),
         sync=S2V2, swing=0, tonic='E', mode=MAJOR, sf=4, minor=False,
         tracks=[('Perc', 9, 40, None), ('Bass', 0, 32, None), ('Strum', 1, 24, None), ('Lute', 2, 24, 'Medieval Lute'), ('Theme', 3, 71, 'Clarinet Solo'), ('Theme2', 4, 24, None)],
         chords=[('E', 'maj', 2), ('A', 'maj', 1), ('B', '7', 1)],
         passes_a=[(24, 'Theme', 0), (24, 'Theme', 0)], passes_a2=[(24, 'Theme2', -12), (24, 'Theme', 0)], theme_v=((64, 86), (60, 80)),
         parts=dict(Perc=dict(kind='drums', cells=[[(0, CONGA_LO, 96), (1.5, CONGA_LO, 84), (0, TAMB, 84), (0.5, TAMB, 56), (1, TAMB, 62), (1.5, TAMB, 80), (2, TAMB, 56), (2.5, TAMB, 62)],
                                                      [(0, CONGA_LO, 96), (1.5, CONGA_HI, 80), (2.5, CONGA_LO, 70), (0, TAMB, 84), (0.5, TAMB, 56), (1, TAMB, 62), (1.5, TAMB, 80), (2, TAMB, 56), (2.5, TAMB, 62)]],
                              every4=[], hum=(8, 6), band=(44, 104)),
                    Bass=dict(kind='bass', cell=[(0, 1.4, 0), (1.5, 1.4, 7)], lo=28, hi=50, vel=(82, 8), band=(68, 96)),
                    Strum=dict(kind='comp', hits=[(0, 1.3), (1.5, 0.4), (2, 0.4), (2.5, 0.4)], base=52, vel=(70, 8), band=(56, 86), cc64=False),
                    Lute=dict(kind='arp', step=E, pattern=(0, 2, 1, 3, 2, 1), base=57, vel=(66, 8), band=(52, 82)),
                    Theme=dict(kind='theme'), Theme2=dict(kind='theme')),
         intro={'Strum': 1, 'Lute': 1, 'Perc': 5, 'Bass': 9}, brk={'Lute', 'Bass', 'Perc'}, outro_keep=['Strum', 'Lute', 'Bass', 'Perc'], outro_last={'Strum', 'Lute'},
         motif=[(0, 0.5, 4), (0.5, 0.5, 5), (1, 0.5, 4), (1.5, 1.5, 2), (3, 0.5, 2), (3.5, 0.5, 3), (4, 0.5, 2), (4.5, 1.5, 0)], motif_root=76,
         rhythm_ops=['12/8→6/8 (한 마디를 두 마디로)', '16분 솎기', '둘째 박(점4분) 8분 당김(2직·2변)', '템포 ×1.17(마디 시간 기준)'],
         notes='E–E–A–B7 2마디 단위 타란텔라 루프, 탬버린·프레임 드럼, 나일론 스트럼 + 류트 아르페지오. 클라리넷 주제 → 나일론 재제시'),
    dict(key=('summer', 1), sid='vs-summer1-fable', title='Summer I Fable', genre='roots reggae / dub',
         genre_reason='3/8 "더위에 늘어진" 튜티를 뒷박에 기대는 원드롭과 멜로디카로; 3/8 두 마디를 4/4 한 마디로',
         meter=(4, 4), bpm=62, bars=48, form=(8, 8, 8), map='3/8→4/4', theme_part='solo', theme_window=(1, 24), grid=E, antic=(PPQ, 3 * PPQ),
         sync=S4V4, swing=0, tonic='G', mode=MINOR, sf=-2, minor=True,
         tracks=[('Drums', 9, 26, None), ('Bass', 0, 33, None), ('Organ', 1, 16, None), ('Skank', 2, 25, None), ('Theme', 3, 109, None), ('Theme2', 4, 16, None)],
         chords=[('G', 'm7', 1), ('C', 'm7', 1), ('G', 'm7', 1), ('D', '7', 1)],
         passes_a=[(12, 'Theme', 0)], passes_a2=[(12, 'Theme2', -12)], theme_v=((64, 84), (58, 76)),
         parts=dict(Drums=dict(kind='drums', cells=[[(2, KICK, 102), (2, RIM, 88)] + [(k / 2, HAT, 60 if k % 2 == 0 else 48) for k in range(8)] + [(3.75, HAT, 44)],
                                                       [(2, KICK, 102), (2, RIM, 88), (3.5, KICK, 84)] + [(k / 2, HAT, 60 if k % 2 == 0 else 48) for k in range(8)]],
                               every4=[(3.5, OPEN_HAT, 64)], hum=(10, 6), band=(40, 110)),
                    Bass=dict(kind='bass', cell=[(0, 1.4, 0), (2.5, 0.5, 7), (3, 0.9, 0)], lo=28, hi=48, vel=(84, 8), band=(70, 98)),
                    Organ=dict(kind='comp', hits=[(0.75, 0.2), (1.75, 0.2), (2.75, 0.2), (3.75, 0.2)], base=55, vel=(66, 8), band=(52, 82), cc64=False),
                    Skank=dict(kind='comp', hits=[(0.5, 0.3), (1.5, 0.3), (2.5, 0.3), (3.5, 0.3)], base=52, vel=(74, 8), band=(60, 90), cc64=False),
                    Theme=dict(kind='theme'), Theme2=dict(kind='theme')),
         intro={'Skank': 1, 'Organ': 1, 'Drums': 3, 'Bass': 5}, brk={'Drums', 'Bass'}, outro_keep=['Drums', 'Bass', 'Skank', 'Organ'], outro_last={'Skank', 'Organ'},
         motif=[(0, 0.5, 2), (0.5, 0.5, 2), (1, 1, 0), (2.5, 0.5, -1), (3, 1, 0), (4, 0.5, 2), (4.5, 0.5, 4), (5, 3, 3)], motif_root=67,
         rhythm_ops=['3/8 두 마디→4/4 한 마디(세 8분 + 연장)', '16분 솎기', '2·4박 당김(4직·4변)', '8분음 속도 −17%'],
         notes='Gm7–Cm7–Gm7–D7, 원드롭(킥+림 3박), 스컁 뒷박 기타, 오르간 버블 a-자리. 멜로디카 주제 → 오르간 한 옥타브 아래. 창 1–24(12마디)'),
    dict(key=('summer', 2), sid='vs-summer2-fable', title='Summer II Fable', genre='neoclassical ambient',
         genre_reason='4/4 Adagio 의 독주 선율을 천둥이 끊는 장면: 지속 현악 위 솔로 바이올린, 팀파니 트레몰로가 천둥, 하프가 빗방울',
         meter=(4, 4), bpm=56, bars=44, form=(6, 4, 6), map='4/4', theme_part='solo', theme_window=None, grid=PPQ, antic=(PPQ, 3 * PPQ),
         sync=S4V4, swing=0, tonic='G', mode=MINOR, sf=-2, minor=True,
         tracks=[('Strings', 0, 48, ('Full Strings', 'Full Strings Legato')), ('Harp', 1, 46, 'Harp'), ('Timpani', 2, 47, ('Timpani', 'Timpani Tremolo')),
                 ('Theme', 3, 40, ('Violins 1', 'Violin (Arco)')), ('Theme2', 4, 46, 'Harp')],
         chords=[('G', 'm9', 2), ('Eb', 'maj7', 2), ('C', 'm7', 2), ('D', '9sus', 2)],
         passes_a=[(8, 'Theme', 0), (6, 'Theme', 0)], passes_a2=[(8, 'Theme2', 0)], theme_v=((58, 80), (56, 78)),
         parts=dict(Strings=dict(kind='pad', base=55, vel=(56, 5), band=(46, 66)),
                    Harp=dict(kind='arp', step=PPQ, pattern=(0, 2, 1, 3), base=60, vel=(60, 8), band=(46, 76)),
                    Timpani=dict(kind='thunder', pitch=43, vel=(84, 6), band=(60, 104)),
                    Theme=dict(kind='theme'), Theme2=dict(kind='theme')),
         intro={'Strings': 1, 'Harp': 3, 'Timpani': 1}, brk={'Strings', 'Timpani'}, outro_keep=['Strings', 'Harp', 'Timpani'], outro_last={'Strings'},
         motif=[(0, 2, 4), (2, 1, 2), (3, 1, 3), (4, 2.5, 2), (6.5, 1.5, 0)], motif_root=74,
         rhythm_ops=['8분·16분 솎기(4분 골격 — 23음 → 14음, 8마디 중 6마디 변함)', '2·4박 당김(4직·4변)', '템포 45→56 (+24%)'],
         notes='Gm9–E♭maj7–Cm7–D9sus 2마디씩 현악 지속, 하프 4분 아르페지오, 팀파니 롤은 구간 끝(천둥). 솔로 바이올린 주제 → 하프 재제시'),
    dict(key=('summer', 3), sid='vs-summer3-fable', title='Summer III Fable', genre='drum and bass',
         genre_reason='3/4 프레스토 폭풍의 속도와 무게를 174 BPM 브레이크비트와 서브베이스로; 런은 골격만, 3/4 를 4/4 로',
         meter=(4, 4), bpm=174, bars=128, form=(16, 16, 16), map='3/4→4/4', theme_part='solo', theme_window=None, grid=PPQ, antic=(PPQ, 3 * PPQ),
         sync=S3V5, swing=0, tonic='G', mode=MINOR, sf=-2, minor=True,
         tracks=[('Drums', 9, 25, None), ('Sub', 0, 38, None), ('Pad', 1, 90, None), ('Riser', 2, 101, None), ('Theme', 3, 81, None), ('Theme2', 4, 80, None)],
         chords=[('G', 'm', 2), ('Eb', 'maj', 1), ('F', 'maj', 1)],
         passes_a=[(20, 'Theme', 0), (20, 'Theme', 0)], passes_a2=[(20, 'Theme2', 12)], theme_v=((74, 94), (70, 90)),
         parts=dict(Drums=dict(kind='drums', cells=[[(0, KICK, 108), (2.5, KICK, 100), (1, SNARE, 104), (3, SNARE, 104), (3.75, SNARE, 48)] + [(k / 2, HAT, 64 if k % 2 == 0 else 50) for k in range(8)],
                                                       [(0, KICK, 108), (1.75, KICK, 96), (2.5, KICK, 100), (1, SNARE, 104), (3, SNARE, 104), (2.25, SNARE, 46)] + [(k / 2, HAT, 64 if k % 2 == 0 else 50) for k in range(8)]],
                               every4=[(3.5, OPEN_HAT, 70)], hum=(6, 6), band=(40, 118)),
                    Sub=dict(kind='bass', cell=[(0, 1.9, 0), (2.5, 0.5, 0), (3, 0.9, -5)], lo=28, hi=43, vel=(96, 6), band=(84, 108)),
                    Pad=dict(kind='pad', base=60, vel=(62, 5), band=(52, 72)),
                    Riser=dict(kind='riser', pitch=72, vel=(70, 4), band=(60, 80)),
                    Theme=dict(kind='theme'), Theme2=dict(kind='theme')),
         intro={'Pad': 1, 'Riser': 1, 'Drums': 9, 'Sub': 9}, brk={'Pad', 'Riser', 'Sub'}, outro_keep=['Drums', 'Sub', 'Pad'], outro_last={'Drums', 'Sub'},
         motif=[(0, 0.5, 0), (0.5, 0.5, 0), (1, 0.5, 2), (1.5, 0.5, 0), (2.5, 0.5, -1), (3, 1, 0), (4, 0.5, 4), (4.5, 0.5, 3), (5, 1, 2), (6, 2, 0)], motif_root=67,
         rhythm_ops=['16분 런→4분 골격', '3/4→4/4 (마디 끝 음 연장)', '2·4박 당김(3직·5변)', '템포 150→174 (+16%)'],
         notes='Gm–Gm–E♭–F 패드, 투스텝 브레이크, 서브 루트 + 5도 아래. 소우 리드 주제 → 스퀘어 한 옥타브 위. 라이저는 드롭 앞 2마디'),
    dict(key=('autumn', 1), sid='vs-autumn1-fable', title='Autumn I Fable', genre='polka (harvest dance)',
         genre_reason='4/4 "농부의 춤과 노래" 리토르넬로를 2/4 움파 폴카로: 튜바·아코디언 뒷박·트럼펫·스네어',
         meter=(2, 4), bpm=100, bars=144, form=(16, 16, 16), map='4/4→2/4', theme_part='solo', theme_window=None, grid=PPQ, antic=(PPQ,),
         sync=S4V4, swing=0, tonic='F', mode=MAJOR, sf=-1, minor=False,
         tracks=[('Drums', 9, 0, None), ('Tuba', 0, 58, 'Tuba'), ('Accordion', 1, 21, 'Polka Accordion'), ('Theme', 2, 56, None), ('Theme2', 3, 65, None)],
         chords=[('F', 'maj', 2), ('C', '7', 2), ('F', 'maj', 1), ('Bb', 'maj', 1), ('C', '7', 1), ('F', 'maj', 1)],
         passes_a=[(24, 'Theme', 0), (24, 'Theme', 0)], passes_a2=[(24, 'Theme2', -12)], theme_v=((70, 90), (64, 84)),
         parts=dict(Drums=dict(kind='drums', cells=[[(0, KICK, 100), (1, SNARE, 90), (0.5, HAT, 50), (1.5, HAT, 56)], [(0, KICK, 100), (1, SNARE, 90), (1.5, SNARE, 52), (0.5, HAT, 50), (1.5, HAT, 56)]],
                               every4=[], hum=(8, 6), band=(40, 110)),
                    Tuba=dict(kind='bass', cell=[(0, 0.9, 0)], alt=[(0, 0.9, 7)], lo=29, hi=48, vel=(88, 8), band=(72, 104)),
                    Accordion=dict(kind='comp', hits=[(0.5, 0.4), (1.5, 0.4)], base=57, vel=(74, 8), band=(60, 90), cc64=False),
                    Theme=dict(kind='theme'), Theme2=dict(kind='theme')),
         intro={'Accordion': 1, 'Tuba': 1, 'Drums': 9}, brk={'Tuba', 'Drums'}, outro_keep=['Drums', 'Tuba', 'Accordion'], outro_last={'Tuba', 'Accordion'},
         motif=[(0, 0.5, 4), (0.5, 0.5, 5), (1, 0.5, 4), (1.5, 0.5, 2), (2, 1, 0), (3, 0.5, 2), (3.5, 0.5, 4)], motif_root=77,
         rhythm_ops=['4/4→2/4 (한 마디를 두 마디로)', '8분·16분 솎기(4분 골격 — 84음 → 45음, 24마디 중 21마디 변함)', '둘째 박 8분 당김(4직·4변)', '템포 120→100 (−17%)'],
         notes='F–C7–F–B♭–C7–F 8마디 폴카 루프(2/4), 튜바 움(근음·5도 교대), 아코디언 파 뒷8분. 트럼펫 주제 → 알토 색소폰 한 옥타브 아래'),
    dict(key=('autumn', 2), sid='vs-autumn2-fable', title='Autumn II Fable', genre='sacred minimal drone (choir, pipe organ)',
         genre_reason='3/4 Adagio molto, 거의 화음뿐인 "잠든 취객": 합창 지속화음과 파이프오르간 드론 위에 잉글리시 호른이 violin1 의 긴 음을 노래',
         meter=(3, 4), bpm=40, bars=40, form=(4, 4, 4), map='3/4', stretch=0.5, theme_part='violin1', theme_window=None, grid=PPQ, antic=(PPQ, 2 * PPQ),
         sync=S2V2, swing=0, tonic='D', mode=MINOR, sf=-1, minor=True,
         tracks=[('Choir', 0, 52, 'Church Choir'), ('Organ', 1, 20, ('Celesta', 'Principal + Mixture')), ('Theme', 2, 69, 'English Horn'),
                 ('Theme2', 3, 52, 'Church Choir'), ('Bells', 4, 14, None)],
         chords=[('D', 'm', 1), ('Bb', 'maj', 1), ('G', 'm', 1), ('A', 'sus', 1), ('D', 'm', 1), ('D', 'maj', 1)],
         passes_a=[(6, 'Theme', -12), (6, 'Theme', -12)], passes_a2=[(6, 'Theme2', 0)], theme_v=((56, 78), (54, 74)),
         parts=dict(Choir=dict(kind='pad', base=57, vel=(60, 5), band=(50, 70)),
                    Organ=dict(kind='drone', pitches=(38, 45), vel=(58, 4), band=(50, 66)),
                    Bells=dict(kind='bells', every=4, base=74, vel=(54, 6), band=(44, 64)),
                    Theme=dict(kind='theme'), Theme2=dict(kind='theme')),
         intro={'Organ': 1, 'Choir': 1, 'Bells': 1}, brk={'Organ', 'Bells'}, outro_keep=['Organ', 'Choir', 'Bells'], outro_last={'Organ'},
         motif=[(0, 3, 2), (3, 2, 1), (5, 1, 0)], motif_root=74,
         rhythm_ops=['음가 ×½ (11마디 → 6마디, 실효 템포 ×1.51)', '다운비트 8분 지연·2·3박 당김(2직·2변)', '템포 53→40', '주제는 violin1 긴 음 13개'],
         notes='D 페달 오르간 드론, 합창 Dm–B♭–Gm–Asus–Dm–D(피카르디) 6마디 루프, 4마디마다 종. 잉글리시 호른 주제(한 옥타브 아래) 두 번 → 합창 상성부 재제시'),
    dict(key=('autumn', 3), sid='vs-autumn3-fable', title='Autumn III Fable', genre='New Orleans brass band (second line)',
         genre_reason='3/8 사냥 호른 콜을 트럼펫·트롬본 콜-앤-리스폰스로, 스네어 세컨드 라인 셔플 위에; 3/8 두 마디를 4/4 한 마디로',
         meter=(4, 4), bpm=96, bars=72, form=(8, 8, 8), map='3/8→4/4', theme_part='solo', theme_window=None, grid=E, antic=(PPQ, 3 * PPQ),
         sync=S4V4, swing=80, tonic='F', mode=MAJOR, sf=-1, minor=False,
         tracks=[('Drums', 9, 0, None), ('Tuba', 0, 58, 'Tuba'), ('Trombone', 1, 57, None), ('Sax', 2, 65, None), ('Theme', 3, 56, None), ('Theme2', 4, 57, None)],
         chords=[('F', '6', 2), ('Bb', 'maj', 1), ('C', '7', 1)],
         passes_a=[(12, 'Theme', 0), (12, 'Theme', 0)], passes_a2=[(12, 'Theme2', -12)], theme_v=((72, 94), (66, 88)),
         parts=dict(Drums=dict(kind='drums', cells=[[(0, KICK, 104), (1.5, KICK, 92), (2.5, KICK, 96), (1, SNARE, 96), (2.5, SNARE, 60), (3, SNARE, 96), (3.5, SNARE, 58)] + [(k / 2, RIDE, 62 if k % 2 == 0 else 50) for k in range(8)],
                                                       [(0, KICK, 104), (2.5, KICK, 96), (3.5, KICK, 90), (1, SNARE, 96), (1.75, SNARE, 56), (3, SNARE, 96), (3.75, SNARE, 60)] + [(k / 2, RIDE, 62 if k % 2 == 0 else 50) for k in range(8)]],
                               every4=[(3.5, CRASH, 70)], hum=(10, 6), band=(40, 112)),
                    Tuba=dict(kind='bass', cell=[(0, 0.9, 0), (2, 0.9, 7), (3.5, 0.4, -1)], lo=29, hi=48, vel=(88, 8), band=(72, 104)),
                    Trombone=dict(kind='riff', notes=[(2.5, 0.5, 0), (3, 0.5, 2), (3.5, 0.5, 3)], base=53, vel=(78, 8), band=(62, 94), bars=(1,)),
                    Sax=dict(kind='comp', hits=[(0, 1.5), (2, 1.5)], base=60, vel=(64, 7), band=(52, 78), cc64=False),
                    Theme=dict(kind='theme'), Theme2=dict(kind='theme')),
         intro={'Drums': 1, 'Tuba': 3, 'Trombone': 5, 'Sax': 5}, brk={'Drums', 'Tuba'}, outro_keep=['Drums', 'Tuba', 'Trombone', 'Sax'], outro_last={'Drums', 'Tuba'},
         motif=[(0, 0.5, 4), (0.5, 0.5, 4), (1, 1, 2), (2.5, 0.5, 2), (3, 1, 0), (4, 0.5, 4), (4.5, 0.5, 5), (5, 1, 4), (6, 2, 2)], motif_root=77,
         rhythm_ops=['3/8 두 마디→4/4 한 마디(세 8분 + 연장)', '16분·32분 꾸밈 흡수(8분 그리드 — 스윙과 16분이 겹치지 않게)', '2·4박 당김(4직·4변)', '8분 셔플 스윙 80틱', '8분음 속도 +20%'],
         notes='F6–F6–B♭–C7 루프(주제의 A 음을 받도록 IV 는 장3화음), 세컨드 라인 스네어, 튜바 2비트. 트럼펫 주제, 트롬본 응답 리프(홀수 마디 뒤 두 박). 트롬본 한 옥타브 아래 재제시'),
    dict(key=('winter', 1), sid='vs-winter1-fable', title='Winter I Fable', genre='tango nuevo',
         genre_reason='4/4 Fm "떨림·발 구르기"를 스타카토 피아노 마르카토, 아코디언(반도네온 대용), 떨리는 바이올린의 탱고 긴장으로',
         meter=(4, 4), bpm=118, bars=88, form=(8, 8, 8), map='4/4', theme_part='solo', theme_window=(4, 12), grid=PPQ, antic=(PPQ, 3 * PPQ),
         sync=S4V4, swing=0, tonic='F', mode=MINOR, sf=-4, minor=True,
         tracks=[('Piano', 0, 0, None), ('Bass', 1, 32, None), ('Accordion', 2, 21, 'Tango Accordion'), ('Theme', 3, 40, ('Violins 1', 'Violin (Arco)')), ('Theme2', 4, 21, 'Tango Accordion')],
         chords=[('F', 'm', 2), ('Db', 'maj7', 2), ('F', 'm', 2), ('Bb', 'm7', 1), ('C', '7', 1), ('F', 'm', 1)],
         passes_a=[(9, 'Theme', 0), (9, 'Theme', 0), (9, 'Theme', 0)], passes_a2=[(9, 'Theme2', 0), (9, 'Theme2', 0)], theme_v=((64, 86), (62, 84)),
         parts=dict(Piano=dict(kind='comp', hits=[(0, 0.4), (1.5, 0.4), (3, 0.4), (3.5, 0.3)], base=53, vel=(84, 8), band=(68, 100), cc64=False),
                    Bass=dict(kind='bass', cell=[(0, 1.4, 0), (1.5, 1.4, 7), (3, 0.9, 0)], lo=28, hi=50, vel=(82, 8), band=(68, 96)),
                    Accordion=dict(kind='comp', hits=[(0, 1.4), (2, 0.9), (3.5, 0.4)], base=60, vel=(70, 8), band=(56, 86), cc64=False),
                    Theme=dict(kind='theme'), Theme2=dict(kind='theme')),
         intro={'Piano': 1, 'Bass': 1, 'Accordion': 5}, brk={'Piano', 'Bass'}, outro_keep=['Piano', 'Bass', 'Accordion'], outro_last={'Piano'},
         motif=[(0, 0.25, 0), (0.25, 0.25, 0), (0.5, 0.25, 0), (0.75, 0.25, 0), (1, 0.5, 0), (1.5, 0.5, 2), (2, 1, 0), (3, 1, -1), (4, 0.25, 2), (4.25, 0.25, 2), (4.5, 0.5, 2), (5, 1, 0), (6, 2, 1)], motif_root=65,
         rhythm_ops=['주제 창 4–12 (solo 진입부)', '8분·32분 솎기(4분 골격 — 96음 → 36음, 9마디 전부 변함; 마르카토 탱고 프레이징)', '2·4박 당김(4직·4변)', '템포 140→118 (−16%)'],
         notes='9마디 탱고 진행 Fm×2–D♭maj7×2–Fm×2–B♭m7–C7–Fm(9마디 패스에 맞춤), 피아노 3-3-2 마르카토, 아코디언 지속+스탭. 떨림은 같은 음 16분 자작 모티프. 솔로 바이올린 주제 → 아코디언 재제시'),
    dict(key=('winter', 2), sid='vs-winter2-fable', title='Winter II Fable', genre='bossa nova',
         genre_reason='4/4 Largo 의 피치카토 빗방울 위 선율을 나일론 컴핑(빗방울)·브러시 드럼·플루트의 난롯가 보사노바로',
         meter=(4, 4), bpm=72, bars=56, form=(8, 8, 8), map='4/4', theme_part='solo', theme_window=None, grid=E, antic=(PPQ, 3 * PPQ),
         sync=S4V4, swing=0, tonic='Eb', mode=MAJOR, sf=-3, minor=False,
         tracks=[('Drums', 9, 0, None), ('Bass', 0, 32, None), ('Guitar', 1, 24, None), ('Vibes', 2, 11, None), ('Theme', 3, 73, 'Flute Solo'), ('Theme2', 4, 11, None)],
         chords=[('Eb', 'maj7', 1), ('G', 'm7', 1), ('F', 'm7', 1), ('Bb', '9', 1)],
         passes_a=[(8, 'Theme', 0), (8, 'Theme', 0)], passes_a2=[(8, 'Theme2', -12)], theme_v=((58, 80), (56, 76)),
         parts=dict(Drums=dict(kind='drums', cells=[[(0, KICK, 78), (2.5, KICK, 72), (0, RIM, 70), (1.5, RIM, 64), (3, RIM, 70)] + [(k / 2, HAT, 44 if k % 2 == 0 else 36) for k in range(8)],
                                                       [(0, KICK, 78), (2.5, KICK, 72), (0.5, RIM, 64), (2, RIM, 70), (3.5, RIM, 64)] + [(k / 2, HAT, 44 if k % 2 == 0 else 36) for k in range(8)]],
                               every4=[], hum=(10, 6), band=(30, 90)),
                    Bass=dict(kind='bass', cell=[(0, 1.4, 0), (1.5, 0.4, 7), (2, 1.4, 0), (3.5, 0.4, 7)], lo=28, hi=48, vel=(70, 8), band=(56, 84)),
                    Guitar=dict(kind='comp', hits=[(0, 0.7), (1.5, 0.7), (2.5, 0.4), (3, 0.9)], base=52, vel=(64, 8), band=(50, 80), cc64=False),
                    Vibes=dict(kind='top', hits=[(1, 1.5), (3.5, 1.0)], base=64, vel=(54, 6), band=(42, 66)),
                    Theme=dict(kind='theme'), Theme2=dict(kind='theme')),
         intro={'Guitar': 1, 'Drums': 3, 'Bass': 5, 'Vibes': 5}, brk={'Drums', 'Bass', 'Guitar'}, outro_keep=['Drums', 'Bass', 'Guitar', 'Vibes'], outro_last={'Guitar'},
         motif=[(0, 1, 2), (1, 0.5, 4), (1.5, 0.5, 2), (2, 2, 0), (4, 1, -1), (5, 1, 0), (6, 2, 2)], motif_root=75,
         rhythm_ops=['16분 꾸밈 솎기(8분 골격)', '2·4박 당김(4직·4변)', '템포 46→72 (+57%)'],
         notes='E♭maj7–Gm7–Fm7–B♭9, 림 보사 클라베, 나일론 신코페이션 컴핑, 비브라폰 탑노트. 플루트 주제 → 비브라폰 한 옥타브 아래'),
    dict(key=('winter', 3), sid='vs-winter3-fable', title='Winter III Fable', genre='synthwave',
         genre_reason='3/8 Fm "얼음 위를 걷다 미끄러지고 바람이 싸운다": 아르페지오 신스와 스윕 패드가 바람, 드럼 신스가 발걸음; 3/8 두 마디를 4/4 한 마디로',
         meter=(4, 4), bpm=118, bars=88, form=(8, 8, 8), map='3/8→4/4', theme_part='solo', theme_window=None, grid=E, antic=(PPQ, 3 * PPQ),
         sync=S4V4, swing=0, tonic='F', mode=MINOR, sf=-4, minor=True,
         tracks=[('Drums', 9, 25, None), ('Bass', 0, 38, None), ('Arp', 1, 80, None), ('Pad', 2, 94, None), ('Theme', 3, 81, None), ('Theme2', 4, 80, None)],
         chords=[('F', 'mM7', 1), ('C', '7', 1)],
         passes_a=[(12, 'Theme', 0), (12, 'Theme', 0)], passes_a2=[(12, 'Theme2', 0), (8, 'Theme2', 0)], theme_v=((72, 92), (68, 88)),
         parts=dict(Drums=dict(kind='drums', cells=[[(0, KICK, 104), (2, KICK, 100), (1, SNARE, 100), (3, SNARE, 100)] + [(k / 2, HAT, 60 if k % 2 == 0 else 48) for k in range(8)],
                                                       [(0, KICK, 104), (2, KICK, 100), (2.75, KICK, 88), (1, SNARE, 100), (3, SNARE, 100)] + [(k / 2, HAT, 60 if k % 2 == 0 else 48) for k in range(8)]],
                               every4=[(3.5, OPEN_HAT, 68)], hum=(6, 6), band=(40, 112)),
                    Bass=dict(kind='pulse', lo=28, hi=48, vel=(90, 6), band=(78, 102)),
                    Arp=dict(kind='arp', step=S, pattern=(0, 1, 2, 3, 2, 1, 0, 3, 1, 2, 3, 2, 0, 1, 2, 1), base=60, vel=(68, 6), band=(56, 80)),
                    Pad=dict(kind='pad', base=55, vel=(58, 5), band=(48, 68)),
                    Theme=dict(kind='theme'), Theme2=dict(kind='theme')),
         intro={'Pad': 1, 'Arp': 1, 'Bass': 5, 'Drums': 5}, brk={'Pad', 'Arp'}, outro_keep=['Drums', 'Bass', 'Arp', 'Pad'], outro_last={'Pad', 'Arp'},
         motif=[(0, 0.5, 0), (0.5, 0.5, 2), (1, 0.5, 4), (1.5, 0.5, 7), (2, 1, 4), (3, 1, 2), (4, 0.5, 0), (4.5, 0.5, 2), (5, 1, 0), (6, 2, -3)], motif_root=65,
         rhythm_ops=['3/8 두 마디→4/4 한 마디(세 8분 + 연장)', '16분 아르페지오 솎기(8분)', '2·4박 당김(4직·4변)', '8분음 속도 +57%'],
         notes='Fm(maj7)–C7 두 코드 루프(주제의 E♮ 를 받음), 8분 옥타브 펄스 베이스, 16분 아르페지오, 스윕 패드. 소우 리드 주제 → 스퀘어 재제시'),
]


# ---------------------------------------------------------------- geometry
def bar_ticks(s):
    num, den = s['meter']
    return num * (PPQ * 4 // den)


def form(s):
    """Section starts (1-based bars) and markers: intro / A / break / A2 / outro with lengths from s['form']."""
    n, (fi, fb, fo) = s['bars'], s['form']
    half = (n - fi - fb - fo) // 2
    a, brk, a2, outro = fi + 1, fi + 1 + half, fi + 1 + half + fb, n - fo + 1
    return dict(a=a, brk=brk, a2=a2, outro=outro, end=n + 1,
                markers=[(1, 'intro'), (a, 'A'), (brk, 'break'), (a2, 'A2'), (outro, 'outro')])


def section(fm, bar):
    if bar < fm['a']:
        return 'intro'
    if bar < fm['brk']:
        return 'A'
    if bar < fm['a2']:
        return 'break'
    if bar < fm['outro']:
        return 'A2'
    return 'outro'


# ---------------------------------------------------------------- theme pipeline
def extract(s):
    key, m = s['key'], MOVEMENTS[s['key']]
    a, b = s['theme_window'] or m['theme']
    t0, t1 = bar_tick(key, a), bar_tick(key, b + 1)
    lo = 0 if a == 1 else t0
    notes = sorted((t - t0, d, p) for t, d, p in m['parts'][s['theme_part']] if lo <= t < t1)
    mono = {}
    for t, d, p in notes:
        if t not in mono or p > mono[t][1]:
            mono[t] = (d, p)
    return [(t, d, p) for t, (d, p) in sorted(mono.items())], t1 - t0


def thin(notes, grid):
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
    """(map_tick, map_end). Identity maps keep ticks (the bar count changes); '3+1' / stretch maps pad each source bar
    to the target bar and extend notes that end on a source bar line to the target bar line."""
    if MAPS[kind] is None:
        return (lambda t: t), (lambda e: e)
    sb, tb = MAPS[kind]

    def mt(t):
        return (t // sb) * tb + t % sb

    def me(e):
        return (e // sb) * tb if e % sb == 0 else mt(e)
    return mt, me


def vary(notes, pattern, phase, TB, antic):
    """Per target bar flagged in `pattern`: anticipate onsets at `antic` offsets by an eighth; failing that, delay a
    downbeat note of at least a beat; failing that, push the whole bar late by an eighth (notes that would cross the bar
    line are dropped, never overlapped onto the next downbeat)."""
    notes = sorted(notes)
    by_bar = {}
    for i, (t, d, p) in enumerate(notes):
        by_bar.setdefault(t // TB, []).append(i)
    out, drop = list(notes), set()
    for bar, idxs in by_bar.items():
        if bar < 0 or not pattern[(bar + phase) % len(pattern)]:
            continue
        changed = False
        for i in idxs:
            t, d, p = out[i]
            if t % TB in antic and not (i and out[i - 1][0] >= t - E):
                out[i] = (t - E, d + E, p)
                if i and out[i - 1][0] + out[i - 1][1] > t - E:
                    pt, pd, pp = out[i - 1]
                    out[i - 1] = (pt, t - E - pt, pp)
                changed = True
        if changed:
            continue
        i = idxs[0]
        t, d, p = out[i]
        if t % TB == 0 and d >= PPQ:
            out[i] = (t + E, d - E, p)
            continue
        end = (bar + 1) * TB
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
    TB = bar_ticks(s)
    src, src_len = extract(s)
    src = thin(src, s['grid'])
    mt, me = meter_map(s['map'])
    k = s.get('stretch', 1)
    plain = [(int(mt(t) * k), max(S // 2, int((me(t + d) - mt(t)) * k)), p) for t, d, p in src]
    n_bars = -(-int(me(src_len) * k) // TB)
    half = len(s['sync']) // 2
    return plain, (vary(plain, s['sync'], 0, TB, s['antic']), vary(plain, s['sync'], half, TB, s['antic'])), n_bars


def theme_plan(s, fm, variants):
    """Lay the passes into A and A2; pass k uses variants[k % len]. Returns (events by track name, residual bars, covered 0-based bars)."""
    TB = bar_ticks(s)
    events, covered, residual, k = {}, set(), [], 0
    for start, end, passes in ((fm['a'], fm['brk'], s['passes_a']), (fm['a2'], fm['outro'], s['passes_a2'])):
        bar = start
        for length, track, octave in passes:
            assert bar + length <= end, f'{s["sid"]}: pass of {length} bars does not fit {start}-{end - 1}'
            lim = (bar - 1 + length) * TB
            for t, d, p in variants[k % len(variants)]:
                tt = (bar - 1) * TB + t
                if tt >= lim or tt < 0:
                    continue
                events.setdefault(track, []).append((tt, min(d, lim - tt), p + octave))
                if t < 0:
                    covered.add(bar - 1)
            covered.update(range(bar, bar + length))
            bar += length
            k += 1
        residual += [b for b in range(start, end) if b not in covered]
    return events, residual, {b - 1 for b in covered}


def straight_run(plain, final, covered, TB):
    """Longest run of covered bars whose onset/duration set equals the plain mapping. A bar where the theme only sustains
    (no onset) is original rhythm too and counts; a true rest bar neither counts nor breaks the run."""
    def shape(notes):
        shp = {}
        for t, d, p in notes:
            shp.setdefault(t // TB, set()).add((t % TB, d))
        return shp
    a, b = shape(plain), shape(final)
    sustain = set()
    for t, d, p in plain:
        sustain.update(range(t // TB + 1, (t + d - 1) // TB + 1))
    best = run = 0
    for bar in range(max(list(a) + list(b) + list(sustain)) + 1):
        if bar not in covered:
            run = 0
            continue
        if bar not in a and bar not in b:
            if bar in sustain:
                run += 1
                best = max(best, run)
            continue
        if a.get(bar) == b.get(bar):
            run += 1
            best = max(best, run)
        else:
            run = 0
    return best


def sounding_bars(events, TB):
    bars = set()
    for evs in events.values():
        for t, d, p in evs:
            bars.update(range(t // TB + 1, (t + d - 1) // TB + 2))
    return bars


# ---------------------------------------------------------------- harmony
def voicing(root, qual, base):
    iv, _ = QUAL[qual]
    r = base + (PC[root] - base % 12) % 12
    return [r + i for i in iv]


def chord_at(s, fm, bar):
    loop = [(r, q) for r, q, n in s['chords'] for _ in range(n)]
    if bar < fm['a']:
        return loop[(bar - 1) % len(loop)]
    anchor = fm['a2'] if bar >= fm['a2'] else fm['a']
    return loop[(bar - anchor) % len(loop)]


def root_pitch(root, lo, hi):
    p = lo + (PC[root] - lo % 12) % 12
    return p if p <= hi else p - 12


def fold(p, lo, hi, iv):
    """Fold into [lo, hi]; an octave that would leave the range becomes the fifth, a fifth-below that would leave it the fifth above."""
    if (iv == 12 and p > hi) or (iv == -5 and p < lo):
        p = p - 12 + 7 if iv == 12 else p + 12
    while p < lo:
        p += 12
    while p > hi:
        p -= 12
    return p


def scale_pitch(s, degree, root):
    return root + 12 * (degree // 7) + s['mode'][degree % 7]


# ---------------------------------------------------------------- rendering
def clamp(v, lo, hi):
    return min(hi, max(lo, v))


def layers_at(s, fm, bar):
    """Which parts sound in `bar`: intro entries in order, break set, outro thinning (keep list, then last set)."""
    sec = section(fm, bar)
    all_parts = [name for name, *_ in s['tracks'] if s['parts'][name]['kind'] != 'theme']
    if sec == 'intro':
        return {p for p in all_parts if s['intro'].get(p, 10 ** 9) <= bar}
    if sec == 'break':
        return set(s['brk'])
    if sec == 'outro':
        n_out = fm['end'] - fm['outro']
        if bar >= fm['end'] - max(2, n_out // 2):
            return set(s['outro_last'])
        return set(s['outro_keep'])
    return set(all_parts)


def render_part(s, fm, name, part, bar, t0, TB, chord, out, sw):
    """Emit one bar of an accompaniment part into out[name] as (tick, dur, pitch, vel)."""
    kind = part['kind']
    root, qual = chord
    lo_v, hi_v = part['band']
    beats = TB / PPQ

    def tick(beat):
        t = t0 + int(beat * PPQ)
        return t + (sw if sw and (beat % 1 == 0.5) else 0)

    def vel(base, amt):
        return clamp(hum_v(base, amt), lo_v, hi_v)

    if kind == 'drums':
        cells = part['cells']
        cell = cells[(bar - 1) % len(cells)]
        for beat, note, v in cell:
            if beat >= beats:
                continue
            out[name].append((hum_t(tick(beat), part['hum'][0]), 90 if note not in (OPEN_HAT, CRASH) else 300, note, vel(v, part['hum'][1])))
        if bar % 4 == 0:
            for beat, note, v in part['every4']:
                if v and beat < beats:
                    out[name].append((hum_t(tick(beat), part['hum'][0]), 300, note, vel(v, part['hum'][1])))
    elif kind == 'bass':
        r = root_pitch(root, part['lo'], part['hi'])
        cell = part['cell'] if not part.get('alt') or bar % 2 else part['alt']
        for beat, dur, iv in cell:
            if beat >= beats:
                continue
            out[name].append((hum_t(tick(beat), 6), int(dur * PPQ) - 20, fold(r + iv, part['lo'], part['hi'], iv), vel(*part['vel'])))
    elif kind == 'pulse':
        r = root_pitch(root, part['lo'], part['hi'])
        for k in range(int(beats * 2)):
            p = r if k % 2 == 0 else fold(r + 12, part['lo'], part['hi'], 12)
            out[name].append((hum_t(t0 + k * E, 4), E - 30, p, vel(part['vel'][0] + (4 if k % 2 == 0 else 0), part['vel'][1])))
    elif kind == 'comp':
        voice = voicing(root, qual, part['base'])
        for beat, dur in part['hits']:
            if beat >= beats:
                continue
            start = tick(beat)
            for p in voice:
                out[name].append((hum_t(start, 6), int(dur * PPQ) - 20, p, vel(*part['vel'])))
    elif kind == 'top':
        voice = voicing(root, qual, part['base'])
        for j, (beat, dur) in enumerate(part['hits']):
            if beat >= beats:
                continue
            out[name].append((hum_t(tick(beat), 6), int(dur * PPQ) - 20, voice[(j + bar) % len(voice)] + 12, vel(*part['vel'])))
    elif kind == 'arp':
        voice = voicing(root, qual, part['base'])
        tones = voice + [voice[0] + 12]
        n = TB // part['step']
        for k in range(n):
            idx = part['pattern'][k % len(part['pattern'])]
            t = t0 + k * part['step'] + (sw if sw and part['step'] == E and k % 2 else 0)
            out[name].append((hum_t(t, 6), part['step'] - 25, tones[idx % len(tones)], vel(*part['vel'])))
    elif kind == 'pad':
        voice = voicing(root, qual, part['base'])
        for p in voice:
            out[name].append((t0 + 5, TB - 30, p, vel(*part['vel'])))
    elif kind == 'drone':
        for p in part['pitches']:
            out[name].append((t0 + 5, TB - 20, p, vel(*part['vel'])))
    elif kind == 'bells':
        if bar % part['every'] == 1 or part['every'] == 1:
            r = root_pitch(root, part['base'], part['base'] + 11)
            out[name].append((t0 + 10, TB * 2 - 40, r, vel(*part['vel'])))
    elif kind == 'riff':
        if bar % 2 in part['bars']:
            r = root_pitch(root, part['base'], part['base'] + 11)
            for beat, dur, deg in part['notes']:
                out[name].append((hum_t(tick(beat), 8), int(dur * PPQ) - 20, r + s['mode'][deg % 7] + 12 * (deg // 7), vel(*part['vel'])))
    elif kind == 'thunder':
        pass                                                   # placed per section in render_song
    elif kind == 'riser':
        pass


def render_song(s, fm, events, residual):
    TB, n = bar_ticks(s), s['bars']
    names = [name for name, *_ in s['tracks']]
    out = {name: [] for name in names}
    sw = s['swing']
    for bar in range(1, fm['end']):
        t0 = (bar - 1) * TB
        active = layers_at(s, fm, bar)
        chord = chord_at(s, fm, bar)
        for name in [nm for nm in names if nm in active]:        # track order: the rng stream must not depend on set order
            render_part(s, fm, name, s['parts'][name], bar, t0, TB, chord, out, sw)
    # section-bound parts
    for name, part in s['parts'].items():
        if part['kind'] == 'thunder':                          # a roll (soft then loud) in the two bars before A, A2 and at the last outro bar
            for b in (fm['a'] - 2, fm['a2'] - 2, fm['end'] - 2):
                t0 = (b - 1) * TB
                out[name].append((t0, TB - 40, part['pitch'], clamp(hum_v(part['vel'][0] - 22, 4), *part['band'])))
                out[name].append((t0 + TB, TB - 60, part['pitch'] + 5, clamp(hum_v(part['vel'][0], part['vel'][1]), *part['band'])))
        if part['kind'] == 'riser':                            # two bars before the A and A2 drops
            for b in (fm['a'] - 2, fm['a2'] - 2):
                out[name].append(((b - 1) * TB, 2 * TB - 60, part['pitch'], clamp(hum_v(*part['vel']), *part['band'])))
    # theme passes + own motif
    for k, (track, evs) in enumerate(events.items()):
        lo, hi = s['theme_v'][0 if track == 'Theme' else 1]
        add_theme(out, track, evs, lo, hi, 8 if s['swing'] == 0 else 6)
    motif = motif_events(s, residual + [b for b in range(max(1, fm['a'] - 4), fm['a'])], TB)
    if sw:
        motif = swing(motif, sw)
    lo, hi = s['theme_v'][0]
    add_theme(out, 'Theme', motif, lo - 4, hi - 6, 8)
    return out


def add_theme(out, track, events, lo, hi, amt_t):
    base = (lo + hi) // 2
    for t, d, p in events:
        v = base + (6 if t % PPQ == 0 else 0)
        out[track].append((hum_t(t, amt_t), max(S // 2, d - 15), p, clamp(hum_v(v, 8), lo, hi)))


def motif_events(s, bars, TB):
    """The own two-bar cell (beats in quarters, scale degrees) laid on `bars`; a cell position past the bar is skipped."""
    out, beats = [], TB / PPQ
    for b in bars:
        cell = (b - 1) % 2
        for beat, dur, deg in s['motif']:
            if int(beat // beats) != cell:
                continue
            t = (b - 1) * TB + int((beat - beats * cell) * PPQ)
            out.append((t, int(dur * PPQ) - 20, scale_pitch(s, deg, s['motif_root'])))
    return out


def dedupe(notes):
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


def mono_clip(notes):
    notes = sorted(notes)
    for i in range(len(notes) - 1):
        t, d, p, v = notes[i]
        nxt = notes[i + 1][0]
        if t + d > nxt:
            notes[i] = (t, max(10, nxt - t - 1), p, v)
    return notes


def compose(sid):
    """Returns nt (by track index), cc, pcs, tracks [(name, ch)], patches {1-based track: spec}, stats."""
    s = next((x for x in SKETCHES if x['sid'] == sid), None)
    assert s, f'unknown sid {sid}'
    seed(261109 + sum(ord(c) for c in sid))
    fm, TB = form(s), bar_ticks(s)
    plain, variants, n_theme = theme_target(s)
    events, residual, covered = theme_plan(s, fm, variants)
    plain_events, _, _ = theme_plan(s, fm, (plain,))
    flat = lambda ev: [n for evs in ev.values() for n in evs]
    straight = straight_run(flat(plain_events), flat(events), covered, TB)
    theme_bars = sounding_bars(events, TB)
    if s['swing']:
        events = {k: swing(v, s['swing']) for k, v in events.items()}
    out = render_song(s, fm, events, residual)
    end = s['bars'] * TB
    names = [name for name, *_ in s['tracks']]
    nt = {}
    for i, name in enumerate(names):
        notes = dedupe([(t, min(d, end - t), p, v) for t, d, p, v in out[name] if 0 <= t < end])
        nt[i] = mono_clip(notes) if name.startswith('Theme') else notes
    cc = {}
    for i, name in enumerate(names):
        if s['parts'][name].get('cc64'):
            cc[i] = [e for bar in range(1, fm['end']) for e in (((bar - 1) * TB, 64, 127), (bar * TB - 12, 64, 0))]
    pcs = {i: pc for i, (_, _, pc, _) in enumerate(s['tracks'])}
    tracks = [(name, ch) for name, ch, _, _ in s['tracks']]
    patches = {i + 1: spec for i, (_, _, _, spec) in enumerate(s['tracks']) if spec}
    stats = dict(straight=straight, theme_bars=len(theme_bars), n_theme=n_theme, ratio=100 * len(theme_bars) / s['bars'], fm=fm, TB=TB)
    return nt, cc, pcs, tracks, patches, stats


# ---------------------------------------------------------------- SMF with copyright
def with_copyright(smf, text):
    """Insert a copyright meta event (FF 02) at tick 0 of the FIRST INSTRUMENT track (MTrk #2). In the conductor track
    Logic 12.4 turns the event into an extra empty 'Studio Grand' track 1 (measured 2026-11-09), which shifts the track
    numbers that produce(patches=...) addresses; inside an instrument track it leaves the track list unchanged."""
    assert smf[:4] == b'MThd'
    pos = 14
    assert smf[pos:pos + 4] == b'MTrk'
    pos += 8 + struct.unpack('>I', smf[pos + 4:pos + 8])[0]           # skip the conductor track
    assert smf[pos:pos + 4] == b'MTrk'
    ln = struct.unpack('>I', smf[pos + 4:pos + 8])[0]
    data = smf[pos + 8:pos + 8 + ln]
    payload = text.encode()
    assert len(payload) < 128, 'pipeline.parse_smf reads one-byte meta lengths'
    data = b'\x00\xff\x02' + bytes(varlen(len(payload))) + payload + data
    return smf[:pos] + b'MTrk' + struct.pack('>I', len(data)) + data + smf[pos + 8 + ln:]


def build(sid):
    nt, cc, pcs, tracks, patches, stats = compose(sid)
    s = next(x for x in SKETCHES if x['sid'] == sid)
    report = check(s, nt, cc, stats, tracks)
    smf = build_smf(s['title'], s['bpm'], s['sf'], s['minor'], s['bars'], tracks, pcs, nt, cc, stats['fm']['markers'], timesig=s['meter'])
    return with_copyright(smf, COPYRIGHT), report, patches


# ---------------------------------------------------------------- checks
def span(vals):
    return f'{min(vals)}..{max(vals)}' if vals else '-'


def tempo_ratio(s):
    """Effective tempo vs the original: ticks are preserved by every map (identity, '3+1', stretch-to-bar) so the quarter
    rate ratio is bpm/src_bpm, divided by the duration stretch factor."""
    return s['bpm'] / MOVEMENTS[s['key']]['tempo_bpm'] / s.get('stretch', 1)


def check(s, nt, cc, stats, tracks):
    sid, n, TB, fm = s['sid'], s['bars'], stats['TB'], stats['fm']
    assert stats['straight'] <= 4, f'{sid}: {stats["straight"]} consecutive original-rhythm bars'
    assert 40 <= stats['ratio'] <= 60, f'{sid}: theme ratio {stats["ratio"]:.1f}%'
    ratio = tempo_ratio(s)
    assert abs(ratio - 1) >= 0.15 or s.get('stretch', 1) in (2, 0.5), f'{sid}: effective tempo ×{ratio:.3f} is within ±15% and no half/double time'
    last = max(t + d for tr in nt.values() for t, d, _, _ in tr)
    assert last <= n * TB, f'{sid}: last note end {last} > {n * TB}'
    names = [name for name, _ in tracks]
    # per-track velocity bands and overlaps
    for i, name in enumerate(names):
        part = s['parts'][name]
        if part['kind'] != 'theme':
            lo, hi = part['band']
            assert all(lo <= v <= hi for *_, v in nt[i]), f'{sid}: {name} velocity outside {lo}..{hi}'
        ends = {}
        for t, d, p, _ in sorted(nt[i]):
            assert ends.get(p, -1) <= t, f'{sid}: overlap pitch {p} on {name} at {t}'
            ends[p] = t + d
        if name.startswith('Theme'):
            prev = -1
            for t, d, p, _ in sorted(nt[i]):
                assert t >= prev, f'{sid}: polyphony on {name} at {t}'
                prev = max(prev, t + d)
    # density: bars with exactly one sounding layer, outside intro/outro, at most 2 in a row
    sounding = [set() for _ in range(n + 2)]
    for i, name in enumerate(names):
        for t, d, p, _ in nt[i]:
            for b in range(t // TB + 1, (t + d - 1) // TB + 2):
                if b <= n:
                    sounding[b].add(name)
    run = worst = 0
    for b in range(fm['a'], fm['outro']):
        run = run + 1 if len(sounding[b]) == 1 else 0
        worst = max(worst, run)
    assert worst <= 2, f'{sid}: {worst} consecutive single-layer bars inside A/break/A2'
    empty = [b for b in range(1, n + 1) if not sounding[b]]
    assert not empty, f'{sid}: silent bars {empty[:5]}'
    # notes per bar per section per track; bass notes per bar
    secs = ('intro', 'A', 'break', 'A2', 'outro')
    per = {}
    for i, name in enumerate(names):
        counts = {sec: 0 for sec in secs}
        for t, *_ in nt[i]:
            counts[section(fm, t // TB + 1)] += 1
        lens = {'intro': fm['a'] - 1, 'A': fm['brk'] - fm['a'], 'break': fm['a2'] - fm['brk'], 'A2': fm['outro'] - fm['a2'], 'outro': fm['end'] - fm['outro']}
        per[name] = '/'.join(f'{counts[sec] / lens[sec]:.1f}' for sec in secs)
    bass_name = next((nm for nm in names if s['parts'][nm]['kind'] in ('bass', 'pulse')), None)
    vels = ' '.join(f'{name} {span([v for *_, v in nt[i]])}' for i, name in enumerate(names))
    npb = ' '.join(f'{name} {per[name]}' for name in names)
    # long theme notes (>= a beat) outside the chord's scale — reported, not asserted (chromatic passing tones in the source)
    clashes = total = 0
    for i, name in enumerate(names):
        if not name.startswith('Theme'):
            continue
        for t, d, p, _ in nt[i]:
            if d < PPQ - 40:
                continue
            total += 1
            root, qual = chord_at(s, fm, t // TB + 1)
            if (p - PC[root]) % 12 not in QUAL[qual][1]:
                clashes += 1
    m = MOVEMENTS[s['key']]
    return (f'  straight_max={stats["straight"]} theme={stats["ratio"]:.0f}% ({stats["theme_bars"]}/{n} bars, pass={stats["n_theme"]}) '
            f'tempo {m["tempo_bpm"]}→{s["bpm"]} ×{ratio:.2f}{" ×" + str(s["stretch"]) + " 음가" if s.get("stretch", 1) != 1 else ""} meter {s["meter"][0]}/{s["meter"][1]} '
            f'| single-layer run {worst} | clashes {clashes}/{total} | vel: {vels} | '
            f'notes/bar intro/A/break/A2/outro: {npb} | bass/bar {per.get(bass_name, "-")} | last_bar={last / TB:.1f}')


def check_prompts():
    import re
    path = os.path.join(os.path.dirname(SK_DIR), 'suno', 'vivaldi_fable_v2.md')
    blocks = re.findall(r'^## (vs-[a-z0-9]+-fable)-v2\n\*\*Style\*\*\n`([^`]+)`\n\n\*\*Description\*\*\n```\n(.*?)\n```',
                        open(path, encoding='utf-8').read(), re.M | re.S)
    sids = [s['sid'] for s in SKETCHES]
    assert [b[0] for b in blocks] == sids, f'blocks {[b[0] for b in blocks]} != {sids}'
    for sid, style, desc in blocks:
        assert len(style) <= 300 and len(desc) <= 1000, f'{sid}: style {len(style)} desc {len(desc)}'
        assert 'Four Seasons' in desc and 'Vivaldi' not in style and 'Seasons' not in style, sid
        print(f'| {sid} | {len(style)} | {len(desc)} |')


if __name__ == '__main__':
    args = sys.argv[1:]
    if args == ['--prompts']:
        check_prompts()
        sys.exit()
    check_only = '--check' in args
    want = [a for a in args if not a.startswith('--')] or [s['sid'] for s in SKETCHES]
    print(f'model {MODEL}')
    bad = 0
    for sid in want:
        smf, report, patches = build(sid)
        path = os.path.join(SK_DIR, f'{sid}-{VER}.mid')
        if check_only:
            same = os.path.exists(path) and open(path, 'rb').read() == smf
            print(f'{os.path.basename(path)} {"OK" if same else "DIFF"} {len(smf)}B')
            bad += not same
        else:
            print(write_smf(path, smf), f'patches={patches}')
        print(report)
    sys.exit(1 if bad else 0)
