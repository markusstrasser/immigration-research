"""Self-employment (unincorporated and incorporated) by nativity and generation, CPS ASEC 2025, adults 25-64.

Uses the generator's group definitions (parents' birthplace, self-ID Mexican origin, 3rd+ NH white).
A_CLSWKR: 1 private, 2 federal, 3 state, 4 local, 5 self-employed incorporated, 6 self-employed not
incorporated, 7 without pay, 0 not in universe. Share of employed adults (A_CLSWKR 1-6).
"""
import pathlib, zipfile
import pandas as pd

ZIP = pathlib.Path(__file__).resolve().parent.parent / "gen_ledger_extension_2026_09_16/_cache/asecpub25csv.zip"
COLS = ["A_AGE", "PRPERTYP", "PRCITSHP", "PENATVTY", "PEFNTVTY", "PEMNTVTY", "PEHSPNON", "PRDTRACE", "PRDTHSP",
        "MARSUPWT", "A_CLSWKR", "SEMP_VAL", "PEARNVAL"]
with zipfile.ZipFile(ZIP) as z:
    d = pd.read_csv(z.open("pppub25.csv"), usecols=COLS)
native = d.PRCITSHP.isin([1, 2, 3]); us_area = [57, 60, 66, 69, 73, 78]
parents_us = d.PEFNTVTY.isin(us_area) & d.PEMNTVTY.isin(us_area)
parent_mexico = d.PEFNTVTY.eq(303) | d.PEMNTVTY.eq(303)
groups = {
    "third_plus_nh_white": native & parents_us & d.PEHSPNON.eq(2) & d.PRDTRACE.eq(1),
    "all_native": native,
    "all_second_gen": native & ~parents_us,
    "mexican_second_gen": native & parent_mexico,
    "mexican_third_plus_selfid": native & parents_us & d.PRDTHSP.eq(1),
    "mexico_born": d.PRCITSHP.isin([4, 5]) & d.PENATVTY.eq(303),
    "mexico_born_noncitizen": d.PRCITSHP.eq(5) & d.PENATVTY.eq(303),
}
base = d.A_AGE.between(25, 64) & d.PRPERTYP.eq(2)
w = d.MARSUPWT / 100
rows = []
print(f"{'group':28}{'n':>7}{'employed%':>11}{'selfemp_unincorp%':>19}{'selfemp_incorp%':>17}{'semp_share_of_earn%':>21}")
for g, m in groups.items():
    mm = base & m; emp = mm & d.A_CLSWKR.between(1, 6)
    n = int(mm.sum()); emp_pct = w[emp].sum() / w[mm].sum() * 100
    un = w[emp & d.A_CLSWKR.eq(6)].sum() / w[emp].sum() * 100
    inc = w[emp & d.A_CLSWKR.eq(5)].sum() / w[emp].sum() * 100
    semp_share = (w[mm] * d.SEMP_VAL[mm]).sum() / (w[mm] * d.PEARNVAL[mm]).sum() * 100
    rows.append((g, n, emp_pct, un, inc, semp_share))
    print(f"{g:28}{n:7d}{emp_pct:11.1f}{un:19.1f}{inc:17.1f}{semp_share:21.1f}")
pd.DataFrame(rows, columns=["group", "n_unweighted", "employed_pct", "self_employed_unincorporated_pct_of_employed",
                            "self_employed_incorporated_pct_of_employed", "self_employment_income_share_of_earnings_pct"]
             ).to_csv(pathlib.Path(__file__).resolve().parent / "self_employment_by_generation.csv", index=False)
