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
