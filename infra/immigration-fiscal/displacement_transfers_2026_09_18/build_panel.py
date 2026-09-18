"""Assemble the metro x year aggregate panel and the predetermined base shares.

Two sources are stitched:
  * ACS 1-year summary tables published AT CBSA level, 2005-2024 (_cache/metro/*.json).
    No geographic allocation is needed - the Census Bureau publishes these at the metro
    level directly. CBSA codes are matched across years; a metro that is not present in
    both endpoints of a window simply drops out of that window.
  * Census 2000 SF3 county tables aggregated to the OMB February-2013 CBSA delineation
    (_cache/sf3/*.json). This supplies the 2000 endpoint and the pre-1990 base shares.

Outcome definitions, and what each one's universe is:
  ssi_rate     % of HOUSEHOLDS with any SSI income            (SF3 P063 / ACS B19056)
  pa_rate      % of HOUSEHOLDS with any public assistance      (SF3 P064 / ACS B19057)
  snap_rate    % of HOUSEHOLDS receiving SNAP, 2008+ only      (ACS B22010)
  nc_epop      employment/population, 25-64, below a BA        (ACS B23006)
  nc_lfp       labour force participation, 25-64, below a BA   (ACS B23006)
  col_epop     the same for BA+, the control group             (ACS B23006)
None of these is split by nativity. That is the price of reaching 2000 and 2005-2007, and
it is stated as a limitation rather than papered over: the PUMS lane supplies the
native-only versions for the years it covers.

Treatment: foreign-born and Mexico-born share of the TOTAL metro population, in points.
"""
import json, pathlib
import numpy as np
import pandas as pd

HERE = pathlib.Path(__file__).parent
CACHE = HERE / "_cache"
DERIVED = HERE / "derived"
DERIVED.mkdir(exist_ok=True)

NC_TOT = ["B23006_002E", "B23006_009E", "B23006_016E"]
NC_LF = ["B23006_003E", "B23006_010E", "B23006_017E"]
NC_EMP = ["B23006_004E", "B23006_006E", "B23006_011E", "B23006_013E",
          "B23006_018E", "B23006_020E"]
COL_TOT, COL_LF = ["B23006_023E"], ["B23006_024E"]
COL_EMP = ["B23006_025E", "B23006_027E"]


def load_cbsa():
    d = pd.read_excel(CACHE / "omb_delineation_2013_list1.xls", skiprows=2)
    d = d[d["Metropolitan/Micropolitan Statistical Area"] == "Metropolitan Statistical Area"]
    d = d.dropna(subset=["FIPS State Code", "FIPS County Code"])
    d["cofips"] = (d["FIPS State Code"].astype(int).astype(str).str.zfill(2)
                   + d["FIPS County Code"].astype(int).astype(str).str.zfill(3))
    d["cbsa"] = d["CBSA Code"].astype(str).str.strip()
    return d[["cofips", "cbsa", "CBSA Title"]].rename(columns={"CBSA Title": "cbsa_title"})


def s(rec, cols):
    vals = [rec.get(c) for c in cols]
    if any(v is None for v in vals):
        return np.nan
    return float(sum(vals))


def acs_rows():
    out = []
    for p in sorted((CACHE / "metro").glob("metro_*.json")):
        d = json.loads(p.read_text())
        for cbsa, rec in d.items():
            mex = rec.get(rec["MEXLEAF"])
            out.append({
                "cbsa": str(cbsa), "cbsa_title": rec["NAME"], "year": int(rec["year"]),
                "pop": rec.get("B01003_001E"),
                "pop_nat": rec.get("B05002_001E"),
                "fb": rec.get("B05002_013E"),
                "mex": mex,
                "hh_tot": rec.get("B19056_001E"), "hh_ssi": rec.get("B19056_002E"),
                "hh_tot_pa": rec.get("B19057_001E"), "hh_pa": rec.get("B19057_002E"),
                "hh_tot_snap": rec.get("B22010_001E"), "hh_snap": rec.get("B22010_002E"),
                "nc_tot": s(rec, NC_TOT), "nc_lf": s(rec, NC_LF), "nc_emp": s(rec, NC_EMP),
                "col_tot": s(rec, COL_TOT), "col_lf": s(rec, COL_LF),
                "col_emp": s(rec, COL_EMP),
                "source": "acs",
            })
    return pd.DataFrame(out)


def sf3_rows(cbsa):
    d = {}
    for name in ("p063_ssi", "p064_pa", "p001_pop", "p043_emp", "pct020_pre1990"):
        p = CACHE / "sf3" / f"{name}.json"
        if not p.exists():
            print(f"  [missing] {name}.json - 2000 endpoint incomplete")
            continue
        d[name] = json.loads(p.read_text())
    if "p001_pop" not in d:
        return pd.DataFrame(), pd.DataFrame()
    # The employment_entry lane already pulled PCT019 at county level; reuse it rather
    # than re-hitting a slow API. Format is a list-of-lists with a header row.
    raw = json.loads((HERE.parent / "employment_entry_2026_09_18" / "_cache"
                      / "sf3_2000_county_pob.json").read_text())
    ph = {n: i for i, n in enumerate(raw[0])}
    pob = []
    for r in raw[1:]:
        pob.append({"cofips": r[ph["state"]].zfill(2) + r[ph["county"]].zfill(3),
                    "fb2000": _f(r[ph["PCT019001"]]),
                    "mex2000": _f(r[ph["PCT019103"]]),
                    "pop2000": _f(r[ph["P001001"]])})
    rows = []
    for fips, rec in d["p001_pop"].items():
        r = {"cofips": fips, "pop": rec.get("P001001")}
        if "p063_ssi" in d:
            g = d["p063_ssi"].get(fips, {})
            r["hh_tot"] = g.get("P063001"); r["hh_ssi"] = g.get("P063002")
        if "p064_pa" in d:
            g = d["p064_pa"].get(fips, {})
            r["hh_tot_pa"] = g.get("P064001"); r["hh_pa"] = g.get("P064002")
        if "p043_emp" in d:
            g = d["p043_emp"].get(fips, {})
            # P043: sex by employment status 16+. male total _002, in LF _003,
            # civilian employed _006 + armed forces _005; female block offset by 8.
            r["all_tot"] = _n(g, "P043002") + _n(g, "P043009")
            r["all_lf"] = _n(g, "P043003") + _n(g, "P043010")
            r["all_emp"] = (_n(g, "P043005") + _n(g, "P043006")
                            + _n(g, "P043012") + _n(g, "P043013"))
        rows.append(r)
    co = pd.DataFrame(rows)
    # place of birth 2000 at county level, from the employment_entry lane's cached pull
    pb = pd.DataFrame(pob)
    if not pb.empty:
        co = co.merge(pb, on="cofips", how="left")
    base = pd.DataFrame()
    if "pct020_pre1990" in d:
        spec = json.loads((CACHE / "sf3" / "pct020_pre1990_spec.json").read_text())
        mexcols = spec.get("Americas|Latin America|Central America|Mexico", [])
        allcols = sorted({c for v in spec.values() for c in v})
        brows = []
        for fips, rec in d["pct020_pre1990"].items():
            brows.append({"cofips": fips,
                          "mex_pre90": sum(_n(rec, c) for c in mexcols),
                          "fb_pre90": sum(_n(rec, c) for c in allcols)})
        base = pd.DataFrame(brows)
    j = co.merge(cbsa, on="cofips", how="inner")
    num = [c for c in j.columns if c not in ("cofips", "cbsa", "cbsa_title", "NAME")]
    g = j.groupby(["cbsa", "cbsa_title"], as_index=False)[num].sum(min_count=1)
    g["year"] = 2000; g["source"] = "sf3"
    if not base.empty:
        b = base.merge(cbsa, on="cofips", how="inner")
        base = b.groupby("cbsa", as_index=False)[["mex_pre90", "fb_pre90"]].sum()
    return g, base


def _f(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return np.nan


def _n(rec, key):
    v = rec.get(key)
    try:
        return float(v)
    except (TypeError, ValueError):
        return 0.0


def rates(df):
    df = df.copy()
    df["fb_share"] = 100 * df["fb"] / df["pop"]
    df["mex_share"] = 100 * df["mex"] / df["pop"]
    df["ssi_rate"] = 100 * df["hh_ssi"] / df["hh_tot"]
    df["pa_rate"] = 100 * df["hh_pa"] / df["hh_tot_pa"]
    df["snap_rate"] = 100 * df["hh_snap"] / df["hh_tot_snap"]
    df["nc_epop"] = 100 * df["nc_emp"] / df["nc_tot"]
    df["nc_lfp"] = 100 * df["nc_lf"] / df["nc_tot"]
    df["col_epop"] = 100 * df["col_emp"] / df["col_tot"]
    df["col_lfp"] = 100 * df["col_lf"] / df["col_tot"]
    if "all_emp" in df.columns:
        df["all_epop"] = 100 * df["all_emp"] / df["all_tot"]
        df["all_lfp"] = 100 * df["all_lf"] / df["all_tot"]
    return df


def main():
    cbsa = load_cbsa()
    acs = acs_rows()
    print("ACS metro rows:", len(acs), "years:", sorted(acs.year.unique()))
    sf3, base = sf3_rows(cbsa)
    print("SF3 2000 metro rows:", len(sf3), "base rows:", len(base))
    if not sf3.empty:
        # 2000 place-of-birth columns come from the cached PCT019 pull
        sf3["fb"] = sf3["fb2000"]
        sf3["mex"] = sf3["mex2000"]
        sf3["pop"] = sf3["pop"].fillna(sf3["pop2000"])
        panel = pd.concat([acs, sf3], ignore_index=True)
    else:
        panel = acs
    panel = rates(panel)
    panel.to_csv(DERIVED / "metro_panel.csv", index=False)
    print("wrote metro_panel.csv", panel.shape)
    if not base.empty:
        base["mex_base_share"] = base["mex_pre90"] / base["mex_pre90"].sum()
        base["fb_base_share"] = base["fb_pre90"] / base["fb_pre90"].sum()
        base.to_csv(DERIVED / "base_shares_pre1990.csv", index=False)
        print("wrote base_shares_pre1990.csv", base.shape,
              "natl pre-1990 Mexico stock %.0f" % base["mex_pre90"].sum())


if __name__ == "__main__":
    main()
