# PSID exact-generation completeness audit

**Later verification, 2026-09-20 — route closed for this workflow:** the in-app
browser reached PSID's ZIP warning: Conditions of Use have not been accepted.
The [current conditions](https://simba.isr.umich.edu/U/CondUse.aspx), item5,
explicitly prohibit AI programs and LLMs in conjunction with PSID data. This
is a use restriction in addition to the authentication gate described below.
No conditions were accepted, no account created, no microdata downloaded and
no contact sent. Reopening requires PSID permission covering the intended
workflow or a separately conducted compliant human analysis. User login alone
would not resolve this restriction. Earlier access findings are retained below.

**Status, 2026-09-20:** primary field audit complete; microdata access and joint
completeness counts pending. No data were obtained from the attempted downloads.
PSID registration is separate from ICPSR. No account creation, access application,
or third-party contact was undertaken.

## Required source files

- [2023 family file, official package1214](https://simba.isr.umich.edu/Zips/GetFileCDS.aspx?file=1214&mainurl=Y)
- [1968–2023 individual file, package1053](https://simba.isr.umich.edu/Zips/GetFileCDS.aspx?file=1053&mainurl=Y)
- [2023 parent-ID file, package1123](https://simba.isr.umich.edu/Zips/GetFileCDS.aspx?file=1123&mainurl=Y),
  or [FIMS](https://simba.isr.umich.edu/FIMS/) retrospective wide mapping for
  biological parents, grandparents and great-grandparents, retaining incomplete
  records and roster-only ancestors.
- Historical family/childbirth birthplace fields as needed after mapping their
  documented release universes. Keep dead and attrited ancestors for birthplace
  lookup; they need not have current survey weights.

Official package requests reached login/conditions-of-use pages in web retrieval;
direct requests returned HTTP403 HTML security challenges. A challenge page is
not a ZIP or codebook. A successfully authenticated session is needed before
attempting an extract. The audit does not infer the user's browser login state.

## Verified fields and distinctions

| Item | Fields | Interpretation |
|---|---|---|
| Reported Mexican origin | ER85120 reference person; ER84993 spouse/partner; codes1/2/3 | Published marginal counts567+364=931 adult-role records, before completeness |
| Current state of birth | ER85113 / ER84986 | State codes establish a US state; zero pools territories/foreign birth |
| Year arrived | ER85114 / ER84987 | Timing does not identify Mexico as birthplace |
| Historical individual country of birth | ER33421/ER33422 in1997; ER33524/ER33525 in1999 | Join state and country and honor applicable universes; zero is not proof of US birth |
| Stable person identity | ER30001 + ER30002 | Use source-documented current family ID and role to attach current reference/spouse information |
| Pedigree | FIMS retrospective GID or recursively joined PID | Biological versus adoptive links separate; panelG1/G2 labels are not immigrant generations |

Sources: [family codebook](https://psidonline.isr.umich.edu/documents/psid/codebook/FAM2023ER_codebook.pdf),
pp.1039,1041,1113–1115;
[individual codebook](https://psidonline.isr.umich.edu/documents/psid/codebook/IND2023ER_codebook.pdf),
pp.598–600,623–624;
[FIMS manual](https://simba.isr.umich.edu/FIMS/FIMS_UG.pdf),pp.3–5,8,12–13.
The [2023 questionnaire](https://psidonline.isr.umich.edu/documents/psid/questionnaires/q2023.pdf)
collects country through KL33COUNTRY and child birth/adoption fields; current
public/sensitive/restricted release mapping remains to be established. Do not
equate birthplace with the country where a person grew up.

## Execution after access

1. Hash source ZIPs and codebooks; verify member lists and actual file signatures.
2. Define focal Mexican-origin respondents and current weights independently of
   whether ancestors are linked. Do not assign children a parent's identity by default.
3. Map biological parent branches with stable IDs. Resolve birthplace from
   applicable reports with wave/variable provenance; retain conflicts and unknowns.
4. Tabulate focal n/weighted population, linked parents, all-four-grandparent
   birthplace completeness, any great-grandparent, all-eight-great-grandparent
   completeness, and effective sample size by age and sample-entry cohort.
5. Identify exact MexicanG4 only when self, both parents and four grandparents
   are confirmed US-born and at least one great-grandparent is confirmed
   Mexico-born. The other seven great-grandparents need not all be observed
   once the nearer-generation exclusions are complete.
6. Identify genericG5+ among Mexican identifiers only when self, both parents,
   all four grandparents and all eight great-grandparents are confirmed US-born.
   This neither proves Mexican origin farther back nor separates G5 from G6+.
7. Stop before national/outcome modeling if completeness, weights or support are
   inadequate. Publish the missingness audit rather than fill branches with names,
   income, a US-state-code zero, or assumptions about panel duration.

The 1990 Latino sample ended in1995; later immigrant refreshment does not repair
every missing ancestral branch. See [PSID FAQ](https://psidonline.isr.umich.edu/guide/faq.aspx).
