# Brief — Pew 2017 Survey of U.S. Muslims, microdata cuts by nativity and origin

Owner: the build agent. Files owned: this directory only (except BRIEF.md). No commits. No edits outside it.
Data (read-only): `sources/immigration-fiscal/data/external/pew/Pew-2017-US-Muslims.zip` (6,121,578 bytes, sha256 `1117f84325f3450e…` in `sources/immigration-fiscal/data/MANIFEST.md`): `2017USMuslimPublicData - checked.sav` (1,001 respondents, 222 variables), `Codebook`, questionnaire and full-report PDFs. Unzip into `_cache/` (git-ignored). Read the .sav with `pyreadstat` (`user_missing=True`), as `infra/immigration-fiscal/pew_outcomes_2026_09_20/analyze.py` does; use `weight` unless the codebook says a different weight applies to an item.
Context: `research/immigration-muslim-origins-funding-outcomes-2026-09-21.md` §2 quotes report-level figures (ids B1–B11: 58% foreign-born; 31% college; 24% income ≥ $100k; 40% < $30k; 37% homeowners; 12% killing civilians often/sometimes justified; 84% rarely/never; 52% homosexuality accepted; foreign-born degrees 38% vs US-born 21%). Reproducing those from the microdata is the gate; the new content is the cuts below.

## Steps
1. Reproduce every B-row above from the microdata with `weight` to within 1 percentage point; print each with the variable used and its label. A miss over 1 point is a finding to report, not to hide.
2. Cuts by nativity (`respondent_birthregion2` US-born vs foreign-born) and, for the foreign-born, by birth region; for the US-born, by parents' birth region (`father_birthregion2`, `mother_birthregion2`): income bands (`income`), education (`educrec`), citizenship (`citizen`), party (`party`, `partyln`), children ever born (`fertREC`), satisfaction (`qa2`), the civilians-justified item, the homosexuality item, discrimination and belonging items if present (locate by label), and any employment or public-assistance item if present (locate by label; say if absent).
3. Standard errors: weighted, with a design-effect adjustment if the methodology PDF states one (search it); otherwise report the weighted-SRS SE and say the design effect is unknown. Cells with n < 50 are reported with a flag.

## Gates
G1 zip sha256 matches. G2 1,001 rows, weight positive and finite. G3 all B-rows reproduced within 1 point or explicitly reported as misses. G4 every variable used is printed with its label in audit.json.

## Outputs
`derived/report_reproduction.csv`, `derived/cuts_by_nativity.csv`, `derived/cuts_by_origin.csv`, `derived/audit.json`, `analysis.py`, `test_analysis.py`, `README.md`, `RESULT.md` (opens with `**Verdict:**`; reproduction table first; then the nativity and origin cuts; gates; files; limits: self-identified Muslim adults, 2017, banded income, region-level birthplace, no replicate weights). Every number tagged `[CALCULATION: derived/<file>]`.

Verification commands (run all, paste tails into RESULT.md):
```sh
cd /Users/alien/Projects/immigration-research
UV_CACHE_DIR=/private/tmp/immigration-uv-cache uv run --offline --no-project --with pyreadstat python3 -m pytest infra/immigration-fiscal/pew_muslims_2017_2026_09_22/ -q
UV_CACHE_DIR=/private/tmp/immigration-uv-cache uv run --offline --no-project --with pyreadstat python3 infra/immigration-fiscal/pew_muslims_2017_2026_09_22/analysis.py
```
Return: the RESULT.md path and at most 10 lines (verdict; reproduction hits/misses; the largest nativity differences with SEs; files; anything skipped and why).
