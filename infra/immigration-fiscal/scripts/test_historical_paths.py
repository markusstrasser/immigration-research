"""Only declared relocated records resolve, with Python/Node parity and exact bytes."""
import hashlib
import subprocess
from pathlib import Path

from historical_paths import RELOCATIONS, ROOT, relocated_record


def test_relocated_receipt_keeps_recorded_hash_and_both_language_paths():
    old = next(iter(RELOCATIONS))
    expected = ROOT / RELOCATIONS[old]
    assert relocated_record(ROOT / old) == expected
    assert hashlib.sha256(expected.read_bytes()).hexdigest() == "0c788d18fcdf48e4db504334b9ea8af02709f8b6fd416b529019c9d7a7b161e0"
    output = subprocess.check_output(["node", "-e",
        "process.stdout.write(require(process.argv[1]).relocatedRecord(process.argv[2]));",
        str(Path(__file__).with_name("historical_paths.cjs")), str(ROOT / old)], text=True)
    assert output == str(expected)


def test_unknown_or_missing_record_has_no_fallback(tmp_path):
    missing = tmp_path / "missing_record.txt"
    assert relocated_record(missing) == missing
    assert not relocated_record(missing).exists()
    assert relocated_record(ROOT / "unlisted.txt") == ROOT / "unlisted.txt"
