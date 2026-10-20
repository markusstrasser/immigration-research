"""Live matched-cash readings, independent of the optional debt-split recipes.

Native-First: use the existing premium, price, row and weighting evaluators.
The case key is the sole run selector; source pins remain mandatory.
"""
import argparse
import json
import hashlib
import sys
import gc
from pathlib import Path

import numpy as np
import pandas as pd

import beside_arms as B
import beside_extra as X
import g2_premium as G
import mexico as MX
from mexico_capital import projected_shapes
import pension_cash as PC
import valuation as V
import world_ledger as W
from service_prices import prepare_us_service_values
from population_basis import economic_path
from gz_io import read_artifact, write_csv_gz

HERE = Path(__file__).resolve().parent
WEIGHTS = ("equal", "equal_lambda_1.16", "equal_lambda_1.5", "equal_lambda_hendren_a",
           "hendren_a", "hendren_b", "log_a", "log_b")
PARTS = dict(world_total_bn="world_total", group_total_bn="group_total",
             other_us_residents_bn="other_us_residents_total", mexico_residents_bn="mexico_residents")


def memory_phase(label):
    sys.path.insert(0, str(HERE.parent/"scripts"))
    from memory_budget import require_within_budget
    peak = require_within_budget("matched-cash " + label)
    print(f"CASH_PHASE {label} physical_peak_bytes={peak}", flush=True)


def cash_contract(I):
    W.gate("reading_basis_cash", I.get("pension_basis") == "matched_cash"
           and I.get("us_pension_basis") == "cash" and bool(I.get("pension_cash_adapter")))
    W.gate("reading_receipt_contract_present", "receipt_incidence_class" in I["vgen"])
    receipts = I["vgen"].receipt_incidence_class
    W.gate("reading_receipts_present", receipts.notna().all()
           and not receipts.isin(["unknown", "", "unclassified"]).any())
    expected = I["glines"][I["glines"].side.eq("receipt")]
    actual = I["vgen"][I["vgen"].side.eq("receipt")].copy()
    if "origin_line" in actual:
        actual["line"] = actual.origin_line
    W.gate("reading_receipt_cells_complete", bool(len(expected)) and
           set(zip(expected.band_end, expected.generation, expected.line)) <=
           set(zip(actual.end, actual.generation, actual.line)))


def recipient_cells(v, contract):
    """Retain raw line identity while letting every class use its own price rule."""
    source = contract.set_index(["end", "line"])
    records = []
    for r in v.to_dict("records"):
        r["origin_line"] = r["line"]
        key = (r["end"], r["line"])
        source_record = source.loc[key] if str(r["line"]).startswith("coverage_") and key in source.index else None
        if source_record is not None and source_record.get("recipient_scope") == "counted":
            r["origin_line"] = "v9_counted_" + r["line"]
        # Drop the nested source text before constructing scalar records. Arrow
        # string inference otherwise materializes it once per expanded component
        # even if the DataFrame drops that column immediately afterward.
        encoded = r.pop("recipient_components_json", None)
        if isinstance(encoded, str) and encoded:
            for c in json.loads(encoded):
                x = dict(r, **c)
                if r.get("cls") == "proportional_mix":
                    x["recipient_component_transport"] = "signed_proportional_source_mix"
                x["side"] = c["component_side"]
                x["receipt_incidence_class"] = c["cls"] if x["side"] == "receipt" else "not_receipt"
                x["net_cost_bn"] = c["G_bn"]
                records.append(x)
        else:
            if str(r["line"]).startswith("coverage_"):
                parent = source.loc[(r["end"], r["line"])]
                r["line"] = parent.source_line
                if parent.source_side == "receipt":
                    r["side"] = "receipt"
            records.append(r)
    out = pd.DataFrame(records).drop(columns=["recipient_components_json"], errors="ignore")
    W.gate("recipient_cell_transport_fiscal_closure", abs(out.net_cost_bn.sum()-v.net_cost_bn.sum()) < 1e-9)
    return out


def reading_reference():
    """Build fixed Mexico reference cells before retaining the wide US frame."""
    trans_nat = G.transitions()
    nat_cells = {p: G.mexico_cells(p) for p in ("gdp", "consumption")}
    rates = MX.ppp()
    en = B.enigh_persons({})
    cells, _ = X.subset_cells(en, en.tam_loc.eq(1).to_numpy(), rates)
    del en
    em = B.emovi_with_residence({})
    tt, _, _ = MX.transitions(em[em.city100k14])
    urban_trans, _ = B.transition_dict(tt, fallback=trans_nat)
    del em
    gc.collect()
    memory_phase("Mexico-reference")
    ratios, _ = X.icp_values()
    return dict(trans_nat=trans_nat, nat_cells=nat_cells, rates=rates, cells=cells,
                urban_trans=urban_trans, ratios=ratios)


def scenarios(I, d):
    """The existing R1/R2/R3 recipes, recomputed on the selected donor frame."""
    parents = I["parents_schooling"]
    ref = I["reading_reference"]
    trans_nat, nat_cells, cells, urban_trans = (ref[k] for k in ("trans_nat", "nat_cells", "cells", "urban_trans"))
    ratios = ref["ratios"]
    rpp, _, _ = B.residence_prices(d)
    ds = d.assign(earn=d.earn / (rpp / 100))
    tab0 = B.premium_table(d, parents, trans_nat, nat_cells)
    urban = B.premium_table(ds, parents, urban_trans, cells)
    ds["industry"] = X.industry_codes(ds)
    ds["cls"] = X.classify(ds.industry.to_numpy())
    prem = W.premium_rows(I)
    e0 = {"G1": float(X.central_row(tab0, "own_schooling_all_ages").mexico_earnings_bn),
          "G2": prem["G2"]["e_mx"]["central"]}
    _, factors = X.industry_table(ds, ratios, e0, {g: prem[g]["employer_us"] for g in e0})
    r1 = X.with_central(urban, "consumption", "p56")
    r2 = X.output_prices(X.with_central(urban, "gdp", "p70"), {g: factors[g]["services"] for g in factors})
    r2c = X.with_central(urban, "consumption", "p70")
    annual = X.annual_ratio(tab0, 2., True)
    e_us = {conv: float(X.central_row(tab0, conv).us_earnings_bn)
            for conv in tab0[tab0.generation.eq("G1")].convention.unique()}
    r3, _ = X.same_person(r1, annual, e_us)
    v3a = B.services_at_prices(I["vgen"], ratios[B.ICP_HEALTH], ratios[B.ICP_GOV_IND])
    kw2 = dict(pgc="response_only", care_vg=(ratios[B.ICP_HEALTH],)*3, mexico_health_vg=(1.,)*3)
    # Remittance principal stays at its Banxico value. The completed sender mix
    # is calculated once from the same cash frame and reused by every reading.
    base_rows, _, _ = X.evaluate(I, weighting_factors(I))
    rem = base_rows.set_index("row").loc[["remit_G1", "remit_G2"]]
    common = dict(I, household_price_basis="consumption", remittance_price_basis="consumption")
    return {
        "R1": (dict(common, g2=r1), dict(remit_rows=rem), None),
        "R2": (dict(I, g2=r2, vgen=v3a), dict(kw2, remit_rows=rem),
               (dict(common, g2=r2c, vgen=v3a), dict(kw2, remit_rows=rem))),
        "R3": (dict(common, g2=r3), dict(remit_rows=rem), None),
    }


def weighting_factors(I):
    fac = W.channel_factors(I, "money")
    fac["_lambda"] = {f"equal_lambda_{k}": v for k, v in W.LAMBDAS.items()}
    fac["_lambda"]["equal_lambda_hendren_a"] = fac["fiscal_a"]["inv_g"]
    return fac


def pension_share(I, share):
    out = dict(I, mxb=I["mxb"].copy())
    m = out["mxb"].item.str.contains("pensions paid", regex=False)
    # Source pesos and recipient value stay fixed; only public financing moves.
    for column in ("fiscal_cost_bn", "fiscal_cost_pesos_bn", "source_pesos_bn"):
        out["mxb"].loc[m, column] *= share
    out["public_pension_share"] = share
    return out


def partial_group_rows(rows, prem, full, full_prem):
    by, rr = full.set_index("row"), rows.set_index("row")
    excluded_debit = 0.
    non_group = by[~by.party.isin(W.GENS)].index
    rr.loc[non_group, by.columns] = by.loc[non_group, by.columns]
    for gen in W.GENS:
        fraction = prem[gen]["persons"] / full_prem[gen]["persons"]
        for rid in (f"ingroup_victims_{gen}", f"uncompensated_received_{gen}"):
            rr.loc[rid, ["low", "central", "high"]] = by.loc[rid, ["low", "central", "high"]] * fraction
        rid = f"remit_{gen}"
        if rid in rr.index:
            sender_share = prem[gen]["e_us_cash"] / full_prem[gen]["e_us_cash"]
            rr.loc[rid, ["low", "central", "high"]] = by.loc[rid, ["low", "central", "high"]] * sender_share
            excluded_debit += float(by.loc[rid, "central"] - rr.loc[rid, "central"])
    return rr.reset_index(), excluded_debit


def prepare(case):
    """Materialize valuation on the exact package export, including post-engine cells."""
    pins = json.loads((HERE/"inputs/pension_cash_pins.json").read_text())["artifacts"]
    artifact = json.loads(read_artifact(HERE/pins[case+"_cash"]["path"]))
    gl, vg, val = PC._value(case, artifact["results"]["set"], basis="set")
    PC._closure(artifact["results"]["set"], gl, vg, val)
    for name, frame in (("valuation.csv", val), ("valuation_by_generation.csv", vg)):
        frame.to_csv(V.case_path(name, case), index=False, lineterminator="\n", float_format="%.12f")
    V.case_path("valuation_meta.json", case).write_text(json.dumps(dict(case=case,
        medicaid_vg=V.CLASSES["medicaid"][1:4], source="exact package export"), sort_keys=True, indent=1)+"\n")
    basis = V.basis_of(case)
    V.mexico_budget(basis, case=case).to_csv(economic_path(V.DERIVED/"mexico_budget.csv", basis, case), index=False,
                                lineterminator="\n", float_format="%.12f")


def run(case):
    import coverage_transport as CT
    import coverage_recipient_values as CR
    import scope_b as SB
    record = json.loads((HERE/"inputs/pension_cash_pins.json").read_text())["artifacts"][case+"_cash"]
    body = read_artifact(HERE/record["path"])
    W.gate("selected_package_artifact_hash", hashlib.sha256(body).hexdigest() == record["sha256"])
    artifact = json.loads(body)
    W.gate("selected_package_artifact_case", artifact["case"] == case and artifact["package_set"] == "cash")
    set_lines = PC._frame(artifact["results"]["set"]["lines"])
    del artifact, body
    I = W.load(case, V.basis_of(case), generation_lines=set_lines)
    del set_lines
    I = dict(I)
    I.pop("pension_basis", None)
    I = PC.adapt_cash(I)
    memory_phase("exact-cash-adapter")
    I["financing_basis"] = "pooled_no_debt_split"
    cash_contract(I)
    # This primary-source construction is identical in every reading/scope.
    # Reuse its small result instead of retaining three large CSV parse heaps.
    I["parents_schooling"], _ = G.parents_schooling()
    gc.collect()
    memory_phase("shared-parent-table")
    I["reading_reference"] = reading_reference()
    contract = pd.read_csv(V.case_path("coverage_valuation_contract_cash.csv", case))
    I["vgen"] = recipient_cells(I["vgen"], contract)
    I = CR.supplement(I, case, "cash")
    completed = G.load_asec(V.basis_of(case), case=case)
    columns = ["PH_SEQ", "PPPOS", "gen", "pw", "pw_counted", "coverage_pw", "sex", "A_AGE",
               "own_cat", "diploma", "works", "birth_year", "earn", "HRSWK", "arrival_age"]
    W.gate("economic_frame_fields_present", set(columns) <= set(completed.columns))
    completed = completed[columns].copy()
    gc.collect()
    memory_phase("economic-frame")
    _, transport = CT.load_donors(case, "cash")
    I["coverage_economic_counterfactual"] = transport
    # The premium and weight producers use these same completed donor weights.
    I["capital_people"] = completed
    I["capital_projected_gen_industry_wages"] = projected_shapes(I)
    fac = weighting_factors(I)
    recipes = {("A_completed", name): recipe for name, recipe in scenarios(I, completed).items()}
    counted, counted_frame = SB.build(I, completed)
    recipes.update({("B_counted_only_beside", name): recipe for name, recipe in scenarios(counted, counted_frame).items()})
    gc.collect()
    memory_phase("recipes")
    records, details, private, cells, comparisons = [], [], [], [], []
    completed_rows, completed_private = {}, {}
    for (scope, reading), (inputs, keywords, twin) in recipes.items():
        cash_contract(inputs)
        for share in ((1., .5, 0.) if scope == "A_completed" else (1.,)):
            obj = pension_share(inputs, share)
            for bound in ("zero", "upper"):
                for end in ("low", "high"):
                    rows, prem, _ = X.evaluate(obj, fac, **dict(keywords, g3_bound=bound, end=end))
                    excluded_debit = 0.
                    if scope == "A_completed":
                        if share == 1:
                            completed_rows[(reading, bound, end)] = (rows.copy(), prem)
                    else:
                        full, full_prem = completed_rows[(reading, bound, end)]
                        # B reports a partial group position beside complete-
                        # lineage effects on others, as the accepted memo says.
                        rows, excluded_debit = partial_group_rows(rows, prem, full, full_prem)
                    totals = W.totals(rows, prem, dict(obj, account_end=end), "central", fac, obj["pos"], WEIGHTS)
                    key = dict(case=case, basis="matched_cash", reading=reading, end=end,
                               g3_bound=bound, public_pension_share=share, scope=scope,
                               enters_total=scope == "A_completed", excluded_senders_debit_bn=excluded_debit)
                    details.append(rows.assign(**key))
                    zero_totals = None
                    if scope == "A_completed" and share == 1:
                        priced = prepare_us_service_values(obj["vgen"], keywords.get("pgc", "average_cost"))
                        m = priced.origin_line.str.contains("lane_residual|net_profile_calibration", regex=True)
                        gap = priced[m & priced.end.eq(end)].groupby("generation").V_central_bn.sum()
                        zr = rows.copy().set_index("row")
                        for gen in W.GENS:
                            zr.loc[f"us_budget_value_{gen}", ["low", "central", "high"]] -= gap.get(gen, 0.)
                        zero_totals = W.totals(zr.reset_index(), prem, dict(obj, account_end=end), "central", fac, obj["pos"], WEIGHTS)
                    for wt in WEIGHTS:
                        t = totals[totals.weighting.eq(wt)].set_index("party").bn
                        rec = dict(key, weighting=wt, status="[DEGRADED] P032 all-public proxy" if share == 1 else "[DEGRADED] funding sensitivity",
                                   **{k: t[p] for k, p in PARTS.items()}, breakeven_w=t["breakeven_w"])
                        W.gate("cash_reading_party_closure", abs(rec["world_total_bn"]-sum(rec[k] for k in
                               ("group_total_bn", "other_us_residents_bn", "mexico_residents_bn"))) < 1e-9)
                        if scope != "A_completed":
                            rec.update(world_total_bn=np.nan, breakeven_w=np.nan,
                                       status="PARTIAL GROUP SCOPE; complete-lineage others; no world total")
                        records.append(rec)
                        if zero_totals is not None:
                            z = zero_totals[zero_totals.weighting.eq(wt)].set_index("party").bn
                            comparisons.append(dict(key, weighting=wt, convention="proportional mix versus zero recipient value; same fiscal cost",
                                proportional_world_bn=t["world_total"], zero_recipient_world_bn=z["world_total"],
                                convention_gap_bn=t["world_total"]-z["world_total"]))
                    if share == 1:
                        pg_obj, pg_kw = twin if twin else (obj, keywords)
                        if twin:
                            pg_obj = pension_share(pg_obj, share)
                            pg_rows, pg_prem, _ = X.evaluate(pg_obj, fac, **dict(pg_kw, g3_bound=bound, end=end))
                        else:
                            pg_rows, pg_prem = rows, prem
                        if scope == "A_completed":
                            completed_private[(reading, bound, end)] = (pg_rows.copy(), pg_prem)
                        elif twin:
                            pg_rows, _ = partial_group_rows(pg_rows, pg_prem, *completed_private[(reading, bound, end)])
                        cv = pg_obj["vgen"][pg_obj["vgen"].end.eq(end)]
                        pc = PC.private_cash_inputs(dict(pg_obj, vgen=cv))
                        for gen in W.GENS:
                            c = pg_rows.set_index("row").central
                            gain = c[f"premium_{gen}"] + pc[gen]["us_taxes_bn"] + c[f"mexico_taxes_avoided_{gen}"]
                            private.append(dict(key, generation=gen, all_taxes_private_bn=gain,
                                with_services_bn=gain+c[f"us_budget_value_{gen}"]-pc[gen]["us_taxes_bn"]
                                +c[f"uncompensated_received_{gen}"]+c[f"mexico_budget_lost_{gen}"],
                                pension_basis="matched_cash", private_price_twin="consumption" if twin else "same reading"))
                        cells.append(cv.assign(**key))
                    print(f"CASH_READING {reading} s={share:g} {bound} {end}", flush=True)
    out = pd.DataFrame(records)
    W.gate("cash_reading_cross_product", len(out) == 3*4*2*2*len(WEIGHTS))
    out.to_csv(V.DERIVED/f"readings_cash_{case}.csv", index=False, lineterminator="\n", float_format="%.12f")
    pd.concat(details, ignore_index=True).to_csv(V.DERIVED/f"reading_rows_cash_{case}.csv", index=False, lineterminator="\n", float_format="%.12f")
    pd.DataFrame(private).to_csv(V.DERIVED/f"private_gains_cash_{case}.csv", index=False, lineterminator="\n", float_format="%.12f")
    # 562,428 rows for oct16 (259.5 MB as text): v9 coverage components cross every recipient line. gzip keeps it pushable.
    write_csv_gz(pd.concat(cells, ignore_index=True), V.DERIVED/f"reading_cells_cash_{case}.csv.gz", float_format="%.12f")
    pd.DataFrame(comparisons).to_csv(V.DERIVED/f"residual_convention_cash_{case}.csv", index=False, lineterminator="\n", float_format="%.12f")
    status = pd.DataFrame([dict(case=case, reading="full_accrual", status="[BLOCKED]", reason="Mexico contribution histories and public service-cost bridge unavailable", value_bn=np.nan),
        dict(case=case, reading="debt_split_beside", status=f"[BLOCKED: no {case} federal split]", reason="theta/MCPF/capital/R&D excluded from all reading totals", value_bn=np.nan)])
    status.to_csv(V.DERIVED/f"readings_status_{case}.csv", index=False, lineterminator="\n")
    sys.path.insert(0, str(HERE.parent/"scripts"))
    from memory_budget import require_within_budget
    peak = require_within_budget("matched-cash readings")
    print(f"CASH_MEMORY physical_peak_bytes={peak}", flush=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--case", default="oct16")
    parser.add_argument("--prepare", action="store_true")
    args = parser.parse_args()
    prepare(args.case) if args.prepare else run(args.case)


if __name__ == "__main__":
    main()
