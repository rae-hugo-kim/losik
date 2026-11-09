# Vivaldi 사계 변주 — 2026-11-05 집계

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
