#!/usr/bin/env python3
"""Checks for this lane: pins, quotes, a full rerun, byte-identical outputs and the RESULT's headline numbers.

1. Every raw source matches its sha256 pin (acquire.py; measure_shares.py pins the ASEC files it reads in
   place from other lanes).
2. Every quote in reads/quotes.json is a substring of its cached source, after HTML entities and page
   markers are removed and whitespace is collapsed on both sides.
3. measure_shares.py and backcast_measured.py rerun into a temporary directory and exit 0. Their gates are
   assertions inside them: the ASEC 2025 run reproduces the account's 24 incidence keys, the Census EIP_CRD
   is rebuilt exactly from each tax unit before any SSN rule, the validation lane's union SNAP, SS and SSI
   are reproduced, the published back-cast's transfers and windows are reproduced, and the debt-legacy
   annual gaps add to its published windows.
4. Every file the rerun writes is byte-identical to the one in derived/.
5. The headline numbers quoted in RESULT.md match derived/.

Run from the repository root (about half a minute; --quick skips steps 3 and 4):
  OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/backcast_pandemic_measured_2026_09_28/verify.py
"""
from __future__ import annotations

import argparse
import filecmp
import html
import json
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

import pandas as pd

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
OUT = HERE / "derived"
SCRIPTS = ("measure_shares.py", "backcast_measured.py")


def norm(s: str) -> str:
    return re.sub(r"\s+", " ", s).strip()


def source_text(path: Path) -> str:
    text = path.read_text(encoding="utf-8", errors="replace")
    if path.suffix == ".htm":
        text = re.sub(r"\[\[Page [^\]]*\]\]", "", html.unescape(text))
    return norm(text)


def check_pins() -> None:
    sys.path.insert(0, str(HERE))
    import acquire
    import measure_shares
    digests = acquire.main()
    for year, (path, pin) in measure_shares.SOURCES.items():
        assert measure_shares.sha(path) == pin, (year, path)
    print(f"  ✓ {len(digests)} cached sources and {len(measure_shares.SOURCES)} ASEC files match their pins")


def check_quotes() -> None:
    quotes = json.loads((HERE / "reads/quotes.json").read_text())
    texts: dict[str, str] = {}
    missing = []
    for q in quotes:
        if q["file"] not in texts:
            texts[q["file"]] = source_text(HERE / q["file"])
        if norm(q["quote"]) not in texts[q["file"]]:
            missing.append(q["id"])
    assert not missing, missing
    print(f"  ✓ reads/quotes.json: {len(quotes)} of {len(quotes)} quotes found in their sources")


def rerun() -> None:
    env = dict(os.environ, OPENBLAS_NUM_THREADS="1")
    with tempfile.TemporaryDirectory() as tmp:
        for script in SCRIPTS:
            done = subprocess.run([sys.executable, str(HERE / script), "--out-dir", tmp], cwd=ROOT, env=env,
                                  capture_output=True, text=True)
            assert done.returncode == 0, (script, done.returncode, done.stdout[-2000:], done.stderr[-2000:])
            print(f"  ✓ {script} reran, rc 0")
        written = sorted(p.name for p in Path(tmp).iterdir())
        kept = sorted(p.name for p in OUT.iterdir() if p.is_file())
        assert written == kept, (written, kept)
        differ = [name for name in written if not filecmp.cmp(Path(tmp) / name, OUT / name, shallow=False)]
        assert not differ, differ
        print(f"  ✓ {len(written)} derived files byte-identical on rerun")


def window(frame: pd.DataFrame, anchor: str, case: str, rule: str, variant: str, status: str,
           name: str = "10y_2015_2024") -> pd.Series:
    row = frame[(frame.anchor == anchor) & (frame["case"] == case) & (frame.rule == rule)
                & (frame.variant == variant) & (frame.status == status) & (frame.window == name)]
    assert len(row) == 1, (anchor, case, rule, variant, status, name)
    return row.iloc[0]


def check_headline() -> None:
    text = (HERE / "RESULT.md").read_text()
    w = pd.read_csv(OUT / "backcast_measured_windows.csv")
    eip = pd.read_csv(OUT / "eip_relative_use.csv").set_index(["allocation", "status", "nipa_year"])
    ratio = pd.read_csv(OUT / "ratio_vs_2024.csv").set_index(["key", "allocation", "income_year"])
    expected = []
    for anchor, case, label in (("sept20", "cbo_informed_low", "low"), ("sept20", "cbo_informed_high", "high"),
                                ("sept27", "main_low", "low"), ("sept27", "main_high", "high")):
        for rule in ("programme", "income"):
            r = window(w, anchor, case, rule, "refundable_pandemic", "borjas")
            lo = window(w, anchor, case, rule, "refundable_pandemic", "borjas_own").new_tn
            hi = window(w, anchor, case, rule, "refundable_pandemic", "modeled").new_tn
            expected += [f"{r.old_tn:.3f} | {r.new_tn:.3f} ({lo:.3f}–{hi:.3f})",
                         f"{100 * r.pandemic_share_old:.1f}% → {100 * r.pandemic_share_new:.1f}%"]
    for status, a in (("borjas", "shared"), ("borjas", "personal"), ("modeled", "shared")):
        expected.append(f"{eip.loc[(a, status, 2020), 'per_person_vs_other_residents']:.2f}")
    expected.append(f"{eip.loc[('shared', 'credit_key_2024', 2024), 'per_person_vs_other_residents']:.2f}")
    expected.append(f"{ratio.loc[('workers_comp', 'shared', 2020), 'ratio_to_2024']:.2f}")
    missing = [e for e in expected if e not in text]
    assert not missing, missing
    print(f"  ✓ RESULT.md: {len(expected)} headline numbers match derived/")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--quick", action="store_true", help="skip the rerun")
    args = parser.parse_args()
    check_pins()
    check_quotes()
    if not args.quick:
        rerun()
    check_headline()


if __name__ == "__main__":
    main()
