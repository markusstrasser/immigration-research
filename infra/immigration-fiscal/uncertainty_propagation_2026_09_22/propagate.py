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

--case sept24 (added 2026-09-24) also carries these sources to the adopted main
cases of September 23 and 24, specification by specification, after
`node sept24_specs.cjs` has written derived/sept24/ (see adopted_cases). Each
later case in later_cases.json does the same for its main case and the
uncorrected model at its responses, from derived/<case>/ (written by the same
script): --case sept26 (CBO's one-year school response, 0.63-0.66) and --case
sept26_schools (schools at full average cost), then --case sept27 (the return on public capital; the default,
as the last entry). The September 20 outputs are written as before and do not change.

From sept27 on, the administrative benefit keys' re-keying is recomputed on the same 161 CPS weights and its
replicate deviation joins the account's before the variance is taken (conceptual audit 2026-09-27, section A):
the two correlate negatively, so appending the benefit keys' SE independently overstated the CPS error. The
result is a partial sampling approximation whose net error is unresolved, not a bound in either direction: the
other omitted covariances (the production term, the school supplement, the pooled medical translator) can go
either way.
"""
from __future__ import annotations

import argparse
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


# --------------------------------------------------------------------------
# The adopted main cases of September 23, 24 and later (--case sept24, sept26, sept26_schools)
# --------------------------------------------------------------------------
MAIN_PROFILE = "cbo_category_lag_non_school_full"
MEDICAID = "medicaid_and_chip_other_medical"
# A case with the return on public capital (sept27): the lines that respond in the long run, and the lines whose
# group amounts key the return (sept24_specs.cjs writes the derivatives as kcoef_<line>).
LONG_RUN_LINES = ["economic_affairs_services", "recreation_culture"]
KCOEF_LINES = ["education_services", "school_reprice", "college_rekey", "public_order_safety", "health_services",
               "general_public_services", "economic_affairs_services", "recreation_culture", "enterprise_share"]
# Later cases, case -> main-case lane, one line each; sept24_specs.cjs reads the same file.
LATER_CASES = json.loads((HERE / "later_cases.json").read_text())
# Per --case: the main case's summary, then (row label, band in that summary, column tag in
# derived/<case>/) for the uncorrected frame and for the adopted case.
ADOPTED = {
    "sept24": ("main_case_2026_09_24/derived/summary.json",
               (("sept23", "adopted_2026_09_23", "sept23"), ("sept24", "main_case", "sept24"))),
    **{name: (f"{lane}/derived/summary.json",
              (("uncorrected_at_adopted_responses", "uncorrected_at_adopted_responses", "uncorrected"),
               (name, "main_case", name)))
       for name, lane in LATER_CASES.items()},
}


def benefit_replicates():
    """The central administrative benefit keys (admin_benefit_keys_2026_09_24/compare.py) on all 161 CPS weights.

    The producer builds its programme table and the account's allocations as locals of main() and then records
    and writes. A trace stops main() at its first line after the table exists, so the producer writes nothing
    (share_comparisons, its only earlier writer, is skipped), as the conceptual audit's probe_uncertainty.py does.
    Each central (BV) factor f = re-keyed union share / key union share is rebuilt with the producer's functions
    on the CPS ASEC 2025 replicate weights this lane uses; its change now x (f - 1) and that change's replicate SE
    must equal derived/program_keys.csv (1e-8). Returns {(allocation, line): (f, now_bn, share of the line)}.
    """
    ad = load_module(FISCAL / "admin_benefit_keys_2026_09_24/compare.py", "up_admin_keys")
    ad.share_comparisons = lambda: None
    local = {}

    class Stop(Exception):
        pass

    def trace(frame, event, arg):
        if frame.f_code is not ad.main.__code__:
            return None
        if event == "line" and "progs" in frame.f_locals:
            local.update(frame.f_locals)
            raise Stop
        return trace
    sys.settrace(trace)
    try:
        ad.main()
    except Stop:
        pass
    finally:
        sys.settrace(None)
    if "progs" not in local or "alloc" not in local:
        raise ValueError("[BLOCKED] compare.py main() no longer builds its programme table before it records")
    published = pd.read_csv(ad.D / "program_keys.csv").query("spec == 'BV'").set_index(["programme", "allocation"])
    out = {}
    for prog, admin, comp, base, keys, line, share, acs, acs_screen, _ in local["progs"]:
        invalid, _ = ad.validity(prog, admin, acs_screen)
        a_states = [x for x in ad.ROUTE_A if not invalid[ad.STATES.index(x)]]
        spec = ad.specs_for(prog, admin, comp, ad.acs_m(acs), a_states, base=base, invalid=invalid)["BV"]
        for a, km in keys.items():
            kp = ad.key_parts(*km)
            f = np.asarray(ad.rekey(spec, kp) / kp["U"], float)
            now = float(local["alloc"].loc[(line, a), "target_bn"]) * share
            p = published.loc[(prog, a)]
            if abs(now * (f[0] - 1) - p.change_bn) > 1e-8 or abs(ad.rep_se(now * (f - 1)) - p.change_se_bn) > 1e-8:
                raise ValueError(f"[BLOCKED] {prog}/{a}: the central re-keying differs from program_keys.csv")
            if (a, line) in out:
                raise ValueError(f"[BLOCKED] two programmes re-key {line}")
            out[(a, line)] = (f, now, share)
    return out


def adopted_cases(ctx, name, joint=None):
    """The lane's error sources on the adopted main cases, specification by specification.

    Point costs are the engine's (sept24_specs.cjs -> derived/<name>/spec_costs.csv). The September 23
    frame is the September 20 case plus general government at response 0.59 or 0.84 on the per-head
    key, and justice by use and uninsured use as fixed target shifts on the per-head and Medicaid keys
    (gate: every specification rebuilds to 1e-6). Its CPS error adds general government's per-head
    replicate spread times that response; the shifts carry none here. On September 24 each line's CPS
    replicate deviation and each MEPS payer gradient is scaled, to first order, by the ratio of the
    group's corrected to uncorrected target on the key this lane rebuilt: ratio-type corrections
    rescale that key, and replacement dollars are treated the same way. The synthetic correction
    lines carry no sampling error here; their spreads are the package's ranges. The benefit keys'
    published SE (admin_benefit_keys_2026_09_24/derived/package_se.csv) is added in separate columns,
    as if independent of the CPS error of the lines it re-keys; it is not (same replicates, see joint).

    Later cases (later_cases.json; "sept26", then "sept26_schools" with schools at full average cost):
    the same, at the case's responses (the payload's meta.responses, written into spec_costs.csv beside
    the September 24 values they replace). Each specification finds
    its September 20 case by the September 24 school response; general government enters at the new
    response, and the education line's response rises by school share x (new - old school response),
    in the rebuild (gate, 1e-6) and in the CPS and school-correction errors. The consumption key's
    edits scale the CPS errors of the four receipt lines they touch by the same first-order ratio.

    A case with the return on public capital ("sept27": its spec_costs.csv has capital columns) adds, in the
    rebuild and in the errors: the long-run responses of economic affairs and recreation (service lines this
    lane replicates), rental assistance (housing_subsidies on the housing_support key, replicated here), the
    enterprise receipt (its key is the group's population share, general government's replicated key) and
    the capital return. The return's derivative with respect to each key line's group amount (kcoef_<line>,
    from sept24_specs.cjs) adds to that line's weight wherever the line's amount carries an error: the CPS
    replicates, the MEPS gradient of health services and the school correction of the education lines.

    joint (default: such a case, sept27 on) carries the administrative benefit keys in the CPS block. On each
    replicate the payload's benefit change on a line, stack factor x now x (f - 1) (derived/<case>/benefit_factors.csv
    and benefit_replicates()), moves with f; its signed deviation, times the line's response (transfers 1, rental
    assistance at the specification's), joins the account's before the variance (first order, the change's level
    fixed at the account's point). se_cps_fiscal_keys_bn and every combined column then use that joint CPS error.
    Beside it: the account's CPS error alone, the benefit keys' own, their correlation, the two appended as if
    independent, the joint error with the factor-product term (the change's level on the replicate), and the
    published append of package_se.csv to the account's combined error.
    """
    summary_file, ((base, base_band, base_tag), (adopted, adopted_band, adopted_tag)) = ADOPTED[name]
    tag = {base: base_tag, adopted: adopted_tag}
    sub = OUT / name
    specs = pd.read_csv(sub / "spec_costs.csv")
    capital = "capital_uncorrected_bn" in specs.columns
    joint = capital if joint is None else joint
    lt = pd.read_csv(sub / "line_targets.csv").set_index(["side", "line", "key", "allocation"])
    main = json.loads((FISCAL / summary_file).read_text())
    ben_se = pd.read_csv(FISCAL / "admin_benefit_keys_2026_09_24/derived/package_se.csv").query(
        "package == 'central'").set_index("allocation").se_bn
    for case, want in ((base, main[base_band]), (adopted, main[adopted_band])):
        got = [specs[f"cost_{tag[case]}_bn"].min(), specs[f"cost_{tag[case]}_bn"].max()]
        if not np.allclose(got, want, rtol=0, atol=1e-9):
            raise ValueError(f"{case} specifications do not span the published band: {got} vs {want}")

    def target(case, side, line, key, a):
        v = lt.loc[(side, line, key, a), f"target_{tag[case]}_bn"]
        return 0.0 if pd.isna(v) else float(v)

    def ratio(case, kind, line, a):
        if case == base:
            return 1.0
        side, key = ("receipt", "cbo_collective") if kind == "receipt" else ("spending", ctx["lane_keys"][(a, line)])
        t0 = target(base, side, line, key, a)
        return target(adopted, side, line, key, a) / t0 if t0 else 1.0

    sp, hf, skeys, ncell = ctx["spending"], ctx["hf"], ctx["skeys"], ctx["ncell"]
    gps = {}
    for a in ["personal", "shared"]:
        g = sp.query("allocation == @a and category == 'general_public_services'").iloc[0]
        gps[a] = g.national_bn * hf * skeys[a][g.allocation_key]
        ctx["lane_keys"][(a, "general_public_services")] = g.allocation_key
    extra = [((a, "service", "general_public_services"), gps[a]) for a in gps]
    if capital:
        # Rental assistance on its account key, and the enterprise receipt: its national amount times the
        # group's population share, general government's per-head key (target / resident population).
        es_national = float(main["enterprises"]["receipt_at_end_specifications"]["national_bn"])
        rent, es_share = {}, {}
        for a in ["personal", "shared"]:
            h = sp.query("allocation == @a and category == 'housing_subsidies'").iloc[0]
            g = sp.query("allocation == @a and category == 'general_public_services'").iloc[0]
            if h.allocation_key != "housing_support" or g.allocation_key != "population":
                raise ValueError("rental assistance or general government is not on the key this lane replicates")
            rent[a] = h.national_bn * hf * skeys[a]["housing_support"]
            es_share[a] = gps[a] / g.national_bn
            ctx["lane_keys"][(a, "housing_subsidies")] = "housing_support"
            extra += [((a, "subsidy", "housing_subsidies"), rent[a]),
                      ((a, "receipt", "enterprise_surplus"), es_national * es_share[a])]
    ben_lines = {}
    if joint:
        # The benefit keys' factor on the replicates and each line's stack factor in the payload; the payload's
        # change must be the producer's (1e-9). A line's amount on the replicates: rental assistance's key, or the
        # transfer line this lane rebuilds.
        bf = pd.read_csv(sub / "benefit_factors.csv").set_index(["line", "allocation"])
        reps = benefit_replicates()
        if set(bf.index) != {(line, a) for a, line in reps}:
            raise ValueError("[BLOCKED] benefit_factors.csv and the producer re-key different lines")
        for (a, line), (f, now, share) in reps.items():
            if not np.isclose(bf.loc[(line, a), "delta_bn"], now * (f[0] - 1), rtol=0, atol=1e-9):
                raise ValueError(f"[BLOCKED] {line}/{a}: the payload's benefit change is not the producer's")
            amount = None if line == "housing_subsidies" else ctx["line_reps"][(a, "transfer", line)]
            ben_lines.setdefault(a, []).append((line, f, now, share, amount, float(bf.loc[(line, a), "stack_factor"])))
    # Every rebuilt line equals the engine model's target on the same key at replicate 0 (model.json
    # stores targets to 1e-8 bn).
    for (a, kind, line), rep in list(ctx["line_reps"].items()) + extra:
        side, key = ("receipt", "cbo_collective") if kind == "receipt" else ("spending", ctx["lane_keys"][(a, line)])
        if not np.isclose(rep[0], target(base, side, line, key, a), rtol=0, atol=1e-8):
            raise ValueError(f"{line}/{key}/{a} differs from the engine model at replicate 0")

    cases = ctx["cases"].query("profile == @MAIN_PROFILE")
    lane = ctx["case_frame"].query("profile == @MAIN_PROFILE")
    comps, pf, school_rel = ctx["comps"], ctx["pf"], ctx["school_rel"]
    rows = []
    for s in specs.itertuples():
        a = s.allocation
        school_old = getattr(s, "school_sept24", s.school)      # the September 20 case's school response
        pick = ((cases.allocation == a) & (cases.normalization == s.normalization)
                & np.isclose(cases.school_share, s.share, rtol=0, atol=1e-6)
                & np.isclose(cases.school_response, school_old, rtol=0, atol=1e-12))
        if pick.sum() != 1:
            raise ValueError(f"no unique September 20 case for {s}")
        c = cases[pick].iloc[0]
        ref = lane[(lane.case_id == c.case_id) & (lane.normalization == s.normalization)].iloc[0]
        edu_key = ctx["lane_keys"][(a, "education_services")]
        rebuilt = (-c.welfare_bn + s.gg * target(base, "spending", "general_public_services", "population", a)
                   + target(base, "spending", "public_order_safety", s.justice, a)
                   - target(base, "spending", "public_order_safety", "population", a)
                   + target(base, "spending", MEDICAID, s.uc, a) - target(base, "spending", MEDICAID, "medicaid", a)
                   + s.share * (s.school - school_old) * target(base, "spending", "education_services", edu_key, a))
        cc = comps.query("case_id == @c.case_id")
        kc = {}                                                  # the capital return's derivatives
        if capital:
            for line in LONG_RUN_LINES:
                if cc.query("component == @line").response.iloc[0] != 0:
                    raise ValueError(f"{line} responds in September 20 case {c.case_id}; the rebuild assumes 0")
                rebuilt += getattr(s, f"response_{line}") * target(base, "spending", line, ctx["lane_keys"][(a, line)], a)
            rebuilt += (s.response_housing_subsidies * target(base, "spending", "housing_subsidies", "housing_support", a)
                        - s.response_receipt_enterprise_surplus * target(base, "receipt", "enterprise_surplus",
                                                                          "cbo_collective", a)
                        + s.capital_uncorrected_bn)
            kc = {line: getattr(s, f"kcoef_{line}") for line in KCOEF_LINES}
        base_cost = getattr(s, f"cost_{tag[base]}_bn")
        if not np.isclose(rebuilt, base_cost, rtol=0, atol=1e-6):
            raise ValueError(f"{base} specification not rebuilt from case {c.case_id}: {rebuilt} vs {base_cost}")
        edu = cc.query("component in ['school_current', 'other_education_current']")
        resp = {r.component: r.response for r in cc.itertuples() if r.component in SERVICE_CATEGORIES}
        resp["education_services"] = edu.responsive_bn.sum() / edu.assigned_bn.sum()
        resp20 = dict(resp)                                      # the September 20 case's responses
        if s.school != school_old:
            # The main profile's non-school education responds fully: r = share x school + (1 - share).
            if not np.isclose(resp["education_services"], s.share * school_old + 1 - s.share, rtol=0, atol=1e-12):
                raise ValueError(f"education response of case {c.case_id} is not share x school + (1 - share)")
            resp["education_services"] += s.share * (s.school - school_old)
        for line in LONG_RUN_LINES if capital else ():
            resp[line] = getattr(s, f"response_{line}")
        se_pf = float(pf.loc[s.normalization].private_plus_receipts_se_sampling_bn)

        def cps_dev(case, weights):
            dev = np.zeros(161)
            for (al, kind, line), rep in ctx["line_reps"].items():
                if al == a:
                    sign, weight = (1.0, 1.0) if kind == "receipt" else (-1.0, 1.0 if kind == "transfer" else weights[line])
                    dev += sign * weight * ratio(case, kind, line, a) * (rep - rep[0])
            return dev

        def meps_se(case, kc):
            grad = np.zeros(len(MEDICAL) * ncell)
            for p, key in enumerate(MEDICAL):
                dshare, cats = ctx["meps_parts"][(a, key)]
                for cat in cats.itertuples():
                    grad[p * ncell:(p + 1) * ncell] += (-cat.national_bn * hf[0] * dshare * ratio(case, "transfer", cat.category, a)
                                                        * (1 + kc.get(cat.category, 0.0)))
            return float(np.sqrt(grad @ ctx["cov"] @ grad))

        for case in (base, adopted):
            # A key line's amount enters the cost at its response and the capital return at its derivative.
            dev = cps_dev(case, {k: v + kc.get(k, 0.0) for k, v in resp.items()} if capital else resp)
            # Positive control: on the uncorrected frame at the September 20 case's own responses the
            # CPS, MEPS and school errors of that case reproduce.
            if case == base and not np.isclose(sdr(cps_dev(case, resp20)), ref.se_cps_fiscal_keys_bn, rtol=1e-9, atol=0):
                raise ValueError("CPS error of the September 20 case not reproduced")
            gg_dev = ratio(case, "service", "general_public_services", a) * (gps[a] - gps[a][0])
            if capital:
                # Gate: the derivatives times this lane's targets rebuild the case's capital return (1e-6).
                def key_of(line):
                    return (s.justice if line == "public_order_safety" else "k" if line in ("school_reprice", "college_rekey")
                            else ctx["lane_keys"][(a, line)])
                rebuilt_k = (sum(kc[line] * target(case, "spending", line, key_of(line), a)
                                 for line in KCOEF_LINES if line != "enterprise_share")
                             + kc["enterprise_share"] * target(case, "receipt", "enterprise_surplus", "cbo_collective", a)
                             / es_national)
                if not np.isclose(rebuilt_k, getattr(s, f"capital_{tag[case]}_bn"), rtol=0, atol=1e-6):
                    raise ValueError(f"{case}: the capital return is not rebuilt from the key lines: {rebuilt_k}")
                d_share = ratio(case, "receipt", "enterprise_surplus", a) * (es_share[a] - es_share[a][0])
                dev_gg = -(s.gg + kc["general_public_services"]) * gg_dev
                dev_other = (-s.response_housing_subsidies * ratio(case, "subsidy", "housing_subsidies", a) * (rent[a] - rent[a][0])
                             + (s.response_receipt_enterprise_surplus * es_national - kc["enterprise_share"]) * d_share)
                dev_capital = -(kc["general_public_services"] * gg_dev + kc["enterprise_share"] * d_share
                                + sum(kc[line] * ratio(case, "service", line, a) * (rep - rep[0])
                                      for line in KCOEF_LINES if (rep := ctx["line_reps"].get((a, "service", line))) is not None))
                dev_account = dev + dev_gg + dev_other
            else:
                dev_gg = -s.gg * ratio(case, "service", "general_public_services", a) * (gps[a] - gps[a][0])
                dev_account = dev + dev_gg
            se_account = sdr(dev_account)
            # The benefit keys' change on the replicates as a welfare deviation: first order (the change's level at
            # the account's point) and with the factor product (its level on the replicate).
            b, b_product = np.zeros(161), np.zeros(161)
            for line, f, now, share, amount, factor in (ben_lines.get(a, []) if case == adopted else []):
                w = -factor * (getattr(s, "response_housing_subsidies", 0.0) if line == "housing_subsidies" else 1.0)
                if w:
                    amount = rent[a] if amount is None else amount
                    b += w * now * (f - f[0])
                    b_product += w * share * amount * (f - f[0])
            se_cps = sdr(dev_account + b) if joint else se_account
            se_m = meps_se(case, kc)

            def education_dollars(r, school):
                return (r["education_services"] * target(case, "spending", "education_services", edu_key, a)
                        + s.share * school * target(case, "spending", "school_reprice", "k", a)
                        + (1 - s.share) * target(case, "spending", "college_rekey", "k", a))
            edu_dollars = education_dollars(resp, s.school)
            if capital:
                # The K-12 and college returns: their keys are the education lines' amounts.
                edu_capital = (kc["education_services"] * target(case, "spending", "education_services", edu_key, a)
                               + kc["school_reprice"] * target(case, "spending", "school_reprice", "k", a)
                               + kc["college_rekey"] * target(case, "spending", "college_rekey", "k", a))
                edu_dollars += edu_capital
            se_school = edu_dollars * school_rel[a]["indep"]
            se_school_up = edu_dollars * school_rel[a]["upper"]
            if case == base and not (
                    np.isclose(meps_se(case, {}), ref.se_meps_donor_bn, rtol=1e-9, atol=0)
                    and np.isclose(education_dollars(resp20, school_old) * school_rel[a]["indep"],
                                   ref.se_school_correction_bn, rtol=1e-9, atol=0)):
                raise ValueError("MEPS or school error of the September 20 case not reproduced")
            indep = np.sqrt(se_cps ** 2 + se_pf ** 2 + se_school ** 2 + se_m ** 2)
            envelope = se_cps + se_pf + se_school_up + se_m
            ben = float(ben_se[a]) if case == adopted else 0.0
            # The published append: package_se.csv beside the account's combined error without the benefit keys.
            indep_account = np.sqrt(se_account ** 2 + se_pf ** 2 + se_school ** 2 + se_m ** 2) if joint else indep
            cost = getattr(s, f"cost_{tag[case]}_bn")
            rows.append(dict(case=case, allocation=a, normalization=s.normalization, school_share=s.share,
                             school_response=s.school, general_government_response=s.gg, medicaid_key=s.uc,
                             justice_key=s.justice, sept20_case_id=c.case_id, net_cost_bn=cost,
                             se_cps_fiscal_keys_bn=se_cps, se_cps_general_government_part_bn=sdr(dev_gg),
                             se_production_term_bn=se_pf, se_school_correction_bn=se_school, se_meps_donor_bn=se_m,
                             se_combined_independent_bn=indep, se_all_positive_correlation_bn=envelope,
                             ci95_low_bn=cost - 1.96 * indep, ci95_high_bn=cost + 1.96 * indep,
                             ci95_envelope_low_bn=cost - 1.96 * envelope, ci95_envelope_high_bn=cost + 1.96 * envelope,
                             se_benefit_keys_package_bn=ben, se_with_benefit_keys_bn=np.sqrt(indep_account ** 2 + ben ** 2),
                             ci95_with_benefit_keys_low_bn=cost - 1.96 * np.sqrt(indep_account ** 2 + ben ** 2),
                             ci95_with_benefit_keys_high_bn=cost + 1.96 * np.sqrt(indep_account ** 2 + ben ** 2)))
            if capital:
                rows[-1].update(capital_return_bn=getattr(s, f"capital_{tag[case]}_bn"),
                                capital_return_education_bn=edu_capital, se_cps_capital_part_bn=sdr(dev_capital),
                                se_cps_rental_and_enterprise_part_bn=sdr(dev_other))
            if joint:
                se_b = sdr(b)
                cov = 4 / 160 * float(np.dot(dev_account[1:] - dev_account[0], b[1:] - b[0]))
                rows[-1].update(se_cps_account_keys_bn=se_account, se_benefit_keys_replicate_bn=se_b,
                                corr_cps_benefit_keys=cov / (se_account * se_b) if se_b else np.nan,
                                se_cps_independent_append_bn=float(np.hypot(se_account, se_b)),
                                se_cps_factor_product_bn=sdr(dev_account + b_product))
    frame = pd.DataFrame(rows)
    frame.to_csv(sub / "case_uncertainty.csv", index=False)
    summary = {}
    for case, f in frame.groupby("case"):
        summary[case] = dict(
            net_cost_band_bn=[f.net_cost_bn.min(), f.net_cost_bn.max()],
            se_independent_bn=[f.se_combined_independent_bn.min(), f.se_combined_independent_bn.max()],
            se_positive_correlation_bn=[f.se_all_positive_correlation_bn.min(), f.se_all_positive_correlation_bn.max()],
            se_cps_bn=[f.se_cps_fiscal_keys_bn.min(), f.se_cps_fiscal_keys_bn.max()],
            ci95_union_bn=[f.ci95_low_bn.min(), f.ci95_high_bn.max()],
            ci95_envelope_union_bn=[f.ci95_envelope_low_bn.min(), f.ci95_envelope_high_bn.max()],
            ci95_with_benefit_keys_union_bn=[f.ci95_with_benefit_keys_low_bn.min(), f.ci95_with_benefit_keys_high_bn.max()],
            specifications=int(len(f)))
        if capital:
            summary[case].update(capital_return_band_bn=[f.capital_return_bn.min(), f.capital_return_bn.max()],
                                 se_cps_capital_part_bn=[f.se_cps_capital_part_bn.min(), f.se_cps_capital_part_bn.max()])
        if joint:
            cols = ["se_cps_account_keys_bn"] + (["se_benefit_keys_replicate_bn", "corr_cps_benefit_keys",
                                                  "se_cps_independent_append_bn", "se_cps_factor_product_bn",
                                                  "se_with_benefit_keys_bn"] if case == adopted else [])
            summary[case].update({c: [f[c].min(), f[c].max()] for c in cols})
    (sub / "summary.json").write_text(json.dumps(summary, indent=2, default=float) + "\n")
    for case, v in summary.items():
        print(f"[{case}] cost {v['net_cost_band_bn'][0]:.1f}-{v['net_cost_band_bn'][1]:.1f}  "
              f"SE {v['se_independent_bn'][0]:.2f}-{v['se_independent_bn'][1]:.2f}  "
              f"95% union {v['ci95_union_bn'][0]:.1f}-{v['ci95_union_bn'][1]:.1f}  "
              f"envelope {v['ci95_envelope_union_bn'][0]:.1f}-{v['ci95_envelope_union_bn'][1]:.1f}", flush=True)


def main():
    ap = argparse.ArgumentParser(description="Propagate sampling and donor errors onto the account's cases.")
    ap.add_argument("--case", choices=(*reversed(list(LATER_CASES)), "sept24", "sept20"), default=list(LATER_CASES)[-1],
                    help="a later case (default: the last in later_cases.json, sept26_schools: schools at full average "
                         "cost; sept26: CBO's one-year school response, 0.63-0.66) or sept24: also that adopted case; "
                         "sept20: its files only")
    args = ap.parse_args()
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
    line_reps, lane_keys = {}, {}          # per line, for --case sept24
    for allocation in ["personal", "shared"]:
        dr = direct.query("allocation == @allocation")
        rep = np.zeros(161)
        for r in dr.itertuples():
            line = r.national_bn * rkeys[allocation][r.allocation_key]
            rep += line
            line_reps[(allocation, "receipt", r.category)] = line_reps.get((allocation, "receipt", r.category), 0) + line
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
                kind = "transfer" if cls == "household_transfer" else "service"
                line_reps[(allocation, kind, r.category)] = line_reps.get((allocation, kind, r.category), 0) + vals
                lane_keys[(allocation, r.category)] = r.allocation_key
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
    meps_rows, meps_parts = [], {}
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
            meps_parts[(allocation, key)] = (dshare, cats[["category", "national_bn"]].copy())
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
    if args.case in ADOPTED:
        adopted_cases(dict(line_reps=line_reps, lane_keys=lane_keys, meps_parts=meps_parts, cov=cov, ncell=ncell,
                           hf=hf, spending=spending, skeys=skeys, cases=cases, comps=comps, pf=pf,
                           school_rel=school_rel, case_frame=case_frame), args.case)


if __name__ == "__main__":
    main()
