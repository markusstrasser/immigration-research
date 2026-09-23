"""Sum the audit's effects on the main case ($203.2-249.6bn) into one net range.

Effects are $bn a year of cost to other residents; negative means the published main case is too
high. Each row is (low, central, high) as the family reports give it; `low` is the most negative.
Rows 11 and 12 are classification and key choices, reported beside the net, not in it.
Run: uv run --no-project python3 infra/immigration-fiscal/dataset_integrity_2026_09_23/synthesis.py
"""
import csv
import json
import pathlib

HERE = pathlib.Path(__file__).resolve().parent
MAIN_CASE = (203.2, 249.6)
mts = json.loads((HERE / "derived" / "spending_mts_credits.json").read_text())
ptc = mts["ptc_effect_on_main_case_bn"]

ROWS = [
    # id, label, low, central, high, measured (adoptable now), source
    ("1", "premium tax credits keyed as EITC+ACTC", ptc, ptc, ptc, True, "spending.md #1; spending_mts_credits.py"),
    ("2", "tax model assumes resident, compliant filers", 5.0, 10.6, 17.0, False, "cps.md row 1: 75% / 60% / 44% on-books"),
    ("3", "federal gap keyed by CPS liability", 9.48, 9.48, 9.48, True, "cps.md row 2 (federal_gap_high_agi arm)"),
    ("4", "ASEC 2025 Mexico-born count above ACS", -8.3, -7.1, -6.0, False, "cps.md row 3, if the ACS level is right"),
    ("5", "Medicaid long-term care keyed by MEPS community key", -15.0, -9.3, -3.6, False, "spending.md #3 (bound; central = midpoint)"),
    ("6", "education key 93% K-12", -4.8, -3.5, -2.2, True, "spending.md #5"),
    ("7", "justice key on FBI 2019 arrests", 1.12, 1.12, 1.12, True, "crime.md #1 (2024 Table 43C)"),
    ("8", "unallocable S&L spending given the administration elasticity", 2.0, 2.0, 2.0, True, "spending.md #7"),
    ("9", "MEPS donor filter", -2.0, -1.0, 0.0, False, "spending.md #4 (bound)"),
    ("10", "foster care keyed by WIC", -2.0, -1.5, -1.0, False, "spending.md #9 (bound)"),
    ("small", "origin allocation, grants, top-codes, flags", -0.5, -0.1, 0.4, False, "cps.md rows 4-6, 12; spending.md #8, #11"),
]
BESIDE = [
    ("11", "household rental assistance held fixed", 0.0, 7.5, "spending.md #6: 0 now, +7.5 if it responded fully"),
    ("12", "income-security consumption keyed by public assistance", -20.0, -7.5, "spending.md #12: -7.5 population key, -20 all-cash key"),
]


def main():
    low = sum(r[2] for r in ROWS)
    cen = sum(r[3] for r in ROWS)
    high = sum(r[4] for r in ROWS)
    m_rows = [r for r in ROWS if r[5]]
    m_low, m_cen, m_high = (sum(r[i] for r in m_rows) for i in (2, 3, 4))
    out = HERE / "derived" / "synthesis_net.csv"
    with out.open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["row", "item", "low_bn", "central_bn", "high_bn", "measured", "source"])
        for r in ROWS:
            w.writerow([r[0], r[1], f"{r[2]:.2f}", f"{r[3]:.2f}", f"{r[4]:.2f}", r[5], r[6]])
        w.writerow(["net", "rows 1-10 + small", f"{low:.2f}", f"{cen:.2f}", f"{high:.2f}", "", ""])
        w.writerow(["measured", "rows " + ",".join(r[0] for r in m_rows), f"{m_low:.2f}", f"{m_cen:.2f}", f"{m_high:.2f}", "", ""])
        for b in BESIDE:
            w.writerow([b[0], b[1], f"{b[2]:.2f}", "", f"{b[3]:.2f}", "choice", b[4]])
    print(f"net {low:.1f} / {cen:.1f} / {high:.1f}")
    print(f"main case at central net: {MAIN_CASE[0] + cen:.1f}-{MAIN_CASE[1] + cen:.1f}")
    print(f"measured rows {[r[0] for r in m_rows]}: {m_low:.1f} / {m_cen:.1f} / {m_high:.1f}"
          f" -> main case {MAIN_CASE[0] + m_cen:.1f}-{MAIN_CASE[1] + m_cen:.1f}")
    print(f"with choices 11-12: {low + BESIDE[1][2]:.1f} to {high + BESIDE[0][3]:.1f}")


if __name__ == "__main__":
    main()
