"""Birth-cohort test: do Mexican IR-5 admissions track US births to Mexico-born mothers 21+ years earlier?

Inputs: `derived/births_mexico_mothers.csv` (build_births.py) and the sister lane's
`late_arrival_tail_2026_09_27/derived/ir5_flow.csv` (IR-5 by country, FY2005-2024; read, not retyped).
Outputs: `derived/cohort_vs_ir5.csv`, `derived/cohort_fit.csv`, `derived/cohort_projection.csv`,
`derived/backlog_catchup.csv`, `derived/decomposition.csv`, `derived/cohort_vs_ir5.png`.

A child born in calendar year b turns 21 in calendar b+21; federal FY t runs Oct t-1 to Sep t, so
the cohort turning 21 in FY t is 0.75*B[t-21] + 0.25*B[t-22]. "Lag L" shifts that by L-21 more
years (petitioning later than 21, processing time). The processing index is IR-5 from all
countries except Mexico, which shares USCIS/State capacity shocks but not the Mexican cohort.
Births after 2004 are [MODEL] (no mother's birthplace on the public file); FY2026+ cohorts use them.
"""
import csv
import math
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
FLOW = HERE.parent / "late_arrival_tail_2026_09_27" / "derived" / "ir5_flow.csv"
BIRTHS = HERE / "derived" / "births_mexico_mothers.csv"
D = HERE / "derived"
FYS = list(range(2005, 2025))
PROJ = list(range(2025, 2031))
CENTRAL, HIGH, FIRST, FB = ("births_mexico_born_mother", "births_mexico_born_mother_high",
                            "births_mexico_born_mother_first", "births_foreign_born_mother")


def load():
    ir5 = {}
    for r in csv.DictReader(FLOW.open()):
        if r["country"] in ("all", "mexico"):
            ir5[(r["country"], int(r["fy"]))] = float(r["ir5_parents"])
    births = {int(r["birth_year"]): r for r in csv.DictReader(BIRTHS.open())}
    return ir5, births


def cohort(births, fy, lag=21, col=CENTRAL):
    a, b = births[fy - lag][col], births[fy - lag - 1][col]
    if a == "" or b == "":
        return None
    return 0.75 * float(a) + 0.25 * float(b)


def status(births, fy, lag=21):
    return "[MODEL]" if any(births[y]["status"] != "measured" for y in (fy - lag, fy - lag - 1)) else "measured"


def ols(y, X):
    X = np.column_stack([np.ones(len(y))] + X)
    beta, *_ = np.linalg.lstsq(X, y, rcond=None)
    fit = X @ beta
    r2 = 1 - ((y - fit) ** 2).sum() / ((y - y.mean()) ** 2).sum()
    return beta, r2, fit


def write(path, rows):
    with path.open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0]), lineterminator="\n")
        w.writeheader()
        w.writerows(rows)


def r3(x):
    return round(float(x), 3)


def main():
    ir5, births = load()
    mex = np.array([ir5[("mexico", t)] for t in FYS])
    allc = np.array([ir5[("all", t)] for t in FYS])
    non = allc - mex
    has_first = births[2000][FIRST] != ""
    i15, i19, i24 = FYS.index(2015), FYS.index(2019), FYS.index(2024)

    # 1. levels, changes and fits by lag
    fits = []
    for lag in range(21, 25):  # lag 25 would need 1979 births
        B = np.array([cohort(births, t, lag) for t in FYS])
        (_, b1), r2_a, _ = ols(np.log(mex), [np.log(B)])
        (_, b2, c2), r2_b, _ = ols(np.log(mex), [np.log(B), np.log(non)])
        _, r2_p, _ = ols(np.log(mex), [np.log(non)])
        row = dict(lag=lag, r_levels=r3(np.corrcoef(mex, B)[0, 1]),
                   r_changes_dlog=r3(np.corrcoef(np.diff(np.log(mex)), np.diff(np.log(B)))[0, 1]),
                   r_changes_dlog_vs_nonmexico=r3(np.corrcoef(np.diff(np.log(mex)), np.diff(np.log(non)))[0, 1]),
                   cohort_only_elasticity=r3(b1), cohort_only_r2=r3(r2_a),
                   processing_only_r2=r3(r2_p), both_cohort_elasticity=r3(b2),
                   both_processing_elasticity=r3(c2), both_r2=r3(r2_b))
        if has_first:
            F = np.array([cohort(births, t, lag, FIRST) for t in FYS])
            row["first_births_r_levels"] = r3(np.corrcoef(mex, F)[0, 1])
            row["first_births_cohort_only_r2"] = r3(ols(np.log(mex), [np.log(F)])[1])
        fits.append(row)

    # 2. per-year table at lag 21, with Mexico's share of IR-5 against its share of the
    #    cohort of US births to all foreign-born mothers turning 21
    B21 = np.array([cohort(births, t) for t in FYS])
    FB21 = np.array([cohort(births, t, col=FB) for t in FYS])
    mex_share, coh_share = mex / allc, B21 / FB21
    rows = []
    for i, t in enumerate(FYS):
        rows.append(dict(
            fy=t, ir5_mexico=int(mex[i]), ir5_all=int(allc[i]), ir5_non_mexico=int(non[i]),
            mexico_share_of_ir5=round(mex_share[i], 4),
            cohort_turning21=round(B21[i]),
            cohort_turning21_first_births=round(cohort(births, t, col=FIRST)) if has_first else "",
            cohort_turning21_foreign_born_mothers=round(FB21[i]),
            mexico_share_of_foreign_born_cohort=round(coh_share[i], 4),
            cohort_birth_years=f"{t - 22}-{t - 21}", cohort_status=status(births, t),
            ir5_per_1000_turning21=round(1000 * mex[i] / B21[i], 1),
            nonmex_ir5_index_fy2019=round(non[i] / non[i19], 3)))
    write(D / "cohort_vs_ir5.csv", rows)
    r_share = np.corrcoef(mex_share, coh_share)[0, 1]
    fits[0]["r_mexico_share_ir5_vs_share_cohort"] = r3(r_share)
    write(D / "cohort_fit.csv", fits)

    # 3. decomposition of the FY2019 -> FY2024 increase in Mexican IR-5
    rise = mex[i24] - mex[i19]
    by_cohort = mex[i19] * B21[i24] / B21[i19] - mex[i19]
    by_world = mex_share[i19] * allc[i24] - mex[i19]
    by_both = mex[i19] * (B21[i24] / B21[i19]) * (non[i24] / non[i19]) - mex[i19]
    dec = [
        dict(counterfactual="FY2019 yield per child turning 21, applied to the FY2024 cohort",
             predicted_fy2024=round(mex[i19] + by_cohort), share_of_rise=round(by_cohort / rise, 3)),
        dict(counterfactual="Mexico keeps its FY2019 share of all-country IR-5",
             predicted_fy2024=round(mex[i19] + by_world), share_of_rise=round(by_world / rise, 3)),
        dict(counterfactual="cohort growth times non-Mexican IR-5 growth (unit elasticities)",
             predicted_fy2024=round(mex[i19] + by_both), share_of_rise=round(by_both / rise, 3)),
    ]
    for d in dec:
        d.update(actual_fy2019=int(mex[i19]), actual_fy2024=int(mex[i24]), rise=int(rise))
    write(D / "decomposition.csv", dec)

    # 4. backlog: FY2020-22 shortfall and FY2023-24 excess against FY2019, and the FY2020-24
    #    cumulative Mexican IR-5 against the cohort path at the FY2019 yield
    i20, i22, i23 = FYS.index(2020), FYS.index(2022), FYS.index(2023)
    y19 = mex[i19] / B21[i19]
    catch = []
    for name, s in (("mexico", mex), ("non_mexico", non), ("all", allc)):
        catch.append(dict(series=name, fy2019=int(s[i19]),
                          shortfall_fy2020_22=int(sum(s[i19] - s[i] for i in range(i20, i22 + 1))),
                          excess_fy2023_24=int(sum(s[i] - s[i19] for i in range(i23, i24 + 1))),
                          actual_fy2020_24=int(s[i20:i24 + 1].sum()),
                          flat_fy2019_x5=int(5 * s[i19]),
                          cohort_path_fy2020_24_at_fy2019_yield=(
                              round(float((y19 * B21[i20:i24 + 1]).sum())) if name == "mexico" else "")))
    write(D / "backlog_catchup.csv", catch)

    # 5. projection to FY2030. Low: the lag-21 two-regressor model with non-Mexican IR-5 back at
    #    its FY2015-19 mean (processing returns to the pre-COVID pace). Mid/high: Mexican IR-5 per
    #    child turning 21 held at the FY2015-19 mean or at FY2024 (which includes the catch-up);
    #    cohort central or high birth variant
    (a, b, c), r2, fit = ols(np.log(mex), [np.log(B21), np.log(non)])
    resid_sd = float(np.std(np.log(mex) - fit, ddof=3))
    yield_pre = float((mex[i15:i19 + 1] / B21[i15:i19 + 1]).mean())
    yield_24 = float(mex[i24] / B21[i24])
    non_pre = float(non[i15:i19 + 1].mean())
    proj = []
    for t in PROJ:
        Bc, Bh = cohort(births, t), cohort(births, t, col=HIGH)
        proj.append(dict(
            fy=t, cohort_status=status(births, t), cohort_turning21=round(Bc),
            cohort_turning21_high=round(Bh),
            cohort_turning21_first_births=round(cohort(births, t, col=FIRST)) if has_first else "",
            low_model_processing_back_to_fy2015_19=round(
                math.exp(a + b * math.log(Bc) + c * math.log(non_pre))),
            mid_yield_fy2015_19=round(yield_pre * Bc),
            high_yield_fy2024=round(yield_24 * Bc),
            high_yield_fy2024_high_births=round(yield_24 * Bh)))
    write(D / "cohort_projection.csv", proj)

    print("✓ fits by lag:")
    for f in fits:
        print("  ", f)
    print(f"✓ decomposition of FY2019→24 rise ({int(rise)}):")
    for d in dec:
        print(f"   {d['share_of_rise']:.2f}  {d['counterfactual']}")
    for c_ in catch:
        print("   backlog", c_)
    print(f"✓ lag-21 model: log mex = {a:.2f} + {b:.3f} log B + {c:.3f} log nonmex, R2 {r2:.3f}, resid sd {resid_sd:.3f}")
    print(f"✓ yield per 1000 turning 21: FY2015-19 mean {1000 * yield_pre:.1f}, FY2024 {1000 * yield_24:.1f}")
    print(f"✓ Mexico share of IR-5 {mex_share.min():.3f}-{mex_share.max():.3f}; of foreign-born cohort "
          f"{coh_share.min():.3f}-{coh_share.max():.3f}; r {r_share:.3f}")
    for p in proj:
        print("  ", p)

    figure(births, mex, non, allc, mex_share, coh_share, proj, has_first, i19)


def figure(births, mex, non, allc, mex_share, coh_share, proj, has_first, i19):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    ORANGE, BLUE, GREY, INK = "#c8662a", "#3b6fb0", "#7a7a7a", "#333333"
    plt.rcParams.update({"font.size": 8.5, "axes.edgecolor": "#999999", "axes.labelcolor": INK,
                         "xtick.color": INK, "ytick.color": INK})
    fig, (ax, bx) = plt.subplots(2, 1, figsize=(9, 8.4), dpi=150, height_ratios=(1.35, 1))

    # A. everything indexed to FY2019 = 100
    yrs = list(range(2002, 2031))
    base = cohort(births, 2019)
    meas = [t for t in yrs if status(births, t) == "measured"]
    model = [meas[-1]] + [t for t in yrs if status(births, t) != "measured"]
    ax.plot(meas, [100 * cohort(births, t) / base for t in meas], color=BLUE, lw=2)
    ax.plot(model, [100 * cohort(births, t) / base for t in model], color=BLUE, lw=2, ls="--")
    if has_first:
        fb = cohort(births, 2019, col=FIRST)
        ax.plot(yrs, [100 * cohort(births, t, col=FIRST) / fb for t in yrs], color=BLUE, lw=1.2, ls=":")
    ax.plot(FYS, 100 * non / non[i19], color=GREY, lw=1.6, marker="o", ms=2.5)
    ax.plot(FYS, 100 * mex / mex[i19], color=ORANGE, lw=2.2, marker="o", ms=3.5)
    lo = [100 * p["low_model_processing_back_to_fy2015_19"] / mex[i19] for p in proj]
    hi = [100 * p["high_yield_fy2024"] / mex[i19] for p in proj]
    px = [p["fy"] for p in proj]
    ax.fill_between([2024] + px, [100 * mex[-1] / mex[i19]] + lo, [100 * mex[-1] / mex[i19]] + hi,
                    color=ORANGE, alpha=0.13, lw=0)
    lab = dict(fontsize=8, va="center")
    ax.text(2024.3, 100 * mex[-1] / mex[i19] + 8, "Mexican IR-5 parents", color=INK, **lab)
    ax.text(2024.3, 100 * non[-1] / non[i19] - 9, "non-Mexican IR-5\n(processing index)", color=INK, **lab)
    ax.text(2030.2, 100 * cohort(births, 2030) / base, "US births to\nMexico-born mothers\nturning 21", color=INK, **lab)
    ax.text(2030.3, hi[-1] + 6, "[MODEL] Mexican IR-5\nFY2025–30 range", color=INK, **lab)
    ax.plot(model[1:], [100 * cohort(births, t) / base for t in model[1:]], ls="none")
    ax.axhline(100, color="#dddddd", lw=0.8, zorder=0)
    ax.set_xlim(2002, 2030.5)
    ax.set_ylabel("index, FY2019 = 100")
    ax.set_title("A. Mexican IR-5 moves with IR-5 from other countries, not with the Mexican birth cohort",
                 loc="left", fontsize=9.5, color=INK)
    handles = [plt.Line2D([], [], color=ORANGE, lw=2.2, marker="o", ms=3.5),
               plt.Line2D([], [], color=GREY, lw=1.6, marker="o", ms=2.5),
               plt.Line2D([], [], color=BLUE, lw=2),
               plt.Line2D([], [], color=BLUE, lw=2, ls="--")]
    labels = ["Mexican IR-5 parents (DHS)", "Non-Mexican IR-5 parents (DHS)",
              "Births to Mexico-born mothers, +21 yr (NCHS)", "same, 2005+ births [MODEL]"]
    if has_first:
        handles.append(plt.Line2D([], [], color=BLUE, lw=1.2, ls=":"))
        labels.append("same, first live births only (FY2026+ [MODEL])")
    ax.legend(handles, labels, fontsize=7.5, loc="upper left", frameon=False)

    # B. Mexico's shares
    bx.plot(FYS, 100 * mex_share, color=ORANGE, lw=2.2, marker="o", ms=3.5)
    bx.plot(FYS, 100 * coh_share, color=BLUE, lw=2)
    bx.text(2024.3, 100 * mex_share[-1], "of all IR-5 parents", color=INK, **lab)
    bx.text(2024.3, 100 * coh_share[-1], "of US births to\nforeign-born mothers\nturning 21", color=INK, **lab)
    bx.set_ylim(0, 50)
    bx.set_xlim(2002, 2030.5)
    bx.set_ylabel("Mexico's share, %")
    bx.set_xlabel("fiscal year (IR-5) / fiscal year the birth cohort turns 21")
    bx.set_title("B. Mexico's share of IR-5 parents stays far below its share of the cohort turning 21",
                 loc="left", fontsize=9.5, color=INK)
    for x in (ax, bx):
        for s in ("top", "right"):
            x.spines[s].set_visible(False)
        x.grid(axis="y", color="#eeeeee", lw=0.6)
        x.set_axisbelow(True)
    fig.text(0.01, 0.005, "Sources: NCHS natality public-use files 1980–2010 (NBER mirror); DHS OHSS LPR by country "
             "and class via late_arrival_tail_2026_09_27. Lane ir5_fraud_and_cohorts_2026_09_27.",
             fontsize=6, color="#555555")
    fig.subplots_adjust(left=0.08, right=0.79, top=0.95, bottom=0.08, hspace=0.3)
    fig.savefig(D / "cohort_vs_ir5.png")
    print("✓ wrote cohort_vs_ir5.png")


if __name__ == "__main__":
    main()
