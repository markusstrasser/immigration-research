#!/usr/bin/env python3
"""Occupation overlap inside the production term's two skill cells.

The nest's ε is one number for natives versus foreign-born inside a schooling
cell, and the cell has no occupations. This measures how much those groups
already share jobs, on the same CPS file and the same group rules as
builder.branch_composition. It does not estimate ε.

Overlap is the sum of the minima of two earnings-share vectors, equal to one
minus the Duncan dissimilarity. The elasticity sketch is a weighted harmonic
mix of a within-job elasticity and a between-job elasticity,

    1/ε ≈ overlap / ε_within + (1 - overlap) / ε_between

and is labeled as a sketch in every row. It is not the nest's solver.

Run from the repo root:
  OPENBLAS_NUM_THREADS=1 uv run --no-project --with numpy --with pandas \\
    python3 infra/immigration-fiscal/production_nativity_nest_2026_09_22/occupation_overlap.py
"""
from __future__ import annotations

import zipfile
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
ZIP = HERE.parent / "gen_ledger_extension_2026_09_16/_cache/asecpub25csv.zip"
DICT = Path.home() / "research-data/immigration-fiscal/data/external/acs_pums_dict/PUMS_Data_Dictionary_2024.txt"
BRANCHES = HERE / "derived/branch_composition.csv"
OUT = HERE / "derived"

# Census 2018 major-group code ranges, the groups the OCCP labels abbreviate.
# Edges are the last code of each group in the 2018 list.
MAJOR_EDGES = [
    (440, "management"), (960, "business"), (1240, "computer"), (1560, "engineering"),
    (1980, "science"), (2060, "community"), (2180, "legal"), (2555, "education"),
    (2920, "arts"), (3550, "health_practitioners"), (3655, "health_support"),
    (3960, "protective"), (4160, "food"), (4255, "cleaning"), (4655, "personal_care"),
    (4965, "sales"), (5940, "office"), (6130, "farming"), (6950, "construction"),
    (7640, "installation"), (8990, "production"), (9760, "transport"),
]


def occupation_labels(path: Path) -> dict[int, str]:
    """Titles from the OCCP block of the ACS 2024 PUMS dictionary. Same 2018 codes as CPS PEIOOCC."""
    labels, in_block = {}, False
    for line in path.read_text(encoding="latin-1").splitlines():
        if line.startswith("OCCP "):
            in_block = True
            continue
        # The next variable name is an unindented token; the prose under OCCP is not.
        if in_block and line and not line[0].isspace() and line.split()[0].isupper():
            break
        if not in_block:
            continue
        parts = line.split()
        if len(parts) >= 2 and parts[0].isdigit():
            title = line.split(".", 1)[-1]
            title = title.split("-", 1)[-1].strip() if "-" in title else title.strip()
            labels[int(parts[0])] = title
    return labels


def major_group(code: int) -> str:
    for edge, name in MAJOR_EDGES:
        if code <= edge:
            return name
    return "unclassified"


def shares(earn_w: np.ndarray, key: np.ndarray) -> pd.Series:
    total = earn_w.sum()
    if total <= 0:
        raise ValueError("empty earnings")
    return pd.Series(earn_w).groupby(key).sum() / total


def overlap(a: pd.Series, b: pd.Series) -> float:
    both = pd.concat([a.rename("a"), b.rename("b")], axis=1).fillna(0.0)
    return float(np.minimum(both.a, both.b).sum())


def cosine(a: pd.Series, b: pd.Series) -> float:
    both = pd.concat([a.rename("a"), b.rename("b")], axis=1).fillna(0.0)
    return float((both.a * both.b).sum() / np.sqrt((both.a ** 2).sum() * (both.b ** 2).sum()))


def load() -> pd.DataFrame:
    cols = ["A_AGE", "A_HGA", "PRPERTYP", "PRCITSHP", "PENATVTY", "PEFNTVTY", "PEMNTVTY",
            "PRDTHSP", "PEARNVAL", "PEIOOCC", "MARSUPWT"]
    with zipfile.ZipFile(ZIP) as zipped:
        frame = pd.read_csv(zipped.open("pppub25.csv"), usecols=cols)
    frame["w"] = frame.MARSUPWT.to_numpy(float) / 100.0
    frame["earn"] = np.maximum(frame.PEARNVAL.to_numpy(float), 0.0)
    us_area = [57, 60, 66, 69, 73, 78]
    native = frame.PRCITSHP.isin([1, 2, 3])
    foreign = frame.PRCITSHP.isin([4, 5])
    parents_us = frame.PEFNTVTY.isin(us_area) & frame.PEMNTVTY.isin(us_area)
    parent_mexico = frame.PEFNTVTY.eq(303) | frame.PEMNTVTY.eq(303)
    civilian = frame.PRPERTYP.eq(2) | frame.A_AGE.lt(15)
    mexico_born = foreign & frame.PENATVTY.eq(303)
    union_us_born = native & (parent_mexico | (parents_us & frame.PRDTHSP.eq(1)))
    frame["branch"] = np.select(
        [civilian & native & ~union_us_born & ~mexico_born,
         civilian & union_us_born,
         civilian & foreign & ~mexico_born,
         civilian & mexico_born],
        ["native_non_union", "union_us_born", "other_foreign_born", "union_mexico_born"],
        default="")
    if (frame.loc[civilian, "branch"] == "").any():
        raise ValueError("civilian universe is not partitioned")
    low = frame.A_HGA.between(31, 39)
    high = frame.A_HGA.between(40, 46)
    frame["cell"] = np.where(low, "low", np.where(high, "high", ""))
    return frame


def check_branch_totals(frame: pd.DataFrame) -> None:
    """Point earnings must match the nest's published branch composition."""
    published = pd.read_csv(BRANCHES)
    published = published.query("proxy == 'PEARNVAL' and split == 'hs_or_less'")
    cell_name = {0: "low", 1: "high"}
    for row in published.itertuples(index=False):
        mask = (frame.branch == row.branch) & (frame.cell == cell_name[row.skill]) & (frame.earn > 0)
        got = float((frame.loc[mask, "earn"] * frame.loc[mask, "w"]).sum())
        if abs(got - row.earnings_estimate) > 1e-7 * row.earnings_estimate:
            raise SystemExit(f"[BLOCKED] {row.branch} cell {row.skill}: {got} != {row.earnings_estimate}")


def main() -> None:
    frame = load()
    check_branch_totals(frame)
    labels = occupation_labels(DICT)
    earners = frame[(frame.earn > 0) & (frame.cell != "") & (frame.branch != "")].copy()
    earners["occ"] = earners.PEIOOCC.to_numpy(int)
    earners["valid_occ"] = earners.occ > 0
    earners["ew"] = earners.earn * earners.w
    dropped = 1 - earners.loc[earners.valid_occ, "ew"].sum() / earners.ew.sum()
    if dropped > 0.05:
        raise SystemExit(f"[BLOCKED] occupation-missing earnings share {dropped:.3f} exceeds 5%")
    use = earners[earners.valid_occ].copy()
    use["major"] = [major_group(int(code)) for code in use.occ]

    groups = {
        "native_non_union": use.branch.eq("native_non_union"),
        "union_us_born": use.branch.eq("union_us_born"),
        "other_foreign_born": use.branch.eq("other_foreign_born"),
        "union_mexico_born": use.branch.eq("union_mexico_born"),
        "all_native": use.branch.isin(["native_non_union", "union_us_born"]),
        "all_foreign": use.branch.isin(["other_foreign_born", "union_mexico_born"]),
    }
    pairs = [
        ("all_native", "all_foreign"),
        ("native_non_union", "union_mexico_born"),
        ("native_non_union", "other_foreign_born"),
        ("other_foreign_born", "union_mexico_born"),
        ("union_us_born", "native_non_union"),
    ]
    rows = []
    share_cache = {}
    for cell in ("low", "high"):
        in_cell = use.cell.eq(cell)
        for grain, column in (("detailed", "occ"), ("major", "major")):
            built = {name: shares(use.loc[in_cell & mask, "ew"].to_numpy(),
                                  use.loc[in_cell & mask, column].to_numpy())
                     for name, mask in groups.items()}
            share_cache[(cell, grain)] = built
            for left, right in pairs:
                rows.append(dict(
                    cell=cell, grain=grain, left=left, right=right,
                    overlap=overlap(built[left], built[right]),
                    cosine=cosine(built[left], built[right]),
                    earnings_missing_occupation_share=float(dropped),
                    output_type="measurement"))
    overlap_path = OUT / "occupation_overlap.csv"
    pd.DataFrame(rows).to_csv(overlap_path, index=False)

    low_mex = use.cell.eq("low") & use.branch.eq("union_mexico_born")
    mex_by_occ = use.loc[low_mex].groupby("occ").ew.sum().sort_values(ascending=False)
    mex_total = float(mex_by_occ.sum())
    top_rows = []
    for code, mex_earn in mex_by_occ.head(12).items():
        in_occ = use.cell.eq("low") & use.occ.eq(code)
        by_branch = use.loc[in_occ].groupby("branch").ew.sum()
        native = float(by_branch.get("native_non_union", 0) + by_branch.get("union_us_born", 0))
        other = float(by_branch.get("other_foreign_born", 0))
        total = native + other + float(mex_earn)
        top_rows.append(dict(
            occ=int(code), title=labels.get(int(code), ""),
            mexico_born_earnings_bn=float(mex_earn) / 1e9,
            share_of_mexico_born_low_earnings=float(mex_earn) / mex_total,
            native_earnings_bn=native / 1e9,
            other_foreign_born_earnings_bn=other / 1e9,
            mexico_born_share_of_occupation=float(mex_earn) / total,
            output_type="measurement"))
    top_path = OUT / "occupation_top_mexico_born_low.csv"
    pd.DataFrame(top_rows).to_csv(top_path, index=False)

    # Sketch only. Within-job values are the older within-cell range; between-job
    # values run from the removal model's occupation elasticity (1.6) to a notch
    # above this account's between-schooling elasticity (2).
    sketch = []
    for cell, grain, left, right, within, between in (
        *[(c, g, "all_native", "all_foreign", w, b)
          for c in ("low", "high") for g in ("detailed", "major")
          for w in (10, 20, np.inf) for b in (1.6, 2.0, 2.5, 3.0)],
        *[(c, g, "native_non_union", "union_mexico_born", w, b)
          for c in ("low",) for g in ("detailed", "major")
          for w in (10, 20, np.inf) for b in (1.6, 2.0, 2.5, 3.0)],
    ):
        theta = overlap(share_cache[(cell, grain)][left], share_cache[(cell, grain)][right])
        inv = (0 if np.isinf(within) else theta / within) + (1 - theta) / between
        sketch.append(dict(
            cell=cell, grain=grain, left=left, right=right,
            overlap=theta, epsilon_within=within, epsilon_between=between,
            epsilon_sketch=1 / inv, output_type="model_sketch"))
    sketch_path = OUT / "elasticity_sketch.csv"
    pd.DataFrame(sketch).to_csv(sketch_path, index=False)

    primary = [r for r in sketch if r["cell"] == "low" and r["left"] == "all_native"
               and r["epsilon_within"] == 20 and r["epsilon_between"] in (2.0, 2.5, 3.0)]
    print(f"occupation-missing earnings share {dropped:.4f}")
    print(f"wrote {overlap_path.name}, {top_path.name}, {sketch_path.name}")
    for row in primary:
        print(f"  {row['grain']:8} within {row['epsilon_within']} between {row['epsilon_between']}"
              f" overlap {row['overlap']:.3f} -> ε {row['epsilon_sketch']:.2f}")


if __name__ == "__main__":
    main()
