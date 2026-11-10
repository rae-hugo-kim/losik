# Vivaldi 사계 변주 v2 — opus (anthropic/claude-opus-5-5) Suno 프롬프트

`tools/vivaldi_opus_v2.py` 의 12곡(`sketches/vs-<season><n>-opus-v2.mid`, 바운스 `bounces/vs-<season><n>-opus-v2.wav`)을 Cover 로 올릴 때 쓰는 블록입니다. 장르는 곡마다 다르고(`VIVALDI_BRIEF_V2.md` §3), Style 에는 원곡 제목·작곡가·계절 이름을 넣지 않고 끝을 `instrumental` 로 맺습니다. Description 에만 "variation on the theme of Vivaldi's Four Seasons, <Season> <mvt>" 를 넣습니다. 길이(공백 포함)는 `python3 vivaldi_opus_v2.py` 의 `prompt-length` 줄이 잽니다. 주제 선율 출처: Mutopia Project(CC BY-SA 3.0), 작품은 퍼블릭 도메인입니다.

## vs-spring1-opus-v2
**Style**
`Afro highlife, 134 BPM, E major, bright palm-wine guitar melody, chopped offbeat acoustic guitar, warm tonewheel organ, bouncy bass, punchy horn section stabs, cowbell-like ride bell, joyful sunny dance, instrumental`

**Description**
```
Afro highlife variation on the theme of Vivaldi's Four Seasons, Spring I (Allegro), 134 BPM, E major, 100 bars. The ritornello cell (three repeated notes, a fall, a turn) is sung by a nylon guitar, then answered by the horn section; its rhythm is re-cut with anticipations, dotted pairs and eighth-note skeletons. Harmony is new: E - A - B7 cycles with F#m7 under the melody. Drums: kick on 1, the a of 2 and the and of 3, rim clicks on 2 and 4, straight eighth hats, a highlife bell pattern on the ride bell, tom fills at section ends. Bass walks root-fifth-octave. Acoustic guitar chops the offbeats, organ holds the chords. Structure: 1-8 intro bell and hats, guitar from 5 / 9-16 guitar motif / 17-29 theme on guitar / 30-33 horn stabs / 34-46 theme on horns / 47-56 call and response / 57-64 break / 65-77 theme an octave higher / 78-85 horns again / 86-92 shout chorus / 93-100 outro.
```

## vs-spring2-opus-v2
**Style**
`Bossa nova, 80 BPM, C# minor, soft nylon guitar comping, breathy solo flute melody, warm electric piano answers, gentle string pad, upright bass, brushed rim click pattern, intimate late-afternoon calm, instrumental`

**Description**
```
Bossa nova variation on the theme of Vivaldi's Four Seasons, Spring II (Largo, the sleeping goatherd), 80 BPM, C# minor, 60 bars. The slow 3/4 solo melody is regrouped into 4/4 as 3+3+2 eighths, with anticipations, late entries and quarter-note skeletons, and played by a breathy solo flute; an electric piano takes the second statement an octave lower. Harmony: C#m9 - D#m7b5 - G#7b9 loop, with F#9, Amaj7 and Bmaj7 under the melody. Nylon guitar plays a two-bar bossa comping cell all through; upright bass on root and fifth with anticipations; soft rim-click bossa pattern and quiet eighth hats; string pad holds the chords. Structure: 1-8 intro guitar alone, bass and pad from 5 / 9-17 theme on flute / 18-25 electric piano motif / 26-34 theme on electric piano / 35-42 flute and guitar dialogue / 43-51 theme on flute / 52-60 outro, flute closes.
```

## vs-spring3-opus-v2
**Style**
`Celtic slip jig in 9/8, 174 BPM, D major, lively tin whistle melody, Irish bouzouki drone strumming, Celtic harp arpeggios, upright bass, bodhran-like tom and rim pulse, green hills dance, instrumental`

**Description**
```
Celtic slip jig variation on the theme of Vivaldi's Four Seasons, Spring III (pastoral dance), 174 BPM quarter (dotted quarter 116), D major, 9/8, 116 bars. The 12/8 siciliana is regrouped into 9/8: each original bar becomes two jig bars, the second dotted beat stretched; anticipations, late entries and dotted-beat skeletons re-cut the rhythm. Tin whistle plays the theme, Celtic harp takes the second statement an octave lower. Harmony: D - G - A - A7 with Em and Bm. Bouzouki strums a drone pattern on every dotted beat; bass holds root and fifth; floor tom and rim give a bodhran-like 3x3 pulse. Structure: 1-8 intro bouzouki and bass drone, percussion from 5 / 9-16 harp air / 17-40 theme on whistle / 41-48 harp arpeggio turn / 49-72 theme on harp / 73-84 jig A on whistle / 85-96 theme fragment on whistle / 97-108 jig B / 109-116 outro, whistle ends.
```

## vs-summer1-opus-v2
**Style**
`Trip-hop, 84 BPM, G minor, heavy slow swung breakbeat, deep sub bass, dark lo-fi piano chords, hazy string swells, vibraphone, plaintive oboe lead, sultry heat haze, cinematic melancholy, instrumental`

**Description**
```
Trip-hop variation on the theme of Vivaldi's Four Seasons, Summer I (exhausted by the heat), 84 BPM, G minor, 64 bars. The 3/8 sighing motif is regrouped: two original bars become one 4/4 bar and the first eighth is stretched to a quarter, so every sigh lands lazily late; anticipations, eighth-note skeletons and swung sixteenths re-cut it further. Oboe plays the theme, vibraphone takes the second statement an octave lower. Harmony: Gm9 - Ebmaj7 - D7b9 loop with Cm7 and Bbmaj7. Drums: slow breakbeat, heavy kick and snare on 2 and 4, ghost snares, swung sixteenth hats, half-time haze section. Sub bass holds long roots. Dark piano plays sparse chords throughout; strings swell in intro, haze and coda. Structure: 1-8 intro piano and strings, drums from 5 / 9-12 vibraphone motif / 13-27 theme on oboe / 28-36 haze / 37-51 theme on vibraphone / 52-64 oboe coda and outro.
```

## vs-summer2-opus-v2
**Style**
`Cinematic neo-classical, 63 BPM, G minor, expressive solo violin, grand piano arpeggio ostinato, lush string ensemble, warm cellos, distant timpani thunder rolls, tremolo strings, brooding film score, instrumental`

**Description**
```
Cinematic neo-classical variation on the theme of Vivaldi's Four Seasons, Summer II (Adagio, distant thunder), 63 BPM, G minor, 48 bars. The adagio line is sung by a solo violin with delayed entries, anticipations and quarter-note skeletons; a grand piano takes the second statement. In the rest bar inside each statement, timpani rolls rumble like distant thunder. Harmony: Gm - Eb - Cm - D7 with Gm9 and Am7b5. Piano plays an eighth-note arpeggio ostinato, strings hold the chords, cellos walk root and fifth. Thunder sections: crescending timpani rolls with sixteenth string tremolo. Structure: 1-8 intro piano ostinato, strings and cellos from 5 / 9-16 theme on violin / 17-20 thunder / 21-28 theme on piano / 29-32 violin build / 33-40 theme on violin / 41-44 storm / 45-48 outro, violin ends on a long G.
```

## vs-summer3-opus-v2
**Style**
`Symphonic metal, 180 BPM, G minor, double kick drums, palm-muted rhythm guitar chugs, soaring lead guitar, epic orchestral strings, huge mixed choir, synth lead, dramatic storm, instrumental`

**Description**
```
Symphonic metal variation on the theme of Vivaldi's Four Seasons, Summer III (Presto, the storm), 180 BPM, G minor, 136 bars. The storm motif is regrouped: one 3/4 bar becomes two 4/4 bars with its three beats spread 3+3+2, then re-picked as eighth tremolo, gallops and syncopated figures. Lead guitar plays the theme, a synth lead takes the second half later. Harmony: Gm - Eb - F loop with Cm and D. Drums: eighth double kick, snare on 2 and 4, ride, crash every section, tom fills; half-time breakdown. Rhythm guitar chugs root-fifth eighths, bass doubles roots, strings hold chords, choir in intro, choir section and climax. Structure: 1-8 intro choir and strings / 9-16 riff and guitar motif / 17-56 theme on lead guitar / 57-64 breakdown / 65-72 choir and synth motif / 73-92 theme on synth lead / 93-104 guitar solo motif / 105-128 climax / 129-136 outro choir.
```

## vs-autumn1-opus-v2
**Style**
`Balkan brass in 7/8, 140 BPM, F major, festive trumpet melody, alto sax answers, oom-pah tuba, polka accordion offbeat chords, tapan-like kick and snare, tipsy wedding dance, instrumental`

**Description**
```
Balkan brass variation on the theme of Vivaldi's Four Seasons, Autumn I (peasant dance and the drunkard), 140 BPM quarter, F major, 7/8 (2+2+3), 120 bars. The dance theme is bent into 7/8: each original bar becomes two 7/8 bars whose beats alternate two- and three-eighth groups, so the tune staggers; anticipations, late entries and one-note-per-group skeletons re-cut it. Trumpet plays the theme, alto sax the second statement. Harmony: F - C7 with Bb and A7. Tuba plays root-fifth oom-pah on the 2+2+3 groups, accordion hits the offbeats, kick on each group, snare offbeats. Structure: 1-8 intro tuba and accordion / 9-16 sax kolo motif / 17-40 theme on trumpet / 41-48 accordion break / 49-72 theme on alto sax / 73-84 call and response / 85-96 theme fragment on trumpet / 97-112 shout chorus / 113-120 outro, tuba closes.
```

## vs-autumn2-opus-v2
**Style**
`Cool jazz ballad, 88 BPM, D minor, breathy tenor sax melody, soft vibraphone, sparse rootless piano comping, upright bass two-feel then walking, brushed snare swirl and ride, smoky late-night club, instrumental`

**Description**
```
Cool jazz ballad variation on the theme of Vivaldi's Four Seasons, Autumn II (Adagio molto, the sleeping drinkers), 88 BPM, D minor, 64 bars. The slow chromatic upper line, originally in 3/4, is regrouped into 4/4 and phrased with swing: long notes are anticipated into the previous bar, some entries come late. Tenor sax plays the theme, vibraphone the second statement. Harmony: Dm9 - Em7b5 - A7b13 - Dm9 with D9, Gm9 and E7b9 under the melody. Drums: soft snare swirl on eighths, ride in swing, hi-hat foot on 2 and 4. Upright bass plays two-feel, walking in the middle section. Piano comps rootless voicings. Structure: 1-8 intro piano and bass, drums and vibraphone from 5 / 9-19 theme on tenor sax / 20-27 piano and vibraphone / 28-38 theme on vibraphone / 39-46 sax improvisation motif / 47-57 theme on tenor sax / 58-64 outro, sax ends on D.
```

## vs-autumn3-opus-v2
**Style**
`Spaghetti western, 112 BPM, D minor, galloping nylon guitar strum, heroic trumpet melody, French horn section, sweeping strings, timpani rolls, clip-clop rim and snare gallop, dusty desert showdown, instrumental`

**Description**
```
Spaghetti western variation on the theme of Vivaldi's Four Seasons, Autumn III (the hunt), 112 BPM, D minor, 84 bars. The 3/8 hunting call is stretched into a 4/4 gallop: three eighths become 3+3+2 quarters, then anticipations, late entries and quarter-note skeletons re-cut it. Trumpet plays the theme, the French horn section takes the second statement. Harmony: Dm - Bb - A7 with F. Drums: gallop figure (eighth plus two sixteenths) on rim with snare on 2 and 4, toms in the outro chase. Guitar strums the gallop all through, bass on root and fifth, strings hold chords in intro and later, timpani hits on 1 and 3 with rolls at section turns. Structure: 1-8 intro guitar and timpani / 9-12 drums and bass join / 13-36 theme on trumpet over horn pads / 37-44 horn call / 45-60 theme on horns / 61-68 trumpet duel / 69-76 chase / 77-84 outro, horns hold the last note.
```

## vs-winter1-opus-v2
**Style**
`Dark techno, 128 BPM, F minor, pounding four-on-the-floor kick, offbeat open hats, claps, sixteenth pulse bass, cold wide pad, stab chords, square lead, icy celesta, frozen industrial night, instrumental`

**Description**
```
Dark techno variation on the theme of Vivaldi's Four Seasons, Winter I (frozen trembling), 128 BPM, F minor, 96 bars. The shivering repeated-note figure is played at half time and re-picked into syncopated 3+3+2 stab patterns; the sixteenth pulse bass carries the chattering teeth. Square lead plays the theme, celesta the second statement. Harmony: Fm - Db - C7b9 loop with Ab and Gm7b5. Drums: four-on-the-floor kick, offbeat open hats, claps on 2 and 4, sixteenth closed hats in the theme; snare roll build. Pad holds the chords throughout, chord stabs on syncopated eighths. Structure: 1-8 intro kick, hats and pad / 9-16 pulse bass and stabs / 17-36 theme on square lead / 37-48 breakdown with celesta motif / 49-56 snare roll build / 57-76 theme on celesta / 77-88 peak with lead motif / 89-96 outro, celesta ends.
```

## vs-winter2-opus-v2
**Style**
`Neo-soul, 72 BPM, Eb major, laid-back swung drums, warm Rhodes chords, melodic finger bass, smooth alto sax lead, soft grand piano, pizzicato violin raindrops, cozy fireside warmth, instrumental`

**Description**
```
Neo-soul variation on the theme of Vivaldi's Four Seasons, Winter II (Largo, by the fire), 72 BPM, Eb major, 54 bars. The warm largo melody is played by an alto sax with swung sixteenths, delayed entries, anticipations and eighth-note skeletons; a grand piano takes the second statement. Pizzicato violin plucks fall like rain on the window. Harmony: Abmaj9 - Gm7 - Fm9 - Bb13 loop with Ebmaj9. Drums: laid-back kick, snare on 2 and 4 with ghost notes, swung sixteenth hats. Bass plays melodic root-fifth lines with approach notes. Rhodes comps lush chords throughout. Structure: 1-8 intro Rhodes and pizzicato, drums and bass from 5 / 9-16 theme on alto sax / 17-22 rain interlude with piano motif / 23-30 theme on piano / 31-38 sax motif / 39-46 theme on alto sax / 47-54 outro, pizzicato fades.
```

## vs-winter3-opus-v2
**Style**
`Tango nuevo, 116 BPM, F minor, marcato piano chords, passionate solo violin, bandoneon-like accordion, deep double bass, dramatic strings, 3-3-2 accents, icy tension and sliding legato, instrumental`

**Description**
```
Tango nuevo variation on the theme of Vivaldi's Four Seasons, Winter III (walking on ice), 116 BPM, F minor, 88 bars. The sliding 3/8 sixteenth figure is regrouped into 4/4: six sixteenths land on 3+3+2 tango accents, with quarter-note skeletons, anticipations and late entries. Solo violin plays the theme, accordion (bandoneon role) the second statement an octave lower. Harmony: Fm - C7b9 with Bbm and Gm7b5. Piano plays marcato chords on four beats and 3-3-2 in the variacion and climax; double bass on root and fifth with approach notes; strings sustain and stab. Structure: 1-8 intro piano and bass / 9-12 accordion motif / 13-36 theme on violin / 37-44 variacion, 3-3-2 rhythm on accordion and strings / 45-60 theme on accordion / 61-72 violin motif / 73-80 climax / 81-88 outro, violin holds F.
```
