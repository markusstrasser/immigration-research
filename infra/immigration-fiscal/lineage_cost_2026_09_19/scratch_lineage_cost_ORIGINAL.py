"""100-year lineage fiscal cost of one unauthorized Mexico-born arrival, built from repo lane outputs.
Period profiles (2024$), no growth, no behavioural response, no general equilibrium."""
import pandas as pd, numpy as np
R = "/Users/alien/Projects/immigration-research/infra/immigration-fiscal"
prof = pd.read_csv(f"{R}/all_age_ledger_2026_09_17/derived/age_profiles.csv")
prof = prof[prof.scenario == "all_age_shared"].pivot(index="band", columns="target", values="balance_per_person")
BANDS = [(0,17),(18,24),(25,34),(35,44),(45,54),(55,64),(65,74),(75,110)]
def band(age): return next(i for i,(a,b) in enumerate(BANDS) if a <= age <= b)
wf = pd.read_csv(f"{R}/ledger_absolute_2026_09_17/derived/waterfall.csv")
final = wf.sort_values("step").groupby("group").cumulative_per_person.last()
base = wf[wf.step == 0].set_index("group").cumulative_per_person
addon = (final - base)  # complete-account items beyond the main partial account, per person-year, flat by age
lt = pd.read_csv(f"{R}/lifetime_longevity_sstiming_2026_09_18/derived/survival_tables.csv")
lx = lt[(lt.year == 2024) & (lt.table == "hispanic")].set_index("age").lx
fg = pd.read_csv(f"{R}/crime_cost_firstgen_2026_09_18/derived/firstgen_cost_weighted.csv")
fg = fg[(fg.denominator=="cms")&(fg.arm=="A")&(fg.status=="undocumented")].set_index("cost").usd_per_person_year
CRIME = {"founder": {"social": fg["total"], "tangible": fg["tangible"]},      # Texas undocumented, per person-year (ladder 144)
         "usborn":  {"social": 2820.0, "tangible": 1009.0}}                    # US-born Mexican-origin adult, crime_cost lane (ladder 78)
UNAUTH_WORKING_PENALTY = -870.0   # ladder 85 corrected arm: unauthorized −9,720 vs Mexico-born mean ≈ −8,850 at 25–64
print("complete-account add-on per person-year:", addon.round(0).to_dict())

def balance(group, age, account, status):
    b = prof.loc[band(age), group]
    if group == "mexico_born" and status == "stays_unauthorized":
        if age >= 65: b = 0.0                                    # no Social Security or Medicare, no earnings-side taxes to speak of
        elif age >= 25: b += UNAUTH_WORKING_PENALTY
    if account == "complete": b += addon[group]
    return b

def person_stream(group, birth_year, start_age, horizon, account, status, crime_key):
    """Expected fiscal balance and crime cost by calendar year for one person, survival-weighted."""
    fis = np.zeros(horizon+1); cr = np.zeros(horizon+1)
    l0 = lx[start_age]
    for age in range(start_age, 101):
        y = birth_year + age
        if y < 0 or y > horizon: continue
        s = lx[age] / l0
        fis[y] += s * balance(group, age, account, status)
        if 18 <= age <= 64: cr[y] += s * CRIME[crime_key]["social"]
    return fis, cr

def lineage(tfr, attribution, account, status, horizon=100, gen_len=29):
    """Founder arrives at 25 in year 0; each generation has its children at age 29."""
    share = 1.0 if attribution == "full" else 0.5
    out = {}
    # founder
    f, c = person_stream("mexico_born", -25, 25, horizon, account, status, "founder")
    out["G1 founder"] = (f, c)
    n = share * tfr["mexico_born"]; birth = 4                    # founder age 29
    for g, group in ((2,"mexican_second_gen"),(3,"mexican_third_plus_selfid"),(4,"mexican_third_plus_selfid"),(5,"mexican_third_plus_selfid")):
        if birth > horizon: break
        f, c = person_stream(group, birth, 0, horizon, account, status, "usborn")
        out[f"G{g} ({n:.2f} persons, born yr {birth})"] = (n*f, n*c)
        n *= share * tfr[group]; birth += gen_len
    return out

def pv(stream, r): return float(sum(v / (1+r)**t for t, v in enumerate(stream)))

FERT = {"low (repo ratios × white TFR 1.55)":  {"mexico_born": 1.71, "mexican_second_gen": 1.31, "mexican_third_plus_selfid": 1.41},
        "high (Mexico-born 2.3, US-born 1.9/1.8)": {"mexico_born": 2.30, "mexican_second_gen": 1.90, "mexican_third_plus_selfid": 1.80}}
rows = []
for account in ("main_partial", "complete"):
    for status in ("stays_unauthorized", "mexico_born_average"):
        for fl, tfr in FERT.items():
            for attr in ("half", "full"):
                L = lineage(tfr, attr, account, status)
                tot = sum(v[0] for v in L.values()); crime = sum(v[1] for v in L.values())
                rows.append(dict(account=account, founder_status=status, fertility=fl.split(" ")[0], attribution=attr,
                                 founder_lifetime=pv(L["G1 founder"][0],0), lineage_100y=pv(tot,0), per_year=pv(tot,0)/100,
                                 lineage_pv3=pv(tot,0.03), crime_social_100y=pv(crime,0), crime_pv3=pv(crime,0.03),
                                 persons=sum(float(k.split("(")[1].split(" ")[0]) for k in L if "(" in k)+1))
df = pd.DataFrame(rows)
pd.set_option("display.width", 250)
print(df.round(0).to_string(index=False))
# generation breakdown for one central case
L = lineage(FERT["low (repo ratios × white TFR 1.55)"], "half", "complete", "stays_unauthorized")
print("\nCentral case (complete account, stays unauthorized, low fertility, half attribution), undiscounted 100-year:")
for k,(f,c) in L.items(): print(f"  {k:<40} fiscal {pv(f,0):>12,.0f}   crime(social) {pv(c,0):>10,.0f}")
L = lineage(FERT["high (Mexico-born 2.3, US-born 1.9/1.8)"], "full", "complete", "stays_unauthorized")
print("Upper case (complete, stays unauthorized, high fertility, full attribution):")
for k,(f,c) in L.items(): print(f"  {k:<40} fiscal {pv(f,0):>12,.0f}   crime(social) {pv(c,0):>10,.0f}")

# ---- White reference lineage: same construction on the baseline-scenario white profile (generation memo table),
# white complete-account add-on (items_by_group), NH white 2024 life table, TFR 1.55 [TRAINING-DATA: NCHS 2023 NH white ≈1.5]
WHITE_BAND = [6244, 7000, 10447, 9275, 9601, 8725, -18246, -24754]
MEX_BASE = pd.read_csv(f"{R}/all_age_ledger_2026_09_17/derived/age_profiles.csv")
MEX_BASE = MEX_BASE[MEX_BASE.scenario == "baseline"].pivot(index="band", columns="target", values="balance_per_person")
lxw = lt[(lt.year == 2024) & (lt.table == "nh_white")].set_index("age").lx
def stream_generic(bands, addon_pp, lxt, birth_year, start_age, horizon, crime_pp):
    fis = np.zeros(horizon+1); cr = np.zeros(horizon+1); l0 = lxt[start_age]
    for age in range(start_age, 101):
        y = birth_year + age
        if y < 0 or y > horizon: continue
        s = lxt[age] / l0
        fis[y] += s * (bands[band(age)] + addon_pp)
        if 18 <= age <= 64: cr[y] += s * crime_pp
    return fis, cr
def lineage_generic(bands, addon_pp, lxt, tfr, share, crime_pp, horizon=100, gen_len=29):
    tot = np.zeros(horizon+1); cr = np.zeros(horizon+1)
    f, c = stream_generic(bands, addon_pp, lxt, -25, 25, horizon, crime_pp); tot += f; cr += c
    n = share * tfr; birth = 4
    while birth <= horizon:
        f, c = stream_generic(bands, addon_pp, lxt, birth, 0, horizon, crime_pp); tot += n*f; cr += n*c
        n *= share * tfr; birth += gen_len
    return tot, cr
print("\n== Reference lineages, complete account, 100 years undiscounted / PV3%  (founder 25 in year 0)")
for lab, bands, add, lxt, tfr, crime in (
    ("3rd+ NH white", WHITE_BAND, addon["third_plus_nh_white"], lxw, 1.55, 1399.0),
    ("Mexico-born avg (baseline profile)", MEX_BASE["mexico_born"].tolist(), addon["mexico_born"], lx, 1.71, 415.0)):
    for share in (0.5, 1.0):
        t, c = lineage_generic(bands, add, lxt, tfr, share, crime)
        print(f"  {lab:<36} attribution {share:<4} fiscal {pv(t,0):>12,.0f} / {pv(t,0.03):>10,.0f}   crime {pv(c,0):>10,.0f}")
