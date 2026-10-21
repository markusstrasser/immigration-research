claude-opus-5-5

# Speech and labelling costs of the immigration debate (lane speech_cost_2026_10_21)

**Verdict:** On US campuses the documented sanctions over immigration speech are few and come from both sides for
scholars, but from one side for invited speakers. In FIRE's full tables, 50 of 1,997 scholar incidents (2000–2026) carry
FIRE's Immigration tag: 26 attacked from the left (six terminations, all 2007–2020, mostly over restrictionist remarks)
and 24 from the right (16 of them 2025–26 government actions: Naval Academy book removals and ICE detentions). For
speakers, 131 of 2,107 deplatforming attempts concern immigration, 93% of them from the left against a 47% base rate,
and half succeeded. Self-censorship is asymmetric in general (55% of conservative vs 17% of liberal faculty hide their
politics to keep their jobs), but the one item that names immigration, students calling it hard to discuss (38% in
2026), runs higher among liberals. Two US list experiments found concealed restrictionism of 19 points (2005, all adults) to
28 points (2005, Christian adults) and 12 points (2010), shrinking as overt restrictionism grew, while a 264-study meta-analysis finds prejudice items honest
within about 5 points. The research field is lopsided: about one team in eight in the only stance-measured many-analysts
study had a restrictionist member, and stance moved estimates (pro minus anti 0.085, SE 0.031). Prejudice vocabulary in
US news rose 5–6× in 2010–19 across topics; the immigration-specific co-occurrence share is unmeasured (GDELT
rate-limited, [DEGRADED]). No channel
identifies an economic cost; nothing here is added to the group's fiscal account. [FRAMING-SENSITIVE: "cost" of
speech is a welfare judgment; the counts are not.]

## Scope

Operator ask 2026-10-21: the immigration issue is contentious, high-end people lost jobs or freedom
through cancellation, and "racism" is used as a label for restrictionists. This lane measures what
the debate does to speech and knowledge, in five channels:

1. Sanctions (FIRE Scholars Under Fire, Campus Deplatforming, documented terminations)
2. Self-censorship (faculty/student/worker surveys)
3. Preference falsification (list experiments vs direct questions; polling misses)
4. Labelling (prejudice-term co-occurrence with immigration restriction in US news)
5. Knowledge production asymmetry (bounded; only if a primary source exists)

Attribution rule (from parent): each channel's size first; then the share plausibly linked to
immigration with its identification; never add a response-mediated effect to the group's cost.
No dollar figure is invented where no link to economic cost is identified.

## Pre-registration (written 2026-10-21 15:10:01 JST, before any magnitude was fetched)

Prior coverage: `rg` over research/, decisions/, infra/ for Scholars Under Fire, list experiment,
Janus, Rozado, self-censor: no hits outside this file (brainstorm ideas 21–25 tagged NOVEL; 24 HAD-PARTS
via the "nobody did half" literature check 7d546ab4).

**Q1 Sanctions.** Source: FIRE Scholars Under Fire (SUF) incident records, the full exported table if one
exists, else every record the public listing exposes. Topic rule, applied by `code_incidents.py` to the
incident's title + description + FIRE's own topic tags, case-insensitive:
- IMM (immigration): `immigra|migrant|emigra|refugee|asylum|border|deport|\bICE\b|DACA|undocumented|illegal alien|xenophob|nativis|great replacement|sanctuary|citizenship`;
- GRP (group differences): `\bIQ\b|intelligence|hereditar|bell curve|eugenic|race science|racial differences|genetic.*(race|group)`;
- RACE (race, broad): `\brac(e|ial|is[mt])|white supremac|black lives|BLM|anti-?black|DEI|diversity`;
- union flags reported separately; IMM is the headline. An incident is IMM only on a regex hit; no hand reclassification.
Outcomes in FIRE's own coding (terminated, suspended, demoted, investigated, censored, no sanction / cleared) and
FIRE's own "attacked from the left / right of the scholar" field. Denominator: all incidents in the same years.
If the table cannot be obtained, report FIRE's published aggregates with quoted cells and mark IMM [GAP].
Non-academic sanctions: no comparable systematic dataset is expected; listing named cases is not a rate and
will not be presented as one.

**Q2 Self-censorship.** Report survey items verbatim with the share answering yes, by political identity where
published: FIRE College Free Speech Rankings topic-difficulty item (immigration is expected to be one of the listed
topics), FIRE faculty survey, Heterodox Academy Campus Expression Survey, Clark et al. psychology-professor taboo survey,
Norris's World of Political Science survey, Cato/YouGov national polls. An item counts as immigration-specific only if
the word "immigration" (or an immigration policy) is in the item; general self-censorship items are reported as the
channel's size, not as its immigration share.

**Q3 Preference falsification.** For each list experiment (Janus 2010; Creighton, Jamal & Malancu 2015; Knoll 2013;
later ones found by search) report: item wording, direct-question share, list-estimate share, difference with SE or CI,
subgroup where the gap concentrates. For polling misses, report only studies that test a hidden-attitude mechanism
directly (e.g. Coppock 2017's list experiment on Trump support, AAPOR 2017 task force) rather than inferring it from the
miss.

**Q4 Labelling.** Level and trend of prejudice terms (racist, racism, xenophobic, xenophobia, nativist, white supremacist)
in US news. Route 1: Rozado et al.'s published series (term frequency per word, by outlet, by year), read from the
paper/supplement. Route 2: GDELT DOC 2.0 timeline (volume share of articles, US sources, from 2017) for
`immigration AND (term)` vs `immigration` alone; ratio = share of immigration articles carrying a prejudice term.
Co-occurrence measures label exposure, not whether the label is applied to restrictionists, nor whether it is apt.

**Q5 Knowledge production.** Report only a primary source measuring an asymmetry in what is studied or published
(survey of researchers' willingness to publish a finding by direction, topic counts by sign of result). Otherwise [GAP].

For every channel: what it measures, size, what it holds fixed, whether a link to economic cost is identified.
Expected a priori: no channel identifies a dollar cost; none will be added to the group's fiscal cost (attribution
rule: response-mediated effects stay beside).

## Findings

### Q1 Sanctions (appended 2026-10-21 15:13:56 JST)

Data: the full FIRE tables, pulled 2026-10-21 from `fire.org/api/knack-data` (Scholars Under Fire 1,997 records,
2000–2026; Campus Deplatforming 2,107 records), sha-pinned in `code_incidents.py` [DATA: `_cache/`, ignored].
FIRE codes each record's topics, its outcome(s) and its political direction, the last "relative to the
controversial expression", judged from who initiated the attempt (methodology PDF, Aug 2026, quoted in the
script docstring). Derived tables: `derived/scholars_topic_direction_outcome.csv`,
`derived/deplatforming_topic_direction_outcome.csv`, `*_topic_by_year.csv`, `*_immigration_incidents.csv`.
[CALCULATION: code_incidents.py]

**Scholars (faculty, postdocs, PhD students).** FIRE's Immigration tag covers 50 of 1,997 incidents (2.5%);
my pre-registered regex covers 90 (4.5%), but an audit of its 40 regex-only hits shows low precision ("citizenship"
in book titles, ICE detentions over Gaza speech, "border" in unrelated text), so FIRE's tag is the better
count and the regex is kept only as an upper bound. 28 of the 50 also carry FIRE's Race tag.

| Immigration-tagged scholars | n | any penalty | terminated | suspended | investigated | censored | outside sanction | no sanction |
|---|---|---|---|---|---|---|---|---|
| all directions | 50 | 35 | 7 | 3 | 20 | 15 | 13 | 14 |
| attacked from the left | 26 | 17 | 6 | 3 | 17 | 2 | 1 | 9 |
| attacked from the right | 24 | 18 | 1 | 0 | 3 | 13 | 12 | 5 |
| (all topics, from the left) | 626 | 451 | 125 | 116 | 359 | 105 | 20 | 173 |
| (all topics, from the right) | 1,262 | 945 | 161 | 97 | 353 | 540 | 383 | 313 |

"Any penalty" is this lane's grouping (termination, suspension, demotion, censorship, investigation, scholarship
suppression, training, retraction, outside sanction); outcomes are not exclusive. The two sides differ in kind.
All 26 left-direction cases predate 2025 and mostly concern a scholar's restrictionist or group-difference remarks
(e.g. Leitner 2011, approval of Arizona's SB 1070, investigation and termination; Engler 2010, terminated; Wax 2017–2022;
Buch 2016 on undocumented students); six ended in termination. 16 of the 24 right-direction cases fall in 2025–26:
10 are the Naval Academy library's removal of books on race and immigration (one action coded per author), two are
ICE detentions of foreign scholars whose speech was about Gaza (Öztürk, Khan Suri), and the rest are watch-list
postings and classroom complaints. Across 2000–2024, 34 incidents carry the tag, 1.7–4.3% of incidents in each
five-year block (4/230, 15/347, 15/696); the immigration-tagged count does not trend up faster than the whole
database.

**Speakers (Campus Deplatforming).** Immigration is a larger share here: 131 of 2,107 attempts (6.2%), and 122 of
the 131 (93%) came from the left, against 47% (981/2,107) for all topics. 65 of the 131 succeeded (revoked,
cancelled, removed, withdrew, postponed or substantially disrupted). The targets are mostly restriction advocates
or officials: Yiannopoulos 16, Kirk 4, Coulter 3, Gilchrist (Minuteman Project) 3, Krikorian (CIS) 2, Shapiro 3,
Jeh Johnson and Napolitano (Obama DHS secretaries) 5 between them. The peak was 2015–19 (58 of 488 attempts, 11.9%).

**Non-academics.** No systematic dataset of employment terminations over immigration speech was found;
named cases are not a rate. [GAP] Criminal speech prosecutions over immigration remarks exist in Europe (UK
post-Southport sentencing 2024, Dutch Wilders conviction 2016) but no dataset counting them by topic was located in
this lane's budget, and none for the US, where such speech is protected. The operator's "lose their freedom" is
documented in SUF only on the other side: the two scholars detained in 2025 were detained by immigration enforcement.

What it measures: publicly documented attempts at US colleges, as FIRE finds and codes them. Not exhaustive by FIRE's
own statement, and its discovery depends on press coverage, so a quietly settled case is missing. Holds fixed:
nothing; these are counts. Link to economic cost: none identified. A termination is a private loss to one scholar;
the claimed social cost runs through deterrence of others, which Q2 measures. Dollar figure: none.

[GAP] next: hand-code the 26 left-direction cases by the expression's content (restrictionist claim, slur, group
difference), double-coded; FIRE's direction says who attacked, not what the scholar said.

### Q2 Self-censorship (appended 2026-10-21, after the 15:13 block; time stamped in the log)

Immigration-specific items (the item names immigration):

| Survey | Population, n | Item | Immigration | By identity | Source |
|---|---|---|---|---|---|
| FIRE/College Pulse CFSR 2027 rankings | 62,997 undergraduates, 262 colleges, Jan–Jun 2026 | "Which of the following issues, if any, would you say are difficult to have an open and honest conversation about on your campus?" | 38% | not in the topline | [SOURCE: 2027 CFSR Report PDF p. 18, nationwide figure, cell "Immigration 38%" (Israeli-Palestinian 50%, Trump 46%, Kirk 44%, abortion 43%, transgender rights 38%); same cell in the appendix topline p. 24] |
| CFSR 2026 rankings | 68,510, Jan–Jun 2025 | same | 33% | — | [SOURCE: 2026 CFSR Report PDF p. 7, Figure 3, cell "Immigration 33%"] |
| CFSR 2020 rankings | 19,969 undergraduates (p. 9), 55 colleges | same, "[Select up to 8 options]" | 36% | liberal 48%, moderate 32%, conservative 31% | [SOURCE: 2020 CFSR Report PDF (legalinsurrection.com mirror) p. 56 topline "36% Immigration"; p. 52: "Fewer Liberal students identified immigration (48%) and race (42%) as difficult topics, yet they still found these topics difficult to discuss more often than Moderates (32% and 37% respectively) and Conservatives (31% and 30% respectively)."] |

General items (channel size, not immigration's share):
- FIRE 2024 faculty survey, 6,269 faculty at 55 colleges: 35% "recently toned down their writing for fear of
  controversy"; 27% often feel unable to speak freely; "Only 17% of liberal faculty say they at least occasionally hide
  their political views in order to keep their jobs, compared to a staggering 55% of conservative faculty who say the
  same" [SOURCE: Faculty-Report-2024-Final.pdf p. 4 key findings 1 and 3; p. 6 for 17%/55%]. The faculty survey did not
  offer immigration: its topic-difficulty item lists 19 topics (toplines p. 6: Israeli-Palestinian 69.9%, racial
  inequality 50.8%, transgender rights 48.5%, affirmative action 47.3%, presidential election 41.2%, crime 17.6%), and
  "immigra" occurs nowhere in the report or the toplines. Self-censor "likely" or more in research topics investigated:
  20.1% (cells 8.4 + 6.1 + 5.6, toplines p. 3), in academic publications 26.8% (10.7 + 7.7 + 8.4, toplines p. 4)
  [SOURCE: 2024-Faculty-Survey-Toplines.pdf].
- Kaufmann (CSPI 2021): "over 9 in 10 Trump-supporting academics and 8 in 10 Brexit-supporting academics say they would
  not feel comfortable expressing their views to a colleague"; "More than half of North American and British
  conservative academics admit self-censoring in research and teaching"; "Over 4 in 10 US and Canadian academics would
  not hire a Trump supporter" [SOURCE: cspicenter.com/p/academic-freedom-in-crisis-punishment, summary bullets, HTML
  page text checked 2026-10-21; the report's PDF was not opened].

Reading. The one immigration-named series does not show an asymmetry against restrictionists: in 2020 liberal students
named immigration as hard to discuss more often (48%) than conservatives (31%), so "hard to discuss" there means
contentious for both sides, and it does not say who withholds which view. The asymmetric evidence is general, not
immigration-specific: conservative faculty hide their politics at about three times the rate of liberal faculty (55% vs
17%), and Trump-supporting social scientists almost all withhold their views. Immigration restriction was Trump's
signature issue, so a share of that withholding plausibly concerns it, but no survey located isolates that share.
[GAP] Heterodox Academy Campus Expression Survey topic items, Norris's World of Political Science survey, Cato/YouGov
2020 national items: not read in this budget; none is known to name immigration specifically.
What it holds fixed: nothing; self-reports, and "difficult to discuss" is not self-censorship. Link to economic cost:
none identified.

### Q3 Preference falsification

| Study | Sample, year | Item | Direct | List | Gap |
|---|---|---|---|---|---|
| Janus 2010 (SSQ 91(4), TESS data) | US phone, n 1,320, Oct 2005–Feb 2006 | support "cutting off immigration to the United States" | 42% | 61% | +19 pt; liberals 26% vs 71% (+45); college graduates 29% vs 71% (+42); postgraduates 30% vs 41% and conservatives not significant [SOURCE: published PDF, journal p. 939 Table 2, row "Population 1.77 2.16 61 ... 42 19"; p. 938 text "unobtrusive estimate of support: 61 percent"; liberals p. 941] |
| Creighton, Jamal & Malancu 2015 (IMR), Christian adults | 2005 (Janus data) | oppose "cutting off all immigration" | 60.3% oppose | 31.9% oppose | 28.4 pt concealed restrictionism [SOURCE: published PDF, journal p. 741 Table 2, "No covariates 0.603* 0.319* 0.284*"] |
| same | 2010 TESS | same | 42.5% oppose | 30.5% oppose | 12.0 pt (same row: "0.425* 0.305* 0.120*"); the rise in overt restrictionism after 2008 is "attributable to greater expression of opposition rather than any underlying change in attitudes" (abstract) |
| Creighton & Jamal 2015 (Soc Sci Res 53) | US, n 3,290 | oppose citizenship for legal Christian / Muslim immigrants | 11% / 30% | 28% / 33% | 19 pt hidden for Christian immigrants, none for Muslim [SOURCE: published PDF, journal p. 98: "19% (±8%) of the U.S. Christian population mask their opposition to Christian immigrants"] |

Corrections from the PDF check (2026-10-21 15:52 JST): the TESS study page summarises Janus as 40% direct vs 62% list
(+22); the published table gives 42% vs 61% (+19), and the table is used. CJM's text says the 2010 bias is "only a third
of the 32 percent observed in the pre-crisis period", but its own Table 2 gives 28.4 points for 2005; the table is used.
| Bazo Vienrich & Creighton 2017 (JEMS) | US | opposition to immigration among Hispanics | lower | "significantly and substantively greater" | concealment concentrated among Hispanics [SOURCE: doi 10.1080/1369183x.2017.1334540 abstract] |

Disconfirmation. Blair, Coppock & Moor (APSR 2020), meta-analysing 264 list experiments, find "nearly no evidence of
sensitivity bias in measures of prejudice": racial prejudice, "if anything, subjects overreport racist attitudes by
approximately 4 points (95% CI –3 to +9)"; religious prejudice −1 point; "we can rule out average biases as large as 10
or 15 percentage points in most cases" [SOURCE: author PDF, p. 14 for the racial-prejudice estimate, p. 15 for the
10–15 point bound, p. 10 for the 264 experiments; Coppock 2017 figures from his author PDF p. 1 and p. 4 ("The
bootstrapped standard error of this difference is 3.4 points")]. Their prejudice domains are race, religion and sexual orientation, not
immigration policy, so the immigration-specific gaps above (12–28 points) sit outside their pooled range and are not
refuted by it; but the list experiment's variance is large (Janus n 1,320 split three ways) and its anchoring on a
three-item baseline is fragile. Coppock 2017 (Reuters/Ipsos, n 5,290, Sept 2016): direct Trump support 32.5%, list
29.6%, difference 2.9 pt (SE 3.4); "no evidence in support of the 'Shy Trump Supporter' hypothesis" in an online poll.
Polling misses tied to immigration attitudes: the hidden-attitude mechanism has been tested directly only for 2016
vote choice and failed there; the 2016 miss is attributed mainly to nonresponse by education and late deciders
[INFERENCE from Coppock's discussion; AAPOR 2017 not re-read here, GAP].

Size. Concealed restrictionism of 12–28 points in two US list experiments (2005, 2010) on the most extreme item,
with the gap shrinking as overt expression became more acceptable after 2008; no estimate after 2010 was found [GAP:
search 2016–2026 list experiments on immigration policy items, e.g. Brexit and German AfD-era studies]. What it holds
fixed: same respondents or randomized arms, same wording; it measures concealment from an interviewer, not public
self-censorship. Link to economic cost: none identified. The plausible cost route is political: if stated preferences
understate restrictionism, representatives read a distorted signal. No study prices that.

### Q4 Labelling (appended 2026-10-21 15:27:48 JST)

Route 1, Rozado, Al-Gharbi & Halberstadt (Social Science Computer Review 41(1), 2023; online 2021), 27 million
articles in 47 US outlets, 1970–2019, frequency = occurrences / all words per outlet-year. "Words such as racist or
sexist increasing in usage between 2010 and 2019 by 638% and 403% in The New York Times or 514% and 141%, respectively,
in The Washington Post"; "the racism theme displays the highest absolute prevalence"; the rise "precedes the political
emergence of Donald Trump ... but appears to accelerate after 2015" (paired slope test t(19) = −2.59, p ≈ .02);
left-leaning and centrist outlets are "highly synchronized in the yearly usage of words that denote racism"
[SOURCE: doi 10.1177/08944393211031452, author-accepted PDF (hoplofobia.info mirror) p. 9 for 638%/403%/514%/141%,
p. 10 for the slope test (sign lost in extraction: "t(19) ¼ 2.59, p value  .02")]. Their series is term frequency, not co-occurrence with
immigration; their Zenodo record 5094015 holds the articles containing target words (624 MB rar), from which an
immigration co-occurrence share could be computed; not done here (no rar extractor installed, disk at 97%) [GAP].

Route 2, GDELT DOC 2.0 (`gdelt_labels.py`, pre-registered above): [DEGRADED] at 15:37 JST. The immigration-only series
landed (5,139,894 US English articles matching `immigration`, 2017-01 to 2026-09; `_cache/gdelt_immigration.csv`), but
the labelled query returned HTTP 429 on all six retries over ~10 minutes; other agents in this session query GDELT from
the same address. No co-occurrence share is reported. A second attempt at the parent's request (15:43–16:01 JST, 60 s between
requests, six tries with 60–360 s backoff) failed the same way: HTTP 429 on all six tries for the labelled query. Q4
route 2 stays [DEGRADED]. Rerun `gdelt_labels.py` from another address or later; it resumes from the cache and writes
`derived/gdelt_label_share_{monthly,yearly}.csv` with the `taxes` control.

## Reproduce

From the repository root.

1. Network fetch, manual (FIRE serves a JavaScript challenge to plain HTTP clients); outputs go to the ignored `_cache/`
   and are sha-pinned in `code_incidents.py`, so a re-pull that changed the records stops `[BLOCKED]`:
   ```sh
   agent-browser open "https://www.fire.org/research-learn/scholars-under-fire"
   agent-browser eval "fetch('/api/knack-data?type=scholars&page=0&range=2500&orderby=year&orderdir=desc').then(r=>r.text())" \
     > infra/immigration-fiscal/speech_cost_2026_10_21/_cache/fire_scholars_under_fire_2026-10-21.json
   agent-browser eval "fetch('/api/knack-data?type=deplatforming&page=0&range=2500&orderby=year&orderdir=desc').then(r=>r.text())" \
     > infra/immigration-fiscal/speech_cost_2026_10_21/_cache/fire_campus_deplatforming_2026-10-21.json
   ```
2. Offline, deterministic, writes the six `derived/` CSVs:
   ```sh
   OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/speech_cost_2026_10_21/code_incidents.py
   ```
3. Network fetch (GDELT DOC API; not deterministic, GDELT revises its index; currently rate-limited):
   ```sh
   uv run --no-project python3 infra/immigration-fiscal/speech_cost_2026_10_21/gdelt_labels.py
   ```
Rerun check (step 2 only; the GDELT fetcher is exempt):
```sh
uv run --no-project python3 scripts/rerun_lane.py infra/immigration-fiscal/speech_cost_2026_10_21 \
  "uv run --no-project python3 {lane}/code_incidents.py" \
  --allow-unrun infra/immigration-fiscal/speech_cost_2026_10_21/gdelt_labels.py
```

What co-occurrence shows and does not show: it measures how often coverage of immigration carries prejudice vocabulary.
It does not show the label is aimed at restrictionists (the article may quote a restrictionist calling an opponent
racist, or report a hate crime), whether the label is apt, or that it changes behaviour. The operator's claim, that
"racism" is used as a label for restrictionists, needs article-level coding of the label's target; no published
dataset with that coding was found [GAP]. The nearest primary evidence that the label deters: Q2's conservative
faculty hiding their views (55% vs 17%) and Q3's concealment gaps, neither of which names the label as the cause.

### Q5 Knowledge production

One primary source measures an asymmetry directly. Borjas & Breznau (NBER w33274, Dec 2024) use the Breznau–Rinke–Wuttke
many-analysts experiment (PNAS 2022): 158 researchers in 71 teams, same ISSP data, same question (does immigration
reduce support for social programs?), immigration stance asked before analysis. Composition: "The researchers skew
heavily towards a pro-immigration stance: Nearly half strongly support the proposal that immigration laws should be
relaxed ... no researcher responded with a '0'"; 31 teams (43.7%) pro-immigration, 9 (12.7%) with at least one
anti-immigration member, 31 moderate. Output: pro- minus anti-immigration teams' average marginal effect 0.085 (SE
0.031, p 0.008), i.e. moving a team from the 16th to the 63rd percentile of the estimate distribution; both tails
received referee scores at least half an SD below moderate teams; five design choices account for "68 percent (or
0.058 ÷ 0.085) of this difference" [SOURCE: w33274.pdf, PDF p. 8 ("no researcher responded with a '0'"), p. 9 ("31 of
the 71 teams (or 43.7 percent) as pro-immigration"), p. 10 ("9 teams (or 12.7 percent) as anti-immigration"), p. 13
("pro- and anti-immigration teams is 0.085 (0.031) points and statistically significant (with a p value of 0.008)"),
Table 2 p. 33 ("D: Pro - Anti ... 0.085** ... (0.031)"), p. 22 (68 percent)]. What it holds fixed: the data and the question (assigned, not chosen). What it
shows: stance moves estimates in both directions, and the field's composition is lopsided (restrictionist researchers
are about one team in eight), so the pooled literature leans by composition even if each side is equally biased.
What it does not show: that restrictionist findings are suppressed at submission or review; the experiment has no
publication stage. [GAP] No survey of economists' willingness to publish a cost-of-immigration finding was found; the
FIRE 2024 faculty toplines give 20.1% at least "likely" to self-censor in research topics investigated and 26.8% in
academic publications, all topics. The repo's own literature check (7d546ab4, "nobody did half") is the HAD-PARTS link:
no complete fiscal account by Mexican origin and integration existed; whether that gap is chill or incentive is not
identified (the 2006 iSteve comment from an economics PhD student attributing it to low career reward, not political
correctness, is anecdote, cited only as the rival hypothesis).

## Steelmen

**Large chilling effect.** FIRE's deplatforming table shows immigration-topic speakers are attacked from the left 93% of
the time, twice the all-topic rate, and half the attempts succeed. Six scholars lost jobs over immigration-related speech
attacked from the left (2007–2020), and each case is public, so its deterrent reach is far larger than its count: 55% of
conservative faculty hide their politics to keep their jobs, over 9 in 10 Trump-supporting social scientists withhold
views from colleagues, and 4 in 10 academics would not hire a Trump supporter. In 2005 a direct question understated
support for ending immigration by 19 points, and by 45 among liberals and 42 among college graduates. The research field itself is one-eighth
restrictionist, and stance moves estimates. Documented incidents are a floor: FIRE finds only cases that reach the press.

**Few cases, mostly noise.** Immigration is 2.5% of 1,997 scholar incidents over 26 years, about two a year; 14 of 50
ended with no sanction, and in 2025–26 the immigration cases run the other way (government removal of books, ICE
detentions of foreign scholars). Students on the left report immigration as hard to discuss more often than
conservatives do. The best meta-analysis of list experiments finds prejudice items are reported honestly within ~5
points, and the one direct test of hidden restrictionist-adjacent voting (shy Trump, 2016) found none. The 2010 list
experiment's concealment gap was a third of 2005's, and overt restrictionism rose after 2008, which is the opposite of a
tightening chill. Label frequency rose for all prejudice terms in all coverage, which says nothing about immigration
specifically until the co-occurrence share is measured against a control topic.

## Attribution and cost

Every channel here is a response of natives' institutions to the debate, not a resource the group uses, so under the
attribution rule none enters the group's fiscal account. None identifies a dollar figure: a termination is a private
loss whose social cost runs through deterrence, and deterrence (Q2) and concealment (Q3) are measured as shares, with
no study linking them to output, policy error or research quality in dollars. Borjas–Breznau is the closest to a
quality measure (both-tail teams scored half an SD lower by referees), and it cuts both ways.

## Gaps and next queries

- Q4 co-occurrence: rerun `gdelt_labels.py`; or extract Rozado's Zenodo 5094015 articles rar (624 MB; needs `unrar`)
  and count immigration mentions among prejudice-term articles by year.
- Q1: double-code the 26 left-direction scholar cases by content; non-academic terminations have no dataset.
- Q2: HxA Campus Expression Survey; Norris 2023 Political Studies; Cato 2020.
- Q3: post-2010 list experiments on immigration (Brexit, AfD-era Germany, US 2016–24); AAPOR 2017 report text.
- Q5: survey of economists on publishing a negative-immigration finding (none found).

## Sources (load-bearing numbers)

- FIRE Scholars Under Fire and Campus Deplatforming tables, `fire.org/api/knack-data`, pulled 2026-10-21, sha256 in
  `code_incidents.py`; methodology PDF (Aug 2026) cached in `_cache/suf_methodology_aug2026.pdf`.
- FIRE 2027 CFSR report, fire.org/sites/default/files/2026/09/2027 College Free Speech Rankings Report.pdf ("Immigration 38%").
- FIRE 2026 CFSR report, fire.org/sites/default/files/2025/09/2026 College Free Speech Rankings Report.pdf ("Immigration 33%").
- FIRE 2020 CFSR report (mirror legalinsurrection.com/wp-content/uploads/2020/09/2020_college_free_speech_rankings-the-FIRE.pdf), liberal 48 / moderate 32 / conservative 31.
- FIRE, Silence in the Classroom (2024), fire.org/research-learn/silence-classroom-2024-fire-faculty-survey-report ("Only 17% of liberal faculty ... compared to a staggering 55% of conservative faculty"); toplines fire.org/sites/default/files/2024/12/2024-Faculty-Survey-Toplines.pdf.
- Kaufmann, Academic Freedom in Crisis, CSPI 2021, cspicenter.com/p/academic-freedom-in-crisis-punishment.
- Janus 2010, Social Science Quarterly 91(4), doi 10.1111/j.1540-6237.2010.00742.x; Table 2 journal p. 939 (42% vs 61%); the TESS page tessexperiments.org/study/janus297 summarises it as 40% vs 62%.
- Creighton, Jamal & Malancu 2015, IMR, doi 10.1111/imre.12091; author PDF amaneyjamal.com/wp-content/uploads/2014/07/Has-Opposition-to-Immigration-Increased.pdf.
- Creighton & Jamal 2015, Social Science Research, PMID 26188440; author PDF amaneyjamal.com/wp-content/uploads/2015/06/Does-Islam-Play-A-Role.pdf.
- Bazo Vienrich & Creighton 2017, JEMS, doi 10.1080/1369183x.2017.1334540 (abstract only).
- Blair, Coppock & Moor 2020, APSR 114(4), doi 10.1017/S0003055420000374.
- Coppock 2017, Statistics, Politics and Policy 8(1), doi 10.1515/spp-2016-0005 (32.5% direct, 29.6% list).
- Rozado, Al-Gharbi & Halberstadt 2023, SSCR 41(1), doi 10.1177/08944393211031452; data Zenodo 5094015.
- Borjas & Breznau 2024, NBER w33274, nber.org/system/files/working_papers/w33274/w33274.pdf.
- Verification (2026-10-21 15:40–15:55 JST): every percentage above was re-read from the primary PDF parsed locally
  with `pdftotext -layout` (or `-raw` for two-column APSR pages); page numbers are PDF pages unless marked "journal p.".
  FIRE PDFs came through a headless-browser session (JS challenge); Janus, CJM and Creighton–Jamal PDFs through the
  research corpus (`~/Projects/corpus/doi_*/paper.pdf`), then pdftotext. Kaufmann was checked against the CSPI HTML page
  only. One figure changed: Janus 40%/62% (TESS summary) → 42%/61% (published Table 2). The FIRE counts are computed from
  the raw records.

## Deviations from the pre-registration

- `\bICE\b` is matched case-sensitively (with re.I it would match "ice"); recorded in the script.
- The regex was found to have low precision on audit; FIRE's own tag is reported as the headline, the regex as an upper
  bound. No incident was hand-reclassified.
- "Any penalty" is this lane's grouping, added after the pre-registration; FIRE's raw outcome counts are reported beside it.

## Log

- 2026-10-21 15:09:23 JST stub written.
- 15:10:01 pre-registration written.
- 15:13:56 Q1 appended (FIRE tables pulled via headless browser; Firecrawl token invalid).
- 15:15:49 Q2–Q3 appended.
- 15:27:48 Q4–Q5, steelmen appended; GDELT pull running.
- 15:37:46 GDELT labelled query 429 ×6; Q4 route 2 marked [DEGRADED]; verdict finalised.
- 15:40–15:55 PDF verification pass; Janus corrected to 42%/61% (+19); page numbers added throughout.
- 16:00:47 GDELT retry (60 s spacing, 6 tries) failed with 429; Q4 stays [DEGRADED]. rerun_lane.py IDENTICAL 9/9, exit 0.
