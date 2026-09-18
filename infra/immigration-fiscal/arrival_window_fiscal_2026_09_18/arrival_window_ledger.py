#!/usr/bin/env python3
"""Mexico-born all-age fiscal account split by CPS year-of-entry window.

Native-First: the upstream CPS builder (`gen_ledger_extension_2026_09_16`), the
all-age lane's account matrix / estimator (`all_age_ledger_2026_09_17`) and the
complete-account charge builder (`ledger_absolute_2026_09_17`) are imported and
called, never copied. This lane only re-cuts the `mexico_born` group by PEINUSYR.

Run from the repository root:

    OPENBLAS_NUM_THREADS=1 uv run --no-project python3 \
      infra/immigration-fiscal/arrival_window_fiscal_2026_09_18/arrival_window_ledger.py

Writes derived/*.csv and audit.json next to this file. No raw-file changes, no
writes to other lanes, no downloads.
"""
from __future__ import annotations

import argparse
import json
import sys
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
FISCAL = HERE.parent
ROOT = HERE.parents[2]
ALL_AGE = FISCAL / "all_age_ledger_2026_09_17"
ABSOLUTE = FISCAL / "ledger_absolute_2026_09_17"
GENEXT = FISCAL / "gen_ledger_extension_2026_09_16"
RESIDUAL = FISCAL / "ledger_residual_agg_2026_09_16"
INSTITUTIONAL = FISCAL / "institutional_bound_2026_09_17"

sys.path.insert(0, str(ALL_AGE))
sys.path.insert(0, str(ABSOLUTE))

import analyze as A                       # noqa: E402  (also puts GENEXT/build on the path)
import absolute_ledger as AL              # noqa: E402
import residual_agg as resid              # noqa: E402
from estimator import account, contrast, summarize  # noqa: E402

# Parent-link and complete-account fields the base generator does not read.
# base.PERSON is consumed by prepare() as usecols at call time, so extending it
# here (before ext.build) is enough.
MY_EXTRA_PERSON = ["A_LINENO", "PEPAR1", "PEPAR2"]
for _f in list(AL.EXTRA_PERSON) + MY_EXTRA_PERSON:
    if _f not in A.ext.base.PERSON:
        A.ext.base.PERSON.append(_f)

COMPONENTS = A.COMPONENTS                  # tax cash noncash employer sales owner_property school lunch
COEFFICIENTS = A.COEFFICIENTS
COMPONENT_ORDER = ["tax", "employer", "sales", "owner_property", "cash", "noncash",
                   "school", "lunch", "medical"]
WHITE = "third_plus_nh_white"
ALL_NATIVE = "all_native"
BAND_LABELS = ["0-17", "18-24", "25-34", "35-44", "45-54", "55-64", "65-74", "75+"]

# ---------------------------------------------------------------------------
# PEINUSYR, "When did you come to the U.S. to stay?", CPS ASEC March 2025
# public-use person file, position 133, length 2. Value list transcribed from
# the held technical documentation, cpsmar25.pdf p. 41 (person record layout):
#   00 = NIU        01 = Before 1950  02 = 1950-1959  03 = 1960-1964
#   04 = 1965-1969  05 = 1970-1974    06 = 1975-1979  07 = 1980-1981
#   08 = 1982-1983  09 = 1984-1985    10 = 1986-1987  11 = 1988-1989
#   12 = 1990-1991  13 = 1992-1993    14 = 1994-1995  15 = 1996-1997
#   16 = 1998-1999  17 = 2000-2001    18 = 2002-2003  19 = 2004-2005
#   20 = 2006-2007  21 = 2008-2009    22 = 2010-2011  23 = 2012-2013
#   24 = 2014-2015  25 = 2016-2017    26 = 2018-2019  27 = 2020-2021
#   28 = 2022-2025
# Every window boundary below falls between two codes, so no code is split.
# ---------------------------------------------------------------------------
CODE_SPAN = {
    1: "before 1950", 2: "1950-1959", 3: "1960-1964", 4: "1965-1969", 5: "1970-1974",
    6: "1975-1979", 7: "1980-1981", 8: "1982-1983", 9: "1984-1985", 10: "1986-1987",
    11: "1988-1989", 12: "1990-1991", 13: "1992-1993", 14: "1994-1995", 15: "1996-1997",
    16: "1998-1999", 17: "2000-2001", 18: "2002-2003", 19: "2004-2005", 20: "2006-2007",
    21: "2008-2009", 22: "2010-2011", 23: "2012-2013", 24: "2014-2015", 25: "2016-2017",
    26: "2018-2019", 27: "2020-2021", 28: "2022-2025",
}
WINDOWS = {
    "w1_pre1990": (list(range(1, 12)), "before 1950 through 1989"),
    "w2_1990_1999": (list(range(12, 17)), "1990 through 1999"),
    "w3_2000_2009": (list(range(17, 22)), "2000 through 2009"),
    "w4_2010_2015": (list(range(22, 25)), "2010 through 2015"),
    "w5_2016_2025": (list(range(25, 29)), "2016 through the March 2025 interview (top code 28 = 2022-2025)"),
}
WINDOW_NAMES = list(WINDOWS)


# ---------------------------------------------------------------------------
# Estimator variants that tolerate structurally empty age bands.
# A window like "arrived before 1990" cannot contain anyone under 18, so the
# upstream `sufficient` (which refuses a nonpositive band population) cannot be
# used unchanged. Totals are unaffected: an empty band contributes zero dollars
# and zero people. Only per-person quantities need the band mask.
# ---------------------------------------------------------------------------
def sufficient_sparse(values, exposures, weights, masks, bands, band_count=8):
    out = {}
    for group, mask in masks.items():
        ns, ys, hs = [], [], []
        for band in range(band_count):
            selected = np.asarray(mask) & (bands == band)
            w = weights[selected]
            n = w.sum(axis=0)
            if not np.isfinite(n).all() or (n < 0).any():
                raise ValueError(f"Nonfinite/negative population: {group}, band {band}")
            ns.append(n)
            ys.append(values[selected].T @ w)
            hs.append(exposures[selected].T @ w)
        out[group] = dict(n=np.array(ns), y=np.array(ys), h=np.array(hs))
    return out


def standardized_gap_support(target, reference, coefficients, means, age_shares, support):
    """Common-age gap restricted to `support` bands, shares renormalised over them.

    `support` is fixed from the full-weight populations and must have positive
    population in every replicate, so the per-person ratios are always defined.
    """
    shares = np.asarray(age_shares, dtype=float)
    sel = np.asarray(support, dtype=bool)
    if not sel.any():
        raise ValueError("empty standardisation support")
    if (target["n"][sel] <= 0).any():
        raise ValueError("standardisation support contains an empty target band")
    s = np.zeros_like(shares)
    s[sel] = shares[sel] / shares[sel].sum()
    # Unsupported bands carry zero weight; their denominator is replaced by one
    # so no 0/0 is ever evaluated.
    tn = np.where(sel[:, None], target["n"], 1.0)
    tg = account(target, coefficients, means) / tn
    rf = account(reference, coefficients, means) / reference["n"]
    value = (s[:, None] * (tg - rf)).sum(axis=0)
    grad = -(s[:, None] * (target["h"][:, :, 0] / tn[:, 0, None]
                           - reference["h"][:, :, 0] / reference["n"][:, 0, None])).sum(axis=0)
    return value, grad


def component_split(target, reference, coefficients, means):
    """Age-matched gap decomposed into the eight base components plus medical."""
    ratio = target["n"] / reference["n"]
    comp = (target["y"][:, :len(COMPONENTS), :] - ratio[:, None, :] * reference["y"][:, :len(COMPONENTS), :]).sum(axis=0)
    comp = coefficients[:len(COMPONENTS), None] * comp
    medical = -(np.einsum("bjr,j->br", target["h"], means)
                - ratio * np.einsum("bjr,j->br", reference["h"], means)).sum(axis=0)
    out = {name: comp[k] for k, name in enumerate(COMPONENTS)}
    out["medical"] = medical
    return out


# ---------------------------------------------------------------------------
def complete_charges(state, base_matrix, civilian, groups_for_ctx, codes, payer_means, exposure,
                     params_path):
    """Per-record charge vectors for the complete-account items, via the absolute lane.

    Recomputed from `ledger_absolute_2026_09_17`'s own `build_charges` and its
    verified parameter file; nothing is read back from that lane's derived CSVs.
    """
    d, index, n_units, weights = state["d"], state["index"], state["n_units"], state["person_weights"]
    heads = d.loc[d.SPM_HEAD.eq(1)].sort_values("SPM_ID")
    params = AL.Params(params_path, False)
    pop_state = resid.read_state_population()
    gs_pc, gs_national = resid.read_general_services_per_capita(pop_state)
    cap = AL.read_cog_capital(RESIDUAL / "_cache/22slsstab1.xlsx", pop_state)
    assf = AL.read_assf_k12(GENEXT / "census_assf_fy2024_summary_tables.xlsx")
    omb = AL.read_omb_functions(RESIDUAL / "_cache/omb_hist03z1_fy2027.xlsx")
    us_resident = params.pick("population", ["2024"], "count")
    vintage = "NST-EST2024 (params)"
    if us_resident is None:
        us_resident = resid.read_us_population()
        vintage = "NST-EST2023 cached fallback"
    member_count = sum(groups_for_ctx[g].astype(int) for g in AL.TARGETS)
    ctx = dict(d=d, index=index, n_units=n_units, civilian=civilian, weights=weights,
               heads=heads, general_services=(gs_pc, gs_national), assf=assf, omb=omb,
               donor_codes=codes, donor_payer_means=payer_means, exposure=exposure,
               n_civilian=float(weights[civilian, 0].sum()), us_resident=us_resident,
               consumption_proxy=base_matrix[:, 4], capital=cap, off=[],
               is_white_ref=groups_for_ctx[WHITE], is_target=member_count > 0)
    charges, dropped, centrals, national, _ = AL.build_charges(ctx, params)
    return charges, dropped, centrals, national, us_resident, vintage


# ---------------------------------------------------------------------------
def own_children(d, weights, window_masks):
    """Own children under 18 in the household, per window adult (18+).

    CPS ASEC carries parent line numbers PEPAR1/PEPAR2 (position of the parent's
    record inside the household). A child under 18 is counted against an adult
    when either pointer equals that adult's A_LINENO in the same household.
    """
    kids = d.A_AGE.lt(18).to_numpy()
    key = d.PH_SEQ.to_numpy()
    lineno = d.A_LINENO.to_numpy()
    counts = {}
    for which in ["PEPAR1", "PEPAR2"]:
        link = d[which].to_numpy()
        valid = kids & (link > 0)
        pairs = pd.DataFrame(dict(h=key[valid], p=link[valid]))
        counts[which] = pairs.groupby(["h", "p"]).size()
    total = counts["PEPAR1"].add(counts["PEPAR2"], fill_value=0)
    own = pd.Series(list(zip(key, lineno))).map(total).fillna(0.0).to_numpy()
    # US-born share of the linked children, to make the omitted dependants concrete.
    native_kid = kids & d.PRCITSHP.isin([1, 2, 3]).to_numpy()
    rows = []
    for name, mask in window_masks.items():
        adults = mask & d.A_AGE.ge(18).to_numpy()
        w = weights[adults, 0]
        if w.sum() <= 0:
            continue
        # children linked to those adults, by household/line pointer
        target = set(zip(key[adults], lineno[adults]))
        linked = np.zeros(len(d), dtype=bool)
        for which in ["PEPAR1", "PEPAR2"]:
            link = d[which].to_numpy()
            linked |= kids & (link > 0) & np.array(
                [(h, p) in target for h, p in zip(key, link)])
        lw = weights[linked, 0]
        rows.append(dict(window=name,
                         adults_18plus=float(w.sum()),
                         own_children_under18_per_adult=float((own[adults] * w).sum() / w.sum()),
                         linked_children_weighted=float(lw.sum()),
                         linked_children_us_born_share=float(weights[linked & native_kid, 0].sum() / lw.sum())
                         if lw.sum() > 0 else float("nan")))
    return pd.DataFrame(rows)


# ---------------------------------------------------------------------------
def try_asec2026(cps_2026: Path) -> dict:
    """Item (7): can the upstream builder consume the ASEC 2026 file unchanged?"""
    if not cps_2026.exists():
        return dict(attempted=False, reason=f"file absent: {cps_2026}")
    try:
        with zipfile.ZipFile(cps_2026) as z:
            names = z.namelist()
        A.ext.build(argparse.Namespace(cps_zip=cps_2026))
        return dict(attempted=True, accepted=True, members=names)
    except Exception as exc:  # noqa: BLE001 - the point is to report the exact failure
        return dict(attempted=True, accepted=False,
                    error=f"{type(exc).__name__}: {exc}")


# ---------------------------------------------------------------------------
def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--params", type=Path, default=ABSOLUTE / "params/params.json")
    ap.add_argument("--skip-complete", action="store_true")
    args = ap.parse_args()

    out = HERE / "derived"
    out.mkdir(exist_ok=True)
    cps = GENEXT / "_cache/asecpub25csv.zip"
    medical_zip = ROOT / "sources/immigration-fiscal/data/external/stage3/ahrq/meps_2024/h256dat.zip"
    medical_sas = medical_zip.with_name("h256su.txt")

    print("[stage] building the upstream CPS state", flush=True)
    state = A.ext.build(argparse.Namespace(cps_zip=cps))
    d = state["d"]
    weights = state["person_weights"]
    civilian = (d.PRPERTYP.eq(2) | d.A_AGE.lt(15)).to_numpy()
    bands = np.digitize(d.A_AGE, [18, 25, 35, 45, 55, 65, 75])

    us = [57, 60, 66, 69, 73, 78]
    parents_us = (d.PEFNTVTY.isin(us) & d.PEMNTVTY.isin(us)).to_numpy()
    lane_groups = {g: state["group"][g] & civilian for g in
                   ["mexico_born", "mexican_second_gen", "mexican_third_plus_selfid",
                    WHITE, ALL_NATIVE]}
    lane_groups["native_two_us_parents"] = lane_groups[ALL_NATIVE] & parents_us

    mexico = lane_groups["mexico_born"]
    entry = d.PEINUSYR.to_numpy()
    if entry[mexico].min() < 1 or entry[mexico].max() > 28:
        raise SystemExit(f"[BLOCKED] PEINUSYR outside 1-28 for Mexico-born: "
                         f"{sorted(set(entry[mexico].tolist()))[:3]}...")
    if d.PEINUSYR.max() > 28:
        raise SystemExit("[BLOCKED] PEINUSYR code 29 present: 2026+ ASEC layout, recode windows")
    window_masks = {name: mexico & np.isin(entry, codes) for name, (codes, _) in WINDOWS.items()}
    covered = sum(m.astype(int) for m in window_masks.values())
    if covered.max() > 1:
        raise SystemExit("[BLOCKED] arrival windows overlap")
    if int(covered[mexico].sum()) != int(mexico.sum()):
        raise SystemExit("[BLOCKED] arrival windows do not partition the Mexico-born group")

    print("[stage] account matrix and MEPS donor transport", flush=True)
    shared, _personal, _renter = A.matrices(state)
    medical, anchors = A.read_meps(medical_zip, medical_sas)
    cells, codes, covariance = A.donor_model(medical, d, False)
    means = cells.mean_public_paid.to_numpy()
    exposure = ~(d.PUB.eq(0) & d.PRIV.eq(0)).to_numpy()
    if (d.loc[~exposure, "A_AGE"] > 0).any():
        raise SystemExit("[BLOCKED] post-reference-year exclusion contains a noninfant")
    health = np.eye(len(cells))[codes] * exposure[:, None]

    # ---- complete-account flat charges (items G, K, X, R central arms) -----
    charge_matrix = np.zeros((len(d), 0))
    charge_keys: list[str] = []
    complete_info: dict = dict(built=False)
    if not args.skip_complete:
        print("[stage] complete-account charges via ledger_absolute_2026_09_17", flush=True)
        charges, dropped, centrals, national, us_resident, vintage = complete_charges(
            state, shared, civilian, lane_groups, codes,
            _payer_means(medical, cells), exposure, args.params)
        wanted = [("G", centrals.get("G")), ("K", centrals.get("K")),
                  ("X", centrals.get("X")), ("R", centrals.get("R"))]
        cols, keys, missing = [], [], []
        full = charges.matrix()
        for item, arm in wanted:
            key = f"{item}|{arm}" if arm else None
            if key is None or key not in charges.columns:
                missing.append(item)
                continue
            cols.append(full[:, charges.columns.index(key)])
            keys.append(key)
        charge_matrix = np.column_stack(cols) if cols else np.zeros((len(d), 0))
        charge_keys = keys
        complete_info = dict(built=True, keys=keys, missing_items=missing,
                             dropped=dropped, us_resident=us_resident,
                             population_vintage=vintage,
                             national={k: national[k] for k in keys if k in national})
        print(f"[complete] charge columns used: {keys}; dropped items: "
              f"{[x['item'] for x in dropped]}", flush=True)

    values = np.column_stack([shared, charge_matrix]) if charge_matrix.size else shared
    n_base = len(COMPONENTS)
    base_coeff = np.concatenate([COEFFICIENTS, np.zeros(charge_matrix.shape[1])])
    complete_coeff = np.concatenate([COEFFICIENTS, np.ones(charge_matrix.shape[1])])

    print("[stage] replicate aggregation over windows and references", flush=True)
    masks = dict(window_masks)
    masks["mexico_born"] = mexico
    masks[WHITE] = lane_groups[WHITE]
    masks[ALL_NATIVE] = lane_groups[ALL_NATIVE]
    stats = sufficient_sparse(values, health, weights, masks, bands, 8)

    # ---- gate 1: the windows partition the Mexico-born cell exactly --------
    union = {k: sum(stats[w][k] for w in WINDOW_NAMES) for k in ["n", "y", "h"]}
    pop_residual = float(np.max(np.abs(union["n"] - stats["mexico_born"]["n"])))
    y_residual = float(np.max(np.abs(union["y"] - stats["mexico_born"]["y"])))
    gate_pop = pop_residual <= 1.0
    print(f"[gate 1] window populations reproduce the Mexico-born cell: "
          f"max |diff| = {pop_residual:.6f} people, {y_residual:.6f} dollars -> "
          f"{'PASS' if gate_pop and y_residual <= 0.01 else 'FAIL'}", flush=True)
    if not (gate_pop and y_residual <= 0.01):
        raise SystemExit("[BLOCKED] gate 1 failed")

    white_totals = np.bincount(bands[masks[WHITE]], weights=weights[masks[WHITE], 0], minlength=8)
    white_shares = white_totals / white_totals.sum()

    # Support: bands with positive population in the full weight AND in every
    # replicate, so no per-person ratio is ever 0/0.
    def support_of(cell):
        return (cell["n"] > 0).all(axis=1)

    supports = {g: support_of(stats[g]) for g in stats}
    full_support = np.ones(8, dtype=bool)
    common_support = np.logical_and.reduce([supports[w] for w in WINDOW_NAMES])
    print(f"[support] per-window populated bands: "
          + "; ".join(f"{w}={[BAND_LABELS[i] for i in np.flatnonzero(supports[w])]}"
                      for w in WINDOW_NAMES), flush=True)
    print(f"[support] common support across all windows: "
          f"{[BAND_LABELS[i] for i in np.flatnonzero(common_support)]} "
          f"({white_shares[common_support].sum():.3f} of the white age standard)", flush=True)

    # ---- gate 2: union reproduces the stored absolute and common-age gap ---
    stored = pd.read_csv(ALL_AGE / "derived/estimates.csv")
    sel = stored[(stored.scenario == "all_age_shared") & (stored.target == "mexico_born")]
    stored_abs = float(sel[sel.metric == "absolute_total"].estimate.iloc[0])
    stored_gap = float(sel[(sel.metric == "standardized_gap_per_person")
                           & (sel.reference == WHITE)].estimate.iloc[0])
    union_abs = float(account(union, base_coeff, means).sum(axis=0)[0])
    union_gap = float(standardized_gap_support(union, stats[WHITE], base_coeff, means,
                                               white_shares, full_support)[0][0])
    d_abs, d_gap = union_abs - stored_abs, union_gap - stored_gap
    ok2 = abs(d_abs) <= 0.01 and abs(d_gap) <= 0.01
    print(f"[gate 2] union absolute {union_abs/1e9:+.5f}bn vs stored {stored_abs/1e9:+.5f}bn "
          f"(residual ${d_abs:.4f}); union common-age gap {union_gap:,.3f} vs stored "
          f"{stored_gap:,.3f} (residual ${d_gap:.4f}) -> {'PASS' if ok2 else 'FAIL'}", flush=True)
    if not ok2:
        raise SystemExit("[BLOCKED] gate 2 failed")

    # ---- gate 3: the four charge columns match the absolute lane's items ---
    gate3 = dict(checked=False)
    items_path = ABSOLUTE / "derived/items_by_group.csv"
    if charge_keys and items_path.exists():
        items = pd.read_csv(items_path)
        want = pd.DataFrame([dict(item=k.split("|")[0], arm=k.split("|")[1]) for k in charge_keys])
        sel_i = items.merge(want, on=["item", "arm"]).query("group == 'mexico_born'")
        if len(sel_i) != len(charge_keys):
            raise SystemExit("[BLOCKED] gate 3: item rows missing from the absolute lane")
        mine_bn = (float(account(stats["mexico_born"], complete_coeff, means)[:, 0].sum())
                   - float(account(stats["mexico_born"], base_coeff, means)[:, 0].sum())) / 1e9
        theirs_bn = float(sel_i.total_bn.sum())
        mine_gap = (float(standardized_gap_support(stats["mexico_born"], stats[WHITE], complete_coeff,
                                                   means, white_shares, full_support)[0][0])
                    - stored_gap)
        theirs_gap = float(sel_i.common_age_gap_per_person_vs_white.sum())
        ok3 = abs(mine_bn - theirs_bn) <= 0.01 and abs(mine_gap - theirs_gap) <= 0.01
        gate3 = dict(checked=True, mine_bn=mine_bn, absolute_lane_bn=theirs_bn,
                     mine_gap=mine_gap, absolute_lane_gap=theirs_gap, passed=ok3)
        print(f"[gate 3] charge columns vs ledger_absolute items_by_group: "
              f"{mine_bn:+.4f}bn vs {theirs_bn:+.4f}bn; gap {mine_gap:+.3f} vs {theirs_gap:+.3f} "
              f"-> {'PASS' if ok3 else 'FAIL'}", flush=True)
        if not ok3:
            raise SystemExit("[BLOCKED] gate 3 failed")

    # ---- per-window estimates --------------------------------------------
    rows, comp_rows, band_rows, rep = [], [], [], {}
    mean_age = {}
    for name in WINDOW_NAMES + ["mexico_born"]:
        m = masks[name]
        mean_age[name] = float(np.average(d.A_AGE.to_numpy()[m], weights=weights[m, 0]))
    for name in WINDOW_NAMES + ["mexico_born"]:
        cell = stats[name]
        n = cell["n"].sum(axis=0)
        for label, coeff, tag in [("partial", base_coeff, ""), ("complete", complete_coeff, "")]:
            if label == "complete" and not charge_keys:
                continue
            y = account(cell, coeff, means).sum(axis=0)
            q = -cell["h"][:, :, 0].sum(axis=0)
            for metric, v, grad in [(f"{label}_absolute_total", y, q),
                                    (f"{label}_absolute_per_person", y / n, q / n[0])]:
                rows.append(dict(window=name, reference="", matching="", metric=metric,
                                 population=float(n[0]), mean_age=mean_age[name],
                                 **summarize(v, grad, covariance)))
                rep[f"{name}|{metric}"] = (v, grad)
            for ref in [WHITE, ALL_NATIVE]:
                for sup_name, sup in [("common_support", common_support),
                                      ("window_support", supports[name])]:
                    std, qs = standardized_gap_support(cell, stats[ref], coeff, means,
                                                       white_shares, sup)
                    metric = f"{label}_common_age_gap_per_person_{sup_name}"
                    rows.append(dict(window=name, reference=ref, matching=sup_name,
                                     metric=metric, population=float(n[0]),
                                     mean_age=mean_age[name],
                                     standard_mass=float(white_shares[sup].sum()),
                                     **summarize(std, qs, covariance)))
                    rep[f"{name}|{ref}|{metric}"] = (std, qs)
                v, grad = contrast(cell, stats[ref], coeff, means, True)
                rows.append(dict(window=name, reference=ref, matching="age_band",
                                 metric=f"{label}_age_matched_gap_total", population=float(n[0]),
                                 mean_age=mean_age[name], **summarize(v, grad, covariance)))
                rep[f"{name}|{ref}|{label}_age_matched_gap_total"] = (v, grad)
        # component split of the partial age-matched gap
        for ref in [WHITE, ALL_NATIVE]:
            split = component_split(cell, stats[ref], COEFFICIENTS, means)
            total = float(contrast(cell, stats[ref], base_coeff, means, True)[0][0])
            recomposed = float(sum(v[0] for v in split.values()))
            if abs(recomposed - total) > 0.02:
                raise SystemExit(f"[BLOCKED] components do not sum to the gap for {name}/{ref}")
            for comp in COMPONENT_ORDER:
                comp_rows.append(dict(window=name, reference=ref, component=comp,
                                      gap_total=float(split[comp][0]),
                                      gap_per_person=float(split[comp][0] / n[0])))
        # per-band balance per person
        per_band = account(cell, base_coeff, means)
        per_band_c = account(cell, complete_coeff, means) if charge_keys else None
        for b in range(8):
            pop_b = float(cell["n"][b, 0])
            band_rows.append(dict(
                window=name, band=b, band_label=BAND_LABELS[b], population=pop_b,
                partial_balance_per_person=float(per_band[b, 0] / pop_b) if pop_b > 0 else float("nan"),
                complete_balance_per_person=(float(per_band_c[b, 0] / pop_b)
                                             if (charge_keys and pop_b > 0) else float("nan"))))

    table = pd.DataFrame(rows)
    table.to_csv(out / "window_estimates.csv", index=False)
    pd.DataFrame(comp_rows).to_csv(out / "window_component_gaps.csv", index=False)
    pd.DataFrame(band_rows).to_csv(out / "window_age_profiles.csv", index=False)

    # ---- derivative view --------------------------------------------------
    deriv_rows = []
    for label in (["partial"] + (["complete"] if charge_keys else [])):
        for ref in [WHITE, ALL_NATIVE]:
            key = f"{label}_common_age_gap_per_person_common_support"
            series = [rep[f"{w}|{ref}|{key}"] for w in WINDOW_NAMES]
            for i in range(len(WINDOW_NAMES)):
                deriv_rows.append(dict(account=label, reference=ref, order=0,
                                       later=WINDOW_NAMES[i], earlier="",
                                       **summarize(series[i][0], series[i][1], covariance)))
            first = []
            for i in range(1, len(WINDOW_NAMES)):
                v = series[i][0] - series[i - 1][0]
                g = series[i][1] - series[i - 1][1]
                first.append((v, g))
                deriv_rows.append(dict(account=label, reference=ref, order=1,
                                       later=WINDOW_NAMES[i], earlier=WINDOW_NAMES[i - 1],
                                       **summarize(v, g, covariance)))
            for i in range(1, len(first)):
                v = first[i][0] - first[i - 1][0]
                g = first[i][1] - first[i - 1][1]
                deriv_rows.append(dict(account=label, reference=ref, order=2,
                                       later=WINDOW_NAMES[i + 1], earlier=WINDOW_NAMES[i - 1],
                                       **summarize(v, g, covariance)))
    deriv = pd.DataFrame(deriv_rows)
    deriv.to_csv(out / "window_derivatives.csv", index=False)

    # ---- window descriptives and omitted dependants -----------------------
    desc = []
    for name in WINDOW_NAMES + ["mexico_born"]:
        m = masks[name]
        desc.append(dict(window=name,
                         codes=",".join(str(c) for c in WINDOWS[name][0]) if name in WINDOWS else "",
                         span=WINDOWS[name][1] if name in WINDOWS else "all codes 1-28",
                         records=int(m.sum()),
                         weighted_population=float(weights[m, 0].sum()),
                         mean_age=mean_age[name],
                         share_under18=float(weights[m & d.A_AGE.lt(18).to_numpy(), 0].sum()
                                             / weights[m, 0].sum())))
    kids = own_children(d, weights, {n: masks[n] for n in WINDOW_NAMES + ["mexico_born"]})
    descr = pd.DataFrame(desc).merge(kids, on="window", how="left")
    descr.to_csv(out / "window_descriptives.csv", index=False)

    # ---- item (7): ASEC 2026 --------------------------------------------
    asec26 = try_asec2026(FISCAL / "ledger_asec2026_2026_09_16/_cache/asecpub26csv.zip")
    if not asec26.get("accepted"):
        print(f"[asec2026] not repeated: {asec26.get('error') or asec26.get('reason')}", flush=True)

    audit = dict(
        inputs=[dict(path=str(p), sha256=A.ext.base.sha(p)) for p in
                [cps, medical_zip, medical_sas, A.ext.HERE / "state_parameters.csv",
                 Path(A.__file__), Path(A.ext.__file__), Path(AL.__file__), Path(__file__)]],
        peinusyr_codes=CODE_SPAN,
        windows={k: dict(codes=v[0], span=v[1]) for k, v in WINDOWS.items()},
        validation=state["validation"], medical_anchors=anchors,
        gates=dict(window_population_residual_people=pop_residual,
                   window_dollar_residual=y_residual,
                   union_absolute=union_abs, stored_absolute=stored_abs,
                   union_absolute_residual=d_abs,
                   union_common_age_gap=union_gap, stored_common_age_gap=stored_gap,
                   union_common_age_residual=d_gap,
                   all_standard_errors_finite=bool(np.isfinite(table.se_joint).all()),
                   charge_columns_vs_absolute_lane=gate3),
        support=dict(common_support=[BAND_LABELS[i] for i in np.flatnonzero(common_support)],
                     common_support_white_mass=float(white_shares[common_support].sum()),
                     per_window={w: [BAND_LABELS[i] for i in np.flatnonzero(supports[w])]
                                 for w in WINDOW_NAMES},
                     white_age_shares=white_shares.tolist()),
        complete_account=complete_info,
        asec_2026=asec26,
    )
    (out / "audit.json").write_text(json.dumps(audit, indent=2, default=str, allow_nan=False) + "\n")

    # ---- console summary --------------------------------------------------
    pd.set_option("display.width", 200)
    print("\n[windows]")
    print(descr[["window", "span", "records", "weighted_population", "mean_age",
                 "own_children_under18_per_adult"]].round(3).to_string(index=False))
    show = table[table.window.isin(WINDOW_NAMES + ["mexico_born"])]
    for metric in ["partial_absolute_per_person", "complete_absolute_per_person"]:
        sub = show[(show.metric == metric)]
        if len(sub):
            print(f"\n[{metric}]")
            print(sub[["window", "population", "estimate", "se_joint"]].round(1).to_string(index=False))
    for label in (["partial"] + (["complete"] if charge_keys else [])):
        sub = show[(show.metric == f"{label}_common_age_gap_per_person_common_support")
                   & (show.reference == WHITE)]
        print(f"\n[{label} common-age gap vs third-plus NH white, common support]")
        print(sub[["window", "estimate", "se_joint", "standard_mass"]].round(1).to_string(index=False))
    print("\n[derivatives, partial account vs white, common support]")
    print(deriv[(deriv.account == "partial") & (deriv.reference == WHITE)]
          [["order", "later", "earlier", "estimate", "se_joint"]].round(1).to_string(index=False))
    print("\n[per-band partial balance per person]")
    prof = pd.DataFrame(band_rows).pivot(index="band_label", columns="window",
                                         values="partial_balance_per_person")
    print(prof.reindex(BAND_LABELS).round(0).to_string())
    print("\n[component split of the partial age-matched gap vs white, $bn]")
    cg = pd.DataFrame(comp_rows)
    cg = cg[cg.reference == WHITE].pivot(index="component", columns="window", values="gap_total") / 1e9
    print(cg.reindex(COMPONENT_ORDER).round(2).to_string())
    print(f"\nPASS: {len(table)} estimates, gates 1-2 passed, "
          f"{int(np.isfinite(table.se_joint).sum())}/{len(table)} finite standard errors")


def _payer_means(medical, cells):
    """MEPS Medicaid/Medicare donor means, as the absolute lane computes them."""
    valid = medical.PERWT24F.gt(0) & medical.AGE24X.ge(0) & medical.BORNUSA.isin([1, 2])
    sample = medical.loc[valid]
    out = {}
    for label, column in [("medicaid", "TOTMCD24"), ("medicare", "TOTMCR24")]:
        wx = sample.assign(wx=sample[column] * sample.PERWT24F).groupby(["age_band", "born"]).wx.sum()
        pop = sample.groupby(["age_band", "born"]).PERWT24F.sum()
        series = (wx / pop).reindex(pd.MultiIndex.from_frame(cells[["age_band", "born"]]))
        if series.isna().any():
            raise ValueError(f"missing donor cell for {label}")
        out[label] = series.to_numpy()
    return out


if __name__ == "__main__":
    main()
