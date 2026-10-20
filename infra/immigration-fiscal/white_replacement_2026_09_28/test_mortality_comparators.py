"""Substantive checks of source refusal, mortality API scope and row-4 conservation."""
import json
import hashlib
from types import SimpleNamespace
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


def ratio_fixture(tmp_path, monkeypatch):
    monkeypatch.setattr(M, "FISCAL", tmp_path)
    source = tmp_path / "status.py"
    source.write_text("old status\n")
    lane = tmp_path / "lane"
    (lane / "derived").mkdir(parents=True)
    ratio = lane / "derived/accrual_ratios_mortality_oct16.csv"
    ratio.write_text("group,mortality,basis,scenario_name,end,payroll_basis,scenario,population,age_mix\n"
                     "white,general,symmetric,A3,,legacy,payable,100,A3\n"
                     "white,general,symmetric,A4,,legacy,payable,100,A4\n")
    manifest = {"dependencies": {"status.py": hashlib.sha256(source.read_bytes()).hexdigest()},
                "output_sha256": hashlib.sha256(ratio.read_bytes()).hexdigest()}
    (lane / "derived/accrual_ratios_mortality_oct16.dependencies.json").write_text(json.dumps(manifest))
    return lane, source


def test_stale_status_dependency_blocks_pension_selection(tmp_path, monkeypatch):
    lane, source = ratio_fixture(tmp_path, monkeypatch)
    source.write_text("newer status\n")
    with pytest.raises(SystemExit, match="pension status dependency hash"):
        M.select_ratio(lane, "white", "general", "symmetric", scenario_name="A3")


def test_pension_selection_preserves_scenario_age_weights(tmp_path, monkeypatch):
    lane, _ = ratio_fixture(tmp_path, monkeypatch)
    row = M.select_ratio(lane, "white", "general", "symmetric", scenario_name="A4")
    assert row["age_mix"] == "A4" and row["population"] == 100
    with pytest.raises(SystemExit, match="exactly one pension ratio"):
        M.select_ratio(lane, "white", "general", "symmetric", scenario_name="observed")


def test_ratio_denominator_repair_preserves_actuarial_numerators():
    amounts = dict(employee_oasdi=10., employer_oasdi=10., employee_hi=3., employer_hi=3.,
                   self_employment_oasdi_hi=4.)
    frame = SimpleNamespace(DUMP={"cash": {"low": {"lines": [dict(side="receipts", id=k, national_bn=v)
                                          for k, v in amounts.items()]}}}, SE_SHARE=.8)
    status = SimpleNamespace(receipt_amount=lambda sc, lid, national: national * 1.1)
    row = dict(oasdi_accrual_gross_bn=25., oasdi_accrual_net_bn=23., part_a_accrual_bn=7.)
    repaired = M.renormalized_row(row, frame, status, {"name": "age_tilt"}, "low")
    assert repaired["multiplier_oasdi_tax_bn"] == pytest.approx(23.2*1.1)
    assert repaired["oasdi_per_tax_dollar_net"] * repaired["multiplier_oasdi_tax_bn"] == pytest.approx(23.)
    assert repaired["part_a_per_hi_tax_dollar"] * repaired["multiplier_hi_tax_bn"] == pytest.approx(7.)


def test_memory_budget_failure_preserves_previous_valid_outputs(tmp_path, monkeypatch):
    derived = tmp_path / "derived"
    derived.mkdir()
    ratio = derived / "accrual_ratios_mortality_oct16.csv"
    manifest = ratio.with_suffix(".dependencies.json")
    ratio.write_bytes(b"previous valid ratio\n")
    manifest.write_bytes(b"previous valid dependency manifest\n")
    before = (ratio.read_bytes(), manifest.read_bytes())

    def blocked(_label):
        raise SystemExit("[BLOCKED] forced physical footprint budget failure")

    monkeypatch.setattr(M, "require_within_budget", blocked)
    with pytest.raises(SystemExit, match="physical footprint budget failure"):
        M.write_mortality_output(tmp_path, [{"group": "new ratio", "amount": 1.}], {"dependencies": {}})
    assert (ratio.read_bytes(), manifest.read_bytes()) == before


def test_mortality_output_admission_hashes_exact_written_csv(tmp_path, monkeypatch):
    (tmp_path / "derived").mkdir()
    monkeypatch.setattr(M, "require_within_budget", lambda _label: 123)
    assert M.write_mortality_output(tmp_path, [{"group": "white", "amount": 1.25}], {"dependencies": {}}) == 123
    ratio = tmp_path / "derived/accrual_ratios_mortality_oct16.csv"
    manifest = json.loads(ratio.with_suffix(".dependencies.json").read_text())
    assert ratio.read_bytes() == b"group,amount\nwhite,1.25\n"
    assert manifest["output_sha256"] == hashlib.sha256(ratio.read_bytes()).hexdigest()


def test_streamed_hash_preserves_source_digest(tmp_path):
    source = tmp_path / "source.bin"
    source.write_bytes(bytes(range(256)) * 5000)
    assert M.file_sha256(source) == hashlib.sha256(source.read_bytes()).hexdigest()


def test_option_snapshot_rejects_valid_newer_source_and_ratio_pair(tmp_path, monkeypatch):
    lane, source = ratio_fixture(tmp_path, monkeypatch)
    table = M.read_verified_ratio_table(lane)
    source.write_text("recomputed status\n")
    ratio = lane / "derived/accrual_ratios_mortality_oct16.csv"
    ratio.write_text(ratio.read_text().replace(",100,A4", ",120,A4"))
    manifest = {"dependencies": {"status.py": M.file_sha256(source)}, "output_sha256": M.file_sha256(ratio)}
    ratio.with_suffix(".dependencies.json").write_text(json.dumps(manifest))
    # The replacement is a valid current producer result, but cannot authorize
    # publication of the option-set prices computed from the old snapshot.
    M.verify_ratio_dependencies(lane)
    with pytest.raises(SystemExit, match="option-set snapshot remains current"):
        M.require_ratio_snapshot_fresh(table)
    assert M.select_verified_ratio(table, "white", "general", "symmetric", scenario_name="A4")["population"] == 100
    assert M.select_ratio(lane, "white", "general", "symmetric", scenario_name="A4")["population"] == 120


def test_option_snapshot_rejects_in_flight_status_change(tmp_path, monkeypatch):
    lane, source = ratio_fixture(tmp_path, monkeypatch)
    table = M.read_verified_ratio_table(lane)
    source.write_text("changed while calculating options\n")
    with pytest.raises(SystemExit, match="pension status dependency hash"):
        M.require_ratio_snapshot_fresh(table)
