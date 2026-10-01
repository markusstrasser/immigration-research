"""National enrollment minus the preserved partial pupil model; not causal identification."""
import argparse
import hashlib
import json
import re
from pathlib import Path
from urllib.request import urlopen

from bs4 import BeautifulSoup
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
OUT = HERE / "derived"
SOURCES = {
    "d03": "https://nces.ed.gov/programs/digest/d03/tables/dt003.asp",
    "d25": "https://nces.ed.gov/programs/digest/d25/tables/dt25_203.10.asp",
    "d23": "https://nces.ed.gov/programs/digest/d23/tables/dt23_203.10.asp",
}


def sources(fetch):
    soups, receipts = {}, {}
    for key, url in SOURCES.items():
        path = HERE / "_cache" / f"nces_{key}_20310.html"
        if fetch and not path.exists():
            raw = urlopen(url, timeout=45).read()
            assert b"Enrollment" in raw and len(raw) > 10000
            path.write_bytes(raw)
        raw = path.read_bytes()
        soups[key] = BeautifulSoup(raw, "html.parser")
        receipts[key] = dict(url=url, sha256=hashlib.sha256(raw).hexdigest())
    return soups, receipts


def totals(soup):
    result = {}
    for row in soup.find_all("tr"):
        cells = [c.get_text(" ", strip=True) for c in row.find_all(["td", "th"], recursive=False)]
        if len(cells) > 15 and re.fullmatch(r"\d{4}", cells[0]):
            year = int(cells[0])
            assert year not in result
            result[year] = int(cells[1].replace(",", "")) * 1000
    return result


def main(fetch=False):
    soups, receipts = sources(fetch)
    old = {}
    for line in soups["d03"].find("pre").get_text().splitlines():
        match = re.match(r"Fall (\d{4})", line)
        if match and 1975 <= int(match[1]) < 1990:
            old[int(match[1])] = int(line.split("|")[3].strip().replace(",", "")) * 1000
    observed = old | {y: v for y, v in totals(soups["d25"]).items() if 1975 <= y <= 2024}
    official = totals(soups["d23"])
    assert set(observed) == set(range(1975, 2025))
    assert observed[1975] == 44819000 and observed[2024] == 49387000
    assert official[2024] == 48707000 and official[2031] == 46890000
    # Preserve the latest observed level; borrow changes from the older projection.
    offset = observed[2024] - official[2024]
    slope = official[2031] - official[2030]
    assert offset == 680000 and slope == -50000
    baseline = observed | {y: official[y] + offset for y in range(2025, 2032)}
    baseline.update({y: baseline[2031] + (y - 2031) * slope for y in range(2032, 2036)})
    model = pd.read_csv(OUT / "projection_2035.csv").pivot(index="year", columns="scenario", values="total_pupils")
    df = pd.DataFrame({"year": range(1975, 2036)})
    df["total_enrollment"] = df.year.map(baseline)
    df["total_status"] = np.where(df.year <= 2024, "NCES observed", np.where(df.year <= 2031, "rebased NCES projection", "linear extension"))
    for scenario in ["low", "central", "high"]:
        df[f"gap_{scenario}"] = df.year.map(model[scenario])
        df[f"remaining_{scenario}"] = df.total_enrollment - df[f"gap_{scenario}"]
    assert df.notna().all().all() and (df.remaining_high > 0).all()
    assert (df.remaining_high <= df.remaining_central).all() and (df.remaining_central <= df.remaining_low).all()
    assert np.allclose(df.remaining_central + df.gap_central, df.total_enrollment)
    df.to_csv(OUT / "us_enrollment_counterfactual.csv", index=False, lineterminator="\n", float_format="%.6f")
    receipts.update(offset_2024=offset, annual_extension_after_2031=slope,
                    definition="Public pre-K–12 and ungraded total; subtract partial modeled ages 5–17 only",
                    model_sha256=hashlib.sha256((OUT / "projection_2035.csv").read_bytes()).hexdigest())
    (OUT / "us_enrollment_sources.json").write_text(json.dumps(receipts, indent=2) + "\n")
    chart(df)
    print(df[df.year.isin([1975, 2000, 2024, 2025, 2035])].to_string(index=False))


def chart(df):
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 11, "svg.hashsalt": "us-school-counterfactual"})
    fig, ax = plt.subplots(figsize=(13, 8), facecolor="#faf9f5")
    ax.set_facecolor("#faf9f5")
    fig.subplots_adjust(left=.075, right=.79, top=.78, bottom=.30)
    fig.text(.075, .94, "U.S. school enrollment: with and without modeled demand", fontsize=19, weight="bold")
    fig.text(.075, .89, "Unauthorized immigration and descendants • partial removal scenario, all else held equal", fontsize=12)
    fig.text(.075, .835, "Public pre-K–12 and ungraded pupils, millions  |  Modeled gap covers ages 5–17", fontsize=11, color="#555555")
    x = df.year
    ax.fill_between(x, df.remaining_high/1e6, df.remaining_low/1e6, color="#347d99", alpha=.16)
    ax.fill_between(x, df.remaining_central/1e6, df.total_enrollment/1e6, color="#bc9261", alpha=.17)
    ax.plot(x, df.remaining_central/1e6, color="#347d99", lw=2.4)
    ax.plot(x[x <= 2024], df.total_enrollment[x <= 2024]/1e6, color="#444444", lw=2.4)
    ax.plot(x[x >= 2024], df.total_enrollment[x >= 2024]/1e6, color="#444444", lw=2.4, ls="--")
    ax.axvline(2024, color="#999999", lw=.8, ls=":")
    ax.axvline(2031, color="#999999", lw=.8, ls=":")
    ax.text(2024.5, 53, "Scenario →", fontsize=9, color="#555555")
    ax.set(xlim=(1975, 2035), ylim=(0, 56), xticks=[1975, 1985, 1995, 2005, 2015, 2025, 2035], yticks=range(0, 56, 10))
    ax.grid(axis="y", alpha=.15); ax.set_axisbelow(True)
    for edge in ["top", "right", "left"]:
        ax.spines[edge].set_visible(False)
    ax.spines["bottom"].set_color("#aaaaaa"); ax.tick_params(length=0, pad=8)
    end = df.iloc[-1]
    ax.text(2036, end.total_enrollment/1e6, f"{end.total_enrollment/1e6:.1f}m total\n2035 scenario", va="bottom", fontsize=12, color="#444444")
    ax.text(2036, end.remaining_central/1e6-1, f"{end.remaining_central/1e6:.1f}m remaining\nAfter partial removal", va="top", fontsize=12, color="#347d99")
    fig.text(.075, .235, f"2035 gap: {end.gap_central/1e6:.1f}m pupils  |  Chosen scenarios: {end.gap_low/1e6:.1f}–{end.gap_high/1e6:.1f}m", fontsize=14, weight="bold")
    notes = [
        "Blue band varies the removed population; it is not a confidence interval and does not vary the total-enrollment projection.",
        "Total: NCES observations through 2024; older NCES projected changes rebased to 2024, then a linear extension after 2031.",
        "Remaining = total minus the earlier partial maternal-lineage model. Lawful immigration and other demographic behavior are held fixed.",
        "Excludes some descendant branches, births after maternal legalization, and pre-K/older pupils; starts at an assumed zero gap in 1975.",
        "Sources: NCES Digest tables 3 (2003) and 203.10 (2023/2025); Pew birth/child-stock estimates. This does not identify the full causal effect.",
    ]
    for i, text in enumerate(notes):
        fig.text(.075, .175-i*.029, text, fontsize=9, color="#555555")
    fig.savefig(OUT / "us_enrollment_counterfactual.png", dpi=180)
    fig.savefig(OUT / "us_enrollment_counterfactual.svg", metadata={"Date": None})
    plt.close(fig)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--fetch", action="store_true", help="Download missing raw HTML without overwriting cached sources")
    main(parser.parse_args().fetch)
