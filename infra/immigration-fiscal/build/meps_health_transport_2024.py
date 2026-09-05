"""Transparent 2024 MEPS donor means and design-based covariance for CPS scenarios.

Native-First: parse the agency's fixed-width SAS layout and use NumPy linear
algebra for the documented with-replacement stratified-PSU Taylor estimator.
Birthplace is US/not-US, never a measured Mexico-specific medical cost.
"""
from __future__ import annotations

import zipfile
from pathlib import Path

import numpy as np
import pandas as pd

from public_mvp_io import parse_meps_sas_fields

PUBLIC_PAYERS = ["TOTMCR24", "TOTMCD24", "TOTVA24", "TOTTRI24", "TOTOFD24", "TOTSTL24"]
FIELDS = ["AGE24X", "BORNUSA", "INSURC24", "PERWT24F", "VARSTR", "VARPSU", *PUBLIC_PAYERS]


def age_band(age):
    return np.digitize(age, [18, 35, 50, 65])


def cps_insurance_category(cps: pd.DataFrame) -> np.ndarray:
    # MEPS INSURC24 puts TRICARE/CHAMPVA with private insurance. CPS PRIV
    # alone excludes these military programs; annual MIL/CHAMPVA must be joined.
    private_equivalent = cps.PRIV.eq(1) | cps.MIL.eq(1) | cps.CHAMPVA.eq(1)
    return np.where(cps.A_AGE.ge(65), 0,
                    np.where(private_equivalent, 1, np.where(cps.PUB.eq(1), 2, 3)))


def read_meps(raw_zip: Path, sas: Path):
    layout = parse_meps_sas_fields(sas)
    if not set(FIELDS).issubset(layout):
        raise ValueError("Required MEPS2024 field absent")
    with zipfile.ZipFile(raw_zip) as z:
        names = [n for n in z.namelist() if n.lower().endswith(".dat")]
        if len(names) != 1:
            raise ValueError("Expected exactly one MEPS ASCII member")
        rows = []
        for line in z.open(names[0]):
            text = line.decode("ascii")
            rows.append({k: float(text[layout[k][0]:sum(layout[k])]) for k in FIELDS})
    d = pd.DataFrame(rows)
    if len(d) != 19140 or d.PERWT24F.gt(0).sum() != 18683:
        raise ValueError("MEPS raw/weighted-record counts fail official codebook anchors")
    anchors = {"all": (np.ones(len(d), bool), 339797630),
               "born_us": (d.BORNUSA.eq(1), 285498519),
               "born_elsewhere": (d.BORNUSA.eq(2), 52835316)}
    checked = {}
    for label, (mask, expected) in anchors.items():
        value = float(d.loc[mask, "PERWT24F"].sum())
        if abs(value - expected) > 1:
            raise ValueError(f"MEPS published population anchor failed: {label} {value} vs {expected}")
        checked[label] = value
    if (d[PUBLIC_PAYERS] < 0).any().any():
        raise ValueError("Missing/reserved public payer value; do not replace with zero")
    d["public_paid"] = d[PUBLIC_PAYERS].sum(axis=1)
    d["age_band"] = age_band(d.AGE24X)
    d["insurance"] = np.where(d.AGE24X.ge(65), 0, d.INSURC24)
    d["born"] = d.BORNUSA
    return d, checked


def donor_model(d: pd.DataFrame, cps: pd.DataFrame, insured: bool):
    keys = ["age_band", "born"] + (["insurance"] if insured else [])
    valid = d.PERWT24F.gt(0) & d.AGE24X.ge(0) & d.BORNUSA.isin([1, 2])
    sample = d.loc[valid]
    cells = sample.groupby(keys, sort=True).agg(n=("public_paid", "size"), population=("PERWT24F", "sum"))
    cells["mean_public_paid"] = sample.assign(wx=sample.public_paid * sample.PERWT24F).groupby(keys).wx.sum() / cells.population
    # Domain influences retain zero contributions from every other observed PSU.
    influence = np.zeros((len(d), len(cells)))
    for j, (key, row) in enumerate(cells.iterrows()):
        mask = valid.to_numpy().copy()
        for col, value in zip(keys, key):
            mask &= d[col].eq(value).to_numpy()
        influence[mask, j] = d.loc[mask, "PERWT24F"] * (d.loc[mask, "public_paid"] - row.mean_public_paid) / row.population
    design = d.loc[d.PERWT24F.gt(0), ["VARSTR", "VARPSU"]].drop_duplicates()
    linear = pd.DataFrame(influence)
    linear["stratum"], linear["psu"] = d.VARSTR, d.VARPSU
    psus = linear.groupby(["stratum", "psu"]).sum().reindex(pd.MultiIndex.from_frame(design)).fillna(0)
    cov = np.zeros((len(cells), len(cells)))
    for _, h in psus.groupby(level=0):
        if len(h) < 2:
            raise ValueError("Lonely MEPS PSU; no silent variance fallback")
        centered = h.to_numpy() - h.to_numpy().mean(axis=0)
        cov += len(h) / (len(h) - 1) * centered.T @ centered
    cells["se_sampling"] = np.sqrt(np.diag(cov))
    target = pd.DataFrame({"age_band": age_band(cps.A_AGE),
                           "born": np.where(cps.PENATVTY.eq(57), 1, 2)})
    if insured:
        target["insurance"] = cps_insurance_category(cps)
    codes = cells.index.get_indexer(pd.MultiIndex.from_frame(target[keys]))
    if (codes < 0).any():
        raise ValueError("CPS target has unsupported health donor cell")
    return cells.reset_index(), codes, cov
