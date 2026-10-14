"""Substantive checks of source refusal, mortality API scope and row-4 conservation."""
import json
import sys
from pathlib import Path

import numpy as np
import pytest

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
import accrual_white as W
import mortality_comparators as M


def test_mortality_keys_restore_on_exception():
    paths = M.verify_tables(M.LANE)
    paths.update(M.verify_tables(M.BLACK))
    old = W.P.L.TABLES
    general = W.P.L.qx_table("general", "male").copy()
    with pytest.raises(RuntimeError):
        with M.table_context(W.P, paths):
            assert np.array_equal(W.P.L.qx_table("general", "male"), general)
            black = W.P.L.qx_table("nh_black", "male")
            white = W.P.L.qx_table("nh_white", "male")
            assert black[40] > white[40]
            assert np.prod(1 - black[40:67]) < np.prod(1 - white[40:67])
            raise RuntimeError("intentional scope exit")
    assert W.P.L.TABLES is old
    assert np.array_equal(W.P.L.qx_table("general", "male"), general)
    assert W.P.L.survival.cache_info().currsize == 0


def test_changed_primary_file_fails_closed(tmp_path):
    (tmp_path / "inputs").mkdir()
    name = "lt2024_Table02.xlsx"
    pin = json.loads((M.LANE / "inputs/pins.json").read_text())["mortality_sources"][name]
    (tmp_path / "inputs" / name).write_bytes(b"altered primary bytes")
    (tmp_path / "inputs/pins.json").write_text(json.dumps({"mortality_sources": {name: pin}}))
    with pytest.raises(SystemExit, match="source hash"):
        M.verify_tables(tmp_path)


def test_wrong_sex_primary_with_valid_hash_fails_closed(tmp_path):
    (tmp_path / "inputs").mkdir()
    pins = json.loads((M.LANE / "inputs/pins.json").read_text())["mortality_sources"]
    female_name = "lt2024_Table03.xlsx"
    (tmp_path / "inputs" / female_name).write_bytes((M.LANE / "inputs/lt2024_Table02.xlsx").read_bytes())
    (tmp_path / "inputs/pins.json").write_text(json.dumps({"mortality_sources": {female_name: pins["lt2024_Table02.xlsx"]}}))
    with pytest.raises(SystemExit, match="source identity"):
        M.verify_tables(tmp_path)


def test_row4_weights_close_and_white_records_are_unchanged():
    p = W.P.frame()
    q = M.row4_frame(p, M.BLACK.parent / "gen_ledger_extension_2026_09_16/_cache/asecpub25csv.zip")
    assert np.array_equal(p.w[p[W.P.WHITE]], q.w[p[W.P.WHITE]])
    assert q.w[q.union].sum() < p.w[p.union].sum()
    assert np.array_equal(p.tax_oasdi, q.tax_oasdi)
    assert np.array_equal(p.tax_hi, q.tax_hi)


def test_symmetric_eligibility_and_payer_frame_preserves_principal_union():
    p = W.P.frame()
    zip_path = M.FISCAL / "gen_ledger_extension_2026_09_16/_cache/asecpub25csv.zip"
    p4 = M.row4_frame(p, zip_path)
    q = M.symmetric_frame(p4, W.P, zip_path)
    for key in ("unauth", "onbooks", "wage", "se", "oasdi_wage", "oasdi_se", "hi_se", "tax_oasdi", "tax_hi"):
        assert np.array_equal(q.loc[p.union, key], p4.loc[p.union, key]), key
    changed = p.civilian & ~p.union
    newly_eligible_rules = changed & q.unauth & ~p.unauth
    assert newly_eligible_rules.any()
    assert (q.onbooks[newly_eligible_rules] < 1).all()
    assert ((q.tax_oasdi[changed] - p.tax_oasdi[changed]).abs() > 0).any()
    assert np.array_equal(q.w, p4.w)


def test_symmetric_source_pin_mismatch_fails_before_frame_build(tmp_path):
    (tmp_path / "inputs").mkdir()
    name = "cps_imputation_keys_2026_09_23/common.py"
    (tmp_path / "inputs/pins.json").write_text(json.dumps({"symmetric_sources": {
        name: {"file": name, "sha256": "invalid source hash"}}}))
    with pytest.raises(SystemExit, match="symmetric source hash"):
        M.symmetric_frame(None, W.P, None, lane=tmp_path)
