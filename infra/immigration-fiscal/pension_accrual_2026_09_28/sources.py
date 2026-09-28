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
}
# The sha256 of each PDF as fetched on 2026-09-28 (Notes 2025.7 and 151: the 09-18 lane's copies).
PDF_SHA256 = {
    "an2025_7": "478d40a0829dc7cdb586fefa2ea3e6eaf75bc18b3bd42564ed4897477e18e207",
    "an2025_3": "814567fa33574e7f99f5cff8ec3cf75db745708481f99e886338058e453c9d76",
    "note151": "e303a40dc437b52e91c63bce484971c73e1e0b08d83ea900cf1e028c6a6f8458",
    "tr2025": "e6603329ce1b8aaa3d64c13bfc2db3b4ca40b5b94838c1afbd707d86960b97fb",
    "mtr2025": "1b3de7a4faeee5ad42059e10740603182b716a5fa7b53b30d360b45b9e474d95",
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


def provenance() -> dict:
    out = {}
    for k, d in DOCS.items():
        out[k] = dict(title=d["title"], url=d["url"], via=d.get("via"), file=str(d["pdf"].relative_to(FISCAL)),
                      sha256=_sha(d["pdf"]))
    return out
