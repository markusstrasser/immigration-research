# Paper-reading brief (shared by every reader agent), 2026-09-21

You are reading ONE economics paper in full for the repository
`/Users/alien/Projects/immigration-research` (topic: fiscal impact of the Mexican-origin resident
population of the United States). Your output is one notes file. Do not commit. Do not edit any
repo file other than your own two cache files and your notes file.

## Method (required)

1. Download the primary PDF into
   `infra/immigration-fiscal/mr_leads_papers_2026_09_21/_cache/<slug>.pdf`
   (`curl -sL -A "Mozilla/5.0" -o …`). NBER pattern:
   `https://www.nber.org/system/files/working_papers/wNNNNN/wNNNNN.pdf`. If blocked, try author
   pages, SSRN delivery, IZA, CEPR or a university repository via web search. Check it with
   `pdfinfo` (pages, title).
2. `pdftotext -layout <slug>.pdf <slug>.txt`, then READ THE WHOLE TEXT in chunks with the Read
   tool (offset/limit): body, tables, footnotes, and the appendix robustness tables. Do not rely
   on abstracts, blog posts, press coverage or search summaries for any number.
3. Every number you report carries a page or table reference and a short verbatim quote of the
   row or sentence it comes from. If a table is garbled in the text, re-extract that page
   (`pdftotext -f N -l N -layout`, or `-raw`) and say you did. Never reconstruct a number from
   memory. If the PDF cannot be obtained after three routes, write the notes file with
   `**Verdict:** BLOCKED` and the routes tried. Do not substitute secondary sources.
4. Budget: at most 8 web searches and about 12 tool turns beyond the reading itself.
5. Steel-man the paper before criticising it. Report estimates that cut in either direction.
   No commentary on data licensing. Never print API keys or environment secrets.

## Notes file: `infra/immigration-fiscal/mr_leads_papers_2026_09_21/notes/<slug>.md` (≤ 250 lines)

```
**Verdict:** one paragraph: what the paper establishes, at what evidence level, and the single
most important caveat for transferring it to the Mexican-origin resident population.

## Citation and version      (authors, title, series and number, date, pages; later or published
                             version and whether estimates changed)
## Question, data, sample   (years, geography or unit, N)
## Identification           (design; instrument construction; first-stage F; what the authors do
                             about shift-share problems: Goldsmith-Pinkham–Sorkin–Swift,
                             Borusyak–Hull–Jaravel, Adão–Kolesár–Morales, the
                             Jaeger–Ruist–Stuhler serial-correlation critique; pre-trends, placebos)
## Main estimates           (table: outcome | estimate | SE or CI | units exactly as defined |
                             table/page | verbatim quote)
## Heterogeneity and mechanisms
## Robustness and what the authors concede
## Threats the authors do not address   (your assessment, each line tagged [INFERENCE])
## Answers to the repo's questions      (the numbered questions in your task message)
## Files covered / skipped              (pages read; anything skipped and why)
```

When done, reply with the notes file path and at most 10 lines.
