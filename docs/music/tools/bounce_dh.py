"""Deep house set (2026-10-12): dh_astra / dh_fable / dh_opus 의 SKETCHES 를 슬롯 순으로 모아 Logic 으로 순차 바운스한다.

주의: produce() 는 시작 시 열려 있는 Logic 프로젝트를 저장 없이 전부 닫는다. 화면이 잠겨 있으면 실패한다.
인자로 sid 를 주면 그 곡만 돌린다.
"""
import json
import os
import sys
import time

from pipeline import SK_DIR, produce
import dh_astra
import dh_fable
import dh_opus

JOBS = sorted(
    [(s['slot'], s['sid'], s['title']) for m in (dh_astra, dh_fable, dh_opus) for s in m.SKETCHES]
)

if __name__ == '__main__':
    only = set(sys.argv[1:])
    results = {}
    for slot, sid, title in JOBS:
        if only and sid not in only:
            continue
        mid = os.path.join(SK_DIR, f'{sid}-v1.mid')
        if not os.path.exists(mid):
            print(f'=== {slot:02d} {sid} MISSING {mid}', flush=True)
            results[sid] = {'ok': False, 'stage': 'missing'}
            continue
        t0 = time.time()
        print(f'=== {slot:02d} {sid} start', flush=True)
        r = produce(sid, title, 'v1', mid, log=lambda m: print('   ', m, flush=True))
        r.pop('strips', None)
        results[sid] = r
        print(f'=== {slot:02d} {sid} {"OK" if r.get("ok") else "FAIL"} {round(time.time() - t0)}s {json.dumps(r, ensure_ascii=False)}', flush=True)
        time.sleep(3)
    print(json.dumps({k: v.get('ok') for k, v in results.items()}))
