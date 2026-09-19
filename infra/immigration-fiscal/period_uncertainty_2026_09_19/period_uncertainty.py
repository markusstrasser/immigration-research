#!/usr/bin/env python3
"""Conditional sampling uncertainty and break-even amounts for adult period profiles.

Native-First: consume the education ledger's sufficient-statistic arrays with
NumPy; reuse the existing NVSS reader, without a new simulation framework.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
BAND_EDGES = np.array([25, 35, 45, 55, 65, 75, 101])
Z = 1.959963984540054


def fingerprint(path):
    path = Path(path)
    with path.open("rb") as stream:
        digest = hashlib.file_digest(stream, "sha256").hexdigest()
    return {"path": str(path.resolve()), "sha256": digest}


def verify_fingerprints(records):
    if not records:
        raise ValueError("Missing input/implementation fingerprints")
    for record in records:
        if fingerprint(record["path"])["sha256"] != record["sha256"]:
            raise ValueError(f"Stale input: {record['path']}")


def verify_releases(annual, institutions, root):
    release = json.loads((annual / "manifest.json").read_text())
    required = {"profiles.csv", "uncertainty.npz"}
    if not required.issubset(release.get("outputs", {})):
        raise ValueError("Annual release lacks required output fingerprints")
    verify_fingerprints([{"path": p, "sha256": h} for p, h in release["sources"].items()])
    verify_fingerprints([{"path": annual / p, "sha256": h} for p, h in release["outputs"].items()])
    inst = json.loads((institutions / "audit.json").read_text())
    if not {"domains.csv", "counts.npz"}.issubset(inst.get("exports", {})):
        raise ValueError("Institution release lacks required output fingerprints")
    verify_fingerprints([{"path": inst["source"], "sha256": inst["source_sha256"]},
                         {"path": institutions.parent / "institutional_counts.py",
                          "sha256": inst["implementation_sha256"]}])
    verify_fingerprints([{"path": institutions / p, "sha256": h} for p, h in inst["exports"].items()])


def verify_health_release(health_dir):
    audit = json.loads((health_dir / "audit.json").read_text())
    verify_fingerprints(audit["inputs"])
    outputs = audit.get("outputs", {})
    if not {"estimates.csv", "medical_uncertainty.npz"}.issubset(outputs):
        raise ValueError("Medical release lacks required output fingerprints")
    verify_fingerprints([{"path": health_dir / p, "sha256": h} for p, h in outputs.items()])


def sdr_variance(values, n_reps):
    values = np.asarray(values, dtype=float)
    if values.shape != (n_reps + 1,) or not np.isfinite(values).all():
        raise ValueError("Expected finite point estimate and every survey replicate")
    return float(4 / n_reps * np.square(values[1:] - values[0]).sum())


def survival_weights(table, rate, last_age=100):
    """Return six band weights and their derivatives for someone alive at25.

    At100, NVSS Lx represents the final open interval. It is discounted at100,
    as in the canonical period engine; truncation at85 is a separate scenario.
    """
    if rate <= -1 or not np.isfinite(rate) or not 25 <= last_age <= 100:
        raise ValueError("Invalid discount rate or horizon")
    if table.age.tolist() != list(range(101)) or table.lx.iloc[25] <= 0:
        raise ValueError("Invalid life table")
    ages = np.arange(25, last_age + 1)
    t = ages - 25
    exposure = table.Lx.to_numpy()[ages] / table.lx.iloc[25]
    if not np.isfinite(exposure).all() or (exposure < 0).any():
        raise ValueError("Invalid survival exposure")
    w = exposure * (1 + rate) ** (-t)
    derivative = -t * exposure * (1 + rate) ** (-t - 1)
    bands = np.digitize(ages, BAND_EDGES[1:-1])
    return (np.bincount(bands, weights=w, minlength=6),
            np.bincount(bands, weights=derivative, minlength=6))


def conditional_estimate(net, population, gradient, covariance, exposure,
                         institutional_counts=None, institution_price=0.0):
    """Combine independent survey errors without pairing unrelated replicates.

    net and population: six age bands ×161 CPS point/replicate estimates.
    gradient: six age bands ×J derivatives of total-dollar net balances.
    institutional_counts: six bands ×81 ACS point/replicate counts. This is an
    external cost allocation over CPS household residents, not a transition rate.
    """
    net, population, gradient, covariance, exposure = map(
        np.asarray, (net, population, gradient, covariance, exposure))
    if net.shape != (6, 161) or population.shape != net.shape:
        raise ValueError("Wrong CPS array dimensions")
    if gradient.ndim != 2 or gradient.shape[0] != 6:
        raise ValueError("Wrong medical gradient dimensions")
    if covariance.shape != (gradient.shape[1],) * 2 or exposure.shape != (6,):
        raise ValueError("Wrong covariance/exposure dimensions")
    if not all(np.isfinite(a).all() for a in (net, population, gradient, covariance, exposure)):
        raise ValueError("Nonfinite estimator inputs")
    if (population <= 0).any() or institution_price < 0:
        raise ValueError("Unsupported population or negative unit cost")
    inst = np.zeros((6, 81)) if institutional_counts is None else np.asarray(institutional_counts)
    if inst.shape != (6, 81) or not np.isfinite(inst).all() or (inst < 0).any():
        raise ValueError("Invalid ACS count arrays")
    costs = inst * institution_price
    cps = exposure @ ((net - costs[:, :1]) / population)
    med_gradient = (exposure[:, None] * gradient / population[:, :1]).sum(axis=0)
    acs = exposure @ ((net[:, :1] - costs) / population[:, :1])
    vc = sdr_variance(cps, 160)
    vm = float(med_gradient @ covariance @ med_gradient)
    va = sdr_variance(acs, 80)
    if vm < -1e-5:
        raise ValueError("Medical covariance produced negative variance")
    se = float(np.sqrt(vc + max(0.0, vm) + va))
    point = float(cps[0])
    return dict(estimate=point, se=se, ci95_low=point-Z*se, ci95_high=point+Z*se,
                variance_cps=vc, variance_meps=max(0.0, vm), variance_acs=va)


def support_ok(population, raw_n, ess, required=None):
    required = np.ones(6, bool) if required is None else np.asarray(required, bool)
    population, raw_n, ess = map(np.asarray, (population, raw_n, ess))
    return bool(np.isfinite(population[required]).all() and
                (population[required] > 0).all() and
                (raw_n[required] >= 30).all() and (ess[required] >= 20).all())


def health_scenarios(profiles, arrays, table, health_dir):
    """Replace the entire calibrated medical term, including its covariance.

    Use only full target coverage: a supported-domain mean cannot be subtracted
    from the whole-population ledger. No F scenario here: the alternate health
    export does not separately identify its covariance with the TRICARE offset.
    """
    data = pd.read_csv(health_dir / "estimates.csv", dtype={"band": str})
    health = np.load(health_dir / "medical_uncertainty.npz", allow_pickle=False)
    if data.row.tolist() != list(range(len(data))):
        raise ValueError("Medical row order differs from uncertainty-array order")
    rows, skipped = [], []
    for i, p in profiles.iterrows():
        if p.entry != "stock" or p.account != "expanded_excluding_N":
            continue
        net, pop = arrays["age_net_replicates"][i], arrays["age_population_replicates"][i]
        if not support_ok(pop, arrays["raw_n"][i], arrays["weight_ess"][i]):
            continue
        selected = data[(data.origin == p.origin) & (data.education == p.education)
                        & (data.outcome == "calibrated") & data.band.isin([str(b) for b in range(6)])]
        base = selected[selected.model == "canonical"].sort_values("band")
        if base.band.tolist() != [str(b) for b in range(6)]:
            raise ValueError("Canonical medical age rows missing")
        if not np.allclose(base.target_population, pop[:, 0], rtol=1e-10, atol=.01):
            raise ValueError("Health and annual target populations differ")
        old_medical = arrays["age_medical_gradients"][i] @ arrays["donor_means"].ravel() / pop[:, 0]
        if not np.allclose(old_medical, -base.dollars_per_person, rtol=1e-10, atol=1e-7):
            raise ValueError("Medical replacement does not reconstruct annual medical term")
        base_pp = health["cps_per_person_replicates"][base.row]
        for model in ["adult_age_birth", "education", "insurance"]:
            alt = selected[selected.model == model].sort_values("band")
            if alt.band.tolist() != [str(b) for b in range(6)] or not np.allclose(alt.supported_target_fraction, 1, rtol=0, atol=1e-12):
                skipped.append(dict(**p.to_dict(), model=model, reason="Medical donor model does not cover every target age cell"))
                continue
            if not np.allclose(alt.population, pop[:, 0], rtol=1e-10, atol=.01):
                raise ValueError("Alternate medical denominator mismatch")
            new_pp = net / pop + base_pp - health["cps_per_person_replicates"][alt.row]
            # Those are gradients of means, so unit denominators below are intentional.
            new_gradient = -health["point_gradients"][alt.row]
            for rate in [0., .02, .03, .05]:
                for horizon in [85, 100]:
                    w, dw = survival_weights(table, rate, horizon)
                    result = conditional_estimate(new_pp, np.ones_like(pop), new_gradient, health["covariance"], w)
                    baseline = float(w @ (net[:, 0] / pop[:, 0]))
                    rows.append(dict(**p.to_dict(), medical_model=model, start_age=25, last_age=horizon,
                                     real_rate=rate, F_percapita=0, institution_price=0, **result,
                                     difference_from_canonical= result["estimate"]-baseline,
                                     signed_omitted_net_receipts_to_zero=-result["estimate"],
                                     constant_annual_net_receipts_to_zero=-result["estimate"]/w.sum(),
                                     local_change_per_percentage_point=float(dw @ new_pp[:, 0])*.01))
    return pd.DataFrame(rows), pd.DataFrame(skipped)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--annual-dir", type=Path)
    parser.add_argument("--institutions-dir", type=Path)
    parser.add_argument("--health-dir", type=Path)
    parser.add_argument("--out-dir", type=Path, default=HERE / "derived")
    args = parser.parse_args()
    root = args.root.resolve()
    annual = args.annual_dir or root / "infra/immigration-fiscal/education_origin_fiscal_2026_09_19/derived"
    institutions = args.institutions_dir or root / "infra/immigration-fiscal/institutional_education_2026_09_19/derived"
    health_dir = args.health_dir or root / "infra/immigration-fiscal/health_transport_sensitivity_2026_09_19/derived"
    profiles_path = annual / "profiles.csv"
    arrays_path = annual / "uncertainty.npz"
    verify_releases(annual, institutions, root)
    verify_health_release(health_dir)
    profiles = pd.read_csv(profiles_path)
    if profiles.profile_id.tolist() != list(range(len(profiles))):
        raise ValueError("Profile rows must match NPZ row order exactly")
    arrays = np.load(arrays_path, allow_pickle=False)
    institution_profiles = pd.read_csv(institutions / "domains.csv")
    institution_arrays = np.load(institutions / "counts.npz", allow_pickle=False)
    inst_lookup = {(r.origin, r.education): i for i, r in institution_profiles.iterrows()}
    life_path = root / "infra/immigration-fiscal/ledger_absolute_2026_09_17/lifetime.py"
    spec = importlib.util.spec_from_file_location("canonical_period", life_path)
    life = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(life)
    table = life.read_life_table(root, "total")
    cov = arrays["medical_covariance"]
    rows, skipped = [], []
    for i, profile in profiles.iterrows():
        key = profile.to_dict()
        if profile.entry != "stock" or profile.account != "expanded_excluding_N":
            continue
        net = arrays["age_net_replicates"][i]
        pop = arrays["age_population_replicates"][i]
        grad = arrays["age_medical_gradients"][i]
        if not support_ok(pop, arrays["raw_n"][i], arrays["weight_ess"][i]):
            skipped.append(dict(**key, reason="At least one required age band fails n30/ESS20/positive-replicates rule"))
            continue
        # ACS does not identify parental nativity: no silent proxy for G3+ whites.
        inst_idx = inst_lookup.get((profile.origin, profile.education))
        prices = [0.0, 50000.0, 100000.0, 150000.0] if inst_idx is not None else [0.0]
        inst = None if inst_idx is None else institution_arrays["institutional_population"][inst_idx]
        inst_n = None if inst_idx is None else institution_arrays["institutional_population_n"][inst_idx]
        for f in [0, 1]:
            fnet = net + f * arrays["age_F_replicates"][i]
            fgrad = grad + f * arrays["age_F_medical_gradients"][i]
            for rate in [0.0, 0.02, 0.03, 0.05]:
                for horizon in [85, 100]:
                    weights, derivatives = survival_weights(table, rate, horizon)
                    for price in prices:
                        result = conditional_estimate(fnet, pop, fgrad, cov, weights, inst, price)
                        point_inst = np.zeros(6) if inst is None else inst[:, 0] * price
                        derivative = float(derivatives @ ((fnet[:, 0] - point_inst) / pop[:, 0]))
                        annual_equiv = result["estimate"] / weights.sum()
                        rows.append(dict(**key, start_age=25, last_age=horizon, real_rate=rate,
                                         F_percapita=f, institution_price=price,
                                         institution_min_raw_n=int(inst_n.min()) if inst_n is not None else np.nan,
                                         institution_sparse_age_bands=int((inst_n < 30).sum()) if inst_n is not None else np.nan,
                                         institution_zero_record_age_bands=int((inst_n == 0).sum()) if inst_n is not None else np.nan,
                                         institution_sparse_bands="|".join(str(b) for b in np.flatnonzero(inst_n < 30)) if inst_n is not None else "",
                                         institution_zero_record_bands="|".join(str(b) for b in np.flatnonzero(inst_n == 0)) if inst_n is not None else "",
                                         institution_sampling_caution=bool(price > 0 and inst_n is not None and (inst_n < 30).any()),
                                         institution_scope="ACS stock costs / CPS household population" if inst_idx is not None else "unavailable; no ACS parental nativity",
                                         **result, survival_annuity=float(weights.sum()),
                                         annual_equivalent=annual_equiv,
                                         signed_omitted_net_receipts_to_zero=-result["estimate"],
                                         nonnegative_extra_receipts_to_zero=max(0, -result["estimate"]),
                                         constant_annual_net_receipts_to_zero=-annual_equiv,
                                         derivative_per_rate_unit=derivative,
                                         local_change_per_percentage_point=derivative*0.01))
    if not rows:
        raise ValueError("No supported stock period profiles")
    out = args.out_dir
    out.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(rows).to_csv(out / "period_profiles.csv", index=False)
    pd.DataFrame(skipped).to_csv(out / "withheld_profiles.csv", index=False)
    health_period, health_skipped = health_scenarios(profiles, arrays, table, health_dir)
    health_period.to_csv(out / "health_period_profiles.csv", index=False)
    health_skipped.to_csv(out / "withheld_health_profiles.csv", index=False)
    inputs = [annual / "manifest.json", profiles_path, arrays_path, institutions / "audit.json", institutions / "domains.csv", institutions / "counts.npz",
              health_dir / "audit.json", health_dir / "estimates.csv", health_dir / "medical_uncertainty.npz",
              life_path, root / life.LIFE_LANE / "_cache/lt2024_Table01.xlsx", Path(__file__)]
    audit = dict(schema="education-period-uncertainty-v1", price_year=2024,
                 inputs=[fingerprint(p) for p in inputs], rows=len(rows), withheld=len(skipped),
                 health_rows=len(health_period), health_withheld=len(health_skipped),
                 interpretation="Current resident adult period profiles, not entry cohorts or admission effects. No descendants, real growth, future policy, emigration or education transitions.",
                 uncertainty="First-order independent CPS/MEPS/ACS sampling errors conditional on transport, survival, calibration controls and cost assumptions; not predictive intervals or causal uncertainty.",
                 support="Every required age band n>=30 and Kish weight ESS>=20 and positive denominator in every replicate. Reporting rule, not a theorem or calibrated coverage guarantee.",
                 institution_prices="0/50k/100k/150k are uncalibrated common public unit-cost assumptions in 2024 dollars, not estimated costs or empirical bounds.",
                 sparse_institutions="Raw institutional n<30 and zero-record age cells are carried into every output. Normal design intervals may be unreliable there; a zero sample count is not proof of zero population. Raw GQ records can include whole-person imputations.",
                 break_even="Omitted net fiscal receipts needed to make this account zero. No measured nonfiscal benefit or total incumbent welfare claim.")
    audit["outputs"] = [fingerprint(out / name) for name in ["period_profiles.csv", "withheld_profiles.csv", "health_period_profiles.csv", "withheld_health_profiles.csv"]]
    (out / "audit.json").write_text(json.dumps(audit, indent=2) + "\n")
    print(json.dumps({"rows": len(rows), "withheld": len(skipped), "output": str(out)}))


if __name__ == "__main__":
    main()
