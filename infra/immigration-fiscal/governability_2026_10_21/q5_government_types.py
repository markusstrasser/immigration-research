"""Q5: fiscal balance and growth under immigration-restricting vs economic-populist governments (descriptive).

Data: IMF World Economic Outlook via the DataMapper API (imf.org/external/datamapper/api/v1/<indicator>),
GGXCNL_NGDP (general-government net lending/borrowing, % of GDP) and NGDP_RPCH (real GDP growth, %).
Downloaded 2026-10-21; the API serves the latest WEO vintage. Years after LAST_YEAR are projections and are
excluded. Tenure years are calendar years mostly in office; peers are unweighted means of named countries.
Case list and peer groups fixed in RESULT.md "Pre-registration" (2026-10-21 15:10 JST), peers named here.

Output: derived/q5_government_types.csv
"""
import csv
import json
import pathlib
import urllib.request

LANE = pathlib.Path(__file__).resolve().parent
CACHE = LANE / "_cache"
DERIVED = LANE / "derived"
API = "https://www.imf.org/external/datamapper/api/v1/"
FILES = {"GGXCNL_NGDP": "imf_ggxcnl.json", "NGDP_RPCH": "imf_ngdp_rpch.json"}
LAST_YEAR = 2025
PRE_YEARS = 5
CEE = ["CZE", "SVK", "ROU", "BGR", "HRV", "SVN", "LTU", "LVA", "EST"]
EA_SOUTH = ["ESP", "PRT", "IRL"]
LATAM = ["BRA", "CHL", "COL", "PER", "URY", "MEX", "ARG"]
# (type, label, country, first tenure year, last tenure year, peers)
CASES = [
    ("immigration-restricting", "Meloni (Italy)", "ITA", 2023, 2025, ["DEU", "FRA", "ESP"]),
    ("immigration-restricting", "PiS (Poland)", "POL", 2016, 2023, CEE),
    ("immigration-restricting", "Fidesz (Hungary)", "HUN", 2011, 2025, CEE),
    ("immigration-restricting", "Trump I (US)", "USA", 2017, 2020, ["CAN", "GBR", "DEU", "FRA", "JPN", "ITA"]),
    ("immigration-restricting", "Trump I pre-COVID (US)", "USA", 2017, 2019, ["CAN", "GBR", "DEU", "FRA", "JPN", "ITA"]),
    ("economic-populist", "Kirchners (Argentina)", "ARG", 2003, 2015, LATAM),
    ("economic-populist", "Chavez/Maduro (Venezuela)", "VEN", 1999, 2025, LATAM),
    ("economic-populist", "Syriza (Greece)", "GRC", 2015, 2019, EA_SOUTH + ["ITA"]),
    ("economic-populist", "AMLO (Mexico)", "MEX", 2019, 2024, LATAM),
    ("economic-populist", "Morales (Bolivia)", "BOL", 2006, 2019, LATAM),
    ("economic-populist", "Correa (Ecuador)", "ECU", 2007, 2017, LATAM),
]


def load(ind):
    path = CACHE / FILES[ind]
    if not path.exists():
        CACHE.mkdir(exist_ok=True)
        urllib.request.urlretrieve(API + ind, path)
    v = json.load(open(path))["values"][ind]
    return {c: {int(y): x for y, x in s.items() if int(y) <= LAST_YEAR} for c, s in v.items()}


def mean(xs):
    xs = [x for x in xs if x is not None]
    return sum(xs) / len(xs) if xs else None


def avg(series, c, y0, y1):
    return mean([series.get(c, {}).get(y) for y in range(y0, y1 + 1)])


def peer_avg(series, peers, own, y0, y1):
    return mean([avg(series, p, y0, y1) for p in peers if p != own])


def f(x):
    return "" if x is None else f"{x:.2f}"


def main():
    bal, gro = load("GGXCNL_NGDP"), load("NGDP_RPCH")
    rows = []
    for typ, label, c, y0, y1, peers in CASES:
        p0, p1 = y0 - PRE_YEARS, y0 - 1
        r = dict(type=typ, case=label, country=c, tenure=f"{y0}-{y1}", pre=f"{p0}-{p1}",
                 balance_tenure=avg(bal, c, y0, y1), balance_pre=avg(bal, c, p0, p1),
                 peer_balance_tenure=peer_avg(bal, peers, c, y0, y1), peer_balance_pre=peer_avg(bal, peers, c, p0, p1),
                 growth_tenure=avg(gro, c, y0, y1), growth_pre=avg(gro, c, p0, p1),
                 peer_growth_tenure=peer_avg(gro, peers, c, y0, y1), peer_growth_pre=peer_avg(gro, peers, c, p0, p1),
                 peers=" ".join(p for p in peers if p != c))
        for k in ("balance", "growth"):
            vals = [r[f"{k}_tenure"], r[f"{k}_pre"], r[f"peer_{k}_tenure"], r[f"peer_{k}_pre"]]
            r[f"{k}_did"] = None if None in vals else (vals[0] - vals[2]) - (vals[1] - vals[3])
        rows.append(r)
    keys = list(rows[0].keys())
    DERIVED.mkdir(exist_ok=True)
    with open(DERIVED / "q5_government_types.csv", "w", newline="") as fh:
        w = csv.writer(fh, lineterminator="\n")
        w.writerow(keys)
        for r in rows:
            w.writerow([f(r[k]) if isinstance(r[k], float) or r[k] is None else r[k] for k in keys])
            print(r["case"], r["tenure"], "bal", f(r["balance_tenure"]), "pre", f(r["balance_pre"]), "did", f(r["balance_did"]),
                  "| gro", f(r["growth_tenure"]), "peer", f(r["peer_growth_tenure"]), "did", f(r["growth_did"]))


if __name__ == "__main__":
    main()
