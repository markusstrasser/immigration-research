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


# Main cases after September 24, in adoption order. Receipts are matched by tag within concept names, so
# no tag may contain another ("_sept26_" would also match "_sept26_schools_").
LATER_CASES = {"sept26": Case("main_case_2026_09_26", "_sept26_", "adopted_2026_09_24", "_corrected_", "adopted_2026_09_24"),
               "sept26_schools": Case("main_case_schools_full_2026_09_26", "_schools_full_", "adopted_2026_09_26",
                                      "_sept26_", "adopted_2026_09_26"),
               "sept27": Case("main_case_long_run_2026_09_27", "_sept27_", "schools_case", "_schools_full_",
                              "adopted_2026_09_26_schools", "case_components_sept27.json")}
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


def carried_parts(case: str, book: pd.ExcelFile, real: pd.Series, share: pd.Series) -> dict[str, dict[str, pd.Series]]:
    """Concept name -> {part: $bn by year} for a case carried back by component: each addition at its 2024
    value times its national series (real, 2024 = 1) times the group's population-share path; the capital
    return by part (core, block, enterprise) from its components' stock paths."""
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
    components = next(iter(data["concepts"].values()))["components"]
    stock = capital_paths(real, components)
    out = {}
    for concept, v in data["concepts"].items():
        for end, e in v["ends"].items():
            parts = {part: e["additions_bn"][part] * index[part] * share for part in ADDITIONS}
            for group in ("core", "block", "enterprise"):
                parts[f"capital_{group}"] = sum(e["capital_bn"][k["id"]] * stock[k["id"]] for k in components
                                                if k["part"] == group) * share
            out[f"{concept}{c.tag}{end}"] = dict(base=e["base_bn"], parts=parts)
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
    parser.add_argument("--case", choices=(*reversed(list(LATER_CASES)), "sept24"), default=list(LATER_CASES)[-1],
                        help="a case after September 24 (default: the last in LATER_CASES, sept27: long-run road "
                             "and park responses, rental assistance, the enterprises and the return on public "
                             "capital; sept26_schools: schools at full average cost; sept26: CBO's one-year school "
                             "response, 0.63-0.66) or sept24: the files as of 2026-09-24")
    parser.add_argument("--out-dir", type=Path, default=HERE / "derived")
    args = parser.parse_args()
    section3 = workbook(args.bea_dir / "Section3All_xls.xlsx")
    receipts = series(section3, "T30100-A", "Current receipts")
    spending = series(section3, "T30100-A", "Current expenditures")
    deflator = series(workbook(args.bea_dir / "Section1All_xls.xlsx"), "T10109-A", "Gross domestic product")
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
            move = summary_c["enterprises"]["receipt_rekey"]["reference_edit_bn"]["shared"]
            if abs(after_c["adopted"]["shared"] - after_c[c.base_receipts]["shared"] - move) > 1e-9:
                raise ValueError(f"[BLOCKED] {c.lane} receipts move by more than the enterprise re-key")
            receipts_for[c.tag] = receipts_for[c.base_tag]
            carried.update(carried_parts(later, section3, real, share))
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
