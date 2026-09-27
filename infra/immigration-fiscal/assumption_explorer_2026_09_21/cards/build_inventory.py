"""Write _cache/inventory_2026_09_26.json: context.json as committed at ba12f3c, citations re-anchored to the
files as they stand, the cards that quote the September 24 case moved to the September 26 case (the first-year
budget response since schools were charged at full cost the same evening; named "one-year scenario" until
2026-09-27; the explorer does not run that main case),
and the combining rules re-read from the FAQ by their opening words. Every value must verify with
build_context.confirmed() before the file is written.

Usage: build_inventory.py   (base: ba12f3c, the last change to context.json before this pass)
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import reanchor as ra  # noqa: E402

bc = ra.bc
BASE = "ba12f3c"
EDITS_BASE = "199582e"  # HEAD when the edits below were written (2026-09-26 22:52); their lines cite its files
FAQ = "research/immigration-objections-faq-2026-09-21.md"
R26 = "infra/immigration-fiscal/main_case_2026_09_26/RESULT.md"
R24 = "infra/immigration-fiscal/main_case_2026_09_24/RESULT.md"
R23 = "infra/immigration-fiscal/main_case_2026_09_23/RESULT.md"
CAA = "research/immigration-complete-annual-account-2026-09-20.md"
LADDER = "research/immigration-confidence-ladder.md"
OUT = ra.LANE/"_cache"/"inventory_2026_09_26.json"

ANCHOR_RULE = ("The $201–246bn is the complete account's change for all other residents in the September 26 case, the "
               "first-year budget response this page runs (the same at rounding on September 24; $203–250bn on September 23; "
               "$165–197bn as published September 20), under a stated service-response assumption, with no reference "
               "group.")


def val(label, value, file_line, unit="$bn/year", se=None):
    return dict(label=label, value=value, unit=unit, se=se, file_line=file_line)


EDITS = {
    "headline_cbo_informed_net_cost": dict(
        finding=("The explorer runs the September 26 case, now the first-year budget response; the adopted main case charges "
                 "schools at their full average cost ($258–292bn) and is not yet in the explorer. "
                 "In the September 26 case the complete account gives $200.9–245.7bn a year of conditional "
                 "net cost to other US residents. It moved from the September 24 case ($200.9–246.3bn) by two corrections "
                 "that nearly cancel. Removing a group that is 12% of residents and 17.5% of pupils saves more than the "
                 "marginal elasticities imply, so general government responds at 0.60–0.85 and schools at 65–68% of "
                 "average cost (+$4.1 / +$3.4bn). The consumption key, corrected for saving and remittances, gives the "
                 "group a larger share of consumption taxes (−$4.1bn). The September 24 case had built the dataset audit, "
                 "the pooled-MEPS medical figure with long-term care by use, care and household services, shelter keying "
                 "and the four outside checks into the case adopted September 23 ($203.2–249.6bn), which charges justice "
                 "and uncompensated hospital care by use. The group's taxes had been overstated (+$48.7 / +$50.3bn) and "
                 "so had its keyed spending (−$51.0 / −$53.6bn). As published September 20, with general government "
                 "fixed and justice charged per head, it was $165.1–197.4bn. Defense, interest on existing debt and "
                 "business subsidies stay at zero response."),
        values=[
            val("September 26 case, the first-year budget response", "200.9-245.7", f"{R26}:2"),
            val("September 26 case, non-school education budgets also fixed / every service proportional",
                "156.5-210.8 / 301.3-334.8", f"{R26}:93-94"),
            val("what the two corrections of September 26 moved: finite-removal responses (low / high end) / consumption key",
                "+4.09 / +3.43; -4.05", f"{R26}:7-9"),
            val("main case adopted September 24 / September 23", "200.9-246.3 / 203.2-249.6", f"{R24}:2-3"),
            val("main CBO-informed comparison as published September 20", "165.1-197.4", f"{CAA}:155"),
        ],
        combining_rule=ANCHOR_RULE[:-1]+"; it carries later corrections that were not propagated to the ledger (ladder "
                       "161). Since September 25 it has its own generation split, computed on the account with no "
                       "reference group (ladder 224).",
        memo=(f"decisions/2026-09-26-main-case-schools-full-cost.md; {R26}; "
              f"decisions/2026-09-26-main-case-finite-removal-and-consumption-key.md; {R24}; "
              f"decisions/2026-09-24-main-case-audit-and-outside-checks.md; {R23}; "
              f"{CAA} § Executed category-specific service responses"),
    ),
    "e2_fixed_functions_and_cbo_inputs": dict(
        finding=("The headline holds defense, existing interest and business subsidies fixed at zero response. That is an "
                 "assumption, not a CBO estimate. What comes from CBO is the tax-incidence rule set (corporate tax 75% to "
                 "capital income, 25% to wages) and the 63–66% school-spending response derived from CBO's enrollment "
                 "coefficients, with economic-affairs and recreation budgets held fixed. General public services were "
                 "also held at zero until September 23, when the main case let them grow at 0.59–0.84 of the population; "
                 "that adds $27.8–39.5bn on the corrected data of September 24 ($28.5–40.6bn before the corrections). "
                 "That range is the cross-state scale of administration spending (0.842, SE 0.039, for state "
                 "administration); the only within-state test gave 0.47 with a 95% interval of −0.72 to 1.66, which "
                 "cannot tell zero from one. The September 26 case treats both as elasticities and applies "
                 "them to the removal of a whole group, 17.5% of pupils and 12% of residents, which saves more than the "
                 "marginal rate: schools respond at 65–68% and general government at 0.60–0.85."),
        values=[
            val("general government response in the main case: the elasticity (September 23 and 24) / the finite-removal "
                "response (adopted September 26)", "0.59-0.84 / 0.6000-0.8504", f"{R26}:46-47",
                unit="share of proportional growth"),
            val("added to the main case by the elasticity response, on the corrected data of September 24 (was: September "
                "23 data)", "27.8-39.5 (was 28.5-40.6)", f"{FAQ}:74-75"),
            val("corporate tax incidence to capital income / wages (CBO's rules)", "75% / 25%", f"{FAQ}:71", unit="share"),
            val("school-spending response: from CBO's coefficients to first order (September 20 to 24) → as a finite "
                "removal (September 26 case)", "0.63 / 0.66 → 0.6522 / 0.6813", f"{R26}:48-49", unit="share"),
            val("CBO enrollment-growth coefficients (+1pp enrollment → per-pupil spending growth)",
                "-0.37 (growth side), -0.34 (decline side)", f"{CAA}:163-164", unit="points"),
        ],
        combining_rule=ANCHOR_RULE,
        memo=(f"{FAQ} § 2; {CAA} § Where the coefficients come from; {R23}; {R26} § The responses; "
              "infra/immigration-fiscal/finite_response_2026_09_26/RESULT.md"),
    ),
    "e2_fixed_service_range_and_breakeven": dict(
        finding=("The sign still turns on ordinary service budgets. In the September 26 case, break-even "
                 "needs 5.8–17.0% of assigned service costs to be incremental, against 4.8–16.0% on September 24 and "
                 "5.5–16.4% on September 23: the consumption key adds $4.05bn to the group's taxes, and with services "
                 "frozen nothing offsets it. With all of them fixed and general government at its adopted response, the "
                 "result runs from −$21.6bn to +$81.5bn on CBO's incidence rules (September 24: −$25.3bn to +$77.8bn; "
                 "September 23: −$22.3bn to +$80.5bn on those rules and −$87.8bn to +$80.5bn across every incidence "
                 "rule; the corrected cases are not recomputed across rules). As published September 20, with general "
                 "government fixed as well, the figures were −$41.5bn to +$112.7bn and 18.5–25.8%."),
        values=[
            val("break-even incremental share, personal / shared allocation, September 26 case (was: September 24)",
                "5.8-13.9% / 8.8-17.0% (was 4.8-12.9% / 7.8-16.0%)", f"{R26}:104-105",
                unit="share of assigned service costs"),
            val("ordinary service budgets fixed, private capital fixed, CBO's incidence rules, September 26 (was: "
                "September 24)", "-21.6 to +81.5 (was -25.3 to +77.8)", f"{R26}:106", unit="$bn/year net outside effect"),
            val("same across every incidence rule, September 23 (not recomputed on the corrected cases)", "-87.8 to +80.5",
                f"{R23}:70", unit="$bn/year net outside effect"),
            val("ordinary service budget fixed, private capital fixed (published September 20)", "-41.53 to +112.67",
                f"{CAA}:282", unit="$bn/year net outside effect"),
            val("break-even incremental share, personal / shared (published September 20)", "18.5-22.7% / 21.5-25.8%",
                f"{CAA}:292-293", unit="share of assigned service costs"),
        ],
        memo=(f"{R26} § Sign reversal; {R24} § Sign reversal on the new case; {R23} § Sign reversal under the adopted "
              f"case; {CAA} § What can reverse the sign?"),
    ),
    "e2_general_public_services_sensitivity": dict(
        finding=("Making general public services 10%, 25%, 50% or 100% responsive adds $4.8bn, $12.1bn, $24.2bn or "
                 "$48.3bn on the September 20 data. The main case adopted September 23 set the response at 0.59–0.84, "
                 "which added $28.5–40.6bn then; the case adopted September 24 kept that response, which adds "
                 "$27.8–39.5bn on its corrected data. Since September 26 the response is 0.60–0.85, the share of average "
                 "cost that removing a group of 12% of residents saves; with audit row 8's constant scaled to match, that adds "
                 "$0.37–0.39bn to the September 24 case."),
        memo=("research/immigration-education-administration-scope-2026-09-20.md § Isolated arithmetic sensitivity; "
              f"{R23}; {R26} (finite-removal response); decisions/2026-09-26-main-case-finite-removal-and-consumption-key.md"),
    ),
    "e2_per_capita_three_functions": dict(combining_rule=ANCHOR_RULE),
    "e6_gap_against_average_resident": dict(combining_rule=ANCHOR_RULE),
    "e4_offset_threshold_is_conditional": dict(
        finding=("Omitted benefits would have to reach $201–246bn a year to offset the September 26 case "
                 "(the same at rounding on September 24; $203–250bn on September 23; $165–197bn as published September "
                 "20). That threshold is conditional on the service-response share, which is assumed and unmeasured: it "
                 "is $157–211bn if non-school education budgets are also held fixed, and it reaches zero where 5.8–17.0% "
                 "of assigned service costs are incremental, so the response share moves the result more than any offset "
                 "listed here."),
        values=[
            val("offset hurdle, September 26 case", "200.9-245.7", f"{R26}:2"),
            val("same, non-school education also fixed (was: September 24)", "156.5-210.8 (was 157.1-210.8)", f"{R26}:93"),
            val("break-even incremental share of assigned service costs (was: September 24)", "5.8-17.0% (was 4.8-16.0%)",
                f"{R26}:104-105", unit="share"),
            val("offset hurdle, main case adopted September 24 / September 23", "200.9-246.3 / 203.2-249.6", f"{R24}:2-3"),
            val("as published September 20: main case; non-school education also fixed", "165.1-197.4; 120.8-160.3",
                f"{R23}:5,14"),
        ],
        memo=f"{FAQ} § 4; {R26}; {R24}; {R23}",
    ),
    "e11_not_a_policy_saving": dict(
        values=[
            val("the number the objection misuses (September 26 case)", "200.9-245.7", f"{R26}:2"),
            val("the same figure on September 24", "200.9-246.3", f"{R24}:2"),
            val("on September 23 / as published September 20", "203.2-249.6 / 165.1-197.4", f"{R23}:4-5"),
            val("US-born share: second generation + third-plus of the 40.897m total", "14.333m + 14.343m of 40.897m",
                "research/immigration-yearly-lifetime-cost-repair-2026-09-19.md:24-26", unit="people"),
        ],
        combining_rule=ANCHOR_RULE,
    ),
    "e16_cbo_surge_projection": dict(
        finding=None,  # filled below from the current text, one clause replaced
        values=None,
        memo=None,
    ),
    "e17_survey_errors_nearly_cancel": dict(
        finding=("The survey errors are real and large, but they run both ways and nearly cancel. The group's taxes were "
                 "overstated: the survey's tax model treats every respondent as a compliant resident filer, and Census's "
                 "fill-ins keep only 9% of the group's own wage gap. Correcting them adds $48.7–50.3bn of cost. Fixing "
                 "spending keys, with care moved into the account, removes $51.0–53.6bn. On September 24 the main case "
                 "moved from $203.2–249.6bn to $200.9–246.3bn. Two corrections adopted September 26 also nearly cancel: "
                 "removing a whole group saves more than the marginal elasticities (+$4.1 / +$3.4bn), and the "
                 "consumption key had given the group too small a share of consumption taxes, because richer residents "
                 "save more (−$4.1bn); CBO's excise distribution, ITEP's gradient and CE's Mexican-origin units support "
                 "that direction. The September 26 case is $200.9–245.7bn, and every correction at its extreme in one direction spans "
                 "$164–277bn without a sign change. Administrative records show no fear-driven benefit under-reporting "
                 "where the group's dollars are: California's SNAP records give Hispanic participants 44.0% of benefit "
                 "dollars against the survey's 44.1%. The count error runs the other way: the CPS puts the Mexico-born "
                 "9–13% above the ACS, and the adopted case corrects to the ACS level."),
        values=[
            val("cost added by correcting the group's overstated taxes / charge removed by fixing spending keys (with "
                "care), September 24", "+48.7 / +50.3; -51.0 / -53.6", f"{LADDER}:369", unit="$bn/year (low / high end)"),
            val("main case before the corrections, after those of September 24, after those of September 26",
                "203.2-249.6 -> 200.9-246.3 -> 200.9-245.7", f"{FAQ}:436-439"),
            val("every correction at its extreme in one direction, September 26 (was: September 24)",
                "164-277 (was 172-276)", f"{R26}:12"),
            val("Hispanic share of California SNAP benefit dollars: administrative records / CPS", "44.0% / 44.1%",
                f"{LADDER}:365", unit="share of dollars"),
            val("CPS Mexico-born count above the ACS since 2019; early-2025 level, CPS / ACS-based", "9-13%; 12.2M / 11.1M",
                f"{LADDER}:349", unit="percent; persons"),
        ],
        memo=(f"{FAQ} § 17; {R26}; {R24}; research/immigration-outside-checks-2026-09-24.md; "
              f"{LADDER} entries 204, 208–210, 216–217, 219, 225, 227 and 229"),
    ),
    "complete_account_assigned_balance": dict(
        finding=("On the September 20 keys, default receipt and preferred service keys give an assigned balance of "
                 "−$478.76bn shared / −$500.82bn personal; zeroing defense, general government and old domestic interest "
                 "leaves −$193.15bn / −$215.21bn. The use keys adopted September 23 add $5.94bn of public order and "
                 "safety and $3.65–5.75bn of uncompensated care to the group's assigned spending. The data corrections "
                 "adopted September 24 lowered the group's receipts on the shared allocation to $488.5bn, from $545.1bn, "
                 "and lowered its keyed spending as well; the consumption key adopted September 26 raises those receipts "
                 "to $492.5bn."),
        values=None,  # the first three kept; the fourth replaced below
        memo=None,
    ),
    "generation_ledger_later_annual_refreshes": dict(
        combining_rule=("The complete account ($201–246bn in the September 26 case, the same at rounding on "
                        "September 24; $203–250bn on September 23; $165–197bn as published September 20) carries later "
                        "corrections that were never carried back into the generation ledger (ladder 161). Since "
                        "September 25 it has its own generation split, computed with no reference group (ladder 224); the "
                        "ledger's generation gaps must not be scaled onto it."),
    ),
    "e4_care_channels_add": dict(values=None),  # one label only, below
}


def faq_rule(opening, phrase=None, drop_prefix=""):
    """The FAQ text from the one line holding `opening` to the end of its paragraph, as (text, "first-last").
    Found by its words, so the rule survives lines added above it. `phrase` starts the text at that phrase
    (it may wrap across lines); `drop_prefix` removes a leading prefix."""
    lines = ra.new_lines(FAQ)
    hits = [i for i, line in enumerate(lines) if opening in line]
    if len(hits) != 1:
        raise ValueError(f"FAQ has {len(hits)} lines holding {opening!r}")
    start = end = hits[0]
    while end+1 < len(lines) and lines[end+1].strip():
        end += 1
    text = " ".join(line.strip() for line in lines[start:end+1])
    if phrase:
        if phrase not in text:
            raise ValueError(f"FAQ paragraph at {start+1} lost {phrase!r}")
        text = phrase+text.split(phrase, 1)[1]
    if drop_prefix:
        if not text.startswith(drop_prefix):
            raise ValueError(f"FAQ {start+1}-{end+1} no longer starts with {drop_prefix!r}")
        text = text[len(drop_prefix):]
    return text, f"{start+1}-{end+1}"


def main():
    # Start from the cards as committed at BASE, so reruns give the same inventory whatever HEAD holds (HEAD's
    # context.json is this script's own output since b84629e).
    ctx = json.loads(ra.subprocess.run(["git", "-C", str(ra.ROOT), "show", f"{BASE}:infra/immigration-fiscal/"
                                        "assumption_explorer_2026_09_21/context.json"],
                                       capture_output=True, text=True, check=True).stdout)
    inv = json.loads(json.dumps(ctx))
    log = []
    by_id = {item["id"]: item for item in inv["items"]}
    missing = set(EDITS)-set(by_id)
    if missing:
        raise ValueError(f"Edits name cards that do not exist: {sorted(missing)}")
    # 1. Re-anchor every citation that no longer verifies.
    for item in inv["items"]:
        for v in item["values"]:
            new, how = ra.reanchor(v["value"], v["file_line"], BASE)
            if new is None:
                raise ValueError(f"Unresolved citation {item['id']}: {v['value']!r} @ {v['file_line']} ({how})")
            if new != v["file_line"]:
                log.append(f"re-anchored ({how}) {item['id']}: {v['file_line']} -> {new}")
                v["file_line"] = new
    # 2. Card edits.
    for cid, edit in EDITS.items():
        item = by_id[cid]
        for key in ("finding", "values", "combining_rule", "memo"):
            if edit.get(key) is not None:
                item[key] = edit[key]
    e16 = by_id["e16_cbo_surge_projection"]
    old = "−$200.9bn to −$246.3bn in the main case adopted September 24 (−$203.2bn to −$249.6bn on September 23)"
    if old not in e16["finding"]:
        raise ValueError("e16 finding no longer carries the September 24 clause")
    e16["finding"] = e16["finding"].replace(old, "−$200.9bn to −$245.7bn in the September 26 case "
                                            "(−$200.9bn to −$246.3bn on September 24; −$203.2bn to −$249.6bn on September 23)")
    swapped = [v for v in e16["values"] if v["file_line"] == f"{R24}:2"]
    if len(swapped) != 1:
        raise ValueError("e16 has no single September 24 main-case value")
    swapped[0].update(label="this account, September 26 case: net effect on other residents",
                      value="-200.9 to -245.7", file_line=f"{R26}:2")
    e16["memo"] = e16["memo"].replace(R24, R26)
    cab = by_id["complete_account_assigned_balance"]
    fourth = [v for v in cab["values"] if v["value"] == "488.5"]
    if len(fourth) != 1:
        raise ValueError("complete_account_assigned_balance has no single 488.5 value")
    fourth[0].update(label="receipts, shared, with the data corrections of September 24 → with the consumption key of "
                           "September 26 (was 545.1 on the September 20 keys)", value="488.5 → 492.5", file_line=f"{R26}:58")
    cab["memo"] = cab["memo"]+f"; {R26} § By side"
    care = [v for v in by_id["e4_care_channels_add"]["values"] if v["value"] == "-4.15"]
    if len(care) != 1:
        raise ValueError("e4_care_channels_add has no single -4.15 value")
    care[0]["label"] = "as the data corrections carry them, inside the main case since September 24"
    # 2b. The edits cite lines of the files at EDITS_BASE; carry those to the files as they stand. Values that
    # already verify are left alone.
    for item in inv["items"]:
        for v in item["values"]:
            new, how = ra.reanchor(v["value"], v["file_line"], EDITS_BASE)
            if new is None:
                raise ValueError(f"Unresolved edited citation {item['id']}: {v['value']!r} @ {v['file_line']} ({how})")
            if new != v["file_line"]:
                log.append(f"re-anchored edit ({how}) {item['id']}: {v['file_line']} -> {new}")
                v["file_line"] = new
    # 3. Combining rules, re-read from the FAQ as it stands.
    rules = {
        "cr_two_anchors": faq_rule("**The two anchors are different objects.**"),
        "cr_offsets_do_not_add": faq_rule("**Offsets do not add unless an entry says so.**"),
        "cr_match_population_horizon_outcome": faq_rule("**A result refutes a claim only when population, horizon"),
        "cr_faq_preamble_routed": faq_rule("Date: 2026-09-21. [ROUTING", drop_prefix="Date: 2026-09-21. "),
        "cr_instrument_ranking_warning": faq_rule("A summary that", phrase="A summary that ranks"),
        "cr_california_texas_shared_ledger": faq_rule("**California and Texas per-person gaps are the shared"),
    }
    if [r["id"] for r in inv["combining_rules"]] != list(rules):
        raise ValueError("combining rule ids changed")
    for r in inv["combining_rules"]:
        text, span = rules[r["id"]]
        if r["text"] != text:
            log.append(f"combining rule {r['id']} text re-read from the FAQ")
        r["text"] = text
        r["file_line"] = f"{FAQ}:{span}"
    # 4. Every value must verify before anything is written.
    failed = [f"{i['id']}: {v['value']!r} @ {v['file_line']}" for i in inv["items"] for v in i["values"]
              if not bc.confirmed(v["value"], v["file_line"])]
    too_many = [i["id"] for i in inv["items"] if len(i["values"]) > 5]
    if failed or too_many:
        raise SystemExit("NOT WRITTEN. Unverified values:\n  "+"\n  ".join(failed)+f"\nmore than five values: {too_many}")
    OUT.write_text(json.dumps(inv, indent=1, ensure_ascii=False)+"\n")
    print("\n".join(log))
    print(f"wrote {OUT}: {len(inv['items'])} cards, {sum(len(i['values']) for i in inv['items'])} values, all verify")


if __name__ == "__main__":
    main()
