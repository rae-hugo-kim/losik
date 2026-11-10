# Vivaldi 사계 변주 v2 — fable 계획 (anthropic/claude-fable-5-1, 2026-11-09)

브리프 `VIVALDI_BRIEF_V2.md` §0 읽기 목록(브리프, `vivaldi_data.py`, `PROMPT_GUIDELINES.md` §4, `LOGIC_LIBRARY_INVENTORY.md` §4·§4.1·§5·§6)만 읽고 세운 계획입니다. 배제 장르는 없습니다(킥오프 `배제 장르:` 빈 줄). 장르는 악장의 템포·박자·표제·질감에서 골랐고, 12곡이 한두 장르로 모이지 않게 어쿠스틱 민속 4, 실내악·오케스트라 3, 재즈·라틴 2, 전자 2, 팝 1 로 펼쳤습니다. 이전 라운드의 장르는 참고하지 않았습니다.

## 악장별 계획

| key | 장르 | 악장 성격에서 나온 이유 | 편성 (트랙 번호: 이름 — 경로) | 박자 | BPM(원본→목표) | 마디 |
|---|---|---|---|---|---|---|
| spring 1 | 챔버 팝(60s baroque pop) | 4/4 E장조 리토르넬로의 밝은 호출-응답. 하프시코드 + 현악 섹션 + 가벼운 드럼이 리토르넬로의 "돌아오는 후렴" 성격을 팝 코러스로 옮긴다 | 1 Drums: SoCal — A PC0(ch10) / 2 Bass: Simple Foundation — A 33 / 3 Harpsichord — **B `Harpsichord`** / 4 Strings: Kensington — A 48 / 5 Theme: Studio Trumpet 1 — A 56 / 6 Theme2: Harpsichord 2 — **B `Harpsichord`** | 4/4 | 115 → 98 (−15%) | 72 |
| spring 2 | 켈틱 에어(harp + tin whistle) | 3/4 Largo, 독주 선율 위에 잎이 살랑이는 반주. 3/4 를 지키고 느린 에어로 — 하프의 분산화음이 바이올린 반주의 "속삭임"을, 휘슬이 독주를 맡는다 | 1 Harp: **B `Celtic Harp`** / 2 Cellos: Studio Cellos — A 42 / 3 Theme: **B `Celtic Tin Whistle`** / 4 Theme2: Classical Acoustic Guitar — A 24 / 5 Pad: Kensington — A 48 (낮게) | 3/4 | 50 → 72 (+44%) | 72 |
| spring 3 | 타란텔라(이탈리아 민속 6/8) | 12/8 시칠리아나 목가 춤. 같은 이탈리아 6/8 춤인 타란텔라로 — 12/8 한 마디를 6/8 두 마디로 묶고 템포를 올린다. 클라리넷·류트·기타 스트럼·탬버린 | 1 Perc: Latin — A PC40(ch10, 탬버린·셰이커) / 2 Bass: 루트 업라이트 — A 32 / 3 Strum: Classical Acoustic Guitar — A 24 / 4 Lute: **B `Medieval Lute`** / 5 Theme: **B `Clarinet Solo`** / 6 Theme2: Classical Acoustic Guitar — A 24 | 6/8 | 144 → 168(4분음 기준, 점4분 112; 마디 시간 ×0.86) | 168 |
| summer 1 | 루츠 레게 / 덥 | 3/8 "더위에 늘어진" 튜티. 뒷박에 기대는 원드롭과 멜로디카가 나른함을 그대로 옮긴다. 3/8 두 마디를 4/4 한 마디로 묶는다(세 8분 + 연장) | 1 Drums: Roots — A PC26(ch10) / 2 Bass: Simple Foundation — A 33 / 3 Organ bubble: 톤휠 오르간 — A 16 / 4 Skank: 어쿠스틱 기타 — A 25 / 5 Theme: Toy Melodica — A 109(비고대로 멜로디카 소리를 원함) / 6 Theme2: 톤휠 오르간 — A 16 | 4/4 | 75 → 62 (8분음 속도 −17%) | 48 |
| summer 2 | 네오클래시컬 앰비언트 | 4/4 Adagio, 독주 선율을 천둥이 끊는다. 지속 현악 위 솔로 바이올린, 팀파니 트레몰로가 천둥, 하프가 빗방울 | 1 Strings: **C `Full Strings` + EXS `Full Strings Legato`** / 2 Harp: **B `Harp`** / 3 Timpani: **C `Timpani` + EXS `Timpani Tremolo`** / 4 Theme: **C `Violins 1` + EXS `Violin (Arco)`** / 5 Theme2: **B `Harp`** | 4/4 | 45 → 56 (+24%) | 44 |
| summer 3 | 드럼 앤 베이스 | 3/4 프레스토 폭풍. 172 BPM 브레이크비트와 서브베이스가 폭풍의 속도와 무게. 16분 런은 골격만, 3/4 를 4/4 로 다시 묶는다 | 1 Drums: Drum Synth Kit — A PC25(ch10) / 2 Sub: Pulse Bass — A 38 / 3 Pad: Epic Cloud Formation — A 90 / 4 Riser: Forever Riser — A 101 / 5 Theme: The Final Lead — A 81 / 6 Theme2: Reverse Engineering — A 80 | 4/4 | 150 → 172 (+15%) | 128 |
| autumn 1 | 폴카(수확 축제 춤) | 4/4 "농부의 춤과 노래" 리토르넬로. 2/4 움파 폴카 — 튜바 베이스, 아코디언 뒷박, 트럼펫 선율, 스네어 | 1 Drums: SoCal — A PC0(ch10) / 2 Tuba: **B `Tuba`** / 3 Accordion: **B `Polka Accordion`** / 4 Theme: Studio Trumpet 1 — A 56 / 5 Theme2: Studio Alto Sax 2 — A 65 | 2/4 | 120 → 100 (−17%) | 144 |
| autumn 2 | 성가풍 드론(미니멀 합창) | 3/4 Adagio molto, 거의 화음뿐인 "잠든 취객". 합창 지속화음과 파이프오르간 위에 잉글리시 호른이 violin1 의 긴 음을 노래한다 | 1 Choir: **B `Church Choir`** / 2 Organ: **C `Celesta` + EXS `Principal + Mixture`** / 3 Theme: **B `English Horn`** / 4 Theme2: **B `Church Choir`** (주제 재제시는 합창 상성부) / 5 Bells: Delicate Bells — A 14 | 3/4 | 53 → 40 (−25%) | 40 |
| autumn 3 | 뉴올리언스 브라스 밴드(세컨드 라인) | 3/8 사냥 호른 콜. 호른 콜을 트럼펫·트롬본 콜-앤-리스폰스로, 스네어 세컨드 라인 셔플 위에. 3/8 두 마디를 4/4 한 마디(세 8분 + 연장, 스윙)로 | 1 Drums: SoCal — A PC0(ch10) / 2 Tuba: **B `Tuba`** / 3 Trombone: Studio Trombone 1 — A 57 / 4 Sax: Studio Alto Sax 2 — A 65 / 5 Theme: Studio Trumpet 1 — A 56 / 6 Theme2: Studio Trombone 1 — A 57 | 4/4(스윙) | 80 → 96 (8분음 속도 +20%) | 72 |
| winter 1 | 탱고 누에보 | 4/4 Fm "떨림·발 구르기". 스타카토 피아노 마르카토와 아코디언(반도네온 대용), 떨리는 바이올린 — 탱고의 날선 긴장. solo 가 쉬는 1–3마디 대신 창을 4–12 로 | 1 Piano: Studio Grand — A 0 / 2 Bass: 루트 업라이트 — A 32 / 3 Accordion: **B `Tango Accordion`** / 4 Theme: **C `Violins 1` + EXS `Violin (Arco)`** / 5 Theme2: **B `Tango Accordion`** | 4/4 | 140 → 118 (−16%) | 88 |
| winter 2 | 보사노바 | 4/4 Largo, 피치카토 빗방울 위 선율. 나일론 기타 컴핑이 빗방울, 브러시 드럼, 플루트가 난롯가 선율 | 1 Drums: SoCal — A PC0(ch10, 브러시풍 약하게) / 2 Bass: 루트 업라이트 — A 32 / 3 Guitar: Classical Acoustic Guitar — A 24 / 4 Vibes: Vibraphone — A 11 / 5 Theme: **B `Flute Solo`** / 6 Theme2: Vibraphone — A 11 | 4/4 | 46 → 72 (+57%) | 56 |
| winter 3 | 신스웨이브 | 3/8 Fm "얼음 위를 걷다 미끄러지고 바람이 싸운다". 아르페지오 신스와 스윕 패드가 바람, 드럼 신스가 발걸음. 3/8 두 마디를 4/4 한 마디로 | 1 Drums: Drum Synth Kit — A PC25(ch10) / 2 Bass: Pulse Bass — A 38 / 3 Arp: Reverse Engineering — A 80 / 4 Pad: Tidal Space — A 94 / 5 Theme: The Final Lead — A 81 / 6 Theme2: Reverse Engineering — A 80 | 4/4 | 75 → 118 (8분음 속도 +57%) | 88 |

## 공통

- **주제 성부**: 전부 `solo`, autumn 2 만 `violin1`(브리프 비고). 창은 기본값, winter 1 은 4–12(1–3 은 solo 쉼), summer 1 은 1–24(3/8 24마디 = 4/4 12마디; 25–30 은 레게 템포에서 48마디 안에 두 번 들어가지 않아 자름).
- **리듬 변형**(§2-2, 곡마다 둘 이상): 그리드 미만 off-grid 음을 앞 음에 흡수하는 런 솎기 + 마디 패턴 당김(지정 박의 음을 8분 앞당김 / 다운비트 지연 / 마디 전체 지연; 패스마다 패턴 위상을 반 바퀴 돌려 이웃 패스의 원리듬 구간이 맞닿지 않게) + 장르별 스윙(brass band·bossa). 원리듬 최장 연속은 곡 전체에서 스윙 전 값으로 재서 ≤4 를 assert.
- **박자 변환**: 4/4→4/4(spring 1, summer 2, winter 1·2), 3/4→3/4(spring 2, autumn 2), 12/8→6/8(spring 3: 한 마디를 두 마디로, 틱 그대로), 3/8 두 마디→4/4 한 마디(summer 1, autumn 3, winter 3: 세 8분 + 마지막 연장), 3/4→4/4 마지막 음 연장(summer 3), 4/4→2/4(autumn 1: 한 마디를 두 마디로). 4/4 가 아닌 곡은 `build_smf(timesig=…)` 와 `bar_ticks = num*PPQ*4//den` 로 직접 계산.
- **화성**: 원곡 베이스를 쓰지 않고 주제 마디의 음 분포에 맞춘 장르 관용 루프(A·A2 구간 시작에서 위상 0; 패스 길이가 루프의 배수가 아니면 둘째 패스부터 위상이 돌아감).
- **주제 비율**: 울리는 마디 기준 40~60%. 나머지는 자작 모티프·전주·간주·후주.
- **밀도**: 층이 하나뿐인 구간은 전주·후주를 빼고 연속 2마디 이하(점검에서 assert), 구간별 트랙 음/마디와 베이스 음/마디를 점검 줄에 출력.
- **출처 메타**: 모든 MIDI 에 저작권 메타(0x02) "Theme: Vivaldi, Le quattro stagioni (Mutopia Project, CC BY-SA 3.0); arrangement 2026 band-fable (claude-fable-5-1)". (작곡 중 정정: 지휘 트랙이 아니라 **첫 악기 트랙** 틱 0 — 지휘 트랙에 넣으면 Logic 이 빈 트랙을 하나 더 만들어 패치 트랙 번호가 밀림, 2026-11-09 실측.)
- **패치 로드**: 경로 B·C 트랙 수 — spring 1: 2, spring 2: 2, spring 3: 2, summer 2: 5, autumn 1: 2, autumn 2: 4, autumn 3: 1, winter 1: 3, winter 2: 1, 나머지 0 (합 22, 곡당 30–40초×트랙). 이름은 `logic_library_inventory.json` 에서 확인했습니다(`Harpsichord`, `Celtic Harp`, `Celtic Tin Whistle`, `Medieval Lute`, `Clarinet Solo`, `Full Strings`/`Full Strings Legato`, `Harp`, `Timpani`/`Timpani Tremolo`, `Violins 1`/`Violin (Arco)`, `Tuba`, `Polka Accordion`, `Church Choir`, `Celesta`/`Principal + Mixture`, `English Horn`, `Tango Accordion`, `Flute Solo`).
- **결정·이유(사용자 판단 대신)**: 솔로 바이올린 `Violin (Arco)` 은 판정이 남아 있지만(브리프 §6) 지속음 3종만 있으므로 느린 지속 선율 두 곡(summer 2, winter 1)에만 쓰고 빠른 런에는 쓰지 않습니다. 청취 판정에서 기계적으로 들리면 FEEDBACK_LOG 에 적습니다.

## 작곡 후 정정 (2026-11-09, 리뷰 1차 반영 — 상세는 FEEDBACK_LOG 절 "계획 대비 달라진 점")

| key | 계획 | 정정 | 이유 |
|---|---|---|---|
| spring 1 | 98 BPM | **96 BPM** | 115→98 은 −14.8% 로 브리프 §2-3(±15%) 미달 |
| spring 2 | 72 BPM · 72마디 · 9마디 주제 | **84 BPM · 84마디 · 음가 ×2(18마디)** | 긴 음뿐이라 런 솎기가 무효(§2-2 연산 하나) → 음가 ×2 를 둘째 연산으로; 실효 템포 ×0.84 |
| summer 3 | 172 BPM | **174 BPM** | 150→172 는 +14.7% |
| autumn 2 | 11마디 주제 그대로 | **음가 ×½(6마디), 합창 6마디 루프 Dm–B♭–Gm–Asus–Dm–D** | 긴 음뿐이라 솎기 무효 → 음가 ×½ 를 둘째 연산으로; 실효 템포 ×1.51 |
| autumn 3 | 16분 그리드 · F7–B♭7–C7 | **8분 그리드 · F6–F6–B♭–C7** | 스윙 80틱이 16분 잔여 음과 겹쳐 주제 음이 30~47틱으로 잘림; 주제 A 음이 B♭7 과 충돌 |
| winter 3 | Fm–D♭–A♭–E♭ · 베이스 E1~A2 | **Fm(maj7)–C7 · 베이스 E1~C3** | 주제의 E♮(화성단음계) 충돌 18/114 → 6/114; 옥타브 펄스 접힘이 음역을 넘김 |
| winter 1 | 모티프 끝음 E♭ | **G** | C7 마디의 E♮ 와 반음 충돌 |
| summer 2 · autumn 1 · winter 1 | 8분 그리드 솎기 | **4분 그리드 솎기**(23→14 / 84→45 / 96→36 음) | 8분 그리드에서는 1~3마디만 바뀌어 §2-2 둘째 연산이 사실상 없었음(2차 리뷰) |
| winter 1 | Fm–Fm–D♭maj7–C7 | **9마디 진행 Fm×2–D♭maj7×2–Fm×2–B♭m7–C7–Fm** | 9마디 패스와 위상을 맞춰 충돌 24→4 |
| autumn 2 | 모티프 (0,3,2)(3,3,1)(6,3,0) | **(0,3,2)(3,2,1)(5,1,0)** | 3/4 두 마디 셀(6박) 밖의 셋째 음이 버려지고 있었음 |
