"""Mexican-origin / all-donor public medical payments, MEPS 2016-2024 pooled.

Gates first: from HC-256 alone this script must reproduce, to 1e-9, every
public-payment ratio and standard error the 2024 lane published
(`../meps_mexican_origin_medical_2026_09_22/derived/ratios.csv`: 0.688 at 18-64,
0.893 at 65+, 0.757 all ages, and the ten transport cells), and that lane's
2023+2024 pooled 65+ check (0.810). It stops with [BLOCKED] otherwise.

Then, on the nine pooled years (weights / 9, HC-036 STRA9624/PSU9624, 2024
dollars by the CPI-U medical care index), for every transport cell (age band x
US birth, the cells `donor_model` matches on), every ledger band and the pooled
age domains:
  * plain weighted means (the transport's estimand);
  * means winsorized within transport cell at the 99.5th and 99.9th percentiles;
  * a two-part model: share with any payment x mean when positive, the second
    part both arithmetic (an identity with the plain ratio) and log-normal with
    a common smearing factor (ratio of geometric means, insensitive to the tail);
by payer (Medicare, Medicaid, other public and its VA / TRICARE parts), year by
year with each year's own design, and the MCBS reconciliation and
disconfirmation tables. `translate.py` turns the cell ratios into dollars.

Run from the repository root:
  OPENBLAS_NUM_THREADS=1 uv run --no-project python3 \
      infra/immigration-fiscal/medical_ethnicity_pooled_2026_09_23/pooled_ratios.py
"""
from __future__ import annotations

import json
import pickle
import sys
from pathlib import Path

import numpy as np
import pandas as pd

LANE = Path(__file__).resolve().parent
sys.path.insert(0, str(LANE))
from design import Z95, Design, Est, chi2_sf, combo, exp_est, log_est, mean, ratio, weighted_quantile  # noqa: E402

CACHE = LANE / "_cache"
DERIVED = LANE / "derived"
REPO = LANE.parents[2]
PRIOR = REPO / "infra/immigration-fiscal/meps_mexican_origin_medical_2026_09_22"
FRED_CPI = Path("/Users/alien/research-data/immigration-fiscal/data/external/fred/cpi_all_urban.csv")

YEARS = list(range(2016, 2025))
COVID = (2020, 2021)
TRANSPORT_LABELS = ["0-17", "18-34", "35-49", "50-64", "65+"]
LEDGER_LABELS = ["0-17", "18-24", "25-34", "35-44", "45-54", "55-64", "65-74", "75+"]
NATIVITY = {"us_born": 1, "foreign_born": 2, "both": 0}

# name -> column(s) summed; payment measures are deflated, shares are not
DOLLARS = {
    "public": ["public"],                        # transport list + OPU (harmonized Medicaid)
    "public_transport": ["public_transport"],    # the transport's verbatim six payers
    "medicare": ["TOTMCR"],
    "medicaid": ["medicaid"],                    # TOTMCD (+ TOTOPU 2016-18)
    "medicaid_reported": ["TOTMCD"],
    "other_public": ["other_public"],            # VA + TRICARE + other federal + state/local
    "va": ["TOTVA"],
    "tricare": ["TOTTRI"],
    "ofd_stl": ["TOTOFD", "TOTSTL"],
    "opu": ["TOTOPU"],
    "out_of_pocket": ["TOTSLF"],
    "private": ["private"],
    "total_exp": ["TOTEXP"],
}
WINSOR_MEASURES = ["public", "public_transport", "medicare", "medicaid", "other_public", "va", "tricare"]
TWO_PART_MEASURES = ["public", "medicare", "medicaid", "other_public"]
PAYER_MEASURES = ["public", "public_transport", "medicare", "medicaid", "medicaid_reported",
                  "other_public", "va", "tricare", "ofd_stl"]


def _ok(msg):
    print(f"  ✓ {msg}", flush=True)


def _warn(msg):
    print(f"  ! {msg}", flush=True)


def _header(s):
    print(f"\n[{s}]", flush=True)


def fail(msg):
    print(f"  ✗ [BLOCKED] {msg}", file=sys.stderr, flush=True)
    raise SystemExit(2)


def transport_band(age):
    """Verbatim `build/meps_health_transport_2024.py::age_band`."""
    return np.digitize(age, [18, 35, 50, 65])


def ledger_band(age):
    """Verbatim `ledger_absolute_2026_09_17/profile_export.py` line 80 bands."""
    return np.digitize(age, [18, 25, 35, 45, 55, 65, 75])


class Frame:
    """Arrays for one estimation sample (one year, or the pool)."""

    def __init__(self, d: pd.DataFrame, weight_divisor: float, deflator: str | None,
                 stratum: str, psu: str, year_normalize: bool = False):
        self.d = d
        self.w = d.PERWT.to_numpy(float) / weight_divisor
        self.design = Design(d[stratum].to_numpy(), d[psu].to_numpy(), self.w)
        age = d.AGE.to_numpy()
        born = d.BORNUSA.to_numpy()
        self.age, self.born = age, born
        self.valid = (self.w > 0) & (age >= 0) & np.isin(born, [1, 2])
        self.tb = transport_band(age)
        self.lb = ledger_band(age)
        defl = d[deflator].to_numpy(float) if deflator else np.ones(len(d))
        self.y = {}
        for name, cols in DOLLARS.items():
            self.y[name] = d[cols].sum(axis=1).to_numpy(float) * defl
        if year_normalize:
            # each measure's all-donor valid-set mean made equal across years (2024 level)
            yr = d.year.to_numpy()
            for name in self.y:
                ref = None
                means = {}
                for yv in np.unique(yr):
                    m = self.valid & (yr == yv)
                    means[yv] = (self.w[m] * self.y[name][m]).sum() / self.w[m].sum()
                ref = means.get(2024, np.mean(list(means.values())))
                fac = np.array([ref / means[v] if means[v] > 0 else 1.0 for v in yr])
                self.y[name] = self.y[name] * fac
        self.share = {
            "any_public": (self.y["public"] > 0).astype(float),
            "medicaid_ever": d.MCDEV.eq(1).to_numpy(float),
            "medicare_ever": d.MCREV.eq(1).to_numpy(float),
            "uninsured_all_year": d.UNINS.eq(1).to_numpy(float),
        }
        self.groups = {
            "mexican_origin": d.HISPNCAT.eq(1).to_numpy(),
            "all_donors": np.ones(len(d), bool),
            "nh_white": d.RACETHX.eq(2).to_numpy(),
            "hispanic": d.HISPANX.eq(1).to_numpy(),
        }
        self.caps: dict = {}

    def domains(self) -> list[dict]:
        out = []
        for b, lab in enumerate(TRANSPORT_LABELS):
            for nat, code in NATIVITY.items():
                m = self.valid & (self.tb == b) & ((self.born == code) if code else True)
                out.append(dict(scheme="transport", band=lab, nativity=nat, mask=m))
        for b, lab in enumerate(LEDGER_LABELS):
            for nat, code in NATIVITY.items():
                m = self.valid & (self.lb == b) & ((self.born == code) if code else True)
                out.append(dict(scheme="ledger", band=lab, nativity=nat, mask=m))
        for lab, am in [("all_ages", self.valid), ("65plus", self.valid & (self.age >= 65)),
                        ("18_64", self.valid & (self.age >= 18) & (self.age < 65)),
                        ("under18", self.valid & (self.age < 18))]:
            for nat, code in NATIVITY.items():
                out.append(dict(scheme="age_domain", band=lab, nativity=nat,
                                mask=am & ((self.born == code) if code else True)))
        return out

    def set_caps(self, q: float) -> dict:
        """Weighted q-quantile of each measure among all valid donors, per transport cell."""
        caps = {}
        for name in WINSOR_MEASURES:
            for b in range(5):
                for code in (1, 2):
                    m = self.valid & (self.tb == b) & (self.born == code)
                    caps[(name, b, code)] = weighted_quantile(self.y[name][m], self.w[m], q)
        return caps

    def capped(self, name: str, caps: dict) -> np.ndarray:
        y = self.y[name].copy()
        for b in range(5):
            for code in (1, 2):
                c = caps[(name, b, code)]
                if c > 0:
                    m = (self.tb == b) & (self.born == code)
                    y[m] = np.minimum(y[m], c)
        return y


def est_mean(fr: Frame, y: np.ndarray, dmask: np.ndarray, group: str) -> Est:
    return mean(fr.design, y, fr.w, dmask & fr.groups[group])


def two_part(fr: Frame, y: np.ndarray, dmask: np.ndarray, g: str, ref: str) -> dict:
    """share>0 ratio x conditional-mean ratio; arithmetic and log-normal second parts."""
    pos = (y > 0).astype(float)
    ly = np.where(y > 0, np.log(np.where(y > 0, y, 1.0)), 0.0)
    out = {}
    pg, pr = est_mean(fr, pos, dmask, g), est_mean(fr, pos, dmask, ref)
    posmask = y > 0
    mg = mean(fr.design, y, fr.w, dmask & fr.groups[g] & posmask)
    mr = mean(fr.design, y, fr.w, dmask & fr.groups[ref] & posmask)
    lg = mean(fr.design, ly, fr.w, dmask & fr.groups[g] & posmask)
    lr = mean(fr.design, ly, fr.w, dmask & fr.groups[ref] & posmask)
    part1 = ratio(pg, pr)
    part2_arith = ratio(mg, mr)
    log_r2 = combo([(1.0, lg), (-1.0, lr)])
    part2_geo = exp_est(log_r2)
    log_total = combo([(1.0, log_est(pg)), (-1.0, log_est(pr)), (1.0, log_r2)])
    two_part_lognormal = exp_est(log_total)
    arith_total = exp_est(combo([(1.0, log_est(part1)), (1.0, log_est(part2_arith))]))
    for k, e in [("share_positive_group", pg), ("share_positive_ref", pr), ("participation_ratio", part1),
                 ("conditional_mean_ratio", part2_arith), ("conditional_geometric_ratio", part2_geo),
                 ("two_part_arithmetic", arith_total), ("two_part_lognormal", two_part_lognormal)]:
        out[k] = e
    out["n_positive_group"] = int((dmask & fr.groups[g] & posmask).sum())
    out["n_positive_ref"] = int((dmask & fr.groups[ref] & posmask).sum())
    return out


def ratio_row(fr: Frame, e: Est, **meta) -> dict:
    se = e.se(fr.design)
    ok = np.isfinite(e.value) and np.isfinite(se)
    return dict(meta, ratio=e.value, se=se,
                ci_lo=e.value - Z95 * se if ok else np.nan,
                ci_hi=e.value + Z95 * se if ok else np.nan,
                excludes_one=bool(ok and (e.value - Z95 * se > 1 or e.value + Z95 * se < 1)))


# ---------------------------------------------------------------------------
def gate_2024(pool: pd.DataFrame) -> dict:
    """Reproduce the 2024 lane's published public ratios and SEs from HC-256 alone."""
    d = pool[pool.year.eq(2024)].reset_index(drop=True)
    fr = Frame(d, 1.0, None, "VARSTR", "VARPSU")
    prior = pd.read_csv(PRIOR / "derived/ratios.csv")
    prior = prior[(prior.denominator == "all_donors") & (prior.measure == "public")
                  & (prior.subgroup == "all")]
    y = fr.y["public_transport"]
    checked, worst_r, worst_se = [], 0.0, 0.0
    lab_map = {"pooled": "age_domain"}
    for dom in fr.domains():
        sch = dom["scheme"]
        pscheme = "pooled" if sch == "age_domain" else sch
        if sch == "transport":
            pband = str(TRANSPORT_LABELS.index(dom["band"]))
        elif sch == "ledger":
            pband = str(LEDGER_LABELS.index(dom["band"]))
        else:
            pband = dom["band"]
        row = prior[(prior.scheme == pscheme) & (prior.band.astype(str) == pband)
                    & (prior.nativity == dom["nativity"])]
        if len(row) != 1:
            continue
        r = ratio(est_mean(fr, y, dom["mask"], "mexican_origin"), est_mean(fr, y, dom["mask"], "all_donors"))
        se = r.se(fr.design)
        dr, dse = abs(r.value - row.ratio.iloc[0]), abs(se - row.se.iloc[0])
        worst_r, worst_se = max(worst_r, dr), max(worst_se, dse)
        checked.append(dict(scheme=sch, band=dom["band"], nativity=dom["nativity"], ratio=r.value,
                            published=float(row.ratio.iloc[0]), se=se, published_se=float(row.se.iloc[0])))
        if dr > 1e-9 or dse > 1e-9:
            fail(f"2024 gate: {sch} {dom['band']} {dom['nativity']} ratio {r.value:.6f} se {se:.6f} "
                 f"vs published {row.ratio.iloc[0]:.6f} / {row.se.iloc[0]:.6f}")
    if len(checked) < 45:
        fail(f"2024 gate matched only {len(checked)} published rows")
    head = {c["band"]: c for c in checked if c["scheme"] == "age_domain" and c["nativity"] == "both"}
    _ok(f"2024 gate: {len(checked)} published ratios and SEs reproduce (max |diff| ratio {worst_r:.1e}, "
        f"SE {worst_se:.1e}); 18-64 {head['18_64']['ratio']:.3f} (SE {head['18_64']['se']:.3f}), "
        f"65+ {head['65plus']['ratio']:.3f} (SE {head['65plus']['se']:.3f}), "
        f"all ages {head['all_ages']['ratio']:.3f}")
    return {"rows_checked": len(checked), "max_abs_diff_ratio": worst_r, "max_abs_diff_se": worst_se,
            "headline": {k: {"ratio": v["ratio"], "se": v["se"]} for k, v in head.items()}}


def gate_2023_2024(pool: pd.DataFrame) -> dict:
    """Reproduce the 2024 lane's secondary pooled 65+ check with its own method."""
    audit = json.loads((PRIOR / "derived/audit.json").read_text())["pooled_2023_2024_65plus"]
    cpi = pd.read_csv(FRED_CPI)
    cpi["yr"] = cpi.observation_date.str.slice(0, 4).astype(int)
    factor = float(cpi[cpi.yr == 2024].CPIAUCSL.mean()) / float(cpi[cpi.yr == 2023].CPIAUCSL.mean())
    if abs(factor - audit["deflator_2023_to_2024"]) > 1e-12:
        fail(f"FRED deflator {factor} != lane's {audit['deflator_2023_to_2024']}")
    d = pool[pool.year.isin([2023, 2024])].reset_index(drop=True).copy()
    d["VS"] = np.where(d.year.eq(2023), d.VARSTR + 10000, d.VARSTR)
    d["gate_defl"] = np.where(d.year.eq(2023), factor, 1.0)
    fr = Frame(d, 2.0, "gate_defl", "VS", "VARPSU")
    m = fr.valid & (fr.age >= 65)
    r = ratio(est_mean(fr, fr.y["public_transport"], m, "mexican_origin"),
              est_mean(fr, fr.y["public_transport"], m, "all_donors"))
    pub = audit["pooled_65plus_public_ratio_vs_all_donors"]
    se = r.se(fr.design)
    if abs(r.value - pub["ratio"]) > 1e-9 or abs(se - pub["se"]) > 1e-9:
        fail(f"2023+2024 gate: {r.value:.6f}/{se:.6f} vs lane {pub['ratio']:.6f}/{pub['se']:.6f}")
    _ok(f"2023+2024 gate: 65+ ratio {r.value:.3f} (SE {se:.3f}) reproduces the lane's pooled check")
    return {"ratio": r.value, "se": se, "published": pub}


# ---------------------------------------------------------------------------
def estimate_all(fr: Frame, label: str, specs: dict[str, dict | None]) -> tuple[pd.DataFrame, pd.DataFrame, dict]:
    """Means, ratios and the Est objects of the transport cells, for each spec."""
    cells, rows, store = [], [], {}
    comparisons = [("mexican_origin", "all_donors"), ("mexican_origin", "nh_white"), ("hispanic", "nh_white")]
    for spec, caps in specs.items():
        measures = list(DOLLARS) + list(fr.share) if caps is None else WINSOR_MEASURES
        ys = {}
        for name in measures:
            if name in fr.share:
                ys[name] = fr.share[name]
            else:
                ys[name] = fr.y[name] if caps is None else fr.capped(name, caps)
        for dom in fr.domains():
            for name, y in ys.items():
                ests = {g: est_mean(fr, y, dom["mask"], g) for g in fr.groups}
                for g, e in ests.items():
                    cells.append(dict(sample=label, spec=spec, scheme=dom["scheme"], band=dom["band"],
                                      nativity=dom["nativity"], group=g, measure=name, mean=e.value,
                                      se=e.se(fr.design), n=e.n, weighted=e.W))
                for num, den in comparisons:
                    r = ratio(ests[num], ests[den])
                    rows.append(ratio_row(fr, r, sample=label, spec=spec, scheme=dom["scheme"],
                                          band=dom["band"], nativity=dom["nativity"],
                                          comparison=f"{num}/{den}", measure=name,
                                          n_num=ests[num].n, n_den=ests[den].n))
                    if dom["scheme"] == "transport" and (num, den) == ("mexican_origin", "all_donors"):
                        store[(spec, name, dom["band"], dom["nativity"])] = r
    return pd.DataFrame(cells), pd.DataFrame(rows), store


def two_part_table(fr: Frame, label: str) -> tuple[pd.DataFrame, dict]:
    rows, store = [], {}
    for dom in fr.domains():
        if dom["scheme"] == "ledger":
            continue
        for name in TWO_PART_MEASURES:
            tp = two_part(fr, fr.y[name], dom["mask"], "mexican_origin", "all_donors")
            for k, e in tp.items():
                if isinstance(e, Est):
                    rows.append(ratio_row(fr, e, sample=label, scheme=dom["scheme"], band=dom["band"],
                                          nativity=dom["nativity"], measure=name, component=k,
                                          n_positive_group=tp["n_positive_group"],
                                          n_positive_ref=tp["n_positive_ref"]))
            if dom["scheme"] == "transport":
                store[("two_part_lognormal", name, dom["band"], dom["nativity"])] = tp["two_part_lognormal"]
    return pd.DataFrame(rows), store


def headline(rt: pd.DataFrame, band: str, measure="public", spec="plain", comparison="mexican_origin/all_donors",
             nativity="both", scheme="age_domain"):
    r = rt[(rt.spec == spec) & (rt.scheme == scheme) & (rt.band == band) & (rt.nativity == nativity)
           & (rt.comparison == comparison) & (rt.measure == measure)]
    if len(r) != 1:
        fail(f"headline lookup {band} {measure} {spec} {comparison}: {len(r)} rows")
    return r.iloc[0]


def by_year(pool: pd.DataFrame, caps995: dict) -> tuple[pd.DataFrame, dict, dict]:
    """Each year alone with its own design; plain means and, with the pooled
    99.5th-percentile caps (2024 dollars) applied to that year, winsorized means."""
    rows, stores, designs = [], {}, {}
    for yv in YEARS:
        d = pool[pool.year.eq(yv)].reset_index(drop=True)
        fr = Frame(d, 1.0, "defl_med", "VARSTR", "VARPSU")
        designs[yv] = fr.design
        for dom in fr.domains():
            if dom["scheme"] == "ledger":
                continue
            for name in ["public", "medicare", "medicaid", "other_public", "va", "tricare"]:
                for spec, y in [("plain", fr.y[name]), ("winsor_p995", fr.capped(name, caps995))]:
                    num = est_mean(fr, y, dom["mask"], "mexican_origin")
                    den = est_mean(fr, y, dom["mask"], "all_donors")
                    r = ratio(num, den)
                    rows.append(ratio_row(fr, r, year=yv, spec=spec, scheme=dom["scheme"], band=dom["band"],
                                          nativity=dom["nativity"], measure=name, n_num=num.n, n_den=den.n,
                                          mean_num=num.value, mean_den=den.value))
                    if dom["scheme"] == "transport":
                        stores[(spec, yv, name, dom["band"], dom["nativity"])] = r
        _ok(f"[{YEARS.index(yv) + 1}/{len(YEARS)}] {yv}: annual-design ratios, "
            f"{int((fr.valid & fr.groups['mexican_origin']).sum()):,} Mexican-origin donors")
    return pd.DataFrame(rows), stores, designs


def heterogeneity(yr: pd.DataFrame) -> pd.DataFrame:
    out = []
    for (spec, sch, band, nat, meas), g in yr.groupby(["spec", "scheme", "band", "nativity", "measure"]):
        g = g[np.isfinite(g.ratio) & np.isfinite(g.se) & (g.se > 0)]
        if len(g) < 3:
            continue
        wv = 1 / g.se ** 2
        rbar = float((wv * g.ratio).sum() / wv.sum())
        q = float((wv * (g.ratio - rbar) ** 2).sum())
        k = len(g) - 1
        c = g[g.year.isin(COVID)]
        out.append(dict(spec=spec, scheme=sch, band=band, nativity=nat, measure=meas, years=len(g),
                        inverse_variance_mean=rbar, cochran_q=q, df=k, p_value=chi2_sf(q, k),
                        min_ratio=float(g.ratio.min()), max_ratio=float(g.ratio.max()),
                        covid_2020_2021=";".join(f"{int(a)}:{b:.3f}" for a, b in zip(c.year, c.ratio))))
    return pd.DataFrame(out)


def mcbs_reconciliation(fr: Frame, label: str) -> pd.DataFrame:
    """Walk from the ledger's estimand to the MCBS lane's, one definitional step at a time."""
    d = fr.d
    old = fr.valid & (fr.age >= 65)
    mcr = d.MCREV.eq(1).to_numpy()
    pov = d.POVCAT.to_numpy()
    mcbs_public = fr.y["medicare"] + fr.y["medicaid"]
    steps = [
        ("1 ledger estimand: Mexican-origin / all donors, all public payers", old, "mexican_origin", "all_donors", fr.y["public"]),
        ("2 reference switched to non-Hispanic white", old, "mexican_origin", "nh_white", fr.y["public"]),
        ("3 group widened to all Hispanic (MCBS CSP_RACE=3)", old, "hispanic", "nh_white", fr.y["public"]),
        ("4 restricted to Medicare-ever (MCBS universe)", old & mcr, "hispanic", "nh_white", fr.y["public"]),
        ("5 public = Medicare + Medicaid only (MCBS payer set)", old & mcr, "hispanic", "nh_white", mcbs_public),
        ("6a step 5 below 200% FPL (POVCAT 1-3)", old & mcr & np.isin(pov, [1, 2, 3]), "hispanic", "nh_white", mcbs_public),
        ("6b step 5 at or above 200% FPL (POVCAT 4-5)", old & mcr & np.isin(pov, [4, 5]), "hispanic", "nh_white", mcbs_public),
        ("7a Mexican-origin / all donors below 200% FPL", old & np.isin(pov, [1, 2, 3]), "mexican_origin", "all_donors", fr.y["public"]),
        ("7b Mexican-origin / all donors at or above 200% FPL", old & np.isin(pov, [4, 5]), "mexican_origin", "all_donors", fr.y["public"]),
        ("8 Mexican-origin / all donors, Medicare-ever only", old & mcr, "mexican_origin", "all_donors", fr.y["public"]),
    ]
    rows = []
    for step, m, g, ref, y in steps:
        num, den = est_mean(fr, y, m, g), est_mean(fr, y, m, ref)
        rows.append(ratio_row(fr, ratio(num, den), sample=label, step=step, group=g, reference=ref,
                              mean_group=num.value, mean_reference=den.value, n_group=num.n, n_reference=den.n))
    for g in ["mexican_origin", "hispanic", "nh_white", "all_donors"]:
        for sh in ["medicaid_ever", "medicare_ever", "uninsured_all_year"]:
            e = est_mean(fr, fr.share[sh], old, g)
            rows.append(dict(sample=label, step=f"share 65+: {sh}", group=g, reference="",
                             mean_group=e.value, mean_reference=np.nan, n_group=e.n, n_reference=0,
                             ratio=np.nan, se=e.se(fr.design), ci_lo=np.nan, ci_hi=np.nan, excludes_one=False))
        low = est_mean(fr, np.isin(pov, [1, 2, 3]).astype(float), old, g)
        rows.append(dict(sample=label, step="share 65+: below 200% FPL", group=g, reference="",
                         mean_group=low.value, mean_reference=np.nan, n_group=low.n, n_reference=0,
                         ratio=np.nan, se=low.se(fr.design), ci_lo=np.nan, ci_hi=np.nan, excludes_one=False))
    return pd.DataFrame(rows)


def standardized(fr: Frame, label: str) -> pd.DataFrame:
    """Direct standardization of the public ratio to the all-donor mix of Medicaid
    coverage, of poverty category, and of both."""
    d = fr.d
    mcd = d.MCDEV.to_numpy()
    pov = d.POVCAT.to_numpy()
    rows = []
    for dom_label, am in [("65plus", fr.valid & (fr.age >= 65)),
                          ("18_64", fr.valid & (fr.age >= 18) & (fr.age < 65)),
                          ("under18", fr.valid & (fr.age < 18)), ("all_ages", fr.valid)]:
        schemes = {
            "medicaid_coverage": [mcd == 1, mcd == 2],
            "poverty_category": [pov == k for k in (1, 2, 3, 4, 5)],
            "coverage_x_poverty": [(mcd == c) & (pov == k) for c in (1, 2) for k in (1, 2, 3, 4, 5)],
        }
        for sname, strata in schemes.items():
            shares = [float(fr.w[am & s].sum() / fr.w[am].sum()) for s in strata]
            num = combo([(a, est_mean(fr, fr.y["public"], am & s, "mexican_origin"))
                         for a, s in zip(shares, strata) if a > 0])
            den = combo([(a, est_mean(fr, fr.y["public"], am & s, "all_donors"))
                         for a, s in zip(shares, strata) if a > 0])
            empty = [k for k, (a, s) in enumerate(zip(shares, strata))
                     if a > 0 and (am & s & fr.groups["mexican_origin"]).sum() == 0]
            r = ratio(num, den)
            pooled = ratio(est_mean(fr, fr.y["public"], am, "mexican_origin"),
                           est_mean(fr, fr.y["public"], am, "all_donors"))
            rows.append(ratio_row(fr, r, sample=label, domain=dom_label, standardized_on=sname,
                                  unstandardized_ratio=pooled.value, empty_group_strata=len(empty)))
    return pd.DataFrame(rows)


def disconfirmation(fr: Frame, label: str) -> pd.DataFrame:
    """Where MEPS could hide excess public spending: Medicaid for non-enrollees,
    the uninsured, recent arrivals."""
    d = fr.d
    rows = []
    yr = d.year.to_numpy()
    mcd2 = d.MCDEV.eq(2).to_numpy()
    unins = d.UNINS.eq(1).to_numpy()
    yrsin = d.YRSINUS.to_numpy()
    for dom_label, am in [("all_ages", fr.valid), ("65plus", fr.valid & (fr.age >= 65)),
                          ("18_64", fr.valid & (fr.age >= 18) & (fr.age < 65)),
                          ("under18", fr.valid & (fr.age < 18))]:
        for g in ["mexican_origin", "all_donors", "nh_white"]:
            def put(what, e, extra=None):
                rows.append(dict(sample=label, domain=dom_label, group=g, quantity=what, value=e.value,
                                 se=e.se(fr.design), n=e.n, **(extra or {})))
            pre = am & np.isin(yr, [2016, 2017, 2018])
            post = am & (yr >= 2019)
            put("OPU $/person 2016-18 (Medicaid paid, person not reporting enrollment)",
                est_mean(fr, fr.y["opu"], pre, g))
            put("OPU share of harmonized Medicaid $ 2016-18",
                ratio(est_mean(fr, fr.y["opu"], pre, g), est_mean(fr, fr.y["medicaid"], pre, g)))
            put("Medicaid $/person paid for people never reporting Medicaid, 2019-24",
                est_mean(fr, fr.y["medicaid"] * mcd2, post, g))
            put("share of Medicaid $ paid for people never reporting Medicaid, 2019-24",
                ratio(est_mean(fr, fr.y["medicaid"] * mcd2, post, g), est_mean(fr, fr.y["medicaid"], post, g)))
            put("uninsured all year, share", est_mean(fr, fr.share["uninsured_all_year"], am, g))
            put("public $/person among the uninsured all year", est_mean(fr, fr.y["public"], am & unins, g))
            put("state/local + other federal $/person among the uninsured all year",
                est_mean(fr, fr.y["ofd_stl"], am & unins, g))
            put("Medicaid ever, share", est_mean(fr, fr.share["medicaid_ever"], am, g))
        # recent arrivals vs all foreign-born donors, same age domain
        fb = am & (fr.born == 2)
        for lab, codes in [("under 5 years in US", [1, 2]), ("5-14 years", [3, 4]), ("15+ years", [5])]:
            m = fb & np.isin(yrsin, codes)
            num = est_mean(fr, fr.y["public"], m, "mexican_origin")
            den = est_mean(fr, fr.y["public"], fb, "all_donors")
            r = ratio(num, den)
            rows.append(dict(sample=label, domain=dom_label, group="mexican_origin foreign-born",
                             quantity=f"public ratio, {lab} / all foreign-born donors", value=r.value,
                             se=r.se(fr.design), n=num.n))
    return pd.DataFrame(rows)


def main():
    DERIVED.mkdir(exist_ok=True)
    pool = pd.read_parquet(CACHE / "pooled.parquet")
    audit = {"deflator": "CUUR0000SAM CPI-U Medical care, NSA annual average, 2024=1 (BLS)",
             "weights": "PERWT / 9 in the pool (HC-036 section 4.0); PERWT in single years",
             "variance": "with-replacement stratified-PSU Taylor linearization; STRA9624/PSU9624 "
                         "from HC-036 in the pool, VARSTR/VARPSU in single years"}

    _header("gates")
    audit["gate_2024"] = gate_2024(pool)
    audit["gate_2023_2024"] = gate_2023_2024(pool)

    _header("pooled 2016-2024")
    fr = Frame(pool, 9.0, "defl_med", "STRA9624", "PSU9624")
    audit["pooled_sample"] = {
        "person_years": int(len(pool)), "valid_donors": int(fr.valid.sum()),
        "mexican_origin_valid": int((fr.valid & fr.groups["mexican_origin"]).sum()),
        "psus": fr.design.n_psu, "strata": len(fr.design.strata)}
    _ok(f"{int(fr.valid.sum()):,} valid donor person-years, "
        f"{int((fr.valid & fr.groups['mexican_origin']).sum()):,} Mexican-origin; "
        f"{fr.design.n_psu} PSUs in {len(fr.design.strata)} strata")
    caps995, caps999 = fr.set_caps(0.995), fr.set_caps(0.999)
    pd.DataFrame([dict(measure=k[0], band=TRANSPORT_LABELS[k[1]], nativity="us_born" if k[2] == 1 else "foreign_born",
                       cap_p995=v, cap_p999=caps999[k]) for k, v in caps995.items()]).to_csv(
        DERIVED / "winsor_caps.csv", index=False)
    cells, rt, store = estimate_all(fr, "pooled_2016_2024",
                                    {"plain": None, "winsor_p995": caps995, "winsor_p999": caps999})
    _ok(f"means {len(cells):,} rows, ratios {len(rt):,} rows (plain, winsorized 99.5 and 99.9)")
    tp, tp_store = two_part_table(fr, "pooled_2016_2024")
    store.update(tp_store)
    _ok(f"two-part rows {len(tp):,}")

    _header("sensitivity samples")
    extra, sample_designs = [], {}
    for label, sub, div, defl, norm in [
            ("pooled_excl_2020_2021", pool[~pool.year.isin(COVID)], 7.0, "defl_med", False),
            ("pooled_cpi_all_items", pool, 9.0, "defl_all", False),
            ("pooled_year_normalized", pool, 9.0, "defl_med", True)]:
        sfr = Frame(sub.reset_index(drop=True), div, defl, "STRA9624", "PSU9624", year_normalize=norm)
        c2, r2, s2 = estimate_all(sfr, label, {"plain": None})
        sample_designs[label] = sfr.design
        extra.append(r2)
        for k, v in s2.items():
            store[(label,) + k[1:]] = v
        _ok(f"{label}: 65+ {headline(r2, '65plus').ratio:.3f}, 18-64 {headline(r2, '18_64').ratio:.3f}, "
            f"under 18 {headline(r2, 'under18').ratio:.3f}")
    rt_all = pd.concat([rt] + extra, ignore_index=True)

    _header("year by year")
    yr, yr_store, yr_designs = by_year(pool, caps995)
    het = heterogeneity(yr)

    _header("MCBS reconciliation, standardization, disconfirmation")
    rec = pd.concat([mcbs_reconciliation(fr, "pooled_2016_2024"),
                     mcbs_reconciliation(Frame(pool[pool.year.eq(2023)].reset_index(drop=True), 1.0,
                                               "defl_med", "VARSTR", "VARPSU"), "2023_only")],
                    ignore_index=True)
    std = standardized(fr, "pooled_2016_2024")
    dis = disconfirmation(fr, "pooled_2016_2024")

    cells.to_csv(DERIVED / "cells.csv", index=False)
    rt_all.to_csv(DERIVED / "ratios.csv", index=False)
    tp.to_csv(DERIVED / "two_part.csv", index=False)
    yr.to_csv(DERIVED / "by_year.csv", index=False)
    het.to_csv(DERIVED / "year_heterogeneity.csv", index=False)
    rec.to_csv(DERIVED / "mcbs_reconciliation.csv", index=False)
    std.to_csv(DERIVED / "standardized.csv", index=False)
    dis.to_csv(DERIVED / "disconfirmation.csv", index=False)
    with open(CACHE / "cell_ests.pkl", "wb") as fh:
        pickle.dump({"pooled_design": fr.design, "pooled": store, "sample_designs": sample_designs,
                     "year_designs": yr_designs, "by_year": yr_store}, fh)

    for band in ["65plus", "18_64", "under18", "all_ages"]:
        parts = []
        for spec in ["plain", "winsor_p995", "winsor_p999"]:
            h = headline(rt, band, spec=spec)
            parts.append(f"{spec} {h.ratio:.3f} ({h.se:.3f})")
        t = tp[(tp.scheme == "age_domain") & (tp.band == band) & (tp.nativity == "both")
               & (tp.measure == "public") & (tp.component == "two_part_lognormal")].iloc[0]
        _ok(f"{band}: " + "; ".join(parts) + f"; two-part log-normal {t.ratio:.3f} ({t.se:.3f})")
    audit["headline"] = {band: {spec: {"ratio": float(headline(rt, band, spec=spec).ratio),
                                       "se": float(headline(rt, band, spec=spec).se)}
                                for spec in ["plain", "winsor_p995", "winsor_p999"]}
                         for band in ["65plus", "18_64", "under18", "all_ages"]}
    (DERIVED / "ratios_audit.json").write_text(json.dumps(audit, indent=2, default=float) + "\n")
    _ok("derived/*.csv and ratios_audit.json written")


if __name__ == "__main__":
    main()
