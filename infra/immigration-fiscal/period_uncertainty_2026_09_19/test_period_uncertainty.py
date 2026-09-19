import importlib.util
import json
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

spec = importlib.util.spec_from_file_location("period_uncertainty", Path(__file__).with_name("period_uncertainty.py"))
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)


def test_shared_age_errors_remain_correlated():
    net = np.zeros((6, 161))
    net[:, 1:] = 2
    result = m.conditional_estimate(net, np.ones_like(net), np.zeros((6, 1)), np.zeros((1, 1)), np.ones(6))
    assert result["variance_cps"] == 4 * 12**2


def test_shared_medical_donors_cancel_for_signed_contrast():
    gradient = np.array([[1.], [-1.], [0.], [0.], [0.], [0.]])
    result = m.conditional_estimate(np.zeros((6, 161)), np.ones((6, 161)), gradient, np.array([[100.]]), np.ones(6))
    assert result["variance_meps"] == 0


def test_institution_denominator_and_independent_replicates():
    pop = np.full((6, 161), 10.)
    pop[:, 1:] = 20
    inst = np.full((6, 81), 2.)
    inst[:, 1:] = 3
    result = m.conditional_estimate(np.zeros_like(pop), pop, np.zeros((6, 1)), np.zeros((1, 1)), np.ones(6), inst, 100)
    assert result["estimate"] == -120
    assert result["variance_cps"] == pytest.approx(4 * 60**2)
    assert result["variance_acs"] == pytest.approx(4 * 60**2)


def test_discount_derivative_matches_finite_difference_with_mixed_signs():
    table = pd.DataFrame({"age": np.arange(101), "lx": np.full(101, 100000), "Lx": np.full(101, 100000)})
    values = np.array([1000, 2000, 3000, -2000, -6000, -10000])
    w, dw = m.survival_weights(table, .03)
    h = 1e-6
    finite = ((m.survival_weights(table, .03+h)[0] - m.survival_weights(table, .03-h)[0]) @ values) / (2*h)
    assert dw @ values == pytest.approx(finite, rel=1e-8)
    assert w.sum() > 0


def test_missing_band_is_withheld_not_filled():
    pop = np.ones((6, 161))
    pop[4] = 0
    assert not m.support_ok(pop, np.full(6, 50), np.full(6, 50))
    with pytest.raises(ValueError, match="Unsupported population"):
        m.conditional_estimate(np.zeros_like(pop), pop, np.zeros((6, 1)), np.zeros((1, 1)), np.ones(6))


def test_stale_input_is_rejected(tmp_path):
    p = tmp_path / "source"
    p.write_text("before")
    record = m.fingerprint(p)
    p.write_text("after")
    with pytest.raises(ValueError, match="Stale input"):
        m.verify_fingerprints([record])


def test_tampered_health_release_is_rejected(tmp_path):
    source = tmp_path / "source"
    source.write_text("source evidence")
    files = [tmp_path / "estimates.csv", tmp_path / "medical_uncertainty.npz"]
    for p in files:
        p.write_text("original")
    audit = {"inputs": [m.fingerprint(source)],
             "outputs": {p.name: m.fingerprint(p)["sha256"] for p in files}}
    (tmp_path / "audit.json").write_text(json.dumps(audit))
    m.verify_health_release(tmp_path)
    files[0].write_text("altered but plausibly formatted estimates")
    with pytest.raises(ValueError, match="Stale input"):
        m.verify_health_release(tmp_path)
