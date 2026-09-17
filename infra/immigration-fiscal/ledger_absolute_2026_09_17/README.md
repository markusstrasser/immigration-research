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
| D | district cost-to-serve differential | enrolment-weighted per-pupil spending faced by Hispanic pupils less that faced by all pupils, by state | dropped without the district files |
| U | transfer under-reporting | each reported program's dollars scaled by its administrative/survey coverage ratio | none |
| I | refundable-credit improper payments | EITC and ACTC improper dollars by each record's share of modeled credits | zero |
| M | MEPS-to-NHEA coverage | transported Medicaid and Medicare costs scaled by the NHEA non-institutional to MEPS ratio per payer | zero |
| N | institutional care | external add from [`institutional_bound_2026_09_17`](../institutional_bound_2026_09_17/RESULT.md), midpoint of its adverse and moderate arms | none |
| E | immigration enforcement | interior stock: ICE ERO, EOIR and appropriated USCIS times the Mexico share of the OHSS unauthorized stock, per head over Mexico-born noncitizens | plus Border Patrol times the Mexico share of southwest border encounters; zero |
| C | corporate income tax, federal and state | 25% by share of national wages, 75% by share of national property income | per capita; 100% capital |
| X | excise and selective sales taxes | per capita | proportional to the ledger's consumption proxy |
| R | rest of the federal budget by function | see below | all per capita; all zero |
| F | federal defense, net interest and general government | zero, as pure public goods | per capita; proportional to modeled federal income and payroll taxes paid |
| S | state-funded coverage for undocumented residents | state general-fund cost per Mexico-born noncitizen times the Mexico share of the state's unauthorized stock, half assumed already inside MEPS | none or all inside MEPS |

### What the rest of the federal budget nets out

Item R prices what the account does not already carry, and nets out what it
does. Each part keeps the same national dollar amount under both arms, so
switching arms changes who is charged and never how much.

- **700 veterans** less subfunction **703** VA hospital and medical care, which
  the MEPS public-payer transport already charges, spread per veteran.
- **602** federal civilian retirement by reported federal government retirement
  income.
- **750** administration of justice: the BOP Mexican-national share of
  subfunction **753** to Mexico-born noncitizens per head, the remainder per capita.
- **500** education and training less subfunction **501**, the federal
  elementary and secondary aid already inside the state per-pupil current
  spending the account charges. Pell is *not* netted, because nothing in this
  account prices it.
- **550** health less subfunction **551** health care services.
- **600** income security: subfunctions **601** and **604** only. Unemployment
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
  upstream absolute and adding items in the order G, K, D, U, I, M, N, E, C, X,
  R, F under the central arms, with a flag naming any step that is an external
  add or a dropped item.
- `arms_matrix.csv` — the union absolute under every combination of the F, E, C
  and R arms, everything else central.
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
