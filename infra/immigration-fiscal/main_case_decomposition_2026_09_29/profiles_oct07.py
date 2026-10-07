"""Ages of the people main case v6 adds (`main_case_2026_10_07`, case key `oct07`), in the decomposition's age bins.

v6 keeps v5's 3.04M added people (the payload's meta.lineage.counts) and prices them at their measured age mix (its
item added_age_mix, meta.lineage.age_mix): each count part, the G3-rate persons and the later losses, at its own
five-year mix, on the identified third-plus generation's ages within each band (the engine's G3+ keys reweighted by
band). This script writes the identified G3+ in this lane's bins, as `profiles_oct05.py` does (the generation lane's
G3plus, convention a, on the ASEC person weights, which audit row 4 leaves unchanged for G3+), and the added people in
each bin at the measured mix: the bin's identified G3+ times (f_b - 1), where f_b = 1 + added_b / identified G3+_b in
its five-year band and added_b = the G3-rate persons x their mix_b + the later losses x their mix_b.

Gates (exit 1): the total is the payload's meta.lineage.counts.identified_g3plus (1e-3 persons); every bin holds G3+
members; the bins are the same as g3plus_ages_oct05.csv's (exact); the five-year shares reproduce the identified mix of
meta.lineage.age_mix (1e-7: the case lane sums single-precision weights, about 1e-8 off); the added people add to
meta.lineage.counts.added (1e-6 persons).
Output: derived/g3plus_ages_oct07.csv (bin, g3plus persons, share, added persons at the measured mix). Run from the
repository root:
  OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/main_case_decomposition_2026_09_29/profiles_oct07.py
"""
from __future__ import annotations

import sys

sys.dont_write_bytecode = True  # read-only imports from other lanes: write nothing beside them

import csv  # noqa: E402
import json  # noqa: E402
from pathlib import Path  # noqa: E402

import numpy as np  # noqa: E402

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import profiles as PR  # noqa: E402  (its helpers and the generation lane's modules; main() is not run)

F = PR.F
FISCAL = PR.FISCAL
OUT = HERE / "derived"
EDGES = PR.EDGES
gate = PR.gate
PAYLOAD = FISCAL / "main_case_2026_10_07/derived/corrections.json"
OCT05 = OUT / "g3plus_ages_oct05.csv"


def main():
    lineage = json.loads(PAYLOAD.read_text())["meta"]["lineage"]
    counts, mix = lineage["counts"], lineage["age_mix"]
    print("[frame]", flush=True)
    d = F.load()
    _, _, gens = F.masks(d)
    w = d.pwwgt0.to_numpy(float)
    g3 = gens["G3plus"]
    b = PR.bins_of(d.A_AGE.to_numpy())
    nb = len(EDGES)
    pg = np.bincount(b, weights=np.where(g3, w, 0.0), minlength=nb)
    total = float(w[g3].sum())

    # Each bin's five-year band (the bins nest in them: single years to 24, five-year bins to 80, 80 and 85 in 80+).
    starts = [int(x.split("-")[0].rstrip("+")) for x in mix["bands"]]
    if starts != list(range(0, 5 * len(starts), 5)) or not mix["bands"][-1].endswith("+"):
        raise SystemExit("[BLOCKED] meta.lineage.age_mix: the bands are not five-year bands from 0 with an open top")
    lo = np.array(EDGES)
    hi = np.append(lo[1:], 999)
    band = np.minimum(lo // 5, len(starts) - 1)
    nested = all(hi[i] <= 5 * (band[i] + 1) or band[i] == len(starts) - 1 for i in range(nb))
    n_band = np.bincount(band, weights=pg, minlength=len(starts))
    m = {k: np.asarray(mix["mixes"][k], float) for k in ("identified", "g3_rate", "later")}
    added_band = counts["at_g3_rate"] * m["g3_rate"] + counts["later_losses"] * m["later"]
    added = pg * (added_band / n_band)[band]

    print("[gates]", flush=True)
    gate("G3+ (convention a) is the payload's identified_g3plus, the generation lane's G3plus population (1e-3 persons)",
         abs(total - counts["identified_g3plus"]) < 1e-3, f"{total:,.6f} vs {counts['identified_g3plus']:,.6f}")
    gate("the bins add to the total (1e-6 persons)", abs(pg.sum() - total) < 1e-6, f"{pg.sum():,.6f}")
    gate("every bin holds G3+ members", bool((pg > 0).all()), f"smallest {pg.min():,.1f}")
    with OCT05.open() as handle:
        v5 = [float(r["g3plus"]) for r in csv.DictReader(handle)]
    gate("the identified G3+ by bin is g3plus_ages_oct05.csv's (exact)", v5 == [float(x) for x in pg], f"{len(v5)} bins")
    gate("every bin lies in one five-year band of meta.lineage.age_mix", nested, f"{len(starts)} bands")
    worst = float(np.abs(n_band / total - m["identified"]).max())
    gate(f"the five-year shares reproduce meta.lineage.age_mix's identified mix ({len(starts)} bands, 1e-7)", worst < 1e-7,
         f"worst {worst:.1e}")
    gap = abs(float(added.sum()) - counts["added"])
    gate("the added people add to meta.lineage.counts.added (1e-6 persons)", gap < 1e-6, f"|diff| {gap:.1e}")

    OUT.mkdir(exist_ok=True)
    with (OUT / "g3plus_ages_oct07.csv").open("w", newline="") as handle:
        out = csv.writer(handle, lineterminator="\n")
        out.writerow(["bin", "g3plus", "share", "added"])
        for i in range(nb):
            out.writerow([EDGES[i], repr(float(pg[i])), repr(float(pg[i] / total)), repr(float(added[i]))])
    at_id = counts["added"] * pg / total
    print(f"  G3+ {total:,.1f} persons; v6's {counts['added']:,.1f} added people at the measured mix: "
          f"{added[lo < 18].sum():,.0f} under 18, {added[lo >= 65].sum():,.0f} at 65+ (at the identified G3+'s ages: "
          f"{at_id[lo < 18].sum():,.0f} and {at_id[lo >= 65].sum():,.0f})", flush=True)
    if PR.FAILS:
        print(f"FAIL: {len(PR.FAILS)} gate(s): {PR.FAILS}")
        sys.exit(1)
    print("  all gates passed")


if __name__ == "__main__":
    main()
