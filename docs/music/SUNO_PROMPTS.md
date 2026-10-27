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
- Suno 는 스타일 필드가 짧을수록 안정적. Description 은 커스텀 모드의 가사란에 `[Instrumental]` 태그와 함께 넣거나, Cover/Extend 시 참고용.
- 코드 진행·BPM·키는 원곡 SMF 와 동일. Suno 가 키를 무시하는 경우가 많으므로 무드·악기 단어를 우선.
