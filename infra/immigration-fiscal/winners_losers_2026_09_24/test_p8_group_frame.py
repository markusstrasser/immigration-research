"""Group-frame consumer contract and explicit coverage-subset controls."""
from types import SimpleNamespace

import pandas as pd
import pytest

from p8_group_frame import COLUMNS, SPLIT_KIND, build_group_frame, produce_group_frame


def fixture_model():
    rows = []
    for item, kind in [("direct fiscal transfer received: the direct response A, sign flipped", "the group's gain or loss"),
                       *[(f"generation {g}", SPLIT_KIND) for g in ("G1", "G2", "G3plus")],
                       ("victims inside the group, equal footing", "the group's gain or loss"),
                       ("remittances received in Mexico", "the group's gain or loss")]:
        row = dict.fromkeys(COLUMNS, "")
        row.update(item=item, kind=kind, bn_low=1., bn_central=1., bn_high=1., usd_per_member_central=1.)
        rows.append(row)
    source_rows = []
    for convention in ("a", "b"):
        for group, cost in (("G1", 1.), ("G2", 2.), ("G3plus", 3.)):
            for end in ("low", "high"):
                source_rows.append(dict(convention=convention, generation=group, band_end=end, cost_bn=cost, population=20.))
    source = pd.DataFrame(source_rows).to_csv(index=False, lineterminator="\n").encode()
    def gate(name, ok, **detail):
        if not ok:
            raise ValueError(name)
    coverage = dict(counts_by_generation={"G1": 1., "G2": 2., "G3plus": 3.},
                    by_end={end: dict(total_bn=.6, by_generation={"G1": .1, "G2": .2, "G3plus": .3})
                            for end in ("low", "high")})
    payload = dict(meta=dict(population_v8=dict(with_coverage=60., without_coverage=54., coverage=6., completion=2.), coverage=coverage))
    wl = SimpleNamespace(group_frame=lambda *args, **kwargs: (pd.DataFrame(rows)[COLUMNS], {}, {}), gate=gate,
        read_input=lambda key: source, CASE=dict(model="live", gen="pin"), GENERATIONS=[(g, g) for g in ("G1", "G2", "G3plus")])
    return SimpleNamespace(wl=wl, B=None, d=None, I=None, mw=None, payload=payload,
        fin={"live": {"ends": {end: dict(cost_bn=6., A_bn=-9.) for end in ("low", "high")}}},
        source={"v8_social_environment": {"current_social_rows": [dict(item="victims", v8_added_by_end_bn={
            end: dict(completion_receivers_bn=-.2) for end in ("low", "high")})]}})


def test_complete_denominator_and_nonadditive_coverage(tmp_path):
    model = fixture_model()
    table, info = produce_group_frame(model, tmp_path)
    assert list(table.columns) == COLUMNS
    assert table.iloc[0].usd_per_member_central == pytest.approx(9e9 / 60.)
    assert table[table.kind.eq(SPLIT_KIND)].bn_central.sum() == pytest.approx(6.)
    subsets = table[table.kind.eq("coverage decomposition, already included")]
    assert subsets.bn_central.sum() == pytest.approx(.6)
    assert info["complete_members_m"] == 60. / 1e6
    assert len(table[table.item.str.contains("victims inside", regex=False)]) == 1
    assert len(table[table.item.str.contains("remittances received", regex=False)]) == 1
    assert (tmp_path / "group_frame.csv").read_bytes().count(b"\r\n") == 0


def test_coverage_count_cannot_be_hidden_in_a_generation_total():
    model = fixture_model()
    model.payload["meta"]["coverage"]["counts_by_generation"]["G1"] = 10.
    with pytest.raises(ValueError, match="coverage_count"):
        build_group_frame(model)


def test_generation_split_must_close_independently():
    model = fixture_model()
    model.fin["live"]["ends"]["low"]["cost_bn"] = 7.
    with pytest.raises(ValueError, match="generation_closure_low"):
        build_group_frame(model)
