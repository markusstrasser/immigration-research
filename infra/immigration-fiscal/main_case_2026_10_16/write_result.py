"""Render the candidate's documented contract from its executed receipts."""
from __future__ import annotations

import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
FISCAL = HERE.parent
sys.path.insert(0, str(FISCAL / "scripts"))
from memory_budget import require_within_budget


def load(name):
    return json.loads((HERE / "derived" / name).read_text())


def band(values):
    return " / ".join(f"{value:.6f}" for value in values)


def main():
    summary = load("summary.json")
    v = summary["v9"]
    old = summary["v8"]
    market = load("market_check.json")
    basket_source = json.loads((FISCAL / "consumption_tax_bases_r5_2026_10_15/derived/evaluation.json").read_text())
    business_source = next(r["delta_bn"] for r in basket_source["records"]
        if r["arm"] == "business_sales_customs" and r["which"] == "set" and r["end"] == "low")
    gates = {}
    for name in ["g1", "contract", "generality", "api_check", "coverage_check"]:
        file = HERE / "derived" / f"{name}.json"
        gates[name] = json.loads(file.read_text()) if file.exists() else {"pass": False}
    passed = all(value.get("pass") is True for value in gates.values())
    state = "PASS" if passed else "INCOMPLETE GATES"
    if v["stub13"]:
        state += " — STUB-13"
    parts = []
    columns = [(which, i) for which in ["set", "cash"] for i in [0, 1]]
    totals = [v["band_bn"][i] if which == "set" else v["cash_set_bn"][i] for which, i in columns]
    starts = [old["band_bn"][i] if which == "set" else old["cash_set_bn"][i] for which, i in columns]
    labels = {
        "veterans_compensation": "13 Military service",
        "income_security_administration": "14 Retirement administration (partial)",
        "public_college_response": "15 Colleges",
        "native_minor_calibration": "16 Native-minor calibration",
        "coverage_tenure": "17 Coverage tenure, alone",
        "consumption_tax_bases": "18 Household taxable basket",
        "passthrough_source_tax": "19 Pass-through source taxes",
        "one_rate": "20 One Trustees rate",
        "health_residual_key": "21 Non-military health residual key",
    }
    rounded_parts = [0.0] * 4
    for key, changes in v["change_by_item"].items():
        if key == "one_rate" and not v["item19_central"]:
            parts.append("| 19 Pass-through source taxes — beside | +0.000000 | +0.000000 | +0.000000 | +0.000000 |")
        row = [round(changes[which][i], 6) for which, i in columns]
        rounded_parts = [a + b for a, b in zip(rounded_parts, row)]
        parts.append("| " + labels[key] + " | " + " | ".join(f"{x:+.6f}" for x in row) + " |")
    residual = [round(end, 6) - round(start, 6) - delta for end, start, delta in zip(totals, starts, rounded_parts)]
    parts.append("| Interactions, balanced display | " + " | ".join(f"{x:+.6f}" for x in residual) + " |")
    parts.append("| **v9** | " + " | ".join(f"**{x:.6f}**" for x in totals) + " |")
    companion_rows = []
    for name, row in v["companions"].items():
        cash = row.get("cash_set_bn", row.get("cash", {}).get("band_bn"))
        label = "household-sharing allocation across members and non-members, item 11 excluded; not a distribution inside the group" if name == "shared_allocation" else name
        companion_rows.append(f"| {label} | {band(row['band_bn'])} | {band(cash) if cash else 'see structured cash record'} |")
    restored = v["companions"]["first_year"]["military_restoration_at_ends"]
    military_screen = [sum(method[e]["direct_bn"]+method[e]["coverage_bn"] for method in restored)/len(restored) for e in (0, 1)]
    military_net = [sum(method[e]["total_bn"] for method in restored)/len(restored) for e in (0, 1)]
    pair = v["beside"]["item6_legal_form_pair"]
    legal_rows = []
    for name, reading in pair["readings"].items():
        row = reading["set"]
        item19 = [p["item19_bn"] for p in row["parts_at_ends"]]
        w09 = [p["w09_bn"] for p in row["parts_at_ends"]]
        total = [p["sum_bn"] for p in row["parts_at_ends"]]
        legal_rows.append(f"| {name} | {band(item19)} | {band(w09)} | {band(total)} | {band(row['band_bn'])} | {band(reading['cash']['band_bn'])} |")
    consumers = {
        "Generation account": "Use new run_generations_v9.cjs/v9_split.cjs oct16 files; route16/17 generation vectors; retain a/b conventions and source13 line parts. Read population_v9. Item19 is absent centrally; only its beside arm routes added_G3plus into G3plus.",
        "Late-arrival line": "Read oct16 generation results and calibrated observed/missing counts; keep constructed coverage and unlocated calibration outside identified arrival cells unless an explicit allocation is supplied.",
        "Debt legacy": "Apply selected line and post-engine fiscal parts and military response0; keep item19/W09 beside. Retain capital-return resource costs outside borrowing and financing. Refresh counts and pins.",
        "Sept24 propagation and pairing": "Read oct16 corrections and selected meta.items ranges; preserve source carrier mappings. Add16/17 by generation and actual item20 capital revaluation; recheck splits instead of scaling v8 totals. Item19/W09 travel only as beside arms.",
        "Uncertainty propagation": "Retain measured conditional CPS stacks, calibrate16 using the source survey construction, and model17/PES covariance separately. No joint total SE is identified; never add generation SEs.",
        "Winners and losers": "Use found v9 ends and complete source-side fiscal/production/post decomposition; include calibrated count and military line components and tenure generation composition. Keep item19/W09 ownership arms beside.",
        "Historical back-cast": "Transport each v9 component/count under stated historical rules; keep20's Trustees rate separate from nominal financing and retain a modeled-backcast label for earlier years.",
        "Distribution weights": "Classify13 by original source lines,14 by retirement administration,15 by college operating/capital, and16/17 by declared source parts. Apply capital-rate revaluation and calibrated denominator explicitly; exclude19/W09 centrally.",
        "World ledger": "Use oct16 generation payloads, calibrated counts and military fiscal parts; item19/W09 are beside. Keep opportunity-capital charges outside budget flows. Comparator corrections need their own population rules.",
        "Household/within-group split": "Use military by-line/population/generation parts, receipt carrier policy and full count-item source files. Calibrated survey weights change existing records; omitted people remain constructed. Allocate or retain an unlocated bucket.",
        "White replacement comparator": "Apply the same military, college, taxable-basket and capital-rate rules on white keys; item19/W09 stay beside and need comparable job/owner keys if shown. Do not impose Mexican calibration or Hispanic omission rates on whites.",
        "Black rough comparator": "Use symmetric applicable13–15/18/20 rules; keep19/W09 beside and origin-specific16/17 on the Mexican side. Preserve rough-comparator limitations and explicit source-key gaps.",
        "Indian full account": "Refresh main-case and white/debt libraries; implement applicable military/college/basket/rate rules on Indian source keys; keep19/W09 beside. Mexican native calibration and PES coverage are not transferable automatically.",
        "Legacy comparators": "Refresh annual-flow, stock, population and case pins from applicable oct16 consumers; separate imported pension stock valuations, nominal financing and the new real resource rate.",
        "Pension legacy": "Read population_v9 and source13 military parts; retain imported pension normal costs and legacy interest scope. Item20 changes annual capital return, not the booked legacy pension liability.",
        "Break conditions": "Use new firstYear/adjustedRun and selected13–18/20 rules; zero capital in first-year pricing. V9_FIRST_YEAR_PASS applies only when item19 is explicitly selected beside. Resolve actual v9 ends, never retain old endpoint indices by assumption.",
        "Main-case decomposition": "Publish13–18/20,16×17,15×20 and coverage repricing/interactions separately; carry all selected post amounts and source-side signs. Item19 has zero central contribution; item6 legal-form pair is a naive beside reading. Reconcile to set/cash totals and preserve old steps as history.",
        "Closed budget": "Read the rebuilt oct16 decomposition and calibrated denominator, with set/cash distinctions. Re-pin budget excesses; the capital-return charge is not borrowing.",
        "Nonresponse/reweight.py (outside table)": "Use calibrated observed weights and the separately constructed coverage people; explicitly state any reweighting of16/17 rather than applying the correction twice.",
        "Public charge (outside table)": "Update membership/decomposition and eligible source cells; keep constructed coverage and calibration distinct from new identified applicants. Preserve source NG/NC limitations.",
        "Post-2024 law (outside table)": "Rebuild the eligible tax/benefit subset on calibrated records and preserve separate16/17 source constructions. The partial-law companion does not identify a full post-2024-law v9 total.",
        "Number drift audit (outside table)": "Add oct16 source-map, pairing, hashes and population_v9/per-member fields only on adoption. Parent owns live_case.json and central prose propagation.",
        "Evidence map/overview": "Move only at operator request; consume rebuilt v9 item/interactions and current count with explicit scope, source18 compatibility and coverage assumptions.",
        "Assumption explorer": "Move only at operator request; migrate full post-engine/rate/carrier evaluator and calibrated population before labeling oct16.",
        "Figures page": "Move only at operator request; consume rebuilt oct16 companions and decomposition. Historical prototypes remain identified as historical.",
        "Tax-key held-out lane": "Resolve actual ends from MAIN_SPECS, preserve held-out separation, and include basket policy,16/17 and the new effective capital rate. Keep19/W09 beside.",
        "All item producer lanes": "Keep original source cases and bytes. Read delivered builders once; retain standalone oracles and record source conflicts through explicit v9 switches rather than modifying producer lanes.",
    }
    item21_rule = " Item21's health residual, state-price and state/local health-capital parts follow the same line/population/generation routes as item13's health subblock; keep its own key ratios and signs. Use postFor's live capital parts at the selected item20 rate, not the source2%/3% metadata dollars. Coverage/count parts already enter their oct16 kernels once."
    consumer_table = "\n".join(f"| {name} | {rule}{item21_rule} |" for name, rule in consumers.items())
    text = f"""gpt-6.1-sol

**Verdict:** **{state} — candidate, adopted null.** **${band(v['band_bn'])}bn set**, **${band(v['cash_set_bn'])}bn cash**, **${band(v['per_member_usd']['set'])}/member set**, **${band(v['per_member_usd']['cash'])}/member cash**, over **{v['population']['with_coverage']:.6f} people**. Set ends {v['end_specifications']['set']}; cash ends {v['end_specifications']['cash']}. Item19 central is **{v['item19_central']}**; default ITEM19=0 puts19 and W09 beside together under the parent's 2026-10-15 13:20 JST ruling. Change-by-item and interactions are below. [CALCULATION: derived/summary.json v9; derived/{{g1,contract,generality,api_check,coverage_check}}.json]

## The items

This is the modeled annual removal account for other US residents: income-year 2024 tax and benefit rules, with the Social Security and Part A promises at what current law can pay (2026 Trustees), under v8's full-adjustment and budget-response premises. It has no white reference group. It is not an observed historical removal effect. Set and cash differ in pension timing; the public-capital return is an imputed resource cost, never debt. LLM framing remains an instrument limitation. [FRAMING-SENSITIVE; DATA: ../main_case_2026_10_15/RESULT.md; notes/llm-bias-caveat.md]

13. Military-service costs use the premise **equal-cost replacement: the residents who would serve in the group's place, in the same service eras, would earn the same benefits**. In steady state, compensation and delivered service-earned benefits respond at0; the means-tested pension at1. VA medical uses **FY2024 actual net outlays of VA's three direct medical accounts**, $89.742bn, transported one-for-one from FY to CY; it is not an exact NIPA medical mass. In the first year no replacement veterans exist yet, so compensation, readjustment, life insurance, veterans_other, TRICARE and VA medical all retain their evaluated first-year response1. The coverage and count kernels restore their signed pre-item13 prices. Source line/population/generation parts remain inspectable.
14. Income-security administration uses the delivered retirement-only partial key. **[DEGRADED]** The unmeasured remainder retains its original key; no complete program bridge is claimed.
15. Public colleges take the source conditional response0.8857748497320679, with matching college capital. Tuition and Pell stay on their existing rules. Operating use for additions retains the source's capital-key proxy.
16. Native Mexican-origin minors take the source ACS calibration inside/outside CA/TX, preserving CPS Hispanic controls. It changes counts and signed source-key prices; raw audit row4 remains the survey frame.
17. Coverage tenure is fixed-count centrally. The full selected registry is passed to the source builder; when16 is selected,17 is joint-minus16. The count-changing TableD transfer is beside.
18. The household_joint food/SNAP taxable-basket proxy is selected. Business-purchase/customs production-key arms stay beside because their incidence differs from the case's consumption premise. The explicit source-evaluator versus declared-carrier discrepancy is documented below.
19. **Beside, zero central contribution.** ITEM19=0 is the default; ITEM19=1 restores the former conditional selection for inspection. The selected source arm foreign_full_ftc_individual_tangible_normal gives the former −3.368257/−0.673877bn v8 pair. Item19 and W09 are opposite-sign refinements of item6 without an identified central and now go beside together. The naive item6 legal-form pair below reports both parts and their sum; it is not jointly solved. Other item19 source arms remain arms. VA medical care stays inside13 because the adopted response rule fixes its sign and source masses bound it; the business-purchase arm of18 stays beside. [SOURCE: parent ruling, 2026-10-15 13:20 JST]
20. **One rate for the capital return and the Social Security and Part A promises; imported public-employee pension and retiree-health normal costs keep their booked valuations.** Public capital uses the Trustees path's flat equivalent **2.0810698764% real** at both ends; the promises use that same Trustees path. Old specification rate fields remain internal source-price coordinates, and an explicit typed revaluation makes the economic rate common; per_spec.effective_capital_rate exposes it.
21. The non-military health_services residual uses the same MEPS age-band/nativity donor model restricted to TOTOFD24 + TOTSTL24, with pooled winsor_p995 ofd_stl ethnic translation. VA retains item13's old-key subblock. State/local health prices and capital follow the new residual key; separately measured fees keep their dollars. This is an allocation and applies in the first year too. Each source health arm has its own signed coverage/count increments. [DATA: ../spending_keys_r5_2026_10_15/RESULT.md Item21; CALCULATION: package.cjs, coverage source kernel]

[DATA: the five source lanes' RESULT/item modules; CALCULATION: package.cjs, item_rate.cjs, coverage_integration.cjs, derived/corrections*.json]

## Items jointly

Standalone changes use each delivered v8 oracle. Every pair is evaluated; the exact remaining all-order interaction is reported, including the coverage repricing residual. Pair algebra is not a claim that unmeasured household, owner-overlap or calibration counterfactuals are identified. [CALCULATION: main_case.cjs; derived/summary.json v9.interactions]

| $bn/year | Set low | Set high | Cash low | Cash high |
|---|---:|---:|---:|---:|
| v8 | {starts[0]:.6f} | {starts[1]:.6f} | {starts[2]:.6f} | {starts[3]:.6f} |
{chr(10).join(parts)}

The displayed interaction absorbs only final-digit rounding so the printed rows add to the printed total. Exact selected-item standalone and joint deltas, all {len(v['interactions']['pairs'])} central pairs and the residual are in the structured summary. Item19's source-alone oracle is retained under v9.beside rather than central change_by_item. Item16+17 never stacks their standalone deltas. [CALCULATION: derived/summary.json v9.change_by_item/interactions/beside]

The full denominator is {v['population']['with_coverage']:.6f}; without covered people it is {v['population']['without_coverage']:.6f}. The same final numerator over the latter denominator gives ${band(v['per_member_without_coverage_people_usd']['set'])}/member set and ${band(v['per_member_without_coverage_people_usd']['cash'])} cash. Those are alternate denominators, not a coverage-off numerator. [CALCULATION: derived/summary.json v9.population/per_member_without_coverage_people_usd]

## Arms and companion readings

| Companion, $bn/year | Set low / high | Cash low / high |
|---|---:|---:|
{chr(10).join(companion_rows)}

Each companion is separate. Its structured record states whether coverage uses central own-price amounts carried into that reading or source-line repricing for school/first-year responses. Central lineage/ancestry/first-year companions exclude19. V9_PASS_OPTION and V9_FIRST_YEAR_PASS apply only to explicitly selected19 arms. Ancestry share weights item11 by its source generation vector and reports the exposure from dropping only that weighted part. [CALCULATION: companions.cjs, item_passthrough_options.cjs, derived/summary.json v9.companions]

First-year item13 restoration before the calibrated count adjustment is **+{military_screen[0]:.9f} / +{military_screen[1]:.9f}bn**, reproducing the fixed-count screen. Including the signed16/17 count-kernel restoration gives **+{military_net[0]:.9f} / +{military_net[1]:.9f}bn** at the rebuilt ends. Both sets retain the six first-year responses at1; item21's allocation remains and its capital charge is zero in this reading. [CALCULATION: derived/summary.json v9.companions.first_year, companions.cjs; CHECK: derived/api_check.json]

Item18's corrected business_sales_customs source-v8 delta is **+${business_source:.9f}bn**, the same at both ends and in both sets; it uses item6's business-base denominator. Its full v9 beside band and the separately named mining sensitivities are rebuilt in main_case_bands.csv. The superseded whole-line sales diagnostic remains explicitly named as such. These are conditional purchaser proxies, not a central taxable-purchase measurement. [DATA: ../consumption_tax_bases_r5_2026_10_15/derived/evaluation.json; CALCULATION: derived/main_case_bands.csv]

## Item 6 legal-form pair — beside

These are naive pairs, **not jointly solved**. Source19's selected post-engine arm and W09's corporate-only frozen arm, plus its separate source extension, are evaluated over all v9 personal specifications in both methods and both accounting sets; each reading searches its own ends. The part changes below are the same in set and cash. [CALCULATION: legal_form_pair.cjs; derived/summary.json v9.beside.item6_legal_form_pair]

| Reading, $bn/year | Item19 low / high | W09 low / high | Sum low / high | v9 set low / high | v9 cash low / high |
|---|---:|---:|---:|---:|---:|
{chr(10).join(legal_rows)}

W09 frozen carries the producer's +3.295299123/+1.219260676bn union/descendant amount. The extension carries +3.403873020/+1.259433017bn including its delivered item10 G3-profile and item12 generation-profile proxies. These source dollars are transported unchanged onto v9; neither new legal-form keys for16/17 nor own missing-person keys are identified. Central v9 coverage/count prices are carried. Adding opposite-sign arms does not resolve owner overlap, compliance, replacement or legal-form interactions. [DATA: ../passthrough_source_tax_r5_2026_10_15/derived/w09.json; CALCULATION: legal_form_pair.cjs]

## The lineage's addition, by part

lineage_addition.json preserves inherited history and adds the current v9 count/cost decomposition, original descendants, observed nonreporters, calibrated reporting union and coverage. It reports the nonlinear count interaction and zero-count-limit probe. Post-engine source-tax parts on added_G3plus are folded into G3plus for generation tables and isolated for ancestry weighting. [CALCULATION: lineage_addition.cjs, derived/lineage_addition.json; ../generation_account_2026_09_24/v9_split.cjs]

## The payloads and item mechanism

package.cjs builds on unmodified v8 and preserves the exported API and all64 specification numbers. New items are located by meta.items; their semantic source parts remain separate from the inherited lineage ranges. With all new items off the exact v8 API/payloads return. Consumer raw-engine routes must use withSyntheticLines/stateFor and then apply every post term; evaluateFull is the canonical full evaluator. postFor(model,spec,profile) returns new dynamic additions, while postEngine(fullSpec) returns the complete canonical-method post total. Partial {{reading}} alone is insufficient for the dynamic capital/service calculation. [CALCULATION: package.cjs; G3/G4]

meta.population_v9 is the authoritative complete/calibrated denominator. meta.population_v8 and prior v4–v8 blocks remain historical source records. Central corrections contain fixed-end generation parts, source-line parts, method-specific military/administration/college amounts,16/17 count and generation changes and20's actual economic rate. They contain no selected19 record or source-tax post block with ITEM19=0. Selecting19 explicitly creates those beside parts. The engine's per_target_person retains its original survey denominator; whole-case per-member outputs use v9. [CALCULATION: derived/corrections*.json, derived/summary.json]

Item12 is rebuilt on the v9 signed-price kernel before16/17. Its raw source count construction remains fixed;16's revised coverage count and17's conditional tenure correction enter once through their own blocks. New13–15/18/20/21 coverage pieces are absorbed into the repriced coverage block and removed from their standalone post components. The file gates the item12 change against each declared coverage delta and identifies capital-rate interactions separately. Native calibration uses new source prices rather than a flat whole-case count factor. [CALCULATION: coverage_integration.cjs; ../coverage_bound_2026_10_14/coverage_oct16.py and derived/coverage_bound_oct16.json]

meta.coverage.counts_by_generation preserves all four inherited source parts (G1, G2, G3plus, added). counts_by_generation_folded is the explicit three-generation view, adding only added to G3plus; count-transfer consumers use that view. Both views close to the same missing-person total and must never be stacked. [CALCULATION: coverage_integration.cjs, coverage_check.cjs]

## Rates beside the case

FRED's **2024 available-trading-day annual averages** are **1.93712% real for10-year TIPS (DFII10)** and **2.15044% for30-year TIPS (DFII30)**, each250 observations, retrieved2026-10-15. They sit beside the Trustees equivalent2.0810698764%; a maturity-specific market yield is not the same cashflow-weighted perpetuity equivalent. [SOURCE: https://fred.stlouisfed.org/series/DFII10 ; https://fred.stlouisfed.org/series/DFII30 ; DATA: inputs/market_sources.json, inputs/market_DFII*_2024.csv; CALCULATION: derived/market_check.json]

Imported valuation inventory: the federal Financial Report's FY2024 pension nominal rates are **FERS3.0%, CSRS2.5%, military3.0%**; these are beside BEA's booked employer normal costs, whose federal valuations come from OPM/DoD source methods. BEA S&L uses a Moody's-AAA-based rule with no exact staged aggregate parameter (the4.9433% flow/stock diagnostic is not the booked discount rate). Federal civilian/military OPEB nominal rates are **3.2%/3.0%**; state GASB75 mixes funded-plan returns and municipal-bond rates, with no single exact aggregate in the staged inputs. These normal costs cannot be exactly re-discounted from their totals alone. [DATA: ../one_rate_2026_10_15/RESULT.md rate inventory; ../one_rate_2026_10_15/inventory.md]

## Gates and reproduction

G1 source controls, all-item-off exact v8 payload/band/per-spec checks, source-item oracles, endpoint search, parts/edits, national totals and denominator/coverage gates; G2 every inherited file/column/row/key with additions and type changes; G3 unmodified v8 producers on new-items-off; G4 retained and new consumer patterns plus negative probes; G5 full byte replay. Gate records are separate from historical inherited source-input copies. [CALCULATION: derived/{{g1,contract,generality,api_check,coverage_check}}.json]

Run `sh infra/immigration-fiscal/main_case_2026_10_16/run_all.sh`, then `uv run --no-project python3 scripts/rerun_lane.py infra/immigration-fiscal/main_case_2026_10_16 "uv run --no-project python3 {{lane}}/measure_run.py -- sh {{lane}}/run_all.sh"`. Timing uses Python perf_counter/getrusage and Node resourceUsage. The canonical lifetime peak physical-footprint guard enforces 2.5GB per process; maxRSS is diagnostic only. G3 compiles original v8 source bytes in an isolated runtime, bounds the raw pricing memo to two entries and unlinks only the matching evicted capture module by exact unitModels identity. Active model references and scalar memo remain; original files/modules/caches are untouched. Source anchors fail loud if upstream changes. No ps, sysctl, time-l or Git write is required. [CALCULATION: measure_run.py, memory_for_pid.py, v8_bounded_runtime.cjs, derived/generality.json; failure-catalog.md]

## Approximations and assumptions

- All inherited v8 assumptions remain: static removal, source proxies, mixed-unit survivors, descendant age/white-price transport, survey/PES construction and source incidence. This is not a confidence interval or measured causal removal effect.
- Item14 is a partial retirement-administration bridge, not a complete re-key. Item15's operating/capital transport and response are conditional. Source13's VA consumption bridge retains its own classification and uncertainty.
- Source18's exact executed oracle omits declared reporter-carrier edits. The explicit default preserves that oracle on all routes; the alternative adds approximately0.003339489600bn to both ends/sets on v8. Its item11 taxable basket remains held and is not an identified zero interaction.
- Item19 and W09 have no identified central and are excluded together. Source19's missing-person source-tax increment remains withheld in its beside arms because own age/sex/job-source keys are absent. The coverage file supplies a generation-mean size diagnostic, approximately−0.138/−0.028bn, which is neither a central omission nor a bound. The naive pair carries W09's original frozen/extension dollars, including its G3/item12 profile transport; new16/17 legal-form and joint owner/compliance counterfactuals remain unmeasured. Source profits/owner rates, outside-owner status and replacement/FTC assumptions remain conditional.
- Nondefault13/14/15/18 source arms rebuild their direct engine/reporter parts while carrying the central coverage and16/17 price kernel. They are explicitly carried-price diagnostics, not full own-price counterfactual rebuilds: in particular, military unchanged does not undo the military part embedded in central coverage. summary.v9.arm_transports and main_case_bands.v9_price_scope name the scope and source-price exposure. V9_ARM_TRANSPORT=require_own rejects these unsupported own-kernel requests. Item21 arms instead take their separately supplied coverage/count prices; old_key reproduces the complete pre21 case. The measured source-price exposure is not a bound on missing count interactions.
- Item21 is a noisy health-use proxy, not a measured residual-program composition. Its 2024 OFD+STL donor mass is9.601250440bn, with3–84 positive records per age/nativity cell; pooled winsor ratio SEs range0.112879–0.315933. The source Item21 section prints every cell count and ratio SE. IHS incidence is unidentified; donor/transport uncertainty is not propagated into a fiscal confidence interval. The218.616754899bn residual includes OPEB. Federal health structures106.019bn stay on the old key without a compatible VA stock split: gross group stock6.976011838bn, source2%/3% return0.139520237/0.209280355bn, before fee offsets. These exposures are neither a proposed correction nor a debt flow. [DATA: ../spending_keys_r5_2026_10_15/derived/item21_exposures.json, item21_key_cells.csv, item21_ratios.csv]
- Item21 transports its separate original-union, reporter, native-child and G3/white own-age source profiles. Lineage count/C3 options rescale each original added-lineage part by its own mass, holding its age profile; other option-specific donor reconstructions are not measured. In shared-allocation and other inherited range sensitivities, the delivered personal donor-key increment is carried; a fresh household-sharing donor calibration is not claimed. Ancestry share weights the declared added-lineage part separately. DA coverage uses its own source-weight integration; count16/17 prices remain central under DA and lineage options. [CALCULATION: package.cjs, companions.cjs, coverage_integration.cjs]
- Option source13 generation shares are a declared canonical-source transport where its producer is pinned to old generation models; v9's generation evaluator separately routes actual line prices. Source19 lineage options use its delivered wage-key sufficient statistics, preserving observed union/completion. Coupling A/3%-pension arms with noncentral original-descendant lineage options retains the source's original-descendant PV transfer; central16/17/coverage pension parts are repriced. This does not claim a new own-person calibration for every arm combination.
- Some old band rows and old JSON blocks are retained as explicitly enumerated history. Read v9 for current whole-case quantities and v9.historical_rows before quoting a retained row. Existing source lanes remain on their own source cases.

[DATA: source RESULT limitations; CALCULATION: package.cjs, item_passthrough_options.cjs, coverage source file, derived/summary.json]

## Consumers

Each row inherits all v8 R1–R13 rules. For central oct16 add source13 military lines, partial14, college15 operating/capital, joint16/17 generation/count changes, source18 carrier policy and item20 capital revaluation. Item19 and W09 are beside only; consumers must use selected meta.items rather than every registry id. Route19's generation parts only when explicitly selecting its beside arm, and label the legal-form pair naive/not jointly solved. Read population_v9 and found ends; never infer complete costs from engine welfare alone. [CALCULATION: package.cjs; ../main_case_2026_10_15/RESULT.md Consumers]

| Consumer, including every v8 outside entry | Required oct16 change |
|---|---|
{consumer_table}

This is propagation guidance. External consumers, central prose, live_case.json and the decision were not edited; the parent owns adoption and propagation. [SCOPE]

## For the parent

1. Parent ruling2026-10-15 13:20 JST is applied: ITEM19=0 by default,19/W09 beside together. The original brief's item19 numeric pair and named arm contradict the producer. The beside numeric-intent arm remains foreign_full_ftc_individual_tangible_normal. Set ITEM19_ARM=foreign_full_ftc_immediate_individual for the literal-name arm (both ends−3.368bn on v8); ITEM19=1 restores conditional central inclusion for inspection. No producer value was re-derived.
2. The item18 producer's evaluator/payload disagree on reporter edits. Recommended/default source_evaluator policy preserves its published/executed0.263315bn oracle consistently. ITEM18_CARRIER_MODE=declared_carriers applies its declared reporter edits, approximately+0.00333949bn more on v8. Repair/adopt the source lane first if changing the canonical oracle; do not mistake a source compatibility choice for a measured zero.
3. The appended L1 handoff supersedes step2 readiness with standalone L1 STEP3DONE. Read the source receipt; quoted instructions are not completion. The final candidate must be non-STUB and pin the final source.
4. Only explicitly selected item19 beside queries use V9_FIRST_YEAR_PASS's item6 labor-share transport; central first-year has no19 term. The held branch exposes the unmeasured first-year source-tax adjustment. V9_PASS_OPTION applies only to selected19 lineage arms; it defaults to reprice source sufficient wage-key components; held preserves canonical latent-tax dollars and reports the exposure.
5. The earlier full upstream generation-source rebuild was blocked by the peer world-ledger source pin. This step2 directly replays the unchanged oct15 set/cash generators and the new oct16 generators: IDENTICAL135/135, exit0; it does not rerun the upstream acquisition/source pipeline. Retain that scope distinction and reconcile peer custody before a full upstream regeneration; do not edit a hash to make it pass.
6. STATUS stays candidate/adopted null. The parent writes decisions/2026-10-16-main-case-v9.md and updates live_case only on adoption. No git metadata was changed.
7. Nondefault13/14/15/18 full-registry arm queries carry the central coverage/count kernel. Recommended bounded branch is explicitly labeled carry; V9_ARM_TRANSPORT=require_own blocks unsupported own-price requests. A full alternate kernel needs baseline price atoms and its own16/17 typed-part tables; no complete reprice is claimed merely because the direct source arm runs. The military unchanged arm is a direct-source diagnostic, not whole-case item13 off.

## Log

{(HERE / 'execution-log.md').read_text()}
"""
    require_within_budget("v9 result renderer")
    (HERE / "RESULT.md").write_text(text)
    print(json.dumps({"result": str(HERE / "RESULT.md"), "gate_state": state, "consumers": len(consumers), "market_input_keys": list(market)}))


if __name__ == "__main__":
    main()
