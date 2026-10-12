"""스케치 7곡 작곡 엔진 (compose v3) + 2026-08-30/31 수정 라운드 체인 복원.

각 곡의 vN 은 compose_song_v3 → revise_* 체인으로 결정적으로 재생성된다 (rng 시드 고정).
트랙 인덱스: 0 Drums(ch10) 1 Bass 2 Arp 3 Pad 4 Lead 5 Keys 6 FX.
"""
from pipeline import PPQ, BAR, E, S, SW, bt, hum_t, hum_v, seed

TRACKS = [('Drums', 9), ('Bass', 0), ('Arp', 1), ('Pad', 2), ('Lead', 3), ('Keys', 4), ('FX', 5)]
GM_PC = {0: 25, 1: 38, 2: 81, 3: 89, 4: 80, 5: 4, 6: 100}   # Drum Synth Kit / Pulse Bass / saw lead / Classic Pad / square lead / EP / FX
N_BARS = 40

QUAL = {'m': [0, 3, 7], 'M': [0, 4, 7], 'm7': [0, 3, 7, 10], 'M7': [0, 4, 7, 11], '7': [0, 4, 7, 10]}
PC = {'C': 0, 'C#': 1, 'Db': 1, 'D': 2, 'Eb': 3, 'E': 4, 'F': 5, 'F#': 6, 'G': 7, 'G#': 8, 'Ab': 8, 'A': 9, 'Bb': 10, 'B': 11}


def mk_chord2(pc, q):
    iv = QUAL[q]
    rb = 36 + pc
    if rb > 43:
        rb -= 12
    r3 = 48 + pc
    if r3 > 55:
        r3 -= 12
    pad = [r3 - 12, r3] + [r3 + i for i in iv[1:]] + [r3 + 12]
    r4 = r3 + 12
    if r4 > 67:
        r4 -= 12
    arp = [r4 + i for i in iv[:3]]
    n9 = r4 + 14
    if n9 > 79:
        n9 -= 12
    stab = [r4 + i for i in iv]
    return dict(bass=rb, pad=pad, arp=arp, stab=stab, n9=n9, r4=r4, third=iv[1])


# (id, title, bpm, keysig_sf)
SONGS = {
    'neon-rain': ('Neon Rain', 96, 0), 'highway-zero': ('Highway Zero', 118, 1),
    'chrome-sunset': ('Chrome Sunset', 104, 0), 'midnight-arcade': ('Midnight Arcade', 112, -1),
    'ghost-signal': ('Ghost Signal', 100, -2), 'star-cruiser': ('Star Cruiser', 122, 2),
    'analog-heart': ('Analog Heart', 108, 4),
}
HARMONY = {
    'neon-rain': ([('A', 'm'), ('G', 'M'), ('F', 'M7'), ('E', '7')], [('F', 'M7'), ('G', 'M'), ('A', 'm'), ('E', '7')]),
    'highway-zero': ([('E', 'm'), ('C', 'M'), ('G', 'M'), ('D', 'M')], [('C', 'M'), ('D', 'M'), ('E', 'm'), ('B', 'm7')]),
    'chrome-sunset': ([('C', 'M7'), ('A', 'm7'), ('D', 'm7'), ('G', '7')], [('F', 'M7'), ('G', '7'), ('E', 'm7'), ('A', 'm7')]),
    'midnight-arcade': ([('D', 'm'), ('G', 'm'), ('C', 'M'), ('F', 'M')], [('Bb', 'M'), ('C', 'M'), ('D', 'm'), ('C', 'M')]),
    'ghost-signal': ([('G', 'm'), ('Ab', 'M7'), ('G', 'm'), ('D', '7')], [('C', 'm7'), ('Ab', 'M7'), ('G', 'm'), ('D', '7')]),
    'star-cruiser': ([('B', 'm7'), ('E', 'm7'), ('A', '7'), ('D', 'M7')], [('E', 'm7'), ('A', '7'), ('D', 'M7'), ('B', 'm7')]),
    'analog-heart': ([('E', 'M'), ('G#', 'm'), ('A', 'M'), ('A', 'm')], [('C#', 'm'), ('A', 'M'), ('E', 'M'), ('B', 'M')]),
}
HOOKS = {
    'chrome-sunset': [
        [(0, .5, 72), (.5, .25, 74), (.75, .75, 76), (1.5, .5, 72), (2, 1.5, 81)], [(0, .75, 79), (.75, .75, 77), (1.5, .5, 74), (2, 2, 76)],
        [(0, .5, 71), (.5, .5, 74), (1, .5, 79), (2, 2, 79)], [(0, 1, 76), (1, .5, 74), (1.5, .5, 72), (2, 2, 69)],
        [(0, .5, 72), (.5, .25, 74), (.75, .75, 76), (1.5, .5, 72), (2, 1.5, 81)], [(0, .75, 79), (.75, .75, 77), (1.5, .5, 74), (2, 2, 76)],
        [(0, .5, 74), (.5, .5, 76), (1, .5, 79), (1.5, .5, 81), (2, 2, 83)], [(0, .75, 74), (.75, .75, 72), (1.5, 2.5, 72)],
    ],
    'ghost-signal': [
        [(0, 1.5, 74), (1.5, .5, 75), (2, 1.5, 74), (3.5, .5, 75)], [(0, 1.5, 74), (1.5, .5, 75), (2, 2, 74)],
        [(0, 1.5, 74), (1.5, .5, 75), (2, 1.5, 74), (3.5, .5, 75)], [(0, 2, 74), (2, 2, 70)],
        [(0, 1.5, 74), (1.5, .5, 75), (2, 1.5, 74), (3.5, .5, 75)], [(0, 1.5, 74), (1.5, .5, 75), (2, 2, 74)],
        [(0, 1, 75), (1, 1, 74), (2, 1, 72), (3, 1, 70)], [(0, 4, 67)],
    ],
    'star-cruiser': [
        [(0, .5, 71), (.5, .5, 83), (1, .5, 71), (1.5, .5, 83), (2, .5, 78), (2.5, .5, 74), (3, .5, 79), (3.5, .5, 81)],
        [(0, .5, 73), (.5, .5, 85), (1, .5, 73), (1.5, .5, 85), (2, .5, 81), (2.5, .5, 78), (3, 1, 76)],
        [(0, .5, 74), (.5, .5, 86), (1, .5, 74), (1.5, .5, 86), (2, .5, 81), (2.5, .5, 78), (3, .5, 74), (3.5, .5, 76)],
        [(0, .5, 71), (.5, .5, 83), (1, .5, 71), (1.5, .5, 83), (2, 2, 79)],
        [(0, .5, 71), (.5, .5, 83), (1, .5, 71), (1.5, .5, 83), (2, .5, 78), (2.5, .5, 74), (3, .5, 79), (3.5, .5, 81)],
        [(0, .5, 73), (.5, .5, 85), (1, .5, 73), (1.5, .5, 85), (2, .5, 81), (2.5, .5, 78), (3, 1, 76)],
        [(0, .5, 74), (.5, .5, 86), (1, .5, 74), (1.5, .5, 86), (2, .5, 83), (2.5, .5, 81), (3, .5, 79), (3.5, .5, 78)],
        [(0, .5, 71), (.5, .5, 83), (1, 1, 79), (2, 2, 74)],
    ],
}
VERSE_TOP = {
    'chrome-sunset': [[(1.5, .5, 67), (2, 1, 72), (3, .5, 74)], [(0, 1.5, 72), (2, 1, 69)],
                      [(1.5, .5, 69), (2, 1, 74), (3, .5, 76)], [(0, 2, 74), (2, 1, 71)]],
}
STYLE = {'chrome-sunset': ('half', 'octave8'), 'ghost-signal': ('half', 'quarter'), 'star-cruiser': ('disco', 'pump16')}
TEXTURE = {'chrome-sunset': {2: 28}, 'ghost-signal': {3: 88}, 'star-cruiser': {5: 62}}   # v0 시점 기본값 (revise 에서 덮어씀)
SC_BOUND = [13, 17, 25, 29]


def in_chorus(b):
    return (17 <= b <= 24) or (29 <= b <= 36)


def chord_at(sid, b):
    vp, cp = HARMONY[sid]
    nm, q = (cp if in_chorus(b) else vp)[(b - 1) % 4]
    return mk_chord2(PC[nm], q)


SK_CC = [(1, 30), (4, 50), (5, 60), (12, 70), (13, 75), (16, 95), (17, 105), (24, 105), (25, 80), (28, 85), (29, 110), (36, 110), (37, 90), (40, 25)]


def sk_cc74(bar):
    for (b0, v0), (b1, v1) in zip(SK_CC, SK_CC[1:]):
        if b0 <= bar <= b1:
            return round(v0 + (v1 - v0) * (bar - b0) / max(1, b1 - b0))
    return 64


def compose_song_v2(sid):
    drum_style, bass_style = STYLE[sid]
    nt = {i: [] for i in range(7)}
    cc = {i: [] for i in range(7)}

    def addn(tr, tick, dur, pitch, vel):
        nt[tr].append((tick, dur, pitch, vel))
    ch_at = lambda b: chord_at(sid, b)
    K, SN, CLAP, CH, OH, CR, TM, TL = 36, 38, 39, 42, 46, 49, 45, 43

    def drums_bar(b, style, fill):
        t0 = bt(b)
        if style in ('straight', 'disco'):
            for beat in range(4):
                addn(0, t0 + beat * PPQ, 120, K, 125)
            for beat in (1, 3):
                if not (fill and beat == 3):
                    addn(0, t0 + beat * PPQ, 120, SN, 120)
                    addn(0, t0 + beat * PPQ, 120, CLAP, 102)
            for s in range(8 if fill else 16):
                addn(0, t0 + s * S, 55, CH, [104, 62, 80, 62][s % 4])
            if style == 'disco':
                for beat in range(4):
                    if not (fill and beat >= 2):
                        addn(0, t0 + beat * PPQ + E, 85, OH, 94)
        else:
            addn(0, t0, 130, K, 122)
            addn(0, bt(b, 1.75), 90, K, 98)
            addn(0, bt(b, 2), 130, SN, 118)
            addn(0, bt(b, 2), 130, CLAP, 94)
            for e8 in range(8):
                addn(0, t0 + e8 * E, 55, CH, 86 if e8 % 2 == 0 else 58)
        if fill:
            for i, s in enumerate(range(8, 14)):
                addn(0, t0 + s * S, 90, SN, 82 + i * 7)
            addn(0, bt(b, 3.5), 110, TM, 112)
            addn(0, bt(b, 3.75), 110, TL, 118)

    def bass_bar(b, ch, style):
        r = ch['bass']
        if style == 'quarter':
            for beat in (0, 1, 2, 3):
                addn(1, bt(b, beat), 300, r, 96 if beat in (0, 2) else 82)
            addn(1, bt(b, 3.75), 100, r + 12, 84)
        elif style == 'octave8':
            for e8 in range(8):
                addn(1, bt(b) + e8 * E, 134, r + (12 if e8 % 2 else 0), 100 if e8 == 0 else 84)
            addn(1, bt(b, 3.75), 90, ch_at(min(b + 1, 40))['bass'], 88)
        else:
            for s in range(16):
                addn(1, bt(b) + s * S, 70, r + (12 if s % 2 else 0), 98 if s % 4 == 0 else 80)

    for b in range(1, 41):
        ch = ch_at(b)
        in_ch = in_chorus(b)
        if b <= 38:
            for p in ch['pad'] + [ch['n9']]:
                addn(3, bt(b), BAR - 20, p, 76)
        # (v2 공용 아르페지오는 v3 에서 통째로 교체되므로 생략)
        if b == 4:
            for i in range(8):
                addn(0, bt(4) + i * S * 2, 90, SN if i % 2 == 0 else TM, 70 + i * 6)
        elif 5 <= b <= 36:
            st = drum_style if not (25 <= b <= 28) else 'half'
            drums_bar(b, st, b % 8 == 4 and not (25 <= b <= 28))
            bass_bar(b, ch, bass_style if not (25 <= b <= 28) else 'quarter')
        if (5 <= b <= 12) or (25 <= b <= 28):
            for beat in (1.5, 3.5):
                for p in ch['stab'] + [ch['n9']]:
                    addn(5, bt(b, beat), 160, p, 68)
    for b in (5, 13, 17, 25, 29):
        addn(0, bt(b), PPQ, CR, 115)
    for b in (15, 27):
        addn(6, bt(b), BAR * 2 - 40, 72, 96)
    for start in (17, 29):
        for i, bar_notes in enumerate(HOOKS[sid]):
            for beat, dur, p in bar_notes:
                addn(4, bt(start + i, beat), int(dur * PPQ) - 20, p, 110)
    if sid in VERSE_TOP:
        for rep in (5, 9):
            for i, bar_notes in enumerate(VERSE_TOP[sid]):
                for beat, dur, p in bar_notes:
                    addn(4, bt(rep + i, beat), int(dur * PPQ) - 20, p, 92)
    c16 = ch_at(16)
    for i, p in enumerate([c16['r4'], c16['r4'] + 2, c16['r4'] + c16['third'], c16['r4'] + 7]):
        addn(4, bt(16, i), 220, p, 88 + i * 4)
    for b in range(1, 41):
        cc[2].append((bt(b), 74, sk_cc74(b)))
    return nt, cc


# ---- 곡별 아르페지오 문법 (v0b) ----
def arp_chrome(addn, b, ch):
    if b <= 4 or b >= 37:
        return
    dyad = [ch['arp'][1], ch['arp'][2]]
    for s in (2, 3, 7, 10, 11, 14):
        for p in dyad:
            addn(2, bt(b) + s * S, 60, p, 72 if s in (3, 11) else 60)


def arp_ghost(addn, b, ch):
    t = ch['arp']
    seq = [t[0] - 12, t[1] - 12]
    for i, beat in enumerate([0, .75, 1.5, 2.25, 3.0, 3.75]):
        addn(2, bt(b, beat), 250, seq[i % 2], 72)


def arp_star(addn, b, ch):
    t = ch['arp']
    for beat in range(4):
        addn(2, bt(b, beat), 180, t[0], 96)
        addn(2, bt(b, beat + .5), 90, t[0] + 12, 74)
        addn(2, bt(b, beat + .75), 90, t[2], 74)


ARP_FN = {'chrome-sunset': arp_chrome, 'ghost-signal': arp_ghost, 'star-cruiser': arp_star}


def compose_song_v3(sid):
    nt, cc = compose_song_v2(sid)
    nt[2] = []

    def addn(tr, tick, dur, pitch, vel):
        nt[tr].append((tick, dur, pitch, vel))
    for b in range(1, 41):
        ARP_FN[sid](addn, b, chord_at(sid, b))
    return nt, cc


def crash_rolls(nt, bounds=SC_BOUND, peak=122):
    """FX 사이렌 대체: 2마디 크래시 롤 크레셴도 + 경계 임팩트 스택 (킥+로우탐+크래시)."""
    nt[6] = []
    for s in bounds:
        for k in range(16):
            nt[0].append((hum_t(bt(s - 2) + k * E, 6), 200, 49, 34 + int(k * (110 - 34) / 15)))
        nt[0].append((bt(s), PPQ, 49, peak))
        nt[0].append((bt(s), 200, 36, 125))
        nt[0].append((bt(s), 240, 43, 116))


# =============================================================== star-cruiser
def star_bass(nt, hi=62, lo=52):
    nt[1] = []
    for b in range(5, 37):
        r = chord_at('star-cruiser', b)['bass'] + 12
        for e8 in range(8):
            nt[1].append((hum_t(bt(b) + e8 * E), 110, r, hum_v(hi if e8 % 4 == 0 else lo, 4)))


def star_chord_voicing(b):
    ch = chord_at('star-cruiser', b)
    return [p - 12 if p > 88 else p for p in [ch['arp'][0] + 12, ch['arp'][1] + 12, ch['arp'][2] + 12, ch['n9'] + 12]]


def revise_star4(nt):
    star_bass(nt)
    nt[5] = []
    for b in range(5, 37):
        chord = star_chord_voicing(b)
        if in_chorus(b):
            for beat in (0, 1.5, 2.5, 3.5):
                for p in chord:
                    nt[5].append((hum_t(int(bt(b, beat)), 8), 150, p, hum_v(90 if beat == 0 else 80, 5)))
        else:
            for p in chord:
                nt[5].append((hum_t(bt(b), 10), BAR - 80, p, hum_v(68, 5)))
    crash_rolls(nt)
    return nt


SWING_SOLO = {
    25: [(0, .5, 74), (0.75, .25, 76), (1, .5, 78), (1.75, .25, 74), (2, .75, 71), (3, .75, 69)],
    26: [(0.5, .5, 76), (1.25, .25, 79), (1.5, .5, 78), (2.5, .75, 74), (3.5, .5, 71)],
    27: [(0, .75, 73), (1, .5, 76), (1.75, .25, 78), (2, 1, 79), (3.25, .75, 81)],
    28: [(0, 1.5, 78), (2, .5, 74), (2.75, .25, 73), (3, 1, 71)],
}
VA_FILLS = {10: [(2, .5, 74), (2.75, .25, 76), (3, 1, 78)], 12: [(2, .5, 79), (2.75, .25, 78), (3, 1, 76)]}


def add_swing_phrase(nt, phrases, vel=94):
    for b, phr in phrases.items():
        for beat, dur, p in phr:
            tick = int(bt(b, beat))
            if (beat * 2) % 2 != 0:
                tick += SW
            nt[4].append((hum_t(tick, 8), int(dur * PPQ) - 25, p, hum_v(vel, 6)))


def revise_star5(nt):
    nt = revise_star4(nt)
    nt[4] = [x for x in nt[4] if not (bt(25) <= x[0] < bt(29))]
    add_swing_phrase(nt, SWING_SOLO)
    add_swing_phrase(nt, VA_FILLS, vel=84)
    return nt


# =============================================================== ghost-signal
def revise_ghost(nt):
    ch_at = lambda b: chord_at('ghost-signal', b)
    nt[1] = []
    for b in range(5, 37):
        r = ch_at(b)['bass']
        nt[1].append((bt(b), PPQ * 2 - 80, r, 74))
        nt[1].append((int(bt(b, 2)), PPQ * 2 - 80, r, 68))
    for b in range(17, 25):
        ch = ch_at(b)
        pair = [ch['arp'][0], ch['arp'][1]]
        for e8 in range(8):
            nt[5].append((hum_t(bt(b) + e8 * E, 6), 200, pair[e8 % 2], hum_v(70, 5)))
    for b in range(29, 37):
        ch = ch_at(b)
        block = ch['stab'] + [ch['n9']]
        for beat in (0, 2):
            for p in block:
                nt[5].append((hum_t(int(bt(b, beat)), 8), PPQ * 2 - 60, p, hum_v(76, 5)))
    for b in (35, 36):
        block = ch_at(b)['stab']
        for e8 in range(8):
            for p in block:
                nt[5].append((hum_t(bt(b) + e8 * E, 6), 200, p, 68 + e8 * 4))
    return nt


def revise_ghost2(nt):
    nt = revise_ghost(nt)
    ch_at = lambda b: chord_at('ghost-signal', b)
    nt[5] = [x for x in nt[5] if not (bt(29) <= x[0] < bt(35) and x[1] > PPQ)]
    for b in range(29, 35):
        ch = ch_at(b)
        block = ch['stab'] + [ch['n9']]
        for beat in (0, 1.5, 2.5):
            for p in block:
                nt[5].append((hum_t(int(bt(b, beat)), 8), 130, p, hum_v(84 if beat == 0 else 74, 5)))
    return nt


def revise_ghost3(nt):
    nt = revise_ghost2(nt)
    for b in range(17, 37):
        if not in_chorus(b):
            continue
        t0 = bt(b)
        for e8 in range(8):
            nt[0].append((hum_t(t0 + e8 * E), 70, 51, hum_v(64 if e8 % 2 == 0 else 48, 6)))
        nt[0].append((hum_t(int(bt(b, 2.5))), 90, 46, hum_v(70, 5)))
    for b in range(5, 17):
        if b % 2 == 1:
            nt[0].append((hum_t(bt(b)), 80, 51, hum_v(52, 5)))
    nt[5] = [(t, d, p, max(30, int(v * 0.78))) for t, d, p, v in nt[5]]
    return nt


# =============================================================== chrome-sunset
def revise_chrome(nt):
    ch_at = lambda b: chord_at('chrome-sunset', b)
    nt[0] = []  # (v2 에서 다시 채움)
    for s in SC_BOUND:
        nt[0].append((bt(s), PPQ, 49, 85))
    nt[1] = []
    for b in range(5, 37):
        r = ch_at(b)['bass']
        nt[1].append((bt(b), int(1.9 * PPQ), r, 76))
        nt[1].append((int(bt(b, 2)), int(1.9 * PPQ), r, 70))
    nt[1].append((bt(37), BAR - 100, ch_at(37)['bass'], 64))
    ch40 = mk_chord2(0, 'M7')
    for p in ch40['pad'] + [ch40['n9']]:
        nt[3].append((bt(39), BAR * 2 - 60, p, 58))
    for i, p in enumerate([ch40['r4'], ch40['r4'] + 4, ch40['r4'] + 7, ch40['r4'] + 11]):
        nt[4].append((int(bt(40, i * 0.5)), PPQ * 2, p, 62))
    return nt


def revise_chrome2(nt):
    nt = revise_chrome(nt)
    nt[0] = []
    for b in range(5, 37):
        t0 = bt(b)
        in_ch = in_chorus(b)
        nt[0].append((hum_t(t0), 130, 36, hum_v(100, 5)))
        if b % 4 == 0:
            nt[0].append((hum_t(int(bt(b, 2.5))), 100, 36, hum_v(74, 5)))
        nt[0].append((hum_t(t0 + 2 * PPQ), 130, 38, hum_v(82, 5)))
        if b % 2 == 1:
            nt[0].append((hum_t(int(bt(b, 3.75))), 80, 38, hum_v(36, 5)))
        if in_ch:
            for e8 in range(8):
                nt[0].append((hum_t(t0 + e8 * E + (SW if e8 % 2 else 0)), 70, 51, hum_v(70 if e8 % 2 == 0 else 52, 7)))
        for e8 in range(8):
            nt[0].append((hum_t(t0 + e8 * E + (SW if e8 % 2 else 0)), 55, 42, hum_v((62 if e8 % 2 == 0 else 44) - (8 if in_ch else 0), 7)))
        if b % 8 == 4:
            for i, beat in enumerate((2, 2.5, 3, 3.5)):
                nt[0].append((hum_t(int(bt(b, beat)), 8), 70, 51, 56 + i * 7))
    for s in SC_BOUND:
        nt[0].append((bt(s), PPQ, 49, 78))
    for e8 in range(8):
        nt[0].append((hum_t(bt(37) + e8 * E), 50, 42, hum_v(50, 5)))
    nt[0].append((bt(37), 130, 36, 82))
    nt[0].append((bt(38), 130, 36, 68))
    return nt


# 각 곡 최신판(2026-08-31) 시점의 편성
TEXTURE_V = {
    'star-cruiser': {5: 90},                 # Epic Cloud 코드 / Drum Synth Kit / Pulse Bass
    'ghost-signal': {3: 88, 5: 6, 1: 33},    # Glistening Pad / Muted Clav / Simple Foundation
    'chrome-sunset': {2: 27, 1: 33, 4: 4, 0: 0},  # 클래식 어쿠스틱 촙 / 핑거베이스 / EP 리드 / SoCal
}
LATEST = {'star-cruiser': revise_star5, 'ghost-signal': revise_ghost3, 'chrome-sunset': revise_chrome2}


def compose_latest(sid):
    seed(940)
    nt, cc = compose_song_v3(sid)
    nt = LATEST[sid](nt)
    pcs = dict(GM_PC)
    pcs.update(TEXTURE_V[sid])
    return nt, cc, pcs
