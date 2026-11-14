# Plan Attack Report — `20261113-220009-a606` (템플릿 패치 로드 자동화)

## Run 1 — 2026-11-13, critic `adversary-opus` (anthropic/claude-opus-5-5)

- 집계: CRITICAL 1 · HIGH 12 · MEDIUM 9 → 판정 **BLOCK**(run_count=1 이라 규칙상 WARN 이지만 CRITICAL 이 실제 결함이라 seed 를 수정)
- Heterogeneity: primary `anthropic/claude-fable-5-1`, critic `anthropic/claude-opus-5-5` — 같은 계열(UNVERIFIED heterogeneity)

### 발견과 반영

|#|심각도|발견(요약)|반영(seed 필드)|
|---|---|---|---|
|1|CRITICAL|템플릿(제목 있는 문서)에서 `save_project_as()` 는 저장 패널이 안 떠 항상 `stage='save'` 실패, 임포트 뒤 저장 시 템플릿 번들에 리전이 저장됨(`pipeline.py:323-325, 764-766`)|`constraints[0-1]`: `copytree` 사본만 열고 `save_quiet()` 만 사용, `save_project_as` 금지|
|2|HIGH|"기존 트랙 사용" 선택지는 레포에 실측 0건|`goal`·`AC0`: 스파이크를 0단계로 분리, 불가 시 판정 기록으로 사이클 종료|
|3|HIGH|열린 프로젝트로 `open -a` 임포트 미실측, 메뉴 임포트는 ⌘⇧G 합성 입력 불가(`pipeline.py:496-497`)|`assumptions[1]`: 패널 기본 폴더에 복사해 이름으로 선택하는 대안 포함, AC0 항목 (1)|
|4|HIGH|conductor 청크(`pipeline.py:82`)로 트랙 대응이 한 칸 밀릴 수 있음|`assumptions[2]`, AC0 항목 (3), AC1 리전 이름 검증|
|5|HIGH|템플릿에서 `mixer_strips()` 순서·개수 보장 없음(Aux·Stack·멀티 출력)|AC0 항목 (4), AC1 "템플릿 직후 스냅샷과 개수·순서·이름 정확히 일치", AC5 체크리스트에 Aux·Stack·Drummer 금지|
|6|HIGH|`finish()` 의 '무제 - 트랙' 하드코딩으로 메트로놈 OFF 조용히 실패|`constraints[8]` `finish(win_title)`, AC2 메트로놈 상태 재확인, `risks[4]`|
|7|MEDIUM|`clear_alerts()` 가 선택 대화상자에 첫 버튼을 자동 클릭|`constraints[3]`: 템플릿 모드에서 미사용, 라벨 지정 클릭, 예상 밖 창은 실패|
|8|HIGH|AC1 이 동어반복(스트립 목록은 템플릿 재측정)|AC1: 새 트랙 0개 + 리전 이름 = SMF 트랙 이름 + `lcd_tempo`|
|9|HIGH|AC2 ±1초는 릴리스 꼬리와 불일치, 템플릿 BPM 기준 오류, 피크만으론 메트로놈으로 통과|AC2: SMF BPM 기준 −0.1s~+12s(`vivaldi_astra.py:348-349` 선례), 메트로놈 OFF 재확인, 마디 1–8 RMS|
|10|HIGH|AC3 디렉터리 mtime 은 내부 파일 변경을 못 잡음|AC3: 번들 전체 sha256 트리 해시|
|11|HIGH|AC4 "같은 SMF" 는 PC 가 없어 비교 불가, `build_smf` 변경 영향 미검증|AC4: `--gm` 별도 SMF(PC 포함) + 기존 스크립트 SMF 바이트 동일성|
|12|MEDIUM|커밋 시점 판정 가능한 AC 없음|AC6 `--dry-run` + `verify-commands.json` 등록|
|13|MEDIUM|실패 케이스 AC 없음, `close_all_projects(save=False)` 가 검증보다 먼저|AC6 실패 3건, `constraints[6]` 검증 선행 + `try/finally`|
|14|HIGH|템포 소유 미정|`constraints[4]` SMF 가 정함 + `lcd_tempo` 확인, AC1 SMF BPM ≠ 템플릿 BPM|
|15|HIGH|실패 시 정리 경로 없음, 기본 `close_all_projects()` 는 제목 있는 프로젝트를 저장(`pipeline.py:230`)|`constraints[6]` `try/finally close_all_projects(save=False)`; 원본은 아예 열지 않음|
|16|HIGH|저장 위치 통제 불가·동명 "대치" 자동 클릭(`pipeline.py:347`)|`constraints[0]` 사본 경로는 코드가 정하고 존재 시 실패; `save_project_as` 미사용|
|17|MEDIUM|CC0/7/10/32 가 템플릿 볼륨·팬·뱅크를 덮음, `build_smf` 호출자 25개|`constraints[2]` CC 금지 assert, `constraints[7]` `pcs=None` 외 변경 금지 + 바이트 동일|
|18|MEDIUM|드럼 트랙 형태 미정(멀티 출력·Drummer)|AC5 체크리스트: 소프트웨어 악기 트랙 + 단일 출력 킷, Drummer 금지|
|19|MEDIUM|트랙 수 초과를 경고만|`constraints[5]` 실패로 격상, AC6 (3)|
|20|MEDIUM|`LogicLock` 재진입 불가(`pipeline.py:691`)|`constraints[10]` 스모크는 잠금 미획득|
|21|MEDIUM|AC5 템플릿 절차 범위 협소|AC5 체크리스트 확장|
|22|MEDIUM|Netac 템플릿의 샘플 누락 대화상자|`risks[3]`, `constraints[3]` 예상 밖 창 = 실패|

## Run 2 — 2026-11-13, 수정판 재공격, critic `adversary-opus`

- 집계: CRITICAL 0 · HIGH 4 · MEDIUM 9 → 판정 **WARN**(규칙상 run_count≥2 는 CRITICAL 시 BLOCK — 해당 없음, 진행 가능)
- 1차 22건 처리: RESOLVED 13 · PARTIAL 9 · OPEN 0 (1차 CRITICAL 은 복사본 + `save_quiet` 로 해소 확인)

### 발견과 반영

|#|심각도|발견(요약)|반영(seed 필드)|
|---|---|---|---|
|a-1|HIGH|AC6(3) 트랙 수 초과를 `close_all_projects()` 전에 판정할 수단이 없음. 실측: `PROJ_DIR` 번들 `Alternatives/000/MetaData.plist` 에 `NumberOfTracks`·`BeatsPerMinute` 키 있음|`constraints[5]` plistlib 선판정, AC0 (4) `NumberOfTracks` 대조, `assumptions[4]`|
|a-2|HIGH|`bounce_and_post` 가 프로젝트를 닫으므로(`pipeline.py:803-804`) 스모크가 AC1 값을 읽을 시점이 없음|`constraints[7]` `produce(template=)` 가 `save_quiet` 전에 수집해 반환 dict 로, 스모크는 assert 만|
|a-3|MEDIUM|AC0 판정이 가능/불가 둘뿐 — conductor 한 칸·채널 대응·드래그 전용·템포 미반영의 처리 없음|AC0 판정표 추가(각 경우 종료 또는 지정 대책)|
|a-4|MEDIUM|메뉴 임포트 패널의 현재 폴더를 알 방법 없음|AC0 (1) 패널 폴더 AX 읽기 실측, `assumptions[1]` 고유 이름 복사·실행 뒤 삭제|
|b-1|HIGH|경로 B·C 가 실제 소리를 냈는지 어떤 AC 도 증명 못함(전체 RMS, 스트립 이름)|AC1·AC2: 마디 1 무음 + 트랙 i 는 마디 2i+2~2i+3 만 연주, 구간별 RMS > −40, `SamplerInstrumentsFiles` 에 .exs|
|b-2|HIGH|`metronome_off` 는 '켜진 체크박스 중 마지막' 휴리스틱(`pipeline.py:401`)이라 재확인이 동어반복, 템플릿은 이미 OFF|`constraints[3]` 템플릿 모드 `metronome_off` 미사용, AC2 마디 1 RMS < −60(클릭 부재), AC5 메트로놈 OFF|
|b-3|MEDIUM|AC0 실측 목록에 리전 읽기·트랙 이름 변경·창 제목·바운스 저장 위치·대화상자 라벨 누락|AC0 (1)(2)(5)–(9) 추가, `risks[5]`|
|b-4|MEDIUM|리전 시작 위치 미확인|AC1 "리전 시작 1 1 1 1", AC2 구간 RMS 가 1마디 밀림을 잡음|
|b-5|MEDIUM|AC0 불가 시 AC5 가 사실과 다른 문서 요구|AC5 불가 분기|
|b-6|MEDIUM|`windows()` 는 osascript 실패를 `[]` 로 돌려줘(`pipeline.py:167`) 예상 밖 창 감지가 거짓 성공|`constraints[3]` `_windows_strict` 패턴 + 허용 창 목록|
|c-1|MEDIUM|테스트 템플릿 제작이 AC0 보다 먼저 필요한데 순서·경로·체크리스트 항목(플러그인 창·끝 마커·재생헤드) 누락|AC0 "체크리스트 초안대로 만든 `PROJ_DIR/templates/tplsmoke.logicx`", AC5 항목 추가|
|c-2|MEDIUM|실패 사본이 재실행을 막음, sid 규칙 없음, `--gm` 경로의 동명 `rmtree`(`pipeline.py:807-811`)|`constraints[6]` `.failed-<ts>` 보존, `constraints[11]` `tplsmoke-<ts>` sid|
|c-3|MEDIUM|시작 시 `close_all_projects(save=False)` 가 사용자 작업을 버림, 자동 저장이 AC3 오탐|`constraints[6]` 프로젝트 창 열려 있으면 시작 거부(`gm_map.measure` 패턴), 해시는 그 뒤 기록; `risks[4]`|

### 판정

- CRITICAL 0 → **PASS 로 진행**. HIGH 4건은 모두 seed 에 반영했고, 남은 불확실성은 전부 AC0 스파이크의 실측 항목으로 옮겼어요.
- Heterogeneity: 두 번 모두 primary `claude-fable-5-1` / critic `claude-opus-5-5` 로 같은 계열(UNVERIFIED). 계획 단계 공격이라 이 기록으로 충분하다고 판단했고, 구현 리뷰(review-gate)에서는 이종 패널을 써요.
