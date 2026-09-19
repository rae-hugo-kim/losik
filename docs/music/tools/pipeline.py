"""Logic Pro Creator Studio 제작 파이프라인 (2026-08 세션 커널 코드 복원본).

SMF 인코딩 · Logic AX 자동화(임포트/저장/메트로놈/바운스) · 리미터 · WAV 변환 · 오디오 계측.
`docs/music/PROMPT_GUIDELINES.md` §3·§6 의 워크플로를 그대로 코드화한 것.
"""
import math
import os
import random
import struct
import subprocess
import time

PPQ = 480
BAR = PPQ * 4
E, S = PPQ // 2, PPQ // 4

BOUNCE_DIR = '/Volumes/Netac 2TB/music/bounces'
PROJ_DIR = '/Volumes/Netac 2TB/music/projects'
SK_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'sketches')
APP = 'Logic Pro Creator Studio'


def bt(bar, beat=0.0):
    return (bar - 1) * BAR + int(beat * PPQ)


# ---------------------------------------------------------------- humanize
_rng = random.Random(940)


def seed(n):
    _rng.seed(n)


def hum_t(t, amt=8):
    return max(0, t + _rng.randint(-amt, amt))


def hum_v(v, amt=12):
    return max(30, min(127, v + _rng.randint(-amt, amt)))


SW = 22  # 8분 스윙 지연 틱


# ---------------------------------------------------------------- SMF
def varlen(n):
    out = bytearray([n & 0x7F])
    n >>= 7
    while n:
        out.insert(0, 0x80 | (n & 0x7F))
        n >>= 7
    return bytes(out)


def track_chunk(events):
    events.sort(key=lambda e: (e[0], e[1]))
    data, last = bytearray(), 0
    for tick, _, ev in events:
        data += varlen(tick - last) + ev
        last = tick
    data += varlen(0) + b'\xff\x2f\x00'
    return b'MTrk' + struct.pack('>I', len(data)) + bytes(data)


def meta(tick, mtype, payload, order=0):
    return (tick, order, bytes([0xFF, mtype, len(payload)]) + payload)


def build_smf(title, bpm, keysig_sf, minor, n_bars, tracks, pcs, nt, cc, markers=()):
    """tracks: [(name, midi_ch)], pcs: {idx: program}, nt: {idx: [(tick,dur,pitch,vel)]},
    cc: {idx: [(tick, cc, val)]}, markers: [(bar, text)]"""
    cond = [
        meta(0, 0x03, title.encode()),
        meta(0, 0x51, struct.pack('>I', round(60_000_000 / bpm))[1:]),
        meta(0, 0x58, bytes([4, 2, 24, 8])),
        meta(0, 0x59, struct.pack('>bB', keysig_sf, 1 if minor else 0)),
        meta(bt(n_bars) + BAR, 0x06, b'END'),
    ]
    for bar, text in markers:
        cond.append(meta(bt(bar), 0x06, text.encode()))
    chs = [track_chunk(cond)]
    for i, (name, mch) in enumerate(tracks):
        evs = [meta(0, 0x03, name.encode()), (0, 0, bytes([0xC0 | mch, pcs[i]]))]
        for tick, c, val in cc.get(i, []):
            evs.append((tick, 0, bytes([0xB0 | mch, c, val])))
        for tick, dur, pitch, vel in nt.get(i, []):
            evs.append((tick, 2, bytes([0x90 | mch, pitch, vel])))
            evs.append((tick + dur, 1, bytes([0x80 | mch, pitch, 0])))
        chs.append(track_chunk(evs))
    return b'MThd' + struct.pack('>IHHH', 6, 1, len(chs), PPQ) + b''.join(chs)


def parse_smf(buf):
    assert buf[:4] == b'MThd'
    fmt, ntrk, div = struct.unpack('>HHH', buf[8:14])
    pos, info = 14, []
    for _ in range(ntrk):
        assert buf[pos:pos + 4] == b'MTrk'
        ln = struct.unpack('>I', buf[pos + 4:pos + 8])[0]
        d, end = buf[pos + 8:pos + 8 + ln], pos + 8 + ln
        i = tick = ons = 0
        mx = 0
        tempo_us = None
        pcs = []
        while i < len(d):
            dt = 0
            while True:
                dt = (dt << 7) | (d[i] & 0x7F)
                c = d[i]
                i += 1
                if not (c & 0x80):
                    break
            tick += dt
            mx = max(mx, tick)
            st = d[i]
            if st == 0xFF:
                mt, ml = d[i + 1], d[i + 2]
                if mt == 0x51:
                    tempo_us = int.from_bytes(d[i + 3:i + 6], 'big')
                i += 3 + ml
            elif st & 0xF0 == 0x90:
                ons += 1 if d[i + 2] > 0 else 0
                i += 3
            elif st & 0xF0 in (0x80, 0xA0, 0xB0, 0xE0):
                i += 3
            elif st & 0xF0 == 0xC0:
                pcs.append(d[i + 1])
                i += 2
            elif st & 0xF0 == 0xD0:
                i += 2
            else:
                raise ValueError(f'status {st:02x}')
        info.append(dict(notes=ons, last_tick=mx, tempo_us=tempo_us, pcs=pcs))
        pos = end
    return fmt, ntrk, div, info


def write_smf(path, smf):
    with open(path, 'wb') as f:
        f.write(smf)
    fmt, ntrk, div, info = parse_smf(smf)
    total = sum(x['notes'] for x in info[1:])
    bpm = 60_000_000 / info[0]['tempo_us']
    last_bar = max(x['last_tick'] for x in info[1:]) / BAR + 1
    return f'{os.path.basename(path)} {len(smf)}B tracks={ntrk} bpm={bpm:.0f} notes={total} last_bar={last_bar:.1f}'


# ---------------------------------------------------------------- Logic AX
def osa(script, timeout=60):
    p = subprocess.run(['osascript', '-e', script], capture_output=True, text=True, timeout=timeout)
    return p.returncode, p.stdout.strip(), p.stderr.strip()


def windows():
    rc, out, err = osa(f'''tell application "System Events"
tell process "{APP}"
set out to ""
repeat with w in windows
set out to out & "|" & (name of w)
end repeat
return out
end tell
end tell''')
    # osascript 는 한글을 NFD 로 돌려줄 때가 있어 리터럴 비교가 실패한다 → NFC 정규화
    import unicodedata
    return [unicodedata.normalize('NFC', w) for w in out.split('|')[1:]] if rc == 0 else []


def wait_window(substr, present=True, timeout=40):
    t0 = time.time()
    while time.time() - t0 < timeout:
        hit = any(substr in w for w in windows())
        if hit == present:
            return True
        time.sleep(1.5)
    return False


def project_windows():
    return [w for w in windows() if w.endswith('- 트랙')]


def close_stray():
    for wn in ('컨트롤러 할당', '설정', '색상'):
        osa(f'''tell application "System Events"
tell process "{APP}"
try
click button 1 of window "{wn}"
end try
end tell
end tell''')


def dismiss_save_panel():
    if any(w == '저장' for w in windows()):
        osa(f'''tell application "System Events"
tell process "{APP}"
set frontmost to true
key code 53
end tell
end tell''')
        time.sleep(1.5)


def close_all_projects(save=None):
    """save=None: 무제는 저장 안 함, 제목 있으면 저장. save=False: 전부 저장 안 함."""
    for _ in range(4):
        pws = project_windows()
        if not pws:
            return True
        title = pws[0]
        if save is False or title.startswith('무제'):
            btn = '저장 안 함'
        else:
            btn = '저장'
        osa(f'''tell application "System Events"
tell process "{APP}"
set frontmost to true
perform action "AXRaise" of window "{title}"
delay 0.5
keystroke "w" using command down
delay 2
repeat with w in windows
try
click button "{btn}" of w
exit repeat
end try
end repeat
end tell
end tell''')
        time.sleep(3)
        dismiss_save_panel()
        t0 = time.time()
        while time.time() - t0 < 20:
            if title not in windows():
                break
            time.sleep(2)
    return not project_windows()


def clear_alerts():
    """임포트 직후 뜨는 템포/알림 시트: 기본 버튼 클릭."""
    osa(f'''tell application "System Events"
tell process "{APP}"
repeat with w in windows
try
if (count of buttons of w) > 0 and not ((name of w) contains "트랙") then
click button 1 of w
end if
end try
end repeat
end tell
end tell''')


def open_mid(path, timeout=150):
    """SMF 임포트 → '무제 - 트랙' 창 등장까지 대기. 임포트가 수 분 지연되는 경우가 있어 넉넉히."""
    subprocess.run(['open', '-a', APP, path], capture_output=True)
    t0 = time.time()
    while time.time() - t0 < timeout:
        if any(w.startswith('무제') and w.endswith('- 트랙') for w in windows()):
            time.sleep(3)
            clear_alerts()
            return True
        time.sleep(4)
    return False


def lcd_tempo():
    """컨트롤 막대 LCD 의 템포 텍스트 (임포트된 곡 식별용 지문)."""
    rc, out, err = osa(f'''on findT(el, depth)
tell application "System Events"
if depth > 8 then return ""
try
if role of el is "AXStaticText" then
set v to value of el
if v contains "." then return v
end if
end try
try
repeat with c in (every UI element of el)
set r to my findT(c, depth + 1)
if r is not "" then return r
end repeat
end try
return ""
end tell
end findT
tell application "System Events"
tell process "{APP}"
repeat with w in windows
if (name of w) ends with "- 트랙" then
repeat with g in (every UI element of w)
try
if description of g is "컨트롤 막대" then return my findT(g, 0)
end try
end repeat
end if
end repeat
return ""
end tell
end tell''', timeout=60)
    return out


def save_project_as(name):
    if os.path.exists(os.path.join(PROJ_DIR, f'{name}.logicx')):
        return False, f'Project already exists: {name}'
    rc, out, err = osa(f'''tell application "System Events"
tell process "{APP}"
set frontmost to true
delay 0.4
click menu bar item "파일" of menu bar 1
delay 0.6
click menu item "저장" of menu 1 of menu bar item "파일" of menu bar 1
delay 2.5
set w to window "저장"
key code 5 using {{command down, shift down}}
delay 1
set value of text field 1 of sheet 1 of w to "{PROJ_DIR}"
set focused of text field 1 of sheet 1 of w to true
key code 36
delay 1
set sg to splitter group 1 of w
set nameField to missing value
repeat with c in (every UI element of sg)
try
if role of c is "AXTextField" and description of c is "텍스트 필드" then set nameField to c
end try
end repeat
set value of nameField to "{name}"
delay 1
if not enabled of button "저장" of sg then error "Project save button is disabled"
click button "저장" of sg
return "saved"
end tell
end tell''', timeout=90)
    ok = wait_window(name, timeout=60)
    close_stray()
    return rc == 0 and ok, out or err


def save_quiet():
    osa(f'''tell application "System Events"
tell process "{APP}"
set frontmost to true
delay 0.4
keystroke "s" using command down
end tell
end tell''')
    time.sleep(4)


def metronome_off(win_title):
    """컨트롤 막대의 값=1 체크박스 중 마지막(메트로놈)을 클릭. 이 변형판은 메트로놈을 바운스에 렌더함."""
    script = '''on collectOn(el, depth, acc)
tell application "System Events"
if depth > 8 then return acc
try
set r to role of el
on error
return acc
end try
if r is "AXCheckBox" then
try
if description of el is "체크상자" and (value of el as integer) is 1 then set end of acc to el
end try
return acc
end if
try
repeat with c in (every UI element of el)
set acc to my collectOn(c, depth + 1, acc)
end repeat
end try
return acc
end tell
end collectOn
tell application "System Events"
tell process "%s"
set frontmost to true
set acc to {}
repeat with g in (every UI element of window "%s")
try
if description of g is "컨트롤 막대" then set acc to my collectOn(g, 0, acc)
end try
end repeat
if (count of acc) < 2 then return "on_count=" & (count of acc) & " skip"
click (item (count of acc) of acc)
delay 1
return "clicked; before=" & (count of acc)
end tell
end tell''' % (APP, win_title)
    rc, out, err = osa(script, timeout=40)
    return out or err


def open_mixer():
    osa(f'''tell application "System Events"
tell process "{APP}"
set frontmost to true
delay 0.3
click menu bar item "윈도우" of menu bar 1
delay 0.5
click menu item "믹서 열기" of menu 1 of menu bar item "윈도우" of menu bar 1
end tell
end tell''')
    time.sleep(3)


def mixer_strips():
    """믹서 창의 채널 스트립 패치명 실측 (§3 게이트: PC 매핑 확인)."""
    rc, out, err = osa(f'''on findStrips(el, depth, out)
tell application "System Events"
if depth > 6 then return out
try
set r to role of el
on error
return out
end try
if r is "AXLayoutItem" then
try
set out to out & "[" & (description of el) & "] "
end try
return out
end if
try
repeat with c in (every UI element of el)
set out to my findStrips(c, depth + 1, out)
end repeat
end try
return out
end tell
end findStrips
tell application "System Events"
tell process "{APP}"
repeat with w in windows
try
if (name of w) contains "믹서" then return my findStrips(w, 0, "")
end try
end repeat
return "no mixer"
end tell
end tell''', timeout=60)
    return out or err


def start_bounce_aiff(proj_name, file_name):
    rc, out, err = osa(f'''tell application "System Events"
tell process "{APP}"
set frontmost to true
perform action "AXRaise" of window "{proj_name} - 트랙"
delay 0.5
click menu bar item "파일" of menu bar 1
delay 0.7
click menu item "바운스" of menu 1 of menu bar item "파일" of menu bar 1
delay 0.7
click menu item "프로젝트 또는 섹션…" of menu 1 of menu item "바운스" of menu 1 of menu bar item "파일" of menu bar 1
delay 5
set w to missing value
repeat with w2 in windows
if (name of w2) contains "바운스" then set w to w2
end repeat
if w is missing value then return "no bounce window"
set offlineReady to false
repeat with modeButton in pop up buttons of w
if value of modeButton is "자동" or value of modeButton is "실시간" or value of modeButton is "오프라인" then
if value of modeButton is not "오프라인" then
click modeButton
click menu item "오프라인" of menu 1 of modeButton
delay 0.5
end if
set offlineReady to (value of modeButton is "오프라인")
exit repeat
end if
end repeat
if not offlineReady then error "Offline bounce mode was not selected"
try
set tbl to table 1 of scroll area 1 of w
repeat with theRow in (every row of tbl)
try
repeat with theCell in (every UI element of theRow)
repeat with cb in (every UI element of theCell)
try
if role of cb is "AXCheckBox" and description of cb is "M4A" and (value of cb as integer) is 1 then click cb
if role of cb is "AXCheckBox" and description of cb is "비압축" and (value of cb as integer) is 0 then click cb
end try
end repeat
end repeat
end try
end repeat
end try
delay 0.5
perform action "AXRaise" of w
key code 36
delay 3
key code 5 using {{command down, shift down}}
delay 1
keystroke "{BOUNCE_DIR}"
key code 36
delay 1.5
set sg to splitter group 1 of w
set nameField to missing value
repeat with c in (every UI element of sg)
try
if role of c is "AXTextField" and description of c is "텍스트 필드" then set nameField to c
end try
end repeat
set value of nameField to "{file_name}"
delay 1
repeat 20 times
if enabled of button "바운스" of splitter group 1 of w then exit repeat
delay 0.5
end repeat
if not enabled of button "바운스" of splitter group 1 of w then error "Bounce button is disabled"
click button "바운스" of splitter group 1 of w
return "bounce started"
end tell
end tell''', timeout=120)
    if 'bounce started' not in out:
        return False, out or err
    if not wait_window('바운스', present=False, timeout=20):
        return False, 'Bounce save dialog did not close'
    return True, out


def wait_file_stable(path, min_size=500000, timeout=240):
    t0 = time.time()
    while time.time() - t0 < timeout:
        if os.path.exists(path) and os.path.getsize(path) > min_size:
            s = os.path.getsize(path)
            time.sleep(3)
            if os.path.getsize(path) == s:
                return True
        time.sleep(3)
    return False


# ---------------------------------------------------------------- audio post
def _aiff_ssnd(buf):
    pos = 12
    while pos + 8 <= len(buf):
        cid = buf[pos:pos + 4]
        ln = struct.unpack('>I', buf[pos + 4:pos + 8])[0]
        if cid == b'SSND':
            off2, _ = struct.unpack('>II', buf[pos + 8:pos + 16])
            return pos + 16 + off2, ln - 8 - off2
        pos += 8 + ln + (ln & 1)
    raise ValueError('no SSND')


def limit_aiff(path):
    """24bit BE AIFF 소프트 리미터: -0.1 dBFS 실링, 니 90%."""
    buf = open(path, 'rb').read()
    off, ln = _aiff_ssnd(buf)
    raw = buf[off:off + ln]
    n = len(raw) // 3
    FS = 8388607.0
    CEIL = 10 ** (-0.1 / 20)
    KNEE = CEIL * 0.9
    out = bytearray(n * 3)
    hits = 0
    th = math.tanh
    for i in range(n):
        x = int.from_bytes(raw[i * 3:i * 3 + 3], 'big', signed=True) / FS
        ax = x if x >= 0 else -x
        if ax > KNEE:
            s_ = 1.0 if x >= 0 else -1.0
            x = s_ * (KNEE + (CEIL - KNEE) * th((ax - KNEE) / (CEIL - KNEE)))
            hits += 1
        v = int(x * FS)
        v = 8388607 if v > 8388607 else (-8388608 if v < -8388608 else v)
        out[i * 3:i * 3 + 3] = v.to_bytes(3, 'big', signed=True)
    new = bytearray(buf)
    new[off:off + ln] = out
    with open(path, 'wb') as f:
        f.write(new)
    return hits


def aiff_to_wav(aif, wav):
    r = subprocess.run(['afconvert', '-f', 'WAVE', '-d', 'LEI24', aif, wav], capture_output=True, text=True)
    return r.returncode == 0 and os.path.exists(wav), r.stderr[:200]


def wav_samples_mono(path, step=1):
    """WAV(LEI24/LEI16) → 모노 float 리스트 (step 간격 서브샘플). 계측용."""
    buf = open(path, 'rb').read()
    pos = 12
    nch = bits = sr = None
    data = None
    while pos + 8 <= len(buf):
        cid = buf[pos:pos + 4]
        ln = struct.unpack('<I', buf[pos + 4:pos + 8])[0]
        if cid == b'fmt ':
            _, nch, sr, _, _, bits = struct.unpack('<HHIIHH', buf[pos + 8:pos + 24])
        elif cid == b'data':
            data = buf[pos + 8:pos + 8 + ln]
        pos += 8 + ln + (ln & 1)
    sw = bits // 8
    frame = sw * nch
    fs = float(2 ** (bits - 1) - 1)
    n = len(data) // frame
    out = []
    for i in range(0, n, step):
        b0 = i * frame
        acc = 0
        for c in range(nch):
            acc += int.from_bytes(data[b0 + c * sw:b0 + (c + 1) * sw], 'little', signed=True)
        out.append(acc / nch / fs)
    return out, sr // step


def band_balance(path, step=4):
    """저역(<150Hz) 에너지 vs 고역 트랜지언트(>2kHz 1차 차분) 비율. 베이스/드럼 밸런스 판정용 상대지표."""
    x, sr = wav_samples_mono(path, step)
    # 1-pole LP for low band
    a = math.exp(-2 * math.pi * 150 / sr)
    lo = 0.0
    lo_e = 0.0
    # high band: x - LP(2k)
    a2 = math.exp(-2 * math.pi * 2000 / sr)
    lp2 = 0.0
    hi_e = 0.0
    tot = 0.0
    for v in x:
        lo = a * lo + (1 - a) * v
        lo_e += lo * lo
        lp2 = a2 * lp2 + (1 - a2) * v
        h = v - lp2
        hi_e += h * h
        tot += v * v
    n = len(x)
    db = lambda e: 10 * math.log10(e / n + 1e-12)
    return dict(low_db=round(db(lo_e), 1), high_db=round(db(hi_e), 1), total_db=round(db(tot), 1),
                low_minus_high=round(db(lo_e) - db(hi_e), 1), seconds=round(n / sr, 1))


def peak_dbfs(path):
    x, sr = wav_samples_mono(path, 1)
    return round(20 * math.log10(max(abs(v) for v in x) + 1e-12), 2)


# ---------------------------------------------------------------- end-to-end
def produce(sid, title, ver, mid_path, log=print):
    """열린 프로젝트 정리 → SMF 임포트(벽시계 기준 대기; 임포트 중 System Events 는 ~2분씩 블록) → finish()."""
    t0 = time.time()
    close_all_projects(save=False)
    subprocess.run(['open', '-a', APP, mid_path], capture_output=True)
    while time.time() - t0 < 900:
        if any(w.startswith('무제') and w.endswith('- 트랙') for w in windows()):
            break
        time.sleep(5)
    else:
        return dict(ok=False, stage='open', windows=windows())
    time.sleep(3)
    clear_alerts()
    time.sleep(2)
    r = finish(sid, title, ver, log=log)
    r['elapsed'] = round(time.time() - t0)
    return r


def finish(sid, title, ver, log=print):
    """메트로놈 OFF → 스트립 실측 → 저장(projects/) → bounce_and_post()."""
    proj = f'{title} {ver}'
    log(f'{sid}: metronome {metronome_off("무제 - 트랙")}')
    time.sleep(1)
    open_mixer()
    strips = mixer_strips()
    ok, msg = save_project_as(proj)
    if not ok:
        return dict(ok=False, stage='save', msg=msg, strips=strips)
    r = bounce_and_post(sid, proj, ver)
    r['strips'] = strips
    return r


def bounce_and_post(sid, proj, ver):
    """저장된 프로젝트(창 '{proj} - 트랙')를 AIFF 바운스 → 리미터 → WAV → .aif 삭제 → 저장·닫기 → 번들 이동."""
    for old in (f'{sid}-{ver}.aif', f'{sid}-{ver}.wav'):
        p = os.path.join(BOUNCE_DIR, old)
        if os.path.exists(p):
            os.remove(p)
    close_stray()
    osa(f'''tell application "System Events"
tell process "{APP}"
set frontmost to true
try
perform action "AXRaise" of window "{proj} - 트랙"
end try
end tell
end tell''')
    time.sleep(2)
    ok2, m2 = start_bounce_aiff(proj, f'{sid}-{ver}')
    if not ok2:
        return dict(ok=False, stage='bounce', msg=m2)
    aif = os.path.join(BOUNCE_DIR, f'{sid}-{ver}.aif')
    if not wait_file_stable(aif):
        return dict(ok=False, stage='file', msg='aif missing')
    hits = limit_aiff(aif)
    wav = os.path.join(BOUNCE_DIR, f'{sid}-{ver}.wav')
    okw, ew = aiff_to_wav(aif, wav)
    if not okw:
        return dict(ok=False, stage='wav', msg=ew)
    os.remove(aif)
    save_quiet()
    close_all_projects()
    import glob as _g
    import shutil
    for f in _g.glob(os.path.join(SK_DIR, '*.logicx')):
        dst = os.path.join(PROJ_DIR, os.path.basename(f))
        if os.path.exists(dst):
            shutil.rmtree(dst)
        shutil.move(f, dst)
    return dict(ok=True, wav=wav, mb=os.path.getsize(wav) // 1024 // 1024, knee=hits)
