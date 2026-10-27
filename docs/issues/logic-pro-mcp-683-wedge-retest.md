# #683 wedge 재검증 기록 (2026-09-05 KST)

`MongLong0214/logic-pro-mcp#683`에서 메인테이너가 요청한 "#759 머지 빌드로 wedge를 다시 시험해
crash와 deadlock을 분리해 달라"는 부분을 실행한 기록입니다. 결론부터: **Mackie Control 서피스를
실제로 바인딩한 상태에서 v3.14.0과 #759 머지 빌드 모두 wedge가 재현되지 않았습니다.** 판정표
3행("둘 다 정상")에 해당하며, 08-24의 wedge가 설치본 3종이 공존한 환경 교란이었다는 해석을
강화합니다. 게시할 코멘트 초안은 [`logic-pro-mcp-683-wedge-comment-draft.md`](logic-pro-mcp-683-wedge-comment-draft.md)에
있습니다.

## 환경

macOS 26.5.2 (Apple M4), Logic Pro Creator Studio 12.3.1 (`com.apple.mobilelogic`). 서버는
`LOGIC_PRO_BUNDLE_ID=com.apple.mobilelogic LOG_LEVEL=debug`로 기동했고 stderr는 파일로 보냈습니다.
이전 회신에서 문제였던 프로세스명 충돌은 이렇게 통제했습니다: 다른 포크(`logic-pro-mcp-creator`)
인스턴스 하나가 다른 omp 세션의 MCP 서버로 계속 떠 있었지만(kill 시 그 세션이 자동 재기동), 그
포크가 만드는 포트는 `LogicProMCP-In/Out`이어서 `LogicProMCP-MCU-Internal`과 겹치지 않고, 러너는
`pgrep` 대신 자기 자식 pid로 `sample`을 뜨도록 했으므로 모호성이 없습니다.

비교 쌍은 계획서(`/tmp/evidence/wedge-plan.md`)대로입니다.

| 라벨 | 바이너리 | 의미 |
|---|---|---|
| before | `~/.local/opt/logic-pro-mcp/LogicProMCP` (v3.14.0 타르볼) | 08-24 원 보고 시점의 바이너리 |
| after | `/tmp/mong-src/.build/release/LogicProMCP` (main @ 8d3730c, 09-03 빌드) | #759 머지본 |

## 절차

서피스 바인딩은 사용자가 GUI에서 했습니다. 먼저 before 서버를 띄워 포트가 보이게 한 뒤, Logic →
Control Surfaces → Setup → New → Install → Mackie Control을 추가하고 Out Port와 Input을 모두
`LogicProMCP-MCU-Internal`로 지정했습니다. CoreMIDI 오류 모달은 뜨지 않았습니다.

각 시행은 새 서버 프로세스 하나로 원 보고의 시퀀스를 그대로 밟습니다.

1. `initialize` (30초 예산)
2. `notifications/initialized` 후 settle 대기 — Logic이 새 포트에 다시 붙어 MCU 핸드셰이크를 보낼 시간
3. `tools/list` (60초 예산; 원 보고의 "no reply, ever" 판정 구간). 무응답이면 `sample <pid> 5` 채취와
   `pgrep -x MIDIServer` 확인
4. 응답이 오면 `logic_system health`를 호출해 `mcu.connected / registered_as_device /
   last_feedback_at`로 **Logic이 실제로 붙어 있었는지** 확인

4번은 첫 시행 뒤에 추가했습니다. 첫 시행(`surface-v3140`)은 전체가 1초 만에 끝나 Logic이 붙을
시간이 없었고, 서버는 피드백 수신을 로그에 남기지 않으므로(`MCUChannel.swift:398` 이후 수신 로그
없음, 상태는 `StateCache`에만 반영) 바인딩 여부를 stderr로는 알 수 없었습니다.

## 결과

서피스가 실제로 붙어 있던 시행(health에서 `connected=true, registered_as_device=true`)만 판정에
씁니다.

| 시행 | 바이너리 | settle | MCU 연결 | initialize | tools/list | 결과 |
|---|---|---|---|---|---|---|
| `surface-v3140-health` | v3.14.0 | 20s | 연결·등록 확인, 피드백 16:34:42Z | 0.076s | 0.022s | 정상 |
| `surface-fixed-health` | main@8d3730c | 20s | 연결·등록 확인, 피드백 16:35:12Z | 0.116s | 0.025s | 정상 |
| `surface-v3140-t1` | v3.14.0 | 10s | 연결·등록 확인 | 0.046s | 0.021s | 정상 |

60초 무응답은 한 번도 없었고 `sample`도 한 번도 트리거되지 않았습니다. 나머지 시행
(`surface-v3140`, `surface-v3140-settle`, `fixed-t1~t3`, `v3140-t2~t3`)도 전부 정상 응답했지만
`mcu.connected=false`였으므로 wedge 판정에는 쓰지 않고 참고용으로만 남깁니다.

부수 관찰 하나. 연속 시행에서 서버 프로세스를 여러 번 재기동하자 세 번째 프로세스부터 Logic이
붙지 않았습니다(`connected=false`). Logic의 Setup 창에는 포트 이름이 그대로 남아 있었으므로
(사용자 확인), UI 표시와 실제 연결이 어긋난 상태입니다. 가상 포트의 uid가 프로세스마다 바뀌어
재부착이 지연되거나 실패하는 것으로 보이지만 원인은 확인하지 않았습니다.

## 판정

계획서의 판정표에서 "before 정상 / after 정상" 행입니다. 서피스가 붙은 상태에서도 wedge가 재현되지
않으므로 crash(#759로 수정)와 deadlock(#683)을 이 호스트에서 분리해 보일 수는 없고, 08-24의 관찰이
v3.14.0의 결함이라는 주장은 더 유지할 수 없습니다. 이전 회신에서 예고한 대로 결과가 부정적이어도
게시합니다.

사용자가 제기했던 "입출력 포트를 반대로 꽂았을 가능성"은 08-31에 이미 처리해 09-03 회신에
포함했습니다(피드백이 전무한 배선에서도 약 2초 내 `readback_unavailable` 봉투가 돌아와 "무응답,
타임아웃 봉투 없음"을 설명하지 못함). 오늘 결과는 반대 방향의 증거를 보탭니다 — 올바른 배선에서도
wedge가 없습니다. 추가 검증은 하지 않았습니다.

## 사후 정리

테스트 후 사용자가 Mackie Control 서피스를 삭제해 Logic 설정을 원상 복구했습니다. 바인딩용으로
띄웠던 before 서버는 러너 실행 전에 내렸고, 러너가 만든 프로세스는 매 시행 종료 시 terminate했습니다.

## 증거

- 시행별 stderr와 결과 JSON: [`evidence/683-wedge-retest/`](evidence/683-wedge-retest/) (`/tmp/evidence/`에서 복사)
- 계획서: `/tmp/evidence/wedge-plan.md` (임시 경로, 유실 가능)
- 러너: 직전 세션의 `wedge_test`를 복원해 settle과 health 프로브를 더한 `wedge_test3` (Python, 세션 커널 내)
