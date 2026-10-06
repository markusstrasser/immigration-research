# Recent papers and essays, July 2025 – October 2026: what could show the account wrong

**Verdict:** No new paper overturns a measured number. One argument changes what the headline means: on any
budget that is eventually closed, the lineage pays part of the fix, and the cost to other residents is then
about $235–345bn a year, against $390–461bn under current law [FRAMING-SENSITIVE]. Eight further items each
move a priced line by roughly $3bn or more, or bear on a qualitative claim; the largest are a school-spending
response slightly below full cost (about −$15–17bn, inside the stated low side) and police records that may
under-record Hispanic offenders (about +$3–4bn on the headline). Two face-value hits fail on their own design:
the 2021–24 surge's cross-metro native-wage gain and a survey-based Hispanic income-tax ratio that tax records
contradict. [INFERENCE, from the graded items below]

Date: 2026-10-06. Window: first published or substantively revised 2025-07-01 → 2026-10-06, priority
2026-03 onward; an older item counts only if major, contrary to a load-bearing claim and never engaged here.
Question from the operator: are there new papers, in any discipline or as essays, that show we are wrong
about something, without nitpicks. Reporting bar: a hit moves the headline by 10% or more, contradicts a
qualitative claim, or invalidates a method; the operator added that anything above about $3bn is worth
mentioning.

Provenance: seven researcher lanes (claude-opus-5-5) swept fiscal and measurement, assimilation and identity,
crime, labor/housing/world welfare, essays and think tanks, administrative/survey-methods/regulatory records, and
pre-publication/lineage/Spanish-language/rebuttal venues. Each checked the repo with `rg` before reporting. The
lead re-read the primary text for Hunt–Orrenius–Zavodny (Table 6), Lee–Scafidi (Table 4 text), the AEI fiscal-gap
passage, the CPS weighting rules and the CBO working paper's identity. Every other number below is a lane's
reading of its source and is marked so. The lane files and PDFs sit in the session scratchpad; only the TPC PDF
was staged in the repo (see the end).

Instrument note: this topic is politically charged and the grading was done by LLMs
([bias caveat](../notes/llm-bias-caveat.md)). The lean of the findings is reported below.

## The estimand challenge: who pays when the budget is closed

Orrenius, Viard & Zavodny, *The Fiscal Impact of Immigration: An Update*, AEI, September 2025 (p. 11, "Significance
of the Growing Fiscal Gap"): current-policy calculations "present an overly negative picture" because "each
additional household that enters the population … will bear part of that burden", so immigrants "dilute the
entire fiscal gap", put at $150tn (Auerbach–Gale 2013's lowest case, 4.23% of the present value of GDP, grown with
GDP). [SOURCE: https://www.aei.org/wp-content/uploads/2025/09/The-Fiscal-Impact-of-Immigration-An-Update.pdf]
The paper's numbers reprint NAS 2017 and were already handled; this argument was not.

Applied here. The headline is the group's change to other residents' net position with no rule that closes the
budget. If the budget is closed by tax rises or cuts that the lineage shares at rate *s*, the cost to others is the
group's net cost minus *s* times the whole adjustment F [INFERENCE: others pay (1 − s)(F_others + G_group) instead of
F_others]. With F at AEI's 4.23% of 2024 GDP, about $1.23tn a year:
- shared per head (*s* ≈ 12.6%, 42.75M of about 340M residents): $234.8–305.7bn;
- shared by tax payments (*s* ≈ 9.5%, a lane estimate from the decomposition's tax gap): $273.1–344.0bn.
[CALCULATION: 390.3 − 0.126 × 1,234 and 461.2 − 0.126 × 1,234; 390.3 − 0.095 × 1,234 and 461.2 − 0.095 × 1,234]

So about $235–345bn, 25–40% below the headline. The printed excess over as many average residents,
$280.5–297.4bn (ladder 269), sits inside: it is the per-head case sized at the account's own average-resident gap.
Part of AEI's gap is Social Security's and Medicare's, which the account already closes by valuing promises at
payable benefits, so a general-fund-only closure would sit nearer the top of the range [INFERENCE].

Why the current-law headline still stands: current law schedules no general-fund closure; the debt-legacy lane
already charges the interest on past gaps beside the account; and the NRC 1997 rule of holding debt at its 2016
share of GDP failed (FAQ 5). What the repo lacks is the sentence saying that the label "cost to other residents"
assumes others carry the group's whole share of a deficit the lineage would help close, and the closed-budget
arm beside it. Repo: HAD-PARTS (ladder 269's two slices; FAQ 18's "cancels the deficit everyone shares"; FAQ 5).

## Worth mentioning ($3bn and up, or a qualitative claim)

**Schools: spending follows growth almost fully and declines only partly.** Lee & Scafidi, EdWorkingPaper
25-1266, August 2025 (reported as published in *Education Finance and Policy*; journal version not read). US
districts 1998–2019; 20-year long differences, OLS without district or year effects. Per-pupil total spending
rises 0.690% per 1% enrollment decline and falls 0.092% per 1% growth (current spending 0.612 / −0.070; staff
per 100 pupils 0.484 / −0.096; all p < .001). [SOURCE: pp. 24–27,
https://edworkingpapers.com/sites/default/files/ai25-1266.pdf]
- The account is a stationary comparison (FAQ 11), so the growth side applies: total spending responds about
  0.91. Over the group's 17.5% pupil share that is a response of 0.916, about −$15–17bn against the centre's
  response of 1 [INFERENCE: (1 − 0.916) × the school line implied by the case's school-response component, −$28.8 /
  −30.5bn at 0.836, which carries v4's pupil share]. That is inside the stated low side ($362–435bn).
- A lane read the decline side as the account's counterfactual (−$85–119bn). That misreads "finite removal",
  which integrates one cost curve over the group's share in either direction; the account is not a removal path.
- The decline side sharpens FAQ 11: twenty years after a decline, districts still keep about 70% of what
  proportional cuts would shed, as more staff per pupil. Ending the migration would return the school money to
  other residents' children as services, not as tax cuts, and not within twenty years.
- Repo: NEW paper; the asymmetry was seen and left untested (service-scaling memo: .822 growing / .751 shrinking,
  pupil-weighted).

**The 2021–24 surge raised natives' wages across metros, but not in a way that scales.** Hunt, Orrenius &
Zavodny, BPEA conference draft, 24–25 September 2026: 164 metros, immigration-court cases as the surge measure,
shift-share and Texas/Arizona busing instruments. Native adjusted real hourly wage per point of surge share
(IV, full controls): 1.0 (SE 0.3) for 2021–24, to be multiplied by 0.8 for the case undercount; 0.8 weighted by
population. By period: 2.3 (0.7) in 2021–22, 1.3 (0.9) in 2022–23, −0.4 (0.7) in 2023–24; the busing instrument
gives −2.6 (0.6) for 2023–24. Native employment unchanged; rents +1.4–1.6%; 90% of the inflow offset by lower
domestic in-migration. [SOURCE: abstract and Table 6, https://www.brookings.edu/wp-content/uploads/2026/09/3_HuntOrreniusZavodny.pdf]
Clemens, Nice & Rigol (RFBerlin DP 169/26, June 2026, "descriptive evidence") report +3.1% for 2021–23 in
commuting zones [lane reading].
- Scaled naively to the Mexico-born share it would be about $240–260bn a year to natives [lane arithmetic]. It
  does not transfer: the authors say the effects "came to be diffused across larger geographies over time and were
  no longer detectable by cross-metro comparisons"; the effect fades to zero within three years; their leading
  explanation is demand from arrivals "who could initially consume but not yet work"; the education split is
  inconclusive, with the largest point estimate for dropouts; and the population is recent arrivals, not a settled
  Mexican-origin lineage. The production term stays as it is (FAQ 14).
- Same flaw on our side (evidence-symmetry rule 2): the account's renter line ($22–58bn) also scales a cross-metro
  rent elasticity to the nation, and the diffusion argument applies to it too. It barely moves the headline,
  because landlords are other residents, but it carries the claim that renters come out behind (ladder 226).
- Repo: NEW (Wilson–Zhou handled). A reader will cite it against FAQ 14.

**Police and prison records may under-record Hispanic offenders.** Van Pelt, *Mankind Quarterly* 66(3), March
2026 (earlier as a Substack post): corrections rosters in states that record Hispanic origin code 29% of people a
name-and-mugshot model predicts to be Hispanic as White; correcting raises Hispanic counts 20–31% [lane reading of
abstract and post]. If the same error sat in the Texas and Arizona NIBRS offender field, the 2.30 ratio would be
2.9–3.2, victims' harm +$6–10bn and the headline about +$3–4bn through the arrest-keyed police costs; custody is
keyed by ACS self-report and would not move [lane arithmetic].
- Against transfer: about 80% of the records are North Carolina's; the "truth" is a model of how Hispanic a name
  and face look, so Hispanic-surnamed people who do not identify count as mislabels (for the lineage frame part of
  that correction is legitimate); in Texas and Arizona the incident offender record already lists more Hispanics
  than booking does (ladder 218); the victim survey gives 0.94. The repo itself leans on surname imputation in
  Treasury's BISG data, so the objection is to what the model is calibrated to, not to name models as such.
- Repo: HAD-PARTS (ladder 218: jails record 14.4% Hispanic against 19.1% by self-report). A settling check needs
  Texas prisoners' self-reported ethnicity, which public ACS cannot isolate; it is a lane, not a quick check.

**Enforcement lowers Hispanic identification.** Hadah & Denteh, SSRN 6226541, March 2026 (revised April): in CPS
children 2004–13, Secure Communities' staggered rollout lowered parent-reported Hispanic identity by 5.9 points
(7.4%) in the third generation, more in college-educated families [lane reading; standard error not recorded].
The lane put the effect on the 2025 survey at +$6–9bn, assuming about 1M third-plus people leave the identified
pool. CPS weights are raked to national Hispanic totals by age and sex
([Census](https://census.gov/programs-surveys/cps/technical-documentation/methodology/weighting.html)), so a
response-level drop mostly moves weight to other Hispanic respondents rather than shrinking the group; what
remains is a composition effect (the leavers are more educated) of the same sign and smaller, unsized. Check:
third-generation identification in the February–April 2025 monthly files against 2022–24 (the ladder 232
files). Repo: NEW.

**Survey Hispanic income tax far below the account's: contradicted by tax records.** Gale, Hall & Sabelhaus,
Brookings/TPC, December 2025 (accepted at the *National Tax Journal*): SCF waves 1998–2022 through TAXSIM at
2018 law put Hispanic income tax per tax unit at $1,151 against $10,078 for white units (0.114); the account's
CPS model gives 0.425 on the same cut [lane calculation]. Taken at face value the cost would be $20–60bn too low.
Treasury's tax records, already in the repo, settle most of it: Hispanic joint returns paid $9,477 in 2023, $9,936
at 2024 wages, against the CPS model's $11,010, so the CPS is about 11% high there, which the audit rows already
more than correct (`external_benchmarks_2026_09_24/RESULT.md`, arm 2). The SCF's Hispanic cell is a different
population (18.4M tax units against 27.9M in tax records and 36.0M in the CPS) pooled back to 1998. Residual
check: the 2022 SCF wave alone, by filing status, against Treasury's joint-return level. Repo: NEW paper,
HAD-PARTS check.

**Social Security's 2026 payable path is lower than the 2025 one the pension lane uses.** The lane estimates
−$2–4bn on the headline [lane estimate, not verified]; the pension lane reads Note 2025.7's payable path
(`pension_accrual_2026_09_28/pension_accrual.py`). An input refresh, due anyway.

**Laws since 2024 cut transfers to noncitizens.** The public-charge final rule (Federal Register, July 2026,
effective 18 September 2026), about $13bn a year less in transfers overall and perhaps −$3–5bn for the group
[secondary summaries; regulatory impact tables not read]; the 2025 budget law (P.L. 119-21), whose child-credit
Social Security number rule alone is about −$1–4bn [lane estimate], with its premium-credit, Medicaid and SNAP
limits unpriced. Neither corrects 2024; both belong beside any statement about current law today.

**The stall after the second generation may be vintage.** Van Hook & Bachmeier, *Texas-Style Exclusion*, Russell
Sage, November 2024 (before the window, never cited): Mexican families linked from the 1940 census to the CPS and
the 2000 census/ACS. By the third generation the mobility process matches whites at equal family background; the
remaining gap runs through parents' schooling, and the slow progress comes mainly from early Texas arrivals; later
vintages advance faster [lane reading of the online supplement and publisher text]. It does not move the 2024
cross-section, which prices today's people, but it bears on any projection of today's children (FAQ 5 already
says the step to third-plus is not a forecast). Check: split ladder 232's carry-over by the second-generation
parent's birth cohort. Their identification shares (third generation about 0.9 of the second, fourth-plus about
0.64) roughly match ladder 233, which supports the 3.04M added descendants. Repo: HAD-PARTS (ladder 232 lists
vintage as "not excluded").

## New evidence in our favour

- Kantova, Havranek, Irsova & Schwarz, CEPR DP21326, March 2026 [abstract]: a meta-analysis of 1,091 estimates puts
  the native–immigrant substitution elasticity at about 17–22 after correcting for publication bias, which shrinks
  FAQ 14's unapplied production upside.
- Kubrin, Christopher, Hodgen, Luo & Hipp, *Journal of Urban Affairs*, online August 2026 [full text, lane]: across
  about 11,500 tracts, 2010–2018, a rising undocumented share at fixed population leaves violent crime unchanged
  (−0.039, t −0.27), consistent with parity against all residents; it holds the Latino share fixed, so it cannot
  test the 2.30.
- Kosack & Ward, *Journal of Economic History* 2020, and Buckles et al., *Explorations in Economic History* 2025
  [abstracts]: no Mexican–white convergence across three generations in linked censuses to 1940; sons of Mexican
  immigrants had the worst outcomes of any origin.
- Ward, Buckles & Price, NBER w33923, 2025 [abstract]: group gaps persist across four generations.
- Maury et al., NBER w35452, July 2026 [abstract]: Latino families receive fewer benefits than white families at
  higher poverty, consistent with the cost coming from lower taxes rather than service use (ladder 269).

## Screened out

- CBO Working Paper 2026-04 (62261), *Immigrant Earnings Assimilation, 1981–2021*: Akee, Chin & Crown's NBER paper,
  already in ladder 92 (stayers positively selected).
- Escobari et al. (Brookings, September 2026), Hernandez (2026), Aslim et al. (PNAS 2026), Lee–Peri–Yang (Korea):
  disruption costs of enforcement or abrupt stops, a removal estimand (FAQ 11), not the stationary account.
- Caiumi & Peri, CEPR DP21756 (July 2026): nested-CES simulation for all 2000–23 immigration; its low-skill
  elasticity is already in ladder 181 [full text not read].
- Census unit-nonresponse posts (September 2025 and 2026): survey income 2–4% high since 2020, no ethnicity split,
  so shares unchanged unless the bias differs by group (unsized).
- 2025 CPS survey exit among noncitizens (St. Louis Fed, PIIE, CIS): under $1.5bn for the ASEC 2025, fielded
  before most of the exit; about three times that for any income-year-2025 account (ladder 209).
- Vintage 2025 population controls: Hispanic persons +0.9%, about +$2bn.
- Richwine (CIS; *Cityscape*, forthcoming) PUMA rent elasticity 1.46% against the repo's 1.32%: renter line
  +$2–6bn, headline under $0.3bn [abstract].
- Cato and Manhattan Institute exchanges, CIS welfare-use reports, Demsas's essays, Penn Wharton's deportation
  score: handled in earlier passes or a federal-deficit estimand (FAQ 16).

## Lean of the findings

The surviving items point both ways: the closure arm, the school growth response, the Trustees path and the new
laws lower the cost; Van Pelt, Hadah–Denteh, the 2025 population controls and nonresponse raise it, each by less.
The face-value dismissals were two that would lower the cost (the surge wage effect scaled up; the school decline
response) and one that would raise it (the SCF tax ratio), each on design or estimand grounds stated above. The
largest open item lowers the cost.

## Not read

The JPAM Point/Counterpoint of June 2026 (Bier against Tara Watson, 45(3)); DiRienzo & Feldmeyer, *Race and
Justice* 2025, on Hispanic counts across FBI files; Van Pelt's state tables; Hunt–Orrenius–Zavodny's appendix;
the public-charge regulatory tables; Van Hook & Bachmeier's body chapters; CEPR full texts. Not swept issue by
issue: ASR, AJS, JPubE, NTJ, AEJ: Policy, JHR, Demography tables of contents; the ASSA 2027, APPAM, NTA and ASC
programs; the 2026–27 job-market papers.

## Next steps

1. The closed-budget arm beside the headline and an FAQ entry ("Everyone runs a deficit. Won't they help pay it
   off?"): the operator's framing call. Recommended, because a stationary comparison run on a year with spending
   26% above receipts is the first thing a public-finance reader will raise.
2. One line each in FAQ 11 (Lee–Scafidi's decline side), FAQ 14 (Hunt–Orrenius–Zavodny) and FAQ 17 (the SCF
   ratio against Treasury's joint returns).
3. Checks, cheapest first: third-generation identification in the 2025 monthly CPS; the pension lane on the 2026
   Trustees path; the 2022 SCF wave by filing status; ladder 232's carry-over by parent cohort; Texas prisoners'
   self-reported ethnicity.
4. The ASEC 2026 (income year 2025, published September 2026) allows a second measured year (FAQ 18), with the
   survey-exit caveat above.

Staged: `sources/immigration-fiscal/data/external/stage3/tpc/race_and_taxes_2025/` (the Gale–Hall–Sabelhaus PDF
with `ACQUIRED.md`). It is a report, not a dataset, so the dataset register is unchanged.
