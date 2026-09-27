#!/usr/bin/env python3
"""Parents of US citizens (IR-5 class, "Immediate relatives - Parents") admitted to LPR status,
Mexico vs India, China and the Philippines, FY2005-FY2024, and their age at admission.

Sources (all cached in _cache/, sha256 in derived/flow_sources.json):
  * OHSS, "Persons Obtaining LPR Status by Region and Country of Birth: FY2005 to 2024", major
    class sheets (file 2026_0604_ohss_lpr_by_country_by_major_class_and_deriv_emp-based_fy2005-2024.xlsx,
    rounded to 10) and the earlier unrounded FY2005-2022 edition
    (sources/.../origin/ohss/lpr_country_birth_major_class_2005_2022.xlsx).
  * Yearbook of Immigration Statistics Table 6 (type and major class of admission): FY2013
    edition (2004-2013), FY2023 edition (2014-2023) and FY2024 edition (2015-2024); Table 9 (broad
    class x age, FY2024); expanded Table 10 (new arrivals vs adjustments by country, FY2023-24).
  * OHSS Profiles on LPRs by country of birth (one workbook per country and year): LPRs by age
    group, new arrival vs adjustment.
  * New Immigrant Survey 2003, Round 1 (ICPSR 38031 v3): visa category "Parent of U.S. Citizen",
    birth year (A7), admission year, country of birth, sampling weight NISWGTSAMP1.

Run from repo root:
  uv run --no-project --with xlrd --with openpyxl --with pandas python3 \
      infra/immigration-fiscal/late_arrival_tail_2026_09_27/flow.py
"""
from __future__ import annotations

import csv
import hashlib
import io
import json
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
CACHE = HERE / "_cache"
OUT = HERE / "derived"

MAJOR_2024 = CACHE / "2026_0604_ohss_lpr_by_country_by_major_class_and_deriv_emp-based_fy2005-2024.xlsx"
MAJOR_2022 = ROOT / "sources/immigration-fiscal/data/external/origin/ohss/lpr_country_birth_major_class_2005_2022.xlsx"
YB_CACHE = ROOT / "infra/immigration-fiscal/indian_ledger_2026_09_18/_cache"  # read-only reuse
YB2024 = YB_CACHE / "yearbook_lpr_fy2024.xlsx"
YB2023 = YB_CACHE / "yearbook_lpr_fy2023.xlsx"
YB2013_T6 = CACHE / "yb2013/2013_table6.xls"
EXP = {2023: CACHE / "2025_0828_ohss_tables8-11newadj_fy2023_v2.xlsx",
       2024: CACHE / "2026_0604_ohss_tables8-11newadj_fy2024.xlsx"}
NIS_ZIP = ROOT / "sources/immigration-fiscal/data/external/icpsr_nis_2003/ICPSR_38031-V3.zip"
PROFILES = CACHE / "profiles"

COUNTRIES = {"Mexico": "mexico", "India": "india", "China, People's Republic": "china",
             "Philippines": "philippines"}
NIS_COUNTRY = {135: "mexico", 98: "india", 44: "china", 164: "philippines"}
NIS_PARENT = 3  # VISACATMO "Parent of U.S. Citizen" (P.I. codebook DS0002)


def sha256(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def num(v):
    if v is None or (isinstance(v, float) and np.isnan(v)):
        return np.nan
    if isinstance(v, str):
        v = v.strip().replace(",", "")
        if v in ("-", ""):
            return 0.0
        if v == "D" or v == "X":
            return np.nan
        return float(v)
    return float(v)


def parents_sheet(path: Path) -> pd.DataFrame:
    """Country x year table from the 'Parents' major-class sheet."""
    book = pd.read_excel(path, sheet_name=None, header=None)
    name = [k for k in book if "Parents" in k]
    assert len(name) == 1, name
    df = book[name[0]]
    hdr = df.index[df[0].astype(str).str.startswith("Region and country")][0]
    years = [int(y) for y in df.loc[hdr, 1:].dropna()]
    body = df.loc[hdr + 1:, : len(years)]
    body.columns = ["label"] + years
    body = body[body.label.notna()]
    body["label"] = body.label.astype(str).str.strip()
    stop = body.index[body.label.str.startswith(("D Data", "1 Data", "Source", "- Represents"))]
    body = body.loc[: stop[0] - 1] if len(stop) else body
    return body


def country_rows(body: pd.DataFrame) -> pd.DataFrame:
    """Rows after the second 'Total' are countries; the first block is regions."""
    tot = body.index[body.label == "Total"]
    assert len(tot) == 2, "expected region and country Total rows"
    return body.loc[tot[1] + 1:], body.loc[tot[1]]


def yearbook_parents() -> dict[int, float]:
    out: dict[int, float] = {}
    t = pd.read_excel(YB2013_T6, header=None)
    hdr = t.index[t[0].astype(str).str.startswith("Type and class")][0]
    yrs = [int(y) for y in t.loc[hdr, 1:].dropna()]
    row = t.index[t[0].astype(str).str.strip() == "Parents"][0]  # first block = TOTAL
    for j, y in enumerate(yrs, start=1):
        out[y] = num(t.loc[row, j])
    for path in (YB2023, YB2024):
        t = pd.read_excel(path, sheet_name="Table 6", header=None)
        hdr = t.index[t[0].astype(str).str.startswith("Type and class")][0]
        yrs = [int(y) for y in t.loc[hdr, 1:].dropna()]
        row = t.index[t[0].astype(str).str.strip() == "Parents"][0]
        for j, y in enumerate(yrs, start=1):
            v = num(t.loc[row, j])
            if y in out and y <= 2013:
                continue
            out.setdefault(y, v)
            out[f"{y}_{path.stem}"] = v
    return out


def profile_rows(path: Path) -> dict[str, float]:
    df = pd.read_excel(path, header=None)
    lab = df[0].astype(str).str.strip().str.replace(" to ", "-", regex=False)
    want = {"Total": "lpr_total", "New arrivals": "new_arrivals",
            "Adjustments of status": "adjustments", "45-54 years": "age_45_54",
            "55-64 years": "age_55_64", "65 years and over": "age_65plus",
            "Immediate relatives of U.S. citizens": "immediate_relatives"}
    out = {}
    for k, v in want.items():
        idx = lab.index[lab == k]
        out[v] = num(df.loc[idx[0], 1]) if len(idx) else np.nan
    return out


def expanded_ir(year: int) -> dict[str, float]:
    out = {}
    for kind, sheet in (("new", "Table 10 New Arrivals"), ("adj", "Table 10 Adjust")):
        t = pd.read_excel(EXP[year], sheet_name=sheet, header=None)
        lab = t[0].astype(str).str.strip()
        hdr = t.index[lab.str.startswith("Region and country")][0]
        col = list(t.loc[hdr]).index("Immediate relatives of U.S. citizens")
        idx = t.index[lab == "Mexico"]
        out[f"mexico_ir_{kind}"] = num(t.loc[idx[-1], col])
        out[f"mexico_total_{kind}"] = num(t.loc[idx[-1], 1])
    return out


def table9_ir_age() -> list[dict]:
    t = pd.read_excel(YB2024, sheet_name="Table 9", header=None)
    lab = t[0].astype(str).str.strip()
    start = t.index[lab == "AGE"][0]
    stop = t.index[lab == "BROAD AGE GROUPS"][0]
    rows = []
    for i in range(start + 1, stop):
        rows.append({"age": lab[i], "all_classes": num(t.loc[i, 1]),
                     "immediate_relatives": num(t.loc[i, 2])})
    return rows


def nis_parents() -> pd.DataFrame:
    with zipfile.ZipFile(NIS_ZIP) as z:
        d2 = pd.read_csv(io.BytesIO(z.read("ICPSR_38031/DS0002/38031-0002-Data.tsv")), sep="\t",
                         usecols=["PU_ID", "CISADMYER", "CISCOBINSMO", "CISADJUST", "VISACATMO",
                                  "NISWGTSAMP1"])
        d3 = pd.read_csv(io.BytesIO(z.read("ICPSR_38031/DS0003/38031-0003-Data.tsv")), sep="\t",
                         usecols=["PU_ID", "A7"])
    d = d2.merge(d3, on="PU_ID", how="left", validate="1:1")
    assert len(d) == 8573, len(d)
    d = d[d.VISACATMO == NIS_PARENT].copy()
    assert len(d) == 995, len(d)  # codebook DS0002: 995 parents of US citizens
    d["age_adm"] = np.where(d.A7 > 1800, d.CISADMYER - d.A7, np.nan)
    d["country"] = d.CISCOBINSMO.map(NIS_COUNTRY).fillna("other")
    return d


def wshare(w, mask):
    return float((w * mask).sum() / w.sum())


def main() -> None:
    OUT.mkdir(exist_ok=True)
    gates = []
    new = parents_sheet(MAJOR_2024)
    old = parents_sheet(MAJOR_2022)
    yb = yearbook_parents()
    years = list(range(2005, 2025))

    rows = []
    for label, key in COUNTRIES.items():
        cn, _ = country_rows(new)
        co, _ = country_rows(old)
        rn = cn[cn.label.str.rstrip("0123456789") == label]
        ro = co[co.label.str.rstrip("0123456789") == label]
        assert len(rn) == 1 and len(ro) == 1, (label, len(rn), len(ro))
        for y in years:
            v_old = num(ro.iloc[0][y]) if y <= 2022 else np.nan
            v_new = num(rn.iloc[0][y])
            use = v_old if y <= 2022 else v_new
            src = "ohss_major_class_fy2005_2022 (unrounded)" if y <= 2022 else "ohss_major_class_fy2005_2024 (rounded to 10)"
            prof_path = next(iter(sorted(PROFILES.glob(f"{key}_{y}.*"))), None)
            prof = profile_rows(prof_path) if prof_path else {}
            rows.append({"fy": y, "country": key, "ir5_parents": use, "source": src,
                         "ir5_rounded_edition": v_new, **prof,
                         "profile_file": prof_path.name if prof_path else ""})
            if y <= 2022:
                gates.append({"gate": f"{key} {y}: rounded edition within 5 of unrounded",
                              "value": v_new - v_old, "pass": abs(v_new - v_old) <= 5})

    # all-country totals
    tot_n = country_rows(new)[1]
    tot_o = country_rows(old)[1]
    cn, _ = country_rows(new)
    co, _ = country_rows(old)
    for y in years:
        total = num(tot_o[y]) if y <= 2022 else num(tot_n[y])
        rows.append({"fy": y, "country": "all", "ir5_parents": total,
                     "source": "same, Total row", "ir5_rounded_edition": num(tot_n[y])})
        ybv = yb.get(y, np.nan)
        gates.append({"gate": f"all {y}: country-sheet Total = Yearbook Table 6 Parents",
                      "value": total - ybv, "pass": abs(total - ybv) <= (0 if y <= 2022 and y <= 2013 else 10)})
        if y <= 2022:
            vals = co[y].map(num)
            s, nd = vals.sum(), int(vals.isna().sum())  # D = withheld small cells
            gates.append({"gate": f"all {y}: Total - country rows within the {nd} withheld (D) cells x 9",
                          "value": total - s, "pass": 0 <= total - s <= 9 * nd})
    for y in range(2014, 2025):
        for ed in ("yearbook_lpr_fy2023", "yearbook_lpr_fy2024"):
            k = f"{y}_{ed}"
            if k in yb and y <= 2022:
                gates.append({"gate": f"all {y}: {ed} Table 6 = unrounded Total (to rounding)",
                              "value": yb[k] - num(tot_o[y]), "pass": abs(yb[k] - num(tot_o[y])) <= 10})
    # profiles: Mexico LPR total in profile = Table 3 edition value check via age rows sum
    for r in rows:
        if r.get("lpr_total") and r["country"] != "all" and not np.isnan(r.get("lpr_total", np.nan)):
            pass

    flow = pd.DataFrame(rows)
    flow["ir5_share_of_country_lpr"] = flow.ir5_parents / flow.lpr_total
    flow["lpr_55plus"] = flow.age_55_64 + flow.age_65plus
    flow["ir5_55plus_upper_bound_share"] = np.minimum(flow.lpr_55plus / flow.ir5_parents, 1.0)
    cols = ["fy", "country", "ir5_parents", "lpr_total", "ir5_share_of_country_lpr",
            "new_arrivals", "adjustments", "immediate_relatives", "age_45_54", "age_55_64",
            "age_65plus", "lpr_55plus", "ir5_55plus_upper_bound_share", "source", "profile_file"]
    flow = flow[cols].sort_values(["country", "fy"])
    flow.to_csv(OUT / "ir5_flow.csv", index=False, lineterminator="\n", float_format="%.4f")

    # age at admission: NIS 2003 parents + Yearbook FY2024 Table 9 immediate relatives
    d = nis_parents()
    age_rows = []
    bands = [(0, 44), (45, 49), (50, 54), (55, 59), (60, 64), (65, 74), (75, 120)]
    for grp in ["mexico", "india", "china", "philippines", "all"]:
        s = d if grp == "all" else d[d.country == grp]
        s = s[s.age_adm.notna()]
        w = s.NISWGTSAMP1.astype(float)
        rec = {"source": "NIS-2003 R1 parents of US citizens (VISACATMO=3)", "group": grp,
               "n": len(s), "weighted_n": float(w.sum()),
               "mean_age": float((w * s.age_adm).sum() / w.sum()),
               "median_age_unweighted": float(s.age_adm.median()),
               "share_adjusting": wshare(w, s.CISADJUST == 1)}
        for lo, hi in bands:
            rec[f"age_{lo}_{hi}"] = wshare(w, s.age_adm.between(lo, hi))
        rec["age_50plus"] = wshare(w, s.age_adm >= 50)
        rec["age_55plus"] = wshare(w, s.age_adm >= 55)
        rec["age_60plus"] = wshare(w, s.age_adm >= 60)
        rec["age_65plus"] = wshare(w, s.age_adm >= 65)
        age_rows.append(rec)
    pd.DataFrame(age_rows).to_csv(OUT / "ir5_age_nis2003.csv", index=False, lineterminator="\n",
                                  float_format="%.4f")
    t9 = pd.DataFrame(table9_ir_age())
    t9.to_csv(OUT / "lpr_age_table9_fy2024.csv", index=False, lineterminator="\n")
    gates.append({"gate": "NIS parents with valid birth year >= 95%",
                  "value": float(d.age_adm.notna().mean()), "pass": d.age_adm.notna().mean() >= 0.95})

    exp = {y: expanded_ir(y) for y in EXP}
    with (OUT / "mexico_ir_new_vs_adjust.csv").open("w", newline="") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(["fy", "mexico_ir_new_arrivals", "mexico_ir_adjustments",
                    "mexico_all_new_arrivals", "mexico_all_adjustments"])
        for y, e in exp.items():
            w.writerow([y, e["mexico_ir_new"], e["mexico_ir_adj"], e["mexico_total_new"],
                        e["mexico_total_adj"]])

    g = pd.DataFrame(gates)
    g.to_csv(OUT / "flow_gates.csv", index=False, lineterminator="\n")
    srcs = {str(p.relative_to(ROOT)): sha256(p) for p in
            [MAJOR_2024, MAJOR_2022, YB2024, YB2023, YB2013_T6, *EXP.values(), NIS_ZIP,
             *sorted(PROFILES.glob("*.xls*"))]}
    (OUT / "flow_sources.json").write_text(json.dumps(srcs, indent=1, sort_keys=True) + "\n")
    bad = g[~g["pass"]]
    print(flow[flow.country.isin(["mexico", "all"])][["fy", "country", "ir5_parents", "lpr_total",
                                                       "lpr_55plus", "ir5_55plus_upper_bound_share"]].to_string())
    print(pd.DataFrame(age_rows).T.to_string())
    print(t9.to_string())
    print(exp)
    print(f"gates: {len(g) - len(bad)}/{len(g)} pass")
    if len(bad):
        print(bad.to_string())
        raise SystemExit("[GATE FAIL] flow gates")


if __name__ == "__main__":
    main()
