# IQ Sex Differences - Matrix Experiment Deployment

**Date:** 2026-03-07  
**Purpose:** convert the local `OMIB` timing pilot from a stimulus bank into a runnable small study.

Companion files:

- `research/iq-sex-differences-matrix-experiment-protocol.md`
- `research/iq-sex-differences-open-matrix-assets.md`
- `sources/iq-sex-diff/build_omib_session_runner.py`
- `sources/iq-sex-diff/serve_omib_pilot.py`
- `sources/iq-sex-diff/data/matrix_open/omib/omib_participant_text.md`
- `sources/iq-sex-diff/data/matrix_open/omib/omib_analyst_checklist.md`

---

## What is now deployable

The repo now has a minimal local session runner for the `OMIB` pilot.

It supports:

1. one participant at a time
2. analyst-assigned `Form` and `Condition`
3. per-item timer reset
4. exported TSV rows with answer strings and click logs
5. direct compatibility with `score_omib_pilot.py`

This is enough for a first local pilot. It is not a production survey platform. [INFERENCE]

## Run path

1. Build or rebuild the runner assets:

```bash
uv run python3 sources/iq-sex-diff/build_omib_session_runner.py
```

2. Start the local server:

```bash
uv run python3 sources/iq-sex-diff/serve_omib_pilot.py --port 8765
```

3. Open:

```text
http://127.0.0.1:8765/pilot_runner/index.html
```

4. Enter participant metadata, assign `Form` and `Condition`, and run the session.

5. Download the TSV and score it:

```bash
uv run python3 sources/iq-sex-diff/score_omib_pilot.py \
  --responses path/to/session.tsv \
  --out path/to/scored.tsv
```

## Files to hand to a human operator

1. participant text: `sources/iq-sex-diff/data/matrix_open/omib/omib_participant_text.md`
2. analyst checklist: `sources/iq-sex-diff/data/matrix_open/omib/omib_analyst_checklist.md`
3. runner entry point: `sources/iq-sex-diff/data/matrix_open/omib/pilot_runner/index.html`

## What remains human-gated

1. participant recruitment
2. randomization ledger for `Form` and `Condition`
3. consent handling consistent with the chosen venue
4. storage of raw TSVs under the project’s human-subjects policy

## Why this is the correct minimal deployment

No heavy backend was added.

That is deliberate.

The current goal is a small randomized timing pilot, not a multi-tenant assessment platform. A local static runner plus TSV export is enough to test whether tighter timing materially moves the matrix sex gap. If the pilot works, a hosted survey implementation can come later. [INFERENCE]
