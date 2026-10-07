#!/usr/bin/env python3
"""The lineage's share of households: AEI's own rule for sharing the fiscal gap.

Orrenius, Viard & Zavodny (AEI, September 2025, pp. 11-12 and note 22) give each household, with its descendants, an
equal part of the gap ("1/200,000,000th of the aggregate burden"). closed_budget.py's per_household rule needs the
lineage's share of households on the account's frame.

Frame: CPS ASEC 2025 civilians through the distribution lane's loader (distribution_weights_2026_09_23/distribute.py
load_cps), on main case v5's lineage basis (world_ledger_2026_09_27/population_basis.py reweight): row 4's weights,
with the identified G3+ records also carrying the 3,039,720 added descendants [ASSUMPTION: the added people live in
households of the identified G3+'s sizes, as the case prices them at that group's ages].

A household counts at its CPS household weight W (HSUP_WGT), split equally over its civilian members, so a mixed
household counts for the lineage by its lineage members' fraction. Each member's slice W / n is scaled by the
member's own reweighting (row 4's factor, and on the lineage also the G3+ factor, over the published weight):

    share = sum over lineage members of (W / n) * w_lineage / w_cps  /  sum over civilians of (W / n) * w_row4 / w_cps,

with n the household's civilian members. The denominator stays on row 4 because the added people are already other
residents in the national count (the decomposition's NC). Splitting person weights instead (sum of w / n) counts
2.3% more households than the household weights do, because children's person weights run higher than their
householders'; it is reported as a diagnostic. The householder's lineage status is reported beside the share.

Gates: the frame reproduces the decomposition's NG and NC (summary_oct05.json); the slices add to the household
weights' count; the share lies below the per-person share (the lineage lives in larger households).

--case oct07 (main case v6, which prices the added people at their measured age mix, meta.lineage.age_mix): each
identified G3+ record carries the added people in proportion to its five-year band's share of them over its share of
the identified G3+ (the G3-rate persons and the later losses at their own mixes, by count), as the white lane's
age_tilt() places them [ASSUMPTION: the added people live in households of the identified G3+ records of their own
ages]. Gates, beside the oct05 ones on the decomposition's summary_oct07.json: the frame's identified G3+ ages are the
age-mix lane's identified mix (1e-6), no band holds added people without identified G3+, and the tilted lineage is the
lineage population. Writes derived/oct07/household_share.json.

Writes derived/household_share.json. Run from the repository root:
  OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/closed_budget_2026_10_06/households.py
  OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/closed_budget_2026_10_06/households.py --case oct07
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import sys
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd

LANE = Path(__file__).resolve().parent
FISCAL = LANE.parent
OUT = LANE / "derived"
DECOMP = FISCAL / "main_case_decomposition_2026_09_29/derived/summary_oct05.json"
# The case each run is on: the decomposition's frame it gates against, where it writes, and (oct07) the payload whose
# meta.lineage.age_mix places the added people.
CASES = {"oct05": dict(decomp=DECOMP, out=OUT),
         "oct07": dict(decomp=FISCAL / "main_case_decomposition_2026_09_29/derived/summary_oct07.json", out=OUT / "oct07",
                       payload=FISCAL / "main_case_2026_10_07/derived/corrections.json")}
sys.path.insert(0, str(FISCAL / "world_ledger_2026_09_27"))
from population_basis import g3plus, reweight  # noqa: E402

HOUSEHOLDER = (1, 2)  # A_EXPRRP: reference person with and without relatives


def gate(name, ok, **detail):
    if not ok:
        raise SystemExit(f"[BLOCKED] gate {name} failed: {detail}")


def age_tilted(d, payload_file: Path) -> np.ndarray:
    """oct07: the lineage weights with the added people on the identified G3+ records at the measured age mix: each
    record's added weight is its band's share of the added people over its share of the identified G3+ (row 4's
    weights), so the identified mix gives v5's proportional placement."""
    lin = json.loads(payload_file.read_text())["meta"]["lineage"]
    am, c = lin["age_mix"], lin["counts"]
    gate("age_mix_on_five_year_bands", am["bands"] == [f"{b}-{b + 4}" for b in range(0, 80, 5)] + ["80+"])
    pw, g3 = d.pw_row4.to_numpy(float), g3plus(d)
    band = np.minimum(d.A_AGE.to_numpy() // 5, 16)
    ident = np.array([pw[g3 & (band == b)].sum() for b in range(17)]) / pw[g3].sum()
    gate("frame_g3plus_ages_are_the_age_mix_lanes_identified_mix", float(np.abs(ident - am["mixes"]["identified"]).max()) < 1e-6,
         max_diff=float(np.abs(ident - am["mixes"]["identified"]).max()))
    mix = (c["at_g3_rate"] * np.asarray(am["mixes"]["g3_rate"], float)
           + c["later_losses"] * np.asarray(am["mixes"]["later"], float)) / c["added"]
    gate("added_mix_sums_to_one_with_no_band_outside_the_identified", abs(mix.sum() - 1) < 1e-12
         and not bool(((ident <= 0) & (mix > 0)).any()), total=float(mix.sum()))
    tilt = np.divide(mix, ident, out=np.zeros(17), where=ident > 0)
    lw = pw.copy()
    lw[g3] *= 1.0 + c["added"] / float(pw[g3].sum()) * tilt[band[g3]]
    tgt = d.target.to_numpy()
    gate("tilted_lineage_is_the_lineage_population", abs(float(lw[tgt].sum()) - c["lineage_population"]) < 1e-2,
         lineage=float(lw[tgt].sum()), case=c["lineage_population"])
    return lw


def main(case: str = "oct05") -> None:
    conf = CASES[case]
    spec = importlib.util.spec_from_file_location("dist_base", FISCAL / "distribution_weights_2026_09_23/distribute.py")
    B = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(B)
    d = B.load_cps()
    with zipfile.ZipFile(B.PATHS["cps"]) as z:
        rel = pd.read_csv(z.open("pppub25.csv"), usecols=["PH_SEQ", "PPPOS", "A_EXPRRP"])
    d = d.merge(rel, on=["PH_SEQ", "PPPOS"], validate="one_to_one", how="left")
    gate("every_person_has_a_relationship", bool(d.A_EXPRRP.notna().all()))
    d = reweight(d, B.PATHS["cps"], gate, "lineage")

    frame = json.loads(conf["decomp"].read_text())["frame"]["row4"]
    civ, tgt = d.civ.to_numpy(), d.target.to_numpy()
    lw, r4 = d.pw.to_numpy(float), d.pw_row4.to_numpy(float)
    if "payload" in conf:
        lw = age_tilted(d, conf["payload"])
    gate("lineage_is_the_decompositions_NG", abs(lw[tgt].sum() - frame["NG"]) < 1e-2, frame=lw[tgt].sum(), NG=frame["NG"])
    gate("row4_civilians_are_the_decompositions_NC", abs(r4[civ].sum() - frame["NC"]) < 1.0, frame=r4[civ].sum(),
         NC=frame["NC"])

    n_civ = d.groupby("PH_SEQ").civ.transform("sum").to_numpy()
    cps = d.pwwgt0.to_numpy(float)
    W = d.HSUP_WGT.to_numpy(float) / 100
    slice_ = np.where(civ, W / np.maximum(n_civ, 1), 0.0)
    hh = d.drop_duplicates("PH_SEQ")
    weighted = float((hh.HSUP_WGT[hh.PH_SEQ.isin(d.PH_SEQ[civ])] / 100).sum())
    gate("slices_add_to_household_weights", abs(slice_.sum() - weighted) < 1e-3, slices=slice_.sum(),
         household_weights=weighted)
    eq_all = np.where(civ, slice_ * r4 / cps, 0.0)
    eq_lin = np.where(tgt, slice_ * lw / cps, 0.0)
    households = float(eq_all.sum())
    person_split = float(np.where(civ, r4 / np.maximum(n_civ, 1), 0.0).sum())

    per_person = frame["NG"] / frame["NC"]
    share = float(eq_lin.sum()) / households
    gate("household_share_below_per_person", 0 < share < per_person, share=share, per_person=per_person)

    # Householder rule: a household belongs to the lineage when its reference person does; the G3+ factor on the
    # reference person adds the added people's households at those households' weights.
    head = civ & d.A_EXPRRP.isin(HOUSEHOLDER).to_numpy()
    share_head = float((W * lw / cps)[head & tgt].sum()) / float((W * r4 / cps)[head].sum())
    size_lin = float(lw[tgt].sum() / eq_lin.sum())
    size_all = float(r4[civ].sum() / households)

    out = {
        "lane": "closed_budget_2026_10_06",
        "rule": "per_household: each household an equal part, split equally over its civilian members",
        "share": share,
        "share_householder": share_head,
        "per_person_share": per_person,
        "ratio_to_per_person": share / per_person,
        "households_row4": households,
        "households_cps_weights": weighted,
        "households_person_weight_split": person_split,
        "lineage_household_equivalents": float(eq_lin.sum()),
        "persons_per_household_lineage": size_lin,
        "persons_per_household_all": size_all,
        "frame": {"NG": float(lw[tgt].sum()), "NC": float(r4[civ].sum())},
    }
    if "payload" in conf:
        out["placement"] = ("the added people on the identified G3+ records at the measured age mix "
                            "(meta.lineage.age_mix), by five-year band")
    conf["out"].mkdir(parents=True, exist_ok=True)
    (conf["out"] / "household_share.json").write_text(json.dumps(out, indent=1) + "\n")
    print(f"per-household share {share:.6f} (householder {share_head:.6f}; per person {per_person:.6f}); "
          f"{size_lin:.3f} vs {size_all:.3f} persons per household")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--case", default="oct05", choices=list(CASES),
                    help="oct05 (default, v5) or oct07 (v6: the added people at their measured age mix)")
    main(ap.parse_args().case)
