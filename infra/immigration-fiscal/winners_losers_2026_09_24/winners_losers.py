"""Who wins and who loses from the Mexican-origin union's presence, person by person, over every
priced channel (brief: BRIEF.md, 2026-09-24).

Frame: the complete annual account's stationary 2024 comparison with and without the 40.896574m
CPS Mexican-origin residents; effects on the 295.83m other residents of CPS ASEC 2025, a dollar
counted as a dollar. Each channel's total is read from its lane's derived files; this script only
divides totals among persons, and never re-estimates one.

Base: distribution_weights_2026_09_23 (ladder 194). Its code is loaded from git at BASE_COMMIT, the
commit that moved it to the September 24 case, so later edits to its working tree cannot change this
lane. Its fiscal_totals("sept24") is the one definition of the September 24 direct response A that
both lanes use. Two regression targets: its channel_by_quintile.csv at SEPT23_COMMIT (the September 23
inputs) and at BASE_COMMIT (the September 24 inputs).

One definition per shared number, read from the lane that owns it: the federal part of the fiscal
cost and the debt legacy interest from debt_legacy_2026_09_23 at DEBT24_COMMIT (September 24; its
September 23 files at DEBT_COMMIT are the method's positive control); victims' harm only as a lane
computed it (decision 4's $30.93bn central); housing as ladder 190 publishes it.

Steps (BRIEF.md numbering):
 1. Channel registry: derived/channels.csv. The adopted fiscal case comes from specs.cjs
    (derived/fiscal_specs.csv): per specification, fiscal = A + F and wages = P, and the gate checks
    that the CPS person-level wages plus A + F equal the adopted cost in all 64 specifications. The
    frame's fiscal channel takes A at the band ends from the base lane's fiscal_totals("sept24"),
    which differs from the engine run by rounding (< 1e-4bn, recorded in gates.json).
 2. Person frame: _cache/person_frame.parquet (ignored); every other resident's dollars in every
    allocated channel at low, central and high. Gate: persons sum to each channel's total.
 3. Key templates for the sister lanes (key_templates.csv), and ingestion of any
    ../<lane>_2026_09_24/derived/winners_losers_rows.csv present at run time. A row enters a net
    only on the account's counterfactual, the group's (or its pupils') absence; the others are listed
    under their own counterfactual in derived/sister_other_counterfactuals.csv (gated).
 4. Cuts: derived/cuts.csv and derived/cut_summary.csv. Gate: every cut sums to the frame.
 5. Net winners and losers under (a) tax-share and (b) per-person financing; the federal
    deficit-financed part is the future taxpayers' row and is not allocated.
 6. The group itself: derived/group_frame.csv.
 7. The page: derived/winners_losers_table.csv and derived/person_nets_by_cut.csv.

Sister-lane rows map to key templates through an explicit `key` column or the patterns in key_map.csv;
test_winners_losers.py holds the ingestion's positive controls on a synthetic frame.

Run from the repository root (specs.cjs first):
  node infra/immigration-fiscal/winners_losers_2026_09_24/specs.cjs
  OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/winners_losers_2026_09_24/winners_losers.py
  OPENBLAS_NUM_THREADS=1 uv run --no-project python3 -m pytest infra/immigration-fiscal/winners_losers_2026_09_24/ -q
"""
from __future__ import annotations

import hashlib
import io
import json
import re
import subprocess
import sys
import types
import warnings
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd

warnings.filterwarnings("ignore", message="Workbook contains no default style")

HERE = Path(__file__).resolve().parent
FISCAL = HERE.parent
ROOT = HERE.parents[2]
DERIVED = HERE / "derived"
CACHE = HERE / "_cache"
SOURCES = CACHE / "sources"

BASE_COMMIT = "7ec7144"     # distribute.py and channel_by_quintile.csv on the September 24 case
SEPT23_COMMIT = "5b8957e"   # channel_by_quintile.csv on the September 23 case
BASE_REL = "infra/immigration-fiscal/distribution_weights_2026_09_23"
# The debt legacy lane's per-line federal fractions, federal split and interest: September 23 at
# DEBT_COMMIT (positive control), September 24 at DEBT24_COMMIT (used).
DEBT_COMMIT = "b42efdc"
DEBT24_COMMIT = "7ec7144"
DEBT_REL = "infra/immigration-fiscal/debt_legacy_2026_09_23/derived"
LEVELS = ("low", "central", "high")
CONVENTIONS = ("a", "b")
SISTERS = {  # lane directory -> registry id
    "school_dilution_2026_09_24": "school_dilution",
    "vending_restaurants_2026_09_24": "vending_restaurants",
    "compliance_gap_2026_09_24": "compliance_edge",
    "movers_reasons_2026_09_24": "movers",
}
# Two lanes finished without rows: generation_account_2026_09_24 (ba12f3c), whose split of the
# account by generation enters the group frame (generation_split), and consumption_key_2026_09_24
# (6841b39), whose proposed key correction is a registry row (consumption_proposal). Neither is in a net.
# A sister row enters a net only on the account's counterfactual, the group's (or its pupils')
# absence (parent ruling, 2026-09-25). The phrase must open the row's counterfactual; a qualifier
# that changes the comparison (enrollment held, spending that follows enrollment) disqualifies it.
ABSENCE = re.compile(r"^\s*(the\s+)?(mexican-origin\s+)?group(['’]s)?(\s+pupils)?\s+(are\s+)?absent\b"
                     r"|^\s*(without|in\s+the\s+absence\s+of)\s+the\s+(mexican-origin\s+)?group\b"
                     r"|^\s*the\s+group['’]s\s+absence\b", re.I)
NOT_ABSENCE = re.compile(r"enrollment held|not the account's counterfactual", re.I)
LANE_LABELS = {  # printed with a lane's allocated rows
    "school_dilution_2026_09_24": "present value of lifetime earnings, not annual cash; the relabel is "
                                  "proposed in decisions/2026-09-25-school-dilution-priced-beside.md",
}
SISTER_COLUMNS = ["group", "channel", "direction", "bn_low", "bn_central", "bn_high", "population_m",
                  "per_person_usd", "basis", "relation_to_account", "counterfactual", "source"]
TODAY = "2026-09-24"

FIPS = {1: "AL", 2: "AK", 4: "AZ", 5: "AR", 6: "CA", 8: "CO", 9: "CT", 10: "DE", 11: "DC", 12: "FL",
        13: "GA", 15: "HI", 16: "ID", 17: "IL", 18: "IN", 19: "IA", 20: "KS", 21: "KY", 22: "LA", 23: "ME",
        24: "MD", 25: "MA", 26: "MI", 27: "MN", 28: "MS", 29: "MO", 30: "MT", 31: "NE", 32: "NV", 33: "NH",
        34: "NJ", 35: "NM", 36: "NY", 37: "NC", 38: "ND", 39: "OH", 40: "OK", 41: "OR", 42: "PA", 44: "RI",
        45: "SC", 46: "SD", 47: "TN", 48: "TX", 49: "UT", 50: "VT", 51: "VA", 53: "WA", 54: "WV", 55: "WI",
        56: "WY"}
POSTAL = {v: k for k, v in FIPS.items()}
MEXICO_BIRTHPLACE = 303          # CPS PENATVTY code for Mexico

# Clemens, Montenegro & Pritchett, "The Place Premium: Wage Differences for Identical Workers Across
# the US Border", HKS RWP09-004 (January 2009), corpus doi_10_2139_ssrn_1211427. Table 1 col. 6,
# Mexico: Ro 2.53 (95% CI 2.42, 2.65). Section 3.3: "the average emigrant comes from the 56th
# percentile of residual wages, suggesting that Ro/Re = 1.03 (with a 95% confidence interval of
# (0.96, 1.12)), so that Re ~ 2.46". Table 8, Mexico: Re 2.79 if the median migrant sits at the
# origin's 50th percentile, 2.08 at the 70th ("stronger than any of the evidence from any country
# above supports"). Low = 2.08, central = 2.46, high = 2.79.
PLACE_PREMIUM_RE = {"low": 2.08, "central": 2.46, "high": 2.79}

PATHS = dict(
    specs=HERE / "derived" / "fiscal_specs.csv",
    lines=HERE / "derived" / "fiscal_lines_band_ends.csv",
    bands=FISCAL / "main_case_2026_09_24/derived/main_case_bands.csv",
    omb_receipts=ROOT / "sources/immigration-fiscal/data/external/omb_hist_fy2027/hist02z1_fy2027.xlsx",
    omb_outlays=ROOT / "sources/immigration-fiscal/data/external/omb_hist_fy2027/hist03z1_fy2027.xlsx",
    crime_dollar=FISCAL / "crime_ratio_direction_2026_09_24/derived/dollar_effects.csv",
    nibrs_cost=FISCAL / "offender_ethnicity_nibrs_2026_09_23/derived/cost_arms.csv",
    congestion_arms=FISCAL / "congestion_2026_09_23/derived/arms_summary.csv",
    congestion_metro=FISCAL / "congestion_2026_09_23/derived/metro_distribution.csv",
    congestion_ua=FISCAL / "congestion_2026_09_23/derived/ua_exposure.csv",
    care=FISCAL / "care_household_services_2026_09_23/derived/summary.csv",
    preferences=FISCAL / "affirmative_action_cost_2026_09_24/derived/channels.csv",
    preferences_log=FISCAL / "affirmative_action_cost_2026_09_24/derived/calc_output.txt",
    scale=FISCAL / "scale_spillovers_2026_09_23/derived/summary.csv",
    scale_metro=FISCAL / "scale_spillovers_2026_09_23/derived/metro_distribution.csv",
    mobility=FISCAL / "labor_mobility_insurance_2026_09_23/derived/insurance_summary.json",
    housing_grid=FISCAL / "housing_transfer_2026_09_23/derived/arms_grid.csv",
    generations=FISCAL / "generation_account_2026_09_24/derived/generation_results.csv",
    consumption=FISCAL / "consumption_key_2026_09_24/derived/engine_summary.json",
    housing_headline=FISCAL / "housing_transfer_2026_09_23/derived/arms_headline.csv",
    real_costs=FISCAL / "sept24_propagation_2026_09_24/derived/real_costs_totals.csv",
    band_variants=FISCAL / "sept24_propagation_2026_09_24/derived/band_variants.csv",
    remittance_flows=FISCAL / "consumption_key_2026_09_24/derived/remittance_flows.csv",
    # The consumption lane's ignored cache: Banxico SIE table CE167, the primary file behind its corridor.
    banxico_ce167=FISCAL / "consumption_key_2026_09_24/_cache/sources/corridor/banxico_CE167_2022_2025.xlsx",
    # Untracked at run time on 2026-09-25; read for a consistency check only.
    debt_corrections=FISCAL / "debt_legacy_2026_09_23/derived/corrections_federal_by_component_2024.csv",
    census_industry=SOURCES / "census_industry_2022_crosswalk.xlsx",
)
CENSUS_INDUSTRY_URL = ("https://www2.census.gov/programs-surveys/demo/guidance/industry-occupation/"
                       "2022-Census-Industry-Code-List-with-Crosswalk.xlsx")
GATES: dict[str, dict] = {}


def gate(name, ok, **detail):
    GATES[name] = dict(passed=bool(ok), **{k: (float(v) if isinstance(v, (np.floating, np.integer)) else v)
                                         for k, v in detail.items()})
    if not ok:
        raise SystemExit(f"[BLOCKED] gate {name} failed: {detail}")


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def file_sha(path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for block in iter(lambda: fh.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def git_show(rel: str, commit: str = BASE_COMMIT) -> bytes:
    return subprocess.run(["git", "-C", str(ROOT), "show", f"{commit}:{rel}"],
                          check=True, capture_output=True).stdout


def debt_csv(name: str, commit: str = DEBT_COMMIT) -> pd.DataFrame:
    return pd.read_csv(io.BytesIO(git_show(f"{DEBT_REL}/{name}", commit)))


def debt_json(name: str, commit: str = DEBT_COMMIT) -> dict:
    return json.loads(git_show(f"{DEBT_REL}/{name}", commit))


def write_csv(df: pd.DataFrame, name: str):
    df.to_csv(DERIVED / name, index=False, lineterminator="\n", float_format="%.10g")


# ================================================================== base lane, pinned at BASE_COMMIT
def load_base():
    """distribute.py at BASE_COMMIT as a module. __file__ points at the base lane, so its caches
    (ACS extract, cached documents) are read from there; nothing here calls its main() or writes."""
    src = git_show(f"{BASE_REL}/distribute.py")
    mod = types.ModuleType("base_distribute")
    mod.__file__ = str(ROOT / BASE_REL / "distribute.py")
    exec(compile(src.decode(), mod.__file__, "exec"), mod.__dict__)
    return mod, sha(src)


# ================================================================== CPS frame
def load_frame(B):
    d = B.load_cps()
    extra_p = ["PH_SEQ", "PPPOS", "A_SEX", "INDUSTRY", "WORKYN", "WKSWORK", "HRSWK", "SEMP_VAL", "FRSE_VAL",
               "MIG_ST", "MIGSAME", "NOCOV_CYR", "PERRP", "A_CLSWKR"]
    extra_h = ["H_SEQ", "GESTFIPS", "H_TENURE", "HRNTVAL", "GTMETSTA"]
    with zipfile.ZipFile(B.PATHS["cps"]) as z:
        p = pd.read_csv(z.open("pppub25.csv"), usecols=extra_p)
        h = pd.read_csv(z.open("hhpub25.csv"), usecols=extra_h).rename(columns={"H_SEQ": "PH_SEQ"})
    gate("cps_extra_columns_aligned", np.array_equal(p.PH_SEQ.to_numpy(), d.PH_SEQ.to_numpy())
         and np.array_equal(p.PPPOS.to_numpy(), d.PPPOS.to_numpy()), records=len(d))
    for c in extra_p[2:]:
        d[c] = p[c].to_numpy()
    hh = h.set_index("PH_SEQ")
    for c in extra_h[1:]:
        d[c] = d.PH_SEQ.map(hh[c]).to_numpy()
    if d[extra_h[1:]].isna().any().any():
        raise SystemExit("[BLOCKED] CPS person without household geography or tenure")
    other, target = d.other.to_numpy(), d.target.to_numpy()
    d["st"] = d.GESTFIPS.astype(int)
    d["st_ab"] = d.st.map(FIPS)
    d["native"] = d.PRCITSHP.isin([1, 2, 3])
    hga = d.A_HGA.to_numpy()
    edu = np.select([hga <= 38, hga == 39, (hga >= 40) & (hga <= 42), hga >= 43],
                    ["below_high_school", "high_school", "some_college", "ba_plus"], "none")
    adult25 = d.A_AGE.to_numpy() >= 25
    d["edu4"] = np.where(adult25, edu, "under_25")
    d["edu_nativity"] = np.where(adult25, pd.Series(edu) + "|" + np.where(d.native, "us_born", "other_foreign_born"),
                                 "under_25")
    age = d.A_AGE.to_numpy()
    d["age3"] = np.select([age < 18, age < 65], ["under_18", "18_64"], "65_plus")
    hisp = d.PEHSPNON.eq(1).to_numpy()
    race = d.PRDTRACE.to_numpy()
    d["race5"] = np.select([~hisp & (race == 1), ~hisp & (race == 2), hisp, ~hisp & (race == 4)],
                           ["nh_white", "nh_black", "hispanic_other_origin", "nh_asian"], "other")
    d["sex"] = np.where(d.A_SEX.eq(1), "male", "female")
    d["worker"] = np.where(d.WORKYN.eq(1), "worker", "not_worker")
    ind = d.INDUSTRY.to_numpy()
    d["industry5"] = np.where(d.WORKYN.eq(1), np.select(
        [ind == 770, ind == 8680, (ind >= 170) & (ind <= 290), ind == 7770],
        ["construction", "restaurants", "agriculture", "landscaping"], "rest"), "not_worker")
    # Tenure of the household: landlord if it reports rental income (CPS HRNTVAL: rents, royalties,
    # estates and trusts, the survey's only landlord proxy), else renter (rented or no cash rent),
    # else owner without rental income.
    landlord = d.HRNTVAL.ne(0).to_numpy()
    d["tenure"] = np.select([landlord, d.H_TENURE.isin([2, 3]).to_numpy()], ["landlord", "renter"],
                            "owner_no_rental_income")
    d["state3"] = np.select([d.st.eq(6), d.st.eq(48)], ["CA", "TX"], "rest")
    tw = pd.Series(d.pw.to_numpy()[target]).groupby(d.st.to_numpy()[target]).sum().sort_values(ascending=False)
    top10 = [FIPS[s] for s in tw.index[:10]]
    d["top10_states"] = np.where(d.st_ab.isin(top10), d.st_ab, "other_states")
    # Household reference person is an other resident (ACS "other renters" exclude households whose
    # householder is in the group; the CPS seed follows the same rule).
    ref = d.PERRP.isin([40, 41]).to_numpy()
    ref_other = pd.Series(np.where(ref, other, False)).groupby(d.PH_SEQ.to_numpy()).transform("max").to_numpy()
    n_other = d.groupby("PH_SEQ").other.transform("sum").to_numpy()
    d["hh_other_ref"] = ref_other & other
    d["n_other_hh"] = np.maximum(n_other, 1)
    d["earn"] = np.maximum(d.PEARNVAL.to_numpy(float), 0)
    d["wsal"] = np.maximum(d.WSAL_VAL.to_numpy(float), 0)
    d["semp"] = np.maximum(d.SEMP_VAL.to_numpy(float) + d.FRSE_VAL.to_numpy(float), 0)
    d["metro_worker"] = d.WORKYN.eq(1).to_numpy() & d.GTMETSTA.eq(1).to_numpy()
    d["uninsured_py"] = np.where(d.NOCOV_CYR.eq(3), 1.0, np.where(d.NOCOV_CYR.eq(2), 0.5, 0.0))
    return d, top10


# ================================================================== channel totals from lanes
def fiscal_inputs():
    """Adopted case by specification (specs.cjs) and its federal/state-local split at the band ends."""
    s = pd.read_csv(PATHS["specs"])
    bands = pd.read_csv(PATHS["bands"])
    bands = bands[bands.profile == "cbo_category_lag_non_school_full"].set_index("variant")
    out = {}
    for case, variant in (("adopted_2026_09_24", "adopted"), ("adopted_2026_09_23", "adopted_2026_09_23")):
        c = s[s.case == case]
        lo, hi = c.cost_bn.min(), c.cost_bn.max()
        gate(f"band_reproduced_{case}", np.isclose(lo, bands.loc[variant, "cost_low_bn"], atol=5e-5)
             and np.isclose(hi, bands.loc[variant, "cost_high_bn"], atol=5e-5),
             band=[lo, hi], published=[bands.loc[variant, "cost_low_bn"], bands.loc[variant, "cost_high_bn"]])
        gate(f"welfare_identity_{case}", np.allclose(c.welfare_bn, c.P_bn + c.A_bn + c.F_bn, atol=1e-9))
        ends = {}
        for end, v in (("low", lo), ("high", hi)):
            r = c[np.isclose(c.cost_bn, v, atol=1e-9)]
            # Specifications that tie at an end share A, P and F (they differ only in dimensions
            # that do not move the cost); take the first.
            if not (np.allclose(r.A_bn, r.A_bn.iloc[0]) and np.allclose(r.P_bn, r.P_bn.iloc[0])):
                raise SystemExit(f"[BLOCKED] tied band-end specifications differ in A or P ({case} {end})")
            ends[end] = r.iloc[0].to_dict()
        out[case] = dict(specs=c.reset_index(drop=True), ends=ends)
    return out


def fiscal_one_definition(B, fin):
    """The direct response A at each band end from the base lane's fiscal_totals (one definition for
    both lanes; it gates its own rebuilt band). It builds A from the published case plus each change,
    so it differs from this lane's engine run by rounding; the gap is recorded and must stay < 1e-3."""
    out = {}
    for case, arg in (("adopted_2026_09_24", "sept24"), ("adopted_2026_09_23", "sept23")):
        ft = B.fiscal_totals(arg)["adopted"]
        A = {"low": float(ft["A_low_cost"]), "high": float(ft["A_high_cost"])}
        e = fin[case]["ends"]
        diff = {end: A[end] - float(e[end]["A_bn"]) for end in ("low", "high")}
        gate(f"fiscal_totals_{arg}_matches_engine", all(abs(v) < 1e-3 for v in diff.values()), fiscal_totals=A,
             engine={end: float(e[end]["A_bn"]) for end in ("low", "high")}, diff=diff)
        fin[case]["A_one_definition"] = A
        out[case] = dict(A=A, engine_A={end: float(e[end]["A_bn"]) for end in ("low", "high")}, diff=diff,
                         A_mid=float(ft["A_mid"]))
    return out


def federal_split(fin):
    """Federal part of the fiscal channel at each band end, under the debt legacy lane's three payer
    conventions (low, central, high).

    Used: that lane's own split (derived/federal_split_2024.csv), so each correction's federal share
    is the one its per-correction file defines. Check: this lane's engine lines times that lane's
    per-line fractions, the correction rows (school_reprice, college_rekey, lane_constants) counted
    once as lines, less the induced receipts F at its federal share, reproduce its federal part and
    fiscal gap. On the September 24 case (DEBT24_COMMIT) the split is used; on the September 23 case
    (DEBT_COMMIT) the same recomputation is the method's positive control."""
    lines = pd.read_csv(PATHS["lines"])
    out, info = {}, {}
    for case, commit in (("adopted_2026_09_23", DEBT_COMMIT), ("adopted_2026_09_24", DEBT24_COMMIT)):
        dl = debt_csv("federal_split_2024_lines.csv", commit)
        split = debt_csv("federal_split_2024.csv", commit)
        f_ind = debt_json("summary.json", commit)["induced_receipts_federal_share_2024"]
        checks = {}
        for end in ("low", "high"):
            le = lines[(lines.case == case) & (lines.end == end)].set_index(["side", "line"])
            gate(f"line_ids_unique_{case}_{end}", le.index.is_unique)
            gap = -le.effect_bn                       # cost to other residents, by line
            F = fin[case]["ends"][end]["F_bn"]
            for conv in ("low", "central", "high"):
                frac = dl[(dl.end == end) & (dl.convention == conv)].set_index(["side", "line"])
                gate(f"debt_lines_unique_{case}_{end}_{conv}", frac.index.is_unique)
                # The lane lists the induced receipts as a line; this lane carries them as F.
                fk = ("production", "induced_receipts_F")
                if fk in frac.index:
                    gate(f"debt_lines_F_{case}_{end}_{conv}", np.isclose(frac.gap_bn[fk], -F, atol=1e-5)
                         and np.isclose(frac.federal_bn[fk], -F * f_ind, atol=1e-5),
                         lane=[float(frac.gap_bn[fk]), float(frac.federal_bn[fk])], engine=[-F, -F * f_ind])
                    frac = frac.drop(index=[fk])
                fr = (frac.federal_bn / frac.gap_bn).where(frac.gap_bn != 0, 0.0)
                # Every line with a responsive effect has a fraction, and every line the lane lists
                # is in the engine run (zero-response lines such as defense carry no effect).
                unknown = [k for k in gap.index if k not in fr.index and abs(gap[k]) > 1e-12]
                absent = [k for k in frac.index if k not in gap.index and abs(frac.gap_bn[k]) > 1e-12]
                if unknown or absent:
                    raise SystemExit(f"[BLOCKED] lines differ from the debt lane ({case} {end} {conv}): "
                                     f"without a fraction {unknown}; not in the engine run {absent}")
                common = gap.index.intersection(frac.index)
                line_diff = float((gap[common] - frac.gap_bn[common]).abs().max())
                fed = float((gap[common] * fr[common]).sum()) - F * f_ind
                cost = float(gap.sum()) - F
                ref = split[(split.profile == "cbo_category_lag_non_school_full") & (split.end == end)
                            & (split.convention == conv)]
                gate(f"debt_split_row_unique_{case}_{end}_{conv}", len(ref) == 1, rows=len(ref))
                ref = ref.iloc[0]
                gate(f"federal_split_recomputed_{case}_{end}_{conv}",
                     np.isclose(fed, ref.federal_bn, atol=1e-5) and np.isclose(cost, ref.fiscal_gap_bn, atol=1e-5)
                     and line_diff < 1e-5, recomputed=fed, lane=float(ref.federal_bn), cost=cost,
                     lane_cost=float(ref.fiscal_gap_bn), max_line_diff_bn=line_diff)
                row = dict(cost_bn=float(ref.fiscal_gap_bn), federal_bn=float(ref.federal_bn),
                           state_local_bn=float(ref.state_local_bn), federal_share=float(ref.federal_share),
                           recomputed_federal_bn=fed, max_line_diff_bn=line_diff)
                for syn in ("school_reprice", "college_rekey", "lane_constants"):
                    if ("spending", syn) in frac.index:
                        row[f"{syn}_bn"] = float(frac.gap_bn[("spending", syn)])
                        row[f"{syn}_federal_bn"] = float(frac.federal_bn[("spending", syn)])
                out[(case, end, conv)] = row
                checks[f"{end}_{conv}"] = [fed, float(ref.federal_bn)]
        info[case] = dict(commit=commit, induced_receipts_federal_share=f_ind, recomputed_vs_lane=checks)
    info["per_correction_file"] = per_correction_check()
    return out, info


def per_correction_check():
    """The debt lane's per-correction file against the correction rows of its lines file: the lane
    constants, and schools with colleges (its education_row6_and_school_price component)."""
    p = PATHS["debt_corrections"]
    if not p.is_file():
        print("  ! [DEGRADED] debt lane's corrections_federal_by_component_2024.csv absent; check not run")
        return dict(status="[DEGRADED] file absent at run time; check not run")
    comp = pd.read_csv(p)
    dl = debt_csv("federal_split_2024_lines.csv", DEBT24_COMMIT).set_index(["end", "convention", "side", "line"])
    worst, n = 0.0, 0
    for component, rows in (("lane_constants", ("lane_constants",)),
                            ("education_row6_and_school_price", ("school_reprice", "college_rekey"))):
        for r in comp[comp.component == component].itertuples():
            v = dl.loc[[(r.end, r.convention, "spending", x) for x in rows]]
            worst = max(worst, abs(v.federal_bn.sum() - r.federal_bn), abs(v.gap_bn.sum() - r.effect_bn))
            n += 1
    gate("debt_lines_carry_per_correction_split", n == 12 and worst < 1e-5, rows=n, max_abs_diff_bn=worst)
    return dict(status="checked", rows=n, max_abs_diff_bn=worst, sha256=file_sha(p))


def deficit_share_fy2024():
    """FY2024 federal deficit over federal outlays: OMB Historical Tables 2.1 (receipts) and 3.1
    (outlays), FY2027 budget release, pinned in sources/."""
    r = pd.read_excel(PATHS["omb_receipts"], header=None)
    row = r[r[0].astype(str).str.strip() == "2024"]
    receipts = float(row.iloc[0, 8])
    o = pd.read_excel(PATHS["omb_outlays"], header=None)
    col = [j for j, v in enumerate(o.iloc[1]) if str(v).strip() == "2024"][0]
    outlays = float(o[o[0].astype(str).str.strip() == "Total, Federal outlays"].iloc[0, col])
    gate("omb_fy2024_totals", 4.8e6 < receipts < 5.0e6 and 6.6e6 < outlays < 6.9e6, receipts_musd=receipts,
         outlays_musd=outlays)
    return dict(receipts_musd=receipts, outlays_musd=outlays, deficit_musd=outlays - receipts,
                share=(outlays - receipts) / outlays)


def crime_inputs(B):
    """Victims' harm only as a lane computed it, each with its footing: decision 4's $30.93bn (central;
    equal footing with the NIBRS mixed-group correction), the victim lane's equal footing ($28.92bn)
    and custody footing ($32.34bn), NIBRS's victim-conditional arm, and the victim lane's envelope."""
    off = pd.read_csv(B.PATHS["crime_offence"]).set_index("offence")
    arms = pd.read_csv(B.PATHS["crime_arms"]).set_index("arm")
    equal = float(off.loc["Total", "cost_full"]) / 1e9
    custody = float(arms.loc["scaling: ACS institutional ratio 1.118 (generic reallocated)", "full_bn"])
    de = pd.read_csv(PATHS["crime_dollar"])
    mixed = de[de.method.str.contains("theta 0.4977", regex=False)
               & de.method.str.contains("NIBRS TX+AZ mean Hispanic fraction of mixed groups", regex=False)]
    gate("crime_mixed_group_row_unique", len(mixed) == 1, rows=len(mixed))
    mixed_equal = float(mixed.full_bn.iloc[0])
    nib = pd.read_csv(PATHS["nibrs_cost"])
    nib_c = nib[(nib.spec == "central") & (nib.arm == "victim-conditional, SHR-calibrated")]
    gate("crime_nibrs_central_unique", len(nib_c) == 1, rows=len(nib_c))
    out = dict(equal=equal, custody=custody, mixed_equal=mixed_equal, nibrs_equal=float(nib_c.full_bn.iloc[0]),
               envelope_low=float(arms.loc["ENVELOPE low, miller2021", "full_bn"]),
               envelope_high=float(arms.loc["ENVELOPE high, miller2021_dot_vsl", "full_bn"]))
    gate("crime_inputs_pinned", np.isclose(equal, 28.9229, atol=5e-4) and np.isclose(custody, 32.3381, atol=5e-4)
         and np.isclose(mixed_equal, 30.9274, atol=5e-4), **{k: v for k, v in out.items()})
    out["footing"] = dict(
        mixed_equal="equal footing (Mexican-origin offending at NCVS Hispanic rates) with the NIBRS mixed-group "
                    "correction, theta 0.4977; decision 4's figure [crime_ratio_direction_2026_09_24]",
        equal="equal footing, no mixed-group correction; the victim lane's central [crime_victim_cost_2026_09_23]",
        custody="custody footing (ACS institutional ratio 1.118, generic Hispanic reallocated), no mixed-group "
                "correction [crime_victim_cost_2026_09_23]",
        nibrs_equal="NIBRS victim-conditional, SHR-calibrated [offender_ethnicity_nibrs_2026_09_23]",
        envelope_low="the victim lane's envelope, every arm at its low setting, Miller 2021 prices",
        envelope_high="the victim lane's envelope, every arm at its high setting, Miller 2021 prices with the "
                      "DOT 2024 VSL for murder")
    return out


def preference_inputs():
    ch = pd.read_csv(PATHS["preferences"])
    text = PATHS["preferences_log"].read_text()
    mex = {}
    for lev in LEVELS:
        m = re.search(rf"2024 {lev}\s*:.*?Mexican-origin \$([0-9.]+)bn", text)
        mex[lev] = float(m.group(1))
    regime = {lev: float(ch[f"y2024_{lev}"].sum()) for lev in LEVELS}
    ch["mex_central"] = ch.y2024_central * ch.mex_share
    parts = {"admissions": ch.mex_central[ch.channel.str.startswith("1 ")].sum(),
             "contractor_hiring": ch.mex_central[ch.channel.str.startswith("2 ")].sum(),
             "lost_profits": ch.mex_central[ch.channel.str.contains("lost profits")].sum(),
             "taxpayer_premium": ch.mex_central[ch.channel.str.contains("price premium")].sum()}
    gate("preferences_group_part_reproduced", np.isclose(sum(parts.values()), mex["central"], atol=0.006),
         parts=sum(parts.values()), lane=mex["central"])
    return dict(group_part=mex, regime=regime, parts={k: float(v) for k, v in parts.items()})


def congestion_inputs():
    arms = pd.read_csv(PATHS["congestion_arms"]).set_index("approach")
    b1 = arms.loc["B1 population elasticity, lanes fixed"]
    m = pd.read_csv(PATHS["congestion_metro"], dtype={"ua": str})
    u = pd.read_csv(PATHS["congestion_ua"], dtype={"ua": str})[["ua", "state"]].drop_duplicates("ua")
    m = m.merge(u, on="ua", how="left", validate="many_to_one")
    gate("congestion_ua_states", m.state.notna().all() and m.state.isin(POSTAL).all(),
         missing=int(m.state.isna().sum()))
    by_state = m.groupby("state").B1_bn.sum()
    gate("congestion_states_sum", np.isclose(by_state.sum(), b1.central_bn, rtol=1e-9),
         states=by_state.sum(), lane=float(b1.central_bn))
    return dict(total={"low": float(b1.min_bn), "central": float(b1.central_bn), "high": float(b1.max_bn)},
                state_share=(by_state / by_state.sum()).rename(index=POSTAL).to_dict())


def scale_inputs():
    s = pd.read_csv(PATHS["scale"])
    j = s[(s.table == "joint_grid") & (s.geography == "CZ 1990")].iloc[0]
    m = pd.read_csv(PATHS["scale_metro"])
    # Metro names carry the first-named state ("New York-Newark-Jersey City, NY-NJ" -> NY); the
    # non-metro remainder of each state is "nonCBSA_<FIPS>".
    st = m.name.str.extract(r",\s*([A-Z]{2})")[0].map(POSTAL)
    st = st.fillna(pd.to_numeric(m.name.str.extract(r"^nonCBSA_(\d+)$")[0], errors="coerce"))
    gate("scale_metro_states", st.notna().all() and st.isin(list(FIPS)).all(), missing=int(st.isna().sum()))
    by_state = m.net_bn.groupby(st.astype(int)).sum()
    total = dict(low=float(j.gain_low_bn), central=float(j.gain_bn), high=float(j.gain_high_bn))
    return dict(total=total, private_share=float(j.private_bn / j.gain_bn),
                receipts_share=float(j.induced_receipts_bn / j.gain_bn),
                state_share=(by_state / by_state.sum()).to_dict(), metro_total_bn=float(by_state.sum()))


def mobility_inputs():
    j = json.loads(PATHS["mobility"].read_text())
    ins = j["insurance_present_bn"]
    bor = j["borjas_bn"]["observed_2024_sorting"]
    tot = j["lane_total_present_bn"]
    for lev in LEVELS:
        gate(f"mobility_parts_add_{lev}", np.isclose(ins[lev] + bor[lev], tot[lev], atol=1e-9),
             parts=ins[lev] + bor[lev], total=tot[lev])
    return dict(insurance=ins, borjas=bor, total=tot)


def care_inputs():
    c = pd.read_csv(PATHS["care"]).set_index("channel")
    tot = c.loc["TOTAL of additive channels"]
    return dict(total={"low": float(tot.low_bn), "central": float(tot.central_bn), "high": float(tot.high_bn)},
                hours_taxes=float(c.loc["taxes on native women's extra hours (household-service channel)", "central_bn"]),
                elder_care=float(c.loc["elder care: Medicaid nursing-facility saving net of Medicaid home care", "central_bn"]),
                private_gain=float(c.loc["native women's private gain from the extra hours", "central_bn"]),
                consumer_surplus_net=float(c.loc["consumer surplus on immigrant-intensive services, net of native low-skill wage gain", "central_bn"]))


def debt_inputs(fin):
    """Interest on past gaps: the debt legacy lane's main benchmark, central payer convention,
    effective rate path, 2005 window, all borrowed, rule programme_income_pandemic_per_head, on the
    September 24 case (DEBT24_COMMIT); the September 23 values (DEBT_COMMIT, decision 4's $30.5-38.9bn)
    are kept for the record."""
    out = {}
    for case, commit, pinned in (("sept24", DEBT24_COMMIT, (28.3387, 36.4297)), ("sept23", DEBT_COMMIT, (30.4759, 38.8646))):
        s = debt_csv("stocks.csv", commit)
        main = s[(s.benchmark == "main") & (s.convention == "central") & (s.rate_path == "effective")
                 & (s.window_start == 2005) & (s.financing == "all_borrowed")]
        c = main[main.rule == "programme_income_pandemic_per_head"].set_index("end")
        lo, hi = float(c.loc["low", "legacy_interest_2024_bn"]), float(c.loc["high", "legacy_interest_2024_bn"])
        gate(f"debt_legacy_pinned_{case}", np.isclose(lo, pinned[0], atol=5e-4) and np.isclose(hi, pinned[1], atol=5e-4),
             low=lo, high=hi)
        # The lane's "range across the eleven back-cast rules on both anchors".
        out[case] = dict(low=lo, high=hi, central=(lo + hi) / 2, rules_min=float(main.legacy_interest_2024_bn.min()),
                         rules_max=float(main.legacy_interest_2024_bn.max()), commit=commit)
    band = debt_json("summary.json", DEBT24_COMMIT)["case"]["band"]
    ends = fin["adopted_2026_09_24"]["ends"]
    gate("debt_legacy_is_sept24_case", np.allclose(band, [ends["low"]["cost_bn"], ends["high"]["cost_bn"]], atol=5e-5),
         lane=band, engine=[ends["low"]["cost_bn"], ends["high"]["cost_bn"]])
    return dict(out["sept24"], sept23=out["sept23"])


def housing_inputs(I):
    """Ladder 190's housing range for other residents. Central: the metro-local arm's long-run
    central ($3.51bn net), the base lane's central and the geography this frame keys by state. The
    national-uniform arm's long-run central ($0.71bn) is the other end of the published range and a
    named variant. Low and high: the lowest and highest net in the lane's long-run grid (-$0.38bn,
    +$9.40bn). Each level's renters and landlords are spread by the cells and states of the
    form-A arm with the same elasticity level and geography, scaled to that level's totals."""
    head = pd.read_csv(PATHS["housing_headline"])
    head = head[(head.arm == "long_run") & (head.level == "central")].drop_duplicates("geography")
    head = {g: head[head.geography == g].iloc[0] for g in ("metro_local", "national_uniform")}
    grid = pd.read_csv(PATHS["housing_grid"])
    lr = grid[grid.arm == "long_run"]
    lo = lr.loc[lr.net_other_residents_welfare_bn.idxmin()]
    hi = lr.loc[lr.net_other_residents_welfare_bn.idxmax()]
    net = "net_other_residents_welfare_bn"
    gate("housing_is_ladder_190", np.isclose(head["national_uniform"][net], 0.708230, atol=5e-6)
         and np.isclose(head["metro_local"][net], 3.507579, atol=5e-6) and np.isclose(lo[net], -0.379246, atol=5e-6)
         and np.isclose(hi[net], 9.403796, atol=5e-6),
         centrals=[float(head["national_uniform"][net]), float(head["metro_local"][net])],
         span=[float(lo[net]), float(hi[net])])

    def level(r, pattern):
        a = I["arms"][pattern]
        return dict(renters_bn=float(r.other_renters_extra_rent_bn), net_bn=float(r[net]),
                    landlords_bn=float(r.other_renters_extra_rent_bn + r[net]),
                    owner_stock_bn=float(r.other_owner_value_gain_stock_bn), pattern=pattern,
                    pattern_scale=float(r.other_renters_extra_rent_bn / a["other_renters_extra_rent_bn"]),
                    row=f"long run, {r.level} elasticity, form {r.form}, {r.geography}, ownership {r.ownership}, "
                        f"leak {r.leak_other_occupied}, {r.rule}")
    for geo in ("metro_local", "national_uniform"):
        a = I["arms"][("central", geo)]
        gate(f"housing_central_is_base_arm_{geo}", np.isclose(a[net], head[geo][net], atol=1e-9)
             and np.isclose(a["other_renters_extra_rent_bn"], head[geo]["other_renters_extra_rent_bn"], atol=1e-9))
    return {"low": level(lo, (lo.level, lo.geography)),
            "central": level(head["metro_local"], ("central", "metro_local")),
            "high": level(hi, (hi.level, hi.geography)),
            "national_uniform_central": level(head["national_uniform"], ("central", "national_uniform"))}


def consumption_proposal(fin):
    """The consumption lane's proposed key (spec both_corridor_net_h2: consumption taxes keyed on CE
    spending by income rank, net of corridor-calibrated remittances). A proposal: it changes the
    fiscal total, never a net or the adopted total here."""
    j = json.loads(PATHS["consumption"].read_text())
    ends = fin["adopted_2026_09_24"]["ends"]
    band = [ends["low"]["cost_bn"], ends["high"]["cost_bn"]]
    gate("consumption_lane_on_adopted_band", np.allclose(j["adopted_band"], band, atol=5e-5), lane=j["adopted_band"],
         engine=band)
    sp = j["specs"]["both_corridor_net_h2"]
    ch = [float(x) for x in sp["change"]]
    gate("consumption_proposal_change", np.allclose(ch, np.subtract(sp["band"], j["adopted_band"]), atol=1e-9)
         and np.allclose(ch, -4.0517, atol=5e-4), change=ch, band=sp["band"])
    both = [float(v["change"][0]) for v in j["specs"].values() if v.get("family") == "both"]
    return dict(change=ch, band=[float(x) for x in sp["band"]], both_min=min(both), both_max=max(both),
                survey=float(j["specs"]["both_survey_cemla"]["change"][0]))


def banxico_remittances():
    """2024 remittances received in Mexico, from Banxico SIE table CE167 (quarterly $mn, revised; the
    consumption lane cites series SE43675, all countries, and SE43738, United States), read the way
    consumption_key_2026_09_24/remittance.py primary_flows() reads them and checked against that lane's
    committed corridor. Also that lane's reading: the corridor needs about 3.3 times the surveyed amount."""
    flows = pd.read_csv(PATHS["remittance_flows"]).set_index("spec")
    lane_us = float(re.search(r"\$([\d.]+)bn", flows.loc["corridor_full", "note"]).group(1))
    cemla = float(re.search(r"\$([\d,]+) a year", flows.loc["survey_cemla", "note"]).group(1).replace(",", ""))
    ratio = float(flows.loc["corridor_net_h2", "sent_per_expected_sending_union_unit"]) / cemla
    gate("corridor_needs_over_3x_surveyed_amounts", 3.2 < ratio < 3.5, ratio=ratio, cemla_usd=cemla)
    out = dict(lane_us_bn=lane_us, corridor_over_cemla=ratio, cemla_usd=cemla)
    path = PATHS["banxico_ce167"]
    if not path.is_file():
        print(f"  [DEGRADED] {path.name} absent: the US corridor is the consumption lane's committed ${lane_us}bn")
        return dict(out, source="[DEGRADED] consumption lane's remittance_flows.csv", us_bn=lane_us,
                    total_bn=None, us_share=None)
    import openpyxl
    rows = list(openpyxl.load_workbook(path, data_only=True).worksheets[0].iter_rows(values_only=True))

    def label(r):
        first = next((c for c in r if isinstance(c, str) and c.strip()), "") if r else ""
        return " ".join(first.replace("\u25cf", " ").split())
    head = next(r for r in rows if r and "Ene-Mar 2022" in r)
    cols = [i for i, c in enumerate(head) if isinstance(c, str) and c.endswith("2024")]
    total = next(r for r in rows if label(r) == "Total")
    us = next(r for r in rows if label(r) == "Estados Unidos")
    tot, usv = sum(float(total[i]) for i in cols) / 1e3, sum(float(us[i]) for i in cols) / 1e3
    gate("banxico_ce167_2024", any("CE167" in label(r) for r in rows[:12]) and len(cols) == 4
         and abs(usv - lane_us) < 5e-4, quarters=len(cols), us_bn=usv, total_bn=tot, lane_us_bn=lane_us)
    return dict(out, source="Banxico SIE CE167 (primary file)", us_bn=usv, total_bn=tot, us_share=usv / tot)


def published_totals(fin):
    """Ruling 5: the real-costs memo's totals at central values on the September 24 case, each crime
    footing on its own, as the propagation lane published them. This lane's allocation base mixes the
    footings and is never quoted as a total."""
    t = pd.read_csv(PATHS["real_costs"], dtype={"section": str})
    t = t[t.section == "7"].set_index(["column", "item"])
    v = lambda col, item: float(t.loc[(col, item), "sept24"])
    ends = ("low", "high")
    out = dict(equal=[v("hispanic_mixed_group", f"total at central values ({e})") for e in ends],
               equal_fiscal=[v("hispanic", f"fiscal main case ({e})") for e in ends],
               custody=[v("custody", f"total at central values ({e})") for e in ends],
               custody_fiscal=[v("custody", f"fiscal main case ({e})") for e in ends],
               custody_victims=v("custody", "victims' harm, full cost"),
               span=[v("full_span", "low end"), v("full_span", "high end")])
    out["range"] = [out["equal"][0], out["custody"][1]]
    a = fin["adopted_2026_09_24"]["ends"]
    bv = pd.read_csv(PATHS["band_variants"]).set_index(["case", "variant"])
    raw = [float(bv.loc[("sept24", "justice_raw_coding"), c]) for c in ("cost_low_bn", "cost_high_bn")]
    note = str(t.loc[("hispanic_mixed_group", "total at central values (low)"), "note"])
    out["equal_victims"] = float(re.search(r"victims ([\d.]+)", note).group(1))
    gate("published_totals_on_their_bands",
         np.allclose(out["custody_fiscal"], [a[e]["cost_bn"] for e in ends], atol=1e-3)
         and np.allclose(out["equal_fiscal"], raw, atol=1e-5), custody_fiscal=out["custody_fiscal"],
         equal_fiscal=out["equal_fiscal"], justice_raw_coding=raw)
    return out


# ================================================================== allocation helpers
def alloc(d, key, total_bn, mask=None):
    """$ per person record, proportional to key among other residents (and mask); sums to total_bn."""
    pw = d.pw.to_numpy()
    m = d.other.to_numpy() if mask is None else (d.other.to_numpy() & mask)
    k = np.where(m, key, 0.0)
    den = float((pw * k).sum())
    if total_bn == 0:
        return np.zeros(len(d))
    if den <= 0:
        raise SystemExit("[BLOCKED] empty distribution key")
    return total_bn * 1e9 * k / den


def alloc_states(d, key, state_bn: dict, mask=None, fallback=None, notes=None, label=""):
    """State totals ($bn by FIPS) spread within each state by key among other residents (and mask).
    A state where that key is empty falls back to `fallback` under the same mask, then to every
    other resident of the state; each fallback is recorded in `notes`."""
    out = np.zeros(len(d))
    st, pw, other = d.st.to_numpy(), d.pw.to_numpy(), d.other.to_numpy()
    for s, tot in state_bn.items():
        if tot == 0:
            continue
        ms = st == s
        mm = ms if mask is None else ms & mask
        for step, (k, m) in enumerate(((key, mm), (fallback, mm), (np.ones(len(d)), ms))):
            if k is None:
                continue
            if (pw * np.where(other & m, k, 0)).sum() > 0:
                out += alloc(d, k, tot, m)
                if step and notes is not None:
                    notes.setdefault("state_fallbacks", []).append(f"{label}: {FIPS.get(s, s)} step {step}")
                break
        else:
            raise SystemExit(f"[BLOCKED] no other residents in state {s}")
    return out


def rake(seed, cell, state, cell_t, state_t, iters=2000, tol=1e-10):
    """Iterative proportional fitting of record totals x (seed x pw) to income-cell and state margins."""
    x = seed.astype(float).copy()
    ct, stt = np.asarray(cell_t, float), np.asarray(state_t, float)
    for it in range(iters):
        cs = np.bincount(cell, weights=x, minlength=len(ct))
        x *= np.divide(ct, cs, out=np.zeros_like(ct), where=cs > 0)[cell]
        ss = np.bincount(state, weights=x, minlength=len(stt))
        x *= np.divide(stt, ss, out=np.zeros_like(stt), where=ss > 0)[state]
        cs = np.bincount(cell, weights=x, minlength=len(ct))
        err = max(np.abs(cs - ct).max() / max(np.abs(ct).max(), 1), 0.0)
        if err < tol:
            return x, it + 1, err
    return x, iters, err


def to_cells100(cells1000):
    return np.asarray(cells1000).reshape(100, 10).sum(axis=1)


# ================================================================== ACS with states (mirrors the base)
def acs_geo(B, acs, arms):
    """The base lane's ACS rent and owner-value channels, kept by state as well as by percentile
    cell (distribute.py acs_channels, same ranking and exposure)."""
    P, H = acs["persons"], acs["households"]
    head = P[P["head"]].drop_duplicates("SERIALNO").set_index("SERIALNO")["p1"]
    H = H.assign(head_p1=H.SERIALNO.map(head))
    H["y"] = H.hinc / np.sqrt(H.np)
    y_of = H.set_index("SERIALNO")["y"]
    ref = P[~P.p1 & ~P.gq].copy()
    ref["y"] = ref.SERIALNO.map(y_of)
    ref["p"] = B.position_rank(ref.y.to_numpy(), ref.pw.to_numpy(), pd.factorize(ref.SERIALNO)[0])
    H["p"] = H.SERIALNO.map(ref.groupby("SERIALNO").p.mean())
    H = H[~(H.p.isna() & H.head_p1.astype(bool))].copy()
    H["cell"] = B.bins(H.p.to_numpy(), B.CELLS)
    alloc_x = B.puma_exposure(H)
    s_nat = B.TARGET_TOTAL / 340.110988e6
    renters = (H.ten.eq(3) & ~H.head_p1.astype(bool)).to_numpy()
    owners = (H.ten.isin([1, 2]) & ~H.head_p1.astype(bool)).to_numpy()
    key = (H.STATE + "|" + H.PUMA).to_numpy()
    st = H.STATE.astype(int).to_numpy()
    out = {}
    for (level, geography), r in arms.items():
        e = r["elasticity"]
        if geography == "metro_local":
            a = alloc_x.assign(f=alloc_x.afact * (1 - (1 - alloc_x.group_share) ** e))
            f = pd.Series(key).map(a.groupby(a.state + "|" + a.puma).f.sum()).to_numpy()
        else:
            f = np.full(len(H), 1 - (1 - s_nat) ** e)
        rent_x = np.where(renters, f * H.rent.to_numpy() * H.wgtp.to_numpy(), 0.0)
        value_x = np.where(owners, f * H.value.to_numpy() * H.wgtp.to_numpy(), 0.0)
        out[(level, geography)] = dict(
            rent_cells=np.bincount(H.cell, weights=rent_x, minlength=B.CELLS),
            value_cells=np.bincount(H.cell, weights=value_x, minlength=B.CELLS),
            rent_state=pd.Series(rent_x).groupby(st).sum().to_dict(),
            value_state=pd.Series(value_x).groupby(st).sum().to_dict())
    return out


# ================================================================== tax keys by government level
def tax_parts(B, d, R, ranking, F, S):
    """distribute.py tax_key split into its federal (CBO shares) and state-local (ITEP rates) parts."""
    civ, pw = d.civ.to_numpy(), d.pw.to_numpy()
    base = np.where(civ, np.maximum(d.money_pc.to_numpy(float), 0), 0.0)
    g = np.where(civ, np.searchsorted(B.CBO_EDGES[1:-1], np.nan_to_num(R["p_all"]), side="right"), -1)
    fed_share = np.array(B.CBO_FED_SHARE[ranking]) / sum(B.CBO_FED_SHARE[ranking])
    sl_group = np.array(B.ITEP_RATE) * np.array(B.CBO_INCOME_SHARE[ranking])
    sl_share = sl_group / sl_group.sum()
    fed, sl = np.zeros(len(d)), np.zeros(len(d))
    for k in range(len(B.CBO_GROUPS)):
        m = g == k
        den = float((pw[m] * base[m]).sum())
        fed[m] = fed_share[k] * base[m] / den
        sl[m] = sl_share[k] * base[m] / den
    return F * fed, S * sl


# ================================================================== key templates (sister lanes)
KEY_TEMPLATES = [
    ("per_person", "every other resident, equally", "CPS ASEC 2025 person weight"),
    ("taxes", "all taxes paid, federal and state-local (ladder 194's convention (a))", "CBO 2022 shares, ITEP rates, CPS money income"),
    ("federal_taxes", "federal taxes paid (CBO 2022 shares by income group)", "CPS money income per capita within group"),
    ("state_local_taxes", "state and local taxes paid (ITEP average rates)", "CPS money income per capita within group"),
    ("workers", "earnings of other-resident workers", "PEARNVAL > 0"),
    ("industry_owner:<NAICS>", "self-employment and farm income of persons whose longest job was in that NAICS (prefix match through the Census 2022 industry crosswalk)", "SEMP_VAL + FRSE_VAL > 0, INDUSTRY"),
    ("industry_worker:<NAICS>", "wage and salary earnings of workers whose longest job was in that NAICS", "WSAL_VAL > 0, INDUSTRY"),
    ("public_school_pupils", "persons aged 5-17, equally (CPS has no school-type item); ':q1'..':q5' restricts to an SPM income quintile as a stand-in for district income", "A_AGE 5-17"),
    ("interstate_movers:<ST>", "persons who lived in state ST a year earlier and now live in another state", "MIG_ST, GESTFIPS, MIGSAME = 2"),
    ("commuters", "workers in metropolitan households, equally", "WORKYN = 1, GTMETSTA = 1"),
    ("renters", "persons in cash-rent households headed by an other resident, one share per household", "H_TENURE = 2, PERRP"),
    ("landlords", "persons in households reporting rental income or loss, by its absolute value (gross rents are not observed)", "HRNTVAL != 0"),
    ("owners", "persons in owner-occupied households headed by an other resident, one share per household", "H_TENURE = 1"),
    ("nh_white_natives", "US-born non-Hispanic white residents, equally", "PEHSPNON = 2, PRDTRACE = 1, PRCITSHP 1-3"),
    ("privately_insured", "persons with private health coverage, equally", "PRIV = 1"),
]
TEMPLATE_NOTE = ("Any template takes '@ST' (postal code) to restrict it to residents of one state, "
                 "for example industry_worker:7225@CA or renters@TX.")


def naics_crosswalk():
    """Census 2022 industry codes with their NAICS equivalents, from the Bureau's crosswalk."""
    if not PATHS["census_industry"].exists():
        SOURCES.mkdir(parents=True, exist_ok=True)
        subprocess.run(["curl", "-sS", "--fail", "-A", "Mozilla/5.0", "-o", str(PATHS["census_industry"]),
                        CENSUS_INDUSTRY_URL], check=True)
    t = pd.read_excel(PATHS["census_industry"], sheet_name="2022 Census Ind Code List ", header=None)
    rows = []
    for _, r in t.iterrows():
        code, naics, desc = str(r[3]).strip(), str(r[4]).strip(), str(r[1]).strip()
        if not re.fullmatch(r"\d{4}", code):
            continue
        for part in naics.split(","):
            part = part.replace("Part of", "").replace("pt.", "").strip()
            base = re.match(r"(\d+)", part)
            if not base:
                continue
            exc = re.findall(r"(\d+)", part.split("exc.")[1]) if "exc." in part else []
            rows.append(dict(census_code=int(code), naics=base.group(1), exclude=" ".join(exc), description=desc))
    x = pd.DataFrame(rows)
    gate("census_industry_crosswalk_parsed", len(x) > 250 and {770, 8680, 7770, 9290}.issubset(set(x.census_code)),
         rows=len(x))
    return x


def census_codes_for(naics: str, xw: pd.DataFrame) -> list[int]:
    hits = []
    for r in xw.itertuples():
        if (r.naics.startswith(naics) or naics.startswith(r.naics)) and not any(
                naics.startswith(e) for e in r.exclude.split() if e):
            hits.append(r.census_code)
    return sorted(set(hits))


def resolve_key(template: str, d: pd.DataFrame, ctx: dict) -> tuple[np.ndarray, np.ndarray, str]:
    """A key template -> (key values, mask over persons, description). Raises ValueError if unknown."""
    t = template.strip()
    state = None
    if "@" in t:
        t, st = t.split("@", 1)
        if st not in POSTAL:
            raise ValueError(f"unknown state in {template}")
        state = POSTAL[st]
    name, _, arg = t.partition(":")
    other = d.other.to_numpy()
    ones = np.ones(len(d))
    if name == "per_person":
        key, mask = ones, other
    elif name == "taxes":
        key, mask = ctx["tax_fed"] + ctx["tax_sl"], other
    elif name == "federal_taxes":
        key, mask = ctx["tax_fed"], other
    elif name == "state_local_taxes":
        key, mask = ctx["tax_sl"], other
    elif name == "workers":
        key, mask = d.earn.to_numpy(), other
    elif name in ("industry_owner", "industry_worker"):
        if not re.fullmatch(r"\d{2,6}", arg):
            raise ValueError(f"NAICS code expected in {template}")
        codes = census_codes_for(arg, ctx["naics"])
        if not codes:
            raise ValueError(f"no Census industry code for NAICS {arg}")
        key = d.semp.to_numpy() if name == "industry_owner" else d.wsal.to_numpy()
        mask = d.INDUSTRY.isin(codes).to_numpy() & other & (key > 0)
    elif name == "public_school_pupils":
        mask = other & d.A_AGE.between(5, 17).to_numpy()
        if arg:
            q = re.fullmatch(r"q([1-5])", arg)
            if not q:
                raise ValueError(f"quintile expected in {template}")
            mask &= ctx["q5"] == int(q.group(1)) - 1
        key = ones
    elif name == "interstate_movers":
        if arg not in POSTAL:
            raise ValueError(f"origin state expected in {template}")
        s = POSTAL[arg]
        mask = other & d.MIG_ST.eq(s).to_numpy() & d.st.ne(s).to_numpy() & d.MIGSAME.eq(2).to_numpy()
        key = ones
    elif name == "commuters":
        key, mask = ones, other & d.metro_worker.to_numpy()
    elif name == "renters":
        key, mask = 1.0 / d.n_other_hh.to_numpy(), other & d.H_TENURE.eq(2).to_numpy() & d.hh_other_ref.to_numpy()
    elif name == "owners":
        key, mask = 1.0 / d.n_other_hh.to_numpy(), other & d.H_TENURE.eq(1).to_numpy() & d.hh_other_ref.to_numpy()
    elif name == "landlords":
        key = np.abs(d.HRNTVAL.to_numpy(float)) / d.n_other_hh.to_numpy()
        mask = other & (key > 0)
    elif name == "nh_white_natives":
        key, mask = ones, other & d.race5.eq("nh_white").to_numpy() & d.native.to_numpy()
    elif name == "privately_insured":
        key, mask = ones, other & d.PRIV.eq(1).to_numpy()
    else:
        raise ValueError(f"unknown key template {template}")
    if state is not None:
        mask = mask & (d.st.to_numpy() == state)
    if (d.pw.to_numpy() * np.where(mask, key, 0)).sum() <= 0:
        raise ValueError(f"key {template} is empty on CPS ASEC 2025")
    return key, mask, template


def load_key_map():
    km = pd.read_csv(HERE / "key_map.csv", dtype=str).fillna("")
    return km


def map_row_to_key(lane: str, row: dict, km: pd.DataFrame) -> tuple[str, str]:
    """(key template, how it was chosen). An explicit `key` column wins; then key_map.csv patterns
    for the lane (first match); '' if no defensible key."""
    explicit = str(row.get("key", "") or "").strip()
    if explicit:
        return explicit, "key column"
    text = f"{row.get('group', '')} | {row.get('channel', '')}"
    for r in km[(km.lane == lane) | (km.lane == "*")].itertuples():
        if re.search(r.group_regex, str(row.get("group", "")), flags=re.I) and (
                not r.channel_regex or re.search(r.channel_regex, str(row.get("channel", "")), flags=re.I)):
            key = r.key
            if "<NAICS>" in key:
                code = re.search(r"NAICS\s*:?\s*(\d{2,6})", text, flags=re.I)
                if not code:
                    code_word = [c for w, c in INDUSTRY_WORDS.items() if re.search(w, text, flags=re.I)]
                    if not code_word:
                        return "", f"key_map row '{r.group_regex}' needs a NAICS code"
                    key = key.replace("<NAICS>", code_word[0])
                else:
                    key = key.replace("<NAICS>", code.group(1))
            if "<ST>" in key:
                named = [c for w, c in STATE_WORDS.items() if re.search(w, text, flags=re.I)]
                st = re.search(r"\b(" + "|".join(POSTAL) + r")\b", text)
                key = key.replace("<ST>", named[0] if named else (st.group(1) if st else r.default_state))
            return key, f"key_map: {r.note or r.group_regex}"
    return "", "no key_map pattern"


INDUSTRY_WORDS = {r"restaurant|eating place|food service": "7225", r"food truck|mobile food": "722330",
                  r"construction|contractor|trades": "23", r"landscap": "561730", r"janitor": "561720",
                  r"private household|domestic": "814", r"agricultur|farm": "11", r"grocer": "4451"}
STATE_WORDS = {r"californ|los angeles|\bcity of la\b|\bL\.A\.": "CA", r"texas": "TX", r"new york": "NY",
               r"illinois": "IL", r"arizona": "AZ", r"florida": "FL"}


REGIONS = {"Northeast": (1, 2), "Midwest": (3, 4), "South": (5, 6, 7), "West": (8, 9)}


def counterfactual_is_absence(text) -> bool:
    """True when a sister row's counterfactual is the account's: the group (or its pupils) absent."""
    t = str(text)
    return bool(ABSENCE.search(t)) and not NOT_ABSENCE.search(t)


def check_sister_counterfactuals(tbl: pd.DataFrame):
    """Gate: every allocated sister row is on the account's counterfactual; the run stops otherwise."""
    alloc_ = tbl[tbl.status == "allocated"] if "status" in tbl else tbl.iloc[0:0]
    bad = [f"{r.lane}:{r.row}" for r in alloc_.itertuples() if not counterfactual_is_absence(r.counterfactual)]
    gate("sister_allocated_rows_on_account_counterfactual", not bad, allocated=len(alloc_), off_counterfactual=bad)


def sister_other_counterfactuals(tbl: pd.DataFrame) -> pd.DataFrame:
    """Sister rows whose counterfactual is not the group's absence, each under its own counterfactual;
    they are never in a net."""
    cols = ["lane", "row", "counterfactual", "group", "channel", "direction", "bn_low", "bn_central", "bn_high",
            "relation_to_account", "basis", "status"]
    if "counterfactual_is_absence" not in tbl:
        return pd.DataFrame(columns=cols)
    return tbl[tbl.counterfactual_is_absence.eq(False)][cols].sort_values(["lane", "row"])


def lane_verdict(lane_dir: Path) -> str:
    """First line of the sister lane's RESULT.md at run time (its rows are provisional until final)."""
    p = lane_dir / "RESULT.md"
    if not p.exists():
        return "no RESULT.md"
    for line in p.read_text().splitlines():
        if line.strip():
            return line.strip()[:160]
    return "empty RESULT.md"


def ingest_sisters(d, ctx, km, lanes=None):
    """Read each sister lane's winners_losers_rows.csv if present. Returns (role table, person-level
    amounts of the allocated rows). A row is allocated only if it is priced, a gain or a loss, beside
    the account, on the account's counterfactual (the group's or its pupils' absence) and mapped to a
    key template; every other row stays in the role table. When the lane
    also gives a regional breakdown of an allocated row (group '<group>:region=<Census region>',
    relation 'overlaps:<channel>') that sums to it, the row is spread by those regional shares."""
    rows, amounts, used = [], {}, {}
    pw = d.pw.to_numpy()
    region_of = d.st.map(DIVISION).map({v: k for k, vs in REGIONS.items() for v in vs}).to_numpy()
    for lane_dir, rid in (lanes or SISTERS).items():
        base = FISCAL / lane_dir
        path = base / "derived" / "winners_losers_rows.csv"
        verdict = lane_verdict(base)
        if not path.exists():
            rows.append(dict(lane=lane_dir, registry_id=rid, status="pending", note="file absent at run time",
                             lane_verdict=verdict))
            continue
        t = pd.read_csv(path, dtype=str).fillna("")
        missing = [c for c in SISTER_COLUMNS if c not in t.columns]
        if missing:
            rows.append(dict(lane=lane_dir, registry_id=rid, status="pending", lane_verdict=verdict,
                             note=f"file present but missing columns {missing}", sha256=file_sha(path)))
            continue
        first = len(rows)
        for i, r in t.iterrows():
            r = r.to_dict()
            rec = dict(lane=lane_dir, registry_id=rid, row=i, sha256=file_sha(path), lane_verdict=verdict,
                       **{c: r[c] for c in SISTER_COLUMNS})
            rec["counterfactual_is_absence"] = counterfactual_is_absence(r["counterfactual"])
            if "key" in t.columns:
                rec["key_column"] = r["key"]
            vals = {}
            for lev in LEVELS:
                try:
                    vals[lev] = float(r[f"bn_{lev}"]) if str(r[f"bn_{lev}"]).strip() != "" else np.nan
                except ValueError:
                    vals[lev] = np.nan
            direction = str(r["direction"]).strip().lower()
            relation = str(r["relation_to_account"]).strip().lower()
            # Two conventions occur. A row whose central is zero or positive gives amounts along its
            # direction (a loss of 16, with a low end of -2 meaning a gain of 2). A loss row with a
            # negative central gives signed changes to the payers (negative = worse off). A gain row
            # with a negative central is ambiguous and stays in the role table.
            signed = not np.isnan(vals["central"]) and vals["central"] < 0
            if np.isnan(vals["central"]) or str(r["basis"]).strip().lower() == "unpriced":
                rec.update(status="role_only", note="unpriced or no central value")
            elif direction not in ("gain", "loss"):
                rec.update(status="role_only", note=f"direction '{direction}' is not gain or loss")
            elif signed and direction == "gain":
                rec.update(status="role_only", note="a gain with a negative central value is ambiguous")
            elif relation == "inside" or relation.startswith("overlaps"):
                rec.update(status="role_only", note=f"relation '{relation}': inside the account or overlapping; "
                                                    "shown, never added to the nets")
            elif not rec["counterfactual_is_absence"]:
                rec.update(status="role_only", note="its counterfactual is not the group's absence, the account's; "
                                                    "listed under its own in sister_other_counterfactuals.csv, "
                                                    "never in a net")
            else:
                key, how = map_row_to_key(lane_dir, r, km)
                if not key:
                    rec.update(status="role_only", note=f"no defensible key ({how})")
                else:
                    try:
                        k, m, _ = resolve_key(key, d, ctx)
                    except ValueError as e:
                        rec.update(status="role_only", note=f"key {key} rejected: {e}")
                    else:
                        sign = 1.0 if direction == "gain" else -1.0
                        cid = f"sister:{rid}:{i}"
                        vv = {lev: (vals[lev] if not np.isnan(vals[lev]) else vals["central"]) for lev in LEVELS}
                        amt = {lev: (vv[lev] if signed else sign * vv[lev]) for lev in LEVELS}
                        amounts[cid] = {lev: alloc(d, k, amt[lev], m) for lev in LEVELS}
                        rec["values_read_as"] = "signed changes" if signed else "amounts along the direction"
                        rec["key_records"] = int((m & (k > 0)).sum())
                        if rec["key_records"] < 30:
                            note_thin = f"; thin key: {rec['key_records']} CPS records"
                        else:
                            note_thin = ""
                        used[cid] = (k, m, amt, str(r["group"]).strip(), str(r["channel"]).strip())
                        pop = float((pw * m).sum() / 1e6)
                        try:
                            ratio = pop / float(r["population_m"])
                        except (ValueError, ZeroDivisionError):
                            ratio = np.nan
                        note = "beside the account; proposed"
                        if lane_dir in LANE_LABELS:
                            note += f"; {LANE_LABELS[lane_dir]}"
                        if np.isfinite(ratio) and not 0.5 <= ratio <= 2.0:
                            note += (f"; the key covers {pop:.2f}m persons against the row's {r['population_m']}m "
                                     "(the row's group is not identifiable in CPS, or the payers differ from it)")
                        rec.update(status="allocated", key=key, key_chosen_by=how, channel_id=cid,
                                   key_population_m=pop, key_population_over_row=ratio, note=note + note_thin)
            rows.append(rec)
        # Regional breakdowns of allocated rows.
        for cid, (k, m, amt, grp, chan) in list(used.items()):
            if not cid.startswith(f"sister:{rid}:"):
                continue
            parts = {}
            for rec in rows[first:]:
                g = str(rec.get("group", ""))
                if (g.startswith(f"{grp}:region=") and str(rec.get("relation_to_account", "")).strip()
                        == f"overlaps:{chan}"):
                    try:
                        parts[g.split("region=", 1)[1].strip()] = float(rec["bn_central"])
                    except ValueError:
                        pass
            if not parts:
                continue
            rec = next(x for x in rows[first:] if x.get("channel_id") == cid)
            ok = set(parts) <= set(REGIONS) and np.isclose(abs(sum(parts.values())), abs(amt["central"]), rtol=0.01,
                                                           atol=1e-6)
            if not ok:
                rec["note"] += "; regional breakdown present but not used (regions unknown or not summing)"
                continue
            tot = sum(parts.values())
            amounts[cid] = {lev: sum(alloc(d, k, amt[lev] * v / tot, m & (region_of == reg))
                                     for reg, v in parts.items()) for lev in LEVELS}
            rec["note"] += "; spread by the lane's regional breakdown (" + ", ".join(
                f"{reg} {v / tot:.1%}" for reg, v in parts.items()) + ")"
    for cid, (k, m, amt, grp, chan) in used.items():
        for lev in LEVELS:
            got = float((pw * amounts[cid][lev]).sum() / 1e9)
            gate(f"closure_{cid}_{lev}", np.isclose(got, amt[lev], rtol=1e-9, atol=1e-9), persons=got, row=amt[lev])
    tbl = pd.DataFrame(rows)
    check_sister_counterfactuals(tbl)
    return tbl, amounts


# ================================================================== inputs the base lane reads
def base_inputs(B, d):
    B.verify_published_text()
    ncvs_ok = B.verify_ncvs_text()
    I = dict(ncvs_verified=ncvs_ok)
    I["fiscal23"] = B.fiscal_totals()
    I["F_total"], I["S_total"] = B.bea_totals()
    I["rates"] = B.ncvs_rates()
    nest = B.nest_rows()
    I["central"] = B.pick(nest, "below_ba", 2.0, 1.0, np.inf)
    I["account"] = B.pick(nest, "hs_or_less", 2.0, 1.0, np.inf)
    I["eps3_bb"] = B.pick(nest, "below_ba", 2.0, 1.0, 3.0)
    I["eps3_hs"] = B.pick(nest, "hs_or_less", 2.0, 1.0, 3.0)
    gate("account_production_term", np.isclose(I["account"].private_plus_receipts_bn, I["fiscal23"]["PF_cash"], rtol=1e-9),
         nest=I["account"].private_plus_receipts_bn, account=I["fiscal23"]["PF_cash"])
    # GDP normalization rows of the same scenarios (the base lane keeps cash only).
    s = pd.read_csv(B.PATHS["nest"])
    s = s[(s.excluded_capital_owner_share == 0) & (s.nest_option == "A_by_nativity") & (s.proxy == "PEARNVAL")
          & (s.labor_supply_elasticity == 0) & (s.capital_tax_retention == 1.0) & (s.labor_share == 0.65)
          & (s.sigma == 2.0) & (s.capital_adjustment == 1.0) & (s.normalization == "gdp")]
    I["account_gdp"] = s[(s.split == "hs_or_less") & (s.sigma_NI == np.inf)].iloc[0]
    I["eps3_hs_gdp"] = s[(s.split == "hs_or_less") & (s.sigma_NI == 3.0)].iloc[0]
    I["basis"] = {sp: B.wage_basis(d, sp) for sp in ("below_ba", "hs_or_less")}
    pw = d.pw.to_numpy()
    branches = pd.read_csv(B.PATHS["branches"])
    for split in I["basis"]:
        for (tag, c), e in I["basis"][split].items():
            name = "native_non_union" if tag == "native" else "other_foreign_born"
            ref = branches[(branches.proxy == "PEARNVAL") & (branches.split == split) & (branches.skill == c)
                           & (branches.branch == name)].earnings_estimate.iloc[0]
            gate(f"wage_base_{split}_{tag}_cell{c}", np.isclose((pw * e).sum(), ref, rtol=1e-9),
                 cps=(pw * e).sum() / 1e9, nest=ref / 1e9)
    ha = pd.read_csv(B.PATHS["housing_arms"]).drop_duplicates(["arm", "level", "form", "geography", "ownership"])
    ha = ha[(ha.arm == "long_run") & (ha.form == "A") & (ha.ownership == "central")]
    I["arms"] = {(r.level, r.geography): r._asdict() for r in ha.itertuples()}
    acs = B.acs_extract()
    I["acs"] = B.acs_channels(acs, I["arms"])
    I["acs_geo"] = acs_geo(B, acs, I["arms"])
    for k in I["arms"]:
        gate(f"acs_geo_mirrors_base_{k[0]}_{k[1]}", np.allclose(I["acs_geo"][k]["rent_cells"], I["acs"][k]["rent_cells"],
             rtol=1e-12, atol=1e-3) and np.allclose(I["acs_geo"][k]["value_cells"], I["acs"][k]["value_cells"], rtol=1e-12, atol=1e-3))
    I["scf"], I["scf_info"] = B.scf_cells()
    off = pd.read_csv(B.PATHS["crime_offence"]).set_index("offence")
    serious = ["Murder", "Rape/sexual assault", "Robbery", "Aggravated assault"]
    I["serious_share"] = float(off.loc[serious, "cost_full"].sum() / off.loc["Total", "cost_full"])
    htot = d.HTOTVAL.to_numpy(float)
    m12 = d.civ.to_numpy() & (d.A_AGE.to_numpy() >= 12)
    p12 = np.full(len(d), np.nan)
    p12[m12] = B.position_rank(htot[m12], pw[m12])
    I["keys_rank"], _ = B.crime_key(d, p12, I["rates"], "rank")
    unc = pd.read_csv(B.PATHS["uncompensated"])
    eq = unc[unc.use_intensity == 1.0]
    I["unreimbursed"] = {"low": float(eq.outside_accounts_bn.min()), "high": float(eq.outside_accounts_bn.max())}
    I["unreimbursed"]["central"] = (I["unreimbursed"]["low"] + I["unreimbursed"]["high"]) / 2
    cex = pd.read_csv(B.PATHS["cex"])
    cex = cex[(cex.arm == "published_jpe_2008") & (cex.shock == "lf_adjusted") & (cex.scope == "narrow_immigrant_intensive")].iloc[0]
    I["cex_q"] = np.array([cex[f"loss_bn_{k}"] for k in ("q1_lowest", "q2_second", "q3_third", "q4_fourth", "q5_highest")])
    I["R_money"] = B.rank_frame(d, "money")
    I["R_spm"] = B.rank_frame(d, "spm")
    return I


def crime_split(B, d, keys, total, s_share):
    return B.per_person(d, keys["serious"], -total * s_share) + B.per_person(d, keys["simple"], -total * (1 - s_share))


def consumer_side_view(d, I):
    pw, other = d.pw.to_numpy(), d.other.to_numpy()
    qm = I["R_money"]["q5"]
    cx = np.zeros(len(d))
    for q in range(5):
        m = other & (qm == q)
        cx[m] = I["cex_q"][q] * 1e9 / pw[m].sum()
    return cx


# ================================================================== regression: the base lane's tables
def regression(B, d, I, case):
    """The base lane's central channels rebuilt by this lane's code, with the fiscal channel at
    fiscal_totals(case) A_mid plus the base's central induced receipts, compared with that lane's
    channel_by_quintile.csv on the same case (September 23 at SEPT23_COMMIT, September 24 at
    BASE_COMMIT)."""
    commit = {"sept23": SEPT23_COMMIT, "sept24": BASE_COMMIT}[case]
    expected = pd.read_csv(io.BytesIO(git_show(f"{BASE_REL}/derived/channel_by_quintile.csv", commit)))
    held = json.loads(git_show(f"{BASE_REL}/derived/inputs.json", commit))["fiscal"]
    fa = B.fiscal_totals(case)["adopted"]
    gate(f"regression_target_is_{case}", held.get("case", "sept23") == case
         and np.isclose(held["adopted"]["A_mid"], fa["A_mid"], atol=1e-9), target_case=held.get("case", "sept23"),
         target_A_mid=held["adopted"]["A_mid"], A_mid=fa["A_mid"])
    F_c = float(I["central"].induced_current_receipts_bn)
    a_c = I["arms"][("central", "metro_local")]
    crime_custody = crime_inputs(B)["custody"]
    rows = []
    for measure in B.MEASURES:
        R = I["R_money"] if measure == "money" else I["R_spm"]
        ranking = "after" if measure == "spm" else "before"
        tax, _ = B.tax_key(d, R, ranking, I["F_total"], I["S_total"])
        ch = {}
        for conv, key in (("a", tax), ("b", np.ones(len(d)))):
            ch[f"fiscal_{conv}"] = B.per_person(d, key, fa["A_mid"] + F_c)
        ch["wages"] = B.wage_delta(I["basis"]["below_ba"], I["central"], True)
        ch["renters"] = -B.spread_cells(I["acs"][("central", "metro_local")]["rent_cells"], R, d)
        tot = a_c["other_renters_extra_rent_bn"] + a_c["net_other_residents_welfare_bn"]
        li = B.per_person(d, B.spread_cells(I["acs"]["intp_cells"], R, d), tot)
        ls = B.per_person(d, B.spread_cells(I["scf"], R, d), tot)
        ch["landlords"] = (li + ls) / 2
        ch["crime"] = crime_split(B, d, I["keys_rank"], crime_custody, I["serious_share"])
        ch["unreimbursed_care"] = B.per_person(d, d.PRIV.eq(1).to_numpy().astype(float), -I["unreimbursed"]["central"])
        ch["housing_net"] = ch["renters"] + ch["landlords"]
        parts = ["wages", "renters", "landlords", "crime", "unreimbursed_care"]
        for conv in ("a", "b"):
            ch[f"TOTAL_{conv}"] = ch[f"fiscal_{conv}"] + sum(ch[p] for p in parts)
        ch["wages_eps3"] = B.wage_delta(I["basis"]["below_ba"], I["eps3_bb"], True)
        ch["wages_account_split"] = B.wage_delta(I["basis"]["hs_or_less"], I["account"], True)
        ch["consumer_prices_side_view"] = consumer_side_view(d, I)
        for name, delta in ch.items():
            q = B.by_bin(delta, d, R)
            exp = expected[(expected.measure == measure) & (expected.channel == name)].set_index("quintile")
            if len(exp) != 6:
                raise SystemExit(f"[BLOCKED] base channel {name}/{measure} not in channel_by_quintile.csv")
            for k in range(6):
                got = dict(bn=q["net"].sum(), loss_bn=q["loss"].sum(), gain_bn=q["gain"].sum()) if k == 0 else \
                    dict(bn=q["net"][k - 1], loss_bn=q["loss"][k - 1], gain_bn=q["gain"][k - 1])
                for col, v in got.items():
                    rows.append(dict(measure=measure, channel=name, quintile=k, column=col,
                                     base=float(exp.loc[k, col]), lane=float(v), diff=float(v - exp.loc[k, col])))
    reg = pd.DataFrame(rows)
    gate(f"regression_{case}_channel_by_quintile", reg["diff"].abs().max() <= 0.01,
         max_abs_diff_bn=float(reg["diff"].abs().max()), cells=len(reg), channels=int(reg.channel.nunique()))
    return reg


SHARED = [  # this frame's channel, the base lane's channel, why their quintile tables differ
    ("fiscal_a", "fiscal_a", "total: the account's own F by band end (mean of 13.56 GDP and 8.95 cash) against the "
     "base's 9.56 (below-BA split), and the future taxpayers' part not allocated; key: federal part by federal "
     "taxes, state-local part by state-local taxes within the group's states, against all taxes nationally"),
    ("fiscal_b", "fiscal_b", "total as fiscal_a; key: per person, the state-local part within the group's states"),
    ("fiscal_a_pooled_national", "fiscal_a", "same key as the base; total only (F and the future taxpayers' part)"),
    ("fiscal_b_pooled_national", "fiscal_b", "same key as the base; total only (F and the future taxpayers' part)"),
    ("wages", "wages", "the account's split (high school or less; the production term P, GDP normalization at "
     "the low-cost end) against the base's below-BA split"),
    ("wages_below_ba_cash", "wages", "the base's own channel (control: must match)"),
    ("renters", "renters", "same central total (metro-local central); raked to ACS extra rent by state as well "
     "as income cell"),
    ("landlords", "landlords", "same central total; CPS rental-income holders raked to the base's income profile "
     "and the rent states, against the base's ACS-INTP/SCF profile without states"),
    ("crime_victims", "crime", "total: decision 4's 30.93 against the base's custody footing 32.34; key: the "
     "group's states"),
    ("crime_victims_custody_footing", "crime", "same total (custody footing); the group's states only"),
    ("crime_victims_national_key", "crime", "same key as the base; total only (30.93 against 32.34)"),
    ("unreimbursed_care", "unreimbursed_care", "same central total; the states of the group's uninsured"),
]


def frame_vs_base(B, d, I, ch):
    """This frame's central channels against the base lane's September 24 channel_by_quintile.csv
    (BASE_COMMIT), SPM quintiles of other residents; quintile 0 is the total."""
    base = pd.read_csv(io.BytesIO(git_show(f"{BASE_REL}/derived/channel_by_quintile.csv", BASE_COMMIT)))
    base = base[base.measure == "spm"]
    rows = []
    for mine, theirs, why in SHARED:
        q = B.by_bin(ch[mine]["central"], d, I["R_spm"])
        exp = base[base.channel == theirs].set_index("quintile").bn
        for k in range(6):
            v = float(q["net"].sum() if k == 0 else q["net"][k - 1])
            rows.append(dict(channel=mine, base_channel=theirs, quintile=k, frame_bn=v, base_bn=float(exp.loc[k]),
                             diff_bn=v - float(exp.loc[k]),
                             frame_share=v / float(q["net"].sum()) if k else 1.0,
                             base_share=float(exp.loc[k] / exp.loc[0]) if k else 1.0, why=why))
    out = pd.DataFrame(rows)
    ctl = out[out.channel == "wages_below_ba_cash"]
    gate("frame_vs_base_control_wages_below_ba", ctl.diff_bn.abs().max() < 1e-6, max_abs_diff_bn=float(ctl.diff_bn.abs().max()))
    return out


# ================================================================== the September 24 person frame
BESIDE = ["renters", "landlords", "crime_victims", "unreimbursed_care", "congestion", "preferences_group_part", "mobility"]


def rake_channel(B, d, R, key, mask, cell_t, state_t: dict, fallback=None, label="", notes=None):
    """Record totals x for other residents matching income-cell (100 SPM percentile cells) and state
    margins, seeded by key among mask; cells or states with a target but no seed use `fallback`."""
    other, pw = d.other.to_numpy(), d.pw.to_numpy()
    idx = np.where(other)[0]
    cell = B.bins(R["p_other"][idx], 100)
    states = sorted(FIPS)
    sidx = pd.Series(range(len(states)), index=states)
    st = sidx.loc[d.st.to_numpy()[idx]].to_numpy()
    st_t = np.array([state_t.get(s, 0.0) for s in states], float)
    ct = np.asarray(cell_t, float)
    gate(f"rake_margins_consistent_{label}", np.isclose(st_t.sum(), ct.sum(), rtol=1e-9), states=st_t.sum(), cells=ct.sum())
    seed = pw[idx] * np.where(mask[idx], key[idx], 0.0)
    for margin, grp, tgt in (("cell", cell, ct), ("state", st, st_t)):
        have = np.bincount(grp, weights=seed, minlength=len(tgt))
        need = (tgt != 0) & (have <= 0)
        if need.any():
            fb = fallback if fallback is not None else np.ones(len(d))
            rows = need[grp]
            seed[rows] = pw[idx][rows] * fb[idx][rows]
            if notes is not None:
                notes.setdefault("rake_fallbacks", []).append(f"{label}: {int(need.sum())} {margin}(s) seeded by the fallback")
    x, it, err = rake(seed, cell, st, ct, st_t)
    ss = np.bincount(st, weights=x, minlength=len(st_t))
    cs = np.bincount(cell, weights=x, minlength=len(ct))
    gate(f"rake_converged_{label}", np.allclose(cs, ct, rtol=1e-8, atol=1.0) and np.allclose(ss, st_t, rtol=1e-8, atol=1.0),
         iterations=it, max_cell_gap=float(np.abs(cs - ct).max()), max_state_gap=float(np.abs(ss - st_t).max()))
    out = np.zeros(len(d))
    out[idx] = x / pw[idx]
    return out


def build_frame(B, d, I, fin, fedsplit, deficit, notes):
    pw, other, tgt = d.pw.to_numpy(), d.other.to_numpy(), d.target.to_numpy()
    st = d.st.to_numpy()
    R = I["R_spm"]
    tax_fed, tax_sl = tax_parts(B, d, R, "after", I["F_total"], I["S_total"])
    tax_all, _ = B.tax_key(d, R, "after", I["F_total"], I["S_total"])
    gate("tax_parts_add_to_base_key", np.allclose(tax_fed + tax_sl, tax_all, rtol=1e-12, atol=0))
    ones = np.ones(len(d))
    ch, totals, meta = {}, {}, {}

    def put(name, arrays, expect):
        ch[name] = arrays
        totals[name] = expect

    # ---- group geography: where the state-local cost, victims' harm and uncompensated care arise
    w_state = pd.Series(pw[tgt]).groupby(st[tgt]).sum()
    w_state = (w_state / w_state.sum()).to_dict()
    w_unins = pd.Series((pw * d.uninsured_py.to_numpy())[tgt]).groupby(st[tgt]).sum()
    w_unins = (w_unins / w_unins.sum()).to_dict()
    meta["group_state_share"] = {FIPS[s]: v for s, v in w_state.items()}

    # ---- fiscal: A + F by band end, split federal / state-local, deficit-financed part apart. A is
    # fiscal_totals("sept24") (one definition with the base lane); F is the account's own.
    case = fin["adopted_2026_09_24"]
    e = case["ends"]
    A1 = case["A_one_definition"]
    cost = {end: -(A1[end] + e[end]["F_bn"]) for end in ("low", "high")}
    for end in ("low", "high"):
        lane = fedsplit[("adopted_2026_09_24", end, "central")]["cost_bn"]
        gate(f"fiscal_cost_matches_debt_lane_{end}", abs(cost[end] - lane) < 1e-3, frame=cost[end], debt_lane=lane,
             diff=cost[end] - lane)
    cost["central"] = (cost["low"] + cost["high"]) / 2
    fed = {end: fedsplit[("adopted_2026_09_24", end, "central")]["federal_bn"] for end in ("low", "high")}
    fed["central"] = (fed["low"] + fed["high"]) / 2
    dsh = deficit["share"]
    fisc = {L: dict(cost=cost[L], federal=fed[L], state_local=cost[L] - fed[L], future=dsh * fed[L],
                    federal_today=(1 - dsh) * fed[L]) for L in LEVELS}
    meta["fiscal"] = fisc
    for conv, kf, ks in (("a", tax_fed, tax_sl), ("b", ones, ones)):
        fedt = {L: -alloc(d, kf, fisc[L]["federal_today"]) for L in LEVELS}
        slt = {L: -alloc_states(d, ks, {s: fisc[L]["state_local"] * w for s, w in w_state.items()}, notes=notes,
                                label=f"fiscal_sl_{conv}") for L in LEVELS}
        put(f"fiscal_federal_today_{conv}", fedt, {L: -fisc[L]["federal_today"] for L in LEVELS})
        put(f"fiscal_state_local_{conv}", slt, {L: -fisc[L]["state_local"] for L in LEVELS})
        put(f"fiscal_{conv}", {L: fedt[L] + slt[L] for L in LEVELS},
            {L: -(fisc[L]["federal_today"] + fisc[L]["state_local"]) for L in LEVELS})
    # Variants without geography: every level's cost pooled nationally, on all taxes (ladder 194's
    # convention (a)) or per person (its convention (b)).
    put("fiscal_a_pooled_national", {L: -alloc(d, tax_all, fisc[L]["federal_today"] + fisc[L]["state_local"]) for L in LEVELS},
        {L: -(fisc[L]["federal_today"] + fisc[L]["state_local"]) for L in LEVELS})
    put("fiscal_b_pooled_national", {L: -alloc(d, ones, fisc[L]["federal_today"] + fisc[L]["state_local"]) for L in LEVELS},
        {L: -(fisc[L]["federal_today"] + fisc[L]["state_local"]) for L in LEVELS})

    # ---- wages: the account's production term P (high school or less, sigma 2, epsilon infinite)
    acc, accg = I["account"], I["account_gdp"]
    ratios = [accg.native_production_gain_bn / acc.native_production_gain_bn,
              accg.other_immigrant_production_gain_bn / acc.other_immigrant_production_gain_bn,
              accg.induced_current_receipts_bn / acc.induced_current_receipts_bn]
    gate("gdp_normalization_is_a_uniform_scale", np.allclose(ratios, ratios[0], rtol=1e-9), ratios=[float(r) for r in ratios])
    nf = {"cash": 1.0, "gdp": float(ratios[0])}
    cash = B.wage_delta(I["basis"]["hs_or_less"], acc, True)
    P_acc = float(acc.native_production_gain_bn + acc.other_immigrant_production_gain_bn)
    gate("account_wages_equal_P_cash", np.isclose((pw * cash).sum() / 1e9, P_acc, rtol=1e-9), cps=(pw * cash).sum() / 1e9, nest=P_acc)
    wages = {end: cash * nf[e[end]["normalization"]] for end in ("low", "high")}
    wages["central"] = (wages["low"] + wages["high"]) / 2
    put("wages", wages, {L: (pw * wages[L]).sum() / 1e9 for L in LEVELS})
    # Gate: inside channels (CPS wages + A + F) equal the adopted cost in every specification.
    worst = 0.0
    for cname, c in fin.items():
        for r in c["specs"].itertuples():
            inside = (pw * cash).sum() / 1e9 * nf[r.normalization] + r.A_bn + r.F_bn
            worst = max(worst, abs(inside + r.cost_bn))
            gate(f"wages_equal_engine_P_{cname}_{r.spec_id}", np.isclose((pw * cash).sum() / 1e9 * nf[r.normalization], r.P_bn, atol=1e-8))
    gate("inside_channels_sum_to_headline_every_specification", worst < 1e-8, max_abs_gap_bn=worst, specifications=128)
    # With A from fiscal_totals the band ends close to its rounding (recorded), not to 1e-9.
    for end in ("low", "high"):
        inside = (pw * ch["fiscal_a"][end]).sum() / 1e9 - fisc[end]["future"] + (pw * wages[end]).sum() / 1e9
        gate(f"inside_channels_equal_band_end_{end}", abs(inside + e[end]["cost_bn"]) < 1e-3, inside=inside,
             headline=-e[end]["cost_bn"], gap=inside + e[end]["cost_bn"])
    # Variants (overlap wages): epsilon 3 on the account's split; the below-BA split (ladder 194).
    for vname, row, rowg in (("wages_eps3", I["eps3_hs"], I["eps3_hs_gdp"]),):
        vc = B.wage_delta(I["basis"]["hs_or_less"], row, True)
        f_gdp = float((rowg.native_production_gain_bn + rowg.other_immigrant_production_gain_bn)
                      / (row.native_production_gain_bn + row.other_immigrant_production_gain_bn))
        vn = {"cash": 1.0, "gdp": f_gdp}
        arr = {end: vc * vn[e[end]["normalization"]] for end in ("low", "high")}
        arr["central"] = (arr["low"] + arr["high"]) / 2
        put(vname, arr, {L: (pw * arr[L]).sum() / 1e9 for L in LEVELS})
        dF = {end: (float(rowg.induced_current_receipts_bn) if e[end]["normalization"] == "gdp" else float(row.induced_current_receipts_bn))
              - e[end]["F_bn"] for end in ("low", "high")}
        dF["central"] = (dF["low"] + dF["high"]) / 2
        meta[f"{vname}_delta_F"] = dF
        for conv, k in (("a", tax_all), ("b", ones)):
            put(f"{vname}_receipts_{conv}", {L: alloc(d, k, dF[L]) for L in LEVELS}, {L: dF[L] for L in LEVELS})
    bb = B.wage_delta(I["basis"]["below_ba"], I["central"], True)
    put("wages_below_ba_cash", {L: bb for L in LEVELS}, {L: (pw * bb).sum() / 1e9 for L in LEVELS})
    meta["wages_P"] = {"cash": P_acc, "gdp": P_acc * nf["gdp"], "gdp_factor": nf["gdp"],
                       "below_ba_cash": float((pw * bb).sum() / 1e9)}

    # ---- housing: renters' extra rent and landlords' receipts, by income cell and state
    notes.setdefault("rake_fallbacks", [])
    renter_key = 1.0 / d.n_other_hh.to_numpy()
    renter_mask = other & d.H_TENURE.eq(2).to_numpy() & d.hh_other_ref.to_numpy()
    landlord_key = np.abs(d.HRNTVAL.to_numpy(float)) / d.n_other_hh.to_numpy()
    owner_mask = other & d.H_TENURE.eq(1).to_numpy() & d.hh_other_ref.to_numpy()
    li = B.per_person(d, B.spread_cells(I["acs"]["intp_cells"], R, d), 1.0)
    ls = B.per_person(d, B.spread_cells(I["scf"], R, d), 1.0)
    cell100 = np.where(other, B.bins(np.nan_to_num(R["p_other"]), 100), 0)
    land_profile = np.bincount(cell100[other], weights=(pw * (li + ls) / 2)[other], minlength=100)
    land_profile /= land_profile.sum()
    hs = housing_inputs(I)
    meta["housing"] = {k: dict(v, pattern=list(v["pattern"])) for k, v in hs.items()}

    def housing_level(h, label):
        g = I["acs_geo"][h["pattern"]]
        acs_total = sum(g["rent_state"].values()) / 1e9
        arm = I["arms"][h["pattern"]]["other_renters_extra_rent_bn"]
        # The base's ACS rebuild of the pattern arm matches the housing lane's total (national uniform
        # to 4e-9 relative, from the base's rounded national share); scale to the level's total exactly.
        gate(f"acs_rent_total_{label}", np.isclose(acs_total, arm, rtol=1e-7), acs=acs_total, lane=arm)
        s = h["renters_bn"] / acs_total
        rent_state = {k: v * s for k, v in g["rent_state"].items()}
        r = -rake_channel(B, d, R, renter_key, renter_mask, to_cells100(g["rent_cells"]) * s, rent_state,
                          fallback=np.ones(len(d)), label=f"renters_{label}", notes=notes)
        tot = h["landlords_bn"] * 1e9
        rs = pd.Series(rent_state)
        ll = rake_channel(B, d, R, landlord_key, other & (landlord_key > 0), land_profile * tot,
                          (rs / rs.sum() * tot).to_dict(), fallback=np.maximum(d.capital.to_numpy(float), 0) + 1e-9,
                          label=f"landlords_{label}", notes=notes)
        return r, ll
    ren, lan, own = {}, {}, {}
    for L in LEVELS:
        ren[L], lan[L] = housing_level(hs[L], L)
    put("renters", ren, {L: -hs[L]["renters_bn"] for L in LEVELS})
    put("landlords", lan, {L: hs[L]["landlords_bn"] for L in LEVELS})
    rn, ln = housing_level(hs["national_uniform_central"], "national_uniform_central")
    put("renters_national_uniform", {L: rn for L in LEVELS},
        {L: -hs["national_uniform_central"]["renters_bn"] for L in LEVELS})
    put("landlords_national_uniform", {L: ln for L in LEVELS},
        {L: hs["national_uniform_central"]["landlords_bn"] for L in LEVELS})
    # Owner-occupiers' value gain, a stock and never added: the metro-local arm by elasticity level.
    for L in LEVELS:
        g = I["acs_geo"][(L, "metro_local")]
        own[L] = rake_channel(B, d, R, renter_key, owner_mask, to_cells100(g["value_cells"]), g["value_state"],
                              fallback=np.ones(len(d)), label=f"owner_value_{L}", notes=notes)
    put("owner_value_stock", own, {L: I["arms"][(L, "metro_local")]["other_owner_value_gain_stock_bn"] for L in LEVELS})

    # ---- crime victims: decision 4's figure (central) and the victim lane's envelope (low, high); the
    # victim lane's two footings as allocated variants. Only figures a lane computed.
    cr = crime_inputs(B)
    meta["crime"] = cr
    crime_tot = {"low": cr["envelope_low"], "central": cr["mixed_equal"], "high": cr["envelope_high"]}
    ks = I["keys_rank"]
    s_share = I["serious_share"]

    def crime_states(total, label):
        out = np.zeros(len(d))
        for cls, share in (("serious", s_share), ("simple", 1 - s_share)):
            out -= alloc_states(d, ks[cls], {s: total * share * w for s, w in w_state.items()}, notes=notes, label=label)
        return out
    put("crime_victims", {L: crime_states(crime_tot[L], f"crime_{L}") for L in LEVELS}, {L: -crime_tot[L] for L in LEVELS})
    for cid, k in (("crime_victims_equal_footing", "equal"), ("crime_victims_custody_footing", "custody")):
        arr = crime_states(cr[k], cid)
        put(cid, {L: arr for L in LEVELS}, {L: -cr[k] for L in LEVELS})
    cn = crime_split(B, d, ks, cr["mixed_equal"], s_share)
    put("crime_victims_national_key", {L: cn for L in LEVELS}, {L: -cr["mixed_equal"] for L in LEVELS})

    # ---- unreimbursed hospital care, by the group's uninsured person-years by state
    priv = d.PRIV.eq(1).to_numpy().astype(float)
    u = I["unreimbursed"]
    put("unreimbursed_care", {L: -alloc_states(d, priv, {s: u[L] * w for s, w in w_unins.items()}, notes=notes,
                                               label=f"unreimbursed_{L}") for L in LEVELS}, {L: -u[L] for L in LEVELS})

    # ---- congestion (B1, lanes fixed), by the urban areas' states, per metropolitan worker
    cg = congestion_inputs()
    meta["congestion"] = cg
    workers = d.WORKYN.eq(1).to_numpy().astype(float)
    put("congestion", {L: -alloc_states(d, d.metro_worker.to_numpy().astype(float),
                                        {POSTAL[s] if isinstance(s, str) else s: cg["total"][L] * v for s, v in cg["state_share"].items()},
                                        fallback=workers, notes=notes, label=f"congestion_{L}") for L in LEVELS},
        {L: -cg["total"][L] for L in LEVELS})

    # ---- race- and ethnicity-based preferences: the part tied to Mexican-origin beneficiaries
    pr = preference_inputs()
    meta["preferences"] = pr
    nhw = other & d.race5.eq("nh_white").to_numpy() & d.native.to_numpy()
    earn, semp = d.earn.to_numpy(), d.semp.to_numpy()
    pkeys = {"admissions": (earn, nhw & (d.A_HGA.to_numpy() >= 43)), "contractor_hiring": (earn, nhw),
             "lost_profits": (semp, nhw), "taxpayer_premium": (tax_all, nhw)}
    pref = {}
    for L in LEVELS:
        f = pr["group_part"][L] / sum(pr["parts"].values())
        pref[L] = sum(-alloc(d, k, pr["parts"][p] * f, m) for p, (k, m) in pkeys.items())
    put("preferences_group_part", pref, {L: -pr["group_part"][L] for L in LEVELS})
    put("preferences_regime", {L: -alloc(d, earn, pr["regime"][L], nhw) for L in LEVELS}, {L: -pr["regime"][L] for L in LEVELS})

    # ---- mobility: local-shock insurance to low-skill US-born men; Borjas's gain to all earnings
    mo = mobility_inputs()
    meta["mobility"] = mo
    lowskill_men = other & d.native.to_numpy() & d.sex.eq("male").to_numpy() & (d.A_HGA.to_numpy() <= 39) & (earn > 0)
    put("mobility", {L: alloc(d, earn, mo["insurance"][L], lowskill_men) + alloc(d, earn, mo["borjas"][L]) for L in LEVELS},
        {L: mo["total"][L] for L in LEVELS})

    # ---- city size and schooling mix (proposed): earnings part by state, receipts by convention
    sc = scale_inputs()
    meta["scale"] = sc
    sstates = sc["state_share"]
    put("scale_private", {L: alloc_states(d, earn, {s: sc["total"][L] * sc["private_share"] * v for s, v in sstates.items()},
                                          notes=notes, label=f"scale_{L}") for L in LEVELS},
        {L: sc["total"][L] * sc["private_share"] for L in LEVELS})
    for conv, k in (("a", tax_all), ("b", ones)):
        put(f"scale_receipts_{conv}", {L: alloc(d, k, sc["total"][L] * sc["receipts_share"]) for L in LEVELS},
            {L: sc["total"][L] * sc["receipts_share"] for L in LEVELS})

    # ---- property crime (victim lane's arrest-share proxy), one share per household, group's states
    pc = property_crime_inputs()
    meta["property_crime"] = pc
    hh_key = 1.0 / d.n_other_hh.to_numpy()
    put("property_crime", {L: -alloc_states(d, hh_key, {s: pc[L] * w for s, w in w_state.items()}, notes=notes,
                                            label=f"property_{L}") for L in LEVELS}, {L: -pc[L] for L in LEVELS})

    # ---- care: who receives the native women's extra hours (display; the taxes are inside fiscal)
    ca = care_hours_inputs()
    meta["care_hours"] = ca
    women = care_women_mask(d)
    meta["care_hours"]["cps_women_m"] = float((pw * women).sum() / 1e6)
    arr = alloc(d, earn, ca["after_tax_earnings_bn"], women)
    put("care_women_after_tax_earnings", {L: arr for L in LEVELS}, {L: ca["after_tax_earnings_bn"] for L in LEVELS})

    # ---- side views, never added
    cx = consumer_side_view(d, I)
    put("consumer_prices", {L: cx for L in LEVELS}, {L: float(I["cex_q"].sum()) for L in LEVELS})
    dbt = debt_inputs(fin)
    meta["debt"] = dbt
    for conv, k in (("a", tax_fed), ("b", ones)):
        put(f"debt_legacy_{conv}", {L: -alloc(d, k, dbt[L]) for L in LEVELS}, {L: -dbt[L] for L in LEVELS})

    # ---- closure: persons sum to each channel's total at every level
    for name, arrays in ch.items():
        for L in LEVELS:
            got = float((pw * arrays[L]).sum() / 1e9)
            gate(f"closure_{name}_{L}", np.isclose(got, totals[name][L], rtol=1e-9, atol=1e-9) and not np.any(arrays[L][~other]),
                 persons=got, total=totals[name][L])
    ctx = dict(tax_fed=tax_fed, tax_sl=tax_sl, q5=R["q5"])
    return ch, totals, meta, ctx


# ================================================================== more channel inputs
def property_crime_inputs():
    """Victim lane's property-crime proxy (arrest shares x NCVS victimisations x unit costs)."""
    p = pd.read_csv(FISCAL / "crime_victim_cost_2026_09_23/derived/property_proxy.csv")
    by = p.groupby("price_set").cost.sum() / 1e9
    gate("property_crime_proxy_reproduced", np.isclose(by["miller2021"], 1.2727, atol=5e-4)
         and np.isclose(by["mccollister2010"], 1.3762, atol=5e-4), **{k: float(v) for k, v in by.items()})
    return {"low": float(by.min()), "central": float(by["miller2021"]), "high": float(by.max())}


def care_hours_inputs():
    """Care lane central (Cortes-Tessada Table 10, metro-weighted shock, CPS-scaled union): the
    native women's extra-hours earnings and the taxes on them."""
    s = pd.read_csv(FISCAL / "care_household_services_2026_09_23/derived/hours_tax_specs.csv")
    r = s[(s.arm == "CT") & (s.coefficient == "t10_female_x_L") & (s.shock == "metro_weighted")
          & (s.scaling == "cps_scaled") & (s.population == "native_nonunion")]
    gate("care_hours_central_row_unique", len(r) == 1, rows=len(r))
    r = r.iloc[0]
    c = care_inputs()
    gate("care_hours_taxes_match_summary", np.isclose(r.tax_bn_account_current, c["hours_taxes"], rtol=1e-9),
         specs=float(r.tax_bn_account_current), summary=c["hours_taxes"])
    return dict(earnings_bn=float(r.earnings_bn), taxes_bn=float(r.tax_bn_account_current),
                after_tax_earnings_bn=float(r.earnings_bn - r.tax_bn_account_current),
                d_hours_week_on_removal=float(r.d_hours_week_on_removal), total=c["total"],
                elder_care_bn=c["elder_care"], private_gain_bn=c["private_gain"],
                consumer_surplus_net_bn=c["consumer_surplus_net"])


DIVISION = {9: 1, 23: 1, 25: 1, 33: 1, 44: 1, 50: 1, 34: 2, 36: 2, 42: 2, 17: 3, 18: 3, 26: 3, 39: 3, 55: 3,
            19: 4, 20: 4, 27: 4, 29: 4, 31: 4, 38: 4, 46: 4, 10: 5, 11: 5, 12: 5, 13: 5, 24: 5, 37: 5, 45: 5,
            51: 5, 54: 5, 1: 6, 21: 6, 28: 6, 47: 6, 5: 7, 22: 7, 40: 7, 48: 7, 4: 8, 8: 8, 16: 8, 30: 8,
            32: 8, 35: 8, 49: 8, 56: 8, 2: 9, 6: 9, 15: 9, 41: 9, 53: 9}


def wquantile(x, w, q):
    o = np.argsort(x, kind="stable")
    cw = np.cumsum(w[o]) / w.sum()
    return x[o][min(int(np.searchsorted(cw, q, side="left")), len(x) - 1)]


def care_women_mask(d):
    """US-born other-resident women in the top quartile of their census division's female hourly-wage
    distribution (all civilian women with earnings and hours), the care lane's Cortes-Tessada group."""
    hours = d.WKSWORK.to_numpy(float) * d.HRSWK.to_numpy(float)
    earn = d.PEARNVAL.to_numpy(float)
    wage = np.divide(earn, hours, out=np.zeros(len(d)), where=hours > 0)
    fem = d.civ.to_numpy() & d.A_SEX.eq(2).to_numpy() & (wage > 0)
    div = d.st.map(DIVISION).to_numpy()
    gate("census_divisions_cover_states", not np.isnan(div.astype(float)).any())
    pw = d.pw.to_numpy()
    top = np.zeros(len(d), bool)
    for k in range(1, 10):
        m = fem & (div == k)
        top |= m & (wage >= wquantile(wage[m], pw[m], 0.75))
    return top & d.other.to_numpy() & d.native.to_numpy()


def ingroup_victims(B):
    """Victims inside the group, which the victim lane excludes: the Hispanic-victim rows' group
    victimisations less the outside (non-group Hispanic) victims, at the lane's unit prices. The rows
    are on the victim lane's equal footing; no lane computed the in-group figure on the custody footing
    or with the mixed-group correction."""
    v = pd.read_csv(B.PATHS["crime_victim"])
    h = v[v.victim == "Hispanic"].copy()
    gate("crime_outside_cost_rows_reproduced", np.allclose(h.outside_victims * h.unit_full, h.cost_full, rtol=1e-6))
    n_in = h.group_victimisations - h.outside_victims
    full = float((n_in * h.unit_full).sum() / 1e9)
    tan = float((n_in * h.unit_tangible).sum() / 1e9)
    return dict(nonfatal_victimisations=float(n_in[h.block == "nonfatal_violence"].sum()),
                homicides=float(n_in[h.block == "homicide"].sum()),
                full_equal_bn=full, tangible_equal_bn=tan,
                murder_full_equal_bn=float((n_in * h.unit_full)[h.block == "homicide"].sum() / 1e9))


# ================================================================== nets, cuts, tree
SOCIAL = ["renters", "landlords", "crime_victims", "property_crime", "unreimbursed_care", "congestion", "mobility"]
PROPOSED = ["preferences_group_part", "scale_private"]


def net_parts(name, conv, sister_ids):
    parts = [f"fiscal_{conv}", "wages"]
    if name in ("social", "with_proposed"):
        parts += SOCIAL
    if name == "with_proposed":
        parts += PROPOSED + [f"scale_receipts_{conv}"] + list(sister_ids)
    return parts


def build_nets(ch, totals, sister_ids):
    """Per-person nets at central values and at the least- and most-costly stacks. Parts that are two
    sides of one estimate move together: fiscal and wages by band end (one specification), renters
    and landlords by level (one rent change), the scale term's earnings and receipts by level. Every
    other channel takes the level whose total is highest (least costly) or lowest (most costly)."""
    nets, ntot, recipe = {}, {}, {}
    for name in ("account", "social", "with_proposed"):
        for conv in CONVENTIONS:
            parts = net_parts(name, conv, sister_ids)
            groups = [([f"fiscal_{conv}", "wages"], ("low", "high")), (["renters", "landlords"], LEVELS),
                      (["scale_private", f"scale_receipts_{conv}"], LEVELS)]
            groups = [(g, levs) for g, levs in groups if all(x in parts for x in g)]
            grouped = {x for g, _ in groups for x in g}
            groups += [([x], LEVELS) for x in parts if x not in grouped]
            for stack in ("central", "least_costly", "most_costly"):
                lev = {}
                for g, levs in groups:
                    if stack == "central":
                        choice = "central"
                    else:
                        sums = {L: sum(totals[x][L] for x in g) for L in levs}
                        choice = (max if stack == "least_costly" else min)(sums, key=sums.get)
                    lev.update({x: choice for x in g})
                arr = sum(ch[x][lev[x]] for x in parts)
                tot = sum(totals[x][lev[x]] for x in parts)
                key = (f"net_{name}_{conv}", stack)
                nets[key], ntot[key], recipe[key] = arr, tot, {x: lev[x] for x in parts}
    return nets, ntot, recipe


MAIN_NETS = [f"net_{n}_{c}" for n in ("account", "social", "with_proposed") for c in CONVENTIONS]
UNITS = {"person": "wages to the earner, taxes and rent shared within the unit",
         "spm_unit_pooled": "every amount pooled within the SPM unit, per capita over its other residents"}


def spm_pooler(d):
    """Ruling 6: pool other residents' amounts within SPM units. Each other resident gets the unit's
    weighted mean over its other residents: the members' sum over their number when their weights are
    equal, and still every total when they are not. Group members stay out, and their items stay in the
    group frame."""
    other, pw = d.other.to_numpy(), d.pw.to_numpy()
    gate("spm_units_nest_in_households", d.groupby("SPM_ID").PH_SEQ.nunique().max() == 1)
    codes, _ = pd.factorize(d.SPM_ID.to_numpy())
    n = int(codes.max()) + 1
    w = np.where(other, pw, 0.0)
    den = np.bincount(codes, weights=w, minlength=n)

    def pool(x):
        mean = np.divide(np.bincount(codes, weights=w * x, minlength=n), den, out=np.zeros(n), where=den > 0)
        return np.where(other, mean[codes], x)
    size = np.bincount(codes, weights=other.astype(float), minlength=n)[codes]
    mixed = np.bincount(codes, weights=(~other & d.target.to_numpy()).astype(float), minlength=n)[codes] > 0
    ws = pd.Series(pw[other]).groupby(codes[other])
    spread = ((ws.max() - ws.min()) / ws.mean()).to_numpy()
    info = dict(other_in_multi_member_units_share=float(w[other & (size > 1)].sum() / w.sum()),
                other_in_mixed_units_m=float(w[other & mixed].sum() / 1e6),
                units_with_unequal_weights_share=float((spread > 1e-9).mean()),
                max_relative_weight_spread=float(spread.max()))
    return pool, info


def pooling_moves(d, nets, pnets):
    """Who moves when the social net is pooled within SPM units, by role, and by whether the unit comes
    out ahead once pooled."""
    other = d.other.to_numpy()
    w = d.pw.to_numpy()[other]
    age, working = d.A_AGE.to_numpy()[other], d.WORKYN.eq(1).to_numpy()[other]
    role = np.select([age < 18, ~working], ["under_18", "adult_not_working"], "adult_working")
    rows = []
    for conv in CONVENTIONS:
        k = (f"net_social_{conv}", "central")
        x, y = nets[k][other], pnets[k][other]
        unit = np.where(y > 0, "unit_ahead", "unit_behind")
        for r in ("under_18", "adult_not_working", "adult_working", "all"):
            for u in ("unit_ahead", "unit_behind", "all"):
                m = (role == r if r != "all" else np.ones(len(w), bool)) & (unit == u if u != "all" else True)
                W = w[m].sum()
                if W == 0:
                    continue
                rows.append(dict(net=k[0], role=r, unit=u, persons_m=W / 1e6,
                                 ahead_person=w[m & (x > 0)].sum() / W, ahead_pooled=w[m & (y > 0)].sum() / W,
                                 up_m=w[m & (x <= 0) & (y > 0)].sum() / 1e6, down_m=w[m & (x > 0) & (y <= 0)].sum() / 1e6,
                                 mean_person_usd=(w * x)[m].sum() / W, mean_pooled_usd=(w * y)[m].sum() / W))
    return pd.DataFrame(rows)


CUT_COLUMNS = ["quintile", "decile", "edu_nativity", "tenure", "age3", "race5", "state3", "top10_states", "sex",
               "worker", "industry5"]


def add_cut_columns(d, R):
    d["quintile"] = np.where(d.other, "Q" + pd.Series(R["q5"] + 1).astype(str), "")
    d["decile"] = np.where(d.other, "D" + pd.Series(R["q10"] + 1).astype(str).str.zfill(2), "")


def tabulate_cuts(d, arrays: dict, totals_by_array: dict, nets: set):
    """Every cut of every array: $bn, persons, households, $ per person and per household, % of
    SPM resources; for nets also the shares of net winners and losers. Gate: groups sum to the frame."""
    other = d.other.to_numpy()
    pw = d.pw.to_numpy()[other]
    hh = d.hh_frac.to_numpy()[other]
    res = (d.resources_pc.to_numpy(float) * d.pw.to_numpy())[other]
    rows, recon = [], []
    for cut in CUT_COLUMNS:
        codes, groups = pd.factorize(d[cut].to_numpy()[other], sort=True)
        n = len(groups)
        persons = np.bincount(codes, weights=pw, minlength=n)
        households = np.bincount(codes, weights=hh, minlength=n)
        resources = np.bincount(codes, weights=res, minlength=n)
        worst = 0.0
        for (name, level), arr in arrays.items():
            x = pw * arr[other]
            bn = np.bincount(codes, weights=x, minlength=n) / 1e9
            tot = totals_by_array[(name, level)]
            worst = max(worst, abs(bn.sum() - tot))
            recon.append(dict(cut=cut, channel=name, level=level, frame_bn=tot, cut_sum_bn=float(bn.sum()),
                              diff_bn=float(bn.sum() - tot)))
            is_net = name in nets
            if is_net:
                win = np.bincount(codes, weights=pw * (arr[other] > 0), minlength=n) / persons
                lose = np.bincount(codes, weights=pw * (arr[other] < 0), minlength=n) / persons
            for g in range(n):
                r = dict(cut=cut, group=groups[g], channel=name, level=level, bn=bn[g], persons_m=persons[g] / 1e6,
                         households_m=households[g] / 1e6, usd_per_person=bn[g] * 1e9 / persons[g],
                         usd_per_household=bn[g] * 1e9 / households[g] if households[g] > 0 else np.nan,
                         pct_of_resources=100 * bn[g] * 1e9 / resources[g] if resources[g] > 0 else np.nan)
                if is_net:
                    r.update(winners_share=win[g], losers_share=lose[g])
                rows.append(r)
        gate(f"cuts_sum_to_frame_{cut}", worst < 1e-6, max_abs_diff_bn=worst, arrays=len(arrays))
    return pd.DataFrame(rows), pd.DataFrame(recon)


TREE_FEATURES = ["decile", "edu_nativity", "tenure", "age3", "race5", "state3", "sex", "worker", "industry5"]


def grow_tree(X: pd.DataFrame, y, w, net, depth=3, min_share=0.02):
    """Weighted greedy classification tree on the winner indicator (Gini), binary splits: one value
    against the rest for categorical cuts, a threshold for deciles. Returns the leaves."""
    wt = w.sum()
    cols = {c: X[c].to_numpy() for c in X.columns}
    dec = np.array([int(s[1:]) if s else 0 for s in cols["decile"]]) if "decile" in cols else None

    def gini(m):
        ww = w[m].sum()
        if ww <= 0:
            return 0.0
        p = (w[m] * y[m]).sum() / ww
        return ww * 2 * p * (1 - p)

    leaves = []

    def split(m, path, level):
        if level == depth:
            return leaves.append((path, m))
        base, best = gini(m), None
        for f, v in cols.items():
            cands = ([(f"decile <= {k}", dec <= k) for k in range(1, 10)] if f == "decile"
                     else [(f"{f} = {g}", v == g) for g in np.unique(v[m])])
            for lab, s in cands:
                l, r = m & s, m & ~s
                if w[l].sum() < min_share * wt or w[r].sum() < min_share * wt:
                    continue
                imp = gini(l) + gini(r)
                if best is None or imp < best[0]:
                    best = (imp, lab, s)
        if best is None or best[0] >= base - 1e-9 * wt:
            return leaves.append((path, m))
        _, lab, s = best
        neg = lab.replace(" = ", " != ").replace("<=", ">")
        split(m & s, path + [lab], level + 1)
        split(m & ~s, path + [neg], level + 1)

    split(np.ones(len(y), bool), [], 0)
    out = []
    for path, m in leaves:
        out.append(dict(path=" & ".join(path) or "all", persons_m=w[m].sum() / 1e6, share_of_persons=w[m].sum() / wt,
                        winners_share=(w[m] * y[m]).sum() / w[m].sum(),
                        mean_net_usd=(w[m] * net[m]).sum() / w[m].sum()))
    return out


PAIRS = [("edu_nativity", "state3"), ("tenure", "decile"), ("tenure", "state3"), ("industry5", "state3"),
         ("age3", "tenure"), ("decile", "state3"), ("worker", "state3"), ("edu_nativity", "tenure")]


def winner_cells(d, nets, min_m=1.0):
    """Two-way cells of the telling cuts: persons, share of net winners, mean net, for each net at
    central values; cells under min_m million persons are dropped."""
    other = d.other.to_numpy()
    w = d.pw.to_numpy()[other]
    out = []
    for a, b in PAIRS:
        ga, gb = d[a].to_numpy()[other], d[b].to_numpy()[other]
        cell = pd.Series(ga).astype(str) + " & " + pd.Series(gb).astype(str)
        codes, groups = pd.factorize(cell, sort=True)
        persons = np.bincount(codes, weights=w)
        for (name, stack), arr in nets.items():
            if stack != "central":
                continue
            x = arr[other]
            win = np.bincount(codes, weights=w * (x > 0)) / persons
            mean = np.bincount(codes, weights=w * x) / persons
            for g in np.where(persons >= min_m * 1e6)[0]:
                out.append(dict(cuts=f"{a} x {b}", cell=groups[g], net=name, persons_m=persons[g] / 1e6,
                                winners_share=win[g], mean_net_usd=mean[g]))
    return pd.DataFrame(out)


def nest_gdp_factor(I):
    acc, accg = I["account"], I["account_gdp"]
    return float((accg.native_production_gain_bn + accg.other_immigrant_production_gain_bn)
                 / (acc.native_production_gain_bn + acc.other_immigrant_production_gain_bn))


# ================================================================== the group itself (step 6)
GENERATIONS = (("G1", "the first generation (born in Mexico)"),
               ("G2", "the second generation (US-born, a parent born in Mexico)"),
               ("G3plus", "the third-plus generation (US-born of US-born parents)"))


def generation_split(fin):
    """The generation lane's split of the adopted main case (committed ba12f3c), both conventions for
    children; gated to add to the band ends. Yields NAS-convention values with convention (a) beside."""
    g = pd.read_csv(PATHS["generations"]).set_index(["convention", "generation", "band_end"])
    ends = fin["adopted_2026_09_24"]["ends"]
    for conv in ("a", "b"):
        for end in ("low", "high"):
            tot = float(sum(g.loc[(conv, gen, end), "cost_bn"] for gen, _ in GENERATIONS))
            gate(f"generation_split_adds_to_band_{conv}_{end}", np.isclose(tot, ends[end]["cost_bn"], atol=1e-3),
                 generations=tot, band=ends[end]["cost_bn"])
    for gen, lab in GENERATIONS:
        b = {end: float(g.loc[("b", gen, end), "cost_bn"]) for end in ("low", "high")}
        b["members"] = float(g.loc[("b", gen, "low"), "population"])
        yield (b, lab, float(g.loc[("a", gen, "low"), "population"]), float(g.loc[("a", gen, "low"), "cost_bn"]),
               float(g.loc[("a", gen, "high"), "cost_bn"]))


def group_frame(B, d, I, fin):
    pw, tgt = d.pw.to_numpy(), d.target.to_numpy()
    N = pw[tgt].sum()
    rows = []

    def add(item, lo, c, hi, basis, note, per=N, kind="the group's gain or loss"):
        rows.append(dict(item=item, kind=kind, bn_low=lo, bn_central=c, bn_high=hi,
                         usd_per_member_central=(c * 1e9 / per) if c is not None and per else np.nan,
                         basis=basis, note=note))
    A1 = fin["adopted_2026_09_24"]["A_one_definition"]
    A = {"low": -A1["low"], "high": -A1["high"]}
    add("direct fiscal transfer received: the direct response A, sign flipped", A["low"],
        (A["low"] + A["high"]) / 2, A["high"],
        "[CALCULATION: distribution_weights_2026_09_23 fiscal_totals('sept24'); engine run in specs.cjs]",
        "low and high are the low- and high-cost band ends; the production gain P goes to other residents and "
        "the induced receipts F to budgets, so neither is a transfer to the group")
    for g, lab, n_a, lo_a, hi_a in generation_split(fin):
        add(f"the account's net cost to other residents attributed to {lab}, minors with their parents (NAS 2017)",
            g["low"], (g["low"] + g["high"]) / 2, g["high"],
            "[CALCULATION: generation_account_2026_09_24/derived/generation_results.csv, git ba12f3c]",
            "the account's own split with no reference group: a cost to other residents, not the group's gain; "
            "never netted against other residents' rows and never the September 19 ledger's gaps; children in "
            f"their own generation: {lo_a:.1f} / {hi_a:.1f}bn at the low / high end ({n_a / 1e6:.2f}m members) "
            "[FRAMING-SENSITIVE]", per=g["members"], kind="the account's split by generation")
    earn = np.maximum(d.PEARNVAL.to_numpy(float), 0)
    fb = tgt & d.PRCITSHP.isin([4, 5]).to_numpy()
    g1 = fb & d.PENATVTY.eq(MEXICO_BIRTHPLACE).to_numpy()
    E1 = float((pw * earn)[g1].sum() / 1e9)
    gain = {L: E1 * (1 - 1 / PLACE_PREMIUM_RE[L]) for L in LEVELS}
    add("first generation (born in Mexico): market gain over the same person's earnings in Mexico", gain["low"],
        gain["central"], gain["high"],
        "[SOURCE: Clemens, Montenegro & Pritchett, HKS RWP09-004 (2009), sec. 3.3 and Table 8] x "
        "[DATA: CPS ASEC 2025 PEARNVAL of Mexico-born members]",
        f"US earnings {E1:.1f}bn x (1 - 1/Re), Re = 2.08 / 2.46 / 2.79 (PPP wage ratio for the same worker); "
        f"{pw[g1].sum() / 1e6:.2f}m members born in Mexico; same employment and hours assumed [INFERENCE]",
        per=pw[g1].sum())
    if pw[fb & ~g1].sum() > 0:
        add("foreign-born members born outside Mexico", None, None, None, "not computed",
            f"{pw[fb & ~g1].sum() / 1e6:.2f}m members; no Mexico counterfactual applies", per=None)
    g23 = tgt & ~fb
    add("second and third-plus generations (US-born)", None, None, None, "no counterfactual in Mexico",
        f"{pw[g23].sum() / 1e6:.2f}m members; they were born here, so no place premium exists and none is invented",
        per=None)
    # Wage competition among the group's own workers: each worker's wage falls by the same percentage
    # as other workers in its nativity branch and skill cell (the account's nest) [INFERENCE].
    hga = d.A_HGA.to_numpy()
    cells = [(hga >= 31) & (hga <= 39), (hga >= 40) & (hga <= 46)]
    native = d.PRCITSHP.isin([1, 2, 3]).to_numpy()
    for lab, row in (("epsilon infinite (account)", I["account"]), ("epsilon 3", I["eps3_hs"])):
        parts = {}
        for tag, br in (("native", native), ("other_fb", ~native)):
            for c in (0, 1):
                m = tgt & br & cells[c]
                w_ = row[f"wage_pct_{tag}_cell{c}"] / 100
                parts[(tag, c)] = float((pw * (-w_) * earn * (1 - B.TAU[c]))[m].sum() / 1e9)
        low_skill = parts[("native", 0)] + parts[("other_fb", 0)]
        high_skill = parts[("native", 1)] + parts[("other_fb", 1)]
        # Low end cash earnings, high end the GDP normalization's uniform scale, central their mean,
        # as the account pairs its two band ends.
        gf = nest_gdp_factor(I)
        add(f"wage competition among the group's own workers, high school or less, after tax ({lab})",
            low_skill, low_skill * (1 + gf) / 2, low_skill * gf,
            "[CALCULATION: account nest wage changes x CPS earnings of members]",
            f"cash: US-born members {parts[('native', 0)]:.2f}bn, foreign-born {parts[('other_fb', 0)]:.2f}bn; "
            f"high end x{gf:.4f} (GDP normalization)")
        add(f"wage gain of the group's own workers, some college or more, after tax ({lab})",
            high_skill, high_skill * (1 + gf) / 2, high_skill * gf,
            "[CALCULATION: account nest wage changes x CPS earnings of members]",
            f"cash: US-born {parts[('native', 1)]:.2f}bn, foreign-born {parts[('other_fb', 1)]:.2f}bn")
    ig = ingroup_victims(B)
    add("victims inside the group (excluded from the victim lane), full cost, equal footing", None,
        -ig["full_equal_bn"], None,
        "[CALCULATION: crime_victim_cost_2026_09_23/derived/cost_by_victim_and_offence_central.csv]",
        f"{ig['homicides']:.0f} homicides and {ig['nonfatal_victimisations']:.0f} non-fatal victimisations a "
        f"year; tangible {-ig['tangible_equal_bn']:.2f}bn. The victim lane's rows are on the equal footing (the "
        "footing of its $28.92bn); no lane computed this figure on the custody footing or with the mixed-group "
        "correction. Police records (NIBRS TX+AZ) put more of the group's victims in-group than NCVS, which "
        "would raise it"),
    rem = banxico_remittances()
    add("remittances received in Mexico from the United States, 2024 (context, not a US resident's gain or loss)",
        None, rem["us_bn"], None, "Banxico CE167, US-origin receipts, revised [SOURCE: Banxico SIE table CE167, "
        "series SE43675/SE43738, read from consumption_key_2026_09_24/_cache/sources/corridor/"
        "banxico_CE167_2022_2025.xlsx as remittance.py primary_flows() reads it]",
        ("all countries {:.2f}bn, the United States {:.2%} of it; ".format(rem["total_bn"], rem["us_share"])
         if rem["total_bn"] else rem["source"] + "; ")
        + "sent from the United States overall, not only by the group. The consumption lane's corridor "
        "(consumption_key_2026_09_24, 6841b39) needs {:.1f} times the surveyed sending amount (CEMLA ${:,.0f} a "
        "year), so it includes flows beyond the CPS households".format(rem["corridor_over_cemla"], rem["cemla_usd"]),
        per=None)
    return pd.DataFrame(rows), ig, dict(g1_members_m=float(pw[g1].sum() / 1e6), g1_earnings_bn=E1,
                                        members_m=float(N / 1e6), remittances=rem)


# ================================================================== registry (step 1)
CF = "2024, with vs without the 40.9m CPS Mexican-origin residents (stationary)"


def registry(T, meta, fin, sister_tbl):
    rows = []

    def row(id_, label, v, who, relation, in_net, source, ladder, status, note=""):
        lo, c, hi = (None, None, None) if v is None else (v["low"], v["central"], v["high"])
        rows.append(dict(id=id_, label=label, bn_low=lo, bn_central=c, bn_high=hi, who=who, relation=relation,
                         in_net=in_net, counterfactual=CF, source_lane=source, ladder=ladder, status=status,
                         date=TODAY, note=note))
    f = meta["fiscal"]
    e = fin["adopted_2026_09_24"]["ends"]
    lv = lambda fn: {L: fn(L) for L in LEVELS}
    band = {"low": -e["low"]["cost_bn"], "high": -e["high"]["cost_bn"]}
    band["central"] = (band["low"] + band["high"]) / 2
    row("main_case", "Adopted main case, other residents' net (fiscal + wages)", band, "fiscal + wages",
        "total", "account", "main_case_2026_09_24 (main_case_bands.csv) via specs.cjs", "219", "adopted",
        "low and high are the band ends $200.875-246.318bn; central is their midpoint")
    st = meta["social_totals"]
    pt = meta["published_totals"]
    published = ("published pairing instead (ruling 5; sept24_propagation_2026_09_24 real_costs_totals.csv section 7): "
                 "equal footing {:.1f}-{:.1f}bn with justice on its raw-coding key, custody footing {:.1f}-{:.1f}bn; "
                 "published range {:.0f}-{:.0f}bn").format(*pt["equal"], *pt["custody"], *pt["range"])
    row("account_plus_social",
        "Allocation base: adopted fiscal band + decision 4 victims (mixed footing), not a published total",
        {"low": band["low"] + st["items_central"], "central": band["central"] + st["items_central"],
         "high": band["high"] + st["items_central"]}, "persons and future taxpayers", "allocation base", "social",
        "this lane", "", "adopted", "what the person nets allocate: social items " + ", ".join(SOCIAL) + " at central "
        f"values, victims' harm at decision 4's {meta['crime']['mixed_equal']:.2f}bn (equal footing) beside a fiscal "
        "band that charges justice by the custody ratio; housing at the metro-local central; low and high are the "
        "fiscal band ends; " + published)
    row("account_plus_social_span",
        "Allocation base, every choice low or every choice high (mixed footing), not a published total",
        {"low": st["least_costly"], "central": band["central"] + st["items_central"], "high": st["most_costly"]},
        "persons and future taxpayers", "allocation base", "social", "this lane", "", "adopted",
        "stacks: fiscal and wages by band end, every other item at its least or most costly level; the published "
        "full span is {:.1f}-{:.1f}bn (real_costs_totals.csv section 7 full_span)".format(*pt["span"]))
    for id_, label, v_, note in (
            ("published_total_equal_footing", "Published total at central values, equal footing (justice on its "
             f"raw-coding key; victims ${pt['equal_victims']:.2f}bn, decision 4)", pt["equal"],
             "fiscal band {:.1f}-{:.1f}bn (band variant justice_raw_coding)".format(*pt["equal_fiscal"])),
            ("published_total_custody_footing", "Published total at central values, custody footing (victims "
             f"${pt['custody_victims']:.2f}bn)", pt["custody"],
             "fiscal band {:.1f}-{:.1f}bn, the adopted band".format(*pt["custody_fiscal"]))):
        row(id_, label, {"low": -v_[0], "central": -(v_[0] + v_[1]) / 2, "high": -v_[1]},
            "persons and future taxpayers", "total (published)", "no",
            "sept24_propagation_2026_09_24 (real_costs_totals.csv section 7)", "", "published",
            note + "; low and high are the fiscal band ends, central their midpoint")
    row("fiscal", "Fiscal: direct response A plus induced receipts F", lv(lambda L: -f[L]["cost"]),
        "a: federal_taxes (today's part) + state_local_taxes within the group's states; b: per_person, "
        "state-local part per person within the group's states", "inside", "account",
        f"A: distribution_weights_2026_09_23 fiscal_totals('sept24') at {BASE_COMMIT}; F: main_case_2026_09_24 "
        "via specs.cjs", "219", "adopted",
        "same band-end specifications as main_case; A differs from the engine run by {:.1e} / {:.1e}bn (rounding "
        "of the rebuilt band)".format(*meta["fiscal_A"]["adopted_2026_09_24"]["diff"].values()))
    row("fiscal_federal_today", "Fiscal, federal part financed by today's taxes", lv(lambda L: -f[L]["federal_today"]),
        "a: federal_taxes; b: per_person", "overlaps:fiscal", "account",
        f"debt_legacy_2026_09_23 federal_split_2024.csv at {DEBT24_COMMIT}", "207", "adopted",
        "part of the fiscal row; the debt lane's split, one definition per correction")
    row("fiscal_state_local", "Fiscal, state and local part", lv(lambda L: -f[L]["state_local"]),
        "a: state_local_taxes@group_states; b: per_person@group_states", "overlaps:fiscal", "account",
        f"fiscal row less the debt lane's federal part ({DEBT24_COMMIT})", "207", "adopted", "part of the fiscal row")
    row("future_taxpayers", "Fiscal, federal part financed by borrowing (FY2024 deficit / outlays)",
        lv(lambda L: -f[L]["future"]), "future federal taxpayers; not allocated to today's persons",
        "overlaps:fiscal", "no", "OMB Historical Tables 2.1 and 3.1 (FY2027 release)", "", "adopted",
        f"share {meta['deficit']['share']:.4f} of the federal part [FRAMING-SENSITIVE]; bounds 0 and 1")
    row("wages", "Wages after tax, long run (account's split: high school or less; sigma 2, epsilon infinite)",
        T["wages"], "account_wage_cells (other residents' earnings by nativity branch and skill cell)", "inside",
        "account", "production_nativity_nest_2026_09_22; wage_distribution_2026_09_23", "176, 191", "adopted",
        "the production term P; GDP normalization at the low-cost end")
    row("wages_eps3", "Wages after tax, epsilon 3 between natives and immigrants", T["wages_eps3"],
        "account_wage_cells", "overlaps:wages", "no", "production_nativity_nest_2026_09_22", "176, 181, 191",
        "proposed", "induced receipts change by {:+.2f}bn (central), financed by the convention".format(
            meta["wages_eps3_delta_F"]["central"]))
    row("wages_below_ba", "Wages after tax, below-BA split (ladder 194's central), cash", T["wages_below_ba_cash"],
        "below_ba_wage_cells", "overlaps:wages", "no", "distribution_weights_2026_09_23", "194", "proposed",
        "not the account's split, so it cannot close to the headline")
    ca = meta["care_hours"]
    c = pd.read_csv(PATHS["care"]).set_index("channel")
    cs = c.loc["consumer surplus on immigrant-intensive services, net of native low-skill wage gain"]
    row("care", "Care and household services (hours taxes, elder care, output)", ca["total"],
        "inside the fiscal row, spread by the financing convention", "overlaps:fiscal", "account",
        "care_household_services_2026_09_23", "198", "adopted",
        f"inside since September 24 (lane_constants -4.15); taxes on native women's extra hours {ca['taxes_bn']:.2f}bn")
    row("care_women_extra_hours", "Native women's after-tax earnings from the extra hours (display)",
        T["care_women_after_tax_earnings"], "US-born other-resident women in the top wage quartile of their "
        "census division (CPS {:.2f}m; lane 14.37m in the ACS)".format(ca["cps_women_m"]), "overlaps:care", "no",
        "care_household_services_2026_09_23", "198", "adopted",
        "their private gain is about zero (envelope: the hours trade off leisure and home production); the taxes "
        "on the hours go to budgets inside the fiscal row")
    row("care_consumer_surplus", "Consumer surplus on immigrant-intensive services, net (side view)",
        {"low": float(cs.low_bn), "central": float(cs.central_bn), "high": float(cs.high_bn)},
        "consumers of household services", "overlaps:wages", "no", "care_household_services_2026_09_23", "198",
        "adopted", "the expenditure side of P; never added")
    row("consumer_prices", "Consumer prices, CEX side view (Cortes 2008 published)", T["consumer_prices"],
        "cex_quintile (money-income quintiles, per person)", "overlaps:wages", "no",
        "consumer_price_benefit_2026_09_18", "194", "adopted", "overlaps the production term; never added")
    hs = meta["housing"]
    lvl_note = (f"levels follow ladder 190's net for other residents: low = {hs['low']['row']}; central = "
                f"{hs['central']['row']}; high = {hs['high']['row']}. Low and high are spread by the form-A arm "
                "with the same elasticity and geography, scaled to their totals (x{:.4f} and x{:.4f}) "
                "[INFERENCE]".format(hs["low"]["pattern_scale"], hs["high"]["pattern_scale"]))
    row("renters", "Renters' extra rent, long run (ladder 190)", T["renters"],
        "renters raked to ACS extra rent by income cell and state", "beside", "social",
        "housing_transfer_2026_09_23", "190", "adopted", lvl_note)
    row("landlords", "Landlords' extra rent receipts less the surplus triangle (ladder 190)", T["landlords"],
        "landlords (CPS rental income) raked to the base's ACS-INTP/SCF income profile and the rent states",
        "beside", "social", "housing_transfer_2026_09_23", "190", "adopted",
        "same levels as renters; landlords assumed local [INFERENCE]")
    row("housing_net", "Housing net to other residents (renters + landlords)",
        lv(lambda L: T["renters"][L] + T["landlords"][L]), "renters and landlords", "overlaps:renters+landlords",
        "no", "housing_transfer_2026_09_23", "190", "adopted",
        "ladder 190: {:.2f}-{:.2f}bn across the two geography arms' centrals (national uniform, metro-local), "
        "span {:.2f} to {:+.2f}bn over the long-run grid".format(
            hs["national_uniform_central"]["net_bn"], hs["central"]["net_bn"], hs["low"]["net_bn"], hs["high"]["net_bn"]))
    nu = hs["national_uniform_central"]
    row("housing_net_national_uniform", "Housing net, national-uniform arm's long-run central (ladder 190's low end)",
        lv(lambda L: T["renters_national_uniform"][L] + T["landlords_national_uniform"][L]),
        "renters_national_uniform and landlords_national_uniform, raked like the central", "overlaps:renters+landlords",
        "no", "housing_transfer_2026_09_23", "190", "adopted",
        f"renters -{nu['renters_bn']:.2f}bn, landlords +{nu['landlords_bn']:.2f}bn; the net_shares rows "
        "'*_housing_national_uniform' swap it for the central")
    row("owner_value_stock", "Owner-occupiers' house-value gain (a one-time stock)", T["owner_value_stock"],
        "owners raked to ACS value by income cell and state", "apart", "no", "housing_transfer_2026_09_23", "190",
        "adopted", "a stock, not an annual flow; never added")
    cr = meta["crime"]
    fo = cr["footing"]
    row("crime_victims", "Crime victims' harm, full cost: decision 4's figure, the victim lane's envelope",
        T["crime_victims"], "ncvs_rank_risk@group_states (persons 12+ by victimisation risk)", "beside", "social",
        "crime_ratio_direction_2026_09_24; crime_victim_cost_2026_09_23", "189, 218", "adopted",
        f"central {cr['mixed_equal']:.2f}bn: {fo['mixed_equal']}; low {cr['envelope_low']:.2f}bn: {fo['envelope_low']}; "
        f"high {cr['envelope_high']:.2f}bn: {fo['envelope_high']}")
    row("crime_victims_equal_footing", "Crime victims' harm, equal footing (victim lane central)",
        T["crime_victims_equal_footing"], "ncvs_rank_risk@group_states", "overlaps:crime_victims", "no",
        "crime_victim_cost_2026_09_23", "189", "adopted", fo["equal"])
    row("crime_victims_custody_footing", "Crime victims' harm, custody footing (victim lane)",
        T["crime_victims_custody_footing"], "ncvs_rank_risk@group_states", "overlaps:crime_victims", "no",
        "crime_victim_cost_2026_09_23", "189", "adopted",
        fo["custody"] + "; the footing of the propagation lane's real-costs totals and of ladder 194's crime channel")
    row("crime_victims_national_key", "Crime victims' harm, decision 4's figure on the national key (no geography)",
        T["crime_victims_national_key"], "ncvs_rank_risk (national)", "overlaps:crime_victims", "no",
        "crime_ratio_direction_2026_09_24", "218", "adopted", fo["mixed_equal"])
    row("crime_victims_nibrs", "Crime victims' harm, NIBRS victim-conditional arm", {L: -cr["nibrs_equal"] for L in LEVELS},
        "not allocated", "overlaps:crime_victims", "no", "offender_ethnicity_nibrs_2026_09_23", "202", "adopted",
        fo["nibrs_equal"])
    row("property_crime", "Property crime, arrest-share proxy", T["property_crime"], "households@group_states",
        "beside", "social", "crime_victim_cost_2026_09_23", "189", "adopted", "proxy; no quality of life priced")
    row("unreimbursed_care", "Unreimbursed hospital care outside budgets", T["unreimbursed_care"],
        "privately_insured@group_uninsured_states", "beside", "social", "uncompensated_care_2026_09_23", "192",
        "adopted")
    row("congestion", "Road congestion, time and fuel (B1, lanes fixed)", T["congestion"],
        "commuters@urban_area_states", "beside", "social", "congestion_2026_09_23", "195", "adopted")
    row("mobility", "Mobility: local-shock insurance and Borjas's gain", T["mobility"],
        "insurance: US-born men with high school or less (earnings); Borjas: all earnings", "beside", "social",
        "labor_mobility_insurance_2026_09_23", "203", "adopted")
    row("preferences", "Race- and ethnicity-based preferences, whole regime, cost to white natives",
        T["preferences_regime"], "nh_white_natives (earnings)", "beside", "no", "affirmative_action_cost_2026_09_24",
        "213", "adopted", "most of it follows other groups' preferences, which the counterfactual keeps")
    row("preferences_group_part", "Preferences, part following Mexican-origin beneficiaries", T["preferences_group_part"],
        "nh_white_natives: earnings (BA+ for admissions), self-employment for lost profits, taxes for the price premium",
        "overlaps:preferences", "with_proposed", "affirmative_action_cost_2026_09_24", "213", "proposed",
        "the part the counterfactual removes")
    sc = meta["scale"]
    row("scale", "City size and schooling mix (Card-Rothstein-Yi, CZ 1990 joint)", sc["total"],
        "earnings@metro_states + receipts by the convention", "beside", "with_proposed",
        "scale_spillovers_2026_09_23", "201", "proposed", "would enter through P and receipts if adopted")
    db = meta["debt"]
    row("debt_legacy", "Interest on past gaps (debt legacy)", T["debt_legacy_a"], "a: federal_taxes; b: per_person",
        "apart", "no", f"debt_legacy_2026_09_23 stocks.csv at {DEBT24_COMMIT} (September 24 case)", "207", "adopted",
        "a different object: interest on the stock built by past annual gaps; never added to the annual account; "
        f"rules range {db['rules_min']:.1f}-{db['rules_max']:.1f}; September 23 case (decision 4's figure) "
        f"{db['sept23']['low']:.1f}-{db['sept23']['high']:.1f}")
    cp = meta["consumption_proposal"]
    row("consumption_key_proposal", "Proposed change to the account's consumption key, −$4.1bn on the fiscal total",
        {"low": -cp["change"][0], "central": -(cp["change"][0] + cp["change"][1]) / 2, "high": -cp["change"][1]},
        "not allocated", "proposed change to the account (not adopted)", "no",
        "consumption_key_2026_09_24 (6841b39), spec both_corridor_net_h2", "", "proposed",
        "signed from other residents' side as every row: the fiscal cost falls by {:.2f}bn at both band ends (main "
        "case {:.1f}-{:.1f}bn); variants {:.1f} to {:.1f}bn, surveyed remittances {:.1f}bn; never in a net or the "
        "adopted total".format(-cp["change"][0], cp["band"][0], cp["band"][1], cp["both_max"], cp["both_min"],
                               cp["survey"]))
    for lane, rid in SISTERS.items():
        s = sister_tbl[sister_tbl.lane == lane]
        if s.empty or (s.status == "pending").all():
            row(rid, f"Sister lane {lane}", None, "", "", "no", lane, "", "pending",
                s.note.iloc[0] if len(s) else "file absent at run time")
            continue
        alloc_ = s[s.status == "allocated"]
        other_cf = int((~s.counterfactual_is_absence.astype(bool)).sum())
        v = {L: float(sum(T[c][L] for c in alloc_.channel_id)) for L in LEVELS} if len(alloc_) else None
        row(rid, f"Sister lane {lane}: {len(s)} rows, {len(alloc_)} allocated", v,
            "; ".join(sorted(set(alloc_.key))) if len(alloc_) else "role table only", "beside",
            "with_proposed" if len(alloc_) else "no", lane, "", "proposed",
            (f"{LANE_LABELS[lane]}; " if len(alloc_) and lane in LANE_LABELS else "")
            + f"allocated rows sum here; {other_cf} rows on other counterfactuals "
            "(sister_other_counterfactuals.csv); every row is in role_table.csv; lane verdict at run time: "
            + str(s.lane_verdict.iloc[0])[:60])
    return pd.DataFrame(rows)


# ================================================================== the page (step 7)
PAGE = [  # channel, label, basis, relation, who gains, who loses
    ("fiscal_a", "fiscal cost, tax-share financing (a)", "measured budgets, modelled response",
     "inside", "", "taxpayers today: federal tax share and state-local taxes in the group's states"),
    ("fiscal_b", "fiscal cost, per-person financing (b)", "measured budgets, modelled response",
     "inside", "", "every other resident equally (state-local part within the group's states)"),
    ("wages", "wages after tax (account's split)", "modelled (CES, sigma 2, epsilon infinite)", "inside",
     "workers with some college or more", "workers with high school or less"),
    ("renters", "rent", "measured rents, modelled elasticity", "beside", "", "renter households"),
    ("landlords", "rent receipts", "measured rents, modelled elasticity", "beside", "landlords", ""),
    ("crime_victims", "crime victims' harm", "measured incidents, modelled prices", "beside", "",
     "persons 12+, by victimisation risk, in the states where the group lives"),
    ("property_crime", "property crime (proxy)", "proxy", "beside", "", "households in the group's states"),
    ("unreimbursed_care", "unreimbursed hospital care", "measured uninsured share, assumed use", "beside", "",
     "privately insured (cost shifting), in the states with the group's uninsured"),
    ("congestion", "road congestion", "measured traffic shares, modelled delay", "beside", "",
     "metropolitan commuters in the congested urban areas' states"),
    ("mobility", "mobility insurance and Borjas's gain", "modelled", "beside",
     "US-born men with high school or less; all workers", ""),
    ("preferences_group_part", "preferences (Mexican-origin beneficiaries' part)", "modelled, weak evidence",
     "beside (proposed)", "", "US-born non-Hispanic whites"),
    ("scale_private", "city size and schooling mix, earnings part", "one regression", "beside (proposed)",
     "workers in the group's metros", "workers in the group's metros"),
]


def page_table(d, ch, meta, gf, sister_tbl):
    pw, other = d.pw.to_numpy(), d.other.to_numpy()
    N_other = pw[other].sum()
    rows = []
    for name, label, basis, rel, who_g, who_l in PAGE:
        x = (pw * ch[name]["central"])[other]
        w = pw[other]
        for side, m, who in (("gain", x > 0, who_g), ("loss", x < 0, who_l)):
            if not m.any():
                continue
            bn = x[m].sum() / 1e9
            rows.append(dict(who=who or "(mixed)", gain_or_loss=side, bn_per_year=bn, persons_m=w[m].sum() / 1e6,
                             usd_per_person=bn * 1e9 / w[m].sum(), usd_per_other_resident=bn * 1e9 / N_other,
                             channel=label, basis=basis, inside_or_beside=rel, frame="other residents"))
    f = meta["fiscal"]["central"]
    rows.append(dict(who="future federal taxpayers (deficit-financed part)", gain_or_loss="loss",
                     bn_per_year=-f["future"], channel="fiscal cost, federal borrowing", basis="measured deficit share",
                     inside_or_beside="inside", frame="future taxpayers, not allocated [FRAMING-SENSITIVE]"))
    for r in gf.itertuples():
        if r.bn_central is None or (isinstance(r.bn_central, float) and np.isnan(r.bn_central)):
            continue
        if r.kind != "the group's gain or loss":      # the account's split by generation is not a gain
            continue
        rows.append(dict(who="the group: " + r.item, gain_or_loss="gain" if r.bn_central > 0 else "loss",
                         bn_per_year=r.bn_central, usd_per_person=r.usd_per_member_central, channel=r.item,
                         basis=r.basis, inside_or_beside="beside (group frame)", frame="the group"))
    for r in sister_tbl.itertuples():
        # Rows on other counterfactuals are listed in sister_other_counterfactuals.csv, not here.
        if getattr(r, "status", "") not in ("allocated", "role_only") or not r.counterfactual_is_absence:
            continue
        v = pd.to_numeric(r.bn_central, errors="coerce")
        sign = {"gain": 1.0, "loss": -1.0}.get(str(r.direction).strip().lower(), np.nan)
        basis = r.basis + (f" [{LANE_LABELS[r.lane]}]" if r.status == "allocated" and r.lane in LANE_LABELS else "")
        rec = dict(who=f"{r.group} ({r.lane})", gain_or_loss=r.direction, bn_per_year=sign * abs(v),
                   channel=r.channel, basis=basis, inside_or_beside=r.relation_to_account,
                   frame=f"sister lane, {r.status}; lane verdict at run time: {r.lane_verdict[:40]}")
        if r.status == "allocated":
            x = (pw * ch[r.channel_id]["central"])[other]
            rec.update(persons_m=pw[other][x != 0].sum() / 1e6, usd_per_person=x.sum() / pw[other][x != 0].sum(),
                       usd_per_other_resident=x.sum() / N_other)
        rows.append(rec)
    return pd.DataFrame(rows)


def person_nets_by_cut(cuts):
    """Wide table: nets by the most telling cuts, central, both conventions."""
    keep = ["decile", "edu_nativity", "tenure", "age3", "race5", "state3", "industry5", "sex"]
    c = cuts[cuts.cut.isin(keep) & cuts.channel.str.startswith("net_") & (cuts.level == "central")]
    out = None
    for (name), g in c.groupby("channel"):
        g = g.set_index(["cut", "group"])
        part = g[["usd_per_person", "winners_share"]].rename(columns={
            "usd_per_person": f"{name}_usd_per_person", "winners_share": f"{name}_winners_share"})
        base = g[["persons_m", "households_m"]]
        out = base.join(part) if out is None else out.join(part)
    return out.reset_index()


def sources_manifest(B, base_sha):
    files = [("base distribute.py at " + BASE_COMMIT, f"{BASE_REL}/distribute.py", base_sha)]
    for k, p in list(PATHS.items()) + [(f"base:{k}", v) for k, v in B.PATHS.items()]:
        p = Path(p)
        if p.is_file() and p.stat().st_size < 3e9:
            files.append((k, str(p.relative_to(ROOT)) if p.is_relative_to(ROOT) else str(p), file_sha(p)))
        elif p.exists():
            files.append((k, str(p.relative_to(ROOT)) if p.is_relative_to(ROOT) else str(p), "directory"))
    for commit in (DEBT_COMMIT, DEBT24_COMMIT):
        for name in ("federal_split_2024_lines.csv", "federal_split_2024.csv", "summary.json", "stocks.csv"):
            files.append((f"debt lane at {commit}", f"{DEBT_REL}/{name}", sha(git_show(f"{DEBT_REL}/{name}", commit))))
    for commit in (SEPT23_COMMIT, BASE_COMMIT):
        for name in ("channel_by_quintile.csv", "inputs.json"):
            files.append((f"base {name} at {commit}", f"{BASE_REL}/derived/{name}",
                          sha(git_show(f"{BASE_REL}/derived/{name}", commit))))
    for extra in ("crime_victim_cost_2026_09_23/derived/property_proxy.csv",
                  "care_household_services_2026_09_23/derived/hours_tax_specs.csv"):
        p = FISCAL / extra
        files.append((extra, str(p.relative_to(ROOT)), file_sha(p)))
    return pd.DataFrame(files, columns=["input", "path", "sha256"])


# ================================================================== main
def main():
    DERIVED.mkdir(exist_ok=True)
    CACHE.mkdir(exist_ok=True)
    print("[base] distribute.py at", BASE_COMMIT)
    B, base_sha = load_base()
    d, top10 = load_frame(B)
    pw, other = d.pw.to_numpy(), d.other.to_numpy()
    print(f"  ✓ CPS frame: {pw[other].sum() / 1e6:.2f}m other residents, {pw[d.target.to_numpy()].sum() / 1e6:.2f}m group")
    I = base_inputs(B, d)
    regs = {}
    for case, commit in (("sept23", SEPT23_COMMIT), ("sept24", BASE_COMMIT)):
        print(f"[regression] {case} inputs against the base's channel_by_quintile.csv at {commit}")
        regs[case] = regression(B, d, I, case)
        print(f"  ✓ max |diff| {regs[case]['diff'].abs().max():.2e}bn over {len(regs[case])} cells")
    print("[fiscal] adopted case by specification, one-definition A, federal split, deficit share")
    fin = fiscal_inputs()
    fiscal_A = fiscal_one_definition(B, fin)
    for case, v in fiscal_A.items():
        print(f"  ✓ {case}: fiscal_totals A minus engine A {v['diff']['low']:+.1e} / {v['diff']['high']:+.1e}bn")
    fedsplit, fs_info = federal_split(fin)
    deficit = deficit_share_fy2024()
    print(f"  ✓ deficit share FY2024 {deficit['share']:.4f}")
    notes = {}
    print("[frame] allocating every channel to persons")
    ch, totals, meta, ctx = build_frame(B, d, I, fin, fedsplit, deficit, notes)
    meta["deficit"] = deficit
    meta["fiscal_A"] = fiscal_A
    meta["consumption_proposal"] = consumption_proposal(fin)
    meta["published_totals"] = published_totals(fin)
    print(f"  ✓ {len(ch)} channels closed at low, central and high")
    fvb = frame_vs_base(B, d, I, ch)
    print("  ✓ frame against the base's September 24 quintiles (derived/quintiles_vs_base_sept24.csv)")
    print("[sisters] ingesting winners_losers_rows.csv where present")
    ctx["naics"] = naics_crosswalk()
    sister_tbl, sister_amounts = ingest_sisters(d, ctx, load_key_map())
    for cid, arrs in sister_amounts.items():
        ch[cid] = arrs
        totals[cid] = {L: float((pw * arrs[L]).sum() / 1e9) for L in LEVELS}
    print(f"  ✓ {len(sister_tbl)} rows; {int((sister_tbl.status == 'allocated').sum())} allocated; "
          f"{int((sister_tbl.status == 'pending').sum())} lanes pending")
    print("[nets] winners and losers")
    nets, ntot, recipe = build_nets(ch, totals, list(sister_amounts))
    for k, arr in nets.items():
        gate(f"closure_{k[0]}_{k[1]}", np.isclose((pw * arr).sum() / 1e9, ntot[k], rtol=1e-9, atol=1e-9))
    for conv in CONVENTIONS:
        acc = ntot[(f"net_account_{conv}", "central")]
        head = -(fin["adopted_2026_09_24"]["ends"]["low"]["cost_bn"] + fin["adopted_2026_09_24"]["ends"]["high"]["cost_bn"]) / 2
        gate(f"account_net_plus_future_equals_headline_{conv}", abs(acc - meta["fiscal"]["central"]["future"] - head) < 1e-3,
             persons=acc, future=meta["fiscal"]["central"]["future"], headline=head,
             gap=acc - meta["fiscal"]["central"]["future"] - head)
    # Sensitivities of the social nets at central values, one part swapped: the fiscal cost pooled
    # nationally; housing at ladder 190's national-uniform central; victims' harm on the custody footing.
    for conv in CONVENTIONS:
        k = (f"net_social_{conv}", "central")
        for tag, rep in (("pooled_national_fiscal", {f"fiscal_{conv}": f"fiscal_{conv}_pooled_national"}),
                         ("housing_national_uniform", {"renters": "renters_national_uniform",
                                                       "landlords": "landlords_national_uniform"}),
                         ("crime_custody_footing", {"crime_victims": "crime_victims_custody_footing"})):
            kk = (f"net_social_{conv}_{tag}", "central")
            nets[kk] = nets[k] + sum(ch[new]["central"] - ch[old]["central"] for old, new in rep.items())
            ntot[kk] = ntot[k] + sum(totals[new]["central"] - totals[old]["central"] for old, new in rep.items())
            recipe[kk] = dict(recipe[k], **{old: f"replaced by {new}" for old, new in rep.items()})
            gate(f"closure_{kk[0]}_{kk[1]}", np.isclose((pw * nets[kk]).sum() / 1e9, ntot[kk], rtol=1e-9, atol=1e-9))
    print("[pooled] person nets pooled within SPM units (ruling 6)")
    pool, meta["pooling"] = spm_pooler(d)
    worst, at = 0.0, ""
    for c, arrs in ch.items():
        for L in LEVELS:
            diff = abs(float((pw * pool(arrs[L]))[other].sum() - (pw * arrs[L])[other].sum())) / 1e9
            worst, at = (diff, f"{c}:{L}") if diff > worst else (worst, at)
    gate("spm_pooling_keeps_every_channel_total", worst < 1e-6, channels=len(ch), levels=len(LEVELS),
         worst_bn=worst, at=at)
    pnets = {k: pool(nets[k]) for k in nets if k[0] in MAIN_NETS}
    for k, arr in pnets.items():
        gate(f"closure_pooled_{k[0]}_{k[1]}", np.isclose((pw * arr).sum() / 1e9, ntot[k], rtol=1e-9, atol=1e-9))
    meta["pooling"]["units"] = UNITS
    print(f"  ✓ {len(ch)} channels keep their totals (worst {worst:.1e}bn); {len(pnets)} pooled nets")
    w = pw[other]
    shares = []
    for unit, arrays_ in (("person", nets), ("spm_unit_pooled", pnets)):
        for (name, stack), arr in arrays_.items():
            x = arr[other]
            shares.append(dict(net=name, stack=stack, unit=unit, total_bn=ntot[(name, stack)],
                               winners_share=w[x > 0].sum() / w.sum(), losers_share=w[x < 0].sum() / w.sum(),
                               winners_m=w[x > 0].sum() / 1e6, losers_m=w[x < 0].sum() / 1e6,
                               winners_gain_bn=(w * x)[x > 0].sum() / 1e9, losers_loss_bn=(w * x)[x < 0].sum() / 1e9,
                               median_usd=wquantile(x, w, 0.5), mean_usd=(w * x).sum() / w.sum(),
                               recipe=json.dumps(recipe[(name, stack)])))
    shares = pd.DataFrame(shares)
    moves = pooling_moves(d, nets, pnets)
    # The ruling's plain mean (members' sum over their number, ignoring unequal person weights) as a check:
    # its shares, and how far it moves the totals the weighted mean keeps.
    plain = spm_pooler(d.assign(pw=1.0))[0]
    meta["pooling"]["plain_mean"] = {
        n: dict(winners_share=float(w[plain(nets[(n, "central")])[other] > 0].sum() / w.sum()),
                total_drift_bn=float((w * (plain(nets[(n, "central")]) - nets[(n, "central")])[other]).sum() / 1e9))
        for n in MAIN_NETS}
    print("[cuts]")
    add_cut_columns(d, I["R_spm"])
    arrays = {(n, L): ch[n][L] for n in ch for L in LEVELS}
    tb = {(n, L): totals[n][L] for n in ch for L in LEVELS}
    arrays.update(nets)
    tb.update(ntot)
    arrays.update({(f"{k[0]}_spm_pooled", k[1]): v for k, v in pnets.items()})
    tb.update({(f"{k[0]}_spm_pooled", k[1]): ntot[k] for k in pnets})
    cuts, recon = tabulate_cuts(d, arrays, tb, {k[0] for k in nets} | {f"{k[0]}_spm_pooled" for k in pnets})
    print(f"  ✓ {len(cuts)} cut rows; every cut sums to the frame")
    print("[tree] cuts that separate winners from losers")
    X = d.loc[other, TREE_FEATURES].reset_index(drop=True)
    tree = []
    for key in (("net_social_a", "central"), ("net_social_b", "central"), ("net_account_a", "central"),
                ("net_account_b", "central")):
        net = nets[key][other]
        for leaf in grow_tree(X, (net > 0).astype(float), w, net):
            tree.append(dict(net=key[0], stack=key[1], **leaf))
    tree = pd.DataFrame(tree)
    cells = winner_cells(d, nets)
    print("[group] the group's own frame")
    gf, ig, ginfo = group_frame(B, d, I, fin)
    meta["group"] = dict(ingroup_victims=ig, **ginfo)
    fut = {L: meta["fiscal"][L]["future"] for L in LEVELS}
    meta["social_totals"] = dict(
        items_central=float(sum(totals[p]["central"] for p in SOCIAL)),
        least_costly=float(ntot[("net_social_a", "least_costly")] - min(fut.values())),
        most_costly=float(ntot[("net_social_a", "most_costly")] - max(fut.values())))
    reg_tbl = registry(totals, meta, fin, sister_tbl)
    page = page_table(d, ch, meta, gf, sister_tbl)
    wide = person_nets_by_cut(cuts)
    fs_rows = [dict(case=k[0], end=k[1], convention=k[2], **v) for k, v in fedsplit.items()]
    fs_rows += [dict(case="adopted_2026_09_24", end=L, convention="central", cost_bn=meta["fiscal"][L]["cost"],
                     federal_bn=meta["fiscal"][L]["federal"], state_local_bn=meta["fiscal"][L]["state_local"],
                     federal_share=meta["fiscal"][L]["federal"] / meta["fiscal"][L]["cost"],
                     deficit_share=deficit["share"], future_taxpayers_bn=meta["fiscal"][L]["future"],
                     federal_today_bn=meta["fiscal"][L]["federal_today"]) for L in ("central",)]
    tmpl = []
    for t, desc, basis in KEY_TEMPLATES:
        pop = np.nan
        if "<" not in t:
            k, m, _ = resolve_key(t, d, ctx)
            pop = float((pw * m).sum() / 1e6)
        tmpl.append(dict(template=t, description=desc, cps_basis=basis, population_m=pop))
    tmpl.append(dict(template="@ST", description=TEMPLATE_NOTE, cps_basis="GESTFIPS", population_m=np.nan))
    print("[write]")
    write_csv(reg_tbl, "channels.csv")
    write_csv(page, "winners_losers_table.csv")
    write_csv(wide, "person_nets_by_cut.csv")
    write_csv(cuts, "cuts.csv")
    write_csv(recon, "cut_reconciliation.csv")
    write_csv(shares, "net_shares.csv")
    write_csv(moves, "pooling_moves.csv")
    write_csv(tree, "winners_tree.csv")
    write_csv(cells, "winner_cells.csv")
    write_csv(gf, "group_frame.csv")
    write_csv(sister_tbl, "role_table.csv")
    write_csv(sister_other_counterfactuals(sister_tbl), "sister_other_counterfactuals.csv")
    write_csv(pd.DataFrame(fs_rows), "fiscal_federal_split.csv")
    for case, r in regs.items():
        write_csv(r, f"regression_{case}.csv")
    write_csv(fvb, "quintiles_vs_base_sept24.csv")
    write_csv(pd.DataFrame(tmpl), "key_templates.csv")
    write_csv(ctx["naics"], "naics_census_industry.csv")
    write_csv(sources_manifest(B, base_sha), "sources_manifest.csv")
    meta["notes"] = notes
    meta["top10_states"] = top10
    meta["federal_split_info"] = fs_info
    (DERIVED / "inputs.json").write_text(json.dumps(meta, indent=1, default=float) + "\n")
    (DERIVED / "gates.json").write_text(json.dumps(GATES, indent=1, default=float) + "\n")
    frame = d.loc[other, ["PH_SEQ", "PPPOS", "SPM_ID", "pw"] + CUT_COLUMNS].reset_index(drop=True)
    cols = {f"{n}|{L}": ch[n][L][other] for n in ch for L in LEVELS}
    cols.update({f"{k[0]}|{k[1]}": v[other] for k, v in nets.items()})
    cols.update({f"{k[0]}_spm_pooled|{k[1]}": v[other] for k, v in pnets.items()})
    frame = pd.concat([frame, pd.DataFrame(cols)], axis=1)
    frame.to_parquet(CACHE / "person_frame.parquet", index=False)
    print(f"  ✓ {sum(g['passed'] for g in GATES.values())} gates passed; person frame {frame.shape} in _cache/")


if __name__ == "__main__":
    main()
