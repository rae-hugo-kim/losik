"""vs-*-fable-v2 바운스 러너 — 저장소 루트에서 `python3 -u docs/music/tools/bounce_vivaldi_fable_v2.py [sid ...]`.

곡마다 vivaldi_fable_v2.compose() 로 경로 B·C 패치 표를 얻어 pipeline.produce(patches=…, select=…) 를 부른다.
select 는 마지막 음이 가장 늦게 끝나는 악기 트랙(1-based) — 패치 로드 뒤 선택돼 있는 트랙의 마지막 리전 끝이
바운스 범위가 되므로, 짧은 트랙이 선택된 채 바운스하면 곡이 잘린다(2026-11-09 실측: 7곡이 1:20~2:40 로 잘림).
결과는 /tmp/vivaldi_fable_v2_results.json 에 누적(재실행 시 해당 sid 만 덮어씀); 잠금 TimeoutError 는 stage='lock-timeout'.
"""
import json, os, sys, time
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)))); sys.path.insert(0, os.getcwd())
from pipeline import SK_DIR, produce, restart_logic
from bounce_dh import NoScreensaver, screen_locked
import vivaldi_fable_v2 as vf
log = lambda m: print(time.strftime('%H:%M:%S'), m, flush=True)
want = sys.argv[1:] or [s['sid'] for s in vf.SKETCHES]
results = {}
OUT = '/tmp/vivaldi_fable_v2_results.json'
if os.path.exists(OUT):
    results = json.load(open(OUT))
with NoScreensaver():
    for n, sid in enumerate(want):
        s = next(x for x in vf.SKETCHES if x['sid'] == sid)
        nt, _, _, _, patches, _ = vf.compose(sid)
        ends = {i + 1: max((t + d for t, d, _, _ in notes), default=0) for i, notes in nt.items()}
        select = max(ends, key=lambda i: (ends[i], -i)) if patches else None   # the track whose last region ends last keeps the bounce full length
        mid = os.path.join(SK_DIR, f'{sid}-v2.mid')
        if n and n % 5 == 0:
            try:
                restart_logic(log)
            except TimeoutError as e:
                log(f'restart skipped: {e}')
        if screen_locked():
            log(f'=== {sid} ABORT screen locked'); results[sid] = {'ok': False, 'stage': 'locked'}; break
        t0 = time.time(); log(f'=== {sid} start patches={patches} select={select}')
        try:
            r = produce(sid, s['title'], 'v2', mid, log=lambda m: log('    ' + m), patches=patches or None, select=select)
        except TimeoutError as e:
            r = {'ok': False, 'stage': 'lock-timeout', 'msg': str(e)}
        r['secs'] = round(time.time() - t0)
        if 'patches' in r:
            r['patches'] = {str(k): [str(v[0]), v[1], list(v[2]) if v[2] else None] for k, v in r['patches'].items()}
        results[sid] = r
        json.dump(results, open(OUT, 'w'), ensure_ascii=False, indent=1)
        log(f'=== {sid} {"OK" if r.get("ok") else "FAIL"} {r["secs"]}s {json.dumps({k: v for k, v in r.items() if k != "strips"}, ensure_ascii=False)[:600]}')
log('DONE ' + json.dumps({k: v.get('ok') for k, v in results.items()}))
