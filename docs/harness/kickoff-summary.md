## Kickoff Summary: Logic 템플릿 프로젝트로 패치·EXS 로드 자동화 (경로 B·C)

**Date**: 2026-11-13
**Type**: Feature
**Seed**: `docs/harness/seed.yaml` (task_id `20261113-220009-a606`, Plan Attack 1·2차 반영판 — `plan-attack-report.md`)

### JTBD
- User: 작곡 지시자(사용자 본인) — 앞으로 소스 악기를 다양하게 쓰고 악기·주법을 공부해 상세 지시로 곡을 만들려는 방향(`FEEDBACK_LOG.md` 2026-11-13 절)
- Problem: 파이프라인이 GM 프로그램 번호(경로 A)로만 악기를 불러, 레거시 오케스트라 패치 48개·Sampler 주법별 EXS 163개 등 인벤토리의 대부분이 지시에 닿지 않는다(`LOGIC_LIBRARY_INVENTORY.md:183-186`)
- Success: 첫 사이클은 "패치 로드 자동화"만 — 사용자가 Logic 에서 악기를 올려 저장한 템플릿 프로젝트의 **복사본**에 파이프라인이 SMF 를 기존 트랙으로 임포트해, 템플릿 패치 그대로 바운스가 나온다. 기존 트랙 배치가 Logic 에서 불가능하면 그 판정 기록이 산출물이다. 브리프 형식·주법 번역은 다음 사이클

### Context
- Repo type: 음악 제작 docs+tools 단일 저장소(`docs/music/tools/*.py`), 통합 세션 `issuereport` 에서 진행
- Tech stack: Python 3 표준 라이브러리, AppleScript/System Events AX 로 Logic Pro Creator Studio 조작
- Build/Test: 자동 테스트 없음. `docs/harness/verify-commands.json` 은 스케치 생성 스크립트 실행 목록. Logic 조작 도구는 `LogicLock` 으로 세션 간 직렬화
- Patterns: `pipeline.produce()` = `close_all_projects` → `open -a APP x.mid` → '무제 - 트랙' 창 대기 → `clear_alerts` → `finish()`(메트로놈 OFF → `mixer_strips()` → `save_project_as` → `bounce_and_post`). `gm_map.py` 가 같은 경로로 GM 128 을 실측
- Risks/constraints: 템플릿 임포트의 기존 트랙 배치는 미실측 `[INFERENCE]` → AC0 스파이크; `save_project_as` 는 무제 문서 전제(제목 있는 문서에서는 실패·덮어쓰기 위험) → 복사본 + `save_quiet`; `clear_alerts` 는 첫 버튼 자동 클릭 → 템플릿 모드에서 미사용; `finish()` 창 이름 '무제 - 트랙' 전제 → 인자화

### Scope
- MUST:
  1. AC0 스파이크: 에이전트가 AX·Logic MCP 로 테스트 템플릿 `PROJ_DIR/templates/tplsmoke.logicx` 를 만들고(안 되는 조작만 사용자에게 부탁, 과정은 방식 ① 실측 자료로 기록), 임포트 수단·배치 선택지와 대화상자 라벨·conductor 처리·`mixer_strips()`/`NumberOfTracks` 대조·리전 읽기·트랙 이름 변경·창 제목·바운스 저장 위치·템포 반영(9항목)을 실측해 기록. 판정표에 따라 종료 또는 지정 대책으로 진행
  2. `pipeline.produce(template=...)`: 프로젝트 창이 열려 있으면 시작 거부 → 템플릿·사본 경로와 `MetaData.plist` `NumberOfTracks` 선판정 → 실행 전 해시 → `copytree` 사본(이미 있으면 실패) → 사본 열기 → SMF 를 기존 트랙으로 임포트(AC0 라벨 지정 클릭, `_windows_strict` + 허용 창 목록, 밖의 창은 실패) → 스냅샷·스트립·리전 이름/시작·`lcd_tempo` 수집(반환 dict) → `finish(win_title=...)` → `save_quiet` → 기존 바운스 경로. 전체 `try/finally` 로 `close_all_projects(save=False)`, 실패 사본은 `.failed-<ts>` 로 보존
  3. 템플릿 모드 SMF 에 PC·CC0/7/10/32 없음(`build_smf(pcs=None)` 허용, 기존 출력 바이트 동일). 템포는 SMF 가 정함(`lcd_tempo` 확인). `metronome_off`·`clear_alerts` 는 템플릿 모드에서 미사용
  4. 템플릿 제작 체크리스트와 호출법을 `LOGIC_LIBRARY_INVENTORY.md` §4·§7 에 기록
- SHOULD: 테스트 템플릿에 경로 A·B·C 를 하나씩(예: Studio Violins 1 / `z_Legacy/Orchestral` Harpsichord / `Violin (Arco).exs` / 단일 출력 Drum Kit)
- MUST NOT: 템플릿 원본을 Logic 으로 열기, `save_project_as` 사용, `clear_alerts` 사용(템플릿 모드), 라이브러리 창 AX 조작·`.cst` 로드 구현, 템플릿 없는 기존 `produce()` 변경, Logic 환경설정 변경, `template_smoke.py` 에서 `LogicLock` 중복 획득
- OUT OF SCOPE: 브리프 형식 변경, 키스위치·CC 주법 번역, `Violin (Arco).exs` 음질 판정, 사계·lo-fi 재렌더, 템플릿 제작의 파이프라인 일반화, 방식 ①·② 구현

### Acceptance Criteria
0. AC0 스파이크 판정 기록(9개 실측 항목 + 판정표) — 불가면 AC1–4·6 N/A, AC5 는 불가 분기
1. AC1 패치·배치 일치 — 반환 dict 의 임포트 후 스트립이 템플릿 직후 스냅샷과 개수·순서·이름 정확히 일치(새 트랙 0), 트랙 i 리전 이름 = SMF 트랙 i 이름, 리전 시작 1 1 1 1, `lcd_tempo` = SMF BPM(≠ 템플릿 BPM)
2. AC2 바운스·발음 — 길이 SMF BPM 기준 9마디 −0.1s~+12s, 마디 1 RMS < −60 dBFS(클릭 없음), 트랙 i 구간(마디 2i+2~2i+3) RMS > −40 dBFS 각각, 사본 `MetaData.plist` `SamplerInstrumentsFiles` 에 경로 C .exs
3. AC3 템플릿 보존 — 시작 조건 확인 뒤 기록한 번들 전체 sha256 트리 해시가 실행 전후 동일
4. AC4 회귀 — `--gm` 별도 SMF(PC 포함)로 템플릿 없는 `produce()` 전 경로 + `gm_patch_map.json` 일치; 기존 스크립트 SMF 바이트 동일
5. AC5 문서 — 인벤토리 §4 B·C 행을 AC0 결과에 따라 갱신 + 템플릿 제작 체크리스트(플러그인 창 닫기·끝 마커·재생헤드 포함) + 호출법·`.failed` 처리
6. AC6 실패 경로 — `--dry-run`(Logic 없이 PC·CC 없음·트랙 수·BPM·구간 배치 assert, `verify-commands.json` 등록) + 경로 없음/사본 존재/트랙 초과/프로젝트 창 열림 4건이 Logic 조작 전에 실패

### Edge Cases
- 리전 이름·시작 AX 읽기 불가 → 배치 검증은 AC2 구간 RMS 로만(AC0 판정표)
- 스트립 이름이 트랙 이름일 수 있음 → 스냅샷 일치 + 구간 RMS + `SamplerInstrumentsFiles` 로 보완
- 샘플 누락·복구·플러그인 창 → 허용 창 목록 밖 = 실패; 체크리스트에 "플러그인 창 닫고 저장"
- 임포트 중 System Events ~2분 블록 → strict 창 조회(실패는 예외)
- 제목 있는 프로젝트의 바운스 기본 위치가 번들 안일 수 있음 → AC0 (8) 실측, 필요 시 `BOUNCE_SEARCH` 보강
- 실패 사본이 재실행을 막음 → `.failed-<ts>` 로 이름 변경, sid `tplsmoke-<ts>`

### Backpressure
- Method: 커밋 시점 자동 = `python3 docs/music/tools/template_smoke.py --dry-run`(verify-commands.json). Logic 필요 항목 = 수동 스모크 — `template_smoke.py --template <path>`(AC1–3), `--gm`(AC4), 실패 3건(AC6) 실행 결과를 FEEDBACK_LOG 에 기록
- Command: `python3 docs/music/tools/template_smoke.py --dry-run` / `--template "/Volumes/Netac 2TB/music/projects/templates/<name>.logicx"` / `--gm`

---
Kickoff complete. Ready for implementation.
Next: `/startdev` or manual planning.
