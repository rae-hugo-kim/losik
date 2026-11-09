---
alwaysApply: true
---
# losik 세션 위계 (프로젝트 규칙, 2026-11-09 확정)

저장소 `rae-hugo-kim/losik` 의 워크트리·브랜치·세션은 네 층이에요. 어떤 세션이든 자기 층을 먼저 확인하고 그 층의 규칙만 따라요.

## 층

| 층 | 브랜치 | 워크트리 | 역할 |
|---|---|---|---|
| 0 메인 세션 | `main` | `/Volumes/Netac 2TB/workspace/losik` | 안정판. 하네스 동기화(`harness-check`)는 여기서만 하고 아래로 머지해 내려보내요. 작업 커밋을 직접 받지 않아요. |
| 1 통합 세션 | `issuereport` | `/Users/hugom4/orca/workspaces/losik/chats` | 음악 프로젝트의 **작업 기준선**이에요. 브랜치 세션은 여기서 갈라지고 여기로 PR 을 내요. 머지·충돌 해소·롤아웃 결정은 이 세션이 해요. `main` 과는 `main → issuereport` 머지(하네스 하강)와 `issuereport → main` PR(승격)로만 만나요. |
| 2 주제 세션 | `rae-hugo-kim/<topic>` | `/Users/hugom4/orca/workspaces/losik/<topic>` | 한 주제(사계, 향후 다른 셋·조사)를 **지속적으로** 맡아요. `orca worktree create --base-branch issuereport` 로 만들고 Orca 부모는 `chats` 예요. 중간 산출물도 `issuereport` 로 PR 을 내요(예: PR #2). 모델별 라운드가 필요하면 아래 3층을 열고 그 결과를 자기 브랜치에 집계해요. |
| 3 라운드 세션 | `rae-hugo-kim/<topic>-<model>` | `/Users/hugom4/orca/workspaces/losik/<topic>-<model>` | 한 라운드(한 모델, 한 브리프)만 하고 닫아요. base 와 Orca 부모는 **주제 세션**이에요. 결과는 주제 브랜치로만 넘기고(주제 세션이 머지·집계) `issuereport` 로 직접 PR 을 내지 않아요. 열고 닫는 것은 주제 세션이 해요. |

현재: 주제 세션 `vivaldi`(사계 v1 집계·PR #2 머지됨, v2 진행 중). 라운드 세션 `band-astra`·`band-fable`·`band-opus` 는 사계 v1 라운드였고(이름이 주제를 안 보여 주지만 유지), v2 라운드에 재사용하거나 `vivaldi-<model>` 로 새로 열어요. `issue` 워크트리는 `main` 에 전부 포함된 채 2026-09 부터 정지한 **폐기 대상**이에요(제거는 사용자 지시로만).

## 라운드 세션을 닫기 전에 (MUST)

`docs/sum/` 과 `docs/reviews/` 는 untracked 라 `git worktree remove` 가 경고 없이 지워요. 닫기 전에 순서대로:

1. 산출물(코드·MIDI·브리프·FEEDBACK_LOG·Suno 블록)이 부모 브랜치에 머지됐는지 확인해요 — `git log <parent>..<branch>` 가 비어야 해요.
2. `sum` 을 실행해요 — 메인 체크아웃 `/Volumes/Netac 2TB/workspace/losik/docs/sum/` 사본과 sum-vault 백업까지 끝나야 해요.
3. `docs/reviews/*` 를 메인 체크아웃 `docs/reviews/` 로 복사해요(파일명이 타임스탬프라 충돌 없음).
4. 브랜치를 푸시해 원격에 남겨요(승인).
5. 그다음 `orca worktree rm`. 바운스·Logic 프로젝트는 `/Volumes/Netac 2TB/music/` 에 있어 영향이 없어요.

2026-11-09 백필: 사계 v1 라운드 sum 3개(10-27 fable·opus, 10-30 astra)를 메인 체크아웃·vault 에, band-*·vivaldi 의 리뷰 파일 61개를 메인 체크아웃 `docs/reviews/` 에 복사했어요.

## 규칙

- **base 와 PR 대상**: 주제 세션은 `issuereport`, 라운드 세션은 자기 주제 브랜치예요. `main` 을 base 로 브랜치를 만들거나 `main` 으로 PR 을 내지 않아요(하네스 동기화 머지 제외).
- **푸시는 세션별 명시 승인** 이 있어야 해요(`rule://harness-core`). PR 을 열 때 그 세션에서 승인받아 푸시하고, 통합 세션의 푸시도 매번 승인받아요. `issuereport` 로의 머지는 통합 세션만, 주제 브랜치로의 머지는 그 주제 세션만 해요(`gh pr merge` 포함, 승인 필요).
- 브랜치 세션은 **다른 브랜치·워크트리를 건드리지 않아요**. 공유 자원은 저장소 밖이에요: Logic 단일 인스턴스(`pipeline.LogicLock` 으로 세션 간 직렬화), 바운스 `/Volumes/Netac 2TB/music/bounces/`, Logic 사운드 라이브러리(Netac). 바운스 결과 파일은 `BOUNCE_SEARCH` 가 형제 워크트리의 `sketches/` 까지 봐요.
- **인계는 복사로**: `docs/sum/` 은 untracked 라 브랜치를 타지 않아요. 세션을 넘길 때 인계 sum 을 새 워크트리 `docs/sum/` 에 복사하고 루트에 `<TOPIC>_KICKOFF.md`(미커밋) 를 둬요.
- 하네스 버전은 `main` 이 기준이에요. 브랜치 세션에서 하네스 동기화를 다시 하지 않아요 — 뒤처졌으면 `git merge main`(승인) 으로 받아요.
- 브랜치 세션의 결정이 프로세스 전체에 닿으면(규칙 문서·GM 매핑표·파이프라인) PR 본문에 그 사실을 적고, 통합 세션이 머지 뒤 `.omp/rules/` 또는 `docs/music/PROMPT_GUIDELINES.md` 로 승격해요.

## 지금 상태의 출처

실측 2026-11-09: `main 64aca55` 는 `issuereport` 의 순수 조상(main 전용 커밋 0), PR #2 머지 후 `issuereport 05421f0` 은 main 대비 +73, band-* 는 issuereport 대비 −30 안팎(v1 산출물은 전부 포함됨), `issue` 는 main 대비 −5 / +0. Orca 부모가 있는 워크트리는 `vivaldi`(부모 `chats`) 하나였고, band-* 는 `vivaldi` 아래로 재부모 지정 예정이에요. 기록: `docs/sum/session_2026-11-09_lofi-suno-cover-rejection.md`.
