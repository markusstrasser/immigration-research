# ft.dk REU alm. del spm. 291 (samling 20191), svar 1618048, bilag 2123368.pdf

[SOURCE: https://www.ft.dk/samling/20191/almdel/reu/spm/291/svar/1618048/2123368.pdf]

Retrieval: direct `curl -L` and headless Chrome (agent-browser) both returned the Cloudflare
"Just a moment..." interstitial, never the PDF (2 attempts each). Obtained via Firecrawl
`firecrawl_scrape` with `parsers:["pdf"], proxy:"stealth", maxAge:0` on 2026-09-16.
PDF metadata returned: title "REU Alm.del - endeligt svar på spørgsmål 291 : Bilag.pdf", 4 pages.
Numbers below transcribed by hand from that parse into `table1_transcribed.csv`.

## What the document actually is

Two tables, both on the SAME closed cohort:

- **Tabel 1** — "Mænd fra årgang 1985, 1986 og 1987 i befolkningen og [heraf] med mindst en dom
  efter straffeloven, fra deres 15-30 år, efter oprindelsesland og herkomst."
  Men born 1985/1986/1987, resident in Denmark, with **at least one criminal-code (straffelov)
  conviction between ages 15 and 30**, by country of origin (oprindelsesland) and
  ancestry (Danish / immigrant / descendant).
- **Tabel 2** — same cohort, at least one conviction under straffeloven **or** særlove
  (special acts) **or** færdselsloven (Road Traffic Act).

Denominator = everyone of that origin in the birth cohort, not arrests, not charges.
So the statistic is **cumulative lifetime-to-30 conviction prevalence**, not an annual rate
and not a conviction-per-arrest ratio.

## Totals (transcription self-check, both exact)

| | population | with >=1 conviction | share |
|---|---|---|---|
| Tabel 1, all origins | 84,848 | 16,730 | 19.7% |
| Tabel 1, Denmark | 78,120 | 14,043 | 18.0% |
| Tabel 2, all origins | 84,848 | 44,942 | 53.0% |
| Tabel 2, Denmark | 78,120 | 40,099 | 51.3% |

Sum over the 63 country rows reproduces the printed "I alt" row exactly for both
population (84,848) and convicted (16,730).

Pueyo's chart is **Tabel 1** (criminal code only).
