"""Price Census's measured 2025 CPS ASEC nonresponse bias on the account's own CPS keys.

Census (Bee & Rothbaum, Research Matters 2025-09-09) corrects nonresponse with alternative weights built from
linked administrative records, and publishes the ratio of survey to nonresponse-adjusted household income at
P10..P95 by householder group. This lane imposes those ratios as a reweight of the ASEC 2025 households: inside
each householder group the weights are moved so that the weighted HTOTVAL quantiles become Q(p) / r(p). Person
weights inherit their household's factor. Then every CPS key the receipt and spending accounts use is recomputed
and its group share compared with the published-weight share.

Inputs: `derived/curves_by_eye.csv` (read by eye from figures 3-6; see RESULT.md), the account's CPS archive (pinned
by the spending builder's CPS_SHA), the account's line amounts (receipts `cbo_collective`, spending
`complete_preferred_F_per_capita`, personal allocation).

Arms:
  curve  : raw by-eye points | smooth (a straight line in p fitted to each group's points)
  count  : free (the group's person total moves with the reweight) | pinned (the group's total is held, as the
           account's row-4 frame holds it; ladder 209)
Groups: Hispanic householder -> Hispanic curve; non-Hispanic Black alone -> Black; non-Hispanic white alone ->
NH white; everyone else -> the all-household curve. Positive control: the reweighted all-household quantile
ratios must reproduce the all-household curve (figure 3) to within the reading error.
"""
from __future__ import annotations

import csv
import importlib.util
import json
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
FISCAL = HERE.parent
ARCHIVE = FISCAL/"gen_ledger_extension_2026_09_16/_cache/asecpub25csv.zip"
RECEIPTS = FISCAL/"full_account_receipts_2026_09_20/derived/category_allocations.csv"
SPENDING = FISCAL/"full_account_spending_2026_09_20/derived/allocations.csv"
OUT = HERE/"derived"
CURVE_COLS = {"hispanic": "hispanic", "black": "black", "nh_white": "nh_white", "other": "all"}
TOP_CODE = 168600  # 2024 OASDI wage base, as in the receipts builder


def load_spending_builder():
    spec = importlib.util.spec_from_file_location("spending_builder", FISCAL/"full_account_spending_2026_09_20/builder.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def read_cps(sb):
    if sb.sha(ARCHIVE) != sb.CPS_SHA:
        raise ValueError("[BLOCKED] CPS source changed")
    fields = ["PH_SEQ", "PPPOS", "A_AGE", "PRPERTYP", "PRCITSHP", "PENATVTY", "PEFNTVTY", "PEMNTVTY", "PRDTHSP",
              "PERRP", "PEHSPNON", "PRDTRACE", "SPM_ID", "SS_VAL", "SSI_VAL", "PAW_VAL", "UC_VAL", "VET_VAL",
              "WC_VAL", "WSAL_VAL", "SEMP_VAL", "FRSE_VAL", "INT_VAL", "DIV_VAL", "RNT_VAL", "FEDTAX_BC",
              "STATETAX_A", "AGI", "FICA", "MCARE", "MCAID", "EIT_CRED", "ACTC_CRD", "SPM_SNAPSUB", "SPM_WICVAL",
              "SPM_CAPHOUSESUB", "SPM_ENGVAL", "SPM_RESOURCES"]
    with zipfile.ZipFile(ARCHIVE) as z:
        d = pd.read_csv(z.open("pppub25.csv"), usecols=fields)
        w = pd.read_csv(z.open("asec_csv_repwgt_2025.csv"), usecols=["h_seq", "PPPOS", "pwwgt0"]).rename(columns={"h_seq": "PH_SEQ"})
        h = pd.read_csv(z.open("hhpub25.csv"), usecols=["H_SEQ", "HSUP_WGT", "HTOTVAL", "HRECORD"])
    d = d.merge(w, on=["PH_SEQ", "PPPOS"], validate="one_to_one", how="left")
    if d.isna().any().any():
        raise ValueError("Missing CPS keys")
    return d, h


def householder_groups(d, h):
    ref = d[d.PERRP.isin([40, 41])].drop_duplicates("PH_SEQ")
    hisp = ref.PEHSPNON.eq(1)
    grp = np.where(hisp, "hispanic", np.where(ref.PRDTRACE.eq(2), "black", np.where(ref.PRDTRACE.eq(1), "nh_white", "other")))
    g = pd.Series(grp, index=ref.PH_SEQ.to_numpy())
    h = h[h.HSUP_WGT > 0].copy()
    h["group"] = g.reindex(h.H_SEQ).to_numpy()
    if h.group.isna().mean() > 0.001:
        raise ValueError("Households without a reference person")
    return h.dropna(subset=["group"])


def wquantile(y, w, p):
    order = np.argsort(y, kind="stable")
    y, w = y[order], w[order]
    c = (np.cumsum(w) - 0.5*w)/w.sum()
    return np.interp(p, c, y)


def wcdf(y, w, edges):
    order = np.argsort(y, kind="stable")
    ys, cw = y[order], np.cumsum(w[order])/w.sum()
    idx = np.searchsorted(ys, edges, side="right")
    return np.where(idx > 0, cw[np.maximum(idx - 1, 0)], 0.0)


def ratio_fn(points, p):
    """r(p) by linear interpolation, flat beyond P10 and P95."""
    return np.interp(p, points[:, 0], points[:, 1])


def household_factors(y, w, points):
    """Weight factors that move the weighted quantiles of y from Q(p) to Q(p)/r(p)."""
    grid = np.linspace(0.001, 0.999, 999)
    q = wquantile(y, w, grid)
    q_adj = np.maximum.accumulate(q/ratio_fn(points, grid))
    edges = np.unique(wquantile(y, w, np.linspace(0.02, 0.98, 49)))
    f_old = np.concatenate([[0.0], wcdf(y, w, edges), [1.0]])
    f_new = np.concatenate([[0.0], np.interp(edges, q_adj, grid, left=0.0, right=1.0), [1.0]])
    f_new[-2] = min(f_new[-2], 1.0)
    bins = np.searchsorted(edges, y, side="left")  # bin k holds (edges[k-1], edges[k]]
    mass_old, mass_new = np.diff(f_old), np.diff(f_new)
    if np.any(mass_old[np.unique(bins)] <= 0):
        raise ValueError("Empty occupied bin")
    factor = np.where(mass_old > 0, mass_new/np.where(mass_old > 0, mass_old, 1), 0.0)
    return factor[bins]


def smooth(points):
    b, a = np.polyfit(points[:, 0], points[:, 1], 1)
    return np.column_stack([points[:, 0], a + b*points[:, 0]])


def key_vectors(d, sb):
    size = d.groupby("SPM_ID").SPM_ID.transform("size").to_numpy(float)
    wage = d.WSAL_VAL.clip(lower=0).to_numpy(float)
    se = .9235*np.maximum(d.SEMP_VAL.to_numpy(float) + d.FRSE_VAL.to_numpy(float), 0)
    se = np.where(se >= 400, se, 0)
    se_capped = np.minimum(se, np.maximum(TOP_CODE - np.minimum(wage, TOP_CODE), 0))
    unit = lambda f: d[f].to_numpy(float)/size
    return {
        # receipt keys (full_account_receipts builder.py:88-99)
        "federal_liability": d.FEDTAX_BC.to_numpy(float),
        "state_liability": d.STATETAX_A.clip(lower=0).to_numpy(float),
        "wage": wage, "wage_oasdi": np.minimum(wage, TOP_CODE), "self_payroll": .124*se_capped + .029*se,
        "positive_fica_worker": d.FICA.gt(0).to_numpy(float),
        "capital": (d.INT_VAL + d.DIV_VAL + d.RNT_VAL).clip(lower=0).to_numpy(float),
        "consumption": d.SPM_RESOURCES.clip(lower=0).to_numpy(float)/size,
        "medicare": d.MCARE.eq(1).to_numpy(float),
        "adults": d.A_AGE.ge(18).to_numpy(float), "population": np.ones(len(d)),
        # spending keys (full_account_spending builder.py:203-216)
        "social_security": d.SS_VAL.to_numpy(float), "ssi": d.SSI_VAL.to_numpy(float),
        "cash_assistance": d.PAW_VAL.to_numpy(float), "unemployment": d.UC_VAL.to_numpy(float),
        "veterans": d.VET_VAL.to_numpy(float), "workers_comp": d.WC_VAL.to_numpy(float),
        "refundable_credits": (d.EIT_CRED + d.ACTC_CRD).to_numpy(float),
        "snap": unit("SPM_SNAPSUB"), "wic": unit("SPM_WICVAL"), "housing_support": unit("SPM_CAPHOUSESUB"),
        "energy": unit("SPM_ENGVAL"), "resources": np.maximum(unit("SPM_RESOURCES"), 0),
        "medicaid_covered": d.MCAID.eq(1).to_numpy(float),
    }


IRS_BINS = [-np.inf, 1, 25e3, 50e3, 75e3, 100e3, 200e3, 500e3, 1e6, np.inf]


def irs_binned_share(d, w, civ, tgt, base_w):
    """Group share of federal liability with national bin totals held at the published-weight CPS's (v4 item 3:
    IRS totals by AGI bin, the group's share inside each bin from the CPS)."""
    tax = d.FEDTAX_BC.to_numpy(float)
    b = np.digitize(d.AGI.to_numpy(float), IRS_BINS[1:-1])
    total = 0.0
    for k in np.unique(b):
        m = b == k
        t_bin = tax[m & civ] @ base_w[m & civ]
        n_new = tax[m & civ] @ w[m & civ]
        if n_new > 0:
            total += t_bin*(tax[m & tgt] @ w[m & tgt])/n_new
    return total/(tax[civ] @ base_w[civ])


def main():
    sb = load_spending_builder()
    curves = pd.read_csv(HERE/"curves_by_eye.csv")
    d, h = read_cps(sb)
    h = householder_groups(d, h)
    civ, tgt = sb.canonical_target(d)
    base = d.pwwgt0.to_numpy(float)
    if abs(base[tgt].sum() - 40896574.15235156) > .01:
        raise ValueError("Canonical target population drift")
    vectors = key_vectors(d, sb)
    hh_index = pd.Index(h.H_SEQ.to_numpy())
    pos = hh_index.get_indexer(d.PH_SEQ.to_numpy())
    in_h = pos >= 0
    controls, shares, quantile_rows = [], [], []
    base_share = {k: (v[tgt] @ base[tgt])/(v[civ] @ base[civ]) for k, v in vectors.items()}
    base_irs = irs_binned_share(d, base, civ, tgt, base)
    pgrid = np.arange(10, 100, 5)/100
    for curve_arm in ["raw", "smooth"]:
        factor = np.ones(len(h))
        for g, col in CURVE_COLS.items():
            pts = curves[["pct", col]].to_numpy(float)
            pts[:, 0] /= 100
            if curve_arm == "smooth":
                pts = smooth(pts)
            m = (h.group == g).to_numpy()
            factor[m] = household_factors(h.HTOTVAL.to_numpy(float)[m], h.HSUP_WGT.to_numpy(float)[m], pts)
        hw_new = h.HSUP_WGT.to_numpy(float)*factor
        # positive control and per-group check: survey / adjusted quantile ratios on the reweighted file
        for g in ["all"] + list(CURVE_COLS):
            m = np.ones(len(h), bool) if g == "all" else (h.group == g).to_numpy()
            y = h.HTOTVAL.to_numpy(float)[m]
            qs, qa = wquantile(y, h.HSUP_WGT.to_numpy(float)[m], pgrid), wquantile(y, hw_new[m], pgrid)
            target_col = "all" if g == "all" else CURVE_COLS[g]
            for p, a, b in zip(pgrid, qs, qa):
                quantile_rows.append(dict(curve=curve_arm, group=g, pct=int(round(p*100)), survey=a, adjusted=b,
                                          implied_ratio=a/b, published=float(np.interp(p*100, curves.pct, curves[target_col]))))
        pf = np.where(in_h, factor[np.maximum(pos, 0)], 1.0)
        for count_arm in ["free", "pinned"]:
            w = base*pf
            if count_arm == "pinned":
                w = w.copy()
                w[tgt] *= base[tgt].sum()/w[tgt].sum()
                rest = civ & ~tgt
                w[rest] *= base[rest].sum()/w[rest].sum()
            controls.append(dict(curve=curve_arm, count=count_arm, group_persons=w[tgt].sum(),
                                 group_persons_base=base[tgt].sum(), civilian_persons=w[civ].sum(),
                                 civilian_persons_base=base[civ].sum()))
            for k, v in vectors.items():
                s = (v[tgt] @ w[tgt])/(v[civ] @ w[civ])
                shares.append(dict(curve=curve_arm, count=count_arm, key=k, base_share=base_share[k], new_share=s,
                                   ratio=s/base_share[k]))
            s = irs_binned_share(d, w, civ, tgt, base)
            shares.append(dict(curve=curve_arm, count=count_arm, key="federal_liability_irs_bins", base_share=base_irs,
                               new_share=s, ratio=s/base_irs))
    shares = pd.DataFrame(shares)
    write(OUT/"key_shares.csv", shares)
    write(OUT/"quantile_check.csv", pd.DataFrame(quantile_rows))
    write(OUT/"controls.csv", pd.DataFrame(controls))
    quantiles = pd.DataFrame(quantile_rows)
    lines = price_lines(shares)
    price_v5(lines, shares, quantiles)


def price_lines(shares):
    r = pd.read_csv(RECEIPTS).query("scenario_id=='cbo_collective' and allocation=='personal'")
    s = pd.read_csv(SPENDING).query("scenario_id=='complete_preferred_F_per_capita' and allocation=='personal'")
    rows = []
    for side, frame, sign in [("receipt", r, -1), ("spending", s, 1)]:
        for rec in frame.itertuples():
            key = rec.allocation_key
            if side == "receipt" and rec.category == "federal_income_tax":
                key = "federal_liability_irs_bins"
            for (curve, count), part in shares.groupby(["curve", "count"]):
                hit = part[part.key == key]
                if hit.empty:
                    continue
                ratio = float(hit.ratio.iloc[0])
                change = rec.target_bn*(ratio - 1)
                rows.append(dict(side=side, category=rec.category, key=key, curve=curve, count=count,
                                 target_bn=rec.target_bn, ratio=ratio, change_bn=change, net_cost_change_bn=sign*change))
    lines = pd.DataFrame(rows)
    write(OUT/"line_changes.csv", lines)
    summary = (lines.groupby(["curve", "count", "side"]).net_cost_change_bn.sum().unstack("side").fillna(0))
    summary["net_cost_change_bn"] = summary.sum(axis=1)
    write(OUT/"summary.csv", summary.reset_index())
    print(summary.round(2).to_string())
    return lines


# Income-type keys: their national totals should fall by the published all-household bias.
INCOME_KEYS = {"federal_liability", "federal_liability_irs_bins", "state_liability", "wage", "wage_oasdi",
               "self_payroll", "capital", "consumption", "resources"}
ACCRUAL = FISCAL/"main_case_2026_10_05/derived/corrections.json"


def price_v5(lines, shares, quantiles):
    """Move the line changes onto v5's rules, on the pinned count.

    - Social Security is accrual in v5: ratio_net x the group's OASDI receipts (meta.pension_accrual), so its change
      follows the OASDI receipt lines, not the benefit key.
    - Medicare keeps (1 - part_a_share) on its key; Part A is part_a_accrual_bn, moved here at the HI wage key.
    - Lines whose v5 key is not a CPS income or receipt vector are not in `lines` (population, schools, MEPS
      medical, use keys); population keys move by exactly 0 on the pinned count.
    - denominator: 'reweighted' as computed; 'calibrated' also lowers the other residents' income-type key totals by
      the shortfall of the reweighted all-household curve against figure 3 (the between-group part this reweight
      does not model), which shrinks the group's share loss.
    """
    acc = json.loads(ACCRUAL.read_text())["meta"]["pension_accrual"]
    rows = []
    for curve, part in lines[lines["count"] == "pinned"].groupby("curve"):
        q = quantiles[(quantiles.curve == curve) & (quantiles.group == "all")]
        shortfall = float((q.published - q.implied_ratio).mean()/q.published.mean())
        ks = shares[(shares.curve == curve) & (shares["count"] == "pinned")].set_index("key")
        for denominator in ["reweighted", "calibrated"]:
            def ratio(key):
                r = float(ks.loc[key, "ratio"])
                if denominator == "calibrated" and key in INCOME_KEYS:
                    s0, s1 = float(ks.loc[key, "base_share"]), float(ks.loc[key, "new_share"])
                    r = s1/(s1 + (1 - s1)*(1 - shortfall))/s0
                return r
            out = []
            for rec in part.itertuples():
                sign = -1 if rec.side == "receipt" else 1
                if rec.category == "social_security":
                    continue
                amount = rec.target_bn*(1 - acc["part_a_share"]) if rec.category == "medicare" else rec.target_bn
                out.append(dict(item=rec.category, side=rec.side, net_cost_change_bn=sign*amount*(ratio(rec.key) - 1)))
            oasdi = sum(part.set_index("category").target_bn[c]*(ratio("wage_oasdi") - 1) for c in acc["oasdi_lines"])
            oasdi += acc["se_oasdi_share"]*part.set_index("category").target_bn[acc["se_line"]]*(ratio("self_payroll") - 1)
            out.append(dict(item="social_security_accrual", side="spending", net_cost_change_bn=acc["ratio_net"]*oasdi))
            out.append(dict(item="part_a_accrual", side="spending",
                            net_cost_change_bn=acc["part_a_accrual_bn"]*(ratio("wage") - 1)))
            for o in out:
                rows.append(dict(curve=curve, denominator=denominator, shortfall=shortfall, **o))
    v5 = pd.DataFrame(rows)
    write(OUT/"v5_line_changes.csv", v5)
    summary = v5.groupby(["curve", "denominator", "side"]).net_cost_change_bn.sum().unstack("side")
    summary["net_cost_change_bn"] = summary.sum(axis=1)
    write(OUT/"v5_summary.csv", summary.reset_index())
    print(summary.round(2).to_string())


def write(path, frame):
    frame.to_csv(path, index=False, lineterminator="\n", float_format="%.10g")


if __name__ == "__main__":
    main()
