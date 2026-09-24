"""Outside checks for a consumption key: CBO's federal excise distribution and ITEP's Who Pays?.

CBO. The outside-checks lane (external_benchmarks_2026_09_24) ranks CPS households by a proxy of
CBO's income before transfers and taxes over the square root of household size and compares the
account's key with CBO's 2022 excise shares (researcher Table 12). Its functions are reused here
read-only; its frame cache supplies the ranking fields, joined to this lane's arrays by PH_SEQ/PPPOS.

ITEP. Who Pays? 7th edition, U.S. Average table (2024 law at 2023 incomes, non-senior families):
sales and excise taxes as a share of family income in seven groups. Tax dollars by group are the rate
times the group's average income times its share of families; the CPS side ranks non-elderly SPM
units by money income with unit weights.
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
BENCH = HERE.parent / "external_benchmarks_2026_09_24"
ITEP_TXT = HERE / "_cache" / "sources" / "itep" / "ITEP-Who-Pays-7th-edition.txt"
ITEP_GROUPS = ["lowest_20", "second_20", "middle_20", "fourth_20", "next_15", "next_4", "top_1"]
ITEP_FAMILY_SHARE = np.array([.20, .20, .20, .20, .15, .04, .01])
ITEP_EDGES = np.cumsum(ITEP_FAMILY_SHARE)[:-1]
ITEP_ROWS = {"Average Income in Group": "average_income", "Sales & Excise Taxes": "sales_excise",
             "General Sales–Individuals": "general_sales_individuals",
             "Other Sales & Excise–Ind.": "other_sales_excise_individuals",
             "Sales & Excise–Business": "sales_excise_business"}


def bench_modules():
    # Read-only use of another lane's modules: no bytecode caches written into its directory.
    sys.dont_write_bytecode = True
    if str(BENCH) not in sys.path:
        sys.path.insert(0, str(BENCH))
    import frame as f  # noqa: E402  (outside-checks lane, read-only)
    import cbo_arm  # noqa: E402
    return f, cbo_arm


def cbo_groups_for(a: dict) -> tuple[np.ndarray, pd.DataFrame]:
    """CBO income group of every person in this lane's order, and CBO's 2022 shares."""
    f, cbo_arm = bench_modules()
    cols = ["PH_SEQ", "PPPOS", "PTOTVAL", "SSI_VAL", "PAW_VAL", "WSAL_VAL", "CAP_VAL", "MCARE", "pwwgt0"]
    d = pd.read_parquet(f.CACHE / "cps25_frame.parquet", columns=cols)
    w = d.pwwgt0.to_numpy(float)
    medicare_bn = next(l for l in f.model()["spending"]["lines"] if l["id"] == "medicare")["national_bn"]
    per = medicare_bn * 1e9 / w[d.MCARE.eq(1).to_numpy()].sum()
    g, _ = f.cbo_groups(d, f.cbo_income(d, per), w)
    key = pd.Series(g, index=pd.MultiIndex.from_arrays([d.PH_SEQ.to_numpy(), d.PPPOS.to_numpy()]))
    mine = pd.MultiIndex.from_arrays([a["ph_seq"], a["pppos"]])
    mapped = key.reindex(mine)
    if mapped.isna().any():
        raise ValueError("[BLOCKED] persons missing from the outside-checks frame")
    return mapped.to_numpy(), cbo_arm.cbo_shares(2022)


def decompose(k: np.ndarray, a: dict, g: np.ndarray, groups: list[str], rep: bool = True):
    """pi[j] = group j's share of the national key; theta[j] = the union's share inside j."""
    W = a["weights"] if rep else a["weights"][:, :1]
    civ, tgt = a["civilian"], a["target"]
    total = k[civ] @ W[civ]
    pi, theta = {}, {}
    for j in groups:
        m = civ & (g == j)
        gj = k[m] @ W[m]
        tj = k[m & tgt] @ W[m & tgt]
        pi[j] = gj / total
        theta[j] = np.divide(tj, gj, out=np.zeros_like(tj), where=gj != 0)
    return pi, theta


def cbo_federal_share(k: np.ndarray, a: dict, g: np.ndarray, cbo: pd.DataFrame) -> dict:
    """Union share of the $99.964bn federal-excise part at CBO's group shares, with this key's thetas."""
    f, cbo_arm = bench_modules()
    pi, theta = decompose(k, a, g, f.GROUPS)
    target = cbo_arm.cbo_detail(cbo, "excise_taxes", float(pi["negative"][0]))
    s_cbo = sum(target[j] * theta[j] for j in f.GROUPS)
    s_key = sum(pi[j] * theta[j] for j in f.GROUPS)
    return dict(pi=pi, theta=theta, cbo=target, share_at_cbo=s_cbo, share_key=s_key)


def itep_table() -> pd.DataFrame:
    """The U.S. Average rows of Who Pays? (7th ed.), parsed from the pdftotext layout."""
    lines = ITEP_TXT.read_text().splitlines()
    start = next(i for i, l in enumerate(lines) if "U. S. Average" in l and "State and local tax (cont.)" in l)
    out = {}
    for l in lines[start:start + 40]:
        s = l.strip()
        for label, key in ITEP_ROWS.items():
            if s.startswith(label) and key not in out:
                vals = s[len(label):].replace("$", "").replace(",", "").replace("%", "").split()
                if len(vals) != 7:
                    raise ValueError(f"[BLOCKED] ITEP row {label!r} parsed to {vals}")
                out[key] = [float(v) for v in vals]
    if set(out) != set(ITEP_ROWS.values()):
        raise ValueError(f"[BLOCKED] ITEP rows missing: {set(ITEP_ROWS.values()) - set(out)}")
    t = pd.DataFrame(out, index=ITEP_GROUPS)
    for c in t.columns:
        if c != "average_income":
            t[c] = t[c] / 100
    return t


def itep_groups(a: dict) -> tuple[np.ndarray, np.ndarray]:
    """ITEP group of every person's SPM unit (non-elderly units ranked by money income, unit weights)
    and a non-elderly mask; elderly units get the group their income would place them in."""
    head = a["head"]
    u = a["unit"]
    n = int(a["n_units"])
    income = np.zeros(n)
    income[u[head]] = a["spm_totval"][head]
    uw = np.zeros(n)
    uw[u[head]] = a["unit_weight"][head]
    age = np.zeros(n)
    age[u[head]] = a["head_age"][head]
    young = age < 65
    o = np.argsort(income[young], kind="mergesort")
    cum = np.cumsum(uw[young][o]) / uw[young].sum()
    cuts = np.interp(ITEP_EDGES, cum, income[young][o])
    grp_u = np.searchsorted(cuts, income, side="right")
    return grp_u[u], young[u]


def itep_compare(keys: dict, a: dict) -> pd.DataFrame:
    """Distribution of each key across ITEP groups (non-elderly persons) against ITEP's tax dollars."""
    t = itep_table()
    grp, young = itep_groups(a)
    w = a["weights"][:, 0]
    civ, tgt = a["civilian"], a["target"]
    rows = []
    itep_dollars = {c: t[c].to_numpy() * t.average_income.to_numpy() * ITEP_FAMILY_SHARE
                    for c in ["sales_excise", "general_sales_individuals", "other_sales_excise_individuals",
                              "sales_excise_business"]}
    for c, dollars in itep_dollars.items():
        shares = dollars / dollars.sum()
        for j, g in enumerate(ITEP_GROUPS):
            rows.append(dict(source="itep", concept=c, group=g, share=shares[j]))
    # money income per person by ITEP group, for the rate each key implies
    head = a["head"]
    inc_p = a["spm_totval"][head][np.argsort(a["unit"][head])][a["unit"]] / a["size"]
    for name, k in keys.items():
        m = civ & young
        tot = k[m] @ w[m]
        for j, g in enumerate(ITEP_GROUPS):
            mj = m & (grp == j)
            rows.append(dict(source="key", concept=name, group=g, share=(k[mj] @ w[mj]) / tot,
                             union_share_in_group=(k[mj & tgt] @ w[mj & tgt]) / (k[mj] @ w[mj]),
                             key_over_income=(k[mj] @ w[mj]) / (inc_p[mj] @ w[mj])))
    return pd.DataFrame(rows)


def itep_unit_rates(a: dict, concept: str = "sales_excise") -> np.ndarray:
    """ITEP's rate for each SPM unit's money-income group, in unit-index order."""
    t = itep_table()
    grp, _ = itep_groups(a)
    head = a["head"]
    out = np.zeros(int(a["n_units"]))
    out[a["unit"][head]] = t[concept].to_numpy()[grp[head]]
    return out


def itep_keyed_share(a: dict, concept: str = "sales_excise", seniors: bool = True,
                     base: str = "resources") -> np.ndarray:
    """Union share when every unit pays ITEP's rate for its money-income group (161 reps).

    base='resources' applies the rate to the account's own key base (positive SPM resources), so the
    result differs from the raw key's 8.104% only through ITEP's gradient; base='money_income' applies
    it to money income, the closer analogue of ITEP's family income.
    """
    t = itep_table()
    grp, young = itep_groups(a)
    head = a["head"]
    if base == "resources":
        per_person = np.clip(a["spm_resources"], 0, None) / a["size"]
    elif base == "money_income":
        inc_u = a["spm_totval"][head][np.argsort(a["unit"][head])]
        per_person = np.clip(inc_u[a["unit"]], 0, None) / a["size"]
    else:
        raise ValueError(base)
    k = t[concept].to_numpy()[grp] * per_person
    civ, tgt, W = a["civilian"], a["target"], a["weights"]
    m = civ if seniors else civ & young
    return (k[m & tgt] @ W[m & tgt]) / (k[m] @ W[m])
