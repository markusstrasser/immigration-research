"""Check isolated adjustments against the frozen receipt registry and party conservation."""
import json
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
D = HERE / "derived"


def test_isolated_changes_close_by_party_and_preserve_headline():
    d = pd.read_csv(D / "p7_fix_deltas_oct14.csv")
    assert len(d) == 144
    assert np.isfinite(d.filter(regex="_bn$")).all().all()
    assert (d.headline_change_bn == 0).all()
    for p in ("world_total_bn", "delta_world_total_bn"):
        prefix = "delta_" if p.startswith("delta_") else ""
        parts = sum(d[prefix + x] for x in ("group_total_bn", "other_us_residents_bn", "mexico_residents_bn"))
        assert (d[p] - parts).abs().max() < 1e-6
    assert (d.us_residents_incl_group_bn - d.other_us_residents_bn - d.group_total_bn).abs().max() < 1e-6


def test_source_incidence_delta_matches_registry_at_both_populations():
    d = pd.read_csv(D / "p7_fix_deltas_oct14.csv")
    meta = json.loads((D / "valuation_meta_oct14.json").read_text())["incidence"]["oct14"]
    for r in d[d.fix.eq("fix2_source_incidence")].itertuples():
        key = "source_tax_credit_bn" if r.population_basis == "lineage" else "identified_union_source_tax_credit_bn"
        assert abs(r.delta_group_total_bn - meta[r.account_end][key]) < 1e-6
        assert abs(r.delta_world_total_bn - meta[r.account_end][key]) < 1e-6
        assert r.delta_other_us_residents_bn == 0


def test_child_payer_move_preserves_world_and_keeps_union_term_separate():
    d = pd.read_csv(D / "p7_fix_deltas_oct14.csv")
    meta = json.loads((D / "valuation_meta_oct14.json").read_text())["incidence"]["oct14"]
    for r in d[d.fix.eq("fix12_child_credit_payer")].itertuples():
        key = "child_credit_other_residents_bn" if r.population_basis == "lineage" else "identified_union_child_credit_other_residents_bn"
        assert abs(r.delta_group_total_bn + meta[r.account_end][key]) < 1e-6
        assert abs(r.delta_other_us_residents_bn - meta[r.account_end][key]) < 1e-6
        assert abs(r.delta_world_total_bn) < 1e-6


def test_remittance_conversion_changes_only_mexico_recipient_principal():
    d = pd.read_csv(D / "p7_fix_deltas_oct14.csv")
    r = d[d.fix.str.startswith("fix7_")]
    assert (r.delta_group_total_bn == 0).all()
    assert (r.delta_other_us_residents_bn == 0).all()
    assert (r.delta_world_total_bn - r.delta_mexico_residents_bn).abs().max() < 1e-6
