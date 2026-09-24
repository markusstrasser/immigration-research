# Brief: which way do the crime ratios err, and by how much?

Lane: `infra/immigration-fiscal/crime_ratio_direction_2026_09_24/` · dispatched 2026-09-24 13:55 CEST

## Question

Most known errors in the offending ratios seem to lean one way:

- offenders of unknown ethnicity lean Hispanic (the NIBRS lane's own finding,
  `offender_ethnicity_nibrs_2026_09_23/RESULT.md`, section "Unknown ethnicity and recording");
- homicides with Hispanic victims are cleared at 64% against 84% for white victims
  (`research/immigration-homicide-victim-offender-and-treasury-cost-2026-09-18.md`, as cited in
  `research/immigration-first-generation-crime-cost-weighted-2026-09-18.md:45`);
- jails record Hispanics as 14.4% of inmates against 18.4% of adults and 22.1% of adult arrests
  (`dataset_integrity_2026_09_23/README.md`, "Categories and coding");
- within-group victims (70–81% of Hispanic offenders' victims are Hispanic) may report less.

One item runs the other way: constructions that subtract all Hispanics from White overstate
Hispanic ÷ NH-white arrest ratios by 1–5%. The NIBRS murder ratio against non-Hispanic whites is
2.30 central (1.53 with every unknown offender non-Hispanic, 3.93 with every unknown Hispanic). Test
the direction and put a size on the net.

## Read first (build on these; do not redo them)

`offender_ethnicity_nibrs_2026_09_23` (RESULT.md, `derived/`, TX/AZ/CA 2022–23 NIBRS zips and staged
files in `_cache/`, `nibrs_rates.py`, `shr_benchmark_check.py`, `victim_cost_rerun.py`);
`homicide_cost_2026_09_18` (clearance conditioning, SHR inputs); `ncvs_victim_offender_2026_09_18` and
`research/immigration-ncvs-victim-offender-off-the-murder-margin-2026-09-18.md` (NCVS perceived
offender ethnicity); `crime_victim_cost_2026_09_23` (victims' harm, about $29bn);
`dataset_integrity_2026_09_23/crime.md` and `crime_*.py`; FAQ 12 in
`research/immigration-objections-faq-2026-09-21.md`. Positive control first: reproduce the NIBRS
lane's murder ratios (2.30 central; 1.53 and 3.93 bounds) before any new method.

## Arms

1. **Victim-conditional imputation of unknown offenders.** In incidents with a known offender,
   estimate P(offender Hispanic | victim ethnicity, offence, and where the data allow weapon,
   circumstance, victim age and sex, agency). Apply it to incidents whose offender is unknown, by
   their victims' ethnicity. Homicide first (NIBRS TX/AZ, and SHR nationally if the local SHR
   supports it), then robbery and aggravated assault. Compare the resulting Hispanic ÷ NH-white and
   Hispanic ÷ all-resident ratios with the lane's central and both bounds. Check in these agencies
   whether clearance really differs by victim ethnicity.
2. **Victim survey against police records.** NCVS perceived offender Hispanic origin for robbery,
   aggravated assault and simple assault (pool years as needed; follow the NCVS lane's data route),
   including crimes never reported to police. Compare NCVS's Hispanic ÷ NH-white offending ratio with
   NIBRS's for the same offences, and state the geography mismatch.
3. **Reporting to police.** NCVS reporting rates by victim ethnicity and by perceived offender
   ethnicity. If crimes with Hispanic offenders or victims are reported less, police-based ratios
   understate.
4. **Jail ethnicity recording.** Size the under-recording: the BJS jail Hispanic share against arrest
   shares, ACS correctional group quarters, and any state jail system that records ethnicity
   separately and publishes it. Say what a corrected jail share does to the justice-by-use line (the
   audit's BJS arm is +$2.45bn).
5. **The counter-direction item.** Test the White-race coding subtraction (1–5%) in the same frame
   so the reported net includes it.

## Deliverables

- `derived/ratio_adjustments.csv`: offence, method, Hispanic ÷ NH white, Hispanic ÷ all, change
  against the central.
- Scripts and one `test_*.py` with the positive control.
- `RESULT.md`: net direction and size for the murder and robbery ratios, and the dollar implications
  for the justice key (inside the account) and victims' harm (beside it).

## Rules (all lanes)

- Own only this lane directory. Do not edit anything else (memos, INDEX, ladder, FAQ, other lanes'
  code or outputs). Do not commit; the parent re-runs and integrates.
- First action: write `RESULT.md` opening `**Verdict:** (pending)`; update it as you go.
- Raw pulls go to `_cache/` (gitignored). Tracked outputs: scripts, `derived/*.csv` written with LF
  line endings (`lineterminator="\n"`), README/RESULT. Read other lanes' `_cache/` files in place;
  do not copy large files.
- Fetch with `subprocess.run(["curl", "-sS", "--fail", ...])`; Python urllib fails TLS on this
  machine. Validate content (row counts, expected columns and keys), never status or size alone.
- Census API key: `set -a; . infra/immigration-fiscal/acquire/config.local.env; set +a` exports
  `CENSUS_API_KEY`. Never print it; redact URLs in logs and errors
  (`sed 's/key=[^&]*/key=REDACTED/'`); never run `ps` or `pgrep -f` dumps.
- Run Python from the repo root `/Users/alien/Projects/immigration-research` with
  `OPENBLAS_NUM_THREADS=1 uv run --no-project --with pandas --with numpy python3 <script>` (add
  `--with` packages as needed; write each `--with pkg` literally).
- Tag every number in RESULT.md: [SOURCE: url + page/table], [DATA: local file],
  [CALCULATION: script/output], [INFERENCE] or [UNVERIFIED]. Never state an author, figure or
  publication from memory. Save each primary document you rely on to `_cache/` and cite page or
  table.
- Report every specification you compute: list the method column of each derived CSV in RESULT.md,
  including rows that go against your leading reading.
- Per-capita figures from pooled years: compute one year at a time or check against an independent
  annual rate (a previous NCVS lane tripled its figures this way).
- No single download over 10 GB without `df -h` first.
- Blocked data: write `[BLOCKED] <what, where>` and continue with the next arm.
- A lane adopts nothing. Express each finding as a proposed change to the adopted main case
  ($203.2–249.6bn, `main_case_2026_09_23/`) and to the social costs beside it; say which.
- Finish: `RESULT.md` opens with `**Verdict:**` (2–5 sentences: the answer, direction, size, how
  sure), then method, results, what would change it, limits, reproduce commands. Return to the
  parent the RESULT.md path and at most 10 lines.
