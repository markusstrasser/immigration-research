# Lane brief: build the next main-case revision as a candidate (not adopted)

Date 2026-09-28, 02:20 JST. Parent session immigration-research-1c. Worker: `mainbuild`, which built the September 27
case (`main_case_long_run_2026_09_27`, case `sept27`).

The September 27 decision (`decisions/2026-09-27-main-case-capital-return-and-long-run-responses.md`, the bullets
"This is a confirmed defect, and its fix is deferred" and "A second known defect waits for the same revision")
queues two fixes and a joint road scenario for the next revision. Adoption follows the propagation, so that consumer
lanes move once. The operator decides; building the candidate now lets him decide on numbers.

## Items

1. **Transfer consolidation** (conceptual audit 3db388d §7).
   - Public housing's operating subsidies sit both on the rental line and in the enterprise surplus, keyed 0.0752
     against 0.1172. Consolidate the transfer before keying, so one attributed amount sits on both legs.
   - Positive control: today a synthetic $1bn on both legs lowers the group's cost by $0.041–0.043bn. After the fix
     it must move it by 0 (1e-9).
   - Expected about +$0.2bn; the bound is +$2.53bn.
2. **Production inputs on the account's weights** (conceptual audit ffcce20 §C).
   - The production model uses the unweighted CPS population (40.90m). The account reweights the Mexico-born
     outside California and Texas: naturalized × 0.856, noncitizens × 0.778 (39.71m).
   - First reproduce `conceptual_audit_2026_09_27/probe_production.py`. P+F falls from 13.32 to 11.68 (GDP
     normalization, specification 48) and from 8.79 to 7.68 (cash, specification 11), which is +$1.64 / +$1.11bn.
   - Then carry the reweighted production through the package.
3. **The joint road scenario.** Entry 239's rating: "the road response ... is not varied jointly with road capital
   and congestion". Vary the long-run road response, the road capital return and the congestion item together, as
   the decision describes. Report it as the candidate's road arm and say whether it belongs in the range or beside it.
4. **Labelled variant, beside the range: public pay** (adversarial audit 61b4eac §1).
   - The production model changes public workers' wages, but the budget does not charge their employer.
   - Build one consistent scenario: charge public employers the production model's wage change for public workers
     in each skill group (CPS class of worker), with matching payroll.
   - Report its sign and size at both ends. It is not added to the range.

## Rules

- Create a new lane in this directory with case name `sept28_candidate`. Import the September 27 package. Do not
  edit any existing lane, the engine or the adopted payload.
- Report old → new at fixed specifications (48 low, 11 high): each item alone, then items 1–3 together. Also give
  the sign break-even and the outer range.
- Gates as in the September 27 lane: every added piece adds exactly, and no other line moves.
- Two runs byte-identical. Write `RESULT.md` first with `**Verdict:** pending`, and append as you go.
- No commits, staging or stash. Do not edit research/, decisions/, INDEX, FAQ or the ladder.
- Final message: the RESULT path and at most ten lines, including the candidate band.
