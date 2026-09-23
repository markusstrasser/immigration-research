# Brief: improper payments and fraud involving unauthorized immigrants — what the auditors found

Operator, 2026-09-23 20:58, calling California's ~$11bn of state-only Medi-Cal for undocumented
immigrants "fraud" and asking to "find it in other places ... sherlock".

That spending is lawful state policy, budgeted openly. The one irregularity in California's
documents is ~$1.1bn of federal Medicaid funds claimed for state-only UIS services and returned in
2025-26 ($819.3M in January 2026 and $288.9M in May 2026; see
`../california_program_costs_2026_09_23/RESULT.md` program table). This lane finds what
investigators and auditors have actually documented, and separates three categories:

- **fraud:** intentional, charged or adjudicated;
- **improper payments:** paid in error or claimed from the wrong funding source, recovered or not;
- **lawful spending** that critics call waste.

## Tasks

1. **Medicaid.** Cover:
   - HHS-OIG audits of states' federal claims for non-qualified immigrants: emergency Medicaid,
     state-only populations and eligibility verification;
   - CMS's 2025 reviews and actions on states claiming federal match for unauthorized enrollees
     (California, Illinois, Oregon, Washington, New York, Colorado, DC and others), with amounts
     recovered or disallowed;
   - GAO reports;
   - state auditors (California State Auditor, Illinois Auditor General on HBIA/HBIS, and others);
   - PERM improper-payment rates attributable to eligibility or immigration status.

   The corpus copy at `/Volumes/2TBPNY/corpus/hhs_oig/` holds only exclusions and integrity
   agreements. You may search it, but the audit reports themselves are on oig.hhs.gov.
2. **Tax.** Cover:
   - TIGTA and IRS findings on ACTC and other refundable credits claimed with ITINs;
   - EITC claimed with SSNs that are not the filer's own;
   - the NTA's view of ITIN processing;
   - dollar amounts denied or recovered.
3. **Social Security and SNAP.**
   - **Social Security:** SSA-OIG on earnings posted to SSNs not the worker's own (Earnings
     Suspense File size), and on benefits to ineligible noncitizens. Note that the suspense file
     is money paid *in* by workers who cannot claim it.
   - **SNAP:** USDA-OIG and FNS quality-control findings on ineligible noncitizens.
4. **Pandemic programs.** Unemployment insurance and Economic Impact Payment findings that involve
   noncitizen eligibility, as distinct from identity-theft fraud generally.
5. For each finding give the amount, year, program and category (fraud / improper / lawful). Say
   whether our account, which uses BEA totals, already contains the dollars; it usually does,
   since outlays are outlays.

## Rules

- Primary documents for every number: OIG and GAO reports, CMS letters, TIGTA, SSA-OIG and
  state auditors.
- Fetch with `curl` through `subprocess` or plain curl with a browser User-Agent; Python urllib
  fails TLS here. Use Wayback `id_` for blocked sites.
- Keep PDFs in `_cache/` and quote with page numbers.
- Tag news-only figures `[SECONDARY]`.
- Keep the three categories separate throughout.
- Steel-man both readings: the programs' defenders, and the critics who see systematic abuse.
  The operator frames the California spending as fraud. The evidence decides the category; say so
  plainly where it doesn't support that word.
- Stay within about 12 research turns.

## Output

`RESULT.md` in this directory, opening with `**Verdict:**`, with a findings table (program | year |
amount | category | agency | source, page, quote) and a summary total by category. Do not commit.
Do not edit outside this directory. Reply to the lead with the path and at most 10 lines.
