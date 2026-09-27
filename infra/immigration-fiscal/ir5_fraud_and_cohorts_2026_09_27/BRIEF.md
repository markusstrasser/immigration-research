# Brief: are Mexican IR-5 "parents" fraud, or US-born children turning 21?

Operator question (2026-09-27): Mexican parents of US citizens (IR-5) rose from 34k (FY2019) to
63k (FY2024), a quarter of all IR-5, many adjusting inside the US — "sounds a lot like fraud".
Test both readings. Sister lane with the flow data: `infra/immigration-fiscal/late_arrival_tail_2026_09_27/`
(`derived/ir5_flow.csv`, FY2005–2024 by country; reuse it, do not re-fetch).

## Tasks

1. **Fraud evidence, primary sources only.** Find every measured fraud or misrepresentation rate
   for family-based and specifically parent (I-130 for a parent, IR-5) petitions: USCIS Benefit
   Fraud and Compliance Assessments (BFCA), USCIS FDNS reports, DHS OIG and GAO reports, State
   Department consular fraud-prevention statistics (refusals under INA 212(a)(6)(C)(i)), DNA-test
   request and failure rates if published, and prosecutions for fabricated parentage. Report each
   rate with population, year, method and page. Say plainly if no parent-specific rate exists.
   Do not quote any figure you did not read in the fetched document.
2. **Birth-cohort test.** US births to Mexico-born mothers by year, 1980–2005 (NCHS natality:
   CDC WONDER or the NBER/NCHS public natality files; mother's birthplace or Hispanic origin +
   nativity, whichever the year supports — document the field). Shift by 21+ years (the petitioner
   must be 21) and compare with Mexican IR-5 FY2005–2024: correlation of levels and changes, the
   predicted path to 2030, and what share of IR-5 the cohort model explains. Add the all-country
   IR-5 series to separate a Mexico-specific rise from processing backlogs (FY2021 COVID dip,
   FY2023–24 surge; cite State NVC / USCIS backlog statistics if found).
3. **Who adjusts.** What the law allows: which parents can adjust inside the US (lawful entry,
   INA 245(a), 245(i) grandfathering) and which must process abroad and face the 212(a)(9)(B)
   bars; the waiver rules (can a citizen child's hardship waive a parent's bar?). Quote the
   statute or USCIS Policy Manual text. Any published count of Mexican IR-5 adjustments vs
   consular issuances (State Visa Office annual report tables for IR-5 issuances by nationality).
4. **Disconfirmation both ways.** What evidence would show fraud (implausible parent ages,
   DNA failure rates, OIG findings) and what shows the cohort mechanism; report which survives.

## Outputs

- `RESULT.md` opening `**Verdict:**` (stub first, append as you go), sources covered/skipped.
- Scripts here; `derived/births_mexico_mothers.csv`, `derived/cohort_vs_ir5.csv`,
  `derived/fraud_rates.csv` (source, year, population, rate, page), one PNG of births-shifted vs
  IR-5 (look at it). `sources/` with archived text of every document a number comes from
  (ignore PDFs/HTML over 1 MB in `.gitignore`).
- `verify.py` for the gates; `.gitignore` with `_cache/`.

## Gates

- Total US births per year in your natality series within 0.5% of NCHS published totals.
- The IR-5 series is read from the sister lane's CSV, not retyped.

## Conventions

- `uv run --no-project python3 …` from the repo root; `--with <pkg>` literally if needed; check
  every script's exit code before comparing outputs.
- Fetch via `subprocess.run(["curl","-sS","--fail",...])`; validate content, not status.
- `csv.writer(..., lineterminator="\n")`. Source tags per `CLAUDE.md`.
- Do not commit; do not edit outside this directory. Return RESULT.md path and ≤10 lines.
