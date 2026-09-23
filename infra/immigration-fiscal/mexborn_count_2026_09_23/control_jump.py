"""Where did the January 2025 and January 2026 CPS population-control changes land?

Each January the CPS moves to a new vintage of population controls. With national raking by age,
sex, race and Hispanic origin only, extra Hispanic control mass should spread over Hispanic
respondents roughly in proportion to their weight in each age-sex cell. This tabulates December ->
January by detailed Hispanic origin (PRDTHSP) and nativity, with November and February as
neighbours for month-to-month noise. Writes derived/control_jump.csv.
"""
from __future__ import annotations

from pathlib import Path

import pandas as pd

from monthly_series import BASIC, read_month

HERE = Path(__file__).resolve().parent
MONTHS = ["nov24", "dec24", "jan25", "feb25", "nov25", "dec25", "jan26", "feb26"]
# PRDTHSP detailed Hispanic origin, 2024-2026 record layouts
ORIGIN = {1: "Mexican", 2: "Puerto Rican", 3: "Cuban", 4: "Dominican", 5: "Salvadoran",
          6: "Other Central American", 7: "South American", 8: "Other Hispanic"}


def main() -> None:
    rows = []
    for m in MONTHS:
        d = read_month(BASIC / f"{m}pub.zip")
        d = d[d.w.gt(0)]
        fb = d.PRCITSHP.isin([4, 5])
        origin = d.PRDTHSP.map(ORIGIN).fillna("Not Hispanic")
        for (o, f), w in d.w.groupby([origin, fb.map({True: "foreign-born", False: "native"})]).sum().items():
            rows.append(dict(month=m, origin=o, nativity=f, weight_m=w / 1e6))
        rows.append(dict(month=m, origin="Mexico-born (PENATVTY 303)", nativity="foreign-born",
                         weight_m=d.w[d.PENATVTY.eq(303) & fb].sum() / 1e6))
    t = pd.DataFrame(rows).pivot_table(index=["origin", "nativity"], columns="month", values="weight_m")[MONTHS]
    t["dec24_to_jan25"] = t.jan25 - t.dec24
    t["nov24_to_dec24"] = t.dec24 - t.nov24
    t["jan25_to_feb25"] = t.feb25 - t.jan25
    t["dec25_to_jan26"] = t.jan26 - t.dec25
    t["nov25_to_dec25"] = t.dec25 - t.nov25
    t["jan26_to_feb26"] = t.feb26 - t.jan26
    t = t.round(6)
    t.to_csv(HERE / "derived/control_jump.csv")
    with pd.option_context("display.width", 250, "display.max_columns", 20):
        print(t.to_string())


if __name__ == "__main__":
    main()
