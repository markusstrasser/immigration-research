"""Land under the oct16 case's public capital lines, r1 corrected after the blind review.

One evaluator prices every record under a configuration. r1's configuration reproduces r1's
$19.74 / 23.68bn exactly; the fixes are applied one at a time, in a stated order, to give
`derived/changes_from_r1.csv`. Rules, factors, sources and pages: `derived/factors.csv` and the RESULT.

Fixes, in the order applied:
1. Water inside park polygons is removed (TIGER 2020 AREAWATER; water.py).
2. Streets of HPMS classes 5-7, parks, airports, plants and sites over two acres (K-12 included) are priced
   as raw land by the residual (subdivision development) method, replacing G&K's 0.65 acreage share:
   raw per gross acre = s·F·(1 − m) − C, floored at 0.10·F; C is calibrated so Maricopa County reproduces
   Munneke, Sirmans & Slade's measured raw/finished ratio 0.262.
3. Serviced sites of two acres or less take the finished-lot (as-is) price × 1.0, replacing 0.80.
4. Land dedicated by subdividers carries no budget cost; BEA's highway stock likewise excludes donated streets.
5. Urban land is priced where the group lives (county Mexican-origin share, ACS 2024 B03001); K-12 keeps its
   where-enrolled weight; rural land stays national.
6. The rate construct stays r × P with expected real land gains at zero (OECD 2009 p.159); g = 1% is the low end.
The price measure stays FHFA's as-is price per acre (Davis et al. 2021 §4.3, the price at the neighbourhood's
lot size); the lot-size-neutral min(as-is, 4 × standardized quarter-acre) is the low end.
Rates: the case's 2.0810698764%, the θ = 0, 0.489, 1 rates of `public_capital_rate_2026_10_24` (d central; hwy_sl at
the highway d), and the adopted bound (θ = 1 at the low end, θ = 0 at the high end; `theta_pairing.bound`).
Range: every factor at its cited low or high end together, with public_land's road width scenarios.

    OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/land_price_rule_r2_2026_10_24/build.py
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

import base  # noqa: E402
import water  # noqa: E402

FISCAL = HERE.parent
ROOT = FISCAL.parent.parent
OUT = HERE / "derived"
RATE_MODEL = FISCAL / "public_capital_rate_2026_10_24" / "derived" / "rate_model.json"
ACS_COUNTY = FISCAL / "school_cost_where_enrolled_2026_09_24" / "_cache" / "acs5_2024_B03001_county.json"
GAZ_TRACTS = base.SCHOOL / "_cache" / "gaz" / "Gaz_tracts_national_2010.zip"
CASE_RATE = 0.020810698764237804

# ------------------------------------------------------------------------------------------ factors
# (central, low-charge end, high-charge end). Sources, pages and quotes: FACTOR_ROWS -> derived/factors.csv.
LOT_SHARE = 0.65                    # NAHB via Gyourko & Krimmel (2021) note 13: the acreage share r1 read as a price
SOFT_MARGIN = 0.304                 # D.S. Thaler pro forma: (290,000 - 90,000 - 111,798) / 290,000
MUNNEKE_RATIO = 74_869 / 285_762    # Munneke, Sirmans & Slade (2023) Table 1: raw / finished $ per acre, Maricopa
CALIBRATION_COUNTY = "04013"        # Maricopa County AZ, the study's market
ENGLOBO_FLOOR = 0.10                # Shinn (2004): raw land 15% of the finished-lot price per lot, x 0.65 lot share
ENGLOBO_LOW_CONST = 0.20            # low end: residual capped at Munneke's ratio at mean parcel sizes (0.19, rounded)
ENGLOBO_HIGH_MIN = 0.46             # high end: at least Munneke's equal-size controlled ratio, e^-0.784
ARTERIAL = (1.0, 1.0, 1.16)         # urban HPMS 1-4 bought from existing parcels; high FTA corridor-sale median
SMALL = (1.0, 1.0, 1.0)             # serviced sites <= 2 acres at the as-is price (the low end caps the price instead)
RURAL = (1.0, 1.0, 1.16)            # county farmland per gross acre; high FTA corridor-sale median
DEDICATED = {                        # share of land dedicated by subdividers (no budget outlay)
    "urban_local": (0.90, 1.00, 0.75),
    "urban_collector": (0.60, 0.85, 0.40),
    "urban_arterial": (0.10, 0.25, 0.0),
    "urban_park": (0.30, 0.50, 0.15),
    "k12": (0.15, 0.30, 0.05),
}
GROWTH = (0.0, 0.010, 0.0)          # expected real land-price growth deducted from r
RENT_YIELD = (0.030, 0.025, 0.045)  # beside arm: market land rent / price
LAND_SHARE_RANGE = (0.691, 0.862)   # r1: ERS historical land share of farm real estate
R1_SUBDIVISION, R1_SMALL = 0.65, 0.80
CALIB = {}                          # C per gross acre, set in prepare()


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


def sha256(path):
    h = hashlib.sha256()
    with Path(path).open("rb") as f:
        while chunk := f.read(1 << 20):
            h.update(chunk)
    return h.hexdigest()


# ------------------------------------------------------------------------------------------ inputs
def std_ratios(d, h):
    """Per record: min(1, 4 × q24 / p24) at the geography that set the record's urban price (low-end cap)."""
    engine, P, upt, status = h["engine"], h["P"], h["upt"], h["status"]
    with zipfile.ZipFile(GAZ_TRACTS) as z:
        g = pd.read_csv(z.open("Gaz_tracts_national.txt"), sep="\t", dtype={"GEOID": str})
    g.columns = [x.strip() for x in g.columns]
    urban = set(status[status.kind.eq("tract2010") & status.urban_fraction.eq(1.0)].record_id)
    g = g[g.GEOID.isin(urban) & g.GEOID.isin(P["xt"].index)][["GEOID", "ALAND"]]
    pr = engine.price_rows(g.GEOID, P).set_index("tract")
    g["p24"], g["q24"] = g.GEOID.map(pr.p24), g.GEOID.map(pr.q24)
    g["county"] = g.GEOID.str[:5]
    g = g[g.p24.gt(0) & g.ALAND.gt(0)]
    g["std24"] = np.minimum(g.p24, 4 * g.q24)
    cu = g.groupby("county").apply(lambda x: np.average(x.std24, weights=x.ALAND) / np.average(x.p24, weights=x.ALAND),
                                   include_groups=False)
    counties = sorted(set(upt.index) | set(upt.nearest_fhfa_county.dropna()))
    cl = engine.price_rows(pd.Series(counties) + "999999", P)
    cl["county"] = cl.tract.str[:5]
    c_own = cl.set_index("county").pipe(lambda x: np.minimum(1.0, 4 * x.q24 / x.p24))
    st = engine.price_rows(pd.Series(sorted(set(d.county.dropna().str[:2]) - {""})) + "000999999", P)
    s_own = st.set_index(st.tract.str[:2]).pipe(lambda x: np.minimum(1.0, 4 * x.q24 / x.p24))
    county_r = pd.Series(np.select([upt.urban_level.eq("urban_tracts"), upt.urban_level.eq("county"), upt.urban_level.eq("nearest_county")],
                                   [upt.index.map(cu), upt.index.map(c_own), upt.nearest_fhfa_county.map(c_own)], np.nan), index=upt.index)
    county_avg_r = pd.Series(np.where(upt.county_p24.notna(), upt.index.map(c_own), upt.nearest_fhfa_county.map(c_own)), index=upt.index)
    r = d.county.map(county_r)
    unknown = d.urban_level.eq("state_unknown_county")
    r[unknown] = d.loc[unknown, "county"].str[:2].map(s_own)
    own_tract = d.tract.notna() & d.p24.notna() & ~d.price_level.eq("state") & ~d["class"].eq("highway")
    tr = engine.price_rows(d.loc[own_tract, "tract"], P).set_index("tract")
    r[own_tract] = d.loc[own_tract, "tract"].map(np.minimum(1.0, 4 * tr.q24 / tr.p24))
    ra = d.county.map(county_avg_r).fillna(r)
    return r.clip(upper=1.0).fillna(1.0), ra.clip(upper=1.0).fillna(1.0)


def location_factors(d):
    """Group residence factor per county: (Mexican-origin share of the county) ÷ (national share)."""
    raw = json.loads(ACS_COUNTY.read_text())
    a = pd.DataFrame(raw[1:], columns=raw[0])
    if "B03001_004E" not in a.columns:
        raise ValueError("[BLOCKED] unexpected ACS B03001 schema")
    a["pop"], a["mex"] = a.B03001_001E.astype(float), a.B03001_004E.astype(float)
    a["fips"] = a.state + a.county
    us_ratio = a.mex.sum() / a["pop"].sum()
    c = a.set_index("fips").pipe(lambda x: x.mex / x["pop"]) / us_ratio
    s = a.groupby("state").apply(lambda x: x.mex.sum() / x["pop"].sum(), include_groups=False) / us_ratio
    loc = d.county.map(c)
    level = pd.Series(np.where(loc.notna(), "county", "state"), index=d.index)
    loc = loc.fillna(d.county.str[:2].map(s)).fillna(1.0)
    return loc, level, dict(us_mexican_origin=float(a.mex.sum()), us_population=float(a["pop"].sum()), acs_counties=int(len(a)),
                            source="ACS 2024 5-year B03001 (001E total, 004E Mexican), county; school_cost_where_enrolled_2026_09_24 cache")


def rates():
    """Case rate, the θ = 0 / 0.489 / 1 rates (d central) and the adopted bound (low end θ = 1, high end θ = 0).

    hwy_sl takes the highway d (federal-aid share 0.425): rate = r_c + d_hwy × (r_i − r_c), the rate model's own rule,
    checked against its stored bound highway rates."""
    rm = json.loads(RATE_MODEL.read_text())
    m, rc, d_hwy = rm["theta_pairing"], rm["r_c"], rm["d_state_local_highways"][1]
    if abs(rc - CASE_RATE) > 1e-15:
        raise ValueError("[BLOCKED] rate model's r_c is not the case rate")
    out = {"case": dict(state_local=CASE_RATE, state_local_hwy=CASE_RATE, federal=CASE_RATE, theta=None)}
    for name, key in [("theta0", "zero"), ("theta0489", "anchor_fg_baseline"), ("theta1", "one")]:
        x = m[key]
        out[name] = dict(state_local=x["d_central"]["rate_state_local"], state_local_hwy=rc + d_hwy * (x["r_i"] - rc),
                         federal=x["d_central"]["rate_federal"], theta=x["theta"])
    b = m["bound"]
    if b["theta_by_end"] != [1.0, 0.0]:
        raise ValueError("[BLOCKED] rate model's bound is no longer θ = 1 low, θ = 0 high")
    out["bound"] = dict(state_local=b["rate_state_local_by_end"], state_local_hwy=b["rate_state_local_highways_by_end"],
                        federal=b["rate_federal_by_end"], theta=b["theta_by_end"])
    for i, (lo_hi, nm) in enumerate([(0, "theta1"), (1, "theta0")]):
        for lv in ["state_local", "state_local_hwy", "federal"]:
            if abs(out["bound"][lv][lo_hi] - out[nm][lv]) > 1e-12:
                raise ValueError(f"[BLOCKED] bound {lv} end {lo_hi} does not equal the {nm} rate")
    # since 1a18b174 the bound prices each line at its own financing level (enterprise, transit, airport, K-12 rates)
    lvl, rbl = b["level_by_component"], b["rate_by_level_by_end"]
    out["bound"]["by_line"] = {c: rbl[l] for c, l in lvl.items()}
    return out


def prepare():
    r1, d, h = base.r1_frame()
    d = d.reset_index(drop=True)
    pw = water.build(d.loc[d["class"].eq("park"), "record_id"])
    d["water_frac"] = d.record_id.map(pw.set_index("record_id").water_frac).fillna(0.0)
    roads = h["roads"]
    hw = d["class"].eq("highway")
    if not np.allclose(d.loc[hw, "acres"].to_numpy(), roads.acres.to_numpy()):
        raise ValueError("[BLOCKED] road records no longer align with roads_county_acres.csv")
    d["width_low"], d["width_high"] = 1.0, 1.0
    d.loc[hw, "width_low"] = (roads.acres_width_low / roads.acres).to_numpy()
    d.loc[hw, "width_high"] = (roads.acres_width_high / roads.acres).to_numpy()
    d["std_ratio"], d["std_ratio_county_avg"] = std_ratios(d, h)
    d["loc"], d["loc_level"], acs = location_factors(d)
    coef, level, _, _ = r1.coefficients()
    d["level"] = d.line.map(level)
    for end in ["low", "high"]:
        d["coef_" + end] = d.line.map(coef[end])
    if d.coef_low.isna().any() or d.level.isna().any():
        raise ValueError("[BLOCKED] a land line has no case coefficient")
    k12 = d.line.eq("k12") & ~d.price_level.eq("state")
    road = d["class"].eq("highway")
    fc = d.functional_class
    d["k12_tract"] = k12
    size = d.site_acres.fillna(d.acres)
    # Price classes: r1's (its small rule read site_acres only) and r2's (site acres, else the record's acres).
    rural_road = road & d.area_type.eq("rural")
    d["class_r1"] = np.select([rural_road, road & fc.le(4), road, d.site_acres.le(2.0)], ["rural_road", "arterial", "large", "small"], "large")
    d["class_r2"] = np.select([rural_road, road & fc.le(4), road, size.le(2.0)], ["rural_road", "arterial", "large", "small"], "large")
    # Dedication happens at subdivision: urban-area streets, parks and school sites; it scales urban acres only.
    d["ded_group"] = np.select([rural_road, road & fc.ge(7), road & fc.between(5, 6), road, d["class"].eq("park"), k12],
                               ["none", "urban_local", "urban_collector", "urban_arterial", "urban_park", "k12"], "none")
    if (d.urban_p24.isna() & d.urban_acres.gt(0) & d.priced_rule).any():
        raise ValueError("[BLOCKED] priced urban acres without a price")
    upt = h["upt"]
    f_cal = float(upt.loc[CALIBRATION_COUNTY, "urban_p24"])
    CALIB.update(county=CALIBRATION_COUNTY, finished_price_per_acre_2024=f_cal,
                 hard_cost_per_gross_acre=f_cal * (LOT_SHARE * (1 - SOFT_MARGIN) - MUNNEKE_RATIO),
                 rule="C = F_Maricopa × (s(1 − m) − 0.262): Maricopa's ratio reproduces Munneke et al.; development cost per "
                      "gross acre carried at FHFA's 2024 Maricopa finished-lot price, so C/F is the study's")
    k = d.k12_tract & d.priced_rule
    dev = (d.loc[k, "value_A"] / (d.loc[k, "acres"] * d.loc[k, "urban_p24"]) - 1).abs()
    CALIB["k12_value_A_vs_acres_times_price_max_rel_dev"] = float(dev.max())
    return r1, d, h, coef, level, acs


# ------------------------------------------------------------------------------------------ evaluator
R1_CFG = dict(water=False, cap=False, englobo="const", englobo_value=R1_SUBDIVISION, small=R1_SMALL, arterial=1.0, rural=1.0,
              share_adj=1.0, k12_mode="r1", classes="class_r1", dedicated=False, ded_idx=0, keying="national", width="central",
              g=0.0, county_avg=False, parks_pasture=False)


def englobo_ratio(F, mode, value=None):
    s1m = LOT_SHARE * (1 - SOFT_MARGIN)
    resid = np.maximum(s1m - CALIB["hard_cost_per_gross_acre"] / F.where(F > 0), ENGLOBO_FLOOR).fillna(ENGLOBO_FLOOR)
    if mode == "const":
        return pd.Series(value, index=F.index)
    if mode == "residual":
        return resid
    if mode == "residual_lo":
        return np.minimum(resid, ENGLOBO_LOW_CONST)
    if mode == "residual_hi":
        return np.maximum(resid, ENGLOBO_HIGH_MIN)
    raise ValueError(mode)


def values(d, cfg):
    """Per record: (urban, rural) national land value and (group-weighted urban, rural) under cfg."""
    wf = (1.0 - d.water_frac) if cfg["water"] else 1.0
    widthf = d["width_" + cfg["width"]] if cfg["width"] != "central" else 1.0
    ua, ra = d.urban_acres * wf * widthf, d.rural_acres * wf * widthf
    p = (d.urban_county_p24 if cfg["county_avg"] else d.urban_p24).fillna(0.0)
    if cfg["cap"]:
        p = p * (d.std_ratio_county_avg if cfg["county_avg"] else d.std_ratio)
    cls = d[cfg["classes"]]
    f = englobo_ratio(p, cfg["englobo"], cfg.get("englobo_value"))
    f = f.where(~cls.eq("small"), cfg["small"]).where(~cls.eq("arterial"), cfg["arterial"]).where(~cls.eq("rural_road"), cfg["rural"])
    if cfg["dedicated"]:
        for k, v in DEDICATED.items():
            f = f.where(~d.ded_group.eq(k), f * (1.0 - v[cfg["ded_idx"]]))
    urban = ua * p * f
    rural_p = d.farm24 * cfg["rural"] * cfg["share_adj"]
    if cfg["parks_pasture"]:
        rural_p = rural_p.where(~d.line.eq("rec_sl"), d.pasture_2024)
    rural = ra * rural_p
    if cfg["k12_mode"] == "r1":
        capped = np.minimum(d.value_B, d.value_A)
        urban = urban.where(~d.k12_tract, capped)
        rural = rural.where(~d.k12_tract, 0.0)
    urban, rural = urban.where(d.priced_rule, 0.0), rural.where(d.priced_rule, 0.0)
    # group_ratio is K-12's where-enrolled weight (1 elsewhere); residence keying reweights urban acres of other lines.
    gu, gr = urban * d.group_ratio, rural * d.group_ratio
    if cfg["keying"] in ("residence", "residence_price"):
        w = d["loc"]
        if cfg["keying"] == "residence_price":
            # acres held at the case's national key per line; only the price follows the group's counties
            m = d.priced_rule & ~d.line.eq("k12")
            a = pd.DataFrame({"line": d.line, "ua": ua.where(m, 0.0), "la": (ua * d["loc"]).where(m, 0.0)}).groupby("line").sum()
            w = w * d.line.map((a.ua / a.la).where(a.la > 0, 1.0))
        gu = gu.where(d.line.eq("k12"), urban * w)
    return urban, rural, gu, gr


def charges(d, cfg, rate):
    """Annual charge per record ($bn) at both ends for one rate dict {state_local, federal}."""
    _, _, gu, gr = values(d, cfg)
    lv = d.level.where(~d.line.eq("hwy_sl"), "state_local_hwy")
    by_line = rate.get("by_line")
    if by_line is not None and not set(d.line).issubset(by_line):
        raise ValueError(f"[BLOCKED] rate model maps no level for {sorted(set(d.line) - set(by_line))}")
    out = {}
    for i, end in enumerate(["low", "high"]):
        if by_line is not None:
            r = d.line.map({k: v[i] for k, v in by_line.items()}) - cfg["g"]
        else:
            at = {k: (v[i] if isinstance(v, list) else v) for k, v in rate.items() if k not in ("theta", "by_line")}
            r = lv.map(at) - cfg["g"]
        out[end] = (gu + gr) * d["coef_" + end] * r / 1e9
    return out


def total(ch):
    return [float(ch["low"].sum()), float(ch["high"].sum())]


def cfg_with(base_cfg, **kw):
    c = dict(base_cfg)
    c.update(kw)
    return c


def r2_cfgs(us_share):
    common = dict(water=True, k12_mode="r2", classes="class_r2", dedicated=True, keying="residence")
    central = cfg_with(R1_CFG, **common, englobo="residual", small=SMALL[0], arterial=ARTERIAL[0], rural=RURAL[0], ded_idx=0, g=GROWTH[0])
    low = cfg_with(R1_CFG, **common, cap=True, englobo="residual_lo", small=SMALL[1], arterial=ARTERIAL[1],
                   rural=RURAL[1], share_adj=LAND_SHARE_RANGE[0] / us_share, ded_idx=1, width="low", g=GROWTH[1])
    high = cfg_with(R1_CFG, **common, englobo="residual_hi", small=SMALL[2], arterial=ARTERIAL[2], rural=RURAL[2],
                    share_adj=LAND_SHARE_RANGE[1] / us_share, ded_idx=2, width="high", g=GROWTH[2])
    return dict(central=central, low=low, high=high)


def rent_rate(y):
    return dict(state_local=y, state_local_hwy=y, federal=y)


# ------------------------------------------------------------------------------------------ outputs
def main():
    start = time.perf_counter()
    OUT.mkdir(exist_ok=True)
    r1, d, h, coef, level, acs = prepare()
    R = rates()
    cfgs = r2_cfgs(r1.FARM["us_share"])
    r1_case = total(charges(d, R1_CFG, R["case"]))
    r1_ref = json.loads((base.R1_DIR / "derived" / "summary.json").read_text())["central"]["case_rate_bn"]
    if not np.allclose(r1_case, r1_ref, rtol=1e-9):
        raise ValueError(f"[BLOCKED] r1 configuration gives {r1_case}, r1 published {r1_ref}")
    changes = change_table(d, cfgs, R)
    by = line_table(d, cfgs, R, coef, level)
    write_csv(by, "land_by_line.csv")
    write_csv(changes, "changes_from_r1.csv")
    write_csv(factor_table(r1.FARM["us_share"]), "factors.csv")
    summary(d, by, cfgs, R, changes, r1_case, acs, h)
    inputs = [base.R1_DIR / "build.py", base.R1_DIR / "_cache" / "valued_records.parquet", base.PUBLIC / "_cache" / "priced_sites.parquet",
              base.PUBLIC / "derived" / "roads_county_acres.csv", base.PUBLIC / "derived" / "case_physical_lines.csv",
              base.PUBLIC / "derived" / "case_contract.json", RATE_MODEL, ACS_COUNTY, base.SCHOOL / "build.py",
              ROOT / "scripts" / "estimate_screen.py", water.OUT]
    write_json(dict(read_only_inputs={str(x.relative_to(ROOT)): sha256(x) for x in inputs},
                    areawater_counties=len(json.loads(water.MANIFEST.read_text())["inputs"]["areawater"]),
                    areawater_url_pattern=water.URL), "input_provenance.json")
    subprocess.run([sys.executable, "-I", "-m", "pytest", str(HERE / "test_lane.py"), "-q", "-p", "no:cacheprovider"], check=True)
    print(f"  ✓ build {time.perf_counter() - start:.1f}s", flush=True)


def change_table(d, cfgs, R):
    """Apply the fixes in order from r1's configuration; each row is the step's effect at the case rate."""
    c = cfgs["central"]
    steps = [
        ("0_r1", "r1 as published", {}),
        ("1_water", "remove TIGER area water from park pieces", dict(water=True)),
        ("2_englobo", "raw land by the residual method (streets 5-7, parks, sites > 2 acres incl. K-12) replaces the 0.65 acreage share",
         dict(englobo="residual", k12_mode="r2", classes="class_r2", small=R1_SMALL)),
        ("3_small_sites", "serviced sites <= 2 acres at the as-is price × 1.0 (replaces 0.80)", dict(small=SMALL[0])),
        ("4_dedication", "land dedicated by subdividers carries no budget cost", dict(dedicated=True, ded_idx=0)),
        ("5_location", "urban land weighted by the group's county of residence (K-12 keeps where-enrolled)", dict(keying="residence")),
        ("6_rate_construct", "r × P with expected real land gains at zero (OECD 2009 p.159): no change", dict(g=GROWTH[0])),
    ]
    cfg = dict(R1_CFG)
    rows, prev = [], None
    for key, what, kw in steps:
        cfg.update(kw)
        t = total(charges(d, cfg, R["case"]))
        rows.append(dict(step=key, change=what, cumulative=True, case_rate_low_bn=t[0], case_rate_high_bn=t[1],
                         delta_low_bn=t[0] - prev[0] if prev else 0.0, delta_high_bn=t[1] - prev[1] if prev else 0.0))
        prev = t
    if cfg != c:
        raise ValueError(f"[BLOCKED] change chain does not end at the central configuration: {set(k for k in c if c[k] != cfg[k])}")
    beside = [
        ("b_price_cap", "price capped at the lot-size-neutral min(as-is, 4 × quarter-acre standardized)", cfg_with(c, cap=True), R["case"]),
        ("b_englobo_const_020", "englobo constant 0.20 (Phoenix ratio transported)", cfg_with(c, englobo="const", englobo_value=ENGLOBO_LOW_CONST), R["case"]),
        ("b_englobo_min_046", "englobo at least 0.46 (equal-size controlled ratio)", cfg_with(c, englobo="residual_hi"), R["case"]),
        ("b_no_dedication", "resource view: dedicated land charged like bought land", cfg_with(c, dedicated=False), R["case"]),
        ("b_national_keying", "every line keyed nationally (r1's keying)", cfg_with(c, keying="national"), R["case"]),
        ("b_residence_price_only", "urban acres held at the national key per line, price at the group's counties",
         cfg_with(c, keying="residence_price"), R["case"]),
        ("b_growth_1pct", "(r - g) × P with g = 1.0% real", cfg_with(c, g=0.010), R["case"]),
        ("b_rent_3pct", "market land rent 3.0% of price (resource/rental view)", c, rent_rate(RENT_YIELD[0])),
        ("b_rent_2_5pct", "market land rent 2.5% of price", c, rent_rate(RENT_YIELD[1])),
        ("b_rent_4_5pct", "market land rent 4.5% of price", c, rent_rate(RENT_YIELD[2])),
        ("b_width_low", "public_land lower design widths", cfg_with(c, width="low"), R["case"]),
        ("b_width_high", "public_land upper design widths", cfg_with(c, width="high"), R["case"]),
        ("b_rate_theta0", "θ = 0 rates", c, R["theta0"]),
        ("b_rate_theta0489", "θ = 0.489 rates (anchor)", c, R["theta0489"]),
        ("b_rate_theta1", "θ = 1 rates", c, R["theta1"]),
        ("b_rate_bound", "adopted bound rates: θ = 1 at the low end, θ = 0 at the high end", c, R["bound"]),
        ("b_bound_residence_price_only", "adopted bound rates, urban acres at the national key, price at the group's counties",
         cfg_with(c, keying="residence_price"), R["bound"]),
    ]
    for key, what, cf, rate in beside:
        t = total(charges(d, cf, rate))
        rows.append(dict(step=key, change=what + " (beside the central, not cumulative)", cumulative=False,
                         case_rate_low_bn=t[0], case_rate_high_bn=t[1], delta_low_bn=t[0] - prev[0], delta_high_bn=t[1] - prev[1]))
    return pd.DataFrame(rows)


def line_table(d, cfgs, R, coef, level):
    rows = []
    vals = {k: values(d, c) for k, c in cfgs.items()}
    chg = {(k, rn): charges(d, c, R[rn]) for k, c in cfgs.items() for rn in R}
    extra = {"growth1pct": charges(d, cfg_with(cfgs["central"], g=0.010), R["case"]),
             "rent3pct": charges(d, cfgs["central"], rent_rate(RENT_YIELD[0])),
             "national_keying": charges(d, cfg_with(cfgs["central"], keying="national"), R["case"]),
             "residence_price_only": charges(d, cfg_with(cfgs["central"], keying="residence_price"), R["case"]),
             "bound_residence_price_only": charges(d, cfg_with(cfgs["central"], keying="residence_price"), R["bound"]),
             "no_dedication": charges(d, cfg_with(cfgs["central"], dedicated=False), R["case"]),
             "r1": charges(d, R1_CFG, R["case"])}
    for line, idx in d.groupby("line", sort=True).groups.items():
        g = d.loc[idx]
        r = dict(line=line, level=level[line], records=len(g), acres=g.acres.sum(),
                 acres_urban=(g.urban_acres * (1 - g.water_frac)).sum(), acres_rural=(g.rural_acres * (1 - g.water_frac)).sum(),
                 water_acres_removed=((g.urban_acres + g.rural_acres) * g.water_frac).sum(),
                 rule="; ".join(sorted(set(g.class_r2) | set(g.ded_group) - {"none"})), coef_low=coef.loc[line, "low"], coef_high=coef.loc[line, "high"])
        for k in ["central", "low", "high"]:
            u, ru, gu, gr = vals[k]
            r[f"value_{k}_bn"] = (u[idx] + ru[idx]).sum() / 1e9
            r[f"group_weighted_value_{k}_bn"] = (gu[idx] + gr[idx]).sum() / 1e9
        r["value_urban_central_bn"] = vals["central"][0][idx].sum() / 1e9
        r["value_rural_central_bn"] = vals["central"][1][idx].sum() / 1e9
        for k in ["central", "low", "high"]:
            for rn in R:
                for end in ["low", "high"]:
                    r[f"charge_{k}_{end}_bn" if rn == "case" else f"{rn}_{k}_{end}_bn"] = chg[(k, rn)][end][idx].sum()
        for name, ch in extra.items():
            for end in ["low", "high"]:
                r[f"{name}_central_{end}_bn" if name != "r1" else f"charge_r1_{end}_bn"] = ch[end][idx].sum()
        rows.append(r)
    return pd.DataFrame(rows)


def factor_table(us_share):
    rows = [
        ("englobo_lot_share_s", "residual method: lot share of a subdivision's gross area", LOT_SHARE, LOT_SHARE, LOT_SHARE,
         "Gyourko & Krimmel (2021) NBER w28993 note 13 and p.16, citing NAHB (the acreage share r1 used as a price)", "note 13, p.16",
         "about 65% of the acreage was taken up by housing, with the rest used for other purposes (e.g., roads, parks, public facilities)"),
        ("englobo_soft_margin_m", "residual method: soft costs, carry and profit as a share of finished-lot revenue", SOFT_MARGIN, SOFT_MARGIN, SOFT_MARGIN,
         "D.S. Thaler & Assoc., Fundamentals of Land Development (2017), Developer's Pro Forma: lot 290,000, hard costs 90,000, land offer 111,798",
         "slide p.13", "Finished lot sales price 290,000 ... Land development - hard costs 90,000 ... Total Offer 111,798"),
        ("englobo_calibration_ratio", "raw/finished $ per acre, Maricopa County 1998-2012 (C calibrated to it)", MUNNEKE_RATIO, ENGLOBO_LOW_CONST, ENGLOBO_HIGH_MIN,
         "Munneke, Sirmans & Slade, Land Prices and the Development Process, JREFE 71 (2025; online 2023) doi 10.1007/s11146-023-09959-8; "
         "low end min(residual, 0.20) (0.19 at mean parcel sizes, Table 2 Model 2.2), high end max(residual, 0.46) (equal-size, e^-0.784)",
         "Table 1 (~p.78); Table 2", "Finished lots sell at 3.8 times the price per acre of raw land"),
        ("englobo_floor", "lowest raw/finished ratio", ENGLOBO_FLOOR, ENGLOBO_FLOOR, ENGLOBO_FLOOR,
         "Shinn, Land Acquisition, Professional Builder (Jul 2004): raw land 15% of the retail finished-lot price, × 0.65 lot share", "web",
         "At 20 percent for finished lots, the price of raw land should be 3 percent of the home price, or 15 percent of the retail lot price."),
        ("urban_arterial", "urban HPMS 1-4, bought from existing parcels at their as-is price", *ARTERIAL,
         "FTA, Valuation of Railroad Right of Way (rev. Jan 2017) p.13 straight ATF; high p.11 corridor-sale median 1.158", "pp.11, 13",
         "the proper methodology would be the basic across the fence approach"),
        ("small_site", "built-up sites and schools of 2 acres or less: serviced lots at the as-is price", *SMALL,
         "Davis, Larson, Oliner & Shui (2021) FHFA WP 19-01 §4.3: as-is values for accounting; low end caps the price (row price_measure)", "§4.3 p.14",
         "many accounting exercises require actual, as opposed to standardized, land values"),
        ("price_measure", "FHFA as-is $/acre (central, high); min(as-is, 4 × standardized quarter-acre) at the low end", 1.0, 0.0, 1.0,
         "Davis, Larson, Oliner & Shui (2021) FHFA WP 19-01 §4.2-4.3 and note 28 (plattage)", "pp.11-14",
         "due to plattage effects the value of a single quarter-acre lot is much less than the value of, say, four lots of 1/16 acre each"),
        ("rural", "rural acres of every line at county farmland value", *RURAL, "r1 factor; FTA (2017) p.11 corridor-sale median 1.158 as the high end",
         "p.11", "the transaction average was calculated as 1.171, with the median as 1.158"),
        ("farm_land_only_share", "land share of Census of Agriculture land and buildings", us_share, *LAND_SHARE_RANGE,
         "r1: NASS Land Values 2024 Summary p.20; ERS AR-26 (1992) p.5 (buildings 18.7%); range ERS historical 13.8-30.9%", "p.20; p.5",
         "Farm building values ... represented 18.7 percent of the total value of farmland and buildings"),
        ("expected_real_land_growth_g", "deducted from every rate: (r - g) × P", *GROWTH,
         "OECD, Measuring Capital (2009) §18.1.2 and eq. 30; low end g = 1.0% from long-run US real house-price growth "
         "(Jordà et al. 2019 Table IX 0.90%; Knoll, Schularick & Steger 2017: +150% real 1890-2012, 0.75%/yr)", "pp.157-159; p.40",
         "the expected real holding gains and losses for land should be set to equal zero when user costs for land are calculated"),
        ("rent_yield_beside", "beside arm: annual land rent ÷ price", *RENT_YIELD,
         "NASS Land Values and Cash Rents 2024 Highlights ($160 cropland rent) over NASS Land Values 2024 Summary ($5,570): 2.87%; non-irrigated 3.04%",
         "Highlights p.1; Summary p.4", "At $160 per acre, the average rate to rent cropland in the United States in 2024"),
    ]
    quotes = {
        "urban_local": ("R. Marlin Smith, Law & Contemp. Probs. 50(1) 1987 pp.5-6 [page UNVERIFIED]; Ridgefield Land Co. v. Detroit, 241 Mich. 468 (1928)",
                        "the owner of a subdivision voluntarily dedicates sufficient land for streets in return for the advantage and privilege of having his plat recorded"),
        "urban_collector": ("Bauman & Ethier, Law & Contemp. Probs. 50(1) 1987 pp.53-54 [page UNVERIFIED]: on-site road dedication in 60.1% of exacting communities",
                            "both off-site and on-site dedications are required more often for roads (28.0% and 60.1%, respectively) than for any other purpose"),
        "urban_arterial": ("[INFERENCE] half-street dedications at plat approval; most arterial ROW bought by highway agencies (FHWA SF-12A ROW outlays)", ""),
        "urban_park": ("Ben-Joseph (2003) Lincoln Institute WP, Land Dedication section: 63% of jurisdictions (1976) to 81% (2002), typically 6-25% of area",
                       "In 1976, 63 percent of municipalities surveyed had some form of land dedication requirements"),
        "k12": ("Bauman & Ethier (1987): on-site school exactions in 26.8% of exacting communities; Shultz & Kelley (1985) [page UNVERIFIED]",
                "Governments enacted laws requiring developers to dedicate land to the city for parks and school sites"),
    }
    for k, v in DEDICATED.items():
        src, q = quotes[k]
        rows.append(("dedicated_share_" + k, f"share of {k} land dedicated by subdividers (budget cost 0); national stock share is [INFERENCE]",
                     *v, src, "see research_dedication_englobo.md A2", q))
    return pd.DataFrame(rows, columns=["factor", "applies_to", "central", "low_charge_end", "high_charge_end", "source", "page", "quote"])


def summary(d, by, cfgs, R, changes, r1_case, acs, h):
    s = {"case_key": "oct16", "r1_reproduced_case_rate_bn": r1_case, "calibration": CALIB}
    for k in ["central", "low", "high"]:
        s[k] = {rn: total(charges(d, cfgs[k], R[rn])) for rn in R}
        s[k]["national_value_bn"] = float(sum(x.sum() for x in values(d, cfgs[k])[:2]) / 1e9)
    s["rates"] = R
    s["beside_central"] = {r.step: [r.case_rate_low_bn, r.case_rate_high_bn] for r in changes[~changes.cumulative].itertuples()}
    s["per_line_central_case_rate_bn"] = {r.line: [r.charge_central_low_bn, r.charge_central_high_bn] for r in by.itertuples()}
    s["per_line_range_case_rate_bn"] = {r.line: dict(low=[r.charge_low_low_bn, r.charge_low_high_bn], high=[r.charge_high_low_bn, r.charge_high_high_bn])
                                        for r in by.itertuples()}
    s["per_line_central_by_rate_bn"] = {r.line: {rn: [getattr(r, "charge_central_low_bn" if rn == "case" else f"{rn}_central_low_bn"),
                                                       getattr(r, "charge_central_high_bn" if rn == "case" else f"{rn}_central_high_bn")] for rn in R}
                                        for r in by.itertuples()}
    s["changes_from_r1_case_rate_bn"] = changes[changes.cumulative][["step", "case_rate_low_bn", "case_rate_high_bn", "delta_low_bn", "delta_high_bn"]].to_dict("records")
    s["screen"] = screen(d, cfgs, R, "bound")
    s["screen_case_rate"] = screen(d, cfgs, R, "case")
    s["checks"] = checks(d, cfgs, h)
    s["top_records_r1_vs_r2"] = top_records(d, cfgs)
    ch = charges(d, cfgs["central"], R["case"])["high"]
    s["location"] = dict(acs, charge_share_by_factor_level={k: float(v) for k, v in (ch.groupby(d.loc_level).sum() / ch.sum()).items()})
    st = s["screen"]
    s["status"] = "identified" if st["passes"] else "not identified: " + ", ".join(k for k in ["precision", "stability", "influence", "data_quality"] if not st[k]["passes"])
    s["frame"] = ("beside the adopted case; budget-cost land charge r × P on land a budget bought: as-is FHFA prices, raw land by the residual "
                  "method for large sites and subdivision streets, dedicated land at zero, county farmland for rural acres, urban land weighted "
                  "by the group's county of residence; case coefficients averaged over the two methods as in public_land")
    write_json(s, "summary.json")
    print(json.dumps(dict(central=s["central"]["case"], low=s["low"]["case"], high=s["high"]["case"], bound=s["central"]["bound"],
                          r1=r1_case, status=s["status"]), indent=1), flush=True)


def screen(d, cfgs, R, rn="case"):
    spec = importlib.util.spec_from_file_location("estimate_screen", ROOT / "scripts" / "estimate_screen.py")
    es = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(es)
    c = cfgs["central"]
    ch = charges(d, c, R[rn])
    central = np.array(total(ch))
    lo, hi = np.array(total(charges(d, cfgs["low"], R[rn]))), np.array(total(charges(d, cfgs["high"], R[rn])))
    variants = {"central": central,
                "county_avg_urban_price": np.array(total(charges(d, cfg_with(c, county_avg=True), R[rn]))),
                "rural_parks_at_pasture": np.array(total(charges(d, cfg_with(c, parks_pasture=True), R[rn]))),
                "national_keying": np.array(total(charges(d, cfg_with(c, keying="national"), R[rn])))}
    ok_s, why_s = es.stability(pd.DataFrame({"beta": [float(v[1]) for v in variants.values()]}))
    by_county = pd.DataFrame({"low": ch["low"], "high": ch["high"], "county": d.county}).groupby("county")[["low", "high"]].sum()
    top = by_county.high.sort_values(ascending=False).head(5).index
    drop5 = central - by_county.loc[top].sum().to_numpy()
    alt = d.county.isin(top)
    ca = charges(d, cfg_with(c, county_avg=True), R[rn])
    reprice = central - np.array([ch[e][alt].sum() for e in ("low", "high")]) + np.array([ca[e][alt].sum() for e in ("low", "high")])
    chn = charges(d, cfg_with(c, keying="national"), R[rn])
    bcn = pd.DataFrame({"low": chn["low"], "high": chn["high"], "county": d.county}).groupby("county")[["low", "high"]].sum()
    topn = bcn.high.sort_values(ascending=False).head(5).index
    nat_moved = (bcn.loc[topn].sum() / bcn.sum()).to_numpy()
    top_shares = (by_county.loc[top, "high"] / central[1]).round(6).to_dict()
    fb = d.urban_level.isin(["nearest_county", "state_unknown_county"]) | (d.farm_level.eq("state") & d.rural_acres.gt(0))
    fallback_share = float(ch["high"][fb].sum() / central[1])
    prec = bool((lo > 0).all() and ((hi - lo) / 2 < central).all())
    infl = bool(((central - drop5) / central <= 0.25).all())
    dq = bool(fallback_share <= es.CV_SHARE_MAX)
    return dict(
        rate=rn,
        thresholds_source="scripts/estimate_screen.py: stability() reused (max/min <= 1.5); influence 25%; data quality CV_SHARE_MAX",
        precision=dict(test="cited-factor range excludes zero and its half-width is below the central", low_bn=lo.tolist(), high_bn=hi.tolist(),
                       half_width_over_central=((hi - lo) / 2 / central).tolist(), passes=prec),
        stability=dict(test="pre-specified constructions: max/min <= 1.5", variants_high_end_bn={k: float(v[1]) for k, v in variants.items()},
                       passes=bool(ok_s), reason=why_s),
        influence=dict(test="drop the five counties with the largest charges; moves <= 25% (the standing rule; the sum decision of 2026-10-24 is reopened)",
                       top5=list(top), without_top5_bn=drop5.tolist(), moved_share=((central - drop5) / central).tolist(),
                       top5_share_of_charge=float(by_county.loc[top, "high"].sum() / central[1]), top5_county_shares_high_end=top_shares,
                       beside_national_keying_top5=list(topn), beside_national_keying_drop5_moved_share=nat_moved.tolist(), passes=infl,
                       beside_reprice_top5_county_average_bn=reprice.tolist(), beside_reprice_moved_share=(np.abs(reprice - central) / central).tolist(),
                       beside_note="decisions/2026-10-24-influence-test-for-sums.md repricing test, reopened the same day: reported, not the pass rule"),
        data_quality=dict(test=f"share of charge on a fallback price <= {es.CV_SHARE_MAX:.0%}", fallback_share=fallback_share, passes=dq),
        passes=bool(prec and ok_s and infl and dq))


def top_records(d, cfgs):
    r1u, r1r, _, _ = values(d, R1_CFG)
    u, ru, _, _ = values(d, cfgs["central"])
    lu, lr, _, _ = values(d, cfgs["low"])
    cu, cr, _, _ = values(d, cfg_with(cfgs["central"], cap=True))
    t = pd.DataFrame({"record_id": d.record_id, "line": d.line, "county": d.county, "acres": d.acres, "water_frac": d.water_frac,
                      "urban_p24": d.urban_p24, "std_ratio": d.std_ratio, "class_r2": d.class_r2, "ded_group": d.ded_group,
                      "value_r1_bn": (r1u + r1r) / 1e9, "value_r2_central_bn": (u + ru) / 1e9, "value_r2_low_bn": (lu + lr) / 1e9,
                      "value_r2_central_price_capped_bn": (cu + cr) / 1e9})
    return t.sort_values("value_r1_bn", ascending=False).head(5).to_dict("records")


def checks(d, cfgs, h):
    c = {}
    u, ru, _, _ = values(d, cfgs["central"])
    nd_u, _, _, _ = values(d, cfg_with(cfgs["central"], dedicated=False))
    roads = d["class"].eq("highway")
    urban_roads = roads & d.area_type.eq("urban")
    engine, P = h["engine"], h["P"]
    g = engine.price_rows(pd.Series(sorted(set(d.loc[urban_roads, "county"]))) + "999999", P)
    carry = (g.g_land * g.g_hpi).set_axis(g.tract.str[:5])
    atf24 = d.urban_acres * d.urban_p24
    atf15 = (atf24 / d.county.map(carry))[urban_roads]
    c["urban_road_value_vs_guerra_duranton_ma"] = dict(
        lane_urban_road_acres=float(d.loc[urban_roads, "acres"].sum()), comparator_acres=58_000 * 247.105381,
        lane_atf_2015_prices_bn=float(atf15.sum() / 1e9), comparator_bn=4100.0, value_ratio=float(atf15.sum() / 1e9 / 4100.0),
        lane_atf_2015_per_acre=float(atf15.sum() / d.loc[urban_roads, "acres"].sum()), comparator_per_acre=287_000.0,
        lane_r2_central_2024_bn=float(u[urban_roads].sum() / 1e9), lane_r2_no_dedication_2024_bn=float(nd_u[urban_roads].sum() / 1e9),
        comparator="Guerra, Duranton & Ma (2024) NBER w32824 pp.13-16: 58,000 km2 of roadway in 316 PMSAs at FHFA as-is prices, factor 1.0: $4.1tr",
        note="GDM value land at full ATF regardless of who paid; the r2 central prices only budget-bought land, as raw land where it was subdivided")
    case = pd.read_csv(base.PUBLIC / "derived" / "case_physical_lines.csv")
    st = case.groupby("line").structures_bn.first()
    v = (u + ru).groupby(d.line).sum() / 1e9
    lines = [x for x in v.index if x in st.index]
    c["land_to_structures"] = dict(all_lines=float(v[lines].sum() / st[lines].sum()),
                                   roads=float(v[[x for x in ["hwy_sl", "hwy_fed", "ent_tolls_sl"] if x in lines]].sum() /
                                               st[[x for x in ["hwy_sl", "hwy_fed", "ent_tolls_sl"] if x in lines]].sum()),
                                   structures_bn=float(st[lines].sum()),
                                   comparator="FHFA national land share of single-family property value 0.356 (xs_nation.csv), land/structures 0.55; "
                                              "BEA publishes no government land")
    man = d.county.eq("36061") & d.urban_acres.gt(0)
    barr = 1_740e9 / (0.6 * 14_528)
    c["manhattan_vs_barr_smith_kulkarni"] = dict(
        lane_as_is_price_per_acre_2024_acre_weighted=float(np.average(d.loc[man, "urban_p24"], weights=d.loc[man, "urban_acres"])),
        comparator_per_developable_acre_2014=barr, comparator_bn_2014=1740.0, comparator_developable_acres=0.6 * 14_528,
        comparator="Barr, Smith & Kulkarni, What's Manhattan Worth? (Oct 2015) p.15: 'the value of developable land in 2014 on Manhattan "
                   "was about $1,740 billion'; pp.13-14: 0.6 of Manhattan's 14,528 acres developable; vacant-land sales, all uses",
        note="FHFA's residential as-is price is about half the all-use vacant-land price per developable acre: as-is is not inflated here")
    c["park_water_acres_removed"] = float(((d.urban_acres + d.rural_acres) * d.water_frac)[d["class"].eq("park")].sum())
    wu, wr, _, _ = values(d, cfg_with(R1_CFG, water=True))
    ou, orr, _, _ = values(d, R1_CFG)
    c["park_water_value_removed_bn_at_r1_rules"] = float(((ou + orr) - (wu + wr)).sum() / 1e9)
    c["park_water_vintage_2021_counties"] = json.loads(water.MANIFEST.read_text())["inputs"]["vintage_2021"]
    c["park_pieces_with_water"] = int((d.water_frac > 0).sum())
    c["park_unclipped_tract_max_water_share"] = water.WATER_MIN
    c["englobo_ratio_distribution_central_large_urban"] = {
        q: float(v) for q, v in englobo_ratio(d.urban_p24.fillna(0.0), "residual")[d.class_r2.eq("large") & d.urban_acres.gt(0)].quantile([0.1, 0.5, 0.9]).items()}
    return c


if __name__ == "__main__":
    main()
