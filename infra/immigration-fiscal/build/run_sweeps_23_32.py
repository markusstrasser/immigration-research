#!/usr/bin/env python3
"""Execute sweeps 23–32: mine PDF → rebuild → query → append memo section."""
from __future__ import annotations

import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
RESEARCH = ROOT / "research"
MINING = RESEARCH / ".mining"
INFRA = Path(__file__).resolve().parents[1]
from paths import data_root

DATA = data_root()
MEMO = RESEARCH / "immigration-sweep-cycles-23-32-2026-06-15.md"


def _pdftext(rel: str, pages: str | None = None) -> str:
    pdf = DATA / rel
    if not pdf.exists():
        return ""
    cmd = ["pdftotext"]
    if pages:
        cmd.extend(pages.split())
    cmd.extend([str(pdf), "-"])
    try:
        return subprocess.check_output(cmd, stderr=subprocess.DEVNULL, text=True, errors="replace")[:12000]
    except Exception:
        return ""


def _run(cmd: list[str], cwd: Path | None = None) -> str:
    print("$", " ".join(cmd))
    return subprocess.check_output(cmd, cwd=cwd or INFRA, text=True, stderr=subprocess.STDOUT)


def _query(sql: str) -> list[dict]:
    import duckdb

    u = Path.home() / "Projects/research/warehouse/immigration_fiscal_union.duckdb"
    con = duckdb.connect(str(u), read_only=True)
    con.execute(f"ATTACH '{Path.home() / 'Projects/research/warehouse/immigration_context.duckdb'}' AS ctx (READ_ONLY)")
    con.execute(f"ATTACH '{Path.home() / 'Projects/research/warehouse/immigration_lifetime_evidence.duckdb'}' AS life (READ_ONLY)")
    cols = [d[0] for d in con.execute(sql).description]
    return [dict(zip(cols, r)) for r in con.execute(sql).fetchall()]


def _append_memo(section: str) -> None:
    MEMO.parent.mkdir(parents=True, exist_ok=True)
    if not MEMO.exists():
        MEMO.write_text(
            "# Sweep cycles 23–32 — full protocol (2026-06-15)\n\n"
            "**Protocol:** `notes/immigration-lifetime-sweep-protocol.md`\n\n"
            "Each cycle: diverge → acquire/mine → rebuild → analyze → synthesize.\n\n---\n\n"
        )
    with MEMO.open("a") as f:
        f.write(section)
        if not section.endswith("\n\n"):
            f.write("\n\n")


def _write_mining(sweep: int, cluster: str, claims: list[dict]) -> None:
    MINING.mkdir(parents=True, exist_ok=True)
    path = MINING / f"immigration-lifetime-sweep-{sweep}-{cluster}.json"
    path.write_text(json.dumps({"sweep": sweep, "mined_at": datetime.now(timezone.utc).isoformat(), "claims": claims}, indent=2))


SWEEPS = [
    {
        "n": 23,
        "title": "NAS Table 8-13 college+ NPV cells",
        "diverge": "Without college+ NAS cells, EU/white lifetime blocked — extract from PDF.",
        "pdf": "external/lifetime/nas/nas_2017_immigration_economic_fiscal_full.pdf",
        "pages": "-f 344 -l 348",
        "rebuild": ["lifetime", "tensor"],
        "cluster": "nas-table-8-13",
        "claims": [
            {"id": "S23-01", "param": "npv_immigrant_lt_hs_individual", "value": -109000, "unit": "2012 USD", "ref": "Table 8-13"},
            {"id": "S23-02", "param": "npv_immigrant_hs_individual", "value": 49000, "unit": "2012 USD", "ref": "Table 8-13"},
            {"id": "S23-03", "param": "npv_immigrant_somcol_individual", "value": 205000, "unit": "2012 USD", "ref": "Table 8-13"},
            {"id": "S23-04", "param": "npv_immigrant_ba_individual", "value": 514000, "unit": "2012 USD", "ref": "Table 8-13"},
        ],
        "sql": """
            SELECT population_group,
              ROUND(MAX(CASE WHEN fiscal_layer='lifetime_npv' THEN value_per_adult_weighted END)) npv,
              ROUND(MAX(CASE WHEN fiscal_layer='federal_annual' THEN value_per_adult_weighted END)) fed
            FROM v_country_fiscal_rollup WHERE effect_order=1
            GROUP BY 1 HAVING npv IS NOT NULL ORDER BY npv
        """,
    },
    {
        "n": 24,
        "title": "Orrenius static school cost critique",
        "diverge": "Static school burden overstates cost if descendant taxes omitted.",
        "pdf": "external/lifetime/dallasfed/orrenius_nas_fiscal_sensitivity_wp1704.pdf",
        "pages": None,
        "rebuild": [],
        "cluster": "orrenius-static",
        "claims": [],
        "sql": """
            SELECT population_group, ROUND(school_per_adult) school, ROUND(net_crude_per_adult) crude
            FROM v_three_layer_annual WHERE population_group IN ('mexico_origin','nh_white_usborn')
        """,
    },
    {
        "n": 25,
        "title": "Return-migration horizon haircut",
        "diverge": "Duleep-Regets selective exit shortens effective NAS horizon for LDC cells.",
        "pdf": "external/lifetime/iza/iza_dp631_duleep_regets_immigrant_quality_human_capital.pdf",
        "pages": None,
        "rebuild": ["lifetime"],
        "cluster": "return-haircut",
        "claims": [{"id": "S25-01", "param": "mexico_growth_sensitivity_pp_per_1k_entry", "value": 0.199, "ref": "IZA dp631"}],
        "sql": "SELECT * FROM life.return_migration_haircut_scenarios",
    },
    {
        "n": 26,
        "title": "School burden microsim adult weights",
        "diverge": "Scenario adult N was PUMA subset — use microsim adults for kids/adult.",
        "pdf": None,
        "rebuild": ["tensor"],
        "cluster": "school-microsim-weights",
        "claims": [],
        "sql": """
            SELECT population_group, ROUND(school_per_adult) school, ROUND(federal_per_adult) fed,
              ROUND(net_crude_per_adult) net FROM v_three_layer_annual
            WHERE school_per_adult IS NOT NULL ORDER BY net_crude_per_adult
        """,
    },
    {
        "n": 27,
        "title": "FB <HS school burden row",
        "diverge": "Low-skill pool school burden was NULL — fill from origin-weighted per_pupil×kids.",
        "pdf": None,
        "rebuild": ["tensor"],
        "cluster": "fb-lt-hs-school",
        "claims": [],
        "sql": """
            SELECT * FROM v_three_layer_annual WHERE population_group='fb_lt_hs'
        """,
    },
    {
        "n": 28,
        "title": "LPR Mexico class weights",
        "diverge": "Dynamic Razin weights need structured LPR xlsx parse.",
        "pdf": None,
        "rebuild": ["tensor"],
        "cluster": "lpr-mexico",
        "claims": [],
        "sql": "SELECT * FROM lpr_mexico_row_sketch LIMIT 5",
    },
    {
        "n": 29,
        "title": "Akers-Boustan native child mobility",
        "diverge": "Descendant fiscal attribution — native HS completion in immigrant cities.",
        "pdf": "external/lifetime/nber/akers_boustan_2024_immigration_inequality_next_generation_w33961.pdf",
        "pages": None,
        "rebuild": [],
        "cluster": "akers-descendants",
        "claims": [],
        "sql": None,
    },
    {
        "n": 30,
        "title": "Marginal vs average pupil (NAS congestible)",
        "diverge": "NAS treats K-12 as congestible not pure public good — average cost upper bound.",
        "pdf": "external/lifetime/nas/nas_2017_immigration_economic_fiscal_full.pdf",
        "pages": "-f 320 -l 325",
        "rebuild": [],
        "cluster": "nas-congestible",
        "claims": [],
        "sql": """
            SELECT population_group, ROUND(net_crude_per_adult) base,
              ROUND(federal_per_adult - 0.5*school_per_adult) half_marg
            FROM v_three_layer_annual WHERE population_group IN ('mexico_origin','nh_white_usborn','eu27_origin')
        """,
    },
    {
        "n": 31,
        "title": "Saiz elasticity × school PUMA",
        "diverge": "High school burden origins may land in inelastic-rent metros.",
        "pdf": None,
        "rebuild": [],
        "cluster": "saiz-school-puma",
        "claims": [],
        "sql": """
            SELECT ROUND(AVG(elasticity),2) med_eps, COUNT(*) n FROM life.saiz_msa_elasticity
            WHERE elasticity IS NOT NULL
        """,
    },
    {
        "n": 32,
        "title": "Converge — three-layer + lifetime thesis",
        "diverge": "Integrate sweeps 23–31 into revised thesis.",
        "pdf": None,
        "rebuild": [],
        "cluster": "converge",
        "claims": [],
        "sql": """
            SELECT t.population_group, ROUND(t.federal_per_adult) fed, ROUND(t.school_per_adult) school,
              ROUND(t.net_crude_per_adult) crude,
              ROUND(MAX(CASE WHEN r.fiscal_layer='lifetime_npv' THEN r.value_per_adult_weighted END)) npv
            FROM v_three_layer_annual t
            LEFT JOIN v_country_fiscal_rollup r ON t.population_group=r.population_group
              AND r.fiscal_layer='lifetime_npv' AND r.effect_order=1
            WHERE t.population_group IN ('mexico_origin','eu27_origin','nh_white_usborn','fb_lt_hs')
            GROUP BY 1,2,3,4 ORDER BY 1
        """,
    },
]


def main() -> None:
    start = int(sys.argv[1]) if len(sys.argv) > 1 else 23
    os.chdir(INFRA)
    for sw in SWEEPS:
        if sw["n"] < start:
            continue
        n = sw["n"]
        print(f"\n{'='*60}\nSWEEP {n}: {sw['title']}\n{'='*60}")
        excerpt = ""
        if sw.get("pdf"):
            excerpt = _pdftext(sw["pdf"], sw.get("pages"))
            if excerpt:
                print(f"  mined {len(excerpt)} chars from {sw['pdf']}")
        if sw.get("claims"):
            _write_mining(n, sw["cluster"], sw["claims"])
        for rb in sw.get("rebuild") or []:
            if rb == "lifetime":
                _run(["bash", "rebuild_lifetime_warehouse.sh"])
            elif rb == "tensor":
                _run(["uv", "run", "--with", "duckdb,pandas", "python", "build/build_country_fiscal_tensor.py"])
        data = _query(sw["sql"]) if sw.get("sql") else []
        synth_lines = []
        if n == 23 and data:
            synth_lines.append("Lifetime NPV now spans all education buckets; Mexico sign may flip positive on full mix [check data].")
        elif n == 26 and data:
            mex = next((r for r in data if r.get("population_group") == "mexico_origin"), {})
            synth_lines.append(f"Mexico school/adult revised to ${mex.get('school', '?'):,.0f} with microsim weights.")
        elif n == 32:
            synth_lines.append("Final object: federal_annual | school_burden_per_adult | net_crude | lifetime_npv — never one scalar.")
        else:
            synth_lines.append(f"Query returned {len(data)} rows; see data block.")
        section = f"## Cycle {n} — {sw['title']}\n\n"
        section += f"**Diverge:** {sw['diverge']}\n\n"
        if sw.get("pdf"):
            section += f"**Paper:** `{sw['pdf']}`"
            if excerpt:
                snippet = excerpt.replace("\n", " ")[:400]
                section += f" — excerpt: _{snippet}…_\n\n"
            else:
                section += " — [UNVERIFIED: pdftotext empty]\n\n"
        if sw.get("claims"):
            section += f"**Mined claims:** `{MINING.name}/immigration-lifetime-sweep-{n}-{sw['cluster']}.json`\n\n"
        if sw.get("rebuild"):
            section += f"**Rebuild:** {', '.join(sw['rebuild'])}\n\n"
        section += "**Data:**\n```json\n" + json.dumps(data[:12], indent=2, default=str) + "\n```\n\n"
        section += "**Synthesis:** " + " ".join(synth_lines) + "\n\n---\n\n"
        _append_memo(section)
        print(f"  appended cycle {n} to {MEMO.name}")
    print(f"\nDone. Memo: {MEMO}")


if __name__ == "__main__":
    main()
