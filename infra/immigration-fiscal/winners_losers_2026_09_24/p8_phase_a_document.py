"""Render the scratch Phase-A comparisons, requiring successful premise gates.

Native-First: render existing CSV/JSON receipts with pandas; do not re-price.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import pandas as pd


FIXES = [
    (1,"R2E04/05/21/37; W1","Pool before/after resource levels both ways; report presence effect","p7_frames.py, p8_incidence.py","mixed_before/after_levels_conserved; mixed_bidirectional_boundary", "recommended", "mixed_unit"),
    (2,"R2E07/09/33; W2","Separate jurisdiction keys; CPS railroad/veteran/military receipt mappings","p7_inputs.cjs, p8_incidence.py","programme_authority/exclusion", "recommended", "pooled"),
    (3,"R2E10/19/26","Trust accrual on covered earnings; current cash stays current, future-born payers included","p7_cohorts.py, p8_incidence.py","trust_accrual_covered_earnings_only; cohort projection tests", "recommended", "pooled"),
    (4,"R2E13/35; M1","Air age-mortality recipients; FARS victim ages/roles, fatal mix proxies injuries","p8_recipient_keys.py, p8_incidence.py","air_old_recipient_death_share; fatal-victim conservation", "recommended", "pooled"),
    (5,"R2E16/17/24/34; M4","Propagate every social producer's low/central/high coherent vector","p8_incidence.py, p8_phase_a.py","social_producer_range; complete producer declarations", "recommended", "pooled"),
    (6,"R2E01","Coverage comparator retains original five hybrid bounds and mobility","p8_incidence.py","matched coverage comparator; frozen control", "coverage", "pooled"),
    (7,"R2E20","Rental stock enters capitalization; rent income including losses proxies landlords","p8_recipient_keys.py","rental capitalization only landlords; state stock preservation", "stack", "pooled"),
    (8,"R2E27; M3","Retain v7 item5b; replacement-only guard prepared, item11 mapping held for Phase B","p8_incidence.py","credits_v7_legacy_only; replacement guard tests", "recommended", "pooled"),
    (9,"R2E28/36/39","Finite epsilon only in hs_or_less; descendant multipliers recomputed for each epsilon","p7_nest.py, inputs/p8_epsilon_sources.json","above_hs_perfect_substitutes; descendant_parts_close", "recommended", "pooled"),
    (10,"R2E29/40/48/49; M2","State-age thinning; responded spending geography, signed corrections and state landlord mask","p8_recipient_keys.py, p8_incidence.py, p7_inputs.cjs","state_local_geography; end_pairing; prison producer; landlord states", "stack", "pooled"),
    (11,"R2E03/32/42/43","Report state and landlord results by arm; explicit frame selection; vintage stated","p8_phase_a_document.py; RESULT.md","explicit frame failure; tagged cut tables", "recommended", "pooled"),
    (12,"R2E15/44–47; M6","Premise gates; unique occurrences; missing manifest blocks; persistent degraded notices","p7_frames.py, winners_losers.py, p8_phase_a.py","resource rate; pins; repeated gates; fallback regression", "recommended", "pooled"),
]


def table(frame, columns, decimals=4):
    rows=["| " + " | ".join(columns) + " |", "|" + "---|"*len(columns)]
    for row in frame[columns].itertuples(index=False,name=None):
        rows.append("| " + " | ".join(f"{x:.{decimals}f}" if isinstance(x,float) else str(x) for x in row) + " |")
    return "\n".join(rows)


def main(out):
    gates=json.loads((out/"phase_a_gates.json").read_text())
    if not gates or not all(v["passed"] for v in gates.values()):
        raise SystemExit("[BLOCKED] no successful Phase-A gate receipt")
    shares=pd.read_csv(out/"phase_a_shares.csv")
    channels=pd.read_csv(out/"phase_a_channels.csv")
    cuts=pd.read_csv(out/"phase_a_cuts.csv")
    mixed=pd.read_csv(out/"phase_a_mixed_levels.csv")
    extrema=pd.read_csv(out/"phase_a_grid_extrema.csv")
    audit=json.loads((out/"phase_a_audit.json").read_text())
    timing=json.loads((out/"phase_a_timing.json").read_text())
    joint_notes=next(s["notes"] for s in audit["scenarios"] if s["fix"]=="joint")
    unmapped={r["programme"] for r in joint_notes.get("unmapped_programmes",[])}
    programmes=json.loads((Path(__file__).resolve().parent/"inputs/p8_programmes_oct14.json").read_text())["programmes"]
    remaining=pd.DataFrame([dict(level=end,programme=row["id"],
        federal_responding_budget_bn=row["national_bn"]*row["response"]*row["jurisdiction"]["federal"],
        state_responding_budget_bn=row["national_bn"]*row["response"]*row["jurisdiction"]["state_local"])
        for end,rows in programmes.items() for row in rows if row["id"] in unmapped and row["national_bn"]>0])
    remaining.to_csv(out/"phase_a_unmapped_programmes.csv",index=False,lineterminator="\n",float_format="%.15g")
    text=["## Phase A: twelve isolated fixes and their joint v7 effect",
          "All amounts are modelled presence effects on other residents (negative = cost); ahead means a positive presence effect. Stationary financing is the verdict; cohort30/cohort10 are beside. The government case stays frozen. All low/central/high comparisons, financing rules a/b/c, frames, sharing rules and channel totals are in the scratch CSVs. [CALCULATION: p8_phase_a.py → phase_a_shares.csv, phase_a_channels.csv]",
          f"The mixed-unit arm pools every person's cash income less their own income taxes/FICA plus a per-person SPM noncash allocation, on an equal per-person scale. After removal only the remaining residents pool their own resources, less the existing signed presence effects. This arm counts a non-member's support of member children in the same unit as a cost of the members' presence. That is why it stays beside the central. Neither sharing rule models re-partnering. Removal-level changes appear only as labelled diagnostics in {out.name}_run.log. [ASSUMPTION; CALCULATION: p7_frames.mixed_resource_change; fixture −67.5]",
          ]
    fix_table = ["| fix | finding IDs | change | files | premise/check | selected measurement |", "|---|---|---|---|---|---|"]
    for number,ids,change,files,checks,arm,sharing in FIXES:
        fix_table.append(f"| {number} | {ids} | {change} | {files} | {checks} | {arm}, {sharing}; tables below |")
    text.append("\n".join(fix_table))
    selected=[]
    for number,_,_,_,_,arm,sharing in FIXES:
        epsilons=["eps8.7","eps17.9"] if number==9 else ["infinite"]
        for epsilon in epsilons:
            s=shares[shares.fix.eq(f"fix_{number}") & shares.arm.eq(arm) & shares.sharing.eq(sharing) & shares.epsilon.eq(epsilon)]
            selected.append(s)
    selected.append(shares[shares.fix.isin(["baseline","joint"]) & shares.arm.eq("recommended") & shares.sharing.eq("pooled") & shares.epsilon.eq("infinite")])
    selected=pd.concat(selected,ignore_index=True)
    rows=[]
    for key,group in selected.groupby(["fix","arm","sharing","epsilon","frame","level"],sort=False):
        row=dict(zip(["fix","arm","sharing","epsilon","frame","level"],key))
        for r in group.itertuples():
            row[f"ahead_{r.financing}_pct"]=100*r.winners_share
            row[f"delta_{r.financing}_pp"]=r.delta_ahead_pp
            row[f"net_{r.financing}_bn"]=r.total_bn
            row[f"delta_net_{r.financing}_bn"]=r.delta_total_bn
        rows.append(row)
    compact=pd.DataFrame(rows)
    compact.to_csv(out/"phase_a_fix_comparisons.csv",index=False,lineterminator="\n",float_format="%.15g")
    text += ["### Shares ahead and isolated changes", "Each selected arm is matched to the same frozen baseline arm, level, frame, sharing and epsilon. Fix 1 changes mixed sharing, fix 6 coverage, fix 7 capitalization in stack, fix 9 epsilon arms, fix 10 combined geography in stack. Fix 8 has no v7 numerical change; fix 11 is reporting; fix 12 validates premises. Low/high vectors for fix 5 include social uncertainty. [CALCULATION: phase_a_fix_comparisons.csv]",
             table(compact,["fix","arm","sharing","epsilon","frame","level","ahead_a_pct","ahead_b_pct","ahead_c_pct","delta_a_pp","delta_b_pp","delta_c_pp"]),
             "### Other residents' net and each channel",
             table(compact,["fix","epsilon","frame","level","net_a_bn","net_b_bn","net_c_bn","delta_net_a_bn","delta_net_b_bn","delta_net_c_bn"]),
             "`phase_a_channels.csv` reports each channel's signed total, baseline and isolated/joint delta for every financing/frame/end/arm/epsilon. Its `mixed_boundary` row is beside the direct channels; add it only for mixed sharing. `future_cohorts` belongs beside living residents, never in their prevalence denominator. [CALCULATION: phase_a_channels.csv]"]
    channel_selections=[]
    for number,_,_,_,_,arm,_ in FIXES:
        epsilons=["eps8.7","eps17.9"] if number==9 else ["infinite"]
        channel_selections.append(channels[channels.fix.eq(f"fix_{number}") & channels.arm.eq(arm) & channels.epsilon.isin(epsilons)])
    channel_selections.append(channels[channels.fix.eq("joint") & channels.arm.eq("recommended") & channels.epsilon.eq("infinite")])
    pd.concat(channel_selections,ignore_index=True).to_csv(out/"phase_a_fix_channels.csv",index=False,lineterminator="\n",float_format="%.15g")
    text += ["The complete selected per-fix channel ledger is `phase_a_fix_channels.csv`; it includes all a/b/c rules and all three frames and levels. [DATA: phase_a_fix_channels.csv]",
             "### Joint comparison across sharing and geographic arms",
             table(shares[shares.fix.eq("joint") & shares.level.eq("central") & shares.epsilon.eq("infinite") & shares.arm.isin(["recommended","stack"])], ["financing","frame","arm","sharing","total_bn","winners_share","delta_ahead_pp"]),
             "### Social-vector share extrema",
             table(extrema[extrema.extreme.isin(["share_min","share_max"]) & extrema.sharing.eq("pooled")], ["fix","financing","frame","extreme","arm","level","social_setting","winners_share","total_bn"]),
             "These extrema are over the enumerated coherent producer low/central/high vectors, fiscal ends and recommended/stack arms. They are not bounds over every independent combination of social parameters or causal uncertainty. [MODEL / FRAMING-SENSITIVE; DATA: phase_a_social_grid.csv]",
             "### Mixed boundary and state/landlord reporting",
             table(mixed[mixed.fix.isin(["fix_1","joint"]) & mixed.financing.eq("a") & mixed.frame.eq("stationary") & mixed.arm.eq("recommended") & mixed.epsilon.eq("infinite")], ["fix","level","forward_member_to_other_bn","reverse_other_to_member_bn","presence_boundary_change_bn","presence_net_bn"]),
             table(cuts[cuts.fix.eq("joint") & cuts.level.eq("central") & cuts.epsilon.eq("infinite") & cuts.arm.isin(["recommended","stack"]) & cuts.sharing.eq("pooled")], ["financing","frame","arm","cut","group","mean_usd","winners_share"]),
             "State and landlord statements must name the arm, rule and frame. Shares ahead and mean losses are different statistics; no unconditional landlord-benefit claim follows from these tables. Publication consumers must explicitly select financing, frame, arm, sharing, case and vintage. Phase B migrates the publication readers to oct15. [FRAMING-SENSITIVE]",
             "### Sources, checks and remaining scope",
             f"{len(gates)} distinct scenario/check gates pass, including the 108-row frozen-v7 positive control. Final source hashes are recorded in phase_a_audit.json. Profile wall time {timing['seconds']:.3f}s; lifetime peak physical footprint {timing['physical_footprint_bytes']/1e9:.3f}GB. resource.getrusage RSS is descriptive only. [CALCULATION: phase_a_gates.json; phase_a_timing.json]",
             f"The frozen case's current cash trust surplus is {audit['trust_cash_surplus_bn']:.6f}bn, not the review's provisional 25–30bn lead: payroll 144.713984bn less cash OASDI/Part A benefits 77.275431bn. Accrual is 75.126444bn; it is routed separately. [DATA: derived/oct14/p7_trust_inputs.json]",
             "[DEGRADED] State-local financing uses responded spending geography for the net charge; receipt geography is not independently identified. School repricing uses the preferred signed spatial proxy at all ends; end-specific district and BEA education-mixture state components require a producer export. FARS fatal-victim age/role mix proxies nonfatal injury dollars; CPS has no victim role. Air uses source national mortality-age margins within states under the existing dispersion assumption. Finite epsilon transports different source populations; the case's first-order descendant P/F increment is held fixed but its multipliers are recomputed at each epsilon. None is an observed removal experiment. [ASSUMPTION; phase_a_audit.json; phase_a_epsilon_inputs.json]",
             "The finite source check pins Caiumi–Peri's 0.115 no-diploma inverse elasticity (Table 7), while their own HS-or-less simulation uses 0.045; 8.7 is therefore an explicit transport to the broader cell. Piyapromdee's low-skill nativity elasticity is 17.870 (Table 1), from metropolitan, gender-specific nests; 17.9 pools those distinctions in this sensitivity. Infinite remains central. Primary PDF hashes match inputs/p8_epsilon_sources.json. [SOURCE: doi:10.3386/w32389; doi:10.1093/restud/rdaa029]",
             "Rule c's unmapped programmes and every allocation fallback remain in each scenario's notes. No pin manifest is auto-created by pricing. Missing recipient or authoritative jurisdiction/state-price fields stop the run. [DATA: phase_a_audit.json; tests]",
             "Railroad retirement maps to PEN_SC=7 / SUR_SC=5 / DIS_SC=6 amounts; Black Lung maps to DIS_SC=8, and state temporary disability to DIS_SC=9. Other disability sources do not enter those keys. Veterans readjustment and other veterans programmes map to VET_TYP4/VET_TYP5; military medical maps to MIL/CHAMPVA enrollment. Remaining universal recipient proxies follow below. These are responding national budget weights, not case costs or misallocated dollar estimates. Zero-national synthetic corrections have zero recipient-key weight and are absent from this list. [DATA: CPS ASEC 2025 ddl25.txt; p8_incidence.programme_keys; phase_a_unmapped_programmes.csv]",
             table(remaining,["level","programme","federal_responding_budget_bn","state_responding_budget_bn"]),
             "The LLM implementation has systematic dispositions on immigration. Deterministic source controls and matched signed comparisons support these modelled allocation results; they do not identify causal incidence. [SOURCE: notes/llm-bias-caveat.md]",
             "Would change it: end-specific producer state school/education-mixture vectors, observed re-partnering or victim-incidence evidence, or a validated source-appropriate finite-elasticity descendant solve would replace the stated proxies. No observed removal effect is inferred from accounting closure. [INFERENCE]",
             "Model self-report: Codex based on GPT-6; exact root served model ID is not exposed in this session. Final code reviewer was explicitly selected as gpt-6-astra at low effort; its claims were checked against source and the regression. [MODEL SELF-REPORT]",
             "Phase B is held by the brief: item11 incidence, coverage members outside the payer pool, live social vintage, oct15 compressed tables/readers and IDENTICAL rerun await parent resumption. Tracked oct14 derived outputs remain unchanged."]
    (out/"phase_a_report.md").write_text("\n\n".join(text)+"\n")
    print(f"[Phase A document] {out/'phase_a_report.md'}")


if __name__ == "__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("--out-dir",type=Path,required=True)
    main(parser.parse_args().out_dir.resolve())
