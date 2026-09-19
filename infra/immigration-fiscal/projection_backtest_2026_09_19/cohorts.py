"""Temporal checks on observed education and relative income, raw inputs read-only."""
from pathlib import Path
import numpy as np
import pandas as pd
import duckdb
import pyreadstat


def education3(x):
    """Years completed: below 12 / exactly 12 / above 12; invalid stays missing."""
    a = pd.to_numeric(x, errors="coerce")
    return pd.Series(np.where(a.between(0, 20), np.where(a < 12, 0, np.where(a == 12, 1, 2)), np.nan), index=x.index)


def gss_check(root, out):
    source = root / "infra/immigration-fiscal/attitudes_gen_2026_09_16/raw/GSS_stata/gss7224_r3a.dta"
    cols = ["year", "age", "cohort", "educ", "maeduc", "paeduc", "born", "parborn", "granborn", "ethnic", "wtssps", "spaneng"]
    # The supplied Stata file has non-UTF8 label bytes; explicit Latin-1 preserves
    # numeric values and avoids a parser-dependent silent variable substitution.
    d, meta = pyreadstat.read_dta(source, usecols=cols, encoding="latin1")
    if "yes" != meta.variable_value_labels["born"][1] or "mexico" != meta.variable_value_labels["ethnic"][17]:
        raise ValueError("GSS codebook anchor changed")
    d = d.apply(pd.to_numeric, errors="coerce")
    d["generation"] = np.select([
        d.born.eq(1) & d.parborn.isin([1, 2, 8]),
        d.born.eq(1) & d.parborn.eq(0) & d.granborn.between(1, 4),
        d.born.eq(1) & d.parborn.eq(0) & d.granborn.eq(0),
    ], [2, 3, 4], default=0)
    d["child_edu"] = education3(d.educ)
    d["row_id"] = np.arange(len(d))
    train = d.year.le(1996) & d.cohort.gt(1960)
    test = d.year.ge(1998) & d.cohort.ge(1972)
    if set(d.loc[train & d.age.between(25, 34), "cohort"]) & set(d.loc[test & d.age.between(25, 34), "cohort"]):
        raise ValueError("Training and held-out birth cohorts overlap")
    d["period"] = np.select([train, test], ["train_through_1996", "heldout_1998_2024"], default="exclude")
    valid = d.age.between(25, 34) & d.child_edu.notna() & d.period.ne("exclude")
    if not d.loc[valid,"wtssps"].gt(0).all():
        raise ValueError("GSS current recommended weight missing: never silently drop newer survey years")
    elig = valid & d.wtssps.gt(0)
    # Matching interview language avoids treating the 2006 frame expansion as a
    # failed schooling forecast. A separate all-language arm exposes the choice.
    frames = {"english_only": (d.year.lt(2006) | d.spaneng.eq(1)),
              "english_only_pre2021": (d.year.lt(2006) | d.spaneng.eq(1)) & d.year.le(2018),
              "all_available_languages": pd.Series(True, index=d.index)}
    rows, pred, coverage = [], [], []
    for frame, frame_mask in frames.items():
        for label, mask in [("all_origins_G2", d.generation.eq(2)), ("all_origins_G3", d.generation.eq(3)),
                            ("all_origins_G4plus", d.generation.eq(4)), ("Mexican_family_origin_G2", d.generation.eq(2) & d.ethnic.eq(17))]:
            x = d[elig & frame_mask & mask].copy()
            pairs = []
            for col in ["maeduc", "paeduc"]:
                p = x.copy(); p["parent_edu"] = education3(p[col]); p["parent"] = col
                pairs.append(p[p.parent_edu.notna()])
            p = pd.concat(pairs, ignore_index=True)
            for period in ["train_through_1996", "heldout_1998_2024"]:
                sample = x[x.period.eq(period)]
                coverage.append(dict(frame=frame, group=label, period=period, eligible_respondents=len(sample),
                                     respondents_with_parent=len(p.loc[p.period.eq(period), "row_id"].unique()),
                                     distinct_birth_cohorts=int(sample.cohort.nunique()),
                                     survey_year_min=sample.year.min(),survey_year_max=sample.year.max(),weight="WTSSPS"))
            for (period, parent_edu), sub in p.groupby(["period", "parent_edu"]):
                w = sub.wtssps.to_numpy()
                probabilities = [float(np.average(sub.child_edu.eq(k), weights=w)) for k in range(3)]
                assert np.isclose(sum(probabilities), 1)
                rows.append(dict(frame=frame, group=label, period=period, parent_edu=int(parent_edu),
                                 respondent_n=int(sub.row_id.nunique()), parent_links=len(sub), weight_sum=float(w.sum()),
                                 below12=probabilities[0], exactly12=probabilities[1], above12=probabilities[2]))
            tr = p[p.period.eq("train_through_1996")]
            te = p[p.period.eq("heldout_1998_2024")]
            if te.empty:
                continue
            # Do not produce an extrapolated prediction for parent categories with
            # fewer than 30 distinct training respondents; count dropped mass.
            supported = [k for k in range(3) if tr.loc[tr.parent_edu.eq(k), "row_id"].nunique() >= 30]
            te_ok = te[te.parent_edu.isin(supported)].copy()
            if te_ok.empty:
                pred.append(dict(frame=frame, group=label, status="insufficient_training_support", retained_parent_weight_share=0))
                continue
            outcome = []
            for k in range(3):
                lookup = {e: np.average(tr.loc[tr.parent_edu.eq(e), "child_edu"].eq(k), weights=tr.loc[tr.parent_edu.eq(e), "wtssps"]) for e in supported}
                predicted = np.average(te_ok.parent_edu.map(lookup), weights=te_ok.wtssps)
                observed = np.average(te_ok.child_edu.eq(k), weights=te_ok.wtssps)
                outcome.extend([predicted, observed, observed - predicted])
            pred.append(dict(frame=frame, group=label, status="supported_parent_categories_only", training_respondents=tr.row_id.nunique(),
                             heldout_respondents=te_ok.row_id.nunique(), retained_parent_weight_share=te_ok.wtssps.sum()/te.wtssps.sum(),
                             **dict(zip([f"{ed}_{metric}" for ed in ["below12", "exactly12", "above12"] for metric in ["predicted", "observed", "error"]], outcome))))
    pd.DataFrame(rows).to_csv(out / "gss_transition_cells.csv", index=False)
    pd.DataFrame(pred).to_csv(out / "gss_temporal_prediction.csv", index=False)
    pd.DataFrame(coverage).to_csv(out / "gss_coverage.csv", index=False)
    return [source]


def ipums_check(db, out):
    """Fixed birth and entry cohorts, followed in repeated cross-sections.

    The outcome is total personal income, because this extract lacks wages.
    Native reference is US-born all races: no missing Hispanic split is invented.
    """
    con = duckdb.connect(str(db), read_only=True)
    q = """SELECT YEAR, AGE, BPL, YRIMMIG, EDUC, EDUCD, EMPSTAT, WKSWORK1,
                    INCTOT, PERWT, GQ, YEAR-AGE AS birth_proxy
             FROM ipums_usa_borjas_panel
             WHERE YEAR IN (1990,2000,2010,2023) AND GQ IN (1,2,5)
               AND AGE BETWEEN 25 AND 74 AND (BPL=200 OR BPL<100)
               AND YEAR-AGE BETWEEN 1946 AND 1965"""
    d = con.execute(q).fetchdf()
    description = con.execute("DESCRIBE ipums_usa_borjas_panel").fetchall()
    if "INCWAGE" in [r[0] for r in description]:
        raise ValueError("Wage data appeared: use them before continuing the income-proxy route")
    con.close()
    d["income"] = d.INCTOT.where(~d.INCTOT.isin([9999999, 9999998, -9999999]))
    d["edu3"] = np.select([d.EDUCD.lt(62), d.EDUCD.isin([62,63,64])], [0,1], default=2)
    rows = []
    for lo, hi in [(1956, 1965), (1946, 1955)]:
        sample = d[d.birth_proxy.between(lo, hi)]
        for y in [1990, 2000, 2010, 2023]:
            if y - lo > 74:
                continue  # Prespecified domain is ages25..74, so no partial birth window.
            subset = sample[sample.YEAR.eq(y)]
            native = subset[subset.BPL.lt(100)]
            mex = subset[subset.BPL.eq(200) & subset.YRIMMIG.between(1975, 1980)]
            if mex.empty or native.empty:
                continue
            # Each target birth-year proxy receives its 1990 composition. The
            # same year-of-birth error occurs in both groups; no person linkage.
            standard = sample[sample.YEAR.eq(1990) & sample.BPL.eq(200) & sample.YRIMMIG.between(1975, 1980)].groupby("birth_proxy").PERWT.sum()
            standard /= standard.sum()
            result = dict(survey_year=y, birth_proxy=f"{lo}-{hi}", entry_window="1975-1980", ages=f"{y-hi}-{y-lo}",
                          target_n=len(mex), native_n=len(native), target_population=mex.PERWT.sum())
            for label, group in [("target", mex), ("native", native)]:
                cells = {}
                for b, s in group.groupby("birth_proxy"):
                    working = s[s.EMPSTAT.eq(1) & s.income.gt(0)]
                    if working.empty:
                        raise ValueError(f"Empty matched employed positive-income cell: year={y} group={label} birth={b} n={len(s)}")
                    cells[b] = [np.average(s.edu3.eq(0),weights=s.PERWT), np.average(s.edu3.eq(2),weights=s.PERWT),
                                np.average(s.EMPSTAT.eq(1),weights=s.PERWT), np.average(np.log(working.income),weights=working.PERWT)]
                cell = pd.DataFrame.from_dict(cells, orient="index").reindex(standard.index)
                if cell.isna().any().any():
                    raise ValueError("Unmatched birth-cohort support")
                estimates = standard.to_numpy() @ cell.to_numpy()
                result.update({f"{label}_{k}": float(v) for k,v in zip(["below_hs", "above_hs", "employment", "log_employed_total_income"],estimates)})
                result[f"{label}_weeks_worked_missing_share"]=float(np.average(group.WKSWORK1.isna(),weights=group.PERWT))
            result["relative_log_total_income"] = result["target_log_employed_total_income"] - result["native_log_employed_total_income"]
            rows.append(result)
    tab = pd.DataFrame(rows)
    for _, block in tab.groupby("birth_proxy"):
        baseline = block.loc[block.survey_year.eq(1990),"relative_log_total_income"].iloc[0]
        tab.loc[block.index, "change_in_relative_log_total_income_from_1990"] = block.relative_log_total_income - baseline
    tab.to_csv(out / "fixed_birth_entry_cohorts.csv",index=False)
    return [db]
