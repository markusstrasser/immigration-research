"""Pension owner/basis contracts and exact pinned historical cash closure."""
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import subprocess

import pandas as pd
import pytest

import mexico_pensions as M
import mexico_compensation as MC
import pension_cash as P
import world_ledger as W

HERE = Path(__file__).resolve().parent


def historical_inputs():
    artifact = json.loads((HERE / "inputs/pension_cash_cells_v7.json").read_text())
    raw = artifact["results"]["set"]
    glines, vgen, val = P._value("oct14", raw)
    specs = pd.DataFrame(raw["specs"]).set_index("band_end")
    # The committed world tables are the independent current-value control,
    # not a synthetic approximation or a regenerated historical output.
    pins = json.loads((HERE / "pins.json").read_text())["oct14"]
    ch = W.pinned_csv(pins["winners"], pins["dirs"]["winners"] + "/channels.csv").set_index("id")
    gen = pd.read_csv(__import__("io").StringIO(raw["generation_results_csv"]))
    return dict(case="oct14", glines=glines, vgen=vgen, val=val, specs=specs, gen=gen, ch=ch,
                mxb=pd.read_csv(HERE / "derived/mexico_budget_lineage.csv"))


def test_primary_2024_parameters_reproduce_existing_model():
    import mexico
    fresh = M.primary_parameters()
    old = mexico.employer_parameters()
    assert fresh["ceav_employer_rates"] == pytest.approx(old["ceav_rates"], abs=1e-14, rel=0)
    assert fresh["retiro_employer_rate"] == old["retirement"]
    assert fresh["housing_employer_rate"] == old["housing"]
    assert fresh["uma_daily_mxn"] == old["uma"]
    assert fresh["ceav_employee_rate"] == mexico.AFORE_RATE
    assert len(fresh["cuota_social_daily_mxn"]) == 7
    assert "not annual average" in fresh["cuota_social_vintage"]


def test_primary_bytes_fail_on_stale_source(tmp_path):
    name = "pension_imss_annex_2024_2025.txt"
    manifest = json.loads((HERE / "inputs/pension_primary_pins.json").read_text())
    (tmp_path / "pension_primary_pins.json").write_text(json.dumps(manifest))
    (tmp_path / name).write_bytes((HERE / "inputs" / name).read_bytes() + b"changed")
    with pytest.raises(M.PensionBlocked, match="primary_pin_stale"):
        M.pinned_text(name, tmp_path)
    with pytest.raises(M.PensionBlocked, match="primary_pin_missing"):
        M.pinned_text("unknown.txt", tmp_path)
    (tmp_path / name).unlink()
    with pytest.raises(M.PensionBlocked, match="primary_source_missing"):
        M.pinned_text(name, tmp_path)


def test_payer_does_not_change_ceav_owner_and_government_is_not_member_tax():
    rows = MC.receipt_rows(dict(employee_ceav=2, employer_employee_ceav=3,
        employer_sar=5, employer_housing=7, employer_health_cash=11,
        government_health_fixed=13, government_cuota_social=17))
    assert {r["receipt_class"] for r in rows if "ceav" in r["component"]} == {"worker_asset"}
    assert {r["owner"] for r in rows if "ceav" in r["component"]} == {"worker"}
    assert sum(float(r["amount_mxn"]) for r in rows if r["member_paid_tax"]) == 11
    assert sum(float(r["amount_mxn"]) for r in rows if r["receipt_class"] == "worker_asset"
               and r["remitter"] != "government") == 17
    assert sum(float(r["amount_mxn"]) for r in rows if r["receipt_class"] == "worker_asset"
               and r["remitter"] == "government") == 17
    assert sum(float(r["amount_mxn"]) for r in rows if r["receipt_class"] == "pooled_public"
               and r["remitter"] == "government") == 13
    with pytest.raises(SystemExit, match="mexico_receipt_component_declared"):
        MC.receipt_rows(dict(unknown=1))


def test_ownership_move_is_conserved_at_arbitrary_weights():
    for deposit in (0, 1, 43):
        eq = M.ownership_delta(deposit)
        assert abs(eq["world"]) <= 1e-6
        assert eq["other_us_residents"] == 0
        for wm, wg in ((1.16, 1), (1, 1.5), (1.7, 1.2)):
            d = M.ownership_delta(deposit, wm, wg)
            assert d["world"] == pytest.approx(wm*d["mexico_residents"]+wg*d["group"], abs=1e-12, rel=0)


def test_missing_accrual_histories_and_mixed_bases_fail():
    with pytest.raises(M.PensionBlocked, match="histories_missing"):
        M.pension_basis("full_accrual", "accrual")
    with pytest.raises(M.PensionBlocked, match="mixed_us_mexico"):
        M.pension_basis("matched_cash", "accrual")
    with pytest.raises(M.PensionBlocked, match="public_funding_unidentified"):
        M.pension_basis("matched_cash", "cash")
    assert M.net_public_service_cost(100, 30, 7) == 77


def test_exact_cash_adapter_closes_and_preserves_input():
    original = historical_inputs()
    before = deepcopy(original)
    cash = P.adapt_cash(original)
    for name in ("glines", "vgen", "val", "specs", "gen", "ch", "mxb"):
        pd.testing.assert_frame_equal(original[name], before[name])
    oracle = cash["pension_meta"]["cash_oracle_bn"]
    for i, end in enumerate(("low", "high")):
        assert cash["specs"].loc[end, "cost_bn"] == pytest.approx(oracle[i], abs=1e-6, rel=0)
        gen = cash["gen"][cash["gen"].convention.eq("a") & cash["gen"].band_end.eq(end)]
        assert gen.cost_bn.sum() == pytest.approx(oracle[i], abs=1e-6, rel=0)
        assert cash["ch"].loc[["fiscal", "displaced_beneficiaries", "wages"], f"bn_{end}"].sum() == pytest.approx(-oracle[i], abs=1e-6, rel=0)
        set_value = original["val"][original["val"].end.eq(end)].set_index(["side", "line"]).net_cost_bn
        cash_value = cash["val"][cash["val"].end.eq(end)].set_index(["side", "line"]).net_cost_bn
        changed = (cash_value-set_value).abs()
        assert {k[1] for k in changed[changed > 1e-6].index} == {"social_security", "medicare", "federal_income_tax"}
    assert W.generation_split_check(cash, "oct14").difference_bn.abs().max() <= 1e-6
    assert "future_pension_accrual" not in cash["ch"].index
    assert cash["pension_meta"]["status"].startswith("[DEGRADED]")
    private = P.private_cash_inputs(cash)
    assert all(x["earned_pension_addon_bn"] == 0 and x["social_security_cash_bn"] > 0 for x in private.values())


def test_p032_source_funding_share_preserves_recipient_value():
    original = historical_inputs()
    full = P.adapt_cash(original)
    for share in (0, .5, 1):
        cash = P.adapt_cash(original, public_pension_share=share)
        mask = cash["mxb"].item.str.contains("pensions paid", regex=False)
        assert cash["mxb"].loc[mask, "fiscal_bn"].sum() == pytest.approx(share*full["mxb"].loc[mask, "bn"].sum(), abs=1e-9, rel=0)
        pd.testing.assert_series_equal(cash["mxb"].recipient_bn, full["mxb"].recipient_bn)
    for share in (-.01, 1.01, float("nan")):
        with pytest.raises(M.PensionBlocked, match="share_outside_bound"):
            P.adapt_cash(original, public_pension_share=share)


def test_oct15_has_no_silent_v7_fallback():
    original = historical_inputs()
    original["case"] = "future_unpinned"
    with pytest.raises(M.PensionBlocked, match="source_artifact_missing"):
        P.adapt_cash(original)
    original["case"] = "oct15"
    with pytest.raises(M.PensionBlocked, match="source_artifact_case_mismatch"):
        P.adapt_cash(original, artifact_key="oct14_cash")


def test_cash_source_hash_fails_before_reconstruction(tmp_path):
    source = HERE / "inputs/pension_cash_cells_v7.json"
    stale = tmp_path / source.name
    stale.write_bytes(source.read_bytes() + b"changed")
    with pytest.raises(M.PensionBlocked, match="source_artifact_stale"):
        P.adapt_cash(dict(case="oct14"), cells_path=stale)


def test_historical_generator_requires_external_output_and_replays(tmp_path):
    script = HERE / "pension_cash_cells.cjs"
    for args, error in (([], "historical-probe"), (["--historical-probe"], "out-dir"),
                        (["--historical-probe", "--out-dir", str(HERE / "derived")], "outside the repository")):
        r = subprocess.run(["node", str(script), *args], capture_output=True, text=True)
        assert r.returncode != 0 and error in r.stderr
    r = subprocess.run(["node", str(script), "--historical-probe", "--out-dir", str(tmp_path)],
                       capture_output=True, text=True)
    assert r.returncode == 0, r.stderr
    assert json.loads(r.stdout)["verdict"] == "PASS"
    pinned = HERE / "inputs/pension_cash_cells_v7.json"
    assert hashlib.sha256((tmp_path / "pension-cash-cells.json").read_bytes()).digest() == hashlib.sha256(pinned.read_bytes()).digest()
