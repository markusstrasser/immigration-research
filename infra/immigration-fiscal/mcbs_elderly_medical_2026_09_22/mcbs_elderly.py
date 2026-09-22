#!/usr/bin/env python3
"""2023 MCBS Cost Supplement PUF: public medical spending per beneficiary at 65+,
Hispanic vs non-Hispanic white.

Purpose: bound how far the fiscal ledger's public-medical transport (MEPS public-payer
cost by age x US birth, no ethnicity dimension) could be off at 65+ for a
Hispanic-heavy population.

Hispanic (CSP_RACE=3) is NOT Mexican-origin and the file carries no country of birth.

Variance: balanced repeated replication with Fay's adjustment rho=0.3 over the 100
supplied replicate weights, as the acquired MCBS Microdata PUF Data User's Guide
prescribes (sec. 7.1 and Appendix B).

Reproduce from the repository root:
    uv run --no-project python3 infra/immigration-fiscal/mcbs_elderly_medical_2026_09_22/mcbs_elderly.py
"""

from __future__ import annotations

import hashlib
import io
import json
import sys
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd

LANE = Path(__file__).resolve().parent
ACCESS = LANE.parent / "fiscal_access_2026_09_20"
ZIP_PATH = ACCESS / "_cache" / "CSPUF2023_Data.zip"
CSV_MEMBER = "cspuf2023.csv"
CODEBOOK = ACCESS / "_cache" / "CSPUF2023_Codebook.txt"
VALIDATION = ACCESS / "derived" / "mcbs_validation.json"
DERIVED = LANE / "derived"

# [SOURCE: fiscal_access_2026_09_20/RESULT.md and the CMS download manifest]
EXPECTED_ZIP_SHA256 = "56937f1a623b77a85d5b401c1fdc00791098772c240073f70cbbbdff9db86d41"
EXPECTED_CSV_SHA256 = "3407a9a76e8ddb71d9b8e840c4c14c94ddd25648c2cc60bf7eeb1d537c96b188"

N_ROWS = 6920
N_COLS = 134
WEIGHT = "CSPUFWGT"
REPS = [f"CSPUF{i:03d}" for i in range(1, 101)]
FAY_RHO = 0.3
# BRR with Fay's adjustment: V(theta) = 1/(R(1-rho)^2) * sum_r (theta_r - theta_0)^2.
FAY_SCALE = 1.0 / (len(REPS) * (1.0 - FAY_RHO) ** 2)  # = 1/49

RACE_LABELS = {1: "Non-Hispanic white", 2: "Non-Hispanic black", 3: "Hispanic", 4: "Other"}
AGE_LABELS = {1: "Under 65", 2: "65-74", 3: "75+"}
INCOME_LABELS = {1: "<$25,000", 2: ">=$25,000"}
AGE65_CODES = (2, 3)  # [DATA: CSPUF2023_Codebook.txt, CSP_AGE/AGE2GRP]

# Payer amount columns used. "public" is built below.
PAYERS = {
    "PAMTTOT": "Total payments, all sources",
    "PAMTCARE": "Medicare payments",
    "PAMTMADV": "Medicare MCO/HMO (Medicare Advantage) payments",
    "PAMTCAID": "Medicaid payments",
    "PUBLIC": "Public = PAMTCARE + PAMTMADV + PAMTCAID",
    "PAMTOOP": "Out-of-pocket payments",
    "PAMTALPR": "All private insurance payments",
    "PAMTOTH": "Other payments (includes VA)",
}

MEASURE_LABELS = dict(PAYERS)
MEASURE_LABELS["ANY_MEDICAID"] = "Share with any Medicaid payment (dual-eligibility proxy)"
MEASURE_LABELS["ANY_MADV"] = "Share with any Medicare MCO/HMO payment (MA-enrolment proxy)"

# Published anchors from the acquired 2023MCBSSummaryofChangesCSPUF.pdf.
# [DATA: methodology/2023MCBSSummaryofChangesCSPUF.pdf, Exhibit 3.2.3 and Exhibit 3.3]
ANCHOR_RACE_TOTALS = {  # Exhibit 3.2.3, weighted counts
    1: 46_481_694,
    2: 6_302_150,
    3: 5_091_829,
    4: 3_493_903,
}
ANCHOR_OVERALL_WEIGHTED = 61_369_577
ANCHOR_EXHIBIT_33 = {  # Exhibit 3.3: age -> (total n, total wgt, hisp n, hisp wgt, nonhisp n, nonhisp wgt)
    1: (1058, 6_779_654, 121, 749_890, 937, 6_029_764),
    2: (2463, 31_805_081, 266, 2_698_696, 2197, 29_106_385),
    3: (3399, 22_784_842, 366, 1_643_244, 3033, 21_141_598),
}


class GateFailure(RuntimeError):
    pass


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def load_frame() -> tuple[pd.DataFrame, dict]:
    """Read the CSV straight out of the pinned zip, hashing both."""
    gates: dict[str, object] = {}
    if not ZIP_PATH.exists():
        raise GateFailure(f"[BLOCKED] missing input {ZIP_PATH}")
    zip_hash = sha256_file(ZIP_PATH)
    if zip_hash != EXPECTED_ZIP_SHA256:
        raise GateFailure(f"[BLOCKED] zip sha256 {zip_hash} != pinned {EXPECTED_ZIP_SHA256}")
    gates["zip_sha256_matches_pin"] = True

    with zipfile.ZipFile(ZIP_PATH) as zf:
        raw = zf.read(CSV_MEMBER)
    csv_hash = hashlib.sha256(raw).hexdigest()
    if csv_hash != EXPECTED_CSV_SHA256:
        raise GateFailure(f"[BLOCKED] csv sha256 {csv_hash} != pinned {EXPECTED_CSV_SHA256}")
    gates["csv_sha256_matches_pin"] = True

    df = pd.read_csv(io.BytesIO(raw))
    gates["zip_sha256"] = zip_hash
    gates["csv_sha256"] = csv_hash
    gates["codebook_sha256"] = sha256_file(CODEBOOK) if CODEBOOK.exists() else None
    return df, gates


def run_gates(df: pd.DataFrame, gates: dict) -> dict:
    if df.shape[0] != N_ROWS:
        raise GateFailure(f"[BLOCKED] rows {df.shape[0]} != {N_ROWS}")
    if df.shape[1] != N_COLS:
        raise GateFailure(f"[BLOCKED] columns {df.shape[1]} != {N_COLS}")
    gates["rows"] = int(df.shape[0])
    gates["columns"] = int(df.shape[1])

    if df["PUF_ID"].nunique() != N_ROWS:
        raise GateFailure("[BLOCKED] PUF_ID is not unique")
    gates["puf_id_unique"] = True

    if not (df["SURVEYYR"] == 2023).all():
        raise GateFailure("[BLOCKED] SURVEYYR is not uniformly 2023")
    gates["survey_year_2023"] = True

    val = json.loads(VALIDATION.read_text())
    expected_race = {int(k): int(v) for k, v in val["race_counts"].items()}
    observed_race = {int(k): int(v) for k, v in df["CSP_RACE"].value_counts().items()}
    if observed_race != expected_race:
        raise GateFailure(f"[BLOCKED] race counts {observed_race} != mcbs_validation.json {expected_race}")
    gates["race_counts_match_validation_json"] = True
    gates["race_counts"] = observed_race

    if not (df[WEIGHT] > 0).all():
        raise GateFailure("[BLOCKED] CSPUFWGT is not strictly positive for every record")
    gates["cspufwgt_all_positive"] = True

    missing = [c for c in REPS if c not in df.columns]
    if missing:
        raise GateFailure(f"[BLOCKED] missing replicate weights: {missing[:5]}")
    if not np.isfinite(df[REPS].to_numpy()).all():
        raise GateFailure("[BLOCKED] non-finite replicate weight")
    gates["replicate_weights_present"] = len(REPS)

    amount_cols = [c for c in PAYERS if c != "PUBLIC"]
    if df[amount_cols].isna().any().any():
        raise GateFailure("[BLOCKED] missing payer amounts")
    gates["payer_amounts_complete"] = True

    # Published-anchor gates (rounded to the dollar as the exhibits print them).
    total_w = float(df[WEIGHT].sum())
    if round(total_w) != ANCHOR_OVERALL_WEIGHTED:
        raise GateFailure(f"[BLOCKED] weighted total {round(total_w)} != Exhibit 3.2.3 {ANCHOR_OVERALL_WEIGHTED}")
    gates["anchor_overall_weighted_matches"] = True
    gates["weight_sum"] = total_w

    for code, target in ANCHOR_RACE_TOTALS.items():
        got = round(float(df.loc[df["CSP_RACE"] == code, WEIGHT].sum()))
        if got != target:
            raise GateFailure(f"[BLOCKED] race {code} weighted {got} != Exhibit 3.2.3 {target}")
    gates["anchor_race_totals_match"] = True

    anchor_rows = []
    for age_code, (n_tot, w_tot, n_h, w_h, n_nh, w_nh) in ANCHOR_EXHIBIT_33.items():
        sub = df[df["CSP_AGE"] == age_code]
        hisp = sub[sub["CSP_RACE"] == 3]
        nonhisp = sub[sub["CSP_RACE"] != 3]
        got = (
            len(sub), round(float(sub[WEIGHT].sum())),
            len(hisp), round(float(hisp[WEIGHT].sum())),
            len(nonhisp), round(float(nonhisp[WEIGHT].sum())),
        )
        want = (n_tot, w_tot, n_h, w_h, n_nh, w_nh)
        if got != want:
            raise GateFailure(f"[BLOCKED] Exhibit 3.3 age {age_code}: computed {got} != published {want}")
        anchor_rows.append(
            {
                "age_group": AGE_LABELS[age_code],
                "published_total_n": n_tot, "computed_total_n": got[0],
                "published_total_weighted": w_tot, "computed_total_weighted": got[1],
                "published_hispanic_n": n_h, "computed_hispanic_n": got[2],
                "published_hispanic_weighted": w_h, "computed_hispanic_weighted": got[3],
                "published_nonhispanic_n": n_nh, "computed_nonhispanic_n": got[4],
                "published_nonhispanic_weighted": w_nh, "computed_nonhispanic_weighted": got[5],
            }
        )
    gates["anchor_exhibit_3_3_matches"] = True
    return {"gates": gates, "anchor_rows": anchor_rows}


def weighted_means(y: np.ndarray, W: np.ndarray, mask: np.ndarray) -> np.ndarray:
    """Return length-(1+R) vector of weighted means: element 0 full sample, rest replicates.

    A domain mean under BRR is a ratio estimator computed inside each replicate, so
    subsetting to the domain per replicate is identical to the domain estimator. The
    acquired user guide sec. 7.3 states subsetting is valid for BRR.
    """
    Wm = W[mask]
    ym = y[mask]
    denom = Wm.sum(axis=0)
    if np.any(denom <= 0):
        raise GateFailure("[BLOCKED] non-positive weight sum in a domain replicate")
    return (Wm * ym[:, None]).sum(axis=0) / denom


def fay_se(est: np.ndarray) -> float:
    """est[0] is the full-sample estimate, est[1:] the replicates."""
    dev = est[1:] - est[0]
    return float(np.sqrt(FAY_SCALE * np.sum(dev**2)))


def build_rows(df: pd.DataFrame, W: np.ndarray) -> tuple[pd.DataFrame, dict]:
    """Estimates for every (domain, race, measure); returns a long table plus a lookup
    of the full replicate vectors so ratios reuse the identical replicate estimates."""
    y_cols = {name: df[name].to_numpy(dtype=float) for name in PAYERS if name != "PUBLIC"}
    y_cols["PUBLIC"] = y_cols["PAMTCARE"] + y_cols["PAMTMADV"] + y_cols["PAMTCAID"]
    y_cols["ANY_MEDICAID"] = (df["PAMTCAID"].to_numpy(dtype=float) > 0).astype(float)
    y_cols["ANY_MADV"] = (df["PAMTMADV"].to_numpy(dtype=float) > 0).astype(float)

    age = df["CSP_AGE"].to_numpy()
    race = df["CSP_RACE"].to_numpy()
    income = df["CSP_INCOME"].to_numpy()
    elderly = np.isin(age, AGE65_CODES)

    domains: list[tuple[str, np.ndarray]] = [("65+", elderly)]
    for code in AGE65_CODES:
        domains.append((AGE_LABELS[code], elderly & (age == code)))
    for icode, ilabel in INCOME_LABELS.items():
        domains.append((f"65+ income {ilabel}", elderly & (income == icode)))

    rows = []
    replicates: dict[tuple[str, int, str], np.ndarray] = {}
    for domain_label, domain_mask in domains:
        for rcode, rlabel in RACE_LABELS.items():
            mask = domain_mask & (race == rcode)
            n_obs = int(mask.sum())
            if n_obs == 0:
                continue
            w_n = float(df.loc[mask, WEIGHT].sum())
            for measure, y in y_cols.items():
                est = weighted_means(y, W, mask)
                replicates[(domain_label, rcode, measure)] = est
                rows.append(
                    {
                        "domain": domain_label,
                        "race_code": rcode,
                        "race_label": rlabel,
                        "measure": measure,
                        "measure_label": MEASURE_LABELS.get(measure, measure),
                        "estimate": float(est[0]),
                        "se": fay_se(est),
                        "n_obs": n_obs,
                        "weighted_n": w_n,
                    }
                )
    table = pd.DataFrame(rows)
    table["cv"] = np.where(table["estimate"] != 0, table["se"] / table["estimate"].abs(), np.nan)
    table["ci95_lo"] = table["estimate"] - 1.96 * table["se"]
    table["ci95_hi"] = table["estimate"] + 1.96 * table["se"]
    return table, replicates


def build_ratios(table: pd.DataFrame, replicates: dict) -> pd.DataFrame:
    """Hispanic / non-Hispanic white, with the ratio formed inside every replicate and
    the identical Fay formula applied to the replicate ratios."""
    rows = []
    domains = list(dict.fromkeys(table["domain"]))
    measures = list(dict.fromkeys(table["measure"]))
    for domain in domains:
        for measure in measures:
            k_h = (domain, 3, measure)
            k_w = (domain, 1, measure)
            if k_h not in replicates or k_w not in replicates:
                continue
            h = replicates[k_h]
            w = replicates[k_w]
            if w[0] == 0 or np.any(w == 0):
                continue
            ratio = h / w
            diff = h - w
            n_h = int(table.query("domain == @domain and race_code == 3 and measure == @measure")["n_obs"].iloc[0])
            n_w = int(table.query("domain == @domain and race_code == 1 and measure == @measure")["n_obs"].iloc[0])
            r_se = fay_se(ratio)
            d_se = fay_se(diff)
            rows.append(
                {
                    "domain": domain,
                    "measure": measure,
                    "measure_label": MEASURE_LABELS.get(measure, measure),
                    "hispanic_mean": float(h[0]),
                    "hispanic_se": fay_se(h),
                    "hispanic_n_obs": n_h,
                    "nhwhite_mean": float(w[0]),
                    "nhwhite_se": fay_se(w),
                    "nhwhite_n_obs": n_w,
                    "ratio": float(ratio[0]),
                    "ratio_se": r_se,
                    "ratio_ci95_lo": float(ratio[0]) - 1.96 * r_se,
                    "ratio_ci95_hi": float(ratio[0]) + 1.96 * r_se,
                    "ratio_excludes_1": bool(
                        (float(ratio[0]) - 1.96 * r_se > 1.0) or (float(ratio[0]) + 1.96 * r_se < 1.0)
                    ),
                    "diff": float(diff[0]),
                    "diff_se": d_se,
                    "diff_ci95_lo": float(diff[0]) - 1.96 * d_se,
                    "diff_ci95_hi": float(diff[0]) + 1.96 * d_se,
                }
            )
    return pd.DataFrame(rows)


def main() -> int:
    DERIVED.mkdir(parents=True, exist_ok=True)
    df, gates = load_frame()
    gate_out = run_gates(df, gates)
    gates = gate_out["gates"]

    W = df[[WEIGHT] + REPS].to_numpy(dtype=float)
    table, replicates = build_rows(df, W)
    ratios = build_ratios(table, replicates)

    elderly = np.isin(df["CSP_AGE"].to_numpy(), AGE65_CODES)
    gates["elderly_n_obs"] = int(elderly.sum())
    gates["elderly_weighted"] = float(df.loc[elderly, WEIGHT].sum())
    gates["elderly_hispanic_n_obs"] = int((elderly & (df["CSP_RACE"].to_numpy() == 3)).sum())
    gates["elderly_nhwhite_n_obs"] = int((elderly & (df["CSP_RACE"].to_numpy() == 1)).sum())

    table.to_csv(DERIVED / "elderly_cost_by_race.csv", index=False)
    ratios.to_csv(DERIVED / "ratios.csv", index=False)
    pd.DataFrame(gate_out["anchor_rows"]).to_csv(DERIVED / "anchor_reproduction.csv", index=False)

    # Sensitivity: the acquired guide names the method (BRR, Fay 0.3) and the software
    # options, not the centering. SAS/Stata centre on the full-sample estimate; R's
    # survey package defaults to centring on the replicate mean. Report both spreads
    # for the headline so the choice is inspectable.
    headline = {}
    for measure in ("PUBLIC", "PAMTTOT"):
        h = replicates[("65+", 3, measure)]
        w = replicates[("65+", 1, measure)]
        ratio = h / w
        dev_mean = ratio[1:] - ratio[1:].mean()
        headline[measure] = {
            "ratio": float(ratio[0]),
            "se_centred_full_sample": fay_se(ratio),
            "se_centred_replicate_mean": float(np.sqrt(FAY_SCALE * np.sum(dev_mean**2))),
        }

    audit = {
        "lane": "mcbs_elderly_medical_2026_09_22",
        "question": (
            "Public medical spending per community-dwelling Medicare beneficiary aged 65+, "
            "Hispanic vs non-Hispanic white, 2023 MCBS Cost Supplement PUF"
        ),
        "inputs": {
            "zip": str(ZIP_PATH),
            "zip_sha256": gates["zip_sha256"],
            "csv_member": CSV_MEMBER,
            "csv_sha256": gates["csv_sha256"],
            "codebook": str(CODEBOOK),
            "codebook_sha256": gates["codebook_sha256"],
            "validation_json": str(VALIDATION),
            "user_guide": str(ACCESS / "_cache" / "methodology" / "MCBSMicrodataPUFDataUsersGuide.pdf"),
            "summary_of_changes": str(ACCESS / "_cache" / "methodology" / "2023MCBSSummaryofChangesCSPUF.pdf"),
        },
        "gates": gates,
        "variance": {
            "method": "Balanced repeated replication with Fay's adjustment",
            "rho": FAY_RHO,
            "replicates": len(REPS),
            "scale": FAY_SCALE,
            "formula": "V(theta) = 1/(R*(1-rho)^2) * sum_r (theta_r - theta_0)^2",
            "formula_status": (
                "The acquired documents PRESCRIBE the method and the software options, not the "
                "algebra. The algebraic line above is the standard definition of those options "
                "(SAS VARMETHOD=BRR(FAY=.30), Stata vce(brr) fay(.3), R svrepdesign type='Fay' "
                "rho=0.3); it is not a literal quote."
            ),
            "quote_user_guide_7_1": (
                "When using the replicate weight approach to variance estimation, the variance "
                "estimation method of balanced repeated replication (BRR) using Fay's adjustment "
                "of 0.3 is recommended."
            ),
            "quote_user_guide_appendix_b_r": (
                "mcbs <- svrepdesign( weights = ~CSPUFWGT, repweights = \"CSPUF[001-100]+\", "
                "type = \"Fay\", rho = 0.3, data = <Source dataset>, combined.weights = TRUE )"
            ),
            "quote_user_guide_appendix_b_stata": (
                "svyset _n [pweight= CSPUFWGT ], brrweight(CSPUF001 - CSPUF100) fay(.3) "
                "vce(brr) singleunit(missing)"
            ),
            "quote_user_guide_7_3_subsetting": (
                "The recommended method of variance estimation for subgroup analysis is the BRR "
                "method; which does not require any special subgroup considerations. The BRR "
                "method allows the researcher to subset data to a subgroup of interest and still "
                "produce unbiased standard error estimates."
            ),
            "centering_sensitivity": headline,
        },
        "anchor": {
            "source": "2023MCBSSummaryofChangesCSPUF.pdf, Exhibits 3.2.3 and 3.3",
            "reproduced": True,
            "overall_weighted_published": ANCHOR_OVERALL_WEIGHTED,
            "overall_weighted_computed": round(gates["weight_sum"]),
            "detail": "derived/anchor_reproduction.csv",
        },
        "outputs": {
            "elderly_cost_by_race.csv": len(table),
            "ratios.csv": len(ratios),
            "anchor_reproduction.csv": len(gate_out["anchor_rows"]),
        },
        "caveats": [
            "Community-dwelling full-year beneficiaries only; anyone with a facility interview "
            "or any facility, hospice or institutional event or cost in 2023 is excluded.",
            "Service- and payer-specific cost and event variables are top-coded at the 99.5 percent level.",
            "CSP_RACE=3 is Hispanic of any national origin, NOT Mexican-origin.",
            "No country of birth, no nativity, no generation; 2023 calendar year only.",
        ],
    }
    (DERIVED / "audit.json").write_text(json.dumps(audit, indent=2) + "\n")

    pd.set_option("display.width", 200)
    print(f"[CALCULATION: mcbs_elderly.py] gates passed; 65+ n={gates['elderly_n_obs']} "
          f"(Hispanic {gates['elderly_hispanic_n_obs']}, NH white {gates['elderly_nhwhite_n_obs']})")
    print("\n--- 65+ weighted means per beneficiary, by race ---")
    print(
        table.query("domain == '65+'")
        .pivot(index="measure", columns="race_label", values="estimate")
        .round(1)
        .to_string()
    )
    print("\n--- Hispanic / non-Hispanic white ratios, 65+ ---")
    print(
        ratios.query("domain == '65+'")[
            ["measure", "hispanic_mean", "hispanic_se", "nhwhite_mean", "nhwhite_se",
             "ratio", "ratio_se", "ratio_ci95_lo", "ratio_ci95_hi", "ratio_excludes_1"]
        ].round(3).to_string(index=False)
    )
    print(f"\nWrote {DERIVED}/elderly_cost_by_race.csv, ratios.csv, anchor_reproduction.csv, audit.json")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except GateFailure as exc:
        print(str(exc), file=sys.stderr)
        sys.exit(2)
