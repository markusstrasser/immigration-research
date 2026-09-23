"""Three checks outside MEPS's scope, each from a primary file parsed here.

1. Nursing-facility Medicaid in the complete account. The account's
   Medicaid/CHIP/other medical line (BEA, $954.2bn) carries institutional LTSS
   and allocates the whole line with one community MEPS key. The union's share
   of that key is set against its share of the 65+ institutional population in
   ACS 2024 (`institutional_bound_2026_09_17/derived/acs_cells.csv`, the same
   cells ledger item N uses). Nursing-facility dollars: CMS/Mathematica,
   "Medicaid LTSS Users and Expenditures by Service Category, 2023". The
   corrected nursing-facility charge is then combined with the MEPS ratios
   from `translate.py`, for the Medicaid line and for all five medical lines,
   with linearized SEs from the lines' influence vectors
   (`_cache/account_line_ests.pkl`).
2. Emergency Medicaid. CBO's letter of 2 October 2024 (Table 1, CMS-64) gives
   federal + state emergency Medicaid for people ineligible for full coverage by
   immigration status, FY2017-2023. What MEPS already records for Mexican-origin
   people who never report Medicaid comes from `derived/disconfirmation.csv`.
3. Coverage key against dollars. MEPS's Mexican-origin share of Medicaid-covered
   people is set against the CPS union's share of reported coverage, and against
   the same people's share of MEPS Medicaid dollars.

Run from the repository root:
  OPENBLAS_NUM_THREADS=1 uv run --no-project python3 \
      infra/immigration-fiscal/medical_ethnicity_pooled_2026_09_23/bounds.py
"""
from __future__ import annotations

import hashlib
import json
import pickle
import re
import sys
from pathlib import Path

import numpy as np
import pandas as pd

LANE = Path(__file__).resolve().parent
sys.path.insert(0, str(LANE))  # the pickled designs are design.Design
CACHE = LANE / "_cache"
DERIVED = LANE / "derived"
FISCAL = LANE.parent
LTSS_PDF = CACHE / "ltss-users-expenditures-category-brief-2023.pdf"
LTSS_URL = ("https://www.medicaid.gov/medicaid/long-term-services-supports/downloads/"
            "ltss-users-expenditures-category-brief-2023.pdf (bytes via web.archive.org snapshot 20260109200423)")
CBO_PDF = CACHE / "cbo_emergency_medicaid_2024.pdf"
CBO_URL = ("https://www.cbo.gov/system/files/2024-10/Arrington_Letter_EmergencyMedicaid_Immigration_final.pdf "
           "(bytes via web.archive.org snapshot 20241003010917; cbo.gov serves a captcha to scripts)")
ACS = FISCAL / "institutional_bound_2026_09_17/derived/acs_cells.csv"
ALLOC = FISCAL / "full_account_spending_2026_09_20/derived/allocations.csv"
KEYS = FISCAL / "full_account_spending_2026_09_20/derived/incidence_keys.csv"
PARAMS = FISCAL / "ledger_absolute_2026_09_17/params/params.json"


def _ok(msg):
    print(f"  ✓ {msg}", flush=True)


def _header(s):
    print(f"\n[{s}]", flush=True)


def fail(msg):
    print(f"  ✗ [BLOCKED] {msg}", file=sys.stderr, flush=True)
    raise SystemExit(2)


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def pdf_text(pdf: Path) -> str:
    import subprocess
    txt = pdf.with_suffix(".txt")
    if not txt.exists():
        subprocess.run(["pdftotext", "-layout", str(pdf), str(txt)], check=True)
    return txt.read_text(encoding="utf-8", errors="replace")


def ltss_2023() -> dict:
    flat = " ".join(pdf_text(LTSS_PDF).split())
    pats = {
        "institutional_bn": r"Expenditures for institutional LTSS totaled \$([\d.]+) billion nationwide in 2023",
        "nursing_facility_bn": r"institutional LTSS expenditures were for services at nursing facilities \(\$([\d.]+) billion, or ([\d.]+) percent\)",
        "icf_iid_bn": r"expenditures were higher for services at ICFs/IID \(\$([\d.]+) billion",
        "mental_health_bn": r"health facility expenditures were a small share of total institutional expenditures \(\$([\d.]+) billion",
        "hcbs_bn": r"HCBS expenditures totaled \$([\d.]+) billion nationwide in 2023",
        "nursing_facility_users": r"received services at nursing facilities \(([\d,]+), or ([\d.]+) percent\)",
    }
    out = {}
    for k, p in pats.items():
        m = re.search(p, flat)
        if not m:
            fail(f"CMS LTSS 2023 brief: pattern for {k} not found")
        out[k] = float(m.group(1).replace(",", ""))
        out[k + "_quote"] = m.group(0)
    if abs(out["nursing_facility_bn"] + out["icf_iid_bn"] + out["mental_health_bn"] - out["institutional_bn"]) > 0.15:
        fail("CMS institutional categories do not add to the institutional total")
    return out


def cbo_table() -> pd.DataFrame:
    rows = []
    total = None
    for line in pdf_text(CBO_PDF).splitlines():
        m = re.match(r"^\s*(20\d\d)\s+([\d,]+)\s+([\d,]+)\s+([\d,]+)\s+(\d+)\s*$", line)
        if m:
            rows.append(dict(fiscal_year=int(m.group(1)), federal_m=int(m.group(2).replace(",", "")),
                             state_m=int(m.group(3).replace(",", "")), total_m=int(m.group(4).replace(",", "")),
                             federal_share_pct=int(m.group(5))))
        t = re.match(r"^\s*Total\s+([\d,]+)\s+([\d,]+)\s+([\d,]+)\s*$", line)
        if t:
            total = int(t.group(3).replace(",", ""))
    df = pd.DataFrame(rows)
    if len(df) != 7 or total != 26554 or int(df.total_m.sum()) != total:
        fail(f"CBO Table 1 not parsed as FY2017-2023 summing to 26,554: {len(df)} rows, total {total}")
    if not (df.federal_m + df.state_m == df.total_m).all():
        fail("CBO Table 1 federal + state != total in some year")
    return df


def main():
    audit = {"inputs": {p.name: {"path": str(p), "sha256": sha256(p)} for p in
                        [LTSS_PDF, CBO_PDF, ACS, ALLOC, KEYS, PARAMS]},
             "urls": {LTSS_PDF.name: LTSS_URL, CBO_PDF.name: CBO_URL}}
    rows = []

    def put(check, quantity, value, unit, basis, se=np.nan):
        rows.append(dict(check=check, quantity=quantity, value=value, se=se, unit=unit, basis=basis))

    _header("1 nursing-facility Medicaid in the complete account")
    lt = ltss_2023()
    audit["ltss_2023"] = lt
    _ok(f"CMS 2023: institutional ${lt['institutional_bn']}bn, nursing facilities ${lt['nursing_facility_bn']}bn, "
        f"ICF/IID ${lt['icf_iid_bn']}bn, mental health ${lt['mental_health_bn']}bn; HCBS ${lt['hcbs_bn']}bn")
    al = pd.read_csv(ALLOC)
    line = al[(al.scenario_id == "complete_preferred_F_per_capita") & (al.allocation == "personal")
              & (al.category == "medicaid_and_chip_other_medical")].iloc[0]
    key_share = float(line.target_bn / line.national_bn)
    acs = pd.read_csv(ACS)
    inst = acs[acs.typehugq.eq(2) & acs.band.isin(["65_74", "75_99"])].groupby("group").weighted.sum()
    union_inst = float(inst["mexico_born"] + inst["usborn_mexican"])
    denom_floor = float(inst["all_natives"] + inst["mexico_born"])  # other foreign-born left out: a floor
    s_hi = union_inst / denom_floor
    nf = lt["nursing_facility_bn"]
    charged = nf * key_share
    for lab, s in [("union share = its share of the 65+ institutional population (a ceiling)", s_hi),
                   ("union share doubled, allowing for under-65 residents", 2 * s_hi)]:
        put("nursing_facility", f"use-based charge, {lab}", nf * s, "$bn (2023)",
            f"{nf} x {s:.4f}")
        put("nursing_facility", f"account over-charge, {lab}", charged - nf * s, "$bn (2023)",
            f"{nf} x ({key_share:.4f} - {s:.4f})")
    put("nursing_facility", "account charge to the union of nursing-facility Medicaid", charged, "$bn (2023)",
        f"{nf} x line share {key_share:.4f} (target_bn / national_bn of the preferred Medicaid line)")
    put("nursing_facility", "union persons 65+ in institutional group quarters, ACS 2024", union_inst, "persons",
        "mexico_born + usborn_mexican, bands 65_74 and 75_99, TYPEHUGQ = 2")
    put("nursing_facility", "all natives + Mexico-born 65+ in institutional group quarters, ACS 2024",
        denom_floor, "persons", "floor on the national count: other foreign-born omitted")
    rate = acs.groupby(["group", "band"]).apply(
        lambda g: g.loc[g.typehugq.eq(2), "weighted"].sum() / g.weighted.sum(), include_groups=False)
    for g in ["mexico_born", "usborn_mexican", "all_natives", "native_nh_white"]:
        for b in ["65_74", "75_99"]:
            put("nursing_facility", f"institutional rate {g} {b}", float(rate.loc[(g, b)]), "share", "ACS 2024 TYPEHUGQ = 2")
    audit["nursing_facility"] = {"line_share": key_share, "union_65plus_institutional": union_inst,
                                 "denominator_floor": denom_floor, "share_ceiling": s_hi,
                                 "charged_bn": charged, "use_based_bn": [nf * s_hi, nf * 2 * s_hi]}
    _ok(f"account charges the union {key_share:.2%} of ${nf}bn = ${charged:.2f}bn; its 65+ institutional share "
        f"is at most {s_hi:.2%} -> over-charge ${charged - 2 * nf * s_hi:.2f}-{charged - nf * s_hi:.2f}bn")

    # combined: MEPS ratio on the non-nursing-facility part of the Medicaid line, use-based nursing
    # facility, the other four medical lines as translate.py scales them
    ta = pd.read_csv(DERIVED / "translation_account.csv")
    ta = ta[ta.line.eq("medicaid_and_chip_other_medical")].set_index("spec")
    store = pickle.load(open(CACHE / "account_line_ests.pkl", "rb"))
    mline = "medicaid_and_chip_other_medical"
    base = float(line.target_bn)
    for spec in ["plain", "winsor_p995", "winsor_p999", "two_part_lognormal", "pooled_excl_2020_2021",
                 "pooled_cpi_all_items", "pooled_year_normalized"]:
        f = float(ta.loc[spec, "key_weighted_ratio"])
        se_f = float(ta.loc[spec, "se_ratio"])
        des, lines = store[spec]["design"], store[spec]["lines"]
        tb_m, f_m, T_m = lines[mline]
        if abs(tb_m - base) > 1e-9 or abs(f_m - f) > 1e-12:
            fail(f"{spec}: account_line_ests.pkl disagrees with translation_account.csv")
        others = [v for k, v in lines.items() if k != mline]
        if len(others) != 4:
            fail(f"{spec}: expected four other medical lines, found {len(others)}")
        total_bn = base + sum(tb for tb, _, _ in others)
        for lab, s in [("share ceiling", s_hi), ("share doubled", 2 * s_hi)]:
            mcd_change = (base - charged) * f + nf * s - base
            put("medicaid_line_combined", f"{spec}, nursing facility at {lab}: change in the $116.91bn line",
                mcd_change, "$bn", f"({base:.3f} - {charged:.3f}) x {f:.4f} + {nf} x {s:.4f} - {base:.3f}",
                se=(base - charged) * se_f)
            tot = mcd_change + sum(tb * (v - 1) for tb, v, _ in others)
            T = (base - charged) * T_m + sum(tb * Tk for tb, _, Tk in others)
            put("medical_lines_combined",
                f"{spec}, nursing facility at {lab}: change in all five medical lines (${total_bn:.2f}bn)",
                tot, "$bn", "Medicaid line as above + the other four lines' translate.py changes",
                se=float(np.sqrt(des.var(T))))
    _ok("combined Medicaid-line and five-line rows written")

    _header("2 emergency Medicaid")
    cbo = cbo_table()
    cbo.to_csv(DERIVED / "cbo_emergency_medicaid_table1.csv", index=False)
    params = json.loads(PARAMS.read_text())["unauthorized"]
    mex_share = {"ohss_jan2022": params["ohss_unauthorized_mexico_share_jan2022"]["value"] / 100,
                 "pew_2023": params["pew_unauthorized_mexico_share_2023_secondary"]["value"] / 100}
    dis = pd.read_csv(DERIVED / "disconfirmation.csv")
    q = "Medicaid $/person paid for people never reporting Medicaid, 2019-24"
    rec = dis[(dis.domain == "all_ages") & (dis.group == "mexican_origin") & (dis.quantity == q)].iloc[0]
    cells = pd.read_csv(DERIVED / "cps_cells.csv")
    union_pop = float(cells.union_persons.sum())
    r_mcd = json.loads(PARAMS.read_text())["meps_coverage"]["nhea_to_meps_ratio_medicaid"]["value"]
    meps_rec = rec.value * union_pop / 1e9
    put("emergency_medicaid", "MEPS-recorded Medicaid for union-equivalent people never reporting Medicaid",
        meps_rec, "$bn (2024 $, MEPS scale)", f"{rec.value:.2f} $/person x {union_pop:,.0f}",
        se=rec.se * union_pop / 1e9)
    put("emergency_medicaid", "same, scaled by the ledger's NHEA/MEPS Medicaid ratio", meps_rec * r_mcd,
        "$bn", f"x {r_mcd}")
    for _, r in cbo.iterrows():
        put("emergency_medicaid", f"CBO federal+state emergency Medicaid FY{r.fiscal_year}", r.total_m / 1e3, "$bn",
            "CBO letter 2 Oct 2024, Table 1 (CMS-64)")
    for fy in (2023, 2021):
        tot = float(cbo.loc[cbo.fiscal_year.eq(fy), "total_m"].iloc[0]) / 1e3
        for lab, sh in [("all of it", 1.0), ("OHSS 2022 Mexico share 44%", mex_share["ohss_jan2022"]),
                        ("Pew 2023 Mexico share 30%", mex_share["pew_2023"])]:
            put("emergency_medicaid", f"FY{fy} union-attributable ({lab}) minus what MEPS records",
                max(tot * sh - meps_rec, 0.0), "$bn", f"{tot:.3f} x {sh:.2f} - {meps_rec:.3f} (floored at 0)")
    audit["emergency_medicaid"] = {"cbo_total_fy2017_2023_m": int(cbo.total_m.sum()),
                                   "mexico_share_of_unauthorized": mex_share,
                                   "meps_recorded_bn": meps_rec}
    _ok(f"CBO FY2017-2023 ${cbo.total_m.sum() / 1e3:.1f}bn (FY2023 ${cbo.total_m.iloc[-1] / 1e3:.2f}bn, peak FY2021 "
        f"${cbo.total_m.max() / 1e3:.2f}bn); MEPS already records ${meps_rec:.2f}bn for the union-equivalent")

    _header("3 coverage key against dollars")
    pool = pd.read_parquet(CACHE / "pooled.parquet")
    v = pool[pool.PERWT.gt(0) & pool.AGE.ge(0) & pool.BORNUSA.isin([1, 2])]
    cov_rows = []
    for lab, s in [("pooled_2016_2024", v)] + [(str(y), v[v.year.eq(y)]) for y in range(2016, 2025)]:
        w = s.PERWT
        mex = s.HISPNCAT.eq(1)
        mcd = s.MCDEV.eq(1)
        cov_rows.append(dict(sample=lab, mexican_share_of_persons=float(w[mex].sum() / w.sum()),
                             mexican_share_of_medicaid_ever=float(w[mex & mcd].sum() / w[mcd].sum()),
                             mexican_share_of_medicaid_dollars=float((w * s.medicaid)[mex].sum() / (w * s.medicaid).sum())))
    cov = pd.DataFrame(cov_rows)
    ik = pd.read_csv(KEYS)
    ik = ik[ik.allocation.eq("personal")].set_index("key")
    cov.attrs = {}
    cps = {"union_share_of_population": float(ik.loc["population", "target_share"]),
           "union_share_of_reported_medicaid_coverage": float(ik.loc["medicaid_covered", "target_share"]),
           "union_share_of_meps_medicaid_key": float(ik.loc["medicaid", "target_share"])}
    cov.to_csv(DERIVED / "coverage_vs_dollars.csv", index=False)
    p = cov.iloc[0]
    for k, val in cps.items():
        put("coverage_key", f"CPS {k}", val, "share", "full_account_spending incidence_keys.csv, personal")
    for k in ["mexican_share_of_persons", "mexican_share_of_medicaid_ever", "mexican_share_of_medicaid_dollars"]:
        put("coverage_key", f"MEPS pooled {k}", float(p[k]), "share", "pooled.parquet, valid donors, PERWT")
    put("coverage_key", "MEPS dollars per Medicaid-covered person, Mexican-origin / all",
        float(p.mexican_share_of_medicaid_dollars / p.mexican_share_of_medicaid_ever), "ratio", "share of $ / share of covered")
    audit["coverage_key"] = {"cps": cps, "meps_pooled": {k: float(p[k]) for k in cov.columns if k != "sample"}}
    _ok(f"MEPS Mexican-origin share of Medicaid-covered {p.mexican_share_of_medicaid_ever:.3f} vs CPS union "
        f"{cps['union_share_of_reported_medicaid_coverage']:.3f}; share of MEPS Medicaid dollars "
        f"{p.mexican_share_of_medicaid_dollars:.3f}")

    pd.DataFrame(rows).to_csv(DERIVED / "bounds.csv", index=False)
    (DERIVED / "bounds_audit.json").write_text(json.dumps(audit, indent=2, default=float) + "\n")
    _ok("bounds.csv, cbo_emergency_medicaid_table1.csv, coverage_vs_dollars.csv, bounds_audit.json written")


if __name__ == "__main__":
    main()
