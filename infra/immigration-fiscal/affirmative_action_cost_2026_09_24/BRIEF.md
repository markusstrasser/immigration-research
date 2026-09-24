# Brief: what race- and ethnicity-based preferences cost white natives

Operator, 2026-09-24 08:39: "Do we have a calculation what affirmative action costs white natives
for career loss?"

We do not. Two earlier pieces of work are relevant:
- `../ledger_residual_agg_2026_09_16/RESULT.md`, section "What remains unpriced", found that
  set-asides and admissions preferences cannot be placed on the per-person generation ledger. It
  holds one aggregate: small disadvantaged businesses won 12.27% of federal prime contract dollars
  in FY2024 (SBA scorecard). That is a total of contracts awarded; it is not a cost.
- `research/immigration-essay-angles-from-bookmarks-2026-09-16.md`, lines 132–145, checked the 8(a)
  mechanism:
  - every applicant must prove economic disadvantage;
  - social disadvantage was presumed for designated groups;
  - US citizenship is required, and nativity is not a category.

## Object

Estimate the annual career cost to non-Hispanic white natives of preferences based on race or
ethnicity:
- lost earnings and lost business profits;
- in 2024, and at the level before 2023;
- with the part that goes to Hispanic beneficiaries, and to Mexican-origin beneficiaries where it
  can be split.

The Hispanic part ties this to immigration: Hispanic immigrants and their descendants became
eligible on arrival or at birth.

## Channels

1. **Selective college admissions before the SFFA ruling (June 2023).** Estimate the seats shifted
   away from white applicants each year, and the earnings effect on a displaced applicant of
   attending the next college instead. Start from:
   - Arcidiacono, Kinsler and Ransom on the Harvard trial data;
   - Espenshade and Radford (2009);
   - Bleemer (2022, QJE) on Proposition 209, and whatever it reports for the non-URM applicants
     who took the seats;
   - Chetty, Deming and Friedman (2023) on Ivy-Plus attendance;
   - Dale and Krueger (2002, 2014);
   - Long (2004);
   - Hinrichs (2012) on state bans.

   Count seats nationally from IPEDS enrollment at selective institutions if a paper gives a shift
   per seat.
2. **Employment.**
   - Federal-contractor affirmative action under EO 11246, revoked by EO 14173 in January 2025:
     Leonard (1984, 1990), Kurtulus (2016, JPAM), Miller (2017, AEJ: Applied), Holzer and Neumark
     (2000, JEL).
   - Public-sector hiring under consent decrees, for example McCrary (2007, AER) on police.
   - Evidence against: correspondence studies of Hispanic versus white callbacks, Quillian et al.
     (2017, PNAS) and Kline, Rose and Walters (2022, QJE).
3. **Contracting.** Covers federal SDB and 8(a), DOT DBE, and state and local MBE programs.
   - The cost to firms without the preference is the profit lost on awards shifted away from
     them.
   - The cost to taxpayers is the price premium: Marion (2007, 2009) on California highway
     contracts after Proposition 209, and later DBE work.
   - Hispanic-owned share of FY2024 federal obligations: FPDS or USAspending business-type flags.
   - 8(a) participants by group: SBA reports.
   - Legal changes: the Ultima ruling (July 2023) ended the 8(a) presumption; DOT issued an
     interim final rule on DBE in 2025.
4. **Other channels.** For DEI hiring after 2020 and grants to minority-serving institutions,
   grade the evidence. Leave a channel unpriced if no credible estimate exists.

## Output

Write `RESULT.md` in this directory, opening with `**Verdict:**`. Include:
- a table with one row per channel and these columns:
  - cost to white natives in $bn a year (low, central, high), for 2024 and before 2023;
  - Hispanic share;
  - Mexican-origin share;
  - evidence grade;
- the evidence against each channel;
- a per-worker figure for white native workers, if the totals allow it;
- where the result sits against our account: outside the fiscal ledger, beside the
  income-distribution entry (ladder 194);
- gaps.

Put calculations in `calc.py`, writing `derived/calc_output.txt`. Rerun it once and confirm the
output is byte-identical.

## Rules

- Check every number used in a calculation against the page of the paper or report it comes from.
  Save the source under `_cache/` or through the research MCP (`fetch_paper`, `read_paper`). Never
  take a figure from an abstract or an LLM extraction alone when the full text is available.
- Tag every figure `[SOURCE]`, `[CALCULATION]`, `[INFERENCE]`, `[TRAINING-DATA]` or `[UNVERIFIED]`.
- Make the strongest case on both sides: that preferences impose a large cost on white natives,
  and that they impose little.
- Spend about 12 research turns before writing. Run a second round only if a channel's central
  value is still unsupported.
- Fetch with `curl` through `subprocess`; Python urllib fails TLS here.
- Do not commit. Do not edit outside this directory. Reply to the lead with the path and at most
  10 lines.
