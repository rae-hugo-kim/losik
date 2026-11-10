"""Canon in D — lo-fi city pop 편곡 v1 (2026-09-19). Suno Cover 업로드용.

텍스트 프롬프트로는 Suno 가 캐논 선율을 가져오지 않아, 원곡(퍼블릭 도메인) 3성부+그라운드 베이스를 그대로 두고
편성만 로파이 시티팝으로 바꾼 SMF 를 바운스해 Cover 소스로 쓴다. 음표 원천은 canon_data.py.

편곡
- 템포 72 (원전 50). 4/4, 화음 1개 = 4분음, 57마디 ≈ 3:10.
- 바이올린 1 → EP(PC 4 Deluxe Classic) vel 90 + CC64 마디 리페달 / 바이올린 2 → 나일론 기타(PC 24) vel 78 /
  바이올린 3 → 스퀘어 신스 리드(PC 80) vel 62 / 첼로 → 핑거 베이스(PC 33) vel 84 / 키보드 더블링 트랙은 버림.
- 드럼(SoCal PC 0): 3마디(바이올린 1 진입)부터 킥 1·3, 스네어 2·4, 스윙 8분 햇(뒷박 +22틱), 4마디마다 4& 오픈햇,
  8마디마다 4박 스네어 2타 필인. 1~2마디는 베이스+햇만. 57마디 크래시.
- 패드(PC 89): 3성부가 다 들어온 7마디부터 D 페달(D2+A2) 롱톤 vel 30, 4마디 단위. 화음이 4분음마다 바뀌어 코드 패드는 부적합.
- 휴머나이즈: 선율 타이밍 ±6 벨로시티 ±8, 베이스 ±4/±6, 드럼 ±5/±8.
"""
import os

from pipeline import PPQ, BAR, E, SK_DIR, SW, bt, hum_t, hum_v, seed, build_smf, write_smf
from canon_data import V1, V2, V3, BASS

TRACKS = [('Drums', 9), ('Bass', 0), ('EP', 1), ('Guitar', 2), ('Lead', 3), ('Pad', 4)]
PCS = {0: 0, 1: 33, 2: 4, 3: 24, 4: 80, 5: 89}
DR, BS, EP, GT, LD, PD = range(6)
SID, TITLE, BPM, N_BARS = 'canon-lofi', 'Canon Lofi', 72, 57
K, SN, CH, OH, CR = 36, 38, 42, 46, 49
DMAJ = {2, 4, 6, 7, 9, 11, 1}


def compose():
    seed(1700)
    nt = {i: [] for i in range(6)}
    cc = {EP: []}

    def g(tr, tick, dur, pitch, vel):
        nt[tr].append((max(0, int(tick)), max(20, int(dur)), pitch, max(1, min(127, vel))))

    for tr, part, vel, jt, jv in ((EP, V1, 90, 6, 8), (GT, V2, 78, 6, 8), (LD, V3, 62, 6, 8), (BS, BASS, 84, 4, 6)):
        for s, d, p in part:
            g(tr, hum_t(s, jt), d - 20, p, hum_v(vel, jv))
    for b in range(1, N_BARS + 1):
        cc[EP] += [(max(0, bt(b) - 10), 64, 0), (bt(b) + 5, 64, 127)]

    def drums(b, full):
        for e8 in range(8):
            if full and b % 4 == 0 and e8 == 7:
                g(DR, hum_t(bt(b, 3.5) + SW, 5), 220, OH, hum_v(64, 8))
            else:
                g(DR, hum_t(bt(b, e8 / 2) + (SW if e8 % 2 else 0), 5), 70, CH, hum_v(60 if e8 % 2 == 0 else 44, 8))
        if not full:
            return
        g(DR, hum_t(bt(b, 0), 5), 150, K, hum_v(96, 8))
        g(DR, hum_t(bt(b, 2), 5), 150, K, hum_v(88, 8))
        g(DR, hum_t(bt(b, 1), 5), 160, SN, hum_v(100, 8))
        if b % 8 == 0:
            g(DR, hum_t(bt(b, 3), 5), 100, SN, hum_v(84, 8))
            g(DR, hum_t(bt(b, 3.5) + SW, 5), 100, SN, hum_v(96, 8))
        else:
            g(DR, hum_t(bt(b, 3), 5), 160, SN, hum_v(102, 8))

    for b in range(1, N_BARS):
        drums(b, full=b >= 3)
    g(DR, bt(N_BARS), 200, K, 100)
    g(DR, bt(N_BARS), 400, CR, 96)
    for b in range(7, N_BARS, 4):
        for p in (38, 45):
            g(PD, bt(b) + 20, BAR * 4 - 60, p, 30)
    return nt, cc


def check(nt):
    """원곡 자체에 반음 경과음(C 자연음 등)이 있어 온음계 검사는 부적합 — 트랙별 음역·음표 수만 보고."""
    return {TRACKS[tr][0]: (len(v), min(p for _, _, p, _ in v), max(p for _, _, p, _ in v)) for tr, v in nt.items() if v}


if __name__ == '__main__':
    nt, cc = compose()
    print('tracks', check(nt))
    markers = [(1, 'ground bass'), (3, 'violin 1 → EP'), (5, 'violin 2 → guitar'), (7, 'violin 3 → lead'), (19, '32nd run'), (39, 'calm'), (53, 'ending')]
    smf = build_smf(TITLE, BPM, 2, False, N_BARS, TRACKS, PCS, nt, cc, markers=markers)
    print(write_smf(os.path.join(SK_DIR, f'{SID}-v1.mid'), smf))
