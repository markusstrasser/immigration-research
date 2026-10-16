# Failure regressions

- **2026-10-16: combined TAXSIM payroll is not a reliable total.** The pinned
  local binary returns $28,653.20 combined FICA on $200,000 wage-only earnings,
  versus $26,706.40 under the 2024 SSA cap. At $210,000 wage-only earnings it
  reports zero Additional Medicare Tax instead of $90; its federal total
  includes its named `addmed` component. The new calculation never uses `fica`,
  replaces `addmed` once with the IRS formula, and tests high-wage, joint and
  self-employment examples. This does not establish a defect in earlier lanes:
  they did not use `fica` for their payroll allocation. Their income-tax uses
  retain the pinned kernel's small Additional Medicare discrepancy; changing
  those historical calibrations is deferred to a separately measured audit.
- **2026-10-16: adult-weight identity initially tested noncivilian records.**
  The exposure population is civilian. The fail-loud gate now tests exactly that
  declared universe, plus keyed native-calibration factors. No weights were
  altered to make the check pass.
- **2026-10-16: fractional shocks on integer raw columns.** Pandas rejected a
  noninteger earnings change. Scenario copies now cast all three earnings fields
  to floating point before changing them; the regression uses a fractional net
  self-employment change and confirms the raw baseline remains unchanged.
