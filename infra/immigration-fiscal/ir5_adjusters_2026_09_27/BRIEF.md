# Lane brief: what does a parent of a US citizen (IR-5) who adjusts status inside the US cost per admission?

Date 2026-09-27, 23:30 JST. Parent session immigration-research-1c. The operator asked: "Parents who adjust
inside the US. Their cost per admission hasn't been computed. The $270–286k figure is an upper bound for them."

## What exists (read first; do not edit these lanes, they belong to another session)

- `../late_arrival_tail_2026_09_27/RESULT.md` and `per_admission.py` → `derived/per_admission.csv`. A Mexican
  parent **newly arriving** at 55 / 60 / 65 is a remaining-lifetime net cost of $270k / $275k / $286k at 3%
  ($525k / $478k / $437k undiscounted; case range at 3% $254–339k).
  - The statutory arm puts years 0–4 at the five-year bars and public care at the lineage lane's priced floor.
  - Year 5 on uses observed ACS receipt by years since arrival.
  - Unauthorized-only items (`S` state coverage, `E` enforcement) are zero for an LPR.
- The same RESULT's "Revision 2026-09-27 (evening)" (b222e28): SSA POMS GN 00303.800 A.4 says the five years of
  residence for a Medicare buy-in "need not" be as an LPR. A parent who adjusts after 5+ years here can buy in
  from the month of adjustment. It names the adjuster variant as not computed. Ladder 235 reads the new-arrival
  values as upper bounds for adjusters.
- `../ir5_fraud_and_cohorts_2026_09_27/RESULT.md` §2 and `../late_arrival_tail_2026_09_27/derived/mexico_ir_new_vs_adjust.csv`.
  About 80% of the Mexican IR-5 flow adjusts inside the US; in-US adjustments rose from 27.3k to 51.3k,
  FY2019–FY2024. The adjuster value is therefore the main case for Mexico, not a side variant.
- `../late_arrival_account_line_2026_09_27/` (ladder 240) is the annual-account line. It does not change here:
  the account is a cross-section of people already present.
- Ladder 235, 240–242.

## The premise to test

"Upper bound" holds only if the admission's incremental cost is below a new arrival's. Two forces pull in
opposite directions:
- **Lower.** The parent is already here, so part of the lifetime cost exists without the green card, and the
  green card removes the unauthorized-only items.
- **Higher.** Eligibility can come sooner than for a new arrival:
  - the Medicare buy-in clock counts prior residence;
  - ACA premium tax credits reach lawfully present people under 65 without a five-year bar (verify, 26 U.S.C.
    36B);
  - the ages at adjustment may differ.

The sign of the difference is the finding.

## Questions

1. **Who adjusts.** Establish for Mexican IR-5 adjusters:
   - their prior status and time in the US before adjusting, from DHS/OHSS tables, NIS-2003 (the tail lane
     already uses its age ratios) or published work;
   - their age at adjustment against consular arrivals.
2. **The counterfactual, in three arms.**
   - (A) Stay anyway: without adjustment the parent remains here in the prior status for life, so the
     admission's cost is the change in eligibility and status-linked items.
   - (B) Leave: without adjustment the parent departs, so the full cost applies. Eligibility timing follows
     the adjuster's clock, not a new arrival's.
   - (C) The mix supported by question 1.
3. **Eligibility at and after adjustment, from primary text** (quote each in `reads/`):
   - the Medicare Part A/B buy-in (POMS GN 00303.800), who pays the premiums, and the Part B general-revenue
     share;
   - the five-year bar's start date for adjusters (8 U.S.C. 1613, 1641);
   - SSI's 40 quarters and the quarters that count (1612);
   - SNAP;
   - ACA premium tax credits for lawfully present people under 65;
   - I-864 deeming as practised.
4. **Cost per admission.** Value arms A–C with the tail lane's machinery at ages 55 / 60 / 65, at 3% and
   undiscounted, and compare each to $270–286k.
   - Import `per_admission.py` read-only or copy what you need into this lane. Do not edit the tail lane.
   - For arm A you need the prior-status cost profile: the ledger's `S`/`E` items and the lineage lane's
     public-care floor.
5. **Mexico's IR-5 flow at the adjuster/new-arrival mix.** Give the weighted per-admission value and the FY2024
   flow valuation beside the tail lane's $16bn at 3%. Say whether "$270–286k is an upper bound for adjusters"
   holds, and under which conditions it fails.

## Rules

- Work only in `infra/immigration-fiscal/ir5_adjusters_2026_09_27/`. Do not edit the tail, account-line or cohort
  lanes. Do not edit `research/`, `decisions/`, INDEX, FAQ, ladder or `CLAUDE.md`.
- The checkout is shared: no commits, and no `git add`, `stash`, `checkout` or `reset`.
- Raw downloads go in an ignored `_cache/`, with a `.gitignore` in the lane. Firecrawl is out of credits: use Exa
  or direct HTTP with a generic User-Agent, and no personal identifier in any request.
- Run Python as `OPENBLAS_NUM_THREADS=1 uv run --no-project python3 <script>` from the repository root. Write
  CSVs with `lineterminator="\n"`. Two runs must be byte-identical.
- Tag every number: [SOURCE], [DATA], [CALCULATION], [INFERENCE] or [TRAINING-DATA]. State which inputs are
  measured and which assumed.
- Stub `RESULT.md` with `**Verdict:** pending` first and append as you go.
- Final message: the RESULT path and at most ten lines. List the files covered and skipped, and every judgment
  call.
