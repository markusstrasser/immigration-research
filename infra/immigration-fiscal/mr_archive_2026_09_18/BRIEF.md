# Lane brief: Marginal Revolution immigration archive + claim extraction (2026-09-18)

## Goal
Build a complete, reproducible archive of every Marginal Revolution (marginalrevolution.com; authors Tyler Cowen and Alex Tabarrok) post about immigration, Mexico/Mexicans, Hispanics/Latinos, Latin America, borders, asylum/refugees, deportation, open borders, and immigrant crime/fiscal/wage effects, 2003 to today. Then extract every checkable claim into a table the parent can grade against the repo's scorecard rubric (`research/immigration-claim-scorecard-2026-09-18.md`, grades HARD / COORDINATE / AGREE). You do NOT grade; you extract and quote. Analysis agents do not commit.

## What is already verified (do not re-probe)
- Direct curl and headless browser (agent-browser) hit a Cloudflare challenge on every marginalrevolution.com URL except `/feed`. WP REST API returns 401.
- Firecrawl `stealth` proxy passes Cloudflare (1 credit/page). Key: `FIRECRAWL_API_KEY` in `~/.env` (never print it). Remaining credits at 20:20 CEST: 539 of 1000. Budget for this lane: at most 250 credits. Check `GET https://api.firecrawl.dev/v1/team/credit-usage` before and after each phase and record in RESULT.md.
- Yoast sitemap index `https://marginalrevolution.com/sitemap_index.xml` lists `post-sitemap.xml` and `post-sitemap2.xml` … `post-sitemap41.xml` (about 1,000 posts each, chronological). The Wayback Machine serves `https://web.archive.org/web/2026id_/https://marginalrevolution.com/post-sitemap.xml` (200, 157 KB). Try Wayback `id_` for every sub-sitemap first; use Firecrawl stealth only for the ones Wayback lacks.
- Wayback serves post pages in full: `https://web.archive.org/web/2024id_/https://marginalrevolution.com/marginalrevolution/2015/09/facts-about-mexicans.html` → 200, `entry-content` present. Use `id_` to get the raw page. Wayback rate limit: stay at ≤1 request/second, retry 429/5xx with backoff, and cache every response on disk immediately so nothing is lost if the lane dies.
- On-site search works through Firecrawl stealth: `https://marginalrevolution.com/?s=<kw>` and `/page/N?s=<kw>`; with `onlyMainContent=false` and `formats=["html"]` the HTML carries `<h2 class="entry-title"><a href="…">Title</a>`, the byline, and "Results for “kw”   N found". About 10–16 posts per page.
- Exa hits (49 URLs) are in `/tmp/mr_exa_urls.txt`; Firecrawl map hits (466 URLs, mostly 2004) in `/tmp/mr_map_urls.txt`. Union them into the candidate set.

## Layout (own these paths only)
`infra/immigration-fiscal/mr_archive_2026_09_18/`
- `fetch_sitemaps.py` → `_cache/sitemaps/post-sitemapN.xml`; `derived/mr_posts_all.csv` (url, date, slug). Report the total post count.
- `select_candidates.py` → `derived/mr_candidates.csv` with a `source` column (slug-keyword | site-search:<kw> | exa | map). Slug regex (case-insensitive): `immigra|migrant|migration|mexic|hispanic|latino|latin-america|border|deport|asylum|refugee|open-borders|h-1b|h1b|visa|naturaliz|remittance|borjas|caplan|nowrasteh|clemens|peri|mariel|amnesty|dreamer|daca|undocumented|illegal|assimilat|enclave|nativis|diversity|huntington|sailer|puerto-ric|cuban|salvador|guatemal|hondur|venezuel|haiti`. Site search: run `immigration`, `immigrants`, `Mexican`, `Mexico`, `Hispanic`, `Latino`, `open borders`, `border`, `deportation`, `asylum` through Firecrawl, all pages, until the credit cap; record the "N found" per keyword.
- `fetch_posts.py` → `_cache/posts/<sha1(url)>.html` (Wayback first, Firecrawl fallback, record which); `derived/mr_posts.jsonl` with url, title, author (byline: Tyler Cowen / Alex Tabarrok / guest), date, categories/tags, body_text (entry-content, quotes preserved with `> `), outbound links, fetch_source, wayback_timestamp.
- `extract_claims.py` (may be a script that writes a template and you fill it by reading, or a keyword-anchored extractor plus your reading) → `derived/mr_claims.csv`: post_url, date, author, claim_text (verbatim quote ≤ 60 words), claim_type (fiscal | wage | crime | assimilation | housing | political | welfare-use | culture | global-gains | other), object (first generation | descendants | all immigrants | Mexican-origin | low-skill | high-skill | unclear), axis (federal | resident/all-government | national average | local | unstated), quoted_source (the paper/report the post leans on, if any), candidate_failure_mode (one of the 7 in `research/immigration-economist-rhetorical-failures-2026-04-22.md`: ledger switching, upper-bound laundering, marginal-to-mass extrapolation, capacity erasure, denominator masking, political-economy erasure, aggregate-output trump card; or `none-apparent`), notes.
- `RESULT.md` opening `**Verdict:**`, then counts (posts in sitemap; candidates by source; fetched; missing with reasons; claims by author × type), the credit ledger, and the 15 posts you judge most load-bearing for the parent's grading, each with one verbatim quote.
- `_cache/` is gitignored repo-wide (`**/_cache/`). Add a `derived/.gitignore` only if a derived file exceeds 10 MB.

## Rules
- `uv run --no-project --with "pandas>=2" --with requests --with lxml python3 <script>`; scripts >10 lines in files; line-based progress output; `PYTHONUNBUFFERED=1` for logs.
- Never print the API key. Never write outside the lane directory except `/private/tmp/claude-501/…/scratchpad`.
- Wrongly attributing a post to Cowen vs Tabarrok is the most likely defect: parse the byline, and where the Wayback copy lacks one, mark `author=unknown`, never guess.
- Quotes must be verbatim from the fetched body. Tag anything from memory `[TRAINING-DATA]` and keep it out of `mr_claims.csv`.
- Do not grade, do not write the memo, do not edit anything under `research/`. Do not commit.
- If Wayback is down (it returned "Temporarily Offline" once at 20:15 CEST), wait 60 s and retry up to 10 times before switching that URL to Firecrawl.
- Turn budget: work in phases and update RESULT.md after each phase so partial progress survives.
