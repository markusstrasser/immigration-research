"""Audit row 2 (`dataset_integrity_2026_09_23/cps.md` row 1) at any on-books share.

The audit's `cps_status_keys.py` re-keys the account's CPS tax keys for the Latin-American-born
imputed unauthorized at on-books shares 0.44 / 0.60 / 0.75. Its main() writes into its own
directory, so this lane imports its constants and repeats its arithmetic, parameterised:

1. gate: uniform shares 0.44 / 0.60 / 0.75 must reproduce the audit's CSV and cps.md's table;
2. grid: uniform shares 0.30 to 0.90;
3. split: one share for the Mexico-born and another for other Latin-American-born, and a
   component split (wage keys, income-tax keys, ACTC);
4. the evidence-weighted 2024 shares (`evidence_shares`), with survey under-reporting variants;
5. inputs: the imputed unauthorized wage earners' mean wage against all wage earners, arrival
   cohorts, modelled tax units.

Writes derived/onbooks_gate.csv, onbooks_grid.csv, onbooks_split.csv, onbooks_inputs.json.
"""
from __future__ import annotations

import sys

sys.dont_write_bytecode = True  # importing sibling lanes must not write __pycache__ there

import json  # noqa: E402
import zipfile  # noqa: E402
from pathlib import Path  # noqa: E402

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

HERE = Path(__file__).resolve().parent
FISCAL = HERE.parent
sys.path.insert(0, str(FISCAL / "dataset_integrity_2026_09_23"))
import cps_status_keys as audit  # noqa: E402  constants and impute() only; main() is never called

OUT = HERE / "derived"
# cps.md row 1: the refundable change applies to the non-PTC part, 0.2302 x 0.99 x $108.8-128.8bn.
NONPTC_BN = [0.2302 * 0.99 * line for line in (108.8, 128.8)]
# cps.md's printed table, used as the gate: receipts shared/personal, non-PTC low/high, net range,
# whole-line net shared/personal.
PRINTED = {
    0.44: (-20.38, -19.20, -3.38, -4.01, 15.2, 17.0, 13.3, 12.1),
    0.60: (-14.51, -13.67, -3.19, -3.78, 9.9, 11.3, 7.8, 7.0),
    0.75: (-9.04, -8.52, -3.01, -3.57, 5.0, 6.0, 2.7, 2.2),
}
# Inputs of the 2024 share construction (RESULT.md "Computation"). Sources in RESULT.md's table.
H2010 = 3.1 / 7.0                        # SSA Note 151 pp.3-4: on-payroll unauthorized / all unauthorized workers
H2040 = (3.4 + 0.2 + 0.6) / (3.4 + 0.2 + 0.6 + 9.0)  # p.4: ESF 3.4M, fraudulent-ID <0.2M, underground 9.0M;
                                         # overstayers held at their 2010 0.6M [INFERENCE]
EROSION_2024 = (H2010 - H2040) * 14 / 30  # SSA's path, linear 2010->2040 [INFERENCE]
H_MMP_SETTLED = 0.25 * 58 / 38           # MMP Table 1: undocumented 24/(24+72); >8-year stays 58% vs 38% overall
H_POST2001 = 0.10 + 0.23                 # Note 148: covered + suspense, other immigrants arriving after 2001
SSA_ON_BOOKS_WAGE = 0.80                 # Note 151 p.4: on-payroll unauthorized earn 80% of the all-worker average
PROTECTED = {"mex": (0.08, 0.11, 0.15), "oth": (0.15, 0.25, 0.35)}  # work-authorized dollar share [INFERENCE]
S_AUTH = (0.80, 0.90, 0.92)              # on-books share of the work-authorized (LPS 92%; ITEP p.28 92%)
# Survey under-reporting of off-books pay (RESULT.md item 3): the share to apply to CPS dollars is
# sigma / (sigma + (1 - u)(1 - sigma)) when a fraction u of off-books pay is missing from the survey.
UNDERREPORT_U = (0.10, 0.25)
WAGE_KEYS = ["wage_oasdi", "wage", "self_payroll", "positive_fica_worker"]
ITIN_RETURNS_TY2022 = 3_791_421      # NTA 2024 ARC research report 3, Figure 5.3.2
ITIN_PRIMARY_TY2023 = 2.4e6          # same report: "over 2.4 million" with the ITIN holder as primary


def evidence_shares(wage_ratio: dict[str, float]) -> dict[str, tuple[float, float]]:
    """2024 dollar-weighted on-books shares (Mexico-born, other Latin-American-born).

    share = p * s_auth + (1 - p) * h * f, where p is the work-authorized ("protected") dollar share,
    h the head-count on-books share of the never-authorized and overstayers, and f the dollar factor:
    1 if on- and off-books workers earn alike, 0.80 / (their CPS mean wage / all-earner mean) if the
    on-books earn SSA's assumed 80% of the all-worker average.
    """
    f_hi = {g: SSA_ON_BOOKS_WAGE / r for g, r in wage_ratio.items()}
    h = {"low": {"mex": H_MMP_SETTLED, "oth": H_POST2001},
         "central": {"mex": H2010 - EROSION_2024 / 2, "oth": H2010 - EROSION_2024},
         "high": {"mex": H2010, "oth": H2010}}
    f = {"low": {g: 1.0 for g in f_hi}, "central": {g: (1 + v) / 2 for g, v in f_hi.items()}, "high": f_hi}
    out = {}
    for i, case in enumerate(("low", "central", "high")):
        out[case] = tuple(PROTECTED[g][i] * S_AUTH[i] + (1 - PROTECTED[g][i]) * min(1.0, h[case][g] * f[case][g])
                          for g in ("mex", "oth"))
    return out


def load():
    extra = ["FILESTAT", "TAX_ID", "DEP_STAT", "FEDTAX_AC", "CTC_CRD"]
    with zipfile.ZipFile(audit.ZIP) as z:
        d = pd.read_csv(z.open("pppub25.csv"), usecols=audit.PCOLS + extra)
        hh = pd.read_csv(z.open("hhpub25.csv"), usecols=["H_SEQ", "HPUBLIC", "HLORENT"])
    return d, audit.impute(d, hh)


def main() -> None:
    d, st = load()
    w = (d.MARSUPWT / 100).to_numpy()
    latin = d.PENATVTY.between(302, 399).to_numpy() & ~d.PENATVTY.eq(327).to_numpy()
    unauth = st["unauthorized"] & latin
    mex = d.PENATVTY.eq(303).to_numpy()
    civ = (d.PRPERTYP.eq(2) | d.A_AGE.lt(15)).to_numpy()
    native = d.PRCITSHP.isin([1, 2, 3]).to_numpy()
    g1 = d.PRCITSHP.isin([4, 5]).to_numpy() & mex
    g2 = native & (d.PEFNTVTY.eq(303) | d.PEMNTVTY.eq(303)).to_numpy()
    g3 = (native & d.PEFNTVTY.isin(audit.US).to_numpy() & d.PEMNTVTY.isin(audit.US).to_numpy()
          & d.PRDTHSP.eq(1).to_numpy())
    target = (g1 | g2 | g3) & civ
    raw = {
        "federal_liability": d.FEDTAX_BC.clip(lower=0).to_numpy(float),
        "state_liability": d.STATETAX_A.clip(lower=0).to_numpy(float),
        "wage_oasdi": d.WSAL_VAL.clip(upper=audit.OASDI_CAP).to_numpy(float),
        "wage": d.WSAL_VAL.to_numpy(float),
        "self_payroll": d.SE_VAL.clip(lower=0).to_numpy(float),
        "positive_fica_worker": d.FICA.gt(0).to_numpy(float),
    }
    cats = pd.read_csv(audit.CATS)
    cats = cats[cats.scenario_id.eq("cbo_collective")]
    tb = {(k, a): cats[cats.allocation.eq(a) & cats.category.isin(c)].target_bn.sum()
          for k, c in audit.KEY_CATEGORIES.items() for a in ("shared", "personal")}
    eitc, actc = d.EIT_CRED.to_numpy(float), d.ACTC_CRD.to_numpy(float)

    def share(v):
        return (w * v)[target].sum() / (w * v).sum()

    def rekey(s_key: dict[str, np.ndarray], s_actc: np.ndarray) -> dict:
        """s_key: per-person share for each receipt key; s_actc: per-person ACTC share."""
        row, rec = {}, {"shared": 0.0, "personal": 0.0}
        for key, v in raw.items():
            ratio = share(np.where(unauth, v * s_key[key], v)) / share(v)
            for a in rec:
                delta = tb[(key, a)] * (ratio - 1)
                row[f"{key}_{a}"] = delta
                rec[a] += delta
        ratio = share(np.where(unauth, actc * s_actc, eitc + actc)) / share(eitc + actc)
        spend = [bn * (ratio - 1) for bn in NONPTC_BN]
        nets = [-rec[a] + sp for a in rec for sp in spend]
        row.update(receipts_shared=rec["shared"], receipts_personal=rec["personal"],
                   refundable_nonptc_lo=spend[0], refundable_nonptc_hi=spend[1],
                   refundable_whole=audit.REFUNDABLE_TARGET_BN * (ratio - 1),
                   net_min=min(nets), net_max=max(nets))
        row["whole_line_net_shared"] = -rec["shared"] + row["refundable_whole"]
        row["whole_line_net_personal"] = -rec["personal"] + row["refundable_whole"]
        return row

    def uniform(s):
        v = np.full(len(d), s)
        return rekey({k: v for k in raw}, v)

    def by_origin(s_mex, s_oth):
        v = np.where(mex, s_mex, s_oth)
        return rekey({k: v for k in raw}, v)

    # 1. Gate against the audit's own CSV (per-key deltas) and cps.md's printed table.
    ref = pd.read_csv(FISCAL / "dataset_integrity_2026_09_23/derived/cps_status_keys.csv")
    gate = []
    for s, printed in PRINTED.items():
        r = uniform(s)
        sub = ref[ref.on_books.round(2).eq(s)]
        csv_err = max(abs(r[f"{k}_{a}"] - sub[(sub.key == k) & (sub.allocation == a)].delta_target_bn.iloc[0])
                      for k in raw for a in ("shared", "personal"))
        mine = (r["receipts_shared"], r["receipts_personal"], r["refundable_nonptc_lo"],
                r["refundable_nonptc_hi"], r["net_min"], r["net_max"],
                r["whole_line_net_shared"], r["whole_line_net_personal"])
        tol = (0.006,) * 4 + (0.051,) * 4
        ok = csv_err < 1e-9 and all(abs(m - p) <= t for m, p, t in zip(mine, printed, tol))
        gate.append(dict(on_books=s, max_abs_err_vs_audit_csv=csv_err, pass_=ok,
                         **{f"mine_{i}": round(m, 3) for i, m in enumerate(mine)},
                         **{f"printed_{i}": p for i, p in enumerate(printed)}))
        if not ok:
            raise SystemExit(f"[BLOCKED] gate fails at on-books {s}: mine {mine} vs printed {printed}")
    pd.DataFrame(gate).to_csv(OUT / "onbooks_gate.csv", index=False)
    print("gate PASS at 0.44 / 0.60 / 0.75")

    # 2. Grid of uniform shares.
    grid = pd.DataFrame([dict(on_books=round(s, 2), **uniform(s)) for s in np.arange(0.30, 0.901, 0.05)])
    grid.to_csv(OUT / "onbooks_grid.csv", index=False)

    # 3. Splits: by origin, and by component (wage keys / income-tax keys / ACTC).
    split = []
    for s_mex in (0.35, 0.40, 0.45, 0.50, 0.55, 0.60, 0.65):
        for s_oth in (0.40, 0.50, 0.60, 0.70, 0.80):
            split.append(dict(kind="origin", s_mex=s_mex, s_oth=s_oth, **by_origin(s_mex, s_oth)))
    for s_pay, s_inc, s_act in [(0.50, 0.60, 0.60), (0.50, 0.50, 0.70), (0.45, 0.60, 0.70),
                                (0.55, 0.60, 0.70), (0.50, 0.60, 0.80)]:
        s_key = {k: np.full(len(d), s_pay if k in WAGE_KEYS else s_inc) for k in raw}
        split.append(dict(kind="component", s_pay=s_pay, s_inc=s_inc, s_actc=s_act,
                          **rekey(s_key, np.full(len(d), s_act))))
    earner = d.WSAL_VAL.gt(0).to_numpy() & civ
    wsal = d.WSAL_VAL.to_numpy(float)

    def mean_wage(m):
        return (w * wsal)[m & earner].sum() / w[m & earner].sum()

    # SSA's comparator for "80 percent of the average level for all workers" is uncapped: 0.8 x the
    # 2010 average wage index ($41,674) = $33,339, the note's "about $34,000".
    all_mean_uncapped = mean_wage(np.ones(len(d), bool))
    wage_ratio = {"mex": mean_wage(unauth & mex) / all_mean_uncapped,
                  "oth": mean_wage(unauth & ~mex) / all_mean_uncapped}
    evidence = evidence_shares(wage_ratio)
    for name, (s_mex, s_oth) in evidence.items():
        split.append(dict(kind=f"evidence_{name}", s_mex=s_mex, s_oth=s_oth, **by_origin(s_mex, s_oth)))
        for u in UNDERREPORT_U:
            adj = [s / (s + (1 - u) * (1 - s)) for s in (s_mex, s_oth)]
            split.append(dict(kind=f"evidence_{name}_underreport_{u}", s_mex=adj[0], s_oth=adj[1],
                              **by_origin(*adj)))
    split = pd.DataFrame(split)
    # Uniform share giving the same mid-range effect as each origin-split evidence case.
    fine = np.round(np.arange(0.25, 0.951, 0.01), 2)
    mids = np.array([(r["net_min"] + r["net_max"]) / 2 for r in map(uniform, fine)])
    ev_mid = (split.net_min + split.net_max) / 2
    split["uniform_equivalent"] = np.interp(-ev_mid, -mids, fine)
    split.to_csv(OUT / "onbooks_split.csv", index=False)

    # 4. Inputs for the dollar-weighting and filing arguments.
    capped = d.WSAL_VAL.clip(upper=audit.OASDI_CAP).to_numpy(float)

    def mean_capped(m):
        m = m & earner
        return (w * capped)[m].sum() / w[m].sum()

    all_mean = mean_capped(np.ones(len(d), bool))
    yr = d.PEINUSYR.to_numpy()
    inputs = {
        "all_wage_earner_mean_capped_wage": all_mean,
        "all_wage_earner_mean_uncapped_wage": all_mean_uncapped,
        "unauthorized_all_origins_M": w[st["unauthorized"]].sum() / 1e6,
        "construction": {"H2010": H2010, "H2040": H2040, "EROSION_2024": EROSION_2024,
                         "H_MMP_SETTLED": H_MMP_SETTLED, "H_POST2001": H_POST2001,
                         "wage_ratio_uncapped": wage_ratio, "PROTECTED": PROTECTED, "S_AUTH": S_AUTH,
                         "shares": evidence},
    }
    for name, g in [("latin", unauth), ("mexico", unauth & mex), ("other_latin", unauth & ~mex)]:
        wd = (w * capped)[g & earner].sum()
        inputs[name] = {
            "persons_M": w[g].sum() / 1e6,
            "wage_earners_M": w[g & earner].sum() / 1e6,
            "capped_wages_bn": wd / 1e9,
            "mean_capped_wage_ratio_to_all_earners": mean_capped(g) / all_mean,
            "mean_wage_ratio_to_all_earners_uncapped": (w * wsal)[g & earner].sum() / w[g & earner].sum()
            / all_mean_uncapped,
            "wage_share_arrived_2022_2025": (w * capped)[g & earner & (yr == 28)].sum() / wd,
            "wage_share_arrived_2020_2025": (w * capped)[g & earner & (yr >= 27)].sum() / wd,
            "wage_share_arrived_after_2001": (w * capped)[g & earner & (yr >= 18)].sum() / wd,
            "modelled_fedtax_bc_bn": (w * d.FEDTAX_BC.clip(lower=0).to_numpy(float))[g].sum() / 1e9,
            "modelled_fedtax_ac_bn": (w * d.FEDTAX_AC.to_numpy(float))[g].sum() / 1e9,
            "modelled_actc_bn": (w * actc)[g].sum() / 1e9,
            "modelled_eitc_bn": (w * eitc)[g].sum() / 1e9,
        }
    # Modelled filing units with an imputed-unauthorized (all origins) head or spouse: distinct
    # (household, TAX_ID) among non-dependent adults the tax model files for (FILESTAT 1-5).
    ua = st["unauthorized"] & d.DEP_STAT.eq(0).to_numpy() & d.FILESTAT.between(1, 5).to_numpy()
    units = pd.DataFrame({"h": d.PH_SEQ[ua], "t": d.TAX_ID[ua], "w": w[ua]}).groupby(["h", "t"]).w.max()
    inputs["modelled_filing_units_with_unauthorized_head_or_spouse_M"] = units.sum() / 1e6
    inputs["itin_returns_ty2022_over_modelled_units"] = ITIN_RETURNS_TY2022 / units.sum()
    inputs["itin_primary_ty2023_over_modelled_units"] = ITIN_PRIMARY_TY2023 / units.sum()
    fs = pd.Series(w[st["unauthorized"] & (d.A_AGE.ge(18).to_numpy())]).groupby(
        d.FILESTAT[st["unauthorized"] & d.A_AGE.ge(18).to_numpy()].to_numpy()).sum() / 1e6
    inputs["unauthorized_adults_by_FILESTAT_M"] = {int(k): v for k, v in fs.items()}
    (OUT / "onbooks_inputs.json").write_text(json.dumps(inputs, indent=2, default=float))

    pd.set_option("display.width", 220)
    cols = ["on_books", "receipts_shared", "receipts_personal", "refundable_nonptc_lo",
            "refundable_nonptc_hi", "net_min", "net_max"]
    print(grid[cols].round(2).to_string(index=False))
    ev = split[split.kind.str.startswith("evidence") | split.kind.eq("origin")]
    print(ev[ev.kind.str.startswith("evidence")][["kind", "s_mex", "s_oth", "uniform_equivalent"] + cols[1:]].round(3).to_string(index=False))
    comp = split[split.kind.eq("component")]
    print(comp[["s_pay", "s_inc", "s_actc"] + cols[1:]].round(2).to_string(index=False))
    print(json.dumps(inputs, indent=1, default=float))


if __name__ == "__main__":
    main()
