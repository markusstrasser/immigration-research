"""Raw ownership cannot use a headcount proxy or conceal undefined drivers."""
import json
from pathlib import Path

import numpy as np
import pytest

from reporter_b_routes import atomic_json_write, component_shares


def test_atomic_publication_preserves_previous_file_until_budget_passes(tmp_path, monkeypatch):
    target = tmp_path / "routes.json"
    target.write_text("previous\n")
    actual_dump = json.dump

    def inspecting_dump(*args, **kwargs):
        assert target.read_text() == "previous\n"
        return actual_dump(*args, **kwargs)

    monkeypatch.setattr(json, "dump", inspecting_dump)

    def blocked():
        raise SystemExit("[BLOCKED] budget regression")

    with pytest.raises(SystemExit, match="budget regression"):
        atomic_json_write(target, {"new": True}, blocked)
    assert target.read_text() == "previous\n"
    assert list(tmp_path.iterdir()) == [target]
    atomic_json_write(target, {"new": True}, lambda: 123)
    assert target.read_text() == '{"new":true}\n'


def test_actual_driver_weights_and_signed_composites():
    weights = np.tile(np.array([[2.0], [3.0], [5.0]]), (1, 161))
    weights[:, 1] = [4, 2, 1]
    omega = np.eye(3)
    x, y = np.array([1.0, 5.0, 9.0]), np.array([7.0, 2.0, 1.0])
    got, zero = component_shares([(1.25, x), (-0.25, y)], weights, omega, -2.3)
    expected = 1.25*x[:, None]*weights/(x @ weights) - 0.25*y[:, None]*weights/(y @ weights)
    assert np.allclose(got, expected, atol=1e-15, rtol=0)
    assert not zero
    assert not np.allclose(got[:, 0], weights[:, 0]/weights[:, 0].sum())


def test_nonzero_raw_part_with_zero_reporter_mass_blocks():
    weights = np.ones((3, 161))
    with pytest.raises(SystemExit, match="nonzero raw part has a zero driver mass"):
        component_shares([(1.0, np.zeros(3))], weights, np.eye(3), 0.01)
    shares, zero = component_shares([(1.0, np.zeros(3))], weights, np.eye(3), 0)
    assert zero and np.array_equal(shares[2], np.ones(161))


def test_incorrect_record_parent_partition_blocks():
    with pytest.raises(SystemExit, match="omega does not partition"):
        component_shares([(1.0, np.ones(3))], np.ones((3, 161)), np.eye(3)*0.9, 1)


def test_published_inventory_and_record_reconstruction():
    here = Path(__file__).resolve().parent
    artifact = json.loads((here / "derived/reporter_b_routes.json").read_text())
    source = json.loads((here / "derived/reporter_b_inputs.json").read_text())
    assert not any(path.endswith(".pyc") for path in artifact["source_sha256"])
    weights = np.array([r["replicate_weights"] for r in artifact["reporters"]])
    omega = np.array([r["omega_b"] for r in artifact["reporters"]])
    for basis in ("set", "cash"):
        routes = artifact["sets"][basis]["routes"]
        assert len(routes) == 339 and set(routes) == set(source["sets"][basis]["parts"])
        modeled = {name for name, route in routes.items()
                   if route["allocations"]["personal"]["ownership"]["kind"] == "modeled_source_anchor"}
        assert modeled == {f"union_G3plus:{line}:veterans" for line in
                           ("health_services", "military_medical", "veterans_other", "other_state_benefits")}
        assert all(route["allocations"]["shared"]["ownership"]["kind"] == "actual_selected_raw_driver"
                   for route in routes.values())
        for name, route in routes.items():
            for key in ("route_id", "part_edit", "global_edit", "cell", "by", "carrier", "selector"):
                assert route[key] == source["sets"][basis]["parts"][name][key]
            for allocation, raw in route["allocations"].items():
                if raw["zero_quantity_ownership"]:
                    assert route["by"][allocation] == 0
                    expected = np.tile([[0], [0], [1]], (1, 161))
                else:
                    components = [(c["raw_share"], np.array(artifact["driver_pool"][c["driver_id"]]["values"])) for c in raw["components"]]
                    expected, zero = component_shares(components, weights, omega, route["by"][allocation])
                    assert not zero
                shares = np.array([raw["generation_shares"][g] for g in ("G1", "G2", "G3plus")])
                costs = np.array([raw["by_generation_bn"][g] for g in ("G1", "G2", "G3plus")])
                assert np.max(np.abs(shares-expected)) < 1e-12
                assert np.max(np.abs(costs-shares*route["by"][allocation])) < 1e-9
