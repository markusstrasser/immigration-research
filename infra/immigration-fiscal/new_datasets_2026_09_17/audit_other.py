"""Independent descriptive checks of ladder 105/106; not population inference."""
import argparse
import json
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent


def wilson(yes, n):
    p, z = yes / n, 1.959963984540054
    center = (p + z * z / (2 * n)) / (1 + z * z / n)
    half = z * np.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / (1 + z * z / n)
    return center - half, center + half


def contrast(a, b):
    """Difference a-b; Newcombe Wilson interval, independent-binomial sensitivity."""
    a, b = a.dropna(), b.dropna()
    assert len(a) and len(b) and a.isin([0, 1]).all() and b.isin([0, 1]).all()
    pa, pb = a.mean(), b.mean()
    la, ua = wilson(a.sum(), len(a))
    lb, ub = wilson(b.sum(), len(b))
    return {"n_a": len(a), "yes_a": int(a.sum()), "pct_a": 100 * pa,
            "n_b": len(b), "yes_b": int(b.sum()), "pct_b": 100 * pb,
            "difference_pp": 100 * (pa - pb),
            "iid95_low_pp": 100 * (pa - pb - np.sqrt((pa - la)**2 + (ub - pb)**2)),
            "iid95_high_pp": 100 * (pa - pb + np.sqrt((ua - pa)**2 + (pb - lb)**2))}


def cils(out):
    path = ROOT.parent / "cils_2026_09_17/raw/ICPSR_20520/DS0001/20520-0001-Data.tsv"
    d = pd.read_csv(path, sep="\t", low_memory=False)
    for col in ["V18", "V21A", "C3", "V448J", "V448L", "V400"]:
        d[col] = pd.to_numeric(d[col], errors="coerce")
    assert d.CASEID.is_unique and len(d) == 5262
    for col in ["V448J", "V448L"]:
        assert d[col].dropna().isin([0, 1]).all()
        assert not d.loc[d.V400.ne(1), col].notna().any()
    comparisons, bounds = [], []
    for label, code in [("Mexican", 2), ("Cuban", 1), ("Filipino", 30)]:
        men = d.loc[d.C3.eq(code) & d.V18.eq(1)]
        first = men.loc[men.V21A.notna() & men.V21A.ne(0)]
        second = men.loc[men.V21A.eq(0)]
        for item, col in [("arrest_last5y", "V448J"), ("detention_last5y", "V448L")]:
            comparisons.append({"origin": label, "item": item,
                                "contrast": "second minus foreign-born youth", **contrast(second[col], first[col])})
            for gen, sub in [("foreign-born youth", first), ("second", second)]:
                n, yes, valid = len(sub), int(sub[col].sum()), int(sub[col].notna().sum())
                bounds.append({"origin": label, "generation": gen, "item": item,
                               "baseline_n": n, "valid_n": valid, "yes": yes,
                               "observed_pct": 100 * yes / valid,
                               "completion_lower_pct": 100 * yes / n,
                               "completion_upper_pct": 100 * (yes + n - valid) / n})
    pd.DataFrame(comparisons).to_csv(out / "cils_contrasts.csv", index=False)
    pd.DataFrame(bounds).to_csv(out / "cils_missing_record_bounds.csv", index=False)


def iimmla(out):
    path = ROOT.parent / "iimmla_2026_09_17/raw/ICPSR_22627/DS0001/22627-0001-Data.tsv"
    d = pd.read_csv(path, sep="\t", low_memory=False)
    d.columns = d.columns.str.lower()
    d = d.copy()
    assert len(d) == 4655
    for col in ["evarre", "evpriso", "gender"]:
        assert d[col].isin([0, 1]).all()
    mother = d.q133a.where(d.q133a.between(1, 6))
    father = d.q150a.where(d.q150a.between(1, 6))
    d["parents_observed"] = mother.notna().astype(int) + father.notna().astype(int)
    d["parent_educ"] = pd.cut(pd.concat([mother, father], axis=1).max(axis=1),
                              [0, 1, 3, 6], labels=["<HS", "HS/voc", "SomeColl+"])
    rows = []
    for sex in ["both", "men", "women"]:
        sm = pd.Series(True, index=d.index) if sex == "both" else d.gender.eq(int(sex == "men"))
        for parents in ["one_or_two", "both_known"]:
            pm = d.parents_observed.ge(1 if parents == "one_or_two" else 2)
            for level in ["all", "<HS", "HS/voc", "SomeColl+"]:
                lm = pd.Series(True, index=d.index) if level == "all" else d.parent_educ.eq(level)
                a = d.loc[sm & pm & lm & d.ethnos10.eq(1) & d.generat3.eq(2)]
                b = d.loc[sm & pm & lm & d.ethnos10.eq(9) & d.generat3.eq(3)]
                for outcome in ["evarre", "evpriso"]:
                    if len(a) and len(b):
                        rows.append({"sex": sex, "parents": parents, "parent_educ": level,
                                     "outcome": outcome, "contrast": "Mexican second minus white third+",
                                     **contrast(a[outcome], b[outcome])})
    pd.DataFrame(rows).to_csv(out / "iimmla_sex_parent_education.csv", index=False)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, default=ROOT / "derived/other_audit")
    out = parser.parse_args().output_dir
    out.mkdir(parents=True, exist_ok=True)
    cils(out)
    iimmla(out)
    (out / "limitations.json").write_text(json.dumps({
        "mode": "descriptive adversarial audit",
        "intervals": "Independent-binomial sensitivity only; no survey-design/population coverage claim",
        "bounds": "Complete missing binary records arbitrarily; original sampled cohort, observed answers assumed truthful",
        "exclusions": "No causal effect, equivalence test, selection correction or national generalization"
    }, indent=2) + "\n")
    print(pd.read_csv(out / "cils_contrasts.csv").round(2).to_string(index=False))
    print(pd.read_csv(out / "cils_missing_record_bounds.csv").query("origin == 'Mexican'").round(2).to_string(index=False))
    z = pd.read_csv(out / "iimmla_sex_parent_education.csv")
    print(z.query("sex == 'men' and parents == 'one_or_two'").round(2).to_string(index=False))


if __name__ == "__main__":
    main()
