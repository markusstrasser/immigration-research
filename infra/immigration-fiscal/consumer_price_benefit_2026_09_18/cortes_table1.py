#!/usr/bin/env python3
"""Cortes (2008 WP) Table 1: low-skilled immigrant share of the labor force, 25 cities.

Transcribed from https://www.economics.uci.edu/files/docs/colloqpapers/w06/Cortes.pdf
(pdftotext -layout, table on the page headed "Table 1. Share of Low-skilled Immigrants
in the Labor Force (%)").  Used to place this lane's counterfactual log change
(-0.6303) inside or outside the identifying variation.
"""
import numpy as np, pandas as pd
from pathlib import Path

D = Path(__file__).resolve().parent / "derived"
T = {"Atlanta": (0.38, 0.84, 3.23), "Baltimore": (0.76, 0.44, 0.67), "Boston": (3.53, 2.71, 2.62),
     "Chicago": (4.99, 5.09, 5.86), "Cincinnati": (0.44, 0.23, 0.34), "Cleveland": (1.82, 0.89, 0.65),
     "Dallas": (2.13, 5.17, 8.63), "Denver": (1.18, 1.42, 4.13), "Detroit": (1.76, 0.93, 1.35),
     "Houston": (3.96, 7.03, 9.21), "Kansas City": (0.58, 0.47, 1.44), "Los Angeles": (11.64, 15.90, 15.09),
     "Miami": (15.13, 14.44, 11.36), "Milwaukee": (1.07, 0.84, 1.54), "Minneapolis": (0.49, 0.37, 1.43),
     "New Orleans": (1.20, 1.13, 1.08), "New York City": (8.91, 7.82, 8.15), "Philadelphia": (1.39, 0.91, 1.06),
     "Portland": (1.03, 1.53, 3.27), "St. Louis": (0.49, 0.24, 0.53), "San Diego": (4.59, 5.92, 6.34),
     "San Francisco": (4.40, 6.73, 6.19), "Seattle": (1.22, 1.00, 1.94), "Tampa": (1.50, 1.69, 2.15),
     "Washington, DC": (1.61, 2.52, 3.76)}
OUR_SHOCK = -0.6302730590177434

df = pd.DataFrame([dict(city=c, s1980=a, s1990=b, s2000=d,
                        dln_1980_2000=float(np.log(d / a)),
                        dln_1990_2000=float(np.log(d / b)))
                   for c, (a, b, d) in T.items()])
df.to_csv(D / "cortes_table1_cities.csv", index=False)
ch = df.dln_1980_2000.to_numpy()
print(f"n={len(ch)} mean={ch.mean():.4f} median={np.median(ch):.4f} "
      f"min={ch.min():.4f} max={ch.max():.4f}")
print(f"our shock dln={OUR_SHOCK:.4f}; |dln| at least as large: "
      f"{(np.abs(ch) >= abs(OUR_SHOCK)).sum()}/{len(ch)}; "
      f"as large and NEGATIVE: {(ch <= OUR_SHOCK).sum()}/{len(ch)}")
