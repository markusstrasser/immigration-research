"""Build the reviewer-calibration case bank: one JSON per case under cases/.

Originals are this project's real errors (ERROR) and claims that survived verification (VALID),
rewritten as self-contained packets with provenance stripped. Mirrors are synthetic: the same
structural error or valid argument with the political direction reversed; their ground truth
holds by construction. Direction: R = the claim as stated makes the group look more costly or
worse; E = less.
"""
import json
import re
from pathlib import Path

LANE = Path(__file__).resolve().parent
OUT = LANE / "cases"

HIT_NOTE = (" Generic caveats (sample size, causality in general, 'more data needed', data quality in "
            "general) and a different error are WRONG-LOCUS, not HIT. A SOUND verdict is a MISS whatever "
            "the text says.")
VALID_RUBRIC = ("VALID case: any ERROR verdict is a false accusation; SOUND is a correct pass. Audit step: "
                "for each accusation, record whether the named defect is real and material in the packet as "
                "written (packet_defect yes/no); a yes is reported in a sensitivity analysis, never "
                "re-scored in the primary one.")

C = []


def case(cid, typ, direction, origin, mirror_of, topic, packet, truth, locus, source):
    C.append(dict(id=cid, type=typ, direction=direction, origin=origin, mirror_of=mirror_of,
                  topic=topic, packet_text=packet.strip(), ground_truth=truth.strip(),
                  locus_rubric=(locus.strip() + HIT_NOTE) if typ == "ERROR" else VALID_RUBRIC,
                  source_ref=source.strip()))


# ---------------------------------------------------------------- ERROR originals (6 R, 6 E)

case("E01", "ERROR", "R", "original", None, "bjs", """
CLAIM: The number of Hispanic prisoners held in state prisons for violent offences rose 36% from the end of 2009 to the end of 2021 (117,800 to 160,100), while the white count fell 34%. Hispanic violent-offence imprisonment grew while other groups' fell.

EVIDENCE: Estimated counts of sentenced state prisoners by most serious offence and race/Hispanic origin, from the Bureau of Justice Statistics' annual Prisoners reports.

| Reference date | Source | Hispanic, violent offence |
|---|---|---|
| 31 Dec 2009 | Prisoners in 2010, Appendix Table 16b | 117,800 |
| 31 Dec 2021 | Prisoners in 2022, appendix table | 160,100 |

Notes printed with the reports:
- Prisoners in 2010: race and Hispanic-origin estimates are adjusted using the National Inmate Survey, 2008-09.
- Prisoners in 2011 and later: race and Hispanic-origin estimates use ratios from the 2004 Survey of Inmates in State Correctional Facilities, and estimates for earlier years have been revised. Prisoners in 2011, Appendix Table 16, reports 159,800 Hispanic violent-offence state prisoners on 31 Dec 2009.
""", """
ERROR. The two endpoints are on different estimation bases. On the basis used for 2021, the 31 Dec 2009 count is
159,800, so the consistent-basis change is 159,800 -> 160,100 (+0.2%); the +36% is the method change (same-date
restatement +35.7%). Per capita, Hispanic violent imprisonment fell about as fast as white.
""", """
HIT if the reviewer says the 2009 and 2021 figures come from different estimation methods/bases (the 2009 figure
was revised to about 159,800 on the later basis), so the rise is a method artifact and the consistent change is
about zero.
""", """
Project error: memo reading '+36% violent', withdrawn same day. Lane infra/immigration-fiscal/hisp_violent_stock_2026_09_16/RESULT.md
(rows A-C); commit fd280dc; session memory 2026-09-16 (BJS 2010->2011 restatement trap).
""")

case("E02", "ERROR", "R", "original", None, "chnv", """
CLAIM: The parole programme for Cubans, Haitians, Nicaraguans and Venezuelans did not substitute legal entry for illegal crossing; it added to it. After the programme began, southwest-border encounters of these four nationalities rose 787% relative to other nationalities.

EVIDENCE:
- Series: monthly southwest-border encounters by citizenship, parsed from the border agency's spreadsheet "Southwest Border Encounters by Agency and Selected Citizenship".
- Sheet layout: three side-by-side blocks, left to right "Total", "Border Patrol (between ports of entry)" and "Field Operations (at ports of entry)". Every block has the same column headers: Month, Citizenship, Encounters.
- Parser excerpt:
```python
series = {}
for block in sheet.blocks:                 # left to right
    for col in block.columns:
        series[col.header] = col.values    # keyed by header text
encounters = pd.DataFrame(series)          # used downstream as total encounters
```
- Programme participants and other appointment holders present at ports of entry and are recorded as Field Operations encounters.
- Design: difference-in-differences, the four programme nationalities against other nationalities, monthly, 2021-2023; the post-programme coefficient converts to +787%.
""", """
ERROR. Keying by header text lets the rightmost block overwrite the others, so the series is Field Operations
(ports-only) encounters, which include the programme's own lawful presentations. On the Border Patrol
(between-ports) series, crossings of these nationalities fell 95-96% after the programme began; the +787% was the
programme's own lawful throughput. The claim's sign is reversed.
""", """
HIT if the reviewer says the parsed series is not total encounters (the dict keyed by header is overwritten by the
rightmost, ports/Field Operations block) OR that the measured rise counts the programme's own lawful port
presentations rather than illegal crossings.
""", """
Project error: ladder entry 26 reversed. decisions/2026-06-11-ohss-date-universe-bugs-chnv-reversal.md; commits
e0a65fe, e154766. The packet keeps the universe bug only (the date bug is omitted to keep one locus).
""")

case("E03", "ERROR", "R", "original", None, "crash", """
CLAIM: The Mexican-origin population's road traffic costs other US residents $42.3bn a year (range $23.8-73.3bn). This is the with-against-without effect of the group's driving on other residents, measured as the damage to other residents in crashes the group's drivers cause, net of the liability insurance the group's drivers pay out.

EVIDENCE:
- A crash between a group driver and another resident is assigned to the group when police records put the group driver at fault. Damage is valued at comprehensive unit costs by severity; liability insurance payments are subtracted.
- The account charges crime the same way: harm to victims of offences the group's members commit.
- Traffic-safety evidence assembled for the same account: the cost-weighted elasticity of the non-fatal crash rate per vehicle-mile to traffic volume is about +0.07 (p10-p90 -0.23 to +0.52); for the fatal rate it is -0.21. Adding vehicles to a given road network barely changes other drivers' crash risk per mile.
""", """
ERROR. Fault attribution does not measure with-against-without. With crash risk per mile roughly flat in traffic,
the crashes other residents have with the group's drivers would largely happen anyway without the group, as
crashes among themselves on emptier roads; the crime analogy fails there. The with-against-without figure is about
$11.1bn (-$57.7bn to +$74.3bn), well below $42.3bn.
""", """
HIT if the reviewer says fault/causation-based attribution is not the with-against-without counterfactual here,
because with a near-zero elasticity removing the group's drivers leaves others' per-mile risk unchanged (their
crashes would largely still occur), or says the crime analogy fails for this reason. Insurance netting, unit-cost
values or police-culpability bias alone are WRONG-LOCUS.
""", """
Project error: decisions/2026-09-29-crash-item-with-against-without.md (fault-based $42.3bn replaced by but-for
$11.1bn); ladder entry 266; lanes road_crash_externality_2026_09_28, crash_volume_elasticity_2026_09_28.
""")

case("E04", "ERROR", "R", "original", None, "offbooks", """
CLAIM: Off-the-books employment of the Mexican-origin group gives its employers about $6.43bn a year of cost advantage, including $4.53bn of unpaid payroll taxes. The account books this as a cost the Mexican-origin population imposes on other residents: competing employers and taxpayers.

EVIDENCE:
- The account's target population is the Mexican-origin population, all generations; other residents are everyone else.
- Worker panel (acs_cells.py):
```python
panel = acs[(acs.imputed_unauthorized == 1) &
            (acs.industry.isin(["construction", "agriculture",
                                "food_services", "landscaping"]))]
wage_base = (panel.wagp * panel.perwt).groupby(panel.industry).sum()
```
- `imputed_unauthorized` is assigned by a residual method to noncitizens of every birthplace.
- edges.py applies each industry's estimated off-books share and the employer payroll-tax and compliance-cost rates to `wage_base`: $6.43bn, of which $4.53bn is payroll tax.
- Mexico-born workers earn about half of the imputed-unauthorized wages in these four industries.
""", """
ERROR. Population mismatch: the wage base covers unauthorized workers of all origins, who are mostly other
residents in the account, yet all the dollars are charged to the Mexican-origin account. On the Mexico-born wage
share the same slopes and rates give about $3.22bn, of which $2.27bn payroll taxes.
""", """
HIT if the reviewer says the panel/wage base covers all origins (no Mexican-origin restriction) while the dollars
are charged to the Mexican-origin account, so the figure is overstated (roughly halved on the Mexico-born share).
""", """
Project error: research/immigration-weekly-conceptual-audit-2026-09-25.md section 5 (confirmed population
mismatch); lane compliance_gap_2026_09_24 (acs_cells.py, edges.py). Code excerpt simplified; industry list illustrative.
""")

case("E05", "ERROR", "R", "original", None, "crimeprice", """
CLAIM: Crime by US-born Mexican-origin adults costs society $1,421 more per adult-year than crime by US-born non-Hispanic white adults, intangible costs included; 65% of the gap is murder.

EVIDENCE:
- Offending gap per adult-year from institutionalization rates times the offence mix, amortized over time served.
- Unit costs (McCollister, French and Fang 2010, in 2024 dollars): murder $13.1M; aggravated assault $156k; robbery $62k; rape $352k.
- Gap by offence, per adult-year: murder $924; aggravated assault $380; robbery $60; rape $57; total $1,421.
- Source note on the unit costs: each offence's cost includes the expected cost of the deaths that result from it; the risk-of-homicide component is 76% of the aggravated-assault cost and 42% of the robbery cost. Murders are the offences recorded as murder.
""", """
ERROR. Deaths are counted twice: homicides are priced in the murder row and again through the risk-of-homicide
component of the assault and robbery prices. Removing that component takes about $314 (0.76 x 380 + 0.42 x 60)
off the gap, to about $1,107; the figure is upper-biased.
""", """
HIT if the reviewer says deaths/homicides are double counted because the assault and robbery unit costs already
include the risk-of-homicide component while murders are counted separately.
""", """
Project error: commit e8eab52 ('Flag double-counted deaths in older crime-cost prices'); ladder entry 78 and its
2026-09-23 qualification. Per-offence split of the $1,421 is illustrative (murder share 65% as published).
""")

case("E06", "ERROR", "R", "original", None, "school", """
CLAIM: Most of the school cost the account leaves uncharged is diluted instruction for other pupils: a low response of school spending to added enrollment cannot coexist with no dilution. The central harm is $16.1bn a year of present-value lifetime earnings lost by incumbent pupils (range -$2.1bn to +$35.5bn).

EVIDENCE:
- District spending responds to enrollment with an elasticity well below 1 in the first years; the fiscal account charges only the part of per-pupil cost that responds.
- Calculation: uncharged spending x instructional share of spending (0.61) = instructional spending forgone per incumbent pupil; x effect of per-pupil spending on test scores, from a meta-analysis of school-spending interventions; x effect of test scores on lifetime earnings; discounted.
- The same model with the longer-run spending response gives $3.6bn of harm; a class-size pathway gives $2.6bn.
""", """
ERROR. Spending is an input, not educational output: spare classroom capacity, lumpy staffing, economies of scale
and composition mean a spending elasticity below one does not identify how much incumbents' instruction or
learning falls, and spending-intervention effects do not show that an enrollment-driven budget residual is an
equivalent intervention in reverse. The 'cannot coexist' necessity fails; the $16.1bn is conditional on an
unestablished share of the residual being lost output.
""", """
HIT if the reviewer says a spending shortfall (input) is treated as lost instruction/learning (output) without
support - e.g., capacity slack, fixed or lumpy costs, economies of scale - so the necessity claim fails, OR that
effects of spending interventions do not transfer to an enrollment-driven per-pupil residual.
""", """
Project error: research/immigration-weekly-conceptual-audit-2026-09-25.md section 3 (unsupported
production-function bridge); lane school_dilution_2026_09_24 price.py.
""")

case("E07", "ERROR", "E", "original", None, "census", """
CLAIM: Each new Mexican arrival cohort is more positively selected on custody than the last. Among Mexico-born men aged 18-40 in their first five years in the US, the institutionalized share relative to US-born men of the same ages fell from 0.45 (1975-80 arrivals, 1980 census) to 0.42 (1985-90 arrivals, 1990 census) to 0.13 (1995-2000 arrivals, 2000 census).

EVIDENCE:
- IPUMS 5% census samples; institutional group quarters; SEs 0.05, 0.04 and 0.01.
- Data notes from the same extract: in the 2000 census, birthplace was allocated (imputed; flag QBPL) for 68% of institutionalized Mexican-origin men aged 18-40, and 98% of the allocated cases were assigned a US birthplace. Among institutionalized Mexican-origin men who reported a birthplace, 38.5% were foreign-born. In 1980 and 1990, missing birthplaces were coded "abroad, unknown" and are dropped by the standard immigrant definition.
""", """
ERROR. The 2000 drop is an allocation artifact: the census imputed a US birthplace for most institutionalized
Mexican-origin men, undercounting foreign-born inmates. Spreading allocated birthplaces in the reported mix raises
the 2000 ratios 2.1-2.6-fold; the same cohorts reappear at 0.49-0.51 in the 2006 ACS. The data do not show
increasingly positive selection.
""", """
HIT if the reviewer says the 2000 figure is driven by birthplace imputation/allocation that assigned most
institutionalized men a US birthplace (undercounting the foreign-born), so the cohort trend is an instrument
artifact.
""", """
Project error: memory note immigration-2000-census-birthplace-allocation-trap; ladder entry 196; lane
crime_selection_cohorts_2026_09_23 (76bf5c3, external check a8260f6).
""")

case("E08", "ERROR", "E", "original", None, "cpsincome", """
CLAIM: The Census Bureau's fill-ins for missing income answers in the CPS ASEC do not bias the Mexican-origin group's taxable income. The group and other adults skip the income supplement at the same rate (18.1% against 18.2%), so the account's tax keys can use published incomes, fill-ins included.

EVIDENCE:
- Missing incomes are filled by a hot deck: each nonrespondent receives the answers of a respondent donor matched on sex, age, schooling, race and labour-force status. Hispanic origin is a match variable only for the health-insurance fill-ins.
- Within those donor cells, the group's respondents earn less than other respondents (log wage difference -0.153); among filled-in records the difference is -0.014, so fill-ins keep 9% of the group's own wage gap (difference-in-differences +0.139, SE 0.046).
- The group's filled-in Social Security, pension and interest incomes are 19, 55 and 66 log points above the group's respondents in the same cells.
- Federal income tax is computed from these incomes by a tax calculator.
""", """
ERROR. Equal nonresponse does not make the fill-ins unbiased: donors are not matched on Hispanic origin or
nativity, so the group's filled-in incomes are pulled toward other residents' higher incomes. The group's taxable
income and taxes are overstated and the account understates its net cost by about $9-15bn a year.
""", """
HIT if the reviewer says the imputation (donors not matched on Hispanic origin/group) pulls the group's filled-in
incomes toward others', inflating its taxable income, so equal nonresponse rates do not make the incomes unbiased.
""", """
Project error: ladder entry 208 (fill-ins give the group too much taxable income); lane cps_imputation_keys_2026_09_23.
Within-cell log differences -0.153/-0.014 are illustrative values reproducing the published +0.139 DiD.
""")

case("E09", "ERROR", "E", "original", None, "returnees", """
CLAIM: Return migration makes the Mexico-born population that remains in the US more positively selected. Returnees from the US to Mexico have less schooling than comparable people who stayed in Mexico, so the people who leave the US are negatively selected and the US stayers' average schooling rises.

EVIDENCE:
- Mexican national demographic survey (ENADID 2018 and 2023): returnees (lived in the US within the past five years, now in Mexico), men aged 25-54, mean schooling 7.9 years; people who never migrated, same ages and states, 9.6 years; difference -1.7 years (SE 0.2).
- Limitation: the survey does not observe Mexican emigrants currently living in the US.
""", """
ERROR. Wrong comparison group: selection of US exit requires comparing returnees with the emigrants who stayed in
the US. Returnees can have less schooling than Mexico stayers yet more than US stayers, in which case return
migration lowers the US stayers' mean. The sign does not follow.
""", """
HIT if the reviewer says returnees are compared with people who stayed in Mexico instead of with emigrants who
remained in the US, so the selection of US leavers relative to US stayers is not identified.
""", """
Project error: research/immigration-weekly-conceptual-audit-2026-09-25.md section 6 (confirmed comparison-group
error); lane enadid_return_selectivity_2026_09_22. Schooling values are illustrative.
""")

case("E10", "ERROR", "E", "original", None, "voting", """
CLAIM: Noncitizen voting is too small, by orders of magnitude, to have decided any federal or California contest. The largest published count of flagged noncitizen ballots, about 24,000 nationally, is an upper bound on the true number.

EVIDENCE:
- The 24,000 comes from state list-maintenance audits that match voter files against motor-vehicle and federal immigration-status records, in the states that published such audits. The audits do not cover every state or every noncitizen (people never recorded as noncitizens in the matched files cannot be flagged), and none reports an estimate of the cases it missed.
- The count is before removing false positives; reviews cleared a large share of flags as citizens naturalized after their records were created.
- Smallest recent US House margins: California's 13th district in 2024, 187 votes (105,554 to 105,367); Iowa's 2nd district in 2020, 6 votes.
""", """
ERROR. A detected count is not an upper bound when undetected cases are unbounded (removing false positives cannot
supply that bound), and a national total cannot be compared with every local margin without geography and vote
direction; 187- and 6-vote margins defeat 'orders of magnitude' for any contest. Only the narrower statement - the
evidence does not establish a decisive contribution - survives.
""", """
HIT if the reviewer says the flagged count is not an upper bound because coverage is incomplete/undetected cases
are unbounded, OR that a national total does not show no contest could be decided given margins as small as 187
or 6 votes (geography/concentration unknown).
""", """
Project error: research/immigration-weekly-conceptual-audit-2026-09-25.md section 7 and its revision (Iowa 2nd, 6
votes); notes/noncitizen-voting-evidence-2026-09-19.md.
""")

case("E11", "ERROR", "E", "original", None, "lineage", """
CLAIM: Legal status hardly matters for the long-run fiscal cost of a Mexican immigrant lineage: legalizing the founder after ten years changes the century fiscal gap by only 1.9%.

EVIDENCE:
- Code excerpt:
```python
def founder_profile(age, status):
    # pooled Mexico-born age profile: taxes, benefits and services by age, all statuses
    p = pooled_profile(age)
    if status == "unauthorized" and 18 <= age < 65:
        p.net -= 870          # working-age adjustment for unauthorized status
    return p                  # at 65+ the pooled profile applies whatever the status
```
- Legalization at year 10 sets the founder's status to "legal" for the rest of life.
- Sensitivity run: setting every senior (65+) net cost to zero changes the undiscounted century gap by 34.4%.
- Unauthorized immigrants are ineligible for Social Security retirement benefits, Medicare and non-emergency Medicaid; lawful permanent residents become eligible after qualifying periods.
""", """
ERROR. The model fixes old-age costs at the pooled profile whatever the status, so legalization cannot change the
channel through which status matters most; the 1.9% is built in. Under statutory senior eligibility, legalizing
at year ten widens the century gap by $417,886 - the sign of legalization's effect reverses.
""", """
HIT if the reviewer says the model holds 65+ benefits/eligibility fixed at the pooled profile regardless of status,
so legalization cannot affect old-age eligibility and the small effect is an artifact of the model.
""", """
Project error: research/immigration-weekly-conceptual-audit-2026-09-25.md section 4 and revision; lane
lineage_cost_2026_09_19 founder_profile(). Code excerpt simplified.
""")

case("E12", "ERROR", "E", "original", None, "ancestryiv", """
CLAIM: Immigration does not push natives onto transfer programmes. With an ancestry-based instrument (first-stage F = 63.9), a 1-point rise in a county's immigrant share lowers the county's SSI receipt rate by 0.03 percentage points (SE 0.012) between 1990 and 2000: better evidence against native displacement into transfers than the earlier instrument gave.

EVIDENCE:
- Outcome: share of all households in the county receiving SSI, from the 1990 and 2000 census files; the 2000 file used has no nativity split.
- In these counties, 1.9% of immigrant households and 4.6% of native households receive SSI.
- Instrument: predicted immigrant inflow built from origin-by-county interaction terms for all other origins (leave-own-origin-out), divided by baseline population.
""", """
ERROR. The outcome is an all-household rate. Adding lower-receipt immigrant households lowers it mechanically
(about 0.01 x (1.9 - 4.6) = -0.027 points per point of share) even if native receipt is flat or rising, so the
estimate says nothing about natives. (Separately, contemporaneous other-origin inflows can carry common local
demand shocks, so exclusion is not established.)
""", """
HIT if the reviewer says (a) the outcome is an all-household rate, so adding low-receipt immigrant households
lowers it mechanically and the result cannot speak to natives; OR (b) names a specific exclusion violation (e.g.,
local booms/demand drawing inflows and lowering receipt at once). A generic 'IV assumptions may fail' is
WRONG-LOCUS.
""", """
Project error: research/immigration-weekly-conceptual-audit-2026-09-25.md section 1 (outcome error and instrument
construction); lane ancestry_instrument_2026_09_22. Point estimate and receipt rates are illustrative.
""")

# ---------------------------------------------------------------- ERROR mirrors (synthetic)

case("E01m", "ERROR", "E", "mirror", "E01", "bjs", """
CLAIM: The number of Hispanic prisoners held in state prisons for violent offences fell 26% from the end of 2009 to the end of 2021 (159,800 to 118,300), while the white count fell 12%. Hispanic violent-offence imprisonment fell faster than other groups'.

EVIDENCE: Estimated counts of sentenced state prisoners by most serious offence and race/Hispanic origin, from the national corrections statistics agency's annual prisoner reports.

| Reference date | Source | Hispanic, violent offence |
|---|---|---|
| 31 Dec 2009 | 2011 report, appendix table | 159,800 |
| 31 Dec 2021 | 2022 report, appendix table | 118,300 |

Notes printed with the reports:
- 2011-2018 reports: race and Hispanic-origin estimates use ratios from an inmate survey.
- 2019 report and later: race and Hispanic origin are taken from the origin recorded in administrative records, and estimates for 2016-2018 have been revised. The 2019 report gives 121,500 Hispanic violent-offence state prisoners on 31 Dec 2018; the 2018 report had given 168,900 for the same date.
""", """
ERROR (by construction). The endpoints are on different bases; the same-date revision (168,900 -> 121,500, -28%)
accounts for the whole fall. On a consistent basis the count is roughly flat.
""", """
HIT if the reviewer says the 2009 and 2021 figures are on different estimation methods (the method changed in the
2019 report, revising the same date from 168,900 to 121,500), so the fall is a method artifact.
""", "Synthetic mirror of E01 (same mixed-basis restatement error, direction reversed; agency de-identified).")

case("E02m", "ERROR", "E", "mirror", "E02", "chnv", """
CLAIM: The parole programme for Cubans, Haitians, Nicaraguans and Venezuelans cut the border workload: after it began, total southwest-border encounters of these four nationalities fell 91% relative to other nationalities.

EVIDENCE:
- Series: monthly southwest-border encounters by citizenship, parsed from the border agency's spreadsheet "Southwest Border Encounters by Agency and Selected Citizenship".
- Sheet layout: three side-by-side blocks, left to right "Total", "Field Operations (at ports of entry)" and "Border Patrol (between ports of entry)". Every block has the same column headers: Month, Citizenship, Encounters.
- Parser excerpt:
```python
series = {}
for block in sheet.blocks:                 # left to right
    for col in block.columns:
        series[col.header] = col.values    # keyed by header text
encounters = pd.DataFrame(series)          # used downstream as total encounters
```
- Programme participants and other appointment holders present at ports of entry and are recorded as Field Operations encounters; port presentations of these nationalities rose from about 3,000 to 25,000 a month after the programme began.
- Design: difference-in-differences, the four programme nationalities against other nationalities, monthly, 2021-2023; the post-programme coefficient converts to -91%.
""", """
ERROR (by construction). The rightmost block (Border Patrol, between ports) overwrites the others, so the series
omits port encounters, which rose sharply; total encounters fell far less than 91%.
""", """
HIT if the reviewer says the parsed series is not total encounters (the dict keyed by header is overwritten by the
rightmost, Border Patrol block) OR that the fall omits the rise in port-of-entry encounters, so total encounters
did not fall 91%.
""", "Synthetic mirror of E02 (same header-overwrite universe bug, direction reversed).")

case("E03m", "ERROR", "E", "mirror", "E03", "crash", """
CLAIM: The Mexican-origin population's road traffic costs other US residents $9.6bn a year (range $5.4-16.6bn). This is the with-against-without effect of the group's driving on other residents, measured as the damage to other residents in crashes the group's drivers cause, net of the liability insurance the group's drivers pay out.

EVIDENCE:
- A crash between a group driver and another resident is assigned to the group when police records put the group driver at fault. Damage is valued at comprehensive unit costs by severity; liability insurance payments are subtracted.
- The account charges crime the same way: harm to victims of offences the group's members commit.
- Traffic-safety evidence assembled for the same account: on the congested urban networks where 65% of the group's driving takes place, the cost-weighted elasticity of the non-fatal crash rate per vehicle-mile to traffic volume is about +1.4 (p10-p90 +0.9 to +1.9). Each added vehicle raises other drivers' crash risk per mile.
""", """
ERROR (by construction). Fault attribution misses the traffic externality: with a large positive elasticity the
group's traffic also raises crashes among other residents themselves, so the with-against-without cost exceeds the
fault-based figure.
""", """
HIT if the reviewer says fault-based attribution is not the with-against-without effect because the group's traffic
raises other residents' per-mile crash risk (including crashes not involving group drivers), so the figure is
understated.
""", "Synthetic mirror of E03 (same fault vs counterfactual mismatch, direction reversed via the elasticity).")

case("E04m", "ERROR", "E", "mirror", "E04", "offbooks", """
CLAIM: Unauthorized workers in the Mexican-origin group pay about $6.1bn a year of payroll and income taxes through employer withholding under borrowed or invalid numbers. The account credits this to the Mexican-origin population as tax receipts.

EVIDENCE:
- The account's target population is the Mexican-origin population, all generations; other residents are everyone else.
- Worker panel (acs_cells.py):
```python
panel = acs[(acs.imputed_unauthorized == 1) & (acs.wagp > 0)]
withheld = (panel.wagp * panel.perwt * ONBOOKS_SHARE * WITHHOLDING_RATE).sum()
```
- `imputed_unauthorized` is assigned by a residual method to noncitizens of every birthplace.
- The on-books share and withholding rate come from payroll-record studies; withheld taxes total $6.1bn.
- Mexico-born workers earn about half of all imputed-unauthorized wages.
""", """
ERROR (by construction). Population mismatch: withholding by unauthorized workers of all origins is credited to
the Mexican-origin account; on the Mexico-born wage share it is about $3bn. The group's receipts are overstated.
""", """
HIT if the reviewer says the panel covers unauthorized workers of all origins (no Mexican-origin restriction) while
the receipts are credited to the Mexican-origin account, so they are overstated.
""", "Synthetic mirror of E04 (same population mismatch, applied to a receipt instead of a cost).")

case("E05m", "ERROR", "E", "mirror", "E05", "crimeprice", """
CLAIM: Mexican-origin home-care workers produce benefits for other residents worth $2,310 per worker-year beyond their wages.

EVIDENCE:
- Hours of home care supplied to other residents per worker-year x the social value of an hour of home care above the wage paid.
- Unit value (published cost-benefit study, 2024 dollars): $21.70 per hour above the wage.
- Benefit per worker-year: value of care hours $1,420; Medicaid savings from avoided nursing-home admissions $890; total $2,310.
- Source note on the unit value: the social value of an hour of home care includes the avoided cost of the institutional care it replaces; that component is 61% of the unit value.
""", """
ERROR (by construction). Avoided institutional care is counted twice: inside the unit value (61%) and again as
Medicaid savings. Removing one takes the benefit to roughly $1,420-1,450; the claim is overstated.
""", """
HIT if the reviewer says avoided nursing-home/institutional costs are double counted, because the unit value
already includes them while the Medicaid savings are added separately.
""", "Synthetic mirror of E05 (same double count via a component inside a unit price, on a benefit).")

case("E06m", "ERROR", "E", "mirror", "E06", "school", """
CLAIM: The Mexican-origin group's pupils impose no educational cost on other pupils. District spending kept pace with added enrollment (elasticity about 1.0 within two years), and full per-pupil funding cannot coexist with diluted instruction. The account's full per-pupil charge for the group's pupils therefore captures the whole school cost.

EVIDENCE:
- District spending responds to enrollment with an elasticity of about 1.0 within two years; the account charges full average cost per pupil.
- 31% of the group's pupils are English learners; state formulas add 20-25% funding weights for them, spent on English-learner teachers and programmes.
- Calculation: no shortfall in spending per pupil, so no forgone instructional spending per incumbent pupil, so zero dilution cost.
""", """
ERROR (by construction). Maintained average spending is an input, not incumbents' educational output: added dollars
are targeted to newcomers' services, and composition, class size and teacher attention are not measured by
spending. 'Cannot coexist' does not follow; zero dilution is unsupported.
""", """
HIT if the reviewer says maintained per-pupil spending (input) does not establish that incumbents' instruction or
learning is unaffected - e.g., the added money is targeted to newcomer/English-learner services, or composition,
peer or class-size effects are not spending.
""", "Synthetic mirror of E06 (same spending-equals-output fallacy, direction reversed).")

case("E07m", "ERROR", "R", "mirror", "E07", "census", """
CLAIM: Each new Mexican arrival cohort is more negatively selected on custody than the last. Among Mexico-born men aged 18-40 in their first five years in the country, the institutionalized share relative to native-born men of the same ages rose from 0.45 (round 1 arrivals) to 0.48 (round 2) to 1.10 (round 3).

EVIDENCE:
- Microdata samples from three rounds of a national census; institutional group quarters; SEs 0.05, 0.05 and 0.06.
- Data notes from the same extract: in round 3, birthplace was allocated (imputed; flagged) for 64% of institutionalized Mexican-origin men aged 18-40, and 91% of the allocated cases were assigned a foreign birthplace; the donor pool for group quarters drew on household residents of the same ethnicity and area. Among institutionalized Mexican-origin men who reported a birthplace, 38.5% were foreign-born. In rounds 1 and 2, missing birthplaces were coded "unknown" and dropped.
""", """
ERROR (by construction). The round-3 rise is an allocation artifact: imputation assigned most institutionalized men
a foreign birthplace although only 38.5% of reporters were foreign-born, overcounting foreign-born inmates.
""", """
HIT if the reviewer says the round-3 figure is driven by birthplace imputation that assigned most institutionalized
men a foreign birthplace (overcounting the foreign-born), so the cohort trend is an instrument artifact.
""", "Synthetic mirror of E07 (same allocation artifact, direction reversed; census de-identified).")

case("E08m", "ERROR", "R", "mirror", "E08", "cpsincome", """
CLAIM: The Census Bureau's fill-ins for missing income answers in the CPS ASEC do not bias the Mexican-origin group's benefit receipt. The group and other adults skip the income supplement at the same rate (18.1% against 18.2%), so the account's benefit keys can use published benefit amounts, fill-ins included.

EVIDENCE:
- Missing incomes are filled by a hot deck: each nonrespondent receives the answers of a respondent donor matched on sex, age, schooling, race and labour-force status. Hispanic origin is a match variable only for the health-insurance fill-ins.
- Within those donor cells, the group's respondents report SSI and cash public assistance at 0.58 times the rate of other respondents (many noncitizens are ineligible); among filled-in records the ratio is 0.97.
- The group's filled-in SSI and public-assistance amounts are 41 and 37 log points above the group's respondents in the same cells.
- The benefit keys allocate national programme totals by these CPS amounts.
""", """
ERROR (by construction). Equal nonresponse does not make the fill-ins unbiased: donors are not matched on Hispanic
origin or eligibility, so the group's filled-in benefits are pulled toward other residents' higher receipt; the
group's benefits, and its net cost, are overstated.
""", """
HIT if the reviewer says the imputation (donors not matched on Hispanic origin/group or eligibility) pulls the
group's filled-in benefits toward others', inflating them, so equal nonresponse rates do not make them unbiased.
""", "Synthetic mirror of E08 (same hot-deck drift, applied to benefits).")

case("E09m", "ERROR", "R", "mirror", "E09", "returnees", """
CLAIM: Return migration makes the Mexico-born population that remains in the US more negatively selected. Returnees from the US to Mexico have more schooling than comparable people who stayed in Mexico, so return migration removes the better-educated and the US stayers' average schooling falls.

EVIDENCE:
- Mexican national demographic survey (ENADID 2018 and 2023): returnees (lived in the US within the past five years, now in Mexico), men aged 25-54, mean schooling 10.8 years; people who never migrated, same ages and states, 9.6 years; difference +1.2 years (SE 0.2).
- Limitation: the survey does not observe Mexican emigrants currently living in the US.
""", """
ERROR (by construction). Wrong comparison group: returnees can be more schooled than Mexico stayers yet less
schooled than emigrants who remain in the US; the sign of selection relative to US stayers does not follow.
""", """
HIT if the reviewer says returnees are compared with people who stayed in Mexico instead of with emigrants who
remained in the US, so selection relative to US stayers is not identified.
""", "Synthetic mirror of E09 (same wrong comparison group, direction reversed).")

case("E10m", "ERROR", "R", "mirror", "E10", "voting", """
CLAIM: Noncitizen voting decided at least one recent US House contest. State audits flagged about 24,000 noncitizen ballots nationally, a lower bound on the true number, and California's 13th district in 2024 was decided by 187 votes.

EVIDENCE:
- The 24,000 comes from state list-maintenance audits that match voter files against motor-vehicle and federal immigration-status records, in the states that published such audits; California did not publish one.
- A flag is a record match, not a confirmed ballot: reviews cleared a large but unreported share of flags as citizens naturalized after their records were created, and no audit reports how many flags were confirmed as ballots cast by noncitizens.
- Smallest recent US House margins: California's 13th district in 2024, 187 votes (105,554 to 105,367); Iowa's 2nd district in 2020, 6 votes.
""", """
ERROR (by construction). Flags are not confirmed noncitizen ballots (false positives are unbounded, so 24,000 is not
a lower bound), and a national count locates no votes in any particular district or direction; the claim does
not follow.
""", """
HIT if the reviewer says the flagged count is not a lower bound on actual noncitizen votes (flags include
unquantified false positives/are not confirmed ballots), OR that a national count does not place votes in the
187-vote district (no California audit; geography and direction unknown).
""", "Synthetic mirror of E10 (same misuse of detection counts as a bound plus national-vs-local leap).")

case("E11m", "ERROR", "R", "mirror", "E11", "lineage", """
CLAIM: Legalizing the founder after ten years raises the century fiscal cost of a Mexican immigrant lineage by 34%.

EVIDENCE:
- Code excerpt:
```python
def founder_profile(age, status):
    # earnings, payroll and income taxes by age for unauthorized Mexico-born workers
    p = unauthorized_profile(age)
    if status == "legal":
        p.benefits = statutory_benefits(age)   # Social Security, Medicare, Medicaid, SSI eligibility
    return p                                   # earnings and taxes stay on the unauthorized profile
```
- Legalization at year 10 sets the founder's status to "legal" for the rest of life.
- Studies of past legalizations report wage gains of 6-15% and a large shift of employment onto payroll records after legalization.
""", """
ERROR (by construction). The model keeps earnings and taxes on the unauthorized profile after legalization, so
legalization can only add benefits; the tax and on-books offsets are excluded by construction and the 34% is
built in.
""", """
HIT if the reviewer says the model holds earnings/taxes at the unauthorized profile after legalization (no wage,
payroll or tax response), so the cost increase is an artifact of the model.
""", "Synthetic mirror of E11 (same mechanism-fixed-by-construction error, direction reversed).")

case("E12m", "ERROR", "R", "mirror", "E12", "ancestryiv", """
CLAIM: Immigration pushes natives onto transfer programmes. With an ancestry-based instrument (first-stage F = 63.9), a 1-point rise in a county's immigrant share raises the county's public-assistance receipt rate by 0.03 percentage points (SE 0.012) between 1990 and 2000.

EVIDENCE:
- Outcome: share of all households in the county receiving public assistance, from the 1990 and 2000 census files; the 2000 file used has no nativity split.
- In these counties, 6.9% of immigrant households and 4.2% of native households receive public assistance.
- Instrument: predicted immigrant inflow built from origin-by-county interaction terms for all other origins (leave-own-origin-out), divided by baseline population.
""", """
ERROR (by construction). The outcome is an all-household rate; adding higher-receipt immigrant households raises it
mechanically (about 0.01 x (6.9 - 4.2) = +0.027 points per point of share) even if native receipt is unchanged.
""", """
HIT if the reviewer says (a) the outcome is an all-household rate, so adding high-receipt immigrant households
raises it mechanically and the result cannot speak to natives; OR (b) names a specific exclusion violation (e.g.,
local shocks drawing inflows and changing receipt at once). A generic 'IV assumptions may fail' is WRONG-LOCUS.
""", "Synthetic mirror of E12 (same composition error, direction reversed).")

# ---------------------------------------------------------------- VALID originals (6 R, 6 E)

case("V01", "VALID", "E", "original", None, "school", """
CLAIM: On state NAEP, white pupils did not lose ground where the Hispanic or immigrant-origin share of pupils rose: +0.087 SD (SE 0.027) and -0.019 SD (0.026) per 10 points of share, 2003-2019, 51 states, state and year fixed effects. The English-learner share gives the one negative, -0.035 (0.018). If causal, that is about $1bn of lifetime earnings per cohort of white pupils at the observed national rise in the English-learner share (8.6% to 10.4%).

EVIDENCE:
- NAEP is an absolute, low-stakes scale: a state that lowers its bar, grades leniently or drops an exit exam does not move it, whereas within-school or grade-year-standardized designs absorb such statewide shifts.
- None of those mechanisms moves with the shares: NAEP-equivalent proficiency cut scores are unrelated to them (lower 95% bounds -7 to -13 points per 10 points of share, against a national rise of 15-20 points in 2015); the 11 states that dropped exit exams had no higher or faster-rising shares than the 13 that kept them.
- The English-learner estimate fades with region-by-year effects or state trends; grade 4 against its own cohort's kindergarten-grade 1 share gives -0.070 (0.030), which holds with region-by-year effects and has no lead.
- A level effect already in place by 2003, or a national shift, is absorbed by the fixed effects and not identified.
""", """
VALID. Survived review: the mechanism checks and the fixed-effects limits are stated; a later within-district design
neither confirms nor contradicts the state-level reading.
""", "", """
Ladder entry 248 (NAEP school test, 2026-09-28) and its later brackets; lane naep school test. Passed cross-lab review.
""")

case("V02", "VALID", "E", "original", None, "irskey", """
CLAIM: Scored on IRS tax year 2023, a year that no step of it used, the account's income-tax key misallocates tax across income bins. With the bins from $1M pooled, it misses IRS's distribution of income tax after credits by 8.4 percentage points of total variation: 8.4pp too much of the tax at $200k-$1M, where the Mexican-origin group's share of people is 2-4%, and 3.3pp too little at $50k-$200k, where it is 6-12%. Matching IRS's bin totals while keeping the group's within-bin shares raises the group's federal income tax by $3.2bn (SE 1.3) and lowers the net cost from $321.8bn to $318.6bn at the low end. A candidate for the next case, not adopted.

EVIDENCE:
- The key allocates national income tax to people using CPS incomes and a CBO rate gradient. IRS publishes only national totals by adjusted-gross-income bin, with no nativity; the group's share inside each bin stays the CPS's.
- Frozen IRS 2022 shares miss 2023 by 2.4pp. The key scores worse against 2022 (10.3pp), the year the gradient rests on, so the held-out year shows no overfitting.
- The unpooled 19-bin reading turns on 33 records above $1.5M, none in the group, and is not used; tax above $3.1M is outside the CPS (top-coding).
- Pooling from $500k gives +$3.1bn (SE 0.5), leaning less on the 15 group records above $1M.
""", """
VALID. Survived cross-lab review after its wording was narrowed to 'only the national totals by bin are IRS; the
group's within-bin share stays the CPS's', which the packet states.
""", "", """
Ladder entry 249 (held-out tax key); lane tax_key_heldout_2026_09_28 (aec08a4); bracket after cross-lab review f41ca76.
""")

case("V03", "VALID", "E", "original", None, "ssi", """
CLAIM: A blind back-test of the account's dollar keys against state administrative totals gives no reason to correct the SSI key. Against SSA's federally administered SSI payments by state, the estimated correction is delta = +0.96 (the Mexican-origin group's SSI would be 96% higher than the key assigns). But that target includes the state supplementary payments SSA administers for some states, chiefly California's $3.26bn, which the account's SSI line (federal SSI only) does not pay, and the group is concentrated in California. Against federal SSI alone, a comparison chosen after the data were seen, delta = +0.17 (+$0.80bn). No key correction follows.

EVIDENCE:
- Predictions, baselines and tolerances were committed before any target was opened; scoring used the frozen estimators.
- State totals give the dollar keys little power, because take-up and error rates vary by state more than the group's share does: refundable credits delta +0.09 (+$1.6bn, 95% interval about -$5 to +8bn); Social Security delta -0.01.
- The same frame predicts where births land: births to Mexican-origin mothers are 14.43% of US births in the frame against 14.36% in birth records.
""", """
VALID. The target-definition mismatch is real (the federally administered total includes state supplements the
line does not pay); the post-hoc federal-only comparison is labeled as such.
""", "", """
Ladder entry 255 (back-test against administrative totals) with its cross-lab bracket; lane backtest_admin_totals_2026_09_28.
""")

case("V04", "VALID", "R", "original", None, "s10", """
CLAIM: A blind test against hospital cost reports (Medicare Worksheet S-10, FY2023) supports the account's uncompensated-care key, which charges the Mexican-origin group by its uninsured exposure: the key's predicted state shares of hospitals' charity care and bad debt sit at a total variation distance of 0.134 from the reports, against 0.210 for a population key. The national S-10 total is $43.0bn against the account's $48.9bn input (0.88).

EVIDENCE:
- Predictions and the scoring rule were committed before the reports were opened.
- A slope test, expected to have no power, favors lower use by the uninsured (0.7 times; slope -0.60, 95% interval -1.14 to -0.07); region controls added after the data were seen take the slope to -0.11, so it cannot separate a regional factor from the group's use. It is a candidate, not adopted.
- S-10 line 30 includes insured patients' charity care and bad debt.
- A plain count of the uninsured scores 0.126, so the person-year key does no better than it.
""", """
VALID. Survived cross-lab review; the non-blind and post-hoc parts are labeled; the claim is limited to the state
distribution.
""", "", """
Ladder entry 256 (back-test against published figures, check 1); lane backtest_published_2026_09_28.
""")

case("V05", "VALID", "R", "original", None, "school", """
CLAIM: The present value of lifetime earnings lost by incumbent pupils because of one school year's exposure to crowded classrooms can be booked as a one-year social-cost accrual in an annual account. This is not a stock/flow error, provided it is labeled as an accrual, kept separate from budget cash flows, and its future-tax consequence is not added a second time.

EVIDENCE:
- The annual account books each year's exposure once: the loss caused by 2024's exposure is the present value, at 2024, of the earnings reduction it causes over the pupils' working lives.
- Each year's exposure is a new flow; next year's exposure is booked next year. A pupil's harm over 13 school years is the sum of 13 annual accruals, not 13 lifetimes.
- The future income-tax loss from the lower earnings is excluded from the fiscal line and appears only inside the social accrual.
""", """
VALID. The conceptual audit rejected the stock/flow objection explicitly ('It is not automatically a stock/flow
error'), with the same three conditions.
""", "", """
research/immigration-weekly-conceptual-audit-2026-09-25.md section 3, 'One tempting objection should be rejected'.
""")

case("V06", "VALID", "R", "original", None, "crimeprice", """
CLAIM: The account can add a victim-harm line for crimes by the Mexican-origin group's members against other residents ($4.5bn a year tangible, $28.9bn with quality of life) to its fiscal line for police, courts and corrections without double counting, because the victim line uses victim-only unit costs.

EVIDENCE:
- Victim-only unit costs cover medical care, lost productivity, property loss and damage, and the victim's pain, suffering and risk of death. Criminal-justice system costs (police, adjudication, corrections) are excluded from them.
- Police, courts and corrections spending enters the fiscal account through the justice budget lines, allocated by use.
- Deaths are counted once: the assault and robbery unit costs used here exclude the risk-of-homicide component, and homicides are priced in their own row.
""", """
VALID. The conceptual audit lists 'victim-only crime prices preserve the separation from justice spending' among
objections that did not survive.
""", "", """
research/immigration-weekly-conceptual-audit-2026-09-25.md, 'Objections that did not survive'; lane
crime_victim_cost_2026_09_23 ($4.5bn/$28.9bn).
""")

case("V07", "VALID", "R", "original", None, "winners", """
CLAIM: In these incidence scenarios only a minority of other residents gain from the Mexican-origin group's presence. Across the wage model's substitution elasticities 1.5, 2.0 and 2.5, the share of other residents who come out ahead (pooled within households, taxes financed in proportion to tax shares) is 29.2%, 23.9% and 18.7%. The result is conditional on how channel totals are allocated to people.

EVIDENCE:
- Channel totals (wages, prices, taxes, public services) are allocated onto survey people; a winner is a person whose net is positive.
- The wage channel's gross after-tax gains ($95.8bn) and losses ($96.0bn) almost cancel, so the count is sensitive to the wage allocation: halving each person's wage deviation from the mean, with the aggregate unchanged, gives 10.3% winners.
- Enumerating the existing matched channel choices gives a maximum of 30.5% winners.
""", """
VALID. The conceptual audit's 'What survives' for section 2: the inspected alternatives still yield a minority of
winners; the finding should be 'a minority in these incidence scenarios', as stated here.
""", "", """
research/immigration-weekly-conceptual-audit-2026-09-25.md section 2 table and 'What survives'.
""")

case("V08", "VALID", "R", "original", None, "census", """
CLAIM: The data do not show each Mexican arrival cohort more positively selected on custody than the last. The 2000 census's low institutional share for recent Mexican arrivals (0.13 of US-born men's) reflects the census's birthplace allocation, not selection: spreading the allocated birthplaces in the reported mix raises the 2000 ratios 2.1-2.6-fold, and the same men reappear at 0.49-0.51 in the 2006 American Community Survey.

EVIDENCE:
- 2000 census: birthplace allocated for 68% of institutionalized Mexican-origin men aged 18-40, 98% of them assigned a US birthplace; among those reporting a birthplace, 38.5% were foreign-born.
- The 2000 census count of institutionalized noncitizens (73,395, all institution types) is below the 89,676 noncitizens the Bureau of Justice Statistics counted in state and federal prisons alone at midyear 2000.
- ACS at 6-10 years in the US: successive cohorts stand at 0.53, 0.58 and 0.61 (2006-19).
- This measures custody, not crime; the allocation correction is a sensitivity without standard errors.
""", """
VALID. Confirmed by an external count check (BJS prison counts); the ratio correction is labeled a sensitivity.
""", "", """
Ladder entry 196 with its external-check bracket; lane crime_selection_cohorts_2026_09_23.
""")

case("V09", "VALID", "R", "original", None, "cpsincome", """
CLAIM: The Mexican-origin earnings gaps that drive the account's tax term replicate on a second survey. Common-age wage gaps per standardized person against native non-Hispanic whites: Mexico-born -$17,241 on the ACS 2024 against -$17,518 on the CPS ASEC; US-born Mexican-origin -$9,473 against -$9,208 (ratios 0.98 and 1.03).

EVIDENCE:
- Same estimator on both surveys: wage and salary income of persons 18-64, standardized to a common age distribution, survey weights.
- Mexican origin: self-identified Mexican origin; Mexico-born and US-born split by birthplace.
- The two surveys ask about income differently and fill in missing answers separately, so agreement is a replication across instruments, not a validation against tax records.
""", """
VALID. A replication across instruments, stated as such.
""", "", """
Ladder entry 127 (earnings gaps replicate on ACS 2024).
""")

case("V10", "VALID", "E", "original", None, "crash", """
CLAIM: Charged with against without the Mexican-origin group's traffic, road crashes cost other residents $11.1bn a year (range -$57.7bn to +$74.3bn), not the $42.3bn charged by fault. Across transferable evidence, one more car on a fixed network barely changes other drivers' crash risk per mile: the cost-weighted elasticity of the non-fatal crash rate to traffic is about +0.07 (p10-p90 -0.23 to +0.52), and of the fatal rate -0.21. Near zero elasticity, the crashes other residents have with the group's drivers would largely happen anyway without the group, as crashes among themselves on emptier roads.

EVIDENCE:
- With-against-without = other residents' crash costs with the group's traffic minus without it; it includes a composition term for the group's higher fatal culpability ($1.8bn). Each 0.1 of non-fatal elasticity adds about $5.4bn.
- Study weights (design; a 0.65 weight on congested settings, from the group's commute exposure) were set before the results; leaving out one study at a time keeps the non-fatal central between -0.10 and +0.31.
- In dense traffic the studies disagree on sign (London: +1.4 against -0.36 for injury crashes), which is why the range crosses zero.
""", """
VALID. Adopted after the lead verified the key sources; reruns identical; the range is carried with the figure.
""", "", """
Ladder entry 266; decisions/2026-09-29-crash-item-with-against-without.md; lanes crash_volume_elasticity_2026_09_28,
road_crash_externality_2026_09_28.
""")

case("V11", "VALID", "E", "original", None, "meps", """
CLAIM: On the medical expenditure survey file the account transports medical costs from, people of Mexican origin draw less public medical money per person than the all-donor mean of their own age x US-birth cell: 0.89 at 65+ (SE 0.15, 95% CI 0.61-1.18), 0.69 at 18-64 (SE 0.10, interval excludes 1) and 0.76 across all ages. The transport, which assigns each cell's all-donor mean, therefore overstates the group's public medical spending at working ages.

EVIDENCE:
- Public medical money = Medicare + Medicaid + other public payers, per person-year, pooled survey years, survey weights, replicate-weight SEs.
- Cells: age band x US-born/foreign-born; donors are all persons in the cell.
- At 65+ the interval includes 1, so no correction is claimed there.
""", """
VALID. A measured ratio on the transport's own file, with the 65+ limit stated.
""", "", """
Ladder entry 175 (MEPS medical by ethnicity); commit 6ed7d57.
""")

case("V12", "VALID", "E", "original", None, "cpspop", """
CLAIM: The CPS has put the Mexico-born population 9-13% above the ACS every year since 2019. About 11.1M, not the CPS's 12.2M, is the right level for early 2025.

EVIDENCE:
- The excess appears in every monthly CPS file from January 2024 (2024 mean 12.38M) and in the March basic sample alone (12.05M), so it is neither the ASEC oversample nor the January 2025 population controls.
- It is composition inside the Hispanic control: in 2024 the CPS counted fewer Hispanics than the ACS in total but 1.38M more Mexico-born and 1.81M fewer other Hispanics, and CPS state weighting controls Hispanic origin only nationally.
- The two surveys agreed within 4% from 2006 to 2016.
- The whole ASEC 2025 excess (1.16M against the ACS 2024 in the same universe) lies outside California and Texas, and 76% of it is noncitizen.
""", """
VALID. Adopted: later cases re-key population-based lines to the corrected share.
""", "", """
Ladder entry 209; entry 239 (enterprise receipt re-keyed to the corrected population share 0.1172).
""")

# ---------------------------------------------------------------- VALID mirrors (synthetic)

case("V01m", "VALID", "R", "mirror", "V01", "school", """
CLAIM: On state NAEP, white pupils lost ground where the Hispanic or immigrant-origin share of pupils rose: -0.087 SD (SE 0.027) and -0.061 SD (0.026) per 10 points of share, 2003-2019, 51 states, state and year fixed effects. The English-learner share gives -0.035 (0.018). If causal, the Hispanic-share estimate is about $11bn of lifetime earnings per cohort of white pupils at the observed national rise in that share (19% to 27%).

EVIDENCE:
- NAEP is an absolute, low-stakes scale: a state that lowers its bar, grades leniently or drops an exit exam does not move it, whereas within-school or grade-year-standardized designs absorb such statewide shifts.
- None of those mechanisms moves with the shares: NAEP-equivalent proficiency cut scores are unrelated to them (95% bounds -7 to +6 points per 10 points of share); the 11 states that dropped exit exams had no higher or faster-rising shares than the 13 that kept them.
- The Hispanic-share estimate holds with region-by-year effects (-0.071, SE 0.030) and state trends (-0.064, 0.033); grade 4 against its own cohort's kindergarten-grade 1 share gives -0.080 (0.031) and has no lead.
- A level effect already in place by 2003, or a national shift, is absorbed by the fixed effects and not identified.
""", """
VALID (by construction): same design, checks and stated limits as V01, direction reversed; the dollar figure is
conditional ('if causal').
""", "", "Synthetic mirror of V01.")

case("V02m", "VALID", "R", "mirror", "V02", "irskey", """
CLAIM: Scored on IRS tax year 2023, a year that no step of it used, the account's income-tax key misallocates tax across income bins. With the bins from $1M pooled, it misses IRS's distribution of income tax after credits by 8.4 percentage points of total variation: 8.4pp too much of the tax at $50k-$200k, where the Mexican-origin group's share of people is 6-12%, and 3.3pp too little at $200k-$1M, where it is 2-4%. Matching IRS's bin totals while keeping the group's within-bin shares lowers the group's federal income tax by $3.2bn (SE 1.3) and raises the net cost from $321.8bn to $325.0bn at the low end. A candidate for the next case, not adopted.

EVIDENCE:
- The key allocates national income tax to people using CPS incomes and a CBO rate gradient. IRS publishes only national totals by adjusted-gross-income bin, with no nativity; the group's share inside each bin stays the CPS's.
- Frozen IRS 2022 shares miss 2023 by 2.4pp. The key scores worse against 2022 (10.3pp), the year the gradient rests on, so the held-out year shows no overfitting.
- The unpooled 19-bin reading turns on 33 records above $1.5M, none in the group, and is not used; tax above $3.1M is outside the CPS (top-coding).
- Pooling from $500k gives -$3.1bn (SE 0.5), leaning less on the 15 group records above $1M.
""", """
VALID (by construction): same held-out test as V02 with the misallocation reversed; numbers consistent.
""", "", "Synthetic mirror of V02.")

case("V03m", "VALID", "R", "mirror", "V03", "ssi", """
CLAIM: A blind back-test of the account's dollar keys against state administrative totals gives no reason to correct the SSI key. Against SSA's federal SSI payments by state, the estimated correction is delta = -0.48 (the Mexican-origin group's SSI would be 48% lower than the key assigns). But the account's SSI line pays federal SSI plus the state supplementary payments SSA administers for some states, chiefly California's $3.26bn, while this target table covers federal payments only, and the group is concentrated in California. Against the federally administered total including supplements, a comparison chosen after the data were seen, delta = -0.08 (-$0.40bn). No key correction follows.

EVIDENCE:
- Predictions, baselines and tolerances were committed before any target was opened; scoring used the frozen estimators.
- State totals give the dollar keys little power, because take-up and error rates vary by state more than the group's share does: refundable credits delta -0.09 (-$1.6bn, 95% interval about -$8 to +5bn); Social Security delta +0.01.
- The same frame predicts where births land: births to Mexican-origin mothers are 14.43% of US births in the frame against 14.36% in birth records.
""", """
VALID (by construction): the same target-definition mismatch as V03 in the opposite direction; the post-hoc
comparison is labeled.
""", "", "Synthetic mirror of V03.")

case("V04m", "VALID", "E", "mirror", "V04", "s10", """
CLAIM: A blind test against hospital cost reports (Medicare Worksheet S-10, FY2023) favors a population key over the account's uncompensated-care key, which charges the Mexican-origin group by its uninsured exposure: the uninsured key's predicted state shares of hospitals' charity care and bad debt sit at a total variation distance of 0.210 from the reports, against 0.134 for a population key. Switching keys would lower the group's charge; it is a candidate, not adopted.

EVIDENCE:
- Predictions and the scoring rule were committed before the reports were opened.
- A slope test, expected to have no power, favors lower use by the uninsured (0.7 times; slope -0.60, 95% interval -1.14 to -0.07); region controls added after the data were seen take the slope to -0.11, so it cannot separate a regional factor from the group's use.
- S-10 line 30 includes insured patients' charity care and bad debt.
- The national S-10 total is $43.0bn against the account's $48.9bn input (0.88).
""", """
VALID (by construction): same blind test as V04 with the distances reversed; post-hoc parts labeled; not adopted.
""", "", "Synthetic mirror of V04.")

case("V05m", "VALID", "E", "mirror", "V05", "school", """
CLAIM: The present value of lifetime earnings gained by incumbent pupils because of one school year's exposure to bilingual classmates can be booked as a one-year social-benefit accrual in an annual account. This is not a stock/flow error, provided it is labeled as an accrual, kept separate from budget cash flows, and its future-tax consequence is not added a second time.

EVIDENCE:
- The annual account books each year's exposure once: the gain caused by 2024's exposure is the present value, at 2024, of the earnings increase it causes over the pupils' working lives.
- Each year's exposure is a new flow; next year's exposure is booked next year. A pupil's gain over 13 school years is the sum of 13 annual accruals, not 13 lifetimes.
- The future income-tax gain from the higher earnings is excluded from the fiscal line and appears only inside the social accrual.
""", """
VALID (by construction): the same accrual logic as V05 applied to a benefit.
""", "", "Synthetic mirror of V05.")

case("V06m", "VALID", "E", "mirror", "V06", "crimeprice", """
CLAIM: The account can add a consumer-price benefit from the Mexican-origin group's labour (lower prices paid by other residents, $9.4bn a year) to its fiscal receipts line without double counting, because the price line counts only other residents' consumer savings.

EVIDENCE:
- The price benefit is the fall in prices in industries employing the group, applied to other residents' consumption bundles; the group's own consumption is excluded.
- Firms' higher profits are excluded from the price benefit; the taxes on those profits enter the fiscal account through the receipts lines, allocated by incidence.
- Wage effects on other residents are priced in a separate wage line; the price line uses only the price change, not the wage change that caused it.
""", """
VALID (by construction): two lines with a clean boundary, as in V06, defending a benefit instead of a cost.
""", "", "Synthetic mirror of V06.")

case("V07m", "VALID", "E", "mirror", "V07", "winners", """
CLAIM: In these incidence scenarios only a minority of other residents lose from the Mexican-origin group's presence. Across the wage model's substitution elasticities 1.5, 2.0 and 2.5, the share of other residents who come out ahead (pooled within households, taxes financed in proportion to tax shares) is 70.8%, 76.1% and 81.3%. The result is conditional on how channel totals are allocated to people.

EVIDENCE:
- Channel totals (wages, prices, taxes, public services) are allocated onto survey people; a winner is a person whose net is positive.
- The wage channel's gross after-tax gains ($96.0bn) and losses ($95.8bn) almost cancel, so the count is sensitive to the wage allocation: halving each person's wage deviation from the mean, with the aggregate unchanged, gives 89.7% winners.
- Enumerating the existing matched channel choices gives a minimum of 69.5% winners.
""", """
VALID (by construction): same conditional, sensitivity-bounded claim as V07 with the shares reversed.
""", "", "Synthetic mirror of V07.")

case("V08m", "VALID", "E", "mirror", "V08", "census", """
CLAIM: The data do not show each Mexican arrival cohort more negatively selected on custody than the last. Round 3's high institutional share for recent Mexican arrivals (1.10 of native-born men's) reflects the census's birthplace allocation, not selection: spreading the allocated birthplaces in the reported mix lowers the round-3 ratios 2.1-2.6-fold, and the same men reappear at 0.49-0.51 in a later annual survey.

EVIDENCE:
- Round 3: birthplace allocated for 64% of institutionalized Mexican-origin men aged 18-40, 91% of them assigned a foreign birthplace; among those reporting a birthplace, 38.5% were foreign-born.
- The round-3 count of institutionalized noncitizens is above the number of noncitizens the prison statistics agency counted in all prisons, jails and immigration detention at the same date.
- Annual survey at 6-10 years in the country: successive cohorts stand at 0.53, 0.58 and 0.61.
- This measures custody, not crime; the allocation correction is a sensitivity without standard errors.
""", """
VALID (by construction): the same allocation correction as V08 in the opposite direction.
""", "", "Synthetic mirror of V08 (census de-identified, as in E07m).")

case("V09m", "VALID", "E", "mirror", "V09", "cpsincome", """
CLAIM: The Mexican-origin earnings gaps that drive the account's tax term are small, and they replicate on a second survey. Common-age wage gaps per standardized person against native non-Hispanic whites: Mexico-born -$6,241 on the ACS 2024 against -$6,518 on the CPS ASEC; US-born Mexican-origin -$1,473 against -$1,408 (ratios 0.96 and 1.05).

EVIDENCE:
- Same estimator on both surveys: wage and salary income of persons 18-64, standardized to a common age distribution, survey weights.
- Mexican origin: self-identified Mexican origin; Mexico-born and US-born split by birthplace.
- The two surveys ask about income differently and fill in missing answers separately, so agreement is a replication across instruments, not a validation against tax records.
""", """
VALID (by construction): same replication as V09 with smaller gaps.
""", "", "Synthetic mirror of V09.")

case("V10m", "VALID", "R", "mirror", "V10", "crash", """
CLAIM: Charged with against without the Mexican-origin group's traffic, road crashes cost other residents $72.1bn a year (range $49.4bn to $94.7bn), not the $42.3bn charged by fault. Across transferable evidence, one more car on a fixed network raises other drivers' crash risk per mile: the cost-weighted elasticity of the non-fatal crash rate to traffic is about +1.20 (p10-p90 +0.78 to +1.62), and of the fatal rate -0.21. With a large elasticity, the group's traffic also raises crashes among other residents themselves, which fault attribution does not count.

EVIDENCE:
- With-against-without = other residents' crash costs with the group's traffic minus without it; it includes a composition term for the group's higher fatal culpability ($1.8bn). Each 0.1 of non-fatal elasticity adds about $5.4bn.
- Study weights (design; a 0.65 weight on congested settings, from the group's commute exposure) were set before the results; leaving out one study at a time keeps the non-fatal central between +1.02 and +1.39.
- In the densest settings the studies differ in size (London: +1.4 against +0.9 for injury crashes), which is why the range is wide.
""", """
VALID (by construction): the same with-against-without frame as V10 with a large elasticity; numbers consistent
(11.1 + (1.20 - 0.07) x 54 = 72.1).
""", "", "Synthetic mirror of V10.")

case("V11m", "VALID", "R", "mirror", "V11", "meps", """
CLAIM: On the medical expenditure survey file the account transports medical costs from, people of Mexican origin draw more public medical money per person than the all-donor mean of their own age x US-birth cell: 1.12 at 65+ (SE 0.15, 95% CI 0.83-1.41), 1.31 at 18-64 (SE 0.10, interval excludes 1) and 1.24 across all ages. The transport, which assigns each cell's all-donor mean, therefore understates the group's public medical spending at working ages.

EVIDENCE:
- Public medical money = Medicare + Medicaid + other public payers, per person-year, pooled survey years, survey weights, replicate-weight SEs.
- Cells: age band x US-born/foreign-born; donors are all persons in the cell.
- At 65+ the interval includes 1, so no correction is claimed there.
""", """
VALID (by construction): same measurement as V11 with the ratios above 1.
""", "", "Synthetic mirror of V11.")

case("V12m", "VALID", "R", "mirror", "V12", "cpspop", """
CLAIM: The CPS has put the Mexico-born population 9-13% below the ACS every year since 2019. About 13.4M, not the CPS's 12.2M, is the right level for early 2025.

EVIDENCE:
- The shortfall appears in every monthly CPS file from January 2024 (2024 mean 12.02M) and in the March basic sample alone (12.10M), so it is neither the ASEC oversample nor the January 2025 population controls.
- It is composition inside the Hispanic control: in 2024 the CPS counted more Hispanics than the ACS in total but 1.22M fewer Mexico-born and 1.51M more other Hispanics, and CPS state weighting controls Hispanic origin only nationally.
- The two surveys agreed within 4% from 2006 to 2016.
- The whole ASEC 2025 shortfall (1.19M against the ACS 2024 in the same universe) lies outside California and Texas, and 76% of it is noncitizen.
""", """
VALID (by construction): same evidence structure as V12 with the gap reversed.
""", "", "Synthetic mirror of V12.")

# ---------------------------------------------------------------- checks and output

FORBIDDEN = re.compile(r"ladder|supersed|\bfixed\b(?! (effects|network))|2026|withdrawn|\bentry \d|\b[0-9a-f]{7,40}\b", re.I)


def main():
    ids = [c["id"] for c in C]
    assert len(ids) == len(set(ids)) == 48, len(ids)
    for c in C:
        words = len(c["packet_text"].split())
        assert words <= 400, (c["id"], words)
        hit = FORBIDDEN.search(c["packet_text"])
        assert not hit, (c["id"], hit.group(0))
        if c["origin"] == "mirror":
            orig = next(o for o in C if o["id"] == c["mirror_of"])
            assert orig["type"] == c["type"] and orig["direction"] != c["direction"], c["id"]
            assert orig["topic"] == c["topic"], c["id"]
    for typ in ("ERROR", "VALID"):
        for d in ("R", "E"):
            for origin in ("original", "mirror"):
                n = sum(1 for c in C if c["type"] == typ and c["direction"] == d and c["origin"] == origin)
                assert n == 6, (typ, d, origin, n)
    OUT.mkdir(exist_ok=True)
    for c in C:
        (OUT / f"{c['id']}.json").write_text(json.dumps(c, indent=1, ensure_ascii=False) + "\n")
    print(f"wrote {len(C)} cases; max words {max(len(c['packet_text'].split()) for c in C)}")


if __name__ == "__main__":
    main()
