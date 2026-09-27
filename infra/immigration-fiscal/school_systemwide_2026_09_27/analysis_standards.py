"""Test 3: did states whose English-learner, Hispanic or immigrant share grew more lower their
proficiency cut scores, measured on the NAEP scale (NCES state mapping studies, 2005–2022)?

Outcome: the NAEP scale equivalent of the state's "proficient" standard for a grade and subject. A lower
value is a lower bar on an absolute scale. Series: the NCES 2005–2009 comparison tables (NCES 2011-458,
built on each year's own state results) for 2005, 2007 and 2009, the per-year reports for 2011–2022. The
per-year 2009 tables differ by more than 3 points for 10 state-cells (Michigan by 17–44 points, Texas by
8–11), so they are a robustness check only; derived/standards_2009_overlap.csv lists both versions.

Writes derived/standards_estimates.csv. Run from the repository root:
    OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/school_systemwide_2026_09_27/analysis_standards.py
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from analysis_naep import FIELDS, TREAT, fmt, record, write  # noqa: E402
from panel import build  # noqa: E402
from stats_util import ols  # noqa: E402

OUT = HERE / "derived"


def mapping(per_year_2009=False):
    m = pd.read_csv(HERE / "derived" / "mapping_cut_scores.csv")
    early_years = [2005, 2007] if per_year_2009 else [2005, 2007, 2009]
    early = m[(m.series == "2005-2009 comparison") & m.year.isin(early_years)]
    late = m[(m.series == "per-year report") & (m.year >= (2009 if per_year_2009 else 2011))]
    both = m[m.year == 2009].pivot_table(index=["grade", "subject", "state"], columns="series", values="naep_equiv")
    both = both.dropna().reset_index()
    both["diff"] = both["per-year report"] - both["2005-2009 comparison"]
    cut = pd.concat([early, late])
    cut = cut[cut.naep_equiv.notna()].copy()
    cut["flag_rel_error"] = cut.flag.fillna("").str.contains("!").astype(int)
    return cut, both


def frame(p, per_year_2009=False):
    cut, overlap = mapping(per_year_2009)
    d = cut.merge(p[["subject", "grade", "year", "state", "cell", "region", "sd2019", "hisp_share",
                     "el_identified_pct_all", "imm_origin_share_617", "fb_share_u18"]],
                  on=["subject", "grade", "year", "state"], how="inner")  # drops Puerto Rico
    # 2022 CCD share is fall 2021 and 2022's EL share is NAEP 2022: both present in the panel
    d["z"] = d.naep_equiv / d.sd2019
    d["cell_state"] = d.cell + "|" + d.state
    d["cell_year"] = d.cell + "|" + d.year.astype(str)
    d["region_cell_year"] = d.region + "|" + d.cell_year
    return d, overlap


def main():
    p = build()
    d, overlap = frame(p)
    alt, _ = frame(p, per_year_2009=True)
    rows = []
    for tkey in ("hisp", "el", "imm"):
        col = TREAT[tkey][0]
        start = 2007 if tkey == "imm" else 2005
        for spec, sub, extra, note in [
            ("twfe", d[(d.year >= start) & (d.year <= 2019)], [], "state-by-cell and cell-by-year FE"),
            ("twfe_region_year", d[(d.year >= start) & (d.year <= 2019)], ["region_cell_year"], "adds region-by-cell-by-year FE"),
            ("twfe_no_flag", d[(d.year >= start) & (d.year <= 2019) & (d.flag_rel_error == 0)], [],
             "drops mappings NCES flags for relative error > 0.5"),
            ("twfe_2009_2019", d[(d.year >= 2009) & (d.year <= 2019)], [], "per-year reports only"),
            ("twfe_with_2022", d[d.year >= start], [], "adds the 2022 mapping"),
            ("twfe_per_year_2009", alt[(alt.year >= start) & (alt.year <= 2019)], [],
             "2009 from the per-year report instead of the comparison series"),
        ]:
            res = ols(sub, "z", [col], fe=["cell_state", "cell_year"] + extra, cluster="state")
            record(rows, res, col, test="cut_score", spec=spec, treatment=tkey, outcome="naep_equivalent_proficient",
                   cell="pooled", units="SD", years=f"{sub.year.min()}-{sub.year.max()}", note=note)
            if spec == "twfe":
                for cell in sorted(sub.cell.unique()):
                    c = sub[sub.cell == cell]
                    r = ols(c, "naep_equiv", [col], fe=["state", "year"], cluster="state")
                    record(rows, r, col, test="cut_score", spec=spec, treatment=tkey,
                           outcome="naep_equivalent_proficient", cell=cell, units="points",
                           years=f"{c.year.min()}-{c.year.max()}", note=note)
        # lead: next mapping wave's share, current share held fixed
        s = d[(d.year >= start) & (d.year <= 2019)].sort_values(["cell", "state", "year"]).copy()
        s["lead_" + col] = s.groupby(["cell", "state"])[col].shift(-1)
        s = s[s.year <= 2017]
        res = ols(s, "z", [col, "lead_" + col], fe=["cell_state", "cell_year"], cluster="state")
        record(rows, res, "lead_" + col, test="cut_score", spec="lead", treatment=tkey,
               outcome="naep_equivalent_proficient", cell="pooled", units="SD", years=f"{start}-2017",
               note="coefficient on the next wave's share")
        # long differences, first to last available mapping per state-cell within the window
        for y0, y1 in ([(start, 2019), (2009, 2019)] if tkey != "imm" else [(2007, 2019), (2009, 2019)]):
            a = d[d.year == y0].set_index(["cell", "state"])
            b = d[d.year == y1].set_index(["cell", "state"])
            ld = pd.DataFrame({"dy": (b.naep_equiv - a.naep_equiv) / b.sd2019, col: b[col] - a[col]}).dropna().reset_index()
            res = ols(ld, "dy", [col], fe=["cell"], cluster="state")
            record(rows, res, col, test="cut_score", spec=f"long_diff_{y0}_{y1}", treatment=tkey,
                   outcome="naep_equivalent_proficient", cell="pooled", units="SD", years=f"{y0}->{y1}",
                   note="change in the cut score on the change in the share")
    OUT.mkdir(exist_ok=True)
    write(OUT / "standards_estimates.csv", sorted(rows, key=lambda r: (r["treatment"], r["spec"], r["cell"])), FIELDS)
    overlap = overlap.sort_values(["grade", "subject", "state"])
    overlap.to_csv(OUT / "standards_2009_overlap.csv", index=False, lineterminator="\n", float_format="%.1f")
    # descriptive: national (unweighted state mean) cut score by year and cell, same-state panel 2009–2019
    desc = d[d.year.between(2005, 2022)].groupby(["cell", "year"]).naep_equiv.agg(["mean", "count"]).reset_index()
    desc["mean"] = desc["mean"].round(2)
    desc.to_csv(OUT / "standards_means.csv", index=False, lineterminator="\n")
    print(f"estimates={len(rows)}; 2009 overlap n={len(overlap)} |diff|>3: {int((overlap['diff'].abs() > 3).sum())}")


if __name__ == "__main__":
    main()
