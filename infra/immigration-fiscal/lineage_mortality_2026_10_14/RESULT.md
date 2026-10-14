Model: gpt-6 (system identity; exact served backend ID is not exposed in this runtime)
**Verdict:** The specified Mexican sex/nativity mortality construction adds **$3.532–3.535bn** at each end of v7, rather than the pooled-Hispanic arm's $14.888–14.893bn. Cash is unchanged. It does not clear the stated $5bn/claim-flip bar: Black's total modeled cost remains above the lineage's and the lineage-minus-white gap remains positive. Recommend retaining whole-population mortality in the headline under that admission rule, with the unadjusted own-group construction and fully symmetric mortality comparisons beside it. This is a modeled transport of historical hazards, not a direct measurement of current lineage mortality. [CALCULATION: `derived/case_changes.csv`, `derived/pooled_control.csv`, `derived/comparisons.csv`]

## Source verification

Fenelon, Chinn and Anderson, *SSM – Population Health* 3 (2017), 245–254, DOI [10.1016/j.ssmph.2017.01.011](https://doi.org/10.1016/j.ssmph.2017.01.011). The published PDF was fetched from the Cleveland health department's copy, pinned by URL and SHA256 in `inputs/pins.json`, extracted with Poppler, and PDF pages 6/7 visually inspected. Every Mexican HR/CI cell is preserved in `derived/hazard_ratios.csv` with exact source row, table and model. No schema or LLM table extraction is used. [SOURCE: `inputs/fenelon2017.pdf`; URL in `inputs/pins.json`]

The central uses **Models 1 and 3**, not Model 1 at both ages. They adjust for age and interview year only. Models 2 and 4 additionally condition on education, family income, employment, marital status and family size. [SOURCE: Tables 3/4 footnotes, PDF pp. 250–251]

| Table / sex | Nativity | M1, 25–64 HR (CI) | M2, 25–64 HR (CI) | M3, 65+ HR (CI) | M4, 65+ HR (CI) |
|---|---|---|---|---|---|
| 3 / male | US-born | 1.22 (1.15–1.30) | 1.03 (0.96–1.10) | 0.87 (0.81–0.94) | 0.77 (0.71–0.83) |
| 3 / male | Foreign-born | 1.18 (1.11–1.25) | 0.97 (0.91–1.03) | 0.71 (0.64–0.78) | 0.60 (0.55–0.66) |
| 4 / female | US-born | 0.98 (0.91–1.06) | 0.80 (0.74–0.87) | 0.92 (0.86–0.99) | 0.82 (0.76–0.88) |
| 4 / female | Foreign-born | 1.28 (1.19–1.38) | 0.87 (0.81–0.94) | 0.79 (0.72–0.86) | 0.66 (0.60–0.73) |

[SOURCE: primary PDF Tables 3/4; DATA: `derived/hazard_ratios.csv`. CIs as printed. US-born Mexican women at 25–64 do not show an above-white central hazard.]

The data are restricted NHIS linked mortality files, interviews **1990–2009**, mortality follow-up through **2011**, adults 25+, pooled sample **890,115**, **143,435 deaths**. Continuous-time proportional hazards are Gompertz-distributed, separately by sex and age group, with linkage-eligibility-adjusted sample weights. The reference is **US-born non-Hispanic whites**. Self-reported survey ethnicity avoids death-certificate ethnic misclassification. It does not solve differential death linkage: the authors flag poorer foreign-born linkage and do not supply a Mexican-specific correction. They also explicitly cannot fully address health-selective return migration. [SOURCE: PDF Data, Methods and Limitations, pp. 247–249,252]

## Construction and reproducibility controls

For each sex, the primary NVSS 2024 NH-white qx (Tables 17/18, copied byte-for-byte from the comparators' pinned spreadsheets) is multiplied by the paper's Mexican HR: foreign-born for G1, US-born for G2/G3+ and all added descendants. HR is 1 below 25 centrally; the separate arm starts the 25–64 ratio at 18. qx is clipped to [0,1], with the imported model's terminal age 100 retained. HR × qx is the requested probability approximation, not the exact integrated-hazard conversion. NVSS NH-white tables pool nativity, whereas the paper's reference is US-born: this reference transport is a limitation, not an observed exact match. The NVSS inputs are 2024 period rates; future mortality improvement remains the case's 2026 Trustees path. [SOURCE: `inputs/pins.json`; CALCULATION: `mortality.py:build_qx`, `derived/mortality_qx.csv`]

The actuarial route is the comparators' imported `mortality_comparators.py`, `accrual_white.py`/`accrual_black.py`, `tr2026_path.py` and their pension modules. The **2026 payable separate-funds path**, future benefit-tax timing and net basis remain the case's; **Note 2025.7's general denominator stays byte-identical**, checked for every new grid. National annual OASDI/HI receipt totals and qualification rates do not change. [CALCULATION: `derived/audit.json`, executable gates]

Before the new tables are admitted:

- General union (published and row-4 frames), white, Black and observed G3+ controls reproduce the committed full-precision ratios to absolute 1e-9; all three general added profiles also reproduce.
- The pooled-Hispanic arm reproduces **$13.930803673bn** for the identified union, **$0.956996829–0.962072946bn** for added descendants, and **$14.887800502–14.892876619bn** for the lineage, at both ends, to absolute 1e-9.

[CALCULATION: `derived/reproduced_ratios.csv`, `derived/pooled_control.csv`, `derived/audit.json`]

The model uses sex-specific family mortality, but does not link actual spouses' nativity: a modeled G1 spouse takes foreign-born mortality along with the worker. This inherited same-population family assumption stays fixed across arms. Part A is own-sex, without additional spouse qualification credit. [DATA: imported `lifetime_model.py:worker`; `accrual_white.py:part_a`]

## Change on v7, accrual and cash

All numbers below are **billions**, annual income-year-2024 case, personal specifications **16 / 11**, benefits current law can pay, net of future income taxes on benefits. Positive means higher modeled removal/resource cost to the other residents. Every non-mortality input is fixed. [DATA: frozen `main_case_2026_10_14`; CALCULATION: `derived/case_changes.csv`]

| Marginal central change | OASDI net | Part A | Total, same at both ends |
|---|---:|---:|---:|
| G1, identified Mexico-born | +1.494646 | +0.833318 | +2.327964 |
| G2, identified | +0.368322 | +0.174599 | +0.542922 |
| G3+, identified | +0.386593 | +0.165955 | +0.552548 |
| Identified union, 39.712M | +2.249561 | +1.173872 | +3.423433 |
| Added descendants, 3.040M | bounded by profile | bounded by profile | +0.108270–0.111354 |
| Whole lineage, 42.752M | | | **+3.531703–3.534787** |

[CALCULATION: `derived/generation_changes.csv`, `derived/added_profiles.csv`; DATA: case lineage counts. Population precision and every generation appear in the CSVs.]

Identified marginal changes use each generation's row-4 actuarial OASDI/HI payroll shares to apply the change to the account's union receipt dollars. All identified generations retain the union's common relative benefit-tax rate, so their weighted net ratios reconstruct the general union exactly before the change. This is an attribution of the **mortality delta**, not a new complete generation account or an assertion that the case originally used each generation's separate ratio. [CALCULATION: `mortality.py`, `derived/audit.json`]

The added-dollar split is not exported by the frozen case. As in the comparator arm, its OASDI and Part A accrued dollars are bounded by componentwise min/max relative changes over the three admitted profiles: measured G3-rate ages with G3 monetary profile, later-generation ages with G3 profile, and measured G3-rate ages with white monetary profile. All three use US-born Mexican mortality. The narrow bound is uncertainty about missing profile-dollar allocation; it does **not** quantify mortality uncertainty, and componentwise extrema need not be a jointly attainable profile. [CALCULATION: `derived/added_profiles.csv`; INFERENCE: same profile-bound convention as the comparators]

The central construction gives an accrual low end **$343.083721–343.086805bn** and high end **$427.180964–427.184048bn**, from v7's $339.552018 / 423.649261bn. **Cash delta is exactly zero** by the scope of the experiment: only future accrued OASDI/Part A and future benefit-tax timing change; observed 2024 cash benefits and receipts are fixed. Cash remains **$264.425574 / 348.522816bn**. This analytic cash invariance is verified in the output/tests; a fresh cash engine was not rerun. [CALCULATION: `derived/case_changes.csv`; DATA: pinned full/union cash and accrual dumps]

## Arms and disconfirmation

| Arm | Whole-lineage delta from v7, same both ends | Meaning |
|---|---:|---|
| Unadjusted central | +3.531703–3.534787 | Mexican sex/nativity estimates, Models 1/3 |
| All extra G1 65+ advantage treated as salmon bias | +1.354613–1.357698 | Replace only G1 old-age HRs with US-born Mexican HRs |
| Turra pooled-retiree inclusion proxy | +3.513712–3.516796 | G1-only all-Hispanic combined/US correction; −0.017991 from the central |
| Adjusted Models 2/4 | +12.552354–12.555941 | Conditional SES mortality; different estimand |
| All lower HR CI ends | +7.905328–7.908794 | Joint low-hazard endpoint scenario |
| All upper HR CI ends | −1.060522–1.057360 | Joint high-hazard endpoint scenario |
| Extend working-age HR to 18 | +3.540169–3.543548 | Extrapolate outside the paper's age support |

[CALCULATION: `derived/case_changes.csv`. CI endpoints are simultaneous endpoint scenarios, **not a 95% CI for the fiscal delta**: covariance and transport uncertainty are not known.]

The adjusted arm exceeds $5bn, but it should not replace the central: conditional SES coefficients applied to an unconditional white life table are not a measured marginal mortality schedule for the actual group. The upper-CI hazard arm changes the sign relative to v7; this demonstrates uncertainty in the point construction, not a flipped white/Black group ranking. [INFERENCE; CALCULATION: arm table and comparisons]

Turra and Elo (2008), [10.1007/s11113-008-9087-4](https://doi.org/10.1007/s11113-008-9087-4), use SSA primary-beneficiary mortality, ages 65+, during 1996–2000, including deaths abroad. Their Table 4 compares all-Hispanic US-resident and combined US/foreign-resident rates, not Mexican foreign-born rates. Including residents abroad barely changes pooled mortality; the ratios combined/US range **0.997900–1.006510**, with some decreases. This disconfirms treating the entire observed mortality advantage as demonstrated salmon bias. It does not identify a share of the Mexican G1-versus-US-born advantage. This lane additionally prices those **raw all-Hispanic combined/US multipliers only on G1 ages 65+**, retaining the NH-white reference; it is explicitly a pooled-retiree transport proxy, not a measured Mexican correction. Exact cells, raw rates, pins and proxy output are in `inputs/salmon_turra_rates.csv`, `salmon-evidence.md`, and the `salmon_turra_pooled_proxy` rows of `case_changes.csv`. [SOURCE: pinned Turra primary PDF Table 4; CALCULATION: `mortality.py:build_qx`]

Arenas et al. (2015), [10.1007/s13524-015-0429-7](https://doi.org/10.1007/s13524-015-0429-7), support health-related return selection among recent migrants, but do not identify a mortality-attenuation share. The evidence researcher read primary PMC full text through Exa; raw-byte archival retrieval failed, so no Arenas quantitative table is used in this calculation. [SOURCE: `salmon-evidence.md`, primary full-text URL and acquisition limits]

**Pre-retirement emigration is not priced.** Age-specific annual Mexican departure estimates do exist: Van Hook and Zhang (2011), [10.1007/s11113-010-9183-0](https://doi.org/10.1007/s11113-010-9183-0), Table 1, men 7.0% at 18–34 and 2.1% at 35–64; women 3.8% and 0.0%. These are CPS residual estimates of one-year departures including circular migration, not permanent exits. The needed age/sex/nativity probability of residence abroad during eligible retirement and return for care is unidentified. Treating gross exits as absorbing would invent that quantity; the earlier informal −$1–3bn is not a verified calculation. Part A abroad is the motivating scope, not a mortality correction inferred from these gross exits. [SOURCE: pinned `inputs/salmon_vanhook_zhang_2011.html`, Table 1 and Methods; INFERENCE: residence-persistence gap; details in `salmon-evidence.md`]

## Every group on its own mortality, beside the committed rows

These substitute **only +$3.531703–3.534787bn for the case lineage's mortality** in the committed `mortality_group` comparison rows. The Black and white own-mortality costs stay unchanged. Figures are billions of total annual cost, **not per-person gaps**: Black retains its own 41.954M count, the lineage and A1 whites use 42.752M. The comparison is still limited by the comparator lane's unresolved full-imputation symmetry. [DATA: pinned `symmetric_results_oct14.csv`, `symmetric_comparisons_oct14.csv`; CALCULATION: `derived/comparisons.csv`]

| Gap, accrual | Committed low / high | With lineage-specific mortality, low / high |
|---|---:|---:|
| Lineage minus A1 white | 537.916287 / 509.477037 | **541.447990–541.451074 / 513.008740–513.011825** |
| Black minus lineage | 63.582834 / 57.860881 | **60.048046–60.051131 / 54.326094–54.329178** |

The newer symmetric-pension-frame and `combined_rules_only` rows are also reported in `comparisons.csv`, each relative to its **own committed case-lineage row** and holding every comparator change already in that row fixed. They are not silently recombined with the rough-lineage numerator. Cash comparisons remain exactly the committed values. No ranking/claim above flips. [CALCULATION: `derived/comparisons.csv`]

## Recommendation and limits

**Central recommendation for the stated admission bar: whole-population mortality.** The best bounded own-group point construction here is the unadjusted sex/nativity arm, and it is the appropriate companion when quoting every group on its own mortality. But it moves the main case by only $3.53bn, changes neither comparison claim, and transports older survey HRs onto a different-reference period table. The source cannot distinguish G2 from G3+, nor identify mortality for descendants who no longer report Mexican origin. These are reasons to retain its explicit beside status under this brief's gate, not evidence that the actual group has whole-population mortality. [INFERENCE; CALCULATION: central and comparison rows]

Put beside it: unadjusted own-group symmetric comparisons; pooled-Hispanic control/proxy; full-extra-advantage salmon bound; small measured pooled-retiree transport proxy; adjusted Models 2/4; CI endpoint scenarios; extension to 18. Pre-retirement emigration remains unpriced until residence persistence and eligible Part A use are identified. The construction would supersede this recommendation with a current Mexican-origin sex/nativity mortality table matched to the account, or a measured correction that clears $5bn or flips a quoted claim. [INFERENCE]

This LLM analysis concerns a politically charged topic. Source cells, conserved dollars and controls are mechanically checkable; choice of central under the materiality gate and historical-to-current transport remain judgment. It does not estimate a causal effect of ancestry on mortality or assign inherent group traits. [INFERENCE; project instrument-bias caveat]

## For the parent

- Do not fold the pooled-Hispanic $14.89bn arm into the headline as Mexican mortality. The requested Mexican-specific construction is +$3.532–3.535bn, below the bar.
- The exact added-profile split is not identified; carry the bound or export the pension-dollar split before using an exact point.
- Quote the fully symmetric own-mortality comparison with its side-arm status and group counts. Full row-13/imputation symmetry remains a separate unresolved issue; this lane neither resolves nor reprices it.
- No merge, stage or commit was performed. Source/output writes are in the lane plus requested scratch handoff. Two early tests also updated ignored shared `.pytest_cache/v/cache/{nodeids,lastfailed}`; those caches are preserved and listed in `changed-paths.txt`. Lane-local `pytest.ini` now disables that writer, with a session guard against re-enabling it.

## Final validation

The required four-command lane rerun ended **IDENTICAL: 39/39**, **exit 0**. All seven focused tests pass, including source-cell mapping, generation closure, cash invariance, unchanged descendants in salmon arms, consumed-input tamper rejection and no shared-cache writing. Both general and pooled-Hispanic controls reproduce before any new table, and every analytical output byte matches the pre-rerun output. Independent review found no material calculation or frozen-loader defect. All four DOI identifiers resolve. [CALCULATION: ignored `_cache/rerun.log`; DATA: `review-evidence.md`]

The final replay took **518.14 seconds wall**, **98.72 seconds user CPU + 5.38 seconds system CPU**, and **0.529 GB peak physical footprint**, below the 2.5 GB process budget. The low CPU/wall ratio shows substantial time outside this process's CPU execution; the counters do not identify its cause. Earlier 75.28-second and 295.61-second runs are not normalized speed claims. No ps/sysctl or `/usr/bin/time` was used. [CALCULATION: Python `time.perf_counter`, `resource.getrusage`, imported `memory_budget.require_within_budget`; ignored `_cache/measured_run.json`, `_cache/timing.json`]

## Log

- 2026-10-14T14:22:40Z: Read the brief and project conventions; acquired/pinned the published Fenelon PDF; parsed all Mexican cells and visually checked the source pages.
- 2026-10-14T14:31:54Z: First calculation finished, controls reproduced before new tables, 141.14 seconds, 0.521 GB peak physical footprint. Central +$3.531703–3.534787bn; cash zero. [CALCULATION: ignored `_cache/run.log`, `_cache/timing.json` at first run]
- 2026-10-14T14:36:18Z: Supplementary primary sources and consumed Turra CSV added to executable pins; focused suite passed 5/5 after correcting one test's exact floating-point comparison. Calculation unchanged. Independent code-route review found no material central defect; concurrent pin/test issues are closed. [DATA: `review-evidence.md`]
- 2026-10-14T14:40:59Z: Profiled full run finished: 275.18 seconds under profiling, 0.519 GB physical footprint. Main hotspots were upstream actuarial grids (176.41 profiled cumulative seconds) and the Black benefit-tax proxy's grouped transform (63.61 seconds). The profile is in ignored `_cache/profile.txt`. Removed two redundant descendant runs with exact qx-equality and five-row completeness guards; added a regression check that both salmon arms leave descendants unchanged. Further upstream optimization is deferred because the brief forbids editing those lanes; the parent can replace the per-unit clip/lambda with a vectorized grouped sum and avoid unused accrual methods after parity checks. [CALCULATION: profile; INFERENCE: proposed upstream follow-up]
- 2026-10-14T14:42:13Z: All four DOI identifiers resolved to the expected papers; 4/4, no hallucinated or unreachable identifiers. Final optimized reproduction and six-test suite pending. [CALCULATION: research citation checker]
- 2026-10-14T14:44:22Z: Final optimized calculation finished, exit 0, 74.16 calculation seconds (75.28 wrapper seconds), 0.661 GB peak physical footprint; seven focused tests passed, including consumed-salmon-input tamper rejection and descendant/cash invariance. The small pooled-retiree proxy changes the own-group delta by −$0.017991bn. [CALCULATION: ignored `_cache/final_run.log`, `_cache/timing.json`; tests]
- 2026-10-14T14:47:00Z: Scope exception found in two early default pytest invocations: they updated ignored root `.pytest_cache/v/cache/nodeids` and `lastfailed`. Preserved shared contents, listed both paths, and added lane-local no-cache configuration plus a fail-loud fixture. No upstream source or analysis output was edited. Final rerun follows the configuration fix. [DATA: cache mtimes; CALCULATION: test session guard]
- 2026-10-14T14:51:34Z: Lane checker ran all four commands successfully. Every generated analytical file reproduced; the checker correctly returned exit 1 because documentation and cache-isolation fixes were edited while it ran (29/33 files unchanged, four edited files plus new pytest.ini). Static files are now frozen for a clean rerun. This run took 295.61 wrapper seconds versus the preceding 75.28, on identical analytical outputs and 0.631 GB footprint. No normalized speedup is claimed. Added CPU counters to the runner to distinguish wall time from consumed CPU in the final receipt. [CALCULATION: ignored `_cache/rerun.log`, `_cache/measured_run.json`]
- 2026-10-14T14:54:12Z: Next verification correctly blocked at the source gate: peer migration changed three comparator scripts' oct14 entrypoints to oct15. Preserved peers' edits; archived exact originally pinned v7 route bytes from git into this lane. Every archive matches its original SHA256; retained original hashes and appended explicit `route_archives`/frozen-v7 mode, rather than accepting changed source bytes. Source verification passes with the archive mapping. The remaining pension modules, case/data and primary inputs continue to be pinned. [DATA: `inputs/pins.json`, `inputs/route_archive/`; CALCULATION: `prepare_sources.py --freeze-route`]
- 2026-10-14T15:08:08Z (2026-10-15 JST): Final four-command rerun ended IDENTICAL 39/39, exit 0; seven tests pass. Final replay 518.14 wall seconds, 104.10 CPU seconds, 0.529 GB physical footprint. Analytical outputs unchanged across the source freeze. Appended this receipt after the completed check; no calculation/source changes followed it. Complete paths recorded in changed-paths.txt. [CALCULATION: final checker and Python receipts]
