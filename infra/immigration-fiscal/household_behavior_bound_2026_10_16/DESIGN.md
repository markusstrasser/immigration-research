# Direct household work response beside v9

Frozen before running fiscal response scenarios, 2026-10-16. A read-only roster
probe has already shown the exposure counts; this is not a preregistration of
those counts. No fiscal response results have been inspected.

The question is whether changes in the work of remaining adults in directly
affected households can be dismissed as fiscally immaterial. The raw material is
the pinned 2025 CPS ASEC person, relationship, income and replicate-weight files
(income year 2024), with v9's observed membership completion. Unlocated lineage
additions and Census-missed people have no household crosswalk. Remaining people
are therefore conditional nonmembers, not proved to have no Mexican ancestry.

Compute two nested exposure groups: every remaining civilian adult sharing a
household with an observed departing member; and adults in such households with
a departing adult and another remaining person under 13, 65+, or reporting a
disability. The second is a broad care-need proxy, not observed caregiving. It
does not cap all caregiving or all household adjustment.

Hold the surviving population and claimant links fixed. Scale positive wage and
net self-employment income of exposed adults by -10%, -25%, -50%, -100%, +10%,
+25%, +50%, and +100%; preserve self-employment losses and other income. Separately
give currently nonworking exposed adults $10,000 annual wages as an illustrative
entry arm. This is a dollar perturbation, not a measured wage or hours response.
Both directions matter: lost help can reduce work, while lost household income
can induce additional work. Do not choose an elasticity from these scenarios.

Reconstruct baseline-after-removal returns once, then compare changed-after with
baseline-after using pinned local 2024 TAXSIM. Include net federal/state income
tax (refundable credits included) and employer plus employee payroll taxes,
deduplicating Additional Medicare Tax. Report statutory survey-dollar responses,
without treating accounting allocation multipliers as marginal tax rates. This
is not an exact rerun of v9's calibrated item 11. Provide SNAP sensitivities using
the existing pinned annualized FY24/FY25 rules, zero/capped shelter deduction,
and existing-participation/full-takeup-for-newly-eligible arms. Keep the original unit-income
residual, deductions and unit weights fixed across earnings perturbations.

Primary materiality reference: 5% of the v9 **cash** lower endpoint, a declared
decision convention. Also show 5% of the accrual lower endpoint for scale only.
Locate any crossing on the prescribed response grid; interpolate only as a
diagnostic, never as an exact nonlinear tax threshold. Do not add this partial
cash response to the accrual headline. Earned pension/Medicare promises, health
coverage responses, consumption taxes, relocation and market-wide effects remain
unpriced. Failure to cross the reference cannot establish that total feedback is
small. Crossing shows a consequential unresolved channel, not a causal estimate.

Validation: raw archive hash; keyed membership/relationship joins; adult weights;
complete, nonduplicated representation of exposed earners; zero-response
identity; unchanged-return isolation; independently hand-checkable payroll and
credit fixtures; fixed SNAP gross-income residual; full signed replicate-weight
aggregation before standard errors; deterministic rerun. External correctness
anchors are Census raw records and dictionaries, NBER's pinned statutory kernel,
and USDA/CFR rules. Independent review checks interpretation and implementation.

Implementation correction after the first fiscal run: use the current
`snap_arm.after_benefit` eligibility-loss rule, rather than the older unclipped
reported-level residual. Existing recipients losing financial eligibility stop
receiving benefits; previously eligible nonparticipants remain nonparticipants.
Newly eligible units receive zero or full modeled benefits. This correction
reuses the current removal lane's rule; it does not select a scenario by its
result. The initial tax response grid is unchanged.
