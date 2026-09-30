"""Render the two annual fiscal distributions; all weights refer to residents.

Run: uv run --no-project --with matplotlib python3 {lane}/plot.py
"""
from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter, PercentFormatter
import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
COLORS = {"white": "#286b8b", "mexican": "#b96936"}
LABELS = {"white": "White reference", "mexican": "Mexican origin"}
BACKGROUND = "#fcfbf8"
XMIN, XMAX = -50_000, 60_000
BINS = np.arange(XMIN, XMAX + 2_000, 2_000)


def survival(x, w, thresholds):
    order = np.argsort(x, kind="stable")
    sx, sw = x[order], w[order]
    c = np.r_[0, np.cumsum(sw)]
    return (c[-1] - c[np.searchsorted(sx, thresholds, side="right")]) / c[-1]


def style(ax):
    ax.set_facecolor(BACKGROUND)
    ax.spines[["top", "right", "left"]].set_visible(False)
    ax.spines["bottom"].set_color("#c7c5bf")
    ax.tick_params(axis="both", length=0, pad=7, labelcolor="#4d4d49")
    ax.grid(axis="y", color="#e6e4df", lw=.6, zorder=0)
    ax.set_axisbelow(True)
    ax.xaxis.set_major_formatter(FuncFormatter(lambda x, _: "0" if x == 0 else f"{x / 1000:+.0f}k"))
    ax.axvline(0, color="#363b3d", lw=1.1, zorder=4)
    ax.set_xlim(XMIN, XMAX)


def save(fig, out, name):
    for ext in ("png", "svg", "pdf"):
        fig.savefig(out / f"{name}.{ext}", dpi=170, facecolor=BACKGROUND,
                    metadata={"Creator": "Annual fiscal distribution comparison"})
    plt.close(fig)


def main(out, derived):
    h = pd.read_parquet(HERE / "_cache/households.parquet")
    s = pd.read_csv(HERE / "derived/shares.csv").set_index(["group", "end"])
    out.mkdir(parents=True, exist_ok=True)
    derived.mkdir(parents=True, exist_ok=True)
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 11, "axes.titleweight": "bold",
                         "pdf.fonttype": 42, "svg.fonttype": "none", "text.parse_math": False})
    ranges = {g: f"{100 * s.loc[g, 'share_residents_positive'].min():.0f}–"
                 f"{100 * s.loc[g, 'share_residents_positive'].max():.0f}%" for g in COLORS}
    hist_rows, curve_rows = [], []
    fig, axes = plt.subplots(2, 2, figsize=(13.6, 8.4), sharex=True, sharey=True,
                             gridspec_kw={"hspace": .39, "wspace": .15})
    fig.patch.set_facecolor(BACKGROUND)
    fig.subplots_adjust(left=.075, right=.96, bottom=.24, top=.755)
    fig.text(.075, .95, f"Net-contributor households contain {ranges['white']} of white residents\n"
             f"and {ranges['mexican']} of Mexican-origin residents",
             fontsize=19, weight="bold", color="#202a30", va="top")
    fig.text(.075, .825, "Annual modeled household balance per group member · 2024 dollars · full allocation with pension accrual",
             fontsize=11, color="#60625e")
    for row, group in enumerate(("white", "mexican")):
        for col, end in enumerate(("low", "high")):
            ax = axes[row, col]
            z = h[(h.group == group) & (h.end == end)]
            x, w = z.net_per_member.to_numpy(), z.resident_weight.to_numpy()
            counts, _ = np.histogram(x, bins=BINS, weights=w)
            mass = counts / w.sum()
            below, above = float(w[x < XMIN].sum() / w.sum()), float(w[x > XMAX].sum() / w.sum())
            if not np.isclose(mass.sum() + below + above, 1, atol=1e-12):
                raise ValueError("[BLOCKED] histogram loses probability mass")
            ax.bar(BINS[:-1], mass, width=np.diff(BINS), align="edge", color=COLORS[group],
                   alpha=.82, edgecolor=BACKGROUND, linewidth=.4, zorder=2)
            style(ax)
            ax.yaxis.set_major_formatter(PercentFormatter(1, decimals=0))
            share = float(s.loc[(group, end), "share_residents_positive"])
            if abs(survival(x, w, np.array([0.]))[0] - share) > 1e-12:
                raise ValueError("[BLOCKED] plotted positive share differs from summary")
            ax.set_title(f"{LABELS[group]}  ·  {'Lower' if end == 'low' else 'Higher'}-cost setting",
                         loc="left", fontsize=12, color=COLORS[group], pad=13)
            ax.text(.97, .94, f"{share:.1%} net positive", transform=ax.transAxes,
                    ha="right", va="top", weight="bold", fontsize=14, color=COLORS[group])
            median = float(s.loc[(group, end), "median"])
            median_label = f"{'−' if median < 0 else '+' if median > 0 else ''}${abs(median):,.0f}"
            ax.text(.97, .77, f"Median: {median_label}",
                    transform=ax.transAxes, ha="right", va="top", fontsize=10, color="#535652")
            ax.text(.02, -.19, f"Outside view: {below:.2%} below −$50k; {above:.2%} above +$60k",
                    transform=ax.transAxes, fontsize=8.5, color="#666964")
            if col == 0:
                ax.set_ylabel("Residents per $2,000 bin", fontsize=10)
            for lo, hi, p in zip(BINS[:-1], BINS[1:], mass):
                hist_rows.append(dict(group=group, end=end, lower=lo, upper=hi, share=p,
                                      below_view=below, above_view=above))
    fig.text(.52, .135, "Net cost to others  ←                         Annual balance per member ($)                         →  Net contribution",
             ha="center", fontsize=11, color="#343d40")
    notes = ("Each resident inherits the balance per member of their group's part of the household; weights count residents, not households.\n"
             "White reference: US-born non-Hispanic whites with US-born parents (rough comparator). Mexican origin: all generations. Actual ages.\n"
             "The two settings are not confidence bounds. Medical and justice costs are allocated, not individual observed bills.\n"
             "Source: CPS ASEC 2025 / MEPS 2024 and the repository's September 29 annual account. This is not a lifetime distribution.")
    fig.text(.075, .085, notes, fontsize=8.3, color="#686b66", va="top", linespacing=1.55)
    save(fig, out, "histograms")

    fig, ax = plt.subplots(figsize=(13.6, 7.4))
    fig.patch.set_facecolor(BACKGROUND)
    fig.subplots_adjust(left=.09, right=.96, bottom=.27, top=.76)
    fig.text(.09, .93, "How many residents live above each fiscal contribution threshold?",
             fontsize=21, weight="bold", color="#202a30")
    fig.text(.09, .865, f"At $0, the curves give the net-positive shares: whites {ranges['white']}; Mexican origin {ranges['mexican']}.",
             fontsize=13, color="#505b5e")
    xs = np.sort(np.unique(np.r_[np.linspace(XMIN, XMAX, 801), 0]))
    style(ax)
    for group in ("white", "mexican"):
        ys = []
        for end in ("low", "high"):
            z = h[(h.group == group) & (h.end == end)]
            y = survival(z.net_per_member.to_numpy(), z.resident_weight.to_numpy(), xs)
            ys.append(y)
            if np.any(np.diff(y) > 1e-12) or np.any((y < -1e-12) | (y > 1 + 1e-12)):
                raise ValueError("[BLOCKED] invalid exceedance curve")
            ax.plot(xs, y, color=COLORS[group], lw=2, linestyle="-" if end == "low" else "--",
                    label=f"{LABELS[group]} · {'lower' if end == 'low' else 'higher'}-cost setting")
            ax.scatter([0], [s.loc[(group, end), "share_residents_positive"]], color=COLORS[group], s=35, zorder=5)
            curve_rows.extend(dict(group=group, end=end, threshold=x, share_above=p) for x, p in zip(xs, y))
        ax.fill_between(xs, np.minimum(*ys), np.maximum(*ys), color=COLORS[group], alpha=.1)
    ax.set_ylim(0, 1)
    ax.yaxis.set_major_formatter(PercentFormatter(1, decimals=0))
    ax.set_ylabel("Share of residents above threshold")
    ax.set_xlabel("Annual net contribution per household member ($)", labelpad=14)
    ax.legend(frameon=False, fontsize=10, loc="upper right")
    ax.text(1400, .365, "Net-positive cutoff", color="#353f41", fontsize=10)
    fig.text(.09, .14, "Read: at +$10k, the curve shows the share living in households contributing more than $10,000 per member annually.",
             fontsize=10, color="#38494e")
    fig.text(.09, .09, notes, fontsize=8.3, color="#686b66", va="top", linespacing=1.55)
    save(fig, out, "thresholds")
    pd.DataFrame(hist_rows).to_csv(derived / "histogram_bins.csv", index=False, lineterminator="\n")
    pd.DataFrame(curve_rows).to_csv(derived / "threshold_curves.csv", index=False, lineterminator="\n")
    print(f"Wrote figures to {out}; histogram mass and threshold gates passed.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out-dir", type=Path, default=HERE / "plots")
    parser.add_argument("--data-out-dir", type=Path, default=HERE / "derived")
    args = parser.parse_args()
    main(args.out_dir, args.data_out_dir)
