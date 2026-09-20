"""Adult skills among BA holders in two separately analyzed US PIAAC releases.

Primary: ages 25-65, US-born respondent and both US-born parents/guardians,
Hispanic versus non-Hispanic white, BA or higher. Sensitivities: BA-only and
descriptive weighted adjustment for five-year age bands and sex. No data pooling.
"""

import sys as _path_sys
from pathlib import Path as _Path
_path_sys.path.insert(0, str(_Path(__file__).resolve().parents[1] / "build"))
import paths as _data_paths


import argparse
import hashlib
import json
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import norm, t


LANE = Path(__file__).resolve().parent
DATA = _data_paths.reused_surveys_root(require_exists=False)
SOURCES = {
    "2012_14": DATA / "docs/2016667REV_HHPUF.zip",
    "2017": DATA / "piaac/prgusap1_2017.csv",
}
PV_NAMES = {d: [f"PV{prefix}{i}" for i in range(1, 11)] for d, prefix in [("literacy", "LIT"), ("numeracy", "NUM")]}
WEIGHTS = [f"SPFWT{i}" for i in range(46)]
FACTORS = ["EDCAT8", "J_Q04A", "J_Q06A", "J_Q07A", "RACETHN_5CAT", "AGEG5LFSEXT", "GENDER_R"]
BENCHMARKS = {
    "2012_14": {"literacy": (271, 1.0), "numeracy": (258, 1.2)},
    "2017": {"literacy": (271, 1.3), "numeracy": (255, 1.4)},
}


def load_release(wave, path):
    keep = FACTORS + WEIGHTS + sum(PV_NAMES.values(), []) + ["VEMETHOD", "VENREPS", "VEFAYFAC"]
    if wave == "2012_14":
        with zipfile.ZipFile(path) as archive:
            with archive.open("SAS/prgushp1_puf.sas7bdat") as source:
                d = pd.read_sas(source, format="sas7bdat", encoding="utf-8")
        d.columns = d.columns.str.upper()
        d = d[keep].copy()
    else:
        d = pd.read_csv(path, sep="|", usecols=keep, low_memory=False)
    expected_n = 8670 if wave == "2012_14" else 3660
    assert len(d) == expected_n
    assert set(d.VEMETHOD.unique()) == {"JK2"}
    for col in [c for c in keep if c != "VEMETHOD"]:
        d[col] = pd.to_numeric(d[col], errors="coerce")
    assert d.VENREPS.eq(45).all() and d.VEFAYFAC.eq(0).all()
    weights = d[WEIGHTS].to_numpy(float)
    assert np.isfinite(weights).all() and (weights >= 0).all()
    assert (weights[:, 0] > 0).all()
    for names in PV_NAMES.values():
        values = d[names].to_numpy(float)
        assert ((~np.isfinite(values)) | ((values >= 0) & (values <= 500))).all()
        complete = np.isfinite(values).all(axis=1)
        empty = (~np.isfinite(values)).all(axis=1)
        assert (complete | empty).all(), "Partially missing PV vectors need explicit treatment"
    return d


def summarize(estimates):
    """46 weight estimates x 10 PVs; JK2 factor 1 and Rubin PV variance."""
    assert estimates.shape == (46, 10) and np.isfinite(estimates).all()
    full = estimates[0]
    sampling_by_pv = ((estimates[1:] - full) ** 2).sum(axis=0)
    sampling_var = float(sampling_by_pv.mean())
    pv_var = float(1.1 * full.var(ddof=1))
    mean = float(full.mean())
    se = (sampling_var + pv_var) ** 0.5
    return {
        "estimate": mean, "se": se,
        "sampling_variance": sampling_var,
        "plausible_value_variance": pv_var,
        "low95_normal": mean - norm.ppf(.975) * se,
        "high95_normal": mean + norm.ppf(.975) * se,
        "low95_t45": mean - t.ppf(.975, 45) * se,
        "high95_t45": mean + t.ppf(.975, 45) * se,
    }


def estimates_for_mean(d, mask, domain):
    valid = mask & d[PV_NAMES[domain]].notna().all(axis=1)
    values = d.loc[valid, PV_NAMES[domain]].to_numpy(float)
    weights = d.loc[valid, WEIGHTS].to_numpy(float)
    totals = weights.sum(axis=0)
    assert (totals > 0).all(), "Empty full/replicate domain: cannot estimate"
    estimates = (weights.T @ values) / totals[:, None]
    fullw = weights[:, 0]
    stats = {
        "eligible_n": int(mask.sum()), "scored_n": int(valid.sum()),
        "missing_scores_n": int((mask & ~valid).sum()),
        "kish_n": float(fullw.sum() ** 2 / (fullw**2).sum()),
        "max_weight_share": float(fullw.max() / fullw.sum()),
        "weight_sum": float(fullw.sum()),
    }
    return estimates, stats


def adjusted_gap(d, mask, domain):
    valid = mask & d[PV_NAMES[domain]].notna().all(axis=1) & d.GENDER_R.isin([1, 2])
    sub = d.loc[valid]
    design = np.column_stack([
        np.ones(len(sub)), sub.RACETHN_5CAT.eq(1).to_numpy(float),
        sub.GENDER_R.eq(2).to_numpy(float),
        *[sub.AGEG5LFSEXT.eq(k).to_numpy(float) for k in range(4, 11)],
    ])
    values = sub[PV_NAMES[domain]].to_numpy(float)
    weights = sub[WEIGHTS].to_numpy(float)
    estimates = np.empty((46, 10))
    max_condition = 0.0
    for r in range(46):
        cross = design.T @ (design * weights[:, r, None])
        assert np.linalg.matrix_rank(cross) == design.shape[1], "Adjustment lost rank in a replicate"
        max_condition = max(max_condition, float(np.linalg.cond(cross)))
        coefficients = np.linalg.solve(cross, design.T @ (values * weights[:, r, None]))
        estimates[r] = coefficients[1]
    return estimates, {
        "scored_n": len(sub),
        "hispanic_n": int(sub.RACETHN_5CAT.eq(1).sum()),
        "white_n": int(sub.RACETHN_5CAT.eq(2).sum()),
        "missing_sex_n": int((mask & ~d.GENDER_R.isin([1, 2])).sum()),
        "max_design_condition_number": max_condition,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, default=LANE / "derived/piaac")
    args = parser.parse_args()
    out = args.output_dir
    out.mkdir(parents=True, exist_ok=True)
    means, contrasts, composition, benchmark_rows, details = [], [], [], [], []
    audit = {"sources": {}, "benchmark_checks": [], "definition": __doc__}
    components = {}
    for wave, path in SOURCES.items():
        d = load_release(wave, path)
        d.to_csv(out / f"{wave}_source_extract.csv", index_label="source_row")
        audit["sources"][wave] = {
            "path": str(path), "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
            "n": len(d), "method": "JK2", "replicates": 45, "PVs": 10,
        }
        age = d.AGEG5LFSEXT.between(3, 10)
        native = d[["J_Q04A", "J_Q06A", "J_Q07A"]].eq(1).all(axis=1)
        race = d.RACETHN_5CAT.isin([1, 2])
        for domain in PV_NAMES:
            est, support = estimates_for_mean(d, age, domain)
            result = summarize(est)
            target_mean, target_se = BENCHMARKS[wave][domain]
            # Published table rounds means to integer, SEs to one decimal.
            matched = abs(result["estimate"] - target_mean) <= .51 and abs(result["se"] - target_se) <= .051
            benchmark_rows.append({"wave": wave, "domain": domain, "age": "25_65", **support, **result, "published_mean": target_mean, "published_se": target_se, "rounded_match": matched})
            audit["benchmark_checks"].append({"wave": wave, "domain": domain, "rounded_match": matched})
            components[f"{wave}|benchmark|{domain}"] = est.tolist()
            assert matched, f"{wave} {domain}: official benchmark failed before subgroup estimation"
        for credential, degree in [("BAplus", d.EDCAT8.isin([6, 7, 8])), ("BA_only", d.EDCAT8.eq(6))]:
            sample = age & native & race & degree
            expected_h = {("2012_14", "BAplus"): 32, ("2012_14", "BA_only"): 21, ("2017", "BAplus"): 28, ("2017", "BA_only"): 22}[(wave, credential)]
            assert int((sample & d.RACETHN_5CAT.eq(1)).sum()) == expected_h
            for group, code in [("Hispanic", 1), ("NH_white", 2)]:
                mask = sample & d.RACETHN_5CAT.eq(code)
                weights = d.loc[mask, "SPFWT0"]
                for variable, categories in [("AGEG5LFSEXT", range(3, 11)), ("GENDER_R", [1, 2]), ("EDCAT8", [6, 7, 8])]:
                    for category in categories:
                        member = d.loc[mask, variable].eq(category)
                        composition.append({"wave": wave, "credential": credential, "group": group, "variable": variable, "category": category, "n": int(member.sum()), "weighted_share": float(weights[member].sum() / weights.sum())})
            for domain in PV_NAMES:
                by_group = {}
                for group, code in [("Hispanic", 1), ("NH_white", 2)]:
                    est, support = estimates_for_mean(d, sample & d.RACETHN_5CAT.eq(code), domain)
                    by_group[group] = est
                    means.append({"wave": wave, "credential": credential, "domain": domain, "group": group, **support, **summarize(est)})
                    components[f"{wave}|{credential}|{domain}|{group}"] = est.tolist()
                delta = by_group["Hispanic"] - by_group["NH_white"]
                contrasts.append({"wave": wave, "credential": credential, "domain": domain, "adjustment": "none", **summarize(delta)})
                components[f"{wave}|{credential}|{domain}|difference"] = delta.tolist()
                adjusted, counts = adjusted_gap(d, sample, domain)
                contrasts.append({"wave": wave, "credential": credential, "domain": domain, "adjustment": "five_year_age_band_and_sex", **summarize(adjusted)})
                details.append({"wave": wave, "credential": credential, "domain": domain, **counts})
                components[f"{wave}|{credential}|{domain}|adjusted"] = adjusted.tolist()
    for name, rows in [("means", means), ("contrasts", contrasts), ("composition", composition), ("benchmarks", benchmark_rows), ("adjustment_support", details)]:
        pd.DataFrame(rows).to_csv(out / f"{name}.csv", index=False)
    (out / "replicate_pv_estimates.json").write_text(json.dumps(components) + "\n")
    audit["intervals"] = "Reported intervals use the approximate pointwise normal convention, without multiple-outcome adjustment. Exact small-domain PV-adjusted degrees of freedom are unresolved; t45 columns are only an illustrative widening, not verified NCES finite-sample intervals."
    audit["adjustment"] = "Weighted linear projection of score on Hispanic indicator, female indicator and seven age-band indicators; recomputed for all 46 weights and 10 PVs. Descriptive, not causal."
    (out / "audit.json").write_text(json.dumps(audit, indent=2) + "\n")
    print("National published-benchmark checks:")
    print(pd.DataFrame(benchmark_rows)[["wave", "domain", "scored_n", "estimate", "se", "rounded_match"]].to_string(index=False))
    assert all(r["rounded_match"] for r in audit["benchmark_checks"]), "Official benchmark mismatch: do not interpret subgroup outputs before resolution"
    print("Subgroup contrasts (Hispanic minus non-Hispanic white, score points):")
    print(pd.DataFrame(contrasts)[["wave", "credential", "domain", "adjustment", "estimate", "se", "low95_normal", "high95_normal"]].to_string(index=False))


if __name__ == "__main__":
    main()
