"""Behavioral controls and fail-closed adoption checks for living citations."""
import json
import sys
from pathlib import Path

import pytest

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
import citation_freshness as C  # noqa: E402


@pytest.fixture
def live():
    return C.load_live()


def test_positive_controls(live):
    assert C.controls(live) == 11


@pytest.mark.parametrize("reference", [
    "rekey_summary_oct07.csv", "generation_results_oct07.csv",
    "../infra/immigration-fiscal/example/derived/oct07/results.csv",
    "example/derived/oct07/", "main_case_2026_10_07/derived/summary.json",
])
def test_current_citations_flag_with_original_line_and_reference(live, reference):
    rows = C.scan_text("synthetic.md", f"# Current\n\nThe estimate uses `{reference}`.\n", live)
    assert len(rows) == 1
    assert rows[0]["line"] == 3
    assert rows[0]["key"] == "oct07"
    assert rows[0]["reference"] == reference


@pytest.mark.parametrize("text", [
    "The October 7 case's estimate uses `rekey_summary_oct07.csv`.",
    "The earlier case uses `rekey_summary_oct07.csv`.",
    "The estimate was in `rekey_summary_oct07.csv`.",
    "On 2026-10-07 the estimate used `rekey_summary_oct07.csv`.",
    "The October 7 case's estimate uses\n`rekey_summary_oct07.csv`.",
    "[Superseded: `rekey_summary_oct07.csv`] The estimate is current.",
    "## Revisions\n\n`rekey_summary_oct07.csv`\n\n### Detail\n`generation_results_oct07.csv`",
    "```python\nrekey_summary_oct07.csv\n```\n<!-- rekey_summary_oct07.csv -->",
    "The estimate uses `rekey_summary_oct14.csv`.",
    "The estimate uses `rekey_summary_oct070.csv`.",
])
def test_records_and_live_references_are_not_flagged(live, text):
    assert C.scan_text("synthetic.md", text, live) == []


def test_revision_mask_ends_at_peer_heading(live):
    text = "## Revisions\n`rekey_summary_oct07.csv`\n## Current\n`rekey_summary_oct07.csv`"
    assert [r["line"] for r in C.scan_text("synthetic.md", text, live)] == [4]


def test_index_case_table_only_is_exempt(live):
    text = ("**Earlier cases.**\n\n| Case | Record |\n|---|---|\n"
            "| October 7 | `rekey_summary_oct07.csv` |\n\n"
            "Current uses `rekey_summary_oct07.csv`.")
    rows = C.scan_text("research/immigration-INDEX.md", text, live)
    assert [r["line"] for r in rows] == [7]


def test_current_marker_overrides_historical_label(live):
    text = "On the October 7 case, now `rekey_summary_oct07.csv` supplies the current figure."
    assert len(C.scan_text("synthetic.md", text, live)) == 1


def test_summary_version_selector(live):
    version_keys = C.versions(C.ROOT)
    rows = C.scan_text("synthetic.md", "Use `summary.json` key `v6` for the current estimate.", live, version_keys)
    assert [(r["key"], r["reference"]) for r in rows] == [("oct07", "summary.json key v6")]
    assert C.scan_text("synthetic.md", "Use `summary.json` key `v7`.", live, version_keys) == []
    assert C.scan_text("synthetic.md", "The earlier case uses `summary.json` key `v6`.", live, version_keys) == []


@pytest.mark.parametrize("reference", [
    "sept24_propagation_2026_09_24/derived/oct14/real_costs_totals.csv",
    "main_case_decomposition_2026_09_29/RESULT.md",
    "oct05/oct07",
])
def test_consumer_lane_date_does_not_date_its_current_output(live, reference):
    assert C.scan_text("synthetic.md", f"The current estimate uses `{reference}`.", live) == []


@pytest.mark.parametrize("tag", ["DATA", "SOURCE", "CALCULATION", "DERIVATION"])
def test_evidence_tags_are_citations_and_nested_record_notes_remain_masked(live, tag):
    text = f"The current estimate is supported by [{tag}: rekey_summary_oct07.csv]."
    assert len(C.scan_text("synthetic.md", text, live)) == 1
    assert C.scan_text("synthetic.md", f"[Superseded: {text} More record text.]", live) == []
    assert C.scan_text("synthetic.md", f"## Revisions\n{text}", live) == []


@pytest.mark.parametrize("text", [
    "The October 7 source was replaced; the current estimate is supported by `rekey_summary_oct07.csv`.",
    "The current estimate is supported by `rekey_summary_oct07.csv`; the October 7 source was replaced.",
    "The October 7 case's source supplies the current estimate in `rekey_summary_oct07.csv`.",
])
def test_current_clause_cannot_inherit_history(live, text):
    assert len(C.scan_text("synthetic.md", text, live)) == 1


def fake_repo(tmp_path, live):
    manifest = tmp_path / C.MANIFEST
    manifest.parent.mkdir(parents=True)
    manifest.write_text(json.dumps(live))
    decision = tmp_path / live["decision"]
    decision.parent.mkdir()
    decision.write_text("# Adopted decision\n")
    package = manifest.parent / live["lane"] / "package.cjs"
    package.parent.mkdir()
    values = {"STATUS": "adopted", "CASE_KEY": live["key"], "LANE": live["lane"],
              "ADOPTED": live["adopted"], "DECISION": live["decision"]}
    package.write_text("\n".join(f'const {k} = "{v}";' for k, v in values.items()))
    derived = package.parent / "derived"
    derived.mkdir()
    for filename in ("corrections.json", "corrections_cash.json"):
        (derived / filename).write_text(json.dumps({"meta": {"adopted": live["adopted"],
            "decision": live["decision"], "source": live["lane"] + "/package.cjs"}}))
    return package


@pytest.mark.parametrize("mutation", ["status", "cash", "set", "newer", "order", "key", "missing-key"])
def test_adoption_mismatch_blocks(tmp_path, live, mutation):
    package = fake_repo(tmp_path, live)
    assert C.load_live(tmp_path) == live
    if mutation == "status":
        package.write_text(package.read_text().replace('STATUS = "adopted"', 'STATUS = "candidate"'))
    elif mutation in {"cash", "set"}:
        name = "corrections_cash.json" if mutation == "cash" else "corrections.json"
        payload = package.parent / "derived" / name
        data = json.loads(payload.read_text())
        data["meta"]["adopted"] = "2026-10-07"
        payload.write_text(json.dumps(data))
    elif mutation == "newer":
        newer = package.parent.parent / "main_case_2026_10_15" / "package.cjs"
        newer.parent.mkdir()
        newer.write_text('const STATUS = "adopted";\nconst ADOPTED = "2026-10-15";\n')
    elif mutation == "missing-key":
        (package.parent / "derived" / "missing_oct07.csv").write_text("value\n")
        changed = dict(live, superseded=[k for k in live["superseded"] if k != "oct07"])
        (tmp_path / C.MANIFEST).write_text(json.dumps(changed))
    else:
        changed = dict(live)
        if mutation == "order":
            changed["superseded"] = list(reversed(changed["superseded"]))
        else:
            changed["key"] = "oct07"
        (tmp_path / C.MANIFEST).write_text(json.dumps(changed))
    with pytest.raises(ValueError, match="BLOCKED"):
        C.load_live(tmp_path)


def test_failed_control_writes_nothing(tmp_path, live, monkeypatch):
    monkeypatch.setattr(C, "load_live", lambda: live)
    monkeypatch.setattr(C, "scan_text", lambda *a, **kw: [])
    target = tmp_path / "must-not-exist"
    with pytest.raises(ValueError, match="control"):
        C.main(["--out", str(target)])
    assert not target.exists()


def test_default_has_no_writes_and_stale_returns_one(tmp_path, live, monkeypatch, capsys):
    monkeypatch.setattr(C, "load_live", lambda: live)
    monkeypatch.setattr(C.M, "memos", lambda _: ([("synthetic.md", "Use `rekey_summary_oct07.csv`.")], []))
    monkeypatch.setattr(C, "ROOT", tmp_path)
    (tmp_path / "CLAUDE.md").write_text("Current guidance.\n")
    assert C.main([]) == 1
    assert "STALE-CITATION synthetic.md:1 oct07" in capsys.readouterr().out
    assert sorted(p.name for p in tmp_path.iterdir()) == ["CLAUDE.md"]
    output = tmp_path / "out"
    assert C.main(["--out", str(output)]) == 1
    content = (output / "citation_freshness.csv").read_bytes()
    assert b"\r\n" not in content
