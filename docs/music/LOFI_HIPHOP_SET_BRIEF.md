# Lo-fi Hip Hop Set — 작곡 브리프 (2026-10-21)

목적: 30곡을 이어 붙여 **1시간 반 안팎의 lo-fi hip hop 플레이리스트** 한 편을 만든다. 모델 셋(gpt-6-astra → claude-fable-5-1 → claude-opus-5-5)이 순차로 10곡씩, 뒤 모델은 앞 모델의 FEEDBACK_LOG 표를 읽고 코드 루프·드럼 셀·브레이크 종류가 겹치지 않게 쓴다.

deep house 셋(`DEEP_HOUSE_SET_BRIEF.md`)에서 세 라운드에 걸쳐 확인된 것을 처음부터 적용한다: **화성층은 들려야 한다**(코드 72~92, 패드 55~72), **드럼 요소는 자기 자리가 있어야 한다**(한 칸에 두 요소 금지, 벨로시티 강약), **곡 길이 ~3분**(Suno 가 3분 입력을 그대로 따름), **Suno 프롬프트 ≤ 1,000자**.

## lo-fi hip hop 레시피 (MUST)

| 요소 | 하라 | 하지 마라 |
|---|---|---|
| 킷 | **PC0 SoCal**(어쿠스틱) | Drum Synth Kit, Tough Kit |
| 킥 | 붐뱁: 1박 고정 + 마디당 1~2개 싱코페이션(& of 2, a of 2, & of 3, a of 3 중 택) · 96~110 · 1박 +6 | 4온더플로어, 매 마디 같은 자리 |
| 스네어 | 2·4박 **86~100**(슬롯 에너지 1은 짝수 마디 림 37 으로 대체 가능) + **고스트 스네어** 1~2개/마디 **38~52** | 클랩 단독(쓰면 스네어 밑 레이어 70~80) |
| 햇 | 8분 **스윙 24~32틱**, 정박 48~60 / 뒷박 68~84. 16분은 2박·4박 뒤 한 칸(e 자리)만 40~50. 오픈햇은 4마디에 1개 이하 | 직선 8분, 16분 연속 |
| 라이드 | 선택. A2 에서만 4분 55~70 | |
| 휴머나이즈 | 타이밍 **±10~14**(lazy), 벨로시티 ±10 (악센트 패턴은 유지) | ±6 이하 |
| 베이스 | **PC33 핑거**(에너지 1~2) 또는 PC38(에너지 3). 킥 자리를 따라가되 1~2음 빼서 숨 쉬게, 근음·5도·옥타브·경과음, E1~C3, 60~82 | 16분 러닝, 슬랩 |
| 코드(Keys) | **PC4 EP** 또는 **PC0 그랜드**. maj7·m7·m9·9·13·sus 재즈 보이싱 4성, **C3~C5**, **72~92**, 컴핑은 마디당 1~3회 또는 홀드. CC64 마디 리페달. 2~4코드 루프(ii–V–I 변형, I–vi–IV–V 재즈화, 도리안 i–IV, 서클 등 허용) | 파워코드, 루트 포지션 3화음 |
| 텍스처(Tex) | **PC24/27 나일론 기타** 아르페지오·코드톤 피킹, 또는 PC16 오르간 소프트 홀드, 또는 두 번째 EP(옥타브 위) 55~72, A/A2 | |
| 리드 | **필수**(lo-fi 의 정체성): 2~4마디 모티프 하나를 반복·변형. PC4 EP(옥타브 위) / PC24 나일론 / PC0 그랜드 상성부. 마디당 ≤6음, 60~82, **A2 전체 + A 의 뒤 8마디**. 코드톤·9도·펜타토닉 안에서 | 16분 러닝, 넓은 도약 |
| 패드 | 선택. PC89/88 1+5(+9), 45~60, 낮게 | 전면 |
| 분위기 | 따뜻·느긋·약간 흐릿. 음역은 중역 중심 | 밝은 고역, 공격적 어택 |

트랙(고정): `[('Drums',9),('Bass',0),('Keys',1),('Tex',2),('Lead',3)]` + 선택 `('Pad',4)`. 검증된 GM PC 만(`PROMPT_GUIDELINES.md` §4).

## 길이와 구조

Suno 3분 입력 실측 통과 → **~3분**. BPM 별 마디 수:

| BPM | 마디 | 구조(마커) | 길이 |
|---|---|---|---|
| ≤ 78 | **56** | 1–8 intro / 9–24 A / 25–32 break / 33–48 A2 / 49–56 outro · `[(1,'intro'),(9,'A'),(25,'break'),(33,'A2'),(49,'outro')]` | 2:52–3:07 |
| ≥ 80 | **64** | 1–8 intro / 9–28 A / 29–36 break / 37–56 A2 / 57–64 outro · `[(1,'intro'),(9,'A'),(29,'break'),(37,'A2'),(57,'outro')]` | 2:54–3:12 |

- 인트로: 키 또는 텍스처 먼저(1마디), 햇 3마디, 킥·스네어 5마디, 베이스 9마디. 아웃트로: 리드·Tex 먼저 빠지고 마지막 4마디는 드럼+키 또는 키만.
- 브레이크(8마디): lo-fi 식 — 드럼 전부 또는 킥 빼고 키·Tex·리드가 남거나, 반대로 드럼+베이스만. 슬롯마다 다르게. A2 첫 마디 크래시 1개(55~70, 조용히).
- 리드는 A 의 마지막 8마디부터 들어와 A2 내내.

## 슬롯 표 (30)

Camelot 인접. 장조·단조 섞음(lo-fi 는 maj7 의 따뜻함이 핵심). 에너지 1(가장 성김)~3(가장 참).

| 슬롯 | 모델 | BPM | 마디 | 키 | 에너지 | 역할 |
|---|---|---|---|---|---|---|
| 1 | astra | 76 | 56 | D minor | 1 | 오프너. 키+햇으로 시작 |
| 2 | fable | 76 | 56 | D minor | 1 | |
| 3 | opus | 78 | 56 | F major | 1–2 | |
| 4 | astra | 78 | 56 | C major | 2 | |
| 5 | fable | 80 | 64 | A minor | 2 | |
| 6 | opus | 80 | 64 | A minor | 2 | |
| 7 | astra | 82 | 64 | E minor | 2 | |
| 8 | fable | 82 | 64 | G major | 2 | |
| 9 | opus | 84 | 64 | D major | 2–3 | |
| 10 | astra | 84 | 64 | B minor | 3 | 피크 시작 |
| 11 | fable | 86 | 64 | B minor | 3 | |
| 12 | opus | 86 | 64 | F♯ minor | 3 | |
| 13 | astra | 88 | 64 | A major | 3 | |
| 14 | fable | 88 | 64 | E major | 3 | |
| 15 | opus | 88 | 64 | C♯ minor | 3 | 피크 |
| 16 | astra | 86 | 64 | C♯ minor | 3 | |
| 17 | fable | 86 | 64 | G♯ minor | 2–3 | |
| 18 | opus | 84 | 64 | B major | 2 | 드리프트 시작 |
| 19 | astra | 84 | 64 | F♯ major | 2 | |
| 20 | fable | 82 | 64 | E♭ minor | 2 | |
| 21 | opus | 82 | 64 | E♭ minor | 2 | |
| 22 | astra | 80 | 64 | B♭ minor | 2 | |
| 23 | fable | 80 | 64 | D♭ major | 2 | |
| 24 | opus | 78 | 56 | A♭ major | 1–2 | |
| 25 | astra | 78 | 56 | F minor | 1–2 | |
| 26 | fable | 76 | 56 | F minor | 1 | 쿨다운 |
| 27 | opus | 76 | 56 | C minor | 1 | |
| 28 | astra | 74 | 56 | E♭ major | 1 | |
| 29 | fable | 74 | 56 | B♭ major | 1 | |
| 30 | opus | 72 | 56 | G minor | 1 | 클로저. 아웃트로 8마디에서 드럼 → 베이스 → 키만 → 마지막 마디 키 한 화음 |

## 겹침 금지

기존 lo-fi hip hop 스케치(`SUNO_PROMPTS.md`)의 루프·셀: rainy-window-beat (Gm9–C9–Fmaj9–Dm9), slow-room-piano (A♭maj7–Gm7–Fm9–B♭13, 하프타임), porch-pocket (E♭maj9–Cm9–A♭maj9–B♭9), late-bus (Cm9–A♭maj9–Fm9–G7♭9 / Cmaj9–Am9–Fmaj9–G9). 뒤 모델은 앞 모델의 FEEDBACK_LOG 표를 읽는다. 같은 키의 인접 슬롯(1·2, 5·6, 10·11, 15·16, 20·21, 25·26)은 **코드 루프·컴핑 리듬·리드 모티프 셋 다** 달라야 한다.

## 산출물 (모델당)

1. `docs/music/tools/lh_<model>.py` — `SKETCHES` 10개(dict: slot, sid, title, bpm, bars, key, energy, notes), `compose(sid) -> (nt, cc, pcs, n_bars, bpm, title, keysig_sf, minor)`, `__main__` 이 10곡을 `pipeline.SK_DIR/{sid}-v1.mid` 로 쓰고 곡마다 점검 줄 출력: 킥/스네어/고스트/햇 정·뒷박/오픈햇 수 벨로시티 범위, 스윙 틱, 베이스 음역·벨로시티, 키 음역·벨로시티·CC64 유무, 리드 마디 범위·마디당 최대 음수, 동일 음 겹침 0, 마커, 마지막 노트가 마지막 마디 안. sid 형식 `lh{슬롯 두 자리}-<영문-kebab>`.
2. `docs/music/FEEDBACK_LOG.md` 끝에 `## 2026-10-21 lofi hip hop set — <model>` 섹션: 표 `| 슬롯 | sid | BPM | 마디 | 키 | 코드 루프 | 드럼 셀(킥 자리) | 리드 모티프 한 줄 | 브레이크 |` + 흐름 한 단락. 해요체/합니다체.
3. `docs/music/suno/lh_<model>.md` — 곡마다 `## {sid}-v1` / `**Style**` 한 줄(≤300자, `instrumental` 로 끝) / `**Description**` fenced(**≤1,000자 공백 포함**, 키·BPM·코드 루프·드럼 골격·리드 모티프·구조 한 줄·"no vocals, lo-fi warmth, DJ-friendly intro/outro"). 작성 후 `len()` 측정 출력 필수.

## 기술 계약

작업 디렉터리 `docs/music/tools/`, Python 3.9 stdlib. `pipeline.build_smf/write_smf`, `bt/hum_t/hum_v/seed/SW`, `sketches.mk_chord2/PC`. 검증된 GM PC 만. Logic·produce()·git·테스트·포매터 실행 금지. 다른 파일 수정 금지.
