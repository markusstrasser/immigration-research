# The Clemens–Pritchett transmission model with Mexican-origin assimilation rates measured in this repo

**Verdict:** Clemens and Pritchett's "epidemiological" model of migration restriction reproduces from its own text (7 of 7 gates, every Table 1 row and both numerical claims), and its conclusion for Mexico, an optimal migration rate 47 times the observed one, rests on an assimilation rate of 0.028 per year that this repo's generational measurements do not support. Measured across three generations of the Mexican-origin lineage against third-plus non-Hispanic whites, the annual convergence rate is 0.010 to 0.013 on earnings and 0.001 to 0.007 on the fiscal balance, below the paper's stated floor of 0.026; the transmission rate for Mexico, built the paper's way from the repo's arrival-cohort wage residuals, is 0.42 against the paper's 0.24. At those values the model's optimal rate is negative on every economic outcome, meaning the model no longer supports relaxing restrictions for this origin. What survives every disconfirmation arm is the collapse in magnitude: no construction using a repo-measured assimilation rate exceeds 15 times the observed rate, and the substitution of the assimilation rate, not the transmission rate, does nearly all the work. The paper's own conservatism argument, that children assimilate faster than their parents so its individual-level rate understates the dynastic one, runs backwards for this lineage: the dynastic earnings rate is below its individual Mexico estimate because the second native-born generation adds almost nothing. [SOURCE: `infra/immigration-fiscal/clemens_pritchett_calibration_2026_09_19/RESULT.md`, `derived/gate_log.txt`, `derived/parameters.csv`, `derived/mstar_by_outcome.csv`, `derived/arms.csv`] [FRAMING-SENSITIVE: the model is about global output, its parameters are total factor productivity, and every repo outcome is a proxy]

Date: 2026-09-19. Lane: `infra/immigration-fiscal/clemens_pritchett_calibration_2026_09_19/`. Paper: Clemens and Pritchett, "The New Economic Case for Migration Restrictions: An Assessment", IZA DP 9730 / CGD WP 423 (2016), published JDE 138 (2019) 153–164; the open working paper is the version parsed and pinned by sha256, the published revision was not obtained.

## 1. What the model is and why it is the right frame for the "culture" objection

The paper formalises the claim that migrants carry the low productivity of their origin into the destination. Three parameters govern the dynamically efficient migration rate: transmission τ, the fraction of origin total factor productivity embodied in an arriving migrant, measured as the conditional earnings gap five years after arrival over the origin TFP gap; assimilation a, the annual rate at which that deviation decays, measured cross-sectionally on the stock; and congestion c, the non-linearity in the unassimilated share. Optimal migration m* rises with a and falls with τ, the productivity gap and the discount rate (working paper eq. 8). The paper calibrates a between 0.026 and 0.128 and τ between 0.157 and 0.497 across nine poor origins including Mexico, finds m* several times observed rates everywhere, and concludes the efficiency case is against current restrictions. [SOURCE: working paper §5–8, parsed text] This is the one framework in the literature that turns "immigrants bring their institutions" into a testable parameter, which is why the repo's generation data belong in it.

## 2. Reproduction

Every Table 1 row is rebuilt from the paper's own regression coefficients (δ to 0.0007, a to 0.6% relative, τ to 0.0004), the §5.3 claim that c = 0.5, τ = 0.5, a = 0.03 gives m* above 0.01 reproduces at 0.0102, and the Figure 9 claim that every origin's optimum is several times the baseline holds with Somalia the minimum at 4.7×. [SOURCE: `derived/gate_log.txt`] [CALCULATION] One diagnostic the paper does not print: its eq. 2 requires the steady-state unassimilated share φ = m/a to lie below one, and at six of the nine countries' own reported optima φ exceeds one (Mexico 0.995), outside the range where the approximations behind eq. 8 hold. The optimal rates, the paper's and this lane's, are directions rather than quantities. [CALCULATION from `derived/gate.csv`]

## 3. The repo's assimilation rates

The model's a is the exponential decay of the deviation from natives, so a = −ln(gap G3+ / gap G1) / 58 years across two 29-year generations (the generation length is a stipulation; 25 or 33 years moves a by +16% / −12%). Gaps are against third-plus non-Hispanic whites, from the repo's own lanes.

| Outcome | G1 gap | G3+ gap | a per year |
|---|---|---|---|
| Median earnings, workers 25–64, share of white level | 0.406 | 0.188 | 0.0133 |
| CPS wage and salary, common age | −$17,546 | −$8,993 | 0.0115 |
| CPS total personal income, common age | −$29,213 | −$16,406 | 0.0099 |
| Ledger balance, common age | −$6,562 to −$6,888 | −$4,571 to −$4,622 | 0.0060–0.0071 |
| Ledger balance, common age and place | −$5,664 to −$5,814 | −$4,896 to −$5,211 | 0.0014–0.0030 |
| Death penalty support, pp | −35.5 | −4.1 | 0.0372 |
| Stouffer civil-liberties tolerance | −1.37 | −0.34 | 0.0240 |
| Generalized trust, pp | −11.2 | −10.5 | 0.0010 |

[SOURCE: `derived/parameters.csv`, drawing on `acs_earnings_replication_2026_09_17/derived/cps_gaps.csv`, `all_age_ledger_2026_09_17/derived/estimates.csv`, `ledger_stress_2026_09_17/derived/state_matched.csv`, `norms_gen_2026_09_18/derived/mex_synth_table.md`, ladder 110 and 117] [CALCULATION] Every economic outcome falls below the paper's floor of 0.026; four attitude items (death penalty, police approval, institutional confidence, tolerance) reach it. Four things stall: the fiscal balance once place is held constant (ladder 125 restated as a rate), generalized trust (ladder 117's interval contains zero), the G2 to G3+ step on earnings (0.0009 to 0.0086 against 0.017 to 0.020 for G1 to G2), and the economic role of government across the first native-born generation (0.0006).

## 4. Transmission for Mexico

τ = δ/γ with γ = 0.523, the paper's own Mexico TFP gap from Jones 2016. The repo's arrival-cohort lane computes the paper's δ object directly: the log-wage residual of Mexico-born full-time workers against US-born white cells of the same year, sex, age and education. At a mean 4.7 years since arrival (ACS 2023–24, arrivals 2015–19, n = 1,223) the residual is −0.245, δ = 0.218, τ = 0.416; the 1980s and 1990s arrival cohorts give 0.57 to 0.66, above the paper's whole range. [SOURCE: `arrival_cohorts_2026_09_18/derived/acs_wage_residual_by_ysm_band.csv`; `derived/tau_repo.csv`] [CALCULATION] The repo residual is against whites rather than all natives, which inflates δ, and is restricted to full-time workers, which deflates it; both are run as arms.

## 5. Implied optimal rate against the observed one

The paper's denominator convention is LPR admissions over destination population: 202,600 Mexico-born admissions in FY2024 over 340.1M gives m = 0.00060, and the FY2015–24 mean gives 0.00046. [SOURCE: DHS Yearbook FY2024 Table 3; Census Vintage 2024] At τ = 0.416 and c = 0.5, m* is positive only if a exceeds 0.0184. No economic outcome clears it: m* runs from −0.024 (fiscal, common age and place) to −0.007 (median earnings), where a negative value means the model's interior optimum does not exist and its corner is zero migration. Every fast attitude item clears it (+0.008 to +0.026). The paper's own Mexico row gives +0.028, 47× observed. [SOURCE: `derived/mstar_by_outcome.csv`, `derived/sign_flip.csv`] [CALCULATION]

## 6. Disconfirmation

Twenty-one arms. Seven return a positive m*: ethnic attrition of 30% with leavers assumed fully converged (the most favourable correction, ladder 67), attrition combined with re-referencing δ to all natives, the paper's own τ with the repo's fastest economic a, and any arm where an attitude item supplies a. Attrition at 17%, the 25-year generation, the all-native reference alone, and the unconditional τ (0.91, not the paper's definition) do not reverse it. The decomposition is the durable result: the paper's Mexico parameters give 47× observed; replacing only τ with the repo's gives 23×; replacing only a gives −25× to +7×; replacing both gives −40× to −12×. [SOURCE: `derived/arms.csv`] The sign is not robust; the order-of-magnitude collapse is.

## 7. What the model cannot hold

The model has one national unassimilated share and cannot express a lineage that converges nationally but not within its own state, which is the repo's finding (ladder 125). It prices no vote, so the political externality range of ladder 97 sits outside it. Fiscal balances are flows between residents, not output, and are reported here only because they are the slowest economic series; the earnings rows are the ones that belong in the model and give the same sign. Everything the paper lists as pushing m* upward (destination productivity gains, capital adjustment, return flows, equal welfare weights) is left uncorrected. First-generation attitude gaps are inflated by interviewer mode by around 20 points (ladder 135), which biases the fast attitude a upward, toward the paper's conclusion.

## 8. Limits

Global-efficiency model, not a host-country balance; TFP parameters proxied by earnings, fiscal and survey outcomes; one origin tested through one row; 29-year generation stipulated; third-plus generation self-identified and attrition-selected; the published 2019 revision unchecked. Resident groups, not admission. No policy advice.

## Sources

Clemens and Pritchett, IZA DP 9730 (2016), sha256 pinned in the lane; DHS OHSS Yearbook FY2024 Table 3; Census Bureau NA-EST2024-POP; repo lanes `acs_earnings_replication_2026_09_17`, `all_age_ledger_2026_09_17`, `ledger_stress_2026_09_17`, `norms_gen_2026_09_18`, `arrival_cohorts_2026_09_18`; ladder 67, 97, 110, 117, 125, 135.
