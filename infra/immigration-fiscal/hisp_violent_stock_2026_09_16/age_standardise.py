"""Direct age-standardisation of the Hispanic male imprisonment rate, 2010 -> 2022.
Rates: BJS Prisoners in 2010 App. Table 15 (p.27) and Prisoners in 2022 - Statistical Tables, Table 13 (p.24),
sentenced prisoners under state OR federal jurisdiction per 100,000 U.S. residents of the same sex/age/origin.
Populations: ACS 1-year PUMS via Census API tabulate (PWGTP-weighted), males by age band, Hispanic (HISP != 01)
and non-Hispanic white (HISP == 01 and RAC1P == 1)."""
import json, os, pathlib, re, urllib.request
HERE = pathlib.Path(__file__).parent
CACHE = HERE / "pop_cache"; CACHE.mkdir(exist_ok=True)

def key():
    k = os.environ.get("CENSUS_API_KEY")
    if not k:
        k = re.search(r'CENSUS_API_KEY="?([A-Za-z0-9]+)', (HERE.parent / "acquire/config.local.env").read_text()).group(1)
    return k

BANDS = [("18-19",18,19),("20-24",20,24),("25-29",25,29),("30-34",30,34),("35-39",35,39),
         ("40-44",40,44),("45-49",45,49),("50-54",50,54),("55-59",55,59),("60-64",60,64),("65+",65,99)]
# BJS male imprisonment rates per 100k, state+federal, sentence > 1 yr
RATE = {  # band: (white2010, hisp2010, white2022, hisp2022)
 "18-19":(149,563,30,85), "20-24":(638,1908,229,663), "25-29":(980,2707,514,1462),
 "30-34":(1061,2808,732,1774), "35-39":(995,2486,813,1747), "40-44":(916,2146,776,1634),
 "45-49":(788,1901,617,1326), "50-54":(552,1495,512,1023), "55-59":(347,1031,407,849),
 "60-64":(233,679,277,650), "65+":(95,294,106,317)}

def pop(year, lo, hi):
    f = CACHE / f"{year}_{lo}_{hi}.json"
    if not f.exists():
        url = (f"https://api.census.gov/data/{year}/acs/acs1/pums?tabulate=weight(PWGTP)"
               f"&row+RAC1P&col+HISP&SEX=1&AGEP={lo}:{hi}&key={key()}")
        f.write_bytes(urllib.request.urlopen(url).read())
    d = json.loads(f.read_text())
    hdr, rows = d[0], d[1:]
    cols = [c["HISP"] for c in hdr[:-1]]          # column dimension = HISP code
    h = w = 0.0
    for r in rows:
        rac = str(r[-1])
        for i, c in enumerate(cols):
            v = r[i]
            v = float(v) if v not in (None, "") else 0.0
            if c != "01":
                h += v
            elif rac == "1":
                w += v
    return w, h

P = {}
for y in (2010, 2022):
    for b, lo, hi in BANDS:
        P[(y, b)] = pop(y, lo, hi)
        print(f"  pop {y} {b}: NHwhite {P[(y,b)][0]:>12,.0f}  Hispanic {P[(y,b)][1]:>12,.0f}")

def crude(y, idx):
    num = sum(RATE[b][idx] * P[(y, b)][1] for b, _, _ in BANDS)
    den = sum(P[(y, b)][1] for b, _, _ in BANDS)
    return num / den
def crude_w(y, idx):
    num = sum(RATE[b][idx] * P[(y, b)][0] for b, _, _ in BANDS)
    den = sum(P[(y, b)][0] for b, _, _ in BANDS)
    return num / den

h10 = crude(2010, 1); h22 = crude(2022, 3)
std22 = sum(RATE[b][1] * P[(2022, b)][1] for b, _, _ in BANDS) / sum(P[(2022, b)][1] for b, _, _ in BANDS)
w10 = crude_w(2010, 0); w22 = crude_w(2022, 2)
stdw22 = sum(RATE[b][0] * P[(2022, b)][0] for b, _, _ in BANDS) / sum(P[(2022, b)][0] for b, _, _ in BANDS)

print(f"\nHispanic males 18+, imprisonment rate per 100,000 (BJS age-specific rates x ACS age structure)")
print(f"  2010 actual (2010 rates, 2010 ages)              {h10:8.1f}")
print(f"  2022 counterfactual (2010 rates, 2022 ages)      {std22:8.1f}   <- ageing effect only")
print(f"  2022 actual (2022 rates, 2022 ages)              {h22:8.1f}")
print(f"  total change 2010->2022                          {h22-h10:+8.1f}  ({100*(h22/h10-1):+.1f}%)")
print(f"  attributable to age structure                    {std22-h10:+8.1f}  ({100*(std22/h10-1):+.1f}%)")
print(f"  attributable to age-specific rates               {h22-std22:+8.1f}")
print(f"  age share of total change                        {100*(std22-h10)/(h22-h10):8.1f}%")
print(f"\nNon-Hispanic white males 18+, same construction")
print(f"  2010 actual {w10:8.1f}   2022 at 2010 rates {stdw22:8.1f}   2022 actual {w22:8.1f}")
print(f"  age effect {stdw22-w10:+8.1f}  rate effect {w22-stdw22:+8.1f}")
print(f"\nHispanic/white ratio 18+: 2010 {h10/w10:.2f}x -> 2022 {h22/w22:.2f}x")
