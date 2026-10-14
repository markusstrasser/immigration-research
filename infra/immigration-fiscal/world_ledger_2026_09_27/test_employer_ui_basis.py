"""Primary-table employer share, foreign exclusion and explicit rounding closure."""
import json
from decimal import Decimal

import numpy as np
import pytest

import employer_ui_basis as E


def test_primary_payer_split_and_ui_subset_close():
    b = E.load_basis()
    c = b["cells"]
    # Primary values are published in integer millions: exact decimal arithmetic
    # is the positive control, independently of implementation evaluation order.
    denom = float(Decimal(str(c["T30100-A/8"]["bn"]))
                  - sum(Decimal(str(c[f"T30600-A/{i}"]["bn"])) for i in (22, 4, 27)))
    employer = float(Decimal(str(c["T30600-A/2"]["bn"])) - Decimal(str(c["T30600-A/4"]["bn"])))
    assert b["national_domestic_residual_bn"] == denom
    assert b["national_employer_residual_bn"] == employer
    assert b["employer_fraction"] == employer / denom
    assert b["national_employer_ui_bn"] <= employer
    assert abs(sum(b[k] for k in ("national_employer_residual_bn", "national_worker_residual_bn",
                                  "national_source_rounding_bn")) - denom) < 1e-6
    assert b["unidentified_group_employer_fraction_bound"] == [0.0, 1.0]


def test_matched_allocation_adds_employer_only_to_compensation():
    b = E.load_basis()
    for group_total in (0., 10., 100.):
        out = E.allocate_group(group_total, b)
        assert abs(out["employer_bn"] + out["worker_bn"] + out["source_rounding_bn"] - group_total) < 1e-6
        assert out["employer_bn"] == group_total * b["employer_fraction"]
        assert out["ui_subset_bn"] <= out["employer_bn"] <= group_total
        assert out["unidentified_employer_bound_bn"] == [0., group_total]


@pytest.mark.parametrize("value", [np.nan, np.inf, -1.])
def test_bad_group_value_fails_closed(value):
    with pytest.raises(SystemExit, match="group_residual_finite_nonnegative"):
        E.allocate_group(value)


def test_source_hash_guard(tmp_path, monkeypatch):
    (tmp_path / "inputs").mkdir()
    (tmp_path / "inputs" / E.SOURCE).write_bytes(b"corrupt workbook")
    (tmp_path / "inputs/pins.json").write_text(json.dumps({"files": {
        E.SOURCE: {"path": f"inputs/{E.SOURCE}", "sha256": "0" * 64}}}))
    monkeypatch.setattr(E, "HERE", tmp_path)
    with pytest.raises(SystemExit, match="source_hash"):
        E.source_path()


def test_nonfinite_national_cell_fails_closed():
    path, _ = E.source_path()
    a = E.read_table(path, "T30100-A")
    c = E.read_table(path, "T30600-A")
    c[2]["bn"] = np.nan
    with pytest.raises(SystemExit, match="cell_finite"):
        E.compute_basis(a, c)
