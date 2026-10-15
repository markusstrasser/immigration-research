"""Trust-fund payer premises: covered earnings and post-2024-born workers."""
import importlib.util
from pathlib import Path
from types import SimpleNamespace

import numpy as np
import pandas as pd
import pytest

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("p8_test_cohorts", HERE / "p7_cohorts.py")
cohort = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cohort)
PARAMETERS = SimpleNamespace(SECA_FACTOR=.9235, ext=SimpleNamespace(OASDI_CAP_2024=168600.))
LIFE = SimpleNamespace(qx_table=lambda population, sex: np.zeros(121))
DECLINE = {"65plus": 0., "total": 0.}


def test_payroll_key_uses_covered_earnings_not_benefit_receipt():
    d = pd.DataFrame(dict(pw=[2., 1., 1.], other=[True, True, False],
                          WSAL_VAL=[200000., 0., 999999.], SEMP_VAL=[0., 50000., 0.],
                          FRSE_VAL=[0., 0., 0.], SS_VAL=[0., 50000., 0.]))
    oasdi, hi = cohort.covered_earnings(d, PARAMETERS)
    assert oasdi.tolist() == [168600., 46175., 168600.]
    assert hi.tolist() == [200000., 46175., 999999.]
    key = cohort.payroll_key(d, .25, PARAMETERS)
    assert np.dot(d.pw, key) == pytest.approx(1., abs=1e-12)
    assert key[0] > key[1] > 0 and key[2] == 0
    changed = d.assign(SS_VAL=[999999., 0., 0.])
    assert np.array_equal(key, cohort.payroll_key(changed, .25, PARAMETERS))


def projection_fixture():
    ages = np.array([0, 15, 35, 70] * 2)
    sex = np.repeat([1, 2], 4)
    weights = np.ones(8)
    other = np.ones(8, bool)
    earnings = np.array([0., 100., 100., 0.] * 2)
    years = np.arange(2024, 2101)
    return cohort._payroll_projection(ages, sex, weights, other, earnings,
                                     years, np.ones((len(years), 3)), LIFE, DECLINE), years


def test_future_born_payers_enter_at_covered_earnings_age_not_retirement():
    projection, years = projection_fixture()
    born = projection["future_born"]
    # Earliest observed covered earnings are at 15. A person born in 2025
    # first reaches that age in 2040; retirement receipt would exclude them
    # until 2090. This tests the cohort boundary, not arithmetic closure alone.
    assert np.all(born[years < 2040] == 0)
    assert born[years == 2040][0] > 0
    assert np.all(born[(years >= 2040) & (years < 2090)] > 0)
    assert np.all(projection["living"] + born <= projection["denominator"] + 1e-12)


def test_payroll_floor_preserves_future_born_when_closed_cohort_exceeds_projection():
    projection, years = projection_fixture()
    constrained = projection["living"] + projection["future_born"] > projection["raw"]
    assert constrained.any()
    assert np.array_equal(projection["denominator"][constrained],
                          (projection["living"] + projection["future_born"])[constrained])
    schedule = (years == 2060).astype(float)
    share = np.sum(schedule * projection["living"] / projection["denominator"])
    unborn_share = np.sum(schedule * projection["future_born"] / projection["denominator"])
    assert 0 < unborn_share <= 1 - share + 1e-12


def test_missing_covered_earnings_blocks_instead_of_using_receipts():
    d = pd.DataFrame(dict(pw=[1.], other=[True], SS_VAL=[10000.], FICA=[0.]))
    with pytest.raises(ValueError, match="BLOCKED.*covered earnings missing"):
        cohort.payroll_key(d, .25, PARAMETERS)


@pytest.mark.parametrize("weight", [np.nan, -1.])
def test_invalid_payroll_weights_block(weight):
    d = pd.DataFrame(dict(pw=[weight], other=[True], WSAL_VAL=[10000.],
                          SEMP_VAL=[0.], FRSE_VAL=[0.]))
    with pytest.raises(ValueError, match="BLOCKED.*payroll payer weights"):
        cohort.payroll_key(d, .25, PARAMETERS)


def test_cohort_trust_key_is_receipt_independent_and_borrowing_keys_conserved():
    ages = np.arange(0, 86, 5)
    d = pd.DataFrame(dict(A_AGE=np.tile(ages, 2),
                          A_SEX=np.repeat([1, 2], len(ages))))
    d["pw"] = 1000.
    d["other"] = True
    d["target"] = False
    d["WSAL_VAL"] = np.where(d.A_AGE.between(15, 60), 50000., 0.)
    d["SEMP_VAL"] = d["FRSE_VAL"] = 0.
    d["FICA"] = d.WSAL_VAL * .0765
    d["FEDTAX_AC"] = d.WSAL_VAL * .1
    d["SS_VAL"] = np.where(d.A_AGE >= 65, 20000., 0.)
    target = d.iloc[[6]].assign(other=False, target=True)
    d = pd.concat([d, target], ignore_index=True)
    totals = {"accrual_bn": 75., "hi_payout_fraction": .25, "borrowing30": 30.,
              "payroll_bn": 144., "cash_benefits_bn": 77., "trust_cost_bn": 8.}
    result = cohort.cohort_keys(d, None, totals)
    alternative = cohort.cohort_keys(d.assign(SS_VAL=999999.), None, totals)
    for name in ("trust", "borrowing10", "borrowing30"):
        assert np.array_equal(result["keys"][name], alternative["keys"][name])
        assert np.dot(d.pw, result["keys"][name]) == pytest.approx(1., abs=1e-12)
    assert result["gates"]["trust_post2024_born_share"] > 0
    assert result["keys"]["trust"][d.A_AGE >= 65].sum() == 0
    assert result["component_living_shares"]["accrual_bn"] < 1
    assert set(result["component_living_shares"]) == {"accrual_bn", "borrowing30"}
    assert result["gates"]["component_conservation"]
