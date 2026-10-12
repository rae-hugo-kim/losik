"""Golden Hour v2 (밴드 편성, 2026-08-25) 복원 + v3 수정.

80마디 · 94 BPM · C장조 · Fmaj7–G7–Dm7–Em7 루프.
트랙: 0 Drums(SoCal) 1 Bass(Simple Foundation) 2 Synth(Epic Cloud) 3 Piano(Studio Grand) 4 Strings(Authentic Strings)
"""
from pipeline import PPQ, BAR, E, S, SW, bt, hum_t, hum_v, seed
from sketches import mk_chord2, PC

TRACKS = [('Drums', 9), ('Bass', 0), ('Synth', 1), ('Piano', 2), ('Strings', 3)]
PCS = {0: 0, 1: 33, 2: 90, 3: 0, 4: 50}
BPM, N_BARS = 94, 80
LOOP = [('F', 'M7'), ('G', '7'), ('D', 'm7'), ('E', 'm7')]
SEC_STARTS = [9, 17, 25, 33, 41, 49, 57, 65, 73]
FILL_BARS = set(s - 1 for s in SEC_STARTS)
K, SN, CLAP, CH, OH, CR, TL, RIDE = 36, 38, 39, 42, 46, 49, 43, 51

HOOK = [
    [(0, .75, 69), (0.75, .75, 72), (1.5, .5, 74), (2, 2, 76)],
    [(0, .75, 74), (0.75, .75, 72), (1.5, .5, 71), (2, 2, 74)],
    [(0, .75, 69), (0.75, .75, 67), (1.5, .5, 65), (2, 2, 69)],
    [(0, 1, 67), (1, .5, 71), (1.5, .5, 74), (2, 2, 79)],
    [(0, .75, 69), (0.75, .75, 72), (1.5, .5, 74), (2, 2, 76)],
    [(0, .75, 74), (0.75, .75, 72), (1.5, .5, 71), (2, 2, 74)],
    [(0, .75, 81), (0.75, .75, 79), (1.5, .5, 76), (2, 2, 74)],
    [(0, 2.5, 76), (2.5, 1.5, 74)],
]
PIANO_LINE = [[(0, 1.5, 76), (1.5, .5, 74), (2, 2, 72)], [(0, 2, 74), (2, 2, 71)],
              [(0, 1.5, 69), (1.5, .5, 67), (2, 2, 65)], [(0, 4, 64)]]
PIANO_RIFF = [[(2, .5, 72), (2.5, .5, 74), (3, 1, 76)], [(2, .5, 74), (2.5, .5, 72), (3, 1, 71)],
              [(2, .5, 69), (2.5, .5, 72), (3, 1, 74)], [(2, .5, 71), (2.5, .5, 74), (3, 1, 76)]]
# v3: G7 마디(34·38)의 리프 — 컴핑의 B(71)·스트링 B 와 동시 발음되던 C(72) 를 코드톤 D–B–A 로 교정.
# 1:23 = 34마디 시작 → 사용자가 지목한 지점이 첫 G7 리프와 정확히 일치.
PIANO_RIFF_G7_FIX = [(2, .5, 74), (2.5, .5, 71), (3, 1, 69)]


def gch(b):
    nm, q = LOOP[(b - 1) % 4]
    return mk_chord2(PC[nm], q)


def compose(version=2):
    seed(941)
    nt = {i: [] for i in range(5)}
    cc = {i: [] for i in range(5)}

    def g(tr, tick, dur, pitch, vel):
        nt[tr].append((max(0, tick), dur, pitch, vel))

    def band_drums(b, energy):
        t0 = bt(b)
        fill = b in FILL_BARS
        g(0, hum_t(t0), 130, K, hum_v(118, 5))
        g(0, hum_t(int(bt(b, 2.5))), 110, K, hum_v(102, 6))
        if energy >= 3 and b % 2 == 0:
            g(0, hum_t(t0 + 2 * PPQ), 110, K, hum_v(96))
        for beat in (1, 3):
            if fill and beat == 3:
                continue
            g(0, hum_t(t0 + beat * PPQ), 130, SN, hum_v(116, 6))
        if not fill:
            if b % 2 == 1:
                g(0, hum_t(int(bt(b, 1.75))), 80, SN, hum_v(44, 6))
            if b % 4 == 2:
                g(0, hum_t(int(bt(b, 3.75))), 80, SN, hum_v(40, 6))
        lim = 5 if fill else 8
        for e8 in range(lim):
            tt = t0 + e8 * E + (SW if e8 % 2 else 0)
            if energy >= 3:
                g(0, hum_t(tt), 70, RIDE, hum_v(86 if e8 % 2 == 0 else 62, 8))
            else:
                g(0, hum_t(tt), 55, CH, hum_v(80 if e8 % 2 == 0 else 54, 8))
        if fill:
            for i, s16 in enumerate(range(10, 13)):
                g(0, hum_t(t0 + s16 * S), 90, SN, 72 + i * 12)
            g(0, hum_t(int(bt(b, 3.25))), 100, 47, hum_v(104))
            g(0, hum_t(int(bt(b, 3.5))), 100, 45, hum_v(110))
            g(0, hum_t(int(bt(b, 3.75))), 110, 43, hum_v(116))

    def band_bass(b, style):
        ch = gch(b)
        r = ch['bass']
        f5 = r + 7
        nxt = gch(b + 1)['bass'] if b < 80 else r
        if style == 'groove':
            g(1, hum_t(bt(b)), int(1.4 * PPQ), r, hum_v(100, 5))
            g(1, hum_t(int(bt(b, 1.5))), int(.4 * PPQ), r, hum_v(82, 5))
            g(1, hum_t(int(bt(b, 2))), int(.9 * PPQ), f5, hum_v(92, 5))
            g(1, hum_t(int(bt(b, 3))), int(.45 * PPQ), r, hum_v(86, 5))
            app = nxt - 1 if abs(nxt - 1 - r) < 8 else nxt + 2
            g(1, hum_t(int(bt(b, 3.5))), int(.45 * PPQ), app, hum_v(88, 5))
        elif style == 'drive':
            seq = [r, r, f5, r, r + 12, f5, r, nxt - 1]
            for e8 in range(8):
                g(1, hum_t(bt(b) + e8 * E), 200, seq[e8], hum_v(96 if e8 in (0, 4) else 82, 5))
        elif style == 'half':
            g(1, bt(b), PPQ * 2 - 60, r, 88)
            g(1, int(bt(b, 2)), PPQ * 2 - 60, f5, 78)
        elif style == 'hold':
            g(1, bt(b), BAR - 100, r, 84)

    def piano_comp(b, soft=False):
        tones = gch(b)['stab']
        seq = [tones[0], tones[2], tones[3], tones[1], tones[3], tones[2]]
        for i, beat in enumerate((0, .5, 1, 2, 2.5, 3)):
            g(3, hum_t(int(bt(b, beat)), 12), 350, seq[i], hum_v(62 if soft else 74, 8))

    def piano_intro(b):
        ch = gch(b)
        for i, p in enumerate(ch['stab'] + [ch['n9']]):
            g(3, hum_t(int(bt(b, i * .5)), 15), PPQ * 2, p, hum_v(58, 6))

    def strings_for(b):
        ch = gch(b)
        r4 = ch['r4']
        th = r4 + ch['third']
        f5 = r4 + 7
        if 13 <= b <= 16:
            g(4, bt(b), PPQ * 2 - 30, r4, 58)
            g(4, int(bt(b, 2)), PPQ * 2 - 30, f5, 62)
        elif 17 <= b <= 24:
            for p in (r4, th):
                g(4, bt(b), BAR - 30, p, 52)
        elif 25 <= b <= 32 or 49 <= b <= 56:
            for p in (r4, f5):
                g(4, bt(b), BAR - 30, p, 56)
        elif 33 <= b <= 40:
            g(4, bt(b), PPQ * 2 - 30, f5, 58)
            g(4, int(bt(b, 2)), PPQ * 2 - 30, th, 56)
        elif 41 <= b <= 48:
            for p in (th, f5):
                g(4, bt(b), BAR - 30, p, 54)
        elif 57 <= b <= 64:
            for p in (r4, th, f5, r4 + 12):
                g(4, bt(b), BAR - 30, p, 60)
        elif 65 <= b <= 72:
            for p in (r4 + 12, th + 12):
                g(4, bt(b), BAR - 30, p, 62)

    def hook(start, transpose=0, vel=104):
        for i, bar in enumerate(HOOK):
            for beat, dur, p in bar:
                g(2, hum_t(int(bt(start + i, beat)), 6), int(dur * PPQ) - 30, p + transpose, hum_v(vel, 6))

    for b in range(1, 81):
        ch = gch(b)
        if b <= 8 or 73 <= b <= 80:
            piano_intro(b)
        elif 57 <= b <= 64:
            piano_comp(b, soft=True)
        else:
            piano_comp(b)
        cc[3].append((bt(b) + 10, 64, 127))
        cc[3].append((bt(b + 1) - 40, 64, 0))
        if 9 <= b <= 24:
            band_drums(b, 2)
        elif 25 <= b <= 40:
            band_drums(b, 3)
        elif 41 <= b <= 48:
            band_drums(b, 1)
        elif 49 <= b <= 56:
            band_drums(b, 3)
        elif 57 <= b <= 64:
            g(0, bt(b), 130, K, 92)
        elif 65 <= b <= 72:
            band_drums(b, 3)
        if 9 <= b <= 24 or 33 <= b <= 48:
            band_bass(b, 'groove')
        elif 25 <= b <= 32 or 49 <= b <= 56 or 65 <= b <= 72:
            band_bass(b, 'drive')
        elif 57 <= b <= 64:
            band_bass(b, 'half')
        elif 73 <= b <= 76:
            band_bass(b, 'hold')
        if 5 <= b <= 8 or 57 <= b <= 64:
            r4 = ch['r4']
            for p in (r4, r4 + 7):
                g(2, bt(b), BAR - 40, p, 58)
        strings_for(b)
    hook(25)
    hook(49)
    hook(65)
    hook(65, transpose=12, vel=66)
    for b in range(17, 25):
        r4 = gch(b)['r4']
        for e8 in range(8):
            g(2, hum_t(bt(b) + e8 * E + (SW if e8 % 2 else 0)), 170, [r4, r4 + 7, r4 + 12, r4 + 7][e8 % 4], hum_v(56, 6))
    for rep in (41, 45):
        for i, bar in enumerate(PIANO_LINE):
            for beat, dur, p in bar:
                g(3, hum_t(int(bt(rep + i, beat)), 10), int(dur * PPQ) - 30, p, hum_v(88, 6))
    for rep in (33, 37):
        for i, bar in enumerate(PIANO_RIFF):
            notes = bar
            # v3: G7 마디(34·38) 교정. 1:23 지목 지점 = 34마디 → 컴핑 B 와의 동시 발음은 의도된 텐션이 아니라 오류
            if version >= 3 and (rep + i) % 4 == 2:
                notes = PIANO_RIFF_G7_FIX
            for beat, dur, p in notes:
                g(3, hum_t(int(bt(rep + i, beat)), 10), int(dur * PPQ) - 30, p, hum_v(84, 6))
    for s in SEC_STARTS:
        for k in range(16):
            g(0, hum_t(bt(s - 2) + k * E, 6), 200, CR, 34 + int(k * (112 - 34) / 15))
        g(0, bt(s), PPQ, CR, 120)
    return nt, cc
