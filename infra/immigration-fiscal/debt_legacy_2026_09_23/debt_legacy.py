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
account's split). sept26, the default since 2026-09-26, is the main case adopted that day: the same
frame with main_case_2026_09_26/derived/corrections.json and the responses in its meta.responses
(general government 0.6000/0.8504, schools 0.6522/0.6813), gated to its bands and to the uncorrected
model at those responses. General government's federal fraction at the low end is composed from
the finite-removal responses of its components, r = [1 - (1 - s)^b] / s (federal tax collection
b = 0.789, state-local b = 0.842). The two new corrections split like the rest: audit row 8's change
as row 8 does, the consumption key's edits by the government level of their lines (see
sept26_components). sept23 and sept24 reproduce this lane's outputs of those dates byte for byte.

Run from the repository root:
  OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/debt_legacy_2026_09_23/debt_legacy.py
  ... debt_legacy.py --case sept24 --out-dir <dir>      # the September 24 result (sept23 likewise)
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import io
import json
import re
from itertools import product
from pathlib import Path

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
# The September 26 case: its payload (responses in meta.responses), bands, the finite-removal lane's
# per-component elasticities and the consumption-key lane's edits.
CORRECTIONS26_FILE = FISCAL / "main_case_2026_09_26/derived/corrections.json"
MAIN26_SUMMARY = FISCAL / "main_case_2026_09_26/derived/summary.json"
R_VALUES = FISCAL / "finite_response_2026_09_26/derived/r_values.json"
CK_PAYLOADS = FISCAL / "consumption_key_2026_09_24/derived/payloads.json"
COMPONENTS: dict = {}                     # the running case's payload by component (set in main())
SHELTER_PARTS = FISCAL / "migrant_shelter_costs_2026_09_23/derived/account_keying_parts.csv"
SHELTER_KEYING = FISCAL / "migrant_shelter_costs_2026_09_23/derived/account_keying.csv"
CARE_SUMMARY = FISCAL / "care_household_services_2026_09_23/derived/summary.csv"
UC_KEYS = {"uninsured_use_low": "equal_low", "uninsured_use_high": "equal_high"}
SYNTHETIC_CARRY = {"school_reprice": "education_services", "college_rekey": "education_services"}


def apply_corrections(model: dict, payload: dict) -> dict:
    """engine.js applyCorrections(): add the synthetic lines, then move each edit's dollars into the
    group's target (other residents' share moves the other way, so national totals hold)."""
    m = copy.deepcopy(model)
    zero = lambda: dict(target_bn=0.0, other_bn=0.0, share=0.0)
    for line in payload["lines"]:
        if any(x["id"] == line["id"] for x in m["spending"]["lines"]):
            raise SystemExit(f"[BLOCKED] correction line exists already: {line['id']}")
        m["spending"]["lines"].append(dict(id=line["id"], family=line["family"], national_bn=0.0,
                                           response_class=line["response_class"], label=line["label"],
                                           preferred_key="k", alternative_key="k",
                                           keys={"k": {"personal": zero(), "shared": zero()}}))
    for e in payload["edits"]:
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
    return m
PROD_DIMS = ["proxy", "split", "normalization", "labor_share", "sigma", "capital_adjustment",
             "labor_supply_elasticity", "capital_tax_retention", "excluded_capital_owner_share"]
PROFILES = {"cbo_category_lag_non_school_full": dict(other_edu=1.0, delayed=0.0, school=(0.63, 0.66)),
            "cbo_category_lag_non_school_fixed": dict(other_edu=0.0, delayed=0.0, school=(0.63, 0.66)),
            "proportional_reference": dict(other_edu=1.0, delayed=1.0, school=(1.0,))}
MAIN = "cbo_category_lag_non_school_full"
BENCHMARKS = {"main": (MAIN, "net_cost_cbo_informed_adopted"),          # profile, back-cast column prefix
              "proportional": ("proportional_reference", "net_cost_full_proportional_adopted")}
WINDOW_STARTS = (2005, 2010, 2015)


def production(normalization: str) -> tuple[float, float]:
    """(P, F) at the account's reference production dims, the one the main case uses."""
    ref = dict(MODEL["production"]["reference"], normalization=normalization)
    index = 0
    for d in PROD_DIMS:
        levels = MODEL["production"]["dims"][d]
        hits = [i for i, v in enumerate(levels)
                if v == ref[d] or (not isinstance(v, str) and not isinstance(ref[d], str) and abs(v - ref[d]) < 1e-9)]
        index = index * len(levels) + hits[0]
    return MODEL["production"]["private_wtp_bn"][index], MODEL["production"]["induced_receipts_bn"][index]


SCHOOL_SHARES = sorted({p["school_share"] for p in MODEL["service"]["profiles"] if p["school_share"] > 0})
SCHOOL_SHARES = [SCHOOL_SHARES[0], SCHOOL_SHARES[-1]]


def lines_at(corner: dict) -> pd.DataFrame:
    """Every account line at one corner: target amount, response, responsive amount ($bn, 2024).

    A corner may carry its own model (the corrected one) and key overrides (the September 24 frame);
    without them it is the September 23 corner: preferred keys plus explicit shifts."""
    model, keys = corner.get("model", MODEL), corner.get("keys", {})
    alloc, rows = corner["allocation"], []
    for line in model["receipts"]["lines"]:
        cell = line["cells"][model["receipts"]["reference"]][alloc]
        response = 1.0 if cell["direct"] else 0.0
        rows.append(dict(side="receipt", id=line["id"], national_bn=line["national_bn"],
                         amount_bn=cell["target_bn"], response=response))
    for line in model["spending"]["lines"]:
        cell = line["keys"][keys.get(line["id"], line["preferred_key"])][alloc]
        amount = cell["target_bn"] + corner["shift"].get(line["id"], 0.0)
        c = line["response_class"]
        s = corner["school_share"]
        if c == "household_transfer":
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
    p, f = production(corner["normalization"])
    return p + direct + f


def corners(profile: str, gg: float, justice: float, uc: float) -> list[dict]:
    spec = PROFILES[profile]
    out = []
    for alloc, norm, share, school in product(("personal", "shared"), ("cash", "gdp"), SCHOOL_SHARES, spec["school"]):
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


def frame_corners(profile: str, model: dict, responses: dict | None = None) -> list[dict]:
    """The September 24 frame (package.cjs MAIN_SPECS): 64 specifications for the main profile, justice
    on the use key, Medicaid on the two uninsured-use keys, general government 0.59 or 0.84. The Sept 23
    changes sit in those keys; `justice` and `uc` record how much, for the federal split.

    With responses (a payload's meta.responses) general government takes their low and high values
    and the CBO school coefficients 0.63 and 0.66 their growth and decline values (September 26); a
    profile whose schools respond in full keeps 1.0."""
    spec, gg = PROFILES[profile], INPUTS["general_government_response"]
    schools = spec["school"]
    if responses is not None:
        gg = responses["general_government"]
        swap = {0.63: responses["school"]["growth"], 0.66: responses["school"]["decline"], 1.0: 1.0}
        schools = tuple(swap[v] for v in schools)
    out = []
    for alloc, norm, share, school, g, uc in product(("personal", "shared"), ("cash", "gdp"), SCHOOL_SHARES,
                                                    schools, (gg["low"], gg["high"]), tuple(UC_KEYS)):
        out.append(dict(profile=profile, allocation=alloc, normalization=norm, school_share=share,
                        school_response=school, other_edu=spec["other_edu"], delayed=spec["delayed"], gg=g,
                        gg_end="low" if g == gg["low"] else "high", uc_key=uc, uc_arm=UC_KEYS[uc],
                        justice=INPUTS["justice_change_bn"]["central"], uc=INPUTS["uncompensated_inside_bn"][UC_KEYS[uc]],
                        shift={}, keys={"public_order_safety": "use", MEDICAID: uc}, model=model))
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


def sept26_anchors(profile: str, corrected: dict, main26: dict, responses: dict) -> dict[str, dict]:
    """Corners that set the September 26 band: the same frame at the adopted responses. Gates: the
    uncorrected model reproduces main_case_2026_09_26's uncorrected_at_adopted_responses band and the
    corrected model its adopted band (summary.json, 1e-6)."""
    want = {"corrected": main26["main_case"], "uncorrected": main26["uncorrected_at_adopted_responses"]}
    if profile != MAIN:
        other = main26["other_profiles"][profile]
        want = {"corrected": other["adopted"], "uncorrected": other["uncorrected_at_adopted_responses"]}
    return frame_anchors(profile, corrected, want, responses)


def frame_anchors(profile: str, corrected: dict, want: dict, responses: dict | None = None) -> dict[str, dict]:
    """The band's corners on the frame, gated against the published uncorrected and corrected bands."""
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
        cs = frame_corners(profile, model, responses)
        lo, hi = max(cs, key=welfare), min(cs, key=welfare)
        got = [-welfare(lo), -welfare(hi)]
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

    extras = dict(nhea_share=nhea_share, resid_health=resid_health, block_health=block_health,
                  matching_fraction=matching_fraction, liheap=liheap,
                  is_resid=is_resid, is_base=is_base, gps=gps, k12_ratio=k12_ratio, labour_share=labour_share,
                  odsc_total=odsc_fed + odsc_sl, sl_gps_grant_share=pro_rata("gps"))
    return out, extras


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

def split_corner(corner: dict, shares: pd.DataFrame, extras: dict, conv: str, year: int,
                 jf: dict, ucf: dict, end: str, parts: list | None = None) -> pd.DataFrame:
    t = lines_at(corner)
    phi = shares.loc[year]
    rows = []
    for r in t.itertuples():
        if r.responsive_bn == 0:
            continue
        sign = 1.0 if r.side == "spending" else -1.0     # gap = spending - receipts
        amount = r.responsive_bn
        if r.id == "general_public_services":
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
        else:
            if r.id not in phi.index:
                raise SystemExit(f"[BLOCKED] no federal share for responsive line {r.id}")
            fed = amount * phi[r.id]
        rows.append(dict(side=r.side, id=r.id, responsive_bn=sign * amount, federal_bn=sign * fed))
    p, f = production(corner["normalization"])
    rows.append(dict(side="production", id="induced_receipts_F", responsive_bn=-f,
                     federal_bn=-f * phi["_induced_receipts"]))
    out = pd.DataFrame(rows)
    out["state_local_bn"] = out.responsive_bn - out.federal_bn
    return out


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
    gg_used = 0.59 if a == "shared" else 0.84
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
        share = (gps_lo if gg_used == 0.59 else gps_hi) if line == "general_public_services" else phi[line]
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
                     parts: list) -> pd.DataFrame:
    """Each correction's effect on the gap at one corner, split by the government level of its line.

    Effect = the line's response at the corner x the edit in the evaluated cell (receipts: the
    reference incidence rule; spending: the key the frame evaluates). The share is the one
    split_corner() applies to that line, so the parts add to the change in the whole split."""
    comp = COMPONENTS
    t = lines_at(corner).set_index("id")
    model, keys, a = corner["model"], corner["keys"], corner["allocation"]
    phi = shares.loc[year]
    evaluated = {l["id"]: keys.get(l["id"], l["preferred_key"]) for l in model["spending"]["lines"]}
    rows = []
    for e in comp["edits"]:
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
        if line == "general_public_services":
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
        else:
            share = phi[line]
        rows.append(dict(component=e["component"], side=e["side"], line=line,
                         cell=e["scenario"] if e["side"] == "receipt" else e["key"],
                         effect_bn=effect, federal_bn=effect * share))
    for p in parts:
        rows.append(dict(component=p.get("component", f"lane_constants:{p['part']}"), side="spending", line=p["sub"],
                         cell="k", effect_bn=p["amount"], federal_bn=p["amount"] * p["share"][year]))
    out = pd.DataFrame(rows)
    out["state_local_bn"] = out.effect_bn - out.federal_bn
    return out


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

    def index(self, reference: str) -> pd.Series:
        """Real national total of a BEA cell set, 2024 = 1 (backcast_categories.py `index`)."""
        nominal = self.wb.cells(reference)
        if nominal[LAST] <= 0:
            raise SystemExit(f"[BLOCKED] {reference} has no positive 2024 value")
        return nominal * self.real / nominal[LAST]

    def nominal(self, real: pd.Series) -> pd.Series:
        return real / self.real


RECEIPT_GROUPS = {3: ["federal_income_tax", "state_local_income_tax", "personal_motor_vehicle", "other_personal_tax"],
                  8: ["employee_oasdi", "employee_hi", "self_employment_oasdi_hi", "employer_oasdi", "employer_hi",
                      "medicare_supplementary_premiums", "other_domestic_social_contributions"],
                  4: ["general_sales_tax", "excise_selective_sales", "customs_duties"],
                  17: ["personal_current_transfers"]}
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
    "customs_duties": ("T30500-A:15", None), "personal_current_transfers": ("T30200-A:21", "T30300-A:20")}


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
        receipts = sum(rec.responsive_bn[names].sum() * hist.index(f"T30100-A:{line}") * hist.share
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
                      jf: dict, ucf: dict, parts: list | None = None) -> pd.DataFrame:
    """Programme rule on the adopted anchor, split by government, real 2024 $bn by year.

    Spending lines carry their own BEA cells (categories.csv) and each year's federal share; receipts
    carry their own federal or state-local series; induced receipts F scale with the group. P is excluded.
    September 24 correction lines: the school and college parts carry with the education line; each part
    of the constant line carries with the line it corrects, or with the group's size where it has none.
    """
    categories = pd.read_csv(FISCAL / "full_account_spending_2026_09_20/derived/categories.csv").set_index("category")
    phi = shares[conv]
    t = lines_at(corner).set_index("id")
    zero = pd.Series(0.0, index=YEARS)
    spending, spending_fed, receipts, receipts_fed = zero.copy(), zero.copy(), zero.copy(), zero.copy()
    for i in t.index[(t.side == "spending") & (t.responsive_bn != 0)]:
        amount = t.responsive_bn[i]
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
        if i == "general_public_services":
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
    for i in t.index[(t.side == "receipt") & (t.responsive_bn != 0)]:
        amount = t.responsive_bn[i]
        fed_cells, sl_cells = RECEIPT_SERIES[i]
        share_2024 = phi.loc[LAST, i]
        fed = amount * share_2024 * hist.index(fed_cells) * hist.share if fed_cells else zero
        sl = amount * (1 - share_2024) * hist.index(sl_cells) * hist.share if sl_cells else zero
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
    receipts_grouped = sum(rec.responsive_bn[names].sum() * hist.index(f"T30100-A:{line}") * hist.share
                           for line, names in RECEIPT_GROUPS.items())
    p, f = production(corner["normalization"])
    induced = f * hist.group / hist.group[LAST]
    out = pd.DataFrame(dict(spending=spending, spending_fed=spending_fed, receipts=receipts,
                            receipts_fed=receipts_fed, induced=induced, induced_fed=induced * phi["_induced_receipts"],
                            receipts_grouped=receipts_grouped, rtc_excess=rtc_excess,
                            rtc_excess_fed=rtc_excess * phi[rtc]))
    for rule, scale in (("programme", 1.0), ("income", hist.income)):
        out[f"gap_{rule}"] = out.spending - out.receipts * scale - out.induced
        out[f"federal_{rule}"] = out.spending_fed - out.receipts_fed * scale - out.induced_fed
        out[f"gap_{rule}_grouped"] = out.spending - out.receipts_grouped * scale - out.induced
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


def main() -> None:
    parser = argparse.ArgumentParser(description="Debt legacy of past federal gaps on an adopted main case.")
    parser.add_argument("--case", choices=("sept26", "sept24", "sept23"), default="sept26",
                        help="sept26: the main case adopted 2026-09-26 (default); sept24: the one adopted "
                             "2026-09-24; sept23: this lane's first result")
    parser.add_argument("--out-dir", type=Path, default=HERE / "derived")
    args = parser.parse_args()
    framed = args.case in ("sept24", "sept26")    # on the September 24 frame, with a corrections payload
    sept26 = args.case == "sept26"
    pins = check_pins()
    wb = Workbook(BEA / "Section3All_xls.xlsx")
    responses, gg_components = None, None
    if sept26:
        payload26 = json.loads(CORRECTIONS26_FILE.read_text())
        responses = payload26["meta"]["responses"]
        if responses != json.loads(MAIN26_SUMMARY.read_text())["responses"]:
            raise SystemExit("[BLOCKED] the payload's responses differ from main_case_2026_09_26 summary.json")
        gg_components = finite_components(responses)
        shares, extras = federal_shares(wb, Grants(), *gg_components)
    else:
        shares, extras = federal_shares(wb, Grants())
    jf = justice_federal(wb)
    ucf = uncompensated_federal(float(shares["central"].loc[LAST, "medicaid_and_chip_other_medical"]))
    hist = History(wb)
    control_gap = programme_control(hist)
    rates = rate_paths()
    out = args.out_dir
    out.mkdir(parents=True, exist_ok=True)

    # 1. The 2024 split of the adopted fiscal gap, at the corners that set each band. On September 24
    # each correction is split by its line's government level too, and the parts must add to the
    # change in the whole split at the same specification. September 26 does the same at the adopted
    # responses, with its payload's two new corrections as components of their own.
    COMPONENTS.clear()
    if sept26:
        corrected = apply_corrections(MODEL, payload26)
        main_summary = json.loads(MAIN26_SUMMARY.read_text())
        anchors = {prof: sept26_anchors(prof, corrected, main_summary, responses) for prof in PROFILES}
        COMPONENTS.update(sept26_components(json.loads(CORRECTIONS_FILE.read_text()), payload26))
    elif framed:
        corrected = apply_corrections(MODEL, json.loads(CORRECTIONS_FILE.read_text()))
        main_summary = json.loads(MAIN24_SUMMARY.read_text())
        anchors = {prof: sept24_anchors(prof, corrected, main_summary) for prof in PROFILES}
        COMPONENTS.update(json.loads(COMPONENTS_FILE.read_text()))
    else:
        anchors = {prof: adopted_anchors(prof) for prof in PROFILES}
    parts, correction_rows = {}, []
    split_rows, line_rows = [], []
    for prof, ends in anchors.items():
        for end, corner in ends.items():
            p, _ = production(corner["normalization"])
            cost = -welfare(corner)
            for conv in CONVENTIONS:
                if framed:
                    before = split_corner(dict(corner, model=MODEL), shares[conv], extras, conv, LAST, jf, ucf, end)
                    parts[(prof, end, conv)] = constant_parts(
                        corner, conv, shares, extras, before.federal_bn.sum() / before.responsive_bn.sum())
                table = split_corner(corner, shares[conv], extras, conv, LAST, jf, ucf, end, parts.get((prof, end, conv)))
                gap = table.responsive_bn.sum()
                if abs(gap - (cost + p)) > 1e-6:
                    raise SystemExit(f"[BLOCKED] {prof} {end}: fiscal gap {gap} != cost + P {cost + p}")
                fed = table.federal_bn.sum()
                if framed and prof == MAIN:
                    cs = correction_split(corner, shares[conv], extras, conv, LAST, parts[(prof, end, conv)])
                    if (cs.federal_bn + cs.state_local_bn - cs.effect_bn).abs().max() > 1e-12:
                        raise SystemExit("[BLOCKED] a correction's federal and state-local parts do not add to it")
                    d_gap = gap - before.responsive_bn.sum()
                    d_fed = fed - before.federal_bn.sum()
                    if abs(cs.effect_bn.sum() - d_gap) > 1e-9 or abs(cs.federal_bn.sum() - d_fed) > 1e-9:
                        raise SystemExit(f"[BLOCKED] {end}/{conv}: corrections add to {cs.effect_bn.sum():.6f} "
                                         f"(federal {cs.federal_bn.sum():.6f}), the split moved {d_gap:.6f} ({d_fed:.6f})")
                    for r in cs.itertuples():
                        correction_rows.append(dict(end=end, convention=conv, allocation=corner["allocation"],
                                                    component=r.component, side=r.side, line=r.line, cell=r.cell,
                                                    effect_bn=r.effect_bn, federal_bn=r.federal_bn,
                                                    state_local_bn=r.state_local_bn))
                split_rows.append(dict(profile=prof, end=end, convention=conv, allocation=corner["allocation"],
                                       normalization=corner["normalization"], school_share=corner["school_share"],
                                       school_response=corner["school_response"],
                                       general_government_response=corner["gg"],
                                       uncompensated_inside_bn=corner["uc"], net_cost_bn=cost, production_P_bn=p,
                                       fiscal_gap_bn=gap, federal_bn=fed, state_local_bn=gap - fed,
                                       federal_share=fed / gap))
                if prof == MAIN:
                    for r in table.itertuples():
                        line_rows.append(dict(end=end, convention=conv, side=r.side, line=r.id,
                                              gap_bn=r.responsive_bn, federal_bn=r.federal_bn,
                                              state_local_bn=r.state_local_bn))
    split = pd.DataFrame(split_rows)
    split.round(6).to_csv(out / "federal_split_2024.csv", index=False)
    pd.DataFrame(line_rows).round(6).to_csv(out / "federal_split_2024_lines.csv", index=False)
    if framed:
        corrections = pd.DataFrame(correction_rows)
        corrections.round(6).to_csv(out / "corrections_federal_split_2024.csv", index=False)
        by_component = corrections.assign(component=corrections.component.str.split(":").str[0]).groupby(
            ["end", "convention", "component"], sort=True)[["effect_bn", "federal_bn", "state_local_bn"]].sum()
        by_component["federal_share"] = by_component.federal_bn / by_component.effect_bn
        by_component.round(6).to_csv(out / "corrections_federal_by_component_2024.csv")
        if sept26:
            extras24 = federal_shares(wb, Grants())[1]       # general government at the elasticities
            bridge = sept26_bridge(anchors[MAIN], shares, extras, extras24, jf, ucf, corrections, main_summary, split)
            bridge.round(6).to_csv(out / "sept26_bridge_2024.csv", index=False)

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
    # The back-cast's concepts for the case: Sept 24 re-run in da2b107, Sept 26 added on 2026-09-26.
    family = "sept26" if sept26 else "corrected"
    benchmarks = ({"main": (MAIN, f"net_cost_cbo_informed_{family}"),
                   "proportional": ("proportional_reference", f"net_cost_full_proportional_{family}")}
                  if framed else BENCHMARKS)
    for bench, (prof, column) in benchmarks.items():
        bench_split = split[split.profile == prof].set_index(["end", "convention"])
        for end, corner in anchors[prof].items():
            p, _ = production(corner["normalization"])
            p_t = p * n / n[LAST]
            shared_receipts = lines_at(dict(corner, allocation="shared"))
            shared_receipts = shared_receipts[shared_receipts.side == "receipt"].set_index("id").amount_bn
            for conv in CONVENTIONS:
                prog = programme_federal(hist, corner, end, conv, shares, extras, jf, ucf, parts.get((prof, end, conv)))
                if abs(prog.loc[LAST, "gap_programme"] - bench_split.loc[(end, conv), "fiscal_gap_bn"]) > 1e-6 or \
                        abs(prog.loc[LAST, "federal_programme"] - bench_split.loc[(end, conv), "federal_bn"]) > 1e-6:
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
                # Whole-budget rules hold the 2024 split (the brief's rule where no category series exists).
                for rule in ("flat", "ratio", "income"):
                    gap = hist.annual[f"{column}_{end}__{rule}"].reindex(YEARS) + p_t
                    record(bench, f"whole_{rule}", end, conv, gap, phi * gap)
                    if conv == "central":
                        windows(bench, end, f"whole_{rule}", "whole_budget", gap, p_t)
                # Sensitivity: the federal part follows federal receipts and expenditure per capita instead.
                receipt_shares = pd.Series({i: (shares[conv].loc[LAST, i] if i in shares[conv].columns
                                                else indirect[i]) for i in shared_receipts.index})
                fr = float((shared_receipts * receipt_shares).sum())
                rho = fr * 1e9 / (n[LAST] * 1e6) / r_f[LAST]
                sigma = (fgap + fr) * 1e9 / (n[LAST] * 1e6) / s_f[LAST]
                for rule, scale in (("ratio", 1.0), ("income", hist.income)):
                    fed = n * 1e6 * (sigma * s_f - rho * scale * r_f) / 1e9
                    if abs(fed[LAST] - fgap) > 1e-6:
                        raise SystemExit("[BLOCKED] federal-series rule does not reproduce its 2024 anchor")
                    gap = hist.annual[f"{column}_{end}__{rule}"].reindex(YEARS) + p_t
                    record(bench, f"whole_{rule}_federal_series", end, conv, gap, fed)
    annual = pd.DataFrame(annual_rows)
    annual.round(6).to_csv(out / "federal_gap_annual.csv", index=False)
    pd.DataFrame(audit_rows).round(6).to_csv(out / "adopted_backcast_windows.csv", index=False)

    # 3. Stocks and 2024 legacy interest for every specification. The account's interest row (BEA
    # domestic interest, per head, zero response) and the group's per-head share of OMB net interest
    # are the two benchmarks the legacy line is compared with, never added to.
    interest_row = next(l for l in (corrected if framed else MODEL)["spending"]["lines"] if l["id"] == "domestic_interest")
    row_allocation = interest_row["keys"][interest_row["preferred_key"]]["personal"]["target_bn"]
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
                        interest_per_member_usd=interest * 1e9 / (TARGET_M * 1e6),
                        interest_per_other_resident_usd=interest * 1e9 / ((RESIDENTS_M - TARGET_M) * 1e6),
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
                                     / (TARGET_M * 1e6)))
    pd.DataFrame(benefit_rows).round(6).to_csv(out / "benefit_sensitivity.csv", index=False)

    # 4. Federal shares by line and year, for audit.
    long = [dict(convention=conv, line=col, year=year, federal_share=shares[conv].loc[year, col])
            for conv in CONVENTIONS for col in shares[conv].columns for year in YEARS]
    pd.DataFrame(long).round(6).to_csv(out / "federal_shares_by_year.csv", index=False)

    # 5. Forward counterpart: ladder 137's constant-flow path (a constant nominal flow borrowed at year
    # end at a constant rate) on the adopted federal flow; the whole gap is ladder 137's convention.
    def forward(f: float, r: float, years: int) -> tuple[float, float, float]:
        debt = f * ((1 + r) ** years - 1) / r
        return debt, debt - years * f, f * ((1 + r) ** (years - 1) - 1)

    for years, want in LADDER137_TABLE.items():      # README rounds to $1bn and the flow to $0.01bn
        if max(abs(a - b) for a, b in zip(forward(LADDER137_FLOW, LADDER137_RATE, years), want)) > 1.0:
            raise SystemExit(f"[BLOCKED] forward formula does not reproduce ladder 137 at year {years}")
    main_split = split[split.profile == MAIN].set_index(["end", "convention"])
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
                   anchors={end: plain({k: v for k, v in c.items() if k not in ("shift", "model")})
                            for end, c in anchors[MAIN].items()},
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
        lanes = (SHELTER_PARTS, SHELTER_KEYING, CARE_SUMMARY) + ((CK_PAYLOADS, R_VALUES) if sept26 else ())
        summary["case"] = dict(
            name=f"main case adopted 2026-09-{26 if sept26 else 24}",
            bands_source=str((MAIN26_SUMMARY if sept26 else MAIN24_SUMMARY).relative_to(ROOT)),
            corrections_sha256=sha(CORRECTIONS26_FILE if sept26 else CORRECTIONS_FILE),
            package_components_sha256=sha(COMPONENTS_FILE),
            lane_sha256={str(p.relative_to(ROOT)): sha(p) for p in lanes},
            band=main_summary["main_case"],
            corrections_2024=plain({f"{e}|{c}": dict(effect_bn=float(g.effect_bn.sum()), federal_bn=float(g.federal_bn.sum()))
                                    for (e, c), g in corrections.groupby(["end", "convention"])}))
        if sept26:
            summary["case"].update(
                responses=plain(responses), consumption_key_spec=COMPONENTS["meta"]["consumption_key_spec"],
                general_government_low_end_components=dict(zip(("federal_tax_collection", "state_local"),
                                                               map(float, gg_components))))
    (out / "summary.json").write_text(json.dumps(summary, indent=1, sort_keys=True) + "\n")
    print(split[split.profile == MAIN].round(3).to_string(index=False))
    print(f"programme control max |diff| {control_gap:.6f}bn")


if __name__ == "__main__":
    main()
