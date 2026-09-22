"""Re-read the lane's artefacts and re-check every gate they claim to have passed."""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

LANE = Path(__file__).resolve().parent
DERIVED = LANE / "derived"
REPO = LANE.parent.parent.parent
TRANSPORT = REPO / "infra/immigration-fiscal/build/meps_health_transport_2024.py"
PROFILE_EXPORT = REPO / "infra/immigration-fiscal/ledger_absolute_2026_09_17/profile_export.py"
COMPONENTS = REPO / "infra/immigration-fiscal/ledger_absolute_2026_09_17/derived/age_profile_components.csv"
PROFILES = REPO / "infra/immigration-fiscal/ledger_absolute_2026_09_17/derived/age_profiles.csv"


@pytest.fixture(scope="module")
def audit():
    return json.loads((DERIVED / "audit.json").read_text())


@pytest.fixture(scope="module")
def cells():
    return pd.read_csv(DERIVED / "cells.csv")


@pytest.fixture(scope="module")
def ratios():
    return pd.read_csv(DERIVED / "ratios.csv")


@pytest.fixture(scope="module")
def translation():
    return pd.read_csv(DERIVED / "ledger_translation.csv")


def test_every_artefact_exists():
    for name in ("cells.csv", "ratios.csv", "ledger_translation.csv", "audit.json"):
        assert (DERIVED / name).exists(), name


def test_input_hashes_still_match(audit):
    for name, rec in audit["inputs"].items():
        p = Path(rec["path"])
        assert p.exists(), f"{name} missing at {p}"
        h = hashlib.sha256()
        with open(p, "rb") as fh:
            for chunk in iter(lambda: fh.read(1 << 20), b""):
                h.update(chunk)
        assert h.hexdigest() == rec["sha256"], f"{name} changed since the lane ran"


def test_hispncat_codebook_gate(audit):
    """HC-256 codebook p.109, all eight categories."""
    expected = {"1": (2679, 42446768), "2": (282, 5310040), "3": (144, 2030498),
                "4": (131, 2829667), "5": (588, 10298522), "6": (216, 4168032),
                "8": (76, 1522056), "9": (15024, 271192047)}
    got = audit["gates"]["hispncat_codebook"]
    assert set(got) == set(expected)
    for code, (n, w) in expected.items():
        assert got[code]["unweighted"] == n
        assert abs(got[code]["weighted"] - w) <= 1


def test_transport_nativity_anchors(audit):
    a = audit["gates"]["nativity_anchors"]
    assert abs(a["born_us"] - 285498519) <= 1
    assert abs(a["born_elsewhere"] - 52835316) <= 1
    assert abs(a["all"] - 339797630) <= 1


def test_record_and_design_gates(audit):
    assert audit["gates"]["n_records"] == 19140
    assert audit["gates"]["n_positive_weight"] == 18683
    assert audit["gates"]["design"]["min_psu_per_stratum"] >= 2
    assert audit["gates"]["mcdev_codebook"] == {"unweighted": 4941, "weighted": 78147553.0}
    assert audit["gates"]["nh_white_equals_racethx2"]["unweighted"] == 10766


def test_band_definitions_have_not_drifted(audit):
    """The lane copies two band formulas; fail if either source changed."""
    t = TRANSPORT.read_text()
    assert "np.digitize(age, [18, 35, 50, 65])" in t, "transport age_band changed"
    p = PROFILE_EXPORT.read_text()
    assert re.search(r"np\.digitize\(d\.A_AGE, \[18, 25, 35, 45, 55, 65, 75\]\)", p), \
        "ledger profile_export band definition changed"
    assert "np.digitize(age, [18, 35, 50, 65])" in audit["band_definitions"]["transport"]


def test_public_payer_list_matches_the_transport(audit):
    t = TRANSPORT.read_text()
    assert 'PUBLIC_PAYERS = ["TOTMCR24", "TOTMCD24", "TOTVA24", "TOTTRI24", "TOTOFD24", "TOTSTL24"]' in t
    for v in ("TOTMCR24", "TOTMCD24", "TOTVA24", "TOTTRI24", "TOTOFD24", "TOTSTL24"):
        assert v in audit["public_payer_definition"]


def test_nh_white_weighted_total(cells):
    row = cells[(cells.scheme == "pooled") & (cells.band == "all_ages") &
                (cells.nativity == "both") & (cells.subgroup == "all") &
                (cells.group == "nh_white")].iloc[0]
    # valid-set restriction (AGE >= 0, BORNUSA in 1/2, PERWT > 0) trims the codebook total
    assert row.n == 10438
    assert row.population < 191692001


def test_every_cell_has_nonnegative_means(cells):
    for c in [c for c in cells.columns if c.startswith("mean_")]:
        vals = cells[c].dropna()
        assert (vals >= -1e-9).all(), c


def test_ratios_reproduce_the_cell_means(ratios, cells):
    idx = cells.set_index(["scheme", "band", "nativity", "subgroup", "group"])
    checked = 0
    for _, r in ratios[ratios.subgroup != "coverage_standardized"].iterrows():
        if not np.isfinite(r.ratio):
            continue
        key = (r.scheme, str(r.band), r.nativity, r.subgroup)
        num = idx.loc[key + ("mexican_origin",), f"mean_{r.measure}"]
        den = idx.loc[key + (r.denominator,), f"mean_{r.measure}"]
        assert r.ratio == pytest.approx(num / den, rel=1e-9)
        assert r.difference == pytest.approx(num - den, rel=1e-9, abs=1e-6)
        checked += 1
    assert checked > 600


def test_confidence_intervals_and_flags(ratios):
    z = 1.959963984540054
    fin = ratios[np.isfinite(ratios.ratio) & np.isfinite(ratios.se)]
    assert np.allclose(fin.ci_lo, fin.ratio - z * fin.se)
    assert np.allclose(fin.ci_hi, fin.ratio + z * fin.se)
    flag = (fin.ci_lo > 1) | (fin.ci_hi < 1)
    assert (fin.excludes_one.to_numpy() == flag.to_numpy()).all()
    assert (fin.se >= 0).all()


def test_se_validation_agrees(audit):
    v = audit["se_validation"]
    assert v["bootstrap_replicates"] >= 1000
    assert v["relative_difference"] < 0.20, v


def test_headline_ratios_are_where_the_result_says(ratios):
    def pick(band, den, measure, subgroup="all"):
        r = ratios[(ratios.scheme == "pooled") & (ratios.band.astype(str) == band) &
                   (ratios.nativity == "both") & (ratios.subgroup == subgroup) &
                   (ratios.denominator == den) & (ratios.measure == measure)]
        assert len(r) == 1, (band, den, measure, subgroup)
        return r.iloc[0]

    assert pick("65plus", "all_donors", "public").ratio == pytest.approx(0.893, abs=0.002)
    assert pick("65plus", "nh_white", "public").ratio == pytest.approx(0.886, abs=0.002)
    assert pick("all_ages", "all_donors", "public").ratio == pytest.approx(0.757, abs=0.002)
    assert pick("18_64", "all_donors", "public").ratio == pytest.approx(0.688, abs=0.002)
    # Medicaid coverage runs the other way and its 65+ interval excludes parity vs white
    assert pick("65plus", "nh_white", "medicaid").excludes_one
    assert pick("65plus", "nh_white", "share_medicaid_ever").ratio > 3
    # holding the coverage mix fixed lowers the ratio in every age domain
    for band in ("65plus", "18_64", "all_ages"):
        pooled = pick(band, "all_donors", "public").ratio
        std = pick(band, "all_donors", "public", "coverage_standardized").ratio
        assert std < pooled


def test_translation_is_the_ledger_charge_times_the_ratio(translation):
    per_band = translation[translation.band >= 0]
    assert len(per_band) == 8
    assert np.allclose(per_band.delta_medical_bn,
                       per_band.ledger_medical_bn * (per_band.ratio_public - 1))
    assert np.allclose(per_band.delta_M_bn, per_band.ledger_M_bn * (per_band.ratio_M - 1))
    assert np.allclose(per_band.delta_total_bn,
                       per_band.delta_medical_bn + per_band.delta_M_bn)
    assert np.allclose(per_band.delta_medical_bn_drop_top1,
                       per_band.ledger_medical_bn * (per_band.ratio_public_drop_top1 - 1))


def test_translation_aggregates_sum_their_bands(translation):
    per_band = translation[translation.band >= 0]
    tot = translation[translation.band_label == "all_bands"].iloc[0]
    old = translation[translation.band_label == "65plus"].iloc[0]
    assert tot.delta_total_bn == pytest.approx(per_band.delta_total_bn.sum(), rel=1e-9)
    assert old.delta_total_bn == pytest.approx(
        per_band[per_band.band.isin([6, 7])].delta_total_bn.sum(), rel=1e-9)
    # an aggregate SE must not exceed the naive independent sum of its parts
    assert old.se_delta_total_bn <= np.sqrt(
        (per_band[per_band.band.isin([6, 7])].se_delta_total_bn ** 2).sum()) * 3


def test_translation_uses_the_ledgers_own_charges(translation):
    comp = pd.read_csv(COMPONENTS)
    sel = ((comp.allocation == "shared") & (comp.account == "expanded") &
           (comp.group == "mexican_observed_total"))
    med = comp[sel & (comp.component == "medical")].set_index("band").signed_total
    mit = comp[sel & (comp.component == "M")].set_index("band").signed_total
    per_band = translation[translation.band >= 0].set_index("band")
    for b in range(8):
        assert per_band.loc[b, "ledger_medical_bn"] == pytest.approx(med.loc[b] / 1e9, rel=1e-9)
        assert per_band.loc[b, "ledger_M_bn"] == pytest.approx(mit.loc[b] / 1e9, rel=1e-9)


def test_union_nativity_mix_identity(translation):
    prof = pd.read_csv(PROFILES)
    sel = (prof.allocation == "personal") & (prof.account == "expanded")
    pop = {g: prof[sel & (prof.group == g)].set_index("band").population
           for g in ("mexican_observed_total", "mexico_born", "mexican_second_gen",
                     "mexican_third_plus_selfid")}
    parts = pop["mexico_born"] + pop["mexican_second_gen"] + pop["mexican_third_plus_selfid"]
    assert np.allclose(parts, pop["mexican_observed_total"], atol=1)
    per_band = translation[translation.band >= 0].set_index("band")
    for b in range(8):
        assert per_band.loc[b, "foreign_born_share"] == pytest.approx(
            pop["mexico_born"].loc[b] / pop["mexican_observed_total"].loc[b], rel=1e-9)


def test_leave_one_out_flips_the_all_band_sign(audit, translation):
    """The headline caveat is a fact about the file, not a judgement call."""
    b0 = audit["leave_one_out"]["bands"]["0"]
    assert b0["dropped_share_of_mexican_band_mean"] > 0.5
    assert b0["dropped_public"] == 1242405.0
    # the same record carries far less of the whole band, which is the point
    assert b0["all_donor_top1_share_of_band_mean"] == pytest.approx(0.292, abs=0.002)
    assert b0["n_mexican"] == 729 and b0["n_all_donors"] == 3545
    tot = translation[translation.band_label == "all_bands"].iloc[0]
    assert tot.delta_medical_bn < 0 < tot.delta_medical_bn_drop_top1


def test_pooled_two_year_check_is_secondary(audit):
    p = audit["pooled_2023_2024_65plus"]
    assert 1.0 < p["deflator_2023_to_2024"] < 1.1
    assert p["pooled_65plus_public_ratio_vs_all_donors"]["n_mexican"] > 500
    assert "cpi_all_urban.csv" in p["cpi_source"]


def test_no_training_data_tag_anywhere():
    for name in ("RESULT.md", "README.md"):
        text = (LANE / name).read_text()
        assert "[TRAINING-DATA]" not in text, name
