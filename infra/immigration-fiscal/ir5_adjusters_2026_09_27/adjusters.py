#!/usr/bin/env python3
"""Cost per admission of a Mexican parent of a US citizen (IR-5) who adjusts status inside the US.

The late-arrival tail lane values a parent who arrives new from abroad. This script values the
same green card for a parent who is already resident, with the tail lane's machinery imported
read-only (`../late_arrival_tail_2026_09_27/per_admission.py`: the ledger's Mexico-born component
profile rescaled by ACS late-arrival earnings and receipt; Hispanic survival; 2024 prices).

The admission's factual profile (the parent as an LPR) differs from a new arrival's in its clocks
(eligibility rules quoted in reads/eligibility_rules.md):
  * Medicare Part B and premium Part A: five years of continuous residence, which need not be as
    an LPR (POMS GN 00303.800 A.4); an adjuster with r years of residence waits max(0, 5 - r)
    years after the green card instead of five. Take-up then follows the new arrival's post-bar
    curve, indexed by years since Medicare eligibility.
  * Medicaid and SSI: the five-year bar runs from adjustment (8 U.S.C. 1613; POMS SI 00502.135),
    except for a parent here continuously since before 22 August 1996 (62 FR 61414).
  * SNAP: five years from adjustment unless 40 qualifying quarters, undocumented work included
    (7 CFR 273.4(a)(6)(ii); FNS 2011 guidance).
  * Social Security: all covered earnings count once a work-authorized SSN exists
    (POMS RS 00301.102 B.4.c), so a long resident's benefit can exceed a new arrival's.
  * Premium tax credit: no five-year bar for any lawfully present parent under 65 or in the
    Medicare wait (26 U.S.C. 36B; ptc.py). The ledger charges the credit per capita at every age
    inside its rest-of-budget item R; with the credit on (for new arrivals too), that share is
    swapped for the credit keyed by coverage and age, and "off" keeps the tail lane's treatment.

Counterfactuals (brief arms):
  A  stay anyway: without the green card the parent stays for life in the prior status
     (unauthorized after an overstay). The admission's cost is the change: federal programs,
     Social Security, the PTC and Medicaid long-term care replace the public-care floor that an
     unauthorized senior draws (lineage lane pricing, the same floor the tail lane uses in its
     barred years); income and payroll taxes rise from an on-books share b at the unauthorized
     wage to the full LPR wage (legalization premium pi). Everything tied to presence (per-capita
     services, excise, sales and property taxes, corporate tax on capital) is identical in both
     and cancels. Enforcement per unauthorized resident is zero centrally (the ledger keeps it
     inside the per-capita federal budget) and $565 a year as a variant.
  B  leave: without the green card the parent departs; the full factual profile counts.
  C  the evidence-based mix: adjuster types from NIS-2003 (nis_adjusters.py), each with its own
     departure without the green card: recent entrants leave at once; the others stay and leave
     at published annual emigration rates for their duration of residence and age
     (reads/emigration_quotes.json). The counterfactual stream is weighted by the probability of
     still being here; arms A and B are the no-departure and immediate-departure bounds.

Run from the repository root (after nis_adjusters.py and ptc.py):
  OPENBLAS_NUM_THREADS=1 uv run --no-project python3 \
      infra/immigration-fiscal/ir5_adjusters_2026_09_27/adjusters.py
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
import sys
from dataclasses import asdict, dataclass, replace
from pathlib import Path

import numpy as np
import pandas as pd

sys.dont_write_bytecode = True  # the tail and ledger lanes are imported read-only

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
TAIL = ROOT / "infra/immigration-fiscal/late_arrival_tail_2026_09_27"
COHORT = ROOT / "infra/immigration-fiscal/ir5_fraud_and_cohorts_2026_09_27"
OUT = HERE / "derived"

AGES = (45, 50, 55, 60, 65)
RATES = (0.0, 0.02, 0.03, 0.05)
# 2024 premiums, CMS fact sheet (reads/eligibility_rules.md section 2)
PART_A_PREMIUM = 505.0 * 12
PART_B_PREMIUM = 174.70 * 12
# Legalization wage premium: "The wage benefit of legalization under IRCA was approximately 6%"
# (Kossoudji & Cobb-Clark 2002, _cache/lit); 0.14 is the low end of their unauthorized-wage penalty.
PI = {"low": 0.0, "central": 0.06, "high": 0.14}
# Share of unauthorized earnings on the books (dataset_integrity_2026_09_23/cps.md row 1: 44/60/75%).
ONBOOKS = {"low": 0.44, "central": 0.60, "high": 0.75}
# Enforcement per unauthorized resident: ICE ERO + EOIR + appropriated USCIS ($6.207bn) over the
# OHSS January 2022 unauthorized stock (10.99m), ledger params (ledger_absolute_2026_09_17 audit.json).
E_PER_UNAUTH = (5_082_218_000 + 844_000_000 + 281_140_000) / 10_990_000
WAGE_SHARE_OF_C = 0.25  # ledger item C: 25% keyed by wages


@dataclass(frozen=True)
class Spec:
    r: float = 0.0            # years of US residence before the green card
    clock: str = "adjuster"   # "adjuster" (Medicare wait max(0, 5 - r)) or "new" (5 years)
    pre1996: bool = False     # continuous residence since before 22 Aug 1996: no Medicaid/SSI bar
    q40: bool = False         # 40 qualifying quarters: no SNAP bar
    earn: str = "late"        # "late" (ACS arrived-50+ earnings ratio) or "resident" (Mexico-born mean)
    ss: str = "late"          # Social Security: "late", "mid" or "resident" (Mexico-born mean)
    index: str = "since_lpr"  # receipt tenure: years since the green card, or "since_arrival" (r + y)
    ptc: str = "off"          # "off", "low", "central", "high"
    premiums: bool = False    # credit Medicare premiums paid by enrollees not on Medicaid


NEW_ARRIVAL = Spec(r=0.0, clock="new")
# Representative adjusters by type (nis_ir5_adjuster_types.csv: mean spells 0.9 / 3.0 / 13.9 / 34.3;
# T2 and T3 worked in the US before the green card, 43% and 100%).
TYPES = {
    "T0_recent": Spec(r=1.0),
    "T1_settling": Spec(r=3.0),
    "T2_long": Spec(r=14.0, ss="mid"),
    "T3_pre1996": Spec(r=30.0, pre1996=True, q40=True, ss="resident"),
}
LONG_TYPES = ("T2_long", "T3_pre1996")
RESIDENCE_VARIANTS = ("ss_resident", "ss_late", "q40", "index_since_arrival", "earn_resident")
# Departure without the green card, per type: (share leaving at once, annual emigration rate of
# those who stay). Keys name the level of staying, so "low" has the most departures. Rates from
# reads/emigration_quotes.json: CPS matching gives 5.0% / 3.6% / 2.0% a year after 0-4 / 5-9 / 10+
# years of residence and 2.3% for all foreign-born aged 35-64 and 65+ (Van Hook & Zhang 2011);
# residual methods give about 1.0%; MPI assumes 1.2% under 10 years and 0.7% after. Settled
# residents take 1.5% centrally [ASSUMPTION: between the residual and CPS-matching estimates; the
# CPS method also counts circular trips]. Recent entrants mostly came as visitors to adjust and
# leave at once [ASSUMPTION], a quarter staying in the high case.
DEPART = {
    "central": {"T0_recent": (1.0, 0.0), "T1_settling": (0.0, 0.036),
                "T2_long": (0.0, 0.015), "T3_pre1996": (0.0, 0.015)},
    "low": {"T0_recent": (1.0, 0.0), "T1_settling": (0.0, 0.050),
            "T2_long": (0.0, 0.023), "T3_pre1996": (0.0, 0.023)},
    "high": {"T0_recent": (0.75, 0.050), "T1_settling": (0.0, 0.012),
             "T2_long": (0.0, 0.007), "T3_pre1996": (0.0, 0.007)},
}


def sha256(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def load_tail():
    spec = importlib.util.spec_from_file_location("tail_per_admission", TAIL / "per_admission.py")
    mod = importlib.util.module_from_spec(spec)
    sys.modules["tail_per_admission"] = mod
    spec.loader.exec_module(mod)
    return mod


pa = load_tail()


class Ptc:
    """PTC per covered person by age (key-by-coverage allocation of the Treasury total), take-up
    for a lawfully present Mexican-born parent, and the per-capita share inside the ledger's R
    (ptc.py)."""

    def __init__(self):
        t = pd.read_csv(OUT / "ptc_inputs.csv", dtype={"age": str})
        amt = t[t.item == "ptc_per_covered_person"]
        self.amount = {int(a): float(v) for a, v in zip(amt.age, amt.value)}
        self.per_capita = float(t[t.item == "ptc_per_capita_inside_ledger_R"].value.iloc[0])
        self.rate = {(i.replace("mrks_rate_", ""), a): float(v)
                     for i, a, v in zip(t.item, t.age, t.value) if i.startswith("mrks_rate_")}

    def takeup(self, a: int, level: str, barred: bool) -> float:
        band = "45-54" if a < 55 else "55-59" if a < 60 else "60-64"  # 65+ in the Medicare wait: 60-64
        if level == "low":
            return self.rate[("mexico_noncitizen", band)]
        if level == "high" and barred:
            return self.rate[("all_no_employer_medicaid_medicare", band)]
        return self.rate[("mexico_naturalized", band)]

    def per_covered(self, a: int) -> float:
        return self.amount[min(max(a, 45), 69)]


def medicare_tenure(spec: Spec, y: int) -> float:
    """Tenure cell for Medicare take-up in an eligible year. The new arrival is first eligible in
    year 5 and reads the 5-9 cell; an adjuster eligible earlier reads the same first-eligible cell
    until year 5, then the new arrival's curve ("since_arrival" reads residence r + y instead)."""
    if spec.index == "since_arrival":
        return spec.r + y
    return max(y, 5)


def lpr_items(mb, acs, a0: int, spec: Spec, case: str, bar_price: dict, ptc: Ptc) -> pd.DataFrame:
    """Single-age items (2024 dollars, costs negative) for a parent who holds the green card from a0."""
    cols = list(mb.columns) + ["ptc", "premiums"]
    out = pd.DataFrame(0.0, index=range(101), columns=cols)
    pre65_scale = mb.loc[5, "medical"] / mb.loc[6, "medical"]
    floor = bar_price[case]
    wm = pa.MEDICARE_WEIGHT[case]
    mc_wait = 5.0 if spec.clock == "new" else max(0.0, 5.0 - spec.r)
    means_bar = 0 if spec.pre1996 else 5
    snap_bar = 0 if spec.q40 else 5
    for a in range(a0, 101):
        y = a - a0
        row = mb.loc[pa.band_of(a)].copy()
        row["ptc"] = row["premiums"] = 0.0
        for z in pa.ZERO_FOR_LPR:
            row[z] = 0.0
        e = acs.earnings_ratio(a) if spec.earn == "late" else 1.0
        for k in pa.EARNINGS_LINKED:
            row[k] *= e
        t = y if spec.index == "since_lpr" else int(spec.r) + y
        ss_all = acs.everyone(a, "mean_ssp_2023usd")
        ssi_all = acs.everyone(a, "mean_ssip_2023usd")
        ss_late = acs.late(a, t, "mean_ssp_2023usd")
        ss = {"late": ss_late, "resident": ss_all, "mid": 0.5 * (ss_late + ss_all)}[spec.ss]
        means_barred = y < means_bar
        ssi = 0.0 if means_barred else acs.late(a, t, "mean_ssip_2023usd")
        cash_ratio = (ss + ssi) / (ss_all + ssi_all)
        for k in pa.CASH_LINKED:
            row[k] *= cash_ratio
        mc_eligible = a >= 65 and y >= mc_wait
        mc_rate = acs.late(a, int(medicare_tenure(spec, y)), "medicare") if mc_eligible else 0.0
        if a >= 65:
            mc_ratio = mc_rate / acs.everyone(a, "medicare")
            if means_barred:
                # Medicare part as in the tail lane's index; no Medicaid; the rest at the floor
                medsum = row["medical"] + row["M"] + row["N"]
                row["medical"] = medsum * wm * mc_ratio - (1.0 - mc_rate) * floor
                row["M"], row["N"] = 0.0, 0.0
            else:
                mcaid = acs.late(a, t, "medicaid") / acs.everyone(a, "medicaid")
                idx = wm * mc_ratio + (1.0 - wm) * mcaid
                for k in pa.MEDICAL_LINKED:
                    row[k] *= idx
        elif means_barred:
            row["medical"], row["M"], row["N"] = -floor * pre65_scale, 0.0, 0.0
        else:
            idx = acs.late(a, t, "medicaid") / acs.everyone(a, "medicaid")
            for k in pa.MEDICAL_LINKED:
                row[k] *= idx
        if y < snap_bar:
            row["noncash"] = 0.0
        if spec.ptc != "off":
            # swap the per-capita share inside R for the credit keyed by coverage and age
            keyed = 0.0 if mc_eligible else ptc.takeup(a, spec.ptc, means_barred) * ptc.per_covered(a)
            row["ptc"] = ptc.per_capita - keyed
        if spec.premiums and mc_eligible:
            sr_late, sr_all = acs.late(a, t, "ss_receipt"), acs.everyone(a, "ss_receipt")
            ss_rate = {"late": sr_late, "resident": sr_all, "mid": 0.5 * (sr_late + sr_all)}[spec.ss]
            buyin = max(0.0, 1.0 - ss_rate / mc_rate) if mc_rate > 0 else 0.0
            on_mcaid = 0.0 if means_barred else acs.late(a, t, "medicaid")
            row["premiums"] = mc_rate * (1.0 - on_mcaid) * (PART_B_PREMIUM + buyin * PART_A_PREMIUM)
        out.loc[a] = row[cols].to_numpy(float)
    return out


def unauth_items(mb, acs, a0: int, spec: Spec, case: str, bar_price: dict, ptc: Ptc, pi: float,
                 onbooks: float, enforcement: float) -> pd.DataFrame:
    """The same person staying in unauthorized status: no federal programs, Social Security or
    premium tax credit (42 U.S.C. 402(y); 8 U.S.C. 1611; 26 U.S.C. 36B(e)), public care at the
    floor, taxes on the on-books share of a lower wage; presence items as in the LPR profile."""
    cols = list(mb.columns) + ["ptc", "premiums"]
    out = pd.DataFrame(0.0, index=range(101), columns=cols)
    pre65_scale = mb.loc[5, "medical"] / mb.loc[6, "medical"]
    floor = bar_price[case]
    for a in range(a0, 101):
        row = mb.loc[pa.band_of(a)].copy()
        row["ptc"] = row["premiums"] = 0.0
        row["S"] = 0.0
        row["E"] = -enforcement
        e = acs.earnings_ratio(a) if spec.earn == "late" else 1.0
        row["tax"] *= e * (1.0 - pi) * onbooks
        row["employer"] *= e * (1.0 - pi) * onbooks
        row["C"] *= e * (1.0 - WAGE_SHARE_OF_C * pi)
        for k in ("cash", "U", "noncash", "I"):
            row[k] = 0.0
        row["medical"] = -floor * (1.0 if a >= 65 else pre65_scale)
        row["M"], row["N"] = 0.0, 0.0
        if spec.ptc != "off":
            row["ptc"] = ptc.per_capita  # the per-capita share inside R comes out; nothing is keyed
        out.loc[a] = row[cols].to_numpy(float)
    return out


def npv_items(items: pd.DataFrame, table, a0: int, r: float, lt) -> dict:
    return {c: lt.survival_npv(items[c].to_numpy(float), table, a0, r)[0] for c in items.columns}


def npv_with_departure(stream: np.ndarray, table, a0: int, r: float, lt, q: float, h: float) -> float:
    """NPV of the counterfactual stream when a share q leaves at once and the rest leave at annual
    rate h (years after a0), on top of mortality."""
    y = np.maximum(np.arange(101) - a0, 0)
    return (1.0 - q) * lt.survival_npv(stream * (1.0 - h) ** y, table, a0, r)[0]


def main() -> None:
    OUT.mkdir(exist_ok=True)
    lt = pa.load_lifetime_module()
    profiles, fingerprints = lt.load_age_profiles(ROOT)  # stops with [BLOCKED] if stale
    comp = pd.read_csv(pa.LEDGER / "derived/age_profile_components.csv")
    hisp = lt.read_life_table(ROOT, "hispanic")
    mb = pa.component_table(comp, "mexico_born")
    audit = json.loads(pa.LINEAGE_AUDIT.read_text())["senior_pricing"]
    bar_price = {c: audit[f"{pa.BAR_REGIME[c]}|{c}"]["public_per_year"] for c in pa.CASES}
    acs = pa.AcsRates()
    ptc = Ptc()
    tail = pd.read_csv(TAIL / "derived/per_admission.csv")

    # gate 1: the new-arrival spec reproduces the tail lane's statutory arm, age by age and in NPV
    for a0 in AGES:
        for case in pa.CASES:
            mine = lpr_items(mb, acs, a0, NEW_ARRIVAL, case, bar_price, ptc).sum(axis=1).to_numpy()
            theirs = pa.late_profile(mb, acs, a0, "statutory", case, bar_price)
            assert np.allclose(mine, theirs, atol=1e-6), (a0, case, np.abs(mine - theirs).max())
            for r in (0.0, 0.03):
                v = lt.survival_npv(mine, hisp, a0, r)[0]
                ref = tail[(tail.arrival_age == a0) & (tail.arm == "statutory") & (tail.case == case)
                           & (tail.survival == "group_specific") & (tail.real_rate == r)].npv_parent
                assert len(ref) == 1 and abs(v - float(ref.iloc[0])) < 0.06, (a0, case, r, v, ref)

    # value every profile: new arrival and each adjuster type, factual and counterfactual
    # the floor alone, at each case's price level: 2026 state rules for new enrollees, the federal
    # floor (emergency Medicaid and uncompensated care) and state coverage everywhere
    floor_regimes = {"floor_2026": "rules_2026_new_enrollee", "floor_federal": "federal_floor",
                     "floor_full": "full_coverage_everywhere"}
    bar_alt = {v: {c: audit[f"{reg}|{c}"]["public_per_year"] for c in pa.CASES}
               for v, reg in floor_regimes.items()}
    variants = {
        "central": {},
        "floor_2026": {},
        "floor_federal": {},
        "floor_full": {},
        "ptc_off": {"ptc": "off"},
        "ptc_low": {"ptc": "low"},
        "ptc_high": {"ptc": "high"},
        "earn_resident": {"earn": "resident"},
        "ss_late": {"ss": "late"},
        "ss_resident": {"ss": "resident"},
        "index_since_arrival": {"index": "since_arrival"},
        "q40": {"q40": True},
        "premiums": {"premiums": True},
    }
    cf_variants = {"central": (PI["central"], ONBOOKS["central"], 0.0),
                   "tax_gain_low": (PI["low"], ONBOOKS["high"], 0.0),
                   "tax_gain_high": (PI["high"], ONBOOKS["low"], 0.0),
                   "enforcement": (PI["central"], ONBOOKS["central"], E_PER_UNAUTH)}
    rows, items_rows = [], []
    profiles_to_run = {"new_arrival": NEW_ARRIVAL, **TYPES}
    for name, base in profiles_to_run.items():
        for vname, vchg in variants.items():
            chg = dict(vchg)
            if vname in RESIDENCE_VARIANTS and name not in LONG_TYPES:
                continue  # these describe years of prior residence; recent entrants have none
            spec = replace(base, **({"ptc": "central"} | chg))
            prices = bar_alt.get(vname, bar_price)
            for a0 in AGES:
                for case in pa.CASES:
                    fact = lpr_items(mb, acs, a0, spec, case, prices, ptc)
                    cfs = {k: unauth_items(mb, acs, a0, spec, case, prices, ptc, *v)
                           for k, v in cf_variants.items()} if vname == "central" else \
                        {"central": unauth_items(mb, acs, a0, spec, case, prices, ptc, *cf_variants["central"])}
                    for r in RATES:
                        fi = npv_items(fact, hisp, a0, r, lt)
                        fsum = sum(fi.values())
                        for cfname, cf in cfs.items():
                            ci = npv_items(cf, hisp, a0, r, lt)
                            csum = sum(ci.values())
                            row = {"profile": name, "variant": vname, "counterfactual": cfname,
                                   "adjust_age": a0, "case": case, "real_rate": r,
                                   "npv_factual_armB": round(fsum, 1),
                                   "npv_counterfactual_stay": round(csum, 1),
                                   "npv_armA": round(fsum - csum, 1)}
                            if name in TYPES:
                                stream = cf.sum(axis=1).to_numpy(float)
                                for lvl, dep in DEPART.items():
                                    row[f"npv_cf_depart_{lvl}"] = round(
                                        npv_with_departure(stream, hisp, a0, r, lt, *dep[name]), 1)
                            rows.append(row)
                            if vname == "central" and cfname == "central" and case == "central" \
                                    and r in (0.0, 0.03):
                                for item in fi:
                                    items_rows.append({"profile": name, "adjust_age": a0, "real_rate": r,
                                                       "item": item, "factual": round(fi[item], 1),
                                                       "counterfactual_stay": round(ci[item], 1),
                                                       "armA_difference": round(fi[item] - ci[item], 1)})
    df = pd.DataFrame(rows)
    df.to_csv(OUT / "adjuster_values.csv", index=False, lineterminator="\n")
    pd.DataFrame(items_rows).to_csv(OUT / "adjuster_items.csv", index=False, lineterminator="\n")
    prov = {"ledger_fingerprints": fingerprints,
            "tail_per_admission_py": sha256(TAIL / "per_admission.py"),
            "tail_per_admission_csv": sha256(TAIL / "derived/per_admission.csv"),
            "tail_acs_tenure_csv": sha256(TAIL / "derived/late_arrival_tenure.csv"),
            "lineage_audit": sha256(pa.LINEAGE_AUDIT),
            "ptc_inputs": sha256(OUT / "ptc_inputs.csv"),
            "bar_price_per_year": bar_price, "bar_price_variants": bar_alt,
            "medicare_weight": pa.MEDICARE_WEIGHT,
            "types": {k: asdict(v) for k, v in TYPES.items()}, "depart": DEPART,
            "pi": PI, "onbooks": ONBOOKS, "enforcement_per_unauthorized": round(E_PER_UNAUTH, 2),
            "part_a_premium": PART_A_PREMIUM, "part_b_premium": PART_B_PREMIUM,
            "gates": ["new-arrival spec reproduces tail statutory profiles (atol 1e-6) and NPVs (< $0.06)"]}
    (OUT / "adjuster_provenance.json").write_text(json.dumps(prov, indent=1, sort_keys=True) + "\n")
    show = df[(df.variant == "central") & (df.counterfactual == "central") & (df.case == "central")
              & df.real_rate.isin([0.0, 0.03]) & df.adjust_age.isin([55, 60, 65])]
    print(show.to_string())


if __name__ == "__main__":
    main()
