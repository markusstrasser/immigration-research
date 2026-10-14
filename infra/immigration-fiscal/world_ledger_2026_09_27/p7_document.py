"""Render the P7 correction section from executed tables, retaining the historical record."""
import json
import re
from pathlib import Path

import pandas as pd
from valuation import case_payload

HERE = Path(__file__).resolve().parent
D = HERE / "derived"
START = "## P7 fixes (2026-10-14)"
END = "<!-- END P7 GENERATED -->"


def table(frame):
    cols = list(frame.columns)
    lines = ["| " + " | ".join(cols) + " |", "|" + "|".join(["---"] * len(cols)) + "|"]
    for row in frame.itertuples(index=False, name=None):
        lines.append("| " + " | ".join(str(x).replace("|", "/") for x in row) + " |")
    return "\n".join(lines)


def number(x):
    return f"{x:,.3f}"


def qualify_history(prefix):
    """Resolve legacy prose labels; numerical historical evidence remains intact."""
    rows = []
    for i, line in enumerate(prefix.splitlines(keepends=True), 1):
        line = line.replace("US residents only", "other US residents in N (excluding the group), group at w")
        label = "other US residents (excluding the group)" if i < 2382 else "all US residents including the group"
        line = re.sub(r"(?<!other )(?<!all )US residents(?! incl\.| including|, the group| include)", label, line)
        rows.append(line)
    return "".join(rows)


def main():
    path = HERE / "RESULT.md"
    existing = path.read_text()
    prefix = qualify_history(existing.split(START)[0])
    suffix = "\n" + (existing.split(END, 1)[1] if END in existing else "").lstrip("\n")
    readings = pd.read_csv(D / "p7_named_readings_oct14.csv")
    private = pd.read_csv(D / "p7_private_gain_oct14.csv")
    delta = pd.read_csv(D / "p7_fix_deltas_oct14.csv")
    incidence = json.loads((D / "valuation_meta_oct14.json").read_text())["incidence"]["oct14"]
    extra = json.loads((D / "beside_extra_meta_oct14.json").read_text())
    child_se = case_payload("oct14")["meta"]["child_credits"]["se_bn"]
    named = []
    for base in ("reading1", "reading2", "reading2_consumption"):
        for bound in ("zero", "upper", "rearing"):
            name = base + ("" if bound == "zero" else f"__g3_{bound}")
            for wt in ("equal", "equal_lambda_1.16", "equal_lambda_1.5"):
                s = readings[readings.scenario.eq(name) & readings.weighting.eq(wt)].set_index("end")
                if s.empty:
                    continue
                def pair(col):
                    return number(s.loc["low", col]) + " / " + number(s.loc["high", col])
                named.append({"reading": base, "G3+": bound, "weights": wt,
                    **{title: pair(col) for title, col in (("world", "world_total_bn"),
                        ("other US residents, excludes group", "other_us_residents_bn"),
                        ("all US residents, includes group", "us_residents_incl_group_bn"),
                        ("group", "group_total_bn"), ("Mexico residents", "mexico_residents_bn"),
                        ("break-even w", "breakeven_w"))}})
    priv = []
    for base in ("reading1", "reading2_consumption"):
        for bound in ("zero", "upper", "rearing"):
            name = base + ("" if bound == "zero" else f"__g3_{bound}")
            s = private[private.scenario.eq(name) & private.generation.eq("group")].set_index("end")
            priv.append({"reading": base, "G3+": bound,
                "wages and wage taxes only": " / ".join(number(s.loc[e, "wages_only_bn"]) for e in ("low", "high")),
                "with services and all taxes, both countries": " / ".join(number(s.loc[e, "with_services_bn"]) for e in ("low", "high"))})
    fixes = []
    for basis in ("lineage", "row4"):
        for name in ("fix1_compensation", "fix2_source_incidence", "fix7_recipient_principal_gdp",
                     "fix7_recipient_principal_consumption", "fix12_child_credit_payer"):
            s = delta[delta.population_basis.eq(basis) & delta.fix.eq(name) & delta.g3_bound.eq("zero")
                      & delta.weighting.eq("equal")].set_index("account_end")
            fixes.append({"fix": name, "population": basis,
                **{title: " / ".join(number(s.loc[e, col]) for e in ("low", "high")) for title, col in (
                    ("world delta", "delta_world_total_bn"), ("group delta", "delta_group_total_bn"),
                    ("other US residents delta, excludes group", "delta_other_us_residents_bn"))},
                "world change at least $5bn?": str(bool(s.world_delta_over_5bn.any()))})
    sensitivities = []
    for base in ("p7_g3_k12_at_cost", "p7_mexico_goods_responsive", "p7_goods_wtp_0.5", "p7_goods_wtp_1"):
        for bound in ("zero", "upper", "rearing"):
            name = base + ("" if bound == "zero" else f"__g3_{bound}")
            s = readings[readings.scenario.eq(name) & readings.weighting.eq("equal")].set_index("end")
            sensitivities.append({"one change from R1": base, "G3+": bound,
                "world delta, low / high": " / ".join(number(s.loc[e, "delta_from_r1_bn"]) for e in ("low", "high"))})
    p7 = extra["p7"]
    fixed = p7["other_us_residents_outer_span_fixed_lambda_1_bn"]
    theta = p7["other_us_residents_outer_span_theta_arms_bn"]
    sym = pd.read_csv(D / "p7_private_symmetry_delta_oct14.csv")
    sym = sym[sym.scenario.eq("reading1") & sym.generation.eq("group")].set_index("account_end")
    sym_before = " / ".join(number(sym.loc[e, "original_asymmetric_private_bn"]) for e in ("low", "high"))
    sym_after = " / ".join(number(sym.loc[e, "symmetric_no_services_private_bn"]) for e in ("low", "high"))
    section = f"""{START}

**Verdict:** The ledger corrects compensation, source-tax incidence, remittance purchasing power and the child-credit payer. The frozen fiscal headline and pins stay unchanged. R1 is now a span across explicit G3+ bounds, not one selected bound. Unknown receipts, non-finite amounts and invalid log consumption stop totals and break-evens. [CALCULATION: run_all.sh; p7_fix_deltas_oct14.csv; p7_named_readings_oct14.csv]

The earlier sections are the historical pre-P7 record. In particular, **“Tax basis: gross pay, each tax once” is superseded here**: CPS PEARNVAL is cash earnings, excluding employer contributions. US total compensation adds the account's employer OASDI/HI plus the employer portion of the other-social-contribution receipt, including unemployment insurance. Self-employment contributions remain paid out of measured cash earnings. BEA's employer fraction of the residual is {json.loads((D / 'us_employer_other_basis.json').read_text())['employer_fraction']:.9f}; applying that national mix to the group's common positive-FICA key is an assumption. The unidentified group employer share is bounded at 0–100% of that residual. [DATA: pinned BEA tables 3.1/8 and 3.6/2,4,20,22,27; employer_ui_basis.py]

Mexico's formal comparators add parsed 2024 IMSS quotas, SAR/CEAV and INFONAVIT to compensation and contribution transfers exactly once. Employer-funded individual retirement/housing deposits are worker assets, so this requested transfer convention is broader than a public-revenue measure. Consumption taxes remain on cash gross. Formal status, salary as contribution base, exposure below the annual minimum and accident-risk assignment are model assumptions; source outputs separate components and statutory/duration bounds. Source SHA pins identify the retrieved primary text bytes where direct PDFs were unavailable, not PDF bytes. [SOURCE: inputs/imss_financing_2024.txt, lss_statutory.txt, infonavit_statutory.txt; inputs/pins.json; CALCULATION: mexico.py → mexico_meta.json]

### Population, endpoints and frame

The adopted lineage has 42,752,213 members; the identified union has 39,712,493. Every named reading reports personal endpoints 16 / 11 at fixed central premium/valuation settings and G3+ zero, sex-age G2 upper bound, and the separate aggregate-G2-rearing-ratio arm. Outer low/high uncertainty scenarios in world_ledger_oct14.csv are different objects. The row4 companion retains the frozen lineage fiscal baseline while changing its person rows; its isolated-fix table applies only the identified-union correction, explicitly labelled, and must not be quoted as a full union fiscal account. [DATA: pins.json; population_basis.py; p7_fix_deltas_oct14.csv population_rule]

All pairs below are low / high personal account endpoint, $bn/year. Other US residents excludes the group and combines today's and future payers; all US residents including the group adds the same weighted group total. All results are conditional accounting/valuation calculations, not observed causal removal effects. The LLM instrument's framing choices remain explicit. [FRAMING-SENSITIVE]

{table(pd.DataFrame(named))}

The complete table, including every named same-person parameter and beside arm at every G3+ bound, endpoint and executed weighting, is [p7_named_readings_oct14.csv](derived/p7_named_readings_oct14.csv). Smaller beside arms are in [p7_beside_arms_endpoints_oct14.csv](derived/p7_beside_arms_endpoints_oct14.csv). World, other US residents excluding the group, all US residents including the group, group, Mexico residents and break-even w have separate columns. No reading label may omit its G3+ convention.

### Private gain

“Wages alone” now includes wage income and wage taxes on **both** sides, without either country's public services or consumption/property taxes. “With services” includes US and Mexican services and all modelled taxes on both sides. Remittance principal is the group's own spending and is excluded from these private comparisons. Each sign at both G3+ bounds is visible below; the aggregate-G2 arm is beside them, not adopted. Reading 2 uses its consumption-PPP twin for purchasing-power private gains. [CALCULATION: beside_extra.private_gain; p7_private_gain_oct14.csv]

{table(pd.DataFrame(priv))}

Fix 5's **service-symmetry correction alone**, holding the original all-tax definition, compensation, incidence and price basis fixed, moves R1's original zero-bound private comparison from **{sym_before}bn to {sym_after}bn** (personal low / high): +{number(sym.delta_private_bn.iloc[0])}bn at either end. The final wage-tax-only definition above additionally changes tax scope, explicitly reported in its component columns; these changes must not be added as independent estimates. Every originally reported private scenario's isolated symmetry change is in p7_private_symmetry_delta_oct14.csv. [CALCULATION: p7_fixes.py → p7_private_symmetry_delta_oct14.csv]

### Each fix in isolation

Each row is **one** change from the pre-P7 oct14 central at its identified personal endpoint, with every other convention held fixed. The full [p7_fix_deltas_oct14.csv](derived/p7_fix_deltas_oct14.csv) gives both G3+ bounds and equal/λ 1.16/λ 1.5 weights, all parties and break-even changes. These are world-ledger deltas: the frozen fiscal headline changes by **zero** for every fix. A world or private-claim change at least $5bn is shown separately from a fiscal-headline move. [CALCULATION: p7_fixes.py]

{table(pd.DataFrame(fixes))}

Fixes 3 (population labels), 4 (fail closed) and 8 (bounds/report coverage) are rule corrections without a standalone monetary shock. The symmetric private-gain convention, fix 5, is reported by the two forms above and their components in p7_private_gain_oct14.csv. Child credits move from member-child rows to the non-member filer holding the return; this conserves the equal/λ world total while changing the group and other US residents excluding the group. The frozen identified-union credit source has replicate SE **{child_se:.6f}bn**; the added-member term is an assumption, not an independent estimate. No joint ENIGH/EMOVI/CPS replicate covariance is available in this route, so no joint replicate SE is invented. [DATA: frozen meta.child_credits; inputs positive controls; CALCULATION: valuation.py]

### Foreign source-tax counterparts and remittances

Item 6's receipt-line set comes from the frozen item registry. Corporate_labor is already inside measured wages and is not charged again. The remaining US capital-source taxes are {number(incidence['low']['capital_source_tax_credit_bn'])} / {number(incidence['high']['capital_source_tax_credit_bn'])}bn on the lineage ({number(incidence['low']['identified_union_capital_source_tax_credit_bn'])} / {number(incidence['high']['identified_union_capital_source_tax_credit_bn'])}bn on the identified union). Their Mexican and rest-of-world counterparts are **explicit exclusions, unidentified**: a matched taxable-capital base, destination and source-tax liability are absent. A wage bill and a statutory corporate rate cannot identify them. [DATA: valuation_meta_oct14.json incidence; SOURCE: OECD corporate effective-tax-rate methodology, https://www.oecd.org/en/publications/corporate-tax-statistics-2024_9c27d6e8-en/full-report/corporate-effective-tax-rates_c3356c78.html]

The declared foreign-parity stress is 0–100% of those US capital-source taxes, **not an empirical finite bound**. At equal weights the capital-source world increment is US tax minus foreign tax, hence 0–{number(incidence['low']['capital_source_tax_credit_bn'])} / 0–{number(incidence['high']['capital_source_tax_credit_bn'])}bn; the corporate-labour double-debit correction is separate. Foreign taxes may exceed the assumed cap. The central exclusion must never be described as a measured zero. [ASSUMPTION; CALCULATION: p7_foreign_counterparts_oct14.csv; DATA: valuation_meta_oct14.json foreign_capital_source_tax_exclusion]

Banxico's principal is paid to recipients; the circular separately reports sender outlay including commissions. Sender-added fees and unmeasured FX spreads are excluded from this principal-only ledger. Recipients exchange nominal dollars at PA.NUS.FCRF and spend at Mexican prices. The lane's central GDP-PPP basis uses market-rate/GDP-PPP; the consumption-PPP recipient-only sensitivity holds the other rows fixed and is evaluated only at equal/λ weights. It is explicitly a one-row purchasing-power sensitivity, never a mixed-basis live log-weight run. The live row schema carries price_basis; each party has one basis, and nominal Mexican rows cannot receive log weights. [SOURCE: Banxico Circular12/2012, https://dof.gob.mx/nota_detalle_popup.php?codigo=5260748; DATA: pinned WDI PA.NUS.FCRF, PA.NUS.PPP, PA.NUS.PRVT.PP; CALCULATION: world_ledger.py]

### Report-only assumptions and the other-residents claim

Fix 6a values G3+ **K–12 only** at cost beside the zero-premium/V=0 convention: the actual K–12 portion of education_services at the pinned school share, school_reprice and K–12 capital/fee-offset components. Colleges, benefits and training stay separate. Fix 6b holds US public goods at average cost and Mexican forgone public goods at the responsive share. Fix 11 scales public-good willingness to pay by group/other-resident income at elasticities 0.5 and 1. Their one-change R1 deltas at each endpoint/bound are in p7_named_readings_oct14.csv delta_from_r1_bn. These are operator-framing sensitivities, not adopted convention changes. [FRAMING-SENSITIVE; CALCULATION: beside_extra.py]

{table(pd.DataFrame(sensitivities))}

These sensitivities change the group's valuation only, so their world deltas are also the group/all-US-including-group deltas; other US residents excluding the group and Mexico residents stay fixed. The equal and λ deltas are the same. The $5bn test is the absolute value of each endpoint delta, not a change to the frozen fiscal headline.

The rearing model's terminal mobility cohort is births 1983–92, approximately ages 32–41 in income-year 2024; subsequent birth cohorts inherit that terminal transition. An identified later-cohort replacement is unavailable, so fix 6c is a documented transport limit, not an invented causal correction. The route accounts for which G2 weights use it. [DATA: mexico_transition.csv; g2_premium.emovi_cohort; beside_extra_meta_oct14.json]

The former statement that other US residents excluding the group lose at every named reading was invariant to the readings' group-only changes. Across the personal account endpoints and beside arms their fixed equal-weight span is **{number(fixed[0])} to {number(fixed[1])}bn**. Across the explicit fiscal-alternative-use θ arms the span is **{number(theta[0])} to {number(theta[1])}bn** (including the labelled education-MVPF-5 extreme). These are different conventions, separately named; neither is a confidence interval. λ-specific spans are in beside_extra_meta_oct14.json p7. [CALCULATION: beside_extra.py; p7_named_readings_oct14.csv; p7_beside_arms_endpoints_oct14.csv]

### Gates and reproduction

Positive controls reproduce the committed oct14 route before correction, original Mexico cash/employee-tax cells, and original valuation by undoing precisely the two incidence fields. New gates cover primary-file hashes, national employer/worker/source-rounding closure at 1e-6bn, group allocation closure, monetary identities, population conservation, exhaustive receipt classes/economic payers, finite rows/log increments, price-basis consistency, both G3+ bounds, personal endpoint coverage and party sums. Existing tolerances were not loosened. [CALCULATION: test_mexico_compensation.py; test_employer_ui_basis.py; test_p7_valuation.py; test_p7_world.py; test_p7_readings.py]

```sh
sh infra/immigration-fiscal/world_ledger_2026_09_27/run_all.sh oct14
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 -m pytest -p no:cacheprovider infra/immigration-fiscal/world_ledger_2026_09_27/ -q
uv run --no-project python3 scripts/rerun_lane.py infra/immigration-fiscal/world_ledger_2026_09_27 "sh {{lane}}/run_all.sh oct14" "uv run --no-project python3 -m pytest -p no:cacheprovider {{lane}}/test_live_contract.py {{lane}}/test_beside_arms.py {{lane}}/test_beside_extra.py {{lane}}/test_mexico_compensation.py {{lane}}/test_employer_ui_basis.py {{lane}}/test_p7_valuation.py {{lane}}/test_p7_world.py {{lane}}/test_p7_readings.py {{lane}}/test_p7_fix_deltas.py -q"
```

The per-command timing log uses Python time.perf_counter and resource.getrusage in _cache/p7_timings.jsonl; no ps/sysctl/time-l. Validation timestamps and return codes follow below. No Git metadata was written by this lane.

{END}
"""
    path.write_text(prefix.rstrip() + "\n\n" + section + suffix)
    print("Rendered P7 RESULT from live correction and named-reading tables")


if __name__ == "__main__":
    main()
