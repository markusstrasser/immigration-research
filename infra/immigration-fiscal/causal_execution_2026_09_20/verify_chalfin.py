"""Independent full-matrix checks of the residualized Chalfin IV replay."""
import argparse
import hashlib
import json
import math
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.linalg import qr


def require(condition, message):
    if not condition:
        raise ValueError(message)


def main():
    root = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data", type=Path, default=root / "raw/chalfin/data/chalfin_data.dta")
    parser.add_argument("--results", type=Path, required=True)
    args = parser.parse_args()
    data_hash = hashlib.sha256(args.data.read_bytes()).hexdigest()
    require(data_hash == "d41b4882f615cfe8063f16ee6dcd0e26f3cf43873f661529234518174d1b567d", "Wrong source snapshot")
    frame = pd.read_stata(args.data).sort_values(["FMSA", "year"])
    reported = json.loads(args.results.read_text())
    require(len(frame) == 276 and not frame.duplicated(["FMSA", "year"]).any(), "Panel identity failure")
    require(len(reported["baseline"]) == 7, "Missing baseline endpoints")
    expected = {"dlogpc_" + c for c in ["murder", "rape", "robbery", "assault", "burglary", "larceny", "motor"]}
    require({r["outcome"] for r in reported["baseline"]} == expected, "Duplicate or unexpected endpoints")
    require(reported["sha256"] == data_hash, "Result provenance mismatch")
    covariates = [c for c in frame if c.startswith(("deduc", "dage", "grp_"))]
    covariates += ["dblack", "demployed", "dusbirths", "dfbnonmex", "dushisp"]
    checks = []
    for row in reported["baseline"]:
        outcome = row["outcome"]
        sample = frame.dropna(subset=[outcome, "dmexfb_alt", "dins", "popweight", "FMSA"] + covariates)
        weight = np.sqrt(sample.popweight.to_numpy(float))
        controls = np.column_stack([np.ones(len(sample)), sample[covariates].to_numpy(float)]) * weight[:, None]
        orthogonal, _, _ = qr(controls, mode="economic", pivoting=True)
        rank = np.linalg.matrix_rank(controls)
        controls = orthogonal[:, :rank]
        x = np.column_stack([sample.dmexfb_alt.to_numpy(float) * weight, controls])
        z = np.column_stack([sample.dins.to_numpy(float) * weight, controls])
        y = sample[outcome].to_numpy(float) * weight
        bread = np.linalg.inv(z.T @ x)
        beta = bread @ z.T @ y
        error = y - x @ beta
        scores = np.vstack([(z[sample.FMSA.to_numpy() == g] * error[sample.FMSA.to_numpy() == g, None]).sum(axis=0)
                            for g in sample.FMSA.unique()])
        variance = bread @ (scores.T @ scores) @ bread.T
        se = np.sqrt(variance[0, 0])
        require(len(sample) == row["n"], f"Sample mismatch: {outcome}")
        require(np.isclose(beta[0], row["beta"], rtol=1e-7, atol=1e-8), f"Coefficient mismatch: {outcome}: {beta[0]} != {row['beta']}")
        require(np.isclose(se, row["se_cr0"], rtol=1e-7, atol=1e-8), f"Covariance mismatch: {outcome}: {se} != {row['se_cr0']}")
        expected_z = float(beta[0] / se)
        expected_ci = [float(beta[0] - 1.959963984540054 * se), float(beta[0] + 1.959963984540054 * se)]
        require(np.allclose(row["ci95"], expected_ci, rtol=1e-6, atol=1e-7), f"Wald interval mismatch: {outcome}")
        require(np.isclose(row["z"], expected_z, rtol=1e-6, atol=1e-7), f"Wald statistic mismatch: {outcome}")
        expected_p = math.erfc(abs(expected_z) / math.sqrt(2))
        require(np.isclose(row["p_normal"], expected_p, rtol=1e-6, atol=1e-7), f"Wald p-value mismatch: {outcome}")
        # Independently evaluate full OLS regressions at AR set boundaries and
        # fixed probes. No residualized replay helper is imported.
        z_bread = np.linalg.inv(z.T @ z)
        intervals = row["ar95"]["intervals"]
        topology = {
            "empty": intervals == [],
            "all_real": intervals == [[None, None]],
            "bounded": len(intervals) == 1 and all(v is not None and math.isfinite(v) for v in intervals[0]) and intervals[0][0] <= intervals[0][1],
            "half_line": len(intervals) == 1 and sum(v is None for v in intervals[0]) == 1,
            "disjoint_unbounded": len(intervals) == 2 and intervals[0][0] is None and intervals[1][1] is None and intervals[0][1] is not None and intervals[1][0] is not None and intervals[0][1] <= intervals[1][0],
        }
        require(topology.get(row["ar95"]["kind"], False), f"AR topology mismatch: {outcome}")
        probes = [-1.0, 0.0, 1.0, float(beta[0])]
        boundaries = [b for pair in intervals for b in pair if b is not None]
        for candidate in probes + boundaries:
            null_y = y - candidate * x[:, 0]
            null_beta = z_bread @ z.T @ null_y
            null_error = null_y - z @ null_beta
            null_scores = np.vstack([(z[sample.FMSA.to_numpy() == g] * null_error[sample.FMSA.to_numpy() == g, None]).sum(axis=0)
                                     for g in sample.FMSA.unique()])
            null_variance = z_bread @ (null_scores.T @ null_scores) @ z_bread.T
            statistic = float(null_beta[0] ** 2 / null_variance[0, 0])
            if candidate in boundaries:
                require(abs(statistic - 3.841458820694124) < 1e-5, f"AR boundary mismatch: {outcome}")
            else:
                inside = any((lo is None or candidate >= lo) and (hi is None or candidate <= hi) for lo, hi in intervals)
                require(inside == (statistic <= 3.841458820694124), f"AR membership mismatch: {outcome}")
        crime = outcome.removeprefix("dlogpc_")
        levels = frame[crime].where(frame[crime] > 0)
        count_difference = np.log(levels).groupby(frame.FMSA).diff()
        mask = frame[outcome].notna()
        require(count_difference[mask].notna().all(), f"Count identity coverage: {crime}")
        count_error = float((count_difference[mask] - frame.loc[mask, outcome]).abs().max())
        require(count_error < 2e-6, f"Count identity mismatch: {crime}")
        rate_difference = frame.groupby("FMSA")["logpc_" + crime].diff()
        rate_error = float((rate_difference[mask] - frame.loc[mask, outcome]).abs().max())
        checks.append({"outcome": outcome, "n": len(sample), "beta": float(beta[0]), "se_cr0": float(se),
                       "count_identity_n": int(mask.sum()), "count_identity_max_error": count_error,
                       "rate_identity_max_error": rate_error})
    exposure = 100 * frame.groupby("FMSA").mexfba.diff()
    mask = frame.dmexfb_alt.notna()
    exposure_error = float((exposure[mask] - frame.loc[mask, "dmexfb_alt"]).abs().max())
    require(exposure[mask].notna().all() and exposure_error < 2e-6, "Exposure identity mismatch")
    print(json.dumps({"status": "PASS", "scope": "Seven baseline endpoints and source identities; sensitivity blocks executed separately, not independently certified here",
                      "method": "Full-matrix just-identified weighted IV; independent pivoted QR controls; cluster CR0",
                      "source_sha256": data_hash, "endpoints": checks,
                      "exposure_identity": "dmexfb_alt = 100 * within-MSA change in mexfba",
                      "exposure_identity_n": int(mask.sum()), "exposure_max_error": exposure_error}, indent=2))


if __name__ == "__main__":
    main()
