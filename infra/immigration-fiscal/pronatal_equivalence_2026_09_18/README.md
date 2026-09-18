# Lifetime period profiles and the pro-natal equivalence budget — September 18, 2026

**Verdict:** On the all-age partial account's period profile (today's cross-section applied as a lifetime), a third-plus non-Hispanic white child has a lifetime balance of +$400k undiscounted, +$231k at 3%; a Mexico-born adult arriving at 25 has −$109k / +$28k; a Mexican second-generation child −$109k / −$12k; a third-plus self-identified child +$16k / +$69k. The fiscal budget that could be paid for one additional reference-profile child and leave the treasury where one more Mexican-origin resident leaves it is therefore **$202k (Mexico-born, from 25), $243k (second generation) and $161k (third-plus) at 3%** against a white child, and $139k / $180k / $99k against an all-native child. Undiscounted, $509k / $509k / $384k against white and $380k / $380k / $255k against all natives.

## Reproduce

```sh
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/pronatal_equivalence_2026_09_18/lifetime_profiles.py
```

Reuses `all_age_ledger_2026_09_17/analyze.py` (imported, `all_age_shared` scenario, full weight, shared allocation, 8 age bands). Gate: the three target profiles reproduce the stored `age_profiles.csv` to $0.0000. Outputs `derived/age_profiles_references.csv` (adds the two references) and `derived/lifetime_equivalence.csv` (rates 0, 2, 3, 5%).

## Per-band balance per person (all_age_shared)

| band | white 3rd+ | all native | Mexico-born | 2nd gen | 3rd+ self-ID |
|---|---:|---:|---:|---:|---:|
| 0–17 | +4,965 | +2,535 | −3,639 | −3,964 | −214 |
| 18–24 | +10,363 | +7,897 | +2,813 | +2,445 | +4,847 |
| 25–34 | +14,942 | +12,945 | +5,972 | +6,212 | +9,491 |
| 35–44 | +11,657 | +10,555 | +1,240 | +6,092 | +7,388 |
| 45–54 | +13,457 | +12,041 | +3,045 | +4,746 | +7,462 |
| 55–64 | +14,782 | +12,862 | +2,667 | +7,055 | +4,926 |
| 65–74 | −14,024 | −14,514 | −11,848 | −15,402 | −15,397 |
| 75+ | −21,298 | −21,179 | −14,982 | −17,737 | −19,128 |

Children carry a per-head share of their household's taxes under shared allocation, which is why reference children are positive; person-source assignment moves that to the adults and leaves lifetime sums nearly unchanged.

## Caveats

- Period profile, not a cohort projection: each age band is today's people of that age. Lifetimes are 83 years by construction (75+ band given 8 years).
- Partial account. The complete account (`ledger_absolute_2026_09_17`) adds about −$1,100 to −$1,500 per person-year to the white-reference gap, roughly +$30–45k to each budget at 3%. Not applied here.
- The marginal child induced by a subsidy is not the average reference child; the all-native columns are the fairer comparator.
- Descendants are in the profiles (a Mexico-born adult's children are the second-generation row; a reference child's children are in the reference), so the budgets already carry one generation of descendants at today's profiles.
- No behavioural response, no general-equilibrium effect, no valuation of the immigrant's own welfare. This is a treasury-equivalence number only.
