"""GSS loader, generation coding and design-based variance for the norms lane.

Generation coding is copied verbatim from attitudes_gen_2026_09_16/generation.py
(the ladder-110 parental-birthplace repair: PARBORN 3/5/7 stay unknown).
Variance follows frontier_execution_2026_09_17/social/analyze_social.py:
stratified PSU linearization with n_h/(n_h-1), all full-sample design cells retained,
zero influence outside the analysis domain.
"""
import numpy as np, pandas as pd, pyreadstat, math

GSS = "raw/GSS_stata/gss7224_r3a.dta"

CON = ["confed","conlegis","conjudge","conarmy","conpress","consci","coneduc",
       "conbus","confinan","conclerg","conmedic","conlabor","contv"]
TOL_SPK = ["spkath","spkrac","spkcom","spkmil","spkhomo","spkmslm"]
TOL_COL = ["colath","colrac","colcom","colmil","colhomo","colmslm"]
TOL_LIB = ["libath","librac","libcom","libmil","libhomo","libmslm"]
LAW = ["obey","courts","cappun","gunlaw","polhitok","polabuse","polmurdr",
       "polescap","polattak","grass"]
ECON = ["helppoor","helpnot","eqwlth","natfare"]
IDENT = ["amcit","amcitizn","amancstr","amchrstn","amenglsh","amfeel","amgovt",
         "amshamed","ambornin","amcult","amimp","amlived","amproud","amownway",
         "ethnofit","ethadapt","ethspkok","immassim","immcult","immlimit"]
DESIGN = ["year","wtssps","wtssnrps","vpsu","vstrat","ballot"]
DEMOG = ["born","parborn","hispanic","ethnic","eth1","race","age","educ","degree",
         "polviews","coninc","sex","trust","mode"]
COLS = DESIGN + DEMOG + CON + TOL_SPK + TOL_COL + TOL_LIB + LAW + ECON + IDENT


def load(path=GSS, year_min=2000):
    d, meta = pyreadstat.read_dta(path, usecols=COLS, encoding="latin1")
    for c in d.columns:
        d[c] = pd.to_numeric(d[c], errors="coerce")
    d = d[d.year >= year_min].reset_index(drop=True).copy()
    d["w"] = d.wtssnrps.fillna(d.wtssps)
    return d


def generation(born, parborn):
    """GSS PARBORN: 1/2/4/6/8 establish a foreign-born parent; 3/5/7 do not."""
    g = pd.Series(np.nan, index=born.index)
    g.loc[born.eq(2)] = 1
    g.loc[born.eq(1) & parborn.isin([1, 2, 4, 6, 8])] = 2
    g.loc[born.eq(1) & parborn.eq(0)] = 3
    return g


def assign_groups(d):
    """Overlapping analysis groups. A row can belong to several columns at once
    (Mexican G2 is also Hispanic G2); each group is its own indicator, never a
    single categorical, so nothing is double counted inside one comparison."""
    g = generation(d.born, d.parborn)
    d = d.copy()
    d["gen"] = g
    hisp = d.hispanic.ge(2)
    mex = d.hispanic.eq(2)
    nhw = d.race.eq(1) & d.hispanic.eq(1)
    lab = {}
    for v, tag in [(1, "G1"), (2, "G2"), (3, "G3+")]:
        lab[f"Mex {tag}"] = (mex & g.eq(v)).to_numpy()
        lab[f"Hisp {tag}"] = (hisp & g.eq(v)).to_numpy()
    lab["Hisp all"] = hisp.to_numpy()
    lab["Mex all"] = mex.to_numpy()
    lab["NHWhite all"] = nhw.to_numpy()
    lab["NHWhite G3+"] = (nhw & g.eq(3)).to_numpy()
    lab["NHWhite G1-2"] = (nhw & g.isin([1, 2])).to_numpy()
    # white subgroups, third-plus generation (the reference population)
    base = nhw & g.eq(3)
    lab["White G3+ liberal"] = (base & d.polviews.isin([1, 2, 3])).to_numpy()
    lab["White G3+ moderate"] = (base & d.polviews.eq(4)).to_numpy()
    lab["White G3+ conservative"] = (base & d.polviews.isin([5, 6, 7])).to_numpy()
    lab["White G3+ no BA"] = (base & d.degree.isin([0, 1, 2])).to_numpy()
    lab["White G3+ BA+"] = (base & d.degree.isin([3, 4])).to_numpy()
    lab["White G3+ no HS"] = (base & d.degree.eq(0)).to_numpy()
    return d, lab


GROUP_ORDER = ["Mex G1","Mex G2","Mex G3+","Hisp G1","Hisp G2","Hisp G3+",
               "Hisp all","NHWhite all","NHWhite G3+","White G3+ liberal",
               "White G3+ moderate","White G3+ conservative","White G3+ no BA",
               "White G3+ BA+","White G3+ no HS"]


class Design:
    """Stratified with-replacement variance over the full 2000+ frame."""

    def __init__(self, d):
        ok = d[["vstrat", "vpsu"]].notna().all(axis=1) & d.w.notna() & d.w.gt(0)
        assert ok.all(), f"{(~ok).sum()} rows lack design fields or weight"
        self.strat = d.vstrat.to_numpy()
        self.psu = d.vpsu.to_numpy()
        npsu = d.groupby(["vstrat", "vpsu"]).size().groupby(level=0).size()
        assert npsu.ge(2).all(), "stratum with a single PSU"
        cross = d.groupby("vstrat").year.nunique()
        assert cross.max() == 1, "strata must be round-unique, as NORC documents"
        self.n_strata = len(npsu)
        self.n_psu = int(npsu.sum())
        self._key = pd.MultiIndex.from_arrays([self.strat, self.psu])

    def cov(self, influence):
        """influence: (n, k) array, zero outside the analysis domain.

        Vectorised equivalent of sum_h n_h/(n_h-1) * C_h' C_h where C_h centres
        the PSU totals within stratum h."""
        s = pd.DataFrame(np.asarray(influence, dtype=float)).groupby(
            [self.strat, self.psu]).sum()
        nh = s.groupby(level=0).size().reindex(s.index.get_level_values(0)).to_numpy().astype(float)
        centred = (s - s.groupby(level=0).transform("mean")).to_numpy()
        keep = nh > 1
        scaled = centred[keep] * np.sqrt(nh[keep] / (nh[keep] - 1.0))[:, None]
        return scaled.T @ scaled


def wmean(d, design, y, mask):
    """Weighted mean of y over mask, with design SE and the influence vector."""
    y = np.asarray(y, dtype=float)
    m = mask & np.isfinite(y)
    w = d.w.to_numpy()
    den = w[m].sum()
    if m.sum() < 2 or den <= 0:
        return None
    est = float(w[m] @ y[m] / den)
    infl = np.where(m, w * (np.nan_to_num(y) - est) / den, 0.0)
    se = math.sqrt(max(0.0, design.cov(infl[:, None])[0, 0]))
    return dict(n=int(m.sum()), mean=est, se=se), infl
