"""Ages of the people main case v5 adds (`main_case_2026_10_05`, case key `oct05`), in the decomposition's age bins.

v5 adds 3.04M descendants of Mexican immigrants who no longer report Mexican origin (the payload's
meta.lineage.counts.added) and prices them at the identified third-plus generation's ages: later losses as G3+ members,
the G3-rate attriters partly as third-plus non-Hispanic whites reweighted to G3+'s five-year age structure
(main_case_lineage_2026_10_05). decompose.cjs places them at that age structure. This script writes it in the bins
`profiles.py` uses: the generation lane's G3plus (`generation_account_2026_09_24/frame.py` masks, convention a, which
the lineage's G3+ pricing uses) on the ASEC person weights. Audit row 4 reweights only the Mexico-born, and
`profiles.py` gates that it leaves G3+ unchanged, so these are also the row-4 frame's counts.

Gates (exit 1): the total is the payload's meta.lineage.counts.identified_g3plus, the generation lane's G3plus
population (1e-3 persons); every bin holds G3+ members; the five-year shares reproduce the lineage lane's
white_lines.json meta.age_structures.g3plus (1e-6), the structure its white pricing uses.
Output: derived/g3plus_ages_oct05.csv (bin, g3plus persons, share). Run from the repository root:
  OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/main_case_decomposition_2026_09_29/profiles_oct05.py
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
PAYLOAD = FISCAL / "main_case_2026_10_05/derived/corrections.json"
WHITE = FISCAL / "main_case_lineage_2026_10_05/derived/white_lines.json"


def main():
    counts = json.loads(PAYLOAD.read_text())["meta"]["lineage"]["counts"]
    print("[frame]", flush=True)
    d = F.load()
    _, _, gens = F.masks(d)
    w = d.pwwgt0.to_numpy(float)
    g3 = gens["G3plus"]
    b = PR.bins_of(d.A_AGE.to_numpy())
    nb = len(EDGES)
    pg = np.bincount(b, weights=np.where(g3, w, 0.0), minlength=nb)
    total = float(w[g3].sum())

    print("[gates]", flush=True)
    gate("G3+ (convention a) is the payload's identified_g3plus, the generation lane's G3plus population (1e-3 persons)",
         abs(total - counts["identified_g3plus"]) < 1e-3, f"{total:,.6f} vs {counts['identified_g3plus']:,.6f}")
    gate("the bins add to the total (1e-6 persons)", abs(pg.sum() - total) < 1e-6, f"{pg.sum():,.6f}")
    gate("every bin holds G3+ members", bool((pg > 0).all()), f"smallest {pg.min():,.1f}")
    white = json.loads(WHITE.read_text())["meta"]["age_structures"]
    bands = [5 * k for k in range(len(white["g3plus"]))]
    lo = np.array(EDGES)
    five = np.array([pg[(lo >= x) & (lo < (bands[k + 1] if k + 1 < len(bands) else 999))].sum() for k, x in enumerate(bands)])
    worst = float(np.abs(five / total - np.array(white["g3plus"])).max())
    gate(f"the five-year shares reproduce white_lines.json's g3plus age structure ({len(bands)} bands, 1e-6)", worst < 1e-6,
         f"worst {worst:.1e}; bands {white['band'][0]} .. {white['band'][-1]}")

    OUT.mkdir(exist_ok=True)
    with (OUT / "g3plus_ages_oct05.csv").open("w", newline="") as handle:
        out = csv.writer(handle, lineterminator="\n")
        out.writerow(["bin", "g3plus", "share"])
        for i in range(nb):
            out.writerow([EDGES[i], repr(float(pg[i])), repr(float(pg[i] / total))])
    added = counts["added"]
    print(f"  G3+ {total:,.1f} persons; v5's {added:,.1f} added people at these ages: "
          f"{added * pg[lo < 18].sum() / total:,.0f} under 18, {added * pg[lo >= 65].sum() / total:,.0f} at 65+", flush=True)
    if PR.FAILS:
        print(f"FAIL: {len(PR.FAILS)} gate(s): {PR.FAILS}")
        sys.exit(1)
    print("  all gates passed")


if __name__ == "__main__":
    main()
