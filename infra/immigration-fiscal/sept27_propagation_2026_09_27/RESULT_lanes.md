**Verdict:** Done. The back-cast, distribution, uncertainty and debt-legacy lanes default to `sept27`, keep
`sept26_schools`, `sept26` and `sept24` (and `sept23` where a lane had it) byte-reproducible, pass every gate, write
byte-identical files on two runs, and pass their 31 tests. The debt lane now compounds cash flows only: 2024 legacy
interest is $30.9–41.6bn (schools case $30.1–37.9bn). The return on public capital (federal $0.83 / 1.74bn) and
the capped programs ($5.09bn) are reported beside it and never compounded. Per the parent note, the uncertainty
lane's CPS block carries the benefit keys jointly: the per-case SE is $10.55–10.66bn ($10.98–11.07bn with their SE
appended as if independent), the 95% union $300.9–408.1bn, and nothing calls it a floor. Old → new tables are in
each section.

Model self-report: claude-opus-5-5 (Opus 5.5), 2026-09-27.

# W1 `lanes`: the September 27 main case in the back-cast, distribution, uncertainty and debt-legacy lanes

In the brief's order: back-cast, distribution, uncertainty, debt legacy. I stayed in the shared checkout, as the
brief directs; nothing was committed, staged, stashed or reset.

Regression gate (protocol a), run before any edit: every lane rebuilt its tracked outputs byte for byte on
`sept26_schools`, every run exited 0, and the 20 lane tests passed.

## 1. Back-cast (`historical_backcast_2026_09_20/`)

`backcast.py` defaults to `--case sept27` and adds the `*_sept27_*` concepts. The earlier concepts keep their
values, and `--case sept26_schools`, `sept26` and `sept24` with `--out-dir` rebuild c0297e4, f5b4aae and da2b107
byte for byte (`test_backcast.py`, 5 tests pass). Two default runs are byte-identical.

The new helper `case_components.cjs` evaluates the case package at each profile's end specifications and writes
`derived/case_components_sept27.json`: the schools case's cost there (the base) and each addition. `backcast.py`
carries the base with the existing rules on the schools case's receipts. Each addition carries its own national
series times the group's population-share path:

| Part | Series |
|---|---|
| Long-run road and park responses | NIPA 3.17 lines 5 and 8 |
| Rental assistance | NIPA 3.13 line 4 |
| Enterprise surplus (receipt at 1) | NIPA 3.1 line 19 |
| Return on public capital, 24 components | FA Table 7.1 net stocks (average of two yearends) at a constant real rate; the 11 enterprise components follow line 79 together |

No series is missing: FA Table 7.1 runs from 1925 and the NIPA lines cover 2005–2024. The flat rule holds every
part per person. The capital return stays in these totals as an imputed resource cost (audit §1).

Gates (all pass): base plus additions equals the case cost at each end, and no other line moves (1e-9); the main
profile's parts equal the case's `change_at_fixed_specifications` (1e-9) and `capital_at_end_specifications`
(1e-9); the base equals the profile's `schools_case` band (1e-4, the file's rounding); the adopted anchors equal
`main_case_bands.csv` (1e-4); each FA component's 2024 average equals the capital lane's stock (1e-6); each NIPA
cell's 2024 value equals the account's national amount (1e-3); the parts add to their concept in every window
(1e-9).

Old (schools case, `*_schools_full_*`) → new (`*_sept27_*`), $tn, `derived/backcast_windows.csv`:

| Concept, end | Rule | 10 years (2015–2024) | 15 years (2010–2024) | 20 years (2005–2024) |
|---|---|---:|---:|---:|
| `net_cost_cbo_informed`, low | flat | 2.4645 → 3.0683 | 3.5944 → 4.4750 | 4.5670 → 5.6860 |
| `net_cost_cbo_informed`, low | ratio | 2.2432 → 2.7676 | 3.2086 → 3.9555 | 3.8602 → 4.7870 |
| `net_cost_cbo_informed`, low | income | 2.5408 → 3.0653 | 3.7932 → 4.5401 | 4.6760 → 5.6028 |
| `net_cost_cbo_informed`, high | flat | 2.7835 → 3.6932 | 4.0597 → 5.3865 | 5.1583 → 6.8442 |
| `net_cost_cbo_informed`, high | ratio | 2.5405 → 3.3474 | 3.6266 → 4.7745 | 4.3743 → 5.7970 |
| `net_cost_cbo_informed`, high | income | 2.8382 → 3.6450 | 4.2112 → 5.3591 | 5.1901 → 6.6128 |
| `net_cost_full_proportional`, low | flat | 2.8725 → 3.3113 | 4.1895 → 4.8295 | 5.3232 → 6.1364 |
| `net_cost_full_proportional`, low | ratio | 2.6234 → 2.9929 | 3.7431 → 4.2661 | 4.5176 → 5.1597 |
| `net_cost_full_proportional`, low | income | 2.9211 → 3.2906 | 4.3277 → 4.8507 | 5.3334 → 5.9755 |
| `net_cost_full_proportional`, high | flat | 3.1916 → 3.8188 | 4.6548 → 5.5696 | 5.9145 → 7.0767 |
| `net_cost_full_proportional`, high | ratio | 2.9208 → 3.4620 | 4.1611 → 4.9248 | 5.0316 → 5.9677 |
| `net_cost_full_proportional`, high | income | 3.2185 → 3.7596 | 4.7456 → 5.5094 | 5.8474 → 6.7835 |

The whole-budget rules now give $2.77–3.69tn over 2015–2024 (schools case $2.24–2.84tn), $3.96–5.39tn over
15 years and $4.79–6.84tn over 20. The 2024 anchors are the case band: $321.8194 / 387.3701bn (proportional
reference $347.3127 / 400.5344bn), in `derived/backcast_annual.csv`.

The capital return is $0.29tn (low) and $0.49tn (high) of the 10-year totals under the ratio rule, $0.32 / 0.53tn
flat (`derived/case_parts_windows.csv`). The enterprise surplus is smaller under the ratio rule (0.019tn over 10
years) than flat (0.053tn): the enterprises' national operating loss was $3.4bn in 2005 and $2.8bn in 2015 (nominal),
against $47.5bn in 2024 (NIPA 3.1 line 19).

Files: `backcast.py`, `case_components.cjs` (new), `test_backcast.py`, `README.md`,
`derived/backcast_annual.csv`, `derived/backcast_windows.csv`, `derived/case_components_sept27.json` (new),
`derived/case_parts_windows.csv` (new), `derived/case_parts_annual.csv` (new: each part by year, which the debt
lane reads to keep the capital return and rental assistance out of its whole-budget rules).

## 2. Distribution (`distribution_weights_2026_09_23/`)

`distribute.py` defaults to `--case sept27`. `LATER_CASES` entries are now a `Case` tuple that also names the
case's profile (`long_run_non_school_full` here) and an optional input from `case_ends.cjs`. A moves at each band
end by the case's change, +63.3309 / +95.4153bn; P and F do not move. The earlier cases rebuild their commits byte
for byte: sept26_schools 39b854b, sept26 f697514, sept24 6e554a3, sept23 5b8957e (`test_distribute.py`, 6 tests
pass). Two default runs are byte-identical and equal the working tree; 261 gates pass.

The new helper `case_ends.cjs` evaluates the case at its end specifications (48 low, 11 high in both methods,
averaged) and writes `derived/case_ends_sept27.json`: the capital return (total and by level) and the capped
programs' amounts. Gates: the band equals `summary.json` `main_case` (1e-9) and the `adopted` row (1e-4); the
capital return equals `capital_at_end_specifications` in total and by level (1e-9); rental assistance equals
`lines_at_end_specifications` (1e-9); both capped lines respond at 1. `distribute.py` refuses the file if any
input's hash changed.

**Three columns (audit §1).** A + F is split at each band end into cash financing, the resource cost (the capital
return, financed by each convention like the cash part and reported alone as `fiscal_resource_*`) and the
displaced beneficiaries. At the low / high ends: cash −286.69 / −325.82bn, resource cost −33.80 / −55.69bn
(federal −0.83 / −1.74bn), displaced −5.09 / −5.09bn (`inputs.json` `financing_columns`).

**Capped programs (brief item 6).** Rental assistance ($4.53bn) and LIHEAP ($0.56bn) fall on eligible
non-recipients among other residents, equal per household, under both conventions; TANF-type aid
(`family_and_general_assistance`, $12.3 / 11.7bn) stays with the conventions. Proxies, on the CPS ASEC 2025
household file:

- rental assistance: renter households paying cash rent with money income below 50% of their state's median
  household money income, neither in public housing nor paying reduced rent (HPUBLIC, HLORENT: the flags the
  account's rental key uses). Source: HUD's very-low-income rule, 24 CFR 5.603 and 982.201(b); the proxy uses the
  state median household income and no family-size adjustment. 10.27m households, $441 each;
- LIHEAP: households below 150% of the 2024 HHS poverty guideline for their size (89 FR 2961), with no energy
  assistance (HENGAST). Source: 42 U.S.C. 8624(b)(2)(B); the proxy omits the 60%-of-state-median alternative.
  17.95m households, $31 each.

The texts are cached in `_cache/capped/` (ignored) with their hashes in `inputs.json`; a gate finds each pinned
figure in them. The displaced loss falls on the bottom fifth (−$3.83bn, 0.67% of its resources) and the second
(−$1.12bn). Financed by tax shares, the bottom fifth would have borne $0.15bn of it; by per-person cuts, $1.02bn.
Both programs target the poorest eligible households, so the equal share per eligible household probably places
the loss too high in the distribution [INFERENCE].

Old (schools case, HEAD) → new, SPM ranking, negative = cost:

| Quantity | Unit | Schools case | Sept 27 | File |
|---|---|---:|---:|---|
| fiscal channel, budget part (A_mid + F_c; from Sept 27 less the capped programs) | $bn | -276.72 | -351.00 | `derived/channel_by_quintile.csv` |
| fiscal channel, tax-share financing, fifth 1 | $bn | -8.39 | -10.64 | `derived/channel_by_quintile.csv` |
| fiscal channel, tax-share financing, fifth 2 | $bn | -17.70 | -22.44 | `derived/channel_by_quintile.csv` |
| fiscal channel, tax-share financing, fifth 3 | $bn | -29.83 | -37.84 | `derived/channel_by_quintile.csv` |
| fiscal channel, tax-share financing, fifth 4 | $bn | -48.92 | -62.05 | `derived/channel_by_quintile.csv` |
| fiscal channel, tax-share financing, fifth 5 | $bn | -171.89 | -218.03 | `derived/channel_by_quintile.csv` |
| fiscal channel, per-person cuts, each fifth | $bn | -55.35 | -70.20 | `derived/channel_by_quintile.csv` |
| fiscal channel, top fifth's part under tax-share financing | % | 62.12 | 62.12 | `derived/channel_by_quintile.csv` |
| fiscal channel under per-person cuts, share of resources, bottom / top fifth | % | -9.75 / -1.03 | -12.37 / -1.31 | `derived/channel_by_quintile.csv` |
| cash financing (fiscal_cash_a) | $bn | — | -306.26 | `derived/channel_by_quintile.csv` |
| resource cost: return on public capital (fiscal_resource_a) | $bn | — | -44.74 | `derived/channel_by_quintile.csv` |
| displaced beneficiaries: rental assistance and LIHEAP | $bn | — | -5.09 | `derived/channel_by_quintile.csv` |
| displaced beneficiaries, bottom / second fifth | $bn | — / — | -3.83 / -1.12 | `derived/channel_by_quintile.csv` |
| central total with the social items (TOTAL) | $bn | -311.42 | -390.80 | `derived/channel_by_quintile.csv` |
| central total, share of resources, bottom / top fifth, tax-share | % | -5.50 / -2.35 | -6.58 / -3.21 | `derived/channel_by_quintile.csv` |
| central total, share of resources, bottom / top fifth, per-person | % | -13.78 / -0.17 | -17.07 / -0.45 | `derived/channel_by_quintile.csv` |
| central total at eta 1.3, equal-split equivalent, tax-share | $bn | -199.04 | -237.60 | `derived/weighted_totals.csv` |
| central total at eta 1.3, mean-normalized, tax-share | $bn | -445.42 | -531.69 | `derived/weighted_totals.csv` |
| central total at eta 1.3, equal-split equivalent, per-person | $bn | -378.71 | -465.49 | `derived/weighted_totals.csv` |
| central total at eta 1.3, mean-normalized, per-person | $bn | -847.48 | -1,041.67 | `derived/weighted_totals.csv` |
| outside the budget: bottom four fifths / top fifth | $bn | -80.72 / 46.02 | -80.72 / 46.02 | `derived/channel_by_quintile.csv` |
| direct fiscal response A at the band ends (negative = cost) | $bn | -271.81 / -300.75 | -335.14 / -396.16 | `derived/inputs.json` |

The lane's `RESULT.md` has a dated verdict bracket and a section "The September 27 case".

Files: `distribute.py`, `case_ends.cjs` (new), `test_distribute.py`, `RESULT.md`, `derived/case_ends_sept27.json` (new),
8 changed derived files (`channel_by_decile.csv`, `channel_by_percentile.csv`, `channel_by_quintile.csv`,
`gates.json`, `inputs.json`, `ranges_weighted.csv`, `regressivity.csv`, `weighted_totals.csv`); the other five
are unchanged. Ignored inputs: `_cache/capped/` (four source texts).

## 3. Uncertainty (`uncertainty_propagation_2026_09_22/`)

Parent note (2026-09-27, 23:40): the sampling SE is not a floor. The administrative benefit-rekey correction is
computed from the same 160 CPS replicate weights as the account and correlates with it at about −0.4, so the
joint SE is smaller than the independent append. Carry it jointly as the audit's `probe_uncertainty.py` does,
report the old independent-append SE beside the joint one, make the joint SE the primary CPS block, drop "floor"
and "lower bound", and never add the pooled medical translator's $8.039bn SE independently: disclose it as
unresolved. Done as below.

`later_cases.json` has a `sept27` entry, and `propagate.py` defaults to it. `sept24_specs.cjs` costs a case whose
package exports `evaluateFull` through that package, on the case's own 64 specifications. Its gates: the adopted
responses replace the September 24 ones one for one; each line takes its specification's response; the costs
span `main_case` and `uncorrected_at_adopted_responses` (1e-9); the payload model equals the methods' mean of
`per_spec.csv` at every specification in cost and capital return (1e-9, max 2.3e-13); the derivatives rebuild the
return on both models (1e-9). `derived/sept27/spec_costs.csv` carries the capital return in its own columns
(uncorrected and case) and its derivative with respect to each key line's group amount.

`propagate.py --case sept27` rebuilds every uncorrected specification from its September 20 case (1e-6) with the
long-run lines, rental assistance, the enterprise receipt and the capital return, and a new gate rebuilds the
return from the derivatives and the lane's line targets (1e-6). The errors flow through the return's keys: each key
line's CPS weight adds the derivative, health capital joins the MEPS gradient, and the K-12 and college returns
scale with the school correction. Rental assistance is replicated on its account key and the enterprise receipt on
the population share. The positive controls (the September 20 case's CPS, MEPS and school errors) still reproduce.

**The benefit keys, jointly.** `benefit_replicates()` rebuilds the producer's central re-keying factors
(`admin_benefit_keys_2026_09_24/compare.py`) on all 161 CPS weights; each change and its replicate SE must equal
`program_keys.csv` (1e-8). `sept24_specs.cjs` writes each line's stack factor in the case payload
(`derived/sept27/benefit_factors.csv`, the methods' mean; gates: the case uses the central package with no
deviation, each shift over its change equals `stackFactor` to 1e-12, the four transfer lines respond fully), and
`propagate.py` gates the file's changes against the producer's (1e-9). Per replicate, each line's change times its
stack factor and response (transfers 1, rental assistance 1 in this case) joins the account's deviation before the
variance. `se_cps_fiscal_keys_bn`, the combined SEs and the intervals use that joint block; the account's block
alone, the benefit keys' own SE, their correlation, the two appended as if independent, the joint block with the
factor-product term and the published append (`se_with_benefit_keys_bn`, `package_se.csv`) sit beside it.

Positive control: the same code forced on for the schools case in scratch reproduces the audit probe's 64 rows
(account SE, benefit SE, correlation, independent append, joint first order, joint with the factor product,
combined) to 5e-15, and its account-only and appended columns equal the lane's published schools-case columns
exactly (`scratchpad/w1/sept27/unc/control.py`, `control.log`).

The older cases rerun without any tracked change (`--case sept26_schools`, `sept26`, `sept24`, `sept20`, then
`audit.py`, all after this change), two `sept27` runs are byte-identical (all five files, `sept24_specs.cjs` and
`propagate.py` each run twice), and 15 tests pass (new: one parametrized case, a test pinning the capital return
and the K-12 and college returns to `per_spec.csv`, and a test of the joint block's identities).

The joint CPS SE is $0.50–0.53bn below the two appended as if independent. The account's own CPS block falls
slightly although more lines respond: the added lines' replicate deviations move with the receipts' (correlation
0.30), so they offset part of them. The rate, the BEA stocks and the long-run responses carry no error model here;
they are arms of the case. The SE is a partial sampling approximation whose net error is unresolved: the
production term's and school supplement's covariances with the CPS keys remain omitted, and so does the pooled
medical translator's ($8.039bn SE before LTSS and package scaling, sharing 2024 MEPS donors with the base; not
added, disclosed in the lane's RESULT).

Old (schools case) → new. Before the parent note this section gave the September 27 SE as $10.92–11.00bn and the
union as $300.25–408.77bn (the account's CPS block alone); that is the third row.

| Quantity | Unit | Schools case | Sept 27 | File |
|---|---|---:|---:|---|
| **per-case SE, sources independent, CPS block joint with the benefit keys** | $bn | 10.60 to 10.71 (audit probe) | **10.55 to 10.66** | `derived/<case>/summary.json` `se_independent_bn` |
| per-case SE, benefit keys' SE appended as if independent (published method) | $bn | 10.99 to 11.09 | 10.98 to 11.07 | `se_with_benefit_keys_bn` |
| per-case SE, sources independent, without the benefit keys | $bn | 10.93 to 11.03 | 10.92 to 11.00 | schools: `se_independent_bn`; Sept 27: from the CSV's columns |
| per-case SE, all positively correlated | $bn | 17.96 to 18.39 | 17.65 to 18.09 | `se_positive_correlation_bn` |
| CPS block, joint | $bn | 8.54 to 8.67 (audit probe) | 8.42 to 8.57 | `se_cps_bn` |
| CPS block of the account alone | $bn | 8.95 to 9.06 | 8.87 to 8.99 | `se_cps_account_keys_bn` |
| benefit keys' own replicate SE | $bn | 1.11 to 1.15 (rental assistance at 0) | 1.20 to 1.23 | `se_benefit_keys_replicate_bn` |
| their correlation with the account | | −0.42 to −0.40 | −0.43 to −0.40 | `corr_cps_benefit_keys` |
| 95% intervals of the main band's cases, union | $bn | 236.90 to 313.41 | 300.92 to 408.06 | `ci95_union_bn` |
| 95% intervals at the correlated upper bound, union | $bn | 222.53 to 327.23 | 286.48 to 422.07 | `ci95_envelope_union_bn` |
| 95% intervals with the benefit keys appended, union | $bn | 236.78 to 313.52 | 300.13 to 408.89 | `ci95_with_benefit_keys_union_bn` |
| capital return across the 64 specifications | $bn | — | 33.80 to 55.69 | `capital_return_band_bn` |
| capital return's own CPS part | $bn | — | 0.20 to 0.35 | `se_cps_capital_part_bn` |
| per-case SE, uncorrected model at the adopted responses (control, no benefit keys) | $bn | 12.27 to 12.34 | 12.26 to 12.33 | `se_independent_bn` |

The schools case's joint values come from the audit's probe, which this lane's code reproduces; its published
files are unchanged.

Files: `later_cases.json`, `sept24_specs.cjs`, `propagate.py`, `test_uncertainty.py`, `RESULT.md` (verdict bracket,
a section "The September 27 case", coverage and a Revisions entry withdrawing the floor wording), `derived/sept27/`
(new: `spec_costs.csv`, `line_targets.csv`, `benefit_factors.csv`, `case_uncertainty.csv`, `summary.json`). No
file of an earlier case changed.

## 4. Debt legacy (`debt_legacy_2026_09_23/`)

`debt_legacy.py` defaults to `--case sept27`. Regression gate first: the schools-case default rebuilt all 14
tracked files byte for byte and the 4 tests passed. After the change `--case sept26_schools`, `sept26`, `sept24`
and `sept23` rebuild 90c4b23, e62fccb, ed1b623 and 96a5c3b byte for byte (`test_debt_legacy.py`, 5 tests pass,
the schools case newly pinned). Two default runs are byte-identical and equal the working tree. The sept27 run
rewrites the two earlier bridge files unchanged.

**Engine port (brief item 4).** `lines_at()` now takes both override kinds engine.js has, a line id and
`receipt:<id>`, from the payload's `meta.responses`: the two long-run lines (in the two long-run profiles),
`housing_subsidies` at 1 and `receipt:enterprise_surplus` at 1. `capital_rows()` ports the capital return from
`meta.capital_return` (key kinds `lines_amount_over_national` and `receipt_amount_over_national`; response kinds
`line_response`, `line_response_over_share`, `long_run_subfunction`, `enterprises_switch`, `fixed`) and splits it
by component level. The case's own profiles replace the lane's (the `profiles` of its `LATER_CASES` entry). The payload
gate admits the 8 enterprise re-key edits, which become the component `enterprise_rekey`.

Gates on the port (`summary.json` `case.per_spec_gates`), at all 64 specifications against the methods' mean
of `per_spec.csv`:
- cost and engine cost: 2.3e-13 (tolerance 1e-6);
- capital return in total, by level, part and component, the receipt's response, group amount and cost, and the
  three lines' responses and group amounts: at most 1.4e-14 (1e-9);
- the receipt alone at 1, no other override and no capital: the cost moves by `enterprise_surplus_receipt_cost_bn`
  (1.9e-14);
- federal plus state and local, over cash, displaced beneficiaries and the capital return, equals `cost_bn` + P at
  every specification and payer convention (2.3e-13), and the capital's federal and state-local parts equal
  `capital_federal_bn` and `capital_state_local_bn` (1.4e-14). The per-row identity would be vacuous; this one
  checks the split against the case lane's own totals;
- `main_case_bands.csv` `adopted` and `uncorrected_at_adopted_responses` rows for all three profiles (4.9e-5; the
  file rounds to 1e-4), and `summary.json`'s bands (1e-6);
- the long-run subfunctions add, level by level, to NIPA 3.17's 2024 federal and state-local consumption (1e-6)
  and blend to the line's response at every corner (1e-12).

**Correction applied (cash flows only).** The compounded flow is the engine's lines less the capped programs:
the long-run lines as current spending, split by subfunction level (federal subfunctions federal, state-local
ones through the function's grant share, 0 under the low convention), and the enterprise surplus receipt at
t32(23)/t31(19) = 3.84%, its own row. The programme rules carry that receipt by each level's own series (NIPA 3.2
line 23, 3.3 line 22); the federal enterprises' result changes sign in 2005–2009 and 2016–2022. The capped
programs (rental assistance, federal; LIHEAP, at its energy-assistance share) have no budget response: LIHEAP,
compounded in every earlier case, now leaves the cash gap too. The whole-budget rules subtract the back-cast's
capital-return and rental parts by year (`case_parts_annual.csv`) and LIHEAP at its 2024 share of the base.

Three columns, 2024, main profile, central convention (`derived/federal_split_2024.csv`):

| $bn | Low end | High end | Federal part, low / high |
|---|---:|---:|---:|
| Cash financing, compounded | 282.69 | 326.43 | 37.26 / 62.21 |
| of which the enterprise surplus receipt | 5.56 | 5.56 | 0.21 / 0.21 |
| Resource cost: return on public capital, never compounded | 33.80 | 55.69 | 0.83 / 1.74 |
| Displaced beneficiaries: rental assistance and LIHEAP, never compounded | 5.09 | 5.09 | 5.05 / 5.05 |
| Sum = net cost + P | 321.58 | 387.21 | |

`derived/sept27_bridge_2024.csv` walks the schools case to this one in those columns. Each step equals the case
lane's `change_at_fixed_specifications` part (1e-6) and moves only its own lines (1e-9): LIHEAP leaves the cash gap
(−$0.56bn, federal −$0.52bn); the long-run responses add $19.44 / 29.63bn of cash, $1.08 / 7.07bn federal; the
enterprise receipt adds $5.56bn, $0.21bn federal; rental assistance and the capital parts go to their own
columns; the range ends do not move (both cases end at specifications 48 and 11).

**Flag.** NIPA 3.17 line 61 (federal grants for economic affairs) is $160.8bn in 2020 and $258.0bn in 2021, against
$9.7–22.0bn in every other year, probably the pandemic relief grants [INFERENCE]. The long-run lines' state-local
part therefore counts as 75% and 100% federal in those years. With those two years at the 2019/2022 average
increase, the interest would be $30.3–40.8bn, $0.6 / 0.8bn lower [CALCULATION: scratch]. The ex-pandemic rule
replaces both years ($22.2–32.8bn).

**Pre-existing gap, named, not repaired.** The engine compounds current spending, which includes consumption of
fixed capital, not gross investment and capital transfers. The 2024 federal bridge from current saving
(−$1,874.5bn) to net lending (−$2,106.2bn), −$231.8bn, is read from the pinned NIPA 3.2 and gated to add up; it is
a national diagnostic, not a group correction (`summary.json` `case.pre_existing_gap`).

The lane's `RESULT.md` has a dated verdict bracket and a section "The September 27 case".

Old (schools case, 90c4b23) → new, main benchmark, central rule and convention unless stated:

| Quantity | Unit | Schools case | Sept 27 | File |
|---|---|---:|---:|---|
| federal part of the 2024 cash gap, central convention | $bn | 36.49 to 55.44 | 37.26 to 62.21 | `derived/federal_split_2024.csv` |
| 2024 cash gap (schools case: the whole gap, cost + P) | $bn | 258.3 to 291.8 | 282.7 to 326.4 | `derived/federal_split_2024.csv` |
| federal share of the 2024 cash gap, central convention | % | 14.1 to 19.0 | 13.2 to 19.1 | `derived/federal_split_2024.csv` |
| federal share of the 2024 cash gap, low convention | % | 4.0 to 10.1 | 3.7 to 10.8 | `derived/federal_split_2024.csv` |
| federal share of the 2024 cash gap, high convention | % | 18.9 to 25.3 | 17.5 to 24.7 | `derived/federal_split_2024.csv` |
| resource cost: return on public capital, 2024 (never compounded) | $bn | — | 33.80 to 55.69 | `derived/federal_split_2024.csv` |
| resource cost, federal part | $bn | — | 0.83 to 1.74 | `derived/federal_split_2024.csv` |
| displaced beneficiaries: rental assistance and LIHEAP, 2024 (never compounded) | $bn | — | 5.09 to 5.09 | `derived/federal_split_2024.csv` |
| displaced beneficiaries, federal part, central convention | $bn | — | 5.05 to 5.05 | `derived/federal_split_2024.csv` |
| displaced beneficiaries, federal part, low convention | $bn | — | 4.53 to 4.53 | `derived/federal_split_2024.csv` |
| enterprise surplus receipt in the cash gap (its own row) | $bn | — | 5.56 to 5.56 | `derived/federal_split_2024_lines.csv` |
| enterprise surplus receipt, federal part (t32(23)/t31(19) = 3.84%) | $bn | — | 0.21 to 0.21 | `derived/federal_split_2024_lines.csv` |
| long-run roads and other economic affairs line, federal part, central convention | $bn | — | 1.00 to 6.35 | `derived/federal_split_2024_lines.csv` |
| long-run roads and other economic affairs line, federal part, low convention | $bn | — | 0.00 to 5.05 | `derived/federal_split_2024_lines.csv` |
| long-run roads and other economic affairs line, federal part, high convention | $bn | — | 1.00 to 6.35 | `derived/federal_split_2024_lines.csv` |
| long-run parks line, federal part, central convention | $bn | — | 0.09 to 0.73 | `derived/federal_split_2024_lines.csv` |
| long-run parks line, federal part, low convention | $bn | — | 0.00 to 0.64 | `derived/federal_split_2024_lines.csv` |
| long-run parks line, federal part, high convention | $bn | — | 0.09 to 0.73 | `derived/federal_split_2024_lines.csv` |
| legacy stock entering 2024 (central rule) | $bn | 932.4 to 1,171.4 | 956.8 to 1,287.7 | `derived/stocks.csv` |
| stock, share of debt at end FY2023 (central rule) | % | 3.55 to 4.46 | 3.65 to 4.91 | `derived/stocks.csv` |
| legacy interest, 2024 (central rule) | $bn | 30.14 to 37.87 | 30.93 to 41.63 | `derived/stocks.csv` |
| interest per group member (central rule) | $ | 737 to 926 | 756 to 1,018 | `derived/stocks.csv` |
| interest per other resident (central rule) | $ | 101 to 127 | 103 to 139 | `derived/stocks.csv` |
| interest, share of FY2024 net interest (central rule) | % | 3.43 to 4.30 | 3.52 to 4.73 | `derived/stocks.csv` |
| interest over the account's interest row allocation (central rule) | ratio | 0.23 to 0.29 | 0.24 to 0.32 | `derived/stocks.csv` |
| the brief's D, stock at the end of FY2024 (central rule) | $bn | 962.5 to 1,209.3 | 987.7 to 1,329.3 | `derived/stocks.csv` |
| nominal sum of the 2005-2023 federal gaps (central rule) | $bn | 816.0 to 1,018.9 | 838.5 to 1,119.4 | `derived/stocks.csv` |
| the 2024 gap's own part-year interest (central rule) | $bn | 0.59 to 0.90 | 0.60 to 1.01 | `derived/stocks.csv` |
| legacy interest across back-cast rules, central convention | $bn | 8.03 to 38.69 | 8.20 to 42.45 | `derived/stocks.csv` |
| legacy stock across back-cast rules, central convention | $tn | 0.25 to 1.20 | 0.25 to 1.31 | `derived/stocks.csv` |
| legacy interest across rules and payer conventions | $bn | -3.11 to 45.64 | -3.13 to 49.40 | `derived/stocks.csv` |
| legacy interest, every specification | $bn | -4.24 to 61.24 | -4.25 to 66.29 | `derived/stocks.csv` |
| legacy interest, central rule, every specification | $bn | 5.98 to 60.15 | 5.94 to 65.19 | `derived/stocks.csv` |
| legacy interest, low payer convention | $bn | 18.88 to 26.75 | 18.84 to 29.35 | `derived/stocks.csv` |
| legacy interest, high payer convention | $bn | 34.74 to 44.81 | 35.53 to 48.57 | `derived/stocks.csv` |
| legacy interest, constant 3.22% rate | $bn | 32.56 to 40.95 | 33.38 to 45.01 | `derived/stocks.csv` |
| legacy interest, 10-year Treasury rate | $bn | 40.45 to 50.83 | 41.51 to 55.87 | `derived/stocks.csv` |
| legacy interest, public securities rate | $bn | 33.12 to 41.64 | 33.98 to 45.78 | `derived/stocks.csv` |
| legacy interest, window from 2010 | $bn | 27.20 to 33.18 | 27.99 to 36.29 | `derived/stocks.csv` |
| legacy interest, window from 2015 | $bn | 17.66 to 21.91 | 18.29 to 24.14 | `derived/stocks.csv` |
| legacy interest, half borrowed | $bn | 15.07 to 18.94 | 15.47 to 20.82 | `derived/stocks.csv` |
| legacy interest, proportional benchmark | $bn | 38.77 to 46.50 | 38.59 to 46.32 | `derived/stocks.csv` |
| legacy interest, rule programme_income_ex_pandemic | $bn | 22.00 to 29.82 | 22.18 to 32.76 | `derived/stocks.csv` |
| legacy interest, rule whole_ratio | $bn | 15.26 to 23.27 | 15.52 to 26.11 | `derived/stocks.csv` |
| legacy interest, rule whole_flat | $bn | 18.34 to 27.87 | 18.73 to 31.27 | `derived/stocks.csv` |
| forward federal debt from the 2024 cash gap, 10 years | $bn | 422.6 to 642.1 | 431.6 to 720.5 | `derived/forward_path.csv` |
| forward federal debt from the 2024 cash gap, 20 years | $bn | 1,002.7 to 1,523.7 | 1,024.1 to 1,709.7 | `derived/forward_path.csv` |
| forward federal debt from the 2024 cash gap, 30 years | $bn | 1,799.3 to 2,734.1 | 1,837.6 to 3,067.9 | `derived/forward_path.csv` |
| forward debt if the whole cash gap were borrowed, 10 years | $tn | 2.99 to 3.38 | 3.27 to 3.78 | `derived/forward_path.csv` |
| back-cast cash net cost, programme, 2015-2024 | $tn | 2.47 to 2.75 | 2.65 to 3.02 | `derived/adopted_backcast_windows.csv` |
| back-cast cash net cost, programme, 2005-2024 | $tn | 4.21 to 4.72 | 4.56 to 5.23 | `derived/adopted_backcast_windows.csv` |
| back-cast cash net cost, programme_income, 2015-2024 | $tn | 2.71 to 2.97 | 2.90 to 3.25 | `derived/adopted_backcast_windows.csv` |
| back-cast cash net cost, programme_income, 2005-2024 | $tn | 4.86 to 5.33 | 5.21 to 5.85 | `derived/adopted_backcast_windows.csv` |
| back-cast cash net cost, whole_ratio, 2015-2024 | $tn | 2.24 to 2.54 | 2.43 to 2.82 | `derived/adopted_backcast_windows.csv` |
| back-cast cash net cost, whole_ratio, 2005-2024 | $tn | 3.86 to 4.37 | 4.21 to 4.89 | `derived/adopted_backcast_windows.csv` |
| per-correction federal part, tax_stack, central convention | $bn | 15.95 to 17.16 | 15.91 to 16.84 | `derived/corrections_federal_by_component_2024.csv` |
| per-correction federal part, tax_stack, central convention, displaced beneficiaries | $bn | — | -0.84 to -0.84 | `derived/corrections_federal_by_component_2024.csv` |
| per-correction federal part, benefit_keys, central convention | $bn | 1.71 to 1.59 | 1.71 to 1.59 | `derived/corrections_federal_by_component_2024.csv` |
| per-correction federal part, benefit_keys, central convention, displaced beneficiaries | $bn | — | -2.18 to -2.18 | `derived/corrections_federal_by_component_2024.csv` |
| per-correction federal part, medical_ethnicity_and_ltss, central convention | $bn | -15.24 to -15.23 | -15.24 to -15.23 | `derived/corrections_federal_by_component_2024.csv` |
| per-correction federal part, education_row6_and_school_price, central convention | $bn | 0.05 to 0.05 | 0.05 to 0.05 | `derived/corrections_federal_by_component_2024.csv` |
| per-correction federal part, lane_constants, central convention | $bn | -5.11 to -5.14 | -5.11 to -5.14 | `derived/corrections_federal_by_component_2024.csv` |
| per-correction federal part, finite_removal, central convention | $bn | -0.00 to -0.00 | -0.00 to -0.00 | `derived/corrections_federal_by_component_2024.csv` |
| per-correction federal part, consumption_key, central convention | $bn | -0.58 to -0.58 | -0.53 to -0.24 | `derived/corrections_federal_by_component_2024.csv` |
| per-correction federal part, enterprise_rekey, central convention | $bn | — | -0.01 to -0.01 | `derived/corrections_federal_by_component_2024.csv` |

The generator is `debt_table.py` in my scratch directory; it reads the 90c4b23 files and the working tree. The
proportional benchmark falls slightly: its roads and parks already responded at 1, and LIHEAP leaving the cash gap
outweighs the enterprise receipt. The per-correction rows split cash from displaced beneficiaries: rental
assistance's re-keys (in `tax_stack` and `benefit_keys`) now respond, in the displaced column.

Files: `debt_legacy.py`, `test_debt_legacy.py`, `RESULT.md`; 10 changed derived files (`adopted_backcast_windows.csv`,
`corrections_federal_by_component_2024.csv`, `corrections_federal_split_2024.csv`, `federal_gap_annual.csv`,
`federal_shares_by_year.csv`, `federal_split_2024.csv`, `federal_split_2024_lines.csv`, `forward_path.csv`,
`stocks.csv`, `summary.json`) and `derived/sept27_bridge_2024.csv` (new). `rates.csv`, `benefit_sensitivity.csv`
and the two earlier bridges are unchanged.

## Consumers and checks

| Consumer | Reads | Status |
|---|---|---|
| `debt_legacy_2026_09_23` | the back-cast's `backcast_annual.csv` and new `case_parts_annual.csv` | gated in the debt run |
| `winners_losers_2026_09_24` (W4, round 2) | debt `stocks.csv` and `summary.json` at a pinned commit | needs a `sept27` pin; `summary.json` `case.band` is the case band (capital included); the interest rows keep their schema |
| `sept24_propagation_2026_09_24/constant_choices.py` (W4) | a debt run's `federal_split_2024.csv` | it filters `profile == 'cbo_category_lag_non_school_full'`; for `sept27` the main profile is `long_run_non_school_full` (`summary.json` `case.main_profile`), and `fiscal_gap_bn` and `federal_bn` are the cash part |
| `sept26_propagation_2026_09_26/old_new_lanes.py` | rebuilds debt and distribution, requires its new column to equal the working tree | stops at that gate now (`--case sept26_schools --middle sept26`): the lanes' working tree holds `sept27`. It reproduces its CSV only against the files of its commits. Not edited (outside my directories) |
| `research/immigration-INDEX.md` line 127 and `sept24_propagation_2026_09_24/RESULT.md` line 6 | the sampling SE | both still say "That SE is a floor" / "This SE is a floor"; outside my directories, not edited. The parent note withdraws that reading |
| readers of `uncertainty_propagation_2026_09_22/derived/sept27/summary.json` | `se_independent_bn`, `se_cps_bn`, `ci95_union_bn` | these now carry the joint CPS block; the published method is `se_with_benefit_keys_bn` and `ci95_with_benefit_keys_union_bn`. Earlier cases' files are unchanged |

Commands, from the repository root:

```sh
node infra/immigration-fiscal/historical_backcast_2026_09_20/case_components.cjs
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/historical_backcast_2026_09_20/backcast.py
node infra/immigration-fiscal/distribution_weights_2026_09_23/case_ends.cjs
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/distribution_weights_2026_09_23/distribute.py
node infra/immigration-fiscal/uncertainty_propagation_2026_09_22/sept24_specs.cjs
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/uncertainty_propagation_2026_09_22/propagate.py
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/debt_legacy_2026_09_23/debt_legacy.py
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 -m pytest infra/immigration-fiscal/<lane>/ -q --import-mode=importlib
```
