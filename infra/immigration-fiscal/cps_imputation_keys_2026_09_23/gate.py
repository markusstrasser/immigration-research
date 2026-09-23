"""Gate: reproduce the complete account's CPS keys and the union's published totals.

Nothing is perturbed here. Every later step starts from vectors this script has
matched to the producers' exports (keys to a relative 1e-9, totals to 1e-6 bn).
Run: OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/cps_imputation_keys_2026_09_23/gate.py
"""
from __future__ import annotations

import json

import numpy as np
import pandas as pd

import common as c

CAPITAL_CATEGORIES = {"corporate_capital", "corporate_labor", "modeled_owner_property",
                      "remaining_production_property", "personal_property_tax"}


def account_tables():
    receipts = pd.read_csv(c.FISCAL / "full_account_receipts_2026_09_20/derived/category_allocations.csv")
    receipts = receipts.query("scenario_id == 'cbo_collective'").copy()
    receipts["direct"] = receipts.response_class.isin(["personal_income", "household_direct"]) & \
        ~receipts.category.isin(CAPITAL_CATEGORIES)
    spending = pd.read_csv(c.FISCAL / "full_account_spending_2026_09_20/derived/allocations.csv")
    spending = spending.query("scenario_id == 'complete_preferred_F_per_capita'").copy()
    return receipts, spending


def receipt_target(receipts, rshares, replicate=0):
    """Target receipts by category from key shares; non-CPS rows keep their published amounts."""
    out = []
    for r in receipts.itertuples():
        keyset = rshares[r.allocation]
        if r.allocation_key in keyset:
            value = r.national_bn * keyset[r.allocation_key][replicate]
        else:
            value = r.target_bn  # owner-property override, resident population, foreign, rounding
        out.append(value)
    return np.asarray(out)


def spending_target(spending, sshares, hf, replicate=0):
    out = []
    for r in spending.itertuples():
        keyset = sshares[r.allocation]
        if r.allocation_key in keyset:  # preferred F-per-capita scenario: every row is average cost
            value = r.national_bn * hf[replicate] * keyset[r.allocation_key][replicate]
        else:
            value = r.target_bn  # MEPS, education and external keys are not CPS income items
        out.append(value)
    return np.asarray(out)


def main():
    d = c.load_frame()
    civ, target = c.masks(d)
    index = c.spm_index(d)
    W = d[c.REPS].to_numpy(float)
    if abs(W[target, 0].sum() - c.TARGET_POP) > .01:
        raise ValueError("Target population drift")
    hf = W[civ].sum(axis=0) / c.RESIDENT
    print("[gate] receipt and spending keys under 161 weights", flush=True)
    rkeys = c.receipt_keys(d, index)
    rshares = {a: c.shares(v, W, civ, target) for a, v in rkeys.items()}
    skeys = c.spending_vectors(d, index)
    sshares = {a: c.shares(v, W, civ, target) for a, v in skeys.items()}

    rows = []
    pub_r = pd.read_csv(c.FISCAL / "full_account_receipts_2026_09_20/derived/allocation_keys.csv")
    for r in pub_r.itertuples():
        if r.allocation_key == "resident_population":
            continue
        rep = rshares[r.allocation][r.allocation_key]
        rows.append(dict(lane="receipts", allocation=r.allocation, key=r.allocation_key, share_rebuilt=rep[0],
                         share_published=r.target_key_share, se_rebuilt=c.sdr(rep),
                         se_published=r.target_share_sampling_se))
    pub_s = pd.read_csv(c.FISCAL / "full_account_spending_2026_09_20/derived/incidence_keys.csv")
    for r in pub_s.itertuples():
        if r.key in sshares[r.allocation]:
            rep = sshares[r.allocation][r.key]
            rows.append(dict(lane="spending", allocation=r.allocation, key=r.key, share_rebuilt=rep[0],
                             share_published=r.target_share, se_rebuilt=c.sdr(rep), se_published=np.nan))
    keys = pd.DataFrame(rows)
    keys["rel_diff"] = (keys.share_rebuilt / keys.share_published - 1).abs()
    keys.to_csv(c.OUT / "gate_keys.csv", index=False)
    if not (keys.rel_diff < 1e-9).all():
        raise SystemExit(f"[BLOCKED] key shares not reproduced:\n{keys.loc[keys.rel_diff >= 1e-9]}")
    se = keys.dropna(subset=["se_published"])
    if not np.allclose(se.se_rebuilt, se.se_published, rtol=1e-6, atol=0):
        raise SystemExit("[BLOCKED] receipt key SEs not reproduced")
    print(f"[gate] {len(keys)} keys reproduced (max relative difference {keys.rel_diff.max():.1e})", flush=True)

    receipts, spending = account_tables()
    receipts["rebuilt_bn"] = receipt_target(receipts, rshares)
    spending["rebuilt_bn"] = spending_target(spending, sshares, hf)
    published = pd.read_csv(c.FISCAL / "full_account_receipts_2026_09_20/derived/scenario_totals.csv")
    pub_sp = pd.read_csv(c.FISCAL / "full_account_spending_2026_09_20/derived/scenario_totals.csv")
    totals = []
    for allocation in ["personal", "shared"]:
        rr = receipts.query("allocation == @allocation")
        ss = spending.query("allocation == @allocation")
        want = published.query("scenario_id == 'cbo_collective' and allocation == @allocation").target_bn.iloc[0]
        want_s = pub_sp.query("scenario_id == 'complete_preferred_F_per_capita' and allocation == @allocation").target_bn.iloc[0]
        for label, got, expect in [
                ("receipts_all_cbo_collective", rr.rebuilt_bn.sum(), want),
                ("receipts_direct_response_1", rr.loc[rr.direct, "rebuilt_bn"].sum(), rr.loc[rr.direct, "target_bn"].sum()),
                ("spending_all_preferred", ss.rebuilt_bn.sum(), want_s),
                ("spending_household_transfers", ss.loc[ss.response_class.eq("household_transfer"), "rebuilt_bn"].sum(),
                 ss.loc[ss.response_class.eq("household_transfer"), "target_bn"].sum())]:
            totals.append(dict(allocation=allocation, total=label, rebuilt_bn=got, published_bn=expect,
                               diff_bn=got - expect))
    totals = pd.DataFrame(totals)
    totals.to_csv(c.OUT / "gate_totals.csv", index=False)
    print(totals.to_string(index=False), flush=True)
    if not (totals.diff_bn.abs() < 1e-6).all():
        raise SystemExit("[BLOCKED] published union totals not reproduced")
    # Line-level check against the explorer model that the main case evaluates.
    model = json.loads((c.FISCAL / "assumption_explorer_2026_09_21/derived/model.json").read_text())
    worst = 0.
    for line in model["receipts"]["lines"]:
        for allocation in ["personal", "shared"]:
            cell = line["cells"]["cbo_collective"][allocation]
            mine = receipts.query("allocation == @allocation and category == @line['id']").rebuilt_bn.iloc[0]
            worst = max(worst, abs(cell["target_bn"] - mine))
    for line in model["spending"]["lines"]:
        for allocation in ["personal", "shared"]:
            cell = line["keys"][line["preferred_key"]][allocation]
            mine = spending.query("allocation == @allocation and category == @line['id']").rebuilt_bn.iloc[0]
            worst = max(worst, abs(cell["target_bn"] - mine))
    print(f"[gate] explorer model lines reproduced, max difference {worst:.2e} bn", flush=True)
    if worst > 1e-6:
        raise SystemExit("[BLOCKED] explorer model lines differ from the rebuilt account")
    print("[gate] all gates passed", flush=True)


if __name__ == "__main__":
    main()
