"""Logic Pro Creator Studio 제작 파이프라인 (2026-08 세션 커널 코드 복원본).

SMF 인코딩 · Logic AX 자동화(임포트/저장/메트로놈/바운스) · 리미터 · WAV 변환 · 오디오 계측.
`docs/music/PROMPT_GUIDELINES.md` §3·§6 의 워크플로를 그대로 코드화한 것.
"""
import hashlib
import math
import os
import plistlib
import random
import re
import shutil
import struct
import subprocess
import tempfile
import time
import unicodedata

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


def build_smf(title, bpm, keysig_sf, minor, n_bars, tracks, pcs, nt, cc, markers=(), timesig=(4, 4), tempos=()):
    """tracks: [(name, midi_ch)], pcs: {idx: program} 또는 None(템플릿 모드: PC 이벤트 없음), nt: {idx: [(tick,dur,pitch,vel)]},
    cc: {idx: [(tick, cc, val)]}, markers: [(bar, text)], timesig: (num, den) with den a power of two,
    tempos: [(tick, bpm)] 추가 템포 이벤트(루바토·아첼레란도). 기본값(4/4, 템포 변화 없음)은 이전 출력과 바이트 동일.
    4/4 가 아니면 bt()/BAR 는 쓰지 말고 bar_ticks = num * PPQ * 4 // den 로 틱을 직접 계산한다(band-fable 7d6d9a0 에서 가져옴)."""
    num, den = timesig
    if not (isinstance(den, int) and den > 0 and den & (den - 1) == 0 and isinstance(num, int) and 1 <= num <= 255):
        raise ValueError(f'timesig must be (1..255, power of two): {timesig}')
    bar_ticks = num * (PPQ * 4 // den)
    cond = [
        meta(0, 0x03, title.encode()),
        meta(0, 0x51, struct.pack('>I', round(60_000_000 / bpm))[1:]),
        meta(0, 0x58, bytes([num, den.bit_length() - 1, 24, 8])),
        meta(0, 0x59, struct.pack('>bB', keysig_sf, 1 if minor else 0)),
        meta(n_bars * bar_ticks, 0x06, b'END'),
    ]
    for tick, tb in tempos:
        cond.append(meta(tick, 0x51, struct.pack('>I', round(60_000_000 / tb))[1:]))
    for bar, text in markers:
        cond.append(meta((bar - 1) * bar_ticks, 0x06, text.encode()))
    chs = [track_chunk(cond)]
    for i, (name, mch) in enumerate(tracks):
        evs = [meta(0, 0x03, name.encode())]
        if pcs is not None:
            evs.append((0, 0, bytes([0xC0 | mch, pcs[i]])))
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
        n_tempo = 0
        n_timesig = 0
        timesig = None
        pcs, ccs = [], []
        first_on = last_off = None
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
                    n_tempo += 1
                if mt == 0x58:
                    timesig = (d[i + 3], 1 << d[i + 4])
                    n_timesig += 1
                i += 3 + ml
            elif st & 0xF0 == 0x90:
                if d[i + 2] > 0:
                    ons += 1
                    first_on = tick if first_on is None else first_on
                else:
                    last_off = tick
                i += 3
            elif st & 0xF0 == 0x80:
                last_off = tick
                i += 3
            elif st & 0xF0 == 0xB0:
                ccs.append(d[i + 1])
                i += 3
            elif st & 0xF0 in (0xA0, 0xE0):
                i += 3
            elif st & 0xF0 == 0xC0:
                pcs.append(d[i + 1])
                i += 2
            elif st & 0xF0 == 0xD0:
                i += 2
            else:
                raise ValueError(f'status {st:02x}')
        info.append(dict(notes=ons, last_tick=mx, tempo_us=tempo_us, n_tempo=n_tempo, n_timesig=n_timesig, timesig=timesig, pcs=pcs, ccs=ccs,
                         first_note_tick=first_on, last_note_off_tick=last_off))
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
    # '… - 트랙' 메인 창 외에 메인 창 없이 남은 '… - 믹서: 트랙' 창도 프로젝트로 본다
    # (2026-10-18 실측: 바운스 뒤 믹서 창만 남으면 임포트가 그 뒤에서 막힘).
    return [w for w in windows() if w.endswith('- 트랙') or w.endswith('- 믹서: 트랙')]


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


# Logic 의 '저장하겠습니까?' 대화상자는 무제 문서면 '저장 안 함', 제목 있는 문서면 '저장하지 않음' 으로
# 버튼 라벨이 다르다 (2026-10-18 실측). 둘 다 시도한다.
DONT_SAVE = ('저장 안 함', '저장하지 않음')


def _click_any(labels):
    tries = '\n'.join(f'try\nclick button "{b}" of w\nexit repeat\nend try' for b in labels)
    return f'repeat with w in windows\n{tries}\nend repeat'


def close_all_projects(save=None):
    """save=None: 무제는 저장 안 함, 제목 있으면 저장. save=False: 전부 저장 안 함."""
    osa(f'''tell application "System Events"
tell process "{APP}"
{_click_any(DONT_SAVE)}
end tell
end tell''')   # 이전 실행이 남긴 '저장하겠습니까?' 대화상자부터 치운다
    for _ in range(4):
        pws = project_windows()
        if not pws:
            return True
        title = pws[0]
        btns = DONT_SAVE if (save is False or title.startswith('무제')) else ('저장',)
        osa(f'''tell application "System Events"
tell process "{APP}"
set frontmost to true
perform action "AXRaise" of window "{title}"
delay 0.5
keystroke "w" using command down
delay 2
{_click_any(btns)}
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
    rc, out, err = osa(f'''tell application "System Events"
tell process "{APP}"
set frontmost to true
delay 0.4
click menu bar item "파일" of menu bar 1
delay 0.6
click menu item "저장" of menu 1 of menu bar item "파일" of menu bar 1
delay 2.5
set w to window "저장"
set sg to splitter group 1 of w
set nameField to missing value
set btns to {{}}
repeat with c in (every UI element of sg)
try
if role of c is "AXTextField" and description of c is "텍스트 필드" then set nameField to c
if role of c is "AXButton" and description of c is "버튼" then set end of btns to c
end try
end repeat
set value of nameField to "{name}"
delay 0.5
click (item (count of btns) of btns)
return "saved"
end tell
end tell''', timeout=90)
    ok = wait_window(f'{name} - 트랙', timeout=60)
    if not ok and any(w == '저장' for w in windows()):
        # 동일 이름 번들이 sketches/ 에 남아 있으면 "대치하겠습니까?" 시트 → 대치
        osa(f'''tell application "System Events"
tell process "{APP}"
try
click button "대치" of sheet 1 of window "저장"
end try
end tell
end tell''')
        ok = wait_window(f'{name} - 트랙', timeout=60)
    close_stray()
    return rc == 0 and ok, out or err


def save_quiet():
    """파일 > 저장 (메뉴). 2026-11-14 실측: `keystroke "s" using command down` 은 한국어 입력 소스에서 '새로운 소프트웨어 악기 트랙'
    으로 해석돼 빈 'Deluxe Classic' 트랙을 만들었다(저장은 안 됨). 메뉴 항목 클릭은 입력 소스와 무관하다."""
    osa(f'''tell application "System Events"
tell process "{APP}"
set frontmost to true
delay 0.4
click menu item "저장" of menu 1 of menu bar item "파일" of menu bar 1
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

# ---------------------------------------------------------------- patch loading (이름으로 패치 올리기)
# SMF 임포트는 GM 프로그램 번호로만 악기를 고른다. 라이브러리 패치(.patch)를 트랙에 올리려면
# ① 트랙 메뉴 "트랙 검색 및 선택…" 으로 트랙을 고르고(키 입력) ② 라이브러리 검색 필드에 패치 이름을 치고
# ③ 결과 표의 행을 AX 로 선택한다. 좌표 클릭(`click at`)은 Logic 에 닿지 않아 쓰지 않는다 (2026-11-09 실측).
def _nfc(s):
    import unicodedata
    return unicodedata.normalize('NFC', s)       # osascript 는 한글을 NFD 로 돌려줄 때가 있다 (windows() 와 같은 이유)


def _as_str(s):
    """AppleScript 문자열 리터럴 안에 넣을 값. 역슬래시·큰따옴표는 이스케이프하고, 결과 구분자 | 는 거부한다."""
    if '|' in s or '\n' in s:
        raise ValueError(f'name cannot contain | or newline: {s!r}')
    return s.replace('\\', '\\\\').replace('"', '\\"')



def _nth(names, i):
    return names[i - 1] if 0 < i <= len(names) else ''


_FIND_BY_DESC = '''on findDesc(el, depth, want)
tell application "System Events"
if depth > 12 then return missing value
try
if (description of el) is want then return el
end try
try
repeat with c in (every UI element of el)
set r to my findDesc(c, depth + 1, want)
if r is not missing value then return r
end repeat
end try
return missing value
end tell
end findDesc
on findRole(el, depth, want)
tell application "System Events"
if depth > 12 then return missing value
try
if (role of el) is want then return el
end try
try
repeat with c in (every UI element of el)
set r to my findRole(c, depth + 1, want)
if r is not missing value then return r
end repeat
end try
return missing value
end tell
end findRole
'''


def _main_window(proj='무제'):
    return f'window "{proj} - 트랙"'


def library_visible(proj='무제'):
    rc, out, err = osa(f'''tell application "System Events"
tell process "{APP}"
return (exists (first UI element of {_main_window(proj)} whose description is "라이브러리")) as text
end tell
end tell''')
    return out == 'true'


def show_library(proj='무제'):
    if library_visible(proj):
        return True
    osa(f'''tell application "System Events"
tell process "{APP}"
set frontmost to true
perform action "AXRaise" of {_main_window(proj)}
delay 0.3
click menu item "라이브러리 보기" of menu 1 of menu bar item "보기" of menu bar 1
end tell
end tell''')
    time.sleep(2)
    return library_visible(proj)


def track_names(proj='무제'):
    """트랙 헤더 순서대로 트랙 이름(= 채널 스트립 이름) 목록."""
    rc, out, err = osa(_FIND_BY_DESC + f'''tell application "System Events"
tell process "{APP}"
set hs to my findDesc((first UI element of {_main_window(proj)} whose description is "그룹"), 0, "트랙 헤더")
if hs is missing value then return ""
set out to ""
repeat with h in UI elements of hs
set out to out & (description of text field 1 of h) & "|"
end repeat
return out
end tell
end tell''', timeout=60)
    return [_nfc(n) for n in out.split('|') if n] if rc == 0 else []


# 인스펙터의 "트랙:" 줄에 적힌 선택 트랙 이름 (트랙 선택이 반영됐는지 확인용). 없으면 "".
_INSPECTOR_TRACK = '''on inspectorTrack(win)
tell application "System Events"
try
set insp to first UI element of win whose description is "인스펙터"
repeat with g in UI elements of list 1 of insp
try
if (value of static text 1 of g) is "트랙:" then return value of text field 1 of g
end try
end repeat
end try
return ""
end tell
end inspectorTrack
'''

# 스트립에서 설명이 desc 인 버튼의 값("켬"/"끔")을 설명으로 다시 찾아 읽는다 (위치 참조가 어긋나도 안전).
_INDICATOR_VALUE = '''on indicatorValue(strip, desc)
tell application "System Events"
try
return value of (first button of strip whose description is desc)
end try
return ""
end tell
end indicatorValue
'''

# 문자열에 ASCII 가 아닌 글자(한글 표시명)가 있는지 — 번역된 라이브러리 표시명과 영어 오타·부분 일치를 가른다.
_HAS_NON_ASCII = '''on hasNonASCII(s)
set cps to id of s
if class of cps is integer then set cps to {cps}
repeat with c in cps
if c > 127 then return true
end repeat
return false
end hasNonASCII
'''


def press_escape():
    """열린 팝오버·메뉴를 닫는다(AX 시간 초과 뒤 정리용). 실패해도 조용히 넘어간다."""
    try:
        osa(f'tell application "System Events" to tell process "{APP}" to key code 53', timeout=15)
    except Exception:
        pass


def select_track(index, proj='무제'):
    """트랙 메뉴 '트랙 검색 및 선택…' 팝오버에 트랙 번호를 치고, 윤곽 목록에서 "<번호>\\t이름" 행을 골라 Return.
    이름이 같은 트랙이 여럿이어도 번호로 고르므로 유일하다. 팝오버가 안 뜨거나 행이 없거나 도중에 오류가 나면
    Escape 로 닫고 실패를 돌려준다. 반환: (성공 여부, 고른 행 텍스트 "<번호>\\t이름" 또는 오류)."""
    index = int(index)
    try:
        rc, out, err = osa(_INSPECTOR_TRACK + f'''tell application "System Events"
tell process "{APP}"
set frontmost to true
perform action "AXRaise" of {_main_window(proj)}
delay 0.3
click menu item "트랙 검색 및 선택…" of menu 1 of menu bar item "트랙" of menu bar 1
set pop to missing value
repeat 10 times
delay 0.4
repeat with w in windows
if (name of w) is "" and (count of UI elements of w) is 1 then
set pop to w
exit repeat
end if
end repeat
if pop is not missing value then exit repeat
end repeat
if pop is missing value then return "ERR no popover"
try
keystroke "{index}"
delay 1.2
set ol to outline 1 of scroll area 1 of group 1 of pop
set hit to missing value
set picked to ""
repeat with r in rows of ol
set t to value of static text 1 of UI element 1 of r
if t starts with "{index}" & tab then
set hit to r
set picked to t
exit repeat
end if
end repeat
if hit is missing value then
key code 53
return "ERR no row for track {index}"
end if
set selected of hit to true
delay 0.3
keystroke return
set want to text ((length of ("{index}" & tab)) + 1) thru -1 of picked
set shown to ""
repeat 16 times
delay 0.5
set shown to my inspectorTrack({_main_window(proj)})
if shown is want then exit repeat
end repeat
if shown is not want then return "ERR inspector shows " & shown & " after selecting " & picked
delay 0.5
return "OK " & picked
on error e
key code 53
return "ERR " & e
end try
end tell
end tell''', timeout=60)
    except subprocess.TimeoutExpired:       # osascript 가 죽으면 on error 의 Escape 도 안 돌므로 여기서 닫는다
        press_escape()
        return False, 'osascript timeout'
    if rc != 0:
        return False, err[:160]
    if not out.startswith('OK '):
        return False, out[:160]
    status, _, picked = out.partition(' ')
    return status == 'OK', _nfc(picked)


def focus_library_slot(slot=None, proj='무제'):
    """인스펙터 채널 스트립의 '라이브러리 표시기' 버튼을 눌러 라이브러리가 보여줄 층을 고른다.
    slot=None → 패치 층(표시기 이름이 플러그인 슬롯 이름과 다른 것; 그 이름이 곧 올라간 패치명),
    slot='Sampler' → 그 플러그인의 프리셋 층(EXS 악기 검색 가능).
    트랙을 바꾼 직후에는 인스펙터 스트립이 아직 이전 트랙 것이거나 반쯤 바뀐 상태라(2026-11-09 실측: 슬롯 그룹과
    표시기 버튼이 다른 트랙 것으로 섞임) 스트립 이름이 인스펙터 "트랙:" 이름과 같고 패치 층 표시기가 정확히 하나일
    때까지 기다린다. 이미 켜진 표시기를 다시 누르면 라이브러리 패널이 닫히므로 켜져 있으면 누르지 않는다.
    반환: (성공 여부, 켜진 표시기 이름, 패치 층 표시기 이름 = 현재 패치명)."""
    want = f'"{_as_str(slot)}"' if slot else 'missing value'
    rc, out, err = osa(_FIND_BY_DESC + _INSPECTOR_TRACK + _INDICATOR_VALUE + f'''tell application "System Events"
tell process "{APP}"
set frontmost to true
set target to missing value
set patchName to ""
set why to ""
repeat 12 times
set target to missing value
set patchName to ""
set insp to first UI element of {_main_window(proj)} whose description is "인스펙터"
set strip to my findRole(insp, 0, "AXLayoutItem")
if strip is missing value then
set why to "no inspector strip"
else
set shown to my inspectorTrack({_main_window(proj)})
if (description of strip) is not shown then
set why to "strip " & (description of strip) & " != inspector " & shown
else
set slots to description of every group of strip
set nPatch to 0
repeat with b in (every button of strip)
set d to ""
try
set d to description of b
end try
if (length of d) > 11 then
if (text 1 thru 11 of d) is "라이브러리 표시기, " then
set nm to text 12 thru -1 of d
if slots does not contain nm then
set nPatch to nPatch + 1
set patchName to nm
if {want} is missing value then set target to b
else if {want} is not missing value and nm is {want} then
set target to b
end if
end if
end if
end repeat
if nPatch is 1 and target is not missing value then exit repeat
set why to "patch indicators=" & nPatch & " target found=" & (target is not missing value)
set target to missing value
end if
end if
delay 0.5
end repeat
if target is missing value then return "ERR no indicator for {slot or 'patch'}: " & why
set td to description of target
-- System Events 참조는 위치(index) 기반이라 스트립이 다시 그려지면 다른 버튼을 가리킨다 → 매번 설명으로 다시 찾는다
set cur to my indicatorValue(strip, td)
if cur is not "켬" then
click (first button of strip whose description is td)
delay 1.5
set cur to my indicatorValue(my findRole((first UI element of {_main_window(proj)} whose description is "인스펙터"), 0, "AXLayoutItem"), td)
end if
if cur is "켬" then return "OK " & (text 12 thru -1 of td) & "|" & patchName
return "ERR indicator did not turn on: " & td & " value=" & cur
end tell
end tell''', timeout=90)
    if rc != 0:
        return False, err[:160], ''
    status, _, rest = out.partition(' ')
    on, _, patch = rest.partition('|')
    return status == 'OK', _nfc(on), _nfc(patch)


def library_pick(patch, proj='무제'):
    """라이브러리 검색 필드에 patch 를 치고 결과 표에서 이름이 정확히 같은 행을 선택한다(선택 = 로드).
    정확히 같은 행이 없을 때, 결과가 **한 행뿐이고 그 이름에 ASCII 가 아닌 글자(한글 표시명)가 있으면** 그 행을 고른다 —
    최신 팩 패치는 한국어 UI 에서 표시명이 번역돼 있어(실측: `Tonewheel Organ` → 표시 "톤휠 오르간") 파일 이름으로
    검색은 되지만 글자가 다르기 때문이다. 영어 이름 한 행(오타·부분 일치, 예: `Bassoon` → `Bassoon Solo`)은 MISS 다.
    반환: (성공 여부, 결과 행 이름 목록, 실제로 고른 행 이름 또는 '', 대체 여부)."""
    patch_lit = _as_str(patch)
    rc, out, err = osa(_FIND_BY_DESC + _HAS_NON_ASCII + f'''tell application "System Events"
tell process "{APP}"
set frontmost to true
if not (exists (first UI element of {_main_window(proj)} whose description is "라이브러리")) then return "ERR no library pane"
set lib to first UI element of {_main_window(proj)} whose description is "라이브러리"
set tf to my findDesc(lib, 0, "텍스트 필드 검색")
if tf is missing value then return "ERR no search field"
set names to ""
set hit to missing value
set lastValue to ""
repeat 3 times
set tf to my findDesc(lib, 0, "텍스트 필드 검색")
if tf is missing value then return "ERR no search field"
set focused of tf to true
delay 0.3
set value of tf to "{patch_lit}"
keystroke return
delay 1.2
repeat 6 times
set lastValue to value of tf
if lastValue is not "{patch_lit}" then exit repeat
set t to my findRole(lib, 0, "AXTable")
if t is not missing value then
set names to ""
set nRows to 0
set lone to missing value
repeat with r in rows of t
set n to value of UI element 1 of UI element 1 of r
set names to names & n & "|"
set nRows to nRows + 1
set lone to r
considering case
if n is "{patch_lit}" and hit is missing value then set hit to r
end considering
end repeat
if hit is missing value and nRows is 1 and my hasNonASCII(value of UI element 1 of UI element 1 of lone) then set hit to lone
if hit is not missing value then exit repeat
end if
delay 0.5
end repeat
if hit is not missing value then exit repeat
delay 1.0
end repeat
if hit is missing value then return "MISS |" & names & "(field=" & lastValue & ")"
set gotName to value of UI element 1 of UI element 1 of hit
set selected of hit to true
delay 2.5
considering case
if gotName is "{patch_lit}" then return "OK " & gotName & "|" & names
end considering
return "SUBST " & gotName & "|" & names
end tell
end tell''', timeout=90)
    if rc != 0:
        return False, [err[:120]], '', False
    status, _, rest = out.partition(' ')
    got, _, names = rest.partition('|')
    rows = [_nfc(n) for n in names.split('|') if n]
    if status not in ('OK', 'SUBST'):
        return False, rows, '', False
    return True, rows, _nfc(got), status == 'SUBST'


def load_patches(patches, proj='무제', log=print):
    """patches: {track_index(1-based, SMF 트랙 순서): spec}. spec 은
      'Harpsichord'                 라이브러리 패치(.patch) 이름 — 파일 이름(확장자 제외). 라이브러리 표시명이 번역돼
                                     있어(한글) 검색 결과가 그 한 행뿐이면 그 행을 올리고 결과에 대체 표식을 남긴다(library_pick).
      ('Violins 1', 'Violin (Arco)') (Sampler 를 쓰는 패치, Sampler 프리셋/EXS 악기 이름) — 패치를 먼저 올려 Sampler 를
                                     확보하고, 인스펙터의 Sampler 라이브러리 표시기로 층을 바꿔 EXS 악기를 올린다.
    번호로 트랙을 고르므로 이름이 겹쳐도 안전하다. 확인: 패치는 (선택된 트랙의) 인스펙터 패치 층 '라이브러리 표시기'
    이름이 고른 행 이름과 같고, i 번째 트랙 헤더를 읽을 수 있으며 그 헤더가 임포트 때 이름에서 바뀌었거나 고른 이름과
    같거나(채널 스트립 이름은 패치 파일 이름과 다를 수 있다 — 실측 `Studio Alto Sax 1` → "(New) Horns") 로드 전부터
    같은 패치였어야 한다. EXS 는 헤더가 고른 EXS 이름으로 바뀌어야 한다(임포트로 자동 명명된 트랙 기준 — 사람이 이름을
    바꾼 트랙은 이름이 안 바뀐다, 2026-11-09 실측).
    선행 조건: 임포트된 '<proj> - 트랙' 창. 반환: {index: (spec, ok, (올라간 패치 표시명, EXS 표시명 또는 None, 헤더 이름,
    대체 여부))}; 하나라도 실패면 RuntimeError."""
    for i, spec in patches.items():
        parts = spec if isinstance(spec, tuple) else (spec,)
        if (type(i) is not int or (isinstance(spec, tuple) and len(parts) != 2)
                or not all(isinstance(p, str) and p for p in parts)):
            raise ValueError(f'bad patch spec {i!r}: {spec!r} — int 번호와 "패치" 또는 ("패치", "EXS") 만 받는다')
        for p in parts:
            _as_str(p)
    if not show_library(proj):
        raise RuntimeError('library pane not available')
    names = track_names(proj)
    if not names:
        raise RuntimeError('no track headers found')
    bad = [i for i in patches if not 1 <= i <= len(names)]
    if bad:
        raise RuntimeError(f'track index out of range {bad}: headers {names}')
    results = {}
    for i in sorted(patches):
        spec = patches[i]
        base, exs = (spec if isinstance(spec, tuple) else (spec, None))
        ok_sel, picked = select_track(i, proj)
        if not ok_sel or picked != f'{i}\t{names[i - 1]}':
            raise RuntimeError(f'track {i}: select failed (picked={picked!r}, expected {names[i - 1]!r})')
        ok_focus, _, before = focus_library_slot(None, proj)  # 앞 트랙에서 Sampler 층을 봤더라도 패치 층으로 되돌린다
        ok_pick, rows, got, subst = library_pick(base, proj) if ok_focus else (False, [], '', False)
        ok_ind, _, loaded = focus_library_slot(None, proj)   # 올라간 패치명 읽기 (표시기 이름)
        name = _nth(track_names(proj), i)
        # 표시기는 '선택된' 트랙의 것이고 헤더는 i 번째 트랙의 것 — 둘 다 맞아야 엉뚱한 트랙에 올라간 경우를 거른다.
        # 헤더를 못 읽으면(빈 문자열) 실패. 헤더가 그대로여도 로드 전 표시기가 이미 그 패치였으면(GM 으로 올라온 같은 패치) 통과.
        ok = bool(ok_pick and ok_ind and loaded == got and name
                  and (name != names[i - 1] or name == got or before == got))
        got_exs = None
        if ok and exs:
            ok_focus, desc, _ = focus_library_slot('Sampler', proj)
            ok_pick, rows, got_exs, subst_exs = library_pick(exs, proj) if ok_focus else (False, [desc], '', False)
            subst = subst or subst_exs
            name = _nth(track_names(proj), i)
            ok = bool(ok_pick and name and name == got_exs)
        results[i] = (spec, ok, (loaded, got_exs, name, subst))
        log(f'track {i}: {names[i - 1]} -> {spec}: {"OK" if ok else "FAIL"}{" SUBST" if subst else ""} '
            f'(patch={loaded}, exs={got_exs}, header={name}, results={rows[:5]})')
    failed = {i: r for i, r in results.items() if not r[1]}
    if failed:
        raise RuntimeError(f'patch load failed: {failed}')
    return results


# 바운스 대화상자 '종료:' 그룹의 첫 슬라이더(마디). AXIncrement/AXDecrement 는 ±10 마디, `set value` 는 값과 무관하게 −1 마디
# (2026-11-14 실측). 템플릿 모드는 프로젝트 끝이 템플릿 값(기본 129 마디)이라 SMF 길이로 줄여야 한다.
BOUNCE_END_STEPPER = '''
set grp to missing value
set seen to false
repeat with e in (every UI element of w)
try
if (role of e) is "AXStaticText" and (value of e) is "종료:" then set seen to true
if seen and (role of e) is "AXGroup" and grp is missing value then set grp to e
end try
end repeat
if grp is missing value then return "no end group"
set s to slider 1 of grp
-- 그룹 텍스트는 늦게 갱신되므로 슬라이더 값(즉시 갱신)으로 마디를 계산한다: 1마디 내리고 값 차이를 잰다
set bar0 to (word 1 of (value of grp as text)) as integer
set v0 to value of s
set value of s to 0
delay 0.3
set v1 to value of s
set per to v0 - v1
if per ≤ 0 then return "end slider did not move"
repeat 600 times
set bar to (round ((value of s) - v1) / per) + bar0 - 1
if bar = {end_bar} then exit repeat
if bar - {end_bar} ≥ 10 then
perform action "AXDecrement" of s
else if bar < {end_bar} then
perform action "AXIncrement" of s
else
set value of s to 0
end if
delay 0.12
end repeat
delay 0.8
if ((word 1 of (value of grp as text)) as integer) is not {end_bar} then return "end bar not set: " & (value of grp as text)
'''


def start_bounce_aiff(proj_name, file_name, end_bar=None):
    stepper = BOUNCE_END_STEPPER.format(end_bar=end_bar) if end_bar else ''
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
{stepper}
perform action "AXRaise" of w
key code 36
delay 3
-- 저장 위치는 건드리지 않는다. ⌘⇧G '폴더로 이동' 팝오버는 합성 입력(키·클릭·AX)을 전혀 받지 않아
-- 모달로 남아 세션을 막는다(2026-10-19 실측). 대신 bounce_and_post() 가 후보 폴더에서 파일을 찾아 옮긴다.
set sg to splitter group 1 of w
set nameField to missing value
set btns to {{}}
repeat with c in (every UI element of sg)
try
if role of c is "AXTextField" and description of c is "텍스트 필드" then set nameField to c
if role of c is "AXButton" and description of c is "버튼" then set end of btns to c
end try
end repeat
if nameField is missing value then return "no name field"
set value of nameField to "{file_name}"
delay 0.5
click (item (count of btns) of btns)
delay 2
repeat with w3 in windows
try
click button "대치" of w3
end try
end repeat
return "bounce started"
end tell
end tell''', timeout=120)
    return 'bounce started' in out, out or err


# 바운스 대화상자의 저장 위치는 Logic 이 마지막으로 쓴 곳(재시작 후에는 .mid 폴더)이라 통제하지 않는다.
# 파일명으로 후보 폴더를 뒤져 bounces/ 로 옮긴다 (2026-10-18 dh20, 2026-10-19 v2 실측).
import glob as _glob
BOUNCE_SEARCH = [BOUNCE_DIR, SK_DIR, PROJ_DIR, os.path.expanduser('~/Music'), os.path.expanduser('~/Music/Logic/Bounces'), os.path.expanduser('~/Desktop'),
                 os.path.expanduser('~/Documents'), os.path.expanduser('~/Downloads')]
# 다른 워크트리(세션)의 sketches/ 도 본다 — Logic 바운스 대화상자는 마지막으로 쓴 폴더를 기억하므로
# 다른 세션이 자기 sketches/ 로 바운스했으면 다음 바운스가 거기로 떨어진다 (2026-10-30 실측: band-fable/docs/music/sketches).
_WT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..'))
BOUNCE_SEARCH += sorted(d for d in _glob.glob(os.path.join(_WT_ROOT, '*', 'docs', 'music', 'sketches')) if d not in BOUNCE_SEARCH)
BOUNCE_SEARCH += [d for d in ('/Volumes/Netac 2TB/workspace/losik/docs/music/sketches',) if os.path.isdir(d) and d not in BOUNCE_SEARCH]


def _aiff_ready(path):
    """Only complete stereo PCM24 big-endian AIFF can enter the in-place limiter."""
    with open(path, 'rb') as f:
        physical = os.fstat(f.fileno()).st_size
        header = f.read(12)
        if len(header) < 12:
            return False
        if header[:4] != b'FORM' or header[8:] not in (b'AIFF', b'AIFC'):
            raise ValueError(f'Not AIFF: {path}')
        end = 8 + struct.unpack('>I', header[4:8])[0]
        if end != physical:
            return False
        pos, comm, audio_size = 12, None, None
        while pos + 8 <= end:
            f.seek(pos)
            kind, size = struct.unpack('>4sI', f.read(8))
            if pos + 8 + size + (size & 1) > end:
                return False
            if kind == b'COMM':
                body = f.read(min(size, 22))
                if len(body) < 18:
                    return False
                channels, frames, bits = struct.unpack('>HIH', body[:8])
                compression = body[18:22] if header[8:] == b'AIFC' else b'NONE'
                comm = channels, frames, bits, compression
            elif kind == b'SSND':
                if size < 8:
                    return False
                offset, _ = struct.unpack('>II', f.read(8))
                audio_size = size - 8 - offset
            pos += 8 + size + (size & 1)
        if pos != end or comm is None or audio_size is None:
            return False
        channels, frames, bits, compression = comm
        if not frames or audio_size != frames * channels * ((bits + 7) // 8):
            return False
        if channels != 2 or bits != 24 or compression not in (b'NONE', b'twos'):
            raise ValueError(f'Expected stereo big-endian PCM24 AIFF, got {comm}: {path}')
        return True


def wait_bounce_file(name, timeout=600, since=None):
    """후보 폴더 중 하나에 name 이 안정적으로 생기면 BOUNCE_DIR 로 옮긴 경로를, 아니면 None.
    since 가 주어지면 그 시각 이전의 파일(옛 잔재)은 무시한다."""
    import shutil
    t0 = time.time()
    while time.time() - t0 < timeout:
        for d in BOUNCE_SEARCH:
            p = os.path.join(d, name)
            try:
                if os.path.exists(p) and os.path.getsize(p) > 500000 and (since is None or os.path.getmtime(p) >= since) and _aiff_ready(p):
                    s = os.path.getsize(p)
                    time.sleep(3)
                    if os.path.getsize(p) == s and _aiff_ready(p):
                        dst = os.path.join(BOUNCE_DIR, name)
                        if p != dst:
                            shutil.move(p, dst)
                        return dst
            except OSError:
                continue   # Logic 이 아직 쓰는 중이거나 사라짐 — 다음 폴링에서 다시 본다
        time.sleep(3)
    return None


def wait_file_stable(path, min_size=500000, timeout=600):
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
LOCK_PATH = os.path.join(os.path.dirname(BOUNCE_DIR), '.logic-lock')   # Netac 공유 — 세션(워크트리)들이 Logic 한 대를 나눠 쓴다


class LogicLock:
    """Logic 은 한 인스턴스뿐이라 세션 간 바운스를 직렬화한다. 다른 세션이 쥐고 있으면 기다린다(최대 wait 초).
    해제는 자기 토큰이 적힌 파일만 지운다(다른 세션의 잠금을 지우지 않도록). 폴링 간격은 짧게 두어 기아를 줄인다.
    세션이 죽어 파일이 남으면 내용(소유자·pid·시각)을 보고 사람이 지운다."""
    def __init__(self, owner, wait=3600):
        self.owner, self.wait = owner, wait
        self.token = f'{owner} {os.getpid()} {time.strftime("%F %T")} {os.urandom(4).hex()}'

    def __enter__(self):
        deadline = time.time() + self.wait
        while True:
            try:
                fd = os.open(LOCK_PATH, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
            except FileExistsError:
                if time.time() > deadline:
                    try:
                        held = open(LOCK_PATH).read().strip()
                    except FileNotFoundError:
                        continue          # 방금 풀렸다 — 한 번 더 시도
                    raise TimeoutError(f'Logic lock held: {held} ({LOCK_PATH})')
                time.sleep(2)
                continue
            try:
                os.write(fd, (self.token + '\n').encode())
            except BaseException:
                os.close(fd)
                os.remove(LOCK_PATH)
                raise
            os.close(fd)
            return self

    def __exit__(self, *exc):
        try:
            if open(LOCK_PATH).read().strip() == self.token:
                os.remove(LOCK_PATH)
        except FileNotFoundError:
            pass
        time.sleep(3)   # 폴링(2s) 중인 다른 세션이 끼어들 틈을 준다 — 한 세션이 12곡을 독점하지 않도록


def restart_logic(log=print, owner=None):
    """Logic 종료 (다음 produce() 가 다시 띄운다). 세션 간 잠금 안에서 실행 — 다른 세션의 바운스 중 죽이지 않도록."""
    owner = owner or _worktree_name()
    with LogicLock(owner):
        subprocess.run(['osascript', '-e', f'tell application "{APP}" to quit'], capture_output=True)
        for _ in range(30):
            if subprocess.run(['pgrep', '-f', APP + '$'], capture_output=True).returncode:
                break
            time.sleep(2)
        log('    logic restarted')


def _worktree_name():
    return os.path.basename(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))


def produce(sid, title, ver, mid_path, log=print, owner=None, patches=None, select=None, template=None):
    """열린 프로젝트 정리 → SMF 임포트(벽시계 기준 대기; 임포트 중 System Events 는 ~2분씩 블록) → finish().
    patches: load_patches() 의 {트랙 번호: 패치 spec} — 임포트 뒤, 바운스 전에 라이브러리 패치/EXS 를 올린다.
      임포트된 트랙 수가 SMF 의 악기 트랙 수(프로그램 체인지가 있는 트랙)와 다르면 stage='tracks' 로 멈춘다 —
      지휘 트랙에 텍스트·저작권 메타가 있으면 Logic 이 빈 트랙을 만들어 번호가 밀린다(2026-11-09 band-fable·astra 실측).
    select: 패치 로드 뒤 선택해 둘 트랙 번호(1-based). 바운스 범위가 선택 트랙의 마지막 리전 끝으로 잡히므로(finish() 참조)
      기본값 None 이면 patches 가 있을 때 SMF 에서 마지막 틱이 가장 늦은 악기 트랙을 골라 자동으로 선택한다.
    template: 템플릿 .logicx 경로 — 있으면 produce_template() 로 간다(사본에 임포트해 템플릿 스트립으로 연주; patches·select 와 함께 쓰지 않는다).
    세션 간 Logic 경합을 막기 위해 LogicLock 을 잡고 돈다(owner 기본값 = 현재 워크트리 이름)."""
    if template is not None:
        if patches is not None or select is not None:
            raise TemplateError('template= cannot be combined with patches=/select=')
        return produce_template(sid, title, ver, mid_path, template, log=log, owner=owner)
    owner = owner or _worktree_name()
    with LogicLock(owner):
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
        imported_tracks = None
        if patches is not None:
            with open(mid_path, 'rb') as midi:
                _, _, _, midi_tracks = parse_smf(midi.read())
            inst = [t for t in midi_tracks if t['pcs']]
            imported_tracks = track_names()
            if len(imported_tracks) != len(inst):
                return dict(ok=False, stage='tracks', expected=len(inst), tracks=imported_tracks)
            if select is None and patches and inst:
                select = max(range(len(inst)), key=lambda i: inst[i]['last_tick']) + 1
        r = finish(sid, title, ver, log=log, patches=patches, select=select)
        r['elapsed'] = round(time.time() - t0)
        if imported_tracks is not None:
            r['imported_tracks'] = imported_tracks
        return r


def finish(sid, title, ver, log=print, patches=None, select=None, win_title='무제 - 트랙'):
    """(패치 로드 → 끝 트랙 선택 →) 메트로놈 OFF → 스트립 실측 → 저장(projects/) → bounce_and_post().
    select: 패치를 올린 뒤 선택해 둘 트랙 번호(1-based). load_patches() 가 마지막으로 고른 트랙이 선택된 채 남으면
    '프로젝트 또는 섹션…' 바운스의 끝이 그 트랙의 마지막 리전 끝으로 잡혀 곡이 잘린다(2026-11-09 band-fable 실측:
    spring 1 72마디 중 53마디, winter 1 88 중 66 — 모두 마지막 패치 트랙의 리전 끝과 일치; 선택 해제 ⇧⌘A 는 효과 없음).
    produce() 는 patches 가 있으면 SMF 에서 가장 늦게 끝나는 악기 트랙을 자동으로 넘긴다; 직접 부를 때는 끝까지
    연주하는 트랙 번호를 넘긴다."""
    proj = f'{title} {ver}'
    loaded = None
    if patches:
        try:
            loaded = load_patches(patches, log=log)
        except Exception as e:          # 이름 오류(ValueError)·AX 시간 초과(TimeoutExpired)도 배치를 끊지 않고 곡 단위 실패로 돌려준다
            press_escape()              # 남은 팝오버·메뉴를 닫는다(다음 produce() 의 close_all_projects 가 막히지 않도록)
            try:
                tracks = track_names()
            except Exception:
                tracks = []
            return dict(ok=False, stage='patches', msg=f'{type(e).__name__}: {e}', tracks=tracks)
    if select is not None:
        try:
            ok_sel, picked = select_track(select)
        except Exception as e:          # AX 시간 초과 등도 곡 단위 실패로 (load_patches 와 같은 계약)
            ok_sel, picked = False, f'{type(e).__name__}: {e}'
        log(f'{sid}: select track {select} -> {ok_sel} {picked!r}')
        if not ok_sel:
            try:
                tracks = track_names()
            except Exception:
                tracks = []
            return dict(ok=False, stage='select', msg=picked, tracks=tracks, patches=loaded)
    log(f'{sid}: metronome {metronome_off(win_title)}')
    time.sleep(1)
    open_mixer()
    strips = mixer_strips()
    ok, msg = save_project_as(proj)
    if not ok:
        return dict(ok=False, stage='save', msg=msg, strips=strips)
    r = bounce_and_post(sid, proj, ver)
    r['strips'] = strips
    if loaded is not None:
        r['patches'] = loaded
    return r


def bounce_and_post(sid, proj, ver, end_bar=None):
    """저장된 프로젝트(창 '{proj} - 트랙')를 AIFF 바운스 → 리미터 → WAV → .aif 삭제 → 저장·닫기 → 번들 이동."""
    # 탐색 폴더 전부에서 동명 잔재를 지운다 — 다른 폴더의 옛 .aif 를 새 바운스로 오인하지 않도록.
    # 형제 워크트리의 sketches/ 도 포함: LogicLock 이 바운스를 직렬화하므로 거기 있는 동명 .aif 는 진행 중이 아니라 잔재다.
    for d in BOUNCE_SEARCH:
        for old in (f'{sid}-{ver}.aif', f'{sid}-{ver}.wav' if d == BOUNCE_DIR else None):
            if old and os.path.exists(os.path.join(d, old)):
                os.remove(os.path.join(d, old))
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
    t_start = time.time() - 5
    ok2, m2 = start_bounce_aiff(proj, f'{sid}-{ver}', end_bar=end_bar)
    if not ok2:
        return dict(ok=False, stage='bounce', msg=m2)
    try:
        aif = wait_bounce_file(f'{sid}-{ver}.aif', since=t_start)
    except ValueError as exc:
        return dict(ok=False, stage='format', msg=str(exc))
    if not aif:
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


# ---------------------------------------------------------------- template mode (seed 20261113-220009-a606)
# 템플릿 .logicx(사용자가 악기를 올려 둔 프로젝트)의 복사본을 열고 SMF 를 템플릿의 채널 스트립으로 연주하게 한다.
# 원본은 Logic 으로 열지 않고, 저장은 ⌘S(save_quiet)만 쓴다. 대화상자는 라벨로만 누른다.
#
# 2026-11-13 실측(AC0): Logic 12.4 의 MIDI 임포트는 열린 프로젝트에서도 항상 새 트랙을 만든다('기존 트랙 사용' 선택지 없음,
# `open -a` 는 새 프로젝트를 연다). 그래서 순서는 ① 파일 > 가져오기 > MIDI 파일… 로 새 트랙 n+1..2n 에 임포트(템포 대화상자
# '템포 가져오기') → ② 새 트랙 i 를 트랙 헤더 컨텍스트 메뉴 '트랙 다시 할당 > 믹서 > 소프트웨어 악기 > <이름> (Inst i)' 로 템플릿
# 스트립에 재할당 → ③ 트랙 > 사용하지 않는 트랙 삭제(리전 없는 원래 트랙 1..n 제거). 열기 패널의 파일 목록과 컨텍스트 메뉴는
# AX 에 노출되지 않아 CGEvent(ax/cgevent.js) + Vision OCR(ax/ocr) 로 텍스트를 찾아 누른다.

class TemplateError(Exception):
    pass


# 시작 시점에 떠 있어도 되는 창(프로젝트 창은 아무것도 열려 있으면 안 된다).
START_ALLOWED_WINDOWS = ('프로젝트 선택',)
AX_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ax')
OCR_BIN = os.path.join(AX_DIR, 'ocr')
CGEVENT_JS = os.path.join(AX_DIR, 'cgevent.js')
SCREEN_SCALE = 2   # Retina: 픽셀/포인트
REGION_KEY_LEN = 12   # 리전 라벨 OCR 매칭에 쓰는 SMF 트랙 이름 앞글자 수(라벨은 잘릴 수 있다)


def windows_strict():
    """Logic 창 이름(NFC). windows() 와 달리 조회 실패는 예외 — 오류를 '창 없음' 으로 읽지 않는다."""
    rc, out, err = osa(f'''tell application "System Events"
tell process "{APP}"
set out to ""
repeat with w in windows
set out to out & "|" & (name of w)
end repeat
return out
end tell
end tell''')
    if rc != 0:
        raise RuntimeError(f'window list failed: {err[:80]}')
    return [unicodedata.normalize('NFC', w) for w in out.split('|')[1:]]


def template_meta(path):
    """Alternatives/000/MetaData.plist 의 NumberOfTracks·BeatsPerMinute (Logic 을 건드리지 않는다)."""
    p = os.path.join(path, 'Alternatives', '000', 'MetaData.plist')
    if not os.path.isfile(p):
        raise TemplateError(f'no MetaData.plist: {p}')
    with open(p, 'rb') as f:
        d = plistlib.load(f)
    tracks, bpm = d.get('NumberOfTracks'), d.get('BeatsPerMinute')
    if not isinstance(tracks, int) or isinstance(tracks, bool) or tracks <= 0:
        raise TemplateError(f'bad NumberOfTracks: {tracks!r}')
    if not isinstance(bpm, (int, float)) or isinstance(bpm, bool) or bpm <= 0:
        raise TemplateError(f'bad BeatsPerMinute: {bpm!r}')
    return dict(tracks=tracks, bpm=float(bpm))


def tree_hash(path):
    """번들 안 모든 파일의 상대 경로·크기·내용을 프레이밍한 sha256. 심볼릭 링크는 거부."""
    h = hashlib.sha256()
    for root, dirs, files in os.walk(path):
        dirs.sort()
        for name in dirs + files:
            if os.path.islink(os.path.join(root, name)):
                raise TemplateError(f'symlink in bundle: {os.path.join(root, name)}')
        for name in sorted(files):
            full = os.path.join(root, name)
            rel = os.path.relpath(full, path).encode()
            h.update(b'F' + rel + b'\0' + str(os.path.getsize(full)).encode() + b'\0')
            with open(full, 'rb') as f:
                for chunk in iter(lambda: f.read(1 << 20), b''):
                    h.update(chunk)
    return h.hexdigest()


def failed_name(proj, ts):
    return f'{proj}.failed-{ts}.logicx'


def preflight_template(template, proj, mid_path):
    """Logic 을 만지기 전에 끝나는 검사: 템플릿 존재, 사본 경로 비어 있음, SMF 음악 트랙 수(conductor 제외) ≤ NumberOfTracks."""
    if re.search(r'[\"\\\\/\n|]', proj) or re.search(r'[\"\\\\\n|]', os.path.basename(mid_path)):
        raise TemplateError(f'name contains quote/backslash/slash/pipe (breaks osascript, paths or window parsing): {proj!r} {os.path.basename(mid_path)!r}')
    if not os.path.isdir(template):
        raise TemplateError(f'template not found: {template}')
    copy = os.path.join(PROJ_DIR, f'{proj}.logicx')
    if os.path.exists(copy):
        raise TemplateError(f'copy already exists: {copy}')
    with open(mid_path, 'rb') as f:
        buf = f.read()
    _, ntrk, div, info = parse_smf(buf)
    if div != PPQ:
        raise TemplateError(f'SMF division {div} != PPQ {PPQ} (bar math assumes build_smf output)')
    smf_tracks = ntrk - 1
    names = smf_track_names(buf)
    keys = [unicodedata.normalize('NFC', n)[:REGION_KEY_LEN] for n in names]
    if len(set(keys)) != len(keys) or any(not k.strip() for k in keys) or \
            any(a != b and b.startswith(a) for a in keys for b in keys):
        raise TemplateError(f'SMF track names must be non-empty, distinct and prefix-free in the first {REGION_KEY_LEN} chars (region OCR key; e.g. "Violin"/"Violin 2" clash): {names}')
    cond = info[0]
    if cond['tempo_us'] is None or cond['n_tempo'] != 1:
        raise TemplateError(f'template mode needs exactly one tempo event in the conductor track (got {cond["n_tempo"]}) — 템포맵 곡은 미실측')
    if cond['n_timesig'] > 1 or cond['timesig'] not in (None, (4, 4)):
        raise TemplateError(f'template mode is measured for constant 4/4 only (SMF conductor: {cond["n_timesig"]} time-signature events, last {cond["timesig"]}): 바운스 종료 마디 계산과 구간 판정이 4/4 기준')
    if any(tr['n_tempo'] or tr['n_timesig'] for tr in info[1:]):
        raise TemplateError('tempo/time-signature events outside the conductor track are not supported in template mode')
    smf_bpm = round(60_000_000 / cond['tempo_us'], 3)
    smf_end_bar = (max(tr['last_tick'] for tr in info) + BAR - 1) // BAR + 1   # 마지막 이벤트가 든 마디의 다음 마디 시작(4/4, 올림) — 바운스 '종료:' 는 그 마디 시작에서 끝난다
    meta_ = template_meta(template)
    if smf_tracks != meta_['tracks']:
        raise TemplateError(f'SMF has {smf_tracks} tracks but template NumberOfTracks is {meta_["tracks"]} (must match: 남는 템플릿 트랙은 사용하지 않는 트랙 삭제 에 지워져 스트립이 어긋난다)')
    return dict(meta_, smf_tracks=smf_tracks, smf_bpm=smf_bpm, smf_end_bar=smf_end_bar, copy=copy)


def strip_names(raw):
    """mixer_strips() 원문 '[A] [B] …' → 트랙 순서의 이름 (출력·마스터·숫자만인 항목 제외)."""
    names = re.findall(r'\[([^\]]*)\]', raw)
    return [n for n in names if n not in ('Stereo Out', 'Master') and not n.replace(' ', '').isdigit()]


# ---- CGEvent + OCR primitives
def ensure_ocr():
    src = OCR_BIN + '.swift'
    if not os.path.isfile(OCR_BIN) or os.path.getmtime(src) > os.path.getmtime(OCR_BIN):
        r = subprocess.run(['swiftc', '-O', '-o', OCR_BIN, src], capture_output=True, text=True)
        if r.returncode:
            raise TemplateError(f'ocr build failed: {r.stderr[:200]}')


def cg(cmd, x, y, n=1):
    r = subprocess.run(['osascript', '-l', 'JavaScript', CGEVENT_JS, cmd, str(round(x)), str(round(y)), str(n)],
                       capture_output=True, text=True, timeout=30)
    if r.returncode:
        raise TemplateError(f'cgevent {cmd} failed (접근성 권한?): {r.stderr[:120]}')


def front_window_rect():
    """Logic 맨 앞 프로젝트 창의 (x, y, w, h) 포인트 — OCR 캡처를 이 영역으로 제한해 다른 앱의 텍스트를 클릭하지 않게 한다."""
    rc, out, err = osa(f'''tell application "System Events"
tell process "{APP}"
repeat with w in windows
if (name of w) ends with "- 트랙" then
set p to position of w
set s to size of w
return (item 1 of p as text) & "," & (item 2 of p as text) & "," & (item 1 of s as text) & "," & (item 2 of s as text)
end if
end repeat
return ""
end tell
end tell''')
    try:
        x, y, w, h = (int(float(v)) for v in out.split(','))
        return x, y, w, h
    except ValueError:
        return None


def ocr_screen():
    """화면 캡처 → [(text, cx, cy, x, y, w, h)] 포인트 좌표. 프로젝트 창이 있으면 그 영역만 캡처한다."""
    ensure_ocr()
    fd, png = tempfile.mkstemp(prefix='losik-ocr-', suffix='.png')
    os.close(fd)
    try:
        rect = front_window_rect()
        cmd = ['screencapture', '-x'] + (['-R', '{},{},{},{}'.format(*rect)] if rect else []) + [png]
        subprocess.run(cmd, check=True)
        r = subprocess.run([OCR_BIN, png, str(SCREEN_SCALE)], capture_output=True, text=True, timeout=120)
        if r.returncode:
            raise TemplateError(f'ocr failed (화면 기록 권한?): {r.stderr[:120]}')
        out = r.stdout
    finally:
        os.remove(png)
    ox, oy = (rect[0], rect[1]) if rect else (0, 0)
    items = []
    for line in out.splitlines():
        box, _, text = line.partition('\t')
        x, y, w, h = map(int, box.split(','))
        x += ox; y += oy
        items.append((unicodedata.normalize('NFC', text), x + w / 2, y + h / 2, x, y, w, h))
    return items


def ocr_find(pat, timeout=8, pred=None):
    rx = re.compile(pat)
    t0 = time.time()
    while True:
        hits = [it for it in ocr_screen() if rx.search(it[0]) and (pred is None or pred(it))]
        if hits:
            return hits
        if time.time() - t0 > timeout:
            raise TemplateError(f'text not on screen: {pat}')
        time.sleep(0.7)


def hover_submenu(pat, timeout=8):
    """메뉴 항목 텍스트 위로 포인터를 옮기고, 오른쪽으로 더 옮겨 서브메뉴를 연다."""
    h = ocr_find(pat, timeout=timeout)[0]
    cg('move', h[1], h[2]); time.sleep(0.6)
    cg('move', h[3] + h[5] + 40, h[2]); time.sleep(0.9)
    return h


def menu_click(*path):
    """메뉴 막대 경로 클릭 (AX). path 는 ('파일', '가져오기', 'MIDI 파일…') 처럼 이름 열."""
    bar = f'menu bar item "{path[0]}" of menu bar 1'
    ref = f'menu 1 of {bar}'
    for p in path[1:-1]:
        ref = f'menu 1 of menu item "{p}" of {ref}'
    rc, out, err = osa(f'''tell application "System Events"
tell process "{APP}"
set frontmost to true
click menu item "{path[-1]}" of {ref}
end tell
end tell''')
    if rc != 0:
        raise TemplateError(f'menu click failed {path}: {err[:120]}')


def click_dialog_button(window_name, label, timeout=60):
    """이름 있는 대화상자(템포 가져오기 등)의 버튼을 라벨로 누른다. AX 에 보이는 대화상자 전용."""
    t0 = time.time()
    while time.time() - t0 < timeout:
        rc, out, err = osa(f'''tell application "System Events"
tell process "{APP}"
repeat with w in windows
try
if (name of w) is "{window_name}" then
click button "{label}" of w
return "ok"
end if
end try
end repeat
return ""
end tell
end tell''')
        if out == 'ok':
            return True
        time.sleep(1)
    return False


def lcd_tempo_value():
    """컨트롤 막대 LCD 템포 슬라이더 값(float). lcd_tempo() 의 텍스트 탐색이 빈 값을 주는 경우가 있어 슬라이더를 읽는다."""
    rc, out, err = osa(f'''on findS(el, depth)
tell application "System Events"
if depth > 8 then return missing value
try
if (role of el) is "AXSlider" and (description of el) is "템포" then return el
end try
try
repeat with c in (every UI element of el)
set r to my findS(c, depth + 1)
if r is not missing value then return r
end repeat
end try
return missing value
end tell
end findS
tell application "System Events"
tell process "{APP}"
repeat with w in windows
if (name of w) ends with "- 트랙" then
repeat with g in (every UI element of w)
try
if (description of g) is "컨트롤 막대" then
set s to my findS(g, 0)
if s is not missing value then return value of s
end if
end try
end repeat
end if
end repeat
return ""
end tell
end tell''', timeout=60)
    try:
        return float(out)
    except ValueError:
        return None


# ---- the three measured steps
def import_token():
    """열기 패널 검색용 고유 숫자 토큰(OCR 이 숫자를 가장 안정적으로 읽는다)."""
    return time.strftime('%H%M%S') + f'{int(time.time() * 1000) % 1000:03d}'


def import_row_pattern(token):
    """결과 행 텍스트 매칭: 행 이름은 약 24자를 넘으면 가운데가 '…' 로 줄고 끝 6자+`.mid` 만 남는다(2026-11-14 실측
    `tplsmoke-20...306393.mid`). 파일 아이콘이 'n ' 같은 글자로 읽히기도 한다. 그래서 토큰의 끝 6자리 + mid 로 맞춘다."""
    return re.compile(rf'{re.escape(token[-6:])}\.?mid$')


def import_midi_menu(mid_path, log=print):
    """파일 > 가져오기 > MIDI 파일… → 패널 검색창(AX)에 고유 이름 → 결과 행 CGEvent 클릭 → '가져오기' → '템포 가져오기'.
    열기 패널은 원격 서비스(openAndSavePanelService)라 AX 로 파일 목록이 보이지 않는다 — 행은 OCR·CGEvent 로 고른다.
    패널 검색은 Mac 전체라 형제 워크트리의 동명 .mid 가 섞일 수 있으므로, SMF 를 `<앞4자>~<숫자 토큰>.mid` 로 복사해 그 토큰으로 찾고
    (정확히 한 행이어야 한다) 끝나면 지운다. 리전 이름은 SMF 트랙 이름에서 오므로 파일 이름은 결과에 남지 않는다."""
    token = import_token()
    stem = os.path.basename(mid_path)[:-4]
    tmp = os.path.join(os.path.dirname(mid_path), f'{stem[:4]}~{token}.mid')   # 18자: 패널이 이름을 줄이지 않는 길이(≈24자 이하)
    shutil.copyfile(mid_path, tmp)
    time.sleep(3)   # 열기 패널 검색은 Spotlight 색인을 쓴다 — 방금 만든 파일이 잡히도록 잠깐 기다린다(2026-11-14 실측: 바로 열면 0행)
    try:
        _import_midi_menu(tmp, token, log=log)
    finally:
        try:
            os.remove(tmp)
        except FileNotFoundError:
            pass


def _import_midi_menu(mid_path, token, log=print):
    fname = os.path.basename(mid_path)
    stem = fname[:-4]
    menu_click('파일', '가져오기', 'MIDI 파일…')
    if not wait_window('가져오기', timeout=30):
        raise TemplateError('import panel did not open')
    time.sleep(1.5)
    field = ocr_find(r'검색$', timeout=15, pred=lambda it: it[3] > 600 and it[2] < 450)[0]   # 패널 상단 오른쪽 검색 필드(OCR: 행 위치 기준용)
    # 검색어는 keystroke 가 아니라 AX 로 넣는다 — 포커스가 패널에 없으면 글자가 Logic 키 명령(k=메트로놈 등)으로 간다(2026-11-14 실측).
    # 검색 필드는 패널 창의 2단계 자식이라 얕은 탐색으로 빨리 찾는다(전체 AX 탐색은 수십 초).
    rc, out, err = osa(f'''tell application "System Events"
tell process "{APP}"
set w to window "가져오기"
set tf to missing value
repeat with g in (every UI element of w)
try
if (role of g) is "AXTextField" then set tf to g
end try
if tf is missing value then
try
repeat with c in (every UI element of g)
if (role of c) is "AXTextField" then
set tf to c
exit repeat
end if
end repeat
end try
end if
if tf is not missing value then exit repeat
end repeat
if tf is missing value then return "ERR no search field"
set focused of tf to true
set value of tf to "{stem}"
delay 0.3
if (value of tf as text) is not "{stem}" then return "ERR field value " & (value of tf as text)
key code 36
return "ok"
end tell
end tell''', timeout=60)
    if out != 'ok':
        raise TemplateError(f'import panel search field: {out or err[:120]}')
    time.sleep(4)
    pat = import_row_pattern(token)
    rows = []
    for attempt in range(4):   # 색인이 늦으면 검색을 다시 실행한다(필드에 포커스를 주고 Return)
        try:
            rows = ocr_find(pat.pattern, timeout=10, pred=lambda it: it[2] > field[2])
            break
        except TemplateError:
            seen = [it[0] for it in ocr_screen() if 'mid' in it[0].lower() and it[2] > field[2]]
            log(f'    import: result row not found yet (attempt {attempt + 1}); rows with mid: {seen}')
            osa(f'''tell application "System Events"
tell process "{APP}"
set frontmost to true
key code 36
end tell
end tell''', timeout=30)
            time.sleep(4)
    if len(rows) != 1:
        raise TemplateError(f'import panel: expected exactly one result row for {fname}, got {[r[0] for r in rows]}')
    row = rows[0]
    cg('click', row[1], row[2]); time.sleep(1.0)
    btn = ocr_find(r'^가져오기$', pred=lambda it: it[2] > row[2])[-1]   # 패널 하단 버튼(행보다 아래)
    cg('click', btn[1], btn[2])
    if not click_dialog_button('', '템포 가져오기', timeout=60):
        raise TemplateError('tempo dialog did not appear')
    log('    import: 템포 가져오기')
    time.sleep(4)


def library_pane_state():
    """컨트롤 막대 '라이브러리' 체크상자 값(1/0) 또는 None."""
    rc, out, err = osa(f'''tell application "System Events"
tell process "{APP}"
repeat with w in windows
if (name of w) ends with "- 트랙" then
repeat with g in (every UI element of w)
try
if (description of g) is "컨트롤 막대" then
repeat with c in (every checkbox of g)
try
if (name of c) is "라이브러리" then return (value of c) as integer
end try
end repeat
end if
end try
end repeat
end if
end repeat
return ""
end tell
end tell''')
    return int(out) if out in ('0', '1') else None


def set_library_pane(on):
    """라이브러리 패널 보기 토글(키 명령 Y; 보기 상태이지 환경설정이 아니다). 템플릿을 라이브러리 열린 채 저장했으면
    트랙 영역이 좁아 리전 OCR 이 실패한다."""
    want = 1 if on else 0
    for _ in range(2):
        if library_pane_state() == want:
            return True
        osa(f'''tell application "System Events"
tell process "{APP}"
set frontmost to true
delay 0.3
keystroke "y"
end tell
end tell''')
        time.sleep(1.5)
    return library_pane_state() == want


def dismiss_crash_reporter():
    """이전 Logic 크래시의 macOS 리포터 대화상자('예기치 않게 종료')는 다른 프로세스라 창 목록에 안 보인다 — OCR 로 '무시' 를 누른다."""
    items = ocr_screen()
    if any('예기치 않게' in it[0] for it in items):
        for it in items:
            if it[0] == '무시':
                cg('click', it[1], it[2]); time.sleep(1.5)
                return True
    return False


def dismiss_panels():
    """실패 정리용: 원격 열기 패널은 System Events 를 받지 않으므로 OCR 로 '취소' 를 찾아 CGEvent 로 누른다. 그 외 시트는 Escape."""
    for _ in range(3):
        names = windows_strict()
        others = [w for w in names if not (w.endswith('- 트랙') or w.endswith('- 믹서: 트랙'))]
        if not others:
            return
        try:
            btn = ocr_find(r'^취소$', timeout=3)[-1]
            cg('click', btn[1], btn[2])
        except TemplateError:
            osa(f'tell application "System Events" to tell process "{APP}" to key code 53')
        time.sleep(2)


def reassign_track(header_xy, inst_index):
    """트랙 헤더 우클릭 → (키보드) 트랙 다시 할당 > 믹서 > 소프트웨어 악기 → (OCR) '… (Inst k)' 클릭.
    컨텍스트 메뉴는 AX 밖이다. 고정 경로는 방향키로 가고(OCR 이 첫 항목을 놓치는 경우가 있다) 마지막 목록만 OCR 로 고른다."""
    for attempt in range(3):
        cg('move', *header_xy); time.sleep(0.8)      # 2026-11-14: 재할당 직후 곧바로 우클릭하면 Logic 이 _routeRightMouseDownEvent 에서 SIGSEGV
        cg('rclick', *header_xy); time.sleep(1.5)
        try:
            ocr_find(r'새로운 오디오 트랙|트랙 삭제|트랙 다시 할당', timeout=5)
            break
        except TemplateError:
            osa(f'tell application "System Events" to tell process "{APP}" to key code 53')
            time.sleep(1.5)
    else:
        raise TemplateError(f'context menu did not open at {header_xy}')
    # ↓ 트랙 다시 할당, → 믹서, → 기타(첫 항목), ↓ 소프트웨어 악기, → 악기 목록
    osa(f'''tell application "System Events"
tell process "{APP}"
key code 125
delay 0.4
key code 124
delay 0.6
key code 124
delay 0.6
key code 125
delay 0.4
key code 124
end tell
end tell''')
    time.sleep(1.2)
    hit = ocr_find(rf'\(Inst {inst_index}\)', timeout=8)[0]
    cg('click', hit[1], hit[2]); time.sleep(1.0)
    return hit[0]


def region_rows(track_names):
    """리전 라벨(SMF 트랙 이름) OCR → 트랙별 헤더 클릭점 [(x, y)] 포인트. 라벨은 잘릴 수 있어 앞 REGION_KEY_LEN 자로 맞춘다(preflight 가 유일성을 보장).
    헤더 x 는 같은 줄에서 라벨 왼쪽에 있는 텍스트(트랙 이름) 중 가장 왼쪽 것으로 잡는다(라이브러리 열림 여부에 따라 트랙 영역이 움직인다)."""
    items = ocr_screen()
    rows = []
    for name in track_names:
        key = unicodedata.normalize('NFC', name)[:REGION_KEY_LEN]
        hits = [it for it in items if it[0].startswith(key) and it[3] > 300]
        if not hits:
            raise TemplateError(f'region label not found: {name}')
        lab = hits[0]
        same = [it for it in items if abs(it[2] - lab[2]) < 20 and 240 < it[3] and it[3] + it[5] < lab[3] - 20
                and len(it[0]) > 2 and re.search(r'[A-Za-z가-힣]', it[0])]   # x>240: 인스펙터 텍스트 제외
        if not same:
            raise TemplateError(f'track header not found left of region: {name}')
        hdr = max(same, key=lambda it: it[5])   # 가장 넓은 텍스트 = 트랙 이름
        rows.append((hdr[1], lab[2]))
    return rows


def move_regions_to_template(track_names, n_template, log=print):
    """새 트랙 i(리전 보유) 를 템플릿 스트립 Inst i 로 재할당하고, 리전 없는 원래 트랙을 지운다."""
    for i, xy in enumerate(region_rows(track_names)):
        label = reassign_track(xy, i + 1)
        log(f'    reassign track {n_template + i + 1} -> {label}')
        time.sleep(3)   # 헤더·스트립 갱신이 끝난 뒤 다음 우클릭 (크래시 회피)
    menu_click('트랙', '사용하지 않는 트랙 삭제')
    time.sleep(2)


def focus_track(k, proj):
    """트랙 k 포커스 — PR #4 의 select_track()(트랙 검색 팝오버에서 "<번호>\\t이름" 행 선택·인스펙터 확인) 를 쓴다."""
    ok, picked = select_track(k, proj=proj)
    if not ok:
        raise TemplateError(f'focus_track({k}): {picked}')


def track_region_names(n, proj):
    """트랙 1..n 을 차례로 포커스해 인스펙터 머리글 '리전: <이름>' 을 OCR 로 읽는다(AX 트리에는 중첩돼 있어 직접 읽기 어렵다)."""
    names = []
    for k in range(1, n + 1):
        focus_track(k, proj)
        time.sleep(0.8)
        hits = [it for it in ocr_screen() if it[3] < 300 and re.search(r'리전:\s*\S', it[0])]
        names.append(re.sub(r'^.*?리전:\s*', '', hits[0][0]).strip() if hits else '')
    return names


def produce_template(sid, title, ver, mid_path, template, log=print, owner=None):
    """템플릿 모드: 시작 조건 → preflight → 해시 → 사본 복사 → 사본 열기 → 스냅샷 → 메뉴 임포트(새 트랙) → 재할당·정리
    → 스트립·리전·템포 → ⌘S → 바운스. 실패하면 저장 없이 닫고 사본을 <proj>.failed-<ts>.logicx 로 남긴다.
    원본은 어떤 단계에서도 열지 않는다. 사본을 열면 창 제목이 '<proj>.logicx - 트랙' 이다(2026-11-13 실측)."""
    owner = owner or _worktree_name()
    proj = f'{title} {ver}'
    with LogicLock(owner):
        dismiss_crash_reporter()
        names = windows_strict()
        if any(w.endswith('- 트랙') or w.endswith('- 믹서: 트랙') for w in names):
            raise TemplateError(f'a project is open: {names}')
        if any(w not in START_ALLOWED_WINDOWS for w in names):
            raise TemplateError(f'unexpected window at start: {names}')
        pf = preflight_template(template, proj, mid_path)
        h0 = tree_hash(template)
        copy = pf['copy']
        with open(mid_path, 'rb') as f:
            track_names = smf_track_names(f.read())
        win_proj = f'{proj}.logicx'
        try:
            shutil.copytree(template, copy)   # try 안: 복사 중 끊기면(Netac) 부분 사본도 .failed 로 남긴다
            subprocess.run(['open', '-a', APP, copy], capture_output=True)
            click_dialog_button('', '저장된 버전', timeout=8)   # 자동 저장 복구 대화상자가 뜨면 저장된 버전(=템플릿 그대로)
            if not wait_window(f'{win_proj} - 트랙', timeout=120):
                raise TemplateError(f'project window did not appear: {win_proj}')
            time.sleep(3)
            assert_only_project(win_proj)
            open_mixer()
            snapshot = strip_names(mixer_strips())
            close_mixer()
            if len(snapshot) < pf['tracks']:
                raise TemplateError(f'mixer read {snapshot} shorter than NumberOfTracks {pf["tracks"]} (mixer window missing?)')
            import_midi_menu(mid_path, log=log)
            assert_only_project(win_proj)
            if not set_library_pane(False):
                raise TemplateError('could not close the library pane (Y)')
            move_regions_to_template(track_names, pf['tracks'], log=log)
            regions = track_region_names(pf['smf_tracks'], win_proj)
            if regions != track_names:
                raise TemplateError(f'regions per track {regions} != SMF tracks {track_names}')
            menu_click('트랙', '사용하지 않는 트랙 삭제')   # 리전 없는 트랙이 어떤 경로로든 생겼으면 여기서 정리
            time.sleep(2)
            open_mixer()
            strips = strip_names(mixer_strips())
            close_mixer()
            if strips != snapshot:
                raise TemplateError(f'strips changed after import: {snapshot} -> {strips}')
            tempo = lcd_tempo_value()
            if tempo is None or abs(tempo - pf['smf_bpm']) > 0.01:
                raise TemplateError(f'tempo {tempo} != SMF {pf["smf_bpm"]}')
            save_quiet()
            r = bounce_and_post(sid, win_proj, ver, end_bar=pf['smf_end_bar'])
            if not r.get('ok'):
                raise TemplateError(f'bounce failed: {r}')
        except BaseException:
            try:   # 정리 중 2차 오류(창 조회 실패·osascript 타임아웃)가 원인 예외와 .failed 보존을 가리지 않게 한다
                try:
                    dismiss_panels()
                except Exception as e:
                    log(f'    cleanup: dismiss_panels failed: {e}')
                try:
                    close_all_projects(save=False)
                except Exception as e:
                    log(f'    cleanup: close_all_projects failed: {e}')
            finally:
                if os.path.isdir(copy):
                    os.rename(copy, os.path.join(PROJ_DIR, failed_name(proj, time.strftime('%Y%m%d-%H%M%S'))))
            raise
        r.update(snapshot=snapshot, strips=strips, regions=regions, tempo=tempo,
                 template_hash_before=h0, template_hash_after=tree_hash(template), preflight=pf, copy=copy)
        return r


def assert_only_project(win_proj):
    """실행 중 예상 밖 창(샘플 누락·복구·플러그인 창 등)이 있으면 실패 — strict 조회."""
    names = windows_strict()
    others = [w for w in names if w not in (f'{win_proj} - 트랙', f'{win_proj} - 믹서: 트랙')]
    if others:
        raise TemplateError(f'unexpected window while working on {win_proj}: {others}')


def close_mixer():
    rc, out, err = osa(f'''tell application "System Events"
tell process "{APP}"
set names to name of every window
repeat with nm in names
if (nm as text) ends with "- 믹서: 트랙" then
set w to window (nm as text)
repeat with b in (every button of w)
try
if (description of b) is "닫기 버튼" then click b
end try
end repeat
end if
end repeat
end tell
end tell''')
    time.sleep(1.5)


def smf_track_names(buf):
    """SMF 의 음악 트랙(conductor 제외) 이름 — 트랙 청크 첫 0x03 meta."""
    _, ntrk, _, _ = parse_smf(buf)
    pos, names = 14, []
    for _ in range(ntrk):
        ln = struct.unpack('>I', buf[pos + 4:pos + 8])[0]
        d = buf[pos + 8:pos + 8 + ln]
        m = re.search(rb'\xff\x03(.)', d, re.S)
        names.append(d[m.end():m.end() + m.group(1)[0]].decode('utf-8', 'replace') if m else '')
        pos += 8 + ln
    return names[1:]
