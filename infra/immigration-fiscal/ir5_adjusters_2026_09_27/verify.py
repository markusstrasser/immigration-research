#!/usr/bin/env python3
"""Checks for this lane: quotes, a full rerun, byte-identical outputs and the RESULT's headline numbers.

1. Every quote in reads/*_quotes.json is a substring of its cached source file after whitespace is
   collapsed on both sides.
2. The five scripts rerun in order from the repository root and each exits 0. Their gates are
   assertions inside them: the OHSS table titles and row sums (ohss_lias.py), the NIS sample counts
   (nis_adjusters.py), the credit totals (ptc.py), the new-arrival profile and NPVs reproducing the
   tail lane (adjusters.py), and the NIS age mix, the tail lane's FY2024 flow and the linear floor
   fit (mix_and_flow.py).
3. Every file in derived/ is rewritten by the rerun (its mtime moves) and is byte-identical to the
   file before the rerun.
4. The headline numbers quoted in RESULT.md match derived/.

Run from the repository root (about four minutes; --quick skips step 2 and 3):
  OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/ir5_adjusters_2026_09_27/verify.py
"""
from __future__ import annotations

import hashlib
import json
import os
import re
import subprocess
import sys
from pathlib import Path

import pandas as pd

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
OUT = HERE / "derived"
SCRIPTS = ("ohss_lias.py", "nis_adjusters.py", "ptc.py", "adjusters.py", "mix_and_flow.py")


def norm(s: str) -> str:
    return re.sub(r"\s+", " ", s).strip()


def check_quotes() -> None:
    for qf in sorted((HERE / "reads").glob("*_quotes.json")):
        quotes = json.loads(qf.read_text())
        texts: dict[str, str] = {}
        bad = []
        for q in quotes:
            if q["file"] not in texts:
                texts[q["file"]] = norm((HERE / q["file"]).read_text(encoding="utf-8", errors="replace"))
            if norm(q["quote"]) not in texts[q["file"]]:
                bad.append(q["id"])
        assert not bad, (qf.name, bad)
        print(f"  ✓ {qf.relative_to(HERE)}: {len(quotes)} of {len(quotes)} quotes found in their sources")


def snapshot() -> dict[str, tuple[str, int]]:
    return {p.name: (hashlib.sha256(p.read_bytes()).hexdigest(), p.stat().st_mtime_ns)
            for p in sorted(OUT.iterdir()) if p.is_file()}


def rerun() -> None:
    before = snapshot()
    env = dict(os.environ, OPENBLAS_NUM_THREADS="1", PYTHONDONTWRITEBYTECODE="1")
    for s in SCRIPTS:
        r = subprocess.run([sys.executable, str(HERE / s)], cwd=ROOT, env=env, capture_output=True, text=True)
        assert r.returncode == 0, (s, r.returncode, r.stderr[-2000:])
        print(f"  ✓ {s} exit 0")
    after = snapshot()
    assert before.keys() == after.keys(), (sorted(before.keys() ^ after.keys()))
    stale = [k for k in before if after[k][1] <= before[k][1]]
    assert not stale, ("not rewritten by the rerun", stale)
    changed = [k for k in before if after[k][0] != before[k][0]]
    assert not changed, ("outputs differ between runs", changed)
    print(f"  ✓ {len(after)} files in derived/ rewritten and byte-identical")


def check_headlines() -> None:
    arms = pd.read_csv(OUT / "arms_by_age.csv")
    flow = pd.read_csv(OUT / "flow_fy2024.csv")
    be = pd.read_csv(OUT / "breakeven.csv")
    fb = pd.read_csv(OUT / "breakeven_floor.csv")

    def arm(profile, a, age, rate, variant="central", case="central"):
        s = arms[(arms.profile == profile) & (arms.arm == a) & (arms.adjust_age == age) & (arms.real_rate == rate)
                 & (arms.variant == variant) & (arms.case == case) & (arms.counterfactual == "central")]
        assert len(s) == 1
        return round(-float(s.npv.iloc[0]) / 1000)

    def fl(a, col="flow_bn", variant="central", rate=0.03, mix="fy2024_central", tmix="nis_all"):
        s = flow[(flow.arm == a) & (flow.variant == variant) & (flow.real_rate == rate) & (flow.age_mix == mix)
                 & (flow.type_mix == tmix) & (flow.case == "central") & (flow.counterfactual == "central")]
        assert len(s) == 1
        return float(s[col].iloc[0])

    ages = (55, 60, 65)
    expect = {
        ("new_arrival", "B", 0.03): (274, 275, 288), ("new_arrival", "B", 0.0): (527, 476, 437),
        ("adjuster_nis_all", "A", 0.03): (185, 182, 186), ("adjuster_nis_all", "B", 0.03): (290, 296, 318),
        ("adjuster_nis_all", "C_central", 0.03): (237, 235, 240),
        ("adjuster_nis_all", "C_central", 0.0): (463, 412, 370),
        ("T3_pre1996", "B", 0.03): (323, 339, 381),
    }
    for (p, a, r), vals in expect.items():
        got = tuple(arm(p, a, age, r) for age in ages)
        assert got == vals, (p, a, r, got, vals)
    got = tuple(arm("adjuster_nis_all", "C_central", age, 0.03, variant="ptc_off") for age in ages)
    assert got == (230, 231, 241), got
    got = tuple(arm("new_arrival", "B", age, 0.03, variant="ptc_off") for age in ages)
    assert got == (270, 275, 286), got
    assert round(fl("C_central"), 1) == -14.3 and round(fl("C_central", "flow_all_as_new_bn"), 1) == -16.1
    assert round(fl("C_central", variant="ptc_off"), 1) == -13.9
    assert round(fl("C_central", "flow_all_as_new_bn", variant="ptc_off"), 1) == -15.9
    assert round(fl("C_central", rate=0.0), 1) == -30.1 and round(fl("C_central", "flow_all_as_new_bn", rate=0.0), 1) == -33.3
    s = be[(be.variant == "central") & (be.case == "central") & (be.profile == "adjuster_nis_all")
           & (be.real_rate == 0.03) & be.adjust_age.isin(ages)]
    assert (round(s.p_stay_breakeven.min(), 2), round(s.p_stay_breakeven.max(), 2)) == (0.15, 0.23)
    assert (round(s.p_stay_central_implied.min(), 2), round(s.p_stay_central_implied.max(), 2)) == (0.50, 0.59)
    s = fb[(fb.case == "central") & (fb.profile == "adjuster_nis_all") & (fb.arm == "C_central")
           & (fb.real_rate == 0.03) & fb.adjust_age.isin(ages)].sort_values("adjust_age")
    assert tuple(round(x) for x in s.floor_breakeven) == (2024, 2136, 3012), tuple(s.floor_breakeven)
    assert float(fb.fit_max_residual.max()) < 0.2
    assert tuple(round(-fl("C_central", c) / 1000) for c in
                 ("mean_new_arrival", "mean_adjuster", "mean_adjuster_as_new_arrival")) == (263, 218, 254)
    sh = pd.read_csv(OUT / "ohss_lias_adjust_shares.csv")
    pct = {(r.series, r.fy): round(100 * r.adjustments / (r.adjustments + r.new_arrivals)) for r in sh.itertuples()}
    assert [pct[("parents_of_us_citizens_all_nationalities", y)] for y in (2019, 2022, 2023, 2024, 2025)] == \
        [52, 40, 52, 53, 52]
    assert [pct[("mexico_nationals_all_classes", y)] for y in (2019, 2022, 2023, 2024, 2025)] == [64, 51, 63, 65, 65]
    print("  ✓ RESULT headline numbers match derived/")


def main() -> None:
    print("[quotes]")
    check_quotes()
    if "--quick" not in sys.argv:
        print("[rerun]")
        rerun()
    print("[headlines]")
    check_headlines()


if __name__ == "__main__":
    main()
