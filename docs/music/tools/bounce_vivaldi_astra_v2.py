"""Serial, locked Vivaldi Astra v2 production, restricted to shared music storage.
Run with optional sids; already successful jobs require matching input hashes.
The pipeline's LogicLock is unchanged. No sibling worktree is a write target.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import time

import pipeline as p
from bounce_dh import NoScreensaver, screen_locked
from vivaldi_astra_v2 import SKETCHES, ROOT, patches

STAGING = Path(p.BOUNCE_DIR).parent/'inputs'/'vivaldi-astra-v2'
LOG = ROOT/'vivaldi_astra_v2_bounce.jsonl'
DOMAIN = 'com.apple.mobilelogic'


def inventory_check(s):
    inventory=json.loads((ROOT/'logic_library_inventory.json').read_text())
    names={Path(x).stem for x in inventory['patches']['Instrument']}
    exs={Path(x).stem for paths in inventory['sampler_presets'].values() for x in paths}
    for spec in patches(s).values():
        base,sampler=spec if isinstance(spec,tuple) else (spec,None)
        assert base in names,('patch missing from inventory',base)
        if sampler:
            assert sampler in exs,('EXS missing from inventory',sampler)
            assert any(x.endswith('/'+base+'.patch') and x.startswith('z_Legacy/Orchestral/') for x in inventory['patches']['Instrument'])


def configure_destination(message):
    # restart_logic calls this callback while STILL holding its own LogicLock.
    running=subprocess.run(['pgrep','-f',p.APP+'$'],capture_output=True).returncode
    if running==0:
        raise RuntimeError('Logic has not quit; do not change a live process save destination')
    if running!=1:
        raise RuntimeError(f'Cannot verify Logic exit: pgrep={running}')
    subprocess.run(['defaults','write',DOMAIN,'defaultBouncePath','-string',p.BOUNCE_DIR],check=True)
    print(message+'; defaultBouncePath='+p.BOUNCE_DIR,flush=True)


def record(row):
    row['timestamp']=time.strftime('%Y-%m-%dT%H:%M:%S%z')
    with LOG.open('a') as out:
        out.write(json.dumps(row,ensure_ascii=False)+'\n')
    print(json.dumps(row,ensure_ascii=False),flush=True)


def run(sids=()):
    selected=[s for s in SKETCHES if not sids or s['sid'] in sids]
    assert not set(sids)-{s['sid'] for s in SKETCHES},'unknown sid'
    if not Path(p.BOUNCE_DIR).is_dir() or not Path(p.PROJ_DIR).is_dir():
        raise FileNotFoundError('Shared music volume is unavailable')
    STAGING.mkdir(parents=True,exist_ok=True)
    previous={}
    if LOG.exists():
        for line in LOG.read_text().splitlines():
            row=json.loads(line)
            previous[row['sid']]=row
    configured=False; completed=0; last_restart=-1; failed=[]
    with NoScreensaver():
        for s in selected:
            sid=s['sid']; evidence={}; digest=None
            def log(message):
                print(message,flush=True)
                evidence.setdefault('events',[]).append(message)
                if ': metronome ' in message:
                    actual=subprocess.run(['defaults','read',DOMAIN,'defaultBouncePath'],capture_output=True,text=True,check=True).stdout.strip()
                    if os.path.realpath(actual)!=os.path.realpath(p.BOUNCE_DIR):
                        raise RuntimeError(f'Unsafe remembered bounce folder: {actual}')
                    evidence['bounce_directory']=actual
            try:
                source=ROOT/'sketches'/(sid+'-v2.mid')
                data=source.read_bytes(); digest=hashlib.sha256(data).hexdigest()
                project=Path(p.PROJ_DIR)/(s['title']+' v2.logicx')
                wav=Path(p.BOUNCE_DIR)/(sid+'-v2.wav')
                if previous.get(sid,{}).get('ok'):
                    old=previous[sid]
                    assert old['midi_sha256']==digest and project.is_dir() and wav.is_file(),('stale successful output',sid)
                    assert old['requested_patches']==json.loads(json.dumps(patches(s))),('changed patch plan',sid)
                    print('PRESERVED '+sid,flush=True)
                    continue
                if project.exists() or wav.exists():
                    raise FileExistsError(f'Inspect existing output before retry: {project} / {wav}')
                inventory_check(s)
                # Failed jobs cannot be moved by a later job's pipeline cleanup.
                jobdir=STAGING/sid
                jobdir.mkdir(exist_ok=True)
                p.SK_DIR=str(jobdir)
                p.BOUNCE_SEARCH=[p.BOUNCE_DIR,p.PROJ_DIR,str(jobdir)]
                mid=jobdir/source.name
                if mid.exists() and mid.read_bytes()!=data:
                    raise FileExistsError(f'Stale staged MIDI: {mid}')
                if not mid.exists():
                    mid.write_bytes(data)
                if screen_locked():
                    raise RuntimeError('screen locked; no Logic mutation started')
                if not configured or (completed and completed%4==0 and completed!=last_restart):
                    p.restart_logic(log=configure_destination)
                    configured=True
                    last_restart=completed
                result=p.produce(sid,s['title'],'v2',str(mid),log=log,patches=patches(s))
                if result.get('ok'):
                    assert len(result['imported_tracks'])==len(s['tracks']),result
                    strip_names=re.findall(r'\[([^]]+)\]',result['strips'])
                    assert len(strip_names)>=len(s['tracks'])+2,('mixer evidence unavailable',result['strips'])
                    assert 'GM 기기' not in result['strips'],result['strips']
                    # All named patches here are legacy English names, not translated aliases.
                    for number,spec in patches(s).items():
                        loaded=result['patches'][number]
                        base,sampler=spec if isinstance(spec,tuple) else (spec,None)
                        assert loaded[1] and loaded[2][0]==base and loaded[2][1]==sampler,loaded
                    assert project.is_dir() and wav.is_file(),('missing final artifact',sid)
                    completed+=1
            except TimeoutError as exc:
                result=dict(ok=False,stage='timeout',status='대기 초과',msg=str(exc))
            except Exception as exc:
                result=dict(ok=False,stage='exception',msg=f'{type(exc).__name__}: {exc}')
                configured=False
            row=dict(sid=sid,midi_sha256=digest,requested_patches=patches(s),**result,**evidence)
            record(row)
            if not result.get('ok'):
                failed.append(sid)
                # The orchestrating session inspects failures before an explicit sid retry.
                # inventory_check() revalidates every name at the start of that retry.
        return failed


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('sids',nargs='*')
    args=parser.parse_args()
    failures=run(args.sids)
    print('FAILED',failures,flush=True)
    raise SystemExit(1 if failures else 0)
