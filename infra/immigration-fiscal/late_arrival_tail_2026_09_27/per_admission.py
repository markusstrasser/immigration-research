#!/usr/bin/env python3
"""Remaining-lifetime net fiscal value of a Mexico-born parent admitted as an LPR at 45-65,
against a same-age US-born non-Hispanic white resident's remaining lifetime.

Inputs (read-only):
  * ledger_absolute_2026_09_17 age-band components (personal allocation, expanded account),
    loaded through that lane's verified loader `lifetime.load_age_profiles` (source hashes are
    checked; it stops with [BLOCKED] on a stale export) and NVSS 2024 life tables through
    `lifetime.read_life_table`.
  * This lane's ACS tabulations: derived/late_arrival_65plus.csv (pooled 65+ receipt) and
    derived/late_arrival_tenure.csv (receipt by years since arrival; earnings by age x arrival).
  * lineage_cost_2026_09_19/derived/audit.json `senior_pricing`: public care per person-year
    for a senior outside Medicare and federal Medicaid (emergency Medicaid, state-funded
    coverage, uncompensated care), used for the five-year bar.

Arms for the admitted parent (all keep the ledger's per-capita shared items G, P, R, X, I):
  pooled_profile  the Mexico-born age profile unmodified (what the annual account charges an
                  average Mexico-born person of that age).
  observed_late   Mexico-born components rescaled to what ACS shows for people who arrived at
                  50+: earnings-linked receipts by the late/early earnings ratio at each age band;
                  Social Security + SSI cash and the Medicare/Medicaid-linked items by receipt at
                  each year since arrival. State coverage for unauthorized residents (S) and
                  enforcement (E) are zero for an LPR.
  statutory_direct  statutory without the per-capita shared items G, P, R, for parent and
                  white alike (taxes and programs only).
  statutory       observed_late, and in years 0-4 after admission the federal bars: no SSI
                  (8 U.S.C. 1612/1613, plus I-864 deeming), no SNAP (noncash), no Medicare
                  (42 U.S.C. 1395o / 1395i-2: five years' continuous LPR residence to buy in
                  without 40 quarters) and no federal Medicaid (1613); public care in those years
                  is the lineage lane's priced floor (low federal_floor, central
                  peak_state_coverage, high full_coverage_everywhere). From year 5 the observed
                  receipt by tenure applies, which embeds deeming and naturalisation as
                  practised.

Run from repo root:
  OPENBLAS_NUM_THREADS=1 uv run --no-project python3 \
      infra/immigration-fiscal/late_arrival_tail_2026_09_27/per_admission.py
"""
from __future__ import annotations

import csv
import hashlib
import importlib.util
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
LEDGER = ROOT / "infra/immigration-fiscal/ledger_absolute_2026_09_17"
LINEAGE_AUDIT = ROOT / "infra/immigration-fiscal/lineage_cost_2026_09_19/derived/audit.json"
OUT = HERE / "derived"

ARRIVAL_AGES = (45, 50, 55, 60, 65)
RATES = (0.0, 0.02, 0.03, 0.05)
CASES = ("low", "central", "high")
BAR_REGIME = {"low": "federal_floor", "central": "peak_state_coverage",
              "high": "full_coverage_everywhere"}
# Share of 65+ public medical spending carried by Medicare vs Medicaid for the medical index.
# [INFERENCE] NHEA 2022: Medicare pays roughly two-thirds of public personal health care for 65+.
MEDICARE_WEIGHT = {"low": 0.75, "central": 0.65, "high": 0.55}
EARNINGS_LINKED = ("tax", "employer", "C")
CASH_LINKED = ("cash", "U")
MEDICAL_LINKED = ("medical", "M", "N")
ZERO_FOR_LPR = ("S", "E")
# Per-capita allocations of state/local general services, their capital outlay and the rest of
# the federal budget. The statutory_direct arm drops them for parent and white alike.
PER_CAPITA_SHARED = ("G", "P", "R")
TENURE_BANDS = ((0, 4), (5, 9), (10, 14), (15, 19), (20, 200))


def load_lifetime_module():
    spec = importlib.util.spec_from_file_location("ledger_lifetime", LEDGER / "lifetime.py")
    mod = importlib.util.module_from_spec(spec)
    sys.modules["ledger_lifetime"] = mod
    spec.loader.exec_module(mod)
    return mod


def sha256(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def band_of(age: int) -> int:
    for i, (lo, hi) in enumerate(((0, 18), (18, 25), (25, 35), (35, 45), (45, 55), (55, 65),
                                  (65, 75), (75, 101))):
        if lo <= age < hi:
            return i
    raise ValueError(age)


def component_table(comp: pd.DataFrame, group: str) -> pd.DataFrame:
    c = comp[(comp.allocation == "personal") & (comp.account == "expanded") & (comp.group == group)]
    c = c.assign(pp=c.signed_total / c.population)
    t = c.pivot(index="band", columns="component", values="pp")
    assert list(t.index) == list(range(8)), group
    return t


def tenure_band(y: int) -> str:
    for lo, hi in TENURE_BANDS:
        if lo <= y <= hi:
            return f"{lo}-{hi}" if hi < 200 else f"{lo}+"
    raise ValueError(y)


class AcsRates:
    """Receipt rates, benefit means and earnings ratios from this lane's ACS tables (Mexico)."""

    def __init__(self):
        ten = pd.read_csv(OUT / "late_arrival_tenure.csv")
        self.ten = ten[(ten.group == "mexico") & ten.period.str.startswith("pooled")]

    def get(self, arrival: str, age: str, tband: str, stat: str) -> float:
        t = self.ten
        r = t[(t.arrival == arrival) & (t.current_age == age) & (t.years_since_arrival == tband)
              & (t.stat == stat)]
        assert len(r) == 1 and np.isfinite(r.estimate.iloc[0]), (arrival, age, tband, stat, len(r))
        return float(r.estimate.iloc[0])

    def late(self, age: int, years_since: int, stat: str) -> float:
        """Arrived at 50+, by current age group and years since arrival; at 55-64 the 15+
        tenure cells are empty (nobody who arrived at 50+ can be 55-64 with 15+ years), so the
        10-14 cell stands in for a parent admitted at 45."""
        cell = "65plus" if age >= 65 else "55-64"
        tb = tenure_band(years_since)
        if cell == "55-64" and tb in ("15-19", "20+"):
            tb = "10-14"
        return self.get("arr50plus", cell, tb.replace("20+", "20plus"), stat)

    def everyone(self, age: int, stat: str) -> float:
        return self.get("all", "65plus" if age >= 65 else "55-64", "all", stat)

    def earnings_ratio(self, age: int) -> float:
        band = next(b for b, lo, hi in (("50-54", 0, 54), ("55-59", 55, 59), ("60-64", 60, 64),
                                        ("65-69", 65, 69), ("70-74", 70, 74), ("75-79", 75, 200))
                    if lo <= age <= hi)
        return self.get("arr50plus_over_arr_lt50", band, "all", "ratio_mean_pernp")


def late_profile(mb: pd.DataFrame, acs: AcsRates, a0: int, arm: str, case: str,
                 bar_price: dict) -> np.ndarray:
    """Single-age net balance from a0 to 100 for a parent admitted at a0 (0 before a0)."""
    out = np.zeros(101)
    pre65_scale = mb.loc[5, "medical"] / mb.loc[6, "medical"]
    for a in range(a0, 101):
        y = a - a0
        row = mb.loc[band_of(a)].copy()
        if arm == "pooled_profile":
            out[a] = row.sum()
            continue
        barred = arm.startswith("statutory") and y < 5
        for z in ZERO_FOR_LPR:
            row[z] = 0.0
        e = acs.earnings_ratio(a)
        for k in EARNINGS_LINKED:
            row[k] *= e
        ss = acs.late(a, y, "mean_ssp_2023usd")
        ssi = 0.0 if barred else acs.late(a, y, "mean_ssip_2023usd")
        cash_ratio = (ss + ssi) / (acs.everyone(a, "mean_ssp_2023usd")
                                   + acs.everyone(a, "mean_ssip_2023usd"))
        for k in CASH_LINKED:
            row[k] *= cash_ratio
        if barred:
            # no Medicare buy-in and no federal Medicaid: public care at the priced floor
            floor = bar_price[case] * (1.0 if a >= 65 else pre65_scale)
            row["medical"], row["M"], row["N"] = -floor, 0.0, 0.0
            row["noncash"] = 0.0  # SNAP five-year bar for adults
        else:
            mcaid = acs.late(a, y, "medicaid") / acs.everyone(a, "medicaid")
            if a >= 65:
                wm = MEDICARE_WEIGHT[case]
                idx = wm * acs.late(a, y, "medicare") / acs.everyone(a, "medicare") + (1 - wm) * mcaid
            else:
                idx = mcaid  # pre-65 public medical is Medicaid-led
            for k in MEDICAL_LINKED:
                row[k] *= idx
        if arm == "statutory_direct":
            for k in PER_CAPITA_SHARED:
                row[k] = 0.0
        out[a] = row.sum()
    return out


def main() -> None:
    lt = load_lifetime_module()
    profiles, fingerprints = lt.load_age_profiles(ROOT)  # stops with [BLOCKED] if stale
    comp = pd.read_csv(LEDGER / "derived/age_profile_components.csv")
    tables = {k: lt.read_life_table(ROOT, k) for k in ("total", "hispanic", "nh_white")}
    mb = component_table(comp, "mexico_born")
    wh = component_table(comp, "third_plus_nh_white")
    # gate: components rebuild the published net profiles
    for g, t in (("mexico_born", mb), ("third_plus_nh_white", wh)):
        net = lt.age_vector(profiles, g)
        for b, (lo, _) in enumerate(lt.BANDS):
            assert abs(t.loc[b].sum() - net[lo]) < 1e-6 * max(1, abs(net[lo])), (g, b)
    audit = json.loads(LINEAGE_AUDIT.read_text())["senior_pricing"]
    bar_price = {c: audit[f"{BAR_REGIME[c]}|{c}"]["public_per_year"] for c in CASES}
    acs = AcsRates()
    white_vec = lt.age_vector(profiles, "third_plus_nh_white")
    white_direct = np.empty(101)
    for b, (lo, hi) in enumerate(lt.BANDS):
        white_direct[lo:hi] = wh.loc[b].drop(list(PER_CAPITA_SHARED)).sum()

    rows = []
    for a0 in ARRIVAL_AGES:
        for arm in ("pooled_profile", "observed_late", "statutory", "statutory_direct"):
            for case in CASES:
                vec = late_profile(mb, acs, a0, arm, case, bar_price)
                for surv in ("group_specific", "common_total"):
                    lt_key = "hispanic" if surv == "group_specific" else "total"
                    wt_key = "nh_white" if surv == "group_specific" else "total"
                    for r in RATES:
                        v_late, yrs = lt.survival_npv(vec, tables[lt_key], a0, r)
                        wv = white_direct if arm == "statutory_direct" else white_vec
                        v_white, yrs_w = lt.survival_npv(wv, tables[wt_key], a0, r)
                        rows.append({"arrival_age": a0, "arm": arm, "case": case,
                                     "survival": surv, "real_rate": r,
                                     "npv_parent": round(v_late, 1),
                                     "npv_white_same_age": round(v_white, 1),
                                     "gap_vs_white": round(v_late - v_white, 1),
                                     "discounted_person_years": round(yrs, 3)})
                if arm == "pooled_profile":
                    rows[-1 - 7:] = [dict(r, case="n/a") for r in rows[-1 - 7:]]
                    break  # case does not enter the pooled profile
    df = pd.DataFrame(rows)
    df.to_csv(OUT / "per_admission.csv", index=False, lineterminator="\n")
    prov = {"ledger_fingerprints": fingerprints,
            "lineage_audit": {str(LINEAGE_AUDIT.relative_to(ROOT)): sha256(LINEAGE_AUDIT)},
            "bar_price_per_year": bar_price, "medicare_weight": MEDICARE_WEIGHT,
            "acs_inputs": {f: sha256(OUT / f) for f in ("late_arrival_65plus.csv",
                                                         "late_arrival_tenure.csv")}}
    (OUT / "per_admission_provenance.json").write_text(json.dumps(prov, indent=1, sort_keys=True) + "\n")
    key = df[(df.survival == "group_specific") & (df.real_rate.isin([0.0, 0.03]))]
    print(key.to_string())


if __name__ == "__main__":
    main()
