# Brief — Mexico-born returnees against Mexico-born people still in the US (ENADID × ACS)

Lane directory: `infra/immigration-fiscal/return_vs_us_stayers_2026_09_26/` (you own only this
directory, plus one new file `sources/immigration-fiscal/data/external/acs_pums_years/csv_pus_2023.zip`).
Written 2026-09-26 by the parent session that runs the weekly-audit corrections.

## The question

Ladder 174 and `enadid_return_selectivity_2026_09_22/RESULT.md` show that Mexico-born adults who
lived in the US five years before an ENADID survey and are back in Mexico hold about one year less
schooling than Mexico-born adults **who never left Mexico**. The weekly audit
(`decisions/2026-09-25-weekly-audit-corrections.md`, "Revisit if") withdrew any reading about the US
side: the sign against emigrants **still in the US** is not established. This lane measures it.

Are returnees less or more schooled than the Mexico-born who were in the US at the start of the same
five-year window and are still there at its end? A negative gap means exit removes the less schooled
and the remaining US stock is positively selected by return; a positive gap means the reverse.

## Design

1. **Returnee side: reuse, do not recompute.** Read ENADID returnee schooling from the tracked
   `enadid_return_selectivity_2026_09_22/derived/return_migrants_by_schooling.csv`: group
   `returnee_from_us`, waves 2018 and 2023, slices `all`, `sex:*`, `age:*`, `sex:*|age:*`, the four
   bands (`lt_lower_secondary`, `lower_secondary`, `upper_secondary`, `tertiary`), plus
   `mean_years_schooling`, with SEs and `weighted_pop`. Band definitions are INEGI `niv_esc`
   (see `BANDS` in `enadid_selectivity.py`): below lower secondary means fewer than 9 completed years;
   lower secondary is complete secundaria and nothing more; upper secondary is any approved grade of
   media superior; tertiary is any approved grade of superior. Mean years come from `esco_acum`.
2. **Stayer side: ACS one-year person PUMS for the same survey years.**
   - 2018: local `sources/immigration-fiscal/data/external/acs_pums_years/csv_pus_2018.zip` (read-only).
   - 2023: not local. Fetch `https://www2.census.gov/programs-surveys/acs/data/pums/2023/1-Year/csv_pus.zip`
     (about 600 MB) into `acs_pums_years/csv_pus_2023.zip`, modelled on
     `arrival_cohorts_2026_09_18/download_missing_acs_years.sh` (HTTP/1.1, content-length check,
     `unzip -tqq` verify, write to `.part` then rename, append a line with the sha256 to that directory's
     `download.log`). Put your fetch script in the lane directory. No Census API key is needed.
   - Universe: `POBP == 303` (Mexico), `AGEP` 20–64. **Main:** `YOEP <= year - 5` (in the US at the start
     of the window). Sensitivity: `YOEP <= year - 6`. Keep group quarters in; report the share in GQ.
   - Weights: `PWGTP`; standard errors from the 80 replicate weights with the ACS successive-difference
     formula, SE² = 4/80 · Σ(rep − full)². Keep negative and zero replicate values.
3. **Harmonize schooling.** Reuse the ACS `SCHL` → years scale and band logic of
   `schooling_selection_position_2026_09_23/` (read `acs_pums_check.py`, `levels.py`, `RESULT.md`; import
   rather than copy if the functions import cleanly). Main mapping to the ENADID bands: `SCHL` ≤ 11 →
   below lower secondary; 12 → lower secondary; 13–17 → upper secondary; 18 (some college, under one
   year) → upper secondary; 19–24 → tertiary. Sensitivities, each reported separately:
   - (a) `SCHL` 18 counted as tertiary;
   - (b) half of `SCHL` 16–17 (US high-school diploma or GED) re-read as Mexican secundaria, the
     re-reading that lane already uses;
   - (c) records with allocated schooling (`FSCHLP == 1`) dropped.
4. **Standardize.** Composition differs, since returnees are older and more male. Report, for each wave:
   - by sex, the stayers reweighted to the returnees' age-band distribution within sex;
   - pooled, the stayers reweighted to the returnees' sex × age-band cells, using the returnee
     `weighted_pop` by cell from the ENADID file;
   - the unstandardized raw figures beside them.

   The differences are returnee minus stayer. Because the samples are independent, SE =
   sqrt(se_ret² + se_stay²). For the pooled standardized figure, a delta-method or replicate-based
   SE on the stayer side is enough; treat the ENADID cell SEs as independent.
5. **Undercount check.** The ACS undercounts unauthorized residents, who are less schooled, and that
   biases the stayer distribution upward. Rerun the main comparison with non-citizens (`CIT == 5`) in
   the two lowest bands up-weighted by 1.10, 1.25 and 1.75. The last is the most severe factor the
   schooling-selection lane used. Report whether the sign of the tertiary and mean-years gaps survives.
6. **Secondary comparison: short-stay returnees.** People who left inside the window and came back hold
   more schooling (`departures_by_schooling.csv`, group `returned`, `linked_schooling_share_20_64`:
   28.1% tertiary in 2018, 22.6% in 2023). Compare them with ACS Mexico-born people who arrived inside
   the window and are still in the US: `YOEP` from `year - 5` to `year`, ages 20–64. Read the ENADID
   file's own caveats on linkage coverage first, then state what the comparison can and cannot show.
7. **Anchors, a build gate before any result.** Reproduce the ACS published Mexico-born population
   for 2018 and 2023 (table B05006, Mexico row, one-year) from the PUMS weights within 0.5%. Take the
   published figure from the Census API table endpoint without a key if it answers; otherwise use
   data.census.gov. Record the URL and value in `derived/anchor.csv`. PUMS totals differ slightly from
   the tables, so explain any gap over 0.2%. Also gate that every ENADID number you read matches
   `enadid_return_selectivity_2026_09_22/RESULT.md`'s tables, for example the 2018 returnee tertiary
   share of 11.18%.

## Outputs

- `compare.py` (plus `fetch_acs_2023.sh`), `test_compare.py` (pytest: band mapping, SDR formula on a
  toy case, standardization weights summing to one, gates that fail loudly).
- `derived/stayers_by_schooling.csv`, `derived/comparison.csv` (wave, slice, spec, band or measure,
  returnee, stayer, difference, se), `derived/anchor.csv`, and `derived/audit.json` (input sha256s,
  row counts, GQ share, allocated share). Use `csv.writer(..., lineterminator="\n")` or pandas
  `to_csv(..., lineterminator="\n")`.
- `README.md` (how to run) and `RESULT.md` opening with `**Verdict:**`. Give the sign and size, by sex,
  of the tertiary and mean-years gaps against US stayers for both waves, and say whether the sign
  survives every sensitivity. Add a table for each wave and a "What this does not show" section:
  schooling is measured at the survey; the five-year window is not a trend; the ACS covers
  residents, not all stayers; ENADID returnees include deportees. Put a `Model self-report:` line
  with your model id under the verdict, as the other lanes do.
- Tag every number with `[DATA: …]`, `[CALCULATION: …]` or `[SOURCE: …]` as the repo constitution
  requires (`CLAUDE.md` at the repo root).

## Rules

- Run from the repository root:
  `OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/return_vs_us_stayers_2026_09_26/compare.py`
  and `uv run --no-project python3 -m pytest infra/immigration-fiscal/return_vs_us_stayers_2026_09_26/ -q`.
  Then run the script a second time and confirm every file in `derived/` is byte-identical (`shasum`);
  read the exit code first.
- Read the zipped CSVs with pandas `usecols` so memory stays low (SERIALNO, SPORDER, POBP, AGEP, SEX,
  SCHL, FSCHLP, YOEP, CIT, RELSHIPP or RELP, TYPE/TYPEHUGQ if present, PWGTP, PWGTP1–80). The 2018 zip
  holds two person files (`psam_pusa.csv`, `psam_pusb.csv`); check the member names.
- Hard gates raise and stop; never downgrade a failed gate to a warning; no silent fallback.
- Do not edit any file outside your lane directory except to add the one 2023 zip and its
  `download.log` line. Peer sessions share this checkout. **Do not commit**; the parent integrates.
- If a design choice above turns out to be wrong on contact with the data (for example, `YOEP`
  coding differs by year), fix it, say so in RESULT.md, and keep going.

## Return

Your final message: the RESULT.md path and at most 10 lines: the verdict, the anchor gaps, whether the
rerun was byte-identical, test status, and anything you could not do.
