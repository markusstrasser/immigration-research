"""Rents and house values against the 2000-2010 foreign-born inflow, instrumented.

The causal leg the California-Texas housing memo specified and left unstarted: a 2000-2010
metro long difference of log rent and log value on the change in the foreign-born share,
with the displacement lane's settlement shift-share (Z) and the ancestry push-pull
prediction (Z2, lane ancestry_instrument_2026_09_22) as instruments, plus an interaction
with Saiz (2010) supply elasticity on the metros that match his MSA list.

Deviations from the memo's wording, stated: the treatment is the all-foreign-born share, not
the Mexican-born share, because the 2000 SF3 endpoint in the displacement lane's panel has
no Mexico-born count for most metros (its Mexico arm has n = 25); native net migration by
education is not built (no 2000 metro endpoint on disk).

Reads  derived/county_housing_2000_2010.csv (fetch.py),
       ../ancestry_instrument_2026_09_22/derived/cbsa_predicted_inflow.csv,
       ../displacement_transfers_2026_09_18/derived/{metro_panel,base_shares_pre1990,national_stock}.csv,
       ../hedonic_composition_2026_09_19/derived/geo_county_cbsa_2013.csv,
       sources/.../lifetime/saiz/saiz_2010_msa_elasticity.dta
Writes derived/metro_housing_panel.csv, derived/estimates.csv, derived/summary.json

Run from the repository root (statsmodels and scipy are not in the main venv):
  OPENBLAS_NUM_THREADS=1 uv run --no-project --with statsmodels --with scipy \
    python3 infra/immigration-fiscal/housing_causal_2000_2010_2026_09_22/estimate.py
"""
from __future__ import annotations

import json
import pathlib
import re
import sys

import numpy as np
import pandas as pd

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[2]
ANC = HERE.parent / "ancestry_instrument_2026_09_22"
sys.path.insert(0, str(ANC))
from second_instrument import panel, tsls, wls  # noqa: E402  (same estimators, same panel)

XW = HERE.parent / "hedonic_composition_2026_09_19" / "derived" / "geo_county_cbsa_2013.csv"
SAIZ = ROOT / "sources/immigration-fiscal/data/external/lifetime/saiz/saiz_2010_msa_elasticity.dta"
DERIVED = HERE / "derived"


def metro_housing():
    c = pd.read_csv(DERIVED / "county_housing_2000_2010.csv", dtype={"county_fips": str})
    xw = pd.read_csv(XW, dtype={"county_fips": str, "cbsa": str})
    m = c.merge(xw[["county_fips", "cbsa"]], on="county_fips", how="inner")
    m = m.dropna(subset=["rent_med_2000", "rent_med_2010", "value_med_2000", "value_med_2010"])

    def windex(g, col, w):
        return np.average(g[col], weights=g[w]) if g[w].sum() > 0 else np.nan

    rows = []
    for cbsa, g in m.groupby("cbsa"):
        rows.append(dict(
            cbsa=cbsa, counties=len(g),
            rent_2000=windex(g, "rent_med_2000", "renters_2000"),
            rent_2010=windex(g, "rent_med_2010", "renters_2010"),
            value_2000=windex(g, "value_med_2000", "owners_2000"),
            value_2010=windex(g, "value_med_2010", "owners_2010"),
            renters_2000=g.renters_2000.sum(), owners_2000=g.owners_2000.sum(),
            units_2000=g.units_2000.sum()))
    h = pd.DataFrame(rows)
    h["dlog_rent"] = np.log(h.rent_2010) - np.log(h.rent_2000)
    h["dlog_value"] = np.log(h.value_2010) - np.log(h.value_2000)
    h["log_rent_2000"] = np.log(h.rent_2000)
    h["log_value_2000"] = np.log(h.value_2000)
    return h


def saiz_by_cbsa(cbsa_titles):
    """First-city + state match of Saiz's 1999 MSA names to 2013 CBSA titles."""
    s = pd.read_stata(SAIZ)[["msaname", "elasticity", "WRLURI", "population"]]

    def key(name):
        name = re.sub(r"\s*\((MSA|PMSA|NECMA)\)\s*$", "", str(name))
        city, _, st = name.rpartition(",")
        city = city.split("-")[0].split("/")[0].strip().lower()
        st = st.strip().split("-")[0].split(" ")[0].strip().lower()
        return f"{city}|{st}"

    s["key"] = s.msaname.map(key)
    s = s.sort_values("population", ascending=False).drop_duplicates("key")
    t = cbsa_titles.copy()
    t["key"] = t.cbsa_title.map(key)
    out = t.merge(s[["key", "elasticity", "WRLURI"]], on="key", how="left")
    return out[["cbsa", "elasticity", "WRLURI"]]


def main():
    DERIVED.mkdir(exist_ok=True)
    h = metro_housing()
    pred = pd.read_csv(ANC / "derived" / "cbsa_predicted_inflow.csv", dtype={"cbsa": str})
    base = panel("ssi_rate")[["cbsa", "dX", "Z", "w", "pop"]]  # the displacement lane's rows
    titles = pd.read_csv(HERE.parent / "displacement_transfers_2026_09_18" / "derived" / "metro_panel.csv",
                         dtype={"cbsa": str})[["cbsa", "cbsa_title"]].drop_duplicates("cbsa")
    sz = saiz_by_cbsa(titles)
    m = base.merge(h, on="cbsa").merge(pred, on="cbsa").merge(sz, on="cbsa", how="left")
    m["Z2"] = 100.0 * m.pred_2000s_all / m["pop"]
    m.to_csv(DERIVED / "metro_housing_panel.csv", index=False)
    n = len(m)
    w = m["w"].to_numpy()
    print(f"  metros {n}; with a Saiz elasticity {int(m.elasticity.notna().sum())}")

    rows = []

    def add(outcome, **kw):
        rows.append(dict(outcome=outcome, n=n, **kw))

    for zname in ("Z", "Z2"):
        r = wls(m["dX"], m[[zname]], w)
        add("first stage", estimator=f"dX on {zname}", coef=r.params[zname], se=r.bse[zname],
            F=(r.params[zname] / r.bse[zname]) ** 2)
    for outcome, lvl in (("dlog_rent", "log_rent_2000"), ("dlog_value", "log_value_2000")):
        y = m[outcome]
        r = wls(y, m[["dX"]], w)
        add(outcome, estimator="OLS", coef=r.params["dX"], se=r.bse["dX"])
        r = wls(y, m[["dX", lvl]], w)
        add(outcome, estimator="OLS + 2000 level", coef=r.params["dX"], se=r.bse["dX"])
        for zname, zcols in (("Z", ["Z"]), ("Z2", ["Z2"]), ("Z+Z2", ["Z", "Z2"])):
            r = wls(y, m[zcols], w)
            if len(zcols) == 1:
                add(outcome, estimator=f"reduced form on {zname}", coef=r.params[zname], se=r.bse[zname])
            X = np.column_stack([np.ones(n), m.dX])
            Zm = np.column_stack([np.ones(n), m[zcols].to_numpy()])
            b, se, J, p = tsls(y, X, Zm, w)
            add(outcome, estimator=f"IV with {zname}", coef=b[1], se=se[1], hansen_p=p)
            Xc = np.column_stack([np.ones(n), m.dX, m[lvl]])
            Zc = np.column_stack([np.ones(n), m[zcols].to_numpy(), m[lvl]])
            b, se, J, p = tsls(y, Xc, Zc, w)
            add(outcome, estimator=f"IV with {zname} + 2000 level", coef=b[1], se=se[1], hansen_p=p)
        # supply-elasticity interaction on the Saiz-matched metros: inelastic = below the
        # matched sample's population-weighted median elasticity
        s = m.dropna(subset=["elasticity"]).copy()
        ws = s["w"].to_numpy()
        med = np.median(np.repeat(s.elasticity.to_numpy(), (ws / ws.min()).round().astype(int).clip(1, 10_000)))
        s["inel"] = (s.elasticity < med).astype(float)
        s["dX_inel"] = s.dX * s.inel
        s["Z2_inel"] = s.Z2 * s.inel
        ns = len(s)
        Xi = np.column_stack([np.ones(ns), s.dX, s.dX_inel, s.inel])
        Zi = np.column_stack([np.ones(ns), s.Z2, s.Z2_inel, s.inel])
        b, se, J, p = tsls(s[outcome], Xi, Zi, ws)
        rows.append(dict(outcome=outcome, n=ns, estimator="IV with Z2, elastic metros (dX)",
                         coef=b[1], se=se[1], note=f"median elasticity {med:.2f}"))
        rows.append(dict(outcome=outcome, n=ns, estimator="IV with Z2, extra effect in inelastic metros (dX x inelastic)",
                         coef=b[2], se=se[2], note=f"median elasticity {med:.2f}"))
        r = wls(s["dX"], s[["Z2", "Z2_inel", "inel"]], ws)
        rows.append(dict(outcome=outcome, n=ns, estimator="first stage, interaction spec: dX_inel on Z2_inel",
                         coef=wls(s["dX_inel"], s[["Z2", "Z2_inel", "inel"]], ws).params["Z2_inel"],
                         se=wls(s["dX_inel"], s[["Z2", "Z2_inel", "inel"]], ws).bse["Z2_inel"]))
    est = pd.DataFrame(rows)
    est["lo"] = est.coef - 1.96 * est.se
    est["hi"] = est.coef + 1.96 * est.se
    est.to_csv(DERIVED / "estimates.csv", index=False)
    with pd.option_context("display.width", 200, "display.max_rows", 100):
        print(est[["outcome", "estimator", "n", "coef", "se", "lo", "hi", "F", "hansen_p"]].to_string(index=False))
    summary = dict(n=n, saiz_matched=int(m.elasticity.notna().sum()),
                   mean_dlog_rent=float(np.average(m.dlog_rent, weights=w)),
                   mean_dlog_value=float(np.average(m.dlog_value, weights=w)),
                   mean_dX=float(np.average(m.dX, weights=w)))
    (DERIVED / "summary.json").write_text(json.dumps(summary, indent=1))
    print(json.dumps(summary, indent=1))


if __name__ == "__main__":
    main()
