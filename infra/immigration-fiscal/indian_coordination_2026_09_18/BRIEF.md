# Lane: co-ethnic coordination among Indian immigrants — what is measured (2026-09-18)

## Question
Is there evidence that Indian immigrants in the US coordinate along ethnic lines (hiring, promotion, contracting, visa sponsorship, entrepreneurship, caste) beyond what skill and occupation mix predict, and what does it cost or gain natives? Literature and administrative records; no model adjudication of motives.

## Steel-man first
Write the strongest benign account before the evidence: networks cut information and trust frictions (referrals, credit, franchising), raise trade/FDI with the origin country, and any concentrated high-skill group shows the same clustering. Then test it.

## Evidence to fetch and grade (every author, year and number below is a pointer from memory: VERIFY against the primary before citing; if it does not check out, say so)
1. **Hiring/discrimination record.** Federal suits and verdicts alleging preference for Indian/South Asian workers at IT staffing firms (Cognizant jury verdict ~2024, Infosys, TCS, Wipro, HCL); EEOC charges and DOJ Immigrant and Employee Rights settlements on H-1B preference. For each: court, docket, stage, finding, workforce shares in evidence. Dockets and rulings are the source; press only to locate.
2. **H-1B structure.** USCIS H-1B Employer Data Hub and DOL LCA disclosure files: India-born share of approvals, share going to outsourcing firms, wage levels (Level I/II share) at those firms vs product firms. Papers on native effects: Doran–Gelber–Isen lottery, Bound–Khanna–Morales, Glennon offshoring, Mayda et al. 2017 cap cut, Kerr–Lincoln.
3. **Referral and manager co-ethnicity.** Any causal or quasi-experimental paper on co-ethnic managers and hiring/promotion in US tech or elsewhere (Åslund–Hensvik–Skans Sweden; Giuliano–Levine–Leonard retail), and anything specific to Indian managers.
4. **Entrepreneurial niches.** Kerr–Mandorff on ethnic concentration in self-employment (Gujarati motels), AAHOA ownership share claims and their source; Dunkin/7-Eleven franchise claims only if sourced.
5. **Inventor/VC/CEO networks.** Kerr ethnic patenting; co-ethnic VC funding papers (Hegde–Tumlinson; Bengtsson–Hsu); evidence on whether co-ethnic deals perform better or worse (the test of favouritism vs information).
6. **Caste.** Cisco/California CRD case outcome, Seattle ordinance, SB 403 veto, Equality Labs survey and its methodological critiques (Carnegie IAAS caste items as the probability-sample alternative).
7. **Comparison groups.** The same measures for Chinese, Korean, Israeli, Russian-speaking tech workers where a paper reports them, so the India figure has a base rate.

## Disconfirmation (mandatory)
Search explicitly for null or contrary findings: audits showing no co-ethnic preference, suits dismissed on the merits, performance evidence that co-ethnic hires/deals do as well or better.

## Deliverables and rules
`RESULT.md` opening `**Verdict:**`, then a claim table (claim · best source · evidence level · verified Y/N · quote), sources fetched vs skipped with reasons, and a draft memo section. Tag every number [SOURCE]/[INFERENCE]/[UNVERIFIED]/[TRAINING-DATA]; verbatim quotes only from fetched pages; save key sources with `save_source`/`save_paper`. Read `CLAUDE.md` and `notes/llm-bias-caveat.md` first. Own only this directory; never edit `research/`; do not commit; no policy advice. At most 3 research epochs of 12 turns; update RESULT.md after each.
