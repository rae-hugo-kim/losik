# 음악 프롬프트 가이드라인 (Logic MCP 제작 파이프라인)

> 목적: 곡 의뢰 → 작곡 → 검증의 전 과정을 규정해 **결과물 퀄리티 분산을 줄인다.**
> 근거: 2026-08 세션에서 실측된 실패 사례들 (§5). 모든 신규 곡/수정 사이클은 이 문서를 따른다.

## 1. 곡 스펙 템플릿 (의뢰 시 필수 기입)

곡 하나당 아래 9개 필드가 채워져야 작곡 시작. 비어 있으면 작곡 전에 확정부터.

| 필드 | 내용 | 나쁜 예 | 좋은 예 |
|---|---|---|---|
| **정체성 한 줄** | 이 곡만의 색을 한 문장으로 | "신스웨이브 곡" | "심야 고속도로, 몽환+질주감" |
| **레퍼런스** | 방향 지표 1~2곡 (모방 아님) | (없음) | "Kavinsky Nightcall의 무게감" |
| **키/BPM/길이** | 명시적 수치 | "적당히" | "C장조 94BPM, 80마디(3:24)" |
| **진행 (기능 표기)** | 벌스/코러스 별도, 로마자 기능으로 | "마이너 4코드" | "벌스 I–vi–ii–V, 코러스 IV–V–iii–vi" |
| **훅 정체성** | 멜로디의 리듬+음정 아이디어를 언어로 | "좋은 멜로디" | "E 페달톤 모터 리듬" / "옥타브 점프 디스코 리프" |
| **편성** | §4 매핑표의 검증된 패치 기준 | "적당한 신스" | "SoCal 드럼 + 핑거베이스 + 폴리신스 + 그랜드" |
| **텍스처 계획** | 트랙별 그리드·밀도·활동구간 | (전 트랙 상시 연주) | "아르페지오는 프리코러스부터, 4분음 롤" |
| **다이내믹 아크** | 섹션별 에너지 서사 | (없음) | "인트로 얇게 → 코러스 풀 → 브릿지 푹 꺼짐" |
| **경계 처리** | 섹션 전환 장치 | (없음) | "크래시 롤 라이저 + 임팩트 + 드럼 필인" |

## 2. 작곡 규칙 (MUST)

1. **진행**: 곡마다 기능적으로 다른 진행. 조옮김만 다른 클론 금지 — 토닉 대비 (interval, quality) 시그니처로 유니크 검증.
2. **멜로디**: 훅은 손으로 쓴다. 랜덤워크 생성기 출력 금지. 훅 정체성이 한 문장으로 서술 가능해야 함.
3. **아르페지오/반주 텍스처**: 그리드(4분/8분/16분/점8분), 패턴 궤적, 밀도, 활동구간 4가지를 곡별로 분화.
4. **드럼 휴머나이즈**: 벨로시티 지터 ±8~12, 타이밍 ±6~10틱, 스윙(장르별 0~22틱). 미적용 시 메트로놈처럼 들림(실측 사례).
5. **클랩(GM39)은 단독 노출 금지** — 스네어 밑 레이어로만, 밴드 사운드에서는 제거.
6. **신스 코드는 1도+5도**만. 풀 코드 스택은 다른 트랙을 마스킹함(실측 사례). 화음 충전은 피아노/스트링 담당.
7. **베이스 절제**: 서브 영역은 2마디 1히트 수준부터 시작. 벨로시티는 드럼보다 낮게.
8. **피아노 아르페지오/컴핑에는 CC64 서스테인** 마디 단위 리페달.
9. **섹션 경계**: 라이저(크래시 롤 크레셴도) + 임팩트(크래시) + 필인(스네어 램프+탐 하강)을 기본 세트로.

## 3. 품질 게이트 (바운스 전/후 자동 검증)

- [ ] 진행 시그니처 유니크 (복수 곡 배치 시)
- [ ] 멜로디 리듬·음정 시그니처 유니크 (복수 곡 배치 시)
- [ ] **메트로놈 OFF** (이 변형판은 메트로놈을 바운스에 렌더함 — 매 임포트 후 필수)
- [ ] **믹서 스트립 실측** — 의도한 패치가 로드됐는지 (GM 폴백 "GM 기기 N" 발견 시 PC 재선정)
- [ ] 레벨 아크 실측 — 섹션별 RMS가 설계 서사와 일치
- [ ] 경계 임팩트 실측 — 경계 직후 vs 직전 +4dB 이상
- [ ] **최종 산출물: WAV 24bit** (Suno 입력용 — 2026-08-30 결정). 바운스는 AIFF로 뜨고, 리미터(-0.1dBFS) 후처리 단계에서 WAV로 변환·저장, .aif는 삭제
- [ ] 해시 대조 — 수정판이 이전판과 실제로 다른 오디오인지

## 4. 검증된 GM PC → 패치 매핑표 (실측)

2026-11-08 에 Logic 12.4 에서 128개 전부와 드럼 킷 13개를 실측했습니다. 사운드 라이브러리는 Netac 에 둔 상태이고, 팩 정의 81개 중 79개가 설치돼 있었습니다. 측정 도구는 `tools/gm_map.py`, 원자료(믹서 스트립 문자열 포함)는 `gm_patch_map.json` 입니다. 라이브러리를 바꾸면 다시 측정합니다.

- 패치 이름 일부는 Logic 이 한국어로 표시합니다(예: `톤휠 오르간` = Tonewheel Organ, `하드 록` = Hard Rock, `어쿠스틱 기타` = Acoustic Guitar).
- 비고가 비어 있으면 GM 악기와 같은 계열의 패치가 로드됩니다. 비고가 있으면 다른 악기가 로드되므로, 그 GM 악기 소리를 기대하고 쓰면 안 됩니다.

| PC | GM 악기 | 로드되는 패치 | 비고 |
|---|---|---|---|
| 0 | Acoustic Grand | Studio Grand |  |
| 1 | Bright Acoustic | Vintage Upright |  |
| 2 | Electric Grand | Concert Grand |  |
| 3 | Honky-tonk | Dark Lo-Fi Piano |  |
| 4 | E.Piano 1 | Deluxe Classic |  |
| 5 | E.Piano 2 | 80s Wave Bells |  |
| 6 | Harpsichord | Muted Clav | 하프시코드 아님 (클라비넷) |
| 7 | Clavi | 70s Funk Clav |  |
| 8 | Celesta | Toy Celesta |  |
| 9 | Glockenspiel | Toy Glockenspiel |  |
| 10 | Music Box | Mystic Vibes | 뮤직 박스 아님 (비브라폰 계열 이름) |
| 11 | Vibraphone | Vibraphone |  |
| 12 | Marimba | Marimba |  |
| 13 | Xylophone | Vibraphone | 실로폰 아님 (비브라폰) |
| 14 | Tubular Bells | Delicate Bells |  |
| 15 | Dulcimer | Digging Deeper Clav | 덜시머 아님 (클라비넷) |
| 16 | Drawbar Organ | 톤휠 오르간 |  |
| 17 | Percussive Organ | Bebop Organ |  |
| 18 | Rock Organ | Classic Rock Organ |  |
| 19 | Church Organ | Side Man Organ | 교회 오르간 아님 (재즈 오르간) |
| 20 | Reed Organ | Grand Organ |  |
| 21 | Accordion | Cheap Organ | 아코디언 아님 (오르간) |
| 22 | Harmonica | Cheap Organ | 하모니카 아님 (오르간) |
| 23 | Tango Accordion | Cheap Organ | 아코디언 아님 (오르간) |
| 24 | Nylon Guitar | Classical Acoustic Guitar |  |
| 25 | Steel Guitar | 어쿠스틱 기타 |  |
| 26 | Jazz Guitar | 하드 록 | 재즈 기타 아님 (디스토션) |
| 27 | Clean Guitar | Classical Acoustic Guitar | 일렉 기타 아님 (클래식 기타) |
| 28 | Muted Guitar | Phasing Guitar Plucks |  |
| 29 | Overdriven Guitar | Eastern Synth Guitar | 오버드라이브 아님 |
| 30 | Distortion Guitar | 하드 록 |  |
| 31 | Guitar Harmonics | 어쿠스틱 기타 |  |
| 32 | Acoustic Bass | 루트 업라이트 |  |
| 33 | Finger Bass | Simple Foundation |  |
| 34 | Pick Bass | Punchy Bottom |  |
| 35 | Fretless Bass | Punchy Bottom |  |
| 36 | Slap Bass 1 | Slap & Pop |  |
| 37 | Slap Bass 2 | Slap & Pop |  |
| 38 | Synth Bass 1 | Pulse Bass |  |
| 39 | Synth Bass 2 | Taureg Moon Bass |  |
| 40 | Violin | Studio Violins 1 |  |
| 41 | Viola | Studio Violas |  |
| 42 | Cello | Studio Cellos |  |
| 43 | Contrabass | Studio Double Basses |  |
| 44 | Tremolo Strings | Eden Park | 트레몰로 아님 (섹션 기본 주법) |
| 45 | Pizzicato Strings | Eden Park | 피치카토 아님 (섹션 기본 주법) |
| 46 | Orchestral Harp | Space Harp | 오케스트라 하프 아님 (신스) |
| 47 | Timpani | Taiko Drums | 팀파니 아님 (타이코) |
| 48 | String Ensemble 1 | Kensington |  |
| 49 | String Ensemble 2 | Bloomsbury |  |
| 50 | Synth Strings 1 | Authentic Strings |  |
| 51 | Synth Strings 2 | Space Strings |  |
| 52 | Choir Aahs | Mellotron Choir |  |
| 53 | Voice Oohs | Mellotron Choir |  |
| 54 | Synth Voice | GM 기기 11 | 저품질 GM 폴백 — 쓰지 않음 |
| 55 | Orchestra Hit | The Final Lead | 오케스트라 히트 아님 (신스 리드) |
| 56 | Trumpet | Studio Trumpet 1 |  |
| 57 | Trombone | Studio Trombone 1 |  |
| 58 | Tuba | Studio Bass Trombone | 튜바 아님 (베이스 트롬본) |
| 59 | Muted Trumpet | Sugar Hill | 뮤트 트럼펫 아님 (브라스·색소폰 섹션) |
| 60 | French Horn | Studio Baritone Sax | 프렌치 호른 아님 (바리톤 색소폰) |
| 61 | Brass Section | Sugar Hill |  |
| 62 | Synth Brass 1 | Bright Synth Brass |  |
| 63 | Synth Brass 2 | 80s Pop Synth Brass |  |
| 64 | Soprano Sax | (New) Horns | 소프라노 색소폰 아님 (알토 색소폰 — `Studio Alto Sax 1` 패치) |
| 65 | Alto Sax | Studio Alto Sax 2 |  |
| 66 | Tenor Sax | Studio Alto Sax 2 | 테너 아님 (알토) |
| 67 | Baritone Sax | (New) Horns | 바리톤 색소폰 아님 (알토 색소폰 — `Studio Alto Sax 1` 패치) |
| 68 | Oboe | Mellotron Flute | 오보에 아님 (멜로트론 플루트) |
| 69 | English Horn | Studio Baritone Sax | 잉글리시 호른 아님 (바리톤 색소폰) |
| 70 | Bassoon | Studio Bass Trombone | 바순 아님 (베이스 트롬본) |
| 71 | Clarinet | Mellotron Flute | 클라리넷 아님 (멜로트론 플루트) |
| 72 | Piccolo | Mellotron Flute | 피콜로 아님 (멜로트론 플루트) |
| 73 | Flute | Mellotron Flute | 오케스트라 플루트 아님 (멜로트론 플루트) |
| 74 | Recorder | Mellotron Flute | 리코더 아님 (멜로트론 플루트) |
| 75 | Pan Flute | Sweet Dream Flute |  |
| 76 | Blown Bottle | Mellotron Flute | 블로운 보틀 아님 (멜로트론 플루트) |
| 77 | Shakuhachi | Liquid Breath Flute |  |
| 78 | Whistle | Mellotron Flute | 휘슬 아님 (멜로트론 플루트) |
| 79 | Ocarina | Mellotron Flute | 오카리나 아님 (멜로트론 플루트) |
| 80 | Lead 1 square | Reverse Engineering |  |
| 81 | Lead 2 saw | The Final Lead |  |
| 82 | Lead 3 calliope | Sync Lead |  |
| 83 | Lead 4 chiff | Analog Horns |  |
| 84 | Lead 5 charang | 80s Starlight |  |
| 85 | Lead 6 voice | GM 기기 12 | 저품질 GM 폴백 — 쓰지 않음 |
| 86 | Lead 7 fifths | Fifth Formant Keys |  |
| 87 | Lead 8 bass+lead | Ambient Lead |  |
| 88 | Pad 1 new age | Glistening Pad |  |
| 89 | Pad 2 warm | Classic Pad |  |
| 90 | Pad 3 polysynth | Epic Cloud Formation |  |
| 91 | Pad 4 choir | GM 기기 2 | 저품질 GM 폴백 — 쓰지 않음 |
| 92 | Pad 5 bowed | Space Strings |  |
| 93 | Pad 6 metallic | Ghost Voices |  |
| 94 | Pad 7 halo | Tidal Space |  |
| 95 | Pad 8 sweep | Aurora Waves |  |
| 96 | FX 1 rain | Crystal Rain |  |
| 97 | FX 2 soundtrack | Distant Air |  |
| 98 | FX 3 crystal | Glacial Forms |  |
| 99 | FX 4 atmosphere | Pipe Ambience |  |
| 100 | FX 5 brightness | Cosmonaut Space Capsule |  |
| 101 | FX 6 goblins | Forever Riser |  |
| 102 | FX 7 echoes | Backwards Masking |  |
| 103 | FX 8 sci-fi | Dark Abyss |  |
| 104 | Sitar | 80s Starlight | 시타르 아님 |
| 105 | Banjo | 어쿠스틱 기타 | 밴조 아님 |
| 106 | Shamisen | Asian Plucked Strings |  |
| 107 | Koto | Koto |  |
| 108 | Kalimba | Sweet Overdrive Kalimba |  |
| 109 | Bagpipe | Toy Melodica | 백파이프 아님 |
| 110 | Fiddle | Authentic Strings | 피들 아님 (현악 합주) |
| 111 | Shanai | Toy Melodica | 샤나이 아님 |
| 112 | Tinkle Bell | Delicate Bells |  |
| 113 | Agogo | Agogo High |  |
| 114 | Steel Drums | GM 기기 11 | 저품질 GM 폴백 — 쓰지 않음 |
| 115 | Woodblock | Xylo Keyboard | 우드블록 아님 |
| 116 | Taiko Drum | Taiko Drums |  |
| 117 | Melodic Tom | Tom Mid High - Synthia | 패치 이름으로 보아 드럼 킷의 탐 한 조각 |
| 118 | Synth Drum | Kick 1 - Drum Synth Kit | 드럼 킷 전체가 로드됨 |
| 119 | Reverse Cymbal | Kick 1 - Tough Kit | 드럼 킷 전체가 로드됨 |
| 120 | Guitar Fret Noise | Mech Impact | 효과음 아님 |
| 121 | Breath Noise | Breathy Vox | 효과음 아님 (보컬 계열 이름) |
| 122 | Seashore | Deeper Emotion | 효과음 아님 |
| 123 | Bird Tweet | 선원 | 효과음 아님 |
| 124 | Telephone Ring | Azure Crystal Synth Bells | 효과음 아님 |
| 125 | Helicopter | Ocean Waves Modular | 효과음 아님 |
| 126 | Applause | Rain Strum | 효과음 아님 |
| 127 | Gunshot | Underwater Laser | 효과음 아님 |

**드럼 킷 (채널 10)**

| PC | 로드되는 킷 |
|---|---|
| 0 | SoCal |
| 8 | 복고풍 록 |
| 16 | Kick 1 - Tough Kit |
| 24 | Kick 1 - Drum Synth Kit |
| 25 | Kick 1 - Drum Synth Kit |
| 26 | Roots |
| 27 | SoCal |
| 28 | SoCal |
| 32 | Roots |
| 40 | Latin |
| 48 | Latin |
| 56 | Latin |
| 127 | SoCal |

**GM 번호로는 닿지 않는 패치** (설치돼 있지만 SMF 임포트로는 불러올 수 없으며, 쓰려면 트랙에 패치를 이름으로 불러오는 자동화가 필요합니다):
- `z_Legacy/Orchestral`: Harpsichord, Celesta, Oboe, Bassoon Solo, English Horn, Piccolo, Flute Solo, Clarinet Solo, Harp, Timpani, Glockenspiel, Xylophone, Tubular Bells, Crotales, French Horn Solo·French Horns·Trumpets·Trombones·Tuba·Full Brass, 합창 11종, 현악 섹션(Violins 1·2, Violas, Cellos, Basses, Full Strings 등)이 있습니다.
- `Strings/Studio Strings`: Section Instruments 중 Abbey Wood·King's Cross 가 해당합니다(Eden Park·Kensington·Bloomsbury 는 PC 44·45·48·49 로 닿습니다).
- `z_Legacy/World`: Medieval Lute, Celtic Harp, Hammered Dulcimer, Oud, Sitar, Erhu 등이 있습니다.
- Alchemy 프리셋과 Studio Horns 단일 악기 대부분도 해당합니다.
- 서양 솔로 바이올린 패치는 라이브러리에 없습니다(현악은 모두 섹션 패치입니다).

**함정 (사용 금지/주의)**:
- 비고가 적힌 번호는 GM 이름대로의 소리가 나지 않습니다. 사계 편성에서는 특히 PC 6(하프시코드), 46(하프), 47(팀파니), 60(프렌치 호른), 68·70(오보에·바순)이 해당합니다.
- `GM 기기 N` 으로 로드되는 PC 54·85·91·114 는 저품질 GM 폴백이므로 쓰지 않습니다.
- PC 48 은 이전에 "GM 기기 4" 로 폴백했지만, 라이브러리 설치 뒤 Studio Strings 섹션(Kensington)으로 로드됩니다(2026-11-08).
- PC 119(GM 리버스 심벌)는 Tough Kit 전체가 로드됩니다. 리버스 심벌 효과는 **크래시 롤 크레셴도**(벨로시티 34→112 램프)로 만듭니다.
- 표에 없는 경우(라이브러리 변경 뒤 등)는 사용 후 반드시 스트립을 실측합니다.

## 5. 실패 사례 → 규칙 매핑 (이 문서의 근거)

| 사례 | 증상 | 대응 규칙 |
|---|---|---|
| v0a 배치: 7곡 전부 i–VI–III–VII 조옮김 | "같은 곡을 키만 바꾼 느낌" | §2-1 |
| 공용 아르페지오 3공식 | "아르페지오가 다 똑같이 들림" | §2-3 |
| 고정 벨로시티 햇+노출 클랩 | "메트로놈 넣었나?" | §2-4, §2-5 |
| 메트로놈이 바운스에 렌더 | 전 곡 클릭 오염 → 전량 재바운스 | §3 게이트 |
| 신스 풀코드 스택 | "신디사이저 소리밖에 안 들림" | §2-6 |
| 808 매마디 홀드 | "베이스가 너무 부각" | §2-7 |
| 피아노 아르페지오 스타카토 | "끊어지는 느낌" | §2-8 |
| PC 48/119 오매핑 | 스트링 저품질 / 라이저 단타 | §4 함정 (PC 48 은 2026-11-08 라이브러리 설치로 해소) |

## 6. 워크플로 (고정)

```
스펙(§1) 확정 → SMF 생성 → 파서 자기검증 → Logic 임포트(템포 지문 확인)
→ 메트로놈 OFF → 프로젝트 저장(projects/) → AIFF 바운스(bounces/)
→ 리미터 -0.1 후처리 → §3 게이트 → 청취/피드백 → 버전 증가(vN)
```

- 저장 위치: 프로젝트 `/Volumes/Netac 2TB/music/projects/`, 바운스 `/Volumes/Netac 2TB/music/bounces/`, MIDI 소스는 리포 `docs/music/sketches/`
- 구버전은 삭제하지 않고 `music/_archive-*/`로 보관
- 헤드폰(블루투스) 청취는 Logic이 아니라 **바운스 파일을 Finder/QuickTime으로** (BT HFP 16kHz 강등 이슈)
- **Suno 프롬프트는 공백 포함 1,000자 이내 (MUST)** — Suno 입력 필드 상한. Description ≤ 1,000자, Style ≤ 300자. 쓰고 나서 `len()` 으로 재서 출력한다(2026-10-21: 30블록이 1,262~1,710자로 넘쳐 전량 재작성). 잘라내는 우선순위는 키·BPM·코드 루프 → 드럼 골격 → 층(패드·텍스처·퍼커션) → 구조 한 줄 → "no lead, no vocals"; 벨로시티 수치·16분 칸 번호 같은 구현 세부는 넣지 않는다. 양식은 `SUNO_PROMPTS.md` 사용 메모
- 코드는 `docs/music/tools/`(`pipeline.py` AX·SMF·계측 / `sketches.py`·`goldenhour.py` 작곡 / `round_*.py` 라운드별 수정)에 둔다 — 커널 상주 함수는 세션과 함께 휘발됨(2026-09-05 복원 비용 발생)
- **밸런스는 SMF 의 CC7 로 잡히지 않는다** (계측: star v6 1차 시도 저역-고역 차 25.1→27.4 dB, 무효). 확실한 수단은 ① 편성/음역 정리 ② 악기 교체 ③ 벨로시티 스케일. AX 페이더는 새 임포트마다 리셋되고 성공률이 랜덤
- 바운스 전/후 `band_balance()` 로 저역-고역 차(dB)를 이전판과 대조해 밸런스 변화 방향을 계측한다 (절대값이 아니라 상대 변화만 의미 있음)
- osascript 창 이름은 한글이 NFD 로 돌아올 수 있음 → NFC 정규화 후 비교 (`pipeline.windows()`). 임포트 중에는 System Events 호출이 ~2분씩 블록되므로 대기 루프는 호출 횟수가 아니라 벽시계 기준으로
- 같은 이름의 `.logicx` 가 `sketches/` 에 남아 있으면 저장 시 "대치하겠습니까?" 시트가 뜬다 (`save_project_as` 가 처리)
