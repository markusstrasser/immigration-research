"""Compare adolescent ASVAB percentiles among later BA holders, descriptively.

Uses audited NLSY97 family classifications and the public sampling design.
The outcome is prior preparation, not institutional quality or college learning.
"""

import argparse
import hashlib
import json
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import t


ROOT = Path(__file__).resolve().parents[3]
LANE = Path(__file__).resolve().parent


def load_rows(root):
    paths = {
        "rows": root / "infra/immigration-fiscal/frontier_execution_2026_09_17/derived/nlsy/analysis_rows.csv",
        "base": root / "infra/immigration-fiscal/new_datasets_2026_09_17/derived/nlsy/full_selected_data.csv",
        "score_design": root / "infra/immigration-fiscal/frontier_execution_2026_09_17/derived/nlsy/selected.csv",
    }
    rows = pd.read_csv(paths["rows"]).set_index("R0000100").sort_index()
    base = pd.read_csv(paths["base"]).set_index("R0000100").sort_index()
    raw = pd.read_csv(paths["score_design"]).set_index("R0000100").sort_index()
    assert len(rows) == 8984 and rows.index.is_unique
    assert rows.index.equals(base.index) and rows.index.equals(raw.index)
    score = raw.R9829600.where(raw.R9829600.ge(0)) / 1000
    degree = base.T8129600.where(base.T8129600.between(0, 7))
    ba = degree.ge(4).astype(float).where(degree.notna())
    for actual, expected in [
        (rows.afqt_percentile, score),
        (rows.BAplus_2013, ba),
        (rows.w2013, base.T8135900 / 100),
        (rows.stratum, raw.R1489700),
        (rows.psu, raw.R1489800),
    ]:
        np.testing.assert_allclose(actual, expected, equal_nan=True)
    rows["degree_2013"] = degree
    return rows, paths


class Survey:
    def __init__(self, rows):
        self.rows = rows
        self.design = pd.MultiIndex.from_frame(rows[["stratum", "psu"]])
        self.grid = self.design.unique().sort_values()
        counts = pd.Series(1, index=self.grid).groupby(level=0).sum()
        assert len(counts) == 117 and counts.eq(2).all()
        self.df = int(counts.sum() - len(counts))
        self.critical = float(t.ppf(0.975, self.df))

    def variance(self, influence):
        totals = pd.Series(np.asarray(influence), index=self.design)
        totals = totals.groupby(level=[0, 1]).sum().reindex(self.grid, fill_value=0)
        centered = totals - totals.groupby(level=0).transform("mean")
        return float(2 * centered.pow(2).sum())

    def estimate(self, mask, weight):
        y = self.rows.afqt_percentile
        valid = mask & y.notna() & weight.gt(0)
        w = weight.where(valid, 0)
        denominator = float(w.sum())
        assert denominator > 0, "An empty domain cannot produce a valid estimate"
        mean = float((w * y.fillna(0)).sum() / denominator)
        influence = (w * (y.fillna(0) - mean) / denominator).to_numpy()
        se = self.variance(influence) ** 0.5
        return {
            "n": int(valid.sum()),
            "mean_percentile": mean,
            "design_se": se,
            "low95": mean - self.critical * se,
            "high95": mean + self.critical * se,
            "kish_n": float(denominator**2 / w.pow(2).sum()),
            "domain_psus": len(self.design[valid].unique()),
        }, influence


def define_groups(rows):
    mexican = rows.comparison.eq("Mexican_Chicano_self_ID")
    white = rows.comparison.eq("Baseline_NH_White_not_Mexican_self_ID")
    g3 = rows.linked_exact.str.startswith("G3_")
    g4 = rows.linked_exact.str.startswith("G4plus_")
    return {
        "Mexican_self_ID_all_family_histories": mexican,
        "Mexican_self_ID_G2": mexican & rows.linked_exact.str.startswith("G2_"),
        "Mexican_self_ID_G3": mexican & g3,
        "Mexican_self_ID_G4plus": mexican & g4,
        "Mexican_self_ID_G3_G4plus_pooled": mexican & (g3 | g4),
        "Mexican_self_ID_USparents_GP_unresolved": mexican & rows.linked_exact.eq("USborn_USparents_grandparents_unresolved"),
        "NH_white_all_family_histories": white,
        "NH_white_G4plus": white & g4,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--output-dir", type=Path, default=LANE / "derived/nlsy")
    args = parser.parse_args()
    out = args.output_dir
    out.mkdir(parents=True, exist_ok=True)
    rows, paths = load_rows(args.root)
    survey = Survey(rows)
    groups = define_groups(rows)
    benchmark, _ = survey.estimate(pd.Series(True, index=rows.index), rows.wbase)
    assert benchmark["n"] == 7093
    assert abs(benchmark["mean_percentile"] - 50.410) < 0.0006
    assert abs(benchmark["design_se"] - 0.638) < 0.0006
    ba = rows.BAplus_2013.eq(1)
    retained = rows.w2013.gt(0)
    coverage, means, contrasts, score_bounds = [], [], [], []
    for name, mask in groups.items():
        n_ba = int((mask & ba & retained).sum())
        scored = mask & ba & retained & rows.afqt_percentile.notna()
        coverage.append({
            "group": name,
            "baseline_n": int(mask.sum()),
            "degree_2013_observed_n": int((mask & retained & rows.BAplus_2013.notna()).sum()),
            "BAplus_2013_n": n_ba,
            "BAplus_and_score_n": int(scored.sum()),
            "BAplus_score_missing_n": n_ba - int(scored.sum()),
        })
        # Finite-sample bounds for missing scores within the classified BA group.
        # These cannot bound Mexican nonidentifiers excluded by the identity rule.
        domain_weight = rows.w2013.where(mask & ba & retained, 0)
        total_weight = float(domain_weight.sum())
        assert total_weight > 0
        score_bounds.append({
            "group": name,
            "BAplus_2013_n": n_ba,
            "missing_score_weight_fraction": float(domain_weight[rows.afqt_percentile.isna()].sum() / total_weight),
            "mean_if_missing_scores_0": float((domain_weight * rows.afqt_percentile.fillna(0)).sum() / total_weight),
            "mean_if_missing_scores_100": float((domain_weight * rows.afqt_percentile.fillna(100)).sum() / total_weight),
        })
    masks = {}
    for weight_name, weight in [("2013_interview", rows.w2013), ("baseline_among_2013_retained", rows.wbase.where(retained, 0))]:
        for condition, cmask in [("BAplus", ba), ("BA_only", rows.degree_2013.eq(4)), ("all_known_degree", rows.BAplus_2013.notna())]:
            for name, mask in groups.items():
                actual_mask = mask & cmask
                result, influence = survey.estimate(actual_mask, weight)
                key = (weight_name, condition, name)
                masks[key] = (result, influence)
                means.append({"weight": weight_name, "credential": condition, "group": name, **result})
            for name in groups:
                if not name.startswith("Mexican_"):
                    continue
                for reference in ["NH_white_G4plus", "NH_white_all_family_histories"]:
                    high, uh = masks[(weight_name, condition, name)]
                    low, ul = masks[(weight_name, condition, reference)]
                    difference = high["mean_percentile"] - low["mean_percentile"]
                    se = survey.variance(uh - ul) ** 0.5
                    contrasts.append({
                        "weight": weight_name, "credential": condition,
                        "group": name, "reference": reference,
                        "group_n": high["n"], "reference_n": low["n"],
                        "difference_percentile_points": difference,
                        "design_se": se,
                        "low95": difference - survey.critical * se,
                        "high95": difference + survey.critical * se,
                    })
    pd.DataFrame(coverage).to_csv(out / "coverage.csv", index=False)
    pd.DataFrame(score_bounds).to_csv(out / "missing_score_bounds.csv", index=False)
    pd.DataFrame(means).to_csv(out / "means.csv", index=False)
    pd.DataFrame(contrasts).to_csv(out / "contrasts.csv", index=False)
    rows[["comparison", "linked_exact", "sex", "stratum", "psu", "wbase", "w2013", "degree_2013", "BAplus_2013", "afqt_percentile"]].to_csv(out / "analysis_rows.csv")
    manifest = {
        "benchmark": benchmark,
        "df": survey.df,
        "source_hashes": {k: {"path": str(p), "sha256": hashlib.sha256(p.read_bytes()).hexdigest()} for k, p in paths.items()},
        "estimand": "Descriptive adolescent ASVAB percentile among observed 2013 BA holders; cohort born 1980-84, resident in US at original sampling.",
        "weights": "2013 interview weights principal; baseline weights among retained 2013 respondents sensitivity. Neither corrects unobserved test-score or family-history selection.",
        "limits": [
            "Prior adolescent skills, not learning caused by college or institution selectivity.",
            "Mexican/Chicano self-ID; not all Mexican descendants or an ancestry-attrition correction.",
            "Grandparent classification uses generic birthplace; no claim of exact Mexico origin of each forebear.",
            "BA versus postgraduate composition assessed through BA-only sensitivity; no standardization for major or sex.",
            "Sampling-design intervals omit nonresponse bias and classification uncertainty.",
            "No percentile-to-IQ or percentile-to-normal-score conversion.",
            "BA is measured in 2013, not lifetime attainment or a common exact age.",
        ],
    }
    (out / "audit.json").write_text(json.dumps(manifest, indent=2) + "\n")
    print(pd.DataFrame(coverage).to_string(index=False))
    selected = pd.DataFrame(means)
    print(selected[(selected.weight == "2013_interview") & (selected.credential == "BAplus")].to_string(index=False))
    selected = pd.DataFrame(contrasts)
    print(selected[(selected.weight == "2013_interview") & (selected.credential == "BAplus") & (selected.reference == "NH_white_G4plus")].to_string(index=False))


if __name__ == "__main__":
    main()
