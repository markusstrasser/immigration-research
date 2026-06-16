#!/usr/bin/env python3
"""Emit immigration-lifetime-cluster-s-restrictionist-full.json from corpus parses.

Reads marker-modal page.md per paper, splits by section headers, tags sentences
with numerics as parameter_claims. Merges hand-curated Gould Table 1 + anchor
claims from cluster-s.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
CORPUS = Path.home() / "Projects" / "corpus"
OUT = REPO / "research" / ".mining" / "immigration-lifetime-cluster-s-restrictionist-full.json"
BASE = REPO / "research" / ".mining" / "immigration-lifetime-cluster-s-restrictionist.json"

PAPERS: list[dict] = [
    {
        "sha": "sha_ebb48fc02c714bfe",
        "source_rel_path": "external/lifetime/nber/borjas_2003_labor_demand_curve_immigration_w9755.pdf",
        "prefix": "W9755",
        "target": 51,
    },
    {
        "sha": "sha_d18f2c501794dccc",
        "source_rel_path": "external/lifetime/nber/borjas_2005_native_internal_migration_immigration_w11610.pdf",
        "prefix": "W11610",
        "target": 56,
    },
    {
        "sha": "sha_841c0a577e4ffa05",
        "source_rel_path": "external/lifetime/nber/borjas_grogger_hanson_2006_immigration_african_american_employment_w12518.pdf",
        "prefix": "BGH",
        "target": 48,
    },
    {
        "sha": "sha_73e2279cb366d94b",
        "source_rel_path": "external/lifetime/nber/gould_2024_asylum_seekers_homelessness_w33655.pdf",
        "prefix": "GOULD",
        "target": 32,
    },
    {
        "sha": "sha_c731d5cbb632176f",
        "source_rel_path": "external/lifetime/dallasfed/orrenius_nas_fiscal_sensitivity_wp1704.pdf",
        "prefix": "ORR",
        "target": 18,
    },
    {
        "sha": "sha_e761985b0f6b84d8",
        "source_rel_path": "external/lifetime/nber/razin_sadka_swagel_2011_migration_welfare_state_w15597.pdf",
        "prefix": "R15597",
        "target": 35,
    },
    {
        "sha": "sha_15b1f196f1207bc6",
        "source_rel_path": "external/lifetime/nber/razin_wahba_2012_welfare_magnet_immigration_w17515.pdf",
        "prefix": "R17515",
        "target": 28,
    },
    {
        "sha": "sha_c0bc44bdd41dad19",
        "source_rel_path": "external/lifetime/nber/hanson_liu_mcgee_2018_rise_fall_us_low_skilled_immigration_w23753.pdf",
        "prefix": "H23753",
        "target": 42,
    },
    {
        "sha": "sha_c3910a894c59e230",
        "source_rel_path": "external/lifetime/nber/borjas_1997_ethnicity_intergenerational_welfare_w6175.pdf",
        "prefix": "W6175",
        "target": 47,
    },
]

NUM_RE = re.compile(
    r"(?<![A-Za-z0-9])(?:\d{1,3}(?:,\d{3})+|\d+\.?\d*|\d+/\d+|\d+–\d+|\d+-\d+)(?:%|pp|bps)?"
)
SECTION_RE = re.compile(r"^#{1,3}\s+\*?\*?(.+?)\*?\*?\s*$", re.M)
SENT_SPLIT = re.compile(r"(?<=[.!?])\s+")


def _parse_dir(sha: str) -> Path | None:
    root = CORPUS / sha
    if not root.is_dir():
        return None
    for d in root.iterdir():
        if d.is_dir() and d.name.startswith("parsed."):
            return d
    return None


def _slug(s: str, n: int = 48) -> str:
    s = re.sub(r"[^a-z0-9]+", "_", s.lower()).strip("_")
    return s[:n] or "section"


def _sections(text: str) -> list[tuple[str, str]]:
    parts = SECTION_RE.split(text)
    if len(parts) < 2:
        return [("body", text)]
    out: list[tuple[str, str]] = []
    # split returns [preamble, h1, body1, h2, body2, ...]
    if parts[0].strip():
        out.append(("preamble", parts[0]))
    for i in range(1, len(parts) - 1, 2):
        out.append((parts[i].strip(), parts[i + 1]))
    return out


def _numeric_claims(
    paper: dict, section: str, body: str, start_idx: int
) -> tuple[list[dict], int]:
    claims: list[dict] = []
    idx = start_idx
    sec_ref = section[:80]
    for sent in SENT_SPLIT.split(body):
        sent = re.sub(r"\s+", " ", sent).strip()
        if len(sent) < 40 or len(sent) > 420:
            continue
        if not NUM_RE.search(sent):
            continue
        if sent.lower().startswith(("http", "www.", "figure", "table")):
            continue
        if re.search(r"^\|", sent):
            continue
        idx += 1
        claims.append(
            {
                "claim_id": f"S-{paper['prefix']}-{idx:03d}",
                "source_rel_path": paper["source_rel_path"],
                "corpus_sha": paper["sha"],
                "parameter_name": f"{_slug(section)}_{idx}",
                "value_text": sent[:400],
                "population": None,
                "page_ref": sec_ref,
                "claim_type": "empirical",
                "notes": "auto-mined from corpus section sentence",
            }
        )
    return claims, idx


def _mine_paper(paper: dict) -> list[dict]:
    pdir = _parse_dir(paper["sha"])
    if not pdir:
        print(f"WARN: missing corpus parse for {paper['sha']}")
        return []
    text = (pdir / "page.md").read_text(errors="replace")
    claims: list[dict] = []
    idx = 0
    for section, body in _sections(text):
        if section.lower().startswith(("references", "bibliography", "appendix figure")):
            continue
        batch, idx = _numeric_claims(paper, section, body, idx)
        claims.extend(batch)
    # cap near target but keep all if fewer
    target = paper["target"]
    if len(claims) > target + 8:
        # prefer sentences with % or coefficient-like tokens
        def score(c: dict) -> int:
            t = c["value_text"]
            s = 0
            if "%" in t:
                s += 3
            if re.search(r"\b(elasticity|coefficient|estimate|θ|gamma)\b", t, re.I):
                s += 2
            if re.search(r"\$", t):
                s += 1
            return s

        claims.sort(key=score, reverse=True)
        claims = sorted(claims[:target], key=lambda c: c["claim_id"])
    return claims


def _gould_table_claims() -> list[dict]:
    src = "external/lifetime/nber/gould_2024_asylum_seekers_homelessness_w33655.pdf"
    sha = "sha_73e2279cb366d94b"
    rows = [
        ("nyc_sheltered_change_2022_2024", 77352, "persons", "NYC CoC"),
        ("chicago_sheltered_change_2022_2024", 14590, "persons", "Chicago CoC"),
        ("massachusetts_sheltered_change_2022_2024", 13353, "persons", "MA CoC"),
        ("denver_sheltered_change_2022_2024", 6556, "persons", "Denver CoC"),
        ("top_four_sheltered_change_combined", 111851, "persons", "top 4 CoCs"),
        ("nationwide_sheltered_change_2022_2024", 148626, "persons", "US total"),
        ("nyc_direct_asylum_sheltered_2024_pit", 66700, "persons", "NYC"),
        ("chicago_direct_asylum_sheltered_2024_pit", 13679, "persons", "Chicago"),
        ("massachusetts_direct_asylum_sheltered_2024_pit", 7821, "persons", "MA"),
        ("denver_direct_asylum_sheltered_2024_pit", 4300, "persons", "Denver"),
        ("top_four_direct_asylum_sheltered_2024_pit", 92500, "persons", "top 4"),
        ("nationwide_direct_asylum_share_of_shelter_rise", 0.6224, "fraction", "US"),
        ("nationwide_indirect_asylum_sheltered_2024_pit", 87611, "persons", "US"),
        ("nationwide_indirect_asylum_share_of_shelter_rise", 0.5895, "fraction", "US"),
        ("nyc_indirect_asylum_sheltered_2024_pit", 51099, "persons", "NYC"),
    ]
    out = []
    for i, (name, val, unit, pop) in enumerate(rows, 1):
        out.append(
            {
                "claim_id": f"S-GOULD-T1-{i:02d}",
                "source_rel_path": src,
                "corpus_sha": sha,
                "parameter_name": name,
                "value_numeric": val,
                "unit": unit,
                "population": pop,
                "page_ref": "Table 1",
                "claim_type": "empirical",
                "notes": "Gould Table 1 machine extract 2026-06-15",
            }
        )
    return out


def main() -> None:
    base = json.loads(BASE.read_text())
    curated = {c["claim_id"]: c for c in base.get("parameter_claims", [])}
    mined: list[dict] = []
    for paper in PAPERS:
        batch = _mine_paper(paper)
        print(f"{paper['prefix']}: {len(batch)} claims (target {paper['target']})")
        mined.extend(batch)

    # Replace Gould auto-mine with table extract + keep narrative claims without dup IDs
    mined = [c for c in mined if c["corpus_sha"] != "sha_73e2279cb366d94b"]
    mined.extend(_gould_table_claims())
    gould_narr = _mine_paper(next(p for p in PAPERS if p["prefix"] == "GOULD"))
    gould_narr = [c for c in gould_narr if "Table 1" not in c.get("page_ref", "")]
    mined.extend(gould_narr[:17])

    # Merge curated anchors (overwrite same claim_id if any)
    for c in mined:
        curated.pop(c.get("claim_id", ""), None)
    all_claims = list(curated.values()) + mined
    # dedupe by claim_id
    seen: set[str] = set()
    deduped: list[dict] = []
    for c in all_claims:
        cid = c.get("claim_id") or ""
        if cid in seen:
            continue
        seen.add(cid)
        deduped.append(c)

    blob = {
        "cluster": "S_restrictionist_steelman_full",
        "mined_at": "2026-06-15",
        "parse_method": "corpus marker-modal section miner + Gould Table 1",
        "full_extract_memo": "research/immigration-restrictionist-corpus-full-extract-2026-06-15.md",
        "claim_count": len(deduped),
        "corpus_root": str(CORPUS),
        "parameter_claims": deduped,
        "generators": base.get("generators", []),
        "perspectives": base.get("perspectives", []),
        "narratives": base.get("narratives", []),
    }
    OUT.write_text(json.dumps(blob, indent=2) + "\n")
    print(f"Wrote {OUT} ({len(deduped)} claims)")


if __name__ == "__main__":
    main()
