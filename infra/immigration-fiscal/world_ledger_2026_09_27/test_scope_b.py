"""Scope B is a partial group beside complete-lineage other residents."""
import copy

import pandas as pd
import pytest

import scope_b as S


def fixture():
    specs = pd.DataFrame([dict(end=e, cost_bn=10., A_bn=-15., P_bn=2., F_bn=3.)
                          for e in ("low", "high")]).set_index("end")
    ch = pd.DataFrame(dict(bn_low=[-10., -11., -1., 2.], bn_high=[-10., -11., -1., 2.],
                          bn_central=[-10., -11., -1., 2.]),
                      index=["main_case", "fiscal", "displaced_beneficiaries", "wages"])
    v = pd.DataFrame([dict(end=e, line=line, origin_line=line, net_cost_bn=value)
                      for e in ("low", "high") for line, value in (("counted", 12.5), ("coverage_tax", 2.5))])
    return dict(case="oct15", basis="oct15", pension_basis="matched_cash", specs=specs,
        ch=ch, val=v, vgen=v, gen=pd.DataFrame(dict(population=[100.], cost_bn=[10.])),
        pos=pd.DataFrame(dict(party=["G1"], mean_g=[2.], counted_mean_g=[1.], persons_m=[3.], counted_persons_m=[2.])),
        capital_projected_gen_industry_wages={"stale": True})


def test_partial_group_retains_complete_lineage_other_account():
    I = fixture()
    old = copy.deepcopy(I)
    out = S.partial_group(I)
    assert not out["vgen"].origin_line.str.startswith("coverage_").any()
    for name in ("specs", "ch", "val", "gen"):
        pd.testing.assert_frame_equal(out[name], old[name])
        pd.testing.assert_frame_equal(I[name], old[name])
    assert out["scope_enters_total"] is False
    assert out["world_total_status"].startswith("[NOT DEFINED]")


def test_partial_group_requires_source_identity():
    I = fixture()
    I["vgen"] = I["vgen"].drop(columns="origin_line")
    with pytest.raises(SystemExit, match="source identity"):
        S.partial_group(I)


def test_build_drops_donor_columns_and_recomputes_only_group_inputs(monkeypatch):
    I = fixture()
    d = pd.DataFrame(dict(pw=[15., 25.], pw_counted=[10., 20.], coverage_pw=[5., 5.]))
    monkeypatch.setattr(S, "economic_inputs", lambda obj, frame: {"recomputed_on": float(frame.pw.sum())})
    seen = []
    def shapes(obj):
        assert "capital_projected_gen_industry_wages" not in obj
        seen.append(obj["capital_people"].pw.sum())
        return {"fresh": True}
    monkeypatch.setattr(S.K, "projected_shapes", shapes)
    out, counted = S.build(I, d)
    assert counted.pw.tolist() == [10., 20.]
    assert "pw_counted" not in counted and "coverage_pw" not in counted
    assert out["pos"].mean_g.item() == 1.
    assert out["pos"].persons_m.item() == 2.
    assert out["capital_projected_gen_industry_wages"] == {"fresh": True}
    assert seen == [30.]
    assert d.pw.tolist() == [15., 25.]
    for name in ("specs", "ch", "val", "gen"):
        pd.testing.assert_frame_equal(out[name], I[name])
