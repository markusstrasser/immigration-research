#!/usr/bin/env python3
"""California's imputed unauthorized residents and their Medi-Cal coverage, CPS ASEC 2025.

Status is the Borjas (2017) residual from `status_impute_2026_09_16/impute_status.py`, imported
unmodified. Rule sets:
  * `borjas_paper_rules` -- the paper's rules as that lane runs them;
  * `no_medicaid_rule`   -- rule (c) without Medicaid, as `parent_status_2026_09_23` runs it;
  * `state_aware_california`, `state_aware_verified_states` -- the paper rules, except that
    Medicaid is not read as a legal-status signal at the state-ages listed in STATUS_BLIND_2024,
    where programs covered income-eligible people regardless of immigration status during 2024.
    Implemented by passing `impute()` a copy of the frame with MCAID set to "No" there; the
    imported code is unchanged.

Coverage items as the status lane reads them: MCAID is "Medicaid, PCHIP or other means-tested
coverage last year" (calendar 2024). CAID (Medicaid only, last year), NOW_MCAID and NOW_CAID
(current, February-April 2025) are reported alongside. I_MCAID and I_MCARE flag hot-deck (1),
logical (2) and whole-unit (3) imputation [SOURCE: ASEC 2025 data dictionary, ddl25.txt
lines 5266-5314].

Run from the repository root:
    OPENBLAS_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1 uv run --no-project python3 \
        infra/immigration-fiscal/california_medical_status_2026_09_23/cps_ca_status.py
"""
from __future__ import annotations

import json
import sys
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(ROOT / "status_impute_2026_09_16"))
from impute_status import impute  # noqa: E402

CPS = ROOT / "gen_ledger_extension_2026_09_16/_cache/asecpub25csv.zip"
MEXICO = 303
CALIFORNIA = 6
US_BIRTH = [57, 60, 66, 69, 73, 78]          # US and territories, as dataset_integrity's union
REPS = [f"pwwgt{i}" for i in range(1, 161)]
IMPUTE_FIELDS = ["PH_SEQ", "A_LINENO", "A_SPOUSE", "PRCITSHP", "PENATVTY", "PEINUSYR", "SS_VAL",
                 "SSI_VAL", "MCAID", "MCARE", "MIL", "CHAMPVA", "VET_YN", "PEAFEVER", "PRPERTYP",
                 "A_CLSWKR", "PEIOOCC"]
PERSON = IMPUTE_FIELDS + ["PPPOS", "A_AGE", "MARSUPWT", "PEFNTVTY", "PEMNTVTY", "PRDTHSP",
                          "CAID", "NOW_MCAID", "NOW_CAID", "I_MCAID", "I_MCARE"]
AGE_BANDS = [("0-18", 0, 18), ("19-25", 19, 25), ("26-49", 26, 49), ("50-64", 50, 64),
             ("65+", 65, 200), ("50+", 50, 200), ("all", 0, 200)]
DHCS_AGE_GROUPS = [("0-18", 0, 18), ("19-44", 19, 44), ("45-64", 45, 64), ("65+", 65, 200),
                   ("all", 0, 200)]

# Published gate values (millions): status_impute_2026_09_16/status_counts.csv; the union target
# of dataset_integrity_2026_09_23/cps_status_keys.py; parent_status_2026_09_23 for 4.778M.
GATE = {
    ("borjas_paper_rules", "national_all_ages"): 14.896400744023408,
    ("borjas_paper_rules", "mexico_all_ages"): 4.56714438160163,
    ("borjas_paper_rules", "union_all_ages"): 4.56714438160163,
    ("borjas_paper_rules", "mexico_25_64"): 3.9170610819750302,
    ("no_medicaid_rule", "national_all_ages"): 18.581325048426173,
    ("no_medicaid_rule", "mexico_all_ages"): 5.709560908219401,
    ("no_medicaid_rule", "mexico_25_64"): 4.778136460024849,
}

# Coverage regardless of immigration status in force during calendar 2024 (the MCAID year):
# (state FIPS, program, first age, last age). Sources and dates in RESULT.md section 4: DHCS for
# California, the Oregon Health Authority, NY DOH 23 OHIP/INF-2, and KFF (1 May 2024 release for
# the March 2024 state lists; 19 May 2026 brief for DC, Illinois and Washington details).
# Left out: Colorado (adult coverage is Marketplace, children from 2025), Minnesota (2025),
# Washington adults (Apple Health Expansion from July 2024, capped at about 13,000 enrollees).
STATUS_BLIND_2024 = [
    (6, "CA Medi-Cal: children 2016, 19-25 2020, 50+ May 2022, 26-49 Jan 2024", 0, 200),
    (41, "OR Healthier Oregon: all ages from 1 July 2023", 0, 200),
    (11, "DC Healthcare Alliance 21+ and children's coverage", 0, 200),
    (17, "IL children", 0, 18),
    (17, "IL HBIA 42-64 (new enrollment paused 2023) and HBIS 65+", 42, 200),
    (36, "NY children", 0, 18),
    (36, "NY Medicaid for undocumented 65+ from 1 Jan 2024", 65, 200),
    (53, "WA children", 0, 18),
    (9, "CT children", 0, 18), (23, "ME children", 0, 18), (25, "MA children", 0, 18),
    (34, "NJ children", 0, 18), (44, "RI children", 0, 18), (49, "UT children", 0, 18),
    (50, "VT children", 0, 18),
]
BLIND_STATES = sorted({s for s, *_ in STATUS_BLIND_2024})


def load():
    with zipfile.ZipFile(CPS) as z:
        d = pd.read_csv(z.open("pppub25.csv"), usecols=PERSON)
        hh = pd.read_csv(z.open("hhpub25.csv"), usecols=["H_SEQ", "HPUBLIC", "HLORENT", "GESTFIPS"])
        r = pd.read_csv(z.open("asec_csv_repwgt_2025.csv"), usecols=["h_seq", "PPPOS", "pwwgt0"] + REPS)
    d = d.merge(r.rename(columns={"h_seq": "PH_SEQ"}), on=["PH_SEQ", "PPPOS"], how="left",
                validate="one_to_one")
    if d[REPS + ["pwwgt0"]].isna().any().any():
        raise ValueError("Incomplete person-replicate join")
    if (d.MARSUPWT / 100 - d.pwwgt0).abs().max() >= .01:
        raise ValueError("Full-weight merge validation failed")
    state = d.PH_SEQ.map(hh.set_index("H_SEQ").GESTFIPS)
    if state.isna().any():
        raise ValueError("Person record without a household state")
    d = pd.concat([d, state.astype(int).rename("state")], axis=1)
    return d, hh


class Est:
    """Weighted totals and ratios with the ASEC successive-difference replicate SE."""

    def __init__(self, W: np.ndarray):
        self.W = W

    def total(self, m: np.ndarray):
        t = self.W[m].sum(0)
        return float(t[0]), float(np.sqrt(4 / 160 * ((t[1:] - t[0]) ** 2).sum())), int(m.sum())

    def ratio(self, num: np.ndarray, den: np.ndarray):
        a, b = self.W[num & den].sum(0), self.W[den].sum(0)
        th = np.divide(a, b, out=np.full_like(b, np.nan), where=b > 0)
        return float(th[0]), float(np.sqrt(4 / 160 * ((th[1:] - th[0]) ** 2).sum()))


def blind_mask(d: pd.DataFrame, entries) -> np.ndarray:
    age, state = d.A_AGE.to_numpy(), d.state.to_numpy()
    m = np.zeros(len(d), bool)
    for fips, _, lo, hi in entries:
        m |= (state == fips) & (age >= lo) & (age <= hi)
    return m


def status_sets(d, hh):
    out = {"borjas_paper_rules": impute(d, hh),
           "no_medicaid_rule": impute(d, hh, use_medicaid_rule=False)}
    for name, entries in (("state_aware_california", [e for e in STATUS_BLIND_2024 if e[0] == CALIFORNIA]),
                          ("state_aware_verified_states", STATUS_BLIND_2024)):
        dm = d.copy()
        dm.loc[blind_mask(d, entries), "MCAID"] = 2
        out[name] = impute(dm, hh)
    return out


def main():
    d, hh = load()
    W = d[["pwwgt0"] + REPS].to_numpy(float)
    E = Est(W)
    age = d.A_AGE.to_numpy()
    state = d.state.to_numpy()
    ca = state == CALIFORNIA
    mex = d.PENATVTY.eq(MEXICO).to_numpy()
    native = d.PRCITSHP.isin([1, 2, 3]).to_numpy()
    noncitizen = d.PRCITSHP.eq(5).to_numpy()
    civ = (d.PRPERTYP.eq(2) | d.A_AGE.lt(15)).to_numpy()
    g1 = d.PRCITSHP.isin([4, 5]).to_numpy() & mex
    g2 = native & (d.PEFNTVTY.eq(MEXICO) | d.PEMNTVTY.eq(MEXICO)).to_numpy()
    g3 = (native & d.PEFNTVTY.isin(US_BIRTH).to_numpy() & d.PEMNTVTY.isin(US_BIRTH).to_numpy()
          & d.PRDTHSP.eq(1).to_numpy())
    union = (g1 | g2 | g3) & civ
    mcaid = d.MCAID.eq(1).to_numpy()

    S = status_sets(d, hh)
    out = HERE / "derived"
    out.mkdir(exist_ok=True)

    # ---- Gate ------------------------------------------------------------------------------
    gate_rows = []
    for (rules, what), pub in GATE.items():
        u = S[rules]["unauthorized"]
        m = {"national_all_ages": u, "mexico_all_ages": u & mex, "union_all_ages": u & union,
             "mexico_25_64": u & mex & (age >= 25) & (age <= 64)}[what]
        got = W[m, 0].sum() / 1e6
        ok = abs(got - pub) < 0.0005
        gate_rows.append({"rules": rules, "count": what, "published_millions": round(pub, 6),
                          "reproduced_millions": round(got, 6), "pass": ok})
        print(f"GATE {rules:20s} {what:18s} published {pub:.4f}M reproduced {got:.4f}M "
              f"{'PASS' if ok else 'FAIL'}", flush=True)
    pd.DataFrame(gate_rows).to_csv(out / "cps_gate.csv", index=False)
    if not all(r["pass"] for r in gate_rows):
        raise SystemExit("[BLOCKED] gate failed; no new numbers written")

    blind_state = np.isin(state, BLIND_STATES)
    regions = {"US": np.ones(len(d), bool), "California": ca, "rest_of_US": ~ca,
               "other_listed_states": blind_state & ~ca, "unlisted_states": ~blind_state}
    groups = {"all_foreign_born": np.ones(len(d), bool), "mexico_born": mex, "union": union}
    paper_u = S["borjas_paper_rules"]["unauthorized"]

    # ---- 1. Counts by rule set, region, group; and the count each rule set adds --------------
    rows = []
    for rules, s in S.items():
        u = s["unauthorized"]
        for reg, rm in regions.items():
            for grp, gm in groups.items():
                p, se, n = E.total(u & rm & gm)
                mv, mvse, mvn = E.total(u & ~paper_u & rm & gm)
                rows.append({"rules": rules, "region": reg, "group": grp,
                             "unauthorized_millions": round(p / 1e6, 4), "se": round(se / 1e6, 4),
                             "n": n, "added_vs_paper_millions": round(mv / 1e6, 4),
                             "added_se": round(mvse / 1e6, 4), "added_n": mvn})
    counts = pd.DataFrame(rows)
    counts.to_csv(out / "cps_counts_by_rules.csv", index=False)

    # ---- 2. Coverage among no_medicaid_rule unauthorized, by age band ------------------------
    nm = S["no_medicaid_rule"]["unauthorized"]
    items = {"MCAID": mcaid, "CAID": d.CAID.eq(1).to_numpy(), "NOW_MCAID": d.NOW_MCAID.eq(1).to_numpy(),
             "NOW_CAID": d.NOW_CAID.eq(1).to_numpy()}
    imp = d.I_MCAID.isin([1, 3]).to_numpy()
    logical = d.I_MCAID.eq(2).to_numpy()
    rows = []
    for reg, rm in regions.items():
        for grp, gm in (("all_foreign_born", groups["all_foreign_born"]), ("mexico_born", mex)):
            for band, lo, hi in AGE_BANDS:
                den = nm & rm & gm & (age >= lo) & (age <= hi)
                pop, pse, n = E.total(den)
                r = {"region": reg, "group": grp, "age": band, "unauthorized_no_medicaid_rule_millions":
                     round(pop / 1e6, 4), "se": round(pse / 1e6, 4), "n": n}
                for item, im in items.items():
                    c, cse, cn = E.total(den & im)
                    sh, shse = E.ratio(im, den)
                    r.update({f"{item}_millions": round(c / 1e6, 4), f"{item}_se": round(cse / 1e6, 4),
                              f"{item}_n": cn, f"{item}_share": round(sh, 4), f"{item}_share_se": round(shse, 4)})
                sh, shse = E.ratio(imp, den & mcaid)
                r["MCAID_yes_donor_imputed_share"] = round(sh, 4)
                r["MCAID_yes_donor_imputed_share_se"] = round(shse, 4)
                sh, _ = E.ratio(logical, den & mcaid)
                r["MCAID_yes_logical_imputed_share"] = round(sh, 4)
                rows.append(r)
    cov = pd.DataFrame(rows)
    cov.to_csv(out / "cps_coverage_by_age.csv", index=False)

    # ---- 3. By state: people the Medicaid clause moves into the legal column ----------------
    moved = nm & ~paper_u
    rows = []
    for st in sorted(np.unique(state)):
        sm = state == st
        a, ase, an = E.total(moved & sm)
        b, bse, bn = E.total(moved & sm & mex)
        c, _, cn = E.total(nm & sm)
        own, _, _ = E.total(moved & sm & mcaid)
        sh, shse = E.ratio(mcaid, nm & sm)
        rows.append({"state_fips": int(st), "listed_status_blind_2024": bool(st in BLIND_STATES),
                     "moved_millions": round(a / 1e6, 4), "moved_se": round(ase / 1e6, 4),
                     "moved_n": an, "moved_own_medicaid_millions": round(own / 1e6, 4),
                     "moved_mexico_born_millions": round(b / 1e6, 4), "moved_mexico_born_se": round(bse / 1e6, 4),
                     "moved_mexico_born_n": bn, "no_medicaid_unauthorized_millions": round(c / 1e6, 4),
                     "no_medicaid_unauthorized_n": cn, "MCAID_share_of_no_medicaid_unauthorized": round(sh, 4),
                     "MCAID_share_se": round(shse, 4)})
    by_state = pd.DataFrame(rows).sort_values("moved_millions", ascending=False)
    by_state.to_csv(out / "cps_moved_by_state.csv", index=False)

    # ---- 4. What moved people look like: own Medicaid report vs spouse chain -----------------
    rows = []
    for reg, rm in regions.items():
        for grp, gm in groups.items():
            base = moved & rm & gm
            t, tse, tn = E.total(base)
            o, ose, on = E.total(base & mcaid)
            h, hse, hn = E.total(base & mcaid & imp)
            rows.append({"region": reg, "group": grp, "moved_millions": round(t / 1e6, 4),
                         "se": round(tse / 1e6, 4), "n": tn,
                         "own_medicaid_millions": round(o / 1e6, 4), "own_se": round(ose / 1e6, 4),
                         "own_medicaid_donor_imputed_millions": round(h / 1e6, 4),
                         "own_medicaid_donor_imputed_se": round(hse / 1e6, 4),
                         "via_spouse_only_millions": round((t - o) / 1e6, 4)})
    pd.DataFrame(rows).to_csv(out / "cps_moved_decomposition.csv", index=False)

    # ---- 5. All Californians with Medicaid, for the survey-vs-DHCS calibration ---------------
    rows = []
    for band, lo, hi in DHCS_AGE_GROUPS + [b for b in AGE_BANDS if b[0] in ("19-25", "26-49", "50+")]:
        am = ca & (age >= lo) & (age <= hi)
        r = {"age": band}
        for item, im in items.items():
            c, cse, cn = E.total(am & im)
            r.update({f"{item}_millions": round(c / 1e6, 4), f"{item}_se": round(cse / 1e6, 4), f"{item}_n": cn})
        rows.append(r)
    pd.DataFrame(rows).to_csv(out / "cps_ca_all_medicaid.csv", index=False)

    # ---- 6. Why no senior stays unauthorized: Medicare reported alongside Medicaid -----------
    rows = []
    mcare = d.MCARE.eq(1).to_numpy()
    for reg, rm in (("California", ca), ("US", np.ones(len(d), bool))):
        den = rm & noncitizen & (age >= 65) & mcaid
        p, pse, n = E.total(den)
        sh, shse = E.ratio(mcare, den)
        rows.append({"region": reg, "noncitizens_65plus_with_MCAID_millions": round(p / 1e6, 4), "n": n,
                     "share_with_MCARE": round(sh, 4),
                     "share_MCARE_hotdeck": round(E.ratio(d.I_MCARE.isin([1, 3]).to_numpy(), den & mcare)[0], 4),
                     "share_MCARE_logical": round(E.ratio(d.I_MCARE.eq(2).to_numpy(), den & mcare)[0], 4)})
    pd.DataFrame(rows).to_csv(out / "cps_65plus_medicare_edit.csv", index=False)

    # ---- 7. California's Medicaid reports in excess of unlisted states' rates, by age band ----
    # Lower-end count of status-blind enrollees among the moved: sum over bands of California's
    # no_medicaid_rule unauthorized with MCAID minus what unlisted states' rate in the same band
    # would give. Computed replicate by replicate for the SDR SE.
    unl = regions["unlisted_states"]
    rows = []
    for grp, gm in (("all_foreign_born", np.ones(len(d), bool)), ("mexico_born", mex)):
        tot = np.zeros(W.shape[1])
        for band, lo, hi in AGE_BANDS[:4]:
            am = (age >= lo) & (age <= hi)
            n_ca = W[nm & ca & gm & am].sum(0)
            m_ca = W[nm & ca & gm & am & mcaid].sum(0)
            r_u = W[nm & unl & gm & am & mcaid].sum(0) / W[nm & unl & gm & am].sum(0)
            ex = m_ca - n_ca * r_u
            tot += ex
            rows.append({"group": grp, "age": band, "excess_millions": round(ex[0] / 1e6, 4),
                         "se": round(float(np.sqrt(4 / 160 * ((ex[1:] - ex[0]) ** 2).sum())) / 1e6, 4),
                         "california_rate": round(m_ca[0] / n_ca[0], 4), "unlisted_rate": round(r_u[0], 4)})
        rows.append({"group": grp, "age": "0-64", "excess_millions": round(tot[0] / 1e6, 4),
                     "se": round(float(np.sqrt(4 / 160 * ((tot[1:] - tot[0]) ** 2).sum())) / 1e6, 4),
                     "california_rate": None, "unlisted_rate": None})
    pd.DataFrame(rows).to_csv(out / "cps_ca_excess_over_unlisted.csv", index=False)

    pd.set_option("display.width", 250)
    pd.set_option("display.max_columns", 40)
    print(pd.DataFrame(rows).to_string(index=False))
    print(counts.to_string(index=False))
    print(cov[cov.region.isin(["California", "unlisted_states"])][
        ["region", "group", "age", "unauthorized_no_medicaid_rule_millions", "se", "n", "MCAID_millions",
         "MCAID_share", "MCAID_share_se", "NOW_MCAID_millions", "MCAID_yes_donor_imputed_share"]].to_string(index=False))
    print(pd.read_csv(out / "cps_ca_all_medicaid.csv").to_string(index=False))
    print(pd.read_csv(out / "cps_65plus_medicare_edit.csv").to_string(index=False))
    (out / "cps_run.json").write_text(json.dumps({
        "cps_zip": str(CPS.relative_to(ROOT.parent.parent)), "rule_sets": list(S),
        "status_blind_2024": [{"state_fips": s, "program": p, "age_from": lo, "age_to": hi}
                              for s, p, lo, hi in STATUS_BLIND_2024]}, indent=2))


if __name__ == "__main__":
    main()
