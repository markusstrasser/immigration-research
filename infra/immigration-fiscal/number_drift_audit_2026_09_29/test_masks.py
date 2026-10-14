"""Regression checks for the audit's masks (audit_numbers.mask).

    uv run --no-project --offline python3 -m pytest infra/immigration-fiscal/number_drift_audit_2026_09_29/ -q
"""
import subprocess
import sys
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
import audit_numbers as A  # noqa: E402


def raws(text):
    return [t[2] for t in A.tokens(text)]


def test_an_all_digit_hash_is_masked_only_when_it_names_a_commit():
    # After 9e316341 the INDEX cited 73934145 and "audit 4827413"; both met the audit as unsourced quantities.
    hashes = subprocess.run(["git", "-C", str(A.ROOT), "rev-list", "--all"], capture_output=True, text=True,
                            check=True).stdout.split()
    commit = next(h[:8] for h in hashes if h[:8].isdigit())
    other = next(str(n) for n in range(10_000_000, 10_001_000) if not any(h.startswith(str(n)) for h in hashes))
    assert raws(f"audit {commit} §A, {other} people") == [other]
    # digits inside a decimal or a comma-grouped number are never read as a hash
    assert raws(f"0.{commit[:7]}") == [f"0.{commit[:7]}"]
    assert raws("39,712,493 people") == ["39,712,493"]
