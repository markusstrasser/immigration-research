"""Render deterministic source-linked results from measured item artifacts.

Native-First: plain Markdown and CSV/JSON inputs, no reporting dependency.
"""
import json
from pathlib import Path

import pandas as pd

HERE = Path(__file__).resolve().parent
OUT = HERE / "derived"


def main():
    data = json.loads((OUT / "items.json").read_text())
    diagnostics = json.loads((OUT / "origin_diagnostic.json").read_text())
    evaluation = json.loads((OUT / "evaluation.json").read_text())
    if not evaluation["v8_unchanged_gate"] or not evaluation["post_engine_item_closure_1e_9"]:
        raise ValueError("[BLOCKED] case evaluation gates failed")
    lines = [
        "**Verdict:** Items 16 and 17 measured as a conditional survey-weight calibration and tenure price transfer. Their joint accrual change is small because the two items largely offset. These are candidate items for the parent's adoption decision, not an adopted v9 case.",
        "", "[CALCULATION: derived/items.json, derived/effects.csv, derived/evaluation.json] All changes below are annual income-year-2024 $bn of net cost to other residents, against unchanged v8; positive raises cost. Set means the case's accrual set; cash uses its own cash-set prices. Per-member changes divide by the unchanged 45,230,062.30075857-member v8 lineage, as requested. Missing counts, repricing and transfers are modeled, not observed omitted people or causal estimates.",
        "", "| Item / arm | Set low | Set high | Cash low | Cash high | Set $/member low / high | Cash $/member low / high |",
        "|---|---:|---:|---:|---:|---:|---:|",
    ]
    labels = {"item16": "16: native-child survey calibration", "item17": "17: tenure, fixed counts",
              "joint": "16 + 17, joint", "item17_count_transfer": "17: count-changing Table D transfer",
              "joint_count_transfer": "Joint count-changing transfer"}
    for scenario, label in labels.items():
        s, c = (data["sets"][b][scenario]["by_end"] for b in ("set", "cash"))
        lines.append(f"| {label} | {s['low']['total_bn']:+.9f} | {s['high']['total_bn']:+.9f} | {c['low']['total_bn']:+.9f} | {c['high']['total_bn']:+.9f} | {s['low']['per_v8_member_usd']:+.2f} / {s['high']['per_v8_member_usd']:+.2f} | {c['low']['per_v8_member_usd']:+.2f} / {c['high']['per_v8_member_usd']:+.2f} |")
    lines += ["", "## Counts and construction", "",
        "[DATA: derived/native_cells.csv; derived/native_audit.json] Native citizenship codes 1–3, ages 0–17. CPS March 2025 is compared with ACS 2024 annual PUMS: the time reference differs. Central ACS excludes institutions and active military, retaining noninstitutional group quarters. Outside CA/TX, Mexican CPS 5,308,839.165 versus ACS 4,921,871 (difference 386,968.165; independent-survey z=2.677). Hispanic totals there give z=0.401. National Hispanic CPS 17,892,629.696 versus ACS 18,004,712 gives z=-0.992891. The offsetting other-Hispanic difference supports a composition explanation, without identifying misclassification as its cause.",
        "", "[FRAMING-SENSITIVE] Parent policy: preserve CPS Hispanic control totals when national absolute independent-survey z≤1.96; when ACS is significantly lower use that lower total. The test selects preservation here. Eight age×region cells use 0–4, 5–9, 10–14, 15–17 × CA/TX versus outside. Mexican stratum weight = ACS Mexican/CPS Mexican; other-Hispanic weight = (preserved CPS Hispanic minus ACS Mexican)/CPS other Hispanic. Both are applied to existing lineage members. This reassigns survey weight between origin strata, keeps person identities/generation masks/household rosters fixed, and creates no entrant identities. ACS cannot identify full G2/G3+ ancestry; the conditional CPS generation mix remains.",
        "", "[DATA: derived/native_states.csv; derived/native_calibration_replicates.json] State and age×state comparisons are supplied. Thirty-two all-age Mexican state cells meet both surveys' n≥30 and CV≤30% descriptive screen; sparse states are not separately raked. CPS counts use 160 SDR replicates (4/160); ACS uses 80 (4/80). Independent-survey difference SEs omit covariance and nonsampling errors. All 161 CPS calibration columns close to the fixed central ACS targets; the fiscal central values do not claim a combined monetary confidence interval.",
        "", "[DATA: derived/native_verifier_universe.csv; derived/native_household_cells.csv] Retaining ACS active military reproduces the verifier's 4,922,143 outside CA/TX and 6,290,238 inside. The central differences are 272 and 26 active-duty minors. The separate household-only all-G2 price screen reproduces the verifier; it is not the keyed correction:",
        "", "| Fixed G2 price screen, outside CA/TX | Low change | High change |", "|---|---:|---:|"]
    for basis in ("set", "cash"):
        values = diagnostics["fixed_G2_price_screen_bn"][basis]
        lines.append(f"| {basis} | {values['low']:+.9f} | {values['high']:+.9f} |")
    native = data["sets"]["set"]["item16"]
    lines += ["", f"[CALCULATION: derived/items.json] The observed lineage count changes by {sum(native['observed_people_change_by_generation'].values()):+,.6f}; covered people change by {sum(native['coverage_people_change_by_generation'].values()):+,.6f}; together {native['population_change']:+,.6f}. The synthetic 3.04M descendant stock stays fixed. The revised denominator is {data['population_v8']+native['population_change']:,.6f}, but the per-member changes above retain v8's denominator.",
        "", "[SOURCE: ../coverage_bound_2026_10_14/inputs/pes_cross.pdf, Table D; ../coverage_bound_2026_10_14/source_tables.py and controls] Item17's central fixed-count arm uses owner -2.18%, renter -7.83%, all Hispanic -4.99% as a conditional tenure contrast: net-omission odds 1/(1+NCE)-1. The tenure contrast tilts the existing PES part, then normalizes within exact current age×sex×generation cells. The demographic-analysis-under-five part, birth-date mixture, arrival rule, and every signed count cell remain fixed. No-cash-rent occupants are treated as nonowners/renters. This normalized transfer does not assert independence of marginal PES errors. The count-changing sensitivity instead applies the actual Table D tenure×2020-age×sex cells, retaining V2024 control absorption and DA under five. It is a sensitivity, not an identified correction.",
        "", "## Pricing and interactions", "",
        "[CALCULATION: measure.py; derived/line_parts_set.csv and line_parts_cash.csv] The fiscal change integrates actual person key vectors through the frozen final-routing signed line prices: schools, benefits, receipts, SPM/owner/tenant keys, state-price pieces, capital and production profiles. Every line closes to net profile integration at 1e-9bn. The rows retain generation, source line/side, category and economic class; this is not fixed per-head child pricing. National budgets/key masses, response parameters, key coefficients and production attribution stay fixed. Complete administrative justice use is retained for observed people and excluded for constructed omitted people, exactly as v8 declares.",
        "", "- **Item9:** domestic corporate-source correction and receipt responses are already in each accounting set's price kernel; held fixed.",
        "- **Item10:** actual completion identities are joined by PH_SEQ/PPPOS. Reporter and observed nonreporter weights follow their own child/origin factors, not their parents' factors. The former use identified prices, the latter added-population prices. Synthetic descendants' weights stay fixed. Source school/credit/benefit carriers and G2/G3+ ownership stay active.",
        "- **Item11:** central retains the case's declared generation-total-per-member distribution (`households.py:1143–1151`) for that post-engine component. Its assigned contribution moves with the observed weights and omitted-person composition. This is not a fresh nonlinear survivor-tax/benefit solution. Reassigning actual child identities would need a joint household assignment rule and registry/kernel reruns; the marginal ACS rake does not identify that rule. Net component totals cannot bound that counterfactual.",
        "- **Item12:** item16 recounts the adopted omission base once, using the revised child weights. Item17 then reweights tenure on that revised base. Central tenure preserves its count cells. Actual completion nonreporters remain outside v8's adopted omission base, even where PRDTHSP is another Hispanic origin; that issue is reported separately below. No generic count factor is also applied to the coverage amount.",
        "- **16×17:** `joint` is computed afresh; standalone effects must not simply be added. `items.cjs` exports two post-engine builders. Parent must pass the complete selected registry IDs as `ctx.selectedItems`; missing selection fails. Item17 after item16 supplies `joint minus item16`, including generation parts and count changes. The CSV selectors are in each item's metadata. Parent must add these two declared amounts to its full evaluator; the v8 evaluator adds only its original post-engine items. Population changes likewise require the parent's v9 denominator update.",
        "", "[DATA: derived/items.json metadata] The original union gates at 39,712,493.331188. Final-routing coverage is +0.016270768/+0.016390852bn above the preserved adopted coverage in both sets; this previously accepted routing gap is held fixed and not bundled into either new item. Unchanged v8 is evaluated through its original engine/package and reproduces 365.791930255/455.981784589bn set and 281.752563676/371.942418010bn cash. Existing item9–12 settings are fixed, so a simultaneous new item changing their coefficients/responses needs a price-kernel interaction check; these endpoint amounts are not a claim of all-order nonlinear invariance.",
        "", "## WC14 text correction, no item", "",
        "[DATA: derived/linked_origin_age_sex.csv and linked_origin_replicates.json] Non-Mexican does not imply non-Hispanic. PRDTHSP is tabulated by linked generation G2/G3/G4+ × age band × sex, with every observed origin code and all-parent/biological-only arms. Among all-parent linked G3 children, 88.811077% report Mexican origin and 93.739813% report any Hispanic origin; 44.050139% of non-Mexican reporters remain Hispanic. These are observed linked children; latent adults' Hispanic identity is unobserved.",
        "", "[CALCULATION: derived/origin_diagnostic.json] The verifier's +0.40/+0.51bn set screen uses a generic +5% rate and child origin fractions transported to all descendant ages. The own-age/sex minor-only construction below uses the central birthday/DA/PES rule and current blended latent prices. It is beside the items and is not adopted:",
        "", "| Origin coverage construction | Set low / high | Cash low / high |", "|---|---:|---:|"]
    for name in ("all_parent_types_minor_only", "biological_minor_only", "observed_completion_nonreporter_hispanic", "all_parent_types_child_to_adult_transport"):
        s, c = [diagnostics["sets"][b][name]["coverage_increment_bn"] for b in ("set", "cash")]
        lines.append(f"| {name} | {s['low']:+.9f} / {s['high']:+.9f} | {c['low']:+.9f} / {c['high']:+.9f} |")
    lines += ["", "The last row explicitly transports same-sex child fractions to adults [UNVERIFIED]; it stays outside central values. The observed-completion row also stays beside because fixing the coverage lane's categorical premise was requested as a text correction without an item. Neither row is silently stacked onto items16/17. Adult coverage can lower cash cost under existing age prices; a positive generic 5% screen is not a bound. No take-up, legal-status or benefit-eligibility multiplier is introduced. Table D's tenure effect works only through observed case price cells.",
        "", "## Reproduction, evidence and limits", "",
        "`OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/count_composition_r5_2026_10_15/run_all.py` runs native measurement, line integration, diagnostics and original-v8 evaluation. Run lane pytest, then `scripts/rerun_lane.py` with that replay, explicit test paths and `write_result.py`. Outputs use LF. Source receipts are `derived/native_audit.json` and `derived/sources.json`; upstream caches are hash-validated against their principal manifests. No new data download, upstream output edit, Git staging, merge or commit occurs.",
        "", "Log anchor from `date -u`: 2026-10-15T02:31:32Z (measurement inspection); replay phase timestamps, Python perf_counter timings and child peak RSS are in ignored `_cache/replay.log`, with measure receipts in `_cache/run.log`. The process limit is 2.5GB; every replay child fails on excess. The source filters ACS before loading replicate weights. Known repaired failures and regression checks are in `failure-catalog.md`.",
        "", "This is LLM-assisted analysis on a politically sensitive subject. Model judgment does not establish truth. Counts/ratios are checked against stored primary survey inputs; the calibration target, control-agreement threshold, fixed household roster, tenure transfer, latent profiles and pricing response remain explicit modeling choices. Timing differences, nonsampling error, sparse links and unobserved omitted-person selection limit interpretation. No claim that these amounts are observed fiscal costs or confidence bounds.",
    ]
    (HERE / "RESULT.md").write_text("\n".join(lines)+"\n")


if __name__ == "__main__":
    main()
