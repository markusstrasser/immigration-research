"""Consumption-to-income ratios by income position (CE 2024), carried to CPS resource units.

The CE decile table (Table 1110) gives each decile's mean expenditure and income before taxes. The CE
microdata give the shape of the ratio inside each decile (50 rank bins, rescaled so each decile's
aggregate ratio equals the published one). Each CPS SPM unit is ranked by pre-tax money income plus
SNAP (the CE income concept), weighted by units, as CE ranks consumer units. Because the account's
key is SPM resources, the CE ratio over pre-tax income is converted to a ratio over resources with the
CPS's own pre-tax-income-to-resources ratio in the same rank bin.

2024 CE tables carry no income after taxes (BLS stopped publishing TAXSIM estimates), which is why the
ratio is taken over pre-tax income and converted with CPS taxes and transfers.
"""
from __future__ import annotations

import numpy as np
import pandas as pd

import ce_pumd
import ce_tables

DECILE_TABLE = "cu-income-deciles-before-taxes-2024.xlsx"
CONCEPTS = ["consumption", "total", "taxable_broad"]


def published_deciles() -> dict:
    t = ce_tables.parse(DECILE_TABLE)
    c = ce_tables.concepts(t)
    out = {"income": np.array(t["Income before taxes"][1:]), "units_k": np.array(t["Number of consumer units (in thousands)"][1:])}
    for k in CONCEPTS:
        out[k] = np.array(c[k][1:])
    return out


def pumd_ranked() -> pd.DataFrame:
    """CE interviews with a weighted rank of income before taxes inside each quarterly file.

    BLS's INC_RANK does not follow FINCBTXM (rank correlation 0.83 in these files), so the rank is
    recomputed; with it the microdata reproduce Table 1110's decile income means within 2.3%.
    """
    d = ce_pumd.read()
    d = d[d.weight > 0].copy()
    parts = []
    for _, s in d.groupby("file"):
        s = s.sort_values("income", kind="mergesort")
        cum = s.weight.cumsum() / s.weight.sum()
        parts.append(cum - s.weight / (2 * s.weight.sum()))
    d["rank"] = pd.concat(parts).reindex(d.index)
    return d


def rank_bins(rank: np.ndarray, nb: int) -> np.ndarray:
    return np.clip((np.asarray(rank) * nb).astype(int), 0, nb - 1)


def ce_curve(concept: str, nb: int = 50, pumd: pd.DataFrame | None = None, pub: dict | None = None,
             within: bool = True) -> dict:
    """Ratio of the concept to pre-tax income in nb rank bins, each decile matching Table 1110.

    within=False gives the published step function (every bin in a decile gets its decile's ratio).
    Also returns the CE level of the concept per consumer unit by bin (for the level transport).
    """
    pub = pub or published_deciles()
    pumd = pumd_ranked() if pumd is None else pumd
    r_pub = pub[concept] / pub["income"]
    b = rank_bins(pumd["rank"], nb)
    w = pumd.weight.to_numpy()
    C = np.bincount(b, weights=w * pumd[concept].to_numpy(), minlength=nb)
    Y = np.bincount(b, weights=w * pumd.income.to_numpy(), minlength=nb)
    N = np.bincount(b, weights=w, minlength=nb)
    dec = np.arange(nb) * 10 // nb
    ratio = np.empty(nb)
    level = np.empty(nb)
    for k in range(10):
        m = dec == k
        pumd_ratio = C[m].sum() / Y[m].sum()
        pumd_level = C[m].sum() / N[m].sum()
        if within:
            ratio[m] = C[m] / Y[m] * r_pub[k] / pumd_ratio
            level[m] = C[m] / N[m] * pub[concept][k] / pumd_level
        else:
            ratio[m] = r_pub[k]
            level[m] = pub[concept][k]
    # The lowest bin's pre-tax income is near zero, so its ratio is unstable: pool the bottom decile's
    # bins at the decile ratio (the decile holds about 1% of the key).
    bottom = dec == 0
    ratio[bottom] = r_pub[0]
    level[bottom] = pub[concept][0]
    return {"ratio": ratio, "level": level, "nb": nb, "concept": concept, "within": within}


def cps_units(a: dict) -> dict:
    """Unit-level arrays in unit-index order, from the person frame."""
    head = a["head"]
    order = np.argsort(a["unit"][head])
    pick = lambda x: np.asarray(x)[head][order]
    y = pick(a["spm_totval"] + a["snap"])
    uw = pick(a["unit_weight"])
    res = pick(a["spm_resources"]).clip(min=0)
    o = np.argsort(y, kind="mergesort")
    cum = np.empty(len(y))
    cum[o] = np.cumsum(uw[o]) / uw.sum()
    rank = cum - uw / (2 * uw.sum())
    return {"income": y, "weight": uw, "resources": res, "rank": rank, "size": pick(a["size"]),
            "head_age": pick(a["head_age"])}


def unit_factor(a: dict, curve: dict, transport: str = "ratio", cap_bottom: float | None = None) -> np.ndarray:
    """Consumption per resource dollar for every unit (unit-index order).

    ratio transport: CE (concept / pre-tax income) at the unit's rank times the CPS bin's
    pre-tax income over resources. level transport: CE concept per unit at the rank over CPS
    resources per unit in the bin.
    """
    u = cps_units(a)
    nb = curve["nb"]
    b = rank_bins(u["rank"], nb)
    Y = np.bincount(b, weights=u["weight"] * u["income"], minlength=nb)
    R = np.bincount(b, weights=u["weight"] * u["resources"], minlength=nb)
    N = np.bincount(b, weights=u["weight"], minlength=nb)
    dec = np.arange(nb) * 10 // nb
    if transport == "ratio":
        # Pool the bottom decile's bins for the CPS conversion too (pre-tax income near zero).
        Yb, Rb = Y.copy(), R.copy()
        Yb[dec == 0], Rb[dec == 0] = Y[dec == 0].sum(), R[dec == 0].sum()
        per_bin = curve["ratio"] * Yb / Rb
    elif transport == "level":
        Nb, Rb = N.copy(), R.copy()
        Nb[dec == 0], Rb[dec == 0] = N[dec == 0].sum(), R[dec == 0].sum()
        per_bin = curve["level"] / (Rb / Nb)
    else:
        raise ValueError(transport)
    if cap_bottom is not None:
        per_bin = np.where(dec == 0, np.minimum(per_bin, cap_bottom), per_bin)
    return per_bin[b]


def unit_factor_by_size(a: dict, concept: str, pumd: pd.DataFrame, pub: dict, nb: int = 20) -> np.ndarray:
    """Rank x consumer-unit-size ratios from the CE microdata, each rank bin rescaled to Table 1110."""
    r_pub = pub[concept] / pub["income"]
    b = rank_bins(pumd["rank"], nb)
    s = np.clip(pumd.fam_size.to_numpy(), 1, 5).astype(int) - 1
    w = pumd.weight.to_numpy()
    C = np.zeros((nb, 5)); Y = np.zeros((nb, 5))
    np.add.at(C, (b, s), w * pumd[concept].to_numpy())
    np.add.at(Y, (b, s), w * pumd.income.to_numpy())
    dec = np.arange(nb) * 10 // nb
    ratio = C / np.where(Y > 0, Y, np.nan)
    for k in range(10):
        m = dec == k
        ratio[m] *= r_pub[k] / (C[m].sum() / Y[m].sum())
    # Bottom decile: one ratio per size (incomes near zero); empty cells take the bin's ratio.
    bottom = dec == 0
    ratio[bottom] = (C[bottom].sum(0) / Y[bottom].sum(0)) * r_pub[0] / (C[bottom].sum() / Y[bottom].sum())
    fill = (C.sum(1) / Y.sum(1))[:, None] * np.ones((1, 5))
    ratio = np.where(np.isfinite(ratio) & (ratio > 0), ratio, fill)
    u = cps_units(a)
    ub = rank_bins(u["rank"], nb)
    us = np.clip(u["size"], 1, 5).astype(int) - 1
    Yc = np.zeros((nb, 5)); Rc = np.zeros((nb, 5))
    np.add.at(Yc, (ub, us), u["weight"] * u["income"])
    np.add.at(Rc, (ub, us), u["weight"] * u["resources"])
    Yc[bottom] = Yc[bottom].sum(0); Rc[bottom] = Rc[bottom].sum(0)
    conv = np.where(Rc > 0, Yc / np.where(Rc > 0, Rc, 1), 1.0)
    return (ratio * conv)[ub, us]


AGE_EDGES = [35, 55, 65]  # reference person or unit head: under 35, 35-54, 55-64, 65 and over


def unit_factor_by_size_age(a: dict, concept: str, pumd: pd.DataFrame, pub: dict, nb: int = 20,
                            min_records: int = 20) -> np.ndarray:
    """Rank x size x age-of-head ratios: each rank x size cell's ratio (unit_factor_by_size) times the
    age cell's CE ratio relative to its rank x size cell; cells with fewer than min_records CE
    interviews keep the rank x size ratio. Conversion to resources uses the CPS rank x size x age cell."""
    b = rank_bins(pumd["rank"], nb)
    s = np.clip(pumd.fam_size.to_numpy(), 1, 5).astype(int) - 1
    g = np.searchsorted(AGE_EDGES, pumd.age_ref.to_numpy(), side="right")
    w = pumd.weight.to_numpy()
    C = np.zeros((nb, 5, 4)); Y = np.zeros((nb, 5, 4)); n = np.zeros((nb, 5, 4))
    np.add.at(C, (b, s, g), w * pumd[concept].to_numpy())
    np.add.at(Y, (b, s, g), w * pumd.income.to_numpy())
    np.add.at(n, (b, s, g), 1)
    dec = np.arange(nb) * 10 // nb
    bottom = dec == 0
    # Bottom decile pooled over rank bins, as elsewhere.
    for arr in (C, Y, n):
        arr[bottom] = arr[bottom].sum(0)
    rel = (C / np.where(Y > 0, Y, np.nan)) / (C.sum(2, keepdims=True) / Y.sum(2, keepdims=True))
    rel = np.where((n >= min_records) & np.isfinite(rel) & (rel > 0), rel, 1.0)
    # Keep each rank x size cell's aggregate ratio: renormalize rel to the cell's income weights.
    rel = rel / ((rel * Y).sum(2, keepdims=True) / Y.sum(2, keepdims=True))
    rel = np.where(np.isfinite(rel), rel, 1.0)
    u = cps_units(a)
    ub = rank_bins(u["rank"], nb)
    us = np.clip(u["size"], 1, 5).astype(int) - 1
    ug = np.searchsorted(AGE_EDGES, u["head_age"], side="right")
    Yc = np.zeros((nb, 5, 4)); Rc = np.zeros((nb, 5, 4)); Ys = np.zeros((nb, 5)); Rs = np.zeros((nb, 5))
    np.add.at(Yc, (ub, us, ug), u["weight"] * u["income"])
    np.add.at(Rc, (ub, us, ug), u["weight"] * u["resources"])
    Yc[bottom] = Yc[bottom].sum(0); Rc[bottom] = Rc[bottom].sum(0)
    np.add.at(Ys, (ub, us), u["weight"] * u["income"])
    np.add.at(Rs, (ub, us), u["weight"] * u["resources"])
    Ys[bottom] = Ys[bottom].sum(0); Rs[bottom] = Rs[bottom].sum(0)
    # unit_factor_by_size gives ratio(rank, size) * (Y/R)(rank, size); swap in the age cell's Y/R.
    base = unit_factor_by_size(a, concept, pumd, pub, nb)
    conv_s = np.where(Rs > 0, Ys / np.where(Rs > 0, Rs, 1), 1.0)
    conv_c = np.where(Rc > 0, Yc / np.where(Rc > 0, Rc, 1), conv_s[:, :, None])
    return base / conv_s[ub, us] * conv_c[ub, us, ug] * rel[ub, us, ug]


def ce_check(pumd: pd.DataFrame, concept: str = "consumption", cells=("vig",), reps: int = 200, seed: int = 7) -> pd.DataFrame:
    """Actual over predicted concept for CE groups, prediction = national ratio in the same cell.

    cells: 'vig' (20 income-rank bins), 'size' (consumer-unit size 1..5+), 'age' (reference person
    under 35, 35-54, 55-64, 65+). SE from a consumer-unit cluster bootstrap (NEWID's first seven
    digits identify the consumer unit across its interviews).
    """
    d = pumd.copy()
    d["vig"] = rank_bins(d["rank"], 20)
    d["size"] = np.clip(d.fam_size, 1, 5)
    d["age"] = pd.cut(d.age_ref, [0, 34, 54, 64, 200], labels=False)
    d["cu"] = d.newid.astype(str).str.zfill(8).str[:7]
    groups = {"hispanic": d.hispanic.to_numpy(), "mexican_origin": d.mexican_origin.to_numpy(),
              "mexican_code1": d.horref1.eq(1).to_numpy(), "mexican_american_chicano": d.horref1.isin([2, 3]).to_numpy(),
              "not_hispanic": (~d.hispanic).to_numpy()}
    key = d[list(cells)].astype(int).astype(str).agg("|".join, axis=1).to_numpy()
    codes, inv = np.unique(key, return_inverse=True)

    def stat(wt):
        C = np.bincount(inv, weights=wt * d[concept].to_numpy(), minlength=len(codes))
        Y = np.bincount(inv, weights=wt * d.income.to_numpy(), minlength=len(codes))
        r = np.divide(C, Y, out=np.zeros_like(C), where=Y != 0)
        pred = r[inv] * d.income.to_numpy()
        return {g: (wt[m] * d[concept].to_numpy()[m]).sum() / (wt[m] * pred[m]).sum() for g, m in groups.items()}

    w = d.weight.to_numpy()
    point = stat(w)
    rng = np.random.default_rng(seed)
    cus, cu_inv = np.unique(d.cu.to_numpy(), return_inverse=True)
    draws = {g: [] for g in groups}
    for _ in range(reps):
        k = np.bincount(rng.integers(0, len(cus), len(cus)), minlength=len(cus))
        s = stat(w * k[cu_inv])
        for g in groups:
            draws[g].append(s[g])
    rows = []
    for g, m in groups.items():
        rows.append({"concept": concept, "cells": "x".join(cells), "group": g, "records": int(m.sum()),
                     "actual_over_predicted": point[g], "bootstrap_se": float(np.std(draws[g], ddof=1))})
    return pd.DataFrame(rows)
