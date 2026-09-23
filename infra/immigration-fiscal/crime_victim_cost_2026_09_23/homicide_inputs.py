"""Homicide inputs for 2024: national victims by ethnicity and the offender distribution.

Victims: CDC WONDER D158 (final deaths 2018-2024), NCHS 113-cause "Assault (homicide)"
GR113-127, 2024, by Hispanic origin x single race, parsed from the homicide lane's cached XML
response (not from its derived CSV, which is only compared).
Offenders: FBI Supplementary Homicide Reports as compiled by the Murder Accountability
Project (SHR76_25a.csv, sha256 checked), murder and non-negligent manslaughter excluding
justifiable homicide; each victim record carries its first offender. For every victim group
the share of cleared, ethnicity-known victims whose first offender is Hispanic.
Reuses the homicide lane's parser and ethnicity coding unchanged.
"""
from pathlib import Path
import hashlib
import sys
import xml.etree.ElementTree as ET

import pandas as pd

HERE = Path(__file__).resolve().parent
HOM = HERE.parent / "homicide_cost_2026_09_18"
sys.path.insert(0, str(HOM))
import shr_analysis as shr  # noqa: E402
import wonder  # noqa: E402

SHR_SHA256 = "eeedbf5e58a4a2e91d88e8078341210bd2034b57e6d42d0e2de2667020b88a12"
GROUPS = ["hispanic", "nh_white", "nh_black", "nh_other"]
WINDOWS = {"2024": (2024, 2024), "2022_2024": (2022, 2024), "2019_2024": (2019, 2024)}
OUT = HERE / "derived"


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def wonder_2024() -> pd.DataFrame:
    root = ET.fromstring((HOM / "_cache/wonder_D158_yr_hisp_race_113.xml").read_text())
    d = pd.DataFrame(wonder.rows(root, 3), columns=["year", "hispanic_origin", "race", "deaths"])
    d["year"] = d.year.str.strip()
    d["deaths"] = pd.to_numeric(d.deaths.str.replace(",", ""), errors="coerce")
    d = d[d.year.eq("2024")]
    held = pd.read_csv(HOM / "derived/wonder_deaths_year_hispanic_race.csv", dtype={"year": str})
    held = held[held.year.eq("2024")].reset_index(drop=True)
    if not (d.reset_index(drop=True)[["hispanic_origin", "race"]].equals(held[["hispanic_origin", "race"]])
            and ((d.deaths.fillna(-1).to_numpy() == held.deaths.fillna(-1).to_numpy()).all())):
        raise SystemExit("[BLOCKED] WONDER XML parse disagrees with the homicide lane's derived CSV")
    print("[gate] WONDER 2024 XML parse equals the homicide lane's derived CSV, 21 cells")
    tot = pd.DataFrame(wonder.rows(ET.fromstring((HOM / "_cache/wonder_D158_yr_hisp_113.xml").read_text()), 2),
                       columns=["year", "hispanic_origin", "deaths"])
    tot = tot[tot.year.str.strip().eq("2024")]
    tot["deaths"] = pd.to_numeric(tot.deaths.str.replace(",", ""), errors="coerce")
    margin = tot.set_index("hispanic_origin").deaths
    nh = d[d.hispanic_origin.eq("Not Hispanic or Latino")].set_index("race").deaths
    out = {
        "hispanic": margin["Hispanic or Latino"],
        "nh_white": nh["White"],
        "nh_black": nh["Black or African American"],
        "nh_other": margin["Not Hispanic or Latino"] - nh["White"] - nh["Black or African American"],
        "not_stated": margin["Not Stated"],
    }
    if abs(nh.sum() - margin["Not Hispanic or Latino"]) > 0.5:
        raise SystemExit("[BLOCKED] non-Hispanic race cells do not sum to the published margin")
    stated = sum(out[g] for g in GROUPS)
    rows = [dict(group=g, deaths=out[g], deaths_not_stated_allocated=out[g] * (1 + out["not_stated"] / stated))
            for g in GROUPS]
    rows.append(dict(group="not_stated", deaths=out["not_stated"], deaths_not_stated_allocated=0.0))
    res = pd.DataFrame(rows)
    print(f"[wonder] 2024 homicide deaths {res.deaths.sum():,.0f}: "
          + ", ".join(f"{r.group} {r.deaths:,.0f}" for r in res.itertuples()))
    return res


def main() -> None:
    OUT.mkdir(exist_ok=True)
    got = sha256(shr.RAW)
    if got != SHR_SHA256:
        raise SystemExit(f"[BLOCKED] SHR file hash {got} != pinned {SHR_SHA256}")
    print("[gate] SHR76_25a.csv sha256 matches the homicide lane's pin")
    cols = shr.COLS + ["OffCount", "VicCount"]
    df = pd.read_csv(shr.RAW, usecols=cols, low_memory=False)
    df = df[df.Homicide.eq("Murder and non-negligent manslaughter")].copy()
    df = df[~df.Circumstance.isin(shr.JUSTIFIABLE)]
    df["vic_eth"] = shr.ethnicity(df.VicRace, df.VicEthnic)
    df["off_eth"] = shr.ethnicity(df.OffRace, df.OffEthnic)
    df.loc[df.Solved.ne("Yes"), "off_eth"] = "unsolved"

    mats, probs = [], []
    for w, (lo, hi) in WINDOWS.items():
        d = df[df.Year.between(lo, hi)]
        m = pd.crosstab(d.vic_eth, d.off_eth).reindex(
            index=GROUPS + ["unknown"], columns=GROUPS + ["unknown", "unsolved"], fill_value=0)
        mats.append(m.reset_index().melt(id_vars="vic_eth", var_name="off_eth", value_name="victims")
                    .assign(window=w))
        known = d[d.vic_eth.isin(GROUPS) & d.off_eth.isin(GROUPS)]
        for g in GROUPS:
            k = known[known.vic_eth.eq(g)]
            v = d[d.vic_eth.eq(g)]
            probs.append(dict(
                window=w, victim=g, victims_all=len(v),
                cleared_share=float(v.Solved.eq("Yes").mean()),
                cleared_off_eth_known=len(k),
                off_hispanic=int(k.off_eth.eq("hispanic").sum()),
                p_off_hispanic=float(k.off_eth.eq("hispanic").mean()),
                **{f"p_off_{o}": float(k.off_eth.eq(o).mean()) for o in GROUPS if o != "hispanic"}))
        # multiple-offender incidents among Hispanic first-offender victims (attribution note)
        h = d[d.off_eth.eq("hispanic")]
        print(f"[{w}] victims {len(d):,}; cleared {d.Solved.eq('Yes').mean():.3f}; Hispanic first "
              f"offender {len(h):,}, of which multiple-offender incidents "
              f"{pd.to_numeric(h.OffCount, errors='coerce').gt(0).mean():.3f}")
    pd.concat(mats).to_csv(OUT / "shr_victim_by_first_offender.csv", index=False)
    p = pd.DataFrame(probs)
    p.to_csv(OUT / "shr_p_offender_given_victim.csv", index=False, float_format="%.6f")
    print(p.round(4).to_string(index=False))
    wonder_2024().to_csv(OUT / "wonder_2024_homicide_victims.csv", index=False, float_format="%.3f")


if __name__ == "__main__":
    main()
