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


def build_smf(title, bpm, keysig_sf, minor, n_bars, tracks, pcs, nt, cc, markers=(), timesig=(4, 4), tempos=()):
    """tracks: [(name, midi_ch)], pcs: {idx: program}, nt: {idx: [(tick,dur,pitch,vel)]},
    cc: {idx: [(tick, cc, val)]}, markers: [(bar, text)], timesig: (num, den) with den a power of two,
    tempos: [(tick, bpm)] 추가 템포 이벤트(루바토·아첼레란도). 기본값(4/4, 템포 변화 없음)은 이전 출력과 바이트 동일.
    4/4 가 아니면 bt()/BAR 는 쓰지 말고 bar_ticks = num * PPQ * 4 // den 로 틱을 직접 계산한다(band-fable 7d6d9a0 에서 가져옴)."""
    num, den = timesig
    assert den > 0 and den & (den - 1) == 0, f'timesig denominator must be a power of two: {timesig}'
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


def select_track(index, proj='무제'):
    """트랙 메뉴 '트랙 검색 및 선택…' 팝오버에 트랙 번호를 치고, 윤곽 목록에서 "<번호>\\t이름" 행을 골라 Return.
    이름이 같은 트랙이 여럿이어도 번호로 고르므로 유일하다. 팝오버가 안 뜨거나 행이 없거나 도중에 오류가 나면
    Escape 로 닫고 실패를 돌려준다. 반환: (성공 여부, 고른 행 텍스트 "<번호>\\t이름" 또는 오류)."""
    index = int(index)
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
    정확히 같은 행이 없고 결과가 **한 행뿐**이면 그 행을 고른다 — 최신 팩 패치는 한국어 UI 에서 표시명이 번역돼
    있어(실측: `Tonewheel Organ` → 표시 "톤휠 오르간") 파일 이름으로 검색은 되지만 글자가 다르기 때문이다.
    반환: (성공 여부, 결과 행 이름 목록, 실제로 고른 행 이름 또는 '')."""
    patch_lit = _as_str(patch)
    rc, out, err = osa(_FIND_BY_DESC + f'''tell application "System Events"
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
if hit is missing value and nRows is 1 then set hit to lone
if hit is not missing value then exit repeat
end if
delay 0.5
end repeat
if hit is not missing value then exit repeat
delay 1.0
end repeat
if hit is missing value then return "MISS " & names & "|(field=" & lastValue & ")"
set gotName to value of UI element 1 of UI element 1 of hit
set selected of hit to true
delay 2.5
return "OK " & gotName & "|" & names
end tell
end tell''', timeout=90)
    if rc != 0:
        return False, [err[:120]], ''
    status, _, rest = out.partition(' ')
    got, _, names = rest.partition('|')
    return status == 'OK', [_nfc(n) for n in names.split('|') if n], _nfc(got) if status == 'OK' else ''


def load_patches(patches, proj='무제', log=print):
    """patches: {track_index(1-based, SMF 트랙 순서): spec}. spec 은
      'Harpsichord'                 라이브러리 패치(.patch) 이름 — 파일 이름(확장자 제외). 라이브러리 표시명이 번역돼
                                     있어도 검색 결과가 한 행뿐이면 그 행을 올린다(library_pick).
      ('Violins 1', 'Violin (Arco)') (Sampler 를 쓰는 패치, Sampler 프리셋/EXS 악기 이름) — 패치를 먼저 올려 Sampler 를
                                     확보하고, 인스펙터의 Sampler 라이브러리 표시기로 층을 바꿔 EXS 악기를 올린다.
    번호로 트랙을 고르므로 이름이 겹쳐도 안전하다. 확인: 패치는 (선택된 트랙의) 인스펙터 패치 층 '라이브러리 표시기'
    이름이 고른 행 이름과 같고 i 번째 트랙 헤더가 임포트 때 이름에서 바뀌었거나(채널 스트립 이름은 패치 파일 이름과
    다를 수 있다 — 실측 `Studio Alto Sax 1` → "(New) Horns") 고른 이름과 같아야 한다. EXS 는 헤더가 고른 EXS 이름으로
    바뀌어야 한다(임포트로 자동 명명된 트랙 기준 — 사람이 이름을 바꾼 트랙은 이름이 안 바뀐다, 2026-11-09 실측).
    선행 조건: 임포트된 '<proj> - 트랙' 창. 반환: {index: (spec, ok, (올라간 패치 표시명, EXS 표시명 또는 None, 헤더 이름))};
    하나라도 실패면 RuntimeError."""
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
        ok_focus, _, _ = focus_library_slot(None, proj)      # 앞 트랙에서 Sampler 층을 봤더라도 패치 층으로 되돌린다
        ok_pick, rows, got = library_pick(base, proj) if ok_focus else (False, [], '')
        ok_ind, _, loaded = focus_library_slot(None, proj)   # 올라간 패치명 읽기 (표시기 이름)
        name = _nth(track_names(proj), i)
        # 표시기는 '선택된' 트랙의 것이고 헤더는 i 번째 트랙의 것 — 둘 다 맞아야 엉뚱한 트랙에 올라간 경우를 거른다
        ok = ok_pick and ok_ind and loaded == got and (name != names[i - 1] or name == got)
        got_exs = None
        if ok and exs:
            ok_focus, desc, _ = focus_library_slot('Sampler', proj)
            ok_pick, rows, got_exs = library_pick(exs, proj) if ok_focus else (False, [desc], '')
            name = _nth(track_names(proj), i)
            ok = ok_pick and name == got_exs
        results[i] = (spec, ok, (loaded, got_exs, name))
        log(f'track {i}: {names[i - 1]} -> {spec}: {"OK" if ok else "FAIL"} (patch={loaded}, exs={got_exs}, header={name}, results={rows[:5]})')
    failed = {i: r for i, r in results.items() if not r[1]}
    if failed:
        raise RuntimeError(f'patch load failed: {failed}')
    return results


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
BOUNCE_SEARCH = [BOUNCE_DIR, SK_DIR, PROJ_DIR, os.path.expanduser('~/Music'), os.path.expanduser('~/Desktop'),
                 os.path.expanduser('~/Documents'), os.path.expanduser('~/Downloads')]
# 다른 워크트리(세션)의 sketches/ 도 본다 — Logic 바운스 대화상자는 마지막으로 쓴 폴더를 기억하므로
# 다른 세션이 자기 sketches/ 로 바운스했으면 다음 바운스가 거기로 떨어진다 (2026-10-30 실측: band-fable/docs/music/sketches).
_WT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..'))
BOUNCE_SEARCH += sorted(d for d in _glob.glob(os.path.join(_WT_ROOT, '*', 'docs', 'music', 'sketches')) if d not in BOUNCE_SEARCH)
BOUNCE_SEARCH += [d for d in ('/Volumes/Netac 2TB/workspace/losik/docs/music/sketches',) if os.path.isdir(d) and d not in BOUNCE_SEARCH]


def wait_bounce_file(name, timeout=600, since=None):
    """후보 폴더 중 하나에 name 이 안정적으로 생기면 BOUNCE_DIR 로 옮긴 경로를, 아니면 None.
    since 가 주어지면 그 시각 이전의 파일(옛 잔재)은 무시한다."""
    import shutil
    t0 = time.time()
    while time.time() - t0 < timeout:
        for d in BOUNCE_SEARCH:
            p = os.path.join(d, name)
            try:
                if os.path.exists(p) and os.path.getsize(p) > 500000 and (since is None or os.path.getmtime(p) >= since):
                    s = os.path.getsize(p)
                    time.sleep(3)
                    if os.path.getsize(p) == s:
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


def produce(sid, title, ver, mid_path, log=print, owner=None, patches=None):
    """열린 프로젝트 정리 → SMF 임포트(벽시계 기준 대기; 임포트 중 System Events 는 ~2분씩 블록) → finish().
    patches: load_patches() 의 {트랙 번호: 패치 spec} — 임포트 뒤, 바운스 전에 라이브러리 패치/EXS 를 올린다.
    세션 간 Logic 경합을 막기 위해 LogicLock 을 잡고 돈다(owner 기본값 = 현재 워크트리 이름)."""
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
        r = finish(sid, title, ver, log=log, patches=patches)
        r['elapsed'] = round(time.time() - t0)
        return r


def finish(sid, title, ver, log=print, patches=None):
    """(패치 로드 →) 메트로놈 OFF → 스트립 실측 → 저장(projects/) → bounce_and_post()."""
    proj = f'{title} {ver}'
    loaded = None
    if patches:
        try:
            loaded = load_patches(patches, log=log)
        except Exception as e:          # 이름 오류(ValueError)·AX 시간 초과(TimeoutExpired)도 배치를 끊지 않고 곡 단위 실패로 돌려준다
            try:
                tracks = track_names()
            except Exception:
                tracks = []
            return dict(ok=False, stage='patches', msg=f'{type(e).__name__}: {e}', tracks=tracks)
    log(f'{sid}: metronome {metronome_off("무제 - 트랙")}')
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


def bounce_and_post(sid, proj, ver):
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
    ok2, m2 = start_bounce_aiff(proj, f'{sid}-{ver}')
    if not ok2:
        return dict(ok=False, stage='bounce', msg=m2)
    aif = wait_bounce_file(f'{sid}-{ver}.aif', since=t_start)
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
