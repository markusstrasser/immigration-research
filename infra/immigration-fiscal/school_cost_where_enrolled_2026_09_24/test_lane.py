"""Positive controls and one hand-checked state for the school-cost-where-enrolled lane.

1. The explorer engine reproduces the published school step ($87.1414-113.9558bn) and main case.
2. The rebuilt school component reproduces the canonical key (updated_account_components.csv).
3. Texas by hand: F-33 FY2024 district spending per pupil weighted by CCD 2023-24 K-12 pupils, read
   straight from the raw files with none of the lane's code, equals state_breakdown.csv.
4. The preferred school line equals share x response x education line x household fraction x k x the
   school-only key share at both band ends.

    uv run --no-project --with pandas --with numpy --with pytest python3 -m pytest \
      infra/immigration-fiscal/school_cost_where_enrolled_2026_09_24/test_lane.py -q
"""
import json
import subprocess
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
OUT = HERE / "derived"
FISCAL = HERE.parent
F33 = Path("/Users/alien/research-data/immigration-fiscal/data/external/census_f33_district/elsec24t.txt")
CCD = Path("/Users/alien/research-data/immigration-fiscal/data/external/nces_ccd/ccd_lea_052_2324_l_1a_073124.csv")
K12 = ["Kindergarten", "Ungraded"] + [f"Grade {g}" for g in range(1, 13)]


def test_engine_reproduces_published_school_step():
    run = subprocess.run(["node", str(HERE / "engine_school.cjs")], capture_output=True, text=True)
    assert run.returncode == 0, run.stdout + run.stderr
    base = json.loads((OUT / "engine_base.json").read_text())
    assert np.allclose(base["base"]["step"], [87.1414, 113.9558], atol=1e-4)
    assert np.allclose(base["base"]["main"], [203.207, 249.64], atol=1e-4)


def test_rebuilt_school_component_matches_canonical():
    emb = json.loads((OUT / "account_embedded_price.json").read_text())
    comp = pd.read_csv(FISCAL / "school_enrollment_2026_09_20/derived/updated_account_components.csv")
    school = comp[comp.component.eq("school")].set_index(["allocation", "group"]).spending_bn
    assert abs(emb["target_school_personal_bn"] - school["personal", "mexican_observed_total"]) < 1e-6
    assert abs(emb["target_school_shared_bn"] - school["shared", "mexican_observed_total"]) < 1e-6
    assert abs(emb["national_school_personal_bn"] - school["personal", "national_civilian"]) < 1e-6
    # R_embedded = group price / national price, personal allocation: 16,860 / 17,669.
    assert abs(emb["r_embedded_personal"] - 0.954197) < 1e-6


def test_texas_by_hand():
    f = pd.read_csv(F33, dtype={"NCESID": str, "FIPST": str})
    f = f[f.FIPST.eq("48")].copy()
    f["LEAID"] = f.NCESID.str.zfill(7)
    f["pp"] = f.TCURSPND * 1000 / f.ENROLL.where(f.ENROLL > 0)
    f = f[f.pp.between(3000, 80000)]
    rows = []
    for chunk in pd.read_csv(CCD, chunksize=1_000_000, dtype={"LEAID": str, "FIPST": str},
                             usecols=["FIPST", "LEAID", "GRADE", "RACE_ETHNICITY", "STUDENT_COUNT", "TOTAL_INDICATOR"]):
        chunk = chunk[chunk.FIPST.eq("48") & chunk.GRADE.isin(K12) & chunk.STUDENT_COUNT.notna()]
        rows.append(chunk)
    c = pd.concat(rows)
    all_k12 = c[c.TOTAL_INDICATOR.eq("Subtotal 4 - By Grade")].groupby("LEAID").STUDENT_COUNT.sum()
    a = c[c.TOTAL_INDICATOR.eq("Category Set A - By Race/Ethnicity; Sex; Grade")]
    hisp = a[a.RACE_ETHNICITY.eq("Hispanic/Latino")].groupby("LEAID").STUDENT_COUNT.sum()
    f["n"] = f.LEAID.map(all_k12)
    f["h"] = f.LEAID.map(hisp).fillna(0)
    f = f[f.n.gt(0)]
    mean_all = np.average(f.pp, weights=f.n)
    mean_hisp = np.average(f.pp, weights=f.h)
    sb = pd.read_csv(OUT / "state_breakdown.csv").set_index("fips").loc[48]
    assert abs(mean_all / sb.f33_all_pupil_per_pupil - 1) < 1e-9
    assert abs(mean_hisp / sb.f33_hispanic_per_pupil - 1) < 1e-9
    assert abs(sb.assf_per_pupil - 12894.849672466036) < 1e-6          # ASSF FY2024 Table 8, Texas
    assert 1.0 < sb.within_state_factor < 1.06                          # Dallas, Houston, El Paso above the mean
    assert abs(sb.acs_mexican_share_of_hispanic_pupils - 0.811774) < 1e-6


def test_preferred_line_is_the_formula():
    base = json.loads((OUT / "engine_base.json").read_text())
    summ = json.loads((OUT / "lines_summary.json").read_text())
    he = base["education_national_bn"] * base["household_fraction"]
    share = {a: base["keys"]["school_operating"][a]["share"] for a in ["personal", "shared"]}
    lo_s, hi_s = base["school_share_bounds"]
    k = summ["k_preferred"]
    t = pd.read_csv(OUT / "per_pupil_weighting.csv")
    row = t[(t.spec == "preferred_district_and_school_level") & (t.key_treatment == "school")].iloc[0]
    assert abs(row.school_low_bn - lo_s * 0.63 * he * k * share["shared"]) < 1e-3
    assert abs(row.school_high_bn - hi_s * 0.66 * he * k * share["personal"]) < 1e-3
