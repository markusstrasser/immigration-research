#!/usr/bin/env python3
"""Complete absolute account for the all-age Mexican-origin ledger.

Extends `all_age_ledger_2026_09_17` with the fiscal items that partial account
omits, under explicit conventions, and reports the union's absolute balance as a
waterfall from the measured +$50.24bn to a complete resident account.

Native-First: the upstream builder and estimator are imported, never copied. The
CPS record loading, civilian-household domain, target/reference masks, age
bands, full and 160 replicate weights and MEPS donor transport are the upstream
lane's. Every external number is read from a parameter file whose entries must
be `status: verified`; entries that are not verified are refused and the items
that depend on them are dropped and reported, never filled from a substitute.

Run from the repository root:

    OPENBLAS_NUM_THREADS=1 uv run --no-project python3 \
      infra/immigration-fiscal/ledger_absolute_2026_09_17/absolute_ledger.py \
      --params infra/immigration-fiscal/ledger_absolute_2026_09_17/params/params.json
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
FISCAL = HERE.parent
ROOT = HERE.parents[2]
ALL_AGE = FISCAL / "all_age_ledger_2026_09_17"
RESIDUAL = FISCAL / "ledger_residual_agg_2026_09_16"
GENEXT = FISCAL / "gen_ledger_extension_2026_09_16"
INSTITUTIONAL = FISCAL / "institutional_bound_2026_09_17"

sys.path.insert(0, str(GENEXT))
sys.path.insert(0, str(FISCAL / "build"))
sys.path.insert(0, str(ALL_AGE))
sys.path.insert(0, str(RESIDUAL))

import extend_ledger as ext                                     # noqa: E402
from meps_health_transport_2024 import donor_model, read_meps    # noqa: E402
from estimator import (account, contrast, standardized_gap, sufficient,  # noqa: E402
                       sum_cells)
import residual_agg as resid                                     # noqa: E402

COMPONENTS = ["tax", "cash", "noncash", "employer", "sales", "owner_property", "school", "lunch"]
COEFFICIENTS = np.array([1, -1, -1, 1, 1, 1, -1, 1], dtype=float)
TARGETS = ["mexico_born", "mexican_second_gen", "mexican_third_plus_selfid"]
UNION = "mexican_observed_total"
WHITE = "third_plus_nh_white"
ALL_NATIVE = "all_native"
REPORT_GROUPS = TARGETS + [UNION, WHITE, ALL_NATIVE]
NATIONAL = "all_civilian_residents"

# Waterfall order, central arms only.
# The brief's order runs to F at step 12; item S is appended as step 13 so the
# endpoint includes state-funded coverage, with the step-12 endpoint still visible.
WATERFALL_ORDER = ["G", "K", "P", "D", "U", "I", "M", "N", "E", "C", "X", "R", "F", "S"]
BRIEF_FINAL_STEP = WATERFALL_ORDER.index("F") + 1

ITEM_LABEL = {
    "G": "state-local general services",
    "K": "K-12 capital outlay and interest on school debt",
    "P": "non-school state and local capital outlay",
    "D": "district cost-to-serve differential",
    "U": "transfer under-reporting",
    "I": "refundable-credit improper payments",
    "M": "MEPS-to-NHEA coverage scaling",
    "N": "institutional care (external add)",
    "E": "immigration enforcement",
    "C": "corporate income tax, federal and state",
    "X": "excise and selective sales taxes",
    "R": "rest of the federal budget by function",
    "F": "federal defense, net interest, general government",
    "S": "state-funded coverage for undocumented residents",
}

# Items whose charge is dialled by the marginality parameter m. Records-based
# items (U, I, M, N, E, C, X) stay at m_item = 1.
MARGINAL_ITEMS = {"G", "K", "P", "D", "F", "R_percapita"}

# PEAFEVER is veteran status ("ever served"); VET_YN only flags receipt of
# veterans' payments. PEN_SC1/PEN_SC2 carry the pension SOURCE (3 = federal
# government pension) and PNSN_VAL the total across all sources; DST_* are
# retirement distributions on a different code set and are not pensions.
EXTRA_PERSON = ["INT_VAL", "DIV_VAL", "RNT_VAL", "PEAFEVER", "PEN_SC1", "PEN_SC2",
                "PNSN_VAL", "PEN_YN"]

MONEY_SCALE = [("billion", 1e9), ("bn", 1e9), ("million", 1e6), ("mn", 1e6),
               ("thousand", 1e3), ("dollar", 1.0), ("usd", 1.0), ("$", 1.0)]


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with Path(path).open("rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


class Params:
    """Parameter reader that refuses anything not marked `verified`."""

    def __init__(self, path: Path, allow_placeholder: bool):
        self.path = Path(path)
        self.raw = json.loads(self.path.read_text())
        self.allow_placeholder = allow_placeholder
        self.sha256 = sha256(self.path)
        self.used: dict[str, dict] = {}
        self.refused: list[dict] = []
        self.last_key: str | None = None
        self.last_unit: str | None = None
        self.interpretations: dict[str, dict] = {}

    def first(self, group: str, alias_sets, kind: str, preferred: str | None = None):
        """First accepted entry across several candidate token sets."""
        for tokens in alias_sets:
            value = self.pick(group, tokens, kind, preferred=preferred)
            if value is not None:
                return value
            preferred = None
        return None

    def admin_over_survey(self, group: str, alias_sets, label: str,
                          preferred: str | None = None):
        """An administrative-to-survey dollar ratio, whichever way it was published.

        A coverage ratio is survey over administrative and must be inverted; the
        key or the unit has to say so, because magnitude alone cannot tell a
        coverage ratio from a genuinely over-reported program."""
        value = self.first(group, alias_sets, "ratio", preferred=preferred)
        if value is None:
            return None
        text = f"{self.last_key or ''} {self.last_unit or ''}".lower()
        inverted = any(t in text for t in ["coverage", "survey_over", "survey/admin",
                                           "share_of_admin", "reported_share", "capture"])
        if inverted:
            if not 0.05 < value < 1.5:
                raise SystemExit(f"[BLOCKED] {label}: coverage ratio {value} out of range")
            ratio = 1.0 / value
        else:
            ratio = value
        if not 0.5 <= ratio <= 4.0:
            raise SystemExit(f"[BLOCKED] {label}: admin/survey ratio {ratio} out of range")
        self.interpretations[label] = dict(key=self.last_key, unit=self.last_unit,
                                           published=value, inverted=inverted,
                                           admin_over_survey=ratio)
        return ratio

    def nhea_over_meps(self, group: str, alias_sets, label: str,
                       preferred: str | None = None):
        """An NHEA-to-MEPS scaling ratio. A published MEPS share of NHEA is below
        one and is inverted; the ratio itself is above one."""
        value = self.first(group, alias_sets, "ratio", preferred=preferred)
        if value is None:
            return None
        inverted = value < 1.0
        ratio = 1.0 / value if inverted else value
        if not 1.0 <= ratio <= 3.0:
            raise SystemExit(f"[BLOCKED] {label}: NHEA/MEPS ratio {ratio} out of range")
        self.interpretations[label] = dict(key=self.last_key, unit=self.last_unit,
                                           published=value, inverted=inverted,
                                           nhea_over_meps=ratio)
        return ratio

    def _entries(self, group: str) -> dict:
        g = self.raw.get(group)
        return g if isinstance(g, dict) else {}

    def _accept(self, entry: dict) -> bool:
        status = str(entry.get("status", "")).lower()
        if status == "verified":
            return True
        return self.allow_placeholder and status in {"placeholder", "unverified"}

    def pick(self, group: str, tokens, kind: str, preferred: str | None = None):
        """First accepted entry in `group` whose key holds every token."""
        tokens = [t.lower() for t in tokens]
        candidates = []
        for key, entry in self._entries(group).items():
            if not isinstance(entry, dict):
                continue
            low = key.lower()
            if preferred is not None and key == preferred:
                candidates.insert(0, (key, entry))
            elif all(t in low for t in tokens):
                candidates.append((key, entry))
        reasons = []
        for key, entry in candidates:
            ref = f"{group}.{key}"
            if not self._accept(entry):
                reasons.append(f"{ref}: status={entry.get('status')!r}")
                continue
            value = entry.get("value")
            if value is None:
                reasons.append(f"{ref}: value is null")
                continue
            scaled, note = self._scale(value, entry.get("unit"), kind)
            if scaled is None:
                reasons.append(f"{ref}: unusable unit {entry.get('unit')!r} for kind {kind}")
                continue
            self.used[ref] = dict(value=scaled, raw_value=value, unit=entry.get("unit"),
                                  status=entry.get("status"), source_url=entry.get("source_url"),
                                  note=note)
            self.last_key, self.last_unit = key, entry.get("unit")
            return scaled
        self.refused.append(dict(group=group, tokens=tokens, preferred=preferred,
                                 kind=kind, reasons=reasons or ["no matching key"]))
        return None

    def _scale(self, value, unit, kind):
        try:
            return self._scale_inner(value, unit, kind)
        except (TypeError, ValueError, KeyError):
            return None, None

    def _scale_inner(self, value, unit, kind):
        if kind == "money":
            text = str(unit or "").lower()
            for token, factor in MONEY_SCALE:
                if token in text:
                    return float(value) * factor, f"unit {unit!r} -> x{factor:g}"
            return None, None
        if kind == "share":
            text = str(unit or "").lower()
            v = float(value)
            if "percent" in text or "%" in text:
                return v / 100.0, f"unit {unit!r} -> /100"
            return v, None
        if kind in {"number", "count", "index", "ratio"}:
            return float(value), None
        if kind == "mapping":
            if not isinstance(value, dict) or not value:
                return None, None
            return {k: float(v) for k, v in value.items()}, None
        if kind == "state_money":
            if not isinstance(value, dict) or not value:
                return None, None
            text = str(unit or "").lower()
            factor = next((f for t, f in MONEY_SCALE if t in text), None)
            if factor is None:
                return None, None
            out = {}
            for name, v in value.items():
                fips = STATE_NAME_TO_FIPS.get(str(name).strip())
                if fips is not None:
                    out[fips] = float(v) * factor
            return (out, f"unit {unit!r} -> x{factor:g}") if len(out) == 51 else (None, None)
        if kind == "state_count":
            if not isinstance(value, dict) or not value:
                return None, None
            out = {STATE_NAME_TO_FIPS[str(k).strip()]: float(v) for k, v in value.items()
                   if str(k).strip() in STATE_NAME_TO_FIPS}
            return (out, None) if len(out) == 51 else (None, None)
        raise ValueError(f"unknown parameter kind {kind}")


# --------------------------------------------------------------------------
# Cached in-repo aggregate readers (reused constructions, no new downloads)
# --------------------------------------------------------------------------

def read_assf_k12(path: Path) -> pd.DataFrame:
    """Per-state capital outlay, interest on school debt, membership, from the
    cached Census ASSF FY2024 summary workbook (Tables 1, 8 and 9)."""
    import openpyxl
    wb = openpyxl.load_workbook(path, read_only=True, data_only=True)

    def grid(sheet):
        return [[("" if c is None else c) for c in r]
                for r in wb[sheet].iter_rows(values_only=True)]

    def clean(name):
        return str(name).replace(".", "").strip()

    t1, t8, t9 = grid("1"), grid("8"), grid("9")
    current = {clean(r[0]): float(r[7]) * 1000.0 for r in t1
               if isinstance(r[7], (int, float)) and clean(r[0])}
    perpupil = {clean(r[0]): float(r[2]) for r in t8
                if isinstance(r[2], (int, float)) and clean(r[0])}
    capital = {clean(r[0]): (float(r[2]) + float(r[7])) * 1000.0 for r in t9
               if isinstance(r[2], (int, float)) and isinstance(r[7], (int, float)) and clean(r[0])}
    federal_revenue = float([r[3] for r in t1 if clean(r[0]) == "United States"][0]) * 1000.0
    rows = []
    for name, cur in current.items():
        if name == "United States" or name not in perpupil or name not in capital \
                or perpupil[name] <= 0:
            continue
        membership = cur / perpupil[name]
        rows.append(dict(name=name, membership=membership,
                         capital_and_interest=capital[name],
                         capital_interest_per_pupil=capital[name] / membership))
    table = pd.DataFrame(rows)
    return table, federal_revenue


def read_cog_national_lines(path: Path) -> tuple[float, float]:
    """US totals for general revenue from own sources (line 7) and state-local
    capital outlay (line 67) from the cached 2022 Census of Governments table."""
    import openpyxl
    ws = openpyxl.load_workbook(path, read_only=True, data_only=True)["2022_US_WY"]
    rows = [[("" if c is None else c) for c in r] for r in ws.iter_rows(values_only=True)]
    by_line = {int(r[0]): r for r in rows if isinstance(r[0], (int, float)) and r[0]}
    for line in (7, 67):
        if line not in by_line or not isinstance(by_line[line][2], (int, float)):
            raise SystemExit(f"[BLOCKED] Census of Governments line {line} not found")
    return float(by_line[7][2]) * 1000.0, float(by_line[67][2]) * 1000.0


# 2022 Census of Governments Table 1 line numbers. Lines 69..112 are the
# FUNCTIONAL breakdown of line 66 direct general expenditure and each function's
# own capital outlay is INSIDE its function total; line 67 is the same dollars
# cut by character, not an addition to them. So the general-services residual
# behind item G (line 66 less education, public welfare, hospitals, health and
# correction) already carries the capital outlay of every function it retains.
COG_LINE_CAPITAL_TOTAL = 67          # direct general capital outlay, all functions
COG_LINE_EDUCATION_CAPITAL = 70      # education capital outlay, all levels
COG_LINE_ELSEC_CAPITAL = 74          # elementary and secondary capital outlay
COG_LINE_HOSPITALS_CAPITAL = 82      # hospitals capital outlay
COG_LINE_CORRECTION_CAPITAL = 95     # correction capital outlay


def read_cog_capital(path: Path, pop: pd.Series) -> tuple[dict, dict, dict]:
    """State and local capital outlay by state, split into the part item G
    already charges and the part nothing in the account charges yet.

    Returns (per_capita_by_arm, national_by_arm, national_components), all in
    2022 dollars. Two arms:

    `briefed_gross`   total capital outlay less elementary-and-secondary capital
                      outlay, the literal quantity the extension brief names.
    `net_of_item_G`   the same less the capital outlay already inside the item G
                      general-services residual, which is every function except
                      education, hospitals and correction. Equal to education
                      capital less elementary-and-secondary capital, plus
                      hospitals capital, plus correction capital.
    """
    import openpyxl
    ws = openpyxl.load_workbook(path, read_only=True, data_only=True)["2022_US_WY"]
    rows = [[("" if c is None else c) for c in r] for r in ws.iter_rows(values_only=True)]
    header = rows[8]
    blocks = [(name.strip(), col) for col, name in enumerate(header)
              if isinstance(name, str) and name.strip() and col >= 2]
    by_line = {int(r[0]): r for r in rows if isinstance(r[0], (int, float)) and r[0]}
    wanted = [COG_LINE_CAPITAL_TOTAL, COG_LINE_EDUCATION_CAPITAL, COG_LINE_ELSEC_CAPITAL,
              COG_LINE_HOSPITALS_CAPITAL, COG_LINE_CORRECTION_CAPITAL]
    missing = [ln for ln in wanted if ln not in by_line]
    if missing:
        raise SystemExit(f"[BLOCKED] Census of Governments capital lines not found: {missing}")

    per_capita = {"briefed_gross": {}, "net_of_item_G": {}}
    national = {"briefed_gross": 0.0, "net_of_item_G": 0.0}
    components = {k: 0.0 for k in ["capital_total", "education_capital", "elsec_capital",
                                   "hospitals_capital", "correction_capital",
                                   "capital_inside_item_G"]}
    for name, col in blocks:
        def amount(line: int) -> float:
            v = by_line[line][col]
            if not isinstance(v, (int, float)) or not np.isfinite(v):
                raise ValueError(f"Missing required Census capital cell: {name}, line {line}: {v!r}")
            return 1000.0 * float(v)
        total = amount(COG_LINE_CAPITAL_TOTAL)
        educ = amount(COG_LINE_EDUCATION_CAPITAL)
        elsec = amount(COG_LINE_ELSEC_CAPITAL)
        hosp = amount(COG_LINE_HOSPITALS_CAPITAL)
        corr = amount(COG_LINE_CORRECTION_CAPITAL)
        inside_g = total - educ - hosp - corr
        gross = total - elsec
        net = educ + hosp + corr - elsec
        if net < 0:
            raise SystemExit(f"[BLOCKED] negative unpriced non-school capital in {name}")
        if name == "United States Total":
            national["briefed_gross"] = gross
            national["net_of_item_G"] = net
            components.update(capital_total=total, education_capital=educ,
                              elsec_capital=elsec, hospitals_capital=hosp,
                              correction_capital=corr, capital_inside_item_G=inside_g)
            continue
        fips = STATE_NAME_TO_FIPS.get(name)
        if fips is None:
            continue
        if fips not in pop.index:
            raise SystemExit(f"[BLOCKED] no 2022 population for {name}")
        per_capita["briefed_gross"][fips] = gross / pop.loc[fips]
        per_capita["net_of_item_G"][fips] = net / pop.loc[fips]
    for arm, mapping in per_capita.items():
        if len(mapping) != 51:
            raise SystemExit(f"[BLOCKED] capital arm {arm}: parsed {len(mapping)} "
                             "jurisdictions, expected 51")
    return per_capita, national, components


def read_omb_functions(path: Path) -> dict:
    """FY2024 dollar outlays for every function row of the cached OMB Table 3.1."""
    import openpyxl
    ws = openpyxl.load_workbook(path, read_only=True, data_only=True).worksheets[0]
    rows = [[("" if c is None else c) for c in r] for r in ws.iter_rows(values_only=True)]
    header = next(r for r in rows[:12] if any(str(c).strip() == "2024" for c in r))
    col = [i for i, c in enumerate(header) if str(c).strip() == "2024"][0]
    out = {}
    for r in rows:
        name = str(r[0]).strip()
        if name and name not in out and isinstance(r[col], (int, float)):
            out[name] = float(r[col]) * 1e6
        if name == "Total, Federal outlays" and name in out:
            break
    return out


OMB_FUNCTION_ROWS = {
    "050": "National Defense",
    "150": "International Affairs",
    "250": "General Science, Space, and Technology",
    "270": "Energy",
    "300": "Natural Resources and Environment",
    "350": "Agriculture",
    "370": "Commerce and Housing Credit",
    "400": "Transportation",
    "450": "Community and Regional Development",
    "500": "Education, Training, Employment, and Social Services",
    "550": "Health",
    "570": "Medicare",
    "600": "Income Security",
    "650": "Social Security",
    "700": "Veterans Benefits and Services",
    "750": "Administration of Justice",
    "800": "General Government",
    "900": "Net interest",
}

STATE_NAME_TO_FIPS = {
    "Alabama": 1, "Alaska": 2, "Arizona": 4, "Arkansas": 5, "California": 6,
    "Colorado": 8, "Connecticut": 9, "Delaware": 10, "District of Columbia": 11,
    "Florida": 12, "Georgia": 13, "Hawaii": 15, "Idaho": 16, "Illinois": 17,
    "Indiana": 18, "Iowa": 19, "Kansas": 20, "Kentucky": 21, "Louisiana": 22,
    "Maine": 23, "Maryland": 24, "Massachusetts": 25, "Michigan": 26,
    "Minnesota": 27, "Mississippi": 28, "Missouri": 29, "Montana": 30,
    "Nebraska": 31, "Nevada": 32, "New Hampshire": 33, "New Jersey": 34,
    "New Mexico": 35, "New York": 36, "North Carolina": 37, "North Dakota": 38,
    "Ohio": 39, "Oklahoma": 40, "Oregon": 41, "Pennsylvania": 42,
    "Rhode Island": 44, "South Carolina": 45, "South Dakota": 46,
    "Tennessee": 47, "Texas": 48, "Utah": 49, "Vermont": 50, "Virginia": 51,
    "Washington": 53, "West Virginia": 54, "Wisconsin": 55, "Wyoming": 56,
}


# --------------------------------------------------------------------------
# Institutional external add
# --------------------------------------------------------------------------

ACS_BANDS = ["0_17", "18_24", "25_34", "35_44", "45_54", "55_64", "65_74", "75_99"]


def institutional_cost_by_band(path: Path) -> tuple[dict, dict, dict]:
    """Midpoint of the adverse and moderate arms of the institutional lane,
    by ACS group and age band, rebuilt from that lane's own cells and constants."""
    cells = pd.read_csv(path)
    n, inst, inst_men = {}, {}, {}
    for _, r in cells.iterrows():
        key = (r["group"], r["band"])
        n[key] = n.get(key, 0.0) + float(r["weighted"])
        if int(r["typehugq"]) == 2:
            inst[key] = inst.get(key, 0.0) + float(r["weighted"])
            if int(r["sex"]) == 1:
                inst_men[key] = inst_men.get(key, 0.0) + float(r["weighted"])
    for b in ACS_BANDS:
        for store in (n, inst, inst_men):
            store[("mexican_total", b)] = (store.get(("mexico_born", b), 0.0)
                                           + store.get(("usborn_mexican", b), 0.0))
    prison = 60989.0
    nf_public = (147e9 / 1.2e6) * (0.63 + 0.14)
    cost = {}
    for group in ["mexico_born", "usborn_mexican", "mexican_total", "native_nh_white", "all_natives"]:
        for b in ACS_BANDS:
            i = inst.get((group, b), 0.0)
            if b in {"65_74", "75_99"}:
                adverse = moderate = i * nf_public
            else:
                male_share = inst_men.get((group, b), 0.0) / i if i else 0.0
                adverse, moderate = i * prison, i * prison * male_share
            cost[(group, b)] = 0.5 * (adverse + moderate)
    return cost, n, inst


# --------------------------------------------------------------------------
# Charge construction
# --------------------------------------------------------------------------

class Charges:
    """Named per-record signed dollar charges (cost negative, receipt positive)."""

    def __init__(self, n_records: int):
        self.n = n_records
        self.columns: list[str] = []
        self.data: list[np.ndarray] = []
        self.meta: dict[str, dict] = {}

    def add(self, item: str, arm: str, values: np.ndarray, **meta):
        key = f"{item}|{arm}"
        if key in self.meta:
            raise ValueError(f"duplicate charge column {key}")
        values = np.asarray(values, dtype=float)
        if values.shape != (self.n,) or not np.isfinite(values).all():
            raise ValueError(f"charge column {key} is not a finite length-{self.n} vector")
        self.columns.append(key)
        self.data.append(values)
        self.meta[key] = dict(item=item, arm=arm, **meta)

    def matrix(self) -> np.ndarray:
        return np.column_stack(self.data) if self.data else np.zeros((self.n, 0))


def build_charges(ctx, p: Params):
    """Every item's per-record charge vector, by arm. Returns (Charges, dropped)."""
    d = ctx["d"]
    index, n_units = ctx["index"], ctx["n_units"]
    civilian = ctx["civilian"]
    weights_full = ctx["weights"][:, 0]
    fips = d.GESTFIPS.to_numpy()
    ch = Charges(len(d))
    off = set(ctx.get("off") or [])
    dropped: list[dict] = []
    national: dict[str, dict] = {}
    ratio_inversion_check: list[dict] = []

    def drop(item, reason):
        dropped.append(dict(item=item, label=ITEM_LABEL.get(item, item), reason=reason))

    def unit_share(person_amounts: np.ndarray) -> np.ndarray:
        total = np.bincount(index, weights=np.asarray(person_amounts, dtype=float),
                            minlength=n_units)
        return ext.allocate(total, index, np.ones(len(d), bool), n_units)

    resident = ctx["us_resident"]

    def per_capita_of(total_dollars: float) -> np.ndarray:
        return np.where(civilian, -total_dollars / resident, 0.0)

    def proportional(total_dollars: float, basis: np.ndarray, sign: float = -1.0) -> np.ndarray:
        basis = np.asarray(basis, dtype=float)
        denom = float(basis @ weights_full)
        if denom <= 0:
            raise ValueError("nonpositive allocation basis")
        return sign * total_dollars * basis / denom * civilian

    def record_national(item, arm, target, vector, kind):
        realised = float(np.abs(vector) @ weights_full)
        national[f"{item}|{arm}"] = dict(target_dollars=target, charged_dollars=realised,
                                         ratio=realised / target if target else None, kind=kind)

    # ---- G: state and local general services -----------------------------
    gs_pc, gs_national = ctx["general_services"]
    deflator_ratio = p.pick("deflator", ["deflator", "ratio"], "ratio",
                            preferred="sl_deflator_2022_to_2024_ratio")
    idx_2022 = idx_2024 = None
    if deflator_ratio is None:
        idx_2022 = p.pick("deflator", ["price_index_2022"], "index",
                          preferred="sl_govt_cons_and_investment_price_index_2022")
        idx_2024 = p.pick("deflator", ["price_index_2024"], "index",
                          preferred="sl_govt_cons_and_investment_price_index_2024")
        if idx_2022 and idx_2024 and idx_2022 > 0:
            deflator_ratio = idx_2024 / idx_2022
    gs_rate = d.GESTFIPS.map(gs_pc).to_numpy(dtype=float)
    if np.isnan(gs_rate).any():
        raise ValueError("state without a general-services per-capita rate")
    ch.add("G", "nominal2022", np.where(civilian, -gs_rate, 0.0), source="cache:22slsstab1.xlsx",
           marginal=True, price_level="FY2022")
    record_national("G", "nominal2022", gs_national["general_services_total"],
                    np.where(civilian, -gs_rate, 0.0), "state_per_capita")
    if deflator_ratio:
        factor = deflator_ratio
        from consolidation import census_finance
        finance = census_finance(RESIDUAL / "_cache/22slsstab1.xlsx")
        pop_state = resid.read_state_population()
        fee_pc = {STATE_NAME_TO_FIPS[name]: row["fees"] / pop_state.loc[STATE_NAME_TO_FIPS[name]]
                  for name, row in finance.items() if name in STATE_NAME_TO_FIPS}
        fee_rate = d.GESTFIPS.map(fee_pc).to_numpy(dtype=float)
        if not np.isfinite(fee_rate).all():
            raise ValueError("Missing state service-fee allocation")
        net_rate = (gs_rate - fee_rate) * factor
        national_fees = finance["United States Total"]["fees"] * factor
        ch.add("G", "deflated2024", np.where(civilian, -net_rate, 0.0),
               source="cache:22slsstab1.xlsx + params:deflator", marginal=True,
               price_level="2024", deflator=factor, gross_services=gs_national["general_services_total"] * factor,
               mapped_service_fees=national_fees, fees_by_state_per_capita=fee_pc,
               fee_rule="net service cost by state; Census fee lines 28..36 only; user incidence not observed",
               excluded_receipts="other charges, education, hospitals and miscellaneous revenue")
        record_national("G", "deflated2024", gs_national["general_services_total"] * factor - national_fees,
                        np.where(civilian, -net_rate, 0.0), "state_per_capita")
        g_central = "deflated2024"
    else:
        raise ValueError("2024-price account requires a verified state/local deflator")

    # ---- K: K-12 capital outlay and interest on school debt ---------------
    k12, federal_k12_revenue = ctx["assf"]
    f33_capital = p.pick("k12", ["capital_outlay", "by_state"], "state_money",
                         preferred="f33_capital_outlay_by_state")
    f33_interest = p.pick("k12", ["interest", "by_state"], "state_money",
                          preferred="f33_interest_on_school_debt_by_state")
    f33_membership = p.pick("k12", ["membership", "by_state"], "state_count",
                            preferred="f33_fall_membership_by_state")
    k12_source = "cache:census_assf_fy2024_summary_tables.xlsx"
    k12_national = float(k12.capital_and_interest.sum())
    if f33_capital and f33_interest and f33_membership:
        cap_pp = {f: (f33_capital[f] + f33_interest[f]) / f33_membership[f]
                  for f in f33_capital if f33_membership.get(f)}
        k12_national = sum(f33_capital[f] + f33_interest[f] for f in cap_pp)
        k12_source = "params:k12 F-33 capital, interest and fall membership by state"
        cached_national = float(k12.capital_and_interest.sum())
        if abs(cached_national - k12_national) > 0.01 * abs(k12_national):
            raise SystemExit("[BLOCKED] the cached ASSF capital plus interest total disagrees "
                             f"with the fetched F-33 total: {cached_national} vs {k12_national}")
    else:
        cap_pp = {STATE_NAME_TO_FIPS[r["name"]]: r["capital_interest_per_pupil"]
                  for _, r in k12.iterrows() if r["name"] in STATE_NAME_TO_FIPS}
        drop("K(membership source)", "F-33 capital, interest or fall membership by state not "
                                     "verified; the cached ASSF workbook derivation was used")
    children = d.A_AGE.between(5, 17).to_numpy(dtype=float)
    cap_person = children * pd.Series(fips).map(cap_pp).to_numpy(dtype=float) * ext.PUPIL_RATIO_NATIVE_ACS
    if np.isnan(cap_person).any():
        raise ValueError("state without K-12 capital per-pupil")
    personal = ctx.get("allocation", "shared") == "personal"
    recipient = lambda x: x if personal else unit_share(x)
    ch.add("K", "central", -recipient(cap_person) * civilian, source=k12_source, marginal=True)
    record_national("K", "central", k12_national,
                    -recipient(cap_person) * civilian, "pupil_based")

    # ---- P: non-school state and local capital outlay ---------------------
    # Charged per capita by state of residence on the same 2022 state population
    # denominator item G uses, inflated by the same state-local price index.
    cap_pc, cap_national, cap_components = ctx["capital"]
    if "P" in off:
        drop("P", "switched off at the command line with --off P")
    elif deflator_ratio is None:
        drop("P", "the BEA state-local price index is not verified, so the 2022 capital "
                  "figures could not be brought to the 2024 price level")
    else:
        for arm in ["net_of_item_G", "briefed_gross"]:
            rate = d.GESTFIPS.map(cap_pc[arm]).to_numpy(dtype=float) * deflator_ratio
            if np.isnan(rate).any():
                raise ValueError(f"state without a capital per-capita rate for arm {arm}")
            vector = np.where(civilian, -rate, 0.0)
            ch.add("P", arm, vector, source="cache:22slsstab1.xlsx + params:deflator",
                   marginal=True, price_level="2024", deflator=deflator_ratio,
                   national_2022=cap_national[arm])
            record_national("P", arm, cap_national[arm] * deflator_ratio, vector,
                            "state_per_capita")

    # ---- D: district cost-to-serve differential ---------------------------
    hisp_diff = (None if "D" in off else
                 p.pick("district", ["hispanic", "minus_all"], "state_money",
                        preferred="hispanic_minus_all_by_state")
                 or p.pick("k12", ["hispanic", "differential"], "state_money"))
    white_diff = (None if "D" in off else
                  p.pick("district", ["white", "minus_all"], "state_money",
                         preferred="white_minus_all_by_state")
                  or p.pick("k12", ["white", "differential"], "state_money"))
    if "D" in off:
        drop("D", "switched off at the command line with --off D")
    elif hisp_diff and white_diff:
        h = pd.Series(fips).map(hisp_diff).fillna(0.0).to_numpy(dtype=float)
        w = pd.Series(fips).map(white_diff).fillna(0.0).to_numpy(dtype=float)
        rate = np.where(ctx["is_white_ref"], w, np.where(ctx["is_target"], h, 0.0))
        diff_person = children * rate * ext.PUPIL_RATIO_NATIVE_ACS
        ch.add("D", "central", -recipient(diff_person) * civilian,
               source="params:district F-33 x CCD per-pupil differentials", marginal=True,
               rule="Mexican-origin public pupils aged 5-17 are charged their state's "
                    "Hispanic-minus-all differential, the third-plus non-Hispanic white "
                    "reference its white-minus-all differential, and every other record "
                    "zero; there is no separate all-native rate, so the all-native "
                    "reference carries only the charges of its own members")
    elif hisp_diff or white_diff:
        drop("D", "only one of the two district differentials is verified; the item needs "
                  "both the Hispanic-minus-all and the white-minus-all vector")
    else:
        drop("D", "district F-33 x CCD Hispanic/white per-pupil differentials not verified")

    # ---- U: transfer under-reporting --------------------------------------
    heads = ctx["heads"]
    ratios = {
        "snap": (p.admin_over_survey("underreporting", [["snap"], ["food", "stamp"]], "snap",
                                  preferred="ratio_snap"),
                 heads.SPM_SNAPSUB.to_numpy(dtype=float), "unit"),
        "tanf": (p.admin_over_survey("underreporting", [["tanf"], ["cash", "assistance"],
                                                        ["public", "assistance"]], "tanf",
                                  preferred="ratio_tanf"),
                 d.PAW_VAL.to_numpy(dtype=float), "person"),
        "ssi": (p.admin_over_survey("underreporting", [["ssi"], ["supplemental", "security"]], "ssi",
                                 preferred="ratio_ssi"),
                d.SSI_VAL.to_numpy(dtype=float), "person"),
        "ui": (p.admin_over_survey("underreporting", [["unemployment"], ["_ui"], ["ui_"]], "ui",
                                preferred="ratio_ui"),
               d.UC_VAL.to_numpy(dtype=float), "person"),
        "social_security": (p.admin_over_survey(
            "underreporting", [["social_security"], ["social", "security"], ["oasdi"]],
            "social_security", preferred="ratio_social_security"),
            d.SS_VAL.to_numpy(dtype=float), "person"),
    }
    # The researcher inverted published survey/administrative coverage ratios into
    # the admin/survey ratios this item needs. Re-derive each one from the published
    # coverage vector and refuse the run if any inversion does not hold.
    coverage = p.first("underreporting", [["repo_lane_ratio_base"], ["ratio_base"]], "mapping",
                       preferred="repo_lane_ratio_base")
    inversion = []
    if coverage:
        for program, coverage_key in [("snap", "snap"), ("tanf", "cash_assistance"),
                                      ("ssi", "ssi"), ("ui", "unemployment"),
                                      ("social_security", "social_security")]:
            ratio = ratios[program][0]
            published = coverage.get(coverage_key)
            if ratio is None or published in (None, 0):
                continue
            implied = 1.0 / published
            inversion.append(dict(program=program, published_coverage_ratio=published,
                                  parameter_admin_over_survey=ratio,
                                  recomputed_admin_over_survey=implied,
                                  agree=abs(ratio - implied) <= 1e-3 * max(implied, 1.0)))
        bad = [r for r in inversion if not r["agree"]]
        if bad:
            raise SystemExit("[BLOCKED] an admin/survey ratio is not the reciprocal of its "
                             f"published coverage ratio: {bad}")
    ratio_inversion_check.extend(inversion)
    missing_u = [k for k, (r, _, _) in ratios.items() if r is None]
    priced_u = {}
    if len(missing_u) == len(ratios):
        drop("U", "no verified admin/survey coverage ratio for any program")
    else:
        vector = np.zeros(len(d))
        for name, (ratio, base, level) in ratios.items():
            if ratio is None:
                continue
            unit_total = base.copy() if level == "unit" else np.bincount(
                index, weights=base, minlength=n_units)
            increment = unit_total * (ratio - 1.0)
            spread = (base * (ratio - 1.0) if personal and level == "person" else
                      ext.allocate(increment, index, np.ones(len(d), bool), n_units))
            vector = vector - spread
            priced_u[name] = dict(ratio=ratio, applied=True,
                                  national_increment=float(spread @ weights_full))
        ch.add("U", "central", vector * civilian, source="params:underreporting",
               marginal=False, programs=priced_u, missing=missing_u)

    # ---- I: refundable-credit improper payments ---------------------------
    eitc_improper = p.first("improper_payments", [["eitc", "dollar"], ["eitc", "improper"],
                                                  ["eitc"], ["earned", "income"]], "money",
                            preferred="eitc_improper_payments_fy2024")
    actc_improper = p.first("improper_payments", [["actc", "improper"], ["actc"],
                                                  ["additional_child"], ["child_tax"]], "money",
                            preferred="actc_improper_payments_fy2024")
    if eitc_improper is not None or actc_improper is not None:
        vector = np.zeros(len(d))
        pieces = {}
        for label, total, field in [("eitc", eitc_improper, "EIT_CRED"),
                                    ("actc", actc_improper, "ACTC_CRD")]:
            if total is None:
                continue
            basis = unit_share(d[field].to_numpy(dtype=float))
            vector = vector + proportional(total, basis, sign=-1.0)
            pieces[label] = total
        ch.add("I", "central", vector, source="params:improper_payments",
               marginal=False, pieces=pieces)
    else:
        drop("I", "EITC/ACTC improper-payment dollars not verified")
    ch.add("I", "zero", np.zeros(len(d)), source="convention", marginal=False)

    # ---- M: MEPS-to-NHEA coverage scaling ---------------------------------
    r_mcd = p.nhea_over_meps("meps_coverage", [["ratio", "medicaid"], ["medicaid"]], "medicaid",
                             preferred="nhea_to_meps_ratio_medicaid")
    r_mcr = p.nhea_over_meps("meps_coverage", [["ratio", "medicare"], ["medicare"]], "medicare",
                             preferred="nhea_to_meps_ratio_medicare")
    if r_mcd is not None and r_mcr is not None:
        mcd = ctx["donor_payer_means"]["medicaid"][ctx["donor_codes"]]
        mcr = ctx["donor_payer_means"]["medicare"][ctx["donor_codes"]]
        extra = -(mcd * (r_mcd - 1.0) + mcr * (r_mcr - 1.0)) * ctx["exposure"]
        ch.add("M", "central", extra * civilian, source="params:meps_coverage",
               marginal=False, ratio_medicaid=r_mcd, ratio_medicare=r_mcr)
    else:
        drop("M", "NHEA-to-MEPS per-payer coverage ratios not verified")
    ch.add("M", "zero", np.zeros(len(d)), source="convention", marginal=False)

    # ---- E: immigration enforcement ---------------------------------------
    mex_noncit = (d.PRCITSHP.eq(5) & d.PENATVTY.eq(303)).to_numpy() & civilian
    n_mex_noncit = float(weights_full[mex_noncit].sum())
    unauth_total = p.pick("unauthorized", ["unauthorized", "total"], "count",
                          preferred="ohss_unauthorized_total_jan2022")
    unauth_mex = p.pick("unauthorized", ["unauthorized", "mexico"], "count",
                        preferred="ohss_unauthorized_mexico_jan2022")
    # ICE ERO total already contains custody, transport, ATD and fugitive
    # operations, so the custody line is recorded but never added on top of it.
    interior_parts = {
        "ice_ero_total": p.pick("enforcement", ["ero", "total"], "money",
                                preferred="ice_ero_total"),
        "eoir": p.pick("enforcement", ["eoir"], "money",
                       preferred="doj_eoir_appropriation"),
        "uscis_appropriated": p.pick("enforcement", ["uscis", "appropriated"], "money",
                                     preferred="uscis_net_discretionary_appropriated"),
    }
    custody_detail = p.pick("enforcement", ["custody"], "money",
                            preferred="ice_ero_custody_operations")
    border_patrol = p.pick("enforcement", ["border", "patrol"], "money",
                           preferred="cbp_us_border_patrol")
    mex_share_encounters = p.first("city_migrant", [["mexico", "share", "encounter"],
                                                   ["mexico", "share"], ["encounter", "share"]],
                                   "share", preferred="mexico_share_sw_encounters_fy2024")
    ch.add("E", "zero", np.zeros(len(d)), source="convention", marginal=False)
    if (unauth_total and unauth_mex and n_mex_noncit > 0
            and all(v is not None for v in interior_parts.values())):
        share = unauth_mex / unauth_total
        interior = sum(interior_parts.values()) * share
        rate = interior / n_mex_noncit
        stock = np.where(mex_noncit, -rate, 0.0)
        ch.add("E", "stock", stock, source="params:enforcement,unauthorized",
               marginal=False, mexico_share_of_unauthorized=share,
               national_dollars=interior, per_head=rate, parts=interior_parts,
               custody_inside_ero_total=custody_detail)
        record_national("E", "stock", interior, stock, "head_based")
        if border_patrol is not None and mex_share_encounters is not None:
            flow = border_patrol * mex_share_encounters
            rate2 = (interior + flow) / n_mex_noncit
            ch.add("E", "stock_plus_flow", np.where(mex_noncit, -rate2, 0.0),
                   source="params:enforcement,unauthorized,city_migrant", marginal=False,
                   national_dollars=interior + flow, per_head=rate2)
        else:
            drop("E(flow arm)", "Border Patrol appropriation or Mexico share of FY2024 "
                                "southwest border encounters not verified")
        pew_total = p.first("unauthorized", [["pew", "total"]], "count",
                            preferred="pew_unauthorized_total_2023_secondary")
        pew_mex = p.first("unauthorized", [["pew", "mexico", "2023"]], "count",
                          preferred="pew_unauthorized_mexico_2023_secondary")
        if pew_total and pew_mex:
            pew_share = pew_mex / pew_total
            pew_rate = sum(interior_parts.values()) * pew_share / n_mex_noncit
            ch.add("E", "stock_pew_secondary", np.where(mex_noncit, -pew_rate, 0.0),
                   source="params:enforcement,unauthorized (Pew, secondary)", marginal=False,
                   mexico_share_of_unauthorized=pew_share,
                   note="Pew mid-2023 is a secondary estimate; OHSS January 2022 is the central arm")
        else:
            drop("E(Pew arm)", "the Pew secondary unauthorized estimates are not verified")
        e_central = "stock"
    else:
        drop("E", "DHS/EOIR interior appropriations or the OHSS unauthorized stock not verified")
        e_central = "zero"

    # ---- C: corporate income tax ------------------------------------------
    fed_corp = p.pick("omb", ["receipts", "corporat"], "money",
                      preferred="receipts_corporation_income")
    state_corp = p.first("corporate", [["state", "corporat"], ["corporat"]], "money",
                         preferred="state_corporate_net_income_tax_2024")
    corporate_note = "federal and state"
    if fed_corp is not None and state_corp is None:
        state_corp = 0.0
        corporate_note = "federal only; the state corporate net income tax was zeroed"
        drop("C(state share)", "Census state corporate net income tax not verified; the item "
                               "carries the federal receipt only")
    wage = d.WSAL_VAL.clip(lower=0).to_numpy(dtype=float)
    prop_income = (d.INT_VAL + d.DIV_VAL + d.RNT_VAL).clip(lower=0).to_numpy(dtype=float)
    if fed_corp is not None and state_corp is not None:
        corp_total = fed_corp + state_corp
        wage_share = proportional(corp_total, unit_share(wage), sign=+1.0)
        cap_share = proportional(corp_total, unit_share(prop_income), sign=+1.0)
        ch.add("C", "wage25_capital75", 0.25 * wage_share + 0.75 * cap_share,
               source="params:omb,corporate", marginal=False, national_dollars=corp_total,
               coverage=corporate_note)
        ch.add("C", "per_capita", -per_capita_of(corp_total),
               source="params:omb,corporate", marginal=False, national_dollars=corp_total)
        ch.add("C", "all_capital", cap_share, source="params:omb,corporate",
               marginal=False, national_dollars=corp_total)
        record_national("C", "wage25_capital75", corp_total,
                        0.25 * wage_share + 0.75 * cap_share, "income_share")
        c_central = "wage25_capital75"
    else:
        drop("C", "federal corporate receipts (OMB 2.1) or state corporate net income tax not verified")
        c_central = None

    # ---- X: excise and selective sales taxes ------------------------------
    fed_excise = p.pick("omb", ["receipts", "excise"], "money",
                        preferred="receipts_excise")
    state_excise = p.first("corporate", [["selective", "sales"], ["selective"],
                                        ["state", "excise"]], "money",
                           preferred="state_selective_sales_taxes_2024")
    excise_note = "federal and state"
    if fed_excise is not None and state_excise is None:
        state_excise = 0.0
        excise_note = "federal only; state selective sales taxes were zeroed"
        drop("X(state share)", "Census state selective sales taxes not verified; the item "
                               "carries the federal receipt only")
    if fed_excise is not None and state_excise is not None:
        x_total = fed_excise + state_excise
        flat = np.where(civilian, x_total / resident, 0.0)
        ch.add("X", "per_capita", flat, source="params:omb,corporate", marginal=False,
               national_dollars=x_total, coverage=excise_note)
        record_national("X", "per_capita", x_total, flat, "flat_per_capita")
        consumption = ctx["consumption_proxy"]
        ch.add("X", "consumption_proxy", proportional(x_total, consumption, sign=+1.0),
               source="params:omb,corporate", marginal=False, national_dollars=x_total)
        x_central = "per_capita"
    else:
        drop("X", "federal excise receipts or state selective sales taxes not verified")
        x_central = None

    # ---- R: rest of the federal budget by function ------------------------
    # Each part carries a netted dollar amount, the central arm's allocation and
    # the alternative per-capita allocation of the SAME amount, so switching arms
    # changes who is charged, never how much is charged nationally. Everything the
    # base account already prices is netted out: the MEPS public payers cover
    # Medicare, Medicaid, VA and TRICARE medical, the CPS transfer fields cover
    # unemployment, food and nutrition and other income security, and subfunction
    # 501 is the federal share already sitting inside per-pupil current spending.
    omb = ctx["omb"]
    from consolidation import federal_programs, require_conservation
    programs = federal_programs(HERE / "_cache")

    def func(code):
        return omb[OMB_FUNCTION_ROWS[code]]

    def sub(code, name):
        return p.pick("omb", [f"subf_{code}"], "money")

    veterans_mask = d.PEAFEVER.eq(1).to_numpy() & civilian
    n_vets = float(weights_full[veterans_mask].sum())
    # PNSN_VAL is the total across every pension source; CPS ASEC does not value
    # the federal component separately, so a person flagged with a federal
    # pension source contributes their whole pension income. For anyone holding a
    # second, non-federal pension this over-attributes; the size of that exposure
    # is measured and recorded rather than assumed away.
    federal_source = (d.PEN_SC1.eq(3) | d.PEN_SC2.eq(3)).to_numpy()
    fed_pension = np.where(federal_source, d.PNSN_VAL.to_numpy(dtype=float), 0.0)
    mixed = federal_source & (
        (d.PEN_SC1.eq(3) & d.PEN_SC2.isin([1, 2, 4, 5, 6, 7, 8]))
        | (d.PEN_SC2.eq(3) & d.PEN_SC1.isin([1, 2, 4, 5, 6, 7, 8]))).to_numpy()
    mixed_dollar_share = (float((fed_pension * mixed) @ weights_full)
                          / max(float(fed_pension @ weights_full), 1.0))
    r_parts: list[tuple[str, np.ndarray, np.ndarray, bool]] = []
    r_detail, r_missing = {}, []

    # 700 veterans, net of VA hospital and medical care, which MEPS TOTVA24 prices
    f703 = sub("703", "veterans medical")
    if n_vets > 0 and f703 is not None:
        va_cash = float((recipient(d.VET_VAL.to_numpy(dtype=float)) * civilian) @ weights_full)
        net700 = func("700") - f703 - va_cash
        if net700 < 0:
            raise ValueError("CPS veterans cash exceeds the administrative nonmedical VA target")
        r_parts.append(("700_veterans_net_of_medical",
                        np.where(veterans_mask, -net700 / n_vets, 0.0),
                        per_capita_of(net700), False))
        r_detail["700_veterans_net_of_medical"] = dict(
            dollars=net700, gross=func("700"), va_medical_already_priced=f703,
            cash_already_priced=va_cash,
            conservation_residual=func("700") - f703 - va_cash - net700,
            rule="function 700 less subfunction 703 and the exact weighted CPS VA cash "
                 "already charged in this allocation, with the remainder spread per veteran "
                 "(PEAFEVER = 1, ever served on active duty)")
    else:
        r_missing.append("703 VA medical subfunction, needed to net function 700")

    # 602 federal civilian retirement, by reported federal pension income
    f602 = sub("602", "federal employee retirement")
    if f602 is not None and float(unit_share(fed_pension) @ weights_full) > 0:
        r_parts.append(("602_federal_retirement",
                        proportional(f602, unit_share(fed_pension), sign=-1.0),
                        per_capita_of(f602), False))
        r_detail["602_federal_retirement"] = dict(
            dollars=f602,
            rule="share of total pension income (PNSN_VAL) among people reporting a federal "
                 "government pension source (PEN_SC1 or PEN_SC2 = 3)",
            caveat="CPS ASEC carries no separately valued federal pension amount, so this is a "
                   "proxy that over-attributes for holders of a second non-federal pension",
            share_of_the_allocated_dollars_held_by_mixed_source_people=mixed_dollar_share,
            weighted_people_with_a_federal_pension_source=float(
                weights_full[federal_source & civilian].sum()))
    else:
        r_missing.append("602 federal civilian retirement subfunction")

    # 750 administration of justice: 753 correctional by the BOP Mexican share
    f753 = sub("753", "federal correctional")
    bop_share = p.pick("enforcement", ["bop", "share"], "share",
                       preferred="bop_inmates_mexican_share_pct")
    if f753 is not None:
        # Item N already prices institutional correctional residents at every
        # government level. Do not add federal prisons for the same people.
        justice_grants = programs["justice_grants"]
        rest = func("750") - f753 - justice_grants
        r_parts.append(("750_remainder", per_capita_of(rest), per_capita_of(rest), True))
        r_detail["750_administration_of_justice"] = dict(
            dollars=rest, gross=func("750"), correctional_subfunction=f753,
            federal_grants_netted=justice_grants,
            conservation_residual=require_conservation(func("750"), f753, justice_grants, rest, "justice"),
            matching_limit="justice grants finance G police/courts or N corrections; program amounts include tribal/territorial recipients",
            correctional_already_owned_by="N institutional cost proxy, all government levels",
            rule="exclude federal correctional outlays already represented by N; remaining justice per capita")
    else:
        r_missing.append("753 correctional subfunction or the BOP Mexican-national share")

    # 500 education and training, net of the federal K-12 aid inside per-pupil spending
    f501 = sub("501", "elementary and secondary")
    if f501 is not None:
        net500 = func("500") - f501
        r_parts.append(("500_education_net", per_capita_of(net500), per_capita_of(net500), True))
        r_detail["500_education_net"] = dict(
            dollars=net500, gross=func("500"), elementary_secondary_subfunction=f501,
            assf_federal_school_revenue_crosscheck=federal_k12_revenue,
            rule="function 500 less subfunction 501, the federal elementary and secondary aid "
                 "already inside the state per-pupil current spending the account charges; "
                 "Pell is NOT netted because nothing in this account prices it",
            pell_not_netted=True)
    else:
        r_missing.append("501 elementary/secondary subfunction, needed to net function 500")

    # 550 health, net of Medicaid. OMB has no Medicaid subfunction; subfunction
    # 551 is health care services, far broader than Medicaid, so the NHEA federal
    # Medicaid figure is the right netting quantity.
    f551 = sub("551", "health care services")
    medicaid_federal = programs["medicaid_federal"]
    if medicaid_federal is not None:
        chip_federal = programs["chip_federal"]
        net550 = func("550") - medicaid_federal - chip_federal
        r_parts.append(("550_health_net", per_capita_of(net550), per_capita_of(net550), True))
        r_detail["550_health_net"] = dict(
            dollars=net550, gross=func("550"), federal_medicaid_netted=medicaid_federal,
            federal_chip_netted=chip_federal,
            conservation_residual=require_conservation(func("550"), medicaid_federal + chip_federal, 0, net550, "health"),
            health_care_services_subfunction_not_used=f551,
            rule="function 550 less federal Medicaid and CHIP (OMB FY2024), which the MEPS public-payer "
                 "transport already charges, per capita. OMB subfunction 551 is health care "
                 "services, much broader than Medicaid, so it is not the netting quantity",
            year_mismatch="Medicaid and federal function now both FY2024; MEPS transport remains calendar 2024")
    else:
        r_missing.append("NHEA federal Medicaid, needed to net function 550")

    # 600 income security: only the subfunctions nothing else prices
    f601 = sub("601", "general retirement and disability")
    f604 = sub("604", "housing assistance")
    housing_per_capita = np.zeros(len(d))
    housing_by_subsidy = np.zeros(len(d))
    if f601 is not None and f604 is not None:
        housing_grants = programs["housing"]["dollars"]
        net604 = f604 - housing_grants
        net600 = f601 + net604
        # Housing assistance is isolated so its allocation rule can be switched.
        housing_per_capita = per_capita_of(net604)
        subsidy_basis = ext.allocate(heads.SPM_CAPHOUSESUB.to_numpy(dtype=float),
                                     index, np.ones(len(d), bool), n_units)
        housing_by_subsidy = (proportional(net604, subsidy_basis, sign=-1.0)
                              if float(subsidy_basis @ weights_full) > 0 else housing_per_capita)
        r_parts.append(("600_income_security_net", per_capita_of(net600), per_capita_of(net600), True))
        r_detail["600_income_security_net"] = dict(
            dollars=net600, gross=func("600"), general_retirement_601=f601,
            housing_assistance_604=f604,
            federal_grants_netted=housing_grants, grant_programs=programs["housing"]["programs"],
            conservation_residual=require_conservation(f601 + f604, 0, housing_grants, net600, "income security"),
            matching_limit=programs["limitation"],
            already_priced=["603 unemployment (CPS UC_VAL)",
                            "605 food and nutrition (SPM SNAP, WIC, school lunch)",
                            "609 other income security (CPS SSI and the refundable credits "
                            "inside FEDTAX_AC)",
                            "602, charged separately above"],
            rule="subfunctions 601 and 604 only, per capita; every other income-security "
                 "subfunction is already inside the account")
    else:
        r_missing.append("601 or 604 income-security subfunctions")

    # 400 transportation, per capita in every arm
    transport_grants = programs["transport"]["dollars"]
    transport_net = func("400") - transport_grants
    r_parts.append(("400_transportation", per_capita_of(transport_net),
                    per_capita_of(transport_net), True))
    r_detail["400_transportation"] = dict(
        dollars=transport_net, gross=func("400"), federal_grants_netted=transport_grants,
        grant_programs=programs["transport"]["programs"],
        conservation_residual=require_conservation(func("400"), 0, transport_grants, transport_net, "transportation"),
        matching_limit=programs["limitation"],
        rule="per capita after named highway/airport/port grants whose final services are in G; transit grants retained")

    # functions the central arm treats as pure public goods and prices at zero
    zero_codes = ["150", "250", "270", "300", "350", "370", "450"]
    zero_vector = sum(per_capita_of(func(c)) for c in zero_codes)
    r_detail["zero_in_central"] = dict(codes=zero_codes,
                                       dollars={c: func(c) for c in zero_codes},
                                       rule="zero in the central arm, per capita in the alternative")

    if r_parts:
        central = sum(v for _, v, _, _ in r_parts)
        central_marginal = sum(v for _, v, _, m in r_parts if m)
        if not isinstance(central_marginal, np.ndarray):
            central_marginal = np.zeros(len(d))
        ch.add("R", "central", central,
               source="cache:omb_hist03z1_fy2027.xlsx + params:omb", marginal=False,
               detail=r_detail, missing=r_missing,
               national_dollars=float(np.abs(central) @ weights_full))
        ch.add("R", "central_marginal_part", central_marginal, source="internal",
               marginal=True, hidden=True)
        ch.add("R", "all_per_capita", sum(w for _, _, w, _ in r_parts) + zero_vector,
               source="cache:omb_hist03z1_fy2027.xlsx + params:omb", marginal=True,
               note="the same netted function amounts, every one of them per capita, plus the "
                    "seven functions the central arm prices at zero")
        if f604 is not None and not np.array_equal(housing_by_subsidy, housing_per_capita):
            ch.add("R", "central_housing_by_reported_subsidy",
                   central - housing_per_capita + housing_by_subsidy,
                   source="cache:omb_hist03z1_fy2027.xlsx + params:omb", marginal=False,
                   note="the central arm with subfunction 604 housing assistance allocated by "
                        "each record's share of the reported SPM capped housing subsidy instead "
                        "of per capita; every other part is unchanged",
                   housing_dollars=net604)
        r_central = "central"
    else:
        drop("R", "no function of the rest of the federal budget could be priced")
        ch.add("R", "all_per_capita", zero_vector,
               source="cache:omb_hist03z1_fy2027.xlsx", marginal=True)
        r_central = None
    ch.add("R", "all_zero", np.zeros(len(d)), source="convention", marginal=False)
    if r_missing:
        drop("R(sub-items)", "not priced for lack of a verified parameter: " + "; ".join(r_missing))

    # ---- F: federal pure public goods -------------------------------------
    tricare_base = ctx["donor_payer_means"]["tricare"][ctx["donor_codes"]] * ctx["exposure"] * civilian
    tricare_priced = float(tricare_base @ weights_full)
    f_total = func("050") + func("900") + func("800") - tricare_priced
    ch.add("F", "zero", np.zeros(len(d)), source="convention", marginal=True)
    flat_f = per_capita_of(f_total)
    ch.add("F", "per_capita", flat_f, source="cache:omb_hist03z1_fy2027.xlsx", marginal=True,
           national_dollars=f_total, tricare_already_priced=tricare_priced)
    record_national("F", "per_capita", f_total, flat_f, "flat_per_capita")
    fed_tax_basis = unit_share(np.clip(d.FEDTAX_AC.to_numpy(dtype=float)
                                       + d.FICA.to_numpy(dtype=float), 0, None))
    ch.add("F", "proportional_to_federal_tax", proportional(f_total, fed_tax_basis, sign=-1.0),
           source="cache:omb_hist03z1_fy2027.xlsx", marginal=True, national_dollars=f_total)

    # ---- S: state-funded coverage for undocumented residents --------------
    # No per-state map was verified, so the map is assembled here from the
    # individual verified state budget lines, each named with its own scope and
    # period. Biennial figures are halved to an annual rate; that annualization
    # is arithmetic on a verified number, and it is recorded. Every state whose
    # line could not be verified is dropped and named.
    S_LINES = [
        (17, "il_hbia_hbis_total_state_cost", 1.0,
         "Illinois, Health Benefits for Immigrant Adults plus Seniors, annual state cost"),
        (36, "ny_ep_to_medicaid_state_cost_annual", 1.0,
         "New York, Essential Plan population moved to state-funded Medicaid, annual state cost"),
        (8, "co_omnisalud_subsidy_spend_py2026", 1.0,
         "Colorado, OmniSalud subsidy spending, plan year 2026"),
        (41, "or_healthier_oregon_gf_2023_25", 0.5,
         "Oregon, Healthier Oregon general fund, 2023-25 biennium halved to an annual rate"),
        (53, "wa_apple_health_expansion_service_dollars_2023_25", 0.5,
         "Washington, Apple Health Expansion service dollars, 2023-25 biennium halved"),
        (6, "ca_full_scope_medical_adults_26_49_general_fund", 1.0,
         "California, full-scope Medi-Cal general fund for adults 26-49 ONLY; a "
         "partial-population floor, not California's all-ages total, which is not verified"),
    ]
    s_map, s_detail, s_dropped_states = {}, [], []
    for state_fips, key, factor, note in S_LINES:
        value = p.pick("state_medicaid_undocumented", [key], "money", preferred=key)
        if value is None:
            s_dropped_states.append(f"{key}: not verified")
            continue
        s_map[state_fips] = value * factor
        s_detail.append(dict(fips=state_fips, key=key, published=value,
                             annualization_factor=factor, annual_dollars=value * factor,
                             note=note))
    for missing in ["mn_minnesotacare_undocumented_state_cost", "ma_health_safety_net_state_cost",
                    "co_cover_all_coloradans_children_state_cost",
                    "ca_undocumented_total_general_fund_2024_25"]:
        if p.pick("state_medicaid_undocumented", [missing], "money", preferred=missing) is None:
            s_dropped_states.append(f"{missing}: not verified")
    # The 50% already-inside-MEPS split is the brief's stated convention, not an
    # external parameter; the 0% and 100% arms bracket it.
    s_inside_param = p.first("state_medicaid_undocumented", [["inside", "meps"]], "share",
                             preferred="share_already_inside_meps")
    s_inside = 0.5 if s_inside_param is None else s_inside_param
    if s_map and unauth_total and unauth_mex:
        share = unauth_mex / unauth_total
        state_cost = pd.Series(fips).map(s_map).fillna(0.0).to_numpy(dtype=float)
        pop_by_state = np.bincount(fips, weights=weights_full * mex_noncit, minlength=60)
        denom = np.where(pop_by_state[fips] > 0, pop_by_state[fips], 1.0)
        covered = mex_noncit & (state_cost > 0) & (pop_by_state[fips] > 0)
        for arm, inside in [("half_inside_meps", s_inside), ("none_inside_meps", 0.0),
                            ("all_inside_meps", 1.0)]:
            vector = np.where(covered, -state_cost * share * (1.0 - inside) / denom, 0.0)
            ch.add("S", arm, vector, source="params:state_medicaid_undocumented, assembled "
                                            "from individual verified state lines",
                   marginal=False, share_already_inside_meps=inside,
                   mexico_share_of_the_unauthorized=share,
                   mexico_share_is_national_not_state_specific=True,
                   states=s_detail, states_dropped=s_dropped_states)
        drop("S(states without a verified line)",
             "priced for " + ", ".join(str(f) for f in sorted(s_map)) +
             " only; not priced: " + "; ".join(s_dropped_states))
    else:
        drop("S", "no state general-fund coverage cost for undocumented residents was verified")

    centrals = dict(G=g_central, K="central",
                    P="net_of_item_G" if "P|net_of_item_G" in ch.meta else None,
                    D="central" if "D|central" in ch.meta else None,
                    U="central" if "U|central" in ch.meta else None,
                    I="central" if "I|central" in ch.meta else None,
                    M="central" if "M|central" in ch.meta else None,
                    E="zero", C=c_central, X=x_central, R=r_central, F="zero",
                    S="all_inside_meps" if "S|all_inside_meps" in ch.meta else None)
    ch.meta["E|zero"]["rule"] = "enforcement outlays are owned by R750; appropriation-based E is a standalone allocation sensitivity only"
    if "S|all_inside_meps" in ch.meta:
        ch.meta["S|all_inside_meps"]["rule"] = "no extra mixed-year 2025/2026 coverage appropriation in a 2024 account; overlap unverified"
    return ch, dropped, centrals, national, ratio_inversion_check


# --------------------------------------------------------------------------
# Main
# --------------------------------------------------------------------------

def sdr_se(values: np.ndarray) -> float:
    values = np.asarray(values, dtype=float)
    return float(np.sqrt(4 / 160 * np.square(values[1:] - values[0]).sum()))


def generate(args):
    out = Path(args.out_dir) if getattr(args, "out_dir", None) else HERE / "derived"
    out.mkdir(parents=True, exist_ok=True)
    if getattr(args, "off", None):
        print(f"[off] items switched off at the command line: {sorted(set(args.off))}",
              flush=True)
    params = Params(args.params, args.allow_placeholder)
    if not args.allow_placeholder:
        bad = [f"{g}.{k}" for g, entries in params.raw.items() if isinstance(entries, dict)
               for k, v in entries.items()
               if isinstance(v, dict) and "status" in v and str(v["status"]).lower() != "verified"]
        print(f"[params] {params.path.name}: {len(bad)} entries are not verified and will be refused",
              flush=True)

    for name in EXTRA_PERSON:
        if name not in ext.base.PERSON:
            ext.base.PERSON.append(name)

    cps = GENEXT / "_cache/asecpub25csv.zip"
    medical_zip = ROOT / "sources/immigration-fiscal/data/external/stage3/ahrq/meps_2024/h256dat.zip"
    medical_sas = medical_zip.with_name("h256su.txt")
    print("[stage] building the upstream CPS state", flush=True)
    state = ext.build(argparse.Namespace(cps_zip=cps))
    d = state["d"]
    index, n_units = state["index"], state["n_units"]
    weights = state["person_weights"]
    civilian = (d.PRPERTYP.eq(2) | d.A_AGE.lt(15)).to_numpy()
    groups = {name: state["group"][name] & civilian for name in TARGETS + [WHITE, ALL_NATIVE]}
    groups[NATIONAL] = civilian.copy()
    member_count = sum(groups[name].astype(int) for name in TARGETS)
    if member_count.max() > 1:
        raise ValueError("Target categories overlap")
    bands = np.digitize(d.A_AGE, [18, 25, 35, 45, 55, 65, 75])
    heads = d.loc[d.SPM_HEAD.eq(1)].sort_values("SPM_ID")

    # Base account matrix, identical construction to the upstream lane.
    totals = state["totals"]
    share = lambda x: ext.allocate(x, index, np.ones(len(d), bool), n_units)
    unit = [totals[k] for k in ["modeled_tax_total", "selected_cash_total", "selected_noncash_total",
                                "employer_payroll", "sales_tax_share35", "property_tax_owner"]]
    unit += [ext.PUPIL_RATIO_NATIVE_ACS * totals["k12_cost_at_full_attendance"], totals["school_lunch"]]
    base_matrix = np.column_stack([share(x) for x in unit])
    for k, total in enumerate(unit):
        actual = np.bincount(index, weights=base_matrix[:, k], minlength=n_units)
        if not np.allclose(actual, total, rtol=1e-10, atol=1e-5):
            raise ValueError(f"Unit conservation failed for {COMPONENTS[k]}")

    print("[stage] MEPS donor transport", flush=True)
    medical, anchors = read_meps(medical_zip, medical_sas)
    cells, codes, covariance = donor_model(medical, d, False)
    means = cells.mean_public_paid.to_numpy()
    exposure = ~(d.PUB.eq(0) & d.PRIV.eq(0)).to_numpy()
    health = np.eye(len(cells))[codes] * exposure[:, None]
    valid = medical.PERWT24F.gt(0) & medical.AGE24X.ge(0) & medical.BORNUSA.isin([1, 2])
    sample = medical.loc[valid]
    payer_means = {}
    for label, column in [("medicaid", "TOTMCD24"), ("medicare", "TOTMCR24"), ("tricare", "TOTTRI24")]:
        wx = sample.assign(wx=sample[column] * sample.PERWT24F).groupby(["age_band", "born"]).wx.sum()
        pop = sample.groupby(["age_band", "born"]).PERWT24F.sum()
        series = (wx / pop).reindex(pd.MultiIndex.from_frame(cells[["age_band", "born"]]))
        if series.isna().any():
            raise ValueError(f"missing donor cell for {label}")
        payer_means[label] = series.to_numpy()

    print("[stage] cached aggregates", flush=True)
    pop_state = resid.read_state_population()
    gs_pc, gs_national = resid.read_general_services_per_capita(pop_state)
    cap_pc, cap_national, cap_components = read_cog_capital(
        RESIDUAL / "_cache/22slsstab1.xlsx", pop_state)
    print(f"[capital] 2022 state-local direct general capital outlay "
          f"${cap_components['capital_total']/1e9:,.1f}bn: "
          f"${cap_components['elsec_capital']/1e9:,.1f}bn elementary and secondary, "
          f"${cap_components['capital_inside_item_G']/1e9:,.1f}bn already inside the item G "
          f"general-services residual, ${cap_national['net_of_item_G']/1e9:,.1f}bn unpriced "
          f"(briefed gross arm would charge ${cap_national['briefed_gross']/1e9:,.1f}bn)",
          flush=True)
    assf = read_assf_k12(GENEXT / "census_assf_fy2024_summary_tables.xlsx")
    omb = read_omb_functions(RESIDUAL / "_cache/omb_hist03z1_fy2027.xlsx")
    missing_functions = [c for c, n in OMB_FUNCTION_ROWS.items() if n not in omb]
    if missing_functions:
        raise ValueError(f"OMB Table 3.1 rows absent: {missing_functions}")
    # The cached Table 3.1 and the researcher's independently fetched Table 3.2
    # must agree on every function they both carry.
    omb_crosscheck = []
    for key, entry in (params.raw.get("omb") or {}).items():
        m = re.match(r"^func_(\d{3})_", key)
        if not m or not isinstance(entry, dict) or entry.get("value") is None:
            continue
        code = m.group(1)
        if code not in OMB_FUNCTION_ROWS:
            continue
        cached = omb[OMB_FUNCTION_ROWS[code]]
        fetched = float(entry["value"]) * 1e6
        omb_crosscheck.append(dict(code=code, key=key, cached=cached, params=fetched,
                                   relative=abs(cached - fetched) / max(abs(cached), 1.0),
                                   agree=abs(cached - fetched) <= max(abs(cached), 1.0) * 1e-9))
    disagree = [r for r in omb_crosscheck if not r["agree"]]
    if disagree:
        raise SystemExit(f"[BLOCKED] cached OMB Table 3.1 disagrees with the fetched "
                         f"parameters on {[r['code'] for r in disagree]}")
    print(f"[cross-check] {len(omb_crosscheck)} OMB functions agree between the cached "
          f"Table 3.1 and the fetched parameters", flush=True)

    n_civilian = float(weights[civilian, 0].sum())
    us_resident = params.pick("population", ["2024"], "count")
    population_vintage = "NST-EST2024 (params)"
    if us_resident is None:
        raise ValueError("Missing verified 2024 resident population; a prior-year denominator is not a fallback")
    print(f"[population] resident denominator {us_resident:,.0f} ({population_vintage})", flush=True)
    ctx = dict(d=d, index=index, n_units=n_units, civilian=civilian, weights=weights,
               heads=heads, general_services=(gs_pc, gs_national), assf=assf, omb=omb,
               donor_codes=codes, donor_payer_means=payer_means, exposure=exposure,
               n_civilian=n_civilian, us_resident=us_resident,
               consumption_proxy=base_matrix[:, 4],
               capital=(cap_pc, cap_national, cap_components),
               off=list(args.off or []),
               is_white_ref=groups[WHITE], is_target=member_count > 0)

    print("[gate 0] reproducing the upstream union absolute before any new item", flush=True)
    base_only = sufficient(base_matrix, health, weights, groups, bands, 8)
    base_only[UNION] = sum_cells([base_only[g] for g in TARGETS])
    gate0_value = float(account(base_only[UNION], COEFFICIENTS, means).sum(axis=0)[0])
    stored = pd.read_csv(ALL_AGE / "derived/estimates.csv")
    stored_union = float(stored[(stored.scenario == "all_age_shared")
                                & (stored.target == UNION)
                                & (stored.metric == "absolute_total")].estimate.iloc[0])
    gate0_residual = gate0_value - stored_union
    gate0 = abs(gate0_residual) <= 1.0
    print(f"[gate 0] reproduced {gate0_value/1e9:+.5f}bn vs stored {stored_union/1e9:+.5f}bn, "
          f"residual ${gate0_residual:,.2f} -> {'PASS' if gate0 else 'FAIL'}", flush=True)
    if not gate0:
        raise SystemExit(f"[BLOCKED] gate 0 failed: residual {gate0_residual}")
    del base_only

    print("[stage] building item charges", flush=True)
    charges, dropped, centrals, national, ratio_inversion = build_charges(ctx, params)
    for row in ratio_inversion:
        print(f"[inversion] {row['program']}: published coverage {row['published_coverage_ratio']}"
              f" -> admin/survey {row['parameter_admin_over_survey']} "
              f"(recomputed {row['recomputed_admin_over_survey']:.4f}) -> "
              f"{'PASS' if row['agree'] else 'FAIL'}", flush=True)
    item_matrix = charges.matrix()
    values = np.column_stack([base_matrix, item_matrix]) if item_matrix.size else base_matrix

    print("[stage] replicate aggregation", flush=True)
    stats = sufficient(values, health, weights, groups, bands, 8)
    stats[UNION] = sum_cells([stats[g] for g in TARGETS])

    base_coeff = np.concatenate([COEFFICIENTS, np.zeros(item_matrix.shape[1])])
    base_rep = {g: account(stats[g], base_coeff, means).sum(axis=0) for g in REPORT_GROUPS}
    populations = {g: stats[g]["n"].sum(axis=0) for g in REPORT_GROUPS}

    # The base account recomputed alongside the items must still be the gated one.
    if abs(float(base_rep[UNION][0]) - gate0_value) > 1.0:
        raise SystemExit("[BLOCKED] base account moved once item columns were added")

    # ---- institutional external add --------------------------------------
    inst_cost, inst_pop, _ = institutional_cost_by_band(INSTITUTIONAL / "derived/acs_cells.csv")
    acs_white_total = sum(inst_pop[("native_nh_white", b)] for b in ACS_BANDS)
    acs_shares = {b: inst_pop[("native_nh_white", b)] / acs_white_total for b in ACS_BANDS}
    cps_band_pop = {g: stats[g]["n"][:, 0] for g in REPORT_GROUPS}
    usborn_split = {}
    for b_idx, b in enumerate(ACS_BANDS):
        denom = cps_band_pop["mexican_second_gen"][b_idx] + cps_band_pop["mexican_third_plus_selfid"][b_idx]
        usborn_split[b] = (cps_band_pop["mexican_second_gen"][b_idx] / denom,
                           cps_band_pop["mexican_third_plus_selfid"][b_idx] / denom)
    inst_by_group = {}
    for g, acs_key in [("mexico_born", "mexico_born"), (WHITE, "native_nh_white"),
                       (ALL_NATIVE, "all_natives")]:
        inst_by_group[g] = np.array([inst_cost[(acs_key, b)] for b in ACS_BANDS])
    inst_by_group["mexican_second_gen"] = np.array(
        [inst_cost[("usborn_mexican", b)] * usborn_split[b][0] for b in ACS_BANDS])
    inst_by_group["mexican_third_plus_selfid"] = np.array(
        [inst_cost[("usborn_mexican", b)] * usborn_split[b][1] for b in ACS_BANDS])
    inst_by_group[UNION] = (inst_by_group["mexico_born"]
                            + inst_by_group["mexican_second_gen"]
                            + inst_by_group["mexican_third_plus_selfid"])
    inst_acs_pop = {"mexico_born": "mexico_born", WHITE: "native_nh_white",
                    ALL_NATIVE: "all_natives", "mexican_second_gen": "usborn_mexican",
                    "mexican_third_plus_selfid": "usborn_mexican", UNION: "mexican_total"}

    ACS_REF = {WHITE: "native_nh_white", ALL_NATIVE: "all_natives"}

    def _inst_per_person(g, b):
        """Per-person institutional cost in a band, on ACS populations."""
        key = "usborn_mexican" if g in {"mexican_second_gen", "mexican_third_plus_selfid"} \
            else inst_acs_pop[g]
        return inst_cost[(key, b)] / inst_pop[(key, b)]

    def _inst_band_population(g, b_idx, b):
        """ACS band population for a CPS group, splitting the pooled US-born cell."""
        if g in {"mexican_second_gen", "mexican_third_plus_selfid"}:
            which = 0 if g == "mexican_second_gen" else 1
            return inst_pop[("usborn_mexican", b)] * usborn_split[b][which]
        return inst_pop[(inst_acs_pop[g], b)]

    def inst_standardized_gap(g, reference=WHITE):
        ref_key = ACS_REF[reference]
        total = 0.0
        for b in ACS_BANDS:
            per_r = inst_cost[(ref_key, b)] / inst_pop[(ref_key, b)]
            total += acs_shares[b] * (-_inst_per_person(g, b) + per_r)
        return total

    def inst_age_matched_gap(g, reference=WHITE):
        """Change in the age-matched total gap, on ACS populations throughout."""
        ref_key = ACS_REF[reference]
        total = 0.0
        for b_idx, b in enumerate(ACS_BANDS):
            n_g = _inst_band_population(g, b_idx, b)
            total -= (_inst_per_person(g, b) * n_g
                      - (n_g / inst_pop[(ref_key, b)]) * inst_cost[(ref_key, b)])
        return total

    # ---- per-item aggregation --------------------------------------------
    white_cell, white_n = stats[WHITE], stats[WHITE]["n"]
    white_age_totals = np.bincount(bands[groups[WHITE]], weights=weights[groups[WHITE], 0], minlength=8)
    white_shares = white_age_totals / white_age_totals.sum()

    item_rows, item_rep = [], {}
    for k, key in enumerate(charges.columns):
        meta = charges.meta[key]
        item, arm = meta["item"], meta["arm"]
        col = 8 + k
        for g in REPORT_GROUPS:
            cell = stats[g]
            y_band = cell["y"][:, col, :]
            total = y_band.sum(axis=0)
            item_rep[f"{key}|{g}"] = total
            if meta.get("hidden"):
                continue
            n = populations[g]
            per_band_g = y_band[:, 0] / cell["n"][:, 0]
            per_band_w = white_cell["y"][:, col, 0] / white_n[:, 0]
            gap = float((white_shares * (per_band_g - per_band_w)).sum())
            item_rows.append(dict(item=item, arm=arm, label=ITEM_LABEL.get(item, item),
                                  group=g, total_bn=total[0] / 1e9,
                                  per_person=total[0] / n[0], se_bn=sdr_se(total) / 1e9,
                                  common_age_gap_per_person_vs_white=gap,
                                  source=meta.get("source"), external=False))
    for g in REPORT_GROUPS:
        total = -float(inst_by_group[g].sum())
        item_rows.append(dict(item="N", arm="midpoint", label=ITEM_LABEL["N"], group=g,
                              total_bn=total / 1e9, per_person=total / populations[g][0],
                              se_bn=0.0,
                              common_age_gap_per_person_vs_white=inst_standardized_gap(g)
                              if g in ACS_REF or g in inst_acs_pop else 0.0,
                              source="external:institutional_bound_2026_09_17", external=True))
    items_table = pd.DataFrame(item_rows)
    items_table.to_csv(out / "items_by_group.csv", index=False)

    # ---- aggregates the national reconciliation needs ---------------------
    pop_ratio = n_civilian / us_resident
    deflator_used = float(charges.meta.get("G|deflated2024", {}).get("deflator", 1.0))
    sl_own_revenue, sl_capital = read_cog_national_lines(RESIDUAL / "_cache/22slsstab1.xlsx")
    p_total_outlays = params.pick("omb", ["total_outlays"], "money", preferred="total_outlays")
    p_total_receipts = params.pick("omb", ["receipts_total"], "money", preferred="receipts_total")
    if p_total_outlays is None or p_total_receipts is None:
        raise SystemExit("[BLOCKED] the consolidated federal totals are not verified")
    func_050, func_900, func_800 = omb[OMB_FUNCTION_ROWS["050"]], omb[OMB_FUNCTION_ROWS["900"]], \
        omb[OMB_FUNCTION_ROWS["800"]]
    func_950 = params.pick("omb", ["950"], "money",
                           preferred="func_950_undistributed_offsetting_receipts")
    func_920 = params.pick("omb", ["920"], "money", preferred="func_920_allowances")
    if func_950 is None or func_920 is None:
        raise ValueError("Missing verified OMB 950/920; an absent budget series is not zero")

    # ---- complete-account gaps against both references --------------------
    # The absolute balance answers "what does this group cost". The gap answers
    # "compared with whom". Both are carried to the complete account: the
    # age-matched total in dollars and the common-age balance per standardized
    # person, each starting from the upstream partial gap.
    zero_means = np.zeros_like(means)
    column_of = {key: 8 + i for i, key in enumerate(charges.columns)}
    gap_rows, gap_detail = [], []
    for g in TARGETS + [UNION]:
        cell = stats[g]
        for reference in [WHITE, ALL_NATIVE]:
            ref = stats[reference]
            base_std, _ = standardized_gap(cell, ref, base_coeff, means, white_shares)
            base_matched, _ = contrast(cell, ref, base_coeff, means, True)
            std_total = base_std.copy()
            matched_total = base_matched.copy()
            for item in WATERFALL_ORDER:
                if item == "N":
                    std_item = np.full(161, inst_standardized_gap(g, reference))
                    matched_item = np.full(161, inst_age_matched_gap(g, reference))
                    external = True
                else:
                    arm = centrals.get(item)
                    if arm is None:
                        continue
                    coeff = np.zeros(len(base_coeff))
                    coeff[column_of[f"{item}|{arm}"]] = 1.0
                    std_item, _ = standardized_gap(cell, ref, coeff, zero_means, white_shares)
                    matched_item, _ = contrast(cell, ref, coeff, zero_means, True)
                    external = False
                std_total = std_total + std_item
                matched_total = matched_total + matched_item
                gap_detail.append(dict(group=g, reference=reference, item=item,
                                       arm="midpoint" if external else centrals.get(item),
                                       common_age_gap_per_person=std_item[0],
                                       age_matched_gap_bn=matched_item[0] / 1e9,
                                       external=external))
            gap_rows.append(dict(
                group=g, reference=reference,
                base_common_age_gap_per_person=base_std[0],
                complete_common_age_gap_per_person=std_total[0],
                base_common_age_se=sdr_se(base_std),
                complete_common_age_se=sdr_se(std_total),
                base_age_matched_gap_bn=base_matched[0] / 1e9,
                complete_age_matched_gap_bn=matched_total[0] / 1e9,
                base_age_matched_se_bn=sdr_se(base_matched) / 1e9,
                complete_age_matched_se_bn=sdr_se(matched_total) / 1e9))
    complete_gaps = pd.DataFrame(gap_rows)
    complete_gaps.to_csv(out / "complete_gaps.csv", index=False)
    pd.DataFrame(gap_detail).to_csv(out / "complete_gaps_by_item.csv", index=False)

    # Anchor the starting gaps against the upstream lane's published estimates.
    gap_anchor = []
    for g in TARGETS + [UNION]:
        for reference, metric, column, scale in [
                (WHITE, "standardized_gap_per_person", "base_common_age_gap_per_person", 1.0),
                (ALL_NATIVE, "standardized_gap_per_person", "base_common_age_gap_per_person", 1.0)]:
            match = stored[(stored.scenario == "all_age_shared") & (stored.target == g)
                           & (stored.reference == reference) & (stored.metric == metric)]
            if not len(match):
                continue
            mine = float(complete_gaps[(complete_gaps.group == g)
                                       & (complete_gaps.reference == reference)][column].iloc[0])
            upstream = float(match.estimate.iloc[0]) * scale
            gap_anchor.append(dict(group=g, reference=reference, metric=metric,
                                   upstream=upstream, rebuilt=mine,
                                   agree=abs(mine - upstream) <= 0.01))
    bad_anchor = [a for a in gap_anchor if not a["agree"]]
    if bad_anchor:
        raise SystemExit(f"[BLOCKED] the rebuilt partial gap does not match the upstream "
                         f"published estimate: {bad_anchor}")
    print(f"[gap anchor] {len(gap_anchor)} upstream partial gaps reproduced", flush=True)

    # ---- national reconciliation against the consolidated budget position --
    national_cell = stats[NATIONAL]
    def national_total(coeff, medical):
        return float(account(national_cell, coeff, medical).sum(axis=0)[0])

    account_base = national_total(base_coeff, means)
    lines, account_outlays, account_receipts = [], 0.0, 0.0
    for k, name in enumerate(COMPONENTS):
        coeff = np.zeros(len(base_coeff))
        coeff[k] = COEFFICIENTS[k]
        value = national_total(coeff, zero_means)
        lines.append(dict(block="account", line=f"base component {name}", amount_bn=value / 1e9,
                          note="charged over the civilian household population"))
        if name in {"tax", "employer", "sales", "owner_property"}:
            account_receipts += value
        else:
            account_outlays -= value
    medical_value = -float(np.einsum("bjr,j->br", national_cell["h"], means)[:, 0].sum())
    lines.append(dict(block="account", line="base component public medical", amount_bn=medical_value / 1e9,
                      note="MEPS public-payer transport"))
    account_outlays += -min(medical_value, 0.0)
    for item in WATERFALL_ORDER:
        if item == "N":
            # The ACS cells cover natives and the Mexico-born, not every resident,
            # so this national line is a partial count and is labelled as one.
            value = -float(sum(inst_cost[("all_natives", b)] + inst_cost[("mexico_born", b)]
                               for b in ACS_BANDS))
            lines.append(dict(block="account", line="item N institutional care",
                              amount_bn=value / 1e9,
                              note="external ACS-based add covering natives plus the Mexico-born "
                                   "only, not every resident; not a CPS charge"))
            account_outlays += -min(value, 0.0)
            continue
        arm = centrals.get(item)
        if arm is None:
            lines.append(dict(block="account", line=f"item {item}", amount_bn=0.0,
                              note="dropped for want of a verified parameter"))
            continue
        coeff = np.zeros(len(base_coeff))
        coeff[column_of[f"{item}|{arm}"]] = 1.0
        value = national_total(coeff, zero_means)
        lines.append(dict(block="account", line=f"item {item} ({arm})", amount_bn=value / 1e9,
                          note=ITEM_LABEL[item]))
        if item in {"C", "X"}:
            account_receipts += value
        else:
            account_outlays -= value
        if item == "G":
            fee_mapping = charges.meta[f"G|{arm}"]["fees_by_state_per_capita"]
            fees_allocated = float((d.GESTFIPS.map(fee_mapping).to_numpy(dtype=float)
                                    * deflator_used * civilian) @ weights[:, 0])
            # G is stored net. Gross coverage accounting puts fees on receipts;
            # lunch/D corrections, by contrast, reverse expenditure only.
            account_receipts += fees_allocated
            account_outlays += fees_allocated
    account_position = sum(r["amount_bn"] for r in lines if r["block"] == "account") * 1e9

    federal_outlays = p_total_outlays
    federal_receipts = p_total_receipts
    sl_expenditure = gs_national["direct_general_total"] * deflator_used
    sl_revenue = sl_own_revenue * deflator_used
    from consolidation import census_finance
    sl_grants = census_finance(RESIDUAL / "_cache/22slsstab1.xlsx")["United States Total"]["federal_grants"] * deflator_used
    consolidated_outlays = federal_outlays + sl_expenditure - sl_grants
    consolidated_receipts = federal_receipts + sl_revenue
    consolidated_position = consolidated_receipts - consolidated_outlays
    for label, value, note in [
            ("federal outlays FY2024", -federal_outlays, "OMB Table 2.1/3.1 total outlays"),
            ("federal receipts FY2024", federal_receipts, "OMB Table 2.1 total receipts"),
            ("state and local direct general expenditure", -sl_expenditure,
             f"2022 Census of Governments, inflated by {deflator_used:.6f}"),
            ("state and local general revenue from own sources", sl_revenue,
             f"2022 Census of Governments, inflated by {deflator_used:.6f}"),
            ("state and local federal grants consolidation adjustment", sl_grants,
             "removes intergovernmental financing once; Census 2022 inflated, not a matched-FY cash identity"),
            ("consolidated position", consolidated_position, "mixed-vintage general-finance comparator, not an exact whole-government total")]:
        lines.append(dict(block="consolidated", line=label, amount_bn=value / 1e9, note=note))
    national_residual = consolidated_position - account_position
    for label, value, note in [
            ("item F charged at zero in the central arm", -charges.meta["F|per_capita"]["national_dollars"],
             "defense, net interest and general government less TRICARE already in base medical"),
            ("OMB function 950 undistributed offsetting receipts", -func_950, "negative outlays increase the balance; never priced"),
            ("OMB function 920 allowances", -func_920, "never priced"),
            ("state and local capital outlay, elementary and secondary share",
             -cap_components["elsec_capital"] * deflator_used,
             "priced as item K, but from the Census F-33 FY2024 district file at "
             f"${national.get('K|central', {}).get('target_dollars', 0.0)/1e9:,.1f}bn of capital "
             "plus interest on school debt, not from "
             "this 2022 Census of Governments line; the two differ in year, in universe and "
             "in whether interest on school debt is included, so they are not the same dollars"),
            ("state and local capital outlay already inside item G",
             -cap_components["capital_inside_item_G"] * deflator_used,
             "the Census of Governments functional lines carry each function's own capital "
             "outlay inside the function total, so the general-services residual behind item G "
             "already charges the capital of every function it retains"),
            ("state and local capital outlay, non-school, priced as item P",
             -cap_national[centrals.get("P") or "net_of_item_G"] * deflator_used,
             f"item P central arm {centrals.get('P')}"),
            ("state and local capital outlay still unpriced",
             -(sl_capital - cap_components["elsec_capital"]
               - cap_components["capital_inside_item_G"]
               - cap_national[centrals.get("P") or "net_of_item_G"]) * deflator_used,
             "total direct general capital outlay less the three lines above")]:
        lines.append(dict(block="known part of the residual", line=label, amount_bn=value / 1e9,
                          note=note))
    lines.append(dict(block="residual", line="unpriced or coverage",
                      amount_bn=national_residual / 1e9,
                      note="consolidated position less the account's national sum; NOT forced to "
                           "zero and NOT an error estimate"))
    lines.append(dict(block="coverage", line="account outlays as a share of consolidated outlays",
                      amount_bn=account_outlays / consolidated_outlays,
                      note="share, not dollars"))
    lines.append(dict(block="coverage", line="account receipts as a share of consolidated receipts",
                      amount_bn=account_receipts / consolidated_receipts,
                      note="share, not dollars"))
    lines.append(dict(block="coverage", line="civilian household population over resident population",
                      amount_bn=pop_ratio, note="share, not dollars"))
    national_recon = pd.DataFrame(lines)
    national_recon.to_csv(out / "national_reconciliation.csv", index=False)
    print(f"[national] account position {account_position/1e9:+,.1f}bn vs consolidated "
          f"{consolidated_position/1e9:+,.1f}bn, residual {national_residual/1e9:+,.1f}bn; "
          f"outlay coverage "
          f"{account_outlays/consolidated_outlays:.3f}, receipt coverage "
          f"{account_receipts/consolidated_receipts:.3f}", flush=True)

    # ---- national reconciliation and cancellation gates -------------------
    recon = []
    for key, rec in national.items():
        ratio = rec["ratio"]
        expected = pop_ratio if rec["kind"] in {"flat_per_capita"} else None
        residual = None if expected is None else ratio - expected
        ok = True if expected is None else abs(residual) < 1e-9
        if rec["kind"] == "state_per_capita":
            ok = 0.85 <= ratio <= 1.05
        if rec["kind"] == "income_share":
            ok = 0.80 <= ratio <= 1.05
        if rec["kind"] == "head_based":
            ok = abs(ratio - 1.0) < 1e-9
        if rec["kind"] == "pupil_based":
            ok = 0.50 <= ratio <= 1.20
        recon.append(dict(charge=key, kind=rec["kind"], target_dollars=rec["target_dollars"],
                          charged_dollars=rec["charged_dollars"], ratio=ratio,
                          expected_population_ratio=expected, residual=residual, ok=bool(ok)))
    failed_recon = [r for r in recon if not r["ok"]]
    if failed_recon:
        raise SystemExit(f"[BLOCKED] national-total reconciliation failed: {failed_recon}")

    cancellation = {}
    for key, meta in charges.meta.items():
        if meta.get("hidden"):
            continue
        rec = national.get(key)
        if rec is None or rec["kind"] != "flat_per_capita":
            continue
        row = items_table[(items_table.item == meta["item"]) & (items_table.arm == meta["arm"])
                          & (items_table.group == UNION)]
        gap = float(row.common_age_gap_per_person_vs_white.iloc[0])
        scale = abs(float(row.per_person.iloc[0])) or 1.0
        cancellation[key] = dict(gap_per_standardized_person=gap, relative=gap / scale,
                                 passed=abs(gap / scale) < 1e-6)
    failed_cancel = {k: v for k, v in cancellation.items() if not v["passed"]}
    if failed_cancel:
        raise SystemExit(f"[BLOCKED] common-charge cancellation failed: {failed_cancel}")

    # Public pupils aged 5-17 by group, on the ledger's own pupil rule, so items
    # K, D and P can be read per pupil as well as per person.
    school_age = d.A_AGE.between(5, 17).to_numpy()
    pupils = {g: float(weights[groups[g] & school_age, 0].sum()) * ext.PUPIL_RATIO_NATIVE_ACS
              for g in TARGETS + [WHITE, ALL_NATIVE]}
    pupils[UNION] = sum(pupils[g] for g in TARGETS)

    # ---- item D: the district coverage gate, re-tested here ---------------
    # The parameter file carries one coverage ratio per state: the enrolment
    # weighted all-pupil per-pupil current spending over the F-33 state summary
    # figure. Every state either clears 10% or carries a differential of zero.
    district_gate = dict(built=False)
    dist_group = params.raw.get("district") or {}
    build_meta = params.raw.get("_district_build") or {}
    if dist_group:
        tol = float(build_meta.get("tolerance", 0.10))
        ratios = (dist_group.get("coverage_ratio_by_state") or {}).get("value") or {}
        hisp = (dist_group.get("hispanic_minus_all_by_state") or {}).get("value") or {}
        white = (dist_group.get("white_minus_all_by_state") or {}).get("value") or {}
        states = sorted(ratios)
        failing = [k for k in states if abs(float(ratios[k]) - 1.0) > tol]
        zeroed = [k for k in failing
                  if abs(float(hisp.get(k, 0.0))) < 1e-9 and abs(float(white.get(k, 0.0))) < 1e-9]
        district_gate = dict(
            built=True, tolerance=tol, states=len(states),
            min_ratio=min(float(v) for v in ratios.values()) if ratios else None,
            max_ratio=max(float(v) for v in ratios.values()) if ratios else None,
            states_failing_the_coverage_gate=failing,
            failing_states_charged_zero=zeroed,
            every_state_clears_or_is_zeroed=bool(set(failing) == set(zeroed)),
            all_51_jurisdictions=len(states) == 51,
            per_state={k: dict(coverage_ratio=float(ratios[k]),
                               hispanic_minus_all=float(hisp.get(k, float("nan"))),
                               white_minus_all=float(white.get(k, float("nan"))))
                       for k in states},
            counts=build_meta.get("counts"), sources=build_meta.get("sources"))
        if not district_gate["every_state_clears_or_is_zeroed"]:
            raise SystemExit("[BLOCKED] a state fails the district coverage gate and still "
                             f"carries a nonzero differential: "
                             f"{sorted(set(failing) - set(zeroed))}")
        if not district_gate["all_51_jurisdictions"]:
            raise SystemExit(f"[BLOCKED] the district differential covers {len(states)} "
                             "jurisdictions, expected 51")
        print(f"[district] coverage ratios {district_gate['min_ratio']:.4f} to "
              f"{district_gate['max_ratio']:.4f} over {len(states)} jurisdictions; "
              f"{len(failing)} failed the {tol:.0%} gate and carry a zero differential "
              f"{failing or ''} -> PASS", flush=True)

    # ---- item P: the capital reconciliation gate --------------------------
    # P is a per-capita charge by state of residence on the same denominator as
    # item G, so its charged-over-target ratio must be G's ratio exactly and must
    # sit within a few points of the civilian-household population ratio.
    capital_gate = dict(built=False)
    if centrals.get("P"):
        p_key = f"P|{centrals['P']}"
        g_key = f"G|{g_arm_for_gate}" if (g_arm_for_gate := centrals.get("G")) else None
        p_ratio = float(national[p_key]["ratio"])
        g_ratio = float(national[g_key]["ratio"]) if g_key in national else float("nan")
        capital_gate = dict(
            built=True, arm=centrals["P"], charge_key=p_key,
            national_target_2022=cap_national[centrals["P"]],
            national_target_2024=float(national[p_key]["target_dollars"]),
            charged_dollars=float(national[p_key]["charged_dollars"]),
            ratio=p_ratio, item_G_ratio=g_ratio, population_ratio=pop_ratio,
            item_G_ratio_difference=p_ratio - g_ratio,
            matches_item_G=abs(p_ratio - g_ratio) <= 0.05,
            within_population_ratio=abs(p_ratio - pop_ratio) <= 0.05,
            components=cap_components,
            cog_line_67_matches_the_parsed_total=abs(
                sl_capital - cap_components["capital_total"]) < 1.0,
            alternative_arm_national_2022=cap_national["briefed_gross"],
            note="the briefed gross arm charges total capital outlay less elementary and "
                 "secondary capital outlay; the central arm removes, in addition, the "
                 "capital outlay already inside the item G general-services residual")
        for flag, label in [("matches_item_G",
                             "P's per-capita ratio is far from item G's, although both are "
                             "charged per capita by state on the same 2022 denominator; the "
                             "two differ only by the state mix of the dollars"),
                            ("within_population_ratio",
                             "P does not reconcile to the population ratio"),
                            ("cog_line_67_matches_the_parsed_total",
                             "the parsed capital total disagrees with Census line 67")]:
            if not capital_gate[flag]:
                raise SystemExit(f"[BLOCKED] {label}: {capital_gate}")
        print(f"[capital] item P charged {capital_gate['charged_dollars']/1e9:,.1f}bn of "
              f"{capital_gate['national_target_2024']/1e9:,.1f}bn, ratio {p_ratio:.5f} "
              f"vs item G {g_ratio:.5f} and population ratio {pop_ratio:.5f} -> PASS",
              flush=True)

    # ---- waterfall --------------------------------------------------------
    water_rows = []
    for g in REPORT_GROUPS:
        cumulative = base_rep[g].copy()
        n = populations[g][0]
        water_rows.append(dict(group=g, step=0, item="base", label="all_age_shared absolute",
                               item_bn=0.0, cumulative_bn=cumulative[0] / 1e9,
                               cumulative_per_person=cumulative[0] / n,
                               se_bn=sdr_se(cumulative) / 1e9, flag="cps_records"))
        step = 0
        for item in WATERFALL_ORDER:
            step += 1
            if item == "N":
                delta = -float(inst_by_group[g].sum())
                cumulative = cumulative + delta
                water_rows.append(dict(group=g, step=step, item=item, label=ITEM_LABEL[item],
                                       item_bn=delta / 1e9, cumulative_bn=cumulative[0] / 1e9,
                                       cumulative_per_person=cumulative[0] / n,
                                       se_bn=sdr_se(cumulative) / 1e9,
                                       flag="external_add_no_se"))
                continue
            arm = centrals.get(item)
            if arm is None:
                water_rows.append(dict(group=g, step=step, item=item, label=ITEM_LABEL[item],
                                       item_bn=0.0, cumulative_bn=cumulative[0] / 1e9,
                                       cumulative_per_person=cumulative[0] / n,
                                       se_bn=sdr_se(cumulative) / 1e9,
                                       flag="dropped_no_verified_parameter"))
                continue
            rep = item_rep[f"{item}|{arm}|{g}"]
            cumulative = cumulative + rep
            flag = "cps_records"
            if item == "G" and arm == "nominal2022":
                flag = "degraded_fy2022_price_level"
            if item == "F" and arm == "zero":
                flag = "central_arm_is_zero"
            water_rows.append(dict(group=g, step=step, item=item, label=ITEM_LABEL[item],
                                   item_bn=rep[0] / 1e9, cumulative_bn=cumulative[0] / 1e9,
                                   cumulative_per_person=cumulative[0] / n,
                                   se_bn=sdr_se(cumulative) / 1e9, flag=flag))
    waterfall = pd.DataFrame(water_rows)
    waterfall.to_csv(out / "waterfall.csv", index=False)
    from profile_export import export_profiles
    age_profile_export = export_profiles(
        state, ctx, charges, centrals, stats, means, inst_by_group, out,
        personal_builder=lambda c: build_charges(c, Params(args.params, args.allow_placeholder)))
    for row in waterfall[waterfall.step.eq(waterfall.step.max())].itertuples():
        profile_total = age_profile_export["totals"][f"shared|expanded|{row.group}"]
        if abs(profile_total - row.cumulative_bn * 1e9) > 1.0:
            raise ValueError(f"Annual/profile sum mismatch: {row.group}")

    # ---- arms matrix ------------------------------------------------------
    def arm_vector(item, arm, g=UNION):
        if arm is None:
            return np.zeros(161)
        return item_rep[f"{item}|{arm}|{g}"]

    fixed = base_rep[UNION].copy()
    for item in WATERFALL_ORDER:
        if item in {"F", "E", "C", "R"}:
            continue
        if item == "N":
            fixed = fixed - float(inst_by_group[UNION].sum())
        elif centrals.get(item) is not None:
            fixed = fixed + arm_vector(item, centrals[item])
    def arms_of(item, order):
        """Every arm actually built for this item, the named ones first."""
        built = [m["arm"] for k, m in charges.meta.items()
                 if m["item"] == item and not m.get("hidden")]
        return [a for a in order if a in built] + [a for a in built if a not in order]

    f_arms = arms_of("F", ["zero", "per_capita", "proportional_to_federal_tax"])
    e_arms = arms_of("E", ["stock", "stock_plus_flow", "stock_pew_secondary", "zero"])
    c_arms = arms_of("C", ["wage25_capital75", "per_capita", "all_capital"])
    r_arms = arms_of("R", ["central", "central_housing_by_reported_subsidy",
                           "all_per_capita", "all_zero"])
    matrix_rows = []
    for fa in f_arms or [None]:
        for ea in e_arms or [None]:
            for ca in c_arms or [None]:
                for ra in r_arms or [None]:
                    if ea != "zero" and ra != "all_zero":
                        continue  # appropriation E duplicates enforcement inside R750
                    v = (fixed + arm_vector("F", fa) + arm_vector("E", ea)
                         + arm_vector("C", ca) + arm_vector("R", ra))
                    matrix_rows.append(dict(F_arm=fa, E_arm=ea, C_arm=ca, R_arm=ra,
                                            union_absolute_bn=v[0] / 1e9,
                                            union_per_person=v[0] / populations[UNION][0],
                                            se_bn=sdr_se(v) / 1e9))
    arms_matrix = pd.DataFrame(matrix_rows)
    arms_matrix.to_csv(out / "arms_matrix.csv", index=False)

    # ---- marginality curve ------------------------------------------------
    marginal_rep, fixed_rep = np.zeros(161), base_rep[UNION].copy()
    marginal_detail = []
    for item in WATERFALL_ORDER:
        if item == "N":
            fixed_rep = fixed_rep - float(inst_by_group[UNION].sum())
            marginal_detail.append(dict(item=item, dialled=False))
            continue
        arm = centrals.get(item)
        if arm is None:
            marginal_detail.append(dict(item=item, dialled=False, dropped=True))
            continue
        vec = arm_vector(item, arm)
        if item == "R":
            part = item_rep.get(f"R|central_marginal_part|{UNION}")
            if part is not None:
                marginal_rep = marginal_rep + part
                fixed_rep = fixed_rep + (vec - part)
                marginal_detail.append(dict(item=item, dialled="per-capita functions only"))
                continue
        if item in MARGINAL_ITEMS:
            marginal_rep = marginal_rep + vec
            marginal_detail.append(dict(item=item, dialled=True))
        else:
            fixed_rep = fixed_rep + vec
            marginal_detail.append(dict(item=item, dialled=False))
    curve_rows = []
    n_union = populations[UNION][0]
    for m in np.round(np.arange(0.0, 1.0001, 0.05), 3):
        v = fixed_rep + m * marginal_rep
        curve_rows.append(dict(m=float(m), union_absolute_bn=v[0] / 1e9,
                               union_per_person=v[0] / n_union, se_bn=sdr_se(v) / 1e9))
    curve = pd.DataFrame(curve_rows)
    slope = marginal_rep[0]
    m_star = float(-fixed_rep[0] / slope) if slope else None
    curve["break_even_m_star"] = m_star
    curve.to_csv(out / "marginality_curve.csv", index=False)

    # ---- cross-checks against the sibling lane's published figures --------
    # ledger_residual_agg_2026_09_16 reports the same two per-capita charges under
    # its equal-all-members allocation, where a per-capita charge lands on each
    # adult at exactly the per-person rate. Both must land where it said.
    sibling = []
    g_row = items_table[(items_table.item == "G") & (items_table.arm == "nominal2022")
                        & (items_table.group == UNION)]
    g_pp = -float(g_row.per_person.iloc[0])
    sibling.append(dict(check="general_services_per_person_vs_residual_agg_published_range",
                        value=g_pp, low=3738.0, high=4240.0,
                        passed=3738.0 <= g_pp <= 4240.0,
                        note="ledger_residual_agg_2026_09_16 RESULT.md, $3,738 to $4,240 per "
                             "adult across groups under equal_all_members"))
    f_row = items_table[(items_table.item == "F") & (items_table.arm == "per_capita")
                        & (items_table.group == UNION)]
    f_pp = -float(f_row.per_person.iloc[0])
    f_expected = charges.meta["F|per_capita"]["national_dollars"] / us_resident
    sibling.append(dict(check="federal_public_goods_net_of_already_priced_TRICARE",
                        value=f_pp, passed=abs(f_pp - f_expected) < 1e-6,
                        note="gross defense/interest/general government less already charged TRICARE, per resident"))
    for check in sibling:
        print(f"[sibling] {check['check']}: {check['value']:,.2f} -> "
              f"{'PASS' if check['passed'] else 'FAIL'}", flush=True)
    if not all(c["passed"] for c in sibling):
        raise SystemExit(f"[BLOCKED] a reused construction no longer matches its source lane: "
                         f"{[c for c in sibling if not c['passed']]}")

    # ---- audit ------------------------------------------------------------
    rep_saved = {k: v for k, v in item_rep.items()}
    rep_saved.update({f"base|{g}": base_rep[g] for g in REPORT_GROUPS})
    np.savez_compressed(out / "replicates.npz", **rep_saved)
    finite = all(np.isfinite(v).all() for v in rep_saved.values())
    audit = dict(
        account_status="expanded_partial",
        age_profile_export=age_profile_export,
        interpretation="annual attributed fiscal balance; not a marginal immigration effect or exhaustive fiscal account",
        params_file=str(params.path), params_sha256=params.sha256,
        params_allow_placeholder=bool(args.allow_placeholder),
        params_used=params.used, params_refused=params.refused,
        params_interpretations=params.interpretations,
        omb_cache_vs_params=omb_crosscheck,
        gate0=dict(reproduced=base_rep[UNION][0], stored=stored_union,
                   residual=gate0_residual, passed=bool(gate0)),
        civilian_household_population=n_civilian, us_resident_population=us_resident,
        resident_population_vintage=population_vintage, population_ratio=pop_ratio,
        national_reconciliation=recon, common_charge_cancellation=cancellation,
        replicate_se_finite=bool(finite), sibling_lane_crosschecks=sibling,
        admin_over_survey_inversion_check=ratio_inversion,
        items_dropped=dropped, central_arms=centrals,
        district_coverage_gate=district_gate, capital_reconciliation_gate=capital_gate,
        public_pupils_5_17_by_group=pupils,
        items_switched_off=sorted(set(args.off or [])),
        upstream_partial_gap_anchor=gap_anchor,
        national_reconciliation_vs_consolidated_budget=dict(
            account_position=account_position, consolidated_position=consolidated_position,
            residual_unpriced_or_coverage=national_residual,
            consolidated_outlays=consolidated_outlays, consolidated_receipts=consolidated_receipts,
            account_outlays=account_outlays, account_receipts=account_receipts,
            outlay_coverage=account_outlays / consolidated_outlays,
            receipt_coverage=account_receipts / consolidated_receipts,
            state_local_price_adjustment=deflator_used,
            note="the residual is reported, never forced; it is not an error estimate"),
        complete_gaps=complete_gaps.to_dict("records"),
        brief_final_step=BRIEF_FINAL_STEP,
        item_metadata={k: v for k, v in charges.meta.items() if not v.get("hidden")},
        marginality_dial=marginal_detail, break_even_m_star=m_star,
        inputs=[dict(path=str(pth), sha256=sha256(pth)) for pth in [
            cps, medical_zip, medical_sas, params.path, GENEXT / "state_parameters.csv",
            GENEXT / "census_assf_fy2024_summary_tables.xlsx",
            RESIDUAL / "_cache/omb_hist03z1_fy2027.xlsx",
            RESIDUAL / "_cache/22slsstab1.xlsx", RESIDUAL / "_cache/nst_est2023.csv",
            INSTITUTIONAL / "derived/acs_cells.csv", ALL_AGE / "derived/estimates.csv",
            Path(__file__), HERE / "consolidation.py", HERE / "profile_export.py",
            Path(ext.__file__), Path(ext.base.__file__), Path(resid.__file__), ALL_AGE / "analyze.py",
            Path(sys.modules[donor_model.__module__].__file__), ALL_AGE / "estimator.py",
            HERE / "_cache/outlays_fy2027.xlsx", HERE / "_cache/omb_hist12z3_fy2027.xlsx"]],
        medical_anchors=anchors, cps_validation=state["validation"],
        institutional_external_add=dict(
            source="institutional_bound_2026_09_17/derived/acs_cells.csv",
            arm="midpoint of that lane's adverse and moderate arms",
            group_definitions_differ=[
                "the ACS white reference is NATIVITY=1 & HISP=01 & RAC1P=1, native non-Hispanic "
                "white, not the CPS third-plus non-Hispanic white reference used everywhere else",
                "the ACS US-born Mexican group is NATIVITY=1 & HISP=02, which does not condition "
                "on parents' birthplace, so it is not exactly the union of the CPS second "
                "generation and third-plus self-identified groups",
                "the ACS cost is split between the two CPS US-born target groups in proportion "
                "to their CPS full-weight band populations, which assumes the same "
                "institutionalization rate in both",
            ],
            no_replicate_standard_error=True,
            cps_populations_vs_acs=dict(
                cps_union=float(populations[UNION][0]),
                acs_union=float(sum(inst_pop[("mexican_total", b)] for b in ACS_BANDS))),
        ),
        unpriced=[
            "OMB function 920 allowances and 950 undistributed offsetting receipts",
            "federal and state capital stock other than school capital",
            "the reported housing-subsidy base in the CPS (SPM_CAPHOUSESUB sits outside the "
            "account's selected non-cash transfers); federal housing assistance is instead "
            "carried as OMB subfunction 604 less the named physical-housing grants inside item R",
            "unmapped state-local other charges and miscellaneous general receipts",
            "unresolved federal grant recipient/timing matches outside the named transportation and physical-housing programs",
            "item S mixed-year coverage appropriations are diagnostic only; no additional 2024 central charge",
            "state and local capital outlay outside K-12 beyond what items G and P carry: "
            "the Census of Governments gives no capital sub-line for public welfare, health, "
            "airports, ports, housing and community development, general public buildings or "
            "the unallocable residual, so the split between what item G already charges and "
            "what item P adds is exact only for the functions that publish one",
            "deficit finance: the account charges outlays, not the tax burden that would fund them",
            "emigration, mortality and any lifetime or dynamic margin",
        ],
    )
    (out / "audit.json").write_text(json.dumps(audit, indent=2, default=float, allow_nan=False) + "\n")

    print("\n=== union waterfall (central arms) ===", flush=True)
    print(waterfall[waterfall.group == UNION][
        ["step", "item", "item_bn", "cumulative_bn", "se_bn", "flag"]].to_string(index=False))
    print(f"\narms matrix union absolute range: "
          f"{arms_matrix.union_absolute_bn.min():+.2f}bn to {arms_matrix.union_absolute_bn.max():+.2f}bn "
          f"over {len(arms_matrix)} combinations")
    print(f"break-even m* = {m_star}")
    print(f"items dropped for want of a verified parameter: "
          f"{[x['item'] for x in dropped] or 'none'}")
    print(f"PASS: {len(items_table)} item rows, {len(waterfall)} waterfall rows, "
          f"{len(arms_matrix)} arm combinations, {len(curve)} marginality points")


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--params", type=Path, required=True)
    ap.add_argument("--allow-placeholder", action="store_true",
                    help="development only: accept entries whose status is not `verified`")
    ap.add_argument("--off", action="append", default=[], metavar="ITEM",
                    help="switch an item off and carry it through the waterfall as a "
                         "dropped step; repeatable, e.g. --off D --off P")
    ap.add_argument("--out-dir", type=Path, default=None,
                    help="write `derived/` artefacts somewhere else, for an off-switch "
                         "reproduction run that must not clobber the published output")
    generate(ap.parse_args())


if __name__ == "__main__":
    main()
