**[English](README.en.md)**

# losik

Logic Pro 를 에이전트가 조작해 곡을 만드는 음악 제작 파이프라인이에요. LLM 작곡 라운드(모델별 스케치)가 표준 MIDI 파일을 만들고, `docs/music/tools/pipeline.py` 가 그 파일을 Logic Pro Creator Studio 에 임포트해 바운스(WAV)까지 자동으로 뽑아요. 결과물은 Suno Cover 로 넘겨 연주·프로덕션을 입혀요.

## 구성

- `docs/music/PROMPT_GUIDELINES.md` — 곡 의뢰 → 작곡 → 검증의 규칙(스펙 템플릿, 작곡 MUST, GM 패치 매핑표, Suno 절차)
- `docs/music/LOGIC_LIBRARY_INVENTORY.md` — Logic 사운드 라이브러리 전체 인벤토리와 악기 호출 경로(A: GM 번호 / B: 라이브러리 패치 / C: Sampler 프리셋)
- `docs/music/FEEDBACK_LOG.md` — 곡·라운드별 청취 판정과 결정 기록
- `docs/music/tools/` — `pipeline.py`(SMF 생성·Logic AX 조작·바운스·세션 간 `LogicLock`), `gm_map.py`·`library_inventory.py`(라이브러리 실측), 세트별 작곡 스크립트(`dh_*`, `lh_*`, `vivaldi_*`)
- `docs/music/sketches/` — 생성된 MIDI, 바운스는 `/Volumes/Netac 2TB/music/bounces/`
- 에이전트 정책과 하네스: `AGENTS.md`, `.omp/`, `docs/harness/`

## 현재 사이클

**Logic 템플릿 프로젝트로 패치·EXS 로드 자동화 (경로 B·C)** — `docs/harness/seed.yaml` (`20261113-220009-a606`)

지금 파이프라인은 GM 프로그램 번호(경로 A)로만 악기를 불러서, 레거시 오케스트라 패치와 Sampler 주법별 프리셋이 지시에 닿지 않아요. 악기를 올려 저장한 템플릿 프로젝트의 복사본에 SMF 를 임포트하고(Logic 은 항상 새 트랙을 만들므로 새 트랙을 템플릿 스트립에 다시 할당) 템플릿 패치 그대로 바운스가 나오게 하는 `produce(template=...)` 경로를 만들었어요.

- [x] AC0 스파이크: 테스트 템플릿 제작과 Logic 임포트 동작 9항목 실측, 판정표로 진행/종료 결정
- [x] AC1 패치·배치 일치: 임포트 후 스트립이 템플릿 스냅샷과 정확히 일치, 트랙별 리전 이름·시작 위치·템포 확인
- [x] AC2 바운스·발음: 길이·마디 1 무음·트랙별 구간 RMS·`SamplerInstrumentsFiles` 확인
- [x] AC3 템플릿 보존: 번들 sha256 트리 해시 전후 동일
- [x] AC4 회귀: 기존 GM 경로와 SMF 바이트 동일성 유지
- [x] AC5 문서: 인벤토리 §4 B·C 행 갱신, 템플릿 체크리스트·호출법
- [x] AC6 실패 경로: `--dry-run` 등록, 실패 4건이 Logic 조작 전에 중단

제약: 템플릿 원본은 Logic 으로 열지 않고 복사본만 쓰며, 템플릿 모드의 SMF 에는 PC·CC0/7/10/32 를 넣지 않아요. 기존 `produce()` 동작과 `build_smf` 출력은 바꾸지 않아요.

## 상태

🚧 개발 중 — 자세한 컨텍스트는 `docs/harness/kickoff-summary.md` 와 `docs/sum/` 세션 기록을 참고하세요.
