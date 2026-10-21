"""Q2: vote share of never-governing (cordon-type) parties vs cabinet formation time, duration and early elections.

Data: ParlGov development release (view_election, view_cabinet, view_party; parlgov.org, data through mid-2023).
Specification fixed in RESULT.md "Pre-registration" (2026-10-21 15:10 JST) before this script was written.
Deviation recorded in RESULT.md: Switzerland and Cyprus are dropped (executive not formed by parliament).

Outputs: derived/q2_elections.csv (one row per election), derived/q2_cabinets.csv (one row per cabinet),
derived/q2_coefficients.csv (every coefficient estimated).
"""
import csv
import pathlib
import urllib.request

import numpy as np
import pandas as pd
import statsmodels.formula.api as smf

LANE = pathlib.Path(__file__).resolve().parent
CACHE = LANE / "_cache"
DERIVED = LANE / "derived"
BASE = "https://www.parlgov.org/data/parlgov-development_csv-utf-8/"
START = "1980-01-01"
LOOKBACK_YEARS = 20
DROP = {"CHE", "CYP"}  # collegial / presidential executive: no parliamentary formation
# Statutory maximum term of the lower house, years [TRAINING-DATA]; (country, from_year, years).
TERMS = {"AUS": 3, "NZL": 3, "GBR": 5, "IRL": 5, "ITA": 5, "FRA": 5, "MLT": 5, "LUX": 5, "CAN": 5}
TERM_CHANGES = [("BEL", 2014, 5), ("SWE", 1994, 4), ("TUR", 2018, 5)]
TERM_BEFORE = {"BEL": 4, "SWE": 3, "TUR": 4}
# Named cordon list (small-sample check): country -> (party_name_short, first election year, last year)
CORDON = [("BEL", "VB", 1991, 2100), ("FRA", "FN", 1986, 2100), ("DEU", "AfD", 2013, 2100),
          ("SWE", "SD", 2010, 2021)]


def fetch(name):
    path = CACHE / f"{name}.csv"
    if not path.exists():
        CACHE.mkdir(exist_ok=True)
        urllib.request.urlretrieve(BASE + f"{name}.csv", path)
    return pd.read_csv(path)


def term_years(country, year):
    for c, y, t in TERM_CHANGES:
        if c == country:
            return t if year >= y else TERM_BEFORE[c]
    return TERMS.get(country, 4)


def build():
    el = fetch("view_election")
    cab = fetch("view_cabinet")
    party = fetch("view_party")[["party_id", "family_name"]]
    el = el[(el.election_type == "parliament") & ~el.country_name_short.isin(DROP)].merge(party, on="party_id", how="left")
    el["election_date"] = pd.to_datetime(el.election_date)
    cab = cab[~cab.country_name_short.isin(DROP)].copy()
    cab["start_date"] = pd.to_datetime(cab.start_date)
    in_cab = cab[cab.cabinet_party == 1][["country_name_short", "party_id", "start_date"]]

    rows = []
    for (ctry, eid), g in el.groupby(["country_name_short", "election_id"]):
        d = g.election_date.iloc[0]
        lo = d - pd.DateOffset(years=LOOKBACK_YEARS)
        gov = set(in_cab[(in_cab.country_name_short == ctry) & (in_cab.start_date >= lo)
                         & (in_cab.start_date <= d)].party_id)
        vs = g.vote_share.fillna(0)
        never = ~g.party_id.isin(gov)
        x_rr = vs[(g.family_name == "Right-wing") & never].sum()
        x_both = vs[g.family_name.isin(["Right-wing", "Communist/Socialist"]) & never].sum()
        cordon = sum(vs[g.party_name_short == p].sum() for c, p, y0, y1 in CORDON
                     if c == ctry and y0 <= d.year <= y1)
        s = (g.seats.fillna(0) / g.seats_total.iloc[0]).to_numpy()
        enpp = 1 / np.sum(s ** 2) if np.sum(s ** 2) > 0 else np.nan
        rows.append(dict(country=ctry, election_id=int(eid), election_date=d, x_rr=x_rr, x_both=x_both,
                         x_cordon=cordon, enpp=enpp))
    E = pd.DataFrame(rows).sort_values(["country", "election_date"])
    E["next_election"] = E.groupby("country").election_date.shift(-1)

    first = (cab[cab.caretaker == 0].groupby("election_id").start_date.min().rename("first_cabinet_start"))
    E = E.merge(first, left_on="election_id", right_index=True, how="left")
    E["formation_days"] = (E.first_cabinet_start - E.election_date).dt.days
    E["interval_days"] = (E.next_election - E.election_date).dt.days
    E["term_days"] = [term_years(c, d.year) * 365.25 for c, d in zip(E.country, E.election_date)]
    E["early_election"] = np.where(E.next_election.isna(), np.nan,
                                   (E.interval_days < E.term_days - 180).astype(float))
    E["decade"] = (E.election_date.dt.year // 10) * 10
    E = E[E.election_date >= START]

    C = cab.drop_duplicates("cabinet_id")[["country_name_short", "cabinet_id", "election_id", "start_date",
                                            "caretaker"]].sort_values(["country_name_short", "start_date"])
    C["next_start"] = C.groupby("country_name_short").start_date.shift(-1)
    C = C[(C.caretaker == 0) & (C.start_date >= START) & C.next_start.notna()]
    C["duration_days"] = (C.next_start - C.start_date).dt.days
    C = C.rename(columns={"country_name_short": "country"}).merge(
        E[["election_id", "x_rr", "x_both", "x_cordon", "enpp", "decade"]], on="election_id", how="inner")
    C = C[C.duration_days > 0]
    return E, C


def fit(df, y, x, controls):
    d = df.dropna(subset=[y, x] + controls).copy()
    d["X10"] = d[x] / 10
    f = f"{y} ~ X10 + C(country) + C(decade)" + "".join(f" + {c}" for c in controls)
    m = smf.ols(f, data=d).fit(cov_type="cluster", cov_kwds={"groups": pd.factorize(d.country)[0]})
    return m.params["X10"], m.bse["X10"], int(m.nobs), d.country.nunique(), d[x].mean(), d[x].std()


def main():
    E, C = build()
    E["log_formation"] = np.log1p(E.formation_days.clip(lower=0))
    C["log_duration"] = np.log(C.duration_days)
    DERIVED.mkdir(exist_ok=True)
    E.assign(election_date=E.election_date.dt.date, next_election=E.next_election.dt.date,
             first_cabinet_start=E.first_cabinet_start.dt.date).to_csv(
        DERIVED / "q2_elections.csv", index=False, lineterminator="\n", float_format="%.4f")
    C.assign(start_date=C.start_date.dt.date, next_start=C.next_start.dt.date).to_csv(
        DERIVED / "q2_cabinets.csv", index=False, lineterminator="\n", float_format="%.4f")
    out = []
    specs = [("formation", E, "log_formation"), ("formation_days_raw", E, "formation_days"),
             ("duration", C, "log_duration"), ("early_election", E, "early_election")]
    for name, df, y in specs:
        for x in ("x_rr", "x_both", "x_cordon"):
            for controls in ([], ["enpp"]):
                b, se, n, k, mx, sx = fit(df, y, x, controls)
                out.append([name, y, x, "+".join(controls) or "none", f"{b:.4f}", f"{se:.4f}", f"{b/se:.2f}",
                            n, k, f"{mx:.2f}", f"{sx:.2f}"])
    with open(DERIVED / "q2_coefficients.csv", "w", newline="") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(["outcome", "y", "regressor", "controls", "b_per_10pp", "se_cluster_country", "t", "n",
                    "countries", "x_mean_pp", "x_sd_pp"])
        w.writerows(out)
    for r in out:
        print(*r, sep="\t")
    print("elections", len(E), "median formation days", E.formation_days.median(),
          "cabinets", len(C), "median duration", C.duration_days.median(), "early share", E.early_election.mean())


if __name__ == "__main__":
    main()
