# Brief — sources for pricing unauthorized seniors' public health costs (lineage lane)

Parent: the session integrating the weekly-audit corrections, 2026-09-26. Output file (you own it):
`infra/immigration-fiscal/lineage_cost_2026_09_19/senior_pricing_sources.md`. Archive fetched documents
to `infra/immigration-fiscal/lineage_cost_2026_09_19/_cache/` (ignored by git). Do not edit any other file. Do not commit.

## Why

The lineage model now bars an unauthorized founder from Social Security, Medicare, SSI and federal
Medicaid from age 65 (42 USC 402(y); 8 USC 1611). The federal statute still allows emergency Medicaid
(42 USC 1396b(v)), some states fund full coverage regardless of status, and hospitals give uncompensated
care that governments partly finance. We need per-person annual public cost for an unauthorized
Mexico-born person aged 65+ under each. Figures already in the repo and not to be re-sourced:
Illinois HBIS FY2025 $139M projected for 8,931 enrollees (Feb 2025); New York 65+ about $229M a year
[inference from a $171.9M nine-month deferral]; California UIS Medi-Cal about $10.8bn GF for all ages
(`state_programs_unauthorized_2026_09_23/RESULT.md`, `improper_payments_unauthorized_2026_09_23/RESULT.md`);
uncompensated care $1,524 per uninsured person-year and a 58–70% government offset share
(`uncompensated_care_2026_09_23/RESULT.md`). Read those first.

## Questions (answer each with verbatim quotes, URL, page or table, and date)

1. **Emergency Medicaid, national.** The most recent annual spending on Medicaid emergency services for
   non-qualified noncitizens (total, and federal/state split if given), from CMS-64/MBES, MACPAC, KFF,
   CBO, GAO or HHS-OIG. Then any breakdown by age group or by service (childbirth, dialysis, other) that
   gives the share or per-enrollee cost for people 65+. State studies with age detail are welcome
   (for example DuBard & Massing, JAMA 2007, North Carolina; Colorado or Texas reports). Say which
   populations each figure covers.
2. **California older adults.** DHCS figures for the full-scope Medi-Cal expansion to undocumented adults
   aged 50+ (the Older Adult Expansion): annual cost (total funds and General Fund) and enrollment, from
   the Medi-Cal May Revision / Local Assistance Estimate or LAO. Give a 65+ breakdown if one exists.
   Then the 2025 Budget Act changes: the enrollment freeze for undocumented adults (the ages covered,
   the start date, whether people aged 65+ are exempt, grace periods for people already enrolled) and
   the premiums.
3. **Enrollment status in 2026** for undocumented people aged 65+: Illinois HBIS, New York's 65+
   Medicaid, Oregon's Healthier Oregon, Washington's Apple Health Expansion and the DC Alliance. Say
   whether each is open or closed to new enrollees, and from when.
4. **Care received by uninsured seniors.** Uncompensated care, or total care received, per uninsured
   person by age, especially 65+ or 55–64 against the all-age average. Sources: Coughlin et al.
   (Health Affairs 2014; KFF/Urban 2021, "Sources of Payment for Uncompensated Care for the
   Uninsured"), MEPS or similar.

## Rules

- Primary documents first. If a figure is only in a secondary summary, tag it `[SECONDARY]`, name the
  primary document it cites, and say that you did not see that document.
- Tag each number `[SOURCE: …]`. Mark your own arithmetic `[CALCULATION]` and judgment `[INFERENCE]`.
  If a figure cannot be found, write "not found" and list the places you searched. Never estimate
  a figure into existence.
- For any number that feeds a calculation, read the PDF or table itself; do not rely on a
  schema-extraction summary. Write the output file first and add to it as you go.
- The file opens with `**Verdict:**`, followed by one line per question saying what was found.
- Automated fetching of x.com/twitter.com is blocked.

## Return

The file path and at most 10 lines: the headline figure per question and what is missing.
