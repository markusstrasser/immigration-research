"""Produce the item10 own-job keys in a separate physical-footprint-gated process.

Run after export_lines.cjs. The file is an ignored person-key cache; old cases
are read-only. No survey, upstream source, or pinned producer is mutated.
"""
from __future__ import annotations

import hashlib
import json
import tempfile
import time
from pathlib import Path

import numpy as np
import households as H


def main():
    started = time.perf_counter()
    lines_file = H.CACHE / "oct15/lines.json"
    lines = json.loads(lines_file.read_text())
    source = lines["meta"]["union_completion"]
    d = H.load_frame()
    _, union, gens = H.F.masks(d)
    index = {(int(h), int(p)): i for i, (h, p) in enumerate(zip(d.PH_SEQ, d.PPPOS))}
    records = [r for r in source["observed_records"] if not r["observed_nonreporter"]]
    rows = np.array([index[(r["PH_SEQ"], r["PPPOS"])] for r in records])
    if union[rows].any() or len(set(rows)) != len(rows):
        raise SystemExit("[BLOCKED] completion reporter cache overlaps original union")
    weights = d[H.F.REPS].to_numpy(float)
    vectors, national_mass = H.completion_job_vectors(d, weights, rows, gens)
    target = H.CACHE / "oct15/completion_jobs.npz"
    sources = [Path(__file__), H.HERE / "households.py", H.FISCAL / "union_completion_2026_10_14/job_record_key.py"]
    pins = {str(p.relative_to(H.FISCAL)): hashlib.sha256(p.read_bytes()).hexdigest() for p in sources}
    metadata = dict(source_sha256=pins, identities=[[r["PH_SEQ"], r["PPPOS"]] for r in records],
                    national_driver_mass=national_mass,
                    national_driver_rule="source tax national closure times original G3 wage fill-in factor; no member-only denominator")
    staged = []
    try:
        with tempfile.NamedTemporaryFile(mode="w+b", dir=target.parent, suffix=".npz", delete=False) as stream:
            staged.append(Path(stream.name))
            np.savez_compressed(stream, rows=rows, **{key: v[rows] for key, v in vectors.items()})
        with tempfile.NamedTemporaryFile(mode="w", dir=target.parent, suffix=".json", delete=False) as stream:
            staged.append(Path(stream.name))
            stream.write(json.dumps(metadata, indent=2) + "\n")
        peak = H.require_within_budget("completion own-job keys producer")
        staged[0].replace(target)
        staged[1].replace(target.with_suffix(".json"))
    finally:
        for path in staged:
            path.unlink(missing_ok=True)
    print(json.dumps(dict(elapsed_seconds=time.perf_counter() - started, physical_footprint_bytes=peak)))


if __name__ == "__main__":
    main()
