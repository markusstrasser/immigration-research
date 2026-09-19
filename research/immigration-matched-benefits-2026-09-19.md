# Matched population: skills, investment and fiscal benefit calculations

Date:2026-09-19. Calculation index, not essay text. [FRAMING-SENSITIVE]

**Account version:** Credit and threshold tables use the pinned $217–239bn
release. The later [observed2024 finance refresh](immigration-macro-reconciliation-2026-09-19.md)
gives $234–256bn and raises credited C from $34.550bn to $35.188bn. Production
gains are unchanged; C-replacement increments fall by $0.638bn against that
refresh. The old thresholds remain versioned, not current welfare break-evens.

**Verdict:** The same observed Mexican-origin population produces positive
skill-complementarity gains in the calibrated long-run cases. Those gains are
not large enough within this model to match its attributed fiscal deficit.
Capital-tax attribution can move the fiscal calculation by much more, but the
tax counterfactual, ownership and existing credits determine whether that is
a net benefit to the chosen beneficiaries. It cannot be appended as free income.

## Population, ledger and identification

[SURVEY / MODEL] The canonical CPS ASEC2025 observed union contains40.896574m
civilian-household residents: Mexico-born, Mexican second generation, and
self-identifying Mexican third-plus, all ages and education. This is not a
complete genealogical population. Beneficiaries are residents outside that
union, including other immigrants. Monetary flows use2024 dollars. The model
compares stationary economies with and without the union's labor; it does not
identify the historical effect of immigration, a current admission decision,
or the cost of removal. [SOURCE: canonical CPS data and
[generator](../infra/immigration-fiscal/matched_benefits_2026_09_19/README.md).]

[SURVEY ESTIMATE] The union supplies$1,049.584bn positive annual earnings.
Using the source's education split, HS-or-less workers supply$482.525bn and
some-college-plus workers$567.059bn. These represent17.830% and5.752% of their
respective national earnings pools. Positive earners number11.707m and8.825m.
Workers' attained education proxies skill; neither earnings nor education is
assigned to children as a fiscal burden or a productive benefit. Both wage-only
earnings and a below-BA/BA-plus alternative are exported. [SOURCE:
`derived/skill_composition.csv`; point plus160 CPS replicate weights.]

## Production and investment results

[MODEL OUTPUT] Two competitive CES skill inputs are nested under Cobb-Douglas
capital. Within each education cell, target and outside workers are perfect
substitutes. Source-centered case: elasticity2, labor share.65, fixed hours.
The cash normalization sets implied output to surveyed positive earnings/.65;
the GDP normalization scales earnings shares to officialGDP$29,298bn. That
transport to total compensation is an additional assumption, not missing
survey earnings automatically recovered. All capital belongs initially to
outside-union residents.

| Capital response | Cash normalization, gross outside income gain | GDP normalization, gross outside income gain |
|---|---:|---:|
| Fixed | $25.01bn/year | $37.91bn/year |
| Intermediate | $12.77bn/year | $19.35bn/year |
| Fully adjusted | $8.79bn/year | $13.32bn/year |

[MODEL OUTPUT] Across elasticity1.5/2/2.5, labor share.60/.65/.70 and both
earnings proxies, with the source's HS split and fixed hours, fully adjusted
capital gives$6.37–11.77bn cash or$9.34–19.21bn GDP. Fixed-capital cases give
$19.49–30.45bn cash or$33.30–42.59bn GDP. These are scenarios, not empirical
bounds on all benefits. The homogeneous$13–26bn calculation is not a ceiling.

[MODEL OUTPUT] The small aggregate conceals substantial transfers. In the
source-centered cash/full-adjustment case, outside HS-or-less workers lose
$123.85bn while some-college-plus workers gain$132.64bn. Net capital income
gain is zero after subtracting the alternative return to released capital.
The corresponding GDP values are−$187.69bn and+$201.02bn. These large wage
changes are calibrated stock counterfactuals, not observed effects.

[MODEL OUTPUT] Allowing outside workers' hours to respond with elasticity.33
raises the cash/full-adjustment baseline gross income gain to$10.05bn; private
money-metric WTP plus current receipts is$10.10bn after labor disutility.
GDP values are$15.24bn/$15.31bn. With fixed capital, endogenous hours can make
the net result negative: labor withdrawal and forgone tax revenue matter.
The full exported grid retains these disconfirming cases. This is a simple
constant-tax, quasilinear labor-supply sensitivity, not a household microsimulation.

[DERIVATION] The model pays the opportunity cost of capital. It does not treat
the extra domestic capital income as a free benefit: capital released in the
absent-target economy earns the initial rental rate elsewhere. Capital
adjustment0/.5/1 denotes comparative statics, not adjustment timing. An
independent numerical-factor-price oracle reproduces the surplus; full
adjustment returns zero net capital gain exactly. [SOURCE: generator/tests;
[NAS chapter4, pp169–175](https://www.nationalacademies.org/read/23550/chapter/8).]

## Induced receipts, their private offset and existing credits

[SOURCE / TRANSPORT] Colas–Sachs's author manuscript uses2017 tax components.
For HS-or-less/some-college-plus, current federal/state/payroll marginal rates
sum to38.4%/42.6%. The reported30.3%/36.6% totals instead include transfer
phaseouts and deduct future Social Security accrual; these are not annual
receipt rates. This run exports the three objects separately. Source-supported
elasticity scenarios are1.5–2.5. The published article exists, but the full text
read here is the dated2022 author manuscript, not a silently relabeled2024PDF.
[SOURCE: [author manuscript, §§3–4 and Table1](https://www.dominiksachs.com/downloads/fiscal_low_skilled_immigration_final.pdf);
[published record](https://doi.org/10.1257/pol.20220176).]

[SOURCE / TRANSPORT] Clemens's capital-tax adjustment motivates counting
capital receipts. Its2011–2013 macro rate24.6% excludes sales taxes; this run
uses that rate as sensitivity. It is not an estimated2024 marginal tax rate.
[SOURCE: [Clemens, §3.1](https://docs.iza.org/dp15592.pdf).]

[MODEL OUTPUT] Full-adjustment/source-centered cases yield:

| Share of alternative capital taxes retained in the US | Current induced receipts, cash | Current induced receipts, GDP |
|---|---:|---:|
| 100% | $8.95bn | $13.56bn |
| 50% | $79.04bn | $119.79bn |
| 0% | $149.14bn | $226.03bn |

The retention rate is unestimated. The last row assumes alternative investment
generates no US tax revenue while still earning a return. It is not an
established fiscal benefit. Additional transfer costs from wage shifts lower
the baseline current budget effect by$3.38bn cash/$5.12bn GDP. Discounted
future pension adjustments are shown separately rather than mixed into2024.

[ACCOUNTING] Under the main ownership assumption, the apparently large
$149.14bn cash receipt gain is accompanied by roughly−$140.35bn private
after-tax WTP; their sum remains$8.79bn. The GDP counterpart is about
−$212.71bn private plus$226.03bn fiscal=$13.32bn. Taxes taken from included
capital owners are a transfer inside this beneficiary account. The code
enforces the identity rather than adding taxes to already-gross income.

[MODEL SENSITIVITY] `ownership_sensitivity.csv` also assigns0/50/100% of
capital ownership to people excluded from the beneficiary population (foreign
or target-group owners). With no alternative-US-tax retention, private WTP
plus receipts is then$8.79/$78.89/$148.98bn cash and
$13.32/$119.56/$225.79bn GDP. This additionally values every fiscal dollar
for included residents. These ownership and fiscal-recycling assumptions
are not measured shares. Counting private gains for the excluded owners too
restores the original transfer accounting.

[EXISTING LEDGER] The union already receives$34.550bn corporate-tax creditC
and$24.970bn owner-property credit under both fiscal allocations. Sales
credit$25.768bn and excise/selective-salesX$37.722bn are separately recorded;
they are not treated as known overlap with the capital rate excluding sales.
The aggregate tax field also includes taxes on residents' capital income,
but these are not separated from labor taxes in the stored annual account.
[SOURCE: canonical `age_profile_components.csv`; reconstructed balances match
both fiscal allocations; new `existing_tax_credits.csv`.]

[REPLACEMENT ARITHMETIC] ReplacingC with the model's capital-revenue
attribution, while retaining its induced labor-tax change, leaves the
no-retention candidate receipt increment$114.59bn cash/$191.48bn GDP.
Also removing the entire owner-property credit yields$89.62bn/$166.51bn.
Removing all owner-property is a scope stress test because owner-occupied
capital is not the production model's capital base; it is not a proved exact
overlap. Personal capital-income-tax overlap remains unidentified. These
figures are therefore replacement arithmetic, not corrections permitted for
direct addition. Every exported row sets `direct_addition_permitted=False`.
The alternative100%-retention cases can reduce attributed receipts after
replacement; all outcomes are exported.

## What would change the conclusion

[MAGNITUDE CHECK] Within the two-skill, full-adjustment/fixed-hours model alone,
matching the$217–239bn assigned deficit in gross-income magnitude would require
an elasticity about.09–.14 in the PEARNVAL/HS-split cases, far below the
source-centered1.5–2.5 scenarios. This is not a welfare break-even and does
not restrict omitted mechanisms. [SOURCE: `magnitude_thresholds.csv`.]

[DISCONFIRMATION] Firm evidence shows that low-skill immigrant labor can
complement native labor and induce investment. Clemens–Lewis's2024 revision
uses472 firms in the2021/2022H-2B lotteries. Its firm-level foreign/native
substitution estimates are0.8–2.2. Those parameters concern selected employers
and visa workers, not education groups or an all-generation ethnic union.
They therefore cannot be inserted as an ethnic CES elasticity. The result
supports taking adjustment seriously; it does not identify a national stock
multiplier. [SOURCE: [full paper, introduction and design](https://www.aeaweb.org/conference/2025/program/paper/F28EzA5h).]

[GAPS / DEFEATERS] Empirically estimated outside-group wage responses, 2024
effective marginal taxes, ownership of marginal capital and its alternative
tax location could replace the transported assumptions. Innovation, trade,
housing, occupation changes, extensive labor participation, endogenous
education and policy transition costs remain outside the model. The old
services-price scenarios have different populations and overlap with factor
income, so no service-price gains are added here. These calculations do not
produce a complete net cost to America.

[VERIFICATION]1,296 cases use161 joint CPS weights;18 additional baseline
ownership cases and24 replacement rows are exported. Six tests include
independent numerical factor derivatives and a Newton equilibrium oracle,
zero and homogeneous limits, small-shock curvature, capital opportunity cost,
the source's marginal tax formula, tax/private conservation and invalid-input
rejection. Sampling intervals
exclude parameter and model uncertainty. LLM interpretation is subject to
the [instrument caveat](../notes/llm-bias-caveat.md).
