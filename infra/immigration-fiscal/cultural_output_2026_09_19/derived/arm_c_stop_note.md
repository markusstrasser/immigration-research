# Arm C (registrations) — stopped, not run

Probed 2026-09-19 from this lane; every route to a per-capita inventor or
copyright-registration count was closed within the arm's budget.

| route | result |
|---|---|
| `https://s3.amazonaws.com/data.patentsview.org/download/g_patent.tsv.zip` (legacy bulk) | HTTP 403 [SOURCE: curl probe] |
| `https://patentsview.org/download/data-download-tables` | HTTP 301 to `https://data.uspto.gov/support/transition-guide/patentsview` [SOURCE: curl probe] |
| `https://search.patentsview.org/api/v1/patent/` (current API) | no response without an API key; the service requires registration [SOURCE: curl probe, http=000] |
| `https://publicrecords.copyright.gov/api/search_service/v2/search` | HTTP 200, but it is a record-search service, not bulk registration data |

The Copyright Office search service is reachable but would only answer
surname-by-surname queries, which cannot produce a per-capita registration
rate: the count returned for a surname mixes registration propensity with how
common the name is, and there is no denominator of name-bearers by year. That
is a different and weaker design than the brief's, so the arm is stopped rather
than run in a degraded form.

Obtaining a USPTO API key is the cheap fix if this arm is revived. Inventor
surnames plus the Census surname file would then reproduce the brief's design.
