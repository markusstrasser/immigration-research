# Yglesias claim collection

**Verdict:** 40 claims and 15 concessions in his own words from 15 primary pieces, 2020-08 to
2026-07, every quote checked against a cached copy. Graded in
[`research/immigration-yglesias-claims-audit-2026-09-21.md`](../../../research/immigration-yglesias-claims-audit-2026-09-21.md).

- `BRIEF.md`: the collection protocol (own words only, cache first, quote checked with `rg`,
  evidence he cites recorded, collectors do not grade).
- `notes/economic_claims.md`, `notes/social_claims.md`: one file per reader agent, each opening
  with the model self-report and a `**Verdict:**`. Both list the posts not yet fetched.
- `_cache/` (ignored): fetched pages, the Slow Boring archive listing, the Borjas 1995 abstract page.
- `extract_post.py`: byline, date, paywall status and body text from a cached page, one summary
  line each: `uv run --no-project python3 extract_post.py _cache/sb_<slug>.html`. Checked against
  a free post (18,313 characters against the reader's 18,391), a paywalled preview and the
  Humphreys guest post.

Routes that work for Slow Boring: `sitemap.xml` for discovery (the archive API rejects
`sort=search`), then `slowboring.com/p/<slug>`; the body sits between `class="body markup"` and
`class="post-footer"`, the date is `datePublished` in the JSON-LD, and paywalled posts return
only the preview. Check `<meta name="author">`: three on-topic posts are guest posts (Kolko;
Elmendorf and Williams; Humphreys) and must not be attributed to him.
