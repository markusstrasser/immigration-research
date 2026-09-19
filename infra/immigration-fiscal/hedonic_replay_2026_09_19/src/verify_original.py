"""Independent full-dummy WLS/2SLS verification and two-step Hansen J."""
import json
from importlib.metadata import version

import numpy as np
import pandas as pd
import statsmodels.api as sm
from linearmodels.iv import IV2SLS, IVGMM
from scipy.stats import chi2

from original_replay import LANE, OUT, design, first_stage, fit, load, sample, specs


def manual_hansen(d, x, z, y, weights, beta_iv):
    """Full instrument moments, including FE, with weight from 2SLS residuals.

    Baum/Schaffer/Stillman (2003), section 4.3: ivreg2's robust J uses
    feasible efficient two-step GMM even when point estimation is 2SLS.
    """
    rw = np.sqrt(weights.to_numpy())
    x, z, y = x.to_numpy() * rw[:, None], z.to_numpy() * rw[:, None], y.to_numpy() * rw
    residual = y - x @ beta_iv.to_numpy()
    scores = pd.DataFrame(z * residual[:, None]).groupby(d.tract.to_numpy()).sum().to_numpy()
    moment_cov = scores.T @ scores
    zx = z.T @ x
    zy = z.T @ y
    beta_gmm = np.linalg.solve(zx.T @ np.linalg.solve(moment_cov, zx),
                               zx.T @ np.linalg.solve(moment_cov, zy))
    moments = z.T @ (y - x @ beta_gmm)
    return float(moments @ np.linalg.solve(moment_cov, moments))


def main():
    d, controls = load()
    rows = []
    for arm, c, z, required in specs(controls):
        ds = sample(d, c, iv=z, require=required)
        standardized, _, weights = design(ds, c, iv=z)
        exog = pd.concat([standardized[c], pd.get_dummies(ds.msayear, dtype=float)], axis=1)
        native = fit(ds, arm, c, iv=z)
        if z:
            model = IV2SLS(ds.dloval, exog, ds[["dforeigncap"]], standardized[z], weights=weights)
            independent = model.fit(cov_type="clustered", clusters=ds.tract,
                                    debiased=arm not in {"table1_col5", "table1_col6"})
            se = independent.std_errors.dforeigncap
        else:
            x = pd.concat([ds[["dforeigncap"]], exog], axis=1)
            independent = sm.WLS(ds.dloval, x, weights=weights).fit(
                cov_type="cluster", cov_kwds={"groups": ds.tract})
            se = independent.bse.dforeigncap
        np.testing.assert_allclose(native["coef"], independent.params.dforeigncap, atol=1e-9, rtol=1e-9)
        np.testing.assert_allclose(native["se"], se, atol=1e-9, rtol=1e-9)
        np.testing.assert_allclose(native["r2_overall"], independent.rsquared, atol=1e-9, rtol=1e-9)
        row = dict(arm=arm, n=len(ds), coef=float(independent.params.dforeigncap),
                   se=float(se), full_dummy_coefficient_SE_R2_agree=True)
        if z:
            first = sm.WLS(ds.dforeigncap, pd.concat([standardized[z], exog], axis=1), weights=weights).fit(
                cov_type="cluster", cov_kwds={"groups": ds.tract})
            restriction = np.zeros((len(z), len(first.params)))
            restriction[:, :len(z)] = np.eye(len(z))
            independent_f = float(first.f_test(restriction).fvalue)
            np.testing.assert_allclose(native["F_first"], independent_f, atol=1e-6, rtol=1e-8)
            row.update(first_stage_F=independent_f, first_stage_F_agrees=True)
            if len(z) > 1:
                gmm = IVGMM(ds.dloval, exog, ds[["dforeigncap"]], standardized[z], weights=weights,
                            weight_type="clustered", clusters=ds.tract).fit(iter_limit=2)
                x = pd.concat([exog, ds[["dforeigncap"]]], axis=1)
                instruments = pd.concat([exog, standardized[z]], axis=1)
                manual_j = manual_hansen(ds, x, instruments, ds.dloval, weights, independent.params)
                np.testing.assert_allclose(manual_j, gmm.j_stat.stat, atol=1e-7, rtol=1e-7)
                row.update(hansen_J=manual_j, hansen_df=len(z) - 1,
                           hansen_p=float(chi2.sf(manual_j, len(z) - 1)),
                           full_dummy_two_step_GMM_J_agrees=True)
        rows.append(row)
        print(json.dumps(row), flush=True)
    # Guard the meaningful source discrepancies, rather than force table N/F to pass.
    assert rows[0]["n"] == 34835 and rows[1]["n"] == 34833 and rows[2]["n"] == 30947
    assert abs(rows[3]["first_stage_F"] - 76.01) > 40
    assert abs(rows[4]["first_stage_F"] - 362.23) < .005
    assert abs(rows[5]["first_stage_F"] - 337.632) < .0005
    assert abs(rows[4]["hansen_p"] - .95) < .005
    assert abs(rows[5]["hansen_p"] - .80) < .005
    targets = json.loads((LANE / "table1_targets.json").read_text())["columns"]
    for actual, target in zip(rows, targets, strict=True):
        assert abs(actual["coef"] - target["coef"]) <= .0005
        assert abs(actual["se"] - target["se"]) <= .0005
    appendix = first_stage(d, controls, ["pull"], "appendix_table3_col1")
    assert appendix[0]["n"] == 35120
    # Outcome-only comparison: identical rows, fixed matrix, and weighting.
    common = sample(sample(d, controls), controls, outcome="dlomval")
    for outcome in ["dloval", "dlomval"]:
        standardized, _, weights = design(common, controls, outcome=outcome)
        x = pd.concat([common[["dforeigncap"]], standardized[controls],
                       pd.get_dummies(common.msayear, dtype=float)], axis=1)
        independent = sm.WLS(common[outcome], x, weights=weights).fit(
            cov_type="cluster", cov_kwds={"groups": common.tract})
        native = fit(common, outcome, controls, outcome=outcome)
        np.testing.assert_allclose(native["coef"], independent.params.dforeigncap, atol=1e-9)
        np.testing.assert_allclose(native["se"], independent.bse.dforeigncap, atol=1e-9)
    output = dict(table1=rows, matched_mean_median_verified=True,
                  packages={p: version(p) for p in ["statsmodels", "linearmodels"]})
    (OUT / "original_verification.json").write_text(json.dumps(output, indent=2) + "\n")


if __name__ == "__main__":
    main()
