"""H2: are Mission storefronts less likely to hold an active SF business
registration than storefronts in other commercial districts?

Denominator: SF Commercial Vacancy Tax registry ("Taxable Commercial Spaces",
rzkk-54yv) - every ground-floor commercial space in the city's designated
commercial districts, one row per space per tax year, with a vacancy flag.
Numerator: active Registered Business Locations (g8m3-pdis), matched on
normalised street address.

Measures FORMALITY OF THE STOREFRONT, not tax compliance.
"""
import json, pathlib, re, collections
import numpy as np, pandas as pd
CD = pathlib.Path(__file__).parent/"_cache"; HERE = CD.parent
pd.set_option("display.width", 240, "display.max_columns", 40)

SUF = {"STREET":"ST","ST":"ST","AVENUE":"AVE","AVE":"AVE","AV":"AVE",
 "BOULEVARD":"BLVD","BLVD":"BLVD","ROAD":"RD","RD":"RD","DRIVE":"DR","DR":"DR",
 "PLACE":"PL","PL":"PL","COURT":"CT","CT":"CT","LANE":"LN","LN":"LN",
 "TERRACE":"TER","TER":"TER","WAY":"WAY","CIRCLE":"CIR","CIR":"CIR",
 "HIGHWAY":"HWY","HWY":"HWY","PARKWAY":"PKWY","PKWY":"PKWY","ALLEY":"ALY",
 "PLAZA":"PLZ","SQUARE":"SQ","BUILDING":"BLDG"}
DIRS = {"N":"N","S":"S","E":"E","W":"W","NORTH":"N","SOUTH":"S","EAST":"E","WEST":"W"}

def norm(addr):
    """-> '2344 MISSION ST' or None"""
    if not addr: return None
    a = re.sub(r"[^A-Z0-9 ]", " ", addr.upper())
    a = re.sub(r"\s+", " ", a).strip()
    toks = a.split()
    if not toks: return None
    m = re.match(r"^(\d+)", toks[0])
    if not m: return None
    num = m.group(1)
    rest = toks[1:]
    # drop a leading range piece like '2348' in '2344-2348 MISSION ST'
    if rest and rest[0].isdigit() and len(rest) > 1: rest = rest[1:]
    out = []
    for i, t in enumerate(rest):
        if t in SUF:
            out.append(SUF[t]); break
        if i == 0 and t in DIRS and len(rest) > 1:
            out.append(DIRS[t]); continue
        if t.isdigit() and out:        # suite number before any suffix
            break
        out.append(t)
    else:
        out = [t for t in out if not t.isdigit()]
    if not out: return None
    return f"{num} " + " ".join(out)

# ---- storefronts, tax year 2024 (most complete) ----
sf = json.load(open(CD/"sf_taxable_commercial_spaces.json"))
Y = "2024"
store = [r for r in sf if r.get("taxyear") == Y]
seen = set(); rows = []
for r in store:
    k = r.get("lin") or (r.get("parcelnumber","") + "|" + (r.get("linaddress") or ""))
    if k in seen: continue
    seen.add(k)
    rows.append(dict(lin=k, addr=norm(r.get("linaddress") or r.get("parcelsitusaddress")),
                     nbhd=r.get("analysis_neighborhood"),
                     vacant=(r.get("vacant") == "YES"),
                     filed=(r.get("filed") == "YES"),
                     lat=float(r["latitude"]) if r.get("latitude") else None,
                     lon=float(r["longitude"]) if r.get("longitude") else None))
S = pd.DataFrame(rows)
print(f"tax year {Y}: {len(S)} distinct taxable commercial spaces; "
      f"{S.addr.isna().sum()} unparseable addresses; "
      f"vacant {100*S.vacant.mean():.1f}%; filed {100*S.filed.mean():.1f}%")

# ---- active registered businesses ----
biz = json.load(open(CD/"sf_active_businesses.json"))
baddr = collections.Counter()
for b in biz:
    a = norm(b.get("full_business_address"))
    if a: baddr[a] += 1
print(f"active registered business locations: {len(biz)}; distinct normalised addresses: {len(baddr)}")

S["n_biz_at_addr"] = S.addr.map(lambda a: baddr.get(a, 0) if a else 0)
S["registered"] = (S.n_biz_at_addr > 0).astype(int)
occ = S[(~S.vacant) & S.addr.notna()].copy()
print(f"occupied storefronts with a parseable address: {len(occ)}; "
      f"citywide registration rate {100*occ.registered.mean():.1f}%")

# ---- by neighborhood ----
T = occ.groupby("nbhd").agg(storefronts=("registered","size"),
                            reg_rate=("registered","mean"),
                            biz_per_storefront=("n_biz_at_addr","mean"))
V = S.groupby("nbhd").agg(all_spaces=("vacant","size"), vacancy_rate=("vacant","mean"),
                          filing_rate=("filed","mean"))
T = T.join(V)
acs = pd.DataFrame(json.load(open(CD/"sf_nbhd_acs.json"))).set_index("nbhd")
T = T.join(acs[["mean_hh_inc","hisp_pct","mex_pct","nhasian_pct","fb_pct","pov_pct"]])
T = T[T.storefronts >= 30].sort_values("reg_rate")
T["reg_rate"] *= 100; T["vacancy_rate"] *= 100; T["filing_rate"] *= 100
print("\n=== TABLE 6. Storefront registration rate by SF analysis neighborhood "
      f"(vacancy-tax registry {Y}, occupied spaces only) ===")
print(T.round(1).to_string())
T.round(3).to_csv(HERE/"table6_sf_storefront_registration.csv")

# ---- corridor level ----
CORRIDORS = {   # name: (south, west, north, east)
 "Mission St (14th-Cesar Chavez)":   (37.7480, -122.4235, 37.7692, -122.4155),
 "24th St (Mission-Potrero)":        (37.7508, -122.4205, 37.7543, -122.4055),
 "Valencia St (14th-Cesar Chavez)":  (37.7475, -122.4245, 37.7692, -122.4185),
 "Grant Ave (Chinatown)":            (37.7895, -122.4080, 37.7990, -122.4035),
 "Stockton St (Chinatown)":          (37.7915, -122.4105, 37.7990, -122.4062),
 "Columbus Ave (North Beach)":       (37.7972, -122.4165, 37.8062, -122.4055),
 "Post St (Japantown)":              (37.7838, -122.4350, 37.7866, -122.4275),
 "Clement St (Inner Richmond)":      (37.7812, -122.4735, 37.7845, -122.4565),
 "Irving St (Inner Sunset)":         (37.7620, -122.4725, 37.7652, -122.4595),
 "Chestnut St (Marina)":             (37.7992, -122.4465, 37.8018, -122.4340),
 "Geary Blvd (Richmond)":            (37.7798, -122.4760, 37.7828, -122.4560),
 "Castro St (Castro)":               (37.7580, -122.4370, 37.7640, -122.4320),
 "24th St (Noe Valley)":             (37.7495, -122.4380, 37.7530, -122.4260),
 "Fillmore St (Pac Hts/Lower)":      (37.7830, -122.4370, 37.7960, -122.4310),
}
def inbox(lat, lon, b):
    return lat is not None and lon is not None and b[0] <= lat <= b[2] and b[1] <= lon <= b[3]

blatlon = []
for b in biz:
    loc = b.get("location") or {}
    c = loc.get("coordinates")
    if c: blatlon.append((c[1], c[0], norm(b.get("full_business_address"))))
crows = []
for name, bb in CORRIDORS.items():
    sub = S[[inbox(r.lat, r.lon, bb) for r in S.itertuples()]]
    o = sub[(~sub.vacant) & sub.addr.notna()]
    nb = sum(1 for la, lo, _ in blatlon if inbox(la, lo, bb))
    crows.append(dict(corridor=name, storefronts_total=len(sub),
        vacancy_pct=100*sub.vacant.mean() if len(sub) else np.nan,
        filing_pct=100*sub.filed.mean() if len(sub) else np.nan,
        occupied=len(o),
        registration_pct=100*o.registered.mean() if len(o) else np.nan,
        active_biz_in_box=nb,
        biz_per_occupied_storefront=nb/len(o) if len(o) else np.nan))
CX = pd.DataFrame(crows).sort_values("registration_pct")
print("\n=== TABLE 7. Commercial corridors: storefronts, vacancy, registration ===")
print(CX.round(1).to_string(index=False))
CX.round(3).to_csv(HERE/"table7_sf_corridor_registration.csv", index=False)
