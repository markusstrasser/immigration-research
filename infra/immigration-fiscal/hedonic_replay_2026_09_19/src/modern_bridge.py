"""One-factor diagnostics of the cached modern exercise; not an old-data replay."""
from pathlib import Path
import hashlib
from importlib.metadata import version
import json
import sys

import numpy as np
import pandas as pd

LANE = Path(__file__).resolve().parents[1]
MODERN = LANE.parent / "hedonic_composition_2026_09_19"
sys.path.insert(0, str(MODERN / "src"))
import estim
import prep

CONTROLS = prep.QUAL_D + prep.LEV0
OUT = LANE / "derived"


def digest(d, columns):
    return hashlib.sha256(d[columns].to_csv(index=False, float_format="%.17g").encode()).hexdigest()


def fit(d, arm, cluster="cbsa", iv=None, extra=None):
    controls = CONTROLS + (extra or [])
    cols = list(dict.fromkeys(["dlog_value", "d_fb_share"] + controls + (iv or [])))
    assert np.isfinite(d[cols + ["_w"]].to_numpy(float)).all(), arm
    assert (d._w > 0).all() and d[cluster].nunique() >= 5, arm
    x = prep.standardize(d, controls + (iv or []))
    x["dlog_value"], x["d_fb_share"] = d.dlog_value, d.d_fb_share
    dm = estim.wdemean(x, cols, d.cbsa_period, d._w)
    kwargs = {"k_absorbed": d.cbsa_period.nunique()}
    if iv:
        result = estim.tsls(dm.dlog_value, dm[["d_fb_share"]], dm[controls],
                            dm[iv], d._w, d[cluster], ["d_fb_share"], controls, **kwargs)
    else:
        result = estim.wls(dm.dlog_value, dm[["d_fb_share"] + controls],
                           d._w, d[cluster], ["d_fb_share"] + controls, **kwargs)
    row = estim.row(result, "d_fb_share")
    # This lane verifies beta, covariance and first-stage F; no over-ID claim.
    row.pop("J_p", None)
    row.pop("J_status", None)
    row.update(arm=arm, cluster=cluster, metros=d.cbsa.nunique(),
               row_hash=digest(d, ["geoid", "period"]),
               fixed_matrix_hash=digest(d, ["cbsa_period", "_w", "dlog_value", "d_fb_share"] + CONTROLS))
    return row


def pull(universe, beta, degree_distance=False, min_miles=0.25):
    if not degree_distance:
        return prep.gravity_pull(universe, "fb_share_0", beta, min_miles=min_miles)
    # The original appendix uses Euclidean longitude-latitude degrees, not miles.
    # No distance floor is specified there. Fail on duplicate tract centers.
    out = pd.Series(np.nan, index=universe.index)
    for _, b in universe.groupby("cbsa_period", sort=True):
        xy = b[["lat_0", "lon_0"]].to_numpy(float)
        distance = np.sqrt(((xy[:, None, :] - xy[None, :, :]) ** 2).sum(axis=2))
        np.fill_diagonal(distance, np.inf)
        if (distance == 0).any():
            raise ValueError("Duplicate tract centers require an explicit distance convention")
        out.loc[b.index] = distance ** (-beta) @ (b.fb_share_0 * b.aland_sqmi_0).to_numpy()
    return out / 1000


def ten_year_panel(raw):
    # Endpoints only: do not require valid 2018 prices or controls.
    a = raw[raw.period == "A"]
    b = raw[raw.period == "B"]
    c0 = [c for c in raw if c.endswith("_0")]
    c1 = [c for c in raw if c.endswith("_1")]
    keys = ["geoid", "cbsa", "is_metro", "county_fips"]
    d = a[keys + c0].merge(b[["geoid"] + c1], on="geoid", validate="one_to_one")
    d["period"], d["cbsa_period"] = "D", d.cbsa + "_D"
    for name in ["own_rate", "vac_rate", "sfdet_share", "medyrbuilt", "fb_share", "hisp_share", "mex_share"]:
        d["d_" + name] = d[name + "_1"] - d[name + "_0"]
    d["d_medyrbuilt"] /= 10
    d["medyrbuilt_0"] = (d.medyrbuilt_0 - 1970) / 10
    d["log_inc_0"] = np.log(d.med_inc_0.where(d.med_inc_0 > 0))
    d["log_value_0"] = np.log(d.med_value_0.where(d.med_value_0 > 0))
    d["dlog_value"] = np.log(d.med_value_1.where(d.med_value_1 > 0)) - d.log_value_0
    totals = d.groupby("cbsa").agg(fb0=("fb_count_0", "sum"), fb1=("fb_count_1", "sum"), pop0=("pop_0", "sum"))
    totals["rate"] = (totals.fb1 - totals.fb0) / totals.pop0
    growth = (totals.fb1 - totals.fb0).clip(lower=0)
    ordered = totals.rate.sort_values(ascending=False)
    hits = (growth.reindex(ordered.index).cumsum() / growth.sum()) >= 0.765
    cutoff = ordered.loc[hits[hits].index[0]]
    d["msa_imm_pc"] = d.cbsa.map(totals.rate)
    valid = prep.valid(d, "value")
    totals.to_csv(OUT / "ten_year_metro_selection.csv")
    return valid, float(cutoff)


def main():
    OUT.mkdir(exist_ok=True)
    panel = prep.load()
    valid = prep.valid(panel, "value")
    coverage = valid[valid.sw_sample == 1].copy()
    rows = [fit(coverage, "pooled_current", "cbsa"), fit(coverage, "pooled_tract_cluster", "geoid")]
    assert abs(rows[0]["coef"] - rows[1]["coef"]) < 1e-12
    expected = pd.read_csv(MODERN / "derived/results_main.csv")
    target = expected.query("outcome == 'value' and treat == 'fb' and sample == 'sw' and period == 'pooled' and arm == 'ols2_baseline'").iloc[0]
    assert rows[0]["n"] == target.n
    assert abs(rows[0]["coef"] - target.coef) < 1e-6
    assert abs(rows[0]["se"] - target.se) < 1e-6

    va = valid[valid.period == "A"].copy()
    pa = panel[panel.period == "A"].copy()
    geo_cols = ["lat_0", "lon_0", "fb_share_0", "aland_sqmi_0"]
    neighbors = pa[np.isfinite(pa[geo_cols]).all(axis=1)].copy()
    assert (neighbors.aland_sqmi_0 >= 0).all()
    estimation = va[va.sw_sample == 1].copy()
    rows += [fit(estimation, "native_period_A", "cbsa"), fit(estimation, "native_period_A_tract", "geoid")]
    assert abs(rows[-1]["coef"] - rows[-2]["coef"]) < 1e-12
    # Each consecutive arm changes exactly one instrument construction choice.
    specs = [("A_valid_neighbors_beta1", va, 1., False, 0.25),
             ("A_all_neighbors_beta1", neighbors, 1., False, 0.25),
             ("A_all_neighbors_beta1p6", neighbors, 1.6, False, 0.25),
             ("A_all_neighbors_beta1p6_no_floor", neighbors, 1.6, False, 0.),
             ("A_all_neighbors_beta1p6_degrees", neighbors, 1.6, True, 0.)]
    for label, universe, exponent, degrees, floor in specs:
        d = estimation.copy()
        field = pull(universe, exponent, degrees, floor)
        d["pull"] = field.reindex(d.index)
        assert d.pull.notna().all()
        d["pull_lag"] = d.pull * d.fb_share_0
        d["pull_msa"] = d.pull * d.msa_imm_pc
        for col, extra, instruments in [(4, [], ["pull"]),
                                         (5, ["fb_share_0"], ["pull", "pull_lag", "pull_msa"]),
                                         (6, ["fb_share_0", "pull"], ["pull_lag", "pull_msa"])]:
            rows.append(fit(d, label + f"_col{col}", iv=instruments, extra=extra))
        print(label, "completed", flush=True)

    raw = pd.read_csv(MODERN / "derived/tract_panel.csv", dtype={"geoid": str, "cbsa": str, "county_fips": str})
    raw = raw[(raw.is_metro == 1) & raw.cbsa.notna()].copy()
    decade, cutoff = ten_year_panel(raw)
    for label, mask in [("ten_year_all", decade.index == decade.index),
                        ("ten_year_coverage", decade.msa_imm_pc >= cutoff),
                        ("ten_year_fixed5pct", decade.msa_imm_pc >= 0.05)]:
        rows.append(fit(decade[mask].copy(), label))
    pd.DataFrame(rows).to_csv(OUT / "modern_bridge.csv", index=False, float_format="%.12g")
    manifest = {"input_sha256": {str(p.relative_to(MODERN)): hashlib.sha256(p.read_bytes()).hexdigest() for p in
                 [MODERN / "derived/tract_panel.csv", MODERN / "derived/results_main.csv",
                  MODERN / "src/estim.py", MODERN / "src/prep.py"]},
                "packages": {name: version(name) for name in ["numpy", "pandas", "scipy"]},
                "period_A_price_valid_neighbors": len(va), "period_A_full_neighbors": len(neighbors),
                "period_A_frozen_estimation_rows": len(estimation), "ten_year_coverage_cutoff": cutoff,
                "ten_year_endpoint_valid_rows": len(decade)}
    (OUT / "modern_bridge_manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    print(pd.DataFrame(rows)[["arm", "coef", "se", "n", "clusters", "F_first"]].to_string(index=False))


if __name__ == "__main__":
    main()
