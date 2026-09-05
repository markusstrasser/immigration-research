# Material conceptual and mathematical audit — 2026-09-05

**Subsequent resolution, 2026-09-05:** This is the initial pre-repair audit. Its identified errors led to corrected code, a raw-data fiscal rebuild, revised interpretations and new evidence acquisition. Use the [completed repair record](immigration-material-repair-report-2026-09-05.md) for current results and limits; the initial findings and access conditions below are preserved as the record that triggered the [repair decision](../decisions/2026-09-05-material-inference-repair.md).

**Verdict:** Several consequential errors survive in the June dismantling synthesis and in the local fiscal pipeline. The distributional questions remain legitimate, but some claimed refutations fail, and the SIPP-derived fiscal estimates require rebuilding. A correctly transcribed quotation or successfully reproduced number does not validate the inference made from it. [INFERENCE, supported by the checks below]

**Scope:** Review requested for major assumptions, logic and calculations, without copy-editing or minor objections. Read the current consolidated synthesis and its supporting Decker, Cato and Clemens arguments; inspect the current fiscal pipeline and selected live warehouse outputs. This is a bounded audit, not certification of every research file. Sources and prior conclusions remain intact as historical records; the corrections below supersede the specified claims. No canonical data rebuild or source-code repair was performed during this review.

**Frame:** Incumbent welfare, worldwide output, public budgets and subgroup outcomes are separate questions. No political sign is assumed. This remains an LLM-assisted review; reported errors rest on source definitions, call traces or counterexamples rather than the model's asserted ideological predisposition.

## 1. The local federal proxy mixes household and person units

**Confirmed implementation error.** `infra/immigration-fiscal/build/build_federal_microsim_sipp_2024.py:118` groups eligible same-nativity adults by household/residence/month, sums their earnings and transfers, and retains the first encountered adult's age and education. Lines 148–150 assign an income band to that summed household amount. Lines 249–280 then match these donor amounts to **individual** ACS income bands and adult weights. The household total is carried into the per-adult fiscal proxy without a consistent allocation. [SOURCE: current implementation and bounded donor fixture]

An isolated fixture ran the actual donor builder and microsimulation loader with two adults each earning $8,000 annually and receiving no transfers. Both individual and household incomes fall in the same matching band, and its education code is unaffected by error 2. The builder produces **$2,448 payroll for the two adults; the correct employee-payroll arithmetic is $1,224**: `2 × 8,000 × 0.0765`. This directly demonstrates duplication. A live warehouse join also finds 10,030 matched rows carrying the household donor amount unchanged. [EXECUTED PROBE: `build_donor_cells`, `load_federal_microsim_into_duckdb`; read-only warehouse query]

The defect is not a universal factor of two. Different household sizes, transfer allocations and mismatched income bands change the correction. For example, two adults each earning $24,000 enter a $48,000 household-income donor band rather than their individual $24,000 bands. [RECALC]

**Implication:** Treat the associated SIPP-based per-adult and origin fiscal estimates as invalid pending a consistent donor rebuild, including Mexico's **+$1,519/adult, +$12.9B/year and the ~1.8× native-white/Mexico comparison**. Reproducing their existing SQL totals does not validate their economic meaning. The stored donor cells discard information needed to reconstruct individual members; the raw inputs needed for a defensible replacement were not available at the configured paths. The direction and size of the national correction are therefore unresolved. This does not invalidate independently sourced CBO or NAS estimates. [SOURCE: `immigration-federal-distribution-findings-2026-06-15.md:61–83`; `immigration-lifetime-unified-theory-2026-06-15.md:28,53,60–61`; calculation trace]

## 2. SIPP education is also coded incorrectly

**Confirmed against the primary dictionary.** `infra/immigration-fiscal/build/public_mvp_io.py:68` maps codes 34–35 to high school and 38–39 to associate degree. The Census definitions make 34–35 seventh–ninth grade and 39 high-school completion. Code 43 is a bachelor's degree, but this function assigns it to master's. The microsimulation uses this mapping to select donors. [SOURCE: Census, *2024 SIPP Data Dictionary*, printed p.889, [EEDUC definitions](https://www2.census.gov/programs-surveys/sipp/tech-documentation/data-dictionaries/2024/2024_SIPP_Data_Dictionary.pdf#page=889)]

Correct broad groups for the target ACS categories are:

| SIPP EEDUC | Broad education group |
|---|---|
| 31–38 | Less than high school |
| 39 | High school / GED |
| 40–42 | Some college / associate |
| 43–46 | Bachelor's and above |

**Implication:** Education-specific comparisons use materially wrong donors. Reclassifying the already-collapsed output cannot recover the lost raw codes. These results need rebuilding along with the household/person correction. [INFERENCE]

## 3. The GDP-per-person rebuttal does not measure incumbent welfare

**Locations:** `immigration-dismantle-decker-2026-06-25.md:50–57,188`; consolidated synthesis `:129–134`.

The February 2024 CBO projection really has approximately +2% total real GDP and −0.8% real GDP per person in 2034. However, its denominator includes the newcomers. It is not an estimate of the change in the welfare of the people already resident. [SOURCE: [CBO February 2024, Box 2-1, p.50](https://www.cbo.gov/system/files/2024-02/59710-Outlook-2024.pdf#page=56)]

**Counterexample, not an immigration estimate:** Start with 100 residents each earning 100. After immigration each earns 101, and 20 newcomers each earn 50. The new average is `(100 × 101 + 20 × 50) / 120 = 92.5`. Incumbents gain 1% while the population average falls 7.5%. [RECALC]

CBO's July 2024 analysis explicitly distinguishes existing workers from newcomers: it projects short-run wage-growth reductions for less-educated existing workers, followed by productivity-related gains. Its TFP model also includes innovation. That evidence needs to be evaluated on its own terms. [SOURCE: [CBO July 2024, p.21](https://www.cbo.gov/system/files/2024-07/60165-Immigration.pdf#page=21)]

**Separate mathematical error:** The Decker memo says total GDP up plus GDP per person down is “a richer structure than CRS allows.” False. `F(K,L) = sqrt(KL)` has constant returns: `F(tK,tL) = tF(K,L)`. At `K=L=100`, output is 100. Holding capital at 100 and increasing labor to 121 raises output to 110, while output per worker falls from 1 to `110/121 = 0.9091`. Constant returns concerns scaling **all inputs together**, not changing one factor or worker composition. [FORMAL COUNTEREXAMPLE]

**What survives:** Increasing returns alone does not guarantee a positive net welfare effect for every inflow. But the cited population average does not establish incumbent losses, and the CRS “bonus kill” should be withdrawn.

## 4. The Cato critique alleges an asymmetry its source does not use

**Locations:** `immigration-dismantle-cato-2026-06-25.md:59–67,126`; consolidated synthesis `:66–67,151–159`.

Cato's $14.5T historical estimate does **not** bank descendants' future taxes while omitting their schooling. Its separate first-plus-second-generation calculation includes costs and taxes and reports +$7.9T including interest savings. This does not independently validate Cato, but it defeats the stated allegation. [SOURCE: [Cato 2026, methods and Table 13](https://www.cato.org/white-paper/immigrants-recent-effects-government-budgets-1994-2023)]

The additional claim that removing **either** assumption makes state/local results negative has no matching recalculation. A different NAS cohort, accounting window or government level cannot establish that sign. [INFERENCE: comparison as written]

NAS's warning that zero marginal public-goods costs become less tenable for sustained large inflows is a reason for sensitivity analysis, not proof average-cost attribution is uniquely correct. Congestible services and pure public goods must also be distinguished. [SOURCE: [NAS, chapter 8, pp.360–364](https://www.nationalacademies.org/read/23550/chapter/13)]

**What survives:** The first-generation historical result does not settle a dynastic policy counterfactual. Public-goods and dependent allocation warrant matched sensitivity analysis. The precise 1994–2023 state/local sign under alternate allocations remains unresolved; no replacement total is claimed here.

## 5. The global-gains rebuttal contains a calculation error and a stale benchmark

**Locations:** `immigration-dismantle-clemens-2026-06-25.md:48–51,92`; consolidated synthesis `:137,216–226`; repetitions in the Decker and Cato submemos.

**Recalculation using the repo's own assumptions**—$7,500 annual gain per additional migrant and a $110T world-GDP base:

| Additional migrants | Annual gain | Share of baseline world GDP |
|---|---:|---:|
| 200 million | $1.5T | 1.36% |
| 1 billion | $7.5T | 6.82% |
| 3 billion | $22.5T | **20.45%** |

Thus “+3B for doubling” is wrong. A 100% increase would require `110T / 7,500 = 14.67 billion` additional migrants in this fixed-gain illustration. That implausible requirement is a property of the chosen calibration, not an independent empirical disproof of other models. [RECALC from inputs already reported in `immigration-open-borders-double-world-gdp-and-apartheid-audit-2026-04-21.md:103–110`]

**Source-version correction:** The repeated Docquier–Machado–Sekkat ~4% figure is a real scenario in the 2012 draft. Their published 2015 paper reports a medium-term benchmark of **11.5–12.5%**, with **7.0–17.9%** across robustness cases. The final benchmark was verified on the publisher's own abstract and institutional record; the final model body was not accessible, so the technical reason for the revision remains unverified. Do not present 12% as merely an arithmetic correction to an identical scenario. [SOURCE: [published paper](https://doi.org/10.1111/sjoe.12097); [2012 draft](https://sites.uclouvain.be/econ/DP/IRES/2012023.pdf)]

**Two further scope errors:**

- A US housing-start benchmark is not a measurement of all rich-country destinations' construction capacity. Current building rates are not a fixed physical maximum over thirty years. The April source explicitly labels this a US comparison; the June summary upgrades it into a global binding limit. [SOURCE: `immigration-open-borders-break-even-bounds-2026-04-22.md:14,59`; INFERENCE]
- Clemens–Pritchett's interior optimum constrains the migration **rate** during a transition. It supports rates several times then-current levels and is not a demonstration that large cumulative relocation is impossible. The qualification about pacing is real; “mass-absorption no is precisely their position” overstates it. [SOURCE: [full working-paper model and calibration](https://docs.iza.org/dp9730.pdf), sections 5–8; [published article](https://doi.org/10.1016/j.jdeveco.2018.12.003)]

**What survives:** A doubling forecast remains highly model-dependent. These corrections weaken the purported refutation; they do not establish doubling as a reliable forecast.

## 6. The second-generation crime claim has an undetermined sign

**Locations:** consolidated synthesis `:52–74`; `immigration-confidence-ladder.md:240–242`.

The memo reasons that second-generation offending exceeds first-generation offending, so including the second generation in the native-born comparator inflates that comparator. The conclusion requires a different comparison. [FORMAL CHECK]

Let `r2` be the second-generation rate, `r3` the third-plus-generation rate, and `a` the second-generation share of the native-born denominator. Then:

`r_native = a*r2 + (1-a)*r3`

`r_native - r3 = a*(r2-r3)`

Inflation requires **r2 > r3**. Knowing only that **r2 > r1** does not establish it. With illustrative rates `r1=1, r2=2, r3=3` and `a=0.2`, the native-born comparator is 2.8, below 3; inclusion actually narrows the first-generation advantage relative to a third-plus comparator. Convergence to `r3` leaves that comparator unchanged. [RECALC]

Nor does coding US-born children as native-born inherently make a nativity comparison erroneous; it means it does not answer a descendant-inclusive question. The latter requires matching the relevant generational populations and outcomes. [INFERENCE]

**The proposed resolver cannot resolve crime:** `infra/immigration-fiscal/build/load_cps_second_gen.py:94–128` computes employment, log income, education and female labor-force participation. It contains no offending measure. The related P1 preregistration concerns income and participation. This extract cannot settle the magnitude of a generational crime correction. [SOURCE: implementation; `immigration-preregistration-ledger.md:23–39`]

**What survives:** First-generation findings cannot automatically be generalized to descendants. The available argument does not establish the size or direction of bias relative to third-plus-generation natives. No revised empirical crime rate is claimed.

## 7. The welfare inequality needs a non-overlapping accounting definition

**Locations:** `immigration-smith-decker-friedman-comparative-quantitative-audit-2026-04-11.md:143–151`; Decker submemo `:54–55`; Clemens break-even discussion.

The proposed sum adds macro/productivity gains, consumer/employer surplus and federal revenue, then subtracts wage, local-budget, housing and political costs. As written it is a checklist of mechanisms, not an accounting identity. Income generated by higher productivity can already appear in profits, wages and taxable income. Adding the channels without defining exclusive components risks counting the same effect repeatedly. [ACCOUNTING / INFERENCE]

Likewise, a $100 rent increase is $100 less for the tenant and $100 more for the landlord before secondary effects. Tenant harm matters; the entire payment is not automatically lost national or global output. Different welfare weights, foreign ownership, construction costs and congestion can change the net welfare effect, but must be stated and measured. [ACCOUNTING EXAMPLE]

The reported `$1.5T / 1.4B = $1,071.43` incumbent-loss threshold is arithmetically correct. Showing local rent pressure does not show that this amount of **net additional** annual global loss occurs. [RECALC / INFERENCE]

**The deeper assumption to drop:** A policy's average net benefit does not require every subgroup or government budget to gain. A state/local loss can coexist with an aggregate gain; conversely an aggregate gain does not compensate a losing locality automatically. Require the appropriate net-incumbent calculation or an explicitly distributional objective, not a positive sign in every ledger. [LOGIC]

## 8. Forecasts have been promoted to observed results

**Locations:** consolidated synthesis `:24,299`; Smith submemo `:84,145`; Decker submemo `:185`; Hernandez submemo `:95,203`.

CBO's approximately $0.9T deficit reduction and $8.9T additional nominal GDP are modeled cumulative effects over 2024–2034. Calling them the “realized” fiscal outcome is incorrect. They are also different quantities, not additive welfare benefits; the separately cited Colas–Sachs channel cannot simply be added without checking overlap. [SOURCE: [CBO July 2024, summary and Figure 2](https://www.cbo.gov/system/files/2024-07/60165-Immigration.pdf); INFERENCE]

## Overall interpretation and limits

**Additional checked local arithmetic and labels:** The separate NAS composition calculation reproduces `$387,697,847,000 / 8,496,334 = $45,631.1918764` per adult. This confirms multiplication of the stored benchmark cells, not their external validity as the remaining-life NPV of today's population; the source memo already identifies that limitation. In contrast, `immigration-lifetime-unified-theory-2026-06-15.md:56` labels 7,686,859 as Mexico's less-than-high-school stock, but the source table's row is for **all foreign-born** adults. The Mexico count used in the checked multiply-out is 3,958,855. The mislabeled row did not contaminate that calculation. [READ-ONLY DATABASE RECOMPUTATION]

The school memo and live warehouse also disagree about which origin/native school rows are available. This is a currency discrepancy, not validation of the newly available school values. The previously rejected $771 school / +$748 net pair remains rejected; no school-plus-federal replacement is endorsed while the federal input is invalid. [SOURCE: `immigration-school-burden-per-adult-2026-06-15.md:4,39–47`; current `v_three_layer_annual` and its builder]

The defensible core is that effects differ across people, places, policies and horizons. The stronger claim that the named economists have been refuted often rests on a missing step: evidence of a cost is not proof of a negative net effect; an unmodeled channel is not proof its magnitude dominates; and a source answering another question is not inherently wrong. Several June summaries also overstate qualifications already present in their April source memos. [INFERENCE from the findings above]

The concrete repair priorities are: rebuild the federal proxy with consistent units and verified codes; withdraw the GDP/CRS and Cato accounting rebuttals as written; correct the migration arithmetic and source version; and replace the asserted generational crime bias with its actual conditional sign. Broader questions about housing, fiscal allocation and global gains remain substantive but unresolved at the strength currently claimed.

**Coverage:** Included the consolidated synthesis, relevant Decker/Cato/Clemens submemos, confidence-ladder rows, comparative welfare inequality, April global-gains/break-even sources, fiscal/lifetime synthesis, schooling sources, current donor and tensor implementation, and the CPS loader/preregistration. Read primary CBO reports, the SIPP dictionary, Cato methods and dependent accounting, NAS allocation discussion, the DMS draft and final publication metadata, and the Clemens–Pritchett model. Separate bounded checks covered Cato accounting, global-gains models and local fiscal calculations; the parent verified their implications and the explicit counterexamples.

**Not certified:** Every quotation across all seven authors; underlying crime microdata; a complete wage-literature meta-analysis; every warehouse table; the final DMS full model; or an exact Cato state/local counterfactual rerun. Raw-data limitations prevent corrected national SIPP totals. These gaps are not negative findings about those studies.

**Reproduction from this session:** The isolated fiscal probe and full JSON output are `/tmp/immigration-fiscal-math-probe-2026-09-05.py` and `/tmp/immigration-fiscal-math-probe-2026-09-05.json`. Run `uv run --with duckdb,pandas python3 /tmp/immigration-fiscal-math-probe-2026-09-05.py` from the repo root while that temporary script is available. Persistent warehouse connections are read-only; the fixture uses an in-memory database and synthetic temporary inputs. The identities and migration arithmetic above can be recomputed directly from their displayed inputs.
