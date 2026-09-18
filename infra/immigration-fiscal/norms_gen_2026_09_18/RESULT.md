claude-opus-5[1m]

**Verdict:** Hispanic and Mexican-origin first-generation respondents hold *more* confidence in American institutions than native non-Hispanic whites (eleven of thirteen institutions), and the third-plus generation converges down to parity (all-13 index adjusted gap +0.001, SE 0.018). Civil-liberties tolerance shows a large first-generation deficit that closes to white-conservative and white-non-graduate parity by the third generation (Stouffer 15-item: G1 −1.58, G3+ −0.42 against whites overall, −0.03 against white conservatives, −0.28 against whites without a bachelor's). Approval of police force is *lower* among Hispanics at every generation. The persistent gap is the economic role of government, at about a fifth of the internal white ideological spread on the same items. The only measured norm outside the white range is ANES endorsement of political violence (+10.1 pp adjusted at G3+ versus a white conservative-liberal spread of 8.3 pp), and that item has the worst-documented measurement properties in the set. Two instrument checks show first-generation respondents give markedly less differentiated answers across batteries, and that differentiation gap closes across generations alongside the substantive ones, so part of the measured convergence is convergence in survey response behaviour rather than in belief. Mexican-origin respondents run separately reproduce the pattern on nine of twelve headline items; the exception is the anti-American Muslim clergyman battery, where the Mexican-origin third generation remains −0.25 scale points below whites overall (SE 0.09) and below whites without a bachelor's degree.

Memo: `research/immigration-institutions-and-liberal-norms-by-generation-2026-09-18.md`.

## Frame

Stated survey attitudes, not behaviour. Comparisons are made against whites overall *and* against white ideological and educational subgroups, with the internal white spread reported on every item as a yardstick, so that no result rests on comparing a measured Hispanic mean to an idealised white one. Cross-sectional generations are not lineages; ethnic attrition biases convergence estimates downward and persistence estimates upward.

## Data

- GSS 1972-2024 cumulative R3a, analysis window **2000-2024** (13 rounds; `HISPANIC` does not exist before 2000). Weight `WTSSNRPS` with `WTSSPS` fallback for 2000/2002. Stratified with-replacement design variance over `VSTRAT`/`VPSU`, 1,146 strata and 5,837 PSUs, full frame retained with zero influence outside each domain.
- ANES 2020 and 2024 public CSV time series, pre-election weight for pre-election items and post-election weight for post-election items, ANES variance stratum and variance unit. Every variable id read from the shipped codebook PDFs by `cb_index.py` (`derived/cb_index.json`), none recalled.
- Generation coding reused verbatim from `attitudes_gen_2026_09_16`, including the ladder-110 repair (GSS `PARBORN` 3/5/7 stay unknown). Unknown-generation respondents excluded from every named group.

## Gates, all passing before results were read

| Gate | Result |
|---|---|
| Vectorised design covariance vs explicit stratum loop (`gate_var.py`) | max abs diff 1.6e-11 |
| Adjusted GSS trust gaps vs `frontier_execution_2026_09_17/social` (`gate_prior.py`) | −11.811 (1.546), −11.217 (2.008), −9.726 (1.990) against published −11.81 (1.55), −11.22 (2.01), −9.73 (1.99); max deviation 0.004 pp; n = 13,912 |
| Nine ANES pooled means vs `attitudes_gen_2026_09_16` (`gate_anes.py`) | all within tolerance, including net in-group thermometer by generation |
| Weighted Hispanic generation shares, ANES | 2020 .276/.334/.389 and 2024 .282/.399/.319, exact match to prior lane |
| 70 numbers quoted in the memo re-checked against the CSVs (`verify_memo.py`) | 70/70 |
| Synthesis table and language-check numbers re-checked (`verify_tail.py`) | PASS |

A rank-deficiency bug was found and fixed mid-run: survey-year dummies built over the full 2000+ frame made every short-module item (the Muslim tolerance items from 2008, the ISSP identity modules) collinear with the intercept, silently dropping 26 outcomes from all adjusted models. Year fixed effects are now built inside each estimation sample. The trust gate is unaffected and still reproduces exactly.

## Headline numbers

Adjusted, design SE in parentheses. Full tables in the memo and `derived/`.

| Item | Hisp G3+ vs whites | vs white conservatives | vs whites without a BA | White cons − lib |
|---|---:|---:|---:|---:|
| Stouffer 15-item tolerance (scale pts) | −0.42 (0.18) | −0.03 (0.19) | −0.28 (0.20) | −0.98 (0.10) |
| All-13 institutional confidence index | +0.00 (0.02) | +0.03 (0.02) | +0.01 (0.02) | −0.04 (0.01) |
| Obedience as a top child quality (pp) | +3.2 (1.8) | −1.6 (1.9) | +2.1 (1.9) | +11.5 (1.0) |
| President without Congress or courts (pp) | +4.0 (2.8) | +2.0 (3.0) | +1.1 (2.9) | +7.5 (1.3) |
| Strong leader who bends the rules (pp) | +3.6 (3.2) | −8.3 (3.4) | −0.9 (3.2) | +29.0 (1.7) |
| Authoritarian child-rearing (0-4) | +0.16 (0.08) | −0.24 (0.09) | −0.07 (0.09) | +1.25 (0.05) |
| Government should reduce income differences (1-7) | +0.46 (0.09) | +1.50 (0.09) | +0.47 (0.09) | −2.18 (0.05) |
| Political violence at least a little justified (pp) | +10.1 (2.6) | +14.1 (2.8) | +9.6 (2.7) | −8.3 (1.4) |

Generational convergence is precise in the GSS (15-item tolerance G3+ − G1 = +1.16, SE 0.25; obedience −12.9 pp, SE 2.4; confidence index −0.119, SE 0.022) and undetectable in ANES, where every generational contrast has a standard error of the same size as the gap. The ANES nulls are underpowered, not evidence of flatness.

## Part C

Mostly **[GAP]**. The WVS7 and Pew percentages, and LAPOP's Mexico democracy-support and coup-tolerance bars, were not obtained (the LAPOP country charts are images with no text layer); `ANCHORS.md` records every URL tried and the exact failure mode, plus the verified frame facts (WVS7 country-years Mexico 2018 / USA 2017; LAPOP's most recent round is 2026; Pew's 2025 National Survey of Latinos design). This does not affect the verdict: emigrants are not a random draw from the sending population, so an origin-country average was only ever a prior about the source distribution, never a prediction for migrants or their descendants, and the direct measurement supersedes it.

## Covered and skipped

Covered: all 13 GSS confidence items and two indices; the full Stouffer battery including the Muslim-clergyman items and three summed scales; obedience, courts, death penalty, gun permits, marijuana, the five police-force items and their index; the four role-of-government items; the ISSP national-identity and pluralism modules; two response-style instrument checks; sixteen ANES democratic-norms items plus the authoritarianism battery and scale; interview-language splits in both surveys; a direct GSS web-versus-interviewer mode test on the 2022 and 2024 rounds (`mode_check.py`); a Mexican-origin-only run of the synthesis table (`mex_synth.py`); a grandparent-based third-versus-fourth-generation split in ANES.

Skipped: `AMIMP`, `AMPROUD` and `ETHSPKOK` (absent from release R3a); `WIRTAP` (absent; `GRASS` used in its place among the civil-liberties-adjacent items); pre-2000 GSS rounds (no Hispanic identifier); a year-interacted generational specification; the GSS generalised-trust re-litigation (reproduced as a gate only, findings left to ladder entries 87/110/117).

## Files

Scripts: `norms_lib.py`, `outcomes.py`, `estimate.py`, `run_gss.py`, `cb_index.py`, `anes_spec.py`, `anes_norms.py`, `lang_check.py`, `lang_anes.py`, `mode_check.py`, `ratio.py`, `mex_synth.py`, `make_tables.py`, `gate_var.py`, `gate_prior.py`, `gate_anes.py`, `verify_memo.py`, `verify_tail.py`, `probe_cov.py`.

Outputs: `derived/gss_raw_means.csv` (1,410 rows), `derived/gss_adjusted.csv` (5,358), `derived/anes_raw_means.csv` (238), `derived/anes_adjusted.csv` (680), `derived/gss_language_check.csv`, `derived/anes_language_check.csv`, `derived/gss_mode_check.csv`, `derived/gss_mode_difference.csv`, `derived/gap_vs_white_spread.csv`, `derived/item_coverage.csv`, `derived/tables.md`, `derived/mex_synth_table.md`, `derived/gss_audit.json`, `derived/anes_audit.json`, `derived/cb_index.json`.

Raw data is a symlink to the `attitudes_gen_2026_09_16` lane's `raw/`; nothing under `raw/` was modified. Not committed.
