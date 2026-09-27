# Brief: attachment to the origin state — dual nationality, naturalization, Mexican politics

Operator question (2026-09-27): dual citizenship was raised as a concern for high-skill Indians
(India bars dual citizenship; OCI is a visa). For Mexican origin the legal situation differs.
Trace what is measurable about continuing legal and political attachment to Mexico across
generations, and how it compares with other large origins. Part of the first report on
low-skill Mexican migration. Research lane (sources, not microdata builds, except where a
public table can be tabulated).

## Questions

1. **Law.** What does the Mexican constitution (Art. 30, 32, 37) and the 1998 reform
   ("no pérdida de la nacionalidad") provide? Are US-born children (and grandchildren) of
   Mexican nationals Mexican nationals by birth, and what registration is needed? What rights
   and duties follow (vote abroad, property, military service obligations)? Compare India
   (Citizenship Act 1955 s.9; OCI rules) and one or two other large origins (Philippines RA 9225,
   China). Quote the statutory text from official sources.
2. **Uptake.** Counts with sources and years:
   - INE voto de los mexicanos residentes en el extranjero: registrations (LNERE) and votes cast
     from the US, 2006, 2012, 2018, 2024; as a share of the eligible Mexico-born adult
     population in the US.
   - Matrícula consular issuance per year (SRE/IME).
   - Registrations of US-born persons as Mexican nationals (inscripción de nacimiento at
     consulates / Registro Civil "doble nacionalidad") if published.
   - Naturalization: DHS OHSS estimates of LPRs eligible to naturalize by country and the share
     of eligible Mexican LPRs who have naturalized vs other origins; Pew or MPI naturalization
     rates by origin with their definitions. If ACS citizenship by years in the US can be
     tabulated through the Census API (`set -a; . infra/immigration-fiscal/acquire/config.local.env; set +a`,
     never print the key), add it, noting that unauthorized residents cannot naturalize and
     separating that with the repo's status imputation
     (`infra/immigration-fiscal/status_impute_2026_09_16/`) where possible.
3. **Political attachment by generation.** Survey evidence (Pew National Survey of Latinos,
   LNS, CMPS, held Pew files listed in `research/immigration-dataset-register.md`) on: holding
   Mexican nationality, following Mexican politics, sending remittances, identifying as
   "Mexican" vs "American" first, by generation. Use held microdata where the register lists
   it; otherwise published tables with page citations.
4. **The Mexican state's diaspora policy.** IME, consular network size, documented Mexican
   government positions on US immigration or political matters addressed to the diaspora.
   Facts with primary sources only; no characterisation of motives.
5. **Disconfirmation.** Evidence that dual nationality or origin-state ties reduce US civic
   integration, and evidence that they do not (e.g. naturalization or US turnout among dual
   nationals vs others; the literature on dual citizenship and naturalization — Mazzolari 2009,
   Naujoks, etc. — read the papers, record findings with page numbers).

## Outputs

- `RESULT.md` opening `**Verdict:**` (stub first, append as you go): one section per question,
  a table of counts with source URL and year, the law comparison table, and a "what is not
  measurable" list. Files/sources covered and skipped with reasons.
- `sources/` with archived copies (or `save_source` via research MCP) of every page or PDF a
  number comes from. `derived/*.csv` for any tabulation.

## Conventions

- Every number: `[SOURCE: url, table/page]` read from the fetched document, never from memory.
- Use Exa/Firecrawl/research MCP; prefer official .gob.mx, ine.mx, dhs.gov, uscis.gov PDFs.
- `csv.writer(..., lineterminator="\n")`.
- Do not commit; do not edit outside this directory. Return RESULT.md path and ≤10 lines.
