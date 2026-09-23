# Brief: state-funded programs for unauthorized residents outside California

Operator, 2026-09-23 20:58, after the California lanes confirmed ~$11bn of state Medi-Cal for
undocumented immigrants: "Find it in other places ... if we have the data ... sherlock".

California is done: `../california_program_costs_2026_09_23/RESULT.md` (budget documents) and
`../california_medical_status_2026_09_23/RESULT.md` (survey counts). Do not redo it. This lane
does the same for **every other state**.

## Leads from our own data

With the status imputation's Medicaid clause dropped, CPS ASEC 2025 shows likely-unauthorized
people reporting Medicaid or other means-tested coverage in 2024
(`../california_medical_status_2026_09_23/derived/cps_moved_by_state.csv`; millions, with SE):
- **States with status-blind programs:** New York 0.587 (0.070), Massachusetts 0.172, New Jersey
  0.166, Illinois 0.140, Washington 0.098.
- **States with none:** Texas 0.200 and Florida 0.199. There the report is emergency Medicaid,
  coverage of citizen children, lawful residents the residual misclassifies, misreporting or a
  hot-deck value.

That lane's `STATUS_BLIND_2024` list (sourced to KFF, OHA, NY DOH, DHCS) is the starting
inventory.

## Tasks

1. For each state with a program serving people regardless of immigration status, give the
   program, eligible ages and dates, enrollment, and FY2024-25 and FY2025-26 cost split into state,
   federal and local funds. Cover health (NY Essential Plan and PRUCOL coverage, NY 65+; Illinois
   HBIA/HBIS and their cost overruns; Oregon Healthier Oregon; Washington Apple Health Expansion;
   DC Healthcare Alliance and Immigrant Children's Program; Massachusetts; New Jersey Cover All
   Kids; Colorado OmniSalud / Cover All Coloradans; Minnesota's 2025 MinnesotaCare expansion;
   Connecticut, Maine, Rhode Island, Vermont, Utah children), plus any state cash or food program
   that serves unauthorized people. Include state shares of emergency Medicaid where a state
   publishes them.
2. Say how much of each figure is status-blind coverage of unauthorized people, and how much is
   lawfully present people (PRUCOL, the five-year bar, TPS, asylum applicants). Many "immigrant
   coverage" programs mix them. Mark it `[FRAMING-SENSITIVE]`.
3. Where the program or survey allows, give the Mexican-born or Mexican-origin share of recipients
   (the CPS table above has `moved_mexico_born_millions` by state). The fiscal account charges
   Medicaid through national age × nativity keys (union 12.25% of the line), so the question is
   whether these flows reach the Mexican-origin group more or less than the key assumes.
4. Total the documented state spending across states for the latest year, with its components.

## Rules

- Primary documents for every number: state budget offices, Medicaid agencies, legislative fiscal
  offices, state auditors, CMS.
- Fetch with `curl` through `subprocess` or plain curl with a browser User-Agent. Python urllib
  fails TLS here. Many state sites block curl; use the Wayback `id_` route. Exa `crawling_exa` can
  read e-editions.
- Keep PDFs in `_cache/` and parse locally with `pdftotext -layout`.
- Quote with page numbers. Never take a number from an LLM extraction or a news summary without
  the primary document; if only a news figure exists, tag it `[SECONDARY]`.
- Tag every figure `[SOURCE]`, `[CALCULATION]`, `[INFERENCE]` or `[UNVERIFIED]`.
- Steel-man the programs' case before evaluating it.
- Do not call lawful state spending "fraud". Improper payments belong to the sister lane
  `../improper_payments_unauthorized_2026_09_23/`.
- Stay within about 12 research turns.

## Output

- `RESULT.md` in this directory, opening with `**Verdict:**`.
- State × program table: program | FY | enrollment | total | state | federal | local | population
  covered | Mexican share if known | source, page, quote.
- Cross-state total; gaps.

Do not commit. Do not edit outside this directory. Reply to the lead with the path and at most 10
lines.
