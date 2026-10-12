"""2026-10-12 장르 뼈대 라운드: Fable 세트 8곡 + Astra(gpt) 세트 8곡을 Logic으로 순차 바운스한다. 한 번에 한 프로젝트만 연다.

주의: produce()는 시작할 때 열려 있는 Logic 프로젝트를 **저장하지 않고 전부 닫는다**
(pipeline.close_all_projects(save=False)). 실행 전 Logic에 저장 안 한 작업이 없는지 확인할 것.
화면이 잠겨 있으면 창이 생성되지 않아 15분 대기 후 실패한다.
"""
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
    # Astra (gpt-6-astra) 세트
    ('citrus-root-grid', 'Citrus Root Grid'),
    ('citrus-fifth-grid', 'Citrus Fifth Grid'),
    ('indigo-held-room', 'Indigo Held Room'),
    ('indigo-soft-steps', 'Indigo Soft Steps'),
    ('paper-lantern-eight', 'Paper Lantern Eight'),
    ('paper-lantern-five', 'Paper Lantern Five'),
    ('porch-pocket-anchor', 'Porch Pocket Anchor'),
    ('porch-pocket-skip', 'Porch Pocket Skip'),
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
