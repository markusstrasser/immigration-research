"""Anatomy of the ACS 2020 schooling break: which reported grades feed the extra "no schooling" reports,
and does any boundary other than none / grades 1-8 move?

Input: the Census 1-year PUMS person files for 2017-2019 and 2021-2024, as slimmed (no recoding) by
dataset_integrity_2026_09_23/acs_extract.py into that lane's ignored _cache (read-only here; sha256
pinned below). There is no 1-year 2020 PUMS.

For each population and survey year: weighted shares of SCHL categories. Two universes:
  age20_64  persons aged 20-64 (the brief's table), all quarters
  fixed     birth years 1955-1987 (ages 30-62 in 2017, 37-69 in 2024), households only, and for the
            foreign-born arrival (YOEP) 2009 or earlier: the same people in every year up to mortality,
            emigration and weighting, so a step at 2020 cannot be a change in who is counted
Step estimates per category (percentage points):
  level_step  mean(2021-2024) - mean(2017-2019)
  trend_step  c in share_t = a + b (t - 2019) + c 1[t >= 2021], fitted by OLS on the seven years
Outputs: derived/break_anatomy_shares.csv, derived/break_steps.csv, derived/break_anatomy_audit.json.
Run from the repository root:
  OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/acs_schooling_break_2026_09_26/break_anatomy.py
"""
import hashlib
import json
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
CACHE = ROOT / "infra/immigration-fiscal/dataset_integrity_2026_09_23/_cache"
DERIVED = HERE / "derived"
YEARS = [2017, 2018, 2019, 2021, 2022, 2023, 2024]
SHA = {
    2017: "822ff0ac452e5bf473250307e1ffd111d7fde7c79848c98eee5f526aa2c5d222",
    2018: "e933c8500c74b555878a94bd464b18c3bf40c8e5b2afb9847f4b10685f7aeddd",
    2019: "3e40c5c1bfeb4002d16d0aeea757f535222dc6f2bd867bc117079d95f0714e61",
    2021: "0b96a38973adade9d2131f9bc3ab27d857292ed523e2815c0462ed82c2d6eebc",
    2022: "e43949e008cf3d162f960c1913d254f80e878cd3b82e6a53b66b5d48ff88cea2",
    2023: "e378293a55a4845f489d4c40cec447134e53e90a1963f20f5bd4884480115f8c",
    2024: "7f8fa127db584862759cf1cf59bd14036e9788bea9d5300338527bf35e4f35d0",
}
COLS = ["AGEP", "SCHL", "FSCHLP", "POBP", "NATIVITY", "HISP", "RAC1P", "YOEP", "PWGTP", "RELSHIPP", "RELP"]
# SCHL (2008+ coding) -> category; every code 1-24 is covered (gated)
CATS = [("none", [1]), ("prek", [2, 3]), ("g1_4", [4, 5, 6, 7]), ("g5", [8]), ("g6", [9]), ("g7", [10]),
        ("g8", [11]), ("g9", [12]), ("g10", [13]), ("g11", [14]), ("g12_nodip", [15]), ("diploma", [16]),
        ("ged", [17]), ("college_lt1", [18]), ("college_1plus", [19]), ("assoc", [20]), ("ba", [21]),
        ("grad", [22, 23, 24])]
CAT_OF = {s: c for c, codes in CATS for s in codes}
CAT_NAMES = [c for c, _ in CATS]
BIRTH = (1955, 1987)
ARRIVED_BY = 2009
LATAM = set(range(310, 400))  # POBP Central America, Caribbean, South America (2017+ dictionaries)


def gate(ok: bool, msg: str) -> None:
    if not ok:
        raise SystemExit(msg)


def sha256(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def load(year: int) -> pd.DataFrame:
    p = CACHE / f"acs_person_{year}.parquet"
    gate(p.exists(), f"[BLOCKED] missing {p}")
    gate(sha256(p) == SHA[year], f"[BLOCKED] {p.name} sha256 differs from the pinned value")
    have = pd.read_parquet(p, columns=None).columns
    d = pd.read_parquet(p, columns=[c for c in COLS if c in have])
    gh = d["RELSHIPP"].ge(37) if "RELSHIPP" in d else d["RELP"].isin([16, 17])  # group quarters
    d = d.assign(YEAR=year, gq=gh.fillna(False).to_numpy(), birth=year - d.AGEP)
    d = d[d.AGEP.ge(20)]
    gate(bool(d.SCHL.notna().all()), f"[BLOCKED] {year}: adult without SCHL")
    gate(set(d.SCHL.astype(int).unique()) <= set(CAT_OF), f"[BLOCKED] {year}: SCHL code outside 1-24")
    d["cat"] = d.SCHL.astype(int).map(CAT_OF)
    fb, hisp = d.NATIVITY.eq(2), d.HISP.ne(1)
    d["group"] = np.select(
        [d.POBP.eq(303), fb & hisp & d.POBP.isin(LATAM), fb & hisp, fb, d.NATIVITY.eq(1) & hisp,
         d.NATIVITY.eq(1) & d.RAC1P.eq(1), d.NATIVITY.eq(1) & d.RAC1P.eq(2), d.NATIVITY.eq(1)],
        ["mexico_born", "other_latam_hispanic_fb", "other_hispanic_fb", "non_hispanic_fb", "usborn_hispanic",
         "usborn_nh_white", "usborn_nh_black", "usborn_nh_other"], "unclassified")
    gate(not (d.group == "unclassified").any(), f"[BLOCKED] {year}: record outside every group")
    return d


def universes(d: pd.DataFrame) -> dict:
    fixed = d[~d.gq & d.birth.between(*BIRTH) & (d.NATIVITY.eq(1) | d.YOEP.le(ARRIVED_BY))]
    return {"age20_64": d[d.AGEP.le(64)], "fixed": fixed, "age20_64_reported": d[d.AGEP.le(64) & d.FSCHLP.eq(0)],
            "age65plus": d[d.AGEP.ge(65)]}


POOLS = {"usborn": ["usborn_hispanic", "usborn_nh_white", "usborn_nh_black", "usborn_nh_other"],
         "foreign_born": ["mexico_born", "other_latam_hispanic_fb", "other_hispanic_fb", "non_hispanic_fb"]}


def share_rows(year: int, uni: str, g: pd.DataFrame) -> list[dict]:
    rows = []
    groups = {k: g[g.group == k] for k in g.group.unique()}
    for pool, members in POOLS.items():
        groups[pool] = g[g.group.isin(members)]
    for name, t in groups.items():
        w = t.PWGTP.to_numpy(float)
        W = w.sum()
        by = pd.Series(w).groupby(t.cat.to_numpy()).sum()
        for c in CAT_NAMES:
            rows.append({"universe": uni, "group": name, "year": year, "category": c, "n": len(t),
                         "share_pct": 100 * float(by.get(c, 0.0)) / W})
    return rows


def steps(S: pd.DataFrame) -> pd.DataFrame:
    X = np.column_stack([np.ones(len(YEARS)), np.array(YEARS) - 2019, (np.array(YEARS) >= 2021).astype(float)])
    out = []
    for (uni, grp, cat), t in S.groupby(["universe", "group", "category"], sort=False):
        t = t.set_index("year").reindex(YEARS)
        gate(bool(t.share_pct.notna().all()), f"[BLOCKED] {uni}/{grp}/{cat}: missing year")
        y = t.share_pct.to_numpy()
        coef, *_ = np.linalg.lstsq(X, y, rcond=None)
        pre, post = y[:3].mean(), y[3:].mean()
        out.append({"universe": uni, "group": grp, "category": cat, "n_2019": int(t.n[2019]),
                    "share_2019": y[2], "share_2021": y[3], "share_2024": y[-1], "level_step": post - pre,
                    "trend_step": coef[2], "trend_slope_per_year": coef[1]})
    return pd.DataFrame(out)


def main() -> None:
    DERIVED.mkdir(exist_ok=True)
    rows = []
    for y in YEARS:
        d = load(y)
        for uni, g in universes(d).items():
            rows += share_rows(y, uni, g)
        print(f"{y}: {len(d):,} adults", flush=True)
    S = pd.DataFrame(rows)
    tot = S.groupby(["universe", "group", "year"]).share_pct.sum()
    gate(bool(np.allclose(tot.to_numpy(), 100.0)), "[BLOCKED] category shares do not sum to 100")
    S.to_csv(DERIVED / "break_anatomy_shares.csv", index=False, float_format="%.5f", lineterminator="\n")
    T = steps(S)
    T.to_csv(DERIVED / "break_steps.csv", index=False, float_format="%.5f", lineterminator="\n")
    audit = {"inputs": {str(y): SHA[y] for y in YEARS}, "birth_years_fixed": BIRTH, "arrived_by_fixed": ARRIVED_BY,
             "years": YEARS}
    (DERIVED / "break_anatomy_audit.json").write_text(json.dumps(audit, indent=1) + "\n")
    pd.set_option("display.width", 250)
    for uni in ("age20_64", "fixed"):
        v = T[T.universe == uni].pivot(index="category", columns="group", values="trend_step").reindex(CAT_NAMES)
        print(f"\n== trend_step (pp), universe {uni}")
        print(v.round(2).to_string())


if __name__ == "__main__":
    main()
