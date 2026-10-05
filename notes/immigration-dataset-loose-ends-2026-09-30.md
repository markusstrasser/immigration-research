# Dataset loose ends: how each closed

Date: 2026-09-30. On 2026-09-30 the operator asked for a broad-strokes check of the datasets' labels,
categories, normalizations and capture. It found nothing that invalidates the account and left three
loose ends. The operator then asked "ok let's do the lose ends then ... but quickly". This note records
how each closed, plus the linked-records check that followed. None changes a conclusion.

| Loose end | What was done | Effect on the case ($371.4–434.8bn, low / high) | Where |
|---|---|---|---|
| Legal status not calibrated: the case imputes 4.607M Mexico-born unauthorized | Raked to Pew's 4.3M, DHS's 4.8M and CMS's 5.1M, repricing the EITC, tax compliance and the pension credit | +$1.45 / +1.37bn, −$1.14 / −1.10bn and −$2.91 / −2.80bn. More unauthorized makes the case cheaper: their on-books payroll taxes earn a tenth of the pension accrual, and they lose the EITC | [status_calibration_2026_09_30](../infra/immigration-fiscal/status_calibration_2026_09_30/RESULT.md) |
| SSI has no administrative ethnicity key | SSA's federal SSI by state and age, split at equal take-up | +$1.48 / +1.49bn as an upper bound; +$0.69–0.96bn once the 1996 rules bar noncitizens. The CPS key stays | [ssi_key_bound_2026_09_30](../infra/immigration-fiscal/ssi_key_bound_2026_09_30/RESULT.md) |
| Descendants who stopped identifying as Mexican | Priced at the average resident's cost (below) | +$2.1–20.5bn, depending on the count. The excess over average residents does not change | this note |
| Survey reports against tax and benefit records | Published linkages applied to the case's survey-keyed lines | about −$5bn (−$15bn to +$8bn) | [linked records](immigration-linked-records-evidence-2026-09-30.md) |

## Descendants who stopped identifying

**Counts.** The CPS self-identification union is 40.97M. Adding third-plus attriters gives 41.77M at the
floor and 42.78M at the central, so 0.80–1.81M more
[SOURCE: [population total](../research/immigration-mexican-origin-population-total-2026-09-19.md) §1].
Identity loss keeps growing past the third generation, which puts the lineage at 44.0–46.3M, 3.03–5.33M
beyond the union (ladder 158; the memo's 2026-09-27 revision).

**Price.** Under the case's rules any resident costs other residents $2,581 / $3,847 a year: the shared part
of the decomposition, $102.5 / $152.8bn for 39.71M average residents
[DATA: `main_case_decomposition_2026_09_29/derived/decomposition_sept29.csv`, row `shared`; ladder 269].
Attriters are positively selected: they have +0.76 years of schooling, which closes 72% of the third-plus
schooling gap to whites (population memo §4). So the average resident's cost is the best guess for them.

| Added people | Count | Added cost | Per member (now $9,353 / $10,950) |
|---|---:|---|---|
| Third-plus attriters, floor | 0.80M | +$2.1 / +3.1bn | $9,219 / $10,809 |
| Third-plus attriters, central | 1.81M | +$4.7 / +7.0bn | $9,057 / $10,640 |
| Lineage with identity loss past G3, low | 3.03M | +$7.8 / +11.7bn | $8,872 / $10,446 |
| Lineage with identity loss past G3, high | 5.33M | +$13.8 / +20.5bn | $8,551 / $10,109 |

[CALCULATION: count × $2,581 / $3,847; per member = (case + added) ÷ (39.71M + count)]

Adding people at the average resident's cost raises the total by what any resident costs. It leaves the
group's excess over as many average residents ($269–282bn, ladder 269) where it is, and it lowers the
per-member figure.

**Ceiling.** Suppose the 1.81M central attriters cost what identified third-plus members do: $7,724 / $9,771
each, with children counted in their parents' generation [DATA:
`generation_account_2026_09_24/derived/generation_results_sept29.csv`, convention b, G3plus]. Then they add
+$14.0 / +17.7bn. Their schooling makes this an upper bound, not an estimate.

**Correction, 2026-10-05.** The identity-loss pricing above prices every added person at the average resident's
cost, on the Duncan–Trejo schooling convention. Measured instead (carryover_identity_2026_09_27 §2;
g3_identity_pooled_2026_10_05), third-generation-rate losses and their descendants close C3 = 0.557 (SE 0.246) of
the gap toward third-plus whites, and later losses close none. Priced on v4's rules on the engine, an added person
costs others $6,309–8,790, not $2,581 / $3,847: the arms add +$4.0 / 5.6bn (0.80M), +$9.0 / 12.7bn (1.81M), +$18.9 /
26.4bn (3.04M, arm b) and +$28.8 / 40.1bn (4.27M), on the account's frame.
[CALCULATION: [main_case_lineage_2026_10_05](../infra/immigration-fiscal/main_case_lineage_2026_10_05/RESULT.md),
`derived/v5_summary.json`]
