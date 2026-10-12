"""장르 뼈대 스케치 (2026-10-12) — house ×2, deep house ×2.

드럼 + 베이스 + 코드(+패드)만, 16마디 루프.
1-8 풀 루프 | 9-12 빼기(브레이크) | 13-16 풀 루프 + 13마디 1박 크래시.
실행: cd docs/music/tools && python3 astra_skeletons.py
"""
import os

from pipeline import BAR, E, S, SW, bt, hum_t, hum_v, seed, build_smf, write_smf, SK_DIR
from sketches import PC, mk_chord2

N_BARS = 16
MARKERS = [(1, 'A'), (9, 'break'), (13, 'A2')]
KICK, RIM, SNARE, CLAP, CHH, OHH, CRASH = 36, 37, 38, 39, 42, 46, 49

SKETCHES = [
    dict(sid='warehouse-jack', title='Warehouse Jack', bpm=124, genre='house (Chicago)',
         notes='Drum Synth Kit 4온더플로어 + 16분 셔플 햇, 오프비트 근음 베이스, Tonewheel 오르간 스탭, Am7–D9 2코드 루프. 브레이크 = 킥·베이스 빼기'),
    dict(sid='mirrorball-rise', title='Mirrorball Rise', bpm=126, genre='house (disco-house)',
         notes='SoCal 디스코 킷, 옥타브 8분 핑거베이스, EP 오프비트 스탭 매 8분 뒷박, Dmaj7–Bm7–Gmaj7–A(add9) 4코드. 브레이크 = 햇 빼기'),
    dict(sid='velvet-hour', title='Velvet Hour', bpm=120, genre='deep house',
         notes='부드러운 킥 + 16분 클로즈드 햇, 홀드 EP 9th 코드(CC64 리페달), 점음표 서브 베이스, Classic Pad 1+5도. Fm9–Bbm9–Dbmaj9–C7(b9). 브레이크 = 킥 빼기'),
    dict(sid='low-tide-shuffle', title='Low Tide Shuffle', bpm=118, genre='deep house',
         notes='16분 햇 악센트 패턴, 9th 코드 소프트 스탭(싱코페이션), 옥타브 리프트 워킹 핑거베이스, 패드 없음. Gm9–C9–Fmaj9–Ebmaj9. 브레이크 = 햇 빼기'),
]

# sid -> (bpm, title, keysig_sf, minor, pcs, prog) ; prog = [(root_name, voicing midi list)] (1마디 1코드 순환)
SPEC = {
    'warehouse-jack': (124, 'Warehouse Jack', 0, True, {0: 25, 1: 38, 2: 16},
                       [('A', [57, 60, 64, 67]),           # Am7  A C E G
                        ('D', [54, 57, 60, 64])]),         # D9   F# A C E (rootless)
    'mirrorball-rise': (126, 'Mirrorball Rise', 2, False, {0: 0, 1: 33, 2: 4},
                        [('D', [62, 66, 69, 73]),          # Dmaj7  D F# A C#
                         ('B', [62, 66, 69, 71]),          # Bm7    D F# A B
                         ('G', [62, 66, 67, 71]),          # Gmaj7  D F# G B
                         ('A', [61, 64, 69, 71])]),        # A(add9) C# E A B
    'velvet-hour': (120, 'Velvet Hour', -4, True, {0: 25, 1: 38, 2: 4, 3: 89},
                    [('F', [56, 60, 63, 67]),              # Fm9    Ab C Eb G
                     ('Bb', [56, 60, 61, 65]),             # Bbm9   Ab C Db F
                     ('Db', [56, 60, 63, 65]),             # Dbmaj9 Ab C Eb F
                     ('C', [55, 58, 61, 64])]),            # C7b9   G Bb Db E
    'low-tide-shuffle': (118, 'Low Tide Shuffle', -2, True, {0: 25, 1: 33, 2: 4},
                         [('G', [58, 62, 65, 69]),         # Gm9    Bb D F A
                          ('C', [58, 62, 64, 67]),         # C9     Bb D E G
                          ('F', [57, 60, 64, 67]),         # Fmaj9  A C E G
                          ('Eb', [55, 58, 62, 65])]),      # Ebmaj9 G Bb D F
}


def is_break(b):
    return 9 <= b <= 12


def chord(prog, b):
    nm, voi = prog[(b - 1) % len(prog)]
    return mk_chord2(PC[nm], 'M'), voi


def d(nt, tick, pitch, vel, dur=90, t_amt=7, v_amt=9):
    nt[0].append((hum_t(tick, t_amt), dur, pitch, hum_v(vel, v_amt)))


def fill_and_crash(nt, peak=100, step=S):
    """12마디 3-4박 스네어 램프 → 13마디 1박 크래시 + 킥 (§2.9 경계 세트 축소판)."""
    n = (2 * 480) // step
    for i in range(n):
        d(nt, bt(12, 2) + i * step, SNARE, int(48 + (peak - 48) * i / max(1, n - 1)), 80, 4, 4)
    nt[0].append((bt(13), 480, CRASH, 112))
    nt[0].append((bt(13), 120, KICK, 118))


# ------------------------------------------------------------- house A: Chicago
def comp_warehouse(prog):
    nt = {0: [], 1: [], 2: []}
    for b in range(1, N_BARS + 1):
        ch, voi = chord(prog, b)
        # drums
        for beat in range(4):
            if not is_break(b) and not (b == 13 and beat == 0):
                d(nt, bt(b, beat), KICK, 112, 120)
            if beat in (1, 3):
                d(nt, bt(b, beat), SNARE, 98, 120)
                d(nt, bt(b, beat) + 6, CLAP, 70, 120)          # 스네어 밑 레이어
            d(nt, bt(b, beat + .5), OHH, 86, 110)
            for s16 in (1, 3):                                  # 16분 셔플 클로즈드
                d(nt, bt(b, beat) + s16 * S + SW // 2, CHH, 52 if s16 == 1 else 60, 50)
        # bass: 오프비트 근음 + 3.75 옥타브 픽업 (브레이크 침묵)
        if not is_break(b):
            r = ch['bass']
            for beat in range(4):
                nt[1].append((hum_t(bt(b, beat + .5), 5), 200, r, hum_v(84, 5)))
            nt[1].append((hum_t(bt(b, 3.75), 5), 90, r + 12, hum_v(70, 5)))
        # organ stabs: .5 / 2.5 + 짝수 마디 3.75 푸시
        vel = 74 if is_break(b) else 80
        for beat in (.5, 2.5):
            t = hum_t(bt(b, beat), 6)
            for p in voi:
                nt[2].append((t, 170, p, hum_v(vel, 6)))
        if b % 2 == 0 and b != N_BARS:
            t = hum_t(bt(b, 3.75), 6)
            for p in chord(prog, b + 1)[1]:
                nt[2].append((t, 140, p, hum_v(vel - 6, 6)))
    fill_and_crash(nt, 104)
    return nt, {}


# ------------------------------------------------------------- house B: disco-house
def comp_mirrorball(prog):
    nt = {0: [], 1: [], 2: []}
    for b in range(1, N_BARS + 1):
        ch, voi = chord(prog, b)
        for beat in range(4):
            if not (b == 13 and beat == 0):
                d(nt, bt(b, beat), KICK, 108, 120)
            if beat in (1, 3):
                d(nt, bt(b, beat), SNARE, 102, 120)
                d(nt, bt(b, beat) + 5, CLAP, 72, 120)
            if not is_break(b):
                d(nt, bt(b, beat + .5), OHH, 88, 140)
                for s16 in (1, 3):                              # 디스코 16분 틱
                    d(nt, bt(b, beat) + s16 * S, CHH, 50, 50, 5, 7)
        # bass: 옥타브 8분 (다운 근음 / 업 옥타브)
        r = ch['bass']
        for e8 in range(8):
            up = e8 % 2 == 1
            nt[1].append((hum_t(bt(b) + e8 * E, 4), 150 if up else 190, r + 12 if up else r,
                          hum_v(64 if up else 76, 5)))
        # EP: 매 8분 뒷박 스탭
        for beat in range(4):
            t = hum_t(bt(b, beat + .5), 6)
            for p in voi:
                nt[2].append((t, 140, p, hum_v(70 if beat % 2 == 0 else 76, 6)))
    fill_and_crash(nt, 108)
    return nt, {}


# ------------------------------------------------------------- deep house A: held
def comp_velvet(prog):
    nt = {0: [], 1: [], 2: [], 3: []}
    cc = {2: []}
    for b in range(1, N_BARS + 1):
        ch, voi = chord(prog, b)
        for beat in range(4):
            if not is_break(b) and not (b == 13 and beat == 0):
                d(nt, bt(b, beat), KICK, 96, 120, 6, 8)
            if beat in (1, 3):
                d(nt, bt(b, beat), SNARE, 70, 100, 6, 8)
                d(nt, bt(b, beat) + 8, CLAP, 50, 100, 6, 6)
            for s16 in range(4):                                # 16분 클로즈드, 악센트는 뒷박
                if beat == 3 and s16 == 2:
                    continue
                v = {0: 44, 1: 34, 2: 62, 3: 40}[s16]
                d(nt, bt(b, beat) + s16 * S, CHH, v, 50, 6, 7)
        d(nt, bt(b, 3.5), OHH, 64, 200, 6, 6)                  # 마디당 오픈햇 1개
        # sub bass: 점4분 + 롱 (브레이크도 유지, 약하게)
        r = ch['bass']
        bv = 60 if is_break(b) else 72
        nt[1].append((hum_t(bt(b), 4), 700, r, hum_v(bv, 4)))
        nt[1].append((hum_t(bt(b, 1.5), 4), 1150, r, hum_v(bv - 6, 4)))
        # EP: 마디 홀드 + 살짝 롤 + 3.5박 재터치(윗 2음)
        for i, p in enumerate(voi):
            nt[2].append((hum_t(bt(b) + i * 12, 4), BAR - 120, p, hum_v(64, 5)))
        for p in voi[2:]:
            nt[2].append((hum_t(bt(b, 3.5), 4), 200, p, hum_v(50, 5)))
        cc[2].append((bt(b) + 10, 64, 127))                     # CC64 마디 리페달
        cc[2].append((bt(b) + BAR - 30, 64, 0))
        # pad: 1+5도(+옥타브) (§2.6)
        r3 = ch['pad'][1]
        for p in (r3, r3 + 7, r3 + 12):
            nt[3].append((bt(b), BAR - 20, p, hum_v(52 if not is_break(b) else 60, 3)))
    fill_and_crash(nt, 88, E)
    return nt, cc


# ------------------------------------------------------------- deep house B: stabbed
def comp_lowtide(prog):
    nt = {0: [], 1: [], 2: []}
    acc = {0: 56, 1: 36, 2: 78, 3: 46}
    for b in range(1, N_BARS + 1):
        ch, voi = chord(prog, b)
        nxt = chord(prog, b + 1)[0]['bass'] if b < N_BARS else ch['bass']
        for beat in range(4):
            if not (b == 13 and beat == 0):
                d(nt, bt(b, beat), KICK, 100, 120, 6, 8)
            if beat in (1, 3):
                d(nt, bt(b, beat), RIM, 72, 80, 6, 6)
                d(nt, bt(b, beat) + 4, SNARE, 66, 100, 6, 6)
            if not is_break(b):
                for s16 in range(4):
                    if b % 2 == 0 and beat == 3 and s16 == 2:
                        continue
                    d(nt, bt(b, beat) + s16 * S, CHH, acc[s16], 45, 5, 6)
        if not is_break(b) and b % 2 == 0:
            d(nt, bt(b, 3.5), OHH, 70, 200, 6, 6)              # 2마디당 오픈햇 1개
        # bass: 근음 → 옥타브 리프트 → 5도 → 다음 근음 위 온음 어프로치
        r = ch['bass']
        for beat, p, dur, v in ((0, r, 400, 74), (1.5, r + 12, 180, 64), (2, r + 7, 400, 68),
                                (3, nxt + 2, 200, 62), (3.5, r + 12, 180, 60)):
            nt[1].append((hum_t(bt(b, beat), 5), dur, p, hum_v(v, 5)))
        # EP 소프트 스탭: 1 / 1.75 / 3.5 (3.5 는 다음 코드 선행)
        for beat, dur, v, src in ((0, 300, 62, voi), (1.75, 160, 54, voi),
                                  (3.5, 220, 58, chord(prog, b + 1)[1] if b < N_BARS else voi)):
            t = hum_t(bt(b, beat), 6)
            for p in src:
                nt[2].append((t, dur, p, hum_v(v, 5)))
    fill_and_crash(nt, 92)
    return nt, {}


COMP = {'warehouse-jack': comp_warehouse, 'mirrorball-rise': comp_mirrorball,
        'velvet-hour': comp_velvet, 'low-tide-shuffle': comp_lowtide}
SEEDS = {'warehouse-jack': 1201, 'mirrorball-rise': 1202, 'velvet-hour': 1203, 'low-tide-shuffle': 1204}


def compose(sid):
    bpm, title, sf, minor, pcs, prog = SPEC[sid]
    seed(SEEDS[sid])
    nt, cc = COMP[sid](prog)
    return nt, cc, pcs, N_BARS, bpm, title, sf, minor


def tracks_for(pcs):
    tr = [('Drums', 9), ('Bass', 0), ('Keys', 1)]
    return tr + [('Pad', 2)] if 3 in pcs else tr


if __name__ == '__main__':
    for sk in SKETCHES:
        nt, cc, pcs, n_bars, bpm, title, sf, minor = compose(sk['sid'])
        smf = build_smf(title, bpm, sf, minor, n_bars, tracks_for(pcs), pcs, nt, cc, MARKERS)
        print(write_smf(os.path.join(SK_DIR, f"{sk['sid']}-v1.mid"), smf))
