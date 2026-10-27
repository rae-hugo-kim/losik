# Lo-fi hip hop set — opus

각 Description은 공백과 내부 줄바꿈을 포함해 `lh_opus.py`의 `check_prompts()`가 길이를 측정합니다. MIDI의 리드는 A 마지막 8마디와 A2 전체에서 연주하며, 슬롯 3·15·21·27은 나일론 또는 상성부 EP가 1마디부터 혼자 열고 키는 5마디에 들어옵니다. 슬롯 30은 셋의 클로저로, 아웃트로에서 드럼 → 베이스 순으로 빠지고 키만 남아 마지막 마디를 Gm9 한 화음으로 닫습니다.

`docs/music/tools`에서 `python3 -B lh_opus.py`를 실행해 아래 길이를 확인했습니다. 모두 Style ≤300자·Description ≤1,000자를 통과했고 Style 은 `instrumental` 로 끝납니다.

| 슬롯 | sid | Style 문자 수 | Description 문자 수 |
|---|---|---:|---:|
| 3 | lh03-chalk-awning | 199 | 988 |
| 6 | lh06-iron-teacup | 210 | 992 |
| 9 | lh09-signal-orchard | 182 | 906 |
| 12 | lh12-ember-switchyard | 196 | 988 |
| 15 | lh15-quartz-overpass | 194 | 974 |
| 18 | lh18-lantern-deck | 213 | 977 |
| 21 | lh21-ink-carousel | 217 | 937 |
| 24 | lh24-felt-almanac | 214 | 932 |
| 27 | lh27-moth-library | 216 | 920 |
| 30 | lh30-last-streetlamp | 214 | 967 |

## lh03-chalk-awning-v1
**Style**
`lo-fi hip hop, 78 BPM, F major, nylon guitar picking intro, warm electric piano ninths with sustain, finger bass, lazy acoustic boom bap, ghost snares, swung hats, soft grand piano lead, instrumental`

**Description**
```
Chalk Awning: 78 BPM, F major, 56 bars. Loop Fmaj9-Am7-Bbmaj9-C13sus, I-iii-IV-V13sus; electric piano holds bar one, answers on the and-of-two and beat four in bar two, hits one plus the e-of-three in bar three, pushes the and-of-one in bar four, re-pedalled every bar. Lazy SoCal boom bap: kick on one plus the and-of-three, then the a-of-two, the a-of-three, and the and-of-two with the and-of-three in bar four; snare on 2/4 with ghosts, swung eighth hats, one open hat per four bars. Finger bass follows the kick but skips its last hit, adding a chromatic approach back into Fmaj9 in bar four. Nylon picks chord tones. Grand piano lead: G-A-C / E-C / D-C-A-F / G-F, climbing to E then walking down; A2 alternates a breath in bar one and an early bar three. Intro nylon alone, hats at 3, EP/kick/snare at 5, bass at 9; break 25-32 drums out, bass, EP and nylon trio; crash at 33; outro drops lead and nylon, last 4 bars drums and keys. no vocals, lo-fi warmth, DJ-friendly intro/outro.
```

## lh06-iron-teacup-v1
**Style**
`lo-fi hip hop, 80 BPM, A minor, descending aeolian loop, pedalled jazz grand piano, nylon guitar picking, finger bass, relaxed acoustic boom bap, ghost snares, swung hats, soft electric piano lead, instrumental`

**Description**
```
Iron Teacup: 80 BPM, A minor, 64 bars. Loop Am9-G13-Fmaj9-Em7, descending i-VII-VI-v; grand piano hits one plus a late and-of-four push in odd bars, the and-of-one plus beat three in bar two, beat two plus the and-of-three in bar four, re-pedalled every bar. SoCal boom bap: kick on one with the a-of-two and and-of-three in bar one, the a-of-three in bar two, the and-of-two and a-of-three in bar three, the and-of-three in bar four; snare on 2/4 with ghosts, swung eighth hats, one open hat per four bars. Finger bass skips the last kick hit, dropping to the low fifth in bar one and adding the fifth in bar three. Nylon picks between chords. Electric piano lead: E-D-B / D-B-A / C-A-G / G-B, a falling three-note cell stepped down with the chords, answered upward. Intro piano first, hats at 3, kick/snare at 5, bass and nylon at 9; break 29-36 bass alone, nylon joins at 31, snare and hats at 33; crash at 37; outro 57-64 drums and piano. no vocals, lo-fi warmth, DJ-friendly intro/outro.
```

## lh09-signal-orchard-v1
**Style**
`lo-fi hip hop, 84 BPM, D major, soft electric piano comping, tonewheel organ holds, finger bass, head-nod acoustic boom bap, ghost snares, swung hats, nylon guitar lead, instrumental`

**Description**
```
Signal Orchard: 84 BPM, D major, 64 bars, building toward the peak. Loop Dmaj9-A13sus-Bm9-Gmaj9, I-V13sus-vi-IV; electric piano comps on one, the and-of-two and the and-of-three in odd bars, one late touch in bar two, one plus beat four in bar four, re-pedalled every bar, over a soft organ hold. SoCal boom bap: kick on one plus the and-of-two and and-of-three, then the a-of-three, the a-of-two with the and-of-three, then the and-of-two; snare on 2/4 with ghosts, swung eighth hats, one quiet sixteenth hat after beat four, one open hat per four bars. Finger bass follows the kick minus its last hit. Nylon guitar lead: F#-A-B-A / F#-E / B-D-C# / A-F#, a pentatonic turn and a sigh, then the turn lifted to B. Intro EP first, hats at 3, kick/snare at 5, bass and organ at 9; break 29-36 snare, hats and organ only; crash at 37; outro 57-64 drums and EP. no vocals, lo-fi warmth, DJ-friendly intro/outro.
```

## lh12-ember-switchyard-v1
**Style**
`lo-fi hip hop, 86 BPM, F# minor dorian, warm jazz grand piano stabs, high electric piano picking, deep synth bass, full acoustic boom bap, ghost snares, swung hats, nylon guitar lead, instrumental`

**Description**
```
Ember Switchyard: 86 BPM, F# minor dorian, 64 bars, the peak. Loop F#m9-Amaj9-E6/9-B9, i-III-VII-IV9; grand piano hits one, the a-of-one and the and-of-three in odd bars, the and-of-two plus beat four in bar two, the and-of-one, beat three and the and-of-four in bar four, re-pedalled every bar. Full SoCal boom bap: kick on one with two syncopations every bar (a-of-two/a-of-three, and-of-two/and-of-three, and-of-three/a-of-three, a-of-two/and-of-three); snare on 2/4 with two ghosts, swung eighth hats, one sixteenth hat after beat four, one open hat per four bars. Deep synth bass follows the kick minus its last hit. A high electric piano picks chord tones. Nylon lead: A-C#-E / E-C#-B / G#-B-C# / C#-A-F#, a triad climbing from the and-of-one, folding back down. Intro piano first, hats at 3, kick/snare at 5, bass at 9; break 29-36 piano and bass, hats at 31, kick at 33, snare back at 37; crash at 37; outro 57-64 drums and piano. no vocals, lo-fi warmth, DJ-friendly intro/outro.
```

## lh15-quartz-overpass-v1
**Style**
`lo-fi hip hop, 88 BPM, C# minor, nylon guitar picking intro, electric piano ninths with sustain, deep synth bass, full acoustic boom bap, ghost snares, swung hats, grand piano lead, instrumental`

**Description**
```
Quartz Overpass: 88 BPM, C# minor, 64 bars, peak of the set. Loop C#m9-F#9-Amaj9-G#7b13, i-IV9-VI-V; electric piano on one, beat three and the and-of-four in odd bars, the a-of-one plus the and-of-three in bar two, the and-of-two plus the e-of-three in bar four, re-pedalled every bar. Full SoCal boom bap: kick on one with two syncopations every bar (and-of-two/a-of-three, and-of-three/a-of-three, a-of-two/a-of-three, and-of-two/and-of-three); snare on 2/4 with two ghosts, swung eighth hats, one sixteenth hat after beat four, one open hat per four bars. Deep synth bass follows the kick minus its last hit. Nylon guitar picks busy chord tones. Grand piano lead: G#-B-G#-E / A#-G# / B-C#-B-G# / B#-G#, a neighbour-tone turn repeated a step higher, closed by the leading tone. Intro nylon alone, hats at 3, EP/kick/snare at 5, bass at 9; break 29-36 drums, bass and nylon, keys out; crash at 37; outro 57-64 drums and EP. no vocals, lo-fi warmth, DJ-friendly intro/outro.
```

## lh18-lantern-deck-v1
**Style**
`lo-fi hip hop, 84 BPM, B major, drifting, pedalled jazz grand piano, borrowed minor iv, soft tonewheel organ swells, finger bass, easy acoustic boom bap, ghost snares, swung hats, electric piano lead, instrumental`

**Description**
```
Lantern Deck: 84 BPM, B major, 64 bars, the drift begins. Loop Bmaj9-G#m9-Emaj9-Em9, I-vi-IV-iv with a borrowed minor iv; grand piano on one plus the and-of-three in odd bars, beat two in bar two, one plus the e-of-two in bar four, re-pedalled every bar, with a soft organ swell under each chord. Easy SoCal boom bap: kick on one plus the a-of-three, then the and-of-two with the and-of-three, the and-of-three, and the a-of-two with the a-of-three; snare on 2/4 with one or two ghosts, swung eighth hats, one open hat per four bars. Finger bass follows the kick minus its last hit, approaching the loop's return chromatically from below. Electric piano lead: C#-A#-F# / G#-A#-B / D#-B / D-B-G, a fall and a climb, then the D#-B shape darkened to D-B-G over the minor iv. Intro piano first, hats at 3, kick/snare at 5, bass and organ at 9; break 29-36 piano and hats, kick added at 33; crash at 37; outro 57-64 drums and piano. no vocals, lo-fi warmth, DJ-friendly intro/outro.
```

## lh21-ink-carousel-v1
**Style**
`lo-fi hip hop, 82 BPM, E-flat minor, falling-fourths loop, held jazz grand piano chords, high electric piano picking, finger bass, laid-back acoustic boom bap, ghost snares, swung hats, nylon guitar lead, instrumental`

**Description**
```
Ink Carousel: 82 BPM, Eb minor, 64 bars. Loop Ebm9-Db6/9-Gbmaj9-Cbmaj9, i-VII-III-VI falling in fourths; grand piano holds bars one and three, plays the and-of-one plus beat four in bar two and the and-of-one plus beat three in bar four, re-pedalled every bar. Laid-back SoCal boom bap: kick on one plus the and-of-two and and-of-three, then the a-of-two, the a-of-three, and the and-of-two with the a-of-three; snare on 2/4 with one or two ghosts, swung eighth hats, one open hat per four bars. Finger bass follows the kick minus its last hit. A high electric piano picks sparse chord tones. Nylon guitar lead: Bb-Bb-Db / Bb-Ab-F / F-F-Ab / Bb-Gb, a repeated-note pickup answered by a short fall, then the same pickup a fourth lower. Intro high EP alone, hats at 3, piano/kick/snare at 5, bass at 9; break 29-36 high EP alone, bass joins at 33; crash at 37; outro 57-64 drums and piano. no vocals, lo-fi warmth, DJ-friendly intro/outro.
```

## lh24-felt-almanac-v1
**Style**
`lo-fi hip hop, 78 BPM, A-flat major, cooling down, mellow electric piano ninths with sustain, nylon guitar picking, finger bass, sparse acoustic boom bap, one ghost snare, swung hats, grand piano lead, instrumental`

**Description**
```
Felt Almanac: 78 BPM, Ab major, 56 bars, the cool-down begins. Loop Abmaj9-Fm9-Cm7-Dbmaj9, I-vi-iii-IV; electric piano on one plus the and-of-two in bar one, a whole-bar hold in bar two, a single late hit on the and-of-three in bar three, one plus beat three in bar four, re-pedalled every bar. Sparse SoCal boom bap: kick on one plus the a-of-two, the and-of-three, the and-of-two with the a-of-three, then the a-of-three; snare on 2/4 with a single ghost, swung eighth hats, one open hat per four bars. Finger bass follows the kick minus its last hit. Nylon guitar picks two notes a bar. Grand piano lead, two notes at most: C-Bb / Ab / G-Bb / C-Ab, a sigh, a long Ab, a lift and a settle. Intro EP first, hats at 3, kick/snare at 5, bass and nylon at 9; break 25-32 kick and snare out, hats, bass, EP and nylon stay; crash at 33; outro drops lead and nylon, last 4 bars EP alone. no vocals, lo-fi warmth, DJ-friendly intro/outro.
```

## lh27-moth-library-v1
**Style**
`lo-fi hip hop, 76 BPM, C minor, late-night cool-down, nylon guitar intro, pedalled grand piano, low soft pad, finger bass, sparse acoustic boom bap, rimshot on even bars, swung hats, electric piano lead, instrumental`

**Description**
```
Moth Library: 76 BPM, C minor, 56 bars, late-night cool-down. Loop Cm9-Ebmaj9-Abmaj9-Fm9, i-III-VI-iv; grand piano holds bars one and three, plays one plus the and-of-three in bar two and a single beat-two hit in bar four, re-pedalled every bar, with a low root-and-fifth pad from bar 9. Sparse SoCal boom bap: kick on one plus the and-of-three in bars one and two, the a-of-two in bar three, the a-of-three in bar four; snare on 2 and 4 turning to rimshot in even bars, one ghost, swung eighth hats, one open hat per four bars. Finger bass follows the kick minus its last hit. Electric piano lead: D-Bb / G / C-Eb / C-Ab, falling from the ninth, a lone G, then a lift and a settle. Intro nylon alone, hats at 3, piano/kick/snare at 5, bass and pad at 9; break 25-32 pad and bass, nylon joins at 29; crash at 33; outro drops lead, nylon and pad, last 4 bars piano alone. no vocals, lo-fi warmth, DJ-friendly intro/outro.
```

## lh30-last-streetlamp-v1
**Style**
`lo-fi hip hop, 72 BPM, G minor, set closer, mellow electric piano with sustain, nylon guitar picking, low soft pad, finger bass, sparse acoustic boom bap, one ghost snare, swung hats, grand piano lead, instrumental`

**Description**
```
Last Streetlamp: 72 BPM, G minor, 56 bars, the closer of the set. Loop Gm9-Ebmaj9-Am7b5-D7b9, i-VI-ii-V; electric piano holds bar one, enters late on the and-of-one in bar two, plays one plus beat four in bar three, holds bar four, re-pedalled every bar, with a low root-and-fifth pad, flat fifth under Am7b5. Sparse SoCal boom bap: kick on one plus the a-of-three, the and-of-two, the a-of-three, the and-of-three; snare on 2/4 with a single ghost, swung eighth hats, one open hat per four bars. Finger bass follows the kick minus its last hit. Nylon picks single tones. Grand piano lead: A-Bb-D / G-Bb / C-A / F#-A, rising from the ninth, an echo, and the leading tone turning home. Intro EP first, hats at 3, kick/snare at 5, bass, nylon and pad at 9; break 25-32 EP, bass and pad, no drums; crash at 33; outro 49-56 lets go in order: lead, nylon and pad leave, drums stop after bar 50, bass after bar 52, EP alone, last bar one held Gm9. no vocals, lo-fi warmth, DJ-friendly intro/outro.
```
