"""Independent small-frame checks of actual-driver extension and blocking."""
import copy
import csv
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

from national_keys import full_key


def snapshot():
    vectors = {
        ("receipt", "payroll"): np.array([1., 3., 5., 7.]),
        ("receipt", "hi_payroll"): np.array([2., 4., 8., 16.]),
        ("receipt", "self_payroll"): np.array([0., 2., 3., 4.]),
        ("receipt", "income_tax"): np.array([5., 6., 7., 8.]),
        ("spending", "social_security"): np.array([4., 0., 2., 1.]),
        ("spending", "medicare"): np.array([1., 2., 4., 8.]),
        ("spending", "school_part"): np.array([1., 0., 2., 0.]),
        ("spending", "P_part"): np.array([0., 1., 0., 2.]),
        ("spending", "economic"): np.array([1., 2., 3., 4.]),
        ("spending", "medicaid"): np.array([2., 3., 4., 5.]),
        ("spending", "population"): np.ones(4),
    }
    rows = [
        dict(side="receipt", id="oasdi", key="payroll", amount_bn=7.),
        dict(side="receipt", id="hi", key="hi_payroll", amount_bn=10.),
        dict(side="receipt", id="se", key="self_payroll", amount_bn=4.),
        dict(side="receipt", id="federal_income_tax", key="income_tax"),
        dict(side="spending", id="social_security", key="social_security"),
        dict(side="spending", id="medicare", key="medicare"),
        dict(side="spending", id="education_services", key="education_mix"),
        dict(side="spending", id="school_reprice", key="population"),
        dict(side="spending", id="public_order_safety", key="population"),
        dict(side="spending", id="state_price_public_order_safety", key="population"),
        dict(side="spending", id="economic_affairs_services", key="economic"),
        dict(side="spending", id="roads_vmt_sl", key="population"),
        dict(side="spending", id="uninsured", key="uninsured_use"),
    ]
    capital = [dict(id="hwy", rule=dict(kind="part_rekeyed", parent_line="economic_affairs_services", correction_line="roads_vmt_sl")),
               dict(id="school_offset", rule=dict(kind="receipt_amount_over_national", line="school_carrier")),
               dict(id="enterprise", rule=dict(kind="receipt_amount_over_national", line="enterprise_surplus"))]
    G = dict(allocation="personal", rows=rows, capital=capital,
             roads={"roads_vmt_sl": dict(freight_key="income_tax", old_key="economic")})
    return dict(d=pd.DataFrame({"NOCOV_CYR": [3, 2, 1, 3]}), rows_u=np.array([0, 1, 2]),
                gens={"G1": np.array([True, True, False, False])}, age=np.array([6, 22, 44, 70]),
                W=np.array([[10.], [20.], [30.], [40.]]), w_id=np.array([10., 20., 30., 40.]),
                vec={"personal": vectors},
                PA=dict(oasdi_lines=["oasdi"], hi_lines=["hi"], se_line="se", se_oasdi_share=.75),
                prod_parts={"low": dict(earn=np.array([2., 3., 4., 5.]), cells=[np.array([1, 0, 1, 0]), np.array([0, 1, 0, 1])])},
                lines={"generations": {"G1": {"low": G}},
                       "meta": dict(routes=[dict(side="spending", line="school_reprice", basis="education_services", part="k12")],
                                    carriers={"school_carrier": dict(parent_line="education_services")})})


def piece(lid, category, first_two):
    return dict(g="G1", id=lid, cat=category, bn=1., x=np.array([*first_two, 0.]))


@pytest.mark.parametrize("lid,cat,key", [
    ("oasdi", "taxes", ("receipt", "payroll")),
    ("federal_income_tax", "taxes", ("receipt", "income_tax")),
    ("federal_income_tax", "taxes", ("spending", "social_security")),
    ("medicare", "health", ("spending", "medicare")),
    ("education_services", "schools", ("spending", "school_part")),
    ("school_reprice", "education_other", ("spending", "P_part")),
    ("roads_vmt_sl", "roads_parks", ("receipt", "income_tax")),
    ("hwy", "capital", ("spending", "economic")),
    ("school_offset", "capital", ("spending", "P_part")),
])
def test_declared_driver_recovers_out_of_generation_values(lid, cat, key):
    s = snapshot()
    expected = s["vec"]["personal"][key]
    full, source, override = full_key(s, piece(lid, cat, expected[:2]), "low")
    np.testing.assert_array_equal(full, expected)
    assert "exact_declared_driver" in source
    assert override is None


@pytest.mark.parametrize("lid,cat,expected", [
    ("public_order_safety", "justice_use", [0., 1., 1., 0.]),
    ("state_price_public_order_safety", "justice_use", [0., 1., 1., 0.]),
    ("public_order_safety", "justice_per_head", [1., 1., 1., 1.]),
    ("roads_vmt_sl", "roads_parks", [1., 1., 1., 1.]),
    ("enterprise", "capital", [1., 1., 1., 1.]),
    ("production", "production", [2., 0., 4., 0.]),
    ("production", "production", [0., 3., 0., 5.]),
    ("uninsured", "health", [1., .5, 0., 1.]),
])
def test_custom_and_parent_drivers(lid, cat, expected):
    full, _, _ = full_key(snapshot(), piece(lid, cat, expected[:2]), "low")
    np.testing.assert_array_equal(full, expected)


def test_pension_receipts_use_exact_generation_coefficients():
    s = snapshot()
    v = s["vec"]["personal"]
    # Generation receipt coefficients: OASDI 7/(1*10+3*20),
    # self-employment OASDI .75*4/(0*10+2*20). Do not use a raw wage key.
    expected = .1 * v[("receipt", "payroll")] + .075 * v[("receipt", "self_payroll")]
    full, source, _ = full_key(s, piece("social_security", "pension_accrual", expected[:2]), "low")
    np.testing.assert_allclose(full, expected, rtol=1e-15, atol=0)
    assert "fixed generation receipt coefficients" in source


def test_part_a_receipt_composite():
    s = snapshot()
    v = s["vec"]["personal"]
    expected = .1 * v[("receipt", "hi_payroll")] + .025 * v[("receipt", "self_payroll")]
    full, _, _ = full_key(s, piece("medicare", "pension_accrual", expected[:2]), "low")
    np.testing.assert_allclose(full, expected, rtol=1e-15, atol=0)


def test_ambiguous_same_generation_different_outside_blocks():
    s = snapshot()
    s["vec"]["personal"][("spending", "P_part")] = np.array([1., 0., 9., 0.])
    with pytest.raises(SystemExit, match=r"\[BLOCKED\].*ambiguous full-frame"):
        full_key(s, piece("education_services", "schools", [1., 0.]), "low")


def test_identical_extensions_have_multiple_legitimate_sources():
    s = snapshot()
    s["vec"]["personal"][("spending", "P_part")] = s["vec"]["personal"][("spending", "school_part")].copy()
    full, source, _ = full_key(s, piece("education_services", "schools", [1., 0.]), "low")
    np.testing.assert_array_equal(full, [1., 0., 2., 0.])
    assert "school_part" in source and "P_part" in source


def test_metadata_key_cannot_replace_actual_vector():
    with pytest.raises(SystemExit, match=r"\[BLOCKED\].*no exact declared extension"):
        full_key(snapshot(), piece("oasdi", "taxes", [9., 9.]), "low")


@pytest.mark.parametrize("mutation, message", [
    (lambda s: s["lines"]["generations"]["G1"]["low"]["rows"].append(copy.deepcopy(s["lines"]["generations"]["G1"]["low"]["rows"][0])), "duplicate generation"),
    (lambda s: s["vec"]["personal"][("receipt", "payroll")].__setitem__(3, np.nan), "invalid full candidate"),
    (lambda s: s["vec"]["personal"][("receipt", "payroll")].__setitem__(3, -1.), "invalid full candidate"),
    (lambda s: s.__setitem__("rows_u", np.array([0, 0, 2])), "duplicate/out-of-frame"),
])
def test_invalid_principal_inputs_block(mutation, message):
    s = snapshot()
    mutation(s)
    with pytest.raises(SystemExit, match=r"\[BLOCKED\].*" + message):
        full_key(s, piece("oasdi", "taxes", [1., 3.]), "low")


def test_nonzero_outside_generation_blocks():
    p = piece("oasdi", "taxes", [1., 3.])
    p["x"][2] = 1.
    with pytest.raises(SystemExit, match=r"\[BLOCKED\].*leaks outside"):
        full_key(snapshot(), p, "low")


def test_zero_pension_receipt_denominator_blocks():
    s = snapshot()
    s["vec"]["personal"][("receipt", "self_payroll")][:2] = 0
    with pytest.raises(SystemExit, match=r"\[BLOCKED\].*non-positive pension"):
        full_key(s, piece("social_security", "pension_accrual", [1., 3.]), "low")


def test_union_tenant_driver_uses_principal_all_rent_denominator():
    s = snapshot()
    path = Path(__file__).resolve().parents[1] / "receipt_side_long_run_2026_09_28/derived/states.csv"
    with path.open(newline="") as stream:
        states = list(csv.DictReader(stream))
    group_rent = sum(float(r["group_rent"]) for r in states)
    national_rent = sum(float(r["all_rent"]) for r in states)
    vector = np.array([group_rent / 30, group_rent / 30, 0., 0.])
    s["vec"]["personal"][("receipt", "renter_contract_rent")] = vector
    s["lines"]["generations"]["G1"]["low"]["rows"].append(dict(side="receipt", id="tenant_occupied_property", key="renter_contract_rent"))
    full, source, override = full_key(s, piece("tenant_occupied_property", "taxes", vector[:2]), "low")
    np.testing.assert_array_equal(full, vector)
    assert override == pytest.approx(national_rent, rel=1e-15)
    assert override > full @ s["w_id"]
    assert "principal national mass" in source


def test_union_tenant_principal_mass_mismatch_blocks():
    s = snapshot()
    s["vec"]["personal"][("receipt", "renter_contract_rent")] = np.array([1., 1., 0., 0.])
    s["lines"]["generations"]["G1"]["low"]["rows"].append(dict(side="receipt", id="tenant_occupied_property", key="renter_contract_rent"))
    with pytest.raises(SystemExit, match=r"\[BLOCKED\].*principal group rent"):
        full_key(s, piece("tenant_occupied_property", "taxes", [1., 1.]), "low")
