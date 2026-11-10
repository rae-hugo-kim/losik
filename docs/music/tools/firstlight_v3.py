"""First Light v3 (2026-09-11) — 볼레로형 재설계. 오스티나토 E(leap-early) 위의 11회전 점층·후퇴.

계획(FEEDBACK_LOG 09-11 승인):
  불변: 오스티나토 리듬형(트레실로 3+3+2 + D5 페달 + 마디당 옥타브 도약 1회), 루프 D–A–Bm–G(코드당 2마디), 108 BPM, 베이스 근음 페달.
  가변 5축: 음역 / 밀도 / 음색 / 다이내믹 / 탑노트. 한 회전에 최대 2축.
  에너지 2-3-4-4-5-3-6-8-3-9-1 (후퇴 = 회전 6·9). 떠오름 = 회전 4·7·10 의 7~8마디, 온음계 4도 위 1.5마디 후 복귀.

트랙: 0 Drums(SoCal) 1 Bass(Simple Foundation, 근음 페달) 2 Gtr(Hard Rock 클린 = vel≤92, 오스티나토) 3 AcGtr(Acoustic Guitar)
      4 Piano(Studio Grand, 보컬 탑노트) 5 Strings(Authentic Strings) 6 Pad(Classic Pad, 회전 6·9만) 7 Dist(Hard Rock vel≥108 파워코드, 회전 8·10)

| 회전 | 마디 | 축 | 내용 |
| 1 | 1-8 | — | 기타 오스티나토 + 킥/스네어 |
| 2 | 9-16 | 밀도 | + 베이스 페달, 16분 햇 |
| 3 | 17-24 | 밀도·음색 | + 어쿠스틱 롱스트럼 |
| 4 | 25-32 | 음역 | 7~8마디 떠오름 |
| 5 | 33-40 | 탑노트 | 피아노 첫 등장 |
| 6 | 41-48 | 후퇴 | 하프타임, 어쿠스틱 OUT, 패드 IN(크레셴도)→OUT. 피아노 유지 |
| 7 | 49-56 | 음역·밀도 | 어쿠스틱이 오스티나토 옥타브 위 더블링, 스트링 IN, 라이드. 떠오름 |
| 8 | 57-64 | 음색·다이내믹 | 디스토션 파워코드 IN, 오픈햇, 베이스 8분 펌핑. 피아노 절정 |
| 9 | 65-72 | 후퇴 | 디스토션·스트링 OUT, 하프타임, 패드 IN→OUT. 오스티나토 원형 |
| 10 | 73-80 | 밀도·다이내믹 | 전부 + 디스토션 + 피아노 옥타브 더블링. 떠오름 |
| 11 | 81-88 | 감산 | 회전 1 거울 → 기타 단독 → I 종지 (87-88 D) |
"""
import os
import sys

from pipeline import PPQ, BAR, E, S, SK_DIR, bt, hum_t, hum_v, seed, build_smf, write_smf
from ostinato import LEAP_EARLY

TRACKS = [('Drums', 9), ('Bass', 0), ('Gtr', 1), ('AcGtr', 2), ('Piano', 3), ('Strings', 4), ('Pad', 5), ('Dist', 6)]
PCS = {0: 0, 1: 33, 2: 26, 3: 25, 4: 0, 5: 50, 6: 89, 7: 26}
DR, BS, GT, AG, PN, ST, PD, DI = range(8)
SID, TITLE, BPM, N_BARS = 'first-light', 'First Light', 108, 88
K, SN, CH, OH, CR, RIDE, HT, MT, LT = 36, 38, 42, 46, 49, 51, 47, 45, 43
DMAJ = {2, 4, 6, 7, 9, 11, 1}
SCALE = [0, 2, 4, 5, 7, 9, 11]

# 루프: 이름, 베이스 근음, stab(코드톤 보이싱), 파워코드, r4(근음 4옥타브), 3도
LOOP = [('D', 38, [62, 66, 69, 74], [50, 57, 62], 62, 66), ('A', 33, [61, 64, 69, 73], [45, 52, 57], 57, 61),
        ('Bm', 35, [62, 66, 71, 74], [47, 54, 59], 59, 62), ('G', 31, [62, 67, 71, 74], [43, 50, 55], 55, 59)]
ENERGY = [2, 3, 4, 4, 5, 3, 6, 8, 3, 9, 1]
LIFT_CYCLES = {4, 7, 10}
RETREAT = {6, 9}

# 보컬 탑노트 (피아노) — 8마디, 2~4마디 호흡, 쉼표 포함, 오스티나토 리듬과 독립
TOP = [
    [(1, 1, 74), (2, 2, 78)],
    [(0, 1.5, 81), (1.5, .5, 78), (2, 2, 74)],
    [(0, 1, 69), (1, .5, 71), (1.5, 1.5, 76), (3, 1, 73)],
    [(0, 3, 69)],
    [(1, 1, 74), (2, 1, 78), (3, 1, 81)],
    [(0, 2, 83), (2, 2, 78)],
    [(0.5, .5, 79), (1, .5, 78), (1.5, 1.5, 74), (3, 1, 71)],
    [(0, 3, 74)],
]


def cycle_of(b):
    return (b - 1) // 8 + 1


def chord(b):
    if b >= 87:
        return LOOP[0]
    return LOOP[((b - 1) % 8) // 2]


def diatonic_up(p, steps):
    """온음계 도수 이동 (D장조)."""
    rel = (p - 2) % 12
    octv = (p - 2) // 12
    idx = SCALE.index(rel)
    idx += steps
    return 2 + (octv + idx // 7) * 12 + SCALE[idx % 7]


def compose():
    seed(963)
    nt = {i: [] for i in range(8)}

    def g(tr, tick, dur, pitch, vel):
        nt[tr].append((max(0, int(tick)), int(dur), pitch, vel))

    # ---------------------------------------------------------------- ostinato (불변 리듬형)
    def ostinato(b, vel_off=0, lift=False, lift_partial=False, tr=GT, transpose=0):
        nm = chord(b)[0]
        notes = LEAP_EARLY[nm]
        hits = [(0, 1.5, notes[0]), (1.5, 1.5, notes[1]), (3, .5, notes[2]), (3.5, .5, notes[3])]
        for i, (beat, dur, p) in enumerate(hits):
            up = lift and (not lift_partial or beat < 1.5)     # partial: 마디 첫 음만 떠 있고 1.5박에 복귀
            pp = diatonic_up(p, 3) if up else p
            acc = beat in (0, 1.5, 3)
            g(tr, hum_t(bt(b, beat), 5), int(dur * PPQ) - 30, pp + transpose, hum_v(min(92, (84 if acc else 70) + vel_off), 5))

    # ---------------------------------------------------------------- drums
    def drums(b, hats, fill=False, half=False):
        t0 = bt(b)
        if half:
            g(DR, hum_t(t0), 130, K, hum_v(108, 5))
            g(DR, hum_t(bt(b, 2.5)), 110, K, hum_v(92, 5))
            g(DR, hum_t(bt(b, 2)), 130, SN, hum_v(110, 6))
            for e8 in range(8):
                g(DR, hum_t(t0 + e8 * E, 5), 60, RIDE if hats == 'ride' else CH, hum_v(72 if e8 % 2 == 0 else 50, 6))
            return
        cell = (b - 1) % 4
        kicks = {0: [(0, 118), (2, 108)], 1: [(0, 118), (.75, 96), (2.5, 108)],
                 2: [(0, 118), (2.5, 110)], 3: [(0, 118), (1.5, 100), (2, 112)]}[cell]
        snares = {0: [(1, 116), (3, 118)], 1: [(1, 116), (3, 118)],
                  2: [(1, 116), (2, 104), (2.25, 92), (3, 118)], 3: [(1, 116), (3, 118), (3.5, 104)]}[cell]
        if fill:
            snares = [(x, v) for x, v in snares if x < 2.5]
        for beat, v in kicks:
            g(DR, hum_t(bt(b, beat)), 130, K, hum_v(v, 5))
        for beat, v in snares:
            g(DR, hum_t(bt(b, beat)), 130, SN, hum_v(v, 6))
        if hats and not fill:
            for beat in (1.75, 3.75):
                g(DR, hum_t(bt(b, beat)), 70, SN, hum_v(38, 6))
        lim = 10 if fill else 16
        for s16 in range(lim):
            tt = t0 + s16 * S
            acc = [96, 56, 74, 60][s16 % 4]
            if hats == 'ch':
                g(DR, hum_t(tt, 5), 50, CH, hum_v(acc, 6))
            elif hats == 'ride':
                if s16 % 2 == 0:
                    g(DR, hum_t(tt, 5), 70, RIDE, hum_v(88 if s16 % 4 == 0 else 66, 6))
                elif s16 in (5, 13):
                    g(DR, hum_t(tt, 5), 80, OH, hum_v(84, 6))
            elif hats == 'oh':
                if s16 % 2 == 0:
                    g(DR, hum_t(tt, 5), 90, OH if s16 % 4 == 2 else CH, hum_v(98 if s16 % 4 == 2 else 84, 6))
                else:
                    g(DR, hum_t(tt, 5), 50, CH, hum_v(58, 6))
        if fill:
            for i, s16 in enumerate(range(10, 13)):
                g(DR, hum_t(t0 + s16 * S), 90, SN, 72 + i * 12)
            g(DR, hum_t(bt(b, 3.25)), 100, HT, hum_v(104))
            g(DR, hum_t(bt(b, 3.5)), 100, MT, hum_v(110))
            g(DR, hum_t(bt(b, 3.75)), 110, LT, hum_v(116))

    # ---------------------------------------------------------------- bass: 근음 페달만
    def bass(b, style, vel=90):
        r = chord(b)[1]
        if style == 'half':
            g(BS, bt(b), PPQ * 2 - 40, r, vel)
            g(BS, bt(b, 2), PPQ * 2 - 40, r, vel - 4)
        elif style == 'whole':
            g(BS, bt(b), BAR - 60, r, vel)
        elif style == 'pump':
            for e8 in range(8):
                g(BS, hum_t(bt(b) + e8 * E, 4), 200, r, hum_v(vel if e8 % 2 == 0 else vel - 12, 4))

    # ---------------------------------------------------------------- 화성 받침
    def ac_long(b, vel):
        v = chord(b)[2] + [chord(b)[2][0] + 12]
        for i, p in enumerate(v):
            g(AG, hum_t(bt(b) + i * 14, 6), int(2.3 * PPQ) - i * 14, p, hum_v(vel, 5))
        for i, p in enumerate(v):
            g(AG, hum_t(bt(b, 2.5) + i * 14, 6), int(1.4 * PPQ) - i * 14, p, hum_v(vel - 6, 5))

    def pad(b, vel):
        r4 = chord(b)[4]
        for p in (r4 - 12, r4 - 5):
            g(PD, bt(b), BAR - 20, p, vel)

    def strings(b, vel, high=False):
        _, _, _, _, r4, third = chord(b)
        for p in ((third + 12, r4 + 19, r4 + 24) if high else (r4, r4 + 7, r4 + 12)):
            g(ST, bt(b), BAR - 30, p, vel)

    def dist(b, vel):
        for p in chord(b)[3]:
            g(DI, hum_t(bt(b), 4), BAR - 40, p, hum_v(vel, 3))

    def top(start, vel, transpose=0):
        for i, bar in enumerate(TOP):
            for beat, dur, p in bar:
                g(PN, hum_t(bt(start + i, beat), 8), int(dur * PPQ) - 40, p + transpose, hum_v(vel, 6))

    # ================================================================ 11회전
    for b in range(1, N_BARS + 1):
        c = cycle_of(b)
        i8 = (b - 1) % 8 + 1            # 회전 안의 마디 1..8
        en = ENERGY[c - 1]
        lift = c in LIFT_CYCLES and i8 in (7, 8)
        voff = {1: 0, 2: 2, 3: 4, 4: 4, 5: 6, 6: -6, 7: 8, 8: 12, 9: -8, 10: 14, 11: -12}[c]
        fill = i8 == 8 and c not in (10, 11) and c + 1 not in RETREAT

        # 오스티나토 — 11회전 87-88 은 종지
        if b <= 86:
            ostinato(b, voff, lift=lift, lift_partial=(i8 == 8))
        elif b == 87:
            for beat, p in ((0, 62), (1, 66), (2, 69), (3, 74)):
                g(GT, bt(b, beat), PPQ * (4 - beat) + PPQ * 4 - 100, p, 72 - beat * 4)
        # 드럼
        if c == 1:
            drums(b, None, fill=fill)
        elif c in (2, 3, 4, 5):
            drums(b, 'ch', fill=fill)
        elif c in RETREAT:
            drums(b, 'ride' if c == 9 else 'ch', half=True)
        elif c == 7:
            drums(b, 'ride', fill=fill)
        elif c in (8, 10):
            drums(b, 'oh', fill=fill)
        elif c == 11:
            if i8 <= 4:
                drums(b, None)
            elif i8 <= 6:
                g(DR, hum_t(bt(b)), 130, K, hum_v(84, 5))
        # 베이스
        if c == 2 or c in (3, 4, 5, 7):
            bass(b, 'half', 90 + (4 if c >= 5 else 0))
        elif c in RETREAT:
            bass(b, 'whole', 82)
        elif c in (8, 10):
            bass(b, 'pump', 100)
        elif c == 11 and i8 <= 4:
            bass(b, 'whole', 78)
        elif b >= 87:
            g(BS, bt(b), BAR - 60, 38, 74 - (b - 87) * 10)
        # 어쿠스틱
        if c in (3, 4, 5):
            ac_long(b, 66 + (c - 3) * 4)
        elif c == 7:
            ostinato(b, -10, lift=lift, lift_partial=(i8 == 8), tr=AG, transpose=12)
        elif c in (8, 10):
            ac_long(b, 84)
        elif c == 11 and i8 <= 2:
            ac_long(b, 56)
        # 패드 — 후퇴 회전에만, 스윽 들어와 조용히 나감
        if c in RETREAT:
            pad(b, [34, 46, 56, 60, 60, 56, 46, 34][i8 - 1])
        elif c + 1 in RETREAT and i8 == 8:
            pad(b, 26)
        # 스트링
        if c == 7:
            strings(b, 50)
        elif c == 8:
            strings(b, 60)
        elif c == 10:
            strings(b, 66, high=True)
        # 디스토션
        if c in (8, 10):
            dist(b, 110 if c == 8 else 118)
    # 피아노 탑노트
    top(33, 78)
    top(41, 72)
    top(49, 84)
    top(57, 96)
    top(73, 100)
    top(73, 84, transpose=12)
    # 경계: 회전 시작 크래시(2~10), 8·10 진입은 2마디 크래시 롤, 하이 회전은 2마디마다 크래시
    for c in range(2, 11):
        s = (c - 1) * 8 + 1
        if c in (8, 10):
            for k in range(16):
                g(DR, hum_t(bt(s - 2) + k * E, 6), 200, CR, 34 + int(k * (116 - 34) / 15))
            g(DR, bt(s), PPQ, CR, 124)
            for b in range(s + 2, s + 8, 2):
                g(DR, bt(b), PPQ, CR, 104)
        elif c in RETREAT:
            g(DR, bt(s), PPQ * 2, CR, 84)
        else:
            g(DR, bt(s), PPQ, CR, 112)
    g(DR, bt(81), PPQ * 2, CR, 96)
    g(DR, bt(87), PPQ * 3, CR, 60)
    return nt


def check(nt):
    bad = [(tr, t, p) for tr in nt if tr != DR for t, d, p, v in nt[tr] if p % 12 not in DMAJ]
    clashes = []
    for t1, d1, p1, _ in nt[GT]:
        for t2, d2, p2, _ in nt[PN]:
            if t1 < t2 + d2 and t2 < t1 + d1 and abs(p1 - p2) % 12 == 1 and abs(p1 - p2) < 12:
                clashes.append(((t1 + 60) // BAR + 1, p1, p2))
    rng = {tr: (min(p for _, _, p, _ in nt[tr]), max(p for _, _, p, _ in nt[tr])) for tr in nt if nt[tr]}
    return bad, clashes, rng


if __name__ == '__main__':
    nt = compose()
    bad, clashes, rng = check(nt)
    assert not bad, bad[:5]
    assert not clashes, clashes[:8]
    markers = [((c - 1) * 8 + 1, f'cycle {c} e{ENERGY[c - 1]}') for c in range(1, 12)]
    smf = build_smf(TITLE, BPM, 2, False, N_BARS, TRACKS, PCS, nt, {}, markers=markers)
    print(write_smf(os.path.join(SK_DIR, f'{SID}-v3.mid'), smf))
    print('range', rng)
