claude-opus-5[1m]

**Verdict:** On the complete account, one Mexico-born arrival aged 25 who stays unauthorized, plus the 2.05 descendants their lineage generates inside 100 years, runs a fiscal balance of **−$1.20M** undiscounted over that century, against **+$97k** for one third-plus non-Hispanic white of the same age and the 2.15 descendants of that lineage. The gap is **−$1.30M**, or **−$13.0k per year**; at a 3% real discount it is **−$515k**. The founder's own lifetime accounts for only **−$555k** of the gap, so **the descendants carry 57% of it**, and the single most expensive member of the lineage is not the immigrant but the US-born second generation (−$562k, −$664k per person), because that person lives an entire life inside the window while the founder's childhood was paid for abroad. **No tested arm brings the lineage gap inside the founder's own lifetime gap**; across all 115 arms in the grid and the sensitivity set the ratio never falls below 1.16, and it is 2.3× centrally. **The arm that moves the gap most is the attribution rule** (−$0.85M to −$2.71M), followed by real growth and fertility; legalising the founder moves it by 1.9% and correcting for ethnic attrition by 0.4%. The absolute level is account-dependent and the gap is not: switching from the complete to the partial account moves the Mexican lineage by $1.21M but the gap by only $0.23M. [CALCULATION]

Model self-report: **claude-opus-5[1m]** (Opus 5, 1M context).

Provenance tags: [SOURCE] primary or upstream-lane data · [CALCULATION] arithmetic in this lane · [INFERENCE] my reading · [ASSUMPTION] a stated parameter choice · [UNVERIFIED] not externally checked.

---

## Validation

**Hard oracle, PASS.** This lane's stream machinery reproduces all 768 rows of
`ledger_absolute_2026_09_17/derived/lifetime/period_profiles.csv` with a maximum
absolute difference of **5.8e-11 dollars**. That covers both allocations, both
accounts, all six groups, both mortality arms, both horizons, both start ages and
four discount rates, so the age vector, the NVSS `Lx / lx[start]` exposure weighting
and the interval-start discounting are identical to the lane that produced the
profiles. [DATA: `derived/oracle_period_profiles.csv`]

**Account identity, PASS.** `shared`/`partial` in the absolute lane equals the
brief's `all_age_shared` scenario in `all_age_ledger_2026_09_17` to 9.1e-12 dollars
per person-year across all four Mexican-origin groups. [DATA]

**Byte-identical re-run, PASS.** `derived/` copied, `lineage.py` re-run over the
existing inputs, `diff -rq` against the copy returns nothing, rc 0. [DATA:
`logs/rerun.log`]

**Soft triangulation, PARTIAL.** The pronatal lane's 24 stored lifetime balances are
located at `shared`/`partial` but agree with my recomputation only to within 0.1% to
5.4% (largest absolute gap $9,099 on `all_native` at 0%). The residual is a survival
or top-age convention difference between two in-repo lifetime constructions that I did
not resolve. It does not touch the numbers above, which are anchored on the hashed
`period_profiles` oracle. [DATA: `derived/oracle_pronatal.csv`] [UNVERIFIED]

---

## What the scratch script had wrong

The brief said to copy the scratch script in and check every path and constant. Six
defects were found; all six are repaired, and the original is kept verbatim at
`scratch_lineage_cost_ORIGINAL.py` as the audit trail.

1. **The white reference profile was not in the repo.** The scratch hard-coded
   `WHITE_BAND = [6244, 7000, 10447, 9275, 9601, 8725, -18246, -24754]`, attributed to
   "the generation memo table". It matches no age profile in any lane: the nearest is
   `shared`/`partial`, off by up to **$6,057 per person-year**. The headline comparator
   was therefore unsourced. This lane reads the white profile from
   `ledger_absolute_2026_09_17/derived/age_profiles.csv` like every other group.
   [CALCULATION]
2. **The complete-account add-on was applied flat across ages.** The scratch took one
   per-person number from `waterfall.csv` (Mexico-born −$6,472) and added it at every
   age. The true by-age add-on ranges **−$5,613 to −$10,781** for the Mexico-born and
   **−$3,504 to −$13,928** for whites — it is concentrated in old age, and flattening
   it moves dollars out of the years survival weighting discounts least. This lane uses
   the `expanded` account profile directly, which is the complete account by age.
   [DATA: `derived/audit.json` → `checks`]
3. **Survival used `lx`, not `Lx`.** `lx` is survivors at the start of the interval;
   `Lx` is person-years lived within it. The producing lane uses `Lx`; using `lx`
   overstates exposure at every age. Corrected.
4. **"Full attribution" was a demographic error, not an attribution choice.**
   Multiplying the lineage by TFR per person per generation gives each person their own
   full complement of children while their partner's lineage claims the same children.
   The scratch's "half" arm is in fact the demographically neutral TFR/2 rule. The
   three rules are now named for what they do, and the neutral one is central. This is
   the largest lever in the whole exercise.
5. **Crime was priced on the wrong denominator and the wrong ages.** The scratch applied
   a per-capita all-ages rate over ages 18-64, and mixed a Texas arrest-charge status
   rate for the founder with a national ACS institutional-stock rate per adult 25-64 for
   descendants. Crime is now priced per adult 25-64 over ages 25-64, in three
   internally consistent routes, with the founder's status route as a named sensitivity.
6. **The white TFR constant was 1.55 with no source.** The published figure is **1.5325**
   (1,532.5 per 1,000, NH white, single race, 2023). [SOURCE: NVSR Vol. 74 No. 1,
   "Births: Final Data for 2023", Table 2, quoted and gate-checked in
   `demo_momentum_2026_09_16/RESULT.md` gate (b)]

Two further points the brief flagged. The brief names
`native_fertility_2026_09_16/derived/` as a fertility input; that lane has no `derived/`
directory and is a metro panel on native fertility crowd-out, not a measurement of
fertility by generation. The generation-specific rates come from
`demo_momentum_2026_09_16` instead, which is the lane that measures them. And the
brief's main account (`all_age_shared`) is the partial account; the absolute lane's own
primary for lifetime work is `personal`/`expanded`, which is the complete account by
age. Both are in `lineage_table.csv` and the difference is reported below.

---

## Parameters, and where each came from

| Parameter | Value | Source |
|---|---|---|
| Founder age at arrival | 25 | brief |
| Horizon | 100 calendar years | brief |
| Generation length, central | 29 | see below |
| NH white TFR | 1.5325 | [SOURCE: NVSR 74-01 Table 2, 2023] |
| Mexico-born TFR, low arm | 1.6935 | [CALCULATION] age-std own-children ratio 0.2514/0.2275 × 1.5325 |
| Second-generation TFR, low arm | 1.2940 | [CALCULATION] ratio 0.1921/0.2275 × 1.5325 |
| Third-plus TFR, low arm | 1.4025 | [CALCULATION] ratio 0.2082/0.2275 × 1.5325 |
| Mexican-origin TFR, high arm | 2.256 | [SOURCE: NVSR 61-01, Mexican-origin TFR 2010, last year published by origin] |
| NH white TFR, high arm | 1.791 | [SOURCE: same pair, NH white 2010, bridged race] |
| Unauthorized penalty | −$870 per adult 25-64 per year | [SOURCE: `status_impute_2026_09_16` corrected arm, −9,720 imputed-unauthorized minus −8,850 Mexico-born pooled; parsed from the lane's own table] |
| Crime, route A1, Hispanic any race | $1,419.2 social / $507.6 tangible / $423.3 corrections per adult 25-64 | [SOURCE: `crime_cost_2026_09_16`] |
| Crime, route A1, NH white | $553.4 / $222.3 / $191.9 | [SOURCE: same] |
| Fourth-plus identification rate | 0.8881 | [SOURCE: `mexican_origin_population_total_2026_09_19` arm 3, central bound] |
| Attriter retained share of the fiscal gap | 0.1995 | [CALCULATION] −1,417.6 / −7,105.5 from arm 5, Duncan-Trejo selectivity row |

**Generation length.** The own-children-under-5 age-specific rates imply a mean
maternal age at birth of **31.7 years** for the Mexico-born, **28.3** for the second
generation, **29.2** for the third-plus and **31.5** for NH whites. [CALCULATION] The
central 29 sits inside the US-born Mexican-origin range; 26 and 32 are run as
sensitivities and move the gap by −4% and +4%. This is a proxy, not a birth-registry
mean age: it distributes births over mother's age as rate × sample count and subtracts
the 2.5-year mean age of a child under 5. [INFERENCE]

---

## Arm 1 — the central account

Complete account, `personal` allocation, unauthorized founder, per-capita attribution,
low fertility, generation length 29, common US total life table, no real growth,
100 years, 2024 dollars. [CALCULATION, all rows]

| | Mexican lineage | White reference | Gap |
|---|---|---|---|
| Persons generated | 3.05 | 3.15 | −0.10 |
| Founder's own lifetime | −$428,735 | +$126,117 | **−$554,852** |
| Lineage, 100 years, 0% | **−$1,199,871** | **+$97,280** | **−$1,297,150** |
| Lineage per year, 0% | −$11,999 | +$973 | −$12,972 |
| Lineage, present value at 3% | −$339,261 | +$175,374 | **−$514,635** |
| Crime, social, 0% | $136,160 | $52,733 | +$83,427 |
| Crime, social net of corrections | — | — | +$61,101 |
| Crime, tangible, 0% | $48,700 | $21,183 | +$27,517 |

The crime line is not added to the fiscal line. Corrections spending is already inside
the expanded fiscal account, so the incremental social cost outside the ledger is
$61,101 over the century, about 4.7% of the fiscal gap. [CALCULATION]

### By generation, central case

| Generation | Born, calendar year | Persons | Fiscal, 0% | Per person | White counterpart, 0% |
|---|---|---|---|---|---|
| G1 founder | −25 (age 25 in yr 0) | 1.000 | −$428,735 | −$428,735 | +$126,117 |
| G2 | 4 | 0.847 | −$562,455 | −$664,253 | −$113,419 |
| G3 | 33 | 0.548 | −$78,083 | −$142,523 | +$174,497 |
| G4 | 62 | 0.384 | −$85,362 | −$222,191 | −$34,875 |
| G5 | 91 | 0.269 | −$45,235 | −$167,906 | −$55,041 |

Two things drive this table and both are horizon artifacts as much as group
differences. The second generation is the most expensive member of either lineage
because it is the only generation whose whole life fits inside the window: born in
year 4, dead by year 104, it carries a full childhood **and** a full old age, while the
founder entered at 25 with childhood costs borne abroad. The white G3 is positive
(+$174,497) and the Mexican G3 negative (−$78,083) partly because a person born in
year 33 is 67 at the horizon, so the window captures their working life and cuts before
the expensive years — and the white profile's working years are worth far more.
[INFERENCE]

**The 100-year window is not a complete accounting of any generation after G2.** Any
reading of the G3-G5 rows as lifetime balances is wrong.

---

## Arm 2 — disconfirmation

All three arms were preregistered in the brief and all three are reported whether or
not they move the headline. None does. [CALCULATION]

| Arm | Lineage gap | Change vs central | Founder's own gap | Lineage ÷ founder |
|---|---|---|---|---|
| Central | −$1,297,150 | — | −$554,852 | 2.34 |
| **(a)** G4+ carries the attrition-corrected mixed profile | −$1,291,973 | +$5,177 (+0.4%) | −$554,852 | 2.33 |
| **(b)** Founder legalised at year 10 | −$1,272,572 | +$24,578 (+1.9%) | −$530,273 | 2.40 |
| **(c)** Second and later generations at white TFR | −$1,355,369 | −$58,219 (−4.5%) | −$554,852 | 2.44 |

**(a) barely moves** because ethnic attrition only reaches G4, which is 0.38 of a person
born in year 62 with 38 years inside the window. The construction blends 11.19% of G4+
at a profile that retains 19.95% of the self-ID gap to white. The direction is the
expected one — real descendants include attriters, so the base case is an upper bound —
but the magnitude is 0.4%. [CALCULATION]

**(b) moves 1.9%.** Legal status is nearly irrelevant to this account, which is what
ladder 85 already found at the annual level: the imputed-unauthorized and imputed-legal
Mexico-born differ by $1,486 per adult-year against a gap to whites of roughly $9,000.
Running the founder at the Mexico-born average instead of unauthorized moves the gap by
2.6%. [CALCULATION, consistent with SOURCE: ladder 85]

**(c) moves the wrong way.** The brief anticipated that second-generation fertility
falling to white levels would shrink the lineage. It does the opposite, because the
measured second-generation rate is already **below** white: age-standardised own
children under 5 are 0.1921 for the Mexican second generation and 0.2275 for
third-plus NH whites. Raising the descendants to white fertility adds 0.32 of a person
and widens the gap by 4.5%. [SOURCE: `demo_momentum_2026_09_16`] [CALCULATION]

That finding also explains a counterintuitive line in the central case: **the white
reference lineage generates more people than the Mexican one** (3.15 vs 3.05). Only
the founder's own generation is above white fertility.

---

## Arm 3 — growth, and the full sensitivity ranking

All profiles are 2024-dollar period profiles with no productivity growth. One arm
applies 1% real growth to taxes and outlays together, which is neutral to the sign and
changes the level. [CALCULATION]

Ranked by how far each arm moves the lineage gap from the central −$1,297,150:

| Arm | Lineage gap | Move | Persons, Mex / white |
|---|---|---|---|
| Attribution: maternal full (TFR per person) | −$2,710,256 | −109% | 12.27 / 14.00 |
| 1% real growth, 0% discount | −$2,032,384 | −57% | 3.05 / 3.15 |
| High fertility, NVSR 2010 levels | −$2,023,644 | −56% | 6.45 / 4.06 |
| Group-specific mortality (Hispanic / NH white) | −$1,446,528 | −12% | 3.05 / 3.15 |
| (c) descendants at white TFR | −$1,355,369 | −4.5% | 3.37 / 3.15 |
| Generation length 26 | −$1,348,080 | −3.9% | 3.05 / 3.15 |
| `shared` allocation, complete account | −$1,323,167 | −2.0% | 3.05 / 3.15 |
| **Central** | **−$1,297,150** | — | 3.05 / 3.15 |
| (a) G4+ attrition-corrected | −$1,291,973 | +0.4% | 3.05 / 3.15 |
| (b) founder legalised at year 10 | −$1,272,572 | +1.9% | 3.05 / 3.15 |
| Founder = Mexico-born average | −$1,263,920 | +2.6% | 3.05 / 3.15 |
| Generation length 32 | −$1,242,316 | +4.2% | 2.78 / 2.80 |
| Partial account (`all_age_shared`, the brief's main) | −$1,083,822 | +16% | 3.05 / 3.15 |
| Unauthorized 65+ balance set to zero | −$850,861 | +34% | 3.05 / 3.15 |
| Attribution: intermarried half (TFR/4) | −$848,213 | +35% | 1.63 / 1.61 |
| 1% growth at 3% discount | −$665,475 | +49% | 3.05 / 3.15 |
| Central at 3% discount | −$514,635 | +60% | 3.05 / 3.15 |

Crime routes do not change the fiscal gap at all. They move only the crime line: route
A1 gives a social gap of $83,427, route A2 (ACS institutional stock) $137,256, and
pricing the founder at the Texas undocumented arrest-charge rate $46,591. [CALCULATION]

**Which arm moves the gap most: attribution.** It spans −$848k to −$2,710k, a factor of
3.2, and it is a definitional choice about what "a lineage" means rather than a
measurement. Excluding attribution and the discount arms, everything else at 0% spans a factor of 2.4, from the senior-zero rule to 1% real growth. Any headline number
from this lane that does not name its attribution rule is not interpretable.

**The senior rule deserves its own flag.** Zeroing the unauthorized founder's balance
from 65 — the scratch script's convention, on the argument that they draw no Social
Security or Medicare — improves the gap by 34% and improves the founder's own lifetime
gap by 80% (−$554,852 to −$108,562). It is a large, favourable, unsourced assumption.
The central case does not use it. [INFERENCE]

---

## The level moves, the gap does not

| Account | Mexican lineage | White lineage | Gap |
|---|---|---|---|
| `personal` / expanded (central) | −$1,199,871 | +$97,280 | −$1,297,150 |
| `shared` / expanded | −$1,233,481 | +$89,686 | −$1,323,167 |
| `personal` / partial | +$11,070 | +$1,075,589 | −$1,064,519 |
| `shared` / partial (the brief's `all_age_shared`) | −$15,174 | +$1,068,648 | −$1,083,822 |

On the partial account — taxes, selected transfers, medical, K-12, sales and property
proxies — the Mexican lineage is roughly balanced, within $15k of zero over a century,
and the white lineage is worth a million dollars. On the complete account, which
charges state-local general services, capital outlay, transfer under-reporting,
improper payments, institutional care and the rest of the federal budget by function,
both fall by roughly $1.2M and the Mexican lineage goes deeply negative. [CALCULATION]

The gap ranges only −$1.06M to −$1.32M across the four constructions, a 24% spread,
while the Mexican lineage's absolute level moves by $1.21M and flips sign. That is the
same pattern ladder 130 records at the annual level, and it is the reason this lane's
headline is the gap. **Quoting the absolute without naming the account breaks the
quant-bias gate's compressed rule, which requires every load-bearing number to carry
its ledger, base and gross-or-net status.** [INFERENCE]

---

## What was skipped, and why

- **No uncertainty intervals.** The upstream profiles carry CPS replicate and MEPS
  donor standard errors in `estimates.csv`, and none of them propagate here. The spread
  across arms is 3-5× any plausible sampling interval, so the arms are the honest
  uncertainty statement, but a confidence interval on the central number is not
  available and is not implied. [UNVERIFIED]
- **Intermarriage is a rule, not a measurement.** `intermarried_half` halves mixed
  children by assumption. No repo lane measures Mexican-origin intermarriage rates by
  generation, and I did not go acquire one.
- **No emigration or return migration.** A founder who leaves takes their remaining
  balance and every descendant not yet born with them. The direction is unambiguous,
  smaller lineage and smaller gap, and the magnitude is not estimated because no lane
  in this repo measures Mexico-born return rates. This is the largest unmodelled
  channel. [INFERENCE]
- **The pronatal triangulation is unresolved** at 0.1-5.4%, as reported above.
- **The `truncate83` horizon** in the upstream lifetime module is reproduced in the
  oracle but not used as a lineage arm; the 100-year calendar window already truncates.
- **No NIBRS, no 2023-24 arrest update.** The crime line uses the 2026-09-16 and
  2026-09-18 lane outputs as they stand. Ladder 78 records that the arrest year is the
  dominant source of variation in the crime figure, so the crime line here is one point
  in a band of roughly ±40%, and it is under 5% of the fiscal gap either way.

---

## Draft memo section

> **The descendants, not the arrival, carry most of the hundred-year gap.** Take one
> Mexico-born arrival aged 25 who remains unauthorized, follow their lineage for a
> century on the complete fiscal account, and compare it with one third-plus
> non-Hispanic white of the same age followed the same way. The immigrant lineage runs
> −$1.20M, the white lineage +$97k, a gap of −$1.30M, or about −$13,000 a year. At a 3%
> real discount the gap is −$515k. The founder's own lifetime is −$555k of it. The
> remaining 57% belongs to descendants who were born in the United States.
>
> The most expensive person in either lineage is the US-born second generation, at
> −$664k against the white second generation's −$148k. That is partly a real difference
> in profiles and partly an artifact of where the window falls: the second generation is
> the only cohort whose entire life fits inside a hundred years starting from the
> founder's arrival at 25, so it carries a full childhood and a full old age, while the
> founder's childhood was paid for by Mexico. Generations three and later are cut
> mid-life by the horizon and their totals are not lifetime balances.
>
> Legal status is close to irrelevant to this account. Legalising the founder at year
> ten improves the gap by 1.9%; running the Mexico-born average instead of the
> unauthorized profile improves it by 2.6%. That is the lineage-level restatement of
> what the annual ledger already showed, where imputed-unauthorized and imputed-legal
> Mexico-born adults differ by about $1,500 a year against a gap to whites of about
> $9,000.
>
> Fertility no longer works the way the demographic argument assumes. Age-standardised,
> the Mexican second and third generations now carry fewer young children than
> third-plus white women, so the white reference lineage generates slightly more people
> over the century than the immigrant one, 3.15 against 3.05. Forcing the descendants
> up to white fertility widens the gap by 4.5% rather than closing it.
>
> Two cautions bound all of this. The absolute level is an artifact of the account:
> on the partial ledger the immigrant lineage is within $15,000 of balance over a
> century and the white lineage is worth a million dollars, while the gap moves by only
> a quarter. And the answer depends more on how you define a lineage than on anything
> measured: attributing every child of a lineage member whole to that lineage rather
> than splitting each child between two parents doubles the gap to −$2.71M, while
> halving mixed children cuts it to −$848k. The gap is robustly large and robustly
> negative. Its size is a modelling choice as much as a measurement, and no figure from
> this exercise should be quoted without the rule that produced it.

---

*Lane: `infra/immigration-fiscal/lineage_cost_2026_09_19/`. Not committed. No files
outside this directory were written. No policy recommendation is made or implied; the
repo measures resident groups, not admission.*
