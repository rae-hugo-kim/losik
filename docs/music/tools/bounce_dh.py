"""Deep house set (2026-10-12): dh_astra / dh_fable / dh_opus 의 SKETCHES 를 슬롯 순으로 모아 Logic 으로 순차 바운스한다.

주의: produce() 는 시작 시 열려 있는 Logic 프로젝트를 저장 없이 전부 닫는다.
화면 잠금 대책: osascript 합성 입력은 macOS HID 유휴 타이머를 리셋하지 않아 20분 뒤 화면보호기→잠금이 걸린다
(2026-10-18 04:02 실측). 실행 중에만 com.apple.screensaver idleTime 을 0 으로 두고 끝나면 원복하며,
매 곡 전에 잠금 상태를 확인해 잠겨 있으면 15분 창 대기 대신 즉시 중단한다.
인자로 sid 를 주면 그 곡만 돌린다.
"""
import json
import os
import subprocess
import sys
import time

from pipeline import SK_DIR, produce


def screen_locked():
    out = subprocess.run(['ioreg', '-n', 'Root', '-d1', '-a'], capture_output=True, text=True).stdout
    i = out.find('CGSSessionScreenIsLocked')
    return i >= 0 and '<true/>' in out[i:i + 80]


class NoScreensaver:
    """바운스 동안 화면보호기 유휴 시간이 0(끔)인지 보장한다. 복원은 하지 않는다 —
    이 Mac 은 2026-10-19 사용자 결정으로 idleTime=0 이 기본값이고, 복원 로직은 세션(워크트리) 셋이
    동시에 돌 때 먼저 끝난 세션이 남의 바운스 중 화면보호기를 되살리는 문제가 있었다(리뷰 지적)."""
    KEY = ['defaults', '-currentHost']

    def __enter__(self):
        r = subprocess.run(self.KEY + ['read', 'com.apple.screensaver', 'idleTime'], capture_output=True, text=True)
        cur = r.stdout.strip() if r.returncode == 0 else None
        if cur != '0':
            subprocess.run(self.KEY + ['write', 'com.apple.screensaver', 'idleTime', '-int', '0'], check=True)
            print(f'screensaver idleTime: {cur or "(default)"} -> 0 (kept)', flush=True)
        return self

    def __exit__(self, *exc):
        pass


import importlib
import importlib.util


def jobs_for(set_prefix):
    """`<prefix>_astra/_fable/_opus` 모듈의 SKETCHES 를 슬롯 순으로 모은다 (dh = deep house, lh = lo-fi hip hop).
    아직 작곡되지 않은 모델의 모듈은 건너뛴다 (순차 작곡 중 먼저 끝난 모델부터 바운스하기 위해)."""
    mods = []
    for m in ('astra', 'fable', 'opus'):
        name = f'{set_prefix}_{m}'
        if importlib.util.find_spec(name) is None:
            print(f'    (skip {name}: not composed yet)', flush=True)
            continue
        mods.append(importlib.import_module(name))   # 모듈 내부 오류는 그대로 터뜨린다
    jobs = sorted((s['slot'], s['sid'], s['title']) for m in mods for s in m.SKETCHES)
    titles = {}
    for _, sid, title in jobs:
        titles.setdefault(title, []).append(sid)
    dup = {t: v for t, v in titles.items() if len(v) > 1}
    assert not dup, f'duplicate titles (Logic project name = title): {dup}'
    return jobs

RESTART_EVERY = 5   # Logic 은 임포트를 거듭할수록 바운스가 느려진다(실측 90s → 320s). 5곡마다 재시작.


from pipeline import restart_logic   # 세션 간 잠금 안에서 Logic 을 재시작한다


def run(jobs, log, ver='v1'):
    results = {}
    for n, (slot, sid, title) in enumerate(jobs):
        if n and n % RESTART_EVERY == 0:
            restart_logic(log)
        mid = os.path.join(SK_DIR, f'{sid}-{ver}.mid')
        if not os.path.exists(mid):
            log(f'=== {slot:02d} {sid} MISSING {mid}')
            results[sid] = {'ok': False, 'stage': 'missing'}
            continue
        if screen_locked():
            log(f'=== {slot:02d} {sid} ABORT screen locked')
            results[sid] = {'ok': False, 'stage': 'locked'}
            break
        t0 = time.time()
        log(f'=== {slot:02d} {sid} start')
        r = produce(sid, title, ver, mid, log=lambda m: log('    ' + m))
        r.pop('strips', None)
        results[sid] = r
        log(f'=== {slot:02d} {sid} {"OK" if r.get("ok") else "FAIL"} {round(time.time() - t0)}s {json.dumps(r, ensure_ascii=False)}')
        time.sleep(3)
    return results


if __name__ == '__main__':
    import argparse
    ap = argparse.ArgumentParser(description='셋(dh/lh)을 슬롯 순으로 Logic 바운스한다.')
    ap.add_argument('--set', default='dh', choices=('dh', 'lh'), help='dh = deep house, lh = lo-fi hip hop')
    ap.add_argument('--ver', default='v1', help='스케치 버전 접미사 (v1/v2/v3…)')
    ap.add_argument('sids', nargs='*', help='지정하면 그 sid 만')
    a = ap.parse_args()
    all_jobs = jobs_for(a.set)
    # 프로젝트명은 제목이라 셋을 넘어 유일해야 한다 (2026-10-21 'Tin Lantern' 이 dh05/lh05 에 겹쳐 dh05 v1 프로젝트가 덮어써짐).
    others = {t for sp in ('dh', 'lh') if sp != a.set for _, _, t in jobs_for(sp)}
    clash = [(sid, t) for _, sid, t in all_jobs if t in others]
    assert not clash, f'title used by another set: {clash}'
    known = {j[1] for j in all_jobs}
    unknown = sorted(set(a.sids) - known)
    if unknown:
        ap.error(f'unknown sid: {unknown}')
    jobs = [j for j in all_jobs if not a.sids or j[1] in set(a.sids)]
    with NoScreensaver():
        results = run(jobs, lambda m: print(m, flush=True), a.ver)
    print(json.dumps({k: v.get('ok') for k, v in results.items()}))
    sys.exit(0 if results and all(v.get('ok') for v in results.values()) else 1)
