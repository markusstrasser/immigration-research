# US low-skill immigration effects: fourteen papers read in full

Date: 2026-09-22. Reading lane, no computation. The memo is
[`research/immigration-us-lowskill-effects-integration-2026-09-22.md`](../../../research/immigration-us-lowskill-effects-integration-2026-09-22.md).

## Contents

- `derived/effect_ledger.csv` — one row per paper: DOI, corpus id, population, outcome,
  headline estimate, the abstract sentence it comes from, and the parser used. Built by the
  acquisition session that pulled the PDFs into the corpus.
- `reads/BRIEF.md` — the extraction brief given to each reader.
- `reads/<paper>.md` — fourteen extraction files, one per paper, written by one opus-low
  agent each from the full parsed text. Each numeric row carries a verbatim quote that the
  reader re-found in the parsed file with `rg -F` before finishing; the count of verified
  rows is at the end of each file. The parent re-found the rows the memo quotes (the
  Clemens–Lewis interval, the Burstein footnote, the Caiumi–Peri no-diploma cell, the
  Piyapromdee low-skill elasticity, the Monras, Dee–Murphy, Bracero and Wilson–Zhou
  headline rows) in the corpus texts independently.

## Corpus paths

Texts are in `~/Projects/corpus/<corpus_id>/parsed.*/page.md`; the `corpus_id` column of
`effect_ledger.csv` gives the directory. The Bracero paper is a marker-modal parse; the
rest are pymupdf4llm. Borjas, "The Labor Supply of Undocumented Immigrants", has a PDF
whose parse is the journal cover sheet only and was not read.

## Data on disk (ignored `sources/` tree)

- `sources/immigration-fiscal/data/external/stage3/harvard-dataverse/bracero-aer-2018/` —
  AER replication package (doi:10.7910/DVN/17M4ZP), Stata data and do-file, hashes in its
  `ACQUIRED.md`. Not executed.
- `sources/immigration-fiscal/data/external/stage3/immigrationshock/ancestry-instruments/` —
  the public county and DMA ancestry shift-share instruments cited by Wilson and Zhou. Their
  paper uses these only as a rejected alternative (first-stage F 6.80); the preferred design
  needs restricted immigration-court microdata that are not on disk.

## Not downloaded

East, Hines, Luck, Mansour and Velásquez (JOLE, Secure Communities); Christopher (JPAM,
undocumented rent premium); Mahajan (firm exit).
