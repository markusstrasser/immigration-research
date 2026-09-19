"""Education/origin resident fiscal accounts with preserved survey uncertainty.

Reuses the repaired CPS/MEPS fiscal builders. No record linkage, admission-effect
identification, or education-specific institutional imputation is performed.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import sys

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
BANDS = ["25-34", "35-44", "45-54", "55-64", "65-74", "75+"]
EDUCATIONS = ["lt_hs", "hs_only", "some_college", "ba_plus", "all"]
ORIGIN_CODES = {
    "mexico_born": [303],
    "other_central_america": list(range(310, 317)),
    "caribbean": [321, 323, 324, 327, 328, 329, 330, 332, 333, 338, 339, 340, 341, 343],
    "south_america": [360, 361, 362, 363, 364, 365, 368, 369, 370, 372, 373, 374],
    "southeast_asia": [205, 206, 211, 223, 226, 233, 236, 242, 247],
}
REFERENCES = ["all_native", "third_plus_nh_white"]
MIN_N, MIN_ESS = 30, 20.0
ACCOUNT_NAMES = ["partial", "expanded_excluding_N", "expanded_excluding_N_D"]


def education_masks(d):
    eligible = d.A_AGE.ge(25).to_numpy()
    if not d.loc[eligible, "A_HGA"].between(31, 46).all():
        raise ValueError("Adult education missing/reserved: never classify as less than high school")
    return {
        "lt_hs": d.A_HGA.between(31, 38).to_numpy() & eligible,
        "hs_only": d.A_HGA.eq(39).to_numpy() & eligible,
        "some_college": d.A_HGA.between(40, 42).to_numpy() & eligible,
        "ba_plus": d.A_HGA.between(43, 46).to_numpy() & eligible,
        "all": eligible,
    }


def domain_masks(d, groups):
    civilian = (d.PRPERTYP.eq(2) | d.A_AGE.lt(15)).to_numpy()
    foreign = d.PRCITSHP.isin([4, 5]).to_numpy()
    origins = {name: foreign & d.PENATVTY.isin(codes).to_numpy()
               for name, codes in ORIGIN_CODES.items()}
    origins.update({name: np.asarray(groups[name]) for name in REFERENCES})
    if not d.loc[foreign, "PEINUSYR"].between(1, 28).all():
        raise ValueError("Foreign-born entry code missing or outside verified 2025 codebook")
    education = education_masks(d)
    masks = {}
    for origin, origin_mask in origins.items():
        for ed, ed_mask in education.items():
            masks[(origin, ed, "stock")] = origin_mask & ed_mask & civilian
            if origin not in REFERENCES:
                masks[(origin, ed, "recent_2016_2025")] = (
                    origin_mask & ed_mask & civilian & d.PEINUSYR.between(25, 28).to_numpy())
    return masks


def support(mask, weights, bands):
    rows = []
    for band in range(6):
        use = mask & (bands == band)
        w = weights[use]
        n = len(w)
        pop = w.sum(axis=0)
        ess = float(pop[0] ** 2 / np.square(w[:, 0]).sum()) if n else 0.0
        positive = bool((pop > 0).all())
        rows.append(dict(band=band, band_label=BANDS[band], unweighted_n=n,
                         population=float(pop[0]), weight_ess=ess,
                         all_replicates_positive=positive,
                         support=positive and n >= MIN_N and ess >= MIN_ESS,
                         support_reason=("supported" if positive and n >= MIN_N and ess >= MIN_ESS
                                         else "empty" if not n else "sparse")))
    return rows


def summarize(values, gradient, covariance):
    if values.shape != (161,) or not np.isfinite(values).all():
        raise ValueError("Expected point plus160 finite CPS replicates")
    cps = float(4 / 160 * np.square(values[1:] - values[0]).sum())
    meps = float(gradient @ covariance @ gradient)
    if meps < -1e-5:
        raise ValueError("Negative MEPS variance")
    se = np.sqrt(cps + max(meps, 0))
    return dict(estimate=float(values[0]), se_cps=np.sqrt(cps), se_meps=np.sqrt(max(meps, 0)),
                se_joint=se, ci95_low=float(values[0] - 1.96 * se),
                ci95_high=float(values[0] + 1.96 * se))


def aggregate(values, health, weights, mask, bands):
    n, y, h = [], [], []
    for band in range(6):
        use = mask & (bands == band)
        w = weights[use]
        n.append(w.sum(axis=0))
        y.append(values[use].T @ w)
        h.append(health[use].T @ w)
    return np.array(n), np.array(y), np.array(h)


def safe_means(totals, populations):
    result = np.full_like(totals, np.nan, dtype=float)
    np.divide(totals, populations, out=result, where=populations > 0)
    return result


def standardized_contrast(totals, populations, gradients, ref_totals, ref_pop,
                          ref_gradient, shares, selected):
    """Conditional fixed-standard contrast, same support for both populations."""
    if not selected.any() or shares[selected].sum() <= 0:
        raise ValueError("Empty age-standardization support")
    if (populations[selected] <= 0).any() or (ref_pop[selected] <= 0).any():
        raise ValueError("Nonpositive replicate population on selected support")
    s = shares[selected] / shares[selected].sum()
    value = (s[:, None] * (totals[selected] / populations[selected]
                           - ref_totals[selected] / ref_pop[selected])).sum(axis=0)
    gradient = (s[:, None] * (gradients[selected] / populations[selected, 0, None]
                             - ref_gradient[selected] / ref_pop[selected, 0, None])).sum(axis=0)
    return value, gradient


def sha(path):
    digest = hashlib.sha256()
    with Path(path).open("rb") as handle:
        for block in iter(lambda: handle.read(8 * 1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def verified_upstream_inputs(root):
    """Bind the repaired release's complete input audit before reusing its anchor."""
    audit_path = root / "infra/immigration-fiscal/ledger_absolute_2026_09_17/derived/audit.json"
    audit = json.loads(audit_path.read_text())
    if not audit.get("inputs") or not audit.get("age_profile_export", {}).get("files"):
        raise ValueError("Canonical repaired audit lacks input/profile fingerprints")
    sources = {str(audit_path): sha(audit_path)}
    for record in audit["inputs"]:
        path = Path(record["path"])
        if not path.is_absolute():
            path = root / path
        actual = sha(path)
        if actual != record["sha256"]:
            raise ValueError(f"Stale canonical repaired input; rebuild canonical ledger first: {path}")
        sources[str(path)] = actual
    for filename, expected in audit["age_profile_export"]["files"].items():
        path = audit_path.parent / filename
        actual = sha(path)
        if actual != expected:
            raise ValueError(f"Stale canonical age-profile anchor: {path}")
        sources[str(path)] = actual
    return sources


def configure(source_root):
    fiscal = source_root / "infra/immigration-fiscal"
    for folder in ["all_age_ledger_2026_09_17", "ledger_absolute_2026_09_17",
                   "arrival_window_fiscal_2026_09_18"]:
        sys.path.insert(0, str(fiscal / folder))
    import analyze as annual
    import absolute_ledger as absolute
    import arrival_window_ledger as arrival
    for field in ["A_HGA", "PEINUSYR", *absolute.EXTRA_PERSON]:
        if field not in annual.ext.base.PERSON:
            annual.ext.base.PERSON.append(field)
    return annual, absolute, arrival


def load_helper(path):
    spec = importlib.util.spec_from_file_location("joint_medical_donors", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-root", type=Path, default=HERE.parents[2])
    parser.add_argument("--out", type=Path, default=HERE / "derived")
    parser.add_argument("--health-helper", type=Path)
    args = parser.parse_args()
    root, out = args.source_root.resolve(), args.out.resolve()
    out.mkdir(parents=True, exist_ok=True)
    upstream_sources = verified_upstream_inputs(root)
    A, AL, arrival = configure(root)
    fiscal = root / "infra/immigration-fiscal"
    params_path = fiscal / "ledger_absolute_2026_09_17/params/params.json"
    params = AL.Params(params_path, False)
    cps = fiscal / "gen_ledger_extension_2026_09_16/_cache/asecpub25csv.zip"
    print("[stage] canonical CPS builder", flush=True)
    state = A.ext.build(argparse.Namespace(cps_zip=cps))
    d, weights = state["d"], state["person_weights"]
    civilian = (d.PRPERTYP.eq(2) | d.A_AGE.lt(15)).to_numpy()
    masks = domain_masks(d, state["group"])
    bands = np.digitize(d.A_AGE, [35, 45, 55, 65, 75])
    shared, personal, _ = A.matrices(state)
    medical_zip = root / "sources/immigration-fiscal/data/external/stage3/ahrq/meps_2024/h256dat.zip"
    medical_sas = medical_zip.with_name("h256su.txt")
    medical, anchors = A.read_meps(medical_zip, medical_sas)
    cells, codes, _ = A.donor_model(medical, d, False)
    payer_means = arrival._payer_means(medical, cells)
    exposure = ~(d.PUB.eq(0) & d.PRIV.eq(0)).to_numpy()
    health = np.eye(len(cells))[codes] * exposure[:, None]
    rmcd = params.nhea_over_meps("meps_coverage", [["ratio", "medicaid"]], "medicaid",
                                preferred="nhea_to_meps_ratio_medicaid")
    rmcr = params.nhea_over_meps("meps_coverage", [["ratio", "medicare"]], "medicare",
                                preferred="nhea_to_meps_ratio_medicare")
    if rmcd is None or rmcr is None:
        raise ValueError("Missing verified medical calibration coefficients")
    helper_path = args.health_helper or fiscal / "health_transport_sensitivity_2026_09_19/builder.py"
    helper = load_helper(helper_path)
    # The sibling helper fits all three outcomes jointly, preserving covariance.
    outcomes = pd.DataFrame({"raw_public": medical.public_paid,
                             "calibrated_public": medical.public_paid + (rmcd - 1) * medical.TOTMCD24
                                                  + (rmcr - 1) * medical.TOTMCR24,
                             "tricare": medical.TOTTRI24})
    valid = medical.PERWT24F.gt(0) & medical.AGE24X.ge(0) & medical.BORNUSA.isin([1, 2])
    donor = helper.domain_means_covariance(medical, ["age_band", "born"], outcomes, valid=valid)
    means, covariance = donor["means"], donor["covariance"]
    if not np.array_equal(donor["cells"][["age_band", "born"]].to_numpy(), cells[["age_band", "born"]].to_numpy()):
        raise ValueError("Joint medical donor order differs from canonical donor order")
    if means.shape != (len(cells), 3):
        raise ValueError("Expected cell-major raw/calibrated/TRICARE means")
    if not np.allclose(means[:, 0], cells.mean_public_paid):
        raise ValueError("Joint donor outcome does not reproduce canonical raw means")
    if not np.allclose(means[:, 1], means[:, 0] + (rmcd - 1) * payer_means["medicaid"]
                       + (rmcr - 1) * payer_means["medicare"]):
        raise ValueError("Calibrated payer outcome fails exact M reconstruction")
    support_rows = []
    support_map = {}
    for key, mask in masks.items():
        sr = support(mask, weights, bands)
        support_map[key] = sr
        support_rows.extend(dict(origin=key[0], education=key[1], entry=key[2], **row) for row in sr)
    origin_groups = {name: state["group"][name] & civilian for name in AL.TARGETS + REFERENCES}
    profiles, age_rows, comp_rows, estimate_rows, comparison_rows = [], [], [], [], []
    net_arrays, pop_arrays, gradient_arrays, f_arrays, f_gradients, support_arrays = [], [], [], [], [], []
    profile_lookup = {}
    old_profiles = pd.read_csv(fiscal / "ledger_absolute_2026_09_17/derived/age_profiles.csv")
    old_components = pd.read_csv(fiscal / "ledger_absolute_2026_09_17/derived/age_profile_components.csv")
    anchor_errors, central_meta = {}, {}
    national_h = health[civilian].T @ weights[civilian]
    for allocation, matrix in [("shared", shared), ("personal", personal)]:
        print(f"[stage] {allocation} repaired item charges", flush=True)
        # Build context from the same authoritative resources as the main ledger.
        resid = arrival.resid
        state_population = resid.read_state_population()
        ctx = dict(d=d, index=state["index"], n_units=state["n_units"], civilian=civilian,
                   weights=weights, heads=d.loc[d.SPM_HEAD.eq(1)].sort_values("SPM_ID"),
                   general_services=resid.read_general_services_per_capita(state_population),
                   assf=AL.read_assf_k12(arrival.GENEXT / "census_assf_fy2024_summary_tables.xlsx"),
                   omb=AL.read_omb_functions(arrival.RESIDUAL / "_cache/omb_hist03z1_fy2027.xlsx"),
                   capital=AL.read_cog_capital(arrival.RESIDUAL / "_cache/22slsstab1.xlsx", state_population),
                   donor_codes=codes, donor_payer_means=payer_means, exposure=exposure,
                   n_civilian=float(weights[civilian, 0].sum()),
                   us_resident=params.pick("population", ["2024"], "count"),
                   consumption_proxy=matrix[:, 4], off=[], allocation=allocation,
                   is_white_ref=origin_groups["third_plus_nh_white"],
                   is_target=np.logical_or.reduce([origin_groups[g] for g in AL.TARGETS]))
        if not ctx["us_resident"]:
            raise ValueError("Verified2024 resident denominator absent")
        legacy, dropped, centrals, _, _ = AL.build_charges(ctx, AL.Params(params_path, False))
        legacy_values = {item: legacy.data[legacy.columns.index(f"{item}|{arm}")]
                         for item, arm in centrals.items() if arm is not None}
        old_net = matrix @ A.COEFFICIENTS - health @ means[:, 0] + sum(legacy_values.values())
        anchor = old_profiles[(old_profiles.allocation == allocation)
                              & (old_profiles.account == "expanded")
                              & (old_profiles.group == "mexico_born") & (old_profiles.band >= 2)]
        inst = old_components[(old_components.allocation == allocation)
                              & (old_components.account == "expanded")
                              & (old_components.group == "mexico_born")
                              & (old_components.component == "N") & (old_components.band >= 2)]
        expected = anchor.sort_values("band").net_total.to_numpy() - inst.sort_values("band").signed_total.to_numpy()
        mask = masks[("mexico_born", "all", "stock")]
        actual = np.bincount(bands[mask], weights=old_net[mask] * weights[mask, 0], minlength=6)
        if not np.allclose(actual, expected, rtol=1e-10, atol=.05):
            raise ValueError("Legacy Mexico adult anchor failed before generalized D attribution")
        anchor_errors[allocation] = float(np.max(np.abs(actual - expected)))
        # Source parameters describe pupil ethnicity, so use observed ethnicity
        # consistently across origins rather than only the old Mexican target.
        ctx["is_target"] = d.PEHSPNON.eq(1).to_numpy() & civilian
        ctx["is_white_ref"] = (d.PEHSPNON.eq(2) & d.PRDTRACE.eq(1)).to_numpy() & civilian
        charges, dropped, centrals, _, _ = AL.build_charges(ctx, AL.Params(params_path, False))
        if any(arm is None for item, arm in centrals.items()):
            raise ValueError(f"Required central fiscal item absent: {centrals}")
        items = list(centrals)
        item_values = {item: charges.data[charges.columns.index(f"{item}|{centrals[item]}")]
                       for item in items}
        values = np.column_stack([matrix * A.COEFFICIENTS, *item_values.values()])
        component_names = list(A.COMPONENTS) + items
        central_meta[allocation] = dict(arms=centrals, dropped=dropped)
        f_key = charges.columns.index("F|per_capita")
        f_point = charges.data[f_key]
        f_total = charges.meta["F|per_capita"]["national_dollars"]
        # Recompute the TRICARE netting in every CPS replicate. The fixed federal
        # administrative total is not a CPS sampling estimate.
        f_gross = f_total + float(national_h[:, 0] @ means[:, 2])
        f_per_person = -(f_gross - means[:, 2] @ national_h) / ctx["us_resident"]
        if not np.allclose(f_per_person[0], f_point[civilian][0]):
            raise ValueError("F public-goods point reconstruction failed")
        for key, mask in masks.items():
            n, y, h = aggregate(values, health, weights, mask, bands)
            component = {name: y[:, k, :] for k, name in enumerate(component_names)}
            component["medical"] = -np.einsum("bjr,j->br", h, means[:, 0])
            if not np.allclose(component["M"], -np.einsum("bjr,j->br", h, means[:, 1] - means[:, 0]), rtol=1e-10, atol=.01):
                raise ValueError("Medical calibration increment differs from annual builder")
            for account in ACCOUNT_NAMES:
                selected_components = list(A.COMPONENTS) + ["medical"]
                if account != "partial":
                    selected_components += [item for item in items if not (account.endswith("_D") and item == "D")]
                net = sum(component[c] for c in selected_components)
                grad = np.zeros((6, means.size))
                grad[:, (0 if account == "partial" else 1)::3] = -h[:, :, 0]
                fg = np.zeros_like(grad)
                fg[:, 2::3] = n[:, 0, None] / ctx["us_resident"] * national_h[:, 0]
                profile_id = len(profiles)
                metadata = dict(profile_id=profile_id, allocation=allocation, account=account,
                                origin=key[0], education=key[1], entry=key[2])
                profiles.append(metadata)
                profile_lookup[(allocation, account, *key)] = profile_id
                net_arrays.append(net); pop_arrays.append(n); gradient_arrays.append(grad)
                f_arrays.append(n * f_per_person); f_gradients.append(fg)
                support_arrays.append([r["support"] for r in support_map[key]])
                for band, sr in enumerate(support_map[key]):
                    row = dict(**metadata, **sr, net_total=float(net[band, 0]),
                               net_per_person=(float(net[band, 0] / n[band, 0]) if n[band, 0] else np.nan))
                    if (n[band] > 0).all():
                        row.update(summarize(net[band] / n[band], grad[band] / n[band, 0], covariance))
                    age_rows.append(row)
                    comp_rows.extend(dict(**metadata, band=band, component=c,
                                          signed_total=float(component[c][band, 0])) for c in selected_components)
                # The working-age account retains all 25–64 records, with sparse
                # support warnings separate from estimates, never silent dropping.
                pop = n[:4].sum(axis=0)
                v = net[:4].sum(axis=0)
                g = grad[:4].sum(axis=0)
                use = mask & d.A_AGE.le(64).to_numpy()
                w = weights[use, 0]
                ess = w.sum() ** 2 / np.square(w).sum() if len(w) else 0
                if (pop > 0).all():
                    estimate_rows.append(dict(**metadata, age_scope="25-64", population=float(pop[0]),
                                              unweighted_n=int(use.sum()), weight_ess=float(ess),
                                              sparse_age_bands=sum(not r["support"] for r in support_map[key][:4]),
                                              metric="net_per_person", **summarize(v / pop, g / pop[0], covariance)))
                    estimate_rows.append(dict(**metadata, age_scope="25-64", population=float(pop[0]),
                                              unweighted_n=int(use.sum()), weight_ess=float(ess),
                                              sparse_age_bands=sum(not r["support"] for r in support_map[key][:4]),
                                              metric="net_total", **summarize(v, g, covariance)))
    nets, pops, grads = np.array(net_arrays), np.array(pop_arrays), np.array(gradient_arrays)
    supports = np.array(support_arrays, dtype=bool)
    for row in profiles:
        if row["education"] != "all":
            continue
        indices = [profile_lookup[(row["allocation"], row["account"], row["origin"], ed, row["entry"])]
                   for ed in EDUCATIONS[:4]]
        i = row["profile_id"]
        for label, arrays in [("population", pops), ("net total", nets), ("medical gradient", grads)]:
            if not np.allclose(arrays[i], arrays[indices].sum(axis=0), rtol=1e-10, atol=.05):
                raise ValueError(f"Education partition does not conserve {label}")
    # An all-native all-education fixed age standard is shared by every contrast;
    # education-conditioned references and all-education references are distinct.
    for metadata in profiles:
        i = metadata["profile_id"]
        base_key = (metadata["allocation"], metadata["account"])
        standard_i = profile_lookup[(*base_key, "all_native", "all", "stock")]
        shares = pops[standard_i, :, 0].copy(); shares[4:] = 0
        shares /= shares.sum()
        for reference in REFERENCES:
            for ref_education in dict.fromkeys([metadata["education"], "all"]):
                j = profile_lookup[(*base_key, reference, ref_education, "stock")]
                chosen = supports[i] & supports[j] & (np.arange(6) < 4)
                coverage = float(shares[chosen].sum())
                if chosen.any():
                    val, gradient = standardized_contrast(nets[i], pops[i], grads[i], nets[j], pops[j],
                                                         grads[j], shares, chosen)
                    comparison_rows.append(dict(**metadata, reference=reference, reference_education=ref_education,
                                                metric="common_age_gap_per_person", standard_mass=coverage,
                                                selected_bands=",".join(BANDS[b] for b in np.flatnonzero(chosen)),
                                                **summarize(val, gradient, covariance)))
                else:
                    comparison_rows.append(dict(**metadata, reference=reference, reference_education=ref_education,
                                                metric="common_age_gap_per_person", standard_mass=0.0,
                                                selected_bands="", estimate=np.nan))
                ni, nj = pops[i, :4].sum(axis=0), pops[j, :4].sum(axis=0)
                if (ni > 0).all() and (nj > 0).all():
                    val = nets[i, :4].sum(axis=0) / ni - nets[j, :4].sum(axis=0) / nj
                    gradient = grads[i, :4].sum(axis=0) / ni[0] - grads[j, :4].sum(axis=0) / nj[0]
                    comparison_rows.append(dict(**metadata, reference=reference, reference_education=ref_education,
                                                metric="unstandardized_gap_per_person", standard_mass=1.0,
                                                selected_bands=",".join(BANDS[:4]), **summarize(val, gradient, covariance)))
    tables = {"profiles.csv": profiles, "age_profiles.csv": age_rows, "age_components.csv": comp_rows,
              "annual_estimates.csv": estimate_rows, "comparisons.csv": comparison_rows, "support.csv": support_rows}
    for filename, rows in tables.items():
        pd.DataFrame(rows).to_csv(out / filename, index=False)
    np.savez_compressed(out / "uncertainty.npz", age_net_replicates=nets, age_population_replicates=pops,
                        age_medical_gradients=grads, medical_covariance=covariance, donor_means=means,
                        age_F_replicates=np.array(f_arrays), age_F_medical_gradients=np.array(f_gradients),
                        age_supported=supports,
                        raw_n=np.array([[r["unweighted_n"] for r in support_map[(p["origin"], p["education"], p["entry"])]] for p in profiles]),
                        weight_ess=np.array([[r["weight_ess"] for r in support_map[(p["origin"], p["education"], p["entry"])]] for p in profiles]))
    donor["cells"].to_csv(out / "medical_donor_cells.csv", index=False)
    manifest = dict(schema_version=1, price_year=2024, population="CPS ASEC2025 civilian household residents age25+",
                    main_age_scope="25-64", age_bands=BANDS, uncertainty="160 CPS SDR replicates plus joint full-design MEPS Taylor covariance; conditional on fitted CPS allocation and calibration coefficients and fixed model parameters, not total model uncertainty",
                    medical_outcomes=["raw_public", "calibrated_public", "tricare"], medical_order="cell-major; age_band then born; three outcomes per cell",
                    education_codes={"lt_hs": [31, 38], "hs_only": [39, 39], "some_college": [40, 42], "ba_plus": [43, 46]},
                    origin_codes=ORIGIN_CODES, min_n=MIN_N, min_weight_ess=MIN_ESS,
                    support_threshold_status="Analytical reporting thresholds, not an agency standard or guarantee",
                    institution_N="Excluded; separate matching ACS domain sensitivity required",
                    district_D="Generalized from old Mexican-only charge to observed Hispanic pupils and observed NHwhite pupils; ethnicity/state proxy; symmetric D0 account exported",
                    entry="PEINUSYR25-28,2016 through March2025 interview; current attained education not entry education",
                    education="Current attainment proxy, not latent skill; some_college includes associate degrees",
                    standardization="Fixed point-estimate all-native all-education25-64 age shares, renormalized over reported common support; conditional on shares",
                    native="PRCITSHP1/2/3 includes native persons born in territories or abroad to US parents",
                    geography="Caribbean and South America include English-speaking countries; SEA excludes unidentified Brunei/Timor-Leste",
                    medical_transport="Age×US-birth only; no measured origin/education-specific spending; covariance is sampling uncertainty conditional on transport",
                    F="Defense+interest+general-government average allocation, net CPS-weighted transported TRICARE; conditional government totals, propagated CPS/MEPS TRICARE uncertainty",
                    legacy_anchor_max_dollars=anchor_errors, central_items=central_meta, meps_anchors=anchors,
                    source_root=str(root), health_helper=str(helper_path.resolve()),
                    sources=upstream_sources | {str(p): sha(p) for p in [
                        cps, medical_zip, medical_sas, params_path, Path(AL.__file__), Path(A.__file__),
                        Path(A.ext.__file__), Path(arrival.__file__),
                        fiscal / "build/public_mvp_io.py", helper_path, Path(__file__),
                        root / "sources/immigration-fiscal/data/external/cps_asec_doc/cpsmar25.pdf"]},
                    outputs={name: sha(out / name) for name in [*tables, "uncertainty.npz", "medical_donor_cells.csv"]},
                    codebook="https://www2.census.gov/programs-surveys/cps/techdocs/cpsmar25.pdf; A_HGA6C-3, PEINUSYR6C-6, countries AppendixJ",
                    codebook_discrepancy="Standalone asec2025_ddl_pub_full.pdf says2022-2024 for entry28; full cpsmar25.pdf says2022-2025 and governs this lane")
    (out / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    print(f"[done] {len(profiles)} profiles, {len(estimate_rows)} annual estimates, {len(comparison_rows)} comparisons", flush=True)


if __name__ == "__main__":
    main()
