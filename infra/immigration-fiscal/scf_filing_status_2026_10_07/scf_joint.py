"""SCF 2022: Hispanic vs non-Hispanic white joint filers, income and modelled 2023 federal income tax.

Compares with Treasury OTA WP-124 Table 3 (TY2023 average income tax per joint return:
Hispanic 9,477, White 28,664). Variable numbers verified against codebk2022.txt:
X5744 filed 2021 return (1 yes, 6 not yet), X5746 joint (1), X7004 respondent Hispanic (1 yes,
5 no), X6809 respondent first race (1 white, 3 Hispanic/Latino), X5729 total 2021 income,
X5702..X5724 income components, X42001 weight (per implicate; /5 when pooling).
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import taxcalc as tc

ROOT = Path(__file__).resolve().parents[3]
SRC = ROOT / "sources/immigration-fiscal/data/external/stage3/frb/scf2022"
OUT = Path(__file__).resolve().parent / "derived"
AWI_2021, AWI_2023 = 60575.07, 66621.80  # SSA average wage index
OTA = {"hispanic": 9477.0, "white": 28664.0}  # WP-124 Table 3 Total rows, TY2023

cols = ["yy1", "y1", "x5744", "x5746", "x7004", "x6809", "x5729", "x42001",
        "x5702", "x5704", "x5706", "x5708", "x5710", "x5712", "x5714", "x5716",
        "x5718", "x5720", "x5722", "x5724"]
d = pd.read_stata(SRC / "p22i6.dta", columns=cols, convert_categoricals=False)
s = pd.read_stata(SRC / "rscfp2022.dta", columns=["y1", "age", "kids"], convert_categoricals=False)
d = d.merge(s, on="y1", how="left", validate="1:1")
assert d.age.notna().all()
d["imp"] = d.y1 % 10
d["w"] = d.x42001 / 5.0
d["joint"] = d.x5744.isin([1, 6]) & d.x5746.eq(1)
groups = {
    "hispanic_x7004": d.x7004.eq(1),
    "hispanic_tpc_x6809": d.x6809.eq(3),
    "white_nonhispanic": d.x6809.eq(1) & d.x7004.eq(5),
    "all_joint": pd.Series(True, index=d.index),
}

# Taxcalc inputs: 2021 SCF family income indexed by wages to 2023, 2023 law, MFJ.
f = AWI_2023 / AWI_2021
pos = lambda c: d[c].clip(lower=0) * f
rec = pd.DataFrame({
    "RECID": np.arange(len(d)) + 1, "MARS": 2, "FLPDYR": 2023, "age_head": d.age.astype(int),
    "age_spouse": d.age.astype(int), "e00200": pos("x5702"), "e00200p": pos("x5702"),
    "e00900": d.x5704.where(d.x5704 > -9, 0) * f, "e00900p": d.x5704.where(d.x5704 > -9, 0) * f,
    "e00400": pos("x5706"), "e00300": pos("x5708"), "e00600": pos("x5710"),
    "p23250": d.x5712.where(d.x5712 > -9, 0) * f, "e02000": d.x5714.where(d.x5714 > -9, 0) * f,
    "e02300": pos("x5716"), "e00800": pos("x5718"),
    "e02400": d.x5722.clip(lower=0).where(d.age >= 62, 0) * f,
    "e01700": d.x5722.clip(lower=0).where(d.age < 62, 0) * f,
    "e01400": 0.0, "n24": d.kids.astype(int), "EIC": d.kids.clip(upper=3).astype(int),
    "nu18": d.kids.astype(int), "XTOT": 2 + d.kids.astype(int), "s006": 1.0,
})
rec.loc[rec.e00900 < 0, "e00900"] = rec.e00900.clip(lower=-1e7)
rec["e00900p"] = rec.e00900
rec["e00650"] = rec.e00600
rec["e01500"] = rec.e01700
rec["e02100"] = 0.0
rec["e02100p"] = 0.0
pol = tc.Policy()
calc = tc.Calculator(policy=pol, records=tc.Records(data=rec, start_year=2023, gfactors=None, weights=None),
                     verbose=False)
calc.calc_all()
d["iitax"] = calc.array("iitax")
d["agi"] = calc.array("c00100")
d["inc2023"] = d.x5729.clip(lower=0) * f


def wq(v, w, q):
    o = np.argsort(v)
    cw = np.cumsum(w[o])
    return float(v[o][np.searchsorted(cw, q * cw[-1])])


rows = []
for g, m in groups.items():
    sel = d[m & d.joint]
    per = []
    for i, x in sel.groupby("imp"):
        w = x.x42001.to_numpy()
        per.append(dict(n=len(x), wsum=w.sum(), mean_inc=np.average(x.inc2023, weights=w),
                        med_inc=wq(x.inc2023.to_numpy(), w, 0.5), mean_agi=np.average(x.agi, weights=w),
                        mean_tax=np.average(x.iitax, weights=w), med_tax=wq(x.iitax.to_numpy(), w, 0.5),
                        mean_kids=np.average(x.kids, weights=w)))
    p = pd.DataFrame(per)
    rows.append(dict(group=g, n_unweighted_per_implicate=int(p.n.iloc[0]), joint_units_m=p.wsum.mean() / 1e6,
                     mean_income_2023=p.mean_inc.mean(), median_income_2023=p.med_inc.mean(),
                     mean_agi_taxcalc=p.mean_agi.mean(), mean_iitax_2023=p.mean_tax.mean(),
                     mean_iitax_implicate_sd=p.mean_tax.std(), median_iitax_2023=p.med_tax.mean(),
                     mean_kids=p.mean_kids.mean()))
r = pd.DataFrame(rows)
OUT.mkdir(exist_ok=True)
r.to_csv(OUT / "scf_joint_filers.csv", index=False, lineterminator="\n", float_format="%.4f")
g = r.set_index("group")
cmp = []
for h in ["hispanic_x7004", "hispanic_tpc_x6809"]:
    cmp.append(dict(hispanic_def=h,
                    scf_tax_ratio=g.loc[h, "mean_iitax_2023"] / g.loc["white_nonhispanic", "mean_iitax_2023"],
                    ota_tax_ratio=OTA["hispanic"] / OTA["white"],
                    scf_hisp_tax_over_ota=g.loc[h, "mean_iitax_2023"] / OTA["hispanic"],
                    scf_white_tax_over_ota=g.loc["white_nonhispanic", "mean_iitax_2023"] / OTA["white"],
                    scf_income_ratio=g.loc[h, "mean_income_2023"] / g.loc["white_nonhispanic", "mean_income_2023"],
                    scf_median_income_ratio=g.loc[h, "median_income_2023"] / g.loc["white_nonhispanic", "median_income_2023"]))
c = pd.DataFrame(cmp)
c.to_csv(OUT / "scf_vs_ota.csv", index=False, lineterminator="\n", float_format="%.4f")
pd.set_option("display.width", 200)
print(r.round(1).to_string())
print(c.round(3).to_string())
sys.exit(0)
