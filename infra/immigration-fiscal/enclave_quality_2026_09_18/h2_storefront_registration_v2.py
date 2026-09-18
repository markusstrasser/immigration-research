"""H2, corrected. Are Mission storefronts less likely to have an active business
registration than storefronts elsewhere in San Francisco?

CORRECTION TO THE FIRST PASS. The vacancy-tax registry's `lin` (Location
Identification Number) is derived from the business tax account number (`ban`):
`lin` = "<ban>-NN-NNN". Conditioning the denominator on having a `lin` therefore
conditions on a business account already existing, which makes the registration
rate circular. Only 4,439 of the 7,160 tax-year-2024 rows have a `lin` at all.

This version uses the PARCEL universe instead: every distinct
`parcelnumber` + `parcelsitusaddress` in tax year 2024, whether or not a LIN was
ever assigned. Situs addresses are often ranges ("369-373 WEST PORTAL AV"), so
the match accepts any active registered business whose house number falls inside
the range on the same street.

Reported alongside: the `filed` flag, i.e. whether the owner filed the required
Commercial Vacancy Tax return. That is a landlord-side compliance measure and is
not circular.
"""
import json, pathlib, re, collections
import numpy as np, pandas as pd

HERE = pathlib.Path(__file__).parent; CD = HERE/"_cache"
pd.set_option("display.width", 240, "display.max_columns", 40)

SUF = {"STREET":"ST","ST":"ST","AVENUE":"AVE","AVE":"AVE","AV":"AVE",
 "BOULEVARD":"BLVD","BLVD":"BLVD","BL":"BLVD","ROAD":"RD","RD":"RD","DRIVE":"DR",
 "DR":"DR","PLACE":"PL","PL":"PL","COURT":"CT","CT":"CT","LANE":"LN","LN":"LN",
 "TERRACE":"TER","TER":"TER","TR":"TER","WAY":"WAY","WY":"WAY","CIRCLE":"CIR",
 "CIR":"CIR","HIGHWAY":"HWY","HWY":"HWY","HY":"HWY","PARKWAY":"PKWY","PKWY":"PKWY",
 "PY":"PKWY","ALLEY":"ALY","ALY":"ALY","PLAZA":"PLZ","PZ":"PLZ","SQUARE":"SQ",
 "SQ":"SQ","ROW":"ROW","PARK":"PARK","LOOP":"LOOP","LOP":"LOOP","LN.":"LN"}
DIRS = {"N":"N","S":"S","E":"E","W":"W","NORTH":"N","SOUTH":"S","EAST":"E","WEST":"W"}


def parse_range(addr):
    """'369-373 WEST PORTAL AV' -> (369, 373, 'WEST PORTAL AVE')."""
    if not addr:
        return None
    a = addr.upper().replace("&", " AND ")
    m = re.match(r"^\s*(\d+)\s*(?:-|–|\s+TO\s+|\s+AND\s+)\s*(\d+)\s+(.*)$", a)
    if m:
        lo, hi, rest = int(m.group(1)), int(m.group(2)), m.group(3)
    else:
        m = re.match(r"^\s*(\d+)\s+(.*)$", a)
        if not m:
            return None
        lo = hi = int(m.group(1)); rest = m.group(2)
    st = street_key(rest)
    if not st:
        return None
    if hi < lo:
        hi = lo
    return lo, hi, st


def street_key(rest):
    rest = re.sub(r"[^A-Z0-9 ]", " ", rest.upper())
    toks = [t for t in rest.split() if t]
    out = []
    for i, t in enumerate(toks):
        if t in SUF:
            out.append(SUF[t]); break
        if i == 0 and t in DIRS and len(toks) > 1:
            out.append(DIRS[t]); continue
        if t.isdigit() and out:
            break
        if re.fullmatch(r"(STE|SUITE|UNIT|APT|FL|FLOOR|RM|#)", t):
            break
        out.append(t)
    else:
        out = [t for t in out if not t.isdigit()] or out
    return " ".join(out) if out else None


def parse_point(addr):
    r = parse_range(addr)
    return None if r is None else (r[0], r[2])


# ---------------- active registered businesses ----------------
biz = json.load(open(CD/"sf_active_businesses.json"))
by_street = collections.defaultdict(list)
for b in biz:
    p = parse_point(b.get("full_business_address"))
    if p:
        by_street[p[1]].append(p[0])
for s in by_street:
    by_street[s].sort()
print(f"active registered business locations: {len(biz)}; "
      f"parsed onto {len(by_street)} streets")

import bisect
def any_biz(lo, hi, st, pad=0):
    ns = by_street.get(st)
    if not ns:
        return False
    i = bisect.bisect_left(ns, lo - pad)
    return i < len(ns) and ns[i] <= hi + pad


# ---------------- parcel universe ----------------
sf = [r for r in json.load(open(CD/"sf_taxable_commercial_spaces.json"))
      if r.get("taxyear") == "2024"]
seen = set(); rows = []
for r in sf:
    addr = r.get("parcelsitusaddress")
    key = (r.get("parcelnumber"), (addr or "").strip().upper())
    if key in seen:
        continue
    seen.add(key)
    pr = parse_range(addr)
    rows.append(dict(parcel=r.get("parcelnumber"), addr=addr,
                     lo=pr[0] if pr else None, hi=pr[1] if pr else None,
                     st=pr[2] if pr else None,
                     nbhd=r.get("analysis_neighborhood"),
                     vacant=r.get("vacant") == "YES",
                     filed=r.get("filed") == "YES",
                     has_lin=bool(r.get("lin")),
                     lat=float(r["latitude"]) if r.get("latitude") else None,
                     lon=float(r["longitude"]) if r.get("longitude") else None))
S = pd.DataFrame(rows)
print(f"tax year 2024: {len(S)} distinct parcel-address commercial spaces; "
      f"{S.st.isna().sum()} unparseable; vacant {100*S.vacant.mean():.1f}%; "
      f"owner filed {100*S.filed.mean():.1f}%; has a LIN {100*S.has_lin.mean():.1f}%")

P = S[S.st.notna() & (~S.vacant)].copy()
P["reg"] = [any_biz(r.lo, r.hi, r.st, 0) for r in P.itertuples()]
P["reg_pad4"] = [any_biz(r.lo, r.hi, r.st, 4) for r in P.itertuples()]
print(f"occupied parcels with a parseable address: {len(P)}; "
      f"citywide registration {100*P.reg.mean():.1f}% "
      f"(+/-4 house numbers: {100*P.reg_pad4.mean():.1f}%)")

print("\n--- circularity check: registration rate by whether a LIN exists ---")
print(P.groupby("has_lin").agg(n=("reg","size"), reg_pct=("reg","mean"),
                               filed_pct=("filed","mean")).round(3).to_string())

acs = pd.DataFrame(json.load(open(CD/"sf_nbhd_acs.json"))).set_index("nbhd")
T = P.groupby("nbhd").agg(storefronts=("reg","size"), reg_pct=("reg","mean"),
                          reg_pad4_pct=("reg_pad4","mean"))
V = S.groupby("nbhd").agg(all_spaces=("vacant","size"), vacancy_pct=("vacant","mean"),
                          filing_pct=("filed","mean"))
T = T.join(V).join(acs[["mean_hh_inc","hisp_pct","mex_pct","nhasian_pct","fb_pct","pov_pct"]])
for c in ["reg_pct","reg_pad4_pct","vacancy_pct","filing_pct"]:
    T[c] = 100*T[c]
T = T[T.storefronts >= 30].sort_values("reg_pct")
print("\n=== TABLE 6 (v2). Registration rate by SF analysis neighborhood, "
      "parcel universe, tax year 2024 ===")
print(T.round(1).to_string())
T.round(3).to_csv(HERE/"table6v2_sf_storefront_registration.csv")

CORRIDORS = {
 "Mission St (14th-Cesar Chavez)":   (37.7480, -122.4235, 37.7692, -122.4155),
 "24th St (Mission-Potrero)":        (37.7508, -122.4205, 37.7543, -122.4055),
 "Valencia St (14th-Cesar Chavez)":  (37.7475, -122.4245, 37.7692, -122.4185),
 "Grant Ave (Chinatown)":            (37.7895, -122.4080, 37.7990, -122.4035),
 "Stockton St (Chinatown)":          (37.7915, -122.4105, 37.7990, -122.4062),
 "Columbus Ave (North Beach)":       (37.7972, -122.4165, 37.8062, -122.4055),
 "Post St (Japantown)":              (37.7838, -122.4350, 37.7866, -122.4275),
 "Clement St (Inner Richmond)":      (37.7812, -122.4735, 37.7845, -122.4565),
 "Irving St (Inner Sunset)":         (37.7620, -122.4725, 37.7652, -122.4595),
 "Geary Blvd (Richmond)":            (37.7798, -122.4760, 37.7828, -122.4560),
 "Castro St (Castro)":               (37.7580, -122.4370, 37.7640, -122.4320),
 "24th St (Noe Valley)":             (37.7495, -122.4380, 37.7530, -122.4260),
 "Fillmore St (Pac Hts/Lower)":      (37.7830, -122.4370, 37.7960, -122.4310),
 "Chestnut St (Marina)":             (37.7992, -122.4465, 37.8018, -122.4340),
 "Union St (Cow Hollow)":            (37.7970, -122.4440, 37.7990, -122.4270),
 "Polk St (Russian Hill/Nob Hill)":  (37.7860, -122.4230, 37.7990, -122.4180),
 "Haight St (Haight Ashbury)":       (37.7690, -122.4560, 37.7720, -122.4370),
 "Ocean Ave (Ingleside)":            (37.7230, -122.4700, 37.7260, -122.4500),
 "Mission St (Excelsior, Onondaga-Geneva)": (37.7150, -122.4450, 37.7260, -122.4330),
}
def inbox(lat, lon, b):
    return (lat is not None and lon is not None and b[0] <= lat <= b[2]
            and b[1] <= lon <= b[3])
crows = []
for name, bb in CORRIDORS.items():
    sub = S[[inbox(r.lat, r.lon, bb) for r in S.itertuples()]]
    occ = sub[sub.st.notna() & (~sub.vacant)].copy()
    if len(occ) == 0:
        continue
    occ["reg"] = [any_biz(r.lo, r.hi, r.st, 0) for r in occ.itertuples()]
    crows.append(dict(corridor=name, spaces=len(sub),
                      vacancy_pct=100*sub.vacant.mean(),
                      filing_pct=100*sub.filed.mean(),
                      occupied=len(occ), registration_pct=100*occ.reg.mean()))
CX = pd.DataFrame(crows).sort_values("registration_pct")
print("\n=== TABLE 7 (v2). Commercial corridors ===")
print(CX.round(1).to_string(index=False))
CX.round(3).to_csv(HERE/"table7v2_sf_corridor_registration.csv", index=False)
