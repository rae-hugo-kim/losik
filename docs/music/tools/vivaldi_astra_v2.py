"""Independent Vivaldi v2 arrangements; plan committed as ca115d0 before implementation.
Model: openai-codex/gpt-6-astra. Source: Mutopia Project, CC BY-SA 3.0.
Generate: python3 -B docs/music/tools/vivaldi_astra_v2.py
Read-only proof: append --check. No other composer's module is imported.
"""
import argparse
import hashlib
import json
import random
import struct
from pathlib import Path

import pipeline as p
from vivaldi_data import MOVEMENTS, bar_tick

MODEL = 'openai-codex/gpt-6-astra'
CREDIT = f'Mutopia Project; CC BY-SA 3.0; arrangement {MODEL}'
PPQ = 480
ROOT = Path(__file__).resolve().parents[1]


def track(name, pc=0, patch=None):
    return dict(name=name, pc=pc, patch=patch)


# Each row is an authored orchestration, motif and harmonic palette, not a genre quota.
# Roots are relative to the tonic. Qualities describe the NEW accompaniment.
ROWS = [
    ('spring', 1, 'baroque chamber pop', (4,4), 88, 64, -12,
     '밝은 리토르넬로의 짧은 반복을 하프시코드·오보에·피치카토로 분리합니다.',
     [track('Rhythm',0),track('Bass',43),track('Harmony',patch='Harpsichord'),track('Lead',patch='Oboe'),track('Texture',patch=('Violins 1','Violins 1 Pizzicato'))],
     [(0,'maj9'),(2,'m7'),(7,'7'),(5,'maj7')], [4,7,6,2,4,0]),
    ('spring', 2, 'impressionist chamber nocturne', (3,4), 66, 64, -12,
     '목동의 느린 하강선과 3박 호흡을 잉글리시 호른·피아노·하프로 펼칩니다.',
     [track('Bass',42),track('Harmony',2),track('Lead',patch='English Horn'),track('Texture',patch='Harp')],
     [(0,'m9'),(8,'maj7'),(5,'m9'),(7,'7b9')], [7,3,2,0,11,2]),
    ('spring', 3, 'Celtic folk jig', (6,8), 96, 96, -12,
     '시칠리아나의 춤을 두 큰 박으로 묶고 휘슬과 발현의 대조를 만듭니다.',
     [track('Rhythm',26),track('Bass',32),track('Harmony',25),track('Lead',patch='Celtic Tin Whistle'),track('Texture',patch='Celtic Harp')],
     [(0,'6'),(7,'sus'),(5,'maj7'),(0,'add9')], [7,9,11,9,7,4]),
    ('summer', 1, 'desert trip-hop', (4,4), 62, 48, -12,
     '더위의 한숨과 끊긴 몸짓을 건조한 우드와 반박자 비트로 옮깁니다.',
     [track('Rhythm',24),track('Bass',39),track('Harmony',7),track('Lead',patch='Turkish Oud Lute'),track('Texture',107)],
     [(0,'m9'),(5,'m7'),(0,'m6'),(10,'sus')], [0,2,3,7,5,2]),
    ('summer', 2, 'chamber suspense score', (5,4), 80, 48, -24,
     '긴 음 사이의 천둥을 3+2 불균형과 바순·트레몰로·팀파니로 표현합니다.',
     [track('Pulse',patch='Timpani'),track('Bass',42),track('Harmony',12),track('Lead',patch='Bassoon Solo'),track('Texture',patch=('Violins 1','Violins 1 Tremolo'))],
     [(0,'m9'),(8,'maj7'),(2,'dim'),(7,'7b9')], [7,3,2,8,7,0]),
    ('summer', 3, 'progressive rock', (7,8), 126, 112, 0,
     '폭풍의 반복과 런을 2+2+3 강세와 기타·오르간 리프로 밀어갑니다.',
     [track('Rhythm',8),track('Bass',34),track('Harmony',18),track('Lead',30),track('Texture',48)],
     [(0,'m7'),(10,'add9'),(8,'maj7'),(7,'7')], [0,7,10,7,5,3]),
    ('autumn', 1, 'New Orleans second-line jazz', (4,4), 100, 72, -12,
     '수확 춤의 들뜬 반복음을 클라리넷과 행진형 싱코페이션으로 바꿉니다.',
     [track('Rhythm',0),track('Bass',32),track('Harmony',1),track('Lead',patch='Clarinet Solo'),track('Texture',57)],
     [(0,'6'),(9,'m7'),(2,'m9'),(7,'13')], [4,7,9,10,9,7]),
    ('autumn', 2, 'chamber passacaglia', (3,4), 64, 64, 0,
     '잠든 화음의 반음 움직임을 독주 바이올린·새 저음 반복·내성으로 엮습니다.',
     [track('Bass',42),track('Harmony',patch='Harpsichord'),track('Lead',patch=('Violins 1','Violin (Arco)')),track('Texture',patch='Bassoon Solo')],
     [(0,'m9'),(5,'m7'),(8,'7'),(7,'7b9')], [0,7,5,2,3,0]),
    ('autumn', 3, 'cinematic hunting scherzo', (6,8), 100, 96, -12,
     '사냥의 도약을 호른이 부르고 스타카토 현·팀파니가 추격합니다.',
     [track('Pulse',patch='Timpani'),track('Bass',43),track('Harmony',patch=('Violins 1','Violins 1 Staccato')),track('Lead',patch='French Horn Solo'),track('Texture',48)],
     [(0,'add9'),(5,'6'),(7,'sus'),(2,'m7')], [0,7,4,9,7,0]),
    ('winter', 1, 'industrial breakbeat', (4,4), 112, 80, -12,
     '떨림 반복음을 차가운 짧은 신스 어택과 비대칭 비트로 나눕니다.',
     [track('Rhythm',16),track('Bass',39),track('Harmony',8),track('Lead',82),track('Texture',98)],
     [(0,'m9'),(1,'maj7'),(5,'m7'),(7,'7b9')], [0,1,7,6,3,0]),
    ('winter', 2, 'acoustic bossa nova', (4,4), 90, 64, 0,
     '실내의 노래와 빗방울을 플루트·나일론 엇박·비브라폰으로 만듭니다.',
     [track('Rhythm',40),track('Bass',32),track('Harmony',24),track('Lead',patch='Flute Solo'),track('Texture',11)],
     [(0,'maj9'),(4,'m7'),(2,'m9'),(7,'13')], [7,4,2,0,2,4]),
    ('winter', 3, 'contemporary minimalist chamber', (5,8), 92, 112, 0,
     '빙판 회전음을 3+2와 피치카토·마림바·하프의 서로 다른 주기로 움직입니다.',
     [track('Bass',42),track('Harmony',12),track('Lead',patch=('Violins 1','Violin (Pizzicato)')),track('Texture',patch='Harp')],
     [(0,'m6'),(8,'maj7'),(5,'m9'),(10,'sus')], [7,8,7,3,2,0]),
]
QUALITIES = {'maj9':(0,4,7,11,14), 'maj7':(0,4,7,11), 'm9':(0,3,7,10,14),
             'm7':(0,3,7,10), '7':(0,4,7,10), '7b9':(0,4,7,10,13),
             '13':(0,4,10,14,21), '6':(0,4,7,9), 'm6':(0,3,7,9),
             'add9':(0,4,7,14), 'sus':(0,5,7,10), 'dim':(0,3,6,9)}
TONIC = {'spring':(4,1,4), 'summer':(7,7,7), 'autumn':(5,2,5), 'winter':(5,3,5)}
REPRISE_SHIFT = (12, 0, 12, 0, 12, -12, 12, -12, -12, 12, 0, 0)
SKETCHES = []
for index, row in enumerate(ROWS):
    season,n,genre,meter,bpm,bars,shift,reason,tracks,harmony,motif = row
    key = (season,n)
    SKETCHES.append(dict(key=key, sid=f'vs-{season}{n}-astra',
        title=f'{season.title()} {("I","II","III")[n-1]} Astra', genre=genre,
        genre_reason=reason, meter=meter,bpm=bpm,bars=bars,tracks=tracks,
        theme_part='violin1' if key==('autumn',2) else 'solo',
        theme_window=(4,12) if key==('winter',1) else MOVEMENTS[key]['theme'],
        rhythm_ops=['syncopation','half-duration','run-thinning','subdivision'],
        notes=reason, shift=shift, palette=harmony, motif=motif,
        tonic=TONIC[season][n-1], index=index))


def ticks(s):
    return s['meter'][0]*PPQ*4//s['meter'][1]


def sections(s):
    q=s['bars']//4
    middle=s['bars']//2-16
    return [(1,'intro'),(9,'themeA'),(9+q,'development'),
            (9+q+middle//2,'bridge'),(s['bars']-7-q,'themeB'),(s['bars']-7,'outro')]


def section_at(s, bar):
    return next((b,name) for b,name in reversed(sections(s)) if b<=bar)


def source_phrase(s):
    """One complete source window mapped once into each thematic section."""
    a,z=s['theme_window']
    lo,hi=bar_tick(s['key'],a),bar_tick(s['key'],z+1)
    length=s['bars']//4*ticks(s)
    scale=length/(hi-lo)
    raw=[(t-lo,d,pitch+s['shift']) for t,d,pitch in MOVEMENTS[s['key']]['parts'][s['theme_part']] if lo<=t<hi]
    grid=120 if s['index'] in (2,5,8,9,11) else 240
    cells={}
    for t,d,pitch in raw:
        pos=min(length-grid, int((t*scale+grid/2)//grid)*grid)
        # Retain the longer source note when several ornaments quantize to one cell.
        if pos not in cells or d>cells[pos][0]:
            cells[pos]=(d,pitch,max(96,round(d*scale)))
    reference=sorted(cells)
    events=[]
    for i,(t,(_,pitch,d)) in enumerate(sorted(cells.items())):
        bar=t//ticks(s)
        off=t%ticks(s)
        push=-60 if off%PPQ==0 and off else 0
        swing=40 if s['index'] in (3,6) and (off//240)%2 else 0
        delay=120 if i==0 or (off==0 and bar%2==0) else 0
        start=t+push+swing+delay
        lower=events[-1][0]+120 if events else 0
        upper=reference[i+1]-120 if i+1<len(reference) else length-120
        start=max(lower,min(start,upper))
        assert start>=0 and (not events or start>events[-1][0])
        duration=round(d*(.5 if i%3==0 else .9))
        events.append((start,max(72,duration),pitch))
    events=[(t,min(d,(events[i+1][0] if i+1<len(events) else length)-t-24),pitch)
            for i,(t,d,pitch) in enumerate(events)]
    assert all(d>=60 for _,d,_ in events)
    return events,reference,length


def lead_notes(s):
    phrase,_,length=source_phrase(s)
    out=[]
    for start,name in sections(s):
        stop=next((b for b,_ in sections(s) if b>start),s['bars']+1)
        if name in ('themeA','themeB'):
            for i,(t,d,pitch) in enumerate(phrase):
                # Different articulation/dynamics at the reprise, never a simultaneous source voice.
                dur=d if name=='themeA' else max(60,round(d*(.8 if i%4==3 else 1)))
                pitch += REPRISE_SHIFT[s['index']] if name=='themeB' else 0
                out.append(((start-1)*ticks(s)+t,dur,pitch,name))
        elif name=='development':
            for bar in range(start,stop):
                unit=(bar-start)%len(s['motif'])
                for j,beat in enumerate((.5, s['meter'][0]*4/s['meter'][1]-.75)):
                    pitch=60+s['tonic']+s['motif'][(unit+j)%len(s['motif'])]
                    if s['index']==4:
                        pitch-=12
                    out.append(((bar-1)*ticks(s)+round(beat*PPQ),180+120*(j==0),pitch,name))
    if s['key']==('spring',1):
        out.append((8*ticks(s)-240,180,76+s['shift'],'pickup'))
    return sorted(out)


def harmony_at(s, bar, melody):
    preferred=(bar//2+s['index'])%len(s['palette'])
    start=(bar-1)*ticks(s)
    heard=[(pitch%12,min(t+d,start+ticks(s))-max(t,start)) for t,d,pitch,_ in melody if t<start+ticks(s) and t+d>start]
    def cost(item):
        i,(interval,quality)=item
        root=(s['tonic']+interval)%12
        pcs={(root+x)%12 for x in QUALITIES[quality]}
        return (sum(weight*(0 if pitch in pcs else 2 if any((pitch-x)%12 in (1,11) for x in pcs) else .5)
                    for pitch,weight in heard), (i-preferred)%len(s['palette']))
    interval,quality=min(enumerate(s['palette']),key=cost)[1] if heard else s['palette'][preferred]
    if bar==s['bars']:
        interval,quality=s['palette'][0]
    root=(s['tonic']+interval)%12
    return root,quality


def compose(sid):
    s=next(s for s in SKETCHES if s['sid']==sid)
    size=ticks(s); beats=size/PPQ; end=s['bars']*size
    rng=random.Random(110900+s['index'])
    nt={i:[] for i in range(len(s['tracks']))}; cc={i:[] for i in nt}
    roles={t['name']:i for i,t in enumerate(s['tracks'])}
    lead=lead_notes(s)
    def note(i,t,d,pitch,velocity,jitter=7):
        t=max(0,min(end-1,round(t)+rng.randint(-jitter,jitter)))
        d=min(max(1,round(d)),end-t-12)
        if d>0:
            nt[i].append((t,d,pitch,max(28,min(112,velocity+rng.randint(-6,6)))))
    bass_patterns=[(0,2,3.5),(0,2),(0,1.5,2.5),(0,.75,2.5),(0,3,4.5),
                   (0,.5,1,2,2.5,3),(0,1,2,3),(0,1,2),(0,1.5,2.5),
                   (0,.75,1.5,2.75,3.5),(0,1.5,2,3.5),(0,1.5)]
    for bar in range(1,s['bars']+1):
        start=(bar-1)*size
        _,sec=section_at(s,bar)
        root,quality=harmony_at(s,bar,lead)
        iv=QUALITIES[quality]
        # Bass supplies the root; extended chords keep their seventh/ninth/thirteenth.
        chord=[48+root+x for x in (iv[1:] if len(iv)>4 else iv)]
        voices=chord if sec!='themeB' else chord[1:]+[chord[0]+12]
        shift=12 if s['index'] in (2,9) else 0
        harmony=roles['Harmony']; bass=roles['Bass']; tex=roles['Texture']
        if bar>=3 and bar<=s['bars']-2:
            pattern=bass_patterns[s['index']]
            for j,beat in enumerate(pattern):
                nextbeat=pattern[j+1] if j+1<len(pattern) else beats
                pitch=36+root+(iv[j%min(3,len(iv))] if s['index'] in (5,6,7) else -5 if j%3==2 else 0)
                if pitch>55: pitch-=12
                note(bass,start+beat*PPQ,(nextbeat-beat)*PPQ-70,pitch,70 if sec!='bridge' else 61)
        if s['index'] in (1,11):
            attacks=[j*.5 for j in range(round(beats*2))]
        elif s['index']==3:
            attacks=[.25,1.75,3]
        elif s['index']==4:
            attacks=[0,1.5,3,4]
        elif s['index']==5:
            attacks=[0,1,2]
        elif s['index']==6:
            attacks=[0,1.5,2.75]
        elif s['index']==9:
            attacks=[0,.75,1.5,2.5,3.25]
        elif s['index']==10:
            attacks=[0,.75,1.5,2.5,3.5]
        else:
            attacks=[0,beats/2]
        if sec=='bridge': attacks=attacks[::2]
        if bar==s['bars']: attacks=[0]
        for j,beat in enumerate(attacks):
            t=start+beat*PPQ
            duration=((attacks[j+1]-beat)*PPQ if j+1<len(attacks) else size-beat*PPQ)-60
            if s['index'] in (1,4,9,11):
                pitches=[voices[(j+bar)%len(voices)]+shift]
                duration=min(duration,380)
            else:
                pitches=voices
                duration=min(duration,250 if s['index'] in (2,3,8,10) else 700)
            if bar==s['bars']: duration=min(duration,size-PPQ)
            for k,pitch in enumerate(pitches):
                note(harmony,t+k*9,duration,pitch,66 if sec in ('intro','bridge','outro') else 77)
            if s['tracks'][harmony]['pc'] in (0,1,2,3,4) and not s['tracks'][harmony]['patch']:
                cc[harmony].extend([(max(0,round(t)-20),64,0),(round(t)+30,64,95),(round(t+duration)+20,64,0)])
        if bar<s['bars']:
            if s['index'] in (4,5,8,9):
                for pitch in (60+root,60+root+7):
                    note(tex,start,size-60,pitch,48 if s['index']==9 else 58)
                cc[tex].extend([(start,11,60),(start+size//2,11,88 if sec=='themeB' else 76)])
            else:
                pos=[.5,beats-.5] if s['index'] in (0,6,7) else [j*.5+.25 for j in range(int(beats*2)) if j*.5+.25<beats]
                for j,beat in enumerate(pos):
                    pitch=chord[(j+2+bar)%len(chord)]+(12 if s['index'] in (1,2,10,11) else -12 if s['index']==7 else 0)
                    note(tex,start+beat*PPQ,170 if s['index']!=7 else 350,pitch,59 if sec!='themeB' else 68)
        if 'Pulse' in roles and bar>=3 and bar<s['bars']-1:
            for beat in ([0,3] if s['index']==4 else [0,1.5]):
                note(roles['Pulse'],start+beat*PPQ,300,36+root,60 if sec=='bridge' else 78)
            if bar%8==0:
                for j in range(4):
                    note(roles['Pulse'],start+size-480+j*120,90,36+root,55+j*8)
        if 'Rhythm' in roles and 5<=bar<=s['bars']-2:
            dr=roles['Rhythm']
            patterns={0:([0,1.75,2.5],[1,3]),2:([0,1.5],[1.5]),3:([0,1.75,3.25],[2]),
                      5:([0,1,2.5],[1.5,3]),6:([0,2],[1,2.75,3.5]),
                      9:([0,.75,2.5,3.25],[1,3]),10:([0,2],[.5,1.5,2.5,3.75])}
            kicks,snares=patterns[s['index']]
            if sec!='bridge':
                for beat in kicks:
                    note(dr,start+beat*PPQ,80,36,92 if s['index'] not in (2,10) else 79)
                for beat in snares:
                    note(dr,start+beat*PPQ,85,37 if s['index'] in (2,10) else 38,83)
            for j in range(round(beats*2)):
                if sec=='bridge' and j%2: continue
                offset=55 if s['index']==6 and j%2 else 25 if s['index']==3 and j%2 else 0
                pitch=70 if s['index']==10 else 51 if s['index']==6 else 42
                note(dr,start+j*240+offset,70,pitch,55+(12 if j%2 else 0))
            if bar%4==0 and sec!='bridge':
                for j in (0,1): note(dr,start+size-240+j*120,75,45-j*4,66+j*8)
            if bar in [b for b,name in sections(s) if name in ('themeA','themeB')]:
                note(dr,start+120,300,49,75)
    li=roles['Lead']
    for t,d,pitch,sec in lead:
        note(li,t,d,pitch,82 if sec!='themeB' else 90,jitter=5)
        if d>=PPQ:
            cc[li].extend([(max(0,t-8),11,72),(t+d//2,11,96 if sec=='themeB' else 88)])
    for i,notes in nt.items():
        notes.sort()
        prior={}
        for j,(t,d,pitch,v) in enumerate(notes):
            if pitch in prior:
                k=prior[pitch]; a,b,c,e=notes[k]
                notes[k]=(a,min(b,t-a-1),c,e)
            prior[pitch]=j
        assert all(d>0 for _,d,_,_ in notes)
        cc[i].append((end-1,64,0))
    pcs={i:t['pc'] for i,t in enumerate(s['tracks'])}
    tracks=[(t['name'],9 if t['name']=='Rhythm' else i) for i,t in enumerate(s['tracks'])]
    return nt,cc,pcs,tracks


def patches(s):
    return {i+1:t['patch'] for i,t in enumerate(s['tracks']) if t['patch'] is not None}


def track_events(data, index=0):
    """Read generated SMF events, including attribution outside the conductor."""
    offset=14
    for _ in range(index):
        offset+=8+int.from_bytes(data[offset+4:offset+8],'big')
    assert data[offset:offset+4]==b'MTrk'
    length=int.from_bytes(data[offset+4:offset+8],'big')
    chunk=data[offset+8:offset+8+length]
    pos=tick=0; result=[]
    while pos<len(chunk):
        delta=0
        while True:
            x=chunk[pos];pos+=1;delta=(delta<<7)|(x&127)
            if x<128: break
        tick+=delta
        status=chunk[pos];pos+=1
        if status==255:
            kind=chunk[pos];pos+=1;size=0
            while True:
                x=chunk[pos];pos+=1;size=(size<<7)|(x&127)
                if x<128:break
        else:
            assert 0x80<=status<=0xef
            kind=status
            size=1 if status>>4 in (0xc,0xd) else 2
        result.append((tick,kind,chunk[pos:pos+size]));pos+=size
    return result


def render(s, report=True):
    nt,cc,pcs,tracks=compose(s['sid'])
    m=MOVEMENTS[s['key']]
    smf=p.build_smf(s['title'],s['bpm'],m['ks'][0],'minor' in m['key_name'],s['bars'],tracks,pcs,nt,cc,sections(s),timesig=s['meter'])
    credit=b'\x00'+p.meta(0,2,CREDIT.encode())[2]
    # Logic turns a text-bearing conductor into an extra instrument track.
    # Put copyright on the first actual instrument, preserving 1-based patch numbering.
    offset=22+int.from_bytes(smf[18:22],'big')
    original=int.from_bytes(smf[offset+4:offset+8],'big')
    smf=smf[:offset+4]+struct.pack('>I',original+len(credit))+credit+smf[offset+8:]
    check(s,nt,cc,smf,report)
    return smf


def check(s,nt,cc,data,report=True):
    size=ticks(s);end=size*s['bars']
    assert abs(s['bpm']/MOVEMENTS[s['key']]['tempo_bpm']-1)>=.15
    assert all(0<=t<t+d<=end and 0<=pitch<=127 and 1<=v<=127 for ns in nt.values() for t,d,pitch,v in ns)
    for ns in nt.values():
        prev={}
        for t,d,pitch,v in ns:
            assert t>=prev.get(pitch,-1)
            prev[pitch]=t+d
    assert all(0<=t<=end and 0<=c<128 and 0<=v<128 for events in cc.values() for t,c,v in events)
    events=track_events(data)
    assert [(t,payload) for t,kind,payload in events if kind==0x58]==[(0,bytes([s['meter'][0],s['meter'][1].bit_length()-1,24,8]))]
    assert [(t,int.from_bytes(b,'big')) for t,k,b in events if k==0x51]==[(0,round(60000000/s['bpm']))]
    credits=[event for i in range(len(nt)+1) for event in track_events(data,i) if event[1]==2]
    assert credits==[(0,2,CREDIT.encode())]
    assert not any(kind==2 for _,kind,_ in events)
    assert all(((bar-1)*size,6,name.encode()) in events for bar,name in sections(s))
    assert (end,6,b'END') in events
    fmt,ntrk,division,info=p.parse_smf(data)
    assert fmt==1 and division==480 and ntrk==len(s['tracks'])+1
    assert sum(x['notes'] for x in info)==sum(map(len,nt.values()))
    phrase,reference,_=source_phrase(s)
    assert phrase,('empty source theme',s['sid'])
    theme_bars={bar for bar in range(1,s['bars']+1) if section_at(s,bar)[1] in ('themeA','themeB')}
    ratio=len(theme_bars)/s['bars']
    assert .4<=ratio<=.6
    lead_index=next(i for i,t in enumerate(s['tracks']) if t['name']=='Lead')
    sounding={bar for bar in theme_bars if any(t<bar*size and t+d>(bar-1)*size for t,d,_,_ in nt[lead_index])}
    unchanged=run=0
    for bar in range(s['bars']//4):
        a=[t-bar*size for t in reference if bar*size<=t<(bar+1)*size]
        b=[t-bar*size for t,_,_ in phrase if bar*size<=t<(bar+1)*size]
        run=run+1 if a and a==b else 0;unchanged=max(unchanged,run)
    assert unchanged<=4
    single=run=0;density={};bands={};sections_density={}
    for bar in range(1,s['bars']+1):
        active=sum(any(t<bar*size and t+d>(bar-1)*size for t,d,_,_ in ns) for ns in nt.values())
        interior=section_at(s,bar)[1] not in ('intro','outro')
        run=run+1 if interior and active<=1 else 0;single=max(single,run)
    assert single<=2,('thin interior',s['sid'],single)
    for i,ns in nt.items():
        name=s['tracks'][i]['name']
        assert ns,('empty track',name)
        bands[name]=[min(n[3] for n in ns),max(n[3] for n in ns)]
        density[name]=round(len(ns)/s['bars'],2)
    for start,name in sections(s):
        stop=next((b for b,_ in sections(s) if b>start),s['bars']+1)
        count=sum(start-1<=t//size<stop-1 for ns in nt.values() for t,_,_,_ in ns)
        sections_density[name]=round(count/(stop-start),2)
    metric=dict(sid=s['sid'],meter=s['meter'],bpm=s['bpm'],bars=s['bars'],unchanged_run=unchanged,
        theme_ratio=ratio,theme_sounding_bars=len(sounding),single_layer_run=single,velocity=bands,notes_per_bar=density,
        section_notes_per_bar=sections_density,bass_notes_per_bar=density['Bass'],
        last_note=max(t+d for ns in nt.values() for t,d,_,_ in ns),end_tick=end)
    if report: print('check '+json.dumps(metric,ensure_ascii=False)+' PASS',flush=True)
    return metric


if __name__=='__main__':
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--check',action='store_true')
    args=ap.parse_args()
    assert len(SKETCHES)==len({s['genre'] for s in SKETCHES})==12
    for s in SKETCHES:
        data=render(s)
        path=ROOT/'sketches'/(s['sid']+'-v2.mid')
        if args.check:
            assert path.read_bytes()==data,('stale MIDI',path)
        else:
            temp=path.with_suffix('.mid.tmp');temp.write_bytes(data);temp.replace(path)
        print(s['sid'],hashlib.sha256(data).hexdigest(),'MATCH' if args.check else 'WRITTEN',flush=True)
