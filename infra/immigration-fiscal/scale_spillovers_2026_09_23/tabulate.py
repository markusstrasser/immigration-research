"""ACS 2024 one-year PUMS: earnings, employment and schooling of the Mexican-origin group and of
everyone else, by 2022 PUMA.

Group person: Hispanic origin Mexican (HISP=02) or born in Mexico (POBP=303), the housing and
congestion lanes' rule. Labels: "mexborn" (group, born in Mexico), "group_other" (group, born
elsewhere, nearly all in the US) and "other" (everyone else).

Workers are employed persons (ESR 1, 2, 4, 5). Earnings are PERNP (wages and self-employment)
times ADJINC, for every person with earnings. Years of schooling map SCHL to years (no schooling,
nursery and kindergarten 0; grades 1-11 to 1-11; 12th grade without diploma 11.5; diploma or GED
12; some college under a year 12.5; a year or more without degree 13.5; associate 14; bachelor 16;
master 18; professional 19; doctorate 20). College years are max(0, years - 12), high-school
years min(years, 12). Full-time workers aged 30-65 (usual hours WKHP >= 35), with and without a
bachelor's degree, are the counts Rosenthal and Strange (2008) put in their distance rings.

Outputs (derived/):
  pums_puma_cells.csv   PUMA x label cells, weighted sums of every item (input to arms.py)
  pums_national.csv     national totals and ratios by label, with 80-replicate SEs
  pums_gate.csv         PUMS totals against published ACS 2024 tables (B01003, B23025, B15003, B20003)
  pums_checks.json      person counts and the gate verdict
Run from the repository root (the gate needs the Census key; it is never printed):
  set -a; . infra/immigration-fiscal/acquire/config.local.env; set +a
  OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/scale_spillovers_2026_09_23/tabulate.py
"""
from __future__ import annotations

import io
import json
import os
import pathlib
import urllib.request
import zipfile

import numpy as np
import pandas as pd

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[2]
PUMS = ROOT / "sources/immigration-fiscal/data/external/acs_pums_2024_1yr"
CACHE = HERE / "_cache"
DERIVED = HERE / "derived"
PREPS = [f"PWGTP{i}" for i in range(1, 81)]
CHUNK = 150_000
MEXICO = 303
GATE_TOLERANCE = 0.02
YEARS = {1: 0, 2: 0, 3: 0, 4: 1, 5: 2, 6: 3, 7: 4, 8: 5, 9: 6, 10: 7, 11: 8, 12: 9, 13: 10,
         14: 11, 15: 11.5, 16: 12, 17: 12, 18: 12.5, 19: 13.5, 20: 14, 21: 16, 22: 18, 23: 19, 24: 20}
EDUC = {"lths": (1, 15), "hs": (16, 17), "sc": (18, 20), "ba": (21, 21), "grad": (22, 24)}
LABELS = ("mexborn", "group_other", "other")


def read_zip(usecols):
    with zipfile.ZipFile(PUMS / "csv_pus.zip") as z:
        for member in ("psam_pusa.csv", "psam_pusb.csv"):
            with z.open(member) as fh:
                yield from pd.read_csv(io.TextIOWrapper(fh), usecols=usecols, chunksize=CHUNK,
                                       dtype={"STATE": str, "PUMA": str})


def replicate_se(full, reps):
    return np.sqrt(4 / 80 * ((reps - full[..., None]) ** 2).sum(axis=-1))


def person_items(chunk):
    """Per-person quantities; every column is additive over persons."""
    schl = chunk["SCHL"].fillna(0).astype(int).to_numpy()
    yrs = pd.Series(schl).map(YEARS).fillna(0).to_numpy(float)
    age = chunk["AGEP"].to_numpy()
    worker = chunk["ESR"].isin([1, 2, 4, 5]).to_numpy()
    adj = chunk["ADJINC"].to_numpy(float) / 1e6
    earn = chunk["PERNP"].fillna(0).to_numpy(float) * adj
    wage = chunk["WAGP"].fillna(0).to_numpy(float) * adj
    adult = age >= 25
    fulltime = worker & (chunk["WKHP"].fillna(0).to_numpy() >= 35) & (age >= 30) & (age <= 65)
    items = {
        "persons": np.ones(len(chunk)),
        "adults25": adult.astype(float),
        "adults25_yrs": adult * yrs,
        "adults25_ba": (adult & (schl >= 21)).astype(float),
        "workers": worker.astype(float),
        "workers_yrs": worker * yrs,
        "workers_collyrs": worker * np.maximum(yrs - 12, 0),
        "workers_hsyrs": worker * np.minimum(yrs, 12),
        "earnings": earn,
        "wages": wage,
        "earners": (earn != 0).astype(float),
        "ft3065_lc": (fulltime & (schl < 21)).astype(float),
        "ft3065_ba": (fulltime & (schl >= 21)).astype(float),
    }
    for name, (lo, hi) in EDUC.items():
        in_cell = (schl >= lo) & (schl <= hi)
        if name == "lths":
            in_cell = in_cell | (schl == 0)
        items[f"workers_{name}"] = (worker & in_cell).astype(float)
        items[f"earnings_{name}"] = earn * in_cell
    return pd.DataFrame(items)


def census_table(table, var_list):
    key = os.environ.get("CENSUS_API_KEY", "")
    if not key:
        raise SystemExit("[BLOCKED] CENSUS_API_KEY not set; source acquire/config.local.env")
    url = (f"https://api.census.gov/data/2024/acs/acs1?get={','.join(var_list)}&for=us:1&key={key}")
    cache = CACHE / f"acs2024_{table.lower()}_us.json"
    if not cache.exists():
        with urllib.request.urlopen(url, timeout=120) as r:
            cache.write_bytes(r.read())
    data = json.loads(cache.read_text())
    return dict(zip(data[0], data[1]))


def main():
    DERIVED.mkdir(exist_ok=True)
    cols = ["STATE", "PUMA", "PWGTP", "HISP", "POBP", "AGEP", "SCHL", "ESR", "PERNP", "WAGP",
            "WKHP", "ADJINC"] + PREPS
    national, cells, names = {}, [], None
    for chunk in read_zip(cols):
        grp = (chunk["HISP"].eq(2) | chunk["POBP"].eq(MEXICO)).to_numpy()
        mex = chunk["POBP"].eq(MEXICO).to_numpy()
        items = person_items(chunk)
        names = names or list(items.columns)
        weights = chunk[["PWGTP"] + PREPS].to_numpy(float)
        masks = {"mexborn": grp & mex, "group_other": grp & ~mex, "other": ~grp}
        for label, mask in masks.items():
            national[label] = national.get(label, 0) + items[mask].to_numpy().T @ weights[mask]
            cell = items[mask].mul(chunk["PWGTP"].to_numpy(float)[mask], axis=0)
            cell["STATE"], cell["PUMA"] = chunk["STATE"].to_numpy()[mask], chunk["PUMA"].to_numpy()[mask]
            cell["label"] = label
            cells.append(cell.groupby(["STATE", "PUMA", "label"]).sum())
    national["group"] = national["mexborn"] + national["group_other"]
    national["all"] = national["group"] + national["other"]
    idx = {n: i for i, n in enumerate(names)}
    rows = []
    ratios = {
        "workers_per_person": ("workers", "persons"),
        "earnings_per_person": ("earnings", "persons"),
        "earnings_per_worker": ("earnings", "workers"),
        "ba_plus_share_of_workers": (("workers_ba", "workers_grad"), "workers"),
        "some_college_plus_share_of_workers": (("workers_sc", "workers_ba", "workers_grad"), "workers"),
        "hs_or_less_share_of_workers": (("workers_lths", "workers_hs"), "workers"),
        "mean_years_workers": ("workers_yrs", "workers"),
        "college_years_per_worker": ("workers_collyrs", "workers"),
        "hs_years_per_worker": ("workers_hsyrs", "workers"),
        "mean_years_adults25": ("adults25_yrs", "adults25"),
        "ba_plus_share_adults25": ("adults25_ba", "adults25"),
        "hs_or_less_share_of_earnings": (("earnings_lths", "earnings_hs"), "earnings"),
    }
    for label, tot in national.items():
        se = replicate_se(tot[:, 0], tot[:, 1:])
        for i, item in enumerate(names):
            rows.append({"label": label, "item": item, "estimate": tot[i, 0], "se": se[i]})
        for name, (num, den) in ratios.items():
            num = (num,) if isinstance(num, str) else num
            r = sum(tot[idx[n]] for n in num) / tot[idx[den]]
            rows.append({"label": label, "item": name, "estimate": r[0],
                         "se": float(replicate_se(np.array(r[0]), r[1:]))})
    for i, item in enumerate(names):
        r = national["group"][i] / national["all"][i]
        rows.append({"label": "group_share", "item": item, "estimate": r[0],
                     "se": float(replicate_se(np.array(r[0]), r[1:]))})
    table = pd.DataFrame(rows)
    table.to_csv(DERIVED / "pums_national.csv", index=False)
    puma = pd.concat(cells).groupby(level=[0, 1, 2]).sum().reset_index()
    puma.to_csv(DERIVED / "pums_puma_cells.csv", index=False)

    # Gate against published national tables.
    est = table[table.label == "all"].set_index("item")["estimate"]
    b01003 = census_table("B01003", ["B01003_001E"])
    b23025 = census_table("B23025", ["B23025_004E", "B23025_006E"])
    b15003 = census_table("B15003", ["B15003_001E", "B15003_022E", "B15003_023E", "B15003_024E",
                                     "B15003_025E"])
    b20003 = census_table("B20003", ["B20003_001E"])
    gate = [
        ("total population", "B01003_001E", est["persons"], float(b01003["B01003_001E"])),
        ("employed, civilian plus armed forces", "B23025_004E+006E", est["workers"],
         float(b23025["B23025_004E"]) + float(b23025["B23025_006E"])),
        ("adults 25+", "B15003_001E", est["adults25"], float(b15003["B15003_001E"])),
        ("adults 25+ with a BA or more", "B15003_022E..025E", est["adults25_ba"],
         sum(float(b15003[f"B15003_0{k}E"]) for k in (22, 23, 24, 25))),
        ("aggregate earnings, population 16+ with earnings ($)", "B20003_001E", est["earnings"],
         float(b20003["B20003_001E"])),
    ]
    gate = pd.DataFrame([{"item": n, "table_cell": c, "pums": p, "published": q,
                          "difference": p / q - 1} for n, c, p, q in gate])
    gate.to_csv(DERIVED / "pums_gate.csv", index=False)
    checks = {
        "group_persons_acs": float(table[(table.label == "group") & (table.item == "persons")].estimate.iloc[0]),
        "mexborn_persons_acs": float(table[(table.label == "mexborn") & (table.item == "persons")].estimate.iloc[0]),
        "all_persons_acs": float(est["persons"]),
        "gate_tolerance": GATE_TOLERANCE,
        "gate_max_abs_difference": float(gate["difference"].abs().max()),
        "gate_passed": bool(gate["difference"].abs().max() <= GATE_TOLERANCE),
    }
    (DERIVED / "pums_checks.json").write_text(json.dumps(checks, indent=2))
    pd.set_option("display.width", 200)
    print(gate.to_string(index=False))
    print(json.dumps(checks, indent=1))
    if not checks["gate_passed"]:
        raise SystemExit("[GATE FAILED] PUMS totals differ from published ACS tables by more than 2%")


if __name__ == "__main__":
    main()
