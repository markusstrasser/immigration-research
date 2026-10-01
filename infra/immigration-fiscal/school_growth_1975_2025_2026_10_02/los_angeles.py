"""Matched historical school enrollment shares: MPI's2009–13 county workbook."""
import hashlib
import json
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter
import openpyxl
import pandas as pd

HERE = Path(__file__).resolve().parent
SOURCE = HERE / "_cache/Children-of-Unauthorized-CountyData.xlsx"
URL = "https://www.migrationpolicy.org/sites/default/files/publications/Children-of-Unauthorized-CountyData.xlsx"


def main():
    rows = list(openpyxl.load_workbook(SOURCE,data_only=True)["Enrollment by age group"].values)
    assert "2009-13" in rows[2][0]
    assert [rows[3][i] for i in [5,8,11]] == ["Ages 5-11","Ages 12-14","Ages 15-17"]
    selected = []
    for label,key in [("United States","United States"),("Los Angeles County","Los Angeles County, California")]:
        matches = [r for r in rows[5:] if r[0]==key or r[1]==key]
        assert len(matches)==1
        row = matches[0]
        exposed = sum(row[i] for i in [5,8,11])
        total = sum(row[i] for i in [7,10,13])
        assert 0 < exposed < total
        selected.append(dict(geography=label,enrolled_with_unauthorized_parent=exposed,
                             enrolled_total=total,share=exposed/total))
    df = pd.DataFrame(selected)
    assert df.enrolled_with_unauthorized_parent.tolist()==[3397000,343000]
    assert df.enrolled_total.tolist()==[49775000,1609000]
    ratio = df.share.iloc[1]/df.share.iloc[0]
    out = HERE/"derived"
    out.mkdir(exist_ok=True)
    df.to_csv(out/"la_enrollment_comparison.csv",index=False,lineterminator="\n")
    (out/"la_source.json").write_text(json.dumps({"url":URL,"sha256":hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
        "period":"2009-2013 pooled","school_type":"public and private combined","age":"5–17",
        "ratio":ratio},indent=2)+"\n")
    plt.rcParams.update({"font.family":"DejaVu Sans","font.size":12,"svg.hashsalt":"la-enrollment-20261002"})
    fig,ax = plt.subplots(figsize=(11,6),facecolor="#faf9f5")
    ax.set_facecolor("#faf9f5")
    fig.subplots_adjust(left=.23,right=.9,bottom=.32,top=.7)
    fig.text(.08,.91,"LA County’s share was about 3 times the national share",fontsize=19,weight="bold")
    fig.text(.08,.85,"Enrolled children with at least one unauthorized parent • ages 5–17",fontsize=13)
    fig.text(.08,.79,"2009–2013 pooled estimates | Public and private schools combined",fontsize=11,color="#555555")
    ax.barh([1,0],df.share,height=.52,color=["#aaa9a4","#347d99"])
    ax.set_yticks([1,0],df.geography)
    ax.set(xlim=(0,.28),ylim=(-.65,1.7))
    ax.set_xticks([0,.05,.10,.15,.20,.25]); ax.xaxis.set_major_formatter(PercentFormatter(1,decimals=0))
    ax.grid(axis="x",alpha=.18); ax.set_axisbelow(True)
    for edge in ["top","right","left"]:
        ax.spines[edge].set_visible(False)
    ax.spines["bottom"].set_color("#aaaaaa"); ax.tick_params(length=0,pad=9)
    for i,row in df.iterrows():
        ax.text(row.share+.008,1-i,f"{row.share:.1%}",va="center",fontsize=17,weight="bold")
    fig.text(.23,.235,"LA: 343,000 of 1,609,000 enrolled children in the study population",fontsize=12)
    fig.text(.23,.185,f"Matched ratio: {ratio:.2f}×  |  Both groups use the same years, ages and definitions",fontsize=11,color="#444444")
    notes=["Share within MPI’s study population; includes U.S.-born citizens. Parent-status enrollment, not a count of all descendants.",
           "Historical estimates, not a 2025 measurement or a 2035 LA forecast; no public-only spending estimate is inferred.",
           "Source: Migration Policy Institute, Children of Unauthorized Immigrants county data (2016); ACS2009–13 and SIPP2008."]
    for i,note in enumerate(notes):
        fig.text(.08,.115-i*.029,note,fontsize=9,color="#555555")
    fig.savefig(out/"la_school_comparison.png",dpi=180)
    fig.savefig(out/"la_school_comparison.svg",metadata={"Date":None})
    plt.close(fig)
    print(df.to_string(index=False)); print("LA/US",ratio)


if __name__=="__main__":
    main()
