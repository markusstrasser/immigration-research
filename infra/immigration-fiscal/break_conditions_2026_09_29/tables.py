"""Write derived/conclusions.csv and derived/common_mode.csv for the break-condition lane.

The text cells are this lane's reading of the cited ladder entries and files. Every number that comes from
engine_breaks.cjs is checked against its CSV first, so a changed engine output stops the build instead of
leaving stale text. Run after `node engine_breaks.cjs`:
    uv run --no-project --offline python3 infra/immigration-fiscal/break_conditions_2026_09_29/tables.py
"""
import csv
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
D = HERE / "derived"


def rows(name):
    with open(D / name, newline="") as f:
        return list(csv.DictReader(f))


def check(label, got, want, tol=0.05):
    if abs(got - want) > tol:
        sys.exit(f"[BLOCKED] {label}: engine output {got:.4f}, text says {want}")


# ---- numbers quoted in the text, checked against engine_breaks.cjs outputs
tally = {(r["model"], r["end"]): r for r in rows("c2_tally.csv")}
check("tally 48", float(tally[("corrected", "low_end_48")]["tally_bn"]), 62.0)
check("tally 11", float(tally[("corrected", "high_end_11")]["tally_bn"]), 49.4)
check("accrual tally 48", float(tally[("corrected", "low_end_48")]["tally_on_accrual_bn"]), -15.3)
check("accrual tally 11", float(tally[("corrected", "high_end_11")]["tally_on_accrual_bn"]), -24.2)
split = {r["end"]: r for r in rows("c3_correction_split.csv")}
check("tax side 48", float(split["low_end_48"]["tax_side_move_bn"]), 44.2)
check("tax side 11", float(split["high_end_11"]["tax_side_move_bn"]), 45.6)
check("spending side 48", float(split["low_end_48"]["spending_side_move_bn"]), -55.1)
check("spending side 11", float(split["high_end_11"]["spending_side_move_bn"]), -56.5)
check("net 48", float(split["low_end_48"]["net_move_bn"]), -10.9)
cuts = {(r["direction"], r["set"]): r for r in rows("c1_min_cuts.csv")}
check("down 3-set", float(cuts[("down", "capital_off+school_within_district+roads_parks_first_year")]["move_pct_of_midpoint"]), -26.2)
check("down 3-set with property", float(cuts[("down", "capital_off+roads_parks_first_year+property_tax_response")]["move_pct_of_midpoint"]), -27.2)
check("up 7%+accrual", float(cuts[("up", "capital_7pct+pension_accrual_payable")]["move_pct_of_midpoint"]), 43.7)
check("up 7%+medical", float(cuts[("up", "capital_7pct+medical_mcbs65")]["move_pct_of_midpoint"]), 25.6)
if any(r["direction"] == "down" and r["minimal"] == "yes" and int(float(r["size"])) < 3 for r in cuts.values()):
    sys.exit("[BLOCKED] a smaller downward cut set exists; the text says 3")
if any(r["direction"] == "up" and r["minimal"] == "yes" and int(float(r["size"])) < 2 for r in cuts.values()):
    sys.exit("[BLOCKED] a single upward item breaks C1; the text says 2")
arms = {r["arm"]: r for r in rows("c1_arms.csv")}
check("7% alone", float(arms["capital_7pct"]["move_pct_of_midpoint"]), 22.4)
check("accrual alone", float(arms["pension_accrual_payable"]["move_pct_of_midpoint"]), 21.3)
gen = rows("c6_generation_break_even.csv")
be_max = max(float(r[k]) for r in gen for k in r if k.startswith("break_even"))
check("largest generation break-even", 100 * be_max, 26.9)
be_max_a = max(float(r[k]) for r in gen if r["convention"] == "a" for k in r if k.startswith("break_even"))
check("largest generation break-even, convention a", 100 * be_max_a, 21.5)

# ---- conclusions
CONCLUSIONS = [
    dict(
        id="C1", claim="Other US residents pay about $355bn a year for the group's presence ($322–387bn)",
        premises="P01 frame; P02 one-year removal; P03 long-run service response; P04 capital return 2–3%; P05 cash pensions; "
                 "P06 defense/old interest at 0; P07 keys; P08 corrections; P09 imputed status; P10 production. Measured: line "
                 "amounts, keys' shares. Assumed: P02–P06, P10. [DATA: ladder 239]",
        break_condition="Down a quarter (<$266bn): the first-year budget horizon alone, $200.9–245.7bn (−37%, ladder 229). Inside "
                        "the long-run frame no one or two of the case's own alternatives suffice; minimal sets of 3, e.g. capital "
                        "return off + schools at the within-district 0.836 + roads/parks at CBO's lag, $244.0–279.7bn (−26%). Up a "
                        "quarter (>$443bn): any pair of 7% capital, accrual pensions, defense by GDP share, e.g. 7% + accrual "
                        "$483.6–535.3bn (+44%). [CALCULATION: engine_breaks.cjs → c1_min_cuts.csv]",
        break_distance_note="Every arm at its own range end. 7% alone +22.4%, accrual alone +21.3%: one convention short. "
                            "All 7 downward alternatives stacked −39%; all 5 upward +67%.",
        rival_reading="The removal cost is mostly a horizon and pricing convention: in the first year budgets respond at CBO's "
                      "rates and no return is charged on existing capital, so the cost is ~$200–250bn. [FRAMING-SENSITIVE]",
        discriminating_observation="Budgets after population outflows (2008–12 Mexican net return, 2020–21 enrollment falls, "
                                   "declining-enrollment districts): spending falling ~1:1 within 3–5 years favors the long-run case.",
        observed_yet="partly: inflow side only (within-district 0.836, 230; 2022–24 surge money 'about half, and late', 252)",
        source="ladder 229, 230, 237–239, 252, 253, 257; main_case_long_run_2026_09_27 components.csv; c1_arms.csv; c1_min_cuts.csv",
    ),
    dict(
        id="C2", claim="Public services decide the sign: taxes cover benefits, but not schools and services",
        premises="P01; P03; P04; P05 cash pensions; P07; P08. The tally (direct receipts − household transfers) is $62.0 / "
                 "$49.4bn at ends 48 / 11 [CALCULATION: c2_tally.csv]; the map's $65bn (60–70) is the Sept 24 staircase row "
                 "before data corrections (figures.json 'tally').",
        break_condition="Clause 1 flips on one convention: Social Security and Part A on accrual (+$77.3 / 73.6bn, ladder 257) "
                        "give −$15.3 / −24.2bn. On cash every tax/transfer tail at its adverse end (medical +11.5, tax block +5–6, "
                        "LTSS +3.0, income tax +2.7, benefits +2.3, care +1.6) leaves about +$23bn at the high end [INFERENCE: additive]. Clause 2 flips only "
                        "below a common service response of 2.8–13.6% (sign_reversal.csv).",
        break_distance_note="Clause 1: zero steps on accrual, an arm the operator weighed on 2026-09-28. Clause 2: far; the "
                            "lowest arm (CBO first-year: GG 0.60–0.85, schools 0.65–0.68) is 4–20× the break-even.",
        rival_reading="Payroll taxes buy future benefits; counted when earned, benefits exceed taxes and the group is a net "
                      "recipient before any service is charged (ladder 257). [FRAMING-SENSITIVE]",
        discriminating_observation="Mostly values (2024 cash flows vs promises earned). The fact inside it: the money's worth of "
                                   "the group's payroll taxes (OASDI 0.974, HI 1.32–1.41 per dollar are national ratios); "
                                   "group-specific earnings and mortality would move it.",
        observed_yet="no (national ratios only)",
        source="c2_tally.csv; ladder 239, 257; main_case_long_run_2026_09_27/derived/sign_reversal.csv; figures_2026_09_22 staircase",
    ),
    dict(
        id="C3", claim="Checks against records move taxes and spending by about $50bn each, and the two almost cancel (net about $11bn)",
        premises="P08 (measured: T-MSIS LTSS 210, pooled MEPS 206, admin benefit keys 217, ASEC fill-in DiD 208; assumed: on-books "
                 "share 0.526 for flagged Mexico-born, 254); P09 imputed status flags; P07 CBO gradients (216); P01.",
        break_condition="On the adopted case taxes +$44.2 / 45.6bn, spending −$55.1 / 56.5bn, net −$10.9bn, no interaction "
                        "[CALCULATION: c3_correction_split.csv]. 'Net about $11bn' moves >25% on any one of six component tails "
                        "(medical MCBS +11.5 → +$0.6bn; care −9.2 → −$20.1bn). 'Almost cancel' fails when the net passes half "
                        "the smaller side (~$22bn): care low + tax block low ≈ −$26bn [INFERENCE: additive, components.csv].",
        break_distance_note="Net figure: 1 tail. The cancellation itself: 2 tails. The rounded '$50bn each' already sits 10–13% "
                            "off both sides.",
        rival_reading="The tax side is a model, not a record: it scales imputed-unauthorized pay to an assumed on-books share "
                      "($64.8bn of $136.8bn of wages off the books, 254), so two assumed adjustments of similar size may cancel.",
        discriminating_observation="SSA Earnings Suspense File and ITIN filer counts by state, 2022–24, to measure the on-books "
                                   "share (no 2022–25 measurement exists).",
        observed_yet="spending side yes (210, 255, 256); tax side partly (249 tests IRS national bins; the group's share per bin stays the CPS's)",
        source="c3_correction_split.csv; components.csv; ladder 206, 208, 210, 216, 217, 249, 254–256",
    ),
    dict(
        id="C4", claim="Costs outside the public budget add about $100bn a year ($94–103bn); the pairing is $416.2–490.7bn",
        premises="Inherits C1's premises. Plus P12 VSL and dose-response (PM2.5 at $13.7m VSL; Miller victim prices), P13 "
                 "crash-volume elasticity (266), P19 offender shares (202). Measured: CCRS fault odds (264), NIBRS shares.",
        break_condition="The add (±$25bn) breaks on any one item at its published range end: PM2.5 $31.5bn (−38) or $122.5bn "
                        "(+53); crashes −$57.7bn (−69) or +$74.3bn (+63); scale net −$84.4bn / +$56.6bn (∓70). Crime at "
                        "tangible loss only ($4.5bn, −24.4) falls just short. The pairing (<$340bn or >$567bn) needs two: "
                        "crash low + scale low (−31%) or PM2.5 high + crash high (+26%). [CALCULATION: real_costs_totals.csv §7]",
        break_distance_note="Add: 1 item. Pairing: 2 items; the first-year horizon (C1) also takes it to about $322bn (−29%) "
                            "with the add held fixed [INFERENCE]. Stacked span $142–757bn.",
        rival_reading="Against as many average residents the group is cleaner (PM2.5 −$46.5bn) and no worse on crashes "
                      "(+$0.6bn): most of the add is the cost of any 40.9M people. [FRAMING-SENSITIVE: absolute vs normalized]",
        discriminating_observation="Values for absolute vs normalized. Fact: the crash sign turns on the crash-volume elasticity; "
                                   "a within-network panel of volumes × crashes in the group's counties (PeMS × CCRS) would "
                                   "narrow −58 to +74.",
        observed_yet="partly: transferable elasticities (266), CCRS fault odds (264); no local volume panel",
        source="ladder 189, 195, 202, 258, 260, 264–266; sept27_propagation_2026_09_27/derived/real_costs_totals.csv",
    ),
    dict(
        id="C5", claim="State and local taxpayers pay most of the cost (85%), and about one resident in six gains",
        premises="P03 (schools at 1 are state-local); P05; P06; P10 wage nest σ=2; P11 incidence: state-local cost charged where "
                 "the group lives, tax-share financing, household pooling. Measured: which budget pays each line; CPS persons.",
        break_condition="'Most' (>50%) survives accrual (≈70%), + defense by GDP (≈61%), + legacy interest $36bn (≈57%) "
                        "[CALCULATION: additive on 226's $349.3bn]; it fails only with defense and old interest at average cost "
                        "(+$271bn federal, ≈48%). 'One in six' (17.8%; a quarter = 13.3–22.2%) breaks inside the lane's own "
                        "11–24% (226): σ 1.5 / 2.5 moved winners ±5pp and national charging cut 23.9% to 13% on the Sept 24 case.",
        break_distance_note="SL share: needs a convention the repo rejects. Winners: one convention [INFERENCE: Sept 24 swings "
                            "carried to the Sept 27 base].",
        rival_reading="Who gains is not identified: winners are modeled channel totals assigned to survey people; halving wage "
                      "deviations moves them 23.9% → 10.3% at the same aggregate (audit §2).",
        discriminating_observation="Person-level wage effects by skill and region from linked employer–employee data (LEHD) "
                                   "against the nest's assigned gains. The defense/interest charge is a values choice.",
        observed_yet="no",
        source="ladder 194, 207, 226; research/immigration-weekly-conceptual-audit-2026-09-25.md §2",
    ),
    dict(
        id="C6", claim="Each generation costs others, and progress stops after the second",
        premises="C1's premises, plus: CPS parental birthplace (self-reported for 54%), child convention (a/b), household "
                 "allocation, P15 self-ID, P16 cross-section as lineage (CPS 1994–2025; GSS).",
        break_condition="Clause 1: a generation turns into a net gain only below its service break-even: ≤ 21.5% under "
                        "convention a, ≤ 26.9% under b (G3+, shared) [CALCULATION: c6_generation_break_even.csv, uncorrected "
                        "generation models; corrections −$8.4 to +$2.6bn]. Clause 2: 0.84 of the BA+ gap carried G2→G3+ (232); a "
                        "quarter (<0.63) needs the literature's G2→G3 transmission 0.46–0.53 (236) in place of the CPS "
                        "cross-section. The white-like identity bound gives 0.69–0.76; with 2 SE ≈ 0.52–0.58 [INFERENCE].",
        break_distance_note="Clause 1: far (≤ 27% against ≥ 0.6 in every arm). Clause 2: one source swap, or the identity bound "
                            "plus 2 SE.",
        rival_reading="Cross-sectional G3+ descends from earlier, less-selected stock, so G2 vs G3+ today is not parent→child; "
                      "matched by cohort, progress may continue. Partly answered: 0.83–0.87 in the 1979–85 cohort and at 25–44 (232).",
        discriminating_observation="Linked three-generation records tying G3 to G2 parents' schooling (restricted Census-linked "
                                   "data or PSID immigrant samples).",
        observed_yet="attempted, no power: CPS adults with a Mexico-born grandparent, closing 0.78 (SE 0.64) (232)",
        source="ladder 224, 232, 236, 255; generation_account_2026_09_24/derived/generation_results.csv; c6_generation_break_even.csv",
    ),
    dict(
        id="C7", claim="Legal status explains little of the fiscal gap",
        premises="P09 imputed status (Borjas residual rules on ASEC 2025); P08 on-books share; P01. Carried by ladder 85: "
                 "unauthorized −7,806 vs legal −8,166 raw, −9,720 vs −8,234 per adult after ineligible transfers are zeroed "
                 "and taxes scaled on-books.",
        break_condition="'Little' fails if the status contrast reaches about half the gap (~$4.5k per adult) [INFERENCE: "
                        "threshold]; measured ~$1.5k (15%). Rule switches (Medicaid clause: 47% → 62% unauthorized among "
                        "low-educated parents, 185) reassign recipients but were not priced [GAP].",
        break_distance_note="Needs a ~3× larger contrast than measured; no priced arm reaches it. The weakness is identification "
                            "(status imputed from benefit receipt), not size.",
        rival_reading="Status acts through the children: minors with no legal parent are 12–14 points less often in college "
                      "at 18–24 (186), and G2 is the costliest generation, so an adult cross-section understates status's share.",
        discriminating_observation="Children's schooling around a status shock unrelated to schooling: DACA age cutoffs or IRCA "
                                   "timing, in ACS by parental arrival cohort.",
        observed_yet="no: CPS 2025 cross-section and IIMMLA only (186)",
        source="ladder 85, 185–187, 254; audit §4 (the lineage model's status result is withdrawn and does not carry this)",
    ),
    dict(
        id="C8", claim="Against as many whites, the group costs others about $320bn a year more ($315–330bn)",
        premises="Rough re-key of the Sept 27 rules (not an engine run; union keys 3–7% below the engine); P14 third-plus "
                 "non-Hispanic whites at national rates; P05 handled by accrual or union ages; P07.",
        break_condition="Already crossed by one computed alternative: local whites state by state $412.3 / 406.2bn (+28%); both "
                        "convention arms on accrual $449.8 / 447.3bn (+41%). Down: cash at whites' own ages $157.2 / 154.6bn "
                        "(−51%), read as the age artefact.",
        break_distance_note="Zero steps: the reference geography is one choice. The ordering (the group costs more) survives "
                            "every arm (min +$155bn).",
        rival_reading="The gap is composition (schooling, age), not group-specific; against an all-residents slice the union is "
                      "$85–87bn above average (263).",
        discriminating_observation="Framing (which reference answers the question). Fact left: the same re-key through the engine "
                                   "to remove the rough keys' 3–7% bias.",
        observed_yet="partly (rough keys)",
        source="ladder 259, 263",
    ),
    dict(
        id="C9", claim="Immigrants offend less, and their US-born sons are held at about twice the white rate",
        premises="P18 Texas DPS felony charges 2012–18 with DHS-matched status; Pew/CMS denominators; P17 ACS institutional "
                 "counts 2010–2024 with the prison-coding fix; P15 self-ID; P19 NIBRS TX/AZ offender ethnicity.",
        break_condition="Clause 1: undocumented at 0.40–0.43 of US-born (cost-weighted per capita; 0.31–0.33 per adult) flip "
                        "only with a 2.3–3.2× undercount; the pooled foreign-born (0.63–0.79) with 1.3–2.1×; legal "
                        "non-naturalized already exceed 1 on cost weights (1.20; sexual assault 2.54) (144). Clause 2: 1.7–1.9 "
                        "raw, 2.1–2.3 coded (65); a quarter (<1.5 or >2.5) needs 2010's 2.56.",
        break_distance_note="Clause 1: undercount size unmeasured [GAP]; the DHS-match boundary is the weak point. Clause 2: "
                            "stable over 2019–2024; the coding fix alone +15–20%; the 2023 race redesign −3%.",
        rival_reading="Clause 1: removal and DHS-record matching take immigrant offenders out of the records. Clause 2: custody "
                      "carries sentencing and detention as well as offending; NCVS victims perceive Hispanic non-fatal "
                      "offending at 0.94× white (202).",
        discriminating_observation="Clause 1: arrests with birthplace recorded at booking independently of DHS records (county "
                                   "jail files). Clause 2: police-recorded offending, NIBRS TX/AZ 1.74–4.22× white by offence.",
        observed_yet="clause 2 yes (202, pooled Hispanic, all generations); clause 1 no",
        source="ladder 65, 66, 70, 82, 144, 196, 202",
    ),
]

# ---- premises: kind, flags for C1..C9, and for the top five the best-supported alternative and its effect
C = [f"C{i}" for i in range(1, 10)]
PREMISES = [
    ("P01", "Survey frame: CPS ASEC / ACS Mexican-origin self-ID and parental birthplace, 40.9M in three generations", "measured (survey)",
     "C1 C2 C3 C4 C5 C6 C7 C8 C9"),
    ("P02", "Removal counterfactual over one income year (2024), people alive in 2024, no lifetime", "convention", "C1 C2 C3 C4 C5 C6 C7 C8"),
    ("P03", "Service budgets respond at long-run average cost (schools 1, general government 0.60–0.85, roads/parks long run)",
     "assumed (cross-section slopes)", "C1 C2 C4 C5 C6 C8"),
    ("P04", "Return on public capital at 2–3%", "convention", "C1 C2 C4 C5 C6"),
    ("P05", "Social Security and Medicare counted as cash, not accrual", "convention", "C1 C2 C4 C5 C6 C8"),
    ("P06", "Defense and existing interest at zero response", "assumed", "C1 C4 C5"),
    ("P07", "Allocation keys: CBO incidence and income gradients, use keys for justice and care", "convention + measured shares",
     "C1 C2 C3 C4 C6 C8"),
    ("P08", "Dataset corrections, including an on-books share of 0.526 for flagged Mexico-born workers", "measured in part; on-books share assumed",
     "C1 C2 C3 C4 C6 C7 C8"),
    ("P09", "Legal status imputed by residual rules (benefit receipt defines some legal)", "imputed", "C1 C2 C3 C4 C7"),
    ("P10", "Production nest: two skill groups, σ 2, ε infinite, capital adjusts", "assumed (calibrated)", "C1 C4 C5 C6"),
    ("P11", "Incidence among residents: where the state-local cost falls, financing rule, household pooling", "convention", "C5"),
    ("P12", "Harm prices: VSL $13.7m, PM2.5 dose-response, Miller victim prices", "assumed (published)", "C4"),
    ("P13", "Crash-volume elasticity transferred from other networks", "assumed (published)", "C4"),
    ("P14", "Reference group: third-plus non-Hispanic whites at national rates", "convention", "C6 C8 C9"),
    ("P15", "Ethnic self-identification keeps descendants in the group", "measured in part (232)", "C6 C9"),
    ("P16", "Cross-sectional generations stand in for lineages", "assumed", "C6 C9"),
    ("P17", "ACS institutional counts identify custody by nativity and ethnicity", "measured, coding errors", "C9"),
    ("P18", "Texas arrest status from DHS record matches", "administrative", "C9"),
    ("P19", "Police-recorded offender ethnicity (NIBRS TX/AZ, SHR; arrests for use keys)", "measured", "C1 C4 C9"),
]
SWAP = {
    "P01": ("ACS level for the Mexico-born (CPS +9–13%, 209); NVSS births for the G2/G3 split (255)",
            "C1 −$2.2–2.5bn (−0.7%) [DATA: 209]; C2 ≈0 (removed people pay about what they cost, 209); C6 moves young "
            "children from G3+ to G2, not computed [GAP], signs hold [INFERENCE]; C7 imputed unauthorized 4.57M → ~4.07M, contrast "
            "not recomputed [GAP]; C3, C4, C5, C8 < 1% [INFERENCE]; C9 unaffected. Breaks none."),
    "P02": ("First-year budget horizon (ladder 229)",
            "C1 −37% BREAK; C4 pairing ≈ −29% BREAK [INFERENCE: add held fixed]; C2 sign holds; C5 winners within 0.1pt (226, "
            "Sept 26 base); C6 each generation within $1bn (224, Sept 26 base); C8 not rerun [GAP]. Breaks two."),
    "P08": ("No corrections (uncorrected model)",
            "C1 +$10.9bn (+3%); C2 tally $66.4 / 54.5bn [CALCULATION: c2_tally.csv]; C3 is this premise; C6 −$8.4 to +$2.6bn per "
            "generation; C7 raw vs adjusted contrast changes direction (85). Breaks none."),
    "P03": ("Schools at the within-district 0.836 (the only within-unit estimate)",
            "C1 −8% ($295.9–363.0bn); C2 sign holds; C4 pairing −6%; C6 holds [INFERENCE]; C8 −$11bn (−3%) [INFERENCE: 15% of "
            "the $72bn schools difference]. Breaks none."),
    "P05": ("Accrual at payable benefits (ladder 257)",
            "C2 clause 1 BREAK (tally −$15.3 / −24.2bn); C1 +21% (a break with any one more upward item); C4 pairing +17%; C5 SL "
            "share 85% → ≈70%; C6 not computed by generation [GAP]; C8 already on accrual ($317.6bn). Breaks one."),
}
by_premise = []
for pid, text, kind, flags in PREMISES:
    fl = set(flags.split())
    by_premise.append((pid, text, kind, [1 if c in fl else 0 for c in C]))
order = sorted(by_premise, key=lambda r: (-sum(r[3]), r[0]))
rank = {r[0]: i + 1 for i, r in enumerate(order)}
top = [r[0] for r in order[:5]]
if set(top) != set(SWAP):
    sys.exit(f"[BLOCKED] top five premises are {top}; SWAP covers {sorted(SWAP)}")

D.mkdir(exist_ok=True)
with open(D / "conclusions.csv", "w", newline="") as f:
    w = csv.writer(f, lineterminator="\n")
    keys = ["id", "claim", "premises", "break_condition", "break_distance_note", "rival_reading",
            "discriminating_observation", "observed_yet", "source"]
    w.writerow(keys)
    for c in CONCLUSIONS:
        w.writerow([c[k] for k in keys])
with open(D / "common_mode.csv", "w", newline="") as f:
    w = csv.writer(f, lineterminator="\n")
    w.writerow(["premise_id", "premise", "kind", *C, "n_conclusions", "rank", "best_supported_alternative", "effect_if_swapped"])
    for pid, text, kind, flags in order:
        alt, eff = SWAP.get(pid, ("", ""))
        w.writerow([pid, text, kind, *flags, sum(flags), rank[pid], alt, eff])
print(f"  ✓ conclusions.csv: {len(CONCLUSIONS)} rows; common_mode.csv: {len(PREMISES)} premises; top five {', '.join(top)}")
