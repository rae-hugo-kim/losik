"""first-light v3 오스티나토 원형 후보 (2026-09-11). 볼레로형 재설계의 1단계 — 곡의 90%를 차지하는 8마디 원형을 먼저 고른다.

공통 고정: D장조 108 BPM, 루프 D–A–Bm–G (코드당 2마디 = 8마디 1회전), 16마디(2회전).
  회전 1: 클린기타 오스티나토 + 킥/스네어(셀 변주)      회전 2: + 베이스 근음 페달 + 16분 햇
가변: 오스티나토만. 전부 8분 격자, 1옥타브 안(C#4–D5), 옥타브 도약 없음, 리듬형은 회전 내 고정.

  A wave    코드톤 1-3-5-8-5-3-1-3 상행-하행 물결. 가장 중립적인 아르페지오
  B pedal   코드톤과 D5 페달(개방현 느낌)을 교대 — A 코드 위에서는 sus4 색채가 남
  C stairs  마디 앞 4음 순차 하행 + 뒤 4음 아르페지오 상행. 선율성 가장 높음
  D tresillo 점4분 3+3+2 당김(빰-빰-빠빠). Paper Kite 의 당김 요소
"""
import os
import sys

from pipeline import PPQ, BAR, E, S, SK_DIR, bt, hum_t, hum_v, seed, build_smf, write_smf

TRACKS = [('Drums', 9), ('Bass', 0), ('Gtr', 1)]
PCS = {0: 0, 1: 33, 2: 26}
BPM, N_BARS = 108, 16
LOOP = [('D', 38, [62, 66, 69, 74]), ('A', 33, [61, 64, 69, 73]), ('Bm', 35, [62, 66, 71, 74]), ('G', 31, [62, 67, 71, 74])]
K, SN, CH = 36, 38, 42

# 후보별 1마디 패턴: 코드 인덱스 → [(beat, dur, pitch)]
def wave(ct):
    a, b, c, d = ct
    return [(i * .5, .5, p) for i, p in enumerate([a, b, c, d, c, b, a, b])]


def pedal(ct):
    a, b, c, _ = ct
    return [(i * .5, .5, p) for i, p in enumerate([a, 74, b, 74, c, 74, b, 74])]


STAIRS = {'D': [74, 73, 71, 69, 62, 66, 69, 73], 'A': [73, 71, 69, 67, 61, 64, 69, 71],
          'Bm': [74, 73, 71, 69, 62, 66, 71, 73], 'G': [74, 73, 71, 69, 62, 67, 71, 74]}
TRESILLO = {'D': [62, 69, 74, 69], 'A': [61, 69, 73, 69], 'Bm': [62, 71, 74, 71], 'G': [62, 67, 74, 71]}

CANDIDATES = {
    'A-wave': lambda nm, ct: wave(ct),
    'B-pedal': lambda nm, ct: pedal(ct),
    'C-stairs': lambda nm, ct: [(i * .5, .5, p) for i, p in enumerate(STAIRS[nm])],
    'D-tresillo': lambda nm, ct: [(0, 1.5, TRESILLO[nm][0]), (1.5, 1.5, TRESILLO[nm][1]),
                                  (3, .5, TRESILLO[nm][2]), (3.5, .5, TRESILLO[nm][3])],
}

# 2차 후보 (09-11 판정: 트레실로 리듬 + 페달 긴장 + 마디당 큰 도약 1회 후 복귀)
#   E leap-early: 저음 코드톤 → 1.5박 옥타브 도약 D5 페달 → 3박 중음역 복귀 → 3.5박 이웃음
#   F leap-late : 중음역 → 3박 6도 도약 D5 페달 → 3.5박 즉시 복귀 (떠오름이 마디 끝, 다음 마디 첫 음과 맞물림)
LEAP_EARLY = {'D': [62, 74, 66, 69], 'A': [61, 74, 64, 69], 'Bm': [62, 74, 66, 71], 'G': [62, 74, 67, 71]}
LEAP_LATE = {'D': [66, 69, 74, 66], 'A': [64, 69, 74, 64], 'Bm': [66, 71, 74, 66], 'G': [67, 71, 74, 67]}


def tresillo_of(table):
    return lambda nm, ct: [(0, 1.5, table[nm][0]), (1.5, 1.5, table[nm][1]), (3, .5, table[nm][2]), (3.5, .5, table[nm][3])]


CANDIDATES['E-leap-early'] = tresillo_of(LEAP_EARLY)
CANDIDATES['F-leap-late'] = tresillo_of(LEAP_LATE)


def compose(cand):
    seed(960)
    nt = {0: [], 1: [], 2: []}
    pat = CANDIDATES[cand]
    for b in range(1, N_BARS + 1):
        nm, root, ct = LOOP[((b - 1) // 2) % 4]
        cyc2 = b > 8
        # 오스티나토 — 회전 2 는 벨로시티 +8 만
        for beat, dur, p in pat(nm, ct):
            acc = beat in (0, 1.5, 3) if cand[0] in 'DEF' else beat in (0, 2)
            nt[2].append((hum_t(bt(b, beat), 5), int(dur * PPQ) - 30, p, hum_v((84 if acc else 70) + (8 if cyc2 else 0), 5)))
        # 드럼 셀 (first-light v2 drums_cell 의 킥/스네어 골격)
        cell = (b - 1) % 4
        kicks = {0: [(0, 118), (2, 108)], 1: [(0, 118), (.75, 96), (2.5, 108)],
                 2: [(0, 118), (2.5, 110)], 3: [(0, 118), (1.5, 100), (2, 112)]}[cell]
        snares = {0: [(1, 116), (3, 118)], 1: [(1, 116), (3, 118)],
                  2: [(1, 116), (2, 104), (2.25, 92), (3, 118)], 3: [(1, 116), (3, 118), (3.5, 104)]}[cell]
        for beat, v in kicks:
            nt[0].append((hum_t(bt(b, beat)), 130, K, hum_v(v, 5)))
        for beat, v in snares:
            nt[0].append((hum_t(bt(b, beat)), 130, SN, hum_v(v, 6)))
        if cyc2:
            for s16 in range(16):
                nt[0].append((hum_t(bt(b) + s16 * S, 5), 50, CH, hum_v([96, 56, 74, 60][s16 % 4], 6)))
            # 베이스: 근음 페달 — 2분음표 2회, 벨로시티 일정. 자기 선율 없음
            nt[1].append((bt(b), PPQ * 2 - 40, root, 92))
            nt[1].append((bt(b, 2), PPQ * 2 - 40, root, 88))
    nt[0].append((bt(9), PPQ, 49, 110))
    return nt


if __name__ == '__main__':
    only = sys.argv[1:]
    for cand in CANDIDATES:
        if only and cand not in only:
            continue
        nt = compose(cand)
        smf = build_smf(f'Ostinato {cand}', BPM, 2, False, N_BARS, TRACKS, PCS, nt, {}, markers=[(1, 'cycle 1'), (9, 'cycle 2')])
        print(write_smf(os.path.join(SK_DIR, f'ostinato-{cand}.mid'), smf))
