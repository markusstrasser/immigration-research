# Brief: what California spent on unauthorized residents — primary budget sources

Operator, 2026-09-23 20:10, pasting a City Journal "Eye on the News" piece dated Sep 23 2026:
"Can you confirm this from the data we have?" The claims to test, verbatim from the paste:

1. "California runs the nation's largest welfare system, devoting more than $180 billion annually
   to food, health care, and other programs for the poor and downtrodden."
2. "a shadow welfare system that allows noncitizens to receive health care, rental assistance,
   college grants, tax credits, low-cost car insurance, and even smartphones on the taxpayers' dime."
3. "California taxpayers spent at least $11 billion subsidizing illegal immigrants in the last
   fiscal year." ("Last fiscal year" = FY2025-26, July 2025–June 2026, unless the article says
   otherwise.)
4. Four Southern California public-services offices "admitted that illegal aliens can enroll in
   public-welfare programs or receive benefits on their children's behalf."

A sister lane (`../california_medical_status_2026_09_23/`) checks the same claims against our local
survey and Census finance data. This lane answers from **primary government documents**.

## Tasks

1. Find the article (City Journal / Manhattan Institute) and record exactly what its $11bn and
   $180bn comprise and which sources it cites. Quote it. Do not treat it as evidence.
2. For each program below, give FY2024-25 and FY2025-26 dollars (and the 2026-27 budgeted figure
   if published), split into **state General Fund / other state funds**, **federal funds** and
   **county funds**, and say whether the figure covers only people with unsatisfactory immigration
   status (UIS) or a mixed population:
   - Medi-Cal full-scope coverage for UIS individuals (all ages since Jan 2024), including IHSS,
     long-term care and dental; the 2025 Budget Act changes (enrollment freeze for adults from
     Jan 2026, premiums, dental elimination) and their dates; UIS enrollment counts.
   - Restricted-scope (emergency and pregnancy) Medi-Cal for UIS individuals: the federal share
     at FMAP, since "California taxpayers" excludes federal dollars.
   - CalEITC, Young Child Tax Credit and Foster Youth Tax Credit paid to ITIN filers (FTB annual
     reports), and any one-time payments such as the Golden State Stimulus to ITIN filers.
   - Cal Grant, Middle Class Scholarship and other aid to California Dream Act (AB 540) students
     (CSAC).
   - California Food Assistance Program (CFAP): who is eligible now, and the status and date of
     the expansion to undocumented adults 55+.
   - CAPI (legal immigrants only; say so if confirmed), state rental assistance, California
     LifeLine (phones; status requirement?), California Low Cost Auto Insurance, county indigent
     health programs (e.g., Los Angeles County My Health LA), state-funded legal services.
3. For claim 1: Medi-Cal total funds and General Fund in FY2025-26, and California's total
   health-and-human-services spending, with what "$180 billion" could refer to.
4. Verdict per claim: supported, supported only in total funds, overstated, or unverifiable, with
   the arithmetic.

## Sources and rules

- Primary documents only for numbers: DHCS Medi-Cal Local Assistance Estimates (November 2025,
  May 2026; the "Policy Change" pages for UIS full scope), LAO reports and budget analyses, the
  Department of Finance budget summaries (ebudget.ca.gov), FTB CalEITC reports, CSAC reports,
  CDSS program pages. Download PDFs with `curl` via `subprocess` (Python urllib fails TLS on this
  machine) into `_cache/`, parse locally (`pdftotext -layout`), and quote with page numbers.
  Never take a number from a Firecrawl/LLM schema extraction or a news summary
  (a Firecrawl extraction once fabricated an SSA table here).
- Tag every number `[SOURCE: url, page]`, `[CALCULATION]`, `[INFERENCE]` or `[UNVERIFIED]`.
  Distinguish total funds from General Fund in every row.
- Steel-man the article's reading before evaluating it, and state where "subsidizing illegal
  immigrants" is a framing choice (e.g., mixed-status households, US-citizen children of
  unauthorized parents, emergency care that federal law requires). Flag `[FRAMING-SENSITIVE]`.
- Stay within about 12 research turns; if sources run out, write what you have and list the gaps.

## Output

`RESULT.md` in this directory, opening with `**Verdict:**`, then: the claim-by-claim table, the
program table (program | FY | total | GF/state | federal | county | population covered | source,
page, quote), what the article's $11bn most plausibly sums, and gaps. Keep fetched documents in
`_cache/` (ignored). Do not commit. Do not edit files outside this directory. Reply to the lead
with the path and at most 10 lines.
