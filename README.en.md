**[한국어](README.md)**

# losik

A music production pipeline in which an agent drives Logic Pro. LLM composition rounds (one sketch per model) produce standard MIDI files, and `docs/music/tools/pipeline.py` imports them into Logic Pro Creator Studio and bounces them to WAV automatically. The bounces are then handed to Suno Cover for performance and production.

## Layout

- `docs/music/PROMPT_GUIDELINES.md` — rules for the request → composition → verification loop (spec template, composition MUSTs, GM patch map, Suno procedure)
- `docs/music/LOGIC_LIBRARY_INVENTORY.md` — full inventory of the Logic sound library and the three ways to call an instrument (A: GM program number / B: library patch / C: Sampler preset)
- `docs/music/FEEDBACK_LOG.md` — listening verdicts and decisions per track and round
- `docs/music/tools/` — `pipeline.py` (SMF building, Logic AX automation, bouncing, cross-session `LogicLock`), `gm_map.py` / `library_inventory.py` (library measurement), per-set composition scripts (`dh_*`, `lh_*`, `vivaldi_*`)
- `docs/music/sketches/` — generated MIDI; bounces live in `/Volumes/Netac 2TB/music/bounces/`
- Agent policy and harness: `AGENTS.md`, `.omp/`, `docs/harness/`

## Current cycle

**Loading patches and EXS presets through a Logic template project (routes B·C)** — `docs/harness/seed.yaml` (`20261113-220009-a606`)

Today the pipeline can only pick instruments by GM program number (route A), so legacy orchestral patches and articulation-specific Sampler presets are out of reach. The `produce(template=...)` path imports the SMF into a copy of a template project (Logic always creates new tracks, so the new tracks are reassigned to the template's channel strips) and bounces with the template's patches as-is.

- [x] AC0 spike: build the test template and measure nine aspects of Logic's import behaviour; decide go/stop by the decision table
- [x] AC1 patch and placement: post-import strips match the template snapshot exactly; per-track region names, start positions and tempo verified
- [x] AC2 bounce and audibility: duration, silent bar 1, per-track segment RMS, `SamplerInstrumentsFiles` checked
- [x] AC3 template preserved: sha256 tree hash of the bundle unchanged
- [x] AC4 regression: existing GM path and byte-identical SMF output kept
- [x] AC5 docs: inventory §4 rows B·C updated, template checklist and call signature documented
- [x] AC6 failure paths: `--dry-run` registered; four failure cases stop before touching Logic

Constraints: the template original is never opened in Logic (copies only), and template-mode SMFs carry no PC or CC0/7/10/32 events. The existing `produce()` behaviour and `build_smf` output stay unchanged.

## Status

🚧 In development — see `docs/harness/kickoff-summary.md` and the session notes under `docs/sum/` for full context.
