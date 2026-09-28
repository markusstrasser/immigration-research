# Brief: replacement counterfactual — 40.9M non-Hispanic whites instead of the union

Operator, 2026-09-28 22:10 JST: "it would make sense to not be unfair and say that having that same
amount 40M be native whites ... would it be synergistic (sublinear) or superlinear costs ... whites would
then collaborate and likely produce lots more value on average at the long tails and in infra and tech".

## Estimand

The adopted September 27 case prices **removal**: other residents' gain if the Mexican-origin union
(40.9M) were absent and services scaled down. This lane prices **replacement**: the union against
40.9M additional non-Hispanic white residents, under the same rules (same responses, same capital
return, same keys method). Replacement delta = cost to others of the union − cost to others of the
white population of equal size (a negative cost = the whites leave others better off).
This is an accounting comparison, not a policy scenario [FRAMING-SENSITIVE]; say so in the RESULT.

## Parts

A. **Fiscal re-key (core).** Reuse `black_comparator_rough_2026_09_28/rekey.py` (copy into this lane,
   do not edit the original; keep its engine-line input `derived/engine_lines.json`). Re-key to:
   (A1) third-plus NH whites, (A2) all US-born NH whites, each scaled to 40.9M, at their own age
   structure; (A3) white per-age rates at the union's age structure; (A4) at a stationary life course
   if cheap. Run the same code on the union and report the rough-method vs engine gap (entry 259 found
   3–7% on cost) so the delta is like for like. Report per line (taxes, Medicare, Social Security,
   Medicaid, schools, justice, per-head lines, capital return), totals at specs 48 / 11, per member.
   Whites are older: show the old-age lines separately, and state how the cash basis treats an older
   population vs accrual (ladder 257); size the accrual effect if SSA ratios in
   `pension_accrual*` lanes can be applied, else name it.
B. **Schooling and scale spillovers.** `scale_spillovers_2026_09_23` (ladder 201) prices city size and
   the schooling-mix externality for the union. Scale is the same for any 40.9M; rerun the schooling
   term with the white population's schooling (college share etc.) and report the CRY-netted central
   plus the literature arms (Moretti, Iranzo–Peri, Ciccone–Peri) exactly as 201 does.
C. **Innovation / long tail.** 201 notes Burchardi et al. (no patent response at 9.7 years of
   schooling). Score the white population on the same response if the lane's machinery allows;
   otherwise report inventor rates per capita by education and group from a primary source
   (Bell–Chetty et al. "Lost Einsteins" tables, or USPTO/PatentsView if local) with the interval.
   No training-data numbers as inputs; tag anything unverified.
D. **Sub- or superlinear, channel by channel.** For each channel give the scaling exponent the repo
   already measured (general government 0.84, roads 0.73, parks 0.95, schools ~1, congestion delay
   curve, rent +1% per 1% population, city-size premium 0.0254 per log point) and say whether cost per
   added person rises or falls with total size, and whether geography (the union's CA/TX/LA
   concentration vs the white settlement pattern) changes it. Rerun congestion and housing with white
   settlement shares only if the existing lanes take a share vector as input; otherwise state the
   direction and why.
E. **Crime victims.** `victim_cost.py` re-keyed to NH white offenders, same prices (Miller victim-only),
   cost borne by non-group victims.

## Rules

- Lane dir: `infra/immigration-fiscal/white_replacement_2026_09_28/`. Scripts at lane root, outputs in
  `derived/`, raw pulls in `_cache/`. CSV with `lineterminator="\n"`.
- Run with `OPENBLAS_NUM_THREADS=1 uv run --no-project python3 …` from the repo root.
- Every number tagged `[DATA]`/`[CALCULATION]`/`[SOURCE]`/`[INFERENCE]`. Disconfirmation section:
  what would make whites look worse than expected (age, Social Security, Medicare, geography).
- Rerun every script twice; outputs byte-identical. Do not edit other lanes, the ladder, INDEX or
  memos, and do not commit: the parent integrates and commits.
- Write `RESULT.md` first and append as you go; after the model-ID line its first content line opens
  with `**Verdict:**`. Return its path and ≤10 lines.

Parent's pre-stated expectation (recorded before any run): the fiscal replacement delta (A1) lands
around $420–580bn a year on cash; the white old-age lines cut the white advantage noticeably on
cash and less on accrual; B adds a positive schooling term with a very wide interval; D finds most
cost channels roughly linear, infrastructure and administration sublinear, congestion and rents
superlinear where the population concentrates.
