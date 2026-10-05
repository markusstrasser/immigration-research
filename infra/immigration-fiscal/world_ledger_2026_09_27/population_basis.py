"""The population the group's person-based rows are counted on: the place premium, Mexico's budget and the income
positions, which g2_premium.py, weights.py and valuation.py build from CPS ASEC 2025 person records.

cps   the published CPS union, 40,896,574 persons (G1 12.22M): the basis of every case through sept27.
row4  the 39,712,493 persons the account prices (the dataset audit's row 4; ladder entries 209 and 274). The
      Mexico-born outside California and Texas are raked to ACS 2024 totals by citizenship with the factors in
      main_case_candidate_2026_09_28/derived/production_row4.json, the reweight
      generation_account_2026_09_24/v4_inputs.py applies. The account's fiscal lines have been on row 4 since the
      Sept 24 case, so on the cps basis a generation's person-based rows (12.22M in G1) and its US budget flows
      (11.04M) count different people. A case's pins name its basis ("basis", default cps); world_ledger.py can also
      run a case on the other basis beside it.
lineage  the 42,752,213 persons main case v5 prices (oct05, adopted 2026-10-05): row 4 plus the 3,039,720
      descendants of Mexican immigrants who no longer report Mexican origin, counted whole in G3+
      (main_case_2026_10_05/derived/corrections.json meta.lineage.counts, read at the case's adoption commit). The
      CPS holds the added people as other residents and cannot find them, so the identified G3+ records stand in for
      them: row 4's weights, then every G3+ record's weight times (identified G3+ + added) / identified G3+
      [ASSUMPTION: the added people at the identified G3+'s ages, earnings and incomes, as the generation account's
      per-member figures and the winners lane's group frame place them].

The script that writes a basis-dependent file writes it under its own name on cps and with a _<basis> suffix
otherwise (suffixed). reweight() gates the mask against production_row4.json (records and CPS population per
status), that the mask moves no civilian outside the union, and that the union then sums to the account's row-4
count; on the lineage, that the G3+ records sum to the case's identified G3+ and the union then to its lineage.
"""
import io
import json
import subprocess
import zipfile
from pathlib import Path

import pandas as pd

REPO = Path(__file__).resolve().parents[3]
ROW4_REL = "infra/immigration-fiscal/main_case_candidate_2026_09_28/derived/production_row4.json"
ROW4_PIN = "c313b53"               # the Sept 28 candidate's commit, which wrote production_row4.json
LINEAGE_REL = "infra/immigration-fiscal/main_case_2026_10_05/derived/corrections.json"
LINEAGE_PIN = "4bf0206"            # main case v5's adoption commit, which wrote the payload's meta.lineage
BASES = ("cps", "row4", "lineage")
STATUS = {"naturalized": 4, "noncitizen": 5}      # PRCITSHP
KEEP = (6, 48)                                    # GESTFIPS: California and Texas keep their weights
MEXICO = 303                                      # PENATVTY


def suffixed(path, basis):
    """A basis-dependent file's path: its own name on cps, <stem>_<basis><suffix> on row4 and lineage."""
    if basis not in BASES:
        raise SystemExit(f"[BLOCKED] unknown population basis {basis!r}; one of {BASES}")
    return path if basis == "cps" else path.with_name(f"{path.stem}_{basis}{path.suffix}")


def row4():
    out = subprocess.run(["git", "-C", str(REPO), "show", f"{ROW4_PIN}:{ROW4_REL}"], capture_output=True, check=True)
    return json.load(io.BytesIO(out.stdout))


def lineage():
    """Main case v5's counts (meta.lineage.counts): added, identified_g3plus, lineage_population and the rest."""
    out = subprocess.run(["git", "-C", str(REPO), "show", f"{LINEAGE_PIN}:{LINEAGE_REL}"], capture_output=True,
                         check=True)
    return json.load(io.BytesIO(out.stdout))["meta"]["lineage"]["counts"]


def g3plus(d):
    """The union's third-plus generation: US-born members with no Mexico-born parent (g2_premium.py's and
    weights.py's G3+, which gate that the lineage scales exactly their own G3+ records)."""
    usb = d.PRCITSHP.isin([1, 2, 3]).to_numpy()
    mexpar = d.PEFNTVTY.eq(303).to_numpy() | d.PEMNTVTY.eq(303).to_numpy()
    return d.target.to_numpy() & usb & ~mexpar


def reweight(d, cps_zip, gate, basis="row4"):
    """The distribution lane's CPS frame (load_cps(): pw = pwwgt0, target = the union, civ = civilians) on row 4, or
    on the lineage: row 4's weights (kept as pw_row4), then the G3+ records' times the lineage factor."""
    if basis not in ("row4", "lineage"):
        raise SystemExit(f"[BLOCKED] reweight() takes row4 or lineage, not {basis!r}")
    r = row4()
    with zipfile.ZipFile(cps_zip) as z:
        state = pd.read_csv(z.open("hhpub25.csv"), usecols=["H_SEQ", "GESTFIPS"]).set_index("H_SEQ").GESTFIPS
    st = d.PH_SEQ.map(state)
    gate("row4_every_person_has_a_state", bool(st.notna().all()), missing=int(st.isna().sum()))
    outside = ~st.isin(KEEP).to_numpy()
    civ, target = d.civ.to_numpy(), d.target.to_numpy()
    pw = d.pw.to_numpy(float).copy()
    for label, code in STATUS.items():
        m = d.PENATVTY.eq(MEXICO).to_numpy() & d.PRCITSHP.eq(code).to_numpy() & outside
        ref = r["row4_factors"][label]
        gate(f"row4_mask_is_production_row4s_{label}", int(m.sum()) == ref["records"]
             and abs(float(pw[m].sum()) - ref["cps_population"]) < 1e-3,
             records=int(m.sum()), cps_population=float(pw[m].sum()), want=ref)
        gate(f"row4_mask_moves_no_civilian_outside_the_union_{label}", not bool((civ & ~target & m).any()))
        pw[m] *= ref["factor"]
    gate("row4_union_is_the_accounts_count", abs(float(pw[target].sum()) - r["populations"]["row4"]) < 1e-3,
         union=float(pw[target].sum()), row4=r["populations"]["row4"])
    d = d.copy()
    d["pw"] = pw
    if basis == "lineage":
        c = lineage()
        g3 = g3plus(d)
        identified = float(pw[g3].sum())
        gate("lineage_g3plus_is_the_cases_identified_g3plus", abs(identified - c["identified_g3plus"]) < 1e-3,
             frame=identified, case=c["identified_g3plus"])
        gate("lineage_row4_union_is_the_cases_account_union", abs(float(pw[target].sum()) - c["account_union"]) < 1e-3,
             frame=float(pw[target].sum()), case=c["account_union"])
        lw = pw.copy()
        lw[g3] *= 1.0 + c["added"] / identified
        gate("lineage_union_is_the_cases_lineage", abs(float(lw[target].sum()) - c["lineage_population"]) < 1e-3,
             union=float(lw[target].sum()), lineage=c["lineage_population"])
        d["pw_row4"] = pw
        d["pw"] = lw
    return d
