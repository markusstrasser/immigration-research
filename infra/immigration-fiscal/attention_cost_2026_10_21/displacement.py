"""Agenda displacement test (pre-registered in RESULT.md Append 2).

Do years with a higher immigration share of the agenda show lower housing and family-policy shares
than share arithmetic implies, beyond a quadratic trend?

Data (Comparative Agendas Project, minio.la.utexas.edu/compagendas/datasetfiles/):
  US Congressional Hearings 21.7 (main), US Public Laws 20.1 (robustness),
  Netherlands parliamentary questions 3QS03102024 (Europe; the one CAP agenda series with
  an immigration code over 30+ years whose file was linked; UK PMQs cover only 1997-2008).
Codes: immigration = CAP major 9; housing = major 14; family = subtopics 1302, 1308, 1208.
Spec: share_k = a + b*imm + c1*t + c2*t^2, OLS, Newey-West SE (2 lags). Robustness: first
differences; imm lagged one year; adding log total items. Benchmark: b0 = -mean(share_k)/(1-mean(imm)).
Writes derived/displacement.csv.

Run: uv run --no-project python3 infra/immigration-fiscal/attention_cost_2026_10_21/displacement.py
"""
import csv
import pathlib
import urllib.request

import numpy as np
import pandas as pd

HERE = pathlib.Path(__file__).resolve().parent
CACHE = HERE / "_cache"
OUT = HERE / "derived" / "displacement.csv"
BASE = "https://minio.la.utexas.edu/compagendas/datasetfiles/"
SOURCES = {
    "us_hearings": ("US-Legislative_congressional_hearings-21.7%20%281%29.csv", "us_hearings_21.7.csv", (1946, 2020)),
    "us_public_laws": ("US-Legislative-public_laws_20.1_8.csv", "us_public_laws_20.1.csv", (1948, 2022)),
    "nl_questions": ("3QS03102024.csv", "nl_questions_2024.csv", (1945, 2024)),
}
# Hearings: the codebook warns the last CIS year is incomplete, so 2021 is dropped.
IMM, HOUSING, FAMILY = 9, 14, (1302, 1308, 1208)
NW_LAGS = 2


def load(name):
    remote, local, (y0, y1) = SOURCES[name]
    path = CACHE / local
    if not path.exists():
        CACHE.mkdir(exist_ok=True)
        urllib.request.urlretrieve(BASE + remote, path)
    d = pd.read_csv(path, encoding="latin-1", low_memory=False, usecols=lambda c: c in ("year", "majortopic", "subtopic"))
    d["year"] = pd.to_numeric(d["year"], errors="coerce")
    d = d[d["year"].between(y0, y1)].copy()
    d["majortopic"] = pd.to_numeric(d["majortopic"], errors="coerce")
    d["subtopic"] = pd.to_numeric(d["subtopic"], errors="coerce")
    g = d.groupby("year")
    s = pd.DataFrame({
        "total": g.size(),
        "imm": g["majortopic"].apply(lambda x: (x == IMM).mean()),
        "housing": g["majortopic"].apply(lambda x: (x == HOUSING).mean()),
        "family": g["subtopic"].apply(lambda x: x.isin(FAMILY).mean()),
    })
    return s.reindex(range(y0, y1 + 1)).dropna()


def ols_nw(y, X, lags=NW_LAGS):
    beta, *_ = np.linalg.lstsq(X, y, rcond=None)
    u = y - X @ beta
    n = len(y)
    xu = X * u[:, None]
    S = xu.T @ xu
    for L in range(1, lags + 1):
        w = 1 - L / (lags + 1)
        G = xu[L:].T @ xu[:-L]
        S += w * (G + G.T)
    XtX_inv = np.linalg.inv(X.T @ X)
    V = XtX_inv @ S @ XtX_inv * n / (n - X.shape[1])
    return beta, np.sqrt(np.diag(V))


def fit(s, k, spec):
    t = (s.index.values - s.index.values.mean()) / 10.0
    if spec == "levels_quadtrend":
        y, x, extra = s[k].values, s["imm"].values, [t, t**2]
    elif spec == "first_diff":
        y, x, extra = np.diff(s[k].values), np.diff(s["imm"].values), []
    elif spec == "lag1_quadtrend":
        y, x, extra = s[k].values[1:], s["imm"].values[:-1], [t[1:], t[1:] ** 2]
    elif spec == "levels_quadtrend_logtotal":
        y, x, extra = s[k].values, s["imm"].values, [t, t**2, np.log(s["total"].values)]
    X = np.column_stack([np.ones(len(y)), x] + extra)
    beta, se = ols_nw(y, X)
    return beta[1], se[1], len(y)


def main():
    rows = []
    for name in SOURCES:
        s = load(name)
        for k in ("housing", "family"):
            bench = -s[k].mean() / (1 - s["imm"].mean())
            for spec in ("levels_quadtrend", "first_diff", "lag1_quadtrend", "levels_quadtrend_logtotal"):
                b, se, n = fit(s, k, spec)
                rows.append([name, k, spec, n, f"{s.index.min()}-{s.index.max()}", f"{s['imm'].mean():.5f}",
                             f"{s['imm'].std():.5f}", f"{s[k].mean():.5f}", f"{b:.4f}", f"{se:.4f}",
                             f"{bench:.4f}", f"{b - bench:.4f}", f"{(b - bench) / se:.2f}"])
    OUT.parent.mkdir(exist_ok=True)
    with OUT.open("w", newline="") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(["dataset", "topic", "spec", "n_years", "years", "imm_mean", "imm_sd", "topic_mean",
                    "b", "se_nw2", "mechanical_benchmark", "excess", "excess_t"])
        w.writerows(rows)
    print(f"  ✓ wrote {OUT.relative_to(HERE)} ({len(rows)} rows)")


if __name__ == "__main__":
    main()
