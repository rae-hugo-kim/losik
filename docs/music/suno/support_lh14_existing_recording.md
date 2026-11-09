# Suno support 문의 초안 — lh14 "matches an existing recording" (2026-11-07)

작성 규칙: 리포·프로필에 메일 규칙이 없어 사용자 확인(2026-11-07)으로 정함 — 영어, 간결한 사실 나열, MIDI 소스만 첨부 + WAV 는 링크, 발신 정보는 자리표시자. 보내기 전에 `[ ]` 를 채운다.

반려 시각은 분 단위로는 우리 쪽 기록에 없다(Suno 가 반려 업로드를 라이브러리에 남기지 않음). 대화·파일 mtime·커밋으로 되짚은 **범위**를 본문에 썼고, 앵커는 같은 자리에서 **통과한** 업로드(라이브러리에 시각이 남음)다:

| 사건 | 하한 (우리 기록) | 상한 (사용자 보고) | 앵커 |
|---|---|---|---|
| lh14-v2·lh02-v2 반려 | 2026-11-05 14:42 KST — Suno 블록 커밋 `3296930` 직후 업로드 시작 | 2026-11-06 ~15:10 KST — 반려 보고, v2u 바운스 시작(15:21 mtime) 전 | lh01-v2·lh15-v2 통과 업로드 |
| lh14-v2u 반려 (lh02-v2u 통과) | 2026-11-06 15:25 KST — v2u WAV mtime | 2026-11-07 ~00:05 KST — 보고, v2t 바운스(00:10 mtime) 전 | lh02-v2u 통과 업로드 |
| lh14-v2t 반려 | 2026-11-07 00:10 KST 생성 | 00:25 KST 경 (사용자 "방금 했지", 00:27 기준) | — |

라이브러리에서 lh01-v2·lh15-v2·lh02-v2u 의 업로드 시각을 확인하면 그 시각으로 범위를 좁혀 적을 수 있다.

---

**To**: support@suno.com
**Subject**: Original instrumental flagged as "matches an existing recording" — lh14-brass-orchard (3 attempts)

Hello Suno team,

An upload of my own instrumental track is being rejected with "This audio matches an existing recording. Our system matched this upload to a known recording." The track is original and I own all rights.

Facts:

- Suno account: sangrae13@hanmail.net (Pro plan). I am writing from a different address; please attach this ticket to that account.
- File: lh14-brass-orchard-v2.wav (WAV 24-bit, 2:54, 50.3 MB), rejected between 2026-11-05 15:00 and 2026-11-06 15:00 KST (UTC+9) — in the same session in which lh01-felt-doorway-v2.wav and lh15-quartz-overpass-v2.wav were accepted (both visible in my library). lh02-linen-afternoon-v2.wav was rejected with the same message in that session.
- The track is a MIDI composition rendered in Logic Pro with its stock instruments (SoCal drum kit, Pulse Bass, Deluxe Classic electric piano, Classical Acoustic Guitar, Studio Grand, Classic Pad). No samples, loops, or recordings of other works were used.
- A re-render of the same MIDI was also rejected: lh14-brass-orchard-v2u.wav (tempo 90 BPM instead of 88), between 2026-11-06 15:30 and 2026-11-07 00:00 KST, in the same session in which lh02-linen-afternoon-v2u.wav was accepted (visible in my library). A third render, lh14-brass-orchard-v2t.wav (transposed up one semitone to F major, 90 BPM), was rejected on 2026-11-07 at about 00:25 KST.
- Three other tracks from the same project, made with the same tools and the same workflow, uploaded without issue: lh01-felt-doorway-v2.wav, lh15-quartz-overpass-v2.wav, lh02-linen-afternoon-v2u.wav.

Could you tell me which recording the system matched, and allow the upload? I can send the Logic Pro project if that helps.

Attached: lh14-brass-orchard-v2.mid (31 KB) — the MIDI source of the rejected audio.
All three rejected renders (WAV, ~50 MB each) in one folder: https://www.icloud.com/iclouddrive/0257uUox7gK5E90gVLw3XGUOQ#suno-support-lh14

Thank you,
Hugo

---

## 한국어 대역 (참고용, 보내지 않음)

제목: 자작 연주곡이 "기존 녹음과 일치"로 반려됨 — lh14-brass-orchard (3회 시도)

안녕하세요 Suno 팀,

제 자작 연주곡 업로드가 "This audio matches an existing recording…" 메시지로 반려되고 있습니다. 이 곡은 제가 만든 원곡이며 권리는 전부 제게 있습니다.

사실 관계:
- Suno 계정: sangrae13@hanmail.net (Pro). 발신 주소(naver.com)가 계정과 달라 그 계정에 티켓을 연결해 달라고 명시
- 파일: lh14-brass-orchard-v2.wav (WAV 24비트, 2:54, 50.3 MB), 2026-11-05 15:00 ~ 11-06 15:00 KST 사이 반려 — lh01-v2·lh15-v2 가 통과한(라이브러리에 보임) 같은 자리. lh02-v2 도 같은 메시지로 반려
- MIDI 로 작곡해 Logic Pro 기본 악기(SoCal 드럼, Pulse Bass, Deluxe Classic EP, Classical Acoustic Guitar, Studio Grand, Classic Pad)로 렌더한 곡입니다. 샘플·루프·타인의 녹음은 전혀 쓰지 않았습니다.
- 같은 MIDI 를 다시 렌더한 v2u(템포 88→90 BPM)도 2026-11-06 15:30 ~ 11-07 00:00 KST 사이 반려 — lh02-v2u 가 통과한 같은 자리. 세 번째 렌더 v2t(+1 반음 전조 F장조, 90 BPM)는 2026-11-07 00:25 KST 경 반려.
- 같은 프로젝트·같은 도구·같은 절차로 만든 다른 세 곡(lh01-…-v2, lh02-…-v2u, lh15-…-v2)은 같은 세션에서 문제없이 업로드됐습니다.

어떤 녹음과 일치로 판정됐는지 알려 주시고 업로드를 허용해 주실 수 있을까요? 필요하면 Logic Pro 프로젝트도 보내 드리겠습니다.

첨부: lh14-brass-orchard-v2.mid (31 KB) — 반려된 오디오의 MIDI 소스.
반려된 렌더 세 개(WAV, 각 ~50 MB)는 폴더 하나로: https://www.icloud.com/iclouddrive/0257uUox7gK5E90gVLw3XGUOQ#suno-support-lh14

감사합니다,
Hugo
