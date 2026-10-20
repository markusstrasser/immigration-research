"""Declared byte-preserving record relocations; recorded hashes stay authoritative."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
RELOCATIONS = json.loads(Path(__file__).with_name("historical_record_paths.json").read_text())


def relocated_record(path):
    path = Path(path)
    absolute = path.resolve()
    try:
        relative = str(absolute.relative_to(ROOT))
    except ValueError:
        return path
    return ROOT / RELOCATIONS[relative] if relative in RELOCATIONS else path
