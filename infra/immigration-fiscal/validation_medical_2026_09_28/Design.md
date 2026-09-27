# Medical validation design — frozen before new scoring

2026-09-28. Existing headline ratios are already known; this is a diagnostic reconciliation,
not a blinded confirmation. It does not change the adopted fiscal model.

**Question.** Why does Hispanic/NH-white public medical spending at 65+ differ between
MEPS 2023 (0.845) and MCBS 2023 (1.265), after Medicare-ever and payer alignment?

**Frozen diagnostics.** On both surveys retain Hispanic and NH-white Medicare-ever
people aged 65+. Report raw denominators, weighted sizes, design SEs, and payer means.
1. Decompose the discrepancy into Medicare and Medicaid using an exact additive
decomposition of group-minus-reference dollars. Test whether high Medicaid expenditure
or Medicare differences dominate.
2. Standardize both ethnic groups to the same age (65–74/75+) and sex shares, using
equal cell weights as a common fixed reference. Report every cell and counts; any cell
with fewer than 20 group observations is flagged, never silently dropped. This is a
composition diagnostic, not a causal ethnicity effect.
3. Repeat with payer-wise p99.5 winsorization in MEPS, acknowledging it only approximates
MCBS disclosure top-coding; also p99 as a common capped-tail sensitivity in both surveys.
4. Compare Medicare Advantage payment-positive versus payment-zero MCBS domains and
MEPS observed HMO coverage where available. Payment positivity is not enrollment; do
not call unmatched proxies an exact FFS/MA comparison.
5. Test income as each survey actually measures it. A poverty-band proxy must not be
relabeled the MCBS household-income threshold. Exact matching is permitted only if
the documented income concepts agree.
6. Hold 2024 MEPS out from a 2016–2023 pooled estimate for a retrospective year
prediction of payer-specific Hispanic/NH-white ratios and Mexican/all-donor ratios.
Compare the training-period estimate with the last-year naive baseline. Estimate the
prediction-minus-observed uncertainty using the shared HC-036 PSU design (so overlapping
panel members do not count as independent). This is unused scoring, not unused data:
prior work has inspected year-specific ratios.

**Judgment rules.** No binary pass from mere confidence-interval overlap. Quantify
how far each diagnostic moves the same-year 0.420 ratio-point gap; call a candidate a
substantial reconciliation only if at least half the gap disappears under a documented
common definition. Describe predictive error and interval, not success from an arbitrary
threshold. Small samples and wide intervals remain inconclusive.

**Limits known before scoring.** The only local MCBS cost PUF is 2023, with 134 columns;
it lacks Mexican origin, exact age, country of birth, enrollment months, and direct
FFS/MA enrollment flags. The MCBS cost PUF excludes facility/hospice/institutional users;
MEPS does not expose the identical exclusion. Both differences prevent full population
alignment. Full payer amounts, MEPS 2016–2024, design variables, and MCBS replicate
weights are available locally. No matched claims or restricted files will be invented.

**Pre-scoring documentation amendment.** The CMS guide §3.4 specifies unweighted
top-0.5%-tail-mean replacement, not winsorization. Add that exact disclosure analogue
to MEPS, separately for Medicare and Medicaid over its full Medicare-ever sample.
Its effects cannot replicate unknown MCBS raw tails exactly. CMS §3.3 also states that
MA non-drug spending has an upward ratio adjustment; the PUF lacks unadjusted values.
The fixed standard population in diagnostic 2 is uniform over four age-sex cells
(65–74 male/female and 75+ male/female), explicitly hypothetical, shared by both files.

**Unused-year external check, before acquisition/scoring.** Acquire the officially
listed 2022 MCBS cost PUF (about 10 MB) and corresponding codebook. Calculate the same
Medicare+Medicaid, Hispanic/NH-white, 65+ ratio with Fay BRR. Compare with MEPS2022,
and report the difference with independent-survey SE. This tests whether the 2023
instrument gap recurs, not its cause; MCBS2022–23 may share respondents, so do not
treat those two differences as independent temporal replications.
