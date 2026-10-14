**Verdict:** Complete conditional K1 arms; sector × enterprise-size changes lineage net cost +$1.814 / +$0.671bn,
below the $5bn bar. Public margins do not identify the group's actual C-corporation wage key.

Initial status, superseded: source verification in progress; no point correction admitted. Corporate legal form and
enterprise size must both match before admitting a size arm. [ASSUMPTION]

2026-10-14 20:36 JST — completed verification and computation. The conditional **sector × enterprise-size** legal-form
proxy raises net fiscal cost by **$1.792 / $0.663bn on the identified union**, and **$1.814 / $0.671bn on the
42.75M lineage**, low / high ends, personal allocation. Both are below the $5bn review bar. These are model-based
changes, not observed C-corporation wages of the group. [CALCULATION: `k1_legal.py` → `derived/k1_summary.json`]

| K1 rule, each one change from frozen central | Union low / high delta ($bn) | Union paired SE low / high | Lineage low / high delta ($bn) | Lineage conditional paired SE low / high | Status |
|---|---:|---:|---:|---:|---|
| National enterprise-size legal profile within frozen tax industries | +2.029208 / +0.750807 | 0.523732 / 0.193781 | +2.056985 / +0.761085 | 0.537451 / 0.198857 | Below bar; conditional arm |
| Sector × enterprise-size legal profile within frozen tax industries | +1.791833 / +0.662978 | 0.478059 / 0.176882 | +1.813543 / +0.671011 | 0.491671 / 0.181918 | Below bar; conditional arm |

Corporate targets are $39.820927bn union and $43.272567bn lineage in the sector-size proxy, before responses 1 / 0.37.
The complete item becomes −$64.689476 / −$39.602292bn union and −$69.957594 / −$42.695876bn lineage. Business property,
other production taxes, mining zero, allocation, tax amounts by fine cell, and all responses remain frozen.
[CALCULATION: `derived/k1_summary.json` results.industry_size; DATA: `derived/core.json` responses]

The neutral legal-probability control recovers each frozen pooled corporate target in all 161 replicate columns to
1e-9bn. The parent common core reproduces all five frozen output files byte for byte and both adopted lineage controls.
[DATA: `derived/k1_summary.json` gates; `derived/core.json` gates/control]

Source and method:

- Primary SUSB 2022 workbook has annual payroll by **establishment industry sector × enterprise employment size × LFO**.
  Enterprise size sums employment over an enterprise's establishments; this is consistent with CPS NOEMP's all-location
  employer size. S corporation is a separate category. The corporate category is **C corporations and other corporate
  legal forms**, not a pure tax-form-1120 population. [SOURCE: https://www2.census.gov/programs-surveys/susb/tables/2022/us_state_naicssector_lfo_2022.xlsx;
  https://www.census.gov/programs-surveys/susb/about/glossary.html;
  https://www.census.gov/programs-surveys/susb/technical-documentation/data-user-resources/legal-form-of-organization.html]
- Source <5 + 5–9 → <10; source 10–19 + 20–99 and CPS 10–24 + 25–99 → 10–99; source/CPS 100–499 match; CPS
  500–999 + 1000+ → source 500+. No interpolation. NOEMP 0 carries zero national and group wage dollars in every
  common-core replicate. [DATA: `derived/k1_payroll.csv`, `derived/k1_unknown_size.csv`; CALCULATION: aggregate_bins]
- SUSB's finest published joint LFO × enterprise-size table is sector level. Economic Census 2022 publishes separate
  fine-industry LFO and firm-size tables; their principal API groups contain no joint dimension. ABS 2023 company-summary
  metadata lacks LFO; CBP's legal-form size is establishment size. These were checked in pinned primary API metadata.
  [DATA: `inputs/k1_pins.json` ec2022_lfo_group/ec2022_firmsize_group/abs2023_variables/cbp2023_variables;
  SOURCE: https://www.census.gov/programs-surveys/susb/technical-documentation/methodology.html]
- Let p be Census corporate payroll / all-form payroll at matching sector and size. Apply p to both group and national
  CPS wage arrays, keeping the frozen thin-cell pool. The revised frozen cell share is its current share times
  `(Σ p × group wages / Σ p × national wages) / (Σ group wages / Σ national wages)` in the same pool. Neutral p=1 thus
  gives the current share exactly. Top-wage allocation, row-4 weights and generation correction come from common core.
  [CALCULATION: k1_legal.py calculate; DATA: `_cache/core.npz` cell_pool/size_wages/shares; ASSUMPTION: conditional legal-form
  exchangeability of group and national payroll within sector and employer size]
- Crop/animal production (111CA), rail (482) and government enterprises (GOVF/GOVSL) retain the frozen key, since SUSB
  does not match their payroll universe. National corporate tax held this way is $6.406949bn. Some excluded funds remain
  inside merged 523 and notaries inside 5411; application of broad-sector profiles there is explicitly conditional.
  [SOURCE: SUSB methodology exclusions; DATA: `derived/k1_uncovered_cells.csv`; INFERENCE: mixed-cell scope]
- Source year 2022 is transported to 2024 wages. Fine tax industries inherit their broad sector profile. The same
  profile applies to group and national wages; the group’s actual employer legal form is unobserved. [ASSUMPTION]

IRS cross-check:

IRS SOI 2022 Table 5.3 (C returns excluding S, REIT, RIC) gives $3,345.092703bn salary deductions and $212.915290bn
officer compensation. Census corporate payroll is $4,659.260696bn: IRS salary plus officer is 76.3642% of that.
IRS's C share of C+S salary plus officer compensation is 70.1464%, Census's C share of C+S payroll 70.5309%.
These are consistent in aggregate legal mix, but **do not establish payroll parity**. SOI salary deductions exclude
COGS labor, reduce some credits and exclude officers; industry is the consolidated return, not the establishment.
Census's agriculture sector excludes farm production (IRS/Census ratio 4.513), and its trade and administrative-service
patterns differ sharply from SOI. The sector checks are diagnostic and do not rescale Census probabilities.
[SOURCE: https://www.irs.gov/pub/irs-soi/22co53ccr.xlsx; https://www.irs.gov/pub/irs-soi/22co61ccr.xlsx;
https://www.irs.gov/pub/irs-pdf/p16.pdf, Salaries and Wages/Compensation of Officers/Consolidated Returns definitions;
DATA: `derived/k1_irs_crosscheck.csv`, `derived/k1_summary.json` irs_national_crosscheck]

Identification envelope:

Keeping the transported national corporate-payroll marginals but removing group legal-form exchangeability, each
group's corporate wage numerator in a matched cell-size lies between `max(0,pN−(N−G))` and `min(G,pN)`.
The resulting union delta envelope is [−34.492,+40.847]bn low and [−12.762,+15.113]bn high; the lineage relaxed outer
envelope is [−36.303,+43.061] and [−13.432,+15.933]bn. These are allocation bounds under the transported marginal
assumption, not confidence intervals, plausible policy ranges, or sharp jointly feasible lineage bounds. They show
why public payroll margins alone do not identify a point correction. [CALCULATION: results.industry_size_selection_min/max;
ASSUMPTION: transported national C payroll marginals]

Recommendation: retain the sector-size version as the preferred **conditional K1 sensitivity** and the size-only
version as a comparator. Do not describe either as a verified group C-wage key or adopt it solely because the source
separates C and S. Admission of an empirically identified correction would require matched employer legal-form wages
for the group, or evidence validating conditional exchangeability within the common bins. [INFERENCE]

Checks: 243 reproducible gates pass, plus the resource ceiling in stdout. SUSB disjoint-size, form and national-sector
payroll closures are <=1e-6bn; SOI sector salary and officer totals close <=1e-6bn; probabilities stay in [0,1]; the
neutral control recovers frozen pooled targets; generations conserve at 1e-9bn; every exchangeable estimate lies in its
selection envelope. Unpublished other-form size rows are recorded with their arithmetic residual and never used as
zero or as legal probabilities. The unclassified sector's omitted size cells are unused; its total participates in
national closure. [DATA: derived/k1_summary.json gates; derived/k1_unpublished_rows.csv]

Reproduce:

```sh
# Staged bytes are already pinned; network only needed on a fresh acquisition.
OPENBLAS_NUM_THREADS=1 uv run --no-project --with openpyxl python3 infra/immigration-fiscal/job_capital_key_refine_2026_10_14/k1_legal.py --acquire
OPENBLAS_NUM_THREADS=1 uv run --no-project --with openpyxl python3 infra/immigration-fiscal/job_capital_key_refine_2026_10_14/k1_legal.py
```

Log: 2026-10-14 20:36:26 JST (`date`), final computation 1.901s and peak RSS 0.116GB measured by Python
time.perf_counter/resource.getrusage; compile check passed. Whole-lane rerun is owned by the parent; a K1-only rerun is
logged below with explicit peer-script exclusions.

Files covered: k1_legal.py; every inputs/k1_pins.json source (13); derived/k1_* outputs; _cache/k1_targets.npz.
Files skipped: other lane builders/results belong to peer workers; frozen item6 and adopted v7 are read-only; no research
docs, git metadata, stage, merge or commit modified.

2026-10-14 20:39 JST — K1-only `scripts/rerun_lane.py` finished **IDENTICAL: 36/36**, exit 0. Explicit
`--allow-unrun` exclusions: core.py, housing_keys.cjs, k236.py, k3_sampling.py, k4_detail.py, k5_subsidies.py; these are
peer-owned shared-core/other-arm builders, and this rerun claims only K1 execution. Parent owns whole-lane execution.

2026-10-14 20:39:29 JST (`date`) — second K1-only rerun was IDENTICAL 40/40 but exit 3 because the parent added
refine.py during the run. Repeated with explicit `--allow-unrun refine.py` (parent-owned integrator): **IDENTICAL 40/40,
exit 0**. No computational output changed; parent subsequently owns the complete eight-script rerun.

Every changed path, relative to `infra/immigration-fiscal/job_capital_key_refine_2026_10_14/`:

```text
k1_legal.py
k1-evidence.md
inputs/k1_pins.json
derived/k1_irs_crosscheck.csv
derived/k1_payroll.csv
derived/k1_summary.json
derived/k1_uncovered_cells.csv
derived/k1_unknown_size.csv
derived/k1_unpublished_rows.csv
_cache/k1_22co53ccr.xlsx
_cache/k1_22co61ccr.xlsx
_cache/k1_abs2023_variables.json
_cache/k1_cbp2023_variables.json
_cache/k1_ec2022_firmsize_group.json
_cache/k1_ec2022_lfo_group.json
_cache/k1_irs_tables.html
_cache/k1_p16_2022.pdf
_cache/k1_p16_2022.txt
_cache/k1_susb_2022.xlsx
_cache/k1_susb_glossary.html
_cache/k1_susb_lfo.html
_cache/k1_susb_methodology.html
_cache/k1_susb_tables.html
_cache/k1_targets.npz
```
