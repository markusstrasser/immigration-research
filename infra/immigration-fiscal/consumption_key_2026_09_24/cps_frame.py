"""The account's CPS frame for the consumption key, rebuilt the way the receipts builder builds it.

full_account_receipts_2026_09_20/builder.py (derive_keys) keys general sales, selective excise,
customs and personal current transfers on positive SPM resources per person. This module rebuilds
that frame from the same CPS ASEC 2025 archive through the same helpers, checks that it reproduces
the stored key share (8.104%), and caches the arrays this lane needs in _cache/cps_arrays.npz.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
FISCAL = ROOT / "infra/immigration-fiscal"
RECEIPTS = FISCAL / "full_account_receipts_2026_09_20"
CACHE = HERE / "_cache" / "cps_arrays.npz"
# Fields the receipts builder does not read; appended to the base generator's usecols.
EXTRA = ["AGI", "SEMP_VAL", "FRSE_VAL", "PTOTVAL", "SPM_TOTVAL", "SPM_HAGE", "SPM_MEDXPNS",
         "SPM_WKXPNS", "SPM_CHILDSUPPD", "SPM_STTAX", "SPM_EITC", "SPM_ACTC", "PRCITSHP", "A_SEX"]


def load(path: Path, name: str):
    # Other lanes' modules are read, never written: no bytecode caches in their directories.
    sys.dont_write_bytecode = True
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def stored_key_share() -> float:
    keys = pd.read_csv(RECEIPTS / "derived/allocation_keys.csv")
    row = keys.query("allocation == 'personal' and allocation_key == 'consumption'")
    return float(row.target_key_share.iloc[0])


def build() -> dict:
    coverage = load(FISCAL / "national_coverage_2026_09_20/builder.py", "receipt_coverage")
    annual, absolute, _ = load(FISCAL / "education_origin_fiscal_2026_09_19/builder.py",
                               "receipt_evidence").configure(ROOT)
    for field in EXTRA:
        if field not in annual.ext.base.PERSON:
            annual.ext.base.PERSON.append(field)
    cps = FISCAL / "gen_ledger_extension_2026_09_16/_cache/asecpub25csv.zip"
    if coverage.sha(cps) != annual.ext.CPS_SHA:
        raise ValueError("[BLOCKED] unreviewed CPS source")
    state = annual.ext.build(argparse.Namespace(cps_zip=cps))
    d, w = state["d"], state["person_weights"]
    civilian = (d.PRPERTYP.eq(2) | d.A_AGE.lt(15)).to_numpy()
    groups = {g: state["group"][g] & civilian for g in absolute.TARGETS}
    target = np.logical_or.reduce(list(groups.values()))
    size = d.groupby("SPM_ID").SPM_ID.transform("size").to_numpy(float)
    arrays = dict(
        weights=w.astype(float), civilian=civilian, target=target,
        mexico_born=groups["mexico_born"], second_gen=groups["mexican_second_gen"],
        third_plus=groups["mexican_third_plus_selfid"], unit=np.asarray(state["index"]),
        n_units=np.array(state["n_units"]), size=size,
        spm_resources=d.SPM_RESOURCES.to_numpy(float), spm_totval=d.SPM_TOTVAL.to_numpy(float),
        snap=d.SPM_SNAPSUB.to_numpy(float), fica=d.SPM_FICA.to_numpy(float),
        fedtax=d.SPM_FEDTAX.to_numpy(float), sttax=d.SPM_STTAX.to_numpy(float),
        moop=d.SPM_MEDXPNS.to_numpy(float), work=d.SPM_WKXPNS.to_numpy(float),
        head=d.SPM_HEAD.eq(1).to_numpy(), head_age=d.SPM_HAGE.to_numpy(float),
        age=d.A_AGE.to_numpy(float), wage=d.WSAL_VAL.clip(lower=0).to_numpy(float),
        earnings=d.PEARNVAL.to_numpy(float), income=d.PTOTVAL.to_numpy(float),
        citizen=d.PRCITSHP.to_numpy(), year_entry=d.PEINUSYR.to_numpy(), state_fips=d.GESTFIPS.to_numpy(),
        hispanic=d.PEHSPNON.eq(1).to_numpy(), unit_weight=d.SPM_WEIGHT.to_numpy(float) / 100,
        ph_seq=d.PH_SEQ.to_numpy(), pppos=d.PPPOS.to_numpy(), prdthsp=d.PRDTHSP.to_numpy(),
        penatvty=d.PENATVTY.to_numpy(), pefntvty=d.PEFNTVTY.to_numpy(), pemntvty=d.PEMNTVTY.to_numpy(),
    )
    arrays["cps_sha256"] = np.array(annual.ext.CPS_SHA)
    return arrays


def frame(refresh: bool = False) -> dict:
    """The cached arrays, rebuilt when absent or when the CPS archive's hash changes."""
    if CACHE.exists() and not refresh:
        with np.load(CACHE, allow_pickle=False) as z:
            arrays = {k: z[k] for k in z.files}
        return arrays
    arrays = build()
    CACHE.parent.mkdir(parents=True, exist_ok=True)
    np.savez_compressed(CACHE, **arrays)
    return arrays


def key_shares(values: np.ndarray, a: dict) -> np.ndarray:
    """Group share of a nonnegative per-person key, for the full weight and 160 replicates."""
    civ, tgt, w = a["civilian"], a["target"], a["weights"]
    return (values[tgt] @ w[tgt]) / (values[civ] @ w[civ])


def sdr(shares: np.ndarray) -> float:
    return float(np.sqrt(4 / 160 * np.square(shares[1:] - shares[0]).sum()))


def reproduce(a: dict) -> dict:
    """Gate: the positive-resources-per-person key reproduces the stored 8.104% share."""
    consumption = a["spm_resources"].clip(min=0) / a["size"]
    shares = key_shares(consumption, a)
    stored = stored_key_share()
    ok = abs(shares[0] - stored) < 1e-12
    return dict(reproduced=float(shares[0]), stored=stored, se=sdr(shares), ok=bool(ok),
                target_key_total=float(consumption[a["target"]] @ a["weights"][a["target"], 0]),
                national_key_total=float(consumption[a["civilian"]] @ a["weights"][a["civilian"], 0]))


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--refresh", action="store_true")
    args = ap.parse_args()
    result = reproduce(frame(args.refresh))
    print(json.dumps(result, indent=1))
    if not result["ok"]:
        raise SystemExit("[FAIL] consumption key does not reproduce the stored share")
