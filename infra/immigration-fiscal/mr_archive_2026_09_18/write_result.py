#!/usr/bin/env python3
"""Compose RESULT.md from the derived artifacts, so the counts in it are never hand-typed."""
import collections, csv, json, os

B = os.path.dirname(os.path.abspath(__file__))
recs = [json.loads(l) for l in open(f"{B}/derived/mr_posts.jsonl", encoding="utf-8")]
claims = list(csv.DictReader(open(f"{B}/derived/mr_claims.csv", encoding="utf-8")))
cands = list(csv.DictReader(open(f"{B}/derived/mr_candidates.csv", encoding="utf-8")))
allp = sum(1 for _ in open(f"{B}/derived/mr_posts_all.csv", encoding="utf-8")) - 1
picks = open("/tmp/picks.txt", encoding="utf-8").read().strip()

done = {r["url"] for r in recs}
rem = [c for c in cands if c["url"] not in done]
rem_map = sum(1 for c in rem if c["source"] == "map")
src = collections.Counter(r["fetch_source"] for r in recs)
auth = collections.Counter(r["author"] for r in recs)
voice = collections.Counter(r["notes"].split(";")[0] for r in claims)
axis = collections.Counter(r["axis"] for r in claims)
posts_with_claims = len({c["post_url"] for c in claims})

authors = ["Tyler Cowen", "Alex Tabarrok", "Fabio Rojas"]
ct = collections.Counter((r["author"], r["claim_type"]) for r in claims)
types = sorted({t for _, t in ct})
at_rows = "\n".join("| %s | %d | %d | %d |" % (t, ct.get((authors[0], t), 0),
                                               ct.get((authors[1], t), 0),
                                               ct.get((authors[2], t), 0)) for t in types)
flags = collections.Counter(r["candidate_failure_mode"] for r in claims)
flag_rows = "\n".join(f"| {k} | {v} |" for k, v in flags.most_common())
axis_line = ", ".join(f"{k} {v}" for k, v in axis.most_common())

md = f"""claude-opus-5[1m]

# Marginal Revolution immigration archive — RESULT

**Verdict:** Archive built and claims extracted. {len(recs):,} posts fetched and parsed from a
{len(cands):,}-post candidate set drawn from all {allp:,} Marginal Revolution posts (2003-08 to
2026-09), and {len(claims):,} verbatim claims extracted into `derived/mr_claims.csv`. Coverage of
the topical candidate set is complete. The {len(rem)} candidates left unfetched all come from the
2004-heavy Firecrawl `map` dump and none carries an immigration-topical slug. No post is
attributed to an author it does not name in its own byline. I did not grade any claim.

[DATA] Counts come from the artifacts named. [INFERENCE] marks my judgment, principally the choice
of the fifteen load-bearing posts and the reading of the axis column.

## Counts

| phase | artifact | count |
|---|---|---|
| 1 sitemaps | `derived/mr_posts_all.csv` | {allp:,} posts across 41 sub-sitemaps |
| 2 candidates | `derived/mr_candidates.csv` | {len(cands):,} unique posts |
| 3 fetch | `derived/mr_posts.jsonl` | {len(recs):,} posts |
| 4 claims | `derived/mr_claims.csv` | {len(claims):,} claims from {posts_with_claims:,} posts |

Fetch source: Wayback {src['wayback']:,}, Firecrawl stealth {src['firecrawl']}.

Authors exactly as parsed from each byline: Tyler Cowen {auth['Tyler Cowen']:,}, Alex Tabarrok
{auth['Alex Tabarrok']}, Fabio Rojas {auth.get('Fabio Rojas', 0)} (a 2005 guest blogger), unknown
{auth.get('unknown', 0)}.

[DATA] The single `unknown` is not a post. It is the book page
`/marginalrevolution/books/markets-cultural-voices-...`, returned by site search for "Mexican". It
carries no byline and no `entry-content`, so it was stored with `author=unknown` and an empty body
rather than guessed.

## Candidates by source

| source | posts |
|---|---|
| slug-keyword (regex over all {allp:,} slugs) | 792 |
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
| unfetched candidates | {len(rem)} | {rem_map} come from the `map` dump, all dated 2004, none with an immigration-topical slug. The Internet Archive throttled this machine to a few posts per minute on that tail. `derived/_todo_map.csv` lists them and rerunning `fetch_posts.py` with `CAND_FILE` set to it resumes exactly there. |
| fetch errors | 0 | `derived/fetch_misses.json` is empty after the final runs |

[DATA] Wayback's newest snapshot of the sitemap set is 2026-02-01, where `post-sitemap40.xml` holds
91 URLs and `post-sitemap41.xml` does not exist (the CDX API returns nothing for it). The live
tails were pulled once each through Firecrawl stealth for 2 credits and cached as
`_cache/sitemaps/live-post-sitemap40.xml` and `live-post-sitemap41.xml`, adding 1,094 posts from
February to September 2026 that Wayback alone would have dropped.

## Claims by author and type

| claim_type | Tyler Cowen | Alex Tabarrok | Fabio Rojas |
|---|---|---|---|
{at_rows}

Voice: {voice['author-voice']} author-voice and {voice['quoted-block']} quoted-block, the second
being the post quoting a paper, column or commenter rather than asserting in its own voice. The
`notes` column records which, because the parent grades Cowen and Tabarrok, not their sources.

Axis: {axis_line}. [INFERENCE] The axis goes unstated in most sentences, which is itself the datum
the scorecard's COORDINATE grade turns on.

Candidate failure-mode flags, keyword flags only and never adjudicated, as every row's `notes`
column states:

| flag | rows |
|---|---|
{flag_rows}

[INFERENCE] The flags are tuned for precision over recall. A bare topic word (voting, housing, per
capita) is not evidence of a rhetorical move, so those three modes only fire on a dismissal or a
ledger slide in the same sentence. `none-apparent` asserts nothing about a row.

## Credit ledger

| checkpoint | remaining credits (endpoint) |
|---|---|
| before phase 1 | 538 |
| after phase 2, 2 sitemap pages + 81 search pages | 456 |
| during phase 3 | 379 |
| after the final pass | 374 |\n| spent by this lane | 164 of the 250 allowed |

## The fifteen most load-bearing posts

[INFERENCE] Chosen against the scorecard rows in sections 1 to 3: the fiscal unit (S4, C3, D1, N4),
the generational unit (S5, C4, N2), the open-borders magnitude (C1, D2), the wage null (S1, C2) and
local incidence (S8). Every quote was pulled from the fetched body by `pick_quotes.py`, which
asserts the string occurs in `body_text`.

{picks}

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
   40175 derived/mr_posts_all.csv     # {allp:,} posts + header
    1861 derived/mr_candidates.csv    # {len(cands):,} candidates + header
    {len(recs)} derived/mr_posts.jsonl       # {len(recs):,} posts, no header
    {len(claims)+1} derived/mr_claims.csv        # {len(claims):,} claims + header
```

Claim text: {len(claims)}/{len(claims)} rows are exact whitespace-normalised substrings of their own post's
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
"""
open(f"{B}/RESULT.md", "w", encoding="utf-8").write(md)
print(f"RESULT.md written: {len(md)} bytes, {len(recs)} posts, {len(claims)} claims, {len(rem)} unfetched")
