# Lineage cost lane — one Mexico-born arrival and 100 years of descendants (2026-09-19)

Fiscal and crime account, over 100 calendar years, for one Mexico-born arrival aged 25
plus their descendants, against the identical construction for one third-plus
non-Hispanic white of the same age. Period age profiles in 2024 dollars,
survival-weighted. Not a cohort projection, not an admission counterfactual.

Findings: `RESULT.md`.

## Reproduce

```sh
cd infra/immigration-fiscal/lineage_cost_2026_09_19
PYTHONUNBUFFERED=1 uv run --no-project --with "pandas>=2" --with "numpy>=2" python3 lineage.py
```

Pure arithmetic on stored lane outputs. No downloads, no API keys, no microdata, no
writes outside `derived/`. Runs in about 20 seconds.

Byte-identical re-run check:

```sh
cp -R derived /tmp/lineage_rerun_ref
PYTHONUNBUFFERED=1 uv run --no-project --with "pandas>=2" --with "numpy>=2" python3 lineage.py
diff -rq /tmp/lineage_rerun_ref derived      # must print nothing, rc 0
```

## Files

| File | What it is |
|---|---|
| `inputs.py` | Every input resolved, hashed and loaded. No constant is typed by hand; each is read from a named lane output and carries the row it came from. |
| `lineage.py` | The model, the oracle checks, and all four output tables. |
| `scratch_lineage_cost_ORIGINAL.py` | The pre-lane scratch script, kept verbatim as the audit trail for what was corrected. Not executed by this lane. |

## Inputs (all read-only)

| Input | Used for |
|---|---|
| `ledger_absolute_2026_09_17/derived/age_profiles.csv` | Net balance per person-year by allocation (personal, shared) x account (partial, expanded) x group x age band. This is the complete account **by age**, which supersedes the flat per-person add-on in the scratch script. |
| `ledger_absolute_2026_09_17/derived/lifetime/period_profiles.csv` | Oracle. 768 single-person survival-weighted NPVs this lane must reproduce. |
| `ledger_absolute_2026_09_17/derived/waterfall.csv` | Only to measure how far the scratch script's flat add-on is from the true by-age add-on. |
| `all_age_ledger_2026_09_17/derived/age_profiles.csv` | Cross-check that `shared`/`partial` equals the brief's `all_age_shared` scenario. |
| `lifetime_longevity_sstiming_2026_09_18/derived/survival_tables.csv` | NVSS 2024 lx and Lx, tables `total`, `hispanic`, `nh_white`. |
| `demo_momentum_2026_09_16/cps_fertility_agestd.csv` | Age-standardised own-children-under-5 rates by generation, and the age-specific rates used to derive mean age at birth. |
| `crime_cost_2026_09_16/crime_cost_by_group.csv` | Crime cost per adult 25-64 per year, routes A1 (BJS stock, includes foreign-born) and A2 (ACS institutional stock, US-born). |
| `crime_cost_firstgen_2026_09_18/derived/firstgen_cost_weighted.csv` + `audit.json` | Texas arrest-charge route by legal status, converted to a per-adult basis with the lane's own adult shares. |
| `status_impute_2026_09_16/RESULT.md` | The imputed-unauthorized minus Mexico-born-pooled level difference, parsed from the lane's own table rather than retyped. |
| `mexican_origin_population_total_2026_09_19/derived/arm3_correction_bounds.csv`, `arm5_fiscal_implication.csv` | Fourth-plus identification rate and the attriter's retained share of the fiscal gap. |
| `pronatal_equivalence_2026_09_18/derived/lifetime_equivalence.csv` | Soft triangulation of a second in-repo lifetime construction. |

## Outputs

| File | Contents |
|---|---|
| `derived/lineage_table.csv` | 96 rows: allocation x account x founder status x fertility x attribution x discount. |
| `derived/generation_breakdown.csv` | Central case, both lineages, persons and dollars per generation. |
| `derived/white_reference.csv` | The reference lineage on its own, across the same grid. |
| `derived/sensitivities.csv` | 19 named arms including the three disconfirmation arms. |
| `derived/oracle_period_profiles.csv` | 768 stored-vs-recomputed NPVs. |
| `derived/oracle_pronatal.csv` | 24 stored-vs-located pronatal lifetime balances. |
| `derived/audit.json` | Input sha256s, every parameter with its source, and the check results. |

## Model

One founder aged 25 in calendar year 0. Each generation has its children when the
parent generation reaches age `gen_len` (central 29). Persons per generation multiply
by `multiplier(TFR, attribution)`. Each person contributes their group's age profile,
weighted by NVSS survival exposure `Lx / lx[start_age]`, from their birth year to
calendar year 100 or age 100, whichever comes first. Discounting is at the calendar
year, so the founder's arrival is time zero for both lineages.

Attribution rules, which are the largest single lever:

- `per_capita` — TFR/2. Each child is shared between two parents. The only rule that
  conserves people, and the central case.
- `maternal_full` — TFR. The founder is read as a woman and every child of a lineage
  member is attributed whole to the lineage. The scratch script's "full" arm.
- `intermarried_half` — TFR/4. `per_capita` with mixed children counted half.

The white reference lineage uses the identical rule, the identical generation length
and the identical discounting, with the white age profile, white TFR and (in the
group-specific arm) the NH white life table.

## Limits

- Period profiles, not cohort projections. No productivity growth by default; one arm
  applies 1% real growth to taxes and outlays together.
- No general equilibrium, no behavioural response, no emigration, no remittances.
- The 100-year window truncates G3 and later mid-life. Those generations' totals are
  partial lives, not lifetime balances, and the truncation is not neutral: it can cut
  before or after the expensive years depending on birth year.
- Fertility and intermarriage are assumptions carrying sources, not measurements of
  this lineage.
- The crime social-cost column is McCollister jury-award-derived willingness to pay.
  It sits outside any fiscal ledger and is reported separately from the fiscal line.
  Corrections spending is already inside the expanded fiscal account, so the
  incremental crime cost is reported both gross and net of corrections.
- The repo measures resident groups, not admission. No policy claim is made here.
