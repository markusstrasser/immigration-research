claude-opus-5[1m]

# Marginal Revolution immigration archive — RESULT

**Verdict:** Archive built and claims extracted. 1,723 posts fetched and parsed from a
1,860-post candidate set drawn from all 40,174 Marginal Revolution posts (2003-08 to
2026-09), and 1,093 verbatim claims extracted into `derived/mr_claims.csv`. Coverage of
the topical candidate set is complete. The 137 candidates left unfetched all come from the
2004-heavy Firecrawl `map` dump and none carries an immigration-topical slug. No post is
attributed to an author it does not name in its own byline. I did not grade any claim.

[DATA] Counts come from the artifacts named. [INFERENCE] marks my judgment, principally the choice
of the fifteen load-bearing posts and the reading of the axis column.

## Counts

| phase | artifact | count |
|---|---|---|
| 1 sitemaps | `derived/mr_posts_all.csv` | 40,174 posts across 41 sub-sitemaps |
| 2 candidates | `derived/mr_candidates.csv` | 1,860 unique posts |
| 3 fetch | `derived/mr_posts.jsonl` | 1,723 posts |
| 4 claims | `derived/mr_claims.csv` | 1,093 claims from 562 posts |

Fetch source: Wayback 1,643, Firecrawl stealth 80.

Authors exactly as parsed from each byline: Tyler Cowen 1,426, Alex Tabarrok
283, Fabio Rojas 13 (a 2005 guest blogger), unknown
1.

[DATA] The single `unknown` is not a post. It is the book page
`/marginalrevolution/books/markets-cultural-voices-...`, returned by site search for "Mexican". It
carries no byline and no `entry-content`, so it was stored with `author=unknown` and an empty body
rather than guessed.

## Candidates by source

| source | posts |
|---|---|
| slug-keyword (regex over all 40,174 slugs) | 792 |
| map (Firecrawl site map, 2004-heavy) | 466 |
| site-search across 10 keywords | 1,146 keyword-rows |
| exa | 49 |

Site-search totals the site itself reported ("N found") against the pages actually retrieved, at
15 results per page:

| keyword | N found | pages fetched |
|---|---|---|
| border | 1,153 | 10 |
| immigration | 769 | 10 |
| Mexico | 706 | 10 |
| immigrants | 498 | 10 |
| Mexican | 418 | 10 |
| open borders | 176 | 4 |
| Hispanic | 151 | 10 |
| Latino | 98 | 8 |
| asylum | 58 | 5 |
| deportation | 30 | 3 |

[DATA] The 10-page cap per keyword was set by the credit budget, so site search contributed the
most recent ~150 hits per keyword rather than the full result set. Full-history coverage comes from
the slug regex over every post; site search adds posts whose body mentions the topic while the slug
does not, and those skew recent.

[DATA] All 49 Exa URLs were truncated MovableType-era paths without `.html`. Each was resolved to a
real post URL by prefix match against the sitemap set before fetching.

## Missing, with reasons

| what | count | reason |
|---|---|---|
| unfetched candidates | 137 | 137 come from the `map` dump, all dated 2004, none with an immigration-topical slug. The Internet Archive throttled this machine to a few posts per minute on that tail. `derived/_todo_map.csv` lists them and rerunning `fetch_posts.py` with `CAND_FILE` set to it resumes exactly there. |
| fetch errors | 0 | `derived/fetch_misses.json` is empty after the final runs |

[DATA] Wayback's newest snapshot of the sitemap set is 2026-02-01, where `post-sitemap40.xml` holds
91 URLs and `post-sitemap41.xml` does not exist (the CDX API returns nothing for it). The live
tails were pulled once each through Firecrawl stealth for 2 credits and cached as
`_cache/sitemaps/live-post-sitemap40.xml` and `live-post-sitemap41.xml`, adding 1,094 posts from
February to September 2026 that Wayback alone would have dropped.

## Claims by author and type

| claim_type | Tyler Cowen | Alex Tabarrok | Fabio Rojas |
|---|---|---|---|
| assimilation | 73 | 2 | 1 |
| crime | 82 | 15 | 0 |
| culture | 27 | 5 | 0 |
| fiscal | 63 | 24 | 0 |
| global-gains | 52 | 18 | 0 |
| housing | 22 | 7 | 0 |
| other | 345 | 57 | 3 |
| political | 127 | 8 | 0 |
| wage | 129 | 33 | 0 |

Voice: 430 author-voice and 663 quoted-block, the second
being the post quoting a paper, column or commenter rather than asserting in its own voice. The
`notes` column records which, because the parent grades Cowen and Tabarrok, not their sources.

Axis: unstated 906, national average 92, local 78, federal 17. [INFERENCE] The axis goes unstated in most sentences, which is itself the datum
the scorecard's COORDINATE grade turns on.

Candidate failure-mode flags, keyword flags only and never adjudicated, as every row's `notes`
column states:

| flag | rows |
|---|---|
| none-apparent | 1069 |
| ledger switching | 15 |
| upper-bound laundering | 5 |
| denominator masking | 2 |
| marginal-to-mass extrapolation | 1 |
| political-economy erasure | 1 |

[INFERENCE] The flags are tuned for precision over recall. A bare topic word (voting, housing, per
capita) is not evidence of a rhetorical move, so those three modes only fire on a dismissal or a
ledger slide in the same sentence. `none-apparent` asserts nothing about a row.

## Credit ledger

| checkpoint | remaining credits (endpoint) |
|---|---|
| before phase 1 | 538 |
| after phase 2, 2 sitemap pages + 81 search pages | 456 |
| during phase 3 | 379 |
| after the final pass | 374 |
| spent by this lane | 164 of the 250 allowed |

## The fifteen most load-bearing posts

[INFERENCE] Chosen against the scorecard rows in sections 1 to 3: the fiscal unit (S4, C3, D1, N4),
the generational unit (S5, C4, N2), the open-borders magnitude (C1, D2), the wage null (S1, C2) and
local incidence (S8). Every quote was pulled from the fetched body by `pick_quotes.py`, which
asserts the string occurs in `body_text`.

- **Alex Tabarrok, 2024-05-07 — The Fiscal Impact of Low-Skill Immigration**
  https://marginalrevolution.com/marginalrevolution/2024/05/the-fiscal-impact-of-low-skill-immigration.html
  > Overall the NAS concluded that the net fiscal impact of the average immigrant was positive.

- **Tyler Cowen, 2024-05-10 — TC on less-skilled immigrants not being a fiscal burden**
  https://marginalrevolution.com/marginalrevolution/2024/05/tc-on-less-skilled-immigrants-not-being-a-fiscal-burden.html
  > According to new research from economists at the University of Oregon and the University of St. Gallen in Switzerland, new low-skilled immigrants to the US are a net fiscal plus — each adding an estimated $750 a year to government coffers at the federal, state and local levels.

- **Alex Tabarrok, 2015-09-22 — Open Borders and the Welfare State**
  https://marginalrevolution.com/marginalrevolution/2015/09/open-borders-and-welfare.html
  > Milton Friedman famously said that you can’t have a welfare state and open borders.

- **Alex Tabarrok, 2021-08-29 — Hispanic and White Criminality are Converging**
  https://marginalrevolution.com/marginalrevolution/2021/08/hispanics-and-white-criminality-are-converging.html
  > An otherwise dull new government report on incarceration contains a startling fact: Hispanics are slightly less likely to be jailed than whites.

- **Tyler Cowen, 2019-05-02 — Caplan, Weinersmith, and Open Borders**
  https://marginalrevolution.com/marginalrevolution/2019/05/caplan-weinersmith-and-open-borders.html
  > The simplest argument against open borders is the political one.

- **Tyler Cowen, 2026-08-12 — Immigrant Earnings Assimilation, 1981–2021**
  https://marginalrevolution.com/marginalrevolution/2026/08/immigrant-earnings-assimilation-1981-2021.html
  > Third, earnings assimilation occurs relatively quickly for cohorts arriving since the mid-1990s: The earnings of permanent immigrants converge, or come close to converging, with those of native-born people within 10 years after arrival.

- **Alex Tabarrok, 2023-12-02 — Immigration Backlash**
  https://marginalrevolution.com/marginalrevolution/2023/12/immigration-backlash.html
  > Recent inflows of unauthorized migrants increase the vote share for the Republican Party in federal elections, reduce local public spending, and shift it away from education towards law-and-order.

- **Tyler Cowen, 2024-09-26 — Cutting welfare for immigrants**
  https://marginalrevolution.com/marginalrevolution/2024/09/cutting-welfare-for-immigrants.html
  > A variety of different groups will not like it when I say this, but at least sometimes immigration flows and a welfare state are complements.

- **Tyler Cowen, 2025-09-24 — Michael Clemens on H1-B visas**
  https://marginalrevolution.com/marginalrevolution/2025/09/michael-clemens-on-h1-b-visas.html
  > From 1990 to 2010, rising numbers of H-1B holders caused 30–50 percent of all productivity growth in the US economy.

- **Tyler Cowen, 2026-01-11 — Low-skilled immigration into the UK**
  https://marginalrevolution.com/marginalrevolution/2026/01/low-skilled-immigration-into-the-uk.html
  > The literature does not support the claim that low-skilled immigration has imposed large net welfare losses on the UK as a whole.

- **Tyler Cowen, 2026-01-14 — Negative political externalities from migration to Britain?**
  https://marginalrevolution.com/marginalrevolution/2026/01/negative-political-externalities-from-migration-to-britain.html
  > If this is the argument, one needs to admit that immigration has gone well enough in the UK to date.

- **Tyler Cowen, 2019-05-24 — State and local policy is the real immigration policy**
  https://marginalrevolution.com/marginalrevolution/2019/05/state-and-local-policy-is-the-real-immigration-policy.html
  > State and local governments are making immigration policy all the time, mostly for the worse, and often Democrats are more restrictionist than Republicans.

- **Tyler Cowen, 2024-04-30 — Updated estimates on immigration and wages**
  https://marginalrevolution.com/marginalrevolution/2024/04/updated-estimates-on-immigration-and-wages.html
  > Using these estimates, we calculate that immigration, thanks to native-immigrant complementarity and college skill content of immigrants, had a positive and significant effect between +1.7 to +2.6\% on wages of less educated native workers, over the period 2000-2019 and no significant wage effect on college educated natives.

- **Tyler Cowen, 2025-01-26 — Do Migrants Pay Their Way? A Net Fiscal Analysis for Germany**
  https://marginalrevolution.com/marginalrevolution/2025/01/do-migrants-pay-their-way-a-net-fiscal-analysis-for-germany.html
  > When controlling for demographic differences between these groups, we show that second-generation migrants contribute very similarly to natives to the German welfare state.

- **Tyler Cowen, 2026-02-12 — The economics of mass deportation**
  https://marginalrevolution.com/marginalrevolution/2026/02/the-economics-of-mass-deportation.html
  > In the long run, however, native real wages fall in every state, and by 0.33% nationally, as capital gets decumulated in response to a lower population.

## Files

Scripts: `fetch_sitemaps.py`, `select_candidates.py`, `fetch_posts.py`, `extract_claims.py`,
`spotcheck.py` (byline verification), `rank_loadbearing.py`, `pick_quotes.py`, `write_result.py`.

Data: `derived/mr_posts_all.csv`, `derived/mr_candidates.csv`, `derived/mr_posts.jsonl`,
`derived/mr_claims.csv`, `derived/search_meta.json`, `derived/fetch_misses.json`,
`derived/_todo_map.csv`. Every fetched page is in `_cache/` with a `.meta` sidecar recording
`fetch_source` and `wayback_timestamp`.

## How the fetch handled the Internet Archive

[DATA] Three distinct failure modes appeared and each is handled in `fetch_posts.py`:

1. A 403 whose body is "Internet Archive: Temporarily Offline". Transient, so the URL is deferred
   to a later pass rather than parking a worker on a sleep.
2. A capture that is itself an archived Cloudflare block page, which replays with status 403 or as
   an "Attention Required" page. The CDX API is then asked for a 200-status capture, behind a
   circuit breaker because CDX goes down independently of the replay servers.
3. Outright connection refusal from `web.archive.org` while `archive.org` stayed up, which is
   rate-limiting of this host. Firecrawl stealth covers the highest-value posts during those
   windows, which is why the recent years are fetched first.

All Internet Archive traffic, replay and CDX alike, passes through one process-wide token bucket at
one request per second, so the worker count raises throughput without raising the request rate.

## Verification run

```
$ wc -l derived/mr_posts_all.csv derived/mr_candidates.csv derived/mr_posts.jsonl derived/mr_claims.csv
   40175 derived/mr_posts_all.csv     # 40,174 posts + header
    1861 derived/mr_candidates.csv    # 1,860 candidates + header
    1723 derived/mr_posts.jsonl       # 1,723 posts, no header
    1094 derived/mr_claims.csv        # 1,093 claims + header
```

Claim text: 1093/1093 rows are exact whitespace-normalised substrings of their own post's
fetched `body_text`. `extract_claims.py` asserts this on every run and prints the ratio.

`derived/fetch_misses.json` is `[]`: no candidate that was attempted failed.

Spot check of five random posts, `mr_posts.jsonl` against the raw cached HTML byline, run twice
with different seeds:

- `spotcheck.py 2026`: author matched the raw byline 5 of 5, date present in the raw HTML 5 of 5,
  title exact 4 of 5. The fifth differs only because the raw HTML carries `&#8217;` where the
  parser stores the decoded apostrophe, a decoding difference rather than a mismatch.
- `spotcheck.py 77`: author, date and title all matched 5 of 5.

Firecrawl credit-usage endpoint, `GET https://api.firecrawl.dev/v1/team/credit-usage`: 538
remaining before the lane, 456 after phase 2, 379 during phase 3, 374 at the end. 164 credits spent
against the 250 the brief allowed.
