---
date: 2026-10-07
concepts: [comparison-basis, reference-group, income-tax-incidence, allocation-keys]
status: adopted
supersedes: []
relations:
  - applies: decisions/2026-09-29-main-case-v4.md
  - qualifies: decisions/2026-10-07-main-case-v6.md
evidence: infra/immigration-fiscal/white_replacement_2026_09_28/RESULT.md
---

# 2026-10-07: The comparison groups' income taxes take the main case's own keys: the gap to third-plus whites is $431.6–436.0bn

## Context

The comparison groups (third-plus non-Hispanic whites, non-Hispanic Black residents, Indian origin, an all-residents
slice, and the legacy lane's groups) are priced on rough keys built from CPS ASEC records. Their income taxes followed
the CPS-dollar rule: each group was charged the income tax its members report to the CPS. Like for like (tax before
refundable credits, on the record, published weights), the CPS records $1,981.1bn of federal income tax against the
national line's $2,403.2bn and $490.8bn of state income tax against $536.2bn. It misses $422.1bn and $45.4bn, most
of it at the top of the income distribution. On the comparators' own frame and keys, the CPS-dollar rule charged
$395.9bn of federal and $39.4bn of state income tax to no group. The main case does not have this gap: since v4
(item 3, ladder 249) it keys federal income tax on an IRS-raked key and charges the whole national line.

On 2026-10-07 (16:38 JST) the operator noted that "whites cost others $0.6–1.9k each" gives nobody credit for top
earners' taxes, so whites may roughly break even. The white lane's own arms confirmed it. The recommendation was to put
the comparators' income taxes on the case's own keys, with the old rule and the proportional spread beside. He approved
it at 19:44 ("Ok do"), together with moving the evidence map to v6 and writing the CPS totals to a data file.

## Alternatives considered

1. **Keep the CPS-dollar rule as the central.** Rejected. It understates every group's income tax, most of all the
   groups with more top incomes, and it prices the comparators on a different rule from the case they are compared
   with. It stays as the `cost_cps` arm: A1 $380.3–384.7bn.
2. **Spread the CPS shortfall in proportion to CPS dollars** (`cost_top_tail_proportional`). A check, not the central:
   A1 $421.4–425.8bn. The missing tax sits in the top AGI bins, which IRS's bin shares locate. A proportional spread
   gives the union 0.0555 of the federal line; the raked key gives it 0.0517.
3. **The case's own keys** (adopted). Federal income tax takes v4 item 3's key (`irs_2023_raked_with_cbo_groups`): CPS
   tax before credits in cells of CBO income group × AGI bin, raked to CBO's 2022 group shares and IRS's TY2023 bin
   shares, charging the whole $2,403.2bn. State and local income tax and other personal taxes take the state-liability
   key, as the case keys them.
4. **The personal allocation at the high end, as the case uses at specification 11.** Beside: A1 $448.7 / 453.1bn and
   A3 (white rates at the lineage's ages) $364.1 / 368.4bn. Rejected as the central because every other rough key
   splits a household's amounts over its members, and the benefit-tax rule is shared at both ends. Mixing the two
   allocations inside one comparator would move A3 by −$47.2bn on the allocation alone.
5. **Give the rough union the case's tax-records stack** (its status corrections). Rejected: the comparison is rough
   key against rough key, and the comparators have no such stack. On the same keys the rough union therefore pays
   $11.9 / 23.8bn more income tax than the engine's union.
6. **Re-key the case's own W as well.** The C3 blend prices 1,082,721 lineage members as third-plus whites, through the
   white lane's library at its September 29 default, which keeps the CPS-dollar rule. On the case's keys the case would
   move −$1.748bn at the shared allocation ($387.33 / 459.73bn) and +$1.086bn at the personal one. Measured only: the
   headline moves only on the operator's word. Recommended for the next main-case revision.

## Decision

The comparison groups' central takes the case's own income-tax keys at the shared allocation, at both ends. The
CPS-dollar rule, the proportional spread and the capital arm (capital-side taxes respond) are printed beside it. The
headline stays at $389.1–461.5bn.

On main case v6 (`oct07`, accrual unless noted; low / high, specifications 48 / 11):

| | CPS-dollar rule | Case keys |
|---|---:|---:|
| Union less as many third-plus whites (A1), $bn | 380.3 / 384.7 | **431.6 / 436.0** |
| Per lineage member | $8,896 / 8,998 | **$10,096 / 10,197** |
| A1, cash set, $bn | 212.2 / 218.6 | 263.5 / 269.8 |
| Union less local whites, state by state, at the lineage's ages, $bn | 430.3 / 433.1 | 528.6 / 531.5 |
| Third-plus whites' own cost to others, per member, accrual | $353 / 1,607 | **−$1,200 / +54** |
| The same, cash set | $2,286 / 3,540 | $733 / 1,987 |
| Non-Hispanic Black residents' cost to others, $bn | 527.9 / 575.3 | 501.2 / 548.6 |
| The same per member, over the main case's per member | 1.38 / 1.27 | 1.31 / 1.21 |
| Indian origin, full account, per member | −$10,901 / −9,447 | −$12,890 / −11,436 |
| Legacy, rough union less A1, interest-equivalent, $bn | 81.2 / 81.2 | 101.6 / 101.7 |

- Third-plus whites now about break even on accrual. On the cash set they still cost others $0.7–2.0k each, because
  23% of them are 65 or older and the cash set counts old-age benefits when paid.
- The whites' gap is larger than the rough union's own cost to others ($380.3 / 438.3bn) at the low end, because the
  white slice is a net contributor there.
- The evidence map's claim C8 ("about $320–405bn a year more, depending on which whites") breaks upward at both ends.
  It came from the CPS-dollar rule on the September 27 case. The keys changed, not the data.
- [ASSUMPTION] The added 3.04M keep the case lane's amounts, which are already on the case's keys.
- **Where A1's +$51.27bn comes from** (`derived/income_tax_parts_oct07.csv`; the same at both ends and on both bases):
  - the CPS shortfall spread in proportion to each group's CPS income tax, +$41.08bn;
  - the IRS and CBO raking, which moves that spread toward the top AGI bins, +$12.76bn;
  - the household's tax shared over its SPM unit instead of its tax unit, −$2.21bn;
  - tax before refundable credits, −$0.35bn. This removes a small double count in the old key: credits that offset
    liability came off a group's receipts and were also charged to it as spending;
  - other personal tax on the state key, −$0.01bn.
  Controlled rounding: the raking's unrounded +$12.754bn prints +$12.76bn so the parts add to the total.
- **Local whites move $98.37bn, $47.1bn more than A1.** California and Texas third-plus whites have 35.3% and 33.7%
  of their tax before credits at AGI of $500k or more, against 25.8% for A1, so the raking lifts their key 9.9% and
  13.1%, against A1's 0.6% (+$28.5bn of the difference). Their CPS tax is also larger (+$9.5bn), and at the
  lineage's young ages the SPM split puts more of a household's tax on its young members (+$9.1bn). The key is
  national: no state raking, one scaling.
- The CPS totals are now a data file, `white_replacement_2026_09_28/derived/cps_tax_totals_oct07.csv`. It names the
  variable, placement and key in each row, and replaces the `[DEGRADED: RESULT prose]` source the INDEX used for the
  shortfall (its $393bn and $38bn were the rough key's figures on the published weights).

## Scope

Moved: the comparator lanes (`white_replacement_2026_09_28`, `black_comparator_rough_2026_09_28`,
`indian_full_account_2026_09_29`, `legacy_comparators_2026_09_30`), their readers (`break_conditions_2026_09_29`), the
evidence map (moving to v6 at the operator's request), the INDEX, FAQ, ladder notes and memo revisions. Each lane keeps
`oct05` beside `oct07`, both on the new rule; `sept29` keeps the CPS-dollar rule.

Not moved: the headline and the main-case payload, and the assumption explorer and figures page.

## Evidence

- `white_replacement_2026_09_28/RESULT.md`, section "v6 round 2". `rekey_sept29.py` passes 323 gates on `oct07` and 292
  on `oct05`. Among them: the union's raked shares equal the benchmark lane's at both allocations (1e-12), IRS's bin
  shares are the benchmark's `bins.csv`, and each group's change is minus its change in the three income-tax lines
  (1e-9). `limits_oct07.py` passes 61 gates, with positive controls for W against `white_lines.json` and
  `band_lines.json`.
- The same section in each comparator lane's RESULT, and each lane's `scripts/rerun_lane.py` check (IDENTICAL, exit 0):
  white 86/86 and Black 47/47 (cc793ccf), Indian 43/43 (ac6cc2ac), legacy 29/29 (8bfae970), break conditions 43/43
  (406d3163); the main case's G5 27/27, its payload unchanged. The evidence map follows in 3834b1c8.
- The white library's outside importers (`white_lines.py`, `band_lines.py`, `compare.py`) rebuild byte for byte at
  their September 29 default.

## Revisit if

- The case's W is re-keyed (the next main-case revision).
- IRS publishes TY2024 bin shares, or CBO a 2023 distribution.
- The case adopts one allocation at both ends.
- An IRS-linked survey measures income tax by race or ancestry directly.

## Supersedes

None. The CPS-dollar rule was a lane rule (`white_replacement_2026_09_28/RESULT.md`, section "v4 case (sept29)",
"Rules designed"), now the `cost_cps` arm.
