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

## first-light-v1
**Style**
`korean modern rock / indie band anthem, 108 BPM, D major, clean electric guitar melody opening over drums alone, gradually building band, steel-string acoustic strums, string ensemble, uplifting climax, quiet outro, instrumental`

**Description**
```
Instrumental band-style rock at 108 BPM in D major (D–A–Bm–G verses, G–A–F#m–Bm chorus).
Opens with only a clean electric-guitar theme (a rising D–F#–G–A motif) over kick and snare — no hi-hat yet.
Bass and acoustic guitar join, then a higher guitar counter-line answers the theme an octave up while strings sustain underneath.
Low-register verse melody, then the theme returns as the chorus; second chorus adds strings and the high counter-line.
Bridge drops to fingerpicked guitar, pad and a four-on-the-floor kick, with a snare build and a long crash-roll riser
into the climax: full band, open hi-hats, octave strings and both guitar lines together.
Ends quietly — the theme alone over a soft pad, long chords fading to a D resolution.
Feel: dawn breaking, swelling, hopeful — like Delispice "Chau Chau" or the Stellar Blade "Dawn" OST. About 3 minutes 15 seconds.
```

## first-light-v3 (볼레로형, 2026-09-12 투입) — v1 프롬프트는 폐기
**Style** (100자 제한)
`korean modern rock, 108 BPM, clean guitar ostinato riff, bolero-like build, piano lead, instrumental`

**Description** (1000자 제한, 997자)
```
Instrumental Korean modern rock, 108 BPM, D major, built like a bolero on one repeating riff.
A clean electric guitar plays the same syncopated 3+3+2 ostinato, leaping up an octave to a ringing high D pedal note every bar, over a four-chord loop D–A–Bm–G (two bars per chord) for the whole song. The riff never changes; the arrangement builds around it one layer at a time:
guitar and drums alone → bass on steady root notes → acoustic strums → a piano enters as the "singer", a long-breathed melody above the riff → half-time pull-back with a soft pad → strings and ride cymbal → first peak: distorted power chords, open hi-hats, pumping bass → a second quiet pull-back → the final, biggest peak with the piano doubled an octave up → everything falls away to the lone guitar riff and one ringing D chord.
Bass holds root notes only. The riff briefly lifts a fourth higher at the end of some cycles and returns.
Feel: dawn slowly breaking, waves of build and release, never collapsing. About 3:15.
```

메모: Suno 가 "bolero" 를 라틴 볼레로(스페인풍 리듬)로 오해할 수 있음 — Style 에는 `bolero-like gradual build` 로 한정하고, 결과가 라틴풍이면 Style 에서 bolero 단어를 빼고 `Ravel-style additive build` 로 교체.

## Dawn Set v1 — first-light 와 공통 Description 골격, 곡별 Style·키·진행·모티프만 교체
공통 Description (키·진행·모티프 줄만 곡별로 치환)
```
Instrumental band-style rock in {KEY} at {BPM} BPM ({VERSE} verses, {CHORUS} chorus).
Opens with only a clean electric-guitar theme ({MOTIF}) over kick and snare — no hi-hat yet.
Bass and acoustic guitar join, then a higher guitar counter-line answers the theme an octave up while strings sustain underneath.
Low-register verse melody, then the theme returns as the chorus; second chorus adds strings and the high counter-line.
Bridge drops to fingerpicked guitar, pad and a four-on-the-floor kick, with a snare build and a long crash-roll riser
into the climax: full band, open hi-hats, octave strings and both guitar lines together.
Ends quietly — the theme alone over a soft pad, long chords fading to the tonic.
```

**morning-glass-v1 Style**: `korean modern rock, 104 BPM, G major, clean electric guitar sighing descending melody opening over drums alone, gradually building band, steel-string acoustic strums, strings, hopeful morning light, quiet outro, instrumental`
— KEY G major · VERSE G–Em–C–D · CHORUS Em–C–G–D · MOTIF a sighing descending D–B–A–G line that lifts at the end of each phrase

**blue-hour-v1 Style**: `korean modern rock anthem, 112 BPM, E major, clean electric guitar dotted-rhythm octave-leap melody opening over drums alone, gradually building band, acoustic strums, strings, twilight before dawn, quiet outro, instrumental`
— KEY E major · VERSE E–G#m–A–B · CHORUS A–E–B–C#m · MOTIF a dotted "E, E, then a leap up an octave" figure

**paper-kite-v1 Style**: `korean indie rock, 100 BPM, A major, clean electric guitar syncopated off-beat melody opening over drums alone, gradually building band, acoustic strums, strings, light and airy, quiet outro, instrumental`
— KEY A major · VERSE A–D–Bm–E · CHORUS Bm–D–A–E · MOTIF every phrase enters half a beat late, floating over the beat like a kite

**long-bridge-v1 Style**: `korean modern rock, 116 BPM, C major, clean electric guitar repeated-note pedal melody opening over drums alone, gradually building band, acoustic strums, strings, driving and wide, quiet outro, instrumental`
— KEY C major · VERSE Am–F–C–G · CHORUS C–G–Dm–F · MOTIF an insistent repeated G pedal note that finally steps away

## 사용 메모
- Suno 는 스타일 필드가 짧을수록 안정적. Description 은 커스텀 모드의 가사란에 `[Instrumental]` 태그와 함께 넣거나, Cover/Extend 시 참고용.
- 코드 진행·BPM·키는 원곡 SMF 와 동일. Suno 가 키를 무시하는 경우가 많으므로 무드·악기 단어를 우선.
