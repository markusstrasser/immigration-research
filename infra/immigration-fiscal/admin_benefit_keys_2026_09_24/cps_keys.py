"""CPS ASEC 2025 benefit keys by Hispanic origin: positive control, then national and state shares.

Rebuilds the account's person-level keys exactly as `full_account_spending_2026_09_20/builder.py`
does (same fields, full-sample weight pwwgt0, canonical union, SPM equal-member allocation, MEPS
2024 age x birthplace transport) and gates every target share against that lane's
`derived/incidence_keys.csv` (relative 1e-9). The SNAP key is the brief's positive control.

Then, for each key and for recipient definitions that match the administrative tables, reports
the Hispanic share (PEHSPNON = 1), the union's share, the union's share of Hispanic key dollars,
the Mexican (PRDTHSP = 1) share of Hispanic key dollars and the union's non-Hispanic share,
nationally and by state (GESTFIPS), with successive-difference replicate SEs
(4/160 * sum over 160 replicates of (theta_r - theta_0)^2), as the other CPS lanes do.

Writes derived/cps_keys_national.csv, derived/cps_keys_state.csv and derived/cps_keys_gate.json,
and the replicate state sums that compare.py needs for SEs to _cache/cps_state_replicates.npz.
Run from the repo root:
  OPENBLAS_NUM_THREADS=1 uv run --no-project --with pandas --with numpy python3 \
      infra/immigration-fiscal/admin_benefit_keys_2026_09_24/cps_keys.py
"""
from __future__ import annotations

import hashlib
import json
import sys
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
FISCAL = HERE.parent
ROOT = FISCAL.parents[1]
ZIP = FISCAL / "gen_ledger_extension_2026_09_16/_cache/asecpub25csv.zip"
CPS_SHA = "318845a2b5e0034eb2973898de1738f4df0025727de38499e7669cb9c0deef0b"
KEYS = FISCAL / "full_account_spending_2026_09_20/derived/incidence_keys.csv"
MEPS = ROOT / "sources/immigration-fiscal/data/external/stage3/ahrq/meps_2024/h256dat.zip"
US = [57, 60, 66, 69, 73, 78]
REPS = [f"pwwgt{i}" for i in range(161)]
PCOLS = ["PH_SEQ", "PPPOS", "A_AGE", "A_SEX", "PRPERTYP", "PRCITSHP", "PENATVTY", "PEFNTVTY",
         "PEMNTVTY", "PRDTHSP", "PEHSPNON", "PERRP", "SPM_ID", "SPM_HEAD", "SPM_HHISP", "SS_VAL",
         "SSI_VAL", "PAW_VAL", "PAW_TYP", "UC_VAL", "VET_VAL", "WC_VAL", "WSAL_VAL", "EIT_CRED",
         "ACTC_CRD", "SPM_SNAPSUB", "SPM_ENGVAL", "SPM_WICVAL", "SPM_CAPHOUSESUB", "SPM_RESOURCES",
         "WICYN", "PUB", "PRIV", "MIL", "CHAMPVA", "MCAID"]
HCOLS = ["H_SEQ", "GESTFIPS", "HFOODSP", "HFDVAL", "HFOODNO", "HPUBLIC", "HLORENT", "HRWICYN",
         "HRNUMWIC"]
STATE = {1: "AL", 2: "AK", 4: "AZ", 5: "AR", 6: "CA", 8: "CO", 9: "CT", 10: "DE", 11: "DC", 12: "FL",
         13: "GA", 15: "HI", 16: "ID", 17: "IL", 18: "IN", 19: "IA", 20: "KS", 21: "KY", 22: "LA",
         23: "ME", 24: "MD", 25: "MA", 26: "MI", 27: "MN", 28: "MS", 29: "MO", 30: "MT", 31: "NE",
         32: "NV", 33: "NH", 34: "NJ", 35: "NM", 36: "NY", 37: "NC", 38: "ND", 39: "OH", 40: "OK",
         41: "OR", 42: "PA", 44: "RI", 45: "SC", 46: "SD", 47: "TN", 48: "TX", 49: "UT", 50: "VT",
         51: "VA", 53: "WA", 54: "WV", 55: "WI", 56: "WY"}


def sha(path: Path) -> str:
    with path.open("rb") as f:
        return hashlib.file_digest(f, "sha256").hexdigest()


def load() -> pd.DataFrame:
    if sha(ZIP) != CPS_SHA:
        raise SystemExit("[BLOCKED] CPS ASEC 2025 archive changed")
    with zipfile.ZipFile(ZIP) as z:
        d = pd.read_csv(z.open("pppub25.csv"), usecols=PCOLS)
        h = pd.read_csv(z.open("hhpub25.csv"), usecols=HCOLS).rename(columns={"H_SEQ": "PH_SEQ"})
        w = pd.read_csv(z.open("asec_csv_repwgt_2025.csv"), usecols=["h_seq", "PPPOS", *REPS])
    w = w.rename(columns={"h_seq": "PH_SEQ"})
    d = d.merge(w, on=["PH_SEQ", "PPPOS"], validate="one_to_one", how="left")
    d = d.merge(h, on="PH_SEQ", validate="many_to_one", how="left")
    if d[REPS + ["GESTFIPS"]].isna().any().any():
        raise SystemExit("[BLOCKED] missing CPS weights or state")
    return d


def canonical(d: pd.DataFrame):
    civ = (d.PRPERTYP.eq(2) | d.A_AGE.lt(15)).to_numpy()
    native = d.PRCITSHP.isin([1, 2, 3])
    target = ((d.PRCITSHP.isin([4, 5]) & d.PENATVTY.eq(303))
              | (native & (d.PEFNTVTY.eq(303) | d.PEMNTVTY.eq(303)))
              | (native & d.PEFNTVTY.isin(US) & d.PEMNTVTY.isin(US) & d.PRDTHSP.eq(1)))
    return civ, (target.to_numpy() & civ)


def equal_unit_share(values, ids):
    f = pd.DataFrame({"unit": ids, "v": np.asarray(values, float)})
    return (f.groupby("unit").v.transform("sum") / f.groupby("unit").v.transform("size")).to_numpy()


def unit_field(d, counts, field):
    if not d.groupby("SPM_ID")[field].nunique().eq(1).all():
        raise SystemExit(f"[BLOCKED] nonconstant unit field {field}")
    return d[field].to_numpy(float) / counts


def medicaid_key(d):
    sys.path.insert(0, str(FISCAL / "build"))
    from meps_health_transport_2024 import read_meps, donor_model  # noqa: E402
    md, _ = read_meps(MEPS, MEPS.with_name("h256su.txt"))
    cells, codes, _ = donor_model(md, d, False)
    valid = md.PERWT24F.gt(0) & md.AGE24X.ge(0) & md.BORNUSA.isin([1, 2])
    sample = md.loc[valid]
    index = pd.MultiIndex.from_frame(cells[["age_band", "born"]])
    exposure = ~(d.PUB.eq(0) & d.PRIV.eq(0)).to_numpy()
    sums = sample.assign(wx=sample.TOTMCD24 * sample.PERWT24F).groupby(["age_band", "born"]).wx.sum()
    pop = sample.groupby(["age_band", "born"]).PERWT24F.sum()
    mean = (sums / pop).reindex(index)
    if mean.isna().any():
        raise SystemExit("[BLOCKED] unmatched MEPS payer cell")
    return mean.to_numpy()[codes] * exposure


def measures(d):
    """(programme, measure, allocation, vector, gate key or None, what it matches)."""
    counts = d.groupby("SPM_ID").SPM_ID.transform("size").to_numpy()
    snap = unit_field(d, counts, "SPM_SNAPSUB")
    wic = unit_field(d, counts, "SPM_WICVAL")
    housing = unit_field(d, counts, "SPM_CAPHOUSESUB")
    ref = d.PERRP.isin([40, 41]).to_numpy()
    head = d.SPM_HEAD.eq(1).to_numpy()
    unit_any = lambda v: (pd.Series(v).groupby(d.SPM_ID.to_numpy()).transform("sum") > 0).to_numpy()
    paw = d.PAW_VAL.to_numpy(float)
    uc = d.UC_VAL.to_numpy(float)
    ssi = d.SSI_VAL.to_numpy(float)
    tanf_type = d.PAW_TYP.isin([1, 3]).to_numpy()
    assisted = (d.HPUBLIC.eq(1) | d.HLORENT.eq(1)).to_numpy()
    wic_hh = d.HRWICYN.eq(1).to_numpy()
    age = d.A_AGE.to_numpy()
    out = [
        ("snap", "key", "both", snap, "snap", "account key: SPM unit SNAP split equally over members"),
        ("snap", "persons_in_units", "both", (snap > 0).astype(float), None,
         "persons in SPM units with SNAP (QC participants and household members)"),
        ("snap", "head_dollars", "both", np.where(head, d.SPM_SNAPSUB.to_numpy(float), 0.0), None,
         "SPM unit SNAP dollars at the SPM head (QC benefits by head's ethnicity)"),
        ("snap", "household_dollars", "both", np.where(ref, d.HFDVAL.to_numpy(float), 0.0), None,
         "household SNAP value at the reference person"),
        ("snap", "households", "both", (ref & d.HFOODSP.eq(1).to_numpy()).astype(float), None,
         "households reporting SNAP, by reference person (QC units by head; ACS households)"),
        ("wic", "key", "both", wic, "wic", "account key: SPM unit WIC value split equally over members"),
        ("wic", "women_children_in_wic_households", "both",
         (wic_hh & ((age < 5) | d.WICYN.eq(1).to_numpy())).astype(float), None,
         "children under 5 and women reporting WIC in households reporting WIC (PC participants)"),
        ("wic", "women_reporting", "both", d.WICYN.eq(1).to_numpy(float), None,
         "adult women reporting WIC (WICYN universe is adult women)"),
        ("wic", "participants_by_householder", "both",
         np.where(ref & wic_hh, d.HRNUMWIC.to_numpy(float), 0.0), None,
         "household count of WIC recipients (HRNUMWIC), by reference person"),
        ("housing", "key", "both", housing, "housing_support",
         "account key: SPM housing subsidy split equally over members"),
        ("housing", "head_dollars", "both", np.where(head, d.SPM_CAPHOUSESUB.to_numpy(float), 0.0), None,
         "SPM housing subsidy at the SPM head (PSH households by head's ethnicity)"),
        ("housing", "households_reporting", "both", (ref & assisted).astype(float), None,
         "households reporting public housing or reduced rent, by reference person"),
        ("housing", "subsidized_households", "both",
         (head & (d.SPM_CAPHOUSESUB.to_numpy() > 0)).astype(float), None,
         "SPM units with a housing subsidy value, by SPM head"),
        ("cash", "key", "personal", paw, "cash_assistance", "account key: PAW_VAL, personal"),
        ("cash", "key", "shared", equal_unit_share(paw, d.SPM_ID), "cash_assistance",
         "account key: PAW_VAL split over SPM unit"),
        ("cash", "adult_recipients", "both", (paw > 0).astype(float), None,
         "persons 15+ reporting cash assistance (TANF adult recipients)"),
        ("cash", "adult_recipients_tanf", "both", ((paw > 0) & tanf_type).astype(float), None,
         "persons reporting TANF-type cash assistance"),
        ("cash", "children_in_units", "both", (unit_any(paw) & (age < 18)).astype(float), None,
         "children in SPM units with cash assistance (TANF child recipients)"),
        ("cash", "persons_in_units", "both", unit_any(paw).astype(float), None,
         "persons in SPM units with cash assistance (TANF recipients)"),
        ("cash", "persons_in_tanf_units", "both", unit_any(np.where(tanf_type, paw, 0.0)).astype(float), None,
         "persons in SPM units with TANF-type cash assistance"),
        ("cash", "children_in_tanf_units", "both",
         (unit_any(np.where(tanf_type, paw, 0.0)) & (age < 18)).astype(float), None,
         "children in SPM units with TANF-type cash assistance"),
        ("cash", "tanf_key", "personal", np.where(tanf_type, paw, 0.0), None,
         "TANF-type PAW_VAL dollars, personal"),
        ("ui", "key", "personal", uc, "unemployment", "account key: UC_VAL, personal"),
        ("ui", "key", "shared", equal_unit_share(uc, d.SPM_ID), "unemployment",
         "account key: UC_VAL split over SPM unit"),
        ("ui", "recipients", "both", (uc > 0).astype(float), None, "persons reporting unemployment compensation"),
        ("ssi", "key", "personal", ssi, "ssi", "account key: SSI_VAL, personal"),
        ("ssi", "key", "shared", equal_unit_share(ssi, d.SPM_ID), "ssi", "account key: SSI_VAL split over SPM unit"),
        ("medicaid", "key", "both", medicaid_key(d), "medicaid",
         "account key: MEPS 2024 Medicaid payer means by age x US birth, transported"),
        ("medicaid", "covered", "both", d.MCAID.eq(1).to_numpy(float), "medicaid_covered",
         "persons reporting Medicaid, CHIP or other means-tested coverage in 2024"),
        ("population", "all", "both", np.ones(len(d)), "population", "all civilian persons"),
    ]
    return out


def rep_se(values):
    return float(np.sqrt(4 / 160 * np.square(values[1:] - values[0]).sum()))


def main():
    d = load()
    civ, target = canonical(d)
    W = d[REPS].to_numpy(float)
    if abs(W[target, 0].sum() - 40896574.15235156) > 0.01:
        raise SystemExit("[BLOCKED] canonical union population drift")
    hisp = d.PEHSPNON.eq(1).to_numpy()
    mex = d.PRDTHSP.eq(1).to_numpy() & hisp
    state = d.GESTFIPS.map(STATE).to_numpy()
    if pd.isna(state).any():
        raise SystemExit("[BLOCKED] unexpected GESTFIPS code")
    published = pd.read_csv(KEYS)
    gates, nat_rows, st_rows = [], [], []
    reps = {}                                  # replicate state sums for compare.py (ignored cache)
    geos = sorted(set(state))
    onehot = (state[:, None] == np.array(geos)[None, :]).astype(float)
    for programme, measure, allocation, v, gate_key, note in measures(d):
        v = np.asarray(v, float)
        if not np.isfinite(v).all() or (v < 0).any():
            raise SystemExit(f"[BLOCKED] invalid vector {programme}/{measure}")
        pos = civ & (v > 0)
        vw = v[pos, None] * W[pos]                       # records x 161
        parts = {"total": np.ones(pos.sum(), bool), "hisp": hisp[pos], "union": target[pos],
                 "union_hisp": (target & hisp)[pos], "mex_hisp": mex[pos],
                 "union_nonhisp": (target & ~hisp)[pos]}
        sums = {k: (vw * m[:, None]).sum(0) for k, m in parts.items()}
        if gate_key:
            for alloc in (["personal", "shared"] if allocation == "both" else [allocation]):
                row = published[(published.key == gate_key) & (published.allocation == alloc)]
                if len(row) != 1:
                    raise SystemExit(f"[BLOCKED] no published key {gate_key}/{alloc}")
                pub = float(row.target_share.iloc[0])
                mine = sums["union"][0] / sums["total"][0]
                ok = abs(mine / pub - 1) < 1e-9
                gates.append(dict(programme=programme, measure=measure, allocation=alloc, key=gate_key,
                                  published_target_share=pub, rebuilt_target_share=mine, ok=bool(ok)))
                if not ok:
                    raise SystemExit(f"[GATE FAIL] {gate_key}/{alloc}: {mine} vs {pub}")
        ratio = lambda a, b: a / np.where(b > 0, b, np.nan)
        base = dict(programme=programme, measure=measure, allocation=allocation, note=note)
        nat = dict(base, geography="US", total=sums["total"][0],
                   records=int(pos.sum()), hisp_records=int((pos & hisp).sum()),
                   union_records=int((pos & target).sum()))
        for k, num, den in [("hisp_share", "hisp", "total"), ("union_share", "union", "total"),
                            ("union_in_hisp", "union_hisp", "hisp"), ("mex_in_hisp", "mex_hisp", "hisp"),
                            ("union_nonhisp_share", "union_nonhisp", "total")]:
            r = ratio(sums[num], sums[den])
            nat[k], nat[k + "_se"] = float(r[0]), rep_se(r)
        nat_rows.append(nat)
        oh = onehot[pos]
        ssum = {k: oh.T @ (vw * m[:, None]) for k, m in parts.items()}   # states x 161
        for k, arr in ssum.items():
            reps[f"{programme}|{measure}|{allocation}|{k}"] = arr
        for j, g in enumerate(geos):
            row = dict(base, geography=g, total=ssum["total"][j, 0],
                       records=int(oh[:, j].sum()), hisp_records=int((oh[:, j] * parts["hisp"]).sum()),
                       union_records=int((oh[:, j] * parts["union"]).sum()))
            for k, num, den in [("hisp_share", "hisp", "total"), ("union_share", "union", "total"),
                                ("union_in_hisp", "union_hisp", "hisp"), ("mex_in_hisp", "mex_hisp", "hisp")]:
                r = ratio(ssum[num][j], ssum[den][j])
                row[k] = float(r[0]) if np.isfinite(r[0]) else np.nan
                row[k + "_se"] = rep_se(r) if np.isfinite(r).all() else np.nan
            st_rows.append(row)
    (HERE / "derived").mkdir(exist_ok=True)
    (HERE / "_cache").mkdir(exist_ok=True)
    np.savez_compressed(HERE / "_cache/cps_state_replicates.npz", states=np.array(geos), **reps)
    pd.DataFrame(nat_rows).to_csv(HERE / "derived/cps_keys_national.csv", index=False, lineterminator="\n")
    pd.DataFrame(st_rows).to_csv(HERE / "derived/cps_keys_state.csv", index=False, lineterminator="\n")
    (HERE / "derived/cps_keys_gate.json").write_text(json.dumps(dict(
        cps_sha256=CPS_SHA, union_population=float(W[target, 0].sum()), gates=gates), indent=1) + "\n")
    show = pd.DataFrame(nat_rows)[["programme", "measure", "allocation", "total", "records", "hisp_share",
                                   "hisp_share_se", "union_share", "union_in_hisp", "mex_in_hisp"]]
    pd.set_option("display.width", 200)
    print(show.round(4).to_string(index=False))
    print(f"[gate] {len(gates)} published target shares reproduced (relative 1e-9); SNAP "
          f"{[g['rebuilt_target_share'] for g in gates if g['key'] == 'snap'][0]:.9f}")


if __name__ == "__main__":
    main()
