# Brief: civic attachment and group dissolution by generation, Mexican origin

Operator question (2026-09-27): does the civic side (service, participation, voting, marriage
out of the group) converge across generations faster or slower than the economic gap? Part of
the first report on low-skill Mexican migration. A sister lane
(`generation_carryover_2026_09_27`) measures the economic carry-over; this lane supplies the
civic and intermarriage carry-over so the two can be set side by side.

## What already exists (reuse, do not rebuild)

- CPS Sept 2021+2023 volunteering, giving and veteran status by G1 / G2 / G3+ Mexican with
  replicate SEs and SES adjustment: `infra/immigration-fiscal/service_by_ses_2026_09_23/cps_civic.py`,
  RESULT.md §4. ACS military by origin: same lane and `civic_service_by_ancestry_2026_09_21/`.
- Indian civic CPS lane (voting code may be reusable): `infra/immigration-fiscal/indian_civic_cps_2026_09_18/`.
- Norms by generation (GSS/ANES): `research/immigration-institutions-and-liberal-norms-by-generation-2026-09-18.md`.
- Grandparent linkage classifier for G3 vs G4+: `infra/immigration-fiscal/generation_split_2026_09_20/analyze_cps.py`.
- Lineage model's intermarriage/attribution parameters: `infra/immigration-fiscal/lineage_cost_2026_09_19/`.

## Tasks

1. **Voting.** CPS November Voting and Registration Supplement 2020, 2022 and 2024 (Census
   public-use CSVs from www2.census.gov/programs-surveys/cps/datasets/<yr>/supp/; validate
   rows). Among citizens 18+: registered and voted, by Mexico-born naturalized, G2 (parental
   birthplace from the basic CPS fields in the supplement file), G3+ Mexican, US-born NH whites.
   Raw and adjusted for age, sex, education, family income, state (weighted LPM, replicate SEs
   if the supplement ships replicate weights; otherwise say what SE method you used). Note the
   known over-report of turnout in CPS and that it is roughly common across groups only if
   evidence says so.
2. **Intermarriage by generation.** CPS ASEC 2022–2025 (existing archives; see
   `research/immigration-dataset-register.md` for paths): for married Mexican-origin persons
   25–54 by G1 / G2 / G3+ (and observed G3 vs G4+ where linkage allows), share whose spouse is
   (a) Mexican-origin, (b) other Hispanic, (c) non-Hispanic. Use the spouse pointer. Then the
   identification of children of mixed couples (share of children with one Mexican-origin and
   one non-Hispanic parent who are reported Hispanic/Mexican) — the Duncan–Trejo attrition
   mechanism. Compare Indian-origin G1/G2 endogamy on the same code (the Indian memo reported
   88% G1 spousal endogamy) so the two groups sit on one instrument.
3. **One civic table with carry-over.** Assemble volunteering, giving, veteran status
   (existing), voting (new), endogamy (new), and the norms indices (existing, cite) by
   generation with the gap vs NH whites and ρ(n→n+1) = gap(G n+1)/gap(G n), raw and at equal
   SES. Recompute from the existing lanes' derived CSVs, do not retype.
4. **Disconfirmation.** Where the civic gap is SES composition (it shrinks at equal SES), say so;
   where it persists at equal SES, say so; check whether military service (men) differs from
   women (existing lane found women at parity) and from young cohorts now serving.

## Outputs

- `RESULT.md` opening `**Verdict:**` (stub first, append as you go), files covered and skipped.
- Scripts here; `derived/voting.csv`, `derived/intermarriage.csv`, `derived/child_identification.csv`,
  `derived/civic_carryover.csv` with `source`, `measure`, `generation`, `n`, `estimate`, `se`,
  `adjustment` columns; a `verify.py` for the gates.
- `.gitignore` with `_cache/`.

## Gates

- Recomputing the existing Sept-supplement volunteering rates for Mexican G1/G2/G3+ from
  `service_by_ses_2026_09_23/derived/` matches RESULT.md §4 (10.9 / 15.1 / 19.7%).
- The CPS November total turnout for all citizens within 1 point of Census's published table
  for each year (cite the table URL).
- Spouse linkage: share of married persons with a found spouse record ≥ 99%.

## Conventions

- `uv run --no-project python3 …` from the repo root; add `--with <pkg>` literally if missing.
- Fetch via `subprocess.run(["curl","-sS","--fail",...])`; validate content, not status.
  Census key only if you use the API: `set -a; . infra/immigration-fiscal/acquire/config.local.env; set +a`;
  never print it; no `ps`/`pgrep` dumps.
- `csv.writer(..., lineterminator="\n")`. Source tags per `CLAUDE.md`.
- Do not commit; do not edit outside this directory. Return RESULT.md path and ≤10 lines.
