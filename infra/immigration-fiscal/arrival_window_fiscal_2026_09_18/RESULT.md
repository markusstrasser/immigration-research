claude-opus-5[1m]

**Verdict:** The Mexico-born fiscal account by arrival window is **age structure first, cohort quality second**. On the raw (partial) account the most recent arrivals look *best* — the 2016-2025 window is **+$3,495 per person per year**, the only clearly positive window — but that is because 72.5% of them are aged 18-54 and only 3.2% are 65+. Once age is held fixed on the common-age standard the same window is **−$3,978 per standardized person versus third-plus non-Hispanic white**, still the least negative of the five, with the older windows clustered at −$4,800 to −$5,300. Under the complete account (adding the four flat central charges) **every window is negative per person**, from −$9,288 (pre-1990) to −$2,318 (2016-2025). The cohort trend is **improving in point estimate and flat in evidence**: the first difference turns positive after the 1990s window and grows to +$847 per window, but its standard error is +/-1,575, so **no adjacent-window change reaches one standard error** and the second derivative (+$403 to +$423, SE 1,268-2,451) carries no information at all.

[DATA] [INFERENCE] — CPS ASEC 2025 (income year 2024) and MEPS HC-256, via the held lanes. Model-based charges, not observed receipts.

Lane: `infra/immigration-fiscal/arrival_window_fiscal_2026_09_18/`
Script: `arrival_window_ledger.py` · Outputs: `derived/*.csv`, `derived/audit.json`

---

## 1. Commands

```sh
cd /Users/alien/Projects/immigration-research
OPENBLAS_NUM_THREADS=1 uv run --no-project --with "numpy>=2" --with "pandas>=2" --with "openpyxl" \
  python3 infra/immigration-fiscal/arrival_window_fiscal_2026_09_18/arrival_window_ledger.py
```

The bare form in the brief (`uv run --no-project python3 ...`) needs the three `--with`
wheels because this repo has no `pyproject`; `openpyxl` is required by the absolute lane's
cached Census/OMB workbooks. `--skip-complete` drops section 5 and its dependency.

Run tail:

```
[complete] charge columns used: ['G|deflated2024', 'K|central', 'X|per_capita', 'R|central']; dropped items: ['S(states without a verified line)']
[gate 1] window populations reproduce the Mexico-born cell: max |diff| = 0.000000 people, 0.000051 dollars -> PASS
[support] common support across all windows: ['35-44', '45-54', '55-64', '65-74', '75+'] (0.617 of the white age standard)
[gate 2] union absolute +6.62935bn vs stored +6.62935bn (residual $0.0000); union common-age gap -6,561.712 vs stored -6,561.712 (residual $0.0000) -> PASS
[gate 3] charge columns vs ledger_absolute items_by_group: -76.0694bn vs -76.0694bn; gap +978.226 vs +978.226 -> PASS
[asec2026] not repeated: KeyError: "There is no item named 'pppub25.csv' in the archive"
PASS: 96 estimates, gates 1-2 passed, 96/96 finite standard errors
```

## 2. The PEINUSYR code list and the windows

`PEINUSYR`, "When did you come to the U.S. to stay?", person record position 133, length 2.
Transcribed from the held documentation, `cpsmar25.pdf` p. 41
(`/Users/alien/research-data/immigration-fiscal/data/external/cps_asec_doc/cpsmar25.pdf`):

```
00 = NIU        01 = Before 1950  02 = 1950-1959  03 = 1960-1964
04 = 1965-1969  05 = 1970-1974    06 = 1975-1979  07 = 1980-1981
08 = 1982-1983  09 = 1984-1985    10 = 1986-1987  11 = 1988-1989
12 = 1990-1991  13 = 1992-1993    14 = 1994-1995  15 = 1996-1997
16 = 1998-1999  17 = 2000-2001    18 = 2002-2003  19 = 2004-2005
20 = 2006-2007  21 = 2008-2009    22 = 2010-2011  23 = 2012-2013
24 = 2014-2015  25 = 2016-2017    26 = 2018-2019  27 = 2020-2021
28 = 2022-2025
```

Two documentation notes. The layout page prints a stale range `(0:26)` above a value list
that runs to 28; the file's observed maximum is 28, so the value list governs. And the top
code reads **2022-2025**, not "2022-2024" as the in-repo comment at
`build/analyze_cps_fiscal_2025.py:166` says — the March 2025 interview can record an arrival
earlier in 2025. **The most recent window therefore spans calendar 2016 through the
February-April 2025 interview date, about nine years and two months, not eight.**

Every window boundary falls between two codes, so no code is split:

| window | codes | span | records | weighted population | mean age | share under 18 |
|---|---|---|---|---|---|---|
| `w1_pre1990` | 1-11 | before 1950 through 1989 | 1,403 | 2,939,241 | 61.3 | 0.000 |
| `w2_1990_1999` | 12-16 | 1990 through 1999 | 1,236 | 2,622,621 | 49.7 | 0.000 |
| `w3_2000_2009` | 17-21 | 2000 through 2009 | 1,503 | 3,281,865 | 43.1 | 0.005 |
| `w4_2010_2015` | 22-24 | 2010 through 2015 | 437 | 983,891 | 39.3 | 0.095 |
| `w5_2016_2025` | 25-28 | 2016 through the March 2025 interview | 1,052 | 2,393,164 | 32.4 | 0.182 |
| **union** | 1-28 | | **5,631** | **12,220,782** | 46.5 | 0.045 |

No Mexico-born civilian record carries code 0 (NIU), so the partition is exhaustive without
an "unknown" residual. Reporting domain, group definition, components and bands are the
all-age lane's unchanged: civilian household population, `PRCITSHP` 4/5 with `PENATVTY` 303,
`all_age_shared` scenario, eight bands, full plus 160 replicate weights.

## 3. Absolute partial balance, and why it inverts

| window | absolute $bn | SE $bn | per person | SE |
|---|---|---|---|---|
| `w1_pre1990` | −8.03 | 2.47 | **−2,730** | 831 |
| `w2_1990_1999` | +3.24 | 1.69 | **+1,235** | 640 |
| `w3_2000_2009` | +3.46 | 1.44 | **+1,054** | 438 |
| `w4_2010_2015` | −0.41 | 0.66 | **−415** | 672 |
| `w5_2016_2025` | +8.36 | 2.21 | **+3,495** | 926 |
| union | +6.63 | 5.36 | +542 | 439 |

The ordering here is an age artefact and should not be read as cohort quality. Band
populations (`derived/window_age_profiles.csv`) show why: the pre-1990 window holds 1.14m
people aged 65+ out of 2.94m, the 2016-2025 window holds 0.077m out of 2.39m. The 2010-2015
window is the odd one out on sample as well — 437 records, the thinnest of the five, and its
standard errors are correspondingly the least informative per dollar of estimate.

## 4. Age-held-fixed: common-age gap and age-matched gap

Two standardisations are reported, because the windows do not share an age support. A person
who arrived before 1990 cannot be under 18 in 2025, so bands 0-17, 18-24 and 25-34 are
**structurally empty** for `w1`, and 0-17 and 18-24 for `w2`. The upstream `sufficient`
refuses an empty band; this lane uses a sparse variant and two explicit supports:

- **common support** (primary, comparable across windows): bands 35-44 through 75+, carrying
  **61.7%** of the white age standard, renormalised to 1. Every window is populated in all
  five bands in all 161 weight vectors.
- **window support** (secondary, not comparable across windows): each window's own populated
  bands, renormalised. For `w3`-`w5` and the union this is the full eight-band standard and
  reproduces the published number exactly.

Common-age gap per standardized person, **common support**:

| window | vs third-plus NH white | SE | vs all natives | SE |
|---|---|---|---|---|
| `w1_pre1990` | −4,901 | 753 | −3,886 | 726 |
| `w2_1990_1999` | −5,296 | 809 | −4,281 | 790 |
| `w3_2000_2009` | −5,268 | 983 | −4,253 | 969 |
| `w4_2010_2015` | −4,824 | 1,199 | −3,810 | 1,185 |
| `w5_2016_2025` | **−3,978** | 1,247 | **−2,963** | 1,226 |
| union | −5,360 | 676 | −4,345 | 651 |

Common-age gap on each window's **own** support (levels not comparable between rows, because
the standard mass differs; shown so the `w3`-`w5` full-standard values are on the record):

| window | standard mass | vs white | SE |
|---|---|---|---|
| `w1_pre1990` | 0.617 | −4,901 | 753 |
| `w2_1990_1999` | 0.692 | −5,798 | 771 |
| `w3_2000_2009` | 1.000 | −7,068 | 718 |
| `w4_2010_2015` | 1.000 | −7,538 | 856 |
| `w5_2016_2025` | 1.000 | −5,108 | 916 |
| union | 1.000 | −6,562 | 502 |

Age-matched gap in dollars:

| window | vs white $bn | SE | vs all natives $bn | SE |
|---|---|---|---|---|
| `w1_pre1990` | −14.52 | 2.68 | −11.18 | 2.56 |
| `w2_1990_1999` | −25.00 | 2.06 | −21.30 | 1.93 |
| `w3_2000_2009` | −35.42 | 2.24 | −30.48 | 2.04 |
| `w4_2010_2015` | −10.80 | 1.08 | −9.18 | 0.97 |
| `w5_2016_2025` | −17.36 | 2.51 | −13.02 | 2.36 |
| union | −103.10 | 6.80 | −85.16 | 6.31 |

The union row reproduces the published `−103.10bn` and `−6,562` exactly (gate 2).

### Component split of the age-matched gap vs white, $bn

| component | w1 | w2 | w3 | w4 | w5 | union |
|---|---|---|---|---|---|---|
| tax | −22.85 | −24.87 | −32.11 | −9.35 | −16.68 | −105.86 |
| employer payroll | −2.41 | −3.85 | −5.33 | −1.56 | −3.08 | −16.24 |
| sales | −1.24 | −1.27 | −1.58 | −0.46 | −0.83 | −5.37 |
| owner property | −2.62 | −2.31 | −2.64 | −0.81 | −1.87 | −10.25 |
| **tax side** | **−29.12** | **−32.30** | **−41.66** | **−12.18** | **−22.46** | **−137.72** |
| cash transfers | +14.36 | +6.60 | +6.07 | +1.87 | +3.57 | +32.46 |
| noncash | −0.20 | −0.29 | −0.51 | −0.15 | −0.18 | −1.31 |
| K-12 school | −1.30 | −1.23 | −2.41 | −1.19 | −0.29 | −6.42 |
| school lunch | +0.12 | +0.16 | +0.26 | +0.07 | +0.13 | +0.74 |
| medical | +1.63 | +2.06 | +2.83 | +0.76 | +1.88 | +9.15 |
| **benefit side** | **+14.61** | **+7.30** | **+6.24** | **+1.36** | **+5.11** | **+34.62** |

This is the sharpest cohort-invariant finding in the lane: **in every one of the five windows
the benefit side is a net fiscal plus and the entire deficit is tax side.** Age-matched
Mexico-born residents draw *less* in cash transfers and cost *less* in public medical than
the white reference in all five windows; they pay less tax. The signs never flip by cohort.
Cash dominates the benefit side in the older windows (Social Security), and the tax
shortfall in `w3` (−41.66bn) is both the largest window and the largest population.

## 5. Per-band balance per person, partial account

| band | w1 | w2 | w3 | w4 | w5 | union |
|---|---|---|---|---|---|---|
| 0-17 | — | — | −4,832 | −7,299 | −2,809 | −3,639 |
| 18-24 | — | — | +2,235 | −741 | +4,495 | +2,813 |
| 25-34 | — | +6,616 | +3,507 | +3,004 | +8,555 | +5,972 |
| 35-44 | +1,051 | +1,009 | +660 | +132 | +3,410 | +1,240 |
| 45-54 | +5,683 | +2,717 | +1,331 | +1,995 | +5,075 | +3,045 |
| 55-64 | +4,068 | +2,137 | +1,705 | −2,376 | +1,302 | +2,667 |
| 65-74 | −12,325 | −11,718 | −10,140 | −7,310 | −11,241 | −11,848 |
| 75+ | −16,320 | −13,353 | −12,601 | −8,111 | −10,549 | −14,982 |

Dashes are structurally empty bands, not missing data. The 2016-2025 window is the strongest
window at *every* working-age band it occupies, which is the part of the picture the absolute
column in section 3 exaggerates and the common-age column in section 4 understates.

## 6. Complete account: the four flat central charges

Added: `G|deflated2024` (state-local general services, per capita by state),
`K|central` (K-12 capital outlay and interest on school debt, per pupil),
`X|per_capita` (federal and state excise credit), `R|central` (rest of the federal
budget by function, per-capita part). These are **recomputed**, not read back: the lane
imports `ledger_absolute_2026_09_17.build_charges` and calls it against that lane's verified
`params/params.json`, then selects the four central-arm columns. Gate 3 confirms the four
columns reproduce that lane's own `items_by_group.csv` for `mexico_born` to the cent
(−$76.0694bn, +$978.226 on the common-age gap).

Item F (defence, net interest, general government) is **not** included: the brief does not
list it and its central arm is zero anyway. Items P, D, U, I, M, N, E, C and S are not
included, so these numbers are **not** the absolute lane's headline complete account
(`−7,783` vs white on the full standard); they are the partial account plus four flat items.

| window | complete $bn | complete per person | SE | complete common-age gap vs white (common support) | SE |
|---|---|---|---|---|---|
| `w1_pre1990` | −27.30 | **−9,288** | 861 | −3,523 | 786 |
| `w2_1990_1999` | −13.15 | **−5,015** | 644 | −3,498 | 826 |
| `w3_2000_2009` | −16.82 | **−5,124** | 445 | −3,350 | 985 |
| `w4_2010_2015` | −6.62 | **−6,732** | 691 | −3,164 | 1,123 |
| `w5_2016_2025` | −5.55 | **−2,318** | 946 | −1,809 | 1,258 |
| union | −69.44 | −5,682 | 442 | −5,584 (full standard) | 513 |

Adding flat per-capita charges cannot change a relative gap except through the age-weighted
population ratios, which is why the complete common-age gaps compress toward each other while
the absolute per-person figures spread apart.

## 7. Derivative view, common support, partial account vs white

| order | later | earlier | estimate | SE | SE ratio |
|---|---|---|---|---|---|
| 1st | w2 1990s | w1 pre-1990 | **−395** | 631 | 0.63 |
| 1st | w3 2000s | w2 1990s | **+28** | 898 | 0.03 |
| 1st | w4 2010-15 | w3 2000s | **+444** | 1,187 | 0.37 |
| 1st | w5 2016-25 | w4 2010-15 | **+847** | 1,575 | 0.54 |
| 2nd | w3 | w1 | +423 | 1,268 | 0.33 |
| 2nd | w4 | w2 | +415 | 1,785 | 0.23 |
| 2nd | w5 | w3 | +403 | 2,451 | 0.16 |

Same table, complete account vs white: first differences +25, +147, +186, +1,355
(SEs 649, 892, 1,106, 1,537); second differences +122, +39, +1,169.

**Plain statement.** On point estimates the trend is *worsening once, then improving three
times*: the 1990s cohort is $395 worse than the pre-1990 cohort, and every window after that
is better than the one before it, by +28, +444 and +847. The improvement is monotone in
magnitude, which is what an accelerating improvement looks like. **The evidence does not
support either claim.** No first difference reaches one standard error; the largest,
+847, is 0.54 SE. Every second difference is under 0.35 SE and the three are nearly
identical (+403 to +423), which is the signature of a linear fit through noise, not of
curvature. The honest reading: **the cohort series is statistically flat, with a point
estimate that leans improving and a most-recent window that is the best of the five on every
age-held-fixed measure.** A cohort effect and a duration effect are also not separated here
(section 9).

## 8. Omitted dependants

The US-born children of a window's arrivals are **not in the window**. They are CPS natives
and sit in the `mexican_second_gen` group of the all-age lane, whose common-age gap versus
white is a separate published estimate. Own children under 18 are linked through the CPS
parent pointers `PEPAR1`/`PEPAR2` against each adult's `A_LINENO` within the household:

| window | adults 18+ | own children <18 per adult | linked children | of which US-born |
|---|---|---|---|---|
| `w1_pre1990` | 2,939,241 | 0.263 | 721,249 | 96.6% |
| `w2_1990_1999` | 2,622,621 | 0.691 | 1,687,102 | 96.9% |
| `w3_2000_2009` | 3,264,807 | 0.871 | 2,375,877 | 95.9% |
| `w4_2010_2015` | 890,708 | 0.862 | 724,669 | 91.1% |
| `w5_2016_2025` | 1,957,422 | 0.652 | 1,023,176 | 66.6% |
| union | 11,674,799 | 0.640 | 5,560,310 | 91.2% |

Roughly 5.1m US-born minor children of Mexico-born adults are charged to the second
generation rather than to any window. The 2016-2025 window is the exception to the pattern in
kind as well as in degree: a third of its linked children are themselves foreign-born and so
*are* inside the window's own population and its account. Counts are distinct children within
each window; a child whose two parents arrived in different windows appears in both, which is
why the window counts sum above the union.

## 9. What this does not establish

- **Cohort and duration are confounded by construction.** A window is simultaneously "who
  arrived then" and "how long they have been here". Section 7's derivative is the sum of both
  and cannot attribute to either. The one-year duration derivative that would separate them
  is blocked (section 10).
- **Cross-sectional, not longitudinal.** The pre-1990 window is who *remains* in 2025;
  return migration, mortality and naturalisation-driven attrition all select it.
- **The common support carries 61.7% of the white age standard.** The five-window comparison
  is a comparison over ages 35 and up, not over the whole life course.
- Everything the all-age lane's own caveats cover carries: modelled rates rather than
  receipts, sales and property proxies, the K-12 attendance ratio, the CPS-MEPS additive
  variance approximation, the ASEC-MEPS age alignment.
- Intervals are pointwise normal 95% intervals conditional on fixed age-standard shares and
  model parameters. The tables above quote one standard error.

## 10. ASEC 2026 (income year 2025) — NOT DONE, blocked

The brief's `sources/.../cps_asec_2026/asecpub26csv.zip` does not exist. A copy is held at
`infra/immigration-fiscal/ledger_asec2026_2026_09_16/_cache/asecpub26csv.zip`. `ext.build`
was called on it and **refused**:

```
KeyError: "There is no item named 'pppub25.csv' in the archive"
```

Members are `hhpub26.csv`, `ffpub26.csv`, `pppub26.csv`, `asec_csv_repwgt_2026.csv`. The
upstream `prepare()` opens the 2025 filenames literally. Three further barriers sit behind
that one, all documented by the `ledger_asec2026` lane: `SPM_BBSUBVAL` is absent from the
2026 file, `state_parameters.csv` is a 2024-vintage file, and `PEINUSYR` gains code 29 on the
2026 layout (28 recodes to 2022-2023, 29 = 2024-2026), which would split the most recent
window differently and which `build/analyze_cps_fiscal_2025.py:155` fails loud on by design.
Repeating section 4 on income year 2025 is a real port of the builder, not a file swap.
**The duration derivative at fixed cohort is therefore not reported.**

## 11. Gates

| gate | result |
|---|---|
| windows partition the Mexico-born group (records) | PASS, exact |
| window populations reproduce the Mexico-born cell | PASS, max diff 0.000000 people (12,220,781.88 total) |
| window dollars reproduce the Mexico-born cell | PASS, max diff $0.000051 |
| union absolute vs stored `+6.629355bn` | PASS, residual $0.0000 |
| union common-age gap vs stored `−6,561.712` | PASS, residual $0.0000 |
| four charge columns vs `ledger_absolute` items | PASS, −$76.0694bn and +$978.226 both exact |
| component split sums to each age-matched gap | PASS, all 12 target/reference pairs within $0.02 |
| standard errors finite | PASS, 96/96 |

Standard errors reproduce the published lane exactly where they overlap: union
`absolute_total` SE $5.360bn, `standardized_gap_per_person` SE 501.5, `age_band gap_total`
SE $6.802bn, all matching `all_age_ledger_2026_09_17/derived/estimates.csv`.

## 12. Files

| file | contents |
|---|---|
| `derived/window_estimates.csv` | 96 estimates: absolute, common-age (both supports), age-matched, partial and complete, both references, with `se_cps`/`se_meps`/`se_joint` and 95% intervals |
| `derived/window_component_gaps.csv` | nine-component split of each age-matched gap |
| `derived/window_age_profiles.csv` | per-band population and balance per person, partial and complete |
| `derived/window_derivatives.csv` | levels, first and second differences with replicate SEs |
| `derived/window_descriptives.csv` | codes, span, populations, mean age, own children per adult |
| `derived/audit.json` | input hashes, the PEINUSYR code list, window definitions, supports, gate residuals, charge provenance, the ASEC 2026 failure |
