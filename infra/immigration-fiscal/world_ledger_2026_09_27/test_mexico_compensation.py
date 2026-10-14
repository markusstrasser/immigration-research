"""P7 Mexican compensation: statutory provenance, conservation and cash positive controls."""
import io
import json

import numpy as np
import pandas as pd
import pytest

import mexico as M


def test_primary_source_hash_fails_closed(tmp_path, monkeypatch):
    p = tmp_path / "changed.txt"
    p.write_text("not the pinned primary source")
    (tmp_path / "pins.json").write_text(json.dumps({"files": {
        "changed.txt": {"path": "changed.txt", "sha256": "0" * 64}}}))
    monkeypatch.setattr(M, "INPUTS", tmp_path)
    monkeypatch.setattr(M, "HERE", tmp_path)
    with pytest.raises(SystemExit, match="primary_source_sha256"):
        M.pinned_text("changed.txt")


def test_2024_schedule_is_parsed_and_contributions_add_once():
    p = M.employer_parameters()
    # Independent formula at five UMA: use the source's own parsed values, the last
    # 2024 CEAV tier, and the fixed UMA quota. Detect wrong year, duplicate SAR or caps.
    g = np.array([0.0, 5 * M.UMA_YEAR, 50 * M.UMA_YEAR])
    c = M.mx_employer_contributions(g)
    base = np.minimum(g, p["cap_uma"] * M.UMA_YEAR)
    expected = ((base * (p["cash_benefit"] + p["pension_medical"] + p["disability_life"]
                          + p["daycare"] + p["risk"] + p["retirement"]
                          + p["ceav_rates"][-1] + p["housing"]))
                + p["excess"] * np.maximum(base - 3 * M.UMA_YEAR, 0)
                + p["fixed"] * M.UMA_YEAR * (g > 0))
    np.testing.assert_allclose(c["total"], expected, rtol=0, atol=1e-9)
    np.testing.assert_allclose(c["total"], c["imss"] + c["housing"] + c["retirement"], rtol=0, atol=1e-9)
    assert c["total"][0] == 0
    for component in c:
        assert (c[component] >= 0).all()


def test_occupational_risk_bound_and_unknown_duration_are_explicit():
    p = M.employer_parameters()
    g = np.array([0., 1000., 5 * M.UMA_YEAR])
    central = M.mx_employer_contributions(g)
    low = M.mx_employer_contributions(g, p["risk_min"])
    high = M.mx_employer_contributions(g, p["risk_max"])
    full = M.mx_employer_contributions(g, full_year=True)
    assert (low["total"] <= central["total"]).all()
    assert (high["total"] >= central["total"]).all()
    assert (full["total"] >= central["total"]).all()
    assert full["total"][0] == 0
    with pytest.raises(SystemExit, match="risk_inside_statute"):
        M.mx_employer_contributions(g, p["risk_min"] / 2)


@pytest.mark.parametrize("g", [[np.nan], [np.inf], [-1.]])
def test_nonfinite_or_negative_formal_pay_blocks(g):
    with pytest.raises(SystemExit, match="pay_finite_nonnegative"):
        M.mx_employer_contributions(g)


@pytest.fixture(scope="module")
def enigh():
    return M.load_enigh()


def test_formal_only_and_cash_tax_basis_stays_unchanged(enigh):
    d = enigh
    assert (d.employer_mxn[d.formal_net_mxn == 0] == 0).all()
    np.testing.assert_allclose(d.compensation_mxn, d.gross_mxn + d.employer_mxn, rtol=0, atol=1e-7)
    np.testing.assert_allclose(d.total_tax_mxn, d.withheld_tax_mxn + d.employer_mxn, rtol=0, atol=1e-7)
    np.testing.assert_allclose(d.compensation_mxn - d.total_tax_mxn,
                               d.gross_mxn - d.withheld_tax_mxn, rtol=0, atol=1e-7)
    np.testing.assert_allclose(d.ctax_mxn, d.gross_mxn * d.ctax_rate, rtol=0, atol=1e-7)


@pytest.mark.parametrize("young", [False, True])
def test_current_oct14_cash_and_employee_tax_positive_control(enigh, young):
    name = "mexico_young_by_parent.csv" if young else "mexico_earnings_cells.csv"
    baseline = pd.read_csv(io.StringIO(M.pinned_text(f"positive_control_{name}")))
    rates = M.ppp()
    if young:
        new = M.young_by_parent(enigh, rates)
        keys = ["sex", "band", "parent_cat"]
    else:
        new = M.cells(enigh)
        M.add_ppp(new, rates)
        keys = ["sex", "band", "cat"]
    old = baseline.set_index(keys).sort_index()
    new = new.set_index(keys).sort_index()
    assert old.index.equals(new.index)
    # Existing CSV precision is six significant digits; compare the serialized old
    # columns byte-for-byte after regenerating, not a newly relaxed numeric tolerance.
    columns = [c for c in old if c in new]
    numeric = [c for c in columns if pd.api.types.is_numeric_dtype(old[c])]
    text = new[numeric].to_csv(index=False, float_format="%.6g", lineterminator="\n")
    expected = old[numeric].to_csv(index=False, float_format="%.6g", lineterminator="\n")
    assert text == expected
    for ppp in ("gdp", "consumption"):
        assert f"compensation_per_person_ppp_{ppp}" in new
        assert f"total_tax_per_person_ppp_{ppp}" in new
        assert f"employer_per_person_ppp_{ppp}" in new
