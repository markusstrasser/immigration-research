#!/usr/bin/env python3
"""Reconcile the named NYC shelter ledger; no causal or full-fiscal estimate.

Run with --source-dir containing the official source snapshots named below.
Native-First: small HTML/PDF table extraction and arithmetic; no warehouse writes.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
from pathlib import Path
from bs4 import BeautifulSoup


def money(value: str) -> float:
    clean = value.replace('$', '').replace(',', '').strip()
    return 0.0 if clean in ('–', '—', '-') else float(clean)


def funding_rows(source: Path) -> list[dict]:
    soup = BeautifulSoup(source.read_bytes(), 'html.parser')
    candidates = [t for t in soup.find_all('table')
                  if all(s in t.get_text(' ', strip=True)
                         for s in ('FY 2023', '$1,474', 'City', 'State', 'Federal'))]
    if len(candidates) != 1:
        raise ValueError(f'Expected one funding table, found {len(candidates)}')
    rows = {}
    for tr in candidates[0].find_all('tr'):
        cells = [x.get_text(' ', strip=True) for x in tr.find_all(['th', 'td'])]
        if cells and cells[0] in ('City', 'State', 'Federal', 'Total'):
            if cells[0] in rows:
                raise ValueError(f'Duplicate financing row: {cells[0]}')
            rows[cells[0]] = [money(v) for v in cells[1:4]]
    if set(rows) != {'City', 'State', 'Federal', 'Total'}:
        raise ValueError('Missing required financing source')
    result = []
    for i, year in enumerate((2023, 2024, 2025)):
        gross, city, state, federal = (rows[k][i] for k in ('Total','City','State','Federal'))
        residual = gross - city - state - federal
        if abs(residual) > 1.0:
            raise ValueError(f'Financing fails million-dollar rounding reconciliation: {year}')
        result.append(dict(fiscal_year=year, gross_usd_millions=gross,
                           city_financing_reported_usd_millions=city,
                           state_financing_usd_millions=state,
                           federal_financing_usd_millions=federal,
                           city_residual_calculated_usd_millions=gross-state-federal,
                           rounding_residual_usd_millions=residual,
                           city_share_percent=100*city/gross))
    return result


def text_paragraph(source: Path, start: str) -> str:
    soup = BeautifulSoup(source.read_bytes(), 'html.parser')
    values = [p.get_text(' ', strip=True) for p in soup.find_all('p')]
    found = [v for v in values if v.startswith(start)]
    if len(found) != 1:
        raise ValueError(f'Expected one source paragraph starting {start!r}, found {len(found)}')
    return found[0]


def write_csv(path: Path, rows: list[dict]):
    with path.open('w', newline='') as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def analyze(source_dir: Path, out: Path):
    required = ['nyc_executive_fy2027.html','nyc_fiscal_impacts.html','nyc_cash_report.html']
    fingerprints = {name: hashlib.sha256((source_dir/name).read_bytes()).hexdigest() for name in required}
    rows = funding_rows(source_dir/'nyc_executive_fy2027.html')
    summary = {key: sum(row[key] for row in rows) for key in rows[0]
               if key not in ('fiscal_year','city_share_percent')}
    summary['city_share_percent'] = 100*summary['city_financing_reported_usd_millions']/summary['gross_usd_millions']
    fy25 = rows[2]
    risk_text = text_paragraph(source_dir/'nyc_executive_fy2027.html', 'To date, the City has received $120 million in FEMA funding')
    risk = re.search(r'for a total of \$([\d.]+) million', risk_text)
    if risk is None:
        raise ValueError('Federal receivable risk source format changed')
    summary['fy25_federal_receivable_at_risk_usd_millions'] = float(risk.group(1))
    summary['fy25_city_if_federal_receivable_lost_usd_millions'] = fy25['city_financing_reported_usd_millions']+float(risk.group(1))
    cash_text = text_paragraph(source_dir/'nyc_cash_report.html', 'In FYTD26, the City spent')
    cash = re.match(r'In FYTD26, the City spent \$([\d.]+)\s+billion overall on migrant-related services, compared to \$([\d.]+)\s+billion in FYTD25\.', cash_text)
    if cash is None:
        raise ValueError('Quarterly cash source format changed')
    cash_new, cash_old = map(float, cash.groups())
    summary['cash_july_march_fy26_usd_billions'] = cash_new
    summary['cash_july_march_fy25_usd_billions'] = cash_old
    summary['cash_july_march_change_percent'] = 100*(cash_new/cash_old-1)
    rate_text = text_paragraph(source_dir/'nyc_fiscal_impacts.html', 'OMB shared that the FY 2025 per diem')
    rate = float(re.search(r'was \$([\d.]+)', rate_text).group(1))
    summary['fy25_reported_usd_per_household_night'] = rate
    summary['fy25_implied_household_nights_if_same_cost_scope'] = fy25['gross_usd_millions']*1e6/rate
    summary['fy25_implied_mean_households_if_same_cost_scope'] = summary['fy25_implied_household_nights_if_same_cost_scope']/365
    summary['person_year_cost'] = None
    summary['person_year_cost_status'] = 'Not identified: no matched aggregate person-nights or mean household size'
    # Algebraic rate conversion under explicitly hypothetical household sizes.
    # No empirical size distribution is asserted, and these are not uncertainty bounds.
    scenarios = [dict(assumed_mean_persons_per_household=m,
                      gross_usd_per_person_night=rate/m,
                      gross_usd_per_full_year_person=rate*365/m)
                 for m in (1,2,3,4)]
    out.mkdir(parents=True, exist_ok=True)
    write_csv(out/'nyc_financing_fy2023_25.csv', rows)
    write_csv(out/'household_to_person_scenarios.csv', scenarios)
    (out/'local_cost_summary.json').write_text(json.dumps(dict(
        ledger='NYC asylum shelter and related services; fiscal-year nominal dollars; financing is accrued/assigned, not cash receipts or net migrant fiscal impact',
        source_sha256=fingerprints, results=summary), indent=2)+'\n')
    print(json.dumps(summary, indent=2))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source-dir', type=Path, required=True)
    parser.add_argument('--out-dir', type=Path, required=True)
    args = parser.parse_args()
    analyze(args.source_dir, args.out_dir)
