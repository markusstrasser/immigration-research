"""Positive controls for the microdata panel against the published tables it should reproduce.

G3  PUMS mean one-way commute of all workers (2000 5%) against SF3 P033001/P031002 by CBSA
G4  the same for 2010: ACS 2010 PUMS against the ACS 2010 one-year CBSA table (codes that match)
G5  PUMS 2000 household population 16-64 against the SF1 2000 total population by CBSA (the
    ratio should be near the national 16-64 share with little spread; a PUMA-allocation error
    shows up as outliers)
Fails loudly when a correlation falls below 0.95 or a weighted mean gap exceeds 0.5 minutes.

Writes derived/pums_gates.json.
"""
import json

import numpy as np
import pandas as pd

from common import DERIVED


def wcorr(a, b, w):
    c = np.cov(np.vstack([a, b]), aweights=w)
    return float(c[0, 1] / np.sqrt(c[0, 0] * c[1, 1]))


def main():
    p = pd.read_csv(DERIVED / "pums_metro.csv", dtype={"cbsa": str})
    cm = pd.read_csv(DERIVED / "commute_metro.csv", dtype={"cbsa": str})
    out = {}
    for samp, col, tag in ((200001, "commute_0", "G3_2000"), (201001, "commute_1p", "G4_2010")):
        s = p[p["sample"] == samp].set_index("cbsa")
        m = cm.set_index("cbsa").join((s.commute_min / s.commuters).rename("pums"), how="inner")
        m = m.dropna(subset=[col, "pums", "pop_sf1_0"])
        w = m.pop_sf1_0.to_numpy()
        gap = float(np.average(m.pums - m[col], weights=w))
        out[tag] = dict(n=len(m), weighted_corr=wcorr(m.pums, m[col], w), weighted_mean_gap_min=gap,
                        max_abs_gap_min=float((m.pums - m[col]).abs().max()))
    s = p[p["sample"] == 200001].set_index("cbsa")
    m = cm.set_index("cbsa").join(s["pop"].rename("pums_pop"), how="inner").dropna(subset=["pop_sf1_0"])
    ratio = m.pums_pop / m.pop_sf1_0
    out["G5_pop_ratio_2000"] = dict(n=len(m), median=float(ratio.median()), p05=float(ratio.quantile(0.05)),
                                    p95=float(ratio.quantile(0.95)), min=float(ratio.min()), max=float(ratio.max()))
    (DERIVED / "pums_gates.json").write_text(json.dumps(out, indent=1))
    print(json.dumps(out, indent=1))
    for tag in ("G3_2000", "G4_2010"):
        if out[tag]["weighted_corr"] < 0.95 or abs(out[tag]["weighted_mean_gap_min"]) > 0.5:
            raise SystemExit(f"[BLOCKED] {tag} failed: {out[tag]}")


if __name__ == "__main__":
    main()
