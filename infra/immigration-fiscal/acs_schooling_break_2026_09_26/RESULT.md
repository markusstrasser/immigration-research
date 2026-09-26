**Verdict:** Six lanes read ACS or IPUMS USA schooling in a way the 2020 no-schooling step
reaches (one of them, `dataset_integrity`, only to diagnose it); no headline reverses sign or
conclusion. The largest effects are in
`schooling_selection_position` (the 2020–23 cohort's bottom-tail excess over Mexico falls from
+0.048 to +0.027–0.029, and its "both tails" label holds), `arrival_cohorts` (the 2000→2023 gain
in mean years falls from 2.37 to 2.22–2.27 against INEGI's 2.20), the Borjas panel in `build/`
(the 2023 immigrant share below high school rises from 40.8% to 41.8–41.9%) and the
`scale_spillovers` innovation arm, which is not added (patents move from −$24bn to +$37–57bn inside
a ±$490bn interval). Three premises of the brief do not hold. Grade 9 feeds the step. A "grade 8
or less" band is not continuous once its trend is removed. Natives aged 20–64 are affected
(+30%). The Census Bureau documents over-reporting of "no schooling" in self-response and changes
the question in the 2025 ACS, which creates a second break.

Lane: `acs_schooling_break_2026_09_26`, 2026-09-26, from `BRIEF.md`. Numbers are tagged
`[DATA]` (read from a file), `[CALCULATION]` (computed here, script named) or `[SOURCE]`.

## Lane table

Corrections: **A** is the brief's method: the level excess since 2019, returned to the same
group's 2019 distribution over grades 1–8. **B** is the flow-rate method, preferred (§3). Each
"corrected" cell shows A / B.

| Lane | Exposed | Reason | Headline affected | Old | Corrected (A / B) | Conclusion changes? |
|---|---|---|---|---|---|---|
| `schooling_selection_position_2026_09_23` | **yes** | ranks within Mexico's distribution; C1/C2/C3 cuts below grade 9; 2024 ACS row; 2019→2024 survivor comparison | 2020–23 cohort: ridit; C1 gap vs Mexico (SE) | 0.540; +0.048 (0.006) | 0.543 / 0.545; +0.029 (0.005) / +0.027 (0.005) | no: "middle" and "both tails" hold; bottom excess −40% |
| same | yes | same | Table 4, 2024-ACS row: post-2010 minus 2000–09 cohorts | 0.049–0.068 | 0.046–0.062 / 0.046–0.063 | no |
| same | yes | same | survivor drift 2019→2024 | −0.040 to +0.018 | −0.011 to +0.026 / −0.021 to +0.026 | confirms the lane's reading that the fall is the break |
| same | yes | same | 2020–23 undercount k for ridit 0.5; for C1 = Mexico | 1.77; 0.54 | 2.03 / 2.08; 0.67 / 0.69 | no |
| same | yes | same | 2015–19 cohort in the 2020 and 2021 ACS: women's tails label; 2020–23 in the 2023 ACS: women's C1 gap | both tails; +0.018 | top in both rows; +0.002 / +0.001 (label stays) | yes, for these alternative rows only |
| `arrival_cohorts_2026_09_18` (`origin_relative.py`) | **yes** | scores years (EDUC → 2.5/6.5/9…); 2023 ACS vs 2000 census; drops EDUC 0 | entry-cohort mean-years gain 2000→2023, against INEGI's +2.20 | +2.37 (excess +0.17) | +2.22 / +2.27 (excess +0.02 / +0.07) | no: "the origin moved just as fast" is strengthened |
| `arrival_cohorts` (other scripts) | no | `EDUC` ≤ 5 / `SCHL` ≤ 15 bands, BA+ | — | — | — | — |
| `build/build_borjas_supply_shock_panel.py` | **yes** | `EDUC BETWEEN 1 AND 11` drops no-schooling; 2023 vs 1980–2010 | immigrant share of 18–64 below high school, 2023 | 40.8% | 41.9% / 41.8% | no: the rise to 2023 is larger (+3.9–4.0 pp from 2010, not +2.9) |
| `build/build_tier_a_context_panels.py` | yes, unused | `SCHL` < 12 cut; SCHL code used as years in experience; 2023 only | cells `borjas_supply_shock_cell_2023.csv`, `bgh_outcomes_cell_2023.csv` | not sized | — | no consumer ("structure anchor only") |
| other `build/` scripts | no | `SCHL` < 16 / `EDUC` bands, SIPP, CPS | 2019→2024 recent-arrival below-HS 16.8% → 18.7% | — | — | no: below-diploma band steps ≤0.4 pp |
| `scale_spillovers_2026_09_23` | **yes** (side specs) | scores years on ACS 2024; innovation arm compares with a pre-2020 mean | central scale + composition | +$13.9bn | unchanged (coarse bands) | no |
| same | yes | same | workers' dYRS; average-schooling specs | 0.255; −$47bn to +$28bn | — / 0.247; about −$45bn to +$27bn | no |
| same | yes | same | Mexico-born 25+ mean years; innovation arm, patents; wages | 9.71; −$24.1bn; +$50.3bn | 9.96 / 9.90; +$57.0bn / +$36.8bn; +$115.9bn / +$99.5bn | point sign flips for patents inside a ±$490bn interval; arm stays "not measurable, not added" |
| `return_vs_us_stayers_2026_09_26` | yes (source) | scores years; 2023 ACS | men's 2023 mean-years gap, returnees minus stayers | −0.75 | spec (e) −1.00 / B ≈ −0.92 | no |
| `dataset_integrity_2026_09_23` | diagnostic | measures the break by design (`acs_break_lths`, `acs_noschool_break`) | F6: "natives unaffected"; "no effect at or above HS" | — | natives 20–64 +0.20 pp; grade 9 feeds the step | F6 wording; no dollar item |
| `crime_selection_cohorts_2026_09_23` | no | none through grade 11 is one band (`cohort_lib.py:26`, `acs_reference.py:40`) | — | — | — | — |
| `compliance_gap_2026_09_24` | no | `EDUC` ≤ 6 / ≤ 9 flags (`acs_cells.py:57-58`) | — | — | — | — |
| `service_by_ses_2026_09_23` | no | `SCHL` ≤ 15 / ≤ 17 / ≤ 20 (`service.py:77`) | — | — | — | — |
| `labor_mobility_insurance_2026_09_23` | no | `SCHL` ≤ 17 (`acs_extract.py:107`) | — | — | — | — |
| `high_skill_origin_screen_2026_09_21`, `admission_route_2026_09_21` | no | `SCHL` 21–24 only | — | — | — | — |
| `indian_generation_2026_09_21`, `indian_ledger_2026_09_18` | no | BA+/graduate/HS-or-less; CPS elsewhere | — | — | — | — |
| `housing_supply_ca_tx_2026_09_22`, `tiebout_sorting_2026_09_18` | no | BA+ only (`analysis.py:442`; `analyze_state.py:141`) | — | — | — | — |
| `employment_entry_2026_09_18`, `displacement_transfers_2026_09_18` | no | below-BA filter `SCHL` 1–20 | — | — | — | — |
| `unauthorized_population_size_2026_09_19` | no | `SCHL` extracted, never used | — | — | — | — |
| `school_dilution_2026_09_24`, `school_cost_where_enrolled_2026_09_24`, `ledger_absolute_2026_09_17`, `external_benchmarks_2026_09_24`, `movers_reasons_2026_09_24` | no | no ACS/IPUMS attainment (enrollment, finance or CPS only) | — | — | — | — |
| outside the brief's list | no | coarse bands, CPS, BA+ only or no schooling: `projection_backtest` (`EDUCD` < 62), `figures` (arrival below-HS series), `care_household_services`, `consumer_price_benefit`, `construction_housing_supply`, `institutional_education`, `civic_service_by_ancestry`, `mr_leads_papers`, `cultural_output`, `ancestry_iv_congestion_wages` (no 2020+), `hedonic_composition`, `native_fertility`, CPS lanes, no-schooling lanes | — | — | — | — |

"Old" values are [DATA] from each lane's published `derived/` files, and each fix script's
positive control reproduces them. "Corrected" values are [CALCULATION] from this lane's `derived/`
files, named in §4. Every "no" row was cleared by reading the mapping line cited here or in the fact sheets
`triage_b.md` and `triage_extra.md`. Two read-only sub-agents wrote those sheets. The lines of
every exposed or borderline lane were re-read here. [DATA: the cited files]

## 1. What the break is (measured here)

`break_anatomy.py` reads the Census 1-year PUMS person files for 2017–2019 and 2021–2024. It
uses the unrecoded slim copies in `dataset_integrity_2026_09_23/_cache/`, with sha256 pinned. For
each schooling category it fits `share = a + b·(year − 2019) + c·1[year ≥ 2021]`, where `c` is the
step. It uses two universes: persons aged 20–64, and a fixed population whose attainment cannot
change (born 1955–1987, households only, foreign-born arrived by 2009).
[CALCULATION: `derived/break_steps.csv`]

| Step, pp (20–64 / fixed) | No schooling | Grades 1–8 | Grade 9 | Grade 8 or less, incl. none | Below diploma (`SCHL` ≤ 15) |
|---|---:|---:|---:|---:|---:|
| Mexico-born | +2.85 / +3.00 | −1.87 / −2.22 | −1.26 / −1.05 | +0.98 / +0.78 | +0.42 / +0.33 |
| Other Latin America-born, Hispanic | +2.39 / +2.56 | −1.50 / −2.56 | −0.71 / −0.70 | +0.88 / 0.00 | +0.35 / −0.02 |
| Non-Hispanic foreign-born | +0.79 / +0.52 | −0.30 / −0.22 | −0.07 / −0.04 | +0.49 / +0.30 | +0.36 / +0.15 |
| US-born | +0.20 / +0.21 | −0.05 / −0.07 | −0.06 / −0.04 | +0.15 / +0.13 | −0.09 / −0.10 |
| US-born aged 65+ (one universe) | +0.10 | −0.34 | −0.17 | −0.24 | −0.83 |

- **Grade 9 feeds the step.** In the fixed Mexico-born population the extra "none" reports
  (+3.00) are matched by losses at grade 6 (−2.01), grade 9 (−1.05), grades 7–8 (−0.54) and
  grades 1–4 (−0.27). Grade 5 and preschool gain +0.60. Of the gross losses, 50% are at grade 6
  and 26% at grade 9, the two Mexican completion levels (primaria, secundaria).
- **"Grade 8 or less" is not continuous** once its trend is removed. The raw 29.22% → 29.00%
  (2019 → 2021) hides a decline of about 0.8 pp a year. The band steps up +0.8 to +1.0 pp for the
  Mexico-born and +0.13 to +0.15 pp for the US-born (9% of its level).
- **Natives aged 20–64 are affected**: +0.20 pp on a 0.66% base. For them the extra reports come
  from grade 9 and above, not from grades 1–8. F6 in `dataset_integrity_2026_09_23/acs.md`
  ("natives 65+ stay at 0.8–0.9%") holds only at 65+ (+0.10 pp).
- **A drift outside the step.** The fixed Mexico-born population's "none" share also rises
  0.40 pp a year before and after 2020 (5.59% in 2017, 6.36% in 2019; 10.20% in 2021, 11.46% in
  2024). The same people cannot lose schooling, so reporting drifts even without the step.
  Correcting "to 2019" is therefore a normalization to the 2019 instrument, not to the truth.
- **12th grade without a diploma steps too**: +0.68 to +0.74 pp for the Mexico-born and +0.3 pp
  for US-born Black adults. That is why the below-diploma band moves by +0.3 to +0.4 pp. Coarse
  bands stay within about 0.4 pp, as the brief assumed.

## 2. Cause: what the Census Bureau documents

One search pass covered Census user notes and errata, the Design and Methodology report, the
Federal Register and the 2022 Content Test reports. It found no user note or erratum about a 2020
change to the education item or its edits. It found:

- ACS Design and Methodology v4.0 (2024), ch. 5, §5.10 [SOURCE:
  https://www2.census.gov/programs-surveys/acs/methodology/design_and_methodology/2024/acs_design_methodology_ch05_2024.pdf;
  the same text is in Federal Register 2022-05937 and 2023-23249]:
  - "A relatively high percentage of respondents are selecting the response category, 'No
    schooling completed.' Ongoing research suggests that this includes adults who have completed
    some level of schooling."
  - The Bureau "will implement these changes on the 2025 ACS."
- McElrath, Fabina, Martin, Oliver & Gilmartin, *2022 ACS Content Test Evaluation Report:
  Educational Attainment*, ACS23-RER-10, 15 Nov 2023 [SOURCE:
  https://www.census.gov/content/dam/Census/library/working-papers/2023/acs/2023_McElrath_01.pdf,
  read from the Wayback Machine copy because census.gov did not resolve locally]:
  - In 2016, 2.26% of persons 25+ who answered by mail chose "No schooling completed", and 1.22%
    by internet. By CAPI the figure was 0.85%, and by CATI 0.65%.
  - A header added in 2008 raised the rate.
  - The 2025 question merges none, nursery and kindergarten into "Less than grade 1". In the test
    that category was 1.5% on the old question and 0.6% on the new; the CPS benchmark is 0.3%.
  - The new question also moves "high school graduate" (−1.3 pp; −4.3 pp in CAPI) and "some
    college, no diploma" (+2.1 pp).

The Bureau's documented mechanism is misreporting in self-response. The report does not mention
the 2020 step. A lasting post-2020 shift of low-schooled immigrant households from interviewer
modes to mail and internet would produce it, but PUMS has no mode variable, so this is untested
[INFERENCE]. **The 2025 ACS carries a second, deliberate break in the same item and in the
diploma and some-college categories.** No lane reads 2025 ACS data yet (rg, 2026-09-26).

## 3. Correction methods

`breakfix.py` holds both methods.

- **A (the brief's)** takes the excess share φ = 1 − share₂₀₁₉ / shareₜ of a group's "none"
  reports and returns it to that group's 2019 distribution over grades 1–8. It is the return
  lane's spec (e) with the grade-1–8 destination the brief asks for.
- **B (flow rates, preferred).** In each fixed population (Mexico-born, other Latin American,
  non-Hispanic foreign-born, US-born, US-born Hispanic), every category below a diploma that
  loses mass at the step is a source.
  - The loss rate is λ = loss ÷ counterfactual share. Only the fraction κ of gross losses that
    equals the "none" step went to "none"; the rest went to grade 5, preschool or 12th grade
    without a diploma.
  - The flow rate into "none" is π = κλ. It is applied to any target group's own 2020+ mix:
    flow_c = π_c·obs_c/(1 − λ_c).
  - For the Mexico-born, π is 0.045 (grades 1–4), 0.114 (grade 6), 0.130 (grade 7),
    0.034 (grade 8), 0.100 (grade 9) and 0.030 (grade 11), with κ = 0.754.
  - Why B is preferred: it returns reports to where the anatomy shows they came from, including
    grade 9. It separates the step from the pre-existing drift. And it scales the correction to
    each group's own grade mix, which matters for new arrival cohorts that have no 2019
    counterpart.
- **How A and B compare.** A attributes the whole 2019→t rise, drift included, to the break and
  gives every group the same φ (0.36 in 2024 for the schooling-selection lane). B's φ follows each
  group's grade mix (0.22–0.39 for the same cohorts). A returns reports at about 5.8 years, B at
  about 7.0. The two bracket the effect.

## 4. Exposed lanes in detail

**`schooling_selection_position_2026_09_23`.** `fix_schooling_position.py` imports the lane's
`position.py` read-only and splits each 2020+ "none" record into a kept part and moved
pseudo-records by sex. It then re-runs the lane's own `summarize`/`undercount`. A positive control
first reproduces every published uncorrected statistic to 5 decimals.
[CALCULATION: `derived/schooling_position_corrected.csv`,
`schooling_position_undercount_corrected.csv`, `schooling_position_correction_params.csv`]

- **Main 2020–23 row (2024 ACS).**
  - Pooled ridit 0.540 → 0.543 / 0.545. Men 0.518 → 0.521 / 0.523; women 0.569 → 0.574 / 0.574.
  - C1 (none or primary incomplete) 0.117 → 0.098 / 0.097, against Mexico's 0.070.
  - C1 gap +0.048 → +0.029 / +0.027 (SE 0.005). Men +0.058 → +0.040 / +0.034; women
    +0.034 → +0.013 / +0.017.
  - C5 is unchanged (+0.026), so "both tails" holds, pooled and for each sex.
  - A moves 74–76% of the excess to C2 and none to C3. B moves 4–8% to C1, 53–57% to C2 and
    35–43% to C3.
- **The verdict's "2015–19 and 2020–23 have more at both ends".** The 2015–19 cohort's main row
  is the 2019 ACS, before the step, so its label is untouched. For 2020–23 the step explains about
  40% of the bottom-tail excess. The label survives.
- **Alternative surveys.** The 2015–19 cohort in the 2020 and 2021 ACS, and the 2020–23 cohort in
  the 2023 ACS, keep "both tails" pooled: C1 gaps +0.008 to +0.019 after correction. Women in the
  2020 and 2021 rows turn "top" (C1 gaps −0.009 to −0.018). Women in the 2023 row keep the label
  on a C1 gap of +0.001 to +0.002, down from +0.018.
- **Table 4, 2024-ACS row.** Every cohort's rank rises, by 0.004–0.026 (A) or 0.005–0.017 (B),
  most for the oldest cohorts. Post-2010 minus 2000–09 moves from 0.049–0.068 to 0.046–0.063.
  Post-2010 minus the 1980s/1990s moves from 0.033–0.058 to 0.023–0.050. The verdict's
  "0.02–0.07 above the 2000–09 arrivals" holds.
- **Survivor table.** The 2019→2024 change moves from −0.040…+0.018 to −0.011…+0.026 (A) or
  −0.021…+0.026 (B). This confirms the lane's statement that the fall coincides with the break.
- **Ladder 197's "0.540 (2020–23)"** reads 0.543–0.545 after correction.

**`arrival_cohorts_2026_09_18`, `origin_relative.py`.** The lane's `YRS` map has no key for
`EDUC` 0, so no-schooling reports are dropped from every survey's mean. The step therefore moves
people scored 2.5–9 years out of the 2023 mean and raises it. `fix_arrival_mean_years.py`
reproduces the published series exactly, then corrects 2023. A takes φ = 0.378 from the Mexico-born
20–64 level ratio and uses 2019 recent arrivals' grade 1–8 mix (5.88 years). B takes φ = 0.352 and
returns reports at 7.37 years.
[CALCULATION: `derived/arrival_mean_years_corrected.csv`]

- 2023 mean 11.92 → 11.77 / 11.82 years. The gain from the 2000 survey is +2.37 → +2.22 / +2.27,
  against INEGI's +2.20. The verdict's "the absolute improvement is the Mexican schooling
  expansion" is strengthened.
- **Adjacent defect, not the break.** Scored at 0 instead of dropped, no-schooling reports
  (9.1%, 12.6%, 9.5%, 4.8% and 6.3% of recent arrivals in 1980–2023) lower every level by
  0.5–1.1 years. The gain becomes +2.53, or +2.67 / +2.69 corrected, which is 0.33–0.49 above
  INEGI's. INEGI's grado promedio counts people with no schooling at 0, so the zero-scored series
  is the like-for-like one. On it the slope conclusion is no longer "the same"; it also crosses
  the 2000 long-form → ACS switch, which the schooling-selection lane found reads 0.02–0.03 higher
  in rank [DATA: that lane's §3b]. This is a question for the lane owner.

**`build/build_borjas_supply_shock_panel.py`.** `fix_borjas_panel.py` reproduces the builder's
below-HS weights for every year exactly. It then returns the 2023 excess of `EDUC` 0 to below-HS
(A: φ 0.310 foreign-born, 0.328 native; B: 0.247, 0.233).
[CALCULATION: `derived/borjas_panel_corrected.csv`]

- 2023 immigrant share below high school: 40.8% → 41.9% / 41.8%.
- The headline "9.8% → 40.8%" becomes 9.8% → 41.8–41.9%, and the 2010→2023 rise is +3.9–4.0 pp
  rather than +2.9.
- Adjacent: the builder drops `EDUC` 0 in every year. Kept, the series reads 10.2%, 19.5%, 32.3%,
  39.3% and 44.1%.

**`scale_spillovers_2026_09_23`.** `fix_scale_spillovers.py` reproduces the lane's national totals
from the same 2024 PUMS file exactly, and its dYRS (0.2551) with the lane's CPS scaling. It then
applies B by sub-group.
[CALCULATION: `derived/scale_spillovers_corrected.csv`, `scale_spillovers_correction_params.csv`]

- Workers' mean years: Mexico-born 10.38 → 10.54, group born elsewhere 13.11 → 13.17, others
  14.24 → 14.27. National dYRS 0.255 → 0.247 (−3%). dHSY and dIPHS move by the same −0.008.
- The average-schooling specs scale by about 0.97. The Iranzo–Peri and years-beyond-12 specs
  change by ≤ ~$1bn, because their high-school coefficients are ±0.01. These are analytical
  estimates: the CZ/CBSA arms were not re-run.
- Innovation arm: Mexico-born 25+ mean years 9.71 → 9.90 (B) or 9.96 (A), against BCHTT's
  pre-2020 10.88.
  - Patents move from −0.07 to +0.10 / +0.16 of the average migrant's effect, or −$24.1bn →
    +$36.8bn / +$57.0bn. The interval is about ±$490bn.
  - Wages move from +$50.3bn to +$99.5bn / +$115.9bn.
  - The arm stays "not measurable, not added". The central +$13.9bn does not use years.

**`return_vs_us_stayers_2026_09_26`** (the source lane). Spec (e) re-scores every 2023 "none"
report at 2.68 years. B gives 1.86 years for men and 2.11 for women (φ 0.265 and 0.298,
destination 7.0 years). That is 69–79% of (e)'s shift, which puts the men's 2023 gap at about
−0.92 rather than −1.00 (main −0.75). [CALCULATION: B parameters on the stayer universe, 2023
PUMS; scaled analytically, not re-run in `compare.py`] Negative selection of male returnees stands.

## 5. Documents that quote exposed numbers (for the parent to update)

- `research/immigration-confidence-ladder.md` entry 197 (0.540 for 2020–23), entry 133 (+2.37
  years) and entry 201 (innovation −$24bn / +$50bn).
- `research/immigration-mexican-arrival-cohorts-2026-09-18.md:14,396` and
  `research/immigration-mexican-origin-age-attainment-2026-09-22.md:44` (+2.37 against +2.20).
- `arrival_cohorts_2026_09_18/RESULT.md:7`.
- `research/immigration-INDEX.md:561`, `research/immigration-borjas-supply-shock-panel-2026-06-23.md:15,23`
  and `research/immigration-friend-reproduce-guide.md:138` (40.8%).
- `dataset_integrity_2026_09_23/acs.md` F6 ("leaves natives alone"; "none on any category at or
  above the high-school line").
- The IPUMS register card `IPUMS_USA_EXTRACTS_2026_09_23`'s break note ("grade 8 or less stays
  continuous").

## 6. Not checked

- `scale_spillovers`: the CZ/CBSA-level years specs were not re-run. The national dYRS ratio
  stands in for them.
- `return_vs_us_stayers`: method B was not run through `compare.py`.
- `build_tier_a_context_panels.py`: not sized, because nothing reads its outputs. It also puts a
  diploma in "college" and uses SCHL codes as years, both unrelated to the break.
- The cause of the 12th-grade-without-diploma step, and whether `SCHG` (grade attending, read by
  `school_cost_where_enrolled`) has its own break.
- The mode-shift mechanism, which cannot be tested without a mode variable.
- Whether the arrival-cohort slope conclusion survives zero-scoring together with a census→ACS
  instrument correction. That is the lane owner's call.

## Reproduce

```sh
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/acs_schooling_break_2026_09_26/break_anatomy.py
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/acs_schooling_break_2026_09_26/fix_schooling_position.py
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/acs_schooling_break_2026_09_26/fix_arrival_mean_years.py
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/acs_schooling_break_2026_09_26/fix_borjas_panel.py
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/acs_schooling_break_2026_09_26/fix_scale_spillovers.py
```

On 2026-09-26 every script exited 0 and a second run wrote byte-identical `derived/` files (sha256
compared, 10 files). Each fix script opens with a positive control that reproduces the lane's
published outputs and raises otherwise. No other lane was edited.

Model self-report: claude-opus-5-5 (this lane); the two fact-sheet sub-agents report
claude-opus-5-5.

## Integration (parent session, 2026-09-26)

The parent session reran all five scripts, and they were byte-identical. It reproduced the step
from the Census PUMS files for five nativity groups, and then acted on the findings:

- **Arrival cohorts: fixed.** `origin_relative.py` now scores `EDUC` 0 at 0 years, and the lane
  was rerun. `fix_arrival_mean_years.py`'s positive control now reproduces that rule. Its output
  is unchanged, because it already reported both scorings.
- **Borjas builder: deferred, not rebuilt.** It writes the release's context-warehouse table, and
  no analysis lane reads it. The memo, INDEX and guide carry the corrected figures.
- **Documents.** The documents in §5 and the lanes in the table carry dated brackets, as do the
  register notes and ladder 228, which had presented the step as new. F6 of the dataset integrity
  audit reported it first, on 2026-09-23.

[Decision](../../../decisions/2026-09-26-acs-no-schooling-break.md).
