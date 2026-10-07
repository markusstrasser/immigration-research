"""How concentrated item T is inside each Mexico-born arrival window, and in the white reference.

Item T (`ledger_absolute_2026_09_17`) moves each record's survey income tax onto the main case's
income-tax keys. This check recomputes T on the arrival-window lane's records at both allocations,
with the ledger's own `income_tax_keys` and `income_tax_item`, and reports for each cell its total,
its per-person value, what its ten largest records and ten largest SPM units carry, and its
per-person value without those ten units. It writes `derived/t_concentration.csv` and changes no
other output.

Run from the repository root:

    OPENBLAS_NUM_THREADS=1 uv run --no-project python3 \
        infra/immigration-fiscal/arrival_window_fiscal_2026_09_18/t_concentration.py
"""
from __future__ import annotations

import argparse
import importlib.util
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("arrival_window_ledger", HERE / "arrival_window_ledger.py")
AW = importlib.util.module_from_spec(spec)
spec.loader.exec_module(AW)
A, AL = AW.A, AW.AL


def main() -> None:
    state = A.ext.build(argparse.Namespace(cps_zip=AW.GENEXT / "_cache/asecpub25csv.zip"))
    d, w = state["d"], state["person_weights"][:, 0]
    index, n_units = state["index"], state["n_units"]
    civilian = (d.PRPERTYP.eq(2) | d.A_AGE.lt(15)).to_numpy()
    mexico = state["group"]["mexico_born"] & civilian
    entry = d.PEINUSYR.to_numpy()
    cells = {name: mexico & np.isin(entry, codes) for name, (codes, _) in AW.WINDOWS.items()}
    cells["mexico_born"] = mexico
    cells[AW.WHITE] = state["group"][AW.WHITE] & civilian

    def unit_share(x):
        total = np.bincount(index, weights=np.asarray(x, dtype=float), minlength=n_units)
        return A.ext.allocate(total, index, np.ones(len(d), bool), n_units)

    keys = AL.income_tax_keys(d, civilian, w)
    rows = []
    for personal in (False, True):
        federal, state_part, _ = AL.income_tax_item(d, keys, civilian, w, personal, unit_share)
        t = federal + state_part
        for name, m in cells.items():
            tw = t[m] * w[m]
            pop, total = float(w[m].sum()), float(tw.sum())
            top_records = float(np.sort(tw)[::-1][:10].sum())
            top_units = float(pd.Series(tw).groupby(index[m]).sum().nlargest(10).sum())
            rows.append(dict(allocation="personal" if personal else "shared", cell=name,
                             records=int(m.sum()), population=pop, t_total_bn=total / 1e9,
                             t_per_person=total / pop, top10_records_bn=top_records / 1e9,
                             top10_units_bn=top_units / 1e9,
                             t_per_person_without_top10_units=(total - top_units) / pop,
                             max_record_t=float(t[m].max())))
    table = pd.DataFrame(rows)
    mexico_shared = table.query("allocation == 'shared' and cell == 'mexico_born'").t_total_bn.iloc[0]
    items = pd.read_csv(AW.ABSOLUTE / "derived/items_by_group.csv")
    ledger = items.query("item == 'T' and arm == 'central' and group == 'mexico_born'").total_bn
    if len(ledger) != 1 or abs(float(ledger.iloc[0]) - mexico_shared) > 1e-6:
        raise SystemExit(f"[BLOCKED] T on the Mexico-born cell {mexico_shared!r}bn is not the absolute lane's "
                         f"T row {ledger.tolist()}")
    print(f"[gate] Mexico-born T, shared: {mexico_shared:+.4f}bn = the absolute lane's T row -> PASS")
    table.to_csv(HERE / "derived/t_concentration.csv", index=False, lineterminator="\n")
    pd.set_option("display.width", 200)
    print(table.round(3).to_string(index=False))


if __name__ == "__main__":
    main()
