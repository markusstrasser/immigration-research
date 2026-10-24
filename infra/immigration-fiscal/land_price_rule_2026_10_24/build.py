"""An acquisition-cost price rule for the land under every public capital line of the oct16 case.

The rule prices each acre at what land of that kind costs to obtain where it lies, which is what a
long-run budget response saves when a smaller stock is never built (FTA 2018 p.13; Yellow Book 2016
market-value standard; OECD-Eurostat 2015 para 8.100). Factors and pages: `derived/factors.csv`.

- Urban roads, interstates to minor arterials (HPMS classes 1-4), are bought from existing
  parcels by highway agencies: across-the-fence (ATF) residential land × 1.0.
- Urban collectors and local streets (classes 5-7) are dedicated when land is subdivided; their
  cost is raw land per gross acre, ATF × the developable share 0.65 (NAHB via Gyourko-Krimmel 2021,
  the school lane's arm B).
- Urban parks, airports, plants and every built-up site: the large-site rule, ATF × 0.65 (sites over
  two acres) or 0.80. K-12 keeps the school lane's values.
- Rural acres of every line: the county's farmland value per acre (Census of Agriculture 2022 land
  and buildings, × the state land-only share, × the state June-survey change 2022→2024), × 1.0.
- The urban ATF price is FHFA's 2024 as-is residential price: urban roads take the land-area mean of
  the county's urban tracts, other sites their own tract. Every state fallback is replaced: urban by
  the nearest county with an FHFA price, rural by county farmland.

One central and one range per line; the range moves every factor to its cited low or high end together.
Charge = land × the line's case coefficient (key × response, mean of the two methods, as in
public_land) × 2.0810698764%; also at the θ-paired federal and state/local rates.

    OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/land_price_rule_2026_10_24/build.py
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
import os
import subprocess
import sys
import time
import zipfile
from pathlib import Path

if not sys.flags.isolated:
    os.execv(sys.executable, [sys.executable, "-I", *sys.argv])
sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

import acquire  # noqa: E402
import classify  # noqa: E402

FISCAL = HERE.parent
ROOT = FISCAL.parent.parent
PUBLIC = FISCAL / "public_land_2026_10_24"
SCHOOL = FISCAL / "school_land_2026_10_24"
RATE_MODEL = FISCAL / "public_capital_rate_2026_10_24" / "derived" / "rate_model.json"
OUT = HERE / "derived"
NASS = HERE / "_cache" / "nass"
GAZ_COUNTIES = HERE / "_cache" / "geo" / "2020_Gaz_counties_national.zip"
CORRIDOR_LINES = {"hwy_sl", "hwy_fed", "ent_tolls_sl"}
PERIPHERY_LINES = {"rec_sl", "ent_airports_sl", "ent_sewer_sl", "ent_water_sl", "ent_power_sl"}
OMIT_COUNTIES = {"36061", "06075", "11001"}

# Every factor: (central, low, high). Sources and pages in factors.csv (FACTOR_SOURCES).
F_ARTERIAL = (1.0, 0.65, 1.16)          # urban HPMS 1-4: ATF; low englobo (greenfield-built); high FTA CEF median
F_SUBDIVISION = (0.65, 0.35, 1.0)       # urban HPMS 5-7 and large sites: NAHB share; low NSW englobo; high straight ATF
F_SMALL_SITE = (0.80, 0.80 * 0.35 / 0.65, 1.0)  # sites <= 2 acres: NAHB 0.80, same proportional range
F_RURAL = (1.0, 1.0, 1.16)              # rural farmland is priced per gross acre; high FTA CEF median for acquired roads
LAND_SHARE_RANGE = (0.691, 0.862)       # ERS historical land share of farm real estate (buildings 13.8-30.9%)
FACTOR_SOURCES = [
    ("urban_arterial_corridor", "urban HPMS classes 1-4 (interstate, freeway/expressway, principal and minor arterial)", *F_ARTERIAL,
     "central: FTA, Valuation of Railroad Right of Way (rev. 2018) p.13 'the proper methodology would be the basic across the fence approach'; "
     "low: englobo/developable share (row below), a road built with its subdivision; high: FTA (2018) p.11 corridor sales median 1.158, range 1.096-1.298",
     "_cache/sources/fta_valuation_railroad_row.pdf"),
    ("urban_subdivision_streets", "urban HPMS classes 5-7 (collectors, local streets); urban parks, airports, plants, built-up sites over 2 acres", *F_SUBDIVISION,
     "central: NAHB 'no more than 65% of a large parcel can be used for housing' via Gyourko & Krimmel (2021) NBER w28993 note 13 and p.16 (school_land arm B); "
     "low: NSW OLG Code of Accounting Practice s.5 appendices p.11, 65% englobo adjustment to average site value (0.35), before its 25% in-use access discount; "
     "high: straight ATF, FTA (2018) p.13; OECD-Eurostat land guide (2015) para 8.100 p.139 comparable private land",
     "_cache/sources/nsw_olg_code_section5_appendices.pdf"),
    ("small_site", "built-up sites of 2 acres or less", *F_SMALL_SITE,
     "central: Gyourko & Krimmel (2021) 80% for parcels under two acres (school_land arm B); range scaled by the same 0.35/0.65 and capped at ATF", ""),
    ("rural_corridor_and_site", "rural acres of every line, at county farmland value", *F_RURAL,
     "central: farmland sells per gross acre with no subdivision step; vacated rural roads revert to abutting farms (RCW 35.79.040; A.R.S. 28-7205 'to the center'); "
     "high: FTA (2018) p.11 acquired-corridor median 1.158", ""),
    ("farm_land_only_share", "share of Census of Agriculture land-and-buildings value that is land", 0.0, *LAND_SHARE_RANGE,
     "central: state value of cropland and pasture (NASS Land Values 2024 Summary, defined as land, p.20) weighted by Census 2022 cropland and other farm acres, "
     "over farm real estate (land and buildings); US 0.825; check ERS AR-26 (1992) p.5 buildings 18.7% (0.813); "
     "range: ERS historical buildings share 13.8-30.9% (land 0.691-0.862), applied as a ratio to the central",
     "_cache/sources/nass_land_values_2024.pdf"),
]


def write_csv(frame, name):
    frame.to_csv(OUT / name, index=False, lineterminator="\n", float_format="%.12g")


def json_finite(value):
    if isinstance(value, dict):
        return {str(k): json_finite(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [json_finite(v) for v in value]
    if isinstance(value, np.generic):
        return json_finite(value.item())
    if isinstance(value, float) and not np.isfinite(value):
        raise ValueError("[BLOCKED] nonfinite output")
    return value


def write_json(value, name):
    (OUT / name).write_text(json.dumps(json_finite(value), indent=2, sort_keys=True, allow_nan=False) + "\n")


def school_engine():
    spec = importlib.util.spec_from_file_location("land_rule_school_prices", SCHOOL / "build.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module, module.prices()


# ------------------------------------------------------------------------------------------ rural prices
def num(s):
    return pd.to_numeric(s.astype(str).str.replace(",", "").str.strip(), errors="coerce")


def farm_prices():
    """County farmland $/acre, land only, 2024. Missing or withheld (D) counties take the state value."""
    c = pd.read_csv(NASS / "census2022_land.csv", dtype=str)
    c["v"] = num(c.VALUE)
    s = pd.read_csv(NASS / "survey_land_values.csv", dtype=str)
    s["v"] = num(s.VALUE)
    per_acre = "AG LAND, INCL BUILDINGS - ASSET VALUE, MEASURED IN $ / ACRE"
    crop_v, past_v = "AG LAND, CROPLAND - ASSET VALUE, MEASURED IN $ / ACRE", "AG LAND, PASTURELAND - ASSET VALUE, MEASURED IN $ / ACRE"

    def survey(level, year, item):
        x = s[s.AGG_LEVEL_DESC.eq(level) & s.YEAR.eq(str(year)) & s.SHORT_DESC.eq(item)]
        return x.set_index("STATE_FIPS_CODE" if level == "STATE" else "AGG_LEVEL_DESC").v
    st = c[c.AGG_LEVEL_DESC.eq("STATE")].pivot_table(index="STATE_FIPS_CODE", columns="SHORT_DESC", values="v")
    us = c[c.AGG_LEVEL_DESC.eq("NATIONAL")].set_index("SHORT_DESC").v
    re22, re24 = survey("STATE", 2022, per_acre), survey("STATE", 2024, per_acre)
    us_re22, us_re24 = survey("NATIONAL", 2022, per_acre).iloc[0], survey("NATIONAL", 2024, per_acre).iloc[0]
    crop22, past22 = survey("STATE", 2022, crop_v), survey("STATE", 2022, past_v)

    def land_share(crop_price, past_price, re_price, crop_ac, total_ac):
        return (crop_price * crop_ac + past_price * (total_ac - crop_ac)) / (re_price * total_ac)
    crop_ac, tot_ac = "AG LAND, CROPLAND - ACRES", "FARM OPERATIONS - ACRES OPERATED"
    us_share = land_share(survey("NATIONAL", 2022, crop_v).iloc[0], survey("NATIONAL", 2022, past_v).iloc[0], us_re22,
                          us[crop_ac], us[tot_ac])
    states = pd.DataFrame(index=st.index)
    states["census_per_acre"] = st[per_acre]
    states["land_share"] = land_share(crop22, past22, re22, st[crop_ac], st[tot_ac]).reindex(states.index)
    states["land_share_level"] = np.where(states.land_share.notna(), "state", "national")
    states["land_share"] = states.land_share.fillna(us_share).clip(upper=1.0)
    states["growth_22_24"] = (re24 / re22).reindex(states.index)
    states["growth_level"] = np.where(states.growth_22_24.notna(), "state", "national")
    states["growth_22_24"] = states.growth_22_24.fillna(us_re24 / us_re22)
    states["pasture_2024"] = survey("STATE", 2024, past_v).reindex(states.index)
    states["pasture_level"] = np.where(states.pasture_2024.notna(), "state", "national")
    states["pasture_2024"] = states.pasture_2024.fillna(survey("NATIONAL", 2024, past_v).iloc[0])
    co = c[c.AGG_LEVEL_DESC.eq("COUNTY") & c.SHORT_DESC.eq(per_acre)].copy()
    co["county"] = co.STATE_FIPS_CODE.str.zfill(2) + co.COUNTY_CODE.str.zfill(3)
    co = co.set_index("county").v
    return dict(states=states, county=co, us_share=float(us_share), us_growth=float(us_re24 / us_re22),
                us_census=float(us[per_acre]))


def farm_price_rows(counties, farm):
    t = pd.DataFrame({"county": sorted(set(counties))})
    t["state"] = t.county.str[:2]
    st = farm["states"]
    t["farm_census"] = t.county.map(farm["county"])
    t["farm_level"] = np.where(t.farm_census.notna(), "county", "state")
    t["farm_census"] = t.farm_census.fillna(t.state.map(st.census_per_acre))
    # DC has no farm census; it takes the national values (it has no rural acres).
    t.loc[t.farm_census.isna(), "farm_level"] = "national"
    t["farm_census"] = t.farm_census.fillna(farm["us_census"])
    t["land_share"] = t.state.map(st.land_share).fillna(farm["us_share"])
    t["growth"] = t.state.map(st.growth_22_24).fillna(farm["us_growth"])
    t["pasture_2024"] = t.state.map(st.pasture_2024).fillna(st.pasture_2024.median())
    if t[["farm_census", "land_share", "growth"]].isna().any().any():
        raise ValueError(f"[BLOCKED] farmland price missing: {t[t.farm_census.isna()].county.tolist()[:5]}")
    t["farm24"] = t.farm_census * t.land_share * t.growth
    return t


# ------------------------------------------------------------------------------------------ urban prices
def nearest_fhfa(P):
    """Each county without an FHFA cross-section price -> nearest (great circle) county with one."""
    with zipfile.ZipFile(GAZ_COUNTIES) as z:
        name = [n for n in z.namelist() if n.endswith(".txt")][0]
        g = pd.read_csv(z.open(name), sep="\t", dtype={"GEOID": str})
    g.columns = [x.strip() for x in g.columns]
    g = g.rename(columns={"GEOID": "county", "INTPTLAT": "lat", "INTPTLONG": "lon"})[["county", "lat", "lon"]]
    have = g[g.county.isin(P["xc"].index)]
    lat1, lon1 = np.radians(g.lat.to_numpy())[:, None], np.radians(g.lon.to_numpy())[:, None]
    lat2, lon2 = np.radians(have.lat.to_numpy())[None, :], np.radians(have.lon.to_numpy())[None, :]
    d = 2 * np.arcsin(np.sqrt(np.sin((lat2 - lat1) / 2) ** 2 + np.cos(lat1) * np.cos(lat2) * np.sin((lon2 - lon1) / 2) ** 2)) * 3958.8
    j = d.argmin(axis=1)
    return pd.DataFrame({"county": g.county, "nearest_fhfa_county": have.county.to_numpy()[j], "nearest_miles": d[np.arange(len(g)), j]}).set_index("county")


def county_urban_prices(engine, P, urban_tracts):
    """Urban ATF price per county: land-area-weighted mean of its urban tracts' FHFA tract prices."""
    with zipfile.ZipFile(SCHOOL / "_cache" / "gaz" / "Gaz_tracts_national_2010.zip") as z:
        g = pd.read_csv(z.open("Gaz_tracts_national.txt"), sep="\t", dtype={"GEOID": str})
    g.columns = [x.strip() for x in g.columns]
    g = g[g.GEOID.isin(urban_tracts) & g.GEOID.isin(P["xt"].index)][["GEOID", "ALAND"]]
    pr = engine.price_rows(g.GEOID, P).set_index("tract")
    g["p24"] = g.GEOID.map(pr.p24)
    g["county"] = g.GEOID.str[:5]
    g = g[g.p24.gt(0) & g.ALAND.gt(0)]
    w = g.groupby("county").apply(lambda x: np.average(x.p24, weights=x.ALAND), include_groups=False)
    return w.rename("urban_tract_p24")


def urban_price_table(engine, P, counties, near, urban_tract_price):
    """Per county: urban-tract price, else county FHFA price, else nearest FHFA county's price."""
    t = pd.DataFrame({"county": sorted(set(counties))})
    own = engine.price_rows(t.county + "999999", P)
    own["county"] = own.tract.str[:5]
    own = own.set_index("county")
    t["county_p24"] = np.where(t.county.map(own.price_level).eq("county"), t.county.map(own.p24), np.nan)
    t["nearest_fhfa_county"] = t.county.map(near.nearest_fhfa_county)
    t["nearest_miles"] = t.county.map(near.nearest_miles)
    alt = engine.price_rows(t.nearest_fhfa_county.dropna() + "999999", P)
    alt["county"] = alt.tract.str[:5]
    alt = alt.set_index("county")
    t["nearest_p24"] = t.nearest_fhfa_county.map(alt.p24)
    t["state_p24"] = t.county.map(own.p24)  # the source engine's state fallback, for the replaced-value report
    t["urban_tract_p24"] = t.county.map(urban_tract_price)
    t["urban_p24"] = t.urban_tract_p24.fillna(t.county_p24).fillna(t.nearest_p24)
    t["urban_level"] = np.select([t.urban_tract_p24.notna(), t.county_p24.notna(), t.nearest_p24.notna()],
                                 ["urban_tracts", "county", "nearest_county"], "missing")
    t["urban_county_p24"] = t.county_p24.fillna(t.nearest_p24)  # stability variant: county average, no tract weighting
    return t.set_index("county")


# ------------------------------------------------------------------------------------------ records
def load_records():
    d = pd.read_parquet(PUBLIC / "_cache" / "priced_sites.parquet")
    roads = pd.read_csv(PUBLIC / "derived" / "roads_county_acres.csv", dtype={"county_fips": str, "toll_id": str})
    roads = roads[roads.case_line.notna() & roads.case_line.ne("")].reset_index(drop=True)
    hw = d[d["class"].eq("highway")].copy()
    hw["i"] = hw.record_id.str.split(":").str[1].astype(int)
    hw = hw.sort_values("i").reset_index(drop=True)
    if len(hw) != len(roads) or not np.allclose(hw.acres.to_numpy(), roads.acres.to_numpy()) or (hw.line.to_numpy() != roads.case_line.to_numpy()).any():
        raise ValueError("[BLOCKED] highway records no longer align with public_land roads_county_acres.csv")
    hw["area_type"] = roads.area_type.to_numpy()
    hw["functional_class"] = roads.functional_class.to_numpy()
    hw["county"] = roads.county_fips.to_numpy()
    hw["centerline_miles"] = roads.centerline_miles.to_numpy()
    hw["urban_fraction"] = np.where(hw.area_type.eq("urban"), 1.0, 0.0)
    return d[~d["class"].eq("highway")].copy(), hw


def attach_urban_status(rest, status):
    st = {k: g.set_index("record_id").urban_fraction for k, g in status.groupby("kind")}
    rest = rest.copy()
    rest["urban_fraction"] = np.nan
    park = rest["class"].eq("park")
    rest.loc[park, "urban_fraction"] = rest.loc[park, "record_id"].str.split(":").str[1].map(st["park"]).to_numpy()
    air = rest["class"].eq("airport")
    rest.loc[air, "urban_fraction"] = rest.loc[air, "record_id"].map(st["airport"]).to_numpy()
    fac = ~(park | air | rest["class"].eq("school"))
    rest.loc[fac, "urban_fraction"] = rest.loc[fac, "record_id"].map(st["facility"]).to_numpy()
    # A missing point (or a school) takes its 2010 tract's internal point.
    miss = rest.urban_fraction.isna() & rest.tract.notna()
    rest.loc[miss, "urban_fraction"] = rest.loc[miss, "tract"].map(st["tract2010"]).to_numpy()
    # A county-only record (synthetic tract) is urban if most of the county's tracts are.
    miss = rest.urban_fraction.isna() & rest.county.notna() & rest.county.ne("")
    by_county = st["tract2010"].groupby(st["tract2010"].index.str[:5]).mean()
    rest.loc[miss, "urban_fraction"] = (rest.loc[miss, "county"].map(by_county) >= 0.5).astype(float).to_numpy()
    return rest


def value_records(rest, hw, upt, farm_rows, P, engine):
    """Return one frame with central/low/high national land value per record and the variants."""
    fr = farm_rows.set_index("county")
    out = []
    # Roads.
    h = hw.copy()
    h["rule"] = np.where(h.area_type.eq("rural"), "rural_corridor_and_site",
                         np.where(h.functional_class.le(4), "urban_arterial_corridor", "urban_subdivision_streets"))
    h["urban_p24"] = h.county.map(upt.urban_p24)
    h["urban_level"] = h.county.map(upt.urban_level)
    h["urban_county_p24"] = h.county.map(upt.urban_county_p24)
    # Unknown county (HPMS county 000): the source engine's state price, reported.
    unknown = h.county.str[2:].eq("000")
    if unknown.any():
        stp = engine.price_rows(h.loc[unknown, "county"].str[:2] + "000999999", P).set_index("tract").p24
        h.loc[unknown, "urban_p24"] = (h.loc[unknown, "county"].str[:2] + "000999999").map(stp).to_numpy()
        h.loc[unknown, "urban_county_p24"] = h.loc[unknown, "urban_p24"]
        h.loc[unknown, "urban_level"] = "state_unknown_county"
    h["urban_acres"] = h.acres * h.urban_fraction
    h["rural_acres"] = h.acres - h.urban_acres
    h["site_factor"] = 1.0
    out.append(h)
    # Everything else keeps its record; built-up lines keep their tract price unless it was a state fallback.
    r = rest.copy()
    r["urban_acres"] = r.acres * r.urban_fraction.fillna(1.0)
    r["rural_acres"] = r.acres - r.urban_acres
    r["functional_class"] = 0
    built_up = ~r.line.isin(PERIPHERY_LINES)
    small = r.site_acres.le(2.0)
    r["rule"] = np.where(small, "small_site", "urban_subdivision_streets")
    # Built-up sites are priced wholly at their urban rule unless they sat on a state fallback.
    state_fb = r.price_level.eq("state")
    whole_urban = built_up & ~state_fb
    r.loc[whole_urban, "urban_acres"] = r.loc[whole_urban, "acres"]
    r.loc[whole_urban, "rural_acres"] = 0.0
    tract_p = r.p24.where(~state_fb)
    r["urban_p24"] = tract_p.fillna(r.county.map(upt.urban_p24))
    r["urban_county_p24"] = r.county.map(upt.urban_county_p24).fillna(r.urban_p24)
    r["urban_level"] = np.where(~state_fb & r.p24.notna(), r.price_level, r.county.map(upt.urban_level))
    out.append(r)
    d = pd.concat(out, ignore_index=True, sort=False)
    d["farm24"] = d.county.map(fr.farm24)
    d["farm_level"] = d.county.map(fr.farm_level)
    d["pasture_2024"] = d.county.map(fr.pasture_2024)
    d["land_share"] = d.county.map(fr.land_share)
    miss = d.farm24.isna() & d.county.fillna("").str.fullmatch(r"[0-9]{5}")
    if miss.any():  # HPMS unknown county (000): the state's farmland value
        stv = FARM["states"]
        st = d.loc[miss, "county"].str[:2]
        d.loc[miss, "farm24"] = st.map(stv.census_per_acre * stv.land_share * stv.growth_22_24).to_numpy()
        d.loc[miss, "farm_level"] = "state"
        d.loc[miss, "pasture_2024"] = st.map(stv.pasture_2024).to_numpy()
        d.loc[miss, "land_share"] = st.map(stv.land_share).to_numpy()
    factors = {name: (c, lo, hi) for name, _, c, lo, hi, _, _ in FACTOR_SOURCES}
    ls_lo, ls_hi = LAND_SHARE_RANGE[0] / FARM["us_share"], LAND_SHARE_RANGE[1] / FARM["us_share"]
    priced = d.urban_p24.notna() | d.urban_acres.eq(0)
    d["priced_rule"] = priced & d.farm24.notna()
    for k, idx in [("central", 0), ("low", 1), ("high", 2)]:
        f_urban = d.rule.map(lambda x: factors[x][idx])
        f_rural = factors["rural_corridor_and_site"][idx]
        share_adj = {"central": 1.0, "low": ls_lo, "high": ls_hi}[k]
        urban = d.urban_acres * d.urban_p24.fillna(0) * f_urban
        rural = d.rural_acres * d.farm24 * f_rural * share_adj
        d["value_" + k] = (urban + rural).where(d.priced_rule, 0.0)
        d["urban_value_" + k] = urban.where(d.priced_rule, 0.0)
        d["rural_value_" + k] = (rural).where(d.priced_rule, 0.0)
    # K-12 keeps the school lane's arm B values (tract prices, its own imputation and validation);
    # only its state-fallback schools are repriced above.
    k12 = d.line.eq("k12") & ~d.price_level.eq("state")
    for k in ["central", "low", "high"]:
        scale = {"central": 1.0, "low": F_SUBDIVISION[1] / F_SUBDIVISION[0], "high": F_SUBDIVISION[2] / F_SUBDIVISION[0]}[k]
        # small schools carry 0.80; their range scales identically, so one ratio covers both, capped at ATF
        capped = np.minimum(d.loc[k12, "value_B"] * scale, d.loc[k12, "value_A"])
        d.loc[k12, "value_" + k] = capped
        d.loc[k12, "urban_value_" + k] = capped
        d.loc[k12, "rural_value_" + k] = 0.0
    # Group weights: K-12 carries the where-enrolled weighting per school; scale it with the new value.
    ratio = (d.group_weighted_value_B / d.value_B).where(d.line.eq("k12") & d.value_B.gt(0))
    d["group_ratio"] = ratio.fillna(1.0)
    # Variants for the screen's stability test.
    v = d.copy()
    f_c = d.rule.map(lambda x: factors[x][0])
    d["value_variant_county_avg_urban"] = (d.urban_acres * d.urban_county_p24.fillna(0) * f_c + d.rural_acres * d.farm24).where(d.priced_rule, 0.0)
    d.loc[k12, "value_variant_county_avg_urban"] = d.loc[k12, "value_central"]
    d["value_variant_rural_parks_pasture"] = d.value_central
    rp = d.line.eq("rec_sl")
    d.loc[rp, "value_variant_rural_parks_pasture"] = (d.urban_value_central + d.rural_acres * d.pasture_2024)[rp]
    del v
    return d


def coefficients():
    case = pd.read_csv(PUBLIC / "derived" / "case_physical_lines.csv")
    coef = case.groupby(["end", "line"]).effective_key_times_response.mean().unstack(0)
    level = case.groupby("line")["level"].first()
    by_method = case.pivot_table(index="line", columns=["method", "end"], values="effective_key_times_response")
    return coef, level, by_method, case


def rates():
    m = json.loads(RATE_MODEL.read_text())["theta_pairing"]["anchor_fg_baseline"]
    contract = json.loads((PUBLIC / "derived" / "case_contract.json").read_text())
    return dict(case=contract["rate"], theta=m["theta"],
                paired_central=dict(state_local=m["d_central"]["rate_state_local"], federal=m["d_central"]["rate_federal"]),
                paired_high=dict(state_local=m["d_high"]["rate_state_local"], federal=m["d_high"]["rate_federal"]),
                band=contract["band_bn"])


FARM = None
ENGINE = None
PRICES = None


def fhwa_row_share():
    """FHWA Highway Statistics 2022 Table SF-12A: right-of-way share of state highway capital outlay."""
    xs = pd.read_excel(HERE / "_cache" / "fhwa" / "sf12a_2022.xlsx", header=None, sheet_name=None)
    row = tot = expand = 0.0
    for x in xs.values():
        t = x[x[0].astype(str).str.strip().eq("Total")].iloc[0]
        row, tot = row + float(t[1]), tot + float(t[18])
        expand += float(t[1]) + float(t[3]) + float(t[5]) + float(t[7]) + float(t[11])  # ROW, new construction, added capacity, major widening, new bridge
    return dict(row_share_of_all_capital_outlay=row / tot, row_share_of_expansion_outlay=row / expand, row_thousand_usd=row,
                source="FHWA Highway Statistics 2022 Table SF-12A, sheets 1-14 'Total' rows; columns ROW, New construction, Reconstruction added capacity, Major widening, New bridge",
                note="a purchase flow on mostly existing alignments; it cannot validate a stock ratio, since most street land was dedicated and land is not depreciated")


def main():
    global FARM, ENGINE, PRICES
    start = time.perf_counter()
    OUT.mkdir(exist_ok=True)
    acquire.main()
    status = classify.build()
    engine, P = school_engine()
    ENGINE, PRICES = engine, P
    FARM = farm_prices()
    rest, hw = load_records()
    rest = attach_urban_status(rest, status)
    counties = sorted(set(hw.county) | set(rest.county.dropna()) - {""})
    near = nearest_fhfa(P)
    urban_tracts = set(status[status.kind.eq("tract2010") & status.urban_fraction.eq(1.0)].record_id)
    upt = urban_price_table(engine, P, counties, near, county_urban_prices(engine, P, urban_tracts))
    farm_rows = farm_price_rows([c for c in counties if c[2:] != "000"], FARM)
    d = value_records(rest, hw, upt, farm_rows, P, engine)
    coef, level, by_method, case = coefficients()
    R = rates()
    d["level"] = d.line.map(level)
    for end in ["low", "high"]:
        d["coef_" + end] = d.line.map(coef[end])
    if d.coef_low.isna().any():
        raise ValueError("[BLOCKED] a land line has no case coefficient")
    paired = d.level.map(R["paired_central"])
    paired_hi = d.level.map(R["paired_high"])
    for k in ["central", "low", "high", "variant_county_avg_urban", "variant_rural_parks_pasture"]:
        g = d["value_" + k] * d.group_ratio
        for end in ["low", "high"]:
            d[f"charge_{k}_{end}"] = g * d["coef_" + end] * R["case"] / 1e9
            d[f"paired_{k}_{end}"] = g * d["coef_" + end] * paired / 1e9
            d[f"pairedhigh_{k}_{end}"] = g * d["coef_" + end] * paired_hi / 1e9
    # Old arm B (public_land) on the same records, for the moved-from report.
    d["value_B_old"] = d.value_B
    for end in ["low", "high"]:
        d[f"charge_oldB_{end}"] = d.group_weighted_value_B.fillna(d.value_B).fillna(0) * d["coef_" + end] * R["case"] / 1e9
    tables(d, coef, level, by_method, R, upt, farm_rows, near)
    cache = HERE / "_cache" / "valued_records.parquet"
    keep = ["record_id", "line", "class", "rule", "county", "tract", "acres", "urban_acres", "rural_acres", "functional_class",
            "price_level", "urban_level", "farm_level", "urban_p24", "farm24", "value_central", "value_low", "value_high", "value_B_old"]
    d[keep].to_parquet(cache, index=False)
    inputs = [PUBLIC / "_cache" / "priced_sites.parquet", PUBLIC / "derived" / "roads_county_acres.csv",
              PUBLIC / "derived" / "case_physical_lines.csv", PUBLIC / "derived" / "case_contract.json", RATE_MODEL,
              SCHOOL / "build.py", ROOT / "scripts" / "estimate_screen.py", classify.OUT]
    write_json(dict(read_only_inputs={str(x.relative_to(ROOT)): classify.sha256(x) for x in inputs},
                    acquired=json.loads((HERE / "_cache" / "acquire_manifest.json").read_text())), "input_provenance.json")
    subprocess.run([sys.executable, "-I", "-m", "pytest", str(HERE / "test_lane.py"), "-q", "-p", "no:cacheprovider"], check=True)
    print(f"  ✓ build {time.perf_counter() - start:.1f}s", flush=True)


def tables(d, coef, level, by_method, R, upt, farm_rows, near):
    rows = []
    for line, g in d.groupby("line", sort=True):
        r = dict(line=line, level=level[line], records=len(g), acres=g.acres.sum(), acres_urban=g.urban_acres.sum(),
                 acres_rural=g.rural_acres.sum(), rule="; ".join(sorted(g.rule.unique())),
                 coef_low=coef.loc[line, "low"], coef_high=coef.loc[line, "high"])
        for k in ["central", "low", "high"]:
            r[f"value_{k}_bn"] = g["value_" + k].sum() / 1e9
        r["value_urban_central_bn"] = g.urban_value_central.sum() / 1e9
        r["value_rural_central_bn"] = g.rural_value_central.sum() / 1e9
        r["value_oldB_bn"] = g.value_B_old.fillna(0).sum() / 1e9
        for k in ["central", "low", "high"]:
            for end in ["low", "high"]:
                r[f"charge_{k}_{end}_bn"] = g[f"charge_{k}_{end}"].sum()
                r[f"paired_{k}_{end}_bn"] = g[f"paired_{k}_{end}"].sum()
        for end in ["low", "high"]:
            r[f"charge_oldB_{end}_bn"] = g[f"charge_oldB_{end}"].sum()
        rows.append(r)
    by = pd.DataFrame(rows)
    write_csv(by, "land_by_line.csv")
    f = pd.DataFrame(FACTOR_SOURCES, columns=["factor", "applies_to", "central", "low", "high", "source_and_page", "cached_source"])
    f.loc[f.factor.eq("farm_land_only_share"), "central"] = FARM["us_share"]
    write_csv(f, "factors.csv")
    write_csv(farm_rows, "county_farm_prices.csv")
    pt = upt.reset_index()[["county", "urban_level", "urban_p24", "urban_tract_p24", "county_p24", "nearest_fhfa_county", "nearest_miles", "nearest_p24", "state_p24"]]
    write_csv(pt, "county_urban_prices.csv")
    summary(d, by, R, near)


def total(d, col, ends=("low", "high")):
    return [float(d[f"{col}_{e}"].sum()) for e in ends]


def summary(d, by, R, near):
    s = {}
    for k in ["central", "low", "high"]:
        s[k] = dict(case_rate_bn=total(d, "charge_" + k), paired_theta_bn=total(d, "paired_" + k),
                    paired_theta_high_d_bn=total(d, "pairedhigh_" + k), national_value_bn=float(d["value_" + k].sum() / 1e9))
    s["old_arm_B_same_records_bn"] = total(d, "charge_oldB")
    # What moved: decompose old B -> new central by record type.
    moved = {}
    fb = d.price_level.eq("state")
    for label, mask in [("state_fallback_records", fb), ("records_with_rural_acres", ~fb & d.rural_acres.gt(0)),
                        ("urban_only_records", ~fb & d.rural_acres.eq(0))]:
        moved[label] = dict(old_B_bn=total(d[mask], "charge_oldB"), new_central_bn=total(d[mask], "charge_central"),
                            acres=float(d.loc[mask, "acres"].sum()))
    s["moved_from_public_land_B"] = moved
    # Screen (thresholds imported from scripts/estimate_screen.py).
    spec = importlib.util.spec_from_file_location("estimate_screen", ROOT / "scripts" / "estimate_screen.py")
    es = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(es)
    central = np.array(s["central"]["case_rate_bn"])
    lo, hi = np.array(s["low"]["case_rate_bn"]), np.array(s["high"]["case_rate_bn"])
    variants = {"central": central, "county_avg_urban_price": np.array(total(d, "charge_variant_county_avg_urban")),
                "rural_parks_at_pasture": np.array(total(d, "charge_variant_rural_parks_pasture"))}
    by_county = d.groupby("county")[["charge_central_low", "charge_central_high"]].sum()
    top = by_county.charge_central_high.sort_values(ascending=False).head(5).index
    drop5 = central - by_county.loc[top].sum().to_numpy()
    fallback_share = float((d.loc[d.urban_level.isin(["nearest_county", "state_unknown_county"]), "charge_central_high"].sum()
                            + d.loc[d.farm_level.eq("state") & d.rural_acres.gt(0), "charge_central_high"].sum()) / central[1])
    stab = pd.DataFrame({"beta": [float(v[1]) for v in variants.values()]})
    ok_s, why_s = es.stability(stab)
    screen = dict(
        thresholds_source="scripts/estimate_screen.py: stability() reused (max/min <= 1.5); influence 25%; data quality CV_SHARE_MAX",
        note="The script's precision and influence tests are written for scaling elasticities (hypotheses 1.0 vs 0.75); their land analogues are stated here.",
        precision=dict(test="cited-factor range excludes zero and its half-width is below the central (the item is distinguishable from no land)",
                       low_bn=lo.tolist(), high_bn=hi.tolist(), half_width_over_central=((hi - lo) / 2 / central).tolist(),
                       passes=bool((lo > 0).all() and ((hi - lo) / 2 < central).all())),
        stability=dict(test="pre-specified constructions: max/min <= 1.5", variants_high_end_bn={k: float(v[1]) for k, v in variants.items()},
                       passes=bool(ok_s), reason=why_s),
        influence=dict(test="dropping the five counties with the largest charges moves the total by <= 25%", top5=list(top),
                       without_top5_bn=drop5.tolist(), moved_share=((central - drop5) / central).tolist(),
                       passes=bool(((central - drop5) / central <= 0.25).all())),
        data_quality=dict(test=f"share of charge on a fallback price (nearest-county urban price, state farmland) <= {es.CV_SHARE_MAX:.0%}",
                          fallback_share=fallback_share, passes=bool(fallback_share <= es.CV_SHARE_MAX)))
    # Beside the test (not its pass rule): the same five counties re-measured with FHFA's county-average price.
    alt = d.county.isin(top)
    alt_total = central - np.array([float(d.loc[alt, f"charge_central_{e}"].sum()) for e in ("low", "high")]) + \
        np.array([float(d.loc[alt, f"charge_variant_county_avg_urban_{e}"].sum()) for e in ("low", "high")])
    screen["influence"]["beside_top5_at_county_average_price_bn"] = alt_total.tolist()
    screen["influence"]["beside_note"] = "re-measuring the five counties' urban price moves the total by this much; the drop-five rule is the screen's"
    screen["passes"] = all(screen[k]["passes"] for k in ["precision", "stability", "influence", "data_quality"])
    s["screen"] = screen
    s["checks"] = checks(d, by)
    roads = d[d.line.isin(CORRIDOR_LINES)]
    s["road_value_by_rule_central_bn"] = {k: float(v / 1e9) for k, v in roads.groupby("rule").value_central.sum().items()}
    s["road_charge_by_rule_central_high_bn"] = {k: float(v) for k, v in roads.groupby("rule").charge_central_high.sum().items()}
    s["top5_counties_share_of_charge"] = float(by_county.loc[top, "charge_central_high"].sum() / central[1])
    s["coverage"] = dict(
        urban_level_acres={k: float(v) for k, v in d.groupby("urban_level").urban_acres.sum().items()},
        farm_level_rural_acres={k: float(v) for k, v in d.groupby("farm_level").rural_acres.sum().items()},
        unpriced_records=int((~d.priced_rule).sum()), unpriced_acres=float(d.loc[~d.priced_rule, "acres"].sum()),
        nearest_fhfa_max_miles_used=float(near.loc[near.index.isin(d.loc[d.urban_level.eq("nearest_county"), "county"]), "nearest_miles"].max()))
    s["rates"] = R
    s["case_key"] = "oct16"
    s["per_line_central_case_rate_bn"] = {r.line: [r.charge_central_low_bn, r.charge_central_high_bn] for r in by.itertuples()}
    s["per_line_range_case_rate_bn"] = {r.line: dict(low=[r.charge_low_low_bn, r.charge_low_high_bn], high=[r.charge_high_low_bn, r.charge_high_high_bn]) for r in by.itertuples()}
    s["per_line_central_paired_bn"] = {r.line: [r.paired_central_low_bn, r.paired_central_high_bn] for r in by.itertuples()}
    s["status"] = "identified" if screen["passes"] else "not identified: " + ", ".join(k for k in ["precision", "stability", "influence", "data_quality"] if not screen[k]["passes"])
    s["frame"] = "beside the adopted case; imputed resource charge, no land depreciation; case coefficients averaged over the two methods as in public_land"
    write_json(s, "summary.json")
    print(json.dumps(dict(central=s["central"]["case_rate_bn"], low=s["low"]["case_rate_bn"], high=s["high"]["case_rate_bn"],
                          paired=s["central"]["paired_theta_bn"], oldB=s["old_arm_B_same_records_bn"], status=s["status"]), indent=1), flush=True)


def checks(d, by):
    """Outside checks; each reports its comparator and whether it passes."""
    c = {}
    case = pd.read_csv(PUBLIC / "derived" / "case_physical_lines.csv")
    st = case.groupby("line").structures_bn.first()
    hw = by[by.line.isin(["hwy_sl", "hwy_fed", "ent_tolls_sl"])]
    c["highway_land_to_structures"] = dict(central=float(hw.value_central_bn.sum() / st[hw.line].sum()),
        low=float(hw.value_low_bn.sum() / st[hw.line].sum()), high=float(hw.value_high_bn.sum() / st[hw.line].sum()),
        structures_bn=float(st[hw.line].sum()), comparator="BEA publishes no highway land; see RESULT for the flow comparator")
    roads = d[d.line.isin(CORRIDOR_LINES)]
    urban = roads[roads.area_type.eq("urban")]
    # GDM price the same FHFA pooled cross-section (2015 prices) at factor 1.0; undo this lane's 2015->2024 carry.
    g = ENGINE.price_rows(pd.Series(sorted(set(urban.county))) + "999999", PRICES)
    g = (g.g_land * g.g_hpi).set_axis(g.tract.str[:5])
    atf24 = urban.urban_acres * urban.urban_p24
    atf15 = atf24 / urban.county.map(g)
    gdm_bn, gdm_acres = 4100.0, 58_000 * 247.105381
    c["urban_road_value_vs_guerra_duranton_ma"] = dict(
        lane_urban_road_acres=float(urban.acres.sum()), lane_atf_2024_bn=float(atf24.sum() / 1e9), lane_atf_2015_prices_bn=float(atf15.sum() / 1e9),
        lane_central_2024_bn=float(urban.value_central.sum() / 1e9),
        lane_atf_2015_per_acre=float(atf15.sum() / urban.acres.sum()),
        comparator="Guerra, Duranton & Ma (2024) NBER w32824 pp.13-16: 58,000 km2 of roadway in 316 PMSAs, FHFA (Davis et al. 2021) as-is pooled cross-section, factor 1.0: $4.1tr, $287,000/acre",
        comparator_bn=gdm_bn, comparator_acres=gdm_acres, comparator_per_acre=287_000.0,
        value_ratio_lane_to_gdm=float(atf15.sum() / 1e9 / gdm_bn), acres_ratio_lane_to_gdm=float(urban.acres.sum() / gdm_acres),
        passes=bool(0.67 <= atf15.sum() / 1e9 / gdm_bn <= 1.5),
        pass_rule="lane ATF at the same 2015 price level within a factor 1.5 of GDM; scopes differ (HPMS urban areas nationally vs 316 PMSAs; design ROW widths vs measured roadway)")
    fw = fhwa_row_share()
    c["fhwa_row_share_of_capital_outlay_2022"] = fw
    per_mile = roads.groupby(["area_type"]).apply(lambda g: pd.Series(dict(miles=g.centerline_miles.sum(), value_bn=g.value_central.sum() / 1e9)), include_groups=False)
    c["value_per_centerline_mile_usd"] = {k: float(r.value_bn * 1e9 / r.miles) for k, r in per_mile.iterrows()}
    c["rural_park_farm_price_vs_timberland"] = dict(
        lane_rural_park_mean_usd_per_acre=float((d.loc[d.line.eq("rec_sl"), "rural_value_central"].sum()) / d.loc[d.line.eq("rec_sl"), "rural_acres"].sum()),
        ncreif_timberland_1q2024_usd_per_acre=2162.0, note="NCREIF includes standing timber")
    return c


if __name__ == "__main__":
    main()
