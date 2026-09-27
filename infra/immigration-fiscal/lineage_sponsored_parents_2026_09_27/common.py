"""Shared loaders for the sponsored-parent lineage arms.

Imports the lineage lane (`lineage_cost_2026_09_19/lineage.py`, `inputs.py`) and the late-arrival
lane's per-admission profile (`late_arrival_tail_2026_09_27/per_admission.py`) read-only; no file
outside this directory is written (bytecode caching is switched off so the imports leave no
`__pycache__` in those lanes).
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
import sys
from pathlib import Path

sys.dont_write_bytecode = True

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
FISCAL = HERE.parent
LINEAGE_DIR = FISCAL / "lineage_cost_2026_09_19"
LATE_DIR = FISCAL / "late_arrival_tail_2026_09_27"

sys.path.insert(0, str(LINEAGE_DIR))
import inputs as I  # noqa: E402
import lineage as L  # noqa: E402

_spec = importlib.util.spec_from_file_location("per_admission", LATE_DIR / "per_admission.py")
PA = importlib.util.module_from_spec(_spec)
sys.modules["per_admission"] = PA
_spec.loader.exec_module(PA)

FOUNDER_AGE = L.FOUNDER_START_AGE  # 25
HORIZON = L.HORIZON                # 100
CENTRAL_NAME = "central (personal/expanded, unauthorized, per-capita, low fertility, 0%)"
NEVER_LEGAL_2026 = "senior rule: statutory bars plus priced care, rules_2026_new_enrollee, central"
LEGAL_Y10 = "2b founder legalised at year 10"
REGIMES = ("federal_floor", "rules_2026_new_enrollee", "peak_state_coverage",
           "full_coverage_everywhere")
CASES = ("low", "central", "high")
# Five-year bar programs for a new LPR (8 U.S.C. 1613; SNAP and federal Medicaid), in the
# absolute lane's categories; SSI sits inside `cash` and is not separable at component level.
LPR_BAR = ("medical", "M", "N", "noncash")

INPUTS = [LINEAGE_DIR / "lineage.py", LINEAGE_DIR / "inputs.py",
          LINEAGE_DIR / "derived/sensitivities.csv", LINEAGE_DIR / "derived/audit.json",
          LATE_DIR / "per_admission.py", LATE_DIR / "derived/per_admission.csv",
          LATE_DIR / "derived/late_arrival_tenure.csv", LATE_DIR / "derived/ir5_flow.csv",
          LATE_DIR / "derived/ir5_age_nis2003.csv", LATE_DIR / "derived/mexico_ir_new_vs_adjust.csv",
          FISCAL / "origin_attachment_mexico_2026_09_27/derived/naturalization_share_2024.csv"]


def sha256(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def manifest() -> dict:
    return {str(p.relative_to(FISCAL)): sha256(p) for p in INPUTS}


class Ctx:
    """Everything the lineage lane's `main()` loads, plus the per-admission inputs."""

    def __init__(self):
        self.profiles = I.age_profiles()
        self.tables = I.survival()
        self.fert = I.fertility()
        self.pen = I.unauthorized_penalty()["penalty_per_adult_year"]
        crime = I.crime_rates()
        self.crime_a1 = {"founder": crime["A1_bjs_stock"]["mexican"],
                         "descendant": crime["A1_bjs_stock"]["mexican"],
                         "white": crime["A1_bjs_stock"]["white"]}
        self.attr = I.attrition()
        self.comps = I.age_components()
        self.barred = {(al, "expanded"): I.component_vector(self.comps, self.profiles, "mexico_born",
                                                            "expanded", al, I.STATUTORY_BARRED)
                       for al in ("personal", "shared")}
        self.lpr_bar = I.component_vector(self.comps, self.profiles, "mexico_born", "expanded",
                                          "personal", LPR_BAR)
        # per-admission inputs, as per_admission.main() builds them
        comp_raw = pd.read_csv(PA.LEDGER / "derived/age_profile_components.csv")
        self.mb = PA.component_table(comp_raw, "mexico_born")
        self.acs = PA.AcsRates()
        audit = json.loads(PA.LINEAGE_AUDIT.read_text())["senior_pricing"]
        self.pricing = audit
        self.bar_price = {c: audit[f"{PA.BAR_REGIME[c]}|{c}"]["public_per_year"] for c in PA.CASES}
        self.pre65_scale = float(self.mb.loc[5, "medical"] / self.mb.loc[6, "medical"])
        mbv = I.age_vector(self.profiles, "mexico_born", "expanded", "personal")
        for b, (lo, hi) in enumerate(I.BANDS):
            if abs(self.mb.loc[b].sum() - mbv[lo]) > 1e-6:
                raise SystemExit("[BLOCKED] per-admission component table does not rebuild the "
                                 "lineage lane's Mexico-born profile")

    # ---------------------------------------------------------------- lineage
    def cfg(self, **over) -> dict:
        base = {"allocation": "personal", "account": "expanded", "gen_len": L.GEN_LEN,
                "attribution": "per_capita", "founder_status": "unauthorized",
                "senior_rule": "senior_full", "convergence": "selfid",
                "mortality": {"mexican": "total", "white": "total"},
                "penalty": self.pen, "attr": self.attr, "reference": False,
                "crime": self.crime_a1, "tfr": self.fert["low_cps2025"],
                "fertility_label": "low_cps2025"}
        return {**base, **over}

    def statutory(self, regime=None, case=None) -> dict:
        over = {"senior_rule": "senior_statutory", "senior_barred": self.barred}
        if regime is not None:
            vec, _ = I.senior_addback(regime, case)
            over["senior_addback"] = vec
        return over

    def mex(self, founder_vec=None, **over) -> dict:
        """Lineage lane's Mexican lineage; optionally with the founder's fiscal stream rebuilt
        from `founder_vec` (crime streams are left as the lane computes them and not used)."""
        cfg = self.cfg(**over)
        out = L.lineage(self.profiles, self.tables, cfg)
        if founder_vec is not None:
            f, _ = L.person_stream(founder_vec, self.tables[cfg["mortality"]["mexican"]],
                                   -FOUNDER_AGE, FOUNDER_AGE, 0.0)
            n, _, cs, ct, cn, b = out["G1"]
            out["G1"] = (n, f, cs, ct, cn, b)
        return out

    def white(self) -> dict:
        return L.lineage(self.profiles, self.tables, self.cfg(reference=True))

    def founder_vec(self, **over) -> np.ndarray:
        cfg = self.cfg(**over)
        barred = cfg.get("senior_barred")
        vec, _ = L.founder_profile(self.profiles, cfg["allocation"], cfg["account"],
                                   cfg["founder_status"], cfg["senior_rule"], cfg["penalty"],
                                   cfg.get("legalise_year"),
                                   barred[(cfg["allocation"], cfg["account"])] if barred else None,
                                   cfg.get("senior_addback"))
        return vec

    # ---------------------------------------------------------------- parents
    def parent_stream(self, vec: np.ndarray, a0: int, year: int) -> np.ndarray:
        """Calendar-year fiscal stream of one person admitted at age a0 in calendar `year`,
        survival from a0 on the common total table, cut at the lineage horizon."""
        f, _ = L.person_stream(vec, self.tables["total"], year - a0, a0, 0.0)
        return f

    def living_parents(self, a0: int, gap: int = 29) -> float:
        lx = self.tables["total"].lx.to_numpy()
        return 2.0 * lx[a0] / lx[gap]


def late_components(ctx: Ctx, a0: int, arm: str, case: str) -> pd.DataFrame:
    """`per_admission.late_profile` by component (rows = ages a0..100). Mirrors that function
    line for line; `check_late_components` gates the sum against it."""
    mb, acs, bar_price = ctx.mb, ctx.acs, ctx.bar_price
    rows = {}
    for a in range(a0, 101):
        y = a - a0
        row = mb.loc[PA.band_of(a)].copy()
        if arm == "pooled_profile":
            rows[a] = row
            continue
        barred = arm.startswith("statutory") and y < 5
        for z in PA.ZERO_FOR_LPR:
            row[z] = 0.0
        e = acs.earnings_ratio(a)
        for k in PA.EARNINGS_LINKED:
            row[k] *= e
        ss = acs.late(a, y, "mean_ssp_2023usd")
        ssi = 0.0 if barred else acs.late(a, y, "mean_ssip_2023usd")
        cash_ratio = (ss + ssi) / (acs.everyone(a, "mean_ssp_2023usd")
                                   + acs.everyone(a, "mean_ssip_2023usd"))
        for k in PA.CASH_LINKED:
            row[k] *= cash_ratio
        if barred:
            floor = bar_price[case] * (1.0 if a >= 65 else ctx.pre65_scale)
            row["medical"], row["M"], row["N"] = -floor, 0.0, 0.0
            row["noncash"] = 0.0
        else:
            mcaid = acs.late(a, y, "medicaid") / acs.everyone(a, "medicaid")
            if a >= 65:
                wm = PA.MEDICARE_WEIGHT[case]
                idx = wm * acs.late(a, y, "medicare") / acs.everyone(a, "medicare") + (1 - wm) * mcaid
            else:
                idx = mcaid
            for k in PA.MEDICAL_LINKED:
                row[k] *= idx
        if arm == "statutory_direct":
            for k in PA.PER_CAPITA_SHARED:
                row[k] = 0.0
        rows[a] = row
    return pd.DataFrame(rows).T


def to_vec(df: pd.DataFrame) -> np.ndarray:
    out = np.zeros(101)
    for a, v in df.sum(axis=1).items():
        out[int(a)] = v
    return out


def unauthorized_counterfactual(ctx: Ctx, lpr: pd.DataFrame, regime: str, case: str,
                                bars_from: int) -> np.ndarray:
    """The same parent as a resident without status: from `bars_from` the programs federal law
    closes to them (the lineage lane's STATUTORY_BARRED set) are removed and the public care
    still open to them is charged at the lineage lane's priced regime (pre-65 ages scaled by the
    Mexico-born 55-64/65+ medical ratio, as per_admission does). Before `bars_from` the row is
    the LPR row, which is how the lineage lane treats its unauthorized founder below 65."""
    _, parts = I.senior_addback(regime, case)
    care = parts["public_per_year"]
    out = np.zeros(101)
    for a, row in lpr.iterrows():
        a = int(a)
        r = row.copy()
        if a >= bars_from:
            for k in I.STATUTORY_BARRED:
                r[k] = 0.0
            r["medical"] = -care * (1.0 if a >= 65 else ctx.pre65_scale)
        out[a] = r.sum()
    return out


def disc(stream: np.ndarray, rate: float) -> float:
    return L.discount(stream, rate, 0.0)


def total_stream(lin: dict) -> np.ndarray:
    return sum(v[1] for v in lin.values())
