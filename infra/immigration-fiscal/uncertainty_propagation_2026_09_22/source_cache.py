"""Verify the rederivable all-specification payload against its tracked pin."""
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
CACHE = HERE / "_cache/oct16/spec_sources.json"
MANIFEST = HERE / "derived/oct16/spec_sources_manifest.json"


def load_sources(cache=CACHE, manifest=MANIFEST):
    if not manifest.is_file():
        raise ValueError("[BLOCKED] oct16 source manifest missing; run sept24_specs.cjs")
    pin = json.loads(manifest.read_text())
    if pin["path"] != str(CACHE.relative_to(ROOT)):
        raise ValueError("[BLOCKED] oct16 source cache path differs from manifest")
    if not cache.is_file():
        raise ValueError("[BLOCKED] oct16 source cache missing; run sept24_specs.cjs")
    content = cache.read_bytes()
    if len(content) != pin["bytes"] or hashlib.sha256(content).hexdigest() != pin["sha256"]:
        raise ValueError("[BLOCKED] oct16 source cache differs from tracked manifest")
    return json.loads(content)
