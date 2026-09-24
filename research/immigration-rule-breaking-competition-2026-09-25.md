# Do rule-breaking employers drive honest firms out?

**Verdict:** Breaking labor and tax rules gives an employer a real cost edge, but its measured
size is a few billion dollars a year, and nothing measured here shows it driving compliant firms
out of business. Paying a worker off the books saves 11–12% of the wage in legally required costs,
or 11–24% once the worker's kept payroll tax and typical underpayment are counted. In construction,
landscaping, janitorial services and restaurants the edge comes to $0–14.8bn in 2024 (central
$6.4bn), and $4.5bn of the central figure is payroll tax that the adopted account already counts.
Covered establishments and employment grew no slower where the group's share grew, and the one
negative association disappears once state-wide shocks are removed. [CALCULATION:
[compliance lane](../infra/immigration-fiscal/compliance_gap_2026_09_24/RESULT.md); ladder 220]

The question is the operator's: whether illegal immigrants' businesses, "not needing the same
scruples", drive honest businesses out. "Driving out" is measured here as covered firms'
establishment counts, employment and pay. A compliant firm could also lose share of jobs it would
otherwise do without any change in those counts, and that is not measured. [FRAMING-SENSITIVE]

## 1. The edge per dollar and in dollars

The employer's legally required costs come from BLS ECEC Table 4 (June 2026): 12.2% of wages in
construction, 10.7% in administrative and waste services, 11.2% in accommodation and food, 10.4% in
all private industry. The worker's own 7.65% can be kept by paying a lower cash wage (none, half or
all of it), and underpayment runs from none to twice the Wage and Hour Division's (WHD) recovered
depth. The construction edge of 12–23% of the off-books wage matches two union-commissioned
construction studies that are not immigrant-specific: Ormiston–Belman–Erlich (2020), 12.5–23.5% of
legal labor cost, and Belman, Bilginsoy, Ormiston & Wenz (ICERES 2025), 16.1% on one Michigan
project. [SOURCE: lane `reads/LIT_COMPLIANCE_COSTS.md` §3b; CALCULATION: lane `edges.py` →
`derived/edges_by_industry.csv`]

| 2024, four industries | Low | Central | High |
|---|---:|---:|---:|
| Off-books pay, $bn | 30.1 | 37.1 | 64.5 |
| Off-books workers, m | 0.74 | 0.96 | 1.72 |
| Edge, $bn | 3.6 | 6.4 | 14.8 |
| of which payroll taxes | 2.5 | 4.5 | 10.3 |
| of which workers' compensation (with federal unemployment tax) | 1.1 | 1.3 | 2.2 |
| of which underpayment | 0.0 | 0.6 | 2.3 |

Off-books pay is the cross-state slope (§2) times the group's ACS wage bill; the low and high ends
are the smallest and largest of the slope's four variants. The national level check (§2) allows
zero, so the ledger rows run from $0. Agriculture and private households are not priced.
[CALCULATION: lane `derived/edges_totals.csv`]

Enforcement records confirm the edge exists but see little of it. WHD back wages are 0.001–0.017%
of covered payroll in the focus industries, and OSHA penalties at most 0.026%. The WHD portal file
holds about half of DOL's published action count, so these are floors; scaled to the published
totals, recoveries stay under 0.02% of payroll. The 2008 three-city survey of low-wage workers
(Bernhardt et al. 2009) found minimum-wage violations for 15.6% of US-born, 21.3% of authorized
immigrant and 37.1% of unauthorized workers, so the edge is taken wherever low-wage labor is.
[DATA: lane `derived/enforcement_by_cell.csv`, `whd_gate.csv`; SOURCE: Bernhardt et al., Table 5.1, p. 46]

The group's own businesses: in 2024 the ACS counts 239,000 imputed-unauthorized unincorporated
self-employed in construction (15.0% of the industry's 1.59m) and 12–20% shares in landscaping,
janitorial, restaurants and private households. Their income falls in the IRS category where 57% of
nonfarm proprietor income goes unreported (Publication 1415, Table 5). That tax loss is inside the
adopted account through the September 24 tax correction and is not priced again.

## 2. How much work is off the books

Wage work that the ACS sees but unemployment-insurance payrolls (QCEW) miss rises, across states,
by about 0.6 of a worker per imputed-unauthorized worker in construction (SE 0.10; 0.54 without
California and Texas, 0.88 within states over time), landscaping (0.59) and janitorial services
(0.74). Restaurants show nothing across states (0.01, SE 0.17) but 0.59 within states over time.
Temporary-help employment does not rise with construction's group share (−0.18, SE 0.51), so the
slope is not agency workers coded to construction. [CALCULATION: lane `uncovered.py` →
`derived/uncovered_slopes.csv`, all 68 specifications in the lane RESULT]

The level check disagrees. Calibrated on six low-immigrant industries, construction's national
uncovered share averaged 3.0% in 2012–2023 and was −2.2% in 2024, while the slope implies 8.1% of
the industry's wage workers are the group off the books. The calibration may misstate
construction's definitional gap, or the slope may pick up other informal workers or state-varying
ACS–QCEW differences; these data cannot settle it.

The pooled slope without agriculture implies about 0.38 of the group's wage workers on the books
by head count. SSA's 2010 count had 44% of unauthorized workers paying payroll tax, and the account
uses 0.52 by dollars (range 0.42–0.63). Test B brackets the account's on-books share and gives no
grounds to move it. [SOURCE: SSA Actuarial Note 151, as read in
`../infra/immigration-fiscal/onbooks_share_2026_09_23/RESULT.md`]

## 3. Do compliant firms lose ground?

Two tests were pre-registered before any outcome regression ran.

- **State E-Verify mandates** (Arizona and Mississippi 2008, South Carolina, Alabama and Georgia
  2012, North Carolina 2013), stacked triple differences on exposed against low-exposure
  industries. The design is not identified: establishments and employment in exposed industries
  of mandate states were already sliding relative to controls four years before the mandates
  (pre-trend p < 0.001), through the housing bust, and kept sliding at the same pace. The uncovered
  share did not move (+0.0005, SE 0.014) in any variant.
- **Panel associations, 2012–2023**, with state-year and industry-year fixed effects. With the
  group's share measured from the ACS alone (so that it does not contain QCEW employment), covered
  establishments and employment show no negative association: lagged imputed-unauthorized share
  +0.09 (SE 0.07) and +0.09 (0.06); long differences +0.37 (0.44) and +0.46 (0.38).
  Specialty-trade establishments fell with the lagged Mexico-born noncitizen share on year effects
  alone (−0.17 to −0.26), but net of the same state's low-exposure industries the coefficients are
  −0.09 to +0.11 and none is significant (a check added after the first results were seen).
  Pooled wage associations lean negative (−0.29, SE 0.10, long difference), but per industry,
  across states, they are zero or positive (construction +0.41, janitorial +0.37, restaurants
  +0.27, landscaping −0.01), so they are not robust.

[CALCULATION: lane `everify.py` → `derived/everify_*.csv`; `panel_c.py` → `derived/panel_c.csv`;
`composition.py` → `derived/composition_check.csv`]

The literature points the same way:

- The one firm-level test (Brown, Hotchkiss & Quispe-Agnoli, Georgia UI records 1995–2005) finds
  that firms hiring undocumented workers survive better, and that rivals' undocumented hiring does
  not significantly raise exit in construction (0.492, SE 0.516), agriculture or leisure and
  hospitality. It does raise exit in 4 of 12 sectors, including manufacturing and finance.
- Arizona's 2008 mandate roughly doubled likely-unauthorized men's self-employment (+8.3 points;
  Bohn & Lofstrom), so enforcement pushed work toward the least compliant segment, and it did not
  improve competing low-skilled natives' outcomes (Bohn, Lofstrom & Raphael).
- Police-based removals lowered local business counts rather than letting compliant firms take
  over: Secure Communities −3.4% firms (Shrestha & Sant'Anna 2026 WP); 287(g) −6% businesses per
  1,000 residents, with significant pre-trends in two panels (Shrestha & Kostandini 2024).

No US study compares compliant and noncompliant firms competing in one market after an
enforcement change. [SOURCE: lane `reads/LIT_FIRMS_EVERIFY.md`; 33 of 33 quotes re-found by
`quote_check.py`]

## 4. Who wins and who loses

| Who | Channel | Gain or loss | $bn a year, low / central / high | Relation to the account |
|---|---|---|---|---|
| Noncompliant employers | payroll taxes not paid | gain | 0 / 4.5 / 10.3 | overlaps the September 24 tax correction |
| Noncompliant employers | workers' compensation premiums avoided | gain | 0 / 1.3 / 2.2 | beside |
| Noncompliant employers | underpayment of off-books workers | gain | 0 / 0.6 / 2.3 | beside |
| Off-books workers | underpayment | loss | 0 / 0.6 / 2.3 | beside |
| Off-books workers | own payroll tax kept in cash | gain | 0 / 1.4 / 2.3 | overlaps the September 24 tax correction |
| Off-books workers | no workers' compensation coverage | loss | 0 / 1.3 / 2.2 | overlaps uncompensated care |
| The budget (trust funds, state UI) | payroll taxes not collected | loss | 0 / 5.9 / 10.3 | inside |
| Customers of the four industries | lower prices, if the edge is passed on | gain | 0 / 3.2 / 14.8 | overlaps the production term |
| Compliant owners and their workers | jobs, margin, wages | loss | unpriced: none measured | beside; wages overlap the wage split |

Noncompliant employers include native contractors as well as the group's own businesses, and the
data cannot tell them apart. [FRAMING-SENSITIVE] The customers' gain is priced only as a bounded
share of the measured edge; the compliant owners' loss has no measured basis and stays unpriced.
Neither enters the ledger's nets (symmetry rule 5). [DATA: lane `derived/winners_losers_rows.csv`]

## 5. What this changes

Nothing in the adopted account. No displacement of compliant firms is measured, the edge's tax
part is already inside the account, and the on-books share stays at 0.52. Beside the account sit
$0–2.2bn of workers' compensation premiums avoided and $0–2.3bn of underpayment, transfers from
off-books workers and insurance pools to their employers, within the group where both sides are
group members.

## 6. Steel-man, disconfirmation and bias

The strongest case for the claim: the edge is 12–23% of the off-books wage, or 3.5–7% of a
construction project's cost; it is concentrated in a few trades; enforcement cannot see the cash
economy; the slope puts over half of the group's construction wage workers off the books; and
enforcement shifted activity toward the least compliant firms in Arizona and toward small firms
under mandates (Ayromloo, Feigenberg & Lubotsky).

What cuts against it: covered establishments and employment show null or positive associations,
never the negative one the claim needs; the supportive specialty-trade association vanishes with
state-wide controls; the E-Verify design fails; the Georgia rival effect is insignificant in the
industries the claim is about; removals lowered business counts.

Of the post-hoc checks, three weakened results on the claim's side (the specialty-trade control,
the per-industry wage comparison, the level check) and one strengthened one (excluding agriculture
raised the pooled slope). That imbalance is the direction an LLM's post-training lean would produce
(`../notes/llm-bias-caveat.md`), so the unadjusted results stay in the lane's tables beside the
checks.

**Would change it:** an employer–employee test of rival exit in construction with cash firms
visible (for example LEHD with SSA no-match flags); Florida's 2023 mandate with more post years,
or another mandate outside the housing cycle with flat pre-trends; an independent count of
off-books workers by industry and state that settles the slope against the level check, which
would move the edge anywhere in $0–15bn.

## Sources

- Lane: [`compliance_gap_2026_09_24`](../infra/immigration-fiscal/compliance_gap_2026_09_24/RESULT.md)
  (BRIEF, scripts in run order, `derived/`, reading notes in `reads/`). IPUMS USA ACS 2005–2024
  (extracts 16 and 17), QCEW 2005–2024, DOL WHD and OSHA enforcement files, BLS ECEC June 2026,
  IRS Publications 1415 and 5869. [DATA]
- Parent rerun, 2026-09-25: all twelve analysis scripts exit 0; 21 of 22 derived files
  byte-identical, and `everify_event_study.csv` differs in one t value's last printed digit
  (relative 1.6e-5). The QCEW, DOL and IPUMS downloads were not repeated. [CALCULATION]

## Revisions

None yet.
