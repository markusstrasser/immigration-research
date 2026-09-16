"""Welfare use by immigrant generation — CPS ASEC microdata (Census API pull, see pull_cps_asec.sh).

Generation of a person: gen1 = foreign-born (PRCITSHP 4/5); gen2 = native-born with at least one parent
born outside the US and its territories (PEFNTVTY/PEMNTVTY not in {57,60,66,69,73,78}); gen3+ =
native-born with both parents US/territory-born (the CPS has no grandparents' birthplace, so "3rd+"
pools everyone from third generation onward). Household generation = reference person's (PERRP 40/41).
CIS-style "any welfare": any member on SNAP (HFOODSP), SSI, cash assistance (PAW), WIC, free/reduced
school lunch (HFLUNCH), Medicaid last year (CAID), public/subsidised housing, or a Census-simulated
EITC > 0 (EIT_CRED). Interviewed households only (H_HHTYPE 1). Household rates use HSUP_WGT of the
reference person; person rates use MARSUPWT.

Inputs (raw, read-only): $PNY_DATA_ROOT/external/cps/asec/asec_<year>_{persons,supp}.json
Run:  uv run --with pandas python3 asec_generation_welfare.py 2025 > result_2025.txt
"""
import json
import os
import re
import sys
from pathlib import Path

import pandas as pd

HERE = Path(__file__).resolve().parent
US_AREA = {57, 60, 66, 69, 73, 78}
COLS = ["any_cis", "any_noeitc", "caid", "snap", "cash", "eitc", "lunch", "housing", "wic", "ssi", "paw"]


def data_dir() -> Path:
    if os.environ.get("CPS_ASEC_DIR"):
        return Path(os.environ["CPS_ASEC_DIR"])
    root = os.environ.get("PNY_DATA_ROOT")
    if not root:
        cfg = HERE.parent / "acquire" / "config.local.env"
        if cfg.exists():
            m = re.search(r'^\s*(?:export\s+)?PNY_DATA_ROOT\s*=\s*"?([^"\s#]+)"?', cfg.read_text(), re.M)
            root = m.group(1) if m else None
    if not root:
        sys.exit("[DEGRADED] PNY_DATA_ROOT unset and no acquire/config.local.env — cannot locate external/cps/asec")
    return Path(root) / "external" / "cps" / "asec"


def complete(path: Path) -> bool:
    return path.exists() and path.stat().st_size > 1000 and path.read_bytes()[-8:].strip().endswith(b"]]")


def load(path: Path) -> pd.DataFrame:
    if not complete(path):
        sys.exit(f"[DEGRADED] missing or truncated raw pull: {path} (run pull_cps_asec.sh)")
    rows = json.load(open(path))
    df = pd.DataFrame(rows[1:], columns=rows[0])
    for c in df.columns:
        df[c] = pd.to_numeric(df[c], errors="coerce")
    return df


def wrate(df: pd.DataFrame, cols=COLS, w="HSUP_WGT") -> pd.Series:
    out = {"n": len(df)}
    for c in cols:
        out[c] = 100 * (df[c] * df[w]).sum() / df[w].sum()
    return pd.Series(out)


def main(year: str) -> None:
    d = data_dir()
    p = load(d / f"asec_{year}_persons.json")
    supp = load(d / f"asec_{year}_supp.json")[["H_SEQ", "PPPOS", "HFLUNCH", "A_SEX", "PEINUSYR", "H_TENURE"]]
    p = p.merge(supp, on=["H_SEQ", "PPPOS"], how="left", validate="one_to_one")
    p = p[(p.H_HHTYPE == 1) & (p.MARSUPWT > 0)].copy()
    print(f"[{year} ASEC, income year {int(year) - 1}] persons {len(p):,}  households {p.H_SEQ.nunique():,}  raw dir {d}")

    native = p.PRCITSHP.isin([1, 2, 3])
    par_fb = ~p.PEFNTVTY.isin(US_AREA) | ~p.PEMNTVTY.isin(US_AREA)
    p["gen"] = "gen1"
    p.loc[native & par_fb, "gen"] = "gen2"
    p.loc[native & ~par_fb, "gen"] = "gen3+"
    p["cit"] = p.PRCITSHP.map({4: "naturalized", 5: "noncitizen"})
    hisp = p.PEHSPNON.eq(1)
    race = p.PRDTRACE.map({1: "white", 2: "black", 4: "asian"}).fillna("other")
    p["eth"] = "other"
    p.loc[hisp, "eth"] = "hispanic"
    p.loc[~hisp & (race == "white"), "eth"] = "NH white"
    p.loc[~hisp & (race == "black"), "eth"] = "NH black"
    p.loc[~hisp & (race == "asian"), "eth"] = "NH asian"
    p["ssi"] = p.SSI_YN.eq(1)
    p["paw"] = p.PAW_YN.eq(1)
    p["wic"] = p.WICYN.eq(1)
    p["caid"] = p.CAID.eq(1)
    p["eitc"] = p.EIT_CRED.gt(0)

    hh = p.groupby("H_SEQ").agg(
        snap=("HFOODSP", lambda s: (s == 1).any()), ssi=("ssi", "any"), paw=("paw", "any"), wic=("wic", "any"),
        caid=("caid", "any"), eitc=("eitc", "any"), lunch=("HFLUNCH", lambda s: (s == 1).any()),
        pub=("HPUBLIC", lambda s: (s == 1).any()), rent=("HLORENT", lambda s: (s == 1).any()),
        kids=("HUNDER18", "max"))
    hh["housing"] = hh.pub | hh.rent
    hh["cash"] = hh.ssi | hh.paw
    hh["any_noeitc"] = hh.snap | hh.ssi | hh.paw | hh.wic | hh.lunch | hh.caid | hh.housing
    hh["any_cis"] = hh.any_noeitc | hh.eitc
    ref = p[p.PERRP.isin([40, 41])][["H_SEQ", "gen", "cit", "eth", "A_AGE", "A_HGA", "HSUP_WGT"]].drop_duplicates("H_SEQ")
    hh = hh.join(ref.set_index("H_SEQ"), how="inner")
    hh["age_grp"] = pd.cut(hh.A_AGE, [0, 34, 64, 120], labels=["<35", "35-64", "65+"])
    hh["haskids"] = hh.kids > 0
    hh["lowed"] = hh.A_HGA <= 39  # high school or less

    pd.set_option("display.width", 220)
    pd.set_option("display.float_format", lambda x: f"{x:5.1f}")
    print("\n== Households by generation of reference person; % with any member using (weighted, HSUP_WGT) ==")
    print(hh.groupby("gen").apply(wrate).to_string())
    print("\n-- weighted share of households by generation (%) --")
    print((hh.groupby("gen").HSUP_WGT.sum() / hh.HSUP_WGT.sum() * 100).round(1).to_string())
    print("\n-- gen1 by citizenship --")
    print(hh[hh.gen == "gen1"].groupby("cit").apply(wrate).to_string())
    print("\n-- gen2 and gen3+ by ethnicity of the reference person --")
    sub = hh[hh.gen.isin(["gen2", "gen3+"])]
    print(sub.groupby(["gen", "eth"]).apply(wrate)[["n", "any_cis", "any_noeitc", "caid", "snap", "cash", "eitc"]].to_string())
    print("\n-- ethnic composition of reference persons within generation (%) --")
    print((hh.groupby(["gen", "eth"]).HSUP_WGT.sum() / hh.groupby("gen").HSUP_WGT.sum() * 100).round(1).unstack().to_string())
    print("\n-- by reference-person age group --")
    print(hh.groupby(["age_grp", "gen"], observed=True).apply(wrate)[["n", "any_cis", "any_noeitc", "caid", "snap", "cash"]].to_string())
    print("\n-- households with children under 18 --")
    print(hh[hh.haskids].groupby("gen").apply(wrate)[["n", "any_cis", "any_noeitc", "caid", "snap", "cash", "lunch"]].to_string())
    print("\n-- reference person with high school or less --")
    print(hh[hh.lowed].groupby("gen").apply(wrate)[["n", "any_cis", "any_noeitc", "caid", "snap", "cash"]].to_string())
    print("\n-- composition: share with children, mean head age, share high-school-or-less --")
    print(hh.groupby("gen").apply(lambda x: pd.Series({
        "kids_pct": 100 * (x.haskids * x.HSUP_WGT).sum() / x.HSUP_WGT.sum(),
        "age_mean": (x.A_AGE * x.HSUP_WGT).sum() / x.HSUP_WGT.sum(),
        "lowed_pct": 100 * (x.lowed * x.HSUP_WGT).sum() / x.HSUP_WGT.sum()})).to_string())

    hh["band"] = pd.cut(hh.A_AGE, [0, 29, 39, 49, 64, 120], labels=["<30", "30s", "40s", "50-64", "65+"])
    std_w = hh[hh.gen == "gen3+"].groupby("band", observed=True).HSUP_WGT.sum()
    std_w = std_w / std_w.sum()
    print("\n-- directly age-standardised to the gen3+ reference-person age distribution (5 bands) --")
    for gname, x in hh.groupby("gen"):
        r = x.groupby("band", observed=True).apply(lambda b: wrate(b)[["any_cis", "any_noeitc", "cash", "caid"]])
        print(gname, " ".join(f"{c}={float((r[c] * std_w).sum()):.1f}" for c in r.columns))

    print("\n== Persons aged 25-64, own receipt (weighted, MARSUPWT); hh_snap = lives in a SNAP household ==")
    a = p[(p.A_AGE >= 25) & (p.A_AGE <= 64)].copy()
    a = a.merge(hh[["snap"]].rename(columns={"snap": "hh_snap"}), left_on="H_SEQ", right_index=True, how="left")
    pc = ["ssi", "paw", "caid", "eitc", "hh_snap"]
    print(a.groupby("gen").apply(lambda x: wrate(x, pc, "MARSUPWT")).to_string())
    print("\n-- by ethnicity --")
    print(a[a.gen.isin(["gen2", "gen3+"])].groupby(["gen", "eth"]).apply(lambda x: wrate(x, pc, "MARSUPWT")).to_string())


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "2025")
