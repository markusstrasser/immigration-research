#!/usr/bin/env python3
"""Debt legacy of past federal gaps: interest paid in 2024 on the group-attributable federal debt.

Native-First: consumes the executed complete-account model (assumption_explorer model.json, gated
against main_case_2026_09_23/derived/main_case_bands.csv), the historical back-cast's annual rows
and pinned inputs, the pinned BEA Section 3 workbook, OMB Historical Tables 3.1, 3.2, 7.1 and 12.3
(FY2027 edition), CMS NHEA Table 3 and FRED GS10. No new microdata estimator.

  F_t   federal part of year t's fiscal gap: responsive direct receipts and spending plus the
        induced receipts F of the production model; the private production term P is excluded.
        Nominal dollars of calendar year t.
  D     sum_{t=start}^{2023} F_t * prod_{s=t+1}^{2023} (1 + r_s)   stock entering 2024
  I     r_2024 * D                                                  legacy interest paid in 2024
  D_end D * (1 + r_2024), the brief's formula (stock at the end of 2024, 2024 gap excluded)
  r_s   OMB net interest (Table 3.1) / average debt held by the public (Table 7.1), fiscal year s;
        never the BEA interest line, which includes imputed interest on pension liabilities.

Each account line is split by the government that funds it. Federal benefit programmes are
federal; state-local consumption and benefits are federal in the proportion that federal
grants-in-aid fund them, function by function (BEA Table 3.17). The Medicaid line takes CMS's
federal share of Medicaid spending (NHEA Table 3); OMB Table 12.3 identifies LIHEAP, the
caseload-following income-security grants and the fixed health grants. Three payer conventions:
central (average funding share), low (grants that do not follow caseload count as state-local;
corrections increment state-local), high (all health grants on Medicaid, K-12 at the 12.9% federal
share, general government on the composite's own weights, corrections increment federal).

Sensitivities beside the rules: the 2020-2022 refundable-credit excess attributed per head, the
proposed fiscal benefits of the symmetry lanes carried back by group size, and an audit of the
September 20 grouped-receipt method on the adopted anchor.

Cases (--case). sept24 is the main case adopted 2026-09-24: the explorer model with
main_case_2026_09_24/derived/corrections.json applied, on that case's frame (justice on the use key,
Medicaid on the two uninsured-use keys, general government 0.59/0.84), gated to its bands. Every
correction is split by the government level of the line it edits, component by component, from
sept24_propagation_2026_09_24/derived/package_components.json (gate: the parts add to the whole
account's split). The cases from September 26 on are one entry each in LATER_CASES: the same frame
with the case lane's derived/corrections.json and the responses in its meta.responses, gated to its
bands and to the uncorrected model at those responses. sept26 (CBO's one-year school response,
0.63-0.66, read over the removal: schools 0.6522/0.6813, general government 0.6000/0.8504) adds the
finite-removal responses, audit row 8's change and the consumption key; sept26_schools, the default,
charges schools at full average cost (school response 1) on the same edits. General government's
federal fraction at the low end is composed from the finite-removal responses of its components,
r = [1 - (1 - s)^b] / s (federal tax collection b = 0.789, state-local b = 0.842). The two new
corrections split like the rest: audit row 8's change as row 8 does, the consumption key's edits by
the government level of their lines (see sept26_components). Each run from September 26 on writes one
bridge per step up to its case (<case>_bridge_2024.csv). sept23, sept24, sept26 and sept26_schools
reproduce this lane's outputs of those runs byte for byte.

sept27, the default, is the main case adopted 2026-09-27 (main_case_long_run_2026_09_27): the schools
case plus long-run road and park responses, rental assistance at 1, the return on public capital and
the government enterprises (option D). Its profiles are the case's own (LATER_CASES). The engine port
sets both override kinds the payload's meta.responses carries, lines and `receipt:enterprise_surplus`,
as engine.js does, and adds the return on public capital from meta.capital_return (capital_rows); the
port is gated against the case's per_spec.csv at every specification. Three columns stay apart:
  cash financing     the engine's lines less the capped programs; the only part compounded into debt.
                     The long-run lines split by their subfunctions' levels (responses.json); the
                     enterprise surplus receipt at t32(23)/t31(19), carried by each level's own series;
  resource cost      the return on public capital, an imputed opportunity cost: reported with its
                     federal share by component level, never compounded;
  displaced          rental assistance (federal) and LIHEAP: capped programs whose slots go to eligible
  beneficiaries      households without the group, so no budget response; reported, never compounded.
A pre-existing gap, named and not repaired: the engine compounds current spending, which includes
depreciation, not gross investment and capital transfers (pre_existing_gap in summary.json).

sept29 is the main case adopted 2026-09-29 (main_case_2026_09_29, candidate v4's set; SEPT29 names its lane and
payloads in one place) and writes derived/sept29/. The engine port applies the payload's three new parts as engine.js
does (receipt_lines, national-scale edits, the production grid) and the part_rekeyed capital key; the port is gated
against engine.js through the payload consumer at every specification of both payloads (engine_parity), and against
the adopted lane's per_spec.csv, summary.json and main_case_bands.csv as sept27 is (per_spec_gates, v4_anchors,
case_split). The case has two payloads:
the set, with the pension accrual (social security at the accrual on the group's OASDI receipts), and the cash
set. Only cash is compounded, so the split, the annual flows and the stocks run on the cash set, and a fourth
column sits beside, never compounded:
  pension accrual    the set less the cash set on social security, Medicare and federal income tax (federal);
                     cash + resource cost + displaced + accrual = the adopted (set) net cost + P.
The alternative, the set compounded as if the accrual were borrowed, is the benchmark main_with_accrual.
Public housing's enterprise deficit (receipt line housing_enterprise_surplus, at the rental key) is a capped
program like rental assistance: displaced beneficiaries (the alternative, the line as cash, is the benchmark
main_housing_as_cash). The new lines' federal shares are in v4_shares(); the bridge from September 27 is v4_bridge().
The whole-budget rules are not run for this case (backcast_family), and summary.json says so.

Run from the repository root:
  OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/debt_legacy_2026_09_23/debt_legacy.py
  ... debt_legacy.py --case sept29                          # the main case of 2026-09-29 -> derived/sept29/
  ... debt_legacy.py --case sept26_schools --out-dir <dir>   # the schools case (sept26, sept24, sept23 likewise)
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import importlib.util
import io
import json
import math
import re
import subprocess
from itertools import product
from pathlib import Path
from typing import NamedTuple

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
FISCAL = ROOT / "infra/immigration-fiscal"
BEA = ROOT / "sources/immigration-fiscal/data/external/bea_nipa"
BACKCAST = FISCAL / "historical_backcast_2026_09_20"
NHEA_TABLE3 = ROOT / ("sources/immigration-fiscal/data/external/nhea/nhe_tables/"
                      "Table 03 National Health Expenditures, by Source of Funds.xlsx")
PINNED = {
    BEA / "Section1All_xls.xlsx": "238ba851c9a4932d91a0dedb1b3f2e6c6d37574d154a54267da18b9cb0921a19",
    BEA / "Section3All_xls.xlsx": "69b5c7aefb38675324887ce31d6feb4fcde7c903ab952db7328da0813096615e",
    BACKCAST / "_cache/Section7All_xls.xlsx": "ce107c8ce92393613c0abae38156afcfaef8ab571eedf0302dc09ca44738b9ef",
    ROOT / "sources/immigration-fiscal/data/external/omb_hist_fy2027/hist03z1_fy2027.xlsx":
        "47864b5078698919c3237038ad7296fb7aeb62f6942c3d8acccf98ad0a7122f7",
    HERE / "_cache/hist03z2_fy2027.xlsx": "78100f3efb1a6b08d675b24af173a57359e47dce103a2f1499d905a4bbba06ce",
    HERE / "_cache/hist07z1_fy2027.xlsx": "c3cfce645fe7e4eb9beeb46a970e2b0b30301f02f03f3e5461e9950538641ff9",
    HERE / "_cache/hist12z3_fy2027.xlsx": "43aa30c0d39116909b990a93926540fd173bce4963f26ee3a0d28a6f900d974d",
    HERE / "_cache/fred_GS10.csv": "e22128f6caa50e4e7fed03a1c2d323a517bad452a2c69eab89277450fb59bc5c",
    NHEA_TABLE3: "d379d2746ece097b6f864543d99832882f7dbdc197d1a25473d53d22cdfd58c7",
}
YEARS = list(range(2005, 2025))
FIRST, LAST = 2005, 2024
TARGET_M = 40.896574152351856          # account target population, millions
RESIDENTS_M = 340.110988               # account resident denominator, millions
LADDER137_RATE = 0.03220790586972007   # ladder 137: $879.9bn over the average of $26,330bn and $28,307bn
LADDER137_FLOW = 263.22                # ladder 137's union absolute balance, $bn a year (README table)
LADDER137_TABLE = {10: (3048, 416, 87), 20: (7234, 1969, 218), 30: (12981, 5084, 397)}
K12_FEDERAL_HIGH = 0.1290              # gap_incidence_2026_09_18: OMB subfunction 501 $105.373bn / F-33 $817.03bn
CONVENTIONS = ("central", "low", "high")


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def check_pins() -> dict[str, str]:
    seen = {}
    for path, want in PINNED.items():
        got = sha(path)
        if got != want:
            raise SystemExit(f"[BLOCKED] {path} is not the pinned file: {got}")
        seen[str(path.relative_to(ROOT))] = got
    return seen


# ---------------------------------------------------------------- BEA and OMB readers

class Workbook:
    """BEA NIPA workbook: sheet -> DataFrame indexed by line number, columns years, $bn."""

    def __init__(self, path: Path):
        self.book, self.tables = pd.ExcelFile(path), {}

    def table(self, sheet: str) -> pd.DataFrame:
        if sheet not in self.tables:
            raw = self.book.parse(sheet, header=None)
            header = raw.index[raw.iloc[:, 0].astype(str).str.strip().eq("Line")][0]
            years = [int(float(v)) for v in raw.iloc[header, 3:]]
            body = raw.iloc[header + 1:].copy()
            body.index = pd.to_numeric(body.iloc[:, 0], errors="coerce")
            body = body[body.index.notna()]
            body.index = body.index.astype(int)
            values = body.iloc[:, 3:].apply(pd.to_numeric, errors="coerce") / 1e3
            values.columns = years
            labels = body.iloc[:, 1].astype(str).str.strip()
            if values.index.duplicated().any():
                raise SystemExit(f"[BLOCKED] duplicated line numbers in {sheet}")
            self.tables[sheet] = (values, labels)
        return self.tables[sheet][0]

    def line(self, sheet: str, number: int, label: str | None = None) -> pd.Series:
        values = self.table(sheet)
        if label is not None:
            got = self.tables[sheet][1].loc[number]
            if not got.startswith(label):
                raise SystemExit(f"[BLOCKED] {sheet} line {number} is {got!r}, expected {label!r}")
        return values.loc[number].reindex(YEARS).fillna(0.0)

    def cells(self, reference: str) -> pd.Series:
        """`T31200-A:33;T31200-A:34` -> summed $bn by year (the back-cast's cell syntax)."""
        total = None
        for part in reference.split(";"):
            sheet, number = part.strip().split(":")
            row = self.line(sheet, int(number))
            total = row if total is None else total + row
        return total


def omb_net_interest() -> pd.Series:
    raw = pd.read_excel(ROOT / "sources/immigration-fiscal/data/external/omb_hist_fy2027/hist03z1_fy2027.xlsx",
                        header=None)
    header = raw.index[raw.iloc[:, 0].astype(str).str.strip().eq("Superfunction and Function")][0]
    row = raw.index[raw.iloc[:, 0].astype(str).str.strip().eq("Net interest")][0]
    out = {}
    for j in range(1, raw.shape[1]):
        year = str(raw.iloc[header, j]).strip()
        if year.isdigit():
            out[int(year)] = float(raw.iloc[row, j]) / 1e3
    return pd.Series(out)


def omb_interest_on_public_securities() -> pd.Series:
    """OMB Table 3.2: gross interest on Treasury securities less trust-fund interest (901 + 902 + 903).

    Net interest (the central rate) also nets 908 other interest and 909 investment income, which the
    government receives on its loans and assets; this variant is the interest paid on securities
    held outside the trust funds.
    """
    raw = pd.read_excel(HERE / "_cache/hist03z2_fy2027.xlsx", header=None)
    years = {int(str(v).strip()): j for j, v in enumerate(raw.iloc[2]) if str(v).strip().isdigit()}
    labels = raw.iloc[:, 0].astype(str).str.strip()
    row = lambda prefix: raw.iloc[labels.index[labels.str.startswith(prefix)][0]]
    parts = [row(p) for p in ("901 Interest on Treasury debt securities (gross)",
                              "902 Interest received by on-budget trust funds",
                              "903 Interest received by off-budget trust funds")]
    total = row("Total, Net Interest")
    out = pd.Series({y: sum(float(r.iloc[j]) for r in parts) / 1e3 for y, j in years.items()})
    net = pd.Series({y: float(total.iloc[j]) / 1e3 for y, j in years.items()})
    if abs(net[2024] - 879.879) > 1e-6 or abs(out[2024] - (1133.019 - 116.418 - 67.420)) > 1e-6:
        raise SystemExit("[BLOCKED] OMB Table 3.2 net interest rows differ from the pinned values")
    return out


def omb_debt_held_by_public() -> pd.Series:
    raw = pd.read_excel(HERE / "_cache/hist07z1_fy2027.xlsx", header=None)
    out = {}
    for _, r in raw.iterrows():
        label = str(r.iloc[0]).strip()
        if label.isdigit():
            out[int(label)] = float(r.iloc[3]) / 1e3
    if abs(out[2024] - 28193.866) > 1e-6 or abs(out[2023] - 26235.592) > 1e-6:
        raise SystemExit("[BLOCKED] OMB Table 7.1 debt held by the public differs from the pinned values")
    return pd.Series(out)


class Grants:
    """OMB Table 12.3 outlays for grants by programme, fiscal years, $bn."""

    def __init__(self):
        raw = pd.read_excel(HERE / "_cache/hist12z3_fy2027.xlsx", header=None)
        self.years = {}
        for j in range(raw.shape[1]):
            text = str(raw.iloc[2, j]).strip()
            if text.isdigit():
                self.years[int(text)] = j
        self.raw = raw
        self.labels = raw.iloc[:, 0].astype(str).str.strip().str.lstrip("*").str.strip()

    def section(self, start: str, end: str) -> range:
        a = self.labels.index[self.labels.eq(start)][0]
        b = self.labels.index[self.labels.eq(end)][0]
        return range(a, b + 1)

    def program(self, label: str, rows: range) -> pd.Series:
        hits = [i for i in rows if self.labels.iloc[i] == label]
        if len(hits) != 1:
            raise SystemExit(f"[BLOCKED] OMB 12.3 label {label!r} found {len(hits)} times in its section")
        r = self.raw.iloc[hits[0]]
        return pd.Series({y: pd.to_numeric(r.iloc[j], errors="coerce") for y, j in self.years.items()}
                         ).fillna(0.0) / 1e3

    @staticmethod
    def calendar(fiscal: pd.Series) -> pd.Series:
        """Calendar year t = 3/4 of FY t + 1/4 of FY t+1 (FY t runs October t-1 to September t)."""
        return pd.Series({t: 0.75 * fiscal[t] + 0.25 * fiscal[t + 1] for t in YEARS})


def gs10_fiscal_years() -> pd.Series:
    monthly = pd.read_csv(HERE / "_cache/fred_GS10.csv", parse_dates=["observation_date"])
    monthly["fy"] = monthly.observation_date.dt.year + (monthly.observation_date.dt.month >= 10)
    counts = monthly.groupby("fy").GS10.count()
    means = monthly.groupby("fy").GS10.mean() / 100
    return means[counts == 12]


def nhea_medicaid_federal_share() -> pd.Series:
    """CMS National Health Expenditure Accounts (2024 release) Table 3: Medicaid federal / total, calendar years."""
    raw = pd.read_excel(NHEA_TABLE3, header=None)
    years = {int(float(v)): j for j, v in enumerate(raw.iloc[1]) if str(v).replace(".0", "").strip().isdigit()}
    labels = raw.iloc[:, 0].astype(str).str.strip()
    row = labels.index[labels.eq("Medicaid")][0]
    if labels[row + 1] != "Federal" or labels[row + 2] != "State and Local":
        raise SystemExit("[BLOCKED] NHEA Table 3 Medicaid rows are not Medicaid / Federal / State and Local")
    total = pd.Series({y: float(raw.iloc[row, j]) for y, j in years.items()})
    federal = pd.Series({y: float(raw.iloc[row + 1, j]) for y, j in years.items()})
    if abs(federal[2024] - 596.7) > 0.05 or abs(total[2024] - 931.7) > 0.05:
        raise SystemExit("[BLOCKED] NHEA 2024 Medicaid values differ from the pinned release")
    return (federal / total).reindex(YEARS)


# ---------------------------------------------------------------- the executed model

MODEL = json.loads((FISCAL / "assumption_explorer_2026_09_21/derived/model.json").read_text())
INPUTS = json.loads((FISCAL / "main_case_2026_09_23/derived/inputs.json").read_text())
BANDS = pd.read_csv(FISCAL / "main_case_2026_09_23/derived/main_case_bands.csv")
# The September 24 case: the engine's corrections payload, the adopted bands, and the package's
# corrections by component (exported by sept24_propagation_2026_09_24/export_package.cjs).
CORRECTIONS_FILE = FISCAL / "main_case_2026_09_24/derived/corrections.json"
MAIN24_SUMMARY = FISCAL / "main_case_2026_09_24/derived/summary.json"
COMPONENTS_FILE = FISCAL / "sept24_propagation_2026_09_24/derived/package_components.json"


class Case(NamedTuple):
    lane: str                            # main-case lane
    name: str                            # name in summary.json
    profiles: dict | None = None         # case profile -> (this lane's PROFILES entry, long-run lines respond)
    payloads: dict | None = None         # {"set": path, "cash": path} under infra/immigration-fiscal/ (None: the
                                         # lane's derived/corrections.json)


# Main cases from September 26 on, in adoption order. Each lane's payload carries the September 26 edits
# (case_payload gates it; September 27 adds the enterprise receipt's re-key) and the case's responses in
# meta.responses. Adding a case is one entry here. The finite-removal lane's per-component elasticities
# and the consumption-key lane's edits split the payload's corrections. A case with profiles of its own
# names them: each takes one of this lane's PROFILES for everything but the long-run lines, which take
# the specification's long-run responses where the flag is set (the proportional reference holds them at
# 1, as its base does).
LATER_CASES = {"sept26": Case("main_case_2026_09_26", "main case adopted 2026-09-26"),
               "sept26_schools": Case("main_case_schools_full_2026_09_26",
                                      "main case adopted 2026-09-26, schools at full average cost"),
               "sept27": Case("main_case_long_run_2026_09_27",
                              "main case adopted 2026-09-27: long-run road and park responses, rental assistance, "
                              "the return on public capital, government enterprises (option D)",
                              {"long_run_non_school_full": ("cbo_category_lag_non_school_full", True),
                               "long_run_non_school_fixed": ("cbo_category_lag_non_school_fixed", True),
                               "proportional_reference": ("proportional_reference", False)})}
DEFAULT_CASE = "sept27"
# The main case adopted on 2026-09-29 (candidate v4), in one place: its lane; its two payloads, paths under
# infra/immigration-fiscal/ (the set, with the pension accrual, is the adopted lane's corrections.json, which is the
# candidate's corrections_v4.json plus five meta stamps, gated in case_payload; the adopted lane writes no cash
# payload: its main_case.cjs:78 reads the candidate's corrections_v4_cash.json and gates it against its package's
# pension4 "cash" option, and so does this lane); whether the lane writes the September 27 output contract
# (summary.json, per_spec.csv and main_case_bands.csv, which the lane gates are read against); the payload consumer
# that checks the port against engine.js; the account's priced count (audit row 4); and the adopted bands as the
# decision printed them ($bn to 4 decimals, the mean of the two fill-in methods, at the end specifications).
SEPT29 = dict(lane="main_case_2026_09_29",
              payloads={"set": "main_case_2026_09_29/derived/corrections.json",
                        "cash": "main_case_candidate_v4_2026_09_29/derived/corrections_v4_cash.json"},
              candidate_set="main_case_candidate_v4_2026_09_29/derived/corrections_v4.json",
              stamps=("source", "adopted", "decision", "case", "status"),
              contract=True,
              consumer=FISCAL / "main_case_candidate_v4_2026_09_29/consumer.cjs",
              count=FISCAL / "main_case_candidate_2026_09_28/derived/production_row4.json",
              oracle=dict(set=(371.4146, 434.8410), cash=(294.7011, 361.8175), ends=(48, 11)))
LATER_CASES["sept29"] = Case(SEPT29["lane"],
                             "main case adopted 2026-09-29 (candidate v4): the September 27 case with public housing "
                             "at the tenant key, production on the account's weights, the IRS-matched income-tax key, "
                             "long-run property taxes, payroll compliance, workers' compensation pooled, the pension "
                             "accrual at payable benefits, state pricing and roads keyed by miles",
                             dict(LATER_CASES["sept27"].profiles), SEPT29["payloads"])
LONG_RUN_LINES = ("economic_affairs_services", "recreation_culture")
LONG_RUN_FUNCTIONS = {"economic_affairs_services": "econ", "recreation_culture": "recreation"}
# Capped and rationed programs: without the group their slots go to eligible households who now go
# without, so the cost falls on them, not on a budget. Nothing from them accumulates into debt.
CAPPED = {"housing_subsidies": "rental assistance", "energy_assistance": "LIHEAP"}
ENTERPRISE_RECEIPT = "enterprise_surplus"
# September 29: public housing's enterprise deficit, split out of the enterprise surplus at the rental line's key
# (a receipt line of the payload). Public housing is rationed like rental assistance, so it is capped (later_fields).
HOUSING_ENTERPRISE = "housing_enterprise_surplus"
BACKCAST_PARTS = BACKCAST / "derived/case_parts_annual.csv"
CAPITAL_PARTS = ("capital_core", "capital_block", "capital_enterprise")
R_VALUES = FISCAL / "finite_response_2026_09_26/derived/r_values.json"
CK_PAYLOADS = FISCAL / "consumption_key_2026_09_24/derived/payloads.json"
COMPONENTS: dict = {}                     # the running case's payload by component (set in main())
SHELTER_PARTS = FISCAL / "migrant_shelter_costs_2026_09_23/derived/account_keying_parts.csv"
SHELTER_KEYING = FISCAL / "migrant_shelter_costs_2026_09_23/derived/account_keying.csv"
CARE_SUMMARY = FISCAL / "care_household_services_2026_09_23/derived/summary.csv"
UC_KEYS = {"uninsured_use_low": "equal_low", "uninsured_use_high": "equal_high"}
SYNTHETIC_CARRY = {"school_reprice": "education_services", "college_rekey": "education_services",
                   # September 29: the road re-key's highway parts and the state-price gaps carry with their parents
                   "roads_vmt_sl": "economic_affairs_services", "roads_vmt_fed": "economic_affairs_services",
                   "state_price_public_order_safety": "public_order_safety",
                   "state_price_health_services": "health_services",
                   "state_price_recreation_culture": "recreation_culture"}


def apply_corrections(model: dict, payload: dict) -> dict:
    """engine.js applyCorrections(): add the receipt lines and the synthetic lines, then move each edit's
    dollars into the group's target (other residents' share moves the other way, so national totals hold).

    The three optional parts (September 29 on), as engine.js applies them: receipt_lines adds receipt lines,
    each with a national total and a cell for every executed incidence rule and allocation; an edit
    {side, line, national_bn} scales the line's national total and every cell's target and other amounts to that
    total (shares hold), in order with the other edits (scale_line); production replaces the grid's
    private_wtp_bn, induced_receipts_bn and sampling_se_bn when the dimensions match. A payload without them is
    applied as before."""
    m = copy.deepcopy(model)
    zero = lambda: dict(target_bn=0.0, other_bn=0.0, share=0.0)
    for line in payload.get("receipt_lines") or []:
        if any(x["id"] == line["id"] for x in m["receipts"]["lines"]):
            raise SystemExit(f"[BLOCKED] correction receipt line exists already: {line['id']}")
        national = line.get("national_bn")
        if not isinstance(national, (int, float)) or isinstance(national, bool) or not math.isfinite(national):
            raise SystemExit(f"[BLOCKED] correction receipt line lacks a national total: {line['id']}")
        for sc in m["receipts"]["scenarios"]:
            for a in ("personal", "shared"):
                if not (line.get("cells") or {}).get(sc, {}).get(a):
                    raise SystemExit(f"[BLOCKED] correction receipt line lacks an executed cell: {line['id']}/{sc}/{a}")
        m["receipts"]["lines"].append(copy.deepcopy(line))
    for line in payload["lines"]:
        if any(x["id"] == line["id"] for x in m["spending"]["lines"]):
            raise SystemExit(f"[BLOCKED] correction line exists already: {line['id']}")
        m["spending"]["lines"].append(dict(id=line["id"], family=line["family"], national_bn=0.0,
                                           response_class=line["response_class"], label=line["label"],
                                           preferred_key="k", alternative_key="k",
                                           keys={"k": {"personal": zero(), "shared": zero()}}))
    for e in payload["edits"]:
        if "national_bn" in e:
            scale_line(m, e)
            continue
        if e["side"] == "receipt":
            line = next((x for x in m["receipts"]["lines"] if x["id"] == e["line"]), None)
            if line is None or e["scenario"] not in line["cells"]:
                raise SystemExit(f"[BLOCKED] not an executed receipt cell: {e['line']}/{e['scenario']}")
            cell = line["cells"][e["scenario"]]
        else:
            line = next((x for x in m["spending"]["lines"] if x["id"] == e["line"]), None)
            if line is None or e["key"] not in line["keys"]:
                raise SystemExit(f"[BLOCKED] not an executed allocation rule: {e['line']}/{e['key']}")
            cell = line["keys"][e["key"]]
        for a in ("personal", "shared"):
            t, nxt = cell[a]["target_bn"], cell[a]["target_bn"] + e["by"][a]
            if t != 0:
                cell[a]["share"] *= nxt / t
            cell[a]["target_bn"] = nxt
            cell[a]["other_bn"] -= e["by"][a]
    if payload.get("production") is not None:
        grid = payload["production"]
        for d in PROD_DIMS:
            if not grid.get("dims") or not same_json(grid["dims"].get(d), m["production"]["dims"][d]):
                raise SystemExit(f"[BLOCKED] not this model's production grid: dimension {d}")
        for k in ("private_wtp_bn", "induced_receipts_bn", "sampling_se_bn"):
            xs = grid.get(k)
            if not isinstance(xs, list) or len(xs) != len(m["production"][k]):
                raise SystemExit(f"[BLOCKED] not this model's production grid: {k}")
            m["production"][k] = list(xs)
    return m


def same_json(a, b) -> bool:
    """JSON.stringify(a) === JSON.stringify(b) for parsed JSON values, as engine.js compares the production grid's
    dimensions: numbers by value (JavaScript writes 1.0 as 1, so a Python int and float can be the same text),
    booleans only with booleans, arrays element by element, objects key by key in order."""
    if isinstance(a, bool) or isinstance(b, bool):
        return isinstance(a, bool) and isinstance(b, bool) and a == b
    if isinstance(a, (int, float)) and isinstance(b, (int, float)):
        return a == b
    if isinstance(a, list) and isinstance(b, list):
        return len(a) == len(b) and all(same_json(x, y) for x, y in zip(a, b))
    if isinstance(a, dict) and isinstance(b, dict):
        return list(a) == list(b) and all(same_json(a[k], b[k]) for k in a)
    return type(a) is type(b) and a == b


def scale_line(m: dict, e: dict) -> None:
    """engine.js scaleLine(): a national-scale edit. The line's national total becomes e["national_bn"], and every
    cell's target and other amounts scale by the same factor (shares hold)."""
    lines = m["receipts"]["lines"] if e["side"] == "receipt" else m["spending"]["lines"] if e["side"] == "spending" else None
    line = next((x for x in lines if x["id"] == e["line"]), None) if lines is not None else None
    if line is None:
        raise SystemExit(f"[BLOCKED] not an executed line to scale: {e['side']}/{e['line']}")
    national = e["national_bn"]
    if not isinstance(national, (int, float)) or isinstance(national, bool) or not math.isfinite(national) \
            or not line["national_bn"]:
        raise SystemExit(f"[BLOCKED] not a national total to scale to: {e['line']} {national}")
    f = national / line["national_bn"]
    cells = line["cells"] if e["side"] == "receipt" else line["keys"]
    for k in cells:
        for a in ("personal", "shared"):
            cells[k][a]["target_bn"] *= f
            cells[k][a]["other_bn"] *= f
    line["national_bn"] = national


PROD_DIMS = ["proxy", "split", "normalization", "labor_share", "sigma", "capital_adjustment",
             "labor_supply_elasticity", "capital_tax_retention", "excluded_capital_owner_share"]
# As engine.js PROFILES: school None takes the case's school responses (school_responses); the
# proportional reference charges schools in full.
PROFILES = {"cbo_category_lag_non_school_full": dict(other_edu=1.0, delayed=0.0, school=None),
            "cbo_category_lag_non_school_fixed": dict(other_edu=0.0, delayed=0.0, school=None),
            "proportional_reference": dict(other_edu=1.0, delayed=1.0, school=1.0)}
MAIN = "cbo_category_lag_non_school_full"
# CBO's year-to-year school coefficients (growth, decline), the school responses through September 24,
# as the executed model's service profiles carry them (gated in school_responses).
CBO_SCHOOL = tuple(sorted({p["school_response"] for p in MODEL["service"]["profiles"] if p["profile"] == MAIN}))
BENCHMARKS = {"main": (MAIN, "net_cost_cbo_informed_adopted"),          # profile, back-cast column prefix
              "proportional": ("proportional_reference", "net_cost_full_proportional_adopted")}
WINDOW_STARTS = (2005, 2010, 2015)


def production(normalization: str, model: dict | None = None) -> tuple[float, float]:
    """(P, F) at the account's reference production dims, the one the main case uses, on the model's grid (a
    payload may replace model.json's: the September 29 case's is on the account's row-4 weights)."""
    grid = (model or MODEL)["production"]
    ref = dict(grid["reference"], normalization=normalization)
    index = 0
    for d in PROD_DIMS:
        levels = grid["dims"][d]
        hits = [i for i, v in enumerate(levels)
                if v == ref[d] or (not isinstance(v, str) and not isinstance(ref[d], str) and abs(v - ref[d]) < 1e-9)]
        index = index * len(levels) + hits[0]
    return grid["private_wtp_bn"][index], grid["induced_receipts_bn"][index]


SCHOOL_SHARES = sorted({p["school_share"] for p in MODEL["service"]["profiles"] if p["school_share"] > 0})
SCHOOL_SHARES = [SCHOOL_SHARES[0], SCHOOL_SHARES[-1]]


def school_responses(profile: str, responses: dict | None = None) -> tuple[float, ...]:
    """A profile's school responses: its own, or the case's (growth, decline), CBO's coefficients through
    September 24 and a payload's meta.responses since. Gate: the model carries two CBO coefficients, the
    ones the first later case (September 26) records in meta.responses as the elasticities its growth and
    decline responses replace."""
    own = PROFILES[profile]["school"]
    if own is not None:
        return (own,)
    if responses is not None:
        return (responses["school"]["growth"], responses["school"]["decline"])
    first = json.loads(case_file(next(iter(LATER_CASES)), "corrections.json").read_text())
    replaced = first["meta"]["responses"]["school"]
    if len(CBO_SCHOOL) != 2 or list(CBO_SCHOOL) != replaced["elasticity"]:
        raise SystemExit(f"[BLOCKED] the model's school coefficients {CBO_SCHOOL} are not CBO's growth and decline")
    return CBO_SCHOOL


def lines_at(corner: dict) -> pd.DataFrame:
    """Every account line at one corner: target amount, response, responsive amount ($bn, 2024).

    A corner may carry its own model (the corrected one) and key overrides (the September 24 frame);
    without them it is the September 23 corner: preferred keys plus explicit shifts. From September 27
    a corner may carry line_responses, engine.js's response_override: a spending line's id, or
    "receipt:<id>" for a receipt, replaces the response its class would give."""
    model, keys = corner.get("model", MODEL), corner.get("keys", {})
    override = corner.get("line_responses", {})
    alloc, rows = corner["allocation"], []
    for line in model["receipts"]["lines"]:
        cell = line["cells"][model["receipts"]["reference"]][alloc]
        response = override.get("receipt:" + line["id"], 1.0 if cell["direct"] else 0.0)
        rows.append(dict(side="receipt", id=line["id"], national_bn=line["national_bn"],
                         amount_bn=cell["target_bn"], response=response))
    for line in model["spending"]["lines"]:
        cell = line["keys"][keys.get(line["id"], line["preferred_key"])][alloc]
        amount = cell["target_bn"] + corner["shift"].get(line["id"], 0.0)
        c = line["response_class"]
        s = corner["school_share"]
        if line["id"] in override:
            response = override[line["id"]]
        elif c == "household_transfer":
            response = 1.0
        elif c == "public_goods":
            response = corner["gg"] if line["id"] == "general_public_services" else 0.0
        elif c == "service":
            if line["id"] == "education_services":
                response = s * corner["school_response"] + (1 - s) * corner["other_edu"]
            elif line["id"] in model["service"]["delayed"]:
                response = corner["delayed"]
            else:
                response = 1.0
        elif c == "education_school_part":      # correction lines (engine.js spendingResponse)
            response = s * corner["school_response"]
        elif c == "education_other_part":
            response = (1 - s) * corner["other_edu"]
        elif c == "correction_constant":
            response = 1.0
        else:
            response = 0.0                       # defense, interest, subsidies, foreign, rounding
        rows.append(dict(side="spending", id=line["id"], national_bn=line["national_bn"],
                         amount_bn=amount, response=response))
    out = pd.DataFrame(rows)
    out["responsive_bn"] = out.amount_bn * out.response
    return out


def welfare(corner: dict) -> float:
    t = lines_at(corner)
    direct = t[t.side == "receipt"].responsive_bn.sum() - t[t.side == "spending"].responsive_bn.sum()
    p, f = production(corner["normalization"], corner.get("model"))
    return p + direct + f


SYNTHETIC_RESPONSE = {"school_reprice": lambda c: c["school_share"] * c["school_response"],
                      "college_rekey": lambda c: (1 - c["school_share"]) * c["other_edu"]}
# The September 29 payload's synthetic spending lines. A model without them (the uncorrected one) is evaluated
# as package.cjs adds them, at zero amounts: they add nothing to a capital key.
V4_SYNTHETIC = ("roads_vmt_sl", "roads_vmt_fed", "state_price_public_order_safety", "state_price_health_services",
                "state_price_recreation_culture")


def capital_rows(corner: dict, t: pd.DataFrame | None = None) -> pd.DataFrame:
    """The return on public capital at one corner, component by component (main_case.cjs independentCosts):
    stock_charged_bn x rate x key x response, key and response read on this corner's evaluation.

    A corner without capital_meta or rate has none. The uncorrected model lacks the school and college
    correction lines; as package.cjs adds them at zero amounts, they add nothing to a key and respond as
    engine.js would. A long-run subfunction responds at its reading's value when its line takes the
    specification's long-run response, else at the line's response when that is 0 or 1 (package.cjs
    responseOfRule). From September 29 a key may be part_rekeyed (the payload's rule_kinds): the parent line's
    amount over its national total plus the correction line's amount over the part's national total, the key
    of a part of the parent line that the correction line re-keys (consumer.cjs capitalOf); a model without the
    correction line (the uncorrected one) gives the parent's key."""
    meta = corner.get("capital_meta")
    cols = ["id", "part", "level", "key", "response", "return_bn"]
    if not meta or not corner.get("rate"):
        return pd.DataFrame(columns=cols)
    t = lines_at(corner) if t is None else t
    spend, rec = t[t.side == "spending"].set_index("id"), t[t.side == "receipt"].set_index("id")

    def amount(i):
        if i in spend.index:
            return spend.amount_bn[i]
        if i not in SYNTHETIC_RESPONSE and i not in V4_SYNTHETIC:
            raise SystemExit(f"[BLOCKED] capital key line {i} is not in the evaluation")
        return 0.0

    def response(i):
        return spend.response[i] if i in spend.index else SYNTHETIC_RESPONSE[i](corner)

    rows = []
    for c in meta["components"]:
        k, r = c["key"], c["response"]
        if k["kind"] == "constant":
            key = k["value"]
        elif k["kind"] == "receipt_amount_over_national":
            key = rec.amount_bn[k["line"]] / rec.national_bn[k["line"]]
        elif k["kind"] == "lines_amount_over_national":
            key = sum(amount(i) for i in k["numerator_lines"]) / spend.national_bn[k["denominator_line"]]
        elif k["kind"] == "part_rekeyed":
            key = amount(k["parent_line"]) / spend.national_bn[k["parent_line"]] + amount(k["correction_line"]) / \
                k["part_national_bn"]
        else:
            raise SystemExit(f"[BLOCKED] unknown capital key kind {k['kind']}")
        if r["kind"] == "fixed":
            resp = r["value"]
        elif r["kind"] == "enterprises_switch":
            resp = r["values"][meta["enterprises"]]
        elif r["kind"] == "line_response":
            resp = response(r["line"])
        elif r["kind"] == "line_response_over_share":
            resp = response(r["line"]) / (corner["school_share"] if r["share"] == "school" else 1 - corner["school_share"])
        elif r["kind"] == "long_run_subfunction":
            line_r = response(r["line"])
            if line_r == corner["long_run"][r["line"]]:
                resp = corner["subfunctions"][r["subfunction"]]
            elif line_r in (0, 1):
                resp = line_r
            else:
                raise SystemExit(f"[BLOCKED] {r['line']} responds at {line_r}, neither its long-run response, 0 nor 1")
        else:
            raise SystemExit(f"[BLOCKED] unknown capital response kind {r['kind']}")
        rows.append(dict(id=c["id"], part=c["part"], level=c["level"], key=key, response=resp,
                         return_bn=c["stock_charged_bn"] * corner["rate"] * key * resp))
    return pd.DataFrame(rows, columns=cols)


def cost(corner: dict) -> float:
    """Net cost to other residents: the engine's cost plus the return on public capital (package.cjs cost())."""
    return -welfare(corner) + float(capital_rows(corner).return_bn.sum())


def corners(profile: str, gg: float, justice: float, uc: float) -> list[dict]:
    spec = PROFILES[profile]
    out = []
    for alloc, norm, share, school in product(("personal", "shared"), ("cash", "gdp"), SCHOOL_SHARES,
                                              school_responses(profile)):
        out.append(dict(profile=profile, allocation=alloc, normalization=norm, school_share=share,
                        school_response=school, other_edu=spec["other_edu"], delayed=spec["delayed"], gg=gg,
                        justice=justice, uc=uc,
                        shift={"public_order_safety": justice, "medicaid_and_chip_other_medical": uc}))
    return out


def adopted_anchors(profile: str) -> dict[str, dict]:
    """Corners that set the adopted band: least cost (GG low, UC low) and most cost (GG high, UC high)."""
    gg, uc = INPUTS["general_government_response"], INPUTS["uncompensated_inside_bn"]
    j = INPUTS["justice_change_bn"]["central"]
    least = corners(profile, gg["low"], j, uc["equal_low"])
    most = corners(profile, gg["high"], j, uc["equal_high"])
    lo = max(least, key=welfare)
    hi = min(most, key=welfare)
    band = BANDS[(BANDS.profile == profile) & (BANDS.variant == "adopted")].iloc[0]
    for name, corner, want in (("low", lo, band.cost_low_bn), ("high", hi, band.cost_high_bn)):
        got = -welfare(corner)
        if abs(got - want) > 5e-4:
            raise SystemExit(f"[BLOCKED] adopted {profile} {name} rebuilt {got:.4f}, published {want:.4f}")
    # Published (September 20) band, exact: the evaluator reproduces the engine to 1e-6.
    pub = MODEL["meta"]["headline"]["category_service_response_sensitivity"][profile]
    base = [welfare(c) for c in corners(profile, 0.0, 0.0, 0.0)]
    if abs(min(base) - pub["min_welfare_bn"]) > 1e-6 or abs(max(base) - pub["max_welfare_bn"]) > 1e-6:
        raise SystemExit(f"[BLOCKED] published {profile} band not reproduced")
    return {"low": lo, "high": hi}


MEDICAID = "medicaid_and_chip_other_medical"


def case_profiles(case: str | None) -> dict[str, tuple[str, bool]]:
    """A case's profiles: profile -> (this lane's PROFILES entry, whether the long-run lines take the
    specification's long-run responses). Cases without profiles of their own use PROFILES."""
    c = LATER_CASES.get(case) if case else None
    return dict(c.profiles) if c is not None and c.profiles else {p: (p, False) for p in PROFILES}


def main_profile(case: str | None) -> str:
    return next(iter(case_profiles(case)))


def later_fields(meta: dict, long_run: bool, reading: str, model: dict | None = None) -> dict:
    """The September 27 fields of a corner at one reading ("low" where general government takes its low
    response, else "high"), from the payload's meta, as package.cjs specsFor() and stateFor() set them:
      line_responses  engine.js response_override: the long-run lines (where the profile lets them take
                      the long-run response), rental assistance, and each receipt that names an override;
      long_run, subfunctions, subfunction_rows  the specification's long-run responses and subfunctions;
      rate, capital_meta  the return on public capital at the reading (capital_rows);
      capped          the capped programs, reported apart from the cash gap (split_corner).
    From September 29 every other meta.responses entry named for a spending line of the model (the payload's
    synthetic lines: roads by miles, state pricing) takes its reading too, as consumer.cjs lineResponses sets
    it, where the long-run lines do; each responds as its parent, so where the profile holds every service at 1
    (the proportional reference) it responds at 1, its class's response. Public housing's enterprise deficit is
    a capped program (displaced beneficiaries) like rental assistance."""
    r, capital = meta["responses"], meta["capital_return"]
    over = {line: r[line][reading] for line in LONG_RUN_LINES if long_run}
    over["housing_subsidies"] = r["housing_subsidies"][reading]
    for v in r.values():
        if isinstance(v, dict) and v.get("receipt"):
            over[v["override"]] = v[reading]
    capped = list(CAPPED)
    if model is not None:
        ids = {line["id"] for line in model["spending"]["lines"]}
        for line, v in r.items():
            if line in ids and line not in over and line not in LONG_RUN_LINES and long_run:
                if not isinstance(v, dict) or not all(isinstance(v.get(x), (int, float)) for x in ("low", "high")):
                    raise SystemExit(f"[BLOCKED] meta.responses.{line} has no low and high response")
                over[line] = v[reading]
        if any(x["id"] == HOUSING_ENTERPRISE for x in model["receipts"]["lines"]):
            capped.append(HOUSING_ENTERPRISE)
    if capital["enterprises"] != r[ENTERPRISE_RECEIPT]["option"]:
        raise SystemExit("[BLOCKED] the capital return's enterprise option is not the receipt's")
    return dict(reading=reading, line_responses=over, long_run={line: r[line][reading] for line in LONG_RUN_LINES},
                subfunctions={sf["id"]: sf[reading] for line in LONG_RUN_LINES for sf in r[line]["subfunctions"]},
                subfunction_rows={line: r[line]["subfunctions"] for line in LONG_RUN_LINES},
                rate=capital["rates"][reading], capital_meta=capital, capped=capped)


def frame_corners(profile: str, model: dict, responses: dict | None = None, case: str | None = None,
                  meta: dict | None = None) -> list[dict]:
    """The September 24 frame (package.cjs MAIN_SPECS): 64 specifications for the main profile, justice
    on the use key, Medicaid on the two uninsured-use keys, general government 0.59 or 0.84. The Sept 23
    changes sit in those keys; `justice` and `uc` record how much, for the federal split.

    With responses (a payload's meta.responses, September 26 on) general government takes their low
    and high values and schools their growth and decline values (school_responses); a profile whose
    schools respond in full keeps its own. A case with profiles of its own (September 27) names the
    profile; each corner then carries the case's fields at its reading (later_fields, from the payload's
    meta)."""
    base, long_run = case_profiles(case)[profile] if case else (profile, False)
    spec, gg = PROFILES[base], INPUTS["general_government_response"]
    schools = school_responses(base, responses)
    if responses is not None:
        gg = responses["general_government"]
    out = []
    for alloc, norm, share, school, g, uc in product(("personal", "shared"), ("cash", "gdp"), SCHOOL_SHARES,
                                                    schools, (gg["low"], gg["high"]), tuple(UC_KEYS)):
        out.append(dict(profile=profile, allocation=alloc, normalization=norm, school_share=share,
                        school_response=school, other_edu=spec["other_edu"], delayed=spec["delayed"], gg=g,
                        gg_end="low" if g == gg["low"] else "high", uc_key=uc, uc_arm=UC_KEYS[uc],
                        justice=INPUTS["justice_change_bn"]["central"], uc=INPUTS["uncompensated_inside_bn"][UC_KEYS[uc]],
                        shift={}, keys={"public_order_safety": "use", MEDICAID: uc}, model=model))
        if case is not None and LATER_CASES[case].profiles:
            out[-1].update(later_fields(meta, long_run, out[-1]["gg_end"], model))
    return out


def sept24_anchors(profile: str, corrected: dict, main24: dict) -> dict[str, dict]:
    """Corners that set the September 24 band. Gates: the uncorrected model on the frame reproduces the
    September 23 band and the corrected model the adopted September 24 band (summary.json, 1e-6); the
    use and uninsured-use keys carry exactly the adopted justice and uncompensated-care changes."""
    want = {"corrected": main24["main_case"], "uncorrected": main24["adopted_2026_09_23"]}
    if profile != MAIN:
        other = main24["other_profiles"][profile]
        want = {"corrected": other["adopted"], "uncorrected": other["sept23"]}
    return frame_anchors(profile, corrected, want)


def case_anchors(profile: str, corrected: dict, main26: dict, responses: dict, case: str | None = None,
                 meta: dict | None = None) -> dict[str, dict]:
    """Corners that set a later case's band (LATER_CASES): the same frame at the case's responses. Gates:
    the uncorrected model reproduces the case lane's uncorrected_at_adopted_responses band and the
    corrected model its adopted band (summary.json, 1e-6), for every profile."""
    want = {"corrected": main26["main_case"], "uncorrected": main26["uncorrected_at_adopted_responses"]}
    if profile != main_profile(case):
        other = main26["other_profiles"][profile]
        want = {"corrected": other["adopted"], "uncorrected": other["uncorrected_at_adopted_responses"]}
    return frame_anchors(profile, corrected, want, responses, case, meta)


def frame_anchors(profile: str, corrected: dict, want: dict, responses: dict | None = None, case: str | None = None,
                  meta: dict | None = None) -> dict[str, dict]:
    """The band's corners on the frame, gated against the published uncorrected and corrected bands. The
    band's ends are the corners of least and most cost (cost(): the engine's cost plus any capital return)."""
    lines = {l["id"]: l for l in MODEL["spending"]["lines"]}
    for a in ("personal", "shared"):
        pos, med = lines["public_order_safety"]["keys"], lines[MEDICAID]["keys"]
        if abs(pos["use"][a]["target_bn"] - pos["population"][a]["target_bn"]
               - INPUTS["justice_change_bn"]["central"]) > 1e-9:
            raise SystemExit("[BLOCKED] the use key does not carry the adopted justice change")
        for uc, arm in UC_KEYS.items():
            if abs(med[uc][a]["target_bn"] - med["medicaid"][a]["target_bn"] - INPUTS["uncompensated_inside_bn"][arm]) > 1e-9:
                raise SystemExit(f"[BLOCKED] {uc} does not carry the adopted uncompensated care")
    out = {}
    for name, model in (("uncorrected", MODEL), ("corrected", corrected)):
        cs = frame_corners(profile, model, responses, case, meta)
        lo, hi = min(cs, key=cost), max(cs, key=cost)
        got = [cost(lo), cost(hi)]
        if max(abs(g - w) for g, w in zip(got, want[name])) > 1e-6:
            raise SystemExit(f"[BLOCKED] {profile} {name} band {got} != published {want[name]}")
        out[name] = {"low": lo, "high": hi}
    return out["corrected"]


# ---------------------------------------------------------------- federal shares by line and year

def federal_shares(wb: Workbook, grants: Grants, e_tax: float = 0.789, e_sl: float = 0.842) -> dict:
    """Per convention: line id -> Series of federally funded share, 2005-2024; plus pieces for special lines.

    e_tax and e_sl are the responses of federal tax collection and of state-local general government
    at the low end of the general-government response: their elasticities (scaling_check.json) through
    September 24, their finite-removal responses since September 26."""
    t317 = lambda n, label=None: wb.line("T31700-A", n, label)
    t312 = lambda n, label=None: wb.line("T31200-A", n, label)
    functions = {  # consolidated consumption, federal consumption, SL consumption, SL benefits, federal grants
        "gps": (2, 12, 22, 51, 58), "pos": (4, 14, 23, 52, 60), "econ": (5, 15, 24, 53, 61),
        "housing": (6, 16, 25, None, 69), "health": (7, 17, 26, 54, 70), "recreation": (8, 18, 29, None, 71),
        "education": (9, 19, 30, 55, 72), "income_security": (10, 20, 31, 56, 73)}
    g, fc, sc, sb, gr = {}, {}, {}, {}, {}
    for f, (a, b, c, d, e) in functions.items():
        g[f], fc[f], sc[f] = t317(a), t317(b), t317(c)
        sb[f] = t317(d) if d else pd.Series(0.0, index=YEARS)
        gr[f] = t317(e)
        if not np.allclose(g[f], fc[f] + sc[f], atol=0.0015):
            raise SystemExit(f"[BLOCKED] Table 3.17 {f}: consolidated consumption is not federal + state-local")

    # Medicaid: CMS's calendar-year federal share of Medicaid spending (NHEA Table 3) on the whole line
    # (BEA Medicaid plus other medical care, 98% Medicaid). The rest of BEA's health grants (Medicaid
    # administration, vaccines, public health) funds state-local health consumption. OMB 12.3 names the
    # health grants that are fixed appropriations rather than open-ended matches (all but Medicaid, CHIP,
    # its contingency fund and Basic Health Program payments); the low convention keeps only the matching part.
    health = grants.section("550 HEALTH", "Total, 550")
    med_fy = sum(grants.program(p, health) for p in ("Grants to States for Medicaid", "Children's Health Insurance Fund",
                                                     "Child Enrollment Contingency Fund", "Refundable Premium Tax Credit"))
    block_health = Grants.calendar(grants.program("Total, 550", health) - med_fy)
    medical_care = t312(33, "Medicaid") + t312(34, "Other medical care")
    nhea_share = nhea_medicaid_federal_share()
    fed_medicaid = nhea_share * medical_care
    resid_health = (gr["health"] - fed_medicaid).clip(lower=0)
    other_sl_health_ben = (sb["health"] - medical_care).clip(lower=0)
    health_weight = sc["health"] / (sc["health"] + other_sl_health_ben)

    # OMB 12.3 income security: LIHEAP, and the open-ended (caseload-following) programmes.
    income = grants.section("600 INCOME SECURITY", "Total, 600")
    liheap = Grants.calendar(grants.program("Low income home energy assistance", income))
    matching = sum(Grants.calendar(grants.program(p, income)) for p in (
        "SNAP (formerly Food Stamps)", "Commodity Assistance Program", "Supplemental feeding programs (WIC and CSFP)",
        "Child Nutrition Programs", "Funds for strengthening markets, income, and supply (section 32)",
        "Family support payments to States", "Refugee and entrant assistance",
        "Payments to States for Foster Care and Adoption Assistance",
        "Unemployment trust fund (administrative expenses)", "Unemployment Trust Fund"))
    block_ex_liheap = sum(Grants.calendar(grants.program(p, income)) for p in (
        "Payments to States for Child Care/Develop Block Grants", "Contingency Fund", "Child Care Entitlement to States",
        "Temporary Assistance for Needy Families"))
    matching_fraction = matching / (matching + block_ex_liheap)
    energy = t312(38, "Energy assistance")
    welfare_ben = t312(35, "Family assistance") + t312(37, "General assistance") + t312(39, "Other")
    is_base = sc["income_security"] + welfare_ben
    is_resid = (gr["income_security"] - liheap).clip(lower=0)

    k12 = wb.line("T31600-A", 107, "Elementary and secondary")
    k12_ratio = gr["education"] / k12
    school_high = K12_FEDERAL_HIGH * k12_ratio / k12_ratio[LAST]

    def cons_share(f: str, grant_part: pd.Series) -> pd.Series:
        return ((fc[f] + grant_part) / g[f]).clip(0, 1)

    def pro_rata(f: str) -> pd.Series:           # grants spread over SL consumption and SL benefits
        return (gr[f] / (sc[f] + sb[f])).clip(0, 1)

    one, zero = pd.Series(1.0, index=YEARS), pd.Series(0.0, index=YEARS)
    wc = t312(15, "Workers' compensation") / (t312(15) + t312(30, "Workers' compensation"))
    ssi = t312(23, "Supplemental security income") / (t312(23) + t312(36, "Supplemental security income"))
    federal_benefits = ["social_security", "medicare", "unemployment", "railroad_retirement", "pension_guaranty",
                        "veterans_life_insurance", "military_medical", "veterans_pension_disability",
                        "veterans_readjustment", "veterans_other", "snap", "black_lung", "refundable_tax_credits",
                        "other_federal_benefits"]

    # Receipts: the collecting government, from Tables 3.2-3.6.
    t36 = lambda n: wb.line("T30600-A", n)
    odsc_fed = sum(t36(n) for n in (7, 12, 13, 14, 15, 16, 28, 29, 30))
    odsc_sl = t36(17) + t36(31)
    excise = wb.line("T30500-A", 4, "Excise taxes") / (wb.line("T30500-A", 4) + wb.line("T30500-A", 23, "Excise taxes"))
    transfers = wb.line("T30200-A", 21, "From persons") / wb.line("T30100-A", 17, "From persons")
    labour_fed = (wb.line("T30400-A", 3, "Income taxes") + sum(t36(n) for n in (5, 6, 24, 25, 26)))
    labour_share = labour_fed / (labour_fed + wb.line("T30400-A", 9, "Income taxes"))
    receipts = {"federal_income_tax": one, "employee_oasdi": one, "employee_hi": one, "self_employment_oasdi_hi": one,
                "employer_oasdi": one, "employer_hi": one, "medicare_supplementary_premiums": one,
                "customs_duties": one, "other_domestic_social_contributions": odsc_fed / (odsc_fed + odsc_sl),
                "excise_selective_sales": excise, "personal_current_transfers": transfers}
    for rid in ("state_local_income_tax", "personal_motor_vehicle", "other_personal_tax", "general_sales_tax"):
        receipts[rid] = zero

    out = {}
    for conv in CONVENTIONS:
        s = {rid: v for rid, v in receipts.items()}
        for lid in federal_benefits:
            s[lid] = one
        s.update(workers_compensation=wc, ssi=ssi, temporary_disability=zero, other_state_benefits=zero, defense=one,
                 housing_community_services=(fc["housing"] / g["housing"]).clip(0, 1))
        if conv == "low":
            s["medicaid_and_chip_other_medical"] = nhea_share
            s["health_services"] = cons_share("health", (resid_health - block_health).clip(lower=0) * health_weight)
            s["energy_assistance"] = zero
            share_is = (matching_fraction * is_resid / is_base).clip(0, 1)
            s["general_public_services"] = cons_share("gps", zero)
            s["public_order_safety"] = cons_share("pos", zero)
            s["economic_affairs_services"] = cons_share("econ", zero)
            s["recreation_culture"] = cons_share("recreation", zero)
            s["education_services"] = cons_share("education", zero)
            s["education_benefits"] = zero
            s["employment_training"] = zero
        else:
            if conv == "high":
                s["medicaid_and_chip_other_medical"] = (gr["health"] / medical_care).clip(0, 1)
                s["health_services"] = cons_share("health", zero)
            else:
                s["medicaid_and_chip_other_medical"] = nhea_share
                s["health_services"] = cons_share("health", resid_health * health_weight)
            s["energy_assistance"] = (liheap / energy).clip(0, 1)
            share_is = (is_resid / is_base).clip(0, 1)
            for f, lid in (("gps", "general_public_services"), ("pos", "public_order_safety"),
                           ("econ", "economic_affairs_services"), ("recreation", "recreation_culture"),
                           ("education", "education_services")):
                s[lid] = cons_share(f, pro_rata(f) * sc[f])
            s["education_benefits"] = pro_rata("education")
            s["employment_training"] = pro_rata("econ")
        s["family_and_general_assistance"] = share_is
        s["other_state_welfare"] = share_is
        s["income_security_services"] = cons_share("income_security", share_is * sc["income_security"])
        s["_school_high"] = school_high
        s["_induced_receipts"] = labour_share
        out[conv] = pd.DataFrame(s)

    # General government at the low end of the adopted response: federal executive and legislative
    # budget fixed, federal tax collection at e_tax, state-local at e_sl (0.789 and 0.842 through
    # September 24, scaling_check.json).
    t316 = lambda n, label=None: wb.line("T31600-A", n, label)
    fed_tax = t316(45, "Tax collection and financial management")
    fed_exec = t316(44, "Executive and legislative")
    sl_gps = t316(82, "Executive and legislative") + t316(83, "Tax collection and financial management") + \
        t316(85, "Other") - gr["gps"]
    gps_grants_part = pro_rata("gps") * sc["gps"]
    consumption_low = (fed_tax * e_tax + e_sl * gps_grants_part) / (fed_tax * e_tax + e_sl * sc["gps"])
    composite_low = fed_tax * e_tax / (fed_tax * e_tax + e_sl * sl_gps)
    composite_high = (fed_exec + fed_tax) / (fed_exec + fed_tax + sl_gps)
    consumption_high = out["central"]["general_public_services"]
    gps = {"central": (consumption_low, consumption_high), "low": (composite_low, consumption_high),
           "high": (consumption_low, composite_high)}

    # The federal part of state-local consumption of a function alone (September 29: roads keyed by miles and the
    # state-price gaps are state-local spending): the grant part each convention gives state-local consumption,
    # over that consumption. Public order, economic affairs and recreation: their grant share (0 under the low
    # convention); health: the residual grants the central and low conventions give it (0 under the high one,
    # which puts every health grant on Medicaid).
    health_sl = {"central": resid_health * health_weight, "low": (resid_health - block_health).clip(lower=0) * health_weight,
                 "high": pd.Series(0.0, index=YEARS)}
    sl_federal_share = {conv: dict({f: (pd.Series(0.0, index=YEARS) if conv == "low" else pro_rata(f))
                                    for f in ("pos", "econ", "recreation")},
                                   health=(health_sl[conv] / sc["health"]).clip(0, 1))
                        for conv in CONVENTIONS}
    extras = dict(nhea_share=nhea_share, resid_health=resid_health, block_health=block_health,
                  matching_fraction=matching_fraction, liheap=liheap,
                  is_resid=is_resid, is_base=is_base, gps=gps, k12_ratio=k12_ratio, labour_share=labour_share,
                  odsc_total=odsc_fed + odsc_sl, sl_gps_grant_share=pro_rata("gps"),
                  sl_grant_share={f: pro_rata(f) for f in ("econ", "recreation")},
                  consumption_by_level={f: (fc[f], sc[f]) for f in ("econ", "recreation")},
                  sl_federal_share=sl_federal_share)
    return out, extras


def case_shares(shares: dict, wb: Workbook) -> dict:
    """Shares for the lines the September 27 case makes respond that earlier cases held at 0.

    housing_subsidies   rental assistance: federal (NIPA 3.13 line 4 is a federal subsidy line). A capped
                        program: its federal part is reported with the displaced beneficiaries, never
                        compounded.
    enterprise_surplus  the receipt's federal share, t32(23) / t31(19) in 2024 (NIPA 3.2 line 23 over 3.1
                        line 19). It is held at its 2024 value in every year of this table: the programme
                        rule carries each level with its own series (RECEIPT_SERIES), and the federal
                        enterprises' result changes sign in 2005-2009 and 2016-2022, so no earlier year's
                        ratio is a share.
    Returns the added shares' 2024 values; the columns are added to every convention in place."""
    fed, total = wb.line("T30200-A", 23, "Current surplus of government enterprises")[LAST], \
        wb.line("T30100-A", 19, "Current surplus of government enterprises")[LAST]
    enterprise = fed / total
    if not 0 < enterprise < 1:
        raise SystemExit(f"[BLOCKED] the enterprise surplus's 2024 federal share {enterprise} is not a share")
    for conv in CONVENTIONS:
        shares[conv]["housing_subsidies"] = 1.0
        shares[conv][ENTERPRISE_RECEIPT] = enterprise
    return dict(housing_subsidies=1.0, enterprise_surplus=float(enterprise), enterprise_surplus_federal_bn_2024=float(fed),
                enterprise_surplus_national_bn_2024=float(total))


STATE_PRICE_FUNCTIONS = {"public_order_safety": "pos", "health_services": "health", "recreation_culture": "recreation"}


def v4_shares(shares: dict, extras: dict, wb: Workbook, corrected: dict, meta: dict) -> tuple[dict, dict]:
    """Federal shares for the lines the September 29 case adds or re-scales, on a copy of the shares, so the
    earlier cases a run rebuilds keep theirs. Returns the copy and the rules with their 2024 values.

      modeled_owner_property, tenant_occupied_property, personal_property_tax
                          state-local property taxes (NIPA 3.3 line 9, 3.4 line 11): 0.
      housing_enterprise_surplus  public housing's enterprise deficit, consolidated with its operating subsidy:
                          the subsidy that left rental assistance (a federal subsidy, NIPA 3.13 line 4) is federal
                          and the deficit that left the enterprise surplus is state-local (the federal enterprises'
                          whole 2024 surplus, NIPA 3.2 line 23, is -$1.8bn; the state-local enterprises', 3.3 line
                          22, holds it). The share is the subsidy over the line, in every convention, as rental
                          assistance is federal in every convention.
      enterprise_surplus  the line's key times the federal enterprises' 2024 surplus, t32(23), which the split leaves
                          in the line: the share is t32(23) over the line's national total in the model at hand
                          (split_corner; the column _enterprise_federal_bn carries t32(23)), t31(19)'s share on the
                          model before the split and t32(23) / (t31(19) less the housing deficit) after it, held in
                          every year as case_shares holds it. The column enterprise_surplus is the latter.
      roads_vmt_fed       federal highways: 1.
      roads_vmt_sl        state-local highways: federal only through grants, at economic affairs' share
                          (sl_federal_share; 0 under the low convention), as long_run_fraction splits the
                          state-local subfunctions.
      state_price_<line>  the state-price gap of the parent's state-local functions: state-local spending, federal
                          only through the grants the convention gives state-local consumption of the function
                          (sl_federal_share).
    Gates: the housing line's national total is the deficit and the subsidy that left the two lines (1e-9); the
    deficit fits the state-local enterprises and not the federal ones, and it is NIPA 3.8 line 13, whose other
    state-local lines are the rest of the state-local enterprises (BEA rounding); the state-price lines' parents are
    the payload's (meta.state_pricing); every share lies in [0, 1]."""
    national = lambda m, side, i: next(x for x in m[side]["lines"] if x["id"] == i)["national_bn"]  # noqa: E731
    subsidy = national(MODEL, "spending", "housing_subsidies") - national(corrected, "spending", "housing_subsidies")
    deficit = national(MODEL, "receipts", ENTERPRISE_RECEIPT) - national(corrected, "receipts", ENTERPRISE_RECEIPT)
    housing = national(corrected, "receipts", HOUSING_ENTERPRISE)
    fed_ent = float(wb.line("T30200-A", 23, "Current surplus of government enterprises")[LAST])
    sl_ent = float(wb.line("T30300-A", 22, "Current surplus of government enterprises")[LAST])
    if abs(housing - (deficit - subsidy)) > 1e-9 or not (sl_ent <= deficit < fed_ent < 0) or subsidy <= 0:
        raise SystemExit(f"[BLOCKED] public housing's line ({housing}) is not the deficit ({deficit}) and the "
                         f"subsidy ({subsidy}) that left the enterprise surplus and rental assistance")
    # The programme rule's series (RECEIPT_SERIES_V4): NIPA 3.8 line 13 is the deficit, and lines 8-12, 14 and 15
    # are the state-local enterprises without it (BEA rounds each line to $1m).
    t38 = lambda n: float(wb.line("T30800-A", n)[LAST])  # noqa: E731
    for sheet, n, label in (("T30800-A", 13, "Housing and urban renewal"), ("T30800-A", 7, "State and local"),
                            ("T31300-A", 4, "Housing"), ("T30300-A", 9, "Property taxes"), ("T30400-A", 11, "Property taxes")):
        wb.line(sheet, n, label)                                         # stops on another label
    if abs(t38(13) - deficit) > 5e-4 or abs(sum(t38(n) for n in (8, 9, 10, 11, 12, 14, 15)) - (sl_ent - t38(13))) > 5e-3 \
            or abs(t38(7) - sl_ent) > 5e-4 or abs(t38(2) - fed_ent) > 5e-4:
        raise SystemExit("[BLOCKED] NIPA 3.8 does not split the enterprises as RECEIPT_SERIES_V4 carries them")
    ent_national = national(corrected, "receipts", ENTERPRISE_RECEIPT)
    parents = {x["line"]: x["parent"] for x in meta["state_pricing"]["lines"]}
    if set(parents) != {i for i in V4_SYNTHETIC if i.startswith("state_price_")} or \
            any(parents[i] != i[len("state_price_"):] or parents[i] not in STATE_PRICE_FUNCTIONS for i in parents):
        raise SystemExit(f"[BLOCKED] the payload's state-price lines and parents are not these: {parents}")
    out = {conv: df.copy() for conv, df in shares.items()}
    const = lambda v: pd.Series(float(v), index=YEARS)  # noqa: E731
    for conv in CONVENTIONS:
        s, sl = out[conv], extras["sl_federal_share"][conv]
        for rid in ("modeled_owner_property", "tenant_occupied_property", "personal_property_tax"):
            s[rid] = const(0.0)
        s[HOUSING_ENTERPRISE] = const(-subsidy / housing)
        s[ENTERPRISE_RECEIPT] = const(fed_ent / ent_national)
        s["_enterprise_federal_bn"] = const(fed_ent)
        s["roads_vmt_fed"] = const(1.0)
        s["roads_vmt_sl"] = sl["econ"].reindex(YEARS)
        for line, parent in parents.items():
            s[line] = sl[STATE_PRICE_FUNCTIONS[parent]].reindex(YEARS)
        added = [c for c in s.columns if c in (HOUSING_ENTERPRISE, ENTERPRISE_RECEIPT, "roads_vmt_sl", *parents)]
        if ((s[added] < 0) | (s[added] > 1)).any().any():
            raise SystemExit(f"[BLOCKED] {conv}: a September 29 share outside [0, 1]")
    rules = dict(
        property_taxes=dict(lines=["modeled_owner_property", "tenant_occupied_property", "personal_property_tax"],
                            share=0.0, rule="state-local property taxes (NIPA 3.3 line 9, 3.4 line 11)"),
        housing_enterprise_surplus=dict(share=-subsidy / housing, national_bn=housing, operating_subsidy_bn=subsidy,
                                        enterprise_deficit_bn=deficit, federal_enterprise_surplus_2024_bn=fed_ent,
                                        state_local_enterprise_surplus_2024_bn=sl_ent,
                                        rule="the operating subsidy that left rental assistance is federal; the deficit "
                                             "that left the enterprise surplus is state-local; every convention",
                                        alternative="the enterprise surplus's September 27 share, t32(23)/t31(19)"),
        enterprise_surplus=dict(share=fed_ent / ent_national, national_bn=ent_national,
                                share_before_the_split=fed_ent / national(MODEL, "receipts", ENTERPRISE_RECEIPT),
                                rule="the line's key times the federal enterprises' surplus t32(23), which stays in the "
                                     "line: t32(23) over the line's national total after the housing deficit left it; "
                                     "the re-key edits move the key at the share before the split and the national-"
                                     "scale edit, which removes a state-local deficit, moves no federal dollars",
                                alternative="t32(23)/t31(19), the September 27 share, on the line after the split, "
                                            "which would count most of the federal enterprises' deficit as "
                                            "state-local"),
        roads_vmt_fed=dict(share=1.0, rule="federal highways"),
        roads_vmt_sl={conv: float(out[conv].loc[LAST, "roads_vmt_sl"]) for conv in CONVENTIONS},
        state_price={line: {conv: float(out[conv].loc[LAST, line]) for conv in CONVENTIONS} for line in parents},
        state_local_only_rule="federal only through the grants each convention gives state-local consumption of the "
                              "function (0 under the low convention; health 0 under the high one)")
    return out, rules


def subfunction_levels(responses: dict, extras: dict) -> dict:
    """Gate: each long-run line's subfunctions (meta.responses, from responses.json) add, level by level, to
    NIPA 3.17's 2024 federal and state-local consumption of its function (1e-6), so their levels split the
    line as the lane's consumption shares do."""
    out = {}
    for line, f in LONG_RUN_FUNCTIONS.items():
        fed, sl = (float(x[LAST]) for x in extras["consumption_by_level"][f])
        subs = responses[line]["subfunctions"]
        got = {lv: sum(sf["national_bn"] for sf in subs if sf["level"] == lv) for lv in ("federal", "state_local")}
        if abs(got["federal"] - fed) > 1e-6 or abs(got["state_local"] - sl) > 1e-6:
            raise SystemExit(f"[BLOCKED] {line}: subfunctions by level {got} are not NIPA 3.17's {fed}, {sl}")
        out[line] = dict(federal_bn=got["federal"], state_local_bn=got["state_local"])
    return out


# ---------------------------------------------------------------- special lines: justice change and uncompensated care

def justice_federal(wb: Workbook) -> dict[str, float]:
    """Federal part of the +$5.94bn justice-by-use change, from the lane's central split and BEA Table 3.16."""
    split = pd.read_csv(FISCAL / "cj_use_allocation_2026_09_23/derived/central_split.csv").set_index("component")
    summary = json.loads((FISCAL / "cj_use_allocation_2026_09_23/derived/summary.json").read_text())
    change = split.use_bn - split.per_head_bn
    if abs(change.sum() - INPUTS["justice_change_bn"]["central"]) > 1e-5:
        raise SystemExit("[BLOCKED] justice components do not sum to the adopted change")
    t316 = lambda n, label: wb.line("T31600-A", n, label)[LAST]
    scale = summary["sublines_bn"]["police"] / t316(9, "Police")
    fed_police_nonborder = t316(50, "Police") * scale - split.loc["police_cbp", "national_bn"] - \
        split.loc["police_ice_border", "national_bn"] - split.loc["police_ice_interior", "national_bn"]
    share = {"police_non_border": fed_police_nonborder / split.loc["police_non_border", "national_bn"],
             "law_courts": t316(52, "Law courts") / t316(11, "Law courts"),
             "prisons": t316(53, "Prisons") / t316(12, "Prisons"),
             "police_ice_interior": 1.0, "police_cbp": 1.0, "police_ice_border": 1.0, "fire": t316(51, "Fire") / t316(10, "Fire")}
    base = sum(change[c] * share[c] for c in change.index)
    prisons = change["prisons"]
    return dict(change_bn=float(change.sum()), central=float(base),
                low=float(base - prisons * share["prisons"]), high=float(base + prisons * (1 - share["prisons"])),
                components={c: float(change[c]) for c in change.index}, shares={k: float(v) for k, v in share.items()})


def uncompensated_federal(medicaid_share: float) -> dict[str, dict[str, float]]:
    """Federal part of the under-charged uncompensated care, programme by programme.

    Re-derives the lane's two endpoints (uncompensated.py: OFFSETS, keys, target share) and splits
    each programme's part by payer: Medicaid DSH at the Medicaid line's federal share, Medicare DSH
    federal, the state-local programme group federal only for its federal grants (community health
    centres, Ryan White, Title V: 3.0+1.5+0.1 of 21.7 in 2013; community health centres 1.3 of 11.2
    in 2017) [INFERENCE: mapping of the lane's summed components to KFF-Urban table rows].
    """
    summary = json.loads((FISCAL / "uncompensated_care_2026_09_23/derived/summary.json").read_text())
    s = summary["target_share"]
    keys = summary["account_key_shares"]
    arms = {"equal_low": dict(total_uc=84.9 - 8.1 - 2.1, n=summary["aha_national_bn"], sl_key="per_head",
                              programs={"medicaid": 13.5, "medicare": 8.0, "state_local": 21.7},
                              sl_federal=(3.0 + 1.5 + 0.1) / 21.7),
            "equal_high": dict(total_uc=42.4 - 10.3 - 2.3, n=summary["aha_national_bn"] * summary["uplift_2024"],
                               sl_key="health_other", programs={"medicaid": 9.8, "state_local": 11.2},
                               sl_federal=1.3 / 11.2)}
    out = {}
    for name, a in arms.items():
        parts = {p: v / a["total_uc"] * (s - keys[a["sl_key"] if p == "state_local" else p]) * a["n"]
                 for p, v in a["programs"].items()}
        total = sum(parts.values())
        if abs(total - INPUTS["uncompensated_inside_bn"][name]) > 1e-6:
            raise SystemExit(f"[BLOCKED] uncompensated {name} rebuilt {total}, adopted {INPUTS['uncompensated_inside_bn'][name]}")
        fed = {"medicaid": medicaid_share, "medicare": 1.0, "state_local": a["sl_federal"]}
        central = sum(parts[p] * fed[p] for p in parts)
        low = central - parts["state_local"] * a["sl_federal"]
        out[name] = dict(total=total, central=central, low=low, high=central, parts=parts)
    return out


# ---------------------------------------------------------------- the federal split of one corner

def long_run_fraction(corner: dict, line: str, response: float, conv: str, extras: dict) -> pd.Series:
    """Federal fraction of a long-run line's responsive amount by year (September 27 on).

    Each subfunction (responses.json, carried in the payload's meta.responses) takes its reading's
    response where the line takes the specification's long-run response, else the line's own response.
    Federal subfunctions are federal; state-local ones are federal only through grants, at the function's
    grant share of state-local consumption and benefits (pro_rata, as the line's central share), and 0
    under the low convention, which counts grants as state-local. Gate: the subfunctions blend to the
    line's response (1e-12)."""
    subs = corner["subfunction_rows"][line]
    own = line in corner.get("line_responses", {})
    weights = [(sf["share_of_line"] * (corner["subfunctions"][sf["id"]] if own else response), sf["level"]) for sf in subs]
    if abs(sum(w for w, _ in weights) - response) > 1e-12:
        raise SystemExit(f"[BLOCKED] {line}: the subfunctions do not blend to the line's response {response}")
    grant = (pd.Series(0.0, index=YEARS) if conv == "low"
             else extras["sl_grant_share"][LONG_RUN_FUNCTIONS[line]].reindex(YEARS))
    federal = sum(w * (1.0 if level == "federal" else grant) for w, level in weights)
    return federal / response


def split_corner(corner: dict, shares: pd.DataFrame, extras: dict, conv: str, year: int,
                 jf: dict, ucf: dict, end: str, parts: list | None = None) -> pd.DataFrame:
    """The 2024 fiscal gap at one corner by line, split by government. From September 27 a corner that
    names capped programs gets a financing column: displaced_beneficiaries for their lines, cash for the
    rest (the capital return is not an engine line: capital_rows)."""
    t = lines_at(corner)
    phi = shares.loc[year]
    rows = []
    for r in t.itertuples():
        if r.responsive_bn == 0:
            continue
        sign = 1.0 if r.side == "spending" else -1.0     # gap = spending - receipts
        amount = r.responsive_bn
        if r.side == "spending" and r.id in LONG_RUN_LINES and "subfunction_rows" in corner:
            fed = amount * long_run_fraction(corner, r.id, r.response, conv, extras)[year]
        elif r.id == "general_public_services":
            lo, hi = extras["gps"][conv]
            frac = lo[year] if corner.get("gg_end", end) == "low" else hi[year]
            fed = amount * frac
        elif r.id == "public_order_safety":
            fed = (amount - corner["justice"] * r.response) * phi[r.id] + jf[conv] * r.response
        elif r.id == "medicaid_and_chip_other_medical":
            uc_name = corner.get("uc_arm", "equal_low" if end == "low" else "equal_high")
            fed = (amount - corner["uc"] * r.response) * phi[r.id] + ucf[uc_name][conv] * r.response
        elif r.id == "education_services" and conv == "high":
            school = r.amount_bn * corner["school_share"] * corner["school_response"]
            fed = school * phi["_school_high"] + (amount - school) * shares.loc[year, "education_services"]
        elif r.id == "school_reprice":
            fed = amount * (phi["_school_high"] if conv == "high" else phi["education_services"])
        elif r.id == "college_rekey":
            fed = amount * phi["education_services"]
        elif r.id == "lane_constants":
            if parts is None or abs(sum(p["amount"] for p in parts) - amount) > 1e-9:
                raise SystemExit("[BLOCKED] the constant line's parts do not add to the line")
            fed = sum(p["amount"] * p["share"][year] for p in parts)
        elif r.id == ENTERPRISE_RECEIPT and "_enterprise_federal_bn" in phi.index:
            fed = amount * phi["_enterprise_federal_bn"] / r.national_bn     # September 29: key x t32(23) (v4_shares)
        else:
            if r.id not in phi.index:
                raise SystemExit(f"[BLOCKED] no federal share for responsive line {r.id}")
            fed = amount * phi[r.id]
        rows.append(dict(side=r.side, id=r.id, responsive_bn=sign * amount, federal_bn=sign * fed))
    p, f = production(corner["normalization"], corner.get("model"))
    rows.append(dict(side="production", id="induced_receipts_F", responsive_bn=-f,
                     federal_bn=-f * phi["_induced_receipts"]))
    out = pd.DataFrame(rows)
    out["state_local_bn"] = out.responsive_bn - out.federal_bn
    if "capped" in corner:              # capped spending lines, and from September 29 public housing's receipt line
        out["financing"] = np.where(out.side.isin(["spending", "receipt"]) & out.id.isin(corner["capped"]),
                                    "displaced_beneficiaries", "cash")
    return out


def cash_part(table: pd.DataFrame) -> pd.DataFrame:
    """The rows that are financed: all of them, or the cash rows where a financing column exists."""
    return table[table.financing == "cash"] if "financing" in table.columns else table


def capital_split(corner: dict) -> pd.DataFrame:
    """The capital return at one corner as split rows (resource cost): federal components federal."""
    c = capital_rows(corner)
    return pd.DataFrame(dict(side="capital_return", id=c.id, responsive_bn=c.return_bn,
                             federal_bn=np.where(c.level == "federal", c.return_bn, 0.0),
                             state_local_bn=np.where(c.level == "federal", 0.0, c.return_bn),
                             financing="resource_cost", part=c.part))


def three_columns(table: pd.DataFrame, capital: pd.DataFrame) -> dict[str, float]:
    """Cash financing, resource cost and displaced beneficiaries at one corner, each with its federal part."""
    cash = cash_part(table)
    displaced = table[table.financing == "displaced_beneficiaries"] if "financing" in table.columns else table.iloc[:0]
    return dict(cash_bn=float(cash.responsive_bn.sum()), cash_federal_bn=float(cash.federal_bn.sum()),
                resource_cost_bn=float(capital.responsive_bn.sum()),
                resource_cost_federal_bn=float(capital.federal_bn.sum()),
                displaced_bn=float(displaced.responsive_bn.sum()), displaced_federal_bn=float(displaced.federal_bn.sum()))


# ---------------------------------------------------------------- September 24: the corrections by government

def cell_net(edits: list[dict]) -> dict[tuple, dict]:
    """Edits netted per engine cell: (side, line, scenario or key) -> {personal, shared}."""
    net = {}
    for e in edits:
        cell = (e["side"], e["line"], e["scenario"] if e["side"] == "receipt" else e["key"])
        cur = net.setdefault(cell, {"personal": 0.0, "shared": 0.0})
        for a in ("personal", "shared"):
            cur[a] += e["by"][a]
    return net


def sept26_components(payload24: dict, payload26: dict) -> dict:
    """The September 26 payload by component.

    The September 24 components (package_components.json) carry over. The two new corrections are the
    cell differences between the September 26 and September 24 payloads:
      finite_removal   audit row 8's constant times (row8_factor - 1), on the constant line; it enters
                       the constant line's parts as row8_finite and splits as row 8 does;
      consumption_key  every other cell that moved, taken from the consumption-key lane's edits for the
                       spec the payload names.
    Gates: the September 24 components sum to the September 24 payload, the constant line moved by
    exactly the row-8 change, and the consumption-key edits equal the other cell differences (1e-9)."""
    comp = json.loads(COMPONENTS_FILE.read_text())
    n24, n26, parts = cell_net(payload24["edits"]), cell_net(payload26["edits"]), cell_net(comp["edits"])
    gap = max(abs(parts.get(c, {}).get(a, 0.0) - n24.get(c, {}).get(a, 0.0)) for c in set(parts) | set(n24)
              for a in ("personal", "shared"))
    if gap > 1e-9:
        raise SystemExit(f"[BLOCKED] the September 24 components do not sum to its payload ({gap:.2e})")
    factor = payload26["meta"]["responses"]["row8_factor"]
    row8 = {a: comp["constants"]["row8"]["by"][a] * (factor - 1) for a in ("personal", "shared")}
    diff = {c: {a: n26.get(c, {}).get(a, 0.0) - n24.get(c, {}).get(a, 0.0) for a in ("personal", "shared")}
            for c in set(n24) | set(n26)}
    constant = ("spending", "lane_constants", "k")
    if max(abs(diff[constant][a] - row8[a]) for a in row8) > 1e-12:
        raise SystemExit("[BLOCKED] the constant line did not move by audit row 8's finite-removal change")
    match = re.fullmatch(r".*; consumption key (\S+)", payload26["meta"]["case"])
    if match is None:
        raise SystemExit("[BLOCKED] the September 26 payload names no consumption-key spec")
    ck = json.loads(CK_PAYLOADS.read_text())
    if ck["meta"]["composes_with"] != "main_case_2026_09_24/derived/corrections.json":
        raise SystemExit("[BLOCKED] the consumption-key edits do not compose with the September 24 payload")
    ck_edits = ck["specs"][match.group(1)]["edits"]
    ck_net = cell_net(ck_edits)
    moved = {c for c, v in diff.items() if c != constant and any(abs(x) > 1e-12 for x in v.values())}
    gap = max(abs(diff[c][a] - ck_net.get(c, {}).get(a, 0.0)) for c in moved | set(ck_net) for a in ("personal", "shared"))
    if gap > 1e-9 or not moved <= set(ck_net):
        raise SystemExit(f"[BLOCKED] the consumption-key edits are not the payload's other changes ({gap:.2e})")
    edits = comp["edits"] + [dict(component="consumption_key", **e) for e in ck_edits] + [
        dict(component="finite_removal", side="spending", line="lane_constants", key="k", by=row8)]
    constants = dict(comp["constants"], row8_finite=dict(
        label="finite removal: audit row 8's increment times (row8_factor - 1)", by=row8))
    return dict(meta=dict(comp["meta"], consumption_key_spec=match.group(1), row8_factor=factor),
                constants=constants, edits=edits)


def two_tables(path: Path) -> tuple[pd.DataFrame, pd.DataFrame]:
    """account_keying_parts.csv holds two CSV tables separated by a blank line."""
    first, second = path.read_text().strip().split("\n\n")
    return pd.read_csv(io.StringIO(first)), pd.read_csv(io.StringIO(second))


def constant_parts(corner: dict, conv: str, shares: dict, extras: dict, base_share: float) -> list[dict]:
    """The constant correction line's parts at one corner: amount ($bn, the corner's allocation), the
    federal share by year, and the account line whose national series carries it back (None: group size).

    row 8   unallocable state-local general public services (audit spending.md #7): federal only
            through grants, at their share of state-local general-government spending; 0 under the
            low convention, which counts such grants as state-local.
    row 9   the MEPS donor filter dropped 3.0% of Medicare and 3.7% of Medicaid dollars (spending.md
            #4): split by those shares of the group's two lines [INFERENCE: the audit gives no split].
    row 10  foster care and adoption in BEA 3.12 line 39, the "Other" state welfare line.
    small   origin allocation, grants, top-codes, flags: at the corner's own 2024 federal share.
    shelter mapping A's four parts (account_keying_parts.csv) at the general-government response the
            package priced them at (shared 0.59, personal 0.84), each at its line's federal share.
    care    hours taxes and the output term's receipts at the labour-tax federal share, the elder-care
            Medicaid saving at Medicaid's; the package's -4.15 in proportion to the lane's channels.
    row8_finite  (September 26) row 8's increment times (row8_factor - 1): split and carried as row 8.
    """
    comp = COMPONENTS["constants"]
    a, phi = corner["allocation"], shares[conv]
    const = lambda v: pd.Series(float(v), index=phi.index)
    lines = {l["id"]: l for l in MODEL["spending"]["lines"]}
    target = lambda i: lines[i]["keys"][lines[i]["preferred_key"]][a]["target_bn"]
    parts = [dict(part="row8", sub="state_local_general_public_services", amount=comp["row8"]["by"][a],
                  share=const(0.0) if conv == "low" else extras["sl_gps_grant_share"], carry="general_public_services")]
    if "row8_finite" in comp:
        parts.append(dict(parts[0], part="row8_finite", component="finite_removal:row8",
                          amount=comp["row8_finite"]["by"][a]))
    mcr, mcd = 0.030 * target("medicare"), 0.037 * target(MEDICAID)
    for line, w in (("medicare", mcr / (mcr + mcd)), (MEDICAID, mcd / (mcr + mcd))):
        parts.append(dict(part="row9", sub=line, amount=comp["row9"]["by"][a] * w, share=phi[line], carry=line))
    parts.append(dict(part="row10", sub="other_state_welfare", amount=comp["row10"]["by"][a],
                      share=phi["other_state_welfare"], carry="other_state_welfare"))
    parts.append(dict(part="small", sub="corner_average", amount=comp["small"]["by"][a], share=const(base_share),
                      carry=None))
    weights, keyshare = two_tables(SHELTER_PARTS)
    keying = pd.read_csv(SHELTER_KEYING)
    end_used = "low" if a == "shared" else "high"          # the September 23 responses the package priced
    gg_used = INPUTS["general_government_response"][end_used]
    row = keying[(keying.outlays_case == "central") & (keying.mapping == "A_nyc_codes_consumption")
                 & (keying.served_case == "nyc_jun2025") & np.isclose(keying.general_govt_response, gg_used)]
    if len(row) != 1:
        raise SystemExit("[BLOCKED] shelter keying row not unique")
    row = row.iloc[0]
    ks = keyshare.set_index("category").target_share_national
    pieces = {}
    for w in weights.itertuples():
        line = w.A_nyc_codes_consumption_category
        resp = gg_used if line == "general_public_services" else 1.0
        pieces[line] = pieces.get(line, 0.0) + row.cy2024_outlays_musd * w.weight * resp * (ks[line] - row.served_share)
    if abs(sum(pieces.values()) - row.overcharge_musd) > 0.1 or abs(row.overcharge_musd / 1e3 + comp["shelter"]["by"][a]) > 1e-9:
        raise SystemExit("[BLOCKED] shelter parts do not rebuild the lane's overcharge or the package's figure")
    gps_lo, gps_hi = extras["gps"][conv]
    for line, v in pieces.items():
        share = (gps_lo if end_used == "low" else gps_hi) if line == "general_public_services" else phi[line]
        parts.append(dict(part="shelter", sub=line, amount=comp["shelter"]["by"][a] * v / sum(pieces.values()),
                          share=share, carry=line))
    care = pd.read_csv(CARE_SUMMARY)
    pick = lambda text: float(care.loc[care.channel.str.startswith(text), "central_bn"].iloc[0])
    channels = {"hours_taxes": pick("taxes on native women"), "output_receipts": pick("output gain"),
                "elder_care_medicaid": pick("elder care")}
    if abs(sum(channels.values()) - pick("TOTAL")) > 1e-9:
        raise SystemExit("[BLOCKED] care channels do not add to the lane's total")
    for name, v in channels.items():
        medicaid = name == "elder_care_medicaid"
        parts.append(dict(part="care", sub=name, amount=comp["care"]["by"][a] * v / sum(channels.values()),
                          share=phi[MEDICAID] if medicaid else extras["labour_share"], carry=MEDICAID if medicaid else None))
    return parts


def correction_split(corner: dict, shares: pd.DataFrame, extras: dict, conv: str, year: int,
                     parts: list, edits: list | None = None) -> pd.DataFrame:
    """Each correction's effect on the gap at one corner, split by the government level of its line.

    Effect = the line's response at the corner x the edit in the evaluated cell (receipts: the
    reference incidence rule; spending: the key the frame evaluates). The share is the one
    split_corner() applies to that line, so the parts add to the change in the whole split. The edits are
    COMPONENTS', or the case's (September 29: with the parts its payload adds, v4_components)."""
    t = lines_at(corner).set_index("id")
    model, keys, a = corner["model"], corner["keys"], corner["allocation"]
    phi = shares.loc[year]
    evaluated = {l["id"]: keys.get(l["id"], l["preferred_key"]) for l in model["spending"]["lines"]}
    rows = []
    for e in (COMPONENTS["edits"] if edits is None else edits):
        if e["side"] == "receipt":
            if e["scenario"] != model["receipts"]["reference"]:
                continue
            resp = t.loc[t.side == "receipt", "response"][e["line"]]
            sign = -1.0
        else:
            if e["key"] != evaluated[e["line"]]:
                continue
            resp = t.loc[t.side == "spending", "response"][e["line"]]
            sign = 1.0
        effect = sign * resp * e["by"][a]
        if effect == 0:
            continue
        line = e["line"]
        if e["side"] == "spending" and line in LONG_RUN_LINES and "subfunction_rows" in corner:
            share = long_run_fraction(corner, line, resp, conv, extras)[year]
        elif line == "general_public_services":
            lo, hi = extras["gps"][conv]
            share = lo[year] if corner["gg_end"] == "low" else hi[year]
        elif line == "education_services" and conv == "high":
            school = corner["school_share"] * corner["school_response"] / resp
            share = school * phi["_school_high"] + (1 - school) * phi["education_services"]
        elif line == "school_reprice":
            share = phi["_school_high"] if conv == "high" else phi["education_services"]
        elif line == "college_rekey":
            share = phi["education_services"]
        elif line == "lane_constants":
            continue                                   # its parts follow
        elif line == ENTERPRISE_RECEIPT and "_enterprise_federal_bn" in phi.index:
            # September 29: the line's federal part is its key times t32(23). A cell edit moves the key on the line as
            # the model has it (v4_components gates that every cell edit precedes the scale edit); the national-scale
            # edit removes public housing's state-local deficit and moves no federal dollars.
            share = 0.0 if e.get("scale") else phi["_enterprise_federal_bn"] / next(
                x for x in MODEL["receipts"]["lines"] if x["id"] == line)["national_bn"]
        else:
            share = phi[line]
        rows.append(dict(component=e["component"], side=e["side"], line=line,
                         cell=e["scenario"] if e["side"] == "receipt" else e["key"],
                         effect_bn=effect, federal_bn=effect * share,
                         capped=line in corner.get("capped", ())))
    for p in parts:
        rows.append(dict(component=p.get("component", f"lane_constants:{p['part']}"), side="spending", line=p["sub"],
                         cell="k", effect_bn=p["amount"], federal_bn=p["amount"] * p["share"][year], capped=False))
    out = pd.DataFrame(rows)
    out["state_local_bn"] = out.effect_bn - out.federal_bn
    if "capped" in corner:              # an edit on a capped program's line moves the displaced beneficiaries
        out["financing"] = np.where(out.capped, "displaced_beneficiaries", "cash")
    return out.drop(columns="capped")


# ---------------------------------------------------------------- back-cast machinery

class History:
    """Measured series by year, as the back-cast uses them."""

    def __init__(self, wb: Workbook):
        raw1 = pd.ExcelFile(BEA / "Section1All_xls.xlsx").parse("T10109-A", header=None)
        self.price = self._series(raw1, "Gross domestic product")
        raw7 = pd.ExcelFile(BACKCAST / "_cache/Section7All_xls.xlsx").parse("T70100-A", header=None)
        self.people = self._series(raw7, "Population (midperiod, thousands)")
        annual = pd.read_csv(BACKCAST / "derived/backcast_annual.csv").set_index("year")
        self.annual = annual
        self.group = annual.group_millions.reindex(YEARS)
        self.income = (annual.relative_per_capita_income / annual.relative_per_capita_income[LAST]).reindex(YEARS)
        self.real = self.price[LAST] / self.price.reindex(YEARS)
        share = self.group / (self.people.reindex(YEARS) / 1e3)
        self.share = share / share[LAST]
        self.wb = wb
        if abs(self.group[LAST] - TARGET_M) > 1e-3:
            raise SystemExit("[BLOCKED] back-cast group count does not end at the account's target")

    @staticmethod
    def _series(table: pd.DataFrame, label: str) -> pd.Series:
        header = table.index[table.iloc[:, 0].astype(str).str.strip().eq("Line")][0]
        match = table[table.iloc[:, 1].astype(str).str.strip().eq(label)]
        years = [int(float(v)) for v in table.iloc[header, 3:]]
        return pd.Series(match.iloc[0, 3:].astype(float).to_numpy(), index=years)

    def index(self, reference: str, signed: bool = False) -> pd.Series:
        """Real national total of a BEA cell set, 2024 = 1 (backcast_categories.py `index`). A signed
        series (the enterprise surplus, negative in 2024 and positive for the federal enterprises in some
        years) needs only a nonzero 2024 value; its index is negative in the years its sign differs."""
        nominal = self.wb.cells(reference)
        if (nominal[LAST] == 0) if signed else (nominal[LAST] <= 0):
            raise SystemExit(f"[BLOCKED] {reference} has no {'nonzero' if signed else 'positive'} 2024 value")
        return nominal * self.real / nominal[LAST]

    def nominal(self, real: pd.Series) -> pd.Series:
        return real / self.real


RECEIPT_GROUPS = {3: ["federal_income_tax", "state_local_income_tax", "personal_motor_vehicle", "other_personal_tax",
                      "personal_property_tax"],
                  8: ["employee_oasdi", "employee_hi", "self_employment_oasdi_hi", "employer_oasdi", "employer_hi",
                      "medicare_supplementary_premiums", "other_domestic_social_contributions"],
                  4: ["general_sales_tax", "excise_selective_sales", "customs_duties", "modeled_owner_property",
                      "tenant_occupied_property"],
                  17: ["personal_current_transfers"]}
# The property taxes respond from September 29 on (the long-run property-tax item); a line a case's model lacks, or
# holds at zero response, adds nothing to its group.


def grouped(rec: pd.Series, names: list[str]) -> float:
    """The responsive amounts of a Table 3.1 group's receipt lines ($bn); lines the model lacks count as zero."""
    return rec.reindex(names, fill_value=0.0).sum()
# Own-government series for each direct receipt line: (federal cells, state-local cells).
RECEIPT_SERIES = {
    "federal_income_tax": ("T30400-A:3", None), "state_local_income_tax": (None, "T30400-A:9"),
    "personal_motor_vehicle": (None, "T30400-A:10"), "other_personal_tax": (None, "T30400-A:12"),
    "employee_oasdi": ("T30600-A:24", None), "employee_hi": ("T30600-A:25", None),
    "self_employment_oasdi_hi": ("T30600-A:26", None), "employer_oasdi": ("T30600-A:5", None),
    "employer_hi": ("T30600-A:6", None), "medicare_supplementary_premiums": ("T30600-A:27", None),
    "other_domestic_social_contributions": ("T30600-A:7;T30600-A:12;T30600-A:13;T30600-A:14;T30600-A:15;"
                                            "T30600-A:16;T30600-A:28;T30600-A:29;T30600-A:30",
                                            "T30600-A:17;T30600-A:31"),
    "general_sales_tax": (None, "T30500-A:20"), "excise_selective_sales": ("T30500-A:4", "T30500-A:23"),
    "customs_duties": ("T30500-A:15", None), "personal_current_transfers": ("T30200-A:21", "T30300-A:20"),
    "enterprise_surplus": ("T30200-A:23", "T30300-A:22")}
# Receipt lines whose national series is not positive in 2024, with the Table 3.1 line that carries them
# in the September 20 grouped-receipt audit (they respond from September 27 on).
SIGNED_RECEIPTS = {"enterprise_surplus": 19}
# September 29: the property taxes carry the state-local series of their tax (NIPA 3.3 line 9, 3.4 line 11); the
# enterprise surplus without public housing carries the state-local enterprises less housing and urban renewal
# (NIPA 3.8 lines 8-12, 14, 15) and the federal enterprises (3.2 line 23); public housing's line, when it is not
# capped (the alternative), its deficit (3.8 line 13) and its federal operating subsidy with federal housing
# subsidies (3.13 line 4). Earlier cases keep RECEIPT_SERIES.
RECEIPT_SERIES_V4 = dict(RECEIPT_SERIES, modeled_owner_property=(None, "T30300-A:9"),
                         tenant_occupied_property=(None, "T30300-A:9"), personal_property_tax=(None, "T30400-A:11"),
                         enterprise_surplus=("T30200-A:23", "T30800-A:8;T30800-A:9;T30800-A:10;T30800-A:11;"
                                                            "T30800-A:12;T30800-A:14;T30800-A:15"),
                         housing_enterprise_surplus=("T31300-A:4", "T30800-A:13"))
SIGNED_RECEIPTS_V4 = dict(SIGNED_RECEIPTS, housing_enterprise_surplus=19)


def programme_control(hist: History) -> float:
    """Reproduce backcast_categories_annual.csv (September 20 anchors) with this lane's machinery."""
    categories = pd.read_csv(FISCAL / "full_account_spending_2026_09_20/derived/categories.csv").set_index("category")
    cases = pd.read_csv(FISCAL / "full_account_2026_09_20/derived/service_response_cases.csv")
    published = pd.read_csv(BACKCAST / "derived/backcast_categories_annual.csv")
    worst = 0.0
    for name, profile, case_id, normalization in (("cbo_informed_low", MAIN, "shared_9", "gdp"),
                                                   ("cbo_informed_high", MAIN, "personal_6", "cash")):
        case = cases[(cases.profile == profile) & (cases.case_id == case_id) &
                     (cases.normalization == normalization)].iloc[0]
        corner = dict(allocation=case.allocation, normalization=normalization, school_share=case.school_share,
                      school_response=case.school_response, other_edu=case.other_education_response,
                      delayed=case.delayed_response, gg=0.0, justice=0.0, uc=0.0, shift={})
        if abs(welfare(corner) - case.welfare_bn) > 1e-6:
            raise SystemExit(f"[BLOCKED] control corner {name} does not reproduce its welfare")
        t = lines_at(corner).set_index("id")
        spend = t[(t.side == "spending") & (t.responsive_bn != 0)]
        transfers = sum(spend.responsive_bn[i] * hist.index(categories.loc[i, "source_cells"]) * hist.share
                        for i in spend.index if categories.loc[i, "family"] == "social_benefits")
        services = sum(spend.responsive_bn[i] * hist.index(categories.loc[i, "source_cells"]) * hist.share
                       for i in spend.index if categories.loc[i, "family"] == "consumption")
        rec = t[(t.side == "receipt") & (t.responsive_bn != 0)]
        receipts = sum(grouped(rec.responsive_bn, names) * hist.index(f"T30100-A:{line}") * hist.share
                       for line, names in RECEIPT_GROUPS.items())
        p, f = production(normalization)
        production_t = (p + f) * hist.group / hist.group[LAST]
        for rule, scale in (("programme", 1.0), ("income", hist.income)):
            net = transfers + services - receipts * scale - production_t
            want = published[(published["case"] == name) & (published.rule == rule)].set_index("year").net_cost_bn
            worst = max(worst, float((net - want.reindex(YEARS)).abs().max()))
    if worst > 6e-4:
        raise SystemExit(f"[BLOCKED] programme back-cast control differs from the lane by {worst:.4f}bn")
    return worst


def programme_federal(hist: History, corner: dict, end: str, conv: str, shares: dict, extras: dict,
                      jf: dict, ucf: dict, parts: list | None = None, series: dict | None = None,
                      signed_receipts: dict | None = None) -> pd.DataFrame:
    """Programme rule on the adopted anchor, split by government, real 2024 $bn by year.

    Spending lines carry their own BEA cells (categories.csv) and each year's federal share; receipts
    carry their own federal or state-local series; induced receipts F scale with the group. P is excluded.
    September 24 correction lines: the school and college parts carry with the education line; each part
    of the constant line carries with the line it corrects, or with the group's size where it has none.
    September 27: the capped programs are left out (no budget response; nothing is borrowed for them), the
    long-run lines take their subfunctions' federal fraction by year, and the enterprise surplus receipt
    carries each level with its own series. It follows the group's population share, not its income, so
    the income rule does not scale it (as in the back-cast).
    September 29: the synthetic lines carry with their parent lines (SYNTHETIC_CARRY) at their own federal
    share by year (v4_shares), the receipts with the case's series (RECEIPT_SERIES_V4, SIGNED_RECEIPTS_V4), and a
    capped receipt line (public housing's) is left out like the capped spending lines.
    """
    series = RECEIPT_SERIES if series is None else series
    signed_receipts = SIGNED_RECEIPTS if signed_receipts is None else signed_receipts
    categories = pd.read_csv(FISCAL / "full_account_spending_2026_09_20/derived/categories.csv").set_index("category")
    phi = shares[conv]
    t = lines_at(corner).set_index("id")
    zero = pd.Series(0.0, index=YEARS)
    spending, spending_fed, receipts, receipts_fed = zero.copy(), zero.copy(), zero.copy(), zero.copy()
    for i in t.index[(t.side == "spending") & (t.responsive_bn != 0)]:
        amount = t.responsive_bn[i]
        if i in corner.get("capped", ()):
            continue
        if i == "lane_constants":
            if parts is None or abs(sum(p["amount"] for p in parts) - amount) > 1e-9:
                raise SystemExit("[BLOCKED] the constant line's parts do not add to the line")
            for p in parts:
                path = (hist.index(categories.loc[p["carry"], "source_cells"]) * hist.share if p["carry"]
                        else hist.group / hist.group[LAST])
                spending += p["amount"] * path
                spending_fed += p["amount"] * path * p["share"].reindex(YEARS)
            continue
        carried = amount * hist.index(categories.loc[SYNTHETIC_CARRY.get(i, i), "source_cells"]) * hist.share
        if i in LONG_RUN_LINES and "subfunction_rows" in corner:
            fed = carried * long_run_fraction(corner, i, t.response[i], conv, extras)
        elif i == "general_public_services":
            lo, hi = extras["gps"][conv]
            fed = carried * (lo if corner.get("gg_end", end) == "low" else hi)
        elif i == "public_order_safety":
            j = corner["justice"] * t.response[i]
            fed = carried * ((amount - j) / amount * phi[i] + jf[conv] * t.response[i] / amount)
        elif i == "medicaid_and_chip_other_medical":
            u = corner["uc"] * t.response[i]
            uc_name = corner.get("uc_arm", "equal_low" if end == "low" else "equal_high")
            fed = carried * ((amount - u) / amount * phi[i] + ucf[uc_name][conv] * t.response[i] / amount)
        elif i == "education_services" and conv == "high":
            school = t.amount_bn[i] * corner["school_share"] * corner["school_response"] / amount
            fed = carried * (school * phi["_school_high"] + (1 - school) * phi[i])
        elif i == "school_reprice":
            fed = carried * (phi["_school_high"] if conv == "high" else phi["education_services"])
        elif i == "college_rekey":
            fed = carried * phi["education_services"]
        else:
            fed = carried * phi[i]
        spending += carried
        spending_fed += fed
    population, population_fed, population_grouped = zero.copy(), zero.copy(), zero.copy()
    for i in t.index[(t.side == "receipt") & (t.responsive_bn != 0)]:
        amount = t.responsive_bn[i]
        if i in corner.get("capped", ()):
            continue
        fed_cells, sl_cells = series[i]
        share_2024 = phi.loc[LAST, i]
        signed = i in signed_receipts
        fed = amount * share_2024 * hist.index(fed_cells, signed) * hist.share if fed_cells else zero
        sl = amount * (1 - share_2024) * hist.index(sl_cells, signed) * hist.share if sl_cells else zero
        if signed:                      # population-keyed: never scaled by relative income
            population += fed + sl
            population_fed += fed
            population_grouped += amount * hist.index(f"T30100-A:{signed_receipts[i]}", True) * hist.share
            continue
        receipts += fed + sl
        receipts_fed += fed
    # Sensitivity: the 2020-2022 refundable-credit excess over the 2019-2023 line goes per head (the
    # pandemic payments were close to uniform per person) instead of at the group's 2024 credit key.
    rtc = "refundable_tax_credits"
    idx = hist.index(categories.loc[rtc, "source_cells"])
    trend = idx.copy()
    for y in (2020, 2021, 2022):
        trend[y] = idx[2019] + (idx[2023] - idx[2019]) * (y - 2019) / 4
    key = t.amount_bn[rtc] / t.national_bn[rtc]
    rtc_excess = t.responsive_bn[rtc] * (idx - trend) * hist.share * (1 - TARGET_M / RESIDENTS_M / key)
    # Audit: the September 20 method carries receipts by Table 3.1 group, not by own-government series.
    rec = t[t.side == "receipt"]
    rec = rec[~rec.index.isin(corner.get("capped", ()))]
    receipts_grouped = sum(grouped(rec.responsive_bn, names) * hist.index(f"T30100-A:{line}") * hist.share
                           for line, names in RECEIPT_GROUPS.items())
    p, f = production(corner["normalization"], corner.get("model"))
    induced = f * hist.group / hist.group[LAST]
    out = pd.DataFrame(dict(spending=spending, spending_fed=spending_fed, receipts=receipts,
                            receipts_fed=receipts_fed, induced=induced, induced_fed=induced * phi["_induced_receipts"],
                            receipts_grouped=receipts_grouped, rtc_excess=rtc_excess,
                            rtc_excess_fed=rtc_excess * phi[rtc], population=population,
                            population_fed=population_fed, population_grouped=population_grouped))
    for rule, scale in (("programme", 1.0), ("income", hist.income)):
        out[f"gap_{rule}"] = out.spending - out.receipts * scale - out.population - out.induced
        out[f"federal_{rule}"] = out.spending_fed - out.receipts_fed * scale - out.population_fed - out.induced_fed
        out[f"gap_{rule}_grouped"] = out.spending - out.receipts_grouped * scale - out.population_grouped - out.induced
    out.attrs["rtc_key_share"] = float(key)
    return out


def ex_pandemic(series: pd.Series) -> pd.Series:
    out = series.copy()
    out[[2020, 2021]] = (series[2019] + series[2022]) / 2
    return out


def indirect_receipt_shares(wb: Workbook) -> pd.Series:
    """Federal share of the receipt lines with zero direct response (used only by the federal-series rule)."""
    t31 = lambda n: wb.line("T30100-A", n)[LAST]
    t32 = lambda n: wb.line("T30200-A", n)[LAST]
    corporate = t32(8) / t31(5)
    return pd.Series({"corporate_capital": corporate, "corporate_labor": corporate, "personal_property_tax": 0.0,
                      "modeled_owner_property": 0.0, "remaining_production_property": 0.0,
                      "other_production_taxes": wb.line("T30500-A", 17)[LAST] / 145.258,
                      "government_asset_income": t32(13) / t31(10), "business_current_transfers": t32(20) / t31(16),
                      "enterprise_surplus": t32(23) / t31(19), "rest_world_tax_contributions": 0.0,
                      "rest_world_current_transfers": 0.0, "source_rounding": 0.0})


# ---------------------------------------------------------------- rates and stocks

def rate_paths() -> pd.DataFrame:
    interest, debt, gs10 = omb_net_interest(), omb_debt_held_by_public(), gs10_fiscal_years()
    securities = omb_interest_on_public_securities()
    fy = list(range(2005, 2026))
    average = pd.Series({s: (debt[s - 1] + debt[s]) / 2 for s in fy})
    return pd.DataFrame(dict(effective=interest.reindex(fy) / average,
                             constant_3_22=pd.Series(LADDER137_RATE, index=fy),
                             treasury_10y=gs10.reindex(fy),
                             gross_public_securities=securities.reindex(fy) / average,
                             net_interest_bn=interest.reindex(fy),
                             interest_on_public_securities_bn=securities.reindex(fy),
                             debt_held_by_public_bn=debt.reindex(fy)))


def proposed_benefits(labour_share: float, medicaid_share: float, include_care: bool = True) -> dict:
    """Federal part of the fiscal benefits the symmetry lanes priced but the adopted case omits ($bn, 2024).

    Care lane: taxes on native women's extra hours, the output term's receipts, and the elder-care
    Medicaid saving; mobility lane: the tax on today's net earnings change; scale lane (proposed, not
    adopted): induced receipts on the joint scale-and-schooling net. Taxes are split at the account's
    induced-receipt federal share, the Medicaid saving at the Medicaid line's federal share.
    With include_care False (the September 24 case, which carries care inside the account) the care
    channels are reported but left out of the omitted totals, which would otherwise count them twice.
    """
    care = pd.read_csv(FISCAL / "care_household_services_2026_09_23/derived/summary.csv")
    pick = lambda text: float(care.loc[care.channel.str.startswith(text), "central_bn"].iloc[0])
    taxes, output, elder = pick("taxes on native women"), pick("output gain"), pick("elder care")
    if abs(taxes + output + elder - float(care.loc[care.channel.str.startswith("TOTAL"), "central_bn"].iloc[0])) > 1e-9:
        raise SystemExit("[BLOCKED] care lane channels do not sum to its total")
    mobility = json.loads((FISCAL / "labor_mobility_insurance_2026_09_23/derived/insurance_summary.json").read_text())
    mobility_tax = (mobility["ck_era_central_components_bn"]["fiscal_net_bn"]
                    * mobility["present_day"]["factor_central"])
    scale = pd.read_csv(FISCAL / "scale_spillovers_2026_09_23/derived/summary.csv")
    joint = scale[(scale.table == "joint_grid") & (scale.geography == "CZ 1990")].iloc[0]
    care_taxes, care_elder = (taxes + output, elder) if include_care else (0.0, 0.0)
    omitted = labour_share * (care_taxes + mobility_tax) + medicaid_share * care_elder
    with_scale = omitted + labour_share * float(joint.induced_receipts_bn)
    sources = [FISCAL / "care_household_services_2026_09_23/derived/summary.csv",
               FISCAL / "labor_mobility_insurance_2026_09_23/derived/insurance_summary.json",
               FISCAL / "scale_spillovers_2026_09_23/derived/summary.csv"]
    out = dict(care_taxes_bn=taxes, care_output_receipts_bn=output, care_elder_medicaid_bn=elder,
               mobility_tax_bn=mobility_tax, scale_induced_receipts_bn=float(joint.induced_receipts_bn),
               federal_omitted_bn=omitted, federal_with_scale_bn=with_scale,
               total_omitted_bn=care_taxes + care_elder + mobility_tax,
               total_with_scale_bn=care_taxes + care_elder + mobility_tax + float(joint.induced_receipts_bn),
               source_sha256={str(p.relative_to(ROOT)): sha(p) for p in sources})
    if not include_care:
        out["care_inside_account"] = True
    return out


def stock(federal_nominal: pd.Series, rates: pd.Series, start: int, borrowed: float) -> dict:
    """Debt entering 2024 from the gaps of start..2023 (borrowed at year end, interest from the next year)."""
    flows = federal_nominal * borrowed
    d_start = 0.0
    for t in range(start, LAST):
        d_start += flows[t] * float(np.prod([1 + rates[s] for s in range(t + 1, LAST)]))
    r = float(rates[LAST])
    return dict(stock_entering_2024_bn=d_start, legacy_interest_2024_bn=r * d_start,
                stock_end_2024_brief_bn=d_start * (1 + r), flow_2024_bn=float(flows[LAST]),
                flow_2024_part_year_interest_bn=float(flows[LAST]) * r / 2,
                sum_flows_nominal_bn=float(flows.loc[start:LAST - 1].sum()), rate_2024=r)


# ---------------------------------------------------------------- main

def sept26_bridge(anchors26: dict, shares: dict, extras26: dict, extras24: dict, jf: dict, ucf: dict,
                  corrections: pd.DataFrame, main26: dict, split26: pd.DataFrame) -> pd.DataFrame:
    """The 2024 split from the September 24 case to the September 26 one, main profile, each band end.

    Steps: the finite-removal responses on the September 24 model (general government, with its
    low-end federal fraction recomposed, and schools), then the payload's two new corrections at the
    adopted responses (audit row 8's change and the consumption key, from `corrections`). Gates: the
    September 26 corners are the September 24 ones with the responses replaced; the September 24 step
    reproduces that case's band; the responses step moves the gap by main_case_2026_09_26's own
    general-government (net of row 8) and school changes (1e-6); the steps add to the September 26
    split (1e-9)."""
    corrected24 = apply_corrections(MODEL, json.loads(CORRECTIONS_FILE.read_text()))
    main24 = json.loads(MAIN24_SUMMARY.read_text())
    anchors24 = sept24_anchors(MAIN, corrected24, main24)
    row8 = COMPONENTS["constants"]["row8_finite"]["by"]["shared"]
    ch = main26["changes"]
    responses_change = {"low": ch["general_government"][0] - row8 + ch["schools"][0],
                        "high": ch["general_government"][1] - row8 + ch["schools"][1]}
    keep = ("allocation", "normalization", "school_share", "uc_key", "gg_end")
    rows = []
    for end in ("low", "high"):
        c24, c26 = anchors24[end], anchors26[end]
        if any(c24[k] != c26[k] for k in keep):
            raise SystemExit(f"[BLOCKED] the September 26 {end} corner is not the September 24 one")
        c24r = dict(c26, model=corrected24)       # September 24 model at the adopted responses
        for conv in CONVENTIONS:
            def split_at(corner, extras):
                before = split_corner(dict(corner, model=MODEL), shares[conv], extras, conv, LAST, jf, ucf, end)
                parts = [p for p in constant_parts(corner, conv, shares, extras,
                                                   before.federal_bn.sum() / before.responsive_bn.sum())
                         if p["part"] != "row8_finite"]
                t = split_corner(corner, shares[conv], extras, conv, LAST, jf, ucf, end, parts)
                return t.responsive_bn.sum(), t.federal_bn.sum()
            g24, f24 = split_at(c24, extras24)
            p, _ = production(c24["normalization"])
            if abs(g24 - (main24["main_case"][0 if end == "low" else 1] + p)) > 1e-6:
                raise SystemExit(f"[BLOCKED] the September 24 {end} split does not reproduce its band")
            g24r, f24r = split_at(c24r, extras26)
            if abs(g24r - g24 - responses_change[end]) > 1e-6:
                raise SystemExit(f"[BLOCKED] {end}/{conv}: the responses move the gap by {g24r - g24:.6f}, "
                                 f"main_case_2026_09_26 by {responses_change[end]:.6f}")
            cs = corrections[(corrections.end == end) & (corrections.convention == conv)]
            steps = [("sept24_case", g24, f24), ("finite_removal_responses", g24r - g24, f24r - f24)]
            for name in ("finite_removal", "consumption_key"):
                part = cs[cs.component.str.split(":").str[0] == name]
                steps.append((f"{name}_row8" if name == "finite_removal" else name,
                              part.effect_bn.sum(), part.federal_bn.sum()))
            total = sum(s[1] for s in steps), sum(s[2] for s in steps)
            got = split26[(split26.profile == MAIN) & (split26.end == end) & (split26.convention == conv)].iloc[0]
            if abs(total[0] - got.fiscal_gap_bn) > 1e-9 or abs(total[1] - got.federal_bn) > 1e-9:
                raise SystemExit(f"[BLOCKED] {end}/{conv}: the steps add to {total}, the September 26 split is "
                                 f"{got.fiscal_gap_bn:.6f} ({got.federal_bn:.6f})")
            steps.append(("sept26_case", got.fiscal_gap_bn, got.federal_bn))
            rows += [dict(end=end, convention=conv, step=s, gap_bn=g, federal_bn=f, state_local_bn=g - f)
                     for s, g, f in steps]
    return pd.DataFrame(rows)


def finite_components(responses: dict) -> tuple[float, float]:
    """Federal tax collection's and state-local general government's finite-removal responses,
    r = [1 - (1 - s)^b] / s at the payload's group share s. Gates: their elasticities are the 0.789 and
    0.842 this lane composes with, and with the finite-removal lane's weights they compose to the
    adopted low and high general-government responses (1e-12)."""
    rv = json.loads(R_VALUES.read_text())
    gg = responses["general_government"]
    s = gg["s"]
    r = lambda b: (1 - (1 - s) ** b) / s  # noqa: E731
    r_tax, r_sl = r(rv["b_fin"]), r(rv["b_admin"])
    low = (rv["state_local_bn"] * r_sl + rv["federal_tax_bn"] * r_tax) / rv["total_bn"]
    if (rv["b_fin"], rv["b_admin"]) != (0.789, 0.842) or abs(low - gg["low"]) > 1e-12 or abs(r_sl - gg["high"]) > 1e-12:
        raise SystemExit("[BLOCKED] the components' finite-removal responses do not compose to the adopted ones")
    return r_tax, r_sl


def case_file(case: str, name: str) -> Path:
    return FISCAL / LATER_CASES[case][0] / "derived" / name


def payload_file(case: str, which: str = "set") -> Path:
    """A later case's payload file: corrections.json, or from September 29 the set or the cash set (Case.payloads)."""
    paths = LATER_CASES[case].payloads
    return FISCAL / paths[which] if paths else case_file(case, "corrections.json")


def case_payload(case: str, which: str = "set") -> dict:
    """A later case's corrections payload. Gates: its responses are its lane's summary.json responses, and
    its lines and edits are the first later case's (September 26), so later cases differ by responses,
    except the enterprise receipt's re-key edits a case records in meta.enterprise_receipt_rekey
    (rekey_edits), which follow them. A case with two payloads (September 29) is gated by v4_parts instead:
    the previous case's payload comes first, unchanged; and its set is the candidate's (SEPT29["candidate_set"])
    in everything but the adoption's meta stamps."""
    payload = json.loads(payload_file(case, which).read_text())
    if LATER_CASES[case].payloads:
        v4_parts(case, payload)
        if which == "set" and SEPT29.get("candidate_set"):
            strip = lambda p: dict(p, meta={k: v for k, v in p["meta"].items() if k not in SEPT29["stamps"]})  # noqa: E731
            candidate = json.loads((FISCAL / SEPT29["candidate_set"]).read_text())
            if strip(payload) != strip(candidate) or not payload["meta"].get("adopted"):
                raise SystemExit(f"[BLOCKED] {payload_file(case).name} is not {SEPT29['candidate_set']} with the "
                                 f"adoption's stamps {SEPT29['stamps']}")
        return payload
    if payload["meta"]["responses"] != json.loads(case_file(case, "summary.json").read_text())["responses"]:
        raise SystemExit(f"[BLOCKED] the payload's responses differ from {LATER_CASES[case][0]} summary.json")
    first = json.loads(case_file(next(iter(LATER_CASES)), "corrections.json").read_text())
    n = len(payload["edits"]) - len(rekey_edits(payload, first))
    if (payload["lines"], payload["edits"][:n]) != (first["lines"], first["edits"]):
        raise SystemExit(f"[BLOCKED] {LATER_CASES[case][0]}'s edits differ from September 26's; only responses may")
    return payload


def previous_case(case: str) -> str:
    names = list(LATER_CASES)
    return names[names.index(case) - 1]


def v4_parts(case: str, payload: dict) -> dict:
    """The parts a September 29 payload adds to the previous case's (engine.js's three optional parts, and the
    synthetic lines and cell edits). Gates: the previous case's lines and edits come first, unchanged; the new
    spending lines are V4_SYNTHETIC; the receipt lines are public housing's and the tenant-occupied property tax;
    every edit beyond the previous payload's is a cell edit or a national-scale edit on an executed line; the
    payload's responses are the lane's summary.json responses where the lane writes the September 27 contract."""
    prev = case_payload(previous_case(case))
    n_lines, n_edits = len(prev["lines"]), len(prev["edits"])
    if payload["lines"][:n_lines] != prev["lines"] or payload["edits"][:n_edits] != prev["edits"]:
        raise SystemExit(f"[BLOCKED] {payload_file(case).name}: the previous case's lines and edits do not come first")
    lines = [x["id"] for x in payload["lines"][n_lines:]]
    receipt_lines = sorted(x["id"] for x in payload.get("receipt_lines") or [])
    if lines != list(V4_SYNTHETIC) or receipt_lines != sorted([HOUSING_ENTERPRISE, "tenant_occupied_property"]):
        raise SystemExit(f"[BLOCKED] the September 29 payload adds lines {lines} and receipt lines {receipt_lines}")
    edits = payload["edits"][n_edits:]
    scale = [e for e in edits if "national_bn" in e]
    if any(("by" in e) == ("national_bn" in e) for e in edits) or not payload.get("production"):
        raise SystemExit("[BLOCKED] the September 29 edits are neither cell edits nor national-scale edits, or no grid")
    if SEPT29["contract"] and payload["meta"]["responses"] != json.loads(case_file(case, "summary.json").read_text())["responses"]:
        raise SystemExit(f"[BLOCKED] the payload's responses differ from {LATER_CASES[case][0]} summary.json")
    return dict(previous=prev, lines=lines, receipt_lines=receipt_lines, edits=edits, scale_edits=scale,
                counts=dict(previous_lines=n_lines, previous_edits=n_edits, edits=len(edits), scale_edits=len(scale)))


def v4_components(case: str, payload: dict) -> list[dict]:
    """The September 29 payload's parts as component edits for correction_split: each cell edit as it is; each
    receipt line as edits of its cells' whole amounts; each national-scale edit as the change it makes in every
    cell when it is applied (the amount just before it times the factor less one, replayed in the payload's
    order). The component names the items that move the line (meta.candidate_v4.items_by_line), "v4_<items>"; the
    by-component file groups on the text before ":", so a scale edit's ":scale" part joins its item.
    Gate: the components rebuild the corrected model's every cell from the previous case's (1e-9)."""
    parts = v4_parts(case, payload)
    items = payload["meta"]["candidate_v4"]["items_by_line"]
    name = lambda side, line: "v4_" + "+".join(items.get(f"{'receipts' if side == 'receipt' else 'spending'}:{line}", ["?"]))  # noqa: E731
    prev = parts["previous"]
    out = []
    for line in payload.get("receipt_lines") or []:
        for sc, cells in line["cells"].items():
            out.append(dict(component=name("receipt", line["id"]), side="receipt", line=line["id"], scenario=sc,
                            by={a: cells[a]["target_bn"] for a in ("personal", "shared")}))
    n_edits = len(prev["edits"])
    scaled = set()
    for i, e in enumerate(parts["edits"]):
        if "national_bn" not in e:
            if (e["side"], e["line"]) in scaled and e["line"] == ENTERPRISE_RECEIPT:
                raise SystemExit("[BLOCKED] a cell edit on the enterprise surplus follows its national-scale edit")
            out.append(dict(component=name(e["side"], e["line"]), **e))
            continue
        scaled.add((e["side"], e["line"]))
        before = apply_corrections(MODEL, dict(payload, edits=payload["edits"][:n_edits + i], production=None))
        line = next(x for x in before["receipts" if e["side"] == "receipt" else "spending"]["lines"] if x["id"] == e["line"])
        f = e["national_bn"] / line["national_bn"]
        cells = line["cells"] if e["side"] == "receipt" else line["keys"]
        for k, cell in cells.items():
            out.append(dict(component=name(e["side"], e["line"]) + ":scale", side=e["side"], line=e["line"],
                            **({"scenario": k} if e["side"] == "receipt" else {"key": k}),
                            by={a: cell[a]["target_bn"] * (f - 1) for a in ("personal", "shared")}, scale=True))
    if any(c["component"].startswith("v4_?") for c in out):
        raise SystemExit("[BLOCKED] a September 29 edit's line has no item in meta.candidate_v4.items_by_line")
    # Gate: the previous case's model plus the components gives the corrected model, cell by cell.
    rebuilt = apply_corrections(MODEL, prev)
    got = apply_corrections(MODEL, payload)
    target = {}
    for side, cells_of in (("receipts", "cells"), ("spending", "keys")):
        for line in rebuilt[side]["lines"]:
            for k, cell in line[cells_of].items():
                for a in ("personal", "shared"):
                    target[(side, line["id"], k, a)] = cell[a]["target_bn"]
    for c in out:
        side = "receipts" if c["side"] == "receipt" else "spending"
        k = c.get("scenario", c.get("key"))
        for a in ("personal", "shared"):
            target[(side, c["line"], k, a)] = target.get((side, c["line"], k, a), 0.0) + c["by"][a]
    worst = 0.0
    for side, cells_of in (("receipts", "cells"), ("spending", "keys")):
        for line in got[side]["lines"]:
            for k, cell in line[cells_of].items():
                for a in ("personal", "shared"):
                    worst = max(worst, abs(cell[a]["target_bn"] - target.get((side, line["id"], k, a), 0.0)))
    if worst > 1e-9:
        raise SystemExit(f"[BLOCKED] the September 29 components do not rebuild the corrected model ({worst:.2e})")
    return out


def rekey_edits(payload: dict, first: dict) -> list[dict]:
    """The enterprise receipt's re-key (September 27 on): the payload's last edits, beyond the first later
    case's. Gates: they number meta.enterprise_receipt_rekey.edits, each shifts that receipt, and the one on
    the reference incidence rule is the recorded reference edit."""
    rekey = payload["meta"].get("enterprise_receipt_rekey")
    if not rekey:
        return []
    extra = payload["edits"][len(first["edits"]):]
    if len(extra) != rekey["edits"] or any(e["side"] != "receipt" or e["line"] != rekey["line"] for e in extra):
        raise SystemExit("[BLOCKED] the payload's edits beyond September 26's are not the enterprise receipt's re-key")
    ref = [e for e in extra if e["scenario"] == MODEL["receipts"]["reference"]]
    if len(ref) != 1 or ref[0]["by"] != rekey["reference_edit_bn"]:
        raise SystemExit("[BLOCKED] the re-key's reference-rule edit is not the recorded reference_edit_bn")
    return extra


def backcast_family(case: str) -> str | None:
    """The back-cast's concept tag for a framed case, from the back-cast's own case table.

    None for a case with two payloads (September 29): the back-cast's concept for it is the set, the pension accrual
    included, written to its own directory (derived/<case>/ of the back-cast, in progress on 2026-09-29), and the
    whole-budget rules would need its parts by financing column (the capital return, rental assistance, public
    housing and the accrual) to take the cash part. They are not run; main() names them in summary.json."""
    if case == "sept24":
        return "corrected"
    if LATER_CASES[case].payloads:
        return None
    spec = importlib.util.spec_from_file_location("backcast_cases", BACKCAST / "backcast.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.LATER_CASES[case][1].strip("_")


def per_spec_gates(case: str, corrected: dict, meta: dict, shares: dict, extras: dict, jf: dict, ucf: dict,
                   corrected_cash: dict | None = None) -> dict:
    """The engine port against the case lane's own files, at every specification (September 27 on). From September
    29 `corrected` is the set and the bands file's cash_set row (main profile) is checked on corrected_cash too.

    per_spec.csv holds each fill-in method's run; the payload model is their mean (the case lane's
    independent path gates it to 1e-9), so the port is compared with the methods' mean:
      costs: the cost, the engine's cost (the enterprise receipt included) (1e-6);
      the capital return in total, by level, by part and by component, the enterprise receipt's response,
        group amount and cost, and the three lines' responses and group amounts (1e-9);
      the receipt alone: with only receipt:enterprise_surplus at 1 (no other override, no capital return),
        the cost moves by enterprise_surplus_receipt_cost_bn (1e-9);
      federal plus state and local: at every specification and payer convention the split's federal and
        state-local parts, over the cash lines, the capped programs and the capital return, add to the
        cost plus P (1e-6), and the capital's federal and state-local parts are per_spec's by-level
        columns (1e-9);
      bands: main_case_bands.csv's adopted and uncorrected_at_adopted_responses rows, every profile (1e-4).
    Returns the largest difference of each check."""
    ps = pd.read_csv(case_file(case, "per_spec.csv"))
    methods = ps.method.unique()
    first = ps[ps.method == methods[0]].set_index("spec").sort_index()
    if any(not ps[ps.method == m].set_index("spec").sort_index()[["allocation", "normalization", "share", "gg", "uc"]]
           .equals(first[["allocation", "normalization", "share", "gg", "uc"]]) for m in methods):
        raise SystemExit("[BLOCKED] per_spec.csv: the methods' specifications differ")
    mean = ps.groupby("spec", sort=True).mean(numeric_only=True)
    prof = main_profile(case)
    corners = frame_corners(prof, corrected, meta["responses"], case, meta)
    if len(corners) != len(first):
        raise SystemExit(f"[BLOCKED] {len(corners)} corners against {len(first)} specifications")
    worst: dict[str, float] = {}

    def note(name, value):
        worst[name] = max(worst.get(name, 0.0), abs(float(value)))

    ids = [c["id"] for c in meta["capital_return"]["components"]]
    for i, c in enumerate(corners):
        f, m = first.loc[i], mean.loc[i]
        if (c["allocation"], c["normalization"], c["uc_key"], c["reading"], c["school_share"], c["school_response"],
                c["gg"], c["rate"]) != (f.allocation, f.normalization, f.uc, f.reading, f.share, f.school, f.gg, f.rate):
            raise SystemExit(f"[BLOCKED] corner {i} is not per_spec.csv's specification {i}")
        t = lines_at(c)
        cap = capital_rows(c, t)
        spend, rec = t[t.side == "spending"].set_index("id"), t[t.side == "receipt"].set_index("id")
        note("cost_bn", cost(c) - m.cost_bn)
        note("engine_cost_bn", -welfare(c) - m.engine_cost_bn)
        note("capital_bn", cap.return_bn.sum() - m.capital_total_bn)
        for level in ("state_local", "federal"):
            note("capital_bn", cap[cap.level == level].return_bn.sum() - m[f"capital_{level}_bn"])
        for part in ("core", "block", "enterprise"):
            note("capital_bn", cap[cap.part == part].return_bn.sum() - m[f"capital_{part}_bn"])
        for cid, v in zip(cap.id, cap.return_bn):
            note("capital_bn", v - m[f"capital_{cid}_bn"])
        if list(cap.id) != ids:
            raise SystemExit("[BLOCKED] the capital components are not the payload's")
        es = ENTERPRISE_RECEIPT
        note("receipt_bn", rec.response[es] - m.response_receipt_enterprise_surplus)
        note("receipt_bn", rec.amount_bn[es] - m.group_enterprise_surplus_bn)
        note("receipt_bn", -rec.response[es] * rec.amount_bn[es] - m.enterprise_surplus_receipt_cost_bn)
        for line in (*LONG_RUN_LINES, "housing_subsidies"):
            note("lines_bn", spend.response[line] - m[f"response_{line}"])
            note("lines_bn", spend.amount_bn[line] - m[f"group_{line}_bn"])
        # The receipt alone, on this specification of the schools case.
        alone = dict(c, line_responses={"receipt:" + es: 1.0}, rate=0)
        note("receipt_alone_bn", (cost(alone) - cost(dict(alone, line_responses={}))) - m.enterprise_surplus_receipt_cost_bn)
        p, _ = production(c["normalization"], c["model"])
        capital = capital_split(c)
        for conv in CONVENTIONS:
            before = cash_part(split_corner(dict(c, model=MODEL), shares[conv], extras, conv, LAST, jf, ucf, c["gg_end"]))
            parts = constant_parts(c, conv, shares, extras, before.federal_bn.sum() / before.responsive_bn.sum())
            table = split_corner(c, shares[conv], extras, conv, LAST, jf, ucf, c["gg_end"], parts)
            total = (table.federal_bn.sum() + capital.federal_bn.sum()) + (table.state_local_bn.sum()
                                                                          + capital.state_local_bn.sum())
            note("federal_plus_state_local_bn", total - (m.cost_bn + p))
            note("capital_by_level_bn", capital.federal_bn.sum() - m.capital_federal_bn)
            note("capital_by_level_bn", capital.state_local_bn.sum() - m.capital_state_local_bn)
    bands = pd.read_csv(case_file(case, "main_case_bands.csv"))
    for pf in case_profiles(case):
        variants = [("adopted", corrected), ("uncorrected_at_adopted_responses", MODEL)]
        if corrected_cash is not None and pf == prof:
            variants.append(("cash_set", corrected_cash))
        for variant, model in variants:
            costs = [cost(c) for c in frame_corners(pf, model, meta["responses"], case, meta)]
            row = bands[(bands.profile == pf) & (bands.variant == variant)]
            if len(row) != 1:
                raise SystemExit(f"[BLOCKED] main_case_bands.csv has no single {pf}/{variant} row")
            note("bands_file_bn", min(costs) - row.cost_low_bn.iloc[0])
            note("bands_file_bn", max(costs) - row.cost_high_bn.iloc[0])
    tolerance = dict(cost_bn=1e-6, engine_cost_bn=1e-6, capital_bn=1e-9, receipt_bn=1e-9, lines_bn=1e-9,
                     receipt_alone_bn=1e-9, federal_plus_state_local_bn=1e-6, capital_by_level_bn=1e-9,
                     bands_file_bn=1e-4)
    failed = {k: v for k, v in worst.items() if v > tolerance[k]}
    if failed or set(worst) != set(tolerance):
        raise SystemExit(f"[BLOCKED] the port does not reproduce {case}'s files: {failed or sorted(set(tolerance) - set(worst))}")
    return dict(specifications=len(corners), methods=[str(m) for m in methods], max_abs_diff=worst, tolerance=tolerance)


# The payload consumer (engine.js, model.json and a payload only) at every specification of the case, as JSON.
PARITY_JS = r"""
const C = require(process.argv[1]);
const payload = JSON.parse(require("fs").readFileSync(process.argv[2], "utf8"));
process.stdout.write(JSON.stringify(C.evaluateAll(payload).map((r) => ({ spec: r.spec, cost_bn: r.cost_bn,
  engine_cost_bn: -r.evaluation.welfare_bn, P: r.evaluation.private_wtp_bn, F: r.evaluation.induced_receipts_bn,
  capital: Object.fromEntries(r.capital.components.map((c) => [c.id, c.return_bn])),
  lines: Object.fromEntries(r.evaluation.spending.map((l) => ["spending:" + l.id, [l.amount_bn, l.response]])
    .concat(r.evaluation.receipts.map((l) => ["receipt:" + l.id, [l.amount_bn, l.response]]))) }))));
"""


def engine_parity(case: str, payloads: dict[str, dict], responses: dict) -> dict:
    """The port against engine.js on each payload (September 29): the payload consumer (SEPT29["consumer"], which
    loads only engine.js, model.json and the payload) evaluates the case's 64 specifications; the port's corners
    of the main profile must be the same specifications, in order, and give the same cost, engine cost, P and F,
    capital return by component, and every line's amount and response (1e-9). Returns each payload's band, its
    end specifications and the largest differences."""
    prof = main_profile(case)
    out = {}
    for name, payload in payloads.items():
        run = subprocess.run(["node", "-e", PARITY_JS, str(SEPT29["consumer"]), str(payload_file(case, name))],
                             capture_output=True, text=True)
        if run.returncode != 0:
            raise SystemExit(f"[BLOCKED] the payload consumer failed on {name}: {run.stderr.strip()[-500:]}")
        js = json.loads(run.stdout)
        corners = frame_corners(prof, apply_corrections(MODEL, payload), responses, case, payload["meta"])
        if len(js) != len(corners):
            raise SystemExit(f"[BLOCKED] {name}: {len(js)} consumer specifications against {len(corners)} corners")
        worst = dict(cost_bn=0.0, engine_cost_bn=0.0, production_bn=0.0, capital_bn=0.0, lines_bn=0.0)
        costs = []
        for c, j in zip(corners, js):
            s = j["spec"]
            if (c["allocation"], c["normalization"], c["school_share"], c["school_response"], c["gg"], c["uc_key"],
                    c["reading"]) != (s["allocation"], s["normalization"], s["share"], s["school"], s["gg"], s["uc"],
                                      s["reading"]):
                raise SystemExit(f"[BLOCKED] {name}: a corner is not the consumer's specification {s}")
            t = lines_at(c)
            cap = capital_rows(c, t)
            p, f = production(c["normalization"], c["model"])
            cost_c = -welfare(c) + float(cap.return_bn.sum())
            costs.append(cost_c)
            worst["cost_bn"] = max(worst["cost_bn"], abs(cost_c - j["cost_bn"]))
            worst["engine_cost_bn"] = max(worst["engine_cost_bn"], abs(-welfare(c) - j["engine_cost_bn"]))
            worst["production_bn"] = max(worst["production_bn"], abs(p - j["P"]), abs(f - j["F"]))
            if sorted(cap.id) != sorted(j["capital"]):
                raise SystemExit(f"[BLOCKED] {name}: the capital components differ from the consumer's")
            for cid, v in zip(cap.id, cap.return_bn):
                worst["capital_bn"] = max(worst["capital_bn"], abs(v - j["capital"][cid]))
            lines = {f"{r.side}:{r.id}": (r.amount_bn, r.response) for r in t.itertuples()}
            if set(lines) != set(j["lines"]):
                raise SystemExit(f"[BLOCKED] {name}: the port's lines differ from the engine's "
                                 f"{sorted(set(lines) ^ set(j['lines']))}")
            for k, (amount, response) in lines.items():
                worst["lines_bn"] = max(worst["lines_bn"], abs(amount - j["lines"][k][0]), abs(response - j["lines"][k][1]))
        if max(worst.values()) > 1e-9:
            raise SystemExit(f"[BLOCKED] the port does not reproduce engine.js on {name}: {worst}")
        lo, hi = int(np.argmin(costs)), int(np.argmax(costs))
        out[name] = dict(band_bn=[costs[lo], costs[hi]], end_specifications=[lo, hi], specifications=len(costs),
                         max_abs_diff=worst, tolerance=1e-9, consumer=str(SEPT29["consumer"].relative_to(ROOT)))
    return out


def v4_anchors(case: str, prof: str, corrected: dict, corrected_cash: dict, responses: dict, meta: dict,
               main_summary: dict | None, parity: dict) -> tuple[dict, dict]:
    """A September 29 profile's band corners on the set (the adopted case) and the same specifications on the cash
    set, which is what is compounded. Gates: the cash set's ends are the set's specifications; on the main profile
    the set's and the cash set's bands and ends are engine.js's (engine_parity, 1e-9); where the lane writes the
    September 27 contract, every profile's set band and the uncorrected model's band are its summary.json's, and the
    main profile's cash band and end specifications its cash_set (1e-6). The uncorrected model here is model.json:
    the adopted package adds the payload's two receipt lines and eight correction lines at zero to it, which adds
    nothing to a cost or a capital key (capital_rows). Returns ({end: cash corner}, {end: set corner})."""
    cs_set = frame_corners(prof, corrected, responses, case, meta)
    cs_cash = frame_corners(prof, corrected_cash, responses, case, meta)
    set_costs, cash_costs = [cost(c) for c in cs_set], [cost(c) for c in cs_cash]
    ends = (int(np.argmin(set_costs)), int(np.argmax(set_costs)))
    if (int(np.argmin(cash_costs)), int(np.argmax(cash_costs))) != ends:
        raise SystemExit(f"[BLOCKED] {prof}: the cash set's ends are not the set's specifications {ends}")
    if prof == main_profile(case):
        for name, costs in (("set", set_costs), ("cash", cash_costs)):
            p = parity[name]
            if list(ends) != p["end_specifications"] or max(abs(costs[i] - b) for i, b in zip(ends, p["band_bn"])) > 1e-9:
                raise SystemExit(f"[BLOCKED] {prof}: the {name} band is not engine.js's")
    if main_summary is not None:
        want = main_summary["main_case"] if prof == main_profile(case) else main_summary["other_profiles"][prof]["adopted"]
        unc = [cost(c) for c in frame_corners(prof, MODEL, responses, case, meta)]
        want_unc = (main_summary["uncorrected_at_adopted_responses"] if prof == main_profile(case)
                    else main_summary["other_profiles"][prof]["uncorrected_at_adopted_responses"])
        got = [set_costs[ends[0]], set_costs[ends[1]]]
        if max(abs(g - w) for g, w in zip(got + [min(unc), max(unc)], list(want) + list(want_unc))) > 1e-6:
            raise SystemExit(f"[BLOCKED] {prof}: the band {got} or the uncorrected band is not {case}'s summary.json's")
        if prof == main_profile(case):      # the cash set's band and end specifications, each fill-in method's
            cash = main_summary["cash_set"]
            got = [cash_costs[ends[0]], cash_costs[ends[1]]]
            if max(abs(g - w) for g, w in zip(got, cash["band_bn"])) > 1e-6 or \
                    any(list(e) != list(ends) for e in cash["end_specifications"]):
                raise SystemExit(f"[BLOCKED] {prof}: the cash band {got} at {ends} is not {case}'s summary.json cash_set")
    return ({"low": cs_cash[ends[0]], "high": cs_cash[ends[1]]}, {"low": cs_set[ends[0]], "high": cs_set[ends[1]]})


def accrual_rows(set_corner: dict, cash_corner: dict) -> pd.DataFrame:
    """The pension accrual at one corner (September 29): the set less the cash set, line by line, on the lines
    the two payloads differ on (social security, Medicare and federal income tax, all federal). Gate: no other
    line differs (1e-12). Rows as split_corner's, side pension_accrual, financing pension_accrual."""
    a, b = lines_at(set_corner).set_index(["side", "id"]), lines_at(cash_corner).set_index(["side", "id"])
    if list(a.index) != list(b.index):
        raise SystemExit("[BLOCKED] the set and the cash set do not have the same lines")
    d = (a.responsive_bn - b.responsive_bn) * np.where(a.index.get_level_values(0) == "spending", 1.0, -1.0)
    moved = d[d.abs() > 1e-12]
    if set(moved.index) - set(ACCRUAL_LINES):
        raise SystemExit(f"[BLOCKED] the set and the cash set differ on {sorted(set(moved.index) - set(ACCRUAL_LINES))}")
    rows = [dict(side="pension_accrual", id=line, responsive_bn=float(d.get((side, line), 0.0)),
                 federal_bn=float(d.get((side, line), 0.0)), state_local_bn=0.0, financing="pension_accrual")
            for side, line in ACCRUAL_LINES]
    return pd.DataFrame(rows)


ACCRUAL_LINES = (("spending", "social_security"), ("spending", "medicare"), ("receipt", "federal_income_tax"))


def case_split(case: str, shares: dict, extras: dict, jf: dict, ucf: dict) -> dict:
    """Section 1 of main() on one case: the corners that set each band, the 2024 split at each corner and
    convention, the main profile's lines and, from September 24 on, each correction's split (COMPONENTS
    must hold the case's payload by component). Gates as in main().

    A case with profiles of its own (September 27) splits each corner into the three columns: the cash
    gap (fiscal_gap_bn, federal_bn: the part that is borrowed), the capital return (resource cost) and the
    capped programs (displaced beneficiaries), each with its federal part. Their sum is the net cost plus
    P (1e-6); the corners are the case's end specifications; the port reproduces per_spec.csv
    (per_spec_gates).

    A case with two payloads (September 29) takes its corners from the set, the adopted case, and splits the
    cash set at them (the anchors it returns are the cash corners; set_anchors the set's). The fourth column,
    the pension accrual, is the set less the cash set (accrual_rows); cash + resource cost + displaced + accrual
    = the set's net cost + P (1e-6). The corrections split is the cash set's: the previous case's components,
    then the September 29 parts (v4_components) and the production grid's change in F. The port is gated
    against engine.js (engine_parity) and, where the lane writes the September 27 contract, per_spec.csv."""
    framed = case != "sept23"
    responses, meta, gates = None, None, None
    v4 = case in LATER_CASES and LATER_CASES[case].payloads is not None
    set_anchors, parity, v4_edits, corrected_cash, f_item = None, None, None, None, None
    if case in LATER_CASES:
        payload = case_payload(case)
        responses, meta = payload["meta"]["responses"], payload["meta"]
        corrected = apply_corrections(MODEL, payload)
        if v4:
            cash_payload = case_payload(case, "cash")
            if cash_payload["meta"]["responses"] != responses:
                raise SystemExit("[BLOCKED] the set's and the cash set's responses differ")
            corrected_cash = apply_corrections(MODEL, cash_payload)
            main_summary = json.loads(case_file(case, "summary.json").read_text()) if SEPT29["contract"] else None
            parity = engine_parity(case, {"set": payload, "cash": cash_payload}, responses)
            oracle = SEPT29["oracle"]
            for name in ("set", "cash"):        # the adopted bands as printed (4 decimals)
                if parity[name]["end_specifications"] != list(oracle["ends"]) or \
                        max(abs(g - w) for g, w in zip(parity[name]["band_bn"], oracle[name])) > 5e-5:
                    raise SystemExit(f"[BLOCKED] the {name} band {parity[name]['band_bn']} at "
                                     f"{parity[name]['end_specifications']} is not the adopted {oracle[name]}")
            both = {prof: v4_anchors(case, prof, corrected, corrected_cash, responses, meta, main_summary, parity)
                    for prof in case_profiles(case)}
            anchors = {prof: b[0] for prof, b in both.items()}
            set_anchors = {prof: b[1] for prof, b in both.items()}
            v4_edits = v4_components(case, cash_payload)
            f_item = "v4_" + "+".join(cash_payload["meta"]["candidate_v4"]["items_by_line"]["production:F"])
        else:
            main_summary = json.loads(case_file(case, "summary.json").read_text())
            anchors = {prof: case_anchors(prof, corrected, main_summary, responses, case, meta)
                       for prof in case_profiles(case)}
    elif framed:
        corrected = apply_corrections(MODEL, json.loads(CORRECTIONS_FILE.read_text()))
        main_summary = json.loads(MAIN24_SUMMARY.read_text())
        anchors = {prof: sept24_anchors(prof, corrected, main_summary) for prof in PROFILES}
    else:
        corrected, main_summary = None, None
        anchors = {prof: adopted_anchors(prof) for prof in PROFILES}
    main_prof = main_profile(case if case in LATER_CASES else None)
    three = case in LATER_CASES and LATER_CASES[case].profiles is not None
    if three and main_summary is not None:
        gates = per_spec_gates(case, corrected, meta, shares, extras, jf, ucf, corrected_cash)
        for end, corner in anchors[main_prof].items():
            want = next(iter(main_summary["end_specifications"]))[f"{end}_end"]
            got = dict(allocation=corner["allocation"], normalization=corner["normalization"], share=corner["school_share"],
                       school=corner["school_response"], gg=corner["gg"], uc=corner["uc_key"], reading=corner["reading"])
            if any(got[k] != want[k] for k in got) or any(m[f"{end}_end"]["index"] != want["index"]
                                                       for m in main_summary["end_specifications"]):
                raise SystemExit(f"[BLOCKED] the {end} corner is not the case's end specification {want['index']}")
    parts, correction_rows = {}, []
    split_rows, line_rows = [], []
    for prof, ends in anchors.items():
        for end, corner in ends.items():
            p, _ = production(corner["normalization"], corner.get("model"))
            set_corner = set_anchors[prof][end] if v4 else corner
            net = cost(set_corner)
            capital = capital_split(corner)
            if v4:
                accrual = accrual_rows(set_corner, corner)
                cap_set = capital_split(set_corner)
                if (production(set_corner["normalization"], set_corner["model"])[0] != p
                        or list(cap_set.id) != list(capital.id)
                        or (cap_set.responsive_bn - capital.responsive_bn).abs().max() > 1e-12):
                    raise SystemExit(f"[BLOCKED] {prof} {end}: the set and the cash set differ in P or the capital return")
            for conv in CONVENTIONS:
                if framed:
                    before = split_corner(dict(corner, model=MODEL), shares[conv], extras, conv, LAST, jf, ucf, end)
                    b = cash_part(before)
                    parts[(prof, end, conv)] = constant_parts(corner, conv, shares, extras,
                                                              b.federal_bn.sum() / b.responsive_bn.sum())
                table = split_corner(corner, shares[conv], extras, conv, LAST, jf, ucf, end, parts.get((prof, end, conv)))
                cols = three_columns(table, capital)
                gap, fed = cols["cash_bn"], cols["cash_federal_bn"]
                acc, acc_fed = (float(accrual.responsive_bn.sum()), float(accrual.federal_bn.sum())) if v4 else (0.0, 0.0)
                if abs(gap + cols["displaced_bn"] + cols["resource_cost_bn"] + acc - (net + p)) > 1e-6:
                    raise SystemExit(f"[BLOCKED] {prof} {end}: fiscal gap {gap} (with displaced, resource cost and "
                                     f"accrual) != cost + P {net + p}")
                if framed and prof == main_prof:
                    cs = correction_split(corner, shares[conv], extras, conv, LAST, parts[(prof, end, conv)],
                                          COMPONENTS["edits"] + (v4_edits or []))
                    if v4:              # the production grid's change in F (row-4 weights), as a correction of its own
                        f0 = production(corner["normalization"])[1]
                        effect = -(production(corner["normalization"], corner["model"])[1] - f0)
                        fed_f = effect * shares[conv].loc[LAST, "_induced_receipts"]
                        cs = pd.concat([cs, pd.DataFrame([dict(component=f_item, side="production", line="induced_receipts_F",
                                                               cell="grid", effect_bn=effect, federal_bn=fed_f,
                                                               state_local_bn=effect - fed_f, financing="cash")])],
                                       ignore_index=True)
                    if (cs.federal_bn + cs.state_local_bn - cs.effect_bn).abs().max() > 1e-12:
                        raise SystemExit("[BLOCKED] a correction's federal and state-local parts do not add to it")
                    groups = [("cash", cash_part(cs), cash_part(table), cash_part(before))]
                    if three:
                        pick = lambda x: x[x.financing == "displaced_beneficiaries"]  # noqa: E731
                        groups.append(("displaced", pick(cs), pick(table), pick(before)))
                    for name, c, after_t, before_t in groups:
                        d_gap = after_t.responsive_bn.sum() - before_t.responsive_bn.sum()
                        d_fed = after_t.federal_bn.sum() - before_t.federal_bn.sum()
                        if abs(c.effect_bn.sum() - d_gap) > 1e-9 or abs(c.federal_bn.sum() - d_fed) > 1e-9:
                            raise SystemExit(f"[BLOCKED] {end}/{conv}: {name} corrections add to {c.effect_bn.sum():.6f} "
                                             f"(federal {c.federal_bn.sum():.6f}), the split moved {d_gap:.6f} ({d_fed:.6f})")
                    for r in cs.itertuples():
                        correction_rows.append(dict(end=end, convention=conv, allocation=corner["allocation"],
                                                    component=r.component, side=r.side, line=r.line, cell=r.cell,
                                                    effect_bn=r.effect_bn, federal_bn=r.federal_bn,
                                                    state_local_bn=r.state_local_bn,
                                                    **({"financing": r.financing} if three else {})))
                split_rows.append(dict(profile=prof, end=end, convention=conv, allocation=corner["allocation"],
                                       normalization=corner["normalization"], school_share=corner["school_share"],
                                       school_response=corner["school_response"],
                                       general_government_response=corner["gg"],
                                       uncompensated_inside_bn=corner["uc"], net_cost_bn=net, production_P_bn=p,
                                       fiscal_gap_bn=gap, federal_bn=fed, state_local_bn=gap - fed,
                                       federal_share=fed / gap,
                                       **({k: cols[k] for k in ("resource_cost_bn", "resource_cost_federal_bn",
                                                                "displaced_bn", "displaced_federal_bn")} if three else {}),
                                       **(dict(accrual_bn=acc, accrual_federal_bn=acc_fed,
                                               cash_set_net_cost_bn=cost(corner)) if v4 else {})))
                if prof == main_prof:
                    rows = pd.concat([table, capital] + ([accrual] if v4 else []), ignore_index=True) if three else table
                    for r in rows.itertuples():
                        line_rows.append(dict(end=end, convention=conv, side=r.side, line=r.id,
                                              gap_bn=r.responsive_bn, federal_bn=r.federal_bn,
                                              state_local_bn=r.state_local_bn,
                                              **({"financing": r.financing} if three else {})))
    return dict(anchors=anchors, corrected=corrected, main_summary=main_summary, responses=responses, parts=parts,
                split=pd.DataFrame(split_rows), lines=pd.DataFrame(line_rows), meta=meta, per_spec=gates,
                main_profile=main_prof, case=case, corrections=pd.DataFrame(correction_rows) if framed else None,
                set_anchors=set_anchors, corrected_cash=corrected_cash, parity=parity)


EDUCATION_LINES = {"education_services", "school_reprice", "college_rekey"}


def response_bridge(prev: dict, run: dict, shares: dict, extras: dict, jf: dict, ucf: dict) -> pd.DataFrame:
    """The 2024 split from one later case to the next, main profile, each band end, when they differ by
    responses only (case_payload gates equal edits). Steps: the previous case; the new responses at the
    previous case's corners (matched specifications), as the move on the education lines and the move in
    the constant line's federal part (its small corrections carry the corner's average federal share,
    which the responses shift); the range ends moving to the new case's corners; the new case. Gates: the
    previous corner reproduces the previous split (1e-9); at matched specifications only the education
    lines move (1e-9), and their federal part is their move at the lane's school share (the education
    share, or the high K-12 share under the high convention; 1e-9); the steps move the gap by the new
    lane's band change plus the change in P (1e-6) and add to the new split (1e-9)."""
    change = run["main_summary"]["change"]
    old_r, new_r = prev["responses"], run["responses"]
    old_school = (old_r["school"]["growth"], old_r["school"]["decline"])
    new_school = (new_r["school"]["growth"], new_r["school"]["decline"])
    rows = []
    for i, end in enumerate(("low", "high")):
        c0, c1 = prev["anchors"][MAIN][end], run["anchors"][MAIN][end]
        at = [k for k, v in enumerate(old_school) if v == c0["school_response"]]
        if not at or (len(at) > 1 and new_school[0] != new_school[1]):
            raise SystemExit(f"[BLOCKED] the {end} corner's school response has no single growth/decline position")
        matched = dict(c0, school_response=new_school[at[0]], gg=new_r["general_government"][c0["gg_end"]],
                       model=run["corrected"])
        a, b = lines_at(c0), lines_at(matched)
        if list(a.id) != list(b.id) or (b.responsive_bn - a.responsive_bn)[~a.id.isin(EDUCATION_LINES)].abs().max() > 1e-9:
            raise SystemExit(f"[BLOCKED] {end}: at matched specifications a line other than education moved")
        p0, _ = production(c0["normalization"])
        p1, _ = production(c1["normalization"])
        for conv in CONVENTIONS:
            before = split_corner(dict(matched, model=MODEL), shares[conv], extras, conv, LAST, jf, ucf, end)
            parts = constant_parts(matched, conv, shares, extras, before.federal_bn.sum() / before.responsive_bn.sum())
            t = split_corner(matched, shares[conv], extras, conv, LAST, jf, ucf, end, parts)
            t0 = split_corner(c0, shares[conv], extras, conv, LAST, jf, ucf, end, prev["parts"][(MAIN, end, conv)])
            d = t0.merge(t, on=["side", "id"], how="outer", suffixes=("_0", "_1"), validate="one_to_one").fillna(0.0)
            d = d.assign(gap=d.responsive_bn_1 - d.responsive_bn_0, fed=d.federal_bn_1 - d.federal_bn_0)
            edu, rest = d[d.id.isin(EDUCATION_LINES)], d[~d.id.isin(EDUCATION_LINES)]
            phi = shares[conv].loc[LAST]
            school = phi["_school_high"] if conv == "high" else phi["education_services"]
            want = sum(r.gap * (phi["education_services"] if r.id == "college_rekey" else school) for r in edu.itertuples())
            if rest.gap.abs().max() > 1e-9 or abs(edu.fed.sum() - want) > 1e-9:
                raise SystemExit(f"[BLOCKED] {end}/{conv}: the step on the education lines is not at their federal "
                                 f"share ({edu.fed.sum():.9f} vs {want:.9f}) or another line's amount moved")
            if set(rest.id[rest.fed.abs() > 1e-12]) - {"lane_constants"}:
                raise SystemExit(f"[BLOCKED] {end}/{conv}: a federal part moved on "
                                 f"{sorted(set(rest.id[rest.fed.abs() > 1e-12]))}")
            gm, fm = t.responsive_bn.sum(), t.federal_bn.sum()
            pick = lambda split: split[(split.profile == MAIN) & (split.end == end)  # noqa: E731
                                       & (split.convention == conv)].iloc[0]
            old, new = pick(prev["split"]), pick(run["split"])
            if abs(t0.responsive_bn.sum() - old.fiscal_gap_bn) > 1e-9 or abs(t0.federal_bn.sum() - old.federal_bn) > 1e-9:
                raise SystemExit(f"[BLOCKED] {end}/{conv}: the previous corner does not reproduce the previous split")
            if abs(new.fiscal_gap_bn - old.fiscal_gap_bn - (change[i] + p1 - p0)) > 1e-6:
                raise SystemExit(f"[BLOCKED] {end}/{conv}: the gap moves {new.fiscal_gap_bn - old.fiscal_gap_bn:.6f}, "
                                 f"the lane's band change plus P {change[i] + p1 - p0:.6f}")
            steps = [("previous_case", old.fiscal_gap_bn, old.federal_bn),
                     ("school_response_on_education_lines", edu.gap.sum(), edu.fed.sum()),
                     ("constant_line_federal_share", rest.gap.sum(), rest.fed.sum()),
                     ("range_ends_move", new.fiscal_gap_bn - gm, new.federal_bn - fm)]
            total = sum(s[1] for s in steps), sum(s[2] for s in steps)
            if abs(total[0] - new.fiscal_gap_bn) > 1e-9 or abs(total[1] - new.federal_bn) > 1e-9:
                raise SystemExit(f"[BLOCKED] {end}/{conv}: the steps do not add to the new split")
            steps.append(("this_case", new.fiscal_gap_bn, new.federal_bn))
            rows += [dict(end=end, convention=conv, step=s, gap_bn=g, federal_bn=f, state_local_bn=g - f)
                     for s, g, f in steps]
    return pd.DataFrame(rows)


BRIDGE_COLUMNS = ("cash_gap_bn", "cash_federal_bn", "resource_cost_bn", "resource_cost_federal_bn", "displaced_bn",
                  "displaced_federal_bn")


def capital_bridge(prev: dict, run: dict, shares: dict, extras: dict, jf: dict, ucf: dict) -> pd.DataFrame:
    """The 2024 split from the previous case (the schools case) to one with profiles of its own (September
    27), main profile, each band end, in the three columns: cash (the gap that is borrowed), resource cost
    (the capital return) and displaced beneficiaries (the capped programs), each with its federal part.

    Steps, at the previous case's specifications, in the case lane's chain order:
      previous_case                 the previous split (all of its gap was cash);
      capped_programs_leave_cash    LIHEAP, at response 1 in both cases, moves from cash to displaced;
      long_run_responses            roads and parks at their long-run responses (cash), federal by subfunction;
      rental_assistance             rental assistance at 1 (displaced; federal);
      capital_core, capital_block   the capital return's core and road-and-park parts (resource cost);
      enterprise_surplus_receipt    the enterprise surplus receipt at 1 on its re-keyed share (cash), at its
                                    federal share t32(23)/t31(19): the federal share's own row;
      capital_enterprise            the enterprise capital return (resource cost);
      constant_line_federal_share   the constant line's small corrections take the corner's average cash
                                    share, which the steps above shift;
      range_ends_move               to the new case's corners;
      this_case.
    Gates: the previous corner reproduces the previous split (1e-9); each step moves only its own lines, in
    amount and federal part, and the constant line only in its federal part (1e-9); the capped step moves
    nothing in total (1e-9); the steps add to the new split in every column (1e-9); each step's total is
    the case lane's change_at_fixed_specifications part and the whole its band change plus the change in P
    (1e-6); the range ends do not move where the corners share their specification (1e-9)."""
    new_prof, old_prof, meta = run["main_profile"], prev["main_profile"], run["meta"]
    chain, change = run["main_summary"]["change_at_fixed_specifications"], run["main_summary"]["change"]
    if any(abs(x) > 0 for x in chain["enterprise_rekey"]):
        raise SystemExit("[BLOCKED] the case lane's re-key step moves the cost at fixed specifications")
    long_run = case_profiles(run["case"])[new_prof][1]
    spec_keys = ("allocation", "normalization", "school_share", "school_response", "gg", "uc_key")
    rows = []
    for i, end in enumerate(("low", "high")):
        c0, c1 = prev["anchors"][old_prof][end], run["anchors"][new_prof][end]
        f = later_fields(meta, long_run, c0["gg_end"])
        k0 = dict(c0, profile=new_prof, model=run["corrected"], capped=f["capped"])
        k1 = dict(k0, line_responses={line: f["line_responses"][line] for line in LONG_RUN_LINES},
                  **{k: f[k] for k in ("reading", "long_run", "subfunctions", "subfunction_rows")})
        k2 = dict(k1, line_responses=dict(k1["line_responses"], housing_subsidies=f["line_responses"]["housing_subsidies"]))
        k3 = dict(k2, line_responses=dict(f["line_responses"]))
        capital = capital_split(dict(k3, rate=f["rate"], capital_meta=f["capital_meta"]))
        p0, _ = production(c0["normalization"])
        p1, _ = production(c1["normalization"])
        for conv in CONVENTIONS:
            def split_at(corner):
                before = cash_part(split_corner(dict(corner, model=MODEL), shares[conv], extras, conv, LAST, jf, ucf, end))
                parts = constant_parts(corner, conv, shares, extras, before.federal_bn.sum() / before.responsive_bn.sum())
                return split_corner(corner, shares[conv], extras, conv, LAST, jf, ucf, end, parts)
            pick = lambda split: split[(split.end == end) & (split.convention == conv)].iloc[0]  # noqa: E731
            old, new = pick(prev["split"]), pick(run["split"])
            t_prev = split_corner(c0, shares[conv], extras, conv, LAST, jf, ucf, end, prev["parts"][(old_prof, end, conv)])
            if abs(t_prev.responsive_bn.sum() - old.fiscal_gap_bn) > 1e-9 or abs(t_prev.federal_bn.sum() - old.federal_bn) > 1e-9:
                raise SystemExit(f"[BLOCKED] {end}/{conv}: the previous corner does not reproduce the previous split")
            tables = [t_prev] + [split_at(k) for k in (k0, k1, k2, k3)]
            owns = [set(), set(LONG_RUN_LINES), {"housing_subsidies"}, {ENTERPRISE_RECEIPT}]
            names = ["capped_programs_leave_cash", "long_run_responses", "rental_assistance", "enterprise_surplus_receipt"]
            steps, constant_fed = {}, 0.0
            for name, own, a, b in zip(names, owns, tables[:-1], tables[1:]):
                d = a.merge(b, on=["side", "id"], how="outer", suffixes=("_0", "_1"), validate="one_to_one")
                d[["responsive_bn_0", "responsive_bn_1", "federal_bn_0", "federal_bn_1"]] = \
                    d[["responsive_bn_0", "responsive_bn_1", "federal_bn_0", "federal_bn_1"]].fillna(0.0)
                gap, fed = d.responsive_bn_1 - d.responsive_bn_0, d.federal_bn_1 - d.federal_bn_0
                mine, const = d.id.isin(own), d.id == "lane_constants"
                if gap[~mine].abs().max() > 1e-9 or fed[~mine & ~const].abs().max() > 1e-9:
                    raise SystemExit(f"[BLOCKED] {end}/{conv}: step {name} moves a line other than its own")
                constant_fed += float(fed[const].sum())
                ca, cb = three_columns(a, capital.iloc[:0]), three_columns(b, capital.iloc[:0])
                steps[name] = {k: cb[k] - ca[k] for k in ca}
                steps[name]["cash_federal_bn"] -= float(fed[const].sum())
            for part in ("core", "block", "enterprise"):
                c = capital[capital.part == part]
                steps[f"capital_{part}"] = dict(cash_bn=0.0, cash_federal_bn=0.0, resource_cost_bn=float(c.responsive_bn.sum()),
                                                resource_cost_federal_bn=float(c.federal_bn.sum()), displaced_bn=0.0,
                                                displaced_federal_bn=0.0)
            steps["constant_line_federal_share"] = dict(cash_bn=0.0, cash_federal_bn=constant_fed, resource_cost_bn=0.0,
                                                        resource_cost_federal_bn=0.0, displaced_bn=0.0, displaced_federal_bn=0.0)
            matched = three_columns(tables[-1], capital)
            new_cols = dict(cash_bn=new.fiscal_gap_bn, cash_federal_bn=new.federal_bn, resource_cost_bn=new.resource_cost_bn,
                            resource_cost_federal_bn=new.resource_cost_federal_bn, displaced_bn=new.displaced_bn,
                            displaced_federal_bn=new.displaced_federal_bn)
            steps["range_ends_move"] = {k: new_cols[k] - matched[k] for k in matched}
            if all(c0[k] == c1[k] for k in spec_keys) and max(abs(v) for v in steps["range_ends_move"].values()) > 1e-9:
                raise SystemExit(f"[BLOCKED] {end}/{conv}: the range ends move although the corners share their specification")
            if abs(sum(steps["capped_programs_leave_cash"][k] for k in ("cash_bn", "displaced_bn"))) > 1e-9:
                raise SystemExit(f"[BLOCKED] {end}/{conv}: the capped step moves the total")
            for name, key in (("long_run_responses", "long_run_responses"), ("rental_assistance", "rental_assistance"),
                              ("capital_core", "capital_core"), ("capital_block", "capital_block"),
                              ("enterprise_surplus_receipt", "enterprise_surplus_receipt"),
                              ("capital_enterprise", "capital_enterprise")):
                s = steps[name]
                if abs(s["cash_bn"] + s["resource_cost_bn"] + s["displaced_bn"] - chain[key][i]) > 1e-6:
                    raise SystemExit(f"[BLOCKED] {end}/{conv}: step {name} is not the case lane's {key} "
                                     f"({s['cash_bn'] + s['resource_cost_bn'] + s['displaced_bn']:.6f} vs {chain[key][i]:.6f})")
            order = ["capped_programs_leave_cash", "long_run_responses", "rental_assistance", "capital_core", "capital_block",
                     "enterprise_surplus_receipt", "capital_enterprise", "constant_line_federal_share", "range_ends_move"]
            start = dict(cash_bn=old.fiscal_gap_bn, cash_federal_bn=old.federal_bn, resource_cost_bn=0.0,
                         resource_cost_federal_bn=0.0, displaced_bn=0.0, displaced_federal_bn=0.0)
            total = {k: start[k] + sum(steps[s][k] for s in order) for k in start}
            if max(abs(total[k] - new_cols[k]) for k in total) > 1e-9:
                raise SystemExit(f"[BLOCKED] {end}/{conv}: the steps do not add to the new split")
            whole = sum(new_cols[k] for k in ("cash_bn", "resource_cost_bn", "displaced_bn")) - old.fiscal_gap_bn
            if abs(whole - (change[i] + p1 - p0)) > 1e-6:
                raise SystemExit(f"[BLOCKED] {end}/{conv}: the total moves {whole:.6f}, the lane's band change plus P "
                                 f"{change[i] + p1 - p0:.6f}")
            for name, cols in [("previous_case", start)] + [(s, steps[s]) for s in order] + [("this_case", new_cols)]:
                rows.append(dict(end=end, convention=conv, step=name, cash_gap_bn=cols["cash_bn"],
                                 cash_federal_bn=cols["cash_federal_bn"],
                                 cash_state_local_bn=cols["cash_bn"] - cols["cash_federal_bn"],
                                 **{k: cols[k] for k in BRIDGE_COLUMNS[2:]}))
    out = pd.DataFrame(rows)
    number = out.select_dtypes("number").columns
    out[number] = out[number].round(6) + 0.0             # no negative zeros in the file
    return out


V4_BRIDGE_COLUMNS = BRIDGE_COLUMNS + ("accrual_bn", "accrual_federal_bn")


def v4_bridge(prev: dict, run: dict, shares_prev: dict, shares_new: dict, extras: dict, jf: dict, ucf: dict,
              meta_cash: dict) -> pd.DataFrame:
    """The 2024 split from the previous case (September 27) to the September 29 case, main profile, each band end,
    in four columns: cash, resource cost, displaced beneficiaries and the pension accrual, each with its federal
    part. The cash set is the one split and compounded; the accrual is its own step.

    Steps, at the previous case's specifications (the September 29 corner with the same specification):
      previous_case                  the previous split;
      v4_<items>                     each line's move, assigned to the items that move it (the cash payload's
                                     meta.candidate_v4.items_by_line: spending, receipts, production and capital
                                     entries); a line that two or more items move is one step named for all of
                                     them, since the payload holds their composition, not a split of it;
      constant_line_federal_share    the constant line's small corrections take the corner's average cash share,
                                     which the steps above shift (federal part only);
      pension_accrual                the set less the cash set (accrual_rows);
      range_ends_move                to the new case's corners;
      this_case.
    Gates: the previous corner reproduces the previous split (1e-9); every line that moves is assigned, the
    constant line moves only in its federal part, and no other line moves (1e-9); at the matched specification the
    steps add to its split in every column (1e-9); the whole moves by the change in the set's band plus the change
    in P (1e-6); the range ends do not move where the corners share their specification (1e-9)."""
    items = meta_cash["candidate_v4"]["items_by_line"]
    new_prof, old_prof = run["main_profile"], prev["main_profile"]
    spec_keys = ("allocation", "normalization", "school_share", "school_response", "gg", "uc_key")
    change = [run["parity"]["set"]["band_bn"][i] - prev["main_summary"]["main_case"][i] for i in range(2)]
    cols4 = ("cash_bn", "cash_federal_bn") + V4_BRIDGE_COLUMNS[2:]
    rows = []
    for i, end in enumerate(("low", "high")):
        c0, c1 = prev["anchors"][old_prof][end], run["anchors"][new_prof][end]
        # Schools respond at 1 in growth and decline alike, so a specification can appear twice; its corners are equal.
        cands = [c for c in frame_corners(new_prof, run["corrected_cash"], run["responses"], run["case"], run["meta"])
                 if all(c[k] == c0[k] for k in spec_keys)]
        if not cands:
            raise SystemExit(f"[BLOCKED] {end}: no September 29 corner at the previous case's specification")
        matched = cands[0]
        set_matched = dict(matched, model=run["corrected"])
        accrual = accrual_rows(set_matched, matched)
        cap0, cap1 = capital_split(c0), capital_split(matched)
        p0, _ = production(c0["normalization"], c0["model"])
        p1, _ = production(c1["normalization"], c1["model"])
        for conv in CONVENTIONS:
            old = prev["split"][(prev["split"].profile == old_prof) & (prev["split"].end == end)
                                & (prev["split"].convention == conv)].iloc[0]
            new = run["split"][(run["split"].profile == new_prof) & (run["split"].end == end)
                               & (run["split"].convention == conv)].iloc[0]
            t0 = split_corner(c0, shares_prev[conv], extras, conv, LAST, jf, ucf, end, prev["parts"][(old_prof, end, conv)])
            if abs(t0.responsive_bn.sum() - old.fiscal_gap_bn - old.displaced_bn) > 1e-9 or \
                    abs(cash_part(t0).federal_bn.sum() - old.federal_bn) > 1e-9:
                raise SystemExit(f"[BLOCKED] {end}/{conv}: the previous corner does not reproduce the previous split")
            before = cash_part(split_corner(dict(matched, model=MODEL), shares_new[conv], extras, conv, LAST, jf, ucf, end))
            parts = constant_parts(matched, conv, shares_new, extras, before.federal_bn.sum() / before.responsive_bn.sum())
            t1 = split_corner(matched, shares_new[conv], extras, conv, LAST, jf, ucf, end, parts)
            d = t0.merge(t1, on=["side", "id"], how="outer", suffixes=("_0", "_1"), validate="one_to_one")
            for col in ("responsive_bn_0", "responsive_bn_1", "federal_bn_0", "federal_bn_1"):
                d[col] = d[col].fillna(0.0)
            d["financing_1"] = d.financing_1.fillna(d.financing_0)
            d["financing_0"] = d.financing_0.fillna(d.financing_1)
            steps: dict[str, dict] = {}

            def add(step, col, gap, fed):
                s = steps.setdefault(step, {k: 0.0 for k in cols4})
                s[col] += gap
                s[col.replace("_bn", "_federal_bn")] += fed

            for r in d.itertuples():
                gap, fed = r.responsive_bn_1 - r.responsive_bn_0, r.federal_bn_1 - r.federal_bn_0
                if r.id == "lane_constants":
                    if abs(gap) > 1e-9:
                        raise SystemExit(f"[BLOCKED] {end}/{conv}: the constant line moved in amount")
                    add("constant_line_federal_share", "cash_bn", 0.0, fed)
                    continue
                if abs(gap) <= 1e-12 and abs(fed) <= 1e-12:
                    continue
                key = ("production:F" if r.side == "production"
                       else f"{'receipts' if r.side == 'receipt' else 'spending'}:{r.id}")
                if key not in items:
                    raise SystemExit(f"[BLOCKED] {end}/{conv}: {key} moved ({gap:.3e}, federal {fed:.3e}) but no item moves it")
                if r.financing_0 != r.financing_1:
                    raise SystemExit(f"[BLOCKED] {end}/{conv}: {key} changed financing")
                col = "displaced_bn" if r.financing_1 == "displaced_beneficiaries" else "cash_bn"
                add("v4_" + "+".join(items[key]), col, gap, fed)
            c = cap0.merge(cap1, on="id", how="outer", suffixes=("_0", "_1"), validate="one_to_one").fillna(0.0)
            for r in c.itertuples():
                gap, fed = r.responsive_bn_1 - r.responsive_bn_0, r.federal_bn_1 - r.federal_bn_0
                if abs(gap) <= 1e-12 and abs(fed) <= 1e-12:
                    continue
                key = f"capital:{r.id}"
                if key not in items:
                    raise SystemExit(f"[BLOCKED] {end}/{conv}: capital component {r.id} moved but no item moves it")
                add("v4_" + "+".join(items[key]), "resource_cost_bn", gap, fed)
            add("pension_accrual", "accrual_bn", float(accrual.responsive_bn.sum()), float(accrual.federal_bn.sum()))
            start = dict(cash_bn=old.fiscal_gap_bn, cash_federal_bn=old.federal_bn, resource_cost_bn=old.resource_cost_bn,
                         resource_cost_federal_bn=old.resource_cost_federal_bn, displaced_bn=old.displaced_bn,
                         displaced_federal_bn=old.displaced_federal_bn, accrual_bn=0.0, accrual_federal_bn=0.0)
            matched_cols = {k: start[k] + sum(s[k] for s in steps.values()) for k in start}
            at = dict(three_columns(t1, cap1), accrual_bn=float(accrual.responsive_bn.sum()),
                      accrual_federal_bn=float(accrual.federal_bn.sum()))
            if max(abs(matched_cols[k] - at[k]) for k in start) > 1e-9:
                raise SystemExit(f"[BLOCKED] {end}/{conv}: the steps do not add to the split at the matched specification")
            new_cols = dict(cash_bn=new.fiscal_gap_bn, cash_federal_bn=new.federal_bn, resource_cost_bn=new.resource_cost_bn,
                            resource_cost_federal_bn=new.resource_cost_federal_bn, displaced_bn=new.displaced_bn,
                            displaced_federal_bn=new.displaced_federal_bn, accrual_bn=new.accrual_bn,
                            accrual_federal_bn=new.accrual_federal_bn)
            steps["range_ends_move"] = {k: new_cols[k] - matched_cols[k] for k in start}
            if all(c0[k] == c1[k] for k in spec_keys) and max(abs(v) for v in steps["range_ends_move"].values()) > 1e-9:
                raise SystemExit(f"[BLOCKED] {end}/{conv}: the range ends move although the corners share their specification")
            whole = sum(new_cols[k] for k in ("cash_bn", "resource_cost_bn", "displaced_bn", "accrual_bn")) - \
                sum(start[k] for k in ("cash_bn", "resource_cost_bn", "displaced_bn"))
            if abs(whole - (change[i] + p1 - p0)) > 1e-6:
                raise SystemExit(f"[BLOCKED] {end}/{conv}: the total moves {whole:.6f}, the set's band change plus P "
                                 f"{change[i] + p1 - p0:.6f}")
            order = sorted(s for s in steps if s.startswith("v4_")) + [
                s for s in ("constant_line_federal_share", "pension_accrual", "range_ends_move") if s in steps]
            for name, cols in [("previous_case", start)] + [(s, steps[s]) for s in order] + [("this_case", new_cols)]:
                rows.append(dict(end=end, convention=conv, step=name, cash_gap_bn=cols["cash_bn"],
                                 cash_federal_bn=cols["cash_federal_bn"],
                                 cash_state_local_bn=cols["cash_bn"] - cols["cash_federal_bn"],
                                 **{k: cols[k] for k in V4_BRIDGE_COLUMNS[2:]}))
    out = pd.DataFrame(rows)
    number = out.select_dtypes("number").columns
    out[number] = out[number].round(6) + 0.0             # no negative zeros in the file
    return out


def pre_existing_gap(wb: Workbook) -> dict:
    """The gap this lane names and does not repair: the engine compounds current spending, which includes
    depreciation (consumption of fixed capital), not gross investment and net capital transfers. The
    federal bridge from current saving to net lending, 2024 (NIPA Table 3.2), is a national diagnostic,
    not a group correction. Gate: the lines add up (0.005, BEA rounds each line to $1m) and give the
    audit's -$1,874.5bn and -$2,106.2bn (0.05)."""
    line = lambda n, label: float(wb.line("T30200-A", n, label)[LAST])  # noqa: E731
    v = dict(net_federal_saving_bn=line(37, "Net federal government saving"),
             capital_transfer_receipts_bn=line(42, "Capital transfer receipts"),
             gross_government_investment_bn=line(45, "Gross government investment"),
             capital_transfer_payments_bn=line(46, "Capital transfer payments"),
             net_purchases_of_nonproduced_assets_bn=line(47, "Net purchases of nonproduced assets"),
             consumption_of_fixed_capital_bn=line(48, "Less: Consumption of fixed capital"),
             net_lending_bn=line(49, "Net lending or net borrowing"))
    built = (v["net_federal_saving_bn"] + v["capital_transfer_receipts_bn"] - v["gross_government_investment_bn"]
             - v["capital_transfer_payments_bn"] - v["net_purchases_of_nonproduced_assets_bn"]
             + v["consumption_of_fixed_capital_bn"])
    if abs(built - v["net_lending_bn"]) > 0.005 or abs(v["net_federal_saving_bn"] + 1874.5) > 0.05 \
            or abs(v["net_lending_bn"] + 2106.2) > 0.05:
        raise SystemExit(f"[BLOCKED] NIPA 3.2's 2024 capital account does not give the audit's bridge ({built}, {v})")
    return dict(v, net_lending_less_saving_bn=v["net_lending_bn"] - v["net_federal_saving_bn"],
                rule="net lending = saving + capital transfer receipts - gross investment - capital transfer "
                     "payments - net purchases of nonproduced assets + consumption of fixed capital",
                note="not repaired: this lane compounds each year's current gap, whose spending includes consumption of "
                     "fixed capital; the federal borrowing for investment and capital transfers beyond depreciation "
                     "(net_lending_less_saving_bn, national) is charged to no group here. A national diagnostic, not a "
                     "group correction (research/immigration-conceptual-audit-2026-09-27.md section 1)",
                source="NIPA Table 3.2 lines 37, 42 and 45-49, 2024 (the pinned Section3All_xls.xlsx)")


def three_column_summary(run: dict, split: pd.DataFrame, added_shares: dict, wb: Workbook,
                         whole_parts: dict, v4_rules: dict | None = None) -> dict:
    """summary.json's September 27 additions: the three columns at each band end and convention, the
    enterprise surplus's own row, the capped programs, the per_spec.csv gates and the pre-existing gap. From
    September 29 (v4_rules) the enterprise surplus takes its share after public housing's split, public housing's
    receipt line is a capped program, and a whole-budget rule the back-cast cannot run yet is named."""
    prof = run["main_profile"]
    main = split[split.profile == prof].set_index(["end", "convention"])
    lines = run["lines"].set_index(["end", "convention", "side", "line"])
    cols = ("fiscal_gap_bn", "federal_bn", "resource_cost_bn", "resource_cost_federal_bn", "displaced_bn",
            "displaced_federal_bn")
    financing = {f"{e}|{c}": {("cash_" + k if k in ("fiscal_gap_bn", "federal_bn") else k): float(main.loc[(e, c), k])
                              for k in cols} for e, c in main.index}
    enterprise = {f"{e}|{c}": dict(gap_bn=float(lines.loc[(e, c, "receipt", ENTERPRISE_RECEIPT), "gap_bn"]),
                                   federal_bn=float(lines.loc[(e, c, "receipt", ENTERPRISE_RECEIPT), "federal_bn"]))
                  for e, c in main.index}
    capped_lines = [("spending", line) for line in CAPPED] + ([("receipt", HOUSING_ENTERPRISE)] if v4_rules else [])
    capped = {line: {f"{e}|{c}": dict(gap_bn=float(lines.loc[(e, c, side, line), "gap_bn"]),
                                      federal_bn=float(lines.loc[(e, c, side, line), "federal_bn"]))
                     for e, c in main.index} for side, line in capped_lines}
    if v4_rules:
        ent = v4_rules["enterprise_surplus"]
        added_shares = dict(added_shares, enterprise_surplus=ent["share"],
                            enterprise_surplus_national_bn_2024=ent["national_bn"])
    whole = dict(
        rule="the back-cast's concept less its capital return and rental assistance (their own series, "
             "historical_backcast_2026_09_20/derived/case_parts_annual.csv) and less LIHEAP, which follows the base "
             "at its 2024 share of the base's fiscal gap; the cash part's 2024 federal share is held",
        window_sums_tn={f"{name}|{rule}": {k: {str(s): float(v.loc[s:LAST].sum()) / 1e3 for s in WINDOW_STARTS}
                                           for k, v in d.items()} for (name, rule), d in sorted(whole_parts.items())})
    if v4_rules and not whole_parts:
        whole["not_run"] = ("[DEGRADED] the whole-budget rules (whole_flat, whole_ratio, whole_income and their "
                            "federal-series variants) are not run for this case; the programme rules are. They take the "
                            "back-cast's concept less the parts that are not cash, and historical_backcast_2026_09_20's "
                            "concept for this case (the set, the pension accrual included, in its derived/sept29/, in "
                            "progress on 2026-09-29) would need its parts by financing column: the capital return, "
                            "rental assistance, public housing and the accrual (backcast_family)")
    return dict(
        profiles={p: dict(lane_profile=b, long_run_lines_take_the_specification=lr)
                  for p, (b, lr) in case_profiles(run["case"]).items()},
        main_profile=prof,
        financing_columns_2024=dict(
            rule="cash: the engine's lines less the capped programs, the only part compounded into debt; resource "
                 "cost: the return on public capital (imputed; federal = its federal components), never compounded; "
                 "displaced beneficiaries: the capped programs, whose slots go to eligible households without the "
                 "group, never compounded. cash + resource cost + displaced = net cost + P",
            main_profile=financing),
        enterprise_surplus_receipt=dict(
            rule="the group's share of the enterprises' current surplus (NIPA 3.1 line 19, net of depreciation, before "
                 "interest) at response 1 on the re-keyed population share: a receipt in the cash gap; federal at "
                 "t32(23)/t31(19); the programme rule carries each level with its own series (NIPA 3.2 line 23, 3.3 "
                 "line 22), not scaled by income" if not v4_rules else
                 "the group's share of the enterprises' current surplus less public housing's deficit (split out to its "
                 "own receipt line) at response 1 on the re-keyed population share: a receipt in the cash gap; federal "
                 "at t32(23) over the line's national total after the split; the programme rule carries the federal "
                 "enterprises with NIPA 3.2 line 23 and the state-local ones without housing with NIPA 3.8 lines 8-12, "
                 "14 and 15, not scaled by income",
            federal_share_2024=added_shares["enterprise_surplus"],
            federal_bn_2024_national=added_shares["enterprise_surplus_federal_bn_2024"],
            national_bn_2024=added_shares["enterprise_surplus_national_bn_2024"], main_profile=enterprise),
        long_run_subfunction_levels_2024=added_shares["subfunction_levels_2024"],
        capped_programs=dict(lines=dict(CAPPED, **({HOUSING_ENTERPRISE: "public housing (receipt line)"} if v4_rules
                                                   else {})), main_profile=capped,
                             rule="counted at response 1 in the annual account; no budget response, so nothing from them "
                                  "is borrowed or compounded; rental assistance is federal, LIHEAP at the lane's "
                                  "energy_assistance share (0 under the low convention)" + (
                                      "; public housing's enterprise deficit at its operating subsidy's federal share "
                                      "(v4_shares)" if v4_rules else "")),
        whole_budget_rules=whole,
        per_spec_gates=run["per_spec"],
        pre_existing_gap=pre_existing_gap(wb))


def member_count() -> float:
    """The headcount the September 29 case prices, millions: audit row 4's union (SEPT29["count"],
    populations.row4), the adopted case's per-member divisor. Gate: the file's published count is the account's
    target (1e-9)."""
    pop = json.loads(SEPT29["count"].read_text())["populations"]
    if abs(pop["published"] / 1e6 - TARGET_M) > 1e-9:
        raise SystemExit(f"[BLOCKED] {SEPT29['count'].name}: the published count is not the account's target")
    return pop["row4"] / 1e6


CENTRAL = dict(rule="programme_income_pandemic_per_head", convention="central", rate_path="effective",
               window_start=2005, financing="all_borrowed")


def v4_summary(run: dict, split: pd.DataFrame, v4_rules: dict, stocks: pd.DataFrame, count_m: float,
               family: str | None) -> dict:
    """summary.json's September 29 additions: the payloads and the port's parity with engine.js, the fourth column
    (the pension accrual) at each end and convention, the rules for the lines the case adds, the headcount, and the
    legacy interest on the central rule for the cash set (main) beside the two alternatives."""
    prof = run["main_profile"]
    main = split[split.profile == prof].set_index(["end", "convention"])
    pick = stocks
    for k, v in CENTRAL.items():
        if k != "convention":
            pick = pick[pick[k] == v]
    central = pick[pick.convention == CENTRAL["convention"]].set_index(["benchmark", "end"])
    cols = ("stock_entering_2024_bn", "legacy_interest_2024_bn", "interest_per_member_usd", "flow_2024_bn")
    headline = {}
    for end in ("low", "high"):
        row = main.loc[(end, CENTRAL["convention"])]
        with_acc, as_cash = central.loc[("main_with_accrual", end)], central.loc[("main_housing_as_cash", end)]
        headline[end] = dict(
            **{k: central.loc[("main", end), k] for k in cols},
            cash_gap_2024_bn=row.fiscal_gap_bn, federal_2024_bn=row.federal_bn, federal_share_2024=row.federal_share,
            resource_cost_2024_bn=row.resource_cost_bn, displaced_2024_bn=row.displaced_bn,
            accrual_2024_bn=row.accrual_bn, accrual_federal_2024_bn=row.accrual_federal_bn,
            set_net_cost_bn=row.net_cost_bn, cash_set_net_cost_bn=row.cash_set_net_cost_bn,
            alternative_set_compounded={k: with_acc[k] for k in cols},
            alternative_public_housing_as_cash={k: as_cash[k] for k in cols})
    payloads = {w: dict(file=str(payload_file(run["case"], w).relative_to(ROOT)), sha256=sha(payload_file(run["case"], w)))
                for w in ("set", "cash")}
    if SEPT29.get("candidate_set"):
        payloads["set"].update(candidate=str((FISCAL / SEPT29["candidate_set"]).relative_to(ROOT)),
                               candidate_sha256=sha(FISCAL / SEPT29["candidate_set"]),
                               rule="the candidate's set but for the adoption's meta stamps " + ", ".join(SEPT29["stamps"]))
    return dict(
        lane=SEPT29["lane"], lane_writes_contract=SEPT29["contract"], payloads=payloads,
        consumer=dict(file=str(SEPT29["consumer"].relative_to(ROOT)), sha256=sha(SEPT29["consumer"]),
                      engine_sha256=sha(FISCAL / "assumption_explorer_2026_09_21/engine.js")),
        engine_parity=run["parity"], oracle=SEPT29["oracle"],
        central=dict(CENTRAL, benchmark="main"),
        headline_2024=headline,
        pension_accrual=dict(
            rule="the set (social security and Medicare Part A at the benefits the group's 2024 payroll taxes earn, at "
                 "payable benefits, net of the tax on benefits) less the cash set (the benefits paid in 2024), line by "
                 "line: social security, Medicare and federal income tax, all federal. A liability that accrues in 2024 "
                 "and is paid later, not a 2024 cash flow, so it is a fourth column and never compounded into debt held "
                 "by the public; the split, the annual flows and the stocks run on the cash set. cash + resource cost + "
                 "displaced + accrual = the set's net cost + P",
            alternative="main_with_accrual: the set compounded, the accrual carried back with its lines' own series as "
                        "if it had been borrowed each year (programme rules only)",
            main_profile={f"{e}|{c}": dict(accrual_bn=main.loc[(e, c), "accrual_bn"],
                                           accrual_federal_bn=main.loc[(e, c), "accrual_federal_bn"],
                                           set_net_cost_bn=main.loc[(e, c), "net_cost_bn"],
                                           cash_set_net_cost_bn=main.loc[(e, c), "cash_set_net_cost_bn"])
                          for e, c in main.index}),
        public_housing=dict(
            rule="public housing's enterprise deficit (receipt line housing_enterprise_surplus, at the rental line's "
                 "key, response 1) is a capped program like rental assistance: its units go to eligible households "
                 "without the group, so there is no budget response and nothing is borrowed (displaced beneficiaries)",
            alternative="main_housing_as_cash: the line in the cash gap, carried with NIPA 3.13 line 4 (its federal "
                        "operating subsidy) and 3.8 line 13 (the state-local deficit), not scaled by income "
                        "(programme rules only)"),
        shares=v4_rules,
        members=dict(count_m=count_m, source=str(SEPT29["count"].relative_to(ROOT)) + " populations.row4",
                     rule="per member: the headcount the account prices (the adopted case's divisor); per-head shares "
                          "(OMB net interest, the debt increase, the pandemic credits) stay at the account's population "
                          "key, TARGET_M / RESIDENTS_M"),
        backcast_concept=family)


def main() -> None:
    parser = argparse.ArgumentParser(description="Debt legacy of past federal gaps on an adopted main case.")
    parser.add_argument("--case", choices=(*reversed(list(LATER_CASES)), "sept24", "sept23"), default=DEFAULT_CASE,
                        help="a case from September 26 on (default: sept27: long-run road and park responses, rental "
                             "assistance, the return on public capital and the enterprises; sept29: the main case of "
                             "2026-09-29, written to derived/sept29/; sept26_schools: schools at full average cost; "
                             "sept26: CBO's one-year school response, 0.63-0.66); sept24: the case adopted 2026-09-24; "
                             "sept23: this lane's first result")
    parser.add_argument("--out-dir", type=Path, default=None,
                        help="default derived/, and derived/<case>/ for a case with two payloads (sept29)")
    args = parser.parse_args()
    framed = args.case != "sept23"          # on the September 24 frame, with a corrections payload
    later = args.case in LATER_CASES        # September 26 on: responses from the payload's meta.responses
    three = later and LATER_CASES[args.case].profiles is not None   # September 27 on: the three columns
    v4 = later and LATER_CASES[args.case].payloads is not None      # September 29 on: the set and the cash set
    pins = check_pins()
    wb = Workbook(BEA / "Section3All_xls.xlsx")
    responses, gg_components, added_shares = None, None, None
    if later:
        responses = case_payload(args.case)["meta"]["responses"]
        gg_components = finite_components(responses)
        shares, extras = federal_shares(wb, Grants(), *gg_components)
        if three:
            added_shares = dict(case_shares(shares, wb), subfunction_levels_2024=subfunction_levels(responses, extras))
    else:
        shares, extras = federal_shares(wb, Grants())
    # The case's shares: from September 29 a copy with the lines it adds (v4_shares); the earlier cases a run
    # rebuilds for its bridges keep `shares`.
    run_shares, v4_rules, cash_meta = shares, None, None
    if v4:
        cash_payload = case_payload(args.case, "cash")
        cash_meta = cash_payload["meta"]
        run_shares, v4_rules = v4_shares(shares, extras, wb, apply_corrections(MODEL, cash_payload), cash_meta)
    jf = justice_federal(wb)
    ucf = uncompensated_federal(float(shares["central"].loc[LAST, "medicaid_and_chip_other_medical"]))
    hist = History(wb)
    control_gap = programme_control(hist)
    rates = rate_paths()
    out = args.out_dir or (HERE / "derived" / args.case if v4 else HERE / "derived")
    out.mkdir(parents=True, exist_ok=True)

    # 1. The 2024 split of the adopted fiscal gap, at the corners that set each band. On September 24
    # each correction is split by its line's government level too, and the parts must add to the
    # change in the whole split at the same specification. From September 26 on the same holds at each
    # case's responses, with the September 26 payload's two new corrections as components of their own
    # (later cases carry the same edits; case_payload gates it).
    COMPONENTS.clear()
    if later:
        first = case_payload(next(iter(LATER_CASES)))
        COMPONENTS.update(sept26_components(json.loads(CORRECTIONS_FILE.read_text()), first))
        # September 27 on: the enterprise receipt's re-key, a component of its own (from September 29 the previous
        # case's; the case's own parts are v4_components).
        rekeyed = previous_case(args.case) if v4 else args.case
        COMPONENTS["edits"] = COMPONENTS["edits"] + [dict(component="enterprise_rekey", **e)
                                                     for e in rekey_edits(case_payload(rekeyed), first)]
    elif framed:
        COMPONENTS.update(json.loads(COMPONENTS_FILE.read_text()))
    run = case_split(args.case, run_shares, extras, jf, ucf)
    anchors, parts, split, corrected, main_summary = (run[k] for k in ("anchors", "parts", "split", "corrected",
                                                                        "main_summary"))
    split.round(6).to_csv(out / "federal_split_2024.csv", index=False)
    run["lines"].round(6).to_csv(out / "federal_split_2024_lines.csv", index=False)
    if framed:
        corrections = run["corrections"]
        corrections.round(6).to_csv(out / "corrections_federal_split_2024.csv", index=False)
        by_component = corrections.assign(component=corrections.component.str.split(":").str[0]).groupby(
            ["end", "convention", "component"] + (["financing"] if three else []),
            sort=True)[["effect_bn", "federal_bn", "state_local_bn"]].sum()
        by_component["federal_share"] = by_component.federal_bn / by_component.effect_bn
        by_component.round(6).to_csv(out / "corrections_federal_by_component_2024.csv")
    if later:
        # One bridge per step up to this case: September 24 -> 26 (sept26_bridge), then each later case
        # from the one before (response_bridge; capital_bridge into a case with profiles of its own), each
        # rerun here so every bridge file matches this run.
        chain = list(LATER_CASES)[:list(LATER_CASES).index(args.case) + 1]
        runs = {args.case: run}
        for i, case in enumerate(chain):
            if case not in runs:
                runs[case] = case_split(case, shares, extras, jf, ucf)
            if i == 0:
                extras24 = federal_shares(wb, Grants())[1]       # general government at the elasticities
                r0 = runs[case]
                bridge = sept26_bridge(r0["anchors"][MAIN], shares, extras, extras24, jf, ucf, r0["corrections"],
                                       r0["main_summary"], r0["split"])
            elif LATER_CASES[case].payloads:
                bridge = v4_bridge(runs[chain[i - 1]], runs[case], shares, run_shares, extras, jf, ucf, cash_meta)
            elif LATER_CASES[case].profiles:
                bridge = capital_bridge(runs[chain[i - 1]], runs[case], shares, extras, jf, ucf)
            else:
                bridge = response_bridge(runs[chain[i - 1]], runs[case], shares, extras, jf, ucf)
            bridge.round(6).to_csv(out / f"{case}_bridge_2024.csv", index=False)

    # 2. Annual federal gaps by benchmark, rule, anchor and convention (real 2024 $bn and nominal). The
    # every-service-proportional benchmark charges no interest either, so it gets its own legacy line.
    annual_rows, audit_rows, rtc_keys = [], [], {}

    def record(bench, rule, end, conv, gap, fed):
        nominal = hist.nominal(fed)
        for year in YEARS:
            annual_rows.append(dict(benchmark=bench, rule=rule, end=end, convention=conv, year=year,
                                    fiscal_gap_real_bn=gap[year], federal_real_bn=fed[year],
                                    federal_nominal_bn=nominal[year],
                                    federal_share=fed[year] / gap[year] if gap[year] else np.nan))

    def windows(bench, end, rule, method, gap, p_t):
        """Back-cast concept (net cost to other residents = fiscal gap - P), real 2024 $tn."""
        for start in WINDOW_STARTS:
            audit_rows.append(dict(benchmark=bench, end=end, rule=rule, receipts_method=method, window_start=start,
                                   net_cost_tn=float((gap - p_t).loc[start:LAST].sum()) / 1e3,
                                   fiscal_gap_tn=float(gap.loc[start:LAST].sum()) / 1e3))

    fed_rec = wb.line("T30200-A", 1, "Current receipts")
    fed_exp = wb.line("T30200-A", 24, "Current expenditures")
    residents = hist.people.reindex(YEARS) * 1e3 * (RESIDENTS_M * 1e6 / (hist.people[LAST] * 1e3))
    r_f = fed_rec * 1e9 * hist.real / residents
    s_f = fed_exp * 1e9 * hist.real / residents
    indirect = indirect_receipt_shares(wb)
    n = hist.group
    # The back-cast's concepts for the case: Sept 24 re-run in da2b107, later cases from its LATER_CASES. A case the
    # back-cast does not carry yet (None) runs the programme rules only; summary.json names what is not run.
    family = backcast_family(args.case) if framed else None
    main_prof = run["main_profile"]
    benchmarks = ({"main": (main_prof, f"net_cost_cbo_informed_{family}" if family else None),
                   "proportional": ("proportional_reference", f"net_cost_full_proportional_{family}" if family else None)}
                  if framed else BENCHMARKS)
    # September 29: the cash set is compounded (main, proportional). Two alternatives beside, programme rules only:
    # the set compounded, the pension accrual carried with its lines as if it were borrowed (main_with_accrual), and
    # public housing's enterprise deficit as cash instead of displaced beneficiaries (main_housing_as_cash).
    bench_anchors = {bench: anchors[prof] for bench, (prof, _) in benchmarks.items()}
    if v4:
        benchmarks.update(main_with_accrual=(main_prof, None), main_housing_as_cash=(main_prof, None))
        bench_anchors["main_with_accrual"] = run["set_anchors"][main_prof]
        bench_anchors["main_housing_as_cash"] = {
            end: dict(c, capped=[x for x in c["capped"] if x != HOUSING_ENTERPRISE]) for end, c in anchors[main_prof].items()}
    series_kw = dict(series=RECEIPT_SERIES_V4, signed_receipts=SIGNED_RECEIPTS_V4) if v4 else {}
    main_lines = run["lines"].set_index(["end", "convention", "side", "line"])

    def anchor_2024(bench: str, end: str, conv: str, row: pd.Series) -> tuple[float, float]:
        """The 2024 cash gap and federal part a benchmark's programme rule must reproduce: the split's cash columns,
        plus the accrual (main_with_accrual) or public housing's line (main_housing_as_cash)."""
        gap, fed = float(row.fiscal_gap_bn), float(row.federal_bn)
        if bench == "main_with_accrual":
            return gap + float(row.accrual_bn), fed + float(row.accrual_federal_bn)
        if bench == "main_housing_as_cash":
            h = main_lines.loc[(end, conv, "receipt", HOUSING_ENTERPRISE)]
            return gap + float(h.gap_bn), fed + float(h.federal_bn)
        return gap, fed
    parts_annual = pd.read_csv(BACKCAST_PARTS) if three and family else None
    whole_parts = {}

    def cash_whole(column: str, end: str, rule: str, corner: dict, p: float, p_t: pd.Series, row: pd.Series) -> pd.Series:
        """A whole-budget rule's cash gap by year (September 27 on): the back-cast's concept plus P, less
        the capital return and rental assistance, each carried back by its own series (the back-cast's
        case_parts_annual.csv), and less LIHEAP, which sits in the base and follows it at its 2024 share of
        the base's fiscal gap. Gates: the parts add to the concept (1e-3, the file's rounding) and the 2024
        values are this split's cash, resource cost and displaced beneficiaries (1e-3)."""
        name = f"{column}_{end}"
        k = parts_annual[(parts_annual.concept == name) & (parts_annual.rule == rule)].pivot(
            index="year", columns="part", values="value_bn").reindex(YEARS)
        total = hist.annual[f"{name}__{rule}"].reindex(YEARS)
        if k.isna().any().any() or (k.sum(axis=1) - total).abs().max() > 1e-3:
            raise SystemExit(f"[BLOCKED] {BACKCAST_PARTS.name}: {name}/{rule} parts do not add to the back-cast's concept")
        t = lines_at(corner).set_index(["side", "id"])
        liheap = float(t.responsive_bn[("spending", "energy_assistance")])
        resource = k[list(CAPITAL_PARTS)].sum(axis=1)
        displaced = k.rental_assistance + liheap / (k.base[LAST] + p) * (k.base + p_t)
        cash = total + p_t - resource - displaced
        for got, want in ((cash, row.fiscal_gap_bn), (resource, row.resource_cost_bn), (displaced, row.displaced_bn)):
            if abs(got[LAST] - want) > 1e-3:
                raise SystemExit(f"[BLOCKED] {name}/{rule}: the 2024 parts are not this split's ({got[LAST]} vs {want})")
        whole_parts[(name, rule)] = dict(resource=resource, displaced=displaced)
        return cash
    for bench, (prof, column) in benchmarks.items():
        bench_split = split[split.profile == prof].set_index(["end", "convention"])
        for end, corner in bench_anchors[bench].items():
            p, _ = production(corner["normalization"], corner.get("model"))
            p_t = p * n / n[LAST]
            shared_receipts = lines_at(dict(corner, allocation="shared"))
            shared_receipts = shared_receipts[shared_receipts.side == "receipt"].set_index("id").amount_bn
            for conv in CONVENTIONS:
                prog = programme_federal(hist, corner, end, conv, run_shares, extras, jf, ucf, parts.get((prof, end, conv)),
                                         **series_kw)
                want_gap, want_fed = anchor_2024(bench, end, conv, bench_split.loc[(end, conv)])
                if abs(prog.loc[LAST, "gap_programme"] - want_gap) > 1e-6 or \
                        abs(prog.loc[LAST, "federal_programme"] - want_fed) > 1e-6:
                    raise SystemExit(f"[BLOCKED] {bench} programme back-cast {end}/{conv} does not reproduce 2024")
                if abs(prog.loc[LAST, "gap_programme_grouped"] - prog.loc[LAST, "gap_programme"]) > 1e-9 or \
                        prog.rtc_excess.drop([2020, 2021, 2022]).abs().max() > 1e-9:
                    raise SystemExit(f"[BLOCKED] {bench} {end}/{conv}: audit or per-head variant moves another year")
                rtc_keys[f"{bench}_{end}"] = prog.attrs["rtc_key_share"]
                ph, ph_fed = prog.rtc_excess, prog.rtc_excess_fed
                variants = {  # rule: (fiscal gap, federal part, fiscal gap with the September 20 receipts)
                    "programme": (prog.gap_programme, prog.federal_programme, prog.gap_programme_grouped),
                    "programme_income": (prog.gap_income, prog.federal_income, prog.gap_income_grouped),
                    "programme_ex_pandemic": (ex_pandemic(prog.gap_programme), ex_pandemic(prog.federal_programme),
                                              ex_pandemic(prog.gap_programme_grouped)),
                    "programme_income_ex_pandemic": (ex_pandemic(prog.gap_income), ex_pandemic(prog.federal_income),
                                                     ex_pandemic(prog.gap_income_grouped)),
                    "programme_pandemic_per_head": (prog.gap_programme - ph, prog.federal_programme - ph_fed,
                                                    prog.gap_programme_grouped - ph),
                    "programme_income_pandemic_per_head": (prog.gap_income - ph, prog.federal_income - ph_fed,
                                                           prog.gap_income_grouped - ph)}
                for rule, (gap, fed, grouped) in variants.items():
                    record(bench, rule, end, conv, gap, fed)
                    if conv == "central":
                        windows(bench, end, rule, "own_series", gap, p_t)
                        windows(bench, end, rule, "grouped", grouped, p_t)
                phi = bench_split.loc[(end, conv), "federal_share"]
                fgap = bench_split.loc[(end, conv), "federal_bn"]
                if column is None:              # no back-cast concept for this benchmark: programme rules only
                    continue
                # Whole-budget rules hold the 2024 split (the brief's rule where no category series exists).
                # From September 27 they hold the cash part's split, on the cash part of the concept.
                row = bench_split.loc[(end, conv)]
                whole = {rule: (cash_whole(column, end, rule, corner, p, p_t, row) if three
                                else hist.annual[f"{column}_{end}__{rule}"].reindex(YEARS) + p_t)
                         for rule in ("flat", "ratio", "income")}
                for rule in ("flat", "ratio", "income"):
                    gap = whole[rule]
                    record(bench, f"whole_{rule}", end, conv, gap, phi * gap)
                    if conv == "central":
                        windows(bench, end, f"whole_{rule}", "whole_budget", gap, p_t)
                # Sensitivity: the federal part follows federal receipts and expenditure per capita instead.
                receipt_shares = pd.Series({i: (run_shares[conv].loc[LAST, i] if i in run_shares[conv].columns
                                                else indirect[i]) for i in shared_receipts.index})
                fr = float((shared_receipts * receipt_shares).sum())
                rho = fr * 1e9 / (n[LAST] * 1e6) / r_f[LAST]
                sigma = (fgap + fr) * 1e9 / (n[LAST] * 1e6) / s_f[LAST]
                for rule, scale in (("ratio", 1.0), ("income", hist.income)):
                    fed = n * 1e6 * (sigma * s_f - rho * scale * r_f) / 1e9
                    if abs(fed[LAST] - fgap) > 1e-6:
                        raise SystemExit("[BLOCKED] federal-series rule does not reproduce its 2024 anchor")
                    record(bench, f"whole_{rule}_federal_series", end, conv, whole[rule], fed)
    annual = pd.DataFrame(annual_rows)
    annual.round(6).to_csv(out / "federal_gap_annual.csv", index=False)
    pd.DataFrame(audit_rows).round(6).to_csv(out / "adopted_backcast_windows.csv", index=False)

    # 3. Stocks and 2024 legacy interest for every specification. The account's interest row (BEA
    # domestic interest, per head, zero response) and the group's per-head share of OMB net interest
    # are the two benchmarks the legacy line is compared with, never added to.
    interest_row = next(l for l in (corrected if framed else MODEL)["spending"]["lines"] if l["id"] == "domestic_interest")
    row_allocation = interest_row["keys"][interest_row["preferred_key"]]["personal"]["target_bn"]
    # Per member: the account's target (40.9m) through September 27; from September 29 the headcount the account
    # prices (audit row 4's union, the adopted case's per-member divisor). The per-head shares stay at the account's
    # population key, TARGET_M / RESIDENTS_M, as its population-keyed lines and the back-cast's group series do.
    count_m = member_count() if v4 else TARGET_M
    per_head_net_interest = rates.loc[LAST, "net_interest_bn"] * TARGET_M / RESIDENTS_M
    # Scale reference only: the group's per-head share of each year's increase in debt held by the public.
    public_debt = omb_debt_held_by_public()
    per_head_increase = sum(TARGET_M / RESIDENTS_M * hist.share[t] * (public_debt[t] - public_debt[t - 1])
                            for t in range(FIRST, LAST))
    stock_rows = []
    debt_end_2023 = rates.loc[2023, "debt_held_by_public_bn"]
    for (bench, rule, end, conv), block in annual.groupby(["benchmark", "rule", "end", "convention"], sort=True):
        nominal = block.set_index("year").federal_nominal_bn
        for rate_name in ("effective", "constant_3_22", "treasury_10y", "gross_public_securities"):
            for start in WINDOW_STARTS:
                for financing, borrowed in (("all_borrowed", 1.0), ("half_borrowed", 0.5)):
                    st = stock(nominal, rates[rate_name], start, borrowed)
                    interest = st["legacy_interest_2024_bn"]
                    stock_rows.append(dict(
                        benchmark=bench, rule=rule, end=end, convention=conv, rate_path=rate_name,
                        window_start=start, financing=financing, **st,
                        stock_share_of_debt_end_fy2023=st["stock_entering_2024_bn"] / debt_end_2023,
                        interest_per_member_usd=interest * 1e9 / (count_m * 1e6),
                        interest_per_other_resident_usd=interest * 1e9 / ((RESIDENTS_M - count_m) * 1e6),
                        interest_share_of_fy2024_net_interest=interest / rates.loc[LAST, "net_interest_bn"],
                        interest_share_of_account_interest_allocation=interest / row_allocation,
                        interest_share_of_per_head_net_interest=interest / per_head_net_interest))
    pd.DataFrame(stock_rows).round(6).to_csv(out / "stocks.csv", index=False)
    rates.round(6).to_csv(out / "rates.csv", index_label="fiscal_year")

    # 3b. Rule 5 sensitivity: omitted and proposed fiscal benefits would reduce F_t. Carried back by
    # group size in real terms; the stock is linear, so these rows subtract from any rule's stock.
    benefits = proposed_benefits(float(extras["labour_share"][LAST]),
                                 float(shares["central"].loc[LAST, "medicaid_and_chip_other_medical"]),
                                 include_care=not framed)   # since September 24 care is inside the account
    benefit_rows = []
    names = ("mobility", "mobility_and_scale") if framed else ("care_and_mobility", "care_mobility_and_scale")
    for name, fed_2024 in ((names[0], benefits["federal_omitted_bn"]),
                           (names[1], benefits["federal_with_scale_bn"])):
        nominal = hist.nominal(fed_2024 * hist.group / hist.group[LAST])
        for start in WINDOW_STARTS:
            st = stock(nominal, rates["effective"], start, 1.0)
            benefit_rows.append(dict(benefit_set=name, federal_2024_bn=fed_2024, window_start=start,
                                     stock_reduction_bn=st["stock_entering_2024_bn"],
                                     interest_reduction_2024_bn=st["legacy_interest_2024_bn"],
                                     interest_reduction_per_member_usd=st["legacy_interest_2024_bn"] * 1e9
                                     / (count_m * 1e6)))
    pd.DataFrame(benefit_rows).round(6).to_csv(out / "benefit_sensitivity.csv", index=False)

    # 4. Federal shares by line and year, for audit.
    long = [dict(convention=conv, line=col, year=year, federal_share=run_shares[conv].loc[year, col])
            for conv in CONVENTIONS for col in run_shares[conv].columns if col != "_enterprise_federal_bn"
            for year in YEARS]
    pd.DataFrame(long).round(6).to_csv(out / "federal_shares_by_year.csv", index=False)

    # 5. Forward counterpart: ladder 137's constant-flow path (a constant nominal flow borrowed at year
    # end at a constant rate) on the adopted federal flow; the whole gap is ladder 137's convention.
    def forward(f: float, r: float, years: int) -> tuple[float, float, float]:
        debt = f * ((1 + r) ** years - 1) / r
        return debt, debt - years * f, f * ((1 + r) ** (years - 1) - 1)

    for years, want in LADDER137_TABLE.items():      # README rounds to $1bn and the flow to $0.01bn
        if max(abs(a - b) for a, b in zip(forward(LADDER137_FLOW, LADDER137_RATE, years), want)) > 1.0:
            raise SystemExit(f"[BLOCKED] forward formula does not reproduce ladder 137 at year {years}")
    main_split = split[split.profile == main_prof].set_index(["end", "convention"])
    fwd = []
    for end in ("low", "high"):
        for conv, part in [(c, "federal") for c in CONVENTIONS] + [("none", "whole_gap")]:
            column = "federal_bn" if part == "federal" else "fiscal_gap_bn"
            flow = float(main_split.loc[(end, "central" if conv == "none" else conv), column])
            for financing, borrowed in (("all_borrowed", 1.0), ("half_borrowed", 0.5)):
                f, r = flow * borrowed, LADDER137_RATE
                for years in (10, 20, 30):
                    debt, component, bill = forward(f, r, years)
                    fwd.append(dict(end=end, part=part, convention=conv, financing=financing, rate=r, years=years,
                                    flow_bn=f, debt_bn=debt, interest_component_bn=component,
                                    interest_bill_in_year_bn=bill))
    pd.DataFrame(fwd).round(6).to_csv(out / "forward_path.csv", index=False)

    def plain(value):
        if isinstance(value, dict):
            return {k: plain(v) for k, v in value.items()}
        return float(value) if isinstance(value, (np.floating, float, int)) and not isinstance(value, bool) else value

    summary = dict(inputs=pins, programme_control_max_abs_diff_bn=control_gap, justice_federal=plain(jf),
                   uncompensated_federal=plain(ucf),
                   anchors={end: plain({k: v for k, v in c.items()
                                        if k not in ("shift", "model", "capital_meta", "subfunction_rows")})
                            for end, c in anchors[main_prof].items()},
                   medicaid_federal_share_nhea_2024=float(extras["nhea_share"][LAST]),
                   income_security_matching_fraction_2024=float(extras["matching_fraction"][LAST]),
                   induced_receipts_federal_share_2024=float(extras["labour_share"][LAST]),
                   gps_federal_fraction_2024={c: [float(a[LAST]), float(b[LAST])]
                                              for c, (a, b) in extras["gps"].items()},
                   refundable_credit_key_share_2024=plain(rtc_keys), per_head_share=TARGET_M / RESIDENTS_M,
                   proposed_benefits=plain(benefits), account_interest_row_bn=float(interest_row["national_bn"]),
                   account_interest_allocation_bn=float(row_allocation),
                   per_head_share_of_omb_net_interest_bn=float(per_head_net_interest),
                   per_head_share_of_debt_increase_fy2005_2023_bn=float(per_head_increase),
                   debt_increase_fy2005_2023_bn=float(public_debt[LAST - 1] - public_debt[FIRST - 1]),
                   rate_2024={"omb_net_interest_over_average_debt": float(rates.loc[LAST, "effective"]),
                              "public_securities_interest_over_average_debt":
                                  float(rates.loc[LAST, "gross_public_securities"]),
                              "ladder137": LADDER137_RATE})
    if framed:
        first = next(iter(LATER_CASES))
        lanes = (SHELTER_PARTS, SHELTER_KEYING, CARE_SUMMARY) + ((CK_PAYLOADS, R_VALUES) if later else ()) + (
            (case_file(first, "corrections.json"),) if later and args.case != first else ())
        # September 29 without the lane's September 27 contract: the band is engine.js's through the payload consumer.
        bands_source = (SEPT29["consumer"] if v4 and main_summary is None
                        else case_file(args.case, "summary.json") if later else MAIN24_SUMMARY)
        summary["case"] = dict(
            name=LATER_CASES[args.case][1] if later else "main case adopted 2026-09-24",
            bands_source=str(bands_source.relative_to(ROOT)),
            corrections_sha256=sha(payload_file(args.case) if later else CORRECTIONS_FILE),
            package_components_sha256=sha(COMPONENTS_FILE),
            lane_sha256={str(p.relative_to(ROOT)): sha(p) for p in lanes},
            band=main_summary["main_case"] if main_summary is not None else run["parity"]["set"]["band_bn"],
            corrections_2024=plain({f"{e}|{c}": dict(effect_bn=float(g.effect_bn.sum()), federal_bn=float(g.federal_bn.sum()))
                                    for (e, c), g in cash_part(corrections).groupby(["end", "convention"])}))
        if later:
            summary["case"].update(
                responses=plain(responses), consumption_key_spec=COMPONENTS["meta"]["consumption_key_spec"],
                general_government_low_end_components=dict(zip(("federal_tax_collection", "state_local"),
                                                               map(float, gg_components))))
        if three:
            summary["case"].update(three_column_summary(run, split, added_shares, wb, whole_parts, v4_rules))
            contract = (case_file(args.case, "per_spec.csv"), case_file(args.case, "main_case_bands.csv")) \
                if main_summary is not None else ()
            summary["case"]["lane_sha256"].update({str(q.relative_to(ROOT)): sha(q) for q in (
                *contract, *((BACKCAST_PARTS,) if family else ()))})
        if v4:
            summary["case"]["v4"] = plain(v4_summary(run, split, v4_rules, pd.DataFrame(stock_rows), count_m, family))
    (out / "summary.json").write_text(json.dumps(summary, indent=1, sort_keys=True) + "\n")
    print(split[split.profile == main_prof].round(3).to_string(index=False))
    print(f"programme control max |diff| {control_gap:.6f}bn")


if __name__ == "__main__":
    main()
