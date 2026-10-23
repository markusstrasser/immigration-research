"""Land beside every physical capital line in the adopted oct16 case.

Native-First: invoke the existing case evaluator, primary acquisition modules and
DuckDB spatial joins. The school lane supplies the single FHFA/discount definition.
Raw data are parsed only in isolated Python. No change to the adopted account.

    uv run --no-project python3 infra/immigration-fiscal/public_land_2026_10_24/build.py
"""
from __future__ import annotations

import csv
import hashlib
import json
import os
import resource
import subprocess
import sys
import time
from pathlib import Path

if not sys.flags.isolated:
    os.execv(sys.executable, [sys.executable, "-I", *sys.argv])
sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))  # trusted source only; never a download directory

import numpy as np
import pandas as pd

import acquire_footprints
import acquire_roads
import acquire_universes
import footprints
import roads
import universes
import valuation

OUT = HERE / "derived"
FISCAL = HERE.parent
SCHOOL = FISCAL / "school_land_2026_10_24"
OMIT_COUNTIES = {"36061", "06075", "11001"}  # Manhattan, San Francisco, DC
ARMS = "ABC"


def write_csv(frame, name):
    frame.to_csv(OUT / name, index=False, lineterminator="\n", float_format="%.12g")


def write_json(value, name):
    (OUT / name).write_text(json.dumps(valuation.json_finite(value), indent=2, sort_keys=True, allow_nan=False) + "\n")


def provenance():
    def fingerprint(path, relative):
        h=hashlib.sha256()
        with path.open("rb") as handle:
            while chunk:=handle.read(1_048_576):
                h.update(chunk)
        return dict(path=str(relative),bytes=path.stat().st_size,sha256=h.hexdigest())
    school_inputs=[SCHOOL/"build.py",SCHOOL/"derived"/"summary.json",SCHOOL/"derived"/"schools.csv.gz",
                   SCHOOL/"derived"/"acquired_sources.json",SCHOOL/"_cache"/"hpi"/"hpi_at_county.xlsx",
                   SCHOOL/"_cache"/"gaz"/"Gaz_tracts_national_2010.zip"]
    school_inputs+=sorted((SCHOOL/"_cache"/"fhfa"/"csv").glob("*.csv"))
    school_inputs+=sorted((SCHOOL/"_cache"/"tracts2010").glob("*.zip"))
    source_code=sorted(HERE.glob("*.py"))+sorted(HERE.glob("*.cjs"))
    reused=[fingerprint(p,p.relative_to(FISCAL)) for p in school_inputs]
    own=[fingerprint(p,p.relative_to(HERE)) for p in source_code]
    manifest=json.loads((HERE/"_cache"/"footprints"/"manifest.json").read_text())
    # Retain the primary extraction receipts, not normalization/cache artifacts
    # which acquire_footprints may discover only after the initial build.
    manifest["files"]=[r for r in manifest["files"] if "/padus/" in r["path"] or
        Path(r["path"]).name.startswith(("overture_land_use_","overture_infrastructure_"))]
    write_json(manifest,"footprint_acquired_sources.json")
    write_json(dict(school_read_only_inputs=reused,lane_source=own,
        primary_manifests=["roads_sources.json","universe_sources.json","footprint_acquired_sources.json"]),"input_provenance.json")
    cache_files=[p for p in (HERE/"_cache").rglob("*") if p.is_file()]
    total=sum(p.stat().st_size for p in cache_files)
    if total>=5_000_000_000 or any(p.stat().st_size>=10_000_000_000 for p in cache_files):
        raise ValueError(f"[BLOCKED] cache exceeds disk brief: {total} bytes")
    print(f"lane cache {total:,} bytes; {len(cache_files):,} files",flush=True)


def physical_contract(contract):
    d = pd.DataFrame(contract["rows"])
    rows = []
    school = json.loads((SCHOOL / "derived" / "summary.json").read_text())
    for (method, end, line), g in d.groupby(["method", "end", "physical_line"], sort=True):
        stocks = g.stock_charged_bn.unique()
        if len(stocks) != 1:
            raise ValueError(f"[BLOCKED] fee offsets do not share one physical stock: {line}")
        structures = 0.0 if line.startswith("ent_other_") else float(stocks[0])
        if line == "k12":
            structures = school["inputs"]["k12_structures_bn"]
        rows.append(dict(method=method, end=end, line=line, level=g.level.iloc[0], group=g.group.iloc[0],
                         stock_charged_bn=float(stocks[0]), structures_bn=structures,
                         engine_key=float(g.engine_key.sum()), engine_response=float(g.engine_response.iloc[0]),
                         full_return_at_case_rate_bn=float(g.full_return_at_case_rate_bn.sum()),
                         effective_key_times_response=float(g.effective_key_times_response.sum())))
    full = pd.DataFrame(rows)
    write_csv(full, "case_physical_lines.csv")
    return full


def school_records():
    s = json.loads((SCHOOL / "derived" / "summary.json").read_text())
    d = pd.read_csv(SCHOOL / "derived" / "schools.csv.gz", dtype={"tract": str, "NCESSCH": str})
    d = d[~d.virtual].copy()
    d["record_id"] = "school:" + d.NCESSCH
    d["line"] = "k12"
    d["county"] = d.tract.str[:5]
    d["class"] = "school"
    d["acres"] = d.acres_final
    d["source"] = "school_land_2026_10_24; polygon plus independently validated acreage imputation"
    d["ownership_evidence"] = "CCD public institution, title/lease not established; school benchmark"
    d["priced"] = True
    for arm in ARMS:
        # Published per-school CSVs have six significant digits. Preserve their
        # geography, but restore the source's full precision national arm total.
        source = float(s["arms"][arm]["national_bn"])
        d["value_" + arm] *= source * 1e9 / d["value_" + arm].sum()
        w = np.where(d.k12_all.gt(0), d.k12_hisp * d.mex_share / d.k12_all.clip(lower=1), 0)
        raw = d["value_" + arm] * w
        exposure = s["arms"][arm]["where_enrolled_ratio"] * source * 1e9
        d["group_weighted_value_" + arm] = raw * exposure / raw.sum()
    return d, s


def airport_records(u, c):
    d = u[u["class"].eq("airport") & u.public.eq("1") & u.status.eq("O") & u.site_type.eq("A")].copy()
    d["acres"] = pd.to_numeric(d.acreage, errors="coerce")
    valid = d.acres.gt(0)
    info = dict(universe=len(d), acreage_recorded=int(valid.sum()), acreage_missing=int((~valid).sum()),
                footprint_coverage=float(valid.mean()),
                limitation="FAA acreage belongs to the whole airport; price at reference point, no within-airport land-price weighting; civil PU ownership does not separate all federal owners")
    d = d[valid].copy()
    d["site_acres"] = d.acres
    d["line"] = "ent_airports_sl"
    d["ownership_evidence"] = "FAA PU publicly owned; reported acreage"
    return valuation.locate_points(c, d), info


def match_facilities(c, u):
    """Match public institutions to the smallest containing use polygon, without filling gaps.

    Private-owner tags veto a point proxy. A polygon containing private institutions
    as well as public ones remains ambiguous unless title is explicitly public.
    Near-point matching is deliberately omitted: no class-specific distance/name
    validation exists. All unselected/unknown sites remain in the coverage table.
    """
    path = HERE / "_cache" / "footprints" / "facility_records.parquet"
    c.execute(f"CREATE TABLE facilities AS SELECT *, ST_MakeValid(ST_GeomFromWKB(wkb)) AS g FROM read_parquet('{path}') WHERE area_m2>0")
    c.execute("CREATE INDEX facilities_rtree ON facilities USING RTREE(g)")
    pts = u[u["class"].isin(["college", "hospital", "housing"])].copy()
    if "case_scope" not in pts:
        raise ValueError("[BLOCKED] institution inventory lacks defense/federal-education scope classification")
    excluded_scope=pts[~pts.case_scope.eq("eligible")].groupby(["class","case_scope"]).size().to_dict()
    print("Institution scope exclusions:",excluded_scope,flush=True)
    pts = pts[~(pts["class"].eq("hospital") & ~pts.status.eq("OPEN"))]
    # HUD tract/ZIP/block-group centroids and scattered developments cannot identify
    # fee parcels. Keep their records in coverage but do not call them matches.
    eligible = ~pts["class"].eq("housing") | (pts.geocode_quality.isin(["R", "4"]) & pts.scattered_site.eq("N"))
    pts["match_eligible"] = eligible
    pts["match_class"] = pts["class"].replace({"hospital": "health"})
    c.register("universe_points_input", pts[["record_id", "match_class", "public", "ownership", "lon", "lat", "match_eligible", "case_scope"]])
    c.execute("CREATE TABLE universe_points AS SELECT *,ST_Point(lon,lat) AS g FROM universe_points_input WHERE match_eligible")
    # A class equality in the spatial ON clause selects a hash join (~196m
    # geometry comparisons in the first probe). Independent class partitions
    # preserve the exact matches and let DuckDB use its native spatial join.
    queries=[]
    for cls in ["college","health","housing"]:
        queries.append(f"""SELECT p.record_id,p.public,p.case_scope,p.ownership AS institution_ownership,
            f.id,f.class,f.area_m2,f.ownership AS map_ownership
            FROM (SELECT * FROM universe_points WHERE match_class='{cls}') p
            JOIN (SELECT * FROM facilities WHERE class='{cls}') f ON ST_Intersects(f.g,p.g)""")
    hits=c.execute("SELECT * FROM ("+" UNION ALL ".join(queries)+") ORDER BY record_id,area_m2,id").df()
    # One point locates one campus; several points on a campus never duplicate acres.
    chosen = hits.drop_duplicates("record_id").copy()
    write_csv(chosen, "facility_matches.csv")
    chosen["eligible_public"] = chosen.public.eq("1") & chosen.case_scope.eq("eligible")
    chosen["excluded_scope"] = ~chosen.case_scope.isin(["eligible","not_public"])
    ownership = chosen.groupby("id").agg(public_match=("eligible_public", "any"), excluded_match=("excluded_scope", "any"),
                                             private_match=("public", lambda x: bool(x.eq("0").any())),
                                             institution_owners=("institution_ownership", lambda x: " | ".join(sorted(set(x)))))
    raw = c.execute("SELECT * EXCLUDE(g,wkb,source_tags) FROM facilities ORDER BY id").df().merge(ownership, on="id", how="left")
    flags=["public_match", "private_match", "excluded_match"]
    raw[flags] = raw[flags].fillna(False).astype(bool)
    tagged = raw.ownership.isin(["public_owner_tag", "government_operator_tag"])
    matched = raw.public_match & ~raw.private_match & ~raw.ownership.isin(["private_owner_tag", "private_operator_tag"])
    accepted = (tagged | matched) & ~raw.excluded_match
    raw["ownership_evidence"] = np.where(raw.ownership.eq("public_owner_tag"), "public_owner_tag",
        np.where(raw.ownership.eq("government_operator_tag"), "public_operation_proxy; title and leases unresolved", "public_institution_point; title and leases unresolved"))
    # A contemporaneous inventory is used for health/colleges. Map tags alone do not
    # identify omitted campuses; explicit tagged sites may add branches not in IPEDS.
    mapping = {"college": "college", "health": "health_sl", "public_safety": "pos_sl", "government": "gps_sl",
               "sewer": "ent_sewer_sl", "water": "ent_water_sl", "power": "ent_power_sl", "transit": "ent_transit_sl",
               "port": "ent_ports_sl", "housing": "ent_housing_sl"}
    raw["line"] = raw["class"].map(mapping)
    federal = raw.institution_owners.fillna("").str.contains("GOVERNMENT - FEDERAL|VETERANS HEALTH ADMINISTRATION", regex=True)
    for field in ["owner_type", "operator_type"]:
        federal |= raw[field].fillna("").str.lower().eq("federal")
    for sl, fed in [("health_sl", "health_fed"), ("gps_sl", "gps_fed"), ("pos_sl", "pos_fed"), ("ent_power_sl", "ent_power_fed")]:
        raw.loc[federal & raw.line.eq(sl), "line"] = fed
    # No known government level is invented from a name. An explicit public site
    # without federal evidence is the state/local proxy, and that assumption is
    # carried in diagnostics rather than used as a national owner split.
    raw["owner_level_assumption"] = np.where(federal, "federal evidence", "state/local proxy where level unrecorded")
    accepted &= raw.line.notna()
    raw["accepted"] = accepted
    cov = []
    for cls in sorted(set(raw["class"]) | set(mapping)):
        g = raw[raw["class"].eq(cls)]
        source_class = "hospital" if cls == "health" else cls
        target = pts[pts["class"].eq(source_class) & pts.public.eq("1") & pts.case_scope.eq("eligible")]
        matched_ids = set(chosen.loc[chosen.public.eq("1") & chosen.id.isin(raw.loc[accepted, "id"]), "record_id"])
        nmatch = int(target.record_id.isin(matched_ids).sum())
        cov.append(dict(facility_class=cls, map_records=len(g), accepted_public_sites=int(g.accepted.sum()),
                        unknown_ownership_sites=int(g.ownership.eq("unknown").sum()), public_universe=len(target),
                        public_universe_matches=nmatch, public_universe_match_rate=nmatch / len(target) if len(target) else None,
                        national_completeness="not identified; no area expansion for unmapped sites"))
    selected = raw[accepted].copy()
    c.register("selected_facility_ids", selected[["id", "line"]])
    # Overlapping polygons within the same fiscal line cannot both contribute
    # their area. Component unions preserve each disjoint campus as the C/B site.
    c.execute("CREATE TABLE accepted_geometries AS SELECT f.id,x.line,f.g FROM facilities f JOIN selected_facility_ids x USING(id)")
    queries=[f"""SELECT a.id,b.id FROM (SELECT * FROM accepted_geometries WHERE line='{line}') a
        JOIN (SELECT * FROM accepted_geometries WHERE line='{line}') b ON ST_Intersects(a.g,b.g)
        WHERE a.id<b.id""" for line in sorted(selected.line.unique())]
    pairs=c.execute("SELECT * FROM ("+" UNION ALL ".join(queries)+") ORDER BY 1,2").fetchall() if queries else []
    parent = {x: x for x in selected.id}
    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x
    for a, b in pairs:
        aa, bb = find(a), find(b)
        if aa != bb:
            parent[max(aa, bb)] = min(aa, bb)
    selected["site"] = [find(x) for x in selected.id]
    c.register("selected_facility_groups", selected[["id", "line", "site", "ownership_evidence"]])
    rec = c.execute("""WITH merged AS (SELECT x.site AS record_id, x.line, string_agg(DISTINCT f.class,' | ' ORDER BY f.class) AS class,
        string_agg(DISTINCT x.ownership_evidence,' | ' ORDER BY x.ownership_evidence) AS ownership_evidence,
        ST_Union_Agg(f.g) AS g FROM facilities f JOIN selected_facility_groups x USING(id) GROUP BY x.site,x.line)
        SELECT record_id,line,class,ownership_evidence, ST_Area_Spheroid(g)/4046.8564224 AS acres,
        ST_X(ST_PointOnSurface(g)) AS lon,ST_Y(ST_PointOnSurface(g)) AS lat FROM merged ORDER BY record_id""").df()
    rec["site_acres"] = rec.acres
    rec["source"] = "Overture 2026-10-21.0; public tags or public-institution containment; same-line overlaps dissolved"
    return valuation.locate_points(c, rec), pd.DataFrame(cov), dict(overlap_pairs=len(pairs), raw_accepted_sites=len(selected), dissolved_sites=len(rec))


def road_records():
    d, summary = roads.build_roads(write=True)
    d = d[d.case_line.ne("")].copy().reset_index(drop=True)
    d["record_id"] = ["road:" + str(i) for i in range(len(d))]
    d["line"] = d.case_line
    d["class"] = "highway"
    d["site_acres"] = d.one_mile_unit_acres
    d["ownership_evidence"] = "FHWA HPMS public owner code; ROW width design scenario; fee title/easement unresolved"
    d["source"] = d.source_file
    return valuation.county_price_sites(d), summary


def park_records():
    import duckdb
    p = HERE / "_cache" / "footprints" / "park_tracts.parquet"
    d = duckdb.read_parquet(str(p)).df()
    d["record_id"] = "park:" + d.id.astype(str) + ":" + d.tract.astype(str)
    d["line"] = "rec_sl"
    d["class"] = "park"
    d["ownership_evidence"] = "PAD-US fee ownership STAT/DIST/LOC; recreation designation"
    d["source"] = "USGS PAD-US 4.1 Fee Managers; positive recreation designations; overlap-corrected tract intersections"
    d["geo_level"] = "tract_intersection"
    return d


def road_sensitivities(road, engine, price_tables, case, rate):
    variants = {}
    for label, width, acreage in [("width_low", "row_width_low_ft", "acres_width_low"),
                                  ("width_high", "row_width_high_ft", "acres_width_high")]:
        d = road.copy()
        d["acres"] = d[acreage]
        d["site_acres"] = d[width] * 5280 / 43560
        valued = valuation.price_sites(d, engine, price_tables)
        for end in ["low", "high"]:
            coef = case[case.end.eq(end)].groupby("line").effective_key_times_response.mean()
            variants[end+"_"+label] = {a:float((valued["value_"+a] * valued.line.map(coef)).sum()/1e9*rate) for a in ARMS}
    for miles in [0.1,10.0]:
        d = road.copy()
        d["site_acres"] *= miles
        valued = valuation.price_sites(d, engine, price_tables)
        for end in ["low", "high"]:
            coef = case[case.end.eq(end)].groupby("line").effective_key_times_response.mean()
            variants[end+"_C_"+str(miles)+"_mile_units"] = float((valued.value_C * valued.line.map(coef)).sum()/1e9*rate)
    return variants


def summarize(records, case, contract, school, coverage, extras):
    long = []
    for (end, line), g in case.groupby(["end", "line"], sort=True):
        part = records[records.line.eq(line)]
        coef = float(g.effective_key_times_response.mean())
        for arm in ARMS:
            values = part["value_" + arm]
            group_values = part.get("group_weighted_value_" + arm, values).fillna(values)
            national = float(values.sum() / 1e9)
            group = float(group_values.sum() / 1e9 * coef)
            stock, structures = float(g.stock_charged_bn.iloc[0]), float(g.structures_bn.iloc[0])
            no_land = line.startswith("ent_other_")
            long.append(dict(end=end, line=line, arm=arm, valued_records=len(part), known_acres=float(part.acres.sum()),
                stock_charged_bn=stock, structures_bn=structures, national_mapped_value_bn=national,
                mapped_land_to_structures=national / structures if structures else 0.0,
                engine_key=float(g.engine_key.mean()), engine_response=float(g.engine_response.mean()),
                effective_key_times_response=coef, where_enrolled_factor=school["arms"][arm]["where_enrolled_ratio"] if line=="k12" else 1.0,
                geography_factor_status="measured pupil proxy" if line=="k12" else "not measured; national key applied uniformly",
                group_mapped_charge_case_bn=group * contract["rate"], group_mapped_charge_242pct_bn=group * 0.0242,
                group_mapped_charge_7pct_bn=group * 0.07,
                national_total_status="zero structures in case; no land increment" if no_land else "not identified; valued records only",
                ratio_status="0 by convention; case residual has no net structures" if no_land else "conditional mapped value / national case structures"))
    byline = pd.DataFrame(long)
    write_csv(byline, "land_by_line.csv")
    county = records.groupby(["line", "county"], dropna=False, sort=True).agg(
        records=("record_id", "size"), acres=("acres", "sum"), **{"value_"+a+"_bn": ("value_"+a, lambda x: float(x.sum()/1e9)) for a in ARMS}).reset_index()
    write_csv(county, "land_by_county.csv")
    concentration = county.groupby("county")[["value_"+a+"_bn" for a in ARMS]].sum()
    concentration = concentration.sort_values(["value_B_bn", "county"], ascending=[False, True]).reset_index()
    for a in ARMS:
        concentration["share_"+a] = concentration["value_"+a+"_bn"] / concentration["value_"+a+"_bn"].sum()
    write_csv(concentration, "county_concentration.csv")
    totals = {}
    variants = {}
    for end in ["low", "high"]:
        coef = case[case.end.eq(end)].groupby("line").effective_key_times_response.mean()
        for arm in ARMS:
            rows = byline[byline.end.eq(end) & byline.arm.eq(arm)]
            total = float(rows.group_mapped_charge_case_bn.sum())
            totals[end+"_"+arm] = dict(mapped_charge_case_bn=total, mapped_charge_242pct_bn=total * 0.0242 / contract["rate"],
                mapped_charge_7pct_bn=total * 0.07 / contract["rate"],
                mapped_national_value_bn=float(rows.national_mapped_value_bn.sum()),
                share_of_adopted_headline=[total / b for b in contract["band_bn"]],
                paired_share_of_adopted_headline=total/contract["band_bn"][0 if end=="low" else 1],complete_total_bn=None)
            keep = records[~records.county.isin(OMIT_COUNTIES)]
            gv = keep["group_weighted_value_"+arm].fillna(keep["value_"+arm])
            variants[end+"_"+arm+"_without_manhattan_sf_dc"] = float((gv * keep.line.map(coef)).sum()/1e9 * contract["rate"])
            keep_price=records[records.price_level.ne("state")]
            kept_gv=keep_price["group_weighted_value_"+arm].fillna(keep_price["value_"+arm])
            variants[end+"_"+arm+"_without_state_price_fallback"] = float(
                (kept_gv * keep_price.line.map(coef)).sum()/1e9*contract["rate"])
            road_omits = records[records["class"].eq("highway") & records.ownership.isin([11,12,40])]
            variants[end+"_"+arm+"_without_park_instrumentality_roads"] = total - float(
                (road_omits["value_"+arm] * road_omits.line.map(coef)).sum()/1e9 * contract["rate"])
    school_check = {}
    for a in ARMS:
        arm = school["arms"][a]
        value = arm["national_bn"] * school["inputs"]["pupil_share_s"] * arm["where_enrolled_ratio"] * contract["rate"]
        expected = arm["annual_charge_bn"]["case_flat_real"]["where_enrolled"]
        if abs(value-expected)>1e-10:
            raise ValueError("[BLOCKED] school-land input reproduction failed")
        school_check[a] = dict(reproduced_bn=value, source_bn=expected)
    out = dict(status="[DEGRADED] Complete public-land total not identified; mapped/design-scenario subtotal only; beside adopted case",
        complete_total_bn=None, case_key=contract["case_key"], case_rate=contract["rate"], paired_rate_requested=0.0242,
        paired_rate_note="2.42% applied uniformly as requested; the source paired-theta model has different federal and state/local rates and an item-6 receipt leg, neither bundled here",
        headline_band_bn=contract["band_bn"], totals=totals, variants=variants,
        top10_county_share_B=float(concentration.head(10).value_B_bn.sum()/concentration.value_B_bn.sum()),
        ownership_and_matching=coverage.astype(object).where(pd.notna(coverage),None).to_dict("records"),
        school_input_reproduction=school_check, **extras)
    write_json(out, "summary.json")
    return out, byline


def main():
    start = time.perf_counter()
    OUT.mkdir(parents=True, exist_ok=True)
    acquire_roads.main()
    acquire_universes.main()
    universes.main()
    acquire_footprints.main()
    footprints.main()
    subprocess.run(["node", str(HERE / "case_contract.cjs"), str(OUT / "case_contract.json")], check=True)
    contract = json.loads((OUT / "case_contract.json").read_text())
    case = physical_contract(contract)
    engine, price_tables = valuation.school_prices()
    c = valuation.connection()
    valuation.load_tracts(c)
    u = pd.read_csv(OUT / "universe_records.csv", dtype=str, keep_default_na=False)
    u[["lat", "lon"]] = u[["lat", "lon"]].apply(pd.to_numeric, errors="coerce")
    f, coverage, overlaps = match_facilities(c, u)
    airport, airport_info = airport_records(u, c)
    road, road_info = road_records()
    road_variants = road_sensitivities(road,engine,price_tables,case,contract["rate"])
    park = park_records()
    school, school_summary = school_records()
    subsets = []
    for label, data in [("facilities",f),("airports",airport),("roads",road),("parks",park)]:
        valued = valuation.price_sites(data, engine, price_tables)
        print(f"{label}: {len(valued):,} records, {valued.acres.sum():,.0f} acres; priced {int(valued.priced.sum()):,}", flush=True)
        subsets.append(valued)
    records = pd.concat([school,*subsets], ignore_index=True, sort=False)
    for arm in ARMS:
        col = "group_weighted_value_"+arm
        if col not in records:
            records[col] = np.nan
    footprint_info=json.loads((OUT/"footprint_sources.json").read_text())
    parks_info=footprint_info["park_tract_split"]
    coverage = pd.concat([coverage, pd.DataFrame([dict(facility_class="airport",map_records=airport_info["universe"],
        accepted_public_sites=airport_info["acreage_recorded"],unknown_ownership_sites=0,public_universe=airport_info["universe"],
        public_universe_matches=airport_info["acreage_recorded"],public_universe_match_rate=airport_info["footprint_coverage"],
        national_completeness=str(airport_info["acreage_missing"])+" missing acreage; whole-airport reference-point pricing"),
        dict(facility_class="school",map_records=school_summary["universe"]["non_virtual"],accepted_public_sites=school_summary["matching"]["matched"],
             unknown_ownership_sites=0,public_universe=school_summary["universe"]["non_virtual"],
             public_universe_matches=school_summary["matching"]["matched"],public_universe_match_rate=school_summary["matching"]["match_rate"],
             national_completeness="source school lane imputes unmatched schools; school national estimate, not new estate coverage"),
        dict(facility_class="park",map_records=parks_info["site_count"],accepted_public_sites=parks_info["matched_sites"],
             unknown_ownership_sites=0,public_universe=parks_info["site_count"],public_universe_matches=parks_info["matched_sites"],
             public_universe_match_rate=parks_info["matched_sites"]/parks_info["site_count"],
             national_completeness="selected public-fee recreation designations only; raw tract intersection rate, overlaps removed before price"),
        dict(facility_class="highway",map_records=len(road),accepted_public_sites=len(road),unknown_ownership_sites=0,
             public_universe=0,public_universe_matches=0,public_universe_match_rate=None,
             national_completeness="714/714 official mileage cells; ROW acreage modeled; source ownership/scope exclusions retained")])], ignore_index=True)
    write_csv(coverage, "coverage.csv")
    price_coverage = records.groupby(["class","price_level"],dropna=False,sort=True).agg(
        records=("record_id","size"),acres=("acres","sum"),priced=("priced","sum")).reset_index()
    write_csv(price_coverage,"price_coverage.csv")
    # Keep individual rederivable records in the ignored cache; tracked outputs are compact tables.
    cache_out = HERE / "_cache" / "priced_sites.parquet"
    detail_columns=["record_id","line","class","acres","site_acres","county","tract","geo_level","price_level",
                    "p24","ownership_evidence","source","priced"]
    detail_columns += ["value_"+a for a in ARMS]+["group_weighted_value_"+a for a in ARMS]
    records[detail_columns].to_parquet(cache_out,index=False)
    extras = dict(airport=airport_info, roads=road_info, parks=parks_info, facility_overlap=overlaps,
        road_scenarios_group_charge_bn=road_variants,
        priced_records=int(records.priced.sum()),unpriced_records=int((~records.priced).sum()),
        unpriced_acres=float(records.loc[~records.priced,"acres"].sum()),
        overlap_limit="Same-line facility/PAD overlaps removed. Road easements, utility corridors, and cross-class school/park/facility overlap unresolved; subtotal not a national ownership census or strict lower bound.")
    summary, byline = summarize(records,case,contract,school_summary,coverage,extras)
    provenance()
    for a in ARMS:
        print(a, {e:round(summary["totals"][e+"_"+a]["mapped_charge_case_bn"],4) for e in ["low","high"]})
    for r in byline[byline.arm.eq("B")].itertuples():
        print(f"{r.end:4} {r.line:18} mapped land/structures {r.mapped_land_to_structures:.6f}, charge {r.group_mapped_charge_case_bn:.6f}bn")
    print(summary["status"])
    # The brief's single-command rerun must execute every new script, including
    # scientific validation. Tests read the outputs and never recurse into build.
    subprocess.run([sys.executable,"-I","-m","pytest",str(HERE/"test_lane.py"),"-q","-p","no:cacheprovider"],check=True)
    rss_scale=1 if sys.platform=="darwin" else 1024
    print(json.dumps(dict(seconds=round(time.perf_counter()-start,3),peak_rss_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*rss_scale,
                          child_peak_rss_bytes=resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss*rss_scale)))


if __name__ == "__main__":
    main()
