"""Check the bridge against independent full-dummy WLS and 2SLS estimators."""
import json
from importlib.metadata import version

import numpy as np
import pandas as pd
import statsmodels.api as sm
from linearmodels.iv import IV2SLS

from modern_bridge import CONTROLS, OUT, fit, prep, pull


def main():
    panel = prep.load()
    valid = prep.valid(panel, "value")
    d = valid[valid.sw_sample == 1].copy()
    controls = prep.standardize(d, CONTROLS)
    fe = pd.get_dummies(d.cbsa_period, dtype=float)
    x = pd.concat([d[["d_fb_share"]], controls, fe], axis=1)
    independent = sm.WLS(d.dlog_value, x, weights=d._w).fit(
        cov_type="cluster", cov_kwds={"groups": d.cbsa})
    native = fit(d, "verification_wls")
    np.testing.assert_allclose(native["coef"], independent.params.d_fb_share, atol=1e-10)
    np.testing.assert_allclose(native["se"], independent.bse.d_fb_share, atol=1e-10)
    checks = {"full_dummy_WLS_coefficient_and_SE": True}

    pa = panel[panel.period == "A"]
    geo = ["lat_0", "lon_0", "fb_share_0", "aland_sqmi_0"]
    neighbors = pa[np.isfinite(pa[geo]).all(axis=1)]
    d = d[d.period == "A"].copy()
    d["pull"] = pull(neighbors, 1.6).reindex(d.index)
    d["pull_lag"] = d.pull * d.fb_share_0
    d["pull_msa"] = d.pull * d.msa_imm_pc
    extra = CONTROLS + ["fb_share_0"]
    iv = ["pull", "pull_lag", "pull_msa"]
    z = prep.standardize(d, extra + iv)
    exog = pd.concat([z[extra], pd.get_dummies(d.cbsa_period, dtype=float)], axis=1)
    independent = IV2SLS(d.dlog_value, exog, d[["d_fb_share"]], z[iv], weights=d._w).fit(
        cov_type="clustered", clusters=d.cbsa, debiased=True)
    native = fit(d, "verification_iv", iv=iv, extra=["fb_share_0"])
    np.testing.assert_allclose(native["coef"], independent.params.d_fb_share, atol=1e-9)
    np.testing.assert_allclose(native["se"], independent.std_errors.d_fb_share, atol=1e-9)
    first = sm.WLS(d.d_fb_share, pd.concat([z[iv], exog], axis=1), weights=d._w).fit(
        cov_type="cluster", cov_kwds={"groups": d.cbsa})
    restriction = np.zeros((3, len(first.params)))
    restriction[:, :3] = np.eye(3)
    independent_f = float(first.f_test(restriction).fvalue)
    np.testing.assert_allclose(native["F_first"], independent_f, atol=1e-8)
    checks.update(full_dummy_2SLS_coefficient_and_SE=True,
                  full_dummy_excluded_instrument_F=True,
                  original_paper_reproduction=False,
                  packages={name: version(name) for name in ["statsmodels", "linearmodels"]})
    (OUT / "verification.json").write_text(json.dumps(checks, indent=2) + "\n")
    print(json.dumps(checks, indent=2))


if __name__ == "__main__":
    main()
