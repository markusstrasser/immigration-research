"""Who among other residents gains and loses from the Mexican-origin union's presence, by income,
and the income-weighted net.

Frame (brief, not changed): the complete annual account's stationary 2024 comparison with and
without the 40.896574m CPS Mexican-origin residents, effects on all other US residents, a dollar
counted as a dollar. Each channel's total is taken as given from its lane and divided among other
residents; no total is re-estimated.

Income frame: CPS ASEC 2025 (income year 2024), the account's sha-gated archive and canonical
target. Every other resident gets an equivalized income y_i and a person-weighted percentile:
SPM resources / SPM equivalence scale (central) or household money income / sqrt(size) (check).
Persons living with target members keep their own place; only non-target persons count.

Resolution: channels measured on the CPS are carried per person. Channels whose input is another
survey (ACS rents and capital income, SCF rental holdings) are placed in 1,000 percentile cells
of that survey's own other-resident ranking and spread over the CPS persons in the same cell.
Binned inputs (NCVS income brackets, CBO and ITEP tax groups, CEX quintiles) are spread within
each bin by the microdata's distribution of the channel's base. Quintiles and deciles are for
display only.

Weights: (max(y_i, y_floor) / ybar)^(-eta), eta in {0, 1, 1.3, 1.4, 2}, ybar the unfloored
person-weighted mean over other residents, y_floor the 5th percentile (1st and 10th as
sensitivities). The quintile-bin version sum_q (ybar_q / ybar)^(-eta) Delta_q is reported beside
it, with unfloored and floored bin means, and each weighted sum is also given relative to the
median and as an equal-split equivalent (divided by the mean weight). Signs are from other
residents' point of view: a cost is negative.

Run from the repository root:
  OPENBLAS_NUM_THREADS=1 uv run --no-project python3 \
    infra/immigration-fiscal/distribution_weights_2026_09_23/distribute.py
The first run reads the ACS PUMS ZIPs in chunks (about two minutes) and caches the needed
columns in _cache/; later runs take seconds.
"""
from __future__ import annotations

import hashlib
import importlib.util
import io
import json
import re
import sys
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
FISCAL = HERE.parent
ROOT = HERE.parents[2]
DERIVED = HERE / "derived"
CACHE = HERE / "_cache"
SOURCES = CACHE / "sources"

ETAS = (0.0, 1.0, 1.3, 1.4, 2.0)
FLOORS = {"p1": 0.01, "p2": 0.02, "p3": 0.03, "p5": 0.05, "p10": 0.10}
CENTRAL_FLOOR = "p5"
CELLS = 1000
MEASURES = ("spm", "money")

# ---------------------------------------------------------------- pinned inputs, with sources
TARGET_TOTAL = 40_896_574.15235156
CIVILIAN_TOTAL = 336_727_803          # brief: other residents = 336.727803m - 40.896574m
TAU = (0.384, 0.426)                  # nest builder TAU: labor tax rate, lower / upper skill cell

# BJS, Criminal Victimization 2023 (NCJ 309335, revised June 9, 2025) Table 3 for 2022, and
# Criminal Victimization 2024 (NCJ 310547, September 2025) Table 3 for 2023 and 2024: rate of
# violent victimization per 1,000 persons age 12 or older, by household income. "serious" is
# the table's "violent crime excluding simple assault" (rape or sexual assault, robbery,
# aggravated assault). Persons age 12+ by household income: CV 2024 appendix table 19.
NCVS_BRACKETS = (25_000, 50_000, 100_000, 200_000)
NCVS = {  # year: (violent rates, serious rates, persons 12+)
    2022: ((42.4, 26.6, 18.5, 16.4, 23.4), (19.3, 12.5, 6.8, 6.6, 7.9),
           (38_445_470, 61_575_030, 88_540_080, 68_027_520, 25_716_540)),
    2023: ((39.0, 23.9, 21.4, 17.4, 15.7), (18.7, 10.2, 8.3, 5.1, 4.0),
           (35_790_580, 58_586_650, 89_260_250, 72_096_720, 29_122_830)),
    2024: ((38.3, 22.4, 23.5, 17.7, 22.1), (23.4, 6.5, 8.0, 5.7, 8.0),
           (33_401_030, 54_519_490, 88_435_240, 76_661_880, 33_355_570)),
}
NCVS_LABELS = ("Less than $25,000", "$25,000–$49,999", "$50,000–$99,999",
               "$100,000–$199,999", "$200,000 or more")

# CBO, The Distribution of Household Income, 2022 (January 2026, publication 61911), additional
# data for researchers, table 12 (share of federal taxes, %) and table 10 (share of income before
# transfers and taxes, %), all households, 2022. Groups: quintiles 1-4, then percentiles 81-90,
# 91-95, 96-99 and the top 1 percent. "after": households ranked by income after transfers and
# taxes; "before": ranked by income before transfers and taxes.
CBO_EDGES = (0.0, 0.2, 0.4, 0.6, 0.8, 0.9, 0.95, 0.99, 1.0)
CBO_GROUPS = ("lowest_quintile", "second_quintile", "middle_quintile", "fourth_quintile",
              "percentiles_81_90", "percentiles_91_95", "percentiles_96_99", "top_1_percent")
CBO_FED_SHARE = {"after": (1.7, 4.7, 8.8, 16.0, 13.8, 10.9, 16.8, 26.9),
                 "before": (0.3, 3.9, 8.6, 16.8, 14.6, 11.3, 17.0, 27.3)}
CBO_INCOME_SHARE = {"after": (4.7, 8.5, 12.9, 19.3, 14.2, 10.0, 13.4, 17.8),
                    "before": (3.7, 8.4, 13.2, 19.7, 14.4, 10.1, 13.5, 17.8)}
# ITEP, Who Pays? 7th edition (January 2024), Figure 1 and Appendix A "Average Across All
# States": state and local taxes as a share of income, non-senior residents, 2024 law at 2023
# incomes; groups lowest/second/middle/fourth 20%, next 15%, next 4%, top 1%. The next 15% rate
# is used for CBO's 81-90 and 91-95 groups.
ITEP_RATE = (11.4, 10.4, 10.5, 10.3, 9.5, 9.5, 8.3, 7.2)
# BEA NIPA Tables 3.2 and 3.3, 2024, pinned workbook (published August 26, 2026), $ millions.
BEA_WORKBOOK = ROOT / "sources/immigration-fiscal/data/external/bea_nipa/Section3All_xls.xlsx"

PATHS = dict(
    cps=FISCAL / "gen_ledger_extension_2026_09_16/_cache/asecpub25csv.zip",
    builder=FISCAL / "full_account_spending_2026_09_20/builder.py",
    service_cases=FISCAL / "full_account_2026_09_20/derived/service_response_cases.csv",
    headline_cases=FISCAL / "full_account_2026_09_20/derived/headline_cases.csv",
    nest=FISCAL / "production_nativity_nest_2026_09_22/derived/nest_scenarios.csv",
    branches=FISCAL / "production_nativity_nest_2026_09_22/derived/branch_composition.csv",
    wage_grid=FISCAL / "wage_distribution_2026_09_23/derived/wage_distribution_grid.csv",
    housing_arms=FISCAL / "housing_transfer_2026_09_23/derived/arms_headline.csv",
    housing_exposure=FISCAL / "housing_transfer_2026_09_23/derived/cbsa_exposure.csv",
    xwalk=FISCAL / "employment_entry_2026_09_18/_cache/xwalk_puma22.csv",
    county_cbsa=FISCAL / "hedonic_composition_2026_09_19/derived/geo_county_cbsa_2013.csv",
    scf=FISCAL / "housing_transfer_2026_09_23/_cache/scf/rscfp2022.dta",
    acs=ROOT / "sources/immigration-fiscal/data/external/acs_pums_2024_1yr",
    crime_offence=FISCAL / "crime_victim_cost_2026_09_23/derived/cost_by_offence_central.csv",
    crime_victim=FISCAL / "crime_victim_cost_2026_09_23/derived/cost_by_victim_and_offence_central.csv",
    crime_arms=FISCAL / "crime_victim_cost_2026_09_23/derived/arms.csv",
    uncompensated=FISCAL / "uncompensated_care_2026_09_23/derived/added_cost_arms.csv",
    cex=FISCAL / "consumer_price_benefit_2026_09_18/derived/partA_price_results.csv",
    main_case_bands=FISCAL / "main_case_2026_09_23/derived/main_case_bands.csv",
    main_case_inputs=FISCAL / "main_case_2026_09_23/derived/inputs.json",
)
GATES: dict[str, dict] = {}


def gate(name, ok, **detail):
    GATES[name] = dict(passed=bool(ok), **{k: (float(v) if isinstance(v, (np.floating, float, int, np.integer)) else v)
                                         for k, v in detail.items()})
    if not ok:
        raise SystemExit(f"[BLOCKED] gate {name} failed: {detail}")


def sha(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for block in iter(lambda: fh.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


# ------------------------------------------------------------------------- rank helpers
def position_rank(x, w, tiebreak=None):
    """Person-weighted percentile in (0, 1): the midpoint of each record's weight in sorted order.
    Ties are broken by record order (or by tiebreak), so tied records spread over adjacent cells
    instead of piling into one; tied records have the same income, so no weight changes."""
    order = np.lexsort((np.arange(len(x)) if tiebreak is None else tiebreak, x))
    cw = np.cumsum(w[order])
    out = np.empty(len(x))
    out[order] = (cw - w[order] / 2) / cw[-1]
    return out


def wquantile(x, w, q):
    order = np.argsort(x, kind="stable")
    cw = np.cumsum(w[order]) / w.sum()
    return x[order][np.minimum(np.searchsorted(cw, q, side="left"), len(x) - 1)]


def bins(p, n):
    return np.minimum((p * n).astype(int), n - 1)


# ------------------------------------------------------------------------- CPS frame
def load_cps():
    spec = importlib.util.spec_from_file_location("account_builder", PATHS["builder"])
    builder = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(builder)
    if builder.sha(PATHS["cps"]) != builder.CPS_SHA:
        raise SystemExit("[BLOCKED] CPS source changed")
    person = ["PH_SEQ", "PPPOS", "A_AGE", "PRPERTYP", "PRCITSHP", "PENATVTY", "PEFNTVTY",
              "PEMNTVTY", "PRDTHSP", "SPM_ID", "SPM_RESOURCES", "SPM_EQUIVSCALE", "PEARNVAL",
              "WSAL_VAL", "A_HGA", "INT_VAL", "DIV_VAL", "RNT_VAL", "PRIV", "FEDTAX_AC", "FICA",
              "STATETAX_A", "PRDTRACE", "PEHSPNON"]
    with zipfile.ZipFile(PATHS["cps"]) as z:
        d = pd.read_csv(z.open("pppub25.csv"), usecols=person)
        w = pd.read_csv(z.open("asec_csv_repwgt_2025.csv"), usecols=["h_seq", "PPPOS", "pwwgt0"]
                        ).rename(columns={"h_seq": "PH_SEQ"})
        h = pd.read_csv(z.open("hhpub25.csv"), usecols=["H_SEQ", "HTOTVAL", "H_NUMPER", "HSUP_WGT"]
                        ).rename(columns={"H_SEQ": "PH_SEQ"})
    d = d.merge(w, on=["PH_SEQ", "PPPOS"], validate="one_to_one", how="left")
    d = d.merge(h, on="PH_SEQ", validate="many_to_one", how="left")
    if d[["pwwgt0", "HTOTVAL", "H_NUMPER", "HSUP_WGT"]].isna().any().any():
        raise SystemExit("[BLOCKED] CPS person records without weights or household")
    civ, target = builder.canonical_target(d)
    pw = d.pwwgt0.to_numpy(float)
    gate("cps_canonical_target", abs(pw[target].sum() - TARGET_TOTAL) < 0.01,
         target=pw[target].sum(), expected=TARGET_TOTAL)
    gate("cps_civilian_total", abs(pw[civ].sum() - CIVILIAN_TOTAL) < 1.0,
         civilian=pw[civ].sum(), expected=CIVILIAN_TOTAL)
    other = civ & ~target
    gate("cps_other_residents", abs(pw[other].sum() - (CIVILIAN_TOTAL - TARGET_TOTAL)) < 1.0,
         other=pw[other].sum(), expected=CIVILIAN_TOTAL - TARGET_TOTAL)
    n_rec = d.groupby("PH_SEQ").PH_SEQ.transform("size").to_numpy()
    gate("cps_household_size_matches_records", np.array_equal(n_rec, d.H_NUMPER.to_numpy()),
         mismatches=int((n_rec != d.H_NUMPER.to_numpy()).sum()))
    spm_n = d.groupby("SPM_ID").SPM_ID.transform("size").to_numpy()
    d["civ"], d["target"], d["other"], d["pw"] = civ, target, other, pw
    d["y_spm"] = d.SPM_RESOURCES / d.SPM_EQUIVSCALE
    d["y_money"] = d.HTOTVAL / np.sqrt(d.H_NUMPER)
    d["resources_pc"] = d.SPM_RESOURCES / spm_n          # per-capita SPM resources
    d["money_pc"] = d.HTOTVAL / d.H_NUMPER               # per-capita household money income
    # Households, split over their other-resident members, for per-household dollars.
    n_other = d.groupby("PH_SEQ").other.transform("sum").to_numpy()
    d["hh_frac"] = np.where(other, d.HSUP_WGT / 100 / np.maximum(n_other, 1), 0.0)
    # CPS tax fields, per capita within the household (check key only).
    cps_tax = (d.FEDTAX_AC + 2 * d.FICA + d.STATETAX_A).groupby(d.PH_SEQ).transform("sum")
    d["cps_tax_pc"] = cps_tax / d.H_NUMPER
    d["capital"] = (d.INT_VAL + d.DIV_VAL + d.RNT_VAL).clip(lower=0)
    return d


def rank_frame(d, measure):
    """Percentiles of other residents (display, cells) and of all civilians (published bins)."""
    y = d[f"y_{measure}"].to_numpy(float)
    pw, other, civ = d.pw.to_numpy(), d.other.to_numpy(), d.civ.to_numpy()
    p_other = np.full(len(d), np.nan)
    p_other[other] = position_rank(y[other], pw[other])
    p_all = np.full(len(d), np.nan)
    p_all[civ] = position_rank(y[civ], pw[civ])
    ybar = float(np.average(y[other], weights=pw[other]))
    floors = {k: float(wquantile(y[other], pw[other], q)) for k, q in FLOORS.items()}
    return dict(y=y, p_other=p_other, p_all=p_all, ybar=ybar, floors=floors,
                median=float(wquantile(y[other], pw[other], 0.5)),
                q5=np.where(other, bins(np.nan_to_num(p_other), 5), -1),
                q10=np.where(other, bins(np.nan_to_num(p_other), 10), -1),
                cell=np.where(other, bins(np.nan_to_num(p_other), CELLS), -1))


def spread_cells(cell_amount, R, d):
    """Cell totals ($) to CPS other residents in the same percentile cell, per person weight."""
    other, pw = d.other.to_numpy(), d.pw.to_numpy()
    W = np.bincount(R["cell"][other], weights=pw[other], minlength=CELLS)
    if np.any((cell_amount != 0) & (W == 0)):
        raise SystemExit("[BLOCKED] percentile cell with an amount but no CPS persons")
    per = np.divide(cell_amount, W, out=np.zeros(CELLS), where=W > 0)
    out = np.zeros(len(d))
    out[other] = per[R["cell"][other]]
    return out


def per_person(d, key, total_bn, mask=None):
    """$ per person record so that the weighted sum equals total_bn, proportional to key."""
    pw = d.pw.to_numpy()
    m = d.other.to_numpy() if mask is None else (d.other.to_numpy() & mask)
    k = np.where(m, key, 0.0)
    den = float((pw * k).sum())
    if den == 0:
        raise SystemExit("[BLOCKED] empty distribution key")
    return total_bn * 1e9 * k / den


# ------------------------------------------------------------------------- channel totals
def fiscal_totals():
    """Direct fiscal response A of the published main case and of the adopted main case.
    A = welfare - (P + F); the adopted case adds general government (0.59-0.84), justice by use
    and the under-charged part of uncompensated care to A (main_case_2026_09_23)."""
    cases = pd.read_csv(PATHS["service_cases"])
    main = cases[cases.profile == "cbo_category_lag_non_school_full"].copy()
    heads = pd.read_csv(PATHS["headline_cases"])
    pf = heads.groupby("normalization").private_plus_receipts_bn.agg(["min", "max"])
    if not np.allclose(pf["min"], pf["max"]):
        raise SystemExit("[BLOCKED] production term differs across allocations")
    main["A_bn"] = main.welfare_bn - main.normalization.map(pf["min"])
    gate("fiscal_band_reproduced", np.isclose(-main.welfare_bn.max(), 165.1200005, atol=1e-6)
         and np.isclose(-main.welfare_bn.min(), 197.3841008, atol=1e-6),
         low=-main.welfare_bn.max(), high=-main.welfare_bn.min(), cases=len(main))
    A = np.unique(main.A_bn.round(9))
    pub = dict(A_low_cost=float(A.max()), A_high_cost=float(A.min()), A_mid=float((A.max() + A.min()) / 2),
               band=[float(-main.welfare_bn.max()), float(-main.welfare_bn.min())])
    bands = pd.read_csv(PATHS["main_case_bands"])
    bands = bands[bands.profile == "cbo_category_lag_non_school_full"].set_index("variant")
    inp = json.loads(PATHS["main_case_inputs"].read_text())
    gg_lo = bands.loc["gg_0.59", "cost_low_bn"] - bands.loc["published", "cost_low_bn"]
    gg_hi = bands.loc["gg_0.84", "cost_high_bn"] - bands.loc["published", "cost_high_bn"]
    just = inp["justice_change_bn"]["central"]
    unc = (inp["uncompensated_inside_bn"]["equal_low"], inp["uncompensated_inside_bn"]["equal_high"])
    d_lo, d_hi = gg_lo + just + unc[0], gg_hi + just + unc[1]
    gate("adopted_band_is_published_plus_changes",
         np.isclose(bands.loc["adopted", "cost_low_bn"], pub["band"][0] + d_lo, atol=1e-3)
         and np.isclose(bands.loc["adopted", "cost_high_bn"], pub["band"][1] + d_hi, atol=1e-3),
         adopted=[float(bands.loc["adopted", "cost_low_bn"]), float(bands.loc["adopted", "cost_high_bn"])],
         rebuilt=[pub["band"][0] + d_lo, pub["band"][1] + d_hi])
    ado = dict(A_low_cost=pub["A_low_cost"] - d_lo, A_high_cost=pub["A_high_cost"] - d_hi,
               band=[float(bands.loc["adopted", "cost_low_bn"]), float(bands.loc["adopted", "cost_high_bn"])],
               general_government=[float(gg_lo), float(gg_hi)], justice=float(just))
    ado["A_mid"] = (ado["A_low_cost"] + ado["A_high_cost"]) / 2
    return dict(published=pub, adopted=ado, uncomp_inside=list(unc),
                PF_cash=float(pf.loc["cash", "min"]), PF_gdp=float(pf.loc["gdp", "min"]))


def nest_rows():
    cols = ["proxy", "split", "normalization", "labor_share", "sigma", "capital_adjustment",
            "labor_supply_elasticity", "capital_tax_retention", "excluded_capital_owner_share",
            "nest_option", "sigma_NI", "wage_pct_native_cell0", "wage_pct_native_cell1",
            "wage_pct_other_fb_cell0", "wage_pct_other_fb_cell1", "native_production_gain_bn",
            "other_immigrant_production_gain_bn", "induced_current_receipts_bn",
            "private_plus_receipts_bn", "capital_gain_bn", "capital_tax_gain_bn",
            "capital_private_residual_bn"]
    s = pd.read_csv(PATHS["nest"], usecols=cols)
    return s[(s.excluded_capital_owner_share == 0) & (s.nest_option == "A_by_nativity")
             & (s.proxy == "PEARNVAL") & (s.labor_supply_elasticity == 0)
             & (s.capital_tax_retention == 1.0) & (s.normalization == "cash")
             & (s.labor_share == 0.65)].copy()


def pick(s, split, sigma, cap, eps):
    r = s[(s.split == split) & (s.sigma == sigma) & (s.capital_adjustment == cap)
          & (s.sigma_NI == eps)]
    if len(r) != 1:
        raise SystemExit(f"[BLOCKED] nest row not unique: {split} {sigma} {cap} {eps} ({len(r)})")
    return r.iloc[0]


# ------------------------------------------------------------------------- wages
def wage_basis(d, split, proxy="PEARNVAL"):
    """Per-person earnings of other residents by branch (native, other foreign-born) and cell."""
    earn = np.maximum(d[proxy].to_numpy(float), 0)
    cut = 39 if split == "hs_or_less" else 42
    cells = [d.A_HGA.between(31, cut).to_numpy(), d.A_HGA.between(cut + 1, 46).to_numpy()]
    native = d.PRCITSHP.isin([1, 2, 3]).to_numpy()
    other = d.other.to_numpy()
    basis = {}
    for tag, br in (("native", native), ("other_fb", ~native)):
        for c in (0, 1):
            basis[(tag, c)] = np.where(other & br & cells[c], earn, 0.0)
    return basis


def wage_delta(basis, row, after_tax):
    out = 0.0
    for (tag, c), e in basis.items():
        w = row[f"wage_pct_{tag}_cell{c}"] / 100
        out = out + (-w * e) * ((1 - TAU[c]) if after_tax else 1.0)
    return out


def wage_receipts_bn(basis, row, pw):
    return sum(TAU[c] * (-row[f"wage_pct_{tag}_cell{c}"] / 100) * (pw * e).sum()
               for (tag, c), e in basis.items()) / 1e9


# ------------------------------------------------------------------------- ACS and SCF
def read_zip(name, members, usecols, dtype):
    with zipfile.ZipFile(PATHS["acs"] / name) as z:
        for member in members:
            with z.open(member) as fh:
                yield from pd.read_csv(io.TextIOWrapper(fh), usecols=usecols, dtype=dtype,
                                       chunksize=200_000)


def acs_extract():
    cache = CACHE / "acs_extract.pkl"
    if cache.exists():
        return pd.read_pickle(cache)
    persons = []
    for ch in read_zip("csv_pus.zip", ["psam_pusa.csv", "psam_pusb.csv"],
                       ["SERIALNO", "PWGTP", "RELSHIPP", "HISP", "POBP", "INTP", "ADJINC"],
                       {"SERIALNO": str}):
        persons.append(pd.DataFrame({
            "SERIALNO": ch.SERIALNO.to_numpy(), "pw": ch.PWGTP.to_numpy(float),
            "p1": (ch.HISP.eq(2) | ch.POBP.eq(303)).to_numpy(),
            "head": ch.RELSHIPP.eq(20).to_numpy(), "gq": ch.RELSHIPP.isin([37, 38]).to_numpy(),
            "intp": ch.INTP.fillna(0).to_numpy(float) * ch.ADJINC.to_numpy(float) / 1e6}))
    persons = pd.concat(persons, ignore_index=True)
    households = []
    for ch in read_zip("csv_hus.zip", ["psam_husa.csv", "psam_husb.csv"],
                       ["SERIALNO", "STATE", "PUMA", "WGTP", "NP", "TYPEHUGQ", "TEN", "RNTP",
                        "VALP", "HINCP", "ADJINC", "ADJHSG"],
                       {"SERIALNO": str, "STATE": str, "PUMA": str}):
        ch = ch[ch.TYPEHUGQ.eq(1) & ch.NP.gt(0)]
        adj = ch.ADJHSG.to_numpy(float) / 1e6
        households.append(pd.DataFrame({
            "SERIALNO": ch.SERIALNO.to_numpy(), "STATE": ch.STATE.to_numpy(),
            "PUMA": ch.PUMA.to_numpy(), "wgtp": ch.WGTP.to_numpy(float), "np": ch.NP.to_numpy(float),
            "ten": ch.TEN.to_numpy(),
            "rent": np.where(ch.TEN.eq(3), ch.RNTP.fillna(0).to_numpy(float), 0) * 12 * adj,
            "value": np.where(ch.TEN.isin([1, 2]), ch.VALP.fillna(0).to_numpy(float), 0) * adj,
            "hinc": ch.HINCP.fillna(0).to_numpy(float) * ch.ADJINC.to_numpy(float) / 1e6}))
    households = pd.concat(households, ignore_index=True)
    CACHE.mkdir(exist_ok=True)
    out = dict(persons=persons, households=households)
    pd.to_pickle(out, cache)
    return out


def puma_exposure(households):
    """Each PUMA's share of rent due to the group, f = 1 - (1 - s)^e, averaged over its areas."""
    xw = pd.read_csv(PATHS["xwalk"], dtype=str)
    xw["afact"] = pd.to_numeric(xw["afact"])
    xw["state"], xw["puma"] = xw["state"].str.zfill(2), xw["puma22"].str.zfill(5)
    geo = pd.read_csv(PATHS["county_cbsa"], dtype=str)
    geo = geo[geo["is_metro"] == "1"][["county_fips", "cbsa"]]
    xw = xw.merge(geo, left_on="county", right_on="county_fips", how="left")
    xw["area"] = xw["cbsa"].fillna("nonmetro_" + xw["state"])
    alloc = xw.groupby(["state", "puma", "area"], as_index=False)["afact"].sum()
    alloc["afact"] = alloc["afact"] / alloc.groupby(["state", "puma"])["afact"].transform("sum")
    expo = pd.read_csv(PATHS["housing_exposure"], dtype={"area": str})[["area", "group_share"]]
    alloc = alloc.merge(expo, on="area", how="left", validate="many_to_one")
    if alloc.group_share.isna().any():
        raise SystemExit("[BLOCKED] crosswalk area without a group share")
    key = households.STATE + "|" + households.PUMA
    if not key.isin(alloc.state + "|" + alloc.puma).all():
        raise SystemExit("[BLOCKED] ACS PUMA missing from the crosswalk")
    return alloc


def acs_channels(acs, arms):
    """Other renters' extra rent, other owners' value gain, and the ACS capital-income key,
    in 1,000 percentile cells of ACS other residents ranked by HINCP / sqrt(NP)."""
    P, H = acs["persons"], acs["households"]
    head = P[P["head"]].drop_duplicates("SERIALNO").set_index("SERIALNO")["p1"]
    H = H.assign(head_p1=H.SERIALNO.map(head))
    if H.head_p1.isna().any():
        raise SystemExit("[BLOCKED] ACS household without a householder record")
    H["y"] = H.hinc / np.sqrt(H.np)
    y_of = H.set_index("SERIALNO")["y"]
    ref = P[~P.p1 & ~P.gq].copy()
    ref["y"] = ref.SERIALNO.map(y_of)
    if ref.y.isna().any():
        raise SystemExit("[BLOCKED] ACS person outside an occupied household")
    y_ref, w_ref = ref.y.to_numpy(), ref.pw.to_numpy()
    # Members of a household are adjacent in the sort (ties broken by serial number); the
    # household's percentile is the mean of its other-resident members' positions.
    ref["p"] = position_rank(y_ref, w_ref, pd.factorize(ref.SERIALNO)[0])
    H["p"] = H.SERIALNO.map(ref.groupby("SERIALNO").p.mean())
    H = H[~(H.p.isna() & H.head_p1.astype(bool))].copy()
    if H.p.isna().any():
        raise SystemExit("[BLOCKED] ACS household without an other-resident member")
    H["cell"] = bins(H.p.to_numpy(), CELLS)
    H["q5"] = bins(H.p.to_numpy(), 5)
    ref["cell"] = bins(ref.p.to_numpy(), CELLS)
    alloc = puma_exposure(H)
    s_nat = TARGET_TOTAL / 340.110988e6
    out = {}
    renters = (H.ten.eq(3) & ~H.head_p1.astype(bool)).to_numpy()
    owners = (H.ten.isin([1, 2]) & ~H.head_p1.astype(bool)).to_numpy()
    key = (H.STATE + "|" + H.PUMA).to_numpy()
    for (level, geography), r in arms.items():
        e = r["elasticity"]
        if geography == "metro_local":
            a = alloc.assign(f=alloc.afact * (1 - (1 - alloc.group_share) ** e))
            f_puma = a.groupby(a.state + "|" + a.puma).f.sum()
            f = pd.Series(key).map(f_puma).to_numpy()
        else:
            f = np.full(len(H), 1 - (1 - s_nat) ** e)
        rent_x = np.where(renters, f * H.rent.to_numpy() * H.wgtp.to_numpy(), 0.0)
        value_x = np.where(owners, f * H.value.to_numpy() * H.wgtp.to_numpy(), 0.0)
        gate(f"acs_rent_{level}_{geography}", np.isclose(rent_x.sum() / 1e9,
             r["other_renters_extra_rent_bn"], rtol=1e-6),
             acs=rent_x.sum() / 1e9, lane=r["other_renters_extra_rent_bn"])
        gate(f"acs_owner_value_{level}_{geography}", np.isclose(value_x.sum() / 1e9,
             r["other_owner_value_gain_stock_bn"], rtol=1e-6),
             acs=value_x.sum() / 1e9, lane=r["other_owner_value_gain_stock_bn"])
        out[(level, geography)] = dict(
            rent_cells=np.bincount(H.cell, weights=rent_x, minlength=CELLS),
            value_cells=np.bincount(H.cell, weights=value_x, minlength=CELLS),
            rent_q5=np.bincount(H.q5, weights=rent_x, minlength=5),
            renter_households_q5=np.bincount(H.q5, weights=np.where(renters, H.wgtp, 0.0), minlength=5))
    intp = ref.intp.clip(lower=0).to_numpy() * ref.pw.to_numpy()
    out["intp_cells"] = np.bincount(ref.cell, weights=intp, minlength=CELLS)
    out["acs_checks"] = dict(
        other_persons_m=float(w_ref.sum() / 1e6),
        other_renter_households_m=float(H.wgtp[renters].sum() / 1e6),
        group_share_of_positive_intp=float(
            (P.intp.clip(lower=0) * P.pw)[P.p1 & ~P.gq].sum() / (P.intp.clip(lower=0) * P.pw)[~P.gq].sum()))
    return out


def scf_cells():
    d = pd.read_stata(PATHS["scf"], columns=["y1", "wgt", "income", "kids", "married", "oresre"])
    size = 1 + (d.married == 1).astype(float) + d.kids.astype(float)
    y = (d.income / np.sqrt(size)).to_numpy(float)
    pw = (d.wgt * size).to_numpy(float)
    p = position_rank(y, pw)
    cells = np.bincount(bins(p, CELLS), weights=(d.wgt * d.oresre).to_numpy(float), minlength=CELLS)
    gate("scf_families", np.isclose(d.wgt.sum() / 1e6, 131.306, atol=0.01), families_m=d.wgt.sum() / 1e6)
    return cells, dict(families_m=float(d.wgt.sum() / 1e6), oresre_tn=float((d.wgt * d.oresre).sum() / 1e12),
                       top10pct_share=float(cells[900:].sum() / cells.sum()),
                       top1pct_share=float(cells[990:].sum() / cells.sum()))


# ------------------------------------------------------------------------- tax keys
def bea_totals():
    x = pd.ExcelFile(BEA_WORKBOOK)
    out = {}
    for sheet, lines in (("T30200-A", {"tax": "Current tax receipts", "row": "Taxes from the rest of the world",
                                        "si": "Contributions for government social insurance",
                                        "si_row": "From the rest of the world"}),
                         ("T30300-A", {"tax": "Current tax receipts",
                                       "si": "Contributions for government social insurance"})):
        t = pd.read_excel(x, sheet, header=None)
        col = [j for j, v in enumerate(t.iloc[7]) if str(v).startswith("2024")][0]
        lab = t.iloc[:, 1].astype(str).str.replace(r"\\\d+\\", "", regex=True).str.strip()
        vals = {}
        for k, label in lines.items():
            hit = t.index[lab == label]
            vals[k] = float(t.iloc[hit[0], col]) / 1e3   # $bn
        out[sheet] = vals
    fed = out["T30200-A"]
    F = fed["tax"] - fed["row"] + fed["si"] - fed["si_row"]
    S = out["T30300-A"]["tax"] + out["T30300-A"]["si"]
    gate("bea_2024_totals", 4900 < F < 5100 and 2500 < S < 2600, federal_bn=F, state_local_bn=S)
    return F, S


def tax_key(d, R, ranking, F, S):
    """Taxes attributed to each civilian: CBO federal shares and ITEP state-local rates by
    all-resident percentile group, spread within group by per-capita household money income."""
    civ, pw = d.civ.to_numpy(), d.pw.to_numpy()
    base = np.where(civ, np.maximum(d.money_pc.to_numpy(float), 0), 0.0)
    g = np.where(civ, np.searchsorted(CBO_EDGES[1:-1], np.nan_to_num(R["p_all"]), side="right"), -1)
    fed_share = np.array(CBO_FED_SHARE[ranking]) / sum(CBO_FED_SHARE[ranking])
    sl_group = np.array(ITEP_RATE) * np.array(CBO_INCOME_SHARE[ranking])
    sl_share = sl_group / sl_group.sum()
    fed = np.zeros(len(d))
    sl = np.zeros(len(d))
    for k in range(len(CBO_GROUPS)):
        m = g == k
        den = float((pw[m] * base[m]).sum())
        fed[m] = fed_share[k] * base[m] / den
        sl[m] = sl_share[k] * base[m] / den
    tax = F * fed + S * sl
    return tax, dict(other_share_of_taxes=float((pw * tax)[d.other.to_numpy()].sum() / (pw * tax)[civ].sum()),
                     state_local_group_shares=sl_share.round(4).tolist())


# ------------------------------------------------------------------------- crime key
def ncvs_rates():
    pops = np.array([NCVS[y][2] for y in NCVS], float)
    violent = (np.array([NCVS[y][0] for y in NCVS]) * pops).sum(0) / pops.sum(0)
    serious = (np.array([NCVS[y][1] for y in NCVS]) * pops).sum(0) / pops.sum(0)
    cum = np.cumsum(pops.sum(0)) / pops.sum()
    return dict(violent=violent, serious=serious, simple=violent - serious, cum=cum[:-1],
                pops=pops.sum(0))


def verify_ncvs_text():
    """Positive control: the pinned cells appear in the cached BJS text (when cached)."""
    found = {}
    for fname, years in (("bjs_cv23.txt", (2022, 2023)), ("bjs_cv24.txt", (2023, 2024))):
        path = SOURCES / fname
        if not path.exists():
            print(f"[DEGRADED] {fname} not cached; NCVS cells not re-verified against the report")
            return False
        text = path.read_text()
        block = text[text.index("Rate of violent victimization, by type of crime and"):]
        block = block[:block.index("Note: Rates are per 1,000")]
        for k, label in enumerate(NCVS_LABELS):
            rows = [[float(v) for v in re.findall(r"\d+\.\d", l.split(label)[1])]
                    for l in block.splitlines() if label in l]
            nums = next(r for r in rows if len(r) >= 4)
            expect = (NCVS[years[0]][0][k], NCVS[years[1]][0][k], NCVS[years[0]][1][k], NCVS[years[1]][1][k])
            found[f"{fname}:{label}"] = nums
            if tuple(nums[:4]) != expect:
                raise SystemExit(f"[BLOCKED] NCVS pin differs from {fname} {label}: {nums} vs {expect}")
    gate("ncvs_cells_match_bjs_text", True, rows=len(found))
    return True


def verify_published_text():
    """Positive controls for the CBO and ITEP pins against the cached documents (when cached)."""
    root = SOURCES / "cbo_61911/61911-additional-data-for-researchers/CBO_distribution_household_income_2022_data"
    if root.exists():
        for ranking, stem in (("after", "inc_after_trans_tax"), ("before", "inc_before_trans_tax")):
            t12 = pd.read_csv(root / f"households_ranked_by_{stem}_table_12_federal_tax_shares_1979_2022.csv")
            t10 = pd.read_csv(root / f"households_ranked_by_{stem}_table_10_household_income_shares_1979_2022.csv")
            a12 = t12[(t12.household_type == "all_households") & (t12.year == 2022)].set_index("income_group")
            a10 = t10[(t10.household_type == "all_households") & (t10.year == 2022)].set_index("income_group")
            got_f = tuple(a12.loc[list(CBO_GROUPS), "federal_taxes"])
            got_i = tuple(a10.loc[list(CBO_GROUPS), "inc_before_transfers_taxes"])
            if got_f != CBO_FED_SHARE[ranking] or got_i != CBO_INCOME_SHARE[ranking]:
                raise SystemExit(f"[BLOCKED] CBO pins differ from table 12/10 ({ranking}): {got_f} {got_i}")
        gate("cbo_pins_match_tables", True)
    else:
        print("[DEGRADED] CBO researcher tables not cached; pins not re-verified")
    itep = SOURCES / "itep_ITEP-Who-Pays-7th-edition.txt"
    if itep.exists():
        text = itep.read_text()
        at = text.index("Average Across")
        got = tuple(float(v) for v in re.findall(r"(\d+\.\d)%", text[at:at + 300])[:7])
        pinned = ITEP_RATE[:4] + ITEP_RATE[5:]
        gate("itep_pins_match_appendix", got == pinned, text=str(got), pinned=str(pinned))
    else:
        print("[DEGRADED] ITEP text not cached; pins not re-verified")


def crime_key(d, R_money_all, rates, mode):
    """Victimization risk per other resident age 12+, by household-income bracket."""
    htot = d.HTOTVAL.to_numpy(float)
    age = d.A_AGE.to_numpy()
    if mode == "rank":
        # NCVS bracket populations (2022-2024 pooled) give each bracket's percentile band of
        # persons 12+ ranked by household income; CPS persons 12+ (all civilians) are ranked
        # by HTOTVAL and placed in the same bands.
        idx = np.searchsorted(rates["cum"], np.nan_to_num(R_money_all), side="right")
    else:
        idx = np.searchsorted(NCVS_BRACKETS, htot, side="right")
    idx = np.clip(idx, 0, 4)
    old = age >= 12
    return {k: np.where(old, rates[k][idx], 0.0) for k in ("violent", "serious", "simple")}, idx


# ------------------------------------------------------------------------- weights and tables
def person_weights(d, R, eta, floor):
    """(max(y, floor) / ybar)^(-eta) for other residents; None if the floor is not positive
    (the 1st percentile of SPM resources is below zero, so its weight is undefined)."""
    f = R["floors"][floor]
    if eta > 0 and f <= 0:
        return None
    y = np.maximum(R["y"], f)
    out = np.zeros(len(d))
    m = d.other.to_numpy()
    out[m] = (y[m] / R["ybar"]) ** (-eta)
    return out


def weighted(delta, d, R, eta, floor):
    w = person_weights(d, R, eta, floor)
    if w is None:
        return float("nan")
    return float((d.pw.to_numpy() * w * delta).sum() / 1e9)


def bin_weighted(delta, d, R, eta, nbin, floor=None):
    """sum_q (ybar_q / ybar)^(-eta) Delta_q. The brief's version uses unfloored bin means; with
    `floor` the bin means are of floored incomes, so only the resolution differs from the
    per-person sum at that floor."""
    other, pw = d.other.to_numpy(), d.pw.to_numpy()
    q = R["q5"] if nbin == 5 else R["q10"]
    y = R["y"] if floor is None else np.maximum(R["y"], R["floors"][floor])
    tot = np.bincount(q[other], weights=(pw * delta)[other], minlength=nbin)
    ybin = (np.bincount(q[other], weights=(pw * y)[other], minlength=nbin)
            / np.bincount(q[other], weights=pw[other], minlength=nbin))
    return float(((ybin / R["ybar"]) ** (-eta) * tot).sum() / 1e9)


def by_bin(delta, d, R, nbin=5):
    other, pw = d.other.to_numpy(), d.pw.to_numpy()
    q = (R["q5"] if nbin == 5 else R["q10"])[other]
    x = (pw * delta)[other]
    return dict(net=np.bincount(q, weights=x, minlength=nbin) / 1e9,
                loss=np.bincount(q, weights=np.minimum(x, 0), minlength=nbin) / 1e9,
                gain=np.bincount(q, weights=np.maximum(x, 0), minlength=nbin) / 1e9)


def main():
    DERIVED.mkdir(exist_ok=True)
    verify_published_text()
    ncvs_verified = verify_ncvs_text()
    d = load_cps()
    pw, other = d.pw.to_numpy(), d.other.to_numpy()
    fiscal = fiscal_totals()
    F_total, S_total = bea_totals()
    rates = ncvs_rates()

    # ---- production term: after-tax wages P to workers, induced receipts F to the budget
    nest = nest_rows()
    central = pick(nest, "below_ba", 2.0, 1.0, np.inf)
    account = pick(nest, "hs_or_less", 2.0, 1.0, np.inf)
    eps3 = pick(nest, "below_ba", 2.0, 1.0, 3.0)
    short = pick(nest, "below_ba", 2.0, 0.0, np.inf)
    gate("account_production_term", np.isclose(account.private_plus_receipts_bn, fiscal["PF_cash"], rtol=1e-9),
         nest=account.private_plus_receipts_bn, account=fiscal["PF_cash"])
    branches = pd.read_csv(PATHS["branches"])
    basis = {s: wage_basis(d, s) for s in ("below_ba", "hs_or_less")}
    for split in basis:
        for (tag, c), e in basis[split].items():
            name = "native_non_union" if tag == "native" else "other_foreign_born"
            ref = branches[(branches.proxy == "PEARNVAL") & (branches.split == split)
                           & (branches.skill == c) & (branches.branch == name)].earnings_estimate.iloc[0]
            gate(f"wage_base_{split}_{tag}_cell{c}", np.isclose((pw * e).sum(), ref, rtol=1e-9),
                 cps=(pw * e).sum() / 1e9, nest=ref / 1e9)
    scen = {"below_ba_s2.0": ("below_ba", central), "hs_or_less_s2.0": ("hs_or_less", account),
            "below_ba_s2.0_eps3": ("below_ba", eps3)}
    for split in ("hs_or_less", "below_ba"):
        for sig in (1.5, 2.5):
            scen[f"{split}_s{sig}"] = (split, pick(nest, split, sig, 1.0, np.inf))
    for label, (split, row) in scen.items():
        after = (pw * wage_delta(basis[split], row, True)).sum() / 1e9
        rec = wage_receipts_bn(basis[split], row, pw)
        P = row.native_production_gain_bn + row.other_immigrant_production_gain_bn
        gate(f"wage_after_tax_equals_P_{label}", np.isclose(after, P, rtol=1e-8, atol=1e-9), cps=after, nest=P)
        gate(f"wage_receipts_equal_F_{label}", np.isclose(rec, row.induced_current_receipts_bn, rtol=1e-8),
             cps=rec, nest=row.induced_current_receipts_bn)
    F_c = float(central.induced_current_receipts_bn)
    P_c = float(central.native_production_gain_bn + central.other_immigrant_production_gain_bn)

    # ---- housing arms (long run, form A, central ownership, householder rule)
    ha = pd.read_csv(PATHS["housing_arms"]).drop_duplicates(["arm", "level", "form", "geography", "ownership"])
    ha = ha[(ha.arm == "long_run") & (ha.form == "A") & (ha.ownership == "central")]
    arms = {(r.level, r.geography): r._asdict() for r in ha.itertuples()}
    acs = acs_channels(acs_extract(), arms)
    scf, scf_info = scf_cells()

    # ---- crime victims' harm
    off = pd.read_csv(PATHS["crime_offence"]).set_index("offence")
    carms = pd.read_csv(PATHS["crime_arms"]).set_index("arm")
    crime_equal = float(off.loc["Total", "cost_full"]) / 1e9
    crime_tangible_equal = float(off.loc["Total", "cost_tangible"]) / 1e9
    crime_custody = float(carms.loc["scaling: ACS institutional ratio 1.118 (generic reallocated)", "full_bn"])
    env_low = float(carms.loc["ENVELOPE low, miller2021", "full_bn"])
    env_high = float(carms.loc["ENVELOPE high, miller2021_dot_vsl", "full_bn"])
    gate("crime_central", np.isclose(crime_equal, 28.9229, atol=5e-4) and np.isclose(crime_custody, 32.3381, atol=5e-4),
         equal_footing=crime_equal, custody_footing=crime_custody)
    serious_off = ["Murder", "Rape/sexual assault", "Robbery", "Aggravated assault"]
    serious_share = float(off.loc[serious_off, "cost_full"].sum() / off.loc["Total", "cost_full"])
    serious_share_tan = float(off.loc[serious_off, "cost_tangible"].sum() / off.loc["Total", "cost_tangible"])
    vic = pd.read_csv(PATHS["crime_victim"])
    vic["cls"] = np.where(vic.offence.eq("Simple assault"), "simple", "serious")
    by_race = vic.groupby(["victim", "cls"]).cost_full.sum() / vic.cost_full.sum()

    # ---- unreimbursed hospital care (outside budgets); the inside part is in the adopted case
    unc = pd.read_csv(PATHS["uncompensated"])
    eq = unc[unc.use_intensity == 1.0]
    out_lo, out_hi = float(eq.outside_accounts_bn.min()), float(eq.outside_accounts_bn.max())
    in_lo, in_hi = float(eq.inside_undercharged_bn.min()), float(eq.inside_undercharged_bn.max())
    gate("uncompensated_inside_matches_main_case",
         np.isclose(in_lo, fiscal["uncomp_inside"][0], atol=1e-4) and np.isclose(in_hi, fiscal["uncomp_inside"][1], atol=1e-4),
         lane=[in_lo, in_hi], main_case=fiscal["uncomp_inside"])
    unreimbursed_mid = (out_lo + out_hi) / 2

    cex = pd.read_csv(PATHS["cex"])
    cex = cex[(cex.arm == "published_jpe_2008") & (cex.shock == "lf_adjusted")
              & (cex.scope == "narrow_immigrant_intensive")].iloc[0]
    cex_q = np.array([cex[f"loss_bn_{k}"] for k in ("q1_lowest", "q2_second", "q3_third", "q4_fourth", "q5_highest")])

    # NCVS ranking: all civilians 12+ by unequivalized household money income.
    htot = d.HTOTVAL.to_numpy(float)
    m12 = d.civ.to_numpy() & (d.A_AGE.to_numpy() >= 12)
    p12 = np.full(len(d), np.nan)
    p12[m12] = position_rank(htot[m12], pw[m12])
    keys_rank, idx_rank = crime_key(d, p12, rates, "rank")
    keys_dollar, idx_dollar = crime_key(d, p12, rates, "dollar")
    bracket_share = {mode: (np.bincount(idx[m12], weights=pw[m12], minlength=5) / pw[m12].sum()).round(4).tolist()
                     for mode, idx in (("rank", idx_rank), ("dollar", idx_dollar))}
    hisp = d.PEHSPNON.eq(1).to_numpy()
    race = np.select([~hisp & d.PRDTRACE.eq(1).to_numpy(), ~hisp & d.PRDTRACE.eq(2).to_numpy(), hisp],
                     ["White", "Black", "Hispanic"], "Other")
    priv = d.PRIV.eq(1).to_numpy()
    R_money = rank_frame(d, "money")

    tables = {k: [] for k in ("frame", "quintile", "decile", "weighted", "regress", "weights", "ranges")}
    notes = {}
    for measure in MEASURES:
        R = R_money if measure == "money" else rank_frame(d, measure)
        ranking = "after" if measure == "spm" else "before"
        tax, tax_info = tax_key(d, R, ranking, F_total, S_total)
        notes[f"tax_{measure}"] = tax_info
        keys = {"a": tax, "b": np.ones(len(d))}
        ch = {}

        def crime_split(k, total, s_share=serious_share):
            return per_person(d, k["serious"], -total * s_share) + per_person(d, k["simple"], -total * (1 - s_share))

        # Central channels.
        for conv, key in keys.items():
            ch[f"fiscal_{conv}"] = per_person(d, key, fiscal["adopted"]["A_mid"] + F_c)
        ch["wages"] = wage_delta(basis["below_ba"], central, True)
        ch["renters"] = -spread_cells(acs[("central", "metro_local")]["rent_cells"], R, d)
        landlord = {}
        for (level, geo), a in arms.items():
            tot = a["other_renters_extra_rent_bn"] + a["net_other_residents_welfare_bn"]
            li = per_person(d, spread_cells(acs["intp_cells"], R, d), tot)
            ls = per_person(d, spread_cells(scf, R, d), tot)
            landlord[(level, geo)] = dict(intp=li, scf=ls, mid=(li + ls) / 2)
        ch["landlords"] = landlord[("central", "metro_local")]["mid"]
        ch["crime"] = crime_split(keys_rank, crime_custody)
        ch["unreimbursed_care"] = per_person(d, priv.astype(float), -unreimbursed_mid)
        ch["housing_net"] = ch["renters"] + ch["landlords"]
        central_parts = ["wages", "renters", "landlords", "crime", "unreimbursed_care"]
        for conv in keys:
            ch[f"TOTAL_{conv}"] = ch[f"fiscal_{conv}"] + sum(ch[p] for p in central_parts)

        # Display and sensitivity channels.
        # Check key for (a): the CPS tax fields (federal income tax after credits, payroll tax
        # with the employer half, state income tax), per capita within the household. They omit
        # property, sales and excise taxes.
        ch["fiscal_a_cps_tax_fields"] = per_person(d, np.maximum(d.cps_tax_pc.to_numpy(float), 0),
                                                   fiscal["adopted"]["A_mid"] + F_c)
        ch["wages_pretax"] = wage_delta(basis["below_ba"], central, False)
        for conv, key in keys.items():
            ch[f"fiscal_A_only_{conv}"] = per_person(d, key, fiscal["adopted"]["A_mid"])
            ch[f"TOTAL_{conv}_pretax_wages"] = (ch[f"fiscal_A_only_{conv}"] + ch["wages_pretax"]
                                                + sum(ch[p] for p in central_parts if p != "wages"))
            # Published September 20 band: fiscal A+F, the under-charged part of uncompensated
            # care financed by the same convention, crime on the equal footing (justice per head).
            ch[f"fiscal_published_{conv}"] = per_person(d, key, fiscal["published"]["A_mid"] + F_c)
            ch[f"uncomp_inside_published_{conv}"] = per_person(d, key, -(in_lo + in_hi) / 2)
        ch["crime_equal_footing"] = crime_split(keys_rank, crime_equal)
        for conv in keys:
            ch[f"TOTAL_{conv}_published_band"] = (ch[f"fiscal_published_{conv}"] + ch[f"uncomp_inside_published_{conv}"]
                                                  + ch["wages"] + ch["renters"] + ch["landlords"]
                                                  + ch["crime_equal_footing"] + ch["unreimbursed_care"])
        tan_custody = crime_custody * crime_tangible_equal / crime_equal
        ch["crime_tangible"] = crime_split(keys_rank, tan_custody, serious_share_tan)
        ch["crime_intangible"] = ch["crime"] - ch["crime_tangible"]
        ch["crime_all_violent_key"] = per_person(d, keys_rank["violent"], -crime_custody)
        ch["crime_dollar_brackets"] = crime_split(keys_dollar, crime_custody)
        rr = np.zeros(len(d))
        for grp in ("White", "Black", "Hispanic", "Other"):
            m = race == grp
            for cls in ("serious", "simple"):
                rr += per_person(d, keys_rank[cls], -crime_custody * by_race[(grp, cls)], m)
        ch["crime_race_mix"] = rr
        ch["wages_account_split"] = wage_delta(basis["hs_or_less"], account, True)
        ch["wages_eps3"] = wage_delta(basis["below_ba"], eps3, True)
        ch["wages_short_run_pretax"] = (wage_delta(basis["below_ba"], short, False)
                                        + per_person(d, d.capital.to_numpy(float), short.capital_gain_bn))
        for (level, geo) in arms:
            ch[f"renters_{geo}_{level}"] = -spread_cells(acs[(level, geo)]["rent_cells"], R, d)
            for kname in ("intp", "scf", "mid"):
                ch[f"landlords_{kname}_{geo}_{level}"] = landlord[(level, geo)][kname]
            ch[f"owner_value_stock_{geo}_{level}"] = spread_cells(acs[(level, geo)]["value_cells"], R, d)
        qm = R_money["q5"]
        cx = np.zeros(len(d))
        for q in range(5):
            m = other & (qm == q)
            cx[m] = cex_q[q] * 1e9 / pw[m].sum()
        ch["consumer_prices_side_view"] = cx

        # Range variants: every low or every high choice, per channel, on the weighted scale.
        rng = {}
        for conv, key in keys.items():
            rng[f"fiscal_{conv}"] = {f"A={v:.2f}": per_person(d, key, v + F_c)
                                     for v in (fiscal["adopted"]["A_low_cost"], fiscal["adopted"]["A_high_cost"])}
            # A wage scenario also moves the induced receipts; the difference from the central
            # F is financed by the same convention, so fiscal + wages stays consistent.
            rng[f"wages_{conv}"] = {lab: wage_delta(basis[s], r, True)
                                    + per_person(d, key, float(r.induced_current_receipts_bn) - F_c)
                                    for lab, (s, r) in scen.items()}
        rng["housing"] = {f"{geo}_{level}_{k}": ch[f"renters_{geo}_{level}"] + landlord[(level, geo)][k]
                          for (level, geo) in arms for k in ("intp", "scf", "mid")}
        rng["crime"] = {"envelope_low": crime_split(keys_rank, env_low),
                        "envelope_high": crime_split(keys_rank, env_high),
                        "equal_footing": ch["crime_equal_footing"], "custody_footing": ch["crime"],
                        "all_violent_key": ch["crime_all_violent_key"],
                        "dollar_brackets": ch["crime_dollar_brackets"], "race_mix": ch["crime_race_mix"]}
        rng["unreimbursed_care"] = {"low": per_person(d, priv.astype(float), -out_lo),
                                    "high": per_person(d, priv.astype(float), -out_hi)}

        # ---- gates: splits sum back to the given totals; eta = 0 equals the unweighted sum
        a_c = arms[("central", "metro_local")]
        given = {
            "fiscal_a": fiscal["adopted"]["A_mid"] + F_c, "fiscal_b": fiscal["adopted"]["A_mid"] + F_c,
            "fiscal_a_cps_tax_fields": fiscal["adopted"]["A_mid"] + F_c,
            "wages": P_c, "renters": -a_c["other_renters_extra_rent_bn"],
            "landlords": a_c["other_renters_extra_rent_bn"] + a_c["net_other_residents_welfare_bn"],
            "housing_net": a_c["net_other_residents_welfare_bn"], "crime": -crime_custody,
            "crime_equal_footing": -crime_equal, "crime_race_mix": -crime_custody,
            "crime_all_violent_key": -crime_custody, "crime_dollar_brackets": -crime_custody,
            "unreimbursed_care": -unreimbursed_mid, "consumer_prices_side_view": float(cex_q.sum()),
            "owner_value_stock_metro_local_central": a_c["other_owner_value_gain_stock_bn"],
            "TOTAL_a": fiscal["adopted"]["A_mid"] + F_c + P_c + a_c["net_other_residents_welfare_bn"]
            - crime_custody - unreimbursed_mid,
        }
        given["TOTAL_b"] = given["TOTAL_a"]
        for name, tot in given.items():
            got = (pw * ch[name]).sum() / 1e9
            gate(f"sum_{measure}_{name}", np.isclose(got, tot, rtol=1e-9, atol=1e-9), split=got, given=tot)
        for name, delta in ch.items():
            gate(f"eta0_{measure}_{name}", np.isclose(weighted(delta, d, R, 0.0, CENTRAL_FLOOR),
                 (pw * delta).sum() / 1e9, rtol=1e-12, atol=1e-9))

        # ---- income frame
        for nbin, key in ((5, "q5"), (10, "q10")):
            qv, wv, yv = R[key][other], pw[other], R["y"][other]
            for q in range(nbin):
                m = qv == q
                tables["frame"].append(dict(
                    measure=measure, bins=nbin, bin=q + 1, persons_m=wv[m].sum() / 1e6,
                    households_m=d.hh_frac.to_numpy()[other][m].sum() / 1e6,
                    ybar_bin=np.average(yv[m], weights=wv[m]), y_min=yv[m].min(), y_max=yv[m].max(),
                    resources_pc_bn=(wv * d.resources_pc.to_numpy()[other])[m].sum() / 1e9,
                    money_pc_bn=(wv * d.money_pc.to_numpy()[other])[m].sum() / 1e9))
        tables["frame"].append(dict(measure=measure, bins=0, bin=0, persons_m=pw[other].sum() / 1e6,
                                    households_m=d.hh_frac.sum() / 1e6, ybar_bin=R["ybar"],
                                    y_median=R["median"], **{f"floor_{k}": v for k, v in R["floors"].items()}))
        fr = pd.DataFrame(tables["frame"])
        f5 = fr[(fr.measure == measure) & (fr.bins == 5)].sort_values("bin")
        ybar_q = f5.ybar_bin.to_numpy()
        mean_w = {}
        for eta in ETAS:
            for fl in FLOORS:
                ww = person_weights(d, R, eta, fl)
                mean_w[(eta, fl)] = float((pw * ww)[other].sum() / pw[other].sum()) if ww is not None else np.nan
            ww = person_weights(d, R, eta, CENTRAL_FLOOR)
            mq = np.bincount(R["q5"][other], weights=(pw * ww)[other], minlength=5) / (f5.persons_m.to_numpy() * 1e6)
            for q in range(5):
                tables["weights"].append(dict(measure=measure, eta=eta, quintile=q + 1,
                                              bin_weight=(ybar_q[q] / R["ybar"]) ** (-eta),
                                              mean_person_weight_p5=mq[q]))
            tables["weights"].append(dict(measure=measure, eta=eta, quintile=0,
                                          median_normalization_factor=(R["median"] / R["ybar"]) ** eta,
                                          **{f"mean_person_weight_{fl}": mean_w[(eta, fl)] for fl in FLOORS}))

        # ---- matrix, deciles, weighted totals, regressivity
        hh_q = np.bincount(R["q5"][other], weights=d.hh_frac.to_numpy()[other], minlength=5)
        persons_q = f5.persons_m.to_numpy() * 1e6
        resources_q = f5.resources_pc_bn.to_numpy()
        for name, delta in ch.items():
            q = by_bin(delta, d, R)
            tot = float(q["net"].sum())
            if not np.isclose(tot, (pw * delta).sum() / 1e9, rtol=1e-9, atol=1e-9):
                raise SystemExit(f"[BLOCKED] quintile split of {name} does not sum")
            for k in range(5):
                tables["quintile"].append(dict(
                    measure=measure, channel=name, quintile=k + 1, bn=q["net"][k], loss_bn=q["loss"][k],
                    gain_bn=q["gain"][k], usd_per_household=q["net"][k] * 1e9 / hh_q[k],
                    usd_per_person=q["net"][k] * 1e9 / persons_q[k],
                    pct_of_resources=100 * q["net"][k] / resources_q[k]))
            tables["quintile"].append(dict(
                measure=measure, channel=name, quintile=0, bn=tot, loss_bn=q["loss"].sum(), gain_bn=q["gain"].sum(),
                usd_per_household=tot * 1e9 / hh_q.sum(), usd_per_person=tot * 1e9 / persons_q.sum(),
                pct_of_resources=100 * tot / resources_q.sum()))
            q10 = by_bin(delta, d, R, 10)
            for k in range(10):
                tables["decile"].append(dict(measure=measure, channel=name, decile=k + 1, bn=q10["net"][k]))
            L, G = q["loss"].sum(), q["gain"].sum()
            tables["regress"].append(dict(
                measure=measure, channel=name, net_bn=tot, gross_loss_bn=L, gross_gain_bn=G,
                loss_share_bottom2=(q["loss"][:2].sum() / L) if L < 0 else np.nan,
                gain_share_top2=(q["gain"][3:].sum() / G) if G > 0 else np.nan,
                net_share_q1=q["net"][0] / tot if tot else np.nan, net_share_q5=q["net"][4] / tot if tot else np.nan,
                pct_resources_q1=100 * q["net"][0] / resources_q[0],
                pct_resources_q5=100 * q["net"][4] / resources_q[4]))
            for eta in ETAS:
                row = dict(measure=measure, channel=name, eta=eta, unweighted_bn=tot)
                for fl in FLOORS:
                    row[f"person_{fl}"] = weighted(delta, d, R, eta, fl)
                row["quintile_bins"] = bin_weighted(delta, d, R, eta, 5)
                row["decile_bins"] = bin_weighted(delta, d, R, eta, 10)
                row["quintile_bins_floored_p5"] = bin_weighted(delta, d, R, eta, 5, CENTRAL_FLOOR)
                row["decile_bins_floored_p5"] = bin_weighted(delta, d, R, eta, 10, CENTRAL_FLOOR)
                # Equal-split equivalent: the weighted net divided by the mean weight, i.e. the
                # total that, split equally per person, has the same weighted value. It does not
                # depend on whether weights are normalized to the mean or the median.
                for fl in FLOORS:
                    row[f"equal_split_{fl}"] = row[f"person_{fl}"] / mean_w[(eta, fl)]
                row["median_normalized_p5"] = row[f"person_{CENTRAL_FLOOR}"] * (R["median"] / R["ybar"]) ** eta
                tables["weighted"].append(row)
        # A-4 treatment of victims' harm: population-average values of life and quality of life
        # are already income-weighted, so only the tangible part carries a weight; the intangible
        # part enters at face value on every scale (mean-normalized, median-normalized, equal split).
        intang = float((pw * ch["crime_intangible"]).sum() / 1e9)
        for label, base in (("crime_A4_intangible_unweighted", "crime"),
                            ("TOTAL_a_A4_crime", "TOTAL_a"), ("TOTAL_b_A4_crime", "TOTAL_b")):
            rest = ch[base] - ch["crime_intangible"]
            for eta in ETAS:
                row = dict(measure=measure, channel=label, eta=eta,
                           unweighted_bn=float((pw * ch[base]).sum() / 1e9))
                split = {}
                for fl in FLOORS:
                    wt = weighted(rest, d, R, eta, fl)
                    row[f"person_{fl}"] = wt + intang if np.isfinite(wt) else np.nan
                    split[f"equal_split_{fl}"] = wt / mean_w[(eta, fl)] + intang if np.isfinite(wt) else np.nan
                row["quintile_bins"] = bin_weighted(rest, d, R, eta, 5) + intang
                row["decile_bins"] = bin_weighted(rest, d, R, eta, 10) + intang
                row["quintile_bins_floored_p5"] = bin_weighted(rest, d, R, eta, 5, CENTRAL_FLOOR) + intang
                row["decile_bins_floored_p5"] = bin_weighted(rest, d, R, eta, 10, CENTRAL_FLOOR) + intang
                row.update(split)
                wt = weighted(rest, d, R, eta, CENTRAL_FLOOR)
                row["median_normalized_p5"] = wt * (R["median"] / R["ybar"]) ** eta + intang
                if eta == 0:
                    gate(f"eta0_{measure}_{label}", np.isclose(row[f"person_{CENTRAL_FLOOR}"], row["unweighted_bn"],
                                                              rtol=1e-12, atol=1e-9))
                tables["weighted"].append(row)
        # Ranges, stacked on the weighted scale at every eta.
        for eta in ETAS:
            for conv in keys:
                lo = hi = 0.0
                parts = {}
                for grp in (f"fiscal_{conv}", f"wages_{conv}", "housing", "crime", "unreimbursed_care"):
                    vals = {lab: weighted(v, d, R, eta, CENTRAL_FLOOR) for lab, v in rng[grp].items()}
                    unw = {lab: float((pw * v).sum() / 1e9) for lab, v in rng[grp].items()}
                    kmin, kmax = min(vals, key=vals.get), max(vals, key=vals.get)
                    parts[grp] = (vals[kmin], kmin, unw[kmin], vals[kmax], kmax, unw[kmax])
                    lo += vals[kmin]
                    hi += vals[kmax]
                    tables["ranges"].append(dict(measure=measure, eta=eta, convention=conv, group=grp,
                                                 most_costly_weighted=vals[kmin], most_costly_variant=kmin,
                                                 most_costly_unweighted=unw[kmin], least_costly_weighted=vals[kmax],
                                                 least_costly_variant=kmax, least_costly_unweighted=unw[kmax],
                                                 most_costly_equal_split=vals[kmin] / mean_w[(eta, CENTRAL_FLOOR)],
                                                 least_costly_equal_split=vals[kmax] / mean_w[(eta, CENTRAL_FLOOR)]))
                tables["ranges"].append(dict(measure=measure, eta=eta, convention=conv, group="TOTAL",
                                             most_costly_weighted=lo, least_costly_weighted=hi,
                                             most_costly_unweighted=sum(p[2] for p in parts.values()),
                                             least_costly_unweighted=sum(p[5] for p in parts.values()),
                                             most_costly_equal_split=lo / mean_w[(eta, CENTRAL_FLOOR)],
                                             least_costly_equal_split=hi / mean_w[(eta, CENTRAL_FLOOR)]))

    fr = pd.DataFrame(tables["frame"])
    fr.to_csv(DERIVED / "income_frame.csv", index=False)
    pd.DataFrame(tables["quintile"]).to_csv(DERIVED / "channel_by_quintile.csv", index=False)
    pd.DataFrame(tables["decile"]).to_csv(DERIVED / "channel_by_decile.csv", index=False)
    pd.DataFrame(tables["weighted"]).to_csv(DERIVED / "weighted_totals.csv", index=False)
    pd.DataFrame(tables["regress"]).to_csv(DERIVED / "regressivity.csv", index=False)
    pd.DataFrame(tables["weights"]).to_csv(DERIVED / "weights.csv", index=False)
    pd.DataFrame(tables["ranges"]).to_csv(DERIVED / "ranges_weighted.csv", index=False)
    rq = []
    for (level, geo) in arms:
        a = acs[(level, geo)]
        for k in range(5):
            rq.append(dict(level=level, geography=geo, acs_quintile=k + 1, extra_rent_bn=a["rent_q5"][k] / 1e9,
                           renter_households_m=a["renter_households_q5"][k] / 1e6,
                           usd_per_renter_household=a["rent_q5"][k] / a["renter_households_q5"][k]))
    pd.DataFrame(rq).to_csv(DERIVED / "rent_per_renter_household_acs.csv", index=False)
    wages = []
    for lab, (s, r) in scen.items():
        wages.append(dict(scenario=lab, split=s, sigma=float(r.sigma), eps=float(r.sigma_NI),
                          P_after_tax_bn=float(r.native_production_gain_bn + r.other_immigrant_production_gain_bn),
                          F_induced_receipts_bn=float(r.induced_current_receipts_bn),
                          pretax_bn=float((pw * wage_delta(basis[s], r, False)).sum() / 1e9),
                          native_cell0_pct=float(-r.wage_pct_native_cell0), native_cell1_pct=float(-r.wage_pct_native_cell1)))
    wages.append(dict(scenario="short_run_below_ba_s2.0", split="below_ba", sigma=2.0, eps=np.inf,
                      pretax_bn=float((pw * wage_delta(basis["below_ba"], short, False)).sum() / 1e9),
                      capital_gain_bn=float(short.capital_gain_bn)))
    pd.DataFrame(wages).to_csv(DERIVED / "wage_scenarios.csv", index=False)

    inputs = dict(
        fiscal=fiscal, federal_taxes_2024_bn=F_total, state_local_taxes_2024_bn=S_total,
        production=dict(central_P=P_c, central_F=F_c, account_P_plus_F=float(account.private_plus_receipts_bn)),
        crime=dict(equal_footing=crime_equal, custody_footing=crime_custody, tangible_equal=crime_tangible_equal,
                   envelope=[env_low, env_high], serious_share=serious_share,
                   victim_race_shares={f"{k[0]}|{k[1]}": float(v) for k, v in by_race.items()}),
        ncvs=dict(pooled_violent=rates["violent"].round(3).tolist(), pooled_serious=rates["serious"].round(3).tolist(),
                  pooled_simple=rates["simple"].round(3).tolist(), pooled_persons=rates["pops"].tolist(),
                  bracket_cum_share=rates["cum"].round(4).tolist(), cps_bracket_share_12plus=bracket_share,
                  verified_against_text=ncvs_verified),
        unreimbursed_care=dict(outside_low=out_lo, outside_high=out_hi, outside_mid=unreimbursed_mid,
                               inside_low=in_lo, inside_high=in_hi),
        consumer_prices_side_view_q=cex_q.round(4).tolist(),
        acs=acs["acs_checks"], scf=scf_info, tax_spm=notes["tax_spm"], tax_money=notes["tax_money"],
        housing={f"{k[0]}|{k[1]}": dict(renters=v["other_renters_extra_rent_bn"],
                                        net=v["net_other_residents_welfare_bn"],
                                        owners_stock=v["other_owner_value_gain_stock_bn"])
                 for k, v in arms.items()})
    (DERIVED / "inputs.json").write_text(json.dumps(inputs, indent=1, default=float))
    (DERIVED / "gates.json").write_text(json.dumps(GATES, indent=1, default=float))
    manifest = [dict(file=str(p.relative_to(HERE)), bytes=p.stat().st_size, sha256=sha(p))
                for p in sorted(SOURCES.glob("*")) if p.is_file() and p.suffix in (".pdf", ".txt", ".zip", ".html")]
    pd.DataFrame(manifest).to_csv(DERIVED / "sources_manifest.csv", index=False)
    print(f"{sum(g['passed'] for g in GATES.values())} gates passed")


if __name__ == "__main__":
    main()
