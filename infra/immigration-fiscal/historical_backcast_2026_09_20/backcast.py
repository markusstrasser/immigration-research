#!/usr/bin/env python3
"""Back-cast the 2024 Mexican-origin fiscal concepts to 2005-2024.

Native-First: consumes the complete account's exports, the pinned BEA workbooks
and ACS series; no new microdata estimator. Measured by year: government current
receipts and expenditures (BEA 3.1), the GDP implicit deflator (1.1.9), midperiod
population (7.1), ACS Mexican-origin counts and relative per-capita income.
Assumed: the group's 2024 per-person position relative to the nation. Three rules:

  flat    per-person cost constant in 2024 dollars
  ratio   receipts and charged spending keep their 2024 ratios to national per capita
  income  as ratio, with the receipts ratio scaled by the group's measured
          per-capita income relative to the nation (unit elasticity)

This is not a measured historical account. No year before 2024 has group taxes,
benefits or services observed here.

Cases (--case), one entry each in LATER_CASES. sept27, the default, adds the main case of 2026-09-27
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
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import NamedTuple

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
FISCAL = ROOT / "infra/immigration-fiscal"
PINNED = {"Section1All_xls.xlsx": "238ba851c9a4932d91a0dedb1b3f2e6c6d37574d154a54267da18b9cb0921a19",
          "Section3All_xls.xlsx": "69b5c7aefb38675324887ce31d6feb4fcde7c903ab952db7328da0813096615e",
          "Section7All_xls.xlsx": "ce107c8ce92393613c0abae38156afcfaef8ab571eedf0302dc09ca44738b9ef",
          "fa_Section7All_xls.xlsx": "e67f534560f111575d5314bab8fe4d62dd696c2e49f421eaa2fa73f25dea12ae"}
YEARS = list(range(2005, 2025))
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


# Main cases after September 24, in adoption order. Receipts are matched by tag within concept names, so
# no tag may contain another ("_sept26_" would also match "_sept26_schools_"). The default run is DEFAULT_CASE's.
SEPT29_LANE = "main_case_2026_09_29"
OCT05_LANE = "main_case_2026_10_05"
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
                             "case_components_oct05.json", "adopted_2026_09_27", "oct05", True)}
DEFAULT_CASE = "sept27"
# October 5: the identified third-plus generation by year (CPS ASEC, cps_g3plus_path.py), the lineage's path.
G3PLUS_PATH = HERE / "inputs/cps_g3plus_path.csv"
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
    "tenant_occupied_property": "T30300-A:9", "personal_current_transfers": "T30100-A:17"}
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
        for name, profile in profiles.items():
            # Each case starts from the band the previous case's concepts carry.
            if not np.allclose(base.loc[profile, ["cost_low_bn", "cost_high_bn"]].to_numpy(float),
                               [out[f"{name}{c.base_tag}low"], out[f"{name}{c.base_tag}high"]], rtol=0, atol=1e-9):
                raise ValueError(f"[BLOCKED] {c.lane} {profile} does not start from the {c.base_variant} band")
            band = [float(adopted.loc[profile, "cost_low_bn"]), float(adopted.loc[profile, "cost_high_bn"])]
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
    table = book.parse(sheet, header=None)
    header = table.index[table.iloc[:, 0].astype(str).str.strip().eq("Line")][0]
    match = table[table.iloc[:, 1].astype(str).str.strip().eq(label)]
    if match.empty:
        raise ValueError(f"[BLOCKED] {sheet} has no line labelled {label!r}")
    years = [int(float(v)) for v in table.iloc[header, 3:]]
    return pd.Series(match.iloc[0, 3:].astype(float).to_numpy(), index=years)


def line(book: pd.ExcelFile, reference: str) -> pd.Series:
    """`T31700-A:5` -> that table line by year, as published (NIPA $ millions)."""
    sheet, number = reference.split(":")
    table = book.parse(sheet, header=None)
    header = table.index[table.iloc[:, 0].astype(str).str.strip().eq("Line")][0]
    body = table.iloc[header + 1:]
    match = body[pd.to_numeric(body.iloc[:, 0], errors="coerce") == int(number)]
    if len(match) != 1:
        raise ValueError(f"[BLOCKED] {sheet} has no single line {number}")
    years = [int(float(v)) for v in table.iloc[header, 3:]]
    return pd.Series(pd.to_numeric(match.iloc[0, 3:], errors="coerce").to_numpy(float), index=years)


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
        w = {ENTERPRISE_FA_LINE: 1.0} if c["part"] == "enterprise" else weights[c["id"]]
        value = sum(wt * stock[n] for n, wt in w.items())
        paths[c["id"]] = (value.reindex(YEARS) * real / value[2024])
    return paths


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
    is the resident population (people, 2024 = 1), so with the third-plus share path it follows the third-plus count."""
    parts = {k: v for concept in data["concepts"].values() for k, v in concept.get(f"{prefix}_parts", {}).items()}
    cells = lambda refs: sum(line(gdp_book if ref.startswith("T1") else book, ref) for ref in refs.split(";")) / 1e3  # noqa: E731
    out = {}
    for part, p in parts.items():
        lid, want = p["line"], p["national_bn"]
        if p["rule"] == "per_person":
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
        elif lid == "enterprise_surplus" and prefix == "v5":
            nominal = cells(RECEIPT_CELLS[lid]) - cells(V4_HOUSING[0])
        elif lid == "enterprise_surplus":
            nominal = cells(V4_HOUSING[0])
            want = -data["v4_enterprise_surplus_national_move_bn"]
        elif lid == "housing_enterprise_surplus":
            deficit, subsidies = cells(V4_HOUSING[0]), cells(V4_HOUSING[1])
            subsidy = (want - deficit[2024]) / subsidies[2024]
            if not -1 < subsidy < 0:
                raise ValueError(f"[BLOCKED] {lid}: the consolidated subsidy is not a part of housing subsidies ({subsidy})")
            nominal = deficit + subsidy * subsidies
        elif lid in V4_RECEIPT_CELLS:
            nominal = cells(V4_RECEIPT_CELLS[lid])
            if lid in V4_CARVED:
                if not 0 < want <= nominal[2024] + 1e-3:
                    raise ValueError(f"[BLOCKED] {lid} {want} is not a part of {V4_RECEIPT_CELLS[lid]} {nominal[2024]}")
                want = nominal[2024]
        else:
            raise ValueError(f"[BLOCKED] {part}: no national series for the {p['side']} line {lid}")
        if abs(nominal[2024] - want) > 1e-3:
            raise ValueError(f"[BLOCKED] {part}: its cells' 2024 value {nominal[2024]} is not {want}")
        # A cell BEA leaves blank in a year counts as zero there, as backcast_categories.py and debt_legacy.py count it
        # (October 5's veterans_other, NIPA 3.12 line 20, starts in 2015); no September 29 part has a blank year.
        out[part] = nominal.reindex(YEARS).fillna(0.0) * real / nominal[2024]
    return out


def carried_parts(case: str, book: pd.ExcelFile, real: pd.Series, share: pd.Series,
                  gdp_book: pd.ExcelFile, lineage: dict | None = None) -> dict[str, dict[str, pd.Series]]:
    """Concept name -> {part: $bn by year} for a case carried back by component: each addition at its 2024
    value times its national series (real, 2024 = 1) times the group's population-share path; the capital
    return by part (core, block, enterprise) from its components' stock paths.

    A case with the lineage (October 5; lineage holds the identified third-plus generation's share path `share`, its
    count path `flat` and the resident population `people`, each 2024 = 1) carries the lineage's parts (v5_) and the
    capital return's change (v5_capital_bn, inside the capital parts) on the third-plus share path instead. Its entry's
    lineage_2024 holds each part's lineage value in 2024, which the flat rule keeps per third-plus person."""
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
    components = next(iter(data["concepts"].values()))["components"]
    stock = capital_paths(real, components)
    out = {}
    for concept, v in data["concepts"].items():
        for end, e in v["ends"].items():
            missing = [part for part in e["additions_bn"] if part not in index]
            if missing:
                raise ValueError(f"[BLOCKED] {concept}: no national series for {', '.join(missing)}")
            ours = [part for part in e["additions_bn"] if c.lineage and part.startswith("v5_")]
            parts = {part: e["additions_bn"][part] * index[part] * (lineage["share"] if part in ours else share)
                     for part in e["additions_bn"]}
            own = {part: e["additions_bn"][part] for part in ours}
            for group in ("core", "block", "enterprise"):
                parts[f"capital_{group}"] = sum(e["capital_bn"][k["id"]] * stock[k["id"]] for k in components
                                                if k["part"] == group) * share
                if c.lineage:
                    ids = [k["id"] for k in components if k["part"] == group]
                    parts[f"capital_{group}"] = parts[f"capital_{group}"] + sum(
                        e["v5_capital_bn"][i] * stock[i] for i in ids) * lineage["share"]
                    own[f"capital_{group}"] = sum(e["v5_capital_bn"][i] for i in ids)
            out[f"{concept}{c.tag}{end}"] = dict(base=e["base_bn"], parts=parts,
                                                 **({"lineage_2024": own} if c.lineage else {}))
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


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--bea-dir", type=Path,
                        default=ROOT / "sources/immigration-fiscal/data/external/bea_nipa")
    parser.add_argument("--case", choices=(*reversed(list(LATER_CASES)), "sept24"), default=DEFAULT_CASE,
                        help="a case after September 24 (default: sept27, long-run road and park responses, rental "
                             "assistance, the enterprises and the return on public capital; oct05: the main case "
                             "adopted 2026-10-05, v5, with the lineage; sept29: the main case adopted 2026-09-29, "
                             "candidate v4; sept26_schools: schools at full average cost; sept26: CBO's one-year school "
                             "response, 0.63-0.66) or sept24: the files as of 2026-09-24")
    parser.add_argument("--out-dir", type=Path, default=None,
                        help="default: derived/, or the case's own directory under it (sept29: derived/sept29/; oct05: "
                             "derived/oct05/)")
    args = parser.parse_args()
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
            # The additions follow their own series under both the ratio and income rules: none is keyed by
            # income (the enterprise receipt follows population). The flat rule holds every part per person.
            flat = group / group_2024
            split["by_rule"] = {"flat": dict(base=flat * base_value, **{k: flat * v[2024] for k, v in split["parts"].items()})}
            own = split.get("lineage_2024")
            if own:
                # October 5: the lineage's 2024 values are held per identified third-plus person, the rest per member.
                split["by_rule"]["flat"] = dict(base=flat * base_value, **{
                    k: flat * (v[2024] - own.get(k, 0.0)) + lineage["flat"] * own.get(k, 0.0) for k, v in split["parts"].items()})
                annual[f"{name}__flat"] = sum(split["by_rule"]["flat"].values())
            for rule in ("ratio", "income"):
                split["by_rule"][rule] = dict(base=annual[f"{name}__{rule}"].copy(), **split["parts"])
                annual[f"{name}__{rule}"] += sum(split["parts"].values())
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
    args.out_dir.mkdir(parents=True, exist_ok=True)
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
        for name, split in carried.items():
            for rule, parts in split["by_rule"].items():
                if (sum(parts.values()) - annual[f"{name}__{rule}"]).abs().max() > 1e-9:
                    raise ValueError(f"[BLOCKED] {name}/{rule}: the parts do not add to the concept")
                records += [dict(concept=name, rule=rule, part=part, value_2024_bn=series[2024],
                                 **{w: series.loc[list(ys)].sum() / 1e3 for w, ys in windows.items()})
                            for part, series in parts.items()]
                yearly += [dict(concept=name, rule=rule, part=part, year=year, value_bn=series[year])
                           for part, series in parts.items() for year in YEARS]
        pd.DataFrame(records).round(4).to_csv(args.out_dir / "case_parts_windows.csv", index=False)
        pd.DataFrame(yearly).round(6).to_csv(args.out_dir / "case_parts_annual.csv", index=False)
    print(f"receipts ratio {rho:.3f}; relative income {relative[2008]:.3f} (2008) -> {relative[2024]:.3f} (2024)")
    print(table.round(2).to_string(index=False))


if __name__ == "__main__":
    main()
