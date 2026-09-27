"""One civic table by Mexican-origin generation with the carry-over ratio
rho(n -> n+1) = gap(G n+1) / gap(G n), raw and at equal SES.

Every number is read from a derived CSV, none retyped:
  service_by_ses_2026_09_23/derived/cps_civic_rates.csv, cps_civic_gaps.csv  (CPS Sept 2021+2023:
      volunteering, giving, veteran status; gaps are weighted-LPM coefficients vs US-born NH whites)
  service_by_ses_2026_09_23/derived/military_rates.csv  (ACS 2022-2024, US-born vs Mexico-born only)
  derived/voting.csv  (this lane, CPS November 2020/2022/2024, equal-weight mean of the three)
  derived/intermarriage.csv  (this lane, CPS ASEC 2022-2025; the "gap" is endogamy in excess of
      random matching within state, since NH whites are not a comparator for in-marriage)
  norms_gen_2026_09_18/derived/gss_adjusted.csv, anes_adjusted.csv  (GSS 2000-2024, ANES 2020+2024;
      "adj_mex" controls age, age^2, years of education, log family income, year)

rho SE: delta method treating the two gaps as independent. Gaps from one regression share the
white reference, which makes them positively correlated, so the stated rho SE is conservative.
A rho is left blank when the earlier gap is within 2 SE of zero (the ratio is then meaningless).
"""
import re
import sys
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
FISCAL = HERE.parent
SVC = FISCAL / "service_by_ses_2026_09_23" / "derived"
NORMS = FISCAL / "norms_gen_2026_09_18" / "derived"
GENS = ["G1", "G2", "G3+"]


def cps_sept():
    rates = pd.read_csv(SVC / "cps_civic_rates.csv")
    gaps = pd.read_csv(SVC / "cps_civic_gaps.csv")
    gmap = {"mexico_born": "G1", "mexican_2nd_gen": "G2", "mexican_3rd_plus": "G3+"}
    rows = []
    for measure in ("volunteered", "gave_over_25", "veteran"):
        arm = "men_18_plus_born_1956_on" if measure == "veteran" else "adults_18_plus"
        r = rates[(rates.arm == arm) & (rates.measure == measure)]
        white = r[r.group == "usb_nh_white"].iloc[0]
        for spec, label in (("raw", "raw"), ("ses", "age, sex, education, family income, year"),
                            ("ses_geo", "age, sex, education, family income, year, state, metro")):
            for grp, gen in gmap.items():
                g = gaps[(gaps.measure == measure) & (gaps.spec == spec) & (gaps.group == grp)].iloc[0]
                rr = r[r.group == grp].iloc[0]
                rows.append(dict(source="CPS Sept 2021+2023 (service_by_ses_2026_09_23)",
                                 measure=measure + (" (men born 1956+)" if measure == "veteran" else ""),
                                 generation=gen, n=int(rr.n), rate=100 * rr.rate, white_rate=100 * white.rate,
                                 estimate=g.gap_points, se=g.se_points, adjustment=label, units="points"))
    return rows


def voting():
    v = pd.read_csv(HERE / "derived" / "voting.csv")
    v = v[v.year == "pooled_2020_2022_2024"]
    gmap = {"mexico_born_naturalized": "G1", "mexican_2nd_gen": "G2", "mexican_3rd_plus": "G3+"}
    rows = []
    for m in ("voted", "registered"):
        rate = v[v.measure == f"{m}_rate"].set_index("generation")
        for adj in v[v.measure == f"{m}_gap"].adjustment.unique():
            for grp, gen in gmap.items():
                g = v[(v.measure == f"{m}_gap") & (v.adjustment == adj) & (v.generation == grp)].iloc[0]
                rows.append(dict(source="CPS Nov 2020/2022/2024 (this lane; G1 = naturalized citizens)",
                                 measure=m, generation=gen, n=int(rate.loc[grp, "n"]),
                                 rate=100 * rate.loc[grp, "estimate"], white_rate=100 * rate.loc["usb_nh_white", "estimate"],
                                 estimate=100 * g.estimate, se=100 * g.se, adjustment=adj, units="points"))
    return rows


def endogamy():
    d = pd.read_csv(HERE / "derived" / "intermarriage.csv")
    gmap = {"mex_G1": "G1", "mex_G2": "G2", "mex_G3plus": "G3+"}
    rows = []
    raw_share = d[(d.measure == "spouse_mexican_origin") & (d.adjustment == "raw")].set_index("generation")
    for adj in d.adjustment.unique():
        for grp, gen in gmap.items():
            g = d[(d.measure == "excess_mexican_spouse_over_random") & (d.adjustment == adj) & (d.generation == grp)]
            if g.empty:
                continue
            g = g.iloc[0]
            rows.append(dict(source="CPS ASEC 2022-2025 (this lane), married 25-54",
                             measure="endogamy: Mexican-origin spouse in excess of random matching within state",
                             generation=gen, n=int(g.n), rate=100 * raw_share.loc[grp, "estimate"], white_rate=np.nan,
                             estimate=100 * g.estimate, se=100 * g.se, units="points",
                             adjustment="raw" if adj == "raw" else adj.replace(" at pooled Mexican-origin profile", "")))
    return rows


def norms():
    rows = []
    items = {("gss", "tolscale_classic15"): "civil-liberties tolerance, Stouffer 15 items (scale points)",
             ("gss", "con_index_all13"): "confidence in 13 institutions (1-3 scale)",
             ("gss", "conarmy_great"): "'a great deal' of confidence in the military (share)",
             ("gss", "obey_top2"): "obedience ranked top-2 child value (share)",
             ("gss", "redist"): "government should reduce income differences (7-point)",
             ("anes", "violence_justified"): "political violence at least 'a little' justified (share)"}
    for (src, item), label in items.items():
        f = pd.read_csv(NORMS / f"{src}_adjusted.csv")
        f = f[f["item"] == item]
        for model, adj in (("raw", "raw"), ("adj_mex", "age, age^2, years of education, log family income, year")):
            for gen in GENS:
                c = f[(f.model == model) & f.contrast.str.fullmatch(rf"Mex {re.escape(gen)} vs (NHWhite|white) G3\+")]
                if c.empty:
                    continue
                c = c.iloc[0]
                scale = 100 if "(share)" in label else 1
                rows.append(dict(source=f"{src.upper()} (norms_gen_2026_09_18)", measure=label, generation=gen,
                                 n=int(c.n), rate=np.nan, white_rate=np.nan, estimate=scale * c.estimate,
                                 se=scale * c.se, adjustment=adj, units="points" if scale == 100 else "scale"))
    return rows


def military_context():
    m = pd.read_csv(SVC / "military_rates.csv")
    m = m[(m.universe == "all") & m.group.isin(["usb_mexican_hisp", "mexico_born", "mexico_born_naturalized"])]
    keep = [("men", "18_49", "ever_active_duty"), ("women", "18_49", "ever_active_duty"),
            ("men", "18_24", "now_active_duty"), ("women", "18_24", "now_active_duty")]
    rows = []
    for sex, band, outcome in keep:
        for _, r in m[(m.sex == sex) & (m.age_band == band) & (m.outcome == outcome)].iterrows():
            rows.append(dict(source="ACS 2022-2024 (service_by_ses_2026_09_23)",
                             measure=f"{outcome}, {sex} {band} (ratio to US-born NH white)",
                             generation={"usb_mexican_hisp": "US-born (G2+G3+)", "mexico_born": "G1",
                                         "mexico_born_naturalized": "G1 naturalized"}[r.group],
                             n=int(r.n_records), rate=100 * r.rate, white_rate=np.nan, estimate=r.ratio_to_nh_white,
                             se=r.ratio_se, adjustment="raw", units="ratio"))
    return rows


def add_rho(t):
    t = t.copy()
    t["rho_from_previous"], t["rho_se"], t["rho_g1_to_g3plus"] = np.nan, np.nan, np.nan
    for (_, _, _), grp in t[t.generation.isin(GENS)].groupby(["source", "measure", "adjustment"]):
        by = grp.set_index("generation")
        pairs = [("G1", "G2"), ("G2", "G3+")] + [("G1", "G3+")]
        for a, b in pairs:
            if a not in by.index or b not in by.index:
                continue
            ga, sa, gb, sb = by.loc[a, "estimate"], by.loc[a, "se"], by.loc[b, "estimate"], by.loc[b, "se"]
            if abs(ga) < 2 * sa:
                continue
            rho = gb / ga
            rse = abs(rho) * np.sqrt((sa / ga) ** 2 + (sb / gb) ** 2) if gb != 0 else sb / abs(ga)
            idx = grp.index[grp.generation == b][0]
            if (a, b) == ("G1", "G3+"):
                t.loc[idx, "rho_g1_to_g3plus"] = rho
            else:
                t.loc[idx, "rho_from_previous"], t.loc[idx, "rho_se"] = rho, rse
    return t


def main():
    t = pd.DataFrame(cps_sept() + voting() + endogamy() + norms())
    t = add_rho(t)
    t = pd.concat([t, pd.DataFrame(military_context())], ignore_index=True)
    cols = ["source", "measure", "generation", "n", "estimate", "se", "adjustment", "units", "rate", "white_rate",
            "rho_from_previous", "rho_se", "rho_g1_to_g3plus"]
    t[cols].to_csv(HERE / "derived" / "civic_carryover.csv", index=False, float_format="%.6g", lineterminator="\n")
    s = t[t.generation.isin(GENS)].copy()
    s["cell"] = s.estimate.round(2).astype(str) + " (" + s.se.round(2).astype(str) + ")"
    s["rho"] = s.rho_from_previous.round(2)
    print(s.pivot_table(index=["measure", "adjustment"], columns="generation", values=["cell", "rho"],
                        aggfunc="first").to_string())


if __name__ == "__main__":
    sys.exit(main())
