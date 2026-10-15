"""Regression checks for the new carrier incidence and footprint boundary."""
import importlib.util
from pathlib import Path
from types import SimpleNamespace

import pytest
import valuation as V
import measured_run as M


def payload(source):
    return {"meta": {"union_completion": {"carriers": {"new_receipt": source}}}}


def test_receipt_carrier_preserves_declared_class_and_payer():
    src = dict(kind="line", side="receipt", parent_line="corporate_capital", parent_key="cbo_collective")
    got = V.completion_incidence(payload(src), {"corporate_capital": "source_tax"}, {"corporate_capital": "capital_owners"})
    assert got["new_receipt"]["incidence_class"] == "source_tax"
    assert got["new_receipt"]["economic_payer"] == "capital_owners"


@pytest.mark.parametrize("classes,payers", [({}, {}), ({"corporate_capital": "source_tax"}, {})])
def test_unknown_receipt_class_or_payer_stops(classes, payers):
    src = dict(kind="line", side="receipt", parent_line="corporate_capital", parent_key="cbo_collective")
    with pytest.raises(SystemExit, match="completion_receipt_incidence"):
        V.completion_incidence(payload(src), classes, payers)


def test_unknown_carrier_kind_stops():
    with pytest.raises(SystemExit, match="completion_unknown_source"):
        V.completion_incidence(payload(dict(kind="unknown", parent_line="corporate_capital")), {}, {})


def test_wrapper_reports_rss_without_rejecting_success(monkeypatch, tmp_path):
    monkeypatch.setattr(M, "__file__", str(tmp_path / "measured_run.py"))
    monkeypatch.setattr(M.sys, "argv", ["measured_run.py", "true"])
    monkeypatch.setattr(M.subprocess, "run", lambda command: SimpleNamespace(returncode=0))
    monkeypatch.setattr(M.resource, "getrusage", lambda kind: SimpleNamespace(ru_maxrss=10_000_000_000))
    with pytest.raises(SystemExit) as result:
        M.main()
    assert result.value.code == 0
