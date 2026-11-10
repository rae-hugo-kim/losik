"""'주제선율+드럼 도입 → 편성 누적 → 탑노트 합류 → 벌스/코러스 → 하이라이트 → 잔잔한 마무리' 형식 엔진 (2026-09-08).

레퍼런스: 델리스파이스 '차우차우', 스텔라 블레이드 OST '여명' (형식만 차용).
편곡(레이아웃·드럼·베이스·어쿠스틱·패드·스트링·경계 처리)은 공통, 곡별 스펙(키·BPM·진행·주제선율·탑노트·벌스 멜로디)만 다르다.
동일 스펙으로 first-light v1 을 재생성하고, dawnset.py 가 같은 엔진으로 4곡을 더 만든다.

트랙: 0 Drums(SoCal) 1 Bass(Simple Foundation) 2 Lead(Hard Rock, 클린 = 저벨로시티) 3 AcGtr(Acoustic Guitar 스틸)
      4 Strings(Authentic Strings) 5 Pad(Classic Pad, 1도+5도만) 6 LeadHi(Hard Rock 옥타브 탑노트)

레이아웃 (88마디)
  1-8   Intro A   주제선율 + 드럼(킥/스네어만, 햇 없음)                 2겹
  9-16  Intro B   + 베이스 + 어쿠스틱 기타, 햇 합류                      4겹
  17-24 Intro C   + 탑노트(LeadHi) + 스트링 롱                          6겹
  25-32 Verse 1   드럼/베이스/어쿠스틱(팜뮤트) + 벌스 멜로디(낮은 음역)   4겹
  33-40 Chorus 1  주제선율 복귀, 롱 스트럼, 라이드                        5겹
  41-48 Verse 2   + 패드                                                 5겹
  49-56 Chorus 2  + 탑노트 + 스트링                                       7겹
  57-64 Bridge    패드 + 핑거피킹 + 킥 4분 → 61-64 스네어 빌드 + 크래시 롤  2-3겹
  65-76 Highlight 전부 + 스트링 옥타브 더블링 + 오픈햇, 코러스 진행 ×3      7겹
  77-84 Outro A   주제선율 단독(약하게) + 패드                             2겹
  85-88 Outro B   패드 + 어쿠스틱 롱코드 페이드, I 로 종지                  2겹

스펙 dict 필드: sid, title, bpm, keysig, key(pc), verse/chorus/bridge/tail 진행([(root_name, qual)]),
hook/top/verse_mel (8마디 × [(beat, dur, pitch)] 절대 피치), seed.
"""
import os
import sys

from pipeline import PPQ, BAR, E, S, SW, SK_DIR, bt, hum_t, hum_v, seed, build_smf, write_smf
from sketches import mk_chord2, PC

TRACKS = [('Drums', 9), ('Bass', 0), ('Lead', 1), ('AcGtr', 2), ('Strings', 3), ('Pad', 4), ('LeadHi', 5)]
PCS = {0: 0, 1: 33, 2: 26, 3: 25, 4: 50, 5: 89, 6: 26}
N_BARS = 88
DR, BS, LD, AG, ST, PD, HI, ARP = range(8)
MAJOR = [0, 2, 4, 5, 7, 9, 11]

SECTIONS = [(1, 'Intro A'), (9, 'Intro B'), (17, 'Intro C'), (25, 'Verse 1'), (33, 'Chorus 1'), (41, 'Verse 2'),
            (49, 'Chorus 2'), (57, 'Bridge'), (65, 'Highlight'), (77, 'Outro A'), (85, 'Outro B')]
SEC_STARTS = [s for s, _ in SECTIONS]
FILL_BARS = {s - 1 for s in SEC_STARTS if s > 1} - {64}   # 64 는 스네어 빌드가 대신함
K, SN, CH, OH, CR, RIDE, HT, MT, LT = 36, 38, 42, 46, 49, 51, 47, 45, 43

# ---------------------------------------------------------------- first-light (D장조 108) — 절대 피치 스펙
FIRST_LIGHT = dict(
    sid='first-light', title='First Light', bpm=108, keysig=2, key=PC['D'], seed=942,
    verse=[('D', 'M'), ('A', 'M'), ('B', 'm'), ('G', 'M')],
    chorus=[('G', 'M'), ('A', 'M'), ('F#', 'm'), ('B', 'm')],
    bridge=[('B', 'm'), ('G', 'M'), ('D', 'M'), ('A', 'M')],
    tail=[('G', 'M'), ('A', 'M'), ('D', 'M'), ('D', 'M')],
    # 훅 정체성: 1마디 'D–F#–G–A' 상행 모티프
    hook=[
        [(0, .5, 74), (0.5, .5, 78), (1, 1, 79), (2, 2, 81)],
        [(0, .5, 81), (0.5, .5, 79), (1, 1, 78), (2, 2, 76)],
        [(0, .5, 74), (0.5, .5, 78), (1, 1, 79), (2, 1.5, 81), (3.5, .5, 83)],
        [(0, 2, 83), (2, 1, 81), (3, 1, 78)],
        [(0, .5, 74), (0.5, .5, 78), (1, 1, 79), (2, 2, 81)],
        [(0, .5, 81), (0.5, .5, 83), (1, 1, 85), (2, 2, 88)],
        [(0, 1, 86), (1, .5, 85), (1.5, .5, 83), (2, 2, 81)],
        [(0, 3, 78), (3, 1, 81)],
    ],
    top=[[(1, 3, 86)], [(1, 3, 85)], [(1, 3, 85)], [(1, 3, 86)], [(1, 3, 83)], [(1, 3, 93)], [(1, 3, 85)], [(1, 3, 90)]],
    verse_mel=[
        [(0, 1, 66), (1, .5, 69), (1.5, .5, 71), (2, 2, 69)],
        [(0, 1, 73), (1, 1, 71), (2, 2, 69)],
        [(0, 1, 74), (1, .5, 71), (1.5, .5, 69), (2, 2, 66)],
        [(0, 2, 67), (2, 1, 69), (3, 1, 71)],
        [(0, 1, 66), (1, .5, 69), (1.5, .5, 71), (2, 2, 69)],
        [(0, 1, 73), (1, 1, 71), (2, 2, 69)],
        [(0, 1, 74), (1, .5, 71), (1.5, .5, 69), (2, 2, 66)],
        [(0, 1.5, 71), (1.5, .5, 74), (2, 2, 78)],
    ],
)

# ---------------------------------------------------------------- first-light v2 (09-10 판정 반영)
# 판정: 주제부가 동요/트로트처럼 대칭·예측 가능, 드럼 평이, 기타 음역 높고 가늘다.
# 대응: ① 리드 한 옥타브 하향(D4–A5, 기타 5~17프렛) ② 훅 = 'D–D 옥타브 도약 + 반박 늦은 진입' 2마디 프레이즈, 5·6마디에서
#       A5 정점까지 상행 시퀀스 → 7·8마디 해소 (매 마디 롱노트 금지) ③ 드럼 4마디 셀 변주 + 16분 햇 + 고스트 ④ EP 아르페지오 트랙.
FIRST_LIGHT_V2 = dict(
    FIRST_LIGHT, sid='first-light', title='First Light', seed=943, drums='cell', arp=True, tonic=62,
    hook=[
        [(0, .5, 62), (0.5, .5, 74), (1.5, .5, 71), (2, .5, 69), (2.5, 1.5, 67)],
        [(0.5, .5, 69), (1, .5, 71), (1.5, .5, 73), (2.5, 1.5, 76)],
        [(0, .5, 62), (0.5, .5, 74), (1.5, .5, 73), (2, .5, 71), (2.5, 1.5, 69)],
        [(0.5, .5, 71), (1, .5, 74), (1.5, .5, 76), (2.5, 1, 78), (3.5, .5, 74)],
        [(0, .5, 62), (0.5, .5, 74), (1.5, .5, 74), (2, .5, 76), (2.5, 1.5, 79)],
        [(0.5, .5, 78), (1, .5, 76), (1.5, .5, 74), (2.5, 1.5, 81)],
        [(0, .5, 81), (0.5, .5, 78), (1, .5, 76), (1.5, .5, 74), (2, 2, 73)],
        [(0, 1.5, 74), (1.5, .5, 71), (2, 1.5, 66), (3.5, .5, 62)],
    ],
    # 탑노트: 2마디 프레이즈의 뒷마디에만 응답 (리드가 쉬는 자리), 리드 위 3~6도
    top=[
        [], [(2.5, 1.5, 81)],
        [], [(2.5, 1.5, 83)],
        [], [(2.5, 1.5, 85)],
        [(0, 2, 85)], [(0, 1.5, 86), (1.5, 2.5, 83)],
    ],
    # 벌스: 반박 늦게 들어와 상행하는 3음 → 매 마디 끝 방향 전환, 8마디째 D 로 훅의 옥타브 도약을 예비
    verse_mel=[
        [(0.5, .5, 62), (1, .5, 66), (1.5, 1, 69), (3, .5, 66), (3.5, .5, 64)],
        [(0.5, .5, 64), (1, .5, 66), (1.5, 1.5, 69), (3, 1, 61)],
        [(0.5, .5, 62), (1, .5, 66), (1.5, 1, 71), (3, .5, 69), (3.5, .5, 66)],
        [(0.5, .5, 67), (1, .5, 69), (1.5, 1.5, 71), (3, 1, 74)],
        [(0.5, .5, 62), (1, .5, 66), (1.5, 1, 69), (3, .5, 66), (3.5, .5, 64)],
        [(0.5, .5, 64), (1, .5, 66), (1.5, 1.5, 69), (3, 1, 61)],
        [(0.5, .5, 62), (1, .5, 66), (1.5, 1, 71), (3, .5, 69), (3.5, .5, 66)],
        [(0.5, .5, 67), (1, .5, 71), (1.5, 1.5, 74), (3, 1, 62)],
    ],
)
SPECS = {'v1': FIRST_LIGHT, 'v2': FIRST_LIGHT_V2}


def scale_set(key):
    return {(key + i) % 12 for i in MAJOR}


def lead_tonic(key):
    """리드 음역의 으뜸음: D=74, E=76, C=72, A=69, G=67."""
    return 72 + key if key <= 4 else 60 + key


def approach(target, key):
    """다음 근음으로 가는 온음계 어프로치 (반음 어프로치는 golden-hour 에서 거슬림 후보로 지목됨)."""
    return target - 1 if (target - 1) % 12 in scale_set(key) else target - 2


def chord_name(spec, b):
    if 25 <= b <= 32 or 41 <= b <= 48:
        return spec['verse'][(b - 25) % 4]
    if 57 <= b <= 64:
        return spec['bridge'][(b - 57) // 2]
    if 85 <= b <= 88:
        return spec['tail'][b - 85]
    return spec['chorus'][(b - 1) % 4]


def gch(spec, b):
    nm, q = chord_name(spec, b)
    return mk_chord2(PC[nm], q)


def section_of(b):
    return [n for s, n in SECTIONS if s <= b][-1]


def tracks_for(spec):
    """v2 이후 스펙(arp=True)은 8번째 트랙 Arp(Deluxe Classic EP) 를 갖는다. v1 스펙은 7트랙 그대로."""
    if spec.get('arp'):
        return TRACKS + [('Arp', 6)], {**PCS, ARP: 4}
    return TRACKS, PCS


def compose(spec):
    seed(spec['seed'])
    key = spec['key']
    tracks, _ = tracks_for(spec)
    nt = {i: [] for i in range(len(tracks))}
    cc = {i: [] for i in range(len(tracks))}
    ch_of = lambda b: gch(spec, b)

    def g(tr, tick, dur, pitch, vel):
        nt[tr].append((max(0, int(tick)), int(dur), pitch, vel))

    def strum(tr, tick, pitches, dur, vel, spread=14, jitter=6):
        for i, p in enumerate(pitches):
            g(tr, hum_t(tick + i * spread, jitter), max(30, dur - i * spread), p, hum_v(vel, 5))

    # ------------------------------------------------------------ drums
    def drums(b, energy):
        """energy 0: 킥/스네어만  1: +클로즈햇  2: +라이드  3: +오픈햇(하이라이트)"""
        t0 = bt(b)
        fill = b in FILL_BARS
        g(DR, hum_t(t0), 130, K, hum_v(118, 5))
        g(DR, hum_t(bt(b, 2.5)), 110, K, hum_v(102, 6))
        if energy >= 2 and b % 2 == 0:
            g(DR, hum_t(bt(b, 2)), 110, K, hum_v(96))
        for beat in (1, 3):
            if fill and beat == 3:
                continue
            g(DR, hum_t(t0 + beat * PPQ), 130, SN, hum_v(116 if energy else 108, 6))
        if not fill and energy >= 1:
            if b % 2 == 1:
                g(DR, hum_t(bt(b, 1.75)), 80, SN, hum_v(44, 6))
            if b % 4 == 2:
                g(DR, hum_t(bt(b, 3.75)), 80, SN, hum_v(40, 6))
        lim = 5 if fill else 8
        for e8 in range(lim):
            tt = t0 + e8 * E + (SW if e8 % 2 else 0)
            if energy == 1:
                g(DR, hum_t(tt), 55, CH, hum_v(80 if e8 % 2 == 0 else 54, 8))
            elif energy == 2:
                g(DR, hum_t(tt), 70, RIDE, hum_v(86 if e8 % 2 == 0 else 62, 8))
            elif energy == 3:
                g(DR, hum_t(tt), 90, OH if e8 % 2 == 0 else CH, hum_v(96 if e8 % 2 == 0 else 66, 8))
        if fill:
            for i, s16 in enumerate(range(10, 13)):
                g(DR, hum_t(t0 + s16 * S), 90, SN, 72 + i * 12)
            g(DR, hum_t(bt(b, 3.25)), 100, HT, hum_v(104))
            g(DR, hum_t(bt(b, 3.5)), 100, MT, hum_v(110))
            g(DR, hum_t(bt(b, 3.75)), 110, LT, hum_v(116))

    def drums_cell(b, energy):
        """v2: 4마디 셀 '쿵 짝 / 쿵-쿵 짝 / 쿵 짝 짝짝쿵 짝 / 쿵 짝 쿵쿵 짝짝' + 16분 햇 악센트 + 고스트 스네어.
        energy 0: 킥/스네어만  1: 16분 클로즈햇  2: 라이드 8분 + 오프비트 오픈햇  3: 오픈햇 8분(하이라이트)"""
        t0 = bt(b)
        fill = b in FILL_BARS
        cell = (b - 1) % 4
        kicks = {0: [(0, 118), (2, 108)],
                 1: [(0, 118), (0.75, 96), (2.5, 108)],
                 2: [(0, 118), (2.5, 110)],
                 3: [(0, 118), (1.5, 100), (2, 112)]}[cell]
        snares = {0: [(1, 116), (3, 118)],
                  1: [(1, 116), (3, 118)],
                  2: [(1, 116), (2, 104), (2.25, 92), (3, 118)],
                  3: [(1, 116), (3, 118), (3.5, 104)]}[cell]
        if fill:
            snares = [(bt_, v) for bt_, v in snares if bt_ < 2.5]
        for beat, v in kicks:
            g(DR, hum_t(bt(b, beat)), 130, K, hum_v(v, 5))
        for beat, v in snares:
            g(DR, hum_t(bt(b, beat)), 130, SN, hum_v(v, 6))
        if not fill and energy >= 1:
            for beat in (1.75, 3.75):
                g(DR, hum_t(bt(b, beat)), 70, SN, hum_v(38, 6))
        lim = 10 if fill else 16
        for s16 in range(lim):
            tt = t0 + s16 * S
            acc = [96, 56, 74, 60][s16 % 4]
            if energy == 1:
                g(DR, hum_t(tt, 5), 50, CH, hum_v(acc, 6))
            elif energy == 2:
                if s16 % 2 == 0:
                    g(DR, hum_t(tt, 5), 70, RIDE, hum_v(88 if s16 % 4 == 0 else 66, 6))
                elif s16 in (5, 13):
                    g(DR, hum_t(tt, 5), 80, OH, hum_v(84, 6))
            elif energy == 3:
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

    if spec.get('drums') == 'cell':
        drums = drums_cell

    def bridge_drums(b):
        """57-60 킥 4분 약하게, 61-64 스네어 8분 빌드 (벨로시티 램프) + 킥 유지."""
        for beat in range(4):
            g(DR, hum_t(bt(b, beat)), 130, K, hum_v(84 if b < 61 else 100, 5))
        if b >= 61:
            base = 48 + (b - 61) * 16
            for e8 in range(8):
                g(DR, hum_t(bt(b) + e8 * E), 80, SN, min(120, base + e8 * 2))
            if b == 64:
                for s16 in range(8, 16):
                    g(DR, hum_t(bt(b) + s16 * S), 60, SN, min(124, 96 + (s16 - 8) * 4))

    # ------------------------------------------------------------ bass
    def bass(b, style):
        ch = ch_of(b)
        r = ch['bass']
        f5 = r + 7
        nxt = ch_of(b + 1)['bass'] if b < N_BARS else r
        if style == 'groove':
            g(BS, hum_t(bt(b)), int(1.4 * PPQ), r, hum_v(100, 5))
            g(BS, hum_t(bt(b, 1.5)), int(.4 * PPQ), r, hum_v(82, 5))
            g(BS, hum_t(bt(b, 2)), int(.9 * PPQ), f5, hum_v(92, 5))
            g(BS, hum_t(bt(b, 3)), int(.45 * PPQ), r, hum_v(86, 5))
            g(BS, hum_t(bt(b, 3.5)), int(.45 * PPQ), approach(nxt, key), hum_v(88, 5))
        elif style == 'drive':
            seq = [r, r, f5, r, r + 12, f5, r, approach(nxt, key)]
            for e8 in range(8):
                g(BS, hum_t(bt(b) + e8 * E), 200, seq[e8], hum_v(96 if e8 in (0, 4) else 82, 5))
        elif style == 'half':
            g(BS, bt(b), PPQ * 2 - 60, r, 88)
            g(BS, bt(b, 2), PPQ * 2 - 60, f5, 78)
        elif style == 'hold':
            g(BS, bt(b), BAR - 100, r, 80)

    # ------------------------------------------------------------ acoustic guitar
    def ac_guitar(b, style, vel=72):
        ch = ch_of(b)
        v = ch['stab'] + [ch['r4'] + 12]
        if style == 'mute':      # 팜뮤트 8분 스트럼: 짧은 음, 1·2.5박 악센트, 스윙
            for e8 in range(8):
                tt = bt(b) + e8 * E + (SW if e8 % 2 else 0)
                acc = e8 in (0, 5)
                strum(AG, tt, v[:3], 120 if acc else 90, vel + (8 if acc else -6), spread=8)
        elif style == 'long':    # 롱 스트럼 1박 + 2.5박 푸시
            strum(AG, bt(b), v, int(2.3 * PPQ), vel)
            strum(AG, bt(b, 2.5), v, int(1.4 * PPQ), vel - 6)
        elif style == 'pick':    # 핑거피킹 8분 아르페지오
            seq = [v[0], v[2], v[3], v[1], v[3], v[2], v[3], v[1]]
            for e8 in range(8):
                g(AG, hum_t(bt(b) + e8 * E, 10), 300, seq[e8], hum_v(vel - 10, 6))
        elif style == 'hold':
            strum(AG, bt(b), v, BAR - 60, vel, spread=24)

    # ------------------------------------------------------------ pad / strings
    def pad(b, vel=54):
        r4 = ch_of(b)['r4']
        for p in (r4 - 12, r4 - 5):
            g(PD, bt(b), BAR - 30, p, vel)

    def arp(b, vel=62, high=False):
        """v2: EP 8분 아르페지오 — 1·3·5·옥타브 상행-하행 궤적, 벌스/Intro C/하이라이트에서 상시 움직임."""
        if not spec.get('arp'):
            return
        a = ch_of(b)['arp']
        seq = [a[0], a[1], a[2], a[0] + 12, a[2], a[1], a[0] + 12, a[2]]
        for e8 in range(8):
            g(ARP, hum_t(bt(b) + e8 * E, 8), 220, seq[e8] + (12 if high else 0), hum_v(vel if e8 % 2 == 0 else vel - 10, 5))

    def strings(b, mode, vel=56):
        ch = ch_of(b)
        r4, th, f5 = ch['r4'], ch['r4'] + ch['third'], ch['r4'] + 7
        if mode == 'low':
            for p in (r4, f5):
                g(ST, bt(b), BAR - 30, p, vel)
        elif mode == 'mid':
            for p in (r4, th, f5):
                g(ST, bt(b), BAR - 30, p, vel)
        elif mode == 'high':
            for p in (th + 12, f5 + 12, r4 + 24):
                g(ST, bt(b), BAR - 30, p, vel)

    # ------------------------------------------------------------ melodies
    def line(tr, start, bars, vel=100, jitter=6):
        for i, bar in enumerate(bars):
            for beat, dur, p in bar:
                g(tr, hum_t(bt(start + i, beat), jitter), int(dur * PPQ) - 30, p, hum_v(vel, 6))

    # ============================================================ arrangement
    for b in range(1, N_BARS + 1):
        sec = section_of(b)
        if sec == 'Intro A':
            drums(b, 0)
        elif sec == 'Intro B':
            drums(b, 1); bass(b, 'groove'); ac_guitar(b, 'long', 68)
        elif sec == 'Intro C':
            drums(b, 1); bass(b, 'groove'); ac_guitar(b, 'long', 72); strings(b, 'low', 52); arp(b, 58)
        elif sec == 'Verse 1':
            drums(b, 1); bass(b, 'groove'); ac_guitar(b, 'mute', 70); arp(b, 64)
        elif sec == 'Chorus 1':
            drums(b, 2); bass(b, 'drive'); ac_guitar(b, 'long', 78)
        elif sec == 'Verse 2':
            drums(b, 1); bass(b, 'groove'); ac_guitar(b, 'mute', 72); pad(b, 50); arp(b, 66)
        elif sec == 'Chorus 2':
            drums(b, 2); bass(b, 'drive'); ac_guitar(b, 'long', 80); strings(b, 'mid', 58); pad(b, 48); arp(b, 60, high=True)
        elif sec == 'Bridge':
            bridge_drums(b); bass(b, 'half'); ac_guitar(b, 'pick', 66); pad(b, 56)
            if b >= 61:
                strings(b, 'mid', 48 + (b - 61) * 6)
        elif sec == 'Highlight':
            drums(b, 3); bass(b, 'drive'); ac_guitar(b, 'long', 84); strings(b, 'high', 64); pad(b, 52); arp(b, 68, high=True)
        elif sec == 'Outro A':
            pad(b, 50)
            if b >= 81:
                ac_guitar(b, 'hold', 56)
        elif sec == 'Outro B':
            fade = 52 - (b - 85) * 8
            pad(b, fade); ac_guitar(b, 'hold', fade + 4); bass(b, 'hold')

    hook, top, vmel = spec['hook'], spec['top'], spec['verse_mel']
    # 주제선율: 인트로 3회, 코러스 2회, 하이라이트 1.5회, 아웃트로 1회(약하게)
    line(LD, 1, hook, vel=92)
    line(LD, 9, hook, vel=96)
    line(LD, 17, hook, vel=100)
    line(LD, 33, hook, vel=104)
    line(LD, 49, hook, vel=106)
    line(LD, 65, hook, vel=110)
    line(LD, 73, hook[:4], vel=112)
    line(LD, 77, hook, vel=70, jitter=10)
    # 벌스 멜로디 (낮은 음역)
    line(LD, 25, vmel, vel=84)
    line(LD, 41, vmel, vel=88)
    # 탑노트: Intro C 합류, Chorus 2, Highlight
    line(HI, 17, top, vel=74)
    line(HI, 49, top, vel=84)
    line(HI, 65, top, vel=92)
    line(HI, 73, top[:4], vel=94)
    # 하이라이트 마지막 마디(76): 5도→옥타브 던지고 크래시로 마무리
    tonic = spec.get('tonic', lead_tonic(key))
    g(LD, bt(76, 2), PPQ - 30, tonic + 7, 112)
    g(LD, bt(76, 3), PPQ - 30, tonic + 12, 114)
    # 마지막 종지: 으뜸음 롱노트
    g(LD, bt(85), BAR * 2 - 60, tonic, 66)
    g(LD, bt(87), BAR * 2 - 60, tonic, 58)

    # 섹션 경계: 크래시 롤 라이저(2마디) + 임팩트. Highlight 진입은 4마디 롤.
    for s in SEC_STARTS[1:]:
        roll_bars = 4 if s == 65 else 2
        n = roll_bars * 8
        lo, hi = (34, 118) if s == 65 else (34, 112)
        for k in range(n):
            g(DR, hum_t(bt(s - roll_bars) + k * E, 6), 200, CR, lo + int(k * (hi - lo) / (n - 1)))
        g(DR, bt(s), PPQ, CR, 124 if s == 65 else 120)
    for b in range(65, 77, 2):   # 하이라이트: 2마디마다 크래시
        g(DR, bt(b), PPQ, CR, 108)
    g(DR, bt(77), PPQ * 2, CR, 100)   # 하이라이트 종결 크래시 (아웃트로 진입)
    return nt, cc


def check(spec, nt):
    """자기검증: 다이어토닉 이탈 / 리드-탑노트 단2도 동시발음 / 리드 롱노트(≥1.5박)의 코드톤 여부 / 음역."""
    scale = scale_set(spec['key'])
    bad = [(tr, t, p) for tr in nt if tr != DR for t, d, p, v in nt[tr] if p % 12 not in scale]
    clashes = []
    for t1, d1, p1, _ in nt[LD]:
        for t2, d2, p2, _ in nt[HI]:
            if t1 < t2 + d2 and t2 < t1 + d1 and abs(p1 - p2) % 12 == 1:
                clashes.append((t1 // BAR + 1, p1, p2))
    nonchord = []
    for t, d, p, _ in nt[LD] + nt[HI]:
        if d >= 1.5 * PPQ - 40:
            b = (t + 60) // BAR + 1          # 휴머나이즈 지터(≤10틱)로 마디 앞으로 밀린 다운비트 보정
            ch = gch(spec, min(b, N_BARS))
            root = ch['bass'] % 12
            tones = {x % 12 for x in ch['stab']} | {(root + 2) % 12}          # add9 허용
            tones.add((root + (5 if ch['third'] == 3 else 11)) % 12)          # 마이너 11th(sus) / 메이저 maj7 허용
            if p % 12 not in tones:
                nonchord.append((b, p))
    rng = {tr: (min(p for _, _, p, _ in nt[tr]), max(p for _, _, p, _ in nt[tr])) for tr in nt if nt[tr]}
    return bad, clashes, nonchord, rng


def render(spec, out=None):
    nt, cc = compose(spec)
    bad, clashes, nonchord, rng = check(spec, nt)
    assert not bad, (spec['sid'], 'non-diatonic', bad[:5])
    assert not clashes, (spec['sid'], 'lead/top m2', clashes[:5])
    assert not nonchord, (spec['sid'], 'long non-chord tone', nonchord[:8])
    tracks, pcs = tracks_for(spec)
    smf = build_smf(spec['title'], spec['bpm'], spec['keysig'], False, N_BARS, tracks, pcs, nt, cc, markers=SECTIONS)
    out = out or os.path.join(SK_DIR, f"{spec['sid']}.mid")
    return write_smf(out, smf), rng


if __name__ == '__main__':
    ver = sys.argv[1] if len(sys.argv) > 1 else 'v2'
    s = SPECS[ver]
    msg, rng = render(s, os.path.join(SK_DIR, f"{s['sid']}{'' if ver == 'v1' else '-' + ver}.mid"))
    print(msg)
    print('range', rng)
