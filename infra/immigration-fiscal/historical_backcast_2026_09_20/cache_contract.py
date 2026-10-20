"""Portable receipt for the rebuildable live annual typed-part table."""
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ANNUAL_CACHE = Path("_cache/oct16/case_parts_annual.csv")
ANNUAL_MANIFEST = Path("derived/oct16/case_parts_annual_manifest.json")
ANNUAL_COLUMNS = ["concept", "rule", "part", "year", "value_bn"]
ANNUAL_KEY = ["concept", "rule", "part", "year"]


def verify_cached_annual(lane_root: Path = HERE) -> Path:
    """Resolve the live full table only after its tracked receipt verifies."""
    manifest_path = lane_root / ANNUAL_MANIFEST
    if not manifest_path.is_file():
        raise ValueError("[BLOCKED] annual parts manifest missing; rerun backcast.py")
    manifest = json.loads(manifest_path.read_text())
    path = lane_root / ANNUAL_CACHE
    if (manifest.get("schema_version") != 1 or manifest.get("case") != "oct16"
            or manifest.get("path") != ANNUAL_CACHE.as_posix()
            or manifest.get("columns") != ANNUAL_COLUMNS or manifest.get("full_key") != ANNUAL_KEY):
        raise ValueError("[BLOCKED] annual parts manifest contract differs")
    if not path.is_file():
        raise ValueError("[BLOCKED] annual parts cache missing; rerun backcast.py")
    digest, size, lines = hashlib.sha256(), 0, 0
    with path.open("rb") as stream:
        header = stream.readline()
        digest.update(header)
        size += len(header)
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
            size += len(chunk)
            lines += chunk.count(b"\n")
    if (header != (",".join(ANNUAL_COLUMNS) + "\n").encode()
            or size != manifest.get("bytes") or lines != manifest.get("rows")
            or digest.hexdigest() != manifest.get("sha256")):
        raise ValueError("[BLOCKED] annual parts cache differs from manifest; rerun backcast.py")
    return path
