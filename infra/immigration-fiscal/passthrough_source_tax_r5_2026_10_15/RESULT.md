**Verdict:** Item19 is delivered as an explicit-arm post-engine component, with
no identified central correction. A narrow, frozen-2022-income diagnostic changes
v8 by **−$5.022526137bn low / −$1.193227946bn high** under full foreign-tax-credit
replacement, historical25% residual-capital calibration for S/P, all partnership
profits ultimately taxable to individuals, and the high end's tangible-equity
normal-return proxy. Replacing the ownership exposure with the national
immediate-individual allocation proxy gives **−$3.368256915 / −$0.673876887bn**.
Identical domestic replacement gives **zero**, so the first pair is not an
identified loss of US receipts. W09's corporate-only joint arm is below the
reviewer's estimate: **+$3.295299123 / +$1.219260676bn** on the frozen union and
v6 descendants; a v8 completion/coverage profile extension gives
**+$3.403873020 / +$1.259433017bn**. [CALCULATION: `derived/item.json`,
`derived/w09.json`; INFERENCE: conditional modeling, no adoption]

## Measurement and frame

Perspective: net cost to other US residents, with the departing lineage's job
capital responding under item6's premise. Negative numbers below lower cost.
These are source-table measurements combined with conditional attribution,
not observed immigration effects. This LLM-assisted politically sensitive
analysis is governed by the source/assumption distinctions below. [FRAMING-SENSITIVE]

| Measured source | S corporations | Partnerships | Nonfarm sole proprietors |
|---|---:|---:|---:|
| TY2022 ordinary business profit, $bn | 763.268999 | 847.619582 | 410.664065 |
| Narrow direct-operating residual, $bn | 503.340901 | 629.265801 | 410.664065 |
| TY2023 income-weighted AGI-bin tax/AGI allocation |21.809794%|22.163373%|11.201323%|

[SOURCE: IRS2022 [S Tables6.1/7](https://www.irs.gov/pub/irs-soi/22co61ccr.xlsx),
[partnership Table1](https://www.irs.gov/pub/irs-soi/22pa01.xlsx),
[Schedule C Table2](https://www.irs.gov/pub/irs-soi/22sp02is.xls), and
IRS2023 [Table1.2](https://www.irs.gov/pub/irs-soi/23in12ms.xls) /
[Table1.4](https://www.irs.gov/pub/irs-soi/23in14ar.xls); DATA: `inputs/`]

The industry interface contains58 form-sector records and33 source closure gates.
The S residual removes all nonbusiness receipts because upstream ordinary
partnership income and gains cannot be isolated. This removes valid operating
receipts too and subtracts tax-exempt interest a second time; it is deliberately
a sizing arm, not a proved lower bound. Partnership upstream ordinary net income
is removed before applying capital shares. Rental/portfolio income is not added.
Officer compensation and guaranteed payments are already deducted, so they are
not deducted again. Schedule C owner labor remains in profits. Full definitions,
alternative raw bases and suppressed cells are preserved. [DATA:
`inputs/income_sectors.json`; SOURCE/limitations: `income-evidence.md`]

The K1/SUSB machinery supplies legal-form payroll probabilities by broad sector
and matched enterprise size. Fine wage cells are reaggregated on the same
row4/39.712493M frame and wage-fill-in rules as item6; the frozen replay reproduces
every source output. Manufacturing is pooled, partnership61+81 is pooled using
payroll sufficient statistics, and no equal split of IRS profits is invented.
SUSB missing size cells use one explicitly `[DEGRADED]` all-size profile; no
unknown form probability becomes zero. Crop/animal production and unclassified
source sectors are withheld; mining's capital response stays0; the transport
sector's rail/nonrail scope remains conditional. Nonemployer profits cannot be
identified separately from employer profits in these tables. Thus applying an
employee-payroll key to all form profits is another exposure assumption.
[DATA: `derived/job_keys.json`, `derived/legal_profiles.json`,
`derived/income_key_exposures.csv`, `derived/item.json:source_scope_skips`]

Item10 is measured on231 exact observed person IDs,517435.75719317 people,80 wage
earners. Corrected wages are12.258694044bn,9.084941675bn in supported private
industries; excluded crop/government wages close the difference. Their own
industry/enterprise-size keys add−0.046110425bn to the all-individual,25%-capital
low diagnostic. No population scalar substitutes for their keys. The old-key
SDR uncertainty is conditional; completion's replicate uncertainty is not
measured. Item12's1.960414M missing-person increment for this new tax is withheld
pending own age/sex/source keys; it is not a measured zero. [CALCULATION:
`population_keys.py`; DATA: `derived/job_keys.json:completion`]

## Item19 arms

All rows below hold the source industry amounts in nominal2022 dollars without
growth, use2024 job shares and2023 allocated owner rates, and retain v8's original
four endpoint costs. They include item10's observed jobs and the v6 added-age
mixture. They do not measure item12's new source-tax increment. Default diagnostic
rules are25% S/P residual capital; Schedule C withheld; all partnership ordinary
profits hypothetically ultimately individual-taxable; owners outside already
counted personal-tax/removal losses; all modeled operating income US-source;
no additional national state-source rate. None is an estimated probability.
[CALCULATION: `measure.py:scenarios`; INFERENCE: transport and attribution]

Changes in cost,$bn low/high; **each pair applies to both set and cash**:

| Arm | Low | High |
|---|---:|---:|
| Foreign replacement, full FTC, all residual capital normal |−5.022526137|−5.022526137|
| Identical domestic replacement |0|0|
| Foreign replacement, zero FTC, same pre-tax income |0|0|
| Foreign replacement, half FTC |−2.511263068|−2.511263068|
| Half domestic, half foreign with full FTC |−2.511263068|−2.511263068|
| Foreign full FTC, high-end normal component0 |−5.022526137|0|
| Foreign full FTC, all S/P/C profit capital |−24.239630253|−24.239630253|
| Foreign full FTC, add all Schedule C profit as capital |−9.172051843|−9.172051843|
| Foreign full FTC, national immediate-individual P allocation |−3.368256915|−3.368256915|
| Foreign full FTC, signed-net owner-rate allocation |−5.149302738|−5.149302738|
| Foreign full FTC, TY2022 owner rates |−5.042169781|−5.042169781|
| Foreign full FTC, one extra state-source percentage point |−5.251201918|−5.251201918|
| Foreign full FTC, half outside already-counted owner taxes |−2.511263068|−2.511263068|
| CFC replacement, zero foreign tax, no QBAI allowance |−2.607694253|−2.607694253|
| CFC replacement,10% foreign tax, no QBAI allowance |−4.447566164|−4.447566164|
| CFC replacement, inclusion0 because QBAI covers normal return |−5.022526137|−5.022526137|
| Foreign full FTC, tangible-equity normal-return proxy |−5.022526137|−1.193227946|
| Same proxy, national immediate-individual P allocation |−3.368256915|−0.673876887|

[CALCULATION: `derived/arms.csv`; source-receipt and replacement-receipt parts
separately close in `derived/item.json`]

The tangible-normal diagnostic would put set at360.769404119 /454.788556643bn,
cash at276.730037539 /370.749190063bn. Its changes per member of v8's full
45,230,062.30075857-person denominator are−$111.04 /−$26.38; the
individual-allocation version is−$74.47 /−$14.90. All18 arms' exact endpoints
and per-member figures are in `derived/arms.csv`. These are component additions
to v8, not a new adopted case or a complete missing-population correction.
[CALCULATION: `derived/evaluations.json`, `derived/arms.csv`]

## Replacement, owner labor and the high end

The direct-owner identity is source receipts minus replacement US receipts:
`I*tau*(1-d)*(1-q*(1-c))`, where d is the domestic share,c the usable foreign
credit fraction of tentative US tax,q replacement/source pre-tax income. Thus
identical domestic replacement cancels; full FTC foreign replacement can leave
the whole source tax lost. The helper also solves equal after-tax return under
simple proportional foreign/US taxes. The named same-income FTC arms can
preserve after-tax return when the foreign rate does not exceed the US rate;
full FTC at a higher foreign rate requires a different q. No split or credit
utilization distribution is observed here. Signed sector losses retain an
explicit proportional usable-tax-shield convention; actual carryovers are not
modeled. [SOURCE: pinned2024 IRS Publication514; CALCULATION:
`owner_tax_sources.py`, `test_item.py`]

The75% owner-labor calibration is from historical top S/P owners, not Schedule C
or all2024 owners. Its25% residual includes rents; it is **not** a normal-return
share. The proposed high-end diagnostic instead prices the moving normal part
as `min(max(.25*direct_profit,0), .0295*eligible_book_equity)`, where
`eligible_book_equity=max(0,min(net_equity-other_investments,net_PPE+land))`.
The2.95% is the observed2022 annual nominal10-year Treasury yield, matched to
the frozen2022 income/assets. This excludes tiered financial holdings from the
normal-stock proxy rather than copying C-corporate0.37. Missing stock is
withheld. Book valuations, expensing, intangibles, omitted financial assets,
small-filer balance sheets, year-end timing and imperfect debt attribution mean
it is a conditional tangible-asset diagnostic, not an estimated normal-profit
fraction or a bound. The0/all-residual-normal arms expose that gap. [SOURCE:
[Smith et al., Table IV](https://eml.berkeley.edu/~yagan/Capitalists.pdf),
[Federal Reserve H.15](https://www.federalreserve.gov/datadownload/Preview.aspx?pi=400&preview=H15%2FH15%2FRIFLGFCY10_N.A&rel=H15),
IRS balance sheets; DATA: `inputs/owner_normal_yield.json`, `inputs/income_sectors.json`]

The CFC mirror subtracts additional current US tax on replacement capital rather
than counting item9's foreign-source removal twice: full section78 gross-up,
2024 section25050% deduction and section960(d)80% credit, constrained by the
FTC limit. These are current-inclusion diagnostics at the declared replacement
income, not complete equal-after-tax owner returns: future distributions,
962 elections, QBAI, losses, baskets, ownership routes and destination rates
remain unmeasured. Tests distinguish the full gross-up from the80% credit.
[SOURCE: pinned2024 Forms8992/8993,2023 instructions1118 and2022 Form1118;
`owner-evidence.md`; CALCULATION: `owner_tax_sources.py`]

A national state-source rate is unidentified. One extra percentage point costs
−0.228675781bn in the full-FTC diagnostic; this is a unit sensitivity, not an
estimate. California's elective9.3% PTE payment comes with an owner credit and
cannot simply be added to existing state liability or applied nationally.
[SOURCE: pinned2024 FTB3804 instructions and IRS Notice2020-75;
CALCULATION: `derived/arms.csv`; GAP: source-state/owner/replacement nexus]

## Interactions and packaging

- **Item6:** same jobs and capital premise. Item19 adds only the owner-level
  source/residence-tax difference; property/production lines remain untouched.
  Membership overlap is unresolved: source taxes already lost through group
  owners' personal returns or item11 must be excluded. The outside-owner arm
  makes that restriction explicit rather than claiming all owners are others.
- **Item9:** corporate foreign-source tax remains removed. Direct ordinary
  residuals remove known/unseparated upstream receipts, but geographic source
  and ultimate ownership remain unidentified. The national24.93% immediate-owner
  proxy avoids automatically taxing all corporate/exempt-owned P income again;
  it cannot trace ultimate owners or identify direct-profit ownership.
- **Item10:** measured own observed keys included once, as described above.
- **Item11:** existing stayer amounts held fixed. No owner-tax overlap or
  replacement-income effect is silently inserted into stayer personal taxes.
- **Item12:** old v8 coverage remains in baseline; new pass-through coverage
  prices are explicitly withheld. Do not adopt the displayed exposure as a
  full-lineage source-tax correction without resolving this.
- **W09:** separate corporate-only item6 arm, not added to item19. Its exact
  frozen change is+$3.295299123 /+$1.219260676bn. Transporting G3's corporate ratio
  to item10 adds−0.003969308 /−0.001468644bn; applying generation ratios to item12
  adds+0.112543204 /+0.041640986bn. This gives+$3.403873020 /+$1.259433017bn,
  or+$75.26 /+$27.85 per full-lineage member, in both sets. These population
  extensions are labeled profile proxies and remain distinct from exact keys.
- **Other round5 items:** source profits, allocated owner rates and job keys
  held fixed. No claimed full joint round5 result; any changed source base,
  membership or outside-owner treatment requires rebuilding the item.

[CALCULATION: `derived/item.json:interactions`, `derived/w09.json`;
INFERENCE/GAP: overlap and counterfactual ownership]

`item.cjs.build(ctx,arm,which)` returns a registry-shaped post-engine amount,
with signed source/replacement parts by line and generation. Missing arm is a
hard error. `evaluate.cjs` verifies the component at live v8 specifications16/11,
both methods and both sets; the parent still must wire its post-engine amount
once into v9. No case adoption, merge, stage or commit is performed.
[CALCULATION: `item.cjs`, `evaluate.cjs`]

## Validation and log

2026-10-15 UTC: v8 unchanged passes365.791930255485 /455.981784588979bn set and
281.752563676073 /371.942418009567bn cash. Frozen job-key positive controls
reproduce all source bytes; row4/source-weight gates pass. The code reviewer
found two deterministic integration failures; both were reproduced, repaired
and added to `failure-catalog.md` with regression checks. Dates and final
per-command wall time/peak RSS are recorded from `date`, `perf_counter` and
`getrusage` in ignored `_cache/run_log.json` / `_cache/runtime.json`. Final
pytest/rerun receipts are appended after execution. [CALCULATION: `run.py`]

Final receipt,2026-10-15T02:43:13Z: **22 pytest tests pass**;
`rerun_lane.py` reports **IDENTICAL:31/31**, **exit0**, with every new script
covered and no unrun exemption. The final full rebuild takes33.532792375 seconds;
peak child RSS1,934,688,256 bytes, below2.5GB per process. The initial extra
coverage declaration failure and its fix are retained in `failure-catalog.md`.
No upstream edits or Git writes. [CALCULATION: final command output;
`_cache/run_log.json`, `_cache/runtime.json`]
