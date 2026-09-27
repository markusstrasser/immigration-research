# Lane brief: do the account's keys predict where administrative dollars land? (pre-registered)

Date 2026-09-28, 07:40 JST. Parent session immigration-research-1c. The operator asked for back-tests "where our
stuff predicts some other reality". The national closure cannot test a key, because every key splits 100% of its
line (`external_benchmarks_2026_09_24/RESULT.md`, "Why the national closure cannot test shares"). State totals can.
The group is a third of residents in some states and 1% in others. If a key misstates the group's use, the error
shows up in the states where the group is large.

This lane tests keys that no administrative record by ethnicity has reached. SNAP, WIC, TANF, UI, housing and
Medicaid coverage are done (`admin_benefit_keys_2026_09_24`); do not redo them.

## Protocol: predict, freeze, then look

1. **Phase 1, predict.** Compute every prediction below from the adopted account's own frame: CPS ASEC 2025, the
   microdata behind each key, with the rules the builders apply. Write `derived/predictions.csv` and
   `PREDICTIONS.md`. Each check gets:
   - the account's prediction;
   - two naive baselines;
   - the tolerance you declare now: what counts as a hit, a miss and "no power";
   - what a miss would mean: which key moves, in which direction.

   You may read each external source's documentation to match definitions. Do not open its numbers. If a number is
   already in the repo or you know it, mark that check "not blind".
2. **Freeze.** Message the parent "predictions frozen", with the file paths, and stop. The parent commits them, and
   the commit time is the pre-registration.
3. **Phase 2, score.** Only after the parent says go:
   - fetch the primary files (hash them into `derived/sources.json`, save quotes in `reads/`);
   - score every check against its declared tolerance and both baselines;
   - for any miss, compute the key correction it implies and its effect at specifications 48 and 11, using the
     September 27 package unchanged, with a payload that holds national totals. Report it as a candidate, not
     adopted.

## Checks

1. **Refundable credits by state (IRS SOI).**
   - Target: EITC and the refundable child credit (ACTC), in dollars, by state, for the latest tax year SOI
     publishes by state.
   - Prediction: the account's refundable-credit microdata, SSN rule included, summed by state and scaled to IRS's
     national total.
   - Baselines: the same microdata without the SSN rule; population shares.
   - This line is $55.4bn on the group (24.46% share); Treasury's national Hispanic split already cut it once
     (ladder 216). Report the slope of the error on the state's group share and the errors in CA, TX, AZ, NM, NV,
     CO and IL.
2. **SSI and Social Security by state (SSA).**
   - Target: SSI payments, and OASDI benefits, by state for 2024.
   - Prediction: the account's `ssi` and `social_security` key microdata by state, scaled to the national totals.
   - Baselines: population shares; age-65+ population shares.
3. **Births and who paid (NVSS 2024 natality).**
   - Target: births to mothers of Mexican origin (and to Mexico-born mothers), by state, and the share paid by
     Medicaid (CDC WONDER or the public natality file).
   - Predictions: births from the account's frame, from infants in group households or whatever the builders
     use; the Medicaid-paid share from the group's Medicaid coverage among women 15–44.
   - Baseline: the group's share of women 15–44.
   - Maternity is a large Medicaid item. A gap between NVSS's Medicaid-paid share and the frame's coverage would
     show whether the medical key sees the group's births.

## Rules

- A new lane in this directory. Import the builders, don't copy them. Gate: your per-key national shares reproduce
  the adopted ones to 1e-9.
- Scripts write to `derived/`; raw pulls go in `_cache/`. Two runs through `scripts/rerun_lane.py` must be
  byte-identical.
- Never print the Census API key; pipe Census output through a redaction filter. Tag every number. No commits,
  staging or stash.
- Final message (after Phase 2): the RESULT path and at most ten lines, one per check: hit, miss or no power, and
  the dollar effect of any miss at 48 / 11.
