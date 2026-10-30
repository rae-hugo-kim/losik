# Vivaldi Astra 변주 세트 완료 기준입니다.

- 모델은 `openai-codex/gpt-6-astra`이며, 기존 제작 레시피를 사용해 12악장 변주 세트를 만듭니다.
- 사용자 승인(2026-10-30)은 `git merge issuereport`와 `rae-hugo-kim/band-astra` 커밋까지입니다. 푸시·main 머지·하네스 재동기화는 하지 않습니다.
- 기존 `.omp/mcp.json` 로컬 변경과 `VIVALDI_KICKOFF.md`는 커밋에 포함하지 않습니다.

## Acceptance criteria

- [x] AC1: 브리프 §0의 충돌 규칙으로 issuereport 병합을 완료합니다. 병합 커밋은 `ffc2cd9`이며 독립 리뷰는 PASS WITH NOTES입니다.
- [x] AC2: `tools/vivaldi_astra.py`의 SKETCHES 12개와 compose(sid), 재현 가능한 MIDI 12개를 제공합니다. 원전 한 성부만 사용하고 리듬 변형 2종 이상, 원리듬 연속 ≤4마디, 주제 구간 40~60%, 원본 대비 BPM 변화 ≥15%, 마커·CC64·검증 PC·장르 벨로시티·마지막 노트 경계를 검증합니다.
- [x] AC3: 세션 간 잠금을 사용하는 pipeline.produce로 WAV 24bit 12개와 Logic 프로젝트 12개를 만들고, 실제 패치·메트로놈·길이·피크·RMS·의도하지 않은 디지털 무음을 점검합니다. 잘린 물리 WAV와 한 채널 전체 무음도 거부합니다. 화면의 메트로놈 꺼짐·84 BPM 확인은 첫 곡에 한정하며, 나머지는 클릭 기록과 MIDI/WAV 길이 검증입니다.
- [x] AC4: `suno/vivaldi_astra.md`에 Style ≤300자, Description ≤1,000자의 12블록을 제공하고 len() 실측을 기록합니다.
- [x] AC5: FEEDBACK_LOG 끝에 모델 ID·12곡 표·설계 판단·검증·미확인 업로드 결과를 기록합니다. 원전 Mutopia Project와 CC BY-SA 3.0을 코드·MIDI·기록에 명시합니다.
- [x] AC6: `docs/sum/session_2026-10-30_vivaldi-astra.md`에 과정·결정·실패·결과를 기록하고 리뷰 및 verifier 판정을 받습니다. 코드 리뷰는 PASS WITH NOTES, VivaldiVerifier는 AC1–AC6 PASS이며 블로커가 없습니다.

브랜치 커밋은 위 기준 검증 후 실행하는 전달 절차입니다. Suno 업로드·사용자 청취 판정은 이 세션의 완료 기준이 아니며 결과를 받으면 기록하고, 차단된 곡만 브리프 §2-6에 따라 v2로 개작합니다.
