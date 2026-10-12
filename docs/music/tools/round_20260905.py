"""2026-09-05 수정 라운드: star v6 · ghost v4 · chrome v4/v5/v6 · golden-hour v3.

피드백 원문: docs/music/FEEDBACK_LOG.md (09-05 행).
믹스 밸런스는 AX 페이더(성공률 랜덤) 대신 SMF 안의 CC7(채널 볼륨)으로 고정한다 — Logic 은 리전 내 CC7 을
채널 스트립 페이더로 해석한다. 바운스 후 band_balance() 로 v5 대비 상대 변화를 계측한다.
"""
from pipeline import PPQ, BAR, E, S, SW, bt, hum_t, hum_v, seed
import sketches as sk
from sketches import TRACKS, GM_PC, chord_at, in_chorus, mk_chord2, PC, compose_latest


# ---------------------------------------------------------------- utilities
def cc7(cc, levels):
    """{track: 0-127} → tick 0 채널 볼륨."""
    for tr, v in levels.items():
        cc.setdefault(tr, []).insert(0, (0, 7, v))


def shift_from(nt, from_bar, n_bars):
    """from_bar 이후의 모든 노트를 n_bars 만큼 뒤로 민다 (삽입 공간 확보)."""
    off = n_bars * BAR
    t0 = bt(from_bar)
    for tr in nt:
        nt[tr] = [(t + off if t >= t0 else t, d, p, v) for t, d, p, v in nt[tr]]


def copy_bars(nt, src_start, src_end, dst_start, tracks=None, vel_scale=1.0):
    """src_start..src_end(포함) 마디의 노트를 dst_start 부터 복사 (섹션 반복용)."""
    off = (dst_start - src_start) * BAR
    lo, hi = bt(src_start), bt(src_end + 1)
    for tr in (tracks if tracks is not None else list(nt)):
        add = [(t + off, d, p, max(1, min(127, int(v * vel_scale)))) for t, d, p, v in nt[tr] if lo <= t < hi]
        nt[tr].extend(add)


def clear_bars(nt, start, end, tracks=None, pred=None):
    lo, hi = bt(start), bt(end + 1)
    for tr in (tracks if tracks is not None else list(nt)):
        nt[tr] = [x for x in nt[tr] if not (lo <= x[0] < hi and (pred is None or pred(x)))]

def remap_cc74(cc, n_bars, src_of):
    """섹션 재배치 후 아르페지오 필터 스윕(CC74)을 새 격자에 다시 깐다."""
    cc[2] = [(bt(b), 74, sk.sk_cc74(src_of(b))) for b in range(1, n_bars + 1)]


def strum(nt, tr, tick, pitches, dur, vel, spread=14, jitter=6):
    """코드 스트럼: 저음→고음 순으로 spread 틱씩 지연."""
    for i, p in enumerate(pitches):
        nt[tr].append((hum_t(tick + i * spread, jitter), max(30, dur - i * spread), p, hum_v(vel, 5)))


# =============================================================== star-cruiser v6
STAR_SWING_2 = {   # 29-32: 기존 솔로의 응답구 — 음역을 올리고 3연음적 당김을 섞음
    29: [(0, .75, 79), (1, .5, 81), (1.75, .25, 78), (2, .5, 76), (2.75, .25, 74), (3, 1, 78)],
    30: [(0.5, .5, 81), (1.25, .25, 83), (1.5, .75, 81), (2.5, .5, 78), (3.25, .75, 76)],
    31: [(0, .5, 74), (0.75, .25, 76), (1, .75, 78), (2, .5, 81), (2.75, .25, 83), (3, 1, 85)],
    32: [(0, 1.5, 83), (1.75, .25, 81), (2, .5, 79), (2.75, .25, 78), (3, .5, 76), (3.5, .5, 74)],
}


def star_chord_rhythm(nt, b, chorus, nxt_voicing):
    """'빰~ 밥 빠빠 / 빰~' — 홀수마디는 못갖춘 리듬 + 다음 코드 선행(3.5박), 짝수마디는 선행음이 1.5박까지 홀드."""
    v = sk.star_chord_voicing(b)
    odd = (b % 2 == 1)
    if chorus:
        if odd:
            hits = [(0, 1.4, 92), (2, .4, 84), (2.5, .2, 80), (2.75, .2, 82)]
            for beat, dur, vel in hits:
                strum(nt, 5, int(bt(b, beat)), v, int(dur * PPQ), vel, spread=8)
            strum(nt, 5, int(bt(b, 3.5)), nxt_voicing, int(1.9 * PPQ), 94, spread=8)   # 밀기(anticipation)
        else:
            for beat, dur, vel in ((1.5, .4, 82), (2.0, .4, 80), (3.0, .9, 86)):
                strum(nt, 5, int(bt(b, beat)), v, int(dur * PPQ), vel, spread=8)
    else:
        if odd:
            for beat, dur, vel in ((0, 1.5, 76), (2.5, .3, 68), (3.0, .3, 70)):
                strum(nt, 5, int(bt(b, beat)), v, int(dur * PPQ), vel, spread=10)
            strum(nt, 5, int(bt(b, 3.5)), nxt_voicing, int(1.5 * PPQ), 78, spread=10)
        else:
            for beat, dur, vel in ((2, .5, 70), (3, 1, 74)):
                strum(nt, 5, int(bt(b, beat)), v, int(dur * PPQ), vel, spread=10)


def star_v6(drum_kit=0, bass_pc=33):
    nt, cc, pcs = compose_latest('star-cruiser')          # = v5
    # ① 구조: VB(25-28) 뒤에 4마디 삽입 → 29-32 스윙 확장, 이후 섹션 +4
    shift_from(nt, 29, 4)
    copy_bars(nt, 25, 28, 29, tracks=[0, 1, 2, 3, 5, 6])  # 리듬 섹션 반복 (리드 제외)
    clear_bars(nt, 27, 28, tracks=[0], pred=lambda x: x[2] == 49)   # 원래 자리의 크래시 롤 제거 (31-32 로 복사됨)
    clear_bars(nt, 25, 28, tracks=[6])                             # FX 라이저도 31-32 쪽만 유지
    sk.add_swing_phrase(nt, STAR_SWING_2, vel=96)
    n_bars = 44
    # ② 코드 리듬: Epic Cloud 트랙 전체 재작성 (5-12 벌스, 13-16 프리, 17-24 코러스, 25-32 VB 롱, 33-40 코러스)
    nt[5] = []
    for b in range(5, 41):
        src = b if b <= 28 else (b - 4 if b <= 32 else b - 4)  # 화성 참조는 원 40마디 격자
        if 25 <= b <= 32:                                     # 스윙 구간: 롱 코드로 물러나 솔로 공간
            v = sk.star_chord_voicing(25 + (b - 25) % 4)
            strum(nt, 5, bt(b), v, BAR - 80, 62, spread=16)
            continue
        chorus = in_chorus(src)
        nxt = sk.star_chord_voicing(src + 1 if src < 40 else 40)
        star_chord_rhythm(nt, b, chorus, nxt)
    # ③ 밸런스 — 1차 시도(CC7 만)는 계측상 무효(low-high 25.1→27.4dB)여서 편성 자체로 해결:
    #    저역 정리: 패드의 최저 옥타브(36-43, 베이스와 동일 음역) 제거 + 패드 감량
    nt[3] = [(t, d, p, int(v * 0.75)) for t, d, p, v in nt[3] if p >= 44]
    #    베이스: Pulse Bass(ES2, 벨로시티 둔감) → Simple Foundation 핑거베이스(ghost/chrome 에서 밸런스 합격) + 벨로시티 감량
    nt[1] = [(t, d, p, max(30, int(v * 0.8))) for t, d, p, v in nt[1]]
    #    드럼: Drum Synth Kit → SoCal (사용자: "안 되면 다른 킷으로 선회") + 햇/스네어 벨로시티 상향
    nt[0] = [(t, d, p, min(127, v + 14) if p in (42, 46, 38, 39) else v) for t, d, p, v in nt[0]]
    cc7(cc, {0: 127, 1: 48, 2: 84, 3: 64, 4: 98, 5: 82, 6: 90})
    remap_cc74(cc, n_bars, lambda b: b if b <= 28 else (28 if b <= 32 else b - 4))
    pcs[0] = drum_kit
    pcs[1] = bass_pc
    return nt, cc, pcs, n_bars


# =============================================================== ghost-signal v4
GHOST_TRACKS = TRACKS + [('SubBass', 6)]


def ghost_v4():
    nt, cc, pcs = compose_latest('ghost-signal')           # = v3 (40마디)
    nt[7] = []
    pcs[7] = 38                                            # Pulse Bass = v0 베이스 음색
    # 레이아웃: 1-36 유지 | 37-44 VA' | 45-48 PRE' | 49 BURST | 50-57 VA'' | 58-65 CH | 66-73 CH | 74-77 OUT
    out_src = (37, 40)
    shift_from(nt, 37, 37)                                 # 기존 OUT 37-40 → 74-77
    copy_bars(nt, 5, 12, 37)
    copy_bars(nt, 13, 16, 45)
    copy_bars(nt, 5, 12, 50)
    copy_bars(nt, 29, 36, 58)
    copy_bars(nt, 29, 36, 66)
    # 49: 터뜨리기 — 크래시 쾅 + 킥 + 로우탐 + 서브 드랍, 나머지 침묵 (패드 잔향만)
    clear_bars(nt, 49, 49, tracks=[0, 1, 2, 4, 5, 6])
    clear_bars(nt, 49, 49, tracks=[3])
    for k in range(8):                                     # 48마디 후반 크래시 롤 가속
        nt[0].append((hum_t(bt(48, 2) + k * S, 4), 120, 49, 60 + k * 8))
    nt[0].append((bt(49), PPQ * 2, 49, 127))
    nt[0].append((bt(49), 240, 36, 127))
    nt[0].append((bt(49), 300, 43, 120))
    nt[0].append((int(bt(49, 0.5)), PPQ, 49, 96))
    nt[7].append((bt(49), PPQ * 2, chord_at('ghost-signal', 5)['bass'] - 12, 110))
    ch49 = chord_at('ghost-signal', 13)
    for p in ch49['pad'][:3]:
        nt[3].append((bt(49), BAR - 40, p, 54))
    # 50-57 마지막 벌스: 핑거베이스 제거 → v0 4분 베이스(옥타브 팝) 무게감
    clear_bars(nt, 50, 57, tracks=[1])
    for b in range(50, 74):
        src = 5 + (b - 50) % 8 if b < 58 else 29 + (b - 58) % 8
        r = chord_at('ghost-signal', src)['bass']
        vel = 1.0 if b < 58 else 0.85
        for beat in (0, 1, 2, 3):
            nt[7].append((hum_t(bt(b, beat), 5), 300, r, hum_v(int((96 if beat in (0, 2) else 82) * vel), 4)))
        nt[7].append((hum_t(bt(b, 3.75), 5), 100, r + 12, hum_v(int(84 * vel), 4)))
    # 74 진입 크래시
    nt[0].append((bt(74), PPQ, 49, 100))
    # 66-73 두 번째 파이널 코러스: 라이드 강화 (에너지 유지)
    for b in range(66, 74):
        nt[0].append((hum_t(int(bt(b, 3.5))), 90, 46, hum_v(76, 5)))
    # 밸런스: v3 는 AX 페이더(arp .62 / pad .60 / lead .62 / clav .50)로 잡았고 CC7 은 계측상 무효 →
    # 동일 비율을 벨로시티로 고정 (clav ≈ -6dB, 나머지 ≈ -3dB 근사). 드럼·핑거베이스·서브는 원레벨.
    for tr, k in ((2, 0.85), (3, 0.85), (4, 0.85), (5, 0.75)):
        nt[tr] = [(t, d, p, max(20, int(v * k))) for t, d, p, v in nt[tr]]
    cc7(cc, {0: 122, 1: 108, 2: 92, 3: 86, 4: 92, 5: 74, 6: 100, 7: 104})
    def ghost_src(b):
        if b <= 36:
            return b
        starts = {37: 5, 45: 13, 49: 16, 50: 5, 58: 29, 66: 29, 74: 37}
        k = max(s for s in starts if s <= b)
        return starts[k] + (b - k)
    remap_cc74(cc, 77, ghost_src)
    return nt, cc, pcs, 77


# =============================================================== chrome-sunset v4/v5/v6
def _chrome_base():
    nt, cc, pcs = compose_latest('chrome-sunset')          # = v3
    nt[2] = []                                             # 클래식 기타 촙(혼자 노는 코드악기) 제거
    nt[5] = []                                             # EP 스탭 제거 → 코드 악기로 재사용
    # 패드: 9th 제거 + 대폭 후퇴 (몽환감의 원인)
    keep = []
    for t, d, p, v in nt[3]:
        b = t // BAR + 1
        if t < bt(39) and p == chord_at('chrome-sunset', min(b, 40))['n9']:
            continue
        keep.append((t, d, p, int(v * 0.7)))
    nt[3] = keep
    return nt, cc, pcs


def chrome_chord(b):
    ch = chord_at('chrome-sunset', b)
    r = ch['stab'][0]
    # 기타 보이싱: 루트-5-옥타브-3(or 7) — 열린 느낌
    return [r - 12, r + 7 - 12, r, r + ch['third'], r + 7]


def chrome_v4():
    """어쿠스틱 기타 A: 벌스 팜뮤트 8분 스트럼, 코러스 롱 스트럼(1박+2.5박 푸시), VB 핑거피킹."""
    nt, cc, pcs = _chrome_base()
    pcs[5] = 27
    for b in range(5, 39):
        v = chrome_chord(min(b, 36))
        if 25 <= b <= 28:                                  # 핑거피킹 아르페지오
            seq = [v[0], v[2], v[3], v[4], v[3], v[2], v[4], v[3]]
            for e8 in range(8):
                nt[5].append((hum_t(bt(b) + e8 * E + (SW if e8 % 2 else 0), 6), 300, seq[e8], hum_v(66, 5)))
        elif in_chorus(b):
            strum(nt, 5, bt(b), v, int(2.3 * PPQ), 80, spread=18)
            strum(nt, 5, int(bt(b, 2.5)), v, int(1.4 * PPQ), 72, spread=18)
            if b % 2 == 0:
                strum(nt, 5, int(bt(b, 3.5)), v[1:], int(.4 * PPQ), 60, spread=10)
        elif b >= 37:
            strum(nt, 5, bt(b), v, BAR - 60, 60, spread=24)
        else:                                              # 팜뮤트 8분
            for e8 in range(8):
                acc = e8 in (0, 5)
                strum(nt, 5, bt(b) + e8 * E + (SW if e8 % 2 else 0), v[:4] if acc else v[1:4],
                      110 if acc else 80, 74 if acc else 58, spread=6, jitter=4)
    cc7(cc, {0: 118, 1: 104, 2: 0, 3: 60, 4: 96, 5: 72, 6: 96})
    return nt, cc, pcs, 40


def chrome_v5():
    """어쿠스틱 기타 B: 화성 리듬 2배(반마디 코드 순환) + 16분 신코페이션 스트럼(보사/시티팝), 벌스 뮤트·코러스 오픈."""
    nt, cc, pcs = _chrome_base()
    pcs[5] = 27
    vp, cp = sk.HARMONY['chrome-sunset']

    def voicing(b, half):
        # 반마디 코드 순환: 전반 = 해당 마디 코드, 후반 = 다음 마디 코드 선행(밀기) → 기존 멜로디와 충돌 없음 (수기 검증)
        ch = chord_at('chrome-sunset', b if half == 0 else min(b + 1, 40))
        r = ch['stab'][0]
        return [r - 12, r + 7 - 12, r, r + ch['third'], r + 7]
    PAT = [(0, 1), (.75, 0), (1.5, 1), (2.25, 0), (3.0, 1), (3.5, 0)]   # (beat, accent)
    for b in range(5, 39):
        if b >= 37:
            strum(nt, 5, bt(b), voicing(36, 0), BAR - 60, 60, spread=24)
            continue
        muted = not in_chorus(b) and not (25 <= b <= 28)
        for beat, acc in PAT:
            v = voicing(b, 0 if beat < 2 else 1)
            dur = (130 if acc else 90) if muted else (int(.7 * PPQ) if acc else int(.45 * PPQ))
            vel = (76 if acc else 60) if muted else (84 if acc else 68)
            strum(nt, 5, int(bt(b, beat)), v if acc else v[1:], dur, vel, spread=8 if muted else 14, jitter=5)
    # 반마디 코드 순환에 맞춰 베이스 근음도 반마디마다 갱신
    nt[1] = [x for x in nt[1] if x[0] >= bt(37)]
    for b in range(5, 37):
        for half in (0, 1):
            r = voicing(b, half)[0]
            nt[1].append((int(bt(b, half * 2)), int(1.9 * PPQ), r, 76 if half == 0 else 70))
    cc7(cc, {0: 118, 1: 104, 2: 0, 3: 60, 4: 96, 5: 72, 6: 96})
    return nt, cc, pcs, 40


def chrome_v6(organ_pc=16):
    """오르간: 롱 코드(마디마다 리트리거, 코러스는 2.5박 푸시 추가), 볼륨 약하게."""
    nt, cc, pcs = _chrome_base()
    pcs[5] = organ_pc
    for b in range(5, 39):
        ch = chord_at('chrome-sunset', min(b, 36))
        r = ch['stab'][0]
        v = [r, r + ch['third'], r + 7] + ([ch['stab'][3]] if in_chorus(b) and len(ch['stab']) > 3 else [])
        if in_chorus(b):
            strum(nt, 5, bt(b), v, int(2.4 * PPQ), 66, spread=20)
            strum(nt, 5, int(bt(b, 2.5)), v, int(1.45 * PPQ), 60, spread=20)
        else:
            strum(nt, 5, bt(b), v, BAR - 60, 62, spread=26)
    cc7(cc, {0: 118, 1: 104, 2: 0, 3: 60, 4: 96, 5: 60, 6: 96})
    return nt, cc, pcs, 40


# =============================================================== probe
def probe_pcs(pc_list):
    """PC 매핑 실측용 SMF: 각 PC 를 별도 트랙에 얹고 한 음씩."""
    tracks = [(f'PC{p}', i) for i, p in enumerate(pc_list)]
    pcs = {i: p for i, p in enumerate(pc_list)}
    nt = {i: [(bt(1 + i), PPQ, 60, 90)] for i in range(len(pc_list))}
    return tracks, pcs, nt, {}
