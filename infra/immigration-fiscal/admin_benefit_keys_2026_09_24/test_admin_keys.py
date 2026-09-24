"""Positive control and gates for the administrative benefit keys lane.

The positive control rebuilds the account's SNAP target share from the CPS ASEC 2025 microdata
before anything is compared. Run from the repo root after the lane's scripts:
  OPENBLAS_NUM_THREADS=1 uv run --no-project --with pandas --with numpy --with openpyxl --with pytest \
      python3 -m pytest infra/immigration-fiscal/admin_benefit_keys_2026_09_24/ -q
"""
from __future__ import annotations

import importlib.util
import subprocess
import zipfile
from pathlib import Path

import pandas as pd

HERE = Path(__file__).resolve().parent
KEYS = HERE.parent / "full_account_spending_2026_09_20/derived/incidence_keys.csv"


def module(name):
    spec = importlib.util.spec_from_file_location(name, HERE / f"{name}.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_snap_target_share_rebuilt_from_cps_microdata():
    ck = module("cps_keys")
    d = ck.load()
    civ, target = ck.canonical(d)
    counts = d.groupby("SPM_ID").SPM_ID.transform("size").to_numpy()
    snap = ck.unit_field(d, counts, "SPM_SNAPSUB")
    w = d[ck.REPS[0]].to_numpy(float)
    pos = civ & (snap > 0)
    mine = (snap * w)[pos & target].sum() / (snap * w)[pos].sum()
    published = pd.read_csv(KEYS).query("key == 'snap'").target_share
    assert len(published) == 2
    assert all(abs(mine / p - 1) < 1e-9 for p in published)
    assert abs(mine - 0.148149840) < 1e-9


def test_snap_qc_weighted_totals_match_table_ii2():
    qc = module("snap_qc")
    with zipfile.ZipFile(qc.CACHE / "qcfy2024_csv.zip") as z:
        d = pd.read_csv(z.open("qc_pub_fy2024.csv"), usecols=["FYWGT", "FSUSIZE", "FSBEN"])
    assert abs((d.FYWGT * d.FSUSIZE).sum() - qc.TABLE_II2["individuals"]) <= 1
    assert abs((d.FYWGT * d.FSBEN).sum() / 1000 - qc.TABLE_II2["benefits_thousand"]) <= 1


def test_screen_catches_states_that_code_hispanic_participants_as_not_hispanic():
    # New Jersey, North Carolina and Pennsylvania record almost no Hispanic SNAP participants, even
    # among those living with an undocumented member; Texas and New Mexico lack ethnicity for most.
    # The screen must reject them and keep the three route-A states whose codes work.
    v = pd.read_csv(HERE / "derived/admin_validity.csv")
    snap = v[v.programme == "snap"].set_index("state")
    assert snap.loc[["NJ", "NC", "PA", "TX", "NM"], "invalid"].all()
    assert not snap.loc[["CA", "NV", "AZ"], "invalid"].any()
    qv = pd.read_csv(HERE / "derived/admin_snap_qc_validity.csv").set_index("geography")
    assert qv.loc["North Carolina", "with_undocumented_hisp_share_known"] < 0.2
    assert qv.loc["California", "with_undocumented_hisp_share_known"] > 0.8


def test_translation_reproduces_published_main_case_bands():
    r = subprocess.run(["node", str(HERE / "translate.js")], capture_output=True, text=True)
    assert r.returncode == 0, r.stderr
    assert r.stdout.count(" ok\n") == 3 and "all gates passed" in r.stdout
