#!/usr/bin/env python3
"""The age-mix re-pricing of v5's lineage line: point values from price.cjs, sampling spread from draws of the band rates.

The engine-key route is linear in the mix (price.cjs gate), so a draw's change at an end is
  later x sum_b (piL_b - pi_b) G_b + (1 - C3) g3 x sum_b (pi3_b - pi_b) G_b + C3 g3 x sum_b (pi3_b - pi_b) W_b
with G_b, W_b the unit-band costs of a G3+ member and a third-plus white at the end (W through the white lane's
reweighting, linear to a constant $3-4 a person that cancels in the difference). Draws re-sample the band loss rates
only: each band's rate from normal(rate, se) independently (age_mix.py's rates and linearised SEs, clipped to
[1e-4, 0.9]), mixed by age_mix.py's rule; the identified mix, the counts, C3 and the per-band costs are held.
Gates (exit 1): the draws' formula at each reading's point mixes reproduces price.cjs's change within $1m (the W
residual nearly cancels: 1e-7 to 7e-4 bn); the flat reading is zero. Points are price.cjs's; draws give the spread.
Outputs: derived/age_mix_bands.csv (reading x set: band at 48 / 11, change, SE, 5-95%), derived/summary.json
Run from the repository root after price.cjs:
  OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/added_age_mix_2026_10_07/summarize.py
"""
from __future__ import annotations

import csv
import json
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
OUT = HERE / "derived"
CENTRAL = "cross_section_2007_2026"
DRAWS = 2000
SEED = 20261007
GATES: list[dict] = []


def gate(name: str, ok: bool, detail: str = "") -> None:
    GATES.append({"gate": name, "passed": bool(ok), "detail": detail})
    print(f"  {'PASS' if ok else 'FAIL'} {name}{' - ' + detail if detail else ''}", flush=True)


def draws(x: dict, pi: np.ndarray, rng: np.random.Generator) -> tuple[np.ndarray, np.ndarray]:
    """DRAWS mixes of each part: the band rates re-drawn, hidden(a) = N(a) [x G4+ share] x L / (1 - L), normalised."""
    out = []
    for rate, se, w4 in ((x["g3anc_rate"], x["g3anc_se"], None), (x["g4anc_rate"], x["g4anc_se"], x.get("g4_share"))):
        d = np.clip(rng.normal(np.array(rate), np.array(se), (DRAWS, len(pi))), 1e-4, 0.9)
        h = pi * (np.array(w4) if w4 is not None else 1.0) * d / (1 - d)
        out.append(h / h.sum(axis=1, keepdims=True))
    return out[0], out[1]


def main() -> None:
    P = json.loads((OUT / "price_summary.json").read_text())
    M = json.loads((OUT / "age_mix.json").read_text())
    meta = P["meta"]
    c3, g3, later = meta["c3"], meta["g3_rate"], meta["later"]
    pi = np.array(M["meta"]["identified"])
    nb = len(pi)
    rows, out = [], {"meta": {"source": "added_age_mix_2026_10_07/summarize.py", "central_reading": CENTRAL,
                              "route": meta["central_route"], "ends": None, "draws": DRAWS, "seed": SEED}, "sets": {}}
    for s, S in P["sets"].items():
        ends = S["ends"]
        out["meta"]["ends"] = ends
        G = np.array([S["unit_bands"]["keys"][f"band|{b}"]["g3plus_member_bn"] for b in range(nb)])   # nb x 2 ends
        W = np.array([S["unit_bands"]["white"][f"band|{b}"] for b in range(nb)])

        def change(m3, mL):
            d3, dL = m3 - pi, mL - pi
            return later * dL @ G + (1 - c3) * g3 * d3 @ G + c3 * g3 * d3 @ W

        out["sets"][s] = {"v5_band_bn": S["v5_band_bn"], "readings": {}}
        rows.append({"set": s, "reading": "flat (v5)", "low_bn": S["v5_band_bn"][0], "high_bn": S["v5_band_bn"][1],
                     "change_low_bn": 0.0, "change_high_bn": 0.0, "se_low_bn": 0.0, "se_high_bn": 0.0,
                     "p05_low_bn": 0.0, "p95_low_bn": 0.0, "p05_high_bn": 0.0, "p95_high_bn": 0.0,
                     "added_per_person_low_usd": None, "added_per_person_high_usd": None})
        gate(f"{s}: the flat reading's change is zero", np.abs(change(pi, pi)).max() == 0.0)
        for r, x in M["readings"].items():
            if r == "flat":
                continue
            point = np.array(S["readings"]["keys"][r]["change_bn"])
            lin = change(np.array(x["g3_rate"]), np.array(x["later"]))
            gate(f"{s} {r}: the draws' formula at the point mixes is price.cjs's change ($1m: W's reweighting is linear "
                 "only to a few cents a person across mixes)", np.abs(lin - point).max() < 1e-3, f"{np.abs(lin - point).max():.1e}")
            D3, DL = draws(x, pi, np.random.default_rng([SEED, list(M["readings"]).index(r)]))
            dr = later * (DL - pi) @ G + (1 - c3) * g3 * (D3 - pi) @ G + c3 * g3 * (D3 - pi) @ W     # draws x 2
            se = dr.std(axis=0, ddof=1)
            p05, p95 = np.percentile(dr, 5, axis=0), np.percentile(dr, 95, axis=0)
            band = S["readings"]["keys"][r]["band_bn"]
            rr = S["readings"]["keys"][r]
            out["sets"][s]["readings"][r] = {"band_bn": band, "change_bn": point.tolist(), "se_bn": se.tolist(),
                                             "p05_bn": p05.tolist(), "p95_bn": p95.tolist(),
                                             "change_by_part_bn": rr["change_by_part_bn"],
                                             "added_per_person_usd": rr["added_per_person_usd"],
                                             "per_member_usd": rr["per_member_usd"], "own_ends": rr["own_ends"],
                                             "rough_route_change_bn": S["readings"]["rough"][r]["change_bn"]}
            rows.append({"set": s, "reading": r, "low_bn": band[0], "high_bn": band[1], "change_low_bn": point[0],
                         "change_high_bn": point[1], "se_low_bn": se[0], "se_high_bn": se[1], "p05_low_bn": p05[0],
                         "p95_low_bn": p95[0], "p05_high_bn": p05[1], "p95_high_bn": p95[1],
                         "added_per_person_low_usd": rr["added_per_person_usd"][0],
                         "added_per_person_high_usd": rr["added_per_person_usd"][1]})
        # v5's own added person, for the per-person comparison.
        out["sets"][s]["v5_added_per_person_usd"] = [
            (S["v5_band_bn"][j] - S["union_at_new_responses_bn"][j]) * 1e9 / meta["added"] for j in (0, 1)]
    if not all(g["passed"] for g in GATES):
        raise SystemExit(f"[BLOCKED] {sum(not g['passed'] for g in GATES)} gate(s) failed; nothing written")
    with open(OUT / "age_mix_bands.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]), lineterminator="\n")
        w.writeheader()
        for r in rows:
            w.writerow({k: (f"{v:.6f}" if isinstance(v, float) else v) for k, v in r.items()})
    out["gates"] = GATES
    (OUT / "summary.json").write_text(json.dumps(out, indent=1) + "\n")
    for r in rows:
        print(f"  {r['set']:<4} {r['reading']:<26} {r['low_bn']:.2f} / {r['high_bn']:.2f}  change {r['change_low_bn']:+.2f} "
              f"({r['se_low_bn']:.2f}) / {r['change_high_bn']:+.2f} ({r['se_high_bn']:.2f})")


if __name__ == "__main__":
    main()
