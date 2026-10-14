"""Assemble candidate increments from own-record prices and exact added-person age prices.

The observed candidate and all-age extrapolation are separate arms. The latter
does not add the observed children a second time. Replicate sums retain the
covariance of counts, price-key estimation and household credit changes.
"""
from __future__ import annotations

import csv
import json
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
OUT = HERE / "derived"


def read(name):
    return json.loads((OUT/name).read_text())


def stat(x):
    x = np.asarray(x)
    return dict(estimate=float(x[0]), se=float(np.sqrt(4/160*np.square(x[1:]-x[0]).sum())))


def main():
    kernel, counts, credits, added = (read(n) for n in ("summary.json","count_replicates.json",
                                                       "credits_interaction.json","added_band_prices.json"))
    assert all(g["passed"] for g in read("gates.json"))
    assert all(g["pass"] for g in added["gates"])
    nG, nL = np.array(counts["observed_g3_rate_by_age"]), np.array(counts["observed_later_by_age"])
    nr = {k:np.array(counts[f"reporter_{k}_by_age"]) for k in ("central","all")}
    ratio = np.array(counts["loss_ratio"])
    assert (nG.sum(axis=0)+nL.sum(axis=0)>0).all()
    third_share = nG.sum(axis=0)/(nG.sum(axis=0)+nL.sum(axis=0))
    projected = nr["central"]*ratio[None,:]
    case = json.loads((HERE.parent / "main_case_2026_10_14/derived/corrections.json").read_text())
    baseline_counts = case["meta"]["lineage"]["counts"]
    cf = added["meta"]["c3"]
    out = dict(status="candidate, not adopted", headline="income-year 2024 net annual cost to other residents",
               allocation="personal", specifications=[16,11], fixed="current v7 responses, national totals, original 3.04M and C3",
               counts=dict(baseline=baseline_counts,
                           reporting_additions={k:stat(v.sum(axis=0)) for k,v in nr.items()},
                           observed_nonreporters=stat((nG+nL).sum(axis=0)),
                           extrapolated_nonreporters=stat(projected.sum(axis=0))),
               measured_child_rule="biological, native, under18, linked US-born Mexican-origin parent and third-country-born parent; own parent-birthplace fields agree",
               extrapolation="child loss-to-identifier ratio transferred to all-age one-US-parent reporters; reporting age mix and observed loss ancestry-class share held as their proxies",
               approximations=added["meta"]["approximations"], results={})
    rows = []
    for basis in ("set","cash"):
        out["results"][basis] = {}
        for ei,end in enumerate(("low","high")):
            g = np.array([r["g3_bn_per_person"][basis][ei] for r in added["rates"]])
            g0 = np.array([r["g3_without_child_credits_bn_per_person"][basis][ei] for r in added["rates"]])
            w = np.array([r["white_bn_per_person"][basis][ei] for r in added["rates"]])
            # Source case: Mexico-born grandparent -> (1-C3)G3 + C3W;
            # later native Mexican-origin ancestry -> G3.
            measured = (nG*((1-cf)*g0+cf*w)[:,None]+nL*g0[:,None]).sum(axis=0)
            inferred = (projected*(third_share[None,:]*((1-cf)*g+cf*w)[:,None]
                                   +(1-third_share[None,:])*g[:,None])).sum(axis=0)
            raw = np.array([r["white_raw_bn_per_person"][basis][ei] for r in added["rates"]])
            white_difference = (nG*cf*(w-raw)[:,None]).sum(axis=0)
            entry = dict(observed_loss_net_before_exact_credit_bn=stat(measured),
                         inferred_loss_net_with_case_credit_bn=stat(inferred),
                         white_product_calibration_on_observed_bn=stat(white_difference), arms={})
            base = kernel["pricing"][basis][end]["engine_bn"]
            for arm in ("central","all"):
                own = np.array(kernel["pricing"][basis][end]["replicates"][arm])
                key = "one_us_parent" if arm=="central" else "all_outsiders"
                cr = np.array(credits["results"][key]["replicate_delta_bn"])
                cr_obs = np.array(credits["results"][key+"_plus_observed"]["replicate_delta_bn"])
                for scope,vector,loss_n,credit in (
                    ("reporting_only",own+cr,np.zeros(161),cr),
                    ("observed_completion",own+measured+cr_obs,(nG+nL).sum(axis=0),cr_obs),
                    ("all_age_extrapolation",own+inferred+cr,projected.sum(axis=0),cr)):
                    name = arm+"_"+scope
                    assert np.isfinite(vector).all()
                    n_ident = baseline_counts["account_union"]+nr[arm].sum(axis=0)
                    n_lineage = baseline_counts["lineage_population"]+nr[arm].sum(axis=0)+loss_n
                    summary = dict(delta_bn=stat(vector), candidate_bn=base+float(vector[0]),
                                   own_reporting_price_bn=stat(own), credit_interaction_bn=stat(credit),
                                   identified_union_people=stat(n_ident), lineage_people=stat(n_lineage),
                                   additional_nonreporters=stat(loss_n), passes_5bn_bar=bool(abs(vector[0])>=5),
                                   replicate_delta_bn=vector.tolist())
                    entry["arms"][name] = summary
                    rows.append(dict(basis=basis,end=end,arm=name,delta_bn=vector[0],se_bn=summary["delta_bn"]["se"],
                                     candidate_bn=summary["candidate_bn"],identified_union_people=n_ident[0],
                                     lineage_people=n_lineage[0],passes_5bn_bar=summary["passes_5bn_bar"]))
            out["results"][basis][end] = entry
    (OUT / "candidate.json").write_text(json.dumps(out,indent=2)+"\n")
    with (OUT / "candidate.csv").open("w",newline="") as f:
        writer = csv.DictWriter(f,fieldnames=list(rows[0]),lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    print("PASS: 24 candidate rows; no observed/extrapolated-loss addition; joint replicate SEs")


if __name__ == "__main__":
    main()
