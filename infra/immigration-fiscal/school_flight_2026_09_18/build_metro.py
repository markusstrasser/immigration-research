"""Metro x year panel of child school-type shares from the PUMA cells.

PUMA-level weighted counts are allocated to counties by the Geocorr population
allocation factor for the PUMA vintage in force that year, then summed into the fixed
OMB Feb-2013 metropolitan delineation -- the same geography construction as
employment_entry_2026_09_18/build_panel.py, whose crosswalk files are reused.

Groups (mutually exclusive, Hispanic takes precedence over race, as in CCD):
  wnh_nb  US-born non-Hispanic white      bnh_nb  US-born non-Hispanic Black
  anh_nb  US-born non-Hispanic Asian      onh_nb  US-born non-Hispanic other/multi
  hisp_nb US-born Hispanic                hisp_fb foreign-born Hispanic
  nonhisp_fb foreign-born non-Hispanic

Outcome: private share among US-born non-Hispanic white children, priv/(priv+pub).
NOTE: ACS SCH=3 is "private school, private college, OR HOME SCHOOL"; the private
share therefore includes home-schooled children and rises mechanically with the growth
of home schooling. This is flagged in the memo, not corrected.
"""
import pathlib, sys
import pandas as pd

HERE = pathlib.Path(__file__).parent
CACHE = HERE / "_cache"
DERIVED = HERE / "derived"
DERIVED.mkdir(exist_ok=True)

VINTAGE = {y: ("puma2k" if y <= 2011 else "puma12" if y <= 2021 else "puma22")
           for y in range(2005, 2025)}
GROUPS = ["wnh_nb", "bnh_nb", "anh_nb", "onh_nb", "hisp_nb", "hisp_fb", "nonhisp_fb"]


def load_xwalks():
    out = {}
    for v in ("puma2k", "puma12", "puma22"):
        df = pd.read_csv(CACHE / f"xwalk_{v}.csv", dtype=str)
        pc = [c for c in df.columns if c.lower().startswith("puma")][0]
        df = df.rename(columns={pc: "puma", "county": "cofips"})
        df["state"] = df["state"].str.zfill(2)
        df["puma"] = df["puma"].str.zfill(5)
        df["cofips"] = df["cofips"].str.zfill(5)
        df["afact"] = pd.to_numeric(df["afact"], errors="coerce")
        out[v] = df[["state", "puma", "cofips", "afact"]].dropna()
    return out


def load_cbsa():
    d = pd.read_excel(CACHE / "omb_delineation_2013_list1.xls", skiprows=2)
    d = d[d["Metropolitan/Micropolitan Statistical Area"] == "Metropolitan Statistical Area"]
    d = d.dropna(subset=["FIPS State Code", "FIPS County Code"])
    d["cofips"] = (d["FIPS State Code"].astype(int).astype(str).str.zfill(2)
                   + d["FIPS County Code"].astype(int).astype(str).str.zfill(3))
    d["cbsa"] = d["CBSA Code"].astype(str).str.strip()
    d["state_fips"] = d["FIPS State Code"].astype(int)
    return d[["cofips", "cbsa", "CBSA Title", "state_fips"]].rename(
        columns={"CBSA Title": "cbsa_title"})


def main():
    files = sorted((CACHE / "kids").glob("kids_*.csv"))
    if not files:
        sys.exit("no kid cells")
    cells = pd.concat((pd.read_csv(f, dtype={"state": str, "puma": str})
                       for f in files), ignore_index=True)
    cells["state"] = cells["state"].str.zfill(2)
    cells["puma"] = cells["puma"].str.zfill(5)

    # keep only fully-pulled state-years: a year missing states would give partial metros
    cov = cells.groupby("year")["state"].nunique()
    full = sorted(cov[cov == 51].index)
    part = sorted(cov[cov < 51].index)
    if part:
        print("dropping part-coverage years:", [(int(y), int(cov[y])) for y in part])
    cells = cells[cells["year"].isin(full)]
    if cells.empty:
        sys.exit("no fully covered year yet")
    print("years kept:", full)

    cells["vint"] = cells["year"].map(VINTAGE)
    xw, cbsa = load_xwalks(), load_cbsa()
    parts = []
    for v, g in cells.groupby("vint"):
        m = g.merge(xw[v], on=["state", "puma"], how="left", indicator=True)
        print(f"{v}: puma-county merge miss {(m['_merge'] != 'both').mean():.4f} "
              f"rows {len(m)}")
        m = m[m["_merge"] == "both"].drop(columns="_merge")
        for c in ("pub", "priv", "noschool"):
            m[c] = m[c] * m["afact"]
        parts.append(m)
    alloc = pd.concat(parts, ignore_index=True)
    j = alloc.merge(cbsa, on="cofips", how="inner")

    # A CBSA can span states (New York, Chicago, Washington, Philadelphia, Kansas City,
    # Charlotte, Memphis, Portland...). Grouping on state as well as CBSA would split
    # those metros into one row per state and then drop them from the balanced panel, so
    # each CBSA is assigned ONE state: that of its largest allocated child population.
    home = (j.groupby(["cbsa", "state_fips"], as_index=False)["pub"].sum()
             .sort_values("pub", ascending=False).drop_duplicates("cbsa")
             [["cbsa", "state_fips"]])
    j = j.drop(columns=["state_fips"]).merge(home, on="cbsa", how="left")

    # long -> wide on group x level
    agg = (j.groupby(["cbsa", "cbsa_title", "state_fips", "year", "grp", "lvl"],
                     as_index=False)[["pub", "priv", "noschool"]].sum())
    rows = []
    for (c, t, sf, y), g in agg.groupby(["cbsa", "cbsa_title", "state_fips", "year"]):
        r = {"cbsa": c, "cbsa_title": t, "state_fips": int(sf), "year": int(y)}
        for lvl in ("all", "elem", "sec"):
            sub = g if lvl == "all" else g[g["lvl"] == lvl]
            tot_pub = sub["pub"].sum()
            tot_priv = sub["priv"].sum()
            r[f"enr_{lvl}"] = tot_pub + tot_priv
            r[f"pub_{lvl}"] = tot_pub
            for grp in GROUPS:
                s = sub[sub["grp"] == grp]
                r[f"{grp}_pub_{lvl}"] = s["pub"].sum()
                r[f"{grp}_priv_{lvl}"] = s["priv"].sum()
        rows.append(r)
    p = pd.DataFrame(rows)

    for lvl in ("all", "elem", "sec"):
        w_pub, w_priv = p[f"wnh_nb_pub_{lvl}"], p[f"wnh_nb_priv_{lvl}"]
        p[f"wnh_enr_{lvl}"] = w_pub + w_priv
        p[f"priv_wnh_{lvl}"] = w_priv / (w_pub + w_priv).where((w_pub + w_priv) > 0)
        hisp_pub = p[f"hisp_nb_pub_{lvl}"] + p[f"hisp_fb_pub_{lvl}"]
        hisp_enr = hisp_pub + p[f"hisp_nb_priv_{lvl}"] + p[f"hisp_fb_priv_{lvl}"]
        fb_enr = (p[f"hisp_fb_pub_{lvl}"] + p[f"hisp_fb_priv_{lvl}"]
                  + p[f"nonhisp_fb_pub_{lvl}"] + p[f"nonhisp_fb_priv_{lvl}"])
        asian_enr = p[f"anh_nb_pub_{lvl}"] + p[f"anh_nb_priv_{lvl}"]
        black_enr = p[f"bnh_nb_pub_{lvl}"] + p[f"bnh_nb_priv_{lvl}"]
        den = p[f"enr_{lvl}"].where(p[f"enr_{lvl}"] > 0)
        p[f"hisp_share_{lvl}"] = hisp_enr / den
        p[f"hisp_share_pub_{lvl}"] = hisp_pub / p[f"pub_{lvl}"].where(p[f"pub_{lvl}"] > 0)
        p[f"fb_share_{lvl}"] = fb_enr / den
        p[f"asian_share_{lvl}"] = asian_enr / den
        p[f"black_share_{lvl}"] = black_enr / den
        p[f"wnh_share_{lvl}"] = p[f"wnh_enr_{lvl}"] / den
        # all US-born non-Hispanic children, to test whether flight is white-specific
        nnh_pub = sum(p[f"{g}_pub_{lvl}"] for g in ("wnh_nb", "bnh_nb", "anh_nb", "onh_nb"))
        nnh_priv = sum(p[f"{g}_priv_{lvl}"] for g in ("wnh_nb", "bnh_nb", "anh_nb", "onh_nb"))
        p[f"nnh_enr_{lvl}"] = nnh_pub + nnh_priv
        p[f"priv_nnh_{lvl}"] = nnh_priv / (nnh_pub + nnh_priv).where((nnh_pub + nnh_priv) > 0)
        # US-born Hispanic children: do they also leave?
        hnb_pub, hnb_priv = p[f"hisp_nb_pub_{lvl}"], p[f"hisp_nb_priv_{lvl}"]
        p[f"priv_hnb_{lvl}"] = hnb_priv / (hnb_pub + hnb_priv).where((hnb_pub + hnb_priv) > 0)
        p[f"hnb_enr_{lvl}"] = hnb_pub + hnb_priv

    p = p.sort_values(["cbsa", "year"])
    p.to_csv(DERIVED / "metro_school_panel.csv", index=False)
    print(f"wrote metro_school_panel.csv: {len(p)} rows, {p.cbsa.nunique()} metros, "
          f"years {sorted(p.year.unique())}")
    big = p[p["enr_all"] >= 20000]
    print(f"metros with >=20,000 enrolled children in all years: "
          f"{big.groupby('cbsa').size().eq(len(full)).sum()}")
    print(p.groupby("year")[["priv_wnh_all", "hisp_share_all", "fb_share_all"]]
          .apply(lambda d: pd.Series({
              "priv_wnh_w": (d.priv_wnh_all * p.loc[d.index, "wnh_enr_all"]).sum()
                            / p.loc[d.index, "wnh_enr_all"].sum(),
              "hisp_w": (d.hisp_share_all * p.loc[d.index, "enr_all"]).sum()
                        / p.loc[d.index, "enr_all"].sum(),
              "fb_w": (d.fb_share_all * p.loc[d.index, "enr_all"]).sum()
                      / p.loc[d.index, "enr_all"].sum()})))


if __name__ == "__main__":
    main()
