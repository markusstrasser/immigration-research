"""Build the Denver Public Schools (CDE district 0880) school x year panel.

Run from the repository root:

    OPENBLAS_NUM_THREADS=1 uv run --no-project python3 \
        infra/immigration-fiscal/newcomer_school_shock_2026_09_28/build_denver.py

Needs openpyxl (present in the repo .venv; in a fresh checkout drop --no-project or add
--with openpyxl). Reads only files in _cache/denver/, each pinned by sha256 in INPUTS below;
a missing or changed file raises (no fallback). Sources, definitions and suppression rules:
reads/denver_sources.md.

Writes
  derived/denver_schools.csv  one row per school x spring year (membership, EL, immigrant,
                              homeless, ESSA per-pupil expenditure, teacher FTE, PTR)
  derived/denver_scores.csv   CMAS ELA/math by school x year x language-proficiency group x
                              grade, school level only
  derived/denver_audit.json   input hashes, row counts, suppressed-cell counts, checks

Conventions
  year = spring year of the school year (2024-25 -> 2025; FY2024-25 -> 2025).
  school_id = CDE 4-digit school code (string).
  Published values are copied; suppressed cells ('*', 'N/A', '- -', '< 16', '< 4') are
  blank and counted in the audit. The only arithmetic: enroll_g3_8 (sum of published grade
  3-8 membership), ppe_federal / ppe_state_local (site + central share by source; a blank
  FY2019-20 site federal cell counts as 0 only where site total = site state/local), ptr_calc
  (PK-12 count / teacher FTE from the ratio file, unrounded; CDE rounds the published ratio to
  an integer from 2021-22), and integer parsing of 'N:1' ratio strings.
"""

import csv
import hashlib
import json
import os
import re
from collections import Counter, defaultdict

import openpyxl

LANE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(LANE, "_cache", "denver")
DERIVED = os.path.join(LANE, "derived")
DIST = "0880"
CITY = "denver"

INPUTS = {
    "cde_cmas_ela_disagg_2019.xlsx": "7ef4f0f267221db2b943ac0c00540d7039a8f87de8f09c37694161b69f466b23",
    "cde_cmas_ela_disagg_2021.xlsx": "c3cd8393df98616787c183d760a9b6def79a56e6016577accdb9b58230c278f5",
    "cde_cmas_ela_disagg_2022.xlsx": "470acb93784fed2dca9b7f346e0fb544cbdce27642afa525be88f0173da6dffb",
    "cde_cmas_ela_disagg_2023.xlsx": "c8046592408aa05440818b9953a063096e2a00f983bc80cecff55f2b56b741e3",
    "cde_cmas_ela_disagg_2024.xlsx": "37a85363b5e7daba162ca6951a78666b77a8a37f56f97d05095046d816542ec4",
    "cde_cmas_ela_disagg_2025.xlsx": "2fc233480639e63d94a2755f6b1702c96914d4679cc6d342bf32bb90efe52753",
    "cde_cmas_ela_disagg_2026.xlsx": "2f9be78842116d7674fd5b1b77000183a3136f4816b7d310242d510cc60ec575",
    "cde_cmas_ela_langprof_2017.xlsx": "ca79c8d3bca47359811666873d2366f35f6eff109806807618061371b1d2e023",
    "cde_cmas_ela_langprof_2018.xlsx": "6ef92ccc2d7871f650e74ca2ed1034e538530421591dc7ecae0bad3f33249bf1",
    "cde_cmas_math_disagg_2019.xlsx": "57d580076004faa60428be6be80ad26d1286e0cfcb16f351a6dc30c6904d70cf",
    "cde_cmas_math_disagg_2021.xlsx": "598037b751704244b1dbb8ebb958550fd66fdb69bfb8999f94446ddb06977f94",
    "cde_cmas_math_disagg_2022.xlsx": "b1f1f2cf0e30f507b649a0a995f997773ca0be16b4af90075c3d2c282c0b3483",
    "cde_cmas_math_disagg_2023.xlsx": "e828a56de7435a0844e49a3fbfa44dccd08f72beb17d247dd6ca4789946e2203",
    "cde_cmas_math_disagg_2024.xlsx": "505945024d23c90a219bc082b31dadff707848b32ab5271d7fa266731080bc24",
    "cde_cmas_math_disagg_2025.xlsx": "0c95e05b0557ef76b1279ac73e6add10f4185be0e93773bf3012315e91826ec8",
    "cde_cmas_math_disagg_2026.xlsx": "1117cd6540513408103c5288a24e50868ab282280ed8d3652dca0d081fbab112",
    "cde_cmas_math_langprof_2017.xlsx": "22ab4f7dfb22bd23fff24bcbd2586789b43b74aab0f28e629c553c590492aa84",
    "cde_cmas_math_langprof_2018.xlsx": "a3f0661aceca091b639c7d07f44ed15ed499aa91270226c87aeba1f9e6423842",
    "cde_cmas_overall_2017.xlsx": "fc1888047e435b7e545edcb05e4475a8f6d7c7d6ffe0a1ca128e894e67b0f6fa",
    "cde_cmas_overall_2018.xlsx": "22e6a523d41ada5c6a9d5d958fff33a39442237d072f12b765caa04655d7e25e",
    "cde_cmas_overall_2019.xlsx": "1f35cc5e4544fe9c842ddd76175f1b6cefe485a7765d5556b6c4bf4f0ef62c14",
    "cde_cmas_overall_2021.xlsx": "e2b09b64335cd01d5bc30fb78833b2773320adfc644cab6a9073ce41f943abd7",
    "cde_cmas_overall_2022.xlsx": "e6987f4752bb6351f931d69390508f0578b61777bc1e88c1677602a15e9c0864",
    "cde_cmas_overall_2023.xlsx": "d53fe2a5037d0f3268bc8eb8f130730b065c47e8ea71f736727e6ce7717fbf43",
    "cde_cmas_overall_2024.xlsx": "b7d8ab68bc9ea3ba7451f3ac8518a4c6437d92aa989a975187f60ede3ad3c590",
    "cde_cmas_overall_2025.xlsx": "4b98b24812f867ab62910400e3e9a69dfb3a65aa9b7ebb900841b7362f1e69f9",
    "cde_cmas_overall_2026.xlsx": "3e09dc291af72efcf5566855401fa2697bac5f1cf1fede3ac386765363236197",
    "cde_ft_essa_ppe_fy2019.xlsx": "6b188285bb7f8eb02b3b2013127c3bce05f6d2622e217d09b8269a0ff2c3473b",
    "cde_ft_essa_ppe_fy2020.xlsx": "9a2aefd2575b73e9effe21254c4a65dc6aa95f17e4a7d26e7d8daada9b7ef8e9",
    "cde_ft_essa_ppe_fy2021.xlsx": "fedc9bf454ec308c04bcc016469bee0f1084f6650abafe41908ac3515377d56d",
    "cde_ft_essa_ppe_fy2022.xlsx": "44b18646563fc8f77544e8e568936cdbc8072b0af32b7bda90023016b30acd0b",
    "cde_ft_essa_ppe_fy2023.xlsx": "c1ac0c850a858cd95892727f044d8ae7403e1097c87b8958419885006bb58271",
    "cde_ft_essa_ppe_fy2024.xlsx": "ff5e1da67df6f0ed1b0e05b70f183586ebb8d27123e7386ea50dc4926129a9e5",
    "cde_ft_essa_ppe_fy2025.xlsm": "b99f350becbc95145d73886e0768e42b8d0d3e4566e442abb86bd37202303087",
    "cde_pm_grade_school_2017.xlsx": "812973e1bfc54b4f2212ffb9ef893108e485723b3cdc5cb432f687ac66db22bc",
    "cde_pm_grade_school_2018.xlsx": "45455fccbe2c8eb3f92d0710c65aed69aa8b7fd5f79326400eb1c144652d887d",
    "cde_pm_grade_school_2019.xlsx": "80ac51d1b2e7a9b01e5b2b5bda86cd87d87e1bf53af9bbeb6efb13e9006d5dcc",
    "cde_pm_grade_school_2020.xlsx": "493f230cc3ca01ee1b4dc0f3d8292f2c95305fd12104a324c04c7fb8dc19eaba",
    "cde_pm_grade_school_2021.xlsx": "590f34fbe87c11e3c7ac4a93edec0af9979c79c8626a69ec992cb8979a54f42e",
    "cde_pm_grade_school_2022.xlsx": "e42c1c6cda98bdfd9d7095c4562865985a5d3d2cdf0fe2b814ac665e42182a7f",
    "cde_pm_grade_school_2023.xlsx": "4e9bee7596ccadf07b4b4a48cfada2a0eb9fbc667f909aa099915b72faf0f4de",
    "cde_pm_grade_school_2024.xlsx": "66ccbfd6c03c740b756fe267f978e1d1eb34cf94b1ae378ed82282eab726cc34",
    "cde_pm_grade_school_2025.xlsx": "ce0b2fc80bb824e35c16d938ebe92803202574d21629b1e1cd02180cd17680d0",
    "cde_pm_ipst_school_2017.xlsx": "6c11f3d00b6d4ebc02a47b1363cf164787f871f363cc130c4e8c7cdd44c8f741",
    "cde_pm_ipst_school_2018.xlsx": "05e692b41a81e80b13c5ede67d2f42371429e95e09daf5eb17bc6b4e1c25a3e2",
    "cde_pm_ipst_school_2019.xlsx": "1435b646f6072404ecc6ad482933a831f81ab22a0a36c52c4bdf43fc222ffa1d",
    "cde_pm_ipst_school_2020.xlsx": "34917745639fd2754b034fdbcc8e7802757dc30f275f0325f54d8d9372a54fb2",
    "cde_pm_ipst_school_2021.xlsx": "dd6577b214bc549c134460e4ccdc962fc7b0bdafa2e4f96cd2f5bbbde84837bd",
    "cde_pm_ipst_school_2022.xlsx": "8343381b0f9079d847d09d0415ca44b4d80c588b051ae80e914e507cc5586d67",
    "cde_pm_ipst_school_2023.xlsx": "ca3f1f35941af1da6fd10e589a8db27c5098133a146ec2b6e34fbaba54f1791d",
    "cde_pm_ipst_school_2024.xlsx": "42da20c56a5c80d20786c5f324c7c11cac52b43ba9b957c52d90e75abcf95f3e",
    "cde_pm_ipst_school_2025.xlsx": "08bc958d53ed0bccde66dd374e2e8118fdade5a24323540afdd8261684bd8707",
    "cde_pm_school_workbook_2026.xlsx": "38162e17b78748aa75832741b390eec1ffd9fcca7158896e57b8e24212a5d387",
    "cde_ptr_school_2017.xlsx": "6d97b5b29e721a028f801f2f82c4031c2851a8a12624affeda31546d4ca053bc",
    "cde_ptr_school_2018.xlsx": "5af653db5c5cd9bfc5bff59173e1ff2e865038631de37fea5451cc115c776d9a",
    "cde_ptr_school_2019.xlsx": "82ea5a6ba0b1c5df1a933f839b2d01c23162e6fb9484c80184bf845455f8830c",
    "cde_ptr_school_2020.xlsx": "aaf2e06062742bbf334672f146d65a9e12758c57052ecec9da532e683bc60f86",
    "cde_ptr_school_2021.xlsx": "46758df6912a617fcc336f35668916a58691be198194ae406a9436cfa9500f84",
    "cde_ptr_school_2022.xlsx": "92fae6d816a7013987d114c77a90d6574532ee046353f718cbf04fcaaf0f13b4",
    "cde_ptr_school_2023.xlsx": "306bb0cc1c382e921ae2569ce38c7c2469afc3d36a00786cc3035947383f4a26",
    "cde_ptr_school_2024.xlsx": "f9f11b2f1a2267748068d01bfc1a25903aa01efbc99c4439a06ae54f7eba788b",
    "cde_ptr_school_2025.xlsx": "4e53cd6637a6f3f3abde3e207e1b2b4782737056af0a7a9bd900b397c734fb5a",
    "cde_staff_ratio_workbook_2026.xlsx": "966645abe119392045565bddf58811977c6f66fd6b7cf78a80dd5943913125f3",
}

SUPPRESSION_MARKERS = {"*", "N/A", "- -", "--", "< 16", "<16", "< 4", "<4"}

# CMAS language-proficiency labels as published -> group code. 2017-2018 use the first five;
# 2019-2022 the 'EL:'/'Not EL:' labels; 2023-2026 the 'English Language Proficiency:' labels.
GROUP_CODES = {
    "NEP - Non English Proficient": "nep",
    "LEP - Limited English Proficient": "lep",
    "FEP - Fluent English Proficient": "fep",
    "PHLOTE/FELL/NA": "phlote_fell_na",
    "Unreported": "unreported",
    "English Learner (EL)": "el",
    "Not English Learner (Not EL)": "not_el",
    "EL: NEP (Not English Proficient)": "nep",
    "EL: LEP (Limited English Proficient)": "lep",
    "Not EL: FEP (Fluent English Proficient), FELL (Former English Language Learner)": "fep_fell",
    "Not EL: PHLOTE, NA, Not Reported": "phlote_na_nr",
    "English Language Proficiency: (NEP/LEP)": "el",
    "English Language Proficiency: (Not NEP/LEP)": "not_el",
    "NEP (Not English Proficient)": "nep",
    "LEP (Limited English Proficient)": "lep",
    "FEP (Fluent English Proficient), FELL (Former English Language Learner)": "fep_fell",
    "PHLOTE, NA, Not Reported": "phlote_na_nr",
}

MATH_COURSE_TESTS = {"Algebra I", "Geometry", "Algebra II", "Integrated I", "Integrated II", "Integrated III"}


# ---------------------------------------------------------------- helpers

def verify_inputs():
    hashes = {}
    for name, want in sorted(INPUTS.items()):
        path = os.path.join(CACHE, name)
        if not os.path.exists(path):
            raise FileNotFoundError(f"[BLOCKED] missing input {path}")
        got = hashlib.sha256(open(path, "rb").read()).hexdigest()
        if got != want:
            raise ValueError(f"[BLOCKED] sha256 mismatch for {name}: {got} != {want}")
        hashes[name] = got
    return hashes


def norm(h):
    return " ".join(str(h).split()) if h is not None else None


def code4(v):
    """CDE district/school codes: published as '0880' strings or as integers (880)."""
    if v is None:
        return None
    s = str(v).strip()
    if s.endswith(".0"):
        s = s[:-2]
    return s.zfill(4) if s.isdigit() else s


def parse_value(v):
    """Return (number or None, marker or None). Strings like ' 1,234' or '.094' parse."""
    if v is None:
        return None, None
    if isinstance(v, bool):
        return None, str(v)
    if isinstance(v, (int, float)):
        return v, None
    s = str(v).strip()
    if s == "":
        return None, None
    if s in SUPPRESSION_MARKERS:
        return None, s
    t = s.replace(",", "")
    try:
        f = float(t)
        return (int(f) if re.fullmatch(r"-?\d+", t) else f), None
    except ValueError:
        return None, s


def fmt(x):
    if x is None:
        return ""
    if isinstance(x, bool):
        return str(int(x))
    if isinstance(x, int):
        return str(x)
    if isinstance(x, float):
        if x == int(x) and abs(x) < 1e15:
            return str(int(x))
        s = f"{x:.4f}".rstrip("0").rstrip(".")
        return s
    return str(x)


def sheet_rows(fname, sheet=None, header_keys=("Level",)):
    """Yield (header_index, row) for rows after the first row containing a header key."""
    wb = openpyxl.load_workbook(os.path.join(CACHE, fname), read_only=True, data_only=True)
    ws = wb[sheet] if sheet else wb.worksheets[0]
    ws.reset_dimensions()  # some CDE files carry a wrong stored dimension (A1:A1)
    idx = None
    for r in ws.iter_rows(values_only=True):
        if idx is None:
            cells = [norm(c) for c in r]
            if any(c in header_keys for c in cells if c):
                idx = {}
                for j, c in enumerate(cells):
                    if c is not None and c not in idx:
                        idx[c] = j  # first occurrence wins (later duplicates are prior years)
            continue
        yield idx, r
    wb.close()
    if idx is None:
        raise ValueError(f"no header row found in {fname} / {sheet}")


def pick(idx, *names):
    for n in names:
        if n in idx:
            return idx[n]
    return None


def get(r, j):
    return r[j] if j is not None and j < len(r) else None


YEAR_HEADERS = ("School Year", "Fiscal_year", "Fiscal_Year", "FISCAL_YEAR")


def tally(audit, name, ok):
    """Count a consistency check as equal / differs / not_checkable (ok is None); return ok."""
    audit["check_tallies"][f"{name}:{'not_checkable' if ok is None else 'equal' if ok else 'differs'}"] += 1
    return ok


def check_year(idx, r, year, fname, audit):
    """Where a file carries a school/fiscal-year column, its label must end in the spring year."""
    j = pick(idx, *YEAR_HEADERS)
    if j is None:
        return
    label = str(get(r, j) or "").strip()
    m = re.search(r"(\d{4})$", label)
    if not m or int(m.group(1)) != year:
        raise ValueError(f"{fname}: year label {label!r} does not end in {year}")
    audit["year_labels"][f"{fname}:{label}"] += 1


# ---------------------------------------------------------------- membership

IPST_FIELDS = {
    "enroll_total": ("PK-12 Count", "Total PK-12 Pupil Membership", "PK-12 Pupil Membership"),
    "el_n": ("EL Count", "EL Count Including FEP Monitor Year 1 and Year 2",
             "Multilingual Learner: NEP, LEP, FEP Monitor Year 1 and Monitor Year 2 Count"),
    "el_pct": ("EL Pct", "EL Including FEP Monitor Year 1 and Year 2 Pct",
               "Multilingual Learner: NEP, LEP, FEP Monitor Year 1 and Monitor Year 2 Percent"),
    "el_neplep_n": ("EL Count (NEP/LEP Only)", "Multilingual Learner: NEP/LEP Only Count"),
    "el_neplep_pct": ("EL (NEP/LEP Only) Pct", "Multilingual Learner: NEP/LEP Only Percent"),
    "fep_exited_n": ("EL FEP Exited Year 1 and Year 2 Count",
                     "Multilingual Learner: FEP Exited Year 1 and Exited Year 2 Count"),
    "immigrant_n": ("Immigrant Count",),
    "immigrant_pct": ("Immigrant Pct", "Immigrant Percent"),
    "migrant_n": ("Migrant Count",),
    "homeless_n": ("Homeless Count",),
    "homeless_pct": ("Homeless Pct", "Homeless Percent"),
}
CODE_HEADERS = ("Distr Code", "District Code", "Organization Code", "Dist Code", "Dist_Code", "LEA", "LEA Code")
SCHOOL_HEADERS = ("Sch Code", "School Code")


def load_ipst(audit):
    out = {}
    files = [(y, f"cde_pm_ipst_school_{y}.xlsx", None) for y in range(2017, 2026)]
    files.append((2026, "cde_pm_school_workbook_2026.xlsx", "IPST"))
    for year, fname, sheet in files:
        n = 0
        for idx, r in sheet_rows(fname, sheet, header_keys=CODE_HEADERS):
            jd, js = pick(idx, *CODE_HEADERS), pick(idx, *SCHOOL_HEADERS)
            if code4(get(r, jd)) != DIST:
                continue
            sid = code4(get(r, js))
            if sid in (None, "0000"):
                continue
            check_year(idx, r, year, fname, audit)
            rec = {"school_name": str(get(r, pick(idx, "School Name")) or "").strip()}
            for field, names in IPST_FIELDS.items():
                j = pick(idx, *names)
                if j is None:
                    rec[field] = None
                    continue
                v, m = parse_value(get(r, j))
                rec[field] = v
                if m:
                    audit["suppressed_membership"][f"{year}:{field}:{m}"] += 1
            out[(sid, year)] = rec
            n += 1
        audit["rows_in"][f"ipst:{year}"] = n
    return out


def load_grades(audit):
    out = {}
    files = [(y, f"cde_pm_grade_school_{y}.xlsx", None) for y in range(2017, 2026)]
    files.append((2026, "cde_pm_school_workbook_2026.xlsx", "Grade"))
    for year, fname, sheet in files:
        n = 0
        for idx, r in sheet_rows(fname, sheet, header_keys=CODE_HEADERS):
            jd, js = pick(idx, *CODE_HEADERS), pick(idx, *SCHOOL_HEADERS)
            if code4(get(r, jd)) != DIST:
                continue
            sid = code4(get(r, js))
            if sid in (None, "0000"):
                continue
            grade_cols = [k for k in idx if k in ("Pre-K", "Half-Day K", "Full-Day K", "Half-Day Kinder",
                                                  "Full-Day Kinder", "1st", "2nd", "3rd", "4th", "5th",
                                                  "6th", "7th", "8th", "9th", "10th", "11th", "12th")]
            vals = {}
            for k in grade_cols:
                raw = get(r, idx[k])
                # in the 2025-26 workbook '-' marks a grade with no pupils; the row-sum check
                # below confirms the reading (published PK-12 Count = sum of grade cells)
                if isinstance(raw, str) and raw.strip() == "-":
                    vals[k] = 0
                    continue
                v, m = parse_value(raw)
                if m:
                    audit["suppressed_membership"][f"{year}:grade_{k}:{m}"] += 1
                vals[k] = v
            total, _ = parse_value(get(r, pick(idx, "PK-12 Count")))
            if all(vals[k] is not None for k in grade_cols) and total is not None:
                if not tally(audit, f"grade_cells_sum_vs_pk12:{year}", sum(vals.values()) == total):
                    audit["checks"]["grade_row_sum_ne_pk12"].append(f"{year}:{sid}")
            else:
                tally(audit, f"grade_cells_sum_vs_pk12:{year}", None)
            g38 = [vals.get(k) for k in ("3rd", "4th", "5th", "6th", "7th", "8th")]
            out[(sid, year)] = {
                "enroll_g3_8": sum(g38) if all(v is not None for v in g38) else None,
                "enroll_total_gradefile": total,
                "school_name": str(get(r, pick(idx, "School Name")) or "").strip(),
            }
            n += 1
        audit["rows_in"][f"grade:{year}"] = n
    return out


# ---------------------------------------------------------------- staff (pupil-teacher ratio)

def load_ptr(audit):
    out = {}
    files = [(y, f"cde_ptr_school_{y}.xlsx", None) for y in range(2017, 2026)]
    files.append((2026, "cde_staff_ratio_workbook_2026.xlsx", "Teacher by School"))
    for year, fname, sheet in files:
        n = 0
        for idx, r in sheet_rows(fname, sheet, header_keys=("School Code",)):
            jd, js = pick(idx, *CODE_HEADERS), pick(idx, *SCHOOL_HEADERS)
            if code4(get(r, jd)) != DIST:
                continue
            sid = code4(get(r, js))
            if sid in (None, "0000"):
                continue
            check_year(idx, r, year, fname, audit)
            enr, m1 = parse_value(get(r, pick(idx, "PK-12 Count", "Enrollment Count")))
            fte, m2 = parse_value(get(r, pick(idx, "Teacher FTE")))
            raw_ratio = get(r, pick(idx, "Pupil/Teacher FTE Ratio", "Pupil/ Teacher FTE Ratio", "Pupil/Teacher Ratio"))
            ratio, m3, ratio_form = None, None, ""
            if isinstance(raw_ratio, str) and re.fullmatch(r"\s*\d+\s*:\s*1\s*", raw_ratio):
                ratio, ratio_form = int(raw_ratio.split(":")[0]), "integer N:1 as published"
            else:
                ratio, m3 = parse_value(raw_ratio)
                ratio_form = "decimal as published" if ratio is not None else ""
            for f, m in (("ptr_enroll", m1), ("teacher_fte", m2), ("pupil_teacher_ratio", m3)):
                if m:
                    audit["suppressed_staff"][f"{year}:{f}:{m}"] += 1
            # [CALCULATION] same definition as the published ratio, unrounded in every year
            calc = enr / fte if enr is not None and fte else None
            if calc is not None and ratio is not None:
                tol = 0.5001 if ratio_form.startswith("integer") else 0.01
                if not tally(audit, f"ptr_published_vs_enroll_over_fte:{year}", abs(calc - ratio) <= tol):
                    audit["checks"]["ptr_published_ne_enroll_over_fte"].append(f"{year}:{sid}")
            else:
                tally(audit, f"ptr_published_vs_enroll_over_fte:{year}", None)
            out[(sid, year)] = {"ptr_enroll": enr, "teacher_fte": fte, "pupil_teacher_ratio": ratio,
                                "ptr_ratio_form": ratio_form, "ptr_calc": calc,
                                "school_name": str(get(r, pick(idx, "School Name")) or "").strip()}
            n += 1
        audit["rows_in"][f"ptr:{year}"] = n
    return out


# ---------------------------------------------------------------- ESSA per-pupil expenditure

PPE_FIELDS = {
    "ppe_membership": ("Membership",),
    "ppe_site_federal": ("Site Level - Federal", "Site level - Federal"),
    "ppe_site_state_local": ("Site Level - State/Local", "Site level - State/Local"),
    "ppe_site_total": ("Site Level Total",),
    "ppe_central_federal": ("Site Share of Central Expenditures - Federal",),
    "ppe_central_state_local": ("Site Share of Central Expenditures - State/Local",),
    "ppe_central_total": ("Site Share of Central Expenditures - Total",),
    "ppe_total": ("Total School Expenditures",),
}


def load_ppe(audit):
    out = {}
    files = [(y, f"cde_ft_essa_ppe_fy{y}.xlsx") for y in range(2019, 2025)] + [(2025, "cde_ft_essa_ppe_fy2025.xlsm")]
    for year, fname in files:
        n = 0
        for idx, r in sheet_rows(fname, None, header_keys=("Dist Code", "Dist_Code")):
            if code4(get(r, pick(idx, "Dist Code", "Dist_Code"))) != DIST:
                continue
            sid = code4(get(r, pick(idx, "School Code", "Sch_Code")))
            if sid in (None, "0000"):
                continue
            check_year(idx, r, year, fname, audit)  # FY2021 title row says FY2021-2022; rows say 2020-2021
            rec = {"school_name": str(get(r, pick(idx, "School Name", "School_Name", "Sch_Name")) or "").strip()}
            ch = get(r, pick(idx, "Charter School", "Charter School?"))
            rec["ppe_charter_flag"] = str(ch).strip() if ch not in (None, "") else ""
            for field, names in PPE_FIELDS.items():
                v, m = parse_value(get(r, pick(idx, *names)))
                rec[field] = v
                if m:
                    audit["suppressed_ppe"][f"{year}:{field}:{m}"] += 1
            sf, cf = rec["ppe_site_federal"], rec["ppe_central_federal"]
            ss, cs = rec["ppe_site_state_local"], rec["ppe_central_state_local"]
            st = rec["ppe_site_total"]
            if sf is None and ss is not None and st is not None and abs(st - ss) < 0.5:
                # FY2019-20 leave 'Site Level - Federal' blank where the published site total equals the
                # site state/local amount; the blank is then zero by the file's own identity. The
                # published column stays blank; only the ppe_federal sum reads it as 0.
                sf = 0
                tally(audit, f"ppe_blank_site_federal_zero_by_identity:{year}", True)
            rec["ppe_federal"] = sf + cf if sf is not None and cf is not None else None
            rec["ppe_state_local"] = ss + cs if ss is not None and cs is not None else None
            if rec["ppe_federal"] is not None and rec["ppe_state_local"] is not None and rec["ppe_total"] is not None:
                # published components are whole dollars in most years: allow $2 of rounding
                ok = abs(rec["ppe_federal"] + rec["ppe_state_local"] - rec["ppe_total"]) <= 2
                if not tally(audit, f"ppe_components_vs_total:{year}", ok):
                    audit["checks"]["ppe_parts_ne_total"].append(f"{year}:{sid}")
            else:
                tally(audit, f"ppe_components_vs_total:{year}", None)
            out[(sid, year)] = rec
            n += 1
        audit["rows_in"][f"ppe:{year}"] = n
    return out


# ---------------------------------------------------------------- CMAS

def cmas_files():
    """(year, subject or None, file, sheet, kind)."""
    out = []
    for y in (2017, 2018, 2019, 2021, 2022, 2023, 2024, 2025, 2026):
        out.append((y, None, f"cde_cmas_overall_{y}.xlsx", None, "overall"))
        for subj in ("ela", "math"):
            if y <= 2018:
                out.append((y, subj, f"cde_cmas_{subj}_langprof_{y}.xlsx", None, "langprof"))
            else:
                out.append((y, subj, f"cde_cmas_{subj}_disagg_{y}.xlsx", "Language Proficiency", "langprof"))
    return out


def subject_of(content, test, fixed):
    if fixed:
        return fixed
    c = str(content or test or "")
    if c.startswith(("ELA", "English Language Arts")):
        return "ela"
    if c.startswith(("Math", "Mathematics")):
        return "math"
    return None  # Spanish Language Arts (CSLA) and anything else


def grade_of(label):
    s = str(label).strip()
    if s == "All Grades":
        return "all"
    m = re.search(r"Grade 0?(\d{1,2})$", s)
    if m:
        return m.group(1)
    if re.fullmatch(r"0?\d{1,2}", s):
        return str(int(s))
    return None


def load_cmas(audit):
    rows = {}
    for year, fixed_subj, fname, sheet, kind in cmas_files():
        wb_sheet = sheet
        if kind == "overall":
            wb = openpyxl.load_workbook(os.path.join(CACHE, fname), read_only=True)
            names = [ws.title for ws in wb.worksheets]
            wb.close()
            wb_sheet = next((s for s in names if "ELA" in s or "Detail" in s), names[0])
        n = 0
        for idx, r in sheet_rows(fname, wb_sheet, header_keys=("Level",)):
            if str(get(r, idx["Level"]) or "").strip().upper() != "SCHOOL":
                continue
            if code4(get(r, pick(idx, "District Code", "District Number"))) != DIST:
                continue
            sid = code4(get(r, pick(idx, "School Code", "School Number")))
            grade_label = get(r, pick(idx, "Grade", "Test/Grade", "Test"))
            content = get(r, pick(idx, "Content", "Subject"))
            subj = subject_of(content, grade_label, fixed_subj)
            if subj is None:
                audit["cmas_skipped"][f"{year}:non_ela_math:{content}"] += 1
                continue
            gl = str(grade_label).strip()
            if gl in MATH_COURSE_TESTS:
                audit["cmas_skipped"][f"{year}:{subj}:course_test"] += 1
                continue
            grade = grade_of(gl)
            if grade is None or (grade not in ("all",) and not (3 <= int(grade) <= 8)):
                audit["cmas_skipped"][f"{year}:{subj}:grade_{gl}"] += 1
                continue
            if grade == "all":
                # 2018 math 'All Grades' includes Algebra I/Geometry/Integrated takers
                grade = "3-8+courses" if (year == 2018 and subj == "math") else "3-8"
            if kind == "overall":
                group, group_label = "all", "All Students"
            else:
                group_label = str(get(r, idx["Language Proficiency"])).strip()
                if group_label not in GROUP_CODES:
                    raise ValueError(f"unmapped language proficiency label {group_label!r} in {fname}")
                group = GROUP_CODES[group_label]
            pct_j = pick(idx, "Percent Met or Exceeded Expectations", "% Met or Exceeded Expectations")
            if pct_j is None:
                pct_j = pick(idx, str(year))  # 2022+ overall files: column headed by the year
            fields = {
                "n_records": pick(idx, "Number of Total Records", "# of Total Records"),
                "n_tested": pick(idx, "Number of Valid Scores", "# of Valid Scores"),
                "participation_rate": pick(idx, "Participation Rate", f"Participation Rate {year}"),
                "mean_scale_score": pick(idx, "Mean Scale Score"),
                "sd_scale_score": pick(idx, "Standard Deviation"),
                "n_met_exceeded": pick(idx, "Number Met or Exceeded Expectations", "# Met or Exceeded Expectations"),
                "pct_proficient": pct_j,
            }
            rec = {"school_name": str(get(r, pick(idx, "School Name")) or "").strip(),
                   "group_label": group_label, "grade_label": gl, "source_file": fname}
            for f, j in fields.items():
                v, m = parse_value(get(r, j)) if j is not None else (None, None)
                rec[f] = v
                rec[f + "_note"] = m or ""
                if m:
                    audit["suppressed_cmas"][f"{year}:{f}:{m}"] += 1
            key = (sid, year, subj, group, grade)
            if key in rows:
                raise ValueError(f"duplicate CMAS key {key} in {fname}")
            rows[key] = rec
            n += 1
        audit["rows_in"][f"cmas:{year}:{fixed_subj or 'overall'}"] = n
    return rows


# ---------------------------------------------------------------- write

SCHOOL_COLS = ["city", "school_id", "school_name", "year", "enroll_total", "el_n", "el_pct", "nep_n", "lep_n",
               "newcomer_n", "homeless_n", "ppe_total", "ppe_federal", "ppe_state_local", "teacher_fte",
               "pupil_teacher_ratio", "class_size_avg",
               # additional published fields
               "el_neplep_n", "el_neplep_pct", "fep_exited_n", "immigrant_n", "immigrant_pct", "migrant_n",
               "homeless_pct", "enroll_g3_8", "ptr_enroll", "ptr_ratio_form", "ptr_calc", "ppe_membership",
               "ppe_site_federal", "ppe_site_state_local", "ppe_site_total", "ppe_central_federal",
               "ppe_central_state_local", "ppe_central_total", "ppe_charter_flag",
               "in_membership", "in_ptr", "in_ppe"]

SCORE_COLS = ["city", "school_id", "school_name", "year", "subject", "group", "group_label", "grade", "grade_label",
              "n_records", "n_records_note", "n_tested", "n_tested_note", "participation_rate",
              "participation_rate_note", "mean_scale_score", "mean_scale_score_note", "sd_scale_score",
              "sd_scale_score_note", "n_met_exceeded", "n_met_exceeded_note", "pct_proficient",
              "pct_proficient_note", "source_file"]


def grade_sort(g):
    return (0, int(g)) if g.isdigit() else (1, g)


PARTITIONS = {  # language-proficiency groups that together make up all tested students
    "2017-2018": ("nep", "lep", "fep", "phlote_fell_na", "unreported"),
    "2019+": ("el", "not_el"),
}


def cmas_checks(cmas, audit):
    """Two structural checks, counted (not enforced): the 'All Grades' row against the sum of its
    grade rows, and the all-students row against the sum of the language-proficiency partition.
    A missing row counts as zero students; a suppressed cell makes the comparison not checkable."""
    cells = defaultdict(dict)
    for (sid, year, subj, group, grade), rec in cmas.items():
        cells[(sid, year, subj, group)][grade] = rec
    for (sid, year, subj, group), by_grade in sorted(cells.items()):
        tot_key = next((g for g in by_grade if not g.isdigit()), None)
        if tot_key is None:
            continue
        parts = [rec for g, rec in by_grade.items() if g.isdigit()]
        for f in ("n_records", "n_tested"):
            name = f"cmas_all_grades_vs_grade_sum:{tot_key}:{f}"
            tot = by_grade[tot_key][f]
            if tot is None or any(p[f] is None for p in parts):
                tally(audit, name, None)
                continue
            if not tally(audit, name, sum(p[f] for p in parts) == tot) and tot_key == "3-8":
                audit["checks"]["cmas_all_grades_ne_sum_of_grades"].append(f"{year}:{subj}:{group}:{sid}:{f}")
    keys = {(sid, year, subj, grade) for (sid, year, subj, group, grade) in cmas}
    for sid, year, subj, grade in sorted(keys):
        allrec = cmas.get((sid, year, subj, "all", grade))
        if allrec is None or allrec["n_records"] is None:
            continue
        part = PARTITIONS["2017-2018" if year <= 2018 else "2019+"]
        recs = [cmas.get((sid, year, subj, g, grade)) for g in part]
        if all(r is None for r in recs):
            continue
        name = f"cmas_all_students_vs_language_partition:{year}:n_records"
        if any(r is not None and r["n_records"] is None for r in recs):
            tally(audit, name, None)
            continue
        if not tally(audit, name, sum(r["n_records"] for r in recs if r is not None) == allrec["n_records"]):
            audit["checks"]["cmas_all_ne_language_partition"].append(f"{year}:{subj}:{grade}:{sid}")
    # 2019 on: 'EL' should equal NEP + LEP and 'Not EL' should equal FEP/FELL + PHLOTE/NA/Not Reported
    for sid, year, subj, grade in sorted(keys):
        if year < 2019:
            continue
        for parent, kids in (("el", ("nep", "lep")), ("not_el", ("fep_fell", "phlote_na_nr"))):
            recs = [cmas.get((sid, year, subj, g, grade)) for g in (parent,) + kids]
            if recs[0] is None:
                continue
            name = f"cmas_{parent}_vs_subgroups:{year}:n_records"
            if any(r is not None and r["n_records"] is None for r in recs):
                tally(audit, name, None)
                continue
            parts = sum(r["n_records"] for r in recs[1:] if r is not None)
            if not tally(audit, name, parts == recs[0]["n_records"]):
                audit["checks"][f"cmas_{parent}_ne_subgroups"].append(f"{year}:{subj}:{grade}:{sid}")


def main():
    audit = {"inputs_sha256": verify_inputs(), "rows_in": {}, "rows_out": {},
             "suppressed_membership": Counter(), "suppressed_staff": Counter(), "suppressed_ppe": Counter(),
             "suppressed_cmas": Counter(), "cmas_skipped": Counter(), "year_labels": Counter(),
             "check_tallies": Counter(), "checks": defaultdict(list)}
    ipst, grades, ptr, ppe = load_ipst(audit), load_grades(audit), load_ptr(audit), load_ppe(audit)
    cmas = load_cmas(audit)
    cmas_checks(cmas, audit)

    keys = sorted(set(ipst) | set(ptr) | set(ppe), key=lambda k: (k[0], k[1]))
    school_rows = []
    for sid, year in keys:
        a, g, p, e = ipst.get((sid, year), {}), grades.get((sid, year), {}), ptr.get((sid, year), {}), ppe.get((sid, year), {})
        if a and g and a.get("enroll_total") is not None and g.get("enroll_total_gradefile") is not None:
            if not tally(audit, f"pk12_ipst_vs_gradefile:{year}", a["enroll_total"] == g["enroll_total_gradefile"]):
                audit["checks"]["ipst_pk12_ne_gradefile_pk12"].append(f"{year}:{sid}")
        elif a or g:
            tally(audit, f"pk12_ipst_vs_gradefile:{year}", None)
        name = a.get("school_name") or g.get("school_name") or p.get("school_name") or e.get("school_name") or ""
        row = {"city": CITY, "school_id": sid, "school_name": name, "year": year,
               "nep_n": None, "lep_n": None, "newcomer_n": None, "class_size_avg": None,
               "in_membership": int(bool(a)), "in_ptr": int(bool(p)), "in_ppe": int(bool(e))}
        for f in IPST_FIELDS:
            row[f] = a.get(f)
        row["enroll_g3_8"] = g.get("enroll_g3_8")
        for f in ("ptr_enroll", "teacher_fte", "pupil_teacher_ratio", "ptr_ratio_form", "ptr_calc"):
            row[f] = p.get(f)
        if a.get("enroll_total") is not None and p.get("ptr_enroll") is not None:
            if not tally(audit, f"pk12_ipst_vs_ptrfile:{year}", a["enroll_total"] == p["ptr_enroll"]):
                audit["checks"]["pk12_ipst_ne_ptrfile"].append(f"{year}:{sid}")
        for f in list(PPE_FIELDS) + ["ppe_federal", "ppe_state_local", "ppe_charter_flag"]:
            row[f] = e.get(f)
        if a.get("enroll_total") is not None and e.get("ppe_membership") is not None:
            # does the ESSA file's 'Membership' equal the October PK-12 count of the same school year?
            tally(audit, f"ppe_membership_vs_october_pk12:{year}", a["enroll_total"] == e["ppe_membership"])
        school_rows.append(row)

    score_rows = []
    for (sid, year, subj, group, grade), rec in sorted(
            cmas.items(), key=lambda kv: (kv[0][0], kv[0][1], kv[0][2], kv[0][3], grade_sort(kv[0][4]))):
        row = {"city": CITY, "school_id": sid, "year": year, "subject": subj, "group": group, "grade": grade}
        row.update(rec)
        score_rows.append(row)

    os.makedirs(DERIVED, exist_ok=True)
    with open(os.path.join(DERIVED, "denver_schools.csv"), "w", newline="") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(SCHOOL_COLS)
        for row in school_rows:
            w.writerow([fmt(row.get(c)) for c in SCHOOL_COLS])
    with open(os.path.join(DERIVED, "denver_scores.csv"), "w", newline="") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(SCORE_COLS)
        for row in score_rows:
            w.writerow([fmt(row.get(c)) for c in SCORE_COLS])

    by_year = Counter(r["year"] for r in school_rows)
    audit["rows_out"]["denver_schools_by_year"] = {str(k): v for k, v in sorted(by_year.items())}
    sy = Counter((r["year"], r["subject"], r["group"]) for r in score_rows)
    audit["rows_out"]["denver_scores_by_year_subject_group"] = {f"{y}:{s}:{g}": v for (y, s, g), v in sorted(sy.items())}
    filled = defaultdict(Counter)
    for r in school_rows:
        for c in SCHOOL_COLS[4:]:
            if r.get(c) not in (None, ""):
                filled[r["year"]][c] += 1
    audit["rows_out"]["denver_schools_nonblank_by_year"] = {str(y): dict(sorted(c.items())) for y, c in sorted(filled.items())}
    for k in ("suppressed_membership", "suppressed_staff", "suppressed_ppe", "suppressed_cmas", "cmas_skipped",
              "year_labels", "check_tallies"):
        audit[k] = dict(sorted(audit[k].items()))
    audit["checks"] = {k: sorted(v) for k, v in sorted(audit["checks"].items())}
    with open(os.path.join(DERIVED, "denver_audit.json"), "w") as f:
        json.dump(audit, f, indent=1, sort_keys=True)
        f.write("\n")
    print("schools rows:", len(school_rows), "score rows:", len(score_rows))
    print("checks:", {k: len(v) for k, v in audit["checks"].items()})


if __name__ == "__main__":
    main()
