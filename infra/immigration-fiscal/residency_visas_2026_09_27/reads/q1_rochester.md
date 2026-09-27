# Q1 reads: the Rochester claim (fetched 2026-09-28 JST)

## The claim's origin
- X post, @JobsNowPaper ("Expose H1B Fraud"), 2026-09-26, status 2103979055972569372 (not fetched: x.com
  automated fetching is barred; text as quoted by Instapundit https://instapundit.com/825541/, 2026-09-27):
  > "BREAKING: Rochester General Hospital in New York hired 82 resident doctors. 80 are foreign workers on H-1B
  > or J-1 visas. Only 2 are Americans. 98% of the residency slots went to visa workers- mostly from countries with
  > documented USMLE cheating. Americans got 2 jobs. pic.twitter.com/o8cnE8m3E9"
  The attached image was not seen; its content is unknown.

## Hospital's own roster: RGH Internal Medicine, "Current Residents"
URL https://education.rochesterregional.org/residencies/rgh-internal/current-residents/ (raw: `_cache/rgh_im_current.html`,
text `_cache/rgh_im_current.txt`, made by `strip_html.py`). Counted by `roster.py` → `derived/roster_counts.txt`:
- Chief Residents 5 (Pakistan 2, Nepal, Sudan, Algeria) — these five appear on the program's Graduates page under
  "Class of 2024-2025", so the page shows academic year 2025-26 [SOURCE: .../rgh-internal/graduates/].
- PGY3 24, PGY2 25, PGY1 24. Total names on the page: 78.
- US-school graduates on the page: 2, both Lake Erie College of Osteopathic Medicine (DO):
  "[name] / Lake Erie College of Osteopathic Medicine" (PGY2); "[name] / Lake Erie College of
  Osteopathic Medicine – USA" (PGY1).
- Caribbean-school graduates (schools that mostly enrol US citizens; citizenship NOT stated on the page): "[name]
  / Saba University School of Medicine" (PGY3), "[name] / Ross University School of Medicine" (PGY3),
  "[name] / American University of Antigua College of Medicine – Antigua & Barbuda" (PGY1).
  [Residents' names redacted by the parent before commit; they are on the public page and in the ignored `_cache/`.]
- The page lists medical school only. It states no visa status, citizenship or permanent-residence status.

## Program page: size, visa policy, pay
URL https://education.rochesterregional.org/residencies/rgh-internal/ (text `_cache/rgh_im_main.txt`):
- "24 / R1 Positions" · NRMP number "1509140c0".
- "Sponsorship of J1 and H1 VISAS will be subject to current immigration regulations. If the applicant qualifies for
  an H1B VISA, but the program is unable to secure the VISA in time for the program start date, the applicant must be
  willing to accept a J1 VISA."
- "The following is a list of benefits granted to all residents at no charge." ... "Salaries are paid on a bi-weekly
  basis with a $3,000 annual stipend ... included in the annual salary. The salaries for the 25-26 academic year will
  be: $73,000 PGY-1 / $76,000 PGY-2 / $80,000 PGY-3". One scale; no visa-status distinction on the page.

## AMA FREIDA listing, program 1403531314 (via Exa highlight, 2026-09-28)
https://freida.ama-assn.org/program/1403531314/program-work-schedule : "J-1 visa sponsorship through ECFMG Yes /
H-1B visa No / F-1 visa (OPT 1st year) No" · "Program Size 72 Current Residents / Year 1 24 / Year 2 24 / Year 3 24".
(FREIDA's "H-1B No" conflicts with the program page and with DOL LCA filings below; FREIDA is program-reported and may
be stale.)

## DOL LCA disclosure aggregators (secondary; DOL is the primary)
- h1binfo.org: Rochester General Hospital "Medical Resident Physician 77 [certified LCAs FY2020–FY2026] $65,693
  median"; "Medical Resident 16 $62,056". myvisajobs.com: "filed 89 labor condition applications (LCAs) for H-1B
  visas ... during fiscal year 2025". USCIS H-1B employer-data-hub counts as reproduced there: "2025 | 120 new
  approvals"; 2024: 35; 2023: 30. These cover all RGH occupations (hospitalists, nurses, fellows), not residents only.
  [SECONDARY, not re-derived from DOL files this lane]

## Weill Cornell Medicine-Qatar graduates are IMGs (2 on the roster)
https://qatar-weill.cornell.edu/admissions/medical-program/four-year-medical-curriculum/frequently-asked-questions
(via Exa, 2026-09-28): "Why are graduates of WCM-Q considered IMGs (International Medical Graduates)? Anyone who
graduates from a medical school whose location is outside of the geographic boundaries of the United States or Canada
is considered an International Medical Graduate (IMG)." "WCM-Q Medical Program graduates may enter ERAS and the
National Residency Match Program (NRMP) as International Medical Graduates (IMGs)."

## Related documented pattern (secondary news)
- Fox News via satoji.com mirror, 2026-03-31: Do No Harm filed a Title VI complaint with HHS against Corewell
  (Dearborn), Texas Tech and HCA Brandon IM programs: "at the internal medicine program at Corewell Health in
  Dearborn, Michigan, just one of the 33 residents attended an American medical school"; "At Texas Tech University,
  95% of the 39 internal medicine residents were also trained at foreign medical schools".
