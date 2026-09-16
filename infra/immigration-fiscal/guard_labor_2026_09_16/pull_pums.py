"""ACS 2019-2023 5-year PUMS via tabulate: guard-labor employment share, nativity, ethnic fractionalization by state."""
import json, os, pathlib, urllib.request, csv
HERE = pathlib.Path(__file__).resolve().parent; CACHE = HERE/"_cache"; CACHE.mkdir(exist_ok=True)
KEY = os.environ["CENSUS_API_KEY"]
BASE = "https://api.census.gov/data/2023/acs/acs5/pums?tabulate=weight(PWGTP)"
FIPS = ["%02d"%i for i in range(1,57)]
SKIP = {"03","07","14","43","52"}
FIPS = [f for f in FIPS if f not in SKIP]
GUARD = {"3930":"security_guards_gaming"}
POLICE = {"3870":"police_officers","3820":"detectives_investigators","3801":"bailiffs_correctional","3900":"private_detectives"}
def get(tag, q):
    p = CACHE/f"{tag}.json"
    if not p.exists():
        p.write_bytes(urllib.request.urlopen(f"{BASE}{q}&key={KEY}", timeout=300).read())
    return json.loads(p.read_text())
def cells(tab):
    keys = [list(c.values())[0] for c in tab[0][:-1]]; rowvar = tab[0][-1]
    return rowvar, {r[-1]: dict(zip(keys, r[:-1])) for r in tab[1:]}
rows = []
for st in FIPS:
    _, occ = cells(get(f"occ_{st}", f"&col+OCCP&row+ESR&for=state:{st}"))
    emp = {}
    for esr in ("1","2"):
        for k,v in occ.get(esr,{}).items(): emp[k] = emp.get(k,0)+v
    tot_emp = sum(emp.values())
    _, nat = cells(get(f"nat_{st}", f"&col+ESR&row+NATIVITY&for=state:{st}"))
    pop_nat = {k: sum(v.values()) for k,v in nat.items()}
    _, hr = cells(get(f"hisprace_{st}", f"&col+RAC1P&row+HISP&for=state:{st}"))
    # ethnic groups: Hispanic (any race) as one, plus NH by RAC1P
    groups = {}
    for h, rr in hr.items():
        for r, n in rr.items():
            g = "hisp" if h != "01" else f"nh_{r}"
            groups[g] = groups.get(g,0)+n
    tot_pop = sum(groups.values())
    frac = 1 - sum((n/tot_pop)**2 for n in groups.values())
    rows.append(dict(state=st, employed=tot_emp,
        guards=sum(emp.get(c,0) for c in GUARD), police=sum(emp.get(c,0) for c in POLICE),
        **{f"occ_{c}": emp.get(c,0) for c in list(GUARD)+list(POLICE)},
        pop=sum(pop_nat.values()), foreign_born=pop_nat.get("2",0),
        hisp=groups.get("hisp",0), black=groups.get("nh_2",0), frac=round(frac,5)))
for r in rows:
    r["guard_share"]=r["guards"]/r["employed"]*100; r["police_share"]=r["police"]/r["employed"]*100
    r["fb_share"]=r["foreign_born"]/r["pop"]*100; r["hisp_share"]=r["hisp"]/r["pop"]*100
    r["black_share"]=r["black"]/r["pop"]*100
with open(HERE/"state_pums.csv","w",newline="") as f:
    w=csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
nat_guards=sum(r["guards"] for r in rows); nat_pol=sum(r["police"] for r in rows)
print(f"GATE(a) national security guards+gaming surveillance (OCCP 3930) employed = {nat_guards:,}  [BLS OES 2023 SOC 33-9032 ~1.16M]")
print(f"national public police/corrections/detective employment = {nat_pol:,}")
for r in rows:
    if r["state"] in ("06","48"): print(f"GATE(b) state {r['state']} foreign-born share = {r['fb_share']:.2f}%")
print(f"n states = {len(rows)}")
