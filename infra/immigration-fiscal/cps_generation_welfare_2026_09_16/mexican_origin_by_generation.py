"""Mexican-origin population by generation: education, work, earnings, poverty and welfare (CPS ASEC).

Origin-generation of a person:
  mex_gen1  = born in Mexico (PENATVTY 303)
  mex_gen2  = native-born, at least one parent born in Mexico (PEFNTVTY or PEMNTVTY 303)
  mex_gen3+ = native-born, both parents US/territory-born, self-identified Mexican origin (PRDTHSP 1)
Comparators: gen3+ non-Hispanic white; all gen3+ natives; all natives. Adults 25-64 unless stated.
Inputs: $PNY_DATA_ROOT/external/cps/asec/asec_<year>_{persons,supp,supp2}.json (pull_cps_asec.sh, pull_cps_asec_supp2.sh)
Run:  uv run --with pandas python3 mexican_origin_by_generation.py 2025 > mexican_origin_result_2025.txt
"""
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
from asec_generation_welfare import US_AREA, data_dir, load  # noqa: E402

MEX = 303


def wmean(df, col, w):
    return float((df[col] * df[w]).sum() / df[w].sum())


def wmedian(df, col, w):
    d = df[[col, w]].sort_values(col)
    c = d[w].cumsum()
    return float(d[col][c >= c.iloc[-1] / 2].iloc[0])


def main(year: str) -> None:
    d = data_dir()
    p = load(d / f"asec_{year}_persons.json")
    s1 = load(d / f"asec_{year}_supp.json")[["H_SEQ", "PPPOS", "HFLUNCH", "A_SEX", "PEINUSYR"]]
    s2 = load(d / f"asec_{year}_supp2.json")[["H_SEQ", "PPPOS", "PRDTHSP", "PEARNVAL", "WSAL_VAL", "PEMLR", "PERLIS", "SPM_POOR"]]
    p = p.merge(s1, on=["H_SEQ", "PPPOS"], validate="one_to_one").merge(s2, on=["H_SEQ", "PPPOS"], validate="one_to_one")
    p = p[(p.H_HHTYPE == 1) & (p.MARSUPWT > 0)].copy()

    native = p.PRCITSHP.isin([1, 2, 3])
    par_fb = ~p.PEFNTVTY.isin(US_AREA) | ~p.PEMNTVTY.isin(US_AREA)
    par_mex = p.PEFNTVTY.eq(MEX) | p.PEMNTVTY.eq(MEX)
    p["gen"] = "gen1"
    p.loc[native & par_fb, "gen"] = "gen2"
    p.loc[native & ~par_fb, "gen"] = "gen3+"
    nhw = p.PEHSPNON.eq(2) & p.PRDTRACE.eq(1)
    p["grp"] = None
    p.loc[p.PENATVTY.eq(MEX) & ~native, "grp"] = "1 Mexico-born"
    p.loc[native & par_mex, "grp"] = "2 Mexican 2nd gen"
    p.loc[(p.gen == "gen3+") & p.PRDTHSP.eq(1), "grp"] = "3 Mexican 3rd+ (self-ID)"
    p.loc[(p.gen == "gen3+") & nhw, "grp"] = "R gen3+ NH white"
    p["grp_all3"] = p.gen.where(p.gen == "gen3+", None).replace({"gen3+": "R gen3+ all"})

    print(f"[{year} ASEC] persons {len(p):,}")
    print("\n== Population (all ages, millions, MARSUPWT) ==")
    for g, x in p.groupby("grp"):
        print(f"  {g:26s} {x.MARSUPWT.sum() / 1e6:6.2f}M   (n {len(x):,})")
    print(f"  {'gen3+ all natives':26s} {p[p.gen == 'gen3+'].MARSUPWT.sum() / 1e6:6.2f}M")
    print(f"  {'all natives':26s} {p[native].MARSUPWT.sum() / 1e6:6.2f}M")

    a = p[(p.A_AGE >= 25) & (p.A_AGE <= 64)].copy()
    a["lt_hs"] = a.A_HGA.le(38)
    a["hs_only"] = a.A_HGA.eq(39)
    a["ba_plus"] = a.A_HGA.ge(43)
    a["employed"] = a.PEMLR.isin([1, 2])
    a["poor_off"] = a.PERLIS.eq(1)
    a["poor_spm"] = a.SPM_POOR.eq(1)
    a["ssi"] = a.SSI_YN.eq(1)
    a["paw"] = a.PAW_YN.eq(1)
    a["caid"] = a.CAID.eq(1)
    a["eitc"] = a.EIT_CRED.gt(0)
    a["hh_snap"] = a.HFOODSP.eq(1)
    a["earn_pos"] = a.PEARNVAL.gt(0)
    groups = {**{g: a[a.grp == g] for g in sorted(a.grp.dropna().unique())},
              "R gen3+ all": a[a.gen == "gen3+"], "R all natives": a[a.PRCITSHP.isin([1, 2, 3])]}
    rows = []
    for g, x in groups.items():
        w = "MARSUPWT"
        workers = x[x.earn_pos]
        rows.append({"group": g, "n": len(x), "age_mean": wmean(x, "A_AGE", w),
                     "lt_hs%": 100 * wmean(x, "lt_hs", w), "hs_only%": 100 * wmean(x, "hs_only", w), "ba_plus%": 100 * wmean(x, "ba_plus", w),
                     "employed%": 100 * wmean(x, "employed", w), "earn_mean$": wmean(x, "PEARNVAL", w),
                     "earn_median_workers$": wmedian(workers, "PEARNVAL", w), "earn_mean_workers$": wmean(workers, "PEARNVAL", w),
                     "poor_off%": 100 * wmean(x, "poor_off", w), "poor_spm%": 100 * wmean(x, "poor_spm", w),
                     "medicaid%": 100 * wmean(x, "caid", w), "ssi%": 100 * wmean(x, "ssi", w), "tanf_ga%": 100 * wmean(x, "paw", w),
                     "eitc%": 100 * wmean(x, "eitc", w), "hh_snap%": 100 * wmean(x, "hh_snap", w)})
    out = pd.DataFrame(rows).set_index("group")
    pd.set_option("display.width", 250)
    pd.set_option("display.float_format", lambda v: f"{v:,.1f}")
    print("\n== Adults 25-64 by origin-generation (person-weighted) ==")
    print(out.T.to_string())

    print("\n== Men 25-54 (prime age): employment and earnings ==")
    m = a[(a.A_SEX == 1) & (a.A_AGE <= 54)]
    for g, x in {**{g: m[m.grp == g] for g in sorted(m.grp.dropna().unique())}, "R gen3+ all": m[m.gen == "gen3+"]}.items():
        wk = x[x.earn_pos]
        print(f"  {g:26s} n {len(x):5d}  employed {100 * wmean(x, 'employed', 'MARSUPWT'):5.1f}%  median earnings (workers) ${wmedian(wk, 'PEARNVAL', 'MARSUPWT'):,.0f}  mean ${wmean(wk, 'PEARNVAL', 'MARSUPWT'):,.0f}")

    print("\n== Households by origin-generation of the reference person: any member on any program (CIS list) ==")
    hh = p.groupby("H_SEQ").agg(snap=("HFOODSP", lambda s: (s == 1).any()), ssi=("SSI_YN", lambda s: (s == 1).any()),
                                paw=("PAW_YN", lambda s: (s == 1).any()), wic=("WICYN", lambda s: (s == 1).any()),
                                caid=("CAID", lambda s: (s == 1).any()), eitc=("EIT_CRED", lambda s: (s > 0).any()),
                                lunch=("HFLUNCH", lambda s: (s == 1).any()), pub=("HPUBLIC", lambda s: (s == 1).any()),
                                rent=("HLORENT", lambda s: (s == 1).any()))
    hh["any"] = hh.snap | hh.ssi | hh.paw | hh.wic | hh.caid | hh.eitc | hh.lunch | hh.pub | hh.rent
    hh["any_noeitc"] = hh.snap | hh.ssi | hh.paw | hh.wic | hh.caid | hh.lunch | hh.pub | hh.rent
    hh["cash"] = hh.ssi | hh.paw
    ref = p[p.PERRP.isin([40, 41])][["H_SEQ", "grp", "gen", "A_AGE", "HSUP_WGT"]].drop_duplicates("H_SEQ").set_index("H_SEQ")
    hh = hh.join(ref, how="inner")
    for g, x in {**{g: hh[hh.grp == g] for g in sorted(hh.grp.dropna().unique())}, "R gen3+ all": hh[hh.gen == "gen3+"]}.items():
        print(f"  {g:26s} n {len(x):5d}  any {100 * wmean(x, 'any', 'HSUP_WGT'):5.1f}%  excl. EITC {100 * wmean(x, 'any_noeitc', 'HSUP_WGT'):5.1f}%  Medicaid {100 * wmean(x, 'caid', 'HSUP_WGT'):5.1f}%  SNAP {100 * wmean(x, 'snap', 'HSUP_WGT'):5.1f}%  cash {100 * wmean(x, 'cash', 'HSUP_WGT'):4.1f}%  head age {wmean(x, 'A_AGE', 'HSUP_WGT'):4.1f}")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "2025")
