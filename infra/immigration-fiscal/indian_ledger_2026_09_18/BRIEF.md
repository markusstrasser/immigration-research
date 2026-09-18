# Lane: Indian-origin residents on the repo's fiscal ledger and ACS profile (2026-09-18)

## Goal
The repo uses India-born adults only as a positive-selection benchmark (scorecard N2, OI origin table row). Put them on the same ledger as the Mexican-origin groups so "do they give back to the US treasury" has a measured answer on our conventions, and measure the household-level traits that bear on ethnic coordination.

## Build
1. **Ledger.** Reuse the per-adult-year CPS ASEC ledger in `gen_ledger_extension_2026_09_16/extend_ledger.py` and `cps_generation_welfare_2026_09_16/lifecycle_ledger_by_generation.py` (read both and their RESULT.md first; do not edit them, import or copy into your lane). Groups: India-born (PENATVTY=210; verify the code against the ASEC data dictionary), US-born with an India-born parent (PEFNTVTY/PEMNTVTY; parent pointer trap `PPPOS = PEPAR + 40`), and the repo's same-age non-Hispanic white US-born reference. Adults 25–64 and all-age. Report net per adult-year, the gap against the white reference with SEs (replicate weights if the upstream scripts use them, else state the method), cell Ns, and the components (federal income tax, payroll, state-local, transfers, schooling, Medicaid). Pool the same ASEC years upstream pools.
2. **ACS 2023/2024 1-year PUMS profile** (Census API tabulate or the local IPUMS panel described in `README.md`; foreign-born is BPL>=150 there): India-born vs China-born vs all foreign-born vs US-born: BA+ and graduate share, median household income, occupation concentration (top 10 OCC share, share in computer/math and physicians), self-employment and the industry of the self-employed (accommodation NAICS 7211 for the motel claim), naturalization share by years in US, English, endogamy (spouse birthplace India, and for the US-born spouse ancestry Asian Indian), metro concentration (top 10 PUMAs/metros share).
3. **Entry class** from DHS Yearbook / USCIS H-1B Employer Data Hub: India share of H-1B approvals, of EB green cards, of family admissions, latest five years. Cache files.

## Arms that could reverse the headline
Age-standardised vs raw; household-weighted (see `research/immigration-household-weighted-correction.md`); excluding the top 1 percent of income; temporary-visa holders excluded from the payroll-tax entitlement side (they pay in and many leave; state the direction); second generation only.

## Rules
Identical to `../ncvs_victim_offender_2026_09_18/BRIEF.md` §Rules (all lanes); read it and follow it. Own only this directory. Do not commit. Verification: second run reproduces `derived/` byte-identically (`cmp`), and a gate script asserts the white-reference per-adult net equals the upstream lane's figure to the dollar.
