"""Rough re-key of the adopted v4 case (sept29) to Indian-origin residents, at their own ages and at the age structure
of third-plus NH whites, with the Mexican-origin union and third-plus NH whites on the same footing. Not the engine.

Every group runs through the white lane's sept29 library (white_replacement_2026_09_28/rekey_sept29.py, imported
read-only as the Black lane's rekey_sept29.py imports it): the case's lines, responses and capital (both bases:
accrual, the case; cash, its cash set), the rough CPS ASEC 2025 keys, the two receipt lines v4 splits out, the pension
accrual at each group's own ratios, state prices and road miles from each group's own residence and driving, and the
engine's union-only corrections (school reprice, college re-key, lane constants, production gain) for the union alone.
W.setup() runs first, with every one of its gates (the dumps are the adopted $371.4146 / 434.8410bn and cash
$294.7011 / 361.8175bn; the engine's union amounts reproduce them; the frame is audit row 4's).

Groups (cost = what the group's presence costs other residents, $bn a year, 2024; negative = a net benefit):
  mexican_origin_engine          the engine's own amounts (the adopted case)
  mexican_origin_rough           the rough keys on the union (the calibration of the rough method)
  mexican_origin_rough_white_ages the union's per-age rates at third-plus NH white ages (CPS five-year bands, 80+),
                                 on the union's own count; the engine's union-only lines and medical / justice shares
                                 move by the reweighting (see union_white_ages)
  indian_origin                  India-born (PENATVTY 210, PRCITSHP 4-5) or native with an India-born parent, own ages
  indian_origin_white_ages       the same per-age rates at third-plus NH white ages, on its own count
  india_born, india_born_white_ages  the first generation alone
  indian_origin_g2_pooled[_white_ages]  robustness: the 2025 G2 adults' (25-64) income-tax, OASDI and earnings keys
                                 scaled to the ASEC 2022-2026 pooled means (pooled_asec.py; with_pooled_g2)
  india_born_self_employed_adults / india_born_wage_salary_adults / india_born_other  the India-born split by the
                                 longest job's class (LJCW 5-6 / 1-4 / the rest, children and non-workers included)
  indian_origin_self_employed_households / _wage_salary_households  Indian-origin persons in households classed by
                                 the highest-earning India-born adult worker's class
  A1_third_plus_nh_white         the white lane's A1 (third-plus NH white, own ages, scaled to the union's count)
  nh_black_rough                 the Black lane's group (a positive control only)
External keys for the Indian-origin groups (the rough CPS keys are shared by every group):
  medical (Medicare, other public health, VA, TRICARE, Medicaid's non-LTSS part): MEPS 2024 non-Hispanic Asian Indian
    alone (RACEV2X 4, HISPNCAT 9; India-born: BORNUSA 2), set to the group's CPS population share and, at white ages,
    reweighted to the white structure, as the white lane does for its slices (MEPS has no India-born child under 5,
    so the India-born at white ages take all Asian Indians' per-age MEPS rates) [DEGRADED: 317 sampled persons];
  Medicaid LTSS: T-MSIS 2023 NH Asian / Pacific Islander LTSS spending per NH API resident aged 65+ (CPS) x the
    group's 65+ persons [DEGRADED: the API rate stands in for Asian Indians];
  custody and arrests: the group's population share x its ACS 2023 institutionalization per member relative to all
    residents (acs_custody.py) [DEGRADED: no Indian-specific offending data; institutions include long-term care];
    at white ages x the white lane's NCVS age factor (its crime_c) relative to the group's own ages;
  driving: NHTS 2017 NH Asian driver miles per person 5+ by band (nhts_asian.py) [DEGRADED: Asian for Indian];
  accrual: derived/accrual_ratios.csv (accrual_indian.py), immigrants' careers from arrival, payable benefits.
Beside the central: the top tail spread in proportion to CPS income-tax dollars (the library's 'prop' rule), which
matters for a high-income group because the central charges a group only the income tax CPS records.

Sampling error: 160 CPS ASEC replicate weights (asec_csv_repwgt_2025.csv) re-key the Indian-origin groups' own CPS
weights (national totals, MEPS and the external rates held fixed); SE = sqrt(4/160 sum (x_r - x_0)^2).

Gates (exit 1, nothing written): W.setup()'s; the A1 and NH Black rows reproduce the white and Black lanes'
rekey_summary_sept29.csv costs (5e-5); the white-age weights carry the white age structure exactly (1e-12); replicate
weight 0 equals the published weight (0.0051, the rounding of MARSUPWT); the MEPS frame re-read here matches the library's row for row.
Outputs: derived/rekey_summary.csv, derived/rekey_buckets.csv, derived/rekey_replicates.csv, derived/keys.csv,
derived/age_structures.csv, derived/drivers.csv (per-member drivers of the social rows, and the scale-spillover
formula evaluated nationally on the CPS for each group; see drivers()).
Run from the repository root after acs_custody.py, accrual_indian.py and nhts_asian.py (about 6 min):
  OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/indian_full_account_2026_09_29/rekey_indian.py

--case oct05 re-keys the v5 case adopted 2026-10-05 (main_case_2026_10_05) through the library's oct05 rules and writes
the same files to derived/oct05/. The union's rows (engine and rough) carry the 3,039,720 added people at the case
lane's amounts, on 42,752,213; A1 is on 42,752,213 as in the white lane's oct05 run; the Indian-origin groups and the NH
Black group keep their own counts. Two rows are added: mexican_origin_engine_identified and
mexican_origin_rough_identified, the union on the identified 39,712,493 at v5's responses (the library's overlay off).
mexican_origin_rough_white_ages stays on the identified union [ASSUMPTION: the added people's per-age amounts are not
in the case lane's output]; social_rows.py --case oct05 calibrates it on the identified rows. The gates read the white
and Black lanes' rekey_summary_oct05.csv. Run it after those lanes' oct05 runs.
"""
from __future__ import annotations

import csv
import importlib.util
import sys
import zipfile
from pathlib import Path

sys.dont_write_bytecode = True   # read-only imports from other lanes: write nothing beside them

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

LANE = Path(__file__).resolve().parent
FISCAL = LANE.parent
DER = LANE / "derived"
_spec = importlib.util.spec_from_file_location("rekey_sept29_white", FISCAL / "white_replacement_2026_09_28/rekey_sept29.py")
W = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(W)
R = W.R
ENDS, BASES = W.ENDS, W.BASES
INDIA = 210
N_REP = 160

d = R.d
native = d.PRCITSHP.isin([1, 2, 3])
G1 = (d.PRCITSHP.isin([4, 5]) & d.PENATVTY.eq(INDIA)).to_numpy()
G2 = (native & (d.PEFNTVTY.eq(INDIA) | d.PEMNTVTY.eq(INDIA))).to_numpy()
R.MASK["ind"] = G1 | G2
R.MASK["ind1"] = G1
# India-born adults by the class of their longest job (LJCW 5-6 self-employed, 1-4 wage and salary), and households
# classed by their highest-earning India-born adult worker (members: the household's Indian-origin persons).
with zipfile.ZipFile(R.ZIP) as _z:
    _x = pd.read_csv(_z.open("pppub25.csv"), usecols=["LJCW", "SEMP_VAL", "INDUSTRY"])
ADULT = d.A_AGE.ge(18).to_numpy()
SEMP = _x.SEMP_VAL.to_numpy(float)
SE = _x.LJCW.isin([5, 6]).to_numpy()
WAGE = _x.LJCW.isin([1, 2, 3, 4]).to_numpy()
R.MASK["ind1se"] = G1 & ADULT & SE
R.MASK["ind1wage"] = G1 & ADULT & WAGE
R.MASK["ind1oth"] = G1 & ~(ADULT & (SE | WAGE))
_lead = pd.DataFrame({"hh": d.PH_SEQ, "earn": np.where(G1 & ADULT & (SE | WAGE), R.earn, -1.0),
                      "se": SE}).sort_values(["hh", "earn"], ascending=[True, False]).drop_duplicates("hh")
_lead = _lead[_lead.earn >= 0].set_index("hh").se
_hh_se = d.PH_SEQ.map(_lead)
R.MASK["hhse"] = (R.MASK["ind"] & _hh_se.eq(True)).to_numpy()
R.MASK["hhwage"] = (R.MASK["ind"] & _hh_se.eq(False)).to_numpy()
OLD65 = (d.A_AGE.to_numpy() >= 65).astype(float)
API = (d.PEHSPNON.eq(2) & d.PRDTRACE.isin([4, 5])).to_numpy()

# MEPS 2024 re-read with the race detail the library does not load; rows must line up with R.md.
_lay = R.parse_meps_sas_fields(R.MEPS.with_name("h256su.txt"))
_F = ["PERWT24F", "RACEV2X", "HISPNCAT", "BORNUSA"]
with zipfile.ZipFile(R.MEPS) as _z:
    _name = [n for n in _z.namelist() if n.lower().endswith(".dat")][0]
    _rows = [{k: float(t[_lay[k][0]:sum(_lay[k])]) for k in _F} for t in (ln.decode("ascii") for ln in _z.open(_name))]
MD2 = pd.DataFrame(_rows)
_ind_m = (MD2.RACEV2X.eq(4) & MD2.HISPNCAT.eq(9)).to_numpy()
R.MMASK["ind"] = _ind_m
R.MMASK["ind1"] = _ind_m & MD2.BORNUSA.eq(2).to_numpy()
for _g in ("ind1se", "ind1wage", "ind1oth"):
    R.MMASK[_g] = R.MMASK["ind1"]          # MEPS cannot split by class of worker [DEGRADED]
for _g in ("hhse", "hhwage"):
    R.MMASK[_g] = R.MMASK["ind"]
MEX_MEPS = MD2.HISPNCAT.eq(1).to_numpy()

INST = pd.read_csv(DER / "acs_institutional.csv").set_index("group")
REL_INST = {"ind": float(INST.loc["indian_origin", "per_member_over_all"]),
            "ind1": float(INST.loc["india_born", "per_member_over_all"])}
for _g in ("ind1se", "ind1wage", "ind1oth"):
    REL_INST[_g] = REL_INST["ind1"]
for _g in ("hhse", "hhwage"):
    REL_INST[_g] = REL_INST["ind"]
_taf = pd.read_csv(R.TAF)
_taf = _taf[(_taf.year == 2023) & (_taf.category == "LTSS") & (_taf.measure == "expenditures") & (_taf.state == "National")]
API_LTSS = float(_taf.set_index("group").loc["api_nh", "value"] / _taf.total.iloc[0])
NHTS = pd.read_csv(DER / "nhts_vmt_asian.csv", dtype={"band": str})
W.VRATE["nh_asian"] = (NHTS[(NHTS.group == "nh_asian") & (NHTS.band != "all")].assign(band=lambda x: x.band.astype(int))
                       .set_index("band").vmt_per_person)
for g in ("ind", "ind1", "ind1se", "ind1wage", "ind1oth", "hhse", "hhwage"):
    W.RACE_RATES[g] = "nh_asian"
W.GROUP_OF.update({"ind": "indian_origin", "ind1": "india_born", "ind1se": "india_born", "ind1wage": "india_born",
                   "ind1oth": "india_born", "hhse": "indian_origin", "hhwage": "indian_origin"})
LABEL = {"ind": "indian_origin", "ind1": "india_born", "ind1se": "india_born_self_employed_adults",
         "ind1wage": "india_born_wage_salary_adults", "ind1oth": "india_born_other",
         "hhse": "indian_origin_self_employed_households", "hhwage": "indian_origin_wage_salary_households"}
G2POOL = pd.read_csv(DER / "g2_pooled.csv")
G2POOL = G2POOL[G2POOL.asec_year == "pooled_2022_2026"].set_index("key")
G2ADULT = G2 & d.A_AGE.between(25, 64).to_numpy()
POOL_KEY = {"fit": "fit", "sit": "sit", "oasdi": "oasdi", "hi": "earn"}


def with_pooled_g2(sc, shift=0.0):
    """The robustness row: the 2025 G2 adults' (25-64) tax and earnings keys scaled to the 2022-2026 pooled means
    (pooled_asec.py), each ratio moved by `shift` of its across-year SE."""
    sc = {**sc, "share": dict(sc["share"]), "cps_bn": dict(sc["cps_bn"])}
    cw = sc["cps_w"]
    for k, pk in POOL_KEY.items():
        r = float(G2POOL.loc[pk, "ratio_pooled_over_2025"]) + shift * float(G2POOL.loc[pk, "ratio_se"])
        delta = float((cw * R.K[k])[G2ADULT].sum()) * (r - 1)
        sc["share"][k] += delta / R.KTOT[k]
        if k in sc["cps_bn"]:
            sc["cps_bn"][k] += delta / 1e9
    return sc


def mean_crime(cw):
    return float((cw * R.crime_c).sum() / cw.sum())


def keyed_ind(g, cw, total, ages, mwt, cw_own):
    """R.keyed's CPS shares for an Indian-origin scenario, and its external keys (module docstring)."""
    sc = {"name": g, "ages": ages, "population": total, "cps_w": cw,
          "share": {k: float((cw * v).sum() / R.KTOT[k]) for k, v in R.K.items()},
          "cps_bn": {k: float((cw * R.K[k]).sum() / 1e9) for k in ("fit", "sit")}}
    meps = {c: float((mwt * R.md[c]).sum() / R.MTOT[c]) for c in R.MEPS_COLS}
    ph = sc["share"]["pc"] * R.pc_scale
    frac = total / R.CPS_TOTAL
    crime_f = mean_crime(cw) / mean_crime(cw_own)
    custody = arrest = frac * REL_INST[g] * crime_f
    ltss = API_LTSS * float((cw * OLD65).sum()) / float((R.w * OLD65 * API).sum())
    key = {"fire": ph, "prisons": custody, "law_courts": 0.6 * arrest + 0.4 * ph, "police_cbp": ph,
           "police_ice_border": ph, "police_ice_interior": ph, "police_non_border": 0.5 * arrest + 0.5 * ph}
    justice = float(sum(R.cj.loc[c, "national_bn"] * k for c, k in key.items()) / R.cj.national_bn.sum())
    medicaid = R.LTSS_PART * ltss + (1 - R.LTSS_PART) * meps["TOTMCD24"]
    sc["external"] = {"public_order_safety": justice, "health_services": meps["OTHPUB"], "medicare": meps["TOTMCR24"],
                      "veterans_other": meps["TOTVA24"], "military_medical": meps["TOTTRI24"],
                      "medicaid_and_chip_other_medical": medicaid}
    sc["keys"] = {"meps_medicare": meps["TOTMCR24"], "meps_medicaid": meps["TOTMCD24"], "meps_other_public": meps["OTHPUB"],
                  "meps_va": meps["TOTVA24"], "meps_tricare": meps["TOTTRI24"], "ltss": ltss, "custody": custody,
                  "arrests": arrest, "justice": justice, "medicaid_blended": medicaid, "crime_age_factor": crime_f,
                  "relative_institutionalization": REL_INST[g], "pop_share_cps": frac}
    return sc


def ind_scenario(g, ages="own", wt=None):
    """An Indian-origin scenario on person weights wt (default: the frame's), at its own count."""
    wt = R.w if wt is None else wt
    m = R.MASK[g]
    cw_own = wt * m
    total = float(cw_own.sum())
    cw = cw_own if ages == "own" else R.reweight(m, wt, R.cage, R.PI[ages], total)
    mmask = R.MMASK[g]
    fallback = False
    if ages != "own" and (pd.Series(R.mw * mmask).groupby(R.mage).sum().reindex(R.BANDS, fill_value=0.0).to_numpy()[R.PI[ages] > 0] <= 0).any():
        mmask, fallback = R.MMASK["ind"], True   # MEPS has no India-born under 5: all Asian Indians' per-age rates
    mfrac = (total / R.CPS_TOTAL) * float(R.mw.sum())
    mwt = R.mw * mmask * (mfrac / float(R.mw[mmask].sum())) if ages == "own" else R.reweight(mmask, R.mw, R.mage, R.PI[ages], mfrac)
    sc = keyed_ind(g, cw, total, ages, mwt, cw_own)
    sc["keys"]["meps_frame_all_asian_indian"] = float(fallback)
    return sc


def union_white_ages():
    """The rough union at white ages, as a union piece: its CPS weights reweighted to the white structure on its own
    count; the engine's union medical shares moved by the MEPS Mexican-origin (HISPNCAT 1) ratio of shares at white and
    own ages; Medicaid's LTSS part by the 65+ ratio; justice by the NCVS age factor; the engine's union-only lines and
    production gain (priced29's adjust) by the key ratios, as state_white.union_piece does [INFERENCE]."""
    m = R.MASK["mex"]
    total = float(R.w[m].sum())
    cw = R.reweight(m, R.w, R.cage, R.PI["w3"], total)
    full = R.w * m
    sc = R.keyed("mex", cw, total, "w3")
    frac = {k: float((cw * v).sum() / (full * v).sum()) for k, v in R.K.items()}
    mfrac = (total / R.CPS_TOTAL) * float(R.mw.sum())
    m_own = R.mw * MEX_MEPS * (mfrac / float(R.mw[MEX_MEPS].sum()))
    m_w = R.reweight(MEX_MEPS, R.mw, R.mage, R.PI["w3"], mfrac)
    ratio = {c: float((m_w * R.md[c]).sum() / (m_own * R.md[c]).sum()) for c in R.MEPS_COLS}
    old_r = float((cw * OLD65).sum() / (full * OLD65).sum())
    crime_r = mean_crime(cw) / mean_crime(full)
    es = lambda lid: R.eng_share["spending|" + lid]  # noqa: E731
    sc["name"] = "union_piece"
    sc["external"] = {"public_order_safety": es("public_order_safety") * crime_r,
                      "health_services": es("health_services") * ratio["OTHPUB"],
                      "medicare": es("medicare") * ratio["TOTMCR24"], "veterans_other": es("veterans_other") * ratio["TOTVA24"],
                      "military_medical": es("military_medical") * ratio["TOTTRI24"],
                      "medicaid_and_chip_other_medical": es("medicaid_and_chip_other_medical")
                      * (R.LTSS_PART * old_r + (1 - R.LTSS_PART) * ratio["TOTMCD24"])}
    sc["frac"] = frac
    sc["keys"] = {**{f"meps_ratio_{c}": v for c, v in ratio.items()}, "old_ratio": old_r, "crime_age_factor": crime_r}
    return sc


def evaluate(sc, end, basis, top="cps"):
    """Cost and components; a union piece takes the engine's union-only lines and production gain by its key ratios
    (W.priced29's adjustment, applied here for either top-tail rule)."""
    r, rows, bk, terms, acc = W.run29(sc, end, basis, top, union_sc=W.UNION_SC)
    if sc != "eng" and sc["name"] == "union_piece":
        e = W.DUMP[basis][end]
        adj = 0.0
        for ln in e["lines"]:
            if ln["id"] in W.S.ADJ_KEY and ln["side"] == "spending":
                v = ln["amount_bn"] * ln["response"] * sc["frac"][W.S.ADJ_KEY[ln["id"]]]
                b = "schools and colleges" if ln["id"] in ("school_reprice", "college_rekey") else R.PER_HEAD
                bk[b] = bk.get(b, 0.0) + v
                adj += v
        prod = [x for x in e["lines"] if x["side"] == "scalar" and x["id"] == "production_gain_bn"][0]["effect_bn"]
        prod *= sc["frac"]["hi"]
        bk["production gain (subtracted)"] = -prod
        adj -= prod
        r["production_gain"] = prod
        r["cost"] += adj
        r["cost_ex_old_age"] += adj
        r["union_only_lines_and_production"] = adj
    return r, bk, terms


def per_worker(sc, v):
    """Mean of v over the scenario's adults with earnings ('' when it has none)."""
    if sc is None:
        return ""
    wk = sc["cps_w"] * (R.earn > 0) * ADULT
    return f"{float((wk * v).sum() / wk.sum()):.0f}" if wk.sum() > 0 else ""


def replicate_weights():
    with zipfile.ZipFile(R.ZIP) as z:
        pos = pd.read_csv(z.open("pppub25.csv"), usecols=["PH_SEQ", "PPPOS"])
        rep = pd.read_csv(z.open("asec_csv_repwgt_2025.csv"))
    rep = rep.rename(columns={"h_seq": "PH_SEQ"})
    m = pos.merge(rep, on=["PH_SEQ", "PPPOS"], how="left", validate="one_to_one")
    cols = [f"pwwgt{i}" for i in range(N_REP + 1)]
    if m[cols].isna().any().any():
        raise SystemExit("[BLOCKED] CPS persons without replicate weights")
    civ = R.civ.astype(float)
    return m[cols].to_numpy(float) * civ[:, None]


# Scale-spillover constants: scale_spillovers_2026_09_23 (arms.py CRY_PAPER and CRY_M; derived/checks.json cry_joint
# and ces_shares), its central joint spec "CRY joint: scale by education + college gradient net of CES (sigma 2)".
_CHK = __import__("json").loads((FISCAL / "scale_spillovers_2026_09_23/derived/checks.json").read_text())
CRY_SIZE = {"hsless": 0.020, "more": 0.043}
CRY_POOLED = 0.034
CRY_M = (CRY_POOLED - CRY_SIZE["hsless"]) / (CRY_SIZE["more"] - CRY_SIZE["hsless"])
_SH = _CHK["ces_shares"]["sc_cry"]
CES_CORR = (_SH["theta"] - CRY_M) / (2.0 * _SH["s"] * (1 - _SH["s"]))
COMP_NET = _CHK["cry_joint"]["frachighed"] - CES_CORR
SIZE_COND = _CHK["cry_joint"]["lnsize"]


def drivers(scen, res):
    """Per-member drivers of the social rows for each CPS scenario (social_rows.py scales the union's rows by them),
    and the scale-spillover lane's central joint formula evaluated nationally on the CPS (scale and composition
    parts): gain = sum over HS-or-less / some-college-or-more of others' earnings x (1 - exp(dpsi)), dpsi = CRY size
    coefficient x ln(1 - the group's worker share) + (CRY college gradient - CES term) x dSC."""
    with zipfile.ZipFile(R.ZIP) as z:
        x = pd.read_csv(z.open("pppub25.csv"), usecols=["NOCOV_CYR", "A_HGA"])
    unins = x.NOCOV_CYR.eq(3).to_numpy(float) + 0.5 * x.NOCOV_CYR.eq(2).to_numpy(float)
    sc_plus = (x.A_HGA >= 40).to_numpy()
    earn = R.earn
    worker = earn > 0
    age = d.A_AGE.to_numpy()
    actual = {"mexican_origin_rough": R.w * R.MASK["mex"], "mexican_origin_rough_white_ages": R.w * R.MASK["mex"],
              "indian_origin": R.w * R.MASK["ind"], "indian_origin_white_ages": R.w * R.MASK["ind"],
              "india_born": R.w * G1, "india_born_white_ages": R.w * G1}
    out = []
    for lab, sc in scen.items():
        if sc == "eng" or lab == "nh_black_rough":
            continue
        cw = sc["cps_w"]
        n = float(cw.sum())
        oth = R.w - actual.get(lab, cw)
        wg, wo = float((cw * worker).sum()), float((oth * worker).sum())
        s_w = wg / (wg + wo)
        scg, sco = float((cw * worker * sc_plus).sum()), float((oth * worker * sc_plus).sum())
        dsc = sco / wo - (scg + sco) / (wg + wo)
        e_o = {"hsless": float((oth * earn * ~sc_plus).sum()), "more": float((oth * earn * sc_plus).sum())}
        size = {k: CRY_SIZE[k] / CRY_POOLED * SIZE_COND * np.log1p(-s_w) for k in e_o}
        gain = lambda sz, cp: sum(e_o[k] * (1 - np.exp(sz[k] + cp)) for k in e_o) / 1e9  # noqa: E731
        terms = res[("accrual", lab, "low")][2]
        out.append({"group": lab, "population": n,
                    "persons_16plus_pm": float((cw * (age >= 16)).sum()) / n,
                    "pupils_5_17_pm": float((cw * R.K["k12"]).sum()) / n,
                    "consumption_pm": float((cw * R.K["cons"]).sum()) / n,
                    "renter_consumption_pm": float((cw * R.K["rent"]).sum()) / n,
                    "uninsured_py_pm": float((cw * unins).sum()) / n,
                    "under5_share": float((cw * (age < 5)).sum()) / n,
                    "india_born_persons": float((cw * G1).sum()),
                    "miles_share": terms["s_vmt"] if terms else np.nan, "miles_rho": terms["rho"] if terms else np.nan,
                    "miles_pm": (terms["s_vmt"] / n) if terms else np.nan,
                    "crime_age_mean_pm": mean_crime(cw), "old65_pm": float((cw * OLD65).sum()) / n,
                    "worker_share_of_all": s_w, "dSC": dsc, "others_earn_hsless_bn": e_o["hsless"] / 1e9,
                    "others_earn_more_bn": e_o["more"] / 1e9,
                    "scale_gain_national_bn": gain(size, 0.0), "composition_gain_national_bn": gain({k: 0.0 for k in e_o}, COMP_NET * dsc),
                    "joint_gain_national_bn": gain(size, COMP_NET * dsc)})
    return out


def main(case="sept29"):
    W.use_case(case)
    out = DER if case == "sept29" else DER / case
    W.setup()
    print("[this lane: groups and gates]", flush=True)
    rows = {(r["group"], r["entry_rule"], r["scenario"]): r for r in csv.DictReader(open(DER / "accrual_ratios.csv"))}
    for g in ("indian_origin", "india_born"):
        W.ACC[g] = W.acc_entry(rows[(g, "immigrants_at_arrival", "payable")])
    R.PI["w3"] = R.structure(R.MASK["w3"], R.w, R.cage)
    W.gate("MEPS re-read matches the library's frame row for row",
           len(MD2) == len(R.md) and bool(np.allclose(MD2.PERWT24F.to_numpy(), R.md.PERWT24F.to_numpy())))
    with W.on_lineage():     # oct05: A1 on the lineage's count, as in the white lane's oct05 run
        a1 = R.scenario("w3")
    scen = {"mexican_origin_engine": "eng", "mexican_origin_rough": W.UNION_SC,
            "mexican_origin_rough_white_ages": union_white_ages(),
            "indian_origin": ind_scenario("ind"), "indian_origin_white_ages": ind_scenario("ind", "w3"),
            "india_born": ind_scenario("ind1"), "india_born_white_ages": ind_scenario("ind1", "w3"),
            "indian_origin_g2_pooled": with_pooled_g2(ind_scenario("ind")),
            "indian_origin_g2_pooled_white_ages": with_pooled_g2(ind_scenario("ind", "w3")),
            **{LABEL[g]: ind_scenario(g) for g in ("ind1se", "ind1wage", "ind1oth", "hhse", "hhwage")},
            "A1_third_plus_nh_white": a1, "nh_black_rough": R.scenario("blk", scaled=False)}
    for lab, sc in scen.items():
        if lab.endswith("white_ages"):
            got = R.structure(np.ones(len(d), bool), sc["cps_w"], R.cage)
            W.gate(f"{lab}: the weights carry the third-plus white age structure (1e-12)",
                   float(np.abs(got - R.PI["w3"]).max()) < 1e-12)
    res = {}
    for b in BASES:
        for end in ENDS:
            for lab, sc in scen.items():
                r, bk, terms = evaluate(sc, end, b)
                r["cost_top_tail_proportional"] = r["cost"] if sc == "eng" else evaluate(sc, end, b, "prop")[0]["cost"]
                res[(b, lab, end)] = (r, bk, terms)
            if W.LINEAGE_ON:     # oct05: the union on the identified 39,712,493 at v5's responses, beside
                with W.identified():
                    for lab, sc in (("mexican_origin_engine_identified", "eng"), ("mexican_origin_rough_identified", W.UNION_SC)):
                        r, bk, terms = evaluate(sc, end, b)
                        r["cost_top_tail_proportional"] = r["cost"] if sc == "eng" else evaluate(sc, end, b, "prop")[0]["cost"]
                        res[(b, lab, end)] = (r, bk, terms)
                got = res[(b, "mexican_origin_engine_identified", end)][0]["cost"]
                W.gate(f"{b} {end}: the identified engine union is the union dump (1e-9)",
                       abs(got - W.DUMP[b][end]["cost_bn"]) < 1e-9, f"{got:.6f}")
    wl = pd.read_csv(FISCAL / f"white_replacement_2026_09_28/derived/rekey_summary_{case}.csv")
    bl = pd.read_csv(FISCAL / f"black_comparator_rough_2026_09_28/derived/rekey_summary_{case}.csv")
    for b in BASES:
        for end in ENDS:
            for lab, ref in (("A1_third_plus_nh_white", wl), ("nh_black_rough", bl), ("mexican_origin_rough", wl),
                             ("mexican_origin_engine", wl)):
                want = float(ref.query("basis == @b and group == @lab and end == @end").cost.iloc[0])
                got = res[(b, lab, end)][0]["cost"]
                W.gate(f"{b} {end} {lab} reproduces its lane's rekey_summary_{case}.csv (5e-5)", abs(got - want) < 5e-5,
                       f"{got:.4f} vs {want:.4f}")
    for b in BASES:
        for end in ENDS:
            parts = sum(res[(b, LABEL[g], end)][0]["cost"] for g in ("ind1se", "ind1wage", "ind1oth"))
            # not exact: state-price indexes are per-group averages times the group's key share (rule 4)
            W.gate(f"{b} {end}: the three India-born parts add to the India-born cost ($0.05bn)",
                   abs(parts - res[(b, "india_born", end)][0]["cost"]) < 0.05, f"{parts:.4f}")
    pooled_shift = {}
    for b in BASES:
        for end in ENDS:
            up = evaluate(with_pooled_g2(scen["indian_origin"], 1.0), end, b)[0]["cost"]
            dn = evaluate(with_pooled_g2(scen["indian_origin"], -1.0), end, b)[0]["cost"]
            pooled_shift[(b, end)] = abs(up - dn) / 2 * 1e9 / scen["indian_origin"]["population"]
    W.stop_if_failed()

    print("[replicate weights: the Indian-origin groups]", flush=True)
    rw = replicate_weights()
    W.gate("replicate weight 0 is the published weight (0.0051: MARSUPWT is rounded to hundredths)",
           float(np.abs(rw[:, 0] - W.PUBLISHED_W).max()) < 0.0051)
    W.stop_if_failed()
    reps = []
    runs = [(g, a, False) for g in ("ind", "ind1") for a in ("own", "w3")]
    runs += [("ind", a, True) for a in ("own", "w3")]
    runs += [(g, "own", False) for g in ("ind1se", "ind1wage", "ind1oth", "hhse", "hhwage")]
    for g, ages, pooled in runs:
        if True:
            lab = LABEL[g] + ("_g2_pooled" if pooled else "") + ("" if ages == "own" else "_white_ages")
            for i in range(N_REP + 1):
                sc = ind_scenario(g, ages, rw[:, i])
                sc = with_pooled_g2(sc) if pooled else sc
                for b in BASES:
                    for end in ENDS:
                        r = evaluate(sc, end, b)[0]
                        reps.append({"group": lab, "replicate": i, "basis": b, "end": end,
                                     "population": r["population"], "cost_bn": r["cost"],
                                     "cost_per_member": r["cost"] * 1e9 / r["population"]})
            print(f"  {lab}: {N_REP} replicates", flush=True)
    rp = pd.DataFrame(reps)
    se = {}
    for (lab, b, end), x in rp.groupby(["group", "basis", "end"]):
        x = x.sort_values("replicate")
        for col in ("cost_per_member", "cost_bn", "population"):
            v = x[col].to_numpy()
            se[(lab, b, end, col)] = float(np.sqrt(4 / N_REP * ((v[1:] - v[0]) ** 2).sum()))
    samples = {"indian_origin": int((R.MASK["ind"] & R.civ).sum()), "india_born": int((G1 & R.civ).sum()),
               "indian_origin_g2": int((G2 & R.civ).sum()), "indian_origin_g2_pooled": int((R.MASK["ind"] & R.civ).sum()),
               **{LABEL[g]: int((R.MASK[g] & R.civ).sum()) for g in ("ind1se", "ind1wage", "ind1oth", "hhse", "hhwage")}}
    print(f"  CPS sample persons: {samples}; adults 25-64 India-born "
          f"{int((G1 & R.civ & d.A_AGE.between(25, 64).to_numpy()).sum())}, G2 "
          f"{int((G2 & R.civ & d.A_AGE.between(25, 64).to_numpy()).sum())}")

    sc_of = {lab: sc for lab, sc in scen.items() if sc != "eng" and (lab.startswith("indian") or lab.startswith("india"))}
    summary, buckets = [], []
    for (b, lab, end), (r, bk, terms) in res.items():
        base = lab.replace("_white_ages", "")
        n_sample = samples.get(base, "")
        summary.append({"basis": b, "group": lab, "end": end, "spec": W.DUMP[b][end]["spec"],
                        "population": f"{r['population']:.0f}", "cps_sample_persons": n_sample,
                        "cost_bn": f"{r['cost']:.4f}", "cost_per_member": f"{r['cost'] * 1e9 / r['population']:.0f}",
                        "cost_per_member_se": f"{se[(lab, b, end, 'cost_per_member')]:.0f}" if (lab, b, end, "cost_per_member") in se else "",
                        "cost_bn_se": f"{se[(lab, b, end, 'cost_bn')]:.4f}" if (lab, b, end, "cost_bn") in se else "",
                        "cost_per_member_se_pooled_mean": f"{pooled_shift[(b, end)]:.0f}" if lab == "indian_origin_g2_pooled" else "",
                        "earnings_per_adult_worker": per_worker(sc_of.get(lab), R.earn),
                        "semp_per_adult_worker": per_worker(sc_of.get(lab), SEMP),
                        "cost_top_tail_proportional_bn": f"{r['cost_top_tail_proportional']:.4f}",
                        "cost_top_tail_proportional_per_member": f"{r['cost_top_tail_proportional'] * 1e9 / r['population']:.0f}",
                        "taxes_lost_bn": f"{r['taxes_lost']:.4f}", "spending_saved_bn": f"{r['spending_saved']:.4f}",
                        "capital_bn": f"{r['capital']:.4f}", "production_gain_bn": f"{r['production_gain']:.4f}",
                        "old_age_net_bn": f"{r['old_age_net']:.4f}", "cost_ex_old_age_bn": f"{r['cost_ex_old_age']:.4f}",
                        "gap_bn": f"{r['gap']:.4f}" if b == "cash" and not lab.endswith("white_ages") else "",
                        "union_only_lines_and_production_bn": f"{r.get('union_only_lines_and_production', 0.0):.4f}"})
        for k in list(W.BUCKETS) + [R.PER_HEAD, "capital return", "production gain (subtracted)"]:
            v = bk.get(k, 0.0)
            buckets.append({"basis": b, "group": lab, "end": end, "bucket": k, "cost_bn": f"{v:.4f}",
                            "cost_per_member": f"{v * 1e9 / r['population']:.0f}"})
    keys = []
    for lab, sc in scen.items():
        if sc == "eng":
            continue
        for k, v in {**sc.get("keys", {}), **{f"cps_{k}": sc["share"][k] for k in ("pc", "fit", "sit", "oasdi", "ss", "mcare", "k12", "cons", "house")}}.items():
            keys.append({"group": lab, "key": k, "value": f"{v:.6f}"})
    for g in ("indian_origin", "india_born"):
        for k, v in W.ACC[g].items():
            keys.append({"group": g, "key": f"accrual_{k}", "value": f"{v:.6f}"})
    keys.append({"group": "all", "key": "tmsis_ltss_share_api_nh", "value": f"{API_LTSS:.6f}"})
    ages = []
    pis = {"third_plus_nh_white": R.PI["w3"], "union": R.structure(R.MASK["mex"], R.w, R.cage),
           "indian_origin": R.structure(R.MASK["ind"], R.w, R.cage), "india_born": R.structure(G1, R.w, R.cage)}
    if W.LINEAGE_ON:
        pis["lineage"] = W.PI_LINEAGE      # oct05: the union with the added people at the identified G3+'s ages
    for i, bnd in enumerate(R.BANDS):
        ages.append({"band": f"{bnd}+" if bnd == 80 else f"{bnd}-{bnd + 4}", **{k: f"{v[i]:.6f}" for k, v in pis.items()},
                     "indian_origin_sample": int((R.MASK["ind"] & R.civ & (R.cage == bnd)).sum()),
                     "india_born_sample": int((G1 & R.civ & (R.cage == bnd)).sum())})
    drv = drivers(scen, res)
    out.mkdir(exist_ok=True)
    for name, data in (("rekey_summary.csv", summary), ("rekey_buckets.csv", buckets), ("keys.csv", keys),
                       ("age_structures.csv", ages), ("drivers.csv", [{k: (f"{v:.8g}" if isinstance(v, float) else v)
                                                                        for k, v in r.items()} for r in drv])):
        with open(out / name, "w", newline="") as f:
            wr = csv.DictWriter(f, fieldnames=list(data[0]), lineterminator="\n")
            wr.writeheader()
            wr.writerows(data)
    rp.to_csv(out / "rekey_replicates.csv", index=False, lineterminator="\n", float_format="%.6f")
    s = pd.DataFrame(summary)
    print(s[["basis", "group", "end", "population", "cost_bn", "cost_per_member", "cost_per_member_se",
             "cost_top_tail_proportional_per_member", "old_age_net_bn", "capital_bn"]].to_string(index=False))


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--case", default="sept29", choices=list(W.CASES), help="sept29 (default, derived/) or oct05 (derived/oct05/)")
    main(ap.parse_args().case)
