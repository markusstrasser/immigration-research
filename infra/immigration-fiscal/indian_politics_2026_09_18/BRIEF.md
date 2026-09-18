# Lane: how Indian Americans vote, what they want from policy, and what they give (2026-09-18)

## Questions
1. Vote and party: levels and trend 2008–2024, first vs second generation, by sex, religion and age.
2. Policy content, so "voting for what" is measured rather than asserted: redistribution and taxes, affirmative action, immigration levels and H-1B/green-card backlog, crime and policing, schools (gifted/selective admissions), speech and religion, India-related foreign policy. Where possible compare with US-born whites of the same education and income: the operator's question is whether a group with top-decile income votes like it. [FRAMING-SENSITIVE]: which positions count as bad policy is not this lane's call; report the positions.
3. Organised influence: officeholders by party, donations (OpenSecrets/FEC ethnic-surname studies), lobbying groups (USINPAC, HAF, Indiaspora, Indian American Impact), the US-India caucus, FARA filings; diaspora positions on Indian politics.
4. Giving: charitable giving and volunteering in the US vs to India; remittances US→India.

## Sources (pointers from memory: VERIFY each against the primary; report mismatches)
- Carnegie Indian American Attitudes Survey 2020 and 2024 (Badrinathan, Kapur, Vaishnav), YouGov panel: vote, party ID, issue items, caste, India attitudes. Get the toplines and any microdata.
- AAPI Data / Asian American Voter Survey 2012–2024 by national origin; Pew 2022–23 Asian American survey (Indian subsample); CES/CCES cumulative file if it carries Asian-origin detail (check the codebook; if yes, tabulate vote by origin × education × income against whites, weights on).
- Ballot measures with precinct or exit data by Asian origin: California Prop 16 (2020), Prop 209 history, Washington I-1000/R-88; SF recalls only if Indian-specific data exist (likely not: say so).
- Giving: Indiaspora–Dalberg giving reports (the "giving gap" claim: giving as share of income vs US average); Bridgespan on diaspora giving; World Bank/KNOMAD bilateral remittance matrix and RBI remittance survey (US share of India inflows); compare with `../remit_leak_2026_09_16/RESULT.md` conventions.
- The repo's `../attitudes_gen_2026_09_16/` ANES/GSS work: check whether Asian Indian cells are large enough to say anything (probably not; report Ns).

## Disconfirmation (mandatory)
Test the "rich but votes left" anomaly against composition: education (postgraduates of every race lean Democratic), metro residence, religion (non-Christian), age. If a matched white comparison removes most of the gap, say so. Test the 2020→2024 shift for survey-mode artefacts.

## Deliverables and rules
`RESULT.md` opening `**Verdict:**`, then a claim table (claim · source · sample N and mode · evidence level · verified Y/N), sources fetched vs skipped with reasons, scripts for any tabulation under this directory (`uv run --no-project --with pandas python3 <script>`; outputs to `derived/`), and a draft memo section. Tag every number; verbatim quotes only from fetched pages; save key sources with `save_source`. Read `CLAUDE.md` and `notes/llm-bias-caveat.md` first. Own only this directory; never edit `research/`; do not commit; no policy advice. At most 3 research epochs of 12 turns; update RESULT.md after each.
