"""grid92 (가제) — 멜로디 후보 3개 (2026-09-19). 기획: FEEDBACK_LOG 'grid92 기획'.

공통 고정: A minor 92 BPM, 픽업 ½마디(스네어 4&·4a) + 8마디 = Verse 진행 Am–Am–Fmaj7–Fmaj7 ×2.
  드럼 = drumgrid B-splash 4마디 셀(ORIGINAL 1·2 + REVISED 3 + B 4마디) ×2, 서브 베이스 마디 1박 근음 1히트,
  신스 스퀘어 1도+5도 롱톤(vel 낮게, 2회전에만). 가변 = 피아노 오스티나토만.

  M1 pedal    E5 리듬 페달 — 밀도 7→5→7→3 감소, 마디 끝 E–D–C / C–B 하행 (Runaway 계열)
  M2 tresillo C5·E5·D5 점4분(3+3+2) 순환 — 2마디 위상, 4마디째 D 생략 (연필깎이 계열)
  M3 twonote  A4 롱 + E5 뒷박 2타 — Fmaj7 위 F5→E5 반음, 4마디째 E–D–C 종지

트랙: 0 Drums(SoCal) 1 Sub(Pulse Bass 38) 2 Piano(Studio Grand 0) 3 Synth(Reverse Engineering 80)
SMF 는 픽업을 온전한 1마디로 두고(마디 1 = 픽업, 스네어만 4&·4a) 마디 2~9 가 본체 — Logic 임포트 시 1마디부터 격자 정렬.
"""
import os
import sys

from pipeline import PPQ, BAR, E, S, SK_DIR, bt, hum_t, hum_v, seed, build_smf, write_smf
from drumgrid import ORIGINAL, REVISED, VARIANTS, GM, VEL, HH_ACCENT

TRACKS = [('Drums', 9), ('Sub', 0), ('Piano', 1), ('Synth', 2)]
PCS = {0: 0, 1: 38, 2: 0, 3: 80}
DR, SB, PN, SY = range(4)
BPM = 92
CELL = VARIANTS['B-splash'][0]                       # 4마디 셀 (B-splash)
# Verse 진행: 마디(본체 1..8) → (근음 MIDI, 신스 1도, 신스 5도)
CHORDS = {1: ('Am', 33, 57, 64), 2: ('Am', 33, 57, 64), 3: ('Fmaj7', 29, 53, 60), 4: ('Fmaj7', 29, 53, 60)}

A4, B4, C5, D5, E5, F5 = 69, 71, 72, 74, 76, 77
# 후보: 본체 4마디 × [(beat, dur_beats, pitch)] — 2회 반복
M1 = [
    [(i * .5, .45, E5) for i in range(7)],
    [(0, .45, E5), (.5, .45, E5), (1, .45, E5), (2, .45, E5), (3, .5, D5), (3.5, .5, C5)],
    [(i * .5, .45, E5) for i in range(7)],
    [(0, .45, E5), (.5, .45, E5), (3, .5, C5), (3.5, .5, B4)],
]
M2 = [
    [(0, 1.4, C5), (1.5, 1.4, E5), (3, .9, D5)],
    [(.5, 1.4, C5), (2, 1.4, E5), (3.5, .5, D5)],
    [(0, 1.4, C5), (1.5, 1.4, E5), (3, .9, D5)],
    [(.5, 1.4, C5), (2, 1.9, E5)],
]
M3 = [
    [(0, 1.9, A4), (1.5, .45, E5), (2.5, .45, E5)],
    [(0, 1.9, A4), (1.5, .45, E5), (3, .5, F5), (3.5, .5, E5)],
    [(0, 1.9, A4), (1.5, .45, E5), (2.5, .45, E5)],
    [(0, 1.9, A4), (1.5, .45, E5), (2.5, .5, E5), (3, .5, D5), (3.5, .5, C5)],
]
CANDIDATES = {'M1-pedal': M1, 'M2-tresillo': M2, 'M3-twonote': M3}
ACCENT_BEATS = {0, 1, 2, 3}   # 정박 악센트


def compose(mel):
    seed(971)
    nt = {i: [] for i in range(4)}

    def g(tr, tick, dur, pitch, vel):
        nt[tr].append((max(0, int(tick)), int(dur), pitch, vel))

    # 픽업 (SMF 마디 1): 스네어 4e · 4a — 뒷박 두 타 (09-19 판정: 4&·4a 16분 더블은 장식처럼 짧음)
    g(DR, bt(1, 3.25), 110, GM["Snare"], 96)
    g(DR, bt(1, 3.75), 110, GM['Snare'], 112)

    for i in range(8):                     # 본체 i=0..7 → SMF 마디 b
        b = i + 2
        cell = CELL[i % 4]
        cyc2 = i >= 4
        name, root, s1, s5 = CHORDS[i % 4 + 1]
        # 드럼 셀 + 셀 시작(다음 1박) 크래시
        for row, grid in cell.items():
            for pos, ch in enumerate(grid):
                if ch == '.':
                    continue
                vel = HH_ACCENT[pos % 4] if row == 'HH' else VEL[row]
                g(DR, hum_t(bt(b) + pos * S, 4), 110, GM[row], hum_v(vel, 4))
        if i % 4 == 0 and i > 0:
            g(DR, bt(b), 110, GM['Crash'], VEL['Crash'])
        # 서브: 마디 1박 근음 1히트 (§2-7). vel 92 → 66: 1차 바운스 저역-고역 차 22 dB(드럼 단독 17)로 서브가 믹스 지배
        g(SB, bt(b), int(1.5 * PPQ), root, 66)
        # 신스 1+5 롱톤 — 2회전에만, 낮게
        if cyc2:
            for p in (s1, s5):
                g(SY, bt(b) + 10, BAR - 40, p, 46)
        # 피아노 오스티나토
        for beat, dur, p in mel[i % 4]:
            acc = beat in ACCENT_BEATS
            g(PN, hum_t(bt(b, beat), 6), int(dur * PPQ), p, hum_v((96 if acc else 84) + (4 if cyc2 else 0), 5))
    # 해소: 마디 10 첫 박 — 킥 + 크래시 + 피아노 A + 서브
    g(DR, bt(10), 110, GM['Kick'], VEL['Kick'])
    g(DR, bt(10), 110, GM['Crash'], VEL['Crash'])
    g(PN, bt(10), BAR - 60, A4, 96)
    g(PN, bt(10), BAR - 60, A4 - 12, 88)
    g(SB, bt(10), BAR - 60, 33, 66)
    return nt


if __name__ == '__main__':
    only = sys.argv[1:]
    for name, mel in CANDIDATES.items():
        if only and name not in only:
            continue
        nt = compose(mel)
        smf = build_smf(f'grid92 {name}', BPM, 0, True, 10, TRACKS, PCS, nt, {},
                        markers=[(1, 'pickup'), (2, 'cycle 1'), (6, 'cycle 2 +synth'), (10, 'resolve')])
        print(write_smf(os.path.join(SK_DIR, f'grid92-{name}.mid'), smf))
