"""Wage bills by Mexican-origin generation, CPS ASEC 2025 (income year 2024).

Group masks are copied verbatim from `gen_ledger_extension_2026_09_16/extend_ledger.py`
lines 228-238, so the populations here line up with the all-age ledger's accounts and the
per-person fiscal numbers in `all_age_ledger_2026_09_17/derived/estimates.csv` can be read
against these wage bills without redefining anybody.

Output: derived/wage_bills.csv - weighted persons, weighted wage bill (WSAL_VAL), mean
wage per person and per earner, for each group, all ages and ages 25-64.
"""
import pathlib, zipfile
import numpy as np
import pandas as pd

HERE = pathlib.Path(__file__).parent
ZIP = (HERE.parent / "gen_ledger_extension_2026_09_16" / "_cache" / "asecpub25csv.zip")
COLS = ["PRCITSHP", "PENATVTY", "PEFNTVTY", "PEMNTVTY", "PEHSPNON", "PRDTRACE",
        "PRDTHSP", "A_AGE", "PRPERTYP", "WSAL_VAL", "MARSUPWT",
        "FICA", "FEDTAX_AC", "STATETAX_A"]
US_AREA = [57, 60, 66, 69, 73, 78]


def main():
    with zipfile.ZipFile(ZIP) as z:
        with z.open("pppub25.csv") as f:
            d = pd.read_csv(f, usecols=COLS, low_memory=False)
    print("CPS ASEC person records:", len(d))
    w = d["MARSUPWT"].astype(float) / 100.0   # ASEC supplement weight carries 2 implied decimals
    wage = d["WSAL_VAL"].clip(lower=0).astype(float)
    native = d.PRCITSHP.isin([1, 2, 3])
    parents_us = d.PEFNTVTY.isin(US_AREA) & d.PEMNTVTY.isin(US_AREA)
    parent_mexico = d.PEFNTVTY.eq(303) | d.PEMNTVTY.eq(303)
    groups = {
        "mexico_born": (d.PRCITSHP.isin([4, 5]) & d.PENATVTY.eq(303)),
        "mexican_second_gen": (native & parent_mexico),
        "mexican_third_plus_selfid": (native & parents_us & d.PRDTHSP.eq(1)),
        "third_plus_nh_white": (native & parents_us & d.PEHSPNON.eq(2) & d.PRDTRACE.eq(1)),
        "all_native": native,
    }
    rows = []
    for name, m in groups.items():
        for band, sel in (("all_ages", pd.Series(True, index=d.index)),
                          ("25_64", d.A_AGE.between(25, 64) & d.PRPERTYP.eq(2))):
            k = (m & sel).to_numpy()
            pers = float(w[k].sum())
            bill = float((w[k] * wage[k]).sum())
            earners = float(w[k & (wage > 0).to_numpy()].sum())
            tax = float((w[k] * d.loc[k, ["FICA", "FEDTAX_AC", "STATETAX_A"]]
                         .sum(axis=1).astype(float)).sum())
            rows.append({"group": name, "band": band, "persons": pers,
                         "tax_fica_fed_state": tax,
                         "avg_tax_rate_on_wages": tax / bill if bill else np.nan,
                         "wage_bill": bill,
                         "mean_wage_per_person": bill / pers if pers else np.nan,
                         "earners": earners,
                         "mean_wage_per_earner": bill / earners if earners else np.nan,
                         "n_unweighted": int(k.sum())})
    out = pd.DataFrame(rows)
    (HERE / "derived").mkdir(exist_ok=True)
    out.to_csv(HERE / "derived" / "wage_bills.csv", index=False)
    pd.set_option("display.width", 200)
    print(out.to_string(index=False))


if __name__ == "__main__":
    main()
