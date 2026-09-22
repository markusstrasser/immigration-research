#!/usr/bin/env python3
"""CPS ASEC 2022–2026: Indian-origin generations vs 3rd+ NH whites at common ages.

G1 = India-born. G2 = US-born with an India-born parent. G3+ = US-born, both parents
US-area-born, self-identified Asian Indian (PRDASIAN=1). That G3+ cell is race/ID, not
a grandparent-birthplace G3; the script also reports the diaspora remainder (US-born
Asian Indian with foreign-born parents who are not India-born).

This is an own-person tax/earnings table, not the SPM extended ledger (no K-12, MEPS,
employer payroll, sales or property). Compare G2 fiscal gaps to
indian_ledger_2026_09_18.

Run: uv run --no-project --with pandas --with numpy python3 analyze_cps.py
"""
from __future__ import annotations

import zipfile
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
INFRA = HERE.parent
OUT = HERE / "derived"
OUT.mkdir(exist_ok=True)

INDIA = 210
US = [57, 60, 66, 69, 73, 78]
BANDS = [(25, 34), (35, 44), (45, 54), (55, 64)]
PERSON = [
    "PH_SEQ", "PPPOS", "A_AGE", "A_HGA", "PRPERTYP", "PRCITSHP", "PENATVTY",
    "PEFNTVTY", "PEMNTVTY", "PEHSPNON", "PRDTRACE", "PRDASIAN", "MARSUPWT",
    "PEARNVAL", "FEDTAX_AC", "FICA", "STATETAX_A", "SS_VAL", "SSI_VAL", "PAW_VAL",
    "MCAID",
]
ZIPS = {
    2022: INFRA / "latam_comparison_2026_09_17/_cache/2022/asecpub22csv.zip",
    2023: INFRA / "latam_comparison_2026_09_17/_cache/2023/asecpub23csv.zip",
    2024: INFRA / "same_year_tax_2026_09_20/_cache/asecpub24csv.zip",
    2025: INFRA / "gen_ledger_extension_2026_09_16/_cache/asecpub25csv.zip",
    2026: INFRA / "ledger_asec2026_2026_09_16/_cache/asecpub26csv.zip",
}
GROUPS = [
    "white_g3plus", "india_g1", "india_g2", "india_g3plus_race",
    "india_g2_diaspora", "asian_indian_native_selfid",
]


def load_year(year: int, path: Path) -> pd.DataFrame:
    person = f"pppub{year % 100:02d}.csv"
    with zipfile.ZipFile(path) as z:
        header = z.open(person).readline().decode().strip().split(",")
        cols = [c for c in PERSON if c in header]
        missing = [c for c in PERSON if c not in header]
        if missing:
            print(f"  {year} missing columns: {missing}", flush=True)
        d = pd.read_csv(z.open(person), usecols=cols, low_memory=False)
    d["year"] = year
    if "PRDASIAN" not in d.columns:
        d["PRDASIAN"] = np.nan
    return d


def masks(d: pd.DataFrame) -> dict[str, np.ndarray]:
    native = d.PRCITSHP.isin([1, 2, 3]).to_numpy()
    foreign = d.PRCITSHP.isin([4, 5]).to_numpy()
    parents_us = d.PEFNTVTY.isin(US).to_numpy() & d.PEMNTVTY.isin(US).to_numpy()
    parent_india = (d.PEFNTVTY.eq(INDIA) | d.PEMNTVTY.eq(INDIA)).to_numpy()
    asian_indian = d.PRDASIAN.eq(1).to_numpy()
    return {
        "white_g3plus": native & parents_us & d.PEHSPNON.eq(2).to_numpy() & d.PRDTRACE.eq(1).to_numpy(),
        "india_g1": foreign & d.PENATVTY.eq(INDIA).to_numpy(),
        "india_g2": native & parent_india,
        "india_g3plus_race": native & parents_us & asian_indian,
        "india_g2_diaspora": native & asian_indian & ~parent_india & ~parents_us,
        "asian_indian_native_selfid": native & asian_indian,
    }


def wmean(x, w):
    w = np.asarray(w, float)
    s = w.sum()
    if s <= 0:
        return float("nan")
    return float(np.dot(np.asarray(x, float), w) / s)


def summarise(d: pd.DataFrame, use: np.ndarray, w: np.ndarray, ref_shares: np.ndarray | None):
    age = d.A_AGE.to_numpy()
    ba = (d.A_HGA >= 43).to_numpy(float)
    grad = (d.A_HGA >= 44).to_numpy(float)
    earn = d.PEARNVAL.to_numpy(float)
    tax = (d.FEDTAX_AC + d.FICA + d.STATETAX_A).to_numpy(float)
    cash = (d.SS_VAL + d.SSI_VAL + d.PAW_VAL).to_numpy(float)
    net = tax - cash
    medicaid = d.MCAID.eq(1).to_numpy(float)
    out = {
        "n": int(use.sum()),
        "weighted": float(w[use].sum()),
        "mean_age": wmean(age[use], w[use]),
        "ba_share": wmean(ba[use], w[use]),
        "grad_share": wmean(grad[use], w[use]),
        "earnings": wmean(earn[use], w[use]),
        "modeled_own_tax": wmean(tax[use], w[use]),
        "cash_transfers": wmean(cash[use], w[use]),
        "tax_minus_cash": wmean(net[use], w[use]),
        "medicaid": wmean(medicaid[use], w[use]),
    }
    band_n, band_earn, band_net, band_ba = [], [], [], []
    for lo, hi in BANDS:
        sel = use & (age >= lo) & (age <= hi)
        band_n.append(int(sel.sum()))
        band_earn.append(wmean(earn[sel], w[sel]) if sel.sum() else float("nan"))
        band_net.append(wmean(net[sel], w[sel]) if sel.sum() else float("nan"))
        band_ba.append(wmean(ba[sel], w[sel]) if sel.sum() else float("nan"))
    out["band_n"] = band_n
    if ref_shares is not None and all(n > 0 for n in band_n):
        out["age_std_earnings"] = float(np.dot(ref_shares, band_earn))
        out["age_std_tax_minus_cash"] = float(np.dot(ref_shares, band_net))
        out["age_std_ba"] = float(np.dot(ref_shares, band_ba))
        out["age_std_ok"] = True
    else:
        out["age_std_earnings"] = out["age_std_tax_minus_cash"] = out["age_std_ba"] = float("nan")
        out["age_std_ok"] = False
    return out


def main():
    rows = []
    pop_rows = []
    for year, path in ZIPS.items():
        print(f"[{year}] {path.name}", flush=True)
        if not path.exists():
            print("  SKIP missing zip", flush=True)
            continue
        d = load_year(year, path)
        civ = d.PRPERTYP.eq(2).to_numpy()
        age = d.A_AGE.to_numpy()
        adult = civ & (age >= 25) & (age <= 64)
        w = d.MARSUPWT.to_numpy(float) / 100.0
        g = masks(d)
        ref = adult & g["white_g3plus"]
        shares = np.array([w[ref & (age >= lo) & (age <= hi)].sum() for lo, hi in BANDS])
        shares = shares / shares.sum()
        print(f"  rows {len(d):,}  white 25-64 shares {shares.round(3)}", flush=True)
        for name, mask in g.items():
            for universe, umask, std in (
                ("adults_25_64", adult, shares),
                ("all_civ_or_child", civ | (age < 15), None),
            ):
                use = umask & mask
                s = summarise(d, use, w, std if universe == "adults_25_64" else None)
                print(f"    {universe:16} {name:28} n={s['n']:5d}  w={s['weighted']/1e6:6.3f}M  "
                      f"age={s['mean_age']:5.1f}  BA={s['ba_share']:5.1%}  "
                      f"earn={s['earnings']:8,.0f}  net={s['tax_minus_cash']:8,.0f}  "
                      f"bands={s['band_n']}  std={s['age_std_ok']}", flush=True)
                rows.append({"year": year, "universe": universe, "group": name, **{
                    k: v for k, v in s.items() if k != "band_n"
                }, **{f"n_{lo}_{hi}": n for (lo, hi), n in zip(BANDS, s["band_n"])}})
        # all-age stock
        for name, mask in g.items():
            use = (civ | (age < 15)) & mask
            pop_rows.append({"year": year, "group": name, "n": int(use.sum()),
                             "weighted": float(w[use].sum()),
                             "mean_age": wmean(age[use], w[use]),
                             "share_under18": wmean((age[use] < 18).astype(float), w[use])})

    frame = pd.DataFrame(rows)
    frame.to_csv(OUT / "cps_generation_years.csv", index=False, float_format="%.6f")
    pd.DataFrame(pop_rows).to_csv(OUT / "cps_generation_stock.csv", index=False, float_format="%.6f")

    # Equal-year mean of 2022–2026 adult estimates; stack n for precision.
    adult = frame.query("universe == 'adults_25_64'").copy()
    pooled = []
    for gname in GROUPS:
        sub = adult[adult.group == gname]
        if sub.empty:
            continue
        rec = {"group": gname, "years": int(sub.year.nunique()), "n_stack": int(sub.n.sum()),
               "n_min": int(sub.n.min()), "n_max": int(sub.n.max())}
        for col in ["weighted", "mean_age", "ba_share", "grad_share", "earnings",
                    "modeled_own_tax", "cash_transfers", "tax_minus_cash", "medicaid",
                    "age_std_earnings", "age_std_tax_minus_cash", "age_std_ba"]:
            rec[col] = float(sub[col].mean())
        rec["age_std_years_complete"] = int(sub.age_std_ok.sum())
        pooled.append(rec)
    pd.DataFrame(pooled).to_csv(OUT / "cps_generation_pooled.csv", index=False, float_format="%.6f")
    print("\n== equal-year mean, adults 25-64 ==", flush=True)
    for rec in pooled:
        print(f"  {rec['group']:28} n_stack={rec['n_stack']:5d}  BA={rec['ba_share']:5.1%}  "
              f"earn={rec['earnings']:8,.0f}  net={rec['tax_minus_cash']:8,.0f}  "
              f"std_net={rec['age_std_tax_minus_cash']:8,.0f}  "
              f"std_years={rec['age_std_years_complete']}/{rec['years']}", flush=True)


if __name__ == "__main__":
    main()
