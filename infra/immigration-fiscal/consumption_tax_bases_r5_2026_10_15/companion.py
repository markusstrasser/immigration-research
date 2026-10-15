#!/usr/bin/env python3
"""Bounded current-law companion. This does not create a v9 item or a full-law total.

Build: uv run --no-project python3 {lane}/companion.py
Acquire primary inputs first: the same command with --acquire (network required).
Strict certification: --require-full exits 2 until the explicit gaps are resolved.
Raw downloads are ignored _cache/companion*; tracked inputs pin their bytes.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import resource
import shutil
import subprocess
import sys
import time
from pathlib import Path
from urllib.parse import urlencode

import openpyxl

LANE = Path(__file__).resolve().parent
FISCAL = LANE.parent
ROOT = FISCAL.parents[1]
INPUTS = LANE / 'inputs'
CACHE = LANE / '_cache'
OUT = LANE / 'derived'
CASE = FISCAL / 'main_case_2026_10_15'
OLD = FISCAL / 'post2024_law_2026_10_07'
SCORES = ROOT / 'sources/immigration-fiscal/data/external/stage3/cbo/pl119_21_estimate/61570-pl119-21-2025Recon-CLB.xlsx'
PINNED_BEA = ROOT / 'sources/immigration-fiscal/data/external/bea_nipa/Section3All_xls.xlsx'
SCORE_SHA = 'b6f7a7ae822633a70d4abaec1e26e4b4ac428e7ed09fc3aee9dbd5d83c7bc552'
GAPS = [
    'No FY2028 tariff revenue under the surviving country/product schedules, their overlaps, and refunds is identified.',
    'The legacy individual/benefit rows use 42.752M v5 people; their tax-unit/eligibility shares have not been recomputed on 45.230M v8 people.',
    'JCT business scores compare with January-2025-law phase-down, whereas the companion describes a frozen-2024-law comparison; no baseline bridge is supplied.',
    'JCT scores combine corporate and pass-through revenue effects; no industry/legal-form split isolates federal corporate source tax. Whole-score allocation on item6 is conditional.',
    'Programme-wide benefit and other post-2024 tax changes omitted by the legacy companion remain outside the priced subtotal.',
]
MTS_QUERY = {
    'filter': 'record_date:gte:2023-10-01,record_date:lte:2025-12-31,classification_desc:eq:Customs Duties',
    'page[size]': '10000', 'sort': 'record_date',
}
MTS_URL = 'https://api.fiscaldata.treasury.gov/services/api/fiscal_service/v1/accounting/mts/mts_table_4?' + urlencode(MTS_QUERY)
URLS = {
    'mts_monthly.json': MTS_URL,
    'bea_section3.xlsx': 'https://apps.bea.gov/national/Release/XLS/Survey/Section3All_xls.xlsx',
    'scotus_ieepa.pdf': 'https://www.supremecourt.gov/opinions/25pdf/24-1287_4gcj.pdf',
    'cit_refunds.pdf': 'https://www.cit.uscourts.gov/sites/cit/files/26-123.pdf',
    'ending_ieepa.html': 'https://www.whitehouse.gov/presidential-actions/2026/02/ending-certain-tariff-actions/',
    'section122.html': 'https://www.whitehouse.gov/presidential-actions/2026/02/imposing-a-temporary-import-surcharge-to-address-fundamental-international-payments-problems/',
    'section232_apr.html': 'https://www.whitehouse.gov/presidential-actions/2026/04/strengthening-actions-taken-to-adjust-imports-of-aluminum-steel-and-copper-into-the-united-states/',
    'section232_jun.html': 'https://www.whitehouse.gov/presidential-actions/2026/06/further-adjusting-the-tariff-regimes-for-imports-of-aluminum-steel-and-copper-into-the-united-states/',
    'section232_jul.html': 'https://www.whitehouse.gov/presidential-actions/2026/07/further-strengthening-actions-taken-to-adjust-imports-of-aluminum-into-the-united-states/',
    'section301_final.pdf': 'https://ustr.gov/sites/default/files/files/Press/Releases/2026/FLIP%20301%20Investigation%20Final%20Action%20FRN%207-23-26%20FINAL.pdf',
    'section338_vehicles.html': 'https://www.whitehouse.gov/presidential-actions/2026/07/imposing-additional-duties-to-offset-canadian-discrimination-against-the-commerce-of-the-united-states-with-respect-to-motor-vehicles/',
    'section338_alcohol.html': 'https://www.whitehouse.gov/presidential-actions/2026/07/imposing-additional-duties-to-offset-canadian-discrimination-against-the-commerce-of-the-united-states-with-respect-to-alcoholic-beverages/',
    'section338_dairy.html': 'https://www.whitehouse.gov/presidential-actions/2026/07/imposing-additional-duties-to-offset-canadian-discrimination-against-the-commerce-of-the-united-states-with-respect-to-dairy/',
    'bea_methods.html': 'https://apps.bea.gov/scb/issues/2020/11-november/1120-nipa-methodologies.htm',
    'bea_methods_2026.html': 'https://apps.bea.gov/scb/issues/2026/09-september/0926-nipa-methodologies.htm',
    'bea_ieepa_refunds.html': 'https://www.bea.gov/index.php/help/faq/1488',
    'irs_depreciation.html': 'https://www.irs.gov/publications/p946',
    'irs_174a.html': 'https://www.irs.gov/irb/2025-38_IRB',
    'section338_sept_alcohol_ban.pdf': 'https://www.govinfo.gov/content/pkg/FR-2026-09-14/pdf/2026-18835.pdf',
    'section338_sept_alcohol_scope.pdf': 'https://www.govinfo.gov/content/pkg/FR-2026-09-14/pdf/2026-18838.pdf',
    'section338_sept_dairy_ban.pdf': 'https://www.govinfo.gov/content/pkg/FR-2026-09-14/pdf/2026-18836.pdf',
    'section338_sept_vehicles_ban.pdf': 'https://www.govinfo.gov/content/pkg/FR-2026-09-14/pdf/2026-18837.pdf',
    'section338_sept_vehicles_scope.pdf': 'https://www.govinfo.gov/content/pkg/FR-2026-09-14/pdf/2026-18839.pdf',
    'cit_301_docket.html': 'https://www.cit.uscourts.gov/audio-recordings-select-public-court-proceedings',
}


def gate(ok, why):
    if not ok:
        raise ValueError('[BLOCKED] companion: ' + why)


def sha(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()


def write_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, allow_nan=False) + '\n')


def acquire():
    gate(shutil.disk_usage(LANE).free > 10 * 1024**3, 'less than 10GB free before downloads')
    CACHE.mkdir(exist_ok=True)
    sources = []
    for name, url in URLS.items():
        path = CACHE / ('companion_' + name)
        if not path.exists():
            # macOS curl uses the system trust store. The uv Python OpenSSL store
            # lacks this sandbox's proxy CA; preserve TLS verification via curl.
            fetched = subprocess.run(['curl', '--fail', '--silent', '--show-error', '--location',
                                      '--max-time', '45', url], capture_output=True, check=False)
            gate(fetched.returncode == 0, f'download failed {name}: {fetched.stderr.decode()[-500:]}')
            data = fetched.stdout
            gate(len(data) > 100, f'empty download {name}')
            if name.endswith('.pdf'):
                gate(data.startswith(b'%PDF'), f'not PDF {name}')
            if name.endswith('.xlsx'):
                gate(data.startswith(b'PK'), f'not XLSX {name}')
            path.write_bytes(data)
        sources.append({'path': str(path.relative_to(LANE)), 'url': url, 'sha256': sha(path), 'bytes': path.stat().st_size})
        print('source', name, path.stat().st_size)
    for path in [SCORES, PINNED_BEA, CASE / 'package.cjs', CASE / 'derived/corrections.json', CASE / 'derived/corrections_cash.json', OLD / 'derived/summary.json', OLD / 'derived/tax_summary.json', INPUTS / 'companion_legal.json']:
        sources.append({'path': str(path.relative_to(ROOT)), 'root': 'repo', 'sha256': sha(path), 'bytes': path.stat().st_size})
    write_json(INPUTS / 'companion_sources.json', {'as_of': '2026-10-15', 'sources': sources})


def verify_sources():
    pins = json.loads((INPUTS / 'companion_sources.json').read_text())
    for row in pins['sources']:
        path = (ROOT if row.get('root') == 'repo' else LANE) / row['path']
        gate(path.exists(), f'missing {path}; run --acquire for cached sources')
        gate(sha(path) == row['sha256'], f'stale source {path}; review source changes before repinning')
    gate(sha(SCORES) == SCORE_SHA, 'CBO61570 workbook differs from verified source')


def read_bea(path):
    wb = openpyxl.load_workbook(path, read_only=True, data_only=True)
    try:
        rows = list(wb['T30200-A'].values)
        years = next(r for r in rows if str(r[0]).strip() == 'Line')
        row = next(r for r in rows if len(r) > 2 and r[2] == 'B235RC')
        out = {int(y): float(row[i]) / 1e3 for i, y in enumerate(years) if str(y) in ('2024', '2025')}
        vintage = next(str(r[0]) for r in rows if str(r[0]).startswith('Data published'))
        gate(set(out) == {2024, 2025}, 'BEA customs does not span 2024/2025')
        return {'bn': out, 'vintage': vintage, 'table': '3.2 line 6, B235RC, annual; source units $million'}
    finally:
        wb.close()


def customs_bridge():
    data = json.loads((CACHE / 'companion_mts_monthly.json').read_text())
    rows = data['data']
    gate(len(rows) == 27, 'Treasury monthly customs must contain exactly Oct2023-Dec2025 (27 rows)')
    gate(len({r['record_date'] for r in rows}) == len(rows), 'duplicate Treasury customs months')
    monthly = {r['record_date'][:7]: float(r['current_month_net_rcpt_amt']) / 1e9 for r in rows}
    sept = next(r for r in rows if r['record_date'] == '2025-09-30')
    fy25 = float(sept['current_fytd_net_rcpt_amt']) / 1e9
    fy24 = float(sept['prior_fytd_net_rcpt_amt']) / 1e9
    gate(abs(fy25 - 194.86573987282) < 1e-10 and abs(fy24 - 77.03690994489) < 1e-10, 'FY2025/FY2024 Table4 values differ from W16 primary receipt')
    pinned, current = read_bea(PINNED_BEA), read_bea(CACHE / 'companion_bea_section3.xlsx')
    bridge = []
    for year, fy in [(2024, fy24), (2025, fy25)]:
        prior_q4 = sum(monthly[f'{year-1}-{month:02}'] for month in (10, 11, 12))
        current_q4 = sum(monthly[f'{year}-{month:02}'] for month in (10, 11, 12))
        cy = sum(monthly[f'{year}-{month:02}'] for month in range(1, 13))
        gate(abs(fy - prior_q4 + current_q4 - cy) < 1e-8, f'FY→CY identity {year}')
        bridge.append({'year': year, 'fy_cash_bn': fy, 'subtract_prior_oct_dec_bn': prior_q4,
                       'add_current_oct_dec_bn': current_q4, 'calendar_cash_bn': cy,
                       'pinned_nipa_bn': pinned['bn'][year], 'pinned_nipa_less_calendar_cash_bn': pinned['bn'][year] - cy,
                       'current_nipa_bn': current['bn'][year], 'current_nipa_less_calendar_cash_bn': current['bn'][year] - cy})
    return {'bridge': bridge, 'pinned_bea': pinned, 'current_bea': current,
            'residual_interpretation': 'Observed bridge residual, not identified wholly as accrual. BEA uses Treasury MTS customs; vintage, coverage and accounting adjustments are not separately identified here.',
            'future_policy_assumption': None, 'fy2028_customs_bn': None,
            'ieepa_refund_accounting': {'source': URLS['bea_ieepa_refunds.html'], 'source_date': '2026-04-30',
                                       'accrual_period': '2026Q1', 'capital_transfer_bn': 166,
                                       'treatment': 'One-time capital transfer, separate from current customs; interest separately property income. Not recurring FY2028 customs reduction.'}}


def business_scores():
    wb = openpyxl.load_workbook(SCORES, read_only=True, data_only=True)
    try:
        rows = list(wb['Title VII'].values)
        out = {}
        for section, expected in [(70301, -57507), (70302, -13794)]:
            start = next(i for i, r in enumerate(rows) if any(str(c).strip() == str(section) for c in r if c is not None))
            row = next(r for r in rows[start:start+8] if str(r[2]).startswith('Estimated Revenues'))
            gate(row[6] == expected, f'JCT FY2028 section {section} printed cell')
            out[str(section)] = {'fy2028_revenue_change_nominal_bn': float(row[6]) / 1e3,
                                 'excel_cell': f"'Title VII'!G{rows.index(row)+1}",
                                 'comparison': 'JCT/CBO January2025 current-law baseline, NOT frozen2024 law',
                                 'corporate_pass_through_split': None}
        return out
    finally:
        wb.close()


NODE_EXTRACT = r'''
const P=require(process.argv[1]);
const fs=require('fs'),path=require('path');
const out={population:P.POPULATION_V8, rows:[]};
for(const which of ['set','cash']){
 const X=which==='set'?P:P.CASH;
 const stored=JSON.parse(fs.readFileSync(path.join(path.dirname(process.argv[1]),'derived',which==='set'?'corrections.json':'corrections_cash.json'),'utf8'));
 if(JSON.stringify(X.correctionsPayload())!==JSON.stringify(stored))throw Error('[BLOCKED] live '+which+' payload differs from pinned derived payload');
 for(const [i,end] of ['low','high'].entries()){
  const s=X.MAIN_SPECS[[16,11][i]],methods=[];
  for(const method of P.METHODS){
   const m=X.modelFor('central',method,X.withCentral({}));
   const r=X.evaluateFull(m,s), ev=r.evaluation;
   const wanted=['customs_duties','corporate_capital','corporate_labor'];
   const carriers=X.correctionsPayload().meta.union_completion.carriers;
   const lines=ev.receipts.filter(l=>wanted.includes(l.id));
   const totals=Object.fromEntries(wanted.map(id=>[id,0]));
   for(const l of lines)totals[l.id]+=l.effect_bn;
   // v8 represents completion receipts as signed spending carriers. Its
   // evaluated welfare effect has the receipt sign and the active scenario.
   for(const l of ev.spending){const src=carriers[l.id];if(src?.side==='receipt'&&wanted.includes(src.parent_line))totals[src.parent_line]+=l.effect_bn;}
   // Native-child receipt cells are present in the evaluated model and source map as well.
   for(const l of ev.receipts)if(l.id.startsWith('native_child_receipt_')){
    const id=l.id.slice('native_child_receipt_'.length);if(wanted.includes(id)&&!lines.some(x=>x.id===l.id))totals[id]+=l.effect_bn;
   }
   const cov=X.POST_ENGINE.coverage.by_end[end].decomposition.line_parts;
   for(const l of cov)if(l.source_side==='receipt'&&wanted.includes(l.source_line))totals[l.source_line]-=l.coverage_bn;
   const national=Object.fromEntries(wanted.map(id=>[id,m.receipts.lines.find(l=>l.id===id).national_bn]));
   methods.push({method,cost_bn:r.cost_bn,attributed_responsive_receipts_bn:totals,national_bn:national});
  }
  out.rows.push({which,end,spec:[16,11][i],reading:s.reading,methods});
 }
}
console.log(JSON.stringify(out));
'''


def case_keys():
    p = subprocess.run(['node', '-e', NODE_EXTRACT, str(CASE / 'package.cjs')], cwd=ROOT, capture_output=True, text=True, check=False)
    gate(p.returncode == 0, 'v8 extraction failed: ' + p.stderr[-2000:])
    data = json.loads(p.stdout)
    gate(abs(data['population']['with_coverage'] - 45230062.30075857) < 1e-5, 'v8 lineage denominator drift')
    expected = {'set': (365.791930, 455.981785), 'cash': (281.752564, 371.942418)}
    for row in data['rows']:
        mean_cost = sum(m['cost_bn'] for m in row['methods']) / len(row['methods'])
        gate(abs(mean_cost - expected[row['which']][row['end'] == 'high']) < 1e-6, f"v8 unchanged {row['which']}/{row['end']}")
        row['baseline_cost_bn'] = mean_cost
        row['corporate_share_after_response'] = sum(sum(m['attributed_responsive_receipts_bn'][l] for l in ('corporate_capital', 'corporate_labor')) /
            sum(m['national_bn'][l] for l in ('corporate_capital', 'corporate_labor')) for m in row['methods']) / len(row['methods'])
        row['customs_share_after_response'] = sum(m['attributed_responsive_receipts_bn']['customs_duties'] / m['national_bn']['customs_duties'] for m in row['methods']) / len(row['methods'])
    return data


def full_total(summary):
    gate(not summary['gaps'] and summary['coherent_full_law_net_taken_bn'] is not None,
         'full current-law total unavailable: ' + '; '.join(summary['gaps']))
    return summary['coherent_full_law_net_taken_bn']


def build(out_dir=OUT):
    verify_sources()
    bridge, scores, keys = customs_bridge(), business_scores(), case_keys()
    old = json.loads((OLD / 'derived/tax_summary.json').read_text())
    deflator = old['deflator_fy2028']
    population = keys['population']['with_coverage']
    rows = []
    for key in keys['rows']:
        for section, score in scores.items():
            value = -score['fy2028_revenue_change_nominal_bn'] * deflator * key['corporate_share_after_response']
            rows.append({'part': 'business_expensing_conditional', 'section': section, 'which': key['which'], 'end': key['end'],
                         'nominal_national_bn': -score['fy2028_revenue_change_nominal_bn'], 'price_year': 2024, 'policy_year': 'FY2028',
                         'item6_share_after_response': key['corporate_share_after_response'], 'delta_net_cost_bn': value,
                         'delta_net_taken_bn': -value, 'per_member_usd': value * 1e9 / population,
                         'status': 'conditional_allocation_of_entire_JCT_score; not frozen2024 law change'})
        cpi25 = json.loads((OLD / 'derived/summary.json').read_text())['cpi_u_growth']['2025']
        for vintage in ('pinned_bea', 'current_bea'):
            national = bridge[vintage]['bn']
            delta = national[2025] - national[2024]
            # Historical sensitivity uses CY2025 prices, never the FY2028 deflator.
            value = -key['customs_share_after_response'] * (national[2025] / (1 + cpi25) - national[2024])
            rows.append({'part': 'customs_historical_' + vintage, 'section': 'customs', 'which': key['which'], 'end': key['end'],
                         'nominal_national_bn': delta, 'price_year': 2024, 'policy_year': 'CY2025 vs CY2024 historical',
                         'item6_share_after_response': '', 'delta_net_cost_bn': value, 'delta_net_taken_bn': -value,
                         'per_member_usd': value * 1e9 / population,
                         'status': 'v8 household customs key fixed; item18 joint business-base update not applied; not FY2028 law'})
    summary = {'as_of': '2026-10-15', 'verdict': 'PARTIAL: the legacy roughly-breaks-even statement is not certified for full current law or the v8 lineage.',
               'replacement_lead': 'The priced individual/eligibility subset approximately balances on the legacy v5 frame. Full current-law net effects for FY2028 and the 45.23M v8 lineage remain unidentified; business expensing is a conditional cost increase and the historical customs expansion is not a legally sustainable FY2028 projection.',
               'headline_2024_law_change_bn': {'set': [0, 0], 'cash': [0, 0]},
               'population_v8': keys['population'], 'deflator_fy2028_to2024': deflator, 'scores': scores,
               'legacy_companion_net_taken_bn': old['net_benefit_cuts_minus_tax_cuts_bn'],
               'customs_bridge': bridge, 'case_keys': keys, 'rows': rows, 'gaps': GAPS,
               'coherent_full_law_net_taken_bn': None,
               'legal_status': json.loads((INPUTS / 'companion_legal.json').read_text()),
               'interactions': ['Item9 domestic-source fractions are inside extracted item6 receipts.',
                                'Items10 and12 carriers/coverage receipts enter the extracted shares; the denominator is 45.230M.',
                                'Item11 held fixed: no current-law mixed-household resimulation.',
                                'Item18 customs base revision is excluded here to prevent counting it twice; historical customs uses the v8 household key.',
                                'Expensing score allocation is a sensitivity on the item6 corporate base. JCT actual corporate/pass-through and industry exposure is unresolved.']}
    out_dir.mkdir(parents=True, exist_ok=True)
    write_json(out_dir / 'companion_summary.json', summary)
    with (out_dir / 'companion_rows.csv').open('w', newline='') as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]), lineterminator='\n')
        writer.writeheader()
        writer.writerows(rows)
    write_json(out_dir / 'companion_bridge.json', bridge)
    print('[DEGRADED] Bounded companion written; coherent FY2028 current-law total withheld.')
    for row in rows:
        print(f"{row['part']}/{row['section']}/{row['which']}/{row['end']}: delta_cost_bn={row['delta_net_cost_bn']:.9f}")
    return summary


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--acquire', action='store_true')
    parser.add_argument('--require-full', action='store_true')
    parser.add_argument('--out-dir', type=Path, default=OUT)
    args = parser.parse_args()
    start = time.perf_counter()
    try:
        if args.acquire:
            acquire()
            return
        summary = build(args.out_dir)
        if args.require_full:
            full_total(summary)
    except (ValueError, OSError) as exc:
        print(str(exc), file=sys.stderr)
        raise SystemExit(2)
    finally:
        # Timing varies and belongs in ignored cache, outside deterministic derived outputs.
        peak = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        if sys.platform != 'darwin':
            peak *= 1024
        CACHE.mkdir(exist_ok=True)
        child_peak = resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss
        if sys.platform != 'darwin':
            child_peak *= 1024
        write_json(CACHE / 'companion_runtime.json', {'seconds': time.perf_counter() - start, 'python_peak_rss_bytes': peak,
                    'children_peak_rss_bytes': child_peak})
        gate(peak < 2.5e9, 'Python physical memory exceeded 2.5GB')
        gate(child_peak < 2.5e9, 'child physical memory exceeded 2.5GB')


if __name__ == '__main__':
    main()
