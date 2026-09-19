"""Disconfirmation tests, specified before the results were read.

C1  does the victim x offender ethnicity matrix move when ethnicity-missing records are
    imputed inside race x state x year cells instead of dropped
C2  does the offender age distribution differ between Hispanic and non-Hispanic white
    offenders beyond what the two populations' age structures imply (age-standardised)
C3  does the treasury cost per homicide by offender ethnicity change sign under the
    expanded age-component account (read off treasury_cost_per_homicide.csv)
C4  sensitivity to the life-sentence arm  (same file)
"""
from __future__ import annotations

import zipfile
from pathlib import Path

import numpy as np
import pandas as pd
from cost_model import load_current_results

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
OUT = HERE / "derived"
RAW = HERE / "_cache/SHR76_25a.csv"
CPS = ROOT / "sources/immigration-fiscal/data/external/stage3/census/cps_asec_2025/asecpub25csv.zip"
ETH_ORDER = ["hispanic", "nh_white", "nh_black", "nh_other"]
BANDS = [15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65]
LABELS = ["15-19", "20-24", "25-29", "30-34", "35-39", "40-44", "45-49", "50-54",
          "55-59", "60-64", "65+"]


def ethnicity(race, ethnic):
    out = pd.Series("unknown", index=race.index, dtype=object)
    nonh = ethnic.eq("Not of Hispanic origin")
    out[nonh & race.eq("White")] = "nh_white"
    out[nonh & race.eq("Black")] = "nh_black"
    out[nonh & race.isin(["Asian", "American Indian or Alaskan Native",
                          "Native Hawaiian or Pacific Islander"])] = "nh_other"
    out[ethnic.eq("Hispanic origin")] = "hispanic"
    return out


def impute(df, side, rng):
    """Hot-deck the ethnicity of records with 'Unknown or not reported' ethnicity from the
    observed ethnicity distribution of same race x state x year records that do report."""
    race, eth = f"{side}Race", ("vic_eth" if side == "Vic" else "off_eth")
    known = df[df[eth].ne("unknown")]
    keys = [race, "State", "Year"]
    dist = (known.groupby(keys + [eth]).size().rename("n").reset_index())
    tot = dist.groupby(keys).n.transform("sum")
    dist["p"] = dist.n / tot
    fallback = (known.groupby([race, eth]).size().rename("n").reset_index())
    fallback["p"] = fallback.n / fallback.groupby(race).n.transform("sum")
    out = df[eth].copy()
    miss = df[eth].eq("unknown")
    piv = dist.pivot_table(index=keys, columns=eth, values="p", fill_value=0.0)
    fb = fallback.pivot_table(index=race, columns=eth, values="p", fill_value=0.0)
    sub = df.loc[miss, keys]
    probs = piv.reindex(pd.MultiIndex.from_frame(sub)).to_numpy()
    fbp = fb.reindex(sub[race]).to_numpy()
    bad = np.isnan(probs).any(axis=1) | (np.nan_to_num(probs).sum(axis=1) < 0.5)
    probs = np.where(bad[:, None], fbp, probs)
    probs = np.nan_to_num(probs)
    rowsum = probs.sum(axis=1, keepdims=True)
    probs = np.divide(probs, rowsum, out=np.zeros_like(probs), where=rowsum > 0)
    cats = list(piv.columns)
    draw = np.full(len(sub), "unknown", dtype=object)
    ok = probs.sum(axis=1) > 0
    cum = probs[ok].cumsum(axis=1)
    u = rng.random(ok.sum())[:, None]
    idx = (u > cum).sum(axis=1).clip(0, len(cats) - 1)
    draw[ok] = np.array(cats, dtype=object)[idx]
    out.loc[miss] = draw
    return out


def main() -> None:
    res = load_current_results(OUT)
    rng = np.random.default_rng(20260918)
    cols = ["Year", "State", "Solved", "Situation", "VicAge", "VicRace", "VicEthnic",
            "OffAge", "OffRace", "OffEthnic", "Circumstance", "Homicide"]
    df = pd.read_csv(RAW, usecols=cols, low_memory=False)
    df = df[df.Homicide.eq("Murder and non-negligent manslaughter")
            & df.Year.between(2019, 2023)
            & ~df.Circumstance.isin(["Felon killed by police",
                                     "Felon killed by private citizen"])].copy()
    df["vic_eth"] = ethnicity(df.VicRace, df.VicEthnic)
    df["off_eth"] = ethnicity(df.OffRace, df.OffEthnic)
    A = df[df.Situation.eq("Single victim/single offender") & df.Solved.eq("Yes")].copy()

    # ---- C1 ---------------------------------------------------------------
    drop = A[A.vic_eth.ne("unknown") & A.off_eth.ne("unknown")]
    m_drop = pd.crosstab(drop.off_eth, drop.vic_eth, normalize="index").reindex(
        index=ETH_ORDER, columns=ETH_ORDER, fill_value=0.0)
    B = A.copy()
    B["vic_eth"] = impute(B, "Vic", rng)
    B["off_eth"] = impute(B, "Off", rng)
    imp = B[B.vic_eth.ne("unknown") & B.off_eth.ne("unknown")]
    m_imp = pd.crosstab(imp.off_eth, imp.vic_eth, normalize="index").reindex(
        index=ETH_ORDER, columns=ETH_ORDER, fill_value=0.0)
    print("[C1] victim-ethnicity distribution by offender ethnicity, rows sum to 1")
    print("\n  drop ethnicity-missing records (n = %d)" % len(drop))
    print(m_drop.round(3).to_string())
    print("\n  hot-deck impute inside race x state x year (n = %d)" % len(imp))
    print(m_imp.round(3).to_string())
    delta = (m_imp - m_drop)
    print("\n  max absolute change in any cell: %.3f" % delta.abs().to_numpy().max())
    pd.concat({"drop": m_drop, "impute": m_imp, "delta": delta}).round(4).to_csv(
        OUT / "c1_matrix_drop_vs_impute.csv")
    # marginal offender composition
    comp = pd.DataFrame({
        "drop": drop.off_eth.value_counts(normalize=True),
        "impute": imp.off_eth.value_counts(normalize=True)}).reindex(ETH_ORDER)
    print("\n  offender-ethnicity composition of universe A")
    print(comp.round(3).to_string())
    comp.round(4).to_csv(OUT / "c1_offender_composition.csv")

    # ---- C2 ---------------------------------------------------------------
    off = imp[imp.OffAge.between(10, 98)].copy()
    off["band"] = pd.cut(off.OffAge, bins=BANDS + [200], labels=LABELS, right=False)
    counts = pd.crosstab(off.band, off.off_eth).reindex(columns=ETH_ORDER, fill_value=0)

    with zipfile.ZipFile(CPS) as z:
        c = pd.read_csv(z.open("pppub25.csv"),
                        usecols=["A_AGE", "MARSUPWT", "PEHSPNON", "PRDTRACE", "PRCITSHP",
                                 "PEFNTVTY", "PEMNTVTY"], low_memory=False)
    c["w"] = c.MARSUPWT / 100.0
    native = c.PRCITSHP.isin([1, 2, 3])
    us_area = [57, 60, 66, 69, 73, 78]
    parents_us = c.PEFNTVTY.isin(us_area) & c.PEMNTVTY.isin(us_area)
    pop_masks = {"hispanic": c.PEHSPNON.eq(1),
                 "nh_white": native & parents_us & c.PEHSPNON.eq(2) & c.PRDTRACE.eq(1),
                 "nh_black": c.PEHSPNON.eq(2) & c.PRDTRACE.eq(2)}
    c["band"] = pd.cut(c.A_AGE, bins=BANDS + [200], labels=LABELS, right=False)
    pop = pd.DataFrame({k: c[m].groupby("band", observed=False).w.sum()
                        for k, m in pop_masks.items()})
    rates = (counts[["hispanic", "nh_white", "nh_black"]] / 5.0) / pop * 1e5  # per year per 100k
    std_pop = pop.sum(axis=1) / pop.sum(axis=1).sum()
    std_dist = rates.mul(std_pop, axis=0)
    std_dist = std_dist / std_dist.sum()
    raw_dist = counts[["hispanic", "nh_white", "nh_black"]] / counts[
        ["hispanic", "nh_white", "nh_black"]].sum()
    print("\n[C2] offender age distribution, raw (share of that group's offenders)")
    print(raw_dist.round(3).to_string())
    print("\n     age-specific offending rate per 100,000 population per year")
    print(rates.round(1).to_string())
    print("\n     age distribution standardised to the pooled population age structure")
    print(std_dist.round(3).to_string())
    mean_raw = (raw_dist.mul([17, 22, 27, 32, 37, 42, 47, 52, 57, 62, 70], axis=0)).sum()
    mean_std = (std_dist.mul([17, 22, 27, 32, 37, 42, 47, 52, 57, 62, 70], axis=0)).sum()
    print("\n     mean offender age  raw: " + mean_raw.round(1).to_dict().__str__())
    print("     mean offender age  standardised: " + mean_std.round(1).to_dict().__str__())
    pd.concat({"raw": raw_dist, "rate_per_100k": rates, "standardised": std_dist}).round(4).to_csv(
        OUT / "c2_offender_age_standardised.csv")
    pop.round(0).to_csv(OUT / "c2_population_by_age.csv")

    # ---- C3 / C4 ----------------------------------------------------------
    piv = res[(res.rate == 0.0) & (res.foster_share == 0.0)].pivot_table(
        index=["off_eth", "life_share"], columns="account", values="total")
    print("\n[C3/C4] total treasury cost per cleared homicide, undiscounted, no foster arm")
    print(piv.round(0).to_string())
    piv.round(0).to_csv(OUT / "c3_c4_account_and_life_sensitivity.csv")
    vb = res[(res.rate == 0.0) & (res.foster_share == 0.0)
             & (res.life_share == res.life_share.unique()[1])].pivot_table(
        index="off_eth", columns="account", values="victim_balance")
    print("\n  victim channel alone (sign test)")
    print(vb.round(0).to_string())





# --------------------------------------------------------------------------- C1b
def joint_impute(A: pd.DataFrame, rng) -> pd.DataFrame:
    """Impute the (victim, offender) ethnicity PAIR jointly, conditioning on whichever
    side is observed.  Independent per-side draws mechanically destroy the within-incident
    correlation and therefore understate intra-group pairing; this arm does not."""
    B = A.copy()
    donors = B[B.vic_eth.ne("unknown") & B.off_eth.ne("unknown")]
    keys = ["VicRace", "OffRace", "State", "Year"]
    fine = donors.groupby(keys + ["vic_eth", "off_eth"]).size().rename("n")
    coarse = donors.groupby(["VicRace", "OffRace", "vic_eth", "off_eth"]).size().rename("n")
    glob = donors.groupby(["vic_eth", "off_eth"]).size().rename("n")

    def sample(sub_keys, table, mask_vic, mask_off, obs_vic, obs_off, n):
        try:
            t = table.loc[sub_keys]
        except KeyError:
            return None
        t = t.reset_index()
        if obs_vic is not None:
            t = t[t.vic_eth.eq(obs_vic)]
        if obs_off is not None:
            t = t[t.off_eth.eq(obs_off)]
        if t.n.sum() <= 0:
            return None
        p = (t.n / t.n.sum()).to_numpy()
        idx = rng.choice(len(t), size=n, p=p)
        return t.vic_eth.to_numpy()[idx], t.off_eth.to_numpy()[idx]

    miss = B[B.vic_eth.eq("unknown") | B.off_eth.eq("unknown")]
    for (vr, orc, st, yr, ve, oe), g in miss.groupby(
            ["VicRace", "OffRace", "State", "Year", "vic_eth", "off_eth"]):
        n = len(g)
        obs_v = ve if ve != "unknown" else None
        obs_o = oe if oe != "unknown" else None
        res = sample((vr, orc, st, yr), fine, None, None, obs_v, obs_o, n)
        if res is None:
            res = sample((vr, orc), coarse, None, None, obs_v, obs_o, n)
        if res is None:
            t = glob.reset_index()
            if obs_v:
                t = t[t.vic_eth.eq(obs_v)]
            if obs_o:
                t = t[t.off_eth.eq(obs_o)]
            if t.n.sum() <= 0:
                continue
            p = (t.n / t.n.sum()).to_numpy()
            idx = rng.choice(len(t), size=n, p=p)
            res = t.vic_eth.to_numpy()[idx], t.off_eth.to_numpy()[idx]
        B.loc[g.index, "vic_eth"] = res[0]
        B.loc[g.index, "off_eth"] = res[1]
    return B


def c1b() -> None:
    rng = np.random.default_rng(20260918)
    cols = ["Year", "State", "Solved", "Situation", "VicRace", "VicEthnic",
            "OffRace", "OffEthnic", "Circumstance", "Homicide"]
    df = pd.read_csv(RAW, usecols=cols, low_memory=False)
    df = df[df.Homicide.eq("Murder and non-negligent manslaughter")
            & df.Year.between(2019, 2023)
            & ~df.Circumstance.isin(["Felon killed by police",
                                     "Felon killed by private citizen"])].copy()
    df["vic_eth"] = ethnicity(df.VicRace, df.VicEthnic)
    df["off_eth"] = ethnicity(df.OffRace, df.OffEthnic)
    A = df[df.Situation.eq("Single victim/single offender") & df.Solved.eq("Yes")].copy()
    B = joint_impute(A, rng)
    B = B[B.vic_eth.ne("unknown") & B.off_eth.ne("unknown")]
    m = pd.crosstab(B.off_eth, B.vic_eth, normalize="index").reindex(
        index=ETH_ORDER, columns=ETH_ORDER, fill_value=0.0)
    print("\n[C1b] joint pair imputation, n = %d" % len(B))
    print(m.round(3).to_string())
    print("\n  offender composition")
    print(B.off_eth.value_counts(normalize=True).reindex(ETH_ORDER).round(3).to_string())
    m.round(4).to_csv(OUT / "c1b_matrix_joint_impute.csv")
    B.off_eth.value_counts(normalize=True).reindex(ETH_ORDER).round(4).to_csv(
        OUT / "c1b_offender_composition.csv")


if __name__ == "__main__":
    main()
    c1b()
