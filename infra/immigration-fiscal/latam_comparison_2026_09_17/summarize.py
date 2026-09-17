#!/usr/bin/env python3
"""Render the full prespecified country roster; never select only winners."""
from pathlib import Path
from statistics import NormalDist
import json
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from analyze import COUNTRIES, PRIMARY

ROOT = Path(__file__).resolve().parent / "derived"
levels = pd.read_csv(ROOT / "levels.csv")
contrasts = pd.read_csv(ROOT / "contrasts.csv")
selection = (levels.scope == "age25_54") & (levels.standard == "age_sex_standardized")
ll = levels.loc[selection]
cc = contrasts.loc[(contrasts.scope == "age25_54") &
                   (contrasts.standard == "age_sex_standardized") &
                   (contrasts.benchmark == "white_us_parents")]

lines = ["# CPS ASEC 2022–2026: prime-age economic comparison", "",
         "Civilian household adults 25–54; pooled person-period estimates, standardized to the 2025 established-white age/sex distribution. Earnings include nonworkers and losses. Income years 2021–2025. All intervals use the conservative annual-block covariance bound.", "",
         "Main benchmark: US-born non-Hispanic white-alone adults with both parents US-born. Neither the benchmark nor country origin measures DNA.", ""]
for generation in ["benchmarks", "g1", "g2"]:
    lines += [f"## {generation}", "",
              "| Origin | Records / distinct IDs | BA+ | Employed | Poverty | Mean earnings (2025 USD) | Earnings / white benchmark (95% CI) |",
              "|---|---:|---:|---:|---:|---:|---:|"]
    groups = ["white_us_parents", "all_us_parents", "white_cps_native_parents"] if generation == "benchmarks" else [f"{generation}_{c}" for c in COUNTRIES.values()] + [f"{generation}_LATAM"]
    for group in groups:
        subset = ll.loc[ll.group == group].set_index("metric")
        if subset.empty:
            lines.append(f"| {group} | Unavailable | | | | | |")
            continue
        n, u = subset.iloc[0][["n_person_periods", "n_distinct_ids"]].astype(int)
        values = []
        for metric in ["ba", "employment", "poverty", "earnings_2025usd"]:
            if metric not in subset.index:
                values.append("Unavailable")
            else:
                value = subset.loc[metric, "estimate"]
                values.append(f"${value:,.0f}" if metric == "earnings_2025usd" else f"{100 * value:.1f}%")
        earnings = cc.loc[(cc.group == group) & (cc.metric == "earnings_2025usd")]
        ratio = "Unavailable" if earnings.empty else f"{earnings.iloc[0].estimate:.2f} [{earnings.iloc[0].ci95_low:.2f}, {earnings.iloc[0].ci95_high:.2f}]"
        lines.append(f"| {group.replace(generation + '_', '')} | {n:,} / {u:,} | " + " | ".join(values) + f" | {ratio} |")
    lines += ["", "Records repeat some people across adjacent years; distinct IDs are not a validated longitudinal sample. Unavailable means a denominator failed, not poor performance.", ""]

margin_rows = []
z = NormalDist().inv_cdf(1 - .05 / len(COUNTRIES))
for (scope, standard, group, benchmark), rows in contrasts[contrasts.metric.isin(PRIMARY)].groupby(["scope", "standard", "group", "benchmark"]):
    if group not in {f"{g}_{c}" for g in ["g1", "g2"] for c in COUNTRIES.values()}:
        continue
    for label, rate_margin, earnings_margin in [("strict", .03, .05), ("primary", .05, .10), ("loose", .075, .15)]:
        passes = []
        for row in rows.itertuples():
            earnings = row.metric == "earnings_2025usd"
            direction = -1 if row.metric == "poverty" else 1
            center = 1 if earnings else 0
            margin = earnings_margin if earnings else rate_margin
            passes.append(not row.sparse_guard and not row.zero_event_guard and direction * (row.estimate - center) - z * row.se_upper >= -margin)
        margin_rows.append(dict(scope=scope, standard=standard, group=group, benchmark=benchmark,
                                margin=label, all_four_pass=len(passes) == 4 and all(passes)))
pd.DataFrame(margin_rows).to_csv(ROOT / "margin_sensitivity.csv", index=False)
(ROOT / "RESULTS.md").write_text("\n".join(lines) + "\n")

# All 20 primary countries, source roster order; no favorable-result filtering.
metrics = ["ba", "employment", "poverty", "earnings_2025usd"]
titles = ["BA+ gap (pp)", "Employment gap (pp)", "Poverty gap (pp)", "Earnings ratio"]
fig, axes = plt.subplots(1, 4, figsize=(15, 10), sharey=True)
for ax, metric, title in zip(axes, metrics, titles):
    earnings = metric == "earnings_2025usd"
    center, margin, scale = (1, .1, 1) if earnings else (0, 5, 100)
    ax.axvspan(center - margin, center + margin, color="#eceff1", zorder=0)
    ax.axvline(center, color="#56616a", lw=.8)
    for y, country in enumerate(COUNTRIES.values()):
        row = cc.loc[(cc.group == f"g2_{country}") & (cc.metric == metric)]
        if row.empty:
            ax.text(center, y, "unavailable", fontsize=7, ha="center", color="#777777")
            continue
        r = row.iloc[0]
        color = "#888888" if r.sparse_guard or r.zero_event_guard else "#205873"
        ax.errorbar(r.estimate * scale, y, xerr=1.96 * r.se_upper * scale,
                    fmt="o", ms=4, capsize=2, color=color, lw=1)
    ax.set_title(title, fontsize=11, loc="left")
    ax.grid(axis="y", color="#eeeeee", lw=.6)
    ax.spines[["top", "right", "left"]].set_visible(False)
    ax.tick_params(axis="y", length=0)
axes[0].set_yticks(range(len(COUNTRIES)), list(COUNTRIES.values()), fontsize=10)
axes[0].invert_yaxis()
fig.suptitle("US-born children of Latin American immigrants: economic outcomes", x=.02, ha="left", fontsize=17)
fig.text(.02, .927, "Compared with US-born non-Hispanic white adults with two US-born parents · ages 25–54", fontsize=11)
fig.text(.02, .036, "CPS ASEC 2022–26; fixed age/sex standardization. Points and conservative pointwise 95% sampling intervals.\nShading: ±5 pp or ±10%; analyst-defined closeness bands. Gray: sparse/zero-event guard. Lower poverty is favorable.\nEarnings include all adults, including nonworkers; these are economic descriptions, not fiscal, crime or genetic effects.", fontsize=9)
fig.subplots_adjust(left=.16, right=.98, top=.88, bottom=.14, wspace=.15)
fig.savefig(ROOT / "second_generation_comparison.png", dpi=180)
fig.savefig(ROOT / "second_generation_comparison.pdf")
plt.close(fig)
print("Rendered all 20 countries, both generations, benchmarks and margin sensitivities")
