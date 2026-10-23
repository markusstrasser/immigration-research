**Verdict:** A loss near one percent is the correct scale for the stipulated R1 damage budget, but it is a threshold under a welfare convention. Neither the GDP allocation nor the open-borders arguments identify this lineage's omitted native-output effect. [CALCULATION / INFERENCE]

# Normalization, counterfactual and primary-author arguments

## Dated checks

- 2026-10-24 01:46:29 JST — brief, constitution, goals, FAQ combining rules and instrument-bias note read; RESULT stub created before substantive research.
- 2026-10-24 01:56:40 JST — primary BEA tables and pinned CPS source parsed; adopted case population and R1 rows checked. Timestamps obtained with `date`.
- 2026-10-24 02:03:51 JST — source-data deep-roots construction received; complete causal bridge remains open.
- 2026-10-24 02:07:44 JST — source audit found that the retrieved earlier Mayda working paper defines adults 18+ and low skill as no high-school degree; published-treatment definition reopened before using a vote translation.

## What the denominator measures

[SOURCE: BEA, *The 2026 Annual Update of the National Economic Accounts*, September2026, https://apps.bea.gov/scb/issues/2026/09-september/0926-nea-annual-update.htm, Tables5–6. Download: `_cache/basis_bea_annual_2026.html`.]

The script parses the actual HTML table cells, checks their year headers, and selects **2024 levels**, not the adjacent revision columns. Table6 row1 GDP is $29,381.0bn; row3 GDI $29,296.3bn. Table5 row2 compensation is $15,041.7bn; proprietors' income $1,916.0bn. The repo's world-ledger normalization remains the older rounded $29,300bn. This lane uses the revised denominator without pretending to have rebuilt its numerator. [SOURCE / CALCULATION: `../derived/bea_extracted_rows.json`]

[SOURCE: Census, CPS ASEC2025 public-use file, https://www2.census.gov/programs-surveys/cps/datasets/2025/march/asecpub25csv.zip; technical documentation https://www2.census.gov/programs-surveys/cps/techdocs/cpsmar25.pdf, dictionary section6C. The existing archive at `gen_ledger_extension_2026_09_16/_cache/asecpub25csv.zip` is opened read-only and its SHA256 checked against the source's existing pin.]

National shares use published `pwwgt0` on civilians (`PRPERTYP=2` or age<15). Native follows CPS `PRCITSHP=1,2,3`, including people born abroad to US parents and born in outlying areas; it is not exactly “born in the fifty states.” Labor income is positive `PEARNVAL`; property income is positive `INT_VAL+DIV_VAL+RNT_VAL`, as in the existing distribution loader. Native shares are **80.4383% of earnings**, **80.4755% of wages**, **87.7794% of property income**. These are survey shares, with top-income/missing-income limitations; no claim is made that they measure ownership of the whole national capital stock. [CALCULATION: `../derived/basis.json` `cps`; SOURCE: technical dictionary for the named fields]

Define an allocation proxy `Y_N = GDP × [α s_N,labor + (1−α) s_N,property]`. The central α attributes two-thirds of proprietors' income to labor: `(compensation + 2/3 proprietors)/GDI = .557034`. This two-thirds split, equal supplements incidence and use of a property-income key for the entire nonlabor residual are **assumptions**. The resulting **$24.589tn** is a normalization, not observed native GDP. Assigning no/all proprietors' income to labor gives $24.683/$24.542tn; the repo production model's α=.65 gives $24.388tn. That narrow set is **not a confidence interval** and does not cover the residual-allocation or survey-coverage uncertainty. Native welfare need not move one-for-one with this gross output proxy. [MODEL / CALCULATION]

## Population and treatment units

[DATA: `live_case.json`, case `oct16`; `main_case_2026_10_16/derived/corrections.json` `meta.population_v9`; `main_case_2026_10_16/derived/summary.json`.]

The case counts **44,903,074.086** people, of whom **42,951,314.004** are before Census coverage. The full lineage divided by the CPS published civilian population **336,727,803** is **13.3351%**. This is a declared normalization using a published population denominator and the case's adjusted numerator, not a closed national reweight or a low-skill-immigrant exposure. The case's earlier `meta.lineage.s` and `meta.population_v8` are historical and are not substituted for v9. [CALCULATION]

The observable union on the account's row4 frame is **39,712,493.331**. Mexico-born count **11,036,701.061**, or **11,482,806.169** with the case's G1 missed-person increment. No missing person's individual skill/earnings is observed. Counted Mexico-born positive earners are **4.1314pp** of all positive earners; their non-BA earners are **3.6213pp**, their HS-or-less earners **3.1031pp**. These are alternative schooling denominators, not interchangeable doses. [CALCULATION: `../calculate.py`; `../derived/basis.json`]

For Lewis, labor-force heads ages16–65 with at least one year of potential experience are used, approximating years of education within CPS attainment categories. Labor-force status is the March2025 interview's status, while annual earnings refer to2024. HS equivalents are HS/GED plus half of college without a BA. The nationwide dropout/HS-equivalent ratio is **.180142** with counted Mexico-born workers versus **.142999** without them; Δr **.0371433**. This is a nationwide current-stock proxy for a paper about metro changes in manufacturing outcomes; metropolitan nonlinearity, temporal transport and manufacturing incidence are not thereby measured. No hours-weighted or positive-earner ratio is passed off as Lewis's regressor. [CALCULATION; SOURCE: Lewis TableVII notes, `production.md`]

## The threshold is not a measured harm

[DATA: `world_ledger_2026_09_27/derived/readings_cash_oct16.csv`, `scope=A_completed`, `reading=R1`, `public_pension_share=1`, `g3_bound=zero`, weightings `equal_lambda_1.16` and `hendren_a`.]

The four executed world gains are **$218.342–288.205bn** across fiscal ends and these welfare conventions. Dividing by central `Y_N` gives **0.88797–1.17209% [THRESHOLD]**; dividing by whole GDP gives **0.74314–0.98092% [THRESHOLD]**. The first range treats an additional dollar of native output loss as one dollar of the chosen world-welfare numeraire, holds all other rows fixed, and ignores tax/wage/capital feedback. Under Hendren weights an actual lost dollar would require the appropriate recipient-specific weight. Thus this is a scale comparison rather than a re-evaluation of the weighted world ledger. **Measured range of the omitted harm: not identified.** [MODEL / CALCULATION]

“Other US residents” in that ledger excludes the complete lineage, but includes other immigrants. CPS natives include many lineage descendants and exclude other immigrants. A native-only estimate cannot be treated as an estimate for that ledger's whole nonmember population, especially when wage gains are offset by losses of prior immigrants. [DATA / INFERENCE]

The world ledger imports four current social rows from the pairing: crime victims, property crime, unreimbursed care, congestion (`world_ledger.py` `SOCIAL_PAIRING_ROWS`). Its row loop also carries the earlier wages/renters/landlords/mobility channels. It does **not** import the entire fiscal-plus-social stack or its scale/college-composition net. “Priced somewhere in the repo” and “included in R1” are separate predicates. Existing priced housing/congestion and other lanes are not redone here, and an updated full-world stack would need both group and origin counterparts rather than just subtracting another cost total. [DATA: traced caller; INFERENCE]

## Clemens, in his own terms

[SOURCE: Michael A. Clemens, *Economics and Emigration: Trillion-Dollar Bills on the Sidewalk?*, JEP25(3),2011,83–106, DOI10.1257/jep.25.3.83; verified author manuscript, CGD WP264 August2011, https://www.cgdev.org/sites/default/files/1425376_file_Clemens_Economics_and_Emigration_FINAL_0.pdf. `_cache/basis_clemens_2011.pdf/.txt`.]

The strongest argument is that much of workers' productivity depends on where they can work, while restrictions prevent mutually beneficial moves. The paper's comparison of model estimates gives gains often **50–150% of world GDP** (manuscript printedp2/Table1 printedp28), much larger than eliminating remaining goods/capital barriers; the gain belongs chiefly to people whose productivity rises, not automatically to destination natives. The table's conditional models and distinct welfare/GDP outcomes are not a realized open-borders experiment or a forecast for the Mexican-origin lineage. [SOURCE / INFERENCE]

He **explicitly concedes** destination externalities: pressure on open space, clean air, public amenities and valued cultural homogeneity could reduce global welfare gains (printedpp9–10). He says their mechanisms and magnitudes, especially at large scale, were poorly known, then contrasts possible losses with positive agglomeration and low-skill service complementarities. The manuscript supplies **no native-output percentage** for that externality list. Its 2011 observation that no documented large collapse had been established is not a measured 2026 upper bound of one percent, nor a test of the smaller R1 gain for this one group. [SOURCE / INFERENCE]

[DEGRADED: published PDF retrieval returned403; numerical/page claims above refer explicitly to the author manuscript, whose opening says forthcoming in JEP. The AEA article metadata was opened to verify the bibliographic identity.]

## Caplan and Weinersmith, in their own terms

[SOURCE: Bryan Caplan and Zach Weinersmith, *Open Borders: The Science and Ethics of Immigration*, FirstSecond2019, ISBN9781250316967. Primary book-page excerpts reproduced by Caplan on30October2019: https://www.econlib.org/open-borders-for-conservatives/ and https://www.econlib.org/open-borders-for-liberals/; original image files https://www.econlib.org/wp-content/uploads/2019/10/obp3.jpg and https://www.econlib.org/wp-content/uploads/2019/10/obp4.jpg, saved and visually read. Printed page numbers are not visible, so the filenames are not asserted to be book pagination.]

Their case joins a production argument to freedom of contract and moral equality: allowing willing workers, employers and landlords to transact can create large gains; birthplace is a weak moral reason for excluding those who would gain most. The book excerpts explicitly appeal to free markets, work, equality of opportunity and poverty reduction. The strongest version does **not** require every incumbent to gain, or claim that permission to work must include every existing welfare or voting entitlement. [SOURCE / INFERENCE]

Caplan's own28October2019 description says the book has separate chapters on native impoverishment, fiscal burden, cultural harm and political danger, followed by a chapter on targeted remedies: https://www.econlib.org/how-open-borders-measures-up/. His1November2019 explanation with Weinersmith's illustrations explicitly accepts cultural/political costs as a question and asks whether less costly remedies could address them: https://www.econlib.org/open-borders-in-foreign-policy/. Weinersmith's own2019 explanation, reproduced by Caplan, says very good reasons for exclusion could in principle exist and names crime, terrorism, welfare and cultural concerns: https://www.econlib.org/immigration-as-a-civil-right/. These are affirmative acknowledgments of the relevant objections, not evidence of their magnitudes. [SOURCE]

**At what size?** No Mexican-lineage native-output elasticity or one-percent ceiling is supplied in these directly inspected primary excerpts and author explanations. A full-book claim that they concede or rule out a particular numeric institutional loss is **not verified here**. Borjas–Katz's adverse low-education wage simulation, separately checked in `production.md`, is a subgroup wage effect and cannot supply that ceiling. The large all-world free-migration gain does not answer the lower-threshold, one-group question. [ACCESS LIMIT / INFERENCE]

The publisher page returned403 and Google Books served metadata/restricted pages for the requested substantive chapters. Recovery obtained authentic book-page excerpts from the author's2019 posts and both authors' contemporaneous explanations. This lane therefore does not fabricate chapter page citations or imply a complete read of the book. Its verdict does not depend on an argument from their silence. [DEGRADED]
