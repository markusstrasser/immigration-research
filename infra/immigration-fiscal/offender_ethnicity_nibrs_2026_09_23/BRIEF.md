# Brief: ground the offender input of the crime-victim cost with police records (NIBRS)

Date: 2026-09-23. Operator: "how can we make better case for social costs? better estimates?
better grounding?" The largest social item beside the fiscal account is crime victims' harm,
$28.9bn (custody footing $32.3bn; envelope $15.4–45.3bn; $43.1bn if non-fatal offending follows
arrest shares) [`crime_victim_cost_2026_09_23/RESULT.md`]. Its weakest input, by the lane's own
account (Limits 1–2), is the offending rate: NCVS victims perceive Hispanic non-fatal offending at
0.94 times the white rate while arrests and imprisonment put it far higher, and no held source
identifies Mexican origin. The goal is a better estimate, whichever way it moves.

## Question

Using police-recorded incident data, what are Hispanic offending rates per resident, by offense,
relative to non-Hispanic whites and to all residents, in states where Hispanic residents are
overwhelmingly of Mexican origin? What share of their victims are not Hispanic (the lane's "other
residents" victims)? Re-run the victim-cost calculation with those inputs and report where the
central lands against the NCVS-perception central and the arrest-share arm.

## Data

- FBI NIBRS incident files (Crime Data Explorer downloads, by state and year) for Texas and Arizona,
  2022 and 2023 (Hispanic residents about 85–90% Mexican origin; check with ACS B03001). Add
  California only if its NIBRS agency coverage is adequate for those years; report coverage for
  every state-year (population covered by reporting agencies). Offender segment (ethnicity, race,
  age, sex), victim segment, victim–offender relationship, offense codes, arrestee segment.
- Disk preflight before each download: `df -h` on the destination; stop if a file would leave
  less than 1.5× its size free (the Mac has about 30 GB free). State files, not national masters.
  Keep raw files in `_cache/` (add a `.gitignore` with `_cache/`).
- Denominators: ACS 2022/2023 population by Hispanic origin and age (12+) for the covered agencies'
  jurisdictions if possible, else state totals scaled by coverage. Census key in
  `infra/immigration-fiscal/acquire/config.local.env` (source it; never print it; pipe URL-bearing
  output through `sed -E 's/key=[A-Za-z0-9]+/key=<KEY>/g'`).

## Measurement pipeline (address each)

- Offender ethnicity in NIBRS is recorded by police, often from victim reports; unknown ethnicity
  is common and not random (unknown offenders). Report the unknown share by offense, and bound the
  rates by allocating unknowns (a) proportionally among knowns, (b) all non-Hispanic, (c) all
  Hispanic. Compare the incident-offender view with the arrestee segment.
- Agencies differ in whether they record ethnicity at all; restrict to agencies with a
  non-trivial recorded-ethnicity rate and show the sensitivity.
- Keep the repo's disjoint-category convention: Hispanic of any race; never compare against raw
  "White" (see `research/immigration-crime-race-ethnicity-2026-09-05.md` and the victim lane's
  "Offender ethnicity" section).
- Victims: the account counts harm to other residents only. Use victim ethnicity to estimate the
  share of Hispanic-offender victims who are not Hispanic, by offense, and compare with the victim
  lane's assumption.
- Homicide is already on police-recorded SHR in the victim lane; show NIBRS homicide as a check,
  not a replacement.

## Output

- `RESULT.md` opening with `**Verdict:**`; tables of offending rates and ratios by offense with
  bounds; the victim-cost central re-run on these inputs (reuse `crime_victim_cost_2026_09_23`
  prices and structure; import or replicate its arithmetic, do not edit that lane).
- Every number tagged `[SOURCE]`, `[DATA]`, `[CALCULATION]` or `[INFERENCE]`; report every
  specification computed.
- Scripts and `derived/*.csv` aggregates only. Write only in this directory. Do not commit.
