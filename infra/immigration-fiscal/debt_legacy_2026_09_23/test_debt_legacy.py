"""Permanent gates: `debt_legacy.py --case sept23`, `--case sept24`, `--case sept26` and `--case sept26_schools`
rebuild the files committed for those historical cases byte for byte; sept27 rebuilds the unkeyed derived/ files,
`--case sept29` rebuilds derived/sept29/, `--case oct05` derived/oct05/; the live default/oct14 rebuilds derived/oct14/.

Since 2026-10-14 the default run is oct14; sept27 explicitly rebuilds the old unkeyed directory. Earlier files are
the ones committed at its commit below, the last commit whose derived/ held that run. The ledger lane
(winners_losers_2026_09_24) rebuilds its September 23 reference this way, so this must keep passing.

Run from the repository root:
  OPENBLAS_NUM_THREADS=1 uv run --no-project python3 -m pytest infra/immigration-fiscal/debt_legacy_2026_09_23/ -q --import-mode=importlib
"""
from __future__ import annotations

import os
import copy
import importlib.util
import json
import hashlib
import subprocess
import sys
from pathlib import Path

import pytest

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
SEPT23_COMMIT = "96a5c3b"
SEPT24_COMMIT = "ed1b623"
SEPT26_COMMIT = "e62fccb"
SCHOOLS_COMMIT = "90c4b23"
DERIVED = "infra/immigration-fiscal/debt_legacy_2026_09_23/derived"


def git(*args: str) -> bytes:
    return subprocess.run(["git", *args], cwd=ROOT, capture_output=True, check=True).stdout


def rebuild(tmp_path: Path, *args: str) -> None:
    run = subprocess.run([sys.executable, str(HERE / "debt_legacy.py"), *args, "--out-dir", str(tmp_path)],
                         cwd=ROOT, env={**os.environ, "OPENBLAS_NUM_THREADS": "1"}, capture_output=True, text=True)
    assert run.returncode == 0, run.stderr[-2000:]


def archival_replay_matches(got: Path, archived: Path) -> bool:
    """Historical CSVs and summary bytes stay exact apart from the current supplier's truthful code hash.

    c94314c5 added the shared consumer's missing-capital guard after these archives were recorded. Its numerical
    replay is unchanged; the regenerated provenance must name the current file, not fake the archived hash.
    """
    actual, expected = got.read_bytes(), archived.read_bytes()
    if actual == expected or got.name != "summary.json":
        return actual == expected
    current = json.loads(actual)["case"]["v4"]["consumer"]
    old = json.loads(expected)["case"]["v4"]["consumer"]
    if current["file"] != old["file"]:
        return False
    actual_hash = hashlib.sha256((ROOT / current["file"]).read_bytes()).hexdigest()
    if current["sha256"] != actual_hash or actual.count(actual_hash.encode()) != 1:
        return False
    return actual.replace(actual_hash.encode(), old["sha256"].encode(), 1) == expected


@pytest.mark.parametrize("case, commit, count", [("sept23", SEPT23_COMMIT, 10), ("sept24", SEPT24_COMMIT, 12),
                                                 ("sept26", SEPT26_COMMIT, 13), ("sept26_schools", SCHOOLS_COMMIT, 14)])
def test_old_case_rebuilds_committed_files(tmp_path, case, commit, count):
    names = git("ls-tree", "--name-only", f"{commit}:{DERIVED}").decode().split()
    assert len(names) == count, names
    rebuild(tmp_path, "--case", case)
    differ = [n for n in names if (tmp_path / n).read_bytes() != git("show", f"{commit}:{DERIVED}/{n}")]
    assert not differ, differ


def test_sept27_rebuilds_derived(tmp_path):
    names = sorted(p.name for p in (HERE / "derived").iterdir() if p.is_file())
    assert len(names) == 15, names
    rebuild(tmp_path, "--case", "sept27")
    assert sorted(p.name for p in tmp_path.iterdir()) == names
    differ = [n for n in names if (tmp_path / n).read_bytes() != (HERE / "derived" / n).read_bytes()]
    assert not differ, differ


def test_sept29_rebuilds_its_directory(tmp_path):
    """The main case of 2026-09-29 writes derived/sept29/: the default run's files for its case, plus the bridge
    from September 27."""
    names = sorted(p.name for p in (HERE / "derived" / "sept29").iterdir())
    default = sorted(p.name for p in (HERE / "derived").iterdir() if p.is_file())
    assert names == sorted(default + ["sept29_bridge_2024.csv"]), names
    rebuild(tmp_path, "--case", "sept29")
    assert sorted(p.name for p in tmp_path.iterdir()) == names
    differ = [n for n in names if not archival_replay_matches(tmp_path / n, HERE / "derived" / "sept29" / n)]
    assert not differ, differ


def test_oct05_rebuilds_its_directory(tmp_path):
    """The main case of 2026-10-05 (v5) writes derived/oct05/: September 29's files for its case, plus the bridge from
    September 29. The earlier cases' bridges there are September 29's, byte for byte."""
    names = sorted(p.name for p in (HERE / "derived" / "oct05").iterdir())
    sept29 = sorted(p.name for p in (HERE / "derived" / "sept29").iterdir())
    assert names == sorted(sept29 + ["oct05_bridge_2024.csv"]), names
    rebuild(tmp_path, "--case", "oct05")
    assert sorted(p.name for p in tmp_path.iterdir()) == names
    differ = [n for n in names if not archival_replay_matches(tmp_path / n, HERE / "derived" / "oct05" / n)]
    assert not differ, differ
    bridges = [n for n in sept29 if n.endswith("_bridge_2024.csv")]
    assert len(bridges) == 4, bridges
    moved = [n for n in bridges if (tmp_path / n).read_bytes() != (HERE / "derived" / "sept29" / n).read_bytes()]
    assert not moved, moved


def test_oct14_rebuilds_its_directory(tmp_path):
    """The live v7 default keeps dated files intact and adds its allocation/item bridge."""
    names = sorted(p.name for p in (HERE / "derived" / "oct14").iterdir())
    oct07 = sorted(p.name for p in (HERE / "derived" / "oct07").iterdir())
    assert names == sorted(oct07 + ["oct14_bridge_2024.csv"]), names
    rebuild(tmp_path)
    assert sorted(p.name for p in tmp_path.iterdir()) == names
    differ = [n for n in names if (tmp_path / n).read_bytes() != (HERE / "derived" / "oct14" / n).read_bytes()]
    assert not differ, differ
    bridges = [n for n in oct07 if n.endswith("_bridge_2024.csv")]
    assert len(bridges) == 6, bridges
    moved = [n for n in bridges if (tmp_path / n).read_bytes() != (HERE / "derived" / "oct07" / n).read_bytes()]
    assert not moved, moved


@pytest.fixture
def debt_module():
    spec = importlib.util.spec_from_file_location("debt_contract", HERE / "debt_legacy.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_v7_contract_personal_band_and_receipt_readings(debt_module):
    d = debt_module
    payload = json.loads(d.payload_file("oct14").read_text())
    meta = payload["meta"]
    corners = d.frame_corners(d.main_profile("oct14"), d.MODEL, meta["responses"], "oct14", meta)
    assert len(corners) == 32 and {c["allocation"] for c in corners} == {"personal"}
    all_corners = d.frame_corners(d.main_profile("oct14"), d.MODEL, meta["responses"], "oct14", meta,
                                 all_allocations=True)
    assert len(all_corners) == 64
    for c in corners:
        for line in d.JOB_CAPITAL_LINES:
            assert c["line_responses"]["receipt:" + line] == meta["responses"][line][c["reading"]]


def test_v7_contract_case_oracle_reads_set_cash_ends(debt_module):
    d = debt_module
    oracle = d.case_oracle("oct14")
    summary = json.loads(d.case_file("oct14", "summary.json").read_text())["v7"]
    assert oracle["ends"] == summary["end_specifications"]["set"] == [16, 11]
    assert oracle["set"] == summary["band_bn"]
    assert oracle["cash"] == summary["cash_set_bn"]


def test_v7_contract_other_production_collecting_government(debt_module):
    d = debt_module
    wb = d.Workbook(d.BEA / "Section3All_xls.xlsx")
    shares = {c: d.pd.DataFrame(index=d.YEARS) for c in d.CONVENTIONS}
    d.job_capital_shares(shares, wb)
    fed, sl = wb.cells(d.OTHER_PRODUCTION_FED), wb.cells(d.OTHER_PRODUCTION_SL)
    assert abs((fed + sl)[2024] - 145.258) < 1e-9
    assert abs(fed[2024] - wb.line("T30500-A", 16)[2024] - wb.line("T30500-A", 17)[2024]) < 1e-12
    assert abs(shares["central"].loc[2024, "other_production_taxes"] - fed[2024] / 145.258) < 1e-12
    assert d.RECEIPT_SERIES_V7["other_production_taxes"] == (d.OTHER_PRODUCTION_FED, d.OTHER_PRODUCTION_SL)


def test_v7_contract_grouped_receipts_close_at_2024(debt_module):
    d = debt_module
    payload = json.loads(d.payload_file("oct14").read_text())
    meta = payload["meta"]
    model = d.apply_corrections(d.MODEL, payload)
    c = d.frame_corners(d.main_profile("oct14"), model, meta["responses"], "oct14", meta)[0]
    t = d.lines_at(c).set_index("id")
    rec = t[(t.side == "receipt") & ~t.index.isin(c["capped"]) & ~t.index.isin(d.SIGNED_RECEIPTS_V4)]
    audit = sum(d.grouped(rec.responsive_bn, names) for names in d.RECEIPT_GROUPS.values())
    assert abs(audit - rec.responsive_bn.sum()) < 1e-9
    assert {"corporate_capital", "corporate_labor"} <= set(d.RECEIPT_GROUPS[5])
    assert {"remaining_production_property", "other_production_taxes"} <= set(d.RECEIPT_GROUPS[4])


@pytest.mark.parametrize("defect", ["extra_response", "inherited_response", "wrong_override", "wrong_reading",
                                   "allocation_edits"])
def test_v7_contract_stops_on_unapproved_changes(debt_module, defect):
    d = debt_module
    payload = copy.deepcopy(json.loads(d.payload_file("oct14").read_text()))
    if defect == "extra_response":
        payload["meta"]["responses"]["invented_receipt"] = {"receipt": True, "low": 1, "high": 1}
    elif defect == "inherited_response":
        payload["meta"]["responses"]["housing_subsidies"]["low"] = 0.99
    elif defect == "wrong_override":
        payload["meta"]["responses"]["corporate_capital"]["override"] = "receipt:corporate_labor"
    elif defect == "wrong_reading":
        payload["meta"]["responses"]["corporate_capital"]["high"] = 1
    else:
        next(it for it in payload["meta"]["items"] if it["kind"] == "allocation")["edits"]["count"] = 1
    with pytest.raises(SystemExit, match="allocation item|responses|job-capital response"):
        d.v6_parts("oct14", payload)
