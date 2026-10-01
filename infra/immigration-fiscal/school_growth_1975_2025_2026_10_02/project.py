"""Extend the preserved partial model to2035 under explicit continuation scenarios."""
import json
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import build

HERE = Path(__file__).resolve().parent
YEARS = np.arange(1975, 2036)
FUTURE = {
    "low": {"births_2030": 150000, "minors_2035": 600000},
    "central": {"births_2030": 300000, "minors_2035": 1500000},
    "high": {"births_2030": 450000, "minors_2035": 2400000},
}


def project(name, historical, price):
    p = build.CASES[name]
    f = FUTURE[name]
    births = np.interp(YEARS, historical.year, historical.births_to_unauthorized_mothers)
    after = YEARS > 2023
    births[after] = np.interp(YEARS[after], [2023, 2030, 2035],
                              [300000, f["births_2030"], f["births_2030"]])
    foreign = np.interp(YEARS, historical.year, historical.foreignborn_pupils)
    future = YEARS > 2025
    foreign[future] = np.interp(YEARS[future], [2025, 2035],
                                [historical.foreignborn_pupils.iloc[-1],
                                 f["minors_2035"]*p["child_school_age"]*p["public"]])
    direct = build.pupils(births, p["public"], p["loss"])
    recent = build.pupils(np.where(YEARS > 2023, births, 0.), p["public"], p["loss"])
    later = np.zeros(len(YEARS))
    descendants = births.copy()
    for _ in range(len(YEARS)//18):
        descendants = build.descendant_births(descendants, p["fertility"], p["peak"], p["loss"])
        later += build.pupils(descendants, p["public"], p["loss"])
    total = foreign + direct + later
    return pd.DataFrame(dict(year=YEARS, scenario=name, foreignborn_pupils=foreign,
                             direct_pre2024_births=direct-recent, direct_post2023_births=recent,
                             later_maternal_descendants_pupils=later,
                             total_pupils=total, gross_operating_cost=total*price))


def chart(frames):
    low, mid, high = frames
    plt.rcParams.update({"font.family":"DejaVu Sans", "font.size":11,
                         "svg.hashsalt":"school-projection-2035"})
    colors = ["#aaa9a4", "#347d99", "#94bed3", "#80b9ad"]
    columns = ["foreignborn_pupils", "direct_pre2024_births", "direct_post2023_births", "later_maternal_descendants_pupils"]
    fig, ax = plt.subplots(figsize=(13, 8), facecolor="#faf9f5")
    ax.set_facecolor("#faf9f5")
    fig.subplots_adjust(left=.08, right=.83, bottom=.29, top=.79)
    fig.text(.08, .94, "School demand through 2035: a continuation scenario", fontsize=21, weight="bold")
    fig.text(.08, .895, "Unauthorized immigration and partial maternal descendants • U.S. public-school pupils, millions", fontsize=12)
    ax.stackplot(YEARS, *(mid[c]/1e6 for c in columns), colors=colors)
    ax.fill_between(YEARS, low.total_pupils/1e6, high.total_pupils/1e6,
                    facecolor="none", edgecolor="#333333", alpha=.22, hatch="////", linewidth=.7)
    ax.plot(YEARS, mid.total_pupils/1e6, color="#222222", linewidth=1.6)
    ax.axvline(2025, color="#333333", linestyle="--", linewidth=1.1)
    ymax = np.ceil(high.total_pupils.max()/1e6)
    ax.text(2025.5, ymax*.94, "Projection", fontsize=11)
    ax.text(1976, ymax*.94, "Early history starts at an assumed zero", fontsize=10, color="#666666")
    ax.set(xlim=(1975,2035), ylim=(0,ymax), xticks=[1975,1985,1995,2005,2015,2025,2035])
    ax.grid(axis="y", alpha=.16); ax.set_axisbelow(True)
    for edge in ["left","right","top"]:
        ax.spines[edge].set_visible(False)
    ax.spines["bottom"].set_color("#aaaaaa"); ax.tick_params(length=0, pad=8)
    last = mid.iloc[-1]
    ax.text(1.02,.78,f"2035 central\n{last.total_pupils/1e6:.1f} million pupils\n${last.gross_operating_cost/1e9:.0f}bn/year", transform=ax.transAxes, fontsize=13, weight="bold", linespacing=1.5)
    ax.text(1.02,.45,f"Chosen scenarios\n{low.total_pupils.iloc[-1]/1e6:.1f}–{high.total_pupils.iloc[-1]/1e6:.1f}m pupils\n${low.gross_operating_cost.iloc[-1]/1e9:.0f}–{high.gross_operating_cost.iloc[-1]/1e9:.0f}bn/year", transform=ax.transAxes, fontsize=10, color="#555555", linespacing=1.5)
    labels = ["Foreign-born, currently unauthorized", "U.S.-born children: births through 2023",
              "U.S.-born children: assumed births after 2023", "Later maternal descendants (modeled)"]
    for i, (color,label,column) in enumerate(zip(colors,labels,columns)):
        x = .08+(i%2)*.43; y = .225-(i//2)*.043
        fig.text(x,y,"■", color=color, fontsize=16)
        fig.text(x+.025,y+.002,f"{label} · {last[column]/1e6:.2f}m in 2035", fontsize=10)
    notes = ["Central: 300,000 births/year to unauthorized mothers after 2023; foreign-born unauthorized minors stay at 1.5m.",
             "Gross operating cost at a constant $17,619 per pupil (FY2024); excludes construction and does not subtract family taxes.",
             "Partial lineage: excludes births after maternal legalization and branches through U.S.-born fathers. Band is scenario sensitivity, not a confidence interval.",
             "Sources: Pew birth and child-stock estimates; Census school finances. All pupil curves modeled. Details and exclusions in README."]
    for i,note in enumerate(notes):
        fig.text(.08,.12-i*.026,note,fontsize=9,color="#555555")
    fig.savefig(build.OUT/"school_burden_2035.png",dpi=180)
    fig.savefig(build.OUT/"school_burden_2035.svg",metadata={"Date":None})
    plt.close(fig)


def main():
    historical = pd.read_csv(build.OUT/"annual_scenarios.csv")
    price = json.loads((build.OUT/"audit.json").read_text())["price"]
    frames = [project(name,historical[historical.scenario==name],price) for name in FUTURE]
    for f in frames:
        h = historical[historical.scenario==f.scenario.iloc[0]]
        assert np.allclose(f.loc[f.year<=2025,"total_pupils"],h.total_pupils)
        assert (f.select_dtypes("number") >= 0).all().all()
        assert not f.loc[f.year<2029,"direct_post2023_births"].any()
        assert np.allclose(f.total_pupils,f.foreignborn_pupils+f.direct_pre2024_births+f.direct_post2023_births+f.later_maternal_descendants_pupils)
    assert (frames[0].total_pupils <= frames[1].total_pupils).all()
    assert (frames[1].total_pupils <= frames[2].total_pupils).all()
    # Births after2023 cannot create school-age grandchildren before2046.
    shock = np.where(YEARS>2023,1e6,0.)
    grandchildren = build.descendant_births(shock,2.,29,.005)
    assert not build.pupils(grandchildren,.9,.005).any()
    result = pd.concat(frames,ignore_index=True)
    result.to_csv(build.OUT/"projection_2035.csv",index=False,lineterminator="\n",float_format="%.6f")
    (build.OUT/"projection_assumptions.json").write_text(json.dumps(FUTURE,indent=2)+"\n")
    chart(frames)
    print(result[result.year.isin([2025,2035])][["year","scenario","total_pupils","gross_operating_cost"]].to_string(index=False))


if __name__ == "__main__":
    main()
