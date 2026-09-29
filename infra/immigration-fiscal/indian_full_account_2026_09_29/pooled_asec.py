"""Five ASEC files (2022-2026, income years 2021-2025) pooled for two thin Indian-origin cells: the second generation's
tax and earnings keys, and the India-born self-employed.

1. G2 (native with an India-born parent), adults 25-64: per person, the rough re-key's own tax and earnings keys
   (rekey_white.py K): federal and state income tax split equally within the tax unit (PH_SEQ, TAX_ID), floored at 0;
   earnings (PEARNVAL, floored at 0); OASDI earnings (capped at the year's taxable maximum). Dollars go to 2024 by the
   CPI-U annual average of the income year [DATA: crime_cost_2026_09_16/_cache/cpi_2016_2025.json, BLS CUUR0000SA0].
   Pooled mean = the stacked weighted mean (each year's own weights); SE across years = sd of the five year means /
   sqrt(5) (the indian_generation_2026_09_21 lane's se_year); 2025 SE from its 160 replicate weights.
   The ratio pooled / 2025 of each key is what rekey_indian.py applies to the 2025 G2 adults' keys (the robustness row).
2. India-born adults by the class of their longest job (LJCW 5-6 self-employed, 1-4 wage and salary): n, earnings,
   self-employment income (SEMP_VAL) and the count in traveler accommodation, grocery and convenience stores and
   gasoline stations (INDUSTRY 8660, 4971, 4972, 5090; Census 2017 industry codes) [INFERENCE: the code mapping].
Civilian frame as in the re-key (PRPERTYP 2 or under 15). The 2022-2025 files come from other lanes' caches.
Outputs: derived/g2_pooled.csv, derived/g1_class_pooled.csv.
Run from the repository root (about 2 min):
  OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/indian_full_account_2026_09_29/pooled_asec.py
"""
from __future__ import annotations

import csv
import json
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd

LANE = Path(__file__).resolve().parent
FISCAL = LANE.parent
DER = LANE / "derived"
ZIPS = {2022: FISCAL / "latam_comparison_2026_09_17/_cache/2022/asecpub22csv.zip",
        2023: FISCAL / "latam_comparison_2026_09_17/_cache/2023/asecpub23csv.zip",
        2024: FISCAL / "same_year_tax_2026_09_20/_cache/asecpub24csv.zip",
        2025: FISCAL / "gen_ledger_extension_2026_09_16/_cache/asecpub25csv.zip",
        2026: FISCAL / "ledger_asec2026_2026_09_16/_cache/asecpub26csv.zip"}
CAP = {2021: 142_800, 2022: 147_000, 2023: 160_200, 2024: 168_600, 2025: 176_100}   # SSA taxable maximum [SOURCE: SSA]
US = [57, 60, 66, 69, 73, 78]
INDIA = 210
SMALL_BIZ = [8660, 4971, 4972, 5090]
COLS = ["PH_SEQ", "PPPOS", "TAX_ID", "MARSUPWT", "A_AGE", "PRPERTYP", "PRCITSHP", "PENATVTY", "PEFNTVTY", "PEMNTVTY",
        "FEDTAX_AC", "STATETAX_A", "PEARNVAL", "LJCW", "SEMP_VAL", "INDUSTRY"]
KEYS = ["fit", "sit", "earn", "oasdi"]


def cpi():
    d = json.loads((FISCAL / "crime_cost_2026_09_16/_cache/cpi_2016_2025.json").read_text())
    return {int(r["year"]): float(r["value"]) for s in d["Results"]["series"] for r in s["data"] if r["period"] == "M13"}


def load(year):
    with zipfile.ZipFile(ZIPS[year]) as z:
        d = pd.read_csv(z.open(f"pppub{year % 100:02d}.csv"), usecols=COLS)
        rep = None
        if year == 2025:
            rep = pd.read_csv(z.open("asec_csv_repwgt_2025.csv")).rename(columns={"h_seq": "PH_SEQ"})
    return d, rep


def split(d, col):
    g = d.assign(v=d[col].astype(float)).groupby(["PH_SEQ", "TAX_ID"]).v
    return np.maximum((g.transform("sum") / g.transform("size")).to_numpy(), 0.0)


def main():
    c = cpi()
    g2_rows, cls_rows, means = [], [], {}
    rep_se = {}
    for year in ZIPS:
        d, rep = load(year)
        inc_year = year - 1
        f = c[2024] / c[inc_year]
        civ = (d.PRPERTYP.eq(2) | d.A_AGE.lt(15)).to_numpy()
        w = d.MARSUPWT.to_numpy(float) / 100 * civ
        native = d.PRCITSHP.isin([1, 2, 3])
        g2 = (native & (d.PEFNTVTY.eq(INDIA) | d.PEMNTVTY.eq(INDIA)) & d.A_AGE.between(25, 64)).to_numpy() & civ
        earn = d.PEARNVAL.clip(lower=0).to_numpy(float)
        k = {"fit": split(d, "FEDTAX_AC") * f, "sit": split(d, "STATETAX_A") * f, "earn": earn * f,
             "oasdi": np.minimum(earn, CAP[inc_year]) * f}
        m = {key: float((w * v)[g2].sum() / w[g2].sum()) for key, v in k.items()}
        means[year] = (m, float(w[g2].sum()), {key: float((w * v)[g2].sum()) for key, v in k.items()})
        g2_rows.append({"asec_year": year, "income_year": inc_year, "cpi_to_2024": f"{f:.6f}", "n": int(g2.sum()),
                        "weighted": f"{w[g2].sum():.0f}", **{f"{key}_mean_2024usd": f"{v:.2f}" for key, v in m.items()}})
        if year == 2025:
            r = d[["PH_SEQ", "PPPOS"]].merge(rep, on=["PH_SEQ", "PPPOS"], how="left", validate="one_to_one")
            R = r[[f"pwwgt{i}" for i in range(161)]].to_numpy(float) * civ[:, None]
            for key, v in k.items():
                x = (R[g2] * v[g2, None]).sum(axis=0) / R[g2].sum(axis=0)
                rep_se[key] = float(np.sqrt(4 / 160 * ((x[1:] - x[0]) ** 2).sum()))
        g1a = (d.PRCITSHP.isin([4, 5]) & d.PENATVTY.eq(INDIA) & d.A_AGE.ge(18)).to_numpy() & civ
        for cls, sel in (("self_employed", d.LJCW.isin([5, 6])), ("wage_salary", d.LJCW.isin([1, 2, 3, 4])),
                         ("not_working", ~d.LJCW.isin([1, 2, 3, 4, 5, 6]))):
            s = g1a & sel.to_numpy()
            biz = s & d.INDUSTRY.isin(SMALL_BIZ).to_numpy()
            cls_rows.append({"asec_year": year, "class": cls, "n": int(s.sum()), "weighted": f"{w[s].sum():.0f}",
                             "earnings_mean_2024usd": f"{(w * earn * f)[s].sum() / w[s].sum():.2f}",
                             "semp_mean_2024usd": f"{(w * d.SEMP_VAL.to_numpy(float) * f)[s].sum() / w[s].sum():.2f}",
                             "fed_state_tax_mean_2024usd": f"{(w * (k['fit'] + k['sit']))[s].sum() / w[s].sum():.2f}",
                             "n_motel_grocery_convenience_gas": int(biz.sum()),
                             "weighted_motel_grocery_convenience_gas": f"{w[biz].sum():.0f}"})
    # pooled G2 and the ratios
    tot_w = sum(v[1] for v in means.values())
    for key in KEYS:
        pooled = sum(v[2][key] for v in means.values()) / tot_w
        ym = np.array([v[0][key] for v in means.values()])
        se_year = float(ym.std(ddof=1) / np.sqrt(len(ym)))
        g2_rows.append({"asec_year": "pooled_2022_2026", "income_year": "2021-2025", "cpi_to_2024": "",
                        "n": sum(int(r["n"]) for r in g2_rows if r["asec_year"] != "pooled_2022_2026" and isinstance(r["asec_year"], int)),
                        "weighted": f"{tot_w:.0f}", "key": key, "pooled_mean_2024usd": f"{pooled:.2f}",
                        "pooled_se_year": f"{se_year:.2f}", "asec2025_mean": f"{means[2025][0][key]:.2f}",
                        "asec2025_se_replicate": f"{rep_se[key]:.2f}",
                        "ratio_pooled_over_2025": f"{pooled / means[2025][0][key]:.6f}",
                        "ratio_se": f"{se_year / means[2025][0][key]:.6f}"})
    # pooled G1 classes
    cl = pd.DataFrame(cls_rows)
    for col in ("n", "n_motel_grocery_convenience_gas"):
        cl[col] = cl[col].astype(int)
    for cls, x in cl.groupby("class", sort=False):
        wt = x.weighted.astype(float)
        cls_rows.append({"asec_year": "pooled_2022_2026", "class": cls, "n": int(x.n.sum()), "weighted": f"{wt.sum():.0f}",
                         **{col: f"{(x[col].astype(float) * wt).sum() / wt.sum():.2f}" for col in
                            ("earnings_mean_2024usd", "semp_mean_2024usd", "fed_state_tax_mean_2024usd")},
                         "n_motel_grocery_convenience_gas": int(x.n_motel_grocery_convenience_gas.sum()),
                         "weighted_motel_grocery_convenience_gas": f"{x.weighted_motel_grocery_convenience_gas.astype(float).sum():.0f}"})
    DER.mkdir(exist_ok=True)
    for name, rows in (("g2_pooled.csv", g2_rows), ("g1_class_pooled.csv", cls_rows)):
        fields = list(dict.fromkeys(k for r in rows for k in r))
        with open(DER / name, "w", newline="") as fh:
            wr = csv.DictWriter(fh, fieldnames=fields, lineterminator="\n")
            wr.writeheader()
            wr.writerows(rows)
    print(pd.DataFrame(g2_rows).to_string(index=False))
    print(pd.DataFrame(cls_rows).to_string(index=False))


if __name__ == "__main__":
    main()
