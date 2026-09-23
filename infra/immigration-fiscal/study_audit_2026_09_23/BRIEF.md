# Study integrity audit — shared brief (2026-09-23)

Operator's ask: "check other studies we rely on that they're not FAKE or politicized (starts at data
capture)". Trigger: IZA DP 18374 (German jus soli and youth crime) was quoted as "cut boys' crime by
half"; on re-reading, the design was sound but the estimate imprecise (24 clusters, 95% interval
−16% to −125%) and the population wrong for the US question
(`research/immigration-generational-crime-mechanisms-2026-09-16.md` §3.1 revision).

## Your job, per study

1. **Repo claim.** Quote how the repo cites it (file:line) and what conclusion leans on it.
2. **Data capture first.** Write the pipeline: event → who records it → how the key variable
   (legal status, ethnicity, crime, benefit receipt, birthweight, diagnosis) is captured → residual
   or unknown categories and where they go → linkage/selection → count → denominator. Name the
   institution at each stage. For each stage give the sign of the likely error on the headline.
3. **Design and precision.** Identification, number of clusters, confidence interval of the number
   the repo quotes, whether that number is a point estimate from a noisy ratio, specification
   searching (many outcomes, subgroups), pre-registration.
4. **Replication and critique.** Published replications, comments, reanalyses, from both sides.
5. **Politicization signals.** Authors' and funders' advocacy ties; whether the abstract or press
   release says more than the tables; whether the repo accepted a critique of an opposite-side
   study that applies equally to this one (symmetry test).
6. **Verdict** — one of: SOUND · SOUND BUT IMPRECISE · MEASUREMENT RISK (state the direction) ·
   OVERSTATED IN REPO (quote the repo text and give the corrected wording) · DO NOT RELY.
   "Fake" means fabricated or unreproducible data; say explicitly whether any sign of that exists.

## Rules

- Primary sources: the paper's full text (check `~/Projects/corpus` and the research MCP first;
  `corpus_lookup`, `read_paper`, `fetch_paper`), its data documentation, published comments.
  Parse tables yourself for any number you report; AI summaries are leads, not evidence.
- Tag every claim `[SOURCE: …]`, `[DATA: …]`, `[INFERENCE]`, `[UNVERIFIED]`.
- Apply the same scrutiny to studies whose results cut against immigration as to those that favour it.
- Do not edit any repo file except your own result file. Do not commit.
- Your FIRST tool call writes a stub to your result file opening with
  `**Verdict:** PROBE IN PROGRESS [UNVERIFIED]`; add each study's section as you finish it.
- Budget: 12 turns. Do the studies in the order listed; list what you did not reach under Coverage.

## Result file format

`**Verdict:**` paragraph (which studies hold, which do not, the single most consequential problem) ·
one section per study (items 1–6 above) · a summary table
`Study | Repo use | Weakest pipeline stage | Precision | Politicization signal | Verdict` ·
`## Coverage` (done, skipped, why). Return the path and ≤10 lines, first line your model name.

Prior audits to reuse, not redo: `research/immigration-canon-citation-audit-2026-09-17.md` (labor
canon), `research/immigration-crime-statistics-bias-mechanisms-2026-09-16.md` (crime-statistics
pipeline, including Texas status-identification timing), `research/immigration-economist-dismantling-2026-06-25.md`.
