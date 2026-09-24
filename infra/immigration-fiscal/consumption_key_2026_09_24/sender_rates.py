"""Household remittance-sender rates by householder nativity and generation, CPS Unbanked/Underbanked
supplements 2011-2019 (Census API pulls from sender_pull.py).

Measures (item wording quoted in RESULT.md from the Census technical documentation):
  any12      2015, 2017: HES130 sent money to family/friends outside the US in the last 12 months (any channel)
  nonbank12  2011, 2013: HES21 (via HES20) went to a place other than a bank to send money abroad, past 12 months
             2015: HES130=1 & HES133=1; 2017: HES130=1 & HES1352=1; 2019: HENBRM10 (non-bank service)
Unit: household; groups by the householder (reference person, PERRP 1/2); weight HHSUPWGT.
SEs: Census GVF for percentages, s = sqrt(b/x * p(100-p)), x = weighted base, b from each year's
technical documentation Table 4/8 ("Banked" column; Hispanic b for Mexican-origin groups, All b
otherwise); plus a Kish effective-n binomial SE for comparison (ignores clustering).

Run from the repository root:
    OPENBLAS_NUM_THREADS=1 uv run --no-project --with pandas python3 \
        infra/immigration-fiscal/consumption_key_2026_09_24/sender_rates.py
Writes derived/sender_rates.csv, derived/sender_rates_pooled.csv and derived/sender_person_level.csv.
"""
import json
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
RAW = HERE / "_cache" / "senders"
DERIVED = HERE / "derived"
GVF_B = {  # (All, Hispanic) household b parameters, Banked column
    2011: (3560, 3809), 2013: (4742, 5544), 2015: (5650, 6092), 2017: (5358, 6160), 2019: (6093, 6589),
}
GROUPS = ["mexico_born", "us_born_mex_parent_G2", "us_born_mex_origin_G3plus",
          "other_foreign_born", "other_native", "ALL"]
SCOPES = ("all_households", "no_foreign_born_member", "with_foreign_born_member", "no_mexico_born_member")


def load(year: int) -> pd.DataFrame:
    rows = json.loads((RAW / f"unbank_{year}.json").read_text())
    df = pd.DataFrame(rows[1:], columns=rows[0])
    for c in df.columns:
        if c not in ("HRHHID", "HRHHID2"):
            df[c] = pd.to_numeric(df[c], errors="coerce")
    df["hh"] = df["HRHHID"].astype(str) + "_" + df["HRHHID2"].astype(str)
    return df


def techdoc_counts(df: pd.DataFrame, year: int) -> dict:
    col = {2011: "HES22", 2013: "HES20", 2015: "HES130", 2017: "HES130", 2019: "HENBRM10"}[year]
    return {f"{col}={k}": int((df[col] == k).sum()) for k in (1, 2)}


def household_item(df: pd.DataFrame, col: str) -> pd.Series:
    """Household value = the valid (1/2) value carried on member records; checks consistency."""
    v = df.loc[df[col].isin([1, 2]), ["hh", col]]
    nuniq = v.groupby("hh")[col].nunique()
    if (nuniq > 1).any():
        raise SystemExit(f"[BLOCKED] {col}: {int((nuniq > 1).sum())} households with conflicting values")
    return v.groupby("hh")[col].first()


def build(year: int):
    df = load(year)
    df["fb"] = df["PRCITSHP"].isin([4, 5])
    df["mxb"] = df["PENATVTY"] == 303
    hhflags = df.groupby("hh").agg(any_fb=("fb", "any"), any_mxb=("mxb", "any"), size=("PULINENO", "size"))
    ref = df[df["PERRP"].isin([1, 2])].drop_duplicates("hh").set_index("hh")
    h = ref.join(hhflags)
    usb = h["PENATVTY"] == 57
    mx_parent = (h["PEFNTVTY"] == 303) | (h["PEMNTVTY"] == 303)
    both_us = (h["PEFNTVTY"] == 57) & (h["PEMNTVTY"] == 57)
    mex_origin = h["PRDTHSP"] == 1
    grp = pd.Series("other_native", index=h.index)
    grp[h["PRCITSHP"].isin([4, 5])] = "other_foreign_born"
    grp[h["PENATVTY"] == 303] = "mexico_born"
    grp[usb & mx_parent] = "us_born_mex_parent_G2"
    grp[usb & both_us & mex_origin] = "us_born_mex_origin_G3plus"
    h["grp"] = grp
    if year in (2011, 2013):
        e = household_item(df, "HES20")
        p12 = household_item(df, "HES21")
        nb = pd.Series(np.nan, index=e.index)
        nb[e == 2] = 0
        both = e[e == 1].index.intersection(p12.index)
        nb[both] = (p12[both] == 1).astype(float)
        h["nonbank12"] = nb.reindex(h.index)
    if year in (2015, 2017):
        a = household_item(df, "HES130")
        h["any12"] = (a == 1).astype(float).reindex(h.index)
        nbcol = "HES133" if year == 2015 else "HES1352"
        nbi = household_item(df, nbcol)
        nb = pd.Series(np.nan, index=a.index)
        nb[a == 2] = 0
        s = a[a == 1].index.intersection(nbi.index)
        nb[s] = (nbi[s] == 1).astype(float)
        h["nonbank12"] = nb.reindex(h.index)
    if year == 2019:
        a = household_item(df, "HENBRM10")
        h["nonbank12"] = (a == 1).astype(float).reindex(h.index)
    h["year"] = year
    return h, techdoc_counts(df, year), len(df)


def rate(sub: pd.DataFrame, meas: str, b: int) -> dict:
    s = sub[sub[meas].notna() & (sub["HHSUPWGT"] > 0)]
    w = s["HHSUPWGT"].to_numpy(float)
    y = s[meas].to_numpy(float)
    n = len(s)
    if n == 0:
        return {"n": 0}
    p = float((w * y).sum() / w.sum())
    x = float(w.sum())
    se_gvf = float(np.sqrt(b / x * (100 * p) * (100 - 100 * p)) / 100)
    neff = w.sum() ** 2 / (w ** 2).sum()
    se_kish = float(np.sqrt(p * (1 - p) / neff))
    return {"n": n, "n_yes": int(y.sum()), "wt_households_m": x / 1e6, "rate": p,
            "se_gvf": se_gvf, "se_kish_binomial": se_kish}


def scoped(h: pd.DataFrame, g: str, scope: str) -> pd.DataFrame | None:
    sub = h if g == "ALL" else h[h["grp"] == g]
    if scope == "all_households":
        return sub
    if g in ("mexico_born", "other_foreign_born"):
        return None
    if scope == "no_foreign_born_member":
        return sub[~sub["any_fb"]]
    if scope == "with_foreign_born_member":
        return sub[sub["any_fb"]]
    return sub[~sub["any_mxb"]]


def rates(built: dict) -> pd.DataFrame:
    out = []
    for year, (h, counts, nrec) in built.items():
        print(f"== {year}: person records {nrec}, householders {len(h)}, techdoc-check counts {counts}")
        b_all, b_hisp = GVF_B[year]
        for meas in ("any12", "nonbank12"):
            if meas not in h:
                continue
            for g in GROUPS:
                for scope in SCOPES:
                    sub = scoped(h, g, scope)
                    if sub is None:
                        continue
                    b = b_hisp if g.startswith(("mexico", "us_born_mex")) else b_all
                    out.append({"year": year, "measure": meas, "group": g, "scope": scope, **rate(sub, meas, b)})
    return pd.DataFrame(out)


def pooled(res: pd.DataFrame) -> pd.DataFrame:
    """Pooled 2015+2017 any-channel household rate: mean of the two years' weighted rates.

    June 2015 and June 2017 samples are disjoint under the CPS 4-8-4 rotation, so the SE of the mean
    is sqrt(se15^2 + se17^2)/2.
    """
    pool = []
    for g in GROUPS:
        for scope in SCOPES:
            r = res[(res.measure == "any12") & (res.group == g) & (res.scope == scope) & res.year.isin([2015, 2017])]
            if len(r) != 2:
                continue
            p = r["rate"].mean()
            se = np.sqrt((r["se_gvf"] ** 2).sum()) / 2
            pool.append({"group": g, "scope": scope, "n": int(r["n"].sum()), "n_yes": int(r["n_yes"].sum()),
                         "wt_households_m_mean": round(float(r["wt_households_m"].mean()), 4),
                         "rate_pct": round(100 * p, 2), "se_gvf_pct": round(100 * se, 2)})
    return pd.DataFrame(pool)


def controls(built: dict) -> pd.DataFrame:
    """Nonbank remittance use against FDIC 2019 report Tables 6.1/6.3 (2015, 2017, 2019)."""
    ctrl = []
    for y in (2015, 2017, 2019):
        h = built[y][0]
        cuts = {
            "All": h.index == h.index,
            "US-born (native, PRCITSHP 1-3)": h["PRCITSHP"].isin([1, 2, 3]).to_numpy(),
            "Foreign-born citizen": (h["PRCITSHP"] == 4).to_numpy(),
            "Foreign-born noncitizen": (h["PRCITSHP"] == 5).to_numpy(),
            "Hispanic": (h["PEHSPNON"] == 1).to_numpy(),
        }
        for name, m in cuts.items():
            r = rate(h[m], "nonbank12", GVF_B[y][1] if name == "Hispanic" else GVF_B[y][0])
            ctrl.append({"year": y, "cut": name, "n": r["n"], "rate_pct": round(100 * r["rate"], 2)})
    return pd.DataFrame(ctrl).pivot(index="cut", columns="year", values="rate_pct")


def person_level() -> pd.DataFrame:
    """Adults 18+ by own generation: share living in a household that sent (any channel)."""
    pers = []
    for y in (2015, 2017):
        df = load(y)
        df["fb"] = df["PRCITSHP"].isin([4, 5])
        anyfb = df.groupby("hh")["fb"].any()
        a = household_item(df, "HES130")
        df["send"] = df["hh"].map((a == 1).astype(float))
        df["hh_anyfb"] = df["hh"].map(anyfb)
        usb = df["PENATVTY"] == 57
        g = pd.Series("other_native", index=df.index)
        g[df["PRCITSHP"].isin([4, 5])] = "other_foreign_born"
        g[df["PENATVTY"] == 303] = "mexico_born"
        g[usb & ((df["PEFNTVTY"] == 303) | (df["PEMNTVTY"] == 303))] = "us_born_mex_parent_G2"
        g[usb & (df["PEFNTVTY"] == 57) & (df["PEMNTVTY"] == 57) & (df["PRDTHSP"] == 1)] = "us_born_mex_origin_G3plus"
        df["grp"] = g
        ad = df[(df["PRTAGE"] >= 18) & df["send"].notna() & (df["PWSUPWGT"] > 0)]
        for grp_name in GROUPS[:-1]:
            for scope in ("all", "no_foreign_born_member"):
                s = ad[ad["grp"] == grp_name]
                if scope != "all":
                    if grp_name in ("mexico_born", "other_foreign_born"):
                        continue
                    s = s[~s["hh_anyfb"]]
                w = s["PWSUPWGT"].to_numpy(float)
                p = float((w * s["send"]).sum() / w.sum())
                neff = w.sum() ** 2 / (w ** 2).sum()
                pers.append({"year": y, "group": grp_name, "scope": scope, "n_adults": len(s),
                             "n_households": s["hh"].nunique(), "share_pct": round(100 * p, 2),
                             "se_kish_pct": round(100 * np.sqrt(p * (1 - p) / neff), 2)})
    return pd.DataFrame(pers)


def main() -> None:
    DERIVED.mkdir(exist_ok=True)
    built = {y: build(y) for y in (2011, 2013, 2015, 2017, 2019)}
    res = rates(built)
    res.to_csv(DERIVED / "sender_rates.csv", index=False, lineterminator="\n")
    pd.set_option("display.width", 200)
    show = res[res["scope"] == "all_households"].copy()
    for c in ("rate", "se_gvf", "se_kish_binomial"):
        show[c] = (100 * show[c]).round(2)
    show["wt_households_m"] = show["wt_households_m"].round(2)
    print(show.to_string(index=False))
    print("\n-- control cuts (nonbank12): FDIC 2019 report Table 6.1 publishes 2017/2019 --")
    print(controls(built).to_string())
    pool = pooled(res)
    pool.to_csv(DERIVED / "sender_rates_pooled.csv", index=False, lineterminator="\n")
    print("\n-- pooled 2015+2017 any-channel household rate --")
    print(pool.to_string(index=False))
    pers = person_level()
    pers.to_csv(DERIVED / "sender_person_level.csv", index=False, lineterminator="\n")
    print("\n-- person level: adults 18+ by own generation, share living in a sending household --")
    print(pers.to_string(index=False))


if __name__ == "__main__":
    main()
