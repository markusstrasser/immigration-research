"""Scale and schooling-composition spillovers of a 40.9M US-born NH white slice, beside the union's, on the spillover
lane's own machinery (scale_spillovers_2026_09_23/arms.py, imported read-only; nothing is written there).

The white slice is every US-born NH white PUMA cell (derived/pums_white_cells.csv) times 40,896,574 / the ACS
US-born NH white total, so it keeps the white settlement pattern; other residents are everyone else. The union runs
through the same functions from the spillover lane's own cells, and its central joint estimate must reproduce that
lane's summary.csv (gate). Every scale, composition and joint specification is evaluated on CZs, CBSAs and one
national area, plus the Rosenthal-Strange rings and the Burchardi et al. transport.

Sign: a gain is a benefit of the group's presence to other residents. In the account's cost terms, the replacement
delta (cost of the union minus cost of the white slice) is gain_white - gain_union.
Outputs: derived/spill_grid.csv (every spec, both groups), derived/spill_summary.csv (the rows ladder 201 quotes),
derived/spill_innovation.csv, derived/spill_checks.json.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.dont_write_bytecode = True

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

LANE = Path(__file__).resolve().parent
FISCAL = LANE.parent
SPILL = FISCAL / "scale_spillovers_2026_09_23"
sys.path.insert(0, str(SPILL))
import arms as A  # noqa: E402

DER = LANE / "derived"
CENTRAL_JOINT = "CRY joint: scale by education + college gradient net of CES (sigma 2, CRY weights) [central]"


def white_wide():
    cells = pd.read_csv(DER / "pums_white_cells.csv", dtype={"STATE": str, "PUMA": str})
    allp = cells.groupby(["STATE", "PUMA"])[A.ITEMS].sum()
    wht = cells[cells.label == "nhw_usborn"].set_index(["STATE", "PUMA"])[A.ITEMS].reindex(allp.index, fill_value=0.0)
    k = A.CPS_UNION / float(wht["persons"].sum())
    wide = pd.DataFrame(index=allp.index)
    for v in A.ITEMS:
        wide[f"group_{v}"] = k * wht[v]
        wide[f"other_{v}"] = allp[v] - k * wht[v]
        wide[f"mexborn_{v}"] = 0.0
    return wide.reset_index(), k, wht.sum()


def context(nat_table, cry_joint, geos):
    """The spillover lane's main(): CES shares, Moretti weights and the Glaeser-Resseger demeaning points."""
    sw = pd.read_csv(SPILL / "derived/sample_weights.csv").set_index(["year", "cell"])
    ws = lambda yr, col: np.array([sw.loc[(yr, c), col] for c in ("lths", "hs", "sc", "ba")])  # noqa: E731
    all_w = nat_table[nat_table.label == "all"].set_index("item")["estimate"]
    w_more = all_w["workers_sc"] + all_w["workers_ba"] + all_w["workers_grad"]
    e_more = all_w["earnings_sc"] + all_w["earnings_ba"] + all_w["earnings_grad"]
    rel = (e_more / w_more) / ((all_w["earnings"] - e_more) / (all_w["workers"] - w_more))
    s_cry = cry_joint["s_sc_cry_sample"]
    theta_cry = s_cry * rel / (s_cry * rel + 1 - s_cry)
    ba = lambda yrs: {"s": float(np.mean([sw.loc[(y, "ba"), "worker_share"] for y in yrs])),   # noqa: E731
                      "theta": float(np.mean([sw.loc[(y, "ba"), "income_share"] for y in yrs]))}
    nat = geos[-1][1]
    others_w = np.array([float(nat[f"E_{k}"].iloc[0]) for k in ("lths", "hs", "sc")] + [float(nat["E_baplus"].iloc[0])])
    ctx = {"cry_joint": cry_joint,
           "shares": {"sc_cry": {"s": s_cry, "theta": float(theta_cry), "earnings_ratio_2024": float(rel)},
                      "ba_1980_90": ba((1980, 1990)), "ba_2000": ba((2000,))},
           "weights": {"1980-1990": (ws(1980, "income_share") + ws(1990, "income_share")) / 2,
                       "1990": ws(1990, "income_share"), "1980": ws(1980, "income_share"),
                       "2024 others": others_w / others_w.sum()},
           "gr_bbar": {}, "gr_pbar": {}}
    for _, m in geos:
        pw = m["group_persons"] + m["other_persons"]
        keep = ~m.index.astype(str).str.startswith("nonCBSA")
        ctx["gr_bbar"][id(m)] = float((m["ba25_with"] * pw)[keep].sum() / pw[keep].sum())
        ctx["gr_pbar"][id(m)] = float((m["lnpop_with"] * pw)[keep].sum() / pw[keep].sum())
    return ctx


def geographies(wide, nat_table, cry_joint):
    cz = A.measures(A.cz_areas(wide))
    cb_raw, names, land = A.cbsa_areas(wide)
    cb = A.measures(cb_raw, land)
    nat = A.measures(A.national_area(wide))
    for m in (cz, cb, nat):
        m["E_all"] = m["other_earnings"]
    geos = (("CZ 1990", cz), ("CBSA 2023", cb), ("national", nat))
    return geos, context(nat_table, cry_joint, geos), cb, names


def delta_rows(union_wide, white_wide_, nat_table, cry_joint):
    """Replacement delta (gain_white - gain_union) with its own delta-method interval: both gains move with the same
    parameter draw, so the interval of the difference is not the two intervals combined."""
    gu, cu, _, _ = geographies(union_wide, nat_table, cry_joint)
    gw, cw, _, _ = geographies(white_wide_, nat_table, cry_joint)
    rows = []
    for (geo, mu), (_, mw) in zip(gu, gw):
        single = {s[0]: s for s in A.scale_specs(cu) + A.comp_specs(cu)}
        single_w = {s[0]: s for s in A.scale_specs(cw) + A.comp_specs(cw)}
        joint = {s[0]: s for s in A.joint_specs(cu)}
        joint_w = {s[0]: s for s in A.joint_specs(cw)}
        for name in single:
            _, _, params, fu, _, _ = single[name]
            fw = single_w[name][3]
            # "2024 others" Moretti weights differ by scenario: the white run keeps its own point value
            off = np.array([q[0] for q in single_w[name][2]]) - np.array([q[0] for q in params])
            f = lambda p, fu=fu, fw=fw, off=off: tuple(np.subtract(A.gain_parts(mw, fw(mw, np.asarray(p) + off)),  # noqa: E731
                                                                   A.gain_parts(mu, fu(mu, p))))
            c, rec, lo, hi, sd = A.delta_ci(f, params)
            has = any(q[1] is not None for q in params)
            rows.append({"geography": geo, "spec": name, "delta_cost_bn": c / 1e9, "delta_low_bn": lo / 1e9 if has else np.nan,
                         "delta_high_bn": hi / 1e9 if has else np.nan, "delta_receipts_bn": rec / 1e9})
        for name in joint:
            _, params, cov, fu, _ = joint[name]
            fw = joint_w[name][3]
            if any(abs(a[0] - b[0]) > 0 for a, b in zip(params, joint_w[name][1])):
                raise SystemExit(f"[BLOCKED] joint parameters differ by scenario: {name}")
            f = lambda p, fu=fu, fw=fw: tuple(np.subtract(A.gain_parts(mw, fw(mw, p)), A.gain_parts(mu, fu(mu, p))))  # noqa: E731
            c, rec, lo, hi, sd = A.delta_ci(f, params, cov)
            rows.append({"geography": geo, "spec": name, "delta_cost_bn": c / 1e9, "delta_low_bn": lo / 1e9,
                         "delta_high_bn": hi / 1e9, "delta_receipts_bn": rec / 1e9})
    return pd.DataFrame(rows)


def evaluate_all(wide, nat_table, cry_joint, group):
    cz = A.measures(A.cz_areas(wide))
    cb_raw, names, land = A.cbsa_areas(wide)
    cb = A.measures(cb_raw, land)
    nat = A.measures(A.national_area(wide))
    for m in (cz, cb, nat):
        m["E_all"] = m["other_earnings"]
    geos = (("CZ 1990", cz), ("CBSA 2023", cb), ("national", nat))
    ctx = context(nat_table, cry_joint, geos)
    rows = []
    for geo, m in geos:
        rows += A.evaluate(A.scale_specs(ctx), m, geo, "scale")
        rows += A.evaluate(A.comp_specs(ctx), m, geo, "composition")
        rows += [{**r, "channel": "joint"} for r in A.evaluate_joint(A.joint_specs(ctx), m, geo)]
    for variant in ("by_education", "full_sample"):
        params, fn = A.rs_spec(cb, variant)
        rows += [{**r, "channel": "joint"} for r in A.evaluate_joint(
            [(f"Rosenthal-Strange rings, OLS, {variant.replace('_', ' ')}, uniform within CBSA", params, None, fn,
              "R&S 2008 Table 4 OLS; SE = coef / t; independence")], cb, "CBSA 2023")]
    df = pd.DataFrame(rows)
    df.insert(0, "group", group)
    checks = {k: float(nat[k].iloc[0]) for k in ("s_persons", "s_workers", "s_ba_workers", "dSC", "dBA", "dYRS",
                                                   "dCOLLY", "dHSY", "dIPCOLL", "dIPHS", "dBA25", "other_earnings")}
    checks["earnings_weighted_s_workers_cz"] = float((cz["s_workers"] * cz["other_earnings"]).sum() / cz["other_earnings"].sum())
    top = cb.assign(name=cb.index.map(lambda a: names.get(a, a))).sort_values("group_persons", ascending=False)
    checks["top_cbsas_by_group_persons"] = {str(r.name): round(float(r.s_persons), 4) for _, r in top.head(8).iterrows()}
    return df, checks


def innovation(y, adults, persons, other_earn):
    """The spillover lane's BCHTT transport (arms.innovation) at a given schooling and group size."""
    removed = A.BCHTT["structural_pop_share_of_growth"] * (A.US_POP_2010 - A.US_POP_1965)
    base = A.BCHTT["structural_wage_gain"] * persons / removed
    rows = []
    for out, lvl, slope in (("patents", "pat_level", "pat_x_years"), ("wages", "wage_level", "wage_x_years")):
        a, sa = A.BCHTT[lvl]
        b, sb = A.BCHTT[slope]
        e = a + b * (y - A.BCHTT["mean_years"])
        s = np.sqrt(sa ** 2 + ((y - A.BCHTT["mean_years"]) * sb) ** 2)
        r, lo, hi = e / a, (e - A.Z95 * s) / a, (e + A.Z95 * s) / a
        rows.append({"outcome": out, "mean_years_25plus": y, "adults25": adults, "persons": persons,
                     "ratio_to_average_migrant": r, "ratio_low": lo, "ratio_high": hi,
                     "structural_share_of_E_average_migrant": base, "gain_bn": base * r * other_earn / 1e9,
                     "gain_low_bn": base * lo * other_earn / 1e9, "gain_high_bn": base * hi * other_earn / 1e9})
    return rows


def main():
    cry_table, cry_joint, _ = A.cry_regressions()
    nat_table = pd.read_csv(SPILL / "derived/pums_national.csv")
    union, u_checks = evaluate_all(A.load_cells(), nat_table, cry_joint, "union")
    ref = pd.read_csv(SPILL / "derived/joint_grid.csv")
    for geo in ("CZ 1990", "CBSA 2023", "national"):
        mine = union[(union.channel == "joint") & (union.geography == geo) & (union.spec == CENTRAL_JOINT)].gain_bn.iloc[0]
        theirs = ref[(ref.geography == geo) & (ref.spec == CENTRAL_JOINT)].gain_bn.iloc[0]
        if abs(mine - theirs) > 1e-6:
            raise SystemExit(f"[BLOCKED] union central joint {geo}: {mine} vs the spillover lane's {theirs}")
    print("[gate] the union's central joint estimate reproduces the spillover lane on all three geographies")
    wide, k, wsum = white_wide()
    white, w_checks = evaluate_all(wide, nat_table, cry_joint, "us_born_nh_white")
    grid = pd.concat([union, white], ignore_index=True)
    grid["per_group_member"] = grid["gain_bn"] * 1e9 / A.CPS_UNION
    grid.to_csv(DER / "spill_grid.csv", index=False, lineterminator="\n", float_format="%.6f")
    key = ["channel", "geography", "spec"]
    both = union[key + ["gain_bn", "gain_low_bn", "gain_high_bn", "induced_receipts_bn"]].merge(
        white[key + ["gain_bn", "gain_low_bn", "gain_high_bn", "induced_receipts_bn"]], on=key,
        suffixes=("_union", "_white"))
    both["replacement_delta_cost_bn"] = both["gain_bn_white"] - both["gain_bn_union"]
    dl = delta_rows(A.load_cells(), wide, nat_table, cry_joint)
    both = both.merge(dl, on=["geography", "spec"], how="left")
    if not np.allclose(both.dropna(subset=["delta_cost_bn"]).delta_cost_bn,
                       both.dropna(subset=["delta_cost_bn"]).replacement_delta_cost_bn, atol=1e-6):
        bad = both[(both.delta_cost_bn - both.replacement_delta_cost_bn).abs() > 1e-6]
        print(bad[["channel", "geography", "spec", "delta_cost_bn", "replacement_delta_cost_bn"]].to_string())
        raise SystemExit("[BLOCKED] the delta-method centrals differ from the gain differences")
    both.to_csv(DER / "spill_summary.csv", index=False, lineterminator="\n", float_format="%.6f")
    y = float(wsum["adults25_yrs"] / wsum["adults25"])
    inn = pd.DataFrame(innovation(y, float(wsum["adults25"]) * k, A.CPS_UNION, w_checks["other_earnings"]))
    inn.insert(0, "group", "us_born_nh_white")
    inn.to_csv(DER / "spill_innovation.csv", index=False, lineterminator="\n", float_format="%.6f")
    checks = {"acs_white_persons": float(wsum["persons"]), "scale_to_cps_union": k, "white_mean_years_25plus": y,
              "white_some_college_share_of_workers": float((wsum.workers_sc + wsum.workers_ba + wsum.workers_grad) / wsum.workers),
              "white_ba_share_of_workers": float((wsum.workers_ba + wsum.workers_grad) / wsum.workers),
              "union": u_checks, "us_born_nh_white": w_checks}
    (DER / "spill_checks.json").write_text(json.dumps(checks, indent=1, sort_keys=True) + "\n")
    pd.set_option("display.width", 250)
    pd.set_option("display.max_colwidth", 95)
    show = both[both.geography == "CZ 1990"]
    print(show[["channel", "spec", "gain_bn_union", "gain_bn_white", "gain_low_bn_white", "gain_high_bn_white",
                "replacement_delta_cost_bn", "delta_low_bn", "delta_high_bn"]].round(1).to_string(index=False))
    print(inn.round(3).to_string(index=False))
    print(json.dumps({k: v for k, v in checks.items() if not isinstance(v, dict)}, indent=1))


if __name__ == "__main__":
    main()
