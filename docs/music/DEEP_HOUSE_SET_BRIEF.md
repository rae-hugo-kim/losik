# Deep House Set — 작곡 브리프 (2026-10-12)

목적: 30곡을 이어 붙여 **1시간 이상의 deep house 셋리스트** 한 편을 만든다. 각 곡은 셋의 한 슬롯을 맡는다.
세 모델(gpt-6-astra → claude-fable → claude-opus)이 순차로 10곡씩 작곡하고, 뒤 모델은 앞 모델 결과를 읽고 겹침을 피한다.

## 청취 피드백 (이 라운드의 출발점)

이전 deep house 4곡(velvet-hour, low-tide-shuffle, indigo-*, harbor-fog-*)과 house 전반에 대한 판정: **"너무 신나고 밝고 떠 있다."** 방향은 **chill한, 더 깊은 deep house**.
house 판정에서 확인된 사실: 밝기는 베이스 윤곽보다 코드를 따라간다 / 베이스 5도 상행은 "뛰는" 느낌을 만든다 / 뒷박 베이스·2코드 반복·오르간 여백은 deep 쪽 성분이다.

## "더 깊게"의 구체 레시피 (MUST)

| 요소 | 하라 | 하지 마라 |
|---|---|---|
| 킥 | 벨로시티 **78~96**, 4온더플로어, 휴머나이즈 ±6~8 | 110 이상, 딱딱한 어택 |
| 햇 | 클로즈드 햇 벨로시티 40~64, 밀도는 8분 또는 성긴 16분, 오픈햇은 **2~4마디에 1개** | 매 뒷박 오픈햇, 16분 꽉 채움 |
| 스네어/클랩 | 림 또는 약한 스네어(70~85), 클랩은 그 밑에만 | 클랩 단독, 강한 백비트 |
| 베이스 | **서브 영역(E1~A2)**, 긴 음 또는 뒷박 짧은 음, 움직임은 근음·5도 아래·옥타브 내로 | 옥타브 상행 러닝, 5도 상행 리프, 16분 펌프 |
| 코드 | **2코드 루프 또는 정지 화성**, m9/m11/도리안 색, 낮은 벨로시티(50~70) 홀드 또는 **덥 코드**(짧은 스탭 뒤 긴 여백), 음역 C3~C5 | 4코드 밝은 순환, 매 뒷박 스탭, 장조 중심 |
| 패드 | 쓰면 1도+5도, 벨로시티 35~50, **낮게 깔림** | 전면에 나오는 패드, 풀코드 스택 |
| 주파수 무게 | 서브+중역에 무게. 고역 요소는 햇뿐 | 밝은 고역 스탭, 글리터 |

조성: 슬롯 표의 키를 따른다(단조 또는 도리안). 같은 근음의 병행 장조로 바꾸지 않는다.

## 길이와 구조 (DJ 믹스 전제)

- **64마디** 기본(최소 56, 최대 80). 120 BPM에서 64마디 ≈ 2:08.
- 구조: 1–16 인트로(드럼→베이스 순으로 쌓임, 코드는 12마디부터 살짝) → 17–32 A(풀) → 33–40 브레이크(킥 빼거나 햇 빼기) → 41–56 A'(풀, 41마디 1박 크래시 하나) → 57–64 아웃트로(코드 먼저 빠지고 드럼+베이스만).
- 인트로·아웃트로가 드럼 위주인 이유: 앞뒤 곡과 믹스하기 위해서다. 인트로 첫 8마디는 킥+햇만도 허용.
- 마커: [(1,'intro'),(17,'A'),(33,'break'),(41,'A2'),(57,'outro')].

## 슬롯 표 (30)

Camelot 인접으로 키가 이어진다. BPM은 ±1 허용. 에너지는 1(가장 성김)~3(deep 안에서의 피크).

| 슬롯 | 모델 | BPM | 키 | 에너지 | 역할 |
|---|---|---|---|---|---|
| 1 | astra | 117 | A minor | 1 | 오프너. 드럼+서브 거의 전부, 코드는 암시만 |
| 2 | fable | 117 | A minor | 1 | |
| 3 | opus | 118 | E minor | 1 | |
| 4 | astra | 118 | E minor | 1–2 | |
| 5 | fable | 119 | B minor | 2 | |
| 6 | opus | 119 | B minor | 2 | |
| 7 | astra | 120 | F♯ minor | 2 | |
| 8 | fable | 120 | F♯ minor | 2 | |
| 9 | opus | 120 | C♯ minor | 2 | |
| 10 | astra | 121 | C♯ minor | 2 | |
| 11 | fable | 121 | G♯ minor | 2 | |
| 12 | opus | 121 | G♯ minor | 2–3 | |
| 13 | astra | 122 | E♭ minor | 3 | deep 피크 구간 시작 |
| 14 | fable | 122 | E♭ minor | 3 | |
| 15 | opus | 122 | B♭ minor | 3 | |
| 16 | astra | 123 | B♭ minor | 3 | |
| 17 | fable | 123 | F minor | 3 | |
| 18 | opus | 123 | F minor | 3 | |
| 19 | astra | 122 | C minor | 3 | |
| 20 | fable | 122 | C minor | 2–3 | 피크 끝 |
| 21 | opus | 121 | G minor | 2 | 드리프트. 화성·패드 비중 ↑ |
| 22 | astra | 121 | G minor | 2 | |
| 23 | fable | 120 | D minor | 2 | |
| 24 | opus | 120 | D minor | 2 | |
| 25 | astra | 119 | A minor | 2 | |
| 26 | fable | 119 | A minor | 1–2 | |
| 27 | opus | 118 | D minor | 1 | 쿨다운 |
| 28 | astra | 118 | D minor | 1 | |
| 29 | fable | 117 | A minor | 1 | |
| 30 | opus | 116 | A minor | 1 | 클로저. 아웃트로를 16마디로 늘려 드럼이 서서히 빠지게 |

## 겹침 금지 목록

`docs/music/SUNO_PROMPTS.md`의 deep house 블록(velvet-hour, low-tide-shuffle, indigo-held-room/soft-steps, harbor-fog-minor/major)에 쓰인 진행·베이스 셀·코드 리듬을 그대로 쓰지 않는다. 특히:
- Fm9–B♭m9–D♭maj9–C7♭9 (velvet), Gm9–C9–Fmaj9–E♭maj9 (low-tide), Bm9–Gmaj9–Em9–F♯m7 (indigo), Dm9–Gm9–B♭maj9–A7♭9 (harbor-fog)
- "EP 홀드 vs 두 번 스탭" 쌍 설계, 병행조 쌍 설계 — 이번엔 쌍이 아니라 **셋의 흐름**이 단위다.
- 뒤 모델은 앞 모델이 `docs/music/FEEDBACK_LOG.md`에 적은 표를 읽고 코드 루프·베이스 셀이 같은 곡을 만들지 않는다.

## 산출물 (모델당)

1. `docs/music/tools/dh_<model>.py` — `SKETCHES` 리스트(dict: slot, sid, title, bpm, key, energy, notes), `compose(sid) -> (nt, cc, pcs, n_bars, bpm, title, keysig_sf, minor)`, `__main__`이 전 곡을 `pipeline.SK_DIR`에 `{sid}-v1.mid`로 쓰고 `write_smf` 자체 점검 줄을 출력.
2. sid 형식: `dh{슬롯 두 자리}-<영문-kebab>` (예 `dh01-first-light`). 제목은 Title Case.
3. `docs/music/FEEDBACK_LOG.md` 끝에 `## 2026-10-12 deep house set — <model>` 섹션: 표 `| 슬롯 | sid | BPM | 키 | 마디 | 코드 루프 | 베이스 셀 | 특징 한 줄 |` + 셋 안에서 이 10곡이 맡은 흐름 한 단락. 해요체/합니다체.
4. `docs/music/SUNO_PROMPTS.md` 끝에 곡마다 `## {sid}-v1` 블록(**Style** 한 줄 + **Description** fenced). 기존 블록 형식·영어 서술체 유지. "no lead, no vocals, DJ-friendly intro/outro" 명시.

## 기술 계약

- 작업 디렉터리 `docs/music/tools/`, Python 3.9 stdlib. `pipeline.build_smf/write_smf`, `bt/hum_t/hum_v/seed/SW`, `sketches.mk_chord2/PC`. `docs/music/PROMPT_GUIDELINES.md` §2·§4 준수(검증된 GM PC만: 드럼 PC25 또는 PC0, 베이스 PC38/33, 키 PC4/0/16, 패드 PC89/88).
- 트랙: [('Drums',9),('Bass',0),('Keys',1)] + 선택 ('Pad',2). 리드·멜로디 없음.
- 노트는 마지막 마디 안에서 끝난다. 홀드하는 키에는 CC64 마디 리페달.
- Logic·produce()·git·테스트·포매터 실행 금지. 다른 파일 수정 금지.
