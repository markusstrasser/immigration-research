"""Interest on the fiscal gap: what deficit financing adds to the complete account.

Two objects, both arithmetic on stored repo outputs, no new estimation:

A. Aggregate. The complete resident account gives the Mexican-origin union an absolute
   annual balance of -263.2bn (ledger_absolute, waterfall step 14, central arms) and an
   age-matched gap of -361.1bn vs third-plus NH whites. If a constant annual flow B is
   financed by borrowing at rate r, the debt after N years is B*((1+r)^N - 1)/r; the
   interest component is that minus N*B; the interest bill in year N is r times the
   debt at the start of year N. Arms: 100% of the flow deficit-financed (upper bound,
   since states balance budgets) and a federal-only share, parameterised.

B. Per person. The pronatal lane's period profile (partial account, all_age_shared) is
   compounded FORWARD to age 83 instead of discounted back to the start age, so the
   sum is the terminal debt or asset a lifetime leaves at rate r. A uniform per-year
   shift equal to the complete-minus-partial per-person difference from the waterfall
   is applied as a second arm.

Rate anchors (fetched 2026-09-18 from Treasury FiscalData):
  net interest FY2024 = 879.879bn (OMB Table 3.2, params.json func_900_net_interest)
  debt held by the public 2023-09-29 = 26,330.14bn; 2024-09-30 = 28,307.31bn (debt_to_penny)
  effective rate = 879.879 / mean(26,330.14, 28,307.31) = 3.22%
"""
import json, pathlib
import numpy as np, pandas as pd

HERE = pathlib.Path(__file__).parent
FISCAL = HERE.parent
WATER = FISCAL / "ledger_absolute_2026_09_17/derived/waterfall.csv"
GAPS = FISCAL / "ledger_absolute_2026_09_17/derived/complete_gaps.csv"
PROF = FISCAL / "pronatal_equivalence_2026_09_18/derived/age_profiles_references.csv"
BANDS = {0: (0, 18), 1: (18, 25), 2: (25, 35), 3: (35, 45), 4: (45, 55), 5: (55, 65), 6: (65, 75), 7: (75, 83)}
NET_INTEREST_BN = 879.879
DEBT_START, DEBT_END = 26330.142473, 28307.312291
R_EFF = NET_INTEREST_BN / ((DEBT_START + DEBT_END) / 2)
RATES = {"effective_fy2024": R_EFF, "r3": 0.03, "r4": 0.04, "r5": 0.05}
HORIZONS = [10, 20, 30]
FED_SHARES = {"all_deficit": 1.0, "half_deficit": 0.5}


def aggregate():
    w = pd.read_csv(WATER)
    end = w[w.step == 14].set_index("group")
    g = pd.read_csv(GAPS)
    flows = {
        "union_absolute": float(end.loc["mexican_observed_total", "cumulative_bn"]),
        "union_gap_vs_white": float(g[(g.group == "mexican_observed_total") & (g.reference == "third_plus_nh_white")]
                                    .complete_age_matched_gap_bn.iloc[0]),
        "union_gap_vs_all_native": float(g[(g.group == "mexican_observed_total") & (g.reference == "all_native")]
                                         .complete_age_matched_gap_bn.iloc[0]),
    }
    rows = []
    for fname, B in flows.items():
        for sname, s in FED_SHARES.items():
            for rname, r in RATES.items():
                for N in HORIZONS:
                    debt = s * B * ((1 + r) ** N - 1) / r
                    principal = s * B * N
                    rows.append(dict(flow=fname, annual_flow_bn=B, deficit_share=s, rate_name=rname, rate=r, years=N,
                                     debt_bn=debt, principal_bn=principal, interest_component_bn=debt - principal,
                                     interest_in_year_N_bn=r * s * B * ((1 + r) ** (N - 1) - 1) / r))
    return pd.DataFrame(rows)


def per_person():
    prof = pd.read_csv(PROF).pivot(index="band", columns="group", values="balance_per_person")
    w = pd.read_csv(WATER)
    base = w[w.step == 0].set_index("group").cumulative_per_person
    end = w[w.step == 14].set_index("group").cumulative_per_person
    shift = (end - base)  # complete minus partial, per person-year, crude
    rows = []
    for g in prof.columns:
        sh = float(shift.get(g, np.nan))
        for arm, add in (("partial", 0.0), ("complete_uniform_shift", sh)):
            if np.isnan(add):
                continue
            for start in ([0, 25] if g == "mexico_born" else [0]):
                for rname, r in {"r0": 0.0, **RATES}.items():
                    fv = 0.0
                    for b, (lo, hi) in BANDS.items():
                        for age in range(lo, hi):
                            if age >= start:
                                fv += (prof.loc[b, g] + add) * (1 + r) ** (83 - age)
                    rows.append(dict(group=g, arm=arm, start_age=start, rate_name=rname, rate=r, terminal_value_at_83=fv))
    d = pd.DataFrame(rows)
    ref = d[(d.group == "third_plus_nh_white") & (d.start_age == 0)].set_index(["arm", "rate_name"]).terminal_value_at_83
    d["terminal_budget_vs_white_child"] = d.apply(lambda x: ref[(x.arm, x.rate_name)] - x.terminal_value_at_83, axis=1)
    return d, shift


def main():
    agg = aggregate(); agg.to_csv(HERE / "derived/aggregate_debt_paths.csv", index=False)
    pp, shift = per_person(); pp.to_csv(HERE / "derived/per_person_terminal_values.csv", index=False)
    json.dump(dict(effective_rate_fy2024=R_EFF, net_interest_bn=NET_INTEREST_BN, debt_start_bn=DEBT_START,
                   debt_end_bn=DEBT_END, complete_minus_partial_per_person_year=shift.dropna().round(2).to_dict()),
              open(HERE / "derived/audit.json", "w"), indent=2)
    pd.set_option("display.width", 220)
    print(f"effective rate FY2024 = {R_EFF:.4%}")
    a = agg[(agg.flow == "union_absolute") & (agg.deficit_share == 1.0)]
    print("\n[A] union absolute -263.2bn/yr, all deficit-financed: debt after N years, bn")
    print(a.pivot(index="years", columns="rate_name", values="debt_bn").round(0))
    print("interest component, bn"); print(a.pivot(index="years", columns="rate_name", values="interest_component_bn").round(0))
    print("interest bill in year N, bn"); print(a.pivot(index="years", columns="rate_name", values="interest_in_year_N_bn").round(0))
    print("\ncomplete-minus-partial per person-year:", shift.round(0).to_dict())
    print("\n[B] terminal value at 83 per person, partial profile (rows) and complete uniform-shift arm")
    for arm in ("partial", "complete_uniform_shift"):
        t = pp[pp.arm == arm].pivot(index=["group", "start_age"], columns="rate_name", values="terminal_value_at_83")
        print(f"\n arm={arm}"); print(t[["r0", "effective_fy2024", "r3", "r5"]].round(0))
    print("\n[B] terminal budget vs white child (what the reference child leaves minus what the target leaves), complete arm")
    t = pp[pp.arm == "complete_uniform_shift"].pivot(index=["group", "start_age"], columns="rate_name", values="terminal_budget_vs_white_child")
    print(t[["r0", "effective_fy2024", "r3", "r5"]].round(0))


if __name__ == "__main__":
    main()
