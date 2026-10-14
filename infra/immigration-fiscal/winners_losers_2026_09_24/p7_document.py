"""Generate the current P7 result from executed tables, retaining dated history.

Native-First: pandas table selection and Git's immutable source record; no prose
number is recomputed by hand. Never writes the research memo owned by the parent.
"""
import json
import subprocess
from pathlib import Path

import pandas as pd

HERE=Path(__file__).resolve().parent
OUT=HERE/"derived/oct14"
ROOT=HERE.parents[2]


def markdown(table):
    columns=list(table.columns)
    lines=["| "+" | ".join(columns)+" |","|"+"|".join("---" for _ in columns)+"|"]
    for row in table.itertuples(index=False,name=None):
        lines.append("| "+" | ".join(str(x).replace("|"," / ") for x in row)+" |")
    return "\n".join(lines)


def main():
    shares=pd.read_csv(OUT/"p7_net_shares.csv")
    cuts=pd.read_csv(OUT/"p7_cuts.csv")
    gates=json.loads((OUT/"p7_gates.json").read_text())
    inputs=json.loads((OUT/"p7_inputs.json").read_text())
    control=pd.read_csv(OUT/"p7_positive_control.csv").set_index(["financing","sharing"])
    timings=json.loads((HERE/"inputs/run_receipts.json").read_text())
    if not all(g["passed"] for g in gates.values()):
        raise SystemExit("[BLOCKED] P7 document requires every computation gate")
    central=shares[shares.level.eq("central")]
    rec=central[central.arm.eq("recommended") & central.sharing.eq("pooled")].set_index("financing")
    verdict=(f"On the complete adopted social channel set, stationary financing and the corrected lineage payer pool, "
             f"{100*rec.loc['a','winners_share']:.2f}% / {100*rec.loc['b','winners_share']:.2f}% of other residents are ahead "
             f"under tax shares / per-person cuts, pooled. Their annual net is ${rec.loc['a','total_bn']:.3f}bn. "
             "A minority ahead survives; the former one-in-five count depends on inconsistent financing and incomplete channels. "
             "[MODEL / FRAMING-SENSITIVE; CALCULATION: derived/oct14/p7_net_shares.csv]")
    parts=["**Verdict:** "+verdict,"",
           "# P7 fixes on the frozen adopted v7 account (2026-10-14)","",
           f"The frozen hybrid reproduces **{100*control.loc[('a','spm_unit_pooled'),'winners_share']:.8f}% / "
           f"{100*control.loc[('b','spm_unit_pooled'),'winners_share']:.8f}%** pooled and "
           f"**${control.loc[('a','spm_unit_pooled'),'total_bn']:.7f}bn** "
           "to today's residents. It remains a labelled calculation record in the original `net_shares.csv`; "
           "the new `p7_*` tables carry explicit financing, sharing, population and channel-set tags. "
           "[DATA: p7_positive_control.csv; source oracle at 2204a2bc]",
           "The account and its personal specifications 16/11 are held fixed. `identified_union` and `lineage` name "
           "the **payer-pool** alternatives for the same live 42.75M fiscal case, not separately recomputed fiscal "
           "headlines. The complete social amounts are separately tabulated for the identified 39.71M union and the "
           "42.75M lineage. No frozen main-case file changed. Adding the direct credit to non-member filers changes "
           "their resource net while the government's adopted account stays fixed. [ASSUMPTION / DATA: p7_inputs.json]",
           "The social vintage is the adopted-v7 propagation at **c392d356**, copied verbatim to "
           "`inputs/social_oct14.json`, pinned by SHA-256. A concurrent unadopted peer refresh changed the working "
           "upstream JSON during a preliminary run; it is excluded. Every source pin is checked and within-run "
           "drift fails closed. [SOURCE: Git c392d356; DATA: inputs/pins.json]",
           "## One fix at a time", "",
           "Each dollar delta below compares to the live central hybrid at the **same end, rule and sharing**; "
           "the frozen government-account file stays unchanged. Pure financing reassignment has zero "
           "all-cohort resource delta, reported separately from its present-resident delta. Changes to the stated "
           "distributional claims are material independently. [CALCULATION: p7_net_shares.csv]", ""]
    arms=["financing_only","social_coverage_only","payer_pool_only","crossing_credit_only","state_wages_only",
          "capitalization_only","owner_type_only","owner_type_broad_only"]
    one=shares[shares.arm.isin(arms)&shares.financing.isin(["a","b"])&shares.sharing.eq("pooled")&shares.level.isin(["low","high"])]
    one=one[~(one.arm.eq("financing_only")&one.frame.eq("hybrid"))]
    display=one[["arm","frame","population","financing","level","total_bn","winners_share","winners_share_conditional_se","delta_today_bn","delta_ahead_pp"]].copy()
    for field in ["total_bn","delta_today_bn","delta_ahead_pp"]:
        display[field]=display[field].map(lambda x:f"{x:.3f}")
    display["winners_share"]=display.winners_share.map(lambda x:f"{100*x:.3f}%")
    display["winners_share_conditional_se"]=display.winners_share_conditional_se.map(lambda x:f"{100*x:.3f}pp")
    parts.extend([markdown(display),"",
      "The added-descendant-only incidence arm removes precisely the payload's added count from US-born "
      "nonmembers whose two parents were born in US areas, proportionally within five-year age bands. "
      "Removed weights enter the surrogate member pool at the case's G3+ age records: no weight is discarded. "
      "The within-cell state, income and family assignment is unidentified. [ASSUMPTION; DATA: p7_payer_cells.csv]",
      "Crossing credits go to the measured non-member tax-return carriers. The union's gross forward A+C "
      f"is ${inputs['credits']['forward']['total_bn']:.6f}bn (joint SDR SE ${inputs['credits']['forward']['se_bn']:.6f}bn); "
      f"reverse B+Cr is ${inputs['credits']['reverse']['total_bn']:.6f}bn. The additional forward "
      f"${inputs['added_descendant_forward_credit']['total_bn']:.6f}bn uses item 5b's own G3+ per-member "
      "extrapolation, applied to the recovered G3+ gross forward vector; white-priced added people take zero. "
      "That additional filer location is an assumption, not observed microdata. "
      "[CALCULATION: p7_credits.py, p7_inputs.json; SOURCE: mixed_unit_credits/credits.py]",
      "The identified union's direct filer gain is just below the review's $5bn bar; including the case's "
      "added-person extrapolation puts the full-lineage gain above it at both ends. This improves the "
      "combined other-resident resource account, not the government's unchanged net budget charge. "
      "`all_cohorts_resource_delta_bn` keeps that distinction visible; the parent decides whether to revise "
      "the broader headline interpretation. [CALCULATION: p7_net_shares.csv, p7_inputs.json]",
      "## Financing and future cohorts",""])
    financing=central[central.arm.eq("financing_only")&central.sharing.isin(["person","pooled"])][[
        "population","frame","financing","sharing","total_bn","future_bn","winners_share"]].copy()
    financing["winners_share"]=financing.winners_share.map(lambda x:f"{100*x:.3f}%")
    for f in ["total_bn","future_bn"]:
        financing[f]=financing[f].map(lambda x:f"{x:.3f}")
    parts.extend([markdown(financing),"",
       "Stationary assigns all accrual and borrowing to current keys. Cohort10/30 move the **whole trust block** "
       "together: current payroll receipts, current OASDI/Part A benefits and the net pension increment. "
       "The non-trust borrowing part uses projected federal-tax shares over the 10/30-year service windows. "
       "Each component is conserved between living and future cohorts. [CALCULATION: p7_inputs.cjs, p7_cohorts.py]",
       "The cohort projection is **[DEGRADED]**, with these explicit proxies:", ""])
    parts.extend("- "+p for p in inputs["cohort"]["proxies"])
    parts.extend(["", "Rule (c) allocates cuts by receipt of the responding programmes, valued at their national "
        "budgets and responses. Cash and SPM noncash receipts are survey fields; health enrollment and school "
        "age/enrollment proxy their receipt. The education budget is split at the case's BEA K12 weight; "
        "college receipt uses A_ENRLW=1 and A_HSCOL=2 (CPS universe16–24), so older student receipt and public/private "
        "type are unidentified and this key is explicitly a proxy. Programmes without a CPS person receipt use a declared universal "
        "service key. It is an allocation assumption, not an observed policy experiment. "
        "[DATA: p7_programme_receipt_keys.csv; CALCULATION: p7_inputs.cjs → responding_programme_key]",
        "## Sharing rules are sensitivities, never bounds",""])
    sh=central[central.arm.eq("recommended")][["financing","sharing","winners_share","total_bn"]].copy()
    sh["winners_share"]=sh.winners_share.map(lambda x:f"{100*x:.3f}%")
    sh["total_bn"]=sh.total_bn.map(lambda x:f"{x:.3f}")
    parts.extend([markdown(sh),"",
        "For s=0.5/0.8 the earner retains s of their own wage change and transfers the remainder to other "
        "unit members, conserving weighted dollars in each unit. All other net channels are pooled. "
        "Singletons retain everything. The two-person counterexample (wages 100/0, shared taxes 40/40) gives "
        "person 60/−40, pooled 10/10, and retaining 20% gives −20/40: an individual's sign can lie outside "
        "both endpoint signs. A separate aggregate control with two units, net wages (100,−1) and (8,−10), "
        "puts 50% ahead under both endpoints but 75% under s=0.8. Counts themselves also need not be bounded. "
        "[CALCULATION: test_p7_frames.py]",
        "The mixed-unit arm includes members' personal cash income net of their own income taxes and FICA "
        "plus per-capita SPM noncash benefits. It shares those resources with the other residents of their "
        "units, conserving the combined total and reporting both sides of the boundary. It is a resources "
        "sensitivity; bargaining, refiling, wage adjustment and member departure behavior are unmeasured. "
        "The all-group units remain in the conservation check. [ASSUMPTION; DATA: p7_mixed_reconciliation.csv]",
        "## Geography, ownership and claims",""])
    geo=cuts[cuts.level.eq("central")&cuts.sharing.eq("pooled")&cuts.financing.isin(["a","b"]) &
        cuts.arm.isin(["recommended","recommended_state_wages","recommended_capitalization","stack"]) &
        cuts.frame.eq("stationary")&cuts.cut.isin(["state3","tenure","edu_nativity"])].copy()
    show=geo[["arm","financing","cut","group","persons_m","mean_usd","winners_share"]].copy()
    show["persons_m"]=show.persons_m.map(lambda x:f"{x:.3f}")
    show["mean_usd"]=show.mean_usd.map(lambda x:f"{x:.1f}")
    show["winners_share"]=show.winners_share.map(lambda x:f"{100*x:.3f}%")
    parts.extend([markdown(show),"",
      "State wage incidence conserves every nativity/skill cell's national gross gain/loss at 1e-9bn; "
      "group skill-cell earnings locate the state shock, then other workers' own earnings allocate it. "
      "This is a geographic incidence arm, not a local-labor-market equilibrium solve. Capitalization puts "
      "the state/local burden on owners using ACS state × income property-value margins mapped to CPS "
      "owner cells. Renters bear no direct capitalization charge; the separate rent channel remains. "
      "[ASSUMPTION; CALCULATION: p7_state_wage_cells.csv, property_key]",
      "Reported RHFS rental-unit owner shares proxy rent-receipt shares. Individuals are identified, "
      "corporation/REIT ownership is identified, and LLC/partnership/trust/other ownership remains unresolved. "
      "The two ownership arms assign that residual either through capital income or individual landlords; "
      "both preserve each matching geography's gross landlord dollars and the housing net. "
      "No interpretation makes an LLC automatically a corporate/REIT owner. "
      "[DATA: inputs_rhfs.csv; p7_owner_types_*.csv, p7_inputs.json]",
      "## Complete social rows and exclusions",""])
    cov=pd.read_csv(OUT/"p7_channel_coverage.csv")
    cov=cov[cov.financing.eq("a")&cov.population.eq("lineage")][["item","low_bn","central_bn","high_bn","key"]].copy()
    for f in ["low_bn","central_bn","high_bn"]:
        cov[f]=cov[f].map(lambda x:f"{x:.6f}")
    parts.extend([markdown(cov),"",
      "All 15 adopted live social rows are allocated, plus an explicit source-rounding row of at most "
      "$1,000 that reconciles the source's separately rounded aggregate. The legacy mobility row is "
      "supplemental and not in this adopted channel set. Fear/security use crime-risk keys; schools use "
      "group state pupil shares; pollution uses the source's local fraction plus national dispersion; "
      "crashes use urban vehicle exposure. Volunteering and trade/consumer-scale rows use national "
      "beneficiary/consumption keys where their location is unobserved. Every key is an incidence proxy. "
      "[DATA: p7_channel_coverage.csv; p7_excluded_channels.csv]",
      "The low source social rows use the equal/raw-coded crime footing and the high use custody, while "
      "the frozen main-case fiscal band uses custody at both ends. These incidence sums are therefore "
      "explicit allocation scenarios, not a claim to reproduce the published paired total. Each source "
      "row and its population is preserved; the mismatch is not hidden by a total label. "
      "[DATA: inputs/social_oct14.json lineage_social_rows.keys]",
      "## Dollar extrema and share extrema",""])
    extrema=pd.read_csv(OUT/"p7_grid_extrema.csv")
    extrema.winners_share=extrema.winners_share.map(lambda x:f"{100*x:.3f}%")
    extrema.total_bn=extrema.total_bn.map(lambda x:f"{x:.3f}")
    parts.extend([markdown(extrema),"",
      "The enumerated grid has 2 fiscal ends × 2 wage incidences × 2 capitalization arms × 3 coherent "
      "housing levels, for each rule and person/pooled sharing. Nonhousing social rows follow the selected fiscal "
      "case end at their central model settings, including the matched source crime footing; credit rules are fixed. "
      "The reported share minimum/maximum are over this finite declared grid, not "
      "universal bounds on household outcomes or all uncertain social parameters. "
      "[CALCULATION: p7_enumerated_grid.csv]",
       "## Literature within-cell substitution and skill split", ""])
    ns=pd.read_csv(OUT/"p7_nest_shares.csv")
    display=ns[ns.population.eq("lineage")&ns.sharing.eq("pooled")][[
        "base_arm","epsilon","financing","level","total_bn","winners_share",
        "winners_share_conditional_se","delta_vs_infinite_bn","delta_vs_infinite_ahead_pp"]].copy()
    for f in ["total_bn","delta_vs_infinite_bn","delta_vs_infinite_ahead_pp"]:
        display[f]=display[f].map(lambda x:f"{x:.6f}")
    display.winners_share=display.winners_share.map(lambda x:f"{100*x:.6f}%")
    display.winners_share_conditional_se=display.winners_share_conditional_se.map(lambda x:f"{100*x:.6f}pp")
    central_eps=ns[ns.population.eq("lineage")&ns.sharing.eq("pooled")&ns.base_arm.eq("nest_recommended")&
                   ns.level.eq("central")&~ns.epsilon.eq("infinite")]
    parts.extend([markdown(display),"",
        f"Across rules a/b/c the recommended central share ahead moves by at most "
        f"{central_eps.delta_vs_infinite_ahead_pp.abs().max():.3f} percentage points. "
        "The minority-ahead conclusion survives both literature arms. The modeled wage split does not: "
        "the small aggregate native loss at infinity becomes a native gain at both finite values, while "
        "earlier immigrants move from a small gain to a loss. These are model outcomes under transported parameters. "
        "[CALCULATION: p7_nest_shares.csv; p7_nest_wage_split.csv; p7_nest_delivered_wages.csv]",
        "Each finite-epsilon row changes only within-cell substitution from its matching infinite control. "
        "`nest_recommended` is stationary financing, complete social rows, lineage payer pool and crossing credits; "
        "`nest_stack` also takes state wage incidence, capitalization and the central owner-type allocation. "
        "Low/high preserve personal specifications 16/11 and their cash/GDP normalization; central is the priced-array midpoint. "
        "The new controls reproduce every matching prior P7 sign count and dollar total; the frozen hybrid also remains unchanged. "
        "[CALCULATION: p7_nest_shares.csv; p7_gates.json]",
        "The nest is invoked read-only via its existing row-4 solve and lineage adapter, with a copied scenario list. "
        "Finite epsilons retain the infinite sibling's cell-specific added-descendant multipliers, exactly as the existing ε=3 arm. "
        "Native and earlier-immigrant after-tax wage changes, plus induced labor receipts, change together. "
        "The unchanged delivered infinite baseline receives each epsilon's wage delta, preserving the delta's "
        "state × nativity × skill × sign totals under payer thinning. This avoids reassigning the native/immigrant "
        "transfer while preserving the recommended control. Raw solver wage levels below and actual delivered levels "
        "in `p7_nest_delivered_wages.csv` are distinguished; their epsilon changes match at 1e-9bn. "
        "Extra receipts use the existing epsilon arm's combined national tax key under (a), equal persons under (b), "
        "and the responding-programme receipt key under (c); the nest does not identify their government jurisdiction. "
        "[ASSUMPTION; CALCULATION: p7_nest.py, p7_frames.py]",
        "Caiumi–Peri's 8.7 is the rounded reciprocal of Table 7's no-diploma coefficient, "
        "not a pooled HS-or-less estimate. Piyapromdee's 17.9 is Table 1's rounded low-skill native/immigrant elasticity. "
        "Both arms apply a common epsilon to both model skill cells, as the existing nest does; that transport is assumed. "
        "These are model sensitivities, not estimates on the lineage. "
        "[SOURCE: https://www.nber.org/papers/w32389; https://doi.org/10.1093/restud/rdaa029; "
        "production_nativity_nest_2026_09_22/builder.py SIGMA_NI_CITATION]", ""])
    wage=pd.read_csv(OUT/"p7_nest_wage_split.csv")
    for f in ["after_tax_wage_bn","delta_vs_infinite_bn","induced_receipts_bn","delta_receipts_bn"]:
        wage[f]=wage[f].map(lambda x:f"{x:.6f}")
    parts.extend([markdown(wage),"",
        "The cut tables are `p7_nest_cuts.csv`, with state3, edu_nativity, tenure, decile and every prior cut; "
        "person, pooled, unequal and mixed-unit sharing are all retained. `identified_union` remains a payer-pool "
        "sensitivity of the same lineage production/fiscal case, not a union-only fiscal rerun. "
        "These epsilon arms sit beside the earlier declared grid; its extrema are not bounds over the new arms. "
        "The finite-epsilon account change is Δ(native wages + earlier-immigrant wages + induced receipts); "
        "the frozen main-case files stay unchanged. [DATA: p7_nest_shares.csv, p7_nest_cuts.csv]", ""])
    bills=pd.read_csv(OUT/"p7_card_wage_bills.csv")
    lineage_bills=bills[bills.population.eq("lineage")]
    group_low=lineage_bills.iloc[0]
    show=bills[["population","branch","hs_or_less_bn","above_hs_bn","transfer_bn","card_low_bn","card_high_bn",
                "low_bill_change_pct","high_bill_change_pct"]].copy()
    for f in show.columns[2:]:
        show[f]=show[f].map(lambda x:f"{x:.6f}")
    parts.extend([markdown(show),"",
        f"On the lineage payer/member frame the half assignment moves ${lineage_bills.transfer_bn.sum():.3f}bn "
        f"of the annual wage bill to the low cell. The group's low-cell removal share falls from "
        f"{100*group_low.group_low_removal_share_before:.3f}% to {100*group_low.group_low_removal_share_card:.3f}%. "
        "This sizes a potentially consequential input change without estimating its equilibrium effect. "
        "[DATA: p7_card_wage_bills.csv]",
        "The builder accepts only hs_or_less and below_ba and exposes no skill-split option. Card's requested arm "
        "is therefore sized only: half the CPS some-college/associate wage bill (A_HGA 40–42) moves from the high to "
        "the low cell, conserving each branch and national total. The source's 1–3-year postsecondary definition "
        "and efficiency-hours weights are not replicated by this wage-bill diagnostic. "
        "No Card share-ahead or net-dollar estimate can be inferred from these input shifts. The full file also reports "
        "skill shares and group removal shares before/after. "
        "[SOURCE: https://davidcard.berkeley.edu/papers/immigration-and-inequality.pdf pp.12–13; "
        "DATA: p7_card_wage_bills.csv; CALCULATION: p7_nest.py]",
       "## Live table map", "",markdown(pd.read_csv(OUT/"p7_table_map.csv")),"",
      "## Gates, reproduction and limits", "",
      f"All **{len(gates)} P7 gates** pass, in addition to the unchanged 511 hybrid gates. "
      "New allocations close at absolute 1e-9bn; weights and combined mixed-unit resources are conserved. "
      "The primary source's serializing residual is allocated explicitly. [DATA: p7_gates.json; gates.json]",
      "Winner-share SEs use the 160 official successive-difference replicate weights and hold the "
      "priced arrays, sharing assignments and model fixed. They measure conditional prevalence "
      "uncertainty, not uncertainty of the allocation or causal model. Credit-flow SEs come from the "
      "primary tax model's full calibrated joint replicates. [DATA: p7_net_shares.csv, p7_inputs.json]",
      "```sh\nsh infra/immigration-fiscal/winners_losers_2026_09_24/run_all.sh\n"
      "uv run --no-project python3 scripts/rerun_lane.py infra/immigration-fiscal/winners_losers_2026_09_24 "
      "\"sh {lane}/run_all.sh\"\n```",
      "`run_all.sh` names the imported helpers and directory-level pytest files for the coverage scanner. "
      "No `--allow-unrun` is used. `measured_run.py` records Python wall time/child peak RSS under ignored "
      "`_cache/timings.jsonl`; it fails above 2500 MiB and propagates child failure. No ps/sysctl/time -l is used.",
      "Source review: the initial owner-geometry replacement and one-fix comparator bugs were corrected; "
      "the generated-output pin now has a location-independent logical identity and a regression test. "
      "An actual within-run peer input change triggered frozen-vintage acquisition and drift guarding. "
      "The raw record includes initial failures; successful rerun receipts are recorded by the parent. "
      "[CALCULATION: test_p7_frames.py; scratch winners-code-review.md]",
      "The LLM is an instrument with dispositions on immigration; the stated conclusions follow the "
      "matched numerical scenarios and gates, not the reviewers' predictions. The older minority-ahead "
      "claim survives, while its exact share and who is ahead are conditional on financing, household "
      "sharing, channels and geography. [FRAMING-SENSITIVE; SOURCE: notes/llm-bias-caveat.md]",
      "## Run log (UTC)","",
      "Timing receipts below come directly from Python, captured as a fixed input before the final "
      "byte-identical rerun. A preliminary successful run was rejected on inspection for mixed social "
      "vintages; another failed on the source's separately rounded aggregate. Those failures remain in "
      "the record. Repeated cut filters were replaced with grouped aggregation; the unrelated external "
      "congestion setup hotspot is documented in performance.md.",""])
    for r in timings:
        parts.append(f"- {r['utc']}: exit {r['exit_code']}; {r['seconds']:.3f}s, {r['peak_rss_mb']:.3f} MiB; "
                     +" ".join(r["command"]).replace(str(ROOT)+"/", ""))
    parts.extend(["", "---", "", "# Preserved prior calculation record", ""])
    old=subprocess.run(["git","-C",str(ROOT),"show",
        "2204a2bc:infra/immigration-fiscal/winners_losers_2026_09_24/RESULT.md"],capture_output=True,text=True,check=True).stdout
    (HERE/"RESULT.md").write_text("\n\n".join(parts)+old)
    print("[document] RESULT.md generated from P7 tables; prior record retained")


if __name__=="__main__":
    main()
