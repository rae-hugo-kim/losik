---
alwaysApply: true
---
# losik 세션 위계 (프로젝트 규칙, 2026-11-09 확정)

저장소 `rae-hugo-kim/losik` 의 워크트리·브랜치·세션은 세 층이에요. 어떤 세션이든 자기 층을 먼저 확인하고 그 층의 규칙만 따라요.

## 층

| 층 | 브랜치 | 워크트리 | 역할 |
|---|---|---|---|
| 0 메인 세션 | `main` | `/Volumes/Netac 2TB/workspace/losik` | 안정판. 하네스 동기화(`harness-check`)는 여기서만 하고 아래로 머지해 내려보내요. 작업 커밋을 직접 받지 않아요. |
| 1 통합 세션 | `issuereport` | `/Users/hugom4/orca/workspaces/losik/chats` | 음악 프로젝트의 **작업 기준선**이에요. 브랜치 세션은 여기서 갈라지고 여기로 PR 을 내요. 머지·충돌 해소·롤아웃 결정은 이 세션이 해요. `main` 과는 `main → issuereport` 머지(하네스 하강)와 `issuereport → main` PR(승격)로만 만나요. |
| 2 브랜치 세션 | `rae-hugo-kim/<topic>` | `/Users/hugom4/orca/workspaces/losik/<topic>` | 한 주제(모델별 작곡 라운드, 집계, 라이브러리 조사 등)만 해요. `orca worktree create --base-branch issuereport` 로 만들고 Orca 부모는 `chats` 예요. 끝나면 `issuereport` 로 PR. |

현재 브랜치 세션: `vivaldi`(PR #2, 열림). 라운드 세션 `band-astra`·`band-fable`·`band-opus` 는 산출물이 `vivaldi` 에 바이트 동일하게 집계돼 **종료 대상**이고, `issue` 워크트리는 `main` 에 전부 포함된 채 2026-09 부터 정지해 **폐기 대상**이에요(제거는 사용자 지시로만).

## 규칙

- **base 와 PR 대상은 항상 `issuereport`** 예요. `main` 을 base 로 브랜치를 만들거나 `main` 으로 PR 을 내지 않아요(하네스 동기화 머지 제외).
- **푸시는 세션별 명시 승인** 이 있어야 해요(`rule://harness-core`). 브랜치 세션은 PR 을 열 때 그 세션에서 승인받아 푸시하고, 통합 세션의 푸시도 매번 승인받아요. 머지는 통합 세션만 해요(`gh pr merge` 포함, 승인 필요).
- 브랜치 세션은 **다른 브랜치·워크트리를 건드리지 않아요**. 공유 자원은 저장소 밖이에요: Logic 단일 인스턴스(`pipeline.LogicLock` 으로 세션 간 직렬화), 바운스 `/Volumes/Netac 2TB/music/bounces/`, Logic 사운드 라이브러리(Netac). 바운스 결과 파일은 `BOUNCE_SEARCH` 가 형제 워크트리의 `sketches/` 까지 봐요.
- **인계는 복사로**: `docs/sum/` 은 untracked 라 브랜치를 타지 않아요. 세션을 넘길 때 인계 sum 을 새 워크트리 `docs/sum/` 에 복사하고 루트에 `<TOPIC>_KICKOFF.md`(미커밋) 를 둬요.
- 하네스 버전은 `main` 이 기준이에요. 브랜치 세션에서 하네스 동기화를 다시 하지 않아요 — 뒤처졌으면 `git merge main`(승인) 으로 받아요.
- 브랜치 세션의 결정이 프로세스 전체에 닿으면(규칙 문서·GM 매핑표·파이프라인) PR 본문에 그 사실을 적고, 통합 세션이 머지 뒤 `.omp/rules/` 또는 `docs/music/PROMPT_GUIDELINES.md` 로 승격해요.

## 지금 상태의 출처

실측 2026-11-09: `main 64aca55` 는 `issuereport` 의 순수 조상(main 전용 커밋 0), `issuereport` 는 main 대비 +51, band-* 는 issuereport 대비 +1~+10 / −14, `vivaldi` 는 +19 / −10, `issue` 는 main 대비 −5 / +0. Orca 부모가 있는 워크트리는 `vivaldi`(부모 `chats`) 하나예요. 기록: `docs/sum/session_2026-11-09_lofi-suno-cover-rejection.md`.
