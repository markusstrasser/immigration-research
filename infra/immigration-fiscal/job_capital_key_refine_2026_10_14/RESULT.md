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

## 2026-10-14 round-1 extension after the Opus axis

**Verdict:** Preserve the original six arms and K1×K2 candidate. Broad two-block reallocation plus mining refill lowers the lineage headline by **$7.645493bn low / $3.655646bn high**; narrow tradables gives **−$2.030764 / −$0.686995bn**. The broad low-side move crosses the $5bn bar. These are fixed-price response arms, not an identified removal effect. Recommend K2's domestic-source scope correction for adoption; keep K1, K3 documentary, K4, K5, K6 refill, K7, network and land as conditional arms. [CALCULATION: `reallocation.py` → `derived/reallocation.json`; INFERENCE]

All figures below are one change from the frozen **v7 central**, with personal end specifications 16 / 11. Union is the account's 39.712493M identified members; lineage is the live case's 42.752213M people. Positive Δ means net fiscal cost rises; a negative Δ means more source tax is lost on removal and net cost falls. Set and cash change by the same receipt/subsidy amount. Sampling SEs condition on demand, tax/subsidy totals, national legal propensities, lineage wage calibration and source vintages; they do not measure GE response uncertainty. [DATA: `derived/summary.json.frame`, `derived/core.json`; ASSUMPTION]

### K7: two-block mechanism and limiting cases

For each reading, let A_i be the national taxes in cell i after the central line responses, W_i national wage dollars, W_gi actual group wage dollars, and s_gi the frozen tax-allocation share (thin-cell pooling retained). The jobs key is J = Σ_i s_gi A_i. Let d be the group's demand share. Private non-tradables N follow demand; T follows factor supply. Native refill in N is signed R_N = Σ_N(W_gi − d W_i). At a pinned wage it draws native wage units out of T when positive and returns them to T when negative. National tradable tax intensity is t_T = Σ_T A_i / Σ_T W_i. The K7 loss is:

`J_T + d Σ_N A_i + t_T R_N + J_fixed`.

Mining taxes stay zero; mining refill is a distinct additional term `t_T Σ_mining W_gi`, counted once in combined rows. Thus K7 itself isolates non-tradable reallocation, K6 isolates mining refill, and K7-with-mining is their exact combined probe. Thin-cell tax shares remain pooled while actual wage units determine native refill. The national T intensity is the primary arm; group-weighted intensity is retained as a different assumed destination mix. [CALCULATION: `reallocation.py:two_block`, `derived/reallocation.json.details`; ASSUMPTION]

Demand uses the requested case consumption-lane basis **0.08142000842884183** (`consumption_key_2026_09_24/derived/key_specs.csv`, both_corridor_net_h2, adopted_basis_share), read from data. Added descendants' demand is the live v7 general-consumption carrier's lineage-minus-union increment **0.0076739772081388935**, so lineage d is **0.08909398563698072**. This prices the added people separately rather than multiplying the union result by a population ratio. `personal_current_transfers` is the general-consumption carrier; sales/excise taxes have tax-specific adjustments. The alternative live payload d is union **0.08188016967467436**, lineage **0.08955414688281325** and is reported separately. [DATA: `derived/demand_keys.json`; CALCULATION: `demand_keys.cjs`; ASSUMPTION: transplanting the general-demand increment to the requested consumption basis]

Narrow T is agriculture plus durable/nondurable manufacturing. Broad T adds summary cells 511, 512, 514, 523, 5415, 5412OP, 481, 483 and 55 (software/publishing, media, data, securities, computer/professional services, air/water transport and management). These summary cells are proxies: 511 is broader than software; 5412OP does not split all professional services. The reviewer used media 512; a no-media broad variant is preserved and differs by less than $0.04bn at each end. Government remains fixed; household services enter N with zero business tax. Agriculture stays on the central tax rule in K7; its separate reserve/refill alternative is below. [DATA: `derived/reallocation.json.tradable_cells`; SOURCE: frozen `job_capital.py:124–134`; ASSUMPTION]

The gates use all 161 wage columns: reallocation strength 0 returns the frozen jobs key within **1e−9bn**, and merging to one sector returns the frozen plain-share arm within **1e−6bn** at both readings. The merged sector pools all wages and retains the same zero-mining national tax vectors; it is a limiting aggregation, not the claim that putting every heterogeneous cell in T produces the plain key. An additional equal-intensity two-block test verifies cancellation for multiple demand shares, and a negative-refill test prevents clipping R_N at zero. [CALCULATION: `derived/reallocation.json.gates`, `test_reallocation.py`]

### New one-change arms

Entries are Δnet cost $bn, with paired conditional SDR SE in parentheses. [CALCULATION: `derived/reallocation.json`; negative cost is the sign convention above]

| Change from v7 | Union low | Union high | Lineage low | Lineage high |
|---|---:|---:|---:|---:|
| K7 narrow, national T intensity | -2.539315 (2.451977) | -0.853678 (1.193135) | -0.176029 (2.558295) | +0.250609 (1.246077) |
| K7 broad, national T intensity | -7.246830 (1.221031) | -3.374606 (0.637115) | -6.475352 (1.262638) | -3.047109 (0.660544) |
| K6 mining refill, narrow T | -1.732576 (0.614094) | -0.875850 (0.310437) | -1.854736 (0.638544) | -0.937605 (0.322797) |
| K6 mining refill, broad T | -1.093071 (0.387623) | -0.568456 (0.201585) | -1.170141 (0.403116) | -0.608537 (0.209642) |
| K7 plus mining refill, narrow T | -4.271890 (2.479006) | -1.729528 (1.204618) | -2.030764 (2.584564) | -0.686995 (1.257557) |
| K7 plus mining refill, broad T | -8.339901 (1.249978) | -3.943062 (0.650334) | -7.645493 (1.295241) | -3.655646 (0.675970) |
| Agriculture0 plus refill, narrow mobile T | -1.807016 (0.397215) | +0.134915 (0.248808) | -1.855937 (0.408179) | +0.136881 (0.254612) |
| Agriculture0 plus refill, broad mobile T | -0.136918 (0.291250) | +0.899167 (0.227615) | -0.142231 (0.298412) | +0.921089 (0.231881) |
| Network response 0.7 | +1.639506 (0.203363) | +1.197088 (0.146735) | +1.792362 (0.213423) | +1.304767 (0.154083) |
| Commercial-land response 0 | +1.501624 (0.040617) | +1.501624 (0.040617) | +1.611307 (0.042221) | +1.611307 (0.042221) |

Only the broad K7/reallocation combined low-side point arms exceed $5bn; the other standalone requested point changes stay below the bar. Group-weighted T intensities give union K7-with-mining −4.745414/−1.815476bn narrow and −8.229415/−4.162576bn broad; lineage −2.863777/−0.839779 and −7.549061/−3.809920bn. The reviewer's +4.9–8.5/+2.4–4.3bn tax-loss interval is not a reproduced receipt: its probe uses raw W_g/W cell tax exposure, demand alternatives and different destination weighting. This implementation keeps the exact frozen pooling, actual requested demand basis and live lineage additions. It does not copy the reviewer's output. [CALCULATION: `derived/reallocation.json`; SOURCE: read-only `~/.cache/llmx/lite/bare/f3762ca1b03f/probes/nontradable.py`]

At live payload demand, K7-only union Δ is −1.963498/−0.592825bn narrow and −7.047051/−3.294505bn broad; lineage +0.399787/+0.511462 and −6.275573/−2.967008bn. This is a demand-key sensitivity, not a second change hidden inside the primary probe. [CALCULATION: `derived/reallocation.json` live_demand arms]

**Mining/agriculture refill.** Mining's own taxes remain exactly zero. The low-side mining mobile tax intensity is $0.216840 per wage dollar for narrow T and $0.136803 for broad T (high $0.109617/$0.071145). The group mining wage units replace native mining labor; those natives leave T, releasing capital taxed at those mobile intensities. The declined agriculture-at-zero row also removes the central farm taxes and replaces its group farm wage units at T intensity **excluding agriculture**. At the narrow low end the refill term outweighs the removed farm tax, reversing the old unrefilled agriculture row's direction. At the high end the much lower mobile corporate response leaves a positive cost move. This is a response-model alternative, not observed mining/farm capital departure. [CALCULATION: `derived/reallocation.json`; ASSUMPTION]

**Network.** Cells 22 utilities, 513 telecom, 482 rail and 486 pipelines multiply their current three-line departure by 0.7. The property line retains its central land blend first, so this is a 0.7 network-mobility multiplier on current departure, not replacing the global property response with 0.7. [DATA: `derived/reallocation.json.network_cells`; ASSUMPTION]

**Commercial land.** This is the item lane's commercial/business-land response-zero arm: property responds at τ + (1−τ)(1−λ_b), not zero on the entire property line. Union +1.501624bn and lineage +1.611307bn at both ends. It exactly reproduces the frozen business_land_at_0 output within 1e−9bn. No new estimate of land-price elasticity is inferred. [CALCULATION: `derived/reallocation.json.gates`; DATA: frozen `national.json.land`, `.tpp`; ASSUMPTION]

**Price and Rybczynski directions.** Broad N has $44.345bn union / $32.493bn lineage positive refill wage units; narrow N is negative (−$27.755/−$45.052bn). At a fixed-price allocation with excess group supply over demand, removal creates upward N-price pressure; a rising N price supports local taxable rents/values and can retain capital, tending to offset tax loss. If removed demand exceeds supply, the initial price pressure is downward, tending to lower local taxable rents/values and add tax loss. These are conditional channels, not solved price equilibria: strict constant returns with pinned w and r fixes unit costs and leaves no independent N-price degree of freedom. Rybczynski composition is also conditional. With domestic capital fixed temporarily, labor removal makes K/L rise; at fixed goods prices the capital-intensive sector expands and the labor-intensive sector contracts, which can retain taxable capital and reduce the loss compared with proportional departure. If native refill instead draws labor from a capital-intensive mobile T sector, its capital release amplifies loss; the implemented `t_T R_N` gives that channel's sign. A multi-tradable equilibrium with capital inflow/outflow and industry tax rents can change either magnitude. Wage-tax intensity is not a direct K/L measurement. [INFERENCE; SOURCE: [Feenstra, Advanced International Trade, ch. 1, fixed-price endowment and zero-profit equations](https://assets.press.princeton.edu/chapters/s10615.pdf); DATA: `derived/reallocation.json.details`; SOURCE: local `matched_benefits_2026_09_19/model.py:48–56` for the one-sector capital opportunity-release term]

### K5 by SUT cells, with the 624 check

The existing functional proxy is preserved; this replaces its key only in the labelled cell arms. SUT 2024 Use_Summary.xlsx T00SUB/T00OSUB are parsed from the pinned BEA supply/use ZIP. National cells plus explicit published rounding close to each source total within 1e−6bn. Exact frozen pooled industry shares key the union; the case's G3plus/white wage calibration carries the added people. [SOURCE: https://apps.bea.gov/industry/release/zip/SUPPLY-USE.zip; CALCULATION: `k5_cells.py`, `derived/k5_cells_source.csv`, `inputs/k5_cells_pins.json`]

Each row changes cost equally at both ends; union / lineage paired conditional SE shown. [CALCULATION: `derived/k5_cells_summary.json`]

| Subsidy cell response | Union Δcost (SE), $bn | Lineage Δcost (SE), $bn |
|---|---:|---:|
| Agriculture1, 624+ORE included | +2.606473 (0.240465) | +2.714441 (0.242622) |
| Agriculture0, 624+ORE included | +0.740882 (0.125400) | +0.801587 (0.126178) |
| Agriculture0, 624 excluded | +0.407197 (0.120670) | +0.447970 (0.121183) |
| Agriculture0, 624+ORE excluded | +0.308872 (0.120492) | +0.342628 (0.120971) |

Agriculture's $8.349bn national subsidy contributes union $1.865591bn / lineage $1.912854bn. Social-assistance 624 has $3.742bn national T00OSUB and contributes $0.333684/$0.353617bn. ORE contributes $0.098325/$0.105342bn. [DATA: `derived/k5_cells_source.csv`]

**Overlap verdict:** the case already carries the entire NIPA subsidy aggregate in agricultural, housing, transport and other_subsidies (`full_account_spending_2026_09_20/builder.py:136–140`). Nonhousing responds 0 and housing responds 1 in the live v7 evaluation. Separately, other_federal_benefits, other_state_welfare and family_and_general_assistance respond 1; NIPA footnotes include nonprofit welfare among those benefits. BEA classifies some nonprofit subsidy payments as social benefits ([BEA PPP FAQ](https://www.bea.gov/help/faq/1408)). This is an identified potential program overlap; it does **not** identify 2024 cell 624's $3.742bn as a duplicate. Keep inclusion/exclusion arms. HS and government-enterprise cells are excluded, with their already priced housing/enterprise carriers intact. Do not add a new national spending line or net a gross SUT subsidy off measured corporate tax. Source vintage also differs from the frozen NIPA account. [DATA: `derived/k5_cells_summary.json.live_case_trace`; SOURCE: `subsidy-cells-evidence.md`; INFERENCE]

### Exact stacked candidates and recommendations

The least assumption-dependent adoption candidate remains **K2 only**, which removes foreign-source residence tax from a domestic-jobs source-tax item; its TY2021 SOI ratio remains an explicit vintage proxy. The preserved round-1 K1×K2 stack is a conditional legal-payroll model. The new stacked candidates below recompute corporate job exposure with K1 and domestic tax with K2 **before** K7; T/fixed corporate jobs use the group's new legal-payroll exposure, while national demand-release and native capital tax intensity use national domestic-source totals. Mining refill enters once. Nonfarm subsidies exclude 624 and ORE in the stress stack; they travel through the same N demand/T refill allocation rather than being appended at the old jobs key. Network and land variants change tax vectors before release/intensity. [CALCULATION: `reallocation.py`, `extended_integrate.py`; ASSUMPTION]

All figures are one simultaneous candidate minus v7 central, not a sum of two headline scenarios. [CALCULATION: `derived/extended_stacks.csv`]

| Conditional stack | Union Δ low/high, $bn | Lineage Δ low/high, $bn | Lineage headline low/high, $bn |
|---|---:|---:|---:|
| Narrow K1+K2+K7+mining+subsidy | +1.970566 / +0.940667 | +4.337878 / +2.059127 | 343.889896 / 425.708388 |
| Narrow K1+K2+K7+mining+subsidy+network+land | +5.406650 / +3.729463 | +8.044181 / +5.057133 | 347.596199 / 428.706394 |
| Broad K1+K2+K7+mining+subsidy | -2.175406 / -1.297813 | -1.249750 / -0.893353 | 338.302267 / 422.755908 |
| Broad K1+K2+K7+mining+subsidy+network+land | +1.328572 / +1.558876 | +2.541969 / +2.190070 | 342.093987 / 425.839331 |

Paired conditional SEs and cash endpoints are in `extended_stacks.csv`. Full narrow stack crosses the $5bn bar at both lineage ends; full broad stack does not. The exact full stack exceeds the naive sum of standalone changes by lineage **+$0.883801/+$0.470833bn narrow**, **+$0.996318/+$0.572420bn broad**. These cross terms include domestic-tax reallocation, K1's changed T exposure, and changed tax/spending release intensities. [CALCULATION: `derived/extended_summary.json.stack_diagnostics`]

| Refinement | Recommendation | Load-bearing reason |
|---|---|---|
| K1 legal payroll | **Arm**; preserve conditional K1×K2 candidate | 2022 propensity transported to 2024; within-cell selection remains unobserved |
| K2 foreign-source tax | **Adopt as measurement/scope correction** | Domestic US-jobs item should not carry a foreign-operations residence tax; vintage ratio stays explicit |
| K3 documentary | **Arm** | Gross source component can be priced, but full housing-tax reconciliation remains open |
| K3 special assessments | **Reject additive correction** | ACS owner property concept already contains special assessments |
| K4 finer corporate detail | **Arm**; retain central summary key | Suppression and concordance limit the measured refinement |
| K5 cell subsidies | **Arm** | Recipient industry improves the key; program response and nonprofit/enterprise overlap not identified |
| K6 mining refill / agriculture0 refill | **Arm** | Applies the fixed-resource reasoning consistently, but native destination intensity is an assumed response |
| K6 support/equipment departure | **Reject as measurement correction**; preserve prior sizing arms | Reproducibility of equipment does not show that it departs when jobs refill |
| K7 two-block | **Arm** | Captures a real omitted reallocation mechanism; sector classification, prices and factor response remain conditional |
| Network 0.7 | **Arm** | Response value is stipulated rather than measured |
| Commercial land 0 | **Arm** | Price-response scenario, not an observed elasticity |
| Exact full stack | **Conditional stress candidate** | Publish with component assumptions; do not silently replace the adopted central |

[INFERENCE: recommendations; DATA: retained and extended lane source traces]

### Joint same-direction and quadrature ranges

The decision-09-27 outer-range convention is applied to **point-arm components**: take one extreme per refinement family including central zero, sum all upward moves and all downward moves separately, and also root-sum-square those same selected components. Broad T is fixed for the K7, mining and farm-refill components throughout. K3 uses documentary only (known assessment overlap excluded), K4 strict C detail, K5 one agriculture/overlap alternative at a time; K1 uses industry-size point refinement. Unidentified legal-form selection bounds stay outside this point-arm range. Original K5 functional and new cell keys are alternatives, never summed; original K6 support/equipment departures are replaced by refill alternatives in the joint families. [CALCULATION: `extended_integrate.py` families; SOURCE: `decisions/2026-09-27-main-case-capital-return-and-long-run-responses.md:96–98`]

| End, population | All downward Δ | All upward Δ | Quadrature downward Δ | Quadrature upward Δ |
|---|---:|---:|---:|---:|
| low, union | -9.525530 | +10.966852 | -7.380772 | +5.166663 |
| low, lineage | -8.917425 | +11.706278 | -6.648205 | +5.542003 |
| high, union | -4.858546 | +8.135473 | -3.523947 | +3.652098 |
| high, lineage | -4.648129 | +8.619226 | -3.239327 | +3.862137 |

The lineage headline outer endpoints are **$330.634593–432.268487bn** if all signed point-arm components move together, or **$332.903812–427.511397bn** in quadrature. At the low central end specifically, all-down/all-up levels are $330.634593/$351.258296bn; at the high end $419.001132/$432.268487bn. These are arithmetic sensitivity envelopes, not confidence intervals and not a jointly solved GE allocation. Shared-vector interactions belong to the exact candidate table above; the component-envelope convention does not identify them or independent probabilities. [CALCULATION: `derived/extended_summary.json.joint`; ASSUMPTION]

### Fail-open regression and corrected firm-size prose

The frozen source's `record()` at `job_capital.py:469` uses `rsp = rsp or LINE_RESP`. This extension does not reuse that fallback. Its live `record()` uses `central_responses if rsp is None else rsp` and rejects an explicit empty/incomplete mapping with `[BLOCKED]`. The test distinguishes default None, explicit empty dict (raises), and valid all-zero responses (zero outcome); production baseline calculation calls this same helper. Frozen source stays untouched. [CALCULATION: `reallocation.py:record`, `test_reallocation.py`]

Parent correction for `job_capital_taxes_2026_10_14/RESULT.md:490–493`: the code at 663–669 pools industries. The requested within-cell calculation actually finds a smaller gap: among private BEA cells, **41.54%** of adjusted union wages are at employers under 100, **34.01%** nationally, **38.91%** nationally reweighted to the union's industry wage mix. The within-cell gap is **+2.63 percentage points (SE 0.82)**. For employers 1,000+, union **38.08%**, national **46.76%**, reweighted national **41.87%**; within gap **−3.80 points (SE 0.86)**. This is a standardized mean, not every industry's sign. Raw/private adjusted values differ from the frozen pooled all-industry values because government/households are excluded and the exact top/fill-in rule is retained. [CALCULATION: `within_firm.py` → `derived/within_firm.json`; SOURCE: `within-firm-evidence.md`]

The raw under-100 gap decomposes **+7.530 = +2.627 within +4.903 cell mix**; 1,000+ **−8.683 = −3.799 within −4.884 cell mix**. The 256-row cell/size table carries all individual gaps/contributions and conditional SEs. All-replicate decomposition and generation/weight conservation gates pass at 1e−12. This supports the sign of the legal-payroll concern but does not directly measure C-only group payroll. [CALCULATION: `derived/within_firm.csv`, `.json`]

### Extension verification and scope

The 207 reallocation gates, 62 subsidy gates, 32 within-cell gates and 19 integration gates pass. Six reallocation/response tests plus three subsidy tests pass. New source inputs are pinned; computational tolerances were not loosened. `extension-code-check.md` records the independent scoped code review. The whole-lane replay includes all original eight commands, the five new live commands and both new test files; its receipt is `_cache/extension_rerun.log` / `.json`. [CALCULATION: output gates and checks]

Reproduce extension after the preserved round-1 eight commands:

```sh
node infra/immigration-fiscal/job_capital_key_refine_2026_10_14/demand_keys.cjs
PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/job_capital_key_refine_2026_10_14/within_firm.py
PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/job_capital_key_refine_2026_10_14/k5_cells.py
PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/job_capital_key_refine_2026_10_14/reallocation.py
PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/job_capital_key_refine_2026_10_14/extended_integrate.py
PYTHONDONTWRITEBYTECODE=1 uv run --no-project python3 -m pytest -p no:cacheprovider infra/immigration-fiscal/job_capital_key_refine_2026_10_14/test_reallocation.py infra/immigration-fiscal/job_capital_key_refine_2026_10_14/test_k5_cells.py -q
```

The case and the item lane remain read-only. No merge, stage or commit. No additional scientific capability was retired. This is the full-adjustment fiscal response frame for other residents, with source measurements separated from assumed counterfactual responses. LLM dispositions can influence response-model selection; both directions and source/construction checks are retained. [FRAMING-SENSITIVE; DATA: `notes/llm-bias-caveat.md`; INFERENCE]

Final extension receipt (2026-10-14): **14/14 commands rc0, IDENTICAL64/64, exit0, no --allow-unrun**; nine tests passed. Whole replay 62.68s, peak child RSS 2.005GB, measured by Python perf_counter/resource. Independent scoped review found no material defect; it independently recovered K1/K2/reallocation/mining stack within 5.69e−14bn. All prior scientific output bytes were preserved. No git write performed. [CALCULATION: `_cache/extension_rerun.log`, `.json`; SOURCE: `extension-code-check.md`]
