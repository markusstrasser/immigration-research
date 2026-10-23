"""Market value of the land under US public K-12 schools, and the group's annual charge on it.

Pipeline (all inputs parsed from the primary files acquire.py / acquire_overture.py / fhfa_extract.py fetched):
1. Universe: 99,297 operating CCD schools 2023-24 with EDGE points (schools.py). Exclusively virtual
   schools carry no land.
2. Campuses: Overture 2026-10-21.0 land_use polygons (OSM-derived) of class school, kindergarten and
   schoolyard; polygons that intersect are merged into one campus (union-find, geodesic area of the
   union). Class 'education' (landuse=education) polygons are a fallback container only.
3. Matching: a school point inside a campus matches it; otherwise the nearest campus within 60 m, or
   within 200 m when a distinctive name token is shared, matches unless the campus is tagged private or
   religious. A campus with several matched schools splits its land by K-12 pupils.
4. Unmatched schools: acreage imputed from a log-acres regression fitted on sole-occupant matched
   schools (level, type, charter, log pupils, NCES locale, state), Duan smearing.
5. Price: each campus (point on surface) or unmatched school point gets its 2010 tract. FHFA WP 19-01
   v4.0 pooled cross-section, tract "as-is" residential land value per acre at 2015 prices, falling back
   to county then state; carried to 2022 by the county (else state) annual panel ratio of as-is per acre
   2022/2015, and to 2024 by FHFA's annual county all-transactions HPI 2024/2022 (else state median).
   Arms: A residential (all acres at the tract price, an upper reference); B developable share (0.65 of
   acres for sites over 2 acres, 0.80 below; NAHB median subdivision via Gyourko & Krimmel 2021), the
   central; C vacant-land plattage (Albouy, Ehrlich & Shin 2018 Table A.1 cubic in log lot size, from
   the tract's average lot to the campus acreage), a lower reference; D FHFA's county lot-size
   elasticity bL (beside).
6. Group: the where-enrolled lane's district weights (Hispanic K-12 pupils x the district's raked
   Mexican share, weighting.py) carried to schools by each school's Hispanic K-12 pupils.
7. Validation: California School Campus Database 2025 (parcel-aligned campus polygons) against the
   lane's California acreage, school by school and in total; it also tests the imputation.

Writes derived/*.csv (LF) and derived/summary.json.

    OPENBLAS_NUM_THREADS=1 uv run --no-project --with duckdb python3 infra/immigration-fiscal/school_land_2026_10_24/build.py
"""
import importlib.util
import json
import math
import re
import sys
import zipfile
from pathlib import Path

sys.dont_write_bytecode = True
import duckdb  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import schools  # noqa: E402

FISCAL = HERE.parent
CACHE = HERE / "_cache"
OUT = HERE / "derived"
POLY = CACHE / "overture" / "us_education_2026-10-21.0.parquet"
FHFA = CACHE / "fhfa" / "csv"
HPI = CACHE / "hpi" / "hpi_at_county.xlsx"
TRACTS = sorted((CACHE / "tracts2010").glob("gz_2010_*_140_00_500k.zip"))
CSCD = CACHE / "bench_cscd"
ACRE = 4046.8564224
NEAR_ANY_M, NEAR_NAME_M = 60.0, 200.0
DEV_SHARE_LARGE, DEV_SHARE_SMALL, DEV_SMALL_ACRES = 0.65, 0.80, 2.0   # G&K 2021 pp. 14-16 (NAHB)
AES = (-0.543, -3.053 / 100, 3.601 / 1000)     # AES 2018 Table A.1: log lot size, ^2/100, ^3/1000
CAPITAL = FISCAL / "school_capital_return_2026_09_26" / "derived" / "summary.json"
CASE = FISCAL / "main_case_2026_10_16" / "derived" / "summary.json"
WEIGHTING = FISCAL / "school_cost_where_enrolled_2026_09_24" / "weighting.py"
RATES = {"case_flat_real": None, "omb_2003_3pct": 0.03, "omb_2003_7pct": 0.07}
STOP = {"school", "schools", "elementary", "elem", "el", "es", "middle", "ms", "high", "hs", "junior", "jr", "senior",
        "sr", "the", "of", "and", "at", "academy", "public", "community", "center", "centre", "charter", "magnet",
        "primary", "intermediate", "k", "8", "k8", "12", "k12", "sch", "campus", "learning", "school", "upper",
        "lower", "early", "childhood", "education", "educational", "st", "saint", "preparatory", "prep", "unified",
        "district", "county", "city", "program", "programs", "alternative", "international"}


def _ok(m):
    print(f"  ✓ {m}", flush=True)


def tokens(s):
    return {t for t in re.findall(r"[a-z0-9]+", str(s).lower()) if t not in STOP and len(t) > 1}


def aes_f(x):
    return AES[0] * x + AES[1] * x ** 2 + AES[2] * x ** 3


# ---------------------------------------------------------------------------------------------- campuses
def campuses(c):
    c.execute(f"""CREATE TABLE p AS SELECT row_number() OVER (ORDER BY id) - 1 AS pid, * EXCLUDE (wkb),
                  ST_MakeValid(ST_GeomFromWKB(wkb)) AS g FROM read_parquet('{POLY}')""")
    # Candidate pairs by 0.02-degree grid cell, then exact intersection (a plain self-join on
    # ST_Intersects ran over ten minutes; the grid takes under a second).
    c.execute("""CREATE TABLE cells AS SELECT pid, cx, cy FROM p,
                 range(floor(xmin / 0.02)::BIGINT, floor(xmax / 0.02)::BIGINT + 1) AS rx(cx),
                 range(floor(ymin / 0.02)::BIGINT, floor(ymax / 0.02)::BIGINT + 1) AS ry(cy)
                 WHERE class <> 'education'""")
    pairs = c.execute("""SELECT DISTINCT a.pid, b.pid FROM cells a JOIN cells b ON a.cx = b.cx AND a.cy = b.cy AND a.pid < b.pid
                         JOIN p pa ON pa.pid = a.pid JOIN p pb ON pb.pid = b.pid
                         WHERE pa.xmin <= pb.xmax AND pb.xmin <= pa.xmax AND pa.ymin <= pb.ymax AND pb.ymin <= pa.ymax
                           AND ST_Intersects(pa.g, pb.g) ORDER BY 1, 2""").fetchall()
    pol = c.execute("SELECT pid, class FROM p ORDER BY pid").df()
    parent = np.arange(len(pol))

    def find(i):
        while parent[i] != i:
            parent[i] = parent[parent[i]]
            i = parent[i]
        return i
    for a, b in pairs:
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[max(ra, rb)] = min(ra, rb)
    pol["campus"] = [find(i) for i in range(len(pol))]
    pol.loc[pol["class"].eq("education"), "campus"] = -1 - pol.pid[pol["class"].eq("education")]
    c.register("pc", pol[["pid", "campus"]])
    c.execute("""CREATE TABLE camp AS
                 SELECT pc.campus, count(*) AS n_polys,
                        CASE WHEN count(*) = 1 THEN any_value(p.area_m2) ELSE ST_Area_Spheroid(ST_Union_Agg(p.g)) END / {a} AS acres,
                        CASE WHEN count(*) = 1 THEN any_value(p.g) ELSE ST_Union_Agg(p.g) END AS g,
                        string_agg(coalesce(p.name, ''), ' | ' ORDER BY p.pid) AS names,
                        bool_or(lower(coalesce(p.operator_type, '')) IN ('private', 'religious', 'private_non_profit')) AS private_tag,
                        bool_and(p.class = 'education') AS fallback_only
                 FROM p JOIN pc USING (pid) GROUP BY pc.campus""".format(a=ACRE))
    c.execute("ALTER TABLE camp ADD COLUMN gp GEOMETRY")
    c.execute("UPDATE camp SET gp = ST_Transform(g, 'EPSG:4326', 'EPSG:5070', always_xy := true)")
    st = c.execute("SELECT count(*), sum(acres), sum(fallback_only::INT) FROM camp").fetchall()[0]
    _ok(f"{len(pol):,} polygons, {len(pairs):,} intersecting pairs -> {st[0]:,} campuses ({st[2]:,} fallback), {st[1]:,.0f} acres")
    return len(pol), len(pairs)


def match(c, u):
    pts = u[u.has_point & ~u.virtual][["NCESSCH", "LAT", "LON", "SCH_NAME"]].copy()
    c.register("pts_df", pts)
    c.execute("""CREATE TABLE pts AS SELECT NCESSCH, SCH_NAME, ST_Point(LON, LAT) AS g,
                 ST_Transform(ST_Point(LON, LAT), 'EPSG:4326', 'EPSG:5070', always_xy := true) AS gp FROM pts_df""")
    inside = c.execute("""SELECT pts.NCESSCH, camp.campus, camp.acres, camp.fallback_only
                          FROM pts JOIN camp ON ST_Intersects(camp.g, pts.g)""").df()
    # Prefer a real school campus over a landuse=education container; then the smallest such campus.
    inside = inside.sort_values(["NCESSCH", "fallback_only", "acres", "campus"]).drop_duplicates("NCESSCH")
    rest = pts[~pts.NCESSCH.isin(inside.NCESSCH)]
    c.register("rest_ids", rest[["NCESSCH"]])
    near = c.execute(f"""SELECT pts.NCESSCH, pts.SCH_NAME, camp.campus, camp.names, camp.private_tag,
                                ST_Distance(camp.gp, pts.gp) AS dist_m
                         FROM pts JOIN rest_ids USING (NCESSCH)
                         JOIN camp ON ST_DWithin(camp.gp, pts.gp, {NEAR_NAME_M})
                         WHERE NOT camp.fallback_only""").df()
    near["name_hit"] = [bool(tokens(a) & tokens(b)) for a, b in zip(near.SCH_NAME, near.names)]
    near = near[~near.private_tag & (near.dist_m.le(NEAR_ANY_M) | near.name_hit)]
    near = near.sort_values(["NCESSCH", "dist_m", "campus"]).drop_duplicates("NCESSCH")
    m = pd.concat([inside.assign(how="inside")[["NCESSCH", "campus", "how"]],
                   near.assign(how=np.where(near.dist_m.le(NEAR_ANY_M), "near", "near_name"))[["NCESSCH", "campus", "how"]]])
    return m


def tract_of(c, table, idcol, geom_sql):
    """2010 tract GEOID of each row's point (spatial join on the cartographic boundary files)."""
    if not c.execute("SELECT count(*) FROM duckdb_tables() WHERE table_name = 'tr'").fetchall()[0][0]:
        q = " UNION ALL ".join(f"SELECT GEO_ID, geom FROM ST_Read('/vsizip/{z}/{z.name.replace('.zip', '.shp')}')" for z in TRACTS)
        c.execute(f"CREATE TABLE tr AS SELECT substr(GEO_ID, 10) AS tract, geom FROM ({q})")
    d = c.execute(f"""SELECT x.{idcol} AS id, min(tr.tract) AS tract FROM (SELECT {idcol}, {geom_sql} AS pt FROM {table}) x
                      JOIN tr ON ST_Intersects(tr.geom, x.pt) GROUP BY 1""").df()
    return d


# ------------------------------------------------------------------------------------------------ prices
def prices():
    xt = pd.read_csv(FHFA / "xs_tract.csv", dtype={"Census Tract": str})
    xt["tract"] = xt["Census Tract"].str.zfill(11)
    xc = pd.read_csv(FHFA / "xs_county.csv", dtype={"FIPS": str})
    xc["county"] = xc.FIPS.str.zfill(5)
    xs = pd.read_csv(FHFA / "xs_state.csv", dtype={"State FIPS": str})
    xs["state"] = xs["State FIPS"].str.zfill(2)
    pc = pd.read_csv(FHFA / "panel_county.csv", dtype={"FIPS": str})
    pc["county"] = pc.FIPS.str.zfill(5)
    ps = pd.read_csv(FHFA / "panel_state.csv", dtype={"State FIPS": str})
    ps["state"] = ps["State FIPS"].str.zfill(2)
    AS = "Land Value (Per Acre, As-Is)"

    def ratio(panel, key):
        w = panel.pivot_table(index=key, columns="Year", values=AS)
        return (w[2022] / w[2015]).dropna()
    g_cty, g_st = ratio(pc, "county"), ratio(ps, "state")
    h = pd.read_excel(HPI, header=5, dtype={"FIPS code": str})
    h["county"] = h["FIPS code"].str.zfill(5)
    h["HPI"] = pd.to_numeric(h.HPI, errors="coerce")
    hw = h.pivot_table(index="county", columns="Year", values="HPI")
    hg = (hw[2024] / hw[2022]).dropna()
    hg_st = hg.groupby(hg.index.str[:2]).median()
    # FHFA's tracts are 2010 tracts: the boundary files must be the 2010 ones.
    with zipfile.ZipFile(CACHE / "gaz" / "Gaz_tracts_national_2010.zip") as z:
        g10 = pd.read_csv(z.open("Gaz_tracts_national.txt"), sep="\t", dtype={"GEOID": str}, usecols=["GEOID"])
    vintage = float(xt.tract.isin(g10.GEOID).mean())
    if vintage < 0.99:
        raise SystemExit(f"[BLOCKED] only {vintage:.1%} of FHFA tracts are 2010 tracts")
    std = pd.read_csv(FHFA / "std_params.csv", dtype={"FIPS": str})
    std["county"] = std.FIPS.str.zfill(5)
    return dict(xt=xt.set_index("tract"), xc=xc.set_index("county"), xs=xs.set_index("state"), g_cty=g_cty,
                g_st=g_st, hg=hg, hg_st=hg_st, bl=std.set_index("county")["Lot Size"], AS=AS,
                vintage_2010_share=vintage)


def price_rows(tracts, P):
    """Per 2010 tract: 2024 as-is price per acre, quarter-acre standardized value, average lot size."""
    t = pd.DataFrame({"tract": sorted(set(tracts))})
    t["county"], t["state"] = t.tract.str[:5], t.tract.str[:2]
    AS, Q = P["AS"], "Land Value (1/4 Acre Lot, Standardized)"
    for col, src in [("p15", AS), ("q15", Q), ("lot_sqft", "Lot Size")]:
        t[col] = t.tract.map(P["xt"][src])
        t[col + "_c"] = t.county.map(P["xc"][src])
        t[col + "_s"] = t.state.map(P["xs"][src])
    t["price_level"] = np.where(t.p15.notna(), "tract", np.where(t.p15_c.notna(), "county", "state"))
    for col in ["p15", "q15", "lot_sqft"]:
        t[col] = t[col].fillna(t[col + "_c"]).fillna(t[col + "_s"])
    t["g_land"] = t.county.map(P["g_cty"]).fillna(t.state.map(P["g_st"]))
    t["g_land_level"] = np.where(t.county.map(P["g_cty"]).notna(), "county", "state")
    t["g_hpi"] = t.county.map(P["hg"]).fillna(t.state.map(P["hg_st"]))
    t["g_hpi_level"] = np.where(t.county.map(P["hg"]).notna(), "county", "state")
    t["p24"] = t.p15 * t.g_land * t.g_hpi
    t["q24"] = t.q15 * t.g_land * t.g_hpi
    t["bL"] = t.county.map(P["bl"]).clip(0.0, 1.0)
    return t[["tract", "price_level", "p15", "q15", "lot_sqft", "g_land", "g_land_level", "g_hpi", "g_hpi_level",
              "p24", "q24", "bL"]]


def value_arms(acres, t):
    """Land value (dollars) of a site of `acres` in tract row(s) t, under the four arms."""
    a = np.asarray(acres, float)
    A = a * t.p24.to_numpy()
    share = np.where(a > DEV_SMALL_ACRES, DEV_SHARE_LARGE, DEV_SHARE_SMALL)
    B = A * share
    lot = (t.lot_sqft.to_numpy() / 43_560.0).clip(0.05, None)
    C = A * np.exp(aes_f(np.log(a.clip(lot, None))) - aes_f(np.log(lot)))
    bl = t.bL.fillna(0.3).to_numpy()
    D = np.minimum(A, t.q24.to_numpy() * (a / 0.25) ** bl)
    return A, B, C, D


# Four vacant residential parcels Gyourko & Krimmel (2021, NBER w28993, pp. 13-16 and note 16) describe,
# sold 2013-2018 for single-family development: county, acres, price.
GK_PARCELS = [("Cobb County GA", "13067", 2_374_020 / 43_560, 6_479_937),
              ("Marin County CA", "06041", 171_388 / 43_560, 9_701_312),
              ("Fulton County GA", "13121", 429_937 / 43_560, 533_999),
              ("Alameda County CA", "06001", 442_134 / 43_560, 20_395_778)]


def discount_evidence(P):
    """Each parcel's price per acre against FHFA's county as-is residential price per acre (2013-2018 panel
    range), beside what arms B and C would predict for a parcel of that size."""
    pc = pd.read_csv(FHFA / "panel_county.csv", dtype={"FIPS": str})
    pc["county"] = pc.FIPS.str.zfill(5)
    rows = []
    for name, fips, acres, price in GK_PARCELS:
        w = pc[pc.county.eq(fips) & pc.Year.between(2013, 2018)].set_index("Year")[P["AS"]]
        lot = float(P["xc"].loc[fips, "Lot Size"]) / 43_560.0
        rows.append(dict(parcel=name, county=fips, acres=acres, price_usd=price, price_per_acre=price / acres,
                         fhfa_asis_per_acre_2013=float(w[2013]), fhfa_asis_per_acre_2018=float(w[2018]),
                         ratio_high=price / acres / float(w[2013]), ratio_low=price / acres / float(w[2018]),
                         arm_B_factor=DEV_SHARE_LARGE if acres > DEV_SMALL_ACRES else DEV_SHARE_SMALL,
                         arm_C_factor=float(np.exp(aes_f(np.log(acres)) - aes_f(np.log(lot))))))
    return pd.DataFrame(rows)


# ------------------------------------------------------------------------------------------- imputation
def design(df, states, locales):
    X = [np.ones(len(df)), np.log1p(df.k12_all.to_numpy()), df.charter.astype(float).to_numpy()]
    names = ["const", "log1p_k12", "charter"]
    for lv in ["Middle", "High", "Other", "Secondary", "Prekindergarten", "Not reported", "Not applicable", "Ungraded"]:
        X.append(df.LEVEL.eq(lv).astype(float).to_numpy()); names.append(f"level_{lv}")
    for ty in ["2", "3", "4"]:
        X.append(df.SCH_TYPE.eq(ty).astype(float).to_numpy()); names.append(f"type_{ty}")
    for lo in locales[1:]:
        X.append(df.LOCALE.eq(lo).astype(float).to_numpy()); names.append(f"locale_{lo}")
    for s in states[1:]:
        X.append(df.FIPST.eq(s).astype(float).to_numpy()); names.append(f"state_{s}")
    return np.column_stack(X), names


def impute(u, fit_mask):
    states, locales = sorted(u.FIPST.unique()), sorted(u.LOCALE.fillna("NA").unique())
    v = u.assign(LOCALE=u.LOCALE.fillna("NA"))
    X, names = design(v, states, locales)
    y = np.log(v.acres_alloc.where(fit_mask))
    f = fit_mask.to_numpy() & np.isfinite(y.to_numpy())
    beta, *_ = np.linalg.lstsq(X[f], y.to_numpy()[f], rcond=None)
    resid = y.to_numpy()[f] - X[f] @ beta
    smear = float(np.mean(np.exp(resid)))
    pred = np.exp(X @ beta) * smear
    r2 = 1 - resid.var() / y.to_numpy()[f].var()
    return pred, dict(n_fit=int(f.sum()), r2=float(r2), smear=smear, rmse_log=float(resid.std()),
                      coef={n: float(b) for n, b in zip(names, beta) if not n.startswith("state_")})


# ------------------------------------------------------------------------------------------------- group
def group_weights(u):
    spec = importlib.util.spec_from_file_location("where_enrolled_weighting", WEIGHTING)
    w = importlib.util.module_from_spec(spec)
    sys.path.insert(0, str(WEIGHTING.parent))
    spec.loader.exec_module(w)
    d, _ = w.build()
    share = d.set_index("LEAID").dist_share_raked
    st_share = d.groupby("fips").state_share.first()
    lea = u.LEAID.where(~u.LEA_NAME.fillna("").str.startswith("NEW YORK CITY GEOGRAPHIC DISTRICT"), w.NYC_F33)
    s = lea.map(share)
    src = np.where(s.notna(), "district", "state")
    s = s.fillna(u.FIPST.astype(int).map(st_share))
    return s.to_numpy(), src, float(d.w_mex_dist.sum())


# -------------------------------------------------------------------------------------------- validation
def cscd(c, u):
    """California: CSCD 2025 property acreage per NCES school (by CDS code), against the lane's acreage."""
    c.execute(f"CREATE TABLE cs AS SELECT * FROM ST_Read('{CSCD / 'schools_stacked.geojson'}')")
    c.execute(f"CREATE TABLE cp AS SELECT * FROM ST_Read('{CSCD / 'school_property.geojson'}')")
    # Each school polygon's property: the property polygon holding its point on surface.
    sp = c.execute("""SELECT cs.CDSCode, cs.Pb_Prv_BIE, cs.Charter, cs.Status, min(cp.PropertyId) AS prop
                      FROM cs LEFT JOIN cp ON ST_Intersects(cp.geom, ST_PointOnSurface(cs.geom))
                      GROUP BY ALL""").df()
    props = c.execute("SELECT PropertyId AS prop, Size_AC, School_Cnt FROM cp").df()
    tot = float(props.Size_AC.sum())
    ca = u[u.FIPST.eq("06")].copy()
    ca["CDSCode"] = ca.ST_SCHID.str.replace("CA-", "", regex=False).str.replace("-", "", regex=False)
    sp = sp.merge(props, on="prop", how="left")
    # A CDS code with several branch campuses: sum its distinct properties.
    by = sp.dropna(subset=["prop"]).drop_duplicates(["CDSCode", "prop"]).groupby("CDSCode").agg(
        cscd_acres=("Size_AC", "sum"), cscd_props=("prop", "nunique"), cscd_school_cnt=("School_Cnt", "max"),
        first_prop=("prop", "min"))
    ca = ca.merge(by, left_on="CDSCode", right_index=True, how="left")
    return ca, tot, props


# --------------------------------------------------------------------------------------------------- main
def main():
    OUT.mkdir(exist_ok=True)
    c = duckdb.connect()
    c.execute("LOAD spatial; SET geometry_always_xy = true; SET threads = 4;")
    print("[universe]")
    u = schools.universe()
    _ok(f"{len(u):,} operating schools, {u.k12_all.sum():,.0f} K-12 pupils, {u.virtual.sum():,} exclusively virtual")
    print("[campuses]")
    n_poly, n_pairs = campuses(c)
    m = match(c, u)
    u = u.merge(m, on="NCESSCH", how="left")
    u["matched"] = u.campus.notna()
    land = ~u.virtual
    camp = c.execute("SELECT campus, acres, n_polys, private_tag, fallback_only FROM camp").df()
    u = u.merge(camp[["campus", "acres"]], on="campus", how="left")
    # Split each campus among its matched schools by K-12 pupils (equal split if none has pupils).
    grp = u[u.matched].groupby("campus")
    w = u.k12_all.clip(lower=0)
    tot_w = u.campus.map(grp.k12_all.sum())
    n_on = u.campus.map(grp.size())
    u["n_on_campus"] = n_on
    u["acres_alloc"] = np.where(u.matched, np.where(tot_w > 0, u.acres * w / tot_w, u.acres / n_on), np.nan)
    _ok(f"matched {u.matched[land].sum():,} of {land.sum():,} non-virtual schools "
        f"({u.matched[land].mean():.1%}; pupils {u.k12_all[land & u.matched].sum() / u.k12_all[land].sum():.1%}); "
        f"{u.campus.nunique():,} campuses used, {u.drop_duplicates('campus').acres.sum():,.0f} acres")

    print("[imputation]")
    fit = u.matched & land & u.n_on_campus.eq(1) & u.k12_all.gt(0)
    pred, fitinfo = impute(u, fit)
    u["acres_hat"] = pred
    u["acres_final"] = np.where(u.matched, u.acres_alloc, np.where(land, u.acres_hat, 0.0))
    u["acres_src"] = np.where(u.matched, "polygon", np.where(land, "imputed", "virtual"))
    _ok(f"fit n={fitinfo['n_fit']:,}, R2={fitinfo['r2']:.3f}, smear={fitinfo['smear']:.3f}; imputed "
        f"{(u.acres_src == 'imputed').sum():,} schools, {u.acres_final[u.acres_src == 'imputed'].sum():,.0f} acres")

    print("[prices]")
    P = prices()
    camp_tr = tract_of(c, "camp", "campus", "ST_PointOnSurface(g)")
    pts_tr = tract_of(c, "pts", "NCESSCH", "g")
    u["tract"] = np.where(u.matched, u.campus.map(camp_tr.set_index("id").tract), u.NCESSCH.map(pts_tr.set_index("id").tract))
    # A point off the cartographic tract layer (water, coast): nearest county's state fallback via EDGE county.
    u["tract"] = u.tract.fillna(u.CNTY.fillna("00000") + "999999")
    pr = price_rows(u.tract[land], P)
    t = u[["tract"]].merge(pr, on="tract", how="left")
    # Site acreage drives plattage: a campus shares its whole acreage's price per acre among its schools.
    site_acres = np.where(u.matched, u.acres, u.acres_final).astype(float)
    site_acres = np.where(site_acres > 0, site_acres, 1e-6)
    A, B, C, D = value_arms(site_acres, t)
    frac = np.where(site_acres > 0, u.acres_final.to_numpy() / site_acres, 0.0)
    for k, v in zip("ABCD", (A, B, C, D)):
        u[f"value_{k}"] = np.where(land, v * frac, 0.0)
    u["price_level"] = t.price_level.to_numpy()
    u["p24"] = t.p24.to_numpy()
    u["g_hpi"] = t.g_hpi.to_numpy()
    _ok("price levels: " + ", ".join(f"{k} {v:.1%}" for k, v in
                                       u[land].groupby("price_level").acres_final.sum().div(u.acres_final[land].sum()).items()))

    ev = discount_evidence(P)
    ev.to_csv(OUT / "discount_evidence.csv", index=False, lineterminator="\n", float_format="%.6g")
    _ok("G&K parcels / FHFA county price per acre: " + ", ".join(f"{r.parcel} {r.ratio_low:.2f}-{r.ratio_high:.2f}" for r in ev.itertuples())
        + f"; arm C factors {ev.arm_C_factor.min():.2f}-{ev.arm_C_factor.max():.2f}")

    print("[group]")
    share, share_src, group_admin = group_weights(u)
    u["mex_share"] = share
    u["w_group"] = u.k12_hisp * u.mex_share
    u["w_hisp"] = u.k12_hisp

    print("[validation]")
    ca, cscd_total, props = cscd(c, u)

    # ------------------------------------------------------------------------------------------ outputs
    capital = json.loads(CAPITAL.read_text())
    case = json.loads(CASE.read_text())["v9"]
    rate = float(case["one_rate"]["flat_real_equivalent"])
    RATES["case_flat_real"] = rate
    band = [float(x) for x in case["band_bn"]]
    s = float(capital["pupil_share_s"])
    structures = float(capital["national_k12_capital_bn"]["central"]["structures_avg2024"])
    k12_capital = float(capital["national_k12_capital_bn"]["central"]["avg2024"])
    L = u[land]
    pupils = float(L.k12_all.sum())
    res = {}
    for k in "ABCD":
        V = float(L[f"value_{k}"].sum()) / 1e9
        per_pupil_nat = V / pupils
        wg = L.w_group
        pp = L[f"value_{k}"] / 1e9
        # Land per pupil where the group's pupils enroll: pupil-weighted mean over schools of land per pupil.
        has = L.k12_all > 0
        r_where = float((wg[has] * pp[has] / L.k12_all[has]).sum() / wg[has].sum() / per_pupil_nat)
        r_hisp = float((L.w_hisp[has] * pp[has] / L.k12_all[has]).sum() / L.w_hisp[has].sum() / per_pupil_nat)
        g_conv, g_where = s * V, s * V * r_where
        res[k] = dict(national_bn=V, per_pupil_usd=V * 1e9 / pupils, ratio_to_k12_structures=V / structures,
                      ratio_to_k12_capital=V / k12_capital, where_enrolled_ratio=r_where, hispanic_weight_ratio=r_hisp,
                      group_value_bn={"pupil_share": g_conv, "where_enrolled": g_where},
                      annual_charge_bn={rk: {"pupil_share": g_conv * rv, "where_enrolled": g_where * rv} for rk, rv in RATES.items()},
                      share_of_headline_where_enrolled_at_case_rate=[g_where * rate / b for b in band])

    # Charter and imputed parts (arm B, central).
    parts = {}
    for name, mask in {"charter": L.charter, "imputed": L.acres_src.eq("imputed"), "polygon": L.acres_src.eq("polygon")}.items():
        parts[name] = dict(schools=int(mask.sum()), acres=float(L.acres_final[mask].sum()),
                           value_B_bn=float(L.value_B[mask].sum() / 1e9), pupils=float(L.k12_all[mask].sum()))

    # Match rates by state.
    st = L.groupby("ST").agg(schools=("NCESSCH", "size"), matched=("matched", "sum"), pupils=("k12_all", "sum"),
                             pupils_matched=("k12_all", lambda x: x[L.loc[x.index, "matched"]].sum()),
                             acres=("acres_final", "sum"), acres_imputed=("acres_final", lambda x: x[L.loc[x.index, "acres_src"].eq("imputed")].sum()),
                             value_A_bn=("value_A", lambda x: x.sum() / 1e9), value_B_bn=("value_B", lambda x: x.sum() / 1e9),
                             value_C_bn=("value_C", lambda x: x.sum() / 1e9), group_pupils=("w_group", "sum")).reset_index()
    st["match_rate"] = st.matched / st.schools
    st["pupil_match_rate"] = st.pupils_matched / st.pupils
    st["acres_per_pupil"] = st.acres / st.pupils
    st["value_B_per_pupil_usd"] = st.value_B_bn * 1e9 / st.pupils
    st = st.sort_values("ST")
    st.to_csv(OUT / "by_state.csv", index=False, lineterminator="\n", float_format="%.6g")

    # Validation, California.
    cav = ca[~ca.virtual].copy()
    both = cav[cav.matched & cav.cscd_acres.notna()].copy()
    # Compare campus totals: the lane's campus acreage vs the CSCD property acreage of the same school.
    both = both.drop_duplicates("campus")
    lr = np.log(both.acres / both.cscd_acres)
    imp = cav[cav.acres_src.eq("imputed") & cav.cscd_acres.notna() & cav.cscd_school_cnt.eq(1)]
    sole = cav[cav.matched & cav.n_on_campus.eq(1) & cav.cscd_acres.notna() & cav.cscd_school_cnt.eq(1)]
    val = dict(
        cscd_total_acres=cscd_total, cscd_properties=int(len(props)),
        lane_ca_total_acres=float(cav.acres_final.sum()),
        lane_ca_total_over_cscd=float(cav.acres_final.sum() / cscd_total),
        lane_ca_polygon_acres=float(cav.acres_final[cav.acres_src.eq("polygon")].sum()),
        lane_ca_imputed_acres=float(cav.acres_final[cav.acres_src.eq("imputed")].sum()),
        ca_schools_with_cscd=int(cav.cscd_acres.notna().sum()), ca_schools=int(len(cav)),
        campus_level=dict(n=int(len(both)), median_ratio=float(np.exp(lr.median())), mean_abs_log_error=float(lr.abs().mean()),
                          share_within_25pct=float((lr.abs() <= math.log(1.25)).mean()),
                          sum_ratio=float(both.acres.sum() / both.cscd_acres.sum())),
        sole_occupant=dict(n=int(len(sole)), sum_ratio=float(sole.acres_alloc.sum() / sole.cscd_acres.sum()),
                           median_ratio=float(np.exp(np.log(sole.acres_alloc / sole.cscd_acres).median()))),
        imputed=dict(n=int(len(imp)), sum_ratio=float(imp.acres_hat.sum() / imp.cscd_acres.sum()),
                     median_ratio=float(np.exp(np.log(imp.acres_hat / imp.cscd_acres).median()))),
    )
    # Sensitivities on the central arm B: each re-prices or re-scopes the per-school values.
    has_all = L.k12_all > 0

    def summarize(v, mask=None, weight="w_group"):
        mask = pd.Series(True, index=L.index) if mask is None else mask
        V = float(v[mask].sum()) / 1e9
        h = mask & has_all
        ppn = V * 1e9 / float(L.k12_all[mask].sum())
        r = float((L[weight][h] * v[h] / L.k12_all[h]).sum() / L[weight][h].sum() / ppn)
        return dict(national_bn=V, where_enrolled_ratio=r, ratio_to_k12_structures=V / structures,
                    group_charge_case_rate_bn={"pupil_share": s * V * rate, "where_enrolled": s * V * r * rate})
    vB = L.value_B
    calib_poly = 1.0 / val["campus_level"]["sum_ratio"]
    calib_imp = 1.0 / val["imputed"]["sum_ratio"]
    sens = {
        "central_B": summarize(vB),
        "hispanic_weights": summarize(vB, weight="w_hisp"),
        "acreage_calibrated_to_cscd": dict(summarize(vB * np.where(L.acres_src.eq("imputed"), calib_imp, calib_poly)),
                                           polygon_factor=calib_poly, imputed_factor=calib_imp),
        "excluding_charters": summarize(vB, ~L.charter),
        "excluding_manhattan_36061": summarize(vB, ~L.tract.str.startswith("36061")),
        "no_2022_2024_carry_forward": summarize(vB / L.g_hpi),
        # Near matches (point outside the polygon) take the imputed acreage instead.
        "inside_matches_only": summarize(vB.where(~L.how.isin(["near", "near_name"]), vB * (L.acres_hat / L.acres_final).fillna(1.0))),
        "tract_priced_only_rescaled": dict(summarize(vB, L.price_level.eq("tract")), note="schools priced at their own tract only; national total is for that subset"),
    }

    ca_out = cav[["NCESSCH", "CDSCode", "SCH_NAME", "LEVEL", "charter", "k12_all", "matched", "how", "n_on_campus",
                  "acres", "acres_alloc", "acres_hat", "acres_final", "acres_src", "cscd_acres", "cscd_props",
                  "cscd_school_cnt"]].sort_values("NCESSCH")
    ca_out.to_csv(OUT / "validation_cscd_ca.csv", index=False, lineterminator="\n", float_format="%.6g")

    # Schools file (compact): one row per school.
    sch = u[["NCESSCH", "ST", "LEAID", "LEVEL", "SCH_TYPE", "charter", "virtual", "k12_all", "k12_hisp", "mex_share",
             "matched", "how", "campus", "n_on_campus", "acres_final", "acres_src", "tract", "price_level", "p24",
             "value_A", "value_B", "value_C", "value_D"]].copy()
    sch["campus"] = sch.campus.astype("Int64")
    sch = sch.sort_values("NCESSCH")
    sch.to_csv(OUT / "schools.csv.gz", index=False, lineterminator="\n", float_format="%.6g",
               compression={"method": "gzip", "mtime": 0})

    summary = dict(
        lane="school_land_2026_10_24", status="beside the case, not adopted", year=2024,
        inputs=dict(overture_release="2026-10-21.0", fhfa_land="WP 19-01 v4.0 (June 2024), pooled cross-section 2015 prices",
                    hpi="FHFA annual county all-transactions HPI (last updated 2026-03-31)", nces="EDGE/CCD 2023-24",
                    case_rate=rate, headline_band_bn=band, pupil_share_s=s, k12_structures_bn=structures,
                    k12_capital_bn=k12_capital),
        universe=dict(schools=int(len(u)), virtual=int(u.virtual.sum()), non_virtual=int(land.sum()), pupils_non_virtual=pupils,
                      polygons=n_poly, intersecting_pairs=n_pairs),
        matching=dict(matched=int(L.matched.sum()), match_rate=float(L.matched.mean()),
                      pupil_match_rate=float(L.k12_all[L.matched].sum() / pupils),
                      by_how={k: int(v) for k, v in L.how.value_counts().items()},
                      ca=dict(match_rate=float(L.matched[L.ST.eq("CA")].mean()),
                              pupil_match_rate=float(L.k12_all[L.matched & L.ST.eq("CA")].sum() / L.k12_all[L.ST.eq("CA")].sum())),
                      tx=dict(match_rate=float(L.matched[L.ST.eq("TX")].mean()),
                              pupil_match_rate=float(L.k12_all[L.matched & L.ST.eq("TX")].sum() / L.k12_all[L.ST.eq("TX")].sum())),
                      thresholds_m=dict(any=NEAR_ANY_M, name=NEAR_NAME_M)),
        acreage=dict(total=float(L.acres_final.sum()), polygon=parts["polygon"]["acres"], imputed=parts["imputed"]["acres"],
                     per_school_median_matched=float(L.acres_alloc[L.matched].median()), imputation=fitinfo),
        prices=dict(fhfa_tracts_in_2010_gazetteer=P["vintage_2010_share"], acre_share_by_level={k: float(v) for k, v in L.groupby("price_level").acres_final.sum().div(L.acres_final.sum()).items()},
                    acre_weighted_p24_usd=float((L.p24 * L.acres_final).sum() / L.acres_final.sum()),
                    dev_share=dict(large=DEV_SHARE_LARGE, small=DEV_SHARE_SMALL, small_acres=DEV_SMALL_ACRES), aes_coef=list(AES)),
        group=dict(admin_group_pupils_weighting=group_admin, lane_group_pupils=float(L.w_group.sum()),
                   share_source={k: int(v) for k, v in pd.Series(share_src[land.to_numpy()]).value_counts().items()}),
        arms=res, parts_B=parts, validation=val, sensitivities_B=sens,
        discount_evidence=dict(ratio_mid={r.parcel: (r.ratio_low + r.ratio_high) / 2 for r in ev.itertuples()},
                               median_mid=float(((ev.ratio_low + ev.ratio_high) / 2).median()),
                               arm_C_factor={r.parcel: r.arm_C_factor for r in ev.itertuples()}),
    )
    (OUT / "summary.json").write_text(json.dumps(summary, indent=1, sort_keys=True) + "\n")
    rows = []
    for k, lab in zip("ABCD", ["A residential, all acres", "B developable share (central)", "C vacant-land plattage (AES)",
                               "D FHFA county lot-size elasticity"]):
        r = res[k]
        rows.append(dict(arm=k, label=lab, national_bn=r["national_bn"], per_pupil_usd=r["per_pupil_usd"],
                         land_to_k12_structures=r["ratio_to_k12_structures"], where_enrolled_ratio=r["where_enrolled_ratio"],
                         group_value_pupil_share_bn=r["group_value_bn"]["pupil_share"],
                         group_value_where_enrolled_bn=r["group_value_bn"]["where_enrolled"],
                         **{f"charge_{rk}_{w}_bn": r["annual_charge_bn"][rk][w] for rk in RATES for w in ("pupil_share", "where_enrolled")}))
    pd.DataFrame(rows).to_csv(OUT / "arms.csv", index=False, lineterminator="\n", float_format="%.6g")
    for k in "ABC":
        r = res[k]
        _ok(f"arm {k}: national ${r['national_bn']:,.1f}bn (land/structures {r['ratio_to_k12_structures']:.3f}); "
            f"where-enrolled ratio {r['where_enrolled_ratio']:.3f}; group charge at case rate "
            f"${r['annual_charge_bn']['case_flat_real']['where_enrolled']:.2f}bn")
    _ok(f"CA: lane {val['lane_ca_total_acres']:,.0f} acres vs CSCD {cscd_total:,.0f} (ratio {val['lane_ca_total_over_cscd']:.3f}); "
        f"campus-level median ratio {val['campus_level']['median_ratio']:.3f}, imputed sum ratio {val['imputed']['sum_ratio']:.3f}")


if __name__ == "__main__":
    sys.exit(main())
