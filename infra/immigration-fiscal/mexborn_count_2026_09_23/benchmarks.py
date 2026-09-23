"""Parse the published numbers this lane uses from their primary documents in _cache/sources/.

- OHSS, "Estimates of the Lawful Permanent Resident Population in the United States and the
  Subpopulation Eligible to Naturalize: 2025 and Revised 2024", Table 2a, Mexico row. Fetched with
  curl -A <browser UA> from
  https://ohss.dhs.gov/topics/immigration/lawful-permanent-residents/population-estimates/fy-25-lpr-pop-estimates
  -> ohss_lpr_pop_fy25.html.
- BLS, "Adjustments to Household Survey Population Estimates in January 2025" and "... 2026"
  (bls.gov/cps/methods/population-controls/population-control-adjustments-{2025,2026}.pdf), table
  rows "Civilian noninstitutional population" for the total 16+ and for Hispanic or Latino
  ethnicity; text extracted with `pdftotext -layout`.
- CMS (Allen, Warren and Pacas 2026, JMHS), Table 5 Mexico row, and MPI (Gelatt, Ruiz Soto and
  Bachmeier, fact sheet, October 2025), from the unauthorized lane's cached copies.

Writes derived/benchmarks_parsed.csv.
"""
from __future__ import annotations

import html
import re
from pathlib import Path

import pandas as pd

HERE = Path(__file__).resolve().parent
SRC = HERE / "_cache/sources"
UNAUTH = HERE.parent / "unauthorized_population_size_2026_09_19/_cache/sources"


def text_of(path: Path) -> str:
    s = path.read_text(encoding="utf-8", errors="replace")
    return html.unescape(re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", s)))


def num(s: str) -> float:
    return float(s.replace(",", ""))


def main() -> None:
    rows = []
    t = text_of(SRC / "ohss_lpr_pop_fy25.html")
    table = t[t.index("Table 2a. Estimated Resident LPR Population by Country of Birth"):]
    m = re.search(r"Mexico ([\d,]+) ([\d,]+) ([\d.]+)%", table)
    rows += [dict(source="OHSS LPR population, Table 2a", item="Mexico-born LPRs, January 1 2024 (revised)",
                  value=num(m.group(1)), unit="persons"),
             dict(source="OHSS LPR population, Table 2a", item="Mexico-born LPRs, January 1 2025",
                  value=num(m.group(2)), unit="persons")]

    for year in (2025, 2026):
        b = (SRC / f"bls_population_control_adjustments_{year}.txt").read_text(encoding="utf-8")
        cnp = re.findall(r"Civilian noninstitutional population\s+([\d,]+)\s+([\d,]+)\s+(-?[\d,]+)", b)
        hisp_block = b[b.index("HISPANIC OR LATINO ETHNICITY"):]
        h = re.search(r"Civilian noninstitutional population\s+([\d,]+)\s+([\d,]+)\s+(-?[\d,]+)", hisp_block)
        rows += [dict(source=f"BLS population control adjustments {year}", item=f"January {year} change, civilian noninstitutional 16+ (thousands)",
                      value=num(cnp[0][2]), unit="thousands"),
                 dict(source=f"BLS population control adjustments {year}", item=f"January {year} change, Hispanic or Latino 16+ (thousands)",
                      value=num(h.group(3)), unit="thousands"),
                 dict(source=f"BLS population control adjustments {year}", item=f"Hispanic or Latino 16+ before the January {year} controls (thousands)",
                      value=num(h.group(1)), unit="thousands")]

    cms = (UNAUTH / "cms_warren_2024.md").read_text(encoding="utf-8")
    cms = cms[cms.index("Table 5. CMS Estimates of the Undocumented Population in 2024"):]
    m = re.search(r"\| Mexico \| ([\d,]+) \| ([\d,]+) \| ([\d,]+) \| ([\d,]+) \|", cms)
    rows += [dict(source="CMS 2024, Table 5", item="Mexican undocumented, 2020 (thousands)", value=num(m.group(1)), unit="thousands"),
             dict(source="CMS 2024, Table 5", item="Mexican undocumented, 2024 (thousands)", value=num(m.group(4)), unit="thousands")]
    mpi = re.sub(r"\s+", " ", (UNAUTH / "mpi_fact_sheet_2025.txt").read_text(encoding="utf-8")).replace("- ", "")
    m = re.search(r"stood at ([\d.]+) million as of mid-2023", mpi)
    rows.append(dict(source="MPI fact sheet 2025", item="Mexican unauthorized, mid-2023 (millions)", value=float(m.group(1)), unit="millions"))

    out = pd.DataFrame(rows)
    out.to_csv(HERE / "derived/benchmarks_parsed.csv", index=False)
    print(out.to_string(index=False))


if __name__ == "__main__":
    main()
