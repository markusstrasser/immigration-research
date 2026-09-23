**Verdict:** The evidence puts the 2024 on-books share of the Latin-American-born imputed unauthorized's CPS wages at about **0.52** (Mexico-born 0.53, other Latin-American-born 0.55), range **0.42–0.63**. That is below the audit's unsupported 0.60 and above SSA's 2010 head count of 0.44. At that share, audit row 2 (`cps.md` row 1) is **+$12.4bn to +$14.0bn** on the main case, range +$8.9bn to +$17.8bn, against the audit's +$9.9–11.3bn at 0.60. Evidence level **C, a modelled share**: no source found measures the 2022–2025 share. The figure starts from SSA's 2010 decomposition and adjusts it for dollar weighting, SSA's own projected erosion and the growth of work-authorized "protected" statuses; every adjustment is an assumption stated below. Survey under-reporting of off-books pay would lower the effect by $0.9–2.4bn if the CPS misses 10–25% of that pay; no source measures it for this population.

Model: claude-opus-5-5[1m] (Opus 5.5, 1M context), `onbooks-share` lane, 2026-09-23.

## The three questions

1. **Share of unauthorized earnings on W-2 payroll, 2022–2025.** No measurement exists in what I found. The last actuarial decomposition is SSA's for 2010: 3.1M of 7.0M unauthorized workers (44%) paid payroll tax [SOURCE: SSA Actuarial Note 151, pp.3–4]. Weighted by dollars and moved to 2024, the constructed share is 0.53 for the Mexico-born and 0.55 for other Latin-American-born, range 0.42–0.63 [INFERENCE; construction below]. The only Mexico-specific measure is older and lower: undocumented Mexican migrants reported Social Security withholding in 24% of their U.S. work-years in 1993–2008 [SOURCE: Burtless & Singer 2011, Table 1, p.23].
2. **Share of unauthorized households filing federal returns.** About 0.3–0.6, central about 0.45 [INFERENCE]. In TY2022, 3,791,421 returns carried at least one ITIN, and in TY2023 over 2.4 million had an ITIN holder as primary filer [SOURCE: National Taxpayer Advocate 2024, research report 3, Fig. 5.3.2 and text]. The CPS tax model files for 8.51M units with an imputed-unauthorized head or spouse. Those counts give ratios of 0.45 and 0.28 [CALCULATION: `derived/onbooks_inputs.json`]. The ratios are loose in both directions. ITIN returns include non-unauthorized filers, unauthorized people with SSNs (DACA, TPS, work-permit holders, overstayers) file without an ITIN, and the Borjas residual over-assigns status. The one survey filing rate, 32%, dates from 1975 [SOURCE: North & Houstoun 1976 as quoted by ITEP 2024, p.27].
3. **Row 2 at the evidence-weighted share.** +$12.4bn to +$14.0bn at the central, +$16.0–17.8bn at the low share and +$8.9–10.2bn at the high share [CALCULATION: `onbooks_rekey.py` → `derived/onbooks_split.csv`].

## Source table

Pew and IZA pages are PDF pages; the others are printed pages. Grades: A = administrative count or official measurement fit for this use; B = primary and relevant but dated, partial or indirect; C = an assumption, or a number read only through a secondary source; D = too old to weigh.

| # | Source | Data year | Population and method | Mexico-specific | Number (page) | Implied share | Grade |
|---|---|---|---|---|---|---|---|
| 1 | SSA OCACT, Actuarial Note 151 (Goss et al., April 2013) | 2010 | All unauthorized workers. Actuarial split of an assumed worker count (other immigrants "as likely to work as legal permanent residents", p.2) into Master Earnings File, suspense file and underground | no | 8.3M other-immigrant workers, 1.3M on temporary visas, 0.6M overstayers with own SSN, 0.7M SSNs from fraudulent birth certificates, 1.8M using an SSN not their own, 3.9M underground (p.2); "about 3.1 million unauthorized immigrants working and paying Social Security taxes" (p.3); unauthorized workers 4.8M in 2000, 7.0M in 2010 (p.4); taxable earnings "about 80 percent of the average level for all workers … about $34,000" (p.4) | 0.44 by head count; 0.44–0.59 by dollars depending on the wage gap (below) | B |
| 2 | Same note, trend | 2000; 2040 projection | Same | no | Underground 2.2M of 4.8M in 2000; 9.0M in 2040; suspense-file workers 1.8M → 3.4M; fraudulent-ID SSNs 0.7M → under 0.2M (p.4). SSN issuance at birth, birth-certificate scrutiny and E-Verify "would limit the reporting of their earnings as taxable" (p.3) | 0.54 (2000) → about 0.32 (2040) [CALCULATION] | C (projection) |
| 3 | SSA OCACT, Actuarial Note 148 (Wade et al., March 2009), section "Employment of the Other-Immigrant Population" (HTML) | 2000; post-2001 arrivals | All employed other immigrants, temporary legal included; assumption table | no | 2000: OASDI-covered 33%, noncovered student 8%, suspense 16%, underground 43%. "Arrive after 2001": 10%, 6%, 23%, 61% | 0.49 (2000); 0.33 for post-2001 arrivals, temporary legal included | B |
| 4 | Burtless & Singer, CRR WP 2011-2 (MMP) | 1993–2008 person-years | Mexican migrant household heads from MMP sending communities; yearly self-report of Social Security withholding; two-thirds of person-years in the first five years of a stay (p.8) | **yes** | Undocumented 24% yes, 72% no, 4% unknown; LPR 69/28/3; all statuses by stay: over 8 years 58% against 38% overall; by wage: low 34%, middle 42%, high 51% (Table 1, p.23). Never-legalized 28%, pre-legalization 32%, "about 30 percent" (p.19). Taxes collected on "only about $5 out of every $10" of CPS wages of Mexican and Central American immigrants in 2000–2006, all statuses (p.14). Five years after IRCA legalization, 92% of Mexican workers had taxes withheld (p.19, citing the Legalized Population Survey) | 0.25–0.32 by head count | B |
| 5 | Brown, Hotchkiss & Quispe-Agnoli, IZA DP 3936 (2008) | 2004 | Georgia UI wage records; workers with invalid SSNs against an estimated undocumented share | no | 1.2% of workers flagged against 4.5% estimated undocumented: "capturing about 26 percent" (PDF p.13). The Hotchkiss–Quispe-Agnoli–Ríos-Avila variant reports 22%. Workers using someone else's valid SSN are missed | 0.22–0.26 **lower bound** of the payroll share | B |
| 6 | CBO, *Effects of the Immigration Surge* (July 2024, pub. 60165) | 2024–2034 projection | Surge population; microsimulation assumption | no | "rates of compliance among the surge population are 15 percent lower for income taxes and 10 percent lower for payroll taxes" than the total population (p.10); "about half of adults in the surge population will receive employment authorization and … be equally likely to pay taxes" (p.11); fn.16 cites Note 151 (p.12) | 0.70 (income tax) and 0.80 (payroll) for the unauthorized half, if earnings split evenly [INFERENCE] | C |
| 7 | ITEP, *Tax Payments by Undocumented Immigrants* (July 2024) | 2022 | 10.9M undocumented; incidence model with an assumed contribution rate | no | Literature range "50 to 75 percent (CBO 2007)" (p.26); "we target a 60 percent contribution rate … under the federal individual income tax", sensitivity 50 and 75 (p.27); a resident with the same income profile contributes 92% (p.28) | 0.60 (income tax) | C |
| 8 | Cornelius & Lewis 2006, read only as quoted by ITEP (p.26) | about 2005 | More than 700 undocumented migrants from Mexico | **yes** | "75 percent paid federal income taxes via withholding, filing an income tax return, or both" | 0.75 by head count, any payment | C |
| 9 | North & Houstoun 1976, as quoted by ITEP (pp.26–27) | 1975 | About 800 undocumented | not stated | 73% had income tax withheld; 32% filed | 0.73 withholding | D |
| 10 | Pew Research Center, Passel & Krogstad (21 Aug 2025) | 2023 | 14.0M unauthorized; residual method plus administrative data | counts only | About 6M "had some protection from deportation" (p.6): asylum applicants 2.6M, parole 0.7M, crime victims 0.7M, TPS 0.65M, DACA 0.6M, border releases 1.0M (p.8). Mexico-born about 4.3M; other countries 9.7M (p.11). 610,000 active DACA, "mostly from Mexico" (p.24) | Composition input: work-authorized share | A (counts) |
| 11 | National Taxpayer Advocate, 2024 Annual Report, research report 3 (ITIN processing; text read via Exa, PDF blocked to curl) | TY2022–2023 | All returns with an ITIN | no | 3,791,421 returns with at least one ITIN in TY2022 (Fig. 5.3.2); over 2.4 million with the ITIN holder as primary in TY2023; TY2022 tax before credits $18.2bn, after credits $14.5bn; median AGI $31,033 (Fig. 5.3.3 and text) | Filing indicator | A (counts); C as an unauthorized filing rate |
| 12 | SSA Long-Range OASDI Projection Methodology, 2026 edition (text via Exa; PDF blocked) | current | Model structure | no | Employed other-than-LPR workers split into MEF-posted, ESF-posted and underground; `EO_UND = EO – EO_MEF – EO_ESF` (eq. 2.1.14); no shares published | none | — |
| 13 | Bohn & Lofstrom, IZA DP 6598 (Russell Sage 2013) | 2008–2009 | Arizona's E-Verify mandate (LAWA); likely-unauthorized Hispanic noncitizen men with at most high school; synthetic control | largely | Employment fell "slightly more than 11 percentage points" (PDF p.23); self-employment rose 8.3 points (PDF p.25), "from 8 to 16 percent" (PDF p.37) | Direction: mandates move work off payroll | B |
| 14 | Bollinger, Hirsch, Hokayem & Ziliak (JPE 2019) | 2005–2010 | CPS ASEC linked to SSA Detailed Earnings Records | no | Off-the-books earnings do not appear in the DER, "though they could be reported in the ASEC" (data section; page not pinned) | Direction for item 3 | B (qualitative here) |

## Gate

`onbooks_rekey.py` imports the audit script's constants and imputation and repeats its arithmetic. It never calls the audit's `main()`, which writes into the audit's directory. At 0.44, 0.60 and 0.75, every per-key delta matches the audit's `derived/cps_status_keys.csv` to 1e-9. The printed table reproduces within rounding. The script stops with `[BLOCKED]` if either check fails. [CALCULATION: `derived/onbooks_gate.csv`]

| On-books | Receipts shared / personal | Refundable, non-PTC | Net | Audit's printed net |
|---|---:|---:|---:|---:|
| 0.44 | −20.38 / −19.20 | −3.38 to −4.01 | +15.19 to +17.00 | +15.2 to +17.0 |
| 0.60 | −14.51 / −13.67 | −3.19 to −3.78 | +9.89 to +11.32 | +9.9 to +11.3 |
| 0.75 | −9.04 / −8.52 | −3.01 to −3.57 | +4.95 to +6.03 | +5.0 to +6.0 |

The script's parameter scales each imputed-unauthorized person's wages, liabilities, FICA-worker flag and ACTC by one number. Scaling every person's dollars by *s* is the same as keeping a fraction *s* of the group's dollars. The parameter is therefore a **dollar-weighted** share of CPS-reported pay, not SSA's head count.

## Computation

The 2024 share for each origin group is
share = *p* × *s*_auth + (1 − *p*) × *h* × *f*
[INFERENCE; `evidence_shares()` in `onbooks_rekey.py`]. The terms are:

- ***h***: the head-count on-books share of the never-authorized and overstayers.
  - Central: SSA's 0.443 for 2010, less SSA's own projected erosion to 2024. SSA's p.4 figures imply about 0.32 by 2040 (overstayers held at 0.6M), so linear erosion to 2024 is 0.058. The Mexico-born take half of it, because the projection assumed 1.5M new other immigrants a year and Mexican inflows largely stopped after 2008. Result: 0.414 for the Mexico-born and 0.385 for others.
  - Low: MMP's 25% for undocumented work-years, scaled by its duration gradient for stays over eight years (58/38), giving 0.38 for the Mexico-born; Note 148's 0.33 for post-2001 arrivals for others.
  - High: 0.443 with no erosion.
- ***f***: the dollar factor.
  - It is 1.0 if on- and off-books workers earn alike.
  - It is 0.80/*r* under SSA's assumption that on-payroll unauthorized workers earn 80% of the all-worker average. I read SSA's comparator as uncapped, because 0.8 × the 2010 average wage index of $41,674 [TRAINING-DATA: SSA AWI series] is $33,339, the note's "about $34,000" [INFERENCE]. *r* is the CPS mean wage of the imputed unauthorized wage earners over all wage earners: 0.606 for the Mexico-born and 0.638 for others [CALCULATION]. That gives *f* = 1.32 and 1.25.
  - The central uses the midpoint. MMP's coverage-by-wage gradient (34/42/51%) supports an *f* above 1 but nearer 1 than SSA's.
- ***p***: the dollar share held by work-authorized "protected" people (DACA, TPS, parole, asylum work permits).
  - Mexico-born: 0.08 / 0.11 / 0.15. The 0.11 central is about 0.5M DACA recipients against 4.3–4.6M. Pew says DACA is "mostly from Mexico"; I read that as 60–100%.
  - Others: 0.15 / 0.25 / 0.35. Pew's 6M protected, less roughly 0.5M Mexican DACA recipients, leaves about 5.5M non-Mexicans out of 9.7M [INFERENCE], not all with work permits. In the CPS, 39% of the group's wages come from arrivals in 2020–2025.
- ***s*_auth**: the on-books share of the work-authorized: 0.80 / 0.90 / 0.92. The 0.92 is the post-legalization withholding rate for Mexican workers (Burtless & Singer p.19) and ITEP's same-profile contribution rate (p.28).

| Case | Mexico-born | Other Latin-American | Uniform equivalent | Receipts shared / personal | Refundable non-PTC | **Row 2** |
|---|---:|---:|---:|---:|---:|---:|
| Low | 0.415 | 0.400 | 0.416 | −21.25 / −20.02 | −3.41 to −4.04 | **+16.0 to +17.8** |
| Central | 0.526 | 0.550 | 0.524 | −17.29 / −16.28 | −3.29 to −3.89 | **+12.4 to +14.0** |
| High | 0.635 | 0.683 | 0.631 | −13.38 / −12.60 | −3.17 to −3.75 | **+8.9 to +10.2** |

[CALCULATION: `derived/onbooks_split.csv`; the uniform equivalent is the single share with the same mid-range effect, from `derived/onbooks_grid.csv`]

- **The origin split matters little.** Holding the Mexico-born at 0.50, moving others from 0.40 to 0.80 raises the effect by only about $1bn (+13.0–14.6 to +13.9–15.7). A higher share outside the target shrinks the denominator less, which lowers the target's key share further.
- **The component split matters little.** Wage keys at 0.50, income-tax keys at ITEP's 0.60 and ACTC at 0.60 give +11.8 to +13.3bn, close to the central.
- **Against the audit.** The evidence central sits $2.5–2.7bn above the audit's 0.60 row. The audit's 0.44 row (+15.2–17.0) lies inside the evidence range, near its low-share end.

## Survey under-reporting (brief item 3)

It pushes the other way. The CPS records some off-books pay; off-the-books earnings are absent from SSA's earnings records "though they could be reported in the ASEC" [SOURCE: Bollinger et al. 2019]. If the survey misses a fraction *u* of off-books pay, the CPS dollars already lean toward on-books pay. The factor to apply to CPS dollars is then σ/(σ + (1 − *u*)(1 − σ)), above the true on-books share σ [CALCULATION].

No source measures *u* for unauthorized workers. The nearest analogue is self-employed under-reporting to household surveys, about 25% [SOURCE: Hurst, Li & Pugsley 2014, as verified in `informal_channel_2026_09_16/RESULT.md`; not re-read here]. At *u* = 0.10 the central becomes +11.5 to +13.1bn; at *u* = 0.25 it becomes +10.0 to +11.5bn. The central therefore moves by −$0.9bn to −$2.4bn. The CPS hot deck works the other way in an unknown amount: it fills nonrespondents' earnings from donors.

## Disconfirmation

**Sources that put the share above 0.75.**
- CBO's 2024 assumption implies about 0.80 for payroll among the surge's unauthorized half. Its only cited evidence is Note 151, which gives 0.44.
- Cornelius & Lewis (75%) and North & Houstoun (73%) count anyone who paid *any* income tax through withholding, a return or both. They are head counts, from ITEP's quotation only (and 1975 data for North & Houstoun).

None of the three is a dollar-weighted payroll measure, so none sets the central. They do bound the high case: a share of 0.75 needs every adjustment to go the favourable way at once.

**Sources that put the share below 0.44.**
- MMP undocumented work-years: 0.24–0.32 by head count, Mexico-specific but 1993–2008 and weighted toward early stays.
- Georgia UI invalid-SSN capture: 0.22–0.26, a lower bound by construction. It matches SSA's own suspense-file class, 1.8M of 7.0M = 0.26 in 2010.
- Note 148's 0.33 for post-2001 arrivals, temporary legal workers included.
- SSA's own path to about 0.32 by 2040.

These carry the low case. They do not carry the central, for two reasons. The 2024 Mexico-born stock is long-settled: in the CPS only 20% of its wages come from 2020–2025 arrivals and 42% from arrivals before 2002 [CALCULATION]. And about 40% of the 2023 unauthorized had deportation protection, against 4% in 2007 [SOURCE: Pew p.6].

**E-Verify.** Arizona's mandate moved likely-unauthorized men from wage work into self-employment. Wage employment fell by 11 points and self-employment rose by 8.3 points [SOURCE: Bohn & Lofstrom, IZA DP 6598, PDF pp.23, 25]. Universal state mandates spread after 2010, so this pushes the 2024 share down, behind SSA's projected erosion. A national size is not identified [GAP].

**Composition cuts both ways.** Growth in protected statuses raises the share for others more than for the Mexico-born. The split table shows this moves row 2 by about $1bn.

## Related effect not priced

The audit zeroes EITC for every imputed-unauthorized person. DACA, TPS and other work-permit holders hold SSNs valid for work and can claim it. With *p* = 0.11 to 0.25, the refundable-side reduction is overstated by roughly that fraction of its EITC part: under $1bn, raising the net cost [INFERENCE]. This is outside the on-books question and is not in the numbers above.

## Gaps and coverage

**Covered.** Sources 1–14 above. SSA pages were read from the Wayback `id_` copy of Note 151, because ssa.gov answers curl with an Akamai 403; the fiscalpolicy.org mirror is byte-identical in text. CPS inputs are from ASEC 2025 with the audit's status imputation.

**Skipped, with reasons:**
- **OCACT letters for 2019–2025 bills** (Dream and Promise, Farm Workforce Modernization, Dignity Act): not searched within the turn budget. They are the most likely place for a newer SSA on-books fraction [GAP].
- **SSA OIG, GAO and TIGTA reports on the earnings suspense file, 2015–2025:** not pulled. GAO states the unauthorized part of the file is unknown, so annual file totals cannot give a share without an assumed unauthorized fraction [GAP].
- **NAS 2017, chapter 8:** not read within the budget [GAP].
- **CBO 2007 (the 50–75% range) and CBO's 2013 S.744 estimate:** the 2007 range was read only through ITEP; the 2013 estimate was not searched.
- **Cornelius & Lewis 2006 and North & Houstoun 1976:** read only as ITEP quotes them.
- **Borjas 2017:** supplies the imputation rule and has no payroll measure.
- **Feinleib & Warner 2005:** its "about one-half" appears only as quoted in an Orrenius–Zavodny 2017 conference draft. It is consistent with 0.44–0.54 but not used.
- **The self-employment key:** out of scope. `SE_VAL` gives the imputed unauthorized a 0.2% self-employment share, implausibly low; the audit already flags that this key does not reproduce ($0.5bn line).

**If re-dispatched, next queries:**
- `site:ssa.gov/oact/solvency` for immigration-bill letters from 2019 on, looking for "underground" or "currently work";
- the latest SSA OIG earnings suspense file audit, for tax-year totals;
- the NAS 2017 chapter 8 compliance assumption;
- Census CES linkage work on W-2 presence among likely-unauthorized ACS or CPS respondents.

## Files

- `onbooks_rekey.py`: gate, grid, splits, share construction and CPS inputs. Run from the repository root with `PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/onbooks_share_2026_09_23/onbooks_rekey.py`.
- `derived/onbooks_gate.csv`, `onbooks_grid.csv` (uniform 0.30–0.90), `onbooks_split.csv` (origin, component, evidence and under-reporting cases), `onbooks_inputs.json` (wage ratios, arrival shares, modelled filing units, construction inputs), `run_log.txt`.
- `_cache/` (ignored): the PDFs and text read here: Note 151, CBO 60165, ITEP 2024, CRR 2011-2, Pew 2025, IZA DP 3936 and 6598.
