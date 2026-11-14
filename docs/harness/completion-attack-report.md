# Completion Attack Report — `20261113-220009-a606` (GATE 3.5)

2026-11-14 01:0x, 병렬 3인 패널 + verifier. 리뷰 도중 `pipeline.py`·`template_smoke.py`·`test_template_mode.py` 가 고쳐졌고(아래 "반영"), 최종 스모크는 수정 뒤 코드로 다시 돌렸어요.

|역할|모델|집계|판정|
|---|---|---|---|
|architect|`adversary-sol` (GPT)|HIGH 5 · MEDIUM 2 · LOW 1|BLOCK|
|security-reviewer|(Claude)|HIGH 1 · MEDIUM 6 · LOW 4|PASS(조건부)|
|test-engineer|`adversary-opus` (Claude)|HIGH 2 · MEDIUM 7 · LOW 9|BLOCK|
|verifier|verifier|—|INCOMPLETE|

CRITICAL 은 0건이라 규칙상 BLOCK 은 아니지만, HIGH 를 전부 반영한 뒤 재검증했어요.

## 반영 (코드)

|발견|반영|
|---|---|
|바운스가 `ok=False` dict 를 돌려주면 정리 경로를 안 탐 (architect·verifier·test HIGH)|`produce_template` 이 `ok` 아니면 `TemplateError` → `.failed` 보존 (`test_bounce_failure_dict_takes_cleanup_path`)|
|정리 helper 의 2차 예외가 `.failed` 개명과 원인 예외를 가림 (security·test HIGH)|`dismiss_panels`·`close_all_projects` 를 각각 `try/except`, 개명은 `finally` (`test_cleanup_helper_failure_still_renames_copy_and_reraises_cause`)|
|`copytree` 가 `try` 밖 (architect HIGH)|`try` 안으로 — 부분 사본도 `.failed` 로|
|리전 이름 OCR 실패가 `''` 로 조용히 통과 (verifier MEDIUM)|`regions != track_names` 면 `TemplateError` (`test_region_name_mismatch_fails_closed`)|
|템포 판정이 스모크에만 (verifier MEDIUM)|`produce_template` 에서 `lcd_tempo_value()` 와 SMF BPM 대조 (`test_tempo_mismatch_fails_closed`)|
|실행 중 예상 밖 창 검사 없음 (architect·verifier MEDIUM)|`assert_only_project()` 를 사본 열기 직후와 임포트 직후에|
|빈 믹서 읽기가 `[] == []` 로 통과 (test MEDIUM)|스냅샷 길이 < `NumberOfTracks` 면 `TemplateError` (`test_empty_mixer_read_fails_closed`)|
|SMF 트랙 이름 앞글자 충돌 → 같은 헤더 두 번 재할당 (security·test MEDIUM)|preflight 에서 앞 12자 유일성 검사 (`test_duplicate_track_name_prefixes_rejected`)|
|OCR 이 전체 화면을 봐 다른 앱 텍스트를 클릭 (security MEDIUM)|`front_window_rect()` 로 Logic 프로젝트 창 영역만 캡처(`screencapture -R`), 캡처는 `mkstemp` 임시 파일 후 삭제|
|`cg()` 가 실패를 삼킴 / `ensure_ocr` 재빌드 안 함 (security LOW)|returncode 검사 → `TemplateError`; `ocr.swift` mtime 이 새로우면 재빌드|
|이름의 `\|` 가 창 목록 파싱을 깸 (security LOW)|preflight 이름 검사에 `\|` 추가|
|라이브러리 토글 실패를 모름 (security MEDIUM)|반환값 False 면 `TemplateError`|
|AC2 `SamplerInstrumentsFiles` 검사 삭제 (전원)|스모크가 저장 사본 plist 에 `Violin (Arco).exs`(경로 C)·`Harpsichord.exs`(경로 B) 가 있는지 assert, 사본은 삭제하지 않음|
|AC1 리전 이름을 출력만 (architect·verifier)|스모크 `assert tuple(r['regions']) == SMOKE_TRACKS`|
|`--gm` 이 매핑을 assert 안 함 (test·verifier)|`gm_patch_map.json` 과 스트립 비교 + WAV 길이 assert|
|`windows_strict` 실제 구현·`save_quiet` 메뉴·스테퍼 삽입·`smf_end_bar`·`region_rows` 테스트 없음 (test)|`THelpers` 4건 + `test_smf_end_bar` + `test_end_bar_forwarded_to_bounce` 추가 (총 42 tests)|

## 반영 (문서)

- AC5 체크리스트에 트랙 이름·박자·프로젝트 끝 마커·믹서 보기 항목 추가(`LOGIC_LIBRARY_INVENTORY.md` §4.1).
- `test-plan.md` 결과 절을 최종 수치로 갱신.

## 반영하지 않음 (사유)

- `keystroke "{stem}"`(패널 검색 필드)·`keystroke "y"`(라이브러리) 의 IME 취약 가능성 (security MEDIUM): 두 경우 모두 결과를 바로 검증해요(검색 결과 행 OCR, 라이브러리 체크상자 값). 실패하면 fail-closed 라 그대로 두고 기록만 해요.
- `bounce_and_post` 의 홈 폴더 동명 `.aif` 삭제·`PROJ_DIR` `rmtree` (security MEDIUM): 기존 GM 경로 동작이라 이 사이클 범위 밖이에요. 템플릿은 `templates/` 아래라 `rmtree` 대상(`PROJ_DIR` 루트)과 겹치지 않아요.
- 템플릿 모드 `set value`/`AXIncrement` 스테핑 로직 자체는 Logic 없이 단위 테스트할 수 없어요 — 스모크(WAV 21.60 s)가 증거예요.

## 사용자 판단이 필요한 이탈 (verifier·architect 지적)

1. **AC0 판정표**: "배치 선택지 없음 → 불가로 종료" 대신, 같은 결과를 내는 대책(새 트랙 임포트 → 트랙 다시 할당 → 미사용 트랙 삭제)으로 진행했어요. 결과는 AC1–AC3 를 모두 만족해요. 사용자 승인으로 seed 를 갱신해야 해요.
2. **`save_quiet` 공유 변경**: 합성 ⌘S 가 한국어 입력 소스에서 새 트랙을 만드는 실측 때문에 `파일 > 저장` 메뉴로 바꿨고, 이는 GM 경로에도 적용돼요(constraints[9] 의 문자적 범위 밖). `--gm` 스모크는 변경 뒤에 통과했어요.
