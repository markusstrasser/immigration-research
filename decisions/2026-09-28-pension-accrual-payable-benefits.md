---
date: 2026-09-28
concepts: [pension-accrual, social-security, medicare-part-a, current-law, headline-candidate]
status: adopted
supersedes: []
relations:
  - refines: decisions/2026-09-19-fiscal-program-ownership-and-period-profiles.md
evidence: infra/immigration-fiscal/pension_accrual_2026_09_28/RESULT.md
---

# 2026-09-28: The pension accrual values benefits as current law pays them, with scheduled benefits beside

## Context

The accrual lane (ladder 257) puts Social Security (OASDI) and Medicare Part A on an accrual basis beside the
September 27 case. It valued the benefits that the group's 2024 work earns at scheduled benefits, the Trustees' cost
convention. Net of the income tax on benefits under the 2025 tax law, that put the case at $433.5bn / $493.5bn
against $321.8bn / $387.4bn on cash. The tax on benefits was already on current law (the 2025 tax law), but the
benefits were not.

The operator questioned the convention: "I think most people don't expect to have the same pensions as boomers have
now in 40 years?" The parent recommended payable benefits as the central and scheduled benefits as an arm. The
operator then set the direction (16:40 JST): "move the lane ... we mostly wanna make statements about right now ...
and our models ... too much scenario planning might seem easy to attack I guess ... but the thinking has to be laid
out so that's good".

## Alternatives considered

1. **Scheduled benefits (the earlier central).** The benefit formula paid in full.
   - For: it is what beneficiaries remain legally entitled to. CBO's baseline pays it by statute (BBEDCA section
     257(b)(1)), and the Trustees' cost and the Statement of Social Insurance use it.
   - Against: it assumes a financing law that does not exist, and it sat beside a tax on benefits taken from current
     law.
2. **Payable benefits.** What the trust funds' income pays once their reserves are depleted (OASDI 2034, HI 2033).
   - For: this is what current law lets SSA pay. SSA publishes the ratios itself (Note 2025.7 Table 3), and the
     Medicare Trustees publish HI's payable share.
   - Against: the law does not say how the cut would be made. In 1983 Congress legislated a mixed fix rather than
     let a cut happen.
3. **A reform scenario**, such as a gap closed half by taxes and half by benefit cuts. This needs a forecast of
   legislation. It is the scenario planning the operator wants out of the lead.

## Decision

The central values benefits as current law will pay them (payable). Scheduled benefits stay as the arm `scheduled`,
set out beside the central with the reasoning, not leading it.

- **Lane central:** $399.1bn / $461.0bn at specifications 48 / 11, +$77.3bn / +$73.6bn over cash.
- **Arm `scheduled`:** $433.5bn / $493.5bn. It reproduces the earlier central to 1e-6.

Supporting changes:

- The payable model factor now comes from a model grid on payable benefits (+$0.02bn).
- The national check stays on the Statement of Social Insurance's scheduled basis and compares with the arm
  `scheduled`.

The central reads current law for both the benefits and the tax on them. Any case revision that takes the accrual
takes this central. Adopting the accrual into the case remains the operator's call.

## Evidence

- **What the law allows.** CBO: "Under current law, the Social Security Administration cannot pay benefits in excess
  of the available balances in a trust fund". Beneficiaries "will remain legally entitled to full benefits", and
  "the method for reducing payments is not prescribed in current law" (CBO's January 2025 OASI baseline; *CBO's 2024
  Long-Term Projections for Social Security*).
- **Measured against modelled.** $68.3bn / $62.6bn of the change is the group's 2024 payroll surplus: OASDI and HI
  tax less Social Security and Part A benefits, which cash books as income. The rest depends on the benefit level.
  At payable benefits OASDI earns 0.974 per tax dollar net of the tax on benefits, and Part A 1.32–1.41 per HI tax
  dollar. [CALCULATION: pension lane `summary.json`]
- **What the cut means.** The cut applies to a schedule that grows with wages. A medium earner turning 65 in 2065
  gets 1.65 times today's real benefit on schedule and 1.26 times at payable (TR 2025 Table V.C7; Note 2025.7's 2065
  payable share of 76.6%).

## Revisit if

- Congress legislates a solvency fix. Benefits are then valued under the new law.
- A new Trustees Report moves the depletion dates or the payable shares.
- A measured distribution of a legislated cut would place this lower-earning group away from the proportional cut.

## Supersedes

None. It refines the central of ladder 257. The earlier central is the arm `scheduled`.
