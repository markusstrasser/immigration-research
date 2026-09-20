"""Reconcile FY2024 ICE account gross/net outlays to SF133 and Treasury."""
from collections import defaultdict
import csv
from decimal import Decimal
import io
import json
from pathlib import Path
import xml.etree.ElementTree as ET
import zipfile
from acquire import verified_bytes

ROOT = Path(__file__).resolve().parent
CACHE = ROOT/'_cache'
OUT = ROOT/'derived'
OUT.mkdir(exist_ok=True)
with zipfile.ZipFile(io.BytesIO(verified_bytes('dhs_sf133_2024.zip'))) as archive:
    root = ET.fromstring(archive.read('FY2024_XML_SF133_Department_of_Homeland_Security.xml'))
if root.get('fy') != '2024':
    raise ValueError('Wrong fiscal year')
totals = defaultdict(lambda: defaultdict(Decimal))
rows = []
for account in root.iter('treasury-account'):
    code = account.get('treasury-account-code')
    if account.get('cgac-agency-code') != '070' or code not in {'0540', '5126', '5382', '5542'}:
        continue
    amounts = {}
    for line in account.iter('line'):
        september = [m for m in line.findall('month') if m.get('name') == 'Sep']
        if len(september) != 1:
            raise ValueError('Missing or duplicate September observation')
        value = Decimal(september[0].get('amount'))
        amounts[line.get('number')] = value
        totals[code][line.get('number')] += value
    rows.append(dict(account=code, status=account.get('tafs-status'),
                     availability=account.find('period-of-availability').attrib,
                     september={k: str(v) for k, v in amounts.items()}))
if set(totals) != {'0540', '5126', '5382', '5542'}:
    raise ValueError('Missing selected ICE account coverage')
with zipfile.ZipFile(io.BytesIO(verified_bytes('dhs_fy2024_fileab.zip'))) as archive:
    name = next(n for n in archive.namelist() if 'AccountBalances' in n)
    file_a = list(csv.DictReader(io.TextIOWrapper(archive.open(name), encoding='utf-8-sig')))
treasury_net = {'0540': '9583043451.89', '5126': '32192293.30',
                '5382': '155281257.00', '5542': '746838.00'}
checks = []
for code, lines in totals.items():
    if '4190' not in lines or not {'4020', '4110'} & lines.keys():
        raise ValueError(f'Missing gross/net reporting lines for {code}')
    gross = lines['4020'] + lines['4110']
    net = lines['4190']
    a_gross = sum((Decimal(r['gross_outlay_amount'] or '0') for r in file_a
                   if r['agency_identifier_code'] == '070' and r['main_account_code'] == code), Decimal(0))
    if net != Decimal(treasury_net[code]) or gross != a_gross:
        raise ValueError(f'Account {code} failed SF133/Treasury/File A reconciliation')
    checks.append(dict(account=code, gross=str(gross), net=str(net), gross_minus_net=str(gross-net)))
(OUT/'sf133_probe.json').write_text(json.dumps(dict(accounts=rows, checks=checks), indent=2)+'\n')
print(json.dumps(checks, indent=2))
