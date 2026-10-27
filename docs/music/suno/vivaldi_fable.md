# Vivaldi 사계 변주 — fable (anthropic/claude-fable-5-1)

12곡의 Suno Cover 업로드 프롬프트입니다. 작곡기는 `docs/music/tools/vivaldi_fable.py`, 소스 MIDI 는 `sketches/vs-<season><n>-fable-v1.mid` 입니다. 브리프 §4 대로 Description 에 "variation on the theme of Vivaldi's Four Seasons, <Season> <mvt>" 를 넣고 Style 에는 원곡 제목을 넣지 않았습니다(캐논 라운드: Cover Style 이 실제 레버). 출처 표기: 주제 데이터는 Mutopia Project (CC BY-SA 3.0 전제) 판본에서 가져왔습니다.

길이는 `python3 vivaldi_fable.py --prompts` 로 측정합니다(공백·내부 줄바꿈 포함). 모두 Style ≤ 300자, Description ≤ 1,000자입니다.

| key | sid | Style 문자 수 | Description 문자 수 |
|---|---|---:|---:|
| spring 1 | vs-spring1-fable | 187 | 989 |
| spring 2 | vs-spring2-fable | 168 | 990 |
| spring 3 | vs-spring3-fable | 167 | 957 |
| summer 1 | vs-summer1-fable | 182 | 997 |
| summer 2 | vs-summer2-fable | 188 | 973 |
| summer 3 | vs-summer3-fable | 175 | 994 |
| autumn 1 | vs-autumn1-fable | 191 | 1000 |
| autumn 2 | vs-autumn2-fable | 179 | 1000 |
| autumn 3 | vs-autumn3-fable | 167 | 999 |
| winter 1 | vs-winter1-fable | 174 | 997 |
| winter 2 | vs-winter2-fable | 185 | 992 |
| winter 3 | vs-winter3-fable | 185 | 990 |

## vs-spring1-fable-v1
**Style**
`deep house, 122 BPM, E major, half-time electric piano melody, square synth lead reprise, dub chord stabs, sub bass, tough kit four-on-the-floor, offbeat open hats, warm pad, instrumental`

**Description**
```
Spring I Fable: instrumental variation on the theme of Vivaldi's Four Seasons, Spring I. 122 BPM, E major, 96 bars. The ritornello is played in half time (every note doubled) by a mellow electric piano over a four-bar dub loop B9sus - Emaj9 - B9sus - Amaj13: two stabs per bar, re-pedalled, an electric piano arpeggio in eighths through A and A2, and a low 1-5-9 pad from bar one. Sub bass holds the root for most of the bar and adds a short fifth on the and-of-three. Tough kit: four-on-the-floor kick, open hat on every and-of-two and and-of-four, snare plus clap on 2 and 4, eighth closed hats with louder offbeats, tom fills at bars 16, 48 and 88. Intro 1-8 pad and hats, kick from bar 5; A 9-48 full with the EP theme, then an own two-bar motif; break 49-56 hats and pad, bass returns at 53; A2 57-88 crash, ride replaces downbeat hats, square synth lead restates the theme, then the EP motif; outro 89-96 drums, bass and pad, pad leaves at 93. No vocals, DJ-friendly intro and outro.
```

## vs-spring2-fable-v1
**Style**
`lo-fi hip hop, 70 BPM, C sharp minor, grand piano comping, electric piano melody, nylon guitar reprise, soft organ hold, finger bass, dusty swung boom bap, instrumental`

**Description**
```
Spring II Fable: instrumental variation on the theme of Vivaldi's Four Seasons, Spring II (Largo). 70 BPM, C sharp minor, 56 bars, the 3/4 melody re-barred into 4/4 with each bar's last note stretched to beat four. Nine-bar progression C#m9 x2 - G#9 x2 - C#m9 x2 - Amaj9 x2 - G#7#5, grand piano comping on one and the and-of-three, re-pedalled, soft organ on the upper voices. SoCal boom bap: kick on one and the and-of-three, on one and the a-of-two in even bars, snare on 2/4, a ghost on the a-of-four, swung eighth hats with louder offbeats, one open hat every four bars. Finger bass sits on the kick slots: root, then the fifth. Intro 1-8 piano and organ, hats from 3, drums from 5, short EP motif; A 9-24 electric piano carries the Largo melody, a short restatement, then the motif; break 25-32 no drums, piano and organ; A2 33-48 three bars of motif, then nylon guitar plays the theme an octave lower and its head again; outro 49-56 drums and bass leave at 53, piano alone. No vocals.
```

## vs-spring3-fable-v1
**Style**
`shuffle deep house, 124 BPM, E major, triplet-swing saw lead melody, electric piano reprise, held chords, organ layer, epic poly pad, sub bass, tough kit, instrumental`

**Description**
```
Spring III Fable: instrumental variation on the theme of Vivaldi's Four Seasons, Spring III. 124 BPM, E major, 96 bars. The 12/8 siciliana dance is mapped onto a 4/4 shuffle, so the melody rides in triplet eighths against a straight kick. Four-bar loop F#m11 x2 - Amaj13 - B9sus, electric piano holding each chord a full bar with a soft organ layer on the upper voices and a low poly pad from bar one. Sub bass: root on one, a repeat on the and-of-two, the fifth on the and-of-three. Tough kit: four-on-the-floor, open hats on the and-of-two and and-of-four, snare plus clap on 2/4, eighth closed hats with offbeat accents, tom fills at 16, 48 and 88. Intro 1-8 pad and hats, kick from 5; A 9-48 saw synth lead plays the theme twice, then an own motif; break 49-56 keys and pad, bass back at 53; A2 57-88 crash and ride, electric piano restates the theme an octave down, then the saw-lead motif; outro 89-96 drums, bass and pad, pad leaves at 93. No vocals.
```

## vs-summer1-fable-v1
**Style**
`lo-fi hip hop, 88 BPM, G minor, nylon guitar melody, grand piano reprise, electric piano comping, soft organ, finger bass, lazy swung boom bap with sixteenth hat flicks, instrumental`

**Description**
```
Summer I Fable: instrumental variation on the theme of Vivaldi's Four Seasons, Summer I. 88 BPM, G minor, 64 bars. Each pair of languid 3/8 bars becomes one 4/4 bar, three eighths then a held note: a three-plus-one cell, lazy bounce. Four-bar loop Gm9 - D7b9 - Ebmaj9 - Cm9, electric piano comping in three short pushes per bar, re-pedalled, soft organ on the top voices. SoCal boom bap: kick on one, the and-of-two and the a-of-three, on one and the and-of-three in even bars, snare on 2/4, two ghosts on even bars (the late one yields to the open hat), swung eighth hats with a sixteenth flick after two and four, open hat every four bars. Finger bass sits on the kick slots: root, root, then the fifth. Intro 1-8 keys and organ, hats from 3, drums from 5, short nylon motif; A 9-28 nylon guitar carries the theme, then the motif; break 29-36 kick out, the rest stays; A2 37-56 crash, grand piano restates the theme, then the motif; outro 57-64 drums and bass leave at 61, keys alone. No vocals.
```

## vs-summer2-fable-v1
**Style**
`lo-fi hip hop, 70 BPM, G minor, grand piano melody, electric piano reprise an octave down, EP chords, nylon guitar arpeggio, finger bass with octave pops, slow swung boom bap, instrumental`

**Description**
```
Summer II Fable: instrumental variation on the theme of Vivaldi's Four Seasons, Summer II (Adagio). 70 BPM, G minor, 56 bars. Four-bar loop Gm9 - Cm11 - Ebmaj9 - D7#5, electric piano holding two beats on one and re-hitting on the and-of-three, re-pedalled, nylon guitar picking chord tones in swung eighths in A and A2. SoCal boom bap: kick on one and the a-of-three, plus the and-of-two in even bars, snare on 2/4, a ghost on the a-of-two, swung eighth hats with louder offbeats, one open hat every four bars. Finger bass sits on the kick slots: root, then an octave pop (the fifth where the octave leaves its range). Intro 1-8 EP and guitar, hats from 3, drums from 5, short piano motif; A 9-24 grand piano plays the Adagio melody with its long opening note twice; break 25-32 drums and bass only; A2 33-48 crash, electric piano restates the theme an octave lower, then its head and the motif; outro 49-56 drums and bass leave at 53, keys alone. No vocals, warm and hazy.
```

## vs-summer3-fable-v1
**Style**
`deep house, 124 BPM, G minor, skeletal electric piano melody, square synth lead reprise an octave up, dub chord stabs, EP arpeggio, warm pad, sub bass, tough kit, instrumental`

**Description**
```
Summer III Fable: instrumental variation on the theme of Vivaldi's Four Seasons, Summer III (Presto). 124 BPM, G minor, 96 bars. The storm's sixteenth runs are thinned to one note per beat and the 3/4 bars re-barred into 4/4 with the last note held through beat four. Four-bar loop Gm11 x2 - Ebmaj13 - D9sus: dub stabs on the and-of-one and and-of-three, re-pedalled, an EP arpeggio in eighths through A and A2, a low 1-5-9 pad from bar one. Sub bass: root on one, two short pushes on the and-of-three and and-of-four. Tough kit: four-on-the-floor, open hats on the and-of-two and and-of-four, snare plus clap on 2/4, offbeat-accented closed hats, tom fills at 16, 48, 88. Intro 1-8 pad and hats, kick from 5; A 9-48 electric piano plays the thinned theme twice, then an own motif; break 49-56 kick, hats, keys, pad, arpeggio back at 53; A2 57-88 crash and ride, square synth lead restates the theme an octave up, then the EP motif; outro 89-96 drums, bass and pad, pad leaves at 93. No vocals.
```

## vs-autumn1-fable-v1
**Style**
`lo-fi hip hop, 84 BPM, F major, electric piano melody, nylon guitar reprise an octave down, grand piano comping, nylon arpeggio, pulse synth bass, swung boom bap with hat flicks, instrumental`

**Description**
```
Autumn I Fable: instrumental variation on the theme of Vivaldi's Four Seasons, Autumn I. 84 BPM, F major, 64 bars, the dance ritornello slowed thirty percent to swung boom bap. Loop Fmaj9 - Dm9 - Gm9 - C13: grand piano comping on one, the and-of-two, three and the and-of-four, re-pedalled, nylon guitar picking chord tones in swung eighths in A and A2. SoCal boom bap: kick on one, the and-of-two and the and-of-three (a-of-two in even bars), snare on 2/4, ghosts on the a-of-one and and-of-four in even bars (the late one yields to the open hat), swung eighth hats with a sixteenth flick after two and four, open hat every four bars. Pulse bass sits on the kick slots: root, root, fifth, one fewer in even bars. Intro 1-8 piano and guitar, hats from 3, drums from 5, short EP motif; A 9-28 EP carries the theme, a restatement, then the motif; break 29-36 no drums, keys and guitar; A2 37-56 crash, nylon guitar plays the theme an octave down, then the motif; outro 57-64 band out at 61, keys alone.
```

## vs-autumn2-fable-v1
**Style**
`lo-fi hip hop, 72 BPM, D minor, nylon guitar long-note melody, electric piano reprise, EP chord holds, soft organ, finger bass, sparse boom bap with rim on even bars, instrumental`

**Description**
```
Autumn II Fable: instrumental variation on the theme of Vivaldi's Four Seasons, Autumn II (Adagio). 72 BPM, D minor, 56 bars. The movement is almost all chords, so the first violin's thirteen long notes become the melody, re-barred from 3/4 into 4/4, phrase ends stretched. Eleven-bar progression written to those notes: Dm9 x2 - Gm9 x2 - Fmaj9 - Bb13 - Dm9 - D7b9 - Gm9 - A9sus - Dmaj9, electric piano holds each chord three beats, re-pedalled, organ under. Sparse SoCal boom bap: kick on one and the and-of-three (a-of-three in even bars), snare on odd bars, rim on even bars, ghost on the a-of-four, swung eighth hats, open hat every four bars. Finger bass on the kick slots: root, then fifth. Intro 1-8 EP and organ, hats from 3, drums from 5, short nylon motif; A 9-24 nylon guitar plays the melody an octave down, then the motif; break 25-32 kick out, hats, rim, keys, bass stay; A2 33-48 crash, EP restates the melody and its first five bars; outro 49-56 band out at 53, keys alone. No vocals.
```

## vs-autumn3-fable-v1
**Style**
`deep house, 122 BPM, F major, square synth lead melody, electric piano reprise, two chord stabs per bar, organ long chords, warm pad, sub bass, tough kit, instrumental`

**Description**
```
Autumn III Fable: instrumental variation on the theme of Vivaldi's Four Seasons, Autumn III (the hunt). 122 BPM, F major, 96 bars. Each pair of 3/8 bars becomes one 4/4 bar, three eighths then a held note: the horn calls ride a three-plus-one cell over a straight kick. Four-bar loop F6/9 x2 - Bbmaj9 - C9sus, electric piano playing two stabs per bar, re-pedalled, soft organ holding the upper voices in A and A2, a low 1-5-9 pad from bar one. Sub bass: root for two beats, a push on the and-of-three, the fifth on the and-of-four. Tough kit: four-on-the-floor, open hats on the and-of-two and and-of-four, snare plus clap on 2/4, offbeat-accented closed hats, tom fills at 16, 48, 88. Intro 1-8 pad and hats, kick from 5; A 9-48 square synth lead plays the hunting theme twice, then an own motif; break 49-56 hats and pad, bass returns at 53; A2 57-88 crash and ride, electric piano restates the theme twice, then the square-lead motif; outro 89-96 drums, bass and pad, pad leaves at 93. No vocals.
```

## vs-winter1-fable-v1
**Style**
`deep house, 118 BPM, F minor, electric piano melody, saw synth lead reprise, dub chord stabs, organ arpeggio, warm pad, long sub bass, tough kit, dark and chill, instrumental`

**Description**
```
Winter I Fable: instrumental variation on the theme of Vivaldi's Four Seasons, Winter I. 118 BPM, F minor, 96 bars. The solo entry (bars four to twelve of the original) is the theme; the opening's shivering repeated-note chords are echoed by an own motif of repeated sixteenths on the electric piano. Two-chord loop Fm11 x2 - Dbmaj9 x2: dub stabs on the and-of-one and and-of-three, re-pedalled, an organ arpeggio in eighths in A and A2, a low 1-5-9 pad from bar one. Sub bass holds the root three beats and adds the fifth on the and-of-four. Tough kit: four-on-the-floor, open hats on the and-of-two and and-of-four, snare plus clap on 2/4, offbeat-accented closed hats, tom fills at 16, 48, 88. Intro 1-8 pad and hats, kick from 5; A 9-48 electric piano plays the theme three times, then the shiver motif; break 49-56 keys and pad, bass back at 53; A2 57-88 crash and ride, saw synth lead restates the theme twice, then the EP motif; outro 89-96 drums, bass and pad, pad leaves at 93. No vocals.
```

## vs-winter2-fable-v1
**Style**
`lo-fi hip hop, 68 BPM, E flat major, electric piano melody, grand piano reprise an octave down, grand piano comping, nylon guitar picking, finger bass, slow swung boom bap, instrumental`

**Description**
```
Winter II Fable: instrumental variation on the theme of Vivaldi's Four Seasons, Winter II (Largo). 68 BPM, E flat major, 56 bars. The Largo melody keeps its contour; its ornaments are thinned to an eighth-note skeleton and swung. Four-bar loop Ebmaj9 - Cm9 - Abmaj9 - Bb13, grand piano comping on one, three and four, re-pedalled, nylon guitar picking chord tones in swung eighths instead of the pizzicato in A and A2. SoCal boom bap: kick on one and the a-of-two, on one, the and-of-two and the a-of-three in even bars, snare on 2/4, a ghost on the and-of-four (not on open-hat bars), swung eighth hats with a sixteenth flick after two and four, open hat every four bars. Finger bass on the kick slots: root, then fifth. Intro 1-8 piano and guitar, hats from 3, drums from 5, short EP motif; A 9-24 EP plays the Largo twice; break 25-32 drums and bass only; A2 33-48 crash, grand piano restates the melody an octave down, then the motif; outro 49-56 band leaves at 53, keys alone. No vocals.
```

## vs-winter3-fable-v1
**Style**
`deep house, 124 BPM, F minor, saw synth lead melody, electric piano reprise an octave down, static minor-major chords, EP arpeggio, epic poly pad, long sub bass, tough kit, instrumental`

**Description**
```
Winter III Fable: instrumental variation on the theme of Vivaldi's Four Seasons, Winter III. 124 BPM, F minor, 96 bars. The solo's sixteenth arpeggios are thinned to eighths and each pair of 3/8 bars becomes one 4/4 bar, three eighths then a held note. The cello F pedal becomes a six-bar near-static loop FmM9 x2 - Fm9 - Dbmaj9 - FmM9 x2, electric piano holding each chord a full bar, re-pedalled, an EP arpeggio in eighths in A and A2, a low poly pad from bar one. Sub bass holds the root almost the whole bar. Tough kit: four-on-the-floor, open hats on the and-of-two and and-of-four, snare plus clap on 2/4, offbeat-accented closed hats, tom fills at 16, 48, 88. Intro 1-8 pad and hats, kick from 5; A 9-48 saw synth lead plays the theme twice, then an own motif; break 49-56 hats and pad, bass returns at 53; A2 57-88 crash and ride, electric piano restates the theme an octave down, then at pitch, then the saw-lead motif; outro 89-96 drums, bass and pad, pad leaves at 93. No vocals.
```
