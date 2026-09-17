**Verdict:** No. ACS sampling error on the institutional Δ is an order of magnitude too small to move any headline sign: every Δ has a standard error of $0.19–0.28bn against stored gaps of −$290.6bn and −$215.0bn and a partial balance of +$50.2bn, so the widest 95% interval shifts a headline by at most $0.55bn. Both gates pass exactly — the PUMS `RELSHIPP == 37` tabulation reproduces all 96 API cells and the 107,917 male-18–39 gate to the unit, and the full-weight Δ values reproduce `institutional_bound.csv` to well under $0.01bn.

Model: claude-opus-5[1m].

## What was computed

ACS 2024 1-year person PUMS (both parts, 3,422,888 person records, sha256 `afdc6d90…69894`) with the 80 replicate weights, SDR variance `4/80 × Σ(rep − full)²`, 95% interval `est ± 1.96 × se`. Cost constants and the cost/Δ algebra are taken from the bound lane's `compute_bound.py` by exec'ing its constant block out of the source text, so no number is redefined here and the bound lane's own outputs are never re-run or overwritten.

Group quarters: `RELSHIPP == 37` (institutionalized) matches the API's `TYPEHUGQ = 2` exactly; 84,422 institutional and 98,784 noninstitutional GQ records, 3,239,682 household records, and zero disagreements between the `SERIALNO[4:6] == "HU"` flag and `RELSHIPP ∈ {37, 38}`. Total population per group × band includes household and both GQ types, as in the bound lane.

## Gates

| Gate | Check | Result |
|---|---|---|
| 1 | 96 full-weight cells (N, I, IM over 4 groups × 8 bands) vs `institutional_bound_2026_09_17/derived/acs_cells.csv` | 96/96 exact, 0 mismatches |
| 1b | Male 18–39 US-born Mexican institutional count | 107,917 = 107,917 |
| 2 | Full-weight Δ and cost quantities vs `institutional_bound.csv` | 48/48 within $0.01bn (per-person quantities within $0.05) |

## Headline sign check, pooled Mexican-origin target

Δ is the change the institutional charge makes; the interval is on Δ alone, then carried onto the stored gap.

| Arm | Reference | Stored gap ($bn) | Δ ($bn) | se | Gap + Δ, 95% CI |
|---|---|---|---|---|---|
| adverse | native NH white | −290.59 | −2.107 | 0.283 | −293.25 [−293.81, −292.69] |
| adverse | all natives | −214.996 | +5.253 | 0.274 | −209.74 [−210.28, −209.21] |
| moderate | native NH white | −290.59 | −2.881 | 0.250 | −293.47 [−293.96, −292.98] |
| moderate | all natives | −214.996 | +4.090 | 0.250 | −210.91 [−211.40, −210.42] |

Partial balance: the pooled Mexican-origin institutional cost is $19.79bn (se $0.25bn) on the adverse arm and $18.35bn (se $0.24bn) on the moderate arm, against a stored +$50.238bn absolute balance. Netting leaves +$30.45bn [29.96, 30.95] and +$31.89bn [31.42, 32.35]. No sign flip is reachable inside the sampling interval in any of the six checks.

## Precision of the Δ quantities

Relative standard errors on the aggregate Δ run 4.6–13.4% for the pooled target and the Mexico-born target, and 5.1–5.7% against the white reference for the US-born group. One quantity is not distinguishable from zero: the moderate-arm Δ for US-born self-identified Mexicans against all natives, +$0.112bn [−0.269, +0.493]. That cell is small because the two groups' institutional cost profiles nearly cancel under the male-share weighting, and it is not a headline quantity.

Standardized per-person Δ values carry 4.3–26.8% relative standard errors; the least precise is the US-born-vs-white standardized Δ, −$74.8/person [−114.0, −35.5], which stays negative across the interval.

## Scope of the intervals

These intervals cover ACS sampling error only. They do not cover the cost parameters (the $60,989 per-prisoner figure, the $122,500 nursing-facility total, the 0.77 public-payer share), the choice of the adverse-vs-moderate arm, or the uncertainty in the CPS-based gaps the Δ values are added to. The bound lane's own sensitivity headroom remains the relevant sensitivity on cost: it takes roughly a 2.5–2.7× cost multiplier to erase the +$50.2bn balance, which dwarfs the sampling spread measured here.

## Files

Covered: `derived/institutional_bound_with_variance.csv` (54 rows: arm × target × reference × quantity, with estimate, se, 95% bounds, relative se, and whether the interval excludes zero), `derived/audit.json` (source hash, record counts, both gates in full, headline sign check), `inst_variance.py`.

Skipped: the two `*_nf_medicaid_only` sensitivity arms, per the brief's scope of the `adverse` and `moderate` headline arms. The age standard is held at the white group's full-weight age shares across replicates, as specified, so the standardized Δ intervals do not include variance in the standard itself.

[SOURCE: ACS 2024 1-year person PUMS, https://www2.census.gov/programs-surveys/acs/data/pums/2024/1-Year/csv_pus.zip]
