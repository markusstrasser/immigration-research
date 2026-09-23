**Verdict:** Outside California, state programs that cover people regardless of immigration status
exist, but they are about a tenth of California's size. Primary budget documents put the latest
year's state and local cost at **about $1.0–1.4bn across eight states and DC**. California spends
about $10–11bn from its General Fund on Medi-Cal for undocumented residents (sister lane). New York
itemizes no dollar cost for its two largest status-blind programs: over 140,000 undocumented
children in Child Health Plus and Medicaid for undocumented people aged 65+. Adding them at
inferred per-enrollee rates gives **roughly $1.5–2.1bn** [INFERENCE].

The documented total comes mostly from two states. Illinois' HBIA/HBIS was projected at $558M in
FY2025, and the adult program closed on 1 July 2025. Oregon's Healthier Oregon runs at about $0.3bn
General Fund a year. The rest is New Jersey's Cover All Kids ($164M, FY2026), DC's Alliance ($121M,
FY2026), Washington's Apple Health Expansion (~$72M), Connecticut (~$55M), Colorado's
children's coverage ($53M), Minnesota (~$43M, an estimate) and Utah ($4.5M). All of this is state or
local money. The only federal money is emergency Medicaid and CHIP's unborn-child option for
pregnant women. No state except California publishes a status-specific figure for either one.
[FRAMING-SENSITIVE]

Since 2025 the programs have been cut back. Illinois closed HBIA. DC cut Alliance eligibility and
froze new adult enrollment. Washington closed Apple Health Expansion to new enrollees, and
Minnesota ended adult coverage. Costs ran well above the original estimates: 84–282% in Illinois,
and in Colorado children's costs reached about 12 times the fiscal note.

Two non-health programs cost more than any health program outside California, but neither is
status-blind coverage of unauthorized people. **New York's asylum-seeker assistance** used $1.18bn of
state funds in FY2025, with $1.60bn projected for FY2026. It serves a mixed population, much of it
paroled or with pending asylum claims. **Massachusetts' family shelter system** cost $857M in FY2024
and now requires citizenship, permanent residence or PRUCOL status. Both are excluded from the
totals.

**Mexican share.** In the CPS (ASEC 2025), 18% of likely-unauthorized people reporting Medicaid or
means-tested coverage in the status-blind states outside California were born in Mexico (53% in
California). Weighting each state's documented spending by that state's CPS share puts about **26–34%
of dollars** with Mexican-born people [INFERENCE]. Oregon and Illinois drive this, and their CPS
cells are small (n = 23 and 47). The fiscal account's national key assigns 12.25% of Medicaid to the
Mexican-origin union. On $1–2bn the gap is about **$0.2–0.3bn a year** more than the key assigns.
That is small outside California.

Every dollar figure comes from a primary document with a page number, with two exceptions, both
tagged. Colorado's figures are JBC staff text read through an Exa crawl, because the PDFs return 403
to curl and are not in Wayback. Minnesota's repeal savings come from House Session Daily.

## Scope and method

The lane covers every state except California with a program serving people regardless of
immigration status. It searched budget offices, Medicaid agencies, legislative fiscal offices,
auditors and CMS/HHS-OIG through Exa with domain filters. It fetched the documents with curl, falling
back to the Wayback `id_` route, and parsed them locally with `pdftotext -layout`. Page numbers are
PDF page indices (form-feed splits). The CPS state table comes from
`../california_medical_status_2026_09_23/derived/cps_moved_by_state.csv`. This lane did no survey
work of its own. It did not look at improper payments, which belong to the sister lane.

## 1. State × program table

"n/f" = not found in a primary document. $ figures are nominal. "State" includes state special
funds. The "Mexican share" column gives the Mexican-born share of likely-unauthorized CPS coverage
reporters in that state, for calendar 2024, with the unweighted n. It comes from the survey, not
from program data. No program publishes enrollees' country of birth.

| State | Program | FY | Enrollment | Total | State | Federal | Local | Population covered | Mexican share (CPS) | Source, page, quote |
|---|---|---|---|---|---|---|---|---|---|---|
| IL | HBIA (42–64) + HBIS (65+), state-only Medicaid look-alike | FY2024 (Jul 2023–Jun 2024) | 53,001 [CALCULATION: 11,464 + 13,596 + 27,941] | **$682M** (HFS) / **$719.3M** (auditor) | same | n/f | 0 | undocumented; lawful permanent residents in the 5-year bar removed during 2024 | 25.6% (13/47) | HFS HBIA page: "In FY24, HFS spent a total of $487 million to administer the HBIA program. Combined HBIA/HBIS spending in FY24 was $682 million." Auditor General performance audit (Feb 2025), Digest Exhibit 2, p12: FY24 "$719,255,222"; p5: "In FY24, the HBIA (42-54) level was the most costly at almost $312 million. The HBIS (65+) level cost $211 million, and the HBIA (55-64) level cost $196 million." |
| IL | same, cumulative | FY2021–FY2024 | — | $1,616.8M | same | — | — | — | — | Audit p12: "$67,315,847 $186,722,013 $643,549,815 $719,255,222 $1,616,842,897" |
| IL | same | FY2025 | HBIA 32,083 + HBIS 8,931 (Feb 2025) | **$558M projected** ($279M paid Jul–Dec 2024) | same | n/f | 0 | mostly undocumented after the LPR removal | 25.6% | HFS FY25 dashboard p1: "Total Proj. Costs* $209 $419 $70 $139 $279 $558". I read these as HBIA $209M→$419M, HBIS $70M→$139M, total $279M→$558M, because the total's first figure matches the HFS page's "$279 million ... during FY25" through December 2024 [INFERENCE] |
| IL | HBIS only; HBIA closed | FY2026 | 8,931 (Feb 2025) | n/f; about $139M at the FY2025 HBIS rate [INFERENCE] | same | — | — | undocumented 65+ | — | HFS page: "The Health Benefits for Immigrant Adults (HBIA) program, which served eligible individuals aged 42 to 64, closed effective July 1, 2025." |
| IL | All Kids and pregnancy coverage regardless of status | — | n/f | n/f | — | — | — | children, pregnant | — | [GAP] no separate cost line found |
| NY | Child Health Plus (CHP), undocumented children under 19 | FY2026 (Apr 2025–Mar 2026) | **over 140,000** (25% of CHP) | n/f | 100% state | 0 | 0 | undocumented children | 14.8% (28/179) | DOB FY2026 Annual Information Statement pp62–63: "including undocumented children at a 100 percent State cost"; "the State is covering over 140,000 undocumented children ... Undocumented children account for 50 percent of unfunded non-Federal program costs" |
| NY | Medicaid for undocumented people 65+ (from 1 Jan 2024) | FY2024 | n/f | n/f | delaying the start saved **$171.9M** of state money in FY2024 | — | — | undocumented 65+ | — | DOH FY2024 Enacted Budget Briefing p4: "Delay Implementation of Undocumented Coverage Expansion for 65+ 1/1/24 Article VII ($171.90) $0.00" (FY2024, FY2025 state impact, $M) |
| NY | Essential Plan and state-funded Medicaid for lawfully present immigrants ("Aliessa") | SFY2027 | 450,000 lost eligibility | federal EP funding −$10.8bn vs SFY2026 | n/f | — | — | **lawfully present, not unauthorized**; excluded from totals | — | Comptroller press releases, 2026-02-18 ("DOB projects a decrease of $10.8 billion"; "approximately 525,000 individuals would shift to Medicaid ... the state would bear 100% of their Medicaid costs" if the Basic Health Program reversion were not approved) and 2026-07-15 ("450,000 New Yorkers losing eligibility") |
| NY | Asylum-seeker assistance (state operating funds) | FY2025 actual / FY2026 projected | n/f | **$1,179M / $1,602M** (FY2023–FY2027: $4,323M) | same | n/f | NYC's own spending not included | asylum seekers, mixed status; excluded from health totals | — | AIS p138 (printed p132), table "ASYLUM SEEKER ASSISTANCE STATE OPERATING FUNDS (in millions)": "Total State Funding 27 895 1,179 1,602 620 4,323"; the lines include Medicaid/vaccines/testing of 137 (FY2024), 137 (FY2025) and 34 (FY2026) |
| OR | Healthier Oregon Program (HOP), all ages from 1 Jul 2023 | 2023-25 biennium | n/f | **$861.5M** | **$725.5M GF** | $136M (emergency care) | 0 | "members who meet eligibility requirements for OHP except for their citizenship status" | 62.8% (15/23) | LFO *2025-27 Budget Review – OHA* p11: "The 2023-25 budget for OHA included full implementation, at a cost of $725.5 million General Fund and $136 million Federal Funds, for a total funds budget of $861.5 million as of spring 2024." |
| OR | same | 2025-27 biennium | about 5% of caseload moved to OHP Bridge | current service level $1.3bn | **about $0.61bn GF adopted**, about $305M a year [CALCULATION: $1.1bn − $447.4M − $42.9M; current service level rounded to $0.1bn] | rest of the $1.3bn, emergency care | 0 | same | — | p11: "a program budget of $1.1 billion General Fund, $1.3 billion total funds, at CSL"; LFO *2025-27 Budget Highlights* p42: "Healthier Oregon caseload cost savings of $447.4 million General Fund, a $42.9 million General Fund savings is resultant from a shift of roughly 5% of the Healthier Oregon caseload to OHP Bridge" |
| WA | Apple Health Expansion, adults 19+ at or below 138% FPL, from 1 Jul 2024, capped; enrollment closed | FY2025 | 11,936 (Jul 2024), including 692 aged 65+ | **about $72M** [CALCULATION: $70M + $2.16M reserve] | same | "draw down federal match" where possible; n/f | 0 | "an immigration status making them ineligible for medicaid or federal subsidies" | 61.5% (26/38) | HCA presentation to the Senate Health Committee, 2024-07-18, p7: "HCA set aside 3 percent ($2.16 million) as a reserve ... After reserves, the program has around $70M per FY to expend on service delivery."; p9: "Total enrollment: 11,936"; p11: age breakout |
| WA | Apple Health Expansion changes (House supplemental proposal) | 2025-27 | enrollment closed | −$37.2M | −$35.1M near-general fund | — | — | — | — | House Feb 2026 supplemental summary p2: "Apple Health Expansion Changes -35,052 -37,190 -44,436" ($000; near-general fund 2025-27, total, 4-year) |
| WA | Apple Health for Kids regardless of status; Alien Emergency Medical; pregnancy coverage | — | n/f | n/f | — | — | — | — | — | [GAP] |
| DC | Health Care Alliance (21+) + Immigrant Children's Program (<21), local funds only | FY2023 actual | n/f | $126.3M | local | 0 | = total | residents ineligible for Medicaid, mostly because of status | 0% (0/32) | OCFO FY2026 Approved Budget, DHCF chapter, Table HT0-4 p6 ($000; Actual FY2023, Actual FY2024, Approved FY2025, Approved FY2026): "(H02707) MCO - Alliance 111,194 147,448 132,644 0" and "(H02710) MCO - Immigrant Children 15,119 19,114 18,284 0" [CALCULATION: sums of managed-care lines] |
| DC | same | FY2024 actual | n/f | **$166.6M** | local | 0 | = total | same | — | same table |
| DC | same | FY2025 approved | n/f | $150.9M | local | 0 | = total | same | — | same table |
| DC | merged Health Care Alliance (fee-for-service from FY2026) | FY2026 approved | **22,721** average monthly (FY2026 to Feb 2026) | **$121M** | local | 0 | = total | adults 21+ at 138% FPL; new-enrollment moratorium for 26+ from Oct 2025 | — | DHCF Medicaid Advisory Committee, April 2026, p19: "Alliance program (local funding only) $92 $121 -$29" (FY27 proposed, FY26 approved, change); p28: "Alliance, 8% - 22,721". DHCF oversight testimony 2026-01-29 p5: "the Alliance and Immigrant Children's programs were projected to cost nearly $250 million in FY2026"; p6: FY2027 eligibility cut to "24 percent of FPL" |
| NJ | Cover All Kids Phase II: children "ineligible solely due to immigration status", from Jan 2023 | FY2024 | 46,000 year-end (projected) | about $95.5M [CALCULATION: 396,000 member-months × $205.71 + $14M fee-for-service] | same | 0 | 0 | undocumented children | 9.8% (6/51) | DHS letter to OLS, 2024-06-12: "In FY 2024, year-end enrollment is projected at 46,000 for about 396,000 member months at a cost of $205.71 PMPM"; fee-for-service "$4 million, $14 million, and $16 million" (FY2023–25) |
| NJ | same | FY2025 | about 47,000 | **$151.1M** | $127.8M appropriation + $23.3M Health Care Subsidy Fund | 0 | 0 | same | — | DHS responses to OLS FY2026 discussion points pp26–27: "Cover All Kids Phase II is 100 percent State funded"; "FY2025 $127.8M $23.3M $151.1M" |
| NJ | same | FY2026 | "nearing 47,000" | **$164.0M** | $138.9M + $25.2M (as printed) | 0 | 0 | same | — | same, p27: "FY2026 $138.9M $25.2M $164.0M"; capitation "$233 per member per month" |
| CO | Cover All Coloradans, children (state-only, from Jan 2025) | FY2024-25 actual | n/f | $17.8M | GF | 0 | 0 | "children lacking access due to their immigration status" | 43% (2/4, unusable) | JBC staff supplemental, HCPF, Jan 2026: "HB 22-1289 Fiscal Note $2,102,665 $4,360,863 ... Updated appropriation $16,037,803 $32,075,606 ... Actual/November forecast $17,780,840 $53,360,259" [SOURCE: text via Exa crawl of content.leg.colorado.gov/.../CY26_hcpsup1.pdf; PDF returns 403 to curl; page not verified; saved `_cache/co_jbc_exa_search_text_2026-09-23.json`] |
| CO | same | FY2025-26 November forecast | n/f | **$53.4M** | GF | 0 | 0 | same | — | same; the staff note says actuals are "running higher than the November forecast" |
| CO | pregnant and postpartum coverage regardless of status (Medicaid/CHP+ look-alike, federally matched) | FY2025-26 fiscal-note estimate | n/f | about $29.6M total funds [CALCULATION: 19,514,304 + 1,635,438 + 7,919,640 + 506,095] | n/f | n/f | 0 | pregnant, postpartum | — | HB22-1289 final fiscal note p6, Table 3 ("Non-Citizen Pregnant Adult Medicaid ... $19,514,304" etc.). An estimate, not actual spending |
| CO | OmniSalud (exchange subsidies) | — | n/f | n/f | — | — | — | — | — | [GAP] not retrieved |
| MN | MinnesotaCare for undocumented people, state-only from 1 Jan 2025; adult eligibility ended by 2025 law | FY2026 (2023 estimate) | 7,711 assumed | about **$42.7M** estimated | Health Care Access Fund | 0 | 0 | undocumented (DACA holders moved to the federal Basic Health Program in 2024) | 6.8% (1/11; not status-blind in 2024) | MMB 2026-27 DHS budget book p106 (printed p101): "In January of 2025, Minnesotans who are undocumented but otherwise eligible for MinnesotaCare will be eligible for MinnesotaCare coverage with state-only funds." 2023 preliminary fiscal note p10: "Annual cost of undocumented coverage $0 $4,557,141 $42,654,843 $59,148,048" (FY2024–27). Repeal "expected to save $56.9 million in the 2026-27 biennium" [SECONDARY: House Session Daily] |
| CT | HUSKY state-only coverage: children 15 and under, plus postpartum, regardless of status | FY2026 | about 14,000 children + 3,250 postpartum women (Dec 2024) | about **$55.1M** (FY26), $61.2M (FY27) | state | prenatal care through CHIP unborn-child option at 65% (n/f) | 0 | "would otherwise qualify for Medicaid, except for their immigration status" | 16.4% (3/18) | OFA *FY 26 and FY 27 Budget* p209: "this state-only medical group includes approximately 14,000 children as well as 3,250 women receiving postpartum services"; p208: "state-funded coverage for children ages 15 and under regardless of immigration status". OFA fiscal note on amendment LCO 10410 to HB 7287 (2025): eliminating these programs saves "approximately $55.1 million in FY 26 and $61.2 million in FY 27". That is OFA's price for the programs; the amendment was not adopted [INFERENCE: the budget book still describes the coverage] |
| UT | CHIP-like coverage for children ineligible because of status (SB 217, 2023), capped | FY2024 onward | about 2,000 | **$4.5M/yr GF** appropriated, plus about $0.5M in premiums | $4.5M | small offsets | 0 | children | 21.5% (5/21) | Legislative Fiscal Analyst note, SB 217 2nd Sub.: "This bill appropriates $4,500,000 ongoing General Fund beginning in FY 2024 ... to around 2,000 newly eligible children"; "$25 monthly". Status in 2025-26 [UNVERIFIED] |
| ME | MaineCare for children under 21 regardless of status (from 1 Jul 2022); pregnant people through CHIP | — | n/f | n/f | — | — | — | children, pregnant | 0 obs. | 22 MRSA §3174-FFF; DHHS provider bulletin 2022-07-01 [text via Exa]. The LD 199 (2023) adult expansion fiscal note (FY2024-25 GF $13,679,998, amended to $6,165,595 for parents only) is a proposal; whether it was enacted is [UNVERIFIED]. [GAP] cost |
| VT | Dr. Dynasaur-like coverage for children under 19 and pregnant people regardless of status (Act 48, 2021; from 1 Jul 2022) | — | n/f | n/f | — | — | — | children, pregnant | 12.7% (2/18) | Act 48 (2021) [text via Exa]. [GAP] cost |
| RI | Cover All Kids (FY2023 budget, 2022) | FY2025 | declining as children moved to Medicaid | n/f | state-only group | — | — | children | 0% (0/18) | 2021 fiscal note (H 5714): "FY 2022 Range $1.6 - $5.5M" [text via Exa; local PDF has no text layer]. EOHHS May 2024 caseload follow-up: moving $1.4M from state-only to Medicaid accounts saves "$0.6M from general revenue in FY 2025" [text via Exa]. [GAP] total |
| MA | Children's Medical Security Plan, Health Safety Net, MassHealth Limited for undocumented people | — | n/f | n/f | — | — | — | children; hospital care for uninsured people | 2.1% (2/79) | [GAP] no spending by status found |
| MA | Emergency Assistance family shelter | FY2024 | including 3,265 families "who entered as migrants, refugees, or asylum seekers" (12 Dec 2024 estimate) | **$856.8M** | state (including Transitional Escrow Fund) | n/f | municipal reimbursements inside total | mixed; since the 2025 supplemental budget, limited to citizens, permanent residents and PRUCOL; excluded from health totals | — | EA report to Ways and Means, 2024-12-16, p4: "Total amount expended on the emergency housing assistance program in FY24 $856.8 M"; p2: 3,265, "Estimate based on family head of household citizenship status and primary language spoken" |
| TX | no status-blind program; hospital costs reported under GA-46 | Nov 2024 | 31,012 visits | $121.8M in hospital costs (not state spending), of which $25.2M were Medicaid/CHIP-covered visits [CALCULATION: 3,070,059 + 22,107,204] | n/f | n/f | — | "persons not lawfully present" | 38.4% (29/69) | HHSC news release 2025-04-25 [text via Exa; agency primary]. The first annual report was due 1 Jan 2026 [GAP: not retrieved] |

## 2. Cross-state total, latest year

This counts status-blind health coverage from state and local funds, outside California.

| Component | Year | $M | Basis |
|---|---|---|---|
| Illinois HBIA + HBIS | FY2025 | 558 | HFS projection (HBIS alone in FY2026: about 139 [INFERENCE]) |
| Oregon Healthier Oregon | 2025-27, per year | about 305 | [CALCULATION] from LFO |
| New Jersey Cover All Kids II | FY2026 | 164.0 | DHS |
| DC Health Care Alliance | FY2026 | 121 | DHCF approved budget |
| Washington Apple Health Expansion | FY2025 | about 72 | HCA budget, not actual spending |
| Connecticut state-only group | FY2026 | about 55.1 | OFA pricing |
| Colorado children | FY2025-26 | 53.4 | JBC forecast (page not verified) |
| Minnesota undocumented MinnesotaCare | FY2026 | about 42.7 | 2023 estimate |
| Utah children | yearly | 4.5 | appropriation |
| **Documented subtotal** | | **about 1,376 (with Illinois FY2025) / about 957 (with Illinois HBIS only)** | [CALCULATION] |
| New York CHP, undocumented children | FY2026 | about 336–504 | [INFERENCE]: 140,000 × $200–300 a month × 12. The midpoint uses NJ's $233 capitation, about 391 |
| New York Medicaid, undocumented 65+ | yearly | about 229 | [INFERENCE]: $171.9M for the nine months deferred (Apr–Dec 2023) × 12/9; assumes full enrollment from the first month |
| **With the New York inferences** | | **about 1,520–2,110** | [CALCULATION] |
| *For comparison: California Medi-Cal, undocumented* | 2025-26 | *10,000–11,200 GF* | sister lane `../california_program_costs_2026_09_23/RESULT.md` |
| *Excluded, mixed-status non-health: NY asylum-seeker assistance* | FY2025 / FY2026 | *1,179 / 1,602* | AIS p138 |
| *Excluded: MA family shelter* | FY2024 | *857* | EA report p4 |

The other 49 jurisdictions together spend about 10–20% of California's figure on status-blind
coverage [CALCULATION: 1.0–2.1 / 10.0–11.2]. New York's missing line items are the largest
uncertainty.

## 3. Unauthorized versus lawfully present [FRAMING-SENSITIVE]

| Program | Who is in the figure | Assessment |
|---|---|---|
| IL HBIA/HBIS | Until the 2024 redeterminations, undocumented people **and** lawful permanent residents in the five-year bar. The audit, p9: HFS "referred all legal permanent residents to other programs" to "contain costs". | FY2025 figures are mostly undocumented. FY2021–23 costs include lawful permanent residents (share n/f). Data quality is weak: 6,098 enrollees coded "undocumented" had Social Security numbers (audit p6). |
| NY CHP (the 140,000) and NY 65+ | Undocumented only; lawfully present children draw the 65% federal match | Unauthorized |
| NY Essential Plan / Aliessa | PRUCOL and five-year-bar immigrants | Lawfully present; excluded |
| NY asylum-seeker assistance | Asylum applicants and parolees, some entered without inspection | Mixed and not coverage; excluded |
| OR HOP | "except for their citizenship status": undocumented people plus lawfully present people ineligible for federal Medicaid | Mixed. At least about 5% were lawfully present, since that share moved to OHP Bridge "based on income and eligible citizenship or immigration status" [INFERENCE from LFO] |
| WA Apple Health Expansion | Status bars both Medicaid and exchange subsidies | Mostly undocumented. Includes some lawfully present people, such as DACA holders after the 2025 federal reversal [INFERENCE] |
| DC Alliance / Immigrant Children's Program | Residents ineligible for Medicaid | Mostly undocumented; includes five-year-bar immigrants (share n/f) |
| NJ Cover All Kids II; CO children; CT state-only group; UT; MN | "solely due to immigration status" / "lacking access due to their immigration status" | Unauthorized. New Jersey and Connecticut cover lawfully residing children with federal match elsewhere |
| MA family shelter | Citizens, permanent residents and PRUCOL since 2025 | Lawfully present or PRUCOL; excluded |

Emergency Medicaid is required by federal law for otherwise-eligible people regardless of status
(42 U.S.C. §1396b(v)) [TRAINING-DATA], and states pay the non-federal share. No state except
California publishes that share by status. The only official number found is Texas's
hospital-reported figure above, which measures hospital cost, not Medicaid spending. HHS-OIG
opened a data brief on emergency services claimed for "nonqualified aliens" in selected states on
2026-03-16 (OAS-26-01-061, active).

Cash and food: no current state cash or food program open to unauthorized people was found
outside California. California's CFAP expansion to people 55+ starts in 2027-28 at the earliest
(sister lane). New Jersey's "Excluded New Jerseyans Fund" was a one-time cash benefit (DHS letter to
OLS, 2024-06-12). This lane did not examine state EITCs open to ITIN filers [GAP].

## 4. Mexican share compared with the account's key

The fiscal account charges Medicaid through national age × nativity keys. Under that key the
Mexican-origin union receives 12.25% of the line. For status-blind programs the relevant group is
the Mexican-born: their US-born children are citizens and sit in ordinary Medicaid.

| Group (CPS ASEC 2025, calendar 2024) | Likely-unauthorized coverage reporters (M) | of whom Mexican-born | Share |
|---|---|---|---|
| California | 1.108 (SE 0.078) | 0.592 | 53.4% |
| Status-blind states excluding CA (NY, MA, NJ, IL, WA, CT, OR, UT, RI, DC, VT, ME) | 1.290 | 0.237 | **18.3%** |
| States without status-blind programs (TX 38.4%, FL 8.3%, others) | 1.287 | 0.314 | 24.4% |

[CALCULATION from `cps_moved_by_state.csv`]

Dollar-weighting the section 2 components by each state's CPS share gives **31.3%** with Illinois
at FY2025. With Illinois at HBIS only it is **33.8%**. Adding the New York inferences at New York's
14.8% gives **26.2%** [INFERENCE]. The weight sits almost entirely on Oregon (62.8%, n = 23) and
Illinois (25.6%, n = 47). New York, New Jersey, Massachusetts and DC all have low Mexican shares. So
outside California these flows reach Mexican-born people at about **2–3 times** the key's 12.25%.
In dollars, that is about $0.21–0.29bn a year more than the key assigns [CALCULATION, each total with
its own weighted share: $0.957bn × (0.338 − 0.1225) = $0.21bn; $1.376bn × (0.313 − 0.1225) = $0.26bn;
$1.52–2.11bn × (0.262 − 0.1225) = $0.21–0.29bn]. California is far larger in both share and dollars, and the sister lane
covers it.

The survey counts do not match program counts. New Jersey shows 166k (SE 34k) likely-unauthorized
reporters against about 47,000 enrolled in Cover All Kids II. Illinois shows 140k (SE 34k) against
41,014 in HBIA/HBIS. Washington shows 98k against 11,936 in Apple Health Expansion. DC shows only
8.6k (SE 2.7k) against 22,721 in Alliance. Outside DC, the survey count therefore also holds
emergency Medicaid, lawfully present people the residual method misclassifies, misreports and
hot-deck values [INFERENCE]. Use the CPS for the Mexican share within a state, not for program
counts.

## 5. Steel-man and evaluation

The programs' case runs as follows. Federal law lets states fund this coverage (8 U.S.C. §1621(d))
[TRAINING-DATA]. Unauthorized residents already receive emergency care that is paid for through
emergency Medicaid or uncompensated care, so primary care can replace some costly emergency
episodes. Children's coverage is where the long-run returns are strongest. The enrollees are mostly
younger and cheaper per head than average Medicaid: New Jersey's children cost $227–233 a month. The
enrollees also pay sales, property (through rent) and some income taxes.

The documents give the other side. Costs repeatedly outran estimates. In Illinois the 65+ program
cost 84% more than estimated and the 55–64 program 282% more over FY2021–23 (audit p5). Colorado's
children's program is forecast at $53.4M against a $4.4M fiscal note. DC's pre-cut projection
reached "nearly $250 million". Several states then cut coverage to balance budgets: Illinois closed
HBIA, DC lowered eligibility to 24% FPL for FY2027 and froze new adult enrollment, Washington closed
enrollment, Minnesota ended adult coverage and California froze new enrollment. Oregon moved the
other way: its 2025-27 caseload cost was rebased down by $447.4M. The cutbacks are cost facts, not
evidence of improper spending. These are lawful state appropriations.

This analysis runs on an LLM, which leans toward the programs' framing on politically charged
topics (`notes/llm-bias-caveat.md`). The dollar figures are quoted, not characterized.

## 6. Gaps and next queries

1. **New York dollars.** The CHP undocumented children's cost and the 65+ Medicaid cost are not
   itemized in the AIS. Next: the Senate Finance "White Book" or Assembly "Yellow Book", the DOH
   Medicaid Global Cap reports, and the DOB FY2027 Enacted Financial Plan (the guessed URLs 404; list
   the Wayback CDX for `budget.ny.gov/pubs/archive/fy27/*`).
2. **Oregon.** HOP enrollment and 2023-25 actual spending. Next: OHA HOP dashboards and the LFO 2025-27
   budget report (`olis ... MeasureAnalysisDocument/93679`, which did not fetch).
3. **Washington.** The 2025-27 Apple Health Expansion proviso in ESSB 5167 (grep found only the
   staffing provisos), and the state-only cost of Apple Health for Kids.
4. **Illinois.** Actual FY2025 and FY2026 HBIS costs; the undocumented share of All Kids.
5. **Colorado.** The JBC PDFs return 403 to curl and are not archived, so the numbers rest on the
   Exa crawl text. OmniSalud was not retrieved.
6. **Minnesota.** The primary fiscal note for the 2025 repeal (MMB fiscal notes).
7. **Maine, Vermont, Rhode Island, Massachusetts.** No costs found by status. The March 2026
   Massachusetts shelter report (FY2026 $276.4M appropriated, per Exa text) timed out on
   malegislature.gov.
8. **Emergency Medicaid** state shares: none published outside California. Texas's GA-46 annual report
   (due 2026-01-01) and the HHS-OIG data brief would fill part of this.
9. **Not examined:** Maryland (Healthy Babies, 2026 exchange access), New Mexico, and state EITCs
   open to ITIN filers.

## Sources (all in `_cache/`, ignored)

Illinois: `il_oag_hbia_hbis_2025.pdf` (auditor.illinois.gov
.../2025_Releases/25-HFS-HBIS-HBIA-Perf-Full.pdf), `il_hfs_hbias_dashboard_fy25.pdf`,
`il_hfs_hbia_page.html`. New York: `ny_dob_fy26_ais.pdf` (budget.ny.gov/pubs/archive/fy26/ais/, via
Wayback), `ny_doh_fy24_enacted_briefing.pdf`. Oregon: `or_lfo_2025-27_oha_budget_review.pdf`
(olis CommitteeMeetingDocument/288990, via Wayback), `or_lfo_2025-27_budget_highlights.pdf`,
`or_oha_2025-27_lab_spring2026.pdf`. Washington: `wa_hca_ahe_leg_presentation_2024-07-18.pdf`,
`wa_feb26_budget_summary.pdf`, `wa_5167_session_law.pdf`. DC: `dc_ocfo_dhcf_fy2026_approved.pdf`,
`dc_dhcf_mac_april_fy26.pdf`, `dc_dhcf_perf_testimony_2026-01-29.pdf`,
`dc_dhcf_fy26_budget_testimony.pdf`. New Jersey: `nj_dhs_response_2026.pdf`,
`nj_ols_dhs_analysis_2026.pdf`, `nj_dhs_followup_sba_2024-06-12.pdf` (pub.njleg.state.nj.us, via
Wayback). Colorado: `co_hb1289_final_fiscal_note.pdf`, `co_jbc_hcpf_briefing_summary_fy26-27.pdf`,
`co_jbc_exa_search_text_2026-09-23.json`. Minnesota: `mn_mmb_dhs_2026-27_base_budget.pdf`,
`mn_house_prelim_fiscal_note_2023.pdf`, `mn_lrl_nov25_hcaf_forecast.pdf`,
`mn_house_session_daily_18830.html`. Connecticut: `ct_ofa_fy26-27_budget_book.pdf`,
`ct_ofa_fn_2025_hb7287_lco10410.pdf`. Utah: `ut_lfa_sb217_fiscal_note.html`. Maine:
`me_ofpr_ld199_fn.pdf`. Rhode Island: `ri_osbo_fiscal_note_2021_h5714.pdf` (scan without a text
layer). Massachusetts: `ma_ea_report_2024-12-16.pdf`. Texas HHSC, NY Comptroller, HHS-OIG, Maine
DHHS, Vermont Act 48 and RI EOHHS were read as Exa text only.

Access routes this session: direct curl worked for auditor.illinois.gov, hfs.illinois.gov,
cfo.dc.gov, dhcf.dc.gov, hca.wa.gov, fiscal.wa.gov, lawfilesext.leg.wa.gov, mn.gov, lrl.mn.gov,
house.mn.gov, cga.ct.gov, le.utah.gov and health.ny.gov. The Wayback `id_` route was needed for
budget.ny.gov (the direct fetch timed out), olis.oregonlegislature.gov, oregonlegislature.gov/lfo
and pub.njleg.state.nj.us. content.leg.colorado.gov returns 403 and is not archived, so read it with
Exa text. malegislature.gov and rilegislature.gov timed out on port 443 during the second batch.

Lane `state-programs-unauthorized`, 2026-09-23.

## Parent check (2026-09-23)

The section 2 arithmetic reproduces: $1,375.7M documented, $956.7M with Illinois at HBIS only, and
$1,522–2,109M with the New York inferences. The Oregon per-year figure is $609.7M GF for the
biennium, halved. The key gap was recomputed with each total paired with its own share, giving
$0.21–0.29bn (the lane printed $0.28bn at the top); corrected above.

Quotes verified in `_cache/` (whitespace-tolerant where `pdftotext` splits lines):
- IL HFS "Combined HBIA/HBIS spending in FY24 was $682 million"; auditor "$1,616,842,897"; dashboard "$279";
- OR LFO "$725.5 million General Fund and $136 million Federal Funds" and "$447.4 million General Fund";
- NJ "$164.0M"; DC "$121"; WA "$70M"; CT "$55.1 million";
- NY AIS "covering over 140,000 undocumented children" and asylum "1,179"; DOH "171.90";
- MA "856.8"; MN "42,654,843".

Colorado's `co_jbc_hcpf_supplementals_cy26.pdf` is an HTML error page, so its figures rest on the Exa
text as the lane says. No script in this lane; nothing to rerun.

**How the account actually charges these dollars (parent, 2026-09-23).** Section 4's comparison with
"the 12.25% key" is a composition contrast, not a correction to add. In
`full_account_spending_2026_09_20/builder.py`, BEA's state and local Medicaid (T3.12 line 33,
$938.2bn in 2024) and other medical care (line 34, $16.0bn) form one category. It is charged by MEPS
2024 Medicaid payments per person (`TOTMCD24`), transported to the union by age and US versus
foreign birth. Those payments include state-only coverage that respondents report as Medicaid. The
real question is whether the Mexico-born use more of it than the average foreign-born person of the
same age. The medical-ethnicity lane tests exactly that on the union's own MEPS records (joint −17.7
with LTSS, before the operator). Adding the $0.21–0.29bn to that measurement would double count.

One residual is not covered: that lane pools MEPS 2016–2024, which underweights California's 2024
expansion to adults aged 26–49. [INFERENCE]

Model self-report: claude-opus-5-5[1m].
