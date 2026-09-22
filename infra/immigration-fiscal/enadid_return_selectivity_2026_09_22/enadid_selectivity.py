#!/usr/bin/env python3
"""ENADID 2018/2023 — schooling of Mexico-born return migrants from the United States.

Mexico-side selectivity check. Two distinct objects, never subtracted:

  TSDem   resident endpoint transition. Mexico-born adults 20-64 now resident in a
          sampled Mexican household, classified by where they lived five years before
          the survey (United States vs Mexico). Schooling measured at the survey.
  TMigrante household-reported departures abroad in the five-year reference window,
          split by whether the person has returned. Carries NO schooling variable in
          either wave (verified against both data dictionaries); schooling is recovered
          only for returnees who rejoined the sampled household, via the P4.20 person
          link into TSDem.

Design-based standard errors: Taylor linearization of the domain ratio, strata EST_DIS,
PSU UPM_DIS, with-replacement. Validated on one cell against a bootstrap over PSUs.

Reproduce from the repository root:
  uv run --no-project python3 infra/immigration-fiscal/enadid_return_selectivity_2026_09_22/enadid_selectivity.py
"""
from __future__ import annotations

import hashlib
import io
import json
import math
import re
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd

LANE = Path(__file__).resolve().parent
ACQ = LANE.parent / "enadid_2026_09_20"
CACHE = ACQ / "_cache"
DERIVED = LANE / "derived"
RNG_SEED = 20260922
N_BOOT = 1000

# ---------------------------------------------------------------- variable map
# Every mnemonic and every category label below is copied from the official INEGI
# data dictionaries and category catalogs inside the two open-data bundles.
# Question numbers drift between waves; each wave is mapped separately.
VARMAP = {
    2018: {
        "zip": "enadid_2018_csv.zip",
        "tsdem": "conjunto_de_datos_tsdem_enadid_2018/conjunto_de_datos/conjunto_de_datos_tsdem_enadid_2018.csv",
        "tmig": "conjunto_de_datos_tmigrante_enadid_2018/conjunto_de_datos/conjunto_de_datos_tmigrante_enadid_2018.csv",
        # TSDem
        "birthplace": "p3_7",       # "P3.7 En que estado de la Republica Mexicana o pais nacio (NOMBRE)?"
        "prev5": "p3_19",           # "P3.19 Hace cinco anos, en agosto de 2013, en que estado ... vivia (NOMBRE)?"
        "prev5_ref": "August 2013",
        "niv": "niv",               # "P3.17 Cual es el ultimo ano o grado que aprobo (NOMBRE) en la escuela? (Nivel)"
        "gra": "gra",               # "P3.17 ... (Grado)"
        "niv_esc": None,            # 2018 ships no grouped schooling variable; derived by crosswalk
        "esco_acum": "esco_acum",   # "Escolaridad acumulada (anos aprobados)"
        "age": "edad",              # "Cuantos anos cumplidos tiene (NOMBRE)?"
        "sex": "sexo",              # "(NOMBRE) es hombre o mujer"
        "tsdem_weight": "fac_viv",  # "Factor de expansion a nivel vivienda"
        "tsdem_key": "llave_per",
        "tmig_weight": "fac_viv",   # "Factor de expansion a nivel vivienda"
        "tmig_key": "llave_mig",
        "tsdem_rows": 385978, "tsdem_cols": 93,
        "tmig_rows": 2611, "tmig_cols": 55,
        "tsdem_sha": "dd08b635bee06141e60a3f8a2cac3fbb4490a8db67749968a49998ecbec21968",
        "tmig_sha": "6d0ba35f6ce6b93a37db2523a7f838cfe0168cf8fbb3af7d1a19d9881e7f149c",
        "zip_sha": "51d01ebd08996f41a781232ea14513a7c08e7c949bfe13b0a9e8cc5900cd8b13",
        "anchor_dest_us": 84.8,     # resultados_enadid23.pdf, destination-country chart, 2018 bar
        "anchor_prev_abroad": 0.4,  # same document, prior-residence chart, 2018 "En otro pais"
        "anchor_prev_state": 96.6,
        "anchor_prev_other_state": 2.9,
    },
    2023: {
        "zip": "enadid_2023_csv.zip",
        "tsdem": "conjunto_de_datos_tsdem_enadid_2023/conjunto_de_datos/conjunto_datos_tsdem_enadid_2023.csv",
        "tmig": "conjunto_de_datos_tmigrante_enadid_2023/conjunto_de_datos/conjunto_datos_tmigrante_enadid_2023.csv",
        "birthplace": "p3_10",      # "Pregunta P3.10 En que estado de la Republica Mexicana o pais nacio (NOMBRE)?"
        "prev5": "p3_24",           # "Pregunta P3.24 Hace cinco anos, en agosto de 2018, en que estado ... vivia (NOMBRE)?"
        "prev5_ref": "August 2018",
        "niv": "niv",               # "Pregunta P3.22 ... (Nivel)"
        "gra": "gra",               # "Pregunta P3.22 ... (Grado)"
        "niv_esc": "niv_esc",       # "Nivel de escolaridad (agrupada)"  -- authoritative crosswalk source
        "esco_acum": "esco_acum",   # "Escolaridad acumulada (grados aprobados)"
        "age": "edad",
        "sex": "sexo",
        "tsdem_weight": "fac_viv",
        "tsdem_key": "llave_per",
        "tmig_weight": "fac_hog",   # "Factor de expansion a nivel hogar"
        "tmig_key": "llave_mig",
        "tsdem_rows": 359018, "tsdem_cols": 103,
        "tmig_rows": 3660, "tmig_cols": 52,
        "tsdem_sha": "da2cf21a565906912e27c3188c5a5b1e4e30fcc31bdff828d7d334e871487ba3",
        "tmig_sha": "4d2e7d71bae11142b458bc102fa25325a9f27bd90d89cce8aeee050792f7e365",
        "zip_sha": "248836ef8d4b74dda66d855b390e3557cdc79a1d487cd957b2273baa93ac4485",
        "anchor_dest_us": 87.9,
        "anchor_prev_abroad": 0.3,
        "anchor_prev_state": 96.7,
        "anchor_prev_other_state": 3.0,
    },
}

# catalogos/p3_7.csv (2018), catalogos/p3_10.csv (2023) -- identical in both waves:
#   1 "Aqui, en este estado" | 2 "En otro estado" | 3 "En Estados Unidos de America" | 4 "En otro pais"
BORN_MEXICO = {"1", "2"}
PREV_US = "3"
PREV_MEXICO = {"1", "2"}

# catalogos/niv_esc.csv (2023):
#   1 "Sin escolaridad" 2 "Primaria incompleta" 3 "Primaria completa"
#   4 "Secundaria incompleta" 5 "Secundaria completa" 6 "Medio superior"
#   7 "Superior" 9 "No especificado"
BANDS = {
    "1": "lt_lower_secondary", "2": "lt_lower_secondary",
    "3": "lt_lower_secondary", "4": "lt_lower_secondary",
    "5": "lower_secondary", "6": "upper_secondary", "7": "tertiary",
    "9": "unspecified",
}
BAND_ORDER = ["lt_lower_secondary", "lower_secondary", "upper_secondary", "tertiary"]
AGE_BANDS = [(20, 29), (30, 39), (40, 49), (50, 59), (60, 64)]
SEX_LABELS = {"1": "men", "2": "women"}  # catalogos/sexo.csv
# catalogos/p4_8_ag2.csv, identical in both waves; 9 = age at emigration not specified
DEP_AGE_LABELS = {"1": "0-17", "2": "18-29", "3": "30-59", "4": "60+"}


class GateFailure(RuntimeError):
    """A hard gate failed. Never downgraded to a warning."""


def gate(condition: bool, message: str) -> None:
    if not condition:
        raise GateFailure(message)


# ---------------------------------------------------------------- loading
def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def read_member(zip_path: Path, member: str) -> tuple[pd.DataFrame, str]:
    with zipfile.ZipFile(zip_path) as zf:
        raw = zf.read(member)
    digest = hashlib.sha256(raw).hexdigest()
    df = pd.read_csv(io.BytesIO(raw), dtype=str, encoding="latin-1", low_memory=False)
    # The 2018 members carry a UTF-8 BOM, which latin-1 decoding turns into stray bytes
    # on the first column name; strip any leading non-letter characters.
    df.columns = [re.sub(r"^[^A-Za-z]+", "", c.strip().strip('"')).lower() for c in df.columns]
    return df, digest


def clean(series: pd.Series) -> pd.Series:
    return series.fillna("").astype(str).str.strip().str.strip('"')


def load_wave(year: int) -> dict:
    m = VARMAP[year]
    zpath = CACHE / m["zip"]
    gate(zpath.exists(), f"[BLOCKED] missing bundle {zpath}")
    zsha = sha256_file(zpath)
    gate(zsha == m["zip_sha"], f"[BLOCKED] {m['zip']} sha256 {zsha} != frozen {m['zip_sha']}")

    tsdem, tsdem_sha = read_member(zpath, m["tsdem"])
    tmig, tmig_sha = read_member(zpath, m["tmig"])
    gate(tsdem_sha == m["tsdem_sha"], f"[BLOCKED] {year} TSDem member hash drift")
    gate(tmig_sha == m["tmig_sha"], f"[BLOCKED] {year} TMigrante member hash drift")

    # Gate: reproduce the acquisition lane's validated row/column counts.
    gate(len(tsdem) == m["tsdem_rows"], f"[BLOCKED] {year} TSDem rows {len(tsdem)} != {m['tsdem_rows']}")
    gate(tsdem.shape[1] == m["tsdem_cols"], f"[BLOCKED] {year} TSDem cols {tsdem.shape[1]} != {m['tsdem_cols']}")
    gate(len(tmig) == m["tmig_rows"], f"[BLOCKED] {year} TMigrante rows {len(tmig)} != {m['tmig_rows']}")
    gate(tmig.shape[1] == m["tmig_cols"], f"[BLOCKED] {year} TMigrante cols {tmig.shape[1]} != {m['tmig_cols']}")

    for df, key, wcol, tag in ((tsdem, m["tsdem_key"], m["tsdem_weight"], "TSDem"),
                               (tmig, m["tmig_key"], m["tmig_weight"], "TMigrante")):
        ids = clean(df[key])
        gate(ids.is_unique, f"[BLOCKED] {year} {tag} key {key} not unique")
        gate((ids != "").all(), f"[BLOCKED] {year} {tag} key {key} has blanks")
        w = pd.to_numeric(clean(df[wcol]), errors="coerce")
        gate(w.notna().all(), f"[BLOCKED] {year} {tag} weight {wcol} non-numeric")
        gate((w > 0).all(), f"[BLOCKED] {year} {tag} weight {wcol} not strictly positive")
        df["_w"] = w.astype(float)
        df["_h"] = clean(df["est_dis"])
        df["_psu"] = clean(df["upm_dis"])
        gate((df["_h"] != "").all() and (df["_psu"] != "").all(),
             f"[BLOCKED] {year} {tag} blank design identifier")
        # UPM_DIS must identify a PSU nationally, not only within a stratum.
        spanning = df.groupby("_psu")["_h"].nunique()
        gate((spanning <= 1).all(), f"[BLOCKED] {year} {tag} upm_dis spans multiple strata")

    return {"year": year, "map": m, "tsdem": tsdem, "tmig": tmig,
            "tsdem_sha": tsdem_sha, "tmig_sha": tmig_sha, "zip_sha": zsha}


# ---------------------------------------------------------------- variance engine
def _psu_totals(h: np.ndarray, psu: np.ndarray, u: np.ndarray) -> pd.DataFrame:
    return (pd.DataFrame({"h": h, "psu": psu, "u": u})
            .groupby(["h", "psu"], sort=False, observed=True)["u"].sum().reset_index())


def _taylor_var(tot: pd.DataFrame, lonely: str) -> tuple[float, int]:
    """With-replacement stratified variance of a PSU total. lonely: 'adjust' | 'certainty'."""
    grand = tot["u"].mean()
    var = 0.0
    singles = 0
    for _, g in tot.groupby("h", sort=False, observed=True):
        n = len(g)
        if n > 1:
            var += n / (n - 1) * float(((g["u"] - g["u"].mean()) ** 2).sum())
        else:
            singles += 1
            if lonely == "adjust":
                var += float((g["u"].iloc[0] - grand) ** 2)
    return var, singles


def ratio_se(df: pd.DataFrame, num: np.ndarray, den: np.ndarray,
             lonely: str = "adjust") -> tuple[float, float, int, float, float]:
    """Design-based estimate of R = sum(w*num)/sum(w*den) with Taylor-linearized SE.

    `df` must be the FULL wave frame; `num`/`den` carry zeros outside the domain, which
    is the correct domain-estimation form (all PSUs keep contributing to the variance).
    Returns (ratio, se, n_singleton_strata, weighted_numerator, weighted_denominator).
    """
    w = df["_w"].to_numpy()
    Y = float((w * num).sum())
    X = float((w * den).sum())
    gate(X > 0, "[BLOCKED] empty domain denominator")
    R = Y / X
    u = w * (num - R * den) / X
    var, singles = _taylor_var(_psu_totals(df["_h"].to_numpy(), df["_psu"].to_numpy(), u), lonely)
    return R, math.sqrt(max(var, 0.0)), singles, Y, X


def ratio_diff_se(df: pd.DataFrame, numA: np.ndarray, denA: np.ndarray,
                  numB: np.ndarray, denB: np.ndarray,
                  lonely: str = "adjust") -> tuple[float, float]:
    """Design-based SE of (R_A - R_B), keeping the covariance between the two domains."""
    w = df["_w"].to_numpy()
    YA, XA = float((w * numA).sum()), float((w * denA).sum())
    YB, XB = float((w * numB).sum()), float((w * denB).sum())
    gate(XA > 0 and XB > 0, "[BLOCKED] empty domain in difference")
    RA, RB = YA / XA, YB / XB
    u = w * (numA - RA * denA) / XA - w * (numB - RB * denB) / XB
    var, _ = _taylor_var(_psu_totals(df["_h"].to_numpy(), df["_psu"].to_numpy(), u), lonely)
    return RA - RB, math.sqrt(max(var, 0.0))


def bootstrap_se(df: pd.DataFrame, num: np.ndarray, den: np.ndarray,
                 n_boot: int = N_BOOT, seed: int = RNG_SEED) -> float:
    """Resample PSUs with replacement within strata; SD of the replicate ratios.

    Singleton strata resample to themselves, so this is the 'certainty' analogue of the
    Taylor estimator, which is what it is compared against.
    """
    w = df["_w"].to_numpy()
    codes, _ = pd.factorize(df["_h"].astype(str) + "\x1f" + df["_psu"].astype(str), sort=True)
    hcodes, _ = pd.factorize(df["_h"], sort=True)
    n_psu = codes.max() + 1
    psu_num = np.bincount(codes, weights=w * num, minlength=n_psu)
    psu_den = np.bincount(codes, weights=w * den, minlength=n_psu)
    psu_h = np.zeros(n_psu, dtype=np.int64)
    psu_h[codes] = hcodes
    order = np.argsort(psu_h, kind="stable")
    h_sorted = psu_h[order]
    bounds = np.searchsorted(h_sorted, np.arange(h_sorted.max() + 2))
    rng = np.random.default_rng(seed)
    reps = np.empty(n_boot)
    for b in range(n_boot):
        pick = np.concatenate([
            order[rng.integers(lo, hi, size=hi - lo)] if hi > lo else np.empty(0, dtype=np.int64)
            for lo, hi in zip(bounds[:-1], bounds[1:])
        ])
        d = psu_den[pick].sum()
        reps[b] = psu_num[pick].sum() / d if d > 0 else np.nan
    return float(np.nanstd(reps, ddof=1))


# ---------------------------------------------------------------- schooling bands
def build_crosswalk(tsdem23: pd.DataFrame) -> dict:
    """Derive NIV x GRA -> niv_esc from the 2023 file, which ships INEGI's own grouping.

    2018 has no niv_esc. Rather than invent a mapping, the 2023 pairing is read off the
    microdata, checked to be a function, and then applied to 2018.
    """
    niv, gra, grp = clean(tsdem23["niv"]), clean(tsdem23["gra"]), clean(tsdem23["niv_esc"])
    frame = pd.DataFrame({"niv": niv.str.zfill(2), "gra": gra, "grp": grp})
    frame = frame[(frame["niv"] != "") & (frame["grp"] != "")]
    counts = frame.groupby(["niv", "gra"])["grp"].nunique()
    gate((counts == 1).all(), "[BLOCKED] NIV x GRA -> niv_esc is not a function in 2023")
    xw = frame.groupby(["niv", "gra"])["grp"].first().to_dict()
    return {f"{k[0]}|{k[1]}": v for k, v in xw.items()}


def apply_bands(df: pd.DataFrame, xw: dict, niv_col: str, gra_col: str) -> pd.Series:
    key = clean(df[niv_col]).str.zfill(2) + "|" + clean(df[gra_col])
    grp = key.map(xw)
    return grp.map(BANDS).fillna("unspecified")


# ---------------------------------------------------------------- analysis
def prepare_tsdem(wave: dict, xw: dict) -> pd.DataFrame:
    m, df = wave["map"], wave["tsdem"].copy()
    df["_age"] = pd.to_numeric(clean(df[m["age"]]), errors="coerce")
    df["_sex"] = clean(df[m["sex"]])
    df["_born"] = clean(df[m["birthplace"]])
    df["_prev"] = clean(df[m["prev5"]])
    df["_band"] = apply_bands(df, xw, m["niv"], m["gra"])
    yrs = pd.to_numeric(clean(df[m["esco_acum"]]), errors="coerce")
    df["_years"] = yrs.where(yrs < 99)
    if m["niv_esc"]:  # 2023 only: the derived band must reproduce INEGI's own grouping
        own = clean(df[m["niv_esc"]]).map(BANDS).fillna("unspecified")
        have = clean(df[m["niv_esc"]]) != ""
        agree = float((df.loc[have, "_band"] == own[have]).mean())
        gate(agree == 1.0, f"[BLOCKED] 2023 derived band disagrees with niv_esc ({agree:.6f})")
    df["_universe"] = df["_age"].between(20, 64) & df["_born"].isin(BORN_MEXICO)
    df["_ret"] = df["_universe"] & (df["_prev"] == PREV_US)
    df["_non"] = df["_universe"] & df["_prev"].isin(PREV_MEXICO)
    return df


def age_band_label(age: float) -> str:
    for lo, hi in AGE_BANDS:
        if lo <= age <= hi:
            return f"{lo}-{hi}"
    return "other"


def tsdem_tables(wave: dict, xw: dict, audit: dict) -> pd.DataFrame:
    year = wave["year"]
    df = prepare_tsdem(wave, xw)
    df["_ageband"] = df["_age"].apply(lambda a: age_band_label(a) if pd.notna(a) else "other")
    rows = []

    slices = [("all", lambda d: pd.Series(True, index=d.index))]
    slices += [(f"sex:{lab}", (lambda s: (lambda d: d["_sex"] == s))(code))
               for code, lab in SEX_LABELS.items()]
    slices += [(f"age:{lo}-{hi}", (lambda l, h: (lambda d: d["_ageband"] == f"{l}-{h}"))(lo, hi))
               for lo, hi in AGE_BANDS]
    for code, lab in SEX_LABELS.items():
        for lo, hi in AGE_BANDS:
            slices.append((f"sex:{lab}|age:{lo}-{hi}",
                           (lambda s, l, h: (lambda d: (d["_sex"] == s) & (d["_ageband"] == f"{l}-{h}")))(code, lo, hi)))

    for slice_name, fn in slices:
        sel = fn(df).to_numpy()
        for group, flag in (("returnee_from_us", "_ret"), ("non_migrant", "_non")):
            dom = (df[flag].to_numpy() & sel)
            n_un = int(dom.sum())
            if n_un == 0:
                continue
            known = dom & (df["_band"] != "unspecified").to_numpy()
            for band in BAND_ORDER:
                num = (known & (df["_band"] == band).to_numpy()).astype(float)
                p, se, singles, Y, X = ratio_se(df, num, known.astype(float))
                rows.append(dict(wave=year, slice=slice_name, group=group, measure=band,
                                 n_unweighted=n_un, n_unweighted_band=int(num.sum()),
                                 weighted_pop=X, estimate=p, se=se,
                                 singleton_strata=singles))
            ymask = dom & df["_years"].notna().to_numpy()
            yv = np.nan_to_num(df["_years"].to_numpy(dtype=float), nan=0.0) * ymask
            p, se, singles, Y, X = ratio_se(df, yv, ymask.astype(float))
            rows.append(dict(wave=year, slice=slice_name, group=group, measure="mean_years_schooling",
                             n_unweighted=n_un, n_unweighted_band=int(ymask.sum()),
                             weighted_pop=X, estimate=p, se=se, singleton_strata=singles))

        ret_dom, non_dom = (df["_ret"].to_numpy() & sel), (df["_non"].to_numpy() & sel)
        if ret_dom.sum() == 0 or non_dom.sum() == 0:
            continue
        ret_k = ret_dom & (df["_band"] != "unspecified").to_numpy()
        non_k = non_dom & (df["_band"] != "unspecified").to_numpy()
        for band in BAND_ORDER:
            d, se = ratio_diff_se(df,
                                  (ret_k & (df["_band"] == band).to_numpy()).astype(float), ret_k.astype(float),
                                  (non_k & (df["_band"] == band).to_numpy()).astype(float), non_k.astype(float))
            rows.append(dict(wave=year, slice=slice_name, group="difference_returnee_minus_nonmigrant",
                             measure=band, n_unweighted=int(ret_dom.sum()),
                             n_unweighted_band=int((ret_k & (df["_band"] == band).to_numpy()).sum()),
                             weighted_pop=float("nan"), estimate=d, se=se, singleton_strata=-1))
        rm = ret_dom & df["_years"].notna().to_numpy()
        nm = non_dom & df["_years"].notna().to_numpy()
        yv = np.nan_to_num(df["_years"].to_numpy(dtype=float), nan=0.0)
        d, se = ratio_diff_se(df, yv * rm, rm.astype(float), yv * nm, nm.astype(float))
        rows.append(dict(wave=year, slice=slice_name, group="difference_returnee_minus_nonmigrant",
                         measure="mean_years_schooling", n_unweighted=int(ret_dom.sum()),
                         n_unweighted_band=int(rm.sum()), weighted_pop=float("nan"),
                         estimate=d, se=se, singleton_strata=-1))

    # Design validation on one cell: tertiary share among returnees, all slices pooled.
    ret_k = (df["_ret"] & (df["_band"] != "unspecified")).to_numpy()
    num = (ret_k & (df["_band"] == "tertiary").to_numpy()).astype(float)
    p_adj, se_adj, singles, _, _ = ratio_se(df, num, ret_k.astype(float), lonely="adjust")
    p_cer, se_cer, _, _, _ = ratio_se(df, num, ret_k.astype(float), lonely="certainty")
    se_boot = bootstrap_se(df, num, ret_k.astype(float))
    rel = abs(se_boot - se_cer) / se_cer
    gate(rel < 0.06, f"[BLOCKED] {year} bootstrap/Taylor SE disagree by {rel:.3%}")
    audit["design_validation"][str(year)] = {
        "cell": "tertiary share among Mexico-born returnees from the US, 20-64, both sexes",
        "estimate": p_adj,
        "se_taylor_lonely_adjust": se_adj,
        "se_taylor_lonely_certainty": se_cer,
        "se_bootstrap_psu_within_stratum": se_boot,
        "n_bootstrap_replicates": N_BOOT,
        "relative_gap_bootstrap_vs_taylor_certainty": rel,
        "singleton_psu_strata": singles,
        "note": ("A PSU bootstrap resamples singleton strata to themselves, so it is the "
                 "analogue of lonely='certainty'; the reported SEs use lonely='adjust', "
                 "which is the conservative option."),
    }
    return pd.DataFrame(rows)


def tmig_tables(wave: dict, xw: dict, audit: dict) -> pd.DataFrame:
    year = wave["year"]
    m = wave["map"]
    mig = wave["tmig"].copy()
    mig["_dest_us"] = clean(mig["p4_11"]) == "1"      # catalogos/p4_11.csv: 1 = Estados Unidos de America
    mig["_ret"] = clean(mig["cond_resid"])            # catalogos/cond_resid.csv: 1 Retorno, 2 No retorno, 9 NE
    mig["_sex"] = clean(mig["p4_6"])
    # catalogos/p4_8.csv: "000" Menos de un ano, "001..099" Anos, "999" No sabe
    dep_age = pd.to_numeric(clean(mig["p4_8"]), errors="coerce")
    mig["_dep_age"] = dep_age.where(dep_age < 999)
    mig["_dep_ag2"] = clean(mig["p4_8_ag2"])  # INEGI's own grouping, see DEP_AGE_LABELS

    # Schooling is absent from TMigrante in both waves. Recover it only for returnees who
    # rejoined the sampled household, through P4.20.2 (row number in the person list).
    tsd = prepare_tsdem(wave, xw)
    tsd["_key"] = clean(tsd[m["tsdem_key"]])
    link = (clean(mig["upm"]).str.zfill(7) + clean(mig["viv_sel"]).str.zfill(2)
            + clean(mig["hogar"]) + clean(mig["p4_20_2"]).str.zfill(2))
    link = link.where(clean(mig["p4_20_1"]) == "1", "")  # catalogos/p4_20_1.csv: 1 = Si
    mig["_link"] = link
    band_by_key = dict(zip(tsd["_key"], tsd["_band"]))
    age_by_key = dict(zip(tsd["_key"], tsd["_age"]))
    born_by_key = dict(zip(tsd["_key"], tsd["_born"]))
    mig["_linked_band"] = mig["_link"].map(band_by_key).fillna("")
    mig["_linked_age"] = mig["_link"].map(age_by_key)
    mig["_linked_born"] = mig["_link"].map(born_by_key).fillna("")

    us = mig["_dest_us"].to_numpy()
    rows = []
    for group, mask in (("returned", us & (mig["_ret"] == "1").to_numpy()),
                        ("still_abroad", us & (mig["_ret"] == "2").to_numpy()),
                        ("all_us_departures", us)):
        n_un = int(mask.sum())
        weighted = float((mig["_w"].to_numpy() * mask).sum())
        rows.append(dict(wave=year, group=group, measure="weighted_count", category="",
                         n_unweighted=n_un, estimate=weighted, se=float("nan")))
        for code, lab in SEX_LABELS.items():
            num = (mask & (mig["_sex"] == code).to_numpy()).astype(float)
            p, se, _, _, _ = ratio_se(mig, num, mask.astype(float))
            rows.append(dict(wave=year, group=group, measure="share_sex", category=lab,
                             n_unweighted=int(num.sum()), estimate=p, se=se))
        am = mask & mig["_dep_age"].notna().to_numpy()
        av = np.nan_to_num(mig["_dep_age"].to_numpy(dtype=float), nan=0.0)
        p, se, _, _, _ = ratio_se(mig, av * am, am.astype(float))
        rows.append(dict(wave=year, group=group, measure="mean_age_at_departure", category="",
                         n_unweighted=int(am.sum()), estimate=p, se=se))
        known_ag = mask & mig["_dep_ag2"].isin(DEP_AGE_LABELS).to_numpy()
        for code, lab in DEP_AGE_LABELS.items():
            num = (known_ag & (mig["_dep_ag2"] == code).to_numpy()).astype(float)
            p, se, _, _, _ = ratio_se(mig, num, known_ag.astype(float))
            rows.append(dict(wave=year, group=group, measure="share_age_at_departure",
                             category=lab, n_unweighted=int(num.sum()), estimate=p, se=se))
        # Supplementary: schooling recovered through the household person link. By
        # construction only returnees can be linked, so this is reported for the
        # returned group alone and never presented as a departure-cohort distribution.
        lk = mask & (mig["_linked_band"] != "").to_numpy() & (mig["_linked_band"] != "unspecified").to_numpy()
        rows.append(dict(wave=year, group=group, measure="linked_to_tsdem_coverage", category="",
                         n_unweighted=int(lk.sum()),
                         estimate=(float(lk.sum()) / n_un if n_un else float("nan")), se=float("nan")))
        if group == "returned" and lk.sum() >= 30:
            for band in BAND_ORDER:
                num = (lk & (mig["_linked_band"] == band).to_numpy()).astype(float)
                p, se, _, _, _ = ratio_se(mig, num, lk.astype(float))
                rows.append(dict(wave=year, group=group, measure="linked_schooling_share",
                                 category=band, n_unweighted=int(num.sum()), estimate=p, se=se))
            # Same link, restricted to the TSDem universe (Mexico-born, 20-64 at survey)
            # so the two returnee objects are compared on the same population.
            lk2 = (lk & mig["_linked_age"].between(20, 64).to_numpy()
                   & mig["_linked_born"].isin(BORN_MEXICO).to_numpy())
            rows.append(dict(wave=year, group=group, measure="linked_20_64_coverage", category="",
                             n_unweighted=int(lk2.sum()),
                             estimate=float(lk2.sum()) / n_un, se=float("nan")))
            for band in BAND_ORDER:
                num = (lk2 & (mig["_linked_band"] == band).to_numpy()).astype(float)
                p, se, _, _, _ = ratio_se(mig, num, lk2.astype(float))
                rows.append(dict(wave=year, group=group, measure="linked_schooling_share_20_64",
                                 category=band, n_unweighted=int(num.sum()), estimate=p, se=se))
    audit["tmigrante_schooling"][str(year)] = {
        "has_schooling_variable": False,
        "checked": "full data dictionary, all fields",
        "n_fields": int(m["tmig_cols"]),
        "link_route": "P4.20.1 == 1 and P4.20.2 row number -> TSDem LLAVE_PER (UPM+VIV_SEL+HOGAR+N_REN)",
        "linked_rows_us_departures": int((us & (mig["_linked_band"] != "").to_numpy()).sum()),
        "linked_rows_us_returned": int((us & (mig["_ret"] == "1").to_numpy()
                                        & (mig["_linked_band"] != "").to_numpy()).sum()),
        "linked_rows_us_still_abroad": int((us & (mig["_ret"] == "2").to_numpy()
                                            & (mig["_linked_band"] != "").to_numpy()).sum()),
    }
    return pd.DataFrame(rows)


def anchors(waves: dict, audit: dict) -> pd.DataFrame:
    """Reproduce published ENADID figures before any other number is reported."""
    rows = []
    for year, wave in waves.items():
        m = wave["map"]
        tsd = wave["tsdem"].copy()
        age = pd.to_numeric(clean(tsd[m["age"]]), errors="coerce")
        prev = clean(tsd[m["prev5"]])
        base = (age.between(5, 130) & prev.isin({"1", "2", "3", "4"})).to_numpy()
        for label, codes, published in (
                ("prior residence: same state", {"1"}, m["anchor_prev_state"]),
                ("prior residence: another state", {"2"}, m["anchor_prev_other_state"]),
                ("prior residence: another country", {"3", "4"}, m["anchor_prev_abroad"])):
            num = (base & prev.isin(codes).to_numpy()).astype(float)
            p, se, _, _, X = ratio_se(tsd, num, base.astype(float))
            rows.append(dict(wave=year, source="resultados_enadid23.pdf, prior-residence chart",
                             figure=f"{label}, population 5+", published_pct=published,
                             reproduced_pct=100 * p, se_pct=100 * se,
                             diff_pp=100 * p - published, weighted_denominator=X,
                             n_unweighted=int(base.sum())))
        mig = wave["tmig"].copy()
        dest = clean(mig["p4_11"])
        base = dest.isin({"1", "2"}).to_numpy()  # published note excludes unspecified destination
        num = (base & (dest == "1").to_numpy()).astype(float)
        p, se, _, _, X = ratio_se(mig, num, base.astype(float))
        rows.append(dict(wave=year, source="resultados_enadid23.pdf, destination-country chart",
                         figure="share of international emigrants whose destination was the US",
                         published_pct=m["anchor_dest_us"], reproduced_pct=100 * p, se_pct=100 * se,
                         diff_pp=100 * p - m["anchor_dest_us"], weighted_denominator=X,
                         n_unweighted=int(base.sum())))
    out = pd.DataFrame(rows)
    worst = float(out["diff_pp"].abs().max())
    gate(worst <= 0.06, f"[BLOCKED] anchor reproduction off by {worst:.3f} pp")
    audit["anchor_max_abs_diff_pp"] = worst
    return out


# ---------------------------------------------------------------- main
def main() -> None:
    DERIVED.mkdir(parents=True, exist_ok=True)
    audit = {"lane": LANE.name, "generated_by": "enadid_selectivity.py",
             "inputs": {}, "gates": {}, "variable_map": {},
             "design_validation": {}, "tmigrante_schooling": {}}

    waves = {y: load_wave(y) for y in (2018, 2023)}
    for y, w in waves.items():
        audit["inputs"][str(y)] = {
            "bundle": w["map"]["zip"], "bundle_sha256": w["zip_sha"],
            "tsdem_member": w["map"]["tsdem"], "tsdem_sha256": w["tsdem_sha"],
            # Column counts are the validated source-file counts, taken before the three
            # helper columns (_w, _h, _psu) are attached.
            "tsdem_rows": int(len(w["tsdem"])), "tsdem_cols": int(w["map"]["tsdem_cols"]),
            "tmigrante_member": w["map"]["tmig"], "tmigrante_sha256": w["tmig_sha"],
            "tmigrante_rows": int(len(w["tmig"])), "tmigrante_cols": int(w["map"]["tmig_cols"]),
        }
        audit["variable_map"][str(y)] = {k: v for k, v in w["map"].items()
                                         if k not in {"zip", "tsdem", "tmig"}}
    audit["gates"]["row_counts_reproduced"] = True
    audit["gates"]["weights_strictly_positive"] = True
    audit["gates"]["keys_unique"] = True
    audit["gates"]["bundle_hashes_match_frozen_manifest"] = True

    xw = build_crosswalk(waves[2023]["tsdem"])
    audit["schooling_crosswalk"] = {
        "source": "2023 TSDem microdata: NIV x GRA paired with INEGI's own niv_esc",
        "is_function": True, "n_cells": len(xw),
        "applied_to_2018": "2018 ships no niv_esc; the 2023 crosswalk is applied to its NIV/GRA",
        "bands": {"lt_lower_secondary": "niv_esc 1-4 (sin escolaridad, primaria incompleta, "
                                        "primaria completa, secundaria incompleta)",
                  "lower_secondary": "niv_esc 5 (secundaria completa)",
                  "upper_secondary": "niv_esc 6 (medio superior; includes normal basica and "
                                     "carrera tecnica con secundaria terminada)",
                  "tertiary": "niv_esc 7 (superior; includes carrera tecnica con bachillerato "
                              "terminado, licenciatura, especialidad, maestria, doctorado)"},
        "map": xw,
    }

    anchor = anchors(waves, audit)          # gate: anchors first
    anchor.to_csv(DERIVED / "anchor.csv", index=False)

    ret = pd.concat([tsdem_tables(w, xw, audit) for w in waves.values()], ignore_index=True)
    ret.to_csv(DERIVED / "return_migrants_by_schooling.csv", index=False)

    dep = pd.concat([tmig_tables(w, xw, audit) for w in waves.values()], ignore_index=True)
    dep.to_csv(DERIVED / "departures_by_schooling.csv", index=False)

    for name in ("anchor.csv", "return_migrants_by_schooling.csv", "departures_by_schooling.csv"):
        audit.setdefault("outputs", {})[name] = sha256_file(DERIVED / name)
    with open(DERIVED / "audit.json", "w") as fh:
        json.dump(audit, fh, indent=2, sort_keys=True, default=str)

    print(anchor.to_string(index=False))
    print()
    head = ret[(ret["slice"] == "all") & (ret["measure"] != "mean_years_schooling")]
    print(head[["wave", "group", "measure", "n_unweighted", "estimate", "se"]].to_string(index=False))
    print()
    print(ret[(ret["slice"] == "all") & (ret["measure"] == "mean_years_schooling")]
          [["wave", "group", "estimate", "se"]].to_string(index=False))
    print("\nwrote", DERIVED)


if __name__ == "__main__":
    main()
