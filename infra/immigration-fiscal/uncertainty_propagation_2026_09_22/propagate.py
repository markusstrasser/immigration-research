"""Propagate published sampling and donor errors onto the complete-account headline.

Read-only consumer of existing lanes; no upstream .py is edited. It rebuilds the
CPS incidence keys that feed the complete annual account under all 161 CPS ASEC
2025 weights (full + 160 successive-difference replicates), checks replicate 0
against both producers' exported keys, and carries the replicate spread through
the account's own headline formula

    welfare = direct receipts - household transfers
              - sum_c response_c * services_c + (P + F)

where national BEA totals are fixed control totals, so CPS sampling error enters
only through the target's key shares and the household pool fraction.

Other error sources are added from what upstream lanes already publish (or, for
the MEPS donor means, from the same stratified-PSU Taylor estimator the build
helper uses), under an explicit independence assumption with a
perfect-positive-correlation envelope alongside.
"""
from __future__ import annotations

import importlib.util
import json
import sys
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
FISCAL = HERE.parent
ROOT = FISCAL.parents[1]
OUT = HERE / "derived"
REPS = [f"pwwgt{i}" for i in range(161)]
RESIDENT = 340_110_988.0
CPS_ZIP = FISCAL / "gen_ledger_extension_2026_09_16/_cache/asecpub25csv.zip"
CAPITAL_CATEGORIES = {"corporate_capital", "corporate_labor", "modeled_owner_property",
                      "remaining_production_property", "personal_property_tax"}
SERVICE_CATEGORIES = ["education_services", "public_order_safety", "economic_affairs_services",
                      "housing_community_services", "health_services", "recreation_culture",
                      "income_security_services"]
MEDICAL = {"medicare": ["TOTMCR24"], "medicaid": ["TOTMCD24"], "va_medical": ["TOTVA24"],
           "tricare": ["TOTTRI24"], "health_other": ["TOTVA24", "TOTTRI24", "TOTOFD24", "TOTSTL24"]}
FIELDS = ["PH_SEQ", "PPPOS", "A_AGE", "PRPERTYP", "PRCITSHP", "PENATVTY", "PEFNTVTY", "PEMNTVTY",
          "PRDTHSP", "SPM_ID", "SPM_HEAD", "SS_VAL", "SSI_VAL", "PAW_VAL", "UC_VAL", "VET_VAL",
          "WC_VAL", "WSAL_VAL", "EIT_CRED", "ACTC_CRD", "SPM_SNAPSUB", "SPM_ENGVAL", "SPM_WICVAL",
          "SPM_CAPHOUSESUB", "SPM_RESOURCES", "PUB", "PRIV", "MIL", "CHAMPVA", "MCAID", "AGI",
          "SEMP_VAL", "FRSE_VAL", "FICA", "INT_VAL", "DIV_VAL", "RNT_VAL", "FEDTAX_BC",
          "STATETAX_A", "MCARE"]


def sdr(values):
    values = np.asarray(values, float)
    return float(np.sqrt(4 / 160 * np.square(values[1:] - values[0]).sum()))


def load_module(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


SPENDING = load_module(FISCAL / "full_account_spending_2026_09_20/builder.py", "up_spending_builder")
sys.path.insert(0, str(FISCAL / "build"))
from meps_health_transport_2024 import donor_model, read_meps  # noqa: E402


# --------------------------------------------------------------------------
# CPS microdata and replicate key shares
# --------------------------------------------------------------------------
def load_cps():
    with zipfile.ZipFile(CPS_ZIP) as z:
        d = pd.read_csv(z.open("pppub25.csv"), usecols=FIELDS)
        w = pd.read_csv(z.open("asec_csv_repwgt_2025.csv"), usecols=["h_seq", "PPPOS", *REPS])
    w = w.rename(columns={"h_seq": "PH_SEQ"})
    d = d.merge(w, on=["PH_SEQ", "PPPOS"], validate="one_to_one", how="left")
    if d[REPS].isna().any().any():
        raise ValueError("CPS person without replicate weights")
    return d


def unit_equal(values, ids):
    return SPENDING.equal_unit_share(values, ids)


def receipt_vectors(d):
    """Same definitions as full_account_receipts_2026_09_20/builder.py::derive_keys."""
    wage = d.WSAL_VAL.clip(lower=0).to_numpy(float)
    se = .9235 * np.maximum(d.SEMP_VAL.to_numpy(float) + d.FRSE_VAL.to_numpy(float), 0)
    se = np.where(se >= 400, se, 0)
    se_capped = np.minimum(se, np.maximum(168600 - np.minimum(wage, 168600), 0))
    size = d.groupby("SPM_ID").SPM_ID.transform("size").to_numpy(float)
    medicare = d.MCARE.eq(1).to_numpy(float)
    return dict(
        population=np.ones(len(d)), adults=d.A_AGE.ge(18).to_numpy(float), wage=wage,
        wage_oasdi=np.minimum(wage, 168600), self_payroll=.124 * se_capped + .029 * se,
        positive_fica_worker=d.FICA.gt(0).to_numpy(float),
        capital=(d.INT_VAL + d.DIV_VAL + d.RNT_VAL).clip(lower=0).to_numpy(float),
        interest_dividend=(d.INT_VAL + d.DIV_VAL).clip(lower=0).to_numpy(float),
        federal_liability=d.FEDTAX_BC.to_numpy(float),
        federal_high_agi=(d.FEDTAX_BC * d.AGI.ge(500000)).to_numpy(float),
        state_liability=d.STATETAX_A.clip(lower=0).to_numpy(float),
        consumption=d.SPM_RESOURCES.clip(lower=0).to_numpy(float) / size,
        medicare=medicare, medicare_income=medicare * (d.AGI.clip(lower=0).to_numpy(float) + 1))


def meps_inputs(d):
    fiscal = FISCAL
    meps = fiscal.parents[1] / "sources/immigration-fiscal/data/external/stage3/ahrq/meps_2024/h256dat.zip"
    md, _ = read_meps(meps, meps.with_name("h256su.txt"))
    cells, codes, cov_public = donor_model(md, d, False)
    valid = md.PERWT24F.gt(0) & md.AGE24X.ge(0) & md.BORNUSA.isin([1, 2])
    sample = md.loc[valid]
    index = pd.MultiIndex.from_frame(cells[["age_band", "born"]])
    means = {}
    for name, cols in MEDICAL.items():
        sums = sample.assign(wx=sample[cols].sum(axis=1) * sample.PERWT24F).groupby(["age_band", "born"]).wx.sum()
        pop = sample.groupby(["age_band", "born"]).PERWT24F.sum()
        mean = (sums / pop).reindex(index)
        if mean.isna().any():
            raise ValueError("Unmatched payer cell")
        means[name] = mean.to_numpy()
    return md, cells, codes, cov_public, means


def spending_vectors(d, codes, means):
    """Same definitions as full_account_spending_2026_09_20/builder.py::build_keys."""
    counts = d.groupby("SPM_ID").SPM_ID.transform("size").to_numpy()

    def unit_field(field):
        if not d.groupby("SPM_ID")[field].nunique().eq(1).all():
            raise ValueError(f"Nonconstant unit field {field}")
        return d[field].to_numpy(float) / counts
    dollars = {k: d[v].to_numpy(float) for k, v in [
        ("social_security", "SS_VAL"), ("ssi", "SSI_VAL"), ("cash_assistance", "PAW_VAL"),
        ("unemployment", "UC_VAL"), ("veterans", "VET_VAL"), ("workers_comp", "WC_VAL"), ("wages", "WSAL_VAL")]}
    dollars["refundable_credits"] = (d.EIT_CRED + d.ACTC_CRD).to_numpy(float)
    dollars["all_cash"] = sum(dollars[k] for k in ["social_security", "ssi", "cash_assistance", "unemployment", "veterans"])
    units = {k: unit_field(v) for k, v in [("snap", "SPM_SNAPSUB"), ("energy", "SPM_ENGVAL"),
                                            ("wic", "SPM_WICVAL"), ("housing_support", "SPM_CAPHOUSESUB")]}
    units["resources"] = np.maximum(unit_field("SPM_RESOURCES"), 0)
    ages = {"population": np.ones(len(d)), "age65plus": d.A_AGE.ge(65).to_numpy(float),
            "working_age": d.A_AGE.between(18, 64).to_numpy(float), "adults": d.A_AGE.ge(18).to_numpy(float),
            "age5_24": d.A_AGE.between(5, 24).to_numpy(float), "age18_24": d.A_AGE.between(18, 24).to_numpy(float),
            "medicaid_covered": d.MCAID.eq(1).to_numpy(float)}
    exposure = ~(d.PUB.eq(0) & d.PRIV.eq(0)).to_numpy()
    medical = {k: means[k][codes] * exposure for k in MEDICAL}
    out = {}
    for allocation in ["personal", "shared"]:
        vec = {}
        for k, v in dollars.items():
            vec[k] = v if allocation == "personal" else unit_equal(v, d.SPM_ID)
        vec.update(units)
        vec.update(ages)
        vec.update(medical)
        out[allocation] = vec
    return out, exposure


def replicate_shares(vectors, W, civ, target):
    shares = {}
    for name, v in vectors.items():
        if np.any(v < 0):
            raise ValueError(f"Negative proxy {name}")
        national = v[civ] @ W[civ]
        group = v[target] @ W[target]
        shares[name] = group / national
    return shares


# --------------------------------------------------------------------------
# MEPS donor covariance for every payer mean used by a key
# --------------------------------------------------------------------------
def payer_covariance(md, cells, payer_sets):
    """Stratified-PSU with-replacement Taylor covariance, as donor_model, for stacked payer means."""
    valid = (md.PERWT24F.gt(0) & md.AGE24X.ge(0) & md.BORNUSA.isin([1, 2])).to_numpy()
    w = md.PERWT24F.to_numpy(float)
    columns = []
    for name, cols in payer_sets.items():
        y = md[cols].sum(axis=1).to_numpy(float)
        for _, row in cells.iterrows():
            mask = valid & md.age_band.eq(row.age_band).to_numpy() & md.born.eq(row.born).to_numpy()
            pop = w[mask].sum()
            mean = (w[mask] * y[mask]).sum() / pop
            infl = np.zeros(len(md))
            infl[mask] = w[mask] * (y[mask] - mean) / pop
            columns.append(infl)
    influence = pd.DataFrame(np.column_stack(columns))
    design = md.loc[md.PERWT24F.gt(0), ["VARSTR", "VARPSU"]].drop_duplicates()
    influence["stratum"], influence["psu"] = md.VARSTR.to_numpy(), md.VARPSU.to_numpy()
    psus = influence.groupby(["stratum", "psu"]).sum().reindex(pd.MultiIndex.from_frame(design)).fillna(0)
    k = psus.shape[1]
    cov = np.zeros((k, k))
    for _, h in psus.groupby(level=0):
        if len(h) < 2:
            raise ValueError("Lonely MEPS PSU")
        c = h.to_numpy() - h.to_numpy().mean(axis=0)
        cov += len(h) / (len(h) - 1) * c.T @ c
    return cov


# --------------------------------------------------------------------------
# Account inputs from published derived CSVs
# --------------------------------------------------------------------------
def account_inputs():
    receipts = pd.read_csv(FISCAL / "full_account_receipts_2026_09_20/derived/category_allocations.csv")
    receipts = receipts.query("scenario_id == 'cbo_collective'")
    direct = receipts.response_class.isin(["personal_income", "household_direct"]) & ~receipts.category.isin(CAPITAL_CATEGORIES)
    spending = pd.read_csv(FISCAL / "full_account_spending_2026_09_20/derived/allocations.csv")
    spending = spending.query("scenario_id == 'complete_preferred_F_per_capita'")
    return receipts.loc[direct], spending


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    print("[stage] CPS load", flush=True)
    d = load_cps()
    civ, target = SPENDING.canonical_target(d)
    W = d[REPS].to_numpy(float)
    nt = W[target, 0].sum()
    if abs(nt - 40896574.15235156) > .01:
        raise ValueError(f"Target population drift {nt}")
    hf = W[civ].sum(axis=0) / RESIDENT
    print("[stage] MEPS donor model", flush=True)
    md, cells, codes, cov_public, means = meps_inputs(d)

    # ---- receipt keys, both conventions --------------------------------
    rvec = receipt_vectors(d)
    rkeys = {}
    for allocation in ["personal", "shared"]:
        vec = {k: (v if allocation == "personal" else unit_equal(v, d.SPM_ID)) for k, v in rvec.items()}
        rkeys[allocation] = replicate_shares(vec, W, civ, target)
    svec, exposure = spending_vectors(d, codes, means)
    skeys = {a: replicate_shares(svec[a], W, civ, target) for a in ["personal", "shared"]}

    # ---- key validation against both producers --------------------------
    pub_r = pd.read_csv(FISCAL / "full_account_receipts_2026_09_20/derived/allocation_keys.csv")
    pub_s = pd.read_csv(FISCAL / "full_account_spending_2026_09_20/derived/incidence_keys.csv")
    rows = []
    for r in pub_r.itertuples():
        if r.allocation_key == "resident_population":
            rep = W[target].sum(axis=0) / RESIDENT
        else:
            rep = rkeys[r.allocation][r.allocation_key]
        rows.append(dict(lane="receipts", allocation=r.allocation, key=r.allocation_key,
                         share_rebuilt=rep[0], share_published=r.target_key_share,
                         se_rebuilt=sdr(rep), se_published=r.target_share_sampling_se,
                         carries_cps_replicates=True))
    for r in pub_s.itertuples():
        if r.key in skeys[r.allocation]:
            rep = skeys[r.allocation][r.key]
            rows.append(dict(lane="spending", allocation=r.allocation, key=r.key, share_rebuilt=rep[0],
                             share_published=r.target_share, se_rebuilt=sdr(rep), se_published=np.nan,
                             carries_cps_replicates=True))
        else:
            rows.append(dict(lane="spending", allocation=r.allocation, key=r.key, share_rebuilt=np.nan,
                             share_published=r.target_share, se_rebuilt=np.nan, se_published=np.nan,
                             carries_cps_replicates=False))
    keycheck = pd.DataFrame(rows)
    ok = keycheck.dropna(subset=["share_rebuilt"])
    if not np.allclose(ok.share_rebuilt, ok.share_published, rtol=1e-9, atol=0):
        bad = ok.loc[~np.isclose(ok.share_rebuilt, ok.share_published, rtol=1e-9, atol=0)]
        raise ValueError(f"Replicate-0 key shares disagree with producers:\n{bad}")
    se_ok = keycheck.dropna(subset=["se_published"])
    if not np.allclose(se_ok.se_rebuilt, se_ok.se_published, rtol=1e-6, atol=0):
        raise ValueError("Rebuilt receipt-key SDR SEs disagree with the published ones")
    keycheck.to_csv(OUT / "key_replicate_check.csv", index=False)

    # ---- per-replicate account components -------------------------------
    direct, spending = account_inputs()
    comp_rows, comp_reps = [], {}
    for allocation in ["personal", "shared"]:
        dr = direct.query("allocation == @allocation")
        rep = np.zeros(161)
        for r in dr.itertuples():
            rep += r.national_bn * rkeys[allocation][r.allocation_key]
        if not np.isclose(rep[0], dr.target_bn.sum(), rtol=1e-12):
            raise ValueError("Direct receipts not reproduced at replicate 0")
        comp_reps[(allocation, "direct_receipts")] = rep
        sp = spending.query("allocation == @allocation")
        fixed_keys = {"education_mix", "postsecondary"}
        for cls in ["household_transfer", "service"]:
            for r in sp.query("response_class == @cls").itertuples():
                if r.allocation_key in fixed_keys:
                    share = np.full(161, r.target_key_share)
                else:
                    share = skeys[allocation][r.allocation_key]
                vals = r.national_bn * hf * share
                if not np.isclose(vals[0], r.target_bn, rtol=1e-9, atol=1e-12):
                    raise ValueError(f"Spending {r.category} not reproduced at replicate 0")
                name = "transfers" if cls == "household_transfer" else r.category
                comp_reps[(allocation, name)] = comp_reps.get((allocation, name), 0) + vals
    for (allocation, name), rep in comp_reps.items():
        comp_rows.append(dict(allocation=allocation, component=name, point_bn=rep[0], se_cps_bn=sdr(rep)))
    pd.DataFrame(comp_rows).to_csv(OUT / "component_sampling.csv", index=False)
    np.savez_compressed(OUT / "component_replicates.npz",
                        **{f"{a}|{n}": v for (a, n), v in comp_reps.items()})

    # ---- MEPS donor gradient --------------------------------------------
    cov = payer_covariance(md, cells, MEDICAL)
    check = payer_covariance(md, cells, {"public_paid": ["TOTMCR24", "TOTMCD24", "TOTVA24", "TOTTRI24", "TOTOFD24", "TOTSTL24"]})
    if not np.allclose(check, cov_public, rtol=1e-10, atol=0):
        raise ValueError("Payer covariance estimator does not reproduce donor_model")
    w0 = W[:, 0]
    ncell = len(cells)
    meps_rows = []
    for allocation in ["personal", "shared"]:
        g = np.zeros(len(MEDICAL) * ncell)
        sp = spending.query("allocation == @allocation")
        for p, key in enumerate(MEDICAL):
            v = svec[allocation][key]
            N = v[civ] @ w0[civ]
            share = skeys[allocation][key][0]
            T_j = np.bincount(codes[target], weights=(w0 * exposure)[target], minlength=ncell)
            N_j = np.bincount(codes[civ], weights=(w0 * exposure)[civ], minlength=ncell)
            dshare = (T_j - share * N_j) / N
            cats = sp.query("allocation_key == @key and response_class in ['household_transfer', 'service']")
            national = cats.national_bn.sum()
            # All medical-key categories respond fully in every headline case: welfare falls by target spending.
            g[p * ncell:(p + 1) * ncell] += -national * hf[0] * dshare
            meps_rows.append(dict(allocation=allocation, key=key, categories=";".join(cats.category),
                                  target_bn=float((cats.national_bn * hf[0] * share).sum()),
                                  se_meps_key_only_bn=float(np.sqrt(
                                      (national * hf[0] * dshare) @ cov[p * ncell:(p + 1) * ncell, p * ncell:(p + 1) * ncell]
                                      @ (national * hf[0] * dshare)))))
        meps_rows.append(dict(allocation=allocation, key="ALL_MEDICAL_JOINT", categories="all",
                              target_bn=np.nan, se_meps_key_only_bn=float(np.sqrt(g @ cov @ g))))
    meps = pd.DataFrame(meps_rows)
    meps.to_csv(OUT / "meps_donor_contribution.csv", index=False)
    se_meps = meps.query("key == 'ALL_MEDICAL_JOINT'").set_index("allocation").se_meps_key_only_bn

    # ---- school-correction sampling (published, partial) -----------------
    corr = pd.read_csv(FISCAL / "school_enrollment_2026_09_20/derived/correction_effects.csv")
    corr = corr.query("scenario == 'all_ages' and group == 'mexican_observed_total' and component == 'school'")
    upd = pd.read_csv(FISCAL / "school_enrollment_2026_09_20/derived/updated_account_components.csv")
    school_rel = {}
    for allocation in ["personal", "shared"]:
        c = corr.query("allocation == @allocation").iloc[0]
        t = upd.query("allocation == @allocation and group == 'mexican_observed_total' and component in ['school', 'P']").spending_bn.sum()
        school_rel[allocation] = dict(indep=c.se_zero_covariance_bn / t, upper=c.se_unknown_correlation_upper_bn / t,
                                      target_school_plus_P_bn=t, se_upper_bn=c.se_unknown_correlation_upper_bn)

    # ---- production term sampling (published) ---------------------------
    bens = pd.read_csv(FISCAL / "full_account_benefits_2026_09_20/derived/benefit_scenarios.csv")
    pf = bens.query("scenario_id in ['ces_0086_owner000', 'ces_0248_owner000']").set_index("normalization")

    # ---- cases ------------------------------------------------------------
    cases = pd.read_csv(FISCAL / "full_account_2026_09_20/derived/service_response_cases.csv")
    comps = pd.read_csv(FISCAL / "full_account_2026_09_20/derived/service_response_components.csv")
    out = []
    for c in cases.itertuples():
        cc = comps.query("case_id == @c.case_id")
        edu = cc.query("component in ['school_current', 'other_education_current']")
        resp = {r.component: r.response for r in cc.itertuples() if r.component in SERVICE_CATEGORIES}
        edu_eff = edu.responsive_bn.sum() / edu.assigned_bn.sum()
        resp["education_services"] = edu_eff
        a = c.allocation
        rep = comp_reps[(a, "direct_receipts")] - comp_reps[(a, "transfers")]
        for cat in SERVICE_CATEGORIES:
            rep = rep - resp[cat] * comp_reps[(a, cat)]
        pfv = pf.loc[c.normalization]
        welfare_rep = rep + pfv.private_plus_receipts_bn
        if not np.isclose(welfare_rep[0], c.welfare_bn, atol=1e-7):
            raise ValueError(f"Case {c.case_id} not reproduced")
        se_cps = sdr(welfare_rep)
        responsive_edu = edu_eff * comp_reps[(a, "education_services")][0]
        se_school = responsive_edu * school_rel[a]["indep"]
        se_school_up = responsive_edu * school_rel[a]["upper"]
        se_pf = float(pfv.private_plus_receipts_se_sampling_bn)
        se_m = float(se_meps[a])
        indep = np.sqrt(se_cps ** 2 + se_pf ** 2 + se_school ** 2 + se_m ** 2)
        envelope = se_cps + se_pf + se_school_up + se_m
        out.append(dict(case_id=c.case_id, allocation=a, normalization=c.normalization, profile=c.profile,
                        education_split=c.education_split, school_response=c.school_response,
                        net_cost_bn=-c.welfare_bn, se_cps_fiscal_keys_bn=se_cps, se_production_term_bn=se_pf,
                        se_school_correction_bn=se_school, se_meps_donor_bn=se_m,
                        se_combined_independent_bn=indep, se_all_positive_correlation_bn=envelope,
                        ci95_low_bn=-c.welfare_bn - 1.96 * indep, ci95_high_bn=-c.welfare_bn + 1.96 * indep,
                        ci95_envelope_low_bn=-c.welfare_bn - 1.96 * envelope,
                        ci95_envelope_high_bn=-c.welfare_bn + 1.96 * envelope))
    case_frame = pd.DataFrame(out)
    case_frame.to_csv(OUT / "case_uncertainty.csv", index=False)

    meta = dict(hf_point=float(hf[0]), hf_se=sdr(hf), school_relative_se=school_rel,
                production_term_se={k: float(v) for k, v in pf.private_plus_receipts_se_sampling_bn.items()},
                meps_cells=int(ncell), meps_payer_sets=list(MEDICAL))
    (OUT / "propagation_meta.json").write_text(json.dumps(meta, indent=2) + "\n")
    print(case_frame.groupby("profile")[["net_cost_bn", "se_cps_fiscal_keys_bn", "se_combined_independent_bn",
                                         "se_all_positive_correlation_bn"]].agg(["min", "max"]).to_string())


if __name__ == "__main__":
    main()
