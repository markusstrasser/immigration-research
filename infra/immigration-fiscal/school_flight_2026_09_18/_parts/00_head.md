claude-opus-5[1m]

**Verdict:** NOT REPRODUCED in modern US data. Betts & Fairlie's one-native-per-four-immigrants
holds up as a citation — the phrase is verbatim in their abstract, for secondary school, from
1980–1990 Census data — but nothing like it survives in 2008–2023 metro data. The raw count
specification gives about **one US-born non-Hispanic white child into private school per ten
Hispanic children added to the public schools**, and that estimate **reverses to −0.12 to −0.14
once the metro's total enrolment growth is controlled**: it was measuring population growth, not
substitution. The share specification is **not significant at any level** on the full 334-metro
panel (+0.154, SE 0.095 elementary; +0.078, SE 0.073 secondary), the **foreign-born** share
carries a *negative* coefficient, and the part of the Hispanic share that predicts anything is the
**US-born second generation**, not immigrant arrival — the opposite of Betts & Fairlie's
non-English-speaking mechanism. Nationally the private share *fell* from 11.7% to 10.0% while the
Hispanic share of public enrolment rose from 16.4% to 28.9%.

The public-goods response is real but confined to one margin. Within a state and year, a district
whose Hispanic share rises loses **$447 of local revenue per pupil per 10 points** (SE $69) and
**$369 of property-tax revenue**, with local tax effort down 6.5% of its mean; **state aid offsets
about 60%**, and total revenue and per-pupil spending are statistically unchanged. Poterba's
elderly-share direction does not appear at all, the fractionalisation index gives the opposite sign
to the Hispanic share on local revenue, and in 2,954 California school tax measures higher-Hispanic
districts vote *more* for bonds, not less.

On the accounting: a switch raises measured GDP in the short run by roughly the tuition, and
**lowers** it in the long run, because average private tuition ($12,790 in 2021-22) is about
three-quarters of average public current spending per pupil ($17,846 in FY2024). The tuition is a
real resource cost borne by the family; the lost state aid is a transfer between districts; local
property tax does not move; the only fresh real costs are duplicated capacity and — if the child's
outcomes do not improve — the defensive-expenditure deadweight. In the one clean US randomised
evaluation, switching produced two years of significantly *worse* maths and no reading gain.

Scaled honestly, the point estimates imply about **156,000** white native children moved into
private school across 334 metros over 2008–2023, some $2.0bn of tuition and $1.5bn of state aid
reallocated — but the underlying coefficient is insignificant, so the interval spans zero, and the
same period saw national private enrolment fall by about 450,000 for unrelated reasons.

# School flight, the public-goods response, and what a private-school switch does to the accounts

Lane `infra/immigration-fiscal/school_flight_2026_09_18/`. Agent dispatched 2026-09-18.
Provenance tags: [SOURCE: …] [DATA] [INFERENCE] [TRAINING-DATA] [UNVERIFIED] [GAP]
[FRAMING-SENSITIVE].

Three linked questions the repo has not measured:
1. Does the native private-school share rise when the Hispanic / foreign-born share of
   schoolchildren rises?
2. Does per-pupil spending, local tax effort, or bond support fall as districts become
   more ethnically heterogeneous?
3. When a native family moves a child to private school, what is a real resource cost,
   what is a transfer, and does the tuition buy a measurable outcome gain?

**Data quality note.** Two defects were found and fixed during the build, both recorded
because they changed results. The Census PUMS endpoint returned records outside the
requested age range for California 2010, inflating that state-year 13-fold; every
state-year is now audited against its own cross-year median (`audit_kids.py`,
`derived/kids_audit.csv`, 257 state-years, all inside ±25% after the fix). And the metro
panel initially grouped on state as well as metro, splitting every multi-state metro and
dropping it from the balanced panel; §5.7 reports how much that changed the estimate.

---
