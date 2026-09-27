"""Read-only generation diagnostics; origin bootstrap is not survey uncertainty."""
from pathlib import Path
import hashlib
import json
import re
import sys
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[3]
LANE = ROOT / "infra/immigration-fiscal/selection_curve_2026_09_27"
sys.path.insert(0, str(LANE))
import load  # noqa: E402

pins = {
    LANE / "_cache/frame.parquet": "59ef138b379b1670153ec4ebf6eeada1140dac68b7b68318a801d553379fd7d4",
    LANE / "derived/origin_curve.csv": "e07f3ffc7f8b7700e48ae40ec0ce45d4dbe9816bf7d8334f73015b175baaaddb",
    ROOT / "sources/immigration-fiscal/data/external/cps/cps_2ndgen.xml":
        "896a888b1d0dbc9ebf6525d0ca0e777142a7ae873041ac189f0f02efe6206705",
}
for p, expected in pins.items():
    assert hashlib.sha256(p.read_bytes()).hexdigest() == expected, f"[BLOCKED] changed input: {p}"
labels = load.ddi_labels("YRIMMIG")
df = pd.read_parquet(LANE / "_cache/frame.parquet")
origins = pd.read_csv(LANE / "derived/origin_curve.csv")
origins = origins[origins.spec.eq("all") & origins.n_g1.ge(100)]
assert len(origins) == 78


def fit(x, y, w):
    design = np.c_[np.ones(len(x)), x]
    return np.linalg.lstsq(design * np.sqrt(w[:, None]), y * np.sqrt(w), rcond=None)[0]


rng = np.random.default_rng(20260927)
slopes = {}
for outcome in ["edu", "earn"]:
    x = origins["g1_p_" + outcome].to_numpy()
    y = origins["g2_p_" + outcome].to_numpy()
    w = origins.n_g2.to_numpy()

    def difference(ix):
        xi, yi, wi = x[ix], y[ix], w[ix]
        low = xi < 50
        assert low.sum() > 2 and (~low).sum() > 2
        return fit(xi[low], yi[low], wi[low])[1] - fit(xi[~low], yi[~low], wi[~low])[1]

    draws = np.array([difference(rng.choice(len(x), len(x), replace=True)) for _ in range(10000)])
    slopes[outcome] = {"low_minus_high": float(difference(np.arange(len(x)))),
                       "origin_bootstrap_95": np.quantile(draws, [.025, .975]).tolist()}
bounds = {k: [int(n) for n in re.findall(r"\d{4}", v)] for k, v in labels.items() if k > 0}
lo = {k: (v[0] if len(v) > 1 or k != 1 else 1900) for k, v in bounds.items()}
hi = {k: v[-1] for k, v in bounds.items()}
g1 = df[df.nativity.eq(5)].copy()
assert (g1.yrimmig.isin(bounds) | g1.yrimmig.eq(0)).all(), "Unexpected G1 arrival code"
g1["arrival_min"] = g1.yrimmig.map(lo) - (g1.year - g1.age)
g1["arrival_max"] = g1.yrimmig.map(hi) - (g1.year - g1.age - 1)
arrival = {}
for name, bpl in [("all", None), ("Mexico", 20000), ("India", 52100), ("China", 50000)]:
    s = g1 if bpl is None else g1[g1.bpl.eq(bpl)]
    arrival[name] = {"records": len(s),
                     "definitely_under18": float(np.average(s.arrival_max < 18, weights=s.w)),
                     "possibly_under18": float(np.average((s.arrival_min < 18) | s.yrimmig.eq(0), weights=s.w)),
                     "unknown_arrival_share": float(np.average(s.yrimmig.eq(0), weights=s.w))}
q, hispanic_retention, mexican_retention = .402, .843675, .835009
mixed_couples = 2*q/(1+q)
print(json.dumps({"slope_diagnostics": slopes, "weighted_pooled_records_arrival_bounds": arrival,
                  "equal_fertility_two_couple_types_illustration_only": {
                      "person_outmarriage": q, "mixed_couple_share": mixed_couples,
                      "naive_hispanic_loss": q*(1-hispanic_retention),
                      "couple_hispanic_loss": mixed_couples*(1-hispanic_retention),
                      "couple_mexican_loss": mixed_couples*(1-mexican_retention)},
                  "source_sha256": {str(p.relative_to(ROOT)): h for p, h in pins.items()}}, indent=2))
