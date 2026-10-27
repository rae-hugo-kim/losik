# Suno 투입 프롬프트

각 곡: **Style** = Suno 스타일 필드, **Description** = 커스텀 모드 설명/가사란에 넣는 확장 프롬프트. 오디오 업로드(Cover) 시 해당 WAV 와 함께 사용한다. 모두 instrumental.

> **실투입 기록 (2026-09-19 확인)**: 09-05 의 4곡(star v6 / ghost v4 / chrome **v6** / golden v3)은 아래 **Description 전문이 Style 필드에** 들어갔다 (마침표→쉼표, "3.5 minutes" → "3, 5 minutes" 로 깨짐). Style 100자 제한은 09-12 부터. Cover 가 실제로 받은 텍스트는 Suno 가 오디오에서 자동 생성한 **메타태그**이며, 곡별 원문·대조·판정은 `FEEDBACK_LOG.md` "Suno 완성본 판정" 절, 승격 규칙은 `PROMPT_GUIDELINES.md` §7.
> 4곡 채택본: golden 생성본 1 / star 1 / ghost 1 / chrome 2. 재도전은 채택본 태그의 `[Outro]` 편집부터 (§7.4-2).

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

## Rebetiko 5 버전 (2026-09-18 v1 → 09-19 v2) — SMF `sketches/rebetiko-{1..5}-*-v2.mid`, 엔진 `tools/rebetiko.py`
v1 판정 "그리스가 아니라 이스탄불/알라딘" → v2: 1번 Hitzaz→Minore, 전곡 선율을 코드톤 아르페지오 문법으로, 3번 프레임드럼→붐뱁 킷. 아래 프롬프트는 v2 기준.
Style 100자 이하 / Description 1000자 이하. 1·3번은 보컬 버전 — 가사는 미작성이므로 Suno 가사란에 아래 섹션 태그만 넣고 Suno 자동 가사(그리스어)에 맡기거나, 가사 확정 후 채운다. 2·4·5번은 instrumental.

### rebetiko-1-piraeus (Minore · zeibekiko 9/8 · 66)
**Style**: `1930s Piraeus rebetiko, zeibekiko 9/8, bouzouki, baglamas, raw male vocal, lo-fi, minor key, heavy`

**Description**
```
1930s Piraeus rebetiko in slow zeibekiko 9/8 at about 66 BPM, D minor (Greek "minore": natural minor with a major A chord at cadences — NOT oriental, no augmented seconds).
Opens with a short solo bouzouki taximi (8–10 seconds) outlining the D minor chord — then the guitar enters
with the zeibekiko pattern: bass note, chord, bass, chord, bass, chord, and a heavy weight on the final 3-beat group (2+2+2+3).
Trichordo bouzouki carries the melody doubled an octave below: simple arpeggios of the chord, repeated notes, leaps of a third, tremolo only on the last long note of a phrase. A baglamas shimmers high above in constant tremolo.
A single frame drum, barely there. Raw, unpolished male vocal, singing close to the mic, phrases starting high and falling.
Form: taximi → verse → bouzouki interlude → verse → short coda ending on a long tremolo D. No chorus.
Sound: mono-like, narrow, lo-fi 78rpm warmth, small room. Vamvakaris / Batis lineage. Heavy, slow, solitary. About 2 min.
```
가사란 골격: `[Taximi - bouzouki solo, no drums]` `[Verse 1]` `[Bouzouki interlude]` `[Verse 2]` `[Outro - tremolo]`

### rebetiko-2-hasapiko (Kiourdi · hasapiko 2/4 · 80)
**Style**: `rebetiko hasapiko, twin bouzouki in thirds, walking guitar bass, accordion, melancholy, instrumental`

**Description**
```
Instrumental rebetiko hasapiko in 2/4 at 80 BPM, D minor (Kiourdi, natural minor with a C# leading tone at cadences).
Two bouzoukis play the same melody a third apart — the twin-bouzouki harmony is the core of the sound — with tremolo on held notes.
A nylon-string guitar walks: bass note on beat 1, fifth on beat 2, soft chords on the off-beats. No drums at all; the guitar is the pulse.
Form: guitar-and-single-bouzouki intro → verse (Dm–Gm–C–F–Dm–Gm–A–Dm) → interlude → second verse with an accordion sustaining the chords underneath → interlude with the bouzoukis an octave higher → quiet outro fading on a Dm tremolo.
Feel: walking slowly through a grey Sunday — lyrical, melancholic, steady, like Tsitsanis "Synnefiasmeni Kyriaki" or Vamvakaris "Frangosyriani". 1950s recording warmth, small ensemble, no reverb wash. About 1 minute 40 seconds.
```

### rebetiko-3-smyrna (Hitzazkiar · tsifteteli 4/4 · 100 · 붐뱁 킷)
**Style**: `Smyrna rebetiko meets boom bap, violin, santouri, oud, punchy hip-hop drums, female vocal, oriental`

**Description**
```
1920s Smyrna-style rebetiko in tsifteteli 4/4 at about 100 BPM, D Hitzazkiar (D Eb F# G A Bb C#).
Opens with a free, slow violin taximi, sliding into notes, for about 12 seconds. Then a punchy boom-bap drum kit drops in —
fat kick on 1 and the and-of-2, cracking snare on 2 and 4, swung eighth-note hi-hats, an open hat every other bar, a snare fill every eighth bar — and the piece locks in.
Violin leads the melody with slides and ornaments, doubling a warm female voice; a santouri rings in constant tremolo behind;
an oud plays the low root notes and short turns. The drums are the only modern element; everything else stays 1920s.
Form: violin taximi → verse → verse → violin solo → verse (an octave higher) → second solo → short coda on a drum hit and a held D.
Feel: ornate, sensual, oriental café-aman on top of a head-nodding hip-hop beat — Rosa Eskenazi sampled by a boom-bap producer. About 1 minute 50 seconds.
```
가사란 골격: `[Violin taximi]` `[Verse 1]` `[Verse 2]` `[Violin solo]` `[Verse 3]` `[Solo]` `[Outro]`

### rebetiko-4-teke (Sabah · slow zeibekiko 9/8 · 56, 루바토)
**Style**: `rebetiko taximi, solo bouzouki, baglamas, minor oriental scale, smoky, intimate, 1930s, instrumental`

**Description**
```
Instrumental 1930s teke (hashish den) rebetiko, dark and unstable, D Sabah (D E F Gb A Bb C — the flattened fourth makes it uneasy).
The first half is a long, free bouzouki taximi with no beat at all: phrases circle around F, lean into the unstable Gb, and fall back to D;
the tempo breathes, long pauses between phrases; a guitar plays a single low D drone only twice, very quietly.
Then a very slow zeibekiko 9/8 (about 56 BPM) emerges: only bouzouki and baglamas — the baglamas strums the off-beats and the heavy final beat,
the bouzouki melody doubled an octave below with tremolo. No drums, no bass. Near the end the beat dissolves back into a short taximi fragment on a final low D.
Sound: tiny room, short dry reverb, smoke, lo-fi filtered highs, close and intimate — like "Minore tou Teke". About 2 minutes.
```

### rebetiko-5-serviko (Rast · hasaposerviko 2/4 · 138→170 아첼레란도)
**Style**: `upbeat rebetiko hasaposerviko, fast bouzouki, accordion, baglamas tremolo, hand drum, instrumental`

**Description**
```
Instrumental upbeat rebetiko hasaposerviko in fast 2/4, starting around 138 BPM, D Rast (major-like, with a natural C when descending).
Guitar hammers eighth-note downstrokes (bass + chord together); a baglamas plays constant sixteenth tremolo high up, doing the hi-hat's job;
a hand drum plays doum-tek-doum-tek with tambourine on every off-beat; an accordion sustains the chords from the second verse.
Bright bouzouki melody in sixteenth-note ornaments over D–G–A7–D and D–Bm–G–A7 turns.
Form: intro → A → B → A (accordion joins) → B (bouzouki solo an octave up) → A → B → A, and from the sixth section onward the whole band
accelerates steadily, bar by bar, up to about 170 BPM for the final section, ending with three hard D hits and a final strum-and-tremolo.
Feel: taverna dance, joyful, sweaty, plates about to fly — late Tsitsanis / Papaioannou fast tunes. Live small-room recording. About 1 minute 30 seconds.
```

메모: 부주키·바글라마스·산투리·우드·바이올린·아코디언은 Logic 에 전용 패치가 없어 SMF 는 GM 25(Acoustic Guitar)·24(Classical Acoustic Guitar)·46(Space Harp)·110(Authentic Strings)·21(Cheap Organ)으로 대용 (09-19 스트립 실측). Suno 에는 원 악기명을 그대로 쓴다.

## canon-lofi v3 — 붙여넣기용 (2026-09-20)

Suno 업로드 편집 화면의 4개 필드 순서대로. 각 버전은 **별도 원곡**으로 등록되어 있고, Cover 는 ⑤ 로 각 2개 생성.

| Suno 필드 | 이 문서 | 제한 |
|---|---|---|
| style summary | ① | 100자 (공백 포함) |
| audio description | ② | 1000자 |
| caption | ③ | 곡 페이지 표시용 — 생성 무관으로 추정 |
| lyrics | ④ | `[Instrumental]` + 섹션 메타태그. **직접 쓴 메타태그가 Cover 를 바꾸는지의 첫 실험**(§7.4-2) — 특히 `[Outro]` 링아웃, B `[Guitar Lead]` |
| (Cover 생성 시 Style) | ⑤ | 100자, "instrumental" 포함, 악기는 역할 문구 |

### v3A — `bounces/canon-lofi-v3a.wav` (84 BPM, 2:46)

**① style summary** (93자)
```
lo-fi city pop, instrumental, 84 BPM, D major, Rhodes lead, muted guitar cutting, finger bass
```

**② audio description** (999자)
```
Instrumental lo-fi city pop at 84 BPM in D major: Pachelbel's Canon melody on Rhodes electric piano over the original ground bass (D A B F# G D G A) with seventh-chord colour. Keep the melody as uploaded.
Two bars of bass and hi-hat, then the Rhodes states the theme straight in quarter notes; from the second statement on it plays with city-pop syncopation. The famous descending sixteenth-note runs are played in full on the Rhodes, then the fast passage, then a calm close.
Muted clean guitar plays sixteenth-note cutting chords on the off-beats. Round finger bass on the roots with octave pops. A soft polysynth adds fifths in the second half; a quiet low pad on D underneath.
Drums: soft dusty kick on 1 and 3 with a push on the and-of-four, tape-saturated snare on 2 and 4, swung hi-hats, open hat every fourth bar, snare fills every eight bars. Tape hiss, highs rolled off.
Ending: drums stop, guitar and pad hold a D major ninth chord and ring out.
Feel: late-summer night drive. About 2:45.
```

**③ caption**
```
Pachelbel's Canon as lo-fi city pop (v3A) — Logic sketch, cover source
```

**④ lyrics** (메타태그 — Logic 마디 구조와 1:1, `[Outro]` 는 종지 서술)
```
[Instrumental]

[Intro]
[round finger bass and swung closed hi-hat only]

[Theme]
[warm Rhodes electric piano states the melody straight in quarter notes]
[soft dusty kick on 1 and 3, tape-saturated snare on 2 and 4 enter]

[Verse]
[Rhodes plays the melody with syncopation]
[muted clean guitar sixteenth-note cutting chords on the off-beats]

[Runs]
[Rhodes plays fast descending sixteenth-note runs]
[open hi-hat accents every fourth bar]

[Build]
[soft polysynth fifths enter under the Rhodes]
[low pad on D sustains]

[Calm]
[Rhodes melody softens, guitar cutting lighter]

[Outro]
[drums stop]
[guitar and pad hold a D major ninth chord and ring out]
```

**⑤ Cover Style** (100자)
```
lo-fi city pop, instrumental, warm Rhodes lead, muted guitar cutting, finger bass, dusty swung drums
```

### v3B — `bounces/canon-lofi-v3b.wav` (84 BPM, 2:46)

**① style summary** (90자)
```
lo-fi city pop, instrumental, 84 BPM, D major, Rhodes and lead guitar trading, finger bass
```

**② audio description** (996자)
```
Instrumental lo-fi city pop at 84 BPM in D major: Pachelbel's Canon melody over a lightly reharmonised ground bass (Dmaj7 A7 Bm7 F#m7 Gmaj7 Bm7 Em7 A7). Keep the melody as uploaded.
Two bars of bass and hi-hat, a snare pickup, then the Rhodes states the theme straight; the second statement is syncopated. At the descending sixteenth-note runs a clean electric guitar takes the melody and leads for sixteen bars while the Rhodes drops back to soft chords; then the Rhodes returns for the fast passage and the calm close.
Muted guitar cutting elsewhere. Round finger bass on the roots with octave pops. A soft polysynth adds fifths in the second half; a quiet low pad on D underneath.
Drums: soft dusty kick on 1 and 3 with a push on the and-of-four, tape-saturated snare on 2 and 4, swung hi-hats, open hat every fourth bar, snare fills every eight bars. Tape hiss, highs rolled off.
Ending: drums stop, guitar and pad hold a D major ninth chord and ring out.
Feel: hazy summer night. About 2:45.
```

**③ caption**
```
Pachelbel's Canon as lo-fi city pop, guitar takes the runs (v3B) — Logic sketch, cover source
```

**④ lyrics** (메타태그 — Logic 마디 구조와 1:1, `[Outro]` 는 종지 서술)
```
[Instrumental]

[Intro]
[round finger bass and swung closed hi-hat only]
[snare pickup fill into the theme]

[Theme]
[warm Rhodes electric piano states the melody straight]
[soft dusty kick on 1 and 3, tape-saturated snare on 2 and 4 enter]

[Verse]
[Rhodes plays the melody with syncopation]
[muted clean guitar cutting chords on the off-beats]

[Guitar Lead]
[clean electric guitar takes the melody and plays the descending sixteenth-note runs]
[Rhodes drops back to soft chords on beats 1 and 3]

[Return]
[Rhodes takes the melody back]
[soft polysynth fifths enter, low pad on D sustains]

[Calm]
[Rhodes melody softens, guitar cutting lighter]

[Outro]
[drums stop]
[guitar and pad hold a D major ninth chord and ring out]
```

**⑤ Cover Style** (100자)
```
lo-fi city pop, instrumental, tape-saturated, dusty swung drums, Rhodes, clean guitar takes the lead
```

### v3C — `bounces/canon-lofi-v3c.wav` (90 BPM, 2:35)

**① style summary** (100자)
```
city pop, instrumental, 90 BPM, D major, Rhodes lead, chorus guitar cutting, finger bass, key change
```

**② audio description** (999자)
```
Instrumental city pop at 90 BPM in D major: Pachelbel's Canon melody on Rhodes electric piano over the original ground bass (D A B F# G D G A). Keep the melody as uploaded.
Two bars of bass and hi-hat, then the Rhodes states the theme straight; the second statement is syncopated. The descending sixteenth-note runs are played in full, the fast passage is lightened. After the runs the band modulates up a whole step to E major for eight bars, then drops back to D major and settles into the calm close.
Chorus guitar plays sixteenth-note cutting chords on the off-beats. Round finger bass on the roots with octave pops. A soft polysynth adds fifths in the second half; a quiet low pad underneath.
Drums: light kick on 1 and 3 with a push on the and-of-four, crisp snare on 2 and 4, swung hi-hats, open hat every second bar, snare fills every eight bars. Bright mix, slightly softened highs.
Ending: drums stop, guitar and pad hold a D major ninth chord and ring out.
Feel: bright, airy. About 2:35.
```

**③ caption**
```
Pachelbel's Canon as city pop with a key change (v3C) — Logic sketch, cover source
```

**④ lyrics** (메타태그 — Logic 마디 구조와 1:1, `[Outro]` 는 종지 서술)
```
[Instrumental]

[Intro]
[round finger bass and swung closed hi-hat only]

[Theme]
[Rhodes electric piano states the melody straight]
[light kick on 1 and 3, crisp snare on 2 and 4 enter]

[Verse]
[Rhodes plays the melody with syncopation]
[chorus guitar sixteenth-note cutting chords on the off-beats]

[Runs]
[Rhodes plays fast descending sixteenth-note runs]
[open hi-hat accents every second bar]

[Key Change]
[crash cymbal, whole band modulates up to E major]
[polysynth fifths under the Rhodes, bright]

[Back to D]
[crash cymbal, band returns to D major]
[Rhodes melody softens, guitar cutting lighter]

[Outro]
[drums stop]
[guitar and pad hold a D major ninth chord and ring out]
```

**⑤ Cover Style** (96자)
```
80s city pop, instrumental, lo-fi mix, Rhodes lead, chorus guitar cutting through, key change up
```

결과 기록: Suno 재작성 Style + 청취 판정 → `FEEDBACK_LOG.md` canon-lofi v3 절. 넣은 최종 텍스트가 위와 다르면 그것을 정본으로 이 절을 갱신.

---

### 이력 (기록용)

- **v1** `bounces/canon-lofi-v1.wav` (3:13, 72 BPM, 원곡 3성부 그대로) — 업로드 **차단** *"This audio matches an existing recording"*. 매처 = 커버곡 감지형.
- **v2** `bounces/canon-lofi-v2.wav` (2:46, 84 BPM) — 리하모 Dmaj7 | F#m7 A7 | Bm7 | D/F# | Gmaj7 | Bm7 | Em7 | A7 + 당김 + 단성부 → 통과. Cover 6개(A 기본 / B 로파이 / C 시티팝 Style, "instrumental" 누락)는 FEEDBACK_LOG 참조. 판정: 분위기는 프롬프트대로, 캐논 정체성은 희석.
- **v3 A/B/C** — 그라운드 8/8(B 는 6/8) 복원 + 3~10 원리듬 + 단일 리드, 셋 다 **통과** → 회피 조건은 "모방 성부 제거 + 부분 당김" 이면 충분, 리하모 불필요.
- v2 Cover Style (기록): A `lo-fi city pop, warm Rhodes, muted guitar cutting, round finger bass, dusty swung drums, night drive` / B `lo-fi city pop, tape-saturated, dusty swung drums, warm Rhodes, muted guitar, mellow night drive` / C `80s city pop, lo-fi mix, Rhodes, chorus guitar cutting, slap-free finger bass, laid-back groove`
- v2 업로드 Style `lo-fi city pop, 84 BPM, D major, Rhodes melody, muted guitar cutting, finger bass, dusty drums`; v1 업로드 Style `lo-fi city pop, Pachelbel Canon in D, 72 BPM, Rhodes, nylon guitar, finger bass, dusty drums`. Description 전문은 git 이력(`c98b498` 이후)에.

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
Basalt Current begins the deep peak with Ebm9 and Abm6, two bars each, over an Eb tonic pedal. Keep it dark; the sixth is shadow, not lift.
Place one short low organ chord per bar, cycling through the and-of-2, beat 4, the and-of-3, and the and-of-1.
The bass cell has a longer Eb2 on beat 1 and a short Ab1 below it on the and-of-3; the next bar answers with a short Eb2 on the and-of-1 and a longer Eb2 on beat 3.
Use eight closed-hat positions per bar and one extra quiet sixteenth only in every fourth bar. One open hat every two bars replaces a closed hat. Keep clap strictly below the snare at the same onset.
Structure: 1-16 intro, 17-32 A, 33-40 checkerboard break, 41-56 A2, 57-64 drums and tonic bass only. In the break, odd bars retain kick, snare and bass; even bars retain hats, snare and organ.
Drums first, sub at bar 9, organ touch at 12. A single quiet crash marks bar 41 beat 1.
Peak through density and space, not loudness. No lead, no vocals, DJ-friendly intro/outro.
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
Bass from bar 9, one organ hint at 12, full harmony from 17. Keep every kick soft despite the peak tempo.
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
Bass from bar 9, piano hint at 12, full harmony from 17. One quiet crash lands on bar 41 beat 1.
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
Soft grand piano plays a half-beat stab on the and-of-3 in the first three bars of each cycle, then holds 2.75 beats from the and-of-1 in the fourth bar with sustain.
Soft kick, quiet rimshot on 2 and 4 from bar 9, six or seven closed hats per bar using the a-of-1 and a-of-3 as ghosts, one open hat every three bars.
Sub bass on G#1 only: a short note on the one, a sixteenth pickup on the a-of-1, then a 1.2-beat note from the and-of-3,; second bars end with a short and-of-4.
Structure: 1-16 intro (kick, hats, sub from 9, piano hints at 12/14), 17-32 full, 33-40 break with the kick on beats 1 and 3 only and the sub, no hats, no rim, no piano, 41-56 full with one quiet crash on bar 41 beat 1, 57-64 drums and bass only.
Tense but quiet. No lead, no vocals, DJ-friendly intro/outro.
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
The electric piano holds 3.25 beats from the and-of-1 with sustain, then plays one short touch on the and-of-4 of the next bar.
Soft but driving kick, soft snare on 2 and 4 from bar 9 with no clap, eighth-note hats with ghost sixteenths on the e-of-1 and e-of-3 in odd bars, one open hat every two bars.
Sub bass entirely on the off-beats: four short and-of-beat notes in odd bars; in even bars the and-of-3 note lengthens to 1.4 beats and drops to the fifth below (Bb1) in the full sections.
Structure: 1-16 intro (kick, hats, sub from 9, piano hints at 12/14), 17-32 full, 33-40 break with hats and snare over a whole-note sub drone, no kick, no piano, 41-56 full with one quiet crash on bar 41 beat 1, 57-64 drums and bass only.
Heavy below, empty above. No lead, no vocals, DJ-friendly intro/outro.
```

## dh20-wet-granite-v1
**Style**
```
Instrumental deep house end of peak, 122 BPM, C minor, soft kick, rimshot, six or four sparse closed hats per bar, sub bass with a fifth below, held soft grand piano minor ninth and flat-six major-seventh chords, low root-and-fifth pad entering in the break, rim-and-pad break, no lead, no vocals, DJ-friendly intro/outro.
```

**Description**
```
Wet Granite is a 64-bar track that closes the peak section on Cm9 for five bars and Abmaj7/C for three bars, with C2 under both; Bb falls to Ab and D to C, an aeolian flat-six shade.
Soft grand piano holds 3.5 beats from the one in cycle bars 1, 3 and 5, then 2.75 beats from beat 2 in bars 6 and 8, with sustain re-pressed each attack.
Soft kick, quiet rimshot on 2 and 4 from bar 9, six closed hats in odd bars (with e-of-3 and e-of-4 ghosts) and four in even bars, one open hat every three bars.
Sub bass: a 1.5-beat note on the one, a short and-of-3 and a note on beat 4; the second bar's beat-4 note drops to the fifth below (G1) in the full sections.
A very quiet root-and-fifth pad (G2 and C3) enters at bar 33 and stays until bar 56.
Structure: 1-16 intro (kick, hats, sub from 9, piano hints at 12/14), 17-32 full, 33-40 rimshot and pad only, 41-56 full with one quiet crash on bar 41 beat 1, 57-64 drums and bass only.
Settling, not lifting. No lead, no vocals, DJ-friendly intro/outro.
```

## dh23-paper-lantern-v1
**Style**
```
Instrumental drifting deep house, 120 BPM, D minor, soft kick, rimshot, swung five-hat patterns, sparse sub bass, held electric piano minor ninth and flat-three major ninth chords, very quiet root-and-fifth pad from the first full section, hats-and-pad break, no lead, no vocals, DJ-friendly intro/outro.
```

**Description**
```
Paper Lantern is a 64-bar drifting deep house track on Dm9 and Fmaj9/D, four bars each, with D2 held under both; F steps down to E and A to G while the top E rises to F.
The electric piano holds 1.9 beats from beat 3 in cycle bars 1 and 5, 3.25 beats from the swung and-of-1 in bars 2 and 6, and a short touch on beat 3 of bar 8, sustain re-pressed each attack.
Soft kick, quiet rimshot on 2 and 4 from bar 9, swung closed hats in two five-position patterns, one open hat every four bars.
Sub bass: a 0.75-beat note on beat 2 and a 1.4-beat note from the swung and-of-3; the second bar replaces the long note with a short fifth-below (A1) on the and-of-4 in the full sections.
A very quiet root-and-fifth pad (A2, D3) sits under bars 17-56.
Structure: 1-16 intro (kick, hats, sub from 9, piano hints at 12/14), 17-32 full, 33-40 closed hats and pad only, 41-56 full with one quiet crash on bar 41 beat 1, 57-64 drums and bass only.
Soft-lit and slow. No lead, no vocals, DJ-friendly intro/outro.
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

---

# 2026-10-21 Lo-fi Hip Hop Set (v1) — 곡별 Suno 프롬프트 (슬롯 순)

Cover 업로드 시 `{sid}-v1.wav`(2:52~3:12) 와 함께 쓴다. 구조: 56마디(≤78 BPM) 1–8 intro / 9–24 A / 25–32 break / 33–48 A2 / 49–56 outro, 64마디(≥80 BPM) 1–8 / 9–28 / 29–36 / 37–56 / 57–64. 리드는 A 마지막 8마디 + A2. 모든 블록 Description ≤ 1,000자·Style ≤ 300자 측정 완료.

## lh01-felt-doorway-v1
**Style**
`lo-fi hip hop, 76 BPM, D minor with Dorian color, mellow electric piano, nylon picking, finger bass, sparse acoustic boom bap, swung hats, intimate EP lead, instrumental`

**Description**
```
Felt Doorway: 76 BPM, D minor, 56 bars. Loop Dm9-Dm9-G13-G13; mellow four-voice electric piano alternates downbeat holds with delayed answers, re-pedalled every bar. Sparse SoCal boom bap: kick on one with changing a-of-two, a-of-three, and-of-two or and-of-three pickups; snare on 2/4, even-bar rims, soft ghosts, swung eighth hats with louder offbeats. Finger bass omits a kick each bar. Nylon picks leave long gaps. Four-bar EP lead: A-G-E / F-E-D / E-G-A / B-A-G; repeat with a delayed final answer in A2. Intro 1-8 opens with keys+hats, kick/snare at 5; A 9-24 adds bass, lead at 17; break 25-32 keys alone then nylon; A2 33-48 restores the pocket with one soft crash; outro 49-56 drops lead/nylon, ends keys only. no vocals, lo-fi warmth, DJ-friendly intro/outro
```

## lh02-linen-afternoon-v1
**Style**
`lo-fi hip hop, 76 BPM, D minor, nylon guitar opening, mellow electric piano holds, finger bass, sparse acoustic boom bap, swung hats, soft EP lead, instrumental`

**Description**
```
Linen Afternoon: 76 BPM, D minor, 56 bars. Loop Dm9-Am7-Bbmaj7-Gm9, natural-minor i-v-VI-iv; mellow four-voice electric piano holds every downbeat and adds one late re-hit on the and-of-three in bar two and the and-of-four in bar four, re-pedalled every bar. Sparse SoCal boom bap: kick on one plus the and-of-three, the a-of-two in bar three, both and-of-three and a-of-three in bar four; soft snare on 2/4, one ghost before each bar line, swung eighth hats with louder offbeats, one open hat per four bars. Finger bass holds the root for two beats and adds a low A only in bar four. Four-bar EP lead that rests on beat one: A-F-D / E-G / F-A-Bb / G-F; alternate A2 phrases delay bar two by an eighth and shorten bar four. Intro 1-8 nylon picking alone, hats at 3, kick/snare and keys at 5; A 9-24 adds bass, lead at 17; break 25-32 nylon alone then keys join; A2 33-48 full pocket with one soft crash; outro 49-56 drops lead/nylon, ends keys only. no vocals, lo-fi warmth, DJ-friendly intro/outro
```

## lh03-chalk-awning-v1
**Style**
`lo-fi hip hop, 78 BPM, F major, nylon guitar picking intro, warm electric piano ninths with sustain, finger bass, lazy acoustic boom bap, ghost snares, swung hats, soft grand piano lead, instrumental`

**Description**
```
Chalk Awning: 78 BPM, F major, 56 bars. Loop Fmaj9-Am7-Bbmaj9-C13sus, I-iii-IV-V13sus; electric piano holds bar one, answers on the and-of-two and beat four in bar two, hits one plus the e-of-three in bar three, pushes the and-of-one in bar four, re-pedalled every bar. Lazy SoCal boom bap: kick on one plus the and-of-three, then the a-of-two, the a-of-three, and the and-of-two with the and-of-three in bar four; snare on 2/4 with ghosts, swung eighth hats, one open hat per four bars. Finger bass follows the kick but skips its last hit, adding a chromatic approach back into Fmaj9 in bar four. Nylon picks chord tones. Grand piano lead: G-A-C / E-C / D-C-A-F / G-F, climbing to E then walking down; A2 alternates a breath in bar one and an early bar three. Intro nylon alone, hats at 3, EP/kick/snare at 5, bass at 9; break 25-32 drums out, bass, EP and nylon trio; crash at 33; outro drops lead and nylon, last 4 bars drums and keys. no vocals, lo-fi warmth, DJ-friendly intro/outro.
```

## lh04-paper-saucer-v1
**Style**
`lo-fi hip hop, 78 BPM, C major, pedalled jazz grand piano, soft organ, lyrical nylon lead, finger bass, relaxed acoustic boom bap, ghost snares, swung hats, instrumental`

**Description**
```
Paper Saucer: 78 BPM, C major, 56 bars. Cmaj7-Em7-Dm9-G13, one bar each; four-voice grand piano alternates offbeat two-hit comping and a single held answer, with fresh pedal each bar. SoCal kick on one plus changing and-of-two/a-of-three pickups, snare on 2/4 with two quiet ghosts, swung eighth hats, rare open hat. Finger bass leaves one kick unanswered. Soft organ holds behind a nylon lead: G-B-A / G-F#-E / F-E-C / D-E-G, a rising third followed by descending replies. Intro 1-8: keys first, hats at 3, kick/snare at 5; A 9-24 adds bass and organ, lead at 17; break 25-32 removes kick and bass, keeping backbeat, hats, piano and organ; A2 33-48 adds a quiet crash and the full lead; outro 49-56 drops lead/organ, final four bars drums+keys. no vocals, lo-fi warmth, DJ-friendly intro/outro
```

## lh05-tin-kettle-v1
**Style**
`lo-fi hip hop, 80 BPM, A minor, pedalled jazz grand piano on the off-beat, high electric piano picking, finger bass, relaxed acoustic boom bap, ghost snares, swung hats, nylon guitar lead, instrumental`

**Description**
```
Tin Kettle: 80 BPM, A minor, 64 bars. Loop Am9-Fmaj9-Cmaj9-E7b9, i-VI-III-V; grand piano comps on the and-of-two in odd bars, one plus the and-of-three in bar two, three hits in bar four, re-pedalled every bar. Relaxed SoCal boom bap: kick on one plus the and-of-two, adding the a-of-three in bar two, only the and-of-three in bar three, a-of-two with a-of-three in bar four; snare on 2/4 with two ghosts, swung eighth hats, one open hat per four bars. Finger bass follows the kick minus one or two hits, ending bar four on the low E. A high electric piano picks chord tones above the piano. Four-bar nylon lead: E-G-B / C-A / G-E-D / G#-F; A2 alternates a delayed bar two and a shortened bar four. Intro 1-8 piano first, hats at 3, kick/snare at 5; A 9-28 adds bass and EP picking, lead at 21; break 29-36 drops kick and snare, keeping hats, bass and piano; A2 37-56 full pocket with one soft crash; outro 57-64 drops lead/EP, ends drums+piano. no vocals, lo-fi warmth, DJ-friendly intro/outro
```

## lh06-iron-teacup-v1
**Style**
`lo-fi hip hop, 80 BPM, A minor, descending aeolian loop, pedalled jazz grand piano, nylon guitar picking, finger bass, relaxed acoustic boom bap, ghost snares, swung hats, soft electric piano lead, instrumental`

**Description**
```
Iron Teacup: 80 BPM, A minor, 64 bars. Loop Am9-G13-Fmaj9-Em7, descending i-VII-VI-v; grand piano hits one plus a late and-of-four push in odd bars, the and-of-one plus beat three in bar two, beat two plus the and-of-three in bar four, re-pedalled every bar. SoCal boom bap: kick on one with the a-of-two and and-of-three in bar one, the a-of-three in bar two, the and-of-two and a-of-three in bar three, the and-of-three in bar four; snare on 2/4 with ghosts, swung eighth hats, one open hat per four bars. Finger bass skips the last kick hit, dropping to the low fifth in bar one and adding the fifth in bar three. Nylon picks between chords. Electric piano lead: E-D-B / D-B-A / C-A-G / G-B, a falling three-note cell stepped down with the chords, answered upward. Intro piano first, hats at 3, kick/snare at 5, bass and nylon at 9; break 29-36 bass alone, nylon joins at 31, snare and hats at 33; crash at 37; outro 57-64 drums and piano. no vocals, lo-fi warmth, DJ-friendly intro/outro.
```

## lh07-moss-index-v1
**Style**
`lo-fi hip hop, 82 BPM, E minor, dusty electric piano, acoustic guitar picking, understated grand-piano lead, finger bass, lazy boom bap, shuffled eighth hats, instrumental`

**Description**
```
Moss Index: 82 BPM, E minor, 64 bars. Em9-Am7-Bm7-Em9, one chord per bar. Four-voice EP alternates clipped two-hit comping with longer delayed holds, pedalled each bar. SoCal kick anchors one with changing and-of-three and a-of-two/a-of-three pickups; snare on 2/4 plus two soft ghosts, strongly swung hats and rare open hats. Finger bass follows selected kicks, leaving space. Guitar picks alternate two- and three-note gaps. Piano lead: B-A-G-F# / E-G-E / F#-A-B / A-G-F#-E, a four-bar falling bookmark with a rising answer. Intro 1-8 keys, hats at 3, backbeat at 5; A 9-28 bass/guitar, lead at 21; break 29-36 removes drums and bass for EP/guitar duet; A2 37-56 restores groove and lead with one soft crash; outro 57-64 loses lead/guitar, last four bars drums+keys. no vocals, lo-fi warmth, DJ-friendly intro/outro
```

## lh08-cedar-ledger-v1
**Style**
`lo-fi hip hop, 82 BPM, G major, warm electric piano ninths, nylon guitar picking, finger bass, laid-back acoustic boom bap, ghost snares, swung hats, grand piano lead, instrumental`

**Description**
```
Cedar Ledger: 82 BPM, G major, 64 bars. Loop Gmaj9-Bm7-Em9-Cmaj9, I-iii-vi-IV; warm four-voice electric piano comps on one and the and-of-two, only beat three in bar two, the and-of-one and and-of-three in bar four, re-pedalled every bar. Laid-back SoCal boom bap: kick on one plus a-of-two and and-of-three, a-of-three in bar two, a-of-two in bar three, and-of-three with a-of-three in bar four; snare on 2/4 with two ghosts, swung eighth hats, one open hat per four bars. Finger bass keeps the root and one syncopation on three-kick bars. Nylon guitar picks chord tones in the gaps. Four-bar grand piano lead: D-B-A-F# / F#-A / B-D-E / D-B, falling a fifth then climbing to the ninth; A2 alternates a delayed bar two and a shortened bar four. Intro 1-8 (EP, hats at 3, drums at 5); A 9-28 adds bass and nylon, lead at 21; break 29-36 only kick, bass and EP; A2 37-56 full with a soft crash; outro 57-64 lead/nylon out, ends drums+EP. no vocals, lo-fi warmth, DJ-friendly intro/outro
```

## lh09-signal-orchard-v1
**Style**
`lo-fi hip hop, 84 BPM, D major, soft electric piano comping, tonewheel organ holds, finger bass, head-nod acoustic boom bap, ghost snares, swung hats, nylon guitar lead, instrumental`

**Description**
```
Signal Orchard: 84 BPM, D major, 64 bars, building toward the peak. Loop Dmaj9-A13sus-Bm9-Gmaj9, I-V13sus-vi-IV; electric piano comps on one, the and-of-two and the and-of-three in odd bars, one late touch in bar two, one plus beat four in bar four, re-pedalled every bar, over a soft organ hold. SoCal boom bap: kick on one plus the and-of-two and and-of-three, then the a-of-three, the a-of-two with the and-of-three, then the and-of-two; snare on 2/4 with ghosts, swung eighth hats, one quiet sixteenth hat after beat four, one open hat per four bars. Finger bass follows the kick minus its last hit. Nylon guitar lead: F#-A-B-A / F#-E / B-D-C# / A-F#, a pentatonic turn and a sigh, then the turn lifted to B. Intro EP first, hats at 3, kick/snare at 5, bass and organ at 9; break 29-36 snare, hats and organ only; crash at 37; outro 57-64 drums and EP. no vocals, lo-fi warmth, DJ-friendly intro/outro.
```

## lh10-copper-margin-v1
**Style**
`lo-fi hip hop, 84 BPM, B minor, jazzy electric piano, nylon guitar, round pulse bass, assertive acoustic boom bap, deeply swung hats, compact EP melody, instrumental`

**Description**
```
Copper Margin: 84 BPM, B minor, 64 bars. Bm9-Dmaj7-Gmaj7-F#9, one bar each, warm four-voice EP comping two or three times per bar with re-pedalling. SoCal kick anchors one and alternates paired and/a-of-two and three pickups; snare on 2/4 with two ghost notes, deeply swung hats and occasional soft open hat. Round pulse bass omits the final kick of each bar; nylon picking fills selected gaps. EP lead F#-A-C#-A / A-F#-E / F#-G-B-A / G#-F#-E-F# climbs in thirds then folds inward; later A2 answers arrive late. Intro 1-8 keys, hats 3, kick/snare 5; A 9-28 adds bass/nylon, lead at 21; break 29-36 drums+bass only; A2 37-56 returns harmony and lead with one soft crash; outro 57-64 removes lead/nylon, final four bars drums+keys. no vocals, lo-fi warmth, DJ-friendly intro/outro
```

## lh11-velvet-circuit-v1
**Style**
`lo-fi hip hop, 86 BPM, B minor, pedalled jazz grand piano, soft tonewheel organ holds, synth bass, full acoustic boom bap, ghost snares, swung hats with sixteenth flicks, electric piano lead, instrumental`

**Description**
```
Velvet Circuit: 86 BPM, B minor, 64 bars. Loop Bm9-Em9-Gmaj9-A13, i-iv-VI-VII13; grand piano comps on the a-of-one and three in odd bars, on one, the and-of-two and four in bar two, on one, the and-of-three and and-of-four in bar four, re-pedalled every bar. Full SoCal boom bap: kick on one plus two syncopations per bar (and-of-two/a-of-three, and-of-two/and-of-three, a-of-two/a-of-three, and-of-three/a-of-three); snare on 2/4 with two ghosts, swung eighth hats plus one quiet sixteenth after beat two or four. Synth bass follows the kick minus one hit, landing on F# before each loop. Soft organ holds root and fifth. Four-bar EP lead: D-F#-A-F# / G-F#-E-D / D-F#-G-B / A-G-F#; A2 varies bars two and four. Intro 1-8 (piano, hats at 3, drums at 5); A 9-28 adds bass and organ, lead at 21; break 29-36 drums alone, piano back after four bars; A2 37-56 full with a soft crash; outro 57-64 lead/organ out, ends drums+piano. no vocals, lo-fi warmth, DJ-friendly intro/outro
```

## lh12-ember-switchyard-v1
**Style**
`lo-fi hip hop, 86 BPM, F# minor dorian, warm jazz grand piano stabs, high electric piano picking, deep synth bass, full acoustic boom bap, ghost snares, swung hats, nylon guitar lead, instrumental`

**Description**
```
Ember Switchyard: 86 BPM, F# minor dorian, 64 bars, the peak. Loop F#m9-Amaj9-E6/9-B9, i-III-VII-IV9; grand piano hits one, the a-of-one and the and-of-three in odd bars, the and-of-two plus beat four in bar two, the and-of-one, beat three and the and-of-four in bar four, re-pedalled every bar. Full SoCal boom bap: kick on one with two syncopations every bar (a-of-two/a-of-three, and-of-two/and-of-three, and-of-three/a-of-three, a-of-two/and-of-three); snare on 2/4 with two ghosts, swung eighth hats, one sixteenth hat after beat four, one open hat per four bars. Deep synth bass follows the kick minus its last hit. A high electric piano picks chord tones. Nylon lead: A-C#-E / E-C#-B / G#-B-C# / C#-A-F#, a triad climbing from the and-of-one, folding back down. Intro piano first, hats at 3, kick/snare at 5, bass at 9; break 29-36 piano and bass, hats at 31, kick at 33, snare back at 37; crash at 37; outro 57-64 drums and piano. no vocals, lo-fi warmth, DJ-friendly intro/outro.
```

## lh13-apricot-carbon-v1
**Style**
`lo-fi hip hop, 88 BPM, A major, warm grand piano, soft upper electric piano, nylon melody, rounded pulse bass, buoyant acoustic boom bap, swung hats, instrumental`

**Description**
```
Apricot Carbon: 88 BPM, A major, 64 bars. Amaj7-C#m7-F#m9-Bm9, one bar each; grand piano plays four-voice jazz comping with varied two/three-hit syncopation and per-bar pedal. SoCal kick on one with changing two/three pickups, snare on 2/4 plus quiet ghosts, swung hats with bright offbeat accents and rare open hats. Round pulse bass leaves one kick empty. Soft upper EP picks separate chord tones. Nylon lead A-C#-B-A / G#-B-G# / A-G#-F#-E / F#-A-C#-B makes a small arch, never a run. Intro 1-8 keys, hats at 3, kick/snare at 5; A 9-28 adds bass/EP, lead at 21; break 29-36 removes kick/bass, retains backbeat+hats+piano, upper EP joins halfway; A2 37-56 full pocket and lead with a soft crash; outro 57-64 drops lead/EP, final four bars drums+keys. no vocals, lo-fi warmth, DJ-friendly intro/outro
```

## lh14-brass-orchard-v1
**Style**
`lo-fi hip hop, 88 BPM, E major, bright-but-mellow electric piano ninths, nylon guitar picking, synth bass, full acoustic boom bap, ghost snares, swung hats with sixteenth flicks, nylon guitar lead, instrumental`

**Description**
```
Brass Orchard: 88 BPM, E major, 64 bars. Loop Emaj9-Amaj9-G#m7-C#m9, I-IV-iii-vi; four-voice electric piano comps on one and the a-of-three in odd bars, the e-of-two and four in bar two, three off-beat hits in bar four, re-pedalled every bar. Full SoCal boom bap: kick on one plus two syncopations per bar (a-of-two/and-of-three, and-of-two/a-of-three, and-of-two/and-of-three, a-of-two/a-of-three); snare on 2/4 with two ghosts, swung eighth hats plus one quiet sixteenth after beat two or four. Synth bass follows the kick minus one hit and approaches each loop from B. Nylon guitar picks chord tones between the kicks. Four-bar nylon lead: G#-B-C#-B / A-G#-E / D#-F#-G# / B-G#-F#-E; A2 varies bars two and four. Intro 1-8 (EP, hats at 3, drums at 5); A 9-28 adds bass and nylon, lead at 21; break 29-36 EP alone, bass back after two bars, hats after four; A2 37-56 full with a soft crash; outro 57-64 lead/nylon out, ends drums+EP. no vocals, lo-fi warmth, DJ-friendly intro/outro
```

## lh15-quartz-overpass-v1
**Style**
`lo-fi hip hop, 88 BPM, C# minor, nylon guitar picking intro, electric piano ninths with sustain, deep synth bass, full acoustic boom bap, ghost snares, swung hats, grand piano lead, instrumental`

**Description**
```
Quartz Overpass: 88 BPM, C# minor, 64 bars, peak of the set. Loop C#m9-F#9-Amaj9-G#7b13, i-IV9-VI-V; electric piano on one, beat three and the and-of-four in odd bars, the a-of-one plus the and-of-three in bar two, the and-of-two plus the e-of-three in bar four, re-pedalled every bar. Full SoCal boom bap: kick on one with two syncopations every bar (and-of-two/a-of-three, and-of-three/a-of-three, a-of-two/a-of-three, and-of-two/and-of-three); snare on 2/4 with two ghosts, swung eighth hats, one sixteenth hat after beat four, one open hat per four bars. Deep synth bass follows the kick minus its last hit. Nylon guitar picks busy chord tones. Grand piano lead: G#-B-G#-E / A#-G# / B-C#-B-G# / B#-G#, a neighbour-tone turn repeated a step higher, closed by the leading tone. Intro nylon alone, hats at 3, EP/kick/snare at 5, bass at 9; break 29-36 drums, bass and nylon, keys out; crash at 37; outro 57-64 drums and EP. no vocals, lo-fi warmth, DJ-friendly intro/outro.
```

## lh16-indigo-receipt-v1
**Style**
`lo-fi hip hop, 86 BPM, C# minor with Dorian color, electric piano, soft tonewheel organ, warm grand-piano lead, rounded pulse bass, lazy acoustic boom bap, instrumental`

**Description**
```
Indigo Receipt: 86 BPM, C# minor, 64 bars. C#m9-Emaj7-Bmaj7-G#7b13, four-voice EP with syncopated two/three-hit comping and per-bar pedal. SoCal kick on one plus alternating and-of-two/a-of-three and a-of-two/and-of-three pickups, snare on 2/4 with two ghosts, deeply swung eighth hats, occasional open hat. Round pulse bass skips each last kick; soft organ holds midrange dyads. Piano lead G#-F#-D# / E-F#-G#-B / F#-D#-F# / G#-A#-B#-A# rises through E major then turns around the leading tone. Intro 1-8 keys, hats at 3, backbeat at 5; A 9-28 bass/organ, lead at 21; break 29-36 drums/bass out: EP two bars, EP+organ four, organ alone two; A2 37-56 returns full groove/lead with one soft crash; outro 57-64 drops lead/organ, final four bars drums+keys. no vocals, lo-fi warmth, DJ-friendly intro/outro
```

## lh17-slate-harbour-v1
**Style**
`lo-fi hip hop, 86 BPM, G-sharp minor, high electric piano opening, pedalled jazz grand piano, finger bass, relaxed acoustic boom bap, ghost snares, swung hats, grand piano lead, instrumental`

**Description**
```
Slate Harbour: 86 BPM, G# minor, 64 bars. Loop G#m9-Emaj7-F#13-D#m7, i-VI-VII13-v; grand piano comps three times in bar one (one, and-of-two, a-of-three), holds bar two, hits the a-of-two and four in bar three, one and the and-of-three in bar four, re-pedalled every bar. Relaxed SoCal boom bap: kick on one plus and-of-two and and-of-three in odd bars, a-of-three in bar two, a-of-two in bar four; snare on 2/4 with two ghosts, swung eighth hats. Finger bass keeps the root and one syncopation on three-kick bars. A high electric piano picks single chord tones an octave up. Four-bar grand piano lead: F#-G#-B / D#-B-G# / A#-G#-F# / F#-D#, peaking on D# then sighing down; A2 varies bars two and four. Intro 1-8 high EP alone, hats at 3, drums and piano at 5; A 9-28 adds bass, lead at 21; break 29-36 only EP picking and bass; A2 37-56 full with a soft crash; outro 57-64 lead/EP out, ends drums+piano. no vocals, lo-fi warmth, DJ-friendly intro/outro
```

## lh18-lantern-deck-v1
**Style**
`lo-fi hip hop, 84 BPM, B major, drifting, pedalled jazz grand piano, borrowed minor iv, soft tonewheel organ swells, finger bass, easy acoustic boom bap, ghost snares, swung hats, electric piano lead, instrumental`

**Description**
```
Lantern Deck: 84 BPM, B major, 64 bars, the drift begins. Loop Bmaj9-G#m9-Emaj9-Em9, I-vi-IV-iv with a borrowed minor iv; grand piano on one plus the and-of-three in odd bars, beat two in bar two, one plus the e-of-two in bar four, re-pedalled every bar, with a soft organ swell under each chord. Easy SoCal boom bap: kick on one plus the a-of-three, then the and-of-two with the and-of-three, the and-of-three, and the a-of-two with the a-of-three; snare on 2/4 with one or two ghosts, swung eighth hats, one open hat per four bars. Finger bass follows the kick minus its last hit, approaching the loop's return chromatically from below. Electric piano lead: C#-A#-F# / G#-A#-B / D#-B / D-B-G, a fall and a climb, then the D#-B shape darkened to D-B-G over the minor iv. Intro piano first, hats at 3, kick/snare at 5, bass and organ at 9; break 29-36 piano and hats, kick added at 33; crash at 37; outro 57-64 drums and piano. no vocals, lo-fi warmth, DJ-friendly intro/outro.
```

## lh19-pearl-crossing-v1
**Style**
`lo-fi hip hop, 84 BPM, F# major, soft jazz grand piano, acoustic guitar picking, mellow EP lead, finger bass, open acoustic boom bap pocket, swung hats, instrumental`

**Description**
```
Pearl Crossing: 84 BPM, F# major, 64 bars. F#maj7-G#m9-A#m7-Bmaj7, a rising-root loop under four-voice grand piano with alternating two-hit comping and delayed holds, re-pedalled each bar. SoCal kick on one with a-of-three or changing two/three pickups; snare on 2/4 plus soft ghosts, swung eighth hats, rare open hat. Finger bass follows fewer kicks. Guitar alternates two- and three-note picking. EP lead A#-G#-E# / F#-G#-A# / C#-B#-A# / A#-F#-D# rises and releases into a descending answer. Intro 1-8 keys, hats 3, backbeat 5; A 9-28 adds bass/guitar, lead 21; break 29-36 kick/bass out, keys/guitar with snare for four bars then hats for four; A2 37-56 full lead and groove, one quiet crash; outro 57-64 removes lead/guitar, last four bars drums+keys. no vocals, lo-fi warmth, DJ-friendly intro/outro
```

## lh20-dusk-corridor-v1
**Style**
`lo-fi hip hop, 82 BPM, E-flat minor, hazy electric piano off-beat comping, nylon guitar picking, finger bass, relaxed acoustic boom bap, ghost snares, swung hats, electric piano lead, instrumental`

**Description**
```
Dusk Corridor: 82 BPM, Eb minor, 64 bars. Loop Ebm9-Gbmaj9-Abm9-Bbm7, i-III-iv-v; hazy four-voice electric piano comps on the and-of-one and and-of-three in odd bars, one and four in bar two, a single and-of-two in bar four, re-pedalled every bar. Relaxed SoCal boom bap: kick on one plus and-of-three with a-of-three in bar one, and-of-two in bar two, and-of-three in bar three, a-of-two with and-of-three in bar four; snare on 2/4 with two ghosts, swung eighth hats. Finger bass keeps the root and one syncopation on three-kick bars, approaching each loop from Bb. Nylon guitar picks chord tones off the beat. Four-bar EP lead: Bb-Gb-F / F-Ab-Bb / Cb-Bb-Gb / Ab-F-Eb, dropping then climbing back; A2 varies bars two and four. Intro 1-8 (EP, hats at 3, drums at 5); A 9-28 adds bass and nylon, lead at 21; break 29-36 drops drums and guitar, leaving EP and bass; A2 37-56 full with a soft crash; outro 57-64 lead/nylon out, ends drums+EP. no vocals, lo-fi warmth, DJ-friendly intro/outro
```

## lh21-ink-carousel-v1
**Style**
`lo-fi hip hop, 82 BPM, E-flat minor, falling-fourths loop, held jazz grand piano chords, high electric piano picking, finger bass, laid-back acoustic boom bap, ghost snares, swung hats, nylon guitar lead, instrumental`

**Description**
```
Ink Carousel: 82 BPM, Eb minor, 64 bars. Loop Ebm9-Db6/9-Gbmaj9-Cbmaj9, i-VII-III-VI falling in fourths; grand piano holds bars one and three, plays the and-of-one plus beat four in bar two and the and-of-one plus beat three in bar four, re-pedalled every bar. Laid-back SoCal boom bap: kick on one plus the and-of-two and and-of-three, then the a-of-two, the a-of-three, and the and-of-two with the a-of-three; snare on 2/4 with one or two ghosts, swung eighth hats, one open hat per four bars. Finger bass follows the kick minus its last hit. A high electric piano picks sparse chord tones. Nylon guitar lead: Bb-Bb-Db / Bb-Ab-F / F-F-Ab / Bb-Gb, a repeated-note pickup answered by a short fall, then the same pickup a fourth lower. Intro high EP alone, hats at 3, piano/kick/snare at 5, bass at 9; break 29-36 high EP alone, bass joins at 33; crash at 37; outro 57-64 drums and piano. no vocals, lo-fi warmth, DJ-friendly intro/outro.
```

## lh22-plum-platform-v1
**Style**
`lo-fi hip hop, 80 BPM, Bb minor, mellow electric piano, nylon guitar picking, intimate grand-piano motif, finger bass, spacious acoustic boom bap, lazy swung hats, instrumental`

**Description**
```
Plum Platform: 80 BPM, Bb minor, 64 bars. Bbm9-Gbmaj7-Ab13-Ebm9 returns through the minor subdominant; four-voice EP uses delayed two-hit comping and a final held answer, pedal renewed each bar. SoCal kick anchors one with changing and-of-two and paired three pickups; snare on 2/4 plus quiet ghosts, lazy swung hats and sparse open hats. Finger bass omits the last kick. Nylon picks thin toward the fourth bar. Piano lead F-Ab-F / Gb-F-Db / C-Db-F / F-Eb-Db answers a small upward sigh with a descent. Intro 1-8 keys, hats at 3, backbeat at 5; A 9-28 bass/guitar, lead at 21; break 29-36 drums+bass for four bars then keys+guitar alone for four; A2 37-56 restores groove and full lead with a soft crash; outro 57-64 drops lead/guitar, final four bars drums+keys. no vocals, lo-fi warmth, DJ-friendly intro/outro
```

## lh23-honey-transit-v1
**Style**
`lo-fi hip hop, 80 BPM, D-flat major, pedalled jazz grand piano, soft tonewheel organ holds, finger bass, relaxed acoustic boom bap, ghost snares, swung hats, nylon guitar lead, instrumental`

**Description**
```
Honey Transit: 80 BPM, Db major, 64 bars. Loop Dbmaj9-Ebm9-Gbmaj7-Ab13, I-ii-IV-V13; grand piano comps on one and three in odd bars, one and the and-of-two in bar two, the and-of-one and a-of-three in bar four, re-pedalled every bar. Relaxed SoCal boom bap: kick on one plus a-of-two in bar one, and-of-three with a-of-three in bar two, and-of-two in bar three, and-of-two with and-of-three in bar four; snare on 2/4 with two ghosts, swung eighth hats. Finger bass keeps the root and one syncopation on three-kick bars, landing on Ab before each loop. Soft organ holds root and fifth under the piano. Four-bar nylon lead: F-Ab-C / Bb-Ab-Gb / F-Bb-Db / C-Bb, a climb answered by a step down; A2 varies bars two and four. Intro 1-8 (piano, hats at 3, drums at 5); A 9-28 adds bass and organ, lead at 21; break 29-36 drops piano and bass, leaving drums and organ; A2 37-56 full with a soft crash; outro 57-64 lead/organ out, ends drums+piano. no vocals, lo-fi warmth, DJ-friendly intro/outro
```

## lh24-felt-almanac-v1
**Style**
`lo-fi hip hop, 78 BPM, A-flat major, cooling down, mellow electric piano ninths with sustain, nylon guitar picking, finger bass, sparse acoustic boom bap, one ghost snare, swung hats, grand piano lead, instrumental`

**Description**
```
Felt Almanac: 78 BPM, Ab major, 56 bars, the cool-down begins. Loop Abmaj9-Fm9-Cm7-Dbmaj9, I-vi-iii-IV; electric piano on one plus the and-of-two in bar one, a whole-bar hold in bar two, a single late hit on the and-of-three in bar three, one plus beat three in bar four, re-pedalled every bar. Sparse SoCal boom bap: kick on one plus the a-of-two, the and-of-three, the and-of-two with the a-of-three, then the a-of-three; snare on 2/4 with a single ghost, swung eighth hats, one open hat per four bars. Finger bass follows the kick minus its last hit. Nylon guitar picks two notes a bar. Grand piano lead, two notes at most: C-Bb / Ab / G-Bb / C-Ab, a sigh, a long Ab, a lift and a settle. Intro EP first, hats at 3, kick/snare at 5, bass and nylon at 9; break 25-32 kick and snare out, hats, bass, EP and nylon stay; crash at 33; outro drops lead and nylon, last 4 bars EP alone. no vocals, lo-fi warmth, DJ-friendly intro/outro.
```

## lh25-wool-calendar-v1
**Style**
`lo-fi hip hop, 78 BPM, F minor, pedalled grand piano, sparse acoustic guitar, close nylon lead, soft finger bass, unhurried acoustic boom bap, swung hats, instrumental`

**Description**
```
Wool Calendar: 78 BPM, F minor, 56 bars. Fm9-Fm9-Dbmaj7-Eb9 gives the tonic two bars; warm four-voice grand piano alternates delayed holds and two-hit replies, repedalling every bar. SoCal kick on one plus a-of-two, and-of-two or a-of-three, with one paired pickup bar; snare on 2/4, quiet ghosts, soft swung hats and rare open hats. Finger bass leaves a kick unanswered. Guitar picking alternates pairs and single notes. Nylon lead Ab-G-F / Eb-C-Eb / F-Ab-F / F-Eb-Db is a close falling figure and a small rebound. Intro 1-8 keys, hats at 3, kick/snare at 5; A 9-24 bass/guitar, lead at 17; break 25-32 removes drums/bass, piano+guitar for four bars then piano alone; A2 33-48 full lead/pocket with one soft crash; outro 49-56 removes lead/guitar, last four bars drums+keys. no vocals, lo-fi warmth, DJ-friendly intro/outro
```

## lh26-quiet-ferry-v1
**Style**
`lo-fi hip hop, 76 BPM, F minor, nylon guitar opening, mellow electric piano holds, low synth pad, finger bass, very sparse acoustic boom bap with rimshots, swung hats, grand piano lead, instrumental`

**Description**
```
Quiet Ferry: 76 BPM, F minor, 56 bars. Two-chord loop Fm9 and Bbm9 alternating every bar, i-iv-i-iv, both voiced rootless (C-Eb-G-Ab, then Db-F-Ab-C) with the root left to bass and pad; mellow electric piano holds each downbeat plus one and-of-two hit in bar three, re-pedalled every bar. Very sparse SoCal boom bap: kick on one plus the a-of-three, the and-of-two in bar three; snare on 2 and 4 with rimshots on even bars, one ghost before each bar line, swung eighth hats, one open hat per four bars. Finger bass only holds the root for two beats. Nylon guitar picks single chord tones; a low pad holds F and C from bar 9. Four-bar grand piano lead of sighs: G-Eb / C / F-Ab / Eb; alternate A2 phrases delay bar two by an eighth. Intro 1-8 nylon alone, hats at 3, kick/rim and EP at 5; A 9-24 adds bass and pad, lead at 17; break 25-32 only EP and pad; A2 33-48 restores the pocket with a soft crash; outro 49-56 drops lead/nylon/pad, ends EP only. no vocals, lo-fi warmth, DJ-friendly intro/outro
```

## lh27-moth-library-v1
**Style**
`lo-fi hip hop, 76 BPM, C minor, late-night cool-down, nylon guitar intro, pedalled grand piano, low soft pad, finger bass, sparse acoustic boom bap, rimshot on even bars, swung hats, electric piano lead, instrumental`

**Description**
```
Moth Library: 76 BPM, C minor, 56 bars, late-night cool-down. Loop Cm9-Ebmaj9-Abmaj9-Fm9, i-III-VI-iv; grand piano holds bars one and three, plays one plus the and-of-three in bar two and a single beat-two hit in bar four, re-pedalled every bar, with a low root-and-fifth pad from bar 9. Sparse SoCal boom bap: kick on one plus the and-of-three in bars one and two, the a-of-two in bar three, the a-of-three in bar four; snare on 2 and 4 turning to rimshot in even bars, one ghost, swung eighth hats, one open hat per four bars. Finger bass follows the kick minus its last hit. Electric piano lead: D-Bb / G / C-Eb / C-Ab, falling from the ninth, a lone G, then a lift and a settle. Intro nylon alone, hats at 3, piano/kick/snare at 5, bass and pad at 9; break 25-32 pad and bass, nylon joins at 29; crash at 33; outro drops lead, nylon and pad, last 4 bars piano alone. no vocals, lo-fi warmth, DJ-friendly intro/outro.
```

## lh28-amber-bookend-v1
**Style**
`lo-fi hip hop, 74 BPM, Eb major, warm electric piano, soft tonewheel organ, sparse grand-piano melody, finger bass, gentle boom bap, rim answers, swung hats, instrumental`

**Description**
```
Amber Bookend: 74 BPM, Eb major, 56 bars. Ebmaj7-Abmaj7-Fm9-Bb13, warm four-voice EP holds with one late two-hit reply, sustain refreshed each bar. Sparse SoCal kick on one plus a changing and-of-three, and-of-two, a-of-three or a-of-two; snare on 2/4, even-bar rims, one ghost per bar, swung eighth hats with stronger offbeats and rare open hats. Finger bass plays only selected roots; soft organ holds. Grand-piano lead G-F-Eb / Eb-C-Eb / F-G-F / D-F-G is a falling answer with a gentle upward tail. Intro 1-8 keys, hats at 3, backbeat at 5; A 9-24 bass/organ, lead at 17; break 25-32 keys+hats for four bars, keys alone for four; A2 33-48 full lead and restrained groove with one soft crash; outro 49-56 drops lead/organ, last four bars keys only. no vocals, lo-fi warmth, DJ-friendly intro/outro
```

## lh29-cotton-ledge-v1
**Style**
`lo-fi hip hop, 74 BPM, B-flat major, pedalled jazz grand piano holds, high electric piano picking, finger bass, very sparse acoustic boom bap with rimshots, swung hats, nylon guitar lead, instrumental`

**Description**
```
Cotton Ledge: 74 BPM, Bb major, 56 bars. Loop Bbmaj9 for two bars, then Cm9 and Ebmaj9, I-I-ii-IV; grand piano holds each downbeat with a soft re-hit on the and-of-three in odd bars and on beat four in bar four, re-pedalled every bar. Very sparse SoCal boom bap: kick on one plus the and-of-two in odd bars, the a-of-three in bar two, the and-of-three in bar four; snare on 2 and 4 with rimshots on even bars, one ghost before each bar line, swung eighth hats, one open hat per four bars. Finger bass holds the root for two beats. A high electric piano picks single chord tones above the piano. Four-bar nylon lead: A-C / D / Bb-G / F-G, lifting then resting; A2 delays bar two by an eighth. Intro 1-8 piano first, hats at 3, kick/rim at 5; A 9-24 adds bass and EP picking, lead at 17; break 25-32 hats and EP picking, then piano and EP picking; A2 33-48 restores the pocket with one soft crash; outro 49-56 drops lead/EP, ends piano only. no vocals, lo-fi warmth, DJ-friendly intro/outro
```

## lh30-last-streetlamp-v1
**Style**
`lo-fi hip hop, 72 BPM, G minor, set closer, mellow electric piano with sustain, nylon guitar picking, low soft pad, finger bass, sparse acoustic boom bap, one ghost snare, swung hats, grand piano lead, instrumental`

**Description**
```
Last Streetlamp: 72 BPM, G minor, 56 bars, the closer of the set. Loop Gm9-Ebmaj9-Am7b5-D7b9, i-VI-ii-V; electric piano holds bar one, enters late on the and-of-one in bar two, plays one plus beat four in bar three, holds bar four, re-pedalled every bar, with a low root-and-fifth pad, flat fifth under Am7b5. Sparse SoCal boom bap: kick on one plus the a-of-three, the and-of-two, the a-of-three, the and-of-three; snare on 2/4 with a single ghost, swung eighth hats, one open hat per four bars. Finger bass follows the kick minus its last hit. Nylon picks single tones. Grand piano lead: A-Bb-D / G-Bb / C-A / F#-A, rising from the ninth, an echo, and the leading tone turning home. Intro EP first, hats at 3, kick/snare at 5, bass, nylon and pad at 9; break 25-32 EP, bass and pad, no drums; crash at 33; outro 49-56 lets go in order: lead, nylon and pad leave, drums stop after bar 50, bass after bar 52, EP alone, last bar one held Gm9. no vocals, lo-fi warmth, DJ-friendly intro/outro.
```
