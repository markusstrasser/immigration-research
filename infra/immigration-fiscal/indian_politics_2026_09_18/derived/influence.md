claude-opus-5[1m]

**Verdict:** Indian American organised influence is officeholder-heavy and money-heavy but institutionally thin. Every one of the six Indian-origin members of the 119th House is a Democrat (verified against the House Clerk's official roster); there are zero Indian-origin US Senators and zero sitting governors. Individual campaign giving ran roughly 3:1 Democratic in 2020 ($46.6m vs $16.3m, name-classifier estimate) — a genuine, sizeable money flow. The named ethnic *organisations*, by contrast, are small: the four advocacy bodies together report about $7.4m of annual 990 revenue, and the two ethnic PACs (USINPAC, Indian American Impact Fund) raised $18k and $219k respectively in the 2024 cycle — trivial by federal standards. Diaspora attitudes toward Indian domestic politics are lukewarm-positive and stable: Modi approval 47% (2024, n=1,206, YouGov online panel), BJP identification 28% against Congress 20%, with 51% answering "don't know".

Scope: Q3 of the `indian_politics_2026_09_18` lane — organised influence.
Date of research: 2026-09-18. All fetches this date unless noted.

---

## 1. Officeholders by party

**House — VERIFIED against the official House Clerk roster** (`https://clerk.house.gov/xml/lists/MemberData.xml`, 441 member records parsed, fetched 2026-09-18). This is the Clerk's own machine-readable roster, not a news listicle.

| Member | State/District | Party |
|---|---|---|
| Ami Bera | CA-06 | D |
| Ro Khanna | CA-17 | D |
| Raja Krishnamoorthi | IL-08 | D |
| Shri Thanedar | MI-13 | D |
| Suhas Subramanyam | VA-10 | D |
| Pramila Jayapal | WA-07 | D |

[SOURCE: https://clerk.house.gov/xml/lists/MemberData.xml, fetched 2026-09-18]

**Count by party: 6 Democrats, 0 Republicans.** Note the identification step is mine, not the Clerk's — the roster carries no ethnicity field, so the *party and district* are primary-verified while *"is Indian-origin"* rests on the members' own public biographies. Gabe Amo (RI-01, D) surfaced in the same name sweep and is **excluded** — he is of Ghanaian/Liberian descent, not Indian.

**Senate: [GAP].** `https://www.senate.gov/general/contact_information/senators_cfm.xml` returned **HTTP 403** (bot wall) on 2026-09-18, so I could not machine-verify the Senate roster. Kamala Harris (D-CA), the only Indian-origin Senator to date, left the Senate in January 2021; on that basis the current count is believed to be zero, tagged [UNVERIFIED] pending a primary fetch.

**Governors / statewide: [GAP].** `https://www.nga.org/governors/` fetched HTTP 200 (140 KB) but the governor list is JS-rendered — a grep for Indian-origin names returned zero hits, which is a false-zero risk, not evidence. Historically Bobby Jindal (R-LA, 2008–2016) and Nikki Haley (R-SC, 2011–2017) were the two Indian-origin governors, both Republicans; neither is in office. Vivek Ramaswamy (R) is a 2026 Ohio gubernatorial candidate — election not yet held as of 2026-09-18. [UNVERIFIED] — needs a primary state-page fetch.

**Trend since 2000: [GAP].** The House Clerk roster is a snapshot, not a time series. The directional fact that is primary-sourced elsewhere in this file: the two Indian-origin *governors* in the 2008–2017 window were both Republican, while all six current House members are Democrats — a party inversion between the executive and legislative tracks. Quantifying the trend needs historical Clerk rosters or the Congressional Biographical Directory. [GAP]

**Note on the partisan asymmetry:** the count of 6-0 Democratic is for *elected* federal officeholders. Appointed federal officials of Indian origin under the current Republican administration (e.g. the FBI directorship) are not in this count, and would change the picture if the question were "officials" rather than "officeholders". Flagged because the framing choice is load-bearing. [FRAMING-SENSITIVE]

---

## 2. Donations — surname/name-classifier studies on FEC data

**NOT a verified negative — a qualifying study exists.**

**Pal et al., "An Emerging Lobby: An Analysis of Campaign Contributions from Indian-Americans, 1998–2022"** (Joyojeet Pal, University of Michigan School of Information; project page `https://joyojeet.people.si.umich.edu/?p=1489`, PDF `https://joyojeet.people.si.umich.edu/wp-content/uploads/2025/09/Campaign_Contributions_from_Indian_Americans-1.pdf`, fetched and text-extracted 2026-09-18, 1,344 lines). Companion data site: `https://indianamericancontributions.vercel.app/`. [SOURCE]

- **Years covered:** 1998–2022 (six general + six midterm cycles).
- **Data:** OpenSecrets processed FEC individual-contribution files, cross-referenced against raw FEC filings. Itemised contributions only (the $200 FEC reporting floor applies).
- **Method:** hybrid name-based ethnicity classification. Stage 1 computes relative first-name and last-name popularity in India vs the US from a 2021 Facebook-derived name dump (32,308,972 US names + 6,161,590 India names = ~38.5m, 19% minority class); names above a conservative relative-popularity threshold are labelled Indian, below it not-Indian, ambiguous ones "indistinguishable". Stage 2 trains a neural classifier (ReLU + sigmoid) on that weak labelling, recall-weighted toward the Indian class. Stage 3 manually re-annotates edge cases such as "Roy".
- **Reported error rates (primary, from the fetched PDF):** naive accuracy **99.57%**, **F1 81.69%** on the validation set. Held-out test set of **12,000 manually annotated names**, drawn from the 10,000 highest-contributing individuals per cycle; a separate figure cites a test set of **60,830 unique donors**. The authors explicitly argue accuracy is the wrong metric here — a hypothetical 90%-accurate classifier on this base rate yields precision of only **23.38%** — which is why they threshold conservatively and hand-annotate the long tail's head.
- **Dollar split (2020 cycle):** Indian Americans gave **$46.6m to Democrats vs $16.3m to Republicans** (~74%/26%), across 656 Democratic and 484 Republican candidates. The paper also notes the diaspora's Democratic lean in PAC giving is *weaker* than in candidate giving, and that within the tech industry Indian American giving was more Democratic-skewed (72% figure) than the industry's overall 75:25 split.
- **Scale context from the same paper:** total Indian American giving of ~$35.8m against a comparison figure of $911.2m; the single largest Indian American donor in a cycle discussed was Vinod Khosla at $2.4m, against Timothy Mellon at $45.1m (~20×) and Miriam Adelson at ~$100m+. **The individual-donor channel is real but not dominant at the top of the money distribution.**

**Corroborating prior work (independent, different method):**
- Yoon & Tam Cho, "Pan-Ethnicity Revisited: Asian Indians, Asian-American Politics, and the Voting Rights Act", *Asian Pacific American Law Journal* 10 (2005), `http://hdl.handle.net/1807/78287`. FEC 1980–2000, name parsing. Asian Indian giving rose from ~$129,000 (1980) to over $8m (2000 cycle); a consistent Democratic lean across the whole period, weaker than Black or Latino Democratic lean. Also finds near-total ethnic self-funding of Indian American candidates (contributions from Asian donors to Indian American candidates were ~100% from Indian American donors), i.e. pan-ethnic Asian solidarity is absent in the money. [SOURCE, abstract/full text via Exa]
- Karthick Ramakrishnan / AAPI Data, "Growth of Asian American Political Contributions", 2016-03-14, `https://aapidata.com/blog/asian-am-political-contributions/`. FEC Detailed Files, two-stage surname matching (2000 Census surname list ≥100 occurrences, then an Asian-ethnic-origin list). Explicitly conservative: itemised contributions to principal/authorized candidate committees only, so it excludes PACs, super PACs, joint fundraising and leadership PACs. Reports Indian American subtotals. No error rate published. [SOURCE]

**Caveat that applies to all three:** name classification cannot distinguish an Indian American citizen donor from a naturalised-recently donor from a non-Indian person with an ambiguous name, and it systematically misses Indian Americans with anglicised or intermarried surnames. All three papers say so themselves. Directionally the Democratic lean is robust across three independent implementations and four decades; the *levels* carry classifier error.

Search terms used: "surname matching FEC individual contributions Indian American Asian American political donations study estimate party split" (Exa semantic, 8 results).

---

## 3. Lobbying / advocacy organisations

All 990 figures from the ProPublica Nonprofit Explorer API (`https://projects.propublica.org/nonprofits/api/v2/organizations/{EIN}.json`), which serves IRS Form 990 data; all FEC figures from the openFEC API (`https://api.open.fec.gov/v1/`). Fetched 2026-09-18. [SOURCE]

| Organisation | EIN / FEC ID | Legal form | Latest 990 revenue | FY |
|---|---|---|---|---|
| Hindu American Foundation Inc (Philadelphia PA) | EIN 68-0551525 | 501(c)(3) (IRS subsection 3), NTEE A70 | **$2,632,706** (expenses $2,123,906; assets $4,428,335) | FY2023 |
| Indiaspora (San Francisco CA) | EIN 46-4246368 | 501(c)(3), NTEE P99 | **$2,838,430** (expenses $3,367,539; assets $943,487) | FY2023 |
| Indian American Impact (Philadelphia PA) | EIN 38-4054905 | **501(c)(4)** (subsection 4), NTEE R01, Form 990-O | **$900,583** (expenses $991,914; assets $741,490) | FY2023 |
| Indian American Impact Project (Washington DC) | EIN 81-2175987 | 501(c)(3), NTEE P20 | **$1,017,561** (expenses $1,124,286; assets $259,172) | FY2023 |
| **Indian American Impact Fund** | **FEC C00674127** | PAC – Qualified, Unauthorized (treasurer John Roberson) | see cycle table below | — |
| **USINPAC** (US India PAC) | **FEC C00381699** | PAC – Qualified, Unauthorized (treasurer Sanjay K. Puri) | see cycle table below | — |

Notes on the 990 data:
- HAF FY2022 revenue $2,532,359; FY2021 $2,073,667 — a flat-to-slowly-growing organisation. An FY2024 filing exists in the Explorer index (`680551525_202406_990_2025042223370517.pdf`) but with no structured financials yet, so FY2023 is the latest machine-readable year. [GAP: FY2024 figures]
- Indiaspora's FY2023 appears twice in the API with different totals ($2,812,647 with no PDF; $2,838,430 with a PDF-backed filing) — likely an original/amended pair. I quote the PDF-backed record.
- The Indian American Impact structure is the standard three-entity advocacy stack: a **501(c)(3)** (Impact Project, education/research), a **501(c)(4)** (Indian American Impact, lobbying-capable), and a **federal PAC** (Impact Fund, candidate contributions). Combined FY2023 revenue across the two nonprofits: **$1.92m**.
- **USINPAC appears nowhere in the ProPublica Nonprofit Explorer** (searches for "USINPAC" returned only unrelated entities — Stockholm Environment Institute USinc, International Health Partners-USinc). It is a PAC, not a registered nonprofit. VERIFIED: no 990 exists to report.

**FEC receipts by cycle** (openFEC `/committee/{id}/totals/`):

| Cycle | USINPAC (C00381699) receipts | Impact Fund (C00674127) receipts | Impact Fund contributions to candidates |
|---|---|---|---|
| 2018 | $5,680 | $41,494 | $41,486 |
| 2020 | $3,901 | $77,179 | $77,172 |
| 2022 | $5,198 | $345,734 | $340,733 |
| 2024 | $18,135 | $218,584 | $213,549 |
| 2026 (thru 2025-06-30) | $0 | $5,750 | $5,750 |

USINPAC's FEC registration dates to 2002-09-09 with a last filing date of 2026-07-14, so it is *active but nearly dormant financially*. Its peak cycle in this window is $18k. The Impact Fund is the larger of the two by an order of magnitude and peaked in 2022 at $346k — still small relative to, e.g., a single competitive House race.

**Two defunct predecessor PACs, verified:** "Indian-American Political Affairs Committee (fka Indo-US PAC)" C00218842 (1987–1997) and "India-US Political Action Committee INDIAPAC" C00380840 (2002–2015, receipts under $40/cycle after 2006, terminated). Also "American Association of Physicians of Indian Origin in Political Action Committee" C00199935 (1985–2002). [SOURCE: openFEC committee search q=INDIA, q="US INDIA"]

**Stated positions: [GAP].** I did not fetch the organisations' own position pages (hinduamerican.org, indiaspora.org, indianamericanimpact.org) within budget, so I am reporting no positions in their own words rather than paraphrasing from memory. The one position-adjacent primary datum I *did* verify is at §6: Carnegie found no significant difference between BJP-identifying and Congress-identifying respondents on support for caste-discrimination measures, which it flags as notable because "pro-Hindu groups typically perceived as close to the BJP and its ecosystem have been the most vocally opposed to caste-based regulation in the United States". That is Carnegie's characterisation of those groups' position, not a fetched statement from HAF.

---

## 4. Congressional India Caucus

**Name: "Congressional Caucus on India and Indian Americans."** **VERIFIED against the primary** — the Committee on House Administration's official 119th Congress Congressional Member Organization (CMO) registration list, `https://cha.house.gov/_cache/files/f/2/f2c6808f-20ad-436e-a362-4626a51dda9f/41F5903DA337B46F2ED965DE5B77D3E622747170D48B22E23EA05C73F7C8ADE8.119th-congress-cmo-list-26-.pdf` (1.36 MB PDF, fetched and text-extracted 2026-09-18, entry at line 1193). [SOURCE]

The official CMO registration lists **Rep. Ro Khanna (D-CA-17)** as Chair/Co-Chair, staff contact Preeti Turpuseema. **The CMO filing names only Khanna** — it does not list McCormick, Barr or Veasey.

Secondary reporting (not primary, tagged accordingly) states the 119th Congress leadership is co-chairs **Ro Khanna (D) and Rich McCormick (R-GA)**, vice co-chairs **Andy Barr (R-KY) and Marc Veasey (D-TX)**, with Brad Sherman (D-CA) as chair emeritus. This is corroborated by the **Consulate General of India, San Francisco** press release of 2025-06-04 (`https://www.cgisf.gov.in/section/press-releases/visit-of-all-party-parliamentary-delegation-to-usa-june-04-2025/`), which names "the co-chairs Rep. Ro Khanna and Rep. Rich McCormick and the two vice co-chairs Rep. Andy Barr and Rep. Marc Veasey" in the 119th Congress — a foreign-government primary record of a meeting, which is a stronger source than the news listicles but is still a third party describing US caucus leadership. [SOURCE: cgisf.gov.in, 2025-06-04]

**Membership count: [GAP] for the 119th Congress.** The only sourced figure is **145 members in the 118th Congress** (with 35 members joining under Khanna and then-co-chair Michael Waltz), which traces to a **Khanna office press release of 2025-01-29** as relayed by ANI/ThePrint (`https://theprint.in/world/ro-khanna-rich-mccormick-to-chair-indias-caucus-in-us-congress/2469377/`) and New India Abroad. I did not reach the original house.gov release, so the 145 figure is [UNVERIFIED] at the primary level and refers to the *previous* Congress. The CHA CMO list registers the caucus but does not publish membership counts.

**Senate India Caucus: exists, details [GAP].** Sen. Mark Warner (D-VA) is publicly associated with it (`https://www.warner.senate.gov/` surfaces a "Senate India Caucus" page), and the 2025-06-04 Indian consulate release refers to "the Senate India Caucus" as a body whose members received an Indian parliamentary delegation. I did not verify its co-chairs or membership count from a senate.gov primary — senate.gov returned HTTP 403 on my roster fetch. [GAP]

---

## 5. FARA — Indian foreign principals

**BLOCKED. Exact failure recorded.**

The FARA eFile JSON API's registrant endpoint works: `https://efile.fara.gov/api/v1/Registrants/json/Active` returned **HTTP 200, 102,719 bytes** (fetched 2026-09-18), giving active registrant names, addresses and registration numbers/dates. **But that endpoint carries no foreign-principal linkage**, which is what the question needs.

Every foreign-principal endpoint I probed returned **HTTP 404** (Apache Tomcat "HTTP Status 404 – Not Found", 431-byte body), ten variants:

```
/api/v1/ForeignPrincipals/json/Active        -> 404
/api/v1/ForeignPrincipals/json/active        -> 404
/api/v1/ForeignPrincipals/json/All           -> 404
/api/v1/ForeignPrincipals/json               -> 404
/api/v1/ForeignPrincipals/xml/Active         -> 404
/api/v1/ForeignPrincipals/json/Country/INDIA -> 404
/api/v1/ActiveForeignPrincipals/json/Active  -> 404
/api/v1/ActiveForeignPrincipals/json         -> 404
/api/v1/PrincipalsActive/json/Active         -> 404
/api/v1/ActivePrincipals/json/Active         -> 404
/api/v1/Registrants/json/Active/ForeignPrincipals -> 404
/api/v1/Registrants/json/ActiveForeignPrincipals  -> 404
/ords/fara/fara_search/foreign_principals?country=INDIA -> 404
/ords/fara/api/foreignprincipals             -> 404
```

Bulk-download routes also dead: `https://efile.fara.gov/bulk/csv/FARA_All_ForeignPrincipals.csv` → **404 (355 bytes)**; `https://efile.fara.gov/bulk/zip/FARA_All_ForeignPrincipals.zip` → **404**; `https://efile.fara.gov/api/v1/ForeignPrincipals/csv/Active` → **404**.

The public quick-search at `https://efile.fara.gov/` is an Oracle APEX application requiring a session token and JS execution, which a plain curl cannot drive.

**[GAP] — no FARA registrant/foreign-principal pairs verified.** Recommended next step for a re-dispatch: drive `https://efile.fara.gov/ords/f?p=1381:1` with `agent-browser` (headless CDP) and export the country-filtered result set, or fall back to the DOJ NSD semi-annual reports to Congress. I fetched `https://www.justice.gov/nsd-fara` (HTTP 200, 70 KB) but found no direct link to an active-foreign-principals dataset in its markup. **I am reporting zero FARA findings rather than guessing at registrant names.**

---

## 6. Diaspora positions on Indian domestic politics

**Instrument (identical for both papers, verified from the fetched pages):** Indian American Attitudes Survey (IAAS) 2024, Carnegie Endowment for International Peace with **YouGov**. **N = 1,206** Indian American adult residents (18+, self-identifying as Indian American or of Asian Indian origin, **including both citizens and noncitizens**). **Mode: online, YouGov proprietary panel, sample-matched**, all analyses weighted. **Field period 2024-09-18 to 2024-10-15.** Maximum margin of error **±3 percent**. Cross-sectional, not a panel — Carnegie explicitly warns against reading 2020→2024 differences as within-person change. [SOURCE: both Carnegie pages, fetched 2026-09-18]

**Paper A — "Foreign Policy Attitudes of Indian Americans: 2024 Survey Results"**, `https://carnegieendowment.org/research/2025/03/foreign-policy-attitudes-of-indian-americans-2024-survey-results` (HTTP 200, 375 KB). Authors Badrinathan, Kapur, Vaishnav.

- **Modi job approval: 47% approve** (36% strongly approve, 11% approve), **34% disapprove** (23% strongly, 11% somewhat), **19% no opinion**. n=1,206, online panel. Carnegie's own framing: "In the aggregate, Modi's approval ratings among the diaspora have not budged much in four years."
- **2020 comparison: 50% approved** (35% strongly, 15% somewhat), **31% disapproved** (22% strongly). So approval is down ~3 points and disapproval up ~3 points, both inside or near the ±3 MoE — **not a demonstrated shift**.
- **Indian party identification (2024): BJP 28%, Indian National Congress 20%, third party 1%, "don't know" 51%.** Carnegie: "Fifty-one percent, slightly more than half, reply 'don't know' to this question, suggesting that many Indian Americans maintain a distance from Indian political attachments."
- **2020 comparison: BJP 32%, Congress 12%, third party 11%.** The BJP–Congress gap narrowed from 20 points to 8.
- **On Modi's rhetoric and minorities:** 71% of Christians, 75% of Muslims and 74% of other-religion respondents take the anti-minority-threat view; on the other side 34% of Hindus and 25% of Muslims disagree that Modi's language exemplifies an anti-minority threat. (The Hindu share taking the threat view is in the fetched text's surrounding passage, which I did not capture cleanly — [GAP] on the exact Hindu figure.)
- **On the US posture toward Indian democracy:** plurality **31%** say the Biden administration struck the right balance between promoting democratic values and protecting US strategic interests; **28%** say it prioritised strategic interests over concerns about India's democracy; only **17%** say it prioritised democracy concerns over strategic interests; **24%** no clear view.
- **On the Biden record generally:** roughly half approve of its handling of US–India relations; roughly four in ten call its support for India appropriately calibrated.

**Paper B — "Results From the 2024 Indian American Attitudes Survey" (social survey)**, `https://carnegieendowment.org/research/2025/07/indian-americans-social-survey-data` (HTTP 200, 424 KB). Same instrument, N=1,206, ±3.

- **Caste-discrimination measures:** broad support across party lines — **Democrats 81%, independents 80%, Republicans 70%**. Support was **79% among Upper Caste respondents** and **73% among those with no caste affiliation**. Critically: **no significant difference between BJP supporters and Congress supporters** on this item, which Carnegie flags as notable "because pro-Hindu groups typically perceived as close to the BJP and its ecosystem have been the most vocally opposed to caste-based regulation in the United States." **Organisational position and measured mass opinion diverge here.**
- **Identity trend:** the share of US-born respondents calling the Indian component of their identity important **grew substantially since 2020**; the share identifying as "Indian American" **fell** while "Asian Indian" **rose**; eight in ten ate Indian food in the prior month. Carnegie's summary: "Indian Americans were displaying more, not less, affinity toward their Indian identity."

**Reading:** the diaspora is neither a Modi bloc nor a Modi-opposition bloc. A 47/34/19 approval split with 51% declining to name an Indian party is a population **mostly disengaged** from Indian party politics, with a plurality-positive but soft tilt toward Modi and the BJP that has, if anything, softened since 2020. The organised Hindu-advocacy sector's positions on at least one item (caste regulation) do not track the measured attitudes of BJP-identifying respondents. [FRAMING-SENSITIVE: whether the 28% BJP identification is "high" depends on the comparison chosen — it is above Congress's 20% but below the 51% who abstain.]

---

## Summary of gaps for a re-dispatch

| # | Gap | Suggested next query |
|---|---|---|
| 1 | Senate roster unverified (senate.gov HTTP 403) | curl with a contact-UA header, or congress.gov API with a real key (DEMO/keyless returned 403) |
| 1 | Current governors / statewide officials (NGA page JS-rendered) | `agent-browser` on nga.org/governors, or per-state official pages |
| 1 | Officeholder trend since 2000 | Congressional Biographical Directory, or archived House Clerk rosters per Congress |
| 3 | Organisations' stated positions in their own words | fetch hinduamerican.org, indiaspora.org, indianamericanimpact.org policy pages |
| 3 | FY2024 990s for HAF and Impact Project (PDFs exist, no structured data) | pdftotext the ProPublica filing PDFs already identified by path |
| 4 | India Caucus membership count for the 119th Congress | Khanna's house.gov press releases; CHA CMO list has no counts |
| 4 | Senate India Caucus co-chairs and membership | warner.senate.gov caucus page via agent-browser |
| 5 | **All of FARA** — no registrant/principal pairs obtained | `agent-browser` against the APEX app at efile.fara.gov/ords/f?p=1381:1; or DOJ NSD semi-annual reports |
| 6 | Exact Hindu-respondent figure on the Modi-rhetoric item | re-grep the saved carn_fp text around "anti-minority threat" |

Working files (scratchpad, not committed): `pal.pdf`/`pal.txt`, `carn_fp.html.txt`, `carn_soc.html.txt`, `cmo.pdf`/`cmo.txt`, `members.xml`, the `pp_*.json`/`org_*.json` ProPublica payloads and `tot_*.json`/`c_*.json` FEC payloads, under `/private/tmp/claude-501/-Users-alien-Projects-immigration-research/a3a856d0-ddb5-428f-ae3c-eead47e76df3/scratchpad/`.
