"""Arm 1: victim-conditional imputation of unknown offenders in NIBRS, Texas and Arizona 2022-2023.

    uv run --no-project --with pandas --with numpy --with scikit-learn python3 \
        infra/immigration-fiscal/crime_ratio_direction_2026_09_24/nibrs_impute.py

The NIBRS lane's central already allocates unknown offenders within state-year x offence x victim
ethnicity (its allocation "a"), so the clearance gap by victim ethnicity is absorbed there. This
script asks whether finer conditioning moves the ratios: agency, victim sex and age, weapon,
location, hour, gang flag, arrest and exceptional clearance, one at a time, as a nested chain with
empirical-Bayes shrinkage, and as a multinomial logit. It also tests the imputation against the
only direct evidence on unknown offenders, the arrestees booked in the same incidents, and
tabulates clearance by victim ethnicity in the same agencies.

Allocation at a partition level L (a set of covariates added to the lane's base cell):
    NHU  (non-Hispanic, race unknown)       split over NHW/NHB/NHO by the cell's non-Hispanic shares
    UW   (race White, ethnicity unknown)    Hispanic with P(H | White, cell), else NHW; likewise UB, UO
    UU, NOINFO                              over H/NHW/NHB/NHO by the cell's overall shares
Cell probabilities shrink toward the parent cell: p_L = (n_L phat_L + kappa p_parent)/(n_L + kappa).
With no covariates and kappa = 0 this is the lane's allocation "a" (gate: its central to 1e-9).

Rates use the lane's own denominators (agency populations x ACS composition), so every change
against the central comes from the numerator allocation alone.
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd

import nibrs_base as nb

nr = nb.nr
HERE = Path(__file__).resolve().parent
RESTAGE = HERE / "_cache" / "restage"
OUT = HERE / "derived"
OFFENCES = nr.OFFENCES
OFF = nr.OFF_CLASSES
HC = nr.H_CLASSES
GROUPS = nr.GROUPS
BASE = ["state", "year", "offence", "vclass"]
LOG: list[str] = []


def say(s: str = "") -> None:
    print(s, flush=True)
    LOG.append(s)


def gate(name: str, ok: bool, detail: str) -> None:
    say(f"[gate] {name}: {'PASS' if ok else 'FAIL'} - {detail}")
    if not ok:
        raise SystemExit(f"[BLOCKED] gate failed: {name}")


def load_rows() -> pd.DataFrame:
    return pd.concat([pd.read_pickle(RESTAGE / f"{st}-{yr}.pkl") for st, yr in nr.STATE_YEARS], ignore_index=True)


def check_restage(rows: pd.DataFrame, stages: dict) -> None:
    keys = ["agency_id", "offence", "vclass", "vtype", "age12", "arrest"]
    worst = 0.0
    for (st, yr), d in stages.items():
        lane = d["vcells"]["frac"].set_index(keys)[OFF].sort_index()
        mine = rows[(rows.state == st) & (rows.year == yr)].groupby(keys)[OFF].sum().reindex(lane.index).fillna(0)
        worst = max(worst, float((mine - lane).abs().to_numpy().max()))
        tot = float(rows[(rows.state == st) & (rows.year == yr)][OFF].to_numpy().sum())
        worst = max(worst, abs(tot - float(lane.to_numpy().sum())))
    gate("restaged victimisations sum to the NIBRS lane's staged cells (6 state-years, 13 classes)",
         worst < 1e-6, f"max |diff| {worst:.2e}")


def spec_rows(rows: pd.DataFrame, stages: dict, sp: dict) -> tuple[pd.DataFrame, pd.Series]:
    """Rows and population sums for a lane specification (same filters as nr.spec_cells)."""
    _, pops, kept = nr.spec_cells(stages, sp)
    r = rows[rows.state.isin(sp["states"]) & rows.year.isin(sp["years"]) & rows.vtype.isin(sp["vtypes"])
             & rows.age12.isin(sp["ages"]) & rows.offence.isin(OFFENCES)]
    r = r.merge(kept[["state", "year", "agency_id"]], on=["state", "year", "agency_id"])
    if sp.get("arrest_only"):
        r = r[r.arrest]
    return r.reset_index(drop=True), pops.sum()


# ---------------------------------------------------------------------------------------------
# Cell statistics and shrinkage
# ---------------------------------------------------------------------------------------------
STAT = ["H", "NHW", "NHB", "NHO", "NHU", "HW", "HB", "HO"]


def stats(df: pd.DataFrame, keys: list[str]) -> pd.DataFrame:
    s = pd.DataFrame({"H": df[HC].sum(axis=1), "NHW": df.NHW, "NHB": df.NHB, "NHO": df.NHO, "NHU": df.NHU,
                      "HW": df.HW, "HB": df.HB, "HO": df.HO})
    s[keys] = df[keys]
    return s.groupby(keys, observed=True)[STAT].sum()


def probs(s: pd.DataFrame, parent: pd.DataFrame | None, kappa: float) -> pd.DataFrame:
    """Probability columns for a level: nh shares (3), pairs q_W, q_B, q_O, overall (4)."""
    nh = s[["NHW", "NHB", "NHO"]].to_numpy()
    n_nh = nh.sum(axis=1, keepdims=True)
    out = pd.DataFrame(index=s.index)
    # non-Hispanic race shares
    if parent is None:
        nhs = np.where(n_nh > 0, nh / np.where(n_nh > 0, n_nh, 1), np.nan)
    else:
        pn = parent[["nh_NHW", "nh_NHB", "nh_NHO"]].to_numpy()
        nhs = (nh + kappa * pn) / (n_nh + kappa)
    out[["nh_NHW", "nh_NHB", "nh_NHO"]] = nhs
    # Hispanic vs non-Hispanic within recorded race
    for r, hk, nk in [("W", "HW", "NHW"), ("B", "HB", "NHB"), ("O", "HO", "NHO")]:
        a, b = s[hk].to_numpy(), s[nk].to_numpy()
        if parent is None:
            q = np.where(a + b > 0, a / np.where(a + b > 0, a + b, 1), np.nan)
        else:
            q = (a + kappa * parent[f"q_{r}"].to_numpy()) / (a + b + kappa)
        out[f"q_{r}"] = q
    # overall shares, NHU split by this level's non-Hispanic shares
    nhs_f = np.nan_to_num(nhs, nan=1 / 3)
    ov = np.column_stack([s.H.to_numpy(), nh + s.NHU.to_numpy()[:, None] * nhs_f])
    n_ov = ov.sum(axis=1, keepdims=True)
    if parent is None:
        ovp = np.where(n_ov > 0, ov / np.where(n_ov > 0, n_ov, 1), np.nan)
    else:
        po = parent[["ov_H", "ov_NHW", "ov_NHB", "ov_NHO"]].to_numpy()
        ovp = (ov + kappa * po) / (n_ov + kappa)
    out[["ov_H", "ov_NHW", "ov_NHB", "ov_NHO"]] = ovp
    out["n"] = n_ov[:, 0]
    return out


PCOLS = ["nh_NHW", "nh_NHB", "nh_NHO", "q_W", "q_B", "q_O", "ov_H", "ov_NHW", "ov_NHB", "ov_NHO"]


def _split(num: np.ndarray, fb: np.ndarray) -> np.ndarray:
    """Row shares of num, falling back to fb rows, then to equal shares (the lane's _split)."""
    s = num.sum(axis=1, keepdims=True)
    f = fb.sum(axis=1, keepdims=True)
    k = num.shape[1]
    return np.where(s > 0, num / np.where(s > 0, s, 1), np.where(f > 0, fb / np.where(f > 0, f, 1), 1.0 / k))


def base_probs(df: pd.DataFrame) -> pd.DataFrame:
    """The lane's allocation 'a' (nr.allocate, method 'a'), replicated on cell statistics:
    cell = state-year x offence x victim class, fallback = state-year x offence."""
    s = stats(df, BASE)
    f = stats(df, BASE[:3]).reindex(s.index.droplevel("vclass"))
    f.index = s.index
    nh3c, nh3f = s[["NHW", "NHB", "NHO"]].to_numpy(), f[["NHW", "NHB", "NHO"]].to_numpy()
    nhs = _split(nh3c, nh3f)
    ov = _split(np.column_stack([s.H.to_numpy(), nh3c + s.NHU.to_numpy()[:, None] * nhs]),
                np.column_stack([f.H.to_numpy(), nh3f + f.NHU.to_numpy()[:, None] * nhs]))
    out = pd.DataFrame(index=s.index)
    out[["nh_NHW", "nh_NHB", "nh_NHO"]] = nhs
    for r, hk, nk, j in [("W", "HW", "NHW", 1), ("B", "HB", "NHB", 2), ("O", "HO", "NHO", 3)]:
        pc = np.column_stack([s[hk].to_numpy(), s[nk].to_numpy()])
        pf = np.column_stack([f[hk].to_numpy(), f[nk].to_numpy()])
        none = (pc.sum(axis=1) + pf.sum(axis=1)) == 0
        q = _split(pc, pf)
        q[none] = _split(ov[:, [0, j]], ov[:, [0, j]])[none]
        out[f"q_{r}"] = q[:, 0]
    out[["ov_H", "ov_NHW", "ov_NHB", "ov_NHO"]] = ov
    out["n"] = (s.H + s[["NHW", "NHB", "NHO", "NHU"]].sum(axis=1)).to_numpy()
    return out


def chain_probs(df: pd.DataFrame, levels: list[list[str]], kappa: float) -> pd.DataFrame:
    """Per-row probabilities from a nested chain BASE -> BASE+levels[0] -> ... with shrinkage."""
    parent = base_probs(df)
    keys = list(BASE)
    rowp = df[BASE].merge(parent[PCOLS], left_on=BASE, right_index=True, how="left")
    for lev in levels:
        pkeys = list(keys)
        keys = keys + lev
        s = stats(df, keys)
        par = parent[PCOLS].reindex(s.index.droplevel(lev) if len(lev) else s.index)
        par.index = s.index
        cur = probs(s, par, kappa)
        parent = cur
        rowp = df[keys].merge(cur[PCOLS], left_on=keys, right_index=True, how="left")
        if rowp[PCOLS].isna().any().any():
            raise SystemExit("[BLOCKED] chain probabilities missing for some rows")
        del pkeys
    return rowp[PCOLS].reset_index(drop=True)


def allocate_rows(df: pd.DataFrame, p: pd.DataFrame) -> pd.DataFrame:
    """Allocate each row's offender mass to H/NHW/NHB/NHO with row probabilities p."""
    X = df[OFF].to_numpy()
    col = {k: i for i, k in enumerate(OFF)}
    v = lambda *ks: sum(X[:, col[k]] for k in ks)  # noqa: E731
    P = p[PCOLS].to_numpy()
    nhs = P[:, 0:3]
    qW, qB, qO = P[:, 3], P[:, 4], P[:, 5]
    ov = P[:, 6:10]
    out = np.zeros((len(df), 4))
    out[:, 0] = v(*HC)
    out[:, 1:] = np.column_stack([v("NHW"), v("NHB"), v("NHO")]) + v("NHU")[:, None] * nhs
    for u, q, j in [("UW", qW, 1), ("UB", qB, 2), ("UO", qO, 3)]:
        out[:, 0] += v(u) * q
        out[:, j] += v(u) * (1 - q)
    out += v("UU", "NOINFO")[:, None] * ov
    if not np.allclose(out.sum(axis=1), X.sum(axis=1)):
        raise SystemExit("[BLOCKED] row allocation does not conserve victimisations")
    return pd.DataFrame(out, columns=GROUPS, index=df.index)


def ratios(df: pd.DataFrame, alloc: pd.DataFrame, P: pd.Series, name: str, natpop: dict) -> pd.DataFrame:
    V = alloc.assign(offence=df.offence.to_numpy()).groupby("offence")[GROUPS].sum().reindex(OFFENCES)
    Pg = {g: P[f"c_{nr.POPCOL[g]}_12"] for g in GROUPS}
    Ptot = P["c_total_12"]
    nat = natpop["ncvs2024_12"]
    rows = []
    for o in OFFENCES:
        r = {g: V.loc[o, g] / Pg[g] for g in GROUPS}
        rall = V.loc[o].sum() / Ptot
        RR = {g: r[g] / r["NHW"] for g in GROUPS}
        rows.append(dict(method=name, offence=o, RR_H_NHW=RR["H"], RR_H_all=r["H"] / rall,
                         local_share_H=V.loc[o, "H"] / V.loc[o].sum(),
                         national_share_H=RR["H"] * nat["H"] / sum(RR[g] * nat[g] for g in GROUPS),
                         V_H=V.loc[o, "H"], V_NHW=V.loc[o, "NHW"], V_total=V.loc[o].sum()))
    return pd.DataFrame(rows)


# ---------------------------------------------------------------------------------------------
# Multinomial logit
# ---------------------------------------------------------------------------------------------
LOGIT_X = ["state", "year", "vclass", "vsex", "vageband", "weapon", "location", "hourband", "gang", "arrest", "exc",
           "agency_id"]


def logit_probs(df: pd.DataFrame, C: float = 1.0) -> pd.DataFrame:
    """Per offence, a multinomial logit on the known part of each row (fractional weights).
    Returns the same probability columns as the chain; q_r = P(H) / (P(H) + P(NH race r))."""
    from sklearn.linear_model import LogisticRegression
    from sklearn.preprocessing import OneHotEncoder

    base = base_probs(df)
    brow = df[BASE].merge(base[PCOLS], left_on=BASE, right_index=True, how="left").reset_index(drop=True)
    out = brow.copy()
    for o in OFFENCES:
        m = (df.offence == o).to_numpy()
        d = df[m].reset_index(drop=True)
        nhs = brow.loc[m, ["nh_NHW", "nh_NHB", "nh_NHO"]].to_numpy()
        y = np.column_stack([d[HC].sum(axis=1), d[["NHW", "NHB", "NHO"]].to_numpy() + d.NHU.to_numpy()[:, None] * nhs])
        Xc = d[LOGIT_X].astype(str)
        enc = OneHotEncoder(handle_unknown="ignore", min_frequency=5)
        Z = enc.fit_transform(Xc)
        rr, cc = np.nonzero(y > 1e-12)
        Zt = Z[rr]
        clf = LogisticRegression(C=C, max_iter=2000)
        clf.fit(Zt, cc, sample_weight=y[rr, cc])
        pr = np.zeros((len(d), 4))
        pr[:, clf.classes_] = clf.predict_proba(Z)
        idx = np.nonzero(m)[0]
        out.loc[idx, ["ov_H", "ov_NHW", "ov_NHB", "ov_NHO"]] = pr
        # P(H | recorded race r) needs the race mix of Hispanic offenders, pi(r | H), from the base
        # cell (state-year x offence x victim class); P(H) / (P(H) + P(NH race r)) would let every
        # Hispanic offender be Black or other.
        cs = stats(d, BASE)
        hsum = cs[["HW", "HB", "HO"]].sum(axis=1).replace(0, np.nan)
        for r, j, hk in [("W", 1, "HW"), ("B", 2, "HB"), ("O", 3, "HO")]:
            pi = (cs[hk] / hsum).fillna(0.0)
            pir = d[BASE].merge(pi.rename("pi"), left_on=BASE, right_index=True, how="left").pi.fillna(0.0).to_numpy()
            ph = pr[:, 0] * pir
            with np.errstate(invalid="ignore", divide="ignore"):
                q = np.where(ph + pr[:, j] > 0, ph / (ph + pr[:, j]), 0.0)
            out.loc[idx, f"q_{r}"] = q
    return out[PCOLS]


# ---------------------------------------------------------------------------------------------
# Validation against arrestees, and clearance by victim ethnicity
# ---------------------------------------------------------------------------------------------
ARR_H = [f"arr_{c}" for c in HC]
ARR_NH = [f"arr_{c}" for c in ["NHW", "NHB", "NHO", "NHU"]]
ARR_U = [f"arr_{c}" for c in ["UW", "UB", "UO", "UU"]]


def arrestee_validation(df: pd.DataFrame, pmap: dict[str, pd.DataFrame]) -> pd.DataFrame:
    """Incidents whose offenders carry no recorded ethnicity but which have arrestees with recorded
    ethnicity: compare the arrestees' Hispanic share with the share each method imputes to the
    same unknown offenders. Also the agreement of recorded offender ethnicity with arrestee
    ethnicity in single-offender, single-arrestee incidents."""
    rows = []
    a_h = df[ARR_H].sum(axis=1)
    a_nh = df[ARR_NH].sum(axis=1)
    a_k = a_h + a_nh
    known_eth = df[HC + ["NHW", "NHB", "NHO", "NHU"]].sum(axis=1)
    unk = df[["UW", "UB", "UO", "UU", "NOINFO"]].sum(axis=1)
    cases = {
        "offenders all ethnicity-unknown (recorded, no ethnicity), arrestee ethnicity known":
            (known_eth < 1e-9) & (df.NOINFO < 1e-9) & (a_k > 0),
        "  of which one offender record, one arrestee":
            (known_eth < 1e-9) & (df.NOINFO < 1e-9) & (a_k == 1) & (df[ARR_U].sum(axis=1) == 0) & (df.n_known == 1),
        "  of which recorded race White": (known_eth < 1e-9) & (df.NOINFO < 1e-9) & (a_k > 0) & (df.UW > 0.999),
        "no offender information, arrestee ethnicity known": (df.NOINFO > 0.999) & (a_k > 0),
    }
    for lab, msk in cases.items():
        for o in OFFENCES + ["all five"]:
            mm = msk & ((df.offence == o) if o != "all five" else True)
            if mm.sum() == 0:
                continue
            obs = float((unk[mm] * a_h[mm] / a_k[mm]).sum() / unk[mm].sum())
            rec = dict(case=lab, offence=o, victimisations=int(mm.sum()), arrestee_hispanic_share=obs)
            for name, p in pmap.items():
                al = allocate_rows(df[mm], p[mm])
                rec[f"imputed_H_{name}"] = float(al.H.sum() / al.sum(axis=1).sum())
            rows.append(rec)
    # agreement where the offender's ethnicity is recorded: single offender, single arrestee
    one = (df.n_known == 1) & (a_k == 1) & (df[ARR_U].sum(axis=1) == 0)
    for o in OFFENCES + ["all five"]:
        mm = one & ((df.offence == o) if o != "all five" else True)
        oh = df.loc[mm, HC].sum(axis=1) > 0.5
        onh = df.loc[mm, ["NHW", "NHB", "NHO", "NHU"]].sum(axis=1) > 0.5
        ah = a_h[mm] > 0
        rows.append(dict(case="single recorded offender and single arrestee: offender recorded Hispanic",
                         offence=o, victimisations=int(oh.sum()),
                         arrestee_hispanic_share=float(ah[oh].mean()) if oh.sum() else np.nan))
        rows.append(dict(case="single recorded offender and single arrestee: offender recorded non-Hispanic",
                         offence=o, victimisations=int(onh.sum()),
                         arrestee_hispanic_share=float(ah[onh].mean()) if onh.sum() else np.nan))
        nhw = df.loc[mm, "NHW"] > 0.5
        rows.append(dict(case="single recorded offender and single arrestee: offender recorded NH white",
                         offence=o, victimisations=int(nhw.sum()),
                         arrestee_hispanic_share=float(ah[nhw].mean()) if nhw.sum() else np.nan))
    return pd.DataFrame(rows)


def clearance_by_victim(df: pd.DataFrame) -> pd.DataFrame:
    rows = []
    known_eth = df[HC + ["NHW", "NHB", "NHO", "NHU"]].sum(axis=1)
    for (o, vc), g in df.groupby(["offence", "vclass"]):
        if vc not in ("vH", "vNHW", "vNHB"):
            continue
        ke = known_eth[g.index]
        rows.append(dict(offence=o, victim=vc, victimisations=len(g), offender_identified=float(1 - g.NOINFO.mean()),
                         offender_ethnicity_recorded=float(ke.mean()), arrest=float(g.arrest.mean()),
                         arrest_or_exceptional=float((g.arrest | g.exc).mean()),
                         firearm=float((g.weapon == "firearm").mean())))
    return pd.DataFrame(rows)


# ---------------------------------------------------------------------------------------------
def main() -> None:
    OUT.mkdir(exist_ok=True)
    stages, natpop = nb.load()
    rows = load_rows()
    check_restage(rows, stages)
    sp = nb.lane_specs()["central"]
    df, P = spec_rows(rows, stages, sp)
    say(f"central universe: {len(df):,} victimisations (TX+AZ 2022-2023, agencies recording >= 50%)")

    # Gate: base allocation reproduces the lane's central, and alloc=b / alloc=c bounds
    base = chain_probs(df, [], 0.0)
    res = [ratios(df, allocate_rows(df, base), P, "central (lane allocation a, replicated)", natpop)]
    lane = nb.reproduce(["central"]).set_index("offence")
    got = res[0].set_index("offence")
    gate("row-level replication of the lane's central (all five offences)",
         float((got.RR_H_NHW - lane.RR_H_NHW).abs().max()) < 1e-9 and float((got.RR_H_all - lane.RR_H_all).abs().max()) < 1e-9,
         f"murder {got.loc['Murder', 'RR_H_NHW']:.4f}, robbery {got.loc['Robbery', 'RR_H_NHW']:.4f}")

    methods: dict[str, pd.DataFrame] = {"central": base}
    single = {"agency": ["agency_id"], "victim sex and age": ["vsex", "vageband"], "weapon": ["weapon"],
              "location": ["location"], "hour": ["hourband"], "gang flag": ["gang"],
              "arrest and exceptional clearance": ["arrest", "exc"]}
    for kappa in [20.0]:
        for lab, lev in single.items():
            methods[f"+{lab} (kappa {kappa:g})"] = chain_probs(df, [lev], kappa)
    chain = [["agency_id"], ["weapon"], ["vsex", "vageband"], ["location"], ["hourband"]]
    for kappa in [5.0, 20.0, 100.0]:
        methods[f"chain agency>weapon>victim sex-age>location>hour (kappa {kappa:g})"] = chain_probs(df, chain, kappa)
    chain2 = [["weapon"], ["vsex", "vageband"], ["location"], ["hourband"], ["agency_id"]]
    methods["chain weapon>victim sex-age>location>hour>agency (kappa 20)"] = chain_probs(df, chain2, 20.0)
    chain3 = [["arrest", "exc"], ["agency_id"], ["weapon"], ["vsex", "vageband"]]
    methods["chain arrest-exc>agency>weapon>victim sex-age (kappa 20)"] = chain_probs(df, chain3, 20.0)
    say("fitting multinomial logits (one per offence) ...")
    methods["multinomial logit, all covariates incl. agency (C=1)"] = logit_probs(df, 1.0)
    methods["multinomial logit, all covariates incl. agency (C=0.1)"] = logit_probs(df, 0.1)

    for name, p in methods.items():
        if name == "central":
            continue
        res.append(ratios(df, allocate_rows(df, p), P, name, natpop))

    # Arrestee fill: where an incident's offenders carry no ethnicity and arrestees do, use the
    # arrestees' ethnicity split for that unknown mass; everything else as the central.
    a_h = df[ARR_H].sum(axis=1)
    a_k = a_h + df[ARR_NH].sum(axis=1)
    known_eth = df[HC + ["NHW", "NHB", "NHO", "NHU"]].sum(axis=1)
    fillable = (known_eth < 1e-9) & (a_k > 0)
    alloc_c = allocate_rows(df, base)
    alloc_f = alloc_c.copy()
    arr_nh_split = df[["arr_NHW", "arr_NHB", "arr_NHO"]].to_numpy().astype(float)
    arr_nhu = df["arr_NHU"].to_numpy().astype(float)
    nhs = base[["nh_NHW", "nh_NHB", "nh_NHO"]].to_numpy()
    arr_nh_split = arr_nh_split + arr_nhu[:, None] * nhs
    tot = df[OFF].sum(axis=1).to_numpy()
    fm = fillable.to_numpy()
    alloc_f.loc[fm, "H"] = tot[fm] * (a_h[fm] / a_k[fm]).to_numpy()
    for j, g in enumerate(["NHW", "NHB", "NHO"]):
        alloc_f.loc[fm, g] = tot[fm] * arr_nh_split[fm, j] / a_k[fm].to_numpy()
    res.append(ratios(df, alloc_f, P, "arrestee fill for ethnicity-unknown offenders, else central", natpop))
    say(f"arrestee fill applies to {fm.mean():.3%} of central victimisations "
        f"({df.loc[fm].groupby('offence').size().to_dict()})")

    R = pd.concat(res, ignore_index=True)
    cen = R[R.method.str.startswith("central")].set_index("offence")
    R["dRR_H_NHW_vs_central"] = R.RR_H_NHW / R.offence.map(cen.RR_H_NHW) - 1
    R["dRR_H_all_vs_central"] = R.RR_H_all / R.offence.map(cen.RR_H_all) - 1
    R.to_csv(OUT / "nibrs_imputation_specs.csv", index=False, float_format="%.6f", lineterminator="\n")
    say("\n-- Hispanic / NH-white by method (TX+AZ central universe) --")
    say(R.pivot_table(index="method", columns="offence", values="RR_H_NHW", sort=False)[OFFENCES]
        .to_string(float_format=lambda x: f"{x:.3f}"))
    say("\n-- Hispanic / all residents by method --")
    say(R.pivot_table(index="method", columns="offence", values="RR_H_all", sort=False)[OFFENCES]
        .to_string(float_format=lambda x: f"{x:.3f}"))

    # validation and clearance
    val = arrestee_validation(df, {"central": base,
                                   "chain_k20": methods["chain agency>weapon>victim sex-age>location>hour (kappa 20)"],
                                   "logit_C1": methods["multinomial logit, all covariates incl. agency (C=1)"]})
    val.to_csv(OUT / "nibrs_arrestee_validation.csv", index=False, float_format="%.4f", lineterminator="\n")
    say("\n-- Arrestee validation --")
    say(val.to_string(index=False, float_format=lambda x: f"{x:.3f}"))
    clr = clearance_by_victim(df)
    clr.to_csv(OUT / "nibrs_clearance_by_victim.csv", index=False, float_format="%.4f", lineterminator="\n")
    say("\n-- Clearance by victim ethnicity, same agencies --")
    say(clr.to_string(index=False, float_format=lambda x: f"{x:.3f}"))
    # covariate balance: how unknown-offender victimisations differ from known ones
    bal = []
    for o in ["Murder", "Robbery", "Aggravated assault"]:
        d = df[df.offence == o]
        unkm = d.NOINFO > 0.999
        for c in ["vclass", "weapon", "location", "hourband", "vsex"]:
            a = d[unkm][c].value_counts(normalize=True)
            b = d[~unkm][c].value_counts(normalize=True)
            for k in sorted(set(a.index) | set(b.index)):
                bal.append(dict(offence=o, covariate=c, level=k, share_offender_unknown=float(a.get(k, 0)),
                                share_offender_identified=float(b.get(k, 0))))
    pd.DataFrame(bal).to_csv(OUT / "nibrs_unknown_covariate_balance.csv", index=False, float_format="%.4f",
                             lineterminator="\n")
    (OUT / "nibrs_impute_log.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()
