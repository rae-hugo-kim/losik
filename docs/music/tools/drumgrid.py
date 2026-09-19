"""사용자가 텍스트 격자로 그린 드럼 패턴을 SMF 로 (2026-09-14). 92 BPM 4마디 × 2회 반복.

  original — 사용자 원본 그대로 (휴머나이즈 없음: 격자 자체를 듣기 위해)
  revised  — 09-13 지적 5개만 반영, 그 외 동일:
    1. 마디 4 필인 구간(1&~) 16분 햇 제거 → 4분 풋햇(1·2·3·4)만
    2. 마디 3 단독 클랩 → 같은 자리 고스트 스네어(vel 40)
    3. 마디 3 라이드 = 벨(GM 53) 로 확정
    4. 마디 4 크래시 4& 에 킥 동반(임팩트)
    5. 마디 4 로우탐 3a → 4e (킥 3a 와 저역 겹침 해소)

격자 표기: 16분 16칸, 'x' = 히트, 'O'/'X' 도 히트. 행 라벨 → GM 노트.
"""
import os
import sys

from pipeline import PPQ, S, SK_DIR, bt, build_smf, write_smf

BPM = 92
GM = {'Kick': 36, 'Snare': 38, 'HH': 42, 'HHfoot': 44, 'Ride': 51, 'RideBell': 53, 'Crash': 49,
      'Tom hi': 50, 'Tom mid': 47, 'Tom lo': 45, 'Clap': 39, 'Ghost': 38}
VEL = {'Kick': 112, 'Snare': 110, 'HH': 78, 'HHfoot': 70, 'Ride': 84, 'RideBell': 96, 'Crash': 118,
       'Tom hi': 100, 'Tom mid': 104, 'Tom lo': 108, 'Clap': 96, 'Ghost': 40}
HH_ACCENT = [88, 60, 74, 60]   # 16분 햇 강약 (1 e & a) — 원본에도 적용: 전부 같은 세기면 메트로놈처럼 들림

ORIGINAL = [
    {'Kick':  'x.....x...x.....', 'Snare': '....x.......x...', 'HH': 'xxxxxxxxxxxxxxxx'},
    {'Kick':  'x.....x...x.....', 'Snare': '....x.......x...', 'HH': 'xxxxxxxxxxxxxxxx'},
    {'Kick':  'x.....x...x.....', 'Snare': '....x.......x...', 'HH': '....xxxx....xxxx',
     'Ride':  'O.OO....O.OO....', 'Clap': '.x.......x......'},
    {'Kick':  'x.....x...xx....', 'Snare': '..xxxx..........', 'HH': 'xxxxxxxxxxxxxxxx',
     'Crash': '..............X.', 'Tom hi': '........xx......', 'Tom mid': '..........x.....', 'Tom lo': '...........xx...'},
]

REVISED = [
    ORIGINAL[0],
    ORIGINAL[1],
    {'Kick':  'x.....x...x.....', 'Snare': '....x.......x...', 'HH': '....xxxx....xxxx',
     'RideBell': 'O.OO....O.OO....', 'Ghost': '.x.......x......'},
    {'Kick':  'x.....x...xx..x.', 'Snare': '..xxxx..........', 'HH': 'x...............', 'HHfoot': '....x...x...x...',
     'Crash': '..............X.', 'Tom hi': '........xx......', 'Tom mid': '..........x.....', 'Tom lo': '...........x.x..'},
]

# 크래시 위치 변주 (09-18). 원인 확정: HTML 크래시는 고역만 남은 0.3~0.5초 신스라 4& 에서 '당김'으로 들리지만,
# SoCal 크래시는 전대역 2~3초 감쇠라 다음 1박을 덮어 '반박 빠른 1박'으로 들림. 수정본(REVISED) 기준으로 4마디만 다르다.
#   A downbeat  : 4& 크래시·킥 제거, 다음 마디 1박에 크래시 (전통)
#   B splash    : 4& 스플래시(GM 55, 고역만·짧음 = HTML 크래시의 어쿠스틱 번역) + 킥, 다음 1박에 크래시
#   C soft      : 4& 크래시 vel 84 + 킥, 다음 1박 크래시 없음 (초크는 GM note-off 로 불가 — 세기만 낮춘 당김)
# 세 변주 모두 마지막에 해소 마디(bar 1 패턴) 1개를 붙인다 — 루프 툴처럼 크래시가 1박으로 돌아가도록.
GM['Splash'] = 55
VEL['Splash'] = 100
VEL['CrashSoft'] = 84
GM['CrashSoft'] = 49
_BAR4_REV = REVISED[3]
VARIANTS = {
    'A-downbeat': ([REVISED[0], REVISED[1], REVISED[2],
                    {**_BAR4_REV, 'Kick': 'x.....x...xx....', 'Crash': '................'}], True),
    'B-splash':   ([REVISED[0], REVISED[1], REVISED[2],
                    {**_BAR4_REV, 'Crash': '................', 'Splash': '..............X.'}], True),
    'C-soft':     ([REVISED[0], REVISED[1], REVISED[2],
                    {**_BAR4_REV, 'Crash': '................', 'CrashSoft': '..............X.'}], False),
}
# 클랩 변주 (09-18, B-splash 기준). §2-5 "클랩 단독 노출 금지"는 신스웨이브(08-25)에서 나온 규칙 — 92 BPM 록 그루브·SoCal 킷에서 재판정.
#   B-clap       : 3마디 1e·3e 클랩 단독 vel 96 (원본 그대로)
#   B-clap-layer : 같은 자리 클랩 + 고스트 스네어 겹침
_BAR3_REV = REVISED[2]
_BAR4_B = VARIANTS['B-splash'][0][3]
VARIANTS['B-clap'] = ([REVISED[0], REVISED[1], {**_BAR3_REV, 'Ghost': '................', 'Clap': '.x.......x......'}, _BAR4_B], True)
VARIANTS['B-clap-layer'] = ([REVISED[0], REVISED[1], {**_BAR3_REV, 'Clap': '.x.......x......'}, _BAR4_B], True)


def render(name, bars, reps=2, downbeat_crash=False, tail=False):
    nt = {0: []}
    seq = [bars[i % len(bars)] for i in range(len(bars) * reps + (1 if tail else 0))]
    for i, bar in enumerate(seq):
        b = i + 1
        for row, grid in bar.items():
            assert len(grid) == 16, (name, b, row)
            for pos, ch in enumerate(grid):
                if ch == '.':
                    continue
                vel = HH_ACCENT[pos % 4] if row == 'HH' else VEL[row]
                nt[0].append((bt(b) + pos * S, 110, GM[row], vel))
        if downbeat_crash and i > 0 and i % len(bars) == 0:     # 4마디 셀 끝을 받는 다음 1박
            nt[0].append((bt(b), 110, GM['Crash'], VEL['Crash']))
    smf = build_smf(f'Drum Grid {name}', BPM, 0, False, len(seq), [('Drums', 9)], {0: 0}, nt, {},
                    markers=[(r * len(bars) + 1, f'rep {r + 1}') for r in range(reps)] + ([(len(seq), 'tail')] if tail else []))
    return write_smf(os.path.join(SK_DIR, f'drumgrid-{name}.mid'), smf)


if __name__ == '__main__':
    only = sys.argv[1:]
    for name, bars in (('original', ORIGINAL), ('revised', REVISED)):
        if not only or name in only:
            print(render(name, bars))
    for name, (bars, db) in VARIANTS.items():
        if not only or name in only:
            print(render(name, bars, downbeat_crash=db, tail=True))
