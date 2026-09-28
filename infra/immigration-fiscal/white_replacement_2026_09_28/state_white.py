"""Part F: state-specific replacement. The union in California replaced by California's third-plus NH whites, the
union in Texas by Texas's, and the union elsewhere by the national third-plus NH white rates; Los Angeles as an
information row inside California.

rekey_white.py is imported (its module-level build, nothing written) and its run() prices each piece:
  union pieces   the union's CPS persons in the region (factor 1). Lines the rough run keeps at the engine's national
                 union share (Medicare, Medicaid, justice, other public health, VA, TRICARE) are split within the union
                 by the piece's share of the union on a CPS proxy key (Medicare coverage, veterans' income, persons)
                 [INFERENCE]; the engine's union-specific lines (school reprice, college re-key, lane constants) by
                 pupils, college enrolment and persons; the production gain by earnings. What is left against the
                 national rough union (capital keys) is spread by persons and reported (gate |residual| < $1bn).
  white pieces   third-plus NH white CPS persons of the region (the rest of the US: of the whole country), reweighted
                 to the union piece's age structure ("union ages") or kept at their own ages ("own ages"), scaled to
                 the union piece's population. MEPS has no state: medical keys are the national US-born NH white
                 per-age rates at the piece's age structure [INFERENCE]; justice and LTSS as in A.
National lines, responses and per-unit prices are the case's; a state piece differs only through its CPS keys (earnings,
federal and state income tax, programme dollars, pupils, property) and age. Nothing is state-priced.

Delta = cost of the union piece less cost of the white piece (positive: the union costs other residents more). The
no-response balance (receipts less spending on full line amounts) is reported beside for the reconciliation with the
partial ledger of research/immigration-california-texas-fiscal-geography-2026-09-21.md.
Outputs: derived/state_summary.csv, derived/state_buckets.csv.
"""
import csv
import sys
import zipfile
from pathlib import Path

sys.dont_write_bytecode = True

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

LANE = Path(__file__).resolve().parent
sys.path.insert(0, str(LANE))
import rekey_white as R  # noqa: E402

DER = LANE / "derived"
# The partial ledger's age-matched gaps (union at its own ages against local third-plus NH whites) and standardized
# gaps (at local white ages), $ per person [DATA: ledger_stress_2026_09_17/derived/state_matched.csv,
# metro_match_2026_09_17/derived/metro_matched.csv via the 2026-09-21 memo]
PARTIAL = pd.read_csv(R.FISCAL / "ledger_stress_2026_09_17/derived/state_matched.csv")
PARTIAL = PARTIAL[(PARTIAL.scenario == "all_age_shared") & (PARTIAL.target == "mexican_observed_total")
                  & (PARTIAL.reference == "third_plus_nh_white")]
PARTIAL_CELLS = {"California": "CA_age", "Texas": "TX_age"}
NATIONAL_PARTIAL = float(PARTIAL[(PARTIAL.cells == "state_x_age") & (PARTIAL.metric == "gap_per_person")].estimate.iloc[0])
PARTIAL_LA = -17_196.0   # standardized, metro_match via the memo; not in state_matched.csv

with zipfile.ZipFile(R.ZIP) as z:
    hh = pd.read_csv(z.open("hhpub25.csv"), usecols=["H_SEQ", "GESTFIPS", "GTCBSA"]).rename(columns={"H_SEQ": "PH_SEQ"})
geo = R.d[["PH_SEQ"]].merge(hh, on="PH_SEQ", how="left", validate="many_to_one")
if geo.GESTFIPS.isna().any():
    raise SystemExit("[BLOCKED] CPS persons without a household state")
st = geo.GESTFIPS.to_numpy()
REGIONS = {"California": st == 6, "Texas": st == 48, "rest of US": (st != 6) & (st != 48)}
LA = geo.GTCBSA.to_numpy() == 31080
EXT = ["public_order_safety", "health_services", "medicare", "veterans_other", "military_medical",
       "medicaid_and_chip_other_medical"]
EXT_KEY = {"medicare": "mcare", "veterans_other": "vet", "military_medical": "vet"}   # else persons
ADJ_KEY = {"school_reprice": "k12", "college_rekey": "college", "lane_constants": "pc", "source_rounding": "pc"}
UNION = R.MASK["mex"]
W3 = R.MASK["w3"]


def union_piece(mask):
    cw = R.w * UNION * mask
    sc = R.keyed("mex", cw, float(cw.sum()), "own")
    full = R.w * UNION
    frac = {k: float((cw * v).sum() / (full * v).sum()) for k, v in R.K.items()}
    sc["name"] = "union_piece"
    sc["external"] = {lid: R.eng_share["spending|" + lid] * frac[EXT_KEY.get(lid, "pc")] for lid in EXT}
    sc["frac"] = frac
    return sc


def white_piece(mask, total, target_pi):
    """Third-plus NH whites of `mask`, at `target_pi` ages (None: their own), scaled to `total` persons."""
    m = W3 & mask
    if target_pi is None:
        cw = R.w * m * (total / float(R.w[m].sum()))
        pi = R.structure(m, R.w, R.cage)
    else:
        cw = R.reweight(m, R.w, R.cage, target_pi, total)
        pi = target_pi
    mfrac = (total / R.CPS_TOTAL) * float(R.mw.sum())
    mwt = R.reweight(R.MMASK["w3"], R.mw, R.mage, pi, mfrac)
    sc = R.keyed("w3", cw, total, "piece", mwt)
    sc["sample"] = int(m.sum())
    return sc


def priced(sc, end, adjust=None, arms=False):
    """run() plus, for union pieces, the engine's union-specific lines and production gain by the piece's keys.
    arms: A's two convention arms together (top tail spread by CPS income tax, capital-side taxes respond)."""
    r, rows, buckets = R.run(sc, end, "prop", True) if arms else R.run(sc, end)
    bal = {}
    for side, lid, nat, amt, resp in rows:
        b = next((k for k, v in R.BUCKETS.items() if lid in v), R.PER_HEAD)
        bal[b] = bal.get(b, 0.0) + (amt if side == "receipts" else -amt)
    cost, balance = r["cost"], r["balance"]
    if adjust is not None:
        e = R.case[end]
        for ln in e["lines"]:
            if ln["id"] in ADJ_KEY and ln["side"] == "spending":
                f = adjust[ADJ_KEY[ln["id"]]]
                b = "schools and colleges" if ln["id"] in ("school_reprice", "college_rekey") else R.PER_HEAD
                cost += ln["amount_bn"] * ln["response"] * f
                balance -= ln["amount_bn"] * f
                buckets[b] = buckets.get(b, 0.0) + ln["amount_bn"] * ln["response"] * f
                bal[b] = bal.get(b, 0.0) - ln["amount_bn"] * f
        prod = [x for x in e["lines"] if x["side"] == "scalar" and x["id"] == "production_gain_bn"][0]["effect_bn"]
        cost -= prod * adjust["hi"]
        buckets["production gain (subtracted)"] = -prod * adjust["hi"]
    return cost, balance, buckets, bal


def write(name, rows):
    with open(DER / name, "w", newline="") as f:
        wr = csv.DictWriter(f, fieldnames=list(rows[0]), lineterminator="\n")
        wr.writeheader()
        wr.writerows(rows)


def main():
    rough = {end: R.run(R.scenario("mex"), end)[0] for end in ("low", "high")}
    pieces = {name: union_piece(m) for name, m in REGIONS.items()}
    pieces["Los Angeles metro"] = union_piece(LA)
    summary, bucket_rows = [], []
    for end in ("low", "high"):
        u = {name: priced(sc, end, sc["frac"]) for name, sc in pieces.items()}
        resid = rough[end]["cost"] - sum(u[n][0] for n in REGIONS)
        resid_bal = rough[end]["balance"] - sum(u[n][1] for n in REGIONS)
        if abs(resid) > 1.0 or abs(resid_bal) > 1.0:
            raise SystemExit(f"[BLOCKED] union pieces miss the rough union by {resid:.3f} / {resid_bal:.3f}bn ({end})")
        print(f"[gate] {end}: union pieces sum to the rough union within {resid:+.3f}bn cost, {resid_bal:+.3f}bn balance;"
              " spread by persons")
        totals = {k: {"union": 0.0, "white_union_ages": 0.0, "white_own_ages": 0.0,
                      "bal_union": 0.0, "bal_white_union_ages": 0.0, "bal_white_own_ages": 0.0,
                      "arms_union": 0.0, "arms_white": 0.0} for k in ("sum",)}
        for name, sc in pieces.items():
            pop = sc["population"]
            share = sc["frac"]["pc"]
            uc = u[name][0] + resid * share
            ua = priced(sc, end, sc["frac"], arms=True)[0] + resid * share
            ub = u[name][1] + resid_bal * share
            wmask = REGIONS.get(name, LA) if name != "rest of US" else np.ones(len(R.d), bool)
            pi_union = R.structure(UNION & (REGIONS.get(name, LA)), R.w, R.cage)
            wu = white_piece(wmask, pop, pi_union)
            wo = white_piece(wmask, pop, None)
            cu, bu, bku, blu = priced(wu, end)
            co, bo, _, _ = priced(wo, end)
            ca = priced(wu, end, arms=True)[0]
            row = {"region": name, "end": end, "spec": R.case[end]["spec"], "union_persons": f"{pop:.0f}",
                   "white_cps_sample": wu["sample"], "white_rates_from": "national" if name == "rest of US" else name,
                   "cost_union_bn": f"{uc:.4f}", "cost_white_union_ages_bn": f"{cu:.4f}",
                   "cost_white_own_ages_bn": f"{co:.4f}",
                   "delta_union_ages_bn": f"{uc - cu:.4f}", "delta_own_ages_bn": f"{uc - co:.4f}",
                   "delta_union_ages_per_person": f"{(uc - cu) * 1e9 / pop:.0f}",
                   "delta_own_ages_per_person": f"{(uc - co) * 1e9 / pop:.0f}",
                   "delta_union_ages_both_arms_per_person": f"{(ua - ca) * 1e9 / pop:.0f}",
                   "balance_gap_union_ages_per_person": f"{(ub - bu) * 1e9 / pop:.0f}",
                   "balance_gap_own_ages_per_person": f"{(ub - bo) * 1e9 / pop:.0f}"}
            cell = PARTIAL_CELLS.get(name)
            if cell:
                p = PARTIAL[PARTIAL.cells == cell].set_index("metric").estimate
                row["partial_ledger_gap_per_person"] = f"{p['gap_per_person']:.0f}"
                row["partial_ledger_standardized_per_person"] = f"{p['standardized_gap_per_person']:.0f}"
                row["partial_ledger_population"] = f"{PARTIAL[PARTIAL.cells == cell].population.iloc[0]:.0f}"
            else:
                row["partial_ledger_gap_per_person"] = ""
                row["partial_ledger_standardized_per_person"] = f"{PARTIAL_LA:.0f}" if name == "Los Angeles metro" else ""
                row["partial_ledger_population"] = ""
            summary.append(row)
            if name in REGIONS:
                for k, v in (("union", uc), ("white_union_ages", cu), ("white_own_ages", co), ("bal_union", ub),
                             ("bal_white_union_ages", bu), ("bal_white_own_ages", bo), ("arms_union", ua),
                             ("arms_white", ca)):
                    totals["sum"][k] += v
            if end == "low":
                ubk, ubl = u[name][2], u[name][3]
                for b in list(R.BUCKETS) + [R.PER_HEAD, "capital return", "production gain (subtracted)"]:
                    bucket_rows.append({"region": name, "bucket": b,
                                        "cost_union_bn": f"{ubk.get(b, 0.0):.4f}",
                                        "cost_white_union_ages_bn": f"{bku.get(b, 0.0):.4f}",
                                        "delta_cost_bn": f"{ubk.get(b, 0.0) - bku.get(b, 0.0):.4f}",
                                        "delta_cost_per_person": f"{(ubk.get(b, 0.0) - bku.get(b, 0.0)) * 1e9 / pop:.0f}",
                                        "balance_gap_bn": f"{ubl.get(b, 0.0) - blu.get(b, 0.0):.4f}",
                                        "balance_gap_per_person": f"{(ubl.get(b, 0.0) - blu.get(b, 0.0)) * 1e9 / pop:.0f}"})
        t = totals["sum"]
        pop = R.TARGET
        summary.append({"region": "sum of CA, TX and rest", "end": end, "spec": R.case[end]["spec"],
                        "union_persons": f"{sum(pieces[n]['population'] for n in REGIONS):.0f}", "white_cps_sample": "",
                        "white_rates_from": "state", "cost_union_bn": f"{t['union']:.4f}",
                        "cost_white_union_ages_bn": f"{t['white_union_ages']:.4f}",
                        "cost_white_own_ages_bn": f"{t['white_own_ages']:.4f}",
                        "delta_union_ages_bn": f"{t['union'] - t['white_union_ages']:.4f}",
                        "delta_own_ages_bn": f"{t['union'] - t['white_own_ages']:.4f}",
                        "delta_union_ages_per_person": f"{(t['union'] - t['white_union_ages']) * 1e9 / pop:.0f}",
                        "delta_own_ages_per_person": f"{(t['union'] - t['white_own_ages']) * 1e9 / pop:.0f}",
                        "delta_union_ages_both_arms_per_person": f"{(t['arms_union'] - t['arms_white']) * 1e9 / pop:.0f}",
                        "balance_gap_union_ages_per_person": f"{(t['bal_union'] - t['bal_white_union_ages']) * 1e9 / pop:.0f}",
                        "balance_gap_own_ages_per_person": f"{(t['bal_union'] - t['bal_white_own_ages']) * 1e9 / pop:.0f}",
                        "partial_ledger_gap_per_person": f"{NATIONAL_PARTIAL:.0f}",
                        "partial_ledger_standardized_per_person": "", "partial_ledger_population": ""})
    write("state_summary.csv", summary)
    write("state_buckets.csv", bucket_rows)
    pd.set_option("display.width", 250)
    s = pd.DataFrame(summary)
    print(s[["region", "end", "union_persons", "white_cps_sample", "cost_union_bn", "cost_white_union_ages_bn",
             "cost_white_own_ages_bn", "delta_union_ages_bn", "delta_own_ages_bn", "delta_union_ages_per_person",
             "delta_own_ages_per_person", "delta_union_ages_both_arms_per_person", "balance_gap_union_ages_per_person", "partial_ledger_gap_per_person",
             "partial_ledger_standardized_per_person"]].to_string(index=False))


if __name__ == "__main__":
    main()
