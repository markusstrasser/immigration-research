"""Re-read the written artefacts and check them against the inputs and each other.

Run from the repository root:
    uv run --no-project python3 -m pytest infra/immigration-fiscal/mcbs_elderly_medical_2026_09_22/ -q
"""

from __future__ import annotations

import hashlib
import io
import json
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

import mcbs_elderly as M

LANE = Path(__file__).resolve().parent
DERIVED = LANE / "derived"


@pytest.fixture(scope="module")
def audit() -> dict:
    return json.loads((DERIVED / "audit.json").read_text())


@pytest.fixture(scope="module")
def table() -> pd.DataFrame:
    return pd.read_csv(DERIVED / "elderly_cost_by_race.csv")


@pytest.fixture(scope="module")
def ratios() -> pd.DataFrame:
    return pd.read_csv(DERIVED / "ratios.csv")


@pytest.fixture(scope="module")
def raw() -> pd.DataFrame:
    with zipfile.ZipFile(M.ZIP_PATH) as zf:
        return pd.read_csv(io.BytesIO(zf.read(M.CSV_MEMBER)))


# --- artefacts exist -------------------------------------------------------

def test_all_outputs_written():
    for name in ("elderly_cost_by_race.csv", "ratios.csv", "anchor_reproduction.csv", "audit.json"):
        p = DERIVED / name
        assert p.exists() and p.stat().st_size > 0, f"missing or empty output {p}"


# --- hashes ----------------------------------------------------------------

def test_input_hashes_match_recorded_and_pinned(audit):
    live_zip = M.sha256_file(M.ZIP_PATH)
    assert live_zip == M.EXPECTED_ZIP_SHA256
    assert audit["inputs"]["zip_sha256"] == live_zip
    with zipfile.ZipFile(M.ZIP_PATH) as zf:
        live_csv = hashlib.sha256(zf.read(M.CSV_MEMBER)).hexdigest()
    assert live_csv == M.EXPECTED_CSV_SHA256
    assert audit["inputs"]["csv_sha256"] == live_csv
    assert audit["inputs"]["codebook_sha256"] == M.sha256_file(M.CODEBOOK)


def test_recorded_hashes_agree_with_upstream_validation_json(audit):
    val = json.loads(Path(audit["inputs"]["validation_json"]).read_text())
    assert audit["inputs"]["zip_sha256"] == val["zip_sha256"]
    assert audit["inputs"]["csv_sha256"] == val["csv_sha256"]
    assert audit["inputs"]["codebook_sha256"] == val["codebook_sha256"]


# --- gates -----------------------------------------------------------------

def test_gates_all_passed(audit):
    g = audit["gates"]
    for flag in (
        "zip_sha256_matches_pin",
        "csv_sha256_matches_pin",
        "puf_id_unique",
        "survey_year_2023",
        "race_counts_match_validation_json",
        "cspufwgt_all_positive",
        "payer_amounts_complete",
        "anchor_overall_weighted_matches",
        "anchor_race_totals_match",
        "anchor_exhibit_3_3_matches",
    ):
        assert g[flag] is True, f"gate {flag} not recorded as passed"
    assert g["rows"] == M.N_ROWS == 6920
    assert g["columns"] == M.N_COLS == 134
    assert g["replicate_weights_present"] == 100


def test_gates_fail_loud_on_bad_input(monkeypatch):
    """The gate wall must raise, not warn."""
    df = pd.DataFrame({"PUF_ID": [1, 2], "SURVEYYR": [2023, 2023]})
    with pytest.raises(M.GateFailure):
        M.run_gates(df, {})


def test_race_counts_match_codebook_and_file(raw, audit):
    observed = {int(k): int(v) for k, v in raw["CSP_RACE"].value_counts().items()}
    recorded = {int(k): int(v) for k, v in audit["gates"]["race_counts"].items()}
    assert observed == recorded
    # [DATA: CSPUF2023_Codebook.txt, CSP_RACE/RACE frequencies]
    assert observed == {1: 5091, 2: 732, 3: 753, 4: 344}


# --- published anchor ------------------------------------------------------

def test_anchor_reproduction_exact():
    anc = pd.read_csv(DERIVED / "anchor_reproduction.csv")
    assert len(anc) == 3
    for col in ("total_n", "total_weighted", "hispanic_n", "hispanic_weighted",
                "nonhispanic_n", "nonhispanic_weighted"):
        assert (anc[f"published_{col}"] == anc[f"computed_{col}"]).all(), f"anchor mismatch on {col}"


def test_anchor_overall_weighted(audit, raw):
    assert round(float(raw[M.WEIGHT].sum())) == audit["anchor"]["overall_weighted_published"] == 61_369_577


# --- variance formula ------------------------------------------------------

def test_fay_scale_is_one_over_49(audit):
    assert audit["variance"]["rho"] == 0.3
    assert audit["variance"]["replicates"] == 100
    assert M.FAY_SCALE == pytest.approx(1.0 / 49.0)
    assert audit["variance"]["scale"] == pytest.approx(1.0 / 49.0)


def test_fay_se_zero_when_replicates_equal_point_estimate():
    est = np.full(101, 5.0)
    assert M.fay_se(est) == 0.0


def test_fay_se_matches_hand_computation():
    rng = np.random.default_rng(0)
    est = np.concatenate([[2.0], 2.0 + rng.normal(size=100)])
    expected = float(np.sqrt(np.sum((est[1:] - est[0]) ** 2) / 49.0))
    assert M.fay_se(est) == pytest.approx(expected)


# --- estimates re-derived from the raw file --------------------------------

def test_65plus_domain_is_codebook_age_groups_2_and_3(raw, audit):
    elderly = raw["CSP_AGE"].isin([2, 3])
    assert int(elderly.sum()) == audit["gates"]["elderly_n_obs"] == 5862
    assert int((elderly & (raw["CSP_RACE"] == 3)).sum()) == 632
    assert int((elderly & (raw["CSP_RACE"] == 1)).sum()) == 4454


@pytest.mark.parametrize("race_code,measure", [(3, "PUBLIC"), (1, "PUBLIC"), (3, "PAMTTOT"), (1, "PAMTTOT")])
def test_written_means_reproduce_from_raw(raw, table, race_code, measure):
    sub = raw[raw["CSP_AGE"].isin([2, 3]) & (raw["CSP_RACE"] == race_code)]
    y = (sub["PAMTCARE"] + sub["PAMTMADV"] + sub["PAMTCAID"]) if measure == "PUBLIC" else sub[measure]
    expected = float((sub[M.WEIGHT] * y).sum() / sub[M.WEIGHT].sum())
    row = table.query("domain == '65+' and race_code == @race_code and measure == @measure").iloc[0]
    assert row["estimate"] == pytest.approx(expected, rel=1e-10)
    assert row["n_obs"] == len(sub)
    assert row["weighted_n"] == pytest.approx(float(sub[M.WEIGHT].sum()), rel=1e-12)


def test_public_equals_medicare_plus_ma_plus_medicaid(table):
    wide = table.query("domain == '65+'").pivot(index="race_label", columns="measure", values="estimate")
    assert np.allclose(
        wide["PUBLIC"], wide["PAMTCARE"] + wide["PAMTMADV"] + wide["PAMTCAID"], rtol=1e-12
    )


def test_payer_components_sum_to_total(table, raw):
    """"The variable PAMTTOT is calculated as the sum of the seven top- and bottom-coded
    constituent variables for payments by payer type." [DATA: User's Guide sec. 3.4, p.6]

    Six of the seven are carried in the written table; the residual must therefore equal the
    weighted mean of the seventh, PAMTDISC (uncollected liability), exactly.
    """
    wide = table.query("domain == '65+'").pivot(index="race_label", columns="measure", values="estimate")
    parts = wide["PAMTCARE"] + wide["PAMTMADV"] + wide["PAMTCAID"] + wide["PAMTOOP"] + wide["PAMTALPR"] + wide["PAMTOTH"]
    residual = wide["PAMTTOT"] - parts

    elderly = raw[raw["CSP_AGE"].isin([2, 3])]
    disc = {}
    for code, label in M.RACE_LABELS.items():
        sub = elderly[elderly["CSP_RACE"] == code]
        disc[label] = float((sub[M.WEIGHT] * sub["PAMTDISC"]).sum() / sub[M.WEIGHT].sum())

    for label in wide.index:
        assert residual[label] == pytest.approx(disc[label], rel=1e-9), (
            f"{label}: PAMTTOT residual {residual[label]} != weighted PAMTDISC {disc[label]}"
        )
    assert (residual > 0).all()


def test_shares_are_probabilities(table):
    shares = table[table["measure"].isin(["ANY_MEDICAID", "ANY_MADV"])]
    assert len(shares) > 0
    assert (shares["estimate"] >= 0).all() and (shares["estimate"] <= 1).all()


def test_standard_errors_positive_and_finite(table):
    assert np.isfinite(table["se"]).all()
    assert (table["se"] > 0).all()


# --- ratios consistent with the means --------------------------------------

def test_ratios_equal_hispanic_over_white_means(ratios, table):
    for _, r in ratios.iterrows():
        h = table.query(
            "domain == @r.domain and race_code == 3 and measure == @r.measure"
        )["estimate"].iloc[0]
        w = table.query(
            "domain == @r.domain and race_code == 1 and measure == @r.measure"
        )["estimate"].iloc[0]
        assert r["hispanic_mean"] == pytest.approx(h, rel=1e-12)
        assert r["nhwhite_mean"] == pytest.approx(w, rel=1e-12)
        assert r["ratio"] == pytest.approx(h / w, rel=1e-12)
        assert r["diff"] == pytest.approx(h - w, rel=1e-12)


def test_ratio_ses_match_written_bounds(ratios):
    assert np.allclose(ratios["ratio_ci95_lo"], ratios["ratio"] - 1.96 * ratios["ratio_se"])
    assert np.allclose(ratios["ratio_ci95_hi"], ratios["ratio"] + 1.96 * ratios["ratio_se"])
    flag = (ratios["ratio_ci95_lo"] > 1.0) | (ratios["ratio_ci95_hi"] < 1.0)
    assert (ratios["ratio_excludes_1"] == flag).all()


def test_ratio_se_is_not_the_naive_delta_of_independent_means(ratios):
    """The replicate ratio SE must differ from the independence-assuming delta-method SE;
    if they matched to machine precision the replicate path was not used."""
    r = ratios.query("domain == '65+' and measure == 'PUBLIC'").iloc[0]
    naive = r["ratio"] * np.sqrt(
        (r["hispanic_se"] / r["hispanic_mean"]) ** 2 + (r["nhwhite_se"] / r["nhwhite_mean"]) ** 2
    )
    assert r["ratio_se"] != pytest.approx(naive, rel=1e-9)
    assert 0.5 * naive < r["ratio_se"] < 2.0 * naive  # same order of magnitude


def test_headline_public_ratio_is_above_one_with_ci_recorded(ratios):
    r = ratios.query("domain == '65+' and measure == 'PUBLIC'").iloc[0]
    assert r["ratio"] > 1.0
    assert r["hispanic_n_obs"] == 632 and r["nhwhite_n_obs"] == 4454
    assert r["ratio_ci95_lo"] < 1.0 < r["ratio_ci95_hi"]  # not distinguishable from parity at 95%


def test_all_expected_domains_present(ratios):
    assert set(ratios["domain"]) == {"65+", "65-74", "75+", "65+ income <$25,000", "65+ income >=$25,000"}


# --- documentation honesty -------------------------------------------------

def test_audit_records_the_documented_variance_method(audit):
    v = audit["variance"]
    assert "balanced repeated replication (BRR)" in v["quote_user_guide_7_1"]
    assert "Fay's adjustment of 0.3" in v["quote_user_guide_7_1"]
    assert 'rho = 0.3' in v["quote_user_guide_appendix_b_r"]
    assert "fay(.3)" in v["quote_user_guide_appendix_b_stata"]
    assert "not a literal quote" in v["formula_status"]


def test_audit_carries_the_scope_caveats(audit):
    blob = " ".join(audit["caveats"]).lower()
    assert "community" in blob and "facility" in blob
    assert "99.5" in blob
    assert "not mexican-origin" in blob
    assert "country of birth" in blob


def test_result_md_declares_hispanic_is_not_mexican_origin():
    text = (LANE / "RESULT.md").read_text()
    assert text.startswith("**Verdict:**")
    assert "not Mexican-origin" in text or "NOT Mexican-origin" in text
    assert "[DATA:" in text and "[CALCULATION:" in text
