"""State-level net domestic migration of taxpayers against Mexican-origin concentration.

Sources
  IRS SOI state migration, tax-year pairs 2011-12 .. 2022-23 (`derived/soi_state_agi.csv`,
  built by `build_soi_panel.py`). Outcome variables are built from returns (n1),
  exemptions (n2, a person count) and AGI in $thousands.
  ACS 1-year state covariates (`_cache/state_covariates.csv`).
  ITEP "Who Pays?" 2024 effective state+local tax rate on the top 1% of taxpayers
  (`$IMMIGRATION_FISCAL_ROOT/data/itep/itep_table_5.tsv`, column 4).

Outcomes (per 100 of the state's non-migrant base, so a positive number is net OUTflow)
  net_out_all   (outflow_n2_0 - inflow_n2_0) / nonmig_n2_0 * 100
  net_out_top   (outflow_n1_7 - inflow_n1_7) / nonmig_n1_7 * 100   AGI >= $200k
  net_agi       (outflow_y1_agi_0 - inflow_y2_agi_0) / nonmig_y1_agi_0 * 100

Exposure  Mexican-origin share of population, B03001_004 / B01003_001, in percent.
Disconfirmation exposures: Asian-alone share, Cuban-origin share, and the ITEP top-1%
tax rate entered on its own.

All specifications carry year fixed effects (the SOI AGI brackets are nominal and
unindexed, so the $200k+ group grows mechanically over the panel) and cluster standard
errors on state.

Output: derived/state_panel.csv, derived/state_estimates.csv
"""
import os, re
import numpy as np
import pandas as pd
import statsmodels.api as sm

HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(HERE, "_cache")
DERIVED = os.path.join(HERE, "derived")
os.makedirs(DERIVED, exist_ok=True)
ITEP = os.path.join(os.environ.get("IMMIGRATION_FISCAL_ROOT",
                                   os.path.expanduser("~/research-data/immigration-fiscal")),
                    "data", "itep", "itep_table_5.tsv")

REGION = {
    "CT": "NE", "ME": "NE", "MA": "NE", "NH": "NE", "RI": "NE", "VT": "NE",
    "NJ": "NE", "NY": "NE", "PA": "NE",
    "IL": "MW", "IN": "MW", "MI": "MW", "OH": "MW", "WI": "MW", "IA": "MW",
    "KS": "MW", "MN": "MW", "MO": "MW", "NE": "MW", "ND": "MW", "SD": "MW",
    "DE": "S", "DC": "S", "FL": "S", "GA": "S", "MD": "S", "NC": "S", "SC": "S",
    "VA": "S", "WV": "S", "AL": "S", "KY": "S", "MS": "S", "TN": "S",
    "AR": "S", "LA": "S", "OK": "S", "TX": "S",
    "AZ": "W", "CO": "W", "ID": "W", "MT": "W", "NV": "W", "NM": "W", "UT": "W",
    "WY": "W", "AK": "W", "CA": "W", "HI": "W", "OR": "W", "WA": "W",
}
ABBR = {  # state FIPS -> USPS
    "01": "AL", "02": "AK", "04": "AZ", "05": "AR", "06": "CA", "08": "CO", "09": "CT",
    "10": "DE", "11": "DC", "12": "FL", "13": "GA", "15": "HI", "16": "ID", "17": "IL",
    "18": "IN", "19": "IA", "20": "KS", "21": "KY", "22": "LA", "23": "ME", "24": "MD",
    "25": "MA", "26": "MI", "27": "MN", "28": "MS", "29": "MO", "30": "MT", "31": "NE",
    "32": "NV", "33": "NH", "34": "NJ", "35": "NM", "36": "NY", "37": "NC", "38": "ND",
    "39": "OH", "40": "OK", "41": "OR", "42": "PA", "44": "RI", "45": "SC", "46": "SD",
    "47": "TN", "48": "TX", "49": "UT", "50": "VT", "51": "VA", "53": "WA", "54": "WV",
    "55": "WI", "56": "WY",
}
GAP_GROUP = {"CA": "CA", "TX": "TX"}
SW_IL = {"AZ", "CO", "IL", "NV", "NM"}


def itep_top1():
    rows = {}
    with open(ITEP) as f:
        for line in f:
            p = line.rstrip("\n").split("\t")
            if len(p) < 4:
                continue
            m = re.match(r"^([A-Za-z .]+)$", p[0].strip())
            v = re.match(r"^([\d.]+)%$", p[3].strip())
            if m and v:
                rows[m.group(1).strip()] = float(v.group(1))
    return rows


NAME2AB = {
    "Alabama": "AL", "Alaska": "AK", "Arizona": "AZ", "Arkansas": "AR", "California": "CA",
    "Colorado": "CO", "Connecticut": "CT", "Delaware": "DE", "District of Columbia": "DC",
    "Florida": "FL", "Georgia": "GA", "Hawaii": "HI", "Idaho": "ID", "Illinois": "IL",
    "Indiana": "IN", "Iowa": "IA", "Kansas": "KS", "Kentucky": "KY", "Louisiana": "LA",
    "Maine": "ME", "Maryland": "MD", "Massachusetts": "MA", "Michigan": "MI",
    "Minnesota": "MN", "Mississippi": "MS", "Missouri": "MO", "Montana": "MT",
    "Nebraska": "NE", "Nevada": "NV", "New Hampshire": "NH", "New Jersey": "NJ",
    "New Mexico": "NM", "New York": "NY", "North Carolina": "NC", "North Dakota": "ND",
    "Ohio": "OH", "Oklahoma": "OK", "Oregon": "OR", "Pennsylvania": "PA",
    "Rhode Island": "RI", "South Carolina": "SC", "South Dakota": "SD",
    "Tennessee": "TN", "Texas": "TX", "Utah": "UT", "Vermont": "VT", "Virginia": "VA",
    "Washington": "WA", "West Virginia": "WV", "Wisconsin": "WI", "Wyoming": "WY",
}


def build():
    soi = pd.read_csv(os.path.join(DERIVED, "soi_state_agi.csv"), dtype={"statefips": str})
    soi["statefips"] = soi["statefips"].str.zfill(2)
    soi = soi[soi.statefips.isin(ABBR)]
    # IRS ships an incomplete 2014-15 inmigall file (14 states, Alaska through Illinois),
    # so that pair is dropped from every bracket-based series.
    cov = soi.groupby("pair")["statefips"].nunique()
    soi = soi[soi.pair.isin(cov[cov >= 51].index)]
    tot = soi[soi.agi_stub == 0].set_index(["statefips", "year2"])
    top = soi[soi.agi_stub == 7].set_index(["statefips", "year2"])
    p = pd.DataFrame(index=tot.index)
    p["net_out_all"] = (tot.outflow_n2_0 - tot.inflow_n2_0) / tot.nonmig_n2_0 * 100
    p["net_out_ret"] = (tot.outflow_n1_0 - tot.inflow_n1_0) / tot.nonmig_n1_0 * 100
    p["net_agi"] = (tot.outflow_y1_agi_0 - tot.inflow_y2_agi_0) / tot.nonmig_y1_agi_0 * 100
    p["net_out_top"] = ((top.outflow_n1_0 - top.inflow_n1_0) / top.nonmig_n1_0 * 100)
    p["net_agi_top"] = ((top.outflow_y1_agi_0 - top.inflow_y2_agi_0)
                        / top.nonmig_y1_agi_0 * 100)
    p["out_agi_$k"] = tot.outflow_y1_agi_0
    p["in_agi_$k"] = tot.inflow_y2_agi_0
    p["out_agi_top_$k"] = top.outflow_y1_agi_0
    p["in_agi_top_$k"] = top.inflow_y2_agi_0
    p = p.reset_index().rename(columns={"year2": "year"})
    p["st"] = p.statefips.map(ABBR)

    tot = pd.read_csv(os.path.join(DERIVED, "soi_state_totals.csv"),
                      dtype={"statefips": str})
    tot["statefips"] = tot["statefips"].str.zfill(2)
    tot["st"] = tot.statefips.map(ABBR)
    tot["net_out_all_pairfile"] = (tot.n2_out - tot.n2_in) / tot.n2_in * 100
    tot["net_agi_pairfile_bn"] = (tot.agi_out - tot.agi_in) / 1e6
    p = p.merge(tot[["st", "year2", "net_out_all_pairfile", "net_agi_pairfile_bn"]]
                .rename(columns={"year2": "year"}), on=["st", "year"], how="outer")

    cov = pd.read_csv(os.path.join(CACHE, "state_covariates.csv"))
    for c in [c for c in cov.columns if c.startswith("B")]:
        cov[c] = pd.to_numeric(cov[c], errors="coerce")
        cov.loc[cov[c] < 0, c] = np.nan
    cov["st"] = cov["NAME"].map(NAME2AB)
    cov["mex_share"] = cov.B03001_004E / cov.B01003_001E * 100
    cov["cuban_share"] = cov.B03001_006E / cov.B01003_001E * 100
    cov["asian_share"] = cov.B02001_005E / cov.B01003_001E * 100
    cov["fb_share"] = cov.B05002_013E / cov.B05002_001E * 100
    cov["coll"] = (cov[["B15003_022E", "B15003_023E", "B15003_024E",
                        "B15003_025E"]].sum(axis=1) / cov.B15003_001E * 100)
    cov["lpop"] = np.log(cov.B01003_001E)
    cov["rent"] = cov.B25064_001E
    cov["hhinc"] = cov.B19013_001E
    keep = ["st", "year", "mex_share", "cuban_share", "asian_share", "fb_share",
            "coll", "lpop", "rent", "hhinc"]
    cov = cov[keep].dropna(subset=["st"])
    # ACS has no 2020 1-year file: carry 2019 forward for the 2019-20 SOI pair
    c2020 = cov[cov.year == 2019].copy()
    c2020["year"] = 2020
    cov = pd.concat([cov, c2020], ignore_index=True)

    p = p.merge(cov, on=["st", "year"], how="left")
    p["region"] = p["st"].map(REGION)
    p["gap_group"] = np.where(p.st == "CA", "CA",
                     np.where(p.st == "TX", "TX",
                     np.where(p.st.isin(SW_IL), "SW_IL", "rest")))
    mob = mobility()
    p = p.merge(mob, on=["st", "year"], how="left")
    top1 = itep_top1()
    p["tax_top1"] = p["st"].map({NAME2AB[k]: v for k, v in top1.items() if k in NAME2AB})
    return p


def mobility():
    """ACS state in/out interstate flows by nativity (B07007/B07407) and by income
    (B07010/B07410). `_022E` is the native line of "moved from different state";
    `_055E` is the $75,000-or-more income line of the same row. The 1-year-ago
    universe (B07407/B07410) counts people who LEFT the state, so out-minus-in is net
    domestic outflow."""
    f = {}
    for g in ["B07007", "B07407", "B07010", "B07410"]:
        fp = os.path.join(CACHE, "mobility_%s.csv" % g)
        if not os.path.exists(fp):
            print("[WARN] missing %s; its columns will be NaN" % fp)
            continue
        d = pd.read_csv(fp)
        d["st"] = d["NAME"].map(NAME2AB)
        for c in d.columns:
            if c.startswith("B"):
                d[c] = pd.to_numeric(d[c], errors="coerce")
                d.loc[d[c] < 0, c] = np.nan
        f[g] = d.dropna(subset=["st"]).set_index(["st", "year"])
    if "B07007" not in f:
        raise SystemExit("B07007 is required")
    out = pd.DataFrame(index=f["B07007"].index)

    def col(g, v):
        return f[g][v] if g in f else np.nan

    out["native_pop"] = f["B07007"]["B07007_002E"]
    out["native_in"] = f["B07007"]["B07007_022E"]
    out["native_out"] = col("B07407", "B07407_022E")
    out["fb_in"] = f["B07007"]["B07007_023E"]
    out["fb_out"] = col("B07407", "B07407_023E")
    out["all_in"] = f["B07007"]["B07007_021E"]
    out["all_out"] = col("B07407", "B07407_021E")
    out["hi_in"] = col("B07010", "B07010_055E")
    out["hi_out"] = col("B07410", "B07410_055E")
    out["mover_base"] = col("B07010", "B07010_001E")
    out["net_out_native_acs"] = (out.native_out - out.native_in) / out.native_pop * 100
    out["net_out_fb_acs"] = (out.fb_out - out.fb_in) / out.native_pop * 100
    out["net_out_hi_acs"] = (out.hi_out - out.hi_in) / out.mover_base * 100
    return out.reset_index()


def cluster_ols(df, y, x, ctrl, yearfe=True):
    cols = [y, x] + ctrl
    d = df[cols + ["st", "year"]].dropna()
    if len(d) < 20 or d[x].std() == 0:
        return dict(y=y, x=x, ctrl="+".join(ctrl) if ctrl else "none", n=len(d),
                    coef=np.nan, se=np.nan, lo=np.nan, hi=np.nan)
    X = d[[x] + ctrl].copy()
    if yearfe:
        X = pd.concat([X, pd.get_dummies(d["year"], prefix="y", drop_first=True).astype(float)],
                      axis=1)
    X = sm.add_constant(X, has_constant="add")
    m = sm.OLS(d[y], X).fit(cov_type="cluster", cov_kwds={"groups": d["st"]})
    ci = m.conf_int()
    return dict(y=y, x=x, ctrl="+".join(ctrl) if ctrl else "none", n=len(d),
                coef=m.params[x], se=m.bse[x], lo=ci.loc[x, 0], hi=ci.loc[x, 1])


def main():
    p = build()
    p.to_csv(os.path.join(DERIVED, "state_panel.csv"), index=False)
    print("state-year rows", len(p), "years", sorted(p.year.unique()))

    print("\n=== mean net domestic out-migration by fiscal-gap group (2011-12..latest) ===")
    g = (p.groupby("gap_group")[["net_out_all", "net_out_top", "net_agi", "net_agi_top",
                                 "net_out_native_acs", "net_out_hi_acs"]]
           .mean().round(3))
    print(g.to_string())

    print("\n=== CA and TX by year ===")
    print(p[p.st.isin(["CA", "TX"])][["st", "year", "net_out_all", "net_out_top",
                                      "net_agi", "net_out_native_acs",
                                      "net_out_hi_acs", "mex_share"]]
          .round(3).to_string(index=False))

    rows = []
    specs = [("none", []),
             ("size", ["lpop"]),
             ("size+tax", ["lpop", "tax_top1"]),
             ("size+tax+rent", ["lpop", "tax_top1", "rent"]),
             ("size+tax+rent+coll+inc", ["lpop", "tax_top1", "rent", "coll", "hhinc"])]
    for yv in ["net_out_all", "net_out_top", "net_agi", "net_agi_top",
               "net_out_native_acs", "net_out_hi_acs"]:
        for xv in ["mex_share", "fb_share", "asian_share", "cuban_share", "tax_top1"]:
            for nm, ctrl in specs:
                c = [c for c in ctrl if c != xv]
                rows.append(dict(spec=nm, **cluster_ols(p, yv, xv, c)))
    # region fixed effects arm
    pr = pd.concat([p, pd.get_dummies(p["region"], prefix="rg", drop_first=True).astype(float)],
                   axis=1)
    rgc = [c for c in pr.columns if c.startswith("rg_")]
    for yv in ["net_out_all", "net_out_top", "net_agi", "net_out_native_acs",
               "net_out_hi_acs"]:
        for xv in ["mex_share", "asian_share", "cuban_share"]:
            rows.append(dict(spec="+region", **cluster_ols(
                pr, yv, xv, ["lpop", "tax_top1", "rent", "coll", "hhinc"] + rgc)))
    # within-state arm: state + year fixed effects. The Mexican-origin share moves little
    # inside a state over 12 years, so this is a check on how much of the cross-sectional
    # association is between-state composition, not a preferred specification.
    ps = pd.concat([p, pd.get_dummies(p["st"], prefix="s", drop_first=True).astype(float)],
                   axis=1)
    sfe = [c for c in ps.columns if c.startswith("s_") and c != "s_t"]
    for yv in ["net_out_all", "net_out_top", "net_agi", "net_out_native_acs",
               "net_out_hi_acs"]:
        rows.append(dict(spec="+state FE", **cluster_ols(ps, yv, "mex_share", sfe)))
    est = pd.DataFrame(rows)
    est.to_csv(os.path.join(DERIVED, "state_estimates.csv"), index=False)
    pd.set_option("display.width", 220)
    for yv in est.y.unique():
        print("\n=== %s ===" % yv)
        print(est[est.y == yv][["x", "spec", "n", "coef", "se", "lo", "hi"]]
              .to_string(index=False, float_format=lambda v: "%.4f" % v))


if __name__ == "__main__":
    main()
