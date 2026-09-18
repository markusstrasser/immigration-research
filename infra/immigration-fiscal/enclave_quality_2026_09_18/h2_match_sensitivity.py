"""How much of the 'unregistered' storefront residual is address-matching failure?
Three progressively looser matches, plus a hand-inspectable sample of Mission misses."""
import json, pathlib, re, collections, random
import pandas as pd
CD = pathlib.Path(__file__).parent/"_cache"; HERE = CD.parent
pd.set_option("display.width", 220)

SUF = {"STREET":"ST","ST":"ST","AVENUE":"AVE","AVE":"AVE","AV":"AVE","BOULEVARD":"BLVD",
 "BLVD":"BLVD","ROAD":"RD","RD":"RD","DRIVE":"DR","DR":"DR","PLACE":"PL","PL":"PL",
 "COURT":"CT","CT":"CT","LANE":"LN","LN":"LN","TERRACE":"TER","TER":"TER","WAY":"WAY",
 "CIRCLE":"CIR","CIR":"CIR","HIGHWAY":"HWY","HWY":"HWY","PARKWAY":"PKWY","PKWY":"PKWY",
 "ALLEY":"ALY","PLAZA":"PLZ","SQUARE":"SQ"}
DIRS = {"N":"N","S":"S","E":"E","W":"W","NORTH":"N","SOUTH":"S","EAST":"E","WEST":"W"}

def parse(addr):
    if not addr: return None, None
    a = re.sub(r"[^A-Z0-9 ]", " ", addr.upper()); a = re.sub(r"\s+", " ", a).strip()
    t = a.split()
    if not t: return None, None
    m = re.match(r"^(\d+)", t[0])
    if not m: return None, None
    num = int(m.group(1)); rest = t[1:]
    if rest and rest[0].isdigit() and len(rest) > 1: rest = rest[1:]
    out = []
    for i, tok in enumerate(rest):
        if tok in SUF: out.append(SUF[tok]); break
        if i == 0 and tok in DIRS and len(rest) > 1: out.append(DIRS[tok]); continue
        if tok.isdigit() and out: break
        out.append(tok)
    else:
        out = [x for x in out if not x.isdigit()]
    if not out: return num, None
    return num, " ".join(out)

biz = json.load(open(CD/"sf_active_businesses.json"))
exact, street_nums, streets = set(), collections.defaultdict(set), collections.Counter()
for b in biz:
    n, s = parse(b.get("full_business_address"))
    if n is None or not s: continue
    exact.add((n, s)); street_nums[s].add(n); streets[s] += 1

sf = [r for r in json.load(open(CD/"sf_taxable_commercial_spaces.json"))
      if r.get("taxyear") == "2024"]
seen = set(); rows = []
for r in sf:
    k = r.get("lin")
    if not k or k in seen: continue
    seen.add(k)
    n, s = parse(r.get("linaddress") or r.get("parcelsitusaddress"))
    rows.append(dict(lin=k, num=n, st=s, nbhd=r.get("analysis_neighborhood"),
                     vacant=r.get("vacant") == "YES", addr=r.get("linaddress")))
S = pd.DataFrame(rows)
O = S[(~S.vacant) & S.num.notna() & S.st.notna()].copy()

def m_exact(r):  return (r.num, r.st) in exact
def m_near(r, w=4):
    ns = street_nums.get(r.st)
    if not ns: return False
    return any(abs(x - r.num) <= w for x in ns)
def m_pm10(r):   return m_near(r, 10)

O["exact"] = O.apply(m_exact, axis=1)
O["within4"] = O.apply(lambda r: m_near(r, 4), axis=1)
O["within10"] = O.apply(m_pm10, axis=1)

print("=== TABLE 17. Match sensitivity, occupied storefronts, tax year 2024 ===")
def tab(sub, label):
    return dict(area=label, n=len(sub), exact=100*sub.exact.mean(),
                within4=100*sub.within4.mean(), within10=100*sub.within10.mean())
res = [tab(O, "ALL SF")]
for nb in ["Mission","Chinatown","North Beach","Japantown","Excelsior","Marina",
           "Inner Richmond","Noe Valley","Sunset/Parkside","Bayview Hunters Point",
           "Outer Mission","Bernal Heights","Tenderloin","Castro/Upper Market"]:
    sub = O[O.nbhd == nb]
    if len(sub) >= 30: res.append(tab(sub, nb))
T = pd.DataFrame(res)
print(T.round(1).to_string(index=False))
T.round(2).to_csv(HERE/"table17_h2_match_sensitivity.csv", index=False)

print("\n=== 20 Mission storefronts with NO business registration within +/-10 house numbers ===")
miss = O[(O.nbhd == "Mission") & (~O.within10)]
print(f"{len(miss)} of {len(O[O.nbhd=='Mission'])} Mission occupied storefronts")
random.seed(0)
for a in random.sample(list(miss.addr), min(20, len(miss))): print("  ", a)
