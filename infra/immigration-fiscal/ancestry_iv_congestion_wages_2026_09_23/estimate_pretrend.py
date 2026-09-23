"""Pre-trend placebo: do metros with a high 2000s ancestry prediction already show the 2000-2010
wage and commute movements in 1990-2000, before the inflow the instrument predicts?

Pre-period changes are measured on each metro's 1990-identifiable footprint (build_pums_1990.py);
the main-period 2000-2010 changes come from build_pums.py on the full 2013 footprint. Each
pre-period outcome runs through the same menu with the main-period treatment (the 2000-2010
change in the foreign-born share of employment), so the "IV" row is the placebo scaled into the
main estimate's units: reduced form on the pre-period change / main first stage. The same menu
on the main-period outcome for the same metros sits beside it. Z2_1990s (the ancestry file's
1990s prediction) is added as an instrument for the pre-period inflow itself, since a 1990s
response to the 1990s inflow, not a confounding trend, is one reading of a non-zero placebo
(Jaeger, Ruist and Stuhler's serial-correlation point).

Writes derived/estimates_pretrend.csv.
"""
import numpy as np
import pandas as pd

from common import DERIVED, menu, sample_fg, tsls, wls

GROUPS = ("noba", "ba", "hsl")
MIN_COVERAGE = 0.5


def load():
    fp = pd.read_csv(DERIVED / "pums_metro_1990fp.csv", dtype={"cbsa": str})
    full = pd.read_csv(DERIVED / "pums_metro.csv", dtype={"cbsa": str})

    def vars_(s, tag):
        s = s.set_index("cbsa")
        v = pd.DataFrame(index=s.index)
        for g in GROUPS:
            v[f"adj_week_{g}_{tag}"] = 100 * s[f"r_week_{g}"] / s[f"n_week_{g}"]
            v[f"adj_hour_{g}_{tag}"] = 100 * s[f"r_hour_{g}"] / s[f"n_hour_{g}"]
        v[f"rel_week_{tag}"] = v[f"adj_week_noba_{tag}"] - v[f"adj_week_ba_{tag}"]
        v[f"fbemp_{tag}"] = 100 * s.emp_fb / s.emp
        v[f"lnLH_{tag}"] = 100 * np.log(s.emp2564_noba / s.emp2564_ba)
        v[f"relhs_week_{tag}"] = v[f"adj_week_hsl_{tag}"] - v[f"adj_week_ba_{tag}"]
        v[f"lnLH_hsl_{tag}"] = 100 * np.log(s.emp2564_hsl / s.emp2564_ba)
        v[f"lncomm_nat_{tag}"] = 100 * np.log(s.commute_min_nat / s.commuters_nat)
        v[f"lncar_nat_{tag}"] = 100 * np.log(s.car_min_nat / s.car_nat)
        return v

    a = vars_(fp[fp["sample"] == 199001], "p90")
    b = vars_(fp[fp["sample"] == 200001], "p00")
    c = vars_(full[full["sample"] == 200001], "0")
    e = vars_(full[full["sample"] == 201001], "1")
    cov = fp[fp["sample"] == 199001].set_index("cbsa").fp_pop_share
    return pd.concat([a, b, c, e, cov], axis=1).reset_index()


def main():
    m = sample_fg().merge(load(), on="cbsa", how="inner")  # sample_fg carries the predicted-inflow columns
    m["Z2_1990s"] = 100.0 * m.pred_1990s_all / m["pop"]
    m = m[m.fp_pop_share >= MIN_COVERAGE].copy()
    outs = [f"adj_week_{g}" for g in GROUPS] + [f"adj_hour_{g}" for g in GROUPS] + \
        ["rel_week", "fbemp", "lnLH", "lncomm_nat", "lncar_nat"]
    for o in outs:
        m[f"pre_{o}"] = m[f"{o}_p00"] - m[f"{o}_p90"]
        m[f"main_{o}"] = m[f"{o}_1"] - m[f"{o}_0"]
    for o in ("relhs_week", "lnLH_hsl"):  # the high-school-or-less split, run in its own block below
        m[f"pre_{o}"] = m[f"{o}_p00"] - m[f"{o}_p90"]
        m[f"main_{o}"] = m[f"{o}_1"] - m[f"{o}_0"]
    m["d_fbemp"] = m.main_fbemp
    m["d_lnLH"] = m.main_lnLH
    m["d_lnLH_hsl"] = m.main_lnLH_hsl
    m["pre_fbemp_x"] = m.pre_fbemp
    rows = []
    inst = {"Z2": ["Z2"], "Z2_exmex": ["Z2_exmex"], "Z": ["Z"], "Z2_1990s": ["Z2_1990s"]}
    for d_name, frame in (("FG_1990fp", m), ("FG_1990fp_noLA", m[m.cbsa != "31080"])):
        b = {"design": d_name, "endpoint": "2010 ACS"}
        for o in outs:
            if o == "fbemp":
                continue
            menu(rows, frame, f"pre_{o}", "d_fbemp", {**b, "outcome": f"{o}, 1990-2000 (placebo)"},
                 instruments=inst)
            menu(rows, frame, f"main_{o}", "d_fbemp", {**b, "outcome": f"{o}, 2000-2010 (same metros)"},
                 instruments=inst)
            # the main estimate with the metro's own pre-period change held fixed
            menu(rows, frame, f"main_{o}", "d_fbemp", {**b, "outcome": f"{o}, 2000-2010 given 1990-2000 change"},
                 controls=[f"pre_{o}"], instruments={"Z2": ["Z2"], "Z2_exmex": ["Z2_exmex"]})
            # the pre-period outcome on the pre-period inflow, instrumented by the 1990s prediction
            menu(rows, frame, f"pre_{o}", "pre_fbemp_x", {**b, "outcome": f"{o}, 1990-2000 on 1990s inflow"},
                 instruments={"Z2_1990s": ["Z2_1990s"], "Z2": ["Z2"]})
        # serial correlation of the inflow itself
        menu(rows, frame, "pre_fbemp", "d_fbemp", {**b, "outcome": "foreign-born employment share, 1990-2000"},
             instruments=inst)
        # trend-adjusted (double difference): the 2000s change minus the metro's own 1990s change,
        # on the acceleration of the treatment
        f = frame.copy()
        for o in outs:
            f[f"dd_{o}"] = f[f"main_{o}"] - f[f"pre_{o}"]
        for o in ("rel_week", "adj_week_noba", "adj_week_ba", "adj_week_hsl", "lncar_nat", "lncomm_nat"):
            for x in ("dd_fbemp", "dd_lnLH"):
                if x == "dd_lnLH" and not o.startswith("rel"):
                    continue
                menu(rows, f, f"dd_{o}", x, {**b, "outcome": f"{o}, 2000s minus 1990s change"},
                     instruments={"Z2": ["Z2"], "Z2_exmex": ["Z2_exmex"], "Z2_1990s": ["Z2_1990s"],
                                  "Z2+Z2_1990s": ["Z2", "Z2_1990s"]})
        # Jaeger-Ruist-Stuhler form: the 2000s outcome on both decades' inflows, both predictions
        d = f.dropna(subset=["main_rel_week", "d_fbemp", "pre_fbemp", "Z2", "Z2_1990s", "w"])
        n, w = len(d), d.w.to_numpy()
        Zm = np.column_stack([np.ones(n), d.Z2, d.Z2_1990s])
        for o in ("rel_week", "adj_week_noba", "adj_week_ba", "adj_week_hsl", "lncar_nat"):
            X = np.column_stack([np.ones(n), d.d_fbemp, d.pre_fbemp])
            bcoef, se, _, _ = tsls(d[f"main_{o}"], X, Zm, w)
            for k, lab in ((1, "2000s inflow"), (2, "1990s inflow")):
                rows.append({**b, "outcome": f"{o}, 2000-2010 (JRS two-inflow IV)", "y": f"main_{o}",
                             "x": lab, "controls": "none", "estimator": "IV with Z2+Z2_1990s, two endogenous",
                             "n": n, "coef": bcoef[k], "se": se[k], "lo": bcoef[k] - 1.96 * se[k],
                             "hi": bcoef[k] + 1.96 * se[k]})
        for xname in ("d_fbemp", "pre_fbemp"):
            r = wls(d[xname], d[["Z2", "Z2_1990s"]], w)
            rows.append({**b, "outcome": "JRS first stage", "y": xname, "x": "Z2, Z2_1990s", "controls": "none",
                         "estimator": "first stage, joint F", "n": n, "coef": r.params["Z2"], "se": r.bse["Z2"],
                         "F": float(r.f_test(np.eye(3)[1:]).fvalue),
                         "coef_Z2_1990s": r.params["Z2_1990s"], "se_Z2_1990s": r.bse["Z2_1990s"]})
        # Sanderson-Windmeijer conditional F for each inflow given the other (2 instruments, 2 endogenous,
        # so the robust Wald on the residual has L - k + 1 = 1 effective degree of freedom)
        for xj, xk in (("d_fbemp", "pre_fbemp"), ("pre_fbemp", "d_fbemp")):
            Xk = np.column_stack([np.ones(n), d[xk]])
            bk, _, _, _ = tsls(d[xj], Xk, Zm, w)
            r = wls(d[xj].to_numpy() - Xk @ bk, d[["Z2", "Z2_1990s"]], w)
            rows.append({**b, "outcome": "JRS first stage", "y": xj, "x": f"given {xk}", "controls": "none",
                         "estimator": "Sanderson-Windmeijer conditional F", "n": n,
                         "F": float(r.wald_test(np.eye(3)[1:], scalar=True).statistic) / (2 - 2 + 1)})
        # persistence: the 2000s change on the metro's own 1990s change, and that change's coefficient
        # when it is the control in the lagged-change IV above
        for o in ("rel_week", "adj_week_noba", "adj_week_ba", "adj_week_hsl", "lnLH", "fbemp",
                  "lncomm_nat", "lncar_nat"):
            dd_ = frame.dropna(subset=[f"main_{o}", f"pre_{o}", "w"])
            r = wls(dd_[f"main_{o}"], dd_[[f"pre_{o}"]], dd_.w)
            rows.append({**b, "outcome": f"{o}, persistence", "y": f"main_{o}", "x": f"pre_{o}", "controls": "none",
                         "estimator": "OLS of 2000s change on 1990s change", "n": len(dd_),
                         "coef": r.params[f"pre_{o}"], "se": r.bse[f"pre_{o}"]})
            if o == "fbemp":
                continue
            dd_ = dd_.dropna(subset=["d_fbemp", "Z2"])
            one = np.ones(len(dd_))
            bc, sc, _, _ = tsls(dd_[f"main_{o}"], np.column_stack([one, dd_.d_fbemp, dd_[f"pre_{o}"]]),
                                np.column_stack([one, dd_.Z2, dd_[f"pre_{o}"]]), dd_.w.to_numpy())
            rows.append({**b, "outcome": f"{o}, persistence", "y": f"main_{o}", "x": f"pre_{o}",
                         "controls": "d_fbemp instrumented by Z2",
                         "estimator": "coefficient on the 1990s change in the lagged-change IV", "n": len(dd_),
                         "coef": bc[2], "se": sc[2]})
        # the sigma design and the high-school-or-less split under the same tests: the relative wage on
        # the relative supply it pairs with (no BA / BA; high school or less / BA), placebo and main period
        for o, xs in (("rel_week", ("d_lnLH",)), ("relhs_week", ("d_fbemp", "d_lnLH_hsl"))):
            for x in xs:
                menu(rows, frame, f"pre_{o}", x, {**b, "outcome": f"{o}, 1990-2000 (placebo)"}, instruments=inst)
                menu(rows, frame, f"main_{o}", x, {**b, "outcome": f"{o}, 2000-2010 (same metros)"},
                     instruments=inst)
        menu(rows, frame, "main_relhs_week", "d_fbemp",
             {**b, "outcome": "relhs_week, 2000-2010 given 1990-2000 change"},
             controls=["pre_relhs_week"], instruments={"Z2": ["Z2"], "Z2_exmex": ["Z2_exmex"]})
        f["dd_relhs_week"] = f.main_relhs_week - f.pre_relhs_week
        f["dd_lnLH_hsl"] = f.main_lnLH_hsl - f.pre_lnLH_hsl
        for x in ("dd_fbemp", "dd_lnLH_hsl"):
            menu(rows, f, "dd_relhs_week", x, {**b, "outcome": "relhs_week, 2000s minus 1990s change"},
                 instruments={"Z2": ["Z2"], "Z2_exmex": ["Z2_exmex"], "Z2_1990s": ["Z2_1990s"],
                              "Z2+Z2_1990s": ["Z2", "Z2_1990s"]})
        dh = f.dropna(subset=["main_relhs_week", "d_fbemp", "pre_fbemp", "Z2", "Z2_1990s", "w"])
        nh = len(dh)
        bcoef, se, _, _ = tsls(dh.main_relhs_week, np.column_stack([np.ones(nh), dh.d_fbemp, dh.pre_fbemp]),
                               np.column_stack([np.ones(nh), dh.Z2, dh.Z2_1990s]), dh.w.to_numpy())
        for k, lab in ((1, "2000s inflow"), (2, "1990s inflow")):
            rows.append({**b, "outcome": "relhs_week, 2000-2010 (JRS two-inflow IV)", "y": "main_relhs_week",
                         "x": lab, "controls": "none", "estimator": "IV with Z2+Z2_1990s, two endogenous",
                         "n": nh, "coef": bcoef[k], "se": se[k], "lo": bcoef[k] - 1.96 * se[k],
                         "hi": bcoef[k] + 1.96 * se[k]})
        for o in ("relhs_week", "lnLH_hsl"):
            dd_ = frame.dropna(subset=[f"main_{o}", f"pre_{o}", "w"])
            r = wls(dd_[f"main_{o}"], dd_[[f"pre_{o}"]], dd_.w)
            rows.append({**b, "outcome": f"{o}, persistence", "y": f"main_{o}", "x": f"pre_{o}", "controls": "none",
                         "estimator": "OLS of 2000s change on 1990s change", "n": len(dd_),
                         "coef": r.params[f"pre_{o}"], "se": r.bse[f"pre_{o}"]})
    est = pd.DataFrame(rows)
    est.to_csv(DERIVED / "estimates_pretrend.csv", index=False)
    with pd.option_context("display.width", 250, "display.max_rows", 400):
        show = est[est.estimator.isin(["first stage on Z2", "first stage on Z2_1990s", "reduced form on Z2",
                                       "IV with Z2", "IV with Z2_exmex", "IV with Z2_1990s"])
                   & est.design.eq("FG_1990fp")]
        print(show[["outcome", "x", "controls", "estimator", "n", "coef", "se", "F", "ar_lo", "ar_hi"]]
              .round(4).to_string(index=False))


if __name__ == "__main__":
    main()
