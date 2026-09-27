#!/usr/bin/env python3
"""Task 5: the selection curve p_selected -> p_G1 -> p_G2 -> p_G3, and its figure.

Links and their status:
  p_sel -> p_G1   cross-origin WLS on the CPS origin table (measured, descriptive)
  p_G1  -> p_G2   cross-origin WLS on the CPS origin table (measured, descriptive)
  p_G2  -> p_G3   [MODEL] cross-origin WLS on the GSS origin table (measured on mostly European
                  origins plus Mexico and Japan), applied to CPS groups; and the Borjas rule
                  p_G3 = 50 + beta (p_G2 - 50), beta 0.46-0.53, read from Borjas (1994) GSS
Intervals come from resampling origins in each table independently (2,000 draws).

Inputs: derived/origin_curve.csv, derived/gss_origin_generations.csv.
Outputs: derived/curve_projection.csv, derived/selection_curve.png.

Run: uv run --no-project --with matplotlib python3 \
       infra/immigration-fiscal/selection_curve_2026_09_27/curve.py
"""
from __future__ import annotations

import csv
from pathlib import Path

import numpy as np
import pandas as pd

LANE = Path(__file__).resolve().parent
DER = LANE / "derived"
SEED = 20260927
NBOOT = 2000
MIN_G1 = 100
BORJAS = (0.46, 0.53)   # Borjas 1994 (NBER w4641) p.21: G2->G3 mean convergence, log wage .46, education .53
FOCUS = ["India", "Mexico", "China", "Philippines", "Vietnam", "Nigeria", "Korea", "Cuba", "El Salvador"]


def wls(x, y, w):
    X = np.column_stack([np.ones_like(x), x])
    return np.linalg.solve(X.T @ (X * w[:, None]), X.T @ (w * y))


def boot(x, y, w, rng):
    b = wls(x, y, w)
    d = np.array([wls(x[i], y[i], w[i]) for i in (rng.integers(0, len(x), len(x)) for _ in range(NBOOT))])
    return b, d


def main() -> int:
    rng = np.random.default_rng(SEED)
    o = pd.read_csv(DER / "origin_curve.csv")
    o = o[(o.spec == "all") & (o.n_g1 >= MIN_G1)]
    g = pd.read_csv(DER / "gss_origin_generations.csv")
    g = g[(g.arm == "granborn_1plus")]

    links = {}
    for out, (x, y) in {"sel_g1": ("g1_p_sel", "g1_p_edu"), "g1_g2_edu": ("g1_p_edu", "g2_p_edu"),
                        "g1_g2_earn": ("g1_p_earn", "g2_p_earn")}.items():
        t = o.dropna(subset=[x, y])
        links[out] = boot(t[x].to_numpy(), t[y].to_numpy(), t.n_g2.to_numpy(float), rng)
    for out, var in {"g2_g3_edu": "p_edu", "g2_g3_inc": "p_inc"}.items():
        t = g[(g[f"n_g2_{var}"] >= 30) & (g[f"n_g3_{var}"] >= 40)].dropna(subset=[f"g2_{var}", f"g3_{var}"])
        links[out] = boot(t[f"g2_{var}"].to_numpy(), t[f"g3_{var}"].to_numpy(),
                          t[f"n_g3_{var}"].to_numpy(float), rng)

    def ci(v):
        return float(np.percentile(v, 2.5)), float(np.percentile(v, 97.5))

    rows = []
    # 1. the generic curve along the selection axis
    for p_sel in range(60, 100, 5):   # observed origin means span 58-96
        b1, d1 = links["sel_g1"]
        b2, d2 = links["g1_g2_edu"]
        b3, d3 = links["g2_g3_edu"]
        g1 = b1[0] + b1[1] * p_sel
        g1d = d1[:, 0] + d1[:, 1] * p_sel
        g2 = b2[0] + b2[1] * g1
        g2d = d2[:, 0] + d2[:, 1] * g1d
        g3 = b3[0] + b3[1] * g2
        g3d = d3[:, 0] + d3[:, 1] * g2d
        rows.append({"row": "generic_curve", "group": f"p_sel={p_sel}", "outcome": "education",
                     "p_sel": p_sel, "p_g1": g1, "p_g1_lo": ci(g1d)[0], "p_g1_hi": ci(g1d)[1],
                     "p_g2": g2, "p_g2_lo": ci(g2d)[0], "p_g2_hi": ci(g2d)[1],
                     "p_g3_model": g3, "p_g3_lo": ci(g3d)[0], "p_g3_hi": ci(g3d)[1],
                     "p_g3_borjas_b046": 50 + BORJAS[0] * (g2 - 50), "p_g3_borjas_b053": 50 + BORJAS[1] * (g2 - 50),
                     "status": "p_g1, p_g2 fitted (measured links); p_g3 MODEL"})
    # 2. named origins: observed points, line-predicted G2, projected G3 from the OBSERVED G2
    for name in FOCUS:
        r = o[o.origin == name]
        if r.empty:
            continue
        r = r.iloc[0]
        for outcome, g1c, g2c, l2, l3 in (("education", "g1_p_edu", "g2_p_edu", "g1_g2_edu", "g2_g3_edu"),
                                          ("earnings", "g1_p_earn", "g2_p_earn", "g1_g2_earn", "g2_g3_inc")):
            b2, d2 = links[l2]
            b3, d3 = links[l3]
            g2hat = b2[0] + b2[1] * r[g1c]
            g2hatd = d2[:, 0] + d2[:, 1] * r[g1c]
            g3 = b3[0] + b3[1] * r[g2c]
            g3d = d3[:, 0] + d3[:, 1] * r[g2c]
            rows.append({"row": "origin", "group": name, "outcome": outcome,
                         "p_sel": r.g1_p_sel, "p_g1": r[g1c], "p_g1_lo": np.nan, "p_g1_hi": np.nan,
                         "p_g2": r[g2c], "p_g2_lo": g2hat, "p_g2_hi": np.nan,
                         "p_g3_model": g3, "p_g3_lo": ci(g3d)[0], "p_g3_hi": ci(g3d)[1],
                         "p_g3_borjas_b046": 50 + BORJAS[0] * (r[g2c] - 50),
                         "p_g3_borjas_b053": 50 + BORJAS[1] * (r[g2c] - 50),
                         "status": ("p_sel, p_g1, p_g2 observed (p_g2_lo holds the line-predicted G2); "
                                    "p_g3 MODEL from the observed G2" + (" (GSS income link applied to CPS wage "
                                    "percentiles)" if outcome == "earnings" else ""))})
    link_rows = []
    for k, (b, d) in links.items():
        link_rows.append({"link": k, "intercept": b[0], "slope": b[1],
                          "slope_lo": ci(d[:, 1])[0], "slope_hi": ci(d[:, 1])[1]})
    with open(DER / "curve_projection.csv", "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0]), lineterminator="\n")
        w.writeheader()
        for r in rows:
            w.writerow({k: (f"{v:.4g}" if isinstance(v, float) else v) for k, v in r.items()})
    pd.DataFrame(link_rows).to_csv(DER / "curve_links.csv", index=False, float_format="%.4g",
                                   lineterminator="\n")
    print(pd.DataFrame(link_rows).round(3).to_string())
    print(pd.DataFrame(rows).round(1).to_string())
    figure(o, links, pd.DataFrame(rows))
    return 0


def figure(o: pd.DataFrame, links: dict, proj: pd.DataFrame) -> None:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    fig, axes = plt.subplots(1, 3, figsize=(17, 5.8))
    ink, grey, orange, blue = "#222222", "#9a9a9a", "#d9822b", "#3b6fb6"

    # (a) G1 -> G2
    ax = axes[0]
    t = o.dropna(subset=["g1_p_edu", "g2_p_edu"])
    s = 8 + 400 * np.sqrt(t.n_g2 / t.n_g2.max())
    ax.scatter(t.g1_p_edu, t.g2_p_edu, s=s, facecolor="none", edgecolor=grey, linewidth=0.8)
    b, d = links["g1_g2_edu"]
    xs = np.linspace(10, 80, 50)
    ax.plot(xs, b[0] + b[1] * xs, color=ink, lw=1.2,
            label=f"fit across origins, slope {b[1]:.2f} "
                  f"[{np.percentile(d[:, 1], 2.5):.2f}, {np.percentile(d[:, 1], 97.5):.2f}]")
    ax.plot([10, 80], [10, 80], color=grey, lw=0.8, ls=":", label="no regression (45°)")
    for nm in FOCUS:
        r = t[t.origin == nm]
        if r.empty:
            continue
        r = r.iloc[0]
        col = orange if nm == "Mexico" else blue if nm == "India" else ink
        ax.scatter([r.g1_p_edu], [r.g2_p_edu], s=30, color=col, zorder=3)
        ax.annotate(nm, (r.g1_p_edu, r.g2_p_edu), xytext=(4, 3), textcoords="offset points", fontsize=8, color=col)
    ax.axhline(50, color=grey, lw=0.5)
    ax.axvline(50, color=grey, lw=0.5)
    ax.set_xlabel("Immigrant generation (G1): mean education percentile\nin the US third-plus-generation white distribution")
    ax.set_ylabel("US-born children (G2): mean education percentile")
    ax.set_title("(a) G1 to G2 across 78 parental origins, CPS 1994-2025", fontsize=10, loc="left")
    ax.legend(fontsize=8, frameon=False, loc="upper left")

    # (b) origin selection -> G1 and G2
    ax = axes[1]
    t = o.dropna(subset=["g1_p_sel", "g1_p_edu", "g2_p_edu"])
    ax.scatter(t.g1_p_sel, t.g1_p_edu, s=12, color=grey, label="G1 US percentile")
    ax.scatter(t.g1_p_sel, t.g2_p_edu, s=12, facecolor="none", edgecolor=ink, label="G2 US percentile")
    for nm in ("India", "Mexico"):
        r = t[t.origin == nm].iloc[0]
        col = orange if nm == "Mexico" else blue
        ax.annotate("", xy=(r.g1_p_sel, r.g2_p_edu), xytext=(r.g1_p_sel, r.g1_p_edu),
                    arrowprops=dict(arrowstyle="->", color=col, lw=1.2))
        ax.annotate(nm, (r.g1_p_sel, r.g1_p_edu), xytext=(-40, 0), textcoords="offset points", fontsize=8, color=col)
    ax.axhline(50, color=grey, lw=0.5)
    ax.set_xlabel("How selected: G1 mean percentile in the ORIGIN country's schooling\n"
                  "distribution, same birth cohort (Barro-Lee v3; WIC 2020 where absent)")
    ax.set_ylabel("Mean education percentile in the US white distribution")
    ax.set_title("(b) Selection within origin vs position in the US", fontsize=10, loc="left")
    ax.legend(fontsize=8, frameon=False, loc="upper left")

    # (c) the curve
    ax = axes[2]
    xs = [0, 1, 2, 3]
    for nm, col in (("India", blue), ("Mexico", orange)):
        r = proj[(proj.group == nm) & (proj.outcome == "education")].iloc[0]
        ax.plot(xs[1:3], [r.p_g1, r.p_g2], color=col, lw=1.8, marker="o", label=f"{nm}, observed")
        ax.plot(xs[2:4], [r.p_g2, r.p_g3_model], color=col, lw=1.4, ls="--", marker="o", mfc="white")
        ax.plot([3, 3], [r.p_g3_lo, r.p_g3_hi], color=col, lw=4, alpha=0.3)
        ax.plot([3.08, 3.08], [r.p_g3_borjas_b046, r.p_g3_borjas_b053], color=col, lw=2, alpha=0.9)
        ax.annotate(f"{r.p_sel:.0f}", (0, r.p_sel), xytext=(6, -3), textcoords="offset points", fontsize=8, color=col)
        ax.scatter([0], [r.p_sel], color=col, marker="s", s=25)
        for xv, yv in ((1, r.p_g1), (2, r.p_g2), (3, r.p_g3_model)):
            ax.annotate(f"{yv:.0f}", (xv, yv), xytext=(6, 4), textcoords="offset points", fontsize=8, color=col)
    ax.axhline(50, color=grey, lw=0.6)
    ax.text(3.35, 50.5, "white\nmedian", fontsize=7, color=grey)
    ax.set_xticks(xs, ["selection\n(origin pctile)", "G1\n(US pctile)", "G2\n(US pctile)", "G3\n[MODEL]"])
    ax.set_xlim(-0.3, 3.7)
    ax.set_ylim(0, 100)
    ax.set_ylabel("Mean education percentile")
    ax.set_title("(c) The curve: dashed = projected G3 from observed G2\n"
                 "wide bar: GSS cross-origin interval; thin bar: Borjas 0.46-0.53", fontsize=10, loc="left")
    ax.legend(fontsize=8, frameon=False, loc="lower right")
    fig.tight_layout()
    fig.savefig(DER / "selection_curve.png", dpi=130)


if __name__ == "__main__":
    raise SystemExit(main())
