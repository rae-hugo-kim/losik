# Vivaldi 사계 변주 — astra (openai-codex/gpt-6-astra)

`docs/music/tools/vivaldi_astra.py`가 만드는 12곡의 Suno Cover 프롬프트입니다. 각 곡은 원곡 반주를 쓰지 않고 새로 쓴 반주(드럼·베이스·EP 컴핑·패드)를 깔며, 주제 성부는 한 번에 한 악기만 연주하고 재현부에서 다른 악기로 바뀝니다. 보컬은 없습니다. 화성은 곡마다 고른 팔레트 안에서 `chord_for()`가 마디마다 선율과 반음 충돌이 적은 코드를 고르므로, 고정된 4마디 루프가 그대로 반복되지는 않습니다.

출처: 주제 선율 데이터는 Mutopia Project의 *Le quattro stagioni* 판(`vivaldi_data.py`)에서 가져왔고, 변주 MIDI와 이 프롬프트는 CC BY-SA 3.0을 따릅니다. 표기: Mutopia Project; arrangement: Astra; CC BY-SA 3.0.

박자 변환: 4/4 원곡은 그대로 두고, 3/4는 원곡 한 마디를 4/4 한 마디로 늘리며, 3/8은 원곡 두 마디를 4/4 한 마디로 묶고, 12/8은 원곡 한 마디를 4/4 한 마디로 접어 8분 격자에 얹습니다. 길이는 MIDI 기준(마디×4박÷BPM)이며, 바운스 WAV는 잔향 꼬리만큼 길 수 있습니다. 아래 프롬프트는 Suno 업로드 통과 여부를 주장하지 않습니다(업로드 결과는 아직 기록되지 않았습니다).

길이는 이 파일을 쓴 뒤 일회성 Python 코드로 각 블록의 Style·Description을 `len()`으로 측정했습니다. 모두 Style ≤300자, Description ≤1,000자(공백·줄바꿈 포함)입니다.

| sid | 장르 | BPM | 마디 | 길이 | 원곡 박자 | 주제 창 | Style 문자 수 | Description 문자 수 |
|---|---|---:|---:|---:|---|---|---:|---:|
| vs-spring1-astra | lo-fi hip hop | 84 | 64 | 3:03 | 4/4 | 1–13 | 204 | 898 |
| vs-spring2-astra | lo-fi hip hop | 74 | 56 | 3:02 | 3/4 | 2–10 | 215 | 918 |
| vs-spring3-astra | deep house | 122 | 96 | 3:09 | 12/8 | 1–12 | 229 | 937 |
| vs-summer1-astra | lo-fi hip hop | 88 | 64 | 2:55 | 3/8 | 1–30 | 193 | 922 |
| vs-summer2-astra | lo-fi hip hop | 76 | 56 | 2:57 | 4/4 | 1–8 | 206 | 904 |
| vs-summer3-astra | deep house | 124 | 96 | 3:06 | 3/4 | 1–20 | 214 | 942 |
| vs-autumn1-astra | lo-fi hip hop | 86 | 64 | 2:59 | 4/4 | 1–12 | 204 | 909 |
| vs-autumn2-astra | lo-fi hip hop | 72 | 56 | 3:07 | 3/4 | 4–14 (violin1) | 216 | 924 |
| vs-autumn3-astra | deep house | 116 | 96 | 3:19 | 3/8 | 1–24 | 223 | 943 |
| vs-winter1-astra | deep house | 118 | 96 | 3:15 | 4/4 | 4–12 | 219 | 985 |
| vs-winter2-astra | lo-fi hip hop | 78 | 56 | 2:52 | 4/4 | 1–8 | 190 | 879 |
| vs-winter3-astra | deep house | 120 | 96 | 3:12 | 3/8 | 1–24 | 216 | 960 |

## vs-spring1-astra-v1
**Style**
`lo-fi hip hop, 84 BPM, E major, bright electric piano comping, electric piano lead handing over to nylon guitar, finger bass, sparse acoustic boom bap, swung hats, gentle spring morning mood, instrumental`

**Description**
```
Spring I: 84 BPM, E major, 4/4, 64 bars, about 3:03. A variation on the theme of Vivaldi's Four Seasons, Spring I, over a newly written accompaniment; no vocals. One thematic voice at a time: electric piano plays the solo-violin theme (source already 4/4) in bars 9-24 and its own answer motif G#-F#-B-A# in 25-32; nylon guitar takes the reprise in 41-56. Theme rhythm is rewritten: runs thinned to eighth-note anchors, beats 2 and 4 anticipated, swung offbeats, shortened notes. Chords come from Emaj9, F#m9, Amaj9, B13, picked bar by bar to fit the melody, mostly Emaj9 and Amaj9. Electric piano comps on one and the and-of-three, re-pedalled. Acoustic boom bap from bar 5 with rotating sparse kicks, snare on 2 and 4 plus a ghost; swung hats from bar 3; finger bass from bar 9 follows the kicks. Break 33-40 keys alone; crash at the reprise; outro 57-64 drops the lead, last four bars keys only.
```

## vs-spring2-astra-v1
**Style**
`lo-fi hip hop, 74 BPM, C# minor, slow and sleepy, nylon guitar lead handing over to electric piano, held electric piano chords, finger bass, soft acoustic boom bap, swung hats, warm synth pad interlude, instrumental`

**Description**
```
Spring II: 74 BPM, C# minor, 4/4, 56 bars, about 3:02. A variation on the theme of Vivaldi's Four Seasons, Spring II, with a newly written accompaniment; no vocals. The 3/4 solo-violin line is gently converted to 4/4, each source bar widened into one bar. One thematic voice at a time: nylon guitar plays the sleepy descending theme in bars 9-24; electric piano takes the reprise in 33-44 and its own answer motif G#-E-D#-C# in 45-48. Rhythm rewritten with anticipations, swung offbeats and shortened notes. Chords come from C#m9, Amaj9, F#m9, G#7b9, chosen bar by bar to fit the melody, leaning on G#7b9 and C#m9. Electric piano holds one chord per bar from the and-of-one. Acoustic boom bap from bar 5 with rotating sparse kicks, snare on 2 and 4 plus a ghost; swung hats from bar 3; finger bass from bar 9. Break 25-32 is a warm pad alone; crash at the reprise; outro 49-56 drops the lead, last four bars keys only.
```

## vs-spring3-astra-v1
**Style**
`deep house, 122 BPM, E major, grand piano lead handing over to electric piano, octave-up electric piano stabs, warm synth pad, rolling pulse synth bass, four-on-the-floor, swung open hats, ride lift, airy dance mood, instrumental`

**Description**
```
Spring III: 122 BPM, E major, 4/4, 96 bars, about 3:09. A variation on the theme of Vivaldi's Four Seasons, Spring III, over a newly written accompaniment; no vocals. The 12/8 siciliano is gently folded into 4/4: each source bar becomes one bar on a shuffled eighth grid. One thematic voice at a time: grand piano plays the solo-violin theme in bars 9-32 and its own motif B-D#-C#-G# in 33-48; electric piano takes the reprise in 57-80 and the motif in 81-88. Harmony uses only Emaj9 and Amaj9, chosen bar by bar to fit the melody. Electric piano stabs an octave up on one and the a-of-two; warm pad holds root and fifth. Four-on-the-floor kick from bar 5, snare on 2 and 4, swung closed hats from bar 3 with open hats on the and-of-two and four, ride in the reprise; synth bass one long off-beat note per bar from bar 9; tom fills before sections. Break 49-56 bass and pad only; outro 89-96 drops lead and pad, last four bars keys only.
```

## vs-summer1-astra-v1
**Style**
`lo-fi hip hop, 88 BPM, G minor, languid heat, electric piano lead handing over to grand piano, syncopated electric piano comping, finger bass, sparse acoustic boom bap, swung hats, instrumental`

**Description**
```
Summer I: 88 BPM, G minor, 4/4, 64 bars, about 2:55. A variation on the theme of Vivaldi's Four Seasons, Summer I, with a newly written accompaniment; no vocals. The 3/8 source is gently converted to 4/4 by pairing two short source bars into one bar, so the sighing figures arrive two at a time. One thematic voice at a time: electric piano plays the solo-violin theme in bars 9-24 and its own motif G-A-Bb-D in 25-32; grand piano takes the reprise in 41-56. Rhythm rewritten: runs thinned, at most six notes a bar, anticipations, swung offbeats. Chords come from Gm9, Ebmaj9, Cm9, D7b9, chosen bar by bar to fit the melody, mostly Gm9 and D7b9. Electric piano comps on the a-of-one and the and-of-three. Acoustic boom bap from bar 5 with rotating sparse kicks, snare on 2 and 4 plus a ghost; finger bass from bar 9. Break 33-40 swung hats alone; crash at the reprise; outro 57-64 drops the lead, last four bars keys only.
```

## vs-summer2-astra-v1
**Style**
`lo-fi hip hop, 76 BPM, G minor, heavy still air, grand piano lead handing over to nylon guitar, sparse electric piano chords, finger bass, quiet acoustic boom bap, low ghost snares, swung hats, instrumental`

**Description**
```
Summer II: 76 BPM, G minor, 4/4, 56 bars, about 2:57. A variation on the theme of Vivaldi's Four Seasons, Summer II, over a newly written accompaniment; no vocals. The source is already 4/4, so no meter change. One thematic voice at a time: grand piano plays the long solo-violin line with its rests in bars 9-24; nylon guitar takes the reprise in 33-44 and its own motif D-C-A-Bb in 45-48. Rhythm rewritten with anticipations, swung offbeats and shortened notes. Chords come from Gm9, Cm9, D7b9, Ebmaj9, chosen bar by bar to fit the melody, often landing on Ebmaj9. Electric piano comps on one and four. Instead of thunder, tension comes from a low ghost snare on the a-of-four: acoustic boom bap from bar 5 with rotating sparse kicks and snare on 2 and 4; swung hats from bar 3; finger bass from bar 9. Break 25-32 keys alone; crash at the reprise; outro 49-56 drops the lead, last four bars keys only.
```

## vs-summer3-astra-v1
**Style**
`deep house, 124 BPM, G minor, driving and stormy, square synth lead handing over to electric piano, octave-up electric piano stabs, dark synth pad, pulse synth bass, four-on-the-floor, swung open hats, instrumental`

**Description**
```
Summer III: 124 BPM, G minor, 4/4, 96 bars, about 3:06. A variation on the theme of Vivaldi's Four Seasons, Summer III, with a newly written accompaniment; no vocals. The 3/4 storm is gently converted to 4/4, each source bar widened into one bar, and its repeated notes are thinned to an eighth-note skeleton. One thematic voice at a time: square synth lead plays the solo-violin theme in bars 9-32 and its own motif G-D-C-Bb in 33-48; electric piano cools it down in the reprise 57-80 and the motif in 81-88. Chords come from Gm9, D7b9, Ebmaj9, Cm9, chosen bar by bar to fit the melody. Electric piano stabs an octave up on the and-of-one and the a-of-three; pad holds root and fifth. Four-on-the-floor kick from bar 5, snare on 2 and 4, swung hats from bar 3 with offbeat open hats, ride in the reprise; synth bass one off-beat note per bar from bar 9; tom fills before sections. Break 49-56 pad alone; outro 89-96 last four bars keys only.
```

## vs-autumn1-astra-v1
**Style**
`lo-fi hip hop, 86 BPM, F major, harvest dance groove, nylon guitar lead handing over to grand piano, three-hit electric piano comping, finger bass, offbeat-kick acoustic boom bap, swung hats, instrumental`

**Description**
```
Autumn I: 86 BPM, F major, 4/4, 64 bars, about 2:59. A variation on the theme of Vivaldi's Four Seasons, Autumn I, over a newly written accompaniment; no vocals. The source is already 4/4, so no meter change. One thematic voice at a time: nylon guitar plays the solo-violin dance theme in bars 9-24 and its own motif A-C-D-C in 25-32; grand piano takes the reprise in 41-56. Repeated notes are loosened: runs thinned, at most six notes a bar, anticipations, swung offbeats. Chords come from Fmaj9, Dm9, Bbmaj9, C13, chosen bar by bar to fit the melody, so Bbmaj9 sounds in about half the bars. Electric piano comps on one, the and-of-two and four. Acoustic boom bap from bar 5 with rotating lopsided kicks, snare on 2 and 4 plus a ghost; swung hats from bar 3; finger bass from bar 9 follows the kicks. Break 33-40 finger bass alone; crash at the reprise; outro 57-64 drops the lead, last four bars keys only.
```

## vs-autumn2-astra-v1
**Style**
`lo-fi hip hop, 72 BPM, D minor, drowsy and hushed, electric piano lead handing over to grand piano, sparse electric piano chords, finger bass, very soft acoustic boom bap, swung hats, warm pad interlude, instrumental`

**Description**
```
Autumn II: 72 BPM, D minor, 4/4, 56 bars, about 3:07. A variation on the theme of Vivaldi's Four Seasons, Autumn II, with a newly written accompaniment; no vocals. The theme is the slow first-violin line, gently converted from 3/4 to 4/4 with each source bar widened into one bar; only long tones remain. One thematic voice at a time: electric piano plays it in bars 9-24; grand piano returns for the reprise in 33-44 and its own motif D-A-B-G in 45-48. Notes are shortened and bar starts sometimes delayed. Chords come from Dm9, Gm6, A7b9, Bbmaj9, chosen bar by bar to fit the melody, mostly Gm6 and A7b9. Electric piano comps on the and-of-one and the a-of-three. Acoustic boom bap from bar 5 with rotating sparse kicks, snare on 2 and 4 plus a ghost; swung hats from bar 3; finger bass from bar 9. Break 25-32 is an empty-feeling warm pad alone; crash at the reprise; outro 49-56 drops the lead, last four bars keys only.
```

## vs-autumn3-astra-v1
**Style**
`deep house, 116 BPM, F major, hunting energy held low, classical guitar hook handing over to electric piano, octave-up electric piano stabs, warm synth pad, pulse synth bass, four-on-the-floor, swung open hats, instrumental`

**Description**
```
Autumn III: 116 BPM, F major, 4/4, 96 bars, about 3:19. A variation on the theme of Vivaldi's Four Seasons, Autumn III, over a newly written accompaniment; no vocals. The 3/8 hunt is gently converted to 4/4 by pairing two source bars into one bar, keeping its leaps as a hook. One thematic voice at a time: classical guitar plays the solo-violin theme in bars 9-32 and its own motif F-C-G-A in 33-48; electric piano takes the reprise in 57-80 and the motif in 81-88. Chords come from Fmaj9, Bbmaj9, C13, Am7, chosen bar by bar to fit the melody, mostly swinging between Fmaj9 and Bbmaj9. Electric piano stabs an octave up on one and the e-of-three; pad holds root and fifth. Four-on-the-floor kick from bar 5, snare on 2 and 4, swung hats from bar 3 with offbeat open hats, ride in the reprise; low synth bass one off-beat note per bar from bar 9; tom fills before sections. Break 49-56 hats and pad only; outro 89-96 last four bars keys only.
```

## vs-winter1-astra-v1
**Style**
`deep house, 118 BPM, F minor, cold and shivering, electric piano lead handing over to square synth lead, octave-up electric piano stabs, dark synth pad, pulse synth bass, four-on-the-floor, swung open hats, instrumental`

**Description**
```
Winter I: 118 BPM, F minor, 4/4, 96 bars, about 3:15. A variation on the theme of Vivaldi's Four Seasons, Winter I, with a newly written accompaniment; no vocals. The source is already 4/4; the theme window starts at the trembling solo entry in source bar 4. One thematic voice at a time: electric piano plays the theme in bars 9-32 and its own motif F-Gb-F-C in 33-48; square synth lead answers with the contrasting reprise in 57-80 and the motif in 81-88. Rhythm rewritten: runs thinned to eighth-note anchors, anticipations, swung offbeats. Chords come from Fm9, Dbmaj9, C7b9, Bbm9, chosen bar by bar to fit the melody. Electric piano stabs an octave up on the e-of-one and the and-of-three; pad holds root and fifth. Four-on-the-floor kick from bar 5, snare on 2 and 4, swung hats from bar 3 with offbeat open hats, ride in the reprise; synth bass one off-beat note per bar from bar 9; tom fills before sections. Break 49-56 keys and pad only; outro 89-96 last four bars keys only.
```

## vs-winter2-astra-v1
**Style**
`lo-fi hip hop, 78 BPM, E-flat major, cozy fireside, nylon guitar lead handing over to electric piano, low electric piano chords, finger bass, soft acoustic boom bap, swung hats, instrumental`

**Description**
```
Winter II: 78 BPM, E-flat major, 4/4, 56 bars, about 2:52. A variation on the theme of Vivaldi's Four Seasons, Winter II, over a newly written accompaniment; no vocals. The source is already 4/4, so no meter change. One thematic voice at a time: nylon guitar plays the indoor solo-violin melody in bars 9-24; electric piano takes the reprise in 33-44 and its own motif Bb-G-F-Eb in 45-48. Rhythm rewritten with thinned runs, anticipations, swung offbeats and shortened notes. Chords come from Ebmaj9, Abmaj9, Cm9, Bb13, chosen bar by bar to fit the melody. Electric piano comps on one and three, re-pedalled. Acoustic boom bap from bar 5 with rotating sparse kicks, snare on 2 and 4 plus a ghost; swung hats from bar 3; finger bass from bar 9 follows the kicks. Break 25-32 swung hats alone; crash at the reprise; outro 49-56 drops the lead, and the last four bars are keys only.
```

## vs-winter3-astra-v1
**Style**
`deep house, 120 BPM, F minor, gliding on ice, shuffled grand piano lead handing over to nylon guitar, octave-up electric piano stabs, dark synth pad, pulse synth bass, four-on-the-floor, swung open hats, instrumental`

**Description**
```
Winter III: 120 BPM, F minor, 4/4, 96 bars, about 3:12. A variation on the theme of Vivaldi's Four Seasons, Winter III, with a newly written accompaniment; no vocals. The 3/8 source is gently converted to 4/4 by pairing two source bars into one bar, and its turning figures are thinned into a shuffle. One thematic voice at a time: grand piano plays the solo-violin theme in bars 9-32 and its own motif C-Db-C-Ab in 33-48; nylon guitar closes with the reprise in 57-80 and the motif in 81-88. Chords come from Fm9, Bbm9, Dbmaj9, C7b9, chosen bar by bar to fit the melody, so Bbm9 sounds in over half the bars. Electric piano stabs an octave up on the a-of-one and four; pad holds root and fifth. Four-on-the-floor kick from bar 5, snare on 2 and 4, swung hats from bar 3 with offbeat open hats, ride in the reprise; synth bass one off-beat note per bar from bar 9; tom fills before sections. Break 49-56 bass and pad only; outro 89-96 last four bars keys only.
```
