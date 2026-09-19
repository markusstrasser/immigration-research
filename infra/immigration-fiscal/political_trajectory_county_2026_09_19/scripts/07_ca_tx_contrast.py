#!/usr/bin/env python3
"""Arm 3: California and Texas, two states with a similar Mexican-origin share and
opposite politics. If composition drove outcomes, the two should have converged.

Series built here, 2000-2024:
  - Mexican-origin and Hispanic share of the state population (county panel)
  - Hispanic share of the citizen voting-age population and of actual voters
    (CPS November supplement, script 05)
  - presidential Democratic two-party share (county panel summed to the state)
  - the same share computed only over counties below 10% (and below 5%)
    Mexican-origin: a within-state stand-in for the non-Hispanic vote that uses
    no survey at all
  - an Oaxaca-style split of the CA-TX gap into a composition term (the Hispanic
    share of voters differs) and a conversion term (everybody else votes
    differently), using the national exit-poll Hispanic Democratic share

Output: derived/ca_tx_series.csv, derived/ca_tx_gap_decomposition.csv,
        derived/ca_tx.txt
"""
from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

LANE = Path(__file__).resolve().parent.parent
DER = LANE / "derived"
TXT: list[str] = []
STATES = {"06": "CA", "48": "TX"}


def say(s: str = "") -> None:
    print(s, flush=True)
    TXT.append(s)


def main() -> int:
    p = pd.read_csv(DER / "county_panel.csv", dtype={"fips": str, "state": str})
    p["mex_pp"] = 100 * p.mex_share
    cps = pd.read_csv(DER / "cps_voting_state.csv",
                      dtype={"state_fips": str})
    part = pd.read_csv(DER / "partisanship_series.csv")

    rows = []
    for st, ab in STATES.items():
        d = p[p.state == st]
        for y, g in d.groupby("year"):
            dem2p = 100 * g.dem.sum() / (g.dem.sum() + g.rep.sum())
            low10 = g[g.mex_pp < 10]
            low5 = g[g.mex_pp < 5]
            c = cps[(cps.state_fips == st) & (cps.year == y)]
            hisp_v = c[c.group != "non_hispanic"].voters_m.sum()
            all_v = c.voters_m.sum()
            mex_v = c[c.group == "mexican"].voters_m.sum()
            hisp_c = c[c.group != "non_hispanic"].cvap_m.sum()
            all_c = c.cvap_m.sum()
            rows.append({
                "state": ab, "year": y,
                "mex_share_pop_pp": 100 * g.mex.sum() / g["pop"].sum(),
                "hisp_share_pop_pp": 100 * g.hisp.sum() / g["pop"].sum(),
                "dem2p_pp": dem2p,
                "dem2p_counties_under10pct_mex": (
                    100 * low10.dem.sum() / (low10.dem.sum() + low10.rep.sum())
                    if len(low10) else np.nan),
                "share_of_state_votes_in_those_counties": (
                    100 * low10.total_votes.sum() / g.total_votes.sum()
                    if len(low10) else np.nan),
                "dem2p_counties_under5pct_mex": (
                    100 * low5.dem.sum() / (low5.dem.sum() + low5.rep.sum())
                    if len(low5) else np.nan),
                "cps_hisp_share_of_voters_pp": (100 * hisp_v / all_v
                                                if all_v > 0 else np.nan),
                "cps_mex_share_of_voters_pp": (100 * mex_v / all_v
                                               if all_v > 0 else np.nan),
                "cps_hisp_share_of_cvap_pp": (100 * hisp_c / all_c
                                              if all_c > 0 else np.nan),
                "total_votes": g.total_votes.sum()})
    ser = pd.DataFrame(rows).sort_values(["state", "year"])
    ser.to_csv(DER / "ca_tx_series.csv", index=False)

    say("=== California and Texas, 2000-2024 ===")
    for c in ("mex_share_pop_pp", "hisp_share_pop_pp", "dem2p_pp",
              "dem2p_counties_under10pct_mex", "cps_hisp_share_of_voters_pp",
              "cps_hisp_share_of_cvap_pp"):
        say(f"\n{c}")
        say(ser.pivot(index="year", columns="state", values=c).round(2).to_string())

    say()
    say("share of each state's votes cast in counties under 10% Mexican origin")
    say(ser.pivot(index="year", columns="state",
                  values="share_of_state_votes_in_those_counties")
        .round(1).to_string())

    # Oaxaca-style split of the CA - TX gap
    pv = ser.pivot(index="year", columns="state")
    ex = part.set_index("year")["hisp_dem2p"]
    dec = []
    for y in sorted(ser.year.unique()):
        if y not in ex.index or np.isnan(pv[("cps_hisp_share_of_voters_pp", "CA")]
                                         .get(y, np.nan)):
            continue
        sCA = pv[("cps_hisp_share_of_voters_pp", "CA")][y] / 100
        sTX = pv[("cps_hisp_share_of_voters_pp", "TX")][y] / 100
        DCA = pv[("dem2p_pp", "CA")][y]
        DTX = pv[("dem2p_pp", "TX")][y]
        dh = ex[y]
        # back out the non-Hispanic Democratic two-party share in each state
        nCA = (DCA - sCA * dh) / (1 - sCA)
        nTX = (DTX - sTX * dh) / (1 - sTX)
        sbar, nbar = (sCA + sTX) / 2, (nCA + nTX) / 2
        comp = (sCA - sTX) * (dh - nbar)
        conv = (1 - sbar) * (nCA - nTX)
        dec.append({"year": y, "gap_CA_minus_TX_pp": DCA - DTX,
                    "hisp_share_of_voters_CA_pp": 100 * sCA,
                    "hisp_share_of_voters_TX_pp": 100 * sTX,
                    "hisp_dem2p_national_pp": dh,
                    "nonhisp_dem2p_CA_pp": nCA, "nonhisp_dem2p_TX_pp": nTX,
                    "composition_term_pp": comp, "conversion_term_pp": conv,
                    "residual_pp": (DCA - DTX) - comp - conv})
    dd = pd.DataFrame(dec)
    dd.to_csv(DER / "ca_tx_gap_decomposition.csv", index=False)
    say()
    say("=== splitting the California minus Texas gap ===")
    say("composition = the two states' Hispanic shares of the electorate differ;")
    say("conversion  = everyone else votes differently. Hispanic Democratic share "
        "is the national exit-poll number in both states (stated assumption).")
    say(dd.round(2).to_string(index=False))
    say()
    m = dd.mean(numeric_only=True)
    say(f"averaged over {len(dd)} elections: gap {m.gap_CA_minus_TX_pp:+.1f} points, "
        f"of which composition {m.composition_term_pp:+.1f} and conversion "
        f"{m.conversion_term_pp:+.1f}; the non-Hispanic Democratic two-party share "
        f"is {m.nonhisp_dem2p_CA_pp:.1f} in California against "
        f"{m.nonhisp_dem2p_TX_pp:.1f} in Texas.")
    lo = ser.pivot(index="year", columns="state",
                   values="dem2p_counties_under10pct_mex")
    say(f"survey-free cross-check: in counties under 10% Mexican origin the "
        f"Democratic two-party share averages {lo['CA'].mean():.1f} in California "
        f"and {lo['TX'].mean():.1f} in Texas, a gap of "
        f"{lo['CA'].mean() - lo['TX'].mean():+.1f} points with no Hispanic voters "
        f"of consequence in either set.")
    (DER / "ca_tx.txt").write_text("\n".join(TXT) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
