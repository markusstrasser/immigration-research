# Brief: propagate the per-generation identity loss to the lineage size and lineage cost

Finding (d75963b, `civic_trajectory_mexican_2026_09_27/derived/identity_loss.csv`): loss of Mexican
identification at birth keeps growing past G3 (not reported Mexican 7.8 / 15.1 / 12.0% for children of
G1 / G2 / G3+ parents). Two consumers assume identification stops falling after G3 and apply the
measured third-generation rate 0.8881 to every later generation:

1. `mexican_origin_population_total_2026_09_19`, arm 3 ("4th-plus identifies at the measured
   3rd-generation rate"), behind the 42–45M lineage with 11% attrition (ladder 158; memo
   `research/immigration-mexican-origin-population-total-2026-09-19.md`).
2. `lineage_cost_2026_09_19`, whose `inputs.py` (lines ~376–387) reads `fourth_plus_identification_rate`
   0.8881 from that arm (century-lineage memo; ladder 159; `lineage_sponsored_parents_2026_09_27`
   imports the same machinery).

## Tasks

1. Build identification-by-generation arms from `identity_loss.csv`: (a) the current 0.8881 for G4+;
   (b) one more step, G4 ≈ 0.888 × (1 − 0.120) ≈ 0.78, held for G5+; (c) compounding, applying the
   G3+ parents' loss again at each later generation (G5 ≈ 0.69, …); (d) the "not reported Hispanic"
   series in place of "not reported Mexican" (9.0% per step). State that (b)–(d) are [MODEL]
   extrapolations of a birth-stage loss, excluding later switching and the equal-fertility assumption
   the civic lane flags.
2. Re-run the population total's arm 3 under each arm, reporting the lineage size old → new (millions)
   and the implied attrition share.
3. Re-run the lineage cost's central case and its legalisation arms under each arm, reporting the gap
   old → new, undiscounted and at 3%. Also re-run the sponsored-parent arms (entry 241) if they move by
   more than 0.1%.
4. Say which published figures move (ladder 158, 159, 241; the INDEX population line) and by how much.

## Rules

- Read-only on both upstream lanes: import or copy into this directory and override the parameter
  here. Do not edit `inputs.py` or any fingerprinted file (the ledger loaders stop with `[BLOCKED]`
  after edits).
- First reproduce each upstream central (population arm 3; lineage central −$1,297,150 / −$514,635)
  to 1e-6 before running any arm.
- `uv run --no-project python3 …` from the repo root; stop on the first nonzero exit code.
- Outputs: `RESULT.md` opening `**Verdict:**` (stub first), `derived/arms.csv` (arm, consumer, metric,
  old, new, delta), `verify.py`, and `.gitignore` with `_cache/`. No git. Return RESULT.md path and ≤10
  lines.
