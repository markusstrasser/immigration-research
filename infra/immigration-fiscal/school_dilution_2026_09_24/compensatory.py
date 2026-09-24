"""Task 2: does money follow the group's pupils, and do other pupils' instructional resources fall?

State formulas pay more for poor and English-learner pupils (California LCFF supplemental and
concentration grants inside the general formula; Texas compensatory and bilingual allotments), and
federal Title I and Title III add more. F-33 separates some of it: C14 Title I, B11 federal bilingual
(Title III, through the state), C06 state compensatory and basic-skills programs, C07 state bilingual
programs; formula weights paid inside general formula aid (C01) are not separable.

Cross-sections (district revenue and spending per pupil, real 2024 dollars, within state, pupil-weighted):
  hisp          y ~ Hispanic share + log pupils | state
  hisp_pov      y ~ Hispanic share + child poverty + log pupils | state
  el_pov        y ~ EL share + child poverty + log pupils | state
  el_hisp_pov   y ~ EL share + Hispanic share + child poverty + log pupils | state
Waves: F-33 FY2020 with CCD fall 2019 and SAIPE 2019 (main, pre-COVID); FY2024 with fall 2023 and
SAIPE 2023 (no EL counts); FY2011 and FY2006 with their falls and SAIPE years.

Within-district panel over the waves FY2001, FY2006, FY2011, FY2020 (and FY2024):
  y ~ Hispanic share + log pupils | district + state-year     (composition effect, enrollment held)
  log y ~ log pupils + Hispanic share | district + state-year (scale and composition together)

Standard errors clustered by state. Writes derived/compensatory_estimates.csv.

    OPENBLAS_NUM_THREADS=1 uv run --no-project --with pandas --with pyarrow --with pyfixest \
      python3 infra/immigration-fiscal/school_dilution_2026_09_24/compensatory.py
"""
import sys
import warnings
from pathlib import Path

import numpy as np
import pandas as pd
import pyfixest as pf

warnings.filterwarnings("ignore")
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import district_covariates as dc  # noqa: E402

OUT = HERE / "derived"
WAVES = {2000: (2001, None, 2000), 2005: (2006, 2005, 2005), 2010: (2011, 2010, 2010),
         2019: (2020, 2019, 2019), 2023: (2024, 2023, None)}      # fall: (F-33 FY, SAIPE year, EL fall)
Y = {"rev_total": "TOTALREV", "rev_federal": "TFEDREV", "rev_state": "TSTREV", "rev_local": "TLOCREV",
     "title1": "C14", "fed_bilingual": "B11", "state_comp": "C06", "state_bilingual": "C07",
     "state_formula": "C01", "idea": "C15", "current": "current", "instruction": "instruction",
     "instr_support": None, "administration": None}
PP_BAND = (4_000.0, 80_000.0)


def wave(fall):
    fy, saipe_year, el_fall = WAVES[fall]
    p = pd.read_parquet(HERE / "_cache" / "panel.parquet")
    p = p[p.year.eq(fy) & p.SCHLEV.isin(["01", "02", "03"]) & p.leaid.ne("") & p.fips.le(56) & p.V33.ge(100)]
    p = p.groupby("leaid", as_index=False).first()
    p["instr_support"] = p.pupil_support + p.instr_staff
    p["administration"] = p.gen_admin + p.school_admin + p.business
    for k, col in Y.items():
        p[k] = p[col if col else k].fillna(0) * p.defl_2024 / p.V33
    p = p[p.current.between(*PP_BAND)]
    m = dc.membership(fall)
    p = p.join(m[["hisp_share", "pupils"]], on="leaid", how="inner")
    if saipe_year:
        p = p.join(dc.saipe(saipe_year)[["pov_rate"]], on="leaid")
    else:
        p["pov_rate"] = np.nan
    if el_fall:
        el = dc.english_learners(el_fall)
        p["el_share"] = (p.leaid.map(el) / p.pupils).clip(0, 1)
    else:
        p["el_share"] = np.nan
    p["lnN"] = np.log(p.V33)
    p["fall"], p["fy"] = fall, fy
    return p


def cross_sections(frames):
    rows = []
    for fall, p in frames.items():
        specs = {"hisp": "hisp_share + lnN", "hisp_pov": "hisp_share + pov_rate + lnN",
                 "el_pov": "el_share + pov_rate + lnN", "el_hisp_pov": "el_share + hisp_share + pov_rate + lnN"}
        for name, rhs in specs.items():
            need = [v for v in ["hisp_share", "pov_rate", "el_share"] if v in rhs]
            d = p.dropna(subset=need)
            if len(d) < 1000:
                continue
            for y in Y:
                m = pf.feols(f"{y} ~ {rhs} | fips", data=d, vcov={"CRV1": "fips"}, weights="V33")
                for term in [t for t in ["hisp_share", "el_share", "pov_rate"] if t in rhs]:
                    b, se = float(m.coef()[term]), float(m.se()[term])
                    rows.append({"design": "cross_section", "fy": int(p.fy.iloc[0]), "spec": name, "outcome": y,
                                 "term": term, "coef_usd_per_pupil_per_unit_share": b, "se": se,
                                 "ci_low": b - 1.96 * se, "ci_high": b + 1.96 * se,
                                 "outcome_mean_pw": float((d[y] * d.V33).sum() / d.V33.sum()),
                                 "term_mean_pw": float((d[term] * d.V33).sum() / d.V33.sum()),
                                 "n_districts": int(m._N), "pupils_m": float(d.V33.sum() / 1e6)})
    return rows


def panel(frames, falls, label):
    d = pd.concat([frames[f] for f in falls], ignore_index=True)
    d["stateyear"] = d.fips.astype(int) * 10000 + d.fy
    d = d[d.groupby("leaid").fy.transform("size").ge(2)].copy()
    d["w"] = d.groupby("leaid").V33.transform("mean")
    rows = []
    for y in Y:
        m = pf.feols(f"{y} ~ hisp_share + lnN | leaid + stateyear", data=d, vcov={"CRV1": "fips"}, weights="w")
        b, se = float(m.coef()["hisp_share"]), float(m.se()["hisp_share"])
        rows.append({"design": f"panel_{label}", "fy": -1, "spec": "levels_hisp_lnN", "outcome": y,
                     "term": "hisp_share", "coef_usd_per_pupil_per_unit_share": b, "se": se,
                     "ci_low": b - 1.96 * se, "ci_high": b + 1.96 * se,
                     "outcome_mean_pw": float((d[y] * d.V33).sum() / d.V33.sum()),
                     "term_mean_pw": float((d.hisp_share * d.V33).sum() / d.V33.sum()),
                     "n_districts": int(d.leaid.nunique()), "pupils_m": float(d.groupby("fy").V33.sum().mean() / 1e6)})
        dp = d.dropna(subset=["pov_rate"])
        if dp.fy.nunique() >= 2:
            dp = dp[dp.groupby("leaid").fy.transform("size").ge(2)]
            m = pf.feols(f"{y} ~ hisp_share + pov_rate + lnN | leaid + stateyear", data=dp, vcov={"CRV1": "fips"},
                         weights="w")
            b, se = float(m.coef()["hisp_share"]), float(m.se()["hisp_share"])
            rows.append({"design": f"panel_{label}", "fy": -1, "spec": "levels_hisp_pov_lnN", "outcome": y,
                         "term": "hisp_share", "coef_usd_per_pupil_per_unit_share": b, "se": se,
                         "ci_low": b - 1.96 * se, "ci_high": b + 1.96 * se,
                         "outcome_mean_pw": float((dp[y] * dp.V33).sum() / dp.V33.sum()),
                         "term_mean_pw": float((dp.hisp_share * dp.V33).sum() / dp.V33.sum()),
                         "n_districts": int(dp.leaid.nunique()),
                         "pupils_m": float(dp.groupby("fy").V33.sum().mean() / 1e6)})
    # scale and composition together, in logs of total spending
    for y in ["current", "instruction", "instr_support", "administration", "rev_total"]:
        tot = d[y] * d.V33
        s = d[tot > 0].assign(ly=np.log(tot[tot > 0]))
        m = pf.feols("ly ~ lnN + hisp_share | leaid + stateyear", data=s, vcov={"CRV1": "fips"}, weights="w")
        for term in ("lnN", "hisp_share"):
            b, se = float(m.coef()[term]), float(m.se()[term])
            rows.append({"design": f"panel_{label}", "fy": -1, "spec": "log_total_lnN_hisp", "outcome": y,
                         "term": term, "coef_usd_per_pupil_per_unit_share": b, "se": se,
                         "ci_low": b - 1.96 * se, "ci_high": b + 1.96 * se, "outcome_mean_pw": np.nan,
                         "term_mean_pw": np.nan, "n_districts": int(s.leaid.nunique()),
                         "pupils_m": float(s.groupby("fy").V33.sum().mean() / 1e6)})
        m = pf.feols("ly ~ lnN | leaid + stateyear", data=s, vcov={"CRV1": "fips"}, weights="w")
        b, se = float(m.coef()["lnN"]), float(m.se()["lnN"])
        rows.append({"design": f"panel_{label}", "fy": -1, "spec": "log_total_lnN_only", "outcome": y, "term": "lnN",
                     "coef_usd_per_pupil_per_unit_share": b, "se": se, "ci_low": b - 1.96 * se,
                     "ci_high": b + 1.96 * se, "outcome_mean_pw": np.nan, "term_mean_pw": np.nan,
                     "n_districts": int(s.leaid.nunique()), "pupils_m": float(s.groupby("fy").V33.sum().mean() / 1e6)})
    return rows


def main():
    frames = {f: wave(f) for f in WAVES}
    rows = cross_sections({f: frames[f] for f in (2019, 2023, 2010, 2005)})
    rows += panel(frames, [2000, 2005, 2010, 2019], "fy2001_2020")
    rows += panel(frames, [2000, 2005, 2010, 2019, 2023], "fy2001_2024")
    r = pd.DataFrame(rows)
    OUT.mkdir(exist_ok=True)
    r.to_csv(OUT / "compensatory_estimates.csv", index=False, lineterminator="\n", float_format="%.6f")
    cov = pd.DataFrame([{"fall": f, "fy": WAVES[f][0], "districts": len(p), "pupils_m": p.V33.sum() / 1e6,
                         "hisp_share_pw": (p.hisp_share * p.V33).sum() / p.V33.sum(),
                         "el_covered_pupil_share": p.V33[p.el_share.notna()].sum() / p.V33.sum(),
                         "pov_covered_pupil_share": p.V33[p.pov_rate.notna()].sum() / p.V33.sum()}
                        for f, p in frames.items()])
    cov.to_csv(OUT / "compensatory_coverage.csv", index=False, lineterminator="\n", float_format="%.4f")
    print(cov.to_string(index=False))
    key = r[r.outcome.isin(["rev_total", "rev_state", "rev_local", "rev_federal", "title1", "state_comp",
                            "state_bilingual", "fed_bilingual", "current", "instruction"])]
    print(key[["design", "fy", "spec", "outcome", "term", "coef_usd_per_pupil_per_unit_share", "se"]].to_string(index=False))


if __name__ == "__main__":
    sys.exit(main())
