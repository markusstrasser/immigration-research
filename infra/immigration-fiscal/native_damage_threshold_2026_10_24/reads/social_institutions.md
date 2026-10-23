**Verdict:** no social-capital or institutions estimate checked here identifies this lineage's causal effect on US natives' aggregate output. Several adverse mechanisms have quantitative evidence. The output conversion remains unidentified; the deep-roots evidence also supports an explicit ecological scenario whose assumptions must remain visible.

# Social capital, trust, public goods, deep roots and institutions

## Log

- 2026-10-24 01:47 JST: began primary-source checks; this note owns the social/institutions evidence only.
- 2026-10-24 01:51:58 JST: downloaded and parsed the core PDFs; checked contrary trust and macro-growth findings.
- 2026-10-24 01:55:01 JST: parsed the author's original Excel files, reconstructed the paper's pre-1500 index, and passed source-anchor and coverage checks. Missing source-country indices are bounded explicitly.
- 2026-10-24 01:56:24 JST: checked the original Sturgis table visually after the text extractor encoded minus signs poorly. All timestamps above came from `date` during this dispatch.
- 2026-10-24 02:02:53 JST: promoted `extract_roots.py` and `derived/roots_inputs.json`; compile and scratch-rerun checks passed, with byte identity against the original cached extraction. Timestamp from `date`.

## Scope and evidence rule

The intervention here is removal of the entire Mexican-origin lineage, including descendants. A change in a low-skill foreign-born share, a tract racial-composition index, a room's minority share, and an ancestry-weighted historical index are different treatments. The table below therefore gives the original quantitative outcome and the missing output conversion separately. `N/I` means no identified central or finite uncertainty interval for this group's native-output effect; it does **not** mean zero. Costs and benefits receive the same transport standard. [INFERENCE]

The repo's priced account already contains fiscal public services and their response coefficients; the social companion contains volunteering, city size/schooling mix, school disruption, crime/fear/security, housing and congestion. These are overlap checks, not independent re-estimations. [DATA: `research/immigration-objections-faq-2026-09-21.md`, combining rules and entries 4, 21; `research/immigration-INDEX.md`]

## Evidence table for the parent synthesis

| Channel/mechanism | Quantitative adverse evidence, source and exact outcome | Strongest checked disconfirmation or positive evidence | Conversion per pp of low-skill immigrant share, and to this lineage | Identification and overlap |
|---|---|---|---|---|
| Residential separation reduces cross-class ties | Existing repo county result: +10 pp Hispanic share is associated with EC −0.027 (SE .006); children-weighted −.019 (.005). [DATA: `connectedness_fragmentation_2026_09_28/RESULT.md`, opening verdict; no rerun] | The same lane finds no increasing payoff with county size and a null Hispanic-share × log-population term for white household income (+.0002, SE .0026). The measure combines group composition with possible spillovers onto other residents. [DATA: same lane] | Native-output central/range **N/I**. No causal EC-to-native-income coefficient for this intervention. Multiplying EC by a mobility correlation would create an unmeasured causal bridge. | Correlation. The lineage is narrower than all Hispanics. The city-size/schooling and volunteering rows already price some potential manifestations; no new dollar row. |
| Trust/social capital: heterogeneous neighborhoods reduce cooperation | Dinesen, Schaeffer & Sønderskov (2020), printed p450: pooled partial correlation −.0256, SE .0044; p458 best-practice subset −.0283, SE .0048. Putnam (2007) Table3, pp152–153: tract ethnic homogeneity coefficient +.18, SE .04, for neighbor trust on a four-point scale; standardized beta .04. | Sturgis et al. (2011), Table1 pp71–73: log diversity coefficient on generalized-trust log odds −.026 (SE .080) after individual and neighborhood controls, versus unconditional −.301 (.049). It retains a small negative neighbor-trust association (Table2 pp74–75), so it does not erase the whole channel. Finseraas et al. (2019 WP), Tables3–4 pp18–19: random minority-roommate contact raises trust-game transfer to a minority stranger by 9.92 NOK (SE5.36; controls 11.48, SE5.89); one SD minority-room share raises it 4.23 NOK (SE2.02). | Native-output central/range **N/I** for both adverse and positive evidence. The meta partial correlation is neither a percent income change nor a slope per pp minority share. Putnam's coefficient could map an actual change in tract homogeneity to trust-scale points; no source supplies the subsequent causal native-income conversion. A Norwegian room experiment cannot be multiplied by US lineage population share. | Mostly correlational; the contact study is randomized **for contact and game behavior**, not for national immigration/output. Volunteering and crime/fear/security are already separately priced. |
| Public goods: preference conflict, failed sanctioning and maintenance | Alesina–Baqir–Easterly (1999 WP), pp18–19: a full unit increase in ethnic fractionalization is associated with about .09 less road spending **as a share of local expenditure**; reported t-statistics across the city specifications run −4.7 to −8.7. Algan–Hémet–Laitin (2011 WP), Table6 p18, full controls: fractionalization coefficient .551 (SE .130) on housing-condition dissatisfaction (1–5), 1.734 (.412) on a neglect index, and 1.137 (.260) on poor-quality index. | ABE's own within-county FE comparison, p24/TableVI, loses significance for its core outcomes after full controls; this is a design sensitivity, not proof of no effect. Algan et al.'s civil-conflict index is .062 (SE .179) in the same controlled model. Kustov–Pardelli (2018 author manuscript), pp7–10/Tables1–2, shows the apparent negative diversity association in Brazil reverses across majority-white versus minority-white samples; group composition can mimic a diversity effect. | Native-output central/range **N/I**. ABE's coefficient maps 1 pp fractionalization to roughly .09 pp of the **spending share**, not .09% of GDP. The actual index change from removal depends on all racial-group shares; it is not the Mexican-origin share. A fall in spending is not automatically a welfare loss: resources saved and service value have to be netted. | ABE correlation/lags-as-IV; Algan quasi-experimental allocation claim in French public housing, with block-clustered SEs; Kustov correlation. Fiscal spending already appears in the account. Service quality/productivity beyond that spending is unpriced, with no net dollar conversion. |
| Cultural persistence / deep roots changes institutions and productivity | Putterman–Weil (2009 revision underlying 2010 QJE), Table4 p34: ancestry-adjusted state history coefficient 1.24 (SE .42), or agriculture .153 (.054), on log GDP/person with geography controls. These are two alternative predictors, not additive channels. Their own p15 states the institutional causation path is unresolved. | Briggeman (2022), Table3 printed p92: corrected/updated population-weighted state-history coefficient −.167 (SE .303) with geographic controls, versus the original positive country-weighted slope. Its unweighted relationship remains positive; this is weight, data and functional-form sensitivity, not a universal null. Bove–Elia macro evidence below is a separate, nonnegative alternative in many samples. | Native-output central/range **N/I**. A reproducible **ecological scenario** is possible using the primary ancestry matrix and the original controlled slope, detailed below. Its result is conditional on culture/institution spillover, ancestry and universal resident-incidence assumptions; it is not a low-skill-immigrant causal estimate. | Correlation/model transport. No institutional-transmission dollar term priced. Do not add this broad GDP scenario to trust, social capital, political effects and skill externalities as if independent: it may subsume all. |
| Migration/diversity macro-productivity, possible benefit as well as harm | Bove–Elia (2017), Table6, PDF printed p9: developed countries 1960–2010 fractionalization coefficient .034 (SE .090); 2000–2010 −.428 (.190). First-stage Fs respectively 5 and 3. Dependent variable is **annual percentage GDP/person growth**, treatment **annual percentage growth of fractionalization**, not stock pp. | Table7 p10 developed-country dynamic-panel coefficient .104 (.146); full sample .087 (.043). Ghelli–Ventura (2024), Table1 p4, finds fractionalization/foreign-born-share correlation .977; Table10 p16, migration-share-growth IV coefficient .207 (.077) for 1960–2010 but .030 (.148) for 2000–2010. This disputes an independent diversity interpretation while retaining a possible migration benefit. | Native-output central/range **N/I**. A specified immigration history, change in diversity-growth path, horizon and native incidence are needed to integrate annual growth into an output level. The full lineage's current share cannot stand in for that path or be summed with local productivity estimates. | IV claims with weak instruments/transport uncertainty, global country samples, aggregate resident output. These are competing broad-output readings, not extra independent social rows. |

## Primary source records and reading notes

### Dinesen, Schaeffer and Sønderskov (2020)

[SOURCE: https://pure.au.dk/ws/portalfiles/portal/230771020/Ethnic_Diversity_and_Social_Trust_Final_version_2020.pdf ; DOI 10.1146/annurev-polisci-052918-020708]

Downloaded as `_cache/social_dinesen2020.pdf`; text via `pdftotext -layout`. The quantitative review covers 1,001 estimates from 87 studies (p441). The pooled negative partial correlation is small but not zero (p450); more locally measured diversity and neighbor trust show stronger associations. The preferred-subset result is reported on p458. The authors explicitly state on pp459–460 that the predominantly cross-sectional studies do not establish a causal effect. Their pp455–456 contact discussion includes both negative workplace panel findings and positive Norwegian experimental evidence. This supports an adverse mechanism while leaving the national native-income effect open; it does not justify treating the pooled association as a causal elasticity.

### Putnam (2007) and the Sturgis et al. (2011) re-test

[SOURCE: Putnam, DOI 10.1111/j.1467-9477.2007.00176.x; full published PDF mirror https://h16free.com/wp-content/uploads/2025/02/Putnam-2007-Scandinavian_Political_Studies.pdf]

Downloaded as `_cache/social_putnam.pdf`; relevant Table3 printed pp152–153. This is the author's reported US neighborhood regression, not a productivity estimate. The homogeneity slope is small in standardized terms (.04) and conditional on many correlated socioeconomic and crime variables. The paper discusses short-run withdrawal and the possibility of longer-run new common identities; it does not quantify a permanent native-income loss. [INFERENCE: a contemporary tract cross section cannot itself estimate the full historical removal counterfactual.]

[SOURCE: Sturgis, Brunton-Smith, Read & Allum, https://repository.essex.ac.uk/2281/2/download.pdf ; DOI 10.1017/S0007123410000281]

Downloaded `_cache/social_sturgis.pdf`; Tables1–2 pp71–75 and conclusions pp78–80. Data are from Britain's Taking Part surveys. Generalized trust and neighbor trust are distinct outcomes; only the former loses its adjusted association. PDF text renders some minus signs as `20`; `_cache/social_sturgis_table1.png` is the inspected original page verifying −.026 (.080). A null generalized-trust coefficient does not establish a zero neighbor-trust cost or equivalence to the US.

### Finseraas et al. (2019)

[SOURCE: https://www.econstor.eu/bitstream/10419/198875/1/cesifo1_wp7515.pdf ; published article DOI 10.1016/j.jpubeco.2019.02.002]

Downloaded `_cache/social_finseraas.pdf`; the numeric citations above use **CESifo WP7515**, printed pp18–19, not an unverified transcription of the journal tables. Soldiers were randomly allocated to rooms. Minority-roommate contact has positive outgroup-trust effects; effects on transfers to a majority stranger are small and imprecise (Table3: 2.65, SE7.03, without individual controls). Transfer is from a 100 NOK experimental endowment. This is an informative opposing causal mechanism; game currency is not annual welfare or output and must not be capitalized into GDP.

### Alesina, Baqir and Easterly (1999)

[SOURCE: World Bank Working Paper2108 full text https://datacatalogfiles.worldbank.org/ddh-published/0040225/1/DR0050095/public-goods-and-ethnic-divisions-wb-version_0.pdf ; published DOI 10.1162/003355399556269]

The published scan downloaded as `_cache/social_alesina_baqir_easterly.pdf` was not text extractable. Numeric/text checks therefore use the separately identified May1999 World Bank version, `_cache/social_alesina_wb.pdf`, pp18–24. The index is one minus summed squared race-group shares (p14–15); its mechanical maximum with five groups differs from a hypothetical 0–1 exposition. The city estimate is cross-sectional. Metropolitan/county IV uses earlier values of ethnicity/income, which does not guarantee exclusion of persistent local determinants. The paper itself reports the full-control FE null for its core outcomes on p24. Do not re-label the cross-section as a causal immigration estimate.

### Algan, Hémet and Laitin (2011 / 2016)

[SOURCE: checked numerical version https://docs.iza.org/dp6053.pdf ; final article DOI 10.1086/686010]

The author's newer host failed DNS and the Barcelona copy returned404; the IZA primary working paper downloaded successfully as `_cache/social_algan.pdf`. **Numbers above are October2011 WP6053, not final2016 journal-table estimates.** The allocation argument and sorting tests occupy sections3–4; Table6 printed p18 gives both adverse quality and null conflict results. This is much closer to identifying a contextual social mechanism than a country cross section, but French public-housing households differ from US natives nationally. Housing dissatisfaction/maintenance indices lack a compensating-variation or output conversion. The final journal abstract supports the same mechanism qualitatively; final tables were not substituted silently.

### Kustov and Pardelli (2018)

[SOURCE: https://alexanderkustov.org/files/Kustov_APSR2018_final.pdf ; DOI 10.1017/S0003055418000308]

Downloaded `_cache/social_kustov_pardelli.pdf`. This author manuscript includes appendix tables. Pages7–10/Tables1–2 compare public outcomes in majority-white and minority-white Brazilian municipalities and show the diversity sign depends on which group dominates. The study does not identify Mexican-origin immigration or a universal causal null. Its useful disconfirmation concerns the claim that an ethnic-fractionalization coefficient automatically isolates the effect of diversity, rather than composition. The author's broad interpretation is kept separate from what its observational design identifies.

### Putterman and Weil; deep-roots source data

[SOURCE: https://www.nber.org/system/files/working_papers/w14448/w14448.pdf ; October2009 revision in downloaded file, published QJE2010 DOI 10.1162/qjec.2010.125.4.1627]

Downloaded `_cache/social_putterman_weil.pdf`. Equation1 and worked source-country anchors are printed p11; Table4 is p34. The paper measures inherited population history, not the marginal institutional response to a recent low-skill immigrant. It explicitly leaves the route between institutions and income unresolved (p15). Hence assigning all of a country's ancestry-income association to an externality on natives is an additional causal assumption.

The author's currently linked original input files were downloaded and parsed:

| Input | Author's landing page / direct public file | Cache |
|---|---|---|
| World Migration Matrix1500–2000, v1.1 | https://sites.google.com/brown.edu/louis-putterman/world-migration-matrix-1500-2000 ; https://drive.google.com/uc?export=download&id=1BC9tdKJ_uZi8F8BvzPdo9LXQKpRxsJZ6 | `social_matrix.xls` |
| Original Statehist v3 | https://sites.google.com/brown.edu/louis-putterman ; https://drive.google.com/uc?export=download&id=1mS-KaK5sGgd3HYXSwBmMeBin_hT_8x0R | `social_statehist.xls` |
| Original agricultural transition | https://sites.google.com/brown.edu/louis-putterman/agricultural-transition-data-set ; https://drive.google.com/uc?export=download&id=1eZOMtj9iVecHgGWw-WoeR9IDqMQPcEjR | `social_agyears.xls` |

**Critical construction check:** the Statehist workbook's precomputed `statehistn05v3` includes years 1–1950. It is the wrong regressor for this paper. `extract_roots.py` reconstructs the paper's 1–1500 index from the 30 half-century columns and normalized 5% discount. The resulting unadjusted Mexico .533268 matches the paper's .533 anchor; US 0 and China .906 are additional assertions. It then applies the matrix. [CALCULATION: `derived/roots_inputs.json`, includes input SHA256]

Some source-country indices are absent in this original workbook. They cannot be silently zeroed. Bounding every missing index between0 and1 and explicitly normalizing the matrix's small row-rounding discrepancy gives Mexican ancestry-statehist .514220–.519847 and US .561744–.572933. These are **missing-input construction bounds**, not sampling intervals, not causal uncertainty, and not this lineage's measured ancestry. Shared missing values can tighten their difference if required. [CALCULATION: same extraction script/JSON]

For an explicit ecological illustration only, let `s` be this full lineage's share of the population, assign it Mexico's historical index `XM`, and assign the observed US historical index `XUS` to the mixture. The inferred counterfactual nonlineage index is `(XUS − s XM)/(1−s)`. Applying the country-regression slope `β` uniformly to natives gives the hypothetical with-minus-without log-income difference

`Δ log(native income) = −β × s/(1−s) × (XUS−XM)`.

Native-income harm as a percentage of the no-lineage scenario would be `100 × [1−exp(Δlog)]`. The original controlled slope is `β=1.24` (SE.42); the population-weighted replication slope is `β=−.167` (SE.303). This allows a source-grounded sensitivity calculation without inventing an ancestry gap. The1% crossing condition is `β × s/(1−s) × (XUS−XM) > −log(.99)` [THRESHOLD]. **The actual2024 mixed-ancestry lineage is not identified by the2000 country matrix; the formula's universal externality is assumed, not measured.** Neither the source-input bounds nor a ±1.96SE slope interval covers that causal transport failure.

### Briggeman (2022) disconfirmation

[SOURCE: https://econjwatch.org/file_download/1221/BriggemanMar2022.pdf]

Downloaded `_cache/social_briggeman.pdf`. Table3 p92 supplies the population-weighted estimate above; corrected unweighted results remain positive. The paper also reports curvature and geographic/source-data sensitivities. This matters because a claim that all ancestry-income covariance measures a permanent spillover must survive defensible weights and specifications. The replication is observational too: neither its near-zero weighted slope nor the original positive slope estimates an immigrant-treatment effect.

### Bove and Elia; Ghelli and Ventura

[SOURCE: https://wrap.warwick.ac.uk/id/eprint/81585/1/WRAP_1-s2.0-S0305750X16304466-main.pdf ; DOI 10.1016/j.worlddev.2016.08.012]

Downloaded `_cache/social_bove_elia.pdf`. Printed p5 defines both outcome and diversity treatment as annual percentage-growth rates. Tables6–7 printed pp9–10 contain the developed-country results in the table above. The adverse latest-window IV point is not the paper's only developed-country result; it comes with a weak first stage. The positive full-country result likewise does not justify aUS native-output benefit or causal transport to a low-skill subgroup.

[SOURCE: https://www.econstor.eu/bitstream/10419/295069/1/JCRE-2024-3.pdf ; DOI 10.18718/81781.33]

Downloaded `_cache/social_bove_replication.pdf`. The first journal URL failed certificate verification; an institutional mirror returned403; EconStor succeeded. Table1 p4 verifies the near-collinearity; Table10 p16 separates a migration share-growth regression. The latter is positive in long windows and nearzero in the last window. This is a quantitative opposing interpretation and a warning against an independent diversity coefficient, not a proof of no migration effect.

### Clemens and Pritchett (2016 / 2019)

[SOURCE: https://docs.iza.org/dp9730.pdf ; published JDE2019 DOI 10.1016/j.jdeveco.2018.12.003]

Downloaded `_cache/social_cp.pdf`; numerical citations use the February2016 IZA primary version already underlying the repo's calibration lane. Table1 p35 gives Mexico: adjusted initial earnings gap `.125` (SE`.00377`), within-person assimilation parameter `.0282` (SE`.00219`), sourceTFP gap `.523`, implied transmission `.239`. The fitted assimilation parameter is inferred from a cross-section by years since arrival, with age/education/sex controls; calling it a measured national TFP externality would exceed the design.

Equation3 p18 specifies `1−Atilde = γ τ φ/(1−cφ)`. Here `φ` is the buffer of unassimilated dynastic labor, approximately `m/a` in Eq2, not the full immigrant stock or lineage share. The authors examine a conservative `c=.5` calibration using PUMA earnings patterns (pp38–40); they do not identify a statistical causal upper bound. Figure9/pp40–41 places their parameter readings at dynamically efficient migration rates several times observed`.003`. Their model therefore concedes a negativeTFP spillover in principle and can quantify it **conditional on φ and causal interpretation of τ**. It does not measure this lineage's current effect. [INFERENCE]

The proper per-pp derivative in that conditional model is `∂(1−Atilde)/∂φ = γτ/(1−cφ)^2`; multiply by`.01` for a pp of **unassimilated buffer**, not a pp of all low-skill immigrants. To express a pp of immigrant stock, a source-based stock-to-buffer map is needed. Applying Mexican wage gaps to every native's TFP and treating every descendant as unassimilated would be unsupported substitutions. The repo's earlier negative-optimum exercise remains a scenario and was not rerun here.

## Gaps and what would change the result

- [GAP] Jones's book's own accessible publisher material supports a persistence thesis but supplies no checked causal native-output elasticity. The directly checked quantitative deep-roots sources are stronger evidence than a book-level synopsis. A full-book claim about a numerical Mexican-origin externality should remain unverified unless its text/table is obtained.
- [GAP] No checked study identifies the joint path from the Mexican-origin lineage's presence, through social trust or public-goods quality, to other residents' aggregate annual income. A public-goods-index coefficient and a trust-growth coefficient estimated elsewhere do not jointly identify that path.
- [GAP] No complete2024 lineage ancestry matrix, unassimilated-labor buffer or ethnic-index counterfactual was measured in this dispatch. Primary country history inputs improve an explicit scenario; they do not close the causal bridge.
- [INFERENCE] Measuring the source treatment, obtaining a credible within-country design, estimating native-specific incidence and reconciling overlap with already-priced outcomes would change whether a channel belongs in a causal sum. Without these, including weaker evidence does not produce a finite aggregate bound. It can show scenario sensitivity on either side of the1% threshold.

## Checks and paths

Run `uv run --no-project --with xlrd python3 infra/immigration-fiscal/native_damage_threshold_2026_10_24/extract_roots.py`. It reads the original Excel files from the lane's `_cache/` and writes `derived/roots_inputs.json`; `--out-dir <scratch>` writes the same named output to a scratch directory. The three paper anchors, Excel-format assertions, matrix row-mass check and explicit missing-coverage handling pass. The promoted script compiles and its output byte-matches the historical cached extraction, including country values and source hashes; a scratch-output rerun also byte-matches. No existing lane was rerun or altered; no git metadata was changed. The durable extractor and its derived JSON accompany this source note; the historical cached extractor and source files remain untouched.
