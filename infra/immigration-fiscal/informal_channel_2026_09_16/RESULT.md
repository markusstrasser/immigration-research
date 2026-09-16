# Informal-economy channel — immigrant under-the-table work, fiscal & competitive effects

**Verdict:** **MATERIAL BUT SMALLER THAN THE LEDGER GAPS, AND FIRST-GENERATION-ONLY (with one measured
exception).** The best-anchored per-adult arithmetic puts the *net* uncredited-tax loss from
off-the-books unauthorized work at roughly **$1.5k–$3.4k per unauthorized adult per year** — real,
but 13–29% of the −$11.5k Mexico-born gap, and it moves that gap in the direction the ledger already
points (worse), not enough to flip any sign. For the **US-born second generation the channel is
approximately zero on the tax side**: they hold SSNs, are covered by W-2 withholding, and the only
mechanism that survives into generation 2 is *system avoidance* in mixed-status families, which is
measured, statistically significant, and small in dollar terms.

Model self-report: claude-opus-5[1m] (Claude Opus 5, 1M context), researcher subagent, 2026-09-16.

---

## 1. Size of the unreported-earnings channel by status/nativity

### 1a. SSA: what IS credited (the visible part)

| Quantity | Value | Year | Source |
|---|---|---|---|
| Unauthorized immigrants **working and paying** OASDI payroll taxes | 3.1 million | 2010 | [SOURCE: https://www.ssa.gov/oact/NOTES/pdf_notes/note151.pdf — SSA OCACT Actuarial Note 151, Goss, Wade, Skirvin, Morris, Bye & Huston, April 2013] |
| Unauthorized working **in the underground economy** (no payroll record at all) | **3.9 million** | 2010 | [SOURCE: same, Note 151] |
| Unauthorized using an SSN that does not match their name (→ ESF) | 1.8 million (→3.4M by 2040) | 2010 | [SOURCE: Note 151] |
| **Total unauthorized workers** | 7.0 million | 2010 | [SOURCE: CRS IF10820, citing Note 151 — https://www.everycrsreport.com/files/2018-02-06_IF10820_fda861a7c48b35a75f070a0edd834699e9b6b784.pdf] |
| Payroll taxes from unauthorized workers **and their employers** | **$13 billion** | 2010 | [SOURCE: Note 151] |
| Net trust-fund gain (taxes in minus benefits out) | **$12 billion** (after $1B benefits) | 2010 | [SOURCE: Note 151; confirmed PolitiFact 2016-08-10] |
| Assumed avg OASDI taxable earnings of these workers | **80% of the all-worker average** ≈ $34,000 | 2010 | [SOURCE: Note 151; $34k figure via PolitiFact restatement of SSA] |

**This is the single most decision-relevant number in the whole probe:** SSA's own actuaries put
**3.9M / 7.0M = 56% of unauthorized workers entirely off the books** in 2010, with **44% on payroll**
(3.1M). That is the primary-source replacement for the repo's `[TRAINING-DATA]` row at
`research/immigration-fiscal-impact-unauthorized-memo.md:152` ("50-75% pay via ITIN or mismatched
SSN"), which is **too high by SSA's own accounting** — SSA says 44%, not 50-75%. **The existing repo
row should be corrected.**

### 1b. SSA Earnings Suspense File (the mismatched-but-taxed part)

| Quantity | Value | Year | Source |
|---|---|---|---|
| ESF cumulative uncredited wages | $1.2 trillion / 333M W-2s | TY1937–2012 | [SOURCE: https://oig-files.ssa.gov/audits/full/A-03-15-50058.pdf — SSA OIG A-03-15-50058, Sept 2015] |
| ESF cumulative | $1.5 trillion / 360M wage items | TY1938–2016 | [SOURCE: CRS IF10820, Feb 2018] |
| ESF **annual flow** | ~8.9M wage items, **$98 billion in wages** | TY2016 | [SOURCE: CRS IF10820] |
| ESF annual flow | 7.3M reports, $70.3B | 2010 | [SOURCE: Senior Citizens League table sourced to SSA — https://seniorsleague.org/growth-of-the-social-security-earnings-suspense-file-points-to-the-rising-potential-cost-of-unauthorized-work-to-social-security-2/ — B-grade, secondary compilation] |
| Share of ESF W-2s suspended for **name/SSN mismatch** | 95% | TY2008–2012 | [SOURCE: SSA OIG A-03-15-50058] |
| ESF W-2s with **ITIN-shaped** invalid SSNs | 637,000 W-2s / **$8 billion wages** | TY2008–2012 | [SOURCE: SSA OIG A-03-15-50058] |
| ITINs issued since 1996 | ~21 million, **only one-quarter used on tax returns** | as of June 2014 | [SOURCE: SSA OIG A-03-15-50058, citing IRS] |

**[GAP]** The ESF is *not* an unauthorized-work meter. GAO is explicit: "the portion of these
earnings that represent unauthorized work is unknown," and "most reinstatements are still made to
U.S.-born citizens" [SOURCE: https://www.govinfo.gov/content/pkg/GAOREPORTS-GAO-06-814R/pdf/GAOREPORTS-GAO-06-814R.pdf — GAO-06-814R]. Foreign-born share of reinstatements rose 8% (1986) → ~21% (2003), Mexico
the largest single origin. **Do not use ESF totals as an unauthorized-earnings estimate.** Note 151
itself says SSA cannot identify which wage items are unauthorized. SSA's own bound: ESF earnings for
unauthorized immigrants rise from **<1% of total taxable payroll in 2000 to ~2% by 2040**.

### 1c. IRS tax gap — the self-employment / no-information-reporting channel

The mechanism that carries informal earnings is **income not subject to information reporting**.

| Quantity | Value | Year | Source |
|---|---|---|---|
| Net misreporting % — wages/salaries (W-2 withheld) | **1%** | TY2014–2016 | [SOURCE: https://www.irs.gov/pub/irs-pdf/p5784.pdf — IRS Pub 5784, Table 2-3] |
| Net misreporting % — substantial info reporting, no withholding | 6% | TY2014–2016 | [SOURCE: Pub 5784] |
| Net misreporting % — **little/no info reporting (incl. nonfarm proprietor)** | **55%** | TY2014–2016 | [SOURCE: Pub 5784 / Pub 1415] |
| Net misreporting % — **nonfarm proprietor income specifically** | **57%** | TY2014–2016 | [SOURCE: Pub 5784, Table 2-4] |
| Nonfarm proprietor underreporting tax gap | $80B (TY14–16) → $110B (TY21) → **$117B (TY22)** | various | [SOURCE: Pub 5784; https://www.irs.gov/pub/irs-prior/p5869--2023.pdf; https://www.irs.gov/pub/irs-pdf/p5869.pdf] |
| Gross tax gap | $688B (TY2021), $696B (TY2022) | — | [SOURCE: IRS Pub 5869] |

**The 1% vs 57% contrast is the load-bearing fact for the ledger.** A worker on a W-2 — even a
fraudulent-SSN W-2 posted to the ESF — has payroll and income tax *withheld at source* and loses
almost nothing to underreporting. A worker paid cash as a de-facto proprietor loses a majority of
it. So the fiscal damage is concentrated in SSA's 3.9M "underground economy" group, not in the 3.1M
on payroll. **[GAP] IRS publishes no tax-gap breakdown by nativity or immigration status** — none
exists; the 57% is the generic benchmark and must be applied as an assumption, not a measurement.

### 1d. ITIN filers / taxes actually paid

| Quantity | Value | Year | Source |
|---|---|---|---|
| Total federal+state+local taxes paid by undocumented immigrants | **$96.7 billion** ($59.4B federal, $37.3B state/local) | 2022 | [SOURCE: https://itep.org/undocumented-immigrants-taxes-2024/ — ITEP, July 2024] |
| Per person | **$8,889** | 2022 | [SOURCE: ITEP 2024] |
| Undocumented population base | 10.9 million | 2022 | [SOURCE: ITEP 2024] |
| Payroll/social-insurance taxes they cannot draw on | $33.9B total ($25.6B Social Security, $6.4B Medicare, $1.8B UI) | 2022 | [SOURCE: ITEP 2024; Immigration Research Initiative restatement] |
| Federal income tax | $19.5B | 2022 | [SOURCE: ITEP 2024] |
| Revenue gain if granted work authorization | **+$40.2 billion/yr** ($96.7B → $136.9B) | 2022 basis | [SOURCE: ITEP 2024] |
| State/local income tax under legalization | $7.0B → **over $11B** | 2022 basis | [SOURCE: https://itep.org/what-state-and-local-taxes-do-undocumented-immigrants-pay/, Sept 2025] |

**The $40.2B legalization delta is the cleanest available price tag on the informality channel**, and
ITEP is explicit that it comes from two sources: higher wages *and* higher compliance ("no longer
forced to work off the books"). $40.2B / 10.9M = **$3,688 per undocumented person per year** as the
*upper bound* of the whole channel, since it bundles the wage gain with the compliance gain.
**[FRAMING-SENSITIVE]** ITEP is an advocacy shop; the $96.7B is widely cited and methodologically
transparent (incidence model on Pew-style residual population estimates), but the legalization
counterfactual embeds a behavioral assumption ITEP does not identify causally.

### 1e. Off-the-books share — the direct evidence

**[VERIFIED NEGATIVE]** There is **no direct survey measurement** of the share of unauthorized workers
paid off the books. Every published number is a model residual. SSA's 3.9M/7.0M = **56%** (2010) is
the best-sourced figure and it is an actuarial imputation, not an observation. An independent 2026
audit reaches the same conclusion: "there is no reliable, published count of how many undocumented
workers are paid entirely off the books" [SOURCE: https://factually.co/fact-checks/labor/how-many-undocumented-workers-paid-off-the-books-1b324b, 2026-01-30 — C-grade aggregator, cited only for the negative].

Pew (Passel & Cohn) measures **presence**, not payment mode: 8.0–8.3M unauthorized in the labor force
2007–2014, 5.1% of the labor force (2012), 4.8% (2016); concentrated in farming 26%, cleaning/
maintenance 17%, construction 14%, landscaping services 24%, private household 23%
[SOURCE: https://www.pewresearch.org/race-and-ethnicity/2015/03/26/testimony-of-jeffrey-s-passel-unauthorized-immigrant-population/; https://www.pewresearch.org/race-and-ethnicity/2018/11/27/unauthorized-immigrant-workforce-is-smaller-but-with-more-women/].

**Generic informality benchmark (all US, not immigrant-specific):** 53% of urban fathers and 32% of
urban mothers with young children did informal work over a nine-year window; informal work usually
*accompanies* regular work rather than replacing it [SOURCE: Gunter 2016, "Dynamics of Urban Informal
Labor Supply in the United States," Fragile Families panel — https://pmc.ncbi.nlm.nih.gov/articles/PMC5400111/].
This is the correct disconfirmer to hold: **informality is not an immigrant phenomenon**; it is a
low-wage-labor-market phenomenon that immigrants are over-exposed to by status.

---

## 2. Competitive effects on compliant firms

### 2a. The one clean effect size (construction misclassification)

**Ormiston, Belman, Hinkel + a professional cost estimator (ICERES, June 2025).** Real architectural
plans, 67-unit multi-story residential, Ann Arbor MI, costed in RSMeans:

| | Value | Source |
|---|---|---|
| Project cost, legal non-union contractor | $13,449,363 | [SOURCE: https://faircontracting.org/wp-content/uploads/2026/02/ICERES-Research-Brief-Worker-Misclassification-June-2025-FINAL.pdf] |
| Project cost, contractor misclassifying entire workforce | $12,795,020 | same |
| Illegal cost advantage | **$654,343 = 4.9% of total project cost, 16.1% of labor cost** | same |

The 4.9% is evasion of **workers' comp premiums + the employer share of Social Security and
Medicare only**. It excludes wage theft, which the authors say is *more* common on cash jobs. This is
the first research-based bid-advantage number in this literature — the authors say the claim "has
never been supported by research-based findings" before. **Grade: B+.** Advocacy-adjacent publisher
(faircontracting.org), but the method is transparent, replicable, and uses the industry-standard
cost database; the counterfactual is an engineering calculation, not a regression.

**State corroboration:** 11–21% of Tennessee construction workers are misclassified or unreported;
law-abiding contractors pay "several hundred dollars per worker" in cost-shifted uncompensated
medical care for underground firms' employees [SOURCE: Canak & Adams, "Misclassified Construction
Employees in Tennessee" — https://stoptaxfraud.net/wp-content/uploads/2018/11/TN-payroll-fraud-study-1-15-10.pdf].

**[FRAMING-SENSITIVE]** Note what the 4.9% is *not*: it is a misclassification effect, not an
immigrant effect. The brief never identifies the workforce as immigrant. Attributing it to immigration
requires the separate premise that immigrant-heavy firms misclassify at higher rates, which this
source does not establish.

### 2b. The wage evidence points the OTHER way

This is the most important disconfirmation in the probe. **Hotchkiss, Quispe-Agnoli & Ríos-Avila**
used Georgia UI administrative records (Employer File + Individual Wage File, 1990Q1–2006Q4, ~178M
observations, covering 99.7% of wage/salary workers; undocumented identified by invalid SSN on
payroll):

| Finding | Effect size | Source |
|---|---|---|
| +1pp undocumented share in worker's **county/industry** | documented worker wages **+0.44%** | [SOURCE: https://doi.org/10.1002/soej.12020 — Southern Economic Journal, 2015] |
| +1pp undocumented share **within the firm** | **+0.09%** (+0.11/+0.12/+0.04 low/med/high-skill) | same |
| Working at a firm that hires undocumented vs one that doesn't (FE spec) | **−0.15%** | [SOURCE: FRB Atlanta WP 2012-4, https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2060667] |
| Same, alternative spec | **+0.54%** (≈$185/yr) | [SOURCE: earlier draft, https://economics.ucr.edu/wp-content/uploads/2019/10/Hotchkiss-paper-for-2-16-11-seminar.pdf] |
| Worst case: agriculture, 90th-pct firms (≥20% undocumented) | **−3%** (<$300/quarter) | [SOURCE: FRB Atlanta WP 2012-4] |
| Largest sectoral penalty | −1.7% professional & business services (≈$192/quarter) | same |
| Average undocumented share at firms that hire them | 3.24% (full sample) / ~11% (conditional spec) | same |

**Every specification is under 1% in absolute value**, and the sign flips across specifications —
the authors themselves call the magnitudes "questionable" and "negligible." They attribute the
positive results to Peri–Sparber task specialization. **A channel that moves documented coworkers'
wages by ±0.5% cannot be doing large competitive damage through the wage margin.** The damage, if it
exists, runs through *tax and insurance evasion* (§2a), not through wage undercutting.

**Chassamboulli & Peri 2015** (Review of Economic Dynamics 18(4):792–821; NBER w19932) models the
mechanism formally: unauthorized workers have worse outside options → lower wages → higher firm
surplus per vacancy → more job creation. Simulated: a 50% cut in unauthorized population via
deportation **raises** unskilled native unemployment by 1.13% of its initial value (1.6% in the
revision) and cuts native wages 0.08%; legalization **cuts** native unemployment 1.31% (4% in the
revision), raises native wages 0.19%, and raises income per native +0.45%
[SOURCE: https://www.nber.org/papers/w19932; https://doi.org/10.3386/w19932]. **This model has no
compliant/noncompliant firm distinction** — the cost advantage accrues to all hiring firms via
bargaining, not to rule-breakers via evasion. **[GAP]** No paper found that models compliant-vs-
noncompliant firm competition with immigrant labor as the input. That is a genuinely open seam.

---

## 3. Is it a first-generation channel? — YES, with one measured exception

**Mechanism-by-mechanism, for US-born second-generation workers (who hold valid SSNs from birth):**

| Mechanism | 1st-gen unauthorized | US-born 2nd gen | Why |
|---|---|---|---|
| ESF / mismatched-SSN wage posting | YES (1.8M, 2010) | **NO** | Requires a name/SSN mismatch. A US-born citizen's W-2 matches the Numident. |
| ITIN filing instead of SSN | YES (~21M issued, 25% used) | **NO** | ITINs are issued only to people ineligible for an SSN. |
| Employer-side evasion of employer FICA/workers'-comp | YES | **Possible but not status-driven** | Misclassification is a firm choice; it can hit any worker, citizen or not. |
| Fully off-the-books cash pay | YES (3.9M, 56%, 2010) | **Sharply reduced** | The binding constraint is inability to produce work authorization, which disappears at birth. |
| Self-employment underreporting (57% NMP) | YES | **YES, at the population rate** | Applies to every US proprietor. Not an immigration channel. |
| **System avoidance of formal employment** | YES | **YES — measured** | See below. |

**The one real second-generation channel is measured and it is small.** Desai, Su & Adelman (2019),
using the Immigration and Intergenerational Mobility in Metropolitan Los Angeles survey (n=3,283
adult children), find that **adult US-born children of unauthorized parents are significantly more
likely to avoid "surveilling" institutions — explicitly including formal employment — than adult
children of authorized parents**, while showing *no* difference in attachment to non-surveilling
institutions (community groups, religious organizations)
[SOURCE: https://doi.org/10.1177/0197918319885640 — "Legacies of Marginalization," Journal of
Immigrant & Refugee Studies / International Migration Review series, Dec 2019]. The discriminant
validity here is unusually good: the effect is specific to record-keeping institutions, which is
what the deportation-fear mechanism predicts. **[GAP] The paper reports no dollar figure and no
informal-earnings quantity** — it is a participation/avoidance count model (Poisson + propensity
weighting), so it establishes the channel's existence in generation 2 but does not price it.

Supporting but weaker: qualitative work documents US-born and 1.5-generation Latino youth working
informally *alongside unauthorized parents* (house cleaning, day labor), often unpaid as family labor
[SOURCE: https://ejournals.eu/pliki_artykulu_czasopisma/pelny_tekst/a7634c85-e45b-4f4e-b36d-46929c91f6ab/pobierz]. And Rubalcaba et al. find ICE-arrest shocks raise US-born Hispanic youth labor-force
participation by **6pp** and hours by **15%** in mixed-status families, an added-worker effect lasting
2–3 months [SOURCE: https://econ.vt.edu/content/dam/econ_vt_edu/seminars/spring-2025/2-28-25%20Jaoquin%20Rubalcaba%20Paper.pdf].

Contrary evidence on generation-2 informality: the Mollenkopf/Kasinitz/Waters second-generation New
York study found that among second-generation Chinese respondents "only a few reported having worked
off the books," while West Indian respondents more commonly had
[SOURCE: https://www.levyinstitute.org/wp-content/uploads/2024/02/wp214.pdf]. Small pilot samples,
no rates — cited as texture, not evidence.

**[VERIFIED NEGATIVE] No study measures informal or off-the-books employment by immigrant generation
with population-representative data.** CPS, SIPP and ACS have no informality item; the Fragile
Families informal-work module (Gunter 2016) is not tabulated by generation. This is a real hole and
it means the second-generation sign must be *assumed*, not measured.

---

## 4. Priceable? — Yes, as a bounded per-adult line. Here is the arithmetic.

### Line (i) — first generation, unauthorized adult

Build it from SSA's own decomposition rather than from ESF totals.

```
Off-the-books share (SSA OCACT)          s  = 3.9M / 7.0M = 0.557          [Note 151, 2010]
Avg earnings if on payroll               E  = $34,000  (80% of all-worker avg)  [Note 151, 2010]
Off-books earnings discount              d  = 0.80  (cash work pays less)   [ASSUMPTION — unmeasured]
Combined employee+employer FICA          f  = 0.153
Effective federal+state income tax at    t  = 0.08   [ITEP effective-rate territory]
  this income level after EITC-ineligibility

Per off-the-books worker, taxes NOT collected:
  0.80 x 34,000 x (0.153 + 0.08) = 27,200 x 0.233     = $6,338
Spread over ALL unauthorized workers (only 55.7% are off-books):
  0.557 x 6,338                                        = $3,530 per unauthorized WORKER

Netting: the ESF/on-payroll group ALREADY pays and is ALREADY counted in the ledger's
tax side, so there is nothing to net there. What must be netted is the benefit
liability SSA never pays out on suspended earnings ($1B against $13B in 2010, i.e.
the on-payroll group is a +$12B net contributor, already in ITEP's $96.7B).

Per-ADULT (not per-worker): unauthorized labor-force participation ~ 0.70 of adults
  0.70 x 3,530                                         = $2,471 per unauthorized ADULT/yr
```

**Cross-check against ITEP's legalization counterfactual:** $40.2B / 10.9M = **$3,688 per person**,
which *includes* children and *includes* the wage gain. Restricting to adults (~0.78 of the
undocumented population) and attributing roughly half of ITEP's delta to compliance rather than wages
gives **≈$2,364 per adult** — within 5% of the bottom-up figure. **Two independent routes land at
$2.4k–$2.5k per unauthorized adult per year**, with a defensible band of **$1.5k–$3.4k** spanning the
discount and off-books-share uncertainty. Use **−$2,400/adult-year** as the point estimate.

**Relative to the ledger:** on the −$11.5k Mexico-born gap, this is **21%** — material, same sign,
not sign-flipping. It also belongs on *both* sides: the unreported earnings are missing income as
well as missing tax, so a full treatment raises measured income for this group too.

### Line (ii) — US-born second generation

**Sign: ≈ 0. Recommend booking $0 with a documented rationale, not a guessed negative.**

Every status-driven mechanism (ESF, ITIN, authorization-constrained cash work) is structurally
unavailable to a US-born citizen. What remains is (a) the population-rate self-employment
underreporting that applies to all Americans equally and therefore nets out against the native
comparison group, and (b) the Desai et al. system-avoidance effect, which is real and significant but
unpriced. A defensible upper bound on (b): if second-generation adults in mixed-status families are,
say, 5pp more likely to be in informal work and the per-worker loss is the same $6,338, that is
**≈ −$317/adult-year**, i.e. **3.5% of the −$8.9k second-generation gap** — inside the noise.
**Do not let this channel carry any weight in the second-generation conclusion.**

**The asymmetry is the finding.** This channel widens the first-generation gap by ~20% and leaves
the second-generation gap essentially untouched. It therefore *increases* the measured
first-to-second-generation convergence, it does not explain away the second-generation shortfall.

---

## 5. What could be run on repo data (≤5)

1. **Correct the `[TRAINING-DATA]` row at `research/immigration-fiscal-impact-unauthorized-memo.md:152`.**
   "50-75% pay via ITIN or mismatched SSN" is contradicted by SSA's own decomposition: 3.1M of 7.0M =
   **44%** on payroll, 56% underground (2010). One-line fix, real correction, primary source.
2. **Add an unreported-earnings adjustment arm to the generation ledger §12.** The CPS-modeled-tax
   approach in `research/immigration-mexican-origin-generation-incarceration-2026-09-16.md` can carry
   a sensitivity column: inflate foreign-born non-citizen earnings by the off-books share and apply
   the combined rate. The −$2,400/adult-year line above is the point estimate; run it at 0.8× and
   1.4× for the band.
3. **Self-employment share by nativity from the IPUMS panel** (`research-data/immigration-fiscal/derived`,
   44M rows, foreign-born = BPL≥150). CLASSWKR gives self-employed status; crossing it with nativity
   and generation gives the *exposure* weight for the 57% nonfarm-proprietor NMP. This is the one
   genuinely new number the repo could produce, and nothing published has it by generation.
4. **Industry-exposure weighting.** Pew's occupation shares (farming 26%, landscaping 24%, private
   household 23%, cleaning 17%, construction 14%) crossed with the repo's ACS/CPS industry codes gives
   a per-person informality-exposure index by nativity — a better allocator than a flat 56%.
5. **Skip:** any attempt to use ESF dollar totals as an unauthorized-earnings series. GAO and SSA both
   state the unauthorized share is unknown and most reinstatements go to US-born citizens. It is a
   trap that looks like a clean time series.

---

## Gaps and what a re-dispatch should chase

- **[GAP]** Bernhardt et al. 2009 "Broken Laws, Unprotected Workers" and Bernhardt/Spiller/Theodore
  2013 were not retrieved in this epoch. They carry survey-measured pay-violation rates by nativity
  and status in three cities (LA/Chicago/NYC) and would give a *measured* off-books rate to test
  SSA's imputed 56%. **Highest-value next query.**
- **[GAP]** SSA OCACT has published no successor to Note 151 (April 2013). The 2010 vintage is the
  newest actuarial decomposition. Worth one check of ssa.gov/oact/NOTES for a 2020s note.
- **[GAP]** No paper models compliant-vs-noncompliant firm competition with immigrant labor. Genuinely
  open.
- **[GAP]** Desai et al. 2019 is unpriced — a re-dispatch could pull the actual coefficients from the
  paper to bound line (ii) empirically instead of by assumption.
- **[GAP]** Hurst–Li–Pugsley 2014 (the generic self-employment underreporting benchmark, ~1.3× income
  multiplier) was not retrieved; it would replace the IRS 57% NMP with a household-survey-based
  factor better matched to CPS income.

---

## APPENDIX A (epoch 2) — the two top gaps are now CLOSED

### A1. Bernhardt et al. 2009 — the only SURVEY-MEASURED rates by authorization status

**"Broken Laws, Unprotected Workers"** (Bernhardt, Milkman, Theodore, Heckathorn, Auer, DeFilippis,
González, Narro, Perelshteyn, Polson & Spiller). n=4,387 front-line workers in low-wage industries,
Chicago + Los Angeles + New York City, **2008**. Respondent-driven sampling explicitly designed to
reach unauthorized immigrants and cash-paid workers. Weighted to represent ~1.64M workers = 15% of
the three cities' combined workforce.
[SOURCE: https://escholarship.org/content/qt1vn389nh/qt1vn389nh.pdf; https://www.nelp.org/insights-research/broken-laws-unprotected-workers-violations-of-employment-and-labor-laws-in-americas-cities/]

**Sample composition by nativity and legal status — this is the key table:**

| Group | Share of sample |
|---|---|
| U.S.-born citizen | **30.0%** |
| Foreign-born authorized (incl. naturalized) | **31.2%** |
| **Foreign-born unauthorized** | **38.8%** |

**Measured violation rates:**

| Violation | Rate | Note |
|---|---|---|
| **No pay stub / no earnings documentation** | **57%** of all workers | Required by CA/IL/NY law regardless of cash or check. **Closest published proxy for "off the books."** |
| Paid below minimum wage, prior week | 25.9% | median underpayment $1.43/hr; 60% underpaid by >$1/hr |
| Any pay-related violation, prior week | 68% | avg loss $51 of $339 weekly earnings = **15% wage theft rate** |
| Annualized loss per affected worker | **$2,634 of $17,616** | |
| Overtime violation, **unauthorized** immigrants at risk | **85%** | vs **67%** for authorized immigrants |
| Minimum wage violation, foreign-born | 31% | **~2× the US-born rate** (US-born ≈17.5–18%) |
| Minimum wage violation, **unauthorized women** | **47.4%** | vs 30% unauthorized men; US-born men≈women |
| Injured workers who filed a workers' comp claim | 8% | 50% of those who told the employer faced an illegal reaction |

**How this tests SSA's imputed 56%:** the 57% no-paystub rate is measured, not modeled, and lands
almost exactly on SSA's 56% off-the-books imputation — but **for a low-wage-industry sample in three
big cities, not for unauthorized workers nationally**. Read carefully, it *supports the order of
magnitude* while showing the channel is a low-wage-labor-market phenomenon, not a status phenomenon:
the authors' own headline conclusion is that "where a worker is employed — that is, in which industry
and in what type of job — is generally a much better predictor of violations than the worker's
demographic characteristics," and violation rates hit 40%+ in apparel, personal services and private
households while falling to 12–13% in residential construction and home health care.

**[DISCONFIRMER — record this one.]** The strongest single fact against a nativity-driven reading is
that among US-born workers, **African-American workers had a minimum-wage violation rate triple that
of white workers**. A model that attributes informality to immigration status has to explain that
gradient, which has no immigration content at all. Industry and occupation dominate.

### A2. Hurst, Li & Pugsley 2014 — and why it partially CANCELS in the ledger

**"Are Household Surveys Like Tax Forms? Evidence from Income Underreporting of the Self-Employed,"**
Review of Economics and Statistics 96(1):19–33, March 2014.
[SOURCE: https://doi.org/10.1162/rest_a_00363; NBER w16527; https://www.federalreserve.gov/pubs/feds/2011/201106/201106pap.pdf]

Method: Pissarides–Weber Engel-curve inversion. Estimate the income–expenditure relationship for wage
and salary workers, then back out the self-employed's true income from their reported expenditures.

| Estimate | Value | Source/spec |
|---|---|---|
| **Published headline: self-employed underreport income to household surveys** | **~25%** | RESTat 2014 final |
| Working-paper headline | ~30% | NBER w16527 / FEDS 2011-06 |
| Total family income + food expenditure | 31.7% (CE), 30.1% (PSID) | |
| Labor+business income + food expenditure | 33.5% (CE), 34.9% (PSID) | |
| Using nondurable / total expenditures | 25–28% | |
| Self-employed share of prime-age working males | 10–14% | |

**Citation hygiene:** the published version says **25%**, the widely-circulated working paper says
**30%**. Cite 25% and note the range 20–30%. Underreporting was larger pre-1986 (higher marginal
rates) and **smaller among the self-employed with advanced degrees**.

**Why this matters more than it first appears, and cuts against §4 line (i):** the repo's generation
ledger uses **CPS-modeled taxes on reported income**. Hurst–Li–Pugsley shows CPS-type reported income
is understated ~25% *for every self-employed household*, native and immigrant alike. So the ledger is
not missing informal income only for immigrants — it is missing it for the native comparison group
too, in proportion to each group's self-employment rate. **The correct ledger adjustment is therefore
not the gross informality loss but the DIFFERENTIAL**: (immigrant self-employment exposure − native
self-employment exposure) × underreporting factor, plus the status-specific off-books component that
has no native analogue. This meaningfully shrinks §4's −$2,400 line if foreign-born and native
self-employment rates are close.

**This is now the single highest-value thing the repo can compute** (and it supersedes item 3 in the
§5 list as the priority): self-employment rate by nativity and generation from the IPUMS panel.
If foreign-born self-employment exposure ≈ native, most of the survey-underreporting term cancels and
only the status-specific off-books piece survives — call it **−$1.5k to −$2.0k per unauthorized
adult-year** rather than −$2,400. If foreign-born exposure is materially higher, the original figure
stands. **Until that is run, treat −$2,400 as an upper-ish estimate with a downward-biased floor
around −$1,500.**

---

## Revised bottom line after epoch 2

Nothing overturns the verdict; two things tighten it.

1. **The off-books share is corroborated.** SSA's modeled 56% and Bernhardt's measured 57%-no-paystub
   agree. The repo's `[TRAINING-DATA]` "50-75%" row is still wrong in the other direction (it
   describes the *paying* share, which SSA puts at 44%).
2. **The per-adult line should be quoted as a range, not a point**, because the native comparison
   group also underreports. **−$1,500 to −$2,400 per unauthorized adult-year**, resolvable to a point
   estimate by one IPUMS tabulation. Against the −$11.5k Mexico-born gap that is **13–21%**; against
   the −$8.9k second-generation gap it is **≈0**, because the second generation has no
   status-specific component and its survey-underreporting term cancels against natives by
   construction.
3. **The asymmetry stands and is the finding.** This channel widens the first-generation gap and
   leaves the second-generation gap intact, so it *increases* measured first-to-second-generation
   convergence. It cannot be used to explain away the second-generation shortfall.
