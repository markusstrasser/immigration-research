**Verdict:** Keep agricultural subsidies at response zero under the fixed-land premise. Withhold a new central response for the remaining programs: the frozen NIPA residual mixes crop insurance, rail/transit support and other programs, and any transfers to government enterprises need their existing receipt offset. Computed gross-spending sensitivities add $0.013–2.317bn on the identified union and $0.015–2.469bn on the lineage at each endpoint; these are proxy arms, not a new measured central. [CALCULATION: `k5_subsidies.py` → `derived/k5_summary.json`]

Scope: NIPA non-housing subsidies, program amounts, industry keys, and full-adjustment responses. Frozen item-6 source files remain read-only. K5 owns only files prefixed `k5_` and this evidence note; other agents own the lane's common integration.

## Evidence log

- 2026-10-14: Read the worker brief and item-6 RESULT. The central holds business subsidies at response zero. Agriculture's fixed-land rule and transit's treatment must be distinguished from other programs before computing any candidate. [SOURCE: worker brief K5; `job_capital_taxes_2026_10_14/RESULT.md`]

## Program amounts and rules

The primary frozen BEA Section 3 workbook is reused read-only, sha256 pinned in `inputs/k5_pins.json`. Its Table 3.13 is the actual source of the case's subsidy lines. It contains $94.239bn total, $60.261bn housing assistance already priced separately, and $33.978bn non-housing. The full program ledger is `derived/k5_programs.csv`; all numbers are parsed from the workbook and each case line reproduces to 1e-6bn. [DATA: `sources/immigration-fiscal/data/external/bea_nipa/Section3All_xls.xlsx`, T31300-A]

| Program | National $bn | Key in tested arm | Response recommendation |
|---|---:|---|---|
| Agricultural | 8.233 | Crops/agriculture, 111CA | 0 under the same fixed-land rule as mining |
| Housing | 60.261 | Existing housing-support key | Already response 1; excluded from K5 |
| Maritime | 0.005 | Water transportation, 483 | Withhold; full response 1 is only a sensitivity |
| Air carriers | 0.400 | Air transportation, 481 | Withhold; full response 1 is only a sensitivity |
| Federal Other | 24.627 | Unidentified program mix | Withhold; plain-wage and functional-mix proxies beside |
| State/local | 0.713 | Railroad, 482 proxy | Withhold; full response 1 is only a sensitivity |

[DATA: Table 3.13 lines 3–8; CALCULATION: `derived/k5_programs.csv`; ASSUMPTION: industry assignments and response tests]

The Table 3.13 footnote identifies Federal Other as largely railroads, mass transit systems and FCIC. The MP-5 government-transactions manual identifies state/local subsidies as largely railroad payments. This is evidence against assigning the residual indiscriminately to all business capital. The older manual supplies program identities, not current program amounts. [SOURCE: frozen Table 3.13 footnote 1; BEA MP-5, subsidies section II-61 and III-39; DATA: pinned local `bea_mp5_government_transactions.txt` lines 4566–4583 and 9024–9034]

Agriculture's zero is conditional on fixed acreage/world prices and replacement workers under full adjustment. It is not an observed causal response. The counterargument is that production, crop mix and participation could change if replacement labor costs or domestic prices change; that would require departing from the case's premise and measuring the resulting acreage/insured-liability response. Crop-insurance payment to an insurance provider does not alone make its demand independent of the fixed crops insured. [ASSUMPTION; INFERENCE: item-6 RESULT fixed-factor argument]

For air, maritime and rail/transit, response 1 is the strongest scaling interpretation: fewer residents and fewer local businesses reduce domestic service demand. Counterevidence is fixed rural routes, national security, contractual support and replacement demand. A carrier's wage share does not measure the group's passenger or shipper share. Transit also serves the whole local population, rather than only employees of transit firms. Thus these wage keys are explicitly sensitivities. [INFERENCE; ASSUMPTION]

## Results, one change from the current central

Positive numbers increase the group's fiscal cost: the subsidy saving on removal benefits others. The deterministic engine probe changes the spending line's response from 0 to 1 and confirms that welfare falls by exactly its assigned spending; fiscal cost is minus welfare. [CALCULATION: `k5_subsidies.py` engine sign guard against `assumption_explorer_2026_09_21/engine.js`]

| Gross spending arm | Union delta $bn | Union SE | Lineage delta $bn | Conditional SE |
|---|---:|---:|---:|---:|
| Named air/maritime, response 1 | +0.012605 | 0.003015 | +0.014687 | 0.003187 |
| State/local railroad proxy, response 1 | +0.027219 | 0.017789 | +0.030315 | 0.017858 |
| Unclassified Federal Other + state/local at plain wage key, response 1 | +1.996575 | 0.036199 | +2.144355 | 0.037680 |
| Previous row + named air/maritime | +2.009180 | 0.037043 | +2.159042 | 0.038582 |
| Functional-mix proxy, response 1 except agriculture/housing | +2.316502 | 0.076455 | +2.469310 | 0.080010 |

[CALCULATION: `derived/k5_summary.json` arms; `_cache/k5_changes.npz`]

Each tested response is the same at low and high, personal allocation, set and cash. The identified union is the frozen 39.71M account, and the lineage adds the case's G3+ and white wage-calibrated factors for its 42.75M members. SDR uses all 160 CPS replicates. Added-ancestry counts and wage factors, program amounts, proxies and responses are fixed, so the lineage SE is conditional. Each tested proxy lies below the $5bn review bar at both ends; this is not an exhaustive upper bound on an unidentified program allocation. [DATA: `derived/core.json`; CALCULATION: same]

The plain-wage arms divide each replicate's total corrected group wages by national wages directly. Their exported national vectors are diagnostics; applying pooled industry shares to those vectors would create a different key. Integration must use the exact arrays in `_cache/k5_changes.npz`. Array keys are `<arm>__union`, `<arm>__lineage`, `<arm>__G1`, `<arm>__G2`, `<arm>__G3plus`, `<arm>__white`, each length 161. Positive entries are changes in modeled group cost. Separate `<arm>__others_resource_cost_change_on_removal_*` arrays use the opposite sign. [CALCULATION: `k5_subsidies.py`]

## Why the functional-mix arm is only a proxy

Table 3.17 offers a function split: transportation, general economic/labor affairs, agriculture, energy, housing/community and health. Its agricultural amount is $0.412bn below Table 3.13's program amount, and its housing/community amount is $2.513bn above the housing program. These are different definitions, not permission to splice rows together. The function ledger preserves its own rows and an explicit $0.001bn rounding residual. [DATA: `derived/k5_functions.csv`; CALCULATION: `k5_summary.json` definition_conflicts_bn]

The functional sensitivity keys transport to all transportation wages; general economic/labor affairs to all private industries; energy to utilities; housing/community beyond the separately priced housing program to construction, nonresidential real estate and social assistance; and health to the health/social-assistance cells. Within each selected pool it spreads national amounts by national CPS wages, then applies the frozen group industry shares. Every assignment is an assumption. It preserves functional agriculture at 0, which is not precisely the program-defined agricultural zero. [ASSUMPTION; CALCULATION: `k5_subsidies.py` wage_pool]

The pinned 2024 supply-use table separately provides subsidies on products and other subsidies on production by industry, exported to `derived/k5_sut_subsidies.csv`. Its newer vintage sums to $96.054bn, $1.815bn above the frozen NIPA total. Housing and state/local-enterprise cells also mix subsidy programs; this table cannot replace the frozen national or identify the needed enterprise transfer amounts. It is preserved for reconciliation, not used silently as a substitute. Independent $mn cell rounding is kept explicitly. [DATA: 2024 Use_Summary.xlsx, T00OSUB/T00SUB; CALCULATION: `k5_subsidies.py`]

## Enterprise offsets and separately carried transfers

BEA defines subsidies to include payments to private business and government enterprises at another government level; current enterprise surplus includes the cross-level subsidy receipts. The case already responds to enterprise surplus at 1. Reducing a subsidy paid to an enterprise lowers its subsidy revenue by the same amount, reducing the government's enterprise surplus receipt: the gross spending saving must be paired with that revenue loss, using a consistent key. Adding the spending saving alone would count an internal government transfer. No primary split in the inspected frozen tables identifies the amount of Federal Other paid to such enterprises. Therefore the gross arms cannot be promoted into a central net saving. [SOURCE: https://www.bea.gov/help/glossary/subsidies; https://www.bea.gov/help/glossary/current-surplus-government-enterprises; DATA: `main_case_long_run_2026_09_27/RESULT.md` enterprise treatment]

Housing assistance is already carried separately and excluded throughout K5. Capital investment grants, tax expenditures classified as negative taxes, business current transfers and payments classified as social benefits are outside these NIPA current-subsidy rows. They cannot be added as extra subsidy programs without tracing their existing account carriers. [SOURCE: BEA MP-5; DATA: case model spending families]

## Gates and reproduction

K5 passes all 34 reported gates: primary input pins, exact labels/units, program and case-line closure at 1e-6bn, explicit functional and SUT rounding closure, frozen positive-control and weight-conservation gate reuse, all 161 generation replicate sums at 1e-9bn, vector nonnegativity, and engine sign. Peak RSS was 57.7MB and elapsed time 0.40 seconds, measured with Python resource/time. [CALCULATION: `k5_subsidies.py` → `derived/k5_summary.json` and `_cache/k5_runtime.json`]

```sh
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/job_capital_key_refine_2026_10_14/k5_subsidies.py
uv run --no-project python3 -m py_compile infra/immigration-fiscal/job_capital_key_refine_2026_10_14/k5_subsidies.py
```

- 2026-10-14 20:30:24 JST (from `date`): K5 build and compile both exit 0. Root corrected the initially proposed inverted spending sign; deterministic engine sign guard now protects it. Frozen source files remain read-only. The parent owns the whole-lane rerun and adoption decision.
- Owned-output rerun: `IDENTICAL: 6/6`, exit 0, including all five `derived/k5_*` files and exact replicate NPZ. A varying runtime gate payload and unordered set iteration initially broke byte reproducibility; runtime values now stay only in ignored `_cache/k5_runtime.json`, and case-line gate iteration is sorted. All calculations and sign guards reran successfully.
