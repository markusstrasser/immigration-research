# 2026-06-11: OHSS parser carried two data bugs — CHNV "no substitution" claim reversed, Title-42 timing evidence rewritten, receiver-swing claim survives its kill-test

## Context

The morning bias self-audit (Cato mirror test) left two pre-registered kill-tests open: a Hispanic-share control for the receiver-city GOP-swing claim (ladder 28/31) and a pre-trend event study for the CHNV claim (ladder 26/30). Running them against the local data exposed two upstream bugs in `scripts/parse_ohss_enforcement.py` (immigration-causal, offload volume), which had built the surge analysis's flagship encounter series:

1. **Date bug.** `MONTHS` mapped month names to fiscal indexes (October=1 … September=12), so every `date` was a fiscal index dressed as a calendar month: true Oct-Dec of year Y landed on parquet Jan-Mar of Y; true Jan-Sep shifted +3 months. January-1 cuts survived the within-year permutation (the CHNV DiD's post dummy was accidentally correct); every non-January window — the Title-42 pre/post means, the memo's month narrative, event-time offsets — was scrambled.
2. **Universe bug.** The source sheet ("CBP SW Border Encounters **by Agency** and Selected Citizenship") has three horizontal blocks — Total CBP, USBP, OFO — with identical column names. The parser dict-keyed on column names, so each was silently overwritten by the rightmost block: the parquet was **OFO (port-of-entry) encounters only**, ~5x below total, while every consumer read it as total SWB encounters. The OFO series at ports is dominated by CBP One appointments and parole presentations — i.e., the CHNV program's own lawful channel.

## Decision

1. **Reverse ladder entry 26** ("CHNV parole did not substitute legal flow for illegal flow; it added on top", graded strong). On the corrected USBP (between-ports) universe, with staggered treatment dates (Venezuela 2022-10; Cuba/Haiti/Nicaragua 2023-01) and flat pre-trends: between-port crossings collapsed −95.3% (Cuba), −96.2% (Nicaragua), −57.5% (Venezuela, initial; decays by τ+11 with the Darién rebound); Haiti was never a between-ports population (~150/mo, flat — Haitians used ports). Event-study mean τ[0,+3] = −2.17 log points, sustained ≈ −1.8 through τ[+6,+12]. The original "+787% rise" measured the program's own lawful throughput (OFO) on a scrambled clock. Corrected total-CBP DiD: β=+0.45, t=1.29 — null. The defensible corrected claim: **CHNV substituted lawful port flow for irregular crossings in its initial year (strongest for Cuba/Nicaragua), while total cross-border presentations from those nationalities stayed roughly flat against falling controls and ~530K paroles entered as planned lawful inflow.** Receiver-load implications are a separate ledger: lawful arrivals still land in cities.
2. **Rewrite entry 25's evidence** (Title-42 timing). The specific facts ("peaked Jan-Mar 2023 at 50K+ before the lift", "April-May lull") were artifacts. Corrected series: Dec-2022 local peak 252K → Jan-Feb 2023 trough ~157K (the CHNV substitution visible at the total level) → **anticipation spike April-May 2023 (212K/207K) → post-lift crash June 2023 (145K, −30%) → autumn rebuild → all-time record Dec 2023 (301,980)**. The entry's conclusion (the lift did not cause the surge) survives on different evidence: post-lift 6-month mean was −14.5% below pre-lift.
3. **Restore entry 28/31's receiver-swing claim to medium-survives.** The pre-registered Hispanic-share kill-test (popest 2020 baseline) left the receiver coefficient essentially unchanged (+0.0256 → +0.0238, t≈7.2) while Hispanic share itself entered huge (β=+0.062, t=17.2); within the top-Hispanic quintile, receivers out-swung comparable counties by +4.3pp raw. The morning's retraction of the "implausibly large" *assertion* stands — but the decomposition it demanded now exists and the effect survives it.
4. **Parser fixed, parquets rebuilt, universes split** (`Total CBP` under the legacy filename; new `*_agency_monthly` long format and `swb_usbp_top100_monthly` with Nicaragua). All external anchors verified post-fix: Total CBP Dec 2023 = 301,980 ≈ known record; Venezuela Oct 2022 = 22,060 → collapse after the Oct-12 expulsion deal; CHNV paroles start Oct 2022 Venezuela-only, pause Aug 2024.

## Evidence

- `sources/immigration-causal/scripts/parse_ohss_enforcement.py` (fix + bug notes inline)
- `sources/immigration-causal/scripts/analyze_chnv_pretrends.py` + `data/outcomes/analysis/chnv_pretrends/results.json` (pre-registered rules and verdict)
- `sources/immigration-causal/scripts/analyze_swing_hispanic_control.py` + `data/outcomes/analysis/swing_hispanic_control/results.json` (replication gate passed; verdict "softens back")
- Rerun of `scripts/analyze_surge_title42_chnv.py` on corrected data (β=+0.45 t=1.29; corrected monthly series)
- External anchors: CBP/OHSS published totals (Dec 2023 record ≈ 302K; Venezuela Oct 2022 ≈ 22K). Scripts/data live on the offload volume (gitignored); this record is the canonical in-repo trace.

## Method note (why this was found today)

Both kill-tests were pre-registered with decision rules before results (quant-bias checklist item 23); the event study's per-nationality table then failed an external-anchor sanity check (Venezuela 605→28→7,941 made no calendar sense), which forced the date audit, which exposed the universe bug. The morning audit had downgraded entry 26 for reverse-causation risk — right to distrust it, wrong about why. Checklist addition candidate: **external-anchor check on any series before regression** (one known published value per series).

## Revisit if

- OHSS revises the Nov-2024 enforcement tables (data vintage pinned in `MANIFEST.md`).
- A USBP-universe analysis of the post-June-2024 enforcement regime changes the long-run substitution picture.
- County Hispanic-vote-share data (not just population share) becomes available locally — population share is the rival-channel proxy, not the vote itself.

## Supersedes

- Ladder entry 26 (2026-04-18 surge layer) and the morning's entry 30 downgrade (2026-06-11) — both superseded by the reversal.
- Entry 25's evidentiary text (conclusion retained).
- Surge memo §key-findings 2 and the monthly narrative (see memo Revisions 2026-06-11b).
