# IQ Sex Differences - Access Playbook

**Date:** 2026-03-06  
**Purpose:** turn the remaining high-value external datasets from vague blockers into exact access states.

## Why This Exists

The repo already has enough public-use data to avoid random new acquisitions.

The remaining high-leverage targets are now mostly access-gated. That means the useful question is not “is this dataset real?” It is:

1. what is the exact official access path
2. what is the actual blocker
3. what can be automated now
4. what cannot be automated without credentials, licensing, or a human decision

Probe artifacts:

- [psid_access_probe.py](/Users/alien/Projects/research/sources/iq-sex-diff/psid_access_probe.py#L1)
- [psid_access_probe_latest.txt](/Users/alien/Projects/research/sources/iq-sex-diff/data/psid/psid_access_probe_latest.txt#L1)
- [psid_datacenter_probe.txt](/Users/alien/Projects/research/sources/iq-sex-diff/data/psid/psid_datacenter_probe.txt#L1)

## 1. `PSID CDS/TAS`

### Official live path

- `CDS-TAS` home: [SOURCE: https://psidonline.isr.umich.edu/CDS/]
- `Getting Started`: [SOURCE: https://psidonline.isr.umich.edu/CDS/GettingStarted.aspx]
- `CDS-TAS Data Center`: [SOURCE: https://simba.isr.umich.edu/CDS/default.aspx]
- registration page: [SOURCE: https://simba.isr.umich.edu/U/login.aspx?Tabid=1]
- `Additional Files`: [SOURCE: https://simba.isr.umich.edu/CDS/Zips/AdditionalFiles.aspx]

### What the official docs say

- the home page says the data center provides “easy and free access” to all waves of `CDS` and `TAS` [SOURCE: https://psidonline.isr.umich.edu/CDS/]
- the `Getting Started` page says `Registration is required` to download public-use data and codebooks, and says restricted data require either a restricted data application or the `Virtual Data Enclave` [SOURCE: https://psidonline.isr.umich.edu/CDS/GettingStarted.aspx]

### What works locally now

- the public-use `CDS` and `TAS` bundles are now downloaded and staged under `sources/iq-sex-diff/data/psid/downloads/`
- the relevant bundles are unpacked under `sources/iq-sex-diff/data/psid/unpacked/`
- the first cleaned child panel is now built and analyzed locally [SOURCE: `research/iq-sex-differences-psid-cds-first-pass.md`; `sources/iq-sex-diff/data/psid/psid_cds_panel.parquet`]

### Historical blocker

- the earlier registration / Cloudflare wall was real for direct scripted access
- that blocker is now resolved for this repo because the public-use downloads were completed through an authenticated session and landed locally [SOURCE: `sources/iq-sex-diff/data/psid/psid_access_probe_latest.txt`; `research/iq-sex-differences-psid-cds-first-pass.md`]

### Operational read

`PSID CDS/TAS` is no longer a live acquisition blocker for the repo. The public child panel is built and the public transition panel is now built too. The live question is no longer access. It is interpretation and whether the `TAS` transition wedge should be treated as the same family as the late-school evaluation-versus-tested split. [INFERENCE]

### Next step if we want more from it

1. keep `CDS` as the canonical family-linked child panel
2. treat `TAS` as a built transition extension, not as an access problem
3. if stronger leverage is needed, move to mediator design or restricted transcript/process access rather than reopening `PSID` acquisition

## 2. `HSTS` / transcript microdata

### Official live path

- transcript overview: [SOURCE: https://nces.ed.gov/surveys/slsp/transcripts.asp]
- `HSTS` study page: [SOURCE: https://nces.ed.gov/nationsreportcard/hsts/]
- `HSTS` design page: [SOURCE: https://nces.ed.gov/nationsreportcard/hsts/design.aspx]

### What the official docs say

- transcript data across `HS&B`, `NELS`, `ELS`, `HSLS`, and `NAEP HSTS` are available **only as restricted-use data** because of sensitivity [SOURCE: https://nces.ed.gov/surveys/slsp/transcripts.asp]
- transcript collections are the official and fixed record of courses, credits, and grades [SOURCE: https://nces.ed.gov/surveys/slsp/transcripts.asp]

### Operational read

This is **not** a broken public endpoint problem. It is a licensing problem by design. [INFERENCE]

### Next step if we want it

1. decide whether the project justifies an NCES restricted-use license
2. if yes, use the NCES restricted-use application path
3. if no, stop pretending the public web has the transcript microdata hiding somewhere

## 3. `NAEP` process data

### Official live path

- `NAEP Process Data`: [SOURCE: https://www.nationsreportcard.gov/process_data/]
- NCES restricted-use license page linked from that site: [SOURCE: https://nces.ed.gov/pubsearch/licenses.asp#license]

### What the official docs say

- the 2017 grade 4 and grade 8 math process releases include restricted-use response materials, process files, released cognitive items, and survey questionnaire files [SOURCE: https://www.nationsreportcard.gov/process_data/]
- researchers must `apply for a restricted-use license` to access the dataset [SOURCE: https://www.nationsreportcard.gov/process_data/]

### Operational read

Again, this is a real restricted-use gate, not a missing download script. [INFERENCE]

### Next step if we want it

1. decide whether formal `NAEP` process access is worth the licensing overhead
2. if yes, pursue restricted-use access
3. if no, treat current `PISA` / `TIMSS` local process work as the public-use ceiling

## 4. `HS&B`

### Official live path

- `HS&B` data access page: [SOURCE: https://nces.ed.gov/surveys/hsb/accessingData.asp]

### What the official docs say

- public-use microdata are available through the `Online Codebook`
- restricted-use data are separately available [SOURCE: https://nces.ed.gov/surveys/hsb/accessingData.asp]

### Current local blocker

- the current `Online Codebook` file endpoint in our acquisition path returns `HTTP 500` [SOURCE: `research/iq-sex-differences-nces-datalab-acquisition.md`; `sources/iq-sex-diff/data/hsb/hsb_onlinecodebook_probe.txt`]

### Operational read

This one is still worth retrying because it looks like a broken endpoint rather than a conceptual access wall. [INFERENCE]

## 5. `SECCYD` (ICPSR 21940)

### Official live path

- study page: [SOURCE: https://www.icpsr.umich.edu/web/DSDR/studies/21940]

### What the official docs say

- SECCYD Phase I is "freely available" at ICPSR for registered users [SOURCE: https://www.icpsr.umich.edu/web/DSDR/studies/21940]

### What we got locally

- study-level download returned codebook-only zip (docs, questionnaires, measures chart — no `.sav` or `.dat` files)
- codebook zip stored at `sources/iq-sex-diff/data/seccyd/codebooks/ICPSR_21940-V6.zip`

### Operational read

Same as HS&B — ICPSR "freely available" studies return codebooks without data files for individual (non-institutional) accounts. [INFERENCE]

## 6. ICPSR Download Architecture (discovered 2026-03-06)

### Key finding

ICPSR study-level downloads (`/download/spss`) **always** return codebook-only zips for individual accounts. Per-dataset downloads (`/datasets/{n}/download/ascspss`) also returned codebooks or errors. This applies even when:
- logged in with a registered individual account
- terms of use accepted (via React modal on datadocumentation page)
- download triggered through authenticated Chrome session

### Probable cause

ICPSR membership tiers: individual accounts get codebooks; data files require institutional membership or specific dataset-level authorization. "Freely available" means "free for members of ICPSR member institutions." [INFERENCE]

### What was tried (and failed)

1. **browser_cookie3** — extracts Chrome cookies but ICPSR uses server-side sessions; cookies don't carry login state
2. **Browserbase cloud browser** — Google SSO blocked by Google (automated cloud login detection)
3. **Chrome CDP** (`--remote-debugging-port=9222`) — macOS App Sandbox prevents port from opening
4. **Playwright persistent context** — copied Chrome profile but session state didn't transfer
5. **Direct fetch with cookies** — 403 on API v2 endpoints
6. **Chrome extension (claude-in-chrome)** — successfully navigated and triggered downloads, but all returned codebook-only zips

### What works

The only approach that reached ICPSR's authenticated download flow was `mcp__claude-in-chrome__*` (navigating the user's live Chrome session). But the downloaded content was still codebooks-only.

### Next step

Either obtain institutional ICPSR membership, or find alternative public sources for HSB and SECCYD data.

## Decision Table

| Dataset | Exact state | What blocks us now | Best next move |
| --- | --- | --- | --- |
| `PSID CDS/TAS` | public-use bundles are local and parsed | no live acquisition blocker | analysis interpretation |
| `Add Health` public-use | 169 MB downloaded (waves 1-6) from UNC Dataverse | no live blocker | build extract |
| `HSTS` transcript microdata | real dataset, real transcript leverage | NCES restricted-use license | licensing decision |
| `NAEP` process data | real dataset, strongest U.S. process target | NCES restricted-use license | licensing decision |
| `HS&B` public-use | codebooks downloaded, no data files | ICPSR institutional membership | obtain membership or find alt source |
| `SECCYD` Phase I | codebooks downloaded, no data files | ICPSR institutional membership | obtain membership or find alt source |
| `Fragile Families` | not attempted | Princeton OPR registration | register at oprdata.princeton.edu |

## Bottom Line (updated 2026-03-06)

**Local and ready for analysis:**
- `PSID CDS/TAS` — child panel + transition panel built
- `Add Health` public-use — 169 MB, waves 1-6 (UNC Dataverse)
- `NLSY79`, `NLSY97` — ASVAB, PIAT, transcript, behavior extracts built
- `ECLS-K`, `ECLS-K:2011` — early school extracts built
- `NELS`, `ELS`, `HSLS` — wedge first passes built
- `PISA 2018`, `TIMSS`, `PIAAC` — DIF, cognitive, age-stratified passes built
- `ICAR` — decomposition pass built

**Blocked by ICPSR institutional membership:**
- `HS&B` (4 studies) — codebooks only
- `SECCYD` Phase I — codebooks only

**Blocked by restricted-use licensing:**
- `HSTS` transcript microdata — NCES restricted-use
- `NAEP` process data — NCES restricted-use

**Blocked by registration:**
- `Fragile Families` — Princeton OPR (oprdata.princeton.edu)
- `ABCD` — NDA registration

The analytic stack is substantial. ICPSR data requires institutional membership, not more scripting. [INFERENCE]
