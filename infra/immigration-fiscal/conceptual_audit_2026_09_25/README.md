**Verdict:** The distribution baseline reproduces, but its winner count is sensitive to gross incidence; the off-books lane's person data confirm an all-origin/Mexico-born mismatch. These probes test specific claims. They do not estimate a new welfare total or certify the surrounding models.

# Evidence for the September 25 conceptual audit

Main artifact: [weekly conceptual audit](../../../research/immigration-weekly-conceptual-audit-2026-09-25.md).

The audit window is September 19–25, 2026, through `beefbbade6fe115b9893dfcf7f18da28adb4748c`. The parent of the window is `0d6ae56150f70ca16c9e723d70250065af59a7b0`. Later concurrent figure/prototype work is outside this snapshot. No upstream model or output was changed by the audit. The new scripts write only into this directory's `_cache/`, already ignored by the repository's `**/_cache/` rule. Raw inputs remain read-only.

## Reproduce

From the repository root, using its installed analysis environment and existing local datasets:

```sh
UV_CACHE_DIR=/private/tmp/immigration-audit-uv-cache uv run --no-project python3 infra/immigration-fiscal/conceptual_audit_2026_09_25/inventory_week.py
UV_CACHE_DIR=/private/tmp/immigration-audit-uv-cache OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/conceptual_audit_2026_09_25/probe_distribution.py
UV_CACHE_DIR=/private/tmp/immigration-audit-uv-cache uv run --no-project python3 infra/immigration-fiscal/conceptual_audit_2026_09_25/probe_offbooks.py
```

All three exited 0 on September 25. This is reuse of local data, not an acquisition recipe; restricted survey inputs are not distributed here. See the project's [reproduction inputs](../REPRODUCTION_INPUTS.md) and the original lanes for acquisition/access. In a fresh checkout, follow those environment instructions rather than assuming `--no-project` provisions dependencies.

`inventory_week.py` lists every changed Markdown research/decision/note file and every changed lane `RESULT.md`, `README.md` or `BRIEF.md` between the two commits. It outputs `_cache/weekly_inventory.tsv` and `_cache/commits.txt`: **114 research/decision files, 20 notes, 162 results/readmes, 62 briefs; 366 commits**. Renames are followed by destination path; deleted documents are read from the base. These counts include superseded work, corrections and repeated documentation of the same finding. They are discovery coverage, not independent evidence or an automated substantive audit.

## Distribution probe

[`probe_distribution.py`](probe_distribution.py) loads the winners lane's code from the frozen commit and uses its existing base loader, construction rules, survey weights and pooling function. It refuses tracked economic-input changes since that commit, including staged or unstaged changes; this audit and the independent figure directory are allowed. It does not rebuild or overwrite upstream outputs. The inherited base is pinned by the winners lane itself.

The baseline satisfies **364 checks reached in this construction path**, including source/channel reconciliation, and matches the published pooled central counts in `winners_losers_2026_09_24/derived/net_shares.csv`. This does not claim that every check in the lane's full executable was rerun. `_cache/metadata.json` records the frozen code hash, fiscal inputs, pooling diagnostics and channel-grid extrema; `_cache/sensitivity.csv` records the alternatives.

The population is the lane's approximately **295.8m other residents** in the CPS frame, excluding its Mexican-origin target group. Values below are modeled annual changes, in the lane's 2024-dollar convention. Positive individual net means a winner. The dollar column is the **net assigned to those current people**, not the adopted $201–246bn fiscal account or the published fiscal-plus-social aggregate; the allocation leaves some financing to future taxpayers and has its own social-channel construction. Financing A assigns today's fiscal burden using tax shares; B assigns per person.

| Run | A: pooled winners | B: pooled winners | Assigned annual net, $bn |
|---|---:|---:|---:|
| Published central, reproduced | 23.8736% | 21.3920% | −263.8994 |
| Existing high-school-or-less split, elasticity 1.5 | 29.1707% | 26.2334% | −260.1493 |
| Same split, elasticity 2.5 | 18.7366% | 17.6967% | −266.1340 |
| Existing below-BA split, elasticity 1.5 | 22.7245% | 22.1170% | −261.3799 |
| Same split, elasticity 2.0 | 20.2478% | 19.5610% | −264.7848 |
| Same split, elasticity 2.5 | 18.1359% | 17.5080% | −266.8243 |
| Existing finite native/immigrant substitution variant, epsilon 3 | 25.4655% | 22.9004% | −252.4389 |
| Allocate all federal financing to today's people | 22.4122% | 19.8208% | −275.1979 |

[CALCULATION: `_cache/sensitivity.csv`.] Existing-nest rows replace the private wage component and allocate the associated induced-receipt change using the lane's convention. Other channels stay fixed. These are partial model sensitivities, not a joint equilibrium re-estimation or probability interval. The last row changes the timing of financing incidence; it is not an additional national resource cost.

For a separate identification counterexample, let `w_i` be the central private wage change and `mean(w)` its weighted mean among other residents. Replace it with `mean(w) + k * (w_i - mean(w))`, preserving every other channel. This preserves the aggregate wage change exactly:

| Algebraic dispersion factor k | A: pooled winners | B: pooled winners | Assigned net, $bn |
|---|---:|---:|---:|
| 0 | 1.8680% | 2.0479% | −263.8994 |
| 0.5 | 10.3267% | 11.5605% | −263.8994 |
| 1, original | 23.8736% | 21.3920% | −263.8994 |
| 1.5 | 30.4421% | 27.2986% | −263.8994 |

**These are not fitted economic scenarios, a proposed range, or evidence that k differs from 1.** They disprove only the proposition that validating the aggregate identifies the share with positive net effects. The existing-nest table above, not this artificial rescaling, supplies the empirical-model sensitivity exercise.

The probe also enumerates **1,458 combinations per financing convention** from the existing channel choices. Fiscal/wage low-high choices are paired; renter and landlord choices are paired; remaining channels use their existing low/central/high values. The pooled winner extrema are **13.8589–30.5304%** under A and **13.8084–27.1945%** under B. The maximum uses the central housing choice, showing that a minimum-dollar stack is not automatically a maximum-winner stack. This finite grid is not a set of all economically feasible joint counterfactuals or an uncertainty interval.

Finally, the existing pooler reports **6.9697m other residents in mixed target/other SPM units**. It shares resources only among other-resident members, preserving their aggregate. This is a chosen beneficiary boundary, not the full household's resource change. No corrected all-member household counterfactual was constructed.

## Off-books population probe

[`probe_offbooks.py`](probe_offbooks.py) imports the exact `acs_cells.PERSON` SQL, retains its imputed unauthorized flag and four industry definitions, and compares all-origin wage bills with their Mexico-born intersection. It verifies the all-origin person totals against the cached panel before calculating anything. It then applies the **same published central cell slopes and rates** to the narrower wage base. The output manifest contains input SHA256s, sizes and the exact SQL; no individual records are exported.

| Modeled 2024 amount across the four industries, $bn | Published all-origin unauthorized base | Mexico-born intersection, same slopes |
|---|---:|---:|
| Total employer cost advantage | 6.429890 | 3.219068 |
| Employer-captured payroll taxes | 4.527543 | 2.267985 |
| Workers' compensation | 1.314621 | 0.658792 |
| Wage underpayment | 0.587745 | 0.292300 |
| Implied off-books payroll | 37.080360 | 18.570802 |

[CALCULATION: `_cache/offbooks-totals.csv`, `_cache/offbooks-cells.csv`, `_cache/offbooks-manifest.json`.] Published rows are rounded, so component sums can differ in the last decimal. The industries are construction, landscaping, other janitorial services and restaurants, as defined by the source lane. The raw all-origin unauthorized wage base is larger than the *implied off-books payroll* in the final row; those must not be interchanged.

This is **not** a re-estimated causal effect, an exact all-generation Mexican-origin classification, or a correction to the fiscal headline. It demonstrates the population mismatch in the interpretive crosswalk. The original all-origin question remains legitimate. Estimating what portion is already counted in Mexican-origin receipts requires a separate reconciliation.

## Coverage and limits

The inventory covers the entire dated change window. The table below groups the substantive ideas rather than treating every brief, output and memo as an independent input. Code was traced for promoted findings; deterministic probes were run for the two numerical diagnostics above. Three independent bounded reviews covered fiscal, empirical/generation and social/political families, with synthesis checked against code and primary sources. “No new defect” below means no additional conceptual flaw established in the inspected material, **not** a causal-validity certificate. Unless stated otherwise, lane paths are under `infra/immigration-fiscal/` and coverage is result/method inspection plus selected code, not full reproduction.

| Family and principal inputs | Disposition and limits |
|---|---|
| Annual account and matched benefits: `full_account_2026_09_20`, `full_account_benefits_2026_09_20`, `matched_benefits_2026_09_19/model.py` | Traced budget/welfare identity and private income plus induced receipts. The simple double-count allegation fails. Did not independently reconstruct every finance input. |
| Adopted responses and integrated main case: Sept 23/24 decisions, `main_case_2026_09_24/main_case.cjs`, `assumption_explorer_2026_09_21` | Corrections are combined in one run with interactions; no new arithmetic error established. Small finite-change inconsistency identified. Cross-state response identification is already qualified. |
| County government IV and uncertainty: `gg_response_county_iv_2026_09_23`, `uncertainty_propagation_2026_09_22` | Weak/wide identification and conditional sampling-error floor are disclosed. Did not rerun all regressions or treat specification ranges as probability intervals. |
| Generation attribution: `generation_account_2026_09_24/{production.py,RESULT.md,derived/production_by_generation.json}` | Aumann–Shapley interaction attribution is explicit; standalone removals separately reported. No new additivity flaw. Older white-reference ledger and new no-reference account remain distinct. |
| Century lineage, projection backtest, historical backcast | Legal-status mechanism omission promoted in memo §4. Period versus cohort, horizon, exit and frozen-history assumptions are already disclosed. Did not rebuild all earlier-year accounts. |
| Debt: `debt_legacy_2026_09_23` and benefits contract | Compounding inspected; welfare-use bridge questioned in §8. No principal/annual-flow double count claimed. |
| Distribution: `distribution_weights_2026_09_23`, `winners_losers_2026_09_24` | Deep code trace and baseline/alternative probes; §2. Incidence assumptions remain conditional, not measured household welfare. |
| Medical, care and outside benefit keys: `medical_ethnicity_pooled_2026_09_23`, `ltss_share_2026_09_23`, `admin_benefit_keys_2026_09_24`, `external_benchmarks_2026_09_24` | Denominator, overlap and integration inspected. TANF category bridge remains an open lead. No independent MEPS/MCBS or all administrative-table rebuild. |
| Dataset audit and associated count, imputation, consumption, enrollment, on-books corrections | Screened integration into the adopted run and topic summaries; targeted code where relevant. Did not independently reproduce every individual correction or original source. Small net revision is not independent validation. |
| Population size and ethnic attrition: `unauthorized_population_size_2026_09_19`, `mexican_origin_population_total_2026_09_19`, fourth-generation/later-generation memos, SIPP lineage | Reviewed definitions, coverage scenarios and observed-family-history limitations. No new empirical population estimate; child-to-adult attrition and incomplete G4 history remain limits. Did not certify every publisher's 2026 stock estimate. |
| Return migration and schooling: `enadid_return_selectivity_2026_09_22`, `schooling_selection_position_2026_09_23`, age-attainment and second-generation memos | Wrong return-selection comparator promoted in §6. Other schooling-rank comparisons remain descriptive. No US-stayer contrast built. |
| Religion, origin and admission route: Muslim-origins memo, `admission_route_2026_09_21`, `pew_muslims_2017_2026_09_22`, `nis2003_religion_earnings_2026_09_22` | NIS residence-clock problem noted. Ecological routes, small nativity cells and cross-sectional contrasts already caveated. No new causal religion coefficient or full regression rerun. |
| Indian/later-generation outcomes and public service: Indian fiscal memo, `service_by_ses_2026_09_23` | Partial account, tiny G3 cells, identity attrition and service-versus-patriotism distinctions retained. No newly established material defect. |
| New ancestry IV and reuse: `ancestry_instrument_2026_09_22/second_instrument.py`, `housing_causal_2000_2010_2026_09_22/estimate.py`, `ancestry_iv_congestion_wages_2026_09_23` | Source/construction mismatch and native-outcome mismatch in §1. Author data documentation and 2019/2026 papers checked. Did not fit the correct instrument or assign a bias correction. |
| Production substitution and low-skill literature: `production_nativity_nest_2026_09_22`, low-skill integration memo | Used existing alternatives; occupation-overlap mapping already labeled a sketch. Did not repeat all fourteen full-paper reviews or certify the entire solver. |
| Scale, innovation, institutions and culture: `scale_spillovers_2026_09_23`, `cultural_output_2026_09_19`, Clemens–Pritchett and norms memos | Existing corrections distinguish attitudes from institutional productivity and outputs from willingness to pay. Unidentified scale scenarios remain conditional. No new TFP or cultural-value price. |
| Crime, victims, custody and justice: `crime_victim_cost_2026_09_23`, offender-ethnicity/direction/cohort lanes, detention measurement/reconciliation | Current victim-only prices avoid the earlier public-justice and embedded-homicide double counts. Custody use does not automatically measure offending. Proxy transport is disclosed; no full re-extraction of offender microdata. |
| Status-specific programs and fraud: status-benefits sweep, California/state programs, shelter, ITIN and improper-payment lanes, `fraud_by_citizenship_2026_09_24` | Eligibility, allegations, improper payments and convictions are distinguished. Fraud is within program totals. Federal-loss scenarios have selected-case, duplicate-scheme and intended/actual-loss limitations already stated. No new fraud prevalence estimate. |
| School budget and educational dilution: `school_dilution_2026_09_24/{price.py,RESULT.md}` | §3; primary spending coefficient checked in archived article. Did not rerun the district panel or estimate actual quality loss. |
| Housing, construction and geography: housing-transfer, construction-supply, CA–TX and hedonic/replay lanes | Stock values separated from annual flows and within-beneficiary transfers. Old hedonic interpretation corrected this week; not re-presented as a new defect. The new ancestry-IV problem still applies where reused. |
| Congestion | Fixed-capacity/city-size assumptions and integrated removal calculation inspected. Existing alternative network/refill scenarios are explicit. No measured causal stock-removal effect supplied here. |
| Household care, consumer prices and labor mobility | Care-price overlap with production and taxes inspected; early per-worker/per-resident comparison already corrected. Mobility synthesis carries episode, current-mobility and fixed-regional-factor limits. No rerun of all external studies or new service-price estimate. |
| Off-books competition and vending | Exact population intersection reproduced; §§5 and 9. No firm-compliance outcome or vendor first-stage series constructed. |
| Preferences and distributional welfare weights | White-incidence preference scenario is not automatically Mexican-origin net welfare. Chosen welfare weights are normative, not an observed fiscal correction. No new national cost added. |
| Native movers and political outcomes | Mover mechanism/conditioning issue in §9. Political county-panel identification remains qualified; no new vote-to-policy-to-welfare mapping. |
| Noncitizen voting note | §7; logical bound and geography checked, official California margin verified. Did not re-adjudicate every administrative referral or re-estimate nationwide prevalence. |
| Media, study-integrity and source-audit notes | Screened existing attribution corrections and estimand matching; did not repeat every media fetch or all 26 study audits. Reproducibility access is not itself a completed replication or fraud test. |
| Acquisition, storage, dataset/register and UI changes | Inventoried but excluded from economic verdicts when operational or presentational. The acquisition stop rule was not tested as an empirical identification rule. Concurrent figure prototypes after the snapshot deliberately excluded. |

## Verification boundaries

Primary external sources actually checked for the promoted findings include the ancestry authors' data pages/papers, SSA POMS lawful-presence rules, the cached Jackson–Mackevicius article, official California election returns and CBO debt analyses. The school article's cached primary text was used after web PDF access failed; a transport failure was not treated as absence of evidence. The audit's main memo links those sources beside the claims.

The new probes do not establish: an alternative causal ancestry estimate; native-specific 2000 benefit receipt; the true instructional-output loss; a returnee-versus-US-stayer effect; status-specific lifetime eligibility; all-origin off-books fiscal overlap; a household welfare distribution including the target group; or voting-detection sensitivity. These are explicit remaining empirical tasks. Recommended changes to source models and prior memos have **not** been silently implemented by this audit.
