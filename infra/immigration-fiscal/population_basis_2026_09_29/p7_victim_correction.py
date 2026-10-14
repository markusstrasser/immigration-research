"""Live-case victim correction, alongside the unchanged historical restatement.

Low already contains the NCVS mixed-group correction. High must apply that
correction under its own custody ratio. Consume the victim lane's matched
arms; every other historical row is copied byte-identically into the audit
comparison and is never recomputed. This payload only changes victim harm;
fear, security and the lineage boundary belong to the live-case consumer.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import resource
import time

import pandas as pd

HERE = Path(__file__).resolve().parent
FISCAL = HERE.parent
OUT = HERE / "derived"
VICTIM = FISCAL / "crime_victim_cost_2026_09_23/derived"


def gate(name, ok):
    if not ok:
        raise ValueError(f"[BLOCKED] {name}")
    print(f"PASS {name}")


def correction_rows() -> pd.DataFrame:
    restated = pd.read_csv(OUT / "restated_pairing.csv")
    victim_rows = restated[restated.section.eq("row") & restated.item.eq("victims")].set_index("end")
    arms = pd.read_csv(VICTIM / "mortality_arms.csv")
    arms = arms[arms.real_discount_rate.eq(0.0) & arms.missing_age_arm.eq("central")]
    arms = arms.set_index(["footing", "vsl_standard"])
    old = pd.read_csv(VICTIM / "arms.csv").set_index("arm")
    gate("positive control low already carries mixed groups", abs(arms.loc[("mixed", "legacy"), "full_bn"] - victim_rows.loc["low", "published"]) < 1e-6)
    gate("positive control high is the original custody arm", abs(victim_rows.loc["high", "published"] - old.loc["scaling: ACS institutional ratio 1.118 (generic reallocated)", "full_bn"]) < 1e-9)
    rows = []
    # Exactly the historical factor, as computed by the authoritative basis producer.
    basis = pd.read_csv(HERE / "basis.csv")
    factors = basis[basis.row.eq("victims")].set_index("end").factor
    for standard in ("legacy", "dot_uniform", "dot_life_years"):
        for end, footing in (("low", "mixed"), ("high", "custody")):
            previous = float(victim_rows.loc[end, "restated"])
            factor = float(factors[end])
            full = float(arms.loc[(footing, standard), "full_bn"])
            corrected = full * factor
            delta = corrected - previous
            if standard == "legacy" and end == "low":
                gate("low reproduces historical value within 1e-6bn", abs(corrected - previous) < 1e-6)
                # The historical source/receipt are rounded independently.
                # Keep its already-correct receipt exactly, after the control.
                corrected, delta = previous, 0.0
            rows.append(dict(case="oct14", end=end, footing=footing, vsl_standard=standard,
                             published_weights_bn=full, factor=factor, row4_bn=corrected,
                             previous_row4_bn=previous, delta_row4_bn=delta,
                             measure="absolute", comparator="with_without", beneficiary_population="other US residents outside the identified union",
                             valuation_basis=standard, overlap_set="victim_harm_excludes_fear_security_CJS",
                             scope="39.71M identified union; descendant boundary and fear integration in the consumer"))
    return pd.DataFrame(rows)


def main():
    started = time.perf_counter()
    historical_path = OUT / "restated_pairing.csv"
    previous_bytes = historical_path.read_bytes()
    rows = correction_rows()
    rows.to_csv(OUT / "restated_victims_oct14.csv", index=False, float_format="%.10f", lineterminator="\n")
    payload = dict(case="oct14", historical_restatement_sha256=hashlib.sha256(previous_bytes).hexdigest(),
                   rows=rows.to_dict(orient="records"),
                   uncertainty="NCVS mixed-group correction has no replicate covariance here; custody is an institutional-residence sensitivity, not identified offending")
    (OUT / "victim_correction_oct14.json").write_text(json.dumps(payload, indent=2) + "\n")
    gate("historical restatement byte-identical", historical_path.read_bytes() == previous_bytes)
    print(rows[["end", "vsl_standard", "row4_bn", "previous_row4_bn", "delta_row4_bn"]].to_string(index=False))
    print(f"Elapsed seconds: {time.perf_counter() - started:.3f}; peak RSS bytes: {resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}")


if __name__ == "__main__":
    main()
