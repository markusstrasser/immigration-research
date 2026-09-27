# Lane brief: do visa-holding physicians crowd Americans out of residency, and does a tax break pay for it?

Date 2026-09-28, 00:05 JST. Parent session immigration-research-1c. The operator pasted a claim (verbatim):

> Rochester General Hospital in New York hired 82 resident doctors. 80 are foreign workers on H-1B or J-1
> visas. Only 2 are Americans. 98% of the residency slots went to visa workers – mostly from countries with
> documented USMLE cheating.

He asks whether there are "pockets of coordination that kill opportunity ... maybe because of salary savings or
FICA exemptions for F1 / OPT".

## Questions

1. **The claim.** Check the incoming-class count and the visa and citizenship split against the hospital's own
   pages, announcements or program listings. Which programs and year? Did US citizens who trained abroad count
   as "Americans"? If it can't be verified, say so.
2. **Pay.** Do residents on J-1 or H-1B visas earn the same PGY salary as US graduates in the same program?
   Does Medicare GME (direct GME and IME) pay per resident regardless of citizenship? Quote CMS or the statute.
3. **Tax.** Take J-1 alien physicians, F-1 students on OPT and H-1B holders. For each: which are exempt from
   FICA, for how long, and on what legal basis (26 U.S.C. 3121(b)(19), the "exempt individual" rules and IRS
   Publication 519)? Estimate the saving per resident per year to the employer and to the resident. Add the
   visa costs employers bear for H-1B.
4. **Crowd-out.** NRMP Main Residency Match 2024–2025 results by applicant type: US MD seniors, DO seniors, US-citizen
   IMGs and non-US IMGs.
   - Give the match rates and the IMG share of positions in internal medicine and in community programs.
   - Who goes unmatched, and in which specialties? Is the displacement margin US MD seniors, or US-citizen
     IMGs and DO graduates?
   - Is the binding constraint the Medicare-funded GME cap (1997) rather than employer preference?
5. **"USMLE cheating."** What is documented? Cover NBME and ECFMG irregular-behavior findings, score
   invalidations, and any country-specific actions, with dates and counts. Say what is not documented.
6. **Beyond residency.** Size the F-1 OPT FICA exemption: participants from SEVIS by the Numbers, typical wages,
   and a rough annual FICA revenue forgone, employer and employee separately. Is there a documented employer
   preference for OPT workers on cost grounds?
7. **Verdict.** For each part of the claim and each mechanism: true, false or unverified, with the numbers.

## Rules

- Work only in `infra/immigration-fiscal/residency_visas_2026_09_27/`. Write `RESULT.md` first with
  `**Verdict:** pending` and append after each check.
- Verify every number against the primary source and quote it in `reads/`. Firecrawl is out of credits: use Exa
  or direct HTTP with a generic User-Agent, and no personal identifier in any request. No automated x.com
  fetching.
- Tag every number. Steel-man the claim before testing it. Do not commit, stage or stash; the checkout is
  shared.
- Final message: the RESULT path and at most ten lines.
