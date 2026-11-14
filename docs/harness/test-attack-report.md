# Test Attack Report — `20261113-220009-a606` (GATE 1.5)

- 2026-11-13, critic `adversary-sol` (openai-codex/gpt-5.6-sol), primary `anthropic/claude-fable-5-1` — 이종 계열
- 집계: CRITICAL 0 · HIGH 15 · MEDIUM 1 → **PASS**
- 반영: `docs/harness/test-plan.md` "Test Attack 반영" 절 (T2–T8 보강, AC4 manifest, AC5 수동 대조)
- 미반영(사유): parse_smf running status·VLQ meta — 우리 writer 가 만들지 않는 형식이라 범위 밖(기존 동작 유지); AC5 자동 문서 검사 — 소스 텍스트 검사라 verifier 수동 대조로 대체

## 원문 요약

(a) 놓치는 실패 시나리오: 복사 후 실패 정리 미검증 / strict 창 조회 실패·허용 밖 창 미검증 / AC5 검증 항목 없음
(b) 빠진 엣지: parse_smf running status·VLQ meta / plist 타입·BPM·Alternatives 정책 / conductor 제외가 실제 SMF 와 연결 안 됨 / tree_hash symlink·빈 디렉터리·mode / 9마디 구간 반열림 경계
(c) 통과해도 남는 버그: T1 골든 해시 범위 / T4 상대 경로 프레이밍 / T7·T8 LogicLock·네임스페이스 격리 / 금지 helper 호출 미검증 / preflight 순서 미추적 / 사본이 아닌 원본 open 미검증 / SMF≠템플릿 BPM 전제 / 스냅샷 동어반복
