# Vivaldi 사계 변주 v2 — astra (openai-codex/gpt-6-astra)

`docs/music/tools/vivaldi_astra_v2.py`가 만드는 12곡의 Suno Cover 프롬프트입니다. 장르와 편성은 커밋된 v2 계획(`vivaldi_astra_v2_plan.md`, `ca115d0`)과 작곡기 `ROWS`에서 가져왔으며, v1 장르를 참고하지 않았습니다.

출처: 주제 선율 데이터는 Mutopia Project의 *Le quattro stagioni* 판(`vivaldi_data.py`)에서 가져왔고, 변주 MIDI와 이 프롬프트는 CC BY-SA 3.0을 따릅니다. 표기: Mutopia Project; CC BY-SA 3.0; arrangement openai-codex/gpt-6-astra.

- 원곡에서 빌린 성부는 곡마다 하나(solo, Autumn II만 violin1)뿐입니다. 베이스·화음·대선율은 새로 썼고 원곡 베이스나 모방 성부를 따라 하지 않습니다.
- 형식은 전주 8마디, 주제 A `마디/4`, 자작 전개, 간주(리드 없음·킥/스네어 제외·화음 어택 절반), 주제 B `마디/4`, 후주 8마디입니다. 원전 주제 창 전체를 주제 구간 길이에 맞춰 다시 배치합니다.
- 주제 B의 리드는 `REPRISE_SHIFT`만큼 주제 A에서 옥타브 이동합니다. Spring I·III, Summer II, Autumn I, Winter I은 한 옥타브 위, Summer III, Autumn II·III은 한 옥타브 아래입니다. Spring II, Summer I, Winter II·III은 음역을 유지하고 아티큘레이션(4음마다 짧게)·세기·반주 전위(최저음을 위로 올린 보이싱)·텍스처 세기로 B를 구분합니다. Description의 원전 대비 옥타브 설명은 주제 A 기준입니다.
- 5성 화음(maj9·m9·7b9·13)은 근음을 베이스에 맡기고 나머지 네 음으로 보이싱해 9th·13th가 실제로 들립니다. 팔레트 이름은 그대로입니다.
- 화성은 고정 루프가 아닙니다. `harmony_at()`이 곡별 4코드 팔레트 안에서 그 마디에 울리는 선율과 덜 부딪히는 코드를 마디마다 고르고, 선율이 없으면 2마디마다 팔레트를 돌며, 마지막 마디는 으뜸화음입니다.
- BPM은 MIDI 4분음표 기준이고 길이는 `마디 × 마디당 4분음표 수 × 60/BPM`입니다. 바운스 WAV는 잔향 꼬리만큼 길 수 있습니다.
- B·C 경로 트랙은 SMF PC가 0(자리표시자)이고 실제 소리는 `produce(..., patches=...)`로 올리는 Logic 패치 이름입니다. 프롬프트의 악기 이름은 그 패치(예: `Oboe`, `Harp`, `Violins 1 Pizzicato`, `Violin (Arco)`)를 기준으로 썼으며 GM 소리를 기준으로 쓰지 않았습니다.
- 밀도는 구간별 전체 음 수/마디(주제 구간과 간주)를 `compose()` 결과에서 세어 적었습니다.
- 업로드 통과 여부는 주장하지 않습니다. 업로드 결과는 사용자 확인 전까지 미확인입니다.

길이는 파일을 쓴 뒤 일회성 Python 코드로 각 블록의 Style·Description을 `len()`으로 측정했습니다(공백·줄바꿈 포함). 모두 Style ≤300자, Description ≤1,000자입니다.

| sid | 장르 | 박자 | BPM | 마디 | 길이 | 주제 창 | Style 문자 수 | Description 문자 수 |
|---|---|---|---:|---:|---:|---|---:|---:|
| vs-spring1-astra | baroque chamber pop | 4/4 | 88 | 64 | 2:55 | 1–13 | 192 | 916 |
| vs-spring2-astra | impressionist chamber nocturne | 3/4 | 66 | 64 | 2:55 | 2–10 | 193 | 901 |
| vs-spring3-astra | Celtic folk jig | 6/8 | 96 | 96 | 3:00 | 1–12 | 226 | 966 |
| vs-summer1-astra | desert trip-hop | 4/4 | 62 | 48 | 3:06 | 1–30 | 168 | 944 |
| vs-summer2-astra | chamber suspense score | 5/4 | 80 | 48 | 3:00 | 1–8 | 200 | 962 |
| vs-summer3-astra | progressive rock | 7/8 | 126 | 112 | 3:07 | 1–20 | 202 | 943 |
| vs-autumn1-astra | New Orleans second-line jazz | 4/4 | 100 | 72 | 2:53 | 1–12 | 195 | 932 |
| vs-autumn2-astra | chamber passacaglia | 3/4 | 64 | 64 | 3:00 | 4–14 (violin1) | 176 | 881 |
| vs-autumn3-astra | cinematic hunting scherzo | 6/8 | 100 | 96 | 2:53 | 1–24 | 220 | 954 |
| vs-winter1-astra | industrial breakbeat | 4/4 | 112 | 80 | 2:51 | 4–12 | 204 | 912 |
| vs-winter2-astra | acoustic bossa nova | 4/4 | 90 | 64 | 2:51 | 1–8 | 184 | 980 |
| vs-winter3-astra | contemporary minimalist chamber | 5/8 | 92 | 112 | 3:03 | 1–24 | 208 | 925 |

## vs-spring1-astra-v2
**Style**
`baroque chamber pop, 88 BPM, E major, 4/4, crisp harpsichord chords, oboe lead, pizzicato violin section answers, bowed double bass, light acoustic pop drums, bright buoyant mood, instrumental`

**Description**
```
Spring I: 88 BPM, 4/4, E major, 64 bars, about 2:55. A variation on the theme of Vivaldi's Four Seasons, Spring I; no vocals. Form: intro 1-8, A 9-24, development 25-32, bridge 33-40, B 41-56, outro 57-64. Only one source voice; bass, chords and counter-lines are new. Oboe plays the solo-violin line in A (source bars 1-13, octave down) re-timed over 16 bars on an 8th grid with anticipations, late downbeats, every third note halved; a pickup ends the intro. Development: own motif G#-B-A#-F#-G#-E, 2 notes/bar. B: lead an octave up from A, louder, some notes clipped. Harpsichord chords on beats 1 and 3, picked per bar from Emaj9, F#m7, B7, Amaj7 by melody fit. Pizzicato violins answer on the and-of-1 and and-of-4; double bass on 1, 3 and the and-of-4. Acoustic kit from bar 5: kick 1, a-of-2, and-of-3, snare 2 and 4, 8th hats. Bridge drops oboe, kick and snare. Density ~32 notes/bar in themes, 13 in bridge.
```

## vs-spring2-astra-v2
**Style**
`impressionist chamber nocturne, 66 BPM, C# minor, 3/4, English horn lead, rippling grand piano broken chords, harp sixteenth shimmer, soft cello bass, no drums, hushed sleepy mood, instrumental`

**Description**
```
Spring II: 66 BPM, 3/4, C# minor, 64 bars, about 2:55. A variation on the theme of Vivaldi's Four Seasons, Spring II; no vocals. Form: intro 1-8, A 9-24, development 25-32, bridge 33-40, B 41-56, outro 57-64. Only one source voice; bass, chords and counter-lines are new. English horn plays the solo-violin line in A (source bars 2-10, octave down) stretched over 16 bars of 3/4 on an 8th grid with anticipations, late downbeats, every third note halved. Development: own motif G#-E-D#-C#-B#-D#, 2 notes/bar. B: same register as A; louder, every 4th note clipped, chords re-voiced, texture louder. Piano breaks each chord into single eighth notes, chords picked per bar from C#m9, Amaj7, F#m9, G#7b9 by melody fit. Harp plays offbeat 16ths, octave up; cellos on beats 1 and 3. No drums. Bridge drops the English horn and thins the piano to quarter notes. Density ~16 notes/bar in themes, 11 in bridge.
```

## vs-spring3-astra-v2
**Style**
`Celtic folk jig, 6/8, 96 BPM quarter note, E major, tin whistle lead, steel-string acoustic guitar strums on the two big beats, Celtic harp sixteenths, upright bass, light roots kit with side-stick, lilting dance, instrumental`

**Description**
```
Spring III: 96 BPM (quarter note), 6/8, E major, 96 bars, about 3:00. A variation on the theme of Vivaldi's Four Seasons, Spring III; no vocals. Form: intro 1-8, A 9-32, development 33-48, bridge 49-64, B 65-88, outro 89-96. Only one source voice; bass, chords and counter-lines are new. Tin whistle plays the solo-violin line in A (source bars 1-12 of 12/8, octave down) as 24 bars of 6/8 on a 16th grid with anticipations, late downbeats, every third note halved. Development: own motif B-C#-D#-C#-B-G#, 2 notes/bar. B: lead an octave up from A, louder, some notes clipped. Acoustic guitar plays short chords on the two dotted-quarter beats, picked per bar from E6, Bsus, Amaj7, Eadd9 by melody fit. Celtic harp plays offbeat 16ths, octave up; upright bass on both big beats plus the last 8th. Kit from bar 5: soft kick on both big beats, side-stick on the second, 8th hats. Bridge drops whistle, kick and side-stick. Density ~31 notes/bar in themes, 16 in bridge.
```

## vs-summer1-astra-v2
**Style**
`desert trip-hop, 62 BPM, G minor, 4/4, dry oud lead, half-time electronic drums, swung hats, clavinet stabs, koto offbeats, deep synth bass, hot hazy mood, instrumental`

**Description**
```
Summer I: 62 BPM, 4/4, G minor, 48 bars, about 3:06. A variation on the theme of Vivaldi's Four Seasons, Summer I; no vocals. Form: intro 1-8, A 9-20, development 21-24, bridge 25-28, B 29-40, outro 41-48. Only one source voice; bass, chords and counter-lines are new. Oud plays the solo-violin line in A (source bars 1-30 of 3/8, octave down) regrouped into 12 bars of 4/4 on a swung 8th grid with anticipations, late downbeats, every third note halved. Development: own motif G-A-Bb-D-C-A, 2 notes/bar. B: same register as A; louder, every 4th note clipped, chords re-voiced, texture louder. Clavinet plays short chords on the e-of-1, a-of-2 and beat 4, picked per bar from Gm9, Cm7, Gm6, Fsus by melody fit. Koto plays offbeat 16ths; synth bass on 1, a-of-1 and and-of-3. Electronic kit from bar 5: kick 1, a-of-2, e-of-4, half-time snare on 3, swung 8th hats. Bridge drops oud, kick and snare. Density ~40 notes/bar in themes, 24 in bridge.
```

## vs-summer2-astra-v2
**Style**
`chamber suspense score, 5/4 in 3+2, 80 BPM, G minor, low bassoon lead, tremolo violin section swells, timpani hits and rolls, marimba pulses, cello bass, no drum kit, tense brooding mood, instrumental`

**Description**
```
Summer II: 80 BPM, 5/4 grouped 3+2, G minor, 48 bars, about 3:00. A variation on the theme of Vivaldi's Four Seasons, Summer II; no vocals. Form: intro 1-8, A 9-20, development 21-24, bridge 25-28, B 29-40, outro 41-48. Only one source voice; bass, chords and counter-lines are new. Bassoon plays the solo-violin line in A (source bars 1-8 of 4/4, two octaves down) stretched over 12 bars of 5/4 on an 8th grid with anticipations, late downbeats, every third note halved. Development: own motif D-Bb-A-Eb-D-G, low, 2 notes/bar. B: lead an octave up from A, louder, some notes clipped. Marimba plays single chord tones on beats 1, and-of-2, 4 and 5, chords picked per bar from Gm9, Ebmaj7, Adim, D7b9 by melody fit. Tremolo violins hold root and fifth each bar with a swell; cellos on 1, 4 and the and-of-5. Timpani strike beats 1 and 4 with a short roll every 8 bars. Bridge drops the bassoon and halves the marimba. Density ~13 notes/bar in themes, 9 in bridge.
```

## vs-summer3-astra-v2
**Style**
`progressive rock, 7/8 in 2+2+3, 126 BPM, G minor, distorted lead guitar, driving rock organ chords, picked bass eighths, sustained string section, hard-hitting rock kit, stormy urgent mood, instrumental`

**Description**
```
Summer III: 126 BPM, 7/8 grouped 2+2+3, G minor, 112 bars, about 3:07. A variation on the theme of Vivaldi's Four Seasons, Summer III; no vocals. Form: intro 1-8, A 9-36, development 37-56, bridge 57-76, B 77-104, outro 105-112. Only one source voice; bass, chords and counter-lines are new. Distorted guitar plays the solo-violin line in A (source bars 1-20 of 3/4, at pitch) re-timed over 28 bars of 7/8 on a 16th grid with anticipations, late downbeats, every third note halved. Development: own motif G-D-F-D-C-Bb, 2 notes/bar. B: lead an octave down from A, louder, some notes clipped. Organ hits chords on the 2+2+3 group starts, picked per bar from Gm7, Fadd9, Ebmaj7, D7 by melody fit. Picked bass plays 8th-note chord tones; strings hold root and fifth. Rock kit from bar 5: kick on 8ths 1, 3 and 6, snare on 4 and 7, 8th hats, tom fill every 4 bars. Bridge drops guitar, kick and snare. Density ~41 notes/bar in themes, 20 in bridge.
```

## vs-autumn1-astra-v2
**Style**
`New Orleans second-line jazz, 100 BPM, F major, 4/4, clarinet lead, honky upright piano, walking upright bass, trombone stabs, syncopated parade drums with swung ride, festive strut, instrumental`

**Description**
```
Autumn I: 100 BPM, 4/4, F major, 72 bars, about 2:53. A variation on the theme of Vivaldi's Four Seasons, Autumn I; no vocals. Form: intro 1-8, A 9-26, development 27-36, bridge 37-46, B 47-64, outro 65-72. Only one source voice; bass, chords and counter-lines are new. Clarinet plays the solo-violin line in A (source bars 1-12, octave down) stretched over 18 bars on a swung 8th grid with anticipations, late downbeats, every third note halved. Development: own motif A-C-D-Eb-D-C, 2 notes/bar. B: lead an octave up from A, louder, some notes clipped. Upright piano plays pedaled chords on 1, the and-of-2 and the a-of-3, picked per bar from F6, Dm7, Gm9, C13 by melody fit. Upright bass walks chord tones on every beat; trombone answers on the and-of-1 and and-of-4. Kit from bar 5: kick 1 and 3, snare 2, a-of-3 and and-of-4, swung ride 8ths. Bridge drops clarinet, kick and snare. Density ~36 notes/bar in themes, 18 in bridge.
```

## vs-autumn2-astra-v2
**Style**
`chamber passacaglia, 64 BPM, D minor, 3/4, slow solo violin lead, harpsichord chords, repeating cello ground bass, bassoon inner line, no drums, drowsy still mood, instrumental`

**Description**
```
Autumn II: 64 BPM, 3/4, D minor, 64 bars, about 3:00. A variation on the theme of Vivaldi's Four Seasons, Autumn II; no vocals. Form: intro 1-8, A 9-24, development 25-32, bridge 33-40, B 41-56, outro 57-64. Only one source voice; bass, chords and counter-lines are new. Solo violin plays the first-violin line in A (source bars 4-14, at pitch) stretched over 16 bars on an 8th grid with anticipations, late downbeats, every third note halved. Development: own motif D-A-G-E-F-D, 2 notes/bar. B: lead an octave down from A, louder, some notes clipped. Cellos play a new ground bass of chord tones on every beat. Harpsichord plays chords on 1 and the and-of-2, picked per bar from Dm9, Gm7, Bb7, A7b9 by melody fit. Bassoon adds a low inner line on the and-of-1 and and-of-3. No drums. Bridge drops the violin and thins the harpsichord. Density ~14 notes/bar in themes, 9 in bridge.
```

## vs-autumn3-astra-v2
**Style**
`cinematic hunting scherzo, 6/8, 100 BPM quarter note, F major, bold French horn lead, staccato violin section chords, timpani on the big beats, sustained strings, double basses, no drum kit, galloping chase, instrumental`

**Description**
```
Autumn III: 100 BPM (quarter note), 6/8, F major, 96 bars, about 2:53. A variation on the theme of Vivaldi's Four Seasons, Autumn III; no vocals. Form: intro 1-8, A 9-32, development 33-48, bridge 49-64, B 65-88, outro 89-96. Only one source voice; bass, chords and counter-lines are new. French horn plays the solo-violin line in A (source bars 1-24 of 3/8, octave down) spread over 24 bars of 6/8 on a 16th grid with anticipations, late downbeats, every third note halved. Development: own call F-C-A-D-C-F, 2 notes/bar. B: lead an octave down from A, louder, some notes clipped. Staccato violins hit short chords on the two dotted-quarter beats, picked per bar from Fadd9, Bb6, Csus, Gm7 by melody fit. Strings hold root and fifth with swells; double basses on both big beats plus the last 8th. Timpani strike both big beats with a roll every 8 bars. Bridge drops the horn and halves the staccato chords. Density ~19 notes/bar in themes, 12 in bridge.
```

## vs-winter1-astra-v2
**Style**
`industrial breakbeat, 112 BPM, F minor, 4/4, short sync-saw synth lead, icy celesta stabs, broken kick pattern, hard snare on 2 and 4, gritty synth bass, glassy granular pad, cold tense mood, instrumental`

**Description**
```
Winter I: 112 BPM, 4/4, F minor, 80 bars, about 2:51. A variation on the theme of Vivaldi's Four Seasons, Winter I; no vocals. Form: intro 1-8, A 9-28, development 29-40, bridge 41-52, B 53-72, outro 73-80. Only one source voice; bass, chords and counter-lines are new. Sync synth lead plays the solo-violin line in A (source bars 4-12, octave down) stretched over 20 bars on a 16th grid with anticipations, late downbeats, every third note halved. Development: own motif F-Gb-C-B-Ab-F, 2 notes/bar. B: lead an octave up from A, louder, some notes clipped. Celesta plays single chord tones on 1, a-of-1, and-of-2, and-of-3, e-of-4, chords picked per bar from Fm9, Gbmaj7, Bbm7, C7b9 by melody fit. Synth bass syncopates; a glassy pad holds root and fifth. Kit from bar 5: kick 1, a-of-1, and-of-3, e-of-4, snare 2 and 4, 8th hats. Bridge drops lead, kick and snare. Density ~31 notes/bar in themes, 14 in bridge.
```

## vs-winter2-astra-v2
**Style**
`acoustic bossa nova, 90 BPM, Eb major, 4/4, breathy flute lead, nylon guitar syncopated chords, vibraphone droplets, upright bass, side-stick and shaker, warm indoor calm, instrumental`

**Description**
```
Winter II: 90 BPM, 4/4, Eb major, 64 bars, about 2:51. A variation on the theme of Vivaldi's Four Seasons, Winter II; no vocals. Form: intro 1-8, A 9-24, development 25-32, bridge 33-40, B 41-56, outro 57-64. Only one source voice; bass, chords and counter-lines are new. Flute plays the solo-violin line in A (source bars 1-8, at pitch) stretched over 16 bars on an 8th grid with anticipations, late downbeats, every third note halved. Development: own motif Bb-G-F-Eb-F-G, 2 notes/bar. B: same register as A; louder, every 4th note clipped, chords re-voiced, texture louder. Nylon guitar plays short chords on 1, a-of-1, and-of-2, and-of-3, and-of-4, picked per bar from Ebmaj9, Gm7, Fm9, Bb13 by melody fit. Vibraphone plays offbeat 16ths, octave up; upright bass on 1, and-of-2, 3, and-of-4. Kit from bar 5: soft kick 1 and 3, side-stick and-of-1, and-of-2, and-of-3, a-of-4, shaker 8ths. Bridge drops flute, kick and side-stick. Density ~51 notes/bar in themes, 28 in bridge.
```

## vs-winter3-astra-v2
**Style**
`contemporary minimalist chamber, 5/8 in 3+2, 92 BPM quarter note, F minor, pizzicato solo violin lead, marimba eighth-note pulse, harp sixteenth patterns, cello bass, no drums, glinting icy mood, instrumental`

**Description**
```
Winter III: 92 BPM (quarter note), 5/8 grouped 3+2, F minor, 112 bars, about 3:03. A variation on the theme of Vivaldi's Four Seasons, Winter III; no vocals. Form: intro 1-8, A 9-36, development 37-56, bridge 57-76, B 77-104, outro 105-112. Only one source voice; bass, chords and counter-lines are new. Pizzicato solo violin plays the solo-violin line in A (source bars 1-24 of 3/8, at pitch) re-timed over 28 bars of 5/8 on a 16th grid with anticipations, late downbeats, every third note halved. Development: own motif C-Db-C-Ab-G-F, 2 notes/bar. B: same register as A; louder, every 4th note clipped, chords re-voiced, texture louder. Marimba plays a single chord tone on every 8th, chords picked per bar from Fm6, Dbmaj7, Bbm9, Ebsus by melody fit. Harp plays offbeat 16ths, octave up; cellos on 8ths 1 and 4 (3+2). No drums. Bridge drops the violin and halves the marimba. Density ~17 notes/bar in themes, 10 in bridge.
```
