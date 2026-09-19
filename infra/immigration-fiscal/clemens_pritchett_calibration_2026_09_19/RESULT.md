**Verdict:** The reproduction gate passes 7 of 7 checks, rebuilding every row of Clemens & Pritchett's Table 1 from its own regression coefficients and both of the numerical claims the paper makes about its optimal-migration surface. Substituting this repo's Mexican-origin measurements then moves the model's answer by an order of magnitude and, on every economic outcome, past zero. The repo's generational assimilation rate for Mexican-origin earnings is **0.0099–0.0133 per year** and for the fiscal balance **0.0014–0.0071**, against the paper's stated range of **0.026–0.128** and its own Mexico row of **0.0282**; the repo's cohort-measured transmission rate for Mexico is **0.347–0.664** (headline **0.416**) against the paper's Mexico row of **0.239**. At those values eq. (8) returns **m\* = −0.024 to −0.007**, i.e. no positive optimal rate, against an observed Mexican rate of **0.0596%** per year. The sign is not robust: **7 of 21 disconfirmation arms return a positive m\***, and the paper's conclusion is restored whenever the assimilation-relevant object is one of the four fast-converging attitude items rather than earnings or fiscal balance, or when an aggressive ethnic-attrition correction is combined with a reference-group correction. What survives every arm is the magnitude collapse: the paper's Mexico optimum is 47× the observed Mexican rate, and no construction using a repo-measured generational assimilation rate exceeds 15×.

## Audit correction — September 19, 2026

**Conditional calibration, not a measured refutation.** The formula reproduction and parameter sensitivities are retained. The substituted common-age earnings/income gaps are unconditional on schooling, employment and hours; the paper's productivity concept excludes observed human-capital differences. Dividing contemporary G1/G3+ gaps by an assumed 58-year interval also does not measure one dynastic population's decay rate. Fiscal and attitude gaps have no estimated mapping into TFP. Thus a negative algebraic optimum in these substitutions is a scenario result, not an empirically identified zero-admission optimum or evidence that the paper's conservatism argument is reversed. The global-versus-native distinction already stated below remains valid. [SOURCE: paper §6.2 and equation 10; repo_inputs.py and cpmodel.py; [bounded audit](../../../notes/immigration-cp-calibration-audit-evidence-2026-09-19.md)]


Model self-report: `claude-opus-5[1m]`.

Lane: `/Users/alien/Projects/immigration-research/infra/immigration-fiscal/clemens_pritchett_calibration_2026_09_19/`.
Run commands and input inventory in `README.md`; all tables in `derived/tables.md`.

---

## 1. Reproduction gate — PASS, 7/7

`derived/gate_log.txt`, `derived/gate.csv`. Source: IZA DP 9730 (Feb 2016),
sha256 `ce57a3e8f73d045eb8a85f0a0d7a2dc275f199fa411968260b7a0d5a4446b7fa`, pinned in `_cache/`,
text extracted with `pdftotext -layout`. Every coefficient and constant below is located by its
own row label or sentence in that text by `parse_paper.py`; none is typed from memory.

| Check | Result |
|---|---|
| G1 `delta = 1 - exp(zeta + 5*lambda + 25*mu)` for all 9 countries | PASS, max absolute error 0.000653 |
| G2 `a = ln2/t_half` from eq. (12) for all 9 countries | PASS, max relative error 0.0059 |
| G3 `tau = delta/gamma` for all 9 countries | PASS, max absolute error 0.000426 |
| G4 section 5.3: at `c=0.5, tau=0.5, a=0.03` the paper says `m* > 0.01` | PASS, we get **0.010229** |
| G5 section 8 ranges are the Table 1 extremes | PASS at the precision the prose prints |
| G6 Figure 9: every country's `m*` is "at least several times" `m0=0.003` | PASS, minimum Somalia at **4.70×** |
| G7 eq. (9) and footnote 5 give the same transition time | PASS, both 498.211145618 / m |

Baseline transition time from eq. (9): at the paper's own `m0 = 0.003`, **T = 1,661 years**; at
the Mexico row's own optimum `m* = 0.0281`, **T = 177 years**.

**A structural diagnostic the paper does not print.** Eq. (2) defines the steady-state
unassimilated share as `phi = m/a` and states `0 < phi < 1`. At each country's own reported
optimum with `c = 0.5`, `phi` is Bangladesh 0.76, Ghana 1.28, Guyana 1.62, Haiti 1.06,
Liberia 1.56, Mexico 0.995, Nepal 1.11, Nicaragua 1.17, Somalia 0.55. **Six of the nine sit
above 1** (Ghana, Guyana, Haiti, Liberia, Nepal, Nicaragua) and Mexico sits just under it,
where the congestion term `1 - c*phi` in eq. (3) is at or past its own bound and the
first-order Taylor approximations behind eq. (8) do not hold. This is reported as a diagnostic,
not as a gate failure: it does not affect the reproduction, but it bounds how far any of these
optimal rates, the paper's or ours, should be read as a quantity rather than a direction.
[CALCULATION from `derived/gate.csv`]

## 2. Repo-derived assimilation rates

`derived/parameters.csv`. Definition: the model's `a` is the exponential decay rate of the
deviation from natives, so `a = -ln(gap_late / gap_early) / years`, the same convention as the
paper's `a = ln2 / t_half`. Gaps are against third-plus non-Hispanic whites. One generation is
29 years [INFERENCE, lane brief stipulation; sensitivity at 25 and 33 years is in the file and
moves `a` by ±16%/−12%]. The G1→G3+ column spans 58 years. Four of 21 outcomes are flagged
unusable because their first-generation gap is not distinguishable from zero, so there is
nothing for them to assimilate.

| Outcome | G1 gap | G2 gap | G3+ gap | a G1→G2 | a G2→G3+ | **a G1→G3+** |
|---|---|---|---|---|---|---|
| Median earnings, workers 25–64 (share of white level) | 0.406 | 0.241 | 0.188 | 0.0181 | 0.0086 | **0.0133** |
| CPS wage and salary, common age ($) | −17,546 | −9,980 | −8,993 | 0.0195 | 0.0036 | **0.0115** |
| Mean earnings, adults 25–64 (share of white level) | 0.477 | 0.293 | 0.255 | 0.0168 | 0.0048 | **0.0108** |
| CPS total personal income, common age ($) | −29,213 | −16,832 | −16,406 | 0.0190 | 0.0009 | **0.0099** |
| Ledger balance, common age, person-source ($/yr) | −6,888 | −5,278 | −4,571 | 0.0092 | 0.0050 | **0.0071** |
| Ledger balance, common age, shared ($/yr) | −6,562 | −5,943 | −4,622 | 0.0034 | 0.0087 | **0.0060** |
| Ledger balance, common age **and place**, person-source | −5,814 | −6,791 | −4,896 | −0.0054 | 0.0113 | **0.0030** |
| Ledger balance, common age **and place**, shared | −5,664 | −6,772 | −5,211 | −0.0062 | 0.0090 | **0.0014** |
| Death penalty (pp) | −35.5 | −9.7 | −4.1 | 0.0447 | 0.0297 | **0.0372** |
| Ever approves police striking a citizen (pp) | −42.8 | −25.7 | −8.7 | 0.0176 | 0.0374 | **0.0275** |
| All-13 institutional confidence index | +0.13 | +0.02 | +0.03 | 0.0645 | −0.0140 | **0.0253** |
| Stouffer 15-item tolerance | −1.37 | −1.42 | −0.34 | −0.0012 | 0.0493 | **0.0240** |
| Obedience as a top child quality (pp) | +16.1 | +2.6 | +4.4 | 0.0629 | −0.0181 | **0.0224** |
| Government should reduce income differences (1–7) | +0.59 | +0.58 | +0.32 | 0.0006 | 0.0205 | **0.0105** |
| Anti-American-Muslim-clergyman, 3 items | −0.44 | −0.27 | −0.25 | 0.0168 | 0.0027 | **0.0097** |
| Political violence at least a little justified (pp) | +20.3 | +9.5 | +13.7 | 0.0262 | −0.0126 | **0.0068** |
| Generalized trust, GSS adjusted (pp) | −11.15 | −11.63 | −10.52 | −0.0015 | 0.0035 | **0.0010** |

[SOURCE: earnings and income gaps `acs_earnings_replication_2026_09_17/derived/cps_gaps.csv`;
ledger gaps `all_age_ledger_2026_09_17/derived/estimates.csv` and
`ledger_stress_2026_09_17/derived/state_matched.csv`; attitude items
`norms_gen_2026_09_18/derived/mex_synth_table.md`; trust
`research/immigration-confidence-ladder.md` entry 110; earnings levels
`research/immigration-mexican-origin-by-generation-2026-09-16.md:23,24`]
[CALCULATION for every `a` column]

**Against the paper's range.** The paper reports `a` between **0.026 and 0.128**. Every
economic outcome here falls below that floor. Four attitude items reach it: death penalty
0.0372, police approval 0.0275, institutional confidence 0.0253, Stouffer tolerance 0.0240.

**What stalls.** Four things, at three different places in the lineage.

1. **Fiscal balance, at a common age and place.** `a = 0.0014–0.0030`, roughly a fifth of the
   rate at the age-only standard. This is ladder 125's finding restated as a rate: the first-to-
   third-plus narrowing is +$453 [−1,446, +2,353] and +$918 [−1,216, +3,052] at the joint
   state × age standard, against +$1,939 and +$2,317 at the age-only standard, so most of the
   measured fiscal convergence is where the lineage lives, not what it earns.
2. **Generalized trust.** `a = 0.0010`. Ladder 117 puts adjusted G3+ minus G1 at +2.08 pp
   [−2.36, 6.52], an interval containing zero, so the measured rate here is an upper bound on
   something not distinguishable from no convergence at all.
3. **The G2→G3+ step on earnings.** `a` falls from 0.017–0.020 in the first native-born
   generation to 0.0009–0.0086 in the second. Total personal income is the extreme case: the
   gap moves from −$16,832 to −$16,406, a rate of 0.0009.
4. **The economic role of government.** `a G1→G2 = 0.0006`, essentially flat across the first
   native-born generation, converging only at G3+ and then to +0.32 scale points, which
   ladder 135 measures as about a fifth of the white ideological spread.

Two items **over-converge or reverse**: institutional confidence starts 0.13 above whites and
crosses to +0.03, and political violence endorsement is non-monotone (+20.3 → +9.5 → +13.7).
Neither is a low-productivity trait converging upward, which is what the model's `a` is built
to describe; both are reported for completeness and flagged.

## 3. Repo-derived transmission rate for Mexico

`derived/tau_repo.csv`. The paper's method is `tau = delta / gamma`, with `delta` the earnings
gap of a new arrival conditional on age, education and sex five years after arrival, and `gamma`
the origin TFP gap net of human capital. The repo's arrival-cohort lane computes exactly that
`delta` object: the log-wage residual of Mexico-born full-time full-year workers against US-born
non-Hispanic white cells of the same year, sex, age group and education. `gamma = 0.523` is the
paper's own Table 1 value for Mexico, from Jones (2016), used because it is the denominator its
`tau` is defined against.

| Construction | n | mean years since arrival | residual | delta | **tau** |
|---|---|---|---|---|---|
| ACS 2023–24, arrivals 2015–19 | 1,223 | 4.7 | −0.2454 | 0.2176 | **0.4161** |
| ACS 2023–24, arrivals 2020–21 | 1,620 | 2.9 | −0.3037 | 0.2619 | **0.5008** |
| ACS 2023–24, arrivals 2022–24 | 2,283 | 1.1 | −0.3204 | 0.2741 | **0.5241** |
| IPUMS 2023, arrivals 2015–19 | 996 | – | −0.2003 | 0.1815 | **0.3471** |
| IPUMS 2023, arrivals 2020–24 | 1,898 | – | −0.2755 | 0.2408 | **0.4604** |
| IPUMS 2000, arrivals 2000–07 | 877 | – | −0.3510 | 0.2960 | **0.5659** |
| IPUMS 2000, arrivals 1990–99 | 17,345 | – | −0.3574 | 0.3005 | **0.5745** |
| IPUMS 1980, arrivals pre-1980 | 4,659 | – | −0.4045 | 0.3327 | **0.6360** |
| IPUMS 1990, arrivals 1980–89 | 7,101 | – | −0.4270 | 0.3475 | **0.6644** |

[SOURCE: `arrival_cohorts_2026_09_18/derived/acs_wage_residual_by_ysm_band.csv` and
`ipums_wage_residual_by_ysm_band.csv`] [CALCULATION for delta and tau]

The headline is the ACS 2015–19 arrival cohort at a mean 4.7 years since arrival, the
construction nearest the paper's own "five years after arrival": **tau = 0.416**. That is 1.7×
the paper's Mexico row of 0.239, and the 1980s and 1990s arrival cohorts (0.57–0.66) sit above
the paper's entire stated range of 0.157–0.497.

Two measurement notes that cut in opposite directions and are run as arms in section 5. The
repo residual is against **white** natives while the paper's is against **all** natives, which
inflates the repo `delta`. The repo residual is restricted to **full-time full-year** workers
while the paper's is not, which deflates it.

## 4. Implied optimal migration against the observed rate

`derived/mstar_by_outcome.csv`, `derived/observed_migration.csv`.

**Observed Mexican migration rate.** On the paper's own footnote-6 convention (LPR admissions
over destination population), Mexico-born LPR admissions were **202,600 in FY2024** and averaged
**155,110 per year over FY2015–FY2024**, against a US resident population of **340,110,988** at
1 July 2024. That is **m = 0.000596** (0.0596%) for FY2024 and **0.000456** for the ten-year
mean. [SOURCE: DHS OHSS Yearbook FY2024 Table 3; Census Bureau NA-EST2024-POP, Vintage 2024]
Stock shares for reference: Mexico-born **3.59%** of the US population, all three Mexican-origin
generations **12.02%**. [SOURCE: `all_age_ledger_2026_09_17/derived/estimates.csv`, CPS ASEC
2025] The LPR measure counts status grants, not arrivals, and excludes the unauthorized inflow
that the stock measure contains; it is used because it is the paper's own denominator.

**Result at the headline parameters (tau = 0.416, c = 0.5).** `m* > 0` requires
`a > rho * tau * gamma-tilde = 0.018446`. No economic outcome clears it.

| Outcome supplying `a` | a | m\* | vs observed |
|---|---|---|---|
| Ledger balance, common age and place | 0.0014 | −0.0236 | −39.6× |
| Ledger balance, common age | 0.0060 | −0.0172 | −28.9× |
| CPS total personal income, common age | 0.0099 | −0.0118 | −19.8× |
| Mean earnings, adults 25–64 | 0.0108 | −0.0106 | −17.8× |
| Median earnings, workers 25–64 | 0.0133 | −0.0071 | −11.9× |
| Stouffer tolerance | 0.0240 | +0.0077 | +13.0× |
| Institutional confidence | 0.0253 | +0.0095 | +15.9× |
| Police approval | 0.0275 | +0.0125 | +21.0× |
| Death penalty | 0.0372 | +0.0260 | +43.7× |
| *Reference: the paper's own Mexico row, tau = 0.239* | *0.0282* | *+0.0281* | *+47.1×* |

The split is clean and it is not a close call at either end: every economic outcome sits below
the threshold and every fast-converging attitude item sits above it.

**Where the sign turns.** Eq. (8) has no stock argument, so there is no Mexican-origin stock at
which the model changes sign; `m*` is set by parameters alone and turns at `a = rho*tau*gamma-tilde`.
What the stock controls is the realised TFP loss through eq. (3). The threshold in each
parameter, from `derived/sign_flip.csv`:

- At the repo's mean-earnings `a = 0.0108`, `m*` is positive only for **tau < 0.243** — and the
  paper's own Mexico tau is 0.239, which is why that pairing sits within a rounding error of zero.
- At the repo's fiscal `a = 0.0014–0.0071`, `m*` is positive only for **tau < 0.032–0.159**,
  below the paper's entire stated range for any country.
- At the repo's headline `tau = 0.416`, `m*` is positive only for **a > 0.0184**.
- At the paper's Mexico `tau = 0.239`, `m*` is positive only for **a > 0.0106**.

## 5. Disconfirmation — 7 of 21 arms reverse the headline

`derived/arms.csv`. Every arm resting on a repo-measured `a` is run at both ends of the
economic-outcome range, because the range across constructions is the headline. All at `c = 0.5`.

| Arm | a | tau | m\* | vs observed | m\* positive? |
|---|---|---|---|---|---|
| A0 headline, slow / fast | 0.0014 / 0.0133 | 0.416 | −0.0236 / −0.0071 | −39.6× / −11.9× | no / no |
| A1 ethnic attrition 17% | 0.0047 / 0.0165 | 0.416 | −0.0191 / −0.0026 | −32.1× / −4.4× | no / no |
| A1 ethnic attrition 30% | 0.0076 / 0.0195 | 0.416 | −0.0151 / +0.0014 | −25.3× / +2.4× | no / **yes** |
| A2 reference group | 0.0014 / 0.0133 | 0.306 | −0.0183 / −0.0003 | −30.7× / −0.6× | no / no |
| A3 attrition 17% + reference | 0.0047 / 0.0165 | 0.306 | −0.0134 / +0.0045 | −22.5× / +7.6× | no / **yes** |
| A3 attrition 30% + reference | 0.0076 / 0.0195 | 0.306 | −0.0090 / +0.0089 | −15.1× / +15.0× | no / **yes** |
| A4 generation 25 years | 0.0017 / 0.0155 | 0.416 | −0.0233 / −0.0041 | −39.0× / −6.9× | no / no |
| A5 repo `a` only, paper's tau | 0.0014 / 0.0133 | 0.239 | −0.0146 / +0.0044 | −24.5× / +7.3× | no / **yes** |
| A6 repo tau only, paper's `a` | 0.0282 | 0.416 | +0.0135 | +22.7× | **yes** |
| A7 the paper's own Mexico row | 0.0282 | 0.239 | +0.0281 | +47.1× | **yes** |
| A8 fastest measured outcome | 0.0372 | 0.416 | +0.0260 | +43.7× | **yes** |
| A9 unconditional tau | 0.0014 / 0.0133 | 0.912 | −0.0396 / −0.0275 | −66.4× / −46.2× | no / no |

A1 rests on the third-plus group being self-identified: 17% of third-generation Mexican-ancestry
children and up to 30% of youth drop the identification, with leavers positively selected
(memo §1, ladder 67). The arm scales the measured G3+ gap by `(1-s)` with leavers assumed fully
converged, which is the most favourable possible correction, and adds 0.0032 (17%) or 0.0062
(30%) to `a`. A2 re-references `delta` from white natives to all natives using the memo's own
mean-earnings row, a log shift of 0.0712 that moves `tau` from 0.416 to 0.306; this is an
unconditional shift applied to a conditional residual, so it overstates the correction. A9 is
included as the opposite bound and is **not** the paper's definition: its `gamma` is already net
of human capital, so loading the unconditional gap into `tau` double-counts schooling as TFP.

**The decomposition is the durable result.** Reading A7 → A6 → A5 → A0: the paper's own Mexico
parameters give 47.1× the observed rate; replacing only `tau` with the repo's gives 22.7×;
replacing only `a` gives −24.5× to +7.3×; replacing both gives −39.6× to −11.9×. The
assimilation substitution does nearly all the work, and it does it in the direction the paper
did not anticipate.

## 6. The paper's own conservatism argument runs backwards here

The paper lists seven assumptions that it says keep its estimates "conservatively low". One of
them is directly measurable in this repo, and it fails for the Mexican-origin lineage:

> No replacement by children. The estimates of earnings assimilation from census data are for
> only for the foreign-born themselves, who are assumed to remain infinitely in the labor force.
> In reality, they are replaced by their children raised in the destination country—partially
> replaced within roughly 20–30 years as their children join the labor force, and fully replaced
> within 40–50 years as the immigrants retire. These children would on average exhibit more
> productivity-assimilation than their parents. The assimilation rate of the 'dynastic worker'
> in the model would therefore proceed at a higher rate than the empirical estimates of a in the
> previous section.

The repo measures that dynastic rate. On earnings it is **0.0099–0.0133**, below the paper's own
individual-level Mexico estimate of **0.0282**, because the second native-born generation adds
almost nothing (`a G2→G3+ = 0.0009–0.0086`). For Mexican-origin the correction the paper
described as conservative moves `a` down, not up, and it moves it far enough to change the sign
of `m*`. This is a claim about one origin, and the paper's own §6.2 warns that the relevant
object is cross-sectional rather than longitudinal:

> Thus the assimilation of interest is precisely cross-sectional assimilation of the overall
> stock of migrants, not longitudinal assimilation of individual migrants.

The generational measure here is cross-sectional in exactly that sense, three cross-sections of
a lineage rather than a followed panel, so it is the right object; but the third of those
cross-sections is the attrition-selected one, which is why A1 is the arm that matters most.

## 7. What the model cannot represent

- **Assortative geography.** The model has one home country with one TFP and one scalar
  congestion rate on the national unassimilated share. The repo's own result is that the
  Mexican-origin fiscal gap stops converging once state is held constant (ladder 125, section 2
  above). The model has no place to put that: `c` scales the national `phi`, it cannot express
  a lineage that converges nationally and does not converge within its own state.
- **Political externality.** Ladder 97 composes a range of **$1,300–$43,000 per low-skill
  immigrant-year** from an identified vote-share effect and an identified populist-government
  cost, with the middle link unmeasured. Nothing in eq. (8) prices a vote. This is not a
  criticism of the model's internal logic; it is a boundary on reading `m*` as a welfare answer.
- **Fiscal channels treated as TFP.** The ledger rows in section 2 are taxes minus transfers,
  a flow between residents, not a change in output. Feeding them into `a` treats a distributional
  quantity as a productivity one. They are reported because the brief asks for them and because
  they are the slowest-converging economic series in the repo, but the earnings rows are the ones
  that belong in this model, and they give the same sign.
- **Everything the paper already lists.** No destination productivity gains, no capital
  adjustment, no steady-state gain after `T`, no return flow of high TFP, equal welfare weights
  on rich and poor. All of those push `m*` up and none is corrected here.

## 8. Limits

The model is about global efficiency, not the host country's fiscal balance; `a` and `tau` are
defined on total factor productivity and every repo outcome used here is a proxy for it. The
paper's calibration is cross-country and this one is a single origin, so it tests the paper's
Mexico row and its general conclusion only through that row. The repo measures resident groups,
not admission, and the gap against same-age whites is the measured object; no marginal-admission
or causal claim is made. The 29-year generation is a stipulation, not a measurement. The
attitude items are survey responses, not behaviour, and ladder 135 records that first-generation
respondents differentiate less across batteries and that interviewer mode inflates some
first-generation gaps by around 20 points, both of which would bias the fast attitude `a` values
upward — that is, toward the paper's conclusion. No policy advice is drawn.

## 9. Skipped, and why

- **Penn World Table `gamma` for Mexico.** Not fetched. The paper's `tau` is defined against a
  TFP gap net of human capital from Jones (2016), and substituting a PWT `rtfpna` ratio or a
  GDP-per-worker ratio would change the denominator's definition, not just its vintage, so it
  would not be the paper's `tau`. The effect is transparent: `tau` scales as `1/gamma`, so a
  `gamma` of 0.6 instead of 0.523 would put the headline `tau` at 0.363 and the required `a` at
  0.0161, still above every economic outcome.
- **The published JDE version.** Resolved by DOI through the research MCP for title and
  authorship but paywalled; the open working paper is used throughout and is the version the
  brief names. Any calibration revision between the 2016 working paper and the 2019 article is
  therefore unchecked.
- **Re-running the paper's Borjas-style regression on repo microdata.** Not needed: the
  arrival-cohort lane already computes the conditional residual the paper's `delta` requires, at
  the duration the paper uses, and the brief directs the lane to use repo-derived values.
- **A Mexican-origin second- and third-generation `tau`.** The model has no such parameter;
  `tau` is a property of the arriving migrant, and generational change is `a` by construction.

## 10. Reproducibility

`bash run.sh` from a cleared `derived/`, then `cp -R derived /tmp/run1 && bash run.sh &&
diff -r /tmp/run1 derived` — **no differences**, `derived/` is byte-identical across runs.
Verified this session. `gate.py` exits non-zero if any of the seven checks fails, so the gate
cannot be silently skipped. Nothing in this lane is committed and nothing under `research/` is
written.
