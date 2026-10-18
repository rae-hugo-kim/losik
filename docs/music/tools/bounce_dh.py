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
    """바운스 동안 화면보호기 유휴 시간을 0(끔)으로, 종료 시 이전 값 복원."""
    KEY = ['defaults', '-currentHost']

    def __enter__(self):
        r = subprocess.run(self.KEY + ['read', 'com.apple.screensaver', 'idleTime'], capture_output=True, text=True)
        self.prev = r.stdout.strip() if r.returncode == 0 else None
        subprocess.run(self.KEY + ['write', 'com.apple.screensaver', 'idleTime', '-int', '0'], check=True)
        print(f'screensaver idleTime: {self.prev or "(default)"} -> 0', flush=True)
        return self

    def __exit__(self, *exc):
        if self.prev is None:
            subprocess.run(self.KEY + ['delete', 'com.apple.screensaver', 'idleTime'], capture_output=True)
        else:
            subprocess.run(self.KEY + ['write', 'com.apple.screensaver', 'idleTime', '-int', self.prev])
        print(f'screensaver idleTime restored: {self.prev or "(default)"}', flush=True)


import dh_astra
import dh_fable
import dh_opus

JOBS = sorted(
    [(s['slot'], s['sid'], s['title']) for m in (dh_astra, dh_fable, dh_opus) for s in m.SKETCHES]
)

RESTART_EVERY = 5   # Logic 은 임포트를 거듭할수록 바운스가 느려진다(실측 90s → 320s). 5곡마다 재시작.


def restart_logic(log):
    subprocess.run(['osascript', '-e', 'tell application "Logic Pro Creator Studio" to quit'], capture_output=True)
    for _ in range(30):
        if subprocess.run(['pgrep', '-f', 'Logic Pro Creator Studio$'], capture_output=True).returncode:
            break
        time.sleep(2)
    log('    logic restarted')


def run(jobs, log):
    results = {}
    for n, (slot, sid, title) in enumerate(jobs):
        if n and n % RESTART_EVERY == 0:
            restart_logic(log)
        mid = os.path.join(SK_DIR, f'{sid}-v1.mid')
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
        r = produce(sid, title, 'v1', mid, log=lambda m: log('    ' + m))
        r.pop('strips', None)
        results[sid] = r
        log(f'=== {slot:02d} {sid} {"OK" if r.get("ok") else "FAIL"} {round(time.time() - t0)}s {json.dumps(r, ensure_ascii=False)}')
        time.sleep(3)
    return results


if __name__ == '__main__':
    only = set(sys.argv[1:])
    jobs = [j for j in JOBS if not only or j[1] in only]
    with NoScreensaver():
        results = run(jobs, lambda m: print(m, flush=True))
    print(json.dumps({k: v.get('ok') for k, v in results.items()}))
    sys.exit(0 if all(v.get('ok') for v in results.values()) else 1)
