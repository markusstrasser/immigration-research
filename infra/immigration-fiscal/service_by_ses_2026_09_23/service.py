"""Military and protective service by Indian and Mexican origin, ACS 2022-2024 pooled, raw and at
equal SES, with 80-replicate standard errors.

Extends `civic_service_by_ancestry_2026_09_21` (ACS 2024, US-born men, first ancestry, binomial
SEs): three pooled years, women, the foreign-born, `MIL` split three ways, and SES adjustments.
Inputs are the Parquet files from `extract_acs.py`, the PUMA metro-size classes from `metro.py`
and the neighbourhood-income expectations from `neighborhood.py`.

Outcomes (persons 17+ are asked `MIL`): ever on active duty (`MIL` 1-2), now on active duty
(`MIL` 1), reserve or Guard training only (`MIL` 3). The universe includes group quarters, so
soldiers in barracks count; residents abroad, including troops stationed overseas, are outside
the ACS. Protective-service occupations are counted among employed civilians (`ESR` 1-2).

Standard errors: pooled weights PWGTP and replicate r = the sum over the three years of
PWGTPr; SE = sqrt(4/80 * sum_r (theta_r - theta)^2). Every adjustment is recomputed on each
replicate.

Every specification is a ratio of the group's rate to a comparison rate for US-born
non-Hispanic whites (`comparison_rate`):
  raw                   white rate at the same sex and age band;
  age_direct / _indirect  the same ages only: group rates by age cell weighted to the white age
                        mix (direct), or the group's rate against white age-cell rates at the
                        group's ages (indirect); groups younger than whites within a band have
                        lower raw rates because "ever served" accumulates with age;
  a_education_direct    group rates by own education (less than HS / HS / some college / BA+)
                        weighted to the white education mix, against the white rate;
  a_education_indirect  group's own rate against white education-stratum rates weighted to the
                        group's education mix;
  a_age_education_direct / _indirect  the same with age cell x education cells;
  b_raked_geo / _full   group reweighted (raked) to the white distribution on age, state and
                        division x metro size ("geo") or age x education, state, metro size x
                        education and division x metro size ("full"), against the white rate;
  b_indirect_geo/_full  group's own rate against white rates in the group's own age x state x
                        metro-size (x education) cells; a white cell with fewer than 50 records
                        borrows the rate of its division, then of its metro class;
  c_neighborhood_*      group's own rate against the white rate times the neighbourhood-income
                        expected ratio from `neighborhood.py`;
  c_age_neighborhood_*  the same with the age-indirect comparison rate in place of the white rate.
Raking extrapolates from the few group members who resemble the typical white; indirect
standardisation asks how often whites who resemble the group serve. Own education and adult
place of residence partly follow service (GI Bill, base towns), so (a) and (b) are not clean
controls; (c) uses pre-service neighbourhood income on the DoD side but the group's current
residence.
"""
import sys
from pathlib import Path

import duckdb
import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
CACHE, DERIVED = HERE / "_cache", HERE / "derived"
YEARS = (2022, 2023, 2024)
R = 81  # full weight + 80 replicates
MEXICAN_ANCESTRY = "(210, 211, 212, 213, 215, 218, 219)"
GROUPS = {
    # name: (SQL predicate, neighbourhood group for adjustment (c))
    "usb_mexican_hisp": ("NATIVITY = 1 AND HISP = 2", "us_born_mexican_origin"),
    "usb_mexican_ancestry": (f"NATIVITY = 1 AND ANC1P IN {MEXICAN_ANCESTRY}", "us_born_mexican_origin"),
    "mexico_born": ("POBP = 303", "mexico_born"),
    "mexico_born_naturalized": ("POBP = 303 AND CIT = 4", "mexico_born"),
    "mexico_born_arrived_under_18": ("POBP = 303 AND YOEP IS NOT NULL AND AGEP - (year - YOEP) < 18", "mexico_born"),
    "usb_asian_indian_ancestry": ("NATIVITY = 1 AND ANC1P = 615", "us_born_asian_indian"),
    "usb_asian_indian_race": ("NATIVITY = 1 AND ((year = 2022 AND RAC2P = 38) OR (year >= 2023 AND RAC2P = 4015))",
                              "us_born_asian_indian"),
    "india_born": ("POBP = 210", "india_born"),
    "india_born_naturalized": ("POBP = 210 AND CIT = 4", "india_born"),
    "india_born_arrived_under_18": ("POBP = 210 AND YOEP IS NOT NULL AND AGEP - (year - YOEP) < 18", "india_born"),
    "usb_nh_white": ("NATIVITY = 1 AND HISP = 1 AND RAC1P = 1", "us_born_nh_white"),
    "usb_all": ("NATIVITY = 1", "us_born_all"),
}
REFERENCE = "usb_nh_white"
AGE_CELL = """CASE WHEN AGEP < 18 THEN 0 WHEN AGEP <= 21 THEN 1 WHEN AGEP <= 24 THEN 2 WHEN AGEP <= 29 THEN 3
  WHEN AGEP <= 34 THEN 4 WHEN AGEP <= 39 THEN 5 WHEN AGEP <= 44 THEN 6 WHEN AGEP <= 49 THEN 7
  WHEN AGEP <= 54 THEN 8 WHEN AGEP <= 59 THEN 9 WHEN AGEP <= 64 THEN 10 WHEN AGEP <= 68 THEN 11 ELSE 12 END"""
EDUC = "CASE WHEN SCHL <= 15 THEN 0 WHEN SCHL <= 17 THEN 1 WHEN SCHL <= 20 THEN 2 ELSE 3 END"
EDUC_NAMES = ("less_than_hs", "hs_diploma", "some_college", "ba_plus")
BANDS = {  # name: (age cells, post-draft only)
    "18_24": ((1, 2), False),
    "18_49": ((1, 2, 3, 4, 5, 6, 7), False),
    "25_49": ((3, 4, 5, 6, 7), False),
    "25_34": ((3, 4), False),
    "18_plus_born_1956_on": (tuple(range(1, 13)), True),
}
MILITARY = {"ever_active_duty": "MIL IN (1, 2)", "now_active_duty": "MIL = 1", "reserve_guard_only": "MIL = 3"}
EMPLOYED = "ESR IN (1, 2)"
PROTECTIVE = {
    "public_safety_total": "OCCP IN (3710, 3820, 3870, 3700, 3801, 3802, 3720, 3740, 3750, 3401, 3402)",
    "police_sheriff_detective": "OCCP IN (3710, 3820, 3870)",
    "corrections_bailiff": "OCCP IN (3700, 3801, 3802)",
    "fire": "OCCP IN (3720, 3740, 3750)",
    "ems": "OCCP IN (3401, 3402)",
    "security_guard": "OCCP = 3930",
    "all_protective_service_soc33": "OCCP BETWEEN 3700 AND 3960",
}
METRO_CODES = {"metro_5m_plus": 0, "metro_1m_5m": 1, "metro_under_1m": 2, "non_metro": 3}
CELL_KEYS = ["age_cell", "educ", "st", "division", "metro"]
INDIRECT_LEVELS = {
    "age": [("age_cell",)],
    "age_educ": [("age_cell", "educ"), ("age_cell",)],
    "full": [("age_cell", "educ", "st", "metro"), ("age_cell", "educ", "division", "metro"),
             ("age_cell", "educ", "metro"), ("age_cell", "educ")],
    "geo": [("age_cell", "st", "metro"), ("age_cell", "division", "metro"), ("age_cell", "metro"), ("age_cell",)],
}
# Raking margin sets tried in order; the first that rakes on the full weights is used and recorded.
MARGIN_SETS = {
    "age": [("age", 20), ("age", 60)],
    "age_educ": [("age x educ", 20), ("age x educ", 60)],
    "full": [("age x educ, state, metro x educ, division x metro", 20),
             ("age x educ, state, metro x educ, division x metro", 60),
             ("age x educ, state, metro", 60)],
    "geo": [("age, state, division x metro", 20), ("age, state, division x metro", 60), ("age, state, metro", 60)],
}


def replicate_sums(flag=None):
    weight = lambda r: "PWGTP" if r == 0 else f"PWGTP{r}"
    if flag is None:
        return [f"SUM({weight(r)})::DOUBLE" for r in range(R)]
    return [f"SUM(CASE WHEN {flag} THEN {weight(r)} ELSE 0 END)::DOUBLE" for r in range(R)]


class Cells:
    """Weighted cell sums for one group: keys plus arrays [cells, 81] per measure."""

    def __init__(self, frame, keys, measures):
        self.keys = frame[keys].to_numpy(np.int64)
        self.key_names = keys
        self.n = frame["n"].to_numpy(np.int64)
        self.w2 = frame["w2"].to_numpy(float)
        self.data = {m: frame[[f"{m}_{r}" for r in range(R)]].to_numpy(float) for m in measures}

    def col(self, name):
        return self.keys[:, self.key_names.index(name)]


def connect():
    con = duckdb.connect()
    con.execute("SET threads = 4")
    con.execute("SET memory_limit = '6GB'")
    parts = [f"SELECT {y} AS year, * FROM read_parquet('{CACHE / f'acs{y}_persons.parquet'}')" for y in YEARS]
    con.execute("CREATE VIEW persons AS " + " UNION ALL ".join(parts))
    metro = pd.read_csv(DERIVED / "puma_metro_size.csv")
    metro["metro"] = metro["metro_size"].map(METRO_CODES)
    con.register("metro_df", metro[["st", "puma", "metro"]].rename(columns={"st": "m_st", "puma": "m_puma"}))
    con.execute("CREATE TABLE metro AS SELECT * FROM metro_df")
    missing = con.execute("""SELECT COUNT(*) FROM persons p LEFT JOIN metro m ON m.m_st = p.ST AND m.m_puma = p.PUMA
                             WHERE m.metro IS NULL""").fetchone()[0]
    assert missing == 0, f"{missing} person records have no metro class"
    return con


def military_cells(con, predicate):
    measures = {"pop": None, **MILITARY}
    sums = []
    for name, flag in measures.items():
        sums += [f"{expr} AS {name}_{r}" for r, expr in enumerate(replicate_sums(flag))]
    query = f"""
        SELECT SEX AS sex, {AGE_CELL} AS age_cell, (year - AGEP >= 1956)::INT AS post_draft, {EDUC} AS educ,
               p.ST AS st, p.DIVISION AS division, m.metro AS metro,
               CASE WHEN RELSHIPP = 37 THEN 1 WHEN RELSHIPP = 38 THEN 2 ELSE 0 END AS gq,
               COUNT(*) AS n, SUM(PWGTP::BIGINT * PWGTP)::DOUBLE AS w2, {', '.join(sums)}
        FROM persons p JOIN metro m ON m.m_st = p.ST AND m.m_puma = p.PUMA
        WHERE AGEP >= 18 AND ({predicate})
        GROUP BY ALL"""
    frame = con.execute(query).df()
    keys = ["sex", "age_cell", "post_draft", "educ", "st", "division", "metro", "gq"]
    return Cells(frame, keys, list(measures))


def protective_cells(con, predicate):
    measures = {"adults": None, "employed": EMPLOYED}
    measures.update({name: f"{EMPLOYED} AND {flag}" for name, flag in PROTECTIVE.items()})
    sums = []
    for name, flag in measures.items():
        sums += [f"{expr} AS {name}_{r}" for r, expr in enumerate(replicate_sums(flag))]
    query = f"""
        SELECT SEX AS sex, {AGE_CELL} AS age_cell, {EDUC} AS educ, p.ST AS st, p.DIVISION AS division,
               m.metro AS metro, COUNT(*) AS n,
               SUM(CASE WHEN {EMPLOYED} THEN 1 ELSE 0 END) AS n_employed, SUM(PWGTP::BIGINT * PWGTP)::DOUBLE AS w2,
               {', '.join(sums)}
        FROM persons p JOIN metro m ON m.m_st = p.ST AND m.m_puma = p.PUMA
        WHERE AGEP BETWEEN 18 AND 64 AND ({predicate})
        GROUP BY ALL"""
    frame = con.execute(query).df()
    cells = Cells(frame, ["sex", "age_cell", "educ", "st", "division", "metro"], list(measures))
    cells.n_employed = frame["n_employed"].to_numpy(np.int64)
    return cells


def se(theta):
    """theta: array [81]; replicate SE (ACS successive-difference formula)."""
    return float(np.sqrt(4.0 / 80.0 * np.sum((theta[1:] - theta[0]) ** 2)))


def ratio(num, den):
    with np.errstate(divide="ignore", invalid="ignore"):
        return np.where(den != 0, num / den, np.nan)


def aggregate(cells, mask, keys, measures, counts=None):
    """Sum measures over masked cells by key columns -> (keys [k, len(keys)], {measure: [k, 81]}, n, w2)."""
    sub = cells.keys[mask][:, [cells.key_names.index(k) for k in keys]]
    unique, inverse = np.unique(sub, axis=0, return_inverse=True)
    inverse = inverse.ravel()
    order = np.argsort(inverse, kind="stable")
    bounds = np.flatnonzero(np.r_[True, np.diff(inverse[order]) != 0])
    out = {m: np.add.reduceat(cells.data[m][mask][order], bounds, axis=0) for m in measures}
    n = np.bincount(inverse, weights=(cells.n if counts is None else counts)[mask], minlength=len(unique))
    w2 = np.bincount(inverse, weights=cells.w2[mask], minlength=len(unique))
    return unique, out, n, w2


def align(group_keys, group_vals, ref_keys, ref_vals):
    """Put group and reference cell sums on the union of their keys."""
    union = np.unique(np.vstack([group_keys, ref_keys]), axis=0)
    def place(keys, vals):
        idx = {tuple(k): i for i, k in enumerate(keys)}
        pos = np.array([idx.get(tuple(u), -1) for u in union])
        out = {}
        for m, arr in vals.items():
            full = np.zeros((len(union), arr.shape[1]) if arr.ndim == 2 else len(union))
            full[pos >= 0] = arr[pos[pos >= 0]]
            out[m] = full
        return out
    return union, place(group_keys, group_vals), place(ref_keys, ref_vals)


def ipf(group_w, targets, margins, start, tol=1e-9, max_iter=3000):
    """One raking run. Returns (factors, converged, largest remaining margin gap)."""
    f = start.copy()
    worst = np.inf
    for _ in range(max_iter):
        worst = 0.0
        for m, t in zip(margins, targets):
            current = np.bincount(m, weights=group_w * f, minlength=len(t))
            total = current.sum()
            if not np.isfinite(total) or total <= 0 or (current[t > 0] <= 0).any():
                return f, False, np.inf
            share = current / total
            f = f * np.where(share > 0, t / np.where(share > 0, share, 1.0), 0.0)[m]
            worst = max(worst, float(np.abs(share - t).max()))
        if worst < tol:
            return f, True, worst
        if not np.isfinite(f).all() or f.max() > 1e12:
            return f, False, np.inf
    return f, False, worst


def rake(group_w, ref_w, margins, group_n):
    """Raking factors per cell and replicate so the group's weighted margins match the reference's.

    group_w, ref_w: [cells, 81]; margins: int category arrays [cells]. The reference is restricted
    to cells whose category on every margin holds a group record (common support); `dropped` is
    the reference weight share outside it. Replicates start from the full-weight factors (the
    raked solution is unique within the product family, so the start does not change it); a
    replicate that cannot be raked keeps the full-weight factors and is counted.
    """
    support = np.ones(len(group_n), bool)
    for m in margins:
        support &= (np.bincount(m, weights=group_n, minlength=m.max() + 1) > 0)[m]
    dropped = 1.0 - ref_w[support, 0].sum() / ref_w[:, 0].sum()
    ref = np.where(support[:, None], ref_w, 0.0)
    def targets(r):
        out = []
        for m in margins:
            t = np.bincount(m, weights=ref[:, r], minlength=m.max() + 1)
            out.append(t / t.sum())
        return out
    f0, converged, gap = ipf(group_w[:, 0], targets(0), margins, np.ones(len(group_n)))
    if not converged:
        return None, dropped, gap, 0
    factors = np.repeat(f0[:, None], group_w.shape[1], axis=1)
    fallbacks = 0
    for r in range(1, group_w.shape[1]):
        f, ok, _ = ipf(group_w[:, r], targets(r), margins, f0)
        if ok:
            factors[:, r] = f
        else:
            fallbacks += 1
    return factors, dropped, gap, fallbacks


def dense(codes):
    return np.unique(codes, return_inverse=True)[1].ravel()


def collapse(fine, parent, group_n, minimum=20):
    """Margin categories with fewer than `minimum` group records pool within their parent category;
    pooled buckets still under the minimum pool into one remainder bucket."""
    fine, parent = dense(fine), dense(parent)
    thin = np.bincount(fine, weights=group_n)[fine] < minimum
    code = np.where(thin, fine.max() + 1 + parent, fine)
    code_d = dense(code)
    still = thin & (np.bincount(code_d, weights=group_n)[code_d] < minimum)
    return dense(np.where(still, -1, code))


def margin_arrays(label, minimum, age, educ, st, division, metro, n):
    zero = np.zeros_like(age)
    table = {
        "age x educ": lambda: collapse(age * 4 + educ, age, n, minimum),
        "age": lambda: collapse(age, zero, n, minimum),
        "state": lambda: collapse(st, division, n, minimum),
        "metro x educ": lambda: collapse(metro * 4 + educ, educ, n, minimum),
        "division x metro": lambda: collapse(division * 4 + metro, division, n, minimum),
        "metro": lambda: collapse(metro, zero, n, minimum),
    }
    return [table[name.strip()]() for name in label.split(",")]


def raked(group, ref, mask_g, mask_r, weight, outcomes, kind, primary, counts=None):
    """(b) raking: the group's rate after reweighting to the white reference's distribution."""
    gk, gv, gn, gw2 = aggregate(group, mask_g, CELL_KEYS, [weight] + outcomes, counts)
    rk, rv, _, _ = aggregate(ref, mask_r, CELL_KEYS, [weight])
    union, g, r = align(gk, {**gv, "_n": gn, "_w2": gw2}, rk, rv)
    columns = [union[:, i] for i in range(5)]
    for label, minimum in MARGIN_SETS[kind]:
        margins = margin_arrays(label, minimum, *columns, g["_n"])
        factors, dropped, gap, fallbacks = rake(g[weight], r[weight], margins, g["_n"])
        if factors is not None:
            break
    else:
        return {o: np.full(R, np.nan) for o in outcomes}, {"margins": "raking failed", "ref_share_off_support": dropped}
    denominator = (factors * g[weight]).sum(0)
    rates = {o: ratio((factors * g[o]).sum(0), denominator) for o in outcomes}
    positive = g[weight][:, 0] > 0
    n_eff = (factors[:, 0] * g[weight][:, 0]).sum() ** 2 / float((factors[:, 0] ** 2 * g["_w2"]).sum())
    contribution = np.sort(factors[:, 0] * g[primary][:, 0])[::-1]
    top10 = contribution[:10].sum() / contribution.sum() if contribution.sum() > 0 else np.nan
    return rates, {"n_eff": n_eff, "ref_share_off_support": dropped, "margins": f"{label} (min {minimum})",
                   "replicate_fallbacks": fallbacks, "top10_cell_share": top10,
                   "max_factor": float(factors[positive, 0].max() / np.median(factors[positive, 0]))}


def indirect(group, ref, mask_g, mask_r, weight, outcomes, kind, minimum=50, counts=None):
    """(b) indirect standardisation: white rates in the group's own cells, weighted by the group."""
    gk, gv, _, _ = aggregate(group, mask_g, CELL_KEYS, [weight])
    expected = {o: np.zeros(R) for o in outcomes}
    assigned = np.zeros(len(gk), bool)
    finest = 0.0
    for depth, level in enumerate(INDIRECT_LEVELS[kind]):
        rk, rv, rn, _ = aggregate(ref, mask_r, list(level), [weight] + outcomes, counts)
        lookup = {tuple(k): i for i, k in enumerate(rk)}
        columns = [CELL_KEYS.index(c) for c in level]
        for c in np.where(~assigned)[0]:
            j = lookup.get(tuple(gk[c, columns]))
            if j is None or (rn[j] < minimum and depth < len(INDIRECT_LEVELS[kind]) - 1):
                continue
            for o in outcomes:
                expected[o] += gv[weight][c] * ratio(rv[o][j], rv[weight][j])
            assigned[c] = True
            if depth == 0:
                finest += gv[weight][c, 0]
    total = gv[weight][assigned].sum(0)
    return ({o: expected[o] / total for o in outcomes},
            {"share_at_finest_cell": finest / gv[weight][:, 0].sum(),
             "share_unmatched": 1 - total[0] / gv[weight][:, 0].sum()})


def specifications(group, ref, mask_g, mask_r, weight, outcomes, is_reference, primary, counts=None, ref_counts=None):
    """All (a) and (b) specifications -> {spec: (group_rate, comparison_rate, diagnostics)}."""
    white = {o: ratio(ref.data[o][mask_r].sum(0), ref.data[weight][mask_r].sum(0)) for o in outcomes}
    raw = {o: ratio(group.data[o][mask_g].sum(0), group.data[weight][mask_g].sum(0)) for o in outcomes}
    out = {"raw": (raw, white, {})}
    gkeys, gv, _, _ = aggregate(group, mask_g, ["educ"], [weight] + outcomes, counts)
    rkeys, rv, _, _ = aggregate(ref, mask_r, ["educ"], [weight] + outcomes, ref_counts)
    if len(gkeys) == 4 and len(rkeys) == 4:
        white_mix, group_mix = rv[weight] / rv[weight].sum(0), gv[weight] / gv[weight].sum(0)
        out["a_education_direct"] = ({o: (white_mix * ratio(gv[o], gv[weight])).sum(0) for o in outcomes}, white, {})
        out["a_education_indirect"] = (raw, {o: (group_mix * ratio(rv[o], rv[weight])).sum(0) for o in outcomes}, {})
    if not is_reference:
        names = {"age": "age", "age_educ": "a_age_education", "geo": "b_raked_geo", "full": "b_raked_full"}
        for kind, name in names.items():
            rates, diag = raked(group, ref, mask_g, mask_r, weight, outcomes, kind, primary, counts)
            out[name + "_direct" if kind in ("age", "age_educ") else name] = (rates, white, diag)
        for kind, name in {"age": "age", "age_educ": "a_age_education", "geo": "b_indirect_geo",
                           "full": "b_indirect_full"}.items():
            expected, diag = indirect(group, ref, mask_g, mask_r, weight, outcomes, kind, counts=ref_counts)
            out[name + "_indirect" if kind in ("age", "age_educ") else name] = (raw, expected, diag)
    return out


DIAGNOSTICS = ("n_eff", "ref_share_off_support", "margins", "replicate_fallbacks", "max_factor", "top10_cell_share",
               "share_at_finest_cell", "share_unmatched", "expected_ratio")


def spec_rows(base, specs, outcomes):
    rows = []
    for spec, (group_rate, comparison, diag) in specs.items():
        for outcome in outcomes:
            rel = group_rate[outcome] / comparison[outcome]
            rows.append({**base, "outcome": outcome, "spec": spec, "group_rate": group_rate[outcome][0],
                         "group_rate_se": se(group_rate[outcome]), "comparison_rate": comparison[outcome][0],
                         "comparison_se": se(comparison[outcome]), "ratio": rel[0], "ratio_se": se(rel),
                         **{k: diag.get(k, "") for k in DIAGNOSTICS}})
    return rows


def main():
    DERIVED.mkdir(exist_ok=True)
    only = sys.argv[1:]
    if only:  # smoke test on named groups; the reference is always included
        for name in list(GROUPS):
            if name not in only and name != REFERENCE:
                del GROUPS[name]
    con = connect()
    hood = pd.read_csv(DERIVED / "neighborhood_expected.csv")
    hood = hood[hood.fiscal_year == "FY23"]
    military, protective = {}, {}
    for name, (predicate, _) in GROUPS.items():
        military[name] = military_cells(con, predicate)
        protective[name] = protective_cells(con, predicate)
        print(f"  ✓ {name}: {military[name].n.sum():,} adult records, "
              f"{military[name].data['pop'][:, 0].sum() / 3:,.0f} adults per year", flush=True)

    rate_rows, educ_rows, adjusted_rows = [], [], []
    outcomes = list(MILITARY)
    ref = military[REFERENCE]
    for name, cells in military.items():
        for sex in (1, 2):
            for band, (ages, post_draft) in BANDS.items():
                def band_mask(c, universe="all"):
                    m = (c.col("sex") == sex) & np.isin(c.col("age_cell"), ages)
                    if post_draft:
                        m &= c.col("post_draft") == 1
                    if universe == "household":
                        m &= c.col("gq") == 0
                    return m
                base = {"group": name, "sex": "men" if sex == 1 else "women", "age_band": band}
                for universe in ("all", "household"):
                    mg, mr = band_mask(cells, universe), band_mask(ref, universe)
                    pop, ref_pop = cells.data["pop"][mg].sum(0), ref.data["pop"][mr].sum(0)
                    for outcome in outcomes:
                        theta = ratio(cells.data[outcome][mg].sum(0), pop)
                        rel = theta / ratio(ref.data[outcome][mr].sum(0), ref_pop)
                        in_gq = ratio(cells.data[outcome][mg & (cells.col("gq") > 0)].sum(0), cells.data[outcome][mg].sum(0))
                        rate_rows.append({**base, "universe": universe, "outcome": outcome,
                                          "n_records": int(cells.n[mg].sum()), "adults_per_year": round(pop[0] / 3),
                                          "rate": theta[0], "se": se(theta), "ratio_to_nh_white": rel[0],
                                          "ratio_se": se(rel), "share_in_group_quarters": in_gq[0]})
                mg, mr = band_mask(cells), band_mask(ref)
                gkeys, gv, gn, _ = aggregate(cells, mg, ["educ"], ["pop"] + outcomes)
                rkeys, rv, _, _ = aggregate(ref, mr, ["educ"], ["pop"] + outcomes)
                for i, e in enumerate(gkeys.ravel()):
                    j = int(np.where(rkeys.ravel() == e)[0][0])
                    for outcome in outcomes:
                        theta = ratio(gv[outcome][i], gv["pop"][i])
                        rel = theta / ratio(rv[outcome][j], rv["pop"][j])
                        educ_rows.append({**base, "education": EDUC_NAMES[e], "outcome": outcome,
                                          "n_records": int(gn[i]), "adults_per_year": round(gv["pop"][i][0] / 3),
                                          "rate": theta[0], "se": se(theta), "ratio_to_nh_white": rel[0],
                                          "ratio_se": se(rel)})
                specs = specifications(cells, ref, mg, mr, "pop", outcomes, name == REFERENCE, "ever_active_duty")
                raw, white = specs["raw"][0], specs["raw"][1]
                same_ages = specs["age_indirect"][1] if "age_indirect" in specs else white
                for basis in ("per_teen_15_17", "per_youth_18_24", "per_household"):
                    row = hood[(hood.group == GROUPS[name][1]) & (hood.propensity_basis == basis)]
                    factor = float(row["expected_ratio_to_nh_white"].iloc[0])
                    specs[f"c_neighborhood_{basis}"] = (raw, {o: white[o] * factor for o in outcomes},
                                                        {"expected_ratio": factor})
                    specs[f"c_age_neighborhood_{basis}"] = (raw, {o: same_ages[o] * factor for o in outcomes},
                                                            {"expected_ratio": factor})
                base["n_records"] = int(cells.n[mg].sum())
                adjusted_rows += spec_rows(base, specs, outcomes)
        print(f"  ✓ military specifications: {name}", flush=True)

    protective_rows = []
    ref = protective[REFERENCE]
    occupations = list(PROTECTIVE)
    for name, cells in protective.items():
        for sex in (1, 2):
            mg, mr = cells.col("sex") == sex, ref.col("sex") == sex
            for denominator in ("employed", "adults"):
                counts = cells.n_employed if denominator == "employed" else None
                ref_counts = ref.n_employed if denominator == "employed" else None
                specs = specifications(cells, ref, mg, mr, denominator, occupations, name == REFERENCE,
                                       "public_safety_total", counts, ref_counts)
                n_den = int((cells.n_employed if denominator == "employed" else cells.n)[mg].sum())
                base = {"group": name, "sex": "men" if sex == 1 else "women", "age_band": "18_64",
                        "per_1000": denominator, "n_records_denominator": n_den,
                        "denominator_per_year": round(cells.data[denominator][mg, 0].sum() / 3)}
                for row in spec_rows(base, specs, occupations):
                    if denominator == "employed":
                        row["n_eff"] = ""  # Kish n_eff uses adults' squared weights; per-adult rows only
                    protective_rows.append(row)
        print(f"  ✓ protective specifications: {name}", flush=True)

    for filename, rows in (("military_rates.csv", rate_rows), ("military_by_education.csv", educ_rows),
                           ("military_adjusted.csv", adjusted_rows), ("protective_service.csv", protective_rows)):
        frame = pd.DataFrame(rows)
        frame.to_csv(DERIVED / filename, index=False, float_format="%.6g", lineterminator="\n")
        print(f"  ✓ {filename}: {len(frame)} rows")


if __name__ == "__main__":
    sys.exit(main())
