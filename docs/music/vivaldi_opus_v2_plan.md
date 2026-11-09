# Vivaldi 사계 변주 v2 — opus 계획 (anthropic/claude-opus-5-5)

- 라운드 세션: `band-opus` / 브랜치 `rae-hugo-kim/band-opus`(기준 `rae-hugo-kim/vivaldi`, 2026-11-10 머지 `c3fb910`)
- 모델: **opus — `anthropic/claude-opus-5-5`** (세션 설정 모델 ID 와 킥오프 모델 일치 확인)
- 이 계획을 쓰기 전에 읽은 것은 `VIVALDI_BRIEF_V2.md`, `tools/vivaldi_data.py`, `PROMPT_GUIDELINES.md` §4, `LOGIC_LIBRARY_INVENTORY.md` §4·§4.1·§5·§6, 패치 이름 확인용 `logic_library_inventory.json` 뿐입니다(브리프 §0). 배제 장르는 없습니다(킥오프 `배제 장르:` 빈 줄).

## 공통 방침

- **장르 분산**: 12악장에 12개의 서로 다른 장르를 줍니다(아프로 하이라이프, 보사노바, 켈틱 슬립 지그, 트립합, 시네마틱 네오클래식, 심포닉 메탈, 발칸 브라스, 쿨 재즈 발라드, 스파게티 웨스턴, 다크 테크노, 네오 소울, 탱고 누에보). 장르는 악장의 템포·박자·표제·질감에서 골랐습니다.
- **§2 통과 규칙**: 주제는 한 성부만 쓰고, 출력 마디마다 리듬 변형(당김·늦은 진입·음가 2배·골격만 남기기·스윙/셔플·박자 재배열)을 걸어 원리듬 연속을 4마디 이하로 둡니다. 실효 템포는 원본 대비 ±15% 이상 옮기고, 3/8·12/8 은 다른 박자(4/4, 9/8)로 다시 묶습니다. 화성과 베이스는 장르 관용 화성으로 새로 짭니다. 주제 비율은 40~60% 이고 나머지는 자작 모티프·전주·간주·후주입니다.
- **밀도**: 전주·후주를 빼고 "울리는 층이 하나뿐인 마디"를 연속 2마디 이하로 둡니다. 점검 줄에 구간별 음/마디와 베이스 음/마디를 출력합니다.
- **출처 메타**: Mutopia Project·CC BY-SA 3.0 출처를 모든 MIDI 에 넣되, **지휘 트랙이 아니라 첫 악기 트랙 틱 0** 에 텍스트·저작권 메타로 넣습니다(앞 라운드 실측: 지휘 트랙에 메타가 있으면 Logic 이 빈 트랙을 만들어 트랙 번호가 밀림).
- **트랙 번호**: `patches={번호: …}` 의 번호는 악기 트랙 순서(1부터)입니다. 아래 표의 `#` 이 그 번호입니다. 작곡기 구현 전에 `pipeline.py` 에서 번호 규칙을 다시 확인하고, 다르면 이 계획 아래 "달라진 점" 에 적습니다.
- **바운스 범위**: 패치를 올린 뒤 마지막으로 선택된 트랙의 리전 끝이 바운스 범위가 되어 곡이 잘릴 수 있습니다(앞 라운드 실측). 그래서 ① 패치를 올리는 트랙 중 번호가 가장 큰 트랙이 마지막 마디까지 소리를 내도록 짜고, ② 바운스 전에 선택을 해제하거나 곡 끝까지 리전이 있는 트랙을 선택하는 방법을 `pipeline.py` 를 읽은 뒤 정하며, ③ 바운스 WAV 길이를 기대 길이(마디 수 × 마디 길이)와 대조해 기록합니다.
- **패치 경로 비용**: 트랙당 30–40초가 더 들어서 곡당 패치 트랙은 필요한 만큼만(0–4개) 둡니다.
- **표기**: 경로 A = GM PC 번호(`PROMPT_GUIDELINES.md` §4), B = 라이브러리 패치 이름, C = (Sampler 바탕 패치, EXS 이름). 비고가 있는 GM 번호는 실제로 로드되는 패치 소리를 원할 때만 씁니다. 저품질 폴백(54·85·91·114)은 쓰지 않습니다.

## 악장별 계획

### Spring I — 아프로 하이라이프
- **이유**: 리토르넬로의 밝은 E장조, 같은 음을 세 번 두드린 뒤 도는 짧은 음형, 새소리(트릴)와 춤추는 듯한 활기가 하이라이프의 맑은 기타 리프와 맞물리는 리듬 짜임에 어울립니다. 반복음 셀을 기타와 브라스가 주고받는 콜앤리스폰스로 풀 수 있습니다.
- **박자·BPM·마디**: 4/4, 134 BPM(원본 115 대비 +16.5%), 100마디(약 2:59)
- **주제**: solo 1–13(기본 창)
- **편성**: #1 Drums A 40 (Latin 킷) · #2 Bass A 33 (Simple Foundation) · #3 Rhythm Guitar A 25 (어쿠스틱 기타) · #4 Organ A 16 (톤휠 오르간) · #5 Theme Guitar A 24 (Classical Acoustic Guitar) · #6 Horns A 61 (Sugar Hill, 재제시)

### Spring II — 보사노바
- **이유**: Largo 의 잠든 목동, 나뭇잎이 사각이는 점음 반주와 느긋한 C♯ 단조 선율이 보사노바의 속삭이는 기타 컴핑과 부드러운 플루트 선율에 맞습니다. 3/4 를 4/4 보사 리듬(3+3+2 베이스·기타 당김)으로 다시 묶습니다.
- **박자·BPM·마디**: 4/4, 68 BPM(원본 50 대비 +36%), 52마디(약 3:04)
- **주제**: solo 2–10(기본 창)
- **편성**: #1 Drums A 0 (SoCal, 림·셰이커 대용 하이햇) · #2 Bass A 32 (루트 업라이트) · #3 Guitar A 24 (Classical Acoustic Guitar) · #4 Strings Pad A 48 (Kensington, 나뭇잎 사각임) · #5 EP A 4 (Deluxe Classic, 재제시) · #6 Flute B `Flute Solo` (주제)

### Spring III — 켈틱 슬립 지그 (9/8)
- **이유**: 시칠리아나 춤(12/8)의 목가적 길고–짧은 리듬, 백파이프 같은 지속음 위 춤곡이 켈틱 민속 무곡과 같은 계열입니다. 12/8(점4분 4개)을 9/8 슬립 지그(점4분 3개)로 다시 묶어 박 분할을 바꿉니다.
- **박자·BPM·마디**: 9/8, 4분음표 174 BPM(점4분 116, 원본 점4분 96 대비 +21%), 116마디(약 3:00)
- **주제**: solo 1–12(기본 창)
- **편성**: #1 Bass A 32 (루트 업라이트, 드론·근음) · #2 Folk Kit B `European Folk Kit` · #3 Bouzouki B `Irish Bouzouki` · #4 Harp B `Celtic Harp` (재제시) · #5 Whistle B `Celtic Tin Whistle` (주제, 끝까지 울림)

### Summer I — 트립합
- **이유**: 무더위에 지친 나른함, 짧은 한숨 동기와 긴 쉼표, 무거운 G 단조가 느리고 무거운 브레이크비트와 흐릿한 질감의 트립합과 맞습니다. 3/8 을 4/4 로 묶어 한숨 동기를 늘어진 당김음으로 바꿉니다.
- **박자·BPM·마디**: 4/4, 84 BPM, 64마디(약 3:03). 실효 템포는 맵 설계 뒤 작곡기가 계산해 ±15% 를 확인합니다.
- **주제**: violin1 1–30(기본 창)
- **편성**: #1 Drums A 0 (SoCal) · #2 Sub Bass A 39 (Taureg Moon Bass) · #3 Piano A 3 (Dark Lo-Fi Piano) · #4 Strings A 49 (Bloomsbury, 열기 같은 스웰) · #5 Vibes A 11 (Vibraphone, 재제시) · #6 Oboe B `Oboe` (주제)

### Summer II — 시네마틱 네오클래식
- **이유**: Adagio 독주 선율이 멀리서 오는 천둥(현의 트레몰로 프레스토)에 끊기는 구조는 영화음악식 피아노·현악 서사와 팀파니 천둥으로 그대로 옮길 수 있습니다. 독주는 솔로 바이올린 EXS 로 부릅니다.
- **박자·BPM·마디**: 4/4, 63 BPM(원본 45 대비 +40%), 48마디(약 3:03)
- **주제**: solo 1–8(기본 창)
- **편성**: #1 Piano A 2 (Concert Grand, 재제시) · #2 Strings A 48 (Kensington) · #3 Cellos A 42 (Studio Cellos, 대선율·베이스) · #4 Timpani B `Timpani` (천둥) · #5 Solo Violin C (`Violins 1`, `Violin (Arco)`) (주제, 끝까지 울림)

### Summer III — 심포닉 메탈
- **이유**: 폭풍 프레스토의 G 연타 트레몰로와 쏟아지는 음계는 메탈의 트레몰로 피킹·더블 베이스드럼과 같은 에너지입니다. 합창과 현악이 폭풍의 규모를 더합니다. 3/4 를 4/4 로 다시 묶습니다.
- **박자·BPM·마디**: 4/4, 180 BPM, 136마디(약 3:01). 실효 템포는 맵 설계 뒤 계산해 확인합니다.
- **주제**: violin1 1–20(기본 창)
- **편성**: #1 Drums A 8 (복고풍 록 킷) · #2 Bass A 34 (Punchy Bottom) · #3 Rhythm Guitar A 30 (하드 록) · #4 Lead Guitar A 26 (하드 록, 주제) · #5 Strings A 49 (Bloomsbury) · #6 Synth Lead A 81 (The Final Lead, 재제시) · #7 Choir B `Mixed Choir` (끝까지 울림)

### Autumn I — 발칸 브라스 (7/8)
- **이유**: 농부들의 춤과 취해서 비틀거리는 독주는 발칸 브라스 밴드의 잔치 음악과 같은 장면입니다. 4/4 를 7/8(2+2+3)로 바꿔 한 박이 짧게 꺾이는 "비틀거림"을 박자 자체로 표현합니다.
- **박자·BPM·마디**: 7/8, 4분음표 140 BPM(원본 120 대비 +17%), 120마디(약 3:00)
- **주제**: violin1 1–12(기본 창)
- **편성**: #1 Drums A 0 (SoCal, 타판 대용 킥·스네어) · #2 Trumpet A 56 (Studio Trumpet 1, 주제) · #3 Alto Sax A 65 (Studio Alto Sax 2, 재제시) · #4 Accordion B `Polka Accordion` (뒷박 화음) · #5 Tuba B `Tuba` (베이스, 끝까지 울림)

### Autumn II — 쿨 재즈 발라드
- **이유**: 잠든 취객들의 Adagio molto 는 약음기 현의 반음계 화음과 하프시코드 분산화음뿐인 정지된 밤입니다. 반음계 화성을 그대로 품을 수 있는 쿨 재즈 발라드(브러시·업라이트·피아노 보이싱·테너 색소폰)로 옮깁니다.
- **박자·BPM·마디**: 4/4, 64 BPM(원본 53 대비 +21%), 48마디(약 3:00)
- **주제**: violin1 4–14(기본 창)
- **편성**: #1 Drums A 0 (SoCal, 브러시 대용 여린 스네어·라이드) · #2 Bass A 32 (루트 업라이트) · #3 Piano A 0 (Studio Grand) · #4 Vibes A 11 (Vibraphone, 재제시) · #5 Tenor Sax B `Studio Tenor Sax 1` (주제, 끝까지 울림)

### Autumn III — 스파게티 웨스턴
- **이유**: 사냥(호른 부름, 총성, 쫓기는 짐승)은 말발굽 갤럽 리듬과 트럼펫·호른 부름, 채찍 같은 타격의 서부극 음악과 같은 장면입니다. 3/8 을 4/4 갤럽 셔플로 다시 묶습니다.
- **박자·BPM·마디**: 4/4, 112 BPM, 84마디(약 3:00). 실효 템포는 맵 설계 뒤 계산해 확인합니다.
- **주제**: violin1 1–24(기본 창)
- **편성**: #1 Drums A 0 (SoCal, 갤럽 탐·림) · #2 Bass A 32 (루트 업라이트) · #3 Guitar A 24 (Classical Acoustic Guitar, 스패니시 스트럼) · #4 Strings A 48 (Kensington) · #5 Trumpet A 56 (Studio Trumpet 1, 주제) · #6 Timpani B `Timpani` · #7 Horns B `French Horns` (재제시, 끝까지 울림)

### Winter I — 다크 테크노
- **이유**: 얼어붙어 떨리는 반복음(이 딱딱 부딪힘), 발 구르기, 차가운 바람은 시퀀서 펄스·4온더플로어 킥·차가운 패드의 테크노 언어와 직접 대응합니다.
- **박자·BPM·마디**: 4/4, 128 BPM(주제는 하프타임으로 실효 64 = 원본 140 대비 −54%), 96마디(3:00)
- **주제**: solo 4–13 (기본 1–12 에서 이동 — solo·violin1 은 1–3마디를 쉬고, 12–13마디에 solo 의 첫 하행 아르페지오가 있어 "떨림 → 쏟아짐" 을 한 성부 안에 담습니다)
- **편성**: #1 Drums A 25 (Drum Synth Kit) · #2 Pulse Bass A 38 (Pulse Bass) · #3 Pad A 94 (Tidal Space, 찬바람) · #4 Chords A 90 (Epic Cloud Formation) · #5 Lead A 80 (Reverse Engineering, 주제) · #6 Celesta B `Celesta` (재제시, 끝까지 울림)

### Winter II — 네오 소울
- **이유**: 난롯가의 따뜻한 Largo 선율과 바깥의 빗소리(현 피치카토)는 따뜻한 로즈·느슨한 드럼·색소폰 선율의 네오 소울과 같은 온도입니다. 피치카토 빗소리는 솔로 바이올린 피치카토 EXS 로 남깁니다.
- **박자·BPM·마디**: 4/4, 72 BPM(원본 46 대비 +57%), 54마디(3:00)
- **주제**: solo 1–8(기본 창)
- **편성**: #1 Drums A 0 (SoCal) · #2 Bass A 33 (Simple Foundation) · #3 Rhodes A 4 (Deluxe Classic) · #4 Sax A 65 (Studio Alto Sax 2, 주제) · #5 Piano A 0 (Studio Grand, 재제시) · #6 Pizzicato C (`Violins 1`, `Violin (Pizzicato)`) (빗소리, 끝까지 울림)

### Winter III — 탱고 누에보
- **이유**: 얼음 위를 조심스럽게 걷다 미끄러지는 F 단조 알레그로는 탱고의 마르카토 반주와 미끄러지는 레가토 선율, 극적인 단조와 맞습니다. 3/8 을 4/4 하바네라·3+3+2 탱고 리듬으로 다시 묶습니다.
- **박자·BPM·마디**: 4/4, 116 BPM, 88마디(약 3:02). 실효 템포는 맵 설계 뒤 계산해 확인합니다.
- **주제**: solo 1–24(기본 창)
- **편성**: #1 Piano A 0 (Studio Grand, 마르카토) · #2 Bass A 43 (Studio Double Basses) · #3 Strings A 48 (Kensington) · #4 Bandoneon 대용 B `Polka Accordion` (재제시) · #5 Solo Violin C (`Violins 1`, `Violin (Arco)`) (주제, 끝까지 울림)

## 패치 경로 요약

| 곡 | 패치 트랙 | 이름 |
|---|---|---|
| Spring II | #6 | `Flute Solo` |
| Spring III | #2 #3 #4 #5 | `European Folk Kit`, `Irish Bouzouki`, `Celtic Harp`, `Celtic Tin Whistle` |
| Summer I | #6 | `Oboe` |
| Summer II | #4 #5 | `Timpani`, (`Violins 1`, `Violin (Arco)`) |
| Summer III | #7 | `Mixed Choir` |
| Autumn I | #4 #5 | `Polka Accordion`, `Tuba` |
| Autumn II | #5 | `Studio Tenor Sax 1` |
| Autumn III | #6 #7 | `Timpani`, `French Horns` |
| Winter I | #6 | `Celesta` |
| Winter II | #6 | (`Violins 1`, `Violin (Pizzicato)`) |
| Winter III | #4 #5 | `Polka Accordion`, (`Violins 1`, `Violin (Arco)`) |

이름은 모두 `logic_library_inventory.json` 에 같은 이름의 행이 있음을 확인했습니다(`Oboe`·`Tuba` 는 패치만, `Violin (Arco)`·`Violin (Pizzicato)` 는 EXS 만, 나머지는 패치와 EXS 둘 다).

## 달라진 점 (구현 뒤 갱신)

작곡기 `docs/music/tools/vivaldi_opus_v2.py` 를 구현하면서 바뀐 점과 이유입니다. 실효 템포는 `BPM × L / S / 원본 BPM`(L = 원본 마디의 4분음표 수, S = 그 마디가 차지하는 출력 4분음표 수)로 작곡기가 재고, 점검 줄의 `eff_tempo` 가 그 값입니다.

- **Spring II 68 BPM·52마디 → 80 BPM·60마디**: 3/4 한 마디를 4/4 한 마디(3+3+2)로 묶으면 68 BPM 의 실효 템포가 68×3/4/50 = 1.02배라 ±15% 규칙에 걸립니다. 80 BPM 이면 1.20배이고, 길이 3:00 을 맞추려고 60마디로 늘렸습니다.
- **Autumn II 64 BPM·48마디 → 88 BPM·64마디**: 같은 이유로 64 BPM 은 64×3/4/53 = 0.91배(−9%)입니다. 하프타임(S=8)도 따져 봤지만 긴 음이 4마디씩 늘어져 선율이 끊겨서, 88 BPM(1.25배)·64마디(2:55)를 골랐습니다.
- **Spring III 실효 템포 +21% → −19%**: 계획은 점4분 116 대 96 으로 적었지만, 12/8 한 마디를 9/8 두 마디로 늘리고 둘째·넷째 점4분을 두 배로 늘리는 맵을 골라 실효는 0.81배가 됐습니다. 9/8 재배열과 ±15% 규칙은 그대로 지킵니다.
- **Autumn I 실효 템포 +17% → −33%**: 4/4 한 마디를 7/8 두 마디(박마다 2·3 묶음 번갈아)로 펼쳐 실효는 0.67배입니다. 7/8 한 마디에 4/4 한 마디를 넣으면 한 박이 잘려 선율이 무너져서 이 맵을 골랐습니다.
- **나머지 실효 템포(계획에서 "계산 뒤 확인")**: Summer I 0.84배, Summer III 0.45배, Autumn III 0.53배, Winter III 0.58배로 모두 ±15% 밖이라 BPM 을 바꾸지 않았습니다.
- **Spring I 드럼 A 40 (Latin 킷) → A 0 (SoCal)**: Latin 킷의 키 배치를 인벤토리·가이드에서 확인할 수 없어, 지난 라운드에 GM 키 배치가 확인된 SoCal 로 바꾸고 하이라이프 벨 패턴은 라이드 벨(53)로 냅니다.
- **Spring III #2 B `European Folk Kit` → A 0 (SoCal) 탐·림**: 같은 이유입니다. 인벤토리에 이 킷의 키맵이 없어 바운스 전에는 어떤 소리가 날지 알 수 없습니다. 보드란 느낌은 플로어 탐·로우 탐·림으로 냅니다. 패치 트랙 번호(3·4·5)는 그대로입니다.
- **리듬 변형 분류**: 브리프 §2 의 ② 는 "음가 2배/반" 이라 3/4→4/4 같은 박자 재배열(`regroup`)은 ①–④ 어느 쪽에도 세지 않고 §2-3(박자 옮김) 근거로만 씁니다. 점음 짝(`dot`)은 곧은 8분을 점8분+16분으로 바꾸는 박 분할 변경이라 ④ 로 셉니다. 그래서 곡마다 ①–④ 중 두 부류 이상을 따로 채웠습니다(Spring II·Autumn III 는 ③ `thin4`, Spring III·Summer II·Autumn I 은 ③ `pat` 을 더했습니다).
- **Summer II 천둥**: 주제 한 번 안의 쉬는 마디(12·24·36마디)마다 팀파니 롤을 넣었습니다. 원곡에서 독주가 쉬는 자리에 천둥이 오는 구조를 옮긴 것이고, 원곡 성부를 옮겨 쓰지는 않았습니다.
- **Winter I 대역 보정(바운스 뒤)**: 첫 바운스의 에너지 저/중/고가 96/4/0 % 라 킥(≤92)·펄스 베이스(56–74) 벨로시티를 낮추고 리드·첼레스타(80–102)를 올렸고, 그래도 96/4/0 이라 펄스 베이스 음역을 29–48 → 36–55(근음 F1 → F2)로 올렸습니다. 결과는 95/5/0 으로 거의 같아 Drum Synth Kit 킥 자체가 에너지를 차지한다고 보고, 청취 확인이 필요한 남은 위험으로 FEEDBACK_LOG 에 적었습니다.
- **바운스 범위 확인**: 12곡 WAV 길이가 기대 길이(마디 × 마디 초)와 모두 0.00초 차이입니다. "번호가 가장 큰 패치 트랙이 마지막 마디까지 울림" 설계로 충분했고, 바운스 전 재선택 같은 추가 조작은 쓰지 않았습니다.
