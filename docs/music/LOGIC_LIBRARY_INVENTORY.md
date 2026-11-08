# Logic 사운드 라이브러리 인벤토리 — 메인 세션 핸드오프 (2026-11-08)

이 문서는 Logic Pro 12.4 에 설치된 사운드 라이브러리 전체를 프로젝트 자산으로 관리하기 위한 인벤토리입니다. 2026-11-07~08 `rae-hugo-kim/vivaldi` 세션에서 라이브러리를 Netac 으로 옮기고 팩을 설치한 뒤 전체를 스캔해 만들었습니다. 사계 v2(`VIVALDI_BRIEF_V2.md`)와 이후 작곡 라운드는 악기를 고를 때 이 문서와 `PROMPT_GUIDELINES.md` §4 를 기준으로 삼습니다.

## 0. 파일과 재생성

| 파일 | 내용 | 만드는 방법 |
|---|---|---|
| `docs/music/LOGIC_LIBRARY_INVENTORY.md` (이 문서) | 요약·큐레이션·공백·핸드오프 사항 | §1 환경 설명, §4, §6, §7 은 손으로 씁니다. §2·§3·§5 의 표는 아래 도구의 stdout 섹션(`## packs`, `## patch_counts`, `## plugin_settings`, `## samples`, `## orchestral_summary`, `## orchestral_tables`)을 그대로 붙입니다 |
| `docs/music/logic_library_inventory.json` | 전체 목록: 팩 81, 악기 패치 5,502, 오디오 패치 529, Sampler 프리셋 2,369, 플러그인 프리셋 수, Samples 크기, Apple Loops, IR, GM 도달 패치, 큐레이션 664항목 | `python3 docs/music/tools/library_inventory.py` (읽기 전용, 약 2초, Logic 을 건드리지 않습니다) |
| `docs/music/gm_patch_map.json` + `PROMPT_GUIDELINES.md` §4 | GM 프로그램 128개·드럼 킷 13개가 실제로 불러오는 패치 | `python3 docs/music/tools/gm_map.py` (Logic 을 조작하므로 약 8분, `LogicLock` 사용, 프로젝트가 열려 있으면 거부) |

라이브러리가 바뀌면(팩 추가·삭제, 재배치) 두 도구를 다시 돌리고 이 문서의 표와 수치를 갱신합니다. 전체 목록은 JSON 에서 찾습니다. 예: `grep -n '"Harpsichord' docs/music/logic_library_inventory.json`.

## 1. 환경

| 항목 | 값 |
|---|---|
| Logic | Logic Pro Creator Studio 12.4 |
| 라이브러리 위치 | `/Volumes/Netac 2TB/Logic Sound Library/Logic Pro Library.bundle` — Logic 의 "사운드 라이브러리 위치 변경"으로 옮겼습니다(2026-11-08 00:58) |
| 번들 크기 | 83.7 GB (`du`) |
| 내장 디스크의 레거시 트리 | `/Library/Application Support/Logic` 1.01 GB, `/Library/Application Support/GarageBand` 0.96 GB, `/Library/Audio/Apple Loops` 0.50 GB, `/Library/Audio/Impulse Responses` 15 MB. Logic 12 는 이 트리도 함께 읽습니다. `Sampler Instruments` 에 .exs 60개가 있고 그중 27개가 `09 Orchestral` 입니다 |
| 팩 | 정의 81개 중 설치 79, 불완전 1(Skyline Heat 559/575), 미설치 1(Ellie Dixon - Swing! 데모) |
| Netac 연결 | USB2(480 Mbps)에서는 안정적이고, USB3 로 잡히면 전면·후면 포트 모두에서 끊김이 반복됐습니다(2026-11-07~08). 원인은 케이블 또는 인클로저로 좁혀졌고 아직 가리지 못했습니다 |

Netac 이 분리되면 Logic 은 악기를 전혀 불러오지 못합니다. losik 저장소의 git 본체도 같은 디스크에 있습니다.

## 2. 팩 설치 현황 (81개)

<details>
<summary>팩 전체 표 (상태·FileChecks·크기) — 도구 출력 <code>## packs</code></summary>

| 팩 | 상태 | FileChecks | 다운로드 | 설치 |
|---|---|---|---|---|
| Tone Collection | installed | 127/127 | 0.02 GB | 0.03 GB |
| Chinese Traditional | installed | 315/315 | 0.17 GB | 0.18 GB |
| Japanese Traditional | installed | 8/8 | 0.04 GB | 0.05 GB |
| Step Sequencer Kits | installed | 716/716 | 0.06 GB | 0.12 GB |
| Edges and Angles | installed | 472/472 | 0.11 GB | 0.12 GB |
| Gozadera Latina | installed | 448/448 | 0.12 GB | 0.14 GB |
| Percussion | installed | 203/203 | 0.29 GB | 0.38 GB |
| Flex and Flow | installed | 785/785 | 0.18 GB | 0.22 GB |
| Toy Box | installed | 538/538 | 0.16 GB | 0.18 GB |
| Vintage Drum Machines | installed | 378/378 | 0.02 GB | 0.03 GB |
| Transition Effects | installed | 330/330 | 0.1 GB | 0.1 GB |
| Skyline Heat | partial | 559/575 | 0.09 GB | 0.1 GB |
| Bass Amp Boutique | installed | 50/50 | 0.0 GB | 0.0 GB |
| Vision and Verse | installed | 1167/1167 | 0.26 GB | 0.3 GB |
| Keyboard Collection | installed | 308/308 | 0.2 GB | 0.24 GB |
| Backlight Bounce | installed | 670/670 | 0.12 GB | 0.15 GB |
| Alpha Waves | installed | 384/384 | 0.31 GB | 0.38 GB |
| Modular Rhythms | installed | 700/700 | 0.17 GB | 0.2 GB |
| Step Sequencer Loops | installed | 1041/1041 | 0.72 GB | 0.82 GB |
| 8-Bit Legends | installed | 720/720 | 0.11 GB | 0.15 GB |
| Vintage Synths | installed | 704/704 | 0.23 GB | 0.26 GB |
| Modern Synths | installed | 855/855 | 0.2 GB | 0.22 GB |
| Cinematic Synths | installed | 365/365 | 0.53 GB | 0.58 GB |
| Vintage Mellotron | installed | 33/33 | 0.16 GB | 0.16 GB |
| Beat Tape | installed | 486/486 | 0.15 GB | 0.17 GB |
| Studio Strings | installed | 137/137 | 1.83 GB | 1.85 GB |
| Studio Horns | installed | 128/128 | 2.35 GB | 2.39 GB |
| Vintage Breaks | installed | 100/100 | 0.04 GB | 0.04 GB |
| Hybrid Textures | installed | 271/271 | 0.18 GB | 0.25 GB |
| Vox Melodics | installed | 485/485 | 0.08 GB | 0.08 GB |
| Studio Basses | installed | 276/276 | 5.85 GB | 5.92 GB |
| Studio Pianos | installed | 230/230 | 3.51 GB | 3.52 GB |
| Acoustic Drums | installed | 336/336 | 3.53 GB | 3.96 GB |
| Electronic Drums | installed | 1150/1150 | 0.32 GB | 0.39 GB |
| Modular Melodies | installed | 305/305 | 0.17 GB | 0.18 GB |
| Magnetic Imperfections | installed | 584/584 | 0.63 GB | 0.65 GB |
| Dancefloor Rush | installed | 901/901 | 0.37 GB | 0.41 GB |
| Multi Channel Drum Kits | installed | 341/341 | 6.85 GB | 6.94 GB |
| Stereo IRs | installed | 1834/1834 | 0.69 GB | 0.92 GB |
| Surround IRs | installed | 277/277 | 0.5 GB | 0.9 GB |
| Visions | installed | 954/954 | 0.91 GB | 1.08 GB |
| Synths | installed | 987/987 | 0.88 GB | 0.95 GB |
| Eko Soul | installed | 654/654 | 0.27 GB | 0.3 GB |
| Granular Alchemy | installed | 340/340 | 0.28 GB | 0.29 GB |
| Drill Yard | installed | 654/654 | 0.38 GB | 0.43 GB |
| Boys Noize | installed | 399/399 | 0.07 GB | 0.08 GB |
| Oak Felder | installed | 822/822 | 0.4 GB | 0.47 GB |
| Mark Lettieri | installed | 239/239 | 0.05 GB | 0.05 GB |
| Soulection | installed | 636/636 | 0.21 GB | 0.22 GB |
| Tom Misch | installed | 274/274 | 0.08 GB | 0.1 GB |
| Take A Daytrip | installed | 567/567 | 0.14 GB | 0.16 GB |
| Watch the Sound | installed | 648/648 | 0.13 GB | 0.16 GB |
| TRAKGIRL | installed | 373/373 | 0.11 GB | 0.14 GB |
| PomPom | installed | 388/388 | 0.09 GB | 0.11 GB |
| Tosin Abasi | installed | 178/178 | 0.06 GB | 0.06 GB |
| The Kount | installed | 367/367 | 0.16 GB | 0.19 GB |
| Hardwell | installed | 717/717 | 0.15 GB | 0.18 GB |
| Sergio George | installed | 1076/1076 | 0.95 GB | 1.22 GB |
| Ellie Dixon - Swing! | not installed | 0/0 | 0.45 GB | 0.68 GB |
| Spatial Audio Demo Grid | installed | 1/1 | 0.3 GB | 0.31 GB |
| Manzana | installed | 2/2 | 0.26 GB | 0.36 GB |
| Kehlani - Shoulda Never | installed | 1/1 | 0.58 GB | 0.95 GB |
| Jam Pack 1 | installed | 4711/4711 | 1.07 GB | 1.4 GB |
| Jam Pack Remix Tools | installed | 4516/4516 | 0.92 GB | 1.1 GB |
| Jam Pack Rhythm Section | installed | 8727/8727 | 1.71 GB | 2.85 GB |
| Orchestral Instruments | installed | 5909/5909 | 3.61 GB | 4.25 GB |
| World | installed | 7612/7612 | 3.59 GB | 5.65 GB |
| Jam Pack Voices | installed | 2939/2939 | 0.98 GB | 1.02 GB |
| Logic 10 Instruments | installed | 3658/3658 | 9.28 GB | 13.88 GB |
| Logic Studio 2 | installed | 7206/7206 | 2.37 GB | 2.9 GB |
| GarageBand 11 | installed | 3555/3555 | 1.49 GB | 1.62 GB |
| Alchemy Atmospheric | installed | 4412/4412 | 3.44 GB | 3.89 GB |
| Alchemy Cinematic | installed | 5686/5686 | 3.03 GB | 3.66 GB |
| Alchemy Dance | installed | 8721/8721 | 2.81 GB | 3.27 GB |
| Alchemy Modern Synth | installed | 2856/2856 | 1.5 GB | 1.64 GB |
| Alchemy Textures and Effects | installed | 2239/2239 | 1.69 GB | 1.91 GB |
| Alchemy Vintage Synths | installed | 1659/1659 | 0.82 GB | 0.89 GB |
| Alchemy Modern Songwriter | installed | 3294/3294 | 1.65 GB | 2.03 GB |
| Hip Hop Essentials | installed | 2065/2065 | 0.47 GB | 0.6 GB |
| Electronic Essentials | installed | 1988/1988 | 0.52 GB | 0.66 GB |
| Studio Instrument Essentials | installed | 1038/1038 | 1.93 GB | 2.04 GB |

</details>

## 3. 콘텐츠 규모

**악기 패치 (`Patches/Instrument`, 5,502개)** — 도구 출력 `## patch_counts`

| 분류 | 패치 수 | 하위 분류 (수) |
|---|---|---|
| Bass | 30 | (루트) 29, z_Legacy 1 |
| Brass & Woodwind | 22 | Studio Horns 22 |
| Drums & Percussion | 3872 | Electronic Drums 3744, Acoustic Drums 102, Percussion 26 |
| Guitar | 5 | (루트) 3, Processed 2 |
| Keyboard | 139 | Acoustic Piano 48, Electric Piano 26, Organ 25, Mellotron 21, Clavinet 19 |
| Mallet | 16 | (루트) 9, Processed 7 |
| Strings | 10 | Studio Strings 10 |
| Synthesizer | 1314 | Bass 238, Pad 192, Keyboard 182, Soundscape 135, Arpeggiated 129, Lead 122 |
| z_Legacy | 94 | Orchestral 48, World 46 |

Audio 패치 529개 · Sampler 프리셋 번들 2303 / `/Library` 60 / GarageBand 6

**플러그인 프리셋 (`Plug-In Settings`)** — 도구 출력 `## plugin_settings`

| 플러그인 | 프리셋 수 |
|---|---|
| Alchemy | 3287 |
| Drum Kit Designer | 50 |
| Quick Sampler | 110 |
| Sample Alchemy | 32 |
| Sampler | 2303 |
| Space Designer | 1060 |
| Studio Bass | 12 |
| Studio Horns | 24 |
| Studio Piano | 16 |
| Studio Strings | 16 |
| Ultrabeat | 104 |
| Vintage Mellotron | 10 |

Sampler 프리셋(.exs) 2,369개 가운데 번들의 `z_Legacy` 가 1,659개(Orchestral 163, Synthesizer 694, Drums 489, World 69 …), `z_Internal` 이 312개(Studio Strings·Horns·Piano·Bass·Mellotron·Drum Kit Designer 의 내부 프리셋)입니다.

**샘플·루프·IR** — 도구 출력 `## samples`

| Samples 폴더 | 크기 |
|---|---|
| Alchemy Samples | 13.2 GB |
| Bass | 5.8 GB |
| Brass | 2.3 GB |
| Drums & Percussion | 21.5 GB |
| Guitar | 0.1 GB |
| Keyboard | 3.8 GB |
| Mallet | 0.1 GB |
| Other Strings | 0.1 GB |
| Strings | 1.8 GB |
| Synthesizer | 0.8 GB |
| Textures | 0.0 GB |
| Vocals | 0.0 GB |
| z_Legacy | 18.9 GB |

Apple Loops 폴더 45개 · 루프 29754개 · IR 1066개

## 4. 악기를 불러오는 세 가지 경로

작곡 파이프라인(`tools/pipeline.py`)은 SMF 를 임포트하고 GM 프로그램 번호로 악기를 고릅니다. 그래서 같은 악기라도 어느 경로에 있느냐에 따라 지금 쓸 수 있는지가 갈립니다.

| 경로 | 무엇 | 지금 파이프라인에서 | 비고 |
|---|---|---|---|
| A. GM 프로그램 번호 | SMF 의 Program Change 로 Logic 이 자동 배정하는 패치 94종(저품질 폴백 PC 54, 85, 91, 114 제외, §4 표) | **바로 사용 가능** | 현악 섹션 PC 40–45·48–50·110 · Studio Horns 단일·섹션 PC 56–61·64–67·69·70 · 피아노·EP·오르간·기타·베이스·신스 대부분 |
| B. 라이브러리 패치 (`.patch`) | 라이브러리 창에서 고르는 채널 스트립 전체(악기+이펙트) | **불가** — 트랙에 패치를 이름으로 불러오는 자동화가 필요합니다 | `z_Legacy/Orchestral` 48개(하프시코드·오보에·바순·하프·팀파니·합창 …), Studio Strings 섹션 Abbey Wood·King's Cross, Studio Horns 단일 악기 중 GM 으로 닿지 않는 것 |
| C. Sampler 프리셋 (`.exs`) | Sampler 플러그인 안에서 고르는 악기 | **불가** — Sampler 삽입 후 프리셋 로드 자동화가 필요합니다 | 주법별 오케스트라 163개(Legato·Staccato·Pizzicato·Tremolo·Trill, 키스위치 `+`), 솔로 Violin·Cello·Double Bass(Arco·Pizzicato), iOS 솔로 목관 |

B·C 자동화는 아직 없습니다(§7 핸드오프 1번). 레거시 오케스트라 패치·EXS 가운데 GM 번호로 닿는 것은 World 의 Koto(PC 107) 하나뿐입니다.

## 5. 어쿠스틱·오케스트라 팔레트 (큐레이션)

`logic_library_inventory.json` 의 `orchestral` 664항목을 악기 이름으로 묶은 표입니다. 스캔 범위는 폴더로 정했습니다(`Strings`, `Brass & Woodwind`, `z_Legacy/Orchestral`, `z_Legacy/World`, 어쿠스틱 피아노·오르간·멜로트론·말렛·기타·베이스 폴더와 Sampler 의 대응 폴더). 계열은 폴더가 한 계열이면 폴더로, 여러 계열이 섞인 폴더(Studio Horns 등)에서는 이름으로 정했습니다. 주법은 이름의 표기를 모두 읽었고, 솔로/섹션은 이름의 복수형(Violins, Flutes 등)·`Solo`·`Single Instruments` 폴더로 판단했으며 단서가 없으면 **미상**으로 두었습니다(피아노·오르간·베이스 대부분이 여기에 해당합니다).

- **GM PC** 열이 비어 있으면 경로 B·C 로만 불러올 수 있습니다.
- **주법**의 `keyswitch (+)` 는 한 프리셋에 여러 주법을 키스위치로 담은 레거시 EXS 입니다. `기본` 은 이름에 주법 표기가 없는 경우입니다.

도구 출력 `## orchestral_summary`:

| 계열 | 솔로 | 섹션/합주 | 미상 | 합계 |
|---|---|---|---|---|
| 현악 | 8 | 83 | 8 | 99 |
| 목관 | 52 | 10 | 9 | 71 |
| 금관 | 33 | 44 | 11 | 88 |
| 건반 (피아노·하프시코드·첼레스타·파이프오르간) | 4 | 5 | 99 | 108 |
| 하프·발현 (기타 포함) | 2 | 0 | 6 | 8 |
| 타악 (선율타악 포함) | 6 | 2 | 44 | 52 |
| 합창 | 0 | 37 | 5 | 42 |
| 오르간 (전자·톤휠) | 0 | 0 | 25 | 25 |
| 멜로트론 | 0 | 12 | 9 | 21 |
| 월드 | 0 | 11 | 108 | 119 |
| 일렉·업라이트 베이스 | 0 | 0 | 30 | 30 |
| 기타 | 0 | 0 | 1 | 1 |

큐레이션 항목 합계 664

<details>
<summary>계열별 악기 표 — 도구 출력 <code>## orchestral_tables</code></summary>
**현악** (37개 악기, 99항목)

| 악기 | 솔로/섹션 | 형태 | 주법 | GM PC | 위치 |
|---|---|---|---|---|---|
| Cello | 솔로 | EXS | 기본, Arco, Pizzicato | — | `z_Legacy/Strings` |
| Double Bass | 솔로 | EXS | 기본, Arco, Pizzicato | — | `z_Legacy/Strings` |
| Violin | 솔로 | EXS | Arco, Pizzicato | — | `z_Legacy/Strings` |
| Arco Strings | 섹션/합주 | EXS | Arco | — | `z_Legacy/Strings` |
| Basses | 섹션/합주 | EXS·패치 | 기본, Legato, Pizzicato, Staccato, Tremolo, Trill 1, Trill 2, keyswitch (+) | — | `z_Legacy/Orchestral/09 Strings; z_Legacy/Orchestral/Strings` |
| Cellos | 섹션/합주 | EXS·패치 | 기본, Legato, Pizzicato, Staccato, Tremolo, Trill 1, Trill 2, keyswitch (+) | — | `z_Legacy/Orchestral/09 Strings; z_Legacy/Orchestral/Strings` |
| Cinema Strings | 섹션/합주 | 패치 | 기본 | — | `z_Legacy/Orchestral/Strings` |
| Disco Strings | 섹션/합주 | EXS | 기본 | — | `z_Internal/Studio Strings/Section Instruments` |
| EXS Strings 1 | 섹션/합주 | EXS | 기본 | — | `z_Legacy/Strings` |
| EXS Strings 2 | 섹션/합주 | EXS | 기본 | — | `z_Legacy/Strings` |
| Full Strings | 섹션/합주 | EXS·패치 | 기본, Legato, Pizzicato, Staccato, Tremolo, Trill 1, Trill 2, keyswitch (+) | — | `z_Legacy/Orchestral/09 Strings; z_Legacy/Orchestral/Strings` |
| Hollywood Strings | 섹션/합주 | EXS | 기본 | — | `z_Legacy/Strings` |
| Modern Strings | 섹션/합주 | 패치 | 기본 | — | `z_Legacy/Orchestral/Strings` |
| Pop Strings | 섹션/합주 | 패치 | 기본 | — | `z_Legacy/Orchestral/Strings` |
| Romance Strings | 섹션/합주 | 패치 | 기본 | — | `z_Legacy/Orchestral/Strings` |
| Session Strings | 섹션/합주 | 패치 | 기본 | — | `z_Legacy/Orchestral/Strings` |
| Small Section | 섹션/합주 | EXS | 기본 | — | `z_Internal/Studio Strings/Section Instruments` |
| Smart Strings | 섹션/합주 | 패치 | 기본 | — | `z_Legacy/Orchestral/Strings` |
| String Ensemble | 섹션/합주 | EXS | 기본 | — | `09 Orchestral/09 Strings; z_Internal/Studio Strings/Section Instruments` |
| Strings | 섹션/합주 | EXS | 기본, Pizzicato, Staccato, Sustain | — | `z_Legacy/Strings` |
| Studio Cellos | 섹션/합주 | EXS·패치 | 기본 | 42 | `Strings/Studio Strings; z_Internal/Studio Strings/Single Instruments` |
| Studio Double Basses | 섹션/합주 | EXS·패치 | 기본 | 43 | `Strings/Studio Strings; z_Internal/Studio Strings/Single Instruments` |
| Studio Strings | 섹션/합주 | 패치 | 기본 | — | `z_Legacy/Orchestral/Strings` |
| Studio Violas | 섹션/합주 | EXS·패치 | 기본 | 41 | `Strings/Studio Strings; z_Internal/Studio Strings/Single Instruments` |
| Studio Violins 1 | 섹션/합주 | EXS·패치 | 기본 | 40 | `Strings/Studio Strings; z_Internal/Studio Strings/Single Instruments` |
| Studio Violins 2 | 섹션/합주 | EXS·패치 | 기본 | — | `Strings/Studio Strings; z_Internal/Studio Strings/Single Instruments` |
| Violas | 섹션/합주 | EXS·패치 | 기본, Legato, Pizzicato, Staccato, Tremolo, Trill 1, Trill 2, keyswitch (+) | — | `z_Legacy/Orchestral/09 Strings; z_Legacy/Orchestral/Strings` |
| Violins 1 | 섹션/합주 | EXS·패치 | 기본, Legato, Pizzicato, Staccato, Tremolo, Trill 1, Trill 2, keyswitch (+) | — | `z_Legacy/Orchestral/09 Strings; z_Legacy/Orchestral/Strings` |
| Violins 2 | 섹션/합주 | EXS·패치 | 기본, Legato, Pizzicato, Staccato, Tremolo, Trill 1, Trill 2, keyswitch (+) | — | `z_Legacy/Orchestral/09 Strings; z_Legacy/Orchestral/Strings` |
| Abbey Wood | 미상 | 패치 | 기본 | — | `Strings/Studio Strings/Section Instruments` |
| Bloomsbury | 미상 | 패치 | 기본 | 49 | `Strings/Studio Strings/Section Instruments` |
| Deep Bass | 미상 | EXS | 기본 | — | `z_Legacy/Orchestral/09 Strings` |
| Eden Park | 미상 | 패치 | 기본 | 44, 45 | `Strings/Studio Strings/Section Instruments` |
| Kensington | 미상 | 패치 | 기본 | 48 | `Strings/Studio Strings/Section Instruments` |
| King's Cross | 미상 | 패치 | 기본 | — | `Strings/Studio Strings/Section Instruments` |
| Singer Songwriter | 미상 | EXS | 기본 | — | `z_Internal/Studio Strings/Section Instruments` |
| Upright | 미상 | EXS | 기본 | — | `z_Legacy/Strings` |

**목관** (28개 악기, 71항목)

| 악기 | 솔로/섹션 | 형태 | 주법 | GM PC | 위치 |
|---|---|---|---|---|---|
| Bassoon | 솔로 | EXS | 기본 | — | `z_Legacy/Brass & Woodwinds` |
| Bassoon Solo | 솔로 | EXS·패치 | 기본, Legato, Staccato, keyswitch (+) | — | `z_Legacy/Orchestral/01 Woodwinds; z_Legacy/Orchestral/Woodwinds` |
| Clarinet | 솔로 | EXS | 기본 | — | `Sampler/Sampler Instruments/iOS Instruments; z_Legacy/Brass & Woodwinds` |
| Clarinet Solo | 솔로 | EXS·패치 | 기본, Legato, Staccato, keyswitch (+) | — | `09 Orchestral/01 Woodwinds; z_Legacy/Orchestral/01 Woodwinds; z_Legacy/Orchestral/Woodwinds` |
| English Horn | 솔로 | 패치 | 기본 | — | `z_Legacy/Orchestral/Woodwinds` |
| English Horn Solo | 솔로 | EXS | 기본, Legato, Staccato, keyswitch (+) | — | `z_Legacy/Orchestral/01 Woodwinds` |
| Flute | 솔로 | EXS | 기본 | — | `Sampler/Sampler Instruments/iOS Instruments; z_Legacy/Brass & Woodwinds` |
| Flute Solo | 솔로 | EXS·패치 | 기본, Legato, Staccato, keyswitch (+) | — | `09 Orchestral/01 Woodwinds; z_Legacy/Orchestral/01 Woodwinds; z_Legacy/Orchestral/Woodwinds` |
| Oboe | 솔로 | EXS·패치 | 기본 | — | `z_Legacy/Brass & Woodwinds; z_Legacy/Orchestral/Woodwinds` |
| Oboe Solo | 솔로 | EXS | 기본, Legato, Staccato, keyswitch (+) | — | `z_Legacy/Orchestral/01 Woodwinds` |
| Piccolo | 솔로 | EXS·패치 | 기본, Legato, Staccato, keyswitch (+) | — | `z_Legacy/Orchestral/01 Woodwinds; z_Legacy/Orchestral/Woodwinds` |
| Studio Alt Sax 1 | 솔로 | EXS | 기본 | — | `z_Internal/Studio Horns/Single Instruments` |
| Studio Alt Sax 2 | 솔로 | EXS | 기본 | — | `z_Internal/Studio Horns/Single Instruments` |
| Studio Alto Sax 1 | 솔로 | 패치 | 기본 | 64, 67 | `Brass & Woodwind/Studio Horns/Single Instruments` |
| Studio Alto Sax 2 | 솔로 | 패치 | 기본 | 65, 66 | `Brass & Woodwind/Studio Horns/Single Instruments` |
| Studio Baritone Sax | 솔로 | EXS·패치 | 기본 | 60, 69 | `Brass & Woodwind/Studio Horns/Single Instruments; z_Internal/Studio Horns/Single Instruments` |
| Studio Tenor Sax 1 | 솔로 | EXS·패치 | 기본 | — | `Brass & Woodwind/Studio Horns/Single Instruments; z_Internal/Studio Horns/Single Instruments` |
| Studio Tenor Sax 2 | 솔로 | EXS·패치 | 기본 | — | `Brass & Woodwind/Studio Horns/Single Instruments; z_Internal/Studio Horns/Single Instruments` |
| Clarinets | 섹션/합주 | EXS·패치 | 기본, Legato, Staccato, keyswitch (+) | — | `z_Legacy/Orchestral/01 Woodwinds; z_Legacy/Orchestral/Woodwinds` |
| Flutes | 섹션/합주 | EXS·패치 | 기본, Legato, Staccato, keyswitch (+) | — | `z_Legacy/Orchestral/01 Woodwinds; z_Legacy/Orchestral/Woodwinds` |
| Alto Sax | 미상 | EXS | 기본 | — | `09 Orchestral/01 Woodwinds; z_Legacy/Orchestral/01 Woodwinds` |
| Baritone Sax | 미상 | EXS | 기본 | — | `z_Legacy/Brass & Woodwinds` |
| Classical Flute | 미상 | EXS | 기본 | — | `z_Legacy/Orchestral/01 Woodwinds` |
| Pop Flute | 미상 | EXS | 기본 | — | `z_Legacy/Brass & Woodwinds` |
| Saxophone | 미상 | 패치 | 기본 | — | `z_Legacy/Orchestral/Woodwinds` |
| Soprano Sax | 미상 | EXS | 기본 | — | `z_Legacy/Brass & Woodwinds` |
| Tenor Sax | 미상 | EXS | 기본 | — | `z_Legacy/Brass & Woodwinds` |
| Twilight Drive Sax | 미상 | EXS | 기본 | — | `z_Legacy/Brass & Woodwinds` |

**금관** (34개 악기, 88항목)

| 악기 | 솔로/섹션 | 형태 | 주법 | GM PC | 위치 |
|---|---|---|---|---|---|
| French Horn Solo | 솔로 | EXS·패치 | 기본, Legato, Staccato, keyswitch (+) | — | `09 Orchestral/02 Brass; z_Legacy/Orchestral/02 Brass; z_Legacy/Orchestral/Brass` |
| Studio Bass Trombone | 솔로 | EXS·패치 | 기본 | 58, 70 | `Brass & Woodwind/Studio Horns/Single Instruments; z_Internal/Studio Horns/Single Instruments` |
| Studio Trombone 1 | 솔로 | EXS·패치 | 기본 | 57 | `Brass & Woodwind/Studio Horns/Single Instruments; z_Internal/Studio Horns/Single Instruments` |
| Studio Trombone 2 | 솔로 | EXS·패치 | 기본 | — | `Brass & Woodwind/Studio Horns/Single Instruments; z_Internal/Studio Horns/Single Instruments` |
| Studio Trombone 3 | 솔로 | EXS·패치 | 기본 | — | `Brass & Woodwind/Studio Horns/Single Instruments; z_Internal/Studio Horns/Single Instruments` |
| Studio Trumpet 1 | 솔로 | EXS·패치 | 기본 | 56 | `Brass & Woodwind/Studio Horns/Single Instruments; z_Internal/Studio Horns/Single Instruments` |
| Studio Trumpet 2 | 솔로 | EXS·패치 | 기본 | — | `Brass & Woodwind/Studio Horns/Single Instruments; z_Internal/Studio Horns/Single Instruments` |
| Studio Trumpet 3 | 솔로 | EXS·패치 | 기본 | — | `Brass & Woodwind/Studio Horns/Single Instruments; z_Internal/Studio Horns/Single Instruments` |
| Studio Trumpet 4 | 솔로 | EXS·패치 | 기본 | — | `Brass & Woodwind/Studio Horns/Single Instruments; z_Internal/Studio Horns/Single Instruments` |
| Tuba | 솔로 | 패치 | 기본 | — | `z_Legacy/Orchestral/Brass` |
| Tuba Solo | 솔로 | EXS | 기본, Legato, Staccato, keyswitch (+) | — | `09 Orchestral/02 Brass; z_Legacy/Orchestral/02 Brass` |
| Brass Ensemble | 섹션/합주 | EXS | 기본 | — | `Sampler/Sampler Instruments/iOS Instruments; z_Legacy/Brass & Woodwinds` |
| Elements Section | 섹션/합주 | 패치 | 기본 | — | `Brass & Woodwind/Studio Horns/3-Piece Section` |
| French Horns | 섹션/합주 | EXS·패치 | 기본, Crescendo, Legato, Staccato, keyswitch (+) | — | `09 Orchestral/02 Brass; z_Legacy/Orchestral/02 Brass; z_Legacy/Orchestral/Brass` |
| Full Brass | 섹션/합주 | EXS·패치 | 기본, Legato, Staccato, keyswitch (+) | — | `09 Orchestral/02 Brass; z_Legacy/Orchestral/02 Brass; z_Legacy/Orchestral/Brass` |
| Funk Horn Section | 섹션/합주 | EXS | 기본 | — | `z_Legacy/Brass & Woodwinds` |
| Horn Section | 섹션/합주 | EXS | 기본 | — | `z_Legacy/Brass & Woodwinds` |
| Pop Horn Section | 섹션/합주 | EXS | 기본 | — | `z_Legacy/Brass & Woodwinds` |
| Studio Horns - 3 piece - RnB Section | 섹션/합주 | EXS | 기본 | — | `z_Internal/Studio Horns/Section Instruments` |
| Studio Horns - 6 piece - Soul Section | 섹션/합주 | EXS | 기본 | — | `z_Internal/Studio Horns/Section Instruments` |
| Studio Horns - 7 piece - Jazz Section | 섹션/합주 | EXS | 기본 | — | `z_Internal/Studio Horns/Section Instruments` |
| Trombones | 섹션/합주 | EXS·패치 | 기본, Legato, Staccato, keyswitch (+) | — | `09 Orchestral/02 Brass; z_Legacy/Orchestral/02 Brass; z_Legacy/Orchestral/Brass` |
| Trumpet Section | 섹션/합주 | EXS | 기본 | — | `z_Legacy/Brass & Woodwinds` |
| Trumpets | 섹션/합주 | EXS·패치 | 기본, Legato, Staccato, keyswitch (+) | — | `09 Orchestral/02 Brass; z_Legacy/Orchestral/02 Brass; z_Legacy/Orchestral/Brass` |
| Chicago Street | 미상 | 패치 | 기본 | — | `Brass & Woodwind/Studio Horns/3-Piece Section` |
| French Horn | 미상 | EXS | 기본 | — | `Sampler/Sampler Instruments/iOS Instruments; z_Legacy/Brass & Woodwinds` |
| Funkhouse | 미상 | 패치 | 기본 | — | `Brass & Woodwind/Studio Horns/6-Piece Section` |
| Hell's Kitchen | 미상 | 패치 | 기본 | — | `Brass & Woodwind/Studio Horns/3-Piece Section` |
| Little Brazil | 미상 | 패치 | 기본 | — | `Brass & Woodwind/Studio Horns/6-Piece Section` |
| Memphis Blast | 미상 | 패치 | 기본 | — | `Brass & Woodwind/Studio Horns/6-Piece Section` |
| Midtown Summer Trumpet | 미상 | EXS | 기본 | — | `z_Legacy/Brass & Woodwinds` |
| Mississippi Joint | 미상 | 패치 | 기본 | — | `Brass & Woodwind/Studio Horns/7-Piece Section` |
| Strivers' Row | 미상 | 패치 | 기본 | — | `Brass & Woodwind/Studio Horns/3-Piece Section` |
| Sugar Hill | 미상 | 패치 | 기본 | 59, 61 | `Brass & Woodwind/Studio Horns/7-Piece Section` |

**건반 (피아노·하프시코드·첼레스타·파이프오르간)** (88개 악기, 108항목)

| 악기 | 솔로/섹션 | 형태 | 주법 | GM PC | 위치 |
|---|---|---|---|---|---|
| Celesta | 솔로 | EXS·패치 | 기본 | — | `z_Legacy/Orchestral/05 Keyboards; z_Legacy/Orchestral/Keyboard` |
| Harpsichord | 솔로 | EXS·패치 | 기본 | — | `z_Legacy/Orchestral/05 Keyboards; z_Legacy/Orchestral/Keyboard` |
| Flutes | 섹션/합주 | EXS | 기본 | — | `z_Legacy/Orchestral/07 Pipe Organ` |
| Flutes + 2 Octaves | 섹션/합주 | EXS | 기본 | — | `z_Legacy/Orchestral/07 Pipe Organ` |
| Flutes + Fifth | 섹션/합주 | EXS | 기본 | — | `z_Legacy/Orchestral/07 Pipe Organ` |
| Flutes + Octave | 섹션/합주 | EXS | 기본 | — | `z_Legacy/Orchestral/07 Pipe Organ` |
| Grand Piano+Strings 1 | 섹션/합주 | EXS | 기본 | — | `z_Legacy/Keyboard/Acoustic Piano` |
| 70s Glam | 미상 | 패치 | 기본 | — | `Keyboard/Acoustic Piano/Processed` |
| Amplified Piano | 미상 | EXS·패치 | 기본 | — | `Keyboard/Acoustic Piano/Processed` |
| Ballad | 미상 | 패치 | 기본 | — | `Keyboard/Acoustic Piano` |
| Bass 1 | 미상 | EXS | 기본 | — | `z_Legacy/Orchestral/07 Pipe Organ` |
| Bass 2 | 미상 | EXS | 기본 | — | `z_Legacy/Orchestral/07 Pipe Organ` |
| Below The Surface Piano | 미상 | EXS·패치 | 기본 | — | `Keyboard/Acoustic Piano/Processed` |
| Birdland Calls Piano 01 | 미상 | EXS | 기본 | — | `z_Legacy/Keyboard/Acoustic Piano` |
| Birdland Calls Piano 02 | 미상 | EXS | 기본 | — | `z_Legacy/Keyboard/Acoustic Piano` |
| Birdland Calls Piano 03 | 미상 | EXS | 기본 | — | `z_Legacy/Keyboard/Acoustic Piano` |
| Bokeh | 미상 | 패치 | 기본 | — | `Keyboard/Acoustic Piano/Processed` |
| Boogie Man Piano | 미상 | EXS·패치 | 기본 | — | `Keyboard/Acoustic Piano/Processed` |
| Capstan Piano | 미상 | 패치 | 기본 | — | `Keyboard/Acoustic Piano/Processed` |
| Classical Grand | 미상 | EXS | 기본 | — | `Keyboard/Acoustic Piano` |
| Classical Piano | 미상 | EXS | 기본 | — | `z_Legacy/Keyboard/Acoustic Piano` |
| Concert Grand | 미상 | 패치 | 기본 | 2 | `Keyboard/Acoustic Piano` |
| Concert Grand Piano | 미상 | EXS | 기본 | — | `z_Internal/Studio Piano` |
| Curious Hammers | 미상 | 패치 | 기본 | — | `Keyboard/Acoustic Piano/Processed` |
| Dark Lo-Fi Piano | 미상 | 패치 | 기본 | 3 | `Keyboard/Acoustic Piano/Processed` |
| Darkened Theater | 미상 | 패치 | 기본 | — | `Keyboard/Acoustic Piano/Processed` |
| Dusk | 미상 | 패치 | 기본 | — | `Keyboard/Acoustic Piano/Processed` |
| Early Version | 미상 | 패치 | 기본 | — | `Keyboard/Acoustic Piano` |
| Easy | 미상 | 패치 | 기본 | — | `Keyboard/Acoustic Piano` |
| Echoes Of Pompeii | 미상 | 패치 | 기본 | — | `Keyboard/Acoustic Piano/Processed` |
| Econ_Piano_1027 | 미상 | EXS | 기본 | — | `z_Legacy/Keyboard/Acoustic Piano` |
| Economy_Piano_1028 | 미상 | EXS | 기본 | — | `z_Legacy/Keyboard/Acoustic Piano` |
| Flickering | 미상 | 패치 | 기본 | — | `Keyboard/Acoustic Piano/Processed` |
| Full Organ | 미상 | EXS | 기본 | — | `z_Legacy/Orchestral/07 Pipe Organ` |
| Grain Clouds | 미상 | 패치 | 기본 | — | `Keyboard/Acoustic Piano/Processed` |
| Grand Piano | 미상 | EXS | 기본 | — | `Keyboard/Acoustic Piano` |
| Grand Piano ECO Big | 미상 | EXS | 기본 | — | `z_Legacy/Keyboard/Acoustic Piano` |
| Grand Piano ECO Small | 미상 | EXS | 기본 | — | `z_Legacy/Keyboard/Acoustic Piano` |
| Grand Piano On Stage | 미상 | EXS | 기본 | — | `z_Legacy/Keyboard/Acoustic Piano` |
| Grand Piano Punchy | 미상 | EXS | 기본 | — | `z_Legacy/Keyboard/Acoustic Piano` |
| Grand Piano+Bass | 미상 | EXS | 기본 | — | `z_Legacy/Keyboard/Acoustic Piano` |
| Grand Piano+Pad | 미상 | EXS | 기본 | — | `z_Legacy/Keyboard/Acoustic Piano` |
| Grand_Piano_1027 | 미상 | EXS | 기본 | — | `z_Legacy/Keyboard/Acoustic Piano` |
| Grand_Piano_1028 | 미상 | EXS | 기본 | — | `z_Legacy/Keyboard/Acoustic Piano` |
| Grandma's Piano | 미상 | 패치 | 기본 | — | `Keyboard/Acoustic Piano` |
| I-95 Chronicle Piano | 미상 | EXS·패치 | 기본 | — | `Keyboard/Acoustic Piano; Keyboard/Acoustic Piano/Other` |
| Ivory & Wood | 미상 | 패치 | 기본 | — | `Keyboard/Acoustic Piano` |
| Learner's Piano | 미상 | EXS·패치 | 기본 | — | `Keyboard/Acoustic Piano/Processed` |
| Lucid Recollection | 미상 | 패치 | 기본 | — | `Keyboard/Acoustic Piano/Processed` |
| Magnetic Degredation | 미상 | 패치 | 기본 | — | `Keyboard/Acoustic Piano/Processed` |
| Mellow Vibe Piano | 미상 | EXS·패치 | 기본 | — | `Keyboard/Acoustic Piano/Processed` |
| Muted Clank Keys | 미상 | EXS·패치 | 기본 | — | `Keyboard/Acoustic Piano/Processed` |
| Oak Piano Dream Synth | 미상 | 패치 | 기본 | — | `Keyboard/Acoustic Piano/Processed` |
| Old-Time Recording Keys | 미상 | EXS·패치 | 기본 | — | `Keyboard/Acoustic Piano/Processed` |
| Parallel Earth Piano | 미상 | EXS·패치 | 기본 | — | `Keyboard/Acoustic Piano/Processed` |
| Pop Producer Keys | 미상 | EXS·패치 | 기본 | — | `Keyboard/Acoustic Piano; Keyboard/Acoustic Piano/Other` |
| Principal | 미상 | EXS | 기본 | — | `z_Legacy/Orchestral/07 Pipe Organ` |
| Principal + 2 Octaves | 미상 | EXS | 기본 | — | `z_Legacy/Orchestral/07 Pipe Organ` |
| Principal + Mixture | 미상 | EXS | 기본 | — | `z_Legacy/Orchestral/07 Pipe Organ` |
| Principal + Octave | 미상 | EXS | 기본 | — | `z_Legacy/Orchestral/07 Pipe Organ` |
| Psychic Energy Piano | 미상 | 패치 | 기본 | — | `Keyboard/Acoustic Piano/Processed` |
| Record Collection Grand | 미상 | EXS·패치 | 기본 | — | `Keyboard/Acoustic Piano/Processed` |
| Reflected Sunlight | 미상 | 패치 | 기본 | — | `Keyboard/Acoustic Piano/Processed` |
| Rise Above Piano | 미상 | EXS·패치 | 기본 | — | `Keyboard/Acoustic Piano/Processed` |
| Scattered Memories | 미상 | 패치 | 기본 | — | `Keyboard/Acoustic Piano/Processed` |
| Sergio's Piano | 미상 | 패치 | 기본 | — | `Keyboard/Acoustic Piano` |
| Silver Age | 미상 | 패치 | 기본 | — | `Keyboard/Acoustic Piano` |
| Small Amped Acoustic Piano | 미상 | EXS·패치 | 기본 | — | `Keyboard/Acoustic Piano/Processed` |
| Small Time Piano | 미상 | 패치 | 기본 | — | `Keyboard/Acoustic Piano/Processed` |
| Soft Cinematic | 미상 | 패치 | 기본 | — | `Keyboard/Acoustic Piano` |
| Soft Touch | 미상 | 패치 | 기본 | — | `Keyboard/Acoustic Piano/Processed` |
| Songwriter | 미상 | 패치 | 기본 | — | `Keyboard/Acoustic Piano` |
| Squeeze Pop | 미상 | 패치 | 기본 | — | `Keyboard/Acoustic Piano` |
| Steinway Grand Piano | 미상 | EXS·패치 | 기본 | — | `Keyboard/Acoustic Piano; z_Legacy/Keyboard/Acoustic Piano` |
| Steinway Grand Piano 2 | 미상 | EXS | 기본 | — | `01 Acoustic Pianos; z_Legacy/Keyboard/Acoustic Piano` |
| Steinway Piano | 미상 | EXS | 기본 | — | `z_Legacy/Keyboard/Acoustic Piano` |
| Steinway Piano & Pad | 미상 | EXS | 기본 | — | `z_Legacy/Keyboard/Acoustic Piano` |
| Steinway Piano 2 | 미상 | EXS | 기본 | — | `01 Acoustic Pianos; Keyboard/Acoustic Piano` |
| Studio Grand | 미상 | 패치 | 기본 | 0 | `Keyboard/Acoustic Piano` |
| Studio Grand Piano | 미상 | EXS | 기본 | — | `z_Internal/Studio Piano` |
| Studio Grand Piano (One Mic) | 미상 | EXS | 기본 | — | `z_Internal/Studio Piano` |
| Subtle Dynamics Piano | 미상 | EXS·패치 | 기본 | — | `Keyboard/Acoustic Piano/Processed` |
| Thick Heat Acoustic Piano | 미상 | EXS | 기본 | — | `z_Legacy/Keyboard/Acoustic Piano` |
| Tin Can | 미상 | 패치 | 기본 | — | `Keyboard/Acoustic Piano/Processed` |
| Vintage Upright | 미상 | 패치 | 기본 | 1 | `Keyboard/Acoustic Piano` |
| Vintage Upright Piano | 미상 | EXS | 기본 | — | `z_Internal/Studio Piano` |
| Worn Tape Piano | 미상 | EXS·패치 | 기본 | — | `Keyboard/Acoustic Piano/Processed` |
| Yamaha Grand Piano | 미상 | EXS | 기본 | — | `z_Legacy/Keyboard/Acoustic Piano` |

**하프·발현 (기타 포함)** (7개 악기, 8항목)

| 악기 | 솔로/섹션 | 형태 | 주법 | GM PC | 위치 |
|---|---|---|---|---|---|
| Harp | 솔로 | EXS·패치 | 기본 | — | `z_Legacy/Orchestral/06 Harp; z_Legacy/Orchestral/Harp` |
| Acoustic Guitar | 미상 | 패치 | 기본 | 25, 31, 105 | `Guitar` |
| Acoustic Guitar KB | 미상 | EXS | 기본 | — | `Sampler/Sampler Instruments/iOS Instruments` |
| Classical Acoustic Guitar | 미상 | 패치 | 기본 | 24, 27 | `Guitar` |
| Flutter Guitar | 미상 | 패치 | 기본 | — | `Guitar/Processed` |
| Hard Rock | 미상 | 패치 | 기본 | 26, 30 | `Guitar` |
| Phasing Guitar Plucks | 미상 | 패치 | 기본 | 28 | `Guitar/Processed` |

**타악 (선율타악 포함)** (28개 악기, 52항목)

| 악기 | 솔로/섹션 | 형태 | 주법 | GM PC | 위치 |
|---|---|---|---|---|---|
| Timpani | 솔로 | EXS·패치 | 기본, SingleStrokes, Tremolo, Tremolo Crescendo, keyswitch (+) | — | `z_Legacy/Orchestral/04 Tuned Percussion; z_Legacy/Orchestral/Percussion` |
| Orchestral Kit | 섹션/합주 | EXS·패치 | 기본 | — | `z_Legacy/Orchestral/03 Percussion; z_Legacy/Orchestral/Percussion` |
| 80s Chime Vibe | 미상 | EXS·패치 | 기본 | — | `Mallet/Processed` |
| African Marimba | 미상 | EXS | 기본 | — | `Mallet` |
| Crotales | 미상 | EXS·패치 | 기본 | — | `z_Legacy/Orchestral/04 Tuned Percussion; z_Legacy/Orchestral/Percussion` |
| Echo Kalimba | 미상 | EXS·패치 | 기본 | — | `Mallet/Processed` |
| Fairy Dust | 미상 | 패치 | 기본 | — | `Mallet/Processed` |
| Giant's Doorbell | 미상 | 패치 | 기본 | — | `Mallet/Processed` |
| Glass Marimba Hard Mallet | 미상 | EXS | 기본 | — | `z_Legacy/Mallet` |
| Glass Marimba Muted | 미상 | EXS | 기본 | — | `z_Legacy/Mallet` |
| Glass Marimba Soft Mallet | 미상 | EXS | 기본 | — | `z_Legacy/Mallet` |
| Glockenspiel | 미상 | EXS·패치 | 기본 | — | `z_Legacy/Mallet; z_Legacy/Orchestral/Percussion` |
| Hit Record Marimba | 미상 | EXS·패치 | 기본 | — | `Mallet/Processed` |
| I-95 Silicon Pluck | 미상 | EXS·패치 | 기본 | — | `Mallet/Processed` |
| Lullaby Vibes | 미상 | EXS·패치 | 기본 | — | `Mallet; Mallet/Other` |
| Marimba | 미상 | EXS·패치 | 기본 | 12 | `Mallet; z_Legacy/Mallet` |
| Mini Marimba | 미상 | EXS·패치 | 기본 | — | `Mallet` |
| Music Box | 미상 | EXS·패치 | 기본 | — | `Mallet` |
| Rotary Vibraphone | 미상 | EXS | 기본 | — | `z_Legacy/Mallet` |
| Sweet Overdrive Kalimba | 미상 | EXS·패치 | 기본 | 108 | `Mallet/Processed` |
| Taped Marimba | 미상 | EXS·패치 | 기본 | — | `Mallet; Mallet/Other` |
| Toy Celesta | 미상 | EXS·패치 | 기본 | 8 | `Mallet` |
| Toy Glockenspiel | 미상 | EXS·패치 | 기본 | 9 | `Mallet` |
| Tubular Bells | 미상 | EXS·패치 | 기본 | — | `z_Legacy/Orchestral/04 Tuned Percussion; z_Legacy/Orchestral/Percussion` |
| Vibraphone | 미상 | EXS·패치 | 기본 | 11, 13 | `Mallet` |
| Vibraphone+Bass | 미상 | EXS | 기본 | — | `z_Legacy/Mallet` |
| Xylo Keyboard | 미상 | EXS·패치 | 기본 | 115 | `Mallet` |
| Xylophone | 미상 | EXS·패치 | 기본 | — | `z_Legacy/Orchestral/04 Tuned Percussion; z_Legacy/Orchestral/Percussion` |

**합창** (22개 악기, 42항목)

| 악기 | 솔로/섹션 | 형태 | 주법 | GM PC | 위치 |
|---|---|---|---|---|---|
| Boys Chamber | 섹션/합주 | EXS | Swells | — | `z_Legacy/Orchestral/10 Choir` |
| Boys Chamber Ensemble | 섹션/합주 | EXS·패치 | 기본, keyswitch (+) | — | `z_Legacy/Orchestral/10 Choir; z_Legacy/Orchestral/Choir` |
| Chamber Choir | 섹션/합주 | 패치 | 기본 | — | `z_Legacy/Orchestral/Choir` |
| Chamber Ensemble | 섹션/합주 | EXS | 기본, Swells, keyswitch (+) | — | `z_Legacy/Orchestral/10 Choir` |
| Chamber Female | 섹션/합주 | EXS | Swells | — | `z_Legacy/Orchestral/10 Choir` |
| Chamber Female Ensemble | 섹션/합주 | EXS | 기본, keyswitch (+) | — | `z_Legacy/Orchestral/10 Choir` |
| Chamber Male | 섹션/합주 | EXS | Swells | — | `z_Legacy/Orchestral/10 Choir` |
| Chamber Male Ensemble | 섹션/합주 | EXS | 기본, keyswitch (+) | — | `z_Legacy/Orchestral/10 Choir` |
| Church Choir | 섹션/합주 | EXS·패치 | 기본 | — | `z_Legacy/Orchestral/10 Choir; z_Legacy/Orchestral/Choir` |
| Classical Ensemble | 섹션/합주 | EXS·패치 | 기본, Swells, keyswitch (+) | — | `z_Legacy/Orchestral/10 Choir; z_Legacy/Orchestral/Choir` |
| Classical Female Ensemble | 섹션/합주 | EXS·패치 | 기본, keyswitch (+) | — | `z_Legacy/Orchestral/10 Choir; z_Legacy/Orchestral/Choir` |
| Classical Male Ensemble | 섹션/합주 | EXS·패치 | 기본, keyswitch (+) | — | `z_Legacy/Orchestral/10 Choir; z_Legacy/Orchestral/Choir` |
| Female Chamber Choir | 섹션/합주 | 패치 | 기본 | — | `z_Legacy/Orchestral/Choir` |
| Gospel Choir Effects Soft | 섹션/합주 | EXS | 기본 | — | `z_Legacy/Orchestral/10 Choir` |
| Gospel Ensemble | 섹션/합주 | EXS·패치 | 기본, Swells, keyswitch (+) | — | `z_Legacy/Orchestral/10 Choir; z_Legacy/Orchestral/Choir` |
| Gregorian Ensemble | 섹션/합주 | EXS | 기본, Swells | — | `z_Legacy/Orchestral/10 Choir` |
| Male Chamber Choir | 섹션/합주 | 패치 | 기본 | — | `z_Legacy/Orchestral/Choir` |
| Mixed Choir | 섹션/합주 | EXS·패치 | 기본 | — | `z_Legacy/Orchestral/10 Choir; z_Legacy/Orchestral/Choir` |
| Classical Female | 미상 | EXS | Swells | — | `z_Legacy/Orchestral/10 Choir` |
| Classical Male | 미상 | EXS | Swells | — | `z_Legacy/Orchestral/10 Choir` |
| Gospel Vocal Effects | 미상 | 패치 | 기본 | — | `z_Legacy/Orchestral/Choir` |
| Gospel Voice Effects | 미상 | EXS | 기본, keyswitch (+) | — | `z_Legacy/Orchestral/10 Choir` |

**오르간 (전자·톤휠)** (25개 악기, 25항목)

| 악기 | 솔로/섹션 | 형태 | 주법 | GM PC | 위치 |
|---|---|---|---|---|---|
| Bebop Organ | 미상 | 패치 | 기본 | 17 | `Keyboard/Organ` |
| Blips Piano | 미상 | 패치 | 기본 | — | `Keyboard/Organ` |
| Cheap Organ | 미상 | 패치 | 기본 | 21, 22, 23 | `Keyboard/Organ` |
| Classic Rock Organ | 미상 | 패치 | 기본 | 18 | `Keyboard/Organ` |
| Dreamy Smooth Vox | 미상 | 패치 | 기본 | — | `Keyboard/Organ` |
| Fixer Upper Organ | 미상 | 패치 | 기본 | — | `Keyboard/Organ` |
| Gamer's Organ | 미상 | 패치 | 기본 | — | `Keyboard/Organ/Processed` |
| Ghostly Reversed Organ | 미상 | 패치 | 기본 | — | `Keyboard/Organ/Processed` |
| Grand Organ | 미상 | 패치 | 기본 | 20 | `Keyboard/Organ` |
| Hard Rock Organ | 미상 | 패치 | 기본 | — | `Keyboard/Organ` |
| Heavy Metal Organ | 미상 | 패치 | 기본 | — | `Keyboard/Organ` |
| Industrial Design Organ | 미상 | 패치 | 기본 | — | `Keyboard/Organ/Processed` |
| Jazz Fusion Organ | 미상 | 패치 | 기본 | — | `Keyboard/Organ` |
| Jazz Organ | 미상 | 패치 | 기본 | — | `Keyboard/Organ` |
| Lighter Shade Organ | 미상 | 패치 | 기본 | — | `Keyboard/Organ` |
| Oakland Organ | 미상 | 패치 | 기본 | — | `Keyboard/Organ` |
| Pitched Vocals Organ | 미상 | 패치 | 기본 | — | `Keyboard/Organ/Processed` |
| Power Chord Organ | 미상 | 패치 | 기본 | — | `Keyboard/Organ` |
| Progressive Organ | 미상 | 패치 | 기본 | — | `Keyboard/Organ` |
| Rhythm Organ | 미상 | 패치 | 기본 | — | `Keyboard/Organ` |
| Side Man Organ | 미상 | 패치 | 기본 | 19 | `Keyboard/Organ` |
| Soul Organ | 미상 | 패치 | 기본 | — | `Keyboard/Organ` |
| Tonewheel Organ | 미상 | 패치 | 기본 | 16 | `Keyboard/Organ` |
| Top End Organ | 미상 | 패치 | 기본 | — | `Keyboard/Organ` |
| Toy Melodica | 미상 | 패치 | 기본 | 109, 111 | `Keyboard/Organ` |

**멜로트론** (21개 악기, 21항목)

| 악기 | 솔로/섹션 | 형태 | 주법 | GM PC | 위치 |
|---|---|---|---|---|---|
| Mellotron Airy Choir | 섹션/합주 | 패치 | 기본 | — | `Keyboard/Mellotron` |
| Mellotron Boys Choir | 섹션/합주 | 패치 | 기본 | — | `Keyboard/Mellotron` |
| Mellotron Brass | 섹션/합주 | 패치 | 기본 | — | `Keyboard/Mellotron` |
| Mellotron Brass Choir | 섹션/합주 | 패치 | 기본 | — | `Keyboard/Mellotron` |
| Mellotron Choir | 섹션/합주 | 패치 | 기본 | 52, 53 | `Keyboard/Mellotron` |
| Mellotron Choir & Flute | 섹션/합주 | 패치 | 기본 | — | `Keyboard/Mellotron` |
| Mellotron Cloud Choir | 섹션/합주 | 패치 | 기본 | — | `Keyboard/Mellotron` |
| Mellotron Flutes | 섹션/합주 | 패치 | 기본 | — | `Keyboard/Mellotron` |
| Mellotron GC Brass | 섹션/합주 | 패치 | 기본 | — | `Keyboard/Mellotron` |
| Mellotron Shimmering Chords | 섹션/합주 | 패치 | 기본 | — | `Keyboard/Mellotron` |
| Mellotron Strings & Flute | 섹션/합주 | 패치 | 기본 | — | `Keyboard/Mellotron` |
| Mellotron Violins | 섹션/합주 | 패치 | 기본 | — | `Keyboard/Mellotron` |
| Mellotron Brassy Sequence | 미상 | 패치 | 기본 | — | `Keyboard/Mellotron` |
| Mellotron Cello | 미상 | 패치 | 기본 | — | `Keyboard/Mellotron` |
| Mellotron Flute | 미상 | 패치 | 기본 | 68, 71, 72, 73, 74, 76, 78, 79 | `Keyboard/Mellotron` |
| Mellotron Lo-Fi Lead | 미상 | 패치 | 기본 | — | `Keyboard/Mellotron` |
| Mellotron Lush Sci-Fi Pad | 미상 | 패치 | 기본 | — | `Keyboard/Mellotron` |
| Mellotron Orchestra Swirl | 미상 | 패치 | 기본 | — | `Keyboard/Mellotron` |
| Mellotron Replicant Pad | 미상 | 패치 | 기본 | — | `Keyboard/Mellotron` |
| Mellotron Skating Pad | 미상 | 패치 | 기본 | — | `Keyboard/Mellotron` |
| Mellotron Vintage Pattern | 미상 | 패치 | 기본 | — | `Keyboard/Mellotron` |

**월드** (50개 악기, 119항목)

| 악기 | 솔로/섹션 | 형태 | 주법 | GM PC | 위치 |
|---|---|---|---|---|---|
| African Kit | 섹션/합주 | EXS·패치 | 기본 | — | `z_Legacy/World/01 African; z_Legacy/World/Percussion` |
| Asian Kit | 섹션/합주 | EXS·패치 | 기본 | — | `z_Legacy/World/02 Asian; z_Legacy/World/Percussion` |
| European Folk Kit | 섹션/합주 | EXS·패치 | 기본 | — | `z_Legacy/World/04 European; z_Legacy/World/Percussion` |
| Highlands Bagpipe Ensemble | 섹션/합주 | EXS | 기본 | — | `z_Legacy/World/04 European` |
| Indian & Middle Eastern Kit | 섹션/합주 | EXS·패치 | 기본 | — | `z_Legacy/World/08 South Asian; z_Legacy/World/Percussion` |
| Latin Kit | 섹션/합주 | EXS·패치 | 기본 | — | `z_Legacy/World/07 South American; z_Legacy/World/Percussion` |
| African Kalimba | 미상 | EXS·패치 | 기본 | — | `z_Legacy/World/01 African; z_Legacy/World/Percussion` |
| Afro-Cuban Piano | 미상 | EXS·패치 | 기본 | — | `z_Legacy/World/03 Caribbean; z_Legacy/World/Keyboard` |
| Caribbean Steel Drums | 미상 | EXS·패치 | 기본, keyswitch (+) | — | `z_Legacy/World/03 Caribbean; z_Legacy/World/Percussion` |
| Celtic Hammered Dulcimer | 미상 | EXS·패치 | 기본, keyswitch (+) | — | `z_Legacy/World/04 European; z_Legacy/World/Stringed` |
| Celtic Harp | 미상 | EXS·패치 | 기본 | — | `z_Legacy/World/04 European; z_Legacy/World/Stringed` |
| Celtic Tin Whistle | 미상 | EXS·패치 | 기본, keyswitch (+) | — | `z_Legacy/World/04 European; z_Legacy/World/Woodwinds` |
| Chinese Di Zi Flute | 미상 | EXS | 기본, keyswitch (+) | — | `z_Legacy/World/02 Asian` |
| Chinese Dizi Flute | 미상 | 패치 | 기본 | — | `z_Legacy/World/Woodwinds` |
| Chinese Erhu Violin | 미상 | EXS·패치 | 기본, keyswitch (+) | — | `z_Legacy/World/02 Asian; z_Legacy/World/Stringed` |
| Chinese Guzheng Zither | 미상 | EXS·패치 | 기본, keyswitch (+) | — | `z_Legacy/World/02 Asian; z_Legacy/World/Stringed` |
| Chinese Ruan Moon Guitar | 미상 | EXS·패치 | 기본, keyswitch (+) | — | `z_Legacy/World/02 Asian; z_Legacy/World/Stringed` |
| Chinese Xiao Flute | 미상 | EXS·패치 | 기본, keyswitch (+) | — | `z_Legacy/World/02 Asian; z_Legacy/World/Woodwinds` |
| Erhu | 미상 | EXS·패치 | 기본 | — | `Other Strings; z_Legacy/World/Stringed` |
| Guzheng | 미상 | EXS·패치 | 기본 | — | `Other Strings; z_Legacy/World/Stringed` |
| Indian Bansuri Flute | 미상 | EXS·패치 | 기본, keyswitch (+) | — | `z_Legacy/World/08 South Asian; z_Legacy/World/Woodwinds` |
| Indian Shehnai Oboe | 미상 | EXS·패치 | 기본, keyswitch (+) | — | `z_Legacy/World/08 South Asian; z_Legacy/World/Woodwinds` |
| Indian Sitar | 미상 | EXS·패치 | 기본 | — | `z_Legacy/World/08 South Asian; z_Legacy/World/Stringed` |
| Indonesian Gamelan | 미상 | EXS·패치 | 기본, keyswitch (+) | — | `z_Legacy/World/09 Southeast Asian; z_Legacy/World/Percussion` |
| Indonesian Gamelan Gongs | 미상 | EXS·패치 | 기본, keyswitch (+) | — | `z_Legacy/World/09 Southeast Asian; z_Legacy/World/Percussion` |
| Irish Bouzouki | 미상 | EXS·패치 | 기본, keyswitch (+) | — | `z_Legacy/World/04 European; z_Legacy/World/Stringed` |
| Irish Fiddle | 미상 | EXS | 기본 | — | `z_Legacy/World/04 European` |
| Japanese Koto | 미상 | EXS·패치 | 기본, keyswitch (+) | — | `z_Legacy/World/02 Asian; z_Legacy/World/Stringed` |
| Japanese Shakuhachi Flute | 미상 | EXS·패치 | 기본, keyswitch (+) | — | `z_Legacy/World/02 Asian; z_Legacy/World/Woodwinds` |
| Koto | 미상 | EXS·패치 | 기본 | 107 | `Other Strings; z_Legacy/World/Stringed` |
| Medieval Lute | 미상 | EXS·패치 | 기본 | — | `z_Legacy/World/04 European; z_Legacy/World/Stringed` |
| Medieval Recorder | 미상 | EXS·패치 | 기본, keyswitch (+) | — | `z_Legacy/World/04 European; z_Legacy/World/Woodwinds` |
| Metal Drum Palm | 미상 | EXS·패치 | 기본 | — | `z_Legacy/World/04 European; z_Legacy/World/Percussion` |
| Metal Drum Ping | 미상 | EXS·패치 | 기본 | — | `z_Legacy/World/04 European; z_Legacy/World/Percussion` |
| Metal Drum Slap | 미상 | EXS·패치 | 기본 | — | `z_Legacy/World/04 European; z_Legacy/World/Percussion` |
| Mexican Guitarron | 미상 | EXS·패치 | 기본 | — | `z_Legacy/World/07 South American; z_Legacy/World/Stringed` |
| Native American Flute | 미상 | EXS·패치 | 기본, keyswitch (+) | — | `z_Legacy/World/06 North American; z_Legacy/World/Woodwinds` |
| Persian Santoor | 미상 | EXS·패치 | 기본, keyswitch (+) | — | `z_Legacy/World/05 Middle Eastern; z_Legacy/World/Stringed` |
| Peruvian Panpipes | 미상 | EXS·패치 | 기본, keyswitch (+) | — | `z_Legacy/World/07 South American; z_Legacy/World/Woodwinds` |
| Pipa | 미상 | EXS·패치 | 기본 | — | `Other Strings; z_Legacy/World/Stringed` |
| Polka Accordion | 미상 | EXS·패치 | 기본 | — | `z_Legacy/World/04 European; z_Legacy/World/Keyboard` |
| Russian Balalaika | 미상 | EXS·패치 | 기본, keyswitch (+) | — | `z_Legacy/World/04 European; z_Legacy/World/Stringed` |
| South African Singers | 미상 | EXS·패치 | 기본, keyswitch (+) | — | `z_Legacy/World/01 African; z_Legacy/World/Voice` |
| South African Voice Effects | 미상 | EXS·패치 | 기본, keyswitch (+) | — | `z_Legacy/World/01 African; z_Legacy/World/Voice` |
| Spanish Flamenco Guitar | 미상 | EXS·패치 | 기본, keyswitch (+) | — | `z_Legacy/World/07 South American; z_Legacy/World/Stringed` |
| Tango Accordion | 미상 | EXS·패치 | 기본 | — | `z_Legacy/World/04 European; z_Legacy/World/Keyboard` |
| Tibetan Singing Bowls | 미상 | EXS·패치 | 기본 | — | `z_Legacy/World/02 Asian; z_Legacy/World/Percussion` |
| Turkish Oud Lute | 미상 | EXS·패치 | 기본, keyswitch (+) | — | `z_Legacy/World/05 Middle Eastern; z_Legacy/World/Stringed` |
| Turkish Saz Zither | 미상 | EXS·패치 | 기본 | — | `z_Legacy/World/05 Middle Eastern; z_Legacy/World/Stringed` |
| Whistler | 미상 | EXS | 기본 | — | `z_Legacy/World/04 European` |

**일렉·업라이트 베이스** (29개 악기, 30항목)

| 악기 | 솔로/섹션 | 형태 | 주법 | GM PC | 위치 |
|---|---|---|---|---|---|
| Club Ambience Upright | 미상 | 패치 | 기본 | — | `Bass` |
| Coffee Shop Monstera | 미상 | 패치 | 기본 | — | `Bass` |
| Contemporary Soul | 미상 | 패치 | 기본 | — | `Bass` |
| Crunchy Pop | 미상 | 패치 | 기본 | — | `Bass` |
| Crunchy Vintage | 미상 | 패치 | 기본 | — | `Bass` |
| Dance Clean | 미상 | 패치 | 기본 | — | `Bass` |
| Dance Swirls | 미상 | 패치 | 기본 | — | `Bass` |
| Dancefloor | 미상 | 패치 | 기본 | — | `Bass` |
| Dark Soul | 미상 | 패치 | 기본 | — | `Bass` |
| Distant Vibe | 미상 | 패치 | 기본 | — | `Bass` |
| Envelope | 미상 | 패치 | 기본 | — | `Bass` |
| Focused Sixties | 미상 | 패치 | 기본 | — | `Bass` |
| Fuzzy | 미상 | 패치 | 기본 | — | `Bass` |
| Lo-Fi Tape Upright | 미상 | 패치 | 기본 | — | `Bass` |
| Psychedelic Rock | 미상 | 패치 | 기본 | — | `Bass` |
| Punchy Bottom | 미상 | 패치 | 기본 | 34, 35 | `Bass` |
| Retro Crunch | 미상 | 패치 | 기본 | — | `Bass` |
| Retro Radio | 미상 | 패치 | 기본 | — | `Bass` |
| Rock Growl | 미상 | 패치 | 기본 | — | `Bass` |
| Rock Legend | 미상 | 패치 | Legato | — | `Bass` |
| Roots Upright | 미상 | 패치 | 기본 | 32 | `Bass` |
| Simple Foundation | 미상 | 패치 | 기본 | 33 | `Bass` |
| Slap & Pop | 미상 | 패치 | 기본 | 36, 37 | `Bass` |
| Slap & Pop Dark | 미상 | 패치 | 기본 | — | `Bass` |
| Solid Soul Electric Bass | 미상 | 패치 | 기본 | — | `Bass; Bass/z_Legacy` |
| Swirling | 미상 | 패치 | 기본 | — | `Bass` |
| Vintage Soul | 미상 | 패치 | 기본 | — | `Bass` |
| Warm & Clear | 미상 | 패치 | 기본 | — | `Bass` |
| Wide Rock | 미상 | 패치 | 기본 | — | `Bass` |

**기타** (1개 악기, 1항목)

| 악기 | 솔로/섹션 | 형태 | 주법 | GM PC | 위치 |
|---|---|---|---|---|---|
| Vintage Strat KB | 미상 | EXS | 기본 | — | `Sampler/Sampler Instruments/iOS Instruments` |

</details>

## 6. 사계(바로크 협주곡) 편성 관점 평가

| 역할 | 쓸 수 있는 것 | 공백 |
|---|---|---|
| 독주 바이올린 | Sampler `z_Legacy/Strings/Violin (Arco).exs` — 지속음 3종(sus, 마르카토 sus, 여린 시작 sus) × 12 샘플, 44.1 kHz/16 bit 스테레오, 77 MB · `Violin (Pizzicato).exs` 22 샘플 | 레가토·빠른 패시지 전용 샘플이 없어 사계의 솔로 런은 기계적으로 들릴 가능성이 큽니다(청취로 판단). 라이브러리 패치(`.patch`)로는 솔로 바이올린이 없습니다 |
| 현악 합주 (리피에노) | Studio Strings 단일 섹션 4파트(PC 40–43, Studio Violins 2 는 GM 번호 없음) + 섹션 패치 Eden Park·Kensington·Bloomsbury(PC 44·45·48·49) · 레거시 Violins 1·2/Violas/Cellos/Basses/Full Strings — 각각 Legato·Staccato·Pizzicato·Tremolo·Trill 1·2 와 키스위치 `+` | 레거시 주법 세트는 경로 C |
| 통주저음 — 하프시코드 | `z_Legacy/Orchestral/Keyboard/Harpsichord.patch`, `…/05 Keyboards/Harpsichord.exs` | GM PC 6 은 Muted Clav 를 불러옵니다 → 경로 B·C |
| 통주저음 — 첼로·콘트라베이스·류트·오르간 | Cello/Double Bass 솔로 EXS, Cellos/Basses 섹션, Medieval Lute, 파이프 오르간 11종 레지스트레이션 | Studio Cellos·Double Basses(PC 42·43) 외에는 경로 B·C |
| 목관 색채 | 솔로 Flute·Oboe·Clarinet·Bassoon·English Horn·Piccolo — 각 기본·Legato·Staccato·`+` | GM PC 68·71–74·76·78·79 는 Mellotron Flute, 69·70 은 색소폰·베이스 트롬본, 75·77 은 신스 플루트를 불러옵니다 → 경로 B·C |
| 금관·팀파니 | French Horn Solo·섹션, Trumpets·Trombones·Full Brass(각 Legato·Staccato·`+`), Timpani 4종(기본·SingleStrokes·Tremolo·Tremolo Crescendo) | GM 47 은 Taiko, 60 은 바리톤 색소폰 → 경로 B·C |
| 합창 | 레거시 합창 패치 11종, EXS 31종(Chamber·Classical·Gospel·Gregorian·Boys, Swells 포함) | 경로 B·C |

GM 번호로 쓸 때 반드시 피할 함정은 `PROMPT_GUIDELINES.md` §4 "함정" 절에 있습니다(PC 6·46·47·60·68·70, 저품질 GM 폴백 54, 85, 91, 114).

## 7. 핸드오프 — 메인 세션에서 정하거나 이어서 할 것

1. **패치 이름 로드 자동화 (경로 B·C)**: 오케스트라 악기 대부분이 여기에 걸려 있습니다. 후보 방식은 ① 라이브러리 창을 접근성(AX)으로 조작해 트랙에 패치 적용, ② 채널 스트립 설정(`.cst`) 파일 로드, ③ 악기를 미리 올린 Logic 템플릿 프로젝트에 MIDI 리전만 임포트입니다. 하나의 작업 단위로 따로 진행해야 합니다. 이 자동화가 없으면 v2 는 경로 A 악기(현악 섹션·Studio Horns·피아노·오르간·기타·베이스·신스)만으로 진행합니다.
2. **솔로 바이올린 판정**: `Violin (Arco).exs` 를 Logic 에서 직접 들어 보고 사계 독주에 쓸 만한지 정합니다. 부족하면 전문 솔로 바이올린 음원 구매를 검토합니다(구매해도 1번 자동화가 있어야 파이프라인에서 쓸 수 있습니다).
3. **Netac 연결**: USB3 끊김 원인을 가립니다. 다른 10 Gbps 케이블로 한 번 더 시험하거나 인클로저를 교체합니다. 그때까지는 USB2 로 두는 편이 안전합니다.
4. **팩 잔여**: Skyline Heat 재설치(559/575), Ellie Dixon - Swing! 데모는 선택입니다.
5. **lo-fi 브리프 §4 문구**: `LOFI_HIPHOP_SET_BRIEF.md:24` 의 "검증된 GM PC 만(§4)" 은 §4 가 128개 전수 표가 되면서 뜻이 넓어졌습니다. lo-fi 세션에서 `VIVALDI_BRIEF_V2.md` 의 악기 규칙(폴백 금지, 비고 번호는 실제 패치 소리를 원할 때만)과 같은 식으로 고치면 됩니다.
6. **재측정 규약**: 라이브러리를 바꾸면 `gm_map.py`(Logic 이 비어 있을 때)와 `library_inventory.py` 를 다시 돌리고, §4 표·이 문서·`VIVALDI_BRIEF_V2.md` §3 의 악기 문장을 갱신합니다.

## 8. 관련 문서

- `PROMPT_GUIDELINES.md` §4 — GM PC → 패치 128행 표, 드럼 킷, 닿지 않는 패치, 함정이 있습니다.
- `VIVALDI_BRIEF_V2.md` — 장르 자유 v2 브리프이고, 악기 규칙은 §3 에 있습니다.
- `FEEDBACK_LOG.md` `## 2026-11-07 사계 v2 방향` — 라이브러리 이전·설치·Netac 연결 경위와 실측이 있습니다.
- `tools/gm_map.py`, `tools/library_inventory.py` — 측정 도구입니다.
