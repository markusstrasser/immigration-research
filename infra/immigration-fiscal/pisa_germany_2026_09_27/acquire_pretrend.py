"""Build derived/pretrend_inputs.csv: PISA non-immigrant means and immigrant shares, 2006 and 2009.

Reads only cached OECD StatLink workbooks in _cache/ (fetched by curl from doi.org -> statlinks.oecdcode.org):
  statlink_888933433226.xlsx  PISA 2015 Vol I, Annex B1.7: Table I.7.1 (shares 2006, 2015),
                              Tables I.7.15a/b/c (science/reading/math by immigrant background, 2006 and 2015)
  statlink_888934038742.xlsx  PISA 2018 Vol II, Annex B1.9: Table II.B1.9.9 (shares 2009, 2018),
                              Table II.B1.9.10 (reading by immigrant background, 2009 and 2018)
  statlink_888932381418.xls   PISA 2009 Vol II, Annex B1: Table II.4.1 (reading by immigrant status, 2009).
                              Used as a cross-check and as a fallback for countries the 2018 volume does not list.
  statlink_888932964927.xls   PISA 2012 Vol II, Annex B1.3: Table II.3.4a (math by immigrant background, 2012).
                              Written as cycle-2012 math rows, a cross-check against derived/crosscountry.csv.

Run from the lane directory:
  uv run --no-project --with openpyxl --with xlrd python3 acquire_pretrend.py
"""

import csv
import re
from pathlib import Path

import openpyxl
import xlrd

HERE = Path(__file__).resolve().parent
CACHE = HERE / "_cache"
OUT = HERE / "derived" / "pretrend_inputs.csv"

# Names aligned to derived/crosscountry.csv (PISA 2022 naming).
RENAME = {"Turkey": "Türkiye", "Czechia": "Czech Republic", "Russian Federation": "Russia",
          "Hong Kong-China": "Hong Kong (China)", "Macao-China": "Macao (China)"}
MISSING = {"m", "c", "w", "a", "x", ""}
SKIP_PREFIX = ("OECD", "Partners", "Note", "Notes", "*", "Information", "Values", "Source", "1.", "2.", "3.")


def clean_name(raw):
    if raw is None:
        return None
    name = str(raw).strip()
    if not name or name.startswith(SKIP_PREFIX) or len(name) > 60:
        return None
    name = re.sub(r"[\*\d,\s]+$", "", name).strip()  # footnote marks: "Cyprus1, 2", "Netherlands*"
    return RENAME.get(name, name)


def num(v):
    if v is None:
        return None
    if isinstance(v, (int, float)):
        return float(v)
    s = str(v).strip()
    if s in MISSING:
        return None
    try:
        return float(s)
    except ValueError:
        return None


def xlsx_rows(path, sheet):
    wb = openpyxl.load_workbook(path, read_only=True, data_only=True)
    rows = [list(r) for r in wb[sheet].iter_rows(values_only=True)]
    wb.close()
    return rows


def xls_rows(path, sheet):
    ws = xlrd.open_workbook(str(path)).sheet_by_name(sheet)
    return [ws.row_values(i) for i in range(ws.nrows)]


def country_rows(rows, start):
    """Yield (country, row) for data rows from `start`; stop at the first average row."""
    for r in rows[start:]:
        if not r:
            continue
        head = str(r[0]).strip() if r[0] is not None else ""
        if head.startswith("OECD average"):
            continue
        name = clean_name(r[0])
        if name is None:
            continue
        yield name, r


def cell(r, i):
    return num(r[i]) if i < len(r) else None


def fmt(x):
    return "" if x is None else f"{x:.4f}"


def main():
    out = {}

    # ---- 2006: PISA 2015 Vol I ----
    f15 = CACHE / "statlink_888933433226.xlsx"
    share06 = {}
    for name, r in country_rows(xlsx_rows(f15, "Table I.7.1"), 14):
        # cols: 1-8 = PISA 2015 (non-imm %, SE, imm %, SE, 2nd %, SE, 1st %, SE); 9-16 = PISA 2006 same order
        share06[name] = (cell(r, 11), cell(r, 12))
    for subj, sheet in (("science", "Table I.7.15a"), ("reading", "Table I.7.15b"), ("math", "Table I.7.15c")):
        for name, r in country_rows(xlsx_rows(f15, sheet), 14):
            # cols: 1-2 imm % 2015; 3-4 non-imm mean 2015; 5-6 imm mean 2015; 7-10 gaps 2015;
            # 11-12 non-imm mean 2006; 13-14 imm mean 2006
            m, se = cell(r, 11), cell(r, 12)
            if m is None:
                continue
            sh, shse = share06.get(name, (None, None))
            out[(name, 2006, subj)] = (m, se, sh, shse,
                                       f"PISA2015 VolI Tab {sheet[6:]} + I.7.1 (StatLink 888933433226)")

    # ---- 2009 reading: PISA 2018 Vol II (primary) ----
    f18 = CACHE / "statlink_888934038742.xlsx"
    share09 = {}
    for name, r in country_rows(xlsx_rows(f18, "Table II.B1.9.9"), 14):
        # cols: 1-3 non-imm %, SE, flag; 4-6 imm %, SE, flag (PISA 2009)
        share09[name] = (cell(r, 4), cell(r, 5))
    listed18 = set()
    for name, r in country_rows(xlsx_rows(f18, "Table II.B1.9.10"), 14):
        listed18.add(name)
        # cols: 1-3 all mean; 4-6 non-imm mean, SE, flag (PISA 2009)
        m, se = cell(r, 4), cell(r, 5)
        if m is None:
            continue
        sh, shse = share09.get(name, (None, None))
        out[(name, 2009, "reading")] = (m, se, sh, shse,
                                        "PISA2018 VolII Tab II.B1.9.10 + II.B1.9.9 (StatLink 888934038742)")

    # ---- 2009 reading: PISA 2009 Vol II (fallback for countries absent from the 2018 volume) ----
    f09 = CACHE / "statlink_888932381418.xls"
    for name, r in country_rows(xls_rows(f09, "T.II.4.1"), 12):
        # cols: 1-2 native %, SE; 3-4 native mean, SE; 13-14 imm %, SE; 15-16 imm mean, SE
        if name in listed18:
            continue  # the 2018 volume lists it (Austria is listed there as 'm' on purpose: not trend-comparable)
        m, se = cell(r, 3), cell(r, 4)
        if m is None:
            continue
        out[(name, 2009, "reading")] = (m, se, cell(r, 13), cell(r, 14),
                                        "PISA2009 VolII Tab II.4.1 (StatLink 888932381418; country absent from PISA2018 VolII)")

    # ---- 2012 math cross-check: PISA 2012 Vol II ----
    f12 = CACHE / "statlink_888932964927.xls"
    for name, r in country_rows(xls_rows(f12, "Table II.3.4a"), 14):
        # cols: 1-2 non-imm %, SE; 3-4 imm %, SE; 5-8 ESCS; 9-10 non-imm math mean, SE
        m, se = cell(r, 9), cell(r, 10)
        if m is None:
            continue
        out[(name, 2012, "math")] = (m, se, cell(r, 3), cell(r, 4),
                                     "PISA2012 VolII Tab II.3.4a (StatLink 888932964927)")

    rows = sorted(
        [country, str(cycle), subj, fmt(v[0]), fmt(v[1]), fmt(v[2]), fmt(v[3]), v[4]]
        for (country, cycle, subj), v in out.items()
    )
    OUT.parent.mkdir(exist_ok=True)
    with OUT.open("w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh, lineterminator="\n")
        w.writerow(["country", "cycle", "subject", "nat_mean", "nat_se", "imm_share", "imm_share_se", "source"])
        w.writerows(rows)

    # ---- cross-checks (stdout only) ----
    diffs = []
    for name, r in country_rows(xls_rows(f09, "T.II.4.1"), 12):
        k = (name, 2009, "reading")
        m09 = cell(r, 3)
        if k in out and m09 is not None and out[k][4].startswith("PISA2018"):
            diffs.append((abs(out[k][0] - m09), name, out[k][0], m09))
    diffs.sort(reverse=True)
    print(f"2009 reading non-imm mean, PISA2018 VolII vs PISA2009 VolII: n={len(diffs)}, "
          f"max |diff|={diffs[0][0]:.4f} ({diffs[0][1]})" if diffs else "no 2009 overlap")

    cc = {}
    with (HERE / "derived" / "crosscountry.csv").open(encoding="utf-8") as fh:
        for rec in csv.DictReader(fh):
            cc[clean_name(rec["country"])] = num(rec["nat_math_2012"])
    d12 = sorted(((abs(v[0] - cc[k[0]]), k[0], v[0], cc[k[0]]) for k, v in out.items()
                  if k[1] == 2012 and cc.get(k[0]) is not None), reverse=True)
    print(f"2012 math non-imm mean, PISA2012 VolII vs crosscountry.csv (PISA2022 VolI): n={len(d12)}")
    for d in d12[:8]:
        print(f"  {d[1]}: |diff|={d[0]:.2f}  vol2012={d[2]:.2f}  crosscountry={d[3]:.2f}")

    n = {}
    for (country, cycle, subj) in out:
        n[(cycle, subj)] = n.get((cycle, subj), 0) + 1
    for k in sorted(n):
        print("rows", k, n[k])


if __name__ == "__main__":
    main()
