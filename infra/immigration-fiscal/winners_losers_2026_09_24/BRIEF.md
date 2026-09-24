# Lane brief: who wins and who loses, person by person, over every priced channel

Date: 2026-09-24. Operator: "it would be good to track who loses and who wins exactly".

## Base (read first)

`../distribution_weights_2026_09_23/` (ladder 194) already divides the September 23 case among
other residents person by person. Its frame covers the 295.83m other residents in CPS ASEC 2025,
ranked by equivalized SPM resources. Its channels are:

- fiscal cost under two financing conventions;
- wages;
- renters and landlords;
- crime victims;
- unreimbursed care;
- consumer prices as a side view.

Read `RESULT.md`, `BRIEF.md` and `distribute.py`, and reuse its code by import or by copying it
into this lane; do not edit it. Also read:

- the FAQ section "Before combining numbers from different entries"
  (`../../../research/immigration-objections-faq-2026-09-21.md`);
- the real-costs memo (`../../../research/immigration-real-fiscal-and-social-costs-2026-09-23.md`);
- the evidence-symmetry rules (`../../../notes/quant-bias-checklist.md`), rule 5 especially:
  benefits are priced as carefully as costs, in the same table.

## Build

1. **Channel registry, `channels.csv`.** One row per channel. The columns are:
   - `id` and `label`;
   - `bn_low`, `bn_central`, `bn_high`, signed from other residents' side;
   - `who`, the allocation key id;
   - `relation`: `inside` the account, `beside`, or `overlaps:<id>`;
   - `counterfactual`;
   - `source_lane` and `ladder`;
   - `status`: `adopted`, `proposed` or `pending`;
   - `date`.

   Read every total from the lane's derived files, never from prose. The rows are:

   | Channel | Total and status | Source |
   |---|---|---|
   | Fiscal cost, adopted case | $200.875–246.318bn | `../main_case_2026_09_24/derived/main_case_bands.csv` and `summary.json`; ladder 219 |
   | Wages | after tax, long run; ε = ∞ central and ε = 3 | ladder 191, `../wage_distribution_2026_09_23/` |
   | Housing | renters and landlords | ladder 190, `../housing_transfer_2026_09_23/` |
   | Crime victims | the central the crime lanes now report; state which footing and why | ladders 189, 202, 218 |
   | Unreimbursed care | the part outside budgets | ladder 192 |
   | Congestion | $19.2bn, $8.0–35.3bn | ladder 195, `../congestion_2026_09_23/` |
   | Consumer prices | side view; overlaps the production term; never added | `../consumer_price_benefit_2026_09_18/` |
   | Care channels | inside since September 24; find who receives the native women's extra-hours gain | ladder 198 |
   | Race- and ethnicity-based preferences | $4.0bn to white natives; beside | ladder 213 |
   | City size and schooling mix | +$13.9bn; proposed, not adopted | ladder 201 |
   | Mobility insurance | +$0.65bn; beside | ladder 203 |
   | Debt legacy interest | $30.5–38.9bn on past gaps; a different object, listed apart and never added to the annual account | ladder 207 |
   | School dilution, vending and restaurants, compliance edge, movers, consumption key | `pending`, blank totals | the five sister lanes dated 2026-09-24 |

   For the fiscal row, reproduce the base lane's decomposition on the adopted case: the fiscal
   channel carries induced receipts, and wages carry the production term (`distribute.py`
   `fiscal_totals()`). Gate that the inside channels sum to the adopted headline, specification
   by specification.
2. **Person frame.** Every other resident gets their share of every allocated channel. Gate that
   persons sum to each channel's total at low, central and high. The frame goes in `_cache/`
   (ignored), with tracked summaries in `derived/`.
3. **Allocation keys for new rows.** The sister lanes write
   `../<lane>_2026_09_24/derived/winners_losers_rows.csv` (columns `group, channel, direction,
   bn_low, bn_central, bn_high, population_m, per_person_usd, basis, relation_to_account,
   counterfactual, source`). Define key templates they can map to, and ingest any such file
   present at run time; an absent file leaves its row pending. Templates:
   - `industry_owner:<NAICS>` (self-employment and business income by industry);
   - `industry_worker:<NAICS>`;
   - `public_school_pupils` (by district or area income);
   - `interstate_movers:<state>`;
   - `commuters`;
   - `renters`;
   - `landlords`.

   A row with no defensible key appears in the role table only.
4. **Cuts.** Tabulate the same frame so the cuts reconcile:
   - income quintile and decile (SPM equivalized, as the base);
   - education (below high school, high school, some college, BA+) × nativity (US-born, other
     foreign-born);
   - tenure (renter, owner without rental income, landlord);
   - age (under 18, 18–64, 65+);
   - race and ethnicity (non-Hispanic white, non-Hispanic Black, Hispanic of other origin, Asian,
     other);
   - state (California, Texas, the rest; plus the ten states with the most group members);
   - sex;
   - worker or not;
   - industry for workers (construction, restaurants, agriculture, landscaping, and a rest
     group).

   For each cut, give dollars by channel ($bn, $ per person, $ per household, % of resources) and
   the share of the cut's persons who are net winners and net losers under each financing
   convention.
5. **Net winners and losers.** Give the share of other residents who come out ahead or behind
   under (a) tax-share financing and (b) per-person cuts. Describe the winners and the losers
   concretely, by the cuts that separate them best (for example, degree-holding landlords in the
   top decile). Report the federal deficit-financed share apart, as the future taxpayers' row;
   it is not allocated to today's persons.
6. **The group itself.** Beside the account, in its own frame:
   - its direct fiscal transfer received (the engine's direct term, sign flipped; the production
     gain goes to other residents and is not a transfer to the group);
   - the first generation's market gain over its counterfactual in Mexico, from
     `../clemens_pritchett_calibration_2026_09_19/` or a verified place-premium estimate, quoted.
     The second and third-plus generations have no counterfactual in Mexico; say so and invent
     none;
   - within-group losses: victims inside the group, which the victim-cost lane excludes, and
     wage competition among the group's own workers.

   Report Mexico's remittance receipts ($64.745bn, `../remit_leak_2026_09_16/`) as context.
7. **The page for the parent.** One winners-and-losers table: who, gain or loss, $bn a year, $
   per person, through which channel, basis, and inside or beside. Add a second table of person
   nets by the most telling cuts, plus the full CSVs.

## Rules

- Overlapping channels are never added: consumer prices overlap the production term, and the
  debt legacy is a different object.
- The financing conventions and any income weighting are value choices. Use η only as the base
  lane does. Mark them `[FRAMING-SENSITIVE]`.
- Report every computed row.

## Gates

- Closure: persons sum to each channel's total.
- The adopted band reproduces from `main_case_bands.csv`.
- Regression check: fed the September 23 inputs, your code reproduces the base lane's
  `channel_by_quintile.csv` to $0.01bn.
- The cuts sum to the frame totals.

## Boundaries

- Write only inside this directory. Read anything. Do not edit shared files: memos, the FAQ,
  INDEX, the ladder, other lanes, `engine.js` or `package.cjs`. If one needs a change, stop and
  report the exact diff in RESULT.md. Do not commit; the parent re-runs and commits.
- Stub `RESULT.md` first with `**Verdict:** pending` and keep it current.
- Run Python as `OPENBLAS_NUM_THREADS=1 uv run --no-project python3 <script>`, with extra wheels
  as a literal `--with pkg`.
- Fetch with `subprocess.run(["curl", "-sS", "--fail", ...])`, because Python urllib fails TLS on
  this machine. Check content, never status or size.
- Keys: `set -a; . ../acquire/config.local.env; set +a` if you need the Census API. Never print
  keys. Never run `pgrep -f` or `ps` dumps.
- Evidence: tag claims `[SOURCE: url, page/table]`, `[DATA: file]`, `[CALCULATION: script →
  output]` or `[INFERENCE]`.
- RESULT.md style: lead with the outcome in plain words; short paragraphs; tables with units; a
  "Would change it" line; a model self-report line with the exact model id from your environment.
- Final message: the RESULT.md path and at most ten lines.
