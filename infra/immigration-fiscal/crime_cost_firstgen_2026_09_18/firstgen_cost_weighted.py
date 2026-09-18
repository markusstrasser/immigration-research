"""Cost-weighted felony arrest rates by immigration status, Texas 2012–2018.

Counts: Light, He & Robey, PNAS 2020 (doi:10.1073/pnas.2014704117) replication package,
openICPSR 124923: detailed_category.dta (CMS undocumented denominators, 2012–18),
detailed_category_pew.dta (Pew denominators, 2012–17), detailed_category_nat.dta (legal
immigrants split into non-naturalized and naturalized, CMS denominators).  Each row is an arrest
CHARGE, not a person or a conviction.  "citizen" = US-born.  "legal_immigrant" = foreign-born
minus the undocumented estimate, naturalized included.  "foreign_born" pools undocumented and
legal (robust to the undocumented/legal boundary, which rests on DHS IDENT matching).
Unit costs: McCollister, French & Fang 2010 Tables 3–5 (2008$), the MCC table copied from
../crime_cost_2026_09_16/crime_cost.py; CPI-U 2008→2024 factor 1.45697 from that script's gate.
Age shares: ACS 1-year PUMS API tabulations for Texas (CIT × AGEP) in _cache/tx_age_by_cit_raw.txt.
"""
import json, re
from pathlib import Path
import pandas as pd

HERE = Path(__file__).resolve().parent
CACHE = HERE / "_cache" / "light_texas"
OUT = HERE / "derived"; OUT.mkdir(exist_ok=True)
INFL = 1.45697
MCC = {  # (victim, cjs, career, intangible, published_total) 2008$
    "murder":   (737_517, 392_352, 148_555, 8_442_000, 8_982_907),
    "sexual":   (  5_556,  26_479,   9_212,   199_642,   240_776),
    "assault":  (  8_700,   8_641,   2_126,    95_023,   107_020),
    "robbery":  (  3_299,  13_827,   4_272,    22_575,    42_310),
    "arson":    ( 11_452,   4_392,     584,     5_133,    21_103),
    "burglary": (  1_362,   4_127,     681,       321,     6_462),
    "larceny":  (    480,   2_879,     163,        10,     3_532),
}
UNIT = {o: {"cjs": c * INFL, "tangible": (v + c + k) * INFL, "total": t * INFL}
        for o, (v, c, k, i, t) in MCC.items()}
ZERO = {"cjs": 0.0, "tangible": 0.0, "total": 0.0}
MAP_A = {"homicide": "murder", "sexual_assault": "sexual", "assault": "assault", "robbery": "robbery",
         "burglary": "burglary", "theft": "larceny", "Arson": "arson"}
MAP_B = dict(MAP_A, **{"sexual offsenses": "sexual", "kidnapping": "assault"})
VIOLENT4 = ["homicide", "assault", "robbery", "sexual_assault"]

def load(f):
    d = pd.read_stata(CACHE / f)
    d["category"] = d["category"].astype("string").fillna("NA")
    return d

def age_shares():
    txt = (HERE / "_cache" / "tx_age_by_cit_raw.txt").read_text()
    sh = {}
    for y, band, js in re.findall(r"year=(\d+) AGEP=(\S+)\n(\[\[.*?\]\])", txt, re.S):
        rows = json.loads(js)
        sh[(int(y), band)] = dict(zip([list(c.values())[0] for c in rows[0]], rows[1]))
    return sh

def share(sh, year, bands, cits):
    tot = sum(sh[(year, b)][c] for b in ["0:17", "18:99"] for c in cits)
    return sum(sh[(year, b)][c] for b in bands for c in cits) / tot, tot

def factors(sh, year, pop_undoc_y, bands):
    """ratio_per_band = ratio_per_capita * factor, factor = band share of US-born / band share of group."""
    usb, _ = share(sh, year, bands, "123")
    nonc, nonc_tot = share(sh, year, bands, "5")          # undocumented proxied by all non-citizens
    nat, _ = share(sh, year, bands, "4")
    fb, fb_tot = share(sh, year, bands, "45")
    legal = (fb * fb_tot - nonc * pop_undoc_y) / (fb_tot - pop_undoc_y)
    legal_nc = (nonc * nonc_tot - nonc * pop_undoc_y) / (nonc_tot - pop_undoc_y)
    g = {"citizen": 1.0, "undocumented": usb / nonc, "legal_immigrant": usb / legal, "foreign_born": usb / fb,
         "naturalized": usb / nat, "legal_noncitizen": usb / legal_nc}
    return g, {"usborn": usb, "noncitizen": nonc, "naturalized": nat, "foreign_born": fb, "legal": legal, "legal_noncitizen": legal_nc}

def rates(d, spec):
    pop = d.groupby("year")[sorted({p for ps in spec.values() for p in ps[1]})].first().sum()
    ch = d.groupby("category")[sorted({c for cs in spec.values() for c in cs[0]})].sum()
    r = pd.DataFrame(index=ch.index)
    for s, (cs, ps) in spec.items():
        r[s] = ch[cs].sum(axis=1) / pop[ps].sum() * 1e5
    return r

def run(f, label, spec, sh, year):
    d = load(f); r = rates(d, spec)
    pu = d[d.year == year]["pop_undoc"].iloc[0]
    fac, shares = factors(sh, year, pu, ["18:99"]); fac39, _ = factors(sh, year, pu, ["18:39"])
    rows = []
    def add(arm, cost, s, val, base, hom=float("nan")):
        rows.append({"denominator": label, "arm": arm, "cost": cost, "status": s,
                     "usd_per_person_year": val / 1e5 if arm != "counts" else float("nan"),
                     "per_100k": val, "ratio_per_capita": val / base,
                     "ratio_per_adult": val / base * fac[s], "ratio_per_18_39": val / base * fac39[s],
                     "homicide_share_of_cost": hom})
    for arm, mp in [("A", MAP_A), ("B", MAP_B)]:
        for cost in ["cjs", "tangible", "total"]:
            per = {s: sum(r.loc[o, s] * UNIT.get(mp.get(o), ZERO)[cost] for o in r.index) for s in spec}
            for s in spec:
                add(arm, cost, s, per[s], per["citizen"], r.loc["homicide", s] * UNIT["murder"][cost] / per[s])
    tot = r.sum(); v4 = r.loc[VIOLENT4].sum()
    for s in spec:
        add("counts", "all_felonies", s, tot[s], tot["citizen"]); add("counts", "violent4", s, v4[s], v4["citizen"])
        add("counts", "homicide", s, r.loc["homicide", s], r.loc["homicide", "citizen"])
        add("counts", "sexual_assault", s, r.loc["sexual_assault", s], r.loc["sexual_assault", "citizen"])
    r_out = r.add_suffix("_per100k")
    for s in spec:
        r_out[f"{s}_ratio"] = r[s] / r["citizen"]
    r_out.round(4).to_csv(OUT / f"rates_by_status_offence_{label}.csv")
    return pd.DataFrame(rows), {"factor_adult": fac, "factor_18_39": fac39, "shares_adult": shares}

BASE = {"citizen": (["citizen_charge"], ["tot_citizen"]),
        "legal_immigrant": (["immigrants_charge"], ["tot_legal2_immi"]),
        "undocumented": (["undocumented_immigrants_charge"], ["pop_undoc"]),
        "foreign_born": (["immigrants_charge", "undocumented_immigrants_charge"], ["tot_legal2_immi", "pop_undoc"])}
SPLIT = {"citizen": (["citizen_charge"], ["tot_citizen"]),
         "legal_noncitizen": (["immigrants_charge"], ["tot_legal2_immi"]),
         "naturalized": (["naturalized_charge"], ["naturalized_citizen"]),
         "undocumented": (["undocumented_immigrants_charge"], ["pop_undoc"])}

if __name__ == "__main__":
    sh = age_shares()
    a, ma = run("detailed_category.dta", "cms", BASE, sh, 2018)
    b, mb = run("detailed_category_pew.dta", "pew", BASE, sh, 2015)
    c, mc = run("detailed_category_nat.dta", "cms_split", SPLIT, sh, 2018)
    res = pd.concat([a, b, c]); res.round(5).to_csv(OUT / "firstgen_cost_weighted.csv", index=False)
    json.dump({"cms": ma, "pew": mb, "cms_split": mc, "infl_2008_24": INFL}, open(OUT / "audit.json", "w"), indent=1)
    pd.set_option("display.width", 250); pd.set_option("display.float_format", lambda v: f"{v:,.3f}")
    print("[age factors, adult]", {k: round(v, 3) for k, v in ma["factor_adult"].items()}, {k: round(v, 3) for k, v in mc["factor_adult"].items()})
    cols = ["denominator", "arm", "cost", "status", "usd_per_person_year", "ratio_per_capita", "ratio_per_adult", "ratio_per_18_39", "homicide_share_of_cost"]
    sel = res[(res.status != "citizen") & (res.arm.isin(["A", "counts"]))]
    print(sel[cols].to_string(index=False))
    print(res[(res.status == "citizen") & (res.arm == "A")][["denominator", "cost", "usd_per_person_year", "homicide_share_of_cost"]].to_string(index=False))
