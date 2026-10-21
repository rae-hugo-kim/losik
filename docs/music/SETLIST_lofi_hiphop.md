# Lo-fi Hip Hop Set — 2026-10-21

30곡 · 총 **90:33**(마디×BPM 계산; WAV 실측은 FEEDBACK_LOG) · 76→88→72 BPM · Camelot 인접 키, 장·단조 섞음.
브리프: `LOFI_HIPHOP_SET_BRIEF.md`. 작곡기: `tools/lh_astra.py`(gpt-6-astra) / `tools/lh_fable.py`(claude-fable-5-1) / `tools/lh_opus.py`(claude-opus-5-5). 바운스: `tools/bounce_dh.py --set lh --ver v1` → `/Volumes/Netac 2TB/music/bounces/{sid}-v1.wav`. Suno 프롬프트: `SUNO_PROMPTS.md` 의 `## {sid}-v1` 블록(lo-fi 섹션).

구조: 56마디(≤78 BPM) 1–8 intro / 9–24 A / 25–32 break / 33–48 A2 / 49–56 outro · 64마디(≥80) 1–8 / 9–28 / 29–36 / 37–56 / 57–64. 인트로는 키 또는 텍스처 먼저, 드럼 5마디, 베이스 9마디. 리드 모티프는 A 마지막 8마디부터 A2 내내. 믹스 큐: 앞 곡 outro 첫 마디 ↔ 뒷 곡 1마디.

## 셋리스트

| # | sid | 모델 | BPM | 마디 | 키 | 길이 | E | 메모 |
|---|---|---|---|---|---|---|---|---|
| 1 | lh01-felt-doorway | astra | 76 | 56 | D minor | 2:56 | 1 | Dorian two-chord doorway; keys and hats open together; four-bar descen |
| 2 | lh02-linen-afternoon | fable | 76 | 56 | D minor | 2:56 | 1 | Natural-minor i-v-VI-iv; nylon opens alone, EP answers off the beat. |
| 3 | lh03-chalk-awning | opus | 78 | 56 | F major | 2:52 | 2 | Nylon opens alone; EP holds bar one and answers late; grand lead climb |
| 4 | lh04-paper-saucer | astra | 78 | 56 | C major | 2:52 | 2 | I-iii-ii-V grand-piano comping; nylon lead has a rising third and step |
| 5 | lh05-tin-kettle | fable | 80 | 64 | A minor | 3:12 | 2 | i-VI-III-V7b9 grand piano on the and-of-two; nylon climbs a triad then |
| 6 | lh06-iron-teacup | opus | 80 | 64 | A minor | 3:12 | 2 | Descending aeolian loop; three-note falling cell sequenced down, answe |
| 7 | lh07-moss-index | astra | 82 | 64 | E minor | 3:07 | 2 | Minor i-iv-v-i; a descending four-note piano bookmark rides alternatin |
| 8 | lh08-cedar-ledger | fable | 82 | 64 | G major | 3:07 | 2 | I-iii-vi-IV EP; grand-piano lead falls a fifth then climbs back to the |
| 9 | lh09-signal-orchard | opus | 84 | 64 | D major | 3:02 | 2 | Rising into the peak: EP triple comps, organ holds, one quiet sixteent |
| 10 | lh10-copper-margin | astra | 84 | 64 | B minor | 3:02 | 3 | i-III-VI-V9 peak entry; an EP minor-third ladder resolves into a domin |
| 11 | lh11-velvet-circuit | fable | 86 | 64 | B minor | 2:58 | 3 | i-iv-VI-VII13 grand piano with organ holds; EP lead folds a D-F#-A arc |
| 12 | lh12-ember-switchyard | opus | 86 | 64 | F# minor | 2:58 | 3 | Dorian peak with PC38 bass; and-of-one triad climbs folded back down. |
| 13 | lh13-apricot-carbon | astra | 88 | 64 | A major | 2:54 | 3 | Warm I-iii-vi-ii at the high point; nylon turns around a repeated A-C# |
| 14 | lh14-brass-orchard | fable | 88 | 64 | E major | 2:54 | 3 | I-IV-iii-vi EP; nylon lead rises G#-B-C# then walks down B-G#-F#-E. |
| 15 | lh15-quartz-overpass | opus | 88 | 64 | C# minor | 2:54 | 3 | Peak; nylon opens, EP enters at five; neighbour-tone turn repeated a s |
| 16 | lh16-indigo-receipt | astra | 86 | 64 | C# minor | 2:58 | 3 | i-III-VII-V7b13 hinge; piano rises through E major then turns around t |
| 17 | lh17-slate-harbour | fable | 86 | 64 | G# minor | 2:58 | 2 | i-VI-VII13-v grand piano opened by a high EP; piano lead peaks on D# a |
| 18 | lh18-lantern-deck | opus | 84 | 64 | B major | 3:02 | 2 | Drift begins: borrowed minor iv darkens the loop; organ swells under t |
| 19 | lh19-pearl-crossing | astra | 84 | 64 | F# major | 3:02 | 2 | Stepwise I-ii-iii-IV drift; EP rises to C# then lets the answering phr |
| 20 | lh20-dusk-corridor | fable | 82 | 64 | Eb minor | 3:07 | 2 | i-III-iv-v EP on the off-beat; EP lead drops Bb-Gb-F and climbs back t |
| 21 | lh21-ink-carousel | opus | 82 | 64 | Eb minor | 3:07 | 2 | Same key as slot 20 but a falling-fourths loop, held comping and a rep |
| 22 | lh22-plum-platform | astra | 80 | 64 | Bb minor | 3:12 | 2 | i-VI-VII13-iv suspended return; grand-piano F-Ab-F sigh answers downwa |
| 23 | lh23-honey-transit | fable | 80 | 64 | Db major | 3:12 | 2 | I-ii-IV-V13 grand piano with organ; nylon lead climbs F-Ab-C and answe |
| 24 | lh24-felt-almanac | opus | 78 | 56 | Ab major | 2:52 | 1 | Cool-down begins: sparse two-note lead, EP comping thins to one hit in |
| 25 | lh25-wool-calendar | astra | 78 | 56 | F minor | 2:52 | 2 | Two bars of i then VI-VII9; a close nylon descent softens the cooldown |
| 26 | lh26-quiet-ferry | fable | 76 | 56 | F minor | 2:56 | 1 | i-iv alternating every bar over a low pad, rootless Fm9 and Bbm9 holds |
| 27 | lh27-moth-library | opus | 76 | 56 | C minor | 2:56 | 1 | Energy 1 with even-bar rim and a low 1+5 pad; long-tone EP lead. |
| 28 | lh28-amber-bookend | astra | 74 | 56 | Eb major | 3:01 | 1 | I-IV-ii-V13 closing warmth; grand-piano descending thirds leave room f |
| 29 | lh29-cotton-ledge | fable | 74 | 56 | Bb major | 3:01 | 1 | I-I-ii-IV grand piano with high EP; nylon lead lifts A-C, D then rests |
| 30 | lh30-last-streetlamp | opus | 72 | 56 | G minor | 3:06 | 1 | Closer: outro drops drums at 51, bass at 53, keys alone, final bar one |

## 흐름

- **1–4 오프닝** (Dm→C, 76–78): 키+햇으로 시작, 성긴 붐뱁. 
- **5–9 안착** (Am→D, 80–84): 리드 모티프와 텍스처가 또렷해짐.
- **10–16 피크** (Bm→C♯m, 84–88): 16분 햇 장식, PC38 베이스, 가장 찬 편성. 그래도 lo-fi 답게 중역 중심.
- **17–23 드리프트** (G♯m→D♭, 86–80): 장조 비중 ↑, 라이드·패드 색.
- **24–30 쿨다운** (A♭→Gm, 78–72): 56마디판, 림 백비트, 클로저는 드럼→베이스→키만→마지막 마디 한 화음.

코드 루프·킥 셀·리드 모티프·브레이크의 곡별 상세는 `FEEDBACK_LOG.md` 의 `## 2026-10-21 lofi hip hop set — <model>` 표. 청취 판정은 같은 파일에 `## 청취 판정 — lofi hip hop set` 으로 받는다.
