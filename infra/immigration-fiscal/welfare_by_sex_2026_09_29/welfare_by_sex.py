"""Means-tested benefits per adult by sex, with and without own children, CPS ASEC 2025 (income year 2024).

Question (operator, 2026-09-29): how much more do women than men get in welfare outside the mother role?

Benefits per person, dollars a year:
- person-level: public assistance (TANF and general assistance, PAW_VAL), SSI (SSI_VAL);
- SPM-unit level, split equally among the unit's members: SNAP, housing subsidy, WIC, energy
  assistance, school lunch (SPM_SNAPSUB, SPM_CAPHOUSESUB, SPM_WICVAL, SPM_ENGVAL, SPM_SCHLUNCH);
- Medicaid, valued at MACPAC FY2023 benefit spending per full-year-equivalent enrollee by eligibility
  group (Exhibit 22, national row, all enrollees): child <19 $4,040; 19-64 SSI recipient (disabled)
  $27,361; 19-64 parent (other adult) $5,757; 19-64 non-parent (expansion adult) $8,021; 65+ $20,305.
  MCAID_CYR 3 (all year) counts 1 year, 2 (part year) counts 0.5 (assumption).
- refundable credits reported apart (EITC, ACTC; SPM unit, split equally), not in "welfare".

Parent = an own child under 18 in the household names this person as parent 1 or 2 (PEPAR1/PEPAR2).
Partnered = spouse (A_SPOUSE) or cohabiting partner (PECOHAB) present.
Survey reports: the CPS under-reports SNAP, TANF, SSI and Medicaid against records. That lowers the
dollar levels; it biases the women/men ratio only if under-reporting differs by sex.
"""
import csv
import hashlib
import io
import sys
import zipfile
from pathlib import Path

import pandas as pd

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
ZIP = ROOT / "sources/immigration-fiscal/data/external/stage3/census/cps_asec_2025/asecpub25csv.zip"
ZIP_SHA = None  # recorded in derived/audit.csv at run time
MACPAC_PDF = HERE / "_cache/macpac_ex22_fy2023.pdf"
MACPAC_SHA = "207e4a5084022317c1788e78d739764dc0141d93441706cb75ffed7f1b3039d2"
MEDICAID_FYE = {"child": 4040, "disabled": 27361, "other_adult": 5757, "new_adult": 8021, "aged": 20305}

SPM_BEN = ["SPM_SNAPSUB", "SPM_CAPHOUSESUB", "SPM_WICVAL", "SPM_ENGVAL", "SPM_SCHLUNCH"]
SPM_CRED = ["SPM_EITC", "SPM_ACTC"]
COLS = ["PH_SEQ", "A_LINENO", "A_AGE", "A_SEX", "PRDTRACE", "PEHSPNON", "PEPAR1", "PEPAR2", "A_SPOUSE",
        "PECOHAB", "MARSUPWT", "PAW_VAL", "SSI_VAL", "SSI_YN", "MCAID_CYR", "SPM_ID"] + SPM_BEN + SPM_CRED


def fail(msg):
    print(f"[BLOCKED] {msg}")
    sys.exit(1)


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def load():
    if sha(MACPAC_PDF) != MACPAC_SHA:
        fail("MACPAC Exhibit 22 PDF hash changed")
    with zipfile.ZipFile(ZIP) as z, z.open("pppub25.csv") as f:
        p = pd.read_csv(f, usecols=COLS)
    p["w"] = p["MARSUPWT"] / 100
    pop = p["w"].sum() / 1e6
    if not 330 < pop < 345:
        fail(f"weighted population {pop:.1f}M outside 330-345M: weight scaling wrong")
    # parents: own children under 18 point at this person's line number
    kids = p[p["A_AGE"] < 18]
    par = pd.concat([kids[["PH_SEQ", "PEPAR1"]].rename(columns={"PEPAR1": "L"}),
                     kids[["PH_SEQ", "PEPAR2"]].rename(columns={"PEPAR2": "L"})])
    par = set(map(tuple, par[par["L"] > 0][["PH_SEQ", "L"]].drop_duplicates().to_numpy()))
    p["parent"] = [(h, l) in par for h, l in zip(p["PH_SEQ"], p["A_LINENO"])]
    p["partnered"] = (p["A_SPOUSE"] > 0) | (p["PECOHAB"] > 0)
    n_unit = p.groupby(["PH_SEQ", "SPM_ID"])["A_LINENO"].transform("size")
    p["spm_share"] = p[SPM_BEN].sum(axis=1) / n_unit
    p["credits"] = p[SPM_CRED].sum(axis=1) / n_unit
    p["cash"] = p["PAW_VAL"].clip(lower=0) + p["SSI_VAL"].clip(lower=0)
    years = p["MCAID_CYR"].map({3: 1.0, 2: 0.5}).fillna(0.0)
    grp = pd.Series("new_adult", index=p.index)
    grp[p["parent"]] = "other_adult"
    grp[p["SSI_YN"] == 1] = "disabled"
    grp[p["A_AGE"] < 19] = "child"
    grp[p["A_AGE"] >= 65] = "aged"
    p["medicaid"] = years * grp.map(MEDICAID_FYE)
    p["welfare"] = p["cash"] + p["spm_share"] + p["medicaid"]
    p["any_welfare"] = p["welfare"] > 0
    hisp = p["PEHSPNON"] == 1
    p["race"] = "Other"
    p.loc[~hisp & (p["PRDTRACE"] == 1), "race"] = "White"
    p.loc[~hisp & (p["PRDTRACE"] == 2), "race"] = "Black"
    p.loc[~hisp & (p["PRDTRACE"] == 4), "race"] = "Asian"
    p.loc[hisp, "race"] = "Hispanic"
    p["sex"] = p["A_SEX"].map({1: "men", 2: "women"})
    return p, pop


def wmean(d, col):
    return (d[col] * d["w"]).sum() / d["w"].sum()


def row(label, d):
    return dict(cell=label, n=len(d), pop_m=round(d["w"].sum() / 1e6, 2),
                welfare=round(wmean(d, "welfare")), cash=round(wmean(d, "cash")),
                spm=round(wmean(d, "spm_share")), medicaid=round(wmean(d, "medicaid")),
                credits=round(wmean(d, "credits")), any_share=round(wmean(d, "any_welfare"), 3))


def table(p):
    out = []
    adult = p[(p["A_AGE"] >= 18) & (p["A_AGE"] <= 64)]
    cells = [
        ("18-64 all", adult),
        ("18-64 parent of child <18", adult[adult["parent"]]),
        ("18-64 no own child <18", adult[~adult["parent"]]),
        ("18-64 no own child, no partner", adult[~adult["parent"] & ~adult["partnered"]]),
        ("18-34 no own child, no partner", adult[~adult["parent"] & ~adult["partnered"] & (adult["A_AGE"] <= 34)]),
        ("65+", p[p["A_AGE"] >= 65]),
    ]
    for race in ["White", "Black", "Hispanic", "Asian"]:
        cells.append((f"18-64 no own child, {race}", adult[~adult["parent"] & (adult["race"] == race)]))
        cells.append((f"18-34 no own child, no partner, {race}",
                      adult[~adult["parent"] & ~adult["partnered"] & (adult["A_AGE"] <= 34) & (adult["race"] == race)]))
    for label, d in cells:
        r = {s: row(label, d[d["sex"] == s]) for s in ("women", "men")}
        for s in ("women", "men"):
            out.append(dict(sex=s, **r[s]))
        out.append(dict(sex="women/men", cell=label, n="", pop_m="",
                        welfare=round(r["women"]["welfare"] / r["men"]["welfare"], 2),
                        cash=round(r["women"]["cash"] / r["men"]["cash"], 2) if r["men"]["cash"] else "",
                        spm=round(r["women"]["spm"] / r["men"]["spm"], 2) if r["men"]["spm"] else "",
                        medicaid=round(r["women"]["medicaid"] / r["men"]["medicaid"], 2) if r["men"]["medicaid"] else "",
                        credits=round(r["women"]["credits"] / r["men"]["credits"], 2) if r["men"]["credits"] else "",
                        any_share=round(r["women"]["any_share"] / r["men"]["any_share"], 2)))
    return out


def main():
    p, pop = load()
    rows = table(p)
    (HERE / "derived").mkdir(exist_ok=True)
    with open(HERE / "derived/welfare_by_sex.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]), lineterminator="\n")
        w.writeheader()
        w.writerows(rows)
    with open(HERE / "derived/audit.csv", "w", newline="") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(["item", "value"])
        w.writerow(["asec_zip_sha256", sha(ZIP)])
        w.writerow(["macpac_pdf_sha256", MACPAC_SHA])
        w.writerow(["weighted_population_m", round(pop, 2)])
        w.writerow(["persons", len(p)])
        # survey totals, $bn, for comparison with program records (under-reporting check)
        n_unit = p.groupby(["PH_SEQ", "SPM_ID"])["A_LINENO"].transform("size")
        w.writerow(["snap_total_bn", round((p["SPM_SNAPSUB"] / n_unit * p["w"]).sum() / 1e9, 1)])
        w.writerow(["ssi_total_bn", round((p["SSI_VAL"].clip(lower=0) * p["w"]).sum() / 1e9, 1)])
        w.writerow(["public_assistance_total_bn", round((p["PAW_VAL"].clip(lower=0) * p["w"]).sum() / 1e9, 1)])
        w.writerow(["medicaid_valued_total_bn", round((p["medicaid"] * p["w"]).sum() / 1e9, 1)])
    buf = io.StringIO()
    pd.DataFrame(rows).to_string(buf, index=False)
    print(buf.getvalue())


if __name__ == "__main__":
    main()
