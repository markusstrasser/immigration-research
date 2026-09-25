#!/usr/bin/env python3
"""Read-only population diagnostic; does not re-estimate slopes or welfare costs.

Run from the project root:
UV_CACHE_DIR=/private/tmp/immigration-audit-uv-cache uv run --no-project python3 infra/immigration-fiscal/conceptual_audit_2026_09_25/probe_offbooks.py

Uses the exact lane PERSON SQL, then narrows its existing unauthorized flag to
Mexico-born persons. This is not an all-generation Mexican-origin classifier.
Outputs are written only to this audit's ignored _cache directory.
"""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

import duckdb
import pandas as pd

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
LANE = ROOT / 'infra/immigration-fiscal/compliance_gap_2026_09_24'
OUT = HERE / '_cache/offbooks'
sys.path.insert(0, str(LANE))
from acs_cells import PERSON  # noqa: E402


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open('rb') as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()


def main() -> None:
    for revs in (('beefbba',),):
        changed = subprocess.check_output(
            ['git', '-C', str(ROOT), 'diff', '--name-only', *revs, '--', str(LANE)], text=True).strip()
        if changed:
            raise SystemExit('[BLOCKED] off-books lane changed since audited snapshot: ' + changed)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    con = duckdb.connect()
    con.execute("SET threads=4")
    con.execute(f'CREATE TEMP VIEW p AS {PERSON}')
    raw = con.execute("""
        SELECT cell,
          sum(w * wage) / 1e9 AS all_origin_unauth_wages_bn,
          sum(w * wage) FILTER (WHERE mexborn) / 1e9 AS mexico_born_unauth_wages_bn,
          sum(w) AS all_origin_unauth_workers,
          sum(w) FILTER (WHERE mexborn) AS mexico_born_unauth_workers
        FROM p
        WHERE year=2024 AND st BETWEEN 1 AND 56 AND cw IN (22,23)
          AND unauth AND cell IN ('c23','c56173','c5617z','c722z')
        GROUP BY cell ORDER BY cell
    """).df().set_index('cell')
    panel = con.execute(f"""
        SELECT cell, sum(ws_wagebill_unauth)/1e9 AS panel_wages_bn
        FROM '{LANE}/_cache/panel/acs_cells.parquet'
        WHERE year=2024 AND half='all'
          AND cell IN ('c23','c56173','c5617z','c722z')
        GROUP BY cell
    """).df().set_index('cell')
    if not ((raw['all_origin_unauth_wages_bn'] - panel['panel_wages_bn']).abs() < 1e-8).all():
        raise RuntimeError('Person-level all-origin wages do not reproduce the cached panel')
    published = pd.read_csv(LANE / 'derived/edges_by_industry_year.csv')
    published = published[published.year.eq(2024)].set_index('cell').sort_index()
    share = raw.mexico_born_unauth_wages_bn / raw.all_origin_unauth_wages_bn
    cols = ['edge_bn_central', 'taxes_bn_central', 'workers_comp_bn_central',
            'underpayment_bn_central', 'offbooks_payroll_bn_central']
    scaled = published[cols].mul(share, axis=0)
    totals = pd.DataFrame({'published_all_origin': published[cols].sum(),
                           'mexico_born_same_slope': scaled.sum()})
    raw.assign(mexico_born_wage_share=share).to_csv(f'{OUT}-cells.csv', lineterminator='\n')
    totals.to_csv(f'{OUT}-totals.csv', lineterminator='\n')
    inputs = [LANE/'acs_cells.py', LANE/'cells.py', LANE/'edges.py',
              LANE/'derived/edges_by_industry_year.csv', LANE/'derived/uncovered_slopes.csv',
              LANE/'_cache/panel/acs_cells.parquet',
              *sorted((LANE/'_cache/ipums').glob('workers*.parquet'))]
    manifest = {
        'head': subprocess.check_output(['git', '-C', str(ROOT), 'rev-parse', 'HEAD'], text=True).strip(),
        'method': 'Exact PERSON SQL and panel filters; same published central cell slopes and rates, using Mexico-born share of the all-origin unauthorized wage base. Published rows are rounded; not a causal or welfare re-estimate.',
        'person_sql': PERSON,
        'inputs': [{'path': str(p), 'bytes': p.stat().st_size, 'sha256': digest(p)} for p in inputs],
        'all_origin_person_panel_check': 'PASS',
    }
    Path(f'{OUT}-manifest.json').write_text(json.dumps(manifest, indent=2)+'\n')
    print(totals.to_string())
    print('PASS: exact all-origin person totals reproduce panel; upstream inputs unchanged.')


if __name__ == '__main__':
    main()
