# Muslim-majority origins: evidence collection

**Verdict:** two reader lanes collected 47 sourced findings from eleven primary documents, both
directions recorded, every quote checked against a cached copy; the parent re-checked 15.
Weighed in
[`research/immigration-muslim-origins-funding-outcomes-2026-09-21.md`](../../../research/immigration-muslim-origins-funding-outcomes-2026-09-21.md).
The repo's own measurements on the same question are in `admission_route_2026_09_21/`,
`high_skill_origin_screen_2026_09_21/` and `civic_service_by_ancestry_2026_09_21/`.

- `BRIEF.md`: the collection protocol (primary documents only, cache first, quotes checked with
  `rg`, "for concern" and "against concern" recorded with equal care, collectors do not conclude).
- `notes/mosque_funding.md` (ids A-), `notes/outcomes_attitudes_extremism.md` (ids B-): one file
  per reader, each opening with the model self-report and a `**Verdict:**`, each ending with the
  documents that failed and the next queries.
- `_cache/` (ignored): the statute page, IRS Pub. 1828, US Mosque Survey 2020 Report 1, the SDNY
  releases, Freedom House 2005, Pew 2017, Cato PA 991, Koopmans 2015, the Danish 2019 account.

## Fetch routes learned

- justice.gov: `/archive/usao/nys/pressreleases/…` paths fetch with curl; non-archive paths return
  a bot-check page to curl and to the fetch tool.
- CourtListener: the search API (`/api/rest/v4/search/?q=…&type=o&court=ca2`) answers without a
  token and located *In re 650 Fifth Ave.*, 934 F.3d 147 (2d Cir. 2019); the opinion page itself
  returned an empty 202. The opinion text is still unread.
- ISPU's mosque survey reports sit on a HubSpot CDN (URL in finding A3); ispu.org served HTML in
  place of the Report 2 PDF.
- diyanetamerica.org is JavaScript-rendered and nait.net returned HTTP 500: use a browser route.
- Pew's 2017 microdata need a free Pew account (operator action).
- Cato PA 991 is a two-column PDF: `pdftotext -layout` interleaves columns, so search quotes with
  `rg -U` and `\s+` between words.

## Not reached

New Immigrant Survey 2003 public-use files, the Cooperative Election Study religion item, ISPU's
American Muslim Poll, New America's and GWU's offender tables (the native-born arm Cato omits),
Form 990s of the non-church Islamic nonprofits, the 2011 and 2000 mosque survey waves, a Danish
edition later than income-year 2019.
