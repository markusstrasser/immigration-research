"""Target population by age and Hispanic origin, CPS ASEC 2025, for the NCVS 12+ rate.

Rebuilds the complete account's 40,896,574 Mexican-origin union with the held ledger
builder (same masks and civilian domain as all_age_ledger_2026_09_17/analyze.py) and
tabulates ages 0-11 / 12-17 / 18+ plus the CPS Hispanic 12+ population, which is the
denominator of the population-share scaling. Stops if the union total drifts.
"""
from pathlib import Path
import argparse
import sys

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
FISCAL = HERE.parent
sys.path.insert(0, str(FISCAL / "gen_ledger_extension_2026_09_16"))
sys.path.insert(0, str(FISCAL / "build"))
import extend_ledger as ext  # noqa: E402

UNION_TOTAL = 40_896_574  # complete-account target, research/immigration-complete-annual-account-2026-09-20.md


def main() -> None:
    cps = FISCAL / "gen_ledger_extension_2026_09_16/_cache/asecpub25csv.zip"
    state = ext.build(argparse.Namespace(cps_zip=cps))
    d, g = state["d"], state["group"]
    w = state["person_weights"][:, 0]
    civilian = (d.PRPERTYP.eq(2) | d.A_AGE.lt(15)).to_numpy()
    parts = ["mexico_born", "mexican_second_gen", "mexican_third_plus_selfid"]
    union = np.zeros(len(d), bool)
    for p in parts:
        if (union & g[p] & civilian).any():
            raise ValueError("target categories overlap")
        union |= g[p] & civilian
    total = w[union].sum()
    if abs(total - UNION_TOTAL) > 1:
        raise SystemExit(f"[BLOCKED] union total {total:,.1f} != {UNION_TOTAL:,}")
    print(f"[gate] union total reproduces the complete account: {total:,.1f}")

    age = d.A_AGE.to_numpy()
    hisp = d.PEHSPNON.eq(1).to_numpy()
    rows = []
    for name, mask in [("union", union)] + [(p, g[p] & civilian) for p in parts] + [
            ("cps_hispanic_civilian", hisp & civilian),
            ("cps_all_civilian", civilian),
            ("union_hispanic", union & hisp),
            ("union_not_hispanic", union & ~hisp)]:
        rows.append(dict(group=name,
                         age_0_11=w[mask & (age < 12)].sum(),
                         age_12_17=w[mask & (age >= 12) & (age < 18)].sum(),
                         age_18_plus=w[mask & (age >= 18)].sum(),
                         age_12_plus=w[mask & (age >= 12)].sum(),
                         all_ages=w[mask].sum()))
    out = pd.DataFrame(rows)
    (HERE / "derived").mkdir(exist_ok=True)
    out.to_csv(HERE / "derived/target_population_cps2025.csv", index=False, float_format="%.1f")
    print(out.to_string(index=False, float_format=lambda v: f"{v:,.0f}"))


if __name__ == "__main__":
    main()
