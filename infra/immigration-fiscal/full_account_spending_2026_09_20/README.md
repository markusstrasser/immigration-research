# Complete current-spending allocation

**Verdict:** The national account is complete; ethnic incidence is conditional. Every scenario preserves **$10,061.458bn** of consolidated calendar-2024 BEA current expenditure. Four complete arms allocate every domestic dollar using declared survey/program proxies; the represented-only diagnostic leaves unmatched amounts unallocated. No marginal fiscal response is inferred.

Read [CONTRACT.md](CONTRACT.md) for the category assumptions sent to the parent before computing target-group spending. The preferred key is a declared working specification, not an estimated best-fitting incidence model.

| Complete scenario, target spending in $bn | Personal | Shared |
|---|---:|---:|
| Preferred keys, F per capita | 1,017.925 | 1,023.882 |
| Preferred keys, F fixed target zero | 732.314 | 738.272 |
| Alternative keys, F per capita | 1,070.982 | 1,068.815 |
| Alternative keys, F fixed target zero | 785.371 | 783.205 |

All complete arms keep $400.813bn explicitly foreign and $96.097bn in the modeled outside-CPS domestic allocation. The represented-only diagnostic assigns $173.818bn personal / $181.204bn shared to the target and leaves $7,035.784bn / $7,001.681bn unallocated. Its small covered total is not a claim that the unallocated services have zero cost.

## Reproduce

From a checkout containing this lane, with the existing canonical input files already built:

```sh
OPENBLAS_NUM_THREADS=1 UV_CACHE_DIR=/private/tmp/immigration-uv-cache uv run --no-project \
  --with numpy --with pandas --with openpyxl python3 \
  infra/immigration-fiscal/full_account_spending_2026_09_20/builder.py \
  --source-root /Users/alien/Projects/immigration-research
UV_CACHE_DIR=/private/tmp/immigration-uv-cache uv run --no-project \
  --with numpy --with pandas --with openpyxl --with pytest python3 -m pytest -q \
  infra/immigration-fiscal/full_account_spending_2026_09_20/test_builder.py
```

Dependencies: Python3.11+, numpy, pandas, openpyxl, pytest for tests. `--bea` selects the pinned workbook; `--out` selects output location. The builder reads existing CPS2025, MEPS2024, measured-school operating results and population inputs. It writes only this lane. Raw/source-derived data remain ignored. A failed build invalidates the prior successful audit receipt.

## Boundary and sources

[BEA Section3 workbook](https://apps.bea.gov/national/Release/XLS/Survey/Section3All_xls.xlsx), SHA256 `69b5c7aefb38675324887ce31d6feb4fcde7c903ab952db7328da0813096615e`:

- Table3.17 lines2–10: current consumption by function, total $3,991.840bn (published rounded component arithmetic recorded).
- Table3.12: domestic benefits by program, $4,455.695bn; foreign/territory benefits $34.323bn. The domestic program leaves are disjoint; SSI and selected state/federal programs are combined where CPS cannot separate them.
- Table3.1: other foreign current transfers $87.735bn; domestic interest $1,118.870bn; foreign interest $278.755bn.
- Table3.13: subsidies $94.239bn, separated into housing, agriculture, transport and other.

The account has 42 categories including explicit source rounding. Table3.17 footnote2 says intergovernmental grants disappear in government-sector consolidation. Consumption includes depreciation and is net of sales. Gross investment, capital transfers and gross federal grants are not added. Program payments that purchase care and government-produced health services are separate NIPA categories; identical incidence proxies do not imply duplicate dollars. [Methodological source: [BEA NIPA Handbook](https://www.bea.gov/resources/methodologies/nipa-handbook), workbook labels and footnotes copied to `audit.json`.]

All leaf cells and table metadata are exported. Different sheets carry their own publication date; the workbook file creation date is August25,2026. The source is pinned rather than silently replaced by a later release. Census and MEPS URLs, hashes and existing-local reuse are in `SOURCE_PINS.json`.

## Population, outside scope and allocation

The target remains **40,896,574.152351856** observed CPS people. Its complement within CPS is **295,831,228.8476619**. The resident control is **340,110,988**; the CPS civilian total is **336,727,803.00001377**. The difference **3,383,184.9999862313** is held outside the CPS frame and inside the domestic `other_bn` aggregate. No extra people are imputed to the target.

Complete arms assign `CPS civilian / resident = 0.9900527030312051` of each domestic pool to CPS household proxies and the rest to `outside_household_bn`. This is a common equal-cost scope assumption, not an observation of institutional or military costs; the July2024 versus March2025 population timing also differs. Program-specific institutional composition remains unidentified. Identified BEA foreign/territory benefits and foreign flows stay in `external_bn`. Unknown represented-only residuals stay `unallocated_bn`, never outside-household by relabeling.

Personal versus shared allocation changes who receives CPS cash/program amounts within an SPM resource unit while preserving unweighted unit dollars; original receiver weights are retained. Health means are the existing personal age/birth transport in both cases. `national_key_total` is the denominator of each incidence ratio; `national_positive_key_persons` counts people assigned a positive key, not necessarily actual recipients. A positive MEPS donor mean applies to everyone in its matching cell. School/postsecondary key counts are unavailable from the aggregate export and explicitly missing.

## Sensitivity and outputs

`allocations.csv` uses the parent integration schema: `scenario_id,allocation,category,national_bn,target_bn,other_bn,external_bn,unallocated_bn,allocation_key,target_key_share,response_class`. Additional columns distinguish household/outside-household allocations, pool fraction and proxy scope. `target_key_share` is conditional within CPS; `target_share_national` includes the pool fraction.

Scenario IDs:

- `complete_preferred_F_per_capita` and `complete_preferred_F_fixed` use the preferred program keys.
- `complete_alternative_keys_F_per_capita` and `complete_alternative_keys_F_fixed` use the first listed alternate key for each applicable category. All F categories retain the explicit population key before the F convention is applied.
- `represented_only_F_per_capita` caps matching benefit categories at their transported/reported CPS dollars and leaves other categories unallocated. It is intentionally incomplete attribution, with complete dollar conservation; not a causal lower bound.

Here F covers defense, general public services and domestic interest. `F_fixed` sends target attribution to zero and transfers those dollars to other households. It does not claim spending would fall or taxes would disappear when a group is removed. Parent-owned response coefficients must be applied independently. Explicit foreign interest stays external under both conventions; that is an incidence boundary assumption, not evidence its fiscal financing burden belongs abroad.

`category_proxy_alternatives.csv` supplies every declared category/key choice separately, not only the bundled scenarios. `incidence_keys.csv` supplies denominator, unit, scope and positive-key exposure counts. `categories.csv` is the disjoint national partition. `scenario_totals.csv` is only the spending side. `audit.json` hashes all generators, raw and upstream derived inputs, contract and output files.

Material limitations: aggregate education consumption uses operating-school plus postsecondary model dollars as its mixture, not a BEA K–12/higher split; the school-only and age5–24 alternatives expose this. Federal refundable credits include programs beyond CPS EITC/ACTC; adult-age allocation is an explicit alternative. WIC is a proxy for the broader state welfare residual; some federal benefits go to nonprofits. Neither administrative origin incidence nor all program recipients are observed. There is no defensible probability distribution for these alternatives and no combined confidence interval is claimed.

Eight tests pass, checking exhaustive national and category accounting, prohibited grant/capital leafs, foreign attribution, fixed-cost redistribution, residual versus institutional classification, canonical origin domains, SPM sharing, primary and upstream-school source drift, and output hashes. No core fiscal model or shared register/index was edited.
