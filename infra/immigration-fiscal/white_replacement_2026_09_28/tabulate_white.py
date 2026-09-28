"""ACS 2024 one-year PUMS cells for US-born non-Hispanic white residents, by 2022 PUMA, in the scale-spillover lane's
item layout (its person_items, imported read-only), plus the union's cells re-tabulated as a check.

Group person: NH white alone (RAC1P 1, HISP 01), native (NATIVITY 1), not born in Mexico (the union's rule). The ACS has no parent birthplace, so the
third-plus generation cannot be separated; the slice is all US-born NH whites. Labels: "nhw_usborn", "union" (HISP 02
or POBP 303, the spillover lane's rule) and "rest" (everyone else). The union label must equal the spillover lane's
mexborn + group_other cells (gate).

Output: derived/pums_white_cells.csv (PUMA x label, person-weighted sums of every item).
Run from the repository root:
  OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/white_replacement_2026_09_28/tabulate_white.py
"""
from __future__ import annotations

import io
import sys
import zipfile
from pathlib import Path

sys.dont_write_bytecode = True

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

LANE = Path(__file__).resolve().parent
FISCAL = LANE.parent
SPILL = FISCAL / "scale_spillovers_2026_09_23"
sys.path.insert(0, str(SPILL))
import tabulate as T  # noqa: E402  the spillover lane's person_items and PUMS path

DER = LANE / "derived"


def main():
    cols = ["STATE", "PUMA", "PWGTP", "HISP", "POBP", "RAC1P", "NATIVITY", "AGEP", "SCHL", "ESR", "PERNP", "WAGP",
            "WKHP", "ADJINC"]
    cells = []
    with zipfile.ZipFile(T.PUMS / "csv_pus.zip") as z:
        for member in ("psam_pusa.csv", "psam_pusb.csv"):
            with z.open(member) as fh:
                for chunk in pd.read_csv(io.TextIOWrapper(fh), usecols=cols, chunksize=T.CHUNK,
                                         dtype={"STATE": str, "PUMA": str}):
                    union = (chunk["HISP"].eq(2) | chunk["POBP"].eq(T.MEXICO)).to_numpy()
                    # native NH whites born in Mexico to US parents belong to the union by its rule, not here
                    white = (chunk["RAC1P"].eq(1) & chunk["HISP"].eq(1) & chunk["NATIVITY"].eq(1)).to_numpy() & ~union
                    items = T.person_items(chunk)
                    wt = chunk["PWGTP"].to_numpy(float)
                    for label, mask in (("nhw_usborn", white), ("union", union), ("rest", ~white & ~union)):
                        cell = items[mask].mul(wt[mask], axis=0)
                        cell["STATE"], cell["PUMA"] = chunk["STATE"].to_numpy()[mask], chunk["PUMA"].to_numpy()[mask]
                        cell["label"] = label
                        cells.append(cell.groupby(["STATE", "PUMA", "label"]).sum())
    out = pd.concat(cells).groupby(level=[0, 1, 2]).sum().reset_index()
    ref = pd.read_csv(SPILL / "derived/pums_puma_cells.csv", dtype={"STATE": str, "PUMA": str})
    ref_u = ref[ref.label != "other"].groupby(["STATE", "PUMA"])[T_ITEMS].sum()
    mine_u = out[out.label == "union"].set_index(["STATE", "PUMA"])[T_ITEMS].reindex(ref_u.index)
    if not np.allclose(mine_u.to_numpy(), ref_u.to_numpy(), rtol=1e-9, atol=1e-6):
        raise SystemExit("[BLOCKED] the union cells do not reproduce the spillover lane's pums_puma_cells.csv")
    ref_all = ref.groupby(["STATE", "PUMA"])[T_ITEMS].sum()
    mine_all = out.groupby(["STATE", "PUMA"])[T_ITEMS].sum().reindex(ref_all.index)
    if not np.allclose(mine_all.to_numpy(), ref_all.to_numpy(), rtol=1e-9, atol=1e-6):
        raise SystemExit("[BLOCKED] all-person cells do not reproduce the spillover lane's totals")
    print("[gate] union and all-person PUMA cells reproduce the spillover lane's pums_puma_cells.csv")
    out.to_csv(DER / "pums_white_cells.csv", index=False, lineterminator="\n", float_format="%.4f")
    nat = out.groupby("label")[T_ITEMS].sum()
    for lab in nat.index:
        r = nat.loc[lab]
        print(f"{lab:11s} persons {r.persons / 1e6:7.2f}m workers {r.workers / 1e6:6.2f}m  mean years 25+ "
              f"{r.adults25_yrs / r.adults25:5.2f}  some college+ share of workers "
              f"{(r.workers_sc + r.workers_ba + r.workers_grad) / r.workers:.3f}  BA+ {(r.workers_ba + r.workers_grad) / r.workers:.3f}")


T_ITEMS = ["persons", "adults25", "adults25_yrs", "adults25_ba", "workers", "workers_yrs", "workers_collyrs",
           "workers_hsyrs", "earnings", "wages", "earners", "ft3065_lc", "ft3065_ba", "workers_lths", "earnings_lths",
           "workers_hs", "earnings_hs", "workers_sc", "earnings_sc", "workers_ba", "earnings_ba", "workers_grad",
           "earnings_grad"]

if __name__ == "__main__":
    main()
