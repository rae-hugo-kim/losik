# Vivaldi 사계 변주 — 집계 (v1 2026-11-05 · v2 2026-11-10)

v2(장르 자유, `VIVALDI_BRIEF_V2.md`) 36곡은 아래 `## v2 — 2026-11-10 집계` 절에 있습니다. 그 위는 v1(deep house·lo-fi 전제) 집계입니다.

## v1 — 2026-11-05 집계

12악장 × 3모델 = **36곡**이고, 총 길이는 **111:48**(WAV 실측), 곡당 2:52~3:19 입니다. 세 브랜치(`rae-hugo-kim/band-{astra,fable,opus}`)의 결과를 `rae-hugo-kim/vivaldi` 에 모은 표입니다.
브리프는 `VIVALDI_BRIEF.md` 입니다. 소스 데이터 `tools/vivaldi_data.py` 는 Mutopia Project 출처로 CC BY-SA 3.0 을 전제합니다(작품은 퍼블릭 도메인). MIDI 안의 출처 표기는 astra·opus 24개에만 있고 **fable 12개에는 없습니다**(`vivaldi_fable.py` 가 `build_smf` 에 섹션 마커만 넘깁니다). 공개 전에 fable MIDI 에 표기를 넣어야 합니다. 바운스는 `/Volumes/Netac 2TB/music/bounces/{sid}-v1.wav` 이고(Logic 바운스), 36개 모두 있는 것을 확인했습니다.

| 모델 | 모델 ID | 작곡기 | Suno 블록 | 기록 |
|---|---|---|---|---|
| astra | `openai-codex/gpt-6-astra` | `tools/vivaldi_astra.py` (`--check` 결정성; `--verify-audio` 는 band-astra 의 `render_tide_variants.py` 를 import 하므로 이 브랜치에서는 실행되지 않습니다. 측정 결과 `vivaldi_astra_audio.json`, 바운스 로그 `vivaldi_astra_bounce.jsonl`) | `suno/vivaldi_astra.md` | `FEEDBACK_LOG.md` `## 2026-10-30 Vivaldi 사계 변주 — astra`, `docs/sum/session_2026-10-30_vivaldi-astra.md` |
| fable | `anthropic/claude-fable-5-1` | `tools/vivaldi_fable.py` (`--prompts` 블록 길이) | `suno/vivaldi_fable.md` | `FEEDBACK_LOG.md` `## 2026-10-21 Vivaldi 사계 변주 — fable`, `docs/sum/session_2026-10-27_vivaldi-fable.md` |
| opus | `anthropic/claude-opus-5-5` | `tools/vivaldi_opus.py` (`--bounce` 바운스) | `suno/vivaldi_opus.md` | `FEEDBACK_LOG.md` `## 2026-10-21 Vivaldi 사계 변주 — opus`, `docs/sum/session_2026-10-27_vivaldi-opus.md` |

곡별 주제 창·리듬 변형·주제 비율은 각 모델의 FEEDBACK_LOG 절 표가 원천입니다.

## 측정 정의

`sketches/{sid}-v1.mid` 를 직접 파싱한 값입니다(2026-11-05).
- **마디**: `END` 마커 위치입니다. 박자는 36곡 모두 4/4 이고 템포 변화는 없습니다.
- **본문**: `intro`·`break`·`outro` 를 뺀 마커 구간입니다. fable·opus 는 `A`·`A2`, astra 는 `theme`·`answer`·`reprise`·`answer2` 입니다.
- **음/마디**: 모든 트랙(드럼 포함)의 노트온 수 ÷ 마디 수이고, "전체 / 본문" 순으로 적었습니다. lo-fi v2 의 `A·A2 ≥ 45음/마디` 와 같은 정의입니다.
- **베이스 음/마디**: `Bass` 트랙만 센 값이고, "전체 / 본문" 순입니다.
- **트랙 PC**: 트랙 이름 뒤 숫자가 GM 프로그램 번호입니다(Drums 는 킷 번호). 트랙은 있지만 노트가 하나도 없으면 `(음표 0)` 으로 표시했습니다(astra lo-fi 5곡의 Pad).
- **길이**: WAV `data` 청크 길이(리미터 후처리 포함)를 초 단위로 반올림했습니다. fable·opus 의 FEEDBACK_LOG 표는 내림이라 1초씩 다른 곡이 있습니다. 총 길이와 모델별 12곡 길이는 반올림 전 초를 더한 값이라 표의 곡별 길이를 더한 값과 몇 초 다를 수 있습니다.
- **본문 Keys 음/마디**(모델별 요약): `Keys` 트랙만 본문 마디에서 센 노트온 수 ÷ 본문 마디 수입니다.
- 36곡 모두 CC 는 CC64(서스테인)뿐이고 CC1·CC7·CC11 은 없습니다.

## 셋리스트

| 악장 | 모델 | sid | 장르 | 키 | BPM | 마디 | 길이 | 트랙 PC | 음/마디 (전체 / 본문) | 베이스 음/마디 (전체 / 본문) | Suno 블록 | 업로드 | 청취 판정 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Spring I | astra | `vs-spring1-astra` | lo-fi | E | 84 | 64 | 3:03 | Drums 0, Bass 33, Keys 4, Pad 89 (음표 0), Theme 4, Reprise 24 | 22.6 / 28.1 | 1.0 / 1.5 | `suno/vivaldi_astra.md:26` | 미업로드 | 미청취 |
|  | fable | `vs-spring1-fable` | deep house | E | 122 | 96 | 3:09 | Drums 16, Bass 38, Keys 4, Pad 89, Tex 4, Theme 4, Theme2 80 | 34.6 / 40.9 | 1.8 / 2.0 | `suno/vivaldi_fable.md:22` | 미업로드 | 세트 판정만 (아래 §청취) |
|  | opus | `vs-spring1-opus` | deep house | C♯m | 122 | 96 | 3:09 | Drums 16, Bass 38, Keys 4, Pad 89, Tex 16, ThemeA 0, ThemeB 80 | 29.2 / 33.5 | 3.3 / 4.0 | `suno/vivaldi_opus.md:5` | 미업로드 | 세트 판정만 (아래 §청취) |
| Spring II | astra | `vs-spring2-astra` | lo-fi | C♯m | 74 | 56 | 3:02 | Drums 0, Bass 33, Keys 4, Pad 89, Theme 24, Reprise 4 | 16.1 / 21.6 | 1.0 / 1.4 | `suno/vivaldi_astra.md:35` | 미업로드 | 미청취 |
|  | fable | `vs-spring2-fable` | lo-fi | C♯m | 70 | 56 | 3:12 | Drums 0, Bass 33, Keys 0, Tex 16, Theme 4, Theme2 24 | 23.0 / 28.8 | 1.3 / 1.9 | `suno/vivaldi_fable.md:31` | 미업로드 | 세트 판정만 (아래 §청취) |
|  | opus | `vs-spring2-opus` | lo-fi | C♯m | 78 | 56 | 2:52 | Drums 0, Bass 33, Keys 0, Tex 16, ThemeA 24, ThemeB 4 | 17.8 / 21.2 | 0.9 / 1.2 | `suno/vivaldi_opus.md:14` | 미업로드 | 세트 판정만 (아래 §청취) |
| Spring III | astra | `vs-spring3-astra` | deep house | E | 122 | 96 | 3:09 | Drums 16, Bass 38, Keys 4, Pad 89, Theme 0, Reprise 4 | 25.6 / 29.9 | 0.9 / 1.0 | `suno/vivaldi_astra.md:44` | 미업로드 | 미청취 |
|  | fable | `vs-spring3-fable` | deep house | E | 124 | 96 | 3:06 | Drums 16, Bass 38, Keys 4, Pad 90, Tex 16, Theme 81, Theme2 4 | 29.4 / 34.6 | 2.6 / 3.0 | `suno/vivaldi_fable.md:40` | 미업로드 | 세트 판정만 (아래 §청취) |
|  | opus | `vs-spring3-opus` | deep house | E | 120 | 96 | 3:12 | Drums 16, Bass 38, Keys 16, Pad 90, Tex 4, ThemeA 24, ThemeB 0 | 33.6 / 38.7 | 2.5 / 3.0 | `suno/vivaldi_opus.md:23` | 미업로드 | 세트 판정만 (아래 §청취) |
| Summer I | astra | `vs-summer1-astra` | lo-fi | Gm | 88 | 64 | 2:55 | Drums 0, Bass 33, Keys 4, Pad 89 (음표 0), Theme 4, Reprise 0 | 21.7 / 26.7 | 1.0 / 1.5 | `suno/vivaldi_astra.md:53` | 미업로드 | 미청취 |
|  | fable | `vs-summer1-fable` | lo-fi | Gm | 88 | 64 | 2:55 | Drums 0, Bass 33, Keys 4, Tex 16, Theme 24, Theme2 0 | 31.1 / 35.3 | 2.0 / 2.5 | `suno/vivaldi_fable.md:49` | 미업로드 | 세트 판정만 (아래 §청취) |
|  | opus | `vs-summer1-opus` | lo-fi | Gm | 80 | 64 | 3:12 | Drums 0, Bass 33, Keys 4, Tex 27, ThemeA 0, ThemeB 81 | 19.3 / 23.5 | 1.2 / 1.5 | `suno/vivaldi_opus.md:32` | 미업로드 | 세트 판정만 (아래 §청취) |
| Summer II | astra | `vs-summer2-astra` | lo-fi | Gm | 76 | 56 | 2:57 | Drums 0, Bass 33, Keys 4, Pad 89 (음표 0), Theme 0, Reprise 24 | 20.3 / 25.4 | 1.0 / 1.5 | `suno/vivaldi_astra.md:62` | 미업로드 | 미청취 |
|  | fable | `vs-summer2-fable` | lo-fi | Gm | 70 | 56 | 3:12 | Drums 0, Bass 33, Keys 4, Tex 24, Theme 0, Theme2 4 | 27.5 / 34.1 | 1.6 / 1.9 | `suno/vivaldi_fable.md:58` | 미업로드 | 세트 판정만 (아래 §청취) |
|  | opus | `vs-summer2-opus` | lo-fi | Am | 72 | 56 | 3:07 | Drums 0, Bass 33, Keys 0, Tex 16, ThemeA 4, ThemeB 24, Pad 89 | 18.6 / 23.2 | 0.8 / 1.2 | `suno/vivaldi_opus.md:41` | 미업로드 | 세트 판정만 (아래 §청취) |
| Summer III | astra | `vs-summer3-astra` | deep house | Gm | 124 | 96 | 3:06 | Drums 16, Bass 38, Keys 4, Pad 89, Theme 80, Reprise 4 | 25.9 / 30.5 | 0.8 / 1.0 | `suno/vivaldi_astra.md:71` | 미업로드 | 미청취 |
|  | fable | `vs-summer3-fable` | deep house | Gm | 124 | 96 | 3:06 | Drums 16, Bass 38, Keys 4, Pad 89, Tex 4, Theme 4, Theme2 80 | 35.9 / 41.2 | 2.5 / 3.0 | `suno/vivaldi_fable.md:67` | 미업로드 | 세트 판정만 (아래 §청취) |
|  | opus | `vs-summer3-opus` | deep house | Gm | 124 | 96 | 3:06 | Drums 16, Bass 38, Keys 4, Pad 89, Tex 16, ThemeA 81, ThemeB 0 | 35.7 / 41.2 | 2.8 / 3.0 | `suno/vivaldi_opus.md:50` | 미업로드 | 세트 판정만 (아래 §청취) |
| Autumn I | astra | `vs-autumn1-astra` | lo-fi | F | 86 | 64 | 2:59 | Drums 0, Bass 33, Keys 4, Pad 89 (음표 0), Theme 24, Reprise 0 | 25.2 / 31.8 | 1.2 / 1.5 | `suno/vivaldi_astra.md:80` | 미업로드 | 미청취 |
|  | fable | `vs-autumn1-fable` | lo-fi | F | 84 | 64 | 3:03 | Drums 0, Bass 38, Keys 0, Tex 24, Theme 4, Theme2 24 | 39.4 / 47.3 | 1.7 / 2.5 | `suno/vivaldi_fable.md:76` | 미업로드 | 세트 판정만 (아래 §청취) |
|  | opus | `vs-autumn1-opus` | deep house | Dm | 118 | 96 | 3:15 | Drums 16, Bass 38, Keys 0, Pad 89, Tex 4, ThemeA 24, ThemeB 80 | 30.1 / 34.7 | 1.7 / 2.0 | `suno/vivaldi_opus.md:59` | 미업로드 | 세트 판정만 (아래 §청취) |
| Autumn II | astra | `vs-autumn2-astra` | lo-fi | Dm | 72 | 56 | 3:07 | Drums 0, Bass 33, Keys 4, Pad 89, Theme 4, Reprise 0 | 18.7 / 24.2 | 1.0 / 1.5 | `suno/vivaldi_astra.md:89` | 미업로드 | 미청취 |
|  | fable | `vs-autumn2-fable` | lo-fi | Dm | 72 | 56 | 3:07 | Drums 0, Bass 33, Keys 4, Tex 16, Theme 24, Theme2 4 | 20.3 / 23.5 | 1.6 / 2.0 | `suno/vivaldi_fable.md:85` | 미업로드 | 세트 판정만 (아래 §청취) |
|  | opus | `vs-autumn2-opus` | lo-fi | Dm | 84 | 64 | 3:03 | Drums 0, Bass 33, Keys 4, Tex 27, ThemeA 0, ThemeB 80, Pad 89 | 19.6 / 23.9 | 0.9 / 1.2 | `suno/vivaldi_opus.md:68` | 미업로드 | 세트 판정만 (아래 §청취) |
| Autumn III | astra | `vs-autumn3-astra` | deep house | F | 116 | 96 | 3:19 | Drums 16, Bass 38, Keys 4, Pad 89, Theme 27, Reprise 4 | 25.9 / 29.5 | 0.8 / 1.0 | `suno/vivaldi_astra.md:98` | 미업로드 | 미청취 |
|  | fable | `vs-autumn3-fable` | deep house | F | 122 | 96 | 3:09 | Drums 16, Bass 38, Keys 4, Pad 89, Tex 16, Theme 80, Theme2 4 | 32.8 / 38.6 | 2.6 / 3.0 | `suno/vivaldi_fable.md:94` | 미업로드 | 세트 판정만 (아래 §청취) |
|  | opus | `vs-autumn3-opus` | deep house | F | 122 | 96 | 3:09 | Drums 16, Bass 38, Keys 4, Pad 90, Tex 16, ThemeA 0, ThemeB 80 | 35.2 / 40.2 | 3.3 / 4.0 | `suno/vivaldi_opus.md:77` | 미업로드 | 세트 판정만 (아래 §청취) |
| Winter I | astra | `vs-winter1-astra` | deep house | Fm | 118 | 96 | 3:15 | Drums 16, Bass 38, Keys 4, Pad 89, Theme 4, Reprise 80 | 26.9 / 30.9 | 0.8 / 1.0 | `suno/vivaldi_astra.md:107` | 미업로드 | 미청취 |
|  | fable | `vs-winter1-fable` | deep house | Fm | 118 | 96 | 3:15 | Drums 16, Bass 38, Keys 4, Pad 89, Tex 16, Theme 4, Theme2 81 | 36.0 / 43.3 | 1.8 / 2.0 | `suno/vivaldi_fable.md:103` | 미업로드 | 세트 판정만 (아래 §청취) |
|  | opus | `vs-winter1-opus` | deep house | Fm | 122 | 96 | 3:09 | Drums 16, Bass 38, Keys 16, Pad 89, Tex 4, ThemeA 0, ThemeB 81 | 29.3 / 33.4 | 1.8 / 2.0 | `suno/vivaldi_opus.md:86` | 미업로드 | 세트 판정만 (아래 §청취) |
| Winter II | astra | `vs-winter2-astra` | lo-fi | E♭ | 78 | 56 | 2:52 | Drums 0, Bass 33, Keys 4, Pad 89 (음표 0), Theme 24, Reprise 4 | 21.9 / 28.0 | 1.0 / 1.5 | `suno/vivaldi_astra.md:116` | 미업로드 | 미청취 |
|  | fable | `vs-winter2-fable` | lo-fi | E♭ | 68 | 56 | 3:18 | Drums 0, Bass 33, Keys 0, Tex 24, Theme 4, Theme2 0 | 32.8 / 41.4 | 1.6 / 2.0 | `suno/vivaldi_fable.md:112` | 미업로드 | 세트 판정만 (아래 §청취) |
|  | opus | `vs-winter2-opus` | lo-fi | E♭ | 76 | 56 | 2:57 | Drums 0, Bass 33, Keys 4, Tex 24, ThemeA 0, ThemeB 80 | 19.6 / 24.5 | 0.8 / 1.2 | `suno/vivaldi_opus.md:95` | 미업로드 | 세트 판정만 (아래 §청취) |
| Winter III | astra | `vs-winter3-astra` | deep house | Fm | 120 | 96 | 3:12 | Drums 16, Bass 38, Keys 4, Pad 89, Theme 0, Reprise 24 | 26.2 / 30.8 | 0.9 / 1.0 | `suno/vivaldi_astra.md:125` | 미업로드 | 미청취 |
|  | fable | `vs-winter3-fable` | deep house | Fm | 124 | 96 | 3:06 | Drums 16, Bass 38, Keys 4, Pad 90, Tex 4, Theme 81, Theme2 4 | 30.4 / 36.0 | 0.9 / 1.0 | `suno/vivaldi_fable.md:121` | 미업로드 | 세트 판정만 (아래 §청취) |
|  | opus | `vs-winter3-opus` | deep house | Em | 123 | 96 | 3:07 | Drums 16, Bass 38, Keys 4, Pad 90, Tex 16, ThemeA 0, ThemeB 81 | 27.6 / 31.8 | 2.5 / 3.0 | `suno/vivaldi_opus.md:104` | 미업로드 | 세트 판정만 (아래 §청취) |

## 모델별 요약

| 모델 | deep house / lo-fi | 본문 음/마디 | 본문 베이스 음/마디 | 본문 Keys 음/마디 | 12곡 길이 |
|---|---|---|---|---|---|
| astra | 5 / 7 | 21.6–31.8 (평균 28.1) | 1.0–1.5 (평균 1.3) | 4.0–11.9 (평균 8.0) | 36:54 |
| fable | 6 / 6 | 23.5–47.3 (평균 37.1) | 1.0–3.0 (평균 2.2) | 3.9–15.9 (평균 8.3) | 37:36 |
| opus | 7 / 5 | 21.2–41.2 (평균 30.8) | 1.2–4.0 (평균 2.3) | 4.0–12.0 (평균 6.8) | 37:18 |

본문 45음/마디(lo-fi v2 목표)를 넘는 곡은 `vs-autumn1-fable`(47.3) 하나입니다. 본문 베이스는 36곡 모두 4음/마디 이하이고(최대 `vs-spring1-opus`·`vs-autumn3-opus` 4.0), astra 는 12곡 모두 1.0~1.5 입니다.

## 청취

- **세트 판정 (fable·opus 24곡, Logic 바운스 기준)**: "디테일 부족, 빈 공간 많음". 출처는 `docs/sum/session_2026-11-05_lofi-v2-vivaldi-handoff.md` §사계 인계(추적되지 않는 파일)이고, FEEDBACK_LOG 에는 아직 기록되지 않았습니다. 곡별 판정은 아직 없습니다. lo-fi v1 에서 같은 판정을 받은 뒤 만든 v2 레시피(밀도·다운비트 앵커·베이스 CC7)는 `LOFI_HIPHOP_SET_BRIEF.md` `## v2 보정` 에 있습니다.
- **astra 12곡**: 미청취입니다.
- 곡별 판정을 받으면 위 표의 `청취 판정` 칸에 적고, `FEEDBACK_LOG.md` 에 `## 청취 판정 — Vivaldi 사계 변주` 절을 새로 만들어 세트 판정과 함께 기록합니다.
- **업로드**: 36곡 모두 Suno Cover 미업로드입니다(세 절의 `업로드 결과` 칸 기준). 통과·차단 결과는 `VIVALDI_BRIEF.md` §2-6 대로 기록합니다.

## v2 — 2026-11-10 집계 (장르 자유)

12악장 × 3모델 = **36곡**, 총 길이 **107:44**(WAV 실측; astra 35:32 · fable 36:09 · opus 36:03), 곡당 2:50~3:08 입니다. 라운드 세션 `band-{astra,fable,opus}` 의 v2 결과를 `rae-hugo-kim/vivaldi` 에 머지해 모았습니다(머지 커밋 `a6635e9`·`846eceb`·`8bce7a3`). 브리프는 `VIVALDI_BRIEF_V2.md` 입니다. 바운스는 `/Volumes/Netac 2TB/music/bounces/{sid}-v2.wav` 이고 36개 모두 있습니다.

| 모델 | 모델 ID | 작곡기 | Suno 블록 | 기록 |
|---|---|---|---|---|
| astra | `openai-codex/gpt-6-astra` | `tools/vivaldi_astra_v2.py` (`--check` 12/12 MATCH; 오디오 검증기 `vivaldi_astra_v2_audio.py`, 메타·해시 `vivaldi_astra_v2_midi.json`) | `suno/vivaldi_astra_v2.md` | `FEEDBACK_LOG.md` `## 2026-11-09 Vivaldi 사계 변주 v2 — astra`, 계획 `vivaldi_astra_v2_plan.md` |
| fable | `anthropic/claude-fable-5-1` | `tools/vivaldi_fable_v2.py` (`--check` 12/12 OK; 러너 `bounce_vivaldi_fable_v2.py`) | `suno/vivaldi_fable_v2.md` | `FEEDBACK_LOG.md` `## 2026-11-09 Vivaldi 사계 변주 v2 — fable`, 계획 `vivaldi_fable_v2_plan.md` |
| opus | `anthropic/claude-opus-5-5` | `tools/vivaldi_opus_v2.py` (`--check` identical 12/12, `--bounce`) | `suno/vivaldi_opus_v2.md` | `FEEDBACK_LOG.md` `## 2026-11-10 Vivaldi 사계 변주 v2 — opus`, 계획 `vivaldi_opus_v2_plan.md` |

- **장르 분포**: 36곡에 겹치는 장르가 거의 없습니다. 세 모델이 같은 악장에 비슷한 장르를 고른 곳은 Spring I(baroque chamber pop / chamber pop / Afro highlife), Spring III(Celtic jig / tarantella / Celtic slip jig), Summer I(desert trip-hop / roots reggae / trip-hop), Winter III(minimalist chamber / tango nuevo / tango nuevo) 정도입니다. 모델별 12장르는 각 FEEDBACK_LOG 절의 표에 이유와 함께 있습니다.
- **편성**: 경로 B·C(라이브러리 패치·EXS, `produce(patches=...)`)를 쓴 트랙은 astra 21 · fable 22 · opus 17 개입니다. 표의 `편성` 열에서 `→` 뒤가 올라간 패치(괄호는 `(바탕 패치, EXS)`)입니다. 길이는 WAV `data` 청크 기준 반올림입니다.
- **파이프라인에서 라운드가 찾은 결함 2건**(`LOGIC_LIBRARY_INVENTORY.md` §4.1 에 반영): 지휘 트랙의 저작권 메타가 빈 트랙을 만들어 패치 번호가 밀림(fable·astra), 패치 로드 뒤 선택 트랙의 리전 끝이 바운스 범위가 되어 곡이 잘림(fable 7곡 재바운스). 집계 시점의 36곡은 모두 기대 길이와 일치합니다(각 모델 FEEDBACK_LOG 표).

### v2 셋리스트

| 악장 | 모델 | sid | 장르 | 박자 | BPM | 마디 | 길이 | 편성 (트랙 PC → 패치/EXS) | Suno 블록 | 업로드 | 청취 판정 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Spring I | astra | `vs-spring1-astra` | baroque chamber pop | 4/4 | 88 | 64 | 2:55 | Rhythm 0, Bass 43, Harmony 0 → Harpsichord, Lead 0 → Oboe, Texture 0 → (Violins 1, Violins 1 Pizzicato) | `suno/vivaldi_astra_v2.md:34` | 미업로드 | 미청취 |
|  | fable | `vs-spring1-fable` | chamber pop (60s baroque pop) | 4/4 | 96 | 72 | 3:00 | Drums 0, Bass 33, Harpsichord 6 → Harpsichord, Strings 48, Theme 56, Theme2 6 → Harpsichord | `suno/vivaldi_fable_v2.md:22` | 미업로드 | 미청취 |
|  | opus | `vs-spring1-opus` | Afro highlife | 4/4 | 134 | 100 | 2:59 | Drums 0, Bass 33, Rhythm Guitar 25, Organ 16, Theme Guitar 24, Horns 61 | `suno/vivaldi_opus_v2.md:5` | 미업로드 | 미청취 |
| Spring II | astra | `vs-spring2-astra` | impressionist chamber nocturne | 3/4 | 66 | 64 | 2:55 | Bass 42, Harmony 2, Lead 0 → English Horn, Texture 0 → Harp | `suno/vivaldi_astra_v2.md:43` | 미업로드 | 미청취 |
|  | fable | `vs-spring2-fable` | celtic air (harp, tin whistle) | 3/4 | 84 | 84 | 3:00 | Harp 46 → Celtic Harp, Cellos 42, Theme 73 → Celtic Tin Whistle, Theme2 24, Strings 48 | `suno/vivaldi_fable_v2.md:31` | 미업로드 | 미청취 |
|  | opus | `vs-spring2-opus` | Bossa nova | 4/4 | 80 | 60 | 3:00 | Drums 0, Bass 32, Guitar 24, Strings 48, EP 4, Flute 73 → Flute Solo | `suno/vivaldi_opus_v2.md:14` | 미업로드 | 미청취 |
| Spring III | astra | `vs-spring3-astra` | Celtic folk jig | 6/8 | 96 | 96 | 3:00 | Rhythm 26, Bass 32, Harmony 25, Lead 0 → Celtic Tin Whistle, Texture 0 → Celtic Harp | `suno/vivaldi_astra_v2.md:52` | 미업로드 | 미청취 |
|  | fable | `vs-spring3-fable` | tarantella (Italian folk 6/8) | 6/8 | 168 | 168 | 3:00 | Perc 40, Bass 32, Strum 24, Lute 24 → Medieval Lute, Theme 71 → Clarinet Solo, Theme2 24 | `suno/vivaldi_fable_v2.md:40` | 미업로드 | 미청취 |
|  | opus | `vs-spring3-opus` | Celtic slip jig | 9/8 | 174 | 116 | 3:00 | Bass 32, Percussion 0, Bouzouki 25 → Irish Bouzouki, Harp 24 → Celtic Harp, Whistle 73 → Celtic Tin Whistle | `suno/vivaldi_opus_v2.md:23` | 미업로드 | 미청취 |
| Summer I | astra | `vs-summer1-astra` | desert trip-hop | 4/4 | 62 | 48 | 3:06 | Rhythm 24, Bass 39, Harmony 7, Lead 0 → Turkish Oud Lute, Texture 107 | `suno/vivaldi_astra_v2.md:61` | 미업로드 | 미청취 |
|  | fable | `vs-summer1-fable` | roots reggae / dub | 4/4 | 62 | 48 | 3:06 | Drums 26, Bass 33, Organ 16, Skank 25, Theme 109, Theme2 16 | `suno/vivaldi_fable_v2.md:49` | 미업로드 | 미청취 |
|  | opus | `vs-summer1-opus` | Trip-hop | 4/4 | 84 | 64 | 3:03 | Drums 0, Sub Bass 39, Piano 3, Strings 49, Vibes 11, Oboe 68 → Oboe | `suno/vivaldi_opus_v2.md:32` | 미업로드 | 미청취 |
| Summer II | astra | `vs-summer2-astra` | chamber suspense score | 5/4 | 80 | 48 | 3:00 | Pulse 0 → Timpani, Bass 42, Harmony 12, Lead 0 → Bassoon Solo, Texture 0 → (Violins 1, Violins 1 Tremolo) | `suno/vivaldi_astra_v2.md:70` | 미업로드 | 미청취 |
|  | fable | `vs-summer2-fable` | neoclassical ambient | 4/4 | 56 | 44 | 3:09 | Strings 48 → (Full Strings, Full Strings Legato), Harp 46 → Harp, Timpani 47 → (Timpani, Timpani Tremolo), Theme 40 → (Violins 1, Violin (Arco)), Theme2 46 → Harp | `suno/vivaldi_fable_v2.md:58` | 미업로드 | 미청취 |
|  | opus | `vs-summer2-opus` | Cinematic neo-classical | 4/4 | 63 | 48 | 3:03 | Piano 2, Strings 48, Cellos 42, Timpani 47 → Timpani, Solo Violin 40 → (Violins 1, Violin (Arco)) | `suno/vivaldi_opus_v2.md:41` | 미업로드 | 미청취 |
| Summer III | astra | `vs-summer3-astra` | progressive rock | 7/8 | 126 | 112 | 3:07 | Rhythm 8, Bass 34, Harmony 18, Lead 30, Texture 48 | `suno/vivaldi_astra_v2.md:79` | 미업로드 | 미청취 |
|  | fable | `vs-summer3-fable` | drum and bass | 4/4 | 174 | 128 | 2:57 | Drums 25, Sub 38, Pad 90, Riser 101, Theme 81, Theme2 80 | `suno/vivaldi_fable_v2.md:67` | 미업로드 | 미청취 |
|  | opus | `vs-summer3-opus` | Symphonic metal | 4/4 | 180 | 136 | 3:01 | Drums 8, Bass 34, Rhythm Guitar 30, Lead Guitar 26, Strings 49, Synth Lead 81, Choir 52 → Mixed Choir | `suno/vivaldi_opus_v2.md:50` | 미업로드 | 미청취 |
| Autumn I | astra | `vs-autumn1-astra` | New Orleans second-line jazz | 4/4 | 100 | 72 | 2:53 | Rhythm 0, Bass 32, Harmony 1, Lead 0 → Clarinet Solo, Texture 57 | `suno/vivaldi_astra_v2.md:88` | 미업로드 | 미청취 |
|  | fable | `vs-autumn1-fable` | polka (harvest dance) | 2/4 | 100 | 144 | 2:53 | Drums 0, Tuba 58 → Tuba, Accordion 21 → Polka Accordion, Theme 56, Theme2 65 | `suno/vivaldi_fable_v2.md:76` | 미업로드 | 미청취 |
|  | opus | `vs-autumn1-opus` | Balkan brass | 7/8 | 140 | 120 | 3:00 | Drums 0, Trumpet 56, Alto Sax 65, Accordion 21 → Polka Accordion, Tuba 58 → Tuba | `suno/vivaldi_opus_v2.md:59` | 미업로드 | 미청취 |
| Autumn II | astra | `vs-autumn2-astra` | chamber passacaglia | 3/4 | 64 | 64 | 3:00 | Bass 42, Harmony 0 → Harpsichord, Lead 0 → (Violins 1, Violin (Arco)), Texture 0 → Bassoon Solo | `suno/vivaldi_astra_v2.md:97` | 미업로드 | 미청취 |
|  | fable | `vs-autumn2-fable` | sacred minimal drone (choir, pipe organ) | 3/4 | 40 | 40 | 3:00 | Choir 52 → Church Choir, Organ 20 → (Celesta, Principal + Mixture), Theme 69 → English Horn, Theme2 52 → Church Choir, Bells 14 | `suno/vivaldi_fable_v2.md:85` | 미업로드 | 미청취 |
|  | opus | `vs-autumn2-opus` | Cool jazz ballad | 4/4 | 88 | 64 | 2:55 | Drums 0, Bass 32, Piano 0, Vibes 11, Tenor Sax 66 → Studio Tenor Sax 1 | `suno/vivaldi_opus_v2.md:68` | 미업로드 | 미청취 |
| Autumn III | astra | `vs-autumn3-astra` | cinematic hunting scherzo | 6/8 | 100 | 96 | 2:53 | Pulse 0 → Timpani, Bass 43, Harmony 0 → (Violins 1, Violins 1 Staccato), Lead 0 → French Horn Solo, Texture 48 | `suno/vivaldi_astra_v2.md:106` | 미업로드 | 미청취 |
|  | fable | `vs-autumn3-fable` | New Orleans brass band (second line) | 4/4 | 96 | 72 | 3:00 | Drums 0, Tuba 58 → Tuba, Trombone 57, Sax 65, Theme 56, Theme2 57 | `suno/vivaldi_fable_v2.md:94` | 미업로드 | 미청취 |
|  | opus | `vs-autumn3-opus` | Spaghetti western | 4/4 | 112 | 84 | 3:00 | Drums 0, Bass 32, Guitar 24, Strings 48, Trumpet 56, Timpani 47 → Timpani, Horns 60 → French Horns | `suno/vivaldi_opus_v2.md:77` | 미업로드 | 미청취 |
| Winter I | astra | `vs-winter1-astra` | industrial breakbeat | 4/4 | 112 | 80 | 2:51 | Rhythm 16, Bass 39, Harmony 8, Lead 82, Texture 98 | `suno/vivaldi_astra_v2.md:115` | 미업로드 | 미청취 |
|  | fable | `vs-winter1-fable` | tango nuevo | 4/4 | 118 | 88 | 2:59 | Piano 0, Bass 32, Accordion 21 → Tango Accordion, Theme 40 → (Violins 1, Violin (Arco)), Theme2 21 → Tango Accordion | `suno/vivaldi_fable_v2.md:103` | 미업로드 | 미청취 |
|  | opus | `vs-winter1-opus` | Dark techno | 4/4 | 128 | 96 | 3:00 | Drums 25, Pulse Bass 38, Pad 94, Chords 90, Lead 80, Celesta 8 → Celesta | `suno/vivaldi_opus_v2.md:86` | 미업로드 | 미청취 |
| Winter II | astra | `vs-winter2-astra` | acoustic bossa nova | 4/4 | 90 | 64 | 2:51 | Rhythm 40, Bass 32, Harmony 24, Lead 0 → Flute Solo, Texture 11 | `suno/vivaldi_astra_v2.md:124` | 미업로드 | 미청취 |
|  | fable | `vs-winter2-fable` | bossa nova | 4/4 | 72 | 56 | 3:07 | Drums 0, Bass 32, Guitar 24, Vibes 11, Theme 73 → Flute Solo, Theme2 11 | `suno/vivaldi_fable_v2.md:112` | 미업로드 | 미청취 |
|  | opus | `vs-winter2-opus` | Neo-soul | 4/4 | 72 | 54 | 3:00 | Drums 0, Bass 33, Rhodes 4, Alto Sax 65, Piano 0, Pizzicato 45 → (Violins 1, Violin (Pizzicato)) | `suno/vivaldi_opus_v2.md:95` | 미업로드 | 미청취 |
| Winter III | astra | `vs-winter3-astra` | contemporary minimalist chamber | 5/8 | 92 | 112 | 3:03 | Bass 42, Harmony 12, Lead 0 → (Violins 1, Violin (Pizzicato)), Texture 0 → Harp | `suno/vivaldi_astra_v2.md:133` | 미업로드 | 미청취 |
|  | fable | `vs-winter3-fable` | synthwave | 4/4 | 118 | 88 | 2:59 | Drums 25, Bass 38, Arp 80, Pad 94, Theme 81, Theme2 80 | `suno/vivaldi_fable_v2.md:121` | 미업로드 | 미청취 |
|  | opus | `vs-winter3-opus` | Tango nuevo | 4/4 | 116 | 88 | 3:02 | Piano 0, Bass 43, Strings 48, Accordion 21 → Polka Accordion, Solo Violin 40 → (Violins 1, Violin (Arco)) | `suno/vivaldi_opus_v2.md:104` | 미업로드 | 미청취 |

### v2 청취·업로드

- 36곡 모두 Suno Cover 미업로드, 청취 판정 없음입니다. 판정을 받으면 `청취 판정` 칸에 적고 `FEEDBACK_LOG.md` 에 `## 청취 판정 — Vivaldi 사계 변주 v2` 절을 둡니다.
- 솔로 바이올린 EXS `Violin (Arco)` 는 5곡(`vs-summer2-fable`·`vs-summer2-opus`·`vs-autumn2-astra`·`vs-winter1-fable`·`vs-winter3-opus`)에 올라가 있으므로, 이슈 #1 결정 2(솔로 바이올린 판정)는 이 곡들로 들어 보면 됩니다.
