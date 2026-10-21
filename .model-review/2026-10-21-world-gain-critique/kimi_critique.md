# Attack on the analyst's claims

Ground rules I applied: I verified every number I could against `readings_subset.csv` and the RESULT excerpt, recomputed the ones I couldn't take on faith, and flagged what I cannot verify from the excerpt. Citations are to work I'm confident exists; I say so when I'm not.

---

## Claim 1 — "R3 (MMP same-person hourly gain 2.0) is the most defensible pay counterfactual"

**Verdict: mostly wrong. R1 is the better-anchored reading; R3 as implemented appears internally mis-scaled, and its provenance is weaker.**

Three independent problems.

**(a) The hourly-to-annual conversion is inconsistent with the ledger's own basis.** The ledger defines the premium as annual, per person, "zeros included, so employment and hours differences are part of it," and it *measures* the gap: G1 employment 67.2% (US) vs 70.5% (Mexico), hours 38.7 vs 46.4. From the group totals, R3's G1 premium is exactly recoverable: R1 − R3 = 646.73 − 570.94 = **75.79bn**, so R3 implies a G1 premium of 263.0 − 75.8 = **187.2bn**, i.e. an *annual* ratio of 378.4/191.2 = **1.98 ≈ 2.0**. But if 2.0 is an *hourly* same-person ratio, the annual ratio with measured hours and employment is 2.0 × (0.672 × 38.7)/(0.705 × 46.4) = 2.0 × 0.795 = **1.59**, giving a premium of only ~140bn. R3 as executed is ~**$47bn/yr too high** relative to its own stated parameter — unless the MMP factor was already annual, in which case the claim's word "hourly" is wrong and the hours evidence in the same document is being ignored. Either way this must be reconciled before R3 is "most defensible" anything.

**(b) Provenance and representativeness.** I cannot verify the MMP 2.0 figure from the excerpt, and I am not confident of a published MMP same-person estimate of exactly 2.0 — that needs a citation. Two known problems even if it exists: MMP samples are drawn from selected high-migration sending communities and are not nationally representative (documented in the MMP methodology literature, Massey and collaborators), and same-person estimates that observe the Mexican wage of *return migrants* are contaminated by return selection (Borjas & Bratsberg, "Who Leaves? The Outmigration of the Foreign-Born," QJE 1996) and by partial transferability of US-acquired skills, which biases the premium *down*. Meanwhile R1's p56 is not "choosing a percentile" in the pejorative sense — it *is* CMP's point estimate of selection (δ = +0.028), implemented on 2024 CPS/ENIGH cells of the actual population, including women and all arrival ages. The selection literature for Mexico (Chiquiar & Hanson, JPE 2005; Kaestner & Malamud, ReStat 2014; McKenzie & Rapoport, ReStat 2010; Ibarrarán & Lubotsky 2007 in the Borjas NBER volume) brackets neutral-to-moderately-intermediate selection, which is what p56 embodies. And the experimental evidence we do have on selection corrections (McKenzie, Gibson & Stillman, ReStat 2010, Tonga→NZ lottery) finds selection corrections *modest* relative to the raw place premium — supportive of R1-style direct estimation.

**(c) "CMP ~2.5x, so R3 is conservative" cherry-picks the benchmark.** CMP report Ro 2.53 / Re 2.46 on a 2002 vintage; the ledger's own check on 2024 data gives 3.00 per person (3.15 per worker) for the CMP-comparable subset. Since 2002, Mexico's real minimum wage roughly doubled in real terms (2019–2024 compression at the bottom), so the 2002-vintage ratio *overstates* today's counterfactual ratio for low-wage cells — while the direct 2024 method handles this automatically. R1 borrows only CMP's *selection percentile* (which may itself have drifted since 2002 — flag as [ASSUMPTION]) and measures levels fresh. That is the right architecture.

**Parameter I would defend:** R1's design — direct cross-section at CMP's p56 selection, consumption PPP (see claim 2), G1 premium ≈ 263bn, span ~190–290 across {p70/output-PPP, p50/consumption-PPP}. Treat the hours-consistent MMP number (~1.6 annual, ~140bn) as a low outlier pending provenance, and CMP's Re 2.46 (→ 224.6bn) as a cross-check that sits *inside* R1's span. Note the claims' preferred reading (R3) under-prices G1 by ~76bn relative to this.

Also: R3 changes G1 only (the 75.79bn gap is identical at both ends — confirmed). Claim 1's prose implies a general methodological superiority; it is silent on G2's rearing convention and G3+'s bound, which are far larger swings.

---

## Claim 2 — "Household consumption PPP is the right deflator"

**Verdict: right in principle; the implementation is under-documented and partly inconsistent.**

The welfare object is the same person's real consumption gain across locations, so a consumption PPP is the correct conversion — this is also CMP's practice, and with the US as ICP numeraire it puts the premium and the US-side fiscal flows in consistent "US-consumption-equivalent dollars," which is the best achievable unit for the equal-weight sum. But:

- **Internal contradiction to resolve.** Section A (labeled case-independent) converts ENIGH at **GDP PPP 9.9166** and the CMP check (3.00) is at that factor. If R1/R3 in fact use household-consumption PPP, the PPP basis differs between the premium table and the readings, and the per-reading basis must be documented. Mexico's consumption PPP is typically a few percent above its GDP PPP (verify against ICP 2021; I am not certain of the 2024 value), which would *lower* E_MX and *raise* the premium a few percent (~+$10bn across G1+G2) — small, but it belongs in the table.
- **Mexico's fiscal rows** are government services; converting them at household-consumption PPP misvalues them in both directions. ICP's government-consumption PPP is the right factor there.
- **ICP vintage matters.** The 2021 ICP round moved many PPPs by several percent; state the round and the sensitivity.
- **PPPs for the poor.** The group's comparators are low-decile; national-bundle PPPs can misstate poor households' price levels (Deaton, AER 2010; Deaton & Dupriez 2011 on poverty PPPs). Direction for Mexico is uncertain; flag, don't resolve by silence.
- **Intra-US spatial prices.** The group is concentrated in high-cost metros (LA, Houston, Dallas, Chicago). The US side is nominal dollars at a national numeraire; the group's real US consumption is thereby overstated by perhaps 2–4% (a ~$8–15bn effect on the premium), partially offset by metro wage premia (Moretti 2013; Diamond & Moretti spatial-equilibrium logic). Worth one row.
- **R2's "output service prices"** is defensible only for a *production* account, which this is not — it is a welfare ledger with fiscal transfers. But note the hybrid-unit problem is *minimized* by consumption PPP, not eliminated: VSL rows and PPP-converted earnings are different kinds of dollars (see claim 6).

**Parameter I would defend:** ICP 2021 household-consumption PPP for E_MX and remittance-household rows; government-consumption PPP for Mexico's budget rows; report GDP-PPP sensitivity (~±$10–15bn on the world total). So claim 2's *position* survives, with the consequence that it slightly *raises* the premium relative to section A's printed central.

---

## Claim 3 — "Average cost probably overstates the group's valuation of general administration; no WTP measure; unsettled"

**Verdict: right directionally, but dramatically understated — and it silently demotes claims 1 and 5.**

- **The swing is the largest single convention in the ledger.** On sept27, public goods valued at average cost exceed their responsive cost by **$145.8bn** at the low end (−$161.8bn on the schools case). The response-only convention cuts the group's valued position from +$222.1bn to +$76.3bn. This one knob is bigger than the entire R1↔R2 pay-method gap. A reading cannot be "most defensible" (claim 1) while embedding a convention the analyst himself flags as probably overstated, at half the mid-convention value, without quantification (the oct16 value is not in the excerpt — recompute).
- **"No WTP measure exists" is belied by the ledger itself.** The justice class already does a WTP-style split (protection share 0.4247 at average cost; offender processing at zero), and the ledger prices public safety at DOT VSL — safety *is* a public good. The issue is not the absence of WTP methods; it is that WTP is applied selectively, to categories that cut against the group, while administration gets average cost. That asymmetry is adversarially indefensible.
- **The sign of the bias is ambiguous for the non-rival share.** For defense, basic law, non-rival administration, marginal provision cost ≈ 0 while the group's consumption value is real; average cost may *understate* WTP there. For congestible goods (roads, parks, transfer-program administration), marginal WTP ≈ marginal cost and average cost overstates. Honest treatment: split the class; absent the split, carry the two conventions as a ±~$73bn span around a midpoint — **not** a point in the "central."

**Parameter I would defend:** midpoint of the two conventions (−~$73bn to the group/world total at sept27 scale), with the full ±span reported; long-run, build the non-rival/congestible split.

---

## Claim 4 — "λ = 1 is least defensible; 1.16–1.29 defensible; 1.29 implied by Hendren's weights"

**Verdict: mixed. Right that λ = 1 is hard to defend at the margin for a budget this size; wrong that 1.29 is an efficiency parameter; and the financing mix plausibly pulls the correct blended λ below 1.16.**

- **1.29 is a welfare artifact, not a resource cost.** λ_h = 1.286 falls out of Hendren's *distributional* weights under a tax-share financing experiment (numerically, 1/E[g over payers] with E[g] ≈ 0.78). It embodies the policymaker's revealed inequality aversion. You cannot coherently (i) insist on equal dollar weights for the benefit side and (ii) charge the cost side at a λ derived from distributional weights. The ledger contains the consistent pair: the Hendren a/b columns, which leave **R1 at +284.2/288.2bn** — i.e., under the welfare function that *generated* 1.286, the leak is fully offset by the redistribution's value. The claims lean entirely on the asymmetric hybrid column (`equal_lambda_hendren_a`), which charges distributional-motivated financing costs while refusing distributional credit. That column is the worst of both metrics, and the headline never reports the consistent one. This is the single most important rhetorical flaw in the claim set.
- **The blended λ for *this* budget mix is probably below 1.16.** 1.16 is HSK's lowest top-*federal-income*-rate MVPF (Hendren & Sprung-Keyser, QJE 2020). But the largest single fiscal line is K–12 schooling (~$214–227bn), financed mainly by local property and sales taxes; property taxation on a benefit-tax view has MCPF close to 1.0–1.1, and sales taxes carry lower MEB than top-rate income taxation. A financing-share-weighted MCPF for this specific budget plausibly lands at **1.08–1.20**. Conversely, if part of the cost is deficit-financed (the oct07 notes reference "the borrowed part"), charging λ on that part double-counts — debt carries interest (already a cost) and defers λ to repayment. [Verify in code how the borrowed part is treated.]
- **λ = 1.5 is an upper sensitivity, not a corner to headline.** Its provenance is Browning (1987) via Heckman–Smith — pre-ETI-literature. Modern central estimates (Ballard, Shoven & Whalley, AER 1985; Gruber & Saez 2002; Saez, Slemrod & Giertz, JEL 2012's mid-range ETI; Dahlby 2008) support roughly 1.1–1.3 for US marginal financing, with the high tail driven by top-rate instruments. Note also Kleven & Kreiner (EER 2006): participation margins can push MCPF up in high-tax European settings — not obviously the relevant margin here.
- **Mexico's λ is an unpriced [ASSUMPTION].** The same 1.16/1.5 is applied to Mexico's fiscal rows (base ~127.5/69.1bn — arithmetic below). With >50% informality and a commodity-tax-heavy mix, Mexico's MCPF is a different, unmeasured object; evasion margins push it up, instrument mix pushes it down. "Symmetric application of a US parameter" is not symmetry.

**Parameter I would defend:** λ = **1.15** central (span 1.05–1.30), applied only to the *net marginally-financed fiscal component*, excluding the borrowed part, the pension accrual (already fixed), and all non-fiscal rows; λ_MX = 1.1–1.3 as a flagged assumption; report Hendren a/b as the welfare-consistent alternative and stop calling the hybrid "Hendren."

---

## Claim 5 — "Most defensible world gain ≈ $45–170bn, central near $100bn; negative at λ1.5 under R2/R3"

**Verdict: not robust. The range is a corner-span of the least defensible choices stacked in one direction, and it omits the largest upside knob entirely.**

- The endpoints are exactly the `λ_h` column across R3→R1 (low end): 44.94 to 169.90. So the claim silently adopts the asymmetric hybrid of claim 4 as its operative metric. Under λ = 1.16 the span is 35.8–220.7; under equal weights, 98.6–285.0. "Central near 100" is R3 at λ1.16 — one cell.
- **The range excludes G3+ entirely.** Every row in the subset is `g3_bound = zero` — the bound that assumes 14.34M US-born descendants would earn *their US pay in Mexico* (E_MX = E_US). That contradicts every wage datum in the document, including Mexico's wages for high-school-plus workers running ~3–4× below US levels. The upper bound is +252.7bn. A defensible positive premium (see omissions, +60–130bn) shifts the entire claimed range up by that amount.
- **The claims accept average-cost public goods (up bias ~+73bn vs midpoint) and the zero G3+ bound (down bias ~+84bn at one-third of upper) simultaneously**, then present the result as a conservative central. The two do not cancel reliably; they are independent choices, one aggressive, one conservative.
- "Turns negative at λ1.5 under R2/R3" is true in the table (−97.7/−78.0; −49.0/−43.1) and irrelevant to a central: it stacks the Browning-era upper λ with the least defensible pay basis. Under the welfare-consistent Hendren columns, R1 stays ≈ +284/288.

The honest statement of claim 5 is: *the sign of the world total is not robust; the central tendency depends on three unresolved choices (G3+, public goods, λ), two of which the claim set resolves to the low side.*

---

## Claim 6 — "Other US residents lose $340–401bn (λ=1) / $419–499bn (λ1.29) in every reading; a large transfer with a thin remainder"

**Verdict: the numbers check out against the CSV; the rhetoric does not.**

- **"In every reading" is construction, not robustness.** The readings vary only group-side parameters, so the others line is *identical by design* across R1/R2/R3 (−340.643/−401.060; −419.177/−499.295 at λ_h — verified). The line moved −34.1/+23.1bn on a single decision (2026-10-21), carries [FRAMING-SENSITIVE] removal conventions and the [DEGRADED] P032 all-public pension proxy at share 1. That is a modeled account with live data risk, not a measured loss replicated across readings.
- **"Thin remainder" is reading-dependent.** The group gains 646.7/648.0 (R1) against the transfer. Remainder as a share of the transfer from others: **84%** (λ=1), **57%** (λ1.16), **41%** (λ_h) under R1. Only under R2 (and R3 at λ_h) is the remainder thin (29%, 9%, −3%). Under the CMP-anchored reading, the world keeps two-fifths to five-sixths of the transfer as net gain.
- **Unit hybridity.** The case is branded "matched-cash," yet the others line and the group's line include victimization at **DOT VSL** (−28.91/−32.20bn in-group, plus the property-crime and victims rows). A VSL dollar is a welfare construct, not cash; mixing it into a "cash" account overstates the transfer in cash terms and contaminates the breakeven-w arithmetic. At minimum, decompose the line into cash / VSL / pension-proxy components.
- **External inconsistency on the second generation.** The ledger has G2 as a net fiscal cost to others of $128–153bn/yr (≈ $9–10.7k per person). NAS (2017, *The Economic and Fiscal Consequences of Immigration*, ch. 8) finds the second generation the *most fiscally positive* generation in most scenarios. Part of the gap is definitional (the ledger counts 4.18m G2 children and the cross-sectional growing-cohort charge, which the document itself admits "leans toward cost"), but a discrepancy of this size against the benchmark study demands a reconciliation table, not silence. If NAS is even half right, the others line is overstated by tens of billions.

---

## Claim 7 — "Excludes institutional/political output losses (unpriced; 1% of GDP ≈ $293bn) and innovation/agglomeration"

**Verdict: right and candid, but asymmetric — the unpriced-upside list is longer than the unpriced-downside list, and the 1% benchmark is an arbitrary scale with no probability attached.**

- The 1% figure is a constructed sensitivity (BEA 2024 GDP 29.30tn × 0.01 — arithmetic verified), not a measured channel; the document says so. Fine. But then symmetry requires listing the unpriced *upside* at comparable scale: G3+'s upper bound alone is +252.7bn (almost exactly the size of the 1%-of-GDP scare number), agglomeration/market-size effects of a 13%-larger population, consumer surplus (below), and Mexico-side effects. Naming only the downside converts "unpriced" into "presumed negative."
- The measured partial evidence on the institutional/cultural channel is itself two-sided: Putnam (2007, *Scandinavian Political Studies*) finds short-run diversity→social-capital costs; Alesina, Harnoss & Rapoport (JEG 2016) find birthplace diversity *positively* related to prosperity; Docquier, Lodigiani, Rapoport & Schiff (JDE 2016) find emigration improves *source*-country institutions — relevant to Mexico's side of this counterfactual. And the channel from the *existing stock* (mostly citizens) to policy damage has no identified link; the counterfactual itself (removal or non-birth of citizens) is not institutionally well-defined.
- Innovation for this group specifically is likely modest (Hunt & Gauthier-Loiselle, AEJ:Macro 2010's 9–18% patents-per-capita effect per percentage point of immigrant *college* share is college-driven), but non-zero via G2/G3 and entrepreneurship.

---

## Claim 8 — "Irreversibility + thin sign-uncertain gain ⇒ fails the option-value hurdle; margin is future inflows"

**Verdict: the decision-theoretic framework is apt; the application is wrong in at least four ways, and the conclusion does not follow.** (Full assessment at the end.)

---

# Internal-consistency checks you asked for

**(i) Does λ double-count by hitting the whole other-residents line?** No — verified arithmetically. The scaled base is recoverable from the CSV: (384.513−340.643)/0.16 = (477.737−340.643)/0.5 = **274.19bn** (low end); (455.935−401.060)/0.16 = (572.546−401.060)/0.5 = **342.97bn** (high end). So λ hits ~80%/85% of the line — the fiscal component — while ~66/58bn of non-fiscal rows (crime VSL, congestion, care, wage/rent) are unscaled. That is the right architecture. Three residual double-count risks to verify in `world_ledger.py`: (1) if the fiscal account's revenue estimates already embed behavioral (taxable-income) responses, the λ−1 surcharge partially double-counts MEB; (2) the borrowed part must not bear λ (it carries interest already); (3) the +13.2bn induced taxes on the production gain must be scaled *symmetrically* if the gross cost is scaled — the identical base at both λ values suggests a consistent net base, but check.

**(ii) Is λ applied symmetrically to Mexico's fiscal side?** Mechanically yes: Mexico's base is (41.532−21.125)/0.16 = (84.896−21.125)/0.5 = **127.54bn** (low), 69.08bn (high). But symmetric in mechanism only: US-calibrated parameters are used for a country with >50% informality and a different instrument mix, and scaling Mexico's *budget savings* by λ assumes the marginal peso saved cuts distortionary taxes rather than restoring under-provided spending or paying down debt (λ ≈ 1 + interest on the latter). Also verify the short-run Mishra block and remittance rows are *not* scaled.

**(iii) Is R3 coherent (MMP pay parameter + R1's other choices)?** No, on current evidence: the implied annual ratio is 1.98 while the parameter is labeled *hourly* 2.0 against a measured annual-hours ratio of 0.795 — a ~$47bn inconsistency (claim 1a). Additionally: the wage *basis* of the MMP factor (take-home vs the ledger's grossed-up ENIGH), its PPP basis, and its vintage are undocumented in the excerpt; each is a several-percent lever. And R3 inherits average-cost public goods — a choice claim 3 itself disowns.

**(iv) Bonus checks.** Breakeven-w arithmetic verified (e.g., R1 equal low: (340.643+21.125)/646.729 = 0.5594 ✓; R1 λ_h low: 0.7373 ✓; R3 λ1.16 low: 0.8239 ✓). Group totals are invariant across weightings ✓ (λ hits payers only — consistent design). The headline's Hendren-weight R1 figures (284.2/288.2) are not in the subset — unverifiable here, but they are the welfare-consistent columns and should be in the claims.

---

# Material omissions, both directions

**Omitted gains (raise the world total):**
1. **G3+ premium** — all readings at the zero bound; up to +252.7bn at the upper bound. My defensible band: +60–130bn (¼–½ of upper). The zero bound assumes no US–Mexico wage gap for this group; it is a bound, not a central. Largest single omission.
2. **Counterfactual-Mexico victimization of the group.** The ledger charges US-side in-group victimization at DOT VSL (−28.9/−32.2) but, per the excerpt, never charges the Mexican victimization the same 44.9M people would face in the counterfactual. Mexico's homicide rate ~19–24/100k (INEGI/SESNSP 2023–24, hedge on exact figure) vs US ~5.5–6 → ~6–8k additional homicides/yr on 44.9M. At OECD-style VSL benefit-transfer (~$2–4M at Mexico's income): +$12–30bn; at US VSL: +$80–90bn. Asymmetric place-effect treatment — the crime analog of counting US wages but not Mexican ones. [Verify in code whether Mexico rows include this.]
3. **Leisure**: $19.2 + 13.7bn measured, reported beside, never added (+33bn at full weight).
4. **Consumer surplus to natives** from cheaper immigrant-intensive services (Cortes, JPE 2008: ~2% price decline per 10% low-skilled-immigrant labor-share increase): plausibly +$10–40bn/yr; check whether "rents" in the others line captures any of it.
5. **Agglomeration/scale** of a 13%-larger population; entrepreneurship (G2/G3); **emigration→source-institution** effects for Mexico (Docquier et al. 2016); remittance-financed investment returns (transfers counted, returns not). Each small; collectively material.
6. **SS/OASDI actuarial relief** from a younger population (SSA actuaries' and NAS 2017's finding that immigration improves the actuarial balance) — confirm the accrual rows capture it; the [DEGRADED] all-public P032 proxy at share 1 likely *overstates* the pension cost, an additional downward bias on the total.

**Omitted costs (lower the world total):**
1. **Mexico's absorption costs** in the counterfactual: +22.6% labor force requires housing and infrastructure beyond per-capita service scaling. Unpriced; maybe −$10–50bn.
2. **Intra-US spatial price overstatement** of the group's real US earnings: ~−$8–15bn (claim 2).
3. **Short-run/distributional native wage effects** beyond the long-run −0.7bn (Borjas, QJE 2003; the Mariel debate — Card 1990, Borjas 2017, Peri & Yasenov JOLE 2019): defensible to use the long run for a stock account, but the span belongs in the table.
4. **Housing/rent incidence** (Saiz, JUE 2007: ~1% rent increase per 1% immigration inflow): mostly a transfer within "others" (renters→landlords) at equal weights, but it moves the breakeven w and belongs on the distributional row.
5. **The political/institutional channel** (claim 7) — genuinely unpriced, sign-unknown.

**Both ways / framing:** the stock counterfactual removes 44.9M people including ~30M US-born — a controlled comparison, as the document concedes for G2, *not* a feasible history; US housing-stock revaluation at removal is a massive transfer with amplification externalities; Mexico's political absorption of 44.9M people (many dual nationals) is transformative and unpriced in both directions.

---

# My defensible central and range

Build-up on the oct16 R1 low-end equal reading (+284.96bn), with my defended adjustments (spans in parentheses):

| Adjustment | $bn |
|---|---|
| R1 equal, g3 = zero, average-cost public goods, λ = 1 | 285.0 |
| Public goods: midpoint of average/responsive conventions | −73 (0 to −146) |
| G3+: one-third of upper bound | +84 (0 to +253) |
| Leisure, half weight | +16 (0 to +33) |
| Counterfactual-Mexico victimization differential | +20 (+10 to +90) |
| Consumer surplus to natives | +10 (0 to +40) |
| Mexico absorption costs | −15 (0 to −50) |
| **Equal-weight central** | **≈ +327** |
| λ = 1.15–1.20 on the net fiscal-financing component only | −64 to −80 |
| **Central at λ ≈ 1.2** | **≈ +250bn/yr** |

**Range:** roughly **−250bn to +520bn/yr**. The bottom stacks R2's pay basis, full responsive-cost public goods, zero G3+, λ = 1.5, and maximal absorption costs — every least-defensible choice at once (note R2's basis is itself the weakest piece in the ledger: CMP's *high* selection bound plus the wrong welfare deflator). A judgmental "likely band" with each knob at a defensible interior position is **+$50 to +430bn**. The claims' "$45–170bn, central ~$100bn" occupies the bottom quarter of my range, because it adopts the low resolution of G3+ (zero), the high resolution of λ (a welfare-artifact 1.286), the mis-scaled R3 pay parameter, and silently keeps the average-cost phantom that partially offsets them.

# Does claim 8's conclusion follow?

**No.** The option-value framework (Arrow & Fisher, QJE 1974; Henry 1974; Dixit & Pindyck 1994) is the right decision theory, but the application fails four ways:

1. **The premise is not established.** "Thin and sign-uncertain" is claim 5's output, which does not survive the corrections above. My central is +$250bn at λ1.2 with the plausible band solidly positive; the remainder is 40–85% of the transfer under the best-anchored reading. You cannot invoke an irreversibility hurdle against an expected gain you have understated by stacking low resolutions of every knob.
2. **Most of the uncertainty is parametric, not resolvable.** Quasi-option value requires *learning by waiting*. The PPP basis, the selection percentile, the public-goods convention, and λ will not be revealed by delay; they generate risk adjustment, not option value. The genuinely resolvable uncertainties (institutional response, assimilation trajectories — where existing evidence on English convergence, intermarriage, and second-gen outcomes is already substantial) argue for *staged status design* (provisional admission, deferred permanence), not for the stock counterfactual this ledger prices.
3. **Irreversibility is not one-sided, and the reverse option is perishable.** Non-admission destroys a compounding, multi-generational asset: the existing stock's G2 premium alone is a ~$252bn/yr flow; per admitted family, the PDV of G1+G2 premia net of fiscal cost is plausibly high six figures, against a worst-case stacked reading of ≈ −$3.8k/person/yr (~−$170bn/44.9M). And delay has theta: Mexico's TFR is ~1.9, net Mexico–US migration was negative in 2009–2014 (Pew, Passel et al. 2015), and the supply of young Mexican workers is shrinking (Hanson & McIntosh, JEP 2016). The option to admit later decays every year. A symmetric option-value treatment needs a probability distribution and a learning structure; the claim supplies neither.
4. **The margin is mis-specified.** The ledger prices a *stock* counterfactual (mostly citizens; removal neither feasible nor legal), while the decision margin is *flows* of a different composition (recent Mexican inflows are older at arrival, more educated, and smaller; adult arrivals consume no US K–12 but also pay fewer lifetime taxes — NAS 2017's age-at-arrival results). The breakeven *w* and the option hurdle for a marginal 2026 cohort are different objects from anything computed here. If irreversibility is taken seriously, the instrument it argues for is visa/status design (Martin's dictum that nothing is more permanent than a temporary worker is the honest complication), not a conclusion drawn from the stock's ledger.

**Bottom line:** the ledger's architecture is better than the claims about it. The defensible statement is: sign not robust, central ≈ +$250bn/yr (λ ≈ 1.2), likely band +$50 to +430bn, with the two dominant open items being the G3+ premium (which the claims suppress) and the public-goods convention (which the claims concede but don't price). Claim 8's policy conclusion should be withdrawn pending a probability-weighted, learning-explicit re-analysis on the marginal cohort.
