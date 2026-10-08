"""Write _cache/inventory_2026_10_08.json: the objection cards rebuilt on main case v6 (adopted 2026-10-07,
$389.1–461.5bn) and the docs as they stand, item T in the generation ledger included.

It starts from context.json as committed at cb3c2e6c (the September 26 pass), so reruns give the same inventory
whatever HEAD holds. A card left out of EDITS keeps its text, and its values are re-anchored from cb3c2e6c by
reanchor.py; a value whose line only maps by a blind shift is refused. A card in EDITS takes the fields given there
(`value_edits` changes single values of a kept card), cited by the words of the line that prints each number (at(),
csv_row()), so the citation survives lines added above it. The cards follow their FAQ entries and carry only the live
case: a value or clause that quotes an earlier case is rewritten to v6 or dropped. Combining rules are read from the
FAQ's "Before combining numbers" section by their words.

Before writing, every anchor must resolve to one line, every value must pass build_context.confirmed(), every
sentence of an objection must appear in the FAQ (an entry's heading or steel-man), and every number token in a card's
objection, finding, combining rule and value labels must equal a value of the card or a number printed within two
lines of a line the card cites (the FAQ lines a rule or objection is read from count; a CSV row reads with its header).
Any failure lists them all and stops the write.

Usage: build_inventory.py
"""
import csv
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import reanchor as ra  # noqa: E402

bc = ra.bc
BASE = "cb3c2e6c"
OUT = ra.LANE/"_cache"/"inventory_2026_10_08.json"

FAQ = "research/immigration-objections-faq-2026-09-21.md"
INDEX = "research/immigration-INDEX.md"
CAA = "research/immigration-complete-annual-account-2026-09-20.md"
LEDGER = "research/immigration-yearly-lifetime-cost-repair-2026-09-19.md"
REAL = "research/immigration-real-fiscal-and-social-costs-2026-09-23.md"
BACKCAST = "research/immigration-historical-backcast-2026-09-20.md"
POPULATION = "research/immigration-mexican-origin-population-total-2026-09-19.md"
EDUCATION = "research/immigration-education-fiscal-and-methods-2026-09-19.md"
SCALING = "research/immigration-service-scaling-test-2026-09-20.md"
LADDER = "research/immigration-confidence-ladder.md"
FISCAL = "infra/immigration-fiscal"
R07 = f"{FISCAL}/main_case_2026_10_07/RESULT.md"
LEDGER_DERIVED = f"{FISCAL}/ledger_absolute_2026_09_17/derived"
AGES = f"{LEDGER_DERIVED}/age_normalizations.csv"
GAPS = f"{LEDGER_DERIVED}/complete_gaps.csv"
CARE = f"{FISCAL}/care_household_services_2026_09_23/RESULT.md"
SCALE = f"{FISCAL}/scale_spillovers_2026_09_23/RESULT.md"
CONSTRUCTION = f"{FISCAL}/construction_housing_supply_2026_09_23/RESULT.md"
ARRIVAL = f"{FISCAL}/arrival_window_fiscal_2026_09_18/RESULT.md"
ARRIVAL_ESTIMATES = f"{FISCAL}/arrival_window_fiscal_2026_09_18/derived/window_estimates.csv"
STRESS = f"{FISCAL}/ledger_stress_2026_09_17/RESULT.md"
METRO = f"{FISCAL}/metro_match_2026_09_17/RESULT.md"
EDUCATION_ESTIMATES = f"{FISCAL}/education_origin_fiscal_2026_09_19/derived/annual_estimates.csv"
EDUCATION_COMPARISONS = f"{FISCAL}/education_origin_fiscal_2026_09_19/derived/comparisons.csv"
BLACK = f"{FISCAL}/black_comparator_rough_2026_09_28/RESULT.md"
LEADS = "research/immigration-marginal-revolution-leads-read-2026-09-21.md"
COHORTS = "research/immigration-mexican-arrival-cohorts-2026-09-18.md"
INCARCERATION = "research/immigration-mexican-origin-generation-incarceration-2026-09-16.md"


# Anchors that resolve to no line or to several; main() lists them all and writes nothing.
UNRESOLVED = []


def unresolved(message, placeholder):
    UNRESOLVED.append(message)
    return placeholder


def at(path, needle, through=None, start=False):
    """'path:N' for the one line holding `needle` (beginning with it if `start`), or 'path:N-M' when `through`
    names the words of the last cited line, the first such line at or after N."""
    lines = ra.new_lines(path)
    hits = [i for i, line in enumerate(lines) if (line.startswith(needle) if start else needle in line)]
    if len(hits) != 1:
        return unresolved(f"{path} has {len(hits)} lines holding {needle!r}", f"{path}:0")
    first = hits[0]
    if through is None:
        return f"{path}:{first+1}"
    last = next((i for i in range(first, len(lines)) if through in lines[i]), None)
    if last is None:
        return unresolved(f"{path} has no line holding {through!r} at or after line {first+1}", f"{path}:0")
    return f"{path}:{first+1}-{last+1}" if last > first else f"{path}:{first+1}"


def csv_row(path, **fields):
    """'path:N' for the one CSV row whose columns hold the given values."""
    with open(ra.ROOT/path, newline="") as f:
        reader = csv.DictReader(f)
        hits = [reader.line_num for row in reader if all(row[k] == v for k, v in fields.items())]
    if len(hits) != 1:
        return unresolved(f"{path} has {len(hits)} rows with {fields}", f"{path}:0")
    return f"{path}:{hits[0]}"


def val(label, value, file_line, unit="$bn/year", se=None):
    return dict(label=label, value=value, unit=unit, se=se, file_line=file_line)


def paragraphs(path):
    """(first line, last line, joined text, offsets) per paragraph; offsets give each line's start in the text."""
    lines, out, block = ra.new_lines(path), [], []
    for i, line in enumerate(lines+[""]):
        if line.strip():
            block.append(i)
            continue
        if block:
            text, offsets = "", []
            for k in block:
                offsets.append(len(text)+(1 if text else 0))
                text = (text+" " if text else "")+lines[k].strip()
            out.append((block[0], block[-1], text, offsets))
            block = []
    return out


def faq_rule(opening, phrase=None, drop_prefix=""):
    """The FAQ text from the one line holding `opening` to the end of its paragraph, as (text, "first-last").
    `phrase` starts the text at that phrase (it may wrap across lines); `drop_prefix` removes a leading prefix."""
    lines = ra.new_lines(FAQ)
    hits = [i for i, line in enumerate(lines) if opening in line]
    if len(hits) != 1:
        return unresolved(f"FAQ has {len(hits)} lines holding {opening!r}", ("UNRESOLVED", "0-0"))
    start = end = hits[0]
    while end+1 < len(lines) and lines[end+1].strip():
        end += 1
    text = " ".join(line.strip() for line in lines[start:end+1])
    if phrase:
        if phrase not in text:
            return unresolved(f"FAQ paragraph at {start+1} lost {phrase!r}", ("UNRESOLVED", "0-0"))
        text = phrase+text.split(phrase, 1)[1]
    if drop_prefix:
        if not text.startswith(drop_prefix):
            return unresolved(f"FAQ {start+1}-{end+1} no longer starts with {drop_prefix!r}", ("UNRESOLVED", "0-0"))
        text = text[len(drop_prefix):]
    return text, f"{start+1}-{end+1}"


def faq_excerpt(begin, end):
    """The FAQ words from `begin` through `end` inside one paragraph, bold markers removed, as (text, "a-b")
    with a-b the lines the words sit on."""
    hits = [p for p in paragraphs(FAQ) if begin in p[2]]
    if len(hits) != 1:
        return unresolved(f"FAQ has {len(hits)} paragraphs holding {begin!r}", ("UNRESOLVED", "0-0"))
    first, _, text, offsets = hits[0]
    i = text.index(begin)
    j = text.find(end, i)
    if j < 0:
        return unresolved(f"FAQ paragraph at {first+1} has no {end!r} after {begin!r}", ("UNRESOLVED", "0-0"))
    j += len(end)
    line_of = lambda pos: first+max(k for k, off in enumerate(offsets) if off <= pos)
    return text[i:j].replace("**", ""), f"{line_of(i)+1}-{line_of(j-1)+1}"


def faq_excerpts(*spans):
    """Several faq_excerpt() spans joined into one rule, cited from the first span's first line to the last's last."""
    parts = [faq_excerpt(*span) for span in spans]
    lines = [int(n) for _, span in parts for n in span.split("-")]
    return " ".join(text for text, _ in parts), f"{min(lines)}-{max(lines)}"


TWO_ANCHORS = ("The $389–461bn (entries 2, 4, 11 and 15–19)", "with no reference group.")
LEDGER_OBJECT = ("The generation gaps and the age structures", "re-weighted by age.")
NOT_A_DECOMPOSITION = ("One is not a decomposition of the", "complete-account total.")
LATER_CORRECTIONS = ("The account carries later corrections", "complete-account total.")
CARE_ITEMS = ("Three care channels sit inside the main case", "ladders 198 and 219).")
MATCH = "A result refutes a claim only when population, horizon and outcome match."
PARTIAL = ("Entries 7 and 9 rest on", "partial accounts.")
CA_TX = ("**California and Texas per-person gaps", "−$9k.")
# Ledger cards carry what the ledger is and that it is no split of the complete account.
LEDGER_RULE = faq_excerpts(LEDGER_OBJECT, NOT_A_DECOMPOSITION)
CA_TX_OBJECTION = ("California's white-reference gap is a coastal-price, high-service artifact. Texas already has about "
                   "32% Mexican-origin residents — the same share as California — and is the relevant picture for the "
                   "rest of the country.")


def ledger_row(structure, group, allocation="shared"):
    return at(AGES, f"{allocation},{structure},{group},", start=True)


def gap_row(group, reference):
    return at(GAPS, f"{group},{reference},", start=True)


def comparison_row(profile_id, allocation, education, reference):
    """The education lane's common-age gap of Mexico-born adults against a reference of the same schooling."""
    return csv_row(EDUCATION_COMPARISONS, profile_id=profile_id, allocation=allocation, account="expanded_excluding_N",
                   origin="mexico_born", education=education, entry="stock", reference=reference,
                   reference_education=education, metric="common_age_gap_per_person")


BELOW_HS_CELL = dict(profile_id="1", allocation="shared", account="expanded_excluding_N", origin="mexico_born",
                     education="lt_hs", entry="stock", age_scope="25-64", metric="net_per_person")


# Cards no living document carries any more, with the reason.
DROP = {
    "complete_account_356_endpoint": (
        "Its numbers are the September 20 account's most pessimistic stress test ($356.84bn) and the same test on the "
        "September 23 case ($409.1bn); the complete-account memo keeps them only as the September 20 calculation record. "
        "The live outer range, $311.9–515.6bn with every correction and component at its extreme, is on "
        "e17_survey_errors_nearly_cancel."),
    "interest_on_gap_lane": (
        "A financing projection on the −$263bn complete-account balance, which the lane's README and the ledger memo "
        "mark superseded. The live financing figures are the legacy comparisons of FAQ 2 and 21, now on "
        "e2_legacy_financing_beside and e21_long_run_channels_at_zero."),
    "ledger_absolute_waterfall_and_arms": (
        "Its arms grid (63 cells, −$496.2bn to −$76.1bn; practitioner range −$290.5bn to −$190.1bn) is computed on the "
        "September 19 ledger before item T, and no living document quotes it; the 144-cell range it also carried is "
        "stamped stale. The ledger's current balances are on generation_ledger_annual_balances."),
}

FY = "infra/immigration-fiscal/break_conditions_2026_09_29/RESULT.md"

EDITS = {
    "headline_cbo_informed_net_cost": dict(
        finding=("This page runs main case v6, adopted October 7: other US residents bear a conditional net cost of "
                 "$389.1–461.5bn a year, $9,101–10,794 per member of the 42.75M-person lineage. The case counts the "
                 "Social Security and Part A promises members earn as they work, at the benefits current law can pay; "
                 "counting benefits when paid instead (the preset \"Benefits counted when paid\"), it is $307.4–385.4bn. "
                 "It charges the return on public capital, lets roads, parks, rental assistance and government "
                 "enterprises respond, and takes long-run property taxes; with every service proportional it is "
                 "$418.1–475.8bn. With CBO's year-to-year budget responses, no long-run road, park or property-tax "
                 "response and no capital return, the first-year budget response, shown beside the presets, is "
                 "$288.9–336.5bn, and $207.3–260.3bn counting benefits when paid. Defense, interest on existing "
                 "debt and business subsidies stay at zero response."),
        values=[
            val("main case v6: conditional net cost to other US residents", "389.1-461.5",
                at(INDEX, "**Adopted main case (October 7)", through="($389.1–461.5bn")),
            val("per member of the 42.75M-person lineage", "9,101-10,794", at(R07, "Per member of the", through="$9,101"),
                unit="$/member/year"),
            val("the cash set: Social Security and Part A counted when paid", "307.4-385.4",
                at(INDEX, "Counting benefits when paid, the cash set is $307.4")),
            val("every service proportional", "418.1-475.8", at(CAA, "the current case gives $418.1")),
            val("first-year budget response: CBO's year-to-year responses, no long-run road, park or property-tax "
                "response, no capital return; pensions on accrual / benefits counted when paid",
                "288.9-336.5 / 207.3-260.3", at(INDEX, "it is $288.9–336.5bn")),
        ],
        combining_rule=faq_excerpt(*TWO_ANCHORS),
        memo=(f"decisions/2026-10-07-main-case-v6.md; {R07}; {INDEX} § Adopted main case; {CAA} (current main case, "
              f"top); {FY} (first-year budget response)"),
        population=("the 42.75M-person lineage: the 39.71M Mexican-origin residents of all ages and generations the "
                    "account prices (CPS ASEC 2025, the Mexico-born scaled to the ACS count outside California and "
                    "Texas) plus 3.04M descendants who no longer report Mexican origin"),
        comparator="no reference group; the change for all other US residents, other immigrants included",
        horizon="annual, income-year 2024, stationary long-run comparison",
        evidence_level=("[MODEL / TRANSFERRED EVIDENCE] / [FRAMING-SENSITIVE]; adopted main case v6 "
                        "[CALCULATION: main_case.cjs, gated]"),
    ),
    "e1_gap_under_age_structures": dict(
        finding=("Age works the other way. The raw difference from whites is −$5,276 per person; at any common age "
                 "structure it is −$8,154 to −$9,829, and over a full life course at today's rates −$8,154."),
        values=[
            val("gap against whites, each group's own ages (raw)", -5276.044529,
                ledger_row("own_ages_today", "mexican_observed_total"), unit="$/person/year"),
            val("gap against whites, white's ages today", -8235.809619,
                ledger_row("white_ages_today", "mexican_observed_total"), unit="$/person/year"),
            val("gap against whites, at the group's ages today", -9828.572263,
                ledger_row("union_ages_today", "mexican_observed_total"), unit="$/person/year"),
            val("gap against whites, stationary life course", -8154.135188,
                ledger_row("stationary_life_course", "mexican_observed_total"), unit="$/person/year"),
        ],
        combining_rule=LEDGER_RULE,
        population="observed Mexican-origin union, 40.897m (the survey's count), all ages",
    ),
    "e1_value_of_the_young_structure": dict(
        finding=("Whites with the Mexican-origin age pyramid would run +$4,852 per person, against +$299 at their own "
                 "ages, so the young structure is worth about $4,550 a year."),
        values=[
            val("white reference at the group's ages today", 4852.021195,
                ledger_row("union_ages_today", "third_plus_nh_white"), unit="$/person/year"),
            val("white reference at its own ages today", 299.493461,
                ledger_row("own_ages_today", "third_plus_nh_white"), unit="$/person/year"),
            val("value of the young structure (memo's stated difference)", "about 4,550",
                at(LEDGER, "young age structure is worth about $4,550"), unit="$/person/year"),
            val("under-18 / 65+ shares: the group", "29.6% / 7.7%", at(LEDGER, "The stationary row weights ages"),
                unit="share"),
            val("under-18 / 65+ shares: white reference", "18.0% / 23.4%", at(LEDGER, "The stationary row weights ages"),
                unit="share"),
        ],
        combining_rule=LEDGER_RULE,
    ),
    "e2_fixed_functions_and_cbo_inputs": dict(
        finding=("The headline holds defense, existing interest and business subsidies fixed at zero response. That "
                 "zero is the account's own assumption; it does not come from CBO. What comes from CBO is the "
                 "tax-incidence rule set: corporate tax 75% to capital income, 25% to wages. CBO's scoring also holds economic-affairs and "
                 "recreation budgets fixed; the main case replaces that with long-run responses, since across states "
                 "highway spending rises 0.73% and park spending 0.95% per 1% more residents. Schools are charged at "
                 "their full average cost per pupil: across 2019 districts spending rises 1.004% per 1% more pupils "
                 "(pupil-weighted), and across states 0.973%. The year-to-year school response of 63–66%, computed "
                 "from CBO's coefficients, belongs to the first-year budget response."),
        values=[
            val("corporate tax incidence to capital income / wages (CBO's rules)", "75% / 25%",
                at(FAQ, "the tax-incidence rule set (`cbo_collective`"), unit="share"),
            val("long-run response per 1% more residents across states: highways / parks", "0.73% / 0.95%",
                at(FAQ, "highway spending rises 0.73%"), unit="percent"),
            val("school spending per 1% more pupils: across 2019 districts (pupil-weighted) / across states",
                "1.004% / 0.973%", at(FAQ, "1.004% per 1% more pupils"), unit="percent"),
            val("year-to-year school response from CBO's coefficients, kept for the first-year budget response", "63-66%",
                at(FAQ, "CBO's year-to-year 63–66%"), unit="share of average cost per pupil"),
        ],
        combining_rule=faq_excerpt(*TWO_ANCHORS),
        memo=(f"{FAQ} § 2; decisions/2026-09-27-main-case-capital-return-and-long-run-responses.md; "
              "decisions/2026-09-29-main-case-v4.md; decisions/2026-09-26-main-case-schools-full-cost.md; "
              f"{R07}"),
        population="the 42.75M lineage; the responses apply to nationally assigned service budgets",
        comparator="full proportional-service benchmark",
        horizon="annual 2024, long-run budget responses, private capital fully adjusted",
        evidence_level="[ASSUMPTIONS] + [MODEL / TRANSFERRED EVIDENCE]",
    ),
    "e2_general_public_services_sensitivity": dict(
        finding=("General public services respond at 0.60–0.85 of average cost: removing a group that is 13% of "
                 "residents, at cross-state rates of 0.59–0.84, adds $30.5–43.2bn a year. That range is the cross-state "
                 "scale of administration spending, 0.842 (SE 0.039) for state administration and 0.789 for financial "
                 "administration, with the low end holding the federal executive and legislature fixed. The only "
                 "within-state test gave 0.47 with a 95% interval of −0.72 to 1.66, which cannot tell zero from one; "
                 "zero is a budget-scoring convention."),
        values=[
            val("general public services, finite-removal response", "0.60-0.85",
                at(FAQ, "**General public services** respond at 0.60–0.85"), unit="share of average cost"),
            val("added to the main case by that response", "30.5-43.2", at(FAQ, "adds $30.5–43.2bn")),
            val("cross-state scale of administration spending: state / financial administration", "0.842 (SE 0.039) / 0.789",
                at(FAQ, "That range is the cross-state scale of administration spending", through="0.789"),
                unit="elasticity"),
            val("the only within-state test", "0.47 (-0.72 to 1.66)", at(FAQ, "The only within-state test gave 0.47",
                through="−0.72 to 1.66"), unit="elasticity (95% interval)"),
        ],
        combining_rule=None,
        memo=(f"{FAQ} § 2; infra/immigration-fiscal/finite_response_2026_09_26/RESULT.md (run C); "
              "decisions/2026-09-23-main-case-general-government-and-use-keys.md; "
              "research/immigration-education-administration-scope-2026-09-20.md"),
        population="the 42.75M lineage",
        comparator="zero response, the budget-scoring convention",
        horizon="annual 2024, a finite removal at long-run rates",
        evidence_level="[INFERENCE: cross-state scale] + [MODEL]",
    ),
    "e2_per_capita_three_functions": dict(
        finding=("Charging all three fixed functions per capita is a convention and is not part of the net-cost "
                 "headline. The objection also runs the other way: defense might track the economy. If it did, the "
                 "group's lower output would cut defense by $47.5–72.0bn a year. It has not: national defense was 6.0% "
                 "of GDP in FY1986, 2.9% in 2000, 4.7% in 2010 and 3.2% in 2024, following threats. It stays at zero, "
                 "with that bound beside."),
        values=[
            val("defense cut if defense tracked the group's lower output", "47.5-72.0",
                at(FAQ, "lower output would cut defense by $47.5–72.0bn")),
            val("national defense, share of GDP: FY1986 / 2000 / 2010 / 2024", "6.0% / 2.9% / 4.7% / 3.2%",
                at(FAQ, "national defense was 6.0% of", through="3.2% in 2024"), unit="share of GDP"),
        ],
        relation_to_headline="outside_not_addable",
        combining_rule=None,
        memo=f"{FAQ} § 2; {LADDER} entry 253",
        population="the 42.75M lineage",
        comparator="zero response for defense, the account's assumption",
        horizon="annual 2024",
        evidence_level="[MODEL SENSITIVITY] + [SOURCE: national defense shares of GDP]",
    ),
    "e2_fixed_service_range_and_breakeven": dict(
        finding=("The sign turns on ordinary service budgets, and only at one end. With the enterprises and the capital "
                 "return moving with their lines, the high end turns positive only if fewer than 3.2–5.4% of assigned "
                 "service costs are incremental; the low end's break-even is negative (−3.7% to −1.6%), so no service "
                 "response turns it positive. With the enterprises held at 1 while services fall to zero, the range is "
                 "−9.05% to 1.58%: the low end never turns positive, and the high end does only on the shared "
                 "allocation, below 1.58%. With every service budget frozen, on CBO's incidence rules, other residents' net "
                 "position runs from −$60.8bn (a cost) to +$44.3bn (a gain)."),
        values=[
            val("break-even incremental share, high end", "3.2-5.4%",
                at(FAQ, "the high end turns positive only if fewer than 3.2–5.4%"), unit="share of assigned service costs"),
            val("break-even incremental share, low end (negative: a net cost at every service response)",
                "-3.7% to -1.6%", at(FAQ, "the low end's break-even is negative"), unit="share of assigned service costs"),
            val("the same with the enterprises held at 1 while services fall to zero", "-9.05% to 1.58%",
                at(FAQ, "the range is −9.05% to 1.58%"), unit="share of assigned service costs"),
            val("every service budget frozen, CBO's incidence rules", "-60.8 to +44.3",
                at(FAQ, "other residents' net position runs from −$60.8bn"), unit="$bn/year net outside effect"),
        ],
        memo=(f"{R07} § Sign reversal; infra/immigration-fiscal/main_case_2026_10_07/derived/sign_reversal.csv "
              f"(oct07); {FAQ} § 2"),
        population="the 42.75M lineage",
        comparator="other residents",
        horizon="annual 2024, declared capacity paths",
        evidence_level="[DISCONFIRMATION / MODEL SENSITIVITY]; [CALCULATION: sign_reversal.cjs, gated]",
    ),
    "e2_muni_bond_paper_cannot_settle": dict(
        value_edits={0: dict(label="total revenue at two years (interval)", value="+0.2% (-1.8% to +2.2%)",
                             file_line=at(FAQ, "municipal-bond paper sometimes cited",
                                          through="its revenue result is +0.2%"))},
    ),
    "e3_lower_benefit_draw_by_generation": dict(combining_rule=LEDGER_RULE),
    "e3_union_offset_mirrors_tax_gap": dict(
        finding=("Lower benefits follow lower covered earnings, so the offset mirrors the tax gap: for all generations "
                 "together, $2,653 of lower spending against $10,889 of lower receipts at the white age structure. "
                 "Under the stationary structure it is $2,434 against $10,588, and the second generation's "
                 "lower-spending offset is only $822."),
        values=[
            val("spending gap against whites at white ages (lower spending)", 2652.988346,
                ledger_row("white_ages_today", "mexican_observed_total"), unit="$/person/year"),
            val("receipts gap against whites at white ages (lower receipts)", -10888.797965,
                ledger_row("white_ages_today", "mexican_observed_total"), unit="$/person/year"),
            val("same two quantities under the stationary structure", "-10,588 receipts / +2,434 spending",
                at(LEDGER, "Under the stationary structure the union's gap is"), unit="$/person/year"),
            val("second generation's lower-spending offset, stationary structure", 822,
                at(LEDGER, "Under the stationary structure the union's gap is"), unit="$/person/year"),
        ],
        combining_rule=LEDGER_RULE,
    ),
    "e4_care_channels_add": dict(
        finding=("Two care channels are inside the main case: taxes on the extra hours native women work because "
                 "household services are cheaper, $2.69bn a year ($1.80–5.76bn), and the net Medicaid saving on elder "
                 "care, $1.49bn ($1.20–7.62bn; entry 13). With the output gain to other factors from those hours "
                 "(−$0.03bn) they come to $4.15bn ($2.60–13.35bn), about 1% of the main case."),
        values=[
            val("taxes on native women's extra hours, household-service channel", "2.69 (1.80-5.76)",
                at(CARE, "| Taxes on native women's extra hours, household-service channel |")),
            val("net Medicaid saving on elder care: nursing facilities less Medicaid home care", "1.49 (1.20-7.62)",
                at(CARE, "| Elder care: Medicaid nursing-facility saving net of Medicaid home care |")),
            val("output gain to other factors from those hours, with its taxes", "-0.03",
                at(CARE, "| Output gain to other factors from those hours, with its taxes |")),
            val("the care channels together", "4.15 (2.60-13.35)", at(CARE, "| **Sum of additive channels** |")),
        ],
        combining_rule=faq_excerpt(*CARE_ITEMS),
        memo=(f"{CARE}; {FAQ} § 4 and § 13; research/immigration-consumer-price-and-native-hours-2026-09-18.md"),
        comparator="the account, with native hours and other residents' nursing-facility spending priced",
        evidence_level=("[CALCULATION: care lane, coefficients checked against the papers] + [INFERENCE: log-linear "
                        "extrapolation beyond the identifying variation]; inside the main case"),
    ),
    "e4_offset_threshold_is_conditional": dict(
        finding=("Omitted benefits would have to reach $389–461bn a year to offset the main case. That threshold is "
                 "conditional on the service-response share, which is assumed and unmeasured: it is $289–336bn with "
                 "CBO's first-year responses ($207–260bn counting benefits when paid) and $328–428bn if non-school "
                 "education budgets are also held fixed. At the high end it reaches zero where 3.2–5.4% of assigned "
                 "service costs are incremental; at the low end no service response brings it to zero. So the "
                 "response share moves the result more than any offset listed here."),
        values=[
            val("offset hurdle: the main case", "389-461", at(FAQ, "$389–461bn a year to offset the main case")),
            val("same with CBO's first-year responses; counting benefits when paid", "289-336 / 207-260",
                at(FAQ, "It is $289–336bn with CBO's first-year responses")),
            val("same with non-school education budgets also fixed", "328-428",
                at(FAQ, "$328–428bn if non-school education budgets")),
            val("break-even incremental share at the high end", "3.2-5.4%",
                at(FAQ, "At the high end it reaches zero where 3.2–5.4%"), unit="share of assigned service costs"),
        ],
        combining_rule=faq_excerpt("No ratio of", "can be formed from these."),
        memo=f"{FAQ} § 4; {R07}; {FY}",
        population="the 42.75M lineage",
    ),
    "school_flight_not_estimated_for_hispanic_inflows": dict(
        finding=("Each Asian student arriving in a high-income California district is followed by 1.5 white "
                 "departures, to other districts and not to private schools. White flight from Hispanic arrivals is "
                 "not estimated there, so the paper leaves standing the finding that native flight from public schools "
                 "does not reproduce for Hispanic inflows (ladder 141)."),
        # The tercile line through the memo's sentence on ladder 141.
        value_edits={1: dict(file_line=at(LEADS, "Within the sample the effect shrinks as district income rises",
                                          through="non-reproduction for Hispanic inflows (ladder 141)"))},
    ),
    "e4_prices_and_native_hours": dict(
        finding=("Cheaper household services are worth $21.8bn a year to consumers, or $11.9bn net of native low-skill "
                 "wage gains. They and the production gain price the same labour-supply shock on different populations "
                 "and are not reconciled, so the services figure is neither added nor counted as included. Cheaper "
                 "construction is inside the production gain and adds nothing: construction costs 0.75% less with the "
                 "group present, which holds 24.4% of construction-trades jobs. Of the household-service channel, only "
                 "the taxes native women pay on their extra hours count, and they are inside the main case; a separate "
                 "card under this entry shows them."),
        values=[
            val("cheaper household services to consumers, gross", "21.8",
                at(CARE, "The consumer surplus on cheaper services is $21.8bn gross")),
            val("same, net of native low-skill wage gains", "11.9 (3.9-12.8)",
                at(CARE, "| Consumer surplus on services, net of native low-skill wage gain |")),
            val("construction costs with the group present", "0.75% lower (0.53-1.17%)",
                at(CONSTRUCTION, "In the account's own factor prices", through="lower** with the group present"),
                unit="percent"),
            val("group's share of construction-trades jobs", "24.4%", at(CONSTRUCTION, "24.4% of construction-trades jobs"),
                unit="share"),
        ],
        combining_rule=faq_excerpt("Cheaper household services ($21.8bn to consumers)", "counted as included."),
        memo=(f"{FAQ} § 4; {CARE} § Overlap ruling; {CONSTRUCTION}; "
              "research/immigration-consumer-price-and-native-hours-2026-09-18.md"),
        comparator="the account's production term; the two price the same shock and are not reconciled",
        evidence_level="[CALCULATION: care and construction lanes] + [INFERENCE: overlap ruling]",
    ),
    "e4_production_gain_inside_headline": dict(
        finding=("The account adds production gains and the induced taxes on them: $7.8bn (cash scaling) to $11.9bn "
                 "(GDP scaling) on the account's own weights, the 3.04M added descendants included, and $6–19bn across "
                 "the parameter grid."),
        values=[
            val("production plus induced receipts, cash / GDP scaling", "7.8 / 11.9",
                at(FAQ, "$7.8bn (cash scaling) to $11.9bn (GDP scaling)")),
            val("across the parameter grid", "6-19", at(FAQ, "($6–19bn across the parameter grid")),
        ],
        combining_rule=faq_excerpt("The production gain ($7.8–11.9bn)", "is inside the headline."),
        memo=f"{FAQ} § 4; {R07}; {CAA} § Benefits joined to an explicit fiscal response",
        population=("the 42.75M lineage; the production counterfactual is a stationary economy with and without the "
                    "group's labour"),
    ),
    "e4_scale_and_schooling_net": dict(
        finding=("City size and the group's schooling mix, measured in one regression, net to +$13.7bn a year on the "
                 "account's count (+$13.9bn on the survey's own count, 95% interval −$56.6bn to +$84.4bn): bigger "
                 "cities add "
                 "$38.6bn to other residents' earnings, and lower average schooling takes back $24.9bn. The net counts "
                 "whole, induced receipts included, as a benefit in the fiscal-plus-social total; the fiscal main case "
                 "does not carry it. The instrumented 1970–2000 college-share studies would make it a $109–677bn cost "
                 "instead. The patent term is positive but imprecise, +$37–57bn inside an interval of about ±$490bn, "
                 "and is not added."),
        values=[
            val("net of city size and schooling mix on the account's count, a benefit row of the fiscal-plus-social "
                "total", "13.7", at(FAQ, "mix, $13.7bn (on the survey's raw 40.9M count, bigger cities add $38.6bn")),
            val("same on the survey's own count (95% interval)", "+13.9 (-56.6 to +84.4)",
                at(SCALE, "are worth **+$13.9bn a year**")),
            val("city size / lower schooling, net of the account's own substitution", "+38.6 / -24.9",
                at(FAQ, "mix, $13.7bn (on the survey's raw 40.9M count, bigger cities add $38.6bn", through="takes back $24.9bn")),
            val("net with the instrumented 1970–2000 college-share studies", "-109 to -677",
                at(FAQ, "The 1970–2000 college-share studies would turn the scale net")),
            val("innovation: the patent term inside its interval, not added", "+37 to +57 (about ±490)",
                at(FAQ, "The patent term is positive but imprecise", through="±$490bn")),
        ],
        combining_rule=faq_excerpt("The net of city size and schooling mix", "does not carry it."),
        memo=(f"{SCALE}; {FAQ} § 4; {REAL} § 3b; {LADDER} entry 201; "
              "decisions/2026-09-28-social-items-scale-benefits.md"),
        evidence_level=("[CALCULATION: scale lane] + [INFERENCE: cross-sectional gradients]; a benefit row of the "
                        "fiscal-plus-social total"),
    ),
    "e4_shock_insurance_mobility": dict(
        value_edits={0: dict(label="mobility insurance, total")},
        finding=("The group's mobility across local labour markets is worth about $0.65bn a year to other residents "
                 "($0.18–2.46bn). It sits beside both the fiscal account and the fiscal-plus-social total; its fiscal "
                 "slice is $0.03bn. Mexico-born men with high school or less no longer move more than other natives: "
                 "they moved between states or arrived from abroad at 1.92% a year in 2019–24, against 2.13%. "
                 "Local-shock insurance is worth $0.13bn at today's mobility, and Borjas's efficiency gain at the "
                 "group's observed location $0.52bn."),
        combining_rule=faq_excerpt("Mobility insurance ($0.65bn", "sits beside both totals."),
    ),
    "real_costs_and_benefits_totals": dict(
        faq_entry=4,
        objection="Cheaper services, complementary labour and capital returns never appear in a fiscal ledger.",
        finding=("Beside the fiscal account, other residents' social costs and benefits bring the total to "
                 "$489.0–570.7bn a year at central values, $11.4–13.3k per member of the 42.75M lineage; counting "
                 "benefits when paid, $407.3–494.6bn. The largest rows are fine particles from the group's consumption "
                 "($68.1bn) and crime victims' harm ($30.5–31.9bn); five benefits enter as negative costs, together "
                 "$35.4bn. The low end assumes Mexican-origin offending equals the Hispanic average; the high end "
                 "assumes it sits above that average, as custody does. The 3.04M added descendants' own rows take their "
                 "share of each row's key."),
        values=[
            val("fiscal and social costs together, central values", "489.0-570.7",
                at(REAL, "Fiscal and social costs together come to **$489.0–570.7bn")),
            val("per member of the 42.75M lineage", "11.4-13.3", at(REAL, "Fiscal and social costs together come to"),
                unit="$k/member/year"),
            val("same, counting benefits when paid", "407.3-494.6", at(REAL, "counting benefits when paid, $407.3–494.6bn")),
            val("largest social rows: fine particles (PM2.5); crime victims' harm, low / high end", "68.1; 30.5 / 31.9",
                at(REAL, "| Crime victims' harm, full cost", through="| Fine particles (PM2.5)")),
            val("five benefits, entered as negative costs", "-35.4", at(REAL, "| Five benefits: city size net of schooling")),
        ],
        combining_rule=faq_excerpt("**The fiscal-plus-social total is its own object.**", "at central values (entry 4)."),
        memo=(f"{REAL} verdict and § 7; {FAQ} § 4; "
              "infra/immigration-fiscal/sept24_propagation_2026_09_24/derived/oct07/real_costs_totals.csv"),
        population=("the 42.75M lineage: social rows on the 39.7M the account identifies, plus the 3.04M added "
                    "descendants' share of each row's key"),
        comparator="no reference group; the fiscal account plus social items beside it",
        horizon="annual, 2024 dollars, central values",
        evidence_level=("[CALCULATION: sums of lane results] + [FRAMING-SENSITIVE: lives valued at VSL; the added "
                        "descendants' rows are an ASSUMPTION]"),
    ),
    "e5_asec2026_replication": dict(
        finding=("The adult ledger, on taxes as the survey reports them, re-run on the next survey year moved from "
                 "−$6,066 to −$6,499, inside one standard error."),
    ),
    "e5_ethnic_attrition_narrows_gap": dict(
        finding=("Third-plus is self-identified. Adding back those who stopped identifying, who are 0.76 years "
                 "better schooled, narrows the per-person gap to third-plus whites by about $240, from −$8,218 to "
                 "−$7,981 (the measured generation split, with the income tax the survey misses on the main case's "
                 "keys), while the aggregate moves from −$336.1bn to −$340.9bn as more people are counted. Ethnic "
                 "attrition is measured on the 2025 CPS, and the defensible Mexican-origin total is "
                 "42–45M (floor 41.8M)."),
        values=[
            val("union gap vs third-plus whites → with attriters added (central arm, measured generation split, item T)",
                "-8,218 → -7,981", at(POPULATION, "narrows the per-person gap to third-plus whites by about $240"),
                unit="$/standardized person/year"),
            val("aggregate, standing → with attriters added", "-336.1 → -340.9",
                at(POPULATION, "narrows the per-person gap to third-plus whites by about $240")),
            val("defensible Mexican-origin population total", "42-45M (floor 41.8M)",
                at(POPULATION, "Defensible total 42–45M"), unit="people"),
        ],
        combining_rule=LEDGER_RULE,
        memo=(f"{FAQ} § 5; {POPULATION} § 4. Fiscal implication; {LADDER} entry 158"),
    ),
    "e5_gaps_under_both_allocations": dict(
        finding=("On the personal allocation the gap at white ages narrows at each step (−$9,180, −$7,609, −$7,074); "
                 "on the shared allocation it is −$8,791, −$8,420, −$7,039."),
        values=[
            val("personal, Mexico-born at white ages", -9180.038612,
                ledger_row("white_ages_today", "mexico_born", "personal"), unit="$/person/year"),
            val("personal, second generation", -7608.803263,
                ledger_row("white_ages_today", "mexican_second_gen", "personal"), unit="$/person/year"),
            val("personal, third-plus self-ID", -7074.456625,
                ledger_row("white_ages_today", "mexican_third_plus_selfid", "personal"), unit="$/person/year"),
            val("shared, Mexico-born at white ages", -8790.554157,
                ledger_row("white_ages_today", "mexico_born"), unit="$/person/year"),
            val("shared, second generation", -8420.202117,
                ledger_row("white_ages_today", "mexican_second_gen"), unit="$/person/year"),
        ],
        combining_rule=LEDGER_RULE,
    ),
    "e5_generation_difference_tests": dict(
        finding=("The first and second generations are indistinguishable ($350 apart, standard error at most 1,060); "
                 "the third-plus is $1,732 better than the first, at least 2.1 standard errors."),
        values=[
            val("first minus second generation gap difference (standard error at most)", "350 (SE at most 1,060)",
                at(FAQ, "($350 apart, standard", through="error at most 1,060"), unit="$/person/year"),
            val("third-plus better than first (standard errors)", "1,732 (at least 2.1 SE)",
                at(FAQ, "the third-plus is $1,732 better than the first"), unit="$/person/year"),
        ],
        combining_rule=LEDGER_RULE,
    ),
    "e5_lifetime_npv_from_birth": dict(
        finding=("Period-profile lifetime values at 3%: second generation from birth −$267k, third-plus −$215k, white "
                 "reference −$68k. Mexico-born residents at 25 are −$41k against +$324k for whites at 25."),
        values=[
            val("second generation, age 0, expanded partial profile NPV", -266917,
                at(LEDGER, "Present values of the **current personal-source age profiles**",
                   through="| Second generation, age 0 |"), unit="$/person, 3% real"),
            val("third-plus self-identified, age 0", -215392, at(LEDGER, "| Third-plus self-identified, age 0 |"),
                unit="$/person, 3% real"),
            val("white reference, age 0", -68163, at(LEDGER, "| White reference, age 0 |"), unit="$/person, 3% real"),
            val("Mexico-born, age 25", -41058, at(LEDGER, "| Mexico-born, age 25 |"), unit="$/person, 3% real"),
            val("white reference, age 25", 323794, at(LEDGER, "| White reference, age 25 |"), unit="$/person, 3% real"),
        ],
        combining_rule=faq_excerpt("The National Academies results it is usually set against", "Neither refutes the other."),
    ),
    "e5_national_academies_different_object": dict(
        combining_rule=faq_excerpt("Entry 5 compares", "Neither refutes the other."),
    ),
    "e5_same_age_gaps_by_generation": dict(
        finding=("The same-age gap against third-plus non-Hispanic whites is −$8,849, −$8,499 and −$7,118 for the "
                 "first, second and third-plus generations, with standard errors of 539, 912 and 637; for all "
                 "generations together it is −$8,306."),
        values=[
            val("Mexico-born vs third-plus NH white, complete common-age gap", -8849.420596682718,
                gap_row("mexico_born", "third_plus_nh_white"), unit="$/standardized person/year"),
            val("second generation vs third-plus NH white", -8499.052464827088,
                gap_row("mexican_second_gen", "third_plus_nh_white"), unit="$/standardized person/year"),
            val("third-plus self-ID vs third-plus NH white", -7117.787073631764,
                gap_row("mexican_third_plus_selfid", "third_plus_nh_white"), unit="$/standardized person/year"),
            val("all generations against third-plus non-Hispanic whites", -8305.604765259666,
                gap_row("mexican_observed_total", "third_plus_nh_white"), unit="$/standardized person/year"),
            val("all generations, age-matched total against whites", -403.59491064671687,
                gap_row("mexican_observed_total", "third_plus_nh_white")),
        ],
        combining_rule=LEDGER_RULE,
        population=("generations alive in 2024: Mexico-born 12.221m, second generation 14.333m, third-plus "
                    "self-identified 14.343m (the survey's counts)"),
    ),
    "e5_tax_convergence_by_generation": dict(
        finding=("Taxes converge ($13.4k, $9.4k and $7.9k below whites) but the first generation's lower benefit use "
                 "disappears by the second."),
        values=[
            val("Mexico-born receipts gap vs white at white ages", -13415.144461,
                ledger_row("white_ages_today", "mexico_born"), unit="$/person/year"),
            val("second generation receipts gap", -9373.040694,
                ledger_row("white_ages_today", "mexican_second_gen"), unit="$/person/year"),
            val("third-plus self-ID receipts gap", -7906.712114,
                ledger_row("white_ages_today", "mexican_third_plus_selfid"), unit="$/person/year"),
        ],
        combining_rule=LEDGER_RULE,
        memo=f"{FAQ} § 5 and § 9; {LEDGER} § Same rates under different age structures",
    ),
    "e6_gap_against_average_resident": dict(
        finding=("Against as many average residents, the main case's gap counting benefits when paid is −$279–310bn, "
                 "about −$6,500 to −$7,200 per person; the gap is defined on cash flows only, because an accrued "
                 "pension has no national total to share out. The net-cost headline compares with no reference group "
                 "at all: it is the change for all other residents, other immigrants included. Third-plus whites are "
                 "not a flattering reference either: with every group's income taxes on the case's own keys they about "
                 "break even on accrual, so the gap against as many of them, $432–436bn a year, falls inside the main "
                 "case's $389–461bn."),
        values=[
            val("gap against as many average residents, main case counting benefits when paid (low / high end)",
                "-278.9 / -309.7", at(BLACK, "| Normalized gap, cash set | −278.9 / −309.7 | −260.4")),
            val("per person", "about -6,500 to -7,200", at(FAQ, "many average residents, the main case's gap",
                through="−$7,200 per person"), unit="$/person/year"),
            val("gap against as many third-plus non-Hispanic whites, every group's income taxes on the case's keys",
                "432-436", at(FAQ, "$432–436bn a year, falls inside the main case's")),
        ],
        combining_rule=faq_excerpt(*TWO_ANCHORS),
        memo=(f"{FAQ} § 6; {BLACK} (`derived/rekey_summary_oct07.csv`); "
              "infra/immigration-fiscal/white_replacement_2026_09_28/RESULT.md"),
        population="the 42.75M lineage against as many average residents, or as many third-plus non-Hispanic whites",
        comparator=("as many average residents (cash flows only); as many third-plus non-Hispanic whites on the case's "
                    "income-tax keys"),
        horizon="annual 2024",
        evidence_level="[CALCULATION: comparator lanes on main case v6]",
    ),
    "e6_gaps_against_all_natives": dict(
        finding=("Against all natives the same-age gaps are −$6,478, −$6,128 and −$4,747, and −$5,935 for all "
                 "generations together."),
        values=[
            val("Mexico-born vs all natives, complete common-age gap", -6478.4279387174265,
                gap_row("mexico_born", "all_native"), unit="$/standardized person/year"),
            val("second generation vs all natives", -6128.0598068617965,
                gap_row("mexican_second_gen", "all_native"), unit="$/standardized person/year"),
            val("third-plus self-ID vs all natives", -4746.794415666471,
                gap_row("mexican_third_plus_selfid", "all_native"), unit="$/standardized person/year"),
            val("all generations against all natives", -5934.612107294374,
                gap_row("mexican_observed_total", "all_native"), unit="$/standardized person/year"),
        ],
        combining_rule=LEDGER_RULE,
    ),
    "e7_cell_level_is_not_a_gap": dict(
        comparator="none; the cell's own level",
        finding=("Within this one schooling group the balance is still negative (−$1,879 personal, −$5,518 shared). "
                 "That is a level, so it should not be set against the gaps against another group."),
        values=[
            val("Mexico-born below-HS cell, own net balance: personal / shared", "-1,879 / -5,518",
                at(EDUCATION, "| Below HS | 3,885,815 |"), unit="$/person/year"),
            val("same cell, shared, unrounded", -5517.650168625485,
                csv_row(EDUCATION_ESTIMATES, **BELOW_HS_CELL), unit="$/person/year"),
            val("cell population", 3885815.28273003, csv_row(EDUCATION_ESTIMATES, **BELOW_HS_CELL), unit="people"),
        ],
        combining_rule=faq_excerpt(*PARTIAL),
        memo=f"{EDUCATION} § Annual results; {FISCAL}/education_origin_fiscal_2026_09_19/RESULT.md",
    ),
    "e7_education_specific_gaps": dict(
        finding=("Below-high-school Mexico-born adults do at least as well as below-high-school natives at common ages, "
                 "while high-school-only adults do worse. With the income tax the survey misses, the advantage over "
                 "natives below high school holds only with household costs shared (+$1,908, interval +$40 to "
                 "+$3,777); on the personal allocation (+$1,779, −$1,071 to +$4,628) it cannot be told from zero, and "
                 "against whites below high school it cannot be told from zero under either allocation. The aggregate "
                 "gap is largely a composition effect, which describes who the residents are and does not make the "
                 "dollars smaller."),
        values=[
            val("below HS vs natives below HS, personal", 1778.555569405449,
                comparison_row("181", "personal", "lt_hs", "all_native"), unit="$/person/year"),
            val("below HS vs natives below HS, shared", 1908.4689382458637,
                comparison_row("1", "shared", "lt_hs", "all_native"), unit="$/person/year"),
            val("below HS vs third-plus whites below HS, personal", -24.598893127463498,
                comparison_row("181", "personal", "lt_hs", "third_plus_nh_white"), unit="$/person/year"),
            val("below HS vs third-plus whites below HS, shared", 259.9782226901526,
                comparison_row("1", "shared", "lt_hs", "third_plus_nh_white"), unit="$/person/year"),
            val("HS only vs natives HS only, personal", -2949.917906145647,
                comparison_row("187", "personal", "hs_only", "all_native"), unit="$/person/year"),
        ],
        combining_rule=faq_excerpt(*PARTIAL),
        memo=f"{EDUCATION} § Annual results; {FAQ} § 7 table",
    ),
    "e8_backcast_cumulative_windows": dict(
        finding=("Carrying the 2024 position back on measured national series gives, on the main case, $3.4–4.4tn over "
                 "ten years (2015–2024), $4.8–6.4tn over fifteen and $5.8–8.1tn over twenty (whole-budget rules; the "
                 "added descendants follow the identified third-plus generation's count). The return on public "
                 "capital, an imputed cost that no budget pays in cash, is $0.32–0.53tn of the ten years under the ratio "
                 "rule "
                 "($0.35–0.58tn under the flat rule)."),
        values=[
            val("ten / fifteen / twenty years to 2024, the main case, whole-budget rules", "3.4-4.4 / 4.8-6.4 / 5.8-8.1",
                at(BACKCAST, "**Main case v6 (adopted 2026-10-07"), unit="$tn, 2024 dollars"),
            val("of the ten years, the return on public capital: ratio rule (flat rule)", "0.32-0.53 (0.35-0.58)",
                at(BACKCAST, "**Main case v6 (adopted 2026-10-07"), unit="$tn, 2024 dollars"),
        ],
        memo=(f"{BACKCAST} § Main case v6; infra/immigration-fiscal/historical_backcast_2026_09_20/derived/oct07/"
              f"backcast_windows.csv; {FAQ} § 8"),
        population=("measured ACS Mexican-origin count each year; the added descendants on the identified third-plus "
                    "generation's count; the group's 2024 relative position assumed constant"),
        comparator="other residents (the net-cost concept)",
        horizon="cumulative over 2015–2024, 2010–2024 and 2005–2024, in 2024 dollars",
    ),
    "e8_measured_programme_series": dict(
        evidence_level="[DERIVATION]",
        finding=("National spending per resident on each programme is measured for every year: Medicaid and Medicare "
                 "were 42–47% smaller in 2005, refundable credits were 4.4 times their 2024 level in 2021, police, "
                 "courts and prisons were flat. The group got the 2020–2021 pandemic payments at 0.87–1.03 times other "
                 "residents per person."),
        values=[
            val("Medicaid and Medicare per resident in 2005, smaller than in 2024", "42-47%",
                at(BACKCAST, "Benefits did change: Medicaid and Medicare were 42–47% smaller"), unit="percent"),
            val("Medicaid/CHIP/other medical index, 2005 (2024 = 1)", 0.58,
                at(BACKCAST, "Real national spending per resident, 2024 = 1", through="| Medicaid, CHIP, other medical (117) |"),
                unit="index"),
            val("Medicare index, 2005", 0.53, at(BACKCAST, "| Medicare (64) |"), unit="index"),
            val("refundable tax credits index, 2021", 4.36, at(BACKCAST, "| Refundable tax credits (55) |"), unit="index"),
            val("the group's 2020 / 2021 pandemic payments per person, relative to other residents", "0.87 / 1.03",
                at(BACKCAST, "0.87 times other residents per person (1.02 before the SSN rule)"), unit="ratio"),
        ],
    ),
    "e9_arrival_window_gaps": dict(
        finding=("On the partial account, with taxes as the survey reports them, the 2016–2025 arrival window is "
                 "−$3,978 per standardized person against whites and the older windows −$4,800 to −$5,300; the income "
                 "tax the survey misses widens them to −$5,498 and −$6,600 to −$7,000, mostly through the whites' side. "
                 "The newest window stays the least negative, and no step between adjacent windows reaches one standard "
                 "error."),
        values=[
            val("2016–2025 window vs third-plus NH white: survey taxes → with the missing income tax", "-3,978 → -5,498",
                at(ARRIVAL, "| 2016–2025 | −3,978 | −5,498 |"), unit="$/standardized person/year", se="1,349 (with it)"),
            val("older windows: survey taxes → with the missing income tax", "-4,800 to -5,300 → -6,600 to -7,000",
                at(ARRIVAL, "With T the verdict's −$3,978"), unit="$/standardized person/year"),
            val("all Mexico-born: survey taxes → with the missing income tax", "-5,360 → -6,979",
                at(ARRIVAL, "| all Mexico-born | −5,360 | −6,979 |"), unit="$/standardized person/year", se="765 (with it)"),
            val("first difference into the newest window", "+1,236 (SE 1,554)",
                at(ARRIVAL, "The first difference into it is +1,236"), unit="$/standardized person/year"),
        ],
        combining_rule=faq_excerpt(*PARTIAL),
        memo=f"{ARRIVAL} § window table and the item-T section; {FAQ} § 9",
        horizon="annual 2024; the partial account, with and without the income tax the survey misses",
    ),
    "e10_ageing_by_category": dict(
        values=[
            val("cash transfers incl. Social Security (memo's stated change)", "-70.2",
                at(LEDGER, "[DERIVATION] In dollars at the observed 40.9m headcount")),
            val("public medical", "-80.2", at(LEDGER, "[DERIVATION] In dollars at the observed 40.9m headcount")),
            val("institutions", -7.9, at(LEDGER, "[DERIVATION] In dollars at the observed 40.9m headcount")),
            val("rest of federal", -7.4, at(LEDGER, "[DERIVATION] In dollars at the observed 40.9m headcount")),
            val("K-12", "30.9", at(LEDGER, "[DERIVATION] In dollars at the observed 40.9m headcount")),
        ],
        combining_rule=LEDGER_RULE,
    ),
    "e10_ageing_composition_total": dict(
        finding=("At the white age structure and today's rates the 40.9m residents' balance moves from −$203.5bn to "
                 "−$324.6bn, a change of −$121.1bn; the same number of white-reference residents at those ages runs "
                 "+$12.2bn. This is a composition exercise on the generation ledger; it forecasts nothing."),
        values=[
            val("all generations, shared balance: own ages → white age structure", "-203.5 → -324.6",
                at(LEDGER, "[DERIVATION] In dollars at the observed 40.9m headcount")),
            val("change", "-121.1", at(LEDGER, "[DERIVATION] In dollars at the observed 40.9m headcount")),
            val("personal-source equivalent", "-223.9 → -321.9",
                at(LEDGER, "[DERIVATION] In dollars at the observed 40.9m headcount")),
            val("same number of white-reference residents at those ages", "+12.2",
                at(LEDGER, "[DERIVATION] In dollars at the observed 40.9m headcount")),
            val("like-for-like difference: at white ages / each group at its own ages", "-336.8 / -215.7",
                at(LEDGER, "[DERIVATION] In dollars at the observed 40.9m headcount")),
        ],
        combining_rule=LEDGER_RULE,
    ),
    "e10_old_age_cells_rest_on_small_cohorts": dict(combining_rule=LEDGER_RULE),
    "e11_not_a_policy_saving": dict(
        objection="So ending this migration would save $389–461bn?",
        finding=("No. The account describes a resident stock in a stationary comparison. It is not the effect of an "
                 "admission rule, a removal policy or one more arrival, it contains no transition costs, and most of the "
                 "people in it are US-born citizens. In the first years budgets would not shed the full average cost of "
                 "the group's pupils, nor the long-run road and park costs: with CBO's year-to-year responses, no "
                 "capital response and benefits counted when paid, the main case gives $207–260bn ($289–336bn with the "
                 "pension accrual). The return on public capital ($37–61bn of the case) is an opportunity cost, and the "
                 "pension accrual ($76–82bn) a promise of future benefits; neither is cash a removal would free in the "
                 "year. Schools show how slowly budgets shrink: across US districts whose enrollment fell over "
                 "twenty-year spans, spending fell only about 30% as fast, so they kept about 70% of the money."),
        values=[
            val("the number the objection misuses: the main case", "389.1-461.5",
                at(FAQ, "conditional net cost to other residents at $389–461bn a year ($389.1–461.5bn)")),
            val("first years: CBO's year-to-year responses, no capital response, benefits counted when paid; with the "
                "pension accrual", "207-260 / 289-336", at(FAQ, "$207–260bn ($289–336bn with the pension accrual)")),
            val("the return on public capital inside the case, an opportunity cost", "37-61",
                at(FAQ, "public capital ($37–61bn of the case)")),
            val("the pension accrual inside the case, a promise of future benefits", "76-82",
                at(FAQ, "public capital ($37–61bn of the case)")),
            val("districts with falling enrollment: spending fell as fast as enrollment / money kept",
                "about 30% / 70%", at(FAQ, "fell only about 30% as fast"), unit="share"),
        ],
        combining_rule=faq_excerpt(*TWO_ANCHORS),
        memo=f"{FAQ} § 11; {CAA} § Units, population and comparison; {FY}",
        population="the 42.75M lineage, most of them US-born citizens",
        comparator="no reference group; a stationary comparison",
        horizon="annual 2024; no transition path, no lifetime or lineage value",
    ),
    "e9_new_arrivals_education": dict(
        # The table's caption line states who the shares cover.
        value_edits={0: dict(file_line=at(COHORTS, "Mexico-born, ages 25–54, arrived within the previous five years.",
                                          through="| 1980 census | 1975–80 |"))},
    ),
    "e12_incarceration_ratio_series": dict(
        # The FAQ paragraph runs from the 2024 ratio to the 2000 figure with allocated birthplaces spread.
        value_edits={1: dict(label="2024 ratio; coding-adjusted ratios, 2019–2024", value="1.94×; 2.10-2.23×",
                             file_line=at(FAQ, "(2023, the low point), 1.94× (2024)", through="2.7–3.0× (ladder 196)"))},
    ),
    "e12_no_group_crime_cost_in_headline": dict(
        finding=("The main case charges police, courts and prisons by use: prisons by custody, police half by arrests, "
                 "courts by their criminal share and border enforcement per head. The use key adds little because the "
                 "account compares the group with the average other resident: Hispanic residents are 20.2% of people "
                 "in prisons and jails against 20.7% of residents aged 18–64. The main case does not isolate what the "
                 "key adds; if Mexican-origin offending equals the Hispanic average as census codes record it, the case "
                 "is $4.8bn lower at both ends. Jail counts carry no ethnicity adjustment; with jails at the arrest "
                 "share, prisons and jails "
                 "are 22.9% Hispanic. Victim costs sit outside the fiscal account: crimes by group members against "
                 "other residents cost the victims $30.5–31.9bn a year among the 39.7M people the account identifies, "
                 "and about $33bn with the 3.04M added descendants, a social cost in the fiscal-plus-social total. "
                 "Police records agree: on Texas and Arizona offender rates the victims' cost is $28.6bn."),
        values=[
            val("main case less the case with Mexican-origin offending at the Hispanic average as census codes record "
                "it, at both ends", "4.8", at(FAQ, "The main case does not isolate", through="lower at both ends")),
            val("Hispanic share of people in prisons and jails / of residents aged 18–64", "20.2% / 20.7%",
                at(FAQ, "the account compares the group with the average other resident: Hispanic residents are 20.2%",
                   through="people in prisons and jails against 20.7%"), unit="share"),
            val("prisons and jails with jails at the arrest share", "22.9%",
                at(FAQ, "prisons and jails are 22.9% Hispanic"), unit="share Hispanic"),
            val("victims' harm from crimes by group members against other residents, among the 39.7M; with the 3.04M "
                "added descendants (social cost, beside the fiscal headline)", "30.5-31.9; about 33",
                at(FAQ, "other residents cost the victims $30.5–31.9bn", through="about $33bn with the 3.04M")),
            val("victims' cost on Texas and Arizona police-record offender rates", "28.6",
                at(FAQ, "crude rates for Hispanics of any origin. On those inputs the victims' cost is $28.6bn")),
        ],
        combining_rule=("Victim costs are outside the fiscal account. They count in the fiscal-plus-social total, "
                        "beside the fiscal headline, which already charges police, courts and prisons by use."),
        comparator="the average other resident, the account's comparison",
        memo=(f"{FAQ} § 12; {REAL} § 2–3 and § 6; infra/immigration-fiscal/offender_ethnicity_nibrs_2026_09_23/"
              "RESULT.md; research/immigration-detention-crime-and-fiscal-scope-2026-09-20.md (measurement rule)"),
        population="the lineage's share of public order and safety spending; victims among other residents",
        evidence_level=("[CALCULATION: justice-by-use lane, 38 gates] + [MODEL: victim harm, lives valued at VSL; "
                        "offender rates from NIBRS]"),
    ),
    "e13_care_workforce_composition": dict(
        finding=("The channel reaches this group. Counting its US-born members, the group supplies 15.4% of home-care "
                 "hours against 12.0% of residents; the Mexico-born alone are 14.5% of foreign-born direct-care workers "
                 "and 37.7% of the less-educated foreign-born. Secure Communities, which removed mostly Mexican and "
                 "Central American workers, cut home-care hours and raised institutionalization of the US-born "
                 "elderly."),
        combining_rule=faq_excerpt(*CARE_ITEMS),
    ),
    "e13_elder_care_medicaid_bound": dict(
        finding=("Netted, the Medicaid saving is about $1.5bn a year (design range $1.2–7.6bn; 90% interval −$1.8bn to "
                 "+$8.3bn), and it is inside the main case. The group's own care needs absorb more than half of what it "
                 "supplies, so the net dose is 7.2%; per unit of dose, nursing-home residents rise only 2.7%; Medicaid "
                 "pays $45,197 per institutionalized resident 65+; and the same workers staff $1.0–1.3bn of Medicaid "
                 "home care, which Medicaid rations when aides are scarce."),
        values=[
            val("net Medicaid saving: nursing facilities less Medicaid home care", "1.5 (1.2-7.6)",
                at(CARE, "- **Net Medicaid effect of the group's home-care workers: $1.5bn.**"),
                se="90% interval -1.8 to +8.3"),
            val("net dose: fall in care per unit of other residents' need", "7.2% (5.3-9.3%)",
                at(CARE, "- Care available per unit of other residents' need therefore falls 7.2%"), unit="share"),
            val("nursing-home residents per unit of dose (Secure Communities)", "2.7%",
                at(CARE, "Secure Communities raised nursing-home residents by only 2.7%"), unit="share"),
            val("Medicaid price per institutionalized resident 65+", "45,197",
                at(CARE, "The 65+ share gives $45,197"), unit="$"),
            val("Medicaid home care the same workers staff, an outlay", "1.0-1.3",
                at(CARE, "- the same workers staff $1.0–1.3bn of Medicaid home care.")),
        ],
        combining_rule=faq_excerpt(*CARE_ITEMS),
        memo=(f"{FAQ} § 13; {CARE} § 2. Elder care; research/immigration-marginal-revolution-leads-read-2026-09-21.md "
              "§ 1"),
        comparator="the account, with other residents' nursing-facility spending priced",
    ),
    "e13_mortality_instrument_null": dict(
        combining_rule=faq_excerpt(*CARE_ITEMS),
        value_edits={1: dict(file_line=at(LEADS, "**Grabowski–Gruber–McGarry.**",
                                          through="deaths a year among Medicare beneficiaries"))},
    ),
    "e14_complementarity_removal_model": dict(
        objection=("If natives and immigrants are imperfect substitutes, natives' wages rise with immigrant labour even "
                   "after capital adjusts. A 2026 general-equilibrium model puts the native loss from removing half of "
                   "unauthorized workers at 0.33% of wages, $38.6bn a year at 2024 wages and $26.8–80.4bn across "
                   "published elasticities."),
        finding=("This is a fair hit on the account's production term, which treats union and outside workers in the "
                 "same skill group as perfect substitutes. Three limits keep the model's figure from being added as it "
                 "stands. Its aggregate real wage is unchanged by construction, so the native gain is matched by losses "
                 "of other immigrants, who are among the other residents here. Its natives include naturalized citizens "
                 "and every US-born Mexican-origin worker. It has no taxes, transfers or public services. Direct "
                 "estimates put the elasticity of substitution well above the model's midpoint of 3, which shrinks the "
                 "term. Applied, the objection would change the size of the production term and leave the sign of the "
                 "account as it is; it is not applied."),
        comparator="the account's production term ($7.8–11.9bn in the main case)",
        combining_rule=faq_excerpt("The complementarity figure ($26.8–80.4bn)", "matched by other immigrants' losses."),
    ),
    "e15_same_share_different_gap": dict(
        objection=CA_TX_OBJECTION,
        finding=("The two states have the same Mexican-origin share and different gaps. On the shared all-age ledger, "
                 "matched to local third-plus non-Hispanic whites at common ages, with the income tax the survey misses "
                 "on the main case's keys, California is −$15,228 per person a year and Texas −$9,267; Los Angeles is "
                 "−$21,083 and Houston −$8,977. With taxes as the survey reports them the four are −$12,133, −$7,479, "
                 "−$17,196 and −$7,493. The added tax rests on few records: the ten largest white households carry 67% "
                 "of whites' added tax in California and 98% in Texas. Every interval is adverse: Texas's gap is "
                 "smaller than California's and still clearly negative. Nominal dollars, with no regional price "
                 "parity."),
        values=[
            val("California vs local third-plus NH whites, with the missing income tax (95% interval)",
                "-15,228 (-18,291 to -12,164)",
                at(STRESS, "Union against local third-plus NH whites, shared allocation",
                   through="| California, own-state white ages |"), unit="$/standardized person/year"),
            val("Texas, same", "-9,267 (-12,530 to -6,004)", at(STRESS, "| Texas, own-state white ages |"),
                unit="$/standardized person/year"),
            val("Los Angeles / Houston, same", "-21,083 / -8,977",
                at(METRO, "| Los Angeles | −17,196 [−21,144, −13,249] | −21,083", through="| Houston | −7,493"),
                unit="$/standardized person/year"),
            val("California / Texas with taxes as the survey reports them", "-12,133 / -7,479",
                at(STRESS, "| California, own-state white ages |", through="| Texas, own-state white ages |"),
                unit="$/standardized person/year"),
            val("ten largest white households' share of whites' added tax: California / Texas", "67% / 98%",
                at(STRESS, "The ten largest SPM units carry 67%", through="98% of Texas whites'"), unit="share"),
        ],
        combining_rule=faq_excerpt(*CA_TX),
        memo=(f"{FAQ} § 15; research/immigration-california-texas-fiscal-geography-2026-09-21.md; {STRESS} § item T "
              f"(`derived/state_matched_T.csv`); {METRO} § item T (`derived/metro_matched_T.csv`)"),
        evidence_level=("[CALCULATION: stress and metro-match lanes, shared all-age partial ledger with the missing "
                        "income tax] + [DATA: CPS ASEC 2025]"),
    ),
    "e15_shares_and_metro_match": dict(
        objection=CA_TX_OBJECTION,
        finding=("The shares match: 31.7–33.5% Mexican-origin in Texas and 31.8–32.5% in California in the ACS state "
                 "series, 31.0% and 30.8% in the 2020 Census. Matching on metro barely moves the national per-person "
                 "gap against whites (−$6,910 at age only, −$6,818 by metro and age); it widens the national total "
                 "from −$339bn to −$492bn, because the group lives where the local white benchmark is higher. Share "
                 "catch-up toward 32% is already realized in Texas and does not produce Los Angeles–sized dollars. New "
                 "York holds 1.4% of the US Mexican-origin population, and San Francisco has no published single-metro "
                 "gap."),
        values=[
            val("Mexican-origin share of residents, ACS state series, Texas / California", "31.7-33.5% / 31.8-32.5%",
                at(FAQ, "(ACS 31.7–33.5% Texas"), unit="share"),
            val("same, 2020 Census, Texas / California", "31.0% / 30.8%", at(FAQ, "2020 Census 31.0% / 30.8%"),
                unit="share"),
            val("national per-person gap vs third-plus NH whites, with the missing income tax: age only → metro × age",
                "-6,910 → -6,818", at(METRO, "| age only | −5,734", through="| metro × age | −5,797"),
                unit="$/standardized person/year"),
            val("national total gap vs third-plus NH whites, same: age only → metro × age", "-338.7 → -491.5",
                at(METRO, "widens with place: −$338.7bn age only")),
            val("New York's share of the US Mexican-origin population (residents)", "1.4% (0.50m)",
                at(FAQ, "New York is 1.4%", through="(0.50m)"), unit="share"),
        ],
        combining_rule=faq_excerpt(*CA_TX),
        memo=(f"{FAQ} § 15; research/immigration-california-texas-fiscal-geography-2026-09-21.md; {METRO} § item T; "
              "research/immigration-native-sorting-tiebout-2026-09-18.md; "
              "infra/immigration-fiscal/apportionment_2026_09_18/derived/arm_2020_mexican_origin.csv"),
    ),
    "e16_cbo_surge_projection": dict(
        finding=("The two numbers are different objects and both can hold. CBO's figure is a ten-year projection for "
                 "one recent inflow of every origin, mostly working-age adults in their first years, and it covers "
                 "federal revenue, mandatory spending and net interest only. Discretionary appropriations are excluded "
                 "(CBO's proportional illustration adds about $0.2tn of spending), and so are state and local budgets; "
                 "CBO's June 2025 companion puts the surge's 2023 state and local account at a $9.2bn net cost. This "
                 "account is one year of the resident Mexican-origin lineage of all ages and generations, state and "
                 "local services included: −$389bn to −$461bn in the main case, or −$289bn to −$336bn with CBO-style "
                 "first-year budget responses (−$207bn to −$260bn counting benefits when paid). Where the two overlap "
                 "they agree: Mexico-born arrivals of 2016–2025 are +$3,495 per person on the partial account with "
                 "taxes as the survey reports them, and about break-even (−$1,299, interval −$3,151 to +$554) once the "
                 "remaining items are charged flat per person."),
        values=[
            val("CBO, July 2024: lower covered federal deficits, 2024–2034 (revenue, mandatory spending, net interest)",
                "about 897", at("research/immigration-bryan-caplan-claims-audit-2026-04-21.md",
                                "CBO projects about `$897B` lower covered federal deficits"), unit="$bn over ten years"),
            val("CBO, June 2025: the surge's 2023 state and local net cost (broader alternative)", "9.2 (9.8)",
                at("research/immigration-second-order-effects-2026-09-05.md", "| Local services | CBO estimates"),
                unit="$bn, 2023"),
            val("this account, the main case: net effect on other residents", "-389 to -461",
                at(FAQ, "in deficit. Our account is the annual position", through="−260bn counting benefits when paid")),
            val("Mexico-born arrivals 2016–2025, partial account, taxes as the survey reports them", "+3,495",
                at(ARRIVAL, "| `w5_2016_2025` | +8.36 |"), unit="$/person/year"),
            val("same arrivals, partial account plus the remaining items charged flat per person (95% interval)",
                "-1,299 (-3,151 to +554)",
                at(ARRIVAL_ESTIMATES, "w5_2016_2025,,,partial_plus_G_K_X_R_absolute_per_person,", start=True),
                unit="$/person/year"),
        ],
        combining_rule=faq_excerpt("A decade of a cohort's cheapest years", "Neither refutes the other."),
        memo=(f"{FAQ} § 16; research/immigration-bryan-caplan-claims-audit-2026-04-21.md (federal-ledger rows); "
              "research/immigration-second-order-effects-2026-09-05.md (federal-finances row); "
              f"{ARRIVAL} § 3 and the complete-balance table; {ARRIVAL_ESTIMATES}; {R07}; {LADDER} entry 134"),
        population=("CBO: the 2021–2026 surge inflow of every origin; this account: the resident Mexican-origin lineage "
                    "of all ages and generations"),
    ),
    "e17_survey_errors_nearly_cancel": dict(
        finding=("The survey errors are real, but they run both ways. The survey overstates the group's taxes: its tax "
                 "model treats every respondent as a compliant resident filer, and Census's fill-ins keep only 9% of the "
                 "group's own wage gap; leaving the fill-ins in would lower the main case by $8.3–9.2bn. On the spending "
                 "side the keys overstated the charge: ACA premium credits had been keyed as if they were the EITC, and "
                 "long-term care had been charged at the group's 12.25% share of community Medicaid, where CMS records "
                 "give it 7.4% of those dollars. The main case carries every correction; their combined effect on it is "
                 "not measured separately. The main case, $389.1–461.5bn, spans $311.9–515.6bn with every correction "
                 "and every other component at its extreme at once, and no combination of these changes the sign; "
                 "freezing every service budget does (entry 2). Administrative records show no fear-driven benefit "
                 "under-reporting "
                 "where the group's dollars are: California's SNAP records give Hispanic participants 44.0% of benefit "
                 "dollars against the survey's 44.1%. The count error runs the other way: the CPS puts the Mexico-born "
                 "9–13% above the ACS, the adopted case corrects to the ACS level, and the people in the excess pay "
                 "about what they are charged."),
        values=[
            val("main case less the case with Census's income fill-ins left in, everything else as in the case",
                "8.3-9.2", at(FAQ, "Leaving the survey's", through="fill-ins in would lower the main case by $8.3–9.2bn")),
            val("long-term care: the group's share of community Medicaid, the old key / of the dollars in CMS records",
                "12.25% / 7.4%", at(FAQ, "charged at the group's share of community Medicaid, 12.25%"), unit="share"),
            val("main case with every correction and every other component at its extreme at once", "311.9-515.6",
                at(FAQ, "spans $311.9–515.6bn")),
            val("Hispanic share of California SNAP benefit dollars: administrative records / CPS", "44.0% / 44.1%",
                at(FAQ, "California's SNAP", through="44.0% of benefit dollars"), unit="share of dollars"),
            val("CPS Mexico-born count above the ACS since 2019; CPS / ACS-based level", "9-13%; 12.2M / 11.1M",
                at(FAQ, "population 9–13% above the larger American Community Survey"), unit="percent; persons"),
        ],
        memo=(f"{FAQ} § 17; {R07}; research/immigration-outside-checks-2026-09-24.md; {LADDER} entries 204, 208–210, "
              "216–217, 219, 225, 229 and 289"),
    ),
    "complete_account_assigned_balance": dict(
        finding=("Two parts make up the main case. $104.95–158.93bn is what any 42.75M average residents would cost "
                 "other residents under the same rules, mainly because governments spend more than they tax. The "
                 "group's own excess over as many average residents is $284.13–302.55bn: lower taxes at the same ages "
                 "make up $256.35 / 249.09bn of it (90% / 82%), its age mix adds $19.09 / 63.99bn and its use of "
                 "services at given ages +$8.69 / −$10.53bn. On the cash set lower taxes exceed the whole excess "
                 "(171% / 145%), and the age mix and service use reduce it."),
        values=[
            val("what any 42.75M average residents would cost other residents under the same rules", "104.95-158.93",
                at(INDEX, "Why it costs what it costs: $104.95")),
            val("the group's own excess over as many average residents", "284.13-302.55",
                at(INDEX, "Why it costs what it costs: $104.95")),
            val("of which lower taxes at the same ages, low / high end (share of the excess)", "256.35 / 249.09 (90% / 82%)",
                at(INDEX, "Why it costs what it costs: $104.95")),
            val("of which the age mix", "19.09 / 63.99", at(INDEX, "Why it costs what it costs: $104.95")),
            val("of which the use of services at given ages", "+8.69 / -10.53",
                at(INDEX, "Why it costs what it costs: $104.95")),
        ],
        combining_rule=faq_excerpt(*TWO_ANCHORS),
        memo=(f"{INDEX} § Adopted main case (\"Why it costs what it costs\"); "
              "infra/immigration-fiscal/main_case_decomposition_2026_09_29/RESULT.md (ladder 269)"),
        population="the 42.75M lineage",
        comparator="as many average residents under the same rules",
        horizon="annual 2024",
        evidence_level="[CALCULATION: decomposition of the main case]",
    ),
    "generation_ledger_annual_balances": dict(
        comparator="levels; the common-age shortfalls are the gap rows",
        finding=("Net receipts minus attributed expenditure by resident group, with the income tax the survey misses: "
                 "all Mexican-origin generations together run −$203.52bn household-shared and −$223.94bn "
                 "personal-source; the third-plus non-Hispanic white reference runs +$51.83bn and +$85.79bn."),
        values=[
            val("Mexico-born (12.221m), shared / personal", "-68.84 / -37.72", at(LEDGER, "| Mexico-born | 12.221 |")),
            val("Mexican second generation (14.333m)", "-81.79 / -91.56", at(LEDGER, "| Mexican second generation | 14.333 |")),
            val("Mexican third-plus self-identified (14.343m)", "-52.89 / -94.66",
                at(LEDGER, "| Mexican third-plus, self-identified | 14.343 |")),
            val("observed Mexican-origin population, all generations (40.897m)", "-203.52 / -223.94",
                at(LEDGER, "| Observed Mexican-origin union | 40.897 |")),
            val("third-plus NH white reference (173.054m)", "+51.83 / +85.79",
                at(LEDGER, "| Third-plus non-Hispanic white reference | 173.054 |")),
        ],
        combining_rule=LEDGER_RULE,
        horizon="annual, billions of 2024-price dollars per year; the income tax the survey misses included (item T)",
    ),
    "generation_ledger_later_annual_refreshes": dict(
        finding=("Two later annual accounts are separate releases without item T, and neither is applied to the "
                 "ledger's tables as a flat shift: the Census 2024 finance refresh gives the union −$234.34bn shared "
                 "and −$256.26bn personal, and the measured enrollment correction built on it −$259.38bn and "
                 "−$283.20bn."),
        values=[
            val("Census 2024 finance refresh, shared / personal", "-234.34 / -256.26", at(LEDGER, "**Status:**")),
            val("measured enrollment correction, shared / personal", "-259.38 / -283.20", at(LEDGER, "**Status:**")),
        ],
        combining_rule=faq_excerpt(*LATER_CORRECTIONS),
        memo=(f"{LEDGER} § Status; research/immigration-macro-reconciliation-2026-09-19.md; "
              "research/immigration-four-fiscal-checks-2026-09-20.md"),
    ),
    "ledger_absolute_uncertainty_scope": dict(
        finding=("The ledger's standard errors cover survey sampling only: $539, $912 and $637 per person on the three "
                 "generations' same-age gaps against whites, $446 on the union's and $17.8bn on its age-matched total. "
                 "They say nothing about the accounting choices, which move the result more: the two allocation "
                 "conventions alone put the union's annual balance at −$203.52bn shared and −$223.94bn personal."),
        values=[
            val("standard errors on the same-age gaps: Mexico-born / second generation / third-plus", "539 / 912 / 637",
                at(FAQ, "−$8,499, third-plus −$7,118 per person, standard errors 539, 912 and 637"),
                unit="$/standardized person"),
            val("standard error on the union's same-age gap against whites", 445.6980162204481,
                gap_row("mexican_observed_total", "third_plus_nh_white"), unit="$/standardized person"),
            val("standard error on the union's age-matched total", 17.788426808630746,
                gap_row("mexican_observed_total", "third_plus_nh_white"), unit="$bn"),
            val("the union's annual balance under the two allocation conventions, shared / personal", "-203.52 / -223.94",
                at(LEDGER, "| Observed Mexican-origin union | 40.897 |")),
        ],
        combining_rule=None,
        memo=f"{LEDGER} § Annual results; {GAPS}",
        evidence_level="[MODEL OUTPUT]; the standard errors are CPS replicate errors only",
    ),
    "service_scaling_test": dict(
        finding=("School spending rises .945% (districts weighted equally) or 1.004% (pupil-weighted) per 1% more pupils "
                 "across districts in 2019, and .735% or .836% within districts over 2000–2019; all ten full-panel "
                 "within-state service intervals include 1. The main case charges schools at their full average cost; "
                 "the within-district 0.836 gives the low side, $361–435bn."),
        values=[
            val("across districts, 2019 (unweighted / pupil-weighted)", ".945 [.929, .962] / 1.004 [.991, 1.017]",
                at(SCALING, "| Across districts, 2019 |"), unit="elasticity",
                se="bracketed intervals as printed in the memo table"),
            val("within districts, 2000/2010/2019", ".735 [.675, .796] / .836 [.787, .884]",
                at(SCALING, "| Within districts, 2000/2010/2019 |"), unit="elasticity",
                se="bracketed intervals as printed in the memo table"),
            val("main case with schools at the within-district 0.836 (the low side)", "361-435",
                at(FAQ, "the within-district 0.836 gives the low side, $361–435bn")),
        ],
        memo=(f"{SCALING}; {FAQ} § 2; decisions/2026-09-26-main-case-schools-full-cost.md"),
    ),
}

NEW = [
    dict(
        id="e2_legacy_financing_beside", faq_entry=2,
        objection="Charging every resident an equal share of the national deficit inflates any group's cost.",
        finding=("Obligations left by past budgets are stated beside the account, against third-plus non-Hispanic "
                 "whites on matched keys and the same headcount path. Carrying the 2005–2023 federal gaps as if borrowed, with past accrued Social "
                 "Security and Part A promises capitalized, the modeled excess annual financing charge in 2024 is "
                 "$101.6–101.7bn; carrying those accruals with payroll instead of benefits gives $92.2–92.3bn, and "
                 "counting benefits when paid $35.6–36.3bn. The public-employee pension excess is $5.4bn of attributed "
                 "interest expense. There is no combined legacy total, and both rows stay outside the headline. Both "
                 "are model outputs; no group debt is measured."),
        values=[
            val("excess annual financing charge in 2024, past accrued Social Security and Part A promises capitalized "
                "as if borrowed", "101.6-101.7", at(FAQ, "charge is **$101.6–101.7bn**")),
            val("same, those accruals carried with payroll instead of benefits", "92.2-92.3",
                at(FAQ, "payroll instead of benefits gives **$92.2–92.3bn**")),
            val("same, counting benefits when paid", "35.6-36.3", at(FAQ, "counting benefits when paid gives **$35.6–36.3bn**")),
            val("public-employee pension excess, attributed interest expense", "5.4",
                at(FAQ, "The public-employee pension excess is **$5.4bn**")),
        ],
        relation_to_headline="outside_not_addable",
        combining_rule=faq_excerpt("**Legacy financing charges stay separate.**", "their windows."),
        memo=(f"{FAQ} § 2; infra/immigration-fiscal/legacy_comparators_2026_09_30/RESULT.md; "
              "infra/immigration-fiscal/pension_legacy_2026_09_30/RESULT.md; "
              f"decisions/2026-09-30-legacy-comparisons-separate.md; {LADDER} entries 278–279"),
        population=("the 42.75M lineage on the account's headcount path, the added descendants on the third-plus "
                    "generation's path from 2005"),
        comparator="as many third-plus non-Hispanic whites on matched keys, every group's income taxes on the case's keys",
        horizon=("the 2024 financing charge of federal gaps 2005–2023 carried as if borrowed; public-employee pensions on "
                 "a 1980–2023 service-year kernel"),
        evidence_level="[MODEL OUTPUT; FRAMING-SENSITIVE]",
    ),
    dict(
        id="e5_generation_split_of_the_main_case", faq_entry=5,
        objection="The classic result is a costly first generation and a contributing second.",
        finding=("On the main case itself, with no reference group, every generation alive in 2024 is a net cost at all "
                 "64 specifications. Counted with their children, as the National Academies count them, a "
                 "second-generation adult costs other residents $12.3–13.5k a year, against $16.0–18.6k per Mexico-born "
                 "adult and $11.3–14.7k per third-plus adult; the second generation's total is $109–121bn and the "
                 "third-plus's $111–144bn. So the second generation costs less than the first and is still a net cost in "
                 "this year's account; whether today's children pay more as adults needs a cohort account, which a "
                 "one-year split cannot give. Counted in their own generation, children push the second generation's "
                 "total "
                 "to $150–178bn, above the first's $87–97bn. Per-person figures divide by the lineage's count, 29.27M "
                 "adults of 42.75M members, and the third-plus includes the 3.04M descendants who no longer report "
                 "Mexican origin."),
        values=[
            val("per second-generation adult, children counted with their parents", "12.3-13.5",
                at(FAQ, "a second-generation adult costs other residents $12.3–13.5k"), unit="$k/adult/year"),
            val("per Mexico-born adult / per third-plus adult", "16.0-18.6 / 11.3-14.7",
                at(FAQ, "a second-generation adult costs other residents $12.3–13.5k", through="$11.3–14.7k per third-plus"),
                unit="$k/adult/year"),
            val("totals: second generation / third-plus", "109-121 / 111-144",
                at(FAQ, "$11.3–14.7k per third-plus adult", through="the third-plus's $111–144bn")),
            val("children counted in their own generation: second generation / Mexico-born", "150-178 / 87-97",
                at(FAQ, "second generation's total to $150–178bn, above the first's $87–97bn")),
            val("adults / members of the lineage (the per-person denominators)", "29.27M of 42.75M",
                at(FAQ, "(29.27M adults of 42.75M members)"), unit="people"),
        ],
        relation_to_headline="inside_headline",
        combining_rule=faq_excerpt(*LATER_CORRECTIONS),
        memo=("research/immigration-adopted-account-by-generation-2026-09-25.md; "
              "infra/immigration-fiscal/generation_account_2026_09_24/derived/generation_results_oct07.csv; "
              f"{FAQ} § 5; {LADDER} entry 224"),
        population=("the 42.75M lineage by generation: Mexico-born, second generation, and third-plus with the 3.04M "
                    "added descendants"),
        comparator="no reference group; the change for all other US residents",
        horizon="annual, income-year 2024; one year's split, not a cohort account",
        evidence_level="[CALCULATION: the main case split by generation, 64 specifications]",
    ),
    dict(
        id="e18_unusual_year_budget_replay", faq_entry=18,
        objection=("One year of a price surge, pandemic programmes and a migration wave could make any group look "
                   "expensive."),
        finding=("Of the three, only the budget moves the figure, and by a tenth to a fifth. Inflation raises the "
                 "group's taxes and the cost of its services together: the $389–461bn is 1.3–1.6% of GDP, or "
                 "$317–376bn in 2019 dollars. Pandemic programmes had ended by 2024: per resident in real terms, 2021's "
                 "refundable credits were 4.4 times their 2024 level and SNAP 1.8 times. The surge barely touches this "
                 "group: Mexico-born residents who arrived from 2016 through March 2025 are 2.4M of the 40.9M and cost "
                 "others about 28% as much per person as the Mexico-born average. The budget is the real 2024 effect: "
                 "from 2019 to 2024 real government spending per resident rose 13.6% and receipts 9.7%, and 2024 "
                 "spending ran 26% above receipts. Replayed through the average budget of 2015–2019 and 2022–2023, the "
                 "main case costs 10% less per member with its lower relative income of those years ($351–415bn at "
                 "today's size), or 18–20% less with its 2024 income held fixed ($312–377bn)."),
        values=[
            val("the main case as a share of GDP; in 2019 dollars (CPI-U)", "1.3-1.6%; 317-376",
                at(FAQ, "**Prices.** Inflation raises the group's taxes", through="1.3–1.6% of GDP"),
                unit="share of GDP; $bn/year"),
            val("per resident, real: refundable credits / SNAP, 2021 relative to 2024; 2019", "4.4 / 1.8; 0.86 / 0.70",
                at(FAQ, "**Pandemic programmes.** They had ended by 2024", through="in 2019 they were 0.86 and 0.70"),
                unit="ratio to 2024"),
            val("arrivals of 2016 through March 2025: people of the 40.9M; cost per person relative to the Mexico-born "
                "average (partial account, flat charges, taxes as the survey reports them)", "2.4M of 40.9M; 28%",
                at(FAQ, "**The surge.** It barely touches this group", through="about 28% as much"),
                unit="people; share"),
            val("2019 to 2024, real per resident: spending / receipts; 2024 spending over receipts", "13.6% / 9.7%; 26%",
                at(FAQ, "**The budget.** This is the real 2024 effect", through="2024 spending ran 26% above receipts"),
                unit="percent"),
            val("main case replayed through the average budget of 2015–2019 and 2022–2023: with those years' income / "
                "with 2024 income held fixed", "10% less, 351-415 / 18-20% less, 312-377",
                at(FAQ, "Replayed through the average budget of 2015–2019", through="its 2024 income held fixed ($312–377bn)")),
        ],
        relation_to_headline="overlaps_headline",
        combining_rule=("The replays are the same account run through other years' budgets: they sit beside the "
                        "headline and are never added to it."),
        memo=(f"{FAQ} § 18; {BACKCAST}; infra/immigration-fiscal/cycle_average_2026_10_07/RESULT.md (ladder 290); "
              "infra/immigration-fiscal/historical_backcast_2026_09_20/derived/oct07/backcast_annual.csv; "
              f"{ARRIVAL}; infra/immigration-fiscal/migrant_shelter_costs_2026_09_23/RESULT.md"),
        population="the 42.75M lineage; the Mexico-born by arrival window on the survey's 40.9M",
        comparator="the same account in 2024 against other years' budgets and prices",
        horizon="annual; 2024 against the average budget of 2015–2019 and 2022–2023, replayed on the back-cast",
        evidence_level="[MODEL: back-cast replay] + [DATA: national budgets and prices by year]",
    ),
    dict(
        id="e19_descendants_counted_whole", faq_entry=19,
        objection=("Grandchildren of Mexican immigrants who marry out often stop reporting Mexican origin, and they are "
                   "the ones who did best. An account of the people who still say they are Mexican drops its own "
                   "success stories, so its third generation looks worse than the lineage is."),
        finding=("Yes, they are counted, as whole people. The survey links children to the parents they live with, so "
                 "identity loss is observed: 11.2% of the third generation is not reported as Mexican. Carried through "
                 "the generations on the account's frame, that is 3.04M people beyond the 39.71M who report Mexican "
                 "birth, parentage or origin, a lineage of 42.75M, priced under the same rules at their measured ages. "
                 "Third-generation adults who no longer identify close 56% of the identifiers' college gap to "
                 "third-plus non-Hispanic whites (C3 = 0.557, SE 0.246). Together the added people add $20.0–29.2bn, "
                 "and the main case is $389.1–461.5bn. An added person costs others $6,692–9,696, less than an "
                 "identified member ($9,293–10,886), so the objection's direction holds for the cost per member, which "
                 "falls to $9,101–10,794, while the total rises. If losses stop at the "
                 "third-generation rate (1.81M added) the case is $378.0–445.3bn, if they compound (4.27M) "
                 "$400.2–477.7bn, and C3 one standard error either way gives $386.3–465.4bn."),
        values=[
            val("not reported as Mexican: share of the third generation; people added to the 39.71M",
                "11.2%; 3.04M of 42.75M", at(FAQ, "11.2% of the third generation is not reported as Mexican",
                                            through="a lineage of 42.75M"), unit="share; people"),
            val("share of the college gap that third-generation non-identifiers close (C3)", "0.557 (SE 0.246)",
                at(FAQ, "(C3 = 0.557, SE 0.246"), unit="share"),
            val("added to the main case by the 3.04M", "20.0-29.2", at(FAQ, "Together they add $20.0–29.2bn")),
            val("per member of the 42.75M lineage; an added person / an identified member", "9,101-10,794",
                at(FAQ, "Together they add $20.0–29.2bn", through="$9,101–10,794"), unit="$/member/year"),
            val("identity loss stopping (1.81M) / compounding (4.27M); C3 ± 1 SE",
                "378.0-445.3 / 400.2-477.7; 386.3-465.4",
                at(FAQ, "third-generation rate (1.81M added) the case is $378.0–445.3bn", through="$386.3–465.4bn")),
        ],
        relation_to_headline="inside_headline",
        combining_rule=faq_excerpt(*TWO_ANCHORS),
        memo=(f"{FAQ} § 19; decisions/2026-10-05-main-case-v5.md; decisions/2026-10-07-main-case-v6.md; {R07}; "
              "infra/immigration-fiscal/main_case_lineage_2026_10_05/RESULT.md; "
              f"infra/immigration-fiscal/g3_identity_pooled_2026_10_05/RESULT.md; {LADDER} entries 280, 281 and 292"),
        population=("the 3.04M descendants of Mexican immigrants who no longer report Mexican origin, inside the 42.75M "
                    "lineage"),
        comparator="no reference group; the change for all other US residents",
        horizon="annual, income-year 2024; identity loss carried through the generations on the account's frame",
        evidence_level="[CALCULATION: main case v6] + [MODEL: identity loss past the third generation]",
    ),
    dict(
        id="e19_ancestry_share_beside", faq_entry=19,
        objection="\"Do you count descendants who no longer identify as Mexican?\"",
        finding=("Each person counts once, at their own measured cost, as the account counts its members of mixed "
                 "ancestry. Counting each person by their share of Mexican-immigrant ancestry instead (½ per Mexico-born "
                 "parent, ¼ per grandparent) gives $274.9–374.8bn for the whole lineage, and that figure stays beside "
                 "the headline. The survey shows grandparents only for people who live with their parents, so 70% of "
                 "third-plus members have no grandparent data and the share is a stated bound. The two readings answer "
                 "different questions: whole people asks what the members who exist cost others; the share divides "
                 "each member's cost among the origins of their ancestors, the reading to use when accounts by origin "
                 "must add to a national total."),
        values=[
            val("the lineage counted by share of Mexican-immigrant ancestry", "274.9-374.8",
                at(FAQ, "gives $274.9–374.8bn for the whole lineage")),
            val("third-plus members with no grandparent data", "70%", at(FAQ, "so 70% of third-plus members have no grandparent"),
                unit="share"),
        ],
        relation_to_headline="different_object",
        combining_rule=None,
        memo=f"{FAQ} § 19; {R07} § Companion readings; decisions/2026-10-07-main-case-v6.md",
        population="the 42.75M lineage, each member weighted by their share of Mexican-immigrant ancestry",
        comparator="no reference group; the change for all other US residents",
        horizon="annual, income-year 2024",
        evidence_level="[CALCULATION] / [FRAMING-SENSITIVE]",
    ),
    dict(
        id="e20_closed_budget_reading", faq_entry=20,
        objection=("In fiscal 2024 federal outlays were $6.74tn against receipts of $4.92tn, 37% more. Nearly every "
                   "resident, native or not, receives more than they pay on that budget, and the gap will eventually "
                   "be closed by higher taxes or lower spending. People who join the population share that fix. So an "
                   "account that charges the group's whole share of the deficit to everyone else overstates what "
                   "others pay."),
        finding=("The headline is current law, and current law schedules no rule that closes the budget, so it counts "
                 "the group's share of the deficit as a cost to other residents; that assumption is stated beside the "
                 "headline. If a permanent fix closed the federal budget and the lineage paid its share, other "
                 "residents would pay $357.1–429.5bn a year instead of $389.1–461.5bn, 7–8% less. The fix is $332.9bn a "
                 "year, Auerbach and Gale's 2.33% of GDP less the 1.19 points that would pay scheduled retirement "
                 "benefits after the OASI trust fund runs out late in 2032; the lineage carries $32.0bn of it, 9.61%, "
                 "its share of households. Across current-law gaps and six sharing rules the cost is $346.7–451.4bn. "
                 "Most of the group's cost falls on state and local budgets, which balance every year, so no federal "
                 "fix shares it."),
        values=[
            val("cost to other residents if a permanent fix closed the federal budget and the lineage paid its share",
                "357.1-429.5", at(FAQ, "**$357.1–429.5bn** a year instead of $389.1–461.5bn")),
            val("the fix: Auerbach and Gale's gap less the part that pays scheduled retirement benefits",
                "332.9 = 2.33% - 1.19 points", at(FAQ, "The fix is $332.9bn a year", through="the 1.19 points"),
                unit="$bn/year; share of GDP"),
            val("the lineage's part of the fix: its share of households (of residents)", "32.0; 9.61% (12.74%)",
                at(FAQ, "The lineage carries $32.0bn of it, 9.61%", through="It is 12.74% of residents"),
                unit="$bn/year; share"),
            val("across current-law gaps and six sharing rules", "346.7-451.4",
                at(FAQ, "the cost is $346.7–451.4bn")),
            val("current-policy gaps, low end; AEI's 2013 figure with scheduled benefits paid", "278.3; 231.2-303.6",
                at(FAQ, "On current-policy gaps it reaches $278.3bn", through="$231.2–303.6bn")),
        ],
        relation_to_headline="overlaps_headline",
        combining_rule=faq_excerpt("The current-law figure stays the headline.", "other entries' ranges."),
        memo=(f"{FAQ} § 20; infra/immigration-fiscal/closed_budget_2026_10_06/RESULT.md; Auerbach & Gale, An Update on "
              "the Federal Budget Outlook (March 2026); 2026 Social Security and Medicare Trustees Reports"),
        population="the 42.75M lineage",
        comparator="other residents, if a permanent fix closed the federal budget and the lineage paid its share",
        horizon="annual 2024, with a thirty-year federal fix shared by a stated rule",
        evidence_level="[CALCULATION: closed-budget lane] / [FRAMING-SENSITIVE]",
    ),
    dict(
        id="e21_long_run_channels_at_zero", faq_entry=21,
        objection=("The account prices 2024 with the economy, its technology and its institutions as they are. Costs "
                   "that build over decades would not show: firms that kept low-wage labor instead of investing in "
                   "machines, neighborhoods that separated, and norms that shape productivity changing slowly. If "
                   "those are large, the true cost is above the headline."),
        finding=("Each channel has evidence of a mechanism, and none has a measured national dollar figure, so the "
                 "account carries them at zero and says so. Low-skill immigration moves firms away from machines: in "
                 "Lewis (2011), a rise of 0.1 in a metro's ratio of dropouts to high-school graduates lowers machinery "
                 "per worker by about 6% (IV −0.59, SE 0.31), while output per worker does not measurably change "
                 "(−0.03, SE 0.24); when the bracero program ended in 1964, crops that had used more braceros saw more "
                 "patents for 15–20 years. Counties with a larger Hispanic share have fewer cross-class friendships at "
                 "equal income, poverty and schooling, and a larger low-skill immigrant share raises the Republican "
                 "vote, but no study turns these into a dollar figure. The budget's legacy is measured, beside the "
                 "headline: $101.6–101.7bn a year in interest-equivalent against as many third-plus whites. A zero here "
                 "means the effect is not measured."),
        values=[
            val("the budget's legacy: 2005–2023 federal gaps carried as if borrowed, against as many third-plus whites",
                "101.6-101.7", at(FAQ, "$101.6–101.7bn a year in interest-equivalent")),
            val("machinery per worker after a 0.1 rise in the dropout-to-graduate ratio (Lewis 2011)",
                "about -6% (IV -0.59, SE 0.31)", at(FAQ, "ratio of dropouts to high-school graduates lowers machinery"),
                unit="percent"),
            val("output per worker, same design", "-0.03 (SE 0.24)", at(FAQ, "output per worker does not measurably change"),
                unit="coefficient"),
            val("more patents after the bracero program ended, in crops that had used more braceros", "15-20 years",
                at(FAQ, "had used more braceros saw more patents for 15–20 years"), unit="years"),
        ],
        relation_to_headline="outside_not_addable",
        combining_rule=faq_excerpt("**Legacy financing charges stay separate.**",
                                   "fiscal or fiscal-plus-social total."),
        memo=(f"{FAQ} § 21; infra/immigration-fiscal/automation_channel_2026_09_16/; "
              "infra/immigration-fiscal/connectedness_fragmentation_2026_09_28/RESULT.md; "
              f"infra/immigration-fiscal/legacy_comparators_2026_09_30/RESULT.md; {LADDER} entries 99, 102, 120, 154, "
              "199, 262 and 278"),
        population="the 42.75M lineage; the channels' studies cover metros, counties and crops",
        comparator="the account, which carries each channel at zero",
        horizon="decades; the legacy row is the 2024 charge on 2005–2023 gaps",
        evidence_level="[SOURCE: studies as cited] + [INFERENCE]; [FRAMING-SENSITIVE]",
    ),
]

RULES = {
    "cr_two_anchors": faq_rule("**The two anchors are different objects.**"),
    "cr_offsets_do_not_add": faq_rule("**Offsets do not add unless an entry says so.**"),
    "cr_fiscal_plus_social_own_object": faq_rule("**The fiscal-plus-social total is its own object.**"),
    "cr_match_population_horizon_outcome": faq_rule("**A result refutes a claim only when population, horizon"),
    "cr_legacy_financing_separate": faq_rule("**Legacy financing charges stay separate.**"),
    "cr_faq_preamble_routed": faq_rule("Date: 2026-09-21. [ROUTING", drop_prefix="Date: 2026-09-21. "),
    "cr_instrument_ranking_warning": faq_rule("A summary that", phrase="A summary that ranks"),
    "cr_california_texas_shared_ledger": faq_rule("**California and Texas per-person gaps are the shared"),
}
NEW_RULES = {"cr_fiscal_plus_social_own_object", "cr_legacy_financing_separate"}

# Cards kept as committed whose rule is the FAQ's bold opening: carry its span, for the token check.
MATCH_SPAN = faq_rule("**A result refutes a claim only when population, horizon")[1]


def window_numbers(ref):
    """Numbers printed within two lines of a citation, as build_context.confirmed() reads them."""
    match = re.match(r"(.+?):(\d+)((?:\s*[-,]\s*\d+)*)", str(ref or ""))
    if not match or not (ra.ROOT/match.group(1)).is_file():
        return []
    cited = [int(match.group(2))]+[int(n) for n in re.findall(r"\d+", match.group(3))]
    lines = ra.new_lines(match.group(1))
    window = " ".join(lines[max(0, min(cited)-3):max(cited)+2])
    if match.group(1).endswith(".csv"):
        # A row reads with its header (`ci95_low` names the interval a label calls 95%).
        window = (lines[0]+" "+window).replace(",", " ")
    return [float(n) for n in bc.numbers(window)]


def objection_numbers(text):
    """Numbers of the FAQ paragraphs that hold the objection's sentences (a card quotes its entry's heading or
    steel-man), and the sentences no FAQ paragraph holds."""
    norm = lambda s: " ".join(s.replace("*", "").split()).lower()
    paras = [norm(p[2]) for p in paragraphs(FAQ)]
    pool, missing = [], []
    for sentence in re.split(r"(?<=[.?!])\s+", text.strip().strip('"')):
        hits = [p for p in paras if norm(sentence).rstrip('.?!"') in p]
        if not hits:
            missing.append(sentence)
        pool += [float(n) for p in hits for n in bc.numbers(p)]
    return pool, missing


def token_matches(token, pool):
    """A printed token equals a pooled number at the token's own precision, in the same units or after the
    thousands, millions or billions a page abbreviates ($267k against 266,917)."""
    places = len(token.split(".")[1]) if "." in token else 0
    wanted = float(token)
    return any(abs(round(x/scale, places)-wanted) < 0.5*10**-places+1e-12
               for x in pool for scale in (1, 1e3, 1e6, 1e9))


def unmatched_tokens(item, rule_spans):
    pool = []
    for v in item["values"]:
        pool += [float(n) for n in bc.numbers(repr(abs(v["value"])) if isinstance(v["value"], (int, float))
                                              else v["value"])]
        pool += window_numbers(v["file_line"])
    if item["id"] in rule_spans:
        pool += window_numbers(rule_spans[item["id"]])
    out = []
    if item.get("objection"):
        quoted, missing = objection_numbers(item["objection"])
        out += [f"{item['id']} [objection sentence the FAQ does not hold]: {s}" for s in missing]
        out += [f"{item['id']} [objection]: {token}" for token in bc.numbers(item["objection"])
                if not token_matches(token, pool+quoted)]
    texts = [("finding", item.get("finding")), ("combining_rule", item.get("combining_rule"))]
    texts += [(f"label {i+1}", v["label"]) for i, v in enumerate(item["values"])]
    texts += [(f"unit {i+1}", v.get("unit")) for i, v in enumerate(item["values"])]
    return out+[f"{item['id']} [{where}]: {token}" for where, text in texts if text
                for token in bc.numbers(text) if not token_matches(token, pool)]


def main():
    ctx = json.loads(ra.subprocess.run(["git", "-C", str(ra.ROOT), "show", f"{BASE}:infra/immigration-fiscal/"
                                        "assumption_explorer_2026_09_21/context.json"],
                                       capture_output=True, text=True, check=True).stdout)
    by_id = {item["id"]: item for item in ctx["items"]}
    unknown = (set(EDITS) | set(DROP))-set(by_id)
    if unknown:
        raise ValueError(f"Edits or drops name cards that do not exist: {sorted(unknown)}")
    if set(EDITS) & set(DROP):
        raise ValueError(f"Cards both edited and dropped: {sorted(set(EDITS) & set(DROP))}")
    clash = {card["id"] for card in NEW} & set(by_id)
    if clash:
        raise ValueError(f"New card ids already exist: {sorted(clash)}")
    log, items, rule_spans = [], [], {}
    for item in ctx["items"]:
        if item["id"] in DROP:
            log.append(f"dropped {item['id']}: {DROP[item['id']]}")
            continue
        edit = EDITS.get(item["id"], {})
        card = json.loads(json.dumps(item))
        for key, value in edit.items():
            if key == "combining_rule" and isinstance(value, tuple):
                card[key], rule_spans[item["id"]] = value[0], f"{FAQ}:{value[1]}"
            elif key != "value_edits":
                card[key] = value
        recited = set()
        for index, fields in edit.get("value_edits", {}).items():
            card["values"][index].update(fields)
            if "file_line" in fields:
                recited.add(index)
                log.append(f"re-cited {item['id']} value {index+1}: {fields['file_line']}")
        if "values" not in edit:
            # Kept values: re-anchor from BASE; a blind shift is not trusted to land on the same quantity.
            for index, v in enumerate(card["values"]):
                if index in recited:
                    continue
                new, how = ra.reanchor(v["value"], v["file_line"], BASE)
                if new is None or how.startswith("shifted"):
                    UNRESOLVED.append(f"kept card {item['id']}: {v['value']!r} @ {v['file_line']} ({how})")
                    continue
                if new != v["file_line"]:
                    log.append(f"re-anchored ({how}) {item['id']}: {v['file_line']} -> {new}")
                    v["file_line"] = new
        if card.get("combining_rule") == MATCH:
            rule_spans[item["id"]] = f"{FAQ}:{MATCH_SPAN}"
        log.append(f"{'rewritten' if edit else 'kept'} {item['id']}"+(f" ({', '.join(sorted(edit))})" if edit else ""))
        items.append(card)
    for new in NEW:
        card = dict(new)
        if isinstance(card.get("combining_rule"), tuple):
            card["combining_rule"], rule_spans[card["id"]] = card["combining_rule"][0], f"{FAQ}:{card['combining_rule'][1]}"
        log.append(f"added {card['id']}")
        items.append(card)
    rules = []
    for rid, (text, span) in RULES.items():
        rules.append(dict(id=rid, text=text, file_line=f"{FAQ}:{span}"))
        if rid in NEW_RULES:
            log.append(f"added combining rule {rid}")
    old_rules = [r["id"] for r in ctx["combining_rules"]]
    if set(old_rules)-set(RULES):
        raise ValueError(f"combining rules lost: {sorted(set(old_rules)-set(RULES))}")
    inv = dict(items=items, combining_rules=rules)
    # Every value must verify, no card may carry more than five, and every printed number must trace.
    failed = [f"{i['id']}: {v['value']!r} @ {v['file_line']} ({v['label']})" for i in inv["items"] for v in i["values"]
              if not bc.confirmed(v["value"], v["file_line"])]
    too_many = [i["id"] for i in inv["items"] if len(i["values"]) > 5]
    tokens = [t for i in inv["items"] for t in unmatched_tokens(i, rule_spans)]
    if UNRESOLVED or failed or too_many or tokens:
        raise SystemExit("NOT WRITTEN.\nUnresolved anchors:\n  "+"\n  ".join(UNRESOLVED)+"\nUnverified values:\n  "
                         +"\n  ".join(failed)+f"\nmore than five values: {too_many}"
                         "\nNumber tokens that match no value or cited line:\n  "+"\n  ".join(tokens))
    OUT.write_text(json.dumps(inv, indent=1, ensure_ascii=False)+"\n")
    print("\n".join(log))
    print(f"number tokens checked: every token in objections, findings, rules and value labels matches ({len(items)} cards)")
    print(f"wrote {OUT}: {len(items)} cards, {sum(len(i['values']) for i in items)} values, all verify; "
          f"{len(rules)} combining rules")


if __name__ == "__main__":
    main()
