"""Arm 1, national homicide: victim-conditional imputation of unsolved and ethnicity-missing SHR
offenders with covariates, carried to 2024 homicide deaths as the victim lane does.

    uv run --no-project --with pandas --with numpy --with scikit-learn python3 \
        infra/immigration-fiscal/crime_ratio_direction_2026_09_24/shr_impute.py

The victim lane (`crime_victim_cost_2026_09_23/homicide_inputs.py`) takes P(first offender
Hispanic | victim group) from cleared, ethnicity-known 2024 SHR victims and applies it to CDC
WONDER 2024 deaths, which imputes every unsolved or ethnicity-missing case at its victim group's
national rate. Here the same imputation conditions on more: the state and agency, victim age and
sex, weapon, situation and circumstance class, and year; and an offender whose race is recorded
but whose ethnicity is not is split within that race. Positive control first: the lane's 2024
shares (Hispanic victims 0.7190, NH white 0.1020) and its Hispanic / NH-white homicide offending
ratio of 2.74.

Offender groups: hispanic, nh_white, nh_black, nh_other (the homicide lane's `ethnicity()`).
"""
from __future__ import annotations

import hashlib
import sys
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
FISCAL = HERE.parent
HOM = FISCAL / "homicide_cost_2026_09_18"
VL = FISCAL / "crime_victim_cost_2026_09_23"
NCVS = FISCAL / "ncvs_victim_offender_2026_09_18"
OUT = HERE / "derived"
sys.path.insert(0, str(HOM))
import shr_analysis as shr  # noqa: E402

SHR_SHA256 = "eeedbf5e58a4a2e91d88e8078341210bd2034b57e6d42d0e2de2667020b88a12"
G = ["hispanic", "nh_white", "nh_black", "nh_other"]
LOG: list[str] = []


def say(s: str = "") -> None:
    print(s, flush=True)
    LOG.append(s)


def gate(name: str, ok: bool, detail: str) -> None:
    say(f"[gate] {name}: {'PASS' if ok else 'FAIL'} - {detail}")
    if not ok:
        raise SystemExit(f"[BLOCKED] gate failed: {name}")


def weapon(s: pd.Series) -> pd.Series:
    out = pd.Series("other", index=s.index, dtype=object)
    out[s.isin(["Handgun - pistol, revolver, etc", "Firearm, type not stated", "Rifle", "Other gun", "Shotgun"])] = "firearm"
    out[s.eq("Knife or cutting instrument")] = "knife"
    out[s.eq("Personal weapons, includes beating")] = "personal"
    out[s.isin(["Other or type unknown", "Weapon Not Reported"])] = "unknown"
    return out


def load() -> pd.DataFrame:
    h = hashlib.sha256(shr.RAW.read_bytes()).hexdigest()
    gate("SHR76_25a.csv sha256 equals the homicide lane's pin", h == SHR_SHA256, h[:12])
    cols = shr.COLS + ["Ori", "Situation", "OffCount", "VicCount"]
    df = pd.read_csv(shr.RAW, usecols=sorted(set(cols)), low_memory=False)
    df = df[df.Homicide.eq("Murder and non-negligent manslaughter") & ~df.Circumstance.isin(shr.JUSTIFIABLE)]
    df = df[df.Year.between(2019, 2024)].copy()
    df["vic_eth"] = shr.ethnicity(df.VicRace, df.VicEthnic)
    df["off_eth"] = shr.ethnicity(df.OffRace, df.OffEthnic)
    df.loc[df.Solved.ne("Yes"), "off_eth"] = "unsolved"
    rr = pd.Series("u", index=df.index, dtype=object)
    rr[df.OffRace.eq("White")] = "W"
    rr[df.OffRace.eq("Black")] = "B"
    rr[df.OffRace.isin(["Asian", "American Indian or Alaskan Native", "Native Hawaiian or Pacific Islander"])] = "O"
    df["off_race"] = rr.where(df.Solved.eq("Yes"), "u")
    age = pd.to_numeric(df.VicAge, errors="coerce")
    age[age.ge(998)] = np.nan
    df["vageband"] = pd.cut(age, [-1, 14, 24, 34, 44, 54, 64, 200],
                            labels=["0-14", "15-24", "25-34", "35-44", "45-54", "55-64", "65+"]).astype(object)
    df["vageband"] = df.vageband.where(df.vageband.notna(), "unk")
    df["vsex"] = df.VicSex.where(df.VicSex.isin(["Male", "Female"]), "U")
    df["weapon"] = weapon(df.Weapon)
    circ = pd.Series("other", index=df.index, dtype=object)
    for k, s in shr.CIRC.items():
        circ[df.Circumstance.isin(s)] = k
    df["circ"] = circ
    df["multi_victim"] = df.Situation.str.startswith("Multiple victims")
    return df


def _all_cells(d: pd.DataFrame, keys: list[str]) -> pd.Index:
    """Every cell that occurs among all rows, so cells without a known offender inherit their
    parent's shares instead of falling back to the national victim-group base."""
    return pd.MultiIndex.from_frame(d[keys]).unique() if len(keys) > 1 else pd.Index(d[keys[0]].unique(), name=keys[0])


def shares_known(d: pd.DataFrame, keys: list[str]) -> pd.DataFrame:
    k = d[d.off_eth.isin(G)]
    t = pd.crosstab([k[c] for c in keys], k.off_eth).reindex(columns=G, fill_value=0)
    return t.reindex(_all_cells(d, keys), fill_value=0)


def race_pairs(d: pd.DataFrame, keys: list[str]) -> pd.DataFrame:
    """Counts of Hispanic vs non-Hispanic offenders within recorded race (solved, ethnicity known)."""
    k = d[d.off_eth.isin(G)]
    t = pd.crosstab([k[c] for c in keys] + [k.off_race], k.off_eth.eq("hispanic"))
    t.columns = ["nh" if not c else "h" for c in t.columns]
    t = t.reindex(columns=["h", "nh"], fill_value=0)
    return t.reindex(_all_cells(d, keys + ["off_race"]), fill_value=0)


def impute(d: pd.DataFrame, chain: list[list[str]], kappa: float) -> pd.DataFrame:
    """Row probabilities over G. Known rows: one-hot. Race-known ethnicity-missing rows: split
    within race by the cell's Hispanic share among offenders of that race. Others: cell shares.
    Cells: victim group (national), then each level of the chain, shrunk to its parent."""
    keys = ["vic_eth"]
    base = shares_known(d, keys)
    p = base.div(base.sum(axis=1), axis=0)
    pr_base = race_pairs(d, keys)
    q = (pr_base.h / (pr_base.h + pr_base.nh)).rename("q")
    for lev in chain:
        pkeys = list(keys)
        keys = keys + lev
        c = shares_known(d, keys)
        par = p.reindex(c.index.droplevel(lev) if len(pkeys) > 1 or len(lev) else c.index)
        par = pd.DataFrame(par.to_numpy(), index=c.index, columns=G)
        p = (c + kappa * par).div(c.sum(axis=1) + kappa, axis=0)
        rp = race_pairs(d, keys)
        qpar = q.reindex(rp.index.droplevel(lev))
        q = ((rp.h + kappa * qpar.to_numpy()) / (rp.h + rp.nh + kappa)).rename("q")
    # rows
    cell = d[keys].merge(p, left_on=keys, right_index=True, how="left")[G]
    # cells unseen among known offenders fall back to the victim-group base
    fb = d[["vic_eth"]].merge(base.div(base.sum(axis=1), axis=0), left_on="vic_eth", right_index=True, how="left")[G]
    cell = cell.fillna(fb)
    out = cell.copy()
    kn = d.off_eth.isin(G)
    out.loc[kn, G] = 0.0
    for g in G:
        out.loc[kn & d.off_eth.eq(g), g] = 1.0
    # race known, ethnicity missing (solved)
    qq = d[keys + ["off_race"]].merge(q, left_on=keys + ["off_race"], right_index=True, how="left").q
    qb = d[["vic_eth", "off_race"]].merge((pr_base.h / (pr_base.h + pr_base.nh)).rename("qb"),
                                          left_on=["vic_eth", "off_race"], right_index=True, how="left").qb
    qq = qq.fillna(qb)
    for r, g in [("W", "nh_white"), ("B", "nh_black"), ("O", "nh_other")]:
        m = (~kn) & d.Solved.eq("Yes") & d.off_race.eq(r)
        out.loc[m, G] = 0.0
        out.loc[m, "hispanic"] = qq[m].fillna(0.0)
        out.loc[m, g] = 1 - qq[m].fillna(0.0)
    if not np.allclose(out.sum(axis=1), 1.0):
        raise SystemExit("[BLOCKED] SHR row probabilities do not sum to one")
    return out


LOGIT_X = ["vic_eth", "State", "Ori", "vageband", "vsex", "weapon", "circ", "multi_victim", "Year"]


def logit_fit_predict(train: pd.DataFrame, test: pd.DataFrame, X: list[str], C: float) -> np.ndarray:
    from sklearn.linear_model import LogisticRegression
    from sklearn.preprocessing import OneHotEncoder

    enc = OneHotEncoder(handle_unknown="ignore", min_frequency=5)
    Z = enc.fit_transform(train[X].astype(str))
    y = train.off_eth.map({g: i for i, g in enumerate(G)}).to_numpy()
    clf = LogisticRegression(C=C, max_iter=3000)
    clf.fit(Z, y)
    pr = np.zeros((len(test), 4))
    pr[:, clf.classes_] = clf.predict_proba(enc.transform(test[X].astype(str)))
    return pr


INTER = ["vxState", "vxOri", "vxweapon", "vxage", "vxsex"]


def add_interactions(d: pd.DataFrame) -> pd.DataFrame:
    """Victim group crossed with state, agency, weapon, age and sex, so the logit can let each
    covariate act differently by victim group, as the nested cells do."""
    d = d.copy()
    for new, col in [("vxState", "State"), ("vxOri", "Ori"), ("vxweapon", "weapon"), ("vxage", "vageband"),
                     ("vxsex", "vsex")]:
        d[new] = d.vic_eth.astype(str) + "|" + d[col].astype(str)
    return d


def logit(d: pd.DataFrame, C: float = 1.0, X: list[str] = LOGIT_X) -> pd.DataFrame:
    kn = d.off_eth.isin(G)
    pr = logit_fit_predict(d[kn], d, X, C)
    out = pd.DataFrame(pr, index=d.index, columns=G)
    out.loc[kn, G] = 0.0
    for g in G:
        out.loc[kn & d.off_eth.eq(g), g] = 1.0
    # Race known, ethnicity missing: P(H | race r) = P(H) pi(r | H) / (P(H) pi(r | H) + P(NH race r)),
    # pi(r | H) = recorded-race distribution of known Hispanic offenders by victim group. (Using
    # P(H) / (P(H) + P(NH race r)) would treat every Hispanic offender as possibly Black or other.)
    kh = d[kn & d.off_eth.eq("hispanic")]
    pi = pd.crosstab(kh.vic_eth, kh.off_race, normalize="index").reindex(index=G, columns=["W", "B", "O", "u"]).fillna(0)
    for r, g in [("W", "nh_white"), ("B", "nh_black"), ("O", "nh_other")]:
        m = (~kn) & d.Solved.eq("Yes") & d.off_race.eq(r)
        mm = m.to_numpy()
        ph = pr[mm, 0] * d.loc[m, "vic_eth"].map(pi[r]).to_numpy()
        qh = ph / (ph + pr[mm, G.index(g)])
        out.loc[m, G] = 0.0
        out.loc[m, "hispanic"] = qh
        out.loc[m, g] = 1 - qh
    return out


def cv_check(d: pd.DataFrame, folds: int = 5) -> list[dict]:
    """Held-out calibration on ethnicity-known offenders: each fold's rows are masked (treated as
    unsolved, no race) and predicted from the other folds, by the victim-group base, the main
    chain and the logits. Reports log-loss and predicted vs actual Hispanic share, overall and in
    the strata where unknown cases concentrate."""
    rng = np.random.default_rng(7)
    kn = d.off_eth.isin(G).to_numpy()
    fold = np.full(len(d), -1)
    fold[kn] = rng.integers(0, folds, kn.sum())
    preds = {m: np.zeros((len(d), 4)) for m in ["victim group only", "chain state>weapon>victim age-sex>agency",
                                                 "logit all covariates", "logit without circumstance",
                                                 "logit without circumstance, victim-group interactions"]}
    di = add_interactions(d)
    noc = [x for x in LOGIT_X if x != "circ"]
    for f in range(folds):
        te = fold == f
        dm = d.copy()
        dm.loc[te, "off_eth"] = "unsolved"
        dm.loc[te, "Solved"] = "No"
        dm.loc[te, "off_race"] = "u"
        preds["victim group only"][te] = impute(dm, [], 20.0).to_numpy()[te]
        preds["chain state>weapon>victim age-sex>agency"][te] = impute(
            dm, [["State"], ["weapon"], ["vageband", "vsex"], ["Ori"]], 20.0).to_numpy()[te]
        tr = kn & ~te
        preds["logit all covariates"][te] = logit_fit_predict(d[tr], d[te], LOGIT_X, 1.0)
        preds["logit without circumstance"][te] = logit_fit_predict(d[tr], d[te], noc, 1.0)
        preds["logit without circumstance, victim-group interactions"][te] = logit_fit_predict(di[tr], di[te], noc + INTER, 1.0)
    y = d.off_eth.map({g: i for i, g in enumerate(G)})
    out = []
    strata = {"all known": kn, "circumstance undetermined": kn & d.circ.eq("undetermined").to_numpy(),
              "weapon unknown": kn & d.weapon.eq("unknown").to_numpy(),
              "victim Hispanic": kn & d.vic_eth.eq("hispanic").to_numpy(),
              "victim NH white": kn & d.vic_eth.eq("nh_white").to_numpy(),
              "California": kn & d.State.eq("California").to_numpy(), "Texas": kn & d.State.eq("Texas").to_numpy()}
    for m, pr in preds.items():
        for lab, msk in strata.items():
            yi = y[msk].astype(int).to_numpy()
            p = np.clip(pr[msk], 1e-9, 1)
            out.append(dict(model=m, stratum=lab, n=int(msk.sum()), actual_H=float((yi == 0).mean()),
                            predicted_H=float(pr[msk, 0].mean()),
                            log_loss=float(-np.log(p[np.arange(len(yi)), yi]).mean())))
    return out


def to_deaths(d: pd.DataFrame, P: pd.DataFrame, won: pd.Series, pop: pd.Series) -> dict:
    """P*(offender group | victim group) over all SHR victims of that group, applied to WONDER."""
    pv = P.groupby(d.vic_eth).mean().reindex(G)
    off = {o: float(sum(won[g] * pv.loc[g, o] for g in G)) for o in G}
    tot = sum(won[g] for g in G)
    rate = {"hispanic": off["hispanic"] / pop["Hispanic"], "nh_white": off["nh_white"] / pop["White"],
            "nh_black": off["nh_black"] / pop["Black"]}
    rall = tot / pop.sum()
    return dict(p_H_given_vH=pv.loc["hispanic", "hispanic"], p_H_given_vNHW=pv.loc["nh_white", "hispanic"],
                p_H_given_vNHB=pv.loc["nh_black", "hispanic"], p_H_given_vNHO=pv.loc["nh_other", "hispanic"],
                hispanic_offender_killings=off["hispanic"], share_H=off["hispanic"] / tot,
                RR_H_NHW=rate["hispanic"] / rate["nh_white"], RR_H_all=rate["hispanic"] / rall,
                RR_NHB_NHW=rate["nh_black"] / rate["nh_white"])


def main() -> None:
    OUT.mkdir(exist_ok=True)
    df = load()
    won = pd.read_csv(VL / "derived/wonder_2024_homicide_victims.csv").set_index("group").deaths_not_stated_allocated
    won = won.reindex(G)
    pop = pd.read_csv(NCVS / "derived/cv_population_12plus.csv")
    pop = pop[pop.year.eq(2024)].set_index("group").population
    lanep = pd.read_csv(VL / "derived/shr_p_offender_given_victim.csv")
    rows, cv_rows = [], []
    for w, (lo, hi) in {"2024": (2024, 2024), "2022_2024": (2022, 2024)}.items():
        d = df[df.Year.between(lo, hi)].reset_index(drop=True)
        d = d[d.vic_eth.isin(G)].reset_index(drop=True)
        # positive control: the lane's cleared-known shares and its 2.74 ratio (2024 WONDER x 2024 P)
        known = d[d.off_eth.isin(G)]
        lp = lanep[lanep.window.astype(str).eq(w)].set_index("victim")
        for g in G:
            got = float(known[known.vic_eth.eq(g)].off_eth.eq("hispanic").mean())
            gate(f"{w} P(offender Hispanic | victim {g}), cleared ethnicity-known, equals the victim lane",
                 abs(got - float(lp.loc[g, "p_off_hispanic"])) < 5e-7, f"{got:.6f}")
        pv = known.groupby("vic_eth").off_eth.value_counts(normalize=True).unstack(fill_value=0).reindex(index=G, columns=G)
        base_off = {o: float(sum(won[g] * pv.loc[g, o] for g in G)) for o in G}
        rr = (base_off["hispanic"] / pop["Hispanic"]) / (base_off["nh_white"] / pop["White"])
        if w == "2024":
            gate("victim lane's Hispanic / NH-white homicide offending ratio 2.7379", abs(rr - 2.7379) < 5e-4, f"{rr:.4f}")
        rows.append(dict(window=w, method="victim lane: cleared ethnicity-known, by victim group",
                         p_H_given_vH=pv.loc["hispanic", "hispanic"], p_H_given_vNHW=pv.loc["nh_white", "hispanic"],
                         p_H_given_vNHB=pv.loc["nh_black", "hispanic"], p_H_given_vNHO=pv.loc["nh_other", "hispanic"],
                         hispanic_offender_killings=base_off["hispanic"], share_H=base_off["hispanic"] / sum(won),
                         RR_H_NHW=rr, RR_H_all=(base_off["hispanic"] / pop["Hispanic"]) / (sum(won) / pop.sum()),
                         RR_NHB_NHW=(base_off["nh_black"] / pop["Black"]) / (base_off["nh_white"] / pop["White"])))
        say(f"[{w}] SHR victims of known ethnicity {len(d):,}; solved {d.Solved.eq('Yes').mean():.3f}; offender "
            f"ethnicity known {d.off_eth.isin(G).mean():.3f}; solved, race known, ethnicity missing "
            f"{(d.Solved.eq('Yes') & ~d.off_eth.isin(G) & d.off_race.ne('u')).mean():.3f}")
        specs = {
            "victim group only, race-known splits (ethnicity-missing solved split within race)": [],
            "+state": [["State"]],
            "+weapon": [["weapon"]],
            "+victim age and sex": [["vageband", "vsex"]],
            "+circumstance class": [["circ"]],
            "+situation (multiple victims)": [["multi_victim"]],
            "chain state>weapon>victim age-sex>agency (kappa 20)": [["State"], ["weapon"], ["vageband", "vsex"], ["Ori"]],
            "chain state>agency>weapon>victim age-sex (kappa 20)": [["State"], ["Ori"], ["weapon"], ["vageband", "vsex"]],
            "chain state>circumstance>weapon>victim age-sex (kappa 20)": [["State"], ["circ"], ["weapon"], ["vageband", "vsex"]],
        }
        for name, ch in specs.items():
            P = impute(d, ch, 20.0)
            rows.append(dict(window=w, method=name, **to_deaths(d, P, won, pop)))
        for kappa in [5.0, 100.0]:
            P = impute(d, specs["chain state>weapon>victim age-sex>agency (kappa 20)"], kappa)
            rows.append(dict(window=w, method=f"chain state>weapon>victim age-sex>agency (kappa {kappa:g})",
                             **to_deaths(d, P, won, pop)))
        for C in [1.0, 0.1]:
            P = logit(d, C)
            rows.append(dict(window=w, method=f"multinomial logit, all covariates incl. state and agency (C={C:g})",
                             **to_deaths(d, P, won, pop)))
        noc = [x for x in LOGIT_X if x != "circ"]
        P = logit(d, 1.0, noc)
        rows.append(dict(window=w, method="multinomial logit without circumstance (C=1)", **to_deaths(d, P, won, pop)))
        P = logit(d, 1.0, [x for x in noc if x != "Ori"])
        rows.append(dict(window=w, method="multinomial logit without circumstance or agency (C=1)",
                         **to_deaths(d, P, won, pop)))
        di = add_interactions(d)
        P = logit(di, 1.0, noc + INTER)
        rows.append(dict(window=w, method="multinomial logit without circumstance, victim-group interactions (C=1)",
                         **to_deaths(di, P, won, pop)))
        if w == "2022_2024":
            cv_rows.extend(cv_check(d))
        # solved cases only, imputing the ethnicity-missing ones within race (no unsolved imputation)
        ds = d[d.Solved.eq("Yes")].reset_index(drop=True)
        P = impute(ds, [["State"]], 20.0)
        rows.append(dict(window=w, method="solved only, ethnicity-missing split within race by state (no unsolved)",
                         **to_deaths(ds, P, won, pop)))
        # clearance by victim group
        for g in G:
            x = d[d.vic_eth.eq(g)]
            say(f"   [{w}] victims {g}: {len(x):,}; solved {x.Solved.eq('Yes').mean():.3f}; offender ethnicity known "
                f"{x.off_eth.isin(G).mean():.3f}")
    R = pd.DataFrame(rows)
    ref = R[R.method.str.startswith("victim lane")].set_index("window")
    R["dRR_H_NHW_vs_lane"] = R.RR_H_NHW / R.window.map(ref.RR_H_NHW) - 1
    R["d_share_H_vs_lane"] = R.share_H / R.window.map(ref.share_H) - 1
    R.to_csv(OUT / "shr_imputation_specs.csv", index=False, float_format="%.6f", lineterminator="\n")
    say(R[["window", "method", "p_H_given_vH", "p_H_given_vNHW", "share_H", "hispanic_offender_killings", "RR_H_NHW",
           "RR_H_all", "dRR_H_NHW_vs_lane"]].to_string(index=False, float_format=lambda x: f"{x:.4f}" if abs(x) < 10 else f"{x:,.0f}"))
    cv = pd.DataFrame(cv_rows)
    cv.to_csv(OUT / "shr_imputation_cv.csv", index=False, float_format="%.5f", lineterminator="\n")
    say("\n-- 5-fold cross-validation on ethnicity-known offenders, 2022-2024 (predicted vs actual Hispanic share) --")
    say(cv.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    (OUT / "shr_impute_log.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()
