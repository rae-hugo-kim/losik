"""2026-10-12 장르 뼈대 라운드: 8곡을 Logic으로 순차 바운스한다. 한 번에 한 프로젝트만 연다."""
import json
import os
import sys
import time

from pipeline import SK_DIR, produce

JOBS = [
    ('warehouse-jack', 'Warehouse Jack'),
    ('mirrorball-rise', 'Mirrorball Rise'),
    ('velvet-hour', 'Velvet Hour'),
    ('low-tide-shuffle', 'Low Tide Shuffle'),
    ('dusty-tape-house', 'Dusty Tape House'),
    ('faded-organ-house', 'Faded Organ House'),
    ('rainy-window-beat', 'Rainy Window Beat'),
    ('slow-room-piano', 'Slow Room Piano'),
]

if __name__ == '__main__':
    only = set(sys.argv[1:])
    results = {}
    for sid, title in JOBS:
        if only and sid not in only:
            continue
        mid = os.path.join(SK_DIR, f'{sid}-v1.mid')
        t0 = time.time()
        print(f'=== {sid} start', flush=True)
        r = produce(sid, title, 'v1', mid, log=lambda m: print('   ', m, flush=True))
        r.pop('strips', None)
        results[sid] = r
        print(f'=== {sid} {"OK" if r.get("ok") else "FAIL"} {round(time.time() - t0)}s {json.dumps(r, ensure_ascii=False)}', flush=True)
        time.sleep(3)
    print(json.dumps({k: v.get('ok') for k, v in results.items()}))
