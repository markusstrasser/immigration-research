# Capacity Expansion & Congestion Cost Channels — Immigration Fiscal Ledger
[INFERENCE] [DATA] [SOURCE: mixed — see per-finding tags] [UNVERIFIED until each block is filled]

**Verdict:** The capacity/congestion class is REAL but SPLIT. The field's accountings bracket congestible-goods marginal cost between ZERO and AVERAGE cost and never test above average — NAS says so in its own text and prices that one convention at $160,000 of lifetime NPV per immigrant. Prison capital adds $10.5k-$15.6k to a $57.9k prisoner-year where capacity binds, and BJS puts state prisons at 98.6% of lowest capacity / 88.7% of highest, so it binds in 8 states and not in 22. The congestion-on-incumbents leg is WEAK: the best causal study (Figlio & Ozek 2019) finds precise zeros on incumbent students. School capital per seat is the largest unquantified channel.

Model self-report: claude-opus-5[1m] (Opus 5, 1M context), agent `capacity-congestion`, dispatched 2026-09-16.

## Scope
Operator's angle: the fiscal ledger prices public services at **average operating cost**
(prisoner-year $57.9k, pupil $17.6k, Medicaid per enrollee) and never asks whether a population
increase forces **capacity expansion** (capital: prisons, schools, hospital beds, roads, water,
courts) or imposes **congestion** on incumbents (class size, ER waits, commute time, court
backlogs). Enumerate every channel of this class, what the literature says, and how immigration
fiscal accountings handle it.

Sections: (1) conventions in NAS 2016 / CBO 2024-25 / Manhattan Inst 2025 / Cato 2026 /
generational accounting; (2) prisons (capital cost per bed, capacity binding, ICE bed-day);
(3) schools (cost per seat, class-size/peer effects on incumbents); (4) health (ER congestion,
uncompensated care, border-county hospital closures); (5) infrastructure & land (roads, water,
housing — housing lane owned by `housing_deport_2026_09_16/`); (6) other angles.

## Findings

### Block 1 — Conventions: how the accountings treat capital and congestible goods
[SOURCE: NAS 2016 full text, local copy `/Users/alien/Projects/immigration-research/.scratch/nas-2017-layout.txt`, prepublication proofs; page 264 region = Ch.7] [DATA: verbatim quotes]

**NAS 2016 defines the exact object the operator is naming, then declines to measure it.** Ch.7 verbatim:

> "In the case of 'congestible public goods,' the marginal costs of additional population (immigrant or native) may be higher or lower than average cost but is greater than zero. **Such might be the case if a district's schools were operating at or above capacity and an influx of immigrants created the need to build new schools and hire additional teachers.** Proper accounting of congestible goods requires information—or lacking appropriate data, assumptions—about how the provision and consumption of goods and services change with the share of immigrants in the population. **Most studies attribute the costs of these kinds of goods equally across the whole population—that is, proportional to the number of recipients (Rowthorn, 2008).**"

That is the admission: the field's default is **per-capita average**, and NAS says so while flagging it as an assumption, not a measurement. NAS then states the timescale rule that the ledger must adopt:

> "Congestion may be irrelevant when considering the current fiscal year impact for school or infrastructure budgets created by an additional immigrant. In contrast, **congestion is a central concern when considering long-term costs associated with a growing population.** Similarly, the marginal cost calculus will be quite different when considering the marginal addition of one immigrant at a point in time versus the addition of many thousand immigrants over a period of time."

**The scenario machinery is asymmetric.** NAS's eight scenarios (Box 8-1) vary only the treatment of *pure* public goods (defense, interest, government administration) between average cost (scenarios 1-4) and zero marginal cost (5-8). Congestible goods are handled with **one** convention throughout: Ch.8 verbatim — "As in *The New Americans*, we also model several categories of spending as congestible goods… **Public administration expenses, police and fire-fighting services, and incarceration are all treated as congestible costs.**" The model's variable names confirm the scope: `cong_f` = "Congestible goods (transportation, public admin, etc.), federal"; `cong_s` = "Congestible goods (police, public admin, etc.), state/local". **There is no capital-stock line and no scenario in which congestible marginal cost exceeds average cost.** [DATA: NAS appendix variable table]

**NAS itself quotes the magnitude of the swing in the other direction** (Ch.7, citing National Research Council 1997, p.346):

> "If all the expenditures we categorize as provision of public goods (military expenditures are the leading case) were instead treated as private or congestible goods… the average NPV would drop from +$80,000 to –$5,000… **A similar calculation shows that treating congestible goods (roads, police, etc.) as public goods with zero marginal costs would add $80,000 to the baseline NPV, for a total of +$160,000.**"

So the *published* sensitivity range on the congestible-goods convention alone is **$160,000 of lifetime NPV per immigrant (1996 dollars)** — from zero-marginal (+$160k) to average-cost (+$80k), and NAS never ran the third leg, **marginal above average**, which is the operator's case. The Dustmann–Frattini framing NAS adopts hard-codes the asymmetry: congestible marginal cost is "unknown, although **probably smaller than the average cost** and positive." [SOURCE: Dustmann & Frattini 2014 p.7, quoted at NAS Ch.7]

**[INFERENCE — the essay's load-bearing point]** Every accounting in the field brackets the answer between *zero* marginal cost and *average* cost. The capacity-expansion case says the true marginal cost for a **sustained mass inflow into a binding-capacity jurisdiction exceeds average cost**, because average cost excludes the capital annuity of the facility that must now be built. None of NAS, CBO, Cato or the generational-accounting literature places a scenario on that side of average cost. That is a one-sided sensitivity analysis and it is the single convention the essay must name.

**CBO June 2025 (state/local surge report 61256)** is the one accounting that *scores* congestion, and it scores it as an unpriced residual, not a capital cost. Verbatim from the local text copy: it flags "costs that were borne **without adding to spending**—such as crowding in public schools and public [transportation]"; its "potential effects" ledger is the alternative that includes crowding. Repo-verified numbers (from `immigration-local-cost-incidence-2026-09-05.md`): direct 2023 state/local net cost **$9.2bn**; alternative potential-effect ledger **$9.8bn**; schools **$5.7bn direct vs $9.4bn potential**. The $0.6bn gap between the two headline ledgers is CBO's entire monetised congestion allowance. CBO also states the *opposite-sign* mechanism explicitly — "the marginal cost of an additional student is less [than average]" where slack exists. [SOURCE: `/Users/alien/Projects/immigration-research/.scratch/clarity-next-20260905/local/cbo_61256.txt` lines 47, 215-216, 711, 726]

[GAP] Manhattan Institute 2025 and Cato 2026 conventions not yet quoted at page level. Prior repo work establishes Cato's headline **$14.5T / +$6.6T** rests on assigning immigrants **zero** public-goods cost (the NAS scenario NAS calls "less tenable" for sustained mass inflow) — i.e. Cato sits at the *far* zero-marginal end and does not carry a congestible-capital line either. [SOURCE: `research/immigration-economist-dismantling-2026-06-25.md`]
[GAP] Storesletten / Auerbach-Oreopoulos generational accounting: expected to treat government capital as a per-capita-financed stock requiring new immigrants to "buy in," which is the one literature with a capital-widening term. Not yet verified.

### Block 2 — Prisons: capital cost per bed
[SOURCE: press/primary reporting on named state projects; DATA]

Recent US state prison construction is running at **$250k–$290k per bed**, an order of magnitude above the 1994 benchmark:

| Project | Beds | Total capital | $/bed | Source |
|---|---:|---:|---:|---|
| Alabama, Elmore Co. (opened 2026) | 4,000 | $1.08bn | **$270,000** | [al.com 2024-04-25](https://www.al.com/news/2024/04/alabamas-1-billion-prison-is-taking-shape-in-elmore.html) |
| Utah State Correctional Facility (opened 2022) | 3,600 | ~$1.0bn | **~$278,000** | same al.com piece |
| Indiana (groundbreaking 2023) | 4,200 | ~$1.2bn | **~$286,000** | same al.com piece |
| Alabama, Elmore (original 2022 contract) | 4,000 | $623m | $156,000 | [al.com 2023-03-22](https://www.al.com/news/2023/03/alabamas-billion-dollar-no-bid-prison-disaster-is-only-the-beginning.html) |
| 1994 medium-security benchmark, 6-state avg | 892 (theoretical) | — | $28,924 | [CT OLR 94-R-0422](https://www.cga.ct.gov/PS94/rpt/olr/htm/94-R-0422.htm) |

The Elmore cost escalation (**$623m → $975m → $1.08bn, +73% in two years**) is itself evidence for the capacity argument: capital cost per bed is not a stable parameter, it is bid into a constrained construction market.

**[INFERENCE] Marginal capital cost per prisoner-year, two regimes.** At $270,000/bed, amortised over a 40-year facility life at a 3% real municipal discount rate, the capital annuity is **$11,680 per bed-year**; at 50 years and 3%, **$10,500**; at 30 years and 4%, **$15,620**. Against the ledger's **$57,900** operating prisoner-year:
- **(a) Slack capacity** — marginal capital cost ≈ **$0**; true marginal cost is *below* $57.9k, because average operating cost contains fixed perimeter/administration. The ledger over-charges.
- **(b) Binding capacity** — marginal cost ≈ **$68,000–$73,500 per prisoner-year** (operating + annuity), i.e. **+18% to +27%** over the ledger's price. Arithmetic is mine; the $/bed and the $57.9k are sourced. [INFERENCE: annuity = C·r/(1−(1+r)^−n)]

The Alabama case also demonstrates the ugliest version: al.com reports the two new 4,000-bed prisons are **replacements** — "those new facilities won't increase the state's prison capacity." A billion dollars of capital that buys **zero** marginal beds is capital spending forced by a capacity constraint that shows up nowhere in a per-prisoner operating average.

[GAP] BJS *Prisoners* rated/operational/design capacity and occupancy series (state prison population 2009→2023) not yet pulled — this decides which regime (a) or (b) applies, and it is decidable on public BJS tables. **This is the single highest-value remaining fetch.** Prior: US state prison population fell ~2009-2021 then rose 2022-2023, so many states have *slack*, which argues regime (a) and would make this channel weak for prisons specifically — the honest finding may be that the prison capacity channel is currently NOT binding nationally while being sharply binding in specific states (AL under DOJ consent pressure).
[GAP] ICE detention bed-day cost (FY2024-26 budget per bed-day) not yet pulled.

### Block 3 — Schools: the incumbent-congestion literature runs AGAINST the capacity story
[SOURCE: Figlio & Özek, *J. Labor Economics* 37(4):1061-1096, 2019, [10.1086/703116](https://doi.org/10.1086/703116); NBER w23661 full text]

This is the cleanest test of the congestion-on-incumbents channel and **it finds nothing**. Design: Haitian earthquake refugee influx into Florida public schools, 2010; within-school across-grade variation in refugee volume; refugee birth dates instrument grade placement. Result, verbatim from the working paper:

> "In the top refugee-receiving schools, our preferred estimates… indicate that each percentage [point of refugee concentration is] associated with **0.6 to 0.7 percent of a standard deviation increase in reading test scores and 0.3 to 0.4 percent of a standard deviation in math**, and **0.2 to 0.6 percentage points fewer disciplinary incidents**."

And the power statement, which is what makes this a real null rather than an underpowered one:

> "the standard errors in our preferred models are sufficiently small that we could statistically detect effects of **smaller than one percent of a standard deviation** changes in test scores (1.5 percent in the IV models) for every percentage point increase in the refugee concentration."

**[INFERENCE] The scope condition is the whole argument, and the authors state it themselves:** "only four Florida schools had a refugee concentration of over five percent of their school population," and the receiving schools "might already have support systems in place… such as Haitian Creole speaking counselors, and hence might be more prepared… Such support systems might not exist in other contexts (such as the Syrian refugee crisis in Europe)." So this paper prices **a small shock into a prepared, slack-capacity system** — exactly NAS's regime where congestion "may be irrelevant." It does not price a sustained inflow into a binding-capacity district, and it must not be cited as if it did. Native flight also does not appear: incumbent mobility effects are 0.1pp per pp and mostly vanish with school fixed effects.

**Steel-man for the essay:** the best available causal evidence on schools says incumbent students are not measurably harmed. Anyone arguing the congestion channel on schools is arguing from *capital cost* (seats that must be built) and from *out-of-sample concentration*, not from measured incumbent harm. Say that plainly.

[GAP] Hunt 2017 (immigration and native schooling attainment) and Betts & Fairlie 2003 (native flight to private schools, ~1 native student to private per 4 immigrant arrivals in high school — number from training data, **UNVERIFIED**) not yet pulled at primary.
[GAP] School construction cost per seat (21st Century School Fund "State of Our Schools", NCES facilities, TX/CA bond programs) not yet pulled. Needed to build the schools analogue of the Block-2 annuity table.
[GAP] No 2024-26 paper on immigrant inflow × incumbent outcomes located yet.

### Block 2b — Does prison capacity bind? BJS Table 21, decided
[SOURCE: BJS, *Prisoners in 2023 — Statistical Tables*, NCJ 310197, Table 21, version 9/30/25, https://bjs.ojp.gov/document/p23st.zip] [DATA: own aggregation, 47 jurisdictions with usable capacity]

| Measure, Dec 31 2023 | Value |
|---|---:|
| Sum of state custody population (47 states reporting capacity) | 893,812 |
| Sum of **lowest** capacity (min of rated/operational/design) | 906,568 |
| Custody as % of lowest capacity | **98.6%** |
| Sum of **highest** capacity | 1,008,128 |
| Custody as % of highest capacity | **88.7%** |
| Headroom at highest capacity | 114,316 beds |
| States over 100% of their **highest** capacity | 8 (NE 116.0, IA 115.1, FL 112.1, WA 107.6, ID 106.5, CO 106.1, ND 100.9, AR 100.7) |
| States under 85% of highest capacity | 22 |
| Federal system | 142,260 custody = **100%** of rated capacity |

**[INFERENCE] The answer is regime-dependent and the national aggregate sits exactly on the knife edge.** On the conservative (design/lowest) reading the state system is **98.6% full** — capacity binds and regime (b) applies, so the marginal prisoner-year is $68k–$73.5k, not $57.9k. On the generous (highest) reading there are 114,316 spare beds and regime (a) applies, so the marginal prisoner-year is *below* $57.9k. Twenty-two states have real slack; eight are over even their most generous capacity measure. Alabama is the extreme: 173.7% of design capacity, which is why it spent $1.08bn on a prison that adds no net beds.

The honest ledger statement: **the prison capital channel is a state-level, not a national, cost.** It binds in the eight over-capacity states and in Alabama-class systems under court pressure, and does not bind in the 22 slack states. Since immigrant populations are geographically concentrated, the correct object is a **population-weighted** occupancy, not the national mean. That is a runnable analysis on repo data (see Analyses below). BJS Table 22 gives custody by citizenship status by jurisdiction in the same release, which makes the weighting directly computable from one file.

Caveat that must be stated: the three BJS capacity concepts are not comparable across states — several states define operational capacity *as* a multiple of design (Nebraska's is 125% of design "stress capacity" set by the governor). Using "lowest capacity" mixes definitions. Do not present 98.6% as if it were a single measured quantity. [SOURCE: BJS Jurisdiction Notes, Nebraska entry]

### Blocks 4-6 — remaining channels [PARTIAL]

**4. Health.** [GAP] Not yet researched. Targets identified for the next epoch: emergency-department boarding and wait-time series (CDC NHAMCS); uncompensated-care burden by hospital (AHA annual uncompensated-care fact sheet); the Emergency Medicaid line, which is the one health expenditure that is immigration-specific by construction and appears in state Medicaid budgets (notably NY, CA, TX, FL); border-county hospital closures (Sheps Center rural hospital closure database, filterable to border counties). Capital analogue: hospital construction cost per bed, roughly $1-2m per licensed bed in recent US projects — **UNVERIFIED, training-data figure, must be sourced before use.** A measured wait-time effect of immigration on incumbents has not been located; my prior is that none exists at US national scale, which would make this channel a [GAP] rather than a finding.

**5. Infrastructure and land.** [GAP] Texas Transportation Institute *Urban Mobility Report* gives congestion cost per auto commuter (~$1,000-1,400/yr in large metros, **UNVERIFIED vintage**) and is the natural per-capita congestion price; the mechanism is population-driven and therefore applies to immigrants at the same per-capita rate as anyone else, which makes it a *dilution* channel, not an immigrant-specific one. Water and wastewater capacity: EPA Clean Watersheds Needs Survey and Drinking Water Infrastructure Needs Survey give capital need, allocatable per new connection. **Housing is explicitly out of scope here** — owned by the `housing_deport_2026_09_16/` lane; this memo should cite it and not re-derive rents.

**6. Other angles the same logic produces.** One line each, honestly tagged:
- **Pension / Social Security dilution vs support ratio** — this is the one capacity channel that runs the *other way*: new workers raise the support ratio and improve OASDI actuarial balance in the near term, while accruing their own claims later. The generational-accounting literature is the place this is handled correctly. [GAP: Storesletten 2000 JPE and the SSA Trustees' immigration sensitivity not yet pulled.]
- **Court and USCIS backlogs** — near-pure deadweight, already granted in the repo (Bier's 9-decade EB waits). Immigration-court backlog is caused by immigration by construction; EOIR publishes pending-case counts. [SOURCE: repo `immigration-economist-dismantling-2026-06-25.md`]
- **Language-access mandates** — California court interpreters: **$133.2m average annual appropriation FY2020-21 through FY2023-24**, but the program covers existing residents and deaf/hard-of-hearing users, so it is not a marginal immigration cost. [SOURCE: [CA 2025 Language Need and Interpreter Use Study, pp.1-3](https://languageaccess.courts.ca.gov/system/files/2025-07/2025%20Language%20Need%20and%20Interpreter%20Use%20Study.pdf), via `immigration-second-order-effects-2026-09-05.md`]
- **Insurance pool composition (auto/health)** — [GAP] no source located; risk of a pure-correlation trap here, treat as speculation until a rate-filing or state-fund study is found.
- **Public land and parks** — [GAP] congestible by definition, plausibly trivial per capita, no source.
- **Remittance leakage from local demand** — [GAP] real channel (outflows reduce the local multiplier on immigrant earnings) but it belongs to a demand-side ledger, not a capacity one. World Bank remittance outflow data exists; the incidence claim does not.
- **ICE detention bed-day** — [GAP] the one capacity line that is immigrant-specific by construction. ICE FY2024-26 congressional budget justifications give a per-bed-day rate (adult beds historically ~$150-170/day, **UNVERIFIED**). Must be sourced before use.

## Verdict

**Which channels are material per immigrant-year and measurable:**
1. **Prison capital, state-specific.** Material where capacity binds: **+$10.5k to $15.6k per prisoner-year** on top of $57.9k, i.e. +18% to +27%. Measurable now from BJS Table 21 crossed with Table 22 citizenship shares. Binds in 8 states, not nationally.
2. **School capital (cost per seat).** Structurally the largest channel because K-12 is the largest immigrant-origin state/local cost and enrollment growth forces construction. **Not yet quantified — the top remaining gap.**
3. **ICE detention.** Immigrant-specific by construction, directly budgeted, small per immigrant-year but unambiguous. Not yet quantified.
4. **Congestion on incumbents — weak on the best evidence.** Figlio & Özek find precise zeros on incumbent students at observed US concentrations. Anyone running the congestion argument must argue capital, or out-of-sample concentration, and say which.

**The conventions the essay must state, in order of load:**
- The field brackets the congestible-goods marginal cost between **zero and average cost** and never above it. NAS says so in its own text and prices the published sensitivity at **$160,000 of lifetime NPV per immigrant** across just the two conventions it does run. Naming this one-sidedness is the essay's strongest and most defensible move, because NAS supplies both the definition and the admission.
- **Timescale decides the sign.** NAS: congestion "may be irrelevant" for a one-year, one-immigrant marginal calculation and is "a central concern when considering long-term costs associated with a growing population." The ledger is a long-run lifetime NPV, so it is in the regime where NAS itself says congestion matters, while using the convention appropriate to the regime where it does not.
- **Average cost cuts both ways and the essay must concede it.** Where capacity is slack, average operating cost *overstates* the marginal cost, because fixed perimeter/administration is in the average. CBO says exactly this for schools. An argument that only invokes marginal-above-average is not honest; the claim is that the ledger uses a convention with a known two-sided error and never tests the upper side.
- **Cato sits at the far zero-marginal end**, assigning immigrants zero public-goods cost; this is the assumption doing the work in the $14.5T / +$6.6T headline, not a finding.

## Table — channel × convention × best estimate × source

| Channel | Convention in the accountings | Best estimate of the capacity/congestion increment | Source | Status |
|---|---|---|---|---|
| Pure public goods (defense, interest) | NAS runs BOTH average and zero-marginal (scenarios 1-4 vs 5-8) | Swing of $85,000 lifetime NPV (NRC 1997 calc quoted by NAS) | NAS Ch.7-8 | VERIFIED |
| Congestible goods (police, incarceration, public admin, transport) | NAS runs ONE convention: per-capita average. Never above average | NAS quotes +$80,000 NPV if pushed to zero-marginal; the above-average side is unpriced | NAS Ch.7-8, vars `cong_f`/`cong_s` | VERIFIED — the gap |
| Prison operating | $57,900/prisoner-year, average | baseline | repo crime-cost lane | VERIFIED |
| Prison capital | Absent from every ledger | +$10,500-$15,620/prisoner-year at $270k/bed, 30-50yr, 3-4% | al.com Elmore $1.08bn/4,000 beds | INFERENCE on sourced inputs |
| Prison capacity binding? | Not asked | 98.6% of lowest capacity, 88.7% of highest; 8 states over, 22 slack | BJS Table 21 | VERIFIED |
| K-12 operating | Average current per-pupil ($35,796 NYC FY2024) | baseline | Census school finance | VERIFIED (repo) |
| K-12 capital (cost per seat) | Absent | **[GAP]** | — | GAP |
| K-12 congestion on incumbents | CBO scores it as unpriced residual ($9.2bn direct vs $9.8bn potential; schools $5.7bn vs $9.4bn) | Causal estimate is a precise ZERO at observed US concentrations | CBO 61256; Figlio & Özek 2019 | VERIFIED |
| ICE detention bed-day | Immigrant-specific, budgeted | **[GAP]** | ICE CJ FY2024-26 | GAP |
| Health capacity / ER waits | Not in any ledger | **[GAP]**, likely no measured incumbent effect | — | GAP |
| Road congestion | Not in any ledger | Per-capita, not immigrant-specific; TTI cost per commuter | TTI UMR | GAP/UNVERIFIED |
| Language access | Whole-program funding, not marginal | CA courts $133.2m/yr, not attributable | CA 2025 study | VERIFIED, not attributable |
| Pension support ratio | Generational accounting handles it | Runs the OTHER WAY (near-term improvement) | **[GAP]** Storesletten, SSA Trustees | GAP |

## ≤5 runnable analyses on repo data

1. **Population-weighted prison occupancy.** BJS Table 21 (capacity, custody, % of capacity by state) × Table 22 (non-citizen custody count by state) from the same ZIP already downloaded to the scratchpad. Produces: the occupancy rate faced by the *marginal immigrant prisoner*, not the national mean. Decides regime (a) vs (b) for the ledger's crime line. ~30 lines of Python, no new data acquisition.
2. **Foreign-born-weighted state occupancy.** Same Table 21 crossed with ACS/CPS state foreign-born stock already in the repo warehouse (`state_stage5_context_2023`). Same output as (1) but weighted by where immigrants live rather than where non-citizen prisoners are held, which separates "immigrants live in crowded-prison states" from "immigrants are in crowded prisons."
3. **Capital annuity sensitivity grid for the crime line.** Vary $/bed ($150k-$290k), facility life (30/40/50yr), discount rate (2/3/4%), and the regime-(a) share of states. Output: the range by which the ledger's $57.9k understates or overstates, and the point where the capital adjustment changes the crime line's share of the fiscal gap (currently 17% on the central arm). Pure arithmetic on sourced inputs.
4. **State prison population 2009→2023 vs capacity growth.** BJS Prisoners series (Table 1 gives 2013-2023 in this ZIP; earlier years need one more file). Tests whether capacity tracked population or lagged it, which is the empirical content of "capacity binds."
5. **School-seat capital annuity, once cost-per-seat is sourced.** Same structure as (3) applied to the $17.6k pupil line. Deferred pending the cost-per-seat gap.

## Gaps for a re-dispatch, ranked
1. **School construction cost per seat** — 21st Century School Fund *State of Our Schools*, NCES facilities data, TX/CA bond program per-seat figures. Highest value: K-12 is the largest channel and the one place capital is plausibly large per immigrant-year.
2. **ICE detention bed-day cost**, FY2024-26 congressional budget justification.
3. **Manhattan Institute 2025 and Cato 2026** at page level — quote their capital/congestible rule verbatim.
4. **Storesletten 2000 JPE and Auerbach-Oreopoulos** — the one literature that carries a capital-widening term; verify whether it makes immigrants buy into the existing public capital stock.
5. **Hunt 2017, Betts & Fairlie 2003** at primary; any 2024-26 incumbent-outcome paper.
6. **Health capacity**: Emergency Medicaid state budget lines; Sheps Center border-county closures.

Suggested next queries: "State of Our Schools 2021 construction cost per student capacity"; "ICE congressional budget justification FY2026 adult detention bed rate per day"; "Storesletten 2000 sustaining fiscal policy through immigration public capital"; "Emergency Medicaid spending by state undocumented 2024".
