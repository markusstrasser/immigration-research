# Brief: military and public service by Indian and Mexican origin, per capita and at equal SES

Date: 2026-09-23. Operator, verbatim: "Also check how many of indians and mexican per capita serve
in militrary or the like ... also adjusted for SES/wealth".

## Build on (read first; extend, do not redo)

- `civic_service_by_ancestry_2026_09_21/` (`service.py`, `RESULT.md`, ladder 170): US-born men by
  first-reported ancestry, ACS 2024 PUMS via the Census tabulate API, `MIL` 1 or 2. Asian Indian
  1.05% (se 0.21) against 6.6–7.8% for English, German, Irish at 18–49; Mexican 5.7% overall and
  8.2% among degree holders. Its limits: one year, binomial SEs, men only, US-born only, parental
  income and place not held constant.
- Ladder 152 and its lane: CPS civic supplement, India-born give and volunteer about 20 points less
  than white graduates at equal education.

## Estimate

1. **Military service per capita**, by group, sex and age band (18–49, 25–49, 25–34), and among
   post-draft cohorts only (born 1956 or later) when older ages are shown:
   - Groups: US-born Mexican ancestry or Hispanic-origin Mexican (`HISP` 02); Mexico-born
     (naturalized citizens and all); US-born Asian Indian ancestry; India-born (citizens and all);
     US-born non-Hispanic white; all US-born. Men and women.
   - Ever on active duty (`MIL` 1–2), now on active duty (`MIL` 1), reserve or Guard training only
     (`MIL` 3). ACS 2024 plus 2022–2023 pooled for precision; 80 replicate-weight SEs.
   - Military barracks are group quarters; say whether GQ persons are in the universe.
2. **"Or the like"**: protective-service occupations (police, sheriff, corrections, fire, EMS;
   ACS `OCCP` codes) per 1,000 workers and per 1,000 adults by the same groups; and, from the CPS
   civic engagement and volunteering supplement (2021, 2023), formal volunteering and giving by
   Mexican origin (Mexico-born, second generation from parental birthplace, third-plus Hispanic
   Mexican) and India-born and second generation, against US-born non-Hispanic whites.
3. **Adjust for SES and wealth**, honestly:
   - Own education and income partly follow service (GI Bill, military pay), so they are not clean
     controls. Report raw, then adjusted in three ways and say what each can and cannot show:
     (a) within own-education strata (less than HS / HS / some college / BA+);
     (b) reweighted to the white reference's age × education × state × metro-size distribution;
     (c) an SES-expected rate: apply DoD recruits' distribution across home-neighbourhood income
     (DoD *Population Representation in the Military Services*, latest FY, accessions by home ZIP
     median income quintile; verify the table) to each group's distribution across the same
     quintiles, to get the rate each group would show if only neighbourhood income mattered.
   - For the CPS supplement, family income bracket and education are pre-determined enough to use
     as controls; report both raw and adjusted.
   - Say plainly whether the Indian and Mexican gaps survive each adjustment.

## Conventions

Census key in `infra/immigration-fiscal/acquire/config.local.env` (source it, never print it; pipe
URL-bearing output through `sed -E 's/key=[A-Za-z0-9]+/key=<KEY>/g'`; the API truncates silently,
so check totals against published tables such as ACS B21001 veteran counts). Raw pulls in
`_cache/` (add `.gitignore`). Tags `[SOURCE]`, `[DATA]`, `[CALCULATION]`, `[INFERENCE]`,
`[FRAMING-SENSITIVE]` (service is one costly behaviour, not a measure of patriotism). Evidence-
symmetry rules apply (`notes/quant-bias-checklist.md`). `RESULT.md` opens with `**Verdict:**`.
Write only in this directory; do not commit. Run with
`OPENBLAS_NUM_THREADS=1 uv run --no-project python3 <script>` from the repo root.
