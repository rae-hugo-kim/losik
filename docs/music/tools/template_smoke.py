"""템플릿 모드 스모크 (seed 20261113-220009-a606).

  --dry-run             Logic 없이 테스트 SMF 를 만들어 parse_smf 로 단언 (verify-commands.json 등록, 커밋 시점 검사)
  --preflight TEMPLATE  Logic 없이 preflight_template 만 실행해 실패 사유를 출력 (AC6 (1)(2)(3))
  --template TEMPLATE   사본 열기 → 기존 트랙 임포트 → 바운스 → 반환 dict·WAV 계측을 단언 (AC1–AC3)
  --gm                  같은 노트에 GM PC 를 넣은 SMF 를 템플릿 없이 produce() (AC4 회귀)

테스트 SMF: 4트랙 9마디 BPM 100. 마디 1 은 전 트랙 무음, 트랙 i 는 마디 [2i+2, 2i+3] 에서만 연주
(틱 [ (2i+1)*BAR, (2i+3)*BAR ) ). PC·CC0/7/10/32 없음. LogicLock 은 produce() 가 잡으므로 여기서는 잡지 않는다.
"""
import argparse
import math
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pipeline as P  # noqa: E402

SMOKE_BPM = 100
SMOKE_BARS = 9
SMOKE_TRACKS = ('Tpl Strings', 'Tpl Harpsichord', 'Tpl Violin EXS', 'Tpl Drums')
SMOKE_CHANNELS = (0, 1, 2, 9)
SMOKE_GM_PCS = {0: 48, 1: 6, 2: 40, 3: 0}
FORBIDDEN_CC = {0, 7, 10, 32}
SEGMENT_BARS = [(2 * i + 2, 2 * i + 3) for i in range(4)]   # 1-based inclusive bars per track


def _notes_for(i):
    """트랙 i: 자기 구간 2마디 동안 4분음 8개(드럼은 킥/스네어 교대)."""
    b0, _ = SEGMENT_BARS[i]
    start = P.bt(b0)
    out = []
    for q in range(8):
        pitch = (36, 38)[q % 2] if i == 3 else (60, 64, 67, 72)[q % 4] + (0, 0, -12, 0)[i]
        out.append((start + q * P.PPQ, P.PPQ - 40, pitch, 96))
    return out


def smoke_smf(bpm=SMOKE_BPM, pcs=None):
    tracks = list(zip(SMOKE_TRACKS, SMOKE_CHANNELS))
    nt = {i: _notes_for(i) for i in range(4)}
    return P.build_smf('tplsmoke', bpm, 0, False, SMOKE_BARS, tracks, pcs, nt, {})


def check_smf(buf):
    _, ntrk, _, info = P.parse_smf(buf)
    assert ntrk == 5, ntrk
    assert round(60_000_000 / info[0]['tempo_us']) == SMOKE_BPM
    for i, tr in enumerate(info[1:]):
        b0, b1 = SEGMENT_BARS[i]
        assert tr['pcs'] == [], (i, tr['pcs'])
        assert not (set(tr['ccs']) & FORBIDDEN_CC), (i, tr['ccs'])
        assert tr['notes'] > 0, i
        assert tr['first_note_tick'] >= P.bt(b0) >= P.BAR, (i, tr['first_note_tick'])
        assert tr['last_note_off_tick'] <= P.bt(b1) + P.BAR, (i, tr['last_note_off_tick'])
    return ntrk - 1


def segment_rms_db(wav, bpm, bars):
    """WAV 의 마디 구간별 RMS(dBFS). bars: [(b0, b1)] 1-based inclusive."""
    x, sr = P.wav_samples_mono(wav, 1)
    spb = 60.0 / bpm * 4
    out = []
    for b0, b1 in bars:
        a, b = int((b0 - 1) * spb * sr), int(b1 * spb * sr)
        seg = x[a:b]
        rms = math.sqrt(sum(v * v for v in seg) / max(1, len(seg)))
        out.append(round(20 * math.log10(rms + 1e-12), 1))
    return out


def wav_seconds(wav):
    x, sr = P.wav_samples_mono(wav, 16)   # sr 은 이미 step 으로 나뉘어 돌아온다
    return len(x) / sr


def main(argv):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--dry-run', action='store_true')
    ap.add_argument('--preflight', metavar='TEMPLATE')
    ap.add_argument('--template', metavar='TEMPLATE')
    ap.add_argument('--gm', action='store_true')
    a = ap.parse_args(argv[1:])
    sid = time.strftime('tplsmoke-%Y%m%d-%H%M%S')
    mid = os.path.join(P.SK_DIR, f'{sid}.mid')

    if a.dry_run:
        buf = smoke_smf()
        n = check_smf(buf)
        print(f'dry-run OK: tracks={n} bars={SMOKE_BARS} bpm={SMOKE_BPM} bytes={len(buf)} no PC, no CC{sorted(FORBIDDEN_CC)}')
        return 0

    if a.preflight:
        P.write_smf(mid, smoke_smf())
        try:
            pf = P.preflight_template(a.preflight, f'Tpl Smoke {sid}', mid)
            print('preflight OK:', pf)
        except P.TemplateError as e:
            print('preflight FAIL:', e)
            return 2
        finally:
            os.remove(mid)
        return 0

    if a.template:
        buf = smoke_smf()
        check_smf(buf)
        print(P.write_smf(mid, buf))
        meta = P.template_meta(a.template)
        assert meta['bpm'] != SMOKE_BPM, f'template BPM {meta["bpm"]} must differ from SMF BPM {SMOKE_BPM}'
        print(f'template: {a.template} tracks={meta["tracks"]} bpm={meta["bpm"]}')
        r = P.produce(sid, 'Tpl Smoke', sid[-6:], mid, template=a.template)
        print('result:', {k: v for k, v in r.items() if k not in ('preflight',)})
        if not r.get('ok'):
            return 3
        snap, strips = r['snapshot'], r['strips']
        assert strips == snap, f'strips changed: {snap} -> {strips}'
        assert len(snap) >= meta['tracks'], (snap, meta['tracks'])   # 패치가 만든 Aux(리버브 버스) 스트립이 뒤에 붙는다
        tempo = float(r['tempo'] if r['tempo'] is not None else 'nan')
        assert abs(tempo - SMOKE_BPM) < 0.01, f'lcd tempo {r["tempo"]} != {SMOKE_BPM}'
        assert r['template_hash_before'] == r['template_hash_after'], 'template changed'
        secs = wav_seconds(r['wav'])
        expect = SMOKE_BARS * 4 * 60 / SMOKE_BPM
        assert expect - 0.1 <= secs <= expect + 12, (secs, expect)
        rms = segment_rms_db(r['wav'], SMOKE_BPM, [(1, 1)] + SEGMENT_BARS)
        print(f'wav {secs:.2f}s (expect {expect:.2f}) rms bar1={rms[0]} segments={rms[1:]}')
        assert rms[0] < -60, f'bar 1 not silent: {rms[0]}'
        for i, v in enumerate(rms[1:]):
            assert v > -40, f'track {i} ({SMOKE_TRACKS[i]}) silent: {v} dBFS'
        assert tuple(r['regions']) == SMOKE_TRACKS, r['regions']
        import plistlib
        with open(os.path.join(r['copy'], 'Alternatives', '000', 'MetaData.plist'), 'rb') as f:
            sif = plistlib.load(f).get('SamplerInstrumentsFiles', [])
        exs = sorted(p.split('/')[-1] for p in sif if p.endswith('.exs'))
        for need in ('Violin (Arco).exs', 'Harpsichord.exs'):   # 경로 C(.exs 프리셋)·경로 B(레거시 패치의 Sampler) 가 저장된 사본에 남아 있다
            assert need in exs, f'saved copy lacks {need} in SamplerInstrumentsFiles ({exs})'
        print(f'saved copy {r["copy"]}: SamplerInstrumentsFiles {len(sif)} entries, exs={exs}')
        print('TEMPLATE SMOKE OK')
        return 0

    if a.gm:
        buf = smoke_smf(pcs=SMOKE_GM_PCS)
        print(P.write_smf(mid, buf))
        r = P.produce(sid, 'Tpl Smoke GM', sid[-6:], mid)
        print('result:', r)
        if not r.get('ok'):
            return 3
        import json
        gm = json.load(open(os.path.join(os.path.dirname(P.SK_DIR), 'gm_patch_map.json')))
        expect = [gm['melodic'][str(SMOKE_GM_PCS[i])] for i in range(3)] + [gm['drum_kits'][str(SMOKE_GM_PCS[3])][0]]
        got = P.strip_names(r['strips'])
        assert got == expect, f'GM strips {got} != gm_patch_map {expect}'
        secs = wav_seconds(r['wav']); expect_s = SMOKE_BARS * 4 * 60 / SMOKE_BPM
        assert expect_s - 0.1 <= secs <= expect_s + 12, (secs, expect_s)
        print(f'GM SMOKE OK: strips={got} wav {secs:.2f}s')
        return 0

    ap.print_help()
    return 1


if __name__ == '__main__':
    sys.exit(main(sys.argv))
