---
date: 2026-10-07
concepts: [white-reference-ledger, generation-split, income-tax-incidence, comparison-basis, reference-group]
status: adopted
supersedes: []
relations:
  - applies: decisions/2026-10-07-comparators-income-tax-keys.md
  - applies: decisions/2026-09-29-main-case-v4.md
evidence: infra/immigration-fiscal/ledger_absolute_2026_09_17/README.md
---

# 2026-10-07: The white-reference ledger's expanded account takes the main case's income-tax keys (item T): the union's same-age gap to third-plus whites widens from −$7,152 to −$8,306 a person

## Context

The white-reference ledger (`ledger_absolute_2026_09_17`) is the only source of fiscal results by generation against a
white reference. It taxed each record at the income tax the record reports to the CPS. On the ledger's frame, at the
shared allocation, the survey's federal income tax before refundable credits is $2,018.4bn against the national line's
$2,403.2bn, and its positive state income tax liabilities are $499.0bn against $536.2bn. The survey therefore leaves
$385.6bn of federal and $37.2bn of state income tax charged to no one, most of it at the top of the income
distribution. [DATA: `ledger_absolute_2026_09_17/derived/audit.json`, `item_metadata["T|central"]`]

The comparison groups had the same defect, and on 2026-10-07 at 19:44 JST the operator approved putting their income
taxes on the case's own keys ("Ok do"; [decision](2026-10-07-comparators-income-tax-keys.md)). The ledger still compared
the Mexican-origin generations with whites on the survey's taxes, so the gaps the FAQ and the evidence map quote were
understated, and third-plus whites showed a net cost of $1,221 a person at their own ages. At 22:21 JST the operator was
told that the same rule would be applied to the ledger, with its sizing (gaps wider by $0.8–1.3k a person); he did not
object. Item T was built under his standing approvals ("adopt everything that makes sense", 10:19; "ok do what you
think is good", 12:02) and committed as 9d690482.

## Alternatives considered

1. **Keep the survey's taxes in the expanded account.** Rejected. The expanded account reconciles every other line to
   national totals (item U does so for transfers), and leaving $422.9bn of income tax uncharged compares the groups on a
   different rule from the main case and the comparators. It stays as the `--off T` arm, which reproduces the old
   outputs byte for byte.
2. **Spread the shortfall in proportion to each record's survey income tax.** Not run in the ledger. In the comparators
   it moves the union-less-whites gap by +$41.1bn of the raked key's +$51.3bn, because the missing tax sits in the top
   AGI bins, which IRS's bin shares locate and a proportional spread does not.
3. **The case's own keys** (adopted). Federal income tax is the national line times the record's IRS-raked share
   (`tax_key_heldout_2026_09_28/keys.py`, the key v4's item 3 adopted), less the record's survey tax before refundable
   credits, with the part of its EITC that offsets liability added back ($0.85bn). State income tax is the $536.2bn
   line in proportion to the record's state liability floored at zero, less that base. One module supplies the keys
   to every caller; a caller that builds the ledger's charges without them stops with `[BLOCKED]` unless it passes
   `--off T`.
4. **Put T in the partial account too.** Rejected. The partial account is the survey's own view, kept for comparison
   with survey-based studies. It is now labelled "taxes as the survey reports them" wherever it is quoted.
5. **Leave each tax with its earner (the record allocation) as the central.** Beside: nationally T is $468.4bn on the
   record (federal $422.9bn, state $45.4bn) against $422.9bn shared. The ledger, the case's white end and the
   comparators all split a household's amounts equally over its members, so the shared allocation stays central.

## Decision

The ledger's expanded account takes item T at the shared allocation, as the waterfall's step 15 after S. The partial
account and every other item are unchanged. The headline, $389.1–461.5bn, does not move: the main case has keyed
income tax this way since v4, and its generation split (`generation_account_2026_09_24`) uses no reference group.

Old → new, shared allocation, same-age gap against third-plus non-Hispanic whites, $ a person (SE)
[DATA: `ledger_absolute_2026_09_17/derived/complete_gaps.csv` at 9d690482~1 and at 9d690482]:

| Group | Before T | With T |
|---|---:|---:|
| Mexico-born | −7,584 (384) | −8,849 (539) |
| Second generation | −7,521 (615) | −8,499 (912) |
| Third-plus, self-identified | −6,195 (457) | −7,118 (637) |
| Union | −7,152 (302) | −8,306 (446) |
| Union, against all natives | −4,973 (258) | −5,935 (370) |
| Union, age-matched gap against whites, $bn | −358.1 | −403.6 |

- Against all natives the generations move from −5,404 / −5,342 / −4,015 to −6,478 / −6,128 / −4,747.
- Each group's own income tax rises, so absolute balances improve; the gaps widen because whites' T is larger.
  Third-plus whites go from −$1,221 to +$299 a person at their own ages.
- Lifetime from birth at 3%, personal allocation: the second generation's gap to the white reference widens from
  −$183,510 to −$198,754, the third-plus's from −$129,099 to −$147,229. The map's lineage figure moves from $1.29M to
  $1.48M ($513k to $570k at 3%).
- The standard errors widen by 40–50%, because T rests on top-income records: nationally the ten largest white SPM
  units carry 19% of whites' T ($50.9bn of $263.1bn) [DATA:
  `arrival_window_fiscal_2026_09_18/derived/t_concentration.csv`]. Inside one state or metro a few units can carry most
  of it; the local-whites comparator rests on 14 Texas and 16 California households with AGI of $1M or more
  (`white_replacement_2026_09_28`, c61f00aa).

## Scope

Moved: the ledger and its consumers, 37 lanes. Those built on the expanded account take T: among them the generation
comparison, lineage cost, gap incidence, the practitioner range, education by origin and the high-education origin
screen, where India-born degree holders' advantage is no longer clear of zero. The partial-account lanes (arrival
windows, state and metro matching, generation carryover, population total and identity loss) print T beside their
survey-tax columns, and eleven more carry a one-line label. In states and metros the ten largest white
households carry most of T (67% in California, 98% in Texas). Docs: the INDEX, the FAQ (anchors and entries 1, 3,
5–7, 9, 10, 15, 17, 18), the memos that quote the ledger, dated notes on the ladder entries, and the evidence map's
11.3, 13.3 and lineage figures through its registry rows.

Not rerun: the frozen September 19–22 chain (`full_account`, `admin_tax_checks`, `admin_transfer_checks` and their
neighbours). Their outputs feed the main case as fixed inputs and did not change. A rebuild would stop on
`admin_transfer_checks`' pin of macro_closure's pre-T union balance; T must stay out of that chain, whose receipts
reach the case on the case's own keys, so a rebuild needs an `--off T` switch in macro_closure first.
`projection_backtest`'s ignored outputs in this checkout are pre-T; its tracked code and README are current.

Not moved: the headline and the main-case payload, the assumption explorer and the figures page (both pinned to earlier
cases by design).

## Evidence

- 9d690482: `check_gates.py` 57/57, three of them new for T; pytest 16; `scripts/rerun_lane.py` IDENTICAL 39/39.
  `--off T` is byte-identical to the old `derived/` apart from `audit.json` and T's own rows.
- The key module (2aeb02b1) reruns every earlier caller with unchanged outputs.
- Each consumer lane carries a dated note and its own rerun line.

## Revisit if

- The main case changes its income-tax keys, or adopts one allocation at both ends.
- IRS publishes TY2024 bin shares, or a survey linked to tax records measures income tax by ancestry or race.
- A state or metro comparison needs T: there, a handful of survey records stand in for the top bracket, and a pooled
  or administrative key should replace the national one.

## Supersedes

None. The survey-tax rule was part of the ledger's construction, now the `--off T` arm.
