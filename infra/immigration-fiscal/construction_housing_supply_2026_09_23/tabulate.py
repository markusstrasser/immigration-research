"""ACS 2024 one-year PUMS: the Mexican-origin group's share of construction work, by trade and metro.

Reads only the needed columns of the zipped national person file in chunks.

Person groups (the housing lane's union rule, split as the brief asks):
  mx_born           born in Mexico (POBP=303)
  us_born_mx_origin Hispanic origin Mexican (HISP=02) and US-born (NATIVITY=1)
  fb_mx_origin      Hispanic origin Mexican, foreign-born outside Mexico (small)
  other_us_born, other_foreign_born   everyone else
The union (first three) is the account's group; ACS has no parental birthplace, so this is the
closest person rule (39.4m persons in ACS against the CPS union's 40.9m).

Work definitions:
  construction trades     OCCP 6200-6765 (the 2018 SOC 47-2xxx to 47-4xxx construction occupations),
                          in any industry; extraction occupations (6800+) are excluded
  construction industry   INDP 0770, all occupations
  employed                ESR 1 or 2 (civilian employed); occupation is the current job
  earnings                PERNP (wages plus self-employment income, past 12 months) x ADJINC, for
                          persons whose current or most recent job carries the code
  hours                   WKHP x WKWN (usual weekly hours x weeks worked, past 12 months)
  hs_or_less              SCHL <= 17 (regular diploma or GED or less), the account's low-skill split;
                          below_ba (SCHL <= 20) is its alternative split
Standard errors use the 80 successive-difference replicate weights.

Outputs (derived/):
  construction_national.csv   dimension x category x education x measure x group set: total, group
                              total and group share, each with replicate SE
  construction_puma.csv       PUMA x group totals (full weight) for trades, industry, all employed
  tabulate_checks.json        row counts and ADJINC values
Run from the repository root:
  OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/construction_housing_supply_2026_09_23/tabulate.py
"""
from __future__ import annotations

import io
import json
import pathlib
import zipfile

import numpy as np
import pandas as pd

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[2]
PUMS = ROOT / "sources/immigration-fiscal/data/external/acs_pums_2024_1yr"
DERIVED = HERE / "derived"
PREPS = [f"PWGTP{i}" for i in range(1, 81)]
WCOLS = ["PWGTP"] + PREPS
CHUNK = 150_000
MEXICO = 303
TRADES = (6200, 6765)
CONSTRUCTION_INDUSTRY = 770
MEASURES = ("employed", "earnings", "hours")


def read_persons():
    cols = (["STATE", "PUMA", "AGEP", "SCHL", "HISP", "POBP", "NATIVITY", "ESR", "OCCP", "INDP",
             "COW", "WKHP", "WKWN", "PERNP", "ADJINC"] + WCOLS)
    dtype = {"STATE": str, "PUMA": str}
    with zipfile.ZipFile(PUMS / "csv_pus.zip") as z:
        for member in ("psam_pusa.csv", "psam_pusb.csv"):
            with z.open(member) as fh:
                yield from pd.read_csv(io.TextIOWrapper(fh), usecols=cols, dtype=dtype,
                                       chunksize=CHUNK)


def group_of(chunk):
    hisp_mx = chunk["HISP"].eq(2)
    mx_born = chunk["POBP"].eq(MEXICO)
    us_born = chunk["NATIVITY"].eq(1)
    return np.select(
        [mx_born, hisp_mx & us_born, hisp_mx & ~us_born, us_born],
        ["mx_born", "us_born_mx_origin", "fb_mx_origin", "other_us_born"], "other_foreign_born")


def replicate_se(full, reps):
    return np.sqrt(4 / 80 * ((reps - full[..., None]) ** 2).sum(axis=-1))


# hs_or_less / more is the account's primary skill split; below_ba / ba_plus its alternative.
EDUCATION_SETS = {
    "all": ["hs_or_less", "some_college", "ba_plus"],
    "hs_or_less": ["hs_or_less"],
    "more": ["some_college", "ba_plus"],
    "below_ba": ["hs_or_less", "some_college"],
    "ba_plus": ["ba_plus"],
}
GROUP_SETS = {
    "union": ["mx_born", "us_born_mx_origin", "fb_mx_origin"],
    "mx_born": ["mx_born"],
    "us_born_mx_origin": ["us_born_mx_origin"],
    "fb_mx_origin": ["fb_mx_origin"],
    "other_us_born": ["other_us_born"],
    "other_foreign_born": ["other_foreign_born"],
    "all": ["mx_born", "us_born_mx_origin", "fb_mx_origin", "other_us_born", "other_foreign_born"],
}


def shares(table):
    """Totals and group shares with replicate SEs, per dimension x category x education."""
    rows = []
    idx = table.index.to_frame(index=False)
    for (dim, cat), sub in idx.groupby(["dimension", "category"]):
        block = table.loc[[tuple(r) for r in sub.to_numpy()]]
        for education, cells in EDUCATION_SETS.items():
            edu = block[block.index.get_level_values("education").isin(cells)]
            for measure in MEASURES:
                cols = [f"{measure}|{c}" for c in WCOLS]
                by_group = edu.groupby(level="group")[cols].sum()
                total = by_group.sum(axis=0).to_numpy(float)
                for name, members in GROUP_SETS.items():
                    part = by_group.reindex(members).fillna(0).sum(axis=0).to_numpy(float)
                    share = np.divide(part, total, out=np.zeros_like(part), where=total != 0)
                    rows.append({
                        "dimension": dim, "category": cat, "education": education,
                        "measure": measure, "group_set": name,
                        "total": total[0], "group_total": part[0],
                        "group_total_se": float(replicate_se(part[:1], part[None, 1:])[0]),
                        "share": share[0],
                        "share_se": float(replicate_se(share[:1], share[None, 1:])[0])})
    return pd.DataFrame(rows)


def main():
    DERIVED.mkdir(exist_ok=True)
    national, pumas = [], []
    checks = {"rows": 0, "rows_with_occupation": 0, "adjinc_values": set()}
    for chunk in read_persons():
        checks["rows"] += len(chunk)
        checks["adjinc_values"].update(chunk["ADJINC"].unique().tolist())
        chunk = chunk[chunk["AGEP"].ge(16) & chunk["OCCP"].notna()].copy()
        checks["rows_with_occupation"] += len(chunk)
        occ = chunk["OCCP"].astype(int)
        ind = chunk["INDP"].fillna(-1).astype(int)
        grp = group_of(chunk)
        schl = chunk["SCHL"].fillna(0)
        educ = np.select([schl.le(17), schl.le(20)], ["hs_or_less", "some_college"], "ba_plus")
        employed = chunk["ESR"].isin([1, 2]).to_numpy(float)
        earnings = chunk["PERNP"].fillna(0).to_numpy(float) * chunk["ADJINC"].to_numpy(float) / 1e6
        hours = (chunk["WKHP"].fillna(0) * chunk["WKWN"].fillna(0)).to_numpy(float)
        trade = occ.between(*TRADES).to_numpy()
        con_ind = ind.eq(CONSTRUCTION_INDUSTRY).to_numpy()
        weights = chunk[WCOLS].to_numpy(float)
        # One row per person and dimension: the person's own trade, the construction-trades total,
        # the construction-industry total, trades inside the industry, and all workers.
        dims = [
            ("occupation", np.where(trade, occ.astype(str).to_numpy(), "not_a_trade")),
            ("trades_total", np.where(trade, "all_trades", "not_a_trade")),
            ("industry_total", np.where(con_ind, "construction_industry", "other_industry")),
            ("industry_by_trade", np.where(con_ind, np.where(trade, "trade_in_industry",
                                                             "nontrade_in_industry"),
                                           "other_industry")),
            ("all_workers", np.full(len(chunk), "all")),
        ]
        for dim, cat in dims:
            keep = cat != "not_a_trade" if dim in ("occupation", "trades_total") else np.ones(len(chunk), bool)
            if dim == "industry_by_trade":
                keep = cat != "other_industry"
            if not keep.any():
                continue
            frame = pd.DataFrame({"dimension": dim, "category": cat[keep], "education": educ[keep],
                                  "group": grp[keep]})
            vals = {}
            for name, x in (("employed", employed), ("earnings", earnings), ("hours", hours)):
                prod = weights[keep] * x[keep, None]
                for j, col in enumerate(WCOLS):
                    vals[f"{name}|{col}"] = prod[:, j]
            frame = pd.concat([frame, pd.DataFrame(vals, index=frame.index)], axis=1)
            national.append(frame.groupby(["dimension", "category", "education", "group"]).sum())
        w = chunk["PWGTP"].to_numpy(float)
        puma = pd.DataFrame({
            "STATE": chunk["STATE"], "PUMA": chunk["PUMA"], "group": grp,
            "trades_employed": w * employed * trade,
            "trades_earnings": w * earnings * trade,
            "industry_employed": w * employed * con_ind,
            "industry_earnings": w * earnings * con_ind,
            "all_employed": w * employed,
            "all_earnings": w * earnings})
        pumas.append(puma.groupby(["STATE", "PUMA", "group"]).sum())
    table = pd.concat(national).groupby(level=[0, 1, 2, 3]).sum()
    shares(table).to_csv(DERIVED / "construction_national.csv", index=False)
    puma = pd.concat(pumas).groupby(level=[0, 1, 2]).sum().reset_index()
    puma.to_csv(DERIVED / "construction_puma.csv", index=False)
    checks["adjinc_values"] = sorted(checks["adjinc_values"])
    (DERIVED / "tabulate_checks.json").write_text(json.dumps(checks, indent=2, default=float))
    print(json.dumps(checks, default=float))


if __name__ == "__main__":
    main()
