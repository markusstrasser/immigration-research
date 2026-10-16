**Verdict:** PASS. Independently reconstructed all eight primary unweighted outcome summaries and all eight December-weighted summaries, including the weighted Fay-BRR confidence limits. Counts and estimates agree with the parent's `derived/changes.csv` to its printed precision. No substantive divergence found.

This was one verification pass using the validated `events.parquet`, original-extraction `persons.parquet`, and official December replicate weights. It did **not** import, execute, or read `measure.py` and did not use the parent's coded `event_panel.parquet`. `verify_numbers.py` contains the independent calculation; `numerical_verification.json` records estimates, field-by-field differences and SHA256 hashes of all inputs.

## Independent coding

The official dictionary was re-read at RMESR (printed p.2489), TMWKHRS (p.2579), TPEARN_ALT (p.2631), ENJ_UPDWKYN (p.2747), and job-spell beginning/ending months (pp.2339/2346). Existing source files: `events/dictionary.txt` and the 2025 SIPP guide text.

- Employment: RMESR1–5 =1;6–8 =0; other/missing stays missing.
- Hours: use numeric TMWKHRS, including zero. Missing is zero only with RMESR6–8, no active job spell and AMWKHRS0.
- Earnings: retain numeric TPEARN_ALT, including negatives. Missing is zero only with APEARN_ALT0 and either known no-job status without an active job spell, or explicit ENJ_UPDWKYN1 unpaid family work without an active job spell. The same procedure with TPEARN/APEARN supplies the actual-calendar-month sensitivity. Unpaid family work does not supply an assumed hours value.
- All outcomes require RIN_UNIV1. Other missing values remain missing. Each outcome requires all six monthly values; means compare t−3…t−1 with t…t+2 for the same adult. No restrictions on later moves were added.

The raw extract contains two event-window records with RMESR6–8 and an active calendar job spell. The independent zero rule does not force those records to zero. The resulting primary counts and estimates nevertheless match exactly at printed precision; no consequential discrepancy follows from this diagnostic.

## Independently reconstructed unweighted results

Employment values below are percentages; changes are percentage points. Hours are average weekly hours; earnings are nominal2024 dollars per month.

| Route | Outcome | Adults | Before | After | Change |
|---|---|---:|---:|---:|---:|
| Tracked | Employment |147|73.015873|72.108844|−0.907029 pp|
| Tracked | Hours |146|29.754909|30.017808|+0.262900|
| Tracked | Earnings, month-length standardized |147|6545.433107|7329.702948|+784.269841|
| Tracked | Earnings, calendar month |147|6536.263039|7329.374150|+793.111111|
| Type-2 | Employment |277|78.580024|77.617329|−0.962696 pp|
| Type-2 | Hours |277|30.391637|29.739651|−0.651986|
| Type-2 | Earnings, month-length standardized |277|5618.000000|5531.051745|−86.948255|
| Type-2 | Earnings, calendar month |277|5627.239471|5533.226233|−94.013237|

Every tracked outcome has78 original sample-unit clusters; every Type-2 outcome has145. These descriptive changes do not identify the effect of departure.

## December weights and Fay variance

The official guide's pp.153–154 specify240 replicates and Fay k=.5. For each complete outcome cohort, independently computed the December-weighted average of each person's pre/post mean and of their difference. Replicate-specific weighted differences were recomputed using all240 weights. Variance = sum of squared deviations of replicate estimates from the full estimate divided by `240*(1-.5)^2`; confidence limits use estimate ±1.96 SE.

All eight weighted point estimates and both confidence limits match the parent. Two examples:

- Tracked standardized earnings: **+$738.819674**,95% interval **−$216.803890 to+$1694.443238**.
- Type-2 standardized earnings: **−$222.885729**,95% interval **−$646.245613 to+$200.474155**.

The December WPFINWGT and replicate-file base weight agree within0.0000005, consistent with stored precision; no weights are missing in these outcome cohorts.

## Covered and skipped

Covered: all `specification=all` unweighted N,cluster count,pre,post,change; all corresponding December-weighted values and Fay confidence limits; balanced cohort construction and structural-zero coding; all four outcomes in both routes. Source input hashes are recorded in JSON.

Skipped: unweighted percentile-cluster-bootstrap intervals (not independently rerun in this numerical pass), subgroup/sensitivity rows beyond `all`, benchmark controls, causal identification, and transport to deportation or v9. Those are separate claims; agreement here verifies the primary arithmetic and coding only.
