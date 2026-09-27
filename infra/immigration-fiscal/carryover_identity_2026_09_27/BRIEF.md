# Lane brief: is the Mexican-origin stall after G2 real, once identity loss is corrected on both sides?

Date 2026-09-27, 23:30 JST. Parent session immigration-research-1c. The operator asked: "Is the Mexican stall
after G2 real? It could be partly people ceasing to identify as Mexican. Identity loss keeps growing past G3,
so 17.5–23% of the third-plus generation may be hidden."

## What exists (read first; do not edit these lanes, they belong to another session)

- `../generation_carryover_2026_09_27/RESULT.md` (e2eeb0d, 827a6b5): G2 → G3+ carries over 85–92% of the gap
  on self-identified CPS data (BA+ 0.92, ledger 0.90, earnings 0.88–0.90). On NLSY97, where G3 is defined by
  the grandparents' birthplace and includes non-identifiers, the step is larger: 0.76 on BA+ and 0.64 on years
  of schooling.
  - Its section 3 corrects the **G3+ gap** and the **G3 → G4+ ratio** for attriters. G3 rates are 11.2% (CPS),
    20.6% (NLSY97) and 28.2% (Duncan–Trejo). G4+ rates are 11.2%, 29.2% and 55.6%.
  - It never corrects the **G2 → G3+ step** itself, and it never corrects G2's own non-identifiers.
  - Files: `derived/attrition_bounds.csv`, `attrition_corrected_rho.csv`, `gaps_by_generation.csv`.
- `../identity_loss_propagation_2026_09_27/RESULT.md` (a50644d): G4+ identification 0.781, hidden share of
  the third-plus 17.5–23.0% (`derived/population_arms.csv`, `schedules.csv`).
- `../mexican_origin_population_total_2026_09_19/` and ladder 158: second-generation identification 92.46%,
  third 88.8%; attrition rises as Mexico-born grandparents fall (2.1% with four, 22.0% with one).
- Ladder 158, 233 (`research/immigration-confidence-ladder.md`).

## Questions

1. **The corrected step.** What does G2 → G3+ carry over once both sides include their non-identifiers?
   - G2's hidden share is 1 − 0.9246.
   - For G3+, use the propagation's 17.5–23.0%, bracketed by the carry-over lane's 11.2% and 28.2%.
   - Give the ratio on BA+, earnings and the partial ledger, at three attriter values: like identifiers,
     the measured non-identifier values, and like whites.
   - Carry the uncertainty through: replicate SEs where the lane has them, and brackets otherwise.
2. **Which attriter advantage is right.** The carry-over lane quotes attriters closing 0.6–6.2 BA+ points of a
   −19.8-point gap. It also uses "the population-total lane's convention, under which attriters close 54–72%
   of the [dollar] gap". These cannot both describe the same people. Trace both to their sources and say which
   one the ledger should use, and why.
3. **A same-sample test.** The CPS–NLSY97 difference (0.92 against 0.76 on BA+) mixes attrition with sample
   and cohort.
   - Find a design that holds the sample fixed, for example:
     - an ancestry-defined G3 against identifiers only within one survey;
     - the CPS co-resident parent-pointer design for young adults;
     - NLSY97 microdata, if obtainable without an account.
   - If none is feasible, say so and bound the attrition share of the gap from the evidence that exists.
4. **Verdict.** Is the stall real, partly an artifact, or unresolved? State the corrected ratio range and which
   inputs are measured and which assumed. Name the evidence that would settle it.

## Rules

- Work only in `infra/immigration-fiscal/carryover_identity_2026_09_27/`. Do not edit the carry-over, propagation
  or population lanes. Do not edit `research/`, `decisions/`, INDEX, FAQ, ladder or `CLAUDE.md`.
- The checkout is shared: no commits, and no `git add`, `stash`, `checkout` or `reset`.
- Run Python as `OPENBLAS_NUM_THREADS=1 uv run --no-project python3 <script>` from the repository root. Write
  CSVs with `lineterminator="\n"`. Two runs must be byte-identical.
- Tag every number: [SOURCE], [DATA], [CALCULATION], [INFERENCE] or [TRAINING-DATA]. Weighted or modelled totals
  are [FRAMING-SENSITIVE]. The gap is against third-plus non-Hispanic whites; say so wherever it is quoted.
- Disconfirmation is part of the task: steel-man the stall before testing it.
- Stub `RESULT.md` with `**Verdict:** pending` first and append as you go.
- Final message: the RESULT path and at most ten lines. List the files covered and skipped, and every judgment
  call.
