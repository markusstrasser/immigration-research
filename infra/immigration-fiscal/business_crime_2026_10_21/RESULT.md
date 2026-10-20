**Verdict:** Business crime is not bigger than murder. Retail theft, employee theft, non-retail
business losses and the NIBRS-only person crimes cost residents outside the 44.90M lineage about
**$5.3bn a year gross** in 2024 ($3.0–12.1bn across the arms), which is **33–36% of murder's
$14.6–16.3bn** on v9. On the with/without rule the case's private-security row already uses, the
group's own purchases also carry part of other offenders' theft, and the net is **$1.5bn**
($0.5–4.4bn). Per lineage member that is $118 gross and $33 net
[CALCULATION: `business_crime.py` → `derived/summary.csv`, `derived/arms.csv`].

Business crime would match murder only if the losses were about three times what the NRF's
shrink survey implies, or if the group's share of shoplifting were about three times what police
records show. In Texas and Arizona NIBRS, Hispanic residents commit shoplifting against stores at
0.91 times the all-resident rate (1.37 times the non-Hispanic white rate). Carried to the nation,
they commit 19.0% of it, against a 20.3% share of the population. The group's share of offending
(0.121 on the lineage) is close to its share of retail spending (0.099), so the pass-through nets
most of the loss away. The open input is the 35% of shoplifting victimisations with no recorded
offender. If every one of them were Hispanic, line A would rise from $2.3bn to $4.6bn gross and the
total to about $7.6bn, still half of murder. [FRAMING-SENSITIVE: the gross and net readings answer
different questions; see "Incidence"]

Model self-report: claude-opus-5-5. Lane `infra/immigration-fiscal/business_crime_2026_10_21/`,
2026-10-21. Nothing committed. This lane was produced through an LLM; see `notes/llm-bias-caveat.md`.

## Headline

2024 $bn a year, cost to residents outside the lineage. Each cell shows the low end of the case
(raw-coded justice key 0.0703), then the high end (custody key 0.0661).

| Line | Low arm | **Central** | High arm | What it is |
|---|---:|---:|---:|---|
| A Retail external theft (shoplifting, ORC, retail burglary, robbery and card fraud by non-employees) | 0.98 / 0.98 | **2.32 / 2.32** | 5.52 / 5.50 | NRF shrink × external share × store sales, at cost |
| B Retail employee theft | 0.76 / 0.76 | **1.63 / 1.62** | 4.47 / 4.45 | NRF internal share of the same shrink |
| C Non-retail business losses, police-recorded | 0.44 / 0.44 | **0.49 / 0.49** | 1.10 / 1.10 | NIBRS business victims outside stores, national by CIUS 2024 |
| D Violence against children under 12 outside the family | 0.53 / 0.53 | **0.59 / 0.59** | 0.66 / 0.66 | NIBRS, Miller victim-only prices |
| E Violence at jail/prison locations, victims 12+ | 0.09 / 0.09 | **0.11 / 0.10** | 0.12 / 0.12 | NIBRS, Miller prices |
| F Fraud, embezzlement and extortion against individuals | 0.16 / 0.16 | **0.18 / 0.18** | 0.20 / 0.20 | NIBRS police-recorded losses |
| **Total, gross** (harm caused by the group) | 2.98 / 2.96 | **5.31 / 5.29** | 12.07 / 12.02 | |
| **Total, net** (with/without, pass-through) | 0.53 / 0.52 | **1.48 / 1.45** | 4.38 / 4.33 | A–C less the group's payment toward others' losses |
| Per lineage member, gross / net | $66 / $12 | **$118 / $33** | $268 / $97 | ÷ 44,903,074 |
| Murder on v9 (victims row × 0.3912) | | **14.61 / 16.27** | | |
| Gross total ÷ murder | 0.20 / 0.18 | **0.36 / 0.33** | 0.83 / 0.74 | |

[CALCULATION: `derived/summary.csv`, `derived/arms.csv`] Line A's hard bounds put every unknown
shoplifting offender on one side. They give a gross of $1.42bn (all non-Hispanic) or $4.65bn (all
Hispanic). The police-recorded floor (CIUS 2024 shoplifting × NIBRS mean loss) is $0.05bn. The low
and high arms stack every low or every high choice; they bound the estimate and are not
confidence intervals.

**Bigger than murder? No, on every arm.** On v9 murder is 39.1% of the $37.3–41.6bn victims row:
$14.6bn at the low end and $16.3bn at the high end. The share is 39% rather than the source lane's
32% because the case prices deaths at DOT's $13.7M [CALCULATION: `mortality_arms.csv`, mixed and
custody footings, `dot_uniform`]. Central business and other NCVS-uncovered crime is 0.33–0.36 of
murder gross and 0.09–0.10 net. The stacked high arm reaches 0.74–0.83 gross. Retail theft (A + B
+ C) would equal murder only if losses at cost were about $134bn a year, against the $43.5bn the
central arm uses. That is 14.6 ÷ (0.1213 × 0.9006).

## The chain, link by link

Each link is labelled **measured** (from a primary file), **assumed**, or **inherited** (taken
from the case or a sibling lane).

1. **Retail losses (A, B).** NRF *National Retail Security Survey 2023*: FY2022 shrink 1.6% of
   sales (1.4% in FY2021). Shrink is 36% external theft, 29% internal (employee) theft, 27%
   process and control failures and errors, 6% unknown and 1% other. "External theft" includes
   shoplifting, burglary, robbery and credit-card fraud by non-employees; process error, vendor
   fraud and "other" are not crime and are dropped [SOURCE: NRSS 2023 pp. 2–4 and glossary; text
   gated in `run_log.txt`]. NRF's $112.1bn is 1.6% of all retail sales (gate: the implied base is
   $7.0tn). The central arm applies the rate to 2024 store retail excluding motor-vehicle dealers,
   $5,527bn. The low arm uses 1.4% and also excludes gasoline stations and nonstore retailers
   ($3,597bn). The high arm takes all retail ($7,107bn) and spreads the unknown and other shares
   pro rata [DATA: Census MRTS 2024 not-adjusted annual]. Respondents are 177 large brands; 78%
   leave e-commerce loss out of shrink and 57% leave supply-chain loss out. *Measured, as survey
   self-attribution; NRF is an industry advocate and the shares are not audited (grade C).*
2. **Valuation.** Shrink is taken at retail value. A store loses the replacement cost of a stolen
   good, not the margin, unless the theft causes a stock-out. Central and low therefore take cost,
   retail × (1 − 0.331), the 2022 gross margin excluding motor-vehicle dealers [DATA: ARTS 2022
   restated]; the high arm takes retail value. *Measured margin; the cost basis is assumed.*
   - The stolen value is counted in full as a loss to outsiders. The thief's gain goes to the
     group and is not netted. This follows the victim lane's Miller property-loss convention.
3. **Offender share, shoplifting.** NIBRS TX+AZ 2022–2023 business-type victims (business,
   financial, religious, other) at retail locations. Agencies recording offender ethnicity for at
   least 50% of offenders, 1/n per offender, unknowns allocated in proportion within state-year ×
   offence (allocation a of the offender-ethnicity lane). The national translation is
   `S = RR_H·P_H / Σ RR_g·P_g` on NC-EST2024 all ages [INHERITED: `nibrs_rates.allocate`,
   `compositions`, `national_pops`, imported, not copied].
   - Central 0.1896, against a Hispanic population share of 0.2025.
   - Specification range 0.156–0.195: loss-weighted 0.166, ethnicity ≥95% 0.156, ≥80% 0.180,
     arrest-only incidents 0.184, TX 0.195, AZ 0.180, TX+AZ+CA 0.177, arrestees 0.185.
   - Allocation bounds 0.116–0.379 [DATA: `derived/offender_shares_by_spec.csv`,
     `arrestee_shares_business_incidents.csv`].
   - 35% of shoplifting victimisations have no offender record (`unknown_share`). *Measured,
     police-recorded; the national transfer is assumed [INFERENCE].*
4. **Employee theft share.** Union share of store-retail wages, 0.0983 (cells 0.081–0.131)
   [INHERITED: `job_capital_taxes_2026_10_14/derived/wages_by_industry.csv`, personal
   allocation]. Theft is assumed equal per wage dollar [ASSUMPTION]. The high arm takes the larger
   of the highest cell and the NIBRS retail-embezzlement route (0.1163). BLS CPS table 18 was
   blocked (HTTP 403), so headcount shares were not used. Headcount shares would sit above wage
   shares.
5. **Non-retail business losses (C).** NIBRS business-type victims outside retail locations, net of
   recovered property, each property item capped at $1M. They are scaled to the nation by CIUS 2024
   counts per offence (larceny by type, burglary, robbery, vehicle theft). Fraud, vandalism,
   embezzlement, arson and extortion use the SRS property-crime ratio, 7.38. The result is
   **$5.09bn a year**, with the largest parts other larceny $1.86bn, business vehicle theft $1.08bn,
   fraud $0.67bn and burglary $0.55bn [DATA: `derived/nonretail_business_losses.csv`].
   Police-recorded losses are a floor. The high arm doubles them for non-reporting [ASSUMPTION].
   - Cargo theft is inside this line. TX+AZ NIBRS flag $17.2M a year; CargoNet puts 2024 US and
     Canada cargo theft at $0.455bn [SOURCE: Verisk CargoNet 2024 annual analysis, 2025-01-21], so
     it cannot move the total.
6. **Hispanic → Mexican origin → lineage.** Population share s = 0.5975, with the ACS
   institutional ratio 0.901 / 1.118 in the low and high arms [INHERITED: victim lane]. The union
   is put on the lineage with the case's crime key, (1 + 0.0703) at the low end and (1 + 0.0661)
   at the high end [INHERITED: `real_costs_totals.json` oct16 `lineage_social_rows.keys`].
7. **Incidence (A–C).** Businesses pass losses to purchasers [ASSUMPTION, the security row's
   premise]. Outsiders bear the forward share, L·S·(1 − p). Removing the group also stops its
   payment toward other offenders' theft, L·p·(1 − S). The net is L·(S − p), with p the lineage's
   general-sales-tax payment share, 0.0994 [INHERITED:
   `social_costs_unpriced_2026_09_28/derived/payment_keys.json`; the code gates the identity].
   - Gross answers "what harm do the group's offences do to outsiders". Net answers "what would
     outsiders save if the group were absent", the case's comparator.
   - The brief's "remove the within-lineage share" is the gross column.
8. **Direct victims (D–F).** NIBRS individual victims of Hispanic-offender violence or fraud are
   scaled nationally: covered population to state, then the CIUS violent ratio, 7.94.
   - Child victims in a family or household relationship to an offender count as inside the
     lineage. Other Hispanic victims are outside at (1 − 0.786) × the sibling lane's national
     victim-mix transfer. Non-Hispanic victims are all outside.
   - Prices are Miller 2021 victim-only (the victim lane's set). Murder is excluded from D and E
     because WONDER deaths already count every child and inmate homicide.
   - The victims row's boundary (1 − 0.0103) and crime key are applied
     [DATA: `derived/violent_outside_ncvs.csv`].
   - Children are priced at adult values [ASSUMPTION].

## Overlap with the case's rows (all additive by construction)

| Existing row or account | What it covers | This lane | Treatment |
|---|---|---|---|
| victims ($37.3–41.6bn) | NCVS household population 12+: personal violence; all homicide deaths (WONDER) | D: under 12; E: jail and prison victims | Disjoint universes. Murder is left out of D and E. E's NIBRS jail victims include some staff, who are in NCVS; the overlap is small and unremoved (E is $0.1bn) |
| property_crime ($1.3–1.4bn) | NCVS household burglary, vehicle theft and theft (arrest-share proxy) | A–C business-type victims; F fraud against individuals | Disjoint victim types. NCVS core does not measure fraud. Households' vehicle theft stays in property_crime |
| private_security ($0.46–0.57bn) | Guards (contract and in-house), alarms, locksmiths, armored cars, investigators, equipment | Retail loss prevention | Loss-prevention labour and equipment are counted there. This lane counts **no** prevention spending, only losses |
| fear_avoidance | Willingness to pay beyond violent victim cost | none | Not touched |
| Fiscal account | Police, courts, prisons charged by use | none | Criminal-justice costs excluded; government-victim losses (NIBRS type G) excluded |
| A vs C | NRF external theft includes retail burglary, robbery and card fraud | C | C takes only incidents at non-retail locations and drops shoplifting |
| B vs C | NRF internal theft | C | Embezzlement at retail locations is excluded from C |
| Commercial robbery: employees' pain and fear | NCVS counts workers robbed or threatened at work | beside only | $0.07bn union, not added |

## Disconfirmation: is the group's business-crime rate low?

The evidence points to about population parity, not to a high rate.
- **NIBRS shoplifting offenders.** In TX+AZ the Hispanic share is 34.2% against a 37.5% population
  share, a ratio of 0.91 to all residents. The ratio to non-Hispanic whites is 1.37, because
  non-Hispanic Black residents offend at a higher rate. Arrestees in the same incidents show 34.2%
  Hispanic, with only 5.5% of arrestee ethnicity missing (RR vs non-Hispanic white 1.06).
- **NIBRS non-retail business crime.** Hispanic offender shares run 0.13–0.23 nationally across
  offences, at or below the 0.20 population share, except embezzlement (0.23).
- **FBI 2024 adult arrests, national ethnicity panel.** Hispanic people account for 20.5% of
  larceny-theft arrests, 20.3% of burglary, 17.6% of fraud and 16.4% of embezzlement. That is
  below their 22.1% share of all arrests and below their shares of vehicle theft (26.5%) and
  robbery (27.2%) [DATA: `derived/fbi_2024_adult_arrests_hispanic_share.csv`, from
  `nibrs_arrests_2026_09_16`].
- **Against the operator's hypothesis.** Unseen offenders could differ from seen ones. Organised
  retail crime crews may be both less often caught and differently composed. Nothing held measures
  this, so the hard bounds are reported. Even the all-Hispanic bound leaves the total at half of
  murder.

## Measurement pipeline (analyze lens), shoplifting

| Stage | Controller | Residual category | Sign on the group's share | Grade |
|---|---|---|---|---|
| Theft happens and the store detects it | Retailer loss-prevention policy | Undetected loss sits inside shrink | unknown | C |
| Shrink attributed to theft vs error | NRSS respondents (self-report) | 6% unknown, 1% other | none (volume only) | C |
| Store calls police | Retailer policy (many chains do not report) | Unreported | unknown; police-recorded loss is 2% of the NRF-based figure | C |
| Offender recorded | Police; apprehension needed | 35% no offender record | the bounds 0.116–0.379 | B for the known part |
| Ethnicity recorded | Agency practice | Agencies under 50% recording dropped; ≥95% agencies give 0.156 | down slightly in better-recording agencies | B |
| National transfer | This lane | TX+AZ relative rates assumed national | unknown | C |

The two largest measured spreads, recording quality (0.156–0.190) and loss weighting (0.166), both
lower the share. The unrecorded-offender share has no sign the data can identify.

## Open assumptions

- Business losses pass fully to purchasers, at the case's payment key.
- The stolen-goods cost basis is retail × (1 − gross margin).
- Employee theft is equal per wage dollar.
- Unknown offenders are allocated in proportion to known ones (the bounds are reported).
- TX+AZ relative rates hold nationally.
- Police-recorded C–F are floors, with a 2× multiplier on C in the high arm only.
- Children are priced at Miller's adult prices.
- NRF self-attribution is taken as given. Retailers have an incentive to overstate theft; the low
  arm's 1.4% rate and smaller base cover part of that.
- Not priced:
  - customers' time at locked shelves;
  - store closures and lost sales (NRF says shrink omits them);
  - insurance overhead;
  - e-commerce and supply-chain fraud outside shrink;
  - card fraud borne by issuers outside NIBRS.

## Covered / skipped

Covered:
- the brief;
- the victim lane and its unit costs, mortality arms and scaling;
- the NIBRS lane (staged agencies, compositions, allocation, translation);
- the security row's P7 rule and payment keys;
- propagation keys (oct16);
- FBI 2024 Table 43C via the arrests lane;
- CIUS 2024 Tables 1, 5 and 7;
- the NRSS 2023 PDF, MRTS 2024, ARTS gross margin and CargoNet 2024.

Skipped:
- New NIBRS states. The disk had 8.1 GB free, and the TX/AZ/CA files already cover 90–97% of
  Texas's Hispanic residents in agencies that record ethnicity.
- BLS CPS table 18 (HTTP 403).
- NRF's own PDF (login required); the sponsor-hosted copy is pinned instead.
- National card-fraud totals (no primary source fetched).
- Kidnapping and trafficking (no Miller price).
- Crimes against society (no victim cost).
- Research memos, FAQ, INDEX, ladder and other lanes: not edited, per the brief.

## Sources and pins

sha256 of every input are in `inputs/pins.json`. A run verifies every pin and stops on a mismatch.

| File | Source, retrieved | sha256 (first 16) |
|---|---|---|
| `_cache/nrss2023.pdf` (+ `pdftotext -layout` → `nrss2023.txt` 3efa0bee…) | NRF NRSS 2023, https://info.apprissretail.com/hubfs/Resource-Center/2023.038-national-retail-security-survey-report-2023.pdf, 2026-10-21 | 0c34f950ac643c47 |
| `_cache/mrtssales92-present.xlsx` | Census MRTS, https://www.census.gov/retail/mrts/www/mrtssales92-present.xlsx, 2026-10-21 | 190d718b85361316 |
| `_cache/arts2022r_gmper.xlsx` | Census ARTS 2022 restated, https://www2.census.gov/programs-surveys/arts/tables/2022restated/gmper.xlsx, 2026-10-21 | 4710df1aa375585f |
| NIBRS TX/AZ/CA 2022–2023 zips | FBI CDE bulk store via `offender_ethnicity_nibrs_2026_09_23/_cache` (2026-09-23); hashes equal that lane's manifest | TX-2022 9c2632330fda16ca, TX-2023 895e708876005299, AZ-2022 3cf8957f3000b36e, AZ-2023 21e027cd9a9348d3, CA-2022 313e67394c4b1be9, CA-2023 2dcf66724830e933 |
| CIUS 2024 Tables 1, 5, 7 | FBI, via `nibrs_arrests_2026_09_16/_cache/x/est2024` | f4915ae870feca9a, 0feabb80db5341a8, f4aef2067d980ff1 |
| CargoNet 2024 | https://www.cargonet.com/news-and-events/cargonet-in-the-media/2024-theft-trends/ (2026-10-21), $454,914,764 total loss, 3,625 incidents; cited, not computed | — |

Inherited repository inputs are pinned there too:
- `real_costs_totals.json` (oct16) 3b7d00abeabf786f;
- `payment_keys.json` 1c886f0d713fab51;
- `wages_by_industry.csv` 3bccaa790e713c22;
- `mortality_arms.csv` f5f455e8fef6e248;
- the sibling lane's stage pickles and ACS compositions.

## Files

- `business_crime.py`: model, gates, every arm; `--fetch` downloads the three raw files.
- `bizcrime_stage.py`: NIBRS staging into `_cache/stage/` (ignored), imported by the model.
- `inputs/pins.json`.
- `derived/`:
  - `arms.csv`, `summary.csv`, `summary.json`;
  - `offender_shares_by_spec.csv`, `arrestee_shares_business_incidents.csv`;
  - `nonretail_business_losses.csv`, `violent_outside_ncvs.csv`;
  - `fbi_2024_adult_arrests_hispanic_share.csv`, `run_log.txt`;
  - `nibrs_child_victims_under12_by_relationship_ethnicity.csv`, shared with
    `within_group_harm_2026_10_21`. It holds NIBRS violent victimisations of individuals under 12
    (offences 11A–D, 120, 13A, 13B and 09A; intimidation excluded) for TX, AZ and CA 2022–2023,
    non-tribal agencies, with these columns:
    - `agency_records_ethnicity_ge50`: whether the agency records offender ethnicity for at least
      half of offenders (this lane uses only the True rows);
    - `victim_class` (vH, vNHW, vNHB, vNHO, vNHU, vU);
    - `family_or_household`: True when the victim has a family or household relationship (codes CH
      CF CS FC FP GC GP IL OF PA SB SC SE SP SS) to any offender; unknown relationships count as
      False;
    - offender-class weights at 1/n per recorded offender, before any allocation of unknowns:
      `off_eth_unknown` (race may be known) and `off_no_record` (no offender record).

    Of 76,696 victimisations, 37,333 are family or household.

## Reproduce

```sh
cd /Users/alien/Projects/immigration-research
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/business_crime_2026_10_21/business_crime.py
uv run --no-project python3 scripts/rerun_lane.py infra/immigration-fiscal/business_crime_2026_10_21 \
  "uv run --no-project python3 {lane}/business_crime.py"
```

## Log

- 2026-10-21 01:27:15 JST (`date`): rerun with `_cache/stage` deleted first (cold staging), then
  `rerun_lane.py` gave IDENTICAL 12/12, exit 0. The warm rerun before it was also IDENTICAL
  12/12, exit 0.
- 2026-10-21 01:30:26 JST (`date`): added the shared under-12 table for within_group_harm. The lines
  and totals are unchanged. `rerun_lane.py` gave IDENTICAL 14/14, exit 0.
