"""Rebetiko 5 버전 v2 (2026-09-19). v1 판정 "그리스가 아니라 이스탄불/알라딘" → 선율 문법 전면 교체.

v1 → v2 변경 (FEEDBACK_LOG 09-19)
- 선율 문법: 음계 순차진행+턴 장식(마캄 타크심 문법) → **코드톤 아르페지오 + 반복음 + 3도 도약**, 종지는 V(장3화음)→I.
  선율 표의 모든 음이 그 마디 화음의 구성음이거나 인접 경과음 하나.
- 1번 드로모스: Hitzaz(증2도 = Misirlou 색) → **Minore**(화성단조 D E F G A Bb C#, 하행 C 허용). Vamvakaris·Batis 레퍼런스와 일치.
- 트레몰로: 3박 이상 전부 → **마디 마지막 롱톤에만**. 나머지는 단타.
- taximi: 1번 3→2마디, 3번 유지(스미르나는 그 색이 맞음), 4번 8→4마디.
- 3번 드럼: 프레임드럼 둠텍 → Tough Kit(PC 16, 드럼 채널 실측). v2 붐뱁(스윙 햇·고스트 킥) → v3 **올드스쿨 정박**: 킥 1·3 + 마디 셀별 변주(2&·3&·4&), 스네어 2·4 최전면, 스트레이트 8분 햇.

공통 규약
- 토닉 D(62). 선율은 드로모스 도수(0=토닉, 7=옥타브 위, 음수=아래)로 표기 → deg_pitch().
- 프레이즈 표: 마디 리스트, 마디 = [(시작 8분음 위치, 길이(8분음), 도수)]. 마디 마지막 음이 TREM_MIN 이상이면 트레몰로.
- 부주키(트리코르도 D-A-D): 선율을 한 옥타브 아래로 약하게 더블링 (1·4번).
- 패치(09-19 스트립 실측): 부주키·바글라마스 PC 25(Acoustic Guitar), 기타·우드 PC 24(Classical Acoustic Guitar),
  산투리 PC 46(Space Harp), 바이올린 PC 110(Authentic Strings; 40·41·42·44 는 GM 폴백), 아코디언 PC 21(Cheap Organ; 전용 패치 없음),
  손북 = SoCal(PC 0) 로우 플로어탐(둠 41)·사이드스틱(텍 37)·탬버린(54), 붐뱁 = Tough Kit(PC 16).
- 박자·템포맵은 build_smf(timesig=, tempos=) 로.
"""
import os

from pipeline import PPQ, E, S, SK_DIR, hum_t, hum_v, seed, build_smf, write_smf

VER = 'v2'
TONIC = 62
TREM_MIN = 3   # 8분음 단위, 마디 마지막 음에만 적용
DROMOI = {
    'minore':     [0, 2, 3, 5, 7, 8, 11],   # D E F G A Bb C#  (하행 C 허용)
    'kiourdi':    [0, 2, 3, 5, 7, 8, 10],   # D E F G A Bb C   (종지 C# 허용)
    'rast':       [0, 2, 4, 5, 7, 9, 11],   # D E F# G A B C#  (하행 C 허용)
    'hitzazkiar': [0, 1, 4, 5, 7, 8, 11],   # D Eb F# G A Bb C#
    'sabah':      [0, 2, 3, 4, 7, 8, 10],   # D E F Gb A Bb C
}
EXTRA = {'minore': {10}, 'kiourdi': {11}, 'rast': {10}}   # 토닉 기준 반음 오프셋: 관용적으로 허용되는 음계 밖 음
K, SN, SS, LFT, LT, TAMB, CH_, OH, RIDE, CR = 36, 38, 37, 41, 45, 54, 42, 46, 51, 49
DOUM, TEK = LFT, SS
L = 100   # 특수 토큰: 음계 밖 리딩톤(C#, 61) — kiourdi 전용


def deg_pitch(scale, deg, base=TONIC):
    return base + 12 * (deg // 7) + scale[deg % 7]


class Song:
    def __init__(self, sid, title, bpm, dromos, timesig, tracks, pcs, keysig, minor, rng_seed):
        self.sid, self.title, self.bpm, self.timesig = sid, title, bpm, timesig
        self.scale = DROMOI[dromos]
        self.allowed = set(DROMOI[dromos]) | EXTRA.get(dromos, set())
        self.tracks, self.pcs, self.keysig, self.minor = tracks, pcs, keysig, minor
        self.bar_ticks = timesig[0] * (PPQ * 4 // timesig[1])
        self.nt = {i: [] for i in range(len(tracks))}
        self.tempos, self.markers = [], []
        self.drum_tr = next((i for i, (_, ch) in enumerate(tracks) if ch == 9), None)
        self.ver = VER
        seed(rng_seed)

    def t(self, bar, e8=0.0):
        return (bar - 1) * self.bar_ticks + int(e8 * E)

    def g(self, tr, tick, dur, pitch, vel):
        self.nt[tr].append((max(0, int(tick)), max(20, int(dur)), pitch, max(1, min(127, vel))))

    def p(self, deg, oct_shift=0):
        if deg == L:
            return 61 + 12 * oct_shift
        return deg_pitch(self.scale, deg) + 12 * oct_shift

    def trem(self, tr, tick, dur, pitch, vel, unit=S):
        n = max(1, int(dur) // unit)
        for i in range(n):
            self.g(tr, hum_t(tick + i * unit, 3), unit - 25, pitch, hum_v(vel - (0 if i % 2 == 0 else 9), 4))

    def note(self, tr, tick, dur_t, pitch, vel, trem, double_low):
        if trem:
            self.trem(tr, tick, dur_t, pitch, vel)
            if double_low:
                self.trem(tr, tick, dur_t, pitch - 12, vel - 22)
        else:
            self.g(tr, tick, dur_t - 30, pitch, vel)
            if double_low:
                self.g(tr, tick, dur_t - 30, pitch - 12, vel - 22)

    def phrase(self, tr, bar0, bars, vel=96, oct_shift=0, double_low=False, trem=True, jit=6, slide=False):
        """도수표 프레이즈 렌더. 트레몰로는 마디 마지막 음이 TREM_MIN 이상일 때만."""
        for i, bar in enumerate(bars):
            last_e8 = max(e8 for e8, _, _ in bar)
            for e8, dur, deg in bar:
                tick = hum_t(self.t(bar0 + i, e8), jit)
                dur_t = int(dur * E)
                pitch = self.p(deg, oct_shift)
                v = hum_v(vel + (6 if e8 == 0 else 0), 5)
                if slide and dur >= 2:   # 온음계 아래 이웃음에서 미끄러져 올라옴
                    self.g(tr, tick - S // 2, S // 2 - 10, self.p(deg - 1, oct_shift), v - 20)
                self.note(tr, tick, dur_t, pitch, v, trem and e8 == last_e8 and dur >= TREM_MIN, double_low)

    def free(self, tr, ticks, vel=90, double_low=False):
        """무박 taximi: [(tick, dur, deg)] 절대 틱 배치. 3박 이상 롱톤만 트레몰로."""
        for tick, dur, deg in ticks:
            self.note(tr, tick, dur, self.p(deg), hum_v(vel, 6), dur >= S * 6, double_low)

    def check(self):
        bad = [(tr, t, p) for tr in self.nt if tr != self.drum_tr for t, d, p, v in self.nt[tr]
               if (p - TONIC) % 12 not in self.allowed]
        rng = {self.tracks[tr][0]: (min(p for _, _, p, _ in v), max(p for _, _, p, _ in v)) for tr, v in self.nt.items() if v}
        return bad, rng

    def render(self, n_bars):
        bad, rng = self.check()
        assert not bad, (self.sid, bad[:6])
        smf = build_smf(self.title, self.bpm, self.keysig, self.minor, n_bars, self.tracks, self.pcs, self.nt, {},
                        markers=self.markers, timesig=self.timesig, tempos=self.tempos)
        print(write_smf(os.path.join(SK_DIR, f'rebetiko-{self.sid}-{self.ver}.mid'), smf))
        print('  range', rng)


# =============================================================== 1. piraeus — Minore zeibekiko 9/8
def piraeus():
    s = Song('1-piraeus', 'Piraeus Zeibekiko', 66, 'minore', (9, 8),
             [('FrameDrum', 9), ('Guitar', 0), ('Bouzouki', 1), ('Baglamas', 2)], {0: 0, 1: 24, 2: 25, 3: 25}, -1, True, 1001)
    DR, GT, BZ, BG = range(4)
    # 화음: 이름 → (베이스 근음, 코드톤). Minore: Dm, Gm, A(장), Bb
    CH = {'Dm': (38, [50, 53, 57]), 'Gm': (43, [55, 58, 62]), 'A': (45, [57, 61, 64]), 'Bb': (46, [58, 62, 65])}
    VERSE_CH = ['Dm', 'Dm', 'Gm', 'A', 'Dm', 'Gm', 'A', 'Dm']
    INTER_CH = ['Gm', 'Gm', 'Dm', 'Dm', 'Bb', 'Gm', 'A', 'Dm']

    # taximi 2마디(48bpm): Dm 코드톤에 닻 — D F A D' A F E D
    T0 = s.t(1)
    taximi = [(T0 + 200, 500, 0), (T0 + 800, 400, 2), (T0 + 1300, 700, 4), (T0 + 2100, 1100, 7),
              (T0 + 3300, 400, 4), (T0 + 3800, 400, 2), (T0 + 4300, 300, 1), (T0 + 4700, 1500, 0)]
    s.free(BZ, taximi, vel=88, double_low=True)
    s.tempos = [(0, 48), (s.t(3), 66)]
    # 도수: 0 D, 1 E, 2 F, 3 G, 4 A, 5 Bb, 6 C#, 7 D', 8 E', 9 F', 10 G', 11 A', 12 Bb'
    VERSE = [
        [(0, 2, 4), (2, 1, 4), (3, 1, 2), (4, 2, 4), (6, 3, 2)],
        [(0, 1, 2), (1, 1, 2), (2, 1, 0), (3, 1, 2), (4, 2, 4), (6, 3, 0)],
        [(0, 2, 5), (2, 1, 5), (3, 1, 3), (4, 2, 7), (6, 3, 5)],
        [(0, 1, 6), (1, 1, 6), (2, 1, 4), (3, 1, 6), (4, 2, 8), (6, 3, 6)],
        [(0, 2, 7), (2, 1, 7), (3, 1, 9), (4, 2, 7), (6, 3, 4)],
        [(0, 1, 7), (1, 1, 5), (2, 1, 3), (3, 1, 5), (4, 2, 7), (6, 3, 5)],
        [(0, 2, 8), (2, 1, 6), (3, 1, 4), (4, 2, 6), (6, 2, 4), (8, 1, 6)],
        [(0, 1, 0), (1, 1, 0), (2, 2, 0), (4, 5, 0)],
    ]
    INTER = [
        [(0, .5, 7), (.5, .5, 9), (1, .5, 10), (1.5, .5, 9), (2, 1, 7), (3, 1, 5), (4, 2, 7), (6, 3, 5)],
        [(0, 1, 5), (1, 1, 5), (2, 1, 7), (3, 1, 5), (4, 2, 3), (6, 3, 5)],
        [(0, .5, 7), (.5, .5, 9), (1, .5, 11), (1.5, .5, 9), (2, 1, 7), (3, 1, 9), (4, 2, 11), (6, 3, 9)],
        [(0, 1, 9), (1, 1, 7), (2, 1, 4), (3, 1, 7), (4, 2, 9), (6, 3, 7)],
        [(0, .5, 9), (.5, .5, 7), (1, .5, 5), (1.5, .5, 7), (2, 1, 9), (3, 1, 7), (4, 2, 12), (6, 3, 9)],
        [(0, 1, 10), (1, 1, 7), (2, 1, 5), (3, 1, 7), (4, 2, 10), (6, 3, 7)],
        [(0, .5, 8), (.5, .5, 6), (1, .5, 4), (1.5, .5, 6), (2, 1, 8), (3, 1, 6), (4, 2, 4), (6, 2, 6), (8, 1, 8)],
        [(0, 1, 7), (1, 1, 7), (2, 2, 7), (4, 5, 7)],
    ]

    def guitar(b, name, vel=84):
        root, tones = CH[name]
        # 2+2+2+3: 베이스 0,2,4,6 (근음/5도 교대) · 코드 1,3,5,7 · 마지막 3 (6,7,8) 에 무게
        for e8 in (0, 2, 4, 6):
            bass = root if e8 in (0, 4) else root + 7
            s.g(GT, hum_t(s.t(b, e8), 5), int(1.4 * E), bass, hum_v(vel + (8 if e8 == 6 else 0), 5))
        for e8 in (1, 3, 5, 7, 8):
            v = vel - 14 + (14 if e8 == 8 else 0) + (6 if e8 == 7 else 0)
            for k, pch in enumerate(tones):
                s.g(GT, hum_t(s.t(b, e8) + k * 12, 4), int(.8 * E), pch, hum_v(v, 5))

    def frame(b, vel=62):
        s.g(DR, hum_t(s.t(b, 0)), 120, DOUM, hum_v(vel + 10, 5))
        s.g(DR, hum_t(s.t(b, 3)), 90, TEK, hum_v(vel - 8, 5))
        s.g(DR, hum_t(s.t(b, 4)), 120, DOUM, hum_v(vel, 5))
        s.g(DR, hum_t(s.t(b, 6)), 120, DOUM, hum_v(vel + 4, 5))
        s.g(DR, hum_t(s.t(b, 8)), 90, TEK, hum_v(vel + 12, 5))

    def baglamas(b, name, vel=52):
        tones = CH[name][1]
        for e8 in range(9):
            pch = tones[(e8 // 2) % 3] + 24
            s.trem(BG, s.t(b, e8), E, pch, vel + (8 if e8 in (0, 4, 6) else 0), unit=S)

    # 구조: taximi 1-2 | 픽업 3 | 벌스 4-11 | 간주 12-19 | 벌스 20-27 | 코다 28-29
    s.markers = [(1, 'taximi'), (3, 'pickup'), (4, 'verse'), (12, 'bouzouki interlude'), (20, 'verse 2'), (28, 'coda')]
    guitar(3, 'Dm', vel=76)
    for i, nm in enumerate(VERSE_CH):
        guitar(4 + i, nm); frame(4 + i); baglamas(4 + i, nm)
        guitar(20 + i, nm, vel=88); frame(20 + i, vel=68); baglamas(20 + i, nm, vel=58)
    for i, nm in enumerate(INTER_CH):
        guitar(12 + i, nm, vel=80); frame(12 + i, vel=56); baglamas(12 + i, nm, vel=48)
    s.phrase(BZ, 4, VERSE, vel=96, double_low=True)
    s.phrase(BZ, 12, INTER, vel=100, double_low=True, jit=4)
    s.phrase(BZ, 20, VERSE, vel=102, double_low=True)
    # 코다: A → Dm 종지. 부주키 A 코드 하행 아르페지오 → D 롱톤
    guitar(28, 'A', vel=80)
    s.g(GT, s.t(29, 0), s.bar_ticks - 100, 38, 84)
    for k, pch in enumerate(CH['Dm'][1]):
        s.g(GT, s.t(29, 0) + k * 20, s.bar_ticks - 200, pch, 76)
    s.free(BZ, [(s.t(28, 0), E, 8), (s.t(28, 1), E, 6), (s.t(28, 2), E, 4), (s.t(28, 3), E, 6), (s.t(28, 4), 2 * E, 4),
                (s.t(28, 6), 3 * E, 6), (s.t(29, 0), s.bar_ticks - 200, 7)], vel=96, double_low=True)
    s.g(DR, s.t(29, 0), 200, DOUM, 84)
    s.render(29)


# =============================================================== 2. hasapiko — Kiourdi 2/4, twin bouzouki
def hasapiko():
    s = Song('2-hasapiko', 'Hasapiko Synnefia', 80, 'kiourdi', (2, 4),
             [('Guitar', 0), ('Bouzouki1', 1), ('Bouzouki2', 2), ('Accordion', 3)], {0: 24, 1: 25, 2: 25, 3: 21}, -1, True, 1002)
    GT, B1, B2, AC = range(4)
    CH = {'Dm': (38, [50, 53, 57]), 'Gm': (43, [55, 58, 62]), 'C': (36, [48, 52, 55]), 'F': (41, [53, 57, 60]),
          'A': (45, [57, 61, 64]), 'Bb': (46, [58, 62, 65])}
    A_CH = ['Dm', 'Dm', 'Gm', 'Gm', 'C', 'C', 'F', 'F', 'Dm', 'Dm', 'Gm', 'A', 'Dm', 'Gm', 'A', 'Dm']
    B_CH = ['Gm', 'Gm', 'Dm', 'Dm', 'Bb', 'Bb', 'A', 'Dm']
    # 도수: 0 D, 1 E, 2 F, 3 G, 4 A, 5 Bb, 6 C, 7 D', 8 E', 9 F', 10 G'. L = C#
    # 코드톤: Dm 0·2·4 / Gm 3·5·7 / C 6·8·10 / F 2·4·6 / A 4·L·8 / Bb 5·7·9
    A = [
        [(0, 1, 4), (1, 1, 4), (2, 1, 2), (3, 1, 4)], [(0, 2, 2), (2, 2, 0)],
        [(0, 1, 5), (1, 1, 5), (2, 1, 3), (3, 1, 5)], [(0, 4, 7)],
        [(0, 1, 8), (1, 1, 8), (2, 1, 6), (3, 1, 8)], [(0, 2, 10), (2, 2, 8)],
        [(0, 1, 6), (1, 1, 4), (2, 1, 2), (3, 1, 4)], [(0, 4, 6)],
        [(0, 1, 7), (1, 1, 7), (2, 1, 4), (3, 1, 7)], [(0, 2, 9), (2, 2, 7)],
        [(0, 1, 7), (1, 1, 5), (2, 1, 3), (3, 1, 5)], [(0, 2, 4), (2, 2, L)],
        [(0, 1, 4), (1, 1, 4), (2, 1, 2), (3, 1, 4)], [(0, 1, 5), (1, 1, 3), (2, 2, 5)],
        [(0, 1, L), (1, 1, 8), (2, 1, L), (3, 1, 4)], [(0, 4, 0)],
    ]
    B = [
        [(0, .5, 7), (.5, .5, 10), (1, 1, 7), (2, 2, 5)], [(0, 1, 3), (1, 1, 5), (2, 2, 7)],
        [(0, .5, 9), (.5, .5, 7), (1, 1, 4), (2, 2, 7)], [(0, 4, 4)],
        [(0, 1, 9), (1, 1, 9), (2, 1, 7), (3, 1, 5)], [(0, 2, 7), (2, 2, 9)],
        [(0, 1, 8), (1, 1, L), (2, 1, 4), (3, 1, L)], [(0, 4, 0)],
    ]

    def third_below(deg):
        return 4 - 7 if deg == L else deg - 2     # C# → A (장3도 아래)

    def twin(bar0, bars, vel, oct_shift=0, solo=False):
        for i, bar in enumerate(bars):
            last_e8 = max(e8 for e8, _, _ in bar)
            for e8, dur, deg in bar:
                tick = hum_t(s.t(bar0 + i, e8), 6)
                d = int(dur * E)
                voices = [(B1, s.p(deg, oct_shift), vel)]
                if not solo:
                    voices.append((B2, s.p(third_below(deg), oct_shift), vel - 12))
                for tr, pp, vv in voices:
                    if e8 == last_e8 and dur >= TREM_MIN:
                        s.trem(tr, tick, d, pp, vv)
                    else:
                        s.g(tr, tick + (8 if tr == B2 else 0), d - 30, pp, hum_v(vv + (6 if e8 == 0 else 0), 5))

    def guitar(b, name, vel=80):
        root, tones = CH[name]
        s.g(GT, hum_t(s.t(b, 0), 5), int(.9 * E), root, hum_v(vel, 5))
        s.g(GT, hum_t(s.t(b, 2), 5), int(.9 * E), root + 7 if root + 7 < 50 else root - 5, hum_v(vel - 6, 5))
        for e8 in (1, 3):
            for k, pch in enumerate(tones):
                s.g(GT, hum_t(s.t(b, e8) + k * 10, 4), int(.7 * E), pch, hum_v(vel - 18, 5))

    def accordion(b, name, vel=58):
        for pch in CH[name][1]:
            s.g(AC, s.t(b, 0) + 30, s.bar_ticks - 80, pch + 12, hum_v(vel, 4))

    s.markers = [(1, 'intro'), (9, 'verse A'), (25, 'interlude B'), (33, 'verse A2 +accordion'), (49, 'interlude B2'), (57, 'outro')]
    for i, nm in enumerate(B_CH):
        guitar(1 + i, nm, vel=72); guitar(25 + i, nm); guitar(49 + i, nm, vel=86); accordion(49 + i, nm)
    for i, nm in enumerate(A_CH):
        guitar(9 + i, nm); guitar(33 + i, nm, vel=86); accordion(33 + i, nm)
    twin(1, B, 84, solo=True)
    twin(9, A, 94)
    twin(25, B, 98)
    twin(33, A, 100)
    twin(49, B, 102, oct_shift=1)
    for i, nm in enumerate(['Dm', 'Gm', 'A', 'Dm', 'Dm', 'Dm', 'Dm', 'Dm']):
        guitar(57 + i, nm, vel=78 - i * 4)
        accordion(57 + i, nm, vel=52 - i * 3)
    twin(57, A[12:16], 92)
    for tr, pp in ((B1, 74), (B2, 69)):
        s.trem(tr, s.t(61, 0), s.bar_ticks * 3, pp, 78)
        s.g(tr, s.t(64, 0), s.bar_ticks - 100, pp - 12, 84)
    s.render(64)


# =============================================================== 3. smyrna — Hitzazkiar tsifteteli 4/4, boom-bap kit
def smyrna():
    s = Song('3-smyrna', 'Smyrna Tsifteteli', 100, 'hitzazkiar', (4, 4),
             [('Drums', 9), ('Oud', 0), ('Santouri', 1), ('Violin', 2)], {0: 16, 1: 24, 2: 46, 3: 110}, 2, False, 1003)
    DR, OD, SA, VN = range(4)
    s.ver = 'v3'   # 드럼만 v2 → v3 (올드스쿨 정박)
    CH = {'D': (38, [50, 54, 57]), 'Gm': (43, [55, 58, 62]), 'A': (45, [57, 61])}   # Hitzazkiar: A 는 3도 다이어드
    VERSE_CH = ['D', 'D', 'Gm', 'D', 'D', 'Gm', 'A', 'D']
    SOLO_CH = ['Gm', 'Gm', 'D', 'D', 'A', 'A', 'D', 'D']
    VERSE = [
        [(0, 3, 0), (3, 1, 1), (4, 2, 2), (6, 2, 1)],
        [(0, 2, 0), (2, 1, 1), (3, 1, 0), (4, 4, -1)],
        [(0, 2, 3), (2, 2, 4), (4, 2, 5), (6, 2, 4)],
        [(0, 1, 3), (1, 1, 2), (2, 2, 1), (4, 4, 0)],
        [(0, 2, 4), (2, 2, 5), (4, 2, 6), (6, 2, 7)],
        [(0, 3, 5), (3, 1, 4), (4, 2, 3), (6, 2, 4)],
        [(0, 2, 2), (2, 2, 1), (4, 2, -1), (6, 2, 1)],
        [(0, 8, 0)],
    ]
    SOLO = [
        [(0, .5, 7), (.5, .5, 8), (1, 1, 7), (2, 2, 5), (4, 2, 4), (6, 2, 5)],
        [(0, 1, 6), (1, 1, 5), (2, 1, 4), (3, 1, 3), (4, 4, 4)],
        [(0, 1, 9), (1, .5, 8), (1.5, .5, 7), (2, 2, 8), (4, 2, 7), (6, 2, 6)],
        [(0, 2, 5), (2, 1, 4), (3, 1, 3), (4, 4, 2)],
        [(0, .5, 6), (.5, .5, 7), (1, 1, 6), (2, 2, 4), (4, 2, 6), (6, 2, 4)],
        [(0, 1, 5), (1, 1, 4), (2, 2, 3), (4, 4, 1)],
        [(0, 1, 2), (1, 1, 3), (2, 1, 4), (3, 1, 5), (4, 1, 4), (5, 1, 3), (6, 1, 2), (7, 1, 1)],
        [(0, 8, 0)],
    ]
    T0 = s.t(1)
    taximi = [(T0 + 300, 900, 4), (T0 + 1300, 400, 5), (T0 + 1700, 1700, 4), (T0 + 3500, 350, 3), (T0 + 3850, 350, 2),
              (T0 + 4200, 1600, 1), (T0 + 6000, 600, 0), (T0 + 6700, 300, -1), (T0 + 7000, 300, 0), (T0 + 7300, 300, 1),
              (T0 + 7600, 300, 2), (T0 + 7900, 300, 3), (T0 + 8200, 1800, 4), (T0 + 10200, 450, 6), (T0 + 10650, 450, 5),
              (T0 + 11100, 450, 4), (T0 + 11550, 450, 3), (T0 + 12000, 700, 2), (T0 + 12800, 400, 1), (T0 + 13200, 2000, 0)]
    s.free(VN, taximi, vel=86)
    s.tempos = [(0, 72), (s.t(5), 100)]

    def beat(b, vel=100, fill=False, open_hat=False):
        # 올드스쿨 정박: 킥 1·3 기본 + 4마디 셀 변주 / 스네어 2·4 (최전면) / 스트레이트 8분 햇 (스윙 없음) / 짝수 마디 4& 오픈햇 / 필인 = 4박 스네어 2타
        cell = (b - 1) % 4
        kicks = {0: [(0, 12), (4, 4)], 1: [(0, 12), (3, -6), (4, 4)], 2: [(0, 12), (4, 4), (5, -10)], 3: [(0, 12), (4, 4), (7, -4)]}[cell]
        for e8, off in kicks:
            s.g(DR, hum_t(s.t(b, e8), 3), 160, K, hum_v(vel + off, 4))
        s.g(DR, hum_t(s.t(b, 2), 3), 180, SN, hum_v(vel + 18, 4))
        if fill:
            s.g(DR, hum_t(s.t(b, 6), 3), 120, SN, hum_v(vel + 10, 4))
            s.g(DR, hum_t(s.t(b, 7), 3), 120, SN, hum_v(vel + 18, 4))
        else:
            s.g(DR, hum_t(s.t(b, 6), 3), 180, SN, hum_v(vel + 20, 4))
        for e8 in range(8):
            if open_hat and e8 == 7:
                s.g(DR, hum_t(s.t(b, 7), 4), 200, OH, hum_v(vel - 26, 5))
            else:
                s.g(DR, hum_t(s.t(b, e8), 4), 70, CH_, hum_v((vel - 30) if e8 % 2 == 0 else (vel - 48), 5))

    def oud(b, name, vel=78):
        root, tones = CH[name]
        for e8 in (0, 3, 6):
            s.g(OD, hum_t(s.t(b, e8), 6), int(1.2 * E), root, hum_v(vel, 5))
        s.g(OD, hum_t(s.t(b, 7), 6), int(.45 * E), root + 2 if (root + 2 - TONIC) % 12 in s.allowed else root + 1, hum_v(vel - 12, 5))
        s.g(OD, hum_t(s.t(b, 7.5), 6), int(.45 * E), root, hum_v(vel - 8, 5))

    def santouri(b, name, vel=50):
        tones = CH[name][1]
        for e8 in range(8):
            s.trem(SA, s.t(b, e8), E, tones[e8 % len(tones)] + 24, vel + (6 if e8 % 2 == 0 else 0), unit=S)

    s.markers = [(1, 'violin taximi'), (5, 'verse 1'), (13, 'verse 2'), (21, 'violin solo'), (29, 'verse 3'), (37, 'solo 2'), (45, 'coda')]
    for blk, chs, v in ((5, VERSE_CH, 96), (13, VERSE_CH, 100), (21, SOLO_CH, 102), (29, VERSE_CH, 104), (37, SOLO_CH, 106)):
        for i, nm in enumerate(chs):
            b = blk + i
            beat(b, vel=v, fill=(i == 7), open_hat=(i % 2 == 1))
            oud(b, nm); santouri(b, nm, vel=46 + (v - 96) // 2)
    s.phrase(VN, 5, VERSE, vel=92, slide=True)
    s.phrase(VN, 13, VERSE, vel=96, slide=True)
    s.phrase(VN, 21, SOLO, vel=100, slide=True, jit=4)
    s.phrase(VN, 29, VERSE, vel=100, slide=True, oct_shift=1)
    s.phrase(VN, 37, SOLO, vel=104, slide=True, jit=4)
    # 코다: 킥+크래시 한 방, 스네어 픽업, 바이올린 D 하강 롱톤
    s.g(DR, s.t(45, 0), 200, K, 116); s.g(DR, s.t(45, 0), 400, CR, 108)
    s.g(DR, s.t(45, 3.5), 80, SN, 90); s.g(DR, s.t(46, 0), 200, K, 112); s.g(DR, s.t(46, 0), 400, CR, 104)
    s.free(VN, [(s.t(45, 0), 2 * E, 4), (s.t(45, 2), 2 * E, 2), (s.t(45, 4), 4 * E, 1), (s.t(46, 0), s.bar_ticks - 100, 0)], vel=98)
    s.g(OD, s.t(46, 0), s.bar_ticks - 100, 38, 84)
    s.trem(SA, s.t(46, 0), s.bar_ticks - 200, 74, 52)
    s.render(46)


# =============================================================== 4. teke — Sabah, short taximi + slow zeibekiko 9/8
def teke():
    s = Song('4-teke', 'Minore tou Teke', 56, 'sabah', (9, 8),
             [('Bouzouki', 0), ('Baglamas', 1), ('Guitar', 2)], {0: 25, 1: 25, 2: 24}, -1, True, 1004)
    BZ, BG, GT = range(3)
    CH = {'Dm': (38, [50, 53, 57]), 'F': (41, [53, 57, 60]), 'Bb': (46, [58, 62, 65])}
    ZEI_CH = ['Dm', 'Dm', 'F', 'Dm', 'Bb', 'F', 'Dm', 'Dm', 'Dm', 'F', 'Bb', 'Dm']
    # 도수: 0 D, 1 E, 2 F, 3 Gb, 4 A, 5 Bb, 6 C, 7 D', 9 F'. 코드톤 Dm 0·2·4 / F 2·4·6 / Bb 5·7·9. Gb(3) 는 경과음으로만
    RUB = [46, 56, 48, 60]
    s.tempos = [(s.t(b), t) for b, t in enumerate(RUB, 1)] + [(s.t(5), 56)]
    bt_ = s.bar_ticks
    T = lambda b, frac: s.t(b) + int(frac * bt_)
    # taximi 4마디: Dm 코드톤에 닻, Gb 는 한 번씩만 찔러 넣기
    taximi = [
        (T(1, .05), 700, 2), (T(1, .4), 500, 4), (T(1, .65), 700, 2),
        (T(2, .0), 500, 0), (T(2, .25), 300, 2), (T(2, .4), 300, 3), (T(2, .55), 1000, 2),
        (T(3, .0), 400, 4), (T(3, .2), 400, 5), (T(3, .4), 400, 4), (T(3, .6), 800, 2),
        (T(4, .0), 400, 2), (T(4, .2), 300, 1), (T(4, .35), 1400, 0),
    ]
    s.free(BZ, taximi, vel=84, double_low=True)
    for b in (2, 4):
        s.g(GT, T(b, 0), bt_ - 100, 38, 48)
    ZEI = [
        [(0, 2, 2), (2, 1, 2), (3, 1, 0), (4, 2, 2), (6, 3, 4)],
        [(0, 1, 4), (1, 1, 4), (2, 1, 2), (3, 1, 3), (4, 2, 2), (6, 3, 0)],
        [(0, 2, 6), (2, 1, 6), (3, 1, 4), (4, 2, 2), (6, 3, 4)],
        [(0, 1, 2), (1, 1, 2), (2, 1, 0), (3, 1, -1), (4, 2, 0), (6, 3, 0)],
        [(0, 2, 5), (2, 1, 5), (3, 1, 7), (4, 2, 9), (6, 3, 7)],
        [(0, 1, 6), (1, 1, 6), (2, 1, 4), (3, 1, 6), (4, 2, 4), (6, 3, 2)],
        [(0, 2, 4), (2, 1, 3), (3, 1, 2), (4, 2, 4), (6, 3, 2)],
        [(0, 1, 0), (1, 1, 0), (2, 2, 0), (4, 5, 0)],
        [(0, 2, 7), (2, 1, 7), (3, 1, 9), (4, 2, 7), (6, 3, 4)],
        [(0, 1, 6), (1, 1, 4), (2, 1, 2), (3, 1, 4), (4, 2, 6), (6, 3, 4)],
        [(0, 2, 7), (2, 1, 5), (3, 1, 7), (4, 2, 9), (6, 3, 7)],
        [(0, 1, 3), (1, 1, 2), (2, 2, 0), (4, 5, 0)],
    ]

    def baglamas(b, name, vel=60):
        tones = CH[name][1]
        for e8 in (1, 3, 5, 7, 8):
            v = vel + (12 if e8 == 8 else 0)
            for k, pch in enumerate(tones[:2]):
                s.g(BG, hum_t(s.t(b, e8) + k * 15, 5), int(.7 * E), pch + 24, hum_v(v, 5))

    def guitar(b, name, vel=54):
        root = CH[name][0]
        for e8 in (0, 6):
            s.g(GT, hum_t(s.t(b, e8), 6), int(1.8 * E), root, hum_v(vel, 4))

    # 구조: taximi 1-4 | zeibekiko 5-16 | taximi 회귀 17-19
    s.markers = [(1, 'taximi (rubato)'), (5, 'slow zeibekiko'), (17, 'taximi return')]
    for i, nm in enumerate(ZEI_CH):
        baglamas(5 + i, nm); guitar(5 + i, nm)
    s.phrase(BZ, 5, ZEI, vel=92, double_low=True, jit=8)
    s.tempos += [(s.t(17), 48), (s.t(18), 42)]
    s.free(BZ, [(T(17, .0), 500, 4), (T(17, .25), 500, 2), (T(17, .5), 1000, 0), (T(18, .0), 700, 2),
                (T(18, .35), 500, 3), (T(18, .55), 500, 2), (T(19, .0), bt_ - 400, 0)], vel=86, double_low=True)
    s.g(GT, T(18, .55), bt_ + 800, 38, 52)
    s.render(19)


# =============================================================== 5. serviko — Rast hasaposerviko 2/4 accelerando
def serviko():
    s = Song('5-serviko', 'Taverna Hasaposerviko', 138, 'rast', (2, 4),
             [('HandDrum', 9), ('Guitar', 0), ('Bouzouki', 1), ('Baglamas', 2), ('Accordion', 3)],
             {0: 0, 1: 24, 2: 25, 3: 25, 4: 21}, 2, False, 1005)
    DR, GT, BZ, BG, AC = range(5)
    CH = {'D': (38, [50, 54, 57]), 'G': (43, [55, 59, 62]), 'A7': (45, [57, 61, 64, 55]), 'Bm': (47, [59, 62, 66])}
    A_CH = ['D', 'D', 'G', 'A7', 'D', 'D', 'A7', 'D', 'D', 'Bm', 'G', 'A7', 'D', 'G', 'A7', 'D']
    B_CH = ['G', 'G', 'D', 'D', 'A7', 'A7', 'D', 'D']
    # 도수: 0 D, 2 F#, 3 G, 4 A, 5 B, 6 C#, 7 D', 8 E', 9 F#', 10 G', 11 A'. 코드톤 D 0·2·4 / G 3·5·7 / A7 4·6·8·3 / Bm 5·7·9
    A = [
        [(0, 1, 0), (1, 1, 2), (2, 1, 4), (3, 1, 2)], [(0, 1, 4), (1, 1, 4), (2, 1, 7), (3, 1, 4)],
        [(0, 1, 5), (1, 1, 5), (2, 1, 7), (3, 1, 5)], [(0, 1, 6), (1, 1, 4), (2, 1, 6), (3, 1, 8)],
        [(0, .5, 7), (.5, .5, 9), (1, 1, 7), (2, 1, 4), (3, 1, 7)], [(0, 1, 9), (1, 1, 7), (2, 2, 4)],
        [(0, 1, 6), (1, 1, 8), (2, 1, 6), (3, 1, 3)], [(0, 3, 0), (3, 1, 0)],
        [(0, 1, 7), (1, 1, 7), (2, 1, 9), (3, 1, 7)], [(0, 1, 9), (1, 1, 7), (2, 1, 5), (3, 1, 7)],
        [(0, .5, 7), (.5, .5, 10), (1, 1, 7), (2, 1, 5), (3, 1, 3)], [(0, 1, 4), (1, 1, 6), (2, 1, 8), (3, 1, 6)],
        [(0, 1, 4), (1, 1, 7), (2, 1, 4), (3, 1, 2)], [(0, 1, 3), (1, 1, 5), (2, 1, 7), (3, 1, 5)],
        [(0, 1, 8), (1, 1, 6), (2, 1, 4), (3, 1, 6)], [(0, 3, 0), (3, 1, 0)],
    ]
    B = [
        [(0, 1, 7), (1, 1, 5), (2, 1, 3), (3, 1, 5)], [(0, 1, 7), (1, 1, 10), (2, 2, 7)],
        [(0, .5, 9), (.5, .5, 7), (1, 1, 4), (2, 1, 7), (3, 1, 9)], [(0, 2, 11), (2, 2, 7)],
        [(0, 1, 8), (1, 1, 6), (2, 1, 4), (3, 1, 6)], [(0, 1, 8), (1, 1, 10), (2, 2, 8)],
        [(0, 1, 7), (1, 1, 4), (2, 1, 2), (3, 1, 4)], [(0, 3, 0), (3, 1, 0)],
    ]

    def drum(b, vel=92, busy=False):
        s.g(DR, hum_t(s.t(b, 0), 4), 120, DOUM, hum_v(vel, 6))
        s.g(DR, hum_t(s.t(b, 1), 4), 80, TEK, hum_v(vel - 16, 6))
        s.g(DR, hum_t(s.t(b, 2), 4), 120, DOUM if not busy else TEK, hum_v(vel - 6, 6))
        s.g(DR, hum_t(s.t(b, 3), 4), 80, TEK, hum_v(vel - 12, 6))
        if busy:
            s.g(DR, hum_t(s.t(b, 1.5), 5), 60, TEK, hum_v(vel - 28, 6))
            s.g(DR, hum_t(s.t(b, 3.5), 5), 60, TEK, hum_v(vel - 24, 6))
        for e8 in (0.5, 1.5, 2.5, 3.5):
            s.g(DR, hum_t(s.t(b, e8), 6), 50, TAMB, hum_v(vel - 34, 6))

    def guitar(b, name, vel=86):
        root, tones = CH[name]
        for e8 in range(4):
            s.g(GT, hum_t(s.t(b, e8), 4), int(.8 * E), root if e8 % 2 == 0 else root + 7, hum_v(vel + (6 if e8 == 0 else -6), 5))
            for k, pch in enumerate(tones[:3]):
                s.g(GT, hum_t(s.t(b, e8) + k * 8, 3), int(.6 * E), pch, hum_v(vel - 16 + (6 if e8 == 0 else 0), 5))

    def baglamas(b, name, vel=58):
        tones = CH[name][1]
        for e8 in range(4):
            s.trem(BG, s.t(b, e8), E, tones[e8 % 3] + 24, vel + (6 if e8 % 2 == 0 else 0), unit=S)

    def accordion(b, name, vel=62):
        for pch in CH[name][1][:3]:
            s.g(AC, s.t(b, 0) + 25, s.bar_ticks - 60, pch + 12, hum_v(vel, 4))

    s.markers = [(1, 'intro'), (9, 'A'), (25, 'B'), (33, 'A2 +accordion'), (49, 'B2 solo 8va'), (57, 'A3 accelerando'),
                 (73, 'B3'), (81, 'A4 top speed'), (97, 'coda')]
    blocks = [(1, B_CH, 'intro'), (9, A_CH, 'A'), (25, B_CH, 'B'), (33, A_CH, 'A2'), (49, B_CH, 'B2'), (57, A_CH, 'A3'),
              (73, B_CH, 'B3'), (81, A_CH, 'A4')]
    fast = ('A3', 'B3', 'A4')
    for b0, chs, tag in blocks:
        for i, nm in enumerate(chs):
            b = b0 + i
            guitar(b, nm, vel=78 if tag == 'intro' else 86 + (6 if tag in fast else 0))
            if tag != 'intro':
                drum(b, vel=88 + (8 if tag in fast else 0), busy=tag in ('B2',) + fast)
                baglamas(b, nm, vel=56 + (8 if tag in fast else 0))
            if tag in ('A2', 'B2') + fast:
                accordion(b, nm)
    s.phrase(BZ, 1, B, vel=88, trem=False)
    s.phrase(BZ, 9, A, vel=98, trem=False)
    s.phrase(BZ, 25, B, vel=100, trem=False)
    s.phrase(BZ, 33, A, vel=102, trem=False)
    s.phrase(BZ, 49, B, vel=104, trem=False, oct_shift=1, jit=4)
    s.phrase(BZ, 57, A, vel=104, trem=False)
    s.phrase(BZ, 73, B, vel=106, trem=False)
    s.phrase(BZ, 81, A, vel=108, trem=False, oct_shift=1, jit=4)
    s.tempos = [(s.t(b), round(138 + (170 - 138) * (b - 57) / 39)) for b in range(57, 97)]
    for b in (97, 98):
        guitar(b, 'D', vel=96); drum(b, vel=100, busy=True); baglamas(b, 'D', vel=66); accordion(b, 'D', vel=70)
    s.phrase(BZ, 97, [[(0, 1, 7), (1, 1, 4), (2, 1, 2), (3, 1, 4)], [(0, 1, 7), (1, 1, 4), (2, 1, 2), (3, 1, 0)]], vel=108, trem=False)
    for k, e8 in enumerate((0, 1, 2)):
        s.g(DR, s.t(99, e8), 120, DOUM, 104 - k * 6)
        s.g(GT, s.t(99, e8), int(.8 * E), 38, 96)
        for pch in CH['D'][1]:
            s.g(GT, s.t(99, e8) + 8, int(.6 * E), pch, 84)
    s.g(DR, s.t(100, 0), 300, DOUM, 112)
    s.g(DR, s.t(100, 0), 300, TAMB, 90)
    s.g(GT, s.t(100, 0), s.bar_ticks - 100, 38, 100)
    for pch in CH['D'][1]:
        s.g(GT, s.t(100, 0) + 10, s.bar_ticks - 150, pch, 90)
    s.trem(BZ, s.t(100, 0), s.bar_ticks - 150, 74, 104)
    s.trem(BZ, s.t(100, 0), s.bar_ticks - 150, 62, 84)
    for pch in CH['D'][1]:
        s.g(AC, s.t(100, 0) + 20, s.bar_ticks - 100, pch + 12, 72)
    s.render(100)


if __name__ == '__main__':
    for fn in (piraeus, hasapiko, smyrna, teke, serviko):
        fn()
