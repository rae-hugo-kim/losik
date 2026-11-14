# Current Scope: Logic 템플릿 프로젝트로 패치·EXS 로드 자동화 (경로 B·C)

**Created**: 2026-11-13
**Seed**: `docs/harness/seed.yaml` (`20261113-220009-a606`, Plan Attack 1·2차 반영판)

## MUST
- AC0 스파이크: 에이전트가 AX·Logic MCP 로 테스트 템플릿 `PROJ_DIR/templates/tplsmoke.logicx` 를 만들고(안 되는 조작만 사용자에게 부탁) 9개 항목 실측, 판정표에 따라 종료 또는 지정 대책으로 진행
- `pipeline.produce(template=...)`: 프로젝트 창 열려 있으면 시작 거부 → 경로·`NumberOfTracks` 선판정 → 실행 전 해시 → `copytree` 사본(존재 시 실패) → 사본 열기 → 기존 트랙 임포트(라벨 지정, strict 창 조회, 허용 밖 창은 실패) → 스냅샷·스트립·리전·`lcd_tempo` 수집(반환 dict) → `finish(win_title)` → `save_quiet` → 바운스; `try/finally close_all_projects(save=False)`, 실패 사본 `.failed-<ts>`
- 템플릿 모드 SMF 에 PC·CC0/7/10/32 없음; 템포는 SMF; `metronome_off`·`clear_alerts` 미사용
- 템플릿 제작 체크리스트·호출법을 `LOGIC_LIBRARY_INVENTORY.md` §4·§7 에 기록(AC0 결과에 따라 가능/불가 분기)

## SHOULD
- 테스트 템플릿에 경로 A·B·C 를 하나씩 포함

## MUST NOT
- 템플릿 원본을 Logic 으로 열기, `save_project_as`·`clear_alerts`·`metronome_off` 사용(템플릿 모드)
- 라이브러리 창 AX 조작·`.cst` 로드 구현
- 템플릿 없는 기존 `produce()` 동작 변경, `build_smf` 출력 바이트 변경
- Logic 환경설정 변경, `template_smoke.py` 의 `LogicLock` 중복 획득·Logic 직접 조회

## OUT OF SCOPE
- 브리프 형식 변경, 키스위치·CC 주법 번역
- `Violin (Arco).exs` 음질 판정, 사계·lo-fi 재렌더
- 템플릿 제작의 파이프라인 일반화, 방식 ①·② 구현

## Acceptance Criteria
- [x] AC0 스파이크 판정: 9개 실측 항목과 판정 결과가 FEEDBACK_LOG 에 기록, 불가면 AC1–4·6 N/A·AC5 불가 분기
- [x] AC1 패치·배치 일치: 반환 dict 의 스트립이 스냅샷과 개수·순서·이름 정확히 일치, 트랙 i 리전 = SMF 트랙 i·시작 1 1 1 1, `lcd_tempo` = SMF BPM
- [x] AC2 바운스·발음: 길이 9마디 −0.1s~+12s, 마디 1 RMS < −60, 트랙별 구간 RMS > −40, `SamplerInstrumentsFiles` 에 .exs
- [x] AC3 템플릿 보존: 번들 sha256 트리 해시 전후 동일
- [x] AC4 회귀: `--gm` 별도 SMF 로 GM 경로 전체 + `gm_patch_map.json` 일치; 기존 스크립트 SMF 바이트 동일
- [x] AC5 문서: 인벤토리 §4 B·C 행 갱신(가능/불가 분기) + 템플릿 체크리스트 + 호출법·`.failed` 처리
- [x] AC6 실패 경로: `--dry-run` 등록 + 경로 없음/사본 존재/트랙 초과/프로젝트 창 열림 4건이 Logic 조작 전에 실패
