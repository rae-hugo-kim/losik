# Suno 투입 프롬프트 (2026-09-05 최신판 기준)

각 곡: **Style** = Suno 스타일 필드(짧게, 장르·무드·악기·템포), **Description** = 커스텀 모드 설명/가사란에 넣는 확장 프롬프트.
오디오 업로드(Extend/Cover) 시 해당 WAV 와 함께 사용한다. 모두 instrumental.

## star-cruiser-v6
**Style**
`synthwave disco, 122 BPM, B minor, driving four-on-the-floor, acoustic drum kit, finger bass, polysynth chord stabs with pushed anticipations, octave-jump lead riff, swinging synth solo, interstellar cruise, instrumental`

**Description**
```
Instrumental synthwave with a disco pulse at 122 BPM in B minor (Bm7–Em7–A7–Dmaj7 verses, Em7–A7–Dmaj7–Bm7 chorus).
Punchy acoustic-style drum kit sits in front; the bass is light and clean, never dominant.
Wide polysynth chords play a syncopated "bam— bop ba-ba" rhythm, pushing the next chord in early on the and-of-four.
Octave-jumping lead riff in the chorus; a loose, swinging synth solo section between verses.
Crash-roll risers into every section. Feel: a starship cruising between stars — glossy, propulsive, no distortion.
```

## ghost-signal-v4
**Style**
`dark synthwave thriller, 100 BPM, G minor, half-time drums, muted clavinet chords, hypnotic dotted-eighth arpeggio, semitone ostinato lead, sub bass in the final third, cymbal crash breakdown, eerie, instrumental`

**Description**
```
Instrumental horror/thriller synthwave at 100 BPM in G minor with a Phrygian pull (Gm–A♭maj7–Gm–D7).
Half-time drums with a dark ride pattern; a muted clavinet plays tense, restrained chord stabs.
Hypnotic dotted-eighth synth arpeggio and a lead built on a D–E♭ semitone ostinato.
Around the two-minute mark the tension breaks: a huge cymbal crash, one bar of silence, then the final verse returns
with a heavy, chest-pressing sub bass under the groove. Two final choruses, then a short fade.
Mood: unsettling but controlled — sinister, not loud. About 3 minutes.
```

## chrome-sunset — 세 편성 중 선택 후 하나만 사용
공통 Description
```
Instrumental city-pop / soft evening groove at 104 BPM in C major (Cmaj7–Am7–Dm7–G7 verses, Fmaj7–G7–Em7–Am7 chorus).
Warm brushed drums with ride cymbal, finger bass on root notes, gentle electric-piano melody with a sixth-leap hook.
Feel: a pleasant walk at golden hour — soft, warm, slightly bouncy, relaxed. Nothing aggressive, nothing dreamy or washed out.
```
**v4 Style**: `city pop, 104 BPM, C major, brushed drums, finger bass, steel-string acoustic guitar with palm-muted strums in the verse and open long strums in the chorus, electric piano melody, warm evening, instrumental`

**v5 Style**: `bossa-tinged city pop, 104 BPM, C major, brushed drums, finger bass, nylon-string acoustic guitar with syncopated sixteenth strums and fast chord changes, electric piano melody, warm and lightly bouncy, instrumental`

**v6 Style**: `soft city pop, 104 BPM, C major, brushed drums, finger bass, tonewheel organ long chords low in the mix, electric piano melody, warm evening glow, instrumental`

## golden-hour-v3
**Style**
`warm pop ballad groove, 94 BPM, C major, live band feel, acoustic drums with ride, finger bass, piano comping with sustain, string ensemble, polysynth hook, risers and cymbal impacts at section changes, uplifting, instrumental`

**Description**
```
Instrumental band-style pop at 94 BPM in C major over a four-chord loop (Fmaj7–G7–Dm7–Em7).
Acoustic drums with swung hi-hats in the verses and ride in the choruses; warm finger bass with walking approach notes.
Piano comping with sustain pedal carries the harmony; a string ensemble fills the space; a polysynth plays the chorus hook.
Every section change is marked by a crash-roll riser and an impact.
Late bridge drops to kick pulse and half-time bass, then explodes back into a final chorus with an octave-layered hook.
Feel: golden-hour glow, hopeful and full. About 3.5 minutes.
```

## 사용 메모
- **길이 제한(MUST)**: Suno 입력 필드는 **공백 포함 1,000자**까지만 받는다. Style 은 300자 이내, Description 은 1,000자 이내로 쓴다. 작성 후 `len()` 으로 재야 한다(2026-10-21 — v3 블록 30개가 1,300~1,700자로 넘쳐 전부 재작성).
- Suno 는 스타일 필드가 짧을수록 안정적. Description 은 커스텀 모드의 가사란에 `[Instrumental]` 태그와 함께 넣거나, Cover/Extend 시 참고용.
- 코드 진행·BPM·키는 원곡 SMF 와 동일. Suno 가 키를 무시하는 경우가 많으므로 무드·악기 단어를 우선.

## dusty-tape-house-v1
**Style**
`lo-fi house, 120 BPM, A minor, dusty drum machine four-on-the-floor, swung sixteenth hi-hats, muffled electric piano off-beat stabs, lazy off-beat synth bass, warm tape feel, instrumental`

**Description**
```
Instrumental lo-fi house at 120 BPM in A minor, a two-chord loop (Am9–Dm9, two bars each).
Soft four-on-the-floor kick, snare with a quiet clap layer on 2 and 4, swung sixteenth closed hats with one open hat per bar.
Muffled, low-velocity electric piano stabs on the off-beats; the bass plays off-beat eighths slightly behind the beat.
Bars 9-12 drop the kick for a breakdown, then a crash brings the full loop back. Feel: dusty cassette, warm, unhurried.
```

## faded-organ-house-v1
**Style**
`lo-fi deep house, 122 BPM, F minor, sparse eighth hi-hats, tonewheel organ long chords, glistening pad, held dotted bass, loose humanized groove, hazy, instrumental`

**Description**
```
Instrumental lo-fi house at 122 BPM in F minor over Fm7–D♭maj7–B♭m7–C7.
Four-on-the-floor kick with a loose, widely humanized feel; only eighth-note hats (half the usual density).
A tonewheel organ holds long chords every bar, a soft pad doubles root and fifth underneath.
The bass holds dotted notes in a 3+3+2 pattern, sitting slightly late.
Bars 9-12 drop the hats, then a crash returns the full loop. Feel: faded, hazy, late-night warmth.
```

## rainy-window-beat-v1
**Style**
`lo-fi hip hop, 80 BPM, F major, boom bap drums with ghost notes, swung hi-hats, jazzy electric piano ninth chords with sustain, finger bass following the kick, rainy, instrumental`

**Description**
```
Instrumental lo-fi hip hop at 80 BPM in F major over a ii–V–I–vi loop (Gm9–C9–Fmaj9–Dm9).
Boom-bap acoustic kit: kick on one and the and-of-three, snare backbeat on 2 and 4 with quiet ghost snares, heavily swung eighth hats.
Electric piano plays rolled rootless ninth chords with the sustain pedal re-pressed every bar, plus a softer re-hit on the and-of-three.
Finger bass locks to the kick pattern. Bars 9-12 drop the kick, a snare fill and crash bring the beat back.
Feel: rain on a window, nodding, cozy.
```

## slow-room-piano-v1
**Style**
`lo-fi hip hop, 74 BPM, E-flat major, half-time drums, rimshot backbeat, swung hi-hats, grand piano seventh chords with sustain pedal, sparse held bass, slow and intimate, instrumental`

**Description**
```
Instrumental half-time lo-fi hip hop at 74 BPM in E♭ major over A♭maj7–Gm7–Fm9–B♭13.
Only one backbeat per bar on beat three, alternating snare and rimshot; soft swung eighth hats.
Grand piano plays rolled two-hand voicings with the sustain pedal re-pressed every bar, adding a small top-note re-hit on even bars.
The bass just holds the root for two beats. Bars 9-12 drop the hats, then a crash returns the full groove.
Feel: a quiet room late at night, slow, intimate, spacious.
```

## warehouse-jack-v1
**Style**
`classic Chicago house, 124 BPM, A minor, drum machine four-on-the-floor, shuffled sixteenth hi-hats, off-beat bass, tonewheel organ chord stabs, two-chord vamp, raw and jacking, instrumental`

**Description**
```
Instrumental classic Chicago house at 124 BPM in A minor, a two-chord vamp (Am7–D9) repeated like a hypnotic loop.
Drum machine four-on-the-floor kick, snare with a clap layered underneath on 2 and 4, open hats on every off-beat, lightly shuffled closed sixteenths.
The bass plays only on the off-beats, bouncing against the kick, with an octave pickup at the end of each bar.
Tonewheel organ stabs on the off-beats, pushing into the next chord every two bars.
Bars 9-12 drop the kick and bass for a floating breakdown; a snare ramp and crash bring the full groove back.
Feel: warehouse party, raw, minimal, jacking. No lead, no vocals.
```

## mirrorball-rise-v1
**Style**
`disco house, 126 BPM, D major, live disco drum kit, open hats on the off-beat, octave-jumping finger bass, bright electric piano off-beat stabs, four-chord loop, uplifting, instrumental`

**Description**
```
Instrumental disco-flavored house at 126 BPM in D major over a four-chord loop (Dmaj7–Bm7–Gmaj7–A add9).
Acoustic-style disco kit: four-on-the-floor kick, snare on 2 and 4, open hats on every off-beat and sixteenth ticks.
Finger bass in continuous eighth-note octaves, root on the beat and octave on the off-beat.
Bright electric piano stabs on every off-beat eighth, keeping the energy lifted and bouncy.
Bars 9-12 drop the hats for a heavier breakdown, then a snare ramp and crash return to the full loop.
Feel: mirrorball, sunlit dance floor, glossy and happy. No lead, no vocals.
```

## velvet-hour-v1
**Style**
`warm deep house, 120 BPM, F minor, soft drum machine, sixteenth closed hi-hats, long sub bass, held jazzy ninth chords on electric piano, warm analog pad, late-night, instrumental`

**Description**
```
Instrumental deep house at 120 BPM in F minor (Fm9–Bbm9–Dbmaj9–C7b9).
Soft four-on-the-floor kick, gentle snare and clap on 2 and 4, sixteenth closed hats with accents on the off-beats, one open hat per bar.
Long, warm sub bass in dotted, held notes — barely moving.
Electric piano holds lush ninth chords with sustain pedal for the whole bar, lightly re-touched on the and-of-four; a warm pad underneath.
Bars 9-12 drop the kick so the chords and pad float, then a crash brings the groove back.
Feel: velvet, late night, warm and spacious. No lead, no vocals.
```

## low-tide-shuffle-v1
**Style**
`groovy deep house, 118 BPM, G minor, drum machine with rimshot backbeat, accented sixteenth hi-hats, walking finger bass with octave jumps, soft electric piano ninth-chord stabs, no pad, instrumental`

**Description**
```
Instrumental deep house at 118 BPM in G minor (Gm9–C9–Fmaj9–Ebmaj9).
Steady kick, rimshot and soft snare on 2 and 4, sixteenth hi-hats with an accent on every off-beat sixteenth pattern, an open hat every two bars.
Finger bass walks: root, octave lift, fifth, and a step-wise approach into the next chord.
Electric piano plays soft, short ninth-chord stabs on a syncopated rhythm (1, the e-of-two, and the and-of-four anticipating the next chord). No pad.
Bars 9-12 drop the hats so kick and bass carry the groove, then a crash returns to the full loop.
Feel: low tide at dusk, understated, rolling, groovy. No lead, no vocals.
```

## citrus-root-grid-v1
**Style**
```
Instrumental bright house, 124 BPM, E major, drum machine, four-on-the-floor, off-beat open hats, root-only eighth-note pulse bass, short grand piano chord stabs, no vocals, no lead.
```

**Description**
```
A 16-bar drums-bass-chords learning loop over E–F#m–A–B, one chord per bar.
Use a steady quarter-note kick, snare on beats 2 and 4 with a quieter clap directly underneath, and open hats on every off-beat.
The bass repeats only each chord's root in eight short eighth notes per bar.
Bright grand piano chord stabs land at beat 1 + three sixteenths, beat 3 + one sixteenth, and the and-of-four.
Bars 1–8 play the full loop; bars 9–12 remove all hats; bar 13 beat 1 adds a crash as the full loop returns through bar 16.
This is the control for Citrus Fifth Grid: preserve all parts except the specified bass pitch changes in that companion. No melody or extra instruments.
```

## citrus-fifth-grid-v1
**Style**
```
Instrumental bright house, 124 BPM, E major, drum machine, four-on-the-floor, off-beat open hats, root-and-fifth eighth-note pulse bass, short grand piano chord stabs, no vocals, no lead.
```

**Description**
```
A 16-bar drums-bass-chords learning loop over E–F#m–A–B, one chord per bar.
Keep Citrus Root Grid's kick, snare with quiet layered clap on 2 and 4, open off-beat hats, and short syncopated grand piano chords.
Play eight bass eighth notes per bar, but raise only the fourth and eighth bass attacks from the root to the fifth above it.
Keep the bass timing, note lengths and accents unchanged, so pitch contour is the only comparison variable.
Bars 9–12 remove all hats; the full loop returns with a crash on bar 13 beat 1 and ends within bar 16.
No melody, lead, vocals, pads or additional instrumentation.
```

## indigo-held-room-v1
**Style**
```
Instrumental deep house, 120 BPM, B minor, soft four-on-the-floor kick, accented closed sixteenth hats, long low pulse bass, warm sustained electric piano ninth chords, no pad, no lead.
```

**Description**
```
A 16-bar drums-bass-chords loop over Bm9–Gmaj9–Em9–F#m7, one chord per bar.
Use softer kick velocities, a restrained snare with a quieter clap layer on 2 and 4, and closed sixteenth hats accented on the off-beat eighths.
Hold one low bass root nearly a full bar. Electric piano also holds one chord nearly a full bar, re-pedaling at each new chord.
Bars 9–12 remove the bass only, keeping the kick, hats and chords; bar 13 beat 1 restores bass with a crash.
Compare with Indigo Soft Steps by changing only the electric piano chord attack rhythm and duration. No melody, vocals or extra layers.
```

## indigo-soft-steps-v1
**Style**
```
Instrumental deep house, 120 BPM, B minor, soft four-on-the-floor kick, accented closed sixteenth hats, long low pulse bass, softly stabbed electric piano ninth chords, no pad, no lead.
```

**Description**
```
A 16-bar drums-bass-chords loop over Bm9–Gmaj9–Em9–F#m7, one chord per bar.
Keep Indigo Held Room's exact soft kick, layered snare/clap backbeat, accented sixteenth closed hats and nearly bar-long bass roots.
Replace only the held electric piano chords with two soft chord stabs per bar, on the and-of-one and the and-of-three.
Use the same chord voicings and comparable touch; release the sustain pedal after each short chord.
Bars 9–12 remove the bass only; a crash on bar 13 beat 1 restores the full loop through bar 16.
The contrast is sustained harmony versus gently pulsing harmony, not a change of bass line or drum density. No melody or vocals.
```

## paper-lantern-eight-v1
**Style**
```
Instrumental lo-fi house, 121 BPM, C minor, loose four-on-the-floor, eight swung closed hats per bar, low soft electric piano stabs, slightly late pulse bass, dusty understated feel, no lead.
```

**Description**
```
A 16-bar drums-bass-chords loop over Cm9–Abmaj9–Fm9–Bb9, one chord per bar.
Use a soft four-on-the-floor kick and snare on 2 and 4 with a quiet clap underneath.
Play eight closed eighth-note hats per bar, delaying alternate hats by 22 ticks at 480 PPQ, with up to 10 ticks of humanized timing.
Low-register, low-velocity electric piano stabs land at beat 1 + three sixteenths and the and-of-three.
The bass holds root notes beginning on the and-of-one and and-of-three, sitting 6–10 ticks late.
Bars 9–12 remove only the kick; a crash on bar 13 beat 1 restores the full groove. End within bar 16.
Compare with Paper Lantern Five by hat density alone. No melody, pads or vocals; do not add effects as a substitute for the groove.
```

## paper-lantern-five-v1
**Style**
```
Instrumental lo-fi house, 121 BPM, C minor, loose four-on-the-floor, five sparse swung closed hats per bar, low soft electric piano stabs, slightly late pulse bass, airy dusty pocket, no lead.
```

**Description**
```
A 16-bar drums-bass-chords loop over Cm9–Abmaj9–Fm9–Bb9, one chord per bar.
Preserve Paper Lantern Eight's drums, low electric piano voicings and stabs, and slightly late held bass notes.
Change only the hat density: retain the first, second, fourth, fifth and eighth attacks from the eight-eighth-note hat grid.
Keep each retained hat's original velocity, 22-tick alternate swing and humanized timing; do not redistribute the five hats evenly.
Bars 9–12 remove only the kick, then restore it with a crash on bar 13 beat 1 for the final four bars.
The extra rests are the experiment. No new fill, melody, pad, vocal or additional instrument.
```

## porch-pocket-anchor-v1
**Style**
```
Instrumental lo-fi hip hop, 82 BPM, E-flat major, sparse boom-bap acoustic drums, snare ghost notes, swung eighth hats, finger bass locked to kick, sustained jazzy electric piano, no lead.
```

**Description**
```
A 16-bar drums-bass-chords loop over Ebmaj9–Cm9–Abmaj9–Bb9, one chord per bar.
Keep snare backbeats on beats 2 and 4 with soft ghosts on the last sixteenth of beats 2 and 4, no clap.
Play three kick attacks per bar on beat 1, beat 3 and the and-of-three; finger bass hits the chord root at exactly those kick onsets.
Use eight closed hats per bar with a modest 22-tick alternate delay at 480 PPQ and up to 10 ticks of humanized timing.
Electric piano holds a warm chord each bar with sustain-pedal release and re-pedaling between voicings.
Bars 9–12 remove all hats; a crash on bar 13 beat 1 restores the original loop through bar 16.
This is the anchored control for Porch Pocket Skip. No lead, melody, vocals or extra layers.
```

## porch-pocket-skip-v1
**Style**
```
Instrumental lo-fi hip hop, 82 BPM, E-flat major, syncopated boom-bap kick and finger bass, steady 2-and-4 snare, ghost notes, swung eighth hats, sustained jazzy electric piano, no lead.
```

**Description**
```
A 16-bar drums-bass-chords loop over Ebmaj9–Cm9–Abmaj9–Bb9, one chord per bar.
Keep Porch Pocket Anchor's electric piano voicings and sustain, snare on 2 and 4, ghost notes, and swung hats unchanged.
Move only the three linked kick-and-bass attacks to beat 1, the final sixteenth of beat 1, and the final sixteenth of beat 3.
The number of kick and bass notes stays the same; bass remains root-only and follows each kick exactly.
Bars 9–12 remove all hats; restore the full loop with a crash on bar 13 beat 1, ending within bar 16.
Compare the syncopated pocket against the anchored one without switching to half-time or adding new material. No vocals or melody.
```

## copper-tram-minor-v1
**Style**
```
Instrumental house, 124 BPM, G minor, four-on-the-floor electronic drums, clap layered under snare on 2 and 4, offbeat open hats, octave-leaping eighth-note synth bass, bright short grand piano stabs, no lead, no vocals.
```

**Description**
```
A 16-bar drums-bass-chords loop over Gm7–Cm7–Ebmaj7–F7, one chord per bar.
Kick on every beat, snare with a clap underneath on 2 and 4, closed hat on the beats and an open hat on every offbeat.
Pulse synth bass plays eight eighths per bar: root, root, octave, root, fifth, root, octave, root.
Bright four-note grand piano stabs land on the and-of-1, and-of-2 and beat 4 in odd bars, and on all four offbeats in even bars.
Bars 9–12 remove the piano stabs so only drums and bass run; a crash on bar 13 beat 1 brings the stabs back through bar 16.
Minor-key member of a parallel-mode pair with Copper Tram Major. No melody, no vocals, no extra layers.
```

## copper-tram-major-v1
**Style**
```
Instrumental house, 124 BPM, G major, four-on-the-floor electronic drums, clap layered under snare on 2 and 4, offbeat open hats, octave-leaping eighth-note synth bass, bright short grand piano stabs, no lead, no vocals.
```

**Description**
```
A 16-bar drums-bass-chords loop over Gmaj7–Cmaj7–Em7–D7, one chord per bar.
Every drum hit, the eighth-note bass cell and the stab rhythm are identical to Copper Tram Minor; only the chord qualities and the E and D roots change.
Kick on every beat, snare plus clap on 2 and 4, open hats on the offbeats, root-octave-fifth synth bass in eighths.
Bright grand piano stabs on the offbeats, three per odd bar and four per even bar.
Bars 9–12 drop the stabs; a crash on bar 13 beat 1 restores the full loop through bar 16.
Major-key member of a parallel-mode pair. No melody, no vocals, no extra layers.
```

## harbor-fog-minor-v1
**Style**
```
Instrumental deep house, 120 BPM, D minor, soft kick, accented sixteenth closed hats, long warm sub bass, rootless electric piano ninth chords with sustain pedal, thin root-and-fifth synth pad, no lead, no vocals.
```

**Description**
```
A 16-bar loop over Dm9–Gm9–Bbmaj9–A7(b9), one chord per bar.
Soft kick on every beat, light snare with a quieter clap underneath on 2 and 4, closed hats on every sixteenth with the offbeat eighths accented and an open hat on the last eighth of even bars.
Sub bass holds the root from beat 1 for almost two beats, repeats it on the and-of-2, then drops to the fifth below on the and-of-4 (root on every fourth bar).
Rootless electric piano ninths are held for two beats then softly re-touched on the and-of-2, with sustain pedal re-pedalled every bar; a quiet root-and-fifth pad sustains under each bar.
Bars 9–12 remove kick, snare and clap so only hats, bass, EP and pad remain; a crash on bar 13 beat 1 brings the drums back through bar 16.
Minor-key member of a parallel-mode pair with Harbor Fog Major. No melody, no vocals.
```

## harbor-fog-major-v1
**Style**
```
Instrumental deep house, 120 BPM, D major, soft kick, accented sixteenth closed hats, long warm sub bass, rootless electric piano ninth chords with sustain pedal, thin root-and-fifth synth pad, no lead, no vocals.
```

**Description**
```
A 16-bar loop over Dmaj9–Gmaj9–Bm9–A9, one chord per bar.
Drums, sub bass cell, electric piano rhythm, pedalling and pad rhythm are identical to Harbor Fog Minor; only the chord qualities and the B root change.
Soft four-on-the-floor kick, light snare and clap on 2 and 4, accented sixteenth hats, long sub bass with a fifth-below pickup on the and-of-4.
Electric piano ninths held two beats then re-touched softly, root-and-fifth pad under each bar.
Bars 9–12 drop kick, snare and clap; a crash on bar 13 beat 1 restores the full loop through bar 16.
Major-key member of a parallel-mode pair. No melody, no vocals.
```

## attic-radio-minor-v1
**Style**
```
Instrumental lo-fi house, 121 BPM, A minor, loose four-on-the-floor electronic drums, sparse swung closed hats, lagging synth bass, low muffled electric piano shell chords on the offbeats, no lead, no vocals.
```

**Description**
```
A 16-bar loop over Am9–Fmaj9–Dm9–E7(b9), one chord per bar.
Kick on every beat at moderate velocity, snare with a clap underneath on 2 and 4, and only five closed hats per bar (and-of-1, and-of-2, beat 3, and-of-3, and-of-4) with a 22-tick swing on the offbeats; an open hat replaces the and-of-2 hat every fourth bar.
All timing is humanized up to 10 ticks at 480 PPQ.
Synth bass plays root on beats 1, and-of-2 and 3 and the octave on the and-of-4, sitting about 9 ticks behind the grid.
Low rootless electric piano shells are stabbed quietly on the swung and-of-1, and-of-2 and and-of-4.
Bars 9–12 remove the bass; a crash on bar 13 beat 1 brings it back through bar 16.
Minor-key member of a parallel-mode pair with Attic Radio Major. No melody, no vocals.
```

## attic-radio-major-v1
**Style**
```
Instrumental lo-fi house, 121 BPM, A major, loose four-on-the-floor electronic drums, sparse swung closed hats, lagging synth bass, low muffled electric piano shell chords on the offbeats, no lead, no vocals.
```

**Description**
```
A 16-bar loop over Amaj9–F#m9–Dmaj9–E9, one chord per bar.
Drums, bass lag and rhythm, stab rhythm and humanization are identical to Attic Radio Minor; only the chord qualities and the F# root change.
Five swung closed hats per bar over a moderate four-on-the-floor kick, snare plus clap on 2 and 4.
Synth bass about 9 ticks behind the beat, low rootless electric piano shells stabbed quietly on swung offbeats.
Bars 9–12 drop the bass; a crash on bar 13 beat 1 restores the full loop through bar 16.
Major-key member of a parallel-mode pair. No melody, no vocals.
```

## late-bus-minor-v1
**Style**
```
Instrumental lo-fi hip hop, 80 BPM, C minor, sparse boom-bap acoustic drums, snare ghost notes, swung eighth hats, finger bass locked to the kick, pedalled jazzy grand piano ninths, no lead, no vocals.
```

**Description**
```
A 16-bar loop over Cm9–Abmaj9–Fm9–G7(b9), one chord per bar.
Odd bars: kick on beat 1, the last sixteenth of beat 2 and the and-of-3; even bars: kick on beat 1, the and-of-3 and the last sixteenth of beat 4.
Snare on 2 and 4 with two quiet ghost notes per bar, eight closed hats with a 22-tick swing on the offbeats and an open hat on the last eighth of every fourth bar.
Finger bass hits exactly where the kick hits, root first, with a fifth-below and a fifth-above passing tone.
Rootless grand piano ninths are held for most of each bar with a slight upward roll, re-hit softly on the and-of-2 in even bars, sustain pedal re-pedalled every bar.
Bars 9–12 remove all drums so piano and bass play alone; two snare sixteenths at the end of bar 12 and a crash on bar 13 beat 1 bring the drums back through bar 16.
Minor-key member of a parallel-mode pair with Late Bus Major. No melody, no vocals.
```

## late-bus-major-v1
**Style**
```
Instrumental lo-fi hip hop, 80 BPM, C major, sparse boom-bap acoustic drums, snare ghost notes, swung eighth hats, finger bass locked to the kick, pedalled jazzy grand piano ninths, no lead, no vocals.
```

**Description**
```
A 16-bar loop over Cmaj9–Am9–Fmaj9–G9, one chord per bar.
Drums, kick-locked finger bass cell, piano rhythm and pedalling are identical to Late Bus Minor; only the chord qualities and the A root change.
Boom-bap kick with two ghost snares per bar, backbeat on 2 and 4, swung eighth hats.
Rootless grand piano ninths held per bar with a soft and-of-2 re-hit in even bars and sustain pedal re-pedalled every bar.
Bars 9–12 drop all drums; a snare pickup at the end of bar 12 and a crash on bar 13 beat 1 restore the full loop through bar 16.
Major-key member of a parallel-mode pair. No melody, no vocals.
```

---

# 2026-10-12 장르 뼈대 라운드 — 쌍 단위 프롬프트 (3모델 × 4장르 = 12)

위의 곡별 `*-v1` 블록은 각 곡 하나를 Cover 할 때 쓰고, 아래는 **쌍 하나를 한 프롬프트**로 묶어 그 모델이 던진 질문이 결과에 남도록 쓴 것입니다. 쌍의 두 WAV 를 각각 Cover 하되 Style·Description 은 동일하게 쓰고, 끝의 `Variant` 한 줄만 바꿉니다. Suno 는 키를 자주 무시하므로 무드·악기 단어를 앞에 두고, 바뀌는 축은 Description 마지막 두 줄에 명시했습니다. 전부 instrumental.

## 모델별 설계 의도 (프롬프트에 반영된 것)

| 모델 | 쌍에서 바꾼 것 | 프롬프트에 남긴 방식 |
|---|---|---|
| Claude-opus | 여러 요소 동시 — 장르 안의 두 얼굴 | 두 곡의 성격을 대비 단어로 각각 서술 |
| gpt-6-astra | 한 축만 — 통제 실험 | "everything else identical, only X differs" 를 명시 |
| claude-fable | 조성만(단조↔병행 장조) — 화성 기여도 측정 | 리듬 섹션 동일을 못 박고 minor/major 한 줄만 교체 |

---

## Claude-opus 세트

### house — warehouse-jack / mirrorball-rise
**Style**
`house, 124–126 BPM, four-on-the-floor, drum machine kit, synth bass, organ and electric piano stabs, bright, club, instrumental`

**Description**
```
Instrumental 16-bar house skeleton: four-on-the-floor kick, clap under the snare on 2 and 4, open hats on the off-beats.
Drums, bass and chords only — no lead, no vocals. Bars 9–12 strip a layer, a crash on bar 13 brings the full loop back.
Two contrasting faces of house:
Variant A (Warehouse Jack, A minor, Am7–D9 two-chord loop): Chicago jack — bass only on the off-beats so it bounces against the kick, sparse tonewheel organ stabs leaving space, hypnotic repetition. Break drops kick and bass.
Variant B (Mirrorball Rise, D major, Dmaj7–Bm7–Gmaj7–A(add9)): disco-house — octave-jumping eighth-note finger bass that runs, electric piano stabbing every off-beat, four-chord cycle with lift. Break drops the hats.
```

### deep house — velvet-hour / low-tide-shuffle
**Style**
`deep house, 118–120 BPM, soft kick, closed sixteenth hats, warm sub bass, jazzy ninth chords on electric piano, late night, instrumental`

**Description**
```
Instrumental 16-bar deep house skeleton: softened four-on-the-floor, closed sixteenth hats with light accents, rim-shot backbeat, no lead, no vocals.
Bars 9–12 thin out, crash on bar 13 restores the loop.
Two ways to be "deep":
Variant A (Velvet Hour, F minor, Fm9–B♭m9–D♭maj9–C7♭9): space is the subject — electric piano ninths held with sustain, a soft pad on root and fifth underneath, dotted sub bass that barely moves. Break drops the kick and leaves the pad floating.
Variant B (Low Tide Shuffle, G minor, Gm9–C9–Fmaj9–E♭maj9): groove is the subject — no pad, short soft electric piano stabs on 1, the a-of-1 and the and-of-3, walking finger bass with octave lifts and approach notes, accented back-sixteenth hats. Break drops the hats.
```

### lo-fi house — dusty-tape-house / faded-organ-house
**Style**
`lo-fi house, 120–122 BPM, dusty, swung hats, muffled electric piano, tape warmth, hazy, instrumental`

**Description**
```
Instrumental 16-bar lo-fi house skeleton: four-on-the-floor on a soft drum machine, loose timing, no lead, no vocals.
Bars 9–12 strip a layer, crash on bar 13.
Two kinds of looseness:
Variant A (Dusty Tape House, A minor, Am9–Dm9): bouncy — swung sixteenth hats, off-beat synth bass that lands slightly late behind the kick, muffled electric piano ninth stabs on the off-beats. Break drops the kick.
Variant B (Faded Organ House, F minor, Fm7–D♭maj7–B♭m7–C7): flowing — hats halved to eighths, tonewheel organ long chords with a glistening pad on root and fifth, bass holding a dotted 3+3+2 figure, wider human timing. Break drops the hats.
```

### lo-fi hip hop — rainy-window-beat / slow-room-piano
**Style**
`lo-fi hip hop, 74–80 BPM, boom bap, swung hats, ghost snares, jazzy keys with sustain, rainy, sparse, instrumental`

**Description**
```
Instrumental 16-bar lo-fi hip hop skeleton over acoustic-style drums, finger bass and keys — no melody, no vocals.
Bars 9–12 drop a layer, crash on bar 13.
Two tempos of nodding:
Variant A (Rainy Window Beat, 80 BPM, F major, Gm9–C9–Fmaj9–Dm9): backbeat on 2 and 4 with ghost snares, heavily swung hats, finger bass following the kick, electric piano ninths re-pedalled every bar. Break drops the kick, bass holds the root.
Variant B (Slow Room Piano, 74 BPM, E♭ major, A♭maj7–Gm7–Fm9–B♭13): half-time — snare only on 3, rim instead of snare on even bars, bass holding roots for two beats, grand piano chords with sustain. Break drops the hats.
```

---

## gpt-6-astra 세트 (한 축 통제 실험)

### house — citrus-root-grid / citrus-fifth-grid
**Style**
`house, 124 BPM, four-on-the-floor, bright grand piano stabs, root-note eighth bass, off-beat open hats, sunny, instrumental`

**Description**
```
Instrumental 16-bar house skeleton in E major over E–F♯m–A–B, one chord per bar.
Four-on-the-floor drum machine, clap under snare on 2 and 4, closed hats on the beat, open hats on the off-beats, bright short grand piano stabs, straight eighth-note bass. Bars 9–12 drop the hats; crash on bar 13.
Controlled pair — everything is identical except the bass contour:
Variant A (Citrus Root Grid): bass repeats the root on every eighth.
Variant B (Citrus Fifth Grid): the 4th and 8th eighth of each bar lift from root to fifth; timing, length and velocity unchanged.
```

### deep house — indigo-held-room / indigo-soft-steps
**Style**
`deep house, 120 BPM, soft kick, accented sixteenth hats, long sub bass, electric piano ninths, dim room, instrumental`

**Description**
```
Instrumental 16-bar deep house skeleton in B minor over Bm9–Gmaj9–Em9–F♯m7.
Soft four-on-the-floor, accented closed sixteenth hats, long warm sub bass, rootless electric piano ninths. Bars 9–12 drop the bass; crash on bar 13.
Controlled pair — drums and bass identical, only the chord rhythm differs:
Variant A (Indigo Held Room): electric piano holds one chord per bar with sustain — space first.
Variant B (Indigo Soft Steps): the same voicings are softly stabbed twice per bar on the and-of-1 and the and-of-3 — motion first.
```

### lo-fi house — paper-lantern-eight / paper-lantern-five
**Style**
`lo-fi house, 121 BPM, swung hats, low muffled electric piano, late bass, dusty, lantern-lit, instrumental`

**Description**
```
Instrumental 16-bar lo-fi house skeleton in C minor over Cm9–A♭maj9–Fm9–B♭9.
Soft four-on-the-floor, swung hats, low quiet electric piano ninth stabs, bass dragging slightly behind the kick. Bars 9–12 drop the kick; crash on bar 13.
Controlled pair — only the hat density differs:
Variant A (Paper Lantern Eight): eight swung hats per bar.
Variant B (Paper Lantern Five): five of those eight remain, same timing and velocity on the survivors — more empty space, same groove underneath.
```

### lo-fi hip hop — porch-pocket-anchor / porch-pocket-skip
**Style**
`lo-fi hip hop, 82 BPM, boom bap, ghost snares, swung hats, kick-locked bass, electric piano ninths with sustain, porch at dusk, instrumental`

**Description**
```
Instrumental 16-bar lo-fi hip hop skeleton in E♭ major over E♭maj9–Cm9–A♭maj9–B♭9.
Acoustic-style boom bap, backbeat on 2 and 4, ghost snares, swung hats, electric piano ninths held with sustain. Kick and bass always strike together, three hits per bar. Bars 9–12 drop the hats; crash on bar 13.
Controlled pair — only where the three kick-and-bass hits land differs:
Variant A (Porch Pocket Anchor): on 1, on 3, and the and-of-3 — anchored.
Variant B (Porch Pocket Skip): on 1, the last sixteenth of 1, and the last sixteenth of 3 — pushed ahead, skipping.
Both keep the 2-and-4 backbeat; this is not a half-time comparison.
```

---

## claude-fable 세트 (병행조 대조)

### house — copper-tram-minor / copper-tram-major
**Style**
`house, 124 BPM, tight four-on-the-floor, drum machine, pulse synth bass, bright grand piano four-note stabs, city tram, instrumental`

**Description**
```
Instrumental 16-bar house skeleton in G. Tight, almost machine-straight four-on-the-floor, clap under snare on 2 and 4, closed hats on the beat and open hats on the off-beats.
Eighth-note synth bass cell: root–root–octave–root–fifth–root–octave–root. Grand piano four-note stabs, three per odd bar and four per even bar. Bars 9–12 drop the stabs; crash on bar 13.
Parallel-mode pair — drums, bass rhythm and stab rhythm are note-for-note identical; only the key mode changes:
Variant A (Copper Tram Minor): G minor, Gm7–Cm7–E♭maj7–F7.
Variant B (Copper Tram Major): G major, Gmaj7–Cmaj7–Em7–D7.
```

### deep house — harbor-fog-minor / harbor-fog-major
**Style**
`deep house, 120 BPM, soft kick, sixteenth hats with back-eighth accents, sub bass, rootless electric piano ninths with sustain, soft pad, harbor fog, instrumental`

**Description**
```
Instrumental 16-bar deep house skeleton in D. Soft four-on-the-floor, closed sixteenth hats accenting the back eighths, an open hat on the and-of-4 every other bar.
Sub bass cell: long note on 1, short on the and-of-2 and the and-of-3 a fifth below. Rootless electric piano ninths held for two beats with a soft re-touch, sustain re-pedalled each bar; classic pad on root and fifth underneath. Bars 9–12 drop kick and snare, leaving hats, bass, keys and pad; crash on bar 13.
Parallel-mode pair — rhythm section and pad identical; only the mode changes:
Variant A (Harbor Fog Minor): D minor, Dm9–Gm9–B♭maj9–A7♭9.
Variant B (Harbor Fog Major): D major, Dmaj9–Gmaj9–Bm9–A9.
```

### lo-fi house — attic-radio-minor / attic-radio-major
**Style**
`lo-fi house, 121 BPM, sparse swung hats, late pulse bass, low rootless electric piano shells, attic radio, dusty, instrumental`

**Description**
```
Instrumental 16-bar lo-fi house skeleton in A. Soft four-on-the-floor, clap under snare, only five swung hats per bar with an open hat every fourth bar.
Synth bass sits a touch behind the kick on 1, the and-of-1, 2 and the and-of-3 with octave jumps. Low rootless electric piano shells touched softly on three swung off-beats. Bars 9–12 drop the bass; crash on bar 13.
Parallel-mode pair — drums, bass delay and stab rhythm identical; only the mode changes:
Variant A (Attic Radio Minor): A minor, Am9–Fmaj9–Dm9–E7♭9.
Variant B (Attic Radio Major): A major, Amaj9–F♯m9–Dmaj9–E9.
```

### lo-fi hip hop — late-bus-minor / late-bus-major
**Style**
`lo-fi hip hop, 80 BPM, boom bap, two ghost snares, swung eighth hats, kick-locked finger bass, rootless grand piano ninths with sustain, late bus, instrumental`

**Description**
```
Instrumental 16-bar lo-fi hip hop skeleton in C. Acoustic-style boom bap: kick on 1, the a-of-2 and the and-of-3 in odd bars, 1, the and-of-3 and the a-of-4 in even bars; snare on 2 and 4 with two ghost notes; swung eighth hats.
Finger bass follows the kick exactly with fifth-below and fifth-above passing notes. Rootless grand piano ninths held a whole bar with a light roll, soft re-hit on the and-of-3 in even bars, sustain re-pedalled every bar. Bars 9–12 drop all drums, leaving piano and bass; a two-note snare pickup at the end of bar 12 and a crash on bar 13 bring everything back.
Parallel-mode pair — drums, bass and pedalling identical; only the mode changes:
Variant A (Late Bus Minor): C minor, Cm9–A♭maj9–Fm9–G7♭9.
Variant B (Late Bus Major): C major, Cmaj9–Am9–Fmaj9–G9.
```

# 2026-10-12 Deep House Set (30 slots, 64-bar DJ tracks)

## dh03-cistern-hum-v1
**Style**
```
Instrumental chill deep house, 118 BPM, E minor, soft four-on-the-floor kick, rimshot, three sparse closed hats per bar, long low sub bass on an E pedal, late held electric piano minor ninth and nine-sus-four chords, early-set opener, no lead, no vocals, DJ-friendly intro/outro.
```

**Description**
```
A 64-bar early-set deep house track in E minor over an E pedal: Em9 and A9sus4, two bars each — only two voices step down and back.
The electric piano comes in late, on the and-of-2, and holds for five beats once per chord, leaving long gaps.
Soft kick, quiet rimshot on 2 and 4 from bar 9, three closed hats per bar (after beats 1, 2 and 4, the and-of-3 left empty), one open hat every four bars.
Sub bass on E: a held note on the one, then a short fifth-below note on the and-of-3 of the next bar.
Structure: 1–16 intro (kick and hats, sub from bar 9, a chord hint at bar 12), 17–32 full, 33–40 break with the kick on the one only and no sub, 41–56 full with a crash on bar 41, 57–64 drums and bass only.
Damp, low, patient. No lead, no vocals, no melody, DJ-friendly intro/outro.
```

## dh06-chalk-river-v1
**Style**
```
Instrumental deep house, 119 BPM, B minor, soft kick, soft snare, sparse off-beat closed hats, short sub bass on beats 2 and 4, tonewheel organ minor ninth and dominant ninth chord chops, two-chord loop, drums-only break, no lead, no vocals, DJ-friendly intro/outro.
```

**Description**
```
A 64-bar deep house track in B minor on Bm9 and G9, two bars each; D and A stay while F# slips to F and C# to B, so the second chord darkens rather than brightens.
A tonewheel organ chops the chord short on the one and again as an eighth on beat 4, every bar.
Soft kick, soft snare on 2 and 4 from bar 9, six closed hats per bar (off-beats, beat 3 and a ghost on the last sixteenth), one open hat every two bars.
Sub bass plays short quarter notes on beats 2 and 4 together with the snare; in the second bar it drops a fifth on beat 4.
Structure: 1–16 intro, 17–32 full, 33–40 drums-only break (no sub, no organ), 41–56 full with a crash on bar 41, 57–64 drums and bass only.
Dry, grey, steady current. No lead, no vocals, no melody, DJ-friendly intro/outro.
```

## dh09-wet-asphalt-v1
**Style**
```
Instrumental chill deep house, 120 BPM, C# minor, soft kick, rimshot, swung sparse sixteenth hats, syncopated finger bass, electric piano minor eleventh and half-diminished chords, low pad in the second half, rebuilding break, no lead, no vocals, DJ-friendly intro/outro.
```

**Description**
```
A 64-bar deep house track in C# minor on C#m11 and G#m7b5, two bars each; the half-diminished chord's D natural casts a shadow over the loop.
The electric piano holds two beats from beat 2 and, at the end of each chord, touches the next one early on the and-of-4.
Soft kick, rimshot on 2 and 4 from bar 9, swung closed hats (seven per bar, with ghost notes), one open hat every four bars.
Finger bass pushes in on the last sixteenth of beat 2 and holds a beat and a half, with a short fifth-below pickup.
Structure: 1–16 intro, 17–32 full, 33–40 break that rebuilds two bars at a time — piano and low pad, then hats, then bass, then kick — 41–56 full with the pad and a crash on bar 41, 57–64 drums and bass only.
Night street after rain, reflective. No lead, no vocals, no melody, DJ-friendly intro/outro.
```

## dh12-tarnished-blue-v1
**Style**
```
Instrumental deep house, 121 BPM, G# minor, soft kick, soft snare, sparse off-beat hats with a ghost, off-beat sub bass, electric piano minor ninth and dominant thirteenth chords pushed across the bar line, broken two-step kick in the break, low pad, no lead, no vocals, DJ-friendly intro/outro.
```

**Description**
```
A 64-bar deep house track in G# minor on G#m9 and B13, two bars each; D# and F# are shared and the A natural in B13 adds a dusky colour.
The electric piano plays a short chord on beat 3 and pushes another on the and-of-4 that carries over the bar line.
Soft kick, soft snare on 2 and 4 from bar 9, six closed hats per bar, one open hat every three bars.
Sub bass on the off-beats: three per bar, the last one longer; the next bar answers with a fifth below.
Structure: 1–16 intro, 17–32 full, 33–40 break where the kick breaks into a two-step (the one and the and-of-2) while a low root-and-fifth pad enters, 41–56 full with the pad and a crash on bar 41, 57–64 drums and bass only.
Tarnished, tense, edging toward the peak. No lead, no vocals, no melody, DJ-friendly intro/outro.
```

## dh15-deep-meridian-v1
**Style**
```
Instrumental deep house, 122 BPM, B flat minor, peak of a deep set, soft but driving kick, soft snare with clap underneath, sparse sixteenth hats, syncopated sub bass, short electric piano minor eleventh and seventh-sus stabs, low root-and-fifth pad, no lead, no vocals, DJ-friendly intro/outro.
```

**Description**
```
A 64-bar peak-time deep house track in B flat minor on Bbm11 and Ab7sus4, two bars each; only one voice moves, F to G flat.
The electric piano plays short stabs on the second sixteenth of beat 1, answered on the and-of-2 or the second sixteenth of beat 4.
Soft but driving kick, soft snare with a quiet clap under it on 2 and 4 from bar 9, ten closed hats per bar, one open hat every two bars.
Sub bass: a short root on the one, a ghost before beat 3 and a held note on 3.
Structure: 1–16 intro, 17–32 full with a low root-and-fifth pad, 33–40 break that strips in three steps — hats out, then bass out, then kick out for the last two bars — 41–56 full with a crash on bar 41, 57–64 drums and bass only.
Deep, dark, rolling at the centre of the set. No lead, no vocals, no melody, DJ-friendly intro/outro.
```

## dh18-smoke-orchard-v1
**Style**
```
Instrumental dark deep house, 123 BPM, F minor, peak of a deep set, soft but driving kick, rimshot, paired off-beat hats, sub bass dropping an octave, tonewheel organ minor ninth and phrygian dominant ninth chords, two-bar silent drop before the return, no lead, no vocals, DJ-friendly intro/outro.
```

**Description**
```
A 64-bar peak-time deep house track in F minor on Fm9 and Gb9, two bars each; A flat stays on the bottom while three voices step down, giving a phrygian shade.
A tonewheel organ enters on the and-of-2 and holds two beats, then adds a short chord on the and-of-4.
Soft but driving kick, rimshot on 2 and 4 from bar 9, eight closed hats per bar in pairs (off-beat plus the last sixteenth), one open hat every four bars.
Sub bass: a short root on the one, then a beat-long note an octave lower on the and-of-2.
Structure: 1–16 intro, 17–32 full, 33–38 break without bass, 39–40 all drums and bass stop and only the organ remains, 41–56 full with a crash on bar 41, 57–64 drums and bass only.
Smoky, heavy, late-night peak. No lead, no vocals, no melody, DJ-friendly intro/outro.
```

## dh21-slow-orbit-v1
**Style**
```
Instrumental chill deep house, 121 BPM, G minor, drifting, soft kick, rimshot, swung eighth hats, long sub bass, held electric piano minor ninth and major ninth chords a tritone apart, warm low root-and-fifth pad, sub-and-pad break, no lead, no vocals, DJ-friendly intro/outro.
```

**Description**
```
A 64-bar drifting deep house track in G minor on Gm9 and Dbmaj9, two bars each; the two chords sit a tritone apart but share F, and the other voices move by a half or whole step.
The electric piano holds a chord on the one of every bar, softer in the second bar of each pair.
A low root-and-fifth pad sits underneath from bar 9 and carries much of the weight.
Soft kick, rimshot on 2 and 4 from bar 9, swung closed hats with the downbeat of 4 left empty, one open hat every four bars.
The sub holds for five and a half beats, then answers with two short notes.
Structure: 1–16 intro, 17–32 full, 33–40 break with only sub bass and pad, 41–56 full with a crash on bar 41, 57–64 drums and bass only.
Weightless, slow, after the peak. No lead, no vocals, no melody, DJ-friendly intro/outro.
```

## dh24-umber-lane-v1
**Style**
```
Instrumental chill deep house, 120 BPM, D minor, soft kick, soft snare, sparse paired hats, syncopated finger bass, soft held grand piano minor eleventh chord whose fifth drops a half step, low pad, kick-and-sub break, no lead, no vocals, DJ-friendly intro/outro.
```

**Description**
```
A 64-bar deep house track in D minor on Dm11 and Dm11b5, two bars each; the only movement is the fifth, A sinking to A flat and back, as if the tonic dims.
A soft grand piano enters on beat 3 and holds for five and a half beats.
Soft kick, soft snare on 2 and 4 from bar 9, six closed hats per bar (pairs on the e and the and), one open hat every two bars.
Finger bass on the second sixteenth of beats 1 and 3, with a fifth-below note on beat 4 of the second bar.
Structure: 1–16 intro, 17–32 full with a low root-and-fifth pad from bar 25, 33–40 break with only kick and sub, 41–56 full with a crash on bar 41, 57–64 drums and bass only.
Brown, dusky, beginning to cool. No lead, no vocals, no melody, DJ-friendly intro/outro.
```

## dh27-quiet-pier-v1
**Style**
```
Instrumental chill deep house cooldown, 118 BPM, D minor, soft kick, rimshot, three closed hats per bar, sparse sub bass, soft electric piano minor ninth and sus-two chords, rim-and-piano break, no lead, no vocals, DJ-friendly intro/outro.
```

**Description**
```
A 64-bar cooldown deep house track in D minor on Dm9 and Fsus2, two bars each; only A moves to G, and the sus chord has no third.
The electric piano plays a half-bar chord on the one and a short soft touch on beat 3 of the next bar.
Soft kick, quiet rimshot on 2 and 4 from bar 9, three closed hats per bar (after beat 2, a ghost before beat 4, after beat 4), one open hat every four bars.
The sub plays three times every four bars: a long D, a shorter note on the and-of-2, and a short F at the end.
Structure: 1–16 intro, 17–32 full, 33–40 break with only rimshot and electric piano, 41–56 full with a crash on bar 41, 57–64 drums and bass only.
Still water, wooden boards, quiet. No lead, no vocals, no melody, DJ-friendly intro/outro.
```

## dh30-house-lights-v1
**Style**
```
Instrumental chill deep house closer, 116 BPM, A minor, soft kick, rimshot, very sparse closed hats, short sub bass, soft grand piano minor ninth and sus-two chords, low pad, long 16-bar outro where the drums fall away one by one, no lead, no vocals, DJ-friendly intro/outro.
```

**Description**
```
A 72-bar set closer in A minor on Am9 and Esus2, two bars each; the sus chord has no third and its F# gives a dorian colour.
A soft grand piano plays from the and-of-1 for three beats, and adds a short chord on the and-of-3 of the next bar.
Soft kick, quiet rimshot on 2 and 4 from bar 9, three closed hats per bar, one open hat every four bars.
Sub bass: a beat-long A on the one and a short note on the and-of-3, then a bar of rest.
Structure: 1–16 intro, 17–32 full with a low root-and-fifth pad, 33–40 break with hats, piano and pad only, 41–56 full with a crash on bar 41, then a 16-bar outro: 57–60 drums and bass, 61–64 without the rimshot, 65–68 kick and bass, 69–71 kick alone, and a single kick on the one of bar 72.
House lights coming up, the room emptying. No lead, no vocals, no melody, DJ-friendly intro/outro.
```

## dh01-unlit-threshold-v1
**Style**
`Instrumental chill deep house set opener, 117 BPM, A minor, very soft four-on-the-floor kick, two closed hats per bar, sparse tonic sub, barely audible electric piano minor-ninth shells, no pad, no lead, no vocals, DJ-friendly intro/outro.`

**Description**
```
Unlit Threshold is a 64-bar set opener built almost entirely from drums and A1 sub bass.
Keep Am9 static: a low rootless C3-G3-B3 shell, a short touch on the and-of-2 only once every eight bars in the main sections. Do not introduce a bright chord sequence.
The bass enters at bar 9, holding A1 from the and-of-1 for 3.25 beats, followed by a whole bar of rest. No bass runs or ascending fifths.
Use two quiet closed hats per bar, alternating their locations across two bars, and one open hat every four bars outside the break. Rimshot enters only at bar 17.
Structure: 1-16 intro, 17-32 A, 33-40 break with sub bass alone, 41-56 A2, 57-64 drums and bass only. One quiet crash lands exactly on bar 41 beat 1.
The first eight bars contain kick and hats only. A tiny piano hint at bar 12 is followed by four chord-free bars before the main section.
Low ceiling, empty room, almost no harmonic motion. No lead, no vocals, DJ-friendly intro/outro.
```

## dh04-moss-circuit-v1
**Style**
`Instrumental restrained deep house, 118 BPM, E minor with a dorian sixth colour, soft drum machine, four shifting closed hats per bar, low pulse bass, quiet electric piano, piano-only break, no pad, no lead, no vocals, DJ-friendly intro/outro.`

**Description**
```
Moss Circuit is a 64-bar deep house track on Em9 for six bars and Em6/9 for two bars. Only the piano's D moves down to C#; E remains the bass pedal.
Place piano holds at the and-of-1 in cycle bars 1 and 7, with a shorter late touch at the and-of-3 in cycle bar 4. Keep several whole bars empty and re-pedal each held chord within its bar.
The two-bar bass cell is a 2.75-beat E2 on beat 1, then a short A1, a fifth below, on the and-of-3 of the next bar.
Use a soft four-on-the-floor kick, quiet rimshot, four closed hats in different positions on alternate bars, and one open hat every four bars outside the break.
Structure: 1-16 intro, 17-32 A, 33-40 electric piano alone, 41-56 A2 with one quiet crash on bar 41 beat 1, 57-64 drums and tonic bass only.
Start with drums, introduce bass at bar 9, hint at piano once at bar 12, then open the full harmony at bar 17. No riser, glitter or emphatic backbeat.
Dark green circuitry, small harmonic shadows, no lead, no vocals, DJ-friendly intro/outro.
```

## dh07-silt-letters-v1
**Style**
`Instrumental deep dub house, 120 BPM, F# minor, soft four-on-the-floor kick, five sparse closed hats per bar, gentle rimshot, low finger bass, low tonewheel organ minor ninth and eleventh stabs, no pad, no lead, no vocals, DJ-friendly intro/outro.`

**Description**
```
Silt Letters is a 64-bar track on F#m9 and Bm11, two bars each, over an F# tonic bass pedal.
The organ gives one short chord on the and-of-3 in cycle bar 1 and one on the and-of-1 in cycle bar 3. Leave long gaps after each chord rather than stabbing every offbeat.
The bass cell plays short roots on the and-of-2 and and-of-4, then a longer root on the and-of-1 of the next bar. Keep all notes in the sub register with no octave-running riff.
Use five closed hats per bar with a changing omission pattern and one open hat every three bars. Keep kick velocity soft and rimshot restrained.
Structure: 1-16 intro, 17-32 A, 33-40 hats, rimshot and sub only with both kick and organ absent, 41-56 A2, 57-64 drums and bass only.
Bass enters at bar 9; a small organ hint appears at bar 12; full chord rhythm starts at bar 17. Add a single restrained crash on bar 41 beat 1.
Silt settling in slow water, low midrange weight, no lead, no vocals, DJ-friendly intro/outro.
```

## dh10-underpass-velour-v1
**Style**
`Instrumental late-night deep house, 121 BPM, C# minor, six sparse closed hats per bar, soft kick and rimshot, low pulse bass, held electric piano minor elevenths, hatless and bassless break, no pad, no lead, no vocals, DJ-friendly intro/outro.`

**Description**
```
Underpass Velour is a 64-bar track on C#m11 for three bars and G#m9 for one bar, keeping C# in the bass.
The electric piano holds from beat 2 in cycle bar 1 for 2.5 beats and from beat 1 in cycle bar 4 for 2.25 beats. Re-pedal inside each active bar and leave the middle two bars empty.
Bass alternates a short C#2 on the and-of-1 and a longer C#2 on the and-of-3, then a 1.65-beat F#1 on the and-of-2 of the next bar. The fifth moves downward, never upward.
Six closed hats per bar change positions across a two-bar cycle; an open hat occurs once every three bars, not on every offbeat.
Structure: 1-16 intro, 17-32 A, 33-40 kick, rimshot and piano only, 41-56 A2 with one quiet crash on bar 41 beat 1, 57-64 drums and tonic bass only.
Build from drums to bass at bar 9, add one piano hint at bar 12, and start the full harmony at bar 17.
Soft concrete, restrained pressure, no lead, no vocals, DJ-friendly intro/outro.
```

## dh13-basalt-current-v1
**Style**
`Instrumental deep house peak without brightness, 122 BPM, Eb minor, soft steady kick, eighth-note hats with one occasional sixteenth, quiet snare with a softer clap underneath, low sub bass, sparse minor tonewheel organ chords, no pad, no lead, no vocals, DJ-friendly intro/outro.`

**Description**
```
Basalt Current begins the deep peak with Ebm9 and Abm6, two bars each, over an Eb tonic pedal. Keep the minor centre dark; the added sixth is a shadow rather than a major-key lift.
Place one short low organ chord per bar, cycling through the and-of-2, beat 4, the and-of-3, and the and-of-1.
The bass cell has a longer Eb2 on beat 1 and a short Ab1 below it on the and-of-3; the next bar answers with a short Eb2 on the and-of-1 and a longer Eb2 on beat 3.
Use eight closed-hat positions per bar and one extra quiet sixteenth only in every fourth bar. One open hat every two bars replaces a closed hat. Keep clap strictly below the snare at the same onset.
Structure: 1-16 intro, 17-32 A, 33-40 checkerboard break, 41-56 A2, 57-64 drums and tonic bass only. In the break, odd bars retain kick, snare and bass; even bars retain hats, snare and organ.
Start with drums, add sub at bar 9 and a small organ touch at bar 12. A single quiet crash marks bar 41 beat 1.
Peak through density and negative space, not louder attacks or bright voicings. No lead, no vocals, DJ-friendly intro/outro.
```

## dh16-blackwater-fold-v1
**Style**
`Instrumental dark deep house peak, 123 BPM, Bb minor, soft four-on-the-floor kick, alternating seven and eight closed hats, low root-only sub, sparse tonewheel organ ninth and eleventh chords, two-stage break, no pad, no lead, no vocals, DJ-friendly intro/outro.`

**Description**
```
Blackwater Fold is a 64-bar tonic-centred track on Bbm9 for four bars and Bbm11 for four bars. Exchange the fifth and eleventh in the organ without moving the bass root.
Use only four short organ stabs per eight-bar cycle: the and-of-1 in bar 1, the and-of-3 in bar 3, the and-of-2 in bar 5, and the and-of-3 in bar 8.
Bass stays on Bb1: three short notes on the and-of-1, and-of-3 and and-of-4, then a 1.35-beat note on the and-of-2 of the next bar.
Closed hats alternate seven and eight positions per bar. An open hat appears every two bars. Layer a quiet clap directly beneath each soft snare, never alone.
Structure: 1-16 intro, 17-32 A, 33-36 kick and organ only, 37-40 hats and bass only, 41-56 A2 with one quiet crash on bar 41 beat 1, 57-64 drums and bass only.
Bass enters at bar 9; one organ hint appears at bar 12; the full harmonic rhythm begins at bar 17. Keep every kick soft despite the peak tempo.
Two dark rooms handing the groove to each other, no lead, no vocals, DJ-friendly intro/outro.
```

## dh19-pressure-glass-v1
**Style**
`Instrumental deep house decompression, 122 BPM, C minor, soft kick and rimshot, variable sparse eighth hats, low finger bass, restrained electric piano minor elevenths and a semitone-neighbour chord, no pad, no lead, no vocals, DJ-friendly intro/outro.`

**Description**
```
Pressure Glass is a 64-bar track on Cm11 for six bars and Dbmaj7(#11)/C for two bars. Keep C as a bass pedal so the upper neighbour remains a dark tension rather than a new major centre.
The piano plays low holds in cycle bars 1, 3, 5 and 7, entering on beat 1, beat 2, the and-of-1 and beat 1 respectively. Release the pedal within each bar.
Bass plays a 1.5-beat C2 on beat 1 and a short C2 on the and-of-3; the next bar has a short C2 on the and-of-1 and a low F1 on beat 4.
Closed-hat counts move through 6, 7, 8 and 7 per bar, with one open hat every two bars. Keep rimshot weak and omit clap.
Structure: 1-16 intro, 17-32 A, 33-40 kick, sub and piano only with all hats and backbeats absent, 41-56 A2, 57-64 drums and tonic bass only.
Bass enters at bar 9 and piano hints once at bar 12 before the full section at bar 17. Place only one quiet crash on bar 41 beat 1.
Release the peak's pressure without raising the register. No lead, no vocals, DJ-friendly intro/outro.
```

## dh22-drift-archive-v1
**Style**
`Instrumental drifting deep house, 121 BPM, G minor, soft kick and rimshot, alternating five and six closed hats, long sparse sub, low electric piano, very quiet root-and-fifth pad, harmonic-island break, no lead, no vocals, DJ-friendly intro/outro.`

**Description**
```
Drift Archive is a 64-bar drift on Gm9 and F6/9/G, four bars each, with G remaining the bass pedal.
Hold electric piano chords from the and-of-2 in the first bar of each four-bar cell and from the and-of-1 in its third bar. Re-pedal each active bar; leave whole bars between attacks.
The four-bar bass cell is G2 on beat 2 for 2.5 beats, one empty bar, G2 on the and-of-1 for 2.25 beats, then a short C2 a fifth below on the and-of-4.
Use five and six closed hats on alternating bars and one open hat every three bars. A quiet low pad contains only G2 and D3, entering at bar 17.
Structure: 1-16 intro, 17-32 A, 33-40 piano and root-fifth pad only with every drum and bass note removed, 41-56 A2, 57-64 drums and tonic bass only.
Introduce bass at bar 9 and one small piano hint at bar 12. A single quiet crash marks bar 41 beat 1. Remove both piano and pad before bar 57.
Suspended dust, low harmonic weight, no glittering layer, no lead, no vocals, DJ-friendly intro/outro.
```

## dh25-dim-stairwell-v1
**Style**
`Instrumental cooling deep dub house, 119 BPM, A minor, soft kick, quiet rimshot, alternating four and five closed hats, sparse low finger bass, short electric piano minor chords with long gaps, no pad, no lead, no vocals, DJ-friendly intro/outro.`

**Description**
```
Dim Stairwell is a 64-bar cooldown track on Am9 for one bar and Dm7/A for three bars, with A1 anchored underneath.
The piano gives three short dub touches per four-bar cycle: the and-of-4 in bar 1, the and-of-2 in bar 2, and the and-of-1 in bar 4. Let the third bar remain empty.
The four-bar bass cell plays A1 on the and-of-3 for 1.1 beats, a short A1 on the and-of-1 of the next bar, a whole bar of rest, then A1 on the and-of-2 for 1.75 beats.
Closed hats alternate four and five positions per bar. Use one open hat every three bars, a quiet rimshot and no clap.
Structure: 1-16 intro, 17-32 A, 33-40 rimshot and bass only with kick, hats and piano absent, 41-56 A2 with one quiet crash on bar 41 beat 1, 57-64 drums and bass only.
Begin with kick and hats, add bass at bar 9, hint at piano once at bar 12, and begin the full chord cycle at bar 17.
Descending into a dim stairwell without an ascending bass riff, no lead, no vocals, DJ-friendly intro/outro.
```

## dh28-drowned-linen-v1
**Style**
`Instrumental deep house pre-closer, 118 BPM, D minor, very soft kick and rimshot, alternating two and three closed hats, long sparse sub, low grand piano minor elevenths, two-bar silent inhale, no pad, no lead, no vocals, DJ-friendly intro/outro.`

**Description**
```
Drowned Linen is a 64-bar pre-closer on Dm11 and Cm9/D, four bars each, holding D as the bass pedal.
The low grand piano begins on beat 3 in cycle bars 1 and 5, and on the and-of-1 in bars 4 and 8. Hold these chords quietly inside their bars with pedal releases, not a continuous full-register wash.
The four-bar bass cell is D2 on beat 1 for 3.5 beats, two whole bars of rest, then G1 a fifth below on the and-of-3 for 1.2 beats.
Use only two and three closed hats on alternate bars, one open hat every four bars, a quiet rimshot and a very soft four-on-the-floor kick.
Structure: 1-16 intro, 17-32 A, 33-34 complete silence, 35-40 piano and sub only, 41-56 A2, 57-64 drums and tonic bass only. All held notes and pedals stop before the silent passage.
Bass enters at bar 9, a small piano hint appears at bar 12, and the full harmony opens at bar 17. One quiet crash lands on bar 41 beat 1.
Leave room for the final two slots rather than closing the set here. No lead, no vocals, DJ-friendly intro/outro.
```

## dh02-ash-corridor-v1
**Style**
```
Instrumental chill deep house second opener, 117 BPM, A minor, very soft four-on-the-floor kick, one or three closed hats per bar, rimshot on beat 3 only, long tonic sub, held electric piano minor ninth and half-diminished shells, no pad, no lead, no vocals, DJ-friendly intro/outro.
```

**Description**
```
Ash Corridor is a 64-bar second opener on Am9 for four bars and Bm7b5/A for four bars, with A1 held underneath as a pedal; three inner voices step up by one note and back.
The electric piano plays every other bar from the and-of-2, holding 2.25 beats with the sustain pedal, plus one short touch on the and-of-4 before each chord change.
Very soft kick, a single closed hat on the and-of-2 in odd bars and three hats in even bars, one open hat every four bars, a quiet rimshot on beat 3 only from bar 17.
Sub bass on A1: three beats on the one, then a 1.75-beat note from beat 3 of the next bar; root only, no fifth, no octave jumps.
Structure: 1-16 intro (kick and hats, sub from bar 9, two small piano hints at bars 12 and 14), 17-32 full, 33-36 closed hats alone, 37-40 hats and sub, 41-56 full with one quiet crash on bar 41 beat 1, 57-64 drums and bass only.
Dim, slow and unhurried. No lead, no vocals, no melody, DJ-friendly intro/outro.
```

## dh05-tin-lantern-v1
**Style**
```
Instrumental deep dub house, 119 BPM, B minor with a dorian sixth, soft kick, rimshot, five sparse closed hats per bar, short pushed sub bass, tonewheel organ minor ninth and lydian major-seventh stabs with long gaps, kick-hats-organ break, no pad, no lead, no vocals, DJ-friendly intro/outro.
```

**Description**
```
Tin Lantern is a 64-bar deep house track alternating Bm9 and Dmaj7(#11)/B every bar over a B pedal; only one voice moves, A down to G#, giving the loop a dorian shade.
Tonewheel organ dub stabs: a short hit on the and-of-1 and the last sixteenth of beat 3 in odd bars, one hit on the and-of-2 in even bars, nothing held.
Soft kick, quiet rimshot on 2 and 4 from bar 9, five closed hats per bar with a ghost on the e-of-2 or the e-of-4, one open hat every three bars.
Sub bass: a short pickup on the and-of-1 into a 1.4-beat note on beat 2; the second bar's long note drops to the fifth below (E1) in the full sections only.
Structure: 1-16 intro (kick and hats, sub from bar 9, small organ hints at bars 12 and 14), 17-32 full, 33-40 break with kick, hats and organ but no rim and no sub, 41-56 full with one quiet crash on bar 41 beat 1, 57-64 drums and bass only.
Warm, low and dubby. No lead, no vocals, no melody, DJ-friendly intro/outro.
```

## dh08-slate-hallway-v1
**Style**
```
Instrumental chill deep house, 120 BPM, F# minor with a dorian sixth, soft kick, rimshot, swung closed hats alternating six and four per bar, syncopated sub bass dropping an octave, held electric piano minor ninth and minor eleventh chords planing a whole step, keys-then-sub break, no pad, no lead, no vocals, DJ-friendly intro/outro.
```

**Description**
```
Slate Hallway is a 64-bar deep house track on F#m9 and G#m11/F#, two bars each, over an F# pedal; the three upper voices slide up a whole step and back, the D# giving a dorian colour.
The electric piano holds 1.75 beats from the one, then 1.25 beats from the swung and-of-3 in the next bar, with the sustain pedal re-pressed each attack.
Soft kick, quiet rimshot on 2 and 4 from bar 9, swung closed hats (six positions in odd bars, four in even bars), one open hat every two bars.
Sub bass: short notes on the and-of-2 and beat 3, then a one-beat note on beat 4; in the second bar the beat-4 note drops an octave to F#1 during the full sections.
Structure: 1-16 intro (kick and hats, sub from bar 9, small piano hints at bars 12 and 14), 17-32 full, 33-36 electric piano alone, 37-40 sub alone, 41-56 full with one quiet crash on bar 41 beat 1, 57-64 drums and bass only.
Smooth and shadowed. No lead, no vocals, no melody, DJ-friendly intro/outro.
```

## dh11-cinder-arcade-v1
**Style**
```
Instrumental deep house, 121 BPM, G# minor, soft kick, rimshot, six or seven sparse closed hats per bar with off-grid ghosts, tight sub bass with sixteenth pickups, short soft grand piano minor ninth stabs and one held lydian flat-six chord, half-time kick break, no pad, no lead, no vocals, DJ-friendly intro/outro.
```

**Description**
```
Cinder Arcade is a 64-bar deep house track on G#m9 for three bars and Emaj7(#11)/G# for one bar, with G#1 held under both; two voices step down for the fourth bar and return.
Soft grand piano plays a half-beat stab on the and-of-3 in the first three bars of each cycle, then holds 2.75 beats from the and-of-1 in the fourth bar with the sustain pedal.
Soft kick, quiet rimshot on 2 and 4 from bar 9, six or seven closed hats per bar using the a-of-1 and a-of-3 as ghosts, one open hat every three bars.
Sub bass on G#1 only: a short note on the one, a sixteenth pickup on the a-of-1, then a 1.2-beat note from the and-of-3, or a short note on the and-of-4 in the second bar.
Structure: 1-16 intro (kick and hats, sub from bar 9, small piano hints at bars 12 and 14), 17-32 full, 33-40 break with the kick on beats 1 and 3 only and the sub, no hats, no rim, no piano, 41-56 full with one quiet crash on bar 41 beat 1, 57-64 drums and bass only.
Tense but quiet. No lead, no vocals, no melody, DJ-friendly intro/outro.
```

## dh14-iron-tide-v1
**Style**
```
Instrumental deep house peak without brightness, 122 BPM, Eb minor with a dorian sixth, soft steady kick, soft snare with a quieter clap underneath, nine sparse sixteenth hats per bar, syncopated sub bass, short tonewheel organ minor ninth and half-diminished stabs, top-then-bottom break, no pad, no lead, no vocals, DJ-friendly intro/outro.
```

**Description**
```
Iron Tide is a 64-bar peak-section deep house track alternating Ebm9 and Cm7b5/Eb every bar over an Eb pedal; Db drops to C and F to Eb, a dorian half-diminished shade.
Tonewheel organ stabs: a short hit on the and-of-2 and on beat 3 in odd bars, on the and-of-2 and the e-of-3 in even bars, never held.
Soft but steady kick, soft snare on 2 and 4 with a quieter clap exactly under it from bar 9, nine closed hats per bar in sparse sixteenth pairs, one open hat every two bars.
Sub bass: a note on the one, a short and-of-2, a note on beat 3, and in odd bars a short fifth-below (Bb1) on the and-of-4; even bars hold beat 3 for 1.4 beats.
Structure: 1-16 intro (kick and hats, sub from bar 9, small organ hints at bars 12 and 14), 17-32 full, 33-36 hats, snare and organ only (no kick, no sub), 37-40 kick and sub only, 41-56 full with one quiet crash on bar 41 beat 1, 57-64 drums and bass only.
Dense in the low-mids, never bright. No lead, no vocals, no melody, DJ-friendly intro/outro.
```

## dh17-coal-harbour-v1
**Style**
```
Instrumental dark deep house peak, 123 BPM, F minor with a dorian sixth, soft but driving kick, soft snare without clap, eighth-note hats with two ghost sixteenths, all-off-beat sub bass, held electric piano minor ninth and flat-seven major-seventh chords, drone-sub break, no pad, no lead, no vocals, DJ-friendly intro/outro.
```

**Description**
```
Coal Harbour is a 64-bar peak deep house track on Fm9 and Ebmaj7/F, two bars each, with F2 under both; all four voices step down into a D-Eb cluster and back, the D natural giving a dorian colour.
The electric piano holds 3.25 beats from the and-of-1 with the sustain pedal, then plays one short touch on the and-of-4 of the next bar.
Soft but driving kick, soft snare on 2 and 4 from bar 9 with no clap, eighth-note hats with ghost sixteenths on the e-of-1 and e-of-3 in odd bars, one open hat every two bars.
Sub bass entirely on the off-beats: four short and-of-beat notes in odd bars; in even bars the and-of-3 note lengthens to 1.4 beats and drops to the fifth below (Bb1) in the full sections.
Structure: 1-16 intro (kick and hats, sub from bar 9, small piano hints at bars 12 and 14), 17-32 full, 33-40 break with hats and snare over a whole-note sub drone, no kick, no piano, 41-56 full with one quiet crash on bar 41 beat 1, 57-64 drums and bass only.
Heavy below, empty above. No lead, no vocals, no melody, DJ-friendly intro/outro.
```

## dh20-wet-granite-v1
**Style**
```
Instrumental deep house end of peak, 122 BPM, C minor, soft kick, rimshot, six or four sparse closed hats per bar, sub bass with a fifth below, held soft grand piano minor ninth and flat-six major-seventh chords, low root-and-fifth pad entering in the break, rim-and-pad break, no lead, no vocals, DJ-friendly intro/outro.
```

**Description**
```
Wet Granite is a 64-bar track that closes the peak section on Cm9 for five bars and Abmaj7/C for three bars, with C2 under both; Bb falls to Ab and D to C, an aeolian flat-six shade.
Soft grand piano holds 3.5 beats from the one in cycle bars 1, 3 and 5, then 2.75 beats from beat 2 in bars 6 and 8, with the sustain pedal re-pressed each attack.
Soft kick, quiet rimshot on 2 and 4 from bar 9, six closed hats in odd bars (with e-of-3 and e-of-4 ghosts) and four in even bars, one open hat every three bars.
Sub bass: a 1.5-beat note on the one, a short and-of-3 and a note on beat 4; the second bar's beat-4 note drops to the fifth below (G1) in the full sections.
A very quiet root-and-fifth pad (G2 and C3) enters at bar 33 and stays until bar 56.
Structure: 1-16 intro (kick and hats, sub from bar 9, small piano hints at bars 12 and 14), 17-32 full, 33-40 rimshot and pad only, 41-56 full with one quiet crash on bar 41 beat 1, 57-64 drums and bass only.
Settling, not lifting. No lead, no vocals, no melody, DJ-friendly intro/outro.
```

## dh23-paper-lantern-v1
**Style**
```
Instrumental drifting deep house, 120 BPM, D minor, soft kick, rimshot, swung five-hat patterns, sparse sub bass, held electric piano minor ninth and flat-three major ninth chords, very quiet root-and-fifth pad from the first full section, hats-and-pad break, no lead, no vocals, DJ-friendly intro/outro.
```

**Description**
```
Paper Lantern is a 64-bar drifting deep house track on Dm9 and Fmaj9/D, four bars each, with D2 held under both; F steps down to E and A to G while the top E rises to F.
The electric piano holds 1.9 beats from beat 3 in cycle bars 1 and 5, 3.25 beats from the swung and-of-1 in bars 2 and 6, and a short touch on beat 3 of bar 8, sustain pedal re-pressed each attack.
Soft kick, quiet rimshot on 2 and 4 from bar 9, swung closed hats in two five-position patterns, one open hat every four bars.
Sub bass: a 0.75-beat note on beat 2 and a 1.4-beat note from the swung and-of-3; the second bar replaces the long note with a short fifth-below (A1) on the and-of-4 in the full sections.
A very quiet root-and-fifth pad (A2 and D3) lies underneath from bar 17 to bar 56.
Structure: 1-16 intro (kick and hats, sub from bar 9, small piano hints at bars 12 and 14), 17-32 full, 33-40 closed hats and pad only, 41-56 full with one quiet crash on bar 41 beat 1, 57-64 drums and bass only.
Soft-lit and slow. No lead, no vocals, no melody, DJ-friendly intro/outro.
```

## dh26-dusk-ledger-v1
**Style**
```
Instrumental cooling deep house, 119 BPM, A minor, soft kick, quiet rimshot from bar 13, two or four closed hats per bar, four-bar sub cell with a bar of rest, short electric piano minor ninth and six-nine stabs, kick-only break, no pad, no lead, no vocals, DJ-friendly intro/outro.
```

**Description**
```
Dusk Ledger is a 64-bar cooling deep house track on Am9 for six bars and C6/9/A for two bars, with A1 held underneath; only B falls to A and C rises to D.
The electric piano plays short 0.4-beat stabs on the and-of-4 of cycle bar 1, the and-of-2 of bar 3 and the and-of-4 of bar 5, then a 1.4-beat chord from the and-of-1 of bar 7 and a 1.2-beat chord from the and-of-3 of bar 8, none pedalled.
Soft kick, quiet rimshot on 2 and 4 from bar 13, two closed hats in odd bars and four in even bars, one open hat every four bars.
Sub bass on A1 only, a four-bar cell: a one-beat note on the one and a short and-of-4, a 1.4-beat note from the and-of-3, the first bar again, then a whole bar of rest.
Structure: 1-16 intro (kick and hats, sub from bar 9, small piano hints at bars 12 and 14), 17-32 full, 33-40 kick alone, 41-56 full with one quiet crash on bar 41 beat 1, 57-64 drums and bass only.
Thinning toward the close. No lead, no vocals, no melody, DJ-friendly intro/outro.
```

## dh29-last-corridor-v1
**Style**
```
Instrumental chill deep house pre-closer, 117 BPM, A minor with one dorian touch, very soft kick, rimshot on beat 3 only, one or two closed hats per bar, long sparse tonic sub, held soft grand piano minor eleventh shell with one rootless five-eleven bar, hats-and-rim break, no pad, no lead, no vocals, DJ-friendly intro/outro.
```

**Description**
```
Last Corridor is a 64-bar pre-closer on an Am11 shell for seven bars and Em11/A for one bar, with A1 held underneath; in the eighth bar C falls to A and E rises to F#, a single dorian touch.
Soft grand piano holds three beats from the and-of-1 in cycle bars 1 and 5, and 3.75 beats from the one in bar 8, sustain pedal re-pressed each attack.
Very soft kick, a single closed hat on the and-of-3 in odd bars and two hats in even bars, one open hat every four bars, a quiet rimshot on beat 3 only from bar 17.
Sub bass on A1 only, a four-bar cell: a whole-bar note, a 1.5-beat note on the one, a bar of rest, then a 1.9-beat note from beat 3.
Structure: 1-16 intro (kick and hats, sub from bar 9, small piano hints at bars 12 and 14), 17-32 full, 33-40 closed hats and rimshot only, 41-56 full with one quiet crash on bar 41 beat 1, 57-64 drums and bass only.
Leave the closing to the final slot. No lead, no vocals, no melody, DJ-friendly intro/outro.
```

---

# 2026-10-20 Deep House Set v3 — 곡별 Suno 프롬프트 (슬롯 순)

Cover 업로드 시 `{sid}-v3.wav` 와 함께 쓴다. Style 은 짧게, Description 은 커스텀 모드 가사란에 `[Instrumental]` 과 함께.

## dh01-unlit-threshold-v3
**Style**
`deep house, 117 BPM, A minor, Tough Kit, sub bass, held electric piano, low pad, unlit and spacious, instrumental`

**Description**
```
Deep house at 117 BPM, A minor: static rootless Am9, no changes.
Pulse Bass from bar 9: long A on &1 every other bar, alternate bar empty.
Tough Kit: four-floor kick from bar 5; soft on-beat closed hats, stronger &1/&3; open hats &2/&4. Snare+clap on 2/4 from bar 17. Two tom hits end bars 16/36/56.
Low Classic Pad A-E-B from bar 1. A/A2: held full-bar electric piano, pedal released each bar; eighth-note electric-piano Tex cycles C-G-B in one octave; SoCal congas, 3 hits/2 bars clear of kick/open hats, no shaker.
64 bars: 1-8 pad+hats intro, kick at 5; 9-36 A; 37-40 break: only sparse bass; drums, keys, pad, Tex and Perc drop; 41-56 A2: quarter-note ride replaces on-beat closed hats, off-beats stay, crash at 41; 57-64 drums+bass only.
No lead, no vocals, DJ-friendly intro/outro.
```

## dh02-ash-corridor-v3
**Style**
`chill deep house, 117 BPM, A minor, Tough Kit drums, accented kick, off-beat open hats, snare with clap, soft three-note pad, held electric piano minor ninth, organ arpeggio, sub bass, dim and unhurried, instrumental`

**Description**
```
Ash Corridor: 117 BPM, A minor. Am9 for four bars, Bm7b5/A for four bars over an A pedal; three inner voices step up one note and back.
Electric piano holds each chord for the whole bar, with one short touch on the and-of-4 in the last bar of each chord.
Soft pad (A2, E3, B3) under bars 1-56; quiet organ eighth-note chord-tone arpeggio in full sections.
Drums: four-on-the-floor kick, off-beat-accented eighth-note closed hats, open hat on the and-of-2 and and-of-4, snare with clap on 2 and 4 from bar 9, ride in 41-56, tom fills in bars 16, 36, 56, crash at 41. No shaker or congas.
Sub bass on A1 only from bar 9: three beats on the one, then a 1.75-beat note from beat 3 of the next bar.
Form: 1-8 intro (pad, hats; kick from bar 5), 9-36 full, 37-40 break: hats and pad only, sub returns in 39-40, 41-56 full with ride, 57-64 drums and sub only.
Dim, slow and unhurried. No lead, no vocals, DJ-friendly intro/outro.
```

## dh03-cistern-hum-v3
**Style**
`chill deep house, 118 BPM, E minor, punchy four-on-the-floor kick, snare and clap on 2 and 4, off-beat open hats, sub bass on an E pedal, held electric piano ninth chords, organ arpeggio, warm pad, early-set opener, instrumental`

**Description**
```
Instrumental deep house at 118 BPM in E minor. Loop: Em9 and A9sus4/E, two bars each, over an E pedal; only two voices step down, B to A and F# to E.
Drums: punchy four-on-the-floor kick, snare and clap on 2 and 4 from bar 9, closed-hat eighths, open hats on the and-of-2 and and-of-4. Tom fills at bars 16, 36, 56. Sparse congas from bar 13.
Sub bass from bar 9: a long E2 on the one, then a short B1 on the and-of-3 of the next bar.
Electric piano from bar 9: a short chord on the one and a held chord that rings into the second bar, sustain pedal.
Soft three-voice pad from bar 1, tonic only in the intro.
Tonewheel organ eighth-note arpeggio G4-B4-D5 / G4-A4-D5 in 17-36 and 41-56.
Structure: 1-8 intro (pad and hats, kick from bar 5), 9-36 full, 37-40 break with the kick on beat 1 only and the bass out, 41-56 full with ride and crash, 57-64 drums and bass only.
Dark, patient, early in the set. No lead, no vocals, DJ-friendly intro/outro.
```

## dh04-moss-circuit-v3
**Style**
`deep house, 118 BPM, E minor, Tough Kit, sub bass, sustained electric piano, low pad, mossy and restrained, instrumental`

**Description**
```
Deep house at 118 BPM, E minor: Em9 6 bars, Em6/9 2 bars; Dorian shade.
Pulse Bass from bar 9: long E on beat 1 alternates with short lower fifth on &3; tonic at DJ edges.
Tough Kit: four-floor kick from bar 5; soft on-beat closed hats, stronger &1/&3; open hats &2/&4. Snare+clap on 2/4 from bar 9. Two tom hits end bars 16/36/56.
Low Classic Pad E-B-F# from bar 1. A/A2: held full-bar electric piano, pedal released each bar; eighth-note electric-piano Tex cycles current chord tones in one octave; SoCal congas, 3 hits/2 bars clear of kick/open hats, no shaker.
64 bars: 1-8 pad+hats intro, kick at 5; 9-36 A; 37-40 break: held keys only; bass, drums, pad, Tex and Perc drop; 41-56 A2: quarter-note ride replaces on-beat closed hats, off-beats stay, crash at 41; 57-64 drums+bass only.
No lead, no vocals, DJ-friendly intro/outro.
```

## dh05-tin-lantern-v3
**Style**
`deep dub house, 119 BPM, B minor dorian, Tough Kit drums, accented kick, off-beat open hats, snare with clap, congas, soft pad, tonewheel organ dub stabs, electric piano arpeggio, pushed sub bass, warm and low, instrumental`

**Description**
```
Tin Lantern: 119 BPM, B minor dorian. Bm9 and Dmaj7(#11)/B alternate every bar over a B pedal; only one voice moves, A down to G#.
Tonewheel organ dub stabs, about one beat each: and-of-1 and a-of-3 in odd bars, and-of-2 and beat 4 in even bars.
Soft pad (B2, F#3, C#4) under bars 1-56; quiet electric piano eighth-note chord-tone arpeggio in full sections.
Drums: four-on-the-floor kick, off-beat-accented eighth-note closed hats, open hat on the and-of-2 and and-of-4, snare with clap on 2 and 4 from bar 9, ride in 41-56, tom fills in bars 16, 36, 56, crash at 41. Sparse conga cell in full sections, no shaker.
Sub bass from bar 9: pickup on the and-of-1 into a 1.4-beat note on beat 2; every second bar the long note drops to the fifth below (E1).
Form: 1-8 intro (pad, hats; kick from bar 5), 9-36 full, 37-40 break: kick, hats, organ and pad only, 41-56 full with ride, 57-64 drums and sub only.
Warm, low and dubby. No lead, no vocals, DJ-friendly intro/outro.
```

## dh06-chalk-river-v3
**Style**
`deep house, 119 BPM, B minor, punchy four-on-the-floor kick, snare and clap on 2 and 4, off-beat open hats, short sub bass on 2 and 4, tonewheel organ ninth chords, electric piano arpeggio, warm pad, instrumental`

**Description**
```
Instrumental deep house at 119 BPM in B minor. Loop: Bm9 and G9, two bars each; D and A are held while F# falls to F and C# to B.
Drums: punchy four-on-the-floor kick, snare and clap on 2 and 4 from bar 9, closed-hat eighths, open hats on the and-of-2 and and-of-4. Tom fills at bars 16, 36, 56. Congas from bar 13.
Sub bass from bar 9: short roots on beats 2 and 4 with the snare, dipping to the fifth (F#1) once every four bars.
Tonewheel organ from bar 9: a long chord on the one and a short chord on beat 4, every bar.
Three-voice pad from bar 1, tonic only in the intro.
Electric piano eighth-note arpeggio D4-F#4-A4-C#5 / D4-F4-A4-B4 in 17-36 and 41-56.
Structure: 1-8 intro (pad and hats, kick from bar 5), 9-36 full, 37-40 drums-only break (bass, organ and pad out), 41-56 full with ride and crash, 57-64 drums and bass only.
Dry, steady, grey. No lead, no vocals, DJ-friendly intro/outro.
```

## dh07-silt-letters-v3
**Style**
`deep house, 120 BPM, F# minor, Tough Kit, low bass, held organ, electric-piano texture, silt-dark, instrumental`

**Description**
```
Deep house at 120 BPM, F# minor: F#m9 / Bm11, 2 bars each.
Simple Foundation bass from bar 9: short tonics on &2/&4 alternate with longer tonic on &1.
Tough Kit: four-floor kick from bar 5; soft on-beat closed hats, stronger &1/&3; open hats &2/&4. Snare+clap on 2/4 from bar 9. Two tom hits end bars 16/36/56.
Low Classic Pad F#-C#-G# from bar 1. A/A2: held full-bar Tonewheel Organ, pedal released each bar; eighth-note electric-piano Tex cycles current chord tones in one octave; SoCal congas, 3 hits/2 bars clear of kick/open hats, no shaker.
64 bars: 1-8 pad+hats intro, kick at 5; 9-36 A; 37-40 break: bass, closed/open hats and snare+clap only; kick, keys, pad, Tex and Perc drop; 41-56 A2: quarter-note ride replaces on-beat closed hats, off-beats stay, crash at 41; 57-64 drums+bass only.
No lead, no vocals, DJ-friendly intro/outro.
```

## dh08-slate-hallway-v3
**Style**
`chill deep house, 120 BPM, F# minor dorian, Tough Kit drums, accented kick, swung off-beat open hats, snare with clap, congas, soft pad, held electric piano minor ninth and minor eleventh, organ arpeggio, octave-dropping sub bass, smooth and shadowed, instrumental`

**Description**
```
Slate Hallway: 120 BPM, F# minor dorian. F#m9 and G#m11/F#, two bars each, over an F# pedal; the upper voices slide up a whole step and back.
Electric piano chords on the one and beat 3 in odd bars, on the and-of-1 and swung and-of-3 in even bars.
Soft pad (F#3, C#4, G#4) under bars 1-56; quiet swung organ eighth-note chord-tone arpeggio in full sections.
Drums, swung: four-on-the-floor kick, off-beat-accented eighth-note closed hats, open hat on the and-of-2 and and-of-4, snare with clap on 2 and 4 from bar 9, ride in 41-56, tom fills in bars 16, 36, 56, crash at 41. Sparse conga cell in full sections, no shaker.
Sub bass from bar 9: short notes on the swung and-of-2 and beat 3, a one-beat note on beat 4; every second bar it drops an octave to F#1.
Form: 1-8 intro (pad, hats; kick from bar 5), 9-36 full, 37-40 break: piano and pad alone in 37-38, sub alone in 39-40, 41-56 full with ride, 57-64 drums and sub only.
Smooth and shadowed. No lead, no vocals, DJ-friendly intro/outro.
```

## dh09-wet-asphalt-v3
**Style**
`deep house, 120 BPM, C# minor, punchy kick, snare and clap on 2 and 4, swung off-beat open hats, syncopated finger bass, electric piano minor eleventh and half-diminished chords, organ arpeggio, warm pad, instrumental`

**Description**
```
Instrumental deep house at 120 BPM in C# minor. Loop: C#m11 and G#m7b5, two bars each; its D natural darkens the loop.
Drums: punchy four-on-the-floor kick, snare and clap on 2 and 4 from bar 9, swung closed-hat eighths, swung open hats on the and-of-2 and and-of-4. Tom fills at bars 16, 36, 56. Swung congas from bar 13.
Finger bass from bar 9: syncopated pushes ahead of beats 3 and 1, with a short fifth (G#1) under C#m11.
Electric piano from bar 9: a held chord on beat 2 and a short chord on the and-of-4 anticipating the next chord, sustain pedal.
Three-voice pad from bar 1, tonic only in the intro.
Tonewheel organ eighth-note arpeggio G#4-B4-D#5 / G#4-B4-D5 in 17-36 and 41-56.
Structure: 1-8 intro (pad and hats, kick from bar 5), 9-36 full, 37-40 break that rebuilds one element per bar (piano and pad, hats, bass, kick), 41-56 full with ride and crash, 57-64 drums and bass only.
Wet, after-midnight. No lead, no vocals, DJ-friendly intro/outro.
```

## dh10-underpass-velour-v3
**Style**
`deep house, 121 BPM, C# minor, Tough Kit, sub bass, held electric piano, low pad, enclosed and velvety, instrumental`

**Description**
```
Deep house at 121 BPM, C# minor: C#m11 3 bars, G#m9 1 bar.
Pulse Bass from bar 9: short tonics on &1/&3 alternate with longer lower fifth on &2; tonic at DJ edges.
Tough Kit: four-floor kick from bar 5; soft on-beat closed hats, stronger &1/&3; open hats &2/&4. Snare+clap on 2/4 from bar 9. Two tom hits end bars 16/36/56.
Low Classic Pad C#-G#-D# from bar 1. A/A2: held full-bar electric piano, pedal released each bar; eighth-note electric-piano Tex cycles current chord tones in one octave; SoCal congas, 3 hits/2 bars clear of kick/open hats, no shaker.
64 bars: 1-8 pad+hats intro, kick at 5; 9-36 A; 37-40 break: kick, snare+clap and keys only; hats, bass, pad, Tex and Perc drop; 41-56 A2: quarter-note ride replaces on-beat closed hats, off-beats stay, crash at 41; 57-64 drums+bass only.
No lead, no vocals, DJ-friendly intro/outro.
```

## dh11-cinder-arcade-v3
**Style**
`deep house, 121 BPM, G# minor, Tough Kit drums, accented kick, off-beat open hats, snare with clap, congas, soft pad, soft grand piano minor ninth stabs and one held lydian chord, electric piano arpeggio, tight sub bass, tense but quiet, instrumental`

**Description**
```
Cinder Arcade: 121 BPM, G# minor. G#m9 for three bars and Emaj7(#11)/G# for one bar, G#1 held under both; two voices step down in the fourth bar.
Soft grand piano: short chords on the and-of-1 and and-of-3 for three bars, one long chord from the and-of-1 in the fourth.
Soft pad (G#2, D#3, A#3) under bars 1-56; quiet electric piano eighth-note chord-tone arpeggio in full sections.
Drums: four-on-the-floor kick, off-beat-accented eighth-note closed hats, open hat on the and-of-2 and and-of-4, snare with clap on 2 and 4 from bar 9, ride in 41-56, tom fills in bars 16, 36, 56, crash at 41. Sparse conga cell in full sections, no shaker.
Sub bass on G#1 only from bar 9: short one, sixteenth pickup, 1.2-beat note from the and-of-3; the second bar ends on a short and-of-4.
Form: 1-8 intro (pad, hats; kick from bar 5), 9-36 full, 37-40 break: kick on beats 1 and 3 plus sub only, 41-56 full with ride, 57-64 drums and sub only.
Tense but quiet. No lead, no vocals, DJ-friendly intro/outro.
```

## dh12-tarnished-blue-v3
**Style**
`deep house, 121 BPM, G# minor, punchy four-on-the-floor kick, snare and clap on 2 and 4, off-beat open hats, off-beat sub bass, electric piano minor ninth and thirteenth chords, organ arpeggio, warm pad, instrumental`

**Description**
```
Instrumental deep house at 121 BPM in G# minor. Loop: G#m9 and B13, two bars each; D# and F# are shared, an A natural on top of the second.
Drums: punchy four-on-the-floor kick, snare and clap on 2 and 4 from bar 9, closed-hat eighths, open hats on the and-of-2 and and-of-4. Tom fills at bars 16, 36, 56. Congas from bar 13.
Sub bass from bar 9, all off the beat: short notes on the ands, the fifth (F#1) under B13.
Electric piano from bar 9: a chord on beat 3 and a chord on the and-of-4 held across the bar line, every bar, sustain pedal.
Three-voice pad from bar 1, tonic only in the intro.
Tonewheel organ eighth-note arpeggio F#4-A#4-B4-D#5 / F#4-A4-B4-D#5 in 17-36 and 41-56.
Structure: 1-8 intro (pad and hats, kick from bar 5), 9-36 full, 37-40 break where the kick turns into a broken two-step and everything else stays, 41-56 full with ride and crash, 57-64 drums and bass only.
Smoky, rising toward the peak. No lead, no vocals, DJ-friendly intro/outro.
```

## dh13-basalt-current-v3
**Style**
`deep house, 122 BPM, Eb minor, Tough Kit, sub bass, sustained organ, low pad, basalt-dark pressure, instrumental`

**Description**
```
Deep house at 122 BPM, Eb minor: Ebm9 / Abm6, 2 bars each.
Pulse Bass from bar 9: tonic beat 1, short lower fifth &3; next bar tonic &1/beat 3; tonic at DJ edges.
Tough Kit: four-floor kick from bar 5; soft on-beat closed hats, stronger &1/&3; open hats &2/&4. Snare+clap on 2/4 from bar 9. Two tom hits end bars 16/36/56.
Low Classic Pad Eb-Bb-F from bar 1. A/A2: held full-bar Tonewheel Organ, pedal released each bar; eighth-note electric-piano Tex cycles current chord tones in one octave; SoCal congas, 3 hits/2 bars clear of kick/open hats, no shaker.
64 bars: 1-8 pad+hats intro, kick at 5; 9-36 A; 37-40 break: 37/39 only kick, snare+clap, bass; 38/40 only hats, snare+clap, organ; pad/Tex/Perc drop; 41-56 A2: quarter-note ride replaces on-beat closed hats, off-beats stay, crash at 41; 57-64 drums+bass only.
No lead, no vocals, DJ-friendly intro/outro.
```

## dh14-iron-tide-v3
**Style**
`deep house peak without brightness, 122 BPM, Eb minor dorian, Tough Kit drums, accented kick, off-beat open hats, snare with clap, congas, soft pad, tonewheel organ minor ninth and half-diminished stabs, electric piano arpeggio, syncopated sub bass, dense low-mids, instrumental`

**Description**
```
Iron Tide: 122 BPM, Eb minor dorian. Ebm9 and Cm7b5/Eb alternate every bar over an Eb pedal; Db drops to C and F to Eb.
Organ stabs, one beat each: and-of-2 and beat 3 in odd bars, and-of-2 and e-of-3 in even bars.
Soft pad (Eb3, Bb3, F4) under bars 1-56; quiet electric piano eighth-note chord-tone arpeggio in full sections.
Drums: four-on-the-floor kick, off-beat-accented eighth-note closed hats, open hat on the and-of-2 and and-of-4, snare with clap on 2 and 4 from bar 9, ride in 41-56, tom fills in bars 16, 36, 56, crash at 41. Sparse conga cell in full sections, no shaker.
Sub bass from bar 9: the one, a short and-of-2, beat 3; odd bars add a short Ab1 (fifth below) on the and-of-4, even bars hold beat 3 for 1.4 beats.
Form: 1-8 intro (pad, hats; kick from bar 5), 9-36 full, 37-40 break: hats, snare, organ and pad in 37-38, kick and sub only in 39-40, 41-56 full with ride, 57-64 drums and sub only.
Dense in the low-mids, never bright. No lead, no vocals, DJ-friendly intro/outro.
```

## dh15-deep-meridian-v3
**Style**
`peak-time deep house, 122 BPM, B flat minor, punchy four-on-the-floor kick, snare and clap on 2 and 4, off-beat open hats, syncopated sub bass, electric piano minor eleventh and seven-sus chords, organ arpeggio, warm pad, instrumental`

**Description**
```
Instrumental deep house at 122 BPM in B flat minor. Loop: Bbm11 and Ab7sus4, two bars each; only one voice moves, F to G flat.
Drums: punchy four-on-the-floor kick, snare and clap on 2 and 4 from bar 9, closed-hat eighths, open hats on the and-of-2 and and-of-4. Tom fills at bars 16, 36, 56. Congas from bar 13.
Sub bass from bar 9: roots on the one and beat 3 with a ghost before 3, a short note after beat 4.
Electric piano from bar 9: short off-beat stabs and long holds, pushed just after the beat, sustain pedal.
Three-voice pad from bar 1, tonic only in the intro.
Tonewheel organ eighth-note arpeggio F4-Ab4-Db5 / Gb4-Ab4-Db5 in 17-36 and 41-56.
Structure: 1-8 intro (pad and hats, kick from bar 5), 9-36 full, 37-40 break stripping hats at 37, bass at 39, kick at 40, leaving snare, clap, piano and pad, 41-56 full with ride and crash, 57-64 drums and bass only.
Deep, dark, rolling, mid-set. No lead, no vocals, DJ-friendly intro/outro.
```

## dh16-blackwater-fold-v3
**Style**
`deep house, 123 BPM, Bb minor, Tough Kit, sub bass, held organ, low pad, dense blackwater calm, instrumental`

**Description**
```
Deep house at 123 BPM, Bb minor: Bbm9 / Bbm11, 4 bars each, tonic-centered.
Pulse Bass from bar 9: short tonics &1/&3/&4, next bar longer tonic &2.
Tough Kit: four-floor kick from bar 5; soft on-beat closed hats, stronger &1/&3; open hats &2/&4. Snare+clap on 2/4 from bar 9. Two tom hits end bars 16/36/56.
Low Classic Pad Bb-F-C from bar 1. A/A2: held full-bar Tonewheel Organ, pedal released each bar; eighth-note electric-piano Tex cycles current chord tones in one octave; SoCal congas, 3 hits/2 bars clear of kick/open hats, no shaker.
64 bars: 1-8 pad+hats intro, kick at 5; 9-36 A; 37-40 break: 37-38 kick+organ only; 39-40 hats+bass only; snare+clap, pad, Tex and Perc drop; 41-56 A2: quarter-note ride replaces on-beat closed hats, off-beats stay, crash at 41; 57-64 drums+bass only.
No lead, no vocals, DJ-friendly intro/outro.
```

## dh17-coal-harbour-v3
**Style**
`dark deep house peak, 123 BPM, F minor dorian, Tough Kit drums, accented kick, off-beat open hats, snare with clap, congas, soft pad, held electric piano minor ninth and flat-seven major seventh, organ arpeggio, all-off-beat sub bass, heavy below, instrumental`

**Description**
```
Coal Harbour: 123 BPM, F minor dorian. Fm9 and Ebmaj7/F, two bars each, F2 under both; all voices step down into a D-Eb cluster and back.
Electric piano holds a long chord from the and-of-1 every bar; even bars add a short touch on the and-of-4.
Soft pad (F3, C4, G4) under bars 1-56; quiet organ eighth-note chord-tone arpeggio in full sections.
Drums: four-on-the-floor kick, off-beat-accented eighth-note closed hats, open hat on the and-of-2 and and-of-4, snare with clap on 2 and 4 from bar 9, ride in 41-56, tom fills in bars 16, 36, 56, crash at 41. Sparse conga cell in full sections, no shaker.
Sub bass off-beat only from bar 9: four short notes in odd bars; in even bars the and-of-3 note lengthens to 1.4 beats on the fifth below (Bb1).
Form: 1-8 intro (pad, hats; kick from bar 5), 9-36 full, 37-40 break: hats, snare and pad over a whole-note sub drone, no kick, 41-56 full with ride, 57-64 drums and sub only.
Heavy below, empty above. No lead, no vocals, DJ-friendly intro/outro.
```

## dh18-smoke-orchard-v3
**Style**
`dark deep house, 123 BPM, F minor, punchy four-on-the-floor kick, snare and clap on 2 and 4, off-beat open hats, sub bass dropping an octave, tonewheel organ phrygian ninth chords, electric piano arpeggio, warm pad, instrumental`

**Description**
```
Instrumental deep house at 123 BPM in F minor. Loop: Fm9 and Gb9, two bars each; A flat is held while C, E flat and G step down.
Drums: punchy four-on-the-floor kick, snare and clap on 2 and 4 from bar 9, closed-hat eighths, open hats on the and-of-2 and and-of-4. Tom fills at bars 16, 36, 56. Congas from bar 13.
Sub bass from bar 9: a short root on the one, an octave drop on the and-of-2, the fifth on beat 4 of the second bar.
Tonewheel organ from bar 9: held chords from the and-of-2 with short touches on the and-of-4, sustain pedal.
Three-voice pad from bar 1, tonic only in the intro.
Electric piano eighth-note arpeggio Ab4-C5-Eb5-G5 / Ab4-Bb4-Db5-Fb5 in 17-36 and 41-56.
Structure: 1-8 intro (pad and hats, kick from bar 5), 9-36 full, 37-40 break (bass out at 37; from 39 the organ plays alone), 41-56 full with ride and crash, 57-64 drums and bass only.
Dark peak, heavy but not bright. No lead, no vocals, DJ-friendly intro/outro.
```

## dh19-pressure-glass-v3
**Style**
`deep house, 122 BPM, C minor, Tough Kit, low bass, sustained electric piano, low pad, tense smoked glass, instrumental`

**Description**
```
Deep house at 122 BPM, C minor: Cm11 6 bars, Dbmaj7(#11)/C 2 bars over C pedal; no major-key turn.
Simple Foundation bass from bar 9: tonic beat 1/&3, next bar tonic &1 and lower fifth beat 4; tonic at DJ edges.
Tough Kit: four-floor kick from bar 5; soft on-beat closed hats, stronger &1/&3; open hats &2/&4. Snare+clap on 2/4 from bar 9. Two tom hits end bars 16/36/56.
Low Classic Pad C-G-D from bar 1. A/A2: held full-bar electric piano, pedal released each bar; eighth-note electric-piano Tex cycles current chord tones in one octave; SoCal congas, 3 hits/2 bars clear of kick/open hats, no shaker.
64 bars: 1-8 pad+hats intro, kick at 5; 9-36 A; 37-40 break: kick, bass and keys only; hats, snare+clap, pad, Tex and Perc drop; 41-56 A2: quarter-note ride replaces on-beat closed hats, off-beats stay, crash at 41; 57-64 drums+bass only.
No lead, no vocals, DJ-friendly intro/outro.
```

## dh20-wet-granite-v3
**Style**
`deep house end of peak, 122 BPM, C minor, Tough Kit drums, accented kick, off-beat open hats, snare with clap, congas, soft pad, held soft grand piano minor ninth and flat-six major seventh, electric piano arpeggio, sub bass with a fifth below, settling, instrumental`

**Description**
```
Wet Granite: 122 BPM, C minor, closing the peak. Cm9 for five bars and Abmaj7/C for three bars, C2 under both; Bb falls to Ab and D to C.
Soft grand piano holds from the one in cycle bars 1-5; bars 6-8 get a short touch on the one, then a hold from beat 2.
Soft pad (C3, G3, D4) under bars 1-56; quiet electric piano eighth-note chord-tone arpeggio in full sections.
Drums: four-on-the-floor kick, off-beat-accented eighth-note closed hats, open hat on the and-of-2 and and-of-4, snare with clap on 2 and 4 from bar 9, ride in 41-56, tom fills in bars 16, 36, 56, crash at 41. Sparse conga cell in full sections, no shaker.
Sub bass from bar 9: a 1.5-beat note on the one, a short and-of-3 and a note on beat 4; every second bar the beat-4 note drops to the fifth below (F1).
Form: 1-8 intro (pad, hats; kick from bar 5), 9-36 full, 37-40 break: snare, clap and pad only, 41-56 full with ride, 57-64 drums and sub only.
Settling, not lifting. No lead, no vocals, DJ-friendly intro/outro.
```

## dh21-slow-orbit-v3
**Style**
`drifting deep house, 121 BPM, G minor, punchy kick, snare and clap on 2 and 4, swung off-beat open hats, long sub bass, held electric piano ninth chords a tritone apart, organ arpeggio, lush pad, instrumental`

**Description**
```
Instrumental deep house at 121 BPM in G minor. Loop: Gm9 and Dbmaj9, two bars each, a tritone apart with F held on top.
Drums: punchy four-on-the-floor kick, snare and clap on 2 and 4 from bar 9, swung closed-hat eighths, swung open hats on the and-of-2 and and-of-4. Tom fills at bars 16, 36, 56. Sparse swung congas from bar 13.
Sub bass from bar 9: a long root held across most of two bars, then short notes on beats 3 and 4 (Ab1 under Dbmaj9).
Electric piano from bar 9: whole-bar chords struck every bar, softer on the second, sustain pedal.
Lush three-voice pad from bar 1, a little forward, tonic only in the intro.
Tonewheel organ eighth-note arpeggio F4-A4-D5 / F4-Ab4-Eb5 in 17-36 and 41-56.
Structure: 1-8 intro (pad and hats, kick from bar 5), 9-36 full, 37-40 break with only sub bass and pad (drums and piano out), 41-56 full with ride and crash, 57-64 drums and bass only.
Floating, after the peak. No lead, no vocals, DJ-friendly intro/outro.
```

## dh22-drift-archive-v3
**Style**
`deep house, 121 BPM, G minor, Tough Kit, sub bass, held electric piano, low pad, drifting and archival, instrumental`

**Description**
```
Deep house at 121 BPM, G minor: Gm9 / F6/9/G, 4 bars each, G-centered.
Pulse Bass from bar 9, 4-bar cell: long tonic beat 2; empty; long tonic &1; short lower fifth &4; tonic at DJ edges.
Tough Kit: four-floor kick from bar 5; soft on-beat closed hats, stronger &1/&3; open hats &2/&4. Snare+clap on 2/4 from bar 9. Two tom hits end bars 16/36/56.
Low Classic Pad G-D-A from bar 1. A/A2: held full-bar electric piano, pedal released each bar; eighth-note electric-piano Tex cycles current chord tones in one octave; SoCal congas, 3 hits/2 bars clear of kick/open hats, no shaker.
64 bars: 1-8 pad+hats intro, kick at 5; 9-36 A; 37-40 break: held keys+pad only; bass, drums, Tex and Perc drop; 41-56 A2: quarter-note ride replaces on-beat closed hats, off-beats stay, crash at 41; 57-64 drums+bass only.
No lead, no vocals, DJ-friendly intro/outro.
```

## dh23-paper-lantern-v3
**Style**
`drifting deep house, 120 BPM, D minor, Tough Kit drums, accented kick, swung off-beat open hats, snare with clap, soft pad, held electric piano minor ninth and flat-three major ninth, organ arpeggio, sparse sub bass, soft-lit and slow, instrumental`

**Description**
```
Paper Lantern: 120 BPM, D minor. Dm9 and Fmaj9/D, four bars each, D2 held under both; F falls to E, A to G, top E rises to F.
Electric piano holds from the one and beat 3 in odd bars, a long chord from the swung and-of-1 in even bars, a short touch on beat 4 of bar 8.
Soft pad (D3, A3, E4) under bars 1-56; quiet swung organ eighth-note chord-tone arpeggio in full sections.
Drums, swung: four-on-the-floor kick, off-beat-accented eighth-note closed hats, open hat on the and-of-2 and and-of-4, snare with clap on 2 and 4 from bar 9, ride in 41-56, tom fills in bars 16, 36, 56, crash at 41. No shaker or congas.
Sub bass from bar 9: short beat 2, 1.4-beat note from the swung and-of-3; every second bar swaps the long note for a short G1 (fifth below) on the swung and-of-4.
Form: 1-8 intro (pad, hats; kick from bar 5), 9-36 full, 37-40 break: closed hats, open hats and pad only, 41-56 full with ride, 57-64 drums and sub only.
Soft-lit and slow. No lead, no vocals, DJ-friendly intro/outro.
```

## dh24-umber-lane-v3
**Style**
`deep house, 120 BPM, D minor, punchy four-on-the-floor kick, snare and clap on 2 and 4, off-beat open hats, syncopated finger bass, held grand piano minor eleventh chords, organ arpeggio, lush pad, instrumental`

**Description**
```
Instrumental deep house at 120 BPM in D minor. Loop: Dm11 and Dm11b5, two bars each over D; only A falls to A flat, so the tonic half-darkens.
Drums: punchy four-on-the-floor kick, snare and clap on 2 and 4 from bar 9, closed-hat eighths, open hats on the and-of-2 and and-of-4. Tom fills at bars 16, 36, 56. Congas from bar 13.
Finger bass from bar 9: syncopated notes just after beats 1 and 3, with the fifth (A1) on beat 4 of the second bar.
Grand piano from bar 9: a chord on the one, then a chord on beat 3 held through the whole second bar, sustain pedal.
Three-voice pad from bar 1, tonic only in the intro.
Tonewheel organ eighth-note arpeggio F4-A4-C5 / F4-Ab4-C5 in 17-36 and 41-56.
Structure: 1-8 intro (pad and hats, kick from bar 5), 9-36 full, 37-40 break with only kick and sub (hats, snare, clap, piano and pad out), 41-56 full with ride and crash, 57-64 drums and bass only.
Warm brown, unhurried. No lead, no vocals, DJ-friendly intro/outro.
```

## dh25-dim-stairwell-v3
**Style**
`deep house, 119 BPM, A minor, Tough Kit, low bass, sustained electric piano, low pad, dim and cooling, instrumental`

**Description**
```
Deep house at 119 BPM, A minor: Am9 1 bar, Dm7/A 3 bars, A-centered.
Simple Foundation bass from bar 9, 4-bar cell: tonic &3; shorter tonic &1; empty; longer tonic &2.
Tough Kit: four-floor kick from bar 5; soft on-beat closed hats, stronger &1/&3; open hats &2/&4. Snare+clap on 2/4 from bar 9. Two tom hits end bars 16/36/56.
Low Classic Pad A-E-B from bar 1. A/A2: held full-bar electric piano, pedal released each bar; eighth-note electric-piano Tex cycles current chord tones in one octave; SoCal congas, 3 hits/2 bars clear of kick/open hats, no shaker.
64 bars: 1-8 pad+hats intro, kick at 5; 9-36 A; 37-40 break: sparse bass+snare+clap only; kick, hats, keys, pad, Tex and Perc drop; 41-56 A2: quarter-note ride replaces on-beat closed hats, off-beats stay, crash at 41; 57-64 drums+bass only.
No lead, no vocals, DJ-friendly intro/outro.
```

## dh26-dusk-ledger-v3
**Style**
`cooling deep house, 119 BPM, A minor, Tough Kit drums, accented kick, off-beat open hats, snare with clap, soft pad, electric piano minor ninth and six-nine stabs, organ arpeggio, four-bar sub cell with a rest, thinning toward the close, instrumental`

**Description**
```
Dusk Ledger: 119 BPM, A minor. Am9 for six bars and C6/9/A for two bars, A1 held underneath; only B falls to A and C rises to D.
Electric piano plays two stabs per bar: and-of-2 and a short and-of-4 in cycle bars 1-6, then slightly longer stabs on the and-of-1 and and-of-3 in bars 7-8.
Soft pad (A2, E3, B3) under bars 1-56; quiet organ eighth-note chord-tone arpeggio in full sections.
Drums: four-on-the-floor kick, off-beat-accented eighth-note closed hats, open hat on the and-of-2 and and-of-4, snare with clap on 2 and 4 from bar 9, ride in 41-56, tom fills in bars 16, 36, 56, crash at 41. No shaker or congas.
Sub bass on A1 only from bar 9, a four-bar cell: one-beat note on the one plus a short and-of-4, a 1.4-beat note from the and-of-3, the first bar again, then a bar of rest.
Form: 1-8 intro (pad, hats; kick from bar 5), 9-36 full, 37-40 break: kick alone, 41-56 full with ride, 57-64 drums and sub only.
Thinning toward the close. No lead, no vocals, DJ-friendly intro/outro.
```

## dh27-quiet-pier-v3
**Style**
`chill deep house cooldown, 118 BPM, D minor, punchy four-on-the-floor kick, snare and clap on 2 and 4, off-beat open hats, sparse sub bass, electric piano minor ninth and sus-two chords, organ arpeggio, lush pad, instrumental`

**Description**
```
Instrumental deep house at 118 BPM in D minor. Loop: Dm9 and Fsus2, two bars each; only A moves, down to G; the second chord has no third.
Drums: punchy four-on-the-floor kick, snare and clap on 2 and 4 from bar 9, closed-hat eighths, open hats on the and-of-2 and and-of-4. Tom fills at bars 16, 36, 56. Very sparse congas from bar 13.
Sub bass from bar 9 in a four-bar cell: a long D2, an empty bar, then F1 on the and-of-2 and the and-of-4.
Electric piano from bar 9: the first bar of each chord held whole, the second struck on beats 1 and 3, sustain pedal.
Three-voice pad from bar 1, tonic only in the intro.
Tonewheel organ eighth-note arpeggio F4-A4-C5 / F4-G4-C5 in 17-36 and 41-56.
Structure: 1-8 intro (pad and hats, kick from bar 5), 9-36 full, 37-40 break with only snare, clap and piano (kick, hats, bass and pad out), 41-56 full with ride and crash, 57-64 drums and bass only.
Cooling down, quiet water. No lead, no vocals, DJ-friendly intro/outro.
```

## dh28-drowned-linen-v3
**Style**
`deep house, 118 BPM, D minor, Tough Kit, sub bass, sustained piano, low pad, drowned and hushed, instrumental`

**Description**
```
Deep house at 118 BPM, D minor: Dm11 / Cm9/D, 4 bars each, D-centered.
Pulse Bass from bar 9, 4-bar cell: long tonic beat 1; two empty bars; short lower fifth &3; tonic at DJ edges.
Tough Kit: four-floor kick from bar 5; soft on-beat closed hats, stronger &1/&3; open hats &2/&4. Snare+clap on 2/4 from bar 9. Two tom hits end bars 16/36/56.
Low Classic Pad D-A-E from bar 1. A/A2: held full-bar Studio Grand piano, pedal released each bar; eighth-note electric-piano Tex cycles current chord tones in one octave; SoCal congas, 3 hits/2 bars clear of kick/open hats, no shaker.
64 bars: 1-8 pad+hats intro, kick at 5; 9-36 A; 37-40 break: 37-38 total silence after releases; 39-40 piano+sparse bass only, next bass note at 40; drums/pad/Tex/Perc drop; 41-56 A2: quarter-note ride replaces on-beat closed hats, off-beats stay, crash at 41; 57-64 drums+bass only.
No lead, no vocals, DJ-friendly intro/outro.
```

## dh29-last-corridor-v3
**Style**
`chill deep house pre-closer, 117 BPM, A minor with one dorian touch, Tough Kit drums, accented kick, off-beat open hats, snare with clap, soft pad, held soft grand piano minor eleventh shell, electric piano arpeggio, long sparse tonic sub, leaving room for the closer, instrumental`

**Description**
```
Last Corridor: 117 BPM, A minor, pre-closer. Am11 shell for seven bars, Em11/A for one, A1 held underneath; in bar 8 C falls to A and E rises to F#, one dorian touch.
Soft grand piano holds a long chord from the and-of-1 every bar, the whole bar from the one in bar 8.
Soft pad (A2, E3, B3) under bars 1-56; quiet electric piano eighth-note chord-tone arpeggio in full sections.
Drums: four-on-the-floor kick, off-beat-accented eighth-note closed hats, open hat on the and-of-2 and and-of-4, snare with clap on 2 and 4 from bar 9, ride in 41-56, tom fills in bars 16, 36, 56, crash at 41. No shaker or congas.
Sub bass on A1 only from bar 9, a four-bar cell: a whole-bar note, a 1.5-beat note on the one, a bar of rest, then a 1.9-beat note from beat 3.
Form: 1-8 intro (pad, hats; kick from bar 5), 9-36 full, 37-40 break: hats, snare, clap and pad only, 41-56 full with ride, 57-64 drums and sub only.
Leave the closing to the final slot. No lead, no vocals, DJ-friendly intro/outro.
```

## dh30-house-lights-v3
**Style**
`chill deep house closer, 116 BPM, A minor, punchy four-on-the-floor kick, snare and clap on 2 and 4, off-beat open hats, short sub bass, grand piano minor ninth and sus-two chords, electric piano arpeggio, lush pad, long outro, instrumental`

**Description**
```
Instrumental deep house at 116 BPM in A minor, 72 bars. Loop: Am9 and Esus2, two bars each; G moves to F#; the second chord has no third.
Drums: punchy four-on-the-floor kick, snare and clap on 2 and 4 from bar 9, closed-hat eighths, open hats on the and-of-2 and and-of-4. Tom fills at bars 16, 36, 56. Sparse congas from bar 13.
Sub bass from bar 9: a short root on the one and the and-of-3, then an empty bar.
Grand piano from bar 9: a chord held through the first bar, then a chord on the one and a short one on the and-of-3, sustain pedal.
Three-voice pad from bar 1, tonic in the intro, tonic tail to bar 60.
Electric piano eighth-note arpeggio E4-G4-B4 / E4-F#4-B4 in 17-36 and 41-56.
Structure: 1-8 intro (pad and hats, kick from bar 5), 9-36 full, 37-40 break: kick, snare, clap, bass out, 41-56 full with ride and crash, 57-72 outro: snare/clap out at 61, hats at 65, bass at 69, lone kick to 72.
Lights up, set ends. No lead, no vocals, DJ-friendly intro/outro.
```

---

# 2026-10-21 Deep House Set 96마디판 (v3l) — 곡별 Suno 프롬프트 (슬롯 순)

Cover 업로드 시 `{sid}-v3l.wav`(~3:10, 클로저 104마디 ~3:35) 와 함께 쓴다. 구조 1–8 intro / 9–48 A / 49–56 break / 57–88 A2(57 크래시·라이드) / 89–96 outro(클로저 89–104). 모든 블록 Description ≤ 1,000자·Style ≤ 300자 측정 완료.

## dh01-unlit-threshold-v3l
**Style**
`deep house, 117 BPM, A minor, Tough Kit, sub bass, held electric piano, low pad, unlit and spacious, instrumental`

**Description**
```
Deep house at 117 BPM, A minor: static rootless Am9, no changes.
Pulse Bass from bar 9: long A on &1 every other bar, alternate bar empty.
Tough Kit: four-floor kick from bar 5; soft on-beat closed hats, stronger &1/&3; open hats &2/&4. Snare+clap on 2/4 from bar 17. Two tom hits end bars 16/48/88.
Low Classic Pad A-E-B from bar 1. A/A2: held full-bar electric piano, pedal released each bar; eighth-note electric-piano Tex cycles C-G-B in one octave; SoCal congas, 3 hits/2 bars clear of kick/open hats, no shaker.
96 bars: 1-8 pad+hats intro, kick at 5; 9-48 A; 49-56 break: only sparse bass; drums, keys, pad, Tex and Perc drop; 57-88 A2: quarter-note ride replaces on-beat closed hats, off-beats stay, crash at 57; 89-96 drums+bass only.
No lead, no vocals, DJ-friendly intro/outro.
```

## dh02-ash-corridor-v3l
**Style**
`chill deep house, 117 BPM, A minor, Tough Kit drums, accented kick, off-beat open hats, snare with clap, soft three-note pad, held electric piano minor ninth, organ arpeggio, sub bass, dim and unhurried, instrumental`

**Description**
```
Ash Corridor: 117 BPM, A minor. Am9 for four bars, Bm7b5/A for four bars over an A pedal; three inner voices step up one note and back.
Electric piano holds each chord for the whole bar, with one short touch on the and-of-4 in the last bar of each chord.
Soft pad (A2, E3, B3) under bars 1-88; quiet organ eighth-note chord-tone arpeggio in full sections.
Drums: four-on-the-floor kick, off-beat-accented eighth-note closed hats, open hat on the and-of-2 and and-of-4, snare with clap on 2 and 4 from bar 9, ride in 57-88, tom fills in bars 16, 48, 88, crash at 57. No shaker or congas.
Sub bass on A1 only from bar 9: three beats on the one, then a 1.75-beat note from beat 3 of the next bar.
Form: 1-8 intro (pad, hats; kick from bar 5), 9-48 full, 49-56 break: hats and pad only, sub returns in 53-56, 57-88 full with ride, 89-96 drums and sub only.
Dim, slow and unhurried. No lead, no vocals, DJ-friendly intro/outro.
```

## dh03-cistern-hum-v3l
**Style**
`chill deep house, 118 BPM, E minor, punchy four-on-the-floor kick, snare and clap on 2 and 4, off-beat open hats, sub bass on an E pedal, held electric piano ninth chords, organ arpeggio, warm pad, early-set opener, instrumental`

**Description**
```
Instrumental deep house at 118 BPM in E minor. Loop: Em9 and A9sus4/E, two bars each, over an E pedal; only two voices step down, B to A and F# to E.
Drums: punchy four-on-the-floor kick, snare and clap on 2 and 4 from bar 9, closed-hat eighths, open hats on the and-of-2 and and-of-4. Tom fills at bars 16, 48, 88. Sparse congas from bar 13.
Sub bass from bar 9: a long E2 on the one, then a short B1 on the and-of-3 of the next bar.
Electric piano from bar 9: a short chord on the one and a held chord that rings into the second bar, sustain pedal.
Soft three-voice pad from bar 1, tonic only in the intro.
Tonewheel organ eighth-note arpeggio G4-B4-D5 / G4-A4-D5 in 17-48 and 57-88.
Structure: 1-8 intro (pad and hats, kick from bar 5), 9-48 full, 49-56 break with the kick on beat 1 only and the bass out, 57-88 full with ride and crash, 89-96 drums and bass only.
Dark, patient, early in the set. No lead, no vocals, DJ-friendly intro/outro.
```

## dh04-moss-circuit-v3l
**Style**
`deep house, 118 BPM, E minor, Tough Kit, sub bass, sustained electric piano, low pad, mossy and restrained, instrumental`

**Description**
```
Deep house at 118 BPM, E minor: Em9 6 bars, Em6/9 2 bars; Dorian shade.
Pulse Bass from bar 9: long E on beat 1 alternates with short lower fifth on &3; tonic at DJ edges.
Tough Kit: four-floor kick from bar 5; soft on-beat closed hats, stronger &1/&3; open hats &2/&4. Snare+clap on 2/4 from bar 9. Two tom hits end bars 16/48/88.
Low Classic Pad E-B-F# from bar 1. A/A2: held full-bar electric piano, pedal released each bar; eighth-note electric-piano Tex cycles current chord tones in one octave; SoCal congas, 3 hits/2 bars clear of kick/open hats, no shaker.
96 bars: 1-8 pad+hats intro, kick at 5; 9-48 A; 49-56 break: held keys only; bass, drums, pad, Tex and Perc drop; 57-88 A2: quarter-note ride replaces on-beat closed hats, off-beats stay, crash at 57; 89-96 drums+bass only.
No lead, no vocals, DJ-friendly intro/outro.
```

## dh05-tin-lantern-v3l
**Style**
`deep dub house, 119 BPM, B minor dorian, Tough Kit drums, accented kick, off-beat open hats, snare with clap, congas, soft pad, tonewheel organ dub stabs, electric piano arpeggio, pushed sub bass, warm and low, instrumental`

**Description**
```
Tin Lantern: 119 BPM, B minor dorian. Bm9 and Dmaj7(#11)/B alternate every bar over a B pedal; only one voice moves, A down to G#.
Tonewheel organ dub stabs, about one beat each: and-of-1 and a-of-3 in odd bars, and-of-2 and beat 4 in even bars.
Soft pad (B2, F#3, C#4) under bars 1-88; quiet electric piano eighth-note chord-tone arpeggio in full sections.
Drums: four-on-the-floor kick, off-beat-accented eighth-note closed hats, open hat on the and-of-2 and and-of-4, snare with clap on 2 and 4 from bar 9, ride in 57-88, tom fills in bars 16, 48, 88, crash at 57. Sparse conga cell in full sections, no shaker.
Sub bass from bar 9: pickup on the and-of-1 into a 1.4-beat note on beat 2; every second bar the long note drops to the fifth below (E1).
Form: 1-8 intro (pad, hats; kick from bar 5), 9-48 full, 49-56 break: kick, hats, organ and pad only, 57-88 full with ride, 89-96 drums and sub only.
Warm, low and dubby. No lead, no vocals, DJ-friendly intro/outro.
```

## dh06-chalk-river-v3l
**Style**
`deep house, 119 BPM, B minor, punchy four-on-the-floor kick, snare and clap on 2 and 4, off-beat open hats, short sub bass on 2 and 4, tonewheel organ ninth chords, electric piano arpeggio, warm pad, instrumental`

**Description**
```
Instrumental deep house at 119 BPM in B minor. Loop: Bm9 and G9, two bars each; D and A are held while F# falls to F and C# to B.
Drums: punchy four-on-the-floor kick, snare and clap on 2 and 4 from bar 9, closed-hat eighths, open hats on the and-of-2 and and-of-4. Tom fills at bars 16, 48, 88. Congas from bar 13.
Sub bass from bar 9: short roots on beats 2 and 4 with the snare, dipping to the fifth (F#1) once every four bars.
Tonewheel organ from bar 9: a long chord on the one and a short chord on beat 4, every bar.
Three-voice pad from bar 1, tonic only in the intro.
Electric piano eighth-note arpeggio D4-F#4-A4-C#5 / D4-F4-A4-B4 in 17-48 and 57-88.
Structure: 1-8 intro (pad and hats, kick from bar 5), 9-48 full, 49-56 drums-only break (bass, organ and pad out), 57-88 full with ride and crash, 89-96 drums and bass only.
Dry, steady, grey. No lead, no vocals, DJ-friendly intro/outro.
```

## dh07-silt-letters-v3l
**Style**
`deep house, 120 BPM, F# minor, Tough Kit, low bass, held organ, electric-piano texture, silt-dark, instrumental`

**Description**
```
Deep house at 120 BPM, F# minor: F#m9 / Bm11, 2 bars each.
Simple Foundation bass from bar 9: short tonics on &2/&4 alternate with longer tonic on &1.
Tough Kit: four-floor kick from bar 5; soft on-beat closed hats, stronger &1/&3; open hats &2/&4. Snare+clap on 2/4 from bar 9. Two tom hits end bars 16/48/88.
Low Classic Pad F#-C#-G# from bar 1. A/A2: held full-bar Tonewheel Organ, pedal released each bar; eighth-note electric-piano Tex cycles current chord tones in one octave; SoCal congas, 3 hits/2 bars clear of kick/open hats, no shaker.
96 bars: 1-8 pad+hats intro, kick at 5; 9-48 A; 49-56 break: bass, closed/open hats and snare+clap only; kick, keys, pad, Tex and Perc drop; 57-88 A2: quarter-note ride replaces on-beat closed hats, off-beats stay, crash at 57; 89-96 drums+bass only.
No lead, no vocals, DJ-friendly intro/outro.
```

## dh08-slate-hallway-v3l
**Style**
`chill deep house, 120 BPM, F# minor dorian, Tough Kit drums, accented kick, swung off-beat open hats, snare with clap, congas, soft pad, held electric piano minor ninth and minor eleventh, organ arpeggio, octave-dropping sub bass, smooth and shadowed, instrumental`

**Description**
```
Slate Hallway: 120 BPM, F# minor dorian. F#m9 and G#m11/F#, two bars each, over an F# pedal; the upper voices slide up a whole step and back.
Electric piano chords on the one and beat 3 in odd bars, on the and-of-1 and swung and-of-3 in even bars.
Soft pad (F#3, C#4, G#4) under bars 1-88; quiet swung organ eighth-note chord-tone arpeggio in full sections.
Drums, swung: four-on-the-floor kick, off-beat-accented eighth-note closed hats, open hat on the and-of-2 and and-of-4, snare with clap on 2 and 4 from bar 9, ride in 57-88, tom fills in bars 16, 48, 88, crash at 57. Sparse conga cell in full sections, no shaker.
Sub bass from bar 9: short notes on the swung and-of-2 and beat 3, a one-beat note on beat 4; every second bar it drops an octave to F#1.
Form: 1-8 intro (pad, hats; kick from bar 5), 9-48 full, 49-56 break: piano and pad alone in 49-52, sub alone in 53-56, 57-88 full with ride, 89-96 drums and sub only.
Smooth and shadowed. No lead, no vocals, DJ-friendly intro/outro.
```

## dh09-wet-asphalt-v3l
**Style**
`deep house, 120 BPM, C# minor, punchy kick, snare and clap on 2 and 4, swung off-beat open hats, syncopated finger bass, electric piano minor eleventh and half-diminished chords, organ arpeggio, warm pad, instrumental`

**Description**
```
Instrumental deep house at 120 BPM in C# minor. Loop: C#m11 and G#m7b5, two bars each; its D natural darkens the loop.
Drums: punchy four-on-the-floor kick, snare and clap on 2 and 4 from bar 9, swung closed-hat eighths, swung open hats on the and-of-2 and and-of-4. Tom fills at bars 16, 48, 88. Swung congas from bar 13.
Finger bass from bar 9: syncopated pushes ahead of beats 3 and 1, with a short fifth (G#1) under C#m11.
Electric piano from bar 9: a held chord on beat 2 and a short chord on the and-of-4 anticipating the next chord, sustain pedal.
Three-voice pad from bar 1, tonic only in the intro.
Tonewheel organ eighth-note arpeggio G#4-B4-D#5 / G#4-B4-D5 in 17-48 and 57-88.
Structure: 1-8 intro (pad and hats, kick from bar 5), 9-48 full, 49-56 break that rebuilds one element every two bars (49 piano and pad, 51 hats, 53 bass, 55 kick), 57-88 full with ride and crash, 89-96 drums and bass only.
Wet, after-midnight. No lead, no vocals, DJ-friendly intro/outro.
```

## dh10-underpass-velour-v3l
**Style**
`deep house, 121 BPM, C# minor, Tough Kit, sub bass, held electric piano, low pad, enclosed and velvety, instrumental`

**Description**
```
Deep house at 121 BPM, C# minor: C#m11 3 bars, G#m9 1 bar.
Pulse Bass from bar 9: short tonics on &1/&3 alternate with longer lower fifth on &2; tonic at DJ edges.
Tough Kit: four-floor kick from bar 5; soft on-beat closed hats, stronger &1/&3; open hats &2/&4. Snare+clap on 2/4 from bar 9. Two tom hits end bars 16/48/88.
Low Classic Pad C#-G#-D# from bar 1. A/A2: held full-bar electric piano, pedal released each bar; eighth-note electric-piano Tex cycles current chord tones in one octave; SoCal congas, 3 hits/2 bars clear of kick/open hats, no shaker.
96 bars: 1-8 pad+hats intro, kick at 5; 9-48 A; 49-56 break: kick, snare+clap and keys only; hats, bass, pad, Tex and Perc drop; 57-88 A2: quarter-note ride replaces on-beat closed hats, off-beats stay, crash at 57; 89-96 drums+bass only.
No lead, no vocals, DJ-friendly intro/outro.
```

## dh11-cinder-arcade-v3l
**Style**
`deep house, 121 BPM, G# minor, Tough Kit drums, accented kick, off-beat open hats, snare with clap, congas, soft pad, soft grand piano minor ninth stabs and one held lydian chord, electric piano arpeggio, tight sub bass, tense but quiet, instrumental`

**Description**
```
Cinder Arcade: 121 BPM, G# minor. G#m9 for three bars and Emaj7(#11)/G# for one bar, G#1 held under both; two voices step down in the fourth bar.
Soft grand piano: short chords on the and-of-1 and and-of-3 for three bars, one long chord from the and-of-1 in the fourth.
Soft pad (G#2, D#3, A#3) under bars 1-88; quiet electric piano eighth-note chord-tone arpeggio in full sections.
Drums: four-on-the-floor kick, off-beat-accented eighth-note closed hats, open hat on the and-of-2 and and-of-4, snare with clap on 2 and 4 from bar 9, ride in 57-88, tom fills in bars 16, 48, 88, crash at 57. Sparse conga cell in full sections, no shaker.
Sub bass on G#1 only from bar 9: short one, sixteenth pickup, 1.2-beat note from the and-of-3; the second bar ends on a short and-of-4.
Form: 1-8 intro (pad, hats; kick from bar 5), 9-48 full, 49-56 break: kick on beats 1 and 3 plus sub only, 57-88 full with ride, 89-96 drums and sub only.
Tense but quiet. No lead, no vocals, DJ-friendly intro/outro.
```

## dh12-tarnished-blue-v3l
**Style**
`deep house, 121 BPM, G# minor, punchy four-on-the-floor kick, snare and clap on 2 and 4, off-beat open hats, off-beat sub bass, electric piano minor ninth and thirteenth chords, organ arpeggio, warm pad, instrumental`

**Description**
```
Instrumental deep house at 121 BPM in G# minor. Loop: G#m9 and B13, two bars each; D# and F# are shared, an A natural on top of the second.
Drums: punchy four-on-the-floor kick, snare and clap on 2 and 4 from bar 9, closed-hat eighths, open hats on the and-of-2 and and-of-4. Tom fills at bars 16, 48, 88. Congas from bar 13.
Sub bass from bar 9, all off the beat: short notes on the ands, the fifth (F#1) under B13.
Electric piano from bar 9: a chord on beat 3 and a chord on the and-of-4 held across the bar line, every bar, sustain pedal.
Three-voice pad from bar 1, tonic only in the intro.
Tonewheel organ eighth-note arpeggio F#4-A#4-B4-D#5 / F#4-A4-B4-D#5 in 17-48 and 57-88.
Structure: 1-8 intro (pad and hats, kick from bar 5), 9-48 full, 49-56 break where the kick turns into a broken two-step and everything else stays, 57-88 full with ride and crash, 89-96 drums and bass only.
Smoky, rising toward the peak. No lead, no vocals, DJ-friendly intro/outro.
```

## dh13-basalt-current-v3l
**Style**
`deep house, 122 BPM, Eb minor, Tough Kit, sub bass, sustained organ, low pad, basalt-dark pressure, instrumental`

**Description**
```
Deep house at 122 BPM, Eb minor: Ebm9 / Abm6, 2 bars each.
Pulse Bass from bar 9: tonic beat 1, short lower fifth &3; next bar tonic &1/beat 3; tonic at DJ edges.
Tough Kit: four-floor kick from bar 5; soft on-beat closed hats, stronger &1/&3; open hats &2/&4. Snare+clap on 2/4 from bar 9. Two tom hits end bars 16/48/88.
Low Classic Pad Eb-Bb-F from bar 1. A/A2: held full-bar Tonewheel Organ, pedal released each bar; eighth-note electric-piano Tex cycles current chord tones in one octave; SoCal congas, 3 hits/2 bars clear of kick/open hats, no shaker.
96 bars: 1-8 pad+hats intro, kick at 5; 9-48 A; 49-56 break: 49/51/53/55 only kick, snare+clap, bass; 50/52/54/56 only hats, snare+clap, organ; pad/Tex/Perc drop; 57-88 A2: quarter-note ride replaces on-beat closed hats, off-beats stay, crash at 57; 89-96 drums+bass only.
No lead, no vocals, DJ-friendly intro/outro.
```

## dh14-iron-tide-v3l
**Style**
`deep house peak without brightness, 122 BPM, Eb minor dorian, Tough Kit drums, accented kick, off-beat open hats, snare with clap, congas, soft pad, tonewheel organ minor ninth and half-diminished stabs, electric piano arpeggio, syncopated sub bass, dense low-mids, instrumental`

**Description**
```
Iron Tide: 122 BPM, Eb minor dorian. Ebm9 and Cm7b5/Eb alternate every bar over an Eb pedal; Db drops to C and F to Eb.
Organ stabs, one beat each: and-of-2 and beat 3 in odd bars, and-of-2 and e-of-3 in even bars.
Soft pad (Eb3, Bb3, F4) under bars 1-88; quiet electric piano eighth-note chord-tone arpeggio in full sections.
Drums: four-on-the-floor kick, off-beat-accented eighth-note closed hats, open hat on the and-of-2 and and-of-4, snare with clap on 2 and 4 from bar 9, ride in 57-88, tom fills in bars 16, 48, 88, crash at 57. Sparse conga cell in full sections, no shaker.
Sub bass from bar 9: the one, a short and-of-2, beat 3; odd bars add a short Ab1 (fifth below) on the and-of-4, even bars hold beat 3 for 1.4 beats.
Form: 1-8 intro (pad, hats; kick from bar 5), 9-48 full, 49-56 break: hats, snare, organ and pad in 49-52, kick and sub only in 53-56, 57-88 full with ride, 89-96 drums and sub only.
Dense in the low-mids, never bright. No lead, no vocals, DJ-friendly intro/outro.
```

## dh15-deep-meridian-v3l
**Style**
`peak-time deep house, 122 BPM, B flat minor, punchy four-on-the-floor kick, snare and clap on 2 and 4, off-beat open hats, syncopated sub bass, electric piano minor eleventh and seven-sus chords, organ arpeggio, warm pad, instrumental`

**Description**
```
Instrumental deep house at 122 BPM in B flat minor. Loop: Bbm11 and Ab7sus4, two bars each; only one voice moves, F to G flat.
Drums: punchy four-on-the-floor kick, snare and clap on 2 and 4 from bar 9, closed-hat eighths, open hats on the and-of-2 and and-of-4. Tom fills at bars 16, 48, 88. Congas from bar 13.
Sub bass from bar 9: roots on the one and beat 3 with a ghost before 3, a short note after beat 4.
Electric piano from bar 9: short off-beat stabs and long holds, pushed just after the beat, sustain pedal.
Three-voice pad from bar 1, tonic only in the intro.
Tonewheel organ eighth-note arpeggio F4-Ab4-Db5 / Gb4-Ab4-Db5 in 17-48 and 57-88.
Structure: 1-8 intro (pad and hats, kick from bar 5), 9-48 full, 49-56 break stripping hats at 49, bass at 53, kick at 55, leaving snare, clap, piano and pad, 57-88 full with ride and crash, 89-96 drums and bass only.
Deep, dark, rolling, mid-set. No lead, no vocals, DJ-friendly intro/outro.
```

## dh16-blackwater-fold-v3l
**Style**
`deep house, 123 BPM, Bb minor, Tough Kit, sub bass, held organ, low pad, dense blackwater calm, instrumental`

**Description**
```
Deep house at 123 BPM, Bb minor: Bbm9 / Bbm11, 4 bars each, tonic-centered.
Pulse Bass from bar 9: short tonics &1/&3/&4, next bar longer tonic &2.
Tough Kit: four-floor kick from bar 5; soft on-beat closed hats, stronger &1/&3; open hats &2/&4. Snare+clap on 2/4 from bar 9. Two tom hits end bars 16/48/88.
Low Classic Pad Bb-F-C from bar 1. A/A2: held full-bar Tonewheel Organ, pedal released each bar; eighth-note electric-piano Tex cycles current chord tones in one octave; SoCal congas, 3 hits/2 bars clear of kick/open hats, no shaker.
96 bars: 1-8 pad+hats intro, kick at 5; 9-48 A; 49-56 break: 49-52 kick+organ only; 53-56 hats+bass only; snare+clap, pad, Tex and Perc drop; 57-88 A2: quarter-note ride replaces on-beat closed hats, off-beats stay, crash at 57; 89-96 drums+bass only.
No lead, no vocals, DJ-friendly intro/outro.
```

## dh17-coal-harbour-v3l
**Style**
`dark deep house peak, 123 BPM, F minor dorian, Tough Kit drums, accented kick, off-beat open hats, snare with clap, congas, soft pad, held electric piano minor ninth and flat-seven major seventh, organ arpeggio, all-off-beat sub bass, heavy below, instrumental`

**Description**
```
Coal Harbour: 123 BPM, F minor dorian. Fm9 and Ebmaj7/F, two bars each, F2 under both; all voices step down into a D-Eb cluster and back.
Electric piano holds a long chord from the and-of-1 every bar; even bars add a short touch on the and-of-4.
Soft pad (F3, C4, G4) under bars 1-88; quiet organ eighth-note chord-tone arpeggio in full sections.
Drums: four-on-the-floor kick, off-beat-accented eighth-note closed hats, open hat on the and-of-2 and and-of-4, snare with clap on 2 and 4 from bar 9, ride in 57-88, tom fills in bars 16, 48, 88, crash at 57. Sparse conga cell in full sections, no shaker.
Sub bass off-beat only from bar 9: four short notes in odd bars; in even bars the and-of-3 note lengthens to 1.4 beats on the fifth below (Bb1).
Form: 1-8 intro (pad, hats; kick from bar 5), 9-48 full, 49-56 break: hats, snare and pad over a whole-note sub drone, no kick, 57-88 full with ride, 89-96 drums and sub only.
Heavy below, empty above. No lead, no vocals, DJ-friendly intro/outro.
```

## dh18-smoke-orchard-v3l
**Style**
`dark deep house, 123 BPM, F minor, punchy four-on-the-floor kick, snare and clap on 2 and 4, off-beat open hats, sub bass dropping an octave, tonewheel organ phrygian ninth chords, electric piano arpeggio, warm pad, instrumental`

**Description**
```
Instrumental deep house at 123 BPM in F minor. Loop: Fm9 and Gb9, two bars each; A flat is held while C, E flat and G step down.
Drums: punchy four-on-the-floor kick, snare and clap on 2 and 4 from bar 9, closed-hat eighths, open hats on the and-of-2 and and-of-4. Tom fills at bars 16, 48, 88. Congas from bar 13.
Sub bass from bar 9: a short root on the one, an octave drop on the and-of-2, the fifth on beat 4 of the second bar.
Tonewheel organ from bar 9: held chords from the and-of-2 with short touches on the and-of-4, sustain pedal.
Three-voice pad from bar 1, tonic only in the intro.
Electric piano eighth-note arpeggio Ab4-C5-Eb5-G5 / Ab4-Bb4-Db5-Fb5 in 17-48 and 57-88.
Structure: 1-8 intro (pad and hats, kick from bar 5), 9-48 full, 49-56 break (bass out at 49; from 53 the organ plays alone), 57-88 full with ride and crash, 89-96 drums and bass only.
Dark peak, heavy but not bright. No lead, no vocals, DJ-friendly intro/outro.
```

## dh19-pressure-glass-v3l
**Style**
`deep house, 122 BPM, C minor, Tough Kit, low bass, sustained electric piano, low pad, tense smoked glass, instrumental`

**Description**
```
Deep house at 122 BPM, C minor: Cm11 6 bars, Dbmaj7(#11)/C 2 bars over C pedal; no major-key turn.
Simple Foundation bass from bar 9: tonic beat 1/&3, next bar tonic &1 and lower fifth beat 4; tonic at DJ edges.
Tough Kit: four-floor kick from bar 5; soft on-beat closed hats, stronger &1/&3; open hats &2/&4. Snare+clap on 2/4 from bar 9. Two tom hits end bars 16/48/88.
Low Classic Pad C-G-D from bar 1. A/A2: held full-bar electric piano, pedal released each bar; eighth-note electric-piano Tex cycles current chord tones in one octave; SoCal congas, 3 hits/2 bars clear of kick/open hats, no shaker.
96 bars: 1-8 pad+hats intro, kick at 5; 9-48 A; 49-56 break: kick, bass and keys only; hats, snare+clap, pad, Tex and Perc drop; 57-88 A2: quarter-note ride replaces on-beat closed hats, off-beats stay, crash at 57; 89-96 drums+bass only.
No lead, no vocals, DJ-friendly intro/outro.
```

## dh20-wet-granite-v3l
**Style**
`deep house end of peak, 122 BPM, C minor, Tough Kit drums, accented kick, off-beat open hats, snare with clap, congas, soft pad, held soft grand piano minor ninth and flat-six major seventh, electric piano arpeggio, sub bass with a fifth below, settling, instrumental`

**Description**
```
Wet Granite: 122 BPM, C minor, closing the peak. Cm9 for five bars and Abmaj7/C for three bars, C2 under both; Bb falls to Ab and D to C.
Soft grand piano holds from the one in cycle bars 1-5; bars 6-8 get a short touch on the one, then a hold from beat 2.
Soft pad (C3, G3, D4) under bars 1-88; quiet electric piano eighth-note chord-tone arpeggio in full sections.
Drums: four-on-the-floor kick, off-beat-accented eighth-note closed hats, open hat on the and-of-2 and and-of-4, snare with clap on 2 and 4 from bar 9, ride in 57-88, tom fills in bars 16, 48, 88, crash at 57. Sparse conga cell in full sections, no shaker.
Sub bass from bar 9: a 1.5-beat note on the one, a short and-of-3 and a note on beat 4; every second bar the beat-4 note drops to the fifth below (F1).
Form: 1-8 intro (pad, hats; kick from bar 5), 9-48 full, 49-56 break: snare, clap and pad only, 57-88 full with ride, 89-96 drums and sub only.
Settling, not lifting. No lead, no vocals, DJ-friendly intro/outro.
```

## dh21-slow-orbit-v3l
**Style**
`drifting deep house, 121 BPM, G minor, punchy kick, snare and clap on 2 and 4, swung off-beat open hats, long sub bass, held electric piano ninth chords a tritone apart, organ arpeggio, lush pad, instrumental`

**Description**
```
Instrumental deep house at 121 BPM in G minor. Loop: Gm9 and Dbmaj9, two bars each, a tritone apart with F held on top.
Drums: punchy four-on-the-floor kick, snare and clap on 2 and 4 from bar 9, swung closed-hat eighths, swung open hats on the and-of-2 and and-of-4. Tom fills at bars 16, 48, 88. Sparse swung congas from bar 13.
Sub bass from bar 9: a long root held across most of two bars, then short notes on beats 3 and 4 (Ab1 under Dbmaj9).
Electric piano from bar 9: whole-bar chords struck every bar, softer on the second, sustain pedal.
Lush three-voice pad from bar 1, a little forward, tonic only in the intro.
Tonewheel organ eighth-note arpeggio F4-A4-D5 / F4-Ab4-Eb5 in 17-48 and 57-88.
Structure: 1-8 intro (pad and hats, kick from bar 5), 9-48 full, 49-56 break with only sub bass and pad (drums and piano out), 57-88 full with ride and crash, 89-96 drums and bass only.
Floating, after the peak. No lead, no vocals, DJ-friendly intro/outro.
```

## dh22-drift-archive-v3l
**Style**
`deep house, 121 BPM, G minor, Tough Kit, sub bass, held electric piano, low pad, drifting and archival, instrumental`

**Description**
```
Deep house at 121 BPM, G minor: Gm9 / F6/9/G, 4 bars each, G-centered.
Pulse Bass from bar 9, 4-bar cell: long tonic beat 2; empty; long tonic &1; short lower fifth &4; tonic at DJ edges.
Tough Kit: four-floor kick from bar 5; soft on-beat closed hats, stronger &1/&3; open hats &2/&4. Snare+clap on 2/4 from bar 9. Two tom hits end bars 16/48/88.
Low Classic Pad G-D-A from bar 1. A/A2: held full-bar electric piano, pedal released each bar; eighth-note electric-piano Tex cycles current chord tones in one octave; SoCal congas, 3 hits/2 bars clear of kick/open hats, no shaker.
96 bars: 1-8 pad+hats intro, kick at 5; 9-48 A; 49-56 break: held keys+pad only; bass, drums, Tex and Perc drop; 57-88 A2: quarter-note ride replaces on-beat closed hats, off-beats stay, crash at 57; 89-96 drums+bass only.
No lead, no vocals, DJ-friendly intro/outro.
```

## dh23-paper-lantern-v3l
**Style**
`drifting deep house, 120 BPM, D minor, Tough Kit drums, accented kick, swung off-beat open hats, snare with clap, soft pad, held electric piano minor ninth and flat-three major ninth, organ arpeggio, sparse sub bass, soft-lit and slow, instrumental`

**Description**
```
Paper Lantern: 120 BPM, D minor. Dm9 and Fmaj9/D, four bars each, D2 held under both; F falls to E, A to G, top E rises to F.
Electric piano holds from the one and beat 3 in odd bars, a long chord from the swung and-of-1 in even bars, a short touch on beat 4 of bar 8.
Soft pad (D3, A3, E4) under bars 1-88; quiet swung organ eighth-note chord-tone arpeggio in full sections.
Drums, swung: four-on-the-floor kick, off-beat-accented eighth-note closed hats, open hat on the and-of-2 and and-of-4, snare with clap on 2 and 4 from bar 9, ride in 57-88, tom fills in bars 16, 48, 88, crash at 57. No shaker or congas.
Sub bass from bar 9: short beat 2, 1.4-beat note from the swung and-of-3; every second bar swaps the long note for a short G1 (fifth below) on the swung and-of-4.
Form: 1-8 intro (pad, hats; kick from bar 5), 9-48 full, 49-56 break: closed hats, open hats and pad only, 57-88 full with ride, 89-96 drums and sub only.
Soft-lit and slow. No lead, no vocals, DJ-friendly intro/outro.
```

## dh24-umber-lane-v3l
**Style**
`deep house, 120 BPM, D minor, punchy four-on-the-floor kick, snare and clap on 2 and 4, off-beat open hats, syncopated finger bass, held grand piano minor eleventh chords, organ arpeggio, lush pad, instrumental`

**Description**
```
Instrumental deep house at 120 BPM in D minor. Loop: Dm11 and Dm11b5, two bars each over D; only A falls to A flat, so the tonic half-darkens.
Drums: punchy four-on-the-floor kick, snare and clap on 2 and 4 from bar 9, closed-hat eighths, open hats on the and-of-2 and and-of-4. Tom fills at bars 16, 48, 88. Congas from bar 13.
Finger bass from bar 9: syncopated notes just after beats 1 and 3, with the fifth (A1) on beat 4 of the second bar.
Grand piano from bar 9: a chord on the one, then a chord on beat 3 held through the whole second bar, sustain pedal.
Three-voice pad from bar 1, tonic only in the intro.
Tonewheel organ eighth-note arpeggio F4-A4-C5 / F4-Ab4-C5 in 17-48 and 57-88.
Structure: 1-8 intro (pad and hats, kick from bar 5), 9-48 full, 49-56 break with only kick and sub (hats, snare, clap, piano and pad out), 57-88 full with ride and crash, 89-96 drums and bass only.
Warm brown, unhurried. No lead, no vocals, DJ-friendly intro/outro.
```

## dh25-dim-stairwell-v3l
**Style**
`deep house, 119 BPM, A minor, Tough Kit, low bass, sustained electric piano, low pad, dim and cooling, instrumental`

**Description**
```
Deep house at 119 BPM, A minor: Am9 1 bar, Dm7/A 3 bars, A-centered.
Simple Foundation bass from bar 9, 4-bar cell: tonic &3; shorter tonic &1; empty; longer tonic &2.
Tough Kit: four-floor kick from bar 5; soft on-beat closed hats, stronger &1/&3; open hats &2/&4. Snare+clap on 2/4 from bar 9. Two tom hits end bars 16/48/88.
Low Classic Pad A-E-B from bar 1. A/A2: held full-bar electric piano, pedal released each bar; eighth-note electric-piano Tex cycles current chord tones in one octave; SoCal congas, 3 hits/2 bars clear of kick/open hats, no shaker.
96 bars: 1-8 pad+hats intro, kick at 5; 9-48 A; 49-56 break: sparse bass+snare+clap only; kick, hats, keys, pad, Tex and Perc drop; 57-88 A2: quarter-note ride replaces on-beat closed hats, off-beats stay, crash at 57; 89-96 drums+bass only.
No lead, no vocals, DJ-friendly intro/outro.
```

## dh26-dusk-ledger-v3l
**Style**
`cooling deep house, 119 BPM, A minor, Tough Kit drums, accented kick, off-beat open hats, snare with clap, soft pad, electric piano minor ninth and six-nine stabs, organ arpeggio, four-bar sub cell with a rest, thinning toward the close, instrumental`

**Description**
```
Dusk Ledger: 119 BPM, A minor. Am9 for six bars and C6/9/A for two bars, A1 held underneath; only B falls to A and C rises to D.
Electric piano plays two stabs per bar: and-of-2 and a short and-of-4 in cycle bars 1-6, then slightly longer stabs on the and-of-1 and and-of-3 in bars 7-8.
Soft pad (A2, E3, B3) under bars 1-88; quiet organ eighth-note chord-tone arpeggio in full sections.
Drums: four-on-the-floor kick, off-beat-accented eighth-note closed hats, open hat on the and-of-2 and and-of-4, snare with clap on 2 and 4 from bar 9, ride in 57-88, tom fills in bars 16, 48, 88, crash at 57. No shaker or congas.
Sub bass on A1 only from bar 9, a four-bar cell: one-beat note on the one plus a short and-of-4, a 1.4-beat note from the and-of-3, the first bar again, then a bar of rest.
Form: 1-8 intro (pad, hats; kick from bar 5), 9-48 full, 49-56 break: kick alone, 57-88 full with ride, 89-96 drums and sub only.
Thinning toward the close. No lead, no vocals, DJ-friendly intro/outro.
```

## dh27-quiet-pier-v3l
**Style**
`chill deep house cooldown, 118 BPM, D minor, punchy four-on-the-floor kick, snare and clap on 2 and 4, off-beat open hats, sparse sub bass, electric piano minor ninth and sus-two chords, organ arpeggio, lush pad, instrumental`

**Description**
```
Instrumental deep house at 118 BPM in D minor. Loop: Dm9 and Fsus2, two bars each; only A moves, down to G; the second chord has no third.
Drums: punchy four-on-the-floor kick, snare and clap on 2 and 4 from bar 9, closed-hat eighths, open hats on the and-of-2 and and-of-4. Tom fills at bars 16, 48, 88. Very sparse congas from bar 13.
Sub bass from bar 9 in a four-bar cell: a long D2, an empty bar, then F1 on the and-of-2 and the and-of-4.
Electric piano from bar 9: the first bar of each chord held whole, the second struck on beats 1 and 3, sustain pedal.
Three-voice pad from bar 1, tonic only in the intro.
Tonewheel organ eighth-note arpeggio F4-A4-C5 / F4-G4-C5 in 17-48 and 57-88.
Structure: 1-8 intro (pad and hats, kick from bar 5), 9-48 full, 49-56 break with only snare, clap and piano (kick, hats, bass and pad out), 57-88 full with ride and crash, 89-96 drums and bass only.
Cooling down, quiet water. No lead, no vocals, DJ-friendly intro/outro.
```

## dh28-drowned-linen-v3l
**Style**
`deep house, 118 BPM, D minor, Tough Kit, sub bass, sustained piano, low pad, drowned and hushed, instrumental`

**Description**
```
Deep house at 118 BPM, D minor: Dm11 / Cm9/D, 4 bars each, D-centered.
Pulse Bass from bar 9, 4-bar cell: long tonic beat 1; two empty bars; short lower fifth &3; tonic at DJ edges.
Tough Kit: four-floor kick from bar 5; soft on-beat closed hats, stronger &1/&3; open hats &2/&4. Snare+clap on 2/4 from bar 9. Two tom hits end bars 16/48/88.
Low Classic Pad D-A-E from bar 1. A/A2: held full-bar Studio Grand piano, pedal released each bar; eighth-note electric-piano Tex cycles current chord tones in one octave; SoCal congas, 3 hits/2 bars clear of kick/open hats, no shaker.
96 bars: 1-8 pad+hats intro, kick at 5; 9-48 A; 49-56 break: 49-52 total silence after releases; 53-56 piano+sparse bass only, bass notes at 53/56; drums/pad/Tex/Perc drop; 57-88 A2: quarter-note ride replaces on-beat closed hats, off-beats stay, crash at 57; 89-96 drums+bass only.
No lead, no vocals, DJ-friendly intro/outro.
```

## dh29-last-corridor-v3l
**Style**
`chill deep house pre-closer, 117 BPM, A minor with one dorian touch, Tough Kit drums, accented kick, off-beat open hats, snare with clap, soft pad, held soft grand piano minor eleventh shell, electric piano arpeggio, long sparse tonic sub, leaving room for the closer, instrumental`

**Description**
```
Last Corridor: 117 BPM, A minor, pre-closer. Am11 shell for seven bars, Em11/A for one, A1 held underneath; in bar 8 C falls to A and E rises to F#, one dorian touch.
Soft grand piano holds a long chord from the and-of-1 every bar, the whole bar from the one in bar 8.
Soft pad (A2, E3, B3) under bars 1-88; quiet electric piano eighth-note chord-tone arpeggio in full sections.
Drums: four-on-the-floor kick, off-beat-accented eighth-note closed hats, open hat on the and-of-2 and and-of-4, snare with clap on 2 and 4 from bar 9, ride in 57-88, tom fills in bars 16, 48, 88, crash at 57. No shaker or congas.
Sub bass on A1 only from bar 9, a four-bar cell: a whole-bar note, a 1.5-beat note on the one, a bar of rest, then a 1.9-beat note from beat 3.
Form: 1-8 intro (pad, hats; kick from bar 5), 9-48 full, 49-56 break: hats, snare, clap and pad only, 57-88 full with ride, 89-96 drums and sub only.
Leave the closing to the final slot. No lead, no vocals, DJ-friendly intro/outro.
```

## dh30-house-lights-v3l
**Style**
`chill deep house closer, 116 BPM, A minor, punchy four-on-the-floor kick, snare and clap on 2 and 4, off-beat open hats, short sub bass, grand piano minor ninth and sus-two chords, electric piano arpeggio, lush pad, long outro, instrumental`

**Description**
```
Instrumental deep house at 116 BPM in A minor, 104 bars. Loop: Am9 and Esus2, two bars each; G moves to F#; the second chord has no third.
Drums: punchy four-on-the-floor kick, snare and clap on 2 and 4 from bar 9, closed-hat eighths, open hats on the and-of-2 and and-of-4. Tom fills at bars 16, 48, 88. Sparse congas from bar 13.
Sub bass from bar 9: a short root on the one and the and-of-3, then an empty bar.
Grand piano from bar 9: a chord held through the first bar, then a chord on the one and a short one on the and-of-3, sustain pedal.
Three-voice pad from bar 1, tonic in the intro, tonic tail to bar 92.
Electric piano eighth-note arpeggio E4-G4-B4 / E4-F#4-B4 in 17-48 and 57-88.
Structure: 1-8 intro (pad and hats, kick from bar 5), 9-48 full, 49-56 break: kick, snare, clap, bass out, 57-88 full with ride and crash, 89-104 outro: snare/clap out at 93, hats at 97, bass at 101, one last kick on the one of 104.
Lights up, set ends. No lead, no vocals, DJ-friendly intro/outro.
```
