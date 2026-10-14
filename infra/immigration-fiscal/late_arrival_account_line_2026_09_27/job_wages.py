"""oct14's authorized within-G1 wage fallback on this lane's existing records.

INDUSTRY (longest job) is absent here. PEIOIND and A_DTIND are different
instruments and cannot silently replace it. All WSAL_VAL, including off-books
wages, enters. The job-capital lane's common G1 fill-in multiplier cancels
in the within-G1 ratio. Spreading $1M wages across industries preserves each
cell's total wages; under the authorized common-industry-mix approximation
those totals alone determine the share. Both assignment conventions are kept.
"""
import json
import sys
from pathlib import Path
import numpy as np

import frame as F


def main():
    d = F.load()
    if "INDUSTRY" in d.columns:
        raise SystemExit("[BLOCKED] industry is available: implement the industry rule")
    civ, union, gens = F.masks(d)
    omega, _, _ = F.assignments(d, civ, union, gens)
    w = d.pwwgt0.to_numpy(float).copy()
    row4 = json.loads((F.FISCAL / "main_case_candidate_2026_09_28/derived/production_row4.json").read_text())
    for name, status in (("naturalized", 4), ("noncitizen", 5)):
        mask = d.PENATVTY.eq(303) & d.PRCITSHP.eq(status) & ~d.GESTFIPS.isin([6, 48])
        ref = row4["row4_factors"][name]
        if abs(w[mask].sum() - ref["cps_population"]) >= 1e-6:
            raise SystemExit("[BLOCKED] job wages: row4 frame differs")
        w[mask] *= ref["factor"]
    if abs(w[union].sum() - row4["populations"]["row4"]) >= 1e-3:
        raise SystemExit("[BLOCKED] job wages: union population differs")
    wage = d.WSAL_VAL.clip(lower=0).to_numpy(float)
    out = {"def": F.LATE_DEF, "rule": "[APPROX: industry mix within G1 not measured by cell]",
           "industry_field": "INDUSTRY absent; PEIOIND/A_DTIND not substituted",
           "wages": {}, "shares": {}}
    unit = F.C.spm_index(d)
    vectors = {"personal": wage, "shared": F.C.unit_equal(wage, unit)}
    for conv, om in omega.items():
        out["wages"][conv], out["shares"][conv] = {}, {}
        for allocation, vector in vectors.items():
            values = F.totals(vector, w, om)[:len(F.G1_CELLS)]
            shares = values / values.sum()
            if not np.isfinite(shares).all() or abs(shares.sum() - 1) >= 1e-12:
                raise SystemExit("[BLOCKED] invalid G1 wage shares")
            out["wages"][conv][allocation] = dict(zip(F.G1_CELLS, values.tolist()))
            out["shares"][conv][allocation] = dict(zip(F.G1_CELLS, shares.tolist()))
    F.OUT.mkdir(parents=True, exist_ok=True)
    sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
    from memory_budget import require_within_budget
    print(f"footprint bytes: {require_within_budget('late arrival wages')}")
    (F.OUT / "job_wages_oct15.json").write_text(json.dumps(out, indent=1) + "\n")
    print(f"job wages {F.LATE_DEF}: both shares close (1e-12); {out['rule']}")


if __name__ == "__main__":
    main()
