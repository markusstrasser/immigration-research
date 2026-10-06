#!/usr/bin/env python3
"""The lineage's share of the 2026 public-charge rule's transfer reduction, on the account's own CPS records.

DHS's final rule (91 FR 45324, 2026-07-20, effective 2026-09-18; staged under
sources/immigration-fiscal/data/external/stage3/federal_register/public_charge_2026_final_rule/) prices the rule as a
uniform 10.3% disenrollment (3.3-17.3%) among every benefit recipient in a household with at least one noncitizen,
citizens included (RIA Table IV.11). It does not split that population by origin. The literature-scan memo of
2026-10-06 put the lineage's part at 30-45% [an assumption of the reading worker]; this script replaces it.

Frame: CPS ASEC 2025 civilians through the distribution lane's loader (distribution_weights_2026_09_23/distribute.py
load_cps), with audit row 4's weights (world_ledger_2026_09_27/population_basis.py reweight, "lineage" basis). The
lineage is the case's target group; the 3.04M added descendants ride on the identified G3+ records' weights, so the
numerator is reported on both the lineage weights and row 4's, over a row-4 denominator.

Per programme, the population is DHS's: persons covered during the year (Medicaid MCAID, CHIP PCHIP, SSI SSI_YN,
public assistance PAW_YN, WIC WICYN) or members of a household with SNAP (HFDVAL > 0), in a household where any member
is not a citizen (PRCITSHP 5); rental assistance counts households (public housing HPUBLIC or a government rent
subsidy HLORENT), each split equally over its civilian members. The share of each programme's population is applied
to DHS's dollars: the federal lines of Table IV.13 at each rate, plus DHS's own state match on Medicaid and CHIP
(59% average FMAP, so state = federal x 0.41 / 0.59; the text's $4.05bn) for the combined figure. DHS's printed
$13.045bn grosses every line up by the FMAP; the combined figure here grosses only the two matched programmes.

[ASSUMPTION] the rate is uniform across groups, as DHS models it; a chilling effect concentrated in mixed-status
Hispanic families would raise the lineage's part. CPS benefit receipt is under-reported; the share is a ratio, so
only differential under-reporting moves it.

Gates: the frame reproduces the decomposition's NG and NC; each programme's noncitizen-household population is
positive and its lineage share lies in (0, 1); the federal programme lines add to DHS's printed totals.

Writes derived/public_charge_share.csv and derived/summary.json. From the repository root:
  OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/public_charge_share_2026_10_07/public_charge_share.py
"""
from __future__ import annotations

import csv
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
sys.path.insert(0, str(FISCAL / "world_ledger_2026_09_27"))
from population_basis import reweight  # noqa: E402

# DHS RIA Table IV.13, federal transfer reduction, $ per year, by disenrollment rate (images ER20JY26.020/.021).
DHS_FEDERAL = {
    "medicaid": {"3.3%": 1_834_624_440, "10.3%": 5_704_886_880, "17.3%": 9_574_666_596},
    "chip": {"3.3%": 37_425_052, "10.3%": 116_377_807, "17.3%": 195_320_657},
    "wic": {"3.3%": 9_670_896, "10.3%": 30_072_620, "17.3%": 50_471_534},
    "snap": {"3.3%": 327_503_760, "10.3%": 1_018_393_920, "17.3%": 1_709_202_000},
    "tanf": {"3.3%": 8_827_830, "10.3%": 27_449_190, "17.3%": 46_068_885},
    "ssi": {"3.3%": 154_987_616, "10.3%": 481_951_904, "17.3%": 808_878_672},
    "rental_assistance": {"3.3%": 106_054_400, "10.3%": 329_787_136, "17.3%": 553_491_840},
}
DHS_FEDERAL_TOTAL = {"3.3%": 2_479_093_994, "10.3%": 7_708_919_457, "17.3%": 12_938_100_184}
DHS_PRINTED_COMBINED_PRIMARY = 13_045_067_259  # Table IV.16
FMAP = 0.59
MATCHED = ("medicaid", "chip")


def gate(name, ok, **detail):
    if not ok:
        raise SystemExit(f"[BLOCKED] gate {name} failed: {detail}")


def main() -> None:
    spec = importlib.util.spec_from_file_location("dist_base", FISCAL / "distribution_weights_2026_09_23/distribute.py")
    B = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(B)
    d = B.load_cps()
    with zipfile.ZipFile(B.PATHS["cps"]) as z:
        p = pd.read_csv(z.open("pppub25.csv"), usecols=["PH_SEQ", "PPPOS", "MCAID", "PCHIP", "SSI_YN", "PAW_YN",
                                                         "WICYN"])
        h = pd.read_csv(z.open("hhpub25.csv"), usecols=["H_SEQ", "HFDVAL", "HPUBLIC", "HLORENT"]
                        ).rename(columns={"H_SEQ": "PH_SEQ"})
    d = d.merge(p, on=["PH_SEQ", "PPPOS"], validate="one_to_one", how="left")
    d = d.merge(h, on="PH_SEQ", validate="many_to_one", how="left")
    d = reweight(d, B.PATHS["cps"], gate, "lineage")

    frame = json.loads(DECOMP.read_text())["frame"]["row4"]
    civ, tgt = d.civ.to_numpy(), d.target.to_numpy()
    lw, r4 = d.pw.to_numpy(float), d.pw_row4.to_numpy(float)
    gate("lineage_is_the_decompositions_NG", abs(lw[tgt].sum() - frame["NG"]) < 1e-2)
    gate("row4_civilians_are_the_decompositions_NC", abs(r4[civ].sum() - frame["NC"]) < 1.0)

    for k in DHS_FEDERAL_TOTAL:
        s = sum(v[k] for v in DHS_FEDERAL.values())
        gate(f"dhs_federal_lines_add_{k}", abs(s - DHS_FEDERAL_TOTAL[k]) <= 2, sum=s, printed=DHS_FEDERAL_TOTAL[k])

    noncit_hh = d.PRCITSHP.eq(5).groupby(d.PH_SEQ).transform("any").to_numpy() & civ
    n_civ = d.groupby("PH_SEQ").civ.transform("sum").to_numpy()
    rental_hh = (d.HPUBLIC.eq(1) | d.HLORENT.eq(1)).to_numpy()
    pops = {
        "medicaid": d.MCAID.eq(1).to_numpy(),
        "chip": d.PCHIP.eq(1).to_numpy(),
        "wic": d.WICYN.eq(1).to_numpy(),
        "snap": (d.HFDVAL > 0).to_numpy(),
        "tanf": d.PAW_YN.eq(1).to_numpy(),
        "ssi": d.SSI_YN.eq(1).to_numpy(),
        "rental_assistance": rental_hh,
    }
    rows, shares = [], {}
    for prog, flag in pops.items():
        m = flag & noncit_hh
        unit = np.where(m, 1.0 / np.maximum(n_civ, 1), 0.0) if prog == "rental_assistance" else m.astype(float)
        den = float((unit * r4).sum())
        num_lin = float((unit * lw)[tgt].sum())
        num_r4 = float((unit * r4)[tgt].sum())
        gate(f"{prog}_population_positive", den > 0)
        s_lin, s_r4 = num_lin / den, num_r4 / den
        gate(f"{prog}_share_in_unit_interval", 0 < s_r4 <= s_lin < 1, lineage=s_lin, row4=s_r4)
        shares[prog] = (s_lin, s_r4)
        rows.append({"programme": prog, "unit": "household" if prog == "rental_assistance" else "person",
                     "records": int(m.sum()), "population_row4": round(den),
                     "share_lineage_weights": round(s_lin, 6), "share_row4_weights": round(s_r4, 6),
                     **{f"dhs_federal_{k}": v for k, v in DHS_FEDERAL[prog].items()}})

    summary = {"lane": "public_charge_share_2026_10_07", "rates": {}}
    for k in DHS_FEDERAL_TOTAL:
        fed = DHS_FEDERAL_TOTAL[k]
        state = sum(DHS_FEDERAL[p][k] for p in MATCHED) * (1 - FMAP) / FMAP
        out = {"dhs_federal_bn": fed / 1e9, "combined_matched_only_bn": (fed + state) / 1e9}
        for i, label in enumerate(("lineage_weights", "row4_weights")):
            f_lin = sum(DHS_FEDERAL[p][k] * shares[p][i] for p in DHS_FEDERAL)
            s_lin = sum(DHS_FEDERAL[p][k] * shares[p][i] for p in MATCHED) * (1 - FMAP) / FMAP
            out[label] = {"federal_bn": f_lin / 1e9, "combined_bn": (f_lin + s_lin) / 1e9,
                          "dollar_weighted_share": (f_lin + s_lin) / (fed + state)}
        summary["rates"][k] = out
    p_lin = summary["rates"]["10.3%"]["lineage_weights"]["dollar_weighted_share"]
    summary["at_dhs_printed_primary_bn"] = DHS_PRINTED_COMBINED_PRIMARY / 1e9 * p_lin
    summary["noncitizen_household_population_row4"] = float(r4[noncit_hh].sum())
    summary["lineage_share_of_that_population"] = float(lw[noncit_hh & tgt].sum() / r4[noncit_hh].sum())

    OUT.mkdir(exist_ok=True)
    with open(OUT / "public_charge_share.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]), lineterminator="\n")
        w.writeheader()
        w.writerows(rows)
    (OUT / "summary.json").write_text(json.dumps(summary, indent=1) + "\n")
    for r in rows:
        print(f"  ✓ {r['programme']:18s} n={r['records']:5d} share {r['share_lineage_weights']:.3f} "
              f"(row 4 {r['share_row4_weights']:.3f})")
    for k, v in summary["rates"].items():
        print(f"  ▸ {k}: lineage ${v['lineage_weights']['combined_bn']:.2f}bn of ${v['combined_matched_only_bn']:.2f}bn "
              f"(federal ${v['lineage_weights']['federal_bn']:.2f}bn; share {v['lineage_weights']['dollar_weighted_share']:.3f})")


if __name__ == "__main__":
    main()
