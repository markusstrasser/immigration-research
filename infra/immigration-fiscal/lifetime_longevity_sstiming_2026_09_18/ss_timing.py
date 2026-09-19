"""Phase B: what the snapshot owes when this year's OASDI taxes are claimed later.

The repo's period account credits a worker with the OASDI payroll tax paid in 2024 and
charges a retiree with the OASDI benefit received in 2024.  It books no liability for the
benefit the 2024 worker will claim after 2034.  This script prices that liability with the
SSA Office of the Chief Actuary's money's worth ratios (Actuarial Note 2025.7, Table 1,
Current Law Scheduled scenario), which are exactly PV(expected benefits)/PV(expected taxes)
for a hypothetical worker of a given birth cohort, sex, family type and career-earnings level:

    accrued liability_i = MWR_i * OASDI tax paid in 2024_i

Two adjustments are reported, because the first on its own double-counts:

  accrual_only   subtract the accrued liability from every worker.  This is the objection as
                 usually stated and it is an upper bound: the 2024 retiree's benefit is still
                 charged to 2024 even though it was accrued decades ago.
  cash_to_accrual  subtract the accrued liability from workers AND credit back the OASDI
                 benefits the account charges to today's retirees.  This is the complete
                 switch from a cash basis to an accrual basis.

Earnings level per person is that person's own 2024 wage and salary over the 2024 national
average wage index, matched against the note's five hypothetical career-average levels; the
group-level arm instead assigns one earnings level to the whole group from its mean wage over
ages 21-64 including non-earners, which is the concept the SSA scaled worker embeds.

Outputs derived/mwr_table.csv, derived/ss_timing_group.csv, derived/ss_timing_arms.csv,
derived/ss_timing_audit.json.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
FISCAL = HERE.parent
CACHE = HERE / "_cache"
OUT = HERE / "derived"
OUT.mkdir(exist_ok=True)

sys.path.insert(0, str(FISCAL / "gen_ledger_extension_2026_09_16"))
sys.path.insert(0, str(FISCAL / "build"))
import analyze_cps_fiscal_2025 as base  # noqa: E402

EXTRA = ["A_SEX", "A_MARITL", "A_SPOUSE", "A_LINENO", "SEMP_VAL", "FRSE_VAL"]
for _f in EXTRA:
    if _f not in base.PERSON:
        base.PERSON.append(_f)

import extend_ledger as ext  # noqa: E402

ROOT = FISCAL.parents[1]
CPS = ROOT / "sources/immigration-fiscal/data/external/stage3/census/cps_asec_2025/asecpub25csv.zip"
GROUPS = ["mexico_born", "mexican_second_gen", "mexican_third_plus_selfid",
          "third_plus_nh_white", "all_native"]
MEXICAN = GROUPS[:3]
BAND_EDGES = [18, 25, 35, 45, 55, 65, 75]
BAND_LABEL = ["0-17", "18-24", "25-34", "35-44", "45-54", "55-64", "65-74", "75+"]

# [SOURCE: ssa.gov/oact/cola/awidevelop.html, fetched 2026-09-18, cached _cache/ssa_awi.html]
AWI_2023 = 66_621.80
AWI_2024 = 69_846.57
SECA_FACTOR = 0.9235             # net earnings from self-employment are 92.35% of profit
INCOME_YEAR = 2024               # CPS ASEC 2025 asks about calendar 2024
# [SOURCE: ledger_absolute_2026_09_17/RESULT_extension.md] union complete common-age gap
# against third-plus non-Hispanic whites, dollars per standardized person.
COMPLETE_GAP_UNION = -7224.0
PROFILE_POP = (FISCAL / "pronatal_equivalence_2026_09_18/derived/age_profiles_references.csv")
# [SOURCE: 2025 OASDI Trustees Report, short-range estimates, combined OASDI table,
# cached _cache/ssa_tr2025_IVA.html] net payroll tax contributions, calendar 2024, $bn.
OASDI_PAYROLL_TAX_2024_BN = 1293.3

# [SOURCE: Actuarial Note 2025.7 Table A] career-average earnings of the hypothetical
# workers retiring at 62 in 2024, wage-indexed to 2023.
TABLE_A_DOLLARS = {"Very Low": 16_556.0, "Low": 29_800.0, "Medium": 66_223.0,
                   "High": 105_957.0, "Maximum": 163_970.0}
LEVEL_ORDER = ["Very Low", "Low", "Medium", "High", "Maximum"]
FAMILY = {"single_man": "single_man", "single_woman": "single_woman",
          "one_earner_couple": "one_earner_couple", "two_earner_couple": "two_earner_couple"}


# ------------------------------------------------------------------ MWR table
def parse_mwr() -> pd.DataFrame:
    """Table 1 of Actuarial Note 2025.7 from the cached PDF's text layer."""
    text = (CACHE / "ssa_an2025-7.txt").read_text().splitlines()
    start = next(i for i, l in enumerate(text) if "Table 1. Money" in l)
    end = next(i for i, l in enumerate(text[start:], start)
               if "Note: Based on the intermediate" in l)
    # the earnings-level label is printed once per block, vertically centred on its 11 rows,
    # so it can appear on any row of the block; collect rows first, then label whole blocks.
    num = re.compile(r"^\s*(?:(Very Low|Low|Medium|High|Maximum)\s+)?(\d{4})\s+(\d{4})\s+"
                     r"([\d.]+)\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)\s*$")
    rows, labels = [], []
    for line in text[start:end]:
        m = num.match(line)
        if not m:
            continue
        labels.append(m.group(1))
        rows.append(dict(birth_year=int(m.group(2)), attains_65=int(m.group(3)),
                         single_man=float(m.group(4)), single_woman=float(m.group(5)),
                         one_earner_couple=float(m.group(6)), two_earner_couple=float(m.group(7))))
    if len(rows) % 11:
        raise ValueError(f"MWR parse: {len(rows)} rows is not a whole number of 11-cohort blocks")
    for i in range(0, len(rows), 11):
        block = [l for l in labels[i:i + 11] if l]
        if len(set(block)) != 1:
            raise ValueError(f"MWR parse: block at row {i} carries labels {block}")
        for r in rows[i:i + 11]:
            r["earnings_level"] = block[0]
    t = pd.DataFrame(rows)
    if t.earnings_level.drop_duplicates().tolist() != LEVEL_ORDER:
        raise ValueError(f"MWR parse: block order {t.earnings_level.drop_duplicates().tolist()}")
    counts = t.groupby("earnings_level").size()
    if len(t) != 55 or set(counts.index) != set(LEVEL_ORDER) or (counts != 11).any():
        raise ValueError(f"MWR parse: expected 5 levels x 11 cohorts = 55 rows, got {len(t)}\n{counts}")
    # the note's own text: ratios fall as earnings rise, within every cohort and family type
    for fam in FAMILY:
        w = t.pivot(index="birth_year", columns="earnings_level", values=fam)[LEVEL_ORDER]
        if (w.diff(axis=1).dropna(axis=1).to_numpy() > 1e-9).any():
            raise ValueError(f"MWR not monotone decreasing in earnings level for {fam}")
    return t


def mwr_interpolate(t: pd.DataFrame, fam: str, birth: np.ndarray,
                    ratio: np.ndarray) -> np.ndarray:
    """Bilinear in (birth year, log earnings relative to AWI); flat outside the knots."""
    knots = np.array([TABLE_A_DOLLARS[l] / AWI_2023 for l in LEVEL_ORDER])
    cohorts = np.sort(t.birth_year.unique())
    grid = t.pivot(index="birth_year", columns="earnings_level", values=fam)[LEVEL_ORDER].to_numpy()
    b = np.clip(birth, cohorts[0], cohorts[-1])
    j = np.clip(np.searchsorted(cohorts, b, side="right") - 1, 0, len(cohorts) - 2)
    wb = (b - cohorts[j]) / (cohorts[j + 1] - cohorts[j])
    by_level = grid[j] * (1 - wb)[:, None] + grid[j + 1] * wb[:, None]
    lr = np.log(np.clip(ratio, knots[0], knots[-1]))
    lk = np.log(knots)
    k = np.clip(np.searchsorted(lk, lr, side="right") - 1, 0, len(lk) - 2)
    wk = (lr - lk[k]) / (lk[k + 1] - lk[k])
    rows = np.arange(len(b))
    return by_level[rows, k] * (1 - wk) + by_level[rows, k + 1] * wk


# ------------------------------------------------------------------ CPS stage
def stage() -> pd.DataFrame:
    state = ext.build(argparse.Namespace(cps_zip=CPS))
    d, weights = state["d"], state["person_weights"]
    civilian = (d.PRPERTYP.eq(2) | d.A_AGE.lt(15)).to_numpy()
    wage = d.WSAL_VAL.clip(lower=0).to_numpy(dtype=float)
    se = (d.SEMP_VAL.clip(lower=0) + d.FRSE_VAL.clip(lower=0)).to_numpy(dtype=float)
    capped_wage = np.minimum(wage, ext.OASDI_CAP_2024)
    seca_base = np.minimum(SECA_FACTOR * se, np.maximum(ext.OASDI_CAP_2024 - capped_wage, 0.0))
    out = pd.DataFrame({
        "w": weights[:, 0], "age": d.A_AGE.to_numpy(), "sex": d.A_SEX.to_numpy(),
        "marital": d.A_MARITL.to_numpy(), "civilian": civilian, "wage": wage,
        "oasdi_wage": 2 * ext.OASDI_RATE * capped_wage,
        "oasdi_se": 2 * ext.OASDI_RATE * seca_base,
        "ss_benefit": d.SS_VAL.clip(lower=0).to_numpy(dtype=float),
        "band": np.digitize(d.A_AGE, BAND_EDGES),
    })
    # spouse's own wage, for the one- vs two-earner split
    key = d.PH_SEQ.astype("int64") * 1000 + d.A_LINENO.astype("int64")
    spouse_key = d.PH_SEQ.astype("int64") * 1000 + d.A_SPOUSE.astype("int64")
    wage_by_key = pd.Series(wage, index=key.to_numpy())
    wage_by_key = wage_by_key[~wage_by_key.index.duplicated()]
    out["spouse_wage"] = spouse_key.map(wage_by_key).fillna(-1.0).to_numpy()
    out["married"] = d.A_SPOUSE.gt(0).to_numpy() & d.A_MARITL.isin([1, 2, 3]).to_numpy()
    for g in GROUPS:
        out[g] = state["group"][g] & civilian
    return out


# ------------------------------------------------------------------ analysis
def family_vector(p: pd.DataFrame, arm: str) -> np.ndarray:
    if arm in FAMILY:
        return np.full(len(p), arm, dtype=object)
    if arm != "observed_family":
        raise ValueError(arm)
    single = np.where(p.sex.to_numpy() == 1, "single_man", "single_woman")
    couple = np.where(p.spouse_wage.to_numpy() > 0, "two_earner_couple", "one_earner_couple")
    return np.where(p.married.to_numpy(), couple, single).astype(object)


def accruals(p: pd.DataFrame, mwr: pd.DataFrame, family_arm: str, earnings_arm: str,
             include_se: bool, coverage_scale: float = 1.0) -> np.ndarray:
    tax = (p.oasdi_wage.to_numpy() + (p.oasdi_se.to_numpy() if include_se else 0.0)) * coverage_scale
    birth = (INCOME_YEAR - p.age.to_numpy()).astype(float)
    fam = family_vector(p, family_arm)
    if earnings_arm == "individual":
        ratio = np.where(tax > 0, p.wage.to_numpy() / AWI_2024, 1.0)
    else:
        ratio = np.full(len(p), np.nan)
        pool = p.age.between(21, 64).to_numpy() & p.civilian.to_numpy()
        for g in GROUPS:
            m = p[g].to_numpy() & pool
            grp_ratio = np.average(p.wage.to_numpy()[m], weights=p.w.to_numpy()[m]) / AWI_2024
            ratio[p[g].to_numpy()] = grp_ratio
        ratio = np.where(np.isnan(ratio), 1.0, ratio)
    out = np.zeros(len(p))
    for f in FAMILY:
        m = (fam == f) & (tax > 0)
        if m.any():
            out[m] = mwr_interpolate(mwr, f, birth[m], ratio[m]) * tax[m]
    return out


def per_person(p: pd.DataFrame, value: np.ndarray, group: str) -> np.ndarray:
    """Weighted mean of `value` per resident person, by age band."""
    m = p[group].to_numpy()
    w, b = p.w.to_numpy()[m], p.band.to_numpy()[m]
    num = np.bincount(b, weights=w * value[m], minlength=8)
    den = np.bincount(b, weights=w, minlength=8)
    return np.divide(num, den, out=np.zeros(8), where=den > 0)


def standardized(p: pd.DataFrame, value: np.ndarray, group: str, ref: str) -> float:
    """Per-person value at the reference group's age-band mix (the ledger's common-age rule)."""
    m = p[ref].to_numpy()
    shares = np.bincount(p.band.to_numpy()[m], weights=p.w.to_numpy()[m], minlength=8)
    shares = shares / shares.sum()
    return float((per_person(p, value, group) * shares).sum())


def main() -> None:
    raise SystemExit(
        "[BLOCKED] This archived MWR diagnostic is disabled: whole-career ratios do not "
        "identify current-year accrued liability; group-mean masks overwrite overlapping "
        "groups and complete_gap_after uses a stale union baseline. Use "
        "ledger_absolute_2026_09_17/lifetime.py for current cash period-profile NPVs."
    )


def archived_diagnostic_not_for_current_estimates() -> None:
    mwr = parse_mwr()
    mwr.to_csv(OUT / "mwr_table.csv", index=False)
    print(f"[mwr] parsed {len(mwr)} rows of Actuarial Note 2025.7 Table 1")
    print(mwr[mwr.birth_year.isin([1964, 1985])].to_string(index=False))

    cache = OUT / "cps_ss_stage.parquet"
    if cache.exists():
        p = pd.read_parquet(cache)
        print(f"[stage] reusing {cache.name}, {len(p):,} person records")
    else:
        p = stage()
        p.to_parquet(cache, index=False)
        print(f"[stage] built {cache.name}, {len(p):,} person records")

    audit = {"awi_2023": AWI_2023, "awi_2024": AWI_2024,
             "oasdi_rate_each_side": ext.OASDI_RATE, "oasdi_cap_2024": ext.OASDI_CAP_2024,
             "complete_gap_union_before": COMPLETE_GAP_UNION}

    # ---- gate: the group masks, weights and bands must reproduce the profile lane's
    # population column exactly, since the common-age standardization rests on them.
    stored = pd.read_csv(PROFILE_POP)
    worst, checked = 0.0, 0
    for g in GROUPS:
        m = p[g].to_numpy()
        mine = np.bincount(p.band.to_numpy()[m], weights=p.w.to_numpy()[m], minlength=8)
        for b in range(8):
            row = stored[(stored.group == g) & (stored.band == b)]
            if len(row) != 1:
                raise ValueError(f"no stored population for {g}/{b}")
            worst = max(worst, abs(mine[b] - float(row.population.iloc[0])))
            checked += 1
    print(f"[gate] {checked} group x band populations reproduce age_profiles_references.csv: "
          f"max |diff| = {worst:.6f} people -> {'PASS' if worst < 1e-3 else 'FAIL'}")
    if worst >= 1e-3:
        raise SystemExit(1)
    audit["gate_population_max_abs_diff_people"] = round(worst, 6)

    # ---- external check: the account's OASDI tax base against published receipts
    civ = p.civilian.to_numpy()
    total_oasdi_bn = float(((p.oasdi_wage + p.oasdi_se).to_numpy()[civ] * p.w.to_numpy()[civ]).sum() / 1e9)
    audit["cps_total_oasdi_tax_bn"] = round(total_oasdi_bn, 2)
    print(f"[check] CPS civilian-household OASDI payroll tax, both halves: ${total_oasdi_bn:,.1f}bn")

    # ---- descriptives the mapping rests on
    pool = p.age.between(21, 64).to_numpy() & p.civilian.to_numpy()
    desc = []
    for g in GROUPS:
        m = p[g].to_numpy() & pool
        w = p.w.to_numpy()[m]
        wage = p.wage.to_numpy()[m]
        earners = wage > 0
        desc.append(dict(
            group=g, pop_21_64=float(w.sum()),
            mean_wage_incl_zero=float(np.average(wage, weights=w)),
            mean_wage_earners=float(np.average(wage[earners], weights=w[earners])),
            share_with_wage=float(w[earners].sum() / w.sum()),
            ratio_to_awi_incl_zero=float(np.average(wage, weights=w) / AWI_2024),
            ratio_to_awi_earners=float(np.average(wage[earners], weights=w[earners]) / AWI_2024),
            share_married=float(w[p.married.to_numpy()[m]].sum() / w.sum()),
            share_one_earner_couple=float(
                w[(p.married.to_numpy() & p.spouse_wage.le(0))[m]].sum() / w.sum()),
            mean_oasdi_tax_all_ages=float(
                np.average((p.oasdi_wage + p.oasdi_se).to_numpy()[p[g].to_numpy()],
                           weights=p.w.to_numpy()[p[g].to_numpy()]))))
    dd = pd.DataFrame(desc)
    print("\n[earnings and family inputs, ages 21-64]")
    print(dd.round(4).to_string(index=False))
    audit["descriptives"] = dd.set_index("group").round(4).to_dict("index")

    # ---- arms
    scale = OASDI_PAYROLL_TAX_2024_BN / total_oasdi_bn
    audit["coverage_scale_to_trustees_2024"] = round(scale, 6)
    print(f"[check] published 2024 net payroll tax contributions ${OASDI_PAYROLL_TAX_2024_BN}bn; "
          f"CPS/published = {1/scale:.4f}, coverage scale = {scale:.4f}")

    rows = []
    arms = [("observed_family", "individual", True, 1.0),
            ("observed_family", "individual", False, 1.0),
            ("observed_family", "group_mean", True, 1.0),
            ("observed_family", "individual", True, scale),
            ("single_man", "individual", True, 1.0),
            ("single_woman", "individual", True, 1.0),
            ("one_earner_couple", "individual", True, 1.0),
            ("two_earner_couple", "individual", True, 1.0)]
    for fam_arm, earn_arm, se, cov in arms:
        acc = accruals(p, mwr, fam_arm, earn_arm, se, cov)
        tax = (p.oasdi_wage.to_numpy() + (p.oasdi_se.to_numpy() if se else 0.0)) * cov
        ben = p.ss_benefit.to_numpy()
        for adj_name, adj in [("accrual_only", -acc), ("cash_to_accrual", -acc + ben)]:
            for g in GROUPS:
                m = p[g].to_numpy()
                w = p.w.to_numpy()[m]
                rows.append(dict(
                    family_arm=fam_arm, earnings_arm=earn_arm, self_employment=se,
                    coverage_scale=cov, adjustment=adj_name, group=g, population=float(w.sum()),
                    per_person_year=float(np.average(adj[m], weights=w)),
                    total_bn=float((adj[m] * w).sum() / 1e9),
                    oasdi_tax_per_person=float(np.average(tax[m], weights=w)),
                    ss_benefit_per_person=float(np.average(ben[m], weights=w)),
                    std_vs_white=standardized(p, adj, g, "third_plus_nh_white")))
    res = pd.DataFrame(rows)

    # ---- per age band, so Phase A can run the adjustment through the lifetime machinery
    band_rows = []
    for fam_arm, earn_arm, se, cov in arms:
        acc = accruals(p, mwr, fam_arm, earn_arm, se, cov)
        for adj_name, adj in [("accrual_only", -acc),
                              ("cash_to_accrual", -acc + p.ss_benefit.to_numpy())]:
            for g in GROUPS + ["mexican_observed_total"]:
                if g == "mexican_observed_total":
                    m = np.zeros(len(p), bool)
                    for gg in MEXICAN:
                        m |= p[gg].to_numpy()
                    p["_u"] = m
                    vals, name = per_person(p, adj, "_u"), g
                else:
                    vals, name = per_person(p, adj, g), g
                for b in range(8):
                    band_rows.append(dict(family_arm=fam_arm, earnings_arm=earn_arm,
                                          self_employment=se, coverage_scale=cov,
                                          adjustment=adj_name, group=name, band=b,
                                          adjustment_per_person=float(vals[b])))
    pd.DataFrame(band_rows).to_csv(OUT / "ss_timing_by_band.csv", index=False)
    if "_u" in p.columns:
        p.drop(columns=["_u"], inplace=True)

    # union = the three Mexican-origin groups pooled
    union = []
    KEYS = ["family_arm", "earnings_arm", "self_employment", "coverage_scale", "adjustment"]
    for keys, g in res.groupby(KEYS):
        mex = g[g.group.isin(MEXICAN)]
        pop = mex.population.sum()
        union.append(dict(zip(KEYS, keys),
                          group="mexican_observed_total", population=pop,
                          per_person_year=float((mex.per_person_year * mex.population).sum() / pop),
                          total_bn=float(mex.total_bn.sum()),
                          oasdi_tax_per_person=float((mex.oasdi_tax_per_person * mex.population).sum() / pop),
                          ss_benefit_per_person=float((mex.ss_benefit_per_person * mex.population).sum() / pop),
                          std_vs_white=np.nan))
    res = pd.concat([res, pd.DataFrame(union)], ignore_index=True)

    # the union's standardized value needs the pooled per-band means, not a population average
    for keys, g in res.groupby(KEYS):
        fam_arm, earn_arm, se, cov, adj_name = keys
        acc = accruals(p, mwr, fam_arm, earn_arm, se, cov)
        adj = -acc + (p.ss_benefit.to_numpy() if adj_name == "cash_to_accrual" else 0.0)
        mex_mask = np.zeros(len(p), bool)
        for gg in MEXICAN:
            mex_mask |= p[gg].to_numpy()
        p["_union"] = mex_mask
        v = standardized(p, adj, "_union", "third_plus_nh_white")
        sel = ((res.family_arm == fam_arm) & (res.earnings_arm == earn_arm)
               & (res.self_employment == se) & (res.coverage_scale == cov)
               & (res.adjustment == adj_name) & (res.group == "mexican_observed_total"))
        res.loc[sel, "std_vs_white"] = v
    res.drop(columns=[c for c in ["_union"] if c in res.columns], inplace=True)

    # The repo states the gap as (group minus white), so a negative gap means the group is
    # worse off; the adjustment moves that gap by (group adjustment minus white adjustment).
    white = res[res.group.eq("third_plus_nh_white")].set_index(KEYS).std_vs_white
    res["gap_change"] = res.apply(
        lambda r: r.std_vs_white - white[tuple(r[k] for k in KEYS)], axis=1)
    res["complete_gap_after"] = COMPLETE_GAP_UNION + res.gap_change
    res.to_csv(OUT / "ss_timing_arms.csv", index=False)

    central = res[res.family_arm.eq("observed_family") & res.earnings_arm.eq("individual")
                  & res.self_employment & res.coverage_scale.eq(1.0)]
    central.to_csv(OUT / "ss_timing_group.csv", index=False)
    pd.set_option("display.width", 240)
    print("\n[central arm: observed family type, individual earnings level, self-employment in]")
    print(central[["adjustment", "group", "oasdi_tax_per_person", "ss_benefit_per_person",
                   "per_person_year", "total_bn", "std_vs_white", "gap_change", "complete_gap_after"]]
          .round(1).to_string(index=False))

    print("\n[all arms, union: change in the common-age gap against whites, $ per standardized person]")
    show = res[res.group.eq("mexican_observed_total")].copy()
    show["coverage_scale"] = show.coverage_scale.round(4)
    print(show
          [["family_arm", "earnings_arm", "self_employment", "coverage_scale", "adjustment",
            "per_person_year", "total_bn", "gap_change", "complete_gap_after"]]
          .round({"per_person_year": 1, "total_bn": 1, "gap_change": 1, "complete_gap_after": 1})
          .to_string(index=False))

    json.dump(audit, open(OUT / "ss_timing_audit.json", "w"), indent=2, sort_keys=True, default=float)
    print(f"\n[written] {OUT}/mwr_table.csv, ss_timing_group.csv, ss_timing_arms.csv, "
          f"ss_timing_by_band.csv, ss_timing_audit.json")


if __name__ == "__main__":
    main()
