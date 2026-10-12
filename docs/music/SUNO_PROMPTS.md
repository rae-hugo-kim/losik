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
