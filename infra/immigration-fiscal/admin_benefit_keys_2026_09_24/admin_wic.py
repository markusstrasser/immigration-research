#!/usr/bin/env python3
"""WIC participants by Hispanic ethnicity, nation (by participant category) and state agency.

Source: USDA FNS (now Food and Nutrition Administration), "WIC Participant and Program
Characteristics" (WIC PC), a biennial census of participants with active certifications in April.
PC2022 is the latest release (PC2024 is not published as of 2026-09-24); PC2020 is parsed as a check.
  - Report Table 3.6: national counts by ethnicity x participant category.
  - Appendix Table A.9: national ethnicity series (cross-year and cross-document check).
  - Appendix Table B.8: percent by ethnicity and total participants for every state agency.
Writes derived/admin_wic_pc.csv. Every number is parsed from the PDFs (pdftotext -layout);
the gates below stop the script on any inconsistency.

Run from the repository root:
  OPENBLAS_NUM_THREADS=1 uv run --no-project --with pandas --with numpy --with openpyxl \
      python3 infra/immigration-fiscal/admin_benefit_keys_2026_09_24/admin_wic.py [--refetch]
"""
from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
from admin_tanf import CACHE, GATE_LOG, POSTAL, fetch, gate, is_pdf  # noqa: E402  shared fetch/pin/gate

LANE = Path(__file__).resolve().parent
OUT = LANE / "derived" / "admin_wic_pc.csv"
BASE = "https://www.fna.usda.gov/sites/default/files/resource-files/"
PAGES = {  # landing pages: evidence of the release set (PC2024 absent) and reference period
    "wic/fna_wic_pc_dataviz_page.html":
        "https://www.fna.usda.gov/data-research/data-visualization/wic-participant-program-characteristics",
    "wic/fna_wic_pc2022_page.html":
        "https://www.fna.usda.gov/research/wic/participant-program-characteristics-2022",
}
YEARS = {
    2022: {"report": "wic-ppc-2022-report.pdf", "appendix": "wic-ppc-2022-appendices.pdf", "agencies": 89,
           "count_tol": 0},
    # PC2020 weighted the Colorado, Iowa and Montana files (duplicate identifiers; report ch. 2), so its
    # published counts are rounded weighted values: components can miss their totals by a unit or two.
    2020: {"report": "WICPC2020-1.pdf", "appendix": "WICPC2020-Appendix.pdf", "agencies": None,
           "count_tol": 2},
}
CATS = ["pregnant_women", "breastfeeding_women", "postpartum_women", "women_total",
        "infants", "children", "all"]
TERR = {"American Samoa": "AS", "Guam": "GU", "Puerto Rico": "PR",
        "Commonwealth of the Northern Mariana Islands": "MP", "Northern Mariana Islands": "MP",
        "U.S. Virgin Islands": "VI", "Virgin Islands": "VI"}
STATES = {k: v for k, v in POSTAL.items() if v not in ("GU", "PR", "VI")}
NUM = r"(?:<\s?0\.1|\d{1,3}(?:,\d{3})+|\d+\.\d+|\d+|\*)"


def pdf_pages(pdf: Path) -> list[str]:
    txt = subprocess.run(["pdftotext", "-layout", str(pdf), "-"], capture_output=True,
                         text=True, check=True).stdout
    return txt.split("\f")


def label(page: str) -> str:
    foot = [ln for ln in page.splitlines() if "Westat" in ln or "Insight" in ln]
    m = re.search(r"([A-C]?-?\d+)\s*$", foot[0]) if foot else None
    return m.group(1) if m else "?"


def find_page(pages, title_re) -> int:
    hits = [i for i, p in enumerate(pages)
            if sum("....." in ln for ln in p.splitlines()) < 5  # skip table-of-contents pages
            and any(re.match(r"\s*" + title_re, ln) for ln in p.splitlines())]
    if len(hits) != 1:
        sys.exit(f"[GATE] expected one page with {title_re!r}, found {hits}")
    return hits[0]


def to_f(tok: str):
    """Published token -> float; '*' -> None; '<0.1' -> 0.05 (flagged by the caller)."""
    tok = tok.replace(" ", "")
    if tok == "*":
        return None
    if tok.startswith("<"):
        return 0.05
    return float(tok.replace(",", ""))


def is_pct_line(toks) -> bool:
    return any("." in t or "<" in t for t in toks)


def rhu(x: float) -> float:
    """Round half up to one decimal, as published tables round."""
    return float(int(x * 10 + 0.5 + 1e-9)) / 10


# ---------------------------------------------------------------- tables
def table_36(pages, year):
    i = find_page(pages, r"Table 3\.6\. Distribution of (WIC )?Participants by Race and Ethnicity")
    page = pages[i]
    hdr = " ".join(page.splitlines()[:12])
    order = [hdr.find(w) for w in ("Pregnant", "Breastfeeding", "Postpartum", "Infants", "Children")]
    gate(all(o >= 0 for o in order) and order == sorted(order),
         f"PC{year} T3.6 header lists the categories in the expected order")
    out = {}
    for key, pat in (("total", r"Total Participants"), ("hisp", r"(?<!Non-)Hispanic/Latino"),
                     ("nonhisp", r"Non-Hispanic/Latino"), ("unk", r"Ethnicity not reported")):
        for ln in page.splitlines():
            m = re.search(pat, ln)
            if not m:
                continue
            toks = re.findall(NUM, ln[m.end():])
            if len(toks) != 7:
                continue
            kind = "pct" if is_pct_line(toks) else "n"
            gate((key, kind) not in out, f"PC{year} T3.6 single {key}/{kind} row")
            out[(key, kind)] = toks
    gate(len(out) == 8, f"PC{year} T3.6 parsed count and percent rows for 4 labels ({len(out)})")
    n = {k: [int(t.replace(",", "")) for t in out[(k, "n")]] for k in ("total", "hisp", "nonhisp", "unk")}
    for j, c in enumerate(CATS):
        tol = YEARS[year]["count_tol"]
        gate(abs(n["hisp"][j] + n["nonhisp"][j] + n["unk"][j] - n["total"][j]) <= tol,
             f"PC{year} T3.6 {c}: Hispanic + non-Hispanic + not reported = total {n['total'][j]:,}")
        for k in ("total", "hisp", "nonhisp", "unk"):
            pub = out[(k, "pct")][j].replace(" ", "")
            calc = 100 * n[k][j] / n["total"][j]
            ok = (calc < 0.1) if pub.startswith("<") else abs(rhu(calc) - float(pub)) < 0.051
            gate(ok, f"PC{year} T3.6 {c} {k}: computed {calc:.3f}% vs published {pub}")
    for k in ("total", "hisp", "nonhisp", "unk"):
        v = n[k]
        tol = YEARS[year]["count_tol"]
        gate(abs(v[3] - v[0] - v[1] - v[2]) <= tol and abs(v[6] - v[3] - v[4] - v[5]) <= tol,
             f"PC{year} T3.6 {k}: women subtotal and grand total add up")
    return n, out, i


def table_a9(pages, year):
    i = find_page(pages, r"Table A\.9\. Distribution of (WIC )?Participants by Ethnicity")
    rows = {}
    for ln in pages[i].splitlines():
        m = re.match(r"^\s*(?:Number of|Participants|Percent of)?\s*((?:19|20)\d\d)\s+(.*)$", ln)
        if not m:
            continue
        toks = re.findall(NUM, m.group(2))
        if len(toks) != 4:
            continue
        rows[(int(m.group(1)), "pct" if is_pct_line(toks) else "n")] = toks
    gate((year, "n") in rows and (year, "pct") in rows, f"PC{year} Table A.9 has the {year} rows")
    return rows, i


def table_b8(pages, year):
    i = find_page(pages, r"Table B\.8\. Percentage of (WIC )?Participants,? by Ethnicity")
    lines, done = [], False  # (page index, line) from the title page to the next table's title
    for k in range(i, min(i + 4, len(pages))):
        for ln in pages[k].splitlines():
            if re.match(r"\s*Table B\.9", ln):
                done = True
                break
            lines.append((k, ln))
        if done:
            break
    gate(done, f"PC{year} B.8 ends before Table B.9 within 4 pages")
    row_re = re.compile(rf"^(?P<name>.*?\S)\s{{2,}}(?P<h>{NUM})\s+(?P<n>{NUM})\s+(?P<u>{NUM})\s+"
                        r"(?P<t>\d{1,3}(?:,\d{3})*)\s*$")
    noise = re.compile(r"^(States|and DC|U\.S\.|Territories|Indian Tribal|Organizations|\(continued\)|"
                       r"Hispanic/|Non-|Latino|State Agency|Participants|Ethnicity|Total|Not|Reported|"
                       r"Notes?|Source|These categories|\*|Westat|Table B\.8|Percents? may)", re.I)
    rows, pending, pages_used = [], "", set()
    for k, ln in lines:
        m = row_re.match(ln)
        if not m:
            s = ln.strip()
            if s and not noise.match(s) and not re.search(r"\d", s) and rows:
                pending = (pending + " " + s).strip()  # wrapped agency name (PC2020 layout)
            continue
        name = re.split(r"\s{2,}", m.group("name").strip())[-1]
        if pending:
            name, pending = f"{pending} {name}", ""
        rows.append({"name": name, "h": m.group("h"), "n": m.group("n"), "u": m.group("u"),
                     "t": int(m.group("t").replace(",", "")), "page": k})
        pages_used.add(k)
    gate(not pending, f"PC{year} B.8 no dangling wrapped name ({pending!r})")
    return rows, i, sorted(pages_used)


# ---------------------------------------------------------------- assemble
def year_rows(year: int, files: dict, pinned: dict) -> list[dict]:
    rep = pdf_pages(files["report"])
    app = pdf_pages(files["appendix"])
    full = " ".join(" ".join(p.split()) for p in rep)
    ref = f"April {year}"
    gate(re.search(rf"certif\w*[^.]{{0,80}}April {year}|April {year}[^.]{{0,80}}certif", full) is not None,
         f"PC{year} report ties its census to certifications in {ref}")
    n36, raw36, p36 = table_36(rep, year)
    a9, pa9 = table_a9(app, year)
    b8, pb8, pb8_all = table_b8(app, year)

    # national total: Table 3.6 = Table A.9 = Table B.8 header row
    tot = n36["total"][6]
    a9n = [int(t.replace(",", "")) for t in a9[(year, "n")]]
    gate(a9n == [n36["hisp"][6], n36["nonhisp"][6], n36["unk"][6], tot],
         f"PC{year} A.9 {year} counts {a9n} = Table 3.6 national counts")
    nat = [r for r in b8 if r["name"] == "Total Participants"]
    gate(len(nat) == 1 and nat[0]["t"] == tot, f"PC{year} B.8 national total = {tot:,}")
    b8pct = [nat[0][k].replace(" ", "") for k in "hnu"]
    t36pct = [raw36[(k, "pct")][6].replace(" ", "") for k in ("hisp", "nonhisp", "unk")]
    a9pct = [t.replace(" ", "") for t in a9[(year, "pct")][:3]]
    gate(b8pct == t36pct == a9pct,
         f"PC{year} national percents B.8 {b8pct} = Table 3.6 {t36pct} = A.9 {a9pct}")
    agencies = [r for r in b8 if r["name"] != "Total Participants"]
    stol = 0 if YEARS[year]["count_tol"] == 0 else 0.5 * len(agencies)
    gate(abs(sum(r["t"] for r in agencies) - tot) <= stol,
         f"PC{year} B.8: {len(agencies)} agency totals sum to {sum(r['t'] for r in agencies):,} = {tot:,}")
    names = [r["name"] for r in agencies]
    gate(len(set(names)) == len(names), f"PC{year} B.8 agency names unique")
    gate(set(STATES) <= set(names), f"PC{year} B.8 has all 50 states + DC "
         f"(missing {sorted(set(STATES) - set(names))})")
    terr = [nm for nm in names if nm in TERR]
    gate(len(terr) == 5, f"PC{year} B.8 has 5 territories: {terr}")
    if YEARS[year]["agencies"]:
        gate(len(agencies) == YEARS[year]["agencies"],
             f"PC{year} B.8 has {len(agencies)} state agencies (report: {YEARS[year]['agencies']})")
    # row-wise percent sums and the national Hispanic count rebuilt from rounded state percents
    est, tol = 0, 0.0
    for r in agencies:
        vals = [r[k].replace(" ", "") for k in "hnu"]
        if all(re.fullmatch(r"\d+\.\d", v) for v in vals):
            s = sum(float(v) for v in vals)
            gate(abs(s - 100) <= 0.2, f"PC{year} B.8 {r['name']}: percents sum to {s:.1f}")
        h = to_f(r["h"])
        if h is None:
            tol += r["t"]
        else:
            est += r["t"] * h / 100
            tol += r["t"] * 0.0005
    gate(abs(est - n36["hisp"][6]) <= tol,
         f"PC{year} B.8 state agencies imply {est:,.0f} Hispanic participants vs Table 3.6 "
         f"{n36['hisp'][6]:,} (tol {tol:,.0f} = percent rounding + suppressed cells)")

    rp = f"active certifications, {ref}"
    lab36 = f"pdf p.{p36 + 1} (printed {label(rep[p36])})"
    out = []
    for j, c in enumerate(CATS):
        h, nh, u, t = (n36[k][j] for k in ("hisp", "nonhisp", "unk", "total"))
        out.append({
            "source_year": year, "reference_period": rp, "geography": "United States (all state agencies)",
            "state_postal": "US", "category": c, "participants": t, "hispanic": h, "not_hispanic": nh,
            "ethnicity_unknown": u, "hispanic_share_known": round(h / (h + nh), 5),
            "hispanic_share_all": round(h / t, 5), "source_table": "Report Table 3.6",
            "source_page": lab36, "geography_type": "national",
            "hispanic_pct_published": raw36[("hisp", "pct")][j].replace(" ", ""),
            "not_hispanic_pct_published": raw36[("nonhisp", "pct")][j].replace(" ", ""),
            "unknown_pct_published": raw36[("unk", "pct")][j].replace(" ", ""),
            "value_basis": "published counts", "source_file": files["report"].name,
            "notes": "includes territories and Indian Tribal Organizations",
        })
    for r in agencies:
        nm = r["name"]
        gtype = "state" if nm in STATES else ("territory" if nm in TERR else "indian_tribal_organization")
        postal = STATES.get(nm) or TERR.get(nm) or ""
        h, nh, u = (to_f(r[k]) for k in "hnu")
        notes = []
        if gtype == "indian_tribal_organization":
            notes.append("Indian Tribal Organization; its participants are not in the state row")
        sup = [lab for lab, k in (("Hispanic", "h"), ("non-Hispanic", "n"), ("not reported", "u"))
               if r[k].strip() == "*"]
        if sup:
            notes.append("suppressed (*, small cell): " + ", ".join(sup))
        lt = [lab for lab, k in (("Hispanic", "h"), ("non-Hispanic", "n"), ("not reported", "u"))
              if r[k].replace(" ", "").startswith("<")]
        if lt:
            notes.append("published '<0.1' for " + ", ".join(lt) + " (share math uses 0.05)")
        out.append({
            "source_year": year, "reference_period": rp, "geography": nm, "state_postal": postal,
            "category": "all", "participants": r["t"],
            "hispanic": round(r["t"] * h / 100) if h is not None else None,
            "not_hispanic": round(r["t"] * nh / 100) if nh is not None else None,
            "ethnicity_unknown": (round(r["t"] * u / 100)
                                  if u is not None and not r["u"].strip().startswith("<") else None),
            "hispanic_share_known": round(h / (h + nh), 5) if h is not None and nh is not None and h + nh > 0 else None,
            "hispanic_share_all": round(h / 100, 5) if h is not None else None,
            "source_table": "Appendix Table B.8",
            "source_page": f"pdf p.{r['page'] + 1} (printed {label(app[r['page']])})", "geography_type": gtype,
            "hispanic_pct_published": r["h"].replace(" ", ""),
            "not_hispanic_pct_published": r["n"].replace(" ", ""),
            "unknown_pct_published": r["u"].replace(" ", ""),
            "value_basis": "counts derived: published percent (0.1 pt) x published total",
            "source_file": files["appendix"].name, "notes": "; ".join(notes),
        })
    return out, a9


def main():
    pins: dict = {}
    for rel, url in PAGES.items():
        fetch(url, CACHE / rel, lambda p: "WIC Participant" in p.read_text(errors="replace"), pins)
    viz = (CACHE / "wic/fna_wic_pc_dataviz_page.html").read_text(errors="replace")
    years_listed = sorted({int(y) for y in re.findall(r"participant-program-characteristics-(20\d\d)", viz)})
    gate(2024 not in years_listed and 2022 in years_listed,
         f"release page links PC reports {years_listed}: PC2024 not published, PC2022 latest")
    rows, a9s = [], {}
    for year, spec in YEARS.items():
        files = {k: fetch(BASE + spec[k], CACHE / "wic" / spec[k], is_pdf, pins)
                 for k in ("report", "appendix")}
        r, a9s[year] = year_rows(year, files, pins)
        rows += r
    # cross-document: PC2022's A.9 row for 2020 = PC2020's own national counts
    nat20 = next(r for r in rows if r["source_year"] == 2020 and r["category"] == "all"
                 and r["geography_type"] == "national")
    a = [int(t.replace(",", "")) for t in a9s[2022][(2020, "n")]]
    gate(a == [nat20["hispanic"], nat20["not_hispanic"], nat20["ethnicity_unknown"], nat20["participants"]],
         f"PC2022 A.9 row 2020 {a} = PC2020 Table 3.6")
    df = pd.DataFrame(rows)
    for c in ("participants", "hispanic", "not_hispanic", "ethnicity_unknown"):
        df[c] = df[c].astype("Int64")
    OUT.parent.mkdir(exist_ok=True)
    df.to_csv(OUT, index=False, lineterminator="\n")
    (CACHE / "wic" / "admin_wic_gates.log").write_text("\n".join(GATE_LOG) + "\n")
    print(f"{sum(g.startswith('PASS') for g in GATE_LOG)} gates passed; wrote "
          f"{OUT.relative_to(LANE)} ({len(df)} rows)")
    show = df[(df.state_postal.isin(["US", "CA", "TX", "AZ", "NM", "NV"])) & (df.category == "all")]
    print(show[["source_year", "state_postal", "participants", "hispanic", "hispanic_pct_published",
                "unknown_pct_published", "hispanic_share_known", "hispanic_share_all"]].to_string(index=False))
    print(df[df.geography_type == "indian_tribal_organization"].groupby("source_year").geography.apply(list).to_string())


if __name__ == "__main__":
    main()
