"""Primary-source inputs for the 2026 Trustees payable paths (lane pension_tr2026_2026_10_06).

Every 2026 figure the lane uses is parsed here from a staged primary document's text layer (tables) or checked as a
verbatim quote in it (QUOTES). A missing document, a changed hash or a quote that is not in the text stops the run
with [BLOCKED].

Documents (staged under sources/immigration-fiscal/data/external/stage3/, each directory's ACQUIRED.md giving the URL,
date and sha256; the text layers are `pdftotext -layout` of each PDF, poppler 26.09.0, byte-identical to a fresh
conversion on 2026-10-07):
  tr2026   The 2026 Annual Report of the OASDI Trustees (Tables IV.B1, IV.B2, IV.B3, IV.B5, V.B2, V.C1; Highlights; II.D)
  mtr2026  The 2026 Annual Report of the HI and SMI Trustees (Tables III.B6, III.B7, V.D1; Section II.E)
  an2026_3 SSA Actuarial Note 2026.3, scaled factors under the 2026 Trustees Report (Table 7, the AWI path)
The 2025 reports' tables come through the pension lane's sources module (pension_accrual_2026_09_28/sources.py,
imported read-only), which checks their hashes: tr2025 (Tables IV.B1, IV.B2, IV.B4; V.C1 to check the copied parser) and
mtr2025 (III.B6, III.B7).
"""
from __future__ import annotations

import hashlib
import re
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.dont_write_bytecode = True   # read-only imports from other lanes: write nothing beside them

HERE = Path(__file__).resolve().parent
FISCAL = HERE.parent
ROOT = FISCAL.parents[1]
PENSION = FISCAL / "pension_accrual_2026_09_28"
STAGE = ROOT / "sources/immigration-fiscal/data/external/stage3"
sys.path.insert(0, str(PENSION))
import sources as S25  # noqa: E402  the pension lane's primary-source module (tr2025, mtr2025, Note 2025.7)

DOCS = {
    "tr2026": dict(pdf=STAGE / "ssa/trustees_2026/tr2026.pdf", txt=STAGE / "ssa/trustees_2026/tr2026.txt",
                   url="https://www.ssa.gov/OACT/TR/2026/tr2026.pdf",
                   title="The 2026 Annual Report of the Board of Trustees of the Federal OASI and DI Trust Funds"),
    "mtr2026": dict(pdf=STAGE / "cms/trustees_2026/mtr2026.pdf", txt=STAGE / "cms/trustees_2026/mtr2026.txt",
                    url="https://www.cms.gov/files/document/2026-medicare-trustees-report.pdf",
                    title="2026 Annual Report of the Boards of Trustees of the Federal HI and SMI Trust Funds"),
    "an2026_3": dict(pdf=STAGE / "ssa/trustees_2026/an2026-3.pdf", txt=STAGE / "ssa/trustees_2026/an2026-3.txt",
                     url="https://www.ssa.gov/OACT/NOTES/ran3/an2026-3.pdf",
                     title="SSA Actuarial Note 2026.3, Scaled factors for hypothetical earnings examples under the 2026 Trustees Report assumptions"),
}
# sha256 of each PDF as staged on 2026-10-06 (ACQUIRED.md) and of its text layer
SHA256 = {
    "tr2026": ("fb4e1556a00d925efa03e6355f64f911656a2626eaaceeb16062687008feb683",
               "789faa11edff9427e625c092516cadd94ab4f03553da803ae9bd39f0ef6bc7c1"),
    "mtr2026": ("ffa56b9137006872300b0346149eae1613d09a172b6ba118aad48e66dfc48fa8",
                "58ac07aa337c061f61f398669b3650debe00833b6e01d6eeab7114cc7eb05a81"),
    "an2026_3": ("25bf13bdd186a819a111c3f0b84766098d0cedc3c6f4477b74988c6707d44f01",
                 "2d04b489a7b25525730aaeeb828d37df4b2c7b0c2a8f4d8a7619b1d3b65cbfc7"),
}
# The published payable shares the paths must reproduce within the rounding of their inputs (sources.quotes()).
QUOTES = {
    "tr2026_oasdi_depletion": dict(doc="tr2026", value=2034, fragments=[
        "The combined OASDI fund is projected to become depleted in the third", "quarter of 2034, the same quarter as in last year's report."]),
    "tr2026_oasdi_payable": dict(doc="tr2026", value={"2034": 0.83, "2100": 0.65}, fragments=[
        "After reserves for the OASDI program are depleted, continuing income is",
        "sufficient to pay 83 percent of OASDI scheduled benefits for the rest of",
        "2034, declining to 65 percent for 2100."]),
    "tr2026_oasi_payable": dict(doc="tr2026", value={"2032": 0.78, "2100": 0.62}, fragments=[
        "depleted, projected OASI income is sufficient to pay 78 percent of scheduled",
        "OASI benefits for the rest of 2032, declining to 62 percent for 2100."]),
    "tr2026_transfer_assumption": dict(doc="tr2026", value="combined", fragments=[
        "Full payment of benefits until the combined reserves are depleted in 2034 implicitly assumes that the law will have been changed to permit the transfer of funds between OASI and DI as needed."]),
    "tr2026_di_reserves": dict(doc="tr2026", value="positive through 2100", fragments=[
        "The DI Trust Fund is projected to have sufficient",
        "reserves to pay full benefits throughout the 75-year projection period ending",
        "in 2100. Legislative action will be needed to prevent OASI reserve depletion."]),
    "tr2025_oasi_payable": dict(doc="tr2025", value={"2033": 0.77}, fragments=[
        "The OASI Trust Fund reserves are projected to become depleted in 2033, at",
        "which time OASI income would be sufficient to pay 77 percent of OASI"]),
    "tr2025_di_reserves": dict(doc="tr2025", value="positive through 2099", fragments=[
        "scheduled benefits. DI Trust Fund reserves are not projected to become",
        "depleted during the 75-year period ending in 2099."]),
    "tr2026_interest_ultimate": dict(doc="tr2026", value=0.023, fragments=[
        "reaching its ultimate level of 2.3 percent in 2043.", "The ultimate rates are unchanged from the 2025 report."]),
    "tr2026_mortality_decline": dict(doc="tr2026", value={"65plus": 0.0069, "total": 0.0073}, fragments=[
        "total age-sex-adjusted death rate is about 0.25 percent for alternative I,",
        "0.73 percent for alternative II, and 1.28 percent for alternative III.",
        "death rates for ages 65 and over decline between 2025 and 2100 at average",
        "annual rates of about 0.26 percent for alternative I, 0.69 percent for alterna-"]),
    "tr2026_real_earnings": dict(doc="tr2026", value={"2025_2035_growth": 0.0172, "tr2025_same_period": 0.0144}, fragments=[
        "growth in average real earnings from 2025 to 2035 averages 1.72 percent,",
        "significantly higher than the 1.44 percent annual rate projected in the 2025"]),
    "tr2026_actuarial_deficit": dict(doc="tr2026", value={"2026": 0.0442, "2025": 0.0382}, fragments=[
        "assumptions is 4.42 percent of taxable payroll for the 75-year period",
        "2026-2100, which is larger than the deficit of 3.82 percent for 2025-99 in last"]),
    "tr2026_fertility": dict(doc="tr2026", value={"2026": 1.75, "2025": 1.90}, fragments=[
        "Fertility: The ultimate total fertility rate is 1.75 children per woman for",
        "this report. This rate is lower than the rate of 1.90 children per woman"]),
    "mtr2026_hi_depletion": dict(doc="mtr2026", value="2033Q2", fragments=[
        "The HI trust fund is projected to become depleted in the second quarter",
        "of 2033, which is one quarter earlier than projected in last year's"]),
    "mtr2026_hi_payable": dict(doc="mtr2026", value={"2033": 0.89, "2050": 0.85, "2100": 0.93}, fragments=[
        "The percentage of expenditures covered by non-interest income is",
        "projected to be 89 percent in 2033 (year of depletion), 85 percent in",
        "2050 (25th projection year), and about 93 percent in 2100 (end of the"]),
    "mtr2026_hi_growth_ultimate": dict(doc="mtr2026", value=0.035, fragments=[
        "Medicare expenditures (excluding demographic", "HI (Part A) .................................................................. 3.5"]),
}


def blocked(msg: str):
    raise SystemExit(f"[BLOCKED] {msg}")


def _sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


_TEXT: dict = {}


def text(doc: str) -> list[str]:
    """A document's text layer as lines: the 2026 reports from the stage (PDF and text hashes checked), the 2025
    reports through the pension lane's sources.text (which checks the PDF hash)."""
    if doc in _TEXT:
        return _TEXT[doc]
    if doc not in DOCS:
        _TEXT[doc] = S25.text(doc)
        return _TEXT[doc]
    d = DOCS[doc]
    for k, f in (("pdf", d["pdf"]), ("txt", d["txt"])):
        if not f.exists():
            blocked(f"missing staged document {f}; fetch {d['url']} (see ACQUIRED.md)")
        if _sha(f) != SHA256[doc][0 if k == "pdf" else 1]:
            blocked(f"{f.name} is not the document this lane read (sha256 changed)")
    _TEXT[doc] = d["txt"].read_text().splitlines()
    return _TEXT[doc]


def _norm(s: str) -> str:
    s = s.replace("’", "'").replace("‘", "'").replace("−", "-").replace("–", "-").replace("—", "-")
    return re.sub(r"\s+", " ", s).strip()


def quotes() -> dict:
    """QUOTES, every fragment checked against its document's text layer."""
    cache = {}
    for key, item in QUOTES.items():
        doc = item["doc"]
        if doc not in cache:
            cache[doc] = _norm(" ".join(text(doc)))
        for frag in item["fragments"]:
            if _norm(frag) not in cache[doc]:
                blocked(f"QUOTES {key}: fragment not in {doc}: {frag!r}")
    return QUOTES


def provenance() -> dict:
    return {k: dict(title=d["title"], url=d["url"], file=str(d["pdf"].relative_to(ROOT)), sha256=SHA256[k][0],
                    text_sha256=SHA256[k][1]) for k, d in DOCS.items()}


# ------------------------------------------------------------------ OASDI Trustees Report tables
def _tok(t: str) -> float:
    """A table field: a footnote letter standing for a value under 0.005 in size reads as 0."""
    return 0.0 if t in ("c", "d") else float(t.replace(",", ""))


def intermediate_rows(doc: str, first_line: str, width: int) -> dict:
    """Rows of the intermediate block of a Trustees table whose first page starts with `first_line`: year -> the
    row's `width` numbers (the pension lane's sources._intermediate_rows, for any document)."""
    lines = text(doc)
    starts = [i for i, l in enumerate(lines) if first_line in l]
    if not starts:
        blocked(f"{doc}: no table {first_line!r}")
    row = re.compile(r"^\s*(\d{4})\s[ .]+\s(.*)$")
    out, on = {}, False
    for l in lines[starts[0]:starts[0] + 80]:
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
                blocked(f"{doc} {first_line}: row {m.group(1)} has {len(toks)} fields")
            out[int(m.group(1))] = [_tok(t) for t in toks]
    return out


TR_YEARS = {"tr2026": list(range(2026, 2036)) + list(range(2040, 2101, 5)),
            "tr2025": list(range(2025, 2036)) + list(range(2040, 2101, 5))}


def oasdi_rates(doc: str) -> pd.DataFrame:
    """Tables IV.B1 and IV.B2, intermediate, % of taxable payroll: cost, income, payroll-tax and taxation-of-benefits
    rates for OASI and for combined OASDI. Stops unless the two tables agree on each income rate (payroll + taxation
    of benefits + General Fund = total = Table IV.B1's income rate, to rounding)."""
    b1 = intermediate_rows(doc, "Table IV.B1.—Annual Income Rates, Cost Rates, and Balances,", 9)
    b2 = intermediate_rows(doc, "Table IV.B2.—Components of Annual Income Rates,", 12)
    years = TR_YEARS[doc]
    if sorted(b1) != years or sorted(b2) != years:
        blocked(f"{doc} Tables IV.B1/IV.B2: years {sorted(b1)} / {sorted(b2)}")
    rows = []
    for y in years:
        a, c = b1[y], b2[y]
        rows.append(dict(year=y, oasi_income=a[0], oasi_cost=a[1], oasdi_income=a[6], oasdi_cost=a[7],
                         oasi_payroll=c[0], oasi_tob=c[1], oasi_gf=c[2], oasi_total=c[3],
                         oasdi_payroll=c[8], oasdi_tob=c[9], oasdi_gf=c[10], oasdi_total=c[11]))
    t = pd.DataFrame(rows)
    for f in ("oasi", "oasdi"):
        if (t[f"{f}_income"] - t[f"{f}_total"]).abs().max() > 0.005 or \
                (t[f"{f}_payroll"] + t[f"{f}_tob"] + t[f"{f}_gf"] - t[f"{f}_total"]).abs().max() > 0.015:
            blocked(f"{doc} Tables IV.B1 and IV.B2 disagree on the {f} income rate")
    return t


def oasdi_gdp_rates(doc: str = "tr2026") -> pd.DataFrame:
    """Table IV.B3, intermediate, % of GDP: OASDI non-interest income and cost (no split of taxation of benefits)."""
    b3 = intermediate_rows(doc, "Table IV.B3.—Annual Income Rates, Cost Rates, and Balances,", 9)
    if sorted(b3) != TR_YEARS[doc]:
        blocked(f"{doc} Table IV.B3: years {sorted(b3)}")
    return pd.DataFrame([dict(year=y, oasdi_income_gdp=v[6], oasdi_cost_gdp=v[7]) for y, v in sorted(b3.items())])


def trust_fund_ratios(doc: str) -> pd.DataFrame:
    """The trust fund ratio table (TR 2026 Table IV.B5, TR 2025 Table IV.B4), intermediate: reserves at the start of
    each year as % of the year's cost, OASI, DI and OASDI; NaN where the reserves are depleted ("b")."""
    lines = text(doc)
    starts = [i for i, l in enumerate(lines) if re.search(r"Table IV\.B[45]\.—Trust Fund Ratios, Calendar Years", l)]
    if len(starts) != 1:
        blocked(f"{doc}: {len(starts)} trust fund ratio tables")
    row = re.compile(r"^(\d{4}) [ .]+\s(.*)$")
    out = {}
    for l in lines[starts[0]:starts[0] + 40]:
        m = row.match(l)
        if m:
            toks = m.group(2).split()
            if len(toks) != 9:
                blocked(f"{doc} trust fund ratios: row {m.group(1)} has {len(toks)} fields")
            out[int(m.group(1))] = [np.nan if t == "b" else float(t.replace(",", "")) for t in toks[:3]]
    years = TR_YEARS[doc]
    if sorted(out) != years:
        blocked(f"{doc} trust fund ratios: years {sorted(out)}")
    return pd.DataFrame([dict(year=y, oasi=v[0], di=v[1], oasdi=v[2]) for y, v in sorted(out.items())])


def new_issue_rates(doc: str = "tr2026") -> pd.Series:
    """Table V.B2: average annual nominal interest rate on newly issued trust fund securities by calendar year
    1961-2200 (the pension lane's sources.new_issue_rates_v_b2, for any report): historical 5-year periods
    ("1960 to 1965" covers 1961-65) and single years, the intermediate projection (annual, then every five years to
    2100, linear between); flat after 2100."""
    lines = text(doc)
    # six fields per row (unemployment, labor force, employment, real GDP, nominal rate, real rate); "h" marks a
    # value under 0.05 in size, and the nominal rate (the fifth) must be a number
    period = re.compile(r"^\s*(\d{4}) to (\d{4})[ .]+\s(.*)$")
    single = re.compile(r"^\s*(\d{4})[a-z]?\s[ .]+\s(.*)$")
    field = re.compile(r"-?\d*\.\d|h")

    def nominal(rest: str, y: str) -> float:
        toks = rest.split()
        if len(toks) != 6 or not all(field.fullmatch(t) for t in toks) or toks[4] == "h":
            blocked(f"{doc} Table V.B2: row {y} reads {toks}")
        return float(toks[4]) / 100

    starts = [i for i, l in enumerate(lines) if "Table V.B2.—Additional Economic Factors" in l]
    if len(starts) < 2:
        blocked(f"{doc} Table V.B2 not found")
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
                hist[y] = nominal(m.group(3), m.group(1))
        elif block in ("Single years", "Intermediate") and (m := single.match(l)):
            (hist if block == "Single years" else proj)[int(m.group(1))] = nominal(m.group(2), m.group(1))
    first = TR_YEARS[doc][0]
    if min(hist) != 1961 or max(hist) != first - 1 or sorted(proj)[:10] != list(range(first, first + 10)) or max(proj) != 2100:
        blocked(f"{doc} Table V.B2: history {min(hist)}-{max(hist)}, projection {sorted(proj)}")
    out = pd.Series({**hist, **proj}).sort_index().reindex(range(1961, 2201))
    return out.interpolate(limit_area="inside").ffill()


def program_parameters_v_c1(doc: str) -> pd.DataFrame:
    """Table V.C1: COLA (effective December), AWI and contribution base, historical and intermediate (tr2026 1975-2035,
    tr2025 1975-2034): the pension lane's sources.program_parameters_v_c1, for either report."""
    lines = text(doc)
    start = next((i for i, l in enumerate(lines) if "Table V.C1.—Cost-of-Living Benefit Increases" in l), None)
    if start is None:
        blocked(f"{doc}: no Table V.C1")
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
    last = {"tr2026": 2035, "tr2025": 2034}[doc]
    if t.year.tolist() != list(range(1975, last + 1)):
        blocked(f"{doc} Table V.C1: years {t.year.min()}-{t.year.max()} ({len(t)})")
    return t


def awi_path_2026() -> pd.Series:
    """AWI by calendar year, 1970-2061, from Note 2026.3 Table 7 (actual through 2024, 2026 Trustees intermediate
    after): the pension lane's sources.awi_path, on the 2026 note."""
    lines = text("an2026_3")
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
                            blocked(f"Note 2026.3 Table 7: AWI {y} read twice as {awi[y]} and {v}")
                        awi[y] = v
    years = sorted(awi)
    if years[0] != 1970 or years[-1] != 2061 or len(years) != 92:
        blocked(f"Note 2026.3 Table 7: AWI years {years[0]}-{years[-1]} ({len(years)})")
    return pd.Series(awi).sort_index()


# ------------------------------------------------------------------ Medicare Trustees Report tables
MTR_YEARS = {"mtr2026": list(range(2026, 2036)) + list(range(2040, 2101, 5)),
             "mtr2025": list(range(2025, 2036)) + list(range(2040, 2096, 5)) + [2099]}


def hi_rates(doc: str) -> pd.DataFrame:
    """Table III.B7, intermediate estimates: HI cost and income rates, % of taxable payroll. Stops unless every year
    is there once and the printed difference is income less cost, to rounding."""
    lines = text(doc)
    start = next((i for i, l in enumerate(lines) if "Table III.B7.—HI Cost and Income Rates" in l), None)
    if start is None:
        blocked(f"{doc}: no Table III.B7")
    row = re.compile(r"^\s*(\d{4})\s+(\d+\.\d\d)%?\s+(\d+\.\d\d)%?\s+([−–+-]?\d*\.\d\d)%?\s*$")
    out, on = {}, False
    for l in lines[start:start + 60]:
        if l.strip().startswith("Intermediate estimates:"):
            on = True
            continue
        m = row.match(l)
        if on and m:
            y = int(m.group(1))
            if y in out:
                blocked(f"{doc} Table III.B7: {y} twice")
            diff = float(m.group(4).replace("−", "-").replace("–", "-").replace("+", ""))
            out[y] = dict(year=y, cost=float(m.group(2)), income=float(m.group(3)), difference=diff)
        elif on and l.strip().startswith(("1", "Based on")) and out:
            break
    t = pd.DataFrame(sorted(out.values(), key=lambda r: r["year"]))
    if t.year.tolist() != MTR_YEARS[doc]:
        blocked(f"{doc} Table III.B7: years {t.year.tolist()}")
    if (t.income - t.cost - t.difference).abs().max() > 0.0151:
        blocked(f"{doc} Table III.B7: the difference is not income less cost")
    return t


def hi_asset_ratios(doc: str) -> pd.Series:
    """Table III.B6, intermediate estimates: HI assets at the start of the year as % of the year's expenditures;
    the first year shown as depleted ("—1", footnote 1) and later years are left out."""
    lines = text(doc)
    start = next((i for i, l in enumerate(lines) if "Table III.B6.—Ratio of Assets at the Beginning of the Year" in l), None)
    if start is None:
        blocked(f"{doc}: no Table III.B6")
    row = re.compile(r"^\s*(\d{4})\s+(—1|\d+)%?\s*$")
    out, on = {}, False
    for l in lines[start:start + 45]:
        if l.strip().startswith("Intermediate Estimates:"):
            on = True
            continue
        m = row.match(l)
        if on and m:
            if m.group(2) == "—1":
                break
            out[int(m.group(1))] = float(m.group(2))
    if not out or max(out) < 2032:
        blocked(f"{doc} Table III.B6: years {sorted(out)}")
    return pd.Series(out).sort_index()


def hi_per_beneficiary(doc: str = "mtr2026") -> pd.Series:
    """Table V.D1: HI average incurred cost per beneficiary by year (historical and intermediate)."""
    lines = text(doc)
    start = next(i for i, l in enumerate(lines) if "Table V.D1.—HI and SMI Average Incurred per Beneficiary Costs" in l)
    row = re.compile(r"^\s*(\d{4})\s+\$?([\d,]+)\s+\$?([\d,]+)\s+\$?([\d,]+)\s+\$?([\d,]+)\s")
    out = {}
    for line in lines[start:start + 45]:
        m = row.match(line)
        if m and int(m.group(1)) >= 2015:
            out[int(m.group(1))] = float(m.group(2).replace(",", ""))
    if sorted(out) != list(range(2015, 2036)):
        blocked(f"{doc} Table V.D1: years {sorted(out)}")
    return pd.Series(out).sort_index()
