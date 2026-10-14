"""The Census coverage bound beside the main case: the 2020 PES Hispanic net undercount on the US-born members.

CPS weights are controlled to the Census Bureau's population estimates, so the survey's own Hispanic coverage
shortfall is already corrected; what remains is error in the controls. The 2020 Post-Enumeration Survey puts the
Hispanic net undercount at 4.99% (research/immigration-mexican-origin-population-total-2026-09-19.md section 3, "a
partly absorbed upper bound"). Audit row 4 corrects the Mexico-born only, so the bound applies to the US-born: G2 and
G3+ under the generation account's convention a (own and parents' birthplace), the added descendants included, because
the lineage count derives them from identity-loss rates on the identified population.

Bound = (1 / (1 - 0.0499) - 1) x the US-born generations' cost at each end of the case, proportional: it assumes the
missed members cost what the counted ones do, and it is not an engine run (the group-size responses and the production
term would move slightly). How much the Vintage 2024 controls already absorb is not measured.

Reads generation_account_2026_09_24/derived/generation_results_<key>.csv and the case's band from the case lane's
summary.json (main_case); writes derived/coverage_bound.csv and derived/coverage_bound.json. Run from the repository root:
    OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/coverage_bound_2026_10_14/coverage_bound.py
"""
import csv
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
LANE = Path(__file__).resolve().parent
KEY = "oct14"
CASE_LANE = "main_case_2026_10_14"
GEN = ROOT / f"infra/immigration-fiscal/generation_account_2026_09_24/derived/generation_results_{KEY}.csv"
SUMMARY = ROOT / f"infra/immigration-fiscal/{CASE_LANE}/derived/summary.json"
PES_UNDERCOUNT = 0.0499  # 2020 PES Hispanic net coverage error, -4.99% [SOURCE: 2020 PES Table B, via the population memo]
FACTOR = 1 / (1 - PES_UNDERCOUNT) - 1
US_BORN = ("G2", "G3plus")
TOL = 1e-6


def blocked(why):
    sys.exit(f"[BLOCKED] {why}")


def main():
    if not GEN.exists():
        blocked(f"missing {GEN.relative_to(ROOT)}: run the generation account on {KEY} first")
    rows = [r for r in csv.DictReader(GEN.open()) if r["convention"] == "a"]
    if not SUMMARY.exists():
        blocked(f"missing {SUMMARY.relative_to(ROOT)}")
    band = json.loads(SUMMARY.read_text())["main_case"]
    out, summary = [], {"key": KEY, "pes_hispanic_net_undercount": PES_UNDERCOUNT, "factor": FACTOR, "ends": {}}
    for i, end in enumerate(("low", "high")):
        by = {r["generation"]: r for r in rows if r["band_end"] == end}
        if set(by) != {"G1", "G2", "G3plus"}:
            blocked(f"convention a lacks a generation at the {end} end")
        total = sum(float(r["cost_bn"]) for r in by.values())
        case = float(band[i])
        if abs(total - case) > TOL:
            blocked(f"the generations add to {total:.6f}, not the case's {case:.6f} at the {end} end")
        us_cost = sum(float(by[g]["cost_bn"]) for g in US_BORN)
        us_pop = sum(float(by[g]["population"]) for g in US_BORN)
        bound = FACTOR * us_cost
        missed = FACTOR * us_pop  # the people the bound adds, at the counted members' average cost
        for g in US_BORN:
            out.append({"end": end, "allocation": by[g]["allocation"], "generation": g, "cost_bn": f"{float(by[g]['cost_bn']):.6f}",
                        "population": f"{float(by[g]['population']):.1f}", "bound_bn": f"{FACTOR * float(by[g]['cost_bn']):.6f}"})
        summary["ends"][end] = {"allocation": by["G2"]["allocation"], "case_bn": case, "us_born_cost_bn": us_cost,
                                "us_born_population": us_pop, "bound_bn": bound, "case_with_bound_bn": case + bound,
                                "implied_missed_people": missed}
    with (LANE / "derived" / "coverage_bound.csv").open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(out[0].keys()), lineterminator="\n")
        w.writeheader()
        w.writerows(out)
    (LANE / "derived" / "coverage_bound.json").write_text(json.dumps(summary, indent=1) + "\n")
    for end, s in summary["ends"].items():
        print(f"{end}: US-born {s['us_born_cost_bn']:.3f}bn on {s['us_born_population'] / 1e6:.3f}M -> bound +{s['bound_bn']:.3f}bn "
              f"(case {s['case_bn']:.3f} -> {s['case_with_bound_bn']:.3f})")


if __name__ == "__main__":
    main()
