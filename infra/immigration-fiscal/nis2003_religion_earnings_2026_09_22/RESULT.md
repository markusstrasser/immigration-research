# NIS 2003 — religion, employment and earnings among new legal permanent residents

**Verdict:** Muslims in the 2003 legal-immigrant cohort are 10.4 points less likely to be
working than Christians at interview, and that gap is almost entirely composition. Once age,
sex, schooling, English, class of admission and origin are held fixed it falls to −0.8 points
with a standard error of 2.6. Conditional on working, the pay rate gap is indistinguishable
from zero under every specification tried (adjusted +0.05 log points, SE 0.07). The one
measure that keeps a Muslim deficit is wage income actually received over the prior twelve
months, and that measure loads on months worked rather than on the wage. Descriptive only:
this is a cohort of new legal immigrants interviewed about four months after admission, not
the foreign-born population. [CALCULATION: derived/earnings_gaps.csv]

## Headline

Ages 18–64, weighted by the NIS design weight, Christian (Catholic + Orthodox + Protestant)
reference. Standard errors in brackets from a 500-draw stratified respondent bootstrap.
[CALCULATION: derived/earnings_gaps.csv]

| Group | Employment rate | Gap, unadjusted | Gap, adjusted | Gap, adjusted + origin |
|---|---|---|---|---|
| Christian | 0.6110 [0.0082] n=4,921 | reference | reference | reference |
| Muslim | 0.5073 [0.0252] n=606 | −0.1037 [0.0263] | −0.0225 [0.0243] | −0.0079 [0.0261] |
| Hindu | 0.5461 [0.0260] n=585 | −0.0650 [0.0272] | −0.0627 [0.0280] | +0.0015 [0.0364] |
| Buddhist | 0.4294 [0.0356] n=287 | −0.1817 [0.0364] | −0.0275 [0.0373] | +0.0429 [0.0388] |
| Jewish | 0.6078 [0.0575] n=98 | −0.0032 [0.0585] | −0.0772 [0.0555] | −0.0612 [0.0576] |
| No religion | 0.6063 [0.0185] n=918 | −0.0048 [0.0202] | +0.0119 [0.0197] | +0.0291 [0.0216] |
| Other | 0.5335 [0.0398] n=192 | −0.0776 [0.0405] | −0.0600 [0.0367] | −0.0253 [0.0386] |

Log-earnings gaps to the Christian group. `earn_annual` annualises the pay rate on the job
held at interview; `wage_12m` is wage and salary income received over the prior twelve months.
[CALCULATION: derived/earnings_gaps.csv]

| Group | Median earn_annual | earn_annual unadj | earn_annual adj | adj + origin | Full-time adj | wage_12m unadj | wage_12m adj |
|---|---|---|---|---|---|---|---|
| Christian | 18,730 [335] n=2,173 | ref | ref | ref | ref | ref | ref |
| Muslim | 17,429 [777] n=231 | +0.1225 [0.0804] | +0.0508 [0.0721] | +0.0399 [0.0795] | +0.0437 [0.0696] | −0.2901 [0.1250] | −0.0823 [0.0994] |
| Hindu | 40,380 [11,260] n=272 | +0.4878 [0.1506] | −0.0544 [0.1374] | −0.2061 [0.1824] | +0.0223 [0.1150] | +0.5439 [0.1447] | +0.1125 [0.1233] |
| Buddhist | 16,107 [1,454] n=93 | −0.0009 [0.1226] | +0.0598 [0.1309] | +0.0281 [0.1466] | +0.0694 [0.1182] | −0.5513 [0.2489] | −0.4370 [0.2165] |
| Jewish | suppressed n=42 | suppressed | suppressed | suppressed | suppressed | +0.9563 [0.1743] | +0.4596 [0.1823] |
| No religion | 21,600 [1,648] n=404 | +0.3750 [0.0800] | +0.1755 [0.0722] | +0.1156 [0.0701] | +0.1543 [0.0696] | +0.0433 [0.1126] | −0.0190 [0.0995] |
| Other | 20,800 [1,490] n=82 | +0.2872 [0.1016] | +0.1634 [0.0864] | +0.0970 [0.0929] | +0.1106 [0.0851] | +0.1680 [0.2194] | −0.1183 [0.2018] |

Within the Christian reference, against Catholics: Orthodox employment −0.0882 [0.0233] and
log earnings −0.2530 [0.0853]; Protestant −0.0301 [0.0177] and −0.1410 [0.0861]. Pooling the
three into one reference group therefore hides real spread, and Muslims sit inside that
spread rather than outside it (Muslim against Catholic: employment −0.0548 [0.0254], log
earnings −0.0601 [0.0861]). [CALCULATION: derived/earnings_gaps.csv]

## Cell sizes

Unweighted, all ages. [CALCULATION: derived/religion_cells.csv]

| Group | n | With employment | With earn_annual | With wage_12m |
|---|---|---|---|---|
| Catholic | 3,119 | 2,870 | 1,297 | 1,261 |
| Protestant | 1,313 | 1,241 | 560 | 594 |
| Orthodox | 840 | 810 | 316 | 347 |
| Christian, pooled | 5,272 | 4,921 | 2,173 | 2,202 |
| No religion | 992 | 918 | 404 | 428 |
| Muslim | 643 | 606 | 231 | 254 |
| Hindu | 618 | 585 | 272 | 280 |
| Buddhist | 313 | 287 | 93 | 100 |
| Other | 213 | 192 | 82 | 79 |
| Jewish | 105 | 98 | 42 | 55 |
| Refused / don't know / missing | 417 | — | — | — |

## Gates

| Gate | Status | Evidence |
|---|---|---|
| G1 source zip sha256 | PASS | `61a6e3d5…85c1`, matches `sources/immigration-fiscal/data/MANIFEST.md` |
| G2 8,573 unique respondents per dataset | PASS | all 8 adult datasets, joined on `PU_ID` with no duplicates |
| G3 three or more published counts reproduced | PASS | 19 of 26 anchors exact [CALCULATION: derived/anchors.csv] |
| G4 every code printed with its codebook label | PASS | `code_lists`, `code_sources`, `variable_labels_verified` in derived/audit.json |
| G5 every reported cell n ≥ 50, every SE finite | PASS | 246 reported, 18 suppressed, all Jewish earnings cells |

Anchors that reproduced exactly: the 8,573 completed adult interviews in every dataset; the
sampling frame total 289,478 and 12,488 cases sampled from Table 1 of the weights
documentation; all 32 distinct design weights rebuilt from that table by the documented
recipe, matching `NISWGTSAMP1` to 4.8e−14; the stratum label of all 32 cells; 30 of the 32
stratum-by-replicate completed-case counts; completed cases in strata 2 and 3 exactly
(1,369 and 1,235); and the weighted share adjusting status, 0.5738 against a published
"approximately 57%".

Anchors that came close without matching to the unit, reported rather than tuned: strata 1
and 4 each differ by one case (1,428 against 1,427 and 4,541 against 4,542) with the total
exact, so one case moved between strata in replicate 4 after the documentation was written.
Home ownership among those 25–64 at admission reproduces the shape but not the level:
employment principals 0.3736 against a published 0.38 and diversity principals 0.0443
against 0.05 both round correctly, the residual category 0.1992 against 0.21 is a point low,
and spouses of US citizens 0.3742 against 0.406 is 3.2 points low. Section H reaches only
6,406 of 8,573 adults because it is administered to whichever spouse is most knowledgeable
about household finances, and the published figures were computed on the project team's own
file. That anchor is not counted toward G3.

## Results that looked wrong, and what they turned out to be

All five are recorded with their diagnostics in `derived/audit.json` under
`anomalies_and_resolutions`. None was smoothed over in the tables.

1. **Muslim median earnings below Christian, but the unadjusted log gap positive.** Real.
   The mean of log earnings is a geometric mean and is driven by the left tail, and the
   Christian left tail is much lower: weighted p10 of $2,219 against $6,030, against medians
   of $18,730 and $17,429. Median and mean-log genuinely rank the two groups in opposite
   directions, so both are reported.
2. **Hindu median earnings carry an $11,000 standard error.** Real, and a property of the
   distribution rather than of the estimator, which is unit-tested against `numpy.median` at
   equal weights. The Hindu weighted p45 to p55 band spans $23,302 to $54,539, a width of
   $31,237 against $3,120 for Christians, so the median travels a long way under resampling.
   The log gaps are the stable statistic for that group; the median should not be read as
   precise.
3. **The two earnings measures disagree in sign unadjusted, +0.12 against −0.29.** Both are
   correct and measure different things. The Section C measure annualises the pay rate on the
   current job and so conditions on working. The Section G measure is income actually received
   over twelve months and, for a cohort interviewed four months after admission, loads heavily
   on months in the country and employed. A group with a lower employment rate and the same
   pay rate shows parity on one and a deficit on the other, which is exactly the pattern here.
4. **Muslims report any wage income more often than Christians (0.87 against 0.85) despite a
   lower employment rate.** A universe difference, flagged rather than adjusted away:
   `any_wage_12m` exists only for respondents whose household answered Section G, so its
   denominator is a selected subset of each group. The employment rate is the comparable
   participation measure.
5. **The spouse path recovered 840 wage reports where a valid spouse `G1` existed for 1,522.**
   Correct, and exhaustive over the universe the instrument allows. The recoverable item is
   the spouse's `G15`, and item `G13` that leads to it is reached only "IF NOT MARRIED/PARTNERED
   OR G2=1: G21". Only 848 cases reach that branch. A test of mine asserted the wrong ceiling
   and was corrected against the questionnaire, not by loosening the threshold.

## Limits

- **New legal permanent residents only**, admitted in 2003, interviewed on average four
  months after admission. Employment and earnings are measured at the very start of the US
  career and say nothing about trajectories. Sponsored spouses, refugees and diversity winners
  enter with different rights to work, which the class-of-admission control absorbs only
  crudely.
- **2003–2004 dollars**, PPP-adjusted to US current prices by the data producers. Not deflated
  to any later year.
- **Self-reported religion**, first tradition mentioned. 417 adults refused, did not know or
  were not asked. Denomination (`J33_1MO`) is released only as a string and is blank for 87%
  of the sample, so Sunni and Shia could not be separated: 62 and 18 cases respectively.
- **Small cells.** Every Jewish earnings cell (n = 42 and 37) is suppressed under G5. Buddhist
  and Other earnings cells are just over the line at 93 and 82 and their intervals are wide.
- **Origin is masked.** The public file names 21 countries and folds the rest into 7 world
  regions, so Pakistan and Bangladesh sit inside "East Asia, South Asia and the Pacific" with
  China and India. Origin controls are therefore coarser for Muslim respondents than for
  Hindu or Catholic ones, which cuts against the adjusted Muslim gap being an artefact of
  under-controlling and in favour of it, depending on the direction of within-region sorting.
  This is a real limit on the origin specification, not a solved problem.
- **No design variance.** The public file carries no PSU identifier, so all standard errors
  are a 500-draw respondent bootstrap stratified on the 32 stratum-by-replicate design cells,
  not Taylor linearisation. They will understate variance to the extent the sample is
  clustered within MSAs and counties.
- **Descriptive, not causal.** Religion here proxies origin, language, visa route and
  selection at once. Nothing in this lane identifies an effect of religion.

## Files

Written: `analysis.py`, `test_analysis.py`, `README.md`, `RESULT.md`,
`derived/anchors.csv`, `derived/religion_cells.csv`, `derived/earnings_gaps.csv`,
`derived/audit.json`, `.gitignore`. Not modified: `BRIEF.md`.

Skipped: **means-tested program use**, which the brief listed as optional. Sections G and I
carry SSI (`G59`–`G62`) and other transfer receipt, but they are administered to the
household's financial respondent, so a group-level rate would carry the same universe problem
as `any_wage_12m` at a far lower base rate; it was left out rather than reported unqualified.
**Denomination detail** within Islam and Christianity, for the cell sizes given above.
**Taylor-linearised standard errors**, for want of a PSU identifier in the public tier.

## Verification

```
$ uv run --no-project python3 -m pytest infra/immigration-fiscal/nis2003_religion_earnings_2026_09_22/ -q
........................                                                 [100%]
24 passed in 1.23s
```

```
$ OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/nis2003_religion_earnings_2026_09_22/analysis.py
gate G1: verifying source zip sha256
  G1 PASS 61a6e3d58d79f6522bfe1deda84d287aa53960d46b5e97fbee265b010b9885c1
loading datasets (gate G2)
  G2 PASS: 8573 adults, unique PU_ID, in 8 adult datasets
gate G3: reproducing published counts
  anchors exact: 19/26
    [PASS] completed adult interviews (weights Table 1): published=8573.0 reproduced=8573.0
    [PASS] distinct design weights reconstructed from Table 1: published=32.0 reproduced=32.0
    [PASS] max |NISWGTSAMP1 - documented design weight|: published=0.0 reproduced=4.796163466380676e-14
    [PASS] share adjusting status (weighted): published=0.57 reproduced=0.5738
    [near] completed cases, stratum 1 (Spouse of U.S. Citizen): published=1427.0 reproduced=1428.0
    [near] home ownership, ages 25-64 at admission, Spouse of U.S. Citizen: published=0.406 reproduced=0.3742
wrote derived/religion_cells.csv
model A_christian_ref: reference=Christian groups=['Buddhist', 'Christian', 'Hindu', 'Jewish', 'Muslim', 'No religion', 'Other']
model B_catholic_ref: reference=Catholic groups=['Buddhist', 'Catholic', 'Hindu', 'Jewish', 'Muslim', 'No religion', 'Orthodox', 'Other', 'Protestant']
wrote derived/earnings_gaps.csv
  G5: 246 reported cells (n>=50, finite SE); 18 suppressed
wrote derived/audit.json
--- headline ---
  emp_rate: Christian=0.6110(0.0082;n=4921)  Muslim=0.5073(0.0252;n=606)  Hindu=0.5461(0.0260;n=585)
  empgap_adj: Muslim=-0.0225(0.0243;n=606)  Hindu=-0.0627(0.0280;n=585)
  empgap_adj_origin: Muslim=-0.0079(0.0261;n=606)  Hindu=0.0015(0.0364;n=585)
  loggap_earnC_unadj: Muslim=0.1225(0.0804;n=231)  Hindu=0.4878(0.1506;n=272)
  loggap_earnC_adj: Muslim=0.0508(0.0721;n=231)  Hindu=-0.0544(0.1374;n=272)
  loggap_earnC_adj_origin: Muslim=0.0399(0.0795;n=231)  Hindu=-0.2061(0.1824;n=272)
  loggap_wageG_adj: Muslim=-0.0823(0.0994;n=254)  Hindu=0.1125(0.1233;n=280)
```

The analysis run is trimmed above for width; the full 26-anchor listing and all seven religion
groups per statistic are in `derived/anchors.csv` and `derived/earnings_gaps.csv`.
