"""Exact canonical item-12 donors, scope separation and fail-loud transport."""
import copy
import json

import numpy as np
import pandas as pd
import pytest

import coverage_transport as C


def test_exported_cell_means_close_to_item12_people_and_fiscal_amounts():
    donors, receipt = C.load_donors("oct15", "cash")
    principal = json.loads((C.COVERAGE / "derived/coverage_bound_oct15.json").read_text())
    central = principal["sets"]["cash"]["scenarios"]["central"]
    C.validate_closure(donors, central)
    # Aggregating the exact donor distribution to cell means preserves every
    # fiscal component and count, including signed overcount corrections.
    cells = []
    for key, group in donors.groupby(["age", "sex", "generation"]):
        mass = group.coverage_weight.sum()
        if mass == 0:
            continue
        cells.append(dict(generation=key[2], mass=mass,
            low_mean=group.coverage_weight @ group.fiscal_low_bn_per_person / mass,
            high_mean=group.coverage_weight @ group.fiscal_high_bn_per_person / mass))
    cells = pd.DataFrame(cells)
    for generation in C.GENS:
        d = cells[cells.generation.eq(generation)]
        g = generation.replace("G3+", "G3plus")
        assert d.mass.sum() == pytest.approx(central["implied_net_missing_people"][g], abs=1e-6)
        for end in ("low", "high"):
            assert d.mass @ d[f"{end}_mean"] == pytest.approx(
                central["ends"][end]["by_generation"][g], abs=1e-9)
    assert receipt["basis"] == "cash"


def sample():
    frame = pd.DataFrame(dict(PH_SEQ=[1, 2, 3], PPPOS=[1, 1, 1],
        A_AGE=[30, 30, 40], A_SEX=[1, 1, 2], gen=["G1", "G1", ""],
        target=[True, True, False], pw=[10., 20., 50.],
        earn=[100., 400., 500.], rank_weight=[1.2, .8, 1.]))
    donors = pd.DataFrame(dict(PH_SEQ=[2, 1], PPPOS=[1, 1], age=[30, 30], sex=[1, 1],
        generation=["G1", "G1"], coverage_weight=[4., 1.]))
    return frame, donors


def test_transport_preserves_counted_scope_and_other_reference(monkeypatch):
    frame, donors = sample()
    monkeypatch.setattr(C, "load_donors", lambda *args: (donors, {"basis": "cash"}))
    out = C.transport_weights(frame)
    np.testing.assert_array_equal(out.pw_counted, frame.pw)
    np.testing.assert_array_equal(out.pw, [11., 24., 50.])
    assert out.pw[~out.target].equals(frame.pw[~frame.target])
    assert (out.coverage_pw * out.earn).sum() == 1700.
    assert (out.coverage_pw * out.rank_weight).sum() == pytest.approx(4.4)
    # The original input and its scope-B earnings are untouched.
    assert "coverage_pw" not in frame
    assert (out.pw_counted * out.earn).sum() == (frame.pw * frame.earn).sum()


@pytest.mark.parametrize("defect,reason", [("missing", "missing"), ("age", "ages"),
    ("sex", "sexes"), ("generation", "generations"), ("nonmember", "outside")])
def test_incompatible_donor_frame_fails(monkeypatch, defect, reason):
    frame, donors = sample()
    if defect == "missing":
        donors.loc[0, "PH_SEQ"] = 9
    elif defect == "age":
        donors.loc[0, "age"] = 31
    elif defect == "sex":
        donors.loc[0, "sex"] = 2
    elif defect == "generation":
        donors.loc[0, "generation"] = "G2"
    else:
        frame.loc[1, "target"] = False
    monkeypatch.setattr(C, "load_donors", lambda *args: (donors, {}))
    with pytest.raises(SystemExit, match=reason):
        C.transport_weights(frame)


def test_changed_principal_count_or_fiscal_amount_blocks():
    donors, _ = C.load_donors("oct15", "cash")
    central = json.loads((C.COVERAGE / "derived/coverage_bound_oct15.json").read_text())["sets"]["cash"]["scenarios"]["central"]
    bad = copy.deepcopy(central)
    bad["implied_net_missing_people"]["G1"] += 1.
    with pytest.raises(SystemExit, match="missing people"):
        C.validate_closure(donors, bad)
    bad = copy.deepcopy(central)
    bad["ends"]["low"]["by_generation"]["G1"] += .001
    with pytest.raises(SystemExit, match="fiscal amount"):
        C.validate_closure(donors, bad)


def test_g3_donor_components_are_fixed_before_coverage_transport(monkeypatch):
    import beside_arms as B
    import g2_premium as G

    counted = pd.DataFrame(dict(gen=["G1", "G2", "G2", "G3+"], A_AGE=[30]*4,
        arrival_age=[25.]*4, sex=["male"]*4, earn=[400., 100., 300., 500.], pw=[1., 1., 2., 3.]))
    completed = counted.assign(pw_counted=counted.pw, pw=[1., 10., 2., 7.])
    def money(people, *args):
        cash = people.earn.to_numpy() * np.where(people.earn.eq(100.), .5, .1)
        out = {name: cash * .01 for name in G.MONEY}
        out.update(cash=cash, formal=cash * .5)
        return out
    monkeypatch.setattr(G, "mexico_rearing", money)
    monkeypatch.setattr(G, "mexico_own_schooling", money)
    monkeypatch.setattr(G, "summarize", lambda gen, conv, people, e, delta, extra:
                        dict(generation=gen, convention=conv, **extra))
    monkeypatch.setattr(G.MC, "upper_arrays", lambda m, profile:
                        {name: profile[f"upper_{name}"].to_numpy() for name in G.MONEY})
    monkeypatch.setattr(B.MX, "ppp", lambda: {"PA.NUS.PPP": 10., "PA.NUS.PRVT.PP": 12.})
    cells = {"gdp": {}, "consumption": {}}
    a = B.premium_table(counted, None, None, cells).attrs["g3_pay_profiles"]
    b = B.premium_table(completed, None, None, cells).attrs["g3_pay_profiles"]
    pd.testing.assert_frame_equal(a.drop(columns="pw"), b.drop(columns="pw"))
    np.testing.assert_array_equal(a.pw, [3., 3.])
    np.testing.assert_array_equal(b.pw, [7., 7.])
    assert a.upper_cash.iloc[0] == pytest.approx(500. * (50. + 2.*30.) / (100. + 2.*300.))
    pd.testing.assert_series_equal(G.counted_donor_weights(completed), completed.pw_counted)
