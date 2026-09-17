**Verdict:** No usable author-primary dataset for the 2015 Swiss political-integration study was located in this bounded search. No reduced form, first stage, knowledge or efficacy coefficient was independently reproduced. This is an access/discovery limit, not evidence against the paper.

Date: 2026-09-17. Target: Hainmueller, Hangartner and Pietrantuono, PNAS 112(41), DOI 10.1073/pnas.1418794112. Public sources only; no accounts, payment or external contact.

## What was actually checked

| Primary route | Observed result | Interpretation |
|---|---|---|
| [Hainmueller's current publication page](https://j-hai.github.io/publications/#hainmueller2015naturalization) | Exact article entry has DOI/HTML/PDF links, no replication link. Page saved and SHA256 logged. | Does not establish that no author archive exists elsewhere. |
| [Pietrantuono's research page](https://www.pietrantuono.net/research.html) | Article entry has bibliographic information, no data link. | Another author route checked; not an availability guarantee. |
| [PMC article and Associated Data section](https://pmc.ncbi.nlm.nih.gov/articles/PMC4611668/) | Only the 4 MB supporting PDF is listed; no tabular/archive dataset appears. Main HTML saved. | The article's displayed data links do not expose respondent data. |
| [PMC supplement](https://pmc.ncbi.nlm.nih.gov/articles/instance/4611668/bin/pnas.1418794112.sapp.pdf) | HTTP download returned an HTML “Preparing to download” page rather than PDF bytes; web open also failed. | Failed transport/content validation; not a successfully acquired supplement. |
| Harvard Dataverse public API search for Naturalization | HTTP 403. Dataverse author-page web opens also failed. | Cannot claim a complete Dataverse search. No authentication was attempted. |
| Exact-title web searches plus “replication”, “dataverse”, “zip”, and DOI | Found paper listings and unrelated citizenship datasets; no identified archive for this study. | Search absence is bounded evidence, not proof of nonexistence. |
| Legacy Stanford author research URLs | Web tool returned errors. | Historical author hosting remains unresolved. |

## Reproducible access record

`acquire.py` accepts `--output-dir` and an optional `--urls-json` filename-to-URL mapping. It logs URL, final URL, byte count and SHA256 for successful responses, and explicit errors for unsuccessful requests. It rejects PDF targets without `%PDF-` magic; the check includes a regression assertion for HTML download pages. Any failed retrieval exits nonzero with `DEGRADED`. Run with `uv run python3 acquire.py --output-dir OUT` from a network-enabled environment. `acquisition.json` records the executed probe.

The initial misleading `.pdf` response is preserved under its truthful HTML extension. `author_publications.html` and `pnas_main.html` are source snapshots, not microdata. No synthetic data, recovered scatterplot points or paper coefficients were substituted for respondents.

## Handoff and stopping rule

[GAP] A specific author/publisher repository record containing applicant-level vote margin, eventual citizenship, political knowledge/efficacy, design covariates and sample flags is still required. An exact archive URL would be more useful than more title searches. If obtained, first validate sample/count/scale benchmarks, estimate the referendum-win reduced form and citizenship first stage on identical samples, then their IV ratio with appropriate uncertainty; keep the whole-sample covariate IV distinct from threshold-local fuzzy RD.

No further paper summary was added. Other citizenship datasets encountered were not substituted because they target different interventions/outcomes. No new claims about institutional performance or immigrant admission follow from this unsuccessful replication attempt.

Covered files: `acquire.py`, `acquisition.json`, `author_publications.html`, `pnas_main.html`, and unexpected-response HTML. Skipped: regression code and numerical output because verified respondent data are absent. All earlier social outputs and repository files were preserved.
