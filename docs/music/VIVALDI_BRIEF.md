# Vivaldi 사계 주제 변주 — 세션 브리프 (2026-10-21)

> 이 문서는 v1 라운드(2026-10-21) 브리프입니다. v2 라운드는 `VIVALDI_BRIEF_V2.md` 만 따릅니다.

목적: 사계 **12악장 각각의 메인 주제부**를 변주해, Suno Cover 업로드가 **통과**(저작권 유사도 차단 회피)되면서 사용자가 좋아하는 결(lo-fi hip hop / deep house / chill) 안에 있는 곡을 만든다. 세 세션이 같은 데이터에서 출발해 **모델별로 12곡씩** 만들고, 과정과 결과를 각자 문서화한다.

| 세션(워크스페이스) | 브랜치 | 모델 | 산출물 접미사 |
|---|---|---|---|
| `losik/band-astra` | `rae-hugo-kim/band-astra` | gpt-6-astra | `-astra` |
| `losik/band-fable` | `rae-hugo-kim/band-fable` | claude-fable-5-1 | `-fable` |
| `losik/band-opus` | `rae-hugo-kim/band-opus` | claude-opus-5-5 | `-opus` |

세션은 시작하자마자 **자기 모델 ID를 `docs/sum` 요약과 FEEDBACK_LOG 절 제목에 적는다**(9월 band 라운드는 모델 무기록이라 비교가 불가능했음).

## 0. 세션 시작 절차 (각 세션, MUST)

1. `git status` 를 본다. **band-fable 은 미커밋 작업(캐논 기록 포함, 78파일)이 있으니 먼저 자기 브랜치에 커밋한다.** 그다음 세 세션 모두 `git merge issuereport` — 이 브리프, `docs/music/tools/vivaldi_data.py`, 최신 `pipeline.py`(저장 시트·믹서 창·바운스 폴더 탐색·**세션 간 Logic 잠금**), `bounce_dh.py`(화면보호기 가드는 여기), `.omp/agents/composer-*.md` 를 받는다. 충돌 규칙: `FEEDBACK_LOG.md`/`SUNO_PROMPTS.md`/`docs/sum/*` 는 **양쪽 다 보존**(append-only), `pipeline.py`/`bounce_dh.py`/`PROMPT_GUIDELINES.md` 는 **issuereport 쪽**, 그 외 코드는 자기 브랜치 쪽.
2. `python3 -c "import sys; sys.path.insert(0,'docs/music/tools'); import vivaldi_data as v; print(len(v.MOVEMENTS))"` → 12.
3. `docs/music/PROMPT_GUIDELINES.md` §2·§4·§6, 이 브리프, 그리고 **캐논 기록**을 읽는다 — band-fable 워크트리의 `docs/music/FEEDBACK_LOG.md` "canon-lofi" 절(`/Users/hugom4/orca/workspaces/losik/band-fable/docs/music/FEEDBACK_LOG.md`; band-fable 이 커밋하기 전에는 디스크 경로로만 읽힌다), 작곡기 `band-fable/docs/music/tools/canon_lofi_v3.py`.

## 1. 데이터

`docs/music/tools/vivaldi_data.py` — `MOVEMENTS[(season, n)]` 에 12악장 5성부(solo, violin1, violin2, viola, cello) 전곡 노트(PPQ 480, (틱, 길이, 피치)), `key_name`(음악적 조성 — MIDI `ks` 의 minor 플래그는 LilyPond 가 0 으로 쓰기도 하므로 `key_name` 이 기준), 첫 박자 `ts` 와 박자 변화 `ts_events`(Summer I 은 3/8→4/4→3/8), `pickup`(Spring I 은 8분음 피크업 240틱 — 마디 번호는 첫 다운비트 기준), 실제 마디 수, **기본 주제 창** `theme`. 헬퍼 `bar_tick(key, bar)` 가 피크업·박자 변화를 반영한 마디 다운비트 틱을, `theme_notes(key, part, pad_bars)` 가 창 안의 노트를 첫 다운비트 = 0틱으로 돌려준다(피크업은 **음수 틱** — SMF 에 넣기 전에 반드시 옮기거나 잘라낸다; `hum_t` 는 0 으로 클램프하고 음수 틱은 인코더에서 깨진다). 노트 없는 성부는 빈 리스트(Spring II cello). 출처 Mutopia Project(미러 표기 MutopiaBSD, 현행 목록 CC BY-SA 3.0). 작품 자체는 퍼블릭 도메인. 이 프로젝트는 보수적으로 **CC BY-SA 3.0** 을 전제한다: 데이터 파일과 그 파생물(변주 MIDI 포함)에 출처(Mutopia Project)를 표기하고, 공개 시 같은 조건으로 공개한다. 개인 청취·비공개 Suno 입력은 영향이 없다.

| key | 박자 | 조 | 원본 BPM | 기본 주제 창 | 비고 |
|---|---|---|---|---|---|
| spring 1 | 4/4 | E | 115 | 1–13 | 리토르넬로. 가장 유명 |
| spring 2 | 3/4 | C♯m | 50 | 2–10 | solo 선율 + vn 반주(개 짖는 viola) |
| spring 3 | 12/8 | E | 144 | 1–12 | 시칠리아나 춤 |
| summer 1 | 3/8 → 4/4 → 3/8 | Gm | 75 | 1–30 | 나른한 튜티(3/8 마디가 짧음). 31–51마디가 4/4, 52부터 3/8 복귀 — `bar_tick()` 이 박자 변화를 계산한다 |
| summer 2 | 4/4 | Gm | 45 | 1–8 | solo 선율, 천둥 끊김 |
| summer 3 | 3/4 | Gm | 150 | 1–20 | 폭풍 프레스토 |
| autumn 1 | 4/4 | F | 120 | 1–12 | 춤 리토르넬로 |
| autumn 2 | 3/4 | Dm | 53 | 4–14 | 거의 화음뿐 — 주제는 violin1 에 있음 |
| autumn 3 | 3/8 | F | 80 | 1–24 | 사냥 |
| winter 1 | 4/4 | Fm | 140 | 1–12 | 떨림 화음 → solo 4마디 진입 |
| winter 2 | 4/4 | E♭ | 46 | 1–8 | Largo, 피치카토 위 선율 |
| winter 3 | 3/8 | Fm | 75 | 1–24 | cello F 페달 위 solo 로 시작, 튜티는 21–22마디부터 |

주제 창은 기본값이다. 들어보고 "이 악장의 얼굴"이 아니면 창을 옮기고 그 이유를 기록한다.

## 2. Suno 통과 규칙 (캐논 라운드 실측, MUST)

캐논 v1 은 "matches an existing recording" 으로 **차단**, v2·v3a/b/c 는 통과. 차단 결정 요인은 화성이 아니라 **선율 원리듬 전곡 유지 + 모방 성부**였다. 그래서:

1. **원곡 성부를 그대로 겹쳐 쓰지 않는다.** 주제는 한 성부(보통 solo 또는 violin1)만 가져온다. 바흐식 모방·카논·원곡 vn2/viola 더블링 금지.
2. **리듬을 바꾼다.** 주제 음고 윤곽은 살리되, 리듬은 ① 부분 당김(싱코페이션) ② 음가 2배/반 ③ 런(16분 스케일)은 솎아서 골격음만 ④ 스윙 — 중 둘 이상. 원리듬 그대로인 구간은 **연속 4마디 이하**(캐논 v3: 3~10 마디만 원리듬, 통과).
3. **박자·템포를 옮긴다.** 3/8·12/8 악장은 4/4(셔플) 또는 6/8 로, 원본 BPM 그대로 쓰지 않는다(±15% 이상 또는 하프/더블타임).
4. **화성은 자유.** 원곡 베이스 라인을 그대로 깔지 말고, 장르 관용 보이싱(7th·9th, 도리안 색)으로 재구성. 조옮김도 허용(Camelot 인접 키나 lo-fi 에 편한 키).
5. **주제는 전체의 일부.** 곡의 40~60% 만 주제 변주, 나머지는 장르 골격(인트로·브레이크·아웃트로)과 자기 모티프. 캐논 v2 처럼 "원곡인 듯 아닌 듯"이 목표가 **아니라**, 듣는 사람이 "아, 사계"를 알아채되 Suno 필터는 지나가는 지점.
6. 업로드가 차단되면 ② 리듬 변형 비율을 높이고 ⑤ 주제 비율을 낮춘 v2 를 만든다. 차단/통과 결과를 반드시 기록한다.

## 3. 음악 레시피

장르는 악장마다 고른다 — 빠른 악장은 deep house(`DEEP_HOUSE_SET_BRIEF.md` v2·v3 레시피: 코드 72~92, 패드 55~72, Tough Kit 드럼 분리, 오픈햇 뒷박), 느린 악장은 lo-fi hip hop(`LOFI_HIPHOP_SET_BRIEF.md` 레시피: SoCal 붐뱁, 스윙 24~32, 고스트, EP/나일론, 리드 모티프). 둘 다 사용자 청취 통과본이다. 세 모델이 같은 악장에 다른 장르를 골라도 된다 — 그것이 비교의 재미.

- 길이 **~3분**(Suno 3분 입력 실측 통과): 56/64/96마디 중 BPM 에 맞춰.
- 트랙: 드럼·베이스·키·(패드)·주제 성부(EP/나일론/그랜드/리드 신스 — 검증 PC: 4/0/24/27/80/81)·선택 Tex. 검증된 GM PC 만(§4). 클랩 단독 금지, CC64 리페달.
- 구조 기본: intro 8 / 주제 제시(변주 리듬) / 브레이크 / 주제 재제시(다른 옥타브·악기) / outro 8. 마커 필수.
- 드럼·화성층은 10월 deep house·lo-fi 레시피의 벨로시티 밴드를 지킨다(비어 있거나 뭉개지지 않게).

## 4. 산출물 (세션당, 12곡)

- 작곡기 `docs/music/tools/vivaldi_<model>.py`: `SKETCHES` 12개(dict: key=(season,n), sid, title, genre, bpm, bars, theme_part, theme_window, rhythm_ops=[...], notes), `compose(sid)`, `__main__` 이 `{sid}-v1.mid` 12개를 쓰고 곡마다 점검 줄(원리듬 연속 마디 수 ≤4, 주제 비율 %, 드럼/키 벨로시티 밴드, 마지막 노트 위치).
- **sid 는 `vs-<season><n>-<model>`** (예 `vs-spring1-astra`), **title 은 `<Season> <I/II/III> <Model>`** (예 `Spring I Astra`). 바운스 폴더·Logic 프로젝트 폴더가 세 세션 공용(`/Volumes/Netac 2TB/music/`)이라 접미사 없이는 서로 덮어쓴다.
- 바운스: `pipeline.produce(sid, title, 'v1', mid)` 를 직접 순차 호출한다(`bounce_dh.py` 의 `jobs_for` 는 `<set>_astra/fable/opus` 모듈 규약이라 여기엔 안 맞음; `bounce_dh.NoScreensaver` 와 `pipeline.restart_logic`(잠금 안에서 종료) 은 import 해서 쓴다). **Logic 은 한 대뿐** — `produce()` 가 `/Volumes/Netac 2TB/music/.logic-lock` 을 잡고 돌며 다른 세션이 쥐고 있으면 최대 1시간 기다린다. 해제는 자기 토큰이 적힌 파일만 지우므로 남의 잠금을 지우는 일은 없고, 해제 뒤 3초를 쉬어 기다리던 세션이 끼어들 수 있다(곡 단위로 번갈아 바운스됨). 바운스 루프는 `TimeoutError` 를 잡아 그 곡을 "대기 초과"로 기록하고 다음 곡으로 넘어가거나 나중에 재시도한다. 잠금 파일이 남아 있는데 아무도 안 쓰면(세션이 죽은 경우) 내용(워크트리·pid·시각)을 확인하고 사람이 지운다. 세션 셋이 각자 바운스를 걸어 두면 자동으로 순차 처리된다.
- Suno: `docs/music/suno/vivaldi_<model>.md` 12블록 `## {sid}-v1` — Style ≤ 300자, **Description ≤ 1,000자(공백 포함)**, `len()` 측정 출력. Description 에 "variation on the theme of Vivaldi's Four Seasons, <Season> <mvt>" 를 넣되 원곡 제목을 Style 에는 넣지 않는다(캐논 라운드: Cover Style 이 실제 레버).
- 기록: `docs/music/FEEDBACK_LOG.md` 끝에 `## 2026-10-21 Vivaldi 사계 변주 — <model> (<모델 ID>)` 절: 악장별 표 `| key | sid | 장르 | BPM | 마디 | 주제 창 | 리듬 변형 | 주제 비율 | 업로드 결과 |` + 설계 판단 단락. `docs/sum/session_2026-10-21_vivaldi-<model>.md` 에 과정·결정·실패·결과를 요약(모델 ID 명시). 커밋은 자기 브랜치에.

## 5. 끝났을 때

세 세션이 각자 커밋하면 메인(chats/issuereport)이 세 브랜치의 FEEDBACK_LOG 절·Suno 블록·`docs/sum` 을 모아 `SETLIST_vivaldi.md`(악장 × 모델 36곡 표, 업로드 결과, 청취 판정 칸)를 만든다.
