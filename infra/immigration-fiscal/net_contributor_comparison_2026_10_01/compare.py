"""Annual household fiscal distributions on the September 29 accrual case.

Extend the existing rough white comparator to households, conserving every line
and capital component. Reuse the Mexican-origin central household release intact.
Positive output means a contribution to other residents (opposite to engine cost).
Run: OPENBLAS_NUM_THREADS=1 uv run --no-project python3 {lane}/compare.py
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
FISCAL = HERE.parent
WHITE = FISCAL / "white_replacement_2026_09_28"
MEX = FISCAL / "within_group_distribution_2026_09_29"
sys.dont_write_bytecode = True
sys.path.insert(0, str(WHITE))
import rekey_sept29 as W  # noqa: E402

R = W.R
ENDS = ("low", "high")


def require(ok, message):
    if not ok:
        raise ValueError(f"[BLOCKED] {message}")


def normalized(v, weights):
    v = np.asarray(v, float)
    require(np.isfinite(v).all() and (v >= 0).all(), "invalid allocation vector")
    den = float(v @ weights)
    require(den > 0, "nonzero fiscal line has an empty allocation key")
    return v / den


def weighted_quantile(x, weights, q):
    order = np.argsort(x, kind="stable")
    return np.interp(q, np.cumsum(weights[order]) / weights.sum(), x[order])


def household_table(ids, member_mask, person_cost, weights):
    """Pool only the selected group's members, as the Mexican household lane does."""
    z = pd.DataFrame({"household": np.asarray(ids)[member_mask],
                      "cost": person_cost[member_mask], "w": weights[member_mask]})
    h = z.groupby("household", sort=True).agg(
        members=("cost", "size"), cost=("cost", "sum"), resident_weight=("w", "sum"))
    h["household_weight"] = h.resident_weight / h.members
    h["net_per_member"] = -h.cost / h.members
    return h.reset_index()


def person_inputs():
    with zipfile.ZipFile(R.ZIP) as archive:
        ids = pd.read_csv(archive.open("pppub25.csv"), usecols=["PH_SEQ", "A_LINENO"])
    require(len(ids) == len(R.d) and np.array_equal(ids.PH_SEQ, R.d.PH_SEQ),
            "raw CPS ordering differs from the comparator")
    pa = pd.read_parquet(MEX / "_cache/sept29/person_accrual.parquet")
    p = ids.merge(pa, on=["PH_SEQ", "A_LINENO"], how="left", validate="one_to_one")
    white = R.MASK["w3"] & (R.w > 0)
    require(p.loc[white, "oasdi_gross"].notna().all(), "white pension records missing")
    require(not p.loc[white, "unauth"].astype(bool).any(), "native white mask has unauthorized records")
    require(not p.loc[white, ["union", "mexico_born"]].astype(bool).any().any()
            and p.loc[white, "onbooks"].eq(1).all(), "Part A common-scalar domain changed")
    require(np.array_equal(p.loc[white, "part_a"].gt(0),
                           p.loc[white, "tax_hi"].gt(0) & p.loc[white, "age"].lt(65)),
            "Part A covered-worker domain changed")
    q = p.loc[white]
    ratio = (q.w * q.oasdi_gross).sum() / (q.w * q.tax_oasdi).sum()
    timing = (q.w * q.oasdi_gross * q.tob).sum() / (q.w * q.oasdi_gross).sum()
    require(abs(ratio - W.ACC["white"]["gross"]) <= 0.5001e-6
            and abs(timing - W.ACC["white"]["timing"]) <= 0.5001e-6,
            "cached white pension shape fails the own-white accrual ratio/timing check")
    # Nonmembers' cached net uses the union tax rate; replace it with the white rate.
    ss = p.oasdi_gross.fillna(0).to_numpy() * (1 - W.ACC["white"]["rel"] * p.tob.fillna(0).to_numpy())
    # All native whites start at 21. The cached pooled P(qualify)/covered-years
    # factor is one common scalar and cancels on normalization to the white total.
    hi = p.part_a.fillna(0).to_numpy()
    return white, ss, hi


def white_keys(sc, end, ss, hi):
    cw = sc["cps_w"]
    shared = end == "low"

    def allocated(v):
        return R.split(v, ["PH_SEQ", "SPM_ID"]) if shared else np.asarray(v)

    # Follow main-case sharing for direct person amounts. Already household/unit
    # keys (income tax, consumption, housing, property) retain their own rule.
    direct = {"oasdi", "hi", "workers", "ss", "ssi", "uc", "vet", "wc", "paw", "k12", "college", "edben"}
    keys = {k: normalized(allocated(v) if k in direct else v, cw) for k, v in R.K.items()}
    keys["pension"] = normalized(allocated(ss), cw)
    keys["part_a"] = normalized(allocated(hi), cw)
    keys["old"] = normalized(R.old_c, cw)
    keys["crime"] = normalized(R.crime_c, cw)
    keys["miles"] = normalized((W.AGE >= 5).astype(float), cw)
    # White MEPS means by five-year age; US-born white donor mask is the existing
    # comparator's proxy for third-plus whites. These are imputed cell means.
    mm = R.MMASK["w3"] & (R.mw > 0)
    for col in R.MEPS_COLS:
        z = pd.DataFrame({"band": R.mage[mm], "w": R.mw[mm], "x": R.md[col].to_numpy()[mm]})
        means = z.assign(wx=z.w * z.x).groupby("band").wx.sum() / z.groupby("band").w.sum()
        v = means.reindex(R.cage).to_numpy()
        require(np.isfinite(v[cw > 0]).all(), f"missing white MEPS age cell: {col}")
        keys[col] = normalized(np.nan_to_num(v), cw)

    def mix(parts):
        total = sum(amount for amount, _ in parts)
        require(total > 0, "empty composite key")
        return sum(amount * keys[key] for amount, key in parts) / total

    sg, ex = sc["share"], sc["keys"]
    keys["education"] = mix([(R.K12_PART * sg["k12"], "k12"),
                             ((1 - R.K12_PART) * sg["college"], "college")])
    keys["refund"] = mix([(R.REF_EITC_PART * sg["ref"], "ref"),
                          ((1 - R.REF_EITC_PART) * sg["pc"] * R.pc_scale, "pc")])
    keys["medicaid"] = mix([(R.LTSS_PART * ex["ltss"], "old"),
                            ((1 - R.LTSS_PART) * ex["meps_medicaid"], "TOTMCD24")])
    ph, arrest, custody = sg["pc"] * R.pc_scale, ex["arrests"], ex["custody"]
    cj = R.cj.national_bn
    head = ph * (cj["fire"] + .4 * cj["law_courts"] + cj["police_cbp"]
                 + cj["police_ice_border"] + cj["police_ice_interior"] + .5 * cj["police_non_border"])
    use = custody * cj["prisons"] + arrest * (.6 * cj["law_courts"] + .5 * cj["police_non_border"])
    keys["justice"] = mix([(head, "pc"), (use, "crime")])
    require(abs((head + use) / cj.sum() - sc["external"]["public_order_safety"]) < 1e-12,
            "white justice pieces disagree with its comparator")
    return keys


def allocate_white(sc, end, ss, hi):
    result, rows, _, terms, acc = W.run29(sc, end, "accrual")
    cw, keys = sc["cps_w"], white_keys(sc, end, ss, hi)
    costs, audit = [], []
    med = {"health_services": "OTHPUB", "veterans_other": "TOTVA24", "military_medical": "TOTTRI24",
           "medicaid_and_chip_other_medical": "medicaid", "public_order_safety": "justice",
           "education_services": "education", "refundable_tax_credits": "refund"}

    def add(part, bn, key):
        if abs(bn) < 1e-15:
            return
        require(key in keys, f"unknown person key {key} for {part}")
        v = bn * 1e9 * keys[key]
        got = float(v @ cw) / 1e9
        require(abs(got - bn) < 1e-9, f"piece does not conserve: {part}")
        costs.append(v)
        audit.append(dict(end=end, part=part, key=key, cost_bn=bn, reconstructed_bn=got))

    for side, lid, national, amount, response in rows:
        target = amount * response * (-1 if side == "receipts" else 1)
        before = len(audit)
        if abs(target) < 1e-15:
            continue
        if lid == "federal_income_tax":
            removed = W.receipt_per_rel_benefit(end) * W.ACC["white"]["rel"] * acc["ss_cash"]
            add(lid + "_before_benefit_tax", -(amount + removed) * response, "fit")
            add(lid + "_remove_benefit_tax", removed * response, "ss")
        elif lid == "social_security":
            add(lid, target, "pension")
        elif lid == "medicare":
            add(lid + "_cash_BD", (1 - W.PART_A_SHARE) * acc["medicare_cash"] * response, "TOTMCR24")
            add(lid + "_Part_A_accrual", W.ACC["white"]["part_a"] * acc["hi_tax"] * response, "part_a")
        elif lid in ("roads_vmt_sl", "roads_vmt_fed"):
            base = W.HWY_N[lid.rsplit("_", 1)[1]] * response
            add(lid + "_passenger", base * W.FP * terms["s_vmt"], "miles")
            add(lid + "_freight", base * (1 - W.FP) * terms["k_cons"], "cons")
            add(lid + "_remove_old", -base * terms["k_old"], "hi")
        elif lid == "excise_selective_sales":
            add(lid + "_base", -(amount - terms["gasoline_shift"]) * response, "cons")
            add(lid + "_gasoline_miles", -W.GAS * terms["s_vmt"] * response, "miles")
            add(lid + "_remove_gasoline_old", W.GAS * terms["k_cons"] * response, "cons")
        elif lid == "personal_motor_vehicle":
            add(lid, target, "miles")
        elif lid in W.SP_LINES:
            add(lid, target, med.get(W.SP_LINES[lid]["parent"], R.SPEND_KEY.get(W.SP_LINES[lid]["parent"])))
        elif side == "receipts":
            add(lid, target, W.NEW_RECEIPTS.get(lid, R.RECEIPT_KEY.get(lid)))
        else:
            add(lid, target, med.get(lid, R.SPEND_KEY.get(lid)))
        require(abs(sum(r["cost_bn"] for r in audit[before:]) - target) < 1e-9,
                f"line pieces do not add to comparator: {side}/{lid}")

    e, sg = W.DUMP["accrual"][end], sc["share"]
    ph = sg["pc"] * R.pc_scale
    for c in e["capital"]:
        cid = c["id"]
        base = c["stock_charged_bn"] * c["response"] * e["rate"]
        prefix = cid.split("_")[0]
        if prefix == "pos":
            add("capital_" + cid, base * sc["external"]["public_order_safety"], "justice")
        elif prefix == "health":
            add("capital_" + cid, base * sc["external"]["health_services"], "OTHPUB")
        elif cid in ("hwy_sl", "hwy_fed"):
            add("capital_" + cid + "_passenger", base * W.FP * terms["s_vmt"], "miles")
            add("capital_" + cid + "_freight", base * (1 - W.FP) * terms["k_cons"], "cons")
        elif cid == "ent_housing_sl":
            add("capital_" + cid, base * sg["house"], "house")
        else:
            key = {"k12": "k12", "college": "college", "air": "hi"}.get(prefix, "pc")
            add("capital_" + cid, base * (ph if key == "pc" else sg[key]), key)
    person = np.sum(costs, axis=0)
    got = float(person @ cw) / 1e9
    require(abs(got - result["cost"]) < 1e-8, "white person allocations do not reproduce aggregate cost")
    oracle = pd.read_csv(WHITE / "derived/rekey_summary_sept29.csv")
    want = oracle.query("basis == 'accrual' and group == 'A1_third_plus_nh_white' and end == @end").cost.iloc[0]
    require(abs(got - want) < 5.01e-5, "live white aggregate differs from published comparator")
    return person, audit, result


def summarize(h, group, end, mean_account):
    x, w = h.net_per_member.to_numpy(), h.resident_weight.to_numpy()
    wh = h.household_weight.to_numpy()
    quant = weighted_quantile(x, w, [.1, .25, .5, .75, .9])
    return dict(group=group, end=end, resident_weight=float(w.sum()), sampled_households=len(h),
                share_residents_positive=float(w[x > 0].sum() / w.sum()),
                share_households_positive=float(wh[x > 0].sum() / wh.sum()),
                mean_account_net_per_member=mean_account,
                mean_household_net_per_member=float(np.average(x, weights=w)),
                **dict(zip(["p10", "p25", "median", "p75", "p90"], quant)))


def main(out):
    W.setup()
    sc = W.scenarios()["A1_third_plus_nh_white"]
    member_mask, ss, hi = person_inputs()
    summaries, audits, all_h = [], [], []
    mex_h = pd.read_parquet(MEX / "_cache/sept29/households_person_onbooks.parquet")
    mex_ref = pd.read_csv(MEX / "derived/sept29/net_positive_shares_person_onbooks.csv")
    for end in ENDS:
        cost, audit, result = allocate_white(sc, end, ss, hi)
        h = household_table(R.d.PH_SEQ, member_mask, cost, R.w)
        h["group"], h["end"] = "white", end
        summaries.append(summarize(h, "white", end, -result["cost"] * 1e9 / sc["population"]))
        audits.extend(audit)
        all_h.append(h)
        h = pd.DataFrame({"household": mex_h.PH_SEQ, "members": mex_h.union_members,
                          "cost": mex_h[f"A_{end}_household_cost_usd"],
                          "resident_weight": mex_h.weight * mex_h.union_members,
                          "household_weight": mex_h.weight,
                          "net_per_member": -mex_h[f"A_{end}_per_member_usd"],
                          "group": "mexican", "end": end})
        ref = mex_ref.query("convention == 'A' and breakdown == 'all' and end == @end").iloc[0]
        s = summarize(h, "mexican", end, -ref.net_cost_per_member_usd)
        # The established release rounds every float to six decimal places.
        require(abs(s["share_residents_positive"] - ref.share_members_net_positive) <= 0.5001e-6,
                "Mexican share does not reproduce current central")
        require(abs(s["resident_weight"] - 39_712_493.33118789) < 1, "Mexican population changed")
        summaries.append(s)
        all_h.append(h)
    households = pd.concat(all_h, ignore_index=True)
    out.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(summaries).to_csv(out / "shares.csv", index=False, lineterminator="\n")
    pd.DataFrame(audits).to_csv(out / "white_allocation.csv", index=False, lineterminator="\n")
    cache = HERE / "_cache"
    cache.mkdir(exist_ok=True)
    households.to_parquet(cache / "households.parquet", index=False)
    sources = [WHITE / "derived/rekey_summary_sept29.csv", WHITE / "derived/engine_lines_sept29.json",
               WHITE / "derived/engine_lines_sept29_cash.json", MEX / "_cache/sept29/person_accrual.parquet",
               MEX / "_cache/sept29/households_person_onbooks.parquet", R.ZIP,
               R.MEPS, R.MEPS.with_name("h256su.txt"), R.TAF, R.ARRESTS,
               WHITE / "derived/accrual_ratios.csv", WHITE / "derived/v4_state_relatives.csv",
               WHITE / "derived/v4_nhts_vmt.csv", W.CASE_LANE / "derived/corrections.json",
               FISCAL / "cj_use_allocation_2026_09_23/derived/central_split.csv",
               Path(__file__), WHITE / "rekey_white.py", WHITE / "rekey_sept29.py",
               WHITE / "state_white.py", WHITE / "v4_inputs.py"]
    manifest = {str(p.relative_to(FISCAL.parent.parent)): hashlib.sha256(p.read_bytes()).hexdigest() for p in sources}
    (out / "audit.json").write_text(json.dumps(dict(source_hashes=manifest, gates="PASS",
        basis="income-year 2024, September 29 accrual case, full allocation, actual ages",
        white="US-born non-Hispanic white with US-born parents; rough comparator",
        mexican="Mexican-origin union, all generations; person accrual plus on-books payroll",
        unit="resident-weighted household balance per group member; positive means net contribution",
        interval="two main-case specifications, not a confidence interval"), indent=2) + "\n")
    print(pd.DataFrame(summaries).to_string(index=False))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out-dir", type=Path, default=HERE / "derived")
    main(parser.parse_args().out_dir)
