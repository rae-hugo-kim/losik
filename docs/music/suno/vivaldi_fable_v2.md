# Vivaldi 사계 변주 v2 — fable (anthropic/claude-fable-5-1)

12곡의 Suno Cover 업로드 프롬프트입니다. 작곡기는 `docs/music/tools/vivaldi_fable_v2.py`, 소스 MIDI 는 `sketches/vs-<season><n>-fable-v2.mid` 입니다. 브리프 §4 대로 Description 에 "variation on the theme of Vivaldi's Four Seasons, <Season> <mvt>" 를 넣고 Style 에는 원곡 제목을 넣지 않았습니다. 주제 데이터 출처는 Mutopia Project (CC BY-SA 3.0 전제) 이고 모든 MIDI 에 저작권 메타로 적혀 있습니다.

길이는 `python3 vivaldi_fable_v2.py --prompts` 로 측정합니다(공백·내부 줄바꿈 포함). 모두 Style ≤ 300자, Description ≤ 1,000자입니다.

| key | sid | Style 문자 수 | Description 문자 수 |
|---|---|---:|---:|
| spring 1 | vs-spring1-fable | 158 | 849 |
| spring 2 | vs-spring2-fable | 160 | 896 |
| spring 3 | vs-spring3-fable | 177 | 885 |
| summer 1 | vs-summer1-fable | 154 | 819 |
| summer 2 | vs-summer2-fable | 176 | 870 |
| summer 3 | vs-summer3-fable | 166 | 829 |
| autumn 1 | vs-autumn1-fable | 169 | 811 |
| autumn 2 | vs-autumn2-fable | 160 | 854 |
| autumn 3 | vs-autumn3-fable | 170 | 806 |
| winter 1 | vs-winter1-fable | 149 | 951 |
| winter 2 | vs-winter2-fable | 158 | 846 |
| winter 3 | vs-winter3-fable | 173 | 891 |

## vs-spring1-fable-v2
**Style**
`60s chamber pop, baroque pop, 96 BPM, E major, harpsichord arpeggios, string section, trumpet melody, light drums, finger bass, sunny and bright, instrumental`

**Description**
```
Spring I Fable: instrumental variation on the theme of Vivaldi's Four Seasons, Spring I, as sunny 60s chamber pop. 96 BPM, E major, 72 bars. Four-bar loop E - C#m7 - Amaj7 - B7: harpsichord plays eighth-note arpeggios through the whole song, a string section holds the chords, finger bass walks root, root, fifth, root, and a light kit (kick on one and the and-of-three, snare on two and four, eighth hats, open hat every fourth bar) keeps a 60s backbeat. Intro 1-8 harpsichord and strings, drums and bass from bar 5; A 9-32 a bright trumpet carries the ritornello theme, restates its head, then an own two-bar motif; break 33-40 drums out, harpsichord, strings and bass; A2 41-64 the harpsichord takes the theme an octave up over the full band, then the trumpet motif; outro 65-72 strings leave, drums and bass fade to harpsichord alone. No vocals.
```

## vs-spring2-fable-v2
**Style**
`celtic air, slow 3/4, 84 BPM, C sharp minor, celtic harp arpeggios, tin whistle melody, cellos, soft string pad, nylon guitar, gentle and pastoral, instrumental`

**Description**
```
Spring II Fable: instrumental variation on the theme of Vivaldi's Four Seasons, Spring II (Largo), as a slow Celtic air in 3/4. 84 BPM, C sharp minor, 84 bars; the melody is stretched to double note values, so it floats over the harp at half speed. Eighteen-bar progression in two-bar steps, C#m(add9) - Amaj7 - G#7 - F# - C#m(add9) - Amaj7 - F#m7 - Amaj7 - C#m(add9), written to the stretched melody. Celtic harp plays rolling eighth-note arpeggios in every bar, cellos hold the root, a soft string pad sits under it from bar 5; no drums. Intro 1-8 harp alone, cellos from 3, pad from 5, a short whistle motif from 5; A 9-38 tin whistle sings the Largo melody, then its first twelve bars again; break 39-46 harp and pad only, cellos rest; A2 47-76 nylon guitar takes the melody an octave down, then the whistle motif; outro 77-84 cellos and pad leave, harp alone. No vocals, unhurried, pastoral.
```

## vs-spring3-fable-v2
**Style**
`tarantella, Italian folk dance in 6/8, fast, E major, solo clarinet melody, medieval lute, nylon guitar strumming, tambourine and frame drum, upright bass, festive, instrumental`

**Description**
```
Spring III Fable: instrumental variation on the theme of Vivaldi's Four Seasons, Spring III, as a tarantella. 6/8 at dotted-quarter 112, E major, 168 bars (about three minutes). Four-bar loop E - E - A - B7 (one chord per 6/8 bar): nylon guitar strums a long downbeat then three short strokes, a medieval lute picks six-note arpeggios, upright bass plays root then fifth on the two big beats, tambourine on every eighth with accents on the two beats and a frame drum under them. Intro 1-16 guitar and lute, percussion from 5, bass from 9; A 17-76 solo clarinet plays the siciliana dance theme twice, then an own motif; break 77-92 strumming drops out, lute, bass and percussion carry; A2 93-152 nylon guitar takes the theme an octave down, then the clarinet returns with it, then the motif; outro 153-168 bass and percussion leave, guitar and lute close. No vocals, bright and festive.
```

## vs-summer1-fable-v2
**Style**
`roots reggae, dub, slow one drop, 62 BPM, G minor, melodica melody, organ bubble, offbeat guitar skank, deep finger bass, laid back and hazy, instrumental`

**Description**
```
Summer I Fable: instrumental variation on the theme of Vivaldi's Four Seasons, Summer I, as slow roots reggae. 62 BPM, G minor, 48 bars. Each pair of the original 3/8 bars becomes one 4/4 bar, three eighths then a held note, so the languid tutti leans on the offbeats. Four-bar loop Gm7 - Cm7 - Gm7 - D7: one-drop drums (kick and rim click together on beat three, eighth hats, open hat every fourth bar), finger bass on one, the and-of-three and four, acoustic guitar skank on every offbeat, organ bubble on the a of each beat. Intro 1-8 skank and organ, drums from 3, bass from 5, a short melodica motif from 5; A 9-20 melodica carries the theme; break 21-28 drums and bass only, dub space; A2 29-40 organ restates the theme an octave down; outro 41-48 drums and bass leave, skank and organ fade. No vocals, hazy heat.
```

## vs-summer2-fable-v2
**Style**
`neoclassical ambient, slow 4/4, 56 BPM, G minor, solo violin melody, legato string section, harp arpeggios, timpani rolls like distant thunder, spacious and still, instrumental`

**Description**
```
Summer II Fable: instrumental variation on the theme of Vivaldi's Four Seasons, Summer II (Adagio), as neoclassical ambient. 56 BPM, G minor, 44 bars. The Adagio line is thinned to a quarter-note skeleton. Two-bar chords Gm9 - Ebmaj7 - Cm7 - D9sus held by a legato string section the whole way, harp playing quarter-note arpeggios, and a timpani roll that swells for two bars like distant thunder before the melody enters, before the reprise, and once more at the very end. Intro 1-6 strings, harp from 3, the first roll in 5-6, a short violin motif from 3; A 7-20 solo violin plays the Adagio melody with its long opening note, then its first six bars again; break 21-24 strings only, the second roll in 23-24; A2 25-38 harp takes the melody, then the violin motif; outro 39-44 harp leaves, the last roll in 43-44, strings alone. No drums, no vocals, slow and spacious.
```

## vs-summer3-fable-v2
**Style**
`drum and bass, 174 BPM, G minor, two-step breakbeat, sub bass, saw synth lead melody, square synth, dark poly pad, riser before drops, stormy and urgent, instrumental`

**Description**
```
Summer III Fable: instrumental variation on the theme of Vivaldi's Four Seasons, Summer III (Presto), as drum and bass. 174 BPM, G minor, 128 bars. The storm's sixteenth-note runs are thinned to one note per beat and the 3/4 bars re-barred into 4/4 with the last note held. Four-bar loop Gm - Gm - Eb - F on a dark poly pad; two-step breakbeat (kick on one and the and-of-three, snare on two and four, ghost snares, eighth hats, open hat every fourth bar); sub bass holds the root two beats then pushes on the and-of-three and the fifth below on four. Intro 1-16 pad and a riser, drums and sub drop at 9; A 17-56 saw lead plays the thinned theme twice; break 57-72 drums out, pad, sub and riser; A2 73-112 square lead restates the theme an octave up, then the motif; outro 113-128 pad leaves, drums and sub to the end. No vocals.
```

## vs-autumn1-fable-v2
**Style**
`polka, oompah folk dance in 2/4, 100 BPM, F major, tuba bass, accordion offbeats, trumpet melody, alto sax, snare and bass drum, harvest festival, cheerful, instrumental`

**Description**
```
Autumn I Fable: instrumental variation on the theme of Vivaldi's Four Seasons, Autumn I, as a harvest polka. 2/4 at 100 BPM, F major, 144 bars (about three minutes); each original 4/4 bar becomes two 2/4 bars and the running eighths are thinned to a quarter-note skeleton. Eight-bar loop F - F - C7 - C7 - F - Bb - C7 - F: tuba plays the oom on every downbeat (root and fifth alternating), accordion plays the pah on both offbeat eighths, bass drum on one, snare on two, light hats. Intro 1-16 accordion and tuba, drums from 9, a short trumpet motif from 13; A 17-64 trumpet plays the dance theme twice; break 65-80 accordion out, tuba and drums only; A2 81-128 alto sax takes the theme an octave down, then the trumpet motif; outro 129-144 drums leave, tuba and accordion close. No vocals, cheerful and square.
```

## vs-autumn2-fable-v2
**Style**
`sacred minimalism, slow choral drone in 3/4, 40 BPM, D minor, church choir, pipe organ pedal, english horn melody, distant bells, solemn and still, instrumental`

**Description**
```
Autumn II Fable: instrumental variation on the theme of Vivaldi's Four Seasons, Autumn II (Adagio molto), as a sacred minimal drone. 3/4 at 40 BPM, D minor, 40 bars. The movement is almost all chords, so the first violin's thirteen long notes become the melody. Those notes are halved in length so the line moves at a slow walking pace. A pipe organ holds a D and A pedal the whole way; a church choir moves through a six-bar progression Dm - Bb - Gm - Asus - Dm - D major; soft bells ring the chord root every four bars. Intro 1-4 organ, choir and bells, a short english horn motif; A 5-18 english horn sings the melody twice an octave down, then the motif; break 19-22 organ and bells only; A2 23-36 the choir's upper voice restates the melody, then the horn motif; outro 37-40 choir leaves, organ alone. No drums, no vocals as lyrics, slow and solemn.
```

## vs-autumn3-fable-v2
**Style**
`New Orleans brass band, second line, swung 4/4, 96 BPM, trumpet melody, trombone riffs, alto sax, tuba bass, snare drum second line groove, F major, festive, instrumental`

**Description**
```
Autumn III Fable: instrumental variation on the theme of Vivaldi's Four Seasons, Autumn III (the hunt), as a New Orleans brass band. Swung 4/4 at 96 BPM, F major, 72 bars; each pair of 3/8 bars becomes one 4/4 bar, three eighths then a held note, so the horn calls ride a three-plus-one cell. Four-bar loop F6 - F6 - Bb - C7: tuba on one and three with a pickup on the and-of-four, second-line snare with ghost notes and kick syncopation, ride cymbal eighths, alto sax holding two chords per bar, trombone answering with a three-note riff on odd bars. Intro 1-8 drums, tuba from 3, horns from 5; A 9-32 trumpet plays the hunting theme twice; break 33-40 drums and tuba only; A2 41-64 trombone takes the theme an octave down, then the trumpet motif; outro 65-72 horns leave, drums and tuba close. No vocals.
```

## vs-winter1-fable-v2
**Style**
`tango nuevo, 118 BPM, F minor, staccato piano marcato, accordion like a bandoneon, solo violin melody, upright bass, sharp and dramatic, instrumental`

**Description**
```
Winter I Fable: instrumental variation on the theme of Vivaldi's Four Seasons, Winter I, as tango nuevo. 118 BPM, F minor, 88 bars. The solo entry (bars four to twelve of the original) is the theme, thinned to marcato quarter notes; the opening's shivering repeated notes are echoed by an own motif of repeated sixteenths. Nine-bar progression Fm - Fm - Dbmaj7 - Dbmaj7 - Fm - Fm - Bbm7 - C7 - Fm, one pass per statement: piano stabs the 3-3-2 marcato (one, the and-of-two, four and its offbeat), upright bass on the same cell with root, fifth, root, accordion holding the chord then stabbing the and-of-four. Intro 1-8 piano and bass, accordion from 5, a short violin motif from 5; A 9-40 solo violin plays the theme three times, then the shiver motif; break 41-48 piano and bass only; A2 49-80 accordion restates the theme twice, then the violin motif; outro 81-88 accordion leaves, bass leaves, piano alone. No drums, no vocals, sharp and dramatic.
```

## vs-winter2-fable-v2
**Style**
`bossa nova, 72 BPM, E flat major, nylon guitar comping, brushed drums with rim clicks, upright bass, flute melody, vibraphone, warm and intimate, instrumental`

**Description**
```
Winter II Fable: instrumental variation on the theme of Vivaldi's Four Seasons, Winter II (Largo), as a fireside bossa nova. 72 BPM, E flat major, 56 bars. The Largo melody keeps its contour; its ornaments are thinned to an eighth-note skeleton. Four-bar loop Ebmaj7 - Gm7 - Fm7 - Bb9: nylon guitar comps a syncopated bossa pattern (one, the and-of-two, the and-of-three, four) like raindrops, soft kit with rim-click clave and quiet eighth hats, upright bass on root and fifth, vibraphone adding two top notes per bar. Intro 1-8 guitar alone, drums from 3, bass and vibes from 5, a short flute motif from 5; A 9-24 flute plays the melody twice; break 25-32 vibes and flute out, guitar, bass and drums; A2 33-48 vibraphone takes the melody an octave down, then the flute motif; outro 49-56 band leaves, guitar alone. No vocals, warm and intimate.
```

## vs-winter3-fable-v2
**Style**
`synthwave, 118 BPM, F minor, pulsing octave synth bass, sixteenth-note arpeggio synth, sweeping pad, gated drums, saw lead melody, square lead, icy and driving, instrumental`

**Description**
```
Winter III Fable: instrumental variation on the theme of Vivaldi's Four Seasons, Winter III, as synthwave. 118 BPM, F minor, 88 bars; each pair of the original 3/8 bars becomes one 4/4 bar, three eighths then a held note, and the solo's sixteenth arpeggios are thinned to eighths. Two-chord loop Fm(maj7) - C7: pulsing eighth-note octave synth bass, a sixteenth-note arpeggio synth over the chord tones, a slow sweeping pad, drum machine with kick on one and three, gated snare on two and four, eighth hats, open hat every fourth bar. Intro 1-8 pad and arpeggio, bass and drums from 5, a short lead motif from 5; A 9-40 saw lead plays the theme twice, then an own motif; break 41-48 drums and bass out, pad and arpeggio; A2 49-80 square lead restates the theme and its first eight bars, then the saw motif; outro 81-88 drums and bass leave, arpeggio and pad fade. No vocals, icy and driving.
```
