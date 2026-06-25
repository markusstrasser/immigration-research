#!/usr/bin/env python3
"""Compose cell-level fiscal scenario ledger from SIPP + MEPS + federal + local context.

Outputs descriptive scenario inputs — not a scalar net-fiscal verdict.
Spec: research/immigration-public-mvp-sipp-meps-bridge-2026-04-11.md
      research/immigration-net-negative-dataset-frontier-2026-06-15.md
"""
from __future__ import annotations

import csv
import json
from pathlib import Path

from paths import derived_root, duckdb_path

PROTO = derived_root() / "stage3_proto"
STAGE5 = derived_root() / "stage5"
OUT_SIPP = PROTO / "sipp_scenario_ledger_2024.csv"
OUT_ORIGIN = PROTO / "origin_fiscal_scenario_2023.csv"
META = PROTO / "scenario_ledger_2024.meta.json"

SIPP_EDUC_TO_ACS = {
    "1_lt_hs": "<HS",
    "2_hs_ged": "HS / GED",
    "3_some_college": "some college / associate",
    "4_associate": "some college / associate",
    "5_bachelors": "other",
    "6_masters": "other",
    "7_professional_plus": "other",
}


def _read_csv(path: Path) -> list[dict]:
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def _federal_by_education() -> dict[str, dict]:
    import duckdb

    db = duckdb_path()
    if not db.exists():
        return {}
    con = duckdb.connect(str(db), read_only=True)
    if not con.execute(
        "SELECT COUNT(*) FROM information_schema.tables WHERE table_name='acs_origin_household_federal_microsim_2023'"
    ).fetchone()[0]:
        con.close()
        return {}
    rows = con.execute("""
        SELECT
          education_bucket,
          SUM(weighted_adults) AS w,
          SUM(federal_net_proxy_annual * weighted_adults) / NULLIF(SUM(weighted_adults), 0) AS avg_federal_net,
          SUM(payroll_tax_proxy_annual * weighted_adults) / NULLIF(SUM(weighted_adults), 0) AS avg_payroll,
          SUM(transfer_outflow_proxy_annual * weighted_adults) / NULLIF(SUM(weighted_adults), 0) AS avg_transfers
        FROM acs_origin_household_federal_microsim_2023
        WHERE donor_household_weight IS NOT NULL
        GROUP BY 1
    """).fetchall()
    con.close()
    return {
        r[0]: {"avg_federal_net": r[2], "avg_payroll": r[3], "avg_transfers": r[4], "weight": r[1]}
        for r in rows
    }


def compose_sipp_ledger() -> list[dict]:
    sipp = _read_csv(PROTO / "sipp_public_mvp_cells_2024.csv")
    health = {
        (r["sipp_age_band"], r["sipp_nativity_code"], r["sipp_education_bucket"]): r
        for r in _read_csv(PROTO / "sipp_meps_expected_health_cost_cells_2024.csv")
    }
    fed = _federal_by_education()
    rows = []
    for s in sipp:
        key = (s["age_band"], s["nativity_code"], s["education_bucket"])
        h = health.get(key, {})
        acs_edu = SIPP_EDUC_TO_ACS.get(s["education_bucket"], "other")
        f = fed.get(acs_edu, {})
        annual_earn = float(s.get("mean_monthly_tpearn") or 0) * 12
        annual_transfers = (
            float(s.get("mean_monthly_tsnap_amt") or 0)
            + float(s.get("mean_monthly_ttanf_amt") or 0)
            + float(s.get("mean_monthly_tssi_amt") or 0)
        ) * 12
        rows.append(
            {
                **{k: s[k] for k in ("age_band", "nativity_code", "nativity_label", "education_bucket", "citizenship_code")},
                "sipp_person_weight_sum": s["sipp_person_weight_sum"],
                "mean_annual_tpearn": annual_earn,
                "mean_annual_transfers_snap_tanf_ssi": annual_transfers,
                "expected_mean_totexp23": h.get("expected_mean_totexp23"),
                "expected_mean_totmcd23": h.get("expected_mean_totmcd23"),
                "federal_net_proxy_annual_edu_bucket": f.get("avg_federal_net"),
                "payroll_tax_proxy_annual_edu_bucket": f.get("avg_payroll"),
                "transfer_outflow_proxy_annual_edu_bucket": f.get("avg_transfers"),
                "acs_education_bucket_mapped": acs_edu,
            }
        )
    return rows


def compose_origin_ledger() -> list[dict]:
    import duckdb

    db = duckdb_path()
    if not db.exists():
        return []
    con = duckdb.connect(str(db), read_only=True)
    if not con.execute(
        "SELECT COUNT(*) FROM information_schema.tables WHERE table_name='acs_origin_national_2023'"
    ).fetchone()[0]:
        con.close()
        return []

    has_stage5 = con.execute(
        "SELECT COUNT(*) FROM information_schema.tables WHERE table_name='origin_puma_household_stage5_context_2023'"
    ).fetchone()[0]

    if has_stage5:
        sql = """
            SELECT
              n.origin_label,
              n.weighted_adults,
              h.linked_household_wgt,
              h.linked_mean_hh_school_age_children,
              s.area_wtd_current_spend_per_pupil,
              s.area_wtd_housing_stress_pct,
              s.avg_rpp_all_items_2023,
              s.mean_state_medicaid_total_usd,
              s.avg_lep_count_reported,
              fm.avg_federal_net,
              fm.avg_payroll,
              fm.avg_transfers
            FROM acs_origin_national_2023 n
            LEFT JOIN acs_origin_household_national_2023 h USING (origin_label)
            LEFT JOIN (
              SELECT origin_label,
                     AVG(area_wtd_current_spend_per_pupil) AS area_wtd_current_spend_per_pupil,
                     AVG(area_wtd_housing_stress_pct) AS area_wtd_housing_stress_pct,
                     AVG(rpp_all_items_2023) AS avg_rpp_all_items_2023,
                     -- mean of STATE Medicaid totals across the origin's PUMAs (a "which states do
                     -- they live in" context signal, $billions) — NOT a per-adult cost. Honestly
                     -- named after the 2026-06-25 forensic-gate review; a per-capita version needs a
                     -- state-population denominator (ACS pull) — see HUMAN.md + pre-reg P3.
                     AVG(medicaid_total_computable) AS mean_state_medicaid_total_usd,
                     AVG(lep_count_reported) AS avg_lep_count_reported
              FROM origin_puma_household_stage5_context_2023
              GROUP BY 1
            ) s ON n.origin_label = s.origin_label
            LEFT JOIN (
              SELECT origin_label,
                     SUM(federal_net_proxy_annual * weighted_adults)
                       / NULLIF(SUM(weighted_adults), 0) AS avg_federal_net,
                     SUM(payroll_tax_proxy_annual * weighted_adults)
                       / NULLIF(SUM(weighted_adults), 0) AS avg_payroll,
                     SUM(transfer_outflow_proxy_annual * weighted_adults)
                       / NULLIF(SUM(weighted_adults), 0) AS avg_transfers
              FROM acs_origin_household_federal_microsim_2023
              WHERE donor_household_weight IS NOT NULL
              GROUP BY 1
            ) fm ON n.origin_label = fm.origin_label
            ORDER BY n.weighted_adults DESC
        """
    else:
        sql = """
            SELECT
              n.origin_label,
              n.weighted_adults,
              h.linked_household_wgt,
              h.linked_mean_hh_school_age_children,
              s.area_wtd_current_spend_per_pupil,
              s.area_wtd_housing_stress_pct,
              NULL::DOUBLE AS avg_rpp_all_items_2023,
              NULL::DOUBLE AS mean_state_medicaid_total_usd,
              NULL::DOUBLE AS avg_lep_count_reported,
              fm.avg_federal_net,
              fm.avg_payroll,
              fm.avg_transfers
            FROM acs_origin_national_2023 n
            LEFT JOIN acs_origin_household_national_2023 h USING (origin_label)
            LEFT JOIN (
              SELECT origin_label,
                     AVG(area_wtd_current_spend_per_pupil) AS area_wtd_current_spend_per_pupil,
                     AVG(area_wtd_housing_stress_pct) AS area_wtd_housing_stress_pct
              FROM origin_puma_household_stage2_context_2023
              GROUP BY 1
            ) s ON n.origin_label = s.origin_label
            LEFT JOIN (
              SELECT origin_label,
                     SUM(federal_net_proxy_annual * weighted_adults)
                       / NULLIF(SUM(weighted_adults), 0) AS avg_federal_net,
                     SUM(payroll_tax_proxy_annual * weighted_adults)
                       / NULLIF(SUM(weighted_adults), 0) AS avg_payroll,
                     SUM(transfer_outflow_proxy_annual * weighted_adults)
                       / NULLIF(SUM(weighted_adults), 0) AS avg_transfers
              FROM acs_origin_household_federal_microsim_2023
              WHERE donor_household_weight IS NOT NULL
              GROUP BY 1
            ) fm ON n.origin_label = fm.origin_label
            ORDER BY n.weighted_adults DESC
        """
    cur = con.execute(sql)
    cols = [d[0] for d in cur.description]
    rows = [dict(zip(cols, r)) for r in cur.fetchall()]
    con.close()
    return rows


def compose() -> tuple[Path, Path]:
    PROTO.mkdir(parents=True, exist_ok=True)
    sipp_rows = compose_sipp_ledger()
    origin_rows = compose_origin_ledger()

    with OUT_SIPP.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(sipp_rows[0].keys()) if sipp_rows else [])
        w.writeheader()
        w.writerows(sipp_rows)

    if origin_rows:
        with OUT_ORIGIN.open("w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=list(origin_rows[0].keys()))
            w.writeheader()
            w.writerows(origin_rows)

    meta = {
        "builder": "compose_scenario_ledger.py",
        "sipp_scenario_rows": len(sipp_rows),
        "origin_scenario_rows": len(origin_rows),
        "outputs": [str(OUT_SIPP), str(OUT_ORIGIN)],
        "notes": "Descriptive scenario inputs; not net-fiscal verdict. Federal column is SIPP-donor proxy.",
    }
    META.write_text(json.dumps(meta, indent=2) + "\n")
    print(f"Wrote {OUT_SIPP} ({len(sipp_rows)} rows)")
    if origin_rows:
        print(f"Wrote {OUT_ORIGIN} ({len(origin_rows)} rows)")
    return OUT_SIPP, OUT_ORIGIN


if __name__ == "__main__":
    compose()
