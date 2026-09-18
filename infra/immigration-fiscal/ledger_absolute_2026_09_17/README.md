# Complete absolute account for the all-age Mexican-origin ledger — September 17, 2026

This lane takes the partial all-age account in
[`all_age_ledger_2026_09_17`](../all_age_ledger_2026_09_17/README.md), whose union
absolute balance is **+$50.24bn**, and adds the fiscal items that account omits,
each under an explicit convention with named alternatives. The output is a
waterfall from the measured partial balance to a complete resident account, for
the three Mexican-origin target groups, their union, and the same two reference
populations the upstream lane uses.

It is an accounting scenario built from published aggregates and measured
exposures. It is not observed tax collection, not an admission-policy effect and
not a lifetime present value.

## Reproduce

From the repository root:

```sh
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 \
  infra/immigration-fiscal/ledger_absolute_2026_09_17/absolute_ledger.py \
  --params infra/immigration-fiscal/ledger_absolute_2026_09_17/params/params.json
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 \
  infra/immigration-fiscal/ledger_absolute_2026_09_17/check_gates.py
```

`check_gates.py` re-reads only what the builder wrote and exits non-zero on any
failed gate, so a stale or hand-edited `derived/` cannot pass. A development run
may pass `--params params/params_placeholder.json --allow-placeholder`; that file
carries `status: placeholder` on every entry, its numbers are stand-ins used only
to exercise the machinery, and `check_gates.py` fails the
`parameters_all_verified` gate on any such run.

Requires NumPy, pandas and openpyxl. No downloads and no writes outside this
directory.

## Parameter discipline

Every external number is read from `params/params.json`, written by a separate
researcher lane, where each entry carries a source URL, a verbatim quote holding
the number, a fetch timestamp and a `status`. The builder refuses any entry whose
status is not `verified`: the item that needed it is dropped or zeroed and named
in `derived/audit.json` under `items_dropped` and in the result, and no
substitute value is ever used. `audit.json` records the parameter file's sha256
and every parameter actually consumed.

Three classes of input are read from in-repo caches rather than from the
parameter file, because the upstream lanes already use them and this lane is
told to reuse their construction: the 2022 Census of Governments state-local
table and the Census population file behind the general-services per-capita
vector, the OMB Historical Table 3.1 function outlays, and the Census ASSF
FY2024 school-finance summary workbook. The builder cross-checks every function
of the cached Table 3.1 against the independently fetched Table 3.2 parameters
and refuses to run if they disagree.

## Items and conventions

Charges are per CPS record in dollars for income year 2024; costs negative,
receipts positive. Every item is aggregated by group and age band with the full
weight and each of the 160 replicate weights, so the standard error is the
survey's own `4/160 Σ(replicate − full)²`.

| id | item | central arm | alternatives |
|---|---|---|---|
| G | state and local general services | per capita by state of residence, 2022 Census of Governments direct general expenditure less education, welfare, health, hospitals and corrections, inflated to 2024 by the BEA state-local price index | FY2022 price level |
| K | K-12 capital outlay and interest on school debt | state per-pupil capital plus interest on the ledger's public pupils aged 5–17 | none |
| P | non-school state and local capital outlay | 2022 Census of Governments direct general capital outlay less elementary-and-secondary capital outlay less the capital already inside item G, per capita by state of residence, inflated to 2024 | `briefed_gross`, which subtracts only the elementary-and-secondary share |
| D | district cost-to-serve differential | enrolment-weighted per-pupil spending faced by Hispanic pupils less that faced by all pupils, by state, from the Census F-33 district file joined to the NCES CCD | dropped without the district files |
| U | transfer under-reporting | each reported program's dollars scaled by its administrative/survey ratio. Housing is excluded because function 604 carries federal housing assistance whole; Social Security is excluded because the brief applies it only when its ratio is below 1 | none |
| I | refundable-credit improper payments | EITC and ACTC improper dollars by each record's share of modeled credits | zero |
| M | MEPS-to-NHEA coverage | transported Medicaid and Medicare costs scaled by the NHEA non-institutional to MEPS ratio per payer | zero |
| N | institutional care | external add from [`institutional_bound_2026_09_17`](../institutional_bound_2026_09_17/RESULT.md), midpoint of its adverse and moderate arms | none |
| E | immigration enforcement | interior stock: ICE ERO total, EOIR and appropriated USCIS times the Mexico share of the OHSS January 2022 unauthorized stock, per head over Mexico-born noncitizens. ERO total already contains custody, so the custody line is never added on top | plus Border Patrol times the Mexico share of FY2024 southwest border encounters; the Pew mid-2023 secondary stock; zero |
| C | corporate income tax, federal and state | 25% by share of national wages, 75% by share of national property income | per capita; 100% capital |
| X | excise and selective sales taxes | per capita | proportional to the ledger's consumption proxy |
| R | rest of the federal budget by function | see below | all per capita; all zero |
| F | federal defense, net interest and general government | zero, as pure public goods | per capita; proportional to modeled federal income and payroll taxes paid |
| S | state-funded coverage for undocumented residents | assembled from individual verified state budget lines, per Mexico-born noncitizen in that state, times the Mexico share of the unauthorized stock, half assumed already inside MEPS. Biennial figures are halved to an annual rate | none or all inside MEPS |

### What the rest of the federal budget nets out

Item R prices what the account does not already carry, and nets out what it
does. Each part keeps the same national dollar amount under both arms, so
switching arms changes who is charged and never how much.

- **700 veterans** less subfunction **703** VA hospital and medical care, which
  the MEPS public-payer transport already charges, spread per veteran. Veteran
  status is `PEAFEVER`, ever served on active duty, not `VET_YN`, which only
  flags receipt of veterans' payments.
- **602** federal civilian retirement by total pension income among people
  reporting a federal government pension source, `PEN_SC1` or `PEN_SC2` equal to
  3. CPS ASEC carries no separately valued federal pension amount, so this is a
  proxy; `audit.json` records the share of allocated dollars held by people who
  also hold a non-federal pension.
- **750** administration of justice: the BOP Mexican-national share of
  subfunction **753** to Mexico-born noncitizens per head, the remainder per capita.
- **500** education and training less subfunction **501**, the federal
  elementary and secondary aid already inside the state per-pupil current
  spending the account charges. Pell is *not* netted, because nothing in this
  account prices it.
- **550** health less NHEA federal Medicaid, which the MEPS transport already
  charges. OMB has no Medicaid subfunction and subfunction 551 is health care
  services, far broader, so 551 is not the netting quantity.
- **600** income security: subfunctions **601** and **604** only, with housing
  assistance (604) isolated so its allocation rule can be switched between per
  capita and the reported SPM capped housing subsidy. Unemployment
  (603), food and nutrition (605) and other income security (609) are already in
  the account through the CPS transfer fields, and 602 is charged separately.
- **400** transportation per capita.
- **150, 250, 270, 300, 350, 370, 450** at zero in the central arm and per capita
  in the alternative.

Functions **050**, **900** and **800** are item F. **570** Medicare and **650**
Social Security are already priced. **920** allowances and **950** undistributed
offsetting receipts are left unpriced.

## Outputs

All under `derived/`; `*.npz` is ignored.

- `items_by_group.csv` — item, arm, group, total, per person, replicate standard
  error, and the common-age gap per standardized person against the third-plus
  non-Hispanic white reference.
- `waterfall.csv` — cumulative absolute balance per group, starting at the gated
  upstream absolute and adding items in the order G, K, P, D, U, I, M, N, E, C,
  X, R, F, S under the central arms, with a flag naming any step that is an
  external add or a dropped item. The brief's order ends at F; item S is appended
  as the last step so the endpoint includes state-funded coverage, and
  `audit.json` records F's step number as the brief's final step so both
  endpoints stay visible.
- `complete_gaps.csv` and `complete_gaps_by_item.csv` — the age-standardized
  answer: the common-age gap per standardized person and the age-matched total in
  dollars, for each target and the union against both references, carried from the
  upstream partial gap to the complete account, with each item's contribution
  broken out. The partial values are gated against the upstream `estimates.csv`.
- `national_reconciliation.csv` — the account summed over every civilian-household
  resident against the consolidated FY2024 federal and state-local position built
  from the same parameters, with the residual labelled "unpriced or coverage" and
  the share of consolidated outlays and receipts the account covers. The residual
  is reported, never forced; a gate fails if it comes back near zero.
- `arms_matrix.csv` — the union absolute under every combination of the F, E, C
  and R arms, everything else central. The grid is 3 x 4 x 3 x 4 = 144 rather
  than the brief's 3 x 3 x 3 x 3: the enforcement item gained the Pew secondary
  stock as a fourth arm, and the federal-function item gained an arm that
  allocates subfunction 604 housing assistance by each record's share of the
  reported SPM capped housing subsidy instead of per capita.
- `marginality_curve.csv` — the union absolute as the marginality dial m runs
  from 0 to 1, with the break-even m\*.
- `audit.json` — gates, the parameter file's hash and every parameter consumed,
  national-total reconciliations, the population ratio, dropped items and the
  unpriced list.

## Executed gates

Run `check_gates.py` for the live result. The builder itself fails loud on:

- **Gate 0**, run before any new item is computed: the base account rebuilt here
  must reproduce the upstream `all_age_shared` union absolute of +$50.238bn to
  the dollar, and the base account recomputed alongside the item columns must not
  move.
- **National-total reconciliation**: each item's charges summed over the civilian
  household population, against the national total it comes from. A flat
  per-capita item must reconcile to the civilian-household-to-resident population
  ratio exactly; state-varying and record-based items are held to reported bands.
- **Common-charge cancellation**: a flat per-capita charge must leave the
  common-age gap per standardized person at zero to within 1e-6 relative.
- **OMB cross-check**: every function of the cached Table 3.1 must equal the
  independently fetched parameter for that function.
- **Ratio inversion**: every administrative/survey ratio must be the reciprocal
  of its published survey/administrative coverage ratio, re-derived here.
- **Sibling-lane cross-check**: the two reused per-capita constructions must
  still reproduce the figures the lane they came from published.
- **Unit conservation** on every base component, inherited from the upstream
  allocator.

`check_gates.py` re-tests these from the written artefacts and adds the waterfall
step arithmetic, union additivity against the three disjoint targets, the arms
grid's completeness, the linearity of the marginality curve and the consistency
of m\*.

## What this does not settle

A complete absolute account is dominated by convention, not by measurement. The
arms matrix spans a wide range precisely because the treatment of pure public
goods, corporate incidence and the unallocated federal functions is a choice, not
a finding. A charge that is common per person cancels from relative gaps while
moving every absolute balance, which is why the per-item common-age gap column
sits next to the totals. The marginality dial is a sensitivity over one
parameter, not an estimated marginal cost.

## Extension, September 18, 2026: items D and P

The two items the first build left open are now priced. Full result in
[`RESULT_extension.md`](RESULT_extension.md); the brief that asked for them is in
[`BRIEF_extension.md`](BRIEF_extension.md).

### Item D, district cost-to-serve differential

`district_differential.py` joins the Census F-33 FY2024 district finance file to
the NCES CCD LEA membership-by-race file for school year 2023-24 and asks, per
state, what per-pupil current spending the average Hispanic pupil faces against
what the average pupil faces. Run it before the ledger:

```sh
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 \
  infra/immigration-fiscal/ledger_absolute_2026_09_17/district_differential.py \
  --params infra/immigration-fiscal/ledger_absolute_2026_09_17/params/params.json
```

It writes `derived/district_differential_by_state.csv` and a `district` group of
four verified keys into the parameter file. The ledger then charges Mexican-origin
public pupils aged 5-17 their state's Hispanic-minus-all differential and the
third-plus non-Hispanic white reference its white-minus-all differential. No
separate all-native rate exists; every other record is charged zero.

**Coverage gate.** The all-pupil enrolment-weighted mean per state must sit
within 10% of the F-33 state summary per-pupil figure in
`k12.f33_per_pupil_current_spending_by_state`. Fifty of 51 jurisdictions clear
it. Vermont does not, because its supervisory unions report current spending
against zero enrolment, and it carries a differential of zero. Districts with a
missing or implausible per-pupil value, below $3,000 or above $80,000, are
dropped and counted.

### Item P, non-school state and local capital outlay

The 2022 Census of Governments functional lines each carry their own capital
outlay **inside** the function total; line 67 is the same dollars cut by
character, not an addition. Item G, built as line 66 less education, public
welfare, hospitals, health and correction, therefore already charges the capital
of every function it retains, $239.5bn of the $371.3bn national total. Item P
charges only what nothing else charges: education capital beyond elementary and
secondary, plus hospitals and correction capital, $47.0bn in 2022, inflated by
the same state-local price index and divided by the same 2022 state populations
item G uses.

The literal quantity the extension brief named, total capital outlay less the
elementary-and-secondary share, is built as the `briefed_gross` arm and reported
beside the central one. It is not the central arm because it double-counts the
$239.5bn item G already carries.

Item K prices school capital from the F-33 FY2024 district file at $136.2bn of
capital plus interest on school debt, against $84.8bn of 2022 elementary and
secondary capital outlay in the Census of Governments. Different year, different
universe, and interest on school debt is not in line 67 at all; the national
reconciliation now carries the pieces separately.

### New switches

`--off ITEM`, repeatable, carries an item through the waterfall as a dropped
step, so the pre-extension endpoint can be reproduced. `--out-dir DIR` writes the
artefacts somewhere other than `derived/`, so such a run cannot clobber the
published output.

```sh
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 \
  infra/immigration-fiscal/ledger_absolute_2026_09_17/absolute_ledger.py \
  --params infra/immigration-fiscal/ledger_absolute_2026_09_17/params/params.json \
  --off D --off P --out-dir /tmp/absolute_off
```

### New gates

`check_gates.py` re-tests 50 gates, up from 36. The fourteen new ones cover the
district coverage ratio and its zeroing rule, the differential's coverage of all
51 jurisdictions, agreement between the written district table and the
parameters, item P's reconciliation to the national non-school capital total,
item P sharing item G's per-capita convention, the exhaustiveness of the capital
split against Census line 67, item P's position after item K in the waterfall,
both items sitting on the marginality dial, and the absence of any
command-line-disabled item in a published run.
