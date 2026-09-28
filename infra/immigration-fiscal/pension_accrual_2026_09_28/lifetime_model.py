"""An OASDI lifetime model for SSA's hypothetical scaled workers, used for ratios.

Per worker (birth year b, family type, career level, first year of covered work):
  * earnings: Note 2025.3 Table 6 preliminary scaled factors x the level's adjustment x the AWI of each year
    (Table 7 through 2061, TR 2025 intermediate; the 2060-61 growth after), ages entry-64;
  * taxes: the combined OASDI rate (TR 2025 Table V.C6; 12.4% from 1990, the 2011-12 holiday counted at 12.4%
    as Note 2025.7 footnote 1 counts the General Fund's substitute) up to the contribution base (Table V.C1,
    wage-indexed after 2034);
  * the retired-worker benefit from the benefit formula: AIME over the highest 35 wage-indexed years (indexed to
    the AWI of the year the worker turns 60), bend points 180 and 1,085 x AWI(b+60) / AWI(1977) (TR 2025 figure
    V.C1's $1,226 and $7,391 for 2025), 90/32/15%, no benefit without 10 years (40 quarters), COLAs from 62
    (Table V.C1, 2.4% after 2034), claimed at 65 at Table V.C3's percentage of PIA;
  * one-earner couple: the wife's aged-spouse benefit at 65 while both live, and the widow's benefit after his
    death (his reduced benefit, at least 82.5% of PIA; 91.9% of PIA at 65 if he died before 65);
  * NVSS 2024 period life tables by sex (general population, or Hispanic for the group), improved at the TR
    2025 intermediate rates of decline (0.68% a year at 65 and over, 0.74% below);
  * present values at 2024 using the trust funds' effective nominal rates (Note 2025.7 Table B, 4.8% from 2049),
    the rates on newly issued trust fund securities (TR 2025 Table V.B2, 4.7% from 2045), the AWI's growth, or a
    constant real rate on top of COLA inflation.

Accruals by age, in PVs at 2024 for a worker alive at entry, four attributions of the same lifetime benefits:
  EAN   entry-age normal: the lifetime money's-worth ratio x each year's tax (the 09-18 lane's construction);
  PUC   projected unit credit: lifetime benefits pro rata to each year's wage-indexed earnings;
  ABO   benefits earned to date: the PIA on the record so far (top 35 years to date / 420), year on year;
  MARG  marginal: lifetime benefits less those without that year's earnings (does not add up to the total).

Left out: disability, child and young-survivor benefits, the family maximum and mortality by earnings level.
The level therefore falls short of Note 2025.7's ratios (the lane reports the gap) and the lane uses the model
only for ratios to its own trust-fund-rate, full-career, entry-age result.
"""
from __future__ import annotations

from functools import lru_cache

import numpy as np
import pandas as pd

import sources as S

Y0, Y1 = 1900, 2200
LIFE = S.FISCAL / "lifetime_longevity_sstiming_2026_09_18" / "_cache"
TABLES = {("general", "male"): S.CACHE / "lt2024_Table02.xlsx", ("general", "female"): S.CACHE / "lt2024_Table03.xlsx",
          ("hispanic", "male"): LIFE / "lt2024_Table05.xlsx", ("hispanic", "female"): LIFE / "lt2024_Table06.xlsx"}
LEVEL_ADJ = {"very_low": 0.305, "low": 0.549, "medium": 1.221, "high": 1.953}   # Note 2025.3 Table 6
# TR 2025 Table V.C3: benefit at 65 as a percentage of PIA, and the normal retirement age in months, by birth year
AT65_PCT = {**{b: 100.0 for b in range(1900, 1938)}, 1938: 98 + 8 / 9, 1939: 97 + 7 / 9, 1940: 96 + 2 / 3, 1941: 95 + 5 / 9,
            1942: 94 + 4 / 9, **{b: 93 + 1 / 3 for b in range(1943, 1955)}, 1955: 92 + 2 / 9, 1956: 91 + 1 / 9, 1957: 90.0,
            1958: 88 + 8 / 9, 1959: 87 + 7 / 9}
NRA_MONTHS = {**{b: 780 for b in range(1900, 1938)}, 1938: 782, 1939: 784, 1940: 786, 1941: 788, 1942: 790,
              **{b: 792 for b in range(1943, 1955)}, 1955: 794, 1956: 796, 1957: 798, 1958: 800, 1959: 802}
FAMILY_SEXES = {"single_man": ("male",), "single_woman": ("female",), "one_earner_couple": ("male",),
                "two_earner_couple": ("male", "female")}
METHODS = ("EAN", "PUC", "ABO", "MARG")


def at65_share(b: int) -> float:
    return AT65_PCT.get(b, 86 + 2 / 3) / 100


def spouse_at65_share(b: int) -> float:
    """50% of PIA less 25/36 of 1% a month for up to 36 months before NRA, 5/12 of 1% beyond
    [SOURCE: 42 U.S.C. 402(q)(1)]."""
    early = max(NRA_MONTHS.get(b, 804) - 780, 0)
    return 0.5 * (1 - (25 / 36) / 100 * min(early, 36) - (5 / 12) / 100 * max(early - 36, 0))


def widow_early_share(b: int) -> float:
    """A widow(er) claiming at 65 on a worker who died before claiming: 28.5% reduction spread over the months
    from 60 to the survivor NRA [SOURCE: 20 CFR 404.338]; survivor NRA taken as the worker NRA."""
    nra = NRA_MONTHS.get(b, 804)
    return 1 - 0.285 * max(nra - 780, 0) / (nra - 720)


class Economy:
    """Year-indexed series as arrays over 1900-2200 (index = year - 1900)."""

    def __init__(self):
        years = np.arange(Y0, Y1 + 1)
        c1 = S.program_parameters_v_c1().set_index("year")
        awi = S.awi_path()
        self.awi_growth_after_2061 = float(awi[2061] / awi[2060])
        a = pd.Series(np.nan, index=years)
        a.loc[awi.index] = awi.values
        for y in range(2062, Y1 + 1):
            a[y] = a[y - 1] * self.awi_growth_after_2061
        cola = pd.Series(np.nan, index=years)
        cola.loc[c1.index] = c1.cola.values
        self.cpi_ultimate = S.value("tr_cpi_ultimate")
        cola.loc[2035:] = self.cpi_ultimate
        base = pd.Series(np.nan, index=years)
        base.loc[c1.index] = c1.base.values
        for y in range(2035, Y1 + 1):
            base[y] = base[2034] * a[y - 2] / a[2032]
        tax = pd.Series(np.nan, index=years)
        rates = S.oasdi_tax_rates_v_c6()
        tax.loc[rates.index] = rates.values
        tax.loc[1990:] = 0.124
        ir = S.interest_rates().set_index("year")
        nom = pd.Series(np.nan, index=years)
        nom.loc[ir.index] = ir.nominal.values
        nom.loc[2049:] = ir.nominal.loc[2049]
        new = pd.Series(np.nan, index=years)
        v_b2 = S.new_issue_rates_v_b2()
        new.loc[v_b2.index] = v_b2.values
        self.awi = a.to_numpy()
        self.cola = cola.to_numpy()
        self.base = base.to_numpy()
        self.tax = tax.to_numpy()
        self.tf_nominal = nom.to_numpy()
        self.new_issue_nominal = new.to_numpy()
        self.awi_1977 = float(a[1977])
        self._disc = {}

    def at(self, arr: np.ndarray, b: int) -> np.ndarray:
        """Series values at ages 0-120 for a cohort born in b."""
        return arr[b - Y0: b - Y0 + 121]

    def discount(self, arm) -> np.ndarray:
        """Cumulative discount factor to 2024 by year (1 in 2024): the trust funds' effective nominal rates
        ('tf'), the nominal rate on newly issued trust fund securities ('new_issue', TR Table V.B2), the AWI's
        own growth ('awi', r = g), or a constant real rate (float) on COLA inflation from 2025, with the
        historical new-issue rates through 2024 as in 'new_issue' (a valuation-rate arm changes the future only;
        before 2026-09-28 it also re-accumulated 1961-2024 taxes at the constant rate). Missing years take the
        nearest rate."""
        if arm in self._disc:
            return self._disc[arm]
        if arm == "tf":
            i = pd.Series(self.tf_nominal)
        elif arm == "new_issue":
            i = pd.Series(self.new_issue_nominal)
        elif arm == "awi":
            i = pd.Series(np.append(self.awi[1:] / self.awi[:-1] - 1, np.nan))
        else:
            cut = 2025 - Y0
            future = (1 + float(arm)) * (1 + pd.Series(self.cola)) - 1
            i = pd.concat([pd.Series(self.new_issue_nominal).iloc[:cut], future.iloc[cut:]]).reset_index(drop=True)
        i = i.ffill().bfill().to_numpy()
        f = np.ones(Y1 - Y0 + 1)
        k0 = 2024 - Y0
        for k in range(k0 + 1, len(f)):
            f[k] = f[k - 1] / (1 + i[k - 1])
        for k in range(k0 - 1, -1, -1):
            f[k] = f[k + 1] * (1 + i[k])
        self._disc[arm] = f
        return f


@lru_cache(maxsize=None)
def qx_table(population: str, sex: str) -> np.ndarray:
    raw = pd.read_excel(TABLES[(population, sex)], header=None)
    q = {}
    for _, r in raw.iterrows():
        label = str(r[0]).strip().replace("–", "-")
        if label.startswith("100 and"):
            q[100] = 1.0
        elif "-" in label and label[0].isdigit():
            q[int(label.split("-")[0])] = float(r[1])
    if sorted(q) != list(range(101)):
        raise SystemExit(f"[BLOCKED] life table {TABLES[(population, sex)].name}")
    out = np.ones(121)
    out[:101] = [q[a] for a in range(101)]
    return out


@lru_cache(maxsize=None)
def _decline() -> tuple[float, float]:
    return S.value("tr_mortality_decline_65plus"), S.value("tr_mortality_decline_total")


@lru_cache(maxsize=None)
def survival(b: int, population: str, sex: str, from_age: int) -> np.ndarray:
    """Probability of being alive at mid-age 0-120 given alive at `from_age`, cohort b: 2024 period rates
    improved by calendar year at the TR's intermediate rates of decline."""
    old, young = _decline()
    ages = np.arange(121)
    q = np.clip(qx_table(population, sex) * (1 - np.where(ages >= 65, old, young)) ** ((b + ages) - 2024), 0, 1)
    q[100:] = 1.0
    start = np.cumprod(np.concatenate([[1.0], 1 - q[:-1]]))      # alive at the start of each age, from 0
    alive = start * (1 - q / 2)
    alive = alive / start[from_age]
    alive[:from_age] = 0.0
    return alive


def pia_formula(aime, b: int, econ: Economy):
    k = econ.awi[b + 60 - Y0] / econ.awi_1977
    bp1, bp2 = 180 * k, 1085 * k
    return 0.9 * np.minimum(aime, bp1) + 0.32 * np.clip(aime - bp1, 0, bp2 - bp1) + 0.15 * np.maximum(aime - bp2, 0)


def index_factors(b: int, to_age: int, econ: Economy) -> np.ndarray:
    """AWI(b + to_age) / AWI(b + a) for ages 21 to `to_age`, 1 after, 0 before 21."""
    out = np.zeros(121)
    awi = econ.at(econ.awi, b)
    out[21:to_age + 1] = awi[to_age] / awi[21:to_age + 1]
    out[to_age + 1:] = 1.0
    return out


def earnings_path(b: int, adj: float, entry: int, prelim: np.ndarray, econ: Economy) -> np.ndarray:
    """Nominal earnings at ages 0-120: preliminary factor (ages 21-64) x adj x AWI at ages max(entry, 21)-64."""
    e = np.zeros(121)
    awi = econ.at(econ.awi, b)
    lo = max(entry, 21)
    e[lo:65] = prelim[lo - 21:44] * adj * awi[lo:65]
    return e


def top35(values: np.ndarray) -> float:
    v = values[values > 0]
    if len(v) > 35:
        v = np.sort(v)[-35:]
    return float(v.sum())


def worker(b: int, adj: float, entry: int, family: str, econ: Economy, prelim: np.ndarray, arm="tf",
           population="general", payable: np.ndarray | None = None, alive_at: int | None = None,
           last_year: int | None = None) -> dict:
    """Expected lifetime taxes and benefits (PVs at 2024, for a worker alive at entry) and the four accrual
    attributions by age. `payable`, if given, is the share of scheduled benefits paid by year (Y0-indexed).
    `alive_at` (an age of at most 65) conditions on the unit being alive at the start of that age: taxes at younger
    ages count as paid, later flows take survival from that age. `last_year` drops benefits paid after that
    calendar year. Both default to the lifetime view from entry; `ben_pv_by_age` holds the benefit PVs by age."""
    if alive_at is not None and not 0 < alive_at <= 65:
        raise ValueError(f"alive_at {alive_at}: the widow terms need the unit alive before 65")
    disc = econ.at(econ.discount(arm), b)
    pay = np.ones(121) if payable is None else econ.at(payable, b)
    cola = econ.at(econ.cola, b)
    base = np.nan_to_num(econ.at(econ.base, b), nan=np.inf)
    rate = np.nan_to_num(econ.at(econ.tax, b))
    grow = np.ones(121)
    for a in range(66, 121):
        grow[a] = grow[a - 1] * (1 + cola[a - 1])
    unit = np.zeros(121)
    unit[65:] = 12 * float(np.prod(1 + cola[62:65])) * grow[65:]     # annual benefit per $1 of monthly PIA at 62
    lo = max(entry, 21)
    since = lo if alive_at is None else alive_at
    ages = np.arange(121)
    window = np.ones(121) if last_year is None else (b + ages <= last_year).astype(float)
    out = dict(pv_tax=0.0, pv_ben=0.0, tax_pv_by_age=np.zeros(121), ben_pv_by_age=np.zeros(121),
               acc={m: np.zeros(121) for m in METHODS})
    for sex in FAMILY_SEXES[family]:
        e = earnings_path(b, adj, entry, prelim, econ)
        tax = rate * np.minimum(e, base)
        s_w = survival(b, population, sex, since)
        s_tax = s_w if alive_at is None else np.where(ages < alive_at, 1.0, s_w)
        ie = e * index_factors(b, 60, econ)
        vested = int((e[:65] > 0).sum()) >= 10
        own = at65_share(b) * unit
        if family == "one_earner_couple":
            s_f = survival(b, population, "female", since)
            ben_unit = (s_w * own + s_w * s_f * spouse_at65_share(b) * unit
                        + np.clip(s_w[65] - s_w, 0, None) * s_f * max(at65_share(b), 0.825) * unit
                        + (1 - s_w[65]) * s_f * widow_early_share(b) * unit)
        else:
            ben_unit = s_w * own
        ben_pv = ben_unit * pay * disc * window
        pv_unit = float(ben_pv[65:].sum())   # PV at 2024 of benefits per $1 of PIA at 62
        pia = float(pia_formula(top35(ie[:65]) / 420, b, econ)) if vested else 0.0
        pv_ben = pia * pv_unit
        tax_pv = s_tax * tax * disc
        out["pv_ben"] += pv_ben
        out["pv_tax"] += float(tax_pv[:65].sum())
        out["tax_pv_by_age"] += tax_pv
        out["ben_pv_by_age"][65:] += pia * ben_pv[65:]
        if not vested:
            continue
        total_ie = ie[:65].sum()
        prev = 0.0
        for a in range(lo, 65):
            now = float(pia_formula(top35(ie[lo:a + 1]) / 420, b, econ))
            out["acc"]["ABO"][a] += (now - prev) * pv_unit
            prev = now
            out["acc"]["PUC"][a] += pv_ben * ie[a] / total_ie
            without = ie[:65].copy()
            without[a] = 0.0
            out["acc"]["MARG"][a] += (pia - float(pia_formula(top35(without) / 420, b, econ))) * pv_unit
    out["mwr"] = out["pv_ben"] / out["pv_tax"] if out["pv_tax"] else np.nan
    out["acc"]["EAN"] = out["mwr"] * out["tax_pv_by_age"] if out["pv_tax"] else np.zeros(121)
    # per $ of tax at each age, in PV terms: the factor applied to a person's 2024 tax at that age
    with np.errstate(invalid="ignore", divide="ignore"):
        out["per_tax"] = {m: np.where(out["tax_pv_by_age"] > 0, out["acc"][m] / out["tax_pv_by_age"], np.nan)
                          for m in METHODS}
    return out


def replacement_at_65(b: int, adj: float, econ: Economy, prelim: np.ndarray) -> float:
    """TR Table V.C7's measure: the first-year benefit at 65 over the average of the highest 35 years of
    earnings indexed to the year before entitlement."""
    e = earnings_path(b, adj, 21, prelim, econ)
    pia62 = float(pia_formula(top35((e * index_factors(b, 60, econ))[:65]) / 420, b, econ))
    cola = econ.at(econ.cola, b)
    benefit = 12 * pia62 * float(np.prod(1 + cola[62:65])) * at65_share(b)
    return benefit / (top35((e * index_factors(b, 64, econ))[:65]) / 35)
