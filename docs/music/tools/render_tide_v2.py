"""Serial, explicit-instrument Logic rendering for the five redesigned v2 scores."""
from pathlib import Path
import json
import re
import subprocess
import sys
import time
import pipeline as p
import render_tide_variants as old
import tide_v2 as score
import v2_audio

PROJECTS=Path(p.PROJ_DIR)
BOUNCES=Path(p.BOUNCE_DIR)
EXS={
 'Fingerstyle Electric Bass':Path('/Library/Application Support/Logic/Sampler Instruments/02 Bass/02 Electric Bass/Fingerstyle Electric Bass.exs'),
 'Upright Jazz Bass':Path('/Library/Application Support/Logic/Sampler Instruments/02 Bass/01 Acoustic Bass/Upright Jazz Bass.exs'),
 'Full Brass Staccato':Path('/Library/Application Support/Logic/Sampler Instruments/09 Orchestral/02 Brass/Full Brass Staccato.exs'),
 'Astra Air Harmonica':Path('/Users/hugom4/Music/Audio Music Apps/Sampler Instruments/Astra Air Harmonica.exs')}

COLLECT='''on strips(el,d)
tell application "System Events"
if d>9 then return {}
try
if role of el is "AXLayoutItem" then return {el}
end try
set acc to {}
try
repeat with c in every UI element of el
set acc to acc & my strips(c,d+1)
end repeat
end try
return acc
end tell
end strips
'''


def load_exs(index,path):
    assert path.is_file(),path
    before=p.windows()
    rc,out,err=p.osa(COLLECT+f'''tell application "System Events" to tell process "{p.APP}"
set frontmost to true
set mw to missing value
repeat with w in windows
if (name of w) contains "믹서" then
set mw to w
exit repeat
end if
end repeat
set allStrips to my strips(mw,0)
set strip to item {index+1} of allStrips
set slot to missing value
repeat with e in every UI element of strip
try
if role of e is "AXGroup" and (description of e is "Sampler" or description of e is "input") then set slot to e
end try
end repeat
if slot is missing value then error "Expected Sampler instrument slot"
click (first button of slot whose description is "열기" or description is "open")
end tell''',timeout=60)
    assert rc==0,(out,err)
    time.sleep(1)
    candidates=[w for w in p.windows() if w not in before and '트랙' not in w]
    assert candidates,('Sampler editor did not open',p.windows())
    window=candidates[0]
    rc,out,err=p.osa(f'''tell application "System Events" to tell process "{p.APP}"
set frontmost to true
set w to window "{window}"
click last pop up button of w
delay 0.4
set opened to false
repeat with e in every UI element of w
if role of e is "AXMenu" then
repeat with mi in every UI element of e
if name of mi is "불러오기…" then
click mi
set opened to true
exit repeat
end if
end repeat
end if
end repeat
if not opened then error "Sampler load menu not found"
delay 1
key code 5 using {{command down,shift down}}
delay 1
set f to text field 1 of sheet 1 of window "열기"
set value of f to "{path}"
set focused of f to true
key code 36
delay 1
click button "열기" of splitter group 1 of window "열기"
delay 2
return name of every window
end tell''',timeout=90)
    assert rc==0,(out,err)
    candidates=[w for w in p.windows() if '트랙' not in w and w!='열기']
    assert any(path.stem in w for w in candidates),('Wrong instrument loaded',path,candidates)
    loaded=next(w for w in candidates if path.stem in w)
    rc,out,err=p.osa(f'''tell application "System Events" to tell process "{p.APP}"
set valueName to value of last pop up button of window "{loaded}"
click button 1 of window "{loaded}"
return valueName
end tell''',timeout=30)
    assert rc==0,(out,err)
    print('EXS VERIFIED',index,path.stem,out,flush=True)
    return dict(track=index,path=str(path),preset=out)


def close_project(title):
    windows=[w for w in p.windows() if w.endswith('- 트랙')]
    assert len(windows)==1 and windows[0] in (title+' - 트랙',title+'.logicx - 트랙'),windows
    rc,out,err=p.osa(f'''tell application "System Events" to tell process "{p.APP}"
set frontmost to true
perform action "AXRaise" of window "{windows[0]}"
click menu bar item "파일" of menu bar 1
delay 0.3
click menu item "저장" of menu 1 of menu bar item "파일" of menu bar 1
delay 1
keystroke "w" using command down
delay 1
end tell''',timeout=60)
    assert rc==0,(out,err)
    assert p.wait_window('- 트랙',present=False,timeout=30),p.windows()


def wait_render_finished(title,timeout=360):
    deadline=time.time()+timeout
    while time.time()<deadline:
        windows=p.windows()
        active=any(w in (title+' - 트랙',title+'.logicx - 트랙') for w in windows)
        progress=any(w.replace('\xa0',' ')=='Logic Pro' or '바운스' in w for w in windows)
        if active and not progress:
            return
        time.sleep(2)
    raise RuntimeError(('Logic bounce did not finish',p.windows()))


def consolidate_custom_samples():
    rc,out,err=p.osa(f'''tell application "System Events" to tell process "{p.APP}"
set frontmost to true
click menu bar item "파일" of menu bar 1
click menu item "프로젝트 관리" of menu 1 of menu bar item "파일" of menu bar 1
click menu item "통합…" of menu 1 of menu item "프로젝트 관리" of menu 1 of menu bar item "파일" of menu bar 1
delay 0.5
set w to window "프로젝트 통합: 옵션"
repeat with cb in checkboxes of w
set desired to ((name of cb is "오디오 파일 복사") or (name of cb is "Sampler 오디오 데이터 복사"))
if (value of cb as boolean) is not desired then click cb
end repeat
click button "확인" of w
end tell''',timeout=60)
    assert rc==0,(out,err)
    assert p.wait_window('프로젝트 통합',present=False,timeout=60)


def render(slug):
    manifest=json.loads((score.SKETCHES/(slug+'-manifest.json')).read_text())
    title=manifest['title']
    project=PROJECTS/(title+'.logicx')
    aiff=BOUNCES/(slug+'.aif')
    wav=BOUNCES/(slug+'.wav')
    assert not project.exists() and not aiff.exists() and not wav.exists(),slug
    assert not p.project_windows(),('Another project is open',p.windows())
    print('IMPORT',slug,flush=True)
    assert p.open_mid(str(score.SKETCHES/(slug+'.mid')),timeout=240),p.windows()
    metro=p.metronome_off('무제 - 트랙')
    print('METRONOME',metro,flush=True)
    control=old.control_bar()
    assert f'AXSlider|템포|{float(manifest["bpm"])}' in control,control
    num,den=manifest['sections'][0]['meter']
    assert f'AXPopUpButton|박자표|{num}/{den}' in control,control
    p.open_mixer()
    overrides=[]
    for index,track in enumerate(manifest['tracks']):
        if track['patch'] in EXS:
            overrides.append(load_exs(index,EXS[track['patch']]))
    strips=p.mixer_strips()
    print('PATCHES',strips,flush=True)
    observed=re.findall(r'\[([^\]]+)\]',strips)
    expected=[track['patch'] for track in manifest['tracks']]
    assert observed[:len(expected)]==expected,(observed,expected)
    assert 'GM 기기' not in strips,strips
    ok,msg=p.save_project_as(title)
    assert ok,msg
    assert (project/'Alternatives/000/ProjectData').is_file()
    print('PROJECT SAVED',project,flush=True)
    if any(track['patch']=='Astra Air Harmonica' for track in manifest['tracks']):
        consolidate_custom_samples()
        assert len(list((project/'Media/Samples/Astra Air Harmonica').glob('*.wav')))==11
        print('CUSTOM SAMPLES CONSOLIDATED',flush=True)
    ok,msg=p.start_bounce_aiff(title,slug)
    assert ok,msg
    print('OFFLINE BOUNCE STARTED',flush=True)
    wait_render_finished(title)
    expected_bytes=manifest['duration_seconds']*48000*6
    assert p.wait_file_stable(str(aiff),min_size=int(expected_bytes*.95),timeout=360)
    print('LOGIC RENDER FINISHED',flush=True)
    close_project(title)
    mastering=v2_audio.master(aiff,wav)
    metrics=v2_audio.measure(wav,manifest)
    metrics.update(title=title,project=str(project),bpm=manifest['bpm'],bars=manifest['bars'],
                   mode='offline',metronome=metro,control_bar=control,patches=strips,
                   instrument_overrides=overrides,mastering=mastering)
    (score.SKETCHES/(slug+'-verification.json')).write_text(json.dumps(metrics,indent=2)+'\n')
    subprocess.run(['afplay','-t','6',str(wav)],check=True,timeout=30)
    print('COMPLETE',slug,json.dumps({k:metrics[k] for k in ('seconds','sha256','peak_dbfs','unexpected_zero_runs')}),flush=True)
    return metrics


if __name__=='__main__':
    for slug in sys.argv[1:] or score.IDS:
        render(slug)
