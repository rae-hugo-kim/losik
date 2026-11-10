"""Canon in D — lo-fi city pop v3 A/B/C (2026-09-20). '원곡성' 복원 실험 × 매처 프로브.

v2(리하모 + 당김 + 단성부)는 업로드를 통과했지만 "캐논인 듯 아닌 듯" — 원곡성은 선율보다 화성(그라운드 베이스)에 있었다.
v3 는 Cover Style A/B/C(파헬벨나이트 / 러스티 캐논 / 캐논시티)에 맞춰 세 갈래로 원곡성을 되살린다. 셋 다 단일 리드가
밀고 나가는 캐논-락 형태(카논 모방 없음). 첫 주제(3~10마디)는 원리듬, 이후 당김.

| | A                      | B                                  | C                                   |
| 화성  | 그라운드 8/8 + 7th    | 6/8 (슬롯 5·6 = Bm7·Em7 유지)     | 8/8 + 41~48 E장조 전조, 49 복귀     |
| 런    | EP 16분 원형          | 기타가 리드(19~34) 16분 원형       | EP 16분 원형, 32분(34~38)은 ½      |
| 드럼  | v2                     | 못갖춘마디 픽업 필인(2마디 4박)    | v2 + 오픈햇 2마디마다               |
| 템포  | 84                     | 84                                 | 90                                  |
"""
import os
import sys

from pipeline import PPQ, BAR, E, S, SK_DIR, SW, bt, hum_t, hum_v, seed, build_smf, write_smf
from canon_data import V1

TRACKS = [('Drums', 9), ('Bass', 0), ('EP', 1), ('Guitar', 2), ('Synth', 3), ('Pad', 4)]
PCS = {0: 0, 1: 33, 2: 4, 3: 24, 4: 90, 5: 89}
DR, BS, EP, GT, SY, PD = range(6)
SID, TITLE, N_BARS = 'canon-lofi', 'Canon Lofi', 57
K, SN, CH, OH, CR = 36, 38, 42, 46, 49

M7, m7, D7 = [0, 4, 7, 11], [0, 3, 7, 10], [0, 4, 7, 10]
# 그라운드 D A B F# G D G A 위 7th 컬러 (root_pc, intervals, bass_pc)
GROUND = [(2, M7, 2), (9, D7, 9), (11, m7, 11), (6, m7, 6), (7, M7, 7), (2, M7, 2), (7, M7, 7), (9, D7, 9)]
GROUND_6 = list(GROUND)
GROUND_6[5] = (11, m7, 11)      # D → Bm7  (v2 대체 유지)
GROUND_6[6] = (4, m7, 4)        # G → Em7

SPECS = {
    'a': dict(bpm=84, prog=GROUND, runs='full', gtr_lead=None, mod=None, pickup=False, oh_every=4),
    'b': dict(bpm=84, prog=GROUND_6, runs='full', gtr_lead=(19, 34), mod=None, pickup=True, oh_every=4),
    'c': dict(bpm=90, prog=GROUND, runs='half32', gtr_lead=None, mod=(41, 48, 2), pickup=False, oh_every=2),
}
STRAIGHT_END = 11          # 3~10 마디 주제는 원리듬


def transpose_at(spec, b):
    mod = spec['mod']
    return mod[2] if mod and mod[0] <= b <= mod[1] else 0


def chord_at_beat(spec, abs_beat):
    return spec['prog'][int(abs_beat) % 8]


def bass_root(pc):
    return 38 + ((pc - 2) % 12)


def voicing(pc, iv, low=57):
    r = low + ((pc - (low % 12)) % 12)
    return [r + i for i in iv]


def transform(spec):
    """V1 → (tick, dur, pitch). 3~10 원리듬, 이후 4분음 당김·8분 스윙. 런은 spec['runs'] 에 따라."""
    out = []
    for s, d, p in V1:
        b = s // BAR + 1
        beat_in_bar = (s % BAR) / PPQ
        swing = SW if (s % PPQ) >= PPQ // 2 else 0
        if d >= 400:
            push = 0.0 if b < STRAIGHT_END else {1.0: -0.25, 2.0: -0.5}.get(beat_in_bar, 0.0)
            out.append((s + int(push * PPQ), d - int(push * PPQ) - 30, p))
        elif 200 <= d < 400:
            out.append((s + swing, d - 20, p))
        elif 100 <= d < 200:                       # 16분 런 (19~26)
            if spec['runs'] in ('full', 'half32'):
                out.append((s, d - 12, p))
            elif ((s // S) % 2) == 0:
                out.append((s + swing, E - 30, p))
        else:                                      # 32분 (34~38)
            if spec['runs'] == 'full':
                out.append((s, d - 6, p))
            elif spec['runs'] == 'half32':
                if ((s // 60) % 2) == 0:
                    out.append((s, S // 2 - 8, p))
            elif ((s // 60) % 4) == 0:
                out.append((s, S - 20, p))
    return out


def compose(spec):
    seed(1702)
    nt = {i: [] for i in range(6)}
    cc = {EP: []}
    gl = spec['gtr_lead']

    def g(tr, tick, dur, pitch, vel):
        nt[tr].append((max(0, int(tick)), max(20, int(dur)), pitch, max(1, min(127, vel))))

    def in_gtr_lead(b):
        return gl is not None and gl[0] <= b <= gl[1]

    # 리드 선율: 기본 EP, B 는 19~34 기타
    for t, d, p in transform(spec):
        b = t // BAR + 1
        tr = GT if in_gtr_lead(b) else EP
        g(tr, hum_t(t, 6), d, p + transpose_at(spec, b), hum_v(96 if tr == GT else 92, 8))
    for b in range(1, N_BARS + 1):
        cc[EP] += [(max(0, bt(b) - 10), 64, 0), (bt(b) + 5, 64, 127)]

    # 베이스: 근음 1·3박, 2박 근음+2.5 다음 근음 없음(그라운드는 박마다 바뀜 → 매 박 근음), 3.75 선행
    for b in range(1, N_BARS):
        base = (b - 1) * 4
        tp = transpose_at(spec, b)
        for q in range(4):
            _, _, bpc = chord_at_beat(spec, base + q)
            r = bass_root(bpc) + tp
            g(BS, hum_t(bt(b, q), 4), int(0.55 * PPQ), r, hum_v(92 if q in (0, 2) else 84, 6))
            if q in (1, 3):
                g(BS, hum_t(bt(b, q + 0.5), 4), int(0.3 * PPQ), r + 12, hum_v(76, 6))
        _, _, nxt = chord_at_beat(spec, base + 4)
        g(BS, hum_t(bt(b, 3.75), 4), int(0.25 * PPQ), bass_root(nxt) + transpose_at(spec, b + 1), hum_v(86, 6))
    g(BS, bt(N_BARS), BAR * 2 - 100, 38, 84)

    # 기타 컷팅 (16분 신코페이션) — 기타 리드 구간에서는 EP 가 컴핑(1·3박 코드)으로 교대
    PAT = [(0, 1), (0.75, 0), (1.5, 1), (2.25, 0), (3, 1), (3.5, 0)]
    for b in range(3, N_BARS):
        base = (b - 1) * 4
        tp = transpose_at(spec, b)
        if in_gtr_lead(b):
            for q in (0, 2):
                pc, iv, _ = chord_at_beat(spec, base + q)
                for k, p in enumerate(voicing(pc, iv, low=50)):
                    g(EP, hum_t(bt(b, q) + k * 10, 5), int(1.6 * PPQ), p + tp, hum_v(66, 6))
            continue
        for beat, acc in PAT:
            pc, iv, _ = chord_at_beat(spec, base + beat)
            for k, p in enumerate(voicing(pc, iv)):
                g(GT, hum_t(bt(b, beat) + k * 7, 5), (170 if acc else 110), p + tp, hum_v(74 if acc else 62, 6))
    for k, p in enumerate(voicing(2, [0, 4, 7, 11, 14])):
        g(GT, bt(N_BARS) + k * 30, BAR * 2 - 200, p, 70)

    # 신스 1+5 롱톤: 29마디~
    for b in range(29, N_BARS):
        base = (b - 1) * 4
        tp = transpose_at(spec, b)
        for q in range(4):
            pc, _, _ = chord_at_beat(spec, base + q)
            r = 62 + ((pc - 2) % 12) + tp
            for p in (r, r + 7):
                g(SY, bt(b, q) + 10, PPQ - 40, p, 44)

    # 패드: 으뜸음 페달 (7마디~), 전조 구간은 E
    for b in range(7, N_BARS - 1, 4):
        tp = transpose_at(spec, b)
        for p in (38, 45):
            g(PD, bt(b) + 20, BAR * 4 - 60, p + tp, 30)
    for p in (50, 57, 62, 66, 69):
        g(PD, bt(N_BARS) + 20, BAR * 2 - 60, p, 40)

    # 드럼
    def drums(b, full):
        for e8 in range(8):
            if full and b % spec['oh_every'] == 0 and e8 == 7:
                g(DR, hum_t(bt(b, 3.5) + SW, 5), 220, OH, hum_v(64, 8))
            else:
                g(DR, hum_t(bt(b, e8 / 2) + (SW if e8 % 2 else 0), 5), 70, CH, hum_v(60 if e8 % 2 == 0 else 44, 8))
        if not full:
            return
        g(DR, hum_t(bt(b, 0), 5), 150, K, hum_v(96, 8))
        g(DR, hum_t(bt(b, 2), 5), 150, K, hum_v(88, 8))
        if b % 2 == 0:
            g(DR, hum_t(bt(b, 3.5) + SW, 5), 120, K, hum_v(72, 8))
        g(DR, hum_t(bt(b, 1), 5), 160, SN, hum_v(100, 8))
        if b % 8 == 0:
            g(DR, hum_t(bt(b, 3), 5), 100, SN, hum_v(84, 8))
            g(DR, hum_t(bt(b, 3.5) + SW, 5), 100, SN, hum_v(96, 8))
        else:
            g(DR, hum_t(bt(b, 3), 5), 160, SN, hum_v(102, 8))

    for b in range(1, N_BARS):
        drums(b, full=b >= 3)
    if spec['pickup']:                             # 2마디 4박 못갖춘마디: 스네어 3연타 램프 + 크래시
        for i, beat in enumerate((3.0, 3.25, 3.5, 3.75)):
            g(DR, hum_t(bt(2, beat), 4), 90, SN, 70 + i * 14)
        g(DR, bt(3), 300, CR, 92)
    if spec['mod']:                                # 전조 진입·복귀에 크래시
        g(DR, bt(spec['mod'][0]), 300, CR, 96)
        g(DR, bt(spec['mod'][1] + 1), 300, CR, 96)
    g(DR, bt(N_BARS), 200, K, 100)
    g(DR, bt(N_BARS), 400, CR, 90)
    return nt, cc


def check(spec, nt):
    clashes = []
    for tr in (EP, GT):
        for t, d, p, _ in nt[tr]:
            if d < E - 40:
                continue
            beat = (t + 40) / PPQ
            b = int(beat // 4) + 1
            pc, iv, _ = chord_at_beat(spec, beat)
            pc = (pc + transpose_at(spec, b)) % 12
            allowed = {(pc + i) % 12 for i in iv} | {(pc + 2) % 12, (pc + 9) % 12}
            if 3 in iv:
                allowed.add((pc + 5) % 12)
            if p % 12 not in allowed:
                clashes.append((b, round(beat % 4, 2), p))
    rng = {TRACKS[tr][0]: (len(v), min(p for _, _, p, _ in v), max(p for _, _, p, _ in v)) for tr, v in nt.items() if v}
    return clashes, rng


def render(key):
    spec = SPECS[key]
    nt, cc = compose(spec)
    clashes, rng = check(spec, nt)
    markers = [(1, 'intro'), (3, 'theme straight'), (11, 'theme syncopated'), (19, 'runs'), (29, 'synth in'), (39, 'calm'), (57, 'ring out')]
    if spec['gtr_lead']:
        markers.append((spec['gtr_lead'][0], 'guitar lead'))
    if spec['mod']:
        markers += [(spec['mod'][0], 'E major'), (spec['mod'][1] + 1, 'back to D')]
    smf = build_smf(f'{TITLE} v3{key.upper()}', spec['bpm'], 2, False, N_BARS, TRACKS, PCS, nt, cc, markers=sorted(markers))
    return write_smf(os.path.join(SK_DIR, f'{SID}-v3{key}.mid'), smf), clashes, rng


if __name__ == '__main__':
    for key in (sys.argv[1:] or ('a', 'b', 'c')):
        msg, clashes, rng = render(key)
        print(msg)
        print('  tracks', rng)
        print('  clashes', len(clashes), clashes[:10])
