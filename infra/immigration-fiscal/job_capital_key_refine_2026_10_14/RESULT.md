**Verdict:** The conditional K1 legal-form payroll refinement plus K2 foreign-source exclusion raises v7's annual lineage cost by **$5.445bn low / $2.015bn high**, to **$344.997–425.664bn**, at the personal specifications 16 / 11. The same changes on the identified union are **+$5.083 / +$1.881bn**. The joint change crosses the review's $5bn bar at the low end; neither standalone point does. This is a modelled candidate, not an adopted case or observed member C-corporation employment. [CALCULATION: `refine.py` → `derived/summary.json` stack_K1_industry_size_K2; ASSUMPTION: K1's conditional payroll propensity]

K3's requested gross residential pricing is −$1.573bn at both lineage ends, but the owner-tax instrument already includes special assessments. Withhold that addition pending reconciliation. K4, K5 and K6 are sizing checks below the bar under the stated proxies; none supplies a stronger central measurement. [CALCULATION: `derived/comparison.csv`; SOURCE: Census ACS 2023/2024 subject definitions, Real Estate Taxes; INFERENCE: recommendations below]

## Frame, control and signs

The reference is the frozen adopted v7 `oct14`: $339.552018–423.649261bn, cash set $264.425574–348.522816bn, personal allocation, specifications 16 / 11. The union is the account's 39,712,493 people; the lineage includes the 3.04M added descendants, 42.75M people in total. Every reported arm is one change from this central; all other tax lines, service responses, pension treatment, public-capital return and production terms hold fixed. The production capital-tax term remains zero. [DATA: `main_case_2026_10_14/derived/summary.json` v7, `corrections.json` meta.lineage and meta.job_capital_taxes; ASSUMPTION]

Positive Δcost means the group's modeled net fiscal cost rises. A smaller lost receipt raises that cost; a newly responsive spending subsidy also raises it. The spending sign is checked against the actual engine, not inferred from the receipt convention. [CALCULATION: `k5_subsidies.py` engine sign gate]

`core.py` imports frozen `job_capital_taxes_2026_10_14/job_capital.py` read-only, observes its returned calculation locals, and writes its replay into `_cache/positive_control/`. All five source outputs reproduce **byte for byte**, before any refinement. Its national parser is separately replayed into `_cache/national_control/`, and both outputs reproduce byte for byte. No source lane, frozen case or research document is edited. [CALCULATION: `core.py`, `k236.py` → control gates]

| Positive control: item 6 net-cost change, $bn | Low | High | CPS sampling SE low / high |
|---|---:|---:|---:|
| Identified union | −66.481309 | −40.265271 | 2.005886 / 1.106930 |
| Full lineage, using v7's actual added-person rule | −71.771137 | −43.366887 | 2.079976 / 1.148684 conditional |

[CALCULATION: `derived/core.json` control; DATA: frozen `item.json` central and v7 meta.job_capital_taxes.effect_at_reference_bn]

## One-change arms

All figures below are Δnet fiscal cost in $bn, personal allocation; low / high refer to the current headline's endpoints. SEs are paired errors of the **change**, not the arm's level. Each point below the last row is below $5bn at both lineage ends. The K1 selection envelopes are separate from these point estimates. [CALCULATION: `derived/comparison.csv`]

| Rule / arm | Union Δ low / high | Union SE low / high | Lineage Δ low / high | Lineage conditional SE low / high | $5bn bar |
|---|---:|---:|---:|---:|---|
| K1 size-only corporate payroll proxy | +2.029 / +0.751 | 0.524 / 0.194 | +2.057 / +0.761 | 0.537 / 0.199 | below |
| K1 industry × size corporate payroll proxy | +1.792 / +0.663 | 0.478 / 0.177 | +1.814 / +0.671 | 0.492 / 0.182 | below |
| K2 foreign-source residence tax removed | +3.427 / +1.268 | 0.314 / 0.116 | +3.775 / +1.397 | 0.324 / 0.120 | below |
| K3 gross documentary + assessments | −1.444 / −1.444 | 0.025 / 0.025 | −1.573 / −1.573 | 0.027 / 0.027 | below; overlap unresolved |
| K3 documentary only | −0.837 / −0.837 | 0.014 / 0.014 | −0.912 / −0.912 | 0.016 / 0.016 | below |
| K3 assessments only | −0.607 / −0.607 | 0.010 / 0.010 | −0.661 / −0.661 | 0.011 / 0.011 | below; overlap |
| K4 strict matched C-only minor detail | −0.211 / −0.078 | 0.168 / 0.062 | −0.218 / −0.081 | 0.178 / 0.066 | below |
| K4 limited C-only with unresolved wages at parent | −0.049 / −0.018 | 0.185 / 0.068 | −0.050 / −0.019 | 0.194 / 0.072 | below |
| K4 fuller all-form minor detail | −0.358 / −0.132 | 0.685 / 0.253 | −0.350 / −0.129 | 0.725 / 0.268 | below |
| K4 strict all-form minor detail | +0.426 / +0.158 | 0.434 / 0.160 | +0.451 / +0.167 | 0.461 / 0.171 | below |
| K5 named air / maritime full-response sensitivity | +0.013 / +0.013 | 0.003 / 0.003 | +0.015 / +0.015 | 0.003 / 0.003 | below |
| K5 state/local railroad proxy | +0.027 / +0.027 | 0.018 / 0.018 | +0.030 / +0.030 | 0.018 / 0.018 | below |
| K5 unclassified residual plain-wage proxy | +1.997 / +1.997 | 0.036 / 0.036 | +2.144 / +2.144 | 0.038 / 0.038 | below |
| K5 all nonfarm nonhousing plain-wage proxy | +2.009 / +2.009 | 0.037 / 0.037 | +2.159 / +2.159 | 0.039 / 0.039 | below |
| K5 functional-mix proxy | +2.317 / +2.317 | 0.076 / 0.076 | +2.469 / +2.469 | 0.080 / 0.080 | below |
| K6 support activities, severance stays | −0.371 / −0.296 | 0.124 / 0.099 | −0.396 / −0.316 | 0.127 / 0.102 | below; size only |
| K6 support + extraction equipment-tax proxy | −0.677 / −0.602 | 0.206 / 0.181 | −0.724 / −0.644 | 0.212 / 0.186 | below; size only |
| **Joint K1 industry-size + K2** | **+5.083 / +1.881** | **0.548 / 0.203** | **+5.445 / +2.015** | **0.564 / 0.209** | **above low, below high** |

Complete precision, item-6 levels for applicable arms and changed set/cash headline levels are in `derived/arms.csv`; `derived/summary.json` retains the recipes and recommendations. [DATA]

## K1: legal form within industry

The finest verified public **joint** source is Census SUSB 2022 legal-form × industry sector × **enterprise employment size**, not establishment size. It separates S corporations from **“C-Corporation and other corporate legal forms.”** This label is a proxy qualification; it is not a pure tax-return C-corporation identifier. Finer Economic Census legal-form and firm-size tables are marginal tables, not the required joint observation. [SOURCE: https://www2.census.gov/programs-surveys/susb/tables/2022/us_state_naicssector_lfo_2022.xlsx; `inputs/k1_pins.json`; DATA: `derived/k1_payroll.csv`]

CPS NOEMP and Census size bins match after merging to <10, 10–99, 100–499 and 500+. No interpolation is used; NOEMP0 has zero wage dollars. Corporate payroll propensity in each sector × size cell multiplies both the group's and national wage bills before taking the group's C-payroll share. Original top-wage spreading and thin-cell pooling are retained; neutral corporate propensity 1 recovers every original group target in all 161 columns. Other taxes stay on all employers. [CALCULATION: `k1_legal.py` calculate; `derived/k1_summary.json` gates; ASSUMPTION: group propensity within matched cells equals the national propensity]

SUSB excludes crop/animal production and railroads, and cannot cover the government corporate-tax cells. These cells keep the original key rather than taking an unsupported profile. Its mixed-segment exclusions for some funds and notaries remain caveats. The 2022 payroll mix is transported to 2024. IRS SOI 2022 C-only salary deductions plus separately printed officer compensation are a diagnostic cross-check: they exclude cost-of-goods-sold wages and classify consolidated returns, while Census measures establishment payroll. No false payroll-level parity is claimed. [SOURCE: pinned SUSB methodology; IRS 22co53ccr.xlsx / 22co61ccr.xlsx; DATA: `derived/k1_irs_crosscheck.csv`, `k1_uncovered_cells.csv`; ASSUMPTION]

**Recommendation:** use the industry-size arm if the parent wants a narrower, explicitly modelled corporate key under the same conditional-proportionality convention as the central. Keep the size-only arm diagnostic. This is not measured legal-form employment for union members. Disconfirmation: once exchangeability between members and others within those cells is removed, public marginals allow very wide selection envelopes. On the lineage, Δcost is **−36.303 to +43.061bn low**, **−13.432 to +15.933bn high**. These are relaxed outer identification envelopes, conditional on transported payroll marginals, not confidence intervals or jointly sharp lineage bounds. They exceed the $5bn bar. [CALCULATION: `derived/k1_summary.json` selection_min/max; ASSUMPTION; INFERENCE]

Detailed method, coverage and source checks: [k1-evidence.md](k1-evidence.md).

## K2: foreign-source income

The measured TY2021 source chain is IRS SOI Corporate Foreign Tax Credit Table 1 column 19 (“Difference between limitation and foreign tax credit”), $59.280288bn. The parser verifies the footnote defining it as one way to measure US tax owed on foreign-source income and column 18 less column 2 within the source's adjustments. Dividing by Publication 5655's $371.4bn all-industry income tax after credits gives 0.159613. Applied to the frozen case's federal corporate tax level, and distributed by SOI industry, this removes **$78.475354bn of modelled 2024 national tax**. The historical ratio and scaled 2024 dollars are distinct objects. State tax is held fixed under the original source lane's assumption. [SOURCE: https://www.irs.gov/statistics/soi-tax-stats-corporate-foreign-tax-credit-statistics; pinned `irs_soi_coftc_ty2021.pdf`, `irs_p5655_ty2021.pdf`; CALCULATION: frozen national.py replay → `derived/k236.json` K2]

**Recommendation:** exclude it from a source-tax item tied to capital at US jobs. Strongest counterargument: foreign operations can depend on US headquarters and domestic labor, and US-market demand can affect multinational rents. The inspected tables do not identify the removal response of those foreign profits. That supports a separate residence-tax sensitivity, not automatically treating every foreign profit dollar as capital at the group's domestic jobs. Both source-lane union and v7 full-case foreign-removal arms reproduce to 1e−9bn. [INFERENCE; CALCULATION: `refine.py` K2 gates]

## K3: residential documentary taxes and assessments

The source excludes $26.629311bn nationally: documentary $15.440742bn and special assessments $11.188568bn. Split them by Z.1 owner-occupied versus noncorporate residential market value, then use **live v7** owner/renter shares and their 0.772699 / 0.718912 responses. The owner share is 0.062120648 on the union and 0.068137323 on the lineage; the renter share is 0.114667 / 0.122564495. The owner key incorporates v7's row-4 correction. [DATA: `derived/k236.json`, `housing_keys.json`; SOURCE: frozen Z.1/BEA parsers; CALCULATION: `housing_keys.cjs`]

**Recommendation: withhold an unqualified central addition.** The ACS 2023 real-estate-tax concept includes special assessments; its B25103 median feeds `stage_inputs.py`'s state effective rate, which feeds the modeled owner-tax amount. An extra owner-assessment receipt can therefore overlap. The tenant line is itself a split of BEA housing **taxes on production**; its classification must also be reconciled before adding another housing-tax amount. Documentary-only pricing is preserved as a separate candidate sensitivity; the national stock-value split and inherited property responses are assumptions for transaction taxes. [SOURCE: https://www2.census.gov/programs-surveys/acs/tech_docs/subject_definitions/2023_ACSSubjectDefinitions.pdf, Real Estate Taxes; DATA: `gen_ledger_extension_2026_09_16/stage_inputs.py:34-39`, `extend_ledger.py:173-178`, `generation_account_2026_09_24/keys.py:50-57`, `full_account_receipts_2026_09_20/builder.py:209-214`; INFERENCE]

Sampling is available: 160 CPS replicates reconstruct the modeled-owner key and match live v7 to 1e−9; 80 ACS person replicates stream the existing renter proxy and reproduce its rounded main key. The independent-survey variances are combined with live main-key calibrations fixed. The components use the same keys, so the gross SE scales their shared error rather than adding component SEs in quadrature. [CALCULATION: `k3_sampling.py` → `derived/k3_sampling.json`]

## K4: finer industry

IRS Table 5.3 publishes minor-industry income tax after credits excluding 1120S / REIT / RIC forms, but suppresses many entries. It includes 1120, F, L and PC; it is not exclusively Form 1120. Matched public CPS codes are merged where they cross IRS minors; the strict arm leaves cells with unresolved “not specified” wages unchanged. The fuller all-form and limited C-only arms are separate diagnostics. Every refined cell keeps its frozen BEA corporate-tax total and its management/lessor reallocations; only its internal key changes. National source levels and other lines hold fixed. [SOURCE: https://www.irs.gov/pub/irs-soi/22co53ccr.xlsx, https://www.irs.gov/pub/irs-soi/22co01ccr.xlsx; DATA: `derived/k4_source_rows.csv`, `k4_code_concordance.csv`, `k4_detail_bins.csv`]

**Recommendation:** retain the summary-industry central. Strict C-only detail changes the lineage by only −$0.218 / −$0.081bn, with limited coverage. Source national sector rounding is preserved as an explicit $0.000002bn raw residual, interval-checked against integer-thousand publication precision; generated reconciled allocations still close at 1e−6bn. The property analogue is 2017 detailed T00OTOP, mixing production taxes; no matched 2024 finer business-property-only amount was found in the pinned SUT. [CALCULATION: `derived/k4_summary.json`; DATA: pinned BEA Supply-Use ZIP; INFERENCE]

Detailed method: [k4-evidence.md](k4-evidence.md).

## K5: subsidies

Frozen NIPA 3.13 gives nonhousing subsidies $33.978bn: agriculture $8.233bn, named maritime/air $0.405bn, Federal Other $24.627bn and state/local $0.713bn. Agriculture stays at 0 under fixed land and world prices. Other includes crop insurance, railroads and mass transit; it is not a measured residual of generic business-capital subsidies. Functional and SUT tables offer alternative splits but differ in definitions/vintage and cannot be spliced into this program ledger. [SOURCE: frozen BEA Table 3.13 footnote; MP-5; DATA: `derived/k5_programs.csv`, `k5_functions.csv`, `k5_sut_subsidies.csv`]

**Recommendation:** withhold a new central subsidy response. Full adjustment gives a reason for the domestic-service part to respond; replacement demand, fixed routes and fixed agricultural acres are counterarguments. Payments to government enterprises can already enter the case's responsive enterprise-surplus receipts. Their gross spending saving needs the corresponding receipt loss, and the required program/recipient split is unresolved. The largest tested **gross** proxy, +$2.469bn on the lineage, is below the bar; this does not bound every unidentified program allocation. [SOURCE: BEA glossary subsidies/current surplus of government enterprises; CALCULATION: `derived/k5_summary.json`; INFERENCE]

Detailed program rules and offset problem: [k5-evidence.md](k5-evidence.md).

## K6: support services and equipment

Size NAICS 213 support services separately, with corporate response 1 / 0.37, property 0.880649 and other production components 1, but severance 0. For extraction equipment, the only implemented amount is the source lane's **national** tangible-personal-property fraction, 0.126529, applied to extraction property tax at response 1. It does not identify mining's actual reserve/equipment tax composition. Both arms hold extraction reserves and severance fixed. [CALCULATION: `k236.py` → `_cache/k236_targets.npz`; DATA: frozen national vectors and tpp.tau_of_business_line; ASSUMPTION]

**Recommendation:** size only; retain mining's central zero. A support service can be reproducible without its jobs or equipment departing when fixed extraction output is refilled. The source tables do not identify that removal response. Both tested departures are below $1bn on either lineage end and below the review bar. [INFERENCE; CALCULATION: `derived/comparison.csv` K6]

## Stack and uncertainty

The conditional recommended pair is K1 industry-size plus K2. Compute **revised legal payroll shares × the domestic-source corporate vector** simultaneously. The resulting interaction is **−$0.143322bn low / −$0.053029bn high** on the lineage (union −$0.136142 / −$0.050373bn), verified in every replicate as the exact cross product. Keeping only K2 is the less assumption-dependent alternative: $343.327–425.046bn. K3–K6 are withheld from this stack for the reasons above. [CALCULATION: `derived/summary.json` interactions; DATA: v7 foreign-source arm; ASSUMPTION; INFERENCE]

The conditional K1+K2 candidate is $344.997–425.664bn set and $269.870–350.537bn cash, moving both by +$5.445 / +$2.015bn. End specifications stay 16 / 11: all personal specifications at a reading receive the same receipt change. Sampling errors are $0.564 / $0.209bn for the lineage change. They condition on national payroll probabilities, source tax totals/vintages, the fill-in correction and fixed added-person wage calibration. They exclude uncertainty in ancestry counts, C3, tax response and within-cell legal-form selection. K3's separate survey sampling description is above; it is not a fabricated joint CPS/ACS replicate estimator. [CALCULATION: `derived/summary.json`; ASSUMPTION]

The perspective is the case's change for other residents under full adjustment. These are conditional fiscal quantities, not verified causal effects of a historical removal or welfare totals. The instrument is an LLM with documented immigration dispositions; all numerical moves are reproducible in both directions, and both favorable receipt additions and unfavorable tax removals were kept as arms. [FRAMING-SENSITIVE; DATA: `notes/llm-bias-caveat.md`; INFERENCE]

## Gates, reproduction and log

Gates cover source pins and parsed labels, national closure at 1e−6bn or tighter, all-replicate weight/wage conservation, frozen byte-identical positive controls, original code-cell and thin-pool reconstruction, neutral legal propensity, generation closure, exact adopted K2 arm recovery, corrected live housing keys, fiscal signs and stack cross products. Source-rounding intervals are separate from computational closure; no tolerance is loosened. [DATA: each `derived/*json` gates]

Run from the repository root, in this order:

```sh
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/job_capital_key_refine_2026_10_14/core.py
node infra/immigration-fiscal/job_capital_key_refine_2026_10_14/housing_keys.cjs
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/job_capital_key_refine_2026_10_14/k236.py
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/job_capital_key_refine_2026_10_14/k3_sampling.py
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/job_capital_key_refine_2026_10_14/k1_legal.py
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/job_capital_key_refine_2026_10_14/k4_detail.py
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/job_capital_key_refine_2026_10_14/k5_subsidies.py
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/job_capital_key_refine_2026_10_14/refine.py
```

Raw downloads remain in ignored `_cache/`, pinned in `inputs/`. The Census K1 download can be restored with `k1_legal.py --acquire`; the IRS K4 downloads use their pinned primary URLs. K236 restores its pinned documentation PDFs when missing. Raw national/ACS/CPS inputs are reused read-only from the established source lanes, not copied or mutated. The NPZ caches are rederived in the command order above.

Append-only log, times obtained from `date`:

- 2026-10-14 20:21:41 JST — lane created; frozen source and adopted case read, peers' edits left untouched.
- Core replay: 16.20s / 2.045GB peak RSS on the first joint-code export; all frozen outputs identical. National replay/documentation: 9.77s / 0.082GB; K3 sampling: 29.08s / 1.703GB. All measured by Python perf_counter/getrusage; variable runtime receipts live only in `_cache/`.
- 2026-10-14 20:43:51 JST — all six arms and conditional pair built; Python compile and JavaScript syntax checks exit 0. K1 public coverage exclusions were corrected before integration; original all-employer keys remain in farm, rail and government cells.
- Independent scoped Astra code check found no material executable defect; it independently recovered the joint changes and SEs, and inspected selected primary payroll/IRS rows. Coverage and limits: [code-check.md](code-check.md).
- First whole-lane run: all eight commands exit 0; 41/42 files identical, exit 1 because the newly added live-owner-key positive-control gate had not yet been written to `derived/k3_sampling.json` when the snapshot was taken. Comparison showed only that new gate record; no numeric change. A new whole-lane comparison follows against the complete gate baseline. Python timing: 60.12s, peak child RSS 1.942GB.
- Second whole-lane run: all eight commands exit 0, **IDENTICAL 42/42, exit 0**, no `--allow-unrun`; 55.68s / 1.925GB peak child RSS. A frozen-source Python bytecode cache created by an earlier import was then removed; source imports now disable bytecode writes and explicit cache-invariance gates pass. No source calculation or input was changed. Final rerun follows with these guards.
- Every net changed/generated file, including ignored downloads, NPZ, runtimes and bytecode caches inside the new lane, is listed in [changed-paths.txt](changed-paths.txt). The handoff is the only file outside this new lane; no merge, stage or commit was performed.
- 2026-10-14 20:52 JST — final full rerun with bytecode-invariance guards: **all eight commands rc 0, IDENTICAL 43/43, exit 0**, no `--allow-unrun`. Python perf_counter/getrusage: 91.15s total, 1.322GB peak child RSS. Frozen source cache remains exactly its original two files; source data/outputs/code hashes hold. Final runtime receipts: `_cache/rerun.json`, `_cache/rerun.log`.

The final reproduction check is:

```sh
uv run --no-project python3 scripts/rerun_lane.py infra/immigration-fiscal/job_capital_key_refine_2026_10_14 "uv run --no-project python3 {lane}/core.py" "node {lane}/housing_keys.cjs" "uv run --no-project python3 {lane}/k236.py" "uv run --no-project python3 {lane}/k3_sampling.py" "uv run --no-project python3 {lane}/k1_legal.py" "uv run --no-project python3 {lane}/k4_detail.py" "uv run --no-project python3 {lane}/k5_subsidies.py" "uv run --no-project python3 {lane}/refine.py"
```
