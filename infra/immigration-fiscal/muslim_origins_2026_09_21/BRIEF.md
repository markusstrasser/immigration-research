# Collection brief: Muslim immigrants in the United States, 2026-09-21

You are collecting sourced evidence for the repository `/Users/alien/Projects/immigration-research`
(topic: fiscal, crime and institutional impact of immigration). Your output is one notes file on
ONE axis, named in your task message. You COLLECT and SOURCE; you do not grade or conclude beyond
the verdict paragraph. The parent session weighs the evidence afterwards. Do not commit. Do not
edit any repo file other than your own notes file and files under this lane's `_cache/`.

## Axes

- **A. Mosque funding.** Who pays for the building and running of US mosques and Islamic centers.
  Wanted: (1) the systematic evidence: Ihsan Bagby's US Mosque Survey 2020 (ISPU) and earlier
  waves, on budgets, income sources, building finance, and any item on overseas donations;
  (2) the disclosure rule: whether houses of worship file IRS Form 990 (statute or IRS page);
  (3) documented foreign-state or foreign-charity cases with a primary document each: Saudi
  government funding of named US mosques or centers (Saudi official statements, GAO-05-852 or
  similar, Freedom House 2005), Turkey's Diyanet Center of America, the Alavi Foundation
  litigation (DOJ press releases, Second Circuit opinions), Qatar Charity or Kuwaiti funding of
  named US projects, the North American Islamic Trust's property holdings (its own statements,
  court exhibits); (4) evidence on the trend since 2001 and since 2017.
- **B. Outcomes, attitudes and extremism where religion is observed.** Census surveys do not ask
  religion. Wanted: (1) Pew's 2017 survey of US Muslims (and 2011, 2007): foreign-born share,
  education, income distribution, the attitude items on violence against civilians, sharia or
  religion in law if asked, homosexuality, and whether microdata are downloadable; (2) other
  datasets that observe religion with economic variables: New Immigrant Survey 2003 public-use
  files, the Cooperative Election Study religion item, ISPU's American Muslim Poll; (3) counts of
  jihadist-motivated offenders and deaths in the US by nativity and visa route, with
  denominators: Cato's terrorism-and-immigration risk analysis (latest edition), New America's
  database, the GWU Program on Extremism; (4) the Europe contrast: Koopmans 2015 on religious
  fundamentalism among European Muslims, and the Danish Finance Ministry's fiscal account for the
  MENAPT origin group, each from the primary document.

## Both directions (required)

For every axis record the strongest evidence FOR concern and the strongest AGAINST it, from
primary documents, with the same care. Examples of "against": mosque budgets that are locally
funded; base rates that make offender counts small; US Muslims' education and income relative to
the public. Examples of "for": court findings of foreign-state control; survey items with
illiberal majorities; offender counts by route. Do not soften or sharpen either side.

## Method (required)

1. Your FIRST tool call is a Write of a stub at your notes path containing the line
   `PROBE IN PROGRESS` and the tag `[UNVERIFIED]`. Append findings as you confirm them.
2. Primary sources only, fetched by you: the report, court opinion, agency page or dataset
   documentation itself. News articles count only as pointers to a primary document. Never take a
   number from a search-result snippet or from memory.
3. Save each document you rely on under
   `infra/immigration-fiscal/muslim_origins_2026_09_21/_cache/` (PDFs: `curl -sL -o`, then
   `pdftotext -layout`; never a schema-extraction tool for tables). Check every quote and number
   against the saved text with `rg` before recording it, and give the page or table reference.
4. Every recorded number carries: verbatim quote (≤ 60 words), URL, page or table, year of the
   data, the population it describes, and one of `[SOURCE]` / `[UNVERIFIED]`.
5. Budget: at most 8 web searches and 12 tool turns beyond the stub. Stop at the budget and write
   up what you have; the parent runs further epochs. Fetching x.com / twitter.com is blocked.
6. No commentary on data licensing. Never print API keys or environment secrets.

## Notes file (≤ 220 lines)

The first line is your exact model ID copied from your environment information. Then:

```
**Verdict:** one paragraph: what the primary documents establish, what they do not, what is
thin or missing, and which way the better-measured evidence points.

## Findings
| id | claim or number | verbatim quote | source (URL, page/table) | year · population | tag |

## Against concern / For concern   (two short lists of finding ids, no new claims)
## Datasets with religion observed (axis B) or funding observed (axis A): name, access, n, variables
## Documents read / skipped (URL, how much was readable, cache file)
## Searches run
```

When done, reply with the notes file path and at most 10 lines.
