#!/usr/bin/env python3
"""cb.py — minimal case-bank writer/validator (stdlib only).

Append-only jsonl store of specific, verbatim, ground-truth cases. Content-addressed
id => idempotent append. Provenance tags validated by LOADING the canonical regex
(hooks/provenance_tags.re), never restated here. See README.md for the contract.

    uv run python3 cb.py seed      # add the worked-example cases (idempotent)
    uv run python3 cb.py validate  # re-validate every row
    uv run python3 cb.py list      # list the bank
"""
from __future__ import annotations

import hashlib
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
STORE = HERE / "cases.jsonl"
SCHEMA_URI = "https://schema.local/research/casebank/v1.0.0"
SCHEMA_VERSION = "1-0-0"
GENRES = {"ground-truth-exemplar", "defect-trap", "capability-target", "failure-mode", "generator-seed"}
STATUSES = {"active", "superseded", "retracted"}
CANONICAL_RE = Path.home() / "Projects/skills/hooks/provenance_tags.re"


def canonical_json(obj) -> bytes:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def case_id(case: dict) -> str:
    stable = {
        "domain": case["domain"],
        "genre": case["genre"],
        "verbatim": case["verbatim"],
        "source": case["provenance"]["source"],
    }
    return "cb_" + hashlib.sha256(canonical_json(stable)).hexdigest()[:16]


def _now_z() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


_PROV = None  # cached compiled canonical regex, or False if unavailable


def _provenance_ok(tag: str) -> bool:
    """Validate a bare tag by testing its bracketed forms against the CANONICAL regex.
    Loads hooks/provenance_tags.re; fails LOUD (warns, returns True) if it can't — never
    silently restates the tag list (that drift is the bug the single-source rule prevents)."""
    global _PROV
    if _PROV is None:
        try:
            _PROV = re.compile(CANONICAL_RE.read_text().strip())
        except Exception as e:  # noqa: BLE001
            print(f"  [warn] cannot load canonical provenance regex ({CANONICAL_RE}): {e} — skipping tag check", file=sys.stderr)
            _PROV = False
    if _PROV is False:
        return True
    return bool(_PROV.search(f"[{tag}]") or _PROV.search(f"[{tag}: x]"))


def validate(case: dict) -> None:
    req = ["case_id", "schema_version", "conformsTo", "domain", "genre", "title",
           "verbatim", "payload", "provenance", "asserted_at", "recorded_at"]
    missing = [k for k in req if k not in case]
    if missing:
        raise ValueError(f"missing required fields: {missing}")
    if case["genre"] not in GENRES:
        raise ValueError(f"genre {case['genre']!r} not in {sorted(GENRES)}")
    if len(case["verbatim"]) < 80:
        raise ValueError(f"verbatim too short ({len(case['verbatim'])} < 80) — a gist is not a case")
    if not case["payload"].strip():
        raise ValueError("payload empty — a case must seed something")
    p = case["provenance"]
    for k in ("source", "tag", "capture"):
        if not p.get(k):
            raise ValueError(f"provenance.{k} missing")
    if p["capture"] not in ("verbatim", "reconstructed"):
        raise ValueError(f"provenance.capture {p['capture']!r} invalid")
    if not _provenance_ok(p["tag"]):
        raise ValueError(f"provenance.tag {p['tag']!r} not a canonical provenance tag")
    if case.get("status", "active") not in STATUSES:
        raise ValueError(f"status {case['status']!r} invalid")
    if not re.match(r"^cb_[0-9a-f]{16}$", case["case_id"]):
        raise ValueError(f"case_id {case['case_id']!r} malformed")


def _existing_ids() -> set[str]:
    if not STORE.exists():
        return set()
    return {json.loads(line)["case_id"] for line in STORE.read_text().splitlines() if line.strip()}


def add_case(case: dict) -> str:
    """Compute id, stamp recorded_at, validate, append. Idempotent on content-addressed id."""
    case = dict(case)
    case.setdefault("schema_version", SCHEMA_VERSION)
    case.setdefault("conformsTo", SCHEMA_URI)
    case.setdefault("recorded_at", _now_z())
    if "asserted_at" not in case:
        raise ValueError("asserted_at required (world time the case occurred)")
    case["case_id"] = case_id(case)
    validate(case)
    if case["case_id"] in _existing_ids():
        return case["case_id"]  # idempotent skip
    with STORE.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(case, ensure_ascii=False) + "\n")
    return case["case_id"]


def _rows() -> list[dict]:
    if not STORE.exists():
        return []
    return [json.loads(line) for line in STORE.read_text().splitlines() if line.strip()]


# --- worked examples (verbatim text read from the named sources, 2026-06-15) -------------

SEED = [
    {
        "domain": "agent-review",
        "genre": "defect-trap",
        "title": "Phantom join — plan aggregates over a field that indexes something else",
        "verbatim": (
            "substrate-closure plan §5.4 proposed compile-gate aggregation \"via produces_refs\"; that "
            "field indexes reference databases, not claims — the join doesn't exist (2026-05-12; codified "
            "in plan-review-gate rule). Packet: plan excerpt asserting the join + the actual schema/struct "
            "defs + grep-style evidence listing of where the field appears. Gold: the named join field "
            "cannot join the named entities."
        ),
        "payload": (
            "A plan can assert a join/aggregation over a field whose real semantics don't support it; "
            "packet-only reviewers miss it, the repo-access axis catches it. Detection must NAME the field "
            "and state it cannot join. Seductive wrong reads: 'it's just slow' (it's impossible as written), "
            "or inventing a different field that also doesn't exist."
        ),
        "provenance": {
            "source": "evals/critique_replay/cases.md C5",
            "source_ref": "evals/critique_replay/cases.md",
            "tag": "SOURCE",
            "capture": "reconstructed",
            "retrieved_at": "2026-06-15T00:00:00Z",
        },
        "tags": ["plan-review", "phantom-join", "premise-defect"],
        "asserted_at": "2026-05-12T00:00:00Z",
        "extension": {
            "anchor": "produces_refs + (does-not | no-mapping | indexes-<other>)",
            "invention_traps": ["the aggregation is merely SLOW", "invent a different nonexistent field"],
            "gold": "the named join field cannot join the named entities",
            "stratum": "premise-defect",
        },
    },
    {
        "domain": "manim-expression",
        "genre": "capability-target",
        "title": "MathTex / TransformMatchingTex — the largest 3b1b expression blocker",
        "verbatim": (
            "MathTex / TransformMatchingTex — largest blocker; Stage 0 slice landed (`verify:scene-math`), "
            "Stage 1 MATH table TBD. Workbench inspect loop on 3b1b-class content: blocked on math until "
            "glyph IR is rich enough. Wild 3b1b scenes end-to-end: NOT YET — math depth + a few deferred gaps."
        ),
        "payload": (
            "Highest-leverage capability gap for 3b1b expression parity is equation typesetting + morphing "
            "(MathTex/TransformMatchingTex); it gates end-to-end scene parity. Target = green expression "
            "gates (snapshot parity), NOT Manim API parity or Grant's GL shader look. Probe with minimal-IR "
            "scenes exercising the same expression class; gate on snapshot, not eyeball."
        ),
        "provenance": {
            "source": "anim-workbench/docs/reports/3b1b-reference-bank.md",
            "source_ref": "anim-workbench/docs/reports/3b1b-reference-bank.md",
            "tag": "SOURCE",
            "capture": "verbatim",
            "retrieved_at": "2026-06-15T00:00:00Z",
        },
        "tags": ["manim", "expression-gap", "mathtex", "capability-target"],
        "asserted_at": "2026-06-15T00:00:00Z",
        "extension": {
            "gate": "verify:scene-math (Stage 0 landed); Stage 1 MATH table TBD",
            "coverage_status": "NOT YET end-to-end — blocked on math / glyph-IR richness",
            "in_scope": ["math on screen", "equation morphs", "TransformMatchingTex"],
            "out_scope": ["identical LaTeX font/color", "ManimGL shader look"],
        },
    },
]


def main(argv: list[str]) -> int:
    cmd = argv[1] if len(argv) > 1 else "list"
    if cmd == "seed":
        for c in SEED:
            cid = add_case(c)
            print(f"  + {cid}  {c['genre']:<20} {c['title']}")
        print(f"bank: {STORE} ({len(_rows())} cases)")
    elif cmd == "validate":
        rows = _rows()
        bad = 0
        for r in rows:
            try:
                validate(r)
            except ValueError as e:
                bad += 1
                print(f"  FAIL {r.get('case_id','?')}: {e}")
        print(f"{len(rows) - bad}/{len(rows)} valid")
        return 1 if bad else 0
    elif cmd == "list":
        for r in _rows():
            print(f"  {r['case_id']}  {r['genre']:<20} [{r['domain']}] {r['title']}")
        print(f"({len(_rows())} cases)")
    else:
        print(__doc__)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
