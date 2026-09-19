"""Shared arrangement engine for the recorded themes and feedback revisions."""
from collections import defaultdict
from pathlib import Path
import hashlib
import json
import math
import random
import re
import struct
import sys
import pipeline as p

SKETCHES = Path(__file__).resolve().parents[1] / 'sketches'
IDS = ['returning-tide-astra-v2','paper-lanterns-astra-v2','blue-window-astra-v2',
       'northbound-lights-astra-v2','after-the-rain-astra-v2']
# name, bars, section role, meter; lengths and routes intentionally differ.
FORMS = {
 'tide': [('Nylon Memory',8,'intro',6,8),('Warm Current',8,'build',6,8),('Verse 1',24,'verse',6,8),('Refrain 1',16,'chorus',6,8),('Verse 2',24,'verse',6,8),('Refrain 2',16,'chorus',6,8),('Ebb',16,'bridge',6,8),('Returning',16,'final',6,8),('Shore',8,'outro',6,8)],
 'lantern': [('Breath',8,'intro',4,4),('Verse 1',16,'verse',4,4),('Refrain 1',12,'chorus',4,4),('Turnaround',4,'build',4,4),('Verse 2',16,'verse',4,4),('Refrain 2',12,'chorus',4,4),('Weightless',8,'bridge',4,4),('Harmonica Flight',16,'solo',4,4),('Open Sky',16,'final',4,4),('Drift',8,'outro',4,4)],
 'window': [('Alone',8,'intro',3,4),('Verse 1',16,'verse',3,4),('Reflection 1',12,'chorus',3,4),('Verse 2',16,'verse',3,4),('Reflection 2',12,'chorus',3,4),('Empty Room',12,'bridge',3,4),('Unsaid',16,'final',3,4),('Window Light',12,'outro',3,4)],
 'north': [('Ignition',8,'intro',4,4),('Verse 1',16,'verse',4,4),('Chorus 1',16,'chorus',4,4),('Riff Break',8,'build',4,4),('Verse 2',16,'verse',4,4),('Chorus 2',16,'chorus',4,4),('Seven Steps',8,'bridge',7,8),('Guitar Breakout',16,'solo',4,4),('Headlights',16,'final',4,4),('Distance',8,'outro',4,4)],
 'rain': [('First Drops',8,'intro',4,4),('Verse 1',16,'verse',4,4),('First Opening',16,'chorus',4,4),('Breath',4,'build',4,4),('Verse 2',12,'verse',4,4),('Open Road',16,'chorus',4,4),('Looking Back',8,'bridge',4,4),('Clear Sky',12,'final',4,4),('Afterglow',8,'outro',4,4)]}
# PC27 provides a Sampler slot; named EXS overrides are required before rendering.
PALETTES = {
 'tide': [('drums',0,'SoCal'),('bass',27,'Fingerstyle Electric Bass'),('theme',27,'Classical Acoustic Guitar'),('lead',0,'Studio Grand'),('chords',27,'Classical Acoustic Guitar'),('pad',89,'Classic Pad'),('upper',0,'Studio Grand')],
 'lantern': [('drums',0,'SoCal'),('bass',27,'Fingerstyle Electric Bass'),('lead',27,'Astra Air Harmonica'),('chords',25,'Acoustic Guitar'),('upper',4,'Deluxe Classic')],
 'window': [('lead',0,'Studio Grand'),('chords',0,'Studio Grand'),('bass',27,'Upright Jazz Bass'),('drums',0,'SoCal')],
 'north': [('drums',0,'SoCal'),('bass',27,'Fingerstyle Electric Bass'),('lead',26,'Hard Rock'),('chords',26,'Hard Rock'),('brass',27,'Full Brass Staccato')],
 'rain': [('drums',0,'SoCal'),('lead',0,'Studio Grand'),('bass',27,'Fingerstyle Electric Bass'),('chords',25,'Acoustic Guitar'),('strings',50,'Authentic Strings'),('upper',0,'Studio Grand')]}
PITCH = {'C':0,'C#':1,'Db':1,'D':2,'D#':3,'Eb':3,'E':4,'F':5,'F#':6,'Gb':6,'G':7,'G#':8,'Ab':8,'A':9,'A#':10,'Bb':10,'B':11}
QUALITY = {'':(0,4,7),'m':(0,3,7),'7':(0,4,7,10),'maj7':(0,4,7,11),'m7':(0,3,7,10),'6':(0,4,7,9),'sus2':(0,2,7),'sus4':(0,5,7),'m7b5':(0,3,6,10)}


def chord(name):
    label, *inversion = name.split('/')
    match = re.fullmatch(r'([A-G](?:#|b)?)(.*)',label)
    assert match and match[2] in QUALITY, name
    root = PITCH[match[1]]
    bass = 36 + PITCH[inversion[0]] if inversion else 36 + root
    tones = sorted(60 + (root + interval) % 12 for interval in QUALITY[match[2]])
    return bass, tones, 48 + root


def compose(data):
    style = data['style']
    version = data.get('revision', 2)
    assert version in (2, 3), version
    revised = version == 3
    title = f"{data['title']} Astra v{version}"
    form = data.get('form', FORMS[style])
    palette = data.get('palette', PALETTES[style])
    family_id = data['id'].rsplit('-v', 1)[0] + '-v2'
    rng = random.Random(2900 + IDS.index(family_id))
    notes, cc = defaultdict(list), defaultdict(list)
    roles = {role:i for i,(role,_,_) in enumerate(palette)}
    tracks = [(role.title()+' - '+patch,9 if role=='drums' else i) for i,(role,pc,patch) in enumerate(palette)]
    pcs = {i:pc for i,(_,pc,_) in enumerate(palette)}
    tempo_us = round(60000000/data['bpm'])
    sec_per_q = tempo_us/1000000
    tick = 0
    bar = 1
    sections, bar_map = [], []
    melody = data['melodies']
    for name,count,kind,num,den in form:
        q = num*4/den
        start_tick = tick
        for offset in range(count):
            bar_map.append((bar,tick,q,kind,name,offset,count))
            tick += round(q*p.PPQ)
            bar += 1
        sections.append(dict(name=name,kind=kind,bars=count,meter=[num,den],bar=bar-count,
                             start=start_tick/p.PPQ*sec_per_q,end=tick/p.PPQ*sec_per_q,tick=start_tick))
    end_tick = tick
    first_chorus = next(s for s in sections if s['kind'] == 'chorus')

    def emit(role, start, q, beat, pitch, dur, velocity, jitter=True):
        if role not in roles or beat >= q or dur <= 0:
            return
        assert 0 <= beat < q and 0 <= pitch <= 127, (role,beat,pitch,q)
        onset = start + round(beat*p.PPQ)
        if jitter:
            onset = max(start,onset+rng.randint(-7,7))
            velocity += rng.randint(-8,8)
        duration = min(round(dur*p.PPQ),start+round(q*p.PPQ)-onset)
        assert duration>0
        notes[roles[role]].append((onset,duration,pitch,max(1,min(120,velocity))))

    def phrase(role,start,q,events,velocity):
        for beat,pitch,dur in events:
            assert beat>=0 and dur>0 and beat+dur <= q+.00001, (data['id'],events,q)
            emit(role,start,q,beat,pitch,dur,velocity)

    for bar,start,q,kind,name,offset,count in bar_map:
        chorus = kind in ('chorus','final')
        final = kind=='final'
        bridge = kind=='bridge'
        outro = kind=='outro'
        early = style=='rain' and bar < first_chorus['bar']
        opening = revised and style=='rain' and kind=='chorus' and name==first_chorus['name']
        spotlight = revised and kind=='solo' and style in ('north','lantern')
        key = 'chorus' if kind in ('chorus','final','solo') else 'intro' if kind in ('intro','build') else kind
        progression = data['progressions'][key]
        bass,voice,power_root = chord(progression[offset % len(progression)])
        last = bar==len(bar_map)
        # Melodies follow their own phrase rhythm, not an invariant rising prechorus.
        melodic_key = 'theme' if kind in ('intro','build') else 'hook' if kind=='chorus' else 'peak' if final else 'solo' if kind=='solo' else kind
        material = melody[melodic_key]
        events = material[offset % len(material)]
        lead_role = 'theme' if style=='tide' and kind in ('intro','build','outro') else 'lead'
        if revised and style=='tide' and kind=='verse' and offset%4==3:
            lead_role = 'theme'
        lead_vel = 64
        if style=='tide': lead_vel=68 if chorus else 59
        if style=='lantern': lead_vel=77 if final or kind=='solo' else 69 if chorus else 61
        if style=='window': lead_vel=49 if final else 56 if chorus else 45 if bridge or outro else 51
        if style=='north': lead_vel=91 if final or kind=='solo' else 83 if chorus else 77
        if style=='rain': lead_vel=79 if final else 72 if chorus else 54 if early else 62
        if opening: lead_vel=min(70,58+offset*2)
        if outro: lead_vel=max(28,lead_vel-15-int(12*offset/max(1,count-1)))
        phrase(lead_role,start,q,events,lead_vel)
        if last:
            # The last bar is a tonic landing with an audible release window.
            idx=roles[lead_role]
            notes[idx]=[n for n in notes[idx] if n[0]<start]
            emit(lead_role,start,q,0,data['key']['tonic'],max(.7,q-1),35,False)

        # Each track family has a different rhythm/entry contract.
        if style=='tide':
            if bar>=5 and not (bridge and offset<8) and not (outro and offset>=4):
                for beat,dur,pitch in [(0,1.15,bass),(1.5,.8,bass+7),(2.5,.3,bass)]:
                    emit('bass',start,q,beat,pitch,dur,(58 if chorus else 52) if revised else (69 if chorus else 62))
            if bar>=9 and not (bridge and offset<4) and not (outro and offset>=4):
                for beat in ([0,1.5] if chorus else [.5,2]):
                    for j,pitch in enumerate(voice[:3]):
                        emit('chords',start,q,beat+j*.025,pitch,1.0,52 if chorus else 42)
            if bar>=9 and offset%2==0 and not(outro and offset>=4):
                for pitch in (power_root,power_root+7):
                    # Two-bar sustained pad; root+fifth only, behind nylon and bass.
                    idx=roles['pad']
                    notes[idx].append((start,min(round(q*p.PPQ*1.95),end_tick-start),pitch,28 if chorus else 23))
            if chorus and offset%4==3:
                phrase('upper',start,q,melody['upper'][(offset//4)%4],42)
            if not revised and kind=='verse' and offset%4==3:
                phrase('theme',start,q,melody['theme'][offset%4][-1:],39)
        elif style=='lantern':
            if bar>=5 and not(outro and offset>=4):
                pattern=[(0,.32,bass),(.75,.2,bass+7),(1.5,.28,bass+12),(2.25,.2,bass+7),(2.75,.25,bass),(3.5,.23,bass+7)]
                if bridge: pattern=[(0,.4,bass),(2.5,.3,bass+7)]
                if spotlight: pattern=[(0,.32,bass),(1.5,.28,bass+7),(2.75,.25,bass)]
                for beat,dur,pitch in pattern:
                    emit('bass',start,q,beat,pitch,dur,48 if spotlight else 62 if chorus or kind=='solo' else 56)
            if bar>=5 and not (bridge and offset<4) and not(outro and offset>=4):
                accents=(0,) if spotlight and offset%2==0 else () if spotlight else (.5,1.75,2.5,3.25)
                for beat in accents:
                    for j,pitch in enumerate(voice[:2] if spotlight else voice[:3]):
                        emit('chords',start,q,beat+j*.014,pitch,.24,29 if spotlight else 42 if chorus else 34)
            if (chorus or kind=='solo') and not spotlight:
                if offset%2==1: phrase('upper',start,q,melody['upper'][(offset//2)%4],38)
        elif style=='window':
            if kind in ('verse','chorus') and offset%2==0:
                # One exposed interval, never a wall of stacked chord tones.
                for pitch in (voice[0]-12,voice[1]): emit('chords',start,q,0,pitch,1.35,30,False)
            if kind=='verse' and '2' in name and offset%4==0:
                emit('bass',start,q,.1,bass,1.4,32)
            if kind=='chorus' and offset%4==0:
                emit('bass',start,q,0,bass,1.6,35)
            if final and offset%4==2:
                emit('chords',start,q,1,voice[1],.8,26)
        elif style=='north':
            if not(outro and offset>=4):
                pattern=[(0,.24,bass),(.5,.18,bass),(1.25,.22,bass+7),(1.75,.18,bass),(2.5,.2,bass+12),(3,.17,bass+7),(3.5,.24,bass)]
                if bridge: pattern=[(0,.25,bass),(1.5,.25,bass+7),(2.5,.2,bass),(3,.2,bass+12)]
                if spotlight:
                    pattern=[(0,.4,bass),(1.5,.3,bass+7),(2.5,.35,bass)]
                    if offset>=8: pattern=[(0,.4,bass),(.75,.22,bass+7),(2,.4,bass),(3.5,.2,bass+7)]
                for beat,dur,pitch in pattern: emit('bass',start,q,beat,pitch,dur,67 if spotlight else 78 if chorus else 71)
                accents=(.25,1,1.75,2.25,3.25) if not bridge else (0,1.5,2.5)
                if spotlight:
                    accents=() if offset<2 else (0,) if offset<8 and offset%2==0 else () if offset<8 else (.75,2.5)
                for beat in accents:
                    for pitch in (power_root,power_root+7):
                        emit('chords',start,q,beat,pitch,.35 if spotlight else .19 if not final else .28,
                             45 if spotlight and offset<8 else 54 if spotlight else 69 if chorus else 59)
            if revised and chorus:
                for beat in ((.5,2.5) if offset%2==0 else (1,2.75)):
                    for pitch in (power_root+12,power_root+19):
                        emit('brass',start,q,beat,pitch,.55 if offset%2==0 else .4,75 if final else 68)
            elif chorus and offset%2==1:
                for beat,pitch,dur in melody['upper'][(offset//2)%4]:
                    emit('brass',start,q,beat,pitch,min(.4,dur),65 if final else 55)
            if kind=='solo' and (not revised and offset%4==0 or revised and offset in (11,15)):
                for pitch in voice[:2]: emit('brass',start,q,3 if revised else 0,pitch,.23,48 if revised else 61)
        elif style=='rain':
            if not early and not (bridge and offset<4) and not(outro and offset>=4):
                pattern=[(0,1.4,bass),(2,.65,bass+7),(3.5,.3,bass)]
                if opening: pattern=[(0,1.5,bass)] if offset<4 else [(0,1.4,bass),(2.5,.7,bass+7)]
                bass_velocity=61 if chorus else 47
                if revised:
                    bass_velocity=min(55,40+offset*2) if opening else 61 if final else 52 if chorus else 47
                for beat,dur,pitch in pattern:
                    emit('bass',start,q,beat,pitch,dur,bass_velocity)
                if revised and not final:
                    accents=(.5,) if opening and offset<4 else (.5,2.5)
                    for beat in accents:
                        for j,pitch in enumerate(voice[:2]):
                            emit('chords',start,q,beat+j*.09,pitch,.9,min(44,30+offset*2) if opening else 38)
                else:
                    for beat in (0,1.5,2.75):
                        for j,pitch in enumerate(voice[:3]): emit('chords',start,q,beat+j*.025,pitch,.8,53 if chorus else 38)
            if revised:
                if final:
                    for pitch in voice[1:3]: emit('strings',start,q,0,pitch,3.8,46,False)
                elif kind=='chorus' and not opening and offset>=4:
                    voices=voice[1:2] if offset<8 else voice[1:3]
                    for j,pitch in enumerate(voices):
                        emit('strings',start,q,1+j*.3,pitch,2.5,20 if offset<8 else 24,False)
            elif (chorus and (bar>=57 or offset>=8)) or final:
                for pitch in voice[1:3]: emit('strings',start,q,0,pitch,3.8,46 if final else 34,False)
            if final or (kind=='chorus' and not opening and bar>40):
                if offset%4==3: phrase('upper',start,q,melody['upper'][(offset//4)%4],43)

        # Drums: no shared literal take. Blue remains intimate; Rain starts skeletal.
        hits=[]
        if style=='tide' and not(bridge and offset<8) and not(outro and offset>=4):
            hits=[(0,36,66),(1.5,37 if not chorus else 38,55),(2.5,36,43)]
            hits += [(b,42,36 if b in (0,1.5) else 26) for b in (0,.5,1,1.5,2,2.5)]
        elif style=='lantern' and not(outro and offset>=4):
            hits=[(0,36,62),(1.5,36,43),(2.75,36,48),(1,37,57),(3,37 if not final else 38,59)]
            hits += [(i*.5+(0.04 if i%2 else 0),42,40 if i%2==0 else 28) for i in range(8)]
            if bridge: hits=[(1,37,39),(3,44,30)]
            if spotlight:
                hits=[(0,36,46),(2.75,36,38),(1,37,45),(3,37,45)]
                hits += [(b,42,29) for b in (0,1,2,3)]
        elif style=='window' and kind in ('verse','chorus') and offset%2==0:
            hits=[(0,36,30),(2,37,28)]
        elif style=='north' and not(outro and offset>=4):
            kicks=(0,.75,1.75,2.5,3.5) if not bridge else (0,1.5,2.5)
            hits=[(b,36,86 if b==0 else 75) for b in kicks if b<q]
            hits += [(b,38,84) for b in ((1,3) if not bridge else (1,3)) if b<q]
            hits += [(i*.25,42 if i%8!=7 else 46,53 if i%2==0 else 33) for i in range(round(q*4))]
            if revised and not bridge:
                hits += [(.75,38,44),(2.75,38,49)]
            if spotlight:
                kicks=(0,1.5,2.5) if offset<2 else (0,2.5) if offset<8 else (0,1.5,2.5,3.5)
                hits=[(b,36,72) for b in kicks]+[(1,38,81),(3,38,84)]
                hats=(0,.5,1,1.5,2,2.5,3) if offset<2 else tuple(i*.5 for i in range(8))
                hits += [(b,42,38 if int(b*2)%2 else 46) for b in hats]
                if offset>=2: hits.append((2.75,38,44))
        elif style=='rain' and not(outro and offset>=4):
            if early: hits=[(0,36,36),(2,37,31)] if bar%2 else [(2,37,29)]
            elif bridge and offset<4: hits=[]
            else:
                hits=[(0,36,67),(2.5,36,55),(1,38,63),(3,38,68)]
                hits += [(i*.5,42,43 if i%2==0 else 30) for i in range(8)]
            if revised and not early and not final:
                if opening and offset<4:
                    hits=[(0,36,39),(2,37,34)]
                elif not(bridge and offset<4):
                    hits=[(0,36,52),(2.5,36,42),(1,37,44),(3,37,47)]
                    hits += [(b,42,29) for b in (.5,1.5,2.5,3.5)]
        if chorus and offset==0 and style in ('north','rain') and not(revised and style=='rain' and not final):
            hits.append((0,49,82 if style=='north' else 57))
        if offset==count-1 and kind in ('verse','chorus','solo') and style in ('north','rain','lantern') and not(revised and style=='rain'):
            hits=[h for h in hits if not(h[1]==38 and h[0]>=q-.5)]
            hits += [(q-.5,48,52),(q-.25,45,60)]
        for beat,pitch,velocity in hits: emit('drums',start,q,beat,pitch,.09,velocity)

    # Re-pedal only active piano bars, leaving true gaps where the score is sparse.
    for role,idx in roles.items():
        if palette[idx][1]==0 and role!='drums':
            for _,start,q,_,_,_,_ in bar_map:
                if any(start<=n[0]<start+round(q*p.PPQ) for n in notes[idx]):
                    cc[idx].extend([(start,64,0),(start+30,64,88),(start+round(q*p.PPQ)-30,64,0)])
        cc[idx].append((end_tick,64,0))
    # Humanised re-articulations may touch; previous note-offs must precede retriggers.
    for idx,events in notes.items():
        if palette[idx][0]=='drums': continue
        ordered=sorted(events)
        next_on={}
        result=[]
        for onset,duration,pitch,velocity in reversed(ordered):
            if pitch in next_on: duration=min(duration,next_on[pitch]-onset)
            if duration>0: result.append((onset,duration,pitch,velocity))
            next_on[pitch]=onset
        notes[idx]=list(reversed(result))
    cond=[p.meta(0,3,title.encode()),p.meta(0,0x51,struct.pack('>I',tempo_us)[1:]),
          p.meta(0,0x59,struct.pack('>bB',data['key']['sf'],int(data['key']['minor'])))]
    previous=None
    for section in sections:
        meter=section['meter']
        if meter!=previous:
            cond.append(p.meta(section['tick'],0x58,bytes([meter[0],int(math.log2(meter[1])),36 if meter==[6,8] else 24,8])))
            previous=meter
        cond.append(p.meta(section['tick'],6,section['name'].encode()))
    cond.append(p.meta(end_tick,6,b'END'))
    chunks=[p.track_chunk(cond)]
    windows=[]
    for idx,(name,channel) in enumerate(tracks):
        events=[p.meta(0,3,name.encode()),(0,0,bytes([0xC0|channel,pcs[idx]]))]
        for t,c,value in cc[idx]: events.append((t,0,bytes([0xB0|channel,c,value])))
        for t,duration,pitch,velocity in notes[idx]:
            assert 0<=t<t+duration<=end_tick
            events.extend([(t,2,bytes([0x90|channel,pitch,velocity])),(t+duration,1,bytes([0x80|channel,pitch,0]))])
            a=t/p.PPQ*sec_per_q+.04
            b=min((t+duration)/p.PPQ*sec_per_q,t/p.PPQ*sec_per_q+.8)
            if b>a: windows.append((a,b))
        chunks.append(p.track_chunk(events))
    merged=[]
    for a,b in sorted(windows):
        if merged and a<=merged[-1][1]: merged[-1][1]=max(merged[-1][1],b)
        else: merged.append([a,b])
    smf=b'MThd'+struct.pack('>IHHH',6,1,len(chunks),p.PPQ)+b''.join(chunks)
    manifest=dict(id=data['id'],title=title,style=style,bpm=data['bpm'],key=data['key'],
                  bars=len(bar_map),duration_seconds=end_tick/p.PPQ*sec_per_q,sections=sections,
                  tracks=[dict(role=r,pc=pc,patch=patch,notes=len(notes[i])) for i,(r,pc,patch) in enumerate(palette)],
                  active_intervals=merged,sha256_midi=hashlib.sha256(smf).hexdigest())
    return smf,manifest


if __name__=='__main__':
    for slug in sys.argv[1:] or IDS:
        assert slug in IDS, 'Use tide_v3.py for v3 section-preserving revisions'
        data=json.loads((SKETCHES/(slug+'.json')).read_text())
        smf,manifest=compose(data)
        (SKETCHES/(slug+'.mid')).write_bytes(smf)
        (SKETCHES/(slug+'-manifest.json')).write_text(json.dumps(manifest,indent=2)+'\n')
        print(slug,manifest['bpm'],manifest['bars'],round(manifest['duration_seconds'],3),[(t['role'],t['notes']) for t in manifest['tracks']])
