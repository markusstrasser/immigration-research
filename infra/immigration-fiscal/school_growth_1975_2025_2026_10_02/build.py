"""A partial, explicitly modeled school-demand reconstruction; see README.md."""
from pathlib import Path
import hashlib
import json

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import openpyxl

HERE = Path(__file__).resolve().parent
OUT = HERE / "derived"
YEARS = np.arange(1975, 2026)
COST_FILE = HERE.parent / "gen_ledger_extension_2026_09_16/census_assf_fy2024_summary_tables.xlsx"
BIRTH_FILE = HERE / "inputs/pew_births.csv"
# Source: Pew August 2025 report, printed p14. Counts are all under-18s,
# not enrolled pupils. Intermediate years and pre-1995 history are modeled.
CHILD_ANCHORS = {1995: 1.1e6, 2000: 1.4e6, 2007: 1.5e6,
                 2015: .7e6, 2021: .8e6, 2023: 1.5e6}
CASES = {
    "low": dict(public=.85, loss=.012, fertility=1.6, peak=32,
                early=.5, child_school_age=.65, child_2025=1.2e6),
    "central": dict(public=.90, loss=.005, fertility=2., peak=29,
                    early=1., child_school_age=13/18, child_2025=1.5e6),
    "high": dict(public=.95, loss=.002, fertility=2.4, peak=26,
                 early=1.5, child_school_age=.85, child_2025=1.8e6),
}


def births_input():
    source = pd.read_csv(BIRTH_FILE)
    assert len(source) == 34 and set(source.Year) == set(range(1990, 2024))
    series = source.set_index("Year").iloc[:, 0] * 1000
    assert series[1990] == 120000 and series[2023] == 300000
    # Only births through 2020 can be school-age by 2025. Later inputs
    # are retained as provenance, never extrapolated into the school count.
    return series.to_dict()


def descendant_births(parent_births, fertility, peak, loss):
    """Maternal-line recursion: each child has one mother, avoiding lineage overlap."""
    ages = np.arange(18, 41)
    weights = np.exp(-.5 * ((ages - peak) / 4.) ** 2)
    weights /= weights.sum()
    result = np.zeros(len(YEARS))
    for age, weight in zip(ages, weights):
        # Equal sex ratio; fertility applies per woman. Retention/survival
        # until motherhood is separate from her child's later retention.
        result[age:] += parent_births[:-age] * .5 * fertility * weight * (1-loss)**age
    return result


def pupils(births, public, loss):
    result = np.zeros(len(YEARS))
    for age in range(5, 18):
        result[age:] += births[:-age] * public * (1-loss)**age
    return result


def model(name, published, price):
    p = CASES[name]
    # Census's historical approximation: 200k net unauthorized immigrants
    # annually in 1975-80. Extending this through 1989 is an assumption.
    # Births/person is the 1990 Pew120k / Pew3.5m ratio, held constant early.
    births = np.array([published.get(int(y), 0.) for y in YEARS])
    before = YEARS < 1990
    births[before] = (YEARS[before]-1975) * 200000 * (120000/3500000) * p["early"]
    child_years = [1975, *CHILD_ANCHORS, 2025]
    child_values = [0., *CHILD_ANCHORS.values(), p["child_2025"]]
    immigrant_minors = np.interp(YEARS, child_years, child_values)
    immigrant_minors *= 1 + (p["early"]-1) * np.maximum(0, (1995-YEARS)/20)
    foreign_pupils = immigrant_minors * p["child_school_age"] * p["public"]
    usborn = pupils(births, p["public"], p["loss"])
    later = np.zeros(len(YEARS))
    next_births = births.copy()
    # G3 then G4 etc. Positive minimum motherhood age guarantees termination.
    for _ in range(len(YEARS)//18):
        next_births = descendant_births(next_births, p["fertility"], p["peak"], p["loss"])
        later += pupils(next_births, p["public"], p["loss"])
    total = foreign_pupils + usborn + later
    return pd.DataFrame(dict(year=YEARS, scenario=name,
                             births_to_unauthorized_mothers=births,
                             foreignborn_pupils=foreign_pupils,
                             usborn_children_pupils=usborn,
                             later_maternal_descendants_pupils=later,
                             total_pupils=total,
                             gross_operating_cost=total*price))


def verify(published, frames):
    # A single female/male-balanced cohort of100 must yield exactly90 pupil
    # places at each of13 school ages with90% enrollment and no attrition.
    cohort = np.zeros(len(YEARS)); cohort[0] = 100
    out = pupils(cohort, .9, 0.)
    assert np.all(out[5:18] == 90) and out.sum() == 1170
    children = descendant_births(cohort, 2., 29, 0.)
    assert np.isclose(children.sum(), 100) and not children[:18].any()
    assert abs(sum(v for y, v in published.items() if 2006 <= y <= 2023) - 5.07e6) < 60000
    for f in frames:
        assert np.isfinite(f.select_dtypes("number")).all().all()
        assert np.allclose(f.total_pupils, f.foreignborn_pupils + f.usborn_children_pupils + f.later_maternal_descendants_pupils)
        assert not f.loc[f.year < 1980, "usborn_children_pupils"].any()
        assert not f.loc[f.year < 1998, "later_maternal_descendants_pupils"].any()
    assert (frames[0].total_pupils <= frames[1].total_pupils + 1e-6).all()
    assert (frames[1].total_pupils <= frames[2].total_pupils + 1e-6).all()


def chart(frames, price):
    low, mid, high = frames
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 11,
                         "svg.hashsalt": "school-demand-20261002"})
    fig, ax = plt.subplots(figsize=(13, 8), facecolor="#faf9f5")
    ax.set_facecolor("#faf9f5")
    fig.subplots_adjust(left=.085, right=.84, bottom=.27, top=.77)
    fig.text(.085, .94, "School demand linked to unauthorized immigration", fontsize=23, weight="bold")
    fig.text(.085, .895, "1975–2025 • Partial reconstruction including children born in the U.S.", fontsize=14)
    fig.text(.085, .85, "Annual public-school pupils, millions  |  All curves are modeled", color="#555555")
    colors = ["#aaa9a4", "#347d99", "#80b9ad"]
    components = [mid.foreignborn_pupils, mid.usborn_children_pupils, mid.later_maternal_descendants_pupils]
    ax.stackplot(YEARS, *(v/1e6 for v in components), colors=colors, alpha=.95)
    ax.fill_between(YEARS, low.total_pupils/1e6, high.total_pupils/1e6,
                    facecolor="none", edgecolor="#313131", hatch="////", linewidth=.65, alpha=.28)
    ax.plot(YEARS, mid.total_pupils/1e6, color="#202020", linewidth=1.6)
    ax.axvspan(1975, 1990, color="white", alpha=.35)
    ax.axvline(1990, color="#777777", linestyle=":", linewidth=1)
    ax.axvline(2023, color="#777777", linestyle=":", linewidth=1)
    ax.text(1976, 5.9, "Early history:\nillustrative back-cast", color="#666666", fontsize=10)
    ax.text(1991, 5.9, "1990 onward: anchored to Pew’s\nannual birth estimates", color="#444444", fontsize=10)
    ax.set(xlim=(1975, 2025), ylim=(0, 6.5), xticks=[1975,1985,1995,2005,2015,2025])
    ax.set_yticks(np.arange(0, 7))
    ax.grid(axis="y", alpha=.17)
    ax.set_axisbelow(True)
    for spine in ("top", "right", "left"):
        ax.spines[spine].set_visible(False)
    ax.tick_params(axis="both", length=0, pad=8)
    ax.spines["bottom"].set_color("#bbbbbb")
    final = mid.iloc[-1]
    labels = ["Foreign-born children\ncurrently unauthorized", "U.S.-born children: mother\nunauthorized at birth", "Later descendants\nthrough U.S.-born mothers"]
    for x, color, label, values in zip([.085, .34, .61], colors, labels, components):
        fig.text(x, .205, "■", color=color, fontsize=18)
        fig.text(x+.022, .208, label + f"  ({values.iloc[-1]/1e6:.2f}m in 2025)", fontsize=10, va="top")
    ax.text(1.018, .74, f"2025 scenario\n{final.total_pupils/1e6:.1f} million pupils\n${final.gross_operating_cost/1e9:.0f}bn/year", transform=ax.transAxes,
            fontsize=13, weight="bold", linespacing=1.55)
    ax.text(1.018, .45, f"Sensitivity range\n{low.total_pupils.iloc[-1]/1e6:.1f}–{high.total_pupils.iloc[-1]/1e6:.1f}m pupils\n${low.gross_operating_cost.iloc[-1]/1e9:.0f}–{high.gross_operating_cost.iloc[-1]/1e9:.0f}bn/year\n(hatched band)", transform=ax.transAxes,
            fontsize=10, color="#555555", linespacing=1.55)
    notes = [
        "Gross operating cost at FY2024’s $17,619 per pupil throughout; excludes construction and does not subtract taxes.",
        "Partial maternal lineage: excludes births after legalization and descendants through U.S.-born fathers; not a full causal total.",
        "1975 is an assumed zero baseline, not an observed count. 2024–25 are scenarios. Band varies fertility, retention and enrollment; not a confidence interval.",
        "Sources: Pew (2026 births; 2025 child counts), Census FY2024 school finances. Model and assumptions: accompanying README."
    ]
    for i, line in enumerate(notes):
        fig.text(.085, .117-i*.026, line, fontsize=9, color="#555555")
    fig.savefig(OUT/"school_burden.png", dpi=180)
    fig.savefig(OUT/"school_burden.svg", metadata={"Date": None})
    plt.close(fig)


def main():
    OUT.mkdir(exist_ok=True)
    book = openpyxl.load_workbook(COST_FILE, data_only=True)
    row = list(book["8"].values)[10]
    assert "United States" in row[0]
    price = float(row[2]); assert 17619 < price < 17620
    published = births_input()
    frames = [model(case, published, price) for case in CASES]
    verify(published, frames)
    data = pd.concat(frames, ignore_index=True)
    data.to_csv(OUT/"annual_scenarios.csv", index=False, lineterminator="\n", float_format="%.6f")
    endpoints = data[data.year == 2025].to_dict("records")
    manifest = {"price": price, "parameters": CASES, "endpoints": endpoints,
                "inputs_sha256": {str(p.relative_to(HERE.parent)): hashlib.sha256(p.read_bytes()).hexdigest()
                                  for p in [COST_FILE, BIRTH_FILE]}, "verification": "PASS"}
    (OUT/"audit.json").write_text(json.dumps(manifest, indent=2)+"\n")
    chart(frames, price)
    print(data[data.year == 2025][["scenario", "total_pupils", "gross_operating_cost"]].to_string(index=False))


if __name__ == "__main__":
    main()
