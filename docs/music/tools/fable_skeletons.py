"""장르 뼈대 라운드 (2026-10-12) — lo-fi house ×2 / lo-fi hip hop ×2.

드럼 + 베이스 + 코드(+패드)만, 16마디 루프. 구조: 1-8 풀 루프 / 9-12 빼기(브레이크) / 13-16 풀 + 13마디 1박 크래시.
같은 재료(7th/9th 코드 루프)가 드럼·베이스 골격에 따라 장르가 바뀌는 것을 비교하는 학습용 레퍼런스.
실행: cd docs/music/tools && python3 fable_skeletons.py  → sketches/{sid}-v1.mid
"""
import os

from pipeline import PPQ, BAR, E, S, SW, SK_DIR, bt, hum_t, hum_v, seed, build_smf, write_smf
from sketches import PC, mk_chord2

N_BARS = 16
MARKERS = [(1, 'A'), (9, 'break'), (13, 'A2')]
END = bt(N_BARS + 1) - 120         # 모든 노트·CC 는 16마디 안에서 끝낸다 (self-check last_bar≈16.9)
HH_SWING = 2 * SW                  # 힙합 8분 스윙 (44틱 ≈ 59%) — 하우스는 SW 그대로

# GM 드럼 노트
KICK, RIM, SNARE, CLAP, HAT, OHAT, CRASH = 36, 37, 38, 39, 42, 46, 49

SKETCHES = [
    dict(sid='dusty-tape-house', title='Dusty Tape House', bpm=120, genre='lo-fi house',
         notes='딥하우스 4/4 그리드 + 16분 햇 SW 스윙, 먹먹한 EP 오프비트 스탭, 오프비트 베이스 15틱 지각. Am9–Dm9'),
    dict(sid='faded-organ-house', title='Faded Organ House', bpm=122, genre='lo-fi house',
         notes='햇 절반(8분)만, 톤휠 오르간 롱코드 + Glistening 패드(1+5도), 점4분 베이스, 넓은 휴머나이즈. Fm7–D♭maj7–B♭m7–C7'),
    dict(sid='rainy-window-beat', title='Rainy Window Beat', bpm=80, genre='lo-fi hip hop',
         notes='붐뱁 백비트 + 스윙 햇 + 고스트 스네어, EP 9th 코드 CC64, 핑거베이스가 킥을 따라감. Gm9–C9–Fmaj9–Dm9'),
    dict(sid='slow-room-piano', title='Slow Room Piano', bpm=74, genre='lo-fi hip hop',
         notes='하프타임(3박 스네어만), 짝수 마디 림, 스튜디오 그랜드 코드 CC64, 근음 홀드 베이스. A♭maj7–Gm7–Fm9–B♭13'),
]
META = {s['sid']: s for s in SKETCHES}

# 코드 루프: (근음, 성질, 건반 보이싱). 근음 베이스는 mk_chord2 의 bass 음역(36-43) 사용.
PROG = {
    'dusty-tape-house': [('A', 'm7', [60, 64, 67, 71])] * 2 + [('D', 'm7', [60, 64, 65, 69])] * 2,        # Am9 / Dm9 (rootless)
    'faded-organ-house': [('F', 'm7', [53, 56, 60, 63]), ('Db', 'M7', [49, 53, 56, 60]),
                          ('Bb', 'm7', [53, 56, 58, 61]), ('C', '7', [52, 55, 58, 60])],
    'rainy-window-beat': [('G', 'm7', [58, 62, 65, 69]), ('C', '7', [58, 62, 64, 67]),
                          ('F', 'M7', [57, 60, 64, 67]), ('D', 'm7', [57, 60, 64, 65])],                     # 9th rootless
    'slow-room-piano': [('Ab', 'M7', [44, 51, 60, 63, 67]), ('G', 'm7', [43, 50, 58, 62, 65]),
                        ('F', 'm7', [41, 48, 56, 60, 63, 67]), ('Bb', '7', [46, 53, 56, 62, 67])],          # LH 2음 + RH
}


def chord(sid, b):
    return PROG[sid][(b - 1) % len(PROG[sid])]


def root(sid, b):
    nm, q, _ = chord(sid, b)
    return mk_chord2(PC[nm], q)['bass']


def in_break(b):
    return 9 <= b <= 12


def compose(sid):
    m = META[sid]
    seed(sum(map(ord, sid)))
    nt = {0: [], 1: [], 2: [], 3: []}
    cc = {2: []}

    def add(tr, tick, dur, p, v, ta=8, va=10):
        t = hum_t(tick, ta) if ta else tick
        if t >= END:
            return
        nt[tr].append((t, max(20, min(dur, END - t)), p, hum_v(v, va) if va else v))

    def pedal(b):
        cc[2].append((bt(b) + 10, 64, 127))
        cc[2].append((min(bt(b + 1) - 40, END), 64, 0))

    def crash():
        add(0, bt(13), 960, CRASH, 112, 0, 6)

    COMPOSERS[sid](m, add, pedal)
    crash()
    if sid == 'dusty-tape-house':
        tracks, pcs = TRK3, {0: 25, 1: 38, 2: 4}
        sf, minor = 0, True
    elif sid == 'faded-organ-house':
        tracks, pcs = TRK4, {0: 25, 1: 38, 2: 16, 3: 88}
        sf, minor = -4, True
    elif sid == 'rainy-window-beat':
        tracks, pcs = TRK3, {0: 0, 1: 33, 2: 4}
        sf, minor = -1, False
    else:
        tracks, pcs = TRK3, {0: 0, 1: 33, 2: 0}
        sf, minor = -3, False
    nt = {k: v for k, v in nt.items() if k < len(tracks)}
    return nt, cc, pcs, N_BARS, m['bpm'], m['title'], sf, minor


TRK3 = [('Drums', 9), ('Bass', 0), ('Keys', 1)]
TRK4 = TRK3 + [('Pad', 2)]


# =============================================================== lo-fi house A
def c_dusty(m, add, pedal):
    sid = m['sid']
    for b in range(1, N_BARS + 1):
        brk = in_break(b)
        # 킥: 4/4, 딥하우스라 부드럽게. 브레이크에서는 킥 제거
        if not brk:
            for beat in range(4):
                add(0, bt(b, beat), 120, KICK, 96 if beat % 2 == 0 else 88, 6, 8)
        # 스네어 2·4 + 클랩은 스네어 밑 레이어로만 (§2-5)
        for beat in (1, 3):
            add(0, bt(b, beat), 120, SNARE, 82, 6, 8)
            add(0, bt(b, beat) + 4, 120, CLAP, 58, 6, 8)
        # 16분 클로즈드 햇: 짝수 16분 정박, 홀수 16분에 SW 스윙. 오프비트 8분 악센트, 4박 뒤 오픈햇 1개
        for s in range(16):
            tick = bt(b) + s * S + (SW if s % 2 else 0)
            if s == 14:
                add(0, tick, 200, OHAT, 64, 8, 8)
                continue
            v = 70 if s % 4 == 2 else (52 if s % 4 == 0 else 40)
            add(0, tick, 60, HAT, v, 8, 10)
        # 베이스: 오프비트 8분 근음, 15틱 지각 (lo-fi 의 끌리는 맛). 4박 뒤는 옥타브
        r = root(sid, b)
        for beat in range(4):
            p = r + 12 if beat == 3 and b % 2 == 0 else r
            add(1, bt(b, beat + .5) + 15, 190, p, 74, 6, 6)
        # EP: 먹먹한 오프비트 스탭 (짧고 여린 벨로시티), 홀수 마디는 4박 16분 밀기
        _, _, voi = chord(sid, b)
        hits = [(.5, 150), (2.5, 150)] + ([(3.75, 110)] if b % 2 == 1 else [])
        for beat, dur in hits:
            t0 = hum_t(bt(b, beat) + SW // 2, 6)
            v0 = hum_v(58, 5)
            for i, p in enumerate(voi):
                add(2, t0 + i * 4, dur, p, v0 - (4 if i == 0 else 0), 0, 3)


# =============================================================== lo-fi house B
def c_faded(m, add, pedal):
    sid = m['sid']
    for b in range(1, N_BARS + 1):
        brk = in_break(b)
        # 킥 4/4 (넓은 휴머나이즈), 브레이크에서도 유지하되 여리게
        for beat in range(4):
            add(0, bt(b, beat), 120, KICK, 74 if brk else 90, 12, 12)
        for beat in (1, 3):
            add(0, bt(b, beat), 120, SNARE, 78, 12, 12)
            add(0, bt(b, beat) + 6, 120, CLAP, 54, 12, 12)
        # 햇: 16분 중 하나 걸러 → 8분만, 오프비트에 SW 스윙. 브레이크에서는 햇 전부 제거
        if not brk:
            for e8 in range(8):
                tick = bt(b) + e8 * E + (SW if e8 % 2 else 0)
                if e8 == 7 and b % 2 == 0:
                    add(0, tick, 200, OHAT, 60, 14, 12)
                else:
                    add(0, tick, 60, HAT, 66 if e8 % 2 else 44, 14, 12)
        # 베이스: 점4분 3+3+2 홀드 (근음·근음·5도), 12틱 지각
        r = root(sid, b)
        for beat, dur, p in ((0, 660, r), (1.5, 660, r), (3, 400, r + 7)):
            add(1, bt(b, beat) + 12, dur, p, 70, 12, 8)
        # 오르간 롱코드: 매 마디 리트리거, 약하게
        _, _, voi = chord(sid, b)
        t0 = hum_t(bt(b) + 10, 10)
        for i, p in enumerate(voi):
            add(2, t0 + i * 3, BAR - 70, p, 56, 0, 6)
        # 패드: 1+5도만 (§2-6), 4옥 근처
        rp = 60 + (PC[chord(sid, b)[0]] if PC[chord(sid, b)[0]] <= 7 else PC[chord(sid, b)[0]] - 12)
        for p in (rp, rp + 7):
            add(3, bt(b) + 20, BAR - 50, p, 48, 10, 6)


# =============================================================== lo-fi hip hop A
def c_rainy(m, add, pedal):
    sid = m['sid']
    for b in range(1, N_BARS + 1):
        brk = in_break(b)
        kicks = [0, 2.5, 2.75] if b % 2 == 1 else [0, 1.75, 2.5]
        # 킥 (브레이크에서 제거)
        if not brk:
            for k in kicks:
                add(0, bt(b, k) + (HH_SWING if k % .5 else 0), 120, KICK, 100 if k == 0 else 86, 8, 10)
        # 스네어 2·4 백비트 + 고스트
        for beat in (1, 3):
            add(0, bt(b, beat), 160, SNARE, 96, 8, 8)
        for g in ((.75, 2.25) if b % 2 == 1 else (.75, 3.75)):
            add(0, bt(b, g) + S // 3, 80, SNARE, 36, 8, 6)
        # 8분 햇, 오프비트 스윙. 짝수 마디 4박에 16분 픽업
        for e8 in range(8):
            add(0, bt(b) + e8 * E + (HH_SWING if e8 % 2 else 0), 60, HAT, 46 if e8 % 2 else 64, 10, 10)
        if b % 2 == 0 and not brk:
            add(0, bt(b, 3.75) + S // 3, 50, HAT, 40, 8, 6)
        # 12마디 4박: 스네어 램프 필인
        if b == 12:
            for i, f in enumerate((3.25, 3.5, 3.75)):
                add(0, bt(b, f), 90, SNARE, 52 + i * 12, 4, 4)
        # 베이스: 킥을 따라감 (마지막 킥은 5도). 브레이크는 근음 2박 홀드만
        r = root(sid, b)
        if brk:
            add(1, bt(b) + 12, 2 * PPQ - 40, r, 70, 6, 6)
        else:
            for i, k in enumerate(kicks):
                nxt = kicks[i + 1] if i + 1 < len(kicks) else 4
                p = r + 7 if i == len(kicks) - 1 else r
                add(1, bt(b, k) + 12 + (HH_SWING if k % .5 else 0), int((nxt - k) * PPQ) - 30, p, 76, 6, 6)
        # EP 9th 코드: 1박 늦게 굴려서 + 3박 뒤 재타격, CC64 마디 리페달
        _, _, voi = chord(sid, b)
        t0 = hum_t(bt(b) + 20, 8)
        for i, p in enumerate(voi):
            add(2, t0 + i * 10, int(1.75 * PPQ), p, 64, 0, 5)
        t1 = hum_t(bt(b, 2.5) + HH_SWING, 8)
        for i, p in enumerate(voi[1:]):
            add(2, t1 + i * 6, int(1.25 * PPQ), p, 54, 0, 5)
        pedal(b)


# =============================================================== lo-fi hip hop B
def c_slow(m, add, pedal):
    sid = m['sid']
    for b in range(1, N_BARS + 1):
        brk = in_break(b)
        # 하프타임 킥: 1박, 2박 뒤, (홀수 마디) 4박 뒤
        for k in ([0, 1.5, 3.5] if b % 2 == 1 else [0, 1.5]):
            add(0, bt(b, k) + (HH_SWING if k % 1 else 0), 120, KICK, 98 if k == 0 else 82, 8, 10)
        # 3박 백비트 하나: 홀수 마디 스네어, 짝수 마디 림 (+ 4박 뒤 림 고스트)
        if b % 2 == 1:
            add(0, bt(b, 2), 180, SNARE, 94, 8, 8)
        else:
            add(0, bt(b, 2), 100, RIM, 90, 8, 8)
            add(0, bt(b, 3.5) + HH_SWING, 60, RIM, 40, 8, 6)
        # 8분 햇 스윙 (브레이크에서 제거)
        if not brk:
            for e8 in range(8):
                add(0, bt(b) + e8 * E + (HH_SWING if e8 % 2 else 0), 60, HAT, 42 if e8 % 2 else 58, 10, 10)
        if b == 12:
            for i, f in enumerate((3.0, 3.25, 3.5, 3.75)):
                add(0, bt(b, f), 90, RIM if i < 2 else SNARE, 48 + i * 12, 4, 4)
        # 베이스: 근음 2박 홀드만 (성기게). 짝수 마디는 4박 뒤 근음 옥타브 짧게 한 번
        r = root(sid, b)
        add(1, bt(b) + 14, 2 * PPQ - 30, r, 68, 6, 6)
        if b % 2 == 0:
            add(1, bt(b, 3.5) + HH_SWING + 10, 200, r + 12, 58, 6, 6)
        # 피아노: LH 2음 + RH 롤, 짝수 마디 3박 뒤 RH 상단 2음 재타격. CC64 마디 리페달
        _, _, voi = chord(sid, b)
        t0 = hum_t(bt(b) + 15, 8)
        for i, p in enumerate(voi):
            add(2, t0 + i * 12, BAR - 120, p, 66 if p < 55 else 60, 0, 5)
        if b % 2 == 0:
            t1 = hum_t(bt(b, 2.5) + HH_SWING, 8)
            for i, p in enumerate(voi[-2:]):
                add(2, t1 + i * 8, PPQ, p, 50, 0, 4)
        pedal(b)


COMPOSERS = {'dusty-tape-house': c_dusty, 'faded-organ-house': c_faded,
             'rainy-window-beat': c_rainy, 'slow-room-piano': c_slow}


if __name__ == '__main__':
    for s in SKETCHES:
        nt, cc, pcs, n_bars, bpm, title, sf, minor = compose(s['sid'])
        tracks = TRK4 if len(pcs) == 4 else TRK3
        smf = build_smf(title, bpm, sf, minor, n_bars, tracks, pcs, nt, cc, MARKERS)
        print(write_smf(os.path.join(SK_DIR, f"{s['sid']}-v1.mid"), smf))
