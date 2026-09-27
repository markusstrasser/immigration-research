#!/usr/bin/env python3
"""Selection curve, tasks 1-3 and 6 on the IPUMS-CPS ASEC 1994-2025 extract.

Every person is placed in the distribution of the third-plus-generation non-Hispanic white
reference (NATIVITY 1, HISPAN 0, RACE 100) of the same survey year and five-year age band
(main spec; sex added as a sensitivity). Percentiles are weighted mid-ranks, 0-100, so ties
(zero earnings, one EDUC code) sit at the middle of their mass and the reference mean is 50.

Task 1: percentile distribution and top-tail share of the earnings gap, 2015-2025 pooled.
Task 2: origin-level G1 -> G2 mean percentile, every parental birthplace with >= 150 G2 adults.
Task 3: G1 percentile inside the origin country's schooling distribution (Barro-Lee v3, same
        birth cohort) -> G1 US percentile -> G2 US percentile.
Task 6: nonlinearity, leave-one-out, G2 tails.

Descriptive only: origin-group means by generation observed in the same years are synthetic
cohorts, not the same families.

Run from the repo root:
  OPENBLAS_NUM_THREADS=1 uv run --no-project --with duckdb --with pyarrow python3 \
      infra/immigration-fiscal/selection_curve_2026_09_27/cps_curve.py
"""
from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

LANE = Path(__file__).resolve().parent
sys.path.insert(0, str(LANE))
import load  # noqa: E402

DERIVED = LANE / "derived"
BL_CSV = LANE / "_cache" / "BL_v3_MF.csv"
BL_SHA = "618732c5cc749f91e609a7fb7a1e1142d761c2b97510781b07754322a24218ef"
WIC_RDS = LANE / "_cache" / "wic_v3_ssp2_pop-age-edattain.rds"
WIC_SHA = "ddbdac12a576ad94e142085790a3b9cec0af484f2c7e647879a102a51b7b0d60"
CPI_CSV = LANE / "_cache" / "cpiaucsl_annual.csv"

SEED = 20260927
NBOOT = 2000
MIN_G2 = 150
MIN_G1 = 100
INC_NIU = 99999998
EDUC_MISSING = (0, 1, 999)
AGE_EDGES = [25, 30, 35, 40, 45, 50, 55, 60, 65]

# Merged origins: IPUMS splits some countries across codes or over time.
MERGE = {
    50220: 50200,                   # South Korea -> Korea
    41100: 41000, 41300: 41000,     # Scotland, United Kingdom n.s. -> England/UK
    41200: 41000, 41410: 41000,     # Wales, Northern Ireland -> UK
    46590: 46500,                   # USSR n.s. -> Other USSR/Russia
    45212: 45200, 45213: 45200,     # Slovakia, Czech Republic -> Czechoslovakia
    43610: 43600,                   # Azores -> Portugal
}
ORIGIN_NAME = {41000: "United Kingdom", 46500: "Russia/USSR", 45200: "Czechoslovakia",
               50200: "Korea", 60012: "Egypt", 30040: "Guyana", 21010: "Belize",
               60094: "South Africa", 45700: "Yugoslavia"}
# Residual / not-specified codes are not origins.
DROP = {59900, 49900, 60099, 26000, 30000, 60000, 71000, 21000, 50099, 29900, 30099}

FOCUS = {20000: "Mexico", 52100: "India", 50000: "China", 51500: "Philippines",
         51800: "Vietnam", 60031: "Nigeria", 50200: "Korea", 25000: "Cuba",
         21030: "El Salvador"}

# IPUMS BPL -> Barro-Lee v3 country name.
BL_NAME = {
    20000: "Mexico", 15000: "Canada", 45300: "Germany", 43400: "Italy",
    51500: "Philippines", 41000: "United Kingdom", 25000: "Cuba", 50000: "China",
    45500: "Poland", 41400: "Ireland", 50100: "Japan", 21030: "El Salvador", 52100: "India",
    26010: "Dominican Rep.", 51800: "Viet Nam", 43300: "Greece", 43600: "Portugal",
    46500: "Russian Federation", 30025: "Colombia", 50200: "Republic of Korea",
    42100: "France", 26030: "Jamaica", 42500: "Netherlands", 45400: "Hungary",
    43800: "Spain", 21040: "Guatemala", 26020: "Haiti", 45000: "Austria", 30030: "Ecuador",
    40400: "Norway", 30050: "Peru", 50040: "Taiwan", 40500: "Sweden",
    51300: "Lao People's Democratic Republic", 21070: "Panama", 51700: "Thailand",
    30005: "Argentina", 21050: "Honduras", 26060: "Trinidad and Tobago",
    21060: "Nicaragua", 53000: "Iran (Islamic Republic of)", 46530: "Ukraine",
    50010: "China, Hong Kong Special Administrative Region", 40000: "Denmark",
    53400: "Israel", 42600: "Switzerland", 53700: "Lebanon", 70010: "Australia",
    60031: "Nigeria", 46300: "Lithuania", 51100: "Cambodia", 52140: "Pakistan",
    42000: "Belgium", 30015: "Brazil", 30040: "Guyana", 30020: "Chile",
    21020: "Costa Rica", 60012: "Egypt", 45200: "Czech Republic", 45600: "Romania",
    30065: "Venezuela", 46200: "Latvia", 51200: "Indonesia", 54200: "Turkey",
    26044: "Barbados", 40100: "Finland", 53200: "Iraq", 54100: "Syrian Arab Republic",
    45730: "Croatia", 60065: "Uganda", 60094: "South Africa", 30010: "Bolivia",
    60018: "Sudan", 55100: "Armenia", 21010: "Belize", 45700: "Serbia", 71022: "Tonga",
    71023: "Samoa",
}

# CPS EDUC -> Barro-Lee attainment category 0..6
#   0 no schooling, 1 primary incomplete, 2 primary complete, 3 secondary incomplete,
#   4 secondary complete, 5 tertiary incomplete, 6 tertiary complete
EDUC_TO_BL = {2: 0, 10: 1, 20: 2, 30: 3, 40: 3, 50: 3, 60: 3, 71: 3, 73: 4,
              81: 5, 91: 5, 92: 5, 111: 6, 123: 6, 124: 6, 125: 6}
# CPS EDUC -> Wittgenstein Centre v3 completed level 0..5
#   0 none, 1 incomplete primary, 2 primary, 3 lower secondary, 4 upper secondary,
#   5 post-secondary (WIC short post-secondary, bachelor, master+ and lumped post-secondary)
EDUC_TO_WIC = {2: 0, 10: 1, 20: 2, 30: 2, 40: 3, 50: 3, 60: 3, 71: 3, 73: 4,
               81: 4, 91: 5, 92: 5, 111: 5, 123: 5, 124: 5, 125: 5}
WIC_LEVELS = ["No Education", "Incomplete Primary", "Primary", "Lower Secondary",
              "Upper Secondary", "Post Secondary"]
WIC_OVERRIDE = {41000: "United Kingdom of Great Britain and Northern Ireland",
                50040: "Taiwan Province of China",
                50010: "Hong Kong Special Administrative Region of China",
                30065: "Venezuela (Bolivarian Republic of)",
                30010: "Bolivia (Plurinational State of)",
                26010: "Dominican Republic", 53700: "Lebanon", 60031: "Nigeria", 71023: "Samoa"}

EDUC_YEARS = {2: 0, 10: 2.5, 20: 5.5, 30: 7.5, 40: 9, 50: 10, 60: 11, 71: 12, 73: 12,
              81: 13, 91: 14, 92: 14, 111: 16, 123: 18, 124: 19, 125: 20}


def write_csv(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(exist_ok=True)
    with open(path, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()), lineterminator="\n")
        w.writeheader()
        for r in rows:
            w.writerow({k: (f"{v:.6g}" if isinstance(v, float) else v) for k, v in r.items()})


# ---------------------------------------------------------------------------------------------
# percentile machinery
# ---------------------------------------------------------------------------------------------

def midrank_pct(ref_y: np.ndarray, ref_w: np.ndarray, q: np.ndarray) -> np.ndarray:
    """100 x (weight below q + half the weight equal to q) / total, in the reference sample."""
    order = np.argsort(ref_y, kind="stable")
    y, w = ref_y[order], ref_w[order]
    uniq, start = np.unique(y, return_index=True)
    cw = np.concatenate([[0.0], np.cumsum(w)])
    below_u = cw[start]
    end = np.append(start[1:], len(y))
    eq_u = cw[end] - cw[start]
    tot = cw[-1]
    pos = np.searchsorted(uniq, q, side="left")
    below = np.where(pos < len(uniq), below_u[np.minimum(pos, len(uniq) - 1)], tot)
    hit = (pos < len(uniq)) & (uniq[np.minimum(pos, len(uniq) - 1)] == q)
    eq = np.where(hit, eq_u[np.minimum(pos, len(uniq) - 1)], 0.0)
    return 100.0 * (below + 0.5 * eq) / tot


def wquantile(y: np.ndarray, w: np.ndarray, p: float) -> float:
    o = np.argsort(y, kind="stable")
    cw = np.cumsum(w[o]) / w.sum()
    return float(y[o][min(np.searchsorted(cw, p), len(y) - 1)])


def add_percentiles(df: pd.DataFrame, ref: np.ndarray, var: str, valid: np.ndarray,
                    cell_cols: list[str], out: str) -> None:
    pct = np.full(len(df), np.nan)
    keys = df[cell_cols].to_numpy()
    kid = pd.MultiIndex.from_arrays(keys.T).factorize()[0] if len(cell_cols) > 1 \
        else pd.factorize(keys[:, 0])[0]
    y = df[var].to_numpy(dtype=float)
    w = df.w.to_numpy()
    order = np.argsort(kid, kind="stable")
    bounds = np.flatnonzero(np.diff(kid[order])) + 1
    for idx in np.split(order, bounds):
        v = idx[valid[idx]]
        r = v[ref[v]]
        if len(r) == 0 or len(v) == 0:
            continue
        pct[v] = midrank_pct(y[r], w[r], y[v])
    df[out] = pct


def std_weights(df: pd.DataFrame, mask: np.ndarray, ref_share: pd.Series) -> np.ndarray:
    """Person weights reweighted so the group's age-band mix equals the reference's."""
    sub = df.loc[mask]
    share = sub.groupby("band").w.sum() / sub.w.sum()
    f = (ref_share / share).reindex(sub.band).to_numpy()
    return sub.w.to_numpy() * np.nan_to_num(f, nan=0.0)


def wmean_se(y: np.ndarray, w: np.ndarray) -> tuple[float, float]:
    ok = np.isfinite(y) & (w > 0)
    y, w = y[ok], w[ok]
    m = float(np.sum(w * y) / w.sum())
    neff = w.sum() ** 2 / np.sum(w ** 2)
    sd = float(np.sqrt(np.sum(w * (y - m) ** 2) / w.sum()))
    return m, sd / np.sqrt(neff)


# ---------------------------------------------------------------------------------------------
# frame
# ---------------------------------------------------------------------------------------------

def prepare() -> pd.DataFrame:
    df = load.load_frame()
    df["band"] = np.digitize(df.age, AGE_EDGES) - 1
    df["ref"] = (df.nativity == 1) & (df.hispan == 0) & (df.race == 100)
    po = load.parent_origin(df)
    g1 = df.nativity.to_numpy() == 5
    g2 = df.nativity.isin([2, 3, 4]).to_numpy()
    origin = np.where(g1, df.bpl.to_numpy(), np.where(g2, po, -1))
    origin = pd.Series(origin).replace(MERGE).to_numpy().copy()
    origin[np.isin(origin, list(DROP))] = -1
    origin[(origin // 100) < 150] = -1        # US and US outlying areas are not origins
    df["origin"] = origin
    df["gen"] = np.where(g1, 1, np.where(g2, 2, 3))
    df["educ_ok"] = ~df.educ.isin(EDUC_MISSING)
    df["educ_years"] = df.educ.map(EDUC_YEARS)
    df["earn_ok"] = df.incwage < INC_NIU
    df["earn"] = df.incwage.astype(float)
    df["inctot_ok"] = df.inctot < INC_NIU
    df["inctot_f"] = df.inctot.astype(float)
    ref = df.ref.to_numpy()
    add_percentiles(df, ref, "educ", df.educ_ok.to_numpy(), ["year", "band"], "p_edu")
    add_percentiles(df, ref, "earn", df.earn_ok.to_numpy(), ["year", "band"], "p_earn")
    add_percentiles(df, ref, "educ", df.educ_ok.to_numpy(), ["year", "band", "sex"], "p_edu_sex")
    add_percentiles(df, ref, "earn", df.earn_ok.to_numpy(), ["year", "band", "sex"], "p_earn_sex")
    add_percentiles(df, ref, "inctot_f", df.inctot_ok.to_numpy(), ["year", "band"], "p_inctot")
    pos = df.earn_ok.to_numpy() & (df.earn.to_numpy() > 0)
    add_percentiles(df, ref, "earn", pos, ["year", "band"], "p_earn_pos")
    return df


# ---------------------------------------------------------------------------------------------
# Gate: ladder 178's Mexican G2 no-HS gap from the V02 lane's own estimator
# ---------------------------------------------------------------------------------------------

def gate_ladder178(df: pd.DataFrame) -> dict:
    import importlib.util
    spec = importlib.util.spec_from_file_location("v02", load.G2_LANE / "analysis.py")
    v02 = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(v02)
    ddi = v02.parse_ddi(load.DDI)
    d = df.drop(columns=[c for c in df.columns if c.startswith("p_")]).copy()
    countries = v02.top_countries(d)
    G = v02.build_groups(d, countries)
    tax = v02.build_taxonomies(G, ddi)["region_gen_union"]
    fine_to_group = np.full(G["n_fine"], -1)
    for gi, (_, members) in enumerate(tax):
        fine_to_group[members] = gi
    grp = fine_to_group[G["fine"]]
    ref = [n for n, _ in tax].index("3rd+_NH_white")
    tgt = [n for n, _ in tax].index("Mexico|2nd_gen_all")
    educ = d.educ.to_numpy()
    mask = ~np.isin(educ, v02.EDUC_NIU)
    y = ((educ <= v02.EDUC_LT_HS_MAX) & (educ >= 2)).astype(float)
    yi = np.searchsorted(v02.YEARS, d.year.to_numpy())
    bi = np.digitize(d.age.to_numpy(), v02.AGE_BAND_EDGES) - 1
    fe = (bi * 2 + (d.sex.to_numpy() - 1)) * v02.NY + yi
    w = d.w.to_numpy()
    W = np.zeros((len(tax), v02.NFE))
    Y = np.zeros((len(tax), v02.NFE))
    np.add.at(W, (grp[mask], fe[mask]), w[mask])
    np.add.at(Y, (grp[mask], fe[mask]), (w * y)[mask])
    gaps, status = v02.wls_gaps(W, Y, ref)
    got = float(gaps[tgt])
    published = pd.read_csv(load.G2_LANE / "derived" / "adjusted_gaps.csv")
    pub = published[(published.outcome == "less_than_hs") & (published.taxonomy == "region_gen_union")
                    & (published.period == "all") & (published.group == "Mexico|2nd_gen_all")]
    pub_v = float(pub.adjusted_gap.iloc[0])
    ok = abs(got - pub_v) < 5e-4 and abs(got - 0.1184) < 5e-4
    return {"status": "PASS" if ok else "FAIL", "reproduced": got, "published_csv": pub_v,
            "ladder_178": 0.1184, "solver": status}


# ---------------------------------------------------------------------------------------------
# Task 1
# ---------------------------------------------------------------------------------------------

def cpi_factor() -> dict[int, float]:
    c = pd.read_csv(CPI_CSV).dropna()
    c["yr"] = c.observation_date.str[:4].astype(int)
    idx = dict(zip(c.yr, c.CPIAUCSL))
    return {sy: idx[2024] / idx[sy - 1] for sy in range(1994, 2026)}   # ASEC year -> 2024 $


def task1(df: pd.DataFrame) -> tuple[list[dict], list[dict]]:
    win = (df.year >= 2015).to_numpy()
    cpi = cpi_factor()
    d = df.loc[win].copy()
    d["earn24"] = d.earn * d.year.map(cpi)
    ref = d.ref.to_numpy()
    ref_share = d.loc[ref].groupby("band").w.sum() / d.loc[ref].w.sum()
    groups = {"white_reference_G3plus": ref}
    for code, name in [(52100, "India"), (50000, "China"), (51500, "Philippines"), (20000, "Mexico")]:
        groups[f"{name}_G1"] = ((d.gen == 1) & (d.origin == code)).to_numpy()
        groups[f"{name}_G2"] = ((d.gen == 2) & (d.origin == code)).to_numpy()
    groups["China_broad_G1"] = ((d.gen == 1) & d.origin.isin([50000, 50010, 50040])).to_numpy()
    groups["all_foreign_born_G1"] = (d.gen == 1).to_numpy()
    groups["all_G2"] = (d.gen == 2).to_numpy()

    # white thresholds per (year, band) cell for the tail decomposition
    thr = {}
    for q in (0.90, 0.95, 0.99):
        t = {}
        sub = d.loc[ref & d.earn_ok.to_numpy()]
        for key, g in sub.groupby(["year", "band"]):
            t[key] = wquantile(g.earn.to_numpy(), g.w.to_numpy(), q)
        thr[q] = pd.Series([t[k] for k in zip(d.year, d.band)], index=d.index).to_numpy()

    dist_rows, tail_rows = [], []
    for gname, m in groups.items():
        for var, ok, lab in [("p_earn", "earn_ok", "wage_earnings_incl_zero"),
                             ("p_edu", "educ_ok", "education"),
                             ("p_earn_pos", "earn_ok", "wage_earnings_positive_only")]:
            mm = m & d[ok].to_numpy() & np.isfinite(d[var].to_numpy())
            if mm.sum() == 0:
                continue
            ws = std_weights(d, mm, ref_share)
            y = d.loc[mm, var].to_numpy()
            mean, se = wmean_se(y, ws)
            row = {"group": gname, "outcome": lab, "window": "2015-2025", "n": int(mm.sum()),
                   "mean_pct": mean, "se_mean_pct": se}
            for p in (0.10, 0.25, 0.50, 0.75, 0.90):
                row[f"p{int(p * 100)}"] = wquantile(y, ws, p)
            for cut in (90, 95, 99):
                row[f"share_above_white_p{cut}"] = float(ws[y > cut].sum() / ws.sum())
            dist_rows.append(row)

        # tail decomposition of the age-standardised mean earnings gap (2024 dollars)
        if gname == "white_reference_G3plus":
            continue
        mm = m & d.earn_ok.to_numpy()
        rr = ref & d.earn_ok.to_numpy()
        wg, wr = std_weights(d, mm, ref_share), std_weights(d, rr, ref_share)
        yg, yr = d.loc[mm, "earn24"].to_numpy(), d.loc[rr, "earn24"].to_numpy()
        f_g = d.loc[mm, "year"].map(cpi).to_numpy()
        f_r = d.loc[rr, "year"].map(cpi).to_numpy()
        gap = np.average(yg, weights=wg) - np.average(yr, weights=wr)
        base = {"group": gname, "n": int(mm.sum()), "mean_earn_2024usd": float(np.average(yg, weights=wg)),
                "white_mean_earn_2024usd": float(np.average(yr, weights=wr)), "gap_2024usd": float(gap)}
        for q in (0.90, 0.95, 0.99):
            tg, tr = thr[q][mm] * f_g, thr[q][rr] * f_r
            exg = np.maximum(yg - tg, 0)
            exr = np.maximum(yr - tr, 0)
            ex_gap = np.average(exg, weights=wg) - np.average(exr, weights=wr)
            above_g = yg > tg
            above_r = yr > tr
            cond_gap = (np.average(yg[~above_g], weights=wg[~above_g])
                        - np.average(yr[~above_r], weights=wr[~above_r]))
            # people-share decomposition: gap = sum over persons above T + below T
            part_above = (np.sum(wg[above_g] * yg[above_g]) / wg.sum()
                          - np.sum(wr[above_r] * yr[above_r]) / wr.sum())
            tail_rows.append({**base, "white_threshold": f"p{int(q * 100)}",
                              "group_share_above": float(wg[above_g].sum() / wg.sum()),
                              "white_share_above": float(wr[above_r].sum() / wr.sum()),
                              "excess_over_threshold_gap": float(ex_gap),
                              "share_of_gap_from_excess": float(ex_gap / gap),
                              "gap_winsorised_at_threshold": float(gap - ex_gap),
                              "gap_from_persons_above": float(part_above),
                              "share_of_gap_from_persons_above": float(part_above / gap),
                              "gap_excluding_persons_above": float(cond_gap)})
    return dist_rows, tail_rows


# ---------------------------------------------------------------------------------------------
# Tasks 2, 3, 6
# ---------------------------------------------------------------------------------------------

def barro_lee() -> pd.DataFrame:
    if load.sha256_file(BL_CSV) != BL_SHA:
        raise SystemExit("[BLOCKED] Barro-Lee v3 file hash changed")
    bl = pd.read_csv(BL_CSV)
    bl = bl[bl.sex == "MF"]
    cats = np.stack([bl.lu, bl.lp - bl.lpc, bl.lpc, bl.ls - bl.lsc, bl.lsc, bl.lh - bl.lhc,
                     bl.lhc], axis=1)
    cats = np.clip(cats, 0, None)
    cats = cats / cats.sum(1, keepdims=True)
    for k in range(7):
        bl[f"c{k}"] = cats[:, k]
    return bl


def origin_selection_pct(df: pd.DataFrame, bl: pd.DataFrame) -> np.ndarray:
    """Mid-rank of each G1 person's schooling in the origin country's same-cohort distribution."""
    out = np.full(len(df), np.nan)
    g1 = (df.gen == 1).to_numpy() & df.educ_ok.to_numpy() & (df.origin > 0).to_numpy()
    birth = (df.year - df.age - 1).to_numpy()
    Y = np.clip(np.ceil((birth + 30) / 5) * 5, 1950, 2015).astype(int)
    age_at = Y - birth
    band_lo = np.clip((age_at - 5) // 10 * 10 + 5, 25, 55)   # 25,35,45,55
    cat = df.educ.map(EDUC_TO_BL).to_numpy()
    blk = bl.set_index(["country", "year", "agefrom"])
    lut = {}
    for (c, y, a), row in blk.iterrows():
        cs = np.array([row[f"c{k}"] for k in range(7)])
        below = np.concatenate([[0.0], np.cumsum(cs)[:-1]])
        lut[(c, y, a)] = 100.0 * (below + 0.5 * cs)
    origin = df.origin.to_numpy()
    for i in np.flatnonzero(g1):
        name = BL_NAME.get(int(origin[i]))
        if name is None:
            continue
        v = lut.get((name, int(Y[i]), int(band_lo[i])))
        if v is None or not np.isfinite(cat[i]):
            continue
        out[i] = v[int(cat[i])]
    return out


def wic_selection_pct(df: pd.DataFrame) -> np.ndarray:
    """Same mid-rank, in the WIC v3 2020 reconstruction of the same birth cohort."""
    import pyreadr
    if load.sha256_file(WIC_RDS) != WIC_SHA:
        raise SystemExit("[BLOCKED] WIC file hash changed")
    wic = list(pyreadr.read_r(str(WIC_RDS)).values())[0]
    wic = wic[(wic.year == 2020) & (wic.education != "Under 15")].copy()
    wic["lvl"] = wic.education.map(lambda e: 5 if "Post" in e or e in ("Bachelor", "Master and higher")
                                   else WIC_LEVELS.index(e))
    wic["a0"] = wic.age.str.extract(r"^(\d+)").astype(int)
    tab = wic.groupby(["name", "a0", "lvl"]).pop.sum().unstack("lvl").fillna(0.0)
    lut = {}
    for (name, a0), row in tab.iterrows():
        cs = row.reindex(range(6), fill_value=0.0).to_numpy()
        if cs.sum() <= 0:
            continue
        cs = cs / cs.sum()
        below = np.concatenate([[0.0], np.cumsum(cs)[:-1]])
        lut[(name, int(a0))] = 100.0 * (below + 0.5 * cs)
    out = np.full(len(df), np.nan)
    g1 = (df.gen == 1).to_numpy() & df.educ_ok.to_numpy() & (df.origin > 0).to_numpy()
    birth = (df.year - df.age - 1).to_numpy()
    a0 = np.clip((2020 - birth) // 5 * 5, 25, 100)
    cat = df.educ.map(EDUC_TO_WIC).to_numpy()
    origin = df.origin.to_numpy()
    for i in np.flatnonzero(g1):
        o = int(origin[i])
        name = WIC_OVERRIDE.get(o, BL_NAME.get(o))
        v = lut.get((name, int(a0[i]))) if name else None
        if v is None or not np.isfinite(cat[i]):
            continue
        out[i] = v[int(cat[i])]
    return out


def origin_table(df: pd.DataFrame, labels: dict) -> list[dict]:
    ref = df.ref.to_numpy()
    rows = []
    specs = {
        "all": (np.ones(len(df), bool), np.ones(len(df), bool)),
        "g1_1994_2004__g2_2015_2025": ((df.year <= 2004).to_numpy(), (df.year >= 2015).to_numpy()),
        "g2_both_parents_foreign": (np.ones(len(df), bool), (df.nativity == 4).to_numpy()),
        "g2_2015_2025": (np.ones(len(df), bool), (df.year >= 2015).to_numpy()),
    }
    g2n = df.loc[df.gen == 2].groupby("origin").size()
    origins = [o for o, n in g2n.items() if o > 0 and n >= MIN_G2]
    for spec, (m1, m2) in specs.items():
        ref_share = df.loc[ref].groupby("band").w.sum() / df.loc[ref].w.sum()
        for o in origins:
            isg1 = (df.gen == 1).to_numpy() & (df.origin == o).to_numpy() & m1
            isg2 = (df.gen == 2).to_numpy() & (df.origin == o).to_numpy() & m2
            row = {"spec": spec, "origin_code": int(o),
                   "origin": ORIGIN_NAME.get(int(o), labels.get(int(o), str(o))),
                   "n_g1": int(isg1.sum()), "n_g2": int(isg2.sum())}
            for gen, mk in (("g1", isg1), ("g2", isg2)):
                for var in ("p_edu", "p_earn", "p_edu_sex", "p_earn_sex", "p_inctot"):
                    mm = mk & np.isfinite(df[var].to_numpy())
                    if mm.sum() < 20:
                        row[f"{gen}_{var}"], row[f"{gen}_{var}_se"] = np.nan, np.nan
                        continue
                    ws = std_weights(df, mm, ref_share)
                    m, se = wmean_se(df.loc[mm, var].to_numpy(), ws)
                    row[f"{gen}_{var}"], row[f"{gen}_{var}_se"] = m, se
                    if var == "p_edu" and spec == "all":
                        rm, _ = wmean_se(df.loc[mm, var].to_numpy(), df.loc[mm, "w"].to_numpy())
                        row[f"{gen}_{var}_raw"] = rm
                if gen == "g1":
                    for col in ("p_sel", "p_sel_bl", "p_sel_wic"):
                        mm = mk & np.isfinite(df[col].to_numpy())
                        if mm.sum() >= 20:
                            ws = std_weights(df, mm, ref_share)
                            m, se = wmean_se(df.loc[mm, col].to_numpy(), ws)
                            row[f"g1_{col}"], row[f"g1_{col}_se"] = m, se
                        else:
                            row[f"g1_{col}"], row[f"g1_{col}_se"] = np.nan, np.nan
            rows.append(row)
    return rows


def wls(x, y, w):
    X = np.column_stack([np.ones_like(x), x])
    W = w / w.sum()
    beta = np.linalg.solve(X.T @ (X * W[:, None]), X.T @ (W * y))
    return beta


def fit(tab: pd.DataFrame, xcol: str, ycol: str, rng: np.random.Generator, weight: str = "n_g2",
        noise: bool = False) -> dict:
    """WLS across origins; 95% interval from resampling origins (the residual spread already
    carries each origin mean's sampling error, so no extra noise is added by default)."""
    t = tab.dropna(subset=[xcol, ycol])
    t = t[t.n_g1 >= MIN_G1]
    x, y = t[xcol].to_numpy(), t[ycol].to_numpy()
    w = t[weight].to_numpy(dtype=float) if weight else np.ones(len(t))
    b = wls(x, y, w)
    sx = t.get(f"{xcol}_se", pd.Series(np.zeros(len(t)))).to_numpy()
    sy = t.get(f"{ycol}_se", pd.Series(np.zeros(len(t)))).to_numpy()
    draws = np.empty((NBOOT, 2))
    for k in range(NBOOT):
        idx = rng.integers(0, len(t), len(t))
        xb, yb = x[idx], y[idx]
        if noise:
            xb = xb + rng.normal(0, 1, len(idx)) * np.nan_to_num(sx[idx])
            yb = yb + rng.normal(0, 1, len(idx)) * np.nan_to_num(sy[idx])
        try:
            draws[k] = wls(xb, yb, w[idx])
        except np.linalg.LinAlgError:
            draws[k] = np.nan
    lo, hi = np.nanpercentile(draws[:, 1], [2.5, 97.5])
    ilo, ihi = np.nanpercentile(draws[:, 0], [2.5, 97.5])
    # reliability of the x means across origins (errors-in-variables)
    vx = np.average((x - np.average(x, weights=w)) ** 2, weights=w)
    rel = float(1 - np.average(np.nan_to_num(sx) ** 2, weights=w) / vx) if vx > 0 else np.nan
    resid = y - (b[0] + b[1] * x)
    r2 = 1 - np.average(resid ** 2, weights=w) / np.average((y - np.average(y, weights=w)) ** 2, weights=w)
    return {"n_origins": len(t), "slope": float(b[1]), "slope_lo": float(lo), "slope_hi": float(hi),
            "intercept": float(b[0]), "intercept_lo": float(ilo), "intercept_hi": float(ihi),
            "r2_weighted": float(r2), "x_reliability": rel,
            "slope_disattenuated": float(b[1] / rel) if rel and rel > 0 else np.nan,
            "_resid": dict(zip(t.origin, resid)), "_t": t}


def main() -> int:
    DERIVED.mkdir(exist_ok=True)
    audit = {"cps_sha256": load.check_manifest()}
    print("[load] frame + percentiles", flush=True)
    df = prepare()
    print(f"       {len(df):,} adults; reference n {int(df.ref.sum()):,}", flush=True)

    print("[gate] ladder 178 Mexican G2 no-HS gap", flush=True)
    audit["gate_ladder178"] = gate_ladder178(df)
    print("       ", audit["gate_ladder178"], flush=True)
    if audit["gate_ladder178"]["status"] != "PASS":
        raise SystemExit("[BLOCKED] ladder 178 gate failed")

    # sanity: the reference's own mean percentile is 50 in every spec
    r = df.ref.to_numpy()
    audit["reference_mean_pct"] = {v: float(np.average(df.loc[r, v].dropna(),
                                                        weights=df.loc[r & df[v].notna().to_numpy(), "w"]))
                                   for v in ("p_edu", "p_earn", "p_edu_sex", "p_earn_sex")}

    print("[task1] distributions and tails", flush=True)
    dist, tail = task1(df)
    write_csv(DERIVED / "percentile_distribution.csv", dist)
    write_csv(DERIVED / "tail_share.csv", tail)

    print("[task3] Barro-Lee origin selection percentile", flush=True)
    bl = barro_lee()
    df["p_sel_bl"] = origin_selection_pct(df, bl)
    df["p_sel_wic"] = wic_selection_pct(df)
    # main selection axis: Barro-Lee cohort-matched where the origin is in Barro-Lee,
    # the WIC 2020 reconstruction otherwise (Nigeria, Lebanon, Samoa)
    bl_origins = {o for o, n in BL_NAME.items() if n in set(bl.country)}
    df["p_sel"] = np.where(df.origin.isin(bl_origins), df.p_sel_bl, df.p_sel_wic)
    missing_bl = sorted({BL_NAME[o] for o in BL_NAME} - set(bl.country))
    audit["barro_lee"] = {"sha256": BL_SHA, "names_not_in_file": missing_bl,
                          "g1_with_selection_pct": int(np.isfinite(df.p_sel).sum()),
                          "g1_total_educ_ok": int(((df.gen == 1) & df.educ_ok).sum())}

    print("[task2] origin table", flush=True)
    labels = load.ddi_labels("BPL")
    tab = pd.DataFrame(origin_table(df, labels))
    tab.to_csv(DERIVED / "origin_curve.csv", index=False, float_format="%.6g", lineterminator="\n")

    print("[fit] slopes", flush=True)
    rng = np.random.default_rng(SEED)
    main_t = tab[tab.spec == "all"].copy()
    slope_rows, resid = [], {}

    def add(name, t, x, y, weight="n_g2", note="", keep_resid=False):
        f = fit(t, x, y, rng, weight)
        if keep_resid:
            resid[name] = f["_resid"]
        slope_rows.append({"spec": name, "x": x, "y": y, "weight": weight or "equal",
                           **{k: v for k, v in f.items() if not k.startswith("_")}, "note": note})
        return f

    f_edu = add("G1->G2 education, main", main_t, "g1_p_edu", "g2_p_edu", keep_resid=True)
    f_earn = add("G1->G2 earnings, main", main_t, "g1_p_earn", "g2_p_earn", keep_resid=True)
    add("G1->G2 education, age x sex x year cells", main_t, "g1_p_edu_sex", "g2_p_edu_sex")
    add("G1->G2 earnings, age x sex x year cells", main_t, "g1_p_earn_sex", "g2_p_earn_sex")
    add("G1->G2 total income", main_t, "g1_p_inctot", "g2_p_inctot")
    add("G1 education -> G2 earnings", main_t, "g1_p_edu", "g2_p_earn")
    add("G1->G2 education, unweighted", main_t, "g1_p_edu", "g2_p_edu", weight=None)
    add("G1->G2 earnings, unweighted", main_t, "g1_p_earn", "g2_p_earn", weight=None)
    add("G1->G2 education, not age-standardised", main_t, "g1_p_edu_raw", "g2_p_edu_raw")
    for spec in ("g1_1994_2004__g2_2015_2025", "g2_both_parents_foreign", "g2_2015_2025"):
        t = tab[tab.spec == spec]
        add(f"G1->G2 education, {spec}", t, "g1_p_edu", "g2_p_edu")
        add(f"G1->G2 earnings, {spec}", t, "g1_p_earn", "g2_p_earn")
    # task 3: origin selection axis
    add("origin selection -> G1 US education", main_t, "g1_p_sel", "g1_p_edu", keep_resid=True)
    add("origin selection -> G2 US education", main_t, "g1_p_sel", "g2_p_edu", keep_resid=True)
    add("origin selection -> G2 US earnings", main_t, "g1_p_sel", "g2_p_earn")
    nomex = main_t[main_t.origin_code != 20000]
    add("origin selection -> G1 US education, without Mexico", nomex, "g1_p_sel", "g1_p_edu")
    add("origin selection -> G2 US education, without Mexico", nomex, "g1_p_sel", "g2_p_edu")
    add("origin selection (Barro-Lee only) -> G2 US education", main_t, "g1_p_sel_bl", "g2_p_edu")
    add("origin selection (WIC 2020 only) -> G2 US education", main_t, "g1_p_sel_wic", "g2_p_edu")
    add("origin selection (WIC 2020 only) -> G1 US education", main_t, "g1_p_sel_wic", "g1_p_edu")
    # task 6: nonlinearity and leave-one-out
    t = main_t[main_t.n_g1 >= MIN_G1].dropna(subset=["g1_p_edu", "g2_p_edu"])
    for x, y, lab in (("g1_p_edu", "g2_p_edu", "education"), ("g1_p_earn", "g2_p_earn", "earnings")):
        tt = t.dropna(subset=[x, y])
        med = 50.0
        add(f"G1->G2 {lab}, origins with G1 below white median", tt[tt[x] < med], x, y)
        add(f"G1->G2 {lab}, origins with G1 at/above white median", tt[tt[x] >= med], x, y)
        sel_med = tt.g1_p_sel.median()
        add(f"G1->G2 {lab}, low origin-selection half", tt[tt.g1_p_sel < sel_med], x, y)
        add(f"G1->G2 {lab}, high origin-selection half", tt[tt.g1_p_sel >= sel_med], x, y)
        add(f"G1->G2 {lab}, without Mexico", tt[tt.origin_code != 20000], x, y)
        nm = tt[tt.origin_code != 20000]
        add(f"G1->G2 {lab}, origins with G1 below white median, without Mexico", nm[nm[x] < med], x, y)
        tt = tt.assign(sqrt_n_g2=np.sqrt(tt.n_g2))
        add(f"G1->G2 {lab}, sqrt(n) weights", tt, x, y, weight="sqrt_n_g2")
        add(f"G1->G2 {lab}, without Mexico, India, China, Philippines", tt[~tt.origin_code.isin(
            [20000, 52100, 50000, 51500])], x, y)
    # multiple regression: does origin selection add to G1 US position? (point estimates)
    mr = []
    for y in ("g2_p_edu", "g2_p_earn"):
        tt = t.dropna(subset=["g1_p_edu", "g1_p_sel", y])
        X = np.column_stack([np.ones(len(tt)), tt.g1_p_edu, tt.g1_p_sel])
        w = tt.n_g2.to_numpy(float)
        b = np.linalg.solve(X.T @ (X * w[:, None]), X.T @ (w * tt[y].to_numpy()))
        bs = []
        for _ in range(NBOOT):
            idx = rng.integers(0, len(tt), len(tt))
            Xb, wb, yb = X[idx], w[idx], tt[y].to_numpy()[idx]
            bs.append(np.linalg.lstsq(Xb * np.sqrt(wb)[:, None], yb * np.sqrt(wb), rcond=None)[0])
        bs = np.array(bs)
        mr.append({"y": y, "n_origins": len(tt), "b_g1_us_edu": b[1],
                   "b_g1_us_edu_ci": [float(v) for v in np.percentile(bs[:, 1], [2.5, 97.5])],
                   "b_origin_selection": b[2],
                   "b_origin_selection_ci": [float(v) for v in np.percentile(bs[:, 2], [2.5, 97.5])]})
    audit["multiple_regression_g2_on_g1us_and_selection"] = mr
    # leave-one-out on the main slopes
    loo = {}
    for name, f in (("education", f_edu), ("earnings", f_earn)):
        tt = f["_t"]
        x = "g1_p_edu" if name == "education" else "g1_p_earn"
        y = "g2_p_edu" if name == "education" else "g2_p_earn"
        vals = {}
        for o in tt.origin:
            s = tt[tt.origin != o]
            vals[o] = float(wls(s[x].to_numpy(), s[y].to_numpy(), s.n_g2.to_numpy(float))[1])
        lo_o, hi_o = min(vals, key=vals.get), max(vals, key=vals.get)
        loo[name] = {"min": [lo_o, vals[lo_o]], "max": [hi_o, vals[hi_o]], "full": f["slope"]}
    audit["leave_one_out"] = loo
    write_csv(DERIVED / "slopes.csv", slope_rows)

    # focus origins relative to the line
    focus = []
    for o, nm in FOCUS.items():
        row = main_t[main_t.origin_code == o]
        if row.empty:
            continue
        r0 = row.iloc[0]
        focus.append({"origin": nm, "n_g1": int(r0.n_g1), "n_g2": int(r0.n_g2),
                      "g1_p_sel": r0.g1_p_sel, "g1_p_edu": r0.g1_p_edu, "g2_p_edu": r0.g2_p_edu,
                      "pred_g2_p_edu": f_edu["intercept"] + f_edu["slope"] * r0.g1_p_edu,
                      "resid_edu": resid["G1->G2 education, main"].get(r0.origin, np.nan),
                      "g1_p_earn": r0.g1_p_earn, "g2_p_earn": r0.g2_p_earn,
                      "pred_g2_p_earn": f_earn["intercept"] + f_earn["slope"] * r0.g1_p_earn,
                      "resid_earn": resid["G1->G2 earnings, main"].get(r0.origin, np.nan)})
    base_t = main_t[main_t.n_g1 >= MIN_G1]
    for row in focus:
        for x, y, key in (("g1_p_edu", "g2_p_edu", "edu"), ("g1_p_earn", "g2_p_earn", "earn")):
            s_ = base_t[base_t.origin != row["origin"]].dropna(subset=[x, y])
            b = wls(s_[x].to_numpy(), s_[y].to_numpy(), s_.n_g2.to_numpy(float))
            row[f"loo_pred_g2_{key}"] = float(b[0] + b[1] * row[f"g1_p_{key}"])
            row[f"loo_resid_{key}"] = float(row[f"g2_p_{key}"] - row[f"loo_pred_g2_{key}"])
    write_csv(DERIVED / "focus_origins.csv", focus)
    (DERIVED / "cps_audit.json").write_text(json.dumps(audit, indent=2, default=float) + "\n")
    print(json.dumps(audit, indent=1, default=float)[:3000])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
