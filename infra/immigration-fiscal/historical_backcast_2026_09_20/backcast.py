#!/usr/bin/env python3
"""Back-cast the 2024 Mexican-origin fiscal concepts to 2005-2024.

Native-First: consumes the complete account's exports, the pinned BEA workbooks
and ACS series; no new microdata estimator. Measured by year: government current
receipts and expenditures (BEA 3.1), the GDP implicit deflator (1.1.9), midperiod
population (7.1), ACS Mexican-origin counts and relative per-capita income.
Assumed: the group's 2024 per-person position relative to the nation. Three rules:

  flat    per-person cost constant in 2024 dollars
  ratio   receipts and charged spending keep their 2024 ratios to national per capita
   income  as ratio, with receipts scaled by relative per-capita income (unit
           elasticity). Live oct16 additionally applies per-part pension rules:
           Part A worker counts, OASDI workers x finite PIA earnings response.

This is not a measured historical account. No year before 2024 has group taxes,
benefits or services observed here.

Cases (--case), one entry each in LATER_CASES. The default is oct16, the live personal case, written to derived/oct16/.
Its historical base and items are separate components; the superseded oct07 concepts are not computed beside it.
Explicit earlier-case commands remain available for scratch regressions. sept27 adds the main case of 2026-09-27
as the `*_sept27_*` concepts: the schools case's cost at the case's end specifications under these
rules, plus each addition carried back with its own national series (see ADDITIONS).
sept26_schools adds the main case with schools at full average cost (`*_schools_full_*`); sept26
(CBO's one-year school response, 0.63-0.66) adds the `*_sept26_*` concepts. Each case also writes
every earlier case's concepts, which do not change value by value. An earlier case with --out-dir DIR
writes the files as they stood on that case, byte for byte.

sept29 (the main case adopted on 2026-09-29, candidate v4) adds the `*_sept29_*` concepts and writes
derived/sept29/ beside the default files, which stay September 27's. Its base is again the schools case at the
case's end specifications; its parts are September 27's four additions, the capital return at the case's values
and the change from September 27 line by line (case_components.cjs --case sept29), each carried back with its
own national series (V4_RECEIPT_CELLS and v4_series()).

oct05 (the main case adopted on 2026-10-05, v5: September 29 plus the 3.04M descendants of Mexican immigrants who no
longer report Mexican origin, counted whole) adds the `*_oct05_*` concepts and writes derived/oct05/. Every September 29
part is carried back as --case sept29 carries it; the lineage line is added line by line (case_components.cjs --case
oct05, the v5_ parts and the capital return's change), each part on its own national series (v5_series()) times the
identified third-plus generation's population-share path instead of the group's. The lineage's own count by year (the
third-plus by year times the attrition rate) is not measured, so its 2024 ratio to the identified third-plus is held
[ASSUMPTION]; the third-plus by year is the CPS ASEC count in inputs/cps_g3plus_path.csv (cps_g3plus_path.py). Under
the flat rule the lineage's parts keep their 2024 value per identified third-plus person.

oct07 (main case v6: October 5 plus an item registry) adds the `*_oct07_*` concepts and writes derived/oct07/. Every
October 5 part is carried back as --case oct05 carries it; each item's change is added with its own parts
(case_components.cjs --case oct07, the v6_<item>_<path>_<line> parts and the capital return's change by path), each on
its line's national series (v6_series, the September 29 rules) times the group's population-share path where the part is
the union's (path union) and the third-plus path where it is the added people's (path lineage). An item's capital
offset component (of_component) follows its component's stock. Its backcast_annual.csv also carries the lineage's count
by year and the band's ends per lineage member (per_lineage_member()), which v6's per-member figures divide by.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
from functools import lru_cache
from pathlib import Path
from typing import NamedTuple

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from cache_contract import (ANNUAL_CACHE, ANNUAL_MANIFEST, ANNUAL_COLUMNS,
                            ANNUAL_KEY, verify_cached_annual)

ROOT = HERE.parents[2]
FISCAL = ROOT / "infra/immigration-fiscal"
PINNED = {"Section1All_xls.xlsx": "238ba851c9a4932d91a0dedb1b3f2e6c6d37574d154a54267da18b9cb0921a19",
          "Section3All_xls.xlsx": "69b5c7aefb38675324887ce31d6feb4fcde7c903ab952db7328da0813096615e",
          "Section7All_xls.xlsx": "ce107c8ce92393613c0abae38156afcfaef8ab571eedf0302dc09ca44738b9ef",
          "fa_Section7All_xls.xlsx": "e67f534560f111575d5314bab8fe4d62dd696c2e49f421eaa2fa73f25dea12ae"}
YEARS = list(range(2005, 2025))
def write_cached_annual(frame: pd.DataFrame, out_dir: Path) -> None:
    """Keep the typed annual grid outside git, with a deterministic tracked pin."""
    if frame.duplicated(ANNUAL_KEY).any():
        raise ValueError("[BLOCKED] duplicate annual parts full key")
    cache_root = HERE if out_dir.resolve() == (HERE / "derived/oct16").resolve() else out_dir
    path = cache_root / ANNUAL_CACHE
    path.parent.mkdir(parents=True, exist_ok=True)
    frame.round(6).to_csv(path, index=False, lineterminator="\n")
    manifest = dict(schema_version=1, case="oct16", path=ANNUAL_CACHE.as_posix(),
                    sha256=hashlib.sha256(path.read_bytes()).hexdigest(), bytes=path.stat().st_size,
                    rows=len(frame), columns=ANNUAL_COLUMNS, full_key=ANNUAL_KEY)
    (out_dir / ANNUAL_MANIFEST.name).write_text(json.dumps(manifest, indent=2) + "\n")


# BEA 3.12 veterans' other benefits begin in 2015 in the pinned workbook.
# These are the only permitted blanks, identified by source series AND year.
STRUCTURAL_ZEROS = {("T31200-A:20", year) for year in range(2005, 2015)}


def checked_years(values: pd.Series, reference: str) -> pd.Series:
    """Reject missing observations unless the exact source/year is a structural zero."""
    out = values.reindex(YEARS).copy()
    missing = [int(y) for y in out.index[out.isna()]]
    bad = [y for y in missing if (reference, y) not in STRUCTURAL_ZEROS]
    if bad or not np.isfinite(out.dropna()).all():
        raise ValueError(f"[BLOCKED] {reference}: missing/nonfinite observations {bad}")
    for year in missing:
        out.loc[year] = 0.0
    return out
PROFILES = {"net_cost_cbo_informed": "cbo_category_lag_non_school_full",
            "net_cost_full_proportional": "proportional_reference"}


class Case(NamedTuple):
    lane: str                   # main-case lane
    tag: str                    # concept tag
    base_variant: str           # the lane's band variant for the case it starts from
    base_tag: str               # that case's tag
    base_receipts: str          # that case's key in the lane's summary.json group_receipts_bn
    parts: str | None = None    # additions carried back by their own series (case_components.cjs output)
    rekeyed_receipts: str = "adopted"   # the group_receipts_bn key that differs from base_receipts by the re-key alone
    out: str | None = None      # the case's own directory under derived/ (None: derived/)
    lineage: bool = False       # its parts include the lineage's (v5_), carried at the third-plus path
    items: bool = False         # its parts include the items' (v6_), each on its path's population path


# Main cases after September 24, in adoption order. Receipts are matched by tag within concept names, so
# no tag may contain another ("_sept26_" would also match "_sept26_schools_"). The default run is DEFAULT_CASE's.
SEPT29_LANE = "main_case_2026_09_29"
OCT05_LANE = "main_case_2026_10_05"
OCT07_LANE = "main_case_2026_10_07"
OCT14_LANE = "main_case_2026_10_14"
OCT15_LANE = "main_case_2026_10_15"
OCT16_LANE = "main_case_2026_10_16"
LATER_CASES = {"sept26": Case("main_case_2026_09_26", "_sept26_", "adopted_2026_09_24", "_corrected_", "adopted_2026_09_24"),
               "sept26_schools": Case("main_case_schools_full_2026_09_26", "_schools_full_", "adopted_2026_09_26",
                                      "_sept26_", "adopted_2026_09_26"),
               "sept27": Case("main_case_long_run_2026_09_27", "_sept27_", "schools_case", "_schools_full_",
                              "adopted_2026_09_26_schools", "case_components_sept27.json"),
               # Like September 27 it starts from the schools case; its receipts differ from the schools case's by
               # September 27's re-key and by its own receipt changes, which its v4 parts carry.
               "sept29": Case(SEPT29_LANE, "_sept29_", "schools_case", "_schools_full_", "adopted_2026_09_26_schools",
                              "case_components_sept29.json", "adopted_2026_09_27", "sept29"),
               # September 29's parts and the lineage's on the same schools-case base; case_components.cjs gates that the
               # case less the lineage is September 29's band (the case lane's sept29_case row).
               "oct05": Case(OCT05_LANE, "_oct05_", "schools_case", "_schools_full_", "adopted_2026_09_26_schools",
                             "case_components_oct05.json", "adopted_2026_09_27", "oct05", True),
               # October 5's parts and the items' on the same schools-case base; case_components.cjs gates that the case
               # less the items is October 5's band (the case lane's oct05_case row).
               "oct07": Case(OCT07_LANE, "_oct07_", "schools_case", "_schools_full_", "adopted_2026_09_26_schools",
                             "case_components_oct07.json", "adopted_2026_09_27", "oct07", True, True),
               "oct14": Case(OCT14_LANE, "_oct14_", "schools_case", "_schools_full_", "adopted_2026_09_26_schools",
                             "case_components_oct14.json", "adopted_2026_09_27", "oct14", True, True),
               "oct15": Case(OCT15_LANE, "_oct15_", "schools_case", "_schools_full_", "adopted_2026_09_26_schools",
                             "case_components_oct15.json", "adopted_2026_09_27", "oct15", True, True),
               "oct16": Case(OCT16_LANE, "_oct16_", "schools_case", "_schools_full_", "adopted_2026_09_26_schools",
                             "case_components_oct16.json", "adopted_2026_09_27", "oct16", True, True)}
DEFAULT_CASE = "oct16"
# October 5: the identified third-plus generation by year (CPS ASEC, cps_g3plus_path.py), the lineage's path.
G3PLUS_PATH = HERE / "inputs/cps_g3plus_path.csv"
# The concepts carried per member of each case's lineage, under the ratio and income rules.
PER_LINEAGE_MEMBER = {case: tuple(f"net_cost_cbo_informed_{case}_{end}" for end in ("low", "high"))
                      for case in ("oct07", "oct14", "oct15", "oct16")}
INCOME_RECEIPTS = {"federal_income_tax", "state_local_income_tax", "employee_oasdi", "employee_hi",
                   "employer_oasdi", "employer_hi", "self_employment_oasdi_hi", "other_domestic_social_contributions",
                   "corporate_capital", "corporate_labor", "remaining_production_property", "other_production_taxes",
                   "general_sales_tax", "excise_selective_sales", "customs_duties", "personal_current_transfers"}
# A case's additions and the national series each is carried back with: the account's own source cell
# (full_account_spending_2026_09_20/derived/categories.csv; the receipt in model.json), real, 2024 = 1,
# times the group's population-share path, the share path this back-cast gives every line. The capital
# return follows each component's BEA net stock (CAPITAL_LINES).
ADDITIONS = {"long_run_economic_affairs_services": ("spending", "economic_affairs_services"),
             "long_run_recreation_culture": ("spending", "recreation_culture"),
             "rental_assistance": ("spending", "housing_subsidies"),
             "enterprise_surplus": ("receipt", "enterprise_surplus")}
RECEIPT_CELLS = {"enterprise_surplus": "T30100-A:19"}     # NIPA 3.1 line 19, current surplus of government enterprises
# Each capital component's charged stock as lines of FA Table 7.1 (current-cost net stock, yearend), from the
# capital lane's bea_source, averaged over the year's two yearends as that lane does. Fixed 2024 weights make
# each line set reproduce the component's charged stock. The eleven enterprise components are all of line 79,
# government enterprise fixed assets, with one key and one response, so they follow line 79 together.
FA_WORKBOOK = FISCAL / "school_capital_return_2026_09_26/_cache/fa_Section7All_xls.xlsx"
CAPITAL_LINES = {"k12": (62, 56, 73), "college": (62,), "pos_sl": (63,), "pos_fed": (45,), "health_sl": (61,),
                 "health_fed": (43,), "gps_sl": (59,), "gps_fed": (41,), "hwy_sl": (67,), "rec_sl": (64, 62),
                 "hwy_fed": (49,), "air_fed": (47,), "rec_fed": (46,)}
ENTERPRISE_FA_LINE = 79
# September 29: the national series of each part of the change from September 27 (case_components.cjs --case sept29),
# NIPA cells summed ($ millions by year). A receipt line follows its own cells (NIPA 3.1, 3.4-3.6; the cells of the
# debt lane's RECEIPT_SERIES_V4, both levels of government together), a spending line its categories.csv source cells,
# a synthetic spending line (roads by miles, state pricing) its parent's. Four rules replace a line's own cells:
#   - enterprise_surplus: its change is public housing's deficit moved to its own line (NIPA 3.8 line 13);
#   - housing_enterprise_surplus: that deficit and the federal operating subsidy consolidated with it, a fixed part of
#     federal housing subsidies (NIPA 3.13 line 4; the part is the line's national total less line 13);
#   - the pension accrual (v4_*_accrual): its contributions, employees' and employers' plus the self-employed at
#     se_oasdi_share (Medicare's Part A: HI, the rest of the self-employed), NIPA 3.6; the benefits it no longer
#     charges (v4_*_cash) follow the line's own cells;
#   - the production grid's change (P and F): nominal GDP, NIPA 1.1.5 line 1.
V4_RECEIPT_CELLS = {
    "federal_income_tax": "T30400-A:3", "state_local_income_tax": "T30400-A:9", "personal_motor_vehicle": "T30400-A:10",
    "personal_property_tax": "T30400-A:11", "other_personal_tax": "T30400-A:12",
    "employee_oasdi": "T30600-A:24", "employee_hi": "T30600-A:25", "self_employment_oasdi_hi": "T30600-A:26",
    "employer_oasdi": "T30600-A:5", "employer_hi": "T30600-A:6", "medicare_supplementary_premiums": "T30600-A:27",
    "other_domestic_social_contributions": "T30600-A:7;T30600-A:12;T30600-A:13;T30600-A:14;T30600-A:15;T30600-A:16;"
                                           "T30600-A:28;T30600-A:29;T30600-A:30;T30600-A:17;T30600-A:31",
    "corporate_capital": "T30100-A:5", "corporate_labor": "T30100-A:5",
    "general_sales_tax": "T30500-A:20", "excise_selective_sales": "T30500-A:4;T30500-A:23", "customs_duties": "T30500-A:15",
    "modeled_owner_property": "T30300-A:9", "remaining_production_property": "T30300-A:9",
    "tenant_occupied_property": "T30300-A:9", "personal_current_transfers": "T30100-A:17",
    # Full-account receipt builder's primary declarations, newly nonzero in v8.
    "government_asset_income": "T30100-A:10", "business_current_transfers": "T30100-A:16"}
# Receipt lines that are a part of their cell rather than all of it: the property-tax lines of S&L property taxes.
V4_CARVED = ("modeled_owner_property", "remaining_production_property", "tenant_occupied_property")
V4_HOUSING = ("T30800-A:13", "T31300-A:4")      # public housing's deficit; federal housing subsidies
V4_ACCRUAL = {"oasdi": {"T30600-A:24": "employee_oasdi", "T30600-A:5": "employer_oasdi"},
              "hi": {"T30600-A:25": "employee_hi", "T30600-A:6": "employer_hi"}}
V4_SELF_EMPLOYED = ("T30600-A:26", "self_employment_oasdi_hi")
V4_GDP = ("T10105-A:1", 29298.013)            # nominal GDP and its 2024 value in the pinned workbook, $bn


def later_cases(case: str) -> list[str]:
    """The cases after September 24 up to and including `case`, in adoption order."""
    names = list(LATER_CASES)
    if case in ("oct14", "oct15", "oct16"):
        # Keep the starting schools-case dependency, but compute no superseded consumer case beside the live one.
        return ["sept26", "sept26_schools", case]
    return names[:names.index(case) + 1] if case in LATER_CASES else []


def case_parts(case: str) -> dict:
    """A case's additions at its band ends (case_components.cjs output), gated to the case's current files."""
    c = LATER_CASES[case]
    data = json.loads((HERE / "derived" / c.parts).read_text())
    stale = [rel for rel, digest in data["inputs"].items()
             if hashlib.sha256((FISCAL / rel).read_bytes()).hexdigest() != digest]
    if data["case"] != case or data["lane"] != c.lane or stale:
        raise ValueError(f"[BLOCKED] {c.parts} does not match {c.lane} ({', '.join(stale) or data['case']}): "
                         "rerun case_components.cjs")
    return data


def case_profiles(case: str) -> dict[str, str]:
    """Concept -> the case's profile: the Sept 24 profiles, or those case_components.cjs recorded."""
    c = LATER_CASES[case]
    return PROFILES if c.parts is None else {name: v["profile"] for name, v in case_parts(case)["concepts"].items()}


def response_anchors(case: str) -> dict[str, float]:
    """2024 conditional net cost to other residents, $bn; the range spans allocation and scaling cases.

    The September 20 bands, then the main case adopted on 2026-09-23 (general government at
    0.59-0.84, justice and uncompensated care keyed by use; main_case_2026_09_23), then that case
    with the data corrections adopted on 2026-09-24 (main_case_2026_09_24, variant "adopted"), then
    each later case up to `case` (LATER_CASES, variant "adopted"): September 26 with finite-removal
    responses and the consumption key, schools at full average cost, then September 27.
    """
    summary = pd.read_csv(FISCAL / "full_account_2026_09_20/derived/service_response_summary.csv").set_index("profile")
    adopted = pd.read_csv(FISCAL / "main_case_2026_09_23/derived/main_case_bands.csv")
    adopted = adopted[adopted.variant == "adopted"].set_index("profile")
    out = {}
    for name, profile in PROFILES.items():
        out[f"{name}_low"] = -float(summary.loc[profile, "max_welfare_bn"])
        out[f"{name}_high"] = -float(summary.loc[profile, "min_welfare_bn"])
    for name, profile in PROFILES.items():
        out[f"{name}_adopted_low"] = float(adopted.loc[profile, "cost_low_bn"])
        out[f"{name}_adopted_high"] = float(adopted.loc[profile, "cost_high_bn"])
    corrected = pd.read_csv(FISCAL / "main_case_2026_09_24/derived/main_case_bands.csv")
    corrected = corrected[corrected.variant == "adopted"].set_index("profile")
    for name, profile in PROFILES.items():
        out[f"{name}_corrected_low"] = float(corrected.loc[profile, "cost_low_bn"])
        out[f"{name}_corrected_high"] = float(corrected.loc[profile, "cost_high_bn"])
    for later in later_cases(case):
        c = LATER_CASES[later]
        bands = pd.read_csv(FISCAL / c.lane / "derived/main_case_bands.csv")
        summary_c = json.loads((FISCAL / c.lane / "derived/summary.json").read_text())
        base = bands[bands.variant == c.base_variant].set_index("profile")
        adopted = bands[bands.variant == "adopted"].set_index("profile")
        profiles = case_profiles(later)
        published = {p: summary_c["main_case"] if name == "net_cost_cbo_informed" else summary_c["other_profiles"][p]["adopted"]
                     for name, p in profiles.items()}
        if later in ('oct15', 'oct16'):
            # v8 leaves legacy other_profiles in its inherited summary. Its live
            # alternative profile is the independently evaluated native bridge,
            # already gated to the adopted profile CSV, never that old field.
            principal = case_parts(later)['concepts']
            version = 'v9' if later == 'oct16' else 'v8'
            published = {p: summary_c[version]['band_bn'] if name == 'net_cost_cbo_informed'
                         else [principal[name]['ends'][end]['cost_bn'] for end in ('low', 'high')]
                         for name, p in profiles.items()}
        for name, profile in profiles.items():
            # Each case starts from the band the previous case's concepts carry.
            if not np.allclose(base.loc[profile, ["cost_low_bn", "cost_high_bn"]].to_numpy(float),
                               [out[f"{name}{c.base_tag}low"], out[f"{name}{c.base_tag}high"]], rtol=0, atol=1e-9):
                raise ValueError(f"[BLOCKED] {c.lane} {profile} does not start from the {c.base_variant} band")
            band = [float(adopted.loc[profile, "cost_low_bn"]), float(adopted.loc[profile, "cost_high_bn"])]
            if later == 'oct16' and profile + '/adopted' in summary_c['v9']['historical_rows']:
                # The case explicitly retains this CSV row as v8 history. The
                # independently evaluated/closed native diagnostic is current.
                band = published[profile]
            if not np.allclose(band, published[profile], rtol=0, atol=1e-4):
                raise ValueError(f"[BLOCKED] {c.lane} {profile} bands differ from its summary.json")
            out[f"{name}{c.tag}low"], out[f"{name}{c.tag}high"] = band
    return out


def workbook(path: Path) -> pd.ExcelFile:
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    if digest != PINNED[path.name]:
        raise ValueError(f"[BLOCKED] {path.name} is not the pinned August 2026 vintage: {digest}")
    return pd.ExcelFile(path)


def series(book: pd.ExcelFile, sheet: str, label: str) -> pd.Series:
    table = parsed_sheet(book, sheet)
    header = table.index[table.iloc[:, 0].astype(str).str.strip().eq("Line")][0]
    match = table[table.iloc[:, 1].astype(str).str.strip().eq(label)]
    if match.empty:
        raise ValueError(f"[BLOCKED] {sheet} has no line labelled {label!r}")
    years = [int(float(v)) for v in table.iloc[header, 3:]]
    values = pd.Series(match.iloc[0, 3:].astype(float).to_numpy(), index=years)
    values.loc[YEARS] = checked_years(values, f"{sheet}:{label}")
    return values


@lru_cache(maxsize=128)
def parsed_sheet(book: pd.ExcelFile, sheet: str) -> pd.DataFrame:
    """Parse each verified workbook sheet once; hundreds of parts reuse these cells."""
    return book.parse(sheet, header=None)


def line(book: pd.ExcelFile, reference: str) -> pd.Series:
    """`T31700-A:5` -> that table line by year, as published (NIPA $ millions)."""
    sheet, number = reference.split(":")
    table = parsed_sheet(book, sheet)
    header = table.index[table.iloc[:, 0].astype(str).str.strip().eq("Line")][0]
    body = table.iloc[header + 1:]
    match = body[pd.to_numeric(body.iloc[:, 0], errors="coerce") == int(number)]
    if len(match) != 1:
        raise ValueError(f"[BLOCKED] {sheet} has no single line {number}")
    years = [int(float(v)) for v in table.iloc[header, 3:]]
    values = pd.Series(pd.to_numeric(match.iloc[0, 3:], errors="coerce").to_numpy(float), index=years)
    values.loc[YEARS] = checked_years(values, reference)
    return values


def capital_paths(real: pd.Series, components: list[dict]) -> dict[str, pd.Series]:
    """Each capital component's charged stock by year, real 2024 dollars, 2024 = 1.

    The stock is the average of the year's two yearends (FA Table 7.1), deflated as every amount here.
    Weights: one per line for single-line components; K-12 takes the school lane's structures key on
    line 62 and its equipment and software key on lines 56 and 73; recreation adds museums and zoos as a
    fixed part of line 62. Gates: the lines reproduce the capital lane's national stocks (1e-6), and the
    enterprise components' stocks add to line 79."""
    fa = workbook(FA_WORKBOOK)
    lines = sorted({n for ns in CAPITAL_LINES.values() for n in ns} | {ENTERPRISE_FA_LINE})
    stock = {n: (s + s.shift(1)) / 2 / 1e3 for n in lines for s in [line(fa, f"FAAt701-A:{n}")]}   # $bn, nominal
    cap = FISCAL / "capital_return_services_2026_09_27/derived"
    national = pd.concat([pd.read_csv(cap / "components.csv"), pd.read_csv(cap / "block_components.csv")]) \
        .set_index("component").national_stock_avg2024_bn
    charged = {c["id"]: c["stock_charged_bn"] for c in json.loads((cap / "engine_components.json").read_text())["components"]}
    school = json.loads((FISCAL / "school_capital_return_2026_09_26/derived/summary.json").read_text())
    key, k12 = school["k12_structures_key"]["central"], school["national_k12_capital_bn"]["central"]
    at = lambda n: stock[n][2024]                                                   # noqa: E731
    weights = {cid: {ns[0]: 1.0} for cid, ns in CAPITAL_LINES.items() if len(ns) == 1}
    weights["k12"] = {62: key, 56: (k12["avg2024"] - k12["structures_avg2024"]) / (at(56) + at(73))}
    weights["k12"][73] = weights["k12"][56]
    weights["rec_sl"] = {64: 1.0, 62: (national["rec_sl"] - at(64)) / at(62)}
    expected = {cid: at(ns[0]) for cid, ns in CAPITAL_LINES.items() if len(ns) == 1}
    expected.update(college=(1 - key) * at(62), k12=k12["avg2024"], rec_sl=national["rec_sl"])
    bad = [cid for cid in CAPITAL_LINES if abs(national[cid] - expected[cid]) > 1e-6]
    if bad or abs(k12["structures_avg2024"] - key * at(62)) > 1e-6 or not 0 < weights["rec_sl"][62] < 1 - key:
        raise ValueError(f"[BLOCKED] FA Table 7.1 lines do not reproduce the capital lane's stocks: {bad}")
    enterprise = [c["id"] for c in components if c["part"] == "enterprise"]
    if abs(sum(charged[cid] for cid in enterprise) - at(ENTERPRISE_FA_LINE)) > 1e-6:
        raise ValueError("[BLOCKED] the enterprise components do not add to FA Table 7.1 line 79")
    paths = {}
    for c in components:
        # October 7: an item's offset component (of_component) takes its component's stock.
        w = {ENTERPRISE_FA_LINE: 1.0} if c["part"] == "enterprise" else weights[c.get("of_component", c["id"])]
        value = sum(wt * stock[n] for n, wt in w.items())
        paths[c["id"]] = checked_years(value, f"capital:{c['id']}") * real / value[2024]
    return paths


def declared_national_anchor(data: dict, side: str, lid: str) -> float:
    """Resolve new typed source rows against the verified archived declarations."""
    anchors = {p["national_bn"] for block in data["concepts"].values()
               for prefix in ("v4", "v5", "v6") for p in block.get(f"{prefix}_parts", {}).values()
               if p["line"] == lid and p["side"] == side and p.get("national_bn") is not None}
    if len(anchors) != 1 or not all(np.isfinite(x) for x in anchors):
        raise ValueError(f"[BLOCKED] {side}/{lid}: absent or ambiguous national source anchor {sorted(anchors)}")
    return anchors.pop()


def sum_paths(paths) -> pd.Series:
    """Ordered sum of aligned paths without constructing a Series per addend."""
    iterator = iter(paths)
    first = next(iterator)
    total = np.zeros(len(first), dtype=float)
    np.add(total, first.to_numpy(), out=total)
    for values in iterator:
        if not values.index.equals(first.index):
            raise ValueError("[BLOCKED] historical path indices differ")
        np.add(total, values.to_numpy(), out=total)
    return pd.Series(total, index=first.index)


def v4_series(data: dict, book: pd.ExcelFile, gdp_book: pd.ExcelFile, real: pd.Series, categories: pd.DataFrame,
              receipt_national: dict[str, float], prefix: str = "v4", people: pd.Series | None = None) -> dict[str, pd.Series]:
    """Each September 29 part's national series, real, 2024 = 1 (V4_RECEIPT_CELLS). Gates: a line's own cells are
    its national total in 2024 (1e-3; a spending line's categories.csv total, a receipt line's total in the case);
    a carved line is a part of its cell; the enterprise surplus's move is NIPA 3.8 line 13; the consolidated operating
    subsidy is a part of federal housing subsidies; the accrual's cells are its receipt lines' national totals; every
    part has a series.

    With prefix "v5" the October 5 lineage's parts (v5_parts) go through the same rules, with two of their own. The
    lineage's enterprise surplus part is the added people's share of the line after public housing's deficit left it,
    so it follows the line's own cells, NIPA 3.1 line 19 less 3.8 line 13 (gate: the line's national total in the case).
    lane_constants (rule per_person), whose parts the back-cast does not see, keeps its 2024 value per person: its series
    is the resident population (people, 2024 = 1), so with the third-plus share path it follows the third-plus count.
    With prefix "v6" the October 7 items' parts (v6_parts) go through the October 5 rules."""
    parts = {k: v for concept in data["concepts"].values() for k, v in concept.get(f"{prefix}_parts", {}).items()}
    cell_cache = {}
    def cells(refs):
        if refs not in cell_cache:
            cell_cache[refs] = sum(line(gdp_book if ref.startswith("T1") else book, ref)
                                   for ref in refs.split(";")) / 1e3
        # Non-EIP adjustments mutate their local series; never mutate the cache.
        return cell_cache[refs].copy()
    out = {}
    for part, p in parts.items():
        lid, want = p["line"], p["national_bn"]
        if p["rule"] == "capital":
            continue  # v8 capital carriers take the exact component stock below.
        if want is None and p["side"] == "receipt" and p["rule"] == "line":
            want = declared_national_anchor(data, p["side"], lid)
        if p['rule'] == 'composite_receipts':
            weights, amounts = p['composite_cells'], p['composite_national_bn']
            if abs(sum(weights.values()) - 1) > 1e-12 or set(weights) != set(amounts):
                raise ValueError(f'[BLOCKED] {part}: invalid composite receipt declaration')
            paths = []
            for ref, weight in weights.items():
                source = checked_years(cells(ref), part + ':' + ref)
                if abs(source[2024] - amounts[ref]) > 1e-3:
                    raise ValueError(f'[BLOCKED] {part}: composite national anchor {ref}')
                paths.append(weight * source * real / source[2024])
            out[part] = sum(paths)
            continue
        if p['rule'] == 'non_eip_credits':
            from p7_backcast import pandemic_amounts
            pins = json.loads((HERE / 'inputs/pins.json').read_text())
            for entry in pins.values():
                if hashlib.sha256((HERE / entry['path']).read_bytes()).hexdigest() != entry['sha256']:
                    raise ValueError('[BLOCKED] non-EIP primary source changed: ' + entry['path'])
            nominal = checked_years(cells(categories.loc[lid, 'source_cells']), part)
            for year, paid in pandemic_amounts().items():
                nominal[year] -= paid
            if not nominal.gt(0).all() or abs(nominal[2024] - want) > 1e-3:
                raise ValueError(f'[BLOCKED] {part}: non-EIP refundable-credit source')
            out[part] = checked_years(nominal, part) * real / nominal[2024]
            continue
        if p["rule"] in ("per_person", "coverage"):
            if people is None or abs(people[2024] - 1) > 1e-12:
                raise ValueError(f"[BLOCKED] {part}: no resident population path (2024 = 1) to hold it per person")
            out[part] = people.reindex(YEARS)
            continue
        if p["rule"] == "production":
            nominal, want = cells(V4_GDP[0]), V4_GDP[1]
        elif p["rule"] == "accrual":
            own = V4_ACCRUAL[p["contributions"]]
            se = data["pension_accrual"]["se_oasdi_share"]
            se = se if p["contributions"] == "oasdi" else 1 - se
            nominal = cells(";".join(own)) + se * cells(V4_SELF_EMPLOYED[0])
            want = sum(receipt_national[x] for x in own.values()) + se * receipt_national[V4_SELF_EMPLOYED[1]]
        elif p["side"] == "spending":
            source = p["parent"] or lid
            nominal = cells(categories.loc[source, "source_cells"])
            want = categories.loc[source, "national_bn"]
        elif lid == "enterprise_surplus" and prefix in ("v5", "v6"):
            nominal = cells(RECEIPT_CELLS[lid]) - cells(V4_HOUSING[0])
            if want is None:
                want = declared_national_anchor(data, p["side"], lid)
        elif lid == "enterprise_surplus":
            nominal = cells(V4_HOUSING[0])
            want = -data["v4_enterprise_surplus_national_move_bn"]
        elif lid == "housing_enterprise_surplus":
            if want is None:
                want = declared_national_anchor(data, p["side"], lid)
            deficit, subsidies = cells(V4_HOUSING[0]), cells(V4_HOUSING[1])
            subsidy = (want - deficit[2024]) / subsidies[2024]
            if not -1 < subsidy < 0:
                raise ValueError(f"[BLOCKED] {lid}: the consolidated subsidy is not a part of housing subsidies ({subsidy})")
            nominal = deficit + subsidy * subsidies
        elif lid == "other_production_taxes":
            # The account's production-tax remainder (receipt builder s(1)-s(20)-s(38)-s(4)-s(23)-s(15)).
            # NIPA 3.5 line 17 is not this total; retain every component and gate the result to the account.
            nominal = cells("T30500-A:1") - cells("T30500-A:20;T30500-A:38;T30500-A:4;T30500-A:23;T30500-A:15")
        elif lid in V4_RECEIPT_CELLS:
            if want is None:
                want = receipt_national[lid]
            nominal = cells(V4_RECEIPT_CELLS[lid])
            if lid in ("corporate_capital", "corporate_labor"):
                # CBO's incidence splits one measured corporate-tax line into two account lines. Each follows
                # the same national series, with its 2024 share fixed; neither equals the whole BEA line alone.
                corporate = sum(receipt_national[x] for x in ("corporate_capital", "corporate_labor"))
                if abs(corporate - nominal[2024]) > 1e-3 or abs(want - receipt_national[lid]) > 1e-9:
                    raise ValueError(f"[BLOCKED] {lid}: corporate incidence parts do not reconstruct their national line")
                want = nominal[2024]
            if lid in V4_CARVED:
                if not 0 < want <= nominal[2024] + 1e-3:
                    raise ValueError(f"[BLOCKED] {lid} {want} is not a part of {V4_RECEIPT_CELLS[lid]} {nominal[2024]}")
                want = nominal[2024]
        else:
            raise ValueError(f"[BLOCKED] {part}: no national series for the {p['side']} line {lid}")
        if want is None or not np.isfinite(want):
            raise ValueError(f"[BLOCKED] {part}: no finite national source anchor for {p['side']}/{lid}")
        if abs(nominal[2024] - want) > 1e-3:
            raise ValueError(f"[BLOCKED] {part}: its cells' 2024 value {nominal[2024]} is not {want}")
        # Source cells are checked before summing; no missing observation becomes a zero.
        out[part] = checked_years(nominal, part) * real / nominal[2024]
    return out


def carried_parts(case: str, book: pd.ExcelFile, real: pd.Series, share: pd.Series,
                  gdp_book: pd.ExcelFile, lineage: dict | None = None) -> dict[str, dict[str, pd.Series]]:
    """Concept name -> {part: $bn by year} for a case carried back by component: each addition at its 2024
    value times its national series (real, 2024 = 1) times the group's population-share path; the capital
    return by part (core, block, enterprise) from its components' stock paths.

    A case with the lineage (October 5; lineage holds the identified third-plus generation's share path `share`, its
    count path `flat` and the resident population `people`, each 2024 = 1) carries the lineage's parts (v5_) and the
    capital return's change (v5_capital_bn, inside the capital parts) on the third-plus share path instead. Its entry's
    lineage_2024 holds each part's lineage value in 2024, which the flat rule keeps per third-plus person.

    A case with items (October 7) carries each item part (v6_) on its path, the group's share path for the union's and
    the third-plus share path for the added people's (v6_parts path), and the items' capital change (v6_capital_bn) the
    same way; lineage_2024 takes the added people's."""
    data = case_parts(case)
    c = LATER_CASES[case]
    categories = pd.read_csv(FISCAL / "full_account_spending_2026_09_20/derived/categories.csv") \
        .drop_duplicates("category").set_index("category")
    model = json.loads((FISCAL / "assumption_explorer_2026_09_21/derived/model.json").read_text())
    receipt_national = {l["id"]: l["national_bn"] for l in model["receipts"]["lines"]}
    index = {}
    for part, (side, lid) in ADDITIONS.items():
        cell = categories.loc[lid, "source_cells"] if side == "spending" else RECEIPT_CELLS[lid]
        want = categories.loc[lid, "national_bn"] if side == "spending" else receipt_national[lid]
        nominal = line(book, cell) / 1e3
        if abs(nominal[2024] - want) > 1e-3:
            raise ValueError(f"[BLOCKED] {cell} 2024 is {nominal[2024]}, the account's {lid} {want}")
        index[part] = nominal.reindex(YEARS) * real / nominal[2024]
    index.update(v4_series(data, book, gdp_book, real, categories, receipt_national))
    if c.lineage:
        if lineage is None:
            raise ValueError(f"[BLOCKED] {case} carries the lineage: it needs the third-plus path ({G3PLUS_PATH.name})")
        index.update(v4_series(data, book, gdp_book, real, categories, receipt_national, "v5", lineage["people"]))
    if c.items:
        index.update(v4_series(data, book, gdp_book, real, categories, receipt_national, "v6", lineage["people"]))
    components = next(iter(data["concepts"].values()))["components"]
    stock = capital_paths(real, components)
    if case in ("oct15", "oct16"):
        for block in data["concepts"].values():
            for part, info in block["v6_parts"].items():
                if info["rule"] == "capital":
                    index[part] = stock[info["component"]]
    out = {}
    for concept, v in data["concepts"].items():
        paths6 = {part: p["path"] for part, p in v.get("v6_parts", {}).items()}
        if c.items and (set(paths6.values()) - {"union", "lineage"} or not paths6):
            raise ValueError(f"[BLOCKED] {concept}: an item part's path is not the union's or the added people's")
        for end, e in v["ends"].items():
            missing = [part for part in e["additions_bn"] if part not in index]
            if missing:
                raise ValueError(f"[BLOCKED] {concept}: no national series for {', '.join(missing)}")
            if c.items and any(part.startswith("v6_") and part not in paths6 for part in e["additions_bn"]):
                raise ValueError(f"[BLOCKED] {concept}: an item part has no path")
            ours = [part for part in e["additions_bn"] if c.lineage and (part.startswith("v5_") or paths6.get(part) == "lineage")]
            g3path = {part for part, p in v.get("v6_parts", {}).items()
                      if p.get("population_path") == "g3plus" and part in e["additions_bn"]}
            parts = {part: e["additions_bn"][part] * index[part] * (lineage["share"] if part in ours or part in g3path else share)
                     for part in e["additions_bn"]}
            own = {part: e["additions_bn"][part] for part in ours}
            lineage_parts = {part: parts[part] for part in ours}
            for group in ("core", "block", "enterprise"):
                parts[f"capital_{group}"] = sum(e["capital_bn"][k["id"]] * stock[k["id"]] for k in components
                                                if k["part"] == group) * share
                ids = [k["id"] for k in components if k["part"] == group]
                if c.lineage:
                    lineage_parts[f"capital_{group}"] = sum(
                        e["v5_capital_bn"][i] * stock[i] for i in ids) * lineage["share"]
                    parts[f"capital_{group}"] = parts[f"capital_{group}"] + lineage_parts[f"capital_{group}"]
                    own[f"capital_{group}"] = sum(e["v5_capital_bn"][i] for i in ids)
                if c.items:
                    k6 = e["v6_capital_bn"]
                    parts[f"capital_{group}"] = parts[f"capital_{group}"] + sum(
                        k6["union"][i] * stock[i] for i in ids) * share + sum(k6["lineage"][i] * stock[i] for i in ids) * lineage["share"]
                    own[f"capital_{group}"] = own[f"capital_{group}"] + sum(k6["lineage"][i] for i in ids)
                    lineage_parts[f"capital_{group}"] += sum(k6["lineage"][i] * stock[i] for i in ids) * lineage["share"]
            out[f"{concept}{c.tag}{end}"] = dict(base=e["base_bn"], parts=parts,
                                                 **({"lineage_2024": own, "lineage_parts": lineage_parts,
                                                     "g3path_2024": {part: e["additions_bn"][part] for part in g3path - set(ours)}} if c.lineage else {}))
    return out


def anchors(allocation: str) -> dict[str, float]:
    """2024 complete-account values, $bn and millions; domestic = target plus other residents."""
    receipts = pd.read_csv(FISCAL / "full_account_receipts_2026_09_20/derived/scenario_totals.csv")
    spending = pd.read_csv(FISCAL / "full_account_spending_2026_09_20/derived/scenario_totals.csv")
    accounts = pd.read_csv(FISCAL / "full_account_2026_09_20/derived/accounts.csv")
    r = receipts[(receipts.scenario_id == "cbo_collective") & (receipts.allocation == allocation)].iloc[0]
    g = spending[(spending.scenario_id == "complete_preferred_F_per_capita")
                 & (spending.allocation == allocation)].iloc[0]
    a = accounts[(accounts.receipt_scenario == "cbo_collective") & (accounts.allocation == allocation)
                 & (accounts.spending_scenario == "complete_preferred_F_per_capita")].iloc[0]
    return dict(receipts=float(r.target_bn), spending=float(g.target_bn),
                domestic_receipts=float(r.target_bn + r.other_bn), domestic_spending=float(g.target_bn + g.other_bn),
                group=float(a.target_population) / 1e6, residents=float(a.resident_population) / 1e6,
                gap=-float(a.normalized_gap_bn))


def check_resource_rate_switch():
    if "BACKCAST_RATE_ANCHOR" in os.environ:
        raise ValueError("[BLOCKED] BACKCAST_RATE_ANCHOR retired: DFII10 is a financing-cost sensitivity, not the live resource rate")


def ordered_programme_total(cells, categories, ids):
    """Sum keyed programme paths in a fixed order across Python hash seeds."""
    return sum(cells.get(categories.loc[lid, "source_cells"]) for lid in sorted(ids))


def apply_corrected_stack(annual, carried, book, real, share, income, case="oct15"):
    """Fixed case resource return, charged base and per-part income rules.

    Financing yields remain in separate sensitivity columns, including their
    explicit 2024 anchor movement. They never alter the live resource account.
    """
    from backcast_categories import Cells
    from pension_transport import income_paths, part_factor, part_group
    from round2_programme import inputs as programme_inputs, branch_paths, new_measured_parts

    check_resource_rate_switch()
    paths, pension_audit = income_paths(annual.relative_per_capita_income)
    pins = json.loads((HERE / "inputs/pins.json").read_text())
    entry = next(p for p in pins.values() if p["path"].endswith("DFII10.csv"))
    raw = HERE / entry["path"]
    if hashlib.sha256(raw.read_bytes()).hexdigest() != entry["sha256"]:
        raise ValueError("[BLOCKED] historical capital rate source changed")
    daily = pd.read_csv(raw)
    daily["year"] = pd.to_datetime(daily.iloc[:, 0]).dt.year
    daily["yield"] = pd.to_numeric(daily.DFII10, errors="coerce")
    obs = daily.groupby("year")["yield"].agg(["mean", "count"]).reindex(YEARS)
    if not obs["count"].between(245, 265).all():
        raise ValueError("[BLOCKED] historical capital rate lacks a full year")
    rates = checked_years(obs["mean"] / 100, "historical_yield").clip(lower=0)
    cells = Cells(book)
    total = series(book, "T30100-A", "Current expenditures").reindex(YEARS) / 1e3
    excluded = sum(cells.get(ref) for ref in ("T31700-A:3", "T30100-A:27", "T30100-A:30"))
    prior_charged = total - excluded
    prior_change = (prior_charged * real / prior_charged[2024] - total * real / total[2024]) * share
    cats = pd.read_csv(FISCAL / "full_account_spending_2026_09_20/derived/categories.csv").drop_duplicates("category").set_index("category")
    data = case_parts(case)
    if case == "oct16":
        annual["capital_resource_rate_real"] = data["resource_rate"]
        pension_audit["resource_rate"] = dict(real=data["resource_rate"],
            rule="fixed Trustees flat equivalent in every year; promises retain Trustees path; imported normal costs held",
            financing="DFII10 real-yield sensitivity separate from resource costs; no nominal financing input here")
        pension_audit["v9_transport"] = data["v9_rule"]
    # These cash benefits do not respond on accrual; the other categories are
    # priced on separate component paths, so never belong to the residual base.
    separate = {"social_security", "medicaid_and_chip_other_medical", "housing_subsidies",
                "economic_affairs_services", "recreation_culture"}
    carried_national = (ordered_programme_total(cells, cats, separate) if case == "oct16" else
                        sum(cells.get(cats.loc[lid, "source_cells"]) for lid in separate))
    cash_hi = cells.get(cats.loc["medicare", "source_cells"]) * data["pension_accrual"]["part_a_share"]
    excluded += carried_national + cash_hi
    charged = total - excluded
    if not charged.gt(0).all() or (charged + excluded - total).abs().max() > 1e-9:
        raise ValueError("[BLOCKED] corrected charged-base national closure")
    change = (charged * real / charged[2024] - total * real / total[2024]) * share
    receipts = json.loads((FISCAL / "main_case_schools_full_2026_09_26/derived/summary.json").read_text())["group_receipts_bn"]["adopted"]["shared"]
    diagnostic, comparison, classification, previous_values = [], [], [], {}
    programme_old, measured_use = programme_inputs()
    branch_audit, added_base_audit, new_use_audit, descendant_audit, charged_reconciliation = [], [], [], [], []
    previous = pd.read_csv(HERE / "derived/oct14/backcast_annual.csv").set_index("year")
    previous_windows = pd.read_csv(HERE / "derived/p7/windows.csv")
    for name, split in carried.items():
        concept = name.removesuffix("_low").removesuffix("_high").removesuffix("_" + case)
        metadata = {k: p for prefix in ("v4", "v5", "v6") for k, p in data["concepts"][concept][prefix + "_parts"].items()}
        linked = {k for k, p in metadata.items() if p["rule"] == "accrual"
                  or p.get('income_linked') is True
                  or (p["side"] == "receipt" and p["line"] in INCOME_RECEIPTS)
                  or (p["side"] == "production" and p["line"] == "induced_receipts_bn")}
        for part, info in metadata.items():
            if info['rule'] == 'accrual':
                kind = info.get('contributions')
                if kind not in ('oasdi', 'hi'):
                    raise ValueError(f'[BLOCKED] {part}: accrual lacks its source-specific income rule')
                rule_name = 'PartA workers/member under65' if kind == 'hi' else 'OASDI all-age workers/member x finite PIA earnings response'
            elif part in linked:
                rule_name = 'unit ACS relative-income elasticity'
            elif info.get('item') == 'retiree_health':
                rule_name = 'zero extra group-income response; national OPEB price swap follows function series and fixed service key'
            else:
                rule_name = 'zero extra group-income response; source national/key/population path retained'
            classification.append(dict(concept=concept, part=part, source_line=info['line'], side=info['side'],
                                       source_rule=info['rule'], contribution=info.get('contributions', ''),
                                       population_proxy=part_group(part, info), income_rule=rule_name))
        capital = {k for k, p in metadata.items() if p["rule"] == "capital"}
        original_ratio = sum_paths(split["by_rule"]["ratio"].values())
        original_parts = {k: v.copy() for k, v in split["by_rule"]["ratio"].items()}
        added_spending = sum(v[2024] for k, v in split.get("lineage_parts", {}).items()
                             if k in metadata and metadata[k]["side"] == "spending")
        # Every added expenditure is already a typed component with its own
        # national programme path. Its gross base is explicit, residual zero.
        added_base_audit.append(dict(concept=name, gross_added_expenditure_2024_bn=added_spending,
                                     separately_carried_added_expenditure_2024_bn=added_spending,
                                     residual_added_expenditure_2024_bn=0.0,
                                     broad_sigma_without_carrier_exclusion_2015_2024_bn=(added_spending * prior_change).loc[2015:2024].sum()))
        for rule, parts in split["by_rule"].items():
            parts = {k: v.copy() for k, v in parts.items()}
            legacy = {k: v.copy() for k, v in parts.items()}
            if rule != "flat":
                parts["base"] += (split["base"] + receipts) * change
                legacy["base"] += (split["base"] + receipts) * prior_change
            unit = {k: v.copy() for k, v in parts.items()}
            median = {k: v.copy() for k, v in parts.items()}
            wage_only = {k: v.copy() for k, v in parts.items()}
            if rule == "income":
                for k in sorted(linked):
                    if k in parts:
                        original = parts[k].copy()
                        unit[k] *= income
                        legacy[k] *= income
                        parts[k] *= part_factor(k, metadata[k], paths)
                        median[k] *= part_factor(k, metadata[k], paths, "median_earnings_proxy")
                        wage_only[k] *= part_factor(k, metadata[k], paths, "wage_only_earnings_per_worker")
                        diagnostic += [dict(concept=name, part=k, year=y, rule=metadata[k]["rule"],
                                            contributions=metadata[k].get("contributions", ""),
                                            before_unit_delta_bn=unit[k][y] - original[y],
                                            after_delta_bn=parts[k][y] - original[y]) for y in YEARS]
            split["by_rule"][rule] = parts
            live = sum_paths(parts.values())
            resource_rate = data["resource_rate"] if case == "oct16" else 0.02
            financing = sum_paths(v * rates / resource_rate if (case == "oct16" or name.endswith("_low")) and
                            (k.startswith("capital_") or k in capital) else v for k, v in parts.items())
            before = sum_paths(v * rates / resource_rate if (case == "oct16" or name.endswith("_low")) and
                          (k.startswith("capital_") or k in capital) else v for k, v in legacy.items())
            scenarios = {"live_fixed_resource_rates": live, "before_unit_income_fixed_rates": sum_paths(unit.values()),
                         "financing_cost_dfii10_floor0_beside": financing,
                         "previous_unit_income_dfii10_stack": before,
                         "median_earnings_proxy_beside": sum_paths(median.values()),
                         "wage_only_worker_split_beside": sum_paths(wage_only.values())}
            annual[f"{name}__{rule}"] = live
            annual[f"{name}__{rule}__financing_dfii10_beside"] = financing
            for scenario, values in scenarios.items():
                if not np.isfinite(values).all():
                    raise ValueError(f"[BLOCKED] nonfinite round2 {scenario}")
                comparison += [dict(concept=name, rule=rule, scenario=scenario, year=y, cost_bn=values[y]) for y in YEARS]
            old_end = "low" if name.endswith("_low") else "high"
            if concept == "net_cost_cbo_informed":
                old = previous_windows[(previous_windows.end == old_end) & (previous_windows.rule == rule)
                                       & (previous_windows.population == "lineage") & (previous_windows.scenario == "stack")]
                if len(old) != 1:
                    raise ValueError("[BLOCKED] prior 74ce1f67 stack row absent or duplicated")
                previous_values[(name, rule)] = float(old.iloc[0]["10y_2015_2024_bn"])
        if concept == "net_cost_cbo_informed":
            end = "low" if name.endswith("_low") else "high"
            branches = branch_paths(programme_old, end, "lineage")
            prog = branches["programme_measured"]
            old_ratio = previous[f"net_cost_cbo_informed_oct14_{end}__ratio"]
            # A declared transport overlay, not an independent oct15 programme
            # estimation: new pieces retain their own national paths; fixed
            # resource rates and charged base remain in the oct15 anchor.
            overlay = prog - old_ratio
            # The archived annual ratio was rounded to four decimals whereas
            # programme lines retain full precision. Remove only this known
            # 2024 precision offset before transporting its displacement.
            precision = -overlay[2024] * annual.group_millions / annual.group_millions[2024]
            if precision.abs().max() > 1e-4:
                raise ValueError("[BLOCKED] programme anchor discrepancy exceeds published rounding")
            overlay += precision
            new_parts, new_audit = new_measured_parts(original_parts, metadata, measured_use, end)
            new_use = sum_paths(new_parts.values()) - sum_paths(original_parts.values())
            new_use_audit += [dict(concept=name, **row) for row in new_audit]
            # Programme replaces the broad charged-base change; adding both is
            # double counting. Known new school/Medicaid parts get measured use.
            vals = original_ratio + overlay + new_use
            annual[f"{name}__programme_beside"] = vals
            comparison += [dict(concept=name, rule="programme", scenario="v7_measured_programme_overlay_beside",
                                year=y, cost_bn=vals[y]) for y in YEARS]
            old = previous_windows[(previous_windows.end == end) & (previous_windows.rule == "programme")
                                   & (previous_windows.population == "lineage") & (previous_windows.scenario == "programme_measured")]
            if len(old) != 1:
                raise ValueError("[BLOCKED] prior programme row absent or duplicated")
            previous_values[(name, "programme")] = float(old.iloc[0]["10y_2015_2024_bn"])
            # Apply the same current per-part income correction to this declared
            # overlay; its source programme displacement itself is held fixed.
            old_lines = programme_old[(programme_old.end == end) & (programme_old.population == "lineage")
                                      & (programme_old.rule == "programme") & (programme_old.variant == "programme_measured")]
            receipt_lines = old_lines[old_lines.part.isin([f"receipts:{lid}" for lid in INCOME_RECEIPTS] + ["production_receipts"])]
            receipt_income = receipt_lines.groupby("year").cost_bn.sum().reindex(YEARS, fill_value=0) * (income - 1)
            vals_income, joint_unit = vals + receipt_income, vals + receipt_income
            for k in sorted(linked):
                info = metadata[k]
                if k not in new_parts:
                    continue
                new_item = info.get("item") in ("foreign_source_tax", "union_completion", "mixed_unit_removal", "coverage") or info.get("item") in data.get("v9_items", []) or info.get("item") == "coverage_repricing"
                if info["rule"] == "accrual" or new_item:
                    vals_income += new_parts[k] * (part_factor(k, info, paths) - 1)
                    joint_unit += new_parts[k] * (income - 1)
            annual[f"{name}__programme_income_beside"] = vals_income
            comparison += [dict(concept=name, rule="programme_income", scenario="v7_measured_programme_overlay_beside",
                                year=y, cost_bn=vals_income[y]) for y in YEARS]
            old = previous_windows[(previous_windows.end == end) & (previous_windows.rule == "programme_income")
                                   & (previous_windows.population == "lineage") & (previous_windows.scenario == "programme_measured")]
            if len(old) != 1:
                raise ValueError("[BLOCKED] prior programme-income row absent or duplicated")
            previous_values[(name, "programme_income")] = float(old.iloc[0]["10y_2015_2024_bn"])
            annual[f"{name}__joint_stack"] = vals_income
            if abs(vals_income[2024] - original_ratio[2024]) > 1e-9:
                raise ValueError(f"[BLOCKED] joint programme anchor {name}")
            old_union = branch_paths(programme_old, end, "union")["programme_measured"]
            gap = prog - old_union
            for k, info in metadata.items():
                if k not in split.get("lineage_parts", {}):
                    continue
                own_path = split["lineage_parts"][k]
                if info.get("item") in ("foreign_source_tax", "union_completion", "mixed_unit_removal", "coverage") or info.get("item") in data.get("v9_items", []) or info.get("item") == "coverage_repricing":
                    gap += new_parts.get(k, own_path)
                if k in linked:
                    gap += own_path * (part_factor(k, info, paths) - 1)
                    if k in new_parts:
                        gap += (new_parts[k] - original_parts[k]) * (part_factor(k, info, paths) - 1)
            descendant_audit += [dict(concept=name, year=y, lineage_minus_union_bn=gap[y],
                                      lower_ratio_20pct_change_bn=-0.2 * gap[y]) for y in YEARS]
            comparison += [dict(concept=name, rule="joint", scenario="live_programme_measured_per_part_income",
                                year=y, cost_bn=vals_income[y]) for y in YEARS]
            comparison += [dict(concept=name, rule="joint", scenario="programme_measured_before_unit_income",
                                year=y, cost_bn=joint_unit[y]) for y in YEARS]
            previous_values[(name, "joint")] = previous_values[(name, "income")]
            pieces = {
                "programme_spending": branches["programme"] - old_ratio,
                "pandemic_measured": branches["programme_pandemic"] - branches["programme"],
                "historical_school_medicaid": branches["programme_measured"] - branches["programme_pandemic"],
                "new_known_use_keys": new_use,
                "per_part_income": vals_income - vals,
                "precision_anchor": precision,
            }
            residual = vals_income - original_ratio - sum(pieces.values())
            if residual.abs().max() > 1e-9:
                raise ValueError("[BLOCKED] programme/charged branch reconciliation")
            charged_delta = annual[f"{name}__ratio"] - original_ratio
            programme_delta = sum(v for k, v in pieces.items() if k != 'per_part_income')
            replaced = vals - annual[f"{name}__ratio"]
            closure = replaced - programme_delta + charged_delta
            if closure.abs().max() > 1e-9:
                raise ValueError('[BLOCKED] charged-to-programme spending reconciliation')
            charged_reconciliation += [dict(concept=name, year=y, original_ratio_bn=original_ratio[y],
                                             charged_ratio_bn=annual[f"{name}__ratio"][y], programme_bn=vals[y],
                                             charged_base_delta_bn=charged_delta[y], programme_delta_bn=programme_delta[y],
                                             programme_minus_charged_bn=replaced[y], residual_bn=closure[y]) for y in YEARS]
            for branch, values in pieces.items():
                branch_audit += [dict(concept=name, branch=branch, year=y, delta_bn=values[y],
                                     charged_ratio_bn=annual[f"{name}__ratio"][y],
                                     programme_joint_bn=vals_income[y],
                                     reconciliation_residual_bn=residual[y]) for y in YEARS]
    table = pd.DataFrame(comparison)
    windows = table[table.year >= 2015].groupby(["concept", "rule", "scenario"]).cost_bn.sum().reset_index()
    windows = windows.rename(columns={"cost_bn": "10y_2015_2024_bn"})
    windows["previous_74ce1f67_bn"] = [previous_values.get((n, r), np.nan)
                                         for n, r in zip(windows.concept, windows.rule)]
    windows["change_from_74ce1f67_bn"] = windows["10y_2015_2024_bn"] - windows.previous_74ce1f67_bn
    provenance = [HERE / 'round2_programme.py', HERE / 'p7_backcast.py', HERE / 'backcast.py',
                  HERE / f'derived/{case}/pandemic_zero_audit.json', HERE / 'derived/p7/audit.json',
                  HERE / 'derived/p7/programme_lines.csv', HERE / 'derived/p7/programme_inputs.json']
    pension_audit['programme_inputs'] = {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in provenance}
    return {"round2_annual.csv": table, "round2_windows.csv": windows,
            "round2_income_parts.csv": pd.DataFrame(diagnostic).sort_values(['concept', 'part', 'year']),
            "round2_income_classification.csv": pd.DataFrame(classification),
            "round2_programme_branches.csv": pd.DataFrame(branch_audit),
            "round2_added_expenditure_base.csv": pd.DataFrame(added_base_audit),
            "round2_new_measured_use.csv": pd.DataFrame(new_use_audit),
            "round2_descendants.csv": pd.DataFrame(descendant_audit),
            "round2_charged_programme_reconciliation.csv": pd.DataFrame(charged_reconciliation),
            "round2_charged_base.csv": pd.DataFrame(dict(year=YEARS, total_bn=total, excluded_bn=excluded, residual_charged_bn=charged)),
            "round2_income_paths.csv": pd.DataFrame(paths).rename_axis("year").reset_index()}, pension_audit


def transported_lineage_count(group, g3, union, added, reporters=0.0, covered_g3=0.0):
    """Counts take the same union/G3 paths as their priced components."""
    union_path, g3_path = group / group[2024], g3 / g3[2024]
    return union * union_path + added * g3_path + (reporters + covered_g3) * (g3_path - union_path)


def per_lineage_member(annual: pd.DataFrame, case: str) -> None:
    """Adds `lineage_millions`, the lineage's count by year, and each case's PER_LINEAGE_MEMBER concept per
    lineage member under the ratio and income rules ($, 2024 dollars). The count is the union on the group's path, put
    on the account's frame (the group's count times the case's union over the group's 2024 count), plus the added
    descendants on the identified third-plus path (2024 = 1), the lineage rule above; both counts are the case lane's.
    The frame is a constant factor, so a change against 2024 is the same on the group's frame. Gates: the union and the
    added descendants make the case's per-member population (1e-9 million), and 2024 per member is the case's
    version's per_member_usd.set at each end ($0.01)."""
    lane = LATER_CASES[case].lane
    version = "v9" if case == "oct16" else "v8" if case == "oct15" else "v7" if case == "oct14" else "v6"
    summary = json.loads((FISCAL / lane / "derived/summary.json").read_text())
    counts, per_member = summary["v5"]["lineage"]["counts"], summary[version]["per_member_usd"]
    union, added, lineage = (counts[k] / 1e6 for k in ("account_union", "added", "lineage_population"))
    if case in ("oct15", "oct16"):
        meta = json.loads((FISCAL / lane / "derived/corrections.json").read_text())["meta"]
        completion = meta["union_completion"]["counts"]
        union += completion["reporters"] / 1e6
        added += completion["nonreporters"] / 1e6
        coverage = dict(meta["coverage"].get("counts_by_generation_folded", meta["coverage"]["counts_by_generation"]))
        if case == "oct16":
            for key in ("native_minor_calibration", "coverage_tenure"):
                for gen, change in meta.get(key, {}).get("coverage_people_change_by_generation", {}).items():
                    coverage[gen] += change
        lineage = summary[version]["population"]["with_coverage"] / 1e6
        per_member = dict(per_member, population=lineage * 1e6)
        union += sum(coverage.values()) / 1e6
        calibrated_g3 = 0.0
        if case == "oct16":
            changes = [meta[k]["observed_people_change_by_generation"] for k in
                       ("native_minor_calibration", "coverage_tenure") if k in meta]
            union += sum(sum(c.values()) for c in changes) / 1e6
            calibrated_g3 = sum(c.get("G3plus", 0.0) for c in changes) / 1e6
            if abs(lineage - meta["population_v9"]["with_coverage"] / 1e6) > 1e-9:
                raise ValueError("[BLOCKED] v9 summary and population_v9 disagree")
    if abs(union + added - lineage) > 1e-9 or abs(per_member["population"] / 1e6 - lineage) > 1e-9:
        raise ValueError(f"[BLOCKED] {lane}: its union and added people are not its per-member population")
    group, g3 = annual["group_millions"], annual["g3plus_millions_cps"]
    count = transported_lineage_count(group, g3, union, added,
                                      completion['reporters'] / 1e6 if case in ('oct15', 'oct16') else 0.0,
                                      coverage['G3plus'] / 1e6 + (calibrated_g3 if case == 'oct16' else 0.0) if case in ('oct15', 'oct16') else 0.0)
    annual["lineage_millions"] = count
    for name, want in zip(PER_LINEAGE_MEMBER[case], per_member["set"]):
        for rule in ("ratio", "income"):
            column = f"{name}__{rule}__per_lineage_member_usd"
            annual[column] = annual[f"{name}__{rule}"] * 1e3 / count
            if abs(annual.loc[2024, column] - want) > 0.01:
                raise ValueError(f"[BLOCKED] {column} is {annual.loc[2024, column]} in 2024, not the case's "
                                 f"{version}.per_member_usd.set {want}")


def main() -> tuple[pd.DataFrame, dict]:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--bea-dir", type=Path,
                        default=ROOT / "sources/immigration-fiscal/data/external/bea_nipa")
    parser.add_argument("--case", choices=(*reversed(list(LATER_CASES)), "sept24"), default=DEFAULT_CASE,
                        help="a case after September 24 (default: oct16, the live personal case; sept27: long-run road and park responses, rental "
                             "assistance, the enterprises and the return on public capital; oct07: main case v6, "
                             "October 5 plus the items; oct05: the main case "
                             "adopted 2026-10-05, v5, with the lineage; sept29: the main case adopted 2026-09-29, "
                             "candidate v4; sept26_schools: schools at full average cost; sept26: CBO's one-year school "
                             "response, 0.63-0.66) or sept24: the files as of 2026-09-24")
    parser.add_argument("--out-dir", type=Path, default=None,
                        help="default: derived/, or the case's own directory under it (sept29: derived/sept29/; oct05: "
                             "derived/oct05/; oct07: derived/oct07/; oct14: derived/oct14/; oct15: derived/oct15/; oct16: derived/oct16/)")
    args = parser.parse_args()
    if args.case in ('oct15', 'oct16'):
        check_resource_rate_switch()
    if args.case == 'oct16':
        os.environ.setdefault('BACKCAST_WORKER_PROFILE_DIR', str(HERE / 'derived/oct16'))
    if args.out_dir is None:
        own = LATER_CASES[args.case].out if args.case in LATER_CASES else None
        args.out_dir = HERE / "derived" / (own or "")
    section3 = workbook(args.bea_dir / "Section3All_xls.xlsx")
    receipts = series(section3, "T30100-A", "Current receipts")
    spending = series(section3, "T30100-A", "Current expenditures")
    section1 = workbook(args.bea_dir / "Section1All_xls.xlsx")
    deflator = series(section1, "T10109-A", "Gross domestic product")
    people = series(workbook(HERE / "_cache/Section7All_xls.xlsx"), "T70100-A", "Population (midperiod, thousands)")
    if abs(receipts[2024] - 8008290) > 0.5 or abs(spending[2024] - 10061458) > 0.5:
        raise ValueError("[BLOCKED] BEA 2024 totals differ from the complete account's")

    acs = pd.read_csv(HERE / "inputs/acs_mexican_origin.csv").set_index("year").reindex(YEARS)
    count = acs.acs_mexican_origin.interpolate()                      # 2020 has no standard release
    relative = (acs.per_capita_income_mexican / acs.per_capita_income_total).interpolate().bfill()
    base = anchors("shared")
    group_receipts, group_2024 = base["receipts"], base["group"]
    group = count * group_2024 / count[2024]                          # millions, account definition
    real = deflator[2024] / deflator.reindex(YEARS)
    # BEA midperiod growth, levelled to the account's 2024 resident denominator (340.111m vs 340.095m)
    residents = people.reindex(YEARS) * 1e3 * (base["residents"] * 1e6 / (people[2024] * 1e3))
    r = receipts.reindex(YEARS) * 1e6 * real / residents
    s = spending.reindex(YEARS) * 1e6 * real / residents
    rho = group_receipts * 1e9 / (group_2024 * 1e6) / r[2024]
    income = relative / relative[2024]

    annual = pd.DataFrame(dict(group_millions=group, relative_per_capita_income=relative,
                               national_receipts_per_capita=r, national_spending_per_capita=s))
    concepts = response_anchors(args.case)
    # The 2026-09-24 corrections lower the group's receipts; their concepts split on the corrected total.
    after = json.loads((FISCAL / "main_case_2026_09_24/derived/summary.json").read_text())["group_receipts_bn"]
    if abs(after["adopted_2026_09_23"]["shared"] - group_receipts) > 1e-6:
        raise ValueError("[BLOCKED] main_case_2026_09_24 receipts do not start from the complete account's")
    receipts_for = {"_corrected_": after["adopted"]["shared"]}
    tags = ["_adopted_", "_corrected_"] + [v.tag for v in LATER_CASES.values()]
    if any(a != b and a in b for a in tags for b in tags):
        raise ValueError("[BLOCKED] one concept tag contains another")
    carried = {}
    share = group / residents / (group[2024] / residents[2024])       # the group's population share, 2024 = 1
    lineage = None
    if any(LATER_CASES[later].lineage for later in later_cases(args.case)):
        # October 5: the identified third-plus generation by year (CPS ASEC, survey year t + 1), the lineage's path.
        g3 = pd.read_csv(G3PLUS_PATH).set_index("year").g3plus_persons.reindex(YEARS) / 1e6
        if g3.isna().any():
            raise ValueError(f"[BLOCKED] {G3PLUS_PATH.name} lacks a year of {YEARS[0]}-{YEARS[-1]}")
        lineage = dict(share=g3 / residents / (g3[2024] / residents[2024]), flat=g3 / g3[2024],
                       people=residents / residents[2024])
        annual["g3plus_millions_cps"] = g3
    for later in later_cases(args.case):
        # The consumption key raises them on September 26; the finite-removal and school responses act
        # on spending only.
        c = LATER_CASES[later]
        summary_c = json.loads((FISCAL / c.lane / "derived/summary.json").read_text())
        after_c = summary_c["group_receipts_bn"]
        if abs(after_c["adopted_2026_09_23"]["shared"] - group_receipts) > 1e-6 or \
                abs(after_c[c.base_receipts]["shared"] - receipts_for[c.base_tag]) > 1e-9:
            raise ValueError(f"[BLOCKED] {c.lane} receipts do not start from the {c.base_variant} case's")
        receipts_for[c.tag] = after_c["adopted"]["shared"]
        if c.parts is not None:
            # The base part splits on the starting case's receipts. The case's receipts differ from them only
            # by the enterprise receipt's re-key, which the enterprise_surplus part carries with its own series.
            # September 29's also differ by its own receipt changes, which its v4 parts carry: its lane records
            # September 27's receipts (rekeyed_receipts), which must differ from the schools case's by the re-key.
            move = summary_c["enterprises"]["receipt_rekey"]["reference_edit_bn"]["shared"]
            if abs(after_c[c.rekeyed_receipts]["shared"] - after_c[c.base_receipts]["shared"] - move) > 1e-9:
                raise ValueError(f"[BLOCKED] {c.lane} receipts move by more than the enterprise re-key")
            receipts_for[c.tag] = receipts_for[c.base_tag]
            carried.update(carried_parts(later, section3, real, share, section1, lineage))
    for name, value in concepts.items():
        # cost = spending charged to the group under this response case, less its receipts
        g_receipts = next((v for tag, v in receipts_for.items() if tag in name), group_receipts)
        rho_c = g_receipts * 1e9 / (group_2024 * 1e6) / r[2024]
        split = carried.get(name)
        base_value = value - sum(p[2024] for p in split["parts"].values()) if split else value
        if split and abs(base_value - split["base"]) > 1e-4:
            raise ValueError(f"[BLOCKED] {name}: the base part {base_value} is not the case's base {split['base']}")
        sigma = (base_value + g_receipts) * 1e9 / (group_2024 * 1e6) / s[2024]
        annual[f"{name}__flat"] = group / group_2024 * value
        annual[f"{name}__ratio"] = group * 1e6 * (sigma * s - rho_c * r) / 1e9
        annual[f"{name}__income"] = group * 1e6 * (sigma * s - rho_c * income * r) / 1e9
        if split:
            # Earlier cases hold carried additions' relative keys. Oct15 applies
            # its separate per-part income corrections after this common stage.
            # The flat rule holds every part per person.
            flat = group / group_2024
            split["by_rule"] = {"flat": dict(base=flat * base_value, **{k: flat * v[2024] for k, v in split["parts"].items()})}
            own = split.get("lineage_2024")
            if own:
                # October 5: the lineage's 2024 values are held per identified third-plus person, the rest per member.
                split["by_rule"]["flat"] = dict(base=flat * base_value, **{
                    k: flat * (v[2024] - own.get(k, 0.0)) + lineage["flat"] * own.get(k, 0.0) for k, v in split["parts"].items()})
                annual[f"{name}__flat"] = sum_paths(split["by_rule"]["flat"].values())
            if args.case in ("oct15", "oct16"):
                for part, value in split.get("g3path_2024", {}).items():
                    split["by_rule"]["flat"][part] = lineage["flat"] * value
                annual[f"{name}__flat"] = sum_paths(split["by_rule"]["flat"].values())
            for rule in ("ratio", "income"):
                split["by_rule"][rule] = dict(base=annual[f"{name}__{rule}"].copy(), **split["parts"])
                annual[f"{name}__{rule}"] += sum_paths(split["parts"].values())
    round2 = None
    if args.case in ("oct15", "oct16"):
        round2, pension_audit = apply_corrected_stack(annual, carried, section3, real, share, income, args.case)
    # Gap against the average resident: a receipts shortfall less a spending shortfall, so a
    # national deficit shared by everyone cancels. Domestic shares of the BEA totals stay at 2024.
    name, value = "gap_vs_average_resident", base["gap"]
    r_dom = r * base["domestic_receipts"] * 1e3 / receipts[2024]
    s_dom = s * base["domestic_spending"] * 1e3 / spending[2024]
    rho_r = group_receipts / group_2024 / (base["domestic_receipts"] / base["residents"])
    rho_s = base["spending"] / group_2024 / (base["domestic_spending"] / base["residents"])
    annual[f"{name}__flat"] = group / group_2024 * value
    annual[f"{name}__ratio"] = group * 1e6 * ((1 - rho_r) * r_dom - (1 - rho_s) * s_dom) / 1e9
    annual[f"{name}__income"] = group * 1e6 * ((1 - rho_r * income) * r_dom - (1 - rho_s) * s_dom) / 1e9
    concepts = dict(concepts, **{name: value})
    for name, value in concepts.items():
        for rule in ("flat", "ratio", "income"):
            if not np.isclose(annual.loc[2024, f"{name}__{rule}"], value, rtol=1e-6):
                raise ValueError(f"[BLOCKED] {name}/{rule} does not reproduce its 2024 anchor: "
                                 f"{annual.loc[2024, f'{name}__{rule}']} vs {value}")
    if args.case in PER_LINEAGE_MEMBER:
        per_lineage_member(annual, args.case)
    if args.case in ('oct15', 'oct16'):
        sys.path.insert(0, str(FISCAL / 'scripts'))
        from memory_budget import require_within_budget
        footprint = require_within_budget('historical backcast round2')
        print(f'physical_footprint_bytes={footprint}')
    args.out_dir.mkdir(parents=True, exist_ok=True)
    if round2 is not None:
        for filename, output in round2.items():
            output.to_csv(args.out_dir / filename, index=False, float_format="%.12g", lineterminator="\n")
        (args.out_dir / "round2_pension_audit.json").write_text(json.dumps(pension_audit, indent=2, allow_nan=False) + "\n")
    annual.round(4).to_csv(args.out_dir / "backcast_annual.csv", index_label="year")

    windows = {"10y_2015_2024": range(2015, 2025), "15y_2010_2024": range(2010, 2025),
               "20y_2005_2024": range(2005, 2025)}
    rows = [dict(concept=name, rule=rule, **{w: annual.loc[list(ys), f"{name}__{rule}"].sum() / 1e3
                                             for w, ys in windows.items()})
            for name in concepts for rule in ("flat", "ratio", "income")]
    table = pd.DataFrame(rows)
    table.round(4).to_csv(args.out_dir / "backcast_windows.csv", index=False)
    if carried:
        # Each carried concept by part: the base (the starting case's cost at the case's end specifications,
        # under the rule) and each addition. The capital return is an imputed resource cost, not a payment.
        # The same parts by year feed debt_legacy.py, which compounds the cash part only.
        records, yearly = [], []
        positions = {w: [YEARS.index(year) for year in ys] for w, ys in windows.items()}
        for name, split in carried.items():
            for rule, parts in split["by_rule"].items():
                if (sum_paths(parts.values()) - annual[f"{name}__{rule}"]).abs().max() > 1e-9:
                    raise ValueError(f"[BLOCKED] {name}/{rule}: the parts do not add to the concept")
                for part, path in parts.items():
                    if list(path.index) != YEARS:
                        raise ValueError(f"[BLOCKED] {part}: export path years differ")
                    values = path.to_numpy()
                    if not np.isfinite(values).all():
                        raise ValueError(f"[BLOCKED] {part}: nonfinite export path")
                    records.append(dict(concept=name, rule=rule, part=part, value_2024_bn=values[-1],
                                        **{w: values[pos].sum() / 1e3 for w, pos in positions.items()}))
                    yearly.extend(dict(concept=name, rule=rule, part=part, year=year, value_bn=value)
                                  for year, value in zip(YEARS, values))
        pd.DataFrame(records).round(4).to_csv(args.out_dir / "case_parts_windows.csv", index=False)
        if args.case == "oct16":
            write_cached_annual(pd.DataFrame(yearly), args.out_dir)
        else:
            pd.DataFrame(yearly).round(6).to_csv(args.out_dir / "case_parts_annual.csv", index=False)
    print(f"receipts ratio {rho:.3f}; relative income {relative[2008]:.3f} (2008) -> {relative[2024]:.3f} (2024)")
    print(table.round(2).to_string(index=False))
    return annual, carried


if __name__ == "__main__":
    main()
    sys.path.insert(0, str(FISCAL / "scripts"))
    from memory_budget import require_within_budget

    print(f"peak physical footprint {require_within_budget('historical backcast') / 1e9:.3f} GB")
