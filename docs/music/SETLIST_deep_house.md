# Deep House Set — 2026-10-12

30곡 · 총 **64:18**(v3 WAV 실측) · 116→123→116 BPM · Camelot 인접 키로 이어짐.
브리프: `DEEP_HOUSE_SET_BRIEF.md`. 작곡기: `tools/dh_astra.py`(gpt-6-astra) / `tools/dh_fable.py`(claude-fable-5-1) / `tools/dh_opus.py`(claude-opus-5-5). 바운스: `tools/bounce_dh.py --ver v3` → `/Volumes/Netac 2TB/music/bounces/{sid}-v3.wav` (v1 은 드럼+베이스 뼈대, v2 는 화성층 보정, **v3 가 현재판**: v2 층 + Tough Kit 드럼. Suno 프롬프트는 `SUNO_PROMPTS.md` 의 `## {sid}-v3` 블록).

모든 곡은 64마디(클로저 72마디) DJ 구조(v3): 1–8 인트로(패드+햇 → 5마디 킥) · 9–36 A · 37–40 브레이크 · 41–56 A2(41마디 크래시, 라이드) · 57–64 아웃트로(드럼+베이스). 인트로/아웃트로가 드럼 위주라 **앞 곡 57마디 ↔ 뒷 곡 1마디를 겹쳐** 믹스하면 된다.

## 셋리스트

| # | sid | 모델 | BPM | 키 | 길이 | E | 코드 루프 | 브레이크(37–40, v3) |
|---|---|---|---|---|---|---|---|---|
| 1 | dh01-unlit-threshold | astra | 117 | Am | 2:11 | 1 | Am9 정지 | 서브만 |
| 2 | dh02-ash-corridor | fable | 117 | Am | 2:11 | 1 | Am9 ↔ Bm7♭5/A | 햇만 → 햇+서브 |
| 3 | dh03-cistern-hum | opus | 118 | Em | 2:10 | 1 | Em9 ↔ A9sus4/E | 킥 1박만, 베이스 아웃 |
| 4 | dh04-moss-circuit | astra | 118 | Em | 2:10 | 1–2 | Em9 6 → Em6/9 2 | EP만 |
| 5 | dh05-tin-lantern | fable | 119 | Bm | 2:09 | 2 | Bm9 ↔ Dmaj7♯11/B | 킥+햇+오르간 |
| 6 | dh06-chalk-river | opus | 119 | Bm | 2:09 | 2 | Bm9 ↔ G9 | 드럼만 |
| 7 | dh07-silt-letters | astra | 120 | F♯m | 2:08 | 2 | F♯m9 ↔ Bm11 | 햇·림·서브 |
| 8 | dh08-slate-hallway | fable | 120 | F♯m | 2:08 | 2 | F♯m9 ↔ G♯m11/F♯ | EP만 → 서브만 |
| 9 | dh09-wet-asphalt | opus | 120 | C♯m | 2:08 | 2 | C♯m11 ↔ G♯m7♭5 | 2마디씩 다시 쌓기 |
| 10 | dh10-underpass-velour | astra | 121 | C♯m | 2:06 | 2 | C♯m11 3 → G♯m9 1 | 킥·림·건반 |
| 11 | dh11-cinder-arcade | fable | 121 | G♯m | 2:06 | 2 | G♯m9 3 → Emaj7♯11/G♯ 1 | 하프타임 킥+서브 |
| 12 | dh12-tarnished-blue | opus | 121 | G♯m | 2:06 | 2–3 | G♯m9 ↔ B13 | 2스텝 킥, 패드 진입 |
| 13 | dh13-basalt-current | astra | 122 | E♭m | 2:05 | 3 | E♭m9 ↔ A♭m6 | 홀/짝 마디 교대 |
| 14 | dh14-iron-tide | fable | 122 | E♭m | 2:05 | 3 | E♭m9 ↔ Cm7♭5/E♭ | 위→아래 교대 |
| 15 | dh15-deep-meridian | opus | 122 | B♭m | 2:05 | 3 | B♭m11 ↔ A♭7sus4 | 햇→베이스→킥 3단 빼기 |
| 16 | dh16-blackwater-fold | astra | 123 | B♭m | 2:04 | 3 | B♭m9 ↔ B♭m11 | 킥·건반 → 햇·서브 |
| 17 | dh17-coal-harbour | fable | 123 | Fm | 2:04 | 3 | Fm9 ↔ E♭maj7/F | 서브 드론 |
| 18 | dh18-smoke-orchard | opus | 123 | Fm | 2:04 | 3 | Fm9 ↔ G♭9 | 베이스 아웃 → 오르간만 |
| 19 | dh19-pressure-glass | astra | 122 | Cm | 2:05 | 3 | Cm11 6 → D♭maj7♯11/C 2 | 킥·서브·건반 |
| 20 | dh20-wet-granite | fable | 122 | Cm | 2:05 | 2–3 | Cm9 5 → A♭maj7/C 3 | 림+패드 |
| 21 | dh21-slow-orbit | opus | 121 | Gm | 2:06 | 2 | Gm9 ↔ D♭maj9 | 서브+패드 |
| 22 | dh22-drift-archive | astra | 121 | Gm | 2:06 | 2 | Gm9 ↔ F6/9/G | 건반+패드 |
| 23 | dh23-paper-lantern | fable | 120 | Dm | 2:08 | 2 | Dm9 ↔ Fmaj9/D | 햇+패드 |
| 24 | dh24-umber-lane | opus | 120 | Dm | 2:08 | 2 | Dm11 ↔ Dm11♭5 | 킥+서브 |
| 25 | dh25-dim-stairwell | astra | 119 | Am | 2:09 | 2 | Am9 1 → Dm7/A 3 | 림·서브 |
| 26 | dh26-dusk-ledger | fable | 119 | Am | 2:09 | 1–2 | Am9 6 → C6/9/A 2 | 킥만 |
| 27 | dh27-quiet-pier | opus | 118 | Dm | 2:10 | 1 | Dm9 ↔ Fsus2 | 림+EP |
| 28 | dh28-drowned-linen | astra | 118 | Dm | 2:10 | 1 | Dm11 ↔ Cm9/D | 2마디 무음 → 피아노·서브 |
| 29 | dh29-last-corridor | fable | 117 | Am | 2:11 | 1 | Am11 7 → Em11/A 1 | 햇+림 |
| 30 | dh30-house-lights | opus | 116 | Am | 2:29 | 1 | Am9 ↔ Esus2 | 햇+피아노+패드, 16마디 아웃트로 |

## 흐름

- **1–4 오프닝** (Am→Em, 117–118): 정지 화성·서브 중심. 코드는 암시만.
- **5–12 안착** (Bm→G♯m, 119–121): 2코드 루프가 드러나고 오르간·EP 색이 하나씩 들어옴.
- **13–20 deep 피크** (E♭m→Cm, 122–123): 벨로시티 상한, 햇 밀도 최대. 오픈햇은 & of 2·4(v3).
- **21–26 드리프트** (Gm→Am, 121–119): 패드·화성 비중 ↑, 브레이크가 길어짐.
- **27–30 쿨다운** (Dm→Am, 118–116): 드럼이 하나씩 빠지고 클로저는 킥 하나로 끝남.

## 전환 메모

- 키는 Camelot 8A→9A→10A→11A→12A→1A→2A→3A→4A→5A→6A→7A→8A→7A→8A로 한 칸씩만 움직인다. 같은 키 두 곡(예: 1·2)은 롱 블렌드, 키가 바뀌는 지점(2→3, 4→5 …)은 앞 곡 아웃트로의 코드가 빠진 뒤(57마디 이후) 겹치기.
- 같은 슬롯 쌍 안에서 모델 순서가 astra→fable→opus 로 고정이라, 3곡 단위로 "정지 화성(astra) → 브리지(fable) → 색이 있는 2코드(opus)" 패턴이 반복된다. 단조롭게 들리면 중간 블록(13–20)만 fable↔opus를 바꿔 보는 것이 첫 조정 후보.
- 20→21 은 피크에서 드리프트로 내려오는 유일한 큰 전환. dh20 브레이크(림+패드)에서 dh21 인트로(킥+햇)로 이어 붙이면 에너지가 자연스럽게 빠진다.
- 29→30 은 둘 다 Am·117/116 이라 거의 같은 곡처럼 붙는다. dh30 아웃트로 16마디가 셋 전체의 페이드 역할.

## 모델별 성향 (설계 단계에서 보이는 것 — 청취 전)

| 모델 | 코드 루프 성향 | 브레이크 성향 |
|---|---|---|
| astra | 토닉 페달 위 정지 또는 6:2·3:1 비대칭 길이, 색은 내성 한 음 | 파트를 남기는 쪽(서브만, EP만) |
| fable | 토닉 페달 위 도리안·리디안 차용 화음(m7♭5, maj7♯11), 1:1 교대 | 브레이크를 두 단으로 쪼갬(33–36 / 37–40) |
| opus | 토닉 ↔ 하나의 색 화음(♭VI9, ♭II9, ♭V maj9, sus2), 한 성부만 움직임 | 빼는 순서 자체를 설계(3단 빼기, 다시 쌓기) |

청취 판정은 `FEEDBACK_LOG.md` 에 `## 2026-10-12 청취 판정 — deep house set` 으로 받는다.
