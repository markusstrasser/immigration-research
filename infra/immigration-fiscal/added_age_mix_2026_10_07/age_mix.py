#!/usr/bin/env python3
"""The added people's age mix implied by measured identity loss by age (measure_loss.py), against the identified
third-plus's age mix that main case v5 prices them at.

Who is added (main_case_lineage_2026_10_05 population.json, arm b): g3_rate persons lost at the third-generation rate
(1 - p3 of the corrected third-plus, every generation) and `later` persons lost at the further G4+ step. Within a
five-year age band a, the identified third-plus N(a) = T(a) x (1 - L(a)) for a loss rate L(a), so the hidden are
N(a) x L(a) / (1 - L(a)):
  G3-rate part   L = the G3anc loss rate at the band (children of a G2 parent, and adults living with one);
  later part     L = the G4anc loss rate (children of an identified third-plus parent) on the G4+ members of the band,
                 who are a constant share of the identified third-plus at every age [ASSUMPTION, central; the population
                 lane's convention that members without grandparent detail share the seen members' generation mix];
                 the share measured among co-resident members by age is a sensitivity.
Counts stay arm b's: each part's mix is normalised and multiplied by its count; the implied totals are written beside.
v5 prices both parts at N(a)'s mix, which is this rule with a flat L.

Readings of L (derived/loss_tables.csv):
  cross_section_2007_2026  central: the current reports of the CPS persons the frame can see (a person is hidden in the
                           2025 ASEC by their 2025 report), pooled over 2007-26 (the 2007-21 and 2022-26 rates agree:
                           children 13.4 / 12.6%, adults 14.7 / 14.4%, measure_loss.py period table); bands 0-4, ..., 20-24
                           measured, 25-34, 35-49 and 50+ pooled;
  cross_section_2022_2026, cross_section_1994_2026  the same on the other windows;
  adults_35plus_at_25_34   the central with every band from 35 at the 25-34 rate (co-resident adults past 35 are few and
                           selected);
  g4_share_by_age          the central with the later part's G4+ share measured by age among co-resident identified members;
  cohort_at_birth          the brief's premise: the household respondent's report at birth persists, so today's band takes
                           the child-stage rate of the cohorts born in it; bands from 50 (born before 1976, never seen as
                           children in 1994-2026) hold the 45-49 rate. measure_loss.py's within-cohort table rejects the
                           premise (the same cohorts report 1-7 points less loss as adults), so it is an alternative;
  flat                     v5's own mix (positive control: zero change).
Each reading carries its band rates and their linearised SEs (clusters within survey year); summarize.py draws from
them for the sampling spread.

Gates (exit 1): every mix sums to 1 and is non-negative; flat reproduces the identified mix exactly; arm b's split is
population.json's; the identified mix is white_lines.json's g3plus structure (the lineage lane's).
Outputs: derived/age_mix.json, derived/age_mix.csv, derived/gates_mix.json
Run from the repository root:
  OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/added_age_mix_2026_10_07/age_mix.py
"""
from __future__ import annotations

import csv
import json
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
FISCAL = HERE.parent
OUT = HERE / "derived"
LINEAGE = FISCAL / "main_case_lineage_2026_10_05/derived"
TABLES = OUT / "loss_tables.csv"
CELLS = OUT / "loss_cells.csv"
ARM = "b"
BANDS = list(range(0, 80, 5)) + [80]
LABELS = [f"{b}+" if b == 80 else f"{b}-{b + 4}" for b in BANDS]
# Pricing band (lo of measure_loss.py PRICING_BANDS) that each five-year band reads.
READS = {0: 0, 5: 5, 10: 10, 15: 15, 20: 20, 25: 25, 30: 25, 35: 35, 40: 35, 45: 35}
READS.update({b: 50 for b in BANDS if b >= 50})
GATES: list[dict] = []


def gate(name: str, ok: bool, detail: str = "") -> None:
    GATES.append({"gate": name, "passed": bool(ok), "detail": detail})
    print(f"  {'PASS' if ok else 'FAIL'} {name}{' - ' + detail if detail else ''}", flush=True)


def rates(t: pd.DataFrame, table: str, group: str, label: str) -> tuple[np.ndarray, np.ndarray]:
    x = t[(t.table == table) & (t.group == group) & (t.label == label) & (t.outcome == "not_mexican")].set_index("lo")
    if table == "pricing_band":
        r = np.array([x.rate[READS[b]] for b in BANDS])
        s = np.array([x.se[READS[b]] for b in BANDS])
    else:  # cohort_band: five-year bands; bands with no child-stage observation hold the oldest measured one
        r, s = x.rate.reindex(BANDS).to_numpy().copy(), x.se.reindex(BANDS).to_numpy().copy()
        last = int(np.flatnonzero(np.isfinite(r))[-1])
        r[last + 1:], s[last + 1:] = r[last], s[last]
    if not (np.isfinite(r).all() and (r > 0).all() and (r < 1).all() and np.isfinite(s).all()):
        raise SystemExit(f"[BLOCKED] {table} {group} {label}: a band without a usable rate")
    return r, s


def g4_share_by_age() -> np.ndarray:
    """G4+ share of the identified co-resident third-plus by five-year band, 2007-26, bands from 50 pooled."""
    c = pd.read_csv(CELLS)
    c = c[c.YEAR.between(2007, 2026)].assign(ident=lambda x: x.base - x.lost, band=lambda x: np.minimum(x.age // 5 * 5, 80))
    c["read"] = c.band.map(READS)
    by = c.pivot_table(index="read", columns="group", values="ident", aggfunc="sum")
    share = by.G4anc / (by.G3anc + by.G4anc)
    return np.array([share[READS[b]] for b in BANDS])


def mix(pi: np.ndarray, L: np.ndarray, weight: np.ndarray | None = None) -> np.ndarray:
    h = pi * (weight if weight is not None else 1.0) * L / (1 - L)
    return h / h.sum()


def main() -> None:
    t = pd.read_csv(TABLES)
    wl = json.loads((LINEAGE / "white_lines.json").read_text())["meta"]["age_structures"]
    gate("the identified mix is white_lines.json's g3plus structure on its 17 bands", wl["band"] == LABELS, f"{len(BANDS)} bands")
    pi = np.array(wl["g3plus"], float)
    pop = json.loads((LINEAGE / "population.json").read_text())
    A = pop["arms"][ARM]
    gate("arm b is the lineage lane's central and its split adds to the added persons (1e-6)",
         pop["meta"]["central_arm"] == ARM and abs(A["g3_rate"] + A["later"] - A["added"]) < 1e-6,
         f"g3_rate {A['g3_rate']:,.1f}, later {A['later']:,.1f}")
    g4s = g4_share_by_age()
    readings = {
        "cross_section_2007_2026": ("pricing_band", "2007_2026", None),
        "cross_section_2022_2026": ("pricing_band", "2022_2026", None),
        "cross_section_1994_2026": ("pricing_band", "1994_2026", None),
        "adults_35plus_at_25_34": ("pricing_band", "2007_2026", "adults_35"),
        "g4_share_by_age": ("pricing_band", "2007_2026", "g4_share"),
        "cohort_at_birth": ("cohort_band", "child_stage_rate_of_cohorts_born_2025_minus_band", None),
    }
    out, rows = {}, []
    flat = {"g3_rate": pi.copy(), "later": pi.copy()}
    out["flat"] = {"rule": "v5: both parts at the identified third-plus's mix", "g3_rate": flat["g3_rate"].tolist(),
                   "later": flat["later"].tolist()}
    for name, (table, label, mod) in readings.items():
        r3, s3 = rates(t, table, "G3anc", label)
        r4, s4 = rates(t, table, "G4anc", label)
        if mod == "adults_35":
            for r, s in ((r3, s3), (r4, s4)):
                i25 = BANDS.index(25)
                r[BANDS.index(35):], s[BANDS.index(35):] = r[i25], s[i25]
        w4 = g4s if mod == "g4_share" else None
        m3, mL = mix(pi, r3), mix(pi, r4, w4)
        out[name] = {"table": table, "label": label, "modifier": mod, "g3anc_rate": r3.tolist(), "g3anc_se": s3.tolist(),
                     "g4anc_rate": r4.tolist(), "g4anc_se": s4.tolist(), "g3_rate": m3.tolist(), "later": mL.tolist(),
                     # Informational: the G3-rate count if p3 (a child rate) moved with the measured age profile,
                     # over the count at the child rate for every age; the priced counts stay arm b's.
                     "count_ratio_if_child_rate_scaled_by_age_profile": float(
                         (pi * r3 / (1 - r3)).sum() / ((lc := (pi[:4] * r3[:4]).sum() / pi[:4].sum()) / (1 - lc)))}
        if w4 is not None:
            out[name]["g4_share"] = g4s.tolist()
    for name, x in out.items():
        for part in ("g3_rate", "later"):
            m = np.array(x[part])
            gate(f"{name} {part}: the mix is non-negative and sums to 1 (1e-12)", (m >= 0).all() and abs(m.sum() - 1) < 1e-12)
    gate("flat is the identified mix exactly", out["flat"]["g3_rate"] == pi.tolist() and out["flat"]["later"] == pi.tolist())
    if not all(g["passed"] for g in GATES):
        raise SystemExit(f"[BLOCKED] {sum(not g['passed'] for g in GATES)} gate(s) failed; nothing written")
    for name, x in out.items():
        for part in ("g3_rate", "later"):
            m = np.array(x[part])
            rows.append({"reading": name, "part": part, **{lab: f"{v:.6f}" for lab, v in zip(LABELS, m)},
                         "share_0_19": f"{m[:4].sum():.6f}", "share_20_64": f"{m[4:13].sum():.6f}", "share_65_plus": f"{m[13:].sum():.6f}"})
    meta = {"source": "added_age_mix_2026_10_07/age_mix.py", "arm": ARM, "bands": LABELS, "identified": pi.tolist(),
            "g3_rate": A["g3_rate"], "later": A["later"], "added": A["added"], "c3": pop["c3"]["value"],
            "reads": {str(k): v for k, v in READS.items()},
            "rule": "hidden(a) = N(a) x L(a) / (1 - L(a)) normalised; counts are arm b's"}
    OUT.mkdir(exist_ok=True)
    (OUT / "age_mix.json").write_text(json.dumps({"meta": meta, "readings": out}) + "\n")
    with open(OUT / "age_mix.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]), lineterminator="\n")
        w.writeheader()
        w.writerows(rows)
    (OUT / "gates_mix.json").write_text(json.dumps({"gates": GATES}, indent=1) + "\n")
    print(f"  identified: 0-19 {pi[:4].sum():.3f}, 20-64 {pi[4:13].sum():.3f}, 65+ {pi[13:].sum():.3f}")
    for r in rows:
        print(f"  {r['reading']:<26} {r['part']:<8} 0-19 {float(r['share_0_19']):.3f}  20-64 {float(r['share_20_64']):.3f}  "
              f"65+ {float(r['share_65_plus']):.3f}")


if __name__ == "__main__":
    main()
