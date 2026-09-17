"""Aligned fiscal-year NYC shelter exposure; approximate census-days, not actual bed-nights."""
import argparse
import hashlib
import json
import subprocess
from pathlib import Path

import numpy as np
import pandas as pd
from bs4 import BeautifulSoup


def load_monthly(path):
    frame = pd.read_csv(path, dtype=str)
    # Official chart mixes Jun/June and Jul/July. Normalize month token only.
    date_labels = frame.iloc[:, 0].map(lambda s: s.split("-")[0][:3] + "-" + s.split("-")[1])
    dates = pd.to_datetime(date_labels, format="%b-%y")
    values = frame.iloc[:, 1:].apply(lambda s: pd.to_numeric(s.str.replace(",", "")))
    assert dates.is_unique and dates.is_monotonic_increasing
    values.index = dates
    return values


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--lane-dir", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    raw = args.lane_dir / "raw" / "local"
    out = args.lane_dir / "derived" / "local"
    out.mkdir(parents=True, exist_ok=True)
    manifest = json.loads((raw / "source_manifest.json").read_text())
    for entry in manifest:
        assert hashlib.sha256((raw / entry["filename"]).read_bytes()).hexdigest() == entry["sha256"]
    budget = BeautifulSoup((raw / "executive_fy2027.html").read_text(), "html.parser")
    tables = [t for t in budget.find_all("table") if "1,474" in t.get_text() and "1,455" in t.get_text()]
    assert len(tables) == 1
    budget_rows = {r.find_all(["td", "th"])[0].get_text(strip=True):
                   [c.get_text(strip=True).replace("$", "").replace(",", "") for c in r.find_all(["td", "th"])[1:]]
                   for r in tables[0].find_all("tr") if r.find_all(["td", "th"])}
    assert budget_rows["City"][:3] == ["1232", "2323", "1477"]
    assert budget_rows["Total"][:3] == ["1474", "3752", "3020"]
    paper_text = subprocess.run(["pdftotext", "-layout", str(raw / "meyer_wyse_williams_2026.pdf"), "-"],
                                check=True, capture_output=True, text=True).stdout
    assert "148,626" in paper_text and "66,700" in paper_text and "51,099" in paper_text
    people = load_monthly(raw / "AsylumSeekersbyShelterTypeStackedBar.csv")
    agencies = load_monthly(raw / "InCityCare.csv")
    # Population-type series has all three cells observed in every month we use.
    assert not people.isna().any().any()
    totals = people.sum(axis=1)
    agency_totals = agencies.sum(axis=1, min_count=1)
    reconciliation = pd.DataFrame({"type_total": totals, "agency_total": agency_totals}).dropna()
    reconciliation["difference"] = reconciliation.type_total - reconciliation.agency_total
    # The two official charts differ beyond rounding (max 521 people, Jan 2025).
    # Preserve both estimates; this is a source discrepancy, not a successful reconciliation.
    reconciliation.to_csv(out / "monthly_reconciliation.csv", index_label="month")
    rows = []
    for fy, total_m, city_m, rate in ((2024, 3752, 2323, 373), (2025, 3020, 1477, 371)):
        expected = pd.date_range(f"{fy-1}-07-01", f"{fy}-06-01", freq="MS")
        period = people.loc[expected]
        assert len(period) == 12
        days = period.index.days_in_month.to_numpy()
        type_days = float(period.sum(axis=1).to_numpy() @ days)
        agency_days = float(agency_totals.loc[expected].to_numpy() @ days)
        assert np.isfinite(agency_days) and agency_days > 0
        p_days = agency_days
        fwc_days = float(period["Families with Children"].to_numpy() @ days)
        rows.append({"fiscal_year": fy, "days": int(sum(days)),
                     "approx_census_person_days": p_days,
                     "approx_type_person_days": type_days,
                     "average_people": p_days / sum(days),
                     "share_people_in_families_with_children_type_series": fwc_days / type_days,
                     "program_accrued_millions": total_m, "city_funding_millions": city_m,
                     "program_dollars_per_census_person_day": total_m * 1e6 / p_days,
                     "city_dollars_per_census_person_day": city_m * 1e6 / p_days,
                     "reported_household_per_diem": rate})
    result = pd.DataFrame(rows)
    result.to_csv(out / "fiscal_year_exposure.csv", index=False)
    p0, p1 = result.iloc[0], result.iloc[1]
    # Exact symmetric accounting decomposition C = (C/N)N. Neither component is causal.
    c0, c1 = p0.program_accrued_millions * 1e6, p1.program_accrued_millions * 1e6
    n0, n1 = p0.approx_census_person_days, p1.approx_census_person_days
    u0, u1 = c0 / n0, c1 / n1
    volume = (n1 - n0) * (u0 + u1) / 2
    unit = (u1 - u0) * (n0 + n1) / 2
    assert np.isclose(volume + unit, c1 - c0, rtol=0, atol=1e-5)
    # Reproduce published Table 1 arithmetic, retaining its different estimators.
    homeless = [{"place": p, "change": ch, "direct": dr, "indirect": ind}
                for p, ch, dr, ind in (("NYC", 77352, 66700, 51099),
                    ("Chicago", 14590, 13679, 13629), ("Massachusetts", 13353, 7821, 7821),
                    ("Denver", 6556, 4300, 4727), ("Nationwide", 148626, 92500, 87611))]
    for row in homeless:
        row["direct_share"] = row["direct"] / row["change"]
        row["indirect_share"] = row["indirect"] / row["change"]
    pd.DataFrame(homeless).to_csv(out / "published_homelessness_accounting.csv", index=False)
    audit = {"status": "ARITHMETIC PASS; SOURCE RECONCILIATION DISCREPANCY", "source_hashes_verified": len(manifest),
             "maximum_monthly_reconciliation_difference": float(reconciliation.difference.abs().max()),
             "cost_change_millions": (c1 - c0) / 1e6,
             "volume_component_millions": volume / 1e6,
             "spending_per_census_day_component_millions": unit / 1e6,
             "volume_share_of_change": volume / (c1 - c0),
             "warning": "Census-days approximate person-time from monthly averages of reported counts; not actual occupied nights. Agency and household-type charts differ beyond rounding; both retained. Spending includes non-shelter services. Accounting decomposition, not causal savings or marginal costs."}
    (out / "audit.json").write_text(json.dumps(audit, indent=2) + "\n")
    print(result.to_string(index=False))
    print(json.dumps(audit, indent=2))


if __name__ == "__main__":
    main()
