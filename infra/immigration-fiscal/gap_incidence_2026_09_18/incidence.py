#!/usr/bin/env python3
"""Who finances the complete resident account's Mexican-origin balance?

Stage 1  rebuild the complete absolute account per CPS record, reusing
         `ledger_absolute_2026_09_17.absolute_ledger` unmodified, and split every
         dollar into a FEDERAL and a STATE-LOCAL bucket by the government that
         writes the cheque or receives the tax.
Stage 2  build the financing bases of every federal and state-local revenue
         instrument over NATIVE households (SPM units with a native head), by
         income decile x tenure, nationally and for California and Texas.
Stage 3  allocate the account's net cost onto those households under two
         financing conventions and three property-tax pass-through arms.

This is an ACCOUNTING ALLOCATION of a per-resident account. It is not a causal
estimate of what anyone's taxes would be in the absence of the population.

Run from the repository root:

    OPENBLAS_NUM_THREADS=1 uv run --no-project --with numpy --with pandas \
      --with openpyxl python3 \
      infra/immigration-fiscal/gap_incidence_2026_09_18/incidence.py
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
FISCAL = HERE.parent
ROOT = HERE.parents[2]
ABS = FISCAL / "ledger_absolute_2026_09_17"
RESIDUAL = FISCAL / "ledger_residual_agg_2026_09_16"
GENEXT = FISCAL / "gen_ledger_extension_2026_09_16"
INSTITUTIONAL = FISCAL / "institutional_bound_2026_09_17"
PRICES = FISCAL / "consumer_price_benefit_2026_09_18"
OUT = HERE / "derived"

sys.path.insert(0, str(ABS))
import absolute_ledger as AL  # noqa: E402
import extend_ledger as ext  # noqa: E402
import residual_agg as resid  # noqa: E402
from meps_health_transport_2024 import donor_model, read_meps  # noqa: E402

TARGETS = AL.TARGETS
UNION = AL.UNION
WHITE = AL.WHITE
ALL_NATIVE = AL.ALL_NATIVE
GEOGRAPHIES = {"US": None, "CA": 6, "TX": 48}

COG_LINES = {
    "federal_igr": 4, "own_source": 7, "taxes": 8, "property": 9,
    "general_sales": 11, "selective_sales": 12, "individual_income": 18,
    "corporate_income": 19, "motor_vehicle_license": 20, "other_taxes": 21,
    "charges_and_misc": 22, "direct_general_expenditure": 66,
}
MEPS_PAYERS = ["TOTMCR24", "TOTMCD24", "TOTVA24", "TOTTRI24", "TOTOFD24", "TOTSTL24"]
PAYER_FEDERAL = {"TOTMCR24": 1.0, "TOTVA24": 1.0, "TOTTRI24": 1.0,
                 "TOTOFD24": 1.0, "TOTSTL24": 0.0}

# ---------------------------------------------------------------- CoG revenue
def read_cog_revenue(path: Path) -> pd.DataFrame:
    import openpyxl
    ws = openpyxl.load_workbook(path, read_only=True, data_only=True)["2022_US_WY"]
    rows = [[("" if c is None else c) for c in r] for r in ws.iter_rows(values_only=True)]
    header = rows[8]
    blocks = [(str(n).strip(), col) for col, n in enumerate(header)
              if isinstance(n, str) and str(n).strip() and col >= 2]
    by_line = {int(r[0]): r for r in rows if isinstance(r[0], (int, float)) and r[0]}
    missing = [k for k, ln in COG_LINES.items() if ln not in by_line]
    if missing:
        raise SystemExit(f"[BLOCKED] Census of Governments lines not found: {missing}")
    out = []
    for name, col in blocks:
        def amount(key: str) -> float:
            v = by_line[COG_LINES[key]][col]
            return 1000.0 * float(v) if isinstance(v, (int, float)) else 0.0
        rec = {k: amount(k) for k in COG_LINES}
        rec["name"] = name
        rec["fips"] = 0 if name == "United States Total" else AL.STATE_NAME_TO_FIPS.get(name)
        if rec["fips"] is None:
            continue
        out.append(rec)
    df = pd.DataFrame(out).set_index("fips").sort_index()
    if len(df) != 52:
        raise SystemExit(f"[BLOCKED] expected 52 CoG blocks (US + 51), parsed {len(df)}")
    resid_own = df.own_source - df.taxes - df.charges_and_misc
    if (resid_own.abs() > 0.005 * df.own_source.abs().clip(lower=1)).any():
        raise SystemExit("[BLOCKED] CoG own-source revenue is not taxes plus charges")
    parts = (df.property + df.general_sales + df.selective_sales + df.individual_income
             + df.corporate_income + df.motor_vehicle_license + df.other_taxes)
    if ((parts - df.taxes).abs() > 0.005 * df.taxes.abs().clip(lower=1)).any():
        raise SystemExit("[BLOCKED] CoG tax components do not sum to total taxes")
    return df


# ------------------------------------------------------------- CEX consumption
def cex_consumption_curve():
    q = pd.read_csv(PRICES / "derived/cex_quintile_parents.csv")
    cols = ["q1_lowest", "q2_second", "q3_third", "q4_fourth", "q5_highest"]
    row = q[q.item.astype(str).str.strip().str.lower() == "income before taxes"]
    if len(row) < 1:
        raise SystemExit("[BLOCKED] CEX 'Income before taxes' line not found")
    # The line appears once in the demographic block (row 10) and again in the
    # income block; the demographic one is the quintile definition.
    row = row.sort_values("row").head(1)
    income = row[cols].to_numpy(dtype=float)[0]
    audit = json.loads((PRICES / "derived/cex_audit.json").read_text())
    expend = np.array([audit["major_component_gate"][c]["published_total"] for c in cols],
                      dtype=float)
    if not (np.diff(income) > 0).all() or not (np.diff(expend) > 0).all():
        raise SystemExit("[BLOCKED] CEX quintile income or expenditure is not increasing")
    return income, expend


def consumption_of(income, x, y):
    inc = np.clip(np.asarray(income, dtype=float), 1.0, None)
    li, lx, ly = np.log(inc), np.log(x), np.log(y)
    out = np.interp(li, lx, ly)
    slope_lo = (ly[1] - ly[0]) / (lx[1] - lx[0])
    slope_hi = (ly[-1] - ly[-2]) / (lx[-1] - lx[-2])
    lo, hi = li < lx[0], li > lx[-1]
    out[lo] = ly[0] + slope_lo * (li[lo] - lx[0])
    out[hi] = ly[-1] + slope_hi * (li[hi] - lx[-1])
    return np.exp(out)


# ------------------------------------------------------------------- stage 1
def build_account(args):
    params = AL.Params(Path(args.params), False)
    for name in AL.EXTRA_PERSON:
        if name not in ext.base.PERSON:
            ext.base.PERSON.append(name)
    for name in ["INT_VAL", "DIV_VAL", "RNT_VAL"]:
        if name not in ext.base.PERSON:
            ext.base.PERSON.append(name)

    cps = GENEXT / "_cache/asecpub25csv.zip"
    medical_zip = ROOT / "sources/immigration-fiscal/data/external/stage3/ahrq/meps_2024/h256dat.zip"
    medical_sas = medical_zip.with_name("h256su.txt")
    print("[stage] CPS state", flush=True)
    state = ext.build(argparse.Namespace(cps_zip=cps))
    d = state["d"]
    index, n_units = state["index"], state["n_units"]
    weights = state["person_weights"]
    w0 = weights[:, 0]
    civilian = (d.PRPERTYP.eq(2) | d.A_AGE.lt(15)).to_numpy()
    groups = {n: state["group"][n] & civilian for n in TARGETS + [WHITE, ALL_NATIVE]}
    groups[UNION] = np.logical_or.reduce([groups[g] for g in TARGETS])
    heads = d.loc[d.SPM_HEAD.eq(1)].sort_values("SPM_ID")
    totals = state["totals"]

    def share(x):
        return ext.allocate(np.asarray(x, dtype=float), index, np.ones(len(d), bool), n_units)

    def unit_total(person_amounts):
        return np.bincount(index, weights=np.asarray(person_amounts, dtype=float),
                           minlength=n_units)

    def unit_share(person_amounts):
        return share(unit_total(person_amounts))

    print("[stage] MEPS donor transport", flush=True)
    medical, anchors = read_meps(medical_zip, medical_sas)
    cells, codes, covariance = donor_model(medical, d, False)
    means = cells.mean_public_paid.to_numpy()
    exposure = ~(d.PUB.eq(0) & d.PRIV.eq(0)).to_numpy()
    valid = medical.PERWT24F.gt(0) & medical.AGE24X.ge(0) & medical.BORNUSA.isin([1, 2])
    sample = medical.loc[valid]
    pop = sample.groupby(["age_band", "born"]).PERWT24F.sum()
    idx = pd.MultiIndex.from_frame(cells[["age_band", "born"]])
    payer_cell = {}
    for col in MEPS_PAYERS:
        wx = sample.assign(wx=sample[col] * sample.PERWT24F).groupby(["age_band", "born"]).wx.sum()
        s = (wx / pop).reindex(idx)
        if s.isna().any():
            raise SystemExit(f"[BLOCKED] missing donor cell for {col}")
        payer_cell[col] = s.to_numpy()
    if not np.allclose(sum(payer_cell[c] for c in MEPS_PAYERS), means, rtol=1e-10, atol=1e-6):
        raise SystemExit("[BLOCKED] per-payer donor means do not sum to mean_public_paid")

    print("[stage] cached aggregates", flush=True)
    pop_state = resid.read_state_population()
    gs_pc, gs_national = resid.read_general_services_per_capita(pop_state)
    cap_pc, cap_national, cap_components = AL.read_cog_capital(
        RESIDUAL / "_cache/22slsstab1.xlsx", pop_state)
    assf = AL.read_assf_k12(GENEXT / "census_assf_fy2024_summary_tables.xlsx")
    omb = AL.read_omb_functions(RESIDUAL / "_cache/omb_hist03z1_fy2027.xlsx")
    us_resident = params.pick("population", ["2024"], "count")

    base_unit = [totals[k] for k in ["modeled_tax_total", "selected_cash_total",
                                     "selected_noncash_total", "employer_payroll",
                                     "sales_tax_share35", "property_tax_owner"]]
    base_unit += [ext.PUPIL_RATIO_NATIVE_ACS * totals["k12_cost_at_full_attendance"],
                  totals["school_lunch"]]
    base_matrix = np.column_stack([share(x) for x in base_unit])

    ctx = dict(d=d, index=index, n_units=n_units, civilian=civilian, weights=weights,
               heads=heads, general_services=(gs_pc, gs_national), assf=assf, omb=omb,
               donor_codes=codes,
               donor_payer_means={"medicaid": payer_cell["TOTMCD24"],
                                  "medicare": payer_cell["TOTMCR24"]},
               exposure=exposure, n_civilian=float(w0[civilian].sum()),
               us_resident=us_resident, consumption_proxy=base_matrix[:, 4],
               capital=(cap_pc, cap_national, cap_components), off=[],
               is_white_ref=groups[WHITE],
               is_target=sum(groups[g].astype(int) for g in TARGETS) > 0)

    print("[stage] item charges", flush=True)
    charges, dropped, centrals, national, _ = AL.build_charges(ctx, params)
    if dropped:
        print(f"[items] dropped: {[x['item'] for x in dropped]}", flush=True)

    fed, stl = {}, {}
    fed["base_federal_income_tax"] = +unit_share(d.FEDTAX_AC.to_numpy(dtype=float))
    fed["base_employee_payroll_tax"] = +unit_share(d.FICA.to_numpy(dtype=float))
    fed["base_employer_payroll_tax"] = +share(totals["employer_payroll"])
    stl["base_state_income_tax"] = +unit_share(d.STATETAX_A.to_numpy(dtype=float))
    stl["base_state_local_sales_tax"] = +share(totals["sales_tax_share35"])
    stl["base_owner_property_tax"] = +share(totals["property_tax_owner"])
    if not np.allclose(fed["base_federal_income_tax"] + fed["base_employee_payroll_tax"]
                       + stl["base_state_income_tax"], base_matrix[:, 0],
                       atol=1e-6, rtol=1e-10):
        raise SystemExit("[BLOCKED] the three tax fields do not rebuild the tax column")

    cash_rebuilt = np.zeros(len(d))
    for label, field, fshare in [("social_security", "SS_VAL", 1.0),
                                 ("ssi", "SSI_VAL", 1.0),
                                 ("veterans", "VET_VAL", 1.0),
                                 ("tanf_general_assistance", "PAW_VAL", args.tanf_federal_share),
                                 ("unemployment", "UC_VAL", 0.0)]:
        v = -unit_share(d[field].to_numpy(dtype=float))
        cash_rebuilt = cash_rebuilt + v
        if fshare:
            fed[f"base_cash_{label}"] = fshare * v
        if 1.0 - fshare:
            stl[f"base_cash_{label}"] = (1.0 - fshare) * v
    if not np.allclose(-cash_rebuilt, base_matrix[:, 1], atol=1e-6, rtol=1e-10):
        raise SystemExit("[BLOCKED] cash sub-components do not rebuild the cash column")

    fed["base_noncash_federal_programs"] = -base_matrix[:, 2]
    fed["base_school_lunch_addback"] = +base_matrix[:, 7]

    per_pupil_us = params.pick("k12", ["per_pupil_current_spending_us"], "money",
                               preferred="f33_per_pupil_current_spending_us")
    membership_us = params.pick("k12", ["fall_membership_us"], "count",
                                preferred="f33_fall_membership_us")
    subf501 = params.pick("omb", ["subf_501"], "money")
    if not (per_pupil_us and membership_us and subf501):
        raise SystemExit("[BLOCKED] cannot derive the federal share of K-12 current spending")
    k12_current_us = per_pupil_us * membership_us
    k12_federal_share = subf501 / k12_current_us
    fed["base_k12_federal_aid"] = -k12_federal_share * base_matrix[:, 6]
    stl["base_k12_state_local"] = -(1.0 - k12_federal_share) * base_matrix[:, 6]

    mcd_fed = params.pick("meps_coverage", ["medicaid_federal"], "money",
                          preferred="nhea_2023_medicaid_federal")
    mcd_stl = params.pick("meps_coverage", ["medicaid_state_local"], "money",
                          preferred="nhea_2023_medicaid_state_local")
    if not (mcd_fed and mcd_stl):
        raise SystemExit("[BLOCKED] NHEA Medicaid federal/state split not verified")
    medicaid_federal_share = mcd_fed / (mcd_fed + mcd_stl)
    payer_person = {c: -payer_cell[c][codes] * exposure for c in MEPS_PAYERS}
    if not np.allclose(sum(payer_person.values()), -means[codes] * exposure,
                       atol=1e-6, rtol=1e-10):
        raise SystemExit("[BLOCKED] per-payer medical does not rebuild the medical column")
    for c in MEPS_PAYERS:
        f = medicaid_federal_share if c == "TOTMCD24" else PAYER_FEDERAL[c]
        if f:
            fed[f"base_medical_{c}"] = f * payer_person[c]
        if 1.0 - f:
            stl[f"base_medical_{c}"] = (1.0 - f) * payer_person[c]

    def vec(item):
        return charges.data[charges.columns.index(f"{item}|{centrals[item]}")]

    for item in ["G", "K", "P", "D", "S"]:
        if centrals.get(item):
            stl[f"item_{item}"] = vec(item)
    for item in ["I", "E", "R"]:
        if centrals.get(item):
            fed[f"item_{item}"] = vec(item)
    f_key = f"F|{args.f_arm}"
    if f_key not in charges.columns:
        raise SystemExit(f"[BLOCKED] item F arm {args.f_arm} was not built")
    fed["item_F"] = charges.data[charges.columns.index(f_key)]

    u_ratios = {
        "snap": (params.admin_over_survey("underreporting", [["snap"]], "snap",
                                          preferred="ratio_snap"),
                 heads.SPM_SNAPSUB.to_numpy(dtype=float), "unit", 1.0),
        "tanf": (params.admin_over_survey("underreporting", [["tanf"]], "tanf",
                                          preferred="ratio_tanf"),
                 d.PAW_VAL.to_numpy(dtype=float), "person", args.tanf_federal_share),
        "ssi": (params.admin_over_survey("underreporting", [["ssi"]], "ssi",
                                         preferred="ratio_ssi"),
                d.SSI_VAL.to_numpy(dtype=float), "person", 1.0),
        "ui": (params.admin_over_survey("underreporting", [["unemployment"]], "ui",
                                        preferred="ratio_ui"),
               d.UC_VAL.to_numpy(dtype=float), "person", 0.0),
    }
    u_rebuilt = np.zeros(len(d))
    for name, (ratio, basis, level, fshare) in u_ratios.items():
        if ratio is None:
            raise SystemExit(f"[BLOCKED] item U ratio missing for {name}")
        tot = basis.copy() if level == "unit" else unit_total(basis)
        spread = -share(tot * (ratio - 1.0)) * civilian
        u_rebuilt = u_rebuilt + spread
        if fshare:
            fed[f"item_U_{name}"] = fshare * spread
        if 1.0 - fshare:
            stl[f"item_U_{name}"] = (1.0 - fshare) * spread
    if not np.allclose(u_rebuilt, vec("U"), atol=1e-6, rtol=1e-10):
        raise SystemExit("[BLOCKED] item U rebuild does not reproduce the published vector")

    r_mcd = params.nhea_over_meps("meps_coverage", [["ratio", "medicaid"]], "medicaid",
                                  preferred="nhea_to_meps_ratio_medicaid")
    r_mcr = params.nhea_over_meps("meps_coverage", [["ratio", "medicare"]], "medicare",
                                  preferred="nhea_to_meps_ratio_medicare")
    m_mcd = -(payer_cell["TOTMCD24"][codes] * (r_mcd - 1.0)) * exposure * civilian
    m_mcr = -(payer_cell["TOTMCR24"][codes] * (r_mcr - 1.0)) * exposure * civilian
    if not np.allclose(m_mcd + m_mcr, vec("M"), atol=1e-6, rtol=1e-10):
        raise SystemExit("[BLOCKED] item M rebuild does not reproduce the published vector")
    fed["item_M_medicare"] = m_mcr
    fed["item_M_medicaid"] = medicaid_federal_share * m_mcd
    stl["item_M_medicaid"] = (1.0 - medicaid_federal_share) * m_mcd

    fed_corp = params.pick("omb", ["receipts", "corporat"], "money",
                           preferred="receipts_corporation_income")
    state_corp = params.first("corporate", [["state", "corporat"]], "money",
                              preferred="state_corporate_net_income_tax_2024")
    corp_fed_share = fed_corp / (fed_corp + state_corp)
    fed["item_C"] = corp_fed_share * vec("C")
    stl["item_C"] = (1.0 - corp_fed_share) * vec("C")

    fed_excise = params.pick("omb", ["receipts", "excise"], "money",
                             preferred="receipts_excise")
    state_excise = params.first("corporate", [["selective", "sales"]], "money",
                                preferred="state_selective_sales_taxes_2024")
    excise_fed_share = fed_excise / (fed_excise + state_excise)
    fed["item_X"] = excise_fed_share * vec("X")
    stl["item_X"] = (1.0 - excise_fed_share) * vec("X")

    splits = dict(k12_federal_share=k12_federal_share,
                  medicaid_federal_share=medicaid_federal_share,
                  corporate_federal_share=corp_fed_share,
                  excise_federal_share=excise_fed_share,
                  tanf_federal_share=args.tanf_federal_share,
                  unemployment_federal_share=0.0,
                  k12_current_spending_us=k12_current_us)

    return dict(d=d, index=index, n_units=n_units, weights=weights, w0=w0, heads=heads,
                civilian=civilian, groups=groups, totals=totals, params=params,
                fed=fed, stl=stl, base_matrix=base_matrix, means=means, codes=codes,
                exposure=exposure, splits=splits, centrals=centrals,
                us_resident=us_resident, share=share, unit_total=unit_total,
                payer_cell=payer_cell, medical_anchors=anchors)


# --------------------------------------------------------------------- item N
def institutional_split(acc):
    """Item N split into corrections (state-local) and public nursing (mixed)."""
    cells_df = pd.read_csv(INSTITUTIONAL / "derived/acs_cells.csv")
    inst, inst_men = {}, {}
    for _, r in cells_df.iterrows():
        key = (r["group"], r["band"])
        if int(r["typehugq"]) == 2:
            inst[key] = inst.get(key, 0.0) + float(r["weighted"])
            if int(r["sex"]) == 1:
                inst_men[key] = inst_men.get(key, 0.0) + float(r["weighted"])
    prison, nf_public = 60989.0, (147e9 / 1.2e6) * (0.63 + 0.14)
    mcd_fed = acc["splits"]["medicaid_federal_share"]
    nursing_federal = (0.14 + 0.63 * mcd_fed) / (0.63 + 0.14)

    d, w0, groups = acc["d"], acc["w0"], acc["groups"]
    bands = np.digitize(d.A_AGE, [18, 25, 35, 45, 55, 65, 75])
    band_pop = {g: np.bincount(bands[groups[g]], weights=w0[groups[g]], minlength=8)
                for g in TARGETS}
    usborn = {}
    for i, b in enumerate(AL.ACS_BANDS):
        den = band_pop["mexican_second_gen"][i] + band_pop["mexican_third_plus_selfid"][i]
        usborn[b] = (band_pop["mexican_second_gen"][i] / den,
                     band_pop["mexican_third_plus_selfid"][i] / den)

    def cost(acs_key, b):
        i = inst.get((acs_key, b), 0.0)
        if i <= 0:
            return 0.0, 0.0
        if b in {"65_74", "75_99"}:
            return 0.0, i * nf_public
        ms = inst_men.get((acs_key, b), 0.0) / i
        return 0.5 * (i * prison + i * prison * ms), 0.0

    out = {}
    for g in TARGETS + [UNION, WHITE, ALL_NATIVE]:
        corr = nurse = 0.0
        for b in AL.ACS_BANDS:
            if g == UNION:
                keys = [("mexico_born", 1.0), ("usborn_mexican", 1.0)]
            elif g == "mexico_born":
                keys = [("mexico_born", 1.0)]
            elif g == "mexican_second_gen":
                keys = [("usborn_mexican", usborn[b][0])]
            elif g == "mexican_third_plus_selfid":
                keys = [("usborn_mexican", usborn[b][1])]
            elif g == WHITE:
                keys = [("native_nh_white", 1.0)]
            else:
                keys = [("all_natives", 1.0)]
            for k, wgt in keys:
                c, n = cost(k, b)
                corr += wgt * c
                nurse += wgt * n
        out[g] = dict(corrections=-corr, nursing=-nurse, total=-(corr + nurse),
                      federal=-(nurse * nursing_federal),
                      state_local=-(corr + nurse * (1.0 - nursing_federal)))
    acc["splits"]["nursing_federal_share"] = nursing_federal
    return out


# ------------------------------------------------------------------- stage 2
def native_households(acc, cog, cex):
    """Per-SPM-unit financing bases for native-headed units."""
    d, heads, w0 = acc["d"], acc["heads"], acc["w0"]
    totals, unit_total = acc["totals"], acc["unit_total"]
    n_units = acc["n_units"]
    order = heads.index.to_numpy()

    hw = heads.pwwgt0.to_numpy(dtype=float)
    native_head = heads.PRCITSHP.isin([1, 2, 3]).to_numpy()
    tenure_code = heads.H_TENURE.to_numpy(dtype=int)
    tenure = np.where(tenure_code == 1, "owner",
                      np.where(tenure_code == 2, "renter", "no_cash_rent"))
    fips = heads.GESTFIPS.to_numpy(dtype=int)
    income = heads.SPM_RESOURCES.to_numpy(dtype=float)

    wage = unit_total(d.WSAL_VAL.clip(lower=0).to_numpy(dtype=float))
    capital = unit_total((d.INT_VAL + d.DIV_VAL + d.RNT_VAL).clip(lower=0).to_numpy(dtype=float))
    fed_iit = unit_total(d.FEDTAX_AC.to_numpy(dtype=float))
    payroll = unit_total(d.FICA.to_numpy(dtype=float)) + totals["employer_payroll"]
    st_iit = unit_total(d.STATETAX_A.to_numpy(dtype=float))
    consumption = consumption_of(np.clip(income, 0, None), *cex)

    df = pd.DataFrame(dict(
        unit=np.arange(n_units), weight=hw, native=native_head, fips=fips,
        tenure=tenure, income=income,
        fed_individual_income=fed_iit, fed_social_insurance=payroll,
        wage=wage, capital=capital, consumption=consumption,
        st_individual_income=st_iit,
        prop_owner=totals["property_tax_owner"],
        prop_renter=totals["property_tax_renter_proxy"],
    ))
    return df[df.native].reset_index(drop=True)


def decile_codes(income, weight):
    order = np.argsort(income, kind="stable")
    cum = np.cumsum(weight[order]) / weight.sum()
    code = np.empty(len(income), dtype=int)
    code[order] = np.clip((cum * 10).astype(int), 0, 9)
    return code


def instrument_shares(hh, cog_row, passthrough, args):
    """Share of each revenue instrument borne by each household, within a geography.

    Returns a DataFrame column per instrument, each summing to 1 over the frame
    (weighted). Negative shares are possible and kept: a unit with a net
    refundable credit finances a negative share of the individual income tax.
    """
    w = hh.weight.to_numpy()

    def norm(basis):
        """Shares of an instrument. A basis that is zero everywhere (Texas has no
        individual income tax) returns zeros; the revenue mix gives it weight zero,
        and the closure gate in main() checks that the shares still sum to one."""
        basis = np.asarray(basis, dtype=float)
        den = float(basis @ w)
        if den == 0:
            return np.zeros_like(basis)
        return basis / den

    cons = norm(hh.consumption.to_numpy())
    wage_s = norm(hh.wage.to_numpy())
    cap_s = norm(hh.capital.to_numpy())
    corp = args.corporate_labour_share * wage_s + (1 - args.corporate_labour_share) * cap_s

    owner_base = hh.prop_owner.to_numpy()
    renter_base = hh.prop_renter.to_numpy()
    owner_dollars = float(owner_base @ w)
    renter_dollars = float(renter_base @ w)
    total_property = cog_row["property"]
    resid_share = max(0.0, 1.0 - (owner_dollars + renter_dollars) / total_property)
    occ_owner = owner_dollars / total_property
    occ_renter = renter_dollars / total_property
    # Rental property tax: `passthrough` to the tenant, the rest to the landlord,
    # who is a holder of capital. Non-residential property tax also to capital.
    prop = (occ_owner * norm(owner_base)
            + occ_renter * (passthrough * norm(renter_base) + (1 - passthrough) * cap_s)
            + resid_share * cap_s)

    out = pd.DataFrame(dict(
        fed_individual_income=norm(hh.fed_individual_income.to_numpy()),
        fed_social_insurance=norm(hh.fed_social_insurance.to_numpy()),
        fed_corporate=corp,
        fed_excise=cons,
        st_property=prop,
        st_general_sales=cons,
        st_selective_sales=cons,
        st_individual_income=norm(hh.st_individual_income.to_numpy()),
        st_corporate=corp,
        st_other_taxes=cons,
        st_charges=cons,
    ))
    meta = dict(occupied_owner_share_of_property_tax=occ_owner,
                occupied_renter_share_of_property_tax=occ_renter,
                nonresidential_residual_share=resid_share,
                owner_base_dollars=owner_dollars, renter_base_dollars=renter_dollars,
                cog_property_tax_dollars=total_property)
    return out, meta


def revenue_mix(params, cog_row):
    """Weights with which each convention loads the instruments."""
    fed_keys = [("fed_individual_income", "receipts_individual_income"),
                ("fed_social_insurance", "receipts_social_insurance_retirement"),
                ("fed_corporate", "receipts_corporation_income"),
                ("fed_excise", "receipts_excise")]
    fed = {}
    for name, key in fed_keys:
        v = params.pick("omb", [key], "money", preferred=key)
        if v is None:
            raise SystemExit(f"[BLOCKED] OMB receipt line missing: {key}")
        fed[name] = v
    total = params.pick("omb", ["receipts_total"], "money", preferred="receipts_total")
    other = total - sum(fed.values())
    # "Other receipts" (estate and gift, customs, miscellaneous) carry no separate
    # base here and are spread pro rata over the four measured instruments.
    scale = 1.0 + other / sum(fed.values())
    fed = {k: v * scale / total for k, v in fed.items()}
    if abs(sum(fed.values()) - 1.0) > 1e-9:
        raise SystemExit("[BLOCKED] federal receipt mix does not sum to one")

    stl_map = {"st_property": "property", "st_general_sales": "general_sales",
               "st_selective_sales": "selective_sales",
               "st_individual_income": "individual_income",
               "st_corporate": "corporate_income",
               "st_other_taxes": None, "st_charges": "charges_and_misc"}
    own = cog_row["own_source"]
    stl = {}
    for k, col in stl_map.items():
        if k == "st_other_taxes":
            stl[k] = (cog_row["motor_vehicle_license"] + cog_row["other_taxes"]) / own
        else:
            stl[k] = cog_row[col] / own
    if abs(sum(stl.values()) - 1.0) > 5e-3:
        raise SystemExit(f"[BLOCKED] state-local own-source mix sums to {sum(stl.values())}")
    stl = {k: v / sum(stl.values()) for k, v in stl.items()}
    return fed, stl


# ------------------------------------------------------------------------ main
def cell_frame(hh, shares, weight):
    cell = hh[["decile", "tenure"]].copy()
    cell["households"] = weight
    cell["income_dollars"] = hh.income.to_numpy() * weight
    for k in shares.columns:
        cell[k] = shares[k].to_numpy() * weight
    return cell.groupby(["decile", "tenure"], as_index=False).sum()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--params", default=str(ABS / "params/params.json"))
    ap.add_argument("--tanf-federal-share", type=float, default=0.55)
    ap.add_argument("--corporate-labour-share", type=float, default=0.25)
    ap.add_argument("--f-arm", default="zero",
                    choices=["zero", "per_capita", "proportional_to_federal_tax"],
                    help="item F (defense, net interest, general government) allocation arm")
    ap.add_argument("--out-dir", default=str(OUT))
    args = ap.parse_args()
    out = Path(args.out_dir)
    out.mkdir(parents=True, exist_ok=True)
    globals()["OUT"] = out

    acc = build_account(args)
    inst = institutional_split(acc)
    cog = read_cog_revenue(RESIDUAL / "_cache/22slsstab1.xlsx")
    cex = cex_consumption_curve()
    local_params = json.loads((HERE / "params_incidence.json").read_text())
    r_avg = local_params["treasury_avg_interest_rate_total_interest_bearing_debt_2024_09_30"]["value"] / 100.0
    r_10y = local_params["treasury_10y_par_yield_2026_09_17"]["value"] / 100.0

    d, w0, groups = acc["d"], acc["w0"], acc["groups"]
    fips_person = d.GESTFIPS.to_numpy(dtype=int)

    # ---- account by group, geography and level of government -----------------
    rows = []
    for g in TARGETS + [UNION, WHITE, ALL_NATIVE]:
        mask_g = groups[g]
        pop_g = float((w0 * mask_g).sum())
        for geo, fp in GEOGRAPHIES.items():
            m = mask_g if fp is None else (mask_g & (fips_person == fp))
            wm = w0 * m
            pop = float(wm.sum())
            n_share = pop / pop_g
            fed_total = sum(float(v @ wm) for v in acc["fed"].values()) + inst[g]["federal"] * n_share
            stl_total = sum(float(v @ wm) for v in acc["stl"].values()) + inst[g]["state_local"] * n_share
            rows.append(dict(group=g, geography=geo, population=pop,
                             federal_bn=fed_total / 1e9, state_local_bn=stl_total / 1e9,
                             total_bn=(fed_total + stl_total) / 1e9,
                             per_person=(fed_total + stl_total) / pop if pop else np.nan))
    by_level = pd.DataFrame(rows)
    by_level.to_csv(OUT / "account_by_level.csv", index=False)

    def account_of(group, geo):
        r = by_level[(by_level.group == group) & (by_level.geography == geo)].iloc[0]
        return float(r.federal_bn) * 1e9, float(r.state_local_bn) * 1e9

    union_us = sum(account_of(UNION, "US")) / 1e9
    if args.f_arm == "zero":
        gate = abs(union_us - (-263.224141)) <= 0.02
        print(f"[gate] union complete absolute rebuilt {union_us:+.6f}bn vs published "
              f"-263.224141bn -> {'PASS' if gate else 'FAIL'}", flush=True)
        if not gate:
            raise SystemExit(f"[BLOCKED] account rebuild gate failed: {union_us}")
    else:
        print(f"[arm] item F = {args.f_arm}: union complete absolute {union_us:+.6f}bn",
              flush=True)

    detail = []
    for bucket, store in [("federal", acc["fed"]), ("state_local", acc["stl"])]:
        for name, v in store.items():
            for g in [UNION, WHITE, ALL_NATIVE]:
                detail.append(dict(bucket=bucket, column=name, group=g,
                                   dollars_bn=float(v @ (w0 * groups[g])) / 1e9))
    for g in [UNION, WHITE, ALL_NATIVE]:
        for bucket in ["federal", "state_local"]:
            detail.append(dict(bucket=bucket, column="item_N_institutional", group=g,
                               dollars_bn=inst[g][bucket] / 1e9))
    pd.DataFrame(detail).to_csv(OUT / "account_columns.csv", index=False)

    # ---- financing side ------------------------------------------------------
    hh_all = native_households(acc, cog, cex)
    w_all = hh_all.weight.to_numpy()
    hh_all["decile_us"] = decile_codes(hh_all.income.to_numpy(), w_all) + 1
    fed_mix_us, _ = revenue_mix(acc["params"], cog.loc[0])

    share_rows, meta_rows, matrix_rows = [], [], []
    national_shares = {}
    for pt in [0.0, 0.5, 1.0]:
        sh, meta = instrument_shares(hh_all, cog.loc[0], pt, args)
        national_shares[pt] = sh
        meta_rows.append(dict(geography="US", frame="national", passthrough=pt, **meta))

    conventions = [("marginal_deficit_avg_rate_3.324pct", r_avg,
                    "marginal: federal part borrowed, annual interest at the FY2024 "
                    "average rate on interest-bearing debt; state-local balanced in-year"),
                   ("marginal_deficit_10y_4.94pct", r_10y,
                    "marginal: federal part borrowed, annual interest at the 10-year "
                    "Treasury par yield; state-local balanced in-year"),
                   ("average_pro_rata", 1.0,
                    "average: the whole net cost financed in-year pro rata by the "
                    "existing tax mix at each level of government")]

    for group in [UNION, WHITE]:
        for geo, fp in GEOGRAPHIES.items():
            if fp is None:
                hh = hh_all.copy()
                hh["decile"] = hh["decile_us"]
            else:
                hh = hh_all[hh_all.fips == fp].reset_index(drop=True)
                hh["decile"] = decile_codes(hh.income.to_numpy(), hh.weight.to_numpy()) + 1
            w = hh.weight.to_numpy()
            cog_row = cog.loc[0 if fp is None else fp]
            _, stl_mix = revenue_mix(acc["params"], cog_row)
            fed_national, _ = account_of(group, "US")
            _, stl_here = account_of(group, geo)

            for pt in [0.0, 0.5, 1.0]:
                sh_geo, meta = instrument_shares(hh, cog_row, pt, args)
                if fp is not None:
                    meta_rows.append(dict(geography=geo, frame="state", passthrough=pt, **meta))
                sh_fed = (national_shares[pt] if fp is None
                          else national_shares[pt].loc[hh_all.fips.to_numpy() == fp].reset_index(drop=True))
                agg_stl = cell_frame(hh, sh_geo, w)
                agg_fed = cell_frame(hh, sh_fed, w)
                agg_stl["state_local_share"] = sum(stl_mix[k] * agg_stl[k] for k in stl_mix)
                agg_fed["federal_share"] = sum(fed_mix_us[k] * agg_fed[k] for k in fed_mix_us)
                closure_stl = float(agg_stl["state_local_share"].sum())
                if abs(closure_stl - 1.0) > 2e-3:
                    raise SystemExit(f"[BLOCKED] {geo} state-local shares sum to {closure_stl}")
                if fp is None and abs(float(agg_fed["federal_share"].sum()) - 1.0) > 2e-3:
                    raise SystemExit("[BLOCKED] national federal shares do not sum to one")
                merged = agg_stl[["decile", "tenure", "households", "income_dollars",
                                  "state_local_share"]].merge(
                    agg_fed[["decile", "tenure", "federal_share"]], on=["decile", "tenure"])
                if group == UNION:
                    for _, r in merged.iterrows():
                        share_rows.append(dict(geography=geo, passthrough=pt,
                                               decile=int(r.decile), tenure=r.tenure,
                                               households=r.households,
                                               income_dollars=r.income_dollars,
                                               federal_share=r.federal_share,
                                               state_local_share=r.state_local_share))
                for conv, rate, note in conventions:
                    fed_amount = -fed_national * rate
                    stl_amount = -stl_here
                    for _, r in merged.iterrows():
                        f = fed_amount * r.federal_share
                        s = stl_amount * r.state_local_share
                        matrix_rows.append(dict(
                            group=group, geography=geo, convention=conv, passthrough=pt,
                            decile=int(r.decile), tenure=r.tenure,
                            households=r.households, income_dollars=r.income_dollars,
                            federal_dollars=f, state_local_dollars=s, total_dollars=f + s,
                            per_household=(f + s) / r.households if r.households else np.nan,
                            share_of_income=(f + s) / r.income_dollars if r.income_dollars else np.nan,
                            note=note))
    pd.DataFrame(share_rows).to_csv(OUT / "instrument_shares.csv", index=False)
    pd.DataFrame(meta_rows).to_csv(OUT / "property_tax_structure.csv", index=False)
    matrix = pd.DataFrame(matrix_rows)
    matrix.to_csv(OUT / "incidence_matrix.csv", index=False)

    interest = []
    for group in [UNION, WHITE, ALL_NATIVE]:
        fed_national, stl_us = account_of(group, "US")
        for label, rate in [("fy2024_average_rate_on_interest_bearing_debt", r_avg),
                            ("ten_year_par_yield_2026_09_17", r_10y)]:
            interest.append(dict(group=group, federal_bn=fed_national / 1e9,
                                 state_local_bn=stl_us / 1e9,
                                 total_bn=(fed_national + stl_us) / 1e9,
                                 deficit_financed_share=fed_national / (fed_national + stl_us),
                                 rate=rate, annual_interest_bn=-fed_national * rate / 1e9))
    pd.DataFrame(interest).to_csv(OUT / "interest.csv", index=False)

    audit = dict(splits=acc["splits"],
                 federal_receipt_mix=fed_mix_us,
                 state_local_own_source_mix_us=revenue_mix(acc["params"], cog.loc[0])[1],
                 institutional=inst,
                 cex_income=list(cex[0]), cex_expenditure=list(cex[1]),
                 rates=dict(fy2024_average=r_avg, ten_year=r_10y),
                 native_households_weighted=float(w_all.sum()),
                 native_households_unweighted=int(len(hh_all)),
                 gate_union_absolute_bn=union_us,
                 central_arms=acc["centrals"], item_F_arm=args.f_arm,
                 medical_anchors=acc["medical_anchors"])
    (OUT / "audit.json").write_text(json.dumps(audit, indent=2, default=float))
    print("[done] all outputs written to", OUT, flush=True)


if __name__ == "__main__":
    main()
