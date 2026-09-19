# Suno 투입 프롬프트 — Astra v3 초안 확정

기준: 2026-09-12 청취 피드백. 다섯 곡의 Logic 작업은 **Suno에 전달할 작곡 초안으로 일단 마무리**한다. 아래 문서는 완성본의 품질을 보증하는 평가가 아니라, 승인한 정체성을 다음 제작 단계에 전달하는 브리프다. 음악 파일을 추가 수정하거나 Suno에 업로드한 기록은 아니다.

## 사용 방법

이전 [Suno 프롬프트](SUNO_PROMPTS.md)의 **Style + Description** 구분과 [Song Demo + Cover 사용 경험](FEEDBACK_LOG.md#suno-결과-2026-09-05-첫-투입)을 따른다.

- 각 곡의 **v3 WAV를 오디오 기준으로 사용**한다. 같은 이름의 v1/v2와 혼동하지 않는다.
- **Style / 스타일 서머리**: 띄어쓰기와 문장부호를 포함해 **100자 이하**인 한 줄만 복사한다. 아래 각 항목에 실제 글자 수를 표시했다. 글자 수 표기와 코드 블록 기호는 입력 내용이 아니다.
- **Description**: 장문의 참고용 제작 브리프다. **100자 제한 Style 입력란에 대신 붙이지 않는다.** 확장 설명을 받는 입력란이 별도로 있는 경우에만 그 입력란의 용도·한도에 맞춰 참고한다. Style을 수정하거나 문구를 보강했다면 100자 이내인지 다시 센다.
- **피할 방향**: 결과를 고를 때의 기준이다. 곡이 실제로 그쪽으로 흐를 때만 관련 문구를 보강한다. 금지어 목록을 매번 전부 추가하지 않는다.
- 기존 작업과 현재 초안이 연주곡이므로 **기본안은 Instrumental**이다. 보컬·랩·나레이션의 실제 추가 여부, 가사, 언어, 화자는 아직 정하지 않았다. 일반 편곡 설명을 가사란에 그대로 붙이지 않는다.
- 음색·선율의 주도권·그루브·감정의 진행이 우선이다. BPM·조성·변박·길이는 원본의 기준이지, Suno가 정확히 지킬 수 있는 프로그래밍 명령이 아니다. 코드와 선율의 세부는 WAV를 기준으로 삼는다.
- Source WAV의 특정 시각에 솔로·절정을 강제로 재현시키지 않는다. 이미 오디오에 담긴 전개를 참고하되, 완성 과정에서 프레이즈 길이와 연결은 자연스럽게 정리할 수 있다.
- 소리의 마감·공간·연주 표현은 발전시켜도 된다. 모든 곡을 더 크고 풍성한 마지막 후렴으로 바꾸거나, 같은 믹스 비율로 통일하는 것은 목표가 아니다.

### 업로드·Cover 안내의 범위

이전 세션에서 성공한 흐름은 Song Demo + Cover였다. 현재 화면에서는 제공되는 Audio Upload/Cover 기능을 사용한다. Suno의 [Audio Uploads 안내](https://help.suno.com/en/articles/6141569)는 조회 시점에 Basic 60초, Pro/Premier 8분 업로드를 설명한다. 아래 완곡은 Pro/Premier의 안내 한도 안에 있지만 Basic의 60초 한도는 넘는다. 계정·화면의 실제 제한을 우선한다. 짧은 구간만 허용되면 주선율과 반주의 관계가 함께 드러나는 구간을 선택한다. 여기서 WAV를 자르거나 새 파일을 만들지는 않았다.

[Cover 안내](https://help.suno.com/en/articles/2872257)는 기존 선율을 유지하며 스타일을 변환하는 용도로 설명하지만 결과의 완전한 보존을 보장하지 않는다. 오래된 [Upload Audio 안내](https://help.suno.com/en/articles/2477633)에는 120초 한도가 남아 있어 공식 문서 사이에도 차이가 있다. 모델명·슬라이더 수치·계정별 기능을 이 문서에서 고정하지 않는다. 공식 문서 조회일: 2026-09-12.

## 입력 파일과 음악 기준

WAV: `/Volumes/Netac 2TB/music/bounces/`  
Logic: `/Volumes/Netac 2TB/music/projects/`의 각 `곡명 Astra v3.logicx`  
작곡 원천: `docs/music/sketches/*-astra-v3.json`, `.mid`, `-manifest.json`

| 곡 | WAV 파일 | 템포·박자·조성 | 원본 길이 |
|---|---|---|---|
| Returning Tide | `returning-tide-astra-v3.wav` | 96 BPM, 6/8, D major | 4:15 |
| After the Rain | `after-the-rain-astra-v3.wav` | 92 BPM, 4/4, F major | 3:28.7 |
| Northbound Lights | `northbound-lights-astra-v3.wav` | 124 BPM, 4/4 + 7/8 브리지, E minor | 4:05.8 |
| Blue Window | `blue-window-astra-v3.wav` | 78 BPM, 3/4, A minor | 4:00 |
| Paper Lanterns | `paper-lanterns-astra-v3.wav` | 112 BPM, 4/4, G major | 4:08.6 |

Returning Tide의 96 BPM은 4분음표 기준이다. 6/8의 큰 점4분음표 박으로는 64 BPM에 해당한다.

## 1. Returning Tide

**정체성:** 기억과 감정이 밀려왔다 물러가는, 어택이 살아 있는 따뜻한 어쿠스틱 곡.

**최종 결정:** 스틸스트링의 선택이 맞았다. 나일론의 약한 존재감으로 되돌리지 않는다. v3에서 낮춘 베이스와 기타·피아노의 주고받기를 출발점으로 삼으며, 기타 볼륨만 높여 해결하려 하지 않는다.

**Style — 95자, 공백 포함**
```text
Warm acoustic folk, steel-string guitar and piano, gentle 6/8, soft bass and pads, instrumental
```

**Description**
```text
Develop the uploaded instrumental demo around its recurring memory-like melody and gentle 6/8 sway: 96 quarter-note BPM, or a 64 BPM dotted-quarter pulse. Keep the steel-string acoustic guitar clearly recognizable beside the grand piano. Let them hand phrases to each other instead of continuously doubling the lead. Preserve the guitar's pick attack and woody detail; give it space rather than simply making it louder. Rounded finger bass should support the melody without sitting in front of it, with warm natural drums and a quiet sustained synth cushion behind the acoustic instruments. Let emotion arrive in recurring waves, not as a hard-rock crescendo. Retain the reflective, receding ending.
```

**피할 방향:** 약하고 흐릿한 나일론 주선율, 기타를 덮는 피아노·패드, 지나치게 앞선 베이스, 디스토션 기타 중심의 폭발, 문자 그대로의 파도 효과음.

**Suno 결과에서 볼 것:** 스틸스트링이 피아노 등장 뒤에도 식별되는가? 따뜻함이 저음 과다나 음량 경쟁으로 바뀌지 않았는가?

## 2. After the Rain

**정체성:** 비가 그친 뒤에도 물웅덩이와 떨어지는 물줄기 사이를 조심스럽게 걸어가는 피아노 곡.

**최종 결정:** 초반 공백·엇박이 조금 어렵고 도입이 길지만, 뒤로 갈수록 이해되며 방향은 승인한다. 약간 늘어지는 호흡은 의도에 포함된다. 도입의 추가 축약은 완성 후 편곡에서 판단한다. 갑자기 신나게 첨벙거리는 성격이나 인위적인 첫 스트링 도약으로 되돌리지 않는다.

**Style — 98자, 공백 포함**
```text
Gentle piano-led folk, hesitant rhythm, gradual acoustic layers, subtle late strings, instrumental
```

**Description**
```text
Preserve the uploaded piano motif and the feeling of carefully finding a path between puddles after the rain. Express that image through pauses, hesitant pickups and touch, not literal rain recordings. Let the opening and first verse breathe with piano and a simple, restrained pulse; do not fill every gap. As the music becomes more understandable, bring in finger bass and acoustic guitar gradually without changing its emotional temperature. Strings should arrive later, quietly and behind the piano, adding depth rather than announcing a cinematic transformation. Avoid an abrupt jump into playful stomping or triumphant orchestration. Keep the accepted final section and gentle afterglow. The source is about three and a half minutes; preserve its character over an exact timestamp.
```

**피할 방향:** 밝고 쿵쾅거리는 행진·물장구 같은 리듬, 갑작스러운 드럼 확대, 첫 합류부터 전면에 나오는 스트링, 모든 쉼표의 제거, 비·천둥 효과음 추가.

**Suno 결과에서 볼 것:** 초반의 조심스러움이 후반의 확신과 같은 사람의 감정으로 이어지는가? 음량 증가보다 프레이즈와 화성으로 전환이 설득되는가?

## 3. Northbound Lights

**정체성:** 잘게 맞물리는 리듬과 분명한 기타·브라스 발언으로 앞으로 나아가는 멜로딕 록.

**최종 결정:** v3 기타 솔로에서 주악기의 의도가 느껴져 승인한다. 화려한 솔로 자체를 원한 것은 아니므로, 다음 단계에서 기교 과시를 더 요구하지 않는다. 브리지와 정박 복귀의 연결, 스네어·브라스의 확실한 존재감을 유지한다.

**Style — 95자, 공백 포함**
```text
Driving rock, electric guitar lead, punchy snare, brass stabs, brief 7/8, 124 BPM, instrumental
```

**Description**
```text
Keep the uploaded riff's forward motion and the push-pull between chopped guitar chords, subdivided finger bass and a clearly articulated snare. Give the staccato brass a definite musical statement rather than faint decorative fragments. Preserve the brief asymmetric bridge feel and ease back into the regular pulse without suddenly making every instrument attack at full force. In the guitar feature, let the accompaniment step aside so one melodic voice leads: sustained targets, compact runs and real breathing spaces. The goal is a recognizable solo, not an extended virtuoso display. Keep the band supportive so the guitar does not sound isolated or thin. Retain the original melodic identity and receding finish rather than adding an unrelated stadium climax.
```

**피할 방향:** 기타만 얇게 튀는 믹스, 거의 들리지 않는 브라스 장식, 쉬지 않는 속주, 모든 악기가 동시에 몰아치는 복귀, 지속 신스 코드로 리듬 틈을 메우기.

**Suno 결과에서 볼 것:** 스네어·베이스·짧은 코드가 서로 자리를 나누는가? 브라스는 분명하되 주선율을 지우지 않는가? 기타 특징 구간에서 주도권이 실제로 바뀌는가?

## 4. Blue Window

**정체성:** 여백에서 불안과 답답함이 생기는, 말이 놓일 자리를 남겨 둔 피아노 중심 곡.

**최종 결정:** 처음의 내향적 정서보다 불안과 답답함으로 흘렀지만 이 방향도 나쁘지 않다. 공백이 많다는 이유만으로 메우지 않는다. 보컬·랩·나레이션을 얹는 목적에 따라 활용 가능하며, 용도와 최종 판단은 완성본을 들은 뒤 정한다.

**Style — 92자, 공백 포함**
```text
Sparse uneasy piano, 3/4, A minor, restrained bass and drums, unresolved space, instrumental
```

**Description**
```text
Preserve the uploaded piano phrases and their large spaces. Let hesitation, unresolved harmony and the absence of sound carry the anxious, slightly claustrophobic character. Keep the accompaniment limited to small piano intervals, occasional upright bass and understated percussion; do not turn the gaps into sustained synth or string chords. This is not a relaxing meditation track and does not need a triumphant final chorus. Allow the music to become quieter and more exposed toward its ending. Keep the central register open and generate this base version as an instrumental. The emotional discomfort is an accepted direction; do not automatically correct it into warmth, reassurance or busy decoration.
```

**피할 방향:** 공백을 패드로 덮기, 편안한 수면·명상 음악으로 해석하기, 과장된 공포 효과음, 억지로 희망적인 후렴을 만들기, 목적을 정하기 전에 보컬·랩·나레이션을 모두 추가하기.

**Suno 결과에서 볼 것:** 불안한 공간이 남는가? 그 위에 말을 얹을 여지가 있는가? 지금은 완성본을 듣기 전에 용도를 한 가지로 확정하지 않는다.

**보컬 등을 선택한 뒤의 수정:** 현재 Style의 `instrumental`과 Description의 `generate this base version as an instrumental`을 제거하고, 선택한 한 가지 용도와 가사·언어·화자 방향을 별도로 정한다. 이는 다음 선택지이지 이번 기본 프롬프트에 동시에 넣을 지시가 아니다.

## 5. Paper Lanterns

**정체성:** 숨결 있는 하모니카와 움직이는 핑거베이스가 달리다가, 잠시 바람이 잦아든 듯 주변을 돌아보는 곡.

**최종 결정:** 하모니카 톤, 약 2:26의 변주, 마무리를 승인한다. 스피커에서 베이스가 상대적으로 앞서지만 크게 재조정할 필요는 없다. 하모니카의 음색·음압이 그 인상에 영향을 줬을 수 있다는 것은 사용자의 추정이며, 원인으로 확정하지 않는다.

**Style — 98자, 공백 포함**
```text
Airy folk-pop, breathy harmonica, nimble finger bass, light acoustic strums, 112 BPM, instrumental
```

**Description**
```text
Keep the uploaded harmonica tone as the central identity: human, breathy and comfortably mid-register rather than a shrill whistle or a forceful brass lead. Let the finger bass stay audible and nimble beneath light acoustic-guitar rhythm. Preserve the current balance as a starting point; avoid heavy bass cuts or an unnaturally loud harmonica imposed just to match other songs. Give the lead clarity by leaving room in the accompaniment. Retain the contrasting passage where movement briefly settles, like the wind easing while someone stops to look around, without literal wind sound effects. If the harmonica takes a feature, let it guide the phrase while the backing simplifies. Preserve the accepted drifting ending and do not convert the piece into a bombastic finale.
```

**피할 방향:** 고음 휘슬로 주선율 교체, 큰 브라스, 실제 바람 효과음, 베이스를 무조건 숨기거나 하모니카를 과도하게 증폭하기, 승인한 정지감·마무리를 없애기.

**Suno 결과에서 볼 것:** 숨결과 부유감이 유지되는가? 베이스의 존재감이 다른 곡과 다르다는 이유만으로 평준화하지 않았는가? 잠시 주변을 돌아보는 구간이 살아 있는가?

## 공통 청취 판정

첫 판단은 아래 세 가지로 좁힌다. 통과한 곡에 자동으로 다음 수정 라운드를 만들지 않는다.

1. **정체성 보존:** 핵심 선율·음색·그루브가 각 곡의 방향으로 읽히는가?
2. **서사 보존:** Blue의 불안한 공백, Paper의 정지감, Rain의 조심스러운 전환처럼 승인한 특성을 일반적인 고조 공식으로 덮지 않았는가?
3. **완성 단계의 이득:** 연주 표현·공간·질감이 초안보다 설득력 있게 발전했는가? 정밀한 믹스·길이 조정은 실제 완성본을 듣고 정한다.

새 다곡 배치를 설계할 때는 별도 [다곡 제작 지시문](MULTI_SONG_BRIEF.md)을 사용한다. 이 다섯 곡의 승인 상태와 다음 배치의 다양성 설계는 별개의 결정이다.
