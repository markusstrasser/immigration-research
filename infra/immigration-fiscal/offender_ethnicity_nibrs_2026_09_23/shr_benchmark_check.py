"""Is the SHR homicide benchmark behind the calibrated victim-conditional arm representative of
the nation, and does the tract exposure model reproduce it outside the states it is fitted on?

    uv run --no-project python3 shr_benchmark_check.py      (after nibrs_rates.py)

The calibrated arm shifts every offence so that NIBRS murder, carried to the nation, matches the
SHR's national P(offender Hispanic | victim group): 0.719 for Hispanic victims in 2024. The SHR
holds only reporting agencies' victims (2,376 Hispanic victims in 2024 against 3,776 Hispanic
homicide deaths in CDC WONDER). This check recomputes the benchmark state by state from the MAP
compilation (cleared cases, first offender, the homicide lane's coding) and
  1. reweights the state values to each state's residents of the victim group (ACS 2020-2024
     B03001 tract sums, the victim lane's cache), over states with at least MIN_CASES cases;
  2. drops Texas, Arizona and California, the states the NIBRS inputs come from;
  3. predicts each state's value with the central NIBRS murder delta on that state's tracts
     (derived/offender_given_victim_transfer.csv) and compares like for like, states weighted
     by their SHR cases.
Writes derived/shr_benchmark_by_state.csv and derived/shr_benchmark_check.csv.
"""
from __future__ import annotations

import hashlib

import numpy as np
import pandas as pd

from nibrs_rates import GROUPS, HOM, OUT, SHR_SHA256, VL, gate, load_tracts

MIN_CASES = 20
WINDOWS = {"2024": (2024, 2024), "2022_2024": (2022, 2024)}
NIBRS_STATES = {"Texas", "Arizona", "California"}


def eth(race: pd.Series, ethnic: pd.Series) -> pd.Series:
    """The homicide lane's coding, as in nibrs_rates.shr_state_check."""
    out = pd.Series("unknown", index=race.index, dtype=object)
    nonh = ethnic.eq("Not of Hispanic origin")
    out[nonh & race.eq("White")] = "NHW"
    out[nonh & race.eq("Black")] = "NHB"
    out[nonh & race.isin(["Asian", "American Indian or Alaskan Native", "Native Hawaiian or Pacific Islander"])] = "NHO"
    out[ethnic.eq("Hispanic origin")] = "H"
    return out


def load_shr() -> pd.DataFrame:
    raw = HOM / "_cache/SHR76_25a.csv"
    h = hashlib.sha256()
    with open(raw, "rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    gate("SHR76_25a.csv sha256 equals the homicide lane's pin", h.hexdigest() == SHR_SHA256, h.hexdigest()[:12])
    df = pd.read_csv(raw, usecols=["Year", "State", "Solved", "Homicide", "Circumstance", "VicRace", "VicEthnic",
                                   "OffRace", "OffEthnic"], low_memory=False)
    df["State"] = df.State.replace({"Rhodes Island": "Rhode Island"})     # the MAP file's spelling
    df = df[df.Homicide.eq("Murder and non-negligent manslaughter")
            & ~df.Circumstance.isin({"Felon killed by police", "Felon killed by private citizen"})
            & df.Year.between(2022, 2024)].copy()
    df["off"] = eth(df.OffRace, df.OffEthnic)
    df["vic"] = eth(df.VicRace, df.VicEthnic)
    df["vgrp"] = np.where(df.vic.eq("H"), "H", np.where(df.vic.isin(["NHW", "NHB", "NHO"]), "NH", "unknown"))
    df["known"] = df.Solved.eq("Yes") & df.off.isin(GROUPS)
    return df


def main() -> None:
    shr = load_shr()
    held = pd.read_csv(VL / "derived/shr_p_offender_given_victim.csv").set_index(["window", "victim"])
    k24 = shr[shr.Year.eq(2024) & shr.known & shr.vic.eq("H")]
    gate("2024 Hispanic-victim benchmark reproduces the victim lane (1,085 / 1,509 = 0.719)",
         len(k24) == held.loc[("2024", "hispanic"), "cleared_off_eth_known"]
         and int(k24.off.eq("H").sum()) == held.loc[("2024", "hispanic"), "off_hispanic"],
         f"{int(k24.off.eq('H').sum())} / {len(k24)}")

    t = load_tracts()
    t["state_name"] = t.NAME.str.split("; ").str[-1]
    e = (t.B03001_003E / t.B03001_001E).clip(0.001, 0.999).to_numpy()
    t["logit_e"] = np.log(e / (1 - e))
    t["w_H"] = t.B03001_003E.astype(float)
    t["w_NH"] = (t.B03001_001E - t.B03001_003E).astype(float)
    ogv = pd.read_csv(OUT / "offender_given_victim_transfer.csv")
    mrow = ogv[ogv.spec.eq("central") & ogv.offence.eq("Murder")].set_index("victims")
    delta = {g: float(mrow.loc[g, "delta"]) for g in ["H", "NH"]}
    t_model = {g: float(mrow.loc[g, "p_off_hispanic_national"]) for g in ["H", "NH"]}
    pop = {g: t.groupby("state_name")[f"w_{g}"].sum() for g in ["H", "NH"]}
    pred = {}
    for g in ["H", "NH"]:
        p = t[f"w_{g}"] / (1 + np.exp(-(t.logit_e + delta[g])))
        pred[g] = p.groupby(t.state_name).sum() / pop[g]
        allp = float(p.sum() / t[f"w_{g}"].sum())
        gate(f"national model value reproduces the transfer file ({g} victims)", abs(allp - t_model[g]) < 5e-4,
             f"{allp:.4f} vs {t_model[g]:.4f}")

    rows, summ = [], []
    for win, (y0, y1) in WINDOWS.items():
        d = shr[shr.Year.between(y0, y1)]
        for g in ["H", "NH"]:
            dg = d[d.vgrp.eq(g)]
            kg = dg[dg.known]
            by = pd.DataFrame({"shr_victims": dg.groupby("State").size(), "cleared_known": kg.groupby("State").size(),
                               "off_hispanic": kg.groupby("State").off.apply(lambda s: int(s.eq("H").sum()))}).fillna(0)
            by["p_shr"] = by.off_hispanic / by.cleared_known
            by["p_model"] = pred[g].reindex(by.index)
            by["residents"] = pop[g].reindex(by.index)
            unmatched = sorted(set(by.index) - set(pop[g].index))
            by = by.drop(unmatched)
            for st, r in by.iterrows():
                rows.append(dict(window=win, victims=g, state=st, **r.to_dict()))
            ok = by[by.cleared_known >= MIN_CASES]
            out_ = by[~by.index.isin(NIBRS_STATES)]
            tx_az = by[by.index.isin({"Texas", "Arizona"})]
            ca = by[by.index.isin({"California"})]

            def pooled(x: pd.DataFrame) -> float:
                return float(x.off_hispanic.sum() / x.cleared_known.sum())

            def model_like(x: pd.DataFrame) -> float:
                return float((x.p_model * x.cleared_known).sum() / x.cleared_known.sum())

            summ += [
                dict(window=win, victims=g, measure="SHR, all reporting states (pooled cases)", value=pooled(by),
                     cleared_known=by.cleared_known.sum(), residents_share=np.nan),
                dict(window=win, victims=g, measure=f"SHR, state values weighted by residents (states with >= {MIN_CASES} cases)",
                     value=float((ok.p_shr * ok.residents).sum() / ok.residents.sum()),
                     cleared_known=ok.cleared_known.sum(), residents_share=float(ok.residents.sum() / pop[g].sum())),
                dict(window=win, victims=g, measure="SHR, outside TX, AZ and CA (pooled cases)", value=pooled(out_),
                     cleared_known=out_.cleared_known.sum(), residents_share=float(out_.residents.sum() / pop[g].sum())),
                dict(window=win, victims=g, measure="model, outside TX, AZ and CA (SHR case weights)", value=model_like(out_),
                     cleared_known=out_.cleared_known.sum(), residents_share=np.nan),
                dict(window=win, victims=g, measure="SHR, TX and AZ (pooled cases)", value=pooled(tx_az),
                     cleared_known=tx_az.cleared_known.sum(), residents_share=np.nan),
                dict(window=win, victims=g, measure="model, TX and AZ (SHR case weights)", value=model_like(tx_az),
                     cleared_known=tx_az.cleared_known.sum(), residents_share=np.nan),
                dict(window=win, victims=g, measure="SHR, CA (pooled cases)", value=pooled(ca),
                     cleared_known=ca.cleared_known.sum(), residents_share=np.nan),
                dict(window=win, victims=g, measure="model, CA", value=model_like(ca),
                     cleared_known=ca.cleared_known.sum(), residents_share=np.nan),
                dict(window=win, victims=g, measure="model, nation (residents' tracts; the uncalibrated arm)",
                     value=t_model[g], cleared_known=np.nan, residents_share=1.0),
            ]
            if unmatched:
                print(f"  ! {win} {g}: SHR states without tracts dropped: {unmatched}")
    by_state = pd.DataFrame(rows)
    check = pd.DataFrame(summ)
    by_state.to_csv(OUT / "shr_benchmark_by_state.csv", index=False, float_format="%.4f")
    check.to_csv(OUT / "shr_benchmark_check.csv", index=False, float_format="%.4f")
    print(check.to_string(index=False, float_format=lambda v: f"{v:,.3f}"))
    top = by_state[by_state.window.eq("2022_2024") & by_state.victims.eq("H")].sort_values("cleared_known", ascending=False)
    print("\n2022-2024, Hispanic victims, largest states:")
    print(top.head(15)[["state", "shr_victims", "cleared_known", "p_shr", "p_model", "residents"]]
          .to_string(index=False, float_format=lambda v: f"{v:,.3f}" if v < 10 else f"{v:,.0f}"))


if __name__ == "__main__":
    main()
