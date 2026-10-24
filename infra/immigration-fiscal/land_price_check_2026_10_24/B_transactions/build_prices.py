#!/usr/bin/env python3
"""
Build B_transactions/prices.csv

Primary source (all five counties)
----------------------------------
Albouy, Ehrlich & Shin (2018), "Metropolitan Land Values", Review of Economics and
Statistics 100(3):454-466.  Metro / PMSA land values estimated from CoStar COMPS
vacant-land sales, 2005-2010, and averaged over each metro's urban area.

Values are read from the paper's replication file (Harvard Dataverse
doi:10.7910/DVN/KSTT2Q, file tab_lv_log2m6_estX_M2.xls), sheet "land_values (MSAs)":
  LV (UA)      = average land value per acre over the metro's urban area, 2005-2010 pooled
  LV-2005..10  = the annual values (their mean equals LV (UA))
  n            = number of CoStar land sales behind the PMSA estimate

Second source (Los Angeles, Riverside-San Bernardino, San Jose only)
--------------------------------------------------------------------
Gyourko & Krimmel (2021, JUE 126:103374), 2020 working-paper version, Appendix Table 2:
"Mean P(L) / ft2" = mean price per square foot of vacant land bought for single-family
development, 2013-2018, within 30 miles of the CBSA centroid.  x 43,560 = $/acre.

Conversion to 2024 (never FHFA land data)
-----------------------------------------
  * S&P CoreLogic Case-Shiller metro HPI, monthly SA, annual averages
    (FRED LXXRSA = Los Angeles, SDXRSA = San Diego, SFXRSA = San Francisco;
    values read from the FRED mirror data/cities-month-SA.csv, cross-checked
    against FRED /data/LXXRSA and against github.com/aalokpatwa/case-shiller).
  * CPI-U, U.S. city average, all items, NSA (BLS CUUR0000SA0), annual averages,
    used where the metro has no Case-Shiller index (San Jose, Riverside-San Bernardino).
"""
import json
import pandas as pd

CACHE = "_cache"
SQFT_PER_ACRE = 43560.0
COUNTY = {"06037": "Los Angeles", "06059": "Orange", "06073": "San Diego",
          "06071": "San Bernardino", "06085": "Santa Clara"}

# ------------------------------------------------------------------ source 1
aes = pd.read_excel(f"{CACHE}/aes_msa_table.xls", sheet_name="land_values (MSAs)")

# county_fips -> (PMSA label in replication file, primary deflator, alternate deflator)
AES_ROWS = {
    "06037": ("Los Angeles-Long Beach CA", "cs_la", None),
    "06059": ("Orange County CA", "cs_la", None),   # Orange Co sits in the LA-Long Beach-Anaheim CBSA
    "06073": ("San Diego CA", "cs_sd", None),
    "06071": ("Riverside-San Bernardino CA", "cpi", "cs_la"),
    "06085": ("San Jose CA", "cpi", "cs_sf"),       # no Case-Shiller San Jose index exists
}

# ------------------------------------------------------------------ deflators
cs = pd.read_csv(f"{CACHE}/cs_cities_sa.csv")
cs["Date"] = pd.to_datetime(cs["Date"])
cs["y"] = cs["Date"].dt.year
cs_ann = cs.groupby("y")[["CA-Los Angeles", "CA-San Diego", "CA-San Francisco"]].mean()
CS_COL = {"cs_la": "CA-Los Angeles", "cs_sd": "CA-San Diego", "cs_sf": "CA-San Francisco"}
CS_ID = {"cs_la": "LXXRSA", "cs_sd": "SDXRSA", "cs_sf": "SFXRSA"}

cpi_m = json.load(open(f"{CACHE}/cpi_u_monthly.json"))
_cpi = {}
for k, v in cpi_m.items():
    _cpi.setdefault(int(k.split("-")[0]), []).append(v)
cpi_ann = {y: sum(v) / len(v) for y, v in _cpi.items()}

def defl(kind, year):
    if kind == "cpi":
        return cpi_ann[2024] / cpi_ann[year]
    return cs_ann.loc[2024, CS_COL[kind]] / cs_ann.loc[year, CS_COL[kind]]

def defl_period(kind, y0, y1):
    if kind == "cpi":
        base = sum(cpi_ann[y] for y in range(y0, y1 + 1)) / (y1 - y0 + 1)
        return cpi_ann[2024] / base
    col = CS_COL[kind]
    return cs_ann.loc[2024, col] / cs_ann.loc[y0:y1, col].mean()

def label(kind):
    if kind == "cpi":
        return "CPI-U (U.S. city average, all items, NSA; BLS CUUR0000SA0)"
    name = {"cs_la": "Los Angeles", "cs_sd": "San Diego", "cs_sf": "San Francisco"}[kind]
    return f"Case-Shiller {name} metro HPI (FRED {CS_ID[kind]})"

# ------------------------------------------------------------------ source 2
GK = {  # county_fips: (CBSA label, mean P(L)/ft2, n, deflator)
    "06037": ("Los Angeles", 49.64, 157, "cs_la"),
    "06071": ("Riverside", 9.09, 286, "cpi"),
    "06085": ("San Jose", 32.69, 44, "cpi"),
}

# ------------------------------------------------------------------ build
rows = []
for fips, (pmsa, kind, alt) in AES_ROWS.items():
    r = aes[aes["pmsa"] == pmsa].iloc[0]
    years = list(range(2005, 2011))
    vals = [float(r[f"LV-{y}"]) for y in years]
    conv = [v * defl(kind, y) for v, y in zip(vals, years)]
    p2024 = sum(conv) / len(conv)

    notes = [
        f"Conversion: {label(kind)} annual averages, 2024 / 2005-2010 "
        f"= x{p2024/float(r['LV (UA)']):.3f} (applied year by year to LV-2005..LV-2010)",
        f"as-published 2005-2010 pooled value ${float(r['LV (UA)']):,.0f}/acre nominal",
    ]
    if alt:
        altv = sum(v * defl(alt, y) for v, y in zip(vals, years)) / len(vals)
        notes.append(f"if converted with {label(alt)} instead: ${altv:,.0f}/acre")
    if fips == "06071":
        notes.append("PMSA covers Riverside AND San Bernardino counties, not San Bernardino alone")
    if fips == "06059":
        notes.append("Orange County PMSA = Orange County; converted with the LA metro Case-Shiller index, "
                     "which covers the whole Los Angeles-Long Beach-Anaheim CBSA (LA + Orange)")
    if fips in GK:
        name, psf, n, gk_kind = GK[fips]
        gk = psf * SQFT_PER_ACRE * defl_period(gk_kind, 2013, 2018)
        notes.append(
            f"Second source: Gyourko & Krimmel, Appendix Table 2, {name} CBSA mean P(L)/ft2="
            f"${psf}/ft2 (n={n} parcels, 2013-2018) = ${psf*SQFT_PER_ACRE:,.0f}/acre nominal, "
            f"x{defl_period(gk_kind,2013,2018):.3f} ({label(gk_kind)}) = ${gk:,.0f}/acre in 2024"
        )

    rows.append(dict(
        county_fips=fips,
        county=COUNTY[fips],
        price_per_acre_2024=round(p2024),
        low_per_acre_2024="",
        high_per_acre_2024="",
        n_obs=int(r["n"]),
        year_measured="2005-2010",
        land_type="all urban land (CoStar vacant-land sales; residential, commercial and industrial)",
        method=("CoStar COMPS vacant-land transactions 2005-2010; monocentric hedonic with Bayesian "
                "shrinkage; land value averaged over the metro's urban area; annual values converted "
                f"to 2024 with {label(kind)}"),
        source="Albouy, Ehrlich & Shin (2018), Review of Economics and Statistics 100(3):454-466",
        source_locator=("replication file doi:10.7910/DVN/KSTT2Q, tab_lv_log2m6_estX_M2.xls, sheet "
                        f"'land_values (MSAs)', row PMSA='{pmsa}', cols LV-2005..LV-2010 and n; "
                        "published as Table 2, col. 7 'Urban Average'"),
        notes="; ".join(notes),
    ))

cols = ["county_fips", "county", "price_per_acre_2024", "low_per_acre_2024", "high_per_acre_2024",
        "n_obs", "year_measured", "land_type", "method", "source", "source_locator", "notes"]
pd.DataFrame(rows)[cols].to_csv("prices.csv", index=False, lineterminator="\n")

print(pd.DataFrame(rows)[["county_fips", "county", "price_per_acre_2024", "n_obs"]].to_string(index=False))
print()
for r in rows:
    print(r["county"], "::", r["notes"], "\n")
