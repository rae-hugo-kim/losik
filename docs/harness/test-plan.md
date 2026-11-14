# Test Plan — `20261113-220009-a606` 템플릿 패치 로드 자동화

**Approved**: 2026-11-13 (사용자 승인)
**Files**: `docs/music/tools/test_template_mode.py`(unittest, Logic 미접촉), `docs/music/tools/template_smoke.py`(`--dry-run` / `--preflight` / `--spike` / `--template` / `--gm`)
**Runner**: `python3 -m unittest docs/music/tools/test_template_mode.py` (pytest 없음, 표준 라이브러리만) → `docs/harness/verify-commands.json` 에 등록

## Unit Tests (Logic 없이)

- [x] T1 `build_smf(pcs=None)` → `parse_smf` 의 모든 트랙 `pcs == []`; `pcs` 딕셔너리를 주면 기존과 바이트 동일(RED 단계에서 현재 코드로 골든 해시 고정) — AC4, constraints[2],[8]
- [x] T2 `parse_smf` 가 트랙별 CC 번호 목록(`ccs`)과 첫 노트 tick(`first_note_tick`)을 돌려준다 — 더미 SMF 에 CC7 하나 → `ccs == [7]`, 노트 시작 tick 일치 — AC6 dry-run 전제
- [x] T3 `template_meta(path)`: 임시 `.logicx` 에 `Alternatives/000/MetaData.plist`(plistlib) → `{tracks: 4, bpm: 92.0}`; plist 없음 / `NumberOfTracks` 없음 → `TemplateError` — constraints[5]
- [x] T4 `tree_hash(path)`: 같은 내용의 두 복사본은 같은 해시, 1바이트 변경 시 다른 해시, 파일 열거 순서 무관, 하위 디렉터리 재귀 — AC3
- [x] T5 `preflight_template(template, proj, smf_tracks)`: (a) 템플릿 없음 (b) 사본 경로 이미 있음 (c) `smf_tracks > NumberOfTracks` → 각각 `TemplateError`(메시지에 원인); (d) 정상 → meta 반환. `osascript` 미호출 — AC6 (1)(2)(3)
- [x] T6 `smoke_smf()`: 트랙 4, 9마디, 트랙 이름 모두 다름, BPM 100, 마디 1 노트 없음, 트랙 i 노트가 마디 2i+2~2i+3 안에만, `pcs == []`, `ccs` 에 0/7/10/32 없음 — AC1·AC2 전제, AC6
- [x] T7 `produce(template=...)`: 프로젝트 창이 열려 있으면(`_windows_strict` monkeypatch) 복사 전에 `TemplateError`, 사본 디렉터리 미생성 — AC6 (4), constraints[6]
- [x] T8 `produce(template=...)`: preflight 실패 시 `close_all_projects`·`open` 미호출(기록용 스텁) — constraints[6]

## Edge Cases

- [x] `template_meta`: `NumberOfTracks` 키 없음 → `TemplateError`
- [x] `tree_hash`: 빈 디렉터리 허용, 하위 디렉터리 재귀
- [x] `failed_name(proj, ts)` → `<proj>.failed-<ts>.logicx` 형식
- [x] `build_smf(pcs=None, cc={})`: 트랙 청크가 이름 meta + 노트만 포함

## Integration (Logic 필요 — 스모크 로그가 산출물, 테스트 아님)

- [x] AC0: `template_smoke.py --spike` — 템플릿 제작(AX·MCP) + 9항목 실측 → FEEDBACK_LOG, 판정표 적용
- [x] AC1–AC3: `template_smoke.py --template .../tplsmoke.logicx` 1회 → 반환 dict assert, WAV 길이·마디 1 RMS·구간 RMS·`SamplerInstrumentsFiles`, 해시 전후
- [x] AC4: `template_smoke.py --gm` 1회 + `verify-commands.json` 스크립트 SMF 해시 전후 비교
- [x] AC6: `--preflight` 실패 3건 + 프로젝트 창 열림 1건 실행 로그

## 순서

T1 → T2 → T3 → T4 → T5 → T6 → T7 → T8 → AC0 스파이크 → 임포트·수집 구현(AC0 반영) → AC1–4 스모크 → AC5 문서. git 커밋은 사용자 지시 시점에.

## Test Attack 반영 (GATE 1.5, `adversary-sol`, PASS — `docs/harness/test-attack-report.md`)

- T2 보강: velocity-0 note-on 은 노트로 세지 않음, 노트 없는 트랙은 `first_note_tick is None`. running status·VLQ meta 는 우리 writer 가 만들지 않으므로 범위 밖(기존 parser 동작 유지).
- T3 보강: `BeatsPerMinute` 누락·비수치·0 이하 → `TemplateError`; `NumberOfTracks` 비정수·0 이하 → `TemplateError`; XML·binary plist 모두 읽음; `Alternatives/000` 만 본다(정책 명시).
- T4 보강: 파일 이름 변경·두 파일 내용 교환·파일 추가/삭제 모두 다른 해시(상대 경로·길이·내용을 프레이밍); 심볼릭 링크는 `TemplateError`.
- T5 보강: `preflight_template` 은 SMF 경로를 받아 `parse_smf` 로 음악 트랙 수(conductor 제외 = `ntrk - 1`)를 직접 계산 — conductor+4트랙 SMF 는 4트랙 템플릿에서 통과, conductor+5트랙은 실패.
- T6 보강: 트랙 i 의 첫 노트 tick ≥ `[1,3,5,7][i]*BAR`, 마지막 note-off tick ≤ `[3,5,7,9][i]*BAR`(반열림), 마디 1(`[0, BAR)`) 전 트랙 노트 없음, 템플릿 BPM 과 다르다는 전제는 스모크가 `template_meta(...).bpm != 100` 으로 assert.
- T7/T8 보강(모두 `pipeline` 모듈 네임스페이스에 monkeypatch, `PROJ_DIR` 은 임시 디렉터리, `LogicLock` 은 기록용 no-op, `subprocess.run` 은 기록용 스텁):
  - T8a 호출 순서 추적: 정상 경로에서 `_windows_strict → preflight(meta·hash) → copytree → open(사본 경로)` 순서, `open` 인자가 사본 경로와 같고 템플릿 원본 경로는 어떤 호출에도 등장하지 않음.
  - T8b 금지 helper: `clear_alerts`·`metronome_off`·`save_project_as` 를 호출 즉시 실패하는 스텁으로 두고 정상 템플릿 경로가 통과.
  - T8c 스냅샷 순서: `mixer_strips` 스텁이 호출마다 다른 값을 돌려주고, 반환 dict 의 `snapshot` 은 1회차(사본 open 직후), `strips` 는 2회차(임포트 후), 둘 다 `save_quiet` 호출 전.
  - T8d 복사 후 실패 정리: open 단계에서 예외 주입 → `close_all_projects(save=False)` 호출, 사본이 `<proj>.failed-<ts>.logicx` 로 이름 변경, 원본 해시 불변.
  - T7 보강: `_windows_strict` 가 예외를 내면 전파(빈 목록 취급 금지), 허용 목록 밖 창 이름이 있으면 `TemplateError`, 두 경우 모두 copytree 미호출.
- AC4 보강: RED 전에 `verify-commands.json` 스크립트가 만드는 `sketches/*.mid` 의 SHA-256 manifest 를 `docs/harness/smf-manifest-before.txt` 에 기록하고 GREEN 뒤 같은 manifest 와 비교.
- AC5 는 문서라 자동 검사 없음 — verifier 가 §4 B·C 행과 체크리스트 항목을 수동 대조.

## 결과 (2026-11-14, 최종 — GATE 3.5 반영 뒤 재실행)

- 단위: `python3 -m unittest docs/music/tools/test_template_mode.py` → **42 tests OK** (T1–T8 + 엣지 + THelpers 4 + fail-closed 7: 스트립 변경·바운스 실패 dict·템포 불일치·리전 불일치·정리 helper 2차 예외·빈 믹서·이름 접두 중복·따옴표 이름).
- 커밋 시점: `python3 docs/music/tools/template_smoke.py --dry-run` → OK (`verify-commands.json` 등록).
- AC0: 9항목 실측 `FEEDBACK_LOG.md` "2026-11-13~14" 절. 판정표의 "배치 선택지 없음" 이 실제였고, 같은 결과를 내는 대책(새 트랙 임포트 → 트랙 다시 할당 → 미사용 트랙 삭제)으로 진행했어요 — **사용자 승인 대기 항목**. 리전 시작 위치는 Logic 이 SMF 절대 위치에 놓으므로(실측 5) "1 1 1 1" 대신 구간 RMS 로 배치를 검증했어요(판정표의 지정 대책).
- AC1–AC3: `template_smoke.py --template …/tplsmoke.logicx` (01:14, 최종 코드) → `TEMPLATE SMOKE OK`. strips == snapshot(악기 4 + Aux 3), regions == SMF 트랙 이름(assert), tempo 100.0 == SMF(템플릿 87), WAV 21.60 s(기대 21.60), 마디 1 −95.7 dBFS, 구간 RMS [-20.1, -21.9, -29.6, -19.2], 템플릿 해시 전후 `d7c74c1aa219bef3…`, 저장 사본 `Tpl Smoke 011402.logicx` 의 `SamplerInstrumentsFiles` 에 `Violin (Arco).exs`(경로 C)·`Harpsichord.exs`(경로 B) 존재(assert). 사본은 보존.
- AC4: `--gm` (01:11, 최종 코드) → `GM SMOKE OK`: 스트립 `[Kensington, Muted Clav, Studio Violins 1, SoCal]` == `gm_patch_map.json` PC 48/6/40·킷 0 (assert), WAV 21.60 s. 기존 스케치 SMF 204개 해시 manifest 동일(`docs/harness/smf-manifest-before.txt` 대비 diff 없음).
- AC6: 실패 4건(템플릿 없음·사본 존재·5트랙>4·프로젝트 창 열림) 모두 Logic 조작 전 `TemplateError`, 사본 없음(00:58 실측 + 단위 테스트).
- 제약 밖 공유 변경 1건: `save_quiet()` 를 메뉴 클릭으로(합성 ⌘S 가 새 트랙을 만드는 실측). GM 경로 결과 동일 — **사용자 확인 대기 항목**.
- **PR #4 머지 뒤 재실행 (22:15/22:22, 머지 코드)**: `GM SMOKE OK`, `TEMPLATE SMOKE OK`. 기존 SMF 204개 해시 동일(PR #4 가 추가한 87개는 manifest 밖). 단위 테스트 42 OK.
- **커밋 리뷰 반영 뒤 최종 (23:19)**: `TEMPLATE SMOKE OK` (고유 토큰 임포트 경로). 단위 테스트 46 OK. 리뷰 사이드카 `docs/reviews/review-2026-11-14-2311xx.*`(PASS WITH NOTES) → 최종 해시로 재바인딩.
