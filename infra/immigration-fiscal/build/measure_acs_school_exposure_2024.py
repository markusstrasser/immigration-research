#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = ["numpy>=2", "pandas>=2"]
# ///
"""Measure public K–12 enrollment exposure with symmetric household allocation.

Native-First: two streamed pandas reads of the existing ACS ZIP; 80 official SDR
weights. No new acquisition, fabricated enrollment, or canonical warehouse edit.
School costs require a separate explicitly average/marginal cost assumption.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd

W = ["PWGTP"] + [f"PWGTP{i}" for i in range(1, 81)]


def chunks(path, columns):
    with zipfile.ZipFile(path) as z:
        names = [n for n in z.namelist() if n.lower().endswith(".csv") and "psam_pus" in n.lower()]
        if len(names) != 2:
            raise ValueError("Expected the two national ACS person CSV members")
        for name in names:
            yield from pd.read_csv(z.open(name), usecols=columns, dtype={"SERIALNO": "str"}, chunksize=100000)


def summarize(est):
    se = float(np.sqrt(4/80 * np.square(est[1:] - est[0]).sum()))
    return {"estimate": float(est[0]), "se_sampling": se,
            "ci95_low": float(est[0] - 1.96 * se), "ci95_high": float(est[0] + 1.96 * se)}


def run(args):
    fields = ["SERIALNO", "AGEP", "RELSHIPP", "SCH", "SCHG"]
    parts, n_raw = [], 0
    for c in chunks(args.acs_zip, fields):
        n_raw += len(c)
        c = c.loc[c.RELSHIPP.lt(37)].copy()
        if c.loc[c.AGEP.between(5, 17), ["SCH", "SCHG"]].SCH.isna().any():
            raise ValueError("Missing school attendance for a school-age child")
        c["adult"] = c.AGEP.ge(18).astype(int)
        c["pupil"] = (c.AGEP.between(5, 17) & c.SCH.eq(2) & c.SCHG.between(2, 14)).astype(int)
        c["child"] = c.AGEP.between(5, 17).astype(int)
        c["member"] = 1
        parts.append(c.groupby("SERIALNO")[["adult", "pupil", "child", "member"]].sum())
    households = pd.concat(parts).groupby(level=0).sum()
    if n_raw != 3422888:
        raise ValueError("ACS2024 raw row anchor failed")
    num, den, n = {}, {}, {}
    for c in chunks(args.acs_zip, ["SERIALNO", "AGEP", "RELSHIPP", "NATIVITY", "POBP", "ESR", *W]):
        c = c.loc[c.RELSHIPP.lt(37) & c.AGEP.between(25, 64) & ~c.ESR.isin([4, 5])].copy()
        h = households.reindex(c.SERIALNO)
        if h.isna().any().any() or h.adult.le(0).any():
            raise ValueError("Missing or empty household recipient denominator")
        weights = c[W].to_numpy(dtype=float)
        masks = {"all_native": c.NATIVITY.eq(1).to_numpy(),
                 "mexico_born": (c.NATIVITY.eq(2) & c.POBP.eq(303)).to_numpy(),
                 "all_foreign_born": c.NATIVITY.eq(2).to_numpy()}
        for group, mask in masks.items():
            den[group] = den.get(group, np.zeros(81)) + weights[mask].sum(axis=0)
            n[group] = n.get(group, 0) + int(mask.sum())
            for allocation, divisor in [("equal_all_members", h.member), ("equal_adults_18plus", h.adult)]:
                for metric in ["pupil", "child"]:
                    value = (h[metric] / divisor).to_numpy()
                    key = (group, allocation, metric)
                    num[key] = num.get(key, np.zeros(81)) + value[mask] @ weights[mask]
    rows, estimates = [], {}
    for key, numerator in num.items():
        group, allocation, metric = key
        if (den[group] <= 0).any():
            raise ValueError("Nonpositive survey domain denominator")
        est = numerator / den[group]
        estimates["|".join(key)] = est.tolist()
        rows.append({"group": group, "allocation": allocation, "metric": metric,
                     "n": n[group], "weighted_adults": float(den[group][0]), **summarize(est)})
    contrasts = []
    for allocation in ["equal_all_members", "equal_adults_18plus"]:
        for metric in ["pupil", "child"]:
            a = np.array(estimates[f"all_native|{allocation}|{metric}"])
            b = np.array(estimates[f"mexico_born|{allocation}|{metric}"])
            contrasts.append({"allocation": allocation, "metric": metric,
                              "contrast": "all_native_minus_mexico_born", **summarize(a-b)})
    args.output.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(rows).to_csv(args.output / "school_exposure.csv", index=False)
    pd.DataFrame(contrasts).to_csv(args.output / "school_exposure_contrasts.csv", index=False)
    (args.output / "school_exposure_replicates.json").write_text(json.dumps(estimates) + "\n")
    h = hashlib.sha256()
    with args.acs_zip.open("rb") as f:
        for block in iter(lambda: f.read(1024*1024), b""):
            h.update(block)
    meta = {"source": str(args.acs_zip), "sha256": h.hexdigest(), "raw_rows": n_raw,
            "reference_year": 2024, "unit": "Allocated enrolled children per civilian private-household adult age25–64",
            "pupil": "Age5–17; SCH=2 public attendance in last3months; SCHG2–14 kindergarten–grade12",
            "allocation": "Shares split among all household members or all adults18+, regardless of birthplace; includes native children",
            "child_only_units": int(households.adult.eq(0).sum()),
            "child_only_enrolled_children_retained_outside_adult_account": int(households.loc[households.adult.eq(0), "pupil"].sum()),
            "limits": "Not parent-specific, student-years, marginal expenditure, all K–12 ages, or a causal migrant impact. Group quarters excluded. Census FY2024 current spending17619USD/pupil is a separate average-cost scenario, not actual spending on these children.",
            "average_cost_source": "https://www.census.gov/newsroom/press-releases/2026/school-system-finances.html"}
    (args.output / "manifest.json").write_text(json.dumps(meta, indent=2) + "\n")
    print(pd.DataFrame(rows).query("metric=='pupil'").to_string(index=False))


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--acs-zip", required=True, type=Path)
    p.add_argument("--output", required=True, type=Path)
    run(p.parse_args())
