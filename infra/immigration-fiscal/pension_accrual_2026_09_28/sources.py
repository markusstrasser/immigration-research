"""Primary-source inputs for the pension accrual lane.

Every Trustees, SSA actuarial and CMS figure the lane uses is either parsed here from the cached primary
document's text layer (tables) or read from reads/quotes.json (scalars), whose verbatim fragments must each
appear in that document's text. A missing document, a changed hash or a quote that is not in the text stops
the run with [BLOCKED].

Documents (PDFs in _cache/, ignored; the 09-18 timing lane's cached copies for Notes 2025.7 and 151):
  an2025_7  SSA Actuarial Note 2025.7, money's worth ratios (Tables 1 and 3, Table B interest rates)
  an2025_3  SSA Actuarial Note 2025.3, scaled factors (Table 6) and the AWI path (Table 7)
  note151   SSA Actuarial Note 151 (2013), unauthorized immigration and the trust funds
  tr2025    2025 OASDI Trustees Report (Table V.C7 benefit amounts; depletion, payable ratios, assumptions)
  mtr2025   2025 Medicare Trustees Report (Table II.B1 2024 operations, Table V.D1 HI cost per beneficiary)
The national check (national_check.py) also reads:
  ssa_afr2025  SSA FY 2025 Agency Financial Report, Financial Section (the OASDI Statement of Social Insurance)
  cms_fr2025   CMS Financial Report FY 2025 (the Medicare Statement of Social Insurance, HI rows)
  an2025_1     SSA Actuarial Note 2025.1, unfunded obligation and transition costs (definitions)
"""
from __future__ import annotations

import hashlib
import json
import re
import subprocess
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
FISCAL = HERE.parent
CACHE = HERE / "_cache"
TIMING = FISCAL / "lifetime_longevity_sstiming_2026_09_18"
QUOTES = HERE / "reads" / "quotes.json"

DOCS = {
    "an2025_7": dict(pdf=TIMING / "_cache/ssa_an2025-7.pdf", txt=TIMING / "_cache/ssa_an2025-7.txt",
                     url="https://www.ssa.gov/OACT/NOTES/ran7/an2025-7.pdf",
                     title="SSA Actuarial Note 2025.7, Money's worth ratios under the OASDI program for hypothetical workers (December 2025)"),
    "an2025_3": dict(pdf=CACHE / "an2025-3.pdf", txt=CACHE / "an2025-3.txt",
                     url="https://www.ssa.gov/OACT/NOTES/ran3/an2025-3.pdf",
                     via="https://web.archive.org/web/20260623234113id_/https://www.ssa.gov/oact/NOTES/ran3/an2025-3.pdf",
                     title="SSA Actuarial Note 2025.3, Scaled factors for hypothetical earnings examples under the 2025 Trustees Report assumptions"),
    "note151": dict(pdf=TIMING / "_cache/note151.pdf", txt=TIMING / "_cache/note151.txt",
                    url="https://www.ssa.gov/oact/NOTES/pdf_notes/note151.pdf",
                    title="SSA Actuarial Note 151, Effects of unauthorized immigration on the actuarial status of the Social Security Trust Funds (April 2013)"),
    "tr2025": dict(pdf=CACHE / "tr2025.pdf", txt=CACHE / "tr2025.txt",
                   url="https://www.ssa.gov/OACT/TR/2025/tr2025.pdf",
                   via="https://web.archive.org/web/20260919120748id_/https://www.ssa.gov/OACT/TR/2025/tr2025.pdf",
                   title="The 2025 Annual Report of the Board of Trustees of the Federal OASI and DI Trust Funds"),
    "mtr2025": dict(pdf=CACHE / "mtr2025.pdf", txt=CACHE / "mtr2025.txt",
                    url="https://www.cms.gov/files/document/2025-medicare-trustees-report.pdf",
                    title="2025 Annual Report of the Boards of Trustees of the Federal HI and SMI Trust Funds"),
    "ssa_afr2025": dict(pdf=CACHE / "ssa_afr2025_fin.pdf", txt=CACHE / "ssa_afr2025_fin.txt",
                        url="https://www.ssa.gov/finance/2025/Financial%20Section.pdf",
                        via="https://web.archive.org/web/20260316032752id_/https://www.ssa.gov/finance/2025/Financial%20Section.pdf",
                        title="SSA FY 2025 Agency Financial Report, Financial Section (Statements of Social Insurance, Note 17)"),
    "cms_fr2025": dict(pdf=CACHE / "cms_fr2025.pdf", txt=CACHE / "cms_fr2025.txt",
                       url="https://www.cms.gov/files/document/cms-financial-report-fiscal-year-2025.pdf",
                       title="CMS Financial Report, Fiscal Year 2025 (Statement of Social Insurance)"),
    "an2025_1": dict(pdf=CACHE / "an2025-1.pdf", txt=CACHE / "an2025-1.txt",
                     url="https://www.ssa.gov/OACT/NOTES/ran1/an2025-1.pdf",
                     via="https://web.archive.org/web/20250901133144id_/https://www.ssa.gov/OACT/NOTES/ran1/an2025-1.pdf",
                     title="SSA Actuarial Note 2025.1, Unfunded obligation and transition costs for the OASDI program (June 2025)"),
}
# The sha256 of each PDF as fetched on 2026-09-28 (Notes 2025.7 and 151: the 09-18 lane's copies).
PDF_SHA256 = {
    "an2025_7": "478d40a0829dc7cdb586fefa2ea3e6eaf75bc18b3bd42564ed4897477e18e207",
    "an2025_3": "814567fa33574e7f99f5cff8ec3cf75db745708481f99e886338058e453c9d76",
    "note151": "e303a40dc437b52e91c63bce484971c73e1e0b08d83ea900cf1e028c6a6f8458",
    "tr2025": "e6603329ce1b8aaa3d64c13bfc2db3b4ca40b5b94838c1afbd707d86960b97fb",
    "mtr2025": "1b3de7a4faeee5ad42059e10740603182b716a5fa7b53b30d360b45b9e474d95",
    "ssa_afr2025": "47bfd6c814cb4d0badd32f12c2557e1f09c1ba7239967af474f4af6fabeca34e",
    "cms_fr2025": "032fc57d08e15618cab4b30c81c9b03c8906f1ebf678fda9180ce77b1b50865d",
    "an2025_1": "56ba016b2786805ab26bc628f1d7b01e8ba29d8e969477e597c3038d721f72e6",
}
LEVELS = ["Very Low", "Low", "Medium", "High", "Maximum"]
FAMILIES = ["single_man", "single_woman", "one_earner_couple", "two_earner_couple"]


def _sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def text(doc: str) -> list[str]:
    d = DOCS[doc]
    if not d["pdf"].exists():
        raise SystemExit(f"[BLOCKED] missing primary document {d['pdf']}; fetch {d.get('via', d['url'])}")
    want = PDF_SHA256[doc]
    if want and _sha(d["pdf"]) != want:
        raise SystemExit(f"[BLOCKED] {d['pdf'].name} is not the document this lane read (sha256 changed)")
    if not d["txt"].exists():
        subprocess.run(["pdftotext", "-layout", str(d["pdf"]), str(d["txt"])], check=True)
    return d["txt"].read_text().splitlines()


def _norm(s: str) -> str:
    s = s.replace("’", "'").replace("‘", "'").replace("−", "-").replace("–", "-").replace("—", "-")
    return re.sub(r"\s+", " ", s).strip()


def quotes() -> dict:
    """reads/quotes.json, every fragment checked against its document's text layer."""
    q = json.loads(QUOTES.read_text())
    cache = {}
    for key, item in q.items():
        doc = item["doc"]
        if doc not in cache:
            cache[doc] = _norm(" ".join(text(doc)))
        for frag in item["fragments"]:
            if _norm(frag) not in cache[doc]:
                raise SystemExit(f"[BLOCKED] reads/quotes.json {key}: fragment not in {doc}: {frag!r}")
    return q


def value(key: str) -> float:
    return float(quotes()[key]["value"])


# ------------------------------------------------------------------ Note 2025.7
def mwr_table(number: int) -> pd.DataFrame:
    """Table `number` (1 scheduled, 3 payable) of Note 2025.7: 5 levels x 11 cohorts x 4 family types."""
    lines = text("an2025_7")
    start = next(i for i, l in enumerate(lines) if f"Table {number}. Money" in l)
    end = next(i for i, l in enumerate(lines[start:], start) if "Note: Based on the intermediate" in l)
    num = re.compile(r"^\s*(?:(Very Low|Low|Medium|High|Maximum)\s+)?(\d{4})\s+(\d{4})\s+"
                     r"([\d.]+)\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)\s*$")
    rows, labels = [], []
    for line in lines[start:end]:
        m = num.match(line)
        if m:
            labels.append(m.group(1))
            rows.append(dict(birth_year=int(m.group(2)), attains_65=int(m.group(3)),
                             **{f: float(m.group(4 + k)) for k, f in enumerate(FAMILIES)}))
    if len(rows) != 55:
        raise SystemExit(f"[BLOCKED] Note 2025.7 Table {number}: {len(rows)} rows, expected 55")
    # the level label is printed once per 11-cohort block, on any of its rows
    for i in range(0, 55, 11):
        block = sorted({l for l in labels[i:i + 11] if l})
        if len(block) != 1:
            raise SystemExit(f"[BLOCKED] Note 2025.7 Table {number}: block {i} labels {block}")
        for r in rows[i:i + 11]:
            r["earnings_level"] = block[0]
    t = pd.DataFrame(rows)
    if t.earnings_level.drop_duplicates().tolist() != LEVELS:
        raise SystemExit(f"[BLOCKED] Note 2025.7 Table {number}: level order")
    return t[["birth_year", "attains_65", *FAMILIES, "earnings_level"]]


def interest_rates() -> pd.DataFrame:
    """Table B of Note 2025.7: effective nominal and real rates earned by the combined trust funds, 1941-2049+."""
    lines = text("an2025_7")
    start = next(i for i, l in enumerate(lines) if "Table B. Effective Nominal and Real Interest Rates" in l)
    trip = re.compile(r"(\d{4})(?: and later)?\s+(-?\d+\.\d)\s+(-?\d+\.\d)")
    out = {}
    for line in lines[start:start + 50]:
        for m in trip.finditer(line):
            out[int(m.group(1))] = (float(m.group(2)) / 100, float(m.group(3)) / 100)
    years = sorted(out)
    if years[0] != 1941 or years[-1] != 2049 or len(years) != 109:
        raise SystemExit(f"[BLOCKED] Note 2025.7 Table B: years {years[0]}-{years[-1]} ({len(years)})")
    return pd.DataFrame([dict(year=y, nominal=out[y][0], real=out[y][1]) for y in years])


# ------------------------------------------------------------------ Note 2025.3
def scaled_factors() -> pd.DataFrame:
    """Table 6: preliminary adjusted scaled factors and the four final sets, ages 21-64."""
    lines = text("an2025_3")
    row = re.compile(r"^\s*(\d{2})\s+(\d\.\d{3})\s+(\d\.\d{3})\s+(\d\.\d{3})\s+(\d\.\d{3})\s+(\d\.\d{3})\s*$")
    rows = {}
    for i, l in enumerate(lines):
        if "Table 6.—Calculation of Final Scaled Factors" in l:
            for line in lines[i:i + 40]:
                m = row.match(line)
                if m:
                    rows[int(m.group(1))] = [float(m.group(k)) for k in range(2, 7)]
    if sorted(rows) != list(range(21, 65)):
        raise SystemExit(f"[BLOCKED] Note 2025.3 Table 6: ages {sorted(rows)[:3]}...")
    t = pd.DataFrame([dict(age=a, preliminary=v[0], very_low=v[1], low=v[2], medium=v[3], high=v[4])
                      for a, v in sorted(rows.items())])
    # The final sets are the preliminary factors times one adjustment each (Table 6 header).
    for col, adj in (("very_low", 0.305), ("low", 0.549), ("medium", 1.221), ("high", 1.953)):
        if (t[col] - (t.preliminary * adj).round(3)).abs().max() > 0.0015:
            raise SystemExit(f"[BLOCKED] Note 2025.3 Table 6: {col} is not the preliminary factors x {adj}")
    return t


def aime_distribution() -> pd.DataFrame:
    """Table 1: the distribution of AIMEs of actual workers retiring in 2019-2024 relative to the hypothetical
    scaled workers' AIMEs (career-average earnings): % below each level and % closest to it, men, women, all."""
    lines = text("an2025_3")
    start = next(i for i, l in enumerate(lines) if "Table 1.—Distribution of AIMEs of Actual Workers Retiring" in l)
    row = re.compile(r"^\s*(Very Low|Low|Medium|High|Maximum)\s+\(\$([\d,]+)\)\s*\.+\s+" + r"\s+".join([r"([\d.]+)"] * 6)
                     + r"\s*$")
    out = []
    for l in lines[start:start + 15]:
        m = row.match(l)
        if m:
            v = [float(m.group(k)) for k in range(3, 9)]
            out.append(dict(level=m.group(1), career_average=float(m.group(2).replace(",", "")),
                            below_men=v[0], below_women=v[1], below_all=v[2],
                            closest_men=v[3], closest_women=v[4], closest_all=v[5]))
    t = pd.DataFrame(out)
    if t.level.tolist() != LEVELS or (t[["closest_men", "closest_women", "closest_all"]].sum() - 100).abs().max() > 0.3 \
            or (t[["below_men", "below_women", "below_all"]].diff().dropna() <= 0).any().any():
        raise SystemExit("[BLOCKED] Note 2025.3 Table 1: rows, shares or order")
    return t


def awi_path() -> pd.Series:
    """AWI by calendar year, 1970-2061, from Table 7 (actual through 2023, 2025 Trustees intermediate after)."""
    lines = text("an2025_3")
    row = re.compile(r"^\s*(\d{2})\s+\d\.\d{3}\s+\$?([\d,]+\.\d\d)\s+\$?[\d,]+\.\d\d\s+\$?([\d,]+\.\d\d)\s+"
                     r"\$?[\d,]+\.\d\d\s+\$?([\d,]+\.\d\d)\s+\$?[\d,]+\.\d\d\s*$")
    awi = {}
    for i, l in enumerate(lines):
        if "Table 7.—Example: Developing Earnings" in l:
            for line in lines[i:i + 60]:
                m = row.match(line)
                if m:
                    age = int(m.group(1))
                    for birth, g in ((1949, 2), (1973, 3), (1997, 4)):
                        y, v = birth + age, float(m.group(g).replace(",", ""))
                        if y in awi and abs(awi[y] - v) > 0.005:
                            raise SystemExit(f"[BLOCKED] Note 2025.3 Table 7: AWI {y} read twice as {awi[y]} and {v}")
                        awi[y] = v
    years = sorted(awi)
    if years[0] != 1970 or years[-1] != 2061 or len(years) != 92:
        raise SystemExit(f"[BLOCKED] Note 2025.3 Table 7: AWI years {years[0]}-{years[-1]} ({len(years)})")
    return pd.Series(awi).sort_index()


# ------------------------------------------------------------------ 2025 OASDI Trustees Report
def benefit_amounts_v_c7() -> pd.DataFrame:
    """Table V.C7: scheduled annual benefit at 65 (CPI-indexed 2025 dollars) and its replacement rate."""
    lines = text("tr2025")
    start = next(i for i, l in enumerate(lines) if "Table V.C7.—Annual Scheduled Benefit Amounts" in l)
    head = re.compile(r"Scaled (very low|low|medium|high) earnings")
    row = re.compile(r"^\s*(\d{4})\s[ .]+\s+67:0\s+\$?([\d,]+)\s+([\d.]+)\s+65:0\s+\$?([\d,]+)\s+([\d.]+)\s*$")
    out, level = [], None
    for l in lines[start:start + 160]:
        if "Steady maximum" in l:
            break
        h = head.search(l)
        if h:
            level = h.group(1).replace(" ", "_")
            continue
        m = row.match(l)
        if m and level:
            out.append(dict(level=level, year_65=int(m.group(1)), nra_benefit=float(m.group(2).replace(",", "")),
                            nra_pct=float(m.group(3)), at65_benefit=float(m.group(4).replace(",", "")),
                            at65_pct=float(m.group(5))))
    t = pd.DataFrame(out)
    if set(t.level) != {"very_low", "low", "medium", "high"} or len(t) != 64:
        raise SystemExit(f"[BLOCKED] TR 2025 Table V.C7: {len(t)} rows, levels {sorted(set(t.level))}")
    return t


def program_parameters_v_c1() -> pd.DataFrame:
    """Table V.C1: COLA (effective December), AWI and contribution base, 1975-2023 actual and 2024-2034
    intermediate."""
    lines = text("tr2025")
    start = next(i for i, l in enumerate(lines) if "Table V.C1.—Cost-of-Living Benefit Increases" in l)
    row = re.compile(r"^\s*(\d{4})\s[ .]+\s+[a-z]?\s?(-?\d*\.\d)\s+\$?([\d,]+\.\d\d)\s+(-?\d*\.\d)\s+[a-z]?\$?([\d,]+)\s")
    out, block = {}, "historical"
    for l in lines[start:start + 140]:
        if l.strip().startswith("Intermediate:"):
            block = "intermediate"
        elif l.strip().startswith(("Low-cost:", "High-cost:")):
            block = "other"
        m = row.match(l)
        if m and block in ("historical", "intermediate"):
            y = int(m.group(1))
            out[y] = dict(year=y, cola=float(m.group(2)) / 100, awi=float(m.group(3).replace(",", "")),
                          base=float(m.group(5).replace(",", "")))
    t = pd.DataFrame(sorted(out.values(), key=lambda r: r["year"]))
    if t.year.tolist() != list(range(1975, 2035)):
        raise SystemExit(f"[BLOCKED] TR 2025 Table V.C1: years {t.year.min()}-{t.year.max()} ({len(t)})")
    return t


def new_issue_rates_v_b2() -> pd.Series:
    """Table V.B2: average annual nominal interest rate on newly issued trust fund securities, by calendar year
    1961-2200. Historical 5-year periods ("1960 to 1965" covers 1961-65), historical single years 2014-2024, the
    intermediate projection (annual 2025-2035, then every five years to 2100, linear between); flat after 2100."""
    lines = text("tr2025")
    num = r"(-?\d*\.\d)"
    period = re.compile(rf"^\s*(\d{{4}}) to (\d{{4}})[ .]+\s+{num}\s+{num}\s+{num}\s+{num}\s+{num}\s+(?:{num}|h)\s*$")
    single = re.compile(rf"^\s*(\d{{4}})[a-z]?\s[ .]+\s+{num}\s+{num}\s+{num}\s+{num}\s+{num}\s+{num}\s*$")
    starts = [i for i, l in enumerate(lines) if "Table V.B2.—Additional Economic Factors" in l]
    if len(starts) < 2:
        raise SystemExit("[BLOCKED] TR 2025 Table V.B2 not found")
    hist, proj, block = {}, {}, None
    for l in lines[starts[0]:starts[0] + 60] + lines[starts[1]:starts[1] + 40]:
        s = l.strip()
        if s.startswith(("5-year periods:", "Single years:", "Intermediate:")):
            block = s.rstrip(":")
            continue
        if s.startswith(("Economic cycles:", "Low-cost:", "High-cost:")):
            block = None
            continue
        if block == "5-year periods" and (m := period.match(l)):
            for y in range(int(m.group(1)) + 1, int(m.group(2)) + 1):
                hist[y] = float(m.group(7)) / 100
        elif block in ("Single years", "Intermediate") and (m := single.match(l)):
            (hist if block == "Single years" else proj)[int(m.group(1))] = float(m.group(6)) / 100
    if min(hist) != 1961 or max(hist) != 2024 or sorted(proj)[:11] != list(range(2025, 2036)) or max(proj) != 2100:
        raise SystemExit(f"[BLOCKED] TR 2025 Table V.B2: history {min(hist)}-{max(hist)}, projection {sorted(proj)}")
    out = pd.Series({**hist, **proj}).sort_index().reindex(range(1961, 2201))
    return out.interpolate(limit_area="inside").ffill()


def combined_operations_vi_a3() -> pd.DataFrame:
    """Table VI.A3 (cont.): combined OASI and DI operations, calendar years 2010-2024, $bn: net payroll tax
    contributions, taxation of benefits, cost, benefit payments and reserves at the end of the year."""
    lines = text("tr2025")
    start = next(i for i, l in enumerate(lines) if "Table VI.A3.— Operations of the Combined OASI and DI Trust Funds," in l
                 and "Calendar Years 1957-2024 (Cont.)" in lines[i + 1])
    num = r"\$?([\d,]+\.\d|g|\.\d)"
    row = re.compile(rf"^\s*(\d{{4}}) \. \.\s+{num}\s+{num}\s+{num}\s+{num}\s+{num}\s+{num}\s+{num}\s+{num}\s+{num}"
                     rf"\s+\$?(-?[\d,]*\.\d)\s+{num}\s+\d+\s*$")
    val = lambda s: 0.0 if s == "g" else float(s.replace(",", ""))
    out = []
    for l in lines[start:start + 25]:
        m = row.match(l)
        if m:
            g = [m.group(k) for k in range(1, 13)]
            out.append(dict(year=int(g[0]), income=val(g[1]), payroll_tax=val(g[2]), gf_reimbursements=val(g[3]),
                            taxation_of_benefits=val(g[4]), net_interest=val(g[5]), cost=val(g[6]),
                            benefits=val(g[7]), reserves_end=val(g[11])))
    t = pd.DataFrame(out)
    if t.year.tolist() != list(range(2010, 2025)):
        raise SystemExit(f"[BLOCKED] TR 2025 Table VI.A3: years {t.year.tolist()}")
    if abs(t.set_index("year").payroll_tax[2024] - value("tr_oasdi_payroll_tax_2024_bn")) > 1e-9:
        raise SystemExit("[BLOCKED] TR 2025 Table VI.A3 disagrees with Table II.B1 on 2024 payroll taxes")
    return t


def _intermediate_rows(first_line: str, width: int) -> dict:
    """Rows of the intermediate block of a TR table whose first page starts with `first_line`: year -> the row's
    `width` numbers (a footnote letter standing for a value under 0.005 in size reads as 0)."""
    lines = text("tr2025")
    start = next(i for i, l in enumerate(lines) if first_line in l)
    row = re.compile(r"^\s*(\d{4})\s[ .]+\s(.*)$")
    out, on = {}, False
    for l in lines[start:start + 80]:
        s = l.strip()
        if s.startswith("Intermediate:"):
            on = True
            continue
        if s.startswith("Low-cost:"):
            break
        m = row.match(l)
        if on and m:
            toks = m.group(2).split()
            if len(toks) != width:
                raise SystemExit(f"[BLOCKED] {first_line}: row {m.group(1)} has {len(toks)} fields")
            out[int(m.group(1))] = [0.0 if t in ("c", "d") else float(t) for t in toks]
    return out


def oasdi_rates_iv_b() -> pd.DataFrame:
    """Tables IV.B1 and IV.B2, intermediate: the OASDI cost rate and the rate of income from taxation of scheduled
    benefits, % of taxable payroll, 2025-2035 and every fifth year to 2100."""
    b1 = _intermediate_rows("Table IV.B1.—Annual Income Rates, Cost Rates, and Balances,", 9)
    b2 = _intermediate_rows("Table IV.B2.—Components of Annual Income Rates, Calendar Years 1990-2100", 12)
    years = list(range(2025, 2036)) + list(range(2040, 2101, 5))
    if sorted(b1) != years or sorted(b2) != years:
        raise SystemExit(f"[BLOCKED] TR 2025 Tables IV.B1/IV.B2: years {sorted(b1)} / {sorted(b2)}")
    t = pd.DataFrame([dict(year=y, cost_rate=b1[y][7], income_rate=b1[y][6], payroll_rate=b2[y][8],
                           tob_rate=b2[y][9], income_total=b2[y][11]) for y in years])
    if (t.income_rate - t.income_total).abs().max() > 0.005 or \
            (t.payroll_rate + t.tob_rate - t.income_total).abs().max() > 0.015:
        raise SystemExit("[BLOCKED] TR 2025 Tables IV.B1 and IV.B2 disagree on the OASDI income rate")
    return t


def oasdi_tax_rates_v_c6() -> pd.Series:
    """Table V.C6: combined employee-employer OASDI contribution rate by calendar year, 1937-2025."""
    lines = text("tr2025")
    starts = [i for i, l in enumerate(lines) if "Table V.C6.—Contribution and Benefit Base and Payroll Tax" in l]
    row = re.compile(r"^\s*(\d{4})(?:-(\d{2}))?\s*[a-z]?\s*[ .]+\s+\$?[\d,]+\s+(\d+\.\d\d)\s+\d+\.\d\d\s+[\d.—]+\s")
    out = {}
    for s in starts:
        for l in lines[s:s + 75]:
            m = row.match(l)
            if m:
                y0 = int(m.group(1))
                y1 = int(m.group(1)[:2] + m.group(2)) if m.group(2) else y0
                for y in range(y0, y1 + 1):
                    out[y] = float(m.group(3)) / 100
    years = sorted(out)
    if years[0] != 1937 or years[-1] != 2025 or len(years) != 89:
        raise SystemExit(f"[BLOCKED] TR 2025 Table V.C6: years {years[0]}-{years[-1]} ({len(years)})")
    return pd.Series(out).sort_index()


# ------------------------------------------------------------------ 2025 Medicare Trustees Report
def hi_per_beneficiary() -> pd.Series:
    """Table V.D1: HI average incurred cost per beneficiary, 2015-2034 (historical through 2024)."""
    lines = text("mtr2025")
    start = next(i for i, l in enumerate(lines) if "Table V.D1.—HI and SMI Average Incurred per Beneficiary Costs" in l)
    row = re.compile(r"^\s*(\d{4})\s+\$?([\d,]+)\s+\$?([\d,]+)\s+\$?([\d,]+)\s+\$?([\d,]+)\s")
    out = {}
    for line in lines[start:start + 45]:
        m = row.match(line)
        if m and int(m.group(1)) >= 2015:
            out[int(m.group(1))] = float(m.group(2).replace(",", ""))
    if sorted(out) != list(range(2015, 2035)):
        raise SystemExit(f"[BLOCKED] Medicare TR Table V.D1: years {sorted(out)}")
    return pd.Series(out).sort_index()


# ------------------------------------------------------------------ Statements of Social Insurance, 1 January 2025
def _first_amount(line: str, label: str) -> float:
    """The first amount after `label` on a statement line ($bn; parentheses are negative): the 2025 column."""
    toks = [t for t in line.split(label, 1)[1].replace("$", " ").split() if re.fullmatch(r"\(?[\d,]+\)?", t)]
    if not toks:
        raise SystemExit(f"[BLOCKED] no amount after {label!r}: {line.strip()!r}")
    v = float(toks[0].strip("()").replace(",", ""))
    return -v if toks[0].startswith("(") else v


def sosi_oasdi() -> dict:
    """SSA's Statement of Social Insurance for OASDI as of 1 January 2025 (FY 2025 AFR), 2025 column, $bn:
    non-interest income, cost and net for current participants 62 and over and 15-61, the closed-group net and the
    reserves; each net equals income less cost and the closed group the sum of the two rows."""
    lines = text("ssa_afr2025")
    start = next(i for i, l in enumerate(lines) if l.strip() == "Statements of Social Insurance"
                 and "Old-Age, Survivors, and Disability Insurance" in lines[i + 1] and "as of January 1, 2025" in lines[i + 2])
    if not re.match(r"^\s*2025\s+2024\s+2023\s+2022\s+2021\s*$", lines[start + 5]):
        raise SystemExit("[BLOCKED] SSA AFR 2025 SOSI: the first column is not 2025")
    rows, group, out = {}, None, {}
    for l in lines[start:start + 40]:
        if "(age 62 and over)" in l:
            group = "62_plus"
        elif "(ages 15" in l:
            group = "15_61"
        elif "Future participants" in l:
            break
        for label, key in (("Noninterest income", "income"), ("Cost for scheduled future benefits", "cost"),
                           ("Future noninterest income less future cost", "net")):
            if group and l.strip().startswith(label):
                rows.setdefault(group, {})[key] = _first_amount(l, label)
        if "current participants (closed group measure)" in l:
            out["closed_group_net"] = _first_amount(l, "(closed group measure)")
        if l.strip().startswith("Combined OASI and DI Trust Fund reserves at start of period"):
            out["reserves"] = _first_amount(l, "start of period")
    if sorted(rows) != ["15_61", "62_plus"] or any(sorted(r) != ["cost", "income", "net"] for r in rows.values()) \
            or sorted(out) != ["closed_group_net", "reserves"]:
        raise SystemExit(f"[BLOCKED] SSA AFR 2025 SOSI: read {rows} {out}")
    if any(abs(r["income"] - r["cost"] - r["net"]) > 1.5 for r in rows.values()) or \
            abs(sum(r["net"] for r in rows.values()) - out["closed_group_net"]) > 1.5:
        raise SystemExit("[BLOCKED] SSA AFR 2025 SOSI: rows do not add up")
    return dict(rows=rows, **out)


def sosi_hi() -> dict:
    """CMS's Statement of Social Insurance as of 1 January 2025 (FY 2025 Financial Report), HI, 2025 column, $bn:
    income (excluding interest) and expenditures for current participants who have not attained eligibility age
    (15-64), those 65 and over, future participants and all; the parts add to the totals and the totals' difference
    to the published excess."""
    lines = text("cms_fr2025")
    start = next(i for i, l in enumerate(lines) if l.strip() == "Statement of Social Insurance"
                 and "75-Year Projection as of January 1, 2025" in lines[i + 1])
    groups = {"Have not yet attained eligibility age": "15_64", "Have attained eligibility age": "65_plus",
              "Those expected to become participants": "future", "All current and future participants": "all"}
    rows, section, group, excess = {}, None, None, None
    for l in lines[start:start + 70]:
        s = l.strip()
        if "income (excluding interest) received from" in s:
            section = "income"
        elif "expenditures for or on behalf of" in s:
            section = "expenditures"
        elif "estimated future excess" in s:
            section = "excess"
        for head, key in groups.items():
            if s.startswith(head):
                group = key
        if s.startswith("HI ") or s == "HI":
            if section in ("income", "expenditures"):
                rows.setdefault(group, {})[section] = _first_amount(l, "HI")
            elif section == "excess" and excess is None:
                excess = _first_amount(l, "HI")
                break
    if sorted(rows) != ["15_64", "65_plus", "all", "future"] or \
            any(sorted(r) != ["expenditures", "income"] for r in rows.values()) or excess is None:
        raise SystemExit(f"[BLOCKED] CMS FY 2025 SOSI: read {rows} {excess}")
    for k in ("income", "expenditures"):
        if abs(sum(rows[g][k] for g in ("15_64", "65_plus", "future")) - rows["all"][k]) > 2:
            raise SystemExit(f"[BLOCKED] CMS FY 2025 SOSI: HI {k} parts do not add to the total")
    if abs(rows["all"]["income"] - rows["all"]["expenditures"] - excess) > 2:
        raise SystemExit("[BLOCKED] CMS FY 2025 SOSI: HI income less expenditures is not the published excess")
    return dict(rows=rows, excess=excess)


def provenance() -> dict:
    out = {}
    for k, d in DOCS.items():
        out[k] = dict(title=d["title"], url=d["url"], via=d.get("via"), file=str(d["pdf"].relative_to(FISCAL)),
                      sha256=_sha(d["pdf"]))
    return out
