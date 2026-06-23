#!/usr/bin/env python3
"""Catalog lifetime fiscal evidence + structured side tables (no PDF text mining).

Separate DuckDB from immigration_context.duckdb — papers have no row-level join keys.
Bridge dimensions: education_bucket, state_fips, origin_label, fiscal_layer, topic.
"""
from __future__ import annotations

import csv
import hashlib
import json
import re
import sys
from pathlib import Path

from paths import data_root, derived_root, lifetime_duckdb_path

REPO = Path(__file__).resolve().parents[3]
MANIFEST = Path(__file__).resolve().parents[1] / "DOWNLOAD_MANIFEST.tsv"
MINING_DIR = REPO / "research" / ".mining"
LT = data_root() / "external" / "lifetime"
DERIVED = derived_root()
DUCKDB_PATH = lifetime_duckdb_path()

NBER_RE = re.compile(r"w(\d{4,5})", re.I)
TOPIC_RULES: list[tuple[str, str]] = [
    (r"nas|nrc|generational|storesletten|lee_miller|auerbach", "npv_generational"),
    (r"clemens|colas|orrenius|cgdev", "npv_critique_offset"),
    (r"borjas|card|peri|foged|mariel|labor_demand|task_special|ottaviano.*w12497", "labor_market"),
    (r"h1b|bound_khanna|high.skill|recruit_internationally", "high_skill_labor"),
    (r"welfare|magnet|bitler|safety_net|medicaid|medicare", "transfers_safety_net"),
    (r"asylum|homeless|receiver|vmt|housing|frbsf|crime|butchart|saiz|elasticity", "local_capacity"),
    (r"abramitzky|duncan_trejo|descendant|second_gen|kuka|daca|occupational_mobility", "descendants_assimilation"),
    (r"hanson.*low_skilled|composition|migrant_network|hurricane|border_enforcement|lozano", "composition_networks"),
    (r"remittance|worldbank", "remittances"),
    (r"itep|pew|undocumented|unauthorized", "legal_status_tax"),
    (r"refugee|dp10234", "refugee_path"),
    (r"popproj|np2023", "forward_stock"),
    (r"sipp|meps|census|omb|nces|cdc|life_table", "microsim_inputs"),
    (r"return_migration|duleep|regets|dp631|dp8628", "return_migration_assimilation"),
    (r"ortega.*w14833|international_migration", "oecd_flows"),
    (r"admin|cbp|ice|enforcement", "admin_enforcement_cost"),
    (r"derived/stage2|derived/stage5|receiver_city|school_finance_county", "incidence_bridge"),
    (r"meps_health|health_cost", "health_cost_bridge"),
    (r"dustmann|survey|methodology|green_kotlikoff|cream|cbo", "methodology_comparator"),
]

def _require_duckdb():
    try:
        import duckdb  # noqa: F401
    except ImportError:
        print("duckdb not installed; run: uv run --with duckdb python ...", file=sys.stderr)
        sys.exit(1)


def _sid(rel: str) -> str:
    return hashlib.sha1(rel.encode()).hexdigest()[:16]


def _infer_topic(rel: str, notes: str) -> list[str]:
    blob = f"{rel} {notes}".lower()
    tags = [tag for pat, tag in TOPIC_RULES if re.search(pat, blob)]
    return tags or ["uncategorized"]


def _manifest_lifetime_rows() -> list[dict]:
    rows: list[dict] = []
    if not MANIFEST.exists():
        return rows
    with MANIFEST.open(newline="") as f:
        for row in csv.DictReader(f, delimiter="\t"):
            if row.get("stage") != "lifetime":
                continue
            rel = row["path_relative"]
            p = data_root() / rel
            rows.append(
                {
                    "source_id": _sid(rel),
                    "rel_path": rel,
                    "category": Path(rel).parts[1] if len(Path(rel).parts) > 1 else "root",
                    "file_name": Path(rel).name,
                    "ext": Path(rel).suffix.lower().lstrip("."),
                    "bytes": p.stat().st_size if p.exists() else None,
                    "min_bytes_expected": int(row.get("min_bytes") or 0),
                    "acquire_script": row.get("script", ""),
                    "notes": row.get("notes", ""),
                    "exists": p.exists(),
                }
            )
    return rows


def _scan_orphans(manifest_rows: list[dict]) -> list[dict]:
    known = {r["rel_path"] for r in manifest_rows}
    extra: list[dict] = []
    if not LT.exists():
        return extra
    for p in sorted(LT.rglob("*")):
        if not p.is_file():
            continue
        rel = str(p.relative_to(data_root()))
        if rel in known:
            continue
        extra.append(
            {
                "source_id": _sid(rel),
                "rel_path": rel,
                "category": p.parent.name,
                "file_name": p.name,
                "ext": p.suffix.lower().lstrip("."),
                "bytes": p.stat().st_size,
                "min_bytes_expected": 0,
                "acquire_script": "scan",
                "notes": "orphan (not in manifest)",
                "exists": True,
            }
        )
    return extra


def _load_remittances(con) -> None:
    import pandas as pd

    for country, fname in (("Mexico", "mexico_worker_remittances_bx_trf_pwkr_cd_dt.json"), ("USA", "usa_worker_remittances_bx_trf_pwkr_cd_dt.json")):
        p = LT / "worldbank" / fname
        if not p.exists():
            continue
        raw = json.loads(p.read_text())
        obs = raw[1] if isinstance(raw, list) and len(raw) > 1 else raw
        rows = []
        for o in obs:
            if not isinstance(o, dict):
                continue
            rows.append(
                {
                    "country": country,
                    "year": int(o["date"]) if o.get("date") else None,
                    "indicator_id": o.get("indicator", {}).get("id"),
                    "value_usd": o.get("value"),
                }
            )
        if rows:
            con.register("_remit", pd.DataFrame(rows))
            con.execute("CREATE OR REPLACE TABLE remittance_series AS SELECT * FROM _remit")


def _load_omb(con) -> None:
    import pandas as pd

    for stem, table in (
        ("budget_fy2025_table_3_1_outlays_by_function", "omb_outlays_by_function"),
        ("budget_fy2025_table_12_1_federal_grants_state_local", "omb_federal_grants_slocal"),
    ):
        p = LT / "omb" / f"{stem}.xlsx"
        if not p.exists():
            continue
        df = pd.read_excel(p, sheet_name=0)
        df.columns = [str(c).strip().lower().replace(" ", "_") for c in df.columns]
        con.register("_omb_df", df)
        con.execute(f"CREATE OR REPLACE TABLE {table} AS SELECT * FROM _omb_df")


def _seed_npv_benchmarks(con) -> None:
    """Published anchor cells — NAS Table 8-13 mined sweep 23 (pdftotext 2026-06-15)."""
    rows = [
        # study, acs_education_bucket, age_at_arrival, individual_npv_2012_usd, includes_descendants, adjustment, source_rel_path, notes
        ("NAS 2017", "<HS", 25, -109_000, False, "baseline_public_goods",
         "external/lifetime/nas/nas_2017_immigration_economic_fiscal_full.pdf",
         "Table 8-13 Individual Immigrant CBO outlook; public goods excluded"),
        ("NAS 2017", "HS / GED", 25, 49_000, False, "baseline_public_goods",
         "external/lifetime/nas/nas_2017_immigration_economic_fiscal_full.pdf",
         "Table 8-13 HS row Individual Immigrant +$49k (was -$31k erroneous seed)"),
        ("NAS 2017", "some college / associate", 25, 205_000, False, "baseline_public_goods",
         "external/lifetime/nas/nas_2017_immigration_economic_fiscal_full.pdf",
         "Table 8-13 SomCol Individual Immigrant +$205k"),
        ("NAS 2017", "other", 25, 514_000, False, "baseline_public_goods",
         "external/lifetime/nas/nas_2017_immigration_economic_fiscal_full.pdf",
         "Table 8-13 BA Individual Immigrant +$514k; >BA +$972k not separate ACS bucket"),
        ("NAS 2017", "<HS", 25, -109_000, True, "baseline_public_goods_descendants",
         "external/lifetime/nas/nas_2017_immigration_economic_fiscal_full.pdf",
         "Table 8-13 <HS Total Immigrant -$186k incl descendants"),
        ("NRC 1997", "<HS", 25, -13_000, False, "baseline",
         "external/lifetime/nrc/nrc_1997_new_americans.pdf", "older benchmark relay"),
        ("Clemens 2023", "<HS", 25, 128_000, False, "capital_tax_adjustment",
         "external/lifetime/cgdev/clemens_2023_fiscal_effect_capital_tax_adjustment.pdf",
         "NAS <HS flip with capital-tax channel"),
        ("Colas-Sachs 2024", "<HS", None, 750, False, "indirect_annual_usd",
         "external/lifetime/econstor/colas_sachs_2024_indirect_fiscal_benefits_low_skill.pdf",
         "~$750/yr indirect federal benefit"),
        ("Storesletten 2003", "<HS", None, None, False, "range",
         "external/lifetime/nber/storesletten_2003_fiscal_heterogeneity_w9489.pdf",
         "sign sensitive; -36k to +96k in framework"),
    ]
    con.execute("CREATE OR REPLACE TABLE npv_education_benchmarks AS SELECT * FROM (VALUES "
                + ",".join(["(?,?,?,?,?,?,?,?)"] * len(rows)) + ") AS t(study, acs_education_bucket, "
                "age_at_arrival, individual_npv_2012_usd, includes_descendants, adjustment, "
                "source_rel_path, notes)", [x for row in rows for x in row])


def _seed_return_migration_haircut(con) -> None:
    """Sweep 25 — Duleep-Regets sensitivity bands on effective NPV horizon. [SOURCE: iza_dp631]"""
    con.execute("""
        CREATE OR REPLACE TABLE return_migration_haircut_scenarios AS
        SELECT * FROM (VALUES
          ('baseline_no_haircut', 1.0, 'Full 75yr NAS horizon'),
          ('ldc_selective_emigration', 0.75, 'Duleep-Regets: LDC inverse growth; shorten effective years 25% [INFERENCE]'),
          ('mexico_central_america', 0.70, 'IZA dp631 Central/South Am +19.9pp growth per $1k entry — exit bias [SOURCE: cluster I]'),
          ('high_skill_low_exit', 1.0, 'EU/India corridor — low return probability [INFERENCE]')
        ) AS t(scenario_id, npv_horizon_multiplier, notes)
    """)


def _seed_bridge_dimensions(con) -> None:
    con.execute("""
        CREATE OR REPLACE TABLE bridge_dimensions AS
        SELECT * FROM (VALUES
          ('education_bucket', 'acs_education_bucket', 'Join NAS NPV + SIPP federal microsim + ACS stock'),
          ('state_fips', 'state_fips', 'Join stage2/5 local cost context'),
          ('origin_label', 'origin_label', 'Composition weights only — not lifetime scalar'),
          ('fiscal_layer', 'federal|state_local|local_shock|private_transfer', 'Which ledger the source informs'),
          ('topic', 'source_topic_tags.topic', 'Evidence catalog clustering — no FK to context rows')
        ) AS t(dimension, key_field, join_rule)
    """)


def _load_structured_layers(con) -> None:
    import pandas as pd

    saiz = LT / "saiz" / "saiz_2010_msa_elasticity.dta"
    if saiz.exists():
        df = pd.read_stata(saiz)
        con.register("_saiz", df)
        con.execute("CREATE OR REPLACE TABLE saiz_msa_elasticity AS SELECT * FROM _saiz")

    itep = LT / "itep" / "itep_2024_tax_contributions.json"
    if itep.exists():
        blob = json.loads(itep.read_text())
        if isinstance(blob, dict):
            rows = [{"metric": k, "value": v} for k, v in blob.items()]
            con.register("_itep", pd.DataFrame(rows))
            con.execute("CREATE OR REPLACE TABLE itep_undocumented_tax_summary AS SELECT * FROM _itep")

    csv_tables = [
        ("origin_fiscal_scenario_2023", "derived/stage3_proto/origin_fiscal_scenario_2023.csv"),
        ("sipp_scenario_ledger_2024", "derived/stage3_proto/sipp_scenario_ledger_2024.csv"),
        ("school_finance_county_2023", "derived/stage2/school_finance_county_2023.csv"),
        ("chas_county_housing_stress_2018_2022", "derived/stage2/chas_county_housing_stress_2018_2022.csv"),
        ("irs_migration_county_2022_2023", "derived/stage2/irs_migration_county_2022_2023.csv"),
        ("puma_county_area_xwalk_2023", "derived/stage2/puma_county_area_xwalk_2023.csv"),
        ("state_stage5_context_2023", "derived/stage5/state_stage5_context_2023.csv"),
        ("receiver_city_migrant_costs", "derived/stage5/receiver_city_migrant_costs.csv"),
        ("cdc_period_life_table_2021", "derived/lifetime/cdc_period_life_table_2021.csv"),
        ("ssa_period_life_table_2023", "ssa/ssa_period_life_table_2023.csv"),
        ("hud_pit_coc_annual", "derived/stage5/hud_pit_coc_annual.csv"),
        ("gould_asylum_shelter_attribution_2022_2024", "derived/stage5/gould_asylum_shelter_attribution_2022_2024.csv"),
        ("meps_health_cost_module_2023", "derived/stage3_proto/meps_health_cost_module_2023.csv"),
        ("sipp_meps_expected_health_cost_cells_2024", "derived/stage3_proto/sipp_meps_expected_health_cost_cells_2024.csv"),
        ("acs_foreign_born_education_bucket_totals_2023", "derived/stage3_proto/acs_foreign_born_education_bucket_totals_2023.csv"),
        ("sipp_public_mvp_cells_2024", "derived/stage3_proto/sipp_public_mvp_cells_2024.csv"),
    ]
    for table, rel in csv_tables:
        sub = rel.removeprefix("derived/")
        p = DERIVED / sub if (DERIVED / sub).exists() else LT / rel
        if p.exists():
            con.execute(f"CREATE OR REPLACE TABLE {table} AS SELECT * FROM read_csv_auto('{p}')")


def _claim_values(c: dict) -> tuple[float | None, str | None]:
    vn = c.get("value_numeric")
    vt = c.get("value_text")
    if vn is None and (vr := c.get("value_range")) and isinstance(vr, list) and len(vr) == 2:
        try:
            lo, hi = float(vr[0]), float(vr[1])
            vn = (lo + hi) / 2
            vt = vt or f"{lo}–{hi}"
        except (TypeError, ValueError):
            vt = vt or str(vr)
    return vn, vt


def _load_mining_artifacts(con) -> tuple[int, int, int]:
    import pandas as pd

    claims_n = gens_n = theories_n = 0
    claim_by_id: dict[str, dict] = {}
    gen_by_id: dict[str, dict] = {}
    theory_rows: list[dict] = []
    if not MINING_DIR.exists():
        return 0, 0, 0
    paths = sorted(MINING_DIR.glob("immigration-lifetime-*.json"))
    full_s = MINING_DIR / "immigration-lifetime-cluster-s-restrictionist-full.json"
    if full_s.exists():
        paths = [p for p in paths if p.name != "immigration-lifetime-cluster-s-restrictionist.json"]
    for p in paths:
        try:
            blob = json.loads(p.read_text())
        except json.JSONDecodeError:
            continue
        for c in blob.get("parameter_claims", []):
            rel = c.get("source_rel_path", "")
            vn, vt = _claim_values(c)
            cid = c.get("claim_id") or _sid(f"{rel}:{c.get('parameter_name')}")
            claim_by_id[cid] = {
                    "claim_id": cid,
                    "source_id": _sid(rel) if rel else None,
                    "source_rel_path": rel,
                    "claim_type": c.get("claim_type"),
                    "parameter_name": c.get("parameter_name"),
                    "value_numeric": vn,
                    "value_text": vt,
                    "unit": c.get("unit"),
                    "population": c.get("population"),
                    "direction": c.get("direction"),
                    "confidence": c.get("confidence"),
                    "page_ref": c.get("page_ref"),
                    "unnamed_assumption": c.get("unnamed_assumption", False),
                    "cluster": blob.get("cluster"),
                    "notes": c.get("notes"),
                }
        for g in blob.get("generators", []):
            gid = g.get("id") or g.get("generator_id")
            gen_by_id[gid] = {
                    "generator_id": gid,
                    "name": g.get("name"),
                    "prompt_template": g.get("prompt"),
                    "retrodiction_example": g.get("retrodiction"),
                    "negative_space": g.get("negative_space"),
                    "unnamed_assumptions": json.dumps(g.get("unnamed_assumptions_surfaced", [])),
                    "topics": json.dumps(g.get("topics", [])),
                    "source_rel_paths": json.dumps(g.get("source_rel_paths", [])),
                    "cluster": blob.get("cluster"),
                    "theory_tested": g.get("theory_tested"),
                }
        for t in blob.get("theories_tested", []):
            theory_rows.append(
                {
                    "theory_id": _sid(f"{blob.get('cluster')}:{t.get('theory')}"),
                    "cluster": blob.get("cluster"),
                    "theory": t.get("theory"),
                    "prediction": t.get("prediction"),
                    "duckdb_test": t.get("duckdb_test"),
                    "falsifier": t.get("falsifier"),
                }
            )
    claim_rows = list(claim_by_id.values())
    gen_rows = list(gen_by_id.values())
    if claim_rows:
        con.register("_claims", pd.DataFrame(claim_rows))
        con.execute("CREATE OR REPLACE TABLE parameter_claims AS SELECT * FROM _claims")
        claims_n = len(claim_rows)
    if gen_rows:
        con.register("_gens", pd.DataFrame(gen_rows))
        con.execute("CREATE OR REPLACE TABLE lifetime_generators AS SELECT * FROM _gens")
        gens_n = len(gen_rows)
    if theory_rows:
        con.register("_theories", pd.DataFrame(theory_rows))
        con.execute("CREATE OR REPLACE TABLE theories_tested AS SELECT * FROM _theories")
        theories_n = len(theory_rows)
    return claims_n, gens_n, theories_n


def _create_gould_views(con) -> None:
    """Join Gould Table 1 attribution to HUD PIT + receiver city costs."""
    tables = {r[0] for r in con.execute("SHOW TABLES").fetchall()}
    if "gould_asylum_shelter_attribution_2022_2024" not in tables:
        return
    con.execute("""
        CREATE OR REPLACE VIEW v_gould_shelter_attribution AS
        SELECT * FROM gould_asylum_shelter_attribution_2022_2024
    """)
    if "hud_pit_coc_annual" not in tables:
        return
    con.execute("""
        CREATE OR REPLACE VIEW v_gould_hud_pit_top4 AS
        WITH top4 AS (
          SELECT * FROM gould_asylum_shelter_attribution_2022_2024
          WHERE coc_label IN ('NY-600','IL-510','MA-ALL','CO-503')
        ),
        pit AS (
          SELECT coc_id, coc_name, year, sheltered, unsheltered, total
          FROM hud_pit_coc_annual
          WHERE year IN (2022, 2023, 2024)
        )
        SELECT
          t.locality,
          t.coc_label,
          p.coc_id,
          p.coc_name,
          p.year,
          p.sheltered,
          p.unsheltered,
          p.total,
          t.sheltered_change_2022_2024,
          t.direct_asylum_seekers_2024_pit,
          t.direct_asylum_share_of_change,
          t.indirect_asylum_seekers_2024_pit,
          t.indirect_asylum_share_of_change
        FROM top4 t
        LEFT JOIN pit p
          ON p.coc_id = t.coc_label
          OR (t.coc_label = 'MA-ALL' AND p.coc_id LIKE 'MA-%')
        ORDER BY t.locality, p.coc_id, p.year
    """)
    if "receiver_city_migrant_costs" not in tables:
        return
    con.execute("""
        CREATE OR REPLACE VIEW v_gould_episodic_ledger AS
        SELECT
          g.locality,
          g.coc_label,
          g.sheltered_change_2022_2024,
          g.direct_asylum_seekers_2024_pit,
          g.direct_asylum_share_of_change,
          g.indirect_asylum_seekers_2024_pit,
          r.city AS receiver_city,
          r.fiscal_year,
          r.total_spending_usd_M,
          r.peak_shelter_census,
          r.baseline_shelter_census,
          r.scope_notes,
          r.source AS receiver_source
        FROM gould_asylum_shelter_attribution_2022_2024 g
        LEFT JOIN receiver_city_migrant_costs r
          ON (g.locality LIKE 'New York%' AND lower(r.city) IN ('nyc', 'new york'))
          OR (g.locality = 'Chicago' AND lower(r.city) = 'chicago')
          OR (g.locality = 'Massachusetts' AND lower(r.city) LIKE '%mass%')
          OR (g.locality LIKE 'Metropolitan Denver%' AND lower(r.city) LIKE '%denver%')
        WHERE g.coc_label IN ('NY-600','IL-510','MA-ALL','CO-503')
    """)


def build() -> None:
    _require_duckdb()
    import duckdb
    import pandas as pd

    manifest_rows = _manifest_lifetime_rows()
    catalog = manifest_rows + _scan_orphans(manifest_rows)

    if DUCKDB_PATH.exists():
        DUCKDB_PATH.unlink()
    DUCKDB_PATH.parent.mkdir(parents=True, exist_ok=True)
    con = duckdb.connect(str(DUCKDB_PATH))

    con.register("_catalog", pd.DataFrame(catalog))
    con.execute("""
        CREATE TABLE source_catalog AS
        SELECT
          source_id, rel_path, category, file_name, ext, bytes,
          min_bytes_expected, acquire_script, notes, exists,
          regexp_extract(file_name, 'w(\\d{4,5})', 1) AS nber_id
        FROM _catalog
    """)

    tag_rows = []
    for row in catalog:
        for topic in _infer_topic(row["rel_path"], row["notes"]):
            tag_rows.append({"source_id": row["source_id"], "topic": topic})
    con.register("_tags", pd.DataFrame(tag_rows))
    con.execute("CREATE TABLE source_topic_tags AS SELECT * FROM _tags")

    _seed_npv_benchmarks(con)
    _seed_return_migration_haircut(con)
    _seed_bridge_dimensions(con)
    _load_remittances(con)
    try:
        _load_omb(con)
    except Exception as exc:
        print(f"WARN: OMB xlsx skipped: {exc}", file=sys.stderr)
    try:
        _load_structured_layers(con)
    except Exception as exc:
        print(f"WARN: structured layers skipped: {exc}", file=sys.stderr)

    claims_n, gens_n, theories_n = _load_mining_artifacts(con)
    try:
        _create_gould_views(con)
    except Exception as exc:
        print(f"WARN: Gould views skipped: {exc}", file=sys.stderr)
    if claims_n == 0:
        con.execute("""
            CREATE TABLE parameter_claims (
              claim_id VARCHAR, source_id VARCHAR, source_rel_path VARCHAR,
              claim_type VARCHAR, parameter_name VARCHAR,
              value_numeric DOUBLE, value_text VARCHAR, unit VARCHAR,
              population VARCHAR, direction VARCHAR, confidence VARCHAR,
              page_ref VARCHAR, unnamed_assumption BOOLEAN, cluster VARCHAR, notes VARCHAR
            )
        """)
    if gens_n == 0:
        con.execute("""
            CREATE TABLE lifetime_generators (
              generator_id VARCHAR, name VARCHAR, prompt_template VARCHAR,
              retrodiction_example VARCHAR, negative_space VARCHAR,
              unnamed_assumptions VARCHAR, topics VARCHAR, source_rel_paths VARCHAR,
              cluster VARCHAR, theory_tested VARCHAR
            )
        """)
    if theories_n == 0:
        con.execute("""
            CREATE TABLE theories_tested (
              theory_id VARCHAR, cluster VARCHAR, theory VARCHAR,
              prediction VARCHAR, duckdb_test VARCHAR, falsifier VARCHAR
            )
        """)

    link = DERIVED / "immigration_lifetime_evidence.duckdb"
    if link.is_symlink() or link.exists():
        link.unlink()
    link.symlink_to(DUCKDB_PATH)

    n_src = con.execute("SELECT COUNT(*) FROM source_catalog").fetchone()[0]
    n_tag = con.execute("SELECT COUNT(*) FROM source_topic_tags").fetchone()[0]
    size_mb = DUCKDB_PATH.stat().st_size / (1024 * 1024)
    con.close()
    print(f"Wrote {DUCKDB_PATH} ({size_mb:.2f} MB)")
    print(f"  source_catalog: {n_src}  topic_tags: {n_tag}  claims: {claims_n}  generators: {gens_n}  theories: {theories_n}")


if __name__ == "__main__":
    build()
