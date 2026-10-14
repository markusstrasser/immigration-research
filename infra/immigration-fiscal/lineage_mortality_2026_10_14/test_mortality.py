"""Regression checks on the source mapping, attribution and output boundaries."""
import sys
from pathlib import Path

sys.dont_write_bytecode = True
import numpy as np
import pandas as pd
import pytest
import mortality as M

HERE = Path(__file__).resolve().parent


@pytest.fixture(scope="session", autouse=True)
def memory_budget(request):
    assert request.config.pluginmanager.get_plugin("cacheprovider") is None, "lane tests must not write shared pytest cache"
    yield
    M.require_within_budget("lineage mortality tests")


def test_primary_cells_and_models():
    h = pd.read_csv(HERE / "derived/hazard_ratios.csv")
    # Independently read against rendered PDF pages 6/7, including all CI ends.
    expected = {
        ("male", "us_born"): [(1.22, 1.15, 1.30), (1.03, .96, 1.10), (.87, .81, .94), (.77, .71, .83)],
        ("male", "foreign_born"): [(1.18, 1.11, 1.25), (.97, .91, 1.03), (.71, .64, .78), (.60, .55, .66)],
        ("female", "us_born"): [(.98, .91, 1.06), (.80, .74, .87), (.92, .86, .99), (.82, .76, .88)],
        ("female", "foreign_born"): [(1.28, 1.19, 1.38), (.87, .81, .94), (.79, .72, .86), (.66, .60, .73)],
    }
    assert len(h) == 16
    for (sex, nat), cells in expected.items():
        rs = h[(h.sex == sex) & (h.nativity == nat)].sort_values("model")
        assert rs[["hr", "ci_low", "ci_high"]].to_numpy().tolist() == [list(c) for c in cells]
        assert list(rs.age_band) == ["25-64", "25-64", "65+", "65+"]


def test_qx_age_sex_nativity_and_terminal_boundary():
    h = pd.read_csv(HERE / "derived/hazard_ratios.csv")
    ref = {s: np.full(121, .01) for s in ("male", "female")}
    usb = M.build_qx(ref, h, "central", "us_born")
    fb = M.build_qx(ref, h, "central", "foreign_born")
    assert usb["female"][24] == .01
    assert usb["female"][25] == .0098
    assert usb["male"][64] == .0122
    assert usb["male"][65] == .0087
    assert fb["male"][65] == pytest.approx(.0071, rel=1e-14)
    assert np.all(fb["male"][100:] == 1)
    salmon = M.build_qx(ref, h, "salmon_all_extra", "foreign_born")
    assert salmon["male"][64] == fb["male"][64]
    assert salmon["male"][65] == usb["male"][65]
    arm18 = M.build_qx(ref, h, "extend_to_18", "foreign_born")
    assert arm18["female"][17] == .01
    assert arm18["female"][18] == fb["female"][25]


def test_added_componentwise_bound_not_average():
    controls = [dict(basis="added_profile", group="a", age_mix="x", oasdi_per_tax_dollar_net=1., part_a_per_hi_tax_dollar=1.),
                dict(basis="added_profile", group="b", age_mix="x", oasdi_per_tax_dollar_net=1., part_a_per_hi_tax_dollar=1.)]
    new = [dict(group="a", age_mix="x", oasdi_per_tax_dollar_net=1.2, part_a_per_hi_tax_dollar=.9),
           dict(group="b", age_mix="x", oasdi_per_tax_dollar_net=1.1, part_a_per_hi_tax_dollar=1.3)]
    lo, hi, _ = M.profile_deltas(new, controls, dict(added_ss_bn=5., added_part_a_bn=2.))
    assert abs(lo - .3) < 1e-12
    assert abs(hi - 1.6) < 1e-12


def test_generated_account_closure_cash_and_comparison_signs():
    case = pd.read_csv(HERE / "derived/case_changes.csv")
    gen = pd.read_csv(HERE / "derived/generation_changes.csv")
    assert (case.query("basis == 'cash'").lineage_delta_low_bn == 0).all()
    assert (case.query("basis == 'cash'").cost_low_bn == case.query("basis == 'cash'").base_cost_bn).all()
    for _, r in case.query("basis == 'accrual'").iterrows():
        parts = gen[(gen.arm == r.arm) & (gen.end == r.end)]
        assert abs(parts.delta_low_bn.sum() - r.lineage_delta_low_bn) < 1e-9
        assert abs(parts.delta_high_bn.sum() - r.lineage_delta_high_bn) < 1e-9
    comparison = pd.read_csv(HERE / "derived/comparisons.csv")
    for _, r in comparison.iterrows():
        assert abs(r.lineage_new_cost_low_bn - r.white_cost_bn - r.white_gap_new_low_bn) < 1e-9
        assert abs(r.black_cost_bn - r.lineage_new_cost_high_bn - r.black_minus_lineage_new_low_bn) < 1e-9


def test_all_source_pins_still_match():
    M.check_pins()


def test_consumed_salmon_source_tampering_fails_closed(monkeypatch):
    original = M.hashlib.file_digest

    def changed(stream, algorithm):
        if Path(stream.name).name == "salmon_turra_rates.csv":
            return M.hashlib.sha256(b"changed proxy cells")
        return original(stream, algorithm)

    monkeypatch.setattr(M.hashlib, "file_digest", changed)
    with pytest.raises(SystemExit, match=r"\[BLOCKED\] pin .*salmon_turra_rates.csv"):
        M.check_pins()


def test_salmon_changes_only_g1_and_cash_generations_are_zero():
    r = pd.read_csv(HERE / "derived/accrual_ratios.csv")
    base = r[(r.arm == "central") & ((r.basis == "added_profile") | r.group.isin(["G2", "G3plus"]))]
    cols = ["oasdi_per_tax_dollar_net", "part_a_per_hi_tax_dollar", "benefit_tax_timing"]
    for arm in ("salmon_all_extra", "salmon_turra_pooled_proxy"):
        selected = r[(r.arm == arm) & ((r.basis == "added_profile") | r.group.isin(["G2", "G3plus"]))]
        assert selected[cols].to_numpy().tolist() == base[cols].to_numpy().tolist()
    cash = pd.read_csv(HERE / "derived/generation_changes_cash.csv")
    assert (cash[["oasdi_delta_bn", "part_a_delta_bn", "delta_low_bn", "delta_high_bn"]] == 0).all().all()
