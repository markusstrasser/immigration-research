"""K-12 capital per pupil where the Mexican-origin group's pupils enroll: a district perpetual inventory.

The adopted main case (oct16) charges K-12 capital (a real return on BEA's K-12 stock, plus the depreciation inside
the school line) on the account's school key. That key prices each pupil at its state's average CURRENT spending per
pupil (account_embedded_price.json: R_embedded = 0.954), so the case's implied capital per group pupil is national
capital per pupil times that current-spending relative, not times a capital relative. This lane measures the capital
relative from Census F-33 district capital outlay, FY1992-FY2024, and applies it as a relative factor to the case.

Steps:
  1. Read F-33 all-items district files FY1992-FY1999 (this lane's acquire.py, _cache/f33_pre2000; FY1993-1994 are
     survey years whose reported rows are used unweighted) and FY2000-FY2024 (school_dilution_2026_09_24/_cache/f33;
     FY2022 from the xlsx conversion). J99 starts in FY2000 and is 0 before. Items (FY2015 documentation; FY2024 form Part III): F12 construction, G15 land and existing
     structures, K09 instructional equipment, K10 other equipment, K11 nonspecified equipment, J99 state payment on
     behalf of the LEA for capital outlay; TCAPOUT = F12 + G15 + K09 + K10 + K11 + J99 (gated per row).
  2. Deflate F12 by BEA's state and local educational structures price (FAAt705/FAAt706 line 62) and equipment by the
     state and local equipment price (line 56), fiscal-year means of calendar years t-1 and t, to FY2024 prices.
     Depreciate geometrically at BEA's implied 2024 rates (line 62: D / average stock; line 56 likewise), mid-year
     convention, to the end of FY2024 (mid-2024, BEA's 2024 average stock). G15 is cumulated at CPI-U with no
     depreciation and no real appreciation: a lower bound on recent land.
  3. Pre-FY1992 vintages: BEA's K-12 structures vintages (capital_return lane's PIM weights x K-12 key) give the pre-
     FY1992 share pi of K-12 structures. National pre-FY1992 stock = pi / (1 - pi) x this lane's national FY1992-2024
     PIM (BEA's vintage mix on the F-33 level; the BEA-level variant is reported). Allocated to districts by
     (a) FY1992 enrollment, (b) FY1992 enrollment x the district's own FY1992-1996 real construction per pupil over
     national. Equipment before FY1992 is a steady state at the FY1992 real level (nothing survives 33 years at 22%).
     The same inventory started at FY2000 (arms on FY2000 enrollment and FY2000-2004 intensity) is a sensitivity.
  4. Districts chain by NCES ID to FY2024. Outlay of IDs absent in FY2024 (merged, renumbered) is dropped in the
     primary run and reallocated within its state by FY2024 enrollment in a sensitivity.
  5. Weights: school_cost_where_enrolled_2026_09_24/weighting.py build(), unchanged (CCD 2023-24 Hispanic K-12
     pupils x the district's ACS Mexican share of Hispanics, raked to the state's ACS pupil share). Three families as
     there: C district ratio (the brief's literal R_K), A the account's own CPS state mix at state capital per pupil
     times the within-state factor, B the CCD state mix. The applied factor is F_A = R_K^A / R_embedded^A: capital per
     pupil relative over the current-spending relative the case's key already embeds, on the same pupils.
  6. Dollars: case_base.cjs reads the oct16 K-12 capital return at the one rate (2.081%) at both end specifications
     ($10.94bn, every population part). Depreciation base: BEA-basis K-12 depreciation (structures 48.7, equipment
     15.0) x the same effective key. Structures and equipment take their own factors; nothing is adopted.

    OPENBLAS_NUM_THREADS=1 uv run --no-project python3 \
      infra/immigration-fiscal/school_capital_where_enrolled_2026_10_24/build.py
"""
from __future__ import annotations

import csv
import hashlib
import json
import subprocess
import sys
import warnings

sys.dont_write_bytecode = True
from pathlib import Path  # noqa: E402

import numpy as np  # noqa: E402
import openpyxl  # noqa: E402
import pandas as pd  # noqa: E402

HERE = Path(__file__).resolve().parent
FISCAL = HERE.parent
ROOT = FISCAL.parents[1]
OUT = HERE / "derived"
F33_DIR = FISCAL / "school_dilution_2026_09_24" / "_cache" / "f33"
PRE_DIR = HERE / "_cache" / "f33_pre2000"      # acquire.py: FY1992-FY1999
CPI_FILE = FISCAL / "school_dilution_2026_09_24" / "_cache" / "cpiaucsl_monthly.csv"
CAP = FISCAL / "school_capital_return_2026_09_26"
BEA_FA = CAP / "_cache" / "fa_Section7All_xls.xlsx"
KEY_CSV = CAP / "derived" / "k12_share_key.csv"
NAT_CSV = CAP / "derived" / "national_k12_capital.csv"
BRIDGE_CSV = CAP / "derived" / "cash_accrual_bridge_national.csv"
SCL = FISCAL / "school_cost_where_enrolled_2026_09_24"
EMBED = SCL / "derived" / "account_embedded_price.json"
ACCT = SCL / "derived" / "account_pupils_by_state.csv"
R_OTHER = SCL / "derived" / "r_other_concepts.csv"
CASE_BASE = OUT / "case_base.json"
NODE_SCRIPT = HERE / "case_base.cjs"

START = 1992                  # first measured F-33 district year (acquire.py); FY1992 is the earliest all-items file
SENS_START = 2000             # the FY2000-start inventory, kept as a sensitivity
YEARS = list(range(START, 2025))
SAMPLE_YEARS = (1993, 1994)   # survey years: small districts sampled; reported rows are used unweighted
ITEMS = ["F12", "G15", "K09", "K10", "K11", "J99", "TCAPOUT", "V33"]
EQUIP = ["K09", "K10", "K11"]
WEIGHTS = ["mexican_district_share", "mexican_state_share", "hispanic"]
MAIN_W = "mexican_district_share"
HEADLINE_BN = None            # read from case_base.json (the v9 band)
CHAIN_MIN = 0.98              # share of FY1992-2024 real construction chained to an FY2024 ID
COVER_MIN = 0.85              # share of CCD group pupils in districts with a capital price
GATES: list[dict] = []


def gate(name: str, ok: bool, detail: str) -> None:
    GATES.append({"gate": name, "pass": bool(ok), "detail": detail})
    print(f"  {'✓' if ok else '✗'} {name}: {detail}")


def sha(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def write_csv(name: str, df: pd.DataFrame) -> None:
    df.to_csv(OUT / name, index=False, lineterminator="\n", float_format="%.6f")


# ------------------------------------------------------------------ 1. F-33 panel
def f33_path(y: int) -> Path:
    if y < 2000:
        return PRE_DIR / ("elsec99_xls.csv" if y == 1999 else f"elsec{y % 100:02d}.txt")
    return F33_DIR / (f"elsec{y % 100:02d}_xlsx.csv" if y == 2022 else f"elsec{y % 100:02d}.txt")


def read_year(y: int) -> pd.DataFrame:
    want = {"STATE", "NCESID", "NAME"} | set(ITEMS)
    with warnings.catch_warnings():
        # Data rows carry one trailing empty field beyond the header; index_col=False keeps alignment.
        warnings.simplefilter("ignore", pd.errors.ParserWarning)
        d = pd.read_csv(f33_path(y), dtype=str, index_col=False, encoding="latin-1", keep_default_na=False,
                        usecols=lambda c: c in want)
    missing = set(ITEMS) - set(d.columns)
    if y < 2000 and missing == {"J99"}:
        d["J99"] = "0"           # item J99 (state on-behalf capital outlay) starts in FY2000
        missing = set()
    if missing:
        raise SystemExit(f"[BLOCKED] FY{y} lacks {sorted(missing)}")
    for c in ITEMS:
        d[c] = pd.to_numeric(d[c], errors="coerce").fillna(0.0)
    d["id"] = d.NCESID.str.strip()
    d["year"] = y
    return d


def panel() -> pd.DataFrame:
    frames, ident = [], []
    for y in YEARS:
        d = read_year(y)
        gap = (d.TCAPOUT - d[["F12", "G15", "K09", "K10", "K11", "J99"]].sum(axis=1)).abs()
        ident.append((y, float(gap.max()), int((d[ITEMS] < 0).sum().sum())))
        frames.append(d)
    worst = max(g for _, g, _ in ident)
    gate("tcapout_identity_every_row", worst <= 2.0,
         f"max |TCAPOUT - (F12+G15+K09+K10+K11+J99)| = {worst:.0f} thousand dollars over FY{START}-2024 (rounding)")
    neg = sum(n for _, _, n in ident)
    p = pd.concat(frames, ignore_index=True)
    for c in ITEMS:
        p[c] = p[c].clip(lower=0.0) * (1.0 if c == "V33" else 1000.0)   # thousands of dollars -> dollars
    p["valid_id"] = p.id.str.fullmatch(r"\d{7}")
    bad_share = p.loc[~p.valid_id, "F12"].sum() / p.F12.sum()
    gate("negative_items_clipped", neg <= 5, f"{neg} negative capital/enrollment cells set to 0")
    p = p[p.valid_id].copy()
    p["fips"] = p.id.str[:2].astype(int)
    p = p.groupby(["id", "year"], as_index=False).agg(
        {**{c: "sum" for c in ITEMS}, "fips": "first", "NAME": "last", "STATE": "first"})
    p["equip"] = p[EQUIP].sum(axis=1)
    return p, float(bad_share)


# ------------------------------------------------------------------ 2. BEA prices and rates
def bea_table(path: Path, sheet: str) -> tuple[dict, dict]:
    wb = openpyxl.load_workbook(path, read_only=True)
    rows = list(wb[sheet].iter_rows(values_only=True))
    head = [i for i, r in enumerate(rows) if r and r[0] == "Line"][0]
    years = [int(y) for y in rows[head][3:] if y is not None]
    data, labels = {}, {}
    for r in rows[head + 1:]:
        if isinstance(r[0], int) or (isinstance(r[0], str) and r[0].strip().isdigit()):
            line = int(r[0])
            labels[line] = str(r[1]).strip()
            data[line] = {y: float(v) for y, v in zip(years, r[3:]) if isinstance(v, (int, float))}
    return data, labels


def bea() -> dict:
    K, kl = bea_table(BEA_FA, "FAAt701-A")
    D, dl = bea_table(BEA_FA, "FAAt703-A")
    INV, il = bea_table(BEA_FA, "FAAt705-A")
    Q, ql = bea_table(BEA_FA, "FAAt706-A")
    for lab, where in ((kl, "701"), (dl, "703"), (il, "705"), (ql, "706")):
        for line, text in ((55, "State and local"), (56, "Equipment"), (62, "Educational"), (73, "Software")):
            if not lab[line].startswith(text):
                raise SystemExit(f"[BLOCKED] FAAt{where} line {line} is '{lab[line]}', expected '{text}'")
    price = {}
    for name, line in (("structures", 62), ("equipment", 56)):
        cy = {t: INV[line][t] / Q[line][t] for t in Q[line] if t in INV[line] and Q[line][t] > 0}
        price[name] = {y: (cy[y - 1] + cy[y]) / 2 for y in YEARS}      # school fiscal year July (y-1) - June y
    rate = {
        "structures": D[62][2024] / ((K[62][2023] + K[62][2024]) / 2),
        "equipment": D[56][2024] / ((K[56][2023] + K[56][2024]) / 2),
        "equipment_2023": D[56][2023] / ((K[56][2022] + K[56][2023]) / 2),
        "equipment_software": (D[56][2024] + D[73][2024]) / ((K[56][2023] + K[56][2024] + K[73][2023] + K[73][2024]) / 2),
    }
    return {"price": price, "rate": rate}


def cpi_fy() -> dict:
    c = pd.read_csv(CPI_FILE, parse_dates=["observation_date"])
    c["fy"] = c.observation_date.dt.year + (c.observation_date.dt.month >= 7).astype(int)
    g = c.groupby("fy").CPIAUCSL.agg(["mean", "size"])
    g = g[g["size"] == 12]["mean"]
    return {y: float(g[y]) for y in YEARS}


# ------------------------------------------------------------------ 3-4. perpetual inventory by district
def inventory(p: pd.DataFrame, b: dict, cpi: dict, start: int) -> tuple[pd.DataFrame, pd.DataFrame, dict]:
    """District PIM from FY`start` to FY2024 plus the pre-`start` stock in arms a and b."""
    p = p[p.year >= start].copy()
    ds, de = b["rate"]["structures"], b["rate"]["equipment"]
    ps, pe = b["price"]["structures"], b["price"]["equipment"]
    age = 2024 - p.year
    p["real_f12"] = p.F12 * p.year.map(lambda y: ps[2024] / ps[y])
    p["real_eq"] = p.equip * p.year.map(lambda y: pe[2024] / pe[y])
    p["ks"] = p.real_f12 * (1 - ds) ** age * (1 - ds / 2)
    p["ke"] = p.real_eq * (1 - de) ** age * (1 - de / 2)
    p["g15_real"] = p.G15 * p.year.map(lambda y: cpi[2024] / cpi[y])
    ids24 = set(p.id[p.year == 2024])
    p["chained"] = p.id.isin(ids24)

    # national flows, every unit with a 7-digit ID
    nat = p.groupby("year").agg(units=("id", "size"), f12=("F12", "sum"), g15=("G15", "sum"), equip=("equip", "sum"),
                                j99=("J99", "sum"), v33=("V33", "sum"), real_f12=("real_f12", "sum"), real_eq=("real_eq", "sum"),
                                ks=("ks", "sum"), ke=("ke", "sum")).reset_index()
    ch = p[p.chained].groupby("year").agg(real_f12_chained=("real_f12", "sum"), v33_chained=("V33", "sum")).reset_index()
    nat = nat.merge(ch, on="year")
    nat["structures_price_fy"] = nat.year.map(ps)
    nat["equipment_price_fy"] = nat.year.map(pe)
    nat["cpi_fy"] = nat.year.map(cpi)
    nat["chained_share_real_f12"] = nat.real_f12_chained / nat.real_f12
    nat["chained_share_v33"] = nat.v33_chained / nat.v33

    by = p[p.chained].groupby("id").agg(ks_post=("ks", "sum"), ke_post=("ke", "sum"), g15=("g15_real", "sum"),
                                        fips=("fips", "first")).reset_index()
    y24 = p[p.year == 2024].set_index("id")
    by["V33_2024"] = by.id.map(y24.V33)
    by["NAME"] = by.id.map(y24.NAME)
    v_state = by.groupby("fips").V33_2024.transform("sum")

    def realloc(un_by_fips: pd.Series) -> pd.Series:
        """Spread a state's unchained amount over its FY2024 districts by FY2024 enrollment."""
        return (by.fips.map(un_by_fips).fillna(0.0) * by.V33_2024 / v_state.where(v_state > 0)).fillna(0.0)

    # state reallocation of unchained flows, by FY2024 enrollment (sensitivity)
    un = p[~p.chained].groupby("fips").agg(ks=("ks", "sum"), ke=("ke", "sum"), g15=("g15_real", "sum"))
    for c in ("ks", "ke", "g15"):
        by[f"{c}_realloc_add"] = realloc(un[c])
    lost_states = sorted(set(un.index) - set(by.fips[by.V33_2024 > 0]))

    # pre-`start` structures: BEA's vintage share on this lane's level. FY t runs July t-1 to June t.
    key = pd.read_csv(KEY_CSV)
    w = key.set_index("year")
    k12w = w.pim_weight_in_2024_stock * w.k12_share_central
    pre = k12w[k12w.index <= start - 2].sum() + 0.5 * k12w[start - 1]
    pi = float(pre / k12w.sum())
    natk = pd.read_csv(NAT_CSV).set_index("variant").loc["central"]
    ks_post_nat = float(nat.ks.sum())
    pre_level = {"proportional": pi / (1 - pi) * ks_post_nat, "bea_level": pi * float(natk.structures_avg2024_bn) * 1e9}
    # equipment before `start`: steady state at the start-year real level
    e0 = float(nat.loc[nat.year == start, "real_eq"].iloc[0])
    pre_e = e0 * (1 - de) ** (2024 - start + 1) * (1 - de / 2) / de

    y0 = p[p.year == start].set_index("id")
    early = p[p.year.between(start, start + 4)].groupby("id").agg(rf=("real_f12", "sum"), v=("V33", "sum"))
    nat_int = early.rf.sum() / early.v.sum()
    inten = (early.rf / early.v.where(early.v > 0)) / nat_int
    w_a = y0.V33
    w_b = (y0.V33 * inten.reindex(y0.index)).fillna(0.0)
    alloc = {"a": w_a / w_a.sum(), "b": w_b / w_b.sum()}       # shares over every start-year unit
    fips0 = pd.Series(y0.index.str[:2].astype(int), index=y0.index)
    unchained0 = ~y0.index.isin(ids24)
    for arm, sh in alloc.items():
        s = by.id.map(sh).fillna(0.0)
        s_un = sh[unchained0].groupby(fips0[unchained0]).sum()
        for lvl, tot in pre_level.items():
            by[f"ks_pre_{arm}_{lvl}"] = s * tot
            by[f"ks_pre_{arm}_{lvl}_realloc_add"] = realloc(s_un) * tot
        by[f"ke_pre_{arm}"] = s * pre_e
        by[f"ke_pre_{arm}_realloc_add"] = realloc(s_un) * pre_e
    info = {
        "start_fiscal_year": start, "rates": b["rate"], "pi_pre_start_share_of_k12_structures": pi,
        "pre_start_structures_bn": {k: v / 1e9 for k, v in pre_level.items()},
        "pre_start_equipment_bn": pre_e / 1e9, "national_post_start_structures_pim_bn": ks_post_nat / 1e9,
        "national_post_start_equipment_pim_bn": float(nat.ke.sum()) / 1e9,
        "national_g15_cumulative_cpi_bn": float(p.g15_real.sum()) / 1e9,
        "chained_share_real_f12": float(p.loc[p.chained, "real_f12"].sum() / p.real_f12.sum()),
        "chained_share_real_f12_before_2000": float(p.loc[p.chained & (p.year < 2000), "real_f12"].sum() / p.loc[p.year < 2000, "real_f12"].sum())
        if (p.year < 2000).any() else None,
        "chained_share_structures_stock_2024": float(p.loc[p.chained, "ks"].sum() / p.ks.sum()),
        "chained_share_start_enrollment": float(y0.V33[~unchained0].sum() / y0.V33.sum()),
        "unchained_states_without_fy2024_pupils": lost_states,
        "arm_b_intensity_weight_share_top_1pct_units": float(np.sort((w_b / w_b.sum()).to_numpy())[::-1][: max(1, len(w_b) // 100)].sum()),
        "bea_k12_central": {k: float(natk[k]) for k in ("structures_avg2024_bn", "equipment_software_avg2024_bn", "total_avg2024_bn",
                                                        "depreciation_structures_2024_bn", "depreciation_equipment_software_2024_nipa_basis_bn",
                                                        "depreciation_total_2024_bn")},
        "fy2024_construction_bn": float(nat.loc[nat.year == 2024, "f12"].iloc[0]) / 1e9,
        "fy2024_capital_outlay_items_bn": float(nat.loc[nat.year == 2024, ["f12", "g15", "equip", "j99"]].sum(axis=1).iloc[0]) / 1e9,
    }
    return by, nat, info


def concepts(by: pd.DataFrame, tag: str = "") -> dict[str, pd.Series]:
    """Per-pupil stocks (2024 dollars) by FY2024 NCES ID, for every arm. `post` = measured years, `pre` = before them."""
    e = by.V33_2024.where(by.V33_2024 > 0)
    c = {}
    for arm in ("a", "b"):
        for lvl in ("proportional", "bea_level"):
            sfx = "" if lvl == "proportional" else "_bea_level"
            c[f"structures_{arm}{sfx}"] = (by.ks_post + by[f"ks_pre_{arm}_{lvl}"]) / e
            c[f"structures_{arm}{sfx}_realloc"] = (by.ks_post + by.ks_realloc_add + by[f"ks_pre_{arm}_{lvl}"]
                                                   + by[f"ks_pre_{arm}_{lvl}_realloc_add"]) / e
        c[f"equipment_{arm}"] = (by.ke_post + by[f"ke_pre_{arm}"]) / e
        c[f"equipment_{arm}_realloc"] = (by.ke_post + by.ke_realloc_add + by[f"ke_pre_{arm}"] + by[f"ke_pre_{arm}_realloc_add"]) / e
        c[f"structures_pre_{arm}"] = by[f"ks_pre_{arm}_proportional"] / e
    c["structures_post"] = by.ks_post / e
    c["equipment_post"] = by.ke_post / e
    c["g15_cumulative"] = by.g15 / e
    c["g15_cumulative_realloc"] = (by.g15 + by.g15_realloc_add) / e
    return {f"{tag}{k}": pd.Series(v.to_numpy(), index=by.id) for k, v in c.items()}


# ------------------------------------------------------------------ 5. weights and ratios
def ratios(d: pd.DataFrame, col: str, W, acct: pd.DataFrame) -> dict:
    t = W.state_table(d.assign(valid=d.valid & d[col].notna()), col)
    out = {}
    nat_c = (t.W_all * t.P_all).sum() / t.W_all.sum()
    tp, npup = acct.target_pupils, acct.national_pupils
    ks = t.P_all.reindex(acct.index)
    for name in WEIGHTS:
        f = (t[f"P_{name}"] / t.P_all).reindex(acct.index).fillna(1.0)
        out[name] = {
            "C_district": W.ratio(t, name),
            "state_weighted": float((t[f"W_{name}"] * t.P_all).sum() / t[f"W_{name}"].sum() / nat_c),
            "A_account_state_mix": float(((tp * ks * f).sum() / tp.sum()) / ((npup * ks).sum() / npup.sum())),
            "A_state_mix_only": float(((tp * ks).sum() / tp.sum()) / ((npup * ks).sum() / npup.sum())),
            "B_ccd_state_mix": float(((t[f"W_{name}"] * t.P_all * (t[f"P_{name}"] / t.P_all).fillna(1.0)).sum() / t[f"W_{name}"].sum()) / nat_c),
        }
    out["_national_per_pupil"] = float(nat_c)
    out["_state_table"] = t
    return out


def calibration(info: dict) -> dict:
    bk = info["bea_k12_central"]
    pi = info["pi_pre_start_share_of_k12_structures"]
    post_bea = (1 - pi) * bk["structures_avg2024_bn"]
    ks, ke = info["national_post_start_structures_pim_bn"], info["national_post_start_equipment_pim_bn"]
    pre_s, pre_e = info["pre_start_structures_bn"], info["pre_start_equipment_bn"]
    return {
        "post_start_structures_f33_over_bea_same_vintages": ks / post_bea,
        "total_structures_f33_plus_bea_level_pre_over_bea": (ks + pre_s["bea_level"]) / bk["structures_avg2024_bn"],
        "total_capital_f33_proportional_over_bea": (ks + pre_s["proportional"] + ke + pre_e) / bk["total_avg2024_bn"],
        "equipment_f33_over_bea": (ke + pre_e) / bk["equipment_software_avg2024_bn"],
        "bea_post_start_k12_structures_bn": post_bea,
        "bea_k12_total_bn": bk["total_avg2024_bn"],
    }


def main() -> int:
    OUT.mkdir(exist_ok=True)
    print(f"[1] F-33 panel FY{START}-FY2024")
    p, bad_share = panel()
    b = bea()
    cpi = cpi_fy()
    print("[2] perpetual inventory")
    by, nat, info = inventory(p, b, cpi, START)
    by0, nat0, info0 = inventory(p, b, cpi, SENS_START)
    bridge = pd.read_csv(BRIDGE_CSV).set_index("item").value_bn_or_ratio
    gate("fy2024_construction_matches_capital_lane", abs(info["fy2024_construction_bn"] - float(bridge["  construction"])) < 1e-3,
         f"F12 FY2024 {info['fy2024_construction_bn']:.3f}bn vs Table 9 {float(bridge['  construction']):.3f}bn")
    gate("fy2024_outlay_matches_capital_lane", abs(info["fy2024_capital_outlay_items_bn"] - float(bridge["F-33 FY2024 capital outlay"])) < 1e-2,
         f"items sum {info['fy2024_capital_outlay_items_bn']:.3f}bn vs {float(bridge['F-33 FY2024 capital outlay']):.3f}bn")
    gate("structures_rate_is_capital_lane_1_83pct", 0.0178 < info["rates"]["structures"] < 0.0188,
         f"delta_s {info['rates']['structures']:.5f}")
    gate("equipment_rate_plausible", 0.08 < info["rates"]["equipment"] < 0.25, f"delta_e {info['rates']['equipment']:.5f}")
    gate("chain_coverage_real_construction", info["chained_share_real_f12"] >= CHAIN_MIN,
         f"{info['chained_share_real_f12']:.4f} of FY{START}-2024 real construction chains to an FY2024 ID (min {CHAIN_MIN}; "
         f"FY{START}-1999 alone {info['chained_share_real_f12_before_2000']:.4f}); {info['chained_share_structures_stock_2024']:.4f} "
         f"of the depreciated stock; non-7-digit IDs hold {bad_share:.4%} of F12")
    # survey years: the reported rows are a sample of small districts; measure what the sample leaves out
    v = nat.set_index("year").v33
    sample = {str(y): {"units": int(nat.set_index("year").units[y]), "v33_millions": float(v[y]) / 1e6,
                       "v33_shortfall_vs_1992_1995_mean": float(1 - v[y] / ((v[1992] + v[1995]) / 2))} for y in SAMPLE_YEARS}
    gate("survey_years_cover_most_pupils", all(s["v33_shortfall_vs_1992_1995_mean"] < 0.06 for s in sample.values()),
         "; ".join(f"FY{y} reported rows hold {1 - s['v33_shortfall_vs_1992_1995_mean']:.3f} of the 1992/1995 mean pupils" for y, s in sample.items()))

    calib, calib0 = calibration(info), calibration(info0)
    print(f"  ▸ national calibration: F-33 FY{START}-24 structures PIM / BEA same vintages = "
          f"{calib['post_start_structures_f33_over_bea_same_vintages']:.4f}; F-33 + pre-FY{START} at the proportional rule / "
          f"BEA K-12 ${calib['bea_k12_total_bn']:,.1f}bn = {calib['total_capital_f33_proportional_over_bea']:.4f} "
          f"(FY2000 start: {calib0['post_start_structures_f33_over_bea_same_vintages']:.4f})")
    gate("national_calibration_ratio_plausible", 0.6 <= calib["post_start_structures_f33_over_bea_same_vintages"] <= 1.5,
         f"F-33/BEA post-FY{START} K-12 structures {calib['post_start_structures_f33_over_bea_same_vintages']:.4f}; "
         f"equipment {calib['equipment_f33_over_bea']:.4f}")

    print("[3] district weights (school_cost_where_enrolled weighting.build)")
    sys.path.insert(0, str(SCL))
    import weighting as W  # noqa: E402
    d, _ = W.build()
    conc = {**concepts(by), **concepts(by0, "s2000_")}
    for k, s in conc.items():
        d[k] = d.LEAID.map(s)
    # reuse check: FY2024 capital outlay per pupil through this lane's read reproduces that lane's ratio
    tcap = p[p.year == 2024].set_index("id")
    d["capout_check"] = d.LEAID.map(tcap.TCAPOUT / tcap.V33.where(tcap.V33 > 0))
    acct = pd.read_csv(ACCT).set_index("fips")
    chk = ratios(d, "capout_check", W, acct)
    want = pd.read_csv(R_OTHER).set_index(["concept", "weighting"]).R[("pp_capout", MAIN_W)]
    gate("reuse_reproduces_school_cost_capital_outlay_ratio", abs(chk[MAIN_W]["C_district"] - want) < 5e-4,
         f"FY2024 capital outlay R {chk[MAIN_W]['C_district']:.6f} vs r_other_concepts {want:.6f}")
    has = d.valid & d["structures_a"].notna()
    coverage = {"group_pupils": float(d.w_mex_dist[has].sum() / d.w_mex_dist.sum()),
                "all_pupils": float(d.k12_all[has].sum() / d.k12_all.sum()),
                "f33_fy2024_pupils_in_chained_ids": float(by.V33_2024.sum() / p.loc[p.year == 2024, "V33"].sum())}
    gate("group_pupil_coverage", coverage["group_pupils"] >= COVER_MIN,
         f"{coverage['group_pupils']:.4f} of CCD group pupils and {coverage['all_pupils']:.4f} of all pupils sit in districts with a "
         f"capital price (min {COVER_MIN}); the rest take their state's mean, as in weighting.py")

    # current-spending relative on the account's key: the price the case already charges capital at
    emb = json.loads(EMBED.read_text())
    r_emb = emb["r_embedded_personal"]
    r_emb_check = float((acct.target_school_personal_bn.sum() / acct.target_pupils.sum())
                        / (acct.national_school_personal_bn.sum() / acct.national_pupils.sum()))
    gate("account_embedded_relative_reproduced", abs(r_emb_check - r_emb) < 1e-6, f"{r_emb_check:.9f} vs {r_emb:.9f}")

    print("[4] ratios")
    rows, R = [], {}
    for col in conc:
        rr = ratios(d, col, W, acct)
        R[col] = rr
        for name in WEIGHTS:
            for fam, val in rr[name].items():
                rows.append({"concept": col, "weighting": name, "family": fam, "R": val})
    rk = pd.DataFrame(rows)
    write_csv("r_k_by_concept.csv", rk)
    for c in ("structures_a", "structures_b", "equipment_a", "s2000_structures_a", "s2000_structures_b"):
        val = R[c][MAIN_W]["C_district"]
        gate(f"r_finite_{c}", np.isfinite(val) and 0.3 < val < 3.0, f"R_K {val:.4f}")

    # identity: arm total = stock-weighted mean of the measured and pre-measured relatives (exact for national means)
    def nat_pp(col):
        return R[col]["_national_per_pupil"]
    arm_order = {}
    for tag, start in (("", START), ("s2000_", SENS_START)):
        for arm in ("a", "b"):
            post, pre, tot = nat_pp(f"{tag}structures_post"), nat_pp(f"{tag}structures_pre_{arm}"), nat_pp(f"{tag}structures_{arm}")
            gp = lambda c: R[c][MAIN_W]["C_district"] * nat_pp(c)  # noqa: E731
            lhs = R[f"{tag}structures_{arm}"][MAIN_W]["C_district"]
            rhs = (gp(f"{tag}structures_post") + gp(f"{tag}structures_pre_{arm}")) / (post + pre)
            gate(f"{tag}arm_{arm}_decomposes_into_vintages", abs(lhs - rhs) < 1e-9 and abs(tot - post - pre) / tot < 1e-9,
                 f"start FY{start}: R {lhs:.6f} = vintage mix {rhs:.6f}")
        r_pa, r_pb = R[f"{tag}structures_pre_a"][MAIN_W]["C_district"], R[f"{tag}structures_pre_b"][MAIN_W]["C_district"]
        arm_order[f"FY{start}"] = {"pre_relative_arm_a": r_pa, "pre_relative_arm_b": r_pb, "b_ge_a": bool(r_pb >= r_pa),
                                   "post_relative": R[f"{tag}structures_post"][MAIN_W]["C_district"]}
        print(f"  ▸ start FY{start}: pre-start relative arm a {r_pa:.4f}, arm b {r_pb:.4f}; measured years "
              f"{arm_order[f'FY{start}']['post_relative']:.4f}")

    # the FY1992-1999 vintages alone: the measured years of the FY1992 inventory minus those of the FY2000 one
    # (same districts, same depreciation to 2024, so the difference is exactly the 1992-1999 flows)
    n92, n00 = nat_pp("structures_post"), nat_pp("s2000_structures_post")
    g92, g00 = R["structures_post"][MAIN_W]["C_district"] * n92, R["s2000_structures_post"][MAIN_W]["C_district"] * n00
    v9299 = {"national_per_pupil": n92 - n00, "relative_C": (g92 - g00) / (n92 - n00),
             "share_of_measured_stock": (n92 - n00) / n92}
    arm_order["vintages_FY1992_1999"] = v9299
    print(f"  ▸ FY1992-1999 vintages alone: relative {v9299['relative_C']:.4f}, ${v9299['national_per_pupil']:,.0f} a pupil "
          f"({v9299['share_of_measured_stock']:.3f} of the FY1992-2024 stock)")

    print("[5] dollars on oct16")
    r = subprocess.run(["node", "--max-old-space-size=4096", str(NODE_SCRIPT), str(CASE_BASE)], cwd=ROOT,
                       capture_output=True, text=True)
    if r.returncode:
        raise SystemExit(f"[BLOCKED] case_base.cjs rc={r.returncode}: {r.stderr[-2000:]}")
    print("  " + r.stdout.strip())
    cb = json.loads(CASE_BASE.read_text())
    band = cb["band_bn"]
    base = {}
    for end in ("low", "high"):
        xs = [x for x in cb["rows"] if x["end"] == end]
        base[end] = {"return_bn": float(np.mean([x["k12_return_at_one_rate_bn"] for x in xs])),
                     "effective_key": float(np.mean([x["effective_key"] for x in xs])),
                     "one_rate": xs[0]["one_rate"]}
        gate(f"case_base_methods_agree_{end}", np.ptp([x["k12_return_at_one_rate_bn"] for x in xs]) < 1e-9, "K-12 capital is method-free")
    bk = info["bea_k12_central"]
    sh_s = bk["structures_avg2024_bn"] / bk["total_avg2024_bn"]
    dep_s, dep_e = bk["depreciation_structures_2024_bn"], bk["depreciation_equipment_software_2024_nipa_basis_bn"]
    gate("case_stock_is_bea_k12_central", abs(cb["rows"][0]["stock_charged_bn"] - bk["total_avg2024_bn"]) < 1e-6,
         f"{cb['rows'][0]['stock_charged_bn']:.4f} vs {bk['total_avg2024_bn']:.4f}")

    def factors(arm: str, suffix: str, weighting: str, tag: str) -> dict:
        s = R[f"{tag}structures_{arm}{suffix}"][weighting]
        e = R[f"{tag}equipment_{arm}{'_realloc' if suffix.endswith('realloc') else ''}"][weighting]
        out = {}
        for label, fam, div in (("brief_literal_C", "C_district", 1.0), ("key_consistent_A", "A_account_state_mix", r_emb),
                                ("key_consistent_B", "B_ccd_state_mix", r_emb), ("state_weighted_literal", "state_weighted", 1.0)):
            fs, fe = s[fam] / div, e[fam] / div
            out[label] = {"structures": fs, "equipment": fe,
                          "stock_combined": fs * sh_s + fe * (1 - sh_s),
                          "depreciation_combined": (fs * dep_s + fe * dep_e) / (dep_s + dep_e)}
        return out

    drows, dollars = [], {}
    variants = [("a", "", ""), ("b", "", ""), ("a", "_realloc", ""), ("b", "_realloc", ""), ("a", "_bea_level", ""), ("b", "_bea_level", ""),
                ("a", "", "s2000_"), ("b", "", "s2000_")]
    for arm, suf, tag in variants:
        vname = "fy2000_start" if tag else (suf.strip("_") or "primary")
        for wname in WEIGHTS:
            for label, f in factors(arm, suf, wname, tag).items():
                rec = {"start_fiscal_year": SENS_START if tag else START, "pre_start_arm": arm, "variant": vname, "weighting": wname,
                       "factor": label, **{f"F_{k}": val for k, val in f.items()}}
                for end in ("low", "high"):
                    ret = base[end]["return_bn"]
                    dkey = base[end]["effective_key"]
                    d_ret = ret * (sh_s * (f["structures"] - 1) + (1 - sh_s) * (f["equipment"] - 1))
                    d_dep = dkey * (dep_s * (f["structures"] - 1) + dep_e * (f["equipment"] - 1))
                    rec[f"delta_return_{end}_bn"] = d_ret
                    rec[f"delta_depreciation_{end}_bn"] = d_dep
                    rec[f"delta_{end}_bn"] = d_ret + d_dep
                    rec[f"share_of_headline_{end}"] = (d_ret + d_dep) / band[0 if end == "low" else 1]
                drows.append(rec)
                dollars[(arm, vname, wname, label)] = rec
    write_csv("dollars.csv", pd.DataFrame(drows))

    # land (secondary): G15 cumulated at CPI, return only
    land = {}
    for tag, suf, lab in (("", "", "primary"), ("", "_realloc", "realloc"), ("s2000_", "", "fy2000_start")):
        g = R[f"{tag}g15_cumulative{suf}"][MAIN_W]
        L = (info0 if tag else info)["national_g15_cumulative_cpi_bn"]
        land[lab] = {
            "R_C_district": g["C_district"], "R_A_account_state_mix": g["A_account_state_mix"], "R_state_weighted": g["state_weighted"],
            "national_g15_cumulative_bn": L,
            "group_charge_key_consistent_bn": base["low"]["one_rate"] * L * base["low"]["effective_key"] * g["A_account_state_mix"] / r_emb,
            "group_charge_brief_literal_bn": base["low"]["one_rate"] * L * base["low"]["effective_key"] * g["C_district"],
        }

    # state breakdown, structures arm a
    t = R["structures_a"]["_state_table"]
    tb = R["structures_b"]["_state_table"]
    sb = pd.DataFrame({
        "fips": acct.index, "state": acct.state, "account_group_pupils": acct.target_pupils, "account_all_pupils": acct.national_pupils,
        "account_price_per_pupil": acct.target_school_personal_bn * 1e9 / acct.target_pupils,
        "structures_per_pupil_all_arm_a": t.P_all.reindex(acct.index).to_numpy(),
        "structures_per_pupil_group_arm_a": t[f"P_{MAIN_W}"].reindex(acct.index).to_numpy(),
        "structures_per_pupil_all_arm_b": tb.P_all.reindex(acct.index).to_numpy(),
        "structures_per_pupil_group_arm_b": tb[f"P_{MAIN_W}"].reindex(acct.index).to_numpy(),
        "measured_years_per_pupil_all": R["structures_post"]["_state_table"].P_all.reindex(acct.index).to_numpy(),
        "g15_per_pupil_all": R["g15_cumulative"]["_state_table"].P_all.reindex(acct.index).to_numpy(),
        "ccd_group_pupils": t[f"W_{MAIN_W}"].reindex(acct.index).to_numpy(),
    })
    sb["within_state_factor_arm_a"] = sb.structures_per_pupil_group_arm_a / sb.structures_per_pupil_all_arm_a
    sb = sb.sort_values("account_group_pupils", ascending=False)
    write_csv("state_breakdown.csv", sb)
    bn_cols = ("f12", "g15", "equip", "j99", "real_f12", "real_eq", "ks", "ke", "real_f12_chained")
    write_csv("national_flows.csv", nat.assign(**{c: nat[c] / 1e9 for c in bn_cols}).rename(columns={c: f"{c}_bn" for c in bn_cols}))
    top = by.assign(structures_per_pupil_a=conc["structures_a"].to_numpy(), structures_per_pupil_b=conc["structures_b"].to_numpy())
    wmap = d.set_index("LEAID").w_mex_dist
    top["group_pupils"] = top.id.map(wmap)
    top = top.sort_values("group_pupils", ascending=False).head(40)
    write_csv("top_group_districts.csv", top[["id", "NAME", "fips", "V33_2024", "group_pupils", "ks_post", "ks_pre_a_proportional",
                                              "ks_pre_b_proportional", "structures_per_pupil_a", "structures_per_pupil_b"]]
              .assign(ks_post=lambda x: x.ks_post / 1e9, ks_pre_a_proportional=lambda x: x.ks_pre_a_proportional / 1e9,
                      ks_pre_b_proportional=lambda x: x.ks_pre_b_proportional / 1e9)
              .rename(columns={"ks_post": f"fy{START}_2024_structures_bn", "ks_pre_a_proportional": f"pre_fy{START}_arm_a_bn",
                               "ks_pre_b_proportional": f"pre_fy{START}_arm_b_bn"}))

    pick = lambda rec: {k: val for k, val in rec.items() if k.startswith(("F_", "delta", "share"))}  # noqa: E731
    head = {arm: dollars[(arm, "primary", MAIN_W, "key_consistent_A")] for arm in ("a", "b")}
    lit = {arm: dollars[(arm, "primary", MAIN_W, "brief_literal_C")] for arm in ("a", "b")}
    sens = {arm: {lab: pick(dollars[(arm, "fy2000_start", MAIN_W, lab)]) for lab in ("key_consistent_A", "brief_literal_C")} for arm in ("a", "b")}
    keys_pre = ("start_fiscal_year", "pi_pre_start_share_of_k12_structures", "pre_start_structures_bn", "pre_start_equipment_bn")
    keys_chain = ("chained_share_real_f12", "chained_share_real_f12_before_2000", "chained_share_structures_stock_2024",
                  "chained_share_start_enrollment", "unchained_states_without_fy2024_pupils")
    rk_keys = ("structures_a", "structures_b", "equipment_a", "equipment_b", "structures_post", "structures_pre_a", "structures_pre_b",
               "structures_a_realloc", "structures_b_realloc", "structures_a_bea_level", "structures_b_bea_level", "g15_cumulative")
    summary = {
        "lane": HERE.name, "case_key": cb["case_key"], "case_band_bn": band, "adopted": False,
        "units": "2024 dollars; $bn a year for income year 2024",
        "rates": info["rates"], "pre_start": {k: info[k] for k in keys_pre}, "pre_start_fy2000": {k: info0[k] for k in keys_pre},
        "calibration": calib, "calibration_fy2000_start": calib0,
        "chain": {k: info[k] for k in keys_chain}, "chain_fy2000_start": {k: info0[k] for k in keys_chain},
        "survey_years": sample, "non_7digit_id_share_of_f12": bad_share, "coverage": coverage,
        "r_embedded_account": r_emb, "arm_order": arm_order,
        "R_K_mexican_district_share": {c: R[c][MAIN_W] for c in rk_keys},
        "R_K_mexican_district_share_fy2000_start": {c: R[f"s2000_{c}"][MAIN_W] for c in rk_keys},
        "R_current_spending_f33_district": float(pd.read_csv(R_OTHER).set_index(["concept", "weighting"]).R[("pp", MAIN_W)]),
        "case_base": {"k12_return_at_one_rate_bn": {e: base[e]["return_bn"] for e in base}, "effective_key": base["low"]["effective_key"],
                      "one_rate": base["low"]["one_rate"],
                      "k12_depreciation_base_bn": {"structures": base["low"]["effective_key"] * dep_s, "equipment": base["low"]["effective_key"] * dep_e},
                      "pupil_share_key_variant": cb["rows"][0]["pupil_share_key_variant"]},
        "headline_key_consistent_A": {arm: pick(rec) for arm, rec in head.items()},
        "brief_literal_C": {arm: pick(rec) for arm, rec in lit.items()},
        "fy2000_start_sensitivity": sens,
        "land_lower_bound": land,
        "inputs": {str(pth.relative_to(ROOT)): sha(pth) for pth in
                   [f33_path(y) for y in YEARS] + [CPI_FILE, BEA_FA, KEY_CSV, NAT_CSV, BRIDGE_CSV, EMBED, ACCT, R_OTHER, SCL / "weighting.py",
                                                    SCL / "ccd.py", NODE_SCRIPT]},
        "gates_failed": [g["gate"] for g in GATES if not g["pass"]],
    }
    (OUT / "summary.json").write_text(json.dumps(summary, indent=1, default=float) + "\n")
    with open(OUT / "gates.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["gate", "pass", "detail"], lineterminator="\n")
        w.writeheader()
        w.writerows(GATES)
    print("\n[result] mexican district share weights")
    for arm in ("a", "b"):
        h, l_ = head[arm], lit[arm]
        print(f"  arm {arm}: R_K structures {R[f'structures_{arm}'][MAIN_W]['C_district']:.4f}, equipment {R[f'equipment_{arm}'][MAIN_W]['C_district']:.4f}; "
              f"key-consistent F {h['F_stock_combined']:.4f} -> {h['delta_low_bn']:+.2f}bn; literal {l_['F_stock_combined']:.4f} -> {l_['delta_low_bn']:+.2f}bn; "
              f"FY2000 start {sens[arm]['key_consistent_A']['delta_low_bn']:+.2f}bn / {sens[arm]['brief_literal_C']['delta_low_bn']:+.2f}bn")
    failed = summary["gates_failed"]
    print(f"\n{len(GATES) - len(failed)}/{len(GATES)} gates pass")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
