# Brief: tax credits to ITIN filers and state student aid for undocumented students

Operator, 2026-09-23 20:58: "Find it in other places ... if we have the data ... sherlock", after
California's ~$11bn of state Medi-Cal for undocumented immigrants was confirmed.

## Leads we already hold

- **National Taxpayer Advocate, 2024 annual report, research report 3.**
  - TY2022: 3,791,421 returns carried at least one ITIN, with tax before credits of $18.2bn and
    after credits of $14.5bn.
  - Median AGI $31,033.
  - The report is cited in `../onbooks_share_2026_09_23/RESULT.md`, source table row 11.
- **The dataset audit.** The CPS tax model gives modelled EITC to filers without valid SSNs.
  Applying the SSN rule halves the Mexico-born EITC rate (`../dataset_integrity_2026_09_23/cps.md`
  row 1).
- **California.** CalEITC/YCTC are open to ITIN filers, but FTB does not publish the ITIN share
  (`../california_program_costs_2026_09_23/RESULT.md`).

## Tasks

1. **Federal credits to ITIN filers.** Give the refundable part:
   - ACTC paid to ITIN filers for SSN-holding children (legal since TCJA);
   - other refundable credits;
   - the 2020–2021 recovery rebates and the expanded CTC as they reached mixed-status families.

   Use IRS SOI ITIN tables, TIGTA reports and the NTA. Show the TY2022 difference between tax
   before and after credits ($3.7bn), split into refundable and nonrefundable. Say what share
   plausibly goes to unauthorized filers, not to other ITIN holders (nonresident aliens,
   dependents).
2. **State credits open to ITIN filers.** For each state whose EITC, CTC or other refundable credit
   admits ITIN filers, give the latest year's claims and dollars from ITIN filers where published.
   Candidates:
   - California and Colorado;
   - Washington (Working Families Tax Credit);
   - Oregon, New Jersey, New York, Illinois, Minnesota and Maryland;
   - New Mexico, Maine, Vermont, Massachusetts and DC.

   If a state publishes no ITIN split, say so.
3. **State student aid and tuition.** For each state that gives state grants to undocumented
   students, give recipients and dollars for the latest year:
   - California Dream Act (Cal Grant, Middle Class Scholarship);
   - Texas (TEXAS Grant / TASFA);
   - Illinois (RISE Act, MAP);
   - New York (Senator José Peralta DREAM Act);
   - Washington (WASFA), New Jersey, Minnesota, Colorado, Oregon and others.

   Give in-state tuition only where a state or fiscal office estimates its cost. Do not invent the
   subsidy.
4. **Mexican share.** Where data allow, estimate the share of these dollars reaching Mexican-born
   or Mexican-origin families. For ITIN filers, the NTA or IRS may publish country of birth or
   state distributions. For students, give campus or state origin data if published.

## Rules

- Primary documents: IRS SOI, TIGTA, the NTA, state revenue departments and state
  student-aid agencies.
- Fetch with `curl` through `subprocess` or plain curl with a browser User-Agent; Python urllib
  fails TLS here. Wayback `id_` for blocked sites.
- Keep PDFs in `_cache/` and quote with page numbers.
- Tag news-only figures `[SECONDARY]`, and every figure otherwise `[SOURCE]`, `[CALCULATION]`,
  `[INFERENCE]` or `[UNVERIFIED]`.
- Lawful credits are not fraud. Improper claims belong to
  `../improper_payments_unauthorized_2026_09_23/`.
- Stay within about 12 research turns.

## Output

`RESULT.md` in this directory, opening with `**Verdict:**`, with a program × state table and the
federal ITIN section. Do not commit, and do not edit outside this directory. Reply to the lead with
the path and at most 10 lines.
