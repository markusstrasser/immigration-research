# Lane brief, part 3: can any design here see a national channel?

Date 2026-09-28, 02:45 JST. Parent session immigration-research-1c. Part 2 is committed (rerun 18/18 identical).

## The hole

- Part 2 calls the regional panel "the main deconfounding design". Its country × cycle fixed effects remove every
  national shock, and a national channel of immigration is a national shock: teachers moved to welcome classes,
  money shifted to newcomers, curricula or standards lowered for everyone. So that design measures local exposure
  only. The same blind spot hides system-wide shifts in the US within-state designs.
- The between-country model can see national channels. Jointly it gives −1.6 (SE 4.7) per 10 pp, 95% CI about −11
  to +8. Times Germany's 12.3 pp, that runs from +9 to −13 native points, up to about 40% of the natives' −32.9.
  The regional CI (−13 to +7) is as wide.
- So part 2 moved the point estimate (about a quarter of the decline), not the interval (under a fifth to about
  half). The verdict's "no design here that removes national shocks supports it" is true by construction.

## Tests (bounded; append to `RESULT.md` under "Part 3: national channel" after each)

1. **Pre-pandemic window, 2015→2018.** The 2015–16 asylum wave arrived before PISA 2018, and the pandemic came
   after it.
   - Regress natives' change 2015→2018 (math, reading, science) on the size of the wave. Control for the natives'
     2012→2015 change (pre-trend) and the 2015 level.
   - Measure the wave two ways: (a) first-time asylum applicants in 2015–2016 per capita (Eurostat
     `migr_asyappctza`, Europe only); (b) the change in the first-generation share of 15-year-olds, 2015→2018
     (PISA).
   - Natives' country means: 2012 and 2018 from the 2022 Vol I tables already parsed; 2015 from PISA 2015 Vol I
     Table I.7.15a/b/c (`_cache/statlink_888933433226`). Flag the 2015 switch to computer-based testing: it sits in
     the pre-trend.
   - Use the bounded Swedish values for 2018.
   - Report slopes per 1% of population (asylum) and per 10 pp (share), with HC1 SEs, n and leave-one-out ranges.
     Show the residuals for Germany, Austria and Sweden.
2. **Power.** For each design (part 2's joint cross-country model, the regional panel, and test 1), give the
   smallest effect it could detect at 80% power, both per 10 pp and as a share of Germany's native decline.
3. **Verdict update.** Say which designs can see a national channel and which cannot. State Germany's immigration
   share of the 2012→2022 decline as an interval with a point estimate, not a point alone. Note that Spain alone
   gives −24.7 (7.6) and Canada +1.9 (6.0). Say whether pooling selected immigration (Canada) with unselected
   immigration (Spain) dilutes the slope that applies to Germany's 2015 arrivals.

## Rules

- Same lane and rules as `BRIEF.md` and `BRIEF_2.md`. Scripts write to `derived/`; raw pulls go in `_cache/`.
  Two runs must be byte-identical.
- Quote every input in `reads/`; tag every number. Use Exa or direct HTTP with a generic User-Agent and no
  personal identifier.
- No commits, staging or stash. If the turn cap nears, write what is done and the next queries first.
- Final message: the RESULT path and at most ten lines.
