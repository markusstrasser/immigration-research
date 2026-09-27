"""Grade-4 immigrant-background exposure, cohort-matched to PISA.

Studies: PIRLS 2011, TIMSS 2011 (grade 4), TIMSS 2015 (grade 4), PIRLS 2016.

Two routes, both public, no account (IEA TIMSS & PIRLS International Study Center,
timssandpirls.bc.edu):
  1. Data almanacs (weighted % by country for every questionnaire item), one zip per
     study; parsed from the PDFs with poppler `pdftotext -layout`.
  2. TIMSS 2015 grade-4 SPSS microdata, student (ASG) and home (ASH) files only, fetched
     member-by-member with HTTP range requests (remotezip), for the joint
     "both parents born abroad" share and jackknife SEs. Only TIMSS 2015 asks parental
     birthplace; PIRLS 2011, TIMSS 2011 and PIRLS 2016 do not (see reads/grade4_exposure.md).

Usage (from the lane directory):
  uv run --no-project --with openpyxl --with pandas --with pyreadstat --with remotezip \
      python3 acquire_grade4.py --fetch      # network: fill _cache/grade4/
  uv run --no-project --with openpyxl --with pandas --with pyreadstat \
      python3 acquire_grade4.py              # build derived/grade4_exposure.csv from cache only

Output: derived/grade4_exposure.csv, columns country,study,cycle,definition,share,share_se,source.
share and share_se are percentages of grade-4 pupils with a valid response. Rows with
cycle "2011to2015" / "2011to2016" are changes in percentage points between the matched cycles.
"""
from __future__ import annotations

import csv
import re
import subprocess
import sys
import zipfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
CACHE = HERE / "_cache" / "grade4"
OUT = HERE / "derived" / "grade4_exposure.csv"
UA = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124.0 Safari/537.36"}
BASE = "https://timssandpirls.bc.edu/"

ALMANAC_ZIPS = {
    "P11_Almanacs.zip": "pirls2011/downloads/P11_Almanacs.zip",
    "T11_G4_Almanacs.zip": "timss2011/downloads/T11_G4_Almanacs.zip",
    "T15_G4_Almanacs.zip": "timss2015/international-database/downloads/T15_G4_Almanacs.zip",
    "P16_Almanacs.zip": "pirls2016/international-database/downloads/P16_Almanacs.zip",
}
# (zip, member) for the context almanacs we parse
ALMANAC_PDFS = {
    ("PIRLS", "2011", "home"): ("P11_Almanacs.zip", "P11_HomeAlmanac.pdf"),
    ("PIRLS", "2011", "student"): ("P11_Almanacs.zip", "P11_StudentAlmanac.pdf"),
    ("TIMSS", "2011", "home"): ("T11_G4_Almanacs.zip", "MAT/T11_G4_MAT_HomeAlmanac.pdf"),
    ("TIMSS", "2011", "student"): ("T11_G4_Almanacs.zip", "MAT/T11_G4_MAT_StudentAlmanac.pdf"),
    ("TIMSS", "2015", "home"): ("T15_G4_Almanacs.zip", "MAT/T15_G4_MAT_HomeAlmanac.pdf"),
    ("TIMSS", "2015", "student"): ("T15_G4_Almanacs.zip", "MAT/T15_G4_MAT_StudentAlmanac.pdf"),
    ("PIRLS", "2016", "home"): ("P16_Almanacs.zip", "Context Almanacs/P16_HomeAlmanac.pdf"),
    ("PIRLS", "2016", "student"): ("P16_Almanacs.zip", "Context Almanacs/P16_StudentAlmanac.pdf"),
}

# Almanac items: (study, cycle, questionnaire, variable) -> (definition, indices of the
# valid-% columns that count as "immigrant-background", number of valid categories).
# Valid % columns are the first n_valid percentage columns (they sum to 100).
ALMANAC_ITEMS = {
    ("PIRLS", "2011", "home", "ASBH03A"): ("no_test_language_before_school_parent", (1,), 2),
    ("TIMSS", "2011", "home", "ASBH03A"): ("no_test_language_before_school_parent", (1,), 2),
    ("TIMSS", "2015", "home", "ASBH04A"): ("no_test_language_before_school_parent", (1,), 2),
    ("PIRLS", "2016", "home", "ASBH04A"): ("no_test_language_before_school_parent", (1,), 2),
    # 2011: 1 always-or-almost-always, 2 sometimes, 3 never; 2015/16: 1 always, 2 almost always, 3 sometimes, 4 never
    ("PIRLS", "2011", "student", "ASBG03"): ("test_language_at_home_sometimes_or_never_student", (1, 2), 3),
    ("TIMSS", "2011", "student", "ASBG03"): ("test_language_at_home_sometimes_or_never_student", (1, 2), 3),
    ("TIMSS", "2015", "student", "ASBG03"): ("test_language_at_home_sometimes_or_never_student", (2, 3), 4),
    ("PIRLS", "2016", "student", "ASBG03"): ("test_language_at_home_sometimes_or_never_student", (2, 3), 4),
    ("TIMSS", "2015", "home", "ASBH03A"): ("child_born_abroad_parent", (1,), 2),
    ("PIRLS", "2016", "home", "ASBH03A"): ("child_born_abroad_parent", (1,), 2),
    ("TIMSS", "2015", "student", "ASBG07"): ("child_born_abroad_student", (1,), 2),
    ("TIMSS", "2015", "home", "ASBH17A"): ("father_born_abroad_parent", (1,), 2),
    ("TIMSS", "2015", "home", "ASBH17B"): ("mother_born_abroad_parent", (1,), 2),
}

# OECD members and European countries plus their sub-national benchmarking entities,
# as IEA names them in the almanacs.
KEEP = {
    "Australia", "Austria", "Belgium (Flemish)", "Belgium (French)", "Bulgaria", "Canada", "Chile",
    "Croatia", "Cyprus", "Czech Republic", "Denmark", "England", "Finland", "France", "Georgia",
    "Germany", "Hungary", "Iceland", "Ireland", "Israel", "Italy", "Japan", "Korea, Rep. of",
    "Latvia", "Lithuania", "Luxembourg", "Malta", "Netherlands", "New Zealand", "Northern Ireland",
    "Norway", "Norway (4)", "Norway (5)", "Poland", "Portugal", "Romania", "Russian Federation",
    "Serbia", "Slovak Republic", "Slovenia", "Spain", "Sweden", "Turkey", "United States",
    "Macedonia, Rep. of", "Estonia", "Greece", "Switzerland", "Albania", "Montenegro",
    "Mexico", "Colombia", "Costa Rica",
}
KEEP_SUFFIXES = (", Canada", ", Spain", ", US", ", Belgium", ", Denmark")

# TIMSS 2015 grade 4 microdata: 3-letter file code -> almanac country name
T15_CODES = {
    "AUS": "Australia", "BFL": "Belgium (Flemish)", "BGR": "Bulgaria", "HRV": "Croatia",
    "CAN": "Canada", "COT": "Ontario, Canada", "CQU": "Quebec, Canada", "CHL": "Chile",
    "CYP": "Cyprus", "CZE": "Czech Republic", "DEU": "Germany", "DNK": "Denmark",
    "ENG": "England", "FIN": "Finland", "FRA": "France", "GEO": "Georgia", "HUN": "Hungary",
    "IRL": "Ireland", "ITA": "Italy", "JPN": "Japan", "KOR": "Korea, Rep. of",
    "LTU": "Lithuania", "NLD": "Netherlands", "NIR": "Northern Ireland", "NZL": "New Zealand",
    "NOR": "Norway", "NO4": "Norway (4)", "POL": "Poland", "PRT": "Portugal",
    "RUS": "Russian Federation", "SRB": "Serbia", "SVK": "Slovak Republic", "SVN": "Slovenia",
    "ESP": "Spain", "SWE": "Sweden", "TUR": "Turkey", "USA": "United States",
}
T15_SPSS = "timss2015/international-database/downloads/T15_G4_SPSSData_pt{}.zip"

ROW_RE = re.compile(r"^\s*(\S.*?)\s{2,}(\d+)\s+(\d+|\.)\s+(.*)$")


def keep(name: str) -> bool:
    return name in KEEP or name.endswith(KEEP_SUFFIXES)


# ---------------------------------------------------------------- fetch (network)
def fetch() -> None:
    import urllib.request

    from remotezip import RemoteZip

    CACHE.mkdir(parents=True, exist_ok=True)
    for fname, path in ALMANAC_ZIPS.items():
        dest = CACHE / fname
        if not dest.exists():
            req = urllib.request.Request(BASE + path, headers=UA)
            with urllib.request.urlopen(req, timeout=600) as r:
                dest.write_bytes(r.read())
            print("fetched", fname, dest.stat().st_size)
    spss = CACHE / "t15_g4_spss"
    spss.mkdir(exist_ok=True)
    wanted = {f"AS{kind}{code}M6.sav" for code in T15_CODES for kind in ("G", "H")}
    for part in (1, 2, 3):
        with RemoteZip(BASE + T15_SPSS.format(part), headers=UA) as z:
            for info in z.infolist():
                name = info.filename.split("/")[-1].upper().replace(".SAV", ".sav")
                if name in wanted and not (spss / name).exists():
                    (spss / name).write_bytes(z.read(info))
                    print("fetched", part, name, info.file_size, flush=True)
    missing = sorted(w for w in wanted if not (spss / w).exists())
    print("missing members:", missing)


# ---------------------------------------------------------------- almanacs
def almanac_text(zname: str, member: str) -> str:
    with zipfile.ZipFile(CACHE / zname) as z:
        data = z.read(member)
    r = subprocess.run(["pdftotext", "-layout", "-", "-"], input=data, capture_output=True, check=True)
    return r.stdout.decode("utf-8", "replace")


def parse_almanac(text: str) -> dict[str, list[tuple[str, int, int, list[float | None]]]]:
    """variable -> [(country, sample, valid_n, percentages...)] for the first block of each variable."""
    out: dict[str, list] = {}
    var = None
    for line in text.splitlines():
        m = re.search(r"^Location\s*:.*\((\w+)\)", line)
        if m:
            var = m.group(1).upper()
            if var in out:  # a variable repeats on continuation pages; keep appending
                pass
            else:
                out[var] = []
            continue
        if line.startswith(("Question", "Progress in", "Trends in")) or "Almanac" in line:
            if line.startswith("Question") or "Almanac" in line:
                pass
            continue
        if var is None:
            continue
        m = ROW_RE.match(line)
        if not m:
            continue
        name = m.group(1).strip()
        if name.startswith(("International", "Country")):
            continue
        toks = m.group(4).split()
        if not all(t == "." or re.fullmatch(r"-?\d+(\.\d+)?", t) for t in toks):
            continue  # header or label line, not a data row
        vals = [None if t == "." else float(t) for t in toks]
        valid = None if m.group(3) == "." else int(m.group(3))
        if not any(r[0] == name for r in out[var]):
            out[var].append((name, int(m.group(2)), valid, vals))
    return out


def almanac_rows() -> list[dict]:
    rows = []
    parsed = {}
    for key, (zname, member) in ALMANAC_PDFS.items():
        parsed[key] = parse_almanac(almanac_text(zname, member))
    for (study, cycle, q, var), (defn, idx, nvalid) in ALMANAC_ITEMS.items():
        table = parsed[(study, cycle, q)].get(var)
        if not table:
            raise SystemExit(f"[BLOCKED] {study} {cycle} {q} almanac has no {var}")
        zname, member = ALMANAC_PDFS[(study, cycle, q)]
        for name, _sample, valid, vals in table:
            if not keep(name) or not valid or vals[0] is None:
                continue
            pct = vals[:nvalid]
            if abs(sum(pct) - 100) > 0.35:
                raise SystemExit(f"[BLOCKED] {study}{cycle} {var} {name}: valid % sum {sum(pct)}")
            rows.append({
                "country": name, "study": study, "cycle": cycle, "definition": defn,
                "share": round(sum(pct[i] for i in idx), 1), "share_se": "",
                "source": f"IEA almanac {zname}:{member} {var} valid N={valid}",
            })
    return rows


# ---------------------------------------------------------------- TIMSS 2015 microdata
def t15_microdata_rows() -> list[dict]:
    import numpy as np
    import pandas as pd
    import pyreadstat

    spss = CACHE / "t15_g4_spss"
    rows = []

    def est(y: np.ndarray, valid: np.ndarray, w: np.ndarray, zone: np.ndarray, rep: np.ndarray):
        def share(wt):
            den = wt[valid].sum()
            return 100.0 * wt[valid & (y == 1)].sum() / den if den > 0 else float("nan")
        full = share(w)
        # TIMSS 2015 JRR "includes both replicates within each sampling zone" (T15 User Guide,
        # ch. 4 fn. 8): per zone h two replicates (JKREP=1 doubled / JKREP=0 zeroed, and the
        # reverse); variance = 1/2 * sum over all replicates of squared deviations.
        sq = 0.0
        for h in np.unique(zone[zone > 0]):
            inz = zone == h
            for keep_rep in (1.0, 0.0):
                wr = w.copy()
                wr[inz] = w[inz] * 2.0 * (rep[inz] == keep_rep)
                sq += (share(wr) - full) ** 2
        return full, (0.5 * sq) ** 0.5, int(valid.sum())

    for code in sorted(T15_CODES):
        name = T15_CODES[code]
        gpath, hpath = spss / f"ASG{code}M6.sav", spss / f"ASH{code}M6.sav"
        if not gpath.exists():
            raise SystemExit(f"[BLOCKED] missing {gpath.name}; run --fetch")
        g, _ = pyreadstat.read_sav(str(gpath), usecols=[
            "IDSTUD", "TOTWGT", "JKZONE", "JKREP", "ASBG06A", "ASBG06B", "ASBG07"],
            user_missing=False)
        h, _ = pyreadstat.read_sav(str(hpath), usecols=["IDSTUD", "ASBH17A", "ASBH17B", "ASBH03A"]) \
            if hpath.exists() else (pd.DataFrame(columns=["IDSTUD", "ASBH17A", "ASBH17B", "ASBH03A"]), None)
        d = g.merge(h, on="IDSTUD", how="left")
        w = d["TOTWGT"].to_numpy(float)
        zone = d["JKZONE"].fillna(0).to_numpy(int)
        rep = d["JKREP"].fillna(0).to_numpy(float)
        src = f"IEA TIMSS 2015 G4 IDB T15_G4_SPSSData ASG{code}M6/ASH{code}M6, TOTWGT, JK2 75 zones"

        def both(a, b):
            a, b = d[a].to_numpy(float), d[b].to_numpy(float)
            yes_any = (a == 1) | (b == 1)
            both_no = (a == 2) & (b == 2)
            valid = yes_any | both_no
            return np.where(both_no, 1, 0), valid

        defs = {}
        defs["both_parents_born_abroad_student"] = both("ASBG06A", "ASBG06B")
        defs["both_parents_born_abroad_parent"] = both("ASBH17A", "ASBH17B")
        c = d["ASBG07"].to_numpy(float)
        defs["child_born_abroad_student_idb"] = (np.where(c == 2, 1, 0), (c == 1) | (c == 2))
        for defn, (y, valid) in defs.items():
            if valid.sum() < 100:
                continue
            s, se, n = est(y, valid, w, zone, rep)
            rows.append({"country": name, "study": "TIMSS", "cycle": "2015", "definition": defn,
                         "share": round(s, 2), "share_se": round(se, 2),
                         "source": f"{src}; valid n={n}"})
    return rows


# ---------------------------------------------------------------- changes
MATCH = {("PIRLS", "2016"): ("PIRLS", "2011"), ("TIMSS", "2015"): ("TIMSS", "2011")}


def change_rows(rows: list[dict]) -> list[dict]:
    idx = {(r["country"], r["study"], r["cycle"], r["definition"]): r for r in rows}
    out = []
    for (country, study, cycle, defn), r in sorted(idx.items()):
        if (study, cycle) not in MATCH:
            continue
        ps, pc = MATCH[(study, cycle)]
        prev = idx.get((country, ps, pc, defn))
        if prev is None:
            continue
        out.append({"country": country, "study": study, "cycle": f"{pc}to{cycle}", "definition": defn,
                    "share": round(float(r["share"]) - float(prev["share"]), 1), "share_se": "",
                    "source": f"difference of rows {study} {cycle} and {ps} {pc} (percentage points)"})
    return out


def main() -> None:
    if "--fetch" in sys.argv:
        fetch()
        return
    rows = almanac_rows()
    micro = t15_microdata_rows()
    # Cross-check: the microdata estimate of ASBG07 must reproduce the almanac's weighted %;
    # it then supplies the almanac row's jackknife SE and is dropped as a duplicate.
    alm = {(r["country"], r["definition"]): r for r in rows if r["study"] == "TIMSS" and r["cycle"] == "2015"}
    checked = 0
    for r in [m for m in micro if m["definition"] == "child_born_abroad_student_idb"]:
        a = alm.get((r["country"], "child_born_abroad_student"))
        if a is None:
            raise SystemExit(f"[BLOCKED] no almanac ASBG07 row for {r['country']}")
        if abs(float(a["share"]) - float(r["share"])) > 0.1:
            raise SystemExit(f"[BLOCKED] {r['country']} ASBG07 almanac {a['share']} vs IDB {r['share']}")
        a["share_se"] = r["share_se"]
        a["source"] += f"; SE from IDB ASG file JRR (IDB share {r['share']})"
        checked += 1
    micro = [m for m in micro if m["definition"] != "child_born_abroad_student_idb"]
    print(f"almanac-vs-IDB ASBG07 check passed for {checked} entities")
    rows += micro
    rows += change_rows(rows)
    rows.sort(key=lambda r: (r["country"], r["definition"], r["study"], r["cycle"]))
    OUT.parent.mkdir(exist_ok=True)
    cols = ["country", "study", "cycle", "definition", "share", "share_se", "source"]
    with open(OUT, "w", newline="") as f:
        wr = csv.writer(f, lineterminator="\n")
        wr.writerow(cols)
        for r in rows:
            wr.writerow([r[c] for c in cols])
    print(f"wrote {OUT} rows={len(rows)}")


if __name__ == "__main__":
    main()
