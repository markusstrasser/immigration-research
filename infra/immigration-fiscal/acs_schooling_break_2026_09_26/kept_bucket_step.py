"""Size the 2020 ACS reporting step in the Borjas panel's < HS bucket as rebuilt on 2026-09-26, which
keeps no-schooling records (IPUMS EDUC 0-5 = no schooling through grade 11).

Methods A and B of fix_borjas_panel.py return the excess no-schooling reports to grades 1-9. Under the
rebuilt rule those grades sit in the same bucket, so both corrections leave it unchanged. The bucket
still has a net step, because reports also move from grades 9-11 to 12th grade without a diploma,
which IPUMS files under EDUC 6 (HSG). This script sums break_anatomy.py's detrended steps
(`trend_step`, the §1 table's measure) over the bucket's categories by nativity. It then removes those
steps from the panel's 2023 bucket, scaling each by that nativity's population aged 18-64 in the panel.
The steps are measured at ages 20-64; the panel covers 18-64.
Output: derived/borjas_kept_bucket_step.csv. Run from the repository root:
  uv run --no-project python3 infra/immigration-fiscal/acs_schooling_break_2026_09_26/kept_bucket_step.py
"""
import sys
from pathlib import Path

import duckdb
import pandas as pd

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(ROOT / "infra/immigration-fiscal/build"))
import breakfix as B  # noqa: E402
import paths  # noqa: E402

STEPS = HERE / "derived" / "break_steps.csv"
BUCKET = ["none", "prek", "g1_4", "g5", "g6", "g7", "g8", "g9", "g10", "g11"]  # IPUMS EDUC 0-5


def main() -> None:
    s = pd.read_csv(STEPS)
    control = s[(s.universe == "age20_64") & (s.group == "mexico_born") & (s.category == "none")].trend_step
    B.gate(len(control) == 1 and abs(float(control.iloc[0]) - 2.846) < 0.001,
           "[BLOCKED] break_steps.csv no longer gives §1's Mexico-born no-schooling step (+2.85 pp)")
    step = s[s.category.isin(BUCKET)].groupby(["universe", "group"]).trend_step.sum() / 100

    con = duckdb.connect(str(paths.duckdb_path()), read_only=True)
    p = con.execute("SELECT * FROM borjas_supply_shock_panel WHERE year = 2023").fetchdf()
    con.close()
    fb_pop, nat_pop = p.immigrant_weight.sum(), p.native_weight.sum()
    h = p[p.education_bucket == "HSD"]
    fb, nat = float(h.immigrant_weight.sum()), float(h.native_weight.sum())
    B.gate(abs(fb / (fb + nat) - 0.44095) < 5e-6,
           "[BLOCKED] the panel is not the 2026-09-26 rebuild (2023 < HS share 44.095%)")

    rows = [{"universe": "as rebuilt", "step_fb_pp": 0.0, "step_native_pp": 0.0, "hsd_immigrant_share": fb / (fb + nat)}]
    for uni in ("age20_64", "age20_64_reported"):
        s_fb, s_nat = float(step[(uni, "foreign_born")]), float(step[(uni, "usborn")])
        f2, n2 = fb - s_fb * fb_pop, nat - s_nat * nat_pop
        rows.append({"universe": uni, "step_fb_pp": 100 * s_fb, "step_native_pp": 100 * s_nat,
                     "hsd_immigrant_share": f2 / (f2 + n2)})
    R = pd.DataFrame(rows)
    R.to_csv(HERE / "derived" / "borjas_kept_bucket_step.csv", index=False, float_format="%.5f", lineterminator="\n")
    print(R.to_string(index=False, float_format=lambda v: f"{v:.4f}"))


if __name__ == "__main__":
    main()
