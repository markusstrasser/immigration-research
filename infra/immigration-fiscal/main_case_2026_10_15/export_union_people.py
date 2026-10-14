"""Export item 10's observed CPS identities for downstream household routing.

Runs the unchanged source membership and biological-parent rules, never its
writers. Only the v8 derived/ file is written; survey weights are unmodified.
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
from pathlib import Path
import sys
import time

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
FISCAL = HERE.parent
SOURCE = FISCAL / "union_completion_2026_10_14"
sys.path.insert(0, str(SOURCE))
sys.path.insert(0, str(FISCAL / "scripts"))
from completion import masks, siblings
from memory_budget import require_within_budget


def main():
    started = time.perf_counter()
    file = FISCAL / "within_group_distribution_2026_09_29/households.py"
    spec = importlib.util.spec_from_file_location("union_people_kernel", file)
    kernel = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(kernel)
    d = kernel.load_frame()
    civ, union, _, missing, central, _, _ = masks(d, kernel.F)
    arms, mex, parents = siblings(d, kernel.F, civ, union)
    observed = arms["biological"] & ~mex
    records = []
    for row in d.index[missing | observed]:
        native_parent = next((int(p) for p in parents[row] if p >= 0
            and int(d.iloc[p].PENATVTY) in kernel.F.US_AREAS
            and int(d.iloc[p].PRDTHSP) == 1), None)
        grandparent = observed[row] and native_parent is not None and (
            int(d.iloc[native_parent].PEFNTVTY) == 303
            or int(d.iloc[native_parent].PEMNTVTY) == 303)
        records.append(dict(PH_SEQ=int(d.iloc[row].PH_SEQ), PPPOS=int(d.iloc[row].PPPOS),
                            age=int(d.iloc[row].A_AGE), age_band=min(int(d.iloc[row].A_AGE)//5,16),
                            people=float(d.iloc[row].pwwgt0), generation="G3plus",
                            central_reporter=bool(central[row]), broad_reporter=bool(missing[row]),
                            observed_nonreporter=bool(observed[row]),
                            economic_class="g3_rate" if grandparent else "later" if observed[row] else "G3plus"))
    assert len({(r["PH_SEQ"], r["PPPOS"]) for r in records}) == len(records)
    assert sum(r["central_reporter"] for r in records) == 204
    assert sum(r["observed_nonreporter"] for r in records) == 27
    expected = json.loads((SOURCE / "derived/candidate.json").read_text())["counts"]
    got_report = sum(r["people"] for r in records if r["central_reporter"])
    got_loss = sum(r["people"] for r in records if r["observed_nonreporter"])
    assert abs(got_report-expected["reporting_additions"]["central"]["estimate"]) < 1e-6
    assert abs(got_loss-expected["observed_nonreporters"]["estimate"]) < 1e-6
    data = dict(source="union_completion_2026_10_14/completion.py masks/siblings; unchanged pinned CPS frame",
                key=["PH_SEQ", "PPPOS"], counts=dict(central_reporters=got_report, observed_nonreporters=got_loss),
                source_hashes={str(p.relative_to(FISCAL)): hashlib.sha256(p.read_bytes()).hexdigest()
                               for p in [SOURCE/"completion.py", FISCAL/"generation_account_2026_09_24/frame.py"]},
                records=records)
    target = HERE/"derived/union_people.json"
    peak = require_within_budget("union-completion person-key export")
    target.parent.mkdir(exist_ok=True)
    target.write_text(json.dumps(data, indent=2)+"\n")
    print(json.dumps(dict(records=len(records), elapsed_seconds=time.perf_counter()-started, peak_bytes=peak)))


if __name__ == "__main__":
    main()
