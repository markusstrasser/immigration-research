"""Generate v8 verdict sentences from executed tables; preserve accepted history."""
from __future__ import annotations

import json
import gzip
from pathlib import Path

import pandas as pd

from p7_document import markdown
from p8_phase_a_document import FIXES

HERE = Path(__file__).resolve().parent
OUT = HERE / "derived/oct15"
MARKER = "## v8 case (oct15)"


def format_table(table):
    table = table.copy()
    for col in table:
        if "winners_share" in col or col.endswith("share"):
            table[col] = table[col].map(lambda x: f"{100*x:.4f}%" if pd.notna(x) else "")
        elif pd.api.types.is_float_dtype(table[col]):
            table[col] = table[col].map(lambda x: f"{x:.6f}" if pd.notna(x) else "")
    return markdown(table)


def main():
    shares = pd.read_csv(OUT / "p7_net_shares.csv")
    gates = json.loads(gzip.decompress((OUT / "p7_gates.json.gz").read_bytes()))
    inputs = json.loads((OUT / "p7_inputs.json").read_text())
    clock = json.loads((HERE / "inputs/phase_b_clock.json").read_text())
    if not all(g["passed"] for g in gates.values()):
        raise SystemExit("[BLOCKED] v8 document requires all computation gates")
    selected = shares[shares.arm.eq("recommended") & shares.epsilon.eq("infinite") & shares.sharing.eq("pooled")]
    rec = selected[selected.frame.eq("stationary") & selected.level.eq("central")].set_index("financing")
    verdict = ("On corrected v8, stationary financing, the current paired social stack and household pooling, "
        + " / ".join(f"{100*rec.loc[r,'winners_share']:.4f}%" for r in ("a","b","c"))
        + f" of other residents are ahead under rules a/b/c; their central annual net is ${rec.loc['a','total_bn']:.6f}bn. "
        + "Cohort financing is beside. [MODEL / FRAMING-SENSITIVE; CALCULATION: derived/oct15/p7_net_shares.csv]")
    fiscal = pd.read_csv(OUT / "p8_channel_ledger.csv")
    fiscal = fiscal[fiscal.channel.str.startswith("fiscal/")].groupby(["basis","end"], as_index=False).total_bn.sum()
    costs = fiscal.set_index(["basis","end"]).total_bn
    membership = inputs["membership"]
    parts = [MARKER + " — " + clock["date"], "", verdict, "",
        "All effects are presence minus removal; a positive amount means ahead from the lineage's presence. "
        "The stationary frame is the verdict. Cohort30 and cohort10 are beside. The low/high net rows pair the "
        "fiscal ends with the producer-range ratios transported to the live social rows; the central uses "
        "the central social rows at the fiscal midpoint. The paired-source ledger separately holds social "
        "parameters central at each fiscal end. [ASSUMPTION; DATA: p7_net_shares.csv; p8_channel_ledger.csv]", "",
        "All accepted Phase-A fixes remain active; fix 8 now uses raw surviving-person item-11 changes. "
        "[CALCULATION: p8_incidence.ALL_FIXES; retained phase-A definitions]", "",
        markdown(pd.DataFrame([(r[0],r[1],r[3],r[4]) for r in FIXES],
            columns=["fix","finding IDs","source files","premise gates"])), "",
        "### Shares ahead under each financing rule", "",
        format_table(selected[["frame","level","financing","persons_m","total_bn","future_bn","winners_share"]]
            .sort_values(["frame","level","financing"], key=lambda s: s.map({"stationary":0,"cohort30":1,"cohort10":2}) if s.name=="frame" else s)), "",
        "Rules a/b/c use tax shares, per-person financing, and responding-programme receipt, respectively. "
        "Federal and state-local programme keys remain separate; the trust accrual uses covered earnings "
        "under stationary financing and future payroll payers, including future births, under cohort financing. "
        "The FY2024 borrowing share is the central financing assumption. Public-capital return is a resource cost, "
        "and the unlocated financing block is explicitly per head with zero borrowing. [FRAMING-SENSITIVE; CALCULATION: p8_incidence.py]", "",
        "### Case and channel closure", "",
        f"The corrected case is ${-costs.loc[('set','low')]:.6f}–{-costs.loc[('set','high')]:.6f}bn set and "
        f"${-costs.loc[('cash','low')]:.6f}–{-costs.loc[('cash','high')]:.6f}bn cash, over "
        f"{inputs['population']['with_coverage']:.6f} members including coverage. "
        "The ledger signs below are from other residents' side. [DATA: p8_channel_ledger.csv; p7_inputs.json population]", "",
        format_table(fiscal), "",
        f"The payer pool changes from {membership['oct14_payer_people']:.6f} to {membership['oct15_payer_people']:.6f} people, "
        f"exactly removing the completion records' {membership['removed_completion_people']:.6f} weight "
        f"(gap {membership['payer_gap_people']:.9f}). Coverage contributes {membership['coverage_payer_people']:.0f} payer people. "
        "Actual completion members join the group; survey-absent coverage people have no fabricated payer/household records. "
        "[CALCULATION: p7_inputs.json membership; p8_membership.py]", ""]
    channels = pd.read_csv(OUT / "p7_channel_table.csv")
    table = channels[channels.financing.eq("a") & channels.frame.isin(["stationary","cohort30","cohort10"]) &
        channels.arm.eq("recommended") & channels.epsilon.eq("infinite")]
    parts += [format_table(table[["frame","level","channel","total_bn"]]), "",
        "The mixed_boundary row is added only for the mixed_unit sharing arm. It is excluded from the ordinary "
        "pooled/person channel sum. Item 11 is the budget's recomputation and the stayers' direct resource changes; "
        "the pooling arm compares the household's before/after sharing of resources. Actual surviving-person tax and "
        "benefit flows enter that arm once; its separate pooling residual is the member/non-member resource boundary. "
        "The budget retains every item-11 part. Fixed-pool attribution movements and unlocated credit extrapolation "
        "do not by themselves create disposable resources; the complete attribution reading is the explicit "
        "item11_attribution beside arm. Raw surviving-person flows are measured before subtracting either direction "
        "of the old-credit convention, so a second crossing-credit gain is forbidden. Neither pooling rule models re-partnering. "
        "[CALCULATION: p8_stayers.py; p8_membership.replacement_credit; p7_mixed_reconciliation.csv]", "",
        "### Isolated v8 source items and round-3 social changes", ""]
    effects = json.loads((OUT / "p8_item_effects.json").read_text())
    item_rows = []
    for item, by_basis in effects["items"].items():
        for basis, by_end in by_basis.items():
            for end, values in by_end.items():
                item_rows.append(dict(item=item,basis=basis,end=end,**{k:v for k,v in values.items() if isinstance(v,(int,float))}))
    parts += [format_table(pd.DataFrame(item_rows)), "",
        "The isolated dollar increments above execute each source item alone on v7's actual endpoint specifications. "
        "The isolated share changes below add each source item to the all-off fiscal base with current incidence "
        "keys, payer frame and paired budget counterflows held fixed. Its exported social-key contributions follow "
        "completion/coverage counts in each scope and consumption receipts; item 11 replaces the old direct-credit "
        "vector with raw survivor flows. The leave-one-out rows provide a second controlled decomposition. These "
        "do not claim a separately solved one-item population equilibrium. "
        "The item-interaction financing parts remain explicit in p8_item_effects.json. [ASSUMPTION; CALCULATION: specs.cjs; p8_ablations.py]", ""]
    ablations = pd.read_csv(OUT / "p8_ablations.csv")
    parts += [format_table(ablations[ablations.sharing.eq("pooled")][["scenario","frame","level","financing","total_bn","winners_share","delta_total_bn","delta_ahead_pp"]]), "",
        "Government purchases removed and re-spending of the saving are both central, with the same age-mortality "
        "recipient vector. Their one-sided and neither-side readings are named beside variants. The low fiscal row "
        "uses the adopted case while victims keep equal NCVS footing; matched_justice_footing stays beside. "
        "The added people's crime sender rows are zero; their other rows use the producer's own key shares, including "
        "item 11's consumption shift. Current row levels and declared producer ranges come from the live JSON; "
        "producer ratios transport its uncertainty, while separately declared point budget counterflows stay fixed. "
        "[DATA: live real_costs_totals.json v8_social_environment; p7_channel_coverage.csv]", "",
        "### Joint change from accepted oct14 Phase A", ""]
    old = pd.read_csv(HERE / "inputs/phase_a_joint_oct14.csv")
    keys = ["financing","frame","level","arm","epsilon","sharing"]
    compare = shares.merge(old[keys+["total_bn","winners_share"]], on=keys, suffixes=("_oct15","_oct14"), validate="one_to_one")
    compare["delta_total_bn"] = compare.total_bn_oct15 - compare.total_bn_oct14
    compare["delta_ahead_pp"] = 100*(compare.winners_share_oct15-compare.winners_share_oct14)
    compare.to_csv(OUT / "p8_joint_change.csv", index=False, lineterminator="\n", float_format="%.15g")
    matched = compare[compare.arm.eq("recommended") & compare.epsilon.eq("infinite") & compare.sharing.eq("pooled")]
    parts += [format_table(matched[["frame","level","financing","total_bn_oct14","total_bn_oct15","delta_total_bn","winners_share_oct14","winners_share_oct15","delta_ahead_pp"]]), "",
        "The accepted Phase-A reference is an archived calculated table; no oct14 output is regenerated. "
        "The comparison retains all Phase-A corrections and the stationary-first ruling. [DATA: inputs/phase_a_joint_oct14.csv]", "",
        "### Geography, uncertainty, provenance and limits", ""]
    cuts = pd.read_csv(OUT / "p7_cuts.csv.gz")
    geo = cuts[cuts.frame.eq("stationary") & cuts.level.eq("central") & cuts.sharing.eq("pooled") & cuts.epsilon.eq("infinite") & cuts.cut.isin(["state3","tenure"])]
    parts += [format_table(geo[["arm","financing","cut","group","persons_m","mean_usd","winners_share"]]), "",
        "State and landlord claims are specific to the displayed arm. Rental stock enters capitalization, and "
        "landlord ownership reassignment preserves state dollars. FARS fatal victim ages/roles proxy crash injuries. "
        "School correction geography remains an explicitly degraded administrative/district proxy, and S&L net "
        "financing follows responded spending geography. Source item 11 retains its adopted fixed-membership "
        "counterfactual; the item10 × item11 nonlinear recomputation is uncomputed. Unlocated stayer flows use named "
        "same-state buckets and D a national per-head bucket. Coverage is constructed, with source limitations. "
        "The LLM instrument can introduce framing bias. [DEGRADED / FRAMING-SENSITIVE; DATA: p7_inputs.json]", "",
        format_table(pd.read_csv(OUT / "p7_grid_extrema.csv")), "",
        f"All {len(gates):,} retained gates pass; fiscal and social ledgers close at every end and pension set "
        "within the declared absolute bn tolerance. Inputs are checked by SHA-256 and immutable source commit; "
        "missing manifests and source drift stop the run. Conditional prevalence SEs are not newly estimated "
        "for v8. Cut files use deterministic gzip and explicit frame tags. Historical debt interest remains a "
        "separate unpriced stock object. [DATA: p7_gates.json.gz; p7_inputs.json; inputs/p8_pins_oct15.json]", "",
        "```sh\nsh infra/immigration-fiscal/winners_losers_2026_09_24/run_all.sh\n"
        "uv run --no-project python3 scripts/rerun_lane.py infra/immigration-fiscal/winners_losers_2026_09_24 "
        "\"sh {lane}/run_all.sh\"\n```", "",
        "Would change it: measured recipient keys, a joint completion/removal counterfactual, or different explicit "
        "financing/sharing premises. Model self-report: inherited GPT-6 agent; no unverified exact served-model claim. "
        "The executed source totals and verifier receipts carry the numerical claims. [UNVERIFIED: exact model id]", ""]
    text = (HERE / "RESULT.md").read_text()
    previous = text.split(MARKER, 1)[0].rstrip()
    previous = "**Verdict:** " + verdict + "\n" + previous.split("\n",1)[1]
    (HERE / "RESULT.md").write_text(previous + "\n\n" + "\n\n".join(parts) + "\n")
    print("[document] generated oct15 section and verdict; prior records retained")


if __name__ == "__main__":
    main()
