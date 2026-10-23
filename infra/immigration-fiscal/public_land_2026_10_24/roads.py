"""Highway right-of-way acreage from HPMS miles, with explicit width assumptions.

Native-First: use published FHWA tabulations/SQL aggregates rather than road
polygon downloads. Read cached downloads in isolated Python (-I).

Mainline sections (facility types 1/2) supply classes 1-5 and urban class 6;
County Summary 2024 supplies rural class 6 and all local (class 7) miles. These
sets are disjoint. Public ownership maps to the case's federal highways,
state/local nontoll highways and state/local toll enterprise lines. Tribal roads
join the BEA local-government account; explicit military owners are excluded
from the federal nondefense stock. Private and unknown owners remain in coverage.

Widths are design-based assumptions, never observed ROW widths. FHWA/ITE
Traffic Calming: State of the Practice (1999), Tables 10.5/10.6, reproduces
AASHTO's urban local 50 feet/common and urban collector 40-60 feet. NCDOT
Roadway Design Manual chapter 9 pp.9-1/9-1 continued gives the other ranges.
The central is their midpoint; local urban is 50 ft. No extra lane formula
is introduced, so 4-lane freeway / 2-or-4-lane rural templates are explicit.

    uv run --no-project python3 -I {lane}/roads.py
"""
import hashlib
import json
from pathlib import Path
import re
import resource
import subprocess
import time

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
CACHE = HERE / "_cache" / "roads"
OUT = HERE / "derived"
STATES = {
    1: "Alabama", 2: "Alaska", 4: "Arizona", 5: "Arkansas", 6: "California", 8: "Colorado",
    9: "Connecticut", 10: "Delaware", 11: "District of Columbia", 12: "Florida", 13: "Georgia",
    15: "Hawaii", 16: "Idaho", 17: "Illinois", 18: "Indiana", 19: "Iowa", 20: "Kansas",
    21: "Kentucky", 22: "Louisiana", 23: "Maine", 24: "Maryland", 25: "Massachusetts",
    26: "Michigan", 27: "Minnesota", 28: "Mississippi", 29: "Missouri", 30: "Montana",
    31: "Nebraska", 32: "Nevada", 33: "New Hampshire", 34: "New Jersey", 35: "New Mexico",
    36: "New York", 37: "North Carolina", 38: "North Dakota", 39: "Ohio", 40: "Oklahoma",
    41: "Oregon", 42: "Pennsylvania", 44: "Rhode Island", 45: "South Carolina", 46: "South Dakota",
    47: "Tennessee", 48: "Texas", 49: "Utah", 50: "Vermont", 51: "Virginia", 53: "Washington",
    54: "West Virginia", 55: "Wisconsin", 56: "Wyoming",
}
# One declaration drives both classification and the parsed-primary-codebook gate.
# FHWA HPMS Field Manual 2024, Ownership Item 6, printed pp.38-39.
OWNER_CODES = {
    1: ("state_local", "State Highway Agency"),
    2: ("state_local", "County Highway Agency"),
    3: ("state_local", "Town or Township Highway Agency"),
    4: ("state_local", "City or Municipal Highway Agency"),
    11: ("state_local", "State Park, Forest, or Reservation Agency"),
    12: ("state_local", "Local Park Forest, or Reservation Agency"),
    21: ("state_local", "Other State Agency"),
    25: ("state_local", "Other Local Agency"),
    26: ("private", "Private (other than Railroad)"),
    27: ("private", "Railroad"),
    31: ("state_local", "State Toll Authority"),
    32: ("state_local", "Local Toll Authority"),
    40: ("state_local", "Other Public Instrumentality (i.e. Airport)"),
    50: ("tribal", "Indian Tribe Nation"),
    60: ("federal", "Other Federal Agency"),
    62: ("federal", "Bureau of Indian Affairs"),
    63: ("federal", "Bureau of Fish and Wildlife"),
    64: ("federal", "U.S. Forest Service"),
    66: ("federal", "National Park Service"),
    67: ("federal", "Tennessee Valley Authority"),
    68: ("federal", "Bureau of Land Management"),
    69: ("federal", "Bureau of Reclamation"),
    70: ("federal", "U.S. Army Corps of Engineers"),
    72: ("federal", "U.S. Air Force"),
    73: ("federal", "U.S. Navy/Marines"),
    74: ("federal", "U.S. Army"),
    80: ("other_or_missing", "Other"),
}
STATE_LOCAL = {code for code, (level, _) in OWNER_CODES.items() if level == "state_local"}
FEDERAL = {code for code, (level, _) in OWNER_CODES.items() if level == "federal"}
MILITARY = {72, 73, 74}  # Explicit service ownership; FAAt701 line49 is nondefense.
FUNCTIONS = {1: "interstate", 2: "other_freeway_expressway", 3: "other_principal_arterial",
             4: "minor_arterial", 5: "major_collector", 6: "minor_collector", 7: "local"}


def pdf_text(name, layout=True):
    path = CACHE / name
    if not path.exists() or path.read_bytes()[:4] != b"%PDF":
        raise RuntimeError(f"[BLOCKED] missing valid primary ROW source {path}")
    args = ["pdftotext", *(["-layout"] if layout else []), str(path), "-"]
    return subprocess.run(args, check=True,
                          text=True, capture_output=True).stdout


def parse_owner_codes(text):
    """Pure parser for the 2024 manual's ownership table (including page break).

    Fixture tests can pass text directly; only the production caller reads a PDF.
    The section anchors exclude the following maintenance-operations code table.
    """
    _, start, block = text.partition("OWNERSHIP (Ownership, Item 6)")
    block, stop, _ = block.partition("COUNTY_ID (County ID, Item 63)")
    table, value_text, _ = block.partition("Value Text:")
    if not start or not stop or not value_text:
        raise ValueError("[BLOCKED] ownership table anchors absent from primary manual")
    codes = {}
    for code, label in re.findall(r"^\s*(\d{1,2})[ \t]+([A-Za-z][^\n]+)$", table, flags=re.MULTILINE):
        if int(code) in codes:
            raise ValueError(f"[BLOCKED] duplicate primary ownership code {code}")
        codes[int(code)] = label.strip()
    if not codes:
        raise ValueError("[BLOCKED] primary ownership table is empty")
    return codes


def validate_owner_codes(codes):
    """Fail on missing/new codes or a semantic label change; preserve exact source labels."""
    def words(label):
        return re.sub(r"[^a-z0-9]+", " ", label.lower()).strip()
    expected = {code: words(label) for code, (_, label) in OWNER_CODES.items()}
    actual = {int(code): words(label) for code, label in codes.items()}
    if actual != expected:
        differing = sorted(set(actual) ^ set(expected) |
                           {code for code in set(actual) & set(expected) if actual[code] != expected[code]})
        raise ValueError(f"[BLOCKED] HPMS owner-code meaning changed: {differing}")
    return codes


def validate_tribal_scope(text):
    """Pure check of BEA's sector declaration; legal sovereignty is a different frame."""
    normalized = " ".join(text.split())
    if "Tribal governments are now treated as local governments" not in normalized:
        raise ValueError("[BLOCKED] missing BEA primary tribal-government sector declaration")
    return True


def validate_federal_road_scope(rows):
    """Pure check of the primary Fixed Assets table's federal road branch."""
    if (rows.get(38, ("", ""))[0].strip() != "Nondefense" or
            rows.get(49, ("", ""))[0].strip() != "Highways and streets" or
            rows[49][1].strip() != "k1gndef1sq00"):
        raise ValueError("[BLOCKED] BEA federal-highway stock scope no longer matches nondefense")
    return True


def scope_sources():
    """Parse the already acquired BEA authorities; do not infer scope from owner names alone."""
    tribal = CACHE.parent / "universes" / "scope_bea_tribal_gce2005.pdf"
    # Reading order preserves article columns; -layout interleaves their rows.
    validate_tribal_scope(pdf_text(tribal, layout=False))
    fa = HERE.parent / "school_capital_return_2026_09_26" / "_cache" / "fa_Section7All_xls.xlsx"
    if not fa.exists():
        raise RuntimeError(f"[BLOCKED] primary BEA stock scope missing: {fa}")
    frame = pd.read_excel(fa, sheet_name="FAAt701-A", header=None)
    line = pd.to_numeric(frame[0], errors="coerce")
    selected = {int(row.iloc[0]): (str(row.iloc[1]), str(row.iloc[2]))
                for _, row in frame[line.isin((38, 49))].iterrows()}
    validate_federal_road_scope(selected)
    return {
        "tribal_rule": "BEA SCB October2005 printedp8: tribal governments treated as local; casinos as enterprises",
        "federal_rule": "BEA FAAt701-A line49 k1gndef1sq00: federal NONDEFENSE highways; explicit military owners72/73/74 excluded; Army Corps70 retained",
        "read_only_sources": [{"path": str(p.relative_to(HERE.parent)), "sha256": hashlib.sha256(p.read_bytes()).hexdigest()}
                              for p in (tribal, fa)],
    }


def case_line_for(owner, toll_status):
    """Map HPMS ownership onto the case's BEA sector/defense scope, not legal sovereignty."""
    if owner in MILITARY:
        return ""
    level = owner_level(owner)
    if level in {"state_local", "tribal"}:
        return "ent_tolls_sl" if toll_status == "toll_associated" else "hwy_sl"
    return "hwy_fed" if level == "federal" else ""


def width_parameters():
    """Read template bounds from downloaded primary text; central = midpoint.

    NCDOT templates supplement the two AASHTO urban street templates reproduced
    by FHWA. FHWA PDDM does not supply a nationally representative ROW width.
    None of the template bounds is a confidence interval or measurement.
    """
    nc = " ".join(pdf_text("ncdot_row.pdf").replace("′", "'").split())
    fw = " ".join(pdf_text("fhwa_traffic_calming1999.pdf").split())
    pattern = r"from (\d+)' to (\d+)' for rural projects and (\d+)' to (\d+)' for urban projects"
    freeway = re.search(pattern, nc)
    rural = re.search(r"2-lane arterial or collector would be from (\d+)' to (\d+)'\. "
                      r"For a 4-lane section of roadway, a width of (\d+)' to (\d+)'", nc)
    urban = re.search(r"urban arterial is between (\d+)' to (\d+)'", nc)
    local = re.search(r"Generally, a typical width of (\d+)' to (\d+)' will be adequate", nc)
    ul = re.search(r"Right-of-way width (\d+) feet common (\d+) feet", fw)
    # Table 10.6 wraps "width" onto the next physical line. pdftotext's
    # row-wise column order puts the numerical cells before that word.
    uc = re.search(r"Right-of-way (\d+) to (\d+) feet", fw)
    if not all((freeway, rural, urban, local, ul, uc)):
        raise RuntimeError("[BLOCKED] primary width text changed or did not parse")

    def band(lo, hi):
        return (float(lo), (float(lo) + float(hi)) / 2, float(hi))
    return {
        "rural_freeway": band(*freeway.groups()[:2]),
        "urban_freeway": band(*freeway.groups()[2:]),
        "rural_2_lane_arterial_collector": band(*rural.groups()[:2]),
        "rural_4_lane_arterial_collector": band(*rural.groups()[2:]),
        "urban_arterial": band(*urban.groups()),
        "rural_local": band(*local.groups()),
        "urban_local": (float(ul.group(2)), float(ul.group(1)), float(ul.group(1))),
        "urban_collector": band(*uc.groups()),
    }


def width_for(functional_class, area_type, through_lanes, parameters):
    """Return low/central/high ROW feet and the primary template identifier."""
    fc = int(functional_class)
    if fc in (1, 2):
        key = f"{area_type}_freeway"
    elif fc == 7:
        key = f"{area_type}_local"
    elif area_type == "rural":
        nlanes = 4 if through_lanes >= 4 else 2
        key = f"rural_{nlanes}_lane_arterial_collector"
    elif fc in (3, 4):
        key = "urban_arterial"
    else:
        key = "urban_collector"
    return (*parameters[key], key)


def owner_level(owner):
    return OWNER_CODES.get(owner, ("other_or_missing", "unreported"))[0]


def normalized_mileage():
    rows = []
    for code in STATES:
        path = CACHE / f"sections_{code:02d}_2024.json"
        if not path.exists():
            raise RuntimeError(f"[BLOCKED] road source missing: {path}")
        data = json.loads(path.read_text())
        for r in data:
            rows.append(dict(state_id=code, county_id=int(r.get("county_id", 0) or 0),
                             functional_class=int(r["f_system"]), urban_id=int(r["urban_id"]),
                             ownership=int(r.get("ownership", 0) or 0), toll_id=str(r.get("toll_id", "")).strip(),
                             through_lanes=int(r.get("through_lanes", 0) or 0),
                             centerline_miles=float(r["miles"]), n_sections=int(r["n"]),
                             source_table="HPMS spatial mainline (types 1/2)",
                             source_file=str(path.relative_to(HERE))))
    co = pd.read_csv(CACHE / "hpms_county_2024.csv")
    co = co[co.stateid.isin(STATES) & (co.fsystem.eq(7) | (co.fsystem.eq(6) & co.urbanid.eq(99999)))]
    if set(co.stateid) != set(STATES):
        raise RuntimeError("[BLOCKED] county summary does not cover 50 states and DC")
    for r in co.itertuples(index=False):
        rows.append(dict(state_id=int(r.stateid), county_id=int(r.countyid), functional_class=int(r.fsystem),
                         urban_id=int(r.urbanid), ownership=int(r.ownership), toll_id="",
                         through_lanes=0, centerline_miles=float(r.systemlength), n_sections=0,
                         source_table="HPMS county summary (all local/rural minor collector)",
                         source_file="_cache/roads/hpms_county_2024.csv"))
    df = pd.DataFrame(rows)
    if not np.isfinite(df.centerline_miles).all() or (df.centerline_miles < 0).any():
        raise RuntimeError("[BLOCKED] invalid road mileage")
    df["county_fips"] = df.state_id.map(lambda n: f"{n:02d}") + df.county_id.map(lambda n: f"{n:03d}")
    df["county_known"] = df.county_id.gt(0)
    df["area_type"] = np.where(df.urban_id.eq(99999), "rural", "urban")
    df["functional_class_name"] = df.functional_class.map(FUNCTIONS)
    df["ownership_level"] = df.ownership.map(owner_level)
    # Primary ownership 31/32 identifies state/local toll authorities. A nonblank
    # positive facility ID also locates toll-associated sections, but may include
    # managed lanes. It is a proxy for whole-road toll acreage, not a toll-only width.
    valid_toll = ~df.toll_id.str.lower().isin(("", "0", "0.0", "none", "null", "-1", "-9999"))
    df["toll_status"] = np.where(df.ownership.isin((31, 32)) | valid_toll, "toll_associated", "non_toll_or_unreported")
    df["bea_account_level"] = df.ownership_level.replace({"tribal": "state_local"})
    df["case_line"] = [case_line_for(int(owner), str(toll)) for owner, toll in zip(df.ownership, df.toll_status)]
    df["case_scope"] = np.where(df.ownership.isin(MILITARY), "explicit_defense_excluded",
                                np.where(df.case_line.ne(""), "included", "not_verified_public_account"))
    return df


def closure(df):
    """No calibration: compare measured spatial/summary miles to official HM-20."""
    hm = pd.read_excel(CACHE / "hm20.xlsx", sheet_name="A", header=None)
    by_name = {str(r.iloc[0]).strip(): r for _, r in hm.iterrows() if str(r.iloc[0]).strip() in STATES.values()}
    if set(by_name) != set(STATES.values()):
        raise RuntimeError("[BLOCKED] HM-20 state list changed")
    rows = []
    for code, name in STATES.items():
        for area, first in (("rural", 1), ("urban", 9)):
            for fc in range(1, 8):
                actual = float(by_name[name].iloc[first + fc - 1])
                measured = float(df.loc[df.state_id.eq(code) & df.area_type.eq(area) & df.functional_class.eq(fc),
                                        "centerline_miles"].sum())
                rows.append(dict(state_id=code, state=name, area_type=area, functional_class=fc,
                                 official_hm20_miles=actual, extracted_miles=measured,
                                 difference_miles=measured-actual,
                                 coverage_ratio=measured/actual if actual > 0 else None))
    return pd.DataFrame(rows)


def build_roads(write=True):
    start = time.perf_counter()
    primary_owner_codes = validate_owner_codes(parse_owner_codes(pdf_text("hpms_field_manual2024.pdf")))
    scope = scope_sources()
    parameters = width_parameters()
    df = normalized_mileage()
    unknown = sorted(set(df.ownership) - set(primary_owner_codes) - {0})
    if unknown:
        raise RuntimeError(f"[BLOCKED] ownership values not in primary HPMS manual: {unknown}")
    widths = [width_for(r.functional_class, r.area_type, r.through_lanes, parameters) for r in df.itertuples()]
    for i, col in enumerate(("row_width_low_ft", "assumed_row_width_ft", "row_width_high_ft", "width_template")):
        df[col] = [r[i] for r in widths]
    df["acres"] = df.centerline_miles * 5280 * df.assumed_row_width_ft / 43560
    df["acres_width_low"] = df.centerline_miles * 5280 * df.row_width_low_ft / 43560
    df["acres_width_high"] = df.centerline_miles * 5280 * df.row_width_high_ft / 43560
    df["one_mile_unit_acres"] = df.assumed_row_width_ft * 5280 / 43560
    df["price_unit_note"] = "1-mile segment assumed for nonlinear arm C; not cadastral parcel size"
    df = df.sort_values(["state_id", "county_id", "functional_class", "urban_id", "ownership", "toll_id", "through_lanes", "source_table"]).reset_index(drop=True)
    cl = closure(df)
    if cl.difference_miles.abs().max() > 0.01:
        raise RuntimeError("[BLOCKED] extracted road mileage no longer closes to HM-20 within 0.01 mile per cell")
    official = float(cl.official_hm20_miles.sum())
    total = float(df.centerline_miles.sum())
    public = df.case_line.ne("")
    military = df.ownership.isin(MILITARY)
    tribal = df.ownership.eq(50)
    summary = {
        "status": "design-width scenario; mileage measured; no national observed ROW acreage",
        "official_hm20_miles": official,
        "extracted_miles_all_owners": total,
        "national_mileage_coverage_ratio": total/official,
        "mileage_closure_cells": int(len(cl)),
        "max_absolute_cell_difference_miles": float(cl.difference_miles.abs().max()),
        "primary_owner_codes": primary_owner_codes,
        "owner_code_source": "HPMS Field Manual 2024, Ownership Item 6, printed pp.38-39; _cache/roads/hpms_field_manual2024.pdf",
        "account_scope_authorities": scope,
        "public_miles_used": float(df.loc[public, "centerline_miles"].sum()),
        "all_public_owner_miles_including_explicit_defense": float(df.loc[public | military, "centerline_miles"].sum()),
        "explicit_military_excluded_miles": float(df.loc[military, "centerline_miles"].sum()),
        "explicit_military_excluded_acres": float(df.loc[military, "acres"].sum()),
        "tribal_included_miles": float(df.loc[tribal, "centerline_miles"].sum()),
        "tribal_included_acres": float(df.loc[tribal, "acres"].sum()),
        "public_acres_width_central": float(df.loc[public, "acres"].sum()),
        "public_acres_width_low": float(df.loc[public, "acres_width_low"].sum()),
        "public_acres_width_high": float(df.loc[public, "acres_width_high"].sum()),
        "unknown_county_public_miles": float(df.loc[public & ~df.county_known, "centerline_miles"].sum()),
        "county_count_public": int(df.loc[public & df.county_known, "county_fips"].nunique()),
        "excluded_ownership_miles": df.loc[~public].groupby("ownership_level").centerline_miles.sum().to_dict(),
        "width_parameters_ft_low_central_high": parameters,
        "width_sources": {
            "urban_local_collector": "FHWA/ITE Traffic Calming: State of the Practice (1999), Tables 10.5 and 10.6, printed pages 190 and 193; AASHTO columns; 41 ft urban-local lower scenario from DelDOT column",
            "other_classes": "NCDOT Roadway Design Manual chapter 9 pp.9-1 and 9-1 continued (revisions 2007/2017), supplement to the FHWA/AASHTO templates",
        },
        "caveats": [
            "Widths are typical design cross-sections transferred nationally; not measured or representative existing ROW widths.",
            "No national confidence interval; low/high widths are design-template scenarios.",
            "Toll ID includes managed-lane sections; assigning the entire section's ROW to tolls is a proxy and may overassign toll land.",
            "No toll ID in the county summary: lower-class tolls identified only by toll authority ownership 31/32.",
            "No calibration to HM-20; spatial gaps and overlaps can change county values.",
            "1-mile unit for arm C (test 0.1 and 10 miles); HPMS dynamic-segmentation row length is not a land parcel.",
            "Road, utility and park rights-of-way may overlap; easements cannot automatically be sold as fee-simple land.",
            "Explicit military owners72/73/74 are excluded from the nondefense account; owner70 Army Corps retained. Alternatives retain their acreage.",
            "Tribal owner50 is state/local for the BEA account, while HPMS ownership_level remains tribal. Land restrictions and federal trust interests remain unresolved.",
            "Other federal owners include roads on public park lands; these are highway ROW only, not the full federal estate.",
        ],
    }
    if write:
        OUT.mkdir(exist_ok=True)
        df.to_csv(OUT / "roads_county_acres.csv", index=False, lineterminator="\n", float_format="%.10g")
        cl.to_csv(OUT / "roads_mileage_closure.csv", index=False, lineterminator="\n", float_format="%.10g")
        alternatives = df[military | tribal].copy()
        alternatives["scope_variant"] = np.where(alternatives.ownership.isin(MILITARY), "include_explicit_military", "exclude_tribal")
        alternatives["alternative_case_line"] = np.where(alternatives.ownership.isin(MILITARY), "hwy_fed", alternatives.case_line)
        alternatives["delta_sign"] = np.where(alternatives.ownership.isin(MILITARY), 1, -1)
        alternatives.to_csv(OUT / "roads_scope_alternatives.csv", index=False, lineterminator="\n", float_format="%.10g")
        (OUT / "roads_summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True, allow_nan=False) + "\n")
    print(f"roads: {total:,.3f}/{official:,.3f} official miles ({total/official:.3%}); "
          f"{summary['public_acres_width_central']:,.0f} public acres; "
          f"{summary['county_count_public']} counties; {time.perf_counter()-start:.2f}s; "
          f"maxrss_raw={resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}", flush=True)
    return df, summary


if __name__ == "__main__":
    build_roads()
