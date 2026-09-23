# Wage winners and losers inside "other residents"

**Verdict:** The complete account's production term is small (+$8.8–13.3bn) because it nets
large opposite wage changes among other residents. In the account's own long-run model
(capital fully adjusted, Mexican-origin and other workers in a skill cell perfect substitutes,
the account's default), the Mexican-origin union's presence leaves less-educated native workers'
wages **2.2–7.0% lower** than without it, about **$66–166bn a year** of pre-tax earnings, and
more-educated natives' wages **1.0–3.0% higher**, about **$71–163bn**. Where the skill line is
drawn and the between-skill substitution elasticity σ set the size: with high school or less as
the lower group and σ = 2, less-educated natives lose 4.5–5.3% ($81–102bn) and the rest gain
1.2–1.45% ($87–109bn). Less-educated workers born abroad outside the group lose a further
$14–30bn. After tax, natives as a whole come out between −$14.6bn and −$0.3bn; what the account
counts as the production gain is mostly induced tax receipts. With imperfect substitution between
natives and immigrants inside a cell (ε = 3, the removal model's value), the native low-skill loss
shrinks to $26–107bn, other foreign-born workers lose $24–50bn, and natives net +$26–59bn. These
are transfers among the account's beneficiaries: they are already inside the production term and
must not be added to the net. [CALCULATION: `wage_split.py` →
`derived/wage_distribution_long_run_default.csv`, `derived/wage_distribution_by_epsilon_long_run.csv`]

Date: 2026-09-23. Operator request: the real fiscal and social costs, including who bears them.

## Method

No model is re-run. The executed nest grid
(`../production_nativity_nest_2026_09_22/derived/nest_scenarios.csv`, core ownership, Option A by
nativity) reports each branch's wage without the union relative to with it, `wage_pct =
100*(without/with − 1)`, by skill cell. The union's presence therefore changes a branch's earnings
by `−wage_pct/100 × with-target earnings`, with the branch's CPS earnings from
`branch_composition.csv` and hours held fixed. `wage_pct_vs_absent` restates the change relative to
the no-union wage. Ranges run over the grid's proxies (PEARNVAL, WSAL_VAL), normalizations,
labor shares (0.6–0.7) and labor-supply elasticities (0, 0.33) at each split and σ.

| Lower skill group | σ | Native lower group, wage vs absent | $bn | Native upper group | $bn | Natives after tax, $bn |
|---|---:|---:|---:|---:|---:|---:|
| high school or less | 1.5 | −5.7% to −7.0% | −103 to −137 | +1.6% to +2.0% | +111 to +146 | −1.7 to −0.5 |
| high school or less | 2.0 | −4.5% to −5.3% | −81 to −102 | +1.2% to +1.45% | +87 to +109 | −1.2 to −0.4 |
| high school or less | 2.5 | −3.7% to −4.25% | −66 to −81 | +1.0% to +1.15% | +71 to +87 | −1.0 to −0.3 |
| below a BA | 1.5 | −3.4% to −4.2% | −128 to −166 | +2.4% to +3.0% | +126 to +163 | −14.6 to −7.0 |
| below a BA | 2.0 | −2.7% to −3.2% | −100 to −125 | +1.9% to +2.2% | +99 to +122 | −10.9 to −5.5 |
| below a BA | 2.5 | −2.2% to −2.5% | −82 to −100 | +1.5% to +1.8% | +81 to +98 | −8.7 to −4.5 |

Long run, ε = ∞. [DATA: `derived/wage_distribution_long_run_default.csv`]

## Limits

- This is the account's calibrated CES, not a measured wage effect. σ (1.5–2.5) is the range the
  account borrows from Colas–Sachs; empirical estimates of immigration's effect on less-educated
  natives' wages are disputed (see the [canon citation audit](../../../research/immigration-canon-citation-audit-2026-09-17.md)).
- Hours are held at their with-target level, so the dollar figures are first-order.
- In the short run (capital fixed) the model lowers both native groups' wages and moves the gain to
  capital owners; see `derived/wage_distribution_grid.csv` rows with `capital_adjustment == 0`.
- Native includes the US-born of every origin outside the Mexican-origin union, including other
  immigrants' children.
