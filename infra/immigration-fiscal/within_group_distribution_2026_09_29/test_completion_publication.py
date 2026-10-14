"""A failed own-job memory gate cannot replace either shared cache file."""
import json

import numpy as np
import pandas as pd
import pytest

import completion_keys as C


def test_failed_budget_preserves_job_vectors_and_receipt(tmp_path, monkeypatch):
    cache = tmp_path / "oct15"
    cache.mkdir()
    (cache / "lines.json").write_text(json.dumps({"meta": {"union_completion": {"observed_records": [
        {"PH_SEQ": 2, "PPPOS": 1, "observed_nonreporter": False}]}}}))
    target, receipt = cache / "completion_jobs.npz", cache / "completion_jobs.json"
    target.write_bytes(b"prior vectors")
    receipt.write_bytes(b"prior receipt")
    d = pd.DataFrame({"PH_SEQ": [1, 2], "PPPOS": [1, 1], **{k: [1, 1] for k in C.H.F.REPS}})
    monkeypatch.setattr(C.H, "CACHE", tmp_path)
    monkeypatch.setattr(C.H, "load_frame", lambda: d)
    monkeypatch.setattr(C.H.F, "masks", lambda frame: (np.ones(2, bool), np.array([True, False]), {}))
    monkeypatch.setattr(C.H, "completion_job_vectors", lambda *args: ({"corporate": np.array([1., 2.])}, {"corporate": 3.}))

    def blocked(*args):
        raise SystemExit("[BLOCKED] publication budget regression")

    monkeypatch.setattr(C.H, "require_within_budget", blocked)
    with pytest.raises(SystemExit, match="publication budget regression"):
        C.main()
    assert target.read_bytes() == b"prior vectors"
    assert receipt.read_bytes() == b"prior receipt"
    assert {p.name for p in cache.iterdir()} == {"lines.json", "completion_jobs.npz", "completion_jobs.json"}
