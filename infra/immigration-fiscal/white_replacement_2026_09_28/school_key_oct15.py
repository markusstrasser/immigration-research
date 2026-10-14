"""Round 3 (C3 fix 4): every group's K-12 key on the case's school construction, for the rough engine (case oct15).

The case keys the school part of education_services on public K-12 pupils priced where they live
(school_enrollment_2026_09_20): October 2024 CPS public K-12 rates by age band, with 3-4 and 25+ pooled, transported onto
March 2025 CPS civilians and priced at the state's current spending per pupil (gen_ledger_extension_2026_09_16
state_parameters.csv). The rough engine keyed every group on persons aged 5-17, so the rough comparison dropped the case's
school pricing on the lineage's side (the case-to-rough bridge carried it) and never priced it for the comparators. Here
every record takes the rate of its own cell, fitted on the October records of the same cell: the Mexican-origin union (the
case's own definition), NH Black alone, third-plus NH white alone (A1), other NH white alone, and everyone else. A member's
child outside the group takes its own cell's rate. The national total is every civilian's exposure, so the cells' shares
add to 1.

Positive control: the case's own construction (Mexican-origin against everyone else) on the March frame reproduces the
school lane's transported pupils (national, Mexican-origin, the rest) and the case's school spending for the Mexican-origin
group and the nation, personal allocation, to 1e-6 relative. The gap (about 5e-8) is weight rounding: the rough frame
weighs records MARSUPWT / 100, the school lane the ASEC replicate file's full-sample column.

Run from the repo root (writes derived/school_key_oct15.json; run_oct15.sh runs it before the re-key):
  OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/white_replacement_2026_09_28/school_key_oct15.py
rekey_sept29.py (case oct15) reads the rates through exposure() and replaces R.K["k12"] before it sets the case frame.
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
import sys
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd

LANE = Path(__file__).resolve().parent
FISCAL = LANE.parent
SE = FISCAL / "school_enrollment_2026_09_20"
STATE = FISCAL / "gen_ledger_extension_2026_09_16/state_parameters.csv"
CPS = FISCAL / "gen_ledger_extension_2026_09_16/_cache/asecpub25csv.zip"
OUT = LANE / "derived/school_key_oct15.json"
US = [57, 60, 66, 69, 73, 78]
CELLS = ("mex", "blk", "w3", "owh", "rest")
POOLED = ("3_4", "25_plus")
PTDTRACE = (139, 140)     # October 2024 layout (cpsoct24.txt): RACE


def sha(path):
    with Path(path).open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def require(ok, why):
    if not ok:
        raise SystemExit(f"[BLOCKED] {why}")


def measurement():
    """The school lane's October reader, as a private module instance (its field table gains the race item)."""
    spec = importlib.util.spec_from_file_location("school_measurement_oct15", SE / "measurement.py")
    M = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(M)
    M.FIELDS = {**M.FIELDS, "PTDTRACE": PTDTRACE}
    return M


def partition(d, race):
    """Each record's cell, by its own characteristics: the case's Mexican-origin definition first."""
    native = d.PRCITSHP.isin([1, 2, 3])
    parents_us = d.PEFNTVTY.isin(US) & d.PEMNTVTY.isin(US)
    parent_mex = d.PEFNTVTY.eq(303) | d.PEMNTVTY.eq(303)
    mex = (d.PRCITSHP.isin([4, 5]) & d.PENATVTY.eq(303)) | (native & parent_mex) | (native & parents_us & d.PRDTHSP.eq(1))
    nhw = d.PEHSPNON.eq(2) & d[race].eq(1)
    blk = d.PEHSPNON.eq(2) & d[race].eq(2)
    w3 = native & parents_us & nhw
    return np.select([mex.to_numpy(), blk.to_numpy(), w3.to_numpy(), nhw.to_numpy()], list(CELLS[:4]), CELLS[4])


def codes(age, cell, bands):
    out = np.full(len(age), "out", object)
    for label, lo, hi in bands:
        a = (age >= lo) & (age <= hi)
        if label in POOLED:
            out[a] = label + ":all"
        else:
            for c in CELLS:
                out[a & (cell == c)] = f"{label}:{c}"
    return out


def fit(code, w, pupil):
    """Point rates by code, with the school lane's support gates (n and Kish n_eff at least 50)."""
    rates, rows = {}, []
    for c in sorted(set(code) - {"out"}):
        use = code == c
        den, num = float(w[use].sum()), float(w[use & pupil].sum())
        neff = den ** 2 / float(np.square(w[use]).sum())
        require(use.sum() >= 50 and neff >= 50 and den > 0, f"unsupported October cell {c}: n={int(use.sum())}, neff={neff:.1f}")
        rates[c] = num / den
        rows.append(dict(cell=c, n=int(use.sum()), n_public=int((use & pupil).sum()), kish_neff=neff, rate=num / den))
    rates["out"] = 0.0
    return rates, rows


def march():
    """March 2025 CPS person rows in file order (the rough engine's R.d order), their state and civilian weights."""
    with zipfile.ZipFile(CPS) as z:
        d = pd.read_csv(z.open("pppub25.csv"), usecols=["PH_SEQ", "MARSUPWT", "A_AGE", "PRPERTYP", "PRCITSHP", "PENATVTY",
                                                         "PEFNTVTY", "PEMNTVTY", "PRDTHSP", "PEHSPNON", "PRDTRACE"])
        h = pd.read_csv(z.open("hhpub25.csv"), usecols=["H_SEQ", "GESTFIPS"]).rename(columns={"H_SEQ": "PH_SEQ"})
    d = d.merge(h, on="PH_SEQ", how="left", validate="many_to_one")
    d["PRTAGE"] = d.A_AGE
    civ = (d.PRPERTYP.eq(2) | d.A_AGE.lt(15)).to_numpy()
    sp = pd.read_csv(STATE)
    cost = d.GESTFIPS.map(dict(zip(sp.fips, sp.per_pupil_current_spending))).to_numpy(float)
    require(bool(np.isfinite(cost[civ]).all()), "every civilian's state has a spending per pupil")
    return d, civ, d.MARSUPWT.to_numpy(float) / 100 * civ, cost


def main():
    M = measurement()
    od, ow, audit = M.load_october(SE / "_cache", SE / "sources.json")
    w0 = ow[:, 0]
    pupil = M.public_k12(od)
    ocell = partition(od, "PTDTRACE")
    require(bool(np.array_equal(ocell == "mex", M.origin_masks(od)["target"])), "October Mexican-origin cell is the case's")
    rates, rows = fit(codes(od.PRTAGE.to_numpy(), ocell, M.AGE_BANDS), w0, pupil)
    case_rates, _ = M.fit_rates(od, ow)
    d, civ, w, cost = march()
    mcell = partition(d, "PRDTRACE")
    require(bool(np.array_equal(mcell == "mex", M.origin_masks(d)["target"])), "March Mexican-origin cell is the case's")
    # Positive control: the case's construction on this frame reproduces the school lane and the account.
    case_p = np.array([case_rates[c][0] for c in M.cells(d)]) * civ
    target = M.origin_masks(d)["target"]
    tp = pd.read_csv(SE / "derived/transported_pupils.csv")
    tp = tp[tp.state.eq(0) & tp.age.eq("all_ages")].drop_duplicates().set_index("group").updated_pupils
    acc = pd.read_csv(SE / "derived/updated_account_components.csv")
    acc = acc[acc.allocation.eq("personal") & acc.component.eq("school")].set_index("group").spending_bn
    controls = {}
    for group, mask, pupils_want, bn_want in (
            ("mexican_observed_total", target, tp["mexican_observed_total"], acc["mexican_observed_total"]),
            ("other_residents", ~target, tp["other_residents"], acc["other_residents"]),
            ("national_civilian", np.ones(len(d), bool), tp["national_civilian"], acc["national_civilian"])):
        pupils = float(w[mask] @ case_p[mask])
        bn = float(w[mask] @ (case_p * cost)[mask]) / 1e9
        controls[group] = dict(pupils=pupils, pupils_school_lane=float(pupils_want), spending_bn=bn,
                               spending_bn_account=float(bn_want))
        require(abs(pupils / pupils_want - 1) < 1e-6 and abs(bn / bn_want - 1) < 1e-6,
                f"case construction reproduces the school lane for {group}: {pupils:.6f} / {bn:.9f}")
    exposure = np.array([rates[c] for c in codes(d.A_AGE.to_numpy(), mcell, M.AGE_BANDS)]) * cost * civ
    rough = d.A_AGE.between(5, 17).to_numpy(float) * civ
    national = float(w @ exposure)
    case_national = float(w @ (case_p * cost))
    shares = {}
    for name, mask in (("mex", target), ("blk", mcell == "blk"), ("w3", mcell == "w3"),
                       ("wall", np.isin(mcell, ["w3", "owh"]))):
        shares[name] = dict(rough_5_17=float(w[mask] @ rough[mask] / (w @ rough)),
                            case_construction=float(w[mask] @ (case_p * cost)[mask] / case_national),
                            own_cells=float(w[mask] @ exposure[mask] / national))
    result = dict(case="oct15", rule=__doc__.split("\n\n")[1].replace("\n", " "),
                  rates=rates, cells=rows, pooled=list(POOLED), national_exposure_usd=national,
                  case_construction_national_usd=case_national, controls=controls, shares=shares,
                  sources={str(p.relative_to(FISCAL.parent.parent)): sha(p) for p in
                           (STATE, CPS, SE / "measurement.py", SE / "sources.json", SE / "derived/transported_pupils.csv",
                            SE / "derived/updated_account_components.csv", SE / "_cache/cpsoct24.txt")},
                  october=audit)
    OUT.write_text(json.dumps(result, indent=1, sort_keys=True) + "\n")
    for name, s in shares.items():
        print(f"  {name}: rough {s['rough_5_17']:.6f} -> own cells {s['own_cells']:.6f} "
              f"({s['own_cells'] / s['rough_5_17'] - 1:+.4%}); case construction {s['case_construction']:.6f}", flush=True)
    print(f"[school key] national exposure ${national / 1e9:.3f}bn (case construction ${case_national / 1e9:.3f}bn)", flush=True)


def exposure(R):
    """The per-record school exposure on the rough frame's rows (R.d order): own cell's rate x state spending per pupil.

    Reads the rates main() wrote; checks the state prices it read and the rows' alignment with R.d."""
    stored = json.loads(OUT.read_text())
    require(stored["sources"][str(STATE.relative_to(FISCAL.parent.parent))] == sha(STATE), "state spending per pupil unchanged")
    M = measurement()
    d, civ, w, cost = march()
    require(len(d) == len(R.d) and bool(np.array_equal(d.PH_SEQ.to_numpy(), R.d.PH_SEQ.to_numpy()))
            and bool(np.array_equal(d.A_AGE.to_numpy(), R.d.A_AGE.to_numpy())), "school key rows align with R.d")
    require(bool(np.array_equal(civ, R.civ)), "school key civilians are R.civ")
    cell = partition(d, "PRDTRACE")
    require(bool(np.array_equal(cell == "mex", R.MASK["mex"])) and bool(np.array_equal(cell == "blk", R.MASK["blk"] & ~R.MASK["mex"]))
            and bool(np.array_equal(cell == "w3", R.MASK["w3"] & ~R.MASK["mex"])), "school key cells follow R.MASK")
    e = np.array([stored["rates"][c] for c in codes(d.A_AGE.to_numpy(), cell, M.AGE_BANDS)]) * cost * civ
    require(abs(float(w @ e) / stored["national_exposure_usd"] - 1) < 1e-12, "school exposure reproduces its stored national total")
    return e


if __name__ == "__main__":
    main()
