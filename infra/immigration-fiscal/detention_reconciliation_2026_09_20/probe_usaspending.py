from pathlib import Path
import csv, io, json, zipfile, hashlib
from acquire import verified_bytes
from decimal import Decimal
from collections import defaultdict

ROOT = Path(__file__).resolve().parent
OUT = ROOT / 'derived'
OUT.mkdir(exist_ok=True)
raw = verified_bytes('dhs_fy2024_fileab.zip')
def require(ok, message):
    if not ok:
        raise ValueError(message)

with zipfile.ZipFile(io.BytesIO(raw)) as z:
    names = z.namelist()
    require(len(names) == 2, 'expected A and B members')
    an = next(n for n in names if 'AccountBalances' in n)
    bn = next(n for n in names if 'BreakdownByPA-OC' in n)
    a = list(csv.DictReader(io.TextIOWrapper(z.open(an), encoding='utf-8-sig')))
    b = list(csv.DictReader(io.TextIOWrapper(z.open(bn), encoding='utf-8-sig')))
require(a and b, 'empty source')
periods = sorted(set(r['submission_period'] for r in a+b))
require(periods == ['FY2024P12'], 'unexpected or mixed reporting period')
accounts = {'0540', '5382', '5126'}
selected = [r for r in b if r['agency_identifier_code'] == '070' and r['main_account_code'] in accounts]
require(selected, 'no target account rows')
amounts = defaultdict(lambda: [Decimal(0), Decimal(0), 0])
for r in selected:
    k = (r['treasury_account_symbol'], r['program_activity_code'], r['program_activity_name'])
    amounts[k][0] += Decimal(r['obligations_incurred'] or '0')
    amounts[k][1] += Decimal(r['gross_outlay_amount_FYB_to_period_end'] or '0')
    amounts[k][2] += 1
groups = [dict(tas=k[0], code=k[1], program=k[2], obligations=str(v[0]), outlays=str(v[1]), rows=v[2]) for k,v in sorted(amounts.items())]
ero = [r for r in groups if r['code'] == '0005' and '-0540-' in r['tas']]
ero_total = sum((Decimal(r['outlays']) for r in ero), Decimal(0))
ero_current = sum((Decimal(r['outlays']) for r in ero if r['tas'] == '070-2024/2024-0540-000'), Decimal(0))
ero_prior = ero_total - ero_current
with (OUT/'target_program_activity_rows.csv').open('w', newline='') as out:
    writer = csv.DictWriter(out, fieldnames=list(selected[0]))
    writer.writeheader()
    writer.writerows(selected)
with (OUT/'target_tas_program_totals.csv').open('w', newline='') as out:
    writer = csv.DictWriter(out, fieldnames=list(groups[0]))
    writer.writeheader()
    writer.writerows(groups)
custody = [r for r in selected if 'CUSTODY' in r['program_activity_name'].upper()]
tas_b = defaultdict(Decimal)
for r in selected:
    tas_b[r['treasury_account_symbol']] += Decimal(r['gross_outlay_amount_FYB_to_period_end'] or '0')
reconcile = []
for r in a:
    if r['treasury_account_symbol'] in tas_b:
        av = Decimal(r['gross_outlay_amount'] or '0')
        bv = tas_b[r['treasury_account_symbol']]
        reconcile.append(dict(tas=r['treasury_account_symbol'], file_a_outlays=str(av), file_b_outlays=str(bv), difference=str(bv-av)))
require(len(reconcile) == len(tas_b) and reconcile, 'missing File A account coverage')
require(all(Decimal(r['difference']) == 0 for r in reconcile), 'File A/B outlay mismatch')
result = dict(zip_sha256=hashlib.sha256(raw).hexdigest(), members=names, file_a_rows=len(a), file_b_rows=len(b), periods=periods, selected_rows=len(selected), custody_rows=len(custody), groups=groups, reconciliation=reconcile, object_classes=sorted(set((r['object_class_code'],r['object_class_name']) for r in selected)))
result['ero_totals'] = dict(all_vintage_outlays=str(ero_total), current_2024_outlays=str(ero_current), prior_vintage_outlays=str(ero_prior), prior_vintage_excluding_known_2020_2024_custody=str(ero_prior-Decimal('276788.05')))
(OUT/'usaspending_probe.json').write_text(json.dumps(result, indent=2)+'\n')
print(json.dumps({k: result[k] for k in ['file_a_rows', 'file_b_rows', 'selected_rows', 'custody_rows', 'ero_totals']}, indent=2))
