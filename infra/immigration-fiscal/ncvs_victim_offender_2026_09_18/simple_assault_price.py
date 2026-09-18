#!/usr/bin/env python3
"""Put a central price on a simple assault.

The lane's cost section previously carried simple assault twice, at $0 and at the
aggravated-assault price, a factor of 2.4 on 55-64% of the volume.  This script
replaces that range with a central figure and keeps the old two as bounds.

What the sources actually contain, established here and not assumed:

  * **Miller et al. (2021)**, JBCA 12(1):24-54, publishes ONE pooled "Assault" cost
    per crime, $29,326 in 2017 dollars (table 5; table 8 gives a 95% interval of
    $24,975-$33,681, CV 0.076).  It does **not** publish simple assault separately,
    with or without injury.  Its table 4 does split the incidence: 7,492,068 simple
    and 1,417,526 aggravated assaults, so the priced category is 84.1% simple
    assault by count and the pooled price is an upper bound on simple assault.
  * **Miller, Cohen & Wiersema (1996)**, NIJ NCJ 155282, table 2, publishes
    "Other Assault or Attempt" split by injury: with injury $24,000 and no injury
    $2,000 (1993 dollars), tangible $4,800 / $200 and quality of life $19,300 /
    $1,700.  That is the injury relativity Miller 2021 lacks.
  * **NCVS (N-DASH)** gives the injury share: 12.88% of simple assaults and 24.26%
    of aggravated assaults injure the victim, pooled 2022-2024.

Four routes, then one central figure.

Run:
  cd /Users/alien/Projects/immigration-research/infra/immigration-fiscal/ncvs_victim_offender_2026_09_18
  PYTHONUNBUFFERED=1 uv run --no-project --with "pandas>=2" --with "numpy>=2" python3 simple_assault_price.py
"""
from __future__ import annotations

import csv
import subprocess
import sys
from pathlib import Path

import pandas as pd

HERE = Path(__file__).resolve().parent
CACHE = HERE / "_cache"
DERIVED = HERE / "derived"

FAILS: list[str] = []
_lines: list[str] = []


def say(s: str = "") -> None:
    print(s)
    _lines.append(s)


def gate(name: str, ok: bool, detail: str) -> None:
    say(f"  {'✓' if ok else '✗'} [{name}] {detail}")
    if not ok:
        FAILS.append(name)


def header(s: str) -> None:
    say()
    say(f"[{s}]")


# ---------------------------------------------------------------------------
# Transcribed values.  Every one is gated against the extracted PDF text below.
# ---------------------------------------------------------------------------
# Miller et al. 2021, table 5, "Assault" row, 2017 dollars.
# medical, mental health, productivity, property, public services,
# adjudication+sanctioning, perpetrator work loss, tangible subtotal, QoL, total
M21_ASSAULT = {
    "medical": 1734, "mental_health": 177, "productivity": 1192, "property": 44,
    "public_services": 1891, "adjudication_sanctioning": 2705,
    "perpetrator_work_loss": 1002, "tangible": 8745, "qol": 20581, "total": 29326,
}
# Miller et al. 2021, table 4, assault incidence and arrests.
M21_COUNTS = {
    "assault_total": 8909594, "aggravated": 1417526, "simple": 7492068,
    "arrests_assault": 1451297, "arrests_aggravated": 388927, "arrests_simple": 1062370,
}
# Miller et al. 2021, table 8, 95% limits for the pooled assault unit cost.
M21_ASSAULT_CI = (24975, 33681)
# Miller et al. 2021, table 5, the other violent offences this lane prices.
M21_OTHER = {
    "rape": {"tangible": 11923, "qol": 214518, "total": 226441,
             "public_services": 25, "adjudication_sanctioning": 852},
    "other_sexual_assault": {"tangible": 4627, "qol": 82507, "total": 87134,
                             "public_services": 51, "adjudication_sanctioning": 328},
    "robbery": {"tangible": 16578, "qol": 11145, "total": 27723,
                "public_services": 647, "adjudication_sanctioning": 6754},
}
# Miller, Cohen & Wiersema 1996, table 2, 1993 dollars.
M96_ASSAULT = {
    "pooled": {"tangible": 1550, "qol": 7800, "total": 9400},
    "injured": {"tangible": 4800, "qol": 19300, "total": 24000},
    "not_injured": {"tangible": 200, "qol": 1700, "total": 2000},
}
# McCollister, French & Fang 2010, table 5, aggravated assault, 2008 dollars.
MCC_ASSAULT = {"victim": 8700, "cjs": 8641, "career": 2126,
               "intangible": 95023, "total": 107020}


def pdf_text(pdf: str, txt: str) -> str:
    t = CACHE / txt
    if not t.exists():
        subprocess.run(["pdftotext", "-layout", str(CACHE / pdf), str(t)], check=True)
    return t.read_text(errors="replace")


def toks(v: float) -> list[str]:
    """Both renderings of a number: Cambridge drops the comma in four-digit figures."""
    n = int(v)
    return [f"{n:,}", f"{n}"] if abs(n) >= 1000 else [f"{n}"]


def gate_transcription() -> None:
    m21 = pdf_text("miller2021_jbca.pdf", "miller2021_jbca.txt")
    m96 = pdf_text("victcost.pdf", "victcost.txt")
    checks = [
        ("miller2021", m21, [v for v in M21_ASSAULT.values()]
         + [v for v in M21_COUNTS.values()] + list(M21_ASSAULT_CI)
         + [x for d in M21_OTHER.values() for x in d.values()]),
        ("miller1996", m96, [x for d in M96_ASSAULT.values() for x in d.values()]),
    ]
    for label, text, vals in checks:
        missing = [toks(v)[0] for v in vals if not any(t in text for t in toks(v))]
        gate(f"transcription_{label}", not missing,
             f"{len(vals)} values checked against the PDF text, {len(missing)} missing"
             + (f": {missing}" if missing else ""))
    # Miller 2021 does not price simple assault; prove it rather than assert it.
    lines = [ln for ln in m21.splitlines() if "imple assault" in ln]
    priced = [ln for ln in lines if "$" in ln]
    gate("miller2021_has_no_simple_assault_price", not priced,
         f"{len(lines)} lines mention simple assault, {len(priced)} of them carry a "
         "dollar figure — the cost tables price 'Assault' as one category")
    # The published tangible + QoL must equal the published total.
    gate("m21_components_sum",
         M21_ASSAULT["tangible"] + M21_ASSAULT["qol"] == M21_ASSAULT["total"],
         f"{M21_ASSAULT['tangible']:,} + {M21_ASSAULT['qol']:,} = {M21_ASSAULT['total']:,}")
    parts = sum(M21_ASSAULT[k] for k in
                ("medical", "mental_health", "productivity", "property",
                 "public_services", "adjudication_sanctioning", "perpetrator_work_loss"))
    gate("m21_tangible_sum", abs(parts - M21_ASSAULT["tangible"]) <= 1,
         f"the seven tangible columns sum to {parts:,} against the published "
         f"{M21_ASSAULT['tangible']:,}")
    gate("m21_counts_sum",
         M21_COUNTS["simple"] + M21_COUNTS["aggravated"] == M21_COUNTS["assault_total"],
         f"{M21_COUNTS['simple']:,} + {M21_COUNTS['aggravated']:,} = "
         f"{M21_COUNTS['assault_total']:,}")


def main() -> None:
    cpi = dict(pd.read_csv(DERIVED / "cpi_u_annual.csv").itertuples(index=False, name=None))
    f93 = cpi[2024] / cpi[1993]
    f17 = cpi[2024] / cpi[2017]
    f08 = cpi[2024] / cpi[2008]

    header("transcription gates")
    gate_transcription()
    say(f"  CPI-U factors to 2024 dollars: 1993 x{f93:.4f}, 2008 x{f08:.4f}, 2017 x{f17:.4f}")

    # ------------------------------------------------------------------
    header("NCVS injury share by assault type, pooled 2022-2024")
    # ------------------------------------------------------------------
    nd = pd.read_csv(CACHE / "nd_person_injury_all.csv")
    nd.columns = [c.strip().lstrip("﻿") for c in nd.columns]
    inj = (
        nd[(nd.year.between(2022, 2024))
           & (nd.crimeType.isin(["Simple assault", "Aggravated assault"]))]
        .groupby(["crimeType", "levelDesc1"])["count"].sum().unstack()
    )
    inj["share_injured"] = inj["Injured"] / (inj["Injured"] + inj["Not injured"])
    say(inj.assign(share_injured=lambda d: d.share_injured.round(4)).to_string())
    p_simple = float(inj.loc["Simple assault", "share_injured"])
    p_agg = float(inj.loc["Aggravated assault", "share_injured"])
    gate("injury_share_ordering", p_agg > p_simple,
         f"aggravated {p_agg:.4f} > simple {p_simple:.4f}, as the NCVS definitions require")
    # Injury share across the pooled category Miller prices, weighted by his counts.
    w_s = M21_COUNTS["simple"] / M21_COUNTS["assault_total"]
    w_a = M21_COUNTS["aggravated"] / M21_COUNTS["assault_total"]
    p_pooled = w_s * p_simple + w_a * p_agg
    say(f"  Miller's priced category is {w_s:.1%} simple / {w_a:.1%} aggravated by count, "
        f"so its own injury share is {p_pooled:.4f}.")

    rows: list[dict] = []

    # ------------------------------------------------------------------
    header("route 1 — Miller 2021 pooled assault, reweighted to the simple-assault "
           "injury mix (CENTRAL)")
    # ------------------------------------------------------------------
    # Miller 2021 gives one number for a category whose injury share is p_pooled.
    # Miller 1996 gives the injured:uninjured cost relativity for the same offence
    # family.  Solve Miller 2021's pooled cost into an injured and an uninjured
    # branch at that relativity, then reweight to the simple-assault injury share.
    central = {}
    for comp in ("tangible", "qol", "total"):
        r = M96_ASSAULT["injured"][comp] / M96_ASSAULT["not_injured"][comp]
        c_pooled_17 = (M21_ASSAULT["tangible"] if comp == "tangible"
                       else M21_ASSAULT["qol"] if comp == "qol"
                       else M21_ASSAULT["total"])
        c_noinj = c_pooled_17 / (p_pooled * r + (1 - p_pooled))
        c_inj = r * c_noinj
        c_simple = p_simple * c_inj + (1 - p_simple) * c_noinj
        c_agg = p_agg * c_inj + (1 - p_agg) * c_noinj
        central[comp] = {"ratio": r, "not_injured_2017": c_noinj, "injured_2017": c_inj,
                         "simple_2017": c_simple, "aggravated_2017": c_agg}
        say(f"  {comp:9s} 1996 injured:uninjured ratio {r:5.2f} -> uninjured ${c_noinj:,.0f}, "
            f"injured ${c_inj:,.0f}; simple ${c_simple:,.0f}, aggravated ${c_agg:,.0f} (2017$)")
    # Reconstruction check: the count-weighted simple/aggravated split must return
    # the published pooled cost.
    recon = w_s * central["total"]["simple_2017"] + w_a * central["total"]["aggravated_2017"]
    gate("route1_reconstructs_pooled", abs(recon - M21_ASSAULT["total"]) < 1.0,
         f"count-weighted split returns ${recon:,.0f} against the published "
         f"${M21_ASSAULT['total']:,}")
    r1_total = central["total"]["simple_2017"] * f17
    r1_tang = central["tangible"]["simple_2017"] * f17
    r1_qol = central["qol"]["simple_2017"] * f17
    # Criminal-justice component: Miller's public services + adjudication and
    # sanctioning, scaled by simple assault's own arrest probability.  Perpetrator
    # work loss is forgone output, not a public budget line, so it is excluded.
    arr_pooled = M21_COUNTS["arrests_assault"] / M21_COUNTS["assault_total"]
    arr_simple = M21_COUNTS["arrests_simple"] / M21_COUNTS["simple"]
    cjs_pooled_17 = (M21_ASSAULT["public_services"]
                     + M21_ASSAULT["adjudication_sanctioning"])
    r1_cjs = cjs_pooled_17 * (arr_simple / arr_pooled) * f17
    say(f"  arrest probability: pooled assault {arr_pooled:.4f}, simple assault "
        f"{arr_simple:.4f}, ratio {arr_simple / arr_pooled:.3f}")
    say(f"  CENTRAL simple assault: ${r1_total:,.0f} in 2024 dollars "
        f"(tangible ${r1_tang:,.0f}, quality of life ${r1_qol:,.0f}, "
        f"criminal-justice component ${r1_cjs:,.0f})")
    rows.append({"route": "1_miller2021_reweighted",
                 "source": "Miller et al. 2021 JBCA table 5 + table 4; injury relativity "
                           "from Miller, Cohen & Wiersema 1996 NCJ 155282 table 2; "
                           "injury shares from NCVS N-DASH 2022-2024",
                 "source_year": 2017, "tangible_2024": r1_tang, "qol_2024": r1_qol,
                 "cjs_component_2024": r1_cjs, "total_2024": r1_total})

    # Uncertainty from Miller's own 95% interval on the pooled assault cost.
    lo, hi = (v / M21_ASSAULT["total"] * r1_total for v in M21_ASSAULT_CI)
    say(f"  carrying Miller's own 95% interval on the pooled cost: ${lo:,.0f} to ${hi:,.0f}")

    # ------------------------------------------------------------------
    header("route 2 — Miller, Cohen & Wiersema 1996, applied directly")
    # ------------------------------------------------------------------
    r2 = {}
    for comp in ("tangible", "qol", "total"):
        r2[comp] = (p_simple * M96_ASSAULT["injured"][comp]
                    + (1 - p_simple) * M96_ASSAULT["not_injured"][comp]) * f93
    say(f"  ${r2['total']:,.0f} in 2024 dollars (tangible ${r2['tangible']:,.0f}, "
        f"quality of life ${r2['qol']:,.0f})")
    say("  Lower than route 1 because the 1996 study values lost quality of life far below "
        "the QALY-based 2021 method, and real incomes rose over the 24 years between them.")
    rows.append({"route": "2_miller1996_direct",
                 "source": "Miller, Cohen & Wiersema 1996 NCJ 155282 table 2, "
                           "'Other Assault or Attempt' injured and not-injured rows, "
                           "weighted by the NCVS simple-assault injury share",
                 "source_year": 1993, "tangible_2024": r2["tangible"],
                 "qol_2024": r2["qol"], "cjs_component_2024": float("nan"),
                 "total_2024": r2["total"]})

    # ------------------------------------------------------------------
    header("route 3 — derivation from NCVS-priced components (a bracket, not an estimate)")
    # ------------------------------------------------------------------
    # Tangible victim cost: Miller 2021's medical + mental health + productivity for
    # pooled assault, scaled by the simple-to-pooled injury ratio, since those three
    # columns are injury-driven.  Plus the criminal-justice component from route 1.
    # No quality of life at all, so this is a tangible floor.
    victim_pooled_17 = sum(M21_ASSAULT[k] for k in ("medical", "mental_health", "productivity"))
    r3_victim = victim_pooled_17 * (p_simple / p_pooled) * f17
    r3_cjs_floor = cjs_pooled_17 * (arr_simple / arr_pooled) * f17
    # Ceiling on the criminal-justice channel: McCollister's assault CJS cost, which
    # is built for aggravated assault, so it bounds the simple-assault figure above.
    r3_cjs_ceiling = MCC_ASSAULT["cjs"] * f08
    r3_lo = r3_victim + r3_cjs_floor
    r3_hi = r3_victim + r3_cjs_ceiling
    say(f"  victim tangible (medical, mental health, productivity), injury-scaled: "
        f"${r3_victim:,.0f}")
    say(f"  criminal-justice channel: ${r3_cjs_floor:,.0f} (simple-assault arrest rate on "
        f"Miller's public-service and adjudication columns) to ${r3_cjs_ceiling:,.0f} "
        f"(McCollister's aggravated-assault criminal-justice cost, a ceiling)")
    say(f"  bracket, tangible only, no quality of life: ${r3_lo:,.0f} to ${r3_hi:,.0f}")
    rows.append({"route": "3_derived_tangible_bracket_low",
                 "source": "Miller et al. 2021 table 5 victim columns scaled by the NCVS "
                           "injury ratio, plus the simple-assault arrest-rate-scaled "
                           "criminal-justice columns; no quality of life",
                 "source_year": 2017, "tangible_2024": r3_lo, "qol_2024": 0.0,
                 "cjs_component_2024": r3_cjs_floor, "total_2024": r3_lo})
    rows.append({"route": "3_derived_tangible_bracket_high",
                 "source": "as above with McCollister 2010 aggravated-assault "
                           "criminal-justice cost as the ceiling on that channel",
                 "source_year": 2017, "tangible_2024": r3_hi, "qol_2024": 0.0,
                 "cjs_component_2024": r3_cjs_ceiling, "total_2024": r3_hi})

    # ------------------------------------------------------------------
    header("route 4 — residual against McCollister's aggravated-assault price")
    # ------------------------------------------------------------------
    # If aggravated assault costs what McCollister says, the simple-assault cost is
    # whatever makes Miller's published pooled assault total come out right.
    mcc_agg_17 = MCC_ASSAULT["total"] * (cpi[2017] / cpi[2008])
    r4_17 = (M21_ASSAULT["total"] * M21_COUNTS["assault_total"]
             - mcc_agg_17 * M21_COUNTS["aggravated"]) / M21_COUNTS["simple"]
    r4 = r4_17 * f17
    say(f"  McCollister aggravated assault in 2017 dollars: ${mcc_agg_17:,.0f}")
    say(f"  residual simple-assault cost: ${r4:,.0f} in 2024 dollars")
    say("  This route is fragile and is reported as a lower bound only.  McCollister's")
    say("  intangible cost for aggravated assault comes from jury awards and is five times")
    say(f"  Miller's whole quality-of-life figure for the pooled category, so the residual")
    say("  is a small difference between two large numbers from incompatible methods.")
    rows.append({"route": "4_residual_against_mccollister",
                 "source": "Miller et al. 2021 pooled assault total and table 4 counts, "
                           "minus McCollister 2010 aggravated assault",
                 "source_year": 2017, "tangible_2024": float("nan"),
                 "qol_2024": float("nan"), "cjs_component_2024": float("nan"),
                 "total_2024": r4})

    # Bounds retained from the old arms.
    rows.append({"route": "bound_zero_legacy_arm", "source": "the lane's old lower arm",
                 "source_year": 2024, "tangible_2024": 0.0, "qol_2024": 0.0,
                 "cjs_component_2024": 0.0, "total_2024": 0.0})
    rows.append({"route": "bound_aggravated_legacy_arm",
                 "source": "McCollister 2010 aggravated assault, the lane's old upper arm",
                 "source_year": 2008, "tangible_2024":
                     (MCC_ASSAULT["total"] - MCC_ASSAULT["intangible"]) * f08,
                 "qol_2024": MCC_ASSAULT["intangible"] * f08,
                 "cjs_component_2024": MCC_ASSAULT["cjs"] * f08,
                 "total_2024": MCC_ASSAULT["total"] * f08})
    rows.append({"route": "bound_miller2021_pooled_assault",
                 "source": "Miller et al. 2021 pooled assault, an upper bound because "
                           "15.9% of the priced category is aggravated assault",
                 "source_year": 2017,
                 "tangible_2024": M21_ASSAULT["tangible"] * f17,
                 "qol_2024": M21_ASSAULT["qol"] * f17,
                 "cjs_component_2024": cjs_pooled_17 * f17,
                 "total_2024": M21_ASSAULT["total"] * f17})

    # ------------------------------------------------------------------
    header("the central figure: anchoring on the aggravated-to-simple cost ratio")
    # ------------------------------------------------------------------
    # Everything above reduces to one parameter.  Miller 2021 prices a category that
    # is w_s simple and w_a aggravated, so if aggravated assault costs k times simple
    # assault, C_simple = C_pooled / (w_s + w_a * k).  The two substantive routes are
    # two values of k, and they disagree because they import k from incompatible
    # costing methods.
    pooled_24 = M21_ASSAULT["total"] * f17
    k1 = central["total"]["aggravated_2017"] / central["total"]["simple_2017"]
    k4 = (MCC_ASSAULT["total"] * f08) / r4
    k_central = (k1 * k4) ** 0.5
    for label, k in (("route 1, from the 1996 injury relativity", k1),
                     ("route 4, from McCollister's aggravated-assault price", k4),
                     ("central, the geometric mean of the two", k_central)):
        say(f"  k = {k:5.2f}  ->  simple assault ${pooled_24 / (w_s + w_a * k):>9,.0f}   "
            f"({label})")
    say()
    say("  k has to clear two floors that come from the NCVS itself: aggravated assault "
        "injures")
    say(f"  the victim {p_agg / p_simple:.2f} times as often as simple assault, and leads to "
        f"an arrest")
    say(f"  {(M21_COUNTS['arrests_aggravated'] / M21_COUNTS['aggravated']) / arr_simple:.2f} "
        "times as often, and it is more severe conditional on each.  So route 1's")
    say(f"  k of {k1:.2f} is below what the survey alone implies, while route 4's {k4:.1f} "
        "carries a")
    say("  jury-award intangible into a QALY-based total.  The geometric mean is the")
    say("  transparent compromise and every downstream number is given against k.")

    c_central = pooled_24 / (w_s + w_a * k_central)
    gate("k_central_clears_the_ncvs_floors",
         k_central > max(p_agg / p_simple,
                         (M21_COUNTS["arrests_aggravated"] / M21_COUNTS["aggravated"])
                         / arr_simple),
         f"k = {k_central:.2f} exceeds the injury ratio {p_agg / p_simple:.2f} and the "
         f"arrest ratio "
         f"{(M21_COUNTS['arrests_aggravated'] / M21_COUNTS['aggravated']) / arr_simple:.2f}")
    # Components: the tangible side is built from Miller's own columns (route 3 low,
    # which is independently bracketed above); quality of life is the residual.
    c_tang = r3_lo
    c_qol = c_central - c_tang
    gate("central_qol_positive", c_qol > 0,
         f"tangible ${c_tang:,.0f} from Miller's own columns leaves ${c_qol:,.0f} of "
         "quality-of-life cost inside the central total")
    say()
    say(f"  CENTRAL SIMPLE ASSAULT: ${c_central:,.0f} (2024 dollars) = tangible "
        f"${c_tang:,.0f} (of which criminal-justice ${r1_cjs:,.0f}) + quality of life "
        f"${c_qol:,.0f}")

    sens = pd.DataFrame([
        {"k_aggravated_over_simple": k, "simple_assault_2024": pooled_24 / (w_s + w_a * k)}
        for k in (1.5, 2, 3, k_central, 5, 7, 10, 13)
    ])
    sens.to_csv(DERIVED / "simple_assault_sensitivity_to_k.csv", index=False)
    say()
    say(sens.round(2).to_string(index=False))

    rows.insert(0, {"route": "0_CENTRAL_k_anchored",
                    "source": f"Miller et al. 2021 pooled assault ${pooled_24:,.0f} (2024$) "
                              f"split at an aggravated-to-simple cost ratio of "
                              f"k={k_central:.2f}, the geometric mean of the ratio implied "
                              f"by route 1 (k={k1:.2f}) and route 4 (k={k4:.2f}); tangible "
                              "components from Miller's own columns, quality of life the "
                              "residual",
                    "source_year": 2017, "tangible_2024": c_tang, "qol_2024": c_qol,
                    "cjs_component_2024": r1_cjs, "total_2024": c_central})

    out = pd.DataFrame(rows)
    out.to_csv(DERIVED / "simple_assault_unit_cost.csv", index=False)
    header("simple assault unit cost, every route, 2024 dollars")
    say(out[["route", "source_year", "tangible_2024", "qol_2024",
             "cjs_component_2024", "total_2024"]].round(0).to_string(index=False))

    gate("central_below_aggravated", c_central < MCC_ASSAULT["total"] * f08,
         f"the central simple-assault price ${c_central:,.0f} is "
         f"{MCC_ASSAULT['total'] * f08 / c_central:.1f}x below the aggravated-assault price "
         f"the old upper arm used")
    gate("central_below_miller_pooled", c_central < M21_ASSAULT["total"] * f17,
         f"${c_central:,.0f} is below Miller's pooled assault cost "
         f"${M21_ASSAULT['total'] * f17:,.0f}, which is the arithmetic upper bound on a "
         "category that is 84.1% simple assault")
    span = max(r2["total"], r1_total, r4) / min(r2["total"], r1_total, r4)
    say()
    say(f"  The three substantive routes span a factor of {span:.1f} "
        f"(${min(r2['total'], r1_total, r4):,.0f} to "
        f"${max(r2['total'], r1_total, r4):,.0f}), against the factor the old "
        f"zero-to-aggravated arms left open, which was unbounded below and "
        f"${MCC_ASSAULT['total'] * f08:,.0f} above.")

    # A Miller-2021 price set for every offence the lane prices, so the cost model can
    # run entirely inside one costing framework.
    header("a complete Miller 2021 price set for the four NCVS offence categories")
    # NCVS "rape/sexual assault" pools Miller's rape and other sexual assault; weight
    # them by Miller's own table 4 incidence.
    n_rape, n_osa = 4938892, 3856756
    ws = n_rape / (n_rape + n_osa)
    rsa = {k: ws * M21_OTHER["rape"][k] + (1 - ws) * M21_OTHER["other_sexual_assault"][k]
           for k in ("tangible", "qol", "total", "public_services",
                     "adjudication_sanctioning")}
    price_rows = [
        {"ncvs_offence": "Rape/sexual assault", "total_2024": rsa["total"] * f17,
         "cjs_2024": (rsa["public_services"] + rsa["adjudication_sanctioning"]) * f17},
        {"ncvs_offence": "Robbery", "total_2024": M21_OTHER["robbery"]["total"] * f17,
         "cjs_2024": (M21_OTHER["robbery"]["public_services"]
                      + M21_OTHER["robbery"]["adjudication_sanctioning"]) * f17},
        {"ncvs_offence": "Aggravated assault",
         "total_2024": c_central * k_central,
         "cjs_2024": cjs_pooled_17 * ((M21_COUNTS["arrests_aggravated"]
                                       / M21_COUNTS["aggravated"]) / arr_pooled) * f17},
        {"ncvs_offence": "Simple assault", "total_2024": c_central, "cjs_2024": r1_cjs},
    ]
    prices = pd.DataFrame(price_rows)
    prices.to_csv(DERIVED / "miller2021_price_set.csv", index=False)
    say(prices.round(0).to_string(index=False))
    say()
    say("Miller's rape and other-sexual-assault rows are pooled at his own incidence "
        f"weights ({ws:.1%} rape) to match the single NCVS category.")

    (DERIVED / "simple_assault_price_log.txt").write_text("\n".join(_lines) + "\n")
    if FAILS:
        raise SystemExit("gates failed: " + ", ".join(FAILS))
    say()
    say("[done] simple_assault_price.py")
    (DERIVED / "simple_assault_price_log.txt").write_text("\n".join(_lines) + "\n")


if __name__ == "__main__":
    sys.exit(main())
