"""Pull Statistics Denmark STRAFNA3/4/9 + FOLK1C/1E for the Pueyo-thread Denmark repro."""
import requests, json, io, os, sys, time
import pandas as pd

OUT = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(OUT, 'raw'); BOD = os.path.join(OUT, 'bodies')
os.makedirs(RAW, exist_ok=True); os.makedirs(BOD, exist_ok=True)
S = requests.Session(); S.headers.update({'User-Agent': 'research-agent/1.0'})
YEARS = [str(y) for y in range(2008, 2025)]
BODIES = {}

def dst(name, body, tries=3):
    BODIES[name] = body
    for i in range(tries):
        r = S.post('https://api.statbank.dk/v1/data', json=body, timeout=600)
        if r.status_code == 200:
            df = pd.read_csv(io.StringIO(r.text), sep=';')
            print(f"  ✓ {name}: {len(df)} rows")
            return df
        print(f"  ! {name} HTTP {r.status_code}: {r.text[:200]}")
        time.sleep(3)
    raise SystemExit(f"FAILED {name}")

print("[STRAFNA4 offence x origin x year]")
parts = [dst(f'strafna4_{y}', {"table": "STRAFNA4", "format": "CSV", "lang": "en", "variables": [
    {"code": "OVERTRÆD", "values": ["*"]}, {"code": "IELAND", "values": ["*"]},
    {"code": "Tid", "values": [y]}]}) for y in YEARS]
s4 = pd.concat(parts, ignore_index=True); s4.to_csv(f'{RAW}/strafna4_offence_origin_2008_2024.csv', index=False)

print("[STRAFNA3 sex x age x origin x year]")
s3 = dst('strafna3', {"table": "STRAFNA3", "format": "CSV", "lang": "en", "variables": [
    {"code": "KOEN", "values": ["M", "K"]}, {"code": "ALDER", "values": ["TOT", "15-29", "30-49", "50-79"]},
    {"code": "IELAND", "values": ["*"]}, {"code": "Tid", "values": YEARS}]})
s3.to_csv(f'{RAW}/strafna3_sex_age_origin_2008_2024.csv', index=False)

print("[STRAFNA9 sex x age x ancestry x year]")
s9 = dst('strafna9', {"table": "STRAFNA9", "format": "CSV", "lang": "en", "variables": [
    {"code": "KOEN", "values": ["M", "K"]}, {"code": "ALDER", "values": ["TOT", "15-29", "30-49", "50-79"]},
    {"code": "HERKOMST", "values": ["*"]}, {"code": "Tid", "values": YEARS}]})
s9.to_csv(f'{RAW}/strafna9_sex_age_ancestry_2008_2024.csv', index=False)

AGES = ['15-19', '20-24', '25-29', '30-34', '35-39', '40-44', '45-49',
        '50-54', '55-59', '60-64', '65-69', '70-74', '75-79']
print("[FOLK1C population by origin x sex x age (Q1)]")
pp = []
for y in YEARS:
    pp.append(dst(f'folk1c_{y}', {"table": "FOLK1C", "format": "CSV", "lang": "en", "variables": [
        {"code": "OMRÅDE", "values": ["000"]}, {"code": "KØN", "values": ["TOT", "1", "2"]},
        {"code": "ALDER", "values": AGES}, {"code": "HERKOMST", "values": ["TOT"]},
        {"code": "IELAND", "values": ["*"]}, {"code": "Tid", "values": [y + "K1"]}]}))
pop = pd.concat(pp, ignore_index=True); pop.to_csv(f'{RAW}/folk1c_pop_origin_sex_age_2008_2024.csv', index=False)

print("[FOLK1E verification]")
f1e = dst('folk1e_2024', {"table": "FOLK1E", "format": "CSV", "lang": "en", "variables": [
    {"code": "OMRÅDE", "values": ["000"]}, {"code": "KØN", "values": ["TOT"]},
    {"code": "ALDER", "values": [str(a) for a in range(15, 80)]},
    {"code": "HERKOMST", "values": ["TOT"]}, {"code": "Tid", "values": ["2024K1"]}]})
f1e.to_csv(f'{RAW}/folk1e_2024q1_age15_79.csv', index=False)

json.dump(BODIES, open(f'{BOD}/api_request_bodies.json', 'w'), ensure_ascii=False, indent=1)
print("✓ all pulls done")
