# Brief: the selection curve — how far does a first generation's position carry to G2 and G3?

Operator question (2026-09-27): draw a curve from "how selected the immigrants are" (their
percentile) to where their grandchildren land (G3 percentile). And check whether high-skill
groups' advantage is a top-tail effect (a few very high earners) rather than a shift of the
whole distribution. The H-1B question is already answered (below); do not redo it.

## Already measured (cite, do not redo)

- Indian G1 fiscal gap +$10,732; top 1% excluded +$10,488; recent noncitizens (H-1B proxy)
  excluded +$13,397: `research/immigration-indian-origin-fiscal-coordination-politics-2026-09-18.md` §1.
- Indian G2/G3 gaps and the IT share of the G2 gap (8%/4%):
  `research/immigration-indian-later-generation-fiscal-2026-09-21.md`.
- G1→G2 by parental origin, 1994–2025 IPUMS-CPS ASEC (5.7M persons, parental birthplace):
  `infra/immigration-fiscal/second_generation_by_origin_2026_09_22/` (reuse its loader and
  data path `sources/immigration-fiscal/data/external/cps/cps_2ndgen.csv.gz`; check sha256).
- Observed G3/G4+ via grandparent linkage: `infra/immigration-fiscal/generation_split_2026_09_20/`.
- A sister lane running now measures the Mexican G1→G4+ carry-over:
  `infra/immigration-fiscal/generation_carryover_2026_09_27/` — do not duplicate its Mexican work;
  you may read its derived files at the end for a consistency check.

## Tasks

1. **Top tail vs whole-distribution shift.** For India-born, Indian G2, China-born, Philippines-
   born, Mexico-born and their G2 (CPS ASEC 2015–2025 pooled, adults 25–64, age-standardised):
   place each person in the US-born NH white earnings (and education-years) distribution of the
   same age band and year; report the group's percentile distribution (p10, p25, p50, p75, p90)
   and the mean percentile. Report the share of the group's mean-earnings gap and of the
   partial fiscal gap (reuse the Indian ledger's per-person nets if the lane exposes them;
   otherwise earnings only) contributed by persons above the white p99, p95, p90. Note the
   CPS topcode/rank-swap rules for the years used: the public files cannot see the extreme tail,
   so say what "without the top 1%" can and cannot mean here.
2. **Origin-level selection curve, G1 → G2.** For every parental birthplace with ≥ 150 G2
   adults 25–64 in the 1994–2025 file: G1 mean percentile in the white distribution (education
   and earnings, age/year-standardised) vs G2 mean percentile. Fit rank-on-rank across origins
   (weighted by G2 n, with bootstrap intervals) — slope, intercept, and where India, Mexico,
   China, Philippines, Vietnam, Nigeria, Korea, Cuba, El Salvador sit relative to the line.
3. **Selection relative to origin.** Where you can obtain origin-country education distributions
   (Barro-Lee, Wittgenstein Centre or IPUMS-International tabulations; fetch and pin them), compute
   each G1's percentile *within its origin country's* schooling distribution (Feliciano's
   selectivity) for the same ages. Plot origin-selection percentile → G1 US percentile → G2 US
   percentile. This is the "how selected" axis the operator asked for.
4. **G2 → G3.** Where any origin has an identifiable G3 (CPS grandparent linkage; GSS ETHNIC ×
   GRANBORN × PARBORN for European and Mexican origins; published historical estimates such as
   Borjas's ethnic-capital work and Abramitzky–Boustan–Jácome–Pérez 2021 AER rank-rank by origin),
   estimate the G2→G3 carry-over. Read every published number from the paper (table/page).
5. **The curve.** Combine 2–4 into p_selected → p_G1 → p_G2 → p_G3 with the measured slopes and
   intervals, labelled [MODEL] beyond G2. Mark India and Mexico on it. State which links are
   measured and which assumed.
6. **Disconfirmation.** Test whether the G1→G2 slope differs for high- vs low-selected origins
   (nonlinearity), whether it is driven by one origin (leave-one-out), and whether the G2
   advantage of high-selected groups is itself a top-tail effect.

## Outputs

- `RESULT.md` opening `**Verdict:**` (stub first, append as you go); every computed spec in a
  table; files/sources covered and skipped.
- `derived/percentile_distribution.csv`, `derived/tail_share.csv`, `derived/origin_curve.csv`,
  `derived/slopes.csv`, `derived/curve_projection.csv`; one PNG of the curve
  (`derived/selection_curve.png`, matplotlib, plain, labelled axes) — look at it before
  reporting.
- `verify.py` for the gates; `.gitignore` with `_cache/`.

## Gates

- Reproduce ladder 178's Mexican G2 no-HS gap (+11.8 points) from the shared loader before new work.
- Indian G1 top-1%-excluded direction matches the memo (gap stays ~+$10.5k) if you use the ledger.

## Conventions

- `uv run --no-project python3 …` from the repo root; `--with <pkg>` literally if needed.
- Fetch via `subprocess.run(["curl","-sS","--fail",...])`; validate content, not status.
- `csv.writer(..., lineterminator="\n")`. Source tags per `CLAUDE.md`.
- Do not commit; do not edit outside this directory. Return RESULT.md path and ≤10 lines.
