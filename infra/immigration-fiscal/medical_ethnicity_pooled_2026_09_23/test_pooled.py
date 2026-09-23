"""Re-read the lane's artefacts and re-check the gates and identities they claim."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

LANE = Path(__file__).resolve().parent
DERIVED = LANE / "derived"
Z = 1.959963984540054


def sha(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


@pytest.fixture(scope="module")
def ratios():
    return pd.read_csv(DERIVED / "ratios.csv")


@pytest.fixture(scope="module")
def cells():
    return pd.read_csv(DERIVED / "cells.csv")


def test_every_artefact_exists():
    for name in ["inputs_manifest.json", "gates_by_year.csv", "pool_audit.json", "cells.csv", "ratios.csv",
                 "two_part.csv", "by_year.csv", "year_heterogeneity.csv", "mcbs_reconciliation.csv",
                 "standardized.csv", "disconfirmation.csv", "winsor_caps.csv", "ratios_audit.json",
                 "cps_cells.csv", "translation_ledger.csv", "translation_account.csv",
                 "translation_by_year.csv", "translation_audit.json", "bounds.csv", "bounds_audit.json",
                 "cbo_emergency_medicaid_table1.csv", "coverage_vs_dollars.csv", "se_validation.csv"]:
        assert (DERIVED / name).exists(), name


@pytest.mark.parametrize("audit", ["pool_audit.json", "translation_audit.json", "bounds_audit.json"])
def test_input_hashes_still_match(audit):
    for name, rec in json.loads((DERIVED / audit).read_text())["inputs"].items():
        p = Path(rec["path"])
        assert p.exists(), f"{name} missing at {p}"
        assert sha(p) == rec["sha256"], f"{name} changed since the lane ran"


def test_manifest_pins_all_nine_years_and_hc036():
    m = json.loads((DERIVED / "inputs_manifest.json").read_text())
    years = {r["year"] for r in m if r["year"] is not None}
    assert years == set(range(2016, 2025))
    assert any(r["file"] == "h36u24dat.zip" for r in m)
    for r in m:
        assert len(r["sha256"]) == 64 and r["bytes"] > 0


def test_year_gates():
    g = pd.read_csv(DERIVED / "gates_by_year.csv")
    assert list(g.year) == list(range(2016, 2025))
    assert g.mexican_label.str.contains("MEXICAN").all()
    assert (g.totexp_identity_max_abs_residual <= 5).all()
    assert (g.opu_share_of_medicaid[g.year >= 2019] == 0).all()
    assert (g.opu_share_of_medicaid[g.year <= 2018] > 0).all()
    a = json.loads((DERIVED / "pool_audit.json").read_text())
    assert a["pooled_design"]["min_psu_per_stratum"] >= 2


def test_reproduction_gates():
    a = json.loads((DERIVED / "ratios_audit.json").read_text())
    g = a["gate_2024"]
    assert g["rows_checked"] >= 45
    assert g["max_abs_diff_ratio"] < 1e-9 and g["max_abs_diff_se"] < 1e-9
    assert g["headline"]["18_64"]["ratio"] == pytest.approx(0.688, abs=0.0005)
    assert g["headline"]["65plus"]["ratio"] == pytest.approx(0.893, abs=0.0005)
    b = a["gate_2023_2024"]
    assert b["ratio"] == pytest.approx(b["published"]["ratio"], abs=1e-9)


def test_ratios_reproduce_cell_means(ratios, cells):
    idx = cells.set_index(["sample", "spec", "scheme", "band", "nativity", "group", "measure"])
    sub = ratios[(ratios["sample"] == "pooled_2016_2024") & (ratios.comparison == "mexican_origin/all_donors")
                 & ratios.measure.isin(cells.measure.unique())]
    checked = 0
    for _, r in sub.sample(400, random_state=1).iterrows():
        if not np.isfinite(r.ratio):
            continue
        k = (r["sample"], r.spec, r.scheme, r.band, r.nativity)
        num = idx.loc[k + ("mexican_origin", r.measure), "mean"]
        den = idx.loc[k + ("all_donors", r.measure), "mean"]
        assert r.ratio == pytest.approx(num / den, rel=1e-9)
        checked += 1
    assert checked > 300


def test_confidence_intervals(ratios):
    f = ratios[np.isfinite(ratios.ratio) & np.isfinite(ratios.se)]
    assert np.allclose(f.ci_lo, f.ratio - Z * f.se)
    assert np.allclose(f.ci_hi, f.ratio + Z * f.se)


def test_two_part_arithmetic_is_the_plain_ratio(ratios):
    tp = pd.read_csv(DERIVED / "two_part.csv")
    a = tp[tp.component == "two_part_arithmetic"].set_index(["scheme", "band", "nativity", "measure"]).ratio
    p = ratios[(ratios["sample"] == "pooled_2016_2024") & (ratios.spec == "plain")
               & (ratios.comparison == "mexican_origin/all_donors")].set_index(
        ["scheme", "band", "nativity", "measure"]).ratio
    j = pd.concat([a.rename("tp"), p.rename("plain")], axis=1, join="inner").dropna()
    assert len(j) > 50
    assert np.allclose(j.tp, j.plain, rtol=1e-9)


def test_headline_ratios(ratios):
    def pick(band, spec="plain"):
        r = ratios[(ratios["sample"] == "pooled_2016_2024") & (ratios.spec == spec) & (ratios.scheme == "age_domain")
                   & (ratios.band == band) & (ratios.nativity == "both")
                   & (ratios.comparison == "mexican_origin/all_donors") & (ratios.measure == "public")]
        assert len(r) == 1
        return r.iloc[0]
    assert pick("65plus").ratio == pytest.approx(0.848, abs=0.001)
    assert pick("18_64").ratio == pytest.approx(0.671, abs=0.001)
    assert pick("under18").ratio == pytest.approx(1.367, abs=0.001)
    assert pick("under18", "winsor_p995").ratio == pytest.approx(1.154, abs=0.001)
    assert pick("65plus").ci_hi < 1 and pick("18_64").ci_hi < 1
    assert pick("under18", "winsor_p995").ci_lo > 1


def test_translation_identities():
    a = pd.read_csv(DERIVED / "translation_account.csv")
    lines = a[a.line != "all five medical lines"]
    assert np.allclose(lines.delta_bn, lines.account_target_bn * (lines.key_weighted_ratio - 1))
    for spec, g in a.groupby("spec"):
        tot = g[g.line == "all five medical lines"]
        if len(tot):
            assert tot.delta_bn.iloc[0] == pytest.approx(g[g.line != "all five medical lines"].delta_bn.sum(), rel=1e-9)
    med = a[(a.spec == "plain") & (a.line == "medicaid_and_chip_other_medical")].iloc[0]
    assert med.account_target_bn == pytest.approx(116.91, abs=0.005)
    led = pd.read_csv(DERIVED / "translation_ledger.csv")
    for (spec, age, nat), g in led.groupby(["spec", "age_group", "nativity"]):
        g = g.set_index("component")
        assert g.loc["medical+M", "delta_cost_bn"] == pytest.approx(
            g.loc["medical", "delta_cost_bn"] + g.loc["M", "delta_cost_bn"], rel=1e-9, abs=1e-12)
    base = led[(led.spec == "plain") & (led.age_group == "all ages") & (led.nativity == "both")].set_index("component")
    assert base.loc["medical", "ledger_cost_bn"] == pytest.approx(92.877683, abs=1e-5)
    assert base.loc["M", "ledger_cost_bn"] == pytest.approx(35.150381, abs=1e-5)


ACCOUNT = LANE.parent / "full_account_spending_2026_09_20/derived"


def test_translation_matches_the_account_files():
    a = json.loads((DERIVED / "translation_audit.json").read_text())
    assert a["gates"]["ledger_band_worst_abs_residual_usd"] <= 1.0
    ik = pd.read_csv(ACCOUNT / "incidence_keys.csv")
    ik = ik[ik.allocation == "personal"].set_index("key")
    for key, rec in a["gates"]["account_keys"].items():
        assert rec["target"] == pytest.approx(ik.loc[key, "target_key_total"], rel=1e-9), key
        assert rec["national"] == pytest.approx(ik.loc[key, "national_key_total"], rel=1e-9), key
    al = pd.read_csv(ACCOUNT / "allocations.csv")
    al = al[(al.scenario_id == "complete_preferred_F_per_capita") & (al.allocation == "personal")].set_index("category")
    ta = pd.read_csv(DERIVED / "translation_account.csv")
    for line, bn in a["account_lines_bn"].items():
        assert bn == pytest.approx(al.loc[line, "target_bn"], rel=1e-12), line
        assert (ta[ta.line == line].account_target_bn == bn).all(), line


def test_se_validation():
    v = pd.read_csv(DERIVED / "se_validation.csv")
    assert len(v) == 3
    assert (v.relative_difference < 0.25).all()
    assert (v.replicates >= 1000).all()


def test_bounds():
    cbo = pd.read_csv(DERIVED / "cbo_emergency_medicaid_table1.csv")
    assert int(cbo.total_m.sum()) == 26554
    assert int(cbo[cbo.fiscal_year == 2023].total_m.iloc[0]) == 3775
    b = pd.read_csv(DERIVED / "bounds.csv")
    nf = b[b.check == "nursing_facility"].set_index("quantity").value
    al = pd.read_csv(ACCOUNT / "allocations.csv")
    line = al[(al.scenario_id == "complete_preferred_F_per_capita") & (al.allocation == "personal")
              & (al.category == "medicaid_and_chip_other_medical")].iloc[0]
    charged = nf["account charge to the union of nursing-facility Medicaid"]
    assert charged == pytest.approx(68.8 * line.target_bn / line.national_bn, rel=1e-12)
    for lab in ("union share = its share of the 65+ institutional population (a ceiling)",
                "union share doubled, allowing for under-65 residents"):
        assert nf[f"account over-charge, {lab}"] == pytest.approx(charged - nf[f"use-based charge, {lab}"], rel=1e-12)
    share = (nf["union persons 65+ in institutional group quarters, ACS 2024"]
             / nf["all natives + Mexico-born 65+ in institutional group quarters, ACS 2024"])
    assert nf["use-based charge, union share = its share of the 65+ institutional population (a ceiling)"] == \
        pytest.approx(68.8 * share, rel=1e-12)
    # combined rows: Medicaid line = (line - charged) x ratio + use-based - line; five lines add the other four
    ta = pd.read_csv(DERIVED / "translation_account.csv")
    comb = b[b.check == "medicaid_line_combined"].set_index("quantity").value
    five = b[b.check == "medical_lines_combined"].set_index("quantity").value
    for spec in ("plain", "winsor_p995", "two_part_lognormal"):
        t = ta[ta.spec == spec].set_index("line")
        f = t.loc["medicaid_and_chip_other_medical", "key_weighted_ratio"]
        use = nf["use-based charge, union share = its share of the 65+ institutional population (a ceiling)"]
        want = (line.target_bn - charged) * f + use - line.target_bn
        got = comb[f"{spec}, nursing facility at share ceiling: change in the $116.91bn line"]
        assert got == pytest.approx(want, rel=1e-12)
        others = t.drop(index=["medicaid_and_chip_other_medical", "all five medical lines"]).delta_bn.sum()
        assert five[f"{spec}, nursing facility at share ceiling: change in all five medical lines ($207.43bn)"] == \
            pytest.approx(want + others, rel=1e-9)


def test_no_training_data_tag():
    for name in ("RESULT.md", "README.md"):
        p = LANE / name
        if p.exists():
            assert "[TRAINING-DATA]" not in p.read_text(), name
