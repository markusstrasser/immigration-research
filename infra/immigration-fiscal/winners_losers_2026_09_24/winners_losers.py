"""Who wins and who loses from the Mexican-origin union's presence, person by person, over every
priced channel (brief: BRIEF.md, 2026-09-24).

Frame: the complete annual account's stationary 2024 comparison with and without the 40.896574m
CPS Mexican-origin residents; effects on the 295.83m other residents of CPS ASEC 2025, a dollar
counted as a dollar. Each channel's total is read from its lane's derived files; this script only
divides totals among persons, and never re-estimates one.

Cases (--case, CASES): the adopted main case the run allocates, and the case before it, which the run
keeps as the positive control of its federal split and regression. The default, sept27, is the main
case adopted on 2026-09-27 (ladder 239: the return on public capital, long-run road and park responses,
rental assistance at 1 and every government enterprise), after sept26_schools (schools at full average
cost; ladder 230) and sept26 (the one-year scenario; ladder 229). sept24 (ladder 219) rebuilds the files
this lane committed on the September 24 case byte for byte, and each later case the files of its own
run. Every case writes to derived/ unless --out-dir is given; derived/ holds the default case. The
consumption key's proposal row is sept24's only, since the later cases carry the key inside the fiscal
channel. Under a school response of 1 the school dilution rows stay in the role table
(decisions/2026-09-26-main-case-schools-full-cost.md): nothing is left unfunded.

From September 27 (CASES capped, congestion, preferences):
 - The fiscal channel keeps three financing columns apart (the debt lane's split, one definition per
   column): cash financing, the resource cost (the return on public capital, enterprise capital included,
   an imputed cost that is never borrowed, so none of it goes to future taxpayers) and the displaced
   beneficiaries of the capped programs. fiscal_<conv> is cash financed today plus the resource cost, and
   fiscal_cash_<conv> and fiscal_resource_<conv> split it. The enterprise surplus receipt is a cash line.
 - Rental assistance and LIHEAP are capped and rationed, so without the group eligible households take
   their slots: displaced_beneficiaries falls on eligible non-recipients under both conventions, keyed by
   the distribution lane's capped_keys() (renter households below 50% of the state median income outside
   public or subsidized housing, 24 CFR 5.603 and 982.201(b); households below 150% of the HHS 2024
   poverty guideline without energy assistance, 42 U.S.C. 8624(b)(2)(B), 89 FR 2961). It is in the account
   net. TANF-type aid is a block grant and stays in the fiscal channel.
 - Congestion is the long-run lane's re-derivation (roads now respond, so lanes shrink with the group),
   split by state from that lane's own per-area arm.
 - The preferences row is an attribution under a stated replacement rule, with the other included
   recipients' part carried and the DBE premium reconciled against the fiscal allocation (adversarial
   audit 2026-09-28 section 3).

From September 29 (--case sept29, the main case adopted that day, ladder 275; CASES production, accrual and the
upstream directories), written to derived/sept29/ beside the default files, which stay September 27's:
 - Production is on the account's row-4 weights: the case's wages and F come from the base lane's row-4 re-solve
   (row4_nest_rows, gated there against the case's grid), while the case before it keeps the published rows.
 - The pension switch's accrual is a fourth financing part (the debt lane's accrual_bn, all federal). Nothing
   finances it in 2024: it is the group's claim on benefits paid later, so it joins the future taxpayers' part and
   leaves the cash part; future_pension_accrual reports it, and the future taxpayers' row shows the borrowed part.
 - Public housing's enterprise deficit is capped like rental assistance, on rental assistance's key (the base's
   CAPPED_KEY_OF), inside displaced_beneficiaries.
 - Each upstream lane keeps the case's files in its own place (base_dir, debt_dir, gen_results), read at their
   pinned commits; a pin that is None stops the run (--dev-unpinned: a dry run reads the working tree instead and
   writes outside derived/ only).
 - The group's own rows are on the account's count (CASES group_weights "row4", 39.71m: row4_group_weights), with
   the CPS's published 40.9m beside them in group_frame_cps_published.csv, and the counterfactual label names 39.7m.
   The other residents are the same persons on the same weights in both frames.

From October 5 (--case oct05, main case v5, ladder 281: the September 29 case plus 3.04m descendants who no longer
report Mexican origin, counted whole, a lineage of 42.75m), written to derived/oct05/:
 - The case before (September 29) has a production grid of its own, so both cases read their row-4 scenarios
   (production_rows); the case's grid is September 29's plus the added members' P and F, which the base lane's
   lineage_rows adds to the same re-solve.
 - The group's own rows are on the lineage (CASES group_weights "lineage": lineage_group_weights). The added people are
   not in the CPS as group members, so each identified third-plus-generation member's row-4 weight is raised by
   added / identified G3+ (LINEAGE_RULE) [ASSUMPTION]. The other residents keep the CPS frame, in which the added people
   sit unfound among them, as the distribution lane leaves them; the group's geography (where its state-local cost,
   victims' harm and uncompensated care arise) stays on the identified members' published weights, as in every case.

From October 7 (--case oct07, main case v6: v5 plus the items in its payload's meta.items), written to derived/oct07/:
 - Both cases re-solve September 29's grid with their own added people (the base lane's LATER_CASES), so the gate that
   ties the case's production rows to the case before's compares the two additions' base.
 - The case prices the added people at their measured ages (meta.lineage.age_mix), so the group's frame raises each
   identified G3+ record by the added people of its five-year age band (age_band_factors, LINEAGE_AGE_RULE)
   [ASSUMPTION: all of them take the G3+ members' records, band by band]; the counts are v5's.
 - The items' other effects reach this lane through its upstream files: the engine run (specs.cjs, the whole payload),
   the distribution lane's A, the debt lane's split and accrual, and the generation split.

Base: distribution_weights_2026_09_23 (ladder 194). Its code is loaded from git at the case's base
commit, the commit that moved it to that case, so later edits to its working tree cannot change this
lane. Its fiscal_totals(case) is the one definition of the case's direct response A that both lanes
use. Two regression targets: its channel_by_quintile.csv at the previous case's base commit and at the
case's.

One definition per shared number, read from the lane that owns it: the federal part of the fiscal
cost and the debt legacy interest from debt_legacy_2026_09_23 at the case's debt commit (its files at
the previous case's debt commit are the method's positive control); victims' harm only as a lane
computed it (decision 4's $30.93bn central); housing as ladder 190 publishes it.

Steps (BRIEF.md numbering):
 1. Channel registry: derived/channels.csv. The adopted fiscal case comes from specs.cjs
    (derived/fiscal_specs.csv): per specification, fiscal = A + F and wages = P, and the gate checks
    that the CPS person-level wages plus A + F equal the adopted cost in all 64 specifications. The
    frame's fiscal channel takes A at the band ends from the base lane's fiscal_totals(case), which
    differs from the engine run by rounding (< 1e-4bn, recorded in gates.json).
 2. Person frame: _cache/person_frame.parquet (ignored); every other resident's dollars in every
    allocated channel at low, central and high. Gate: persons sum to each channel's total.
 3. Key templates for the sister lanes (key_templates.csv), and ingestion of any
    ../<lane>_2026_09_24/derived/winners_losers_rows.csv present at run time. A row enters a net
    only on the account's counterfactual, the group's (or its pupils') absence; the others are listed
    under their own counterfactual in derived/sister_other_counterfactuals.csv (gated).
 4. Cuts: derived/cuts.csv and derived/cut_summary.csv. Gate: every cut sums to the frame.
 5. Net winners and losers under (a) tax-share and (b) per-person financing; the federal
    deficit-financed part is the future taxpayers' row and is not allocated.
 6. The group itself: derived/group_frame.csv.
 7. The page: derived/winners_losers_table.csv and derived/person_nets_by_cut.csv.

Sister-lane rows map to key templates through an explicit `key` column or the patterns in key_map.csv;
test_winners_losers.py holds the ingestion's positive controls on a synthetic frame.

Run from the repository root (specs.cjs first, with the same --case and --out-dir):
  node infra/immigration-fiscal/winners_losers_2026_09_24/specs.cjs [--case sept26_schools --out-dir DIR]
  OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/winners_losers_2026_09_24/winners_losers.py [--case sept26_schools --out-dir DIR]
  OPENBLAS_NUM_THREADS=1 uv run --no-project python3 -m pytest infra/immigration-fiscal/winners_losers_2026_09_24/ -q
"""
from __future__ import annotations

import argparse
import contextlib
import hashlib
import importlib.util
import io
import json
import re
import subprocess
import types
import warnings
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd

warnings.filterwarnings("ignore", message="Workbook contains no default style")

HERE = Path(__file__).resolve().parent
FISCAL = HERE.parent
ROOT = HERE.parents[2]
DERIVED = HERE / "derived"
CACHE = HERE / "_cache"
SOURCES = CACHE / "sources"

BASE_COMMIT = "7ec7144"     # distribute.py and channel_by_quintile.csv on the September 24 case
SEPT23_COMMIT = "5b8957e"   # channel_by_quintile.csv on the September 23 case
BASE_REL = "infra/immigration-fiscal/distribution_weights_2026_09_23"
# The debt legacy lane's per-line federal fractions, federal split and interest: September 23 at
# DEBT_COMMIT (positive control), September 24 at DEBT24_COMMIT (used).
DEBT_COMMIT = "b42efdc"
DEBT24_COMMIT = "7ec7144"
# The debt lane's per-correction file on the September 24 case was untracked at DEBT24_COMMIT and
# committed in ed1b623 (the files 7ec7144 left out); since e62fccb its working tree holds a later case.
DEBT24_FILES_COMMIT = "ed1b623"
GEN24_COMMIT = "ba12f3c"    # generation_results.csv on the September 24 case (a later case since 2441ac8)
# The later cases' pins (parent, 2026-09-26). Distribution: the September 26 case at BASE26_COMMIT and
# the schools case at BASE26S_COMMIT, whose fiscal_totals serves both. Debt legacy: the same two cases,
# each commit with its per-correction file. Generation: generation_results.csv on the schools case, and
# generation_summary.json, whose change_from_sept26 holds the September 26 case's split.
BASE26_COMMIT = "f697514"
BASE26S_COMMIT = "39b854b"
DEBT26_COMMIT = "e62fccb"
DEBT26S_COMMIT = "1db19c8"
GEN26S_COMMIT = "0f22f0c"
# The September 27 case's pins (parent, 2026-09-28). Distribution: channel_by_quintile.csv, inputs.json with
# its financing columns and case_ends_sept27.json. Debt legacy: stocks.csv and summary.json (case.band includes
# the capital return; case.main_profile is long_run_non_school_full) with the per-correction files. Generation:
# generation_results.csv and generation_summary.json on the case. The back-cast (de468f2) is not read here.
# b3f4d84 (2026-09-29) differs from 78766c2 in this lane only by case_ends_sept27.json's bands hash: the bands file
# gained the general_government_fixed row beside the range.
BASE27_COMMIT = "b3f4d84"
DEBT27_COMMIT = "e03450b"
GEN27_COMMIT = "8654a0c"
# The September 29 case (candidate v4, adopted 2026-09-29), in one place: its lane and the commits that hold its
# upstream files, each in its lane's own place for the case. Distribution: derived/sept29/ (channel_by_quintile.csv,
# inputs.json) and derived/case_ends_sept29.json. Debt legacy: derived/sept29/. Generation:
# derived/generation_results_sept29.csv. Propagation: SEPT29_PUBLISHED. A pin that is None stops the case
# ([BLOCKED] in configure) until the upstream commit exists, as do the debt lane's interest and the ladder entry.
SEPT29_LANE = "main_case_2026_09_29"
BASE29_COMMIT = "492bf32"
DEBT29_COMMIT = "7e1b500"
GEN29_COMMIT = "aa1f53b"
SEPT29_INTEREST = (30.7514, 41.4794)    # the debt lane's legacy interest at the main benchmark (low, high), from its stocks.csv
SEPT29_LADDER = "275"     # the adopted case's own entry (d40e085), as "239" is September 27's
SEPT29_PUBLISHED = "sept24_propagation_2026_09_24/derived/sept29"
# The October 5 case (main case v5, adopted 2026-10-05, ladder 281: the September 29 case plus the 3.04M descendants
# of Mexican immigrants who no longer report Mexican origin, counted whole). Distribution: derived/oct05/ and
# derived/case_ends_oct05.json at fecaae7e. Debt legacy: derived/oct05/ at 604b09e1. Generation:
# derived/generation_results_oct05.csv at e5ca5efe. Propagation: OCT05_PUBLISHED, read from the working tree as every
# case's is.
OCT05_LANE = "main_case_2026_10_05"
BASE05_COMMIT = "fecaae7e"
DEBT05_COMMIT = "604b09e1"
GEN05_COMMIT = "e5ca5efe"
OCT05_INTEREST = (30.6288, 42.6236)     # the debt lane's legacy interest at the main benchmark, its stocks.csv at 604b09e1
OCT05_LADDER = "281"
OCT05_PUBLISHED = "sept24_propagation_2026_09_24/derived/oct05"
# The October 7 case (main case v6, adopted 2026-10-07, ladder 295: v5 plus the items in its payload's meta.items).
# Distribution: derived/oct07/ and derived/case_ends_oct07.json at 498a6a71. Debt legacy: derived/oct07/ at 0485e5a2.
# Generation: derived/generation_results_oct07.csv at 3f583fb4. Propagation: OCT07_PUBLISHED, read from the working
# tree as every case's is.
OCT07_LANE = "main_case_2026_10_07"
BASE07_COMMIT = "498a6a71"
DEBT07_COMMIT = "0485e5a2"
GEN07_COMMIT = "3f583fb4"
OCT07_INTEREST = (31.8233, 44.1693)     # the debt lane's legacy interest at the main benchmark, its stocks.csv at 0485e5a2
OCT07_LADDER = "295"      # main case v6's own entry (parent, 2026-10-07)
OCT07_PUBLISHED = "sept24_propagation_2026_09_24/derived/oct07"
OLD_PROFILE = "cbo_category_lag_non_school_full"   # every case's main profile before September 27
DEBT_REL = "infra/immigration-fiscal/debt_legacy_2026_09_23/derived"
GEN_REL = "infra/immigration-fiscal/generation_account_2026_09_24/derived"
LEVELS = ("low", "central", "high")
CONVENTIONS = ("a", "b")
SISTERS = {  # lane directory -> registry id
    "school_dilution_2026_09_24": "school_dilution",
    "vending_restaurants_2026_09_24": "vending_restaurants",
    "compliance_gap_2026_09_24": "compliance_edge",
    "movers_reasons_2026_09_24": "movers",
}
# The sister lanes as the September 24 run read them (their rows and RESULT.md at these commits).
SISTER24_COMMITS = {"school_dilution_2026_09_24": "e4bdf40", "vending_restaurants_2026_09_24": "c98f479",
                    "compliance_gap_2026_09_24": "fa338b8", "movers_reasons_2026_09_24": "f9c9504"}
# The later runs read them at their commits of 2026-09-26: the same rows, later RESULT.md verdicts.
SISTER26_COMMITS = {"school_dilution_2026_09_24": "8936938", "vending_restaurants_2026_09_24": "1c9b6fe",
                    "compliance_gap_2026_09_24": "1d14b54", "movers_reasons_2026_09_24": "1c9b6fe"}
# Two lanes finished without rows: generation_account_2026_09_24 (ba12f3c), whose split of the
# account by generation enters the group frame (generation_split), and consumption_key_2026_09_24
# (6841b39), whose proposed key correction is a registry row (consumption_proposal) on the September 24
# case and inside the fiscal channel from September 26 on. Neither is in a net.
# A sister row enters a net only on the account's counterfactual, the group's (or its pupils')
# absence (parent ruling, 2026-09-25). The phrase must open the row's counterfactual; a qualifier
# that changes the comparison (enrollment held, spending that follows enrollment) disqualifies it.
ABSENCE = re.compile(r"^\s*(the\s+)?(mexican-origin\s+)?group(['’]s)?(\s+pupils)?\s+(are\s+)?absent\b"
                     r"|^\s*(without|in\s+the\s+absence\s+of)\s+the\s+(mexican-origin\s+)?group\b"
                     r"|^\s*the\s+group['’]s\s+absence\b", re.I)
NOT_ABSENCE = re.compile(r"enrollment held|not the account's counterfactual", re.I)
LANE_LABELS = {  # printed with a lane's allocated rows
    "school_dilution_2026_09_24": "present value of lifetime earnings, not annual cash; the relabel is "
                                  "proposed in decisions/2026-09-25-school-dilution-priced-beside.md",
}
SISTER_COLUMNS = ["group", "channel", "direction", "bn_low", "bn_central", "bn_high", "population_m",
                  "per_person_usd", "basis", "relation_to_account", "counterfactual", "source"]
# Cases. A runnable case names its engine model (the case column specs.cjs writes), its main-case lane,
# the case before it, and the pins of the lanes that have moved on since: base (distribution),
# debt and debt_files (debt legacy), gen (generation; gen_split names the generation_summary.json key
# that holds the case's split when generation_results.csv holds a later case), the sister commits and
# the debt lane's interest at the main benchmark (gated to 5e-4). published_dir holds the case's
# real-costs totals and band variants (ruling 5). sept23 is a previous case only. From September 27 a case
# also names its main profile and the variant of its lane's main_case_bands.csv that holds the case before it
# (profile, prev_variant; before, OLD_PROFILE and the previous model's name), and three switches: capped
# (the capped programs' displaced beneficiaries and the three financing columns), congestion ("long_run":
# the response lane's re-derived congestion) and preferences ("attribution": the preferences row under its
# stated replacement rule).
CASES = {
    "sept23": dict(model="adopted_2026_09_23", label="September 23 case (decision 4's figure)",
                   base=SEPT23_COMMIT, debt=DEBT_COMMIT, interest=(30.4759, 38.8646)),
    "sept24": dict(model="adopted_2026_09_24", label="September 24 case", prev="sept23",
                   lane="main_case_2026_09_24", ladder="219", date="2026-09-24", base=BASE_COMMIT,
                   debt=DEBT24_COMMIT, debt_files=DEBT24_FILES_COMMIT, gen=GEN24_COMMIT, gen_split=None,
                   sisters=SISTER24_COMMITS, interest=(28.3387, 36.4297), consumption_proposal=True,
                   published="sept24_propagation_2026_09_24", published_dir="sept24_propagation_2026_09_24/derived"),
    "sept26": dict(model="adopted_2026_09_26", label="September 26 case, the one-year scenario", prev="sept24",
                   lane="main_case_2026_09_26", ladder="229", date="2026-09-26", base=BASE26_COMMIT,
                   debt=DEBT26_COMMIT, debt_files=DEBT26_COMMIT, gen=GEN26S_COMMIT, gen_split="change_from_sept26",
                   sisters=SISTER26_COMMITS, interest=(28.2483, 36.3485), consumption_proposal=False,
                   published="sept26_propagation_2026_09_26 (derived/sept26)",
                   published_dir="sept26_propagation_2026_09_26/derived/sept26"),
    "sept26_schools": dict(model="adopted_2026_09_26_schools", label="schools case of September 26", prev="sept26",
                           lane="main_case_schools_full_2026_09_26", ladder="230", date="2026-09-26",
                           base=BASE26S_COMMIT, debt=DEBT26S_COMMIT, debt_files=DEBT26S_COMMIT, gen=GEN26S_COMMIT,
                           gen_split=None, sisters=SISTER26_COMMITS, interest=(30.1448, 37.8726),
                           consumption_proposal=False, published="sept26_propagation_2026_09_26",
                           published_dir="sept26_propagation_2026_09_26/derived"),
    "sept27": dict(model="adopted_2026_09_27", label="September 27 case", prev="sept26_schools",
                   lane="main_case_long_run_2026_09_27", ladder="239", date="2026-09-27", base=BASE27_COMMIT,
                   debt=DEBT27_COMMIT, debt_files=DEBT27_COMMIT, gen=GEN27_COMMIT, gen_split=None,
                   sisters=SISTER26_COMMITS, interest=(30.9346, 41.6323), consumption_proposal=False,
                   published="sept27_propagation_2026_09_27", published_dir="sept27_propagation_2026_09_27/derived",
                   profile="long_run_non_school_full", prev_variant="schools_case", capped=True,
                   congestion="long_run", preferences="attribution"),
    # From September 29 a case may also name: production ("row4": its engine's production grid is on the account's
    # row-4 weights, so its wages and F are the distribution lane's row-4 re-solve, while the case before it keeps the
    # published ones), accrual (the pension switch's accrual, a fourth financing part), and where each upstream lane
    # keeps its files for the case (base_dir, debt_dir under their derived/; gen_results) and where this lane writes
    # them (out, under derived/), and the weights of the group's own frame (group_weights "row4": the account's
    # count, with the CPS's published 40.9m beside it; row4_group_weights).
    "sept29": dict(model="adopted_2026_09_29", label="September 29 case (candidate v4)", prev="sept27",
                   lane=SEPT29_LANE, ladder=SEPT29_LADDER, date="2026-09-29", base=BASE29_COMMIT, debt=DEBT29_COMMIT,
                   debt_files=DEBT29_COMMIT, gen=GEN29_COMMIT, gen_split=None, sisters=SISTER26_COMMITS,
                   interest=SEPT29_INTEREST, consumption_proposal=False, published=SEPT29_PUBLISHED,
                   published_dir=SEPT29_PUBLISHED, profile="long_run_non_school_full", prev_variant="sept27_case",
                   capped=True, congestion="long_run", preferences="attribution", production="row4", accrual=True,
                   base_dir="sept29", debt_dir="sept29", gen_results="generation_results_sept29.csv", out="sept29",
                   group_weights="row4"),
    # From October 5 the case before may have a production grid of its own (its own row-4 rows), and the case's grid
    # may add to another case's (the base lane's LATER_CASES grid_base: its lineage_rows); group_weights "lineage" puts
    # the added people into the group's own frame at the identified third-plus generation's records (lineage_group_weights).
    "oct05": dict(model="adopted_2026_10_05", label="October 5 case (main case v5)", prev="sept29",
                  lane=OCT05_LANE, ladder=OCT05_LADDER, date="2026-10-05", base=BASE05_COMMIT, debt=DEBT05_COMMIT,
                  debt_files=DEBT05_COMMIT, gen=GEN05_COMMIT, gen_split=None, sisters=SISTER26_COMMITS,
                  interest=OCT05_INTEREST, consumption_proposal=False, published=OCT05_PUBLISHED,
                  published_dir=OCT05_PUBLISHED, profile="long_run_non_school_full", prev_variant="sept29_case",
                  capped=True, congestion="long_run", preferences="attribution", production="row4", accrual=True,
                  base_dir="oct05", debt_dir="oct05", gen_results="generation_results_oct05.csv", out="oct05",
                  group_weights="lineage"),
    # From October 7 the case before re-solves a grid with added people too (production_rows' gate compares the two
    # additions' base), and where the case prices the added people at their measured ages the group frame adds them
    # band by band (lineage_group_weights, age_band_factors).
    "oct07": dict(model="adopted_2026_10_07", label="October 7 case (main case v6)", prev="oct05",
                  lane=OCT07_LANE, ladder=OCT07_LADDER, date="2026-10-07", base=BASE07_COMMIT, debt=DEBT07_COMMIT,
                  debt_files=DEBT07_COMMIT, gen=GEN07_COMMIT, gen_split=None, sisters=SISTER26_COMMITS,
                  interest=OCT07_INTEREST, consumption_proposal=False, published=OCT07_PUBLISHED,
                  published_dir=OCT07_PUBLISHED, profile="long_run_non_school_full", prev_variant="oct05_case",
                  capped=True, congestion="long_run", preferences="attribution", production="row4", accrual=True,
                  base_dir="oct07", debt_dir="oct07", gen_results="generation_results_oct07.csv", out="oct07",
                  group_weights="lineage"),
}
RUNNABLE = ("oct07", "oct05", "sept29", "sept27", "sept26_schools", "sept26", "sept24")
DEFAULT_CASE = "sept27"
CASE: dict = {}   # the run's case with its previous case under "prev" (configure)
# At a school response of 1 nothing is left unfunded, so the school dilution rows (priced at the
# account's former 0.63-0.66) stay in the role table (decisions/2026-09-26-main-case-schools-full-cost.md).
SCHOOL_DILUTION_ROLE_ONLY = ("applies to the lower-response scenarios only: at this case's school response of 1 no "
                             "school cost is left unfunded (decisions/2026-09-26-main-case-schools-full-cost.md, "
                             "bullet 'School dilution'); never in a net under this case")

FIPS = {1: "AL", 2: "AK", 4: "AZ", 5: "AR", 6: "CA", 8: "CO", 9: "CT", 10: "DE", 11: "DC", 12: "FL",
        13: "GA", 15: "HI", 16: "ID", 17: "IL", 18: "IN", 19: "IA", 20: "KS", 21: "KY", 22: "LA", 23: "ME",
        24: "MD", 25: "MA", 26: "MI", 27: "MN", 28: "MS", 29: "MO", 30: "MT", 31: "NE", 32: "NV", 33: "NH",
        34: "NJ", 35: "NM", 36: "NY", 37: "NC", 38: "ND", 39: "OH", 40: "OK", 41: "OR", 42: "PA", 44: "RI",
        45: "SC", 46: "SD", 47: "TN", 48: "TX", 49: "UT", 50: "VT", 51: "VA", 53: "WA", 54: "WV", 55: "WI",
        56: "WY"}
POSTAL = {v: k for k, v in FIPS.items()}
MEXICO_BIRTHPLACE = 303          # CPS PENATVTY code for Mexico
# CPS birthplace codes of US areas (the United States, American Samoa, Guam, the Northern Mariana Islands, Puerto Rico,
# the US Virgin Islands): the generation account's third-plus generation has both parents born in them
# (generation_account_2026_09_24/frame.py masks).
US_AREAS = (57, 60, 66, 69, 73, 78)

# Clemens, Montenegro & Pritchett, "The Place Premium: Wage Differences for Identical Workers Across
# the US Border", HKS RWP09-004 (January 2009), corpus doi_10_2139_ssrn_1211427. Table 1 col. 6,
# Mexico: Ro 2.53 (95% CI 2.42, 2.65). Section 3.3: "the average emigrant comes from the 56th
# percentile of residual wages, suggesting that Ro/Re = 1.03 (with a 95% confidence interval of
# (0.96, 1.12)), so that Re ~ 2.46". Table 8, Mexico: Re 2.79 if the median migrant sits at the
# origin's 50th percentile, 2.08 at the 70th ("stronger than any of the evidence from any country
# above supports"). Low = 2.08, central = 2.46, high = 2.79.
PLACE_PREMIUM_RE = {"low": 2.08, "central": 2.46, "high": 2.79}

PATHS = dict(   # specs, lines, bands, real_costs and band_variants are the case's (configure)
    specs=None,
    lines=None,
    bands=None,
    omb_receipts=ROOT / "sources/immigration-fiscal/data/external/omb_hist_fy2027/hist02z1_fy2027.xlsx",
    omb_outlays=ROOT / "sources/immigration-fiscal/data/external/omb_hist_fy2027/hist03z1_fy2027.xlsx",
    crime_dollar=FISCAL / "crime_ratio_direction_2026_09_24/derived/dollar_effects.csv",
    nibrs_cost=FISCAL / "offender_ethnicity_nibrs_2026_09_23/derived/cost_arms.csv",
    congestion_arms=FISCAL / "congestion_2026_09_23/derived/arms_summary.csv",
    congestion_metro=FISCAL / "congestion_2026_09_23/derived/metro_distribution.csv",
    congestion_ua=FISCAL / "congestion_2026_09_23/derived/ua_exposure.csv",
    care=FISCAL / "care_household_services_2026_09_23/derived/summary.csv",
    preferences=FISCAL / "affirmative_action_cost_2026_09_24/derived/channels.csv",
    preferences_log=FISCAL / "affirmative_action_cost_2026_09_24/derived/calc_output.txt",
    scale=FISCAL / "scale_spillovers_2026_09_23/derived/summary.csv",
    scale_metro=FISCAL / "scale_spillovers_2026_09_23/derived/metro_distribution.csv",
    mobility=FISCAL / "labor_mobility_insurance_2026_09_23/derived/insurance_summary.json",
    housing_grid=FISCAL / "housing_transfer_2026_09_23/derived/arms_grid.csv",
    generations=FISCAL / "generation_account_2026_09_24/derived/generation_results.csv",
    consumption=FISCAL / "consumption_key_2026_09_24/derived/engine_summary.json",
    housing_headline=FISCAL / "housing_transfer_2026_09_23/derived/arms_headline.csv",
    real_costs=None,
    band_variants=None,
    remittance_flows=FISCAL / "consumption_key_2026_09_24/derived/remittance_flows.csv",
    # The consumption lane's ignored cache: Banxico SIE table CE167, the primary file behind its corridor.
    banxico_ce167=FISCAL / "consumption_key_2026_09_24/_cache/sources/corridor/banxico_CE167_2022_2025.xlsx",
    # Read for a consistency check only.
    debt_corrections=FISCAL / "debt_legacy_2026_09_23/derived/corrections_federal_by_component_2024.csv",
    census_industry=SOURCES / "census_industry_2022_crosswalk.xlsx",
)
# Inputs only some cases read (configure adds them, so an earlier case's sources_manifest.csv keeps its rows):
# the response lane's net_change.json (its re-derived congestion, and the highway response and key share by
# band end) and the per-area arm in its congestion.py; the preferences lane's code and IPEDS tiers for the
# attribution's replacement rule.
CASE_PATHS = dict(
    long_run_net_change=FISCAL / "service_response_long_run_2026_09_27/derived/net_change.json",
    long_run_congestion_code=FISCAL / "service_response_long_run_2026_09_27/congestion.py",
    preferences_code=FISCAL / "affirmative_action_cost_2026_09_24/calc.py",
    preferences_tiers=FISCAL / "affirmative_action_cost_2026_09_24/derived/ipeds_tiers.csv",
)
# PATHS inputs read from git at the case's pinned commit, not from the working tree, because their lanes
# have moved to later cases. sources_manifest.csv lists each at its PATHS position with the blob's sha256.
PINNED: dict = {}
CENSUS_INDUSTRY_URL = ("https://www2.census.gov/programs-surveys/demo/guidance/industry-occupation/"
                       "2022-Census-Industry-Code-List-with-Crosswalk.xlsx")
GATES: dict[str, dict] = {}


def gate(name, ok, **detail):
    GATES[name] = dict(passed=bool(ok), **{k: (float(v) if isinstance(v, (np.floating, np.integer)) else v)
                                         for k, v in detail.items()})
    if not ok:
        raise SystemExit(f"[BLOCKED] gate {name} failed: {detail}")


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def file_sha(path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for block in iter(lambda: fh.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


# --dev-unpinned (dry runs only): a case's missing commit pins read the working tree instead of git, and a missing
# interest pin is read from the working tree's stocks.csv without its gate. It needs an --out-dir outside derived/,
# so a dry run never writes the lane's outputs.
WORKTREE = "WORKTREE"
DEV: dict = {"unpinned": []}


def configure(case: str, out_dir: Path | None = None, dev_unpinned: bool = False) -> dict:
    """Point the run at a case: its engine runs (specs.cjs) and outputs in out_dir (default derived/),
    its main-case bands and real-costs totals, and its pinned inputs."""
    global DERIVED
    c = CASES[case]
    missing = [k for k in ("base", "debt", "debt_files", "gen", "interest", "ladder") if k in c and c[k] is None]
    DEV["unpinned"] = []
    if missing and not dev_unpinned:
        raise SystemExit(f"[BLOCKED] {case}: {', '.join(missing)} not set in CASES; its upstream files are not committed")
    if dev_unpinned:
        if out_dir is None or Path(out_dir).resolve().is_relative_to(HERE / "derived"):
            raise SystemExit("[BLOCKED] --dev-unpinned writes outside derived/ only: pass --out-dir <scratch directory>")
        if "ladder" in missing:
            raise SystemExit(f"[BLOCKED] {case}: no ladder entry")
        CASES[case] = c = dict(c, **{k: WORKTREE for k in missing if k != "interest"})
        DEV["unpinned"] = missing
        print(f"[DEV] {case}: unpinned {', '.join(missing) or 'nothing'}, read from the working tree; outputs in "
              f"{Path(out_dir).resolve()}")
    CASE.clear()
    CASE.update(c, case=case, prev=dict(CASES[c["prev"]], case=c["prev"]))
    DERIVED = Path(out_dir).resolve() if out_dir else HERE / "derived" / c.get("out", "")
    PATHS.update(specs=DERIVED / "fiscal_specs.csv", lines=DERIVED / "fiscal_lines_band_ends.csv",
                 bands=FISCAL / c["lane"] / "derived/main_case_bands.csv",
                 real_costs=FISCAL / c["published_dir"] / "real_costs_totals.csv",
                 band_variants=FISCAL / c["published_dir"] / "band_variants.csv",
                 generations=FISCAL / "generation_account_2026_09_24/derived" / c.get("gen_results", "generation_results.csv"),
                 debt_corrections=FISCAL / "debt_legacy_2026_09_23/derived" / c.get("debt_dir", "")
                 / "corrections_federal_by_component_2024.csv")
    for k in CASE_PATHS:
        PATHS.pop(k, None)
    if c.get("congestion") == "long_run":
        PATHS.update({k: CASE_PATHS[k] for k in ("long_run_net_change", "long_run_congestion_code")})
    if c.get("preferences") == "attribution":
        PATHS.update({k: CASE_PATHS[k] for k in ("long_run_net_change", "preferences_code", "preferences_tiers")})
    PINNED.clear()
    PINNED.update(generations=c["gen"], debt_corrections=c["debt_files"])
    return CASE


def git_show(rel: str, commit: str | None = None) -> bytes:
    """A file at a commit; the case's base commit by default (WORKTREE: the working tree, --dev-unpinned only)."""
    if (commit or CASE["base"]) == WORKTREE:
        return (ROOT / rel).read_bytes()
    return subprocess.run(["git", "-C", str(ROOT), "show", f"{commit or CASE['base']}:{rel}"],
                          check=True, capture_output=True).stdout


def read_input(key: str) -> bytes:
    """A PATHS input's bytes: from git at its PINNED commit, else from the working tree."""
    p = PATHS[key]
    return git_show(str(p.relative_to(ROOT)), PINNED[key]) if key in PINNED else p.read_bytes()


def lane_rel(rel: str, sub: str | None, name: str) -> str:
    """A lane file's path: rel/name, or rel/sub/name for a case that keeps its files in a directory of its own."""
    return f"{rel}/{sub}/{name}" if sub else f"{rel}/{name}"


def debt_csv(name: str, commit: str, sub: str | None = None) -> pd.DataFrame:
    return pd.read_csv(io.BytesIO(git_show(lane_rel(DEBT_REL, sub, name), commit)))


def debt_json(name: str, commit: str, sub: str | None = None) -> dict:
    return json.loads(git_show(lane_rel(DEBT_REL, sub, name), commit))


def write_csv(df: pd.DataFrame, name: str):
    df.to_csv(DERIVED / name, index=False, lineterminator="\n", float_format="%.10g")


# ================================================================== base lane, pinned at the case's commit
def load_base():
    """distribute.py at the case's base commit as a module. __file__ points at the base lane, so its caches
    (ACS extract, cached documents) are read from there; nothing here calls its main() or writes."""
    src = git_show(f"{BASE_REL}/distribute.py")
    mod = types.ModuleType("base_distribute")
    mod.__file__ = str(ROOT / BASE_REL / "distribute.py")
    exec(compile(src.decode(), mod.__file__, "exec"), mod.__dict__)
    return mod, sha(src)


# ================================================================== CPS frame
def load_frame(B):
    d = B.load_cps()
    extra_p = ["PH_SEQ", "PPPOS", "A_SEX", "INDUSTRY", "WORKYN", "WKSWORK", "HRSWK", "SEMP_VAL", "FRSE_VAL",
               "MIG_ST", "MIGSAME", "NOCOV_CYR", "PERRP", "A_CLSWKR"]
    extra_h = ["H_SEQ", "GESTFIPS", "H_TENURE", "HRNTVAL", "GTMETSTA"]
    with zipfile.ZipFile(B.PATHS["cps"]) as z:
        p = pd.read_csv(z.open("pppub25.csv"), usecols=extra_p)
        h = pd.read_csv(z.open("hhpub25.csv"), usecols=extra_h).rename(columns={"H_SEQ": "PH_SEQ"})
    gate("cps_extra_columns_aligned", np.array_equal(p.PH_SEQ.to_numpy(), d.PH_SEQ.to_numpy())
         and np.array_equal(p.PPPOS.to_numpy(), d.PPPOS.to_numpy()), records=len(d))
    for c in extra_p[2:]:
        d[c] = p[c].to_numpy()
    hh = h.set_index("PH_SEQ")
    for c in extra_h[1:]:
        d[c] = d.PH_SEQ.map(hh[c]).to_numpy()
    if d[extra_h[1:]].isna().any().any():
        raise SystemExit("[BLOCKED] CPS person without household geography or tenure")
    other, target = d.other.to_numpy(), d.target.to_numpy()
    d["st"] = d.GESTFIPS.astype(int)
    d["st_ab"] = d.st.map(FIPS)
    d["native"] = d.PRCITSHP.isin([1, 2, 3])
    hga = d.A_HGA.to_numpy()
    edu = np.select([hga <= 38, hga == 39, (hga >= 40) & (hga <= 42), hga >= 43],
                    ["below_high_school", "high_school", "some_college", "ba_plus"], "none")
    adult25 = d.A_AGE.to_numpy() >= 25
    d["edu4"] = np.where(adult25, edu, "under_25")
    d["edu_nativity"] = np.where(adult25, pd.Series(edu) + "|" + np.where(d.native, "us_born", "other_foreign_born"),
                                 "under_25")
    age = d.A_AGE.to_numpy()
    d["age3"] = np.select([age < 18, age < 65], ["under_18", "18_64"], "65_plus")
    hisp = d.PEHSPNON.eq(1).to_numpy()
    race = d.PRDTRACE.to_numpy()
    d["race5"] = np.select([~hisp & (race == 1), ~hisp & (race == 2), hisp, ~hisp & (race == 4)],
                           ["nh_white", "nh_black", "hispanic_other_origin", "nh_asian"], "other")
    d["sex"] = np.where(d.A_SEX.eq(1), "male", "female")
    d["worker"] = np.where(d.WORKYN.eq(1), "worker", "not_worker")
    ind = d.INDUSTRY.to_numpy()
    d["industry5"] = np.where(d.WORKYN.eq(1), np.select(
        [ind == 770, ind == 8680, (ind >= 170) & (ind <= 290), ind == 7770],
        ["construction", "restaurants", "agriculture", "landscaping"], "rest"), "not_worker")
    # Tenure of the household: landlord if it reports rental income (CPS HRNTVAL: rents, royalties,
    # estates and trusts, the survey's only landlord proxy), else renter (rented or no cash rent),
    # else owner without rental income.
    landlord = d.HRNTVAL.ne(0).to_numpy()
    d["tenure"] = np.select([landlord, d.H_TENURE.isin([2, 3]).to_numpy()], ["landlord", "renter"],
                            "owner_no_rental_income")
    d["state3"] = np.select([d.st.eq(6), d.st.eq(48)], ["CA", "TX"], "rest")
    tw = pd.Series(d.pw.to_numpy()[target]).groupby(d.st.to_numpy()[target]).sum().sort_values(ascending=False)
    top10 = [FIPS[s] for s in tw.index[:10]]
    d["top10_states"] = np.where(d.st_ab.isin(top10), d.st_ab, "other_states")
    # Household reference person is an other resident (ACS "other renters" exclude households whose
    # householder is in the group; the CPS seed follows the same rule).
    ref = d.PERRP.isin([40, 41]).to_numpy()
    ref_other = pd.Series(np.where(ref, other, False)).groupby(d.PH_SEQ.to_numpy()).transform("max").to_numpy()
    n_other = d.groupby("PH_SEQ").other.transform("sum").to_numpy()
    d["hh_other_ref"] = ref_other & other
    d["n_other_hh"] = np.maximum(n_other, 1)
    d["earn"] = np.maximum(d.PEARNVAL.to_numpy(float), 0)
    d["wsal"] = np.maximum(d.WSAL_VAL.to_numpy(float), 0)
    d["semp"] = np.maximum(d.SEMP_VAL.to_numpy(float) + d.FRSE_VAL.to_numpy(float), 0)
    d["metro_worker"] = d.WORKYN.eq(1).to_numpy() & d.GTMETSTA.eq(1).to_numpy()
    d["uninsured_py"] = np.where(d.NOCOV_CYR.eq(3), 1.0, np.where(d.NOCOV_CYR.eq(2), 0.5, 0.0))
    return d, top10


# ================================================================== channel totals from lanes
def fiscal_inputs():
    """The case and the case before it by specification (specs.cjs), with their band ends."""
    s = pd.read_csv(PATHS["specs"])
    if set(s.case) != {CASE["model"], CASE["prev"]["model"]}:
        raise SystemExit(f"[BLOCKED] {PATHS['specs']} holds {sorted(set(s.case))}, not the {CASE['case']} run; "
                         f"run specs.cjs --case {CASE['case']} with the same --out-dir first")
    bands = pd.read_csv(PATHS["bands"])
    bands = bands[bands.profile == CASE.get("profile", OLD_PROFILE)].set_index("variant")
    out = {}
    for case, variant in ((CASE["model"], "adopted"), (CASE["prev"]["model"], CASE.get("prev_variant", CASE["prev"]["model"]))):
        c = s[s.case == case]
        lo, hi = c.cost_bn.min(), c.cost_bn.max()
        gate(f"band_reproduced_{case}", np.isclose(lo, bands.loc[variant, "cost_low_bn"], atol=5e-5)
             and np.isclose(hi, bands.loc[variant, "cost_high_bn"], atol=5e-5),
             band=[lo, hi], published=[bands.loc[variant, "cost_low_bn"], bands.loc[variant, "cost_high_bn"]])
        gate(f"welfare_identity_{case}", np.allclose(c.welfare_bn, c.P_bn + c.A_bn + c.F_bn, atol=1e-9))
        ends = {}
        for end, v in (("low", lo), ("high", hi)):
            r = c[np.isclose(c.cost_bn, v, atol=1e-9)]
            # Specifications that tie at an end share A, P and F (they differ only in dimensions
            # that do not move the cost); take the first.
            if not (np.allclose(r.A_bn, r.A_bn.iloc[0]) and np.allclose(r.P_bn, r.P_bn.iloc[0])):
                raise SystemExit(f"[BLOCKED] tied band-end specifications differ in A or P ({case} {end})")
            ends[end] = r.iloc[0].to_dict()
        out[case] = dict(specs=c.reset_index(drop=True), ends=ends)
    return out


def fiscal_one_definition(B, fin):
    """The direct response A at each band end from the base lane's fiscal_totals (one definition for
    both lanes; it gates its own rebuilt band). It builds A from the published case plus each change,
    so it differs from this lane's engine run by rounding; the gap is recorded and must stay < 1e-3."""
    out = {}
    for case, arg in ((CASE["model"], CASE["case"]), (CASE["prev"]["model"], CASE["prev"]["case"])):
        ft = B.fiscal_totals(arg)["adopted"]
        A = {"low": float(ft["A_low_cost"]), "high": float(ft["A_high_cost"])}
        e = fin[case]["ends"]
        diff = {end: A[end] - float(e[end]["A_bn"]) for end in ("low", "high")}
        gate(f"fiscal_totals_{arg}_matches_engine", all(abs(v) < 1e-3 for v in diff.values()), fiscal_totals=A,
             engine={end: float(e[end]["A_bn"]) for end in ("low", "high")}, diff=diff)
        fin[case]["A_one_definition"] = A
        out[case] = dict(A=A, engine_A={end: float(e[end]["A_bn"]) for end in ("low", "high")}, diff=diff,
                         A_mid=float(ft["A_mid"]))
        if "capped_programs" in ft:
            # The distribution lane's case_ends: its capital return must be the engine run's at both ends.
            cap = {end: float(e[end]["capital_total_bn"]) for end in ("low", "high")}
            gate(f"capital_return_{arg}_matches_engine", all(abs(ft["capital_return"][j] - cap[end]) < 1e-9
                                                             for j, end in enumerate(("low", "high"))),
                 distribution_lane=ft["capital_return"], engine=cap)
            fin[case]["capped"] = dict(programs=ft["capped_programs"], capital_return=ft["capital_return"])
    return out


# The debt lane's columns for each financing part of its 2024 split. Before September 27 its lines carry no
# financing column and every line is cash.
FINANCING = {"cash": ("fiscal_gap_bn", "federal_bn"), "resource_cost": ("resource_cost_bn", "resource_cost_federal_bn"),
             "displaced_beneficiaries": ("displaced_bn", "displaced_federal_bn")}
# From September 29 (CASES accrual) a fourth part: the pension switch's accrual, federal, never borrowed or paid today.
ACCRUAL = ("accrual_bn", "accrual_federal_bn")


def financing_parts(c: dict) -> dict:
    """The debt lane's financing parts for a case (a CASES entry): FINANCING, with the pension accrual where it has one."""
    return dict(FINANCING, pension_accrual=ACCRUAL) if c.get("accrual") else FINANCING


def federal_split(fin):
    """Federal part of the fiscal channel at each band end, under the debt legacy lane's three payer
    conventions (low, central, high).

    Used: that lane's own split (derived/federal_split_2024.csv), so each correction's federal share
    is the one its per-correction file defines. Check: this lane's engine lines times that lane's
    per-line fractions, the correction rows (school_reprice, college_rekey, lane_constants) counted
    once as lines, less the induced receipts F at its federal share, reproduce its federal part and
    fiscal gap. On the case (its debt commit) the split is used; on the case before it (that case's
    debt commit) the same recomputation is the method's positive control.

    From September 27 the lane keeps three financing columns apart (its lines file's financing column):
    cash, the resource cost (the capital components, side capital_return; specs.cjs writes them as lines
    capital_<id>, the debt lane as <id>) and the displaced beneficiaries of
    the capped programs. Each part is recomputed from its own lines and gated against its own columns. The
    row's cost_bn is then their sum, the whole A + F; federal_bn, state_local_bn and federal_share are the
    lane's cash columns; the other two parts sit beside them under the lane's names."""
    lines = pd.read_csv(PATHS["lines"])
    out, info = {}, {}
    for case, commit, profile, sub, parts_of in (
            (CASE["prev"]["model"], CASE["prev"]["debt"], CASE["prev"].get("profile", OLD_PROFILE), CASE["prev"].get("debt_dir"),
             financing_parts(CASE["prev"])),
            (CASE["model"], CASE["debt"], CASE.get("profile", OLD_PROFILE), CASE.get("debt_dir"), financing_parts(CASE))):
        dl = debt_csv("federal_split_2024_lines.csv", commit, sub)
        split = debt_csv("federal_split_2024.csv", commit, sub)
        f_ind = debt_json("summary.json", commit, sub)["induced_receipts_federal_share_2024"]
        checks = {}
        for end in ("low", "high"):
            le = lines[(lines.case == case) & (lines.end == end)].copy()
            # specs.cjs names each capital component capital_<id>; the debt lane names it <id>.
            cap = (le.side == "capital_return").to_numpy()
            if cap.any():
                if not le.line[cap].str.startswith("capital_").all():
                    raise SystemExit(f"[BLOCKED] capital lines not named capital_<id> ({case} {end})")
                le.loc[cap, "line"] = le.line[cap].str.slice(len("capital_"))
            le = le.set_index(["side", "line"])
            gate(f"line_ids_unique_{case}_{end}", le.index.is_unique)
            gap = -le.effect_bn                       # cost to other residents, by line
            F = fin[case]["ends"][end]["F_bn"]
            for conv in ("low", "central", "high"):
                frac = dl[(dl.end == end) & (dl.convention == conv)].set_index(["side", "line"])
                gate(f"debt_lines_unique_{case}_{end}_{conv}", frac.index.is_unique)
                # The lane lists the induced receipts as a line; this lane carries them as F.
                fk = ("production", "induced_receipts_F")
                if fk in frac.index:
                    gate(f"debt_lines_F_{case}_{end}_{conv}", np.isclose(frac.gap_bn[fk], -F, atol=1e-5)
                         and np.isclose(frac.federal_bn[fk], -F * f_ind, atol=1e-5),
                         lane=[float(frac.gap_bn[fk]), float(frac.federal_bn[fk])], engine=[-F, -F * f_ind])
                    if "financing" in frac and frac.financing[fk] != "cash":
                        raise SystemExit(f"[BLOCKED] the debt lane's induced receipts are not cash ({case} {end} {conv})")
                    frac = frac.drop(index=[fk])
                fr = (frac.federal_bn / frac.gap_bn).where(frac.gap_bn != 0, 0.0)
                gap_c = gap
                if "pension_accrual" in parts_of:
                    # September 29: the debt lane books the pension switch's excess over the cash set on lines of its
                    # own (side pension_accrual: social security, Medicare, federal income tax), while the engine run
                    # carries each line whole. Split here: the accrual line is the lane's, the engine line keeps the
                    # rest, its cash part, which is then compared with the lane's cash line.
                    gap_c = gap.copy()
                    acc = frac.gap_bn[frac.index.get_level_values(0) == "pension_accrual"]
                    for (_, lid), a in acc.items():
                        k = [(s, lid) for s in ("spending", "receipt") if (s, lid) in gap_c.index]
                        if len(k) != 1:
                            raise SystemExit(f"[BLOCKED] the accrual line {lid} is not one engine line ({case} {end} {conv})")
                        gap_c.loc[k[0]] -= a
                        gap_c.loc[("pension_accrual", lid)] = a
                # Every line with a responsive effect has a fraction, and every line the lane lists
                # is in the engine run (zero-response lines such as defense carry no effect).
                unknown = [k for k in gap_c.index if k not in fr.index and abs(gap_c[k]) > 1e-12]
                absent = [k for k in frac.index if k not in gap_c.index and abs(frac.gap_bn[k]) > 1e-12]
                if unknown or absent:
                    raise SystemExit(f"[BLOCKED] lines differ from the debt lane ({case} {end} {conv}): "
                                     f"without a fraction {unknown}; not in the engine run {absent}")
                common = gap_c.index.intersection(frac.index)
                line_diff = float((gap_c[common] - frac.gap_bn[common]).abs().max())
                parts = "financing" in frac
                if parts and not frac.financing.isin(list(parts_of)).all():
                    raise SystemExit(f"[BLOCKED] unknown financing in the debt lane's lines: "
                                     f"{sorted(set(frac.financing) - set(parts_of))}")
                sel = {p: common[(frac.financing[common] == p).to_numpy()] if parts else common for p in parts_of}
                fed = float((gap_c[sel["cash"]] * fr[sel["cash"]]).sum()) - F * f_ind
                cost = float((gap_c[sel["cash"]] if parts else gap_c).sum()) - F
                ref = split[(split.profile == profile) & (split.end == end) & (split.convention == conv)]
                gate(f"debt_split_row_unique_{case}_{end}_{conv}", len(ref) == 1, rows=len(ref))
                ref = ref.iloc[0]
                gate(f"federal_split_recomputed_{case}_{end}_{conv}",
                     np.isclose(fed, ref.federal_bn, atol=1e-5) and np.isclose(cost, ref.fiscal_gap_bn, atol=1e-5)
                     and line_diff < 1e-5, recomputed=fed, lane=float(ref.federal_bn), cost=cost,
                     lane_cost=float(ref.fiscal_gap_bn), max_line_diff_bn=line_diff)
                row = dict(cost_bn=float(ref.fiscal_gap_bn), federal_bn=float(ref.federal_bn),
                           state_local_bn=float(ref.state_local_bn), federal_share=float(ref.federal_share),
                           recomputed_federal_bn=fed, max_line_diff_bn=line_diff)
                if parts:
                    whole = ref.fiscal_gap_bn
                    for p in [x for x in parts_of if x != "cash"]:
                        c_col, f_col = parts_of[p]
                        cp, fp = float(gap_c[sel[p]].sum()), float((gap_c[sel[p]] * fr[sel[p]]).sum())
                        gate(f"federal_split_recomputed_{p}_{case}_{end}_{conv}",
                             np.isclose(cp, ref[c_col], atol=1e-5) and np.isclose(fp, ref[f_col], atol=1e-5),
                             recomputed=[cp, fp], lane=[float(ref[c_col]), float(ref[f_col])])
                        row.update({c_col: float(ref[c_col]), f_col: float(ref[f_col])})
                        whole = whole + ref[c_col]
                    row["cost_bn"] = float(whole)
                for syn in ("school_reprice", "college_rekey", "lane_constants"):
                    if ("spending", syn) in frac.index:
                        row[f"{syn}_bn"] = float(frac.gap_bn[("spending", syn)])
                        row[f"{syn}_federal_bn"] = float(frac.federal_bn[("spending", syn)])
                out[(case, end, conv)] = row
                checks[f"{end}_{conv}"] = [fed, float(ref.federal_bn)]
        info[case] = dict(commit=commit, induced_receipts_federal_share=f_ind, recomputed_vs_lane=checks)
    info["per_correction_file"] = per_correction_check()
    return out, info


def per_correction_check():
    """The debt lane's per-correction file against the correction rows of its lines file: the lane
    constants (with row 8's finite-removal piece, its own component from September 26 on), and schools
    with colleges (its education_row6_and_school_price component). Both are read at the case's pinned
    commits.

    From October 5 the lines carry the added people's part of each correction line, and row 8's change at the larger
    group on the constant line. The per-correction file holds them as components of their own (v5_lineage, every line
    together; v5_union_response), so their parts on the correction lines come from the lane's by-line file
    (corrections_federal_split_2024.csv: v5_lineage:constants and v5_union_response:row8 for the constants, v5_lineage on
    school_reprice and college_rekey), itself gated to rebuild those components.

    From October 7 the lines also carry the v6 items, each a component of its own named v6_<item> (v6_retiree_health,
    by line v6_retiree_health:scale; v6_user_fees). The items' rows on school_reprice and college_rekey (v6_user_fees: the
    K-12 weight's re-blend of row 6) join the lineage's there; no item edits the lane constants. The rebuild gate covers
    the v6 components too, a component missing from one file counting as zero."""
    raw = read_input("debt_corrections")
    comp = pd.read_csv(io.BytesIO(raw))
    dl = debt_csv("federal_split_2024_lines.csv", CASE["debt"], CASE.get("debt_dir")).set_index(["end", "convention", "side", "line"])
    lineage = comp.component.str.startswith("v5_").any()
    # The case's own components: the lineage's (v5_, October 5 on) and the v6 items' (v6_, October 7 on).
    own = r"^v[56]_"
    items = sorted(set(comp.component[comp.component.str.startswith("v6_")]))
    if lineage:
        byl = debt_csv("corrections_federal_split_2024.csv", CASE["debt"], CASE.get("debt_dir"))
        cols = ["effect_bn", "federal_bn"]
        rebuilt = byl[byl.component.str.match(own)].assign(component=lambda x: x.component.str.split(":").str[0])
        rebuilt = rebuilt.groupby(["end", "convention", "component"])[cols].sum()
        held = comp[comp.component.str.match(own)].groupby(["end", "convention", "component"])[cols].sum()
        gap = float(rebuilt.sub(held, fill_value=0).abs().max().max())
        gate("debt_by_line_file_rebuilds_lineage_components", gap < 1e-5, max_abs_diff_bn=gap, rows=len(held),
             **({"item_components": items} if items else {}))
        on_lines = {"lane_constants": byl.component.isin(["v5_lineage:constants", "v5_union_response:row8"]),
                    "education_row6_and_school_price": byl.component.str.match(own) & (byl.side == "spending")
                    & byl.line.isin(["school_reprice", "college_rekey"])}
        added = {k: byl[m].groupby(["end", "convention"])[cols].sum() for k, m in on_lines.items()}
    worst, n = 0.0, 0
    for components, rows in ((("lane_constants", "finite_removal"), ("lane_constants",)),
                             (("education_row6_and_school_price",), ("school_reprice", "college_rekey"))):
        parts = comp[comp.component.isin(components)].groupby(["end", "convention"], sort=False)
        for (end, conv), r in parts[["federal_bn", "effect_bn"]].sum().iterrows():
            v = dl.loc[[(end, conv, "spending", x) for x in rows]]
            fed, eff = r.federal_bn, r.effect_bn
            if lineage:
                a = added[components[0]].loc[(end, conv)]
                fed, eff = fed + a.federal_bn, eff + a.effect_bn
            worst = max(worst, abs(v.federal_bn.sum() - fed), abs(v.gap_bn.sum() - eff))
            n += 1
    gate("debt_lines_carry_per_correction_split", n == 12 and worst < 1e-5, rows=n, max_abs_diff_bn=worst)
    out = dict(status="checked", rows=n, max_abs_diff_bn=worst, sha256=sha(raw))
    if lineage:
        out["lineage"] = ("the added people's parts of the correction lines from corrections_federal_split_2024.csv "
                          "(v5_lineage:constants, v5_union_response:row8; v5_lineage on school_reprice and college_rekey)")
    if items:
        out["items"] = (f"the v6 items' components ({', '.join(items)}), rebuilt from the same file; their rows on "
                        "school_reprice and college_rekey join the lineage's there")
    return out


def deficit_share_fy2024():
    """FY2024 federal deficit over federal outlays: OMB Historical Tables 2.1 (receipts) and 3.1
    (outlays), FY2027 budget release, pinned in sources/."""
    r = pd.read_excel(PATHS["omb_receipts"], header=None)
    row = r[r[0].astype(str).str.strip() == "2024"]
    receipts = float(row.iloc[0, 8])
    o = pd.read_excel(PATHS["omb_outlays"], header=None)
    col = [j for j, v in enumerate(o.iloc[1]) if str(v).strip() == "2024"][0]
    outlays = float(o[o[0].astype(str).str.strip() == "Total, Federal outlays"].iloc[0, col])
    gate("omb_fy2024_totals", 4.8e6 < receipts < 5.0e6 and 6.6e6 < outlays < 6.9e6, receipts_musd=receipts,
         outlays_musd=outlays)
    return dict(receipts_musd=receipts, outlays_musd=outlays, deficit_musd=outlays - receipts,
                share=(outlays - receipts) / outlays)


def crime_inputs(B):
    """Victims' harm only as a lane computed it, each with its footing: decision 4's $30.93bn (central;
    equal footing with the NIBRS mixed-group correction), the victim lane's equal footing ($28.92bn)
    and custody footing ($32.34bn), NIBRS's victim-conditional arm, and the victim lane's envelope."""
    off = pd.read_csv(B.PATHS["crime_offence"]).set_index("offence")
    arms = pd.read_csv(B.PATHS["crime_arms"]).set_index("arm")
    equal = float(off.loc["Total", "cost_full"]) / 1e9
    custody = float(arms.loc["scaling: ACS institutional ratio 1.118 (generic reallocated)", "full_bn"])
    de = pd.read_csv(PATHS["crime_dollar"])
    mixed = de[de.method.str.contains("theta 0.4977", regex=False)
               & de.method.str.contains("NIBRS TX+AZ mean Hispanic fraction of mixed groups", regex=False)]
    gate("crime_mixed_group_row_unique", len(mixed) == 1, rows=len(mixed))
    mixed_equal = float(mixed.full_bn.iloc[0])
    nib = pd.read_csv(PATHS["nibrs_cost"])
    nib_c = nib[(nib.spec == "central") & (nib.arm == "victim-conditional, SHR-calibrated")]
    gate("crime_nibrs_central_unique", len(nib_c) == 1, rows=len(nib_c))
    out = dict(equal=equal, custody=custody, mixed_equal=mixed_equal, nibrs_equal=float(nib_c.full_bn.iloc[0]),
               envelope_low=float(arms.loc["ENVELOPE low, miller2021", "full_bn"]),
               envelope_high=float(arms.loc["ENVELOPE high, miller2021_dot_vsl", "full_bn"]))
    gate("crime_inputs_pinned", np.isclose(equal, 28.9229, atol=5e-4) and np.isclose(custody, 32.3381, atol=5e-4)
         and np.isclose(mixed_equal, 30.9274, atol=5e-4), **{k: v for k, v in out.items()})
    out["footing"] = dict(
        mixed_equal="equal footing (Mexican-origin offending at NCVS Hispanic rates) with the NIBRS mixed-group "
                    "correction, theta 0.4977; decision 4's figure [crime_ratio_direction_2026_09_24]",
        equal="equal footing, no mixed-group correction; the victim lane's central [crime_victim_cost_2026_09_23]",
        custody="custody footing (ACS institutional ratio 1.118, generic Hispanic reallocated), no mixed-group "
                "correction [crime_victim_cost_2026_09_23]",
        nibrs_equal="NIBRS victim-conditional, SHR-calibrated [offender_ethnicity_nibrs_2026_09_23]",
        envelope_low="the victim lane's envelope, every arm at its low setting, Miller 2021 prices",
        envelope_high="the victim lane's envelope, every arm at its high setting, Miller 2021 prices with the "
                      "DOT 2024 VSL for murder")
    return out


def preference_inputs():
    ch = pd.read_csv(PATHS["preferences"])
    text = PATHS["preferences_log"].read_text()
    mex = {}
    for lev in LEVELS:
        m = re.search(rf"2024 {lev}\s*:.*?Mexican-origin \$([0-9.]+)bn", text)
        mex[lev] = float(m.group(1))
    regime = {lev: float(ch[f"y2024_{lev}"].sum()) for lev in LEVELS}
    ch["mex_central"] = ch.y2024_central * ch.mex_share
    parts = {"admissions": ch.mex_central[ch.channel.str.startswith("1 ")].sum(),
             "contractor_hiring": ch.mex_central[ch.channel.str.startswith("2 ")].sum(),
             "lost_profits": ch.mex_central[ch.channel.str.contains("lost profits")].sum(),
             "taxpayer_premium": ch.mex_central[ch.channel.str.contains("price premium")].sum()}
    gate("preferences_group_part_reproduced", np.isclose(sum(parts.values()), mex["central"], atol=0.006),
         parts=sum(parts.values()), lane=mex["central"])
    return dict(group_part=mex, regime=regime, parts={k: float(v) for k, v in parts.items()})


PREFERENCE_RULE = (
    "proportional replacement: a program's preferred placements scale with its eligible pool, so without the group "
    "its seats, jobs and contracts go to the non-preferred pool in the proportions of the producer's race-neutral "
    "counterfactual (freed seats as AKR, Espenshade-Chung and Hinrichs split them; contractor jobs over non-Hispanic, "
    "non-Black earners; contracts over incorporated self-employment earnings; the premium over taxes), and no other "
    "eligible group takes them. Under a fixed-target rule other eligible recipients would take the placements and "
    "white natives would recover nothing")


def preference_attribution(d, pr):
    """The preferences row as an attribution (adversarial audit 2026-09-28, section 3). The producer
    (affirmative_action_cost_2026_09_24) prices non-Hispanic white natives' loss from the whole regime
    against race-neutral selection, and this lane's row is that loss times the Mexican-origin share of each
    channel's beneficiaries. A beneficiary share is neither a policy response nor a replacement allocation,
    so the row states the rule it assumes (PREFERENCE_RULE). Under that rule the non-preferred pool's other
    members, other residents who are not white natives, gain too, in the producer's own proportions: the
    white natives' part times (1 - s) / s, where s is their share of the pool:
      admissions: s = W x nat by tier boundary (W the white share of freed seats, nat the native share of
        non-Hispanic white BA+ aged 22-40), over the boundaries' Hispanic freed seats and per-worker losses;
      contractor hiring: s = w x nat_w (w the non-Hispanic white share of non-Hispanic, non-Black earners);
      lost profits: s = white natives' share of incorporated self-employment earnings;
      taxpayer premium: s = their share of income, payroll and state income tax.
    The CPS shares are recomputed on this frame with the producer's definitions (its weight MARSUPWT/100
    equals this frame's pwwgt0 to 0.005 persons) and gated to its logged values; W, the seat losses and the
    per-worker losses come from its calc.py (module constants only, never main()) and ipeds_tiers.csv,
    gated to its logged crossings and per-worker losses. The group's own pool share (its taxes, its firms)
    goes to the others, since without the group the remaining pool takes it [INFERENCE].

    The DBE premium (row 3c) is a price inside observed spending on DOT-assisted contracts. Since
    September 27 the fiscal channel removes the group's key share times the response of highway spending
    and highway capital (the response lane's net_change.json: key share 0.0806; highway response 0.733 at
    the low end, 1 at the high end). That part of the premium is already in the fiscal channel and is
    netted from the row, at the mean of the two ends; the rest is a price change the account does not
    see. Row 3d, the 8(a) premium, is 0 in the central composition."""
    spec = importlib.util.spec_from_file_location("preferences_calc", PATHS["preferences_code"])
    M = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(M)
    log = PATHS["preferences_log"].read_text()
    num = lambda s: float(s.replace(",", ""))  # noqa: E731
    # CPS shares, the producer's definitions (calc.py cps()), all person records.
    w, earn = d.pw.to_numpy(), d.PEARNVAL.to_numpy(float)
    nhw = d.PEHSPNON.eq(2).to_numpy() & d.PRDTRACE.eq(1).to_numpy()
    wn, hisp = nhw & d.native.to_numpy(), d.PEHSPNON.eq(1).to_numpy()
    earner, ba, age = earn > 0, d.A_HGA.to_numpy() >= 43, d.A_AGE.to_numpy()
    inc_se = d.A_CLSWKR.eq(5).to_numpy()
    ws = lambda m, v=None: float((w[m] * (1 if v is None else v[m])).sum())  # noqa: E731
    tax = d.FEDTAX_AC.clip(lower=0).to_numpy(float) + d.FICA.clip(lower=0).to_numpy(float) \
        + d.STATETAX_A.clip(lower=0).to_numpy(float)
    c = dict(nat_ba=ws(wn & ba & (age >= 22) & (age <= 40)) / ws(nhw & ba & (age >= 22) & (age <= 40)),
             emp_wn_ba=ws(wn & ba & (age >= 22) & (age <= 61) & earner) / ws(wn & ba & (age >= 22) & (age <= 61)),
             e_wn_ba=ws(wn & earner & ba & (age >= 25) & (age <= 64), earn) / ws(wn & earner & ba & (age >= 25) & (age <= 64)),
             nat_w=ws(wn & earner) / ws(nhw & earner),
             white_of_nonpref=ws(nhw & earner) / ws(earner & ~hisp & ~(d.PEHSPNON.eq(2).to_numpy() & d.PRDTRACE.eq(2).to_numpy())),
             se_wn=ws(wn & inc_se & earner, earn) / ws(inc_se & earner, earn),
             tax_wn=ws(wn, tax) / ws(np.ones(len(d), bool), tax))
    logged = dict(nat_ba=r"native share of NH-white BA\+ 22-40: ([\d.]+)", emp_wn_ba=r"share with earnings,\s+ages 22-61: ([\d.]+)",
                  e_wn_ba=r"BA\+ aged 25-64 mean earnings \$([\d,]+)", nat_w=r"native share of NH-white workers: ([\d.]+)",
                  white_of_nonpref=r"neither\s+Hispanic nor non-Hispanic Black: ([\d.]+)",
                  se_wn=r"of incorporated\s+self-employed earnings ([\d.]+)", tax_wn=r"income\+payroll\+state income tax ([\d.]+)")
    for k, pat in logged.items():
        v = num(re.search(pat, log).group(1))
        gate(f"preferences_cps_{k}_reproduced", abs(c[k] - v) <= (0.5 if k == "e_wn_ba" else 5e-4) + 1e-9, frame=c[k], lane=v)
    # Admissions at the central scenario: the producer's crossings by tier boundary (calc.py admissions()).
    i = 1
    tiers = pd.read_csv(PATHS["preferences_tiers"]).set_index("tier")
    per_worker = {"E": c["emp_wn_ba"] * M.p("elite_earn_2007") * M.CPI_2024 / M.CPI_2007 * M.p("r_elite")[i],
                  "S": c["emp_wn_ba"] * c["e_wn_ba"] * M.p("r_sel")[i]}
    cross = re.search(r"central\s+boundary E black [\d,]+; boundary E hisp ([\d,]+); boundary S black [\d,]+; "
                      r"boundary S hisp ([\d,]+)", log)
    lost = re.search(r"central\s+2024 stock cost by boundary: E \$[\d.]+bn \(loss per affected worker-year \$([\d,]+)\), "
                     r"S \$[\d.]+bn \(\$([\d,]+)\)", log)
    white = others = 0.0
    for j, (b, rows, red, W) in enumerate((("E", ["E"], M.RED_E, M.W_E), ("S", ["E", "S"], M.RED_S, M.W_S))):
        freed = float(tiers.loc[rows, "hisp"].sum() + tiers.loc[rows, "aian"].sum()) * red["hisp"][i]
        x = freed * W[i] * c["nat_ba"]
        gate(f"preferences_admissions_boundary_{b}_reproduced", abs(x - num(cross.group(j + 1))) <= 0.5
             and abs(per_worker[b] - num(lost.group(j + 1))) <= 0.5, crossings=x, lane_crossings=num(cross.group(j + 1)),
             per_worker=per_worker[b], lane_per_worker=num(lost.group(j + 1)))
        white += x * per_worker[b]
        others += (freed - x) * per_worker[b]
    share = dict(admissions=white / (white + others), contractor_hiring=c["white_of_nonpref"] * c["nat_w"],
                 lost_profits=c["se_wn"], taxpayer_premium=c["tax_wn"])
    # The DBE premium's part already in the fiscal channel.
    net = json.loads(PATHS["long_run_net_change"].read_text())["by_band_end"]
    kh = {end: net[end]["key_share"] * net[end]["highway_response"] for end in ("low", "high")}
    ch = pd.read_csv(PATHS["preferences"])
    dbe = ch[ch.channel.str.startswith("3c ")]
    gate("preferences_dbe_premium_row_unique", len(dbe) == 1, rows=len(dbe))
    dbe_part = float(dbe.y2024_central.iloc[0] * dbe.mex_share.iloc[0])
    overlap = (kh["low"] + kh["high"]) / 2
    white_parts = dict(pr["parts"], taxpayer_premium=pr["parts"]["taxpayer_premium"] - dbe_part * overlap)
    other_parts = {p: v * (1 - share[p]) / share[p] for p, v in white_parts.items()}
    # Elite freed seats that go to none of the four groups the sources report (race other or unknown); the
    # admissions' others take them with the rest of 1 - W.
    outside = lambda t: 1 - sum(t[g][1] - t[g][0] for g in ("white", "asian")) / sum(  # noqa: E731
        t[g][0] - t[g][1] for g in ("black", "hisp"))
    return dict(rule=PREFERENCE_RULE, cps_shares=c, white_share_of_pool=share,
                outside_groups=dict(ec=outside(M.EC), akr=outside(M.AKR["harvard"])),
                admissions_value_white_others=[white, others], dbe_premium_part_bn=dbe_part,
                dbe_in_fiscal_channel_share={"low": kh["low"], "high": kh["high"], "used": overlap},
                dbe_netted_bn=dbe_part * overlap, white_parts=white_parts, other_parts=other_parts,
                scale={L: pr["group_part"][L] / sum(pr["parts"].values()) for L in LEVELS})


def congestion_inputs():
    arms = pd.read_csv(PATHS["congestion_arms"]).set_index("approach")
    b1 = arms.loc["B1 population elasticity, lanes fixed"]
    m = pd.read_csv(PATHS["congestion_metro"], dtype={"ua": str})
    u = pd.read_csv(PATHS["congestion_ua"], dtype={"ua": str})[["ua", "state"]].drop_duplicates("ua")
    m = m.merge(u, on="ua", how="left", validate="many_to_one")
    gate("congestion_ua_states", m.state.notna().all() and m.state.isin(POSTAL).all(),
         missing=int(m.state.isna().sum()))
    by_state = m.groupby("state").B1_bn.sum()
    gate("congestion_states_sum", np.isclose(by_state.sum(), b1.central_bn, rtol=1e-9),
         states=by_state.sum(), lane=float(b1.central_bn))
    return dict(total={"low": float(b1.min_bn), "central": float(b1.central_bn), "high": float(b1.max_bn)},
                state_share=(by_state / by_state.sum()).rename(index=POSTAL).to_dict())


def congestion_long_run(b1):
    """From September 27 roads respond in the long run, so lanes shrink without the group, and the
    congestion item beside the account is the response lane's re-derivation (service_response_long_run_
    2026_09_27/congestion.py, derived/net_change.json): B1 with lanes cut uniformly over urban areas by
    the highway response times the group's key share, at central inputs, $13.99bn at the low band end and
    $12.02bn at the high end, against B1's $19.16bn with lanes fixed.

    By state: that lane's own arm per area (its setup() and the congestion lane's time_cost_arm, imported
    read-only, never its main()), summed within the UMR areas' states. Gates: with no cut it reproduces
    B1's state totals from metro_distribution.csv, and at each band end the lane's total. A uniform cut
    offsets congestion in proportion to each area's delay, so where the group is thin the offset exceeds
    its traffic and other residents there come out ahead.

    Levels: central is the mean of the two ends, the fiscal channel's central; low is the low end's
    factorial minimum and high the high end's maximum (each end's own range, as the real-costs span pairs
    them with the fiscal band ends), each spread by its end's geography."""
    net = json.loads(PATHS["long_run_net_change"].read_text())
    gate("congestion_long_run_starts_from_b1", np.isclose(net["b1_lanes_fixed_bn"], b1["total"]["central"], rtol=0, atol=1e-9)
         and np.allclose(net["b1_factorial_bn"], [b1["total"]["low"], b1["total"]["high"]], rtol=0, atol=1e-9),
         lane=[net["b1_lanes_fixed_bn"]] + list(net["b1_factorial_bn"]))
    spec = importlib.util.spec_from_file_location("long_run_congestion", PATHS["long_run_congestion_code"])
    C = importlib.util.module_from_spec(spec)
    with contextlib.redirect_stdout(io.StringIO()):
        spec.loader.exec_module(C)
        _, nhts, tau, vots, exposures, _ = C.setup()
    A = C.A
    e = exposures["2017 southwest"]
    scope, r_h, eps = e["in_scope"].to_numpy(), nhts["2017 southwest"]["r_hours"], A.POP_FIXED_LANES["central"]
    gate("congestion_long_run_area_states", e.state[scope].isin(POSTAL).all(), missing=int((~e.state[scope].isin(POSTAL)).sum()))

    def by_state(lam, cut):
        # The lane's arm() per area rather than summed: the same log cost and time-cost arm.
        log_c0 = eps * np.log1p(-e.s) - lam * np.log1p(-cut)
        res = A.time_cost_arm(e, log_c0, 0.0, tau["central"], e.phi_commute_route, vots["central"], 2022, r_h)
        usd = pd.Series(np.where(scope, res["usd"].to_numpy(), 0.0) / 1e9)
        return usd[scope].groupby(e.state[scope].map(POSTAL).to_numpy()).sum()
    fixed = by_state(0.0, 0.0)
    worst = max(abs(fixed.get(s, 0.0) - v * b1["total"]["central"]) for s, v in b1["state_share"].items())
    gate("congestion_long_run_reproduces_b1_by_state", np.isclose(fixed.sum(), b1["total"]["central"], rtol=0, atol=1e-9)
         and worst < 1e-9 and set(fixed.index) == set(b1["state_share"]), total=float(fixed.sum()), max_state_gap_bn=worst)
    ends = {}
    for end in ("low", "high"):
        v = net["by_band_end"][end]
        s = by_state(A.LANES_COEF_T10, v["lane_cut"])
        lane_arm = C.arm(e, scope, e.s, eps, A.LANES_COEF_T10, v["lane_cut"], tau["central"], vots["central"], 2022, r_h)
        gate(f"congestion_long_run_{end}_end_reproduced", np.isclose(s.sum(), v["congestion_bn"], rtol=0, atol=1e-9)
             and np.isclose(lane_arm, v["congestion_bn"], rtol=0, atol=1e-9), states=float(s.sum()),
             arm=float(lane_arm), lane=v["congestion_bn"])
        ends[end] = s
    state = {"low": ends["low"] * (net["by_band_end"]["low"]["congestion_range_bn"][0] / ends["low"].sum()),
             "central": (ends["low"] + ends["high"]) / 2,
             "high": ends["high"] * (net["by_band_end"]["high"]["congestion_range_bn"][1] / ends["high"].sum())}
    total = {L: float(state[L].sum()) for L in LEVELS}
    return dict(total=total, state_bn={L: {int(s): float(x) for s, x in state[L].items()} for L in LEVELS},
                by_band_end={end: dict(central_bn=net["by_band_end"][end]["congestion_bn"],
                                       range_bn=net["by_band_end"][end]["congestion_range_bn"],
                                       lane_cut=net["by_band_end"][end]["lane_cut"],
                                       states_with_a_gain=sorted(FIPS[int(s)] for s, x in ends[end].items() if x < 0))
                             for end in ("low", "high")},
                b1_lanes_fixed_bn=b1["total"]["central"])


def scale_inputs():
    s = pd.read_csv(PATHS["scale"])
    j = s[(s.table == "joint_grid") & (s.geography == "CZ 1990")].iloc[0]
    m = pd.read_csv(PATHS["scale_metro"])
    # Metro names carry the first-named state ("New York-Newark-Jersey City, NY-NJ" -> NY); the
    # non-metro remainder of each state is "nonCBSA_<FIPS>".
    st = m.name.str.extract(r",\s*([A-Z]{2})")[0].map(POSTAL)
    st = st.fillna(pd.to_numeric(m.name.str.extract(r"^nonCBSA_(\d+)$")[0], errors="coerce"))
    gate("scale_metro_states", st.notna().all() and st.isin(list(FIPS)).all(), missing=int(st.isna().sum()))
    by_state = m.net_bn.groupby(st.astype(int)).sum()
    total = dict(low=float(j.gain_low_bn), central=float(j.gain_bn), high=float(j.gain_high_bn))
    return dict(total=total, private_share=float(j.private_bn / j.gain_bn),
                receipts_share=float(j.induced_receipts_bn / j.gain_bn),
                state_share=(by_state / by_state.sum()).to_dict(), metro_total_bn=float(by_state.sum()))


def mobility_inputs():
    j = json.loads(PATHS["mobility"].read_text())
    ins = j["insurance_present_bn"]
    bor = j["borjas_bn"]["observed_2024_sorting"]
    tot = j["lane_total_present_bn"]
    for lev in LEVELS:
        gate(f"mobility_parts_add_{lev}", np.isclose(ins[lev] + bor[lev], tot[lev], atol=1e-9),
             parts=ins[lev] + bor[lev], total=tot[lev])
    return dict(insurance=ins, borjas=bor, total=tot)


def care_inputs():
    c = pd.read_csv(PATHS["care"]).set_index("channel")
    tot = c.loc["TOTAL of additive channels"]
    return dict(total={"low": float(tot.low_bn), "central": float(tot.central_bn), "high": float(tot.high_bn)},
                hours_taxes=float(c.loc["taxes on native women's extra hours (household-service channel)", "central_bn"]),
                elder_care=float(c.loc["elder care: Medicaid nursing-facility saving net of Medicaid home care", "central_bn"]),
                private_gain=float(c.loc["native women's private gain from the extra hours", "central_bn"]),
                consumer_surplus_net=float(c.loc["consumer surplus on immigrant-intensive services, net of native low-skill wage gain", "central_bn"]))


def debt_inputs(fin):
    """Interest on past gaps: the debt legacy lane's main benchmark, central payer convention,
    effective rate path, 2005 window, all borrowed, rule programme_income_pandemic_per_head, on the case
    (its debt commit); the previous case's values (on September 24, the September 23 case: decision 4's
    $30.5-38.9bn) are kept for the record."""
    out = {}
    for case in (CASE["case"], CASE["prev"]["case"]):
        commit, pinned = CASES[case]["debt"], CASES[case]["interest"]
        s = debt_csv("stocks.csv", commit, CASES[case].get("debt_dir"))
        main = s[(s.benchmark == "main") & (s.convention == "central") & (s.rate_path == "effective")
                 & (s.window_start == 2005) & (s.financing == "all_borrowed")]
        c = main[main.rule == "programme_income_pandemic_per_head"].set_index("end")
        lo, hi = float(c.loc["low", "legacy_interest_2024_bn"]), float(c.loc["high", "legacy_interest_2024_bn"])
        if pinned is None:     # --dev-unpinned only: configure stops any other run without the pin
            print(f"  [DEV] {case}: legacy interest {lo:.6f} / {hi:.6f}bn from the working tree, not gated (no pin)")
        else:
            gate(f"debt_legacy_pinned_{case}", np.isclose(lo, pinned[0], atol=5e-4) and np.isclose(hi, pinned[1], atol=5e-4),
                 low=lo, high=hi)
        # The lane's "range across the eleven back-cast rules on both anchors".
        out[case] = dict(low=lo, high=hi, central=(lo + hi) / 2, rules_min=float(main.legacy_interest_2024_bn.min()),
                         rules_max=float(main.legacy_interest_2024_bn.max()), commit=commit)
    band = debt_json("summary.json", CASE["debt"], CASE.get("debt_dir"))["case"]["band"]
    ends = fin[CASE["model"]]["ends"]
    gate(f"debt_legacy_is_{CASE['case']}_case", np.allclose(band, [ends["low"]["cost_bn"], ends["high"]["cost_bn"]],
                                                           atol=5e-5),
         lane=band, engine=[ends["low"]["cost_bn"], ends["high"]["cost_bn"]])
    return dict(out[CASE["case"]], **{CASE["prev"]["case"]: out[CASE["prev"]["case"]]})


def housing_inputs(I):
    """Ladder 190's housing range for other residents. Central: the metro-local arm's long-run
    central ($3.51bn net), the base lane's central and the geography this frame keys by state. The
    national-uniform arm's long-run central ($0.71bn) is the other end of the published range and a
    named variant. Low and high: the lowest and highest net in the lane's long-run grid (-$0.38bn,
    +$9.40bn). Each level's renters and landlords are spread by the cells and states of the
    form-A arm with the same elasticity level and geography, scaled to that level's totals."""
    head = pd.read_csv(PATHS["housing_headline"])
    head = head[(head.arm == "long_run") & (head.level == "central")].drop_duplicates("geography")
    head = {g: head[head.geography == g].iloc[0] for g in ("metro_local", "national_uniform")}
    grid = pd.read_csv(PATHS["housing_grid"])
    lr = grid[grid.arm == "long_run"]
    lo = lr.loc[lr.net_other_residents_welfare_bn.idxmin()]
    hi = lr.loc[lr.net_other_residents_welfare_bn.idxmax()]
    net = "net_other_residents_welfare_bn"
    gate("housing_is_ladder_190", np.isclose(head["national_uniform"][net], 0.708230, atol=5e-6)
         and np.isclose(head["metro_local"][net], 3.507579, atol=5e-6) and np.isclose(lo[net], -0.379246, atol=5e-6)
         and np.isclose(hi[net], 9.403796, atol=5e-6),
         centrals=[float(head["national_uniform"][net]), float(head["metro_local"][net])],
         span=[float(lo[net]), float(hi[net])])

    def level(r, pattern):
        a = I["arms"][pattern]
        return dict(renters_bn=float(r.other_renters_extra_rent_bn), net_bn=float(r[net]),
                    landlords_bn=float(r.other_renters_extra_rent_bn + r[net]),
                    owner_stock_bn=float(r.other_owner_value_gain_stock_bn), pattern=pattern,
                    pattern_scale=float(r.other_renters_extra_rent_bn / a["other_renters_extra_rent_bn"]),
                    row=f"long run, {r.level} elasticity, form {r.form}, {r.geography}, ownership {r.ownership}, "
                        f"leak {r.leak_other_occupied}, {r.rule}")
    for geo in ("metro_local", "national_uniform"):
        a = I["arms"][("central", geo)]
        gate(f"housing_central_is_base_arm_{geo}", np.isclose(a[net], head[geo][net], atol=1e-9)
             and np.isclose(a["other_renters_extra_rent_bn"], head[geo]["other_renters_extra_rent_bn"], atol=1e-9))
    return {"low": level(lo, (lo.level, lo.geography)),
            "central": level(head["metro_local"], ("central", "metro_local")),
            "high": level(hi, (hi.level, hi.geography)),
            "national_uniform_central": level(head["national_uniform"], ("central", "national_uniform"))}


def consumption_proposal(fin):
    """The consumption lane's proposed key (spec both_corridor_net_h2: consumption taxes keyed on CE
    spending by income rank, net of corridor-calibrated remittances). A proposal on the September 24
    case: it changes the fiscal total, never a net or the adopted total here. The later cases carry it
    inside the fiscal channel, so their runs have no such row."""
    j = json.loads(PATHS["consumption"].read_text())
    ends = fin[CASE["model"]]["ends"]
    band = [ends["low"]["cost_bn"], ends["high"]["cost_bn"]]
    gate("consumption_lane_on_adopted_band", np.allclose(j["adopted_band"], band, atol=5e-5), lane=j["adopted_band"],
         engine=band)
    sp = j["specs"]["both_corridor_net_h2"]
    ch = [float(x) for x in sp["change"]]
    gate("consumption_proposal_change", np.allclose(ch, np.subtract(sp["band"], j["adopted_band"]), atol=1e-9)
         and np.allclose(ch, -4.0517, atol=5e-4), change=ch, band=sp["band"])
    both = [float(v["change"][0]) for v in j["specs"].values() if v.get("family") == "both"]
    return dict(change=ch, band=[float(x) for x in sp["band"]], both_min=min(both), both_max=max(both),
                survey=float(j["specs"]["both_survey_cemla"]["change"][0]))


def banxico_remittances():
    """2024 remittances received in Mexico, from Banxico SIE table CE167 (quarterly $mn, revised; the
    consumption lane cites series SE43675, all countries, and SE43738, United States), read the way
    consumption_key_2026_09_24/remittance.py primary_flows() reads them and checked against that lane's
    committed corridor. Also that lane's reading: the corridor needs about 3.3 times the surveyed amount."""
    flows = pd.read_csv(PATHS["remittance_flows"]).set_index("spec")
    lane_us = float(re.search(r"\$([\d.]+)bn", flows.loc["corridor_full", "note"]).group(1))
    cemla = float(re.search(r"\$([\d,]+) a year", flows.loc["survey_cemla", "note"]).group(1).replace(",", ""))
    ratio = float(flows.loc["corridor_net_h2", "sent_per_expected_sending_union_unit"]) / cemla
    gate("corridor_needs_over_3x_surveyed_amounts", 3.2 < ratio < 3.5, ratio=ratio, cemla_usd=cemla)
    out = dict(lane_us_bn=lane_us, corridor_over_cemla=ratio, cemla_usd=cemla)
    path = PATHS["banxico_ce167"]
    if not path.is_file():
        print(f"  [DEGRADED] {path.name} absent: the US corridor is the consumption lane's committed ${lane_us}bn")
        return dict(out, source="[DEGRADED] consumption lane's remittance_flows.csv", us_bn=lane_us,
                    total_bn=None, us_share=None)
    import openpyxl
    rows = list(openpyxl.load_workbook(path, data_only=True).worksheets[0].iter_rows(values_only=True))

    def label(r):
        first = next((c for c in r if isinstance(c, str) and c.strip()), "") if r else ""
        return " ".join(first.replace("\u25cf", " ").split())
    head = next(r for r in rows if r and "Ene-Mar 2022" in r)
    cols = [i for i, c in enumerate(head) if isinstance(c, str) and c.endswith("2024")]
    total = next(r for r in rows if label(r) == "Total")
    us = next(r for r in rows if label(r) == "Estados Unidos")
    tot, usv = sum(float(total[i]) for i in cols) / 1e3, sum(float(us[i]) for i in cols) / 1e3
    gate("banxico_ce167_2024", any("CE167" in label(r) for r in rows[:12]) and len(cols) == 4
         and abs(usv - lane_us) < 5e-4, quarters=len(cols), us_bn=usv, total_bn=tot, lane_us_bn=lane_us)
    return dict(out, source="Banxico SIE CE167 (primary file)", us_bn=usv, total_bn=tot, us_share=usv / tot)


def published_totals(fin):
    """Ruling 5: the real-costs memo's totals at central values on the case, each crime footing on its
    own, as the propagation lane published them (its column for the case). This lane's allocation base
    mixes the footings and is never quoted as a total."""
    t = pd.read_csv(PATHS["real_costs"], dtype={"section": str})
    t = t[t.section == "7"].set_index(["column", "item"])
    v = lambda col, item: float(t.loc[(col, item), CASE["case"]])
    ends = ("low", "high")
    out = dict(equal=[v("hispanic_mixed_group", f"total at central values ({e})") for e in ends],
               equal_fiscal=[v("hispanic", f"fiscal main case ({e})") for e in ends],
               custody=[v("custody", f"total at central values ({e})") for e in ends],
               custody_fiscal=[v("custody", f"fiscal main case ({e})") for e in ends],
               custody_victims=v("custody", "victims' harm, full cost"),
               span=[v("full_span", "low end"), v("full_span", "high end")])
    out["range"] = [out["equal"][0], out["custody"][1]]
    a = fin[CASE["model"]]["ends"]
    bv = pd.read_csv(PATHS["band_variants"]).set_index(["case", "variant"])
    raw = [float(bv.loc[(CASE["case"], "justice_raw_coding"), c]) for c in ("cost_low_bn", "cost_high_bn")]
    note = str(t.loc[("hispanic_mixed_group", "total at central values (low)"), "note"])
    out["equal_victims"] = float(re.search(r"victims ([\d.]+)", note).group(1))
    gate("published_totals_on_their_bands",
         np.allclose(out["custody_fiscal"], [a[e]["cost_bn"] for e in ends], atol=1e-3)
         and np.allclose(out["equal_fiscal"], raw, atol=1e-5), custody_fiscal=out["custody_fiscal"],
         equal_fiscal=out["equal_fiscal"], justice_raw_coding=raw)
    return out


# ================================================================== allocation helpers
def alloc(d, key, total_bn, mask=None):
    """$ per person record, proportional to key among other residents (and mask); sums to total_bn."""
    pw = d.pw.to_numpy()
    m = d.other.to_numpy() if mask is None else (d.other.to_numpy() & mask)
    k = np.where(m, key, 0.0)
    den = float((pw * k).sum())
    if total_bn == 0:
        return np.zeros(len(d))
    if den <= 0:
        raise SystemExit("[BLOCKED] empty distribution key")
    return total_bn * 1e9 * k / den


def alloc_states(d, key, state_bn: dict, mask=None, fallback=None, notes=None, label=""):
    """State totals ($bn by FIPS) spread within each state by key among other residents (and mask).
    A state where that key is empty falls back to `fallback` under the same mask, then to every
    other resident of the state; each fallback is recorded in `notes`."""
    out = np.zeros(len(d))
    st, pw, other = d.st.to_numpy(), d.pw.to_numpy(), d.other.to_numpy()
    for s, tot in state_bn.items():
        if tot == 0:
            continue
        ms = st == s
        mm = ms if mask is None else ms & mask
        for step, (k, m) in enumerate(((key, mm), (fallback, mm), (np.ones(len(d)), ms))):
            if k is None:
                continue
            if (pw * np.where(other & m, k, 0)).sum() > 0:
                out += alloc(d, k, tot, m)
                if step and notes is not None:
                    notes.setdefault("state_fallbacks", []).append(f"{label}: {FIPS.get(s, s)} step {step}")
                break
        else:
            raise SystemExit(f"[BLOCKED] no other residents in state {s}")
    return out


def rake(seed, cell, state, cell_t, state_t, iters=2000, tol=1e-10):
    """Iterative proportional fitting of record totals x (seed x pw) to income-cell and state margins."""
    x = seed.astype(float).copy()
    ct, stt = np.asarray(cell_t, float), np.asarray(state_t, float)
    for it in range(iters):
        cs = np.bincount(cell, weights=x, minlength=len(ct))
        x *= np.divide(ct, cs, out=np.zeros_like(ct), where=cs > 0)[cell]
        ss = np.bincount(state, weights=x, minlength=len(stt))
        x *= np.divide(stt, ss, out=np.zeros_like(stt), where=ss > 0)[state]
        cs = np.bincount(cell, weights=x, minlength=len(ct))
        err = max(np.abs(cs - ct).max() / max(np.abs(ct).max(), 1), 0.0)
        if err < tol:
            return x, it + 1, err
    return x, iters, err


def to_cells100(cells1000):
    return np.asarray(cells1000).reshape(100, 10).sum(axis=1)


# ================================================================== ACS with states (mirrors the base)
def acs_geo(B, acs, arms):
    """The base lane's ACS rent and owner-value channels, kept by state as well as by percentile
    cell (distribute.py acs_channels, same ranking and exposure)."""
    P, H = acs["persons"], acs["households"]
    head = P[P["head"]].drop_duplicates("SERIALNO").set_index("SERIALNO")["p1"]
    H = H.assign(head_p1=H.SERIALNO.map(head))
    H["y"] = H.hinc / np.sqrt(H.np)
    y_of = H.set_index("SERIALNO")["y"]
    ref = P[~P.p1 & ~P.gq].copy()
    ref["y"] = ref.SERIALNO.map(y_of)
    ref["p"] = B.position_rank(ref.y.to_numpy(), ref.pw.to_numpy(), pd.factorize(ref.SERIALNO)[0])
    H["p"] = H.SERIALNO.map(ref.groupby("SERIALNO").p.mean())
    H = H[~(H.p.isna() & H.head_p1.astype(bool))].copy()
    H["cell"] = B.bins(H.p.to_numpy(), B.CELLS)
    alloc_x = B.puma_exposure(H)
    s_nat = B.TARGET_TOTAL / 340.110988e6
    renters = (H.ten.eq(3) & ~H.head_p1.astype(bool)).to_numpy()
    owners = (H.ten.isin([1, 2]) & ~H.head_p1.astype(bool)).to_numpy()
    key = (H.STATE + "|" + H.PUMA).to_numpy()
    st = H.STATE.astype(int).to_numpy()
    out = {}
    for (level, geography), r in arms.items():
        e = r["elasticity"]
        if geography == "metro_local":
            a = alloc_x.assign(f=alloc_x.afact * (1 - (1 - alloc_x.group_share) ** e))
            f = pd.Series(key).map(a.groupby(a.state + "|" + a.puma).f.sum()).to_numpy()
        else:
            f = np.full(len(H), 1 - (1 - s_nat) ** e)
        rent_x = np.where(renters, f * H.rent.to_numpy() * H.wgtp.to_numpy(), 0.0)
        value_x = np.where(owners, f * H.value.to_numpy() * H.wgtp.to_numpy(), 0.0)
        out[(level, geography)] = dict(
            rent_cells=np.bincount(H.cell, weights=rent_x, minlength=B.CELLS),
            value_cells=np.bincount(H.cell, weights=value_x, minlength=B.CELLS),
            rent_state=pd.Series(rent_x).groupby(st).sum().to_dict(),
            value_state=pd.Series(value_x).groupby(st).sum().to_dict())
    return out


# ================================================================== tax keys by government level
def tax_parts(B, d, R, ranking, F, S):
    """distribute.py tax_key split into its federal (CBO shares) and state-local (ITEP rates) parts."""
    civ, pw = d.civ.to_numpy(), d.pw.to_numpy()
    base = np.where(civ, np.maximum(d.money_pc.to_numpy(float), 0), 0.0)
    g = np.where(civ, np.searchsorted(B.CBO_EDGES[1:-1], np.nan_to_num(R["p_all"]), side="right"), -1)
    fed_share = np.array(B.CBO_FED_SHARE[ranking]) / sum(B.CBO_FED_SHARE[ranking])
    sl_group = np.array(B.ITEP_RATE) * np.array(B.CBO_INCOME_SHARE[ranking])
    sl_share = sl_group / sl_group.sum()
    fed, sl = np.zeros(len(d)), np.zeros(len(d))
    for k in range(len(B.CBO_GROUPS)):
        m = g == k
        den = float((pw[m] * base[m]).sum())
        fed[m] = fed_share[k] * base[m] / den
        sl[m] = sl_share[k] * base[m] / den
    return F * fed, S * sl


# ================================================================== key templates (sister lanes)
KEY_TEMPLATES = [
    ("per_person", "every other resident, equally", "CPS ASEC 2025 person weight"),
    ("taxes", "all taxes paid, federal and state-local (ladder 194's convention (a))", "CBO 2022 shares, ITEP rates, CPS money income"),
    ("federal_taxes", "federal taxes paid (CBO 2022 shares by income group)", "CPS money income per capita within group"),
    ("state_local_taxes", "state and local taxes paid (ITEP average rates)", "CPS money income per capita within group"),
    ("workers", "earnings of other-resident workers", "PEARNVAL > 0"),
    ("industry_owner:<NAICS>", "self-employment and farm income of persons whose longest job was in that NAICS (prefix match through the Census 2022 industry crosswalk)", "SEMP_VAL + FRSE_VAL > 0, INDUSTRY"),
    ("industry_worker:<NAICS>", "wage and salary earnings of workers whose longest job was in that NAICS", "WSAL_VAL > 0, INDUSTRY"),
    ("public_school_pupils", "persons aged 5-17, equally (CPS has no school-type item); ':q1'..':q5' restricts to an SPM income quintile as a stand-in for district income", "A_AGE 5-17"),
    ("interstate_movers:<ST>", "persons who lived in state ST a year earlier and now live in another state", "MIG_ST, GESTFIPS, MIGSAME = 2"),
    ("commuters", "workers in metropolitan households, equally", "WORKYN = 1, GTMETSTA = 1"),
    ("renters", "persons in cash-rent households headed by an other resident, one share per household", "H_TENURE = 2, PERRP"),
    ("landlords", "persons in households reporting rental income or loss, by its absolute value (gross rents are not observed)", "HRNTVAL != 0"),
    ("owners", "persons in owner-occupied households headed by an other resident, one share per household", "H_TENURE = 1"),
    ("nh_white_natives", "US-born non-Hispanic white residents, equally", "PEHSPNON = 2, PRDTRACE = 1, PRCITSHP 1-3"),
    ("privately_insured", "persons with private health coverage, equally", "PRIV = 1"),
]
TEMPLATE_NOTE = ("Any template takes '@ST' (postal code) to restrict it to residents of one state, "
                 "for example industry_worker:7225@CA or renters@TX.")


def naics_crosswalk():
    """Census 2022 industry codes with their NAICS equivalents, from the Bureau's crosswalk."""
    if not PATHS["census_industry"].exists():
        SOURCES.mkdir(parents=True, exist_ok=True)
        subprocess.run(["curl", "-sS", "--fail", "-A", "Mozilla/5.0", "-o", str(PATHS["census_industry"]),
                        CENSUS_INDUSTRY_URL], check=True)
    t = pd.read_excel(PATHS["census_industry"], sheet_name="2022 Census Ind Code List ", header=None)
    rows = []
    for _, r in t.iterrows():
        code, naics, desc = str(r[3]).strip(), str(r[4]).strip(), str(r[1]).strip()
        if not re.fullmatch(r"\d{4}", code):
            continue
        for part in naics.split(","):
            part = part.replace("Part of", "").replace("pt.", "").strip()
            base = re.match(r"(\d+)", part)
            if not base:
                continue
            exc = re.findall(r"(\d+)", part.split("exc.")[1]) if "exc." in part else []
            rows.append(dict(census_code=int(code), naics=base.group(1), exclude=" ".join(exc), description=desc))
    x = pd.DataFrame(rows)
    gate("census_industry_crosswalk_parsed", len(x) > 250 and {770, 8680, 7770, 9290}.issubset(set(x.census_code)),
         rows=len(x))
    return x


def census_codes_for(naics: str, xw: pd.DataFrame) -> list[int]:
    hits = []
    for r in xw.itertuples():
        if (r.naics.startswith(naics) or naics.startswith(r.naics)) and not any(
                naics.startswith(e) for e in r.exclude.split() if e):
            hits.append(r.census_code)
    return sorted(set(hits))


def resolve_key(template: str, d: pd.DataFrame, ctx: dict) -> tuple[np.ndarray, np.ndarray, str]:
    """A key template -> (key values, mask over persons, description). Raises ValueError if unknown."""
    t = template.strip()
    state = None
    if "@" in t:
        t, st = t.split("@", 1)
        if st not in POSTAL:
            raise ValueError(f"unknown state in {template}")
        state = POSTAL[st]
    name, _, arg = t.partition(":")
    other = d.other.to_numpy()
    ones = np.ones(len(d))
    if name == "per_person":
        key, mask = ones, other
    elif name == "taxes":
        key, mask = ctx["tax_fed"] + ctx["tax_sl"], other
    elif name == "federal_taxes":
        key, mask = ctx["tax_fed"], other
    elif name == "state_local_taxes":
        key, mask = ctx["tax_sl"], other
    elif name == "workers":
        key, mask = d.earn.to_numpy(), other
    elif name in ("industry_owner", "industry_worker"):
        if not re.fullmatch(r"\d{2,6}", arg):
            raise ValueError(f"NAICS code expected in {template}")
        codes = census_codes_for(arg, ctx["naics"])
        if not codes:
            raise ValueError(f"no Census industry code for NAICS {arg}")
        key = d.semp.to_numpy() if name == "industry_owner" else d.wsal.to_numpy()
        mask = d.INDUSTRY.isin(codes).to_numpy() & other & (key > 0)
    elif name == "public_school_pupils":
        mask = other & d.A_AGE.between(5, 17).to_numpy()
        if arg:
            q = re.fullmatch(r"q([1-5])", arg)
            if not q:
                raise ValueError(f"quintile expected in {template}")
            mask &= ctx["q5"] == int(q.group(1)) - 1
        key = ones
    elif name == "interstate_movers":
        if arg not in POSTAL:
            raise ValueError(f"origin state expected in {template}")
        s = POSTAL[arg]
        mask = other & d.MIG_ST.eq(s).to_numpy() & d.st.ne(s).to_numpy() & d.MIGSAME.eq(2).to_numpy()
        key = ones
    elif name == "commuters":
        key, mask = ones, other & d.metro_worker.to_numpy()
    elif name == "renters":
        key, mask = 1.0 / d.n_other_hh.to_numpy(), other & d.H_TENURE.eq(2).to_numpy() & d.hh_other_ref.to_numpy()
    elif name == "owners":
        key, mask = 1.0 / d.n_other_hh.to_numpy(), other & d.H_TENURE.eq(1).to_numpy() & d.hh_other_ref.to_numpy()
    elif name == "landlords":
        key = np.abs(d.HRNTVAL.to_numpy(float)) / d.n_other_hh.to_numpy()
        mask = other & (key > 0)
    elif name == "nh_white_natives":
        key, mask = ones, other & d.race5.eq("nh_white").to_numpy() & d.native.to_numpy()
    elif name == "privately_insured":
        key, mask = ones, other & d.PRIV.eq(1).to_numpy()
    else:
        raise ValueError(f"unknown key template {template}")
    if state is not None:
        mask = mask & (d.st.to_numpy() == state)
    if (d.pw.to_numpy() * np.where(mask, key, 0)).sum() <= 0:
        raise ValueError(f"key {template} is empty on CPS ASEC 2025")
    return key, mask, template


def load_key_map():
    km = pd.read_csv(HERE / "key_map.csv", dtype=str).fillna("")
    return km


def map_row_to_key(lane: str, row: dict, km: pd.DataFrame) -> tuple[str, str]:
    """(key template, how it was chosen). An explicit `key` column wins; then key_map.csv patterns
    for the lane (first match); '' if no defensible key."""
    explicit = str(row.get("key", "") or "").strip()
    if explicit:
        return explicit, "key column"
    text = f"{row.get('group', '')} | {row.get('channel', '')}"
    for r in km[(km.lane == lane) | (km.lane == "*")].itertuples():
        if re.search(r.group_regex, str(row.get("group", "")), flags=re.I) and (
                not r.channel_regex or re.search(r.channel_regex, str(row.get("channel", "")), flags=re.I)):
            key = r.key
            if "<NAICS>" in key:
                code = re.search(r"NAICS\s*:?\s*(\d{2,6})", text, flags=re.I)
                if not code:
                    code_word = [c for w, c in INDUSTRY_WORDS.items() if re.search(w, text, flags=re.I)]
                    if not code_word:
                        return "", f"key_map row '{r.group_regex}' needs a NAICS code"
                    key = key.replace("<NAICS>", code_word[0])
                else:
                    key = key.replace("<NAICS>", code.group(1))
            if "<ST>" in key:
                named = [c for w, c in STATE_WORDS.items() if re.search(w, text, flags=re.I)]
                st = re.search(r"\b(" + "|".join(POSTAL) + r")\b", text)
                key = key.replace("<ST>", named[0] if named else (st.group(1) if st else r.default_state))
            return key, f"key_map: {r.note or r.group_regex}"
    return "", "no key_map pattern"


INDUSTRY_WORDS = {r"restaurant|eating place|food service": "7225", r"food truck|mobile food": "722330",
                  r"construction|contractor|trades": "23", r"landscap": "561730", r"janitor": "561720",
                  r"private household|domestic": "814", r"agricultur|farm": "11", r"grocer": "4451"}
STATE_WORDS = {r"californ|los angeles|\bcity of la\b|\bL\.A\.": "CA", r"texas": "TX", r"new york": "NY",
               r"illinois": "IL", r"arizona": "AZ", r"florida": "FL"}


REGIONS = {"Northeast": (1, 2), "Midwest": (3, 4), "South": (5, 6, 7), "West": (8, 9)}


def counterfactual_is_absence(text) -> bool:
    """True when a sister row's counterfactual is the account's: the group (or its pupils) absent."""
    t = str(text)
    return bool(ABSENCE.search(t)) and not NOT_ABSENCE.search(t)


def check_sister_counterfactuals(tbl: pd.DataFrame):
    """Gate: every allocated sister row is on the account's counterfactual; the run stops otherwise."""
    alloc_ = tbl[tbl.status == "allocated"] if "status" in tbl else tbl.iloc[0:0]
    bad = [f"{r.lane}:{r.row}" for r in alloc_.itertuples() if not counterfactual_is_absence(r.counterfactual)]
    gate("sister_allocated_rows_on_account_counterfactual", not bad, allocated=len(alloc_), off_counterfactual=bad)


def sister_other_counterfactuals(tbl: pd.DataFrame) -> pd.DataFrame:
    """Sister rows whose counterfactual is not the group's absence, each under its own counterfactual;
    they are never in a net."""
    cols = ["lane", "row", "counterfactual", "group", "channel", "direction", "bn_low", "bn_central", "bn_high",
            "relation_to_account", "basis", "status"]
    if "counterfactual_is_absence" not in tbl:
        return pd.DataFrame(columns=cols)
    return tbl[tbl.counterfactual_is_absence.eq(False)][cols].sort_values(["lane", "row"])


def sister_file(lane_dir: str, name: str, commits: dict | None) -> bytes | None:
    """A sister lane's file: from git at the lane's pinned commit when `commits` names the lane (an
    absent file there stops the run), else from the working tree (None when absent)."""
    p = FISCAL / lane_dir / name
    if commits and lane_dir in commits:
        return git_show(str(p.relative_to(ROOT)), commits[lane_dir])
    return p.read_bytes() if p.exists() else None


def lane_verdict(text: bytes | None) -> str:
    """First line of the sister lane's RESULT.md as read (its rows are provisional until final)."""
    if text is None:
        return "no RESULT.md"
    for line in text.decode().splitlines():
        if line.strip():
            return line.strip()[:160]
    return "empty RESULT.md"


def ingest_sisters(d, ctx, km, lanes=None, commits=None, role_only=None):
    """Read each sister lane's winners_losers_rows.csv if present, at the lane's commit in `commits`
    when given. Returns (role table, person-level
    amounts of the allocated rows). A row is allocated only if it is priced, a gain or a loss, beside
    the account, on the account's counterfactual (the group's or its pupils' absence) and mapped to a
    key template; every other row stays in the role table. A lane in `role_only` (lane -> why) keeps
    the rows it would have allocated in the role table under this case. When the lane
    also gives a regional breakdown of an allocated row (group '<group>:region=<Census region>',
    relation 'overlaps:<channel>') that sums to it, the row is spread by those regional shares."""
    role_only = role_only or {}
    rows, amounts, used = [], {}, {}
    pw = d.pw.to_numpy()
    region_of = d.st.map(DIVISION).map({v: k for k, vs in REGIONS.items() for v in vs}).to_numpy()
    for lane_dir, rid in (lanes or SISTERS).items():
        raw = sister_file(lane_dir, "derived/winners_losers_rows.csv", commits)
        verdict = lane_verdict(sister_file(lane_dir, "RESULT.md", commits))
        if raw is None:
            rows.append(dict(lane=lane_dir, registry_id=rid, status="pending", note="file absent at run time",
                             lane_verdict=verdict))
            continue
        t = pd.read_csv(io.BytesIO(raw), dtype=str).fillna("")
        missing = [c for c in SISTER_COLUMNS if c not in t.columns]
        if missing:
            rows.append(dict(lane=lane_dir, registry_id=rid, status="pending", lane_verdict=verdict,
                             note=f"file present but missing columns {missing}", sha256=sha(raw)))
            continue
        first = len(rows)
        for i, r in t.iterrows():
            r = r.to_dict()
            rec = dict(lane=lane_dir, registry_id=rid, row=i, sha256=sha(raw), lane_verdict=verdict,
                       **{c: r[c] for c in SISTER_COLUMNS})
            rec["counterfactual_is_absence"] = counterfactual_is_absence(r["counterfactual"])
            if "key" in t.columns:
                rec["key_column"] = r["key"]
            vals = {}
            for lev in LEVELS:
                try:
                    vals[lev] = float(r[f"bn_{lev}"]) if str(r[f"bn_{lev}"]).strip() != "" else np.nan
                except ValueError:
                    vals[lev] = np.nan
            direction = str(r["direction"]).strip().lower()
            relation = str(r["relation_to_account"]).strip().lower()
            # Two conventions occur. A row whose central is zero or positive gives amounts along its
            # direction (a loss of 16, with a low end of -2 meaning a gain of 2). A loss row with a
            # negative central gives signed changes to the payers (negative = worse off). A gain row
            # with a negative central is ambiguous and stays in the role table.
            signed = not np.isnan(vals["central"]) and vals["central"] < 0
            if np.isnan(vals["central"]) or str(r["basis"]).strip().lower() == "unpriced":
                rec.update(status="role_only", note="unpriced or no central value")
            elif direction not in ("gain", "loss"):
                rec.update(status="role_only", note=f"direction '{direction}' is not gain or loss")
            elif signed and direction == "gain":
                rec.update(status="role_only", note="a gain with a negative central value is ambiguous")
            elif relation == "inside" or relation.startswith("overlaps"):
                rec.update(status="role_only", note=f"relation '{relation}': inside the account or overlapping; "
                                                    "shown, never added to the nets")
            elif not rec["counterfactual_is_absence"]:
                rec.update(status="role_only", note="its counterfactual is not the group's absence, the account's; "
                                                    "listed under its own in sister_other_counterfactuals.csv, "
                                                    "never in a net")
            elif lane_dir in role_only:
                rec.update(status="role_only", note=role_only[lane_dir])
            else:
                key, how = map_row_to_key(lane_dir, r, km)
                if not key:
                    rec.update(status="role_only", note=f"no defensible key ({how})")
                else:
                    try:
                        k, m, _ = resolve_key(key, d, ctx)
                    except ValueError as e:
                        rec.update(status="role_only", note=f"key {key} rejected: {e}")
                    else:
                        sign = 1.0 if direction == "gain" else -1.0
                        cid = f"sister:{rid}:{i}"
                        vv = {lev: (vals[lev] if not np.isnan(vals[lev]) else vals["central"]) for lev in LEVELS}
                        amt = {lev: (vv[lev] if signed else sign * vv[lev]) for lev in LEVELS}
                        amounts[cid] = {lev: alloc(d, k, amt[lev], m) for lev in LEVELS}
                        rec["values_read_as"] = "signed changes" if signed else "amounts along the direction"
                        rec["key_records"] = int((m & (k > 0)).sum())
                        if rec["key_records"] < 30:
                            note_thin = f"; thin key: {rec['key_records']} CPS records"
                        else:
                            note_thin = ""
                        used[cid] = (k, m, amt, str(r["group"]).strip(), str(r["channel"]).strip())
                        pop = float((pw * m).sum() / 1e6)
                        try:
                            ratio = pop / float(r["population_m"])
                        except (ValueError, ZeroDivisionError):
                            ratio = np.nan
                        note = "beside the account; proposed"
                        if lane_dir in LANE_LABELS:
                            note += f"; {LANE_LABELS[lane_dir]}"
                        if np.isfinite(ratio) and not 0.5 <= ratio <= 2.0:
                            note += (f"; the key covers {pop:.2f}m persons against the row's {r['population_m']}m "
                                     "(the row's group is not identifiable in CPS, or the payers differ from it)")
                        rec.update(status="allocated", key=key, key_chosen_by=how, channel_id=cid,
                                   key_population_m=pop, key_population_over_row=ratio, note=note + note_thin)
            rows.append(rec)
        # Regional breakdowns of allocated rows.
        for cid, (k, m, amt, grp, chan) in list(used.items()):
            if not cid.startswith(f"sister:{rid}:"):
                continue
            parts = {}
            for rec in rows[first:]:
                g = str(rec.get("group", ""))
                if (g.startswith(f"{grp}:region=") and str(rec.get("relation_to_account", "")).strip()
                        == f"overlaps:{chan}"):
                    try:
                        parts[g.split("region=", 1)[1].strip()] = float(rec["bn_central"])
                    except ValueError:
                        pass
            if not parts:
                continue
            rec = next(x for x in rows[first:] if x.get("channel_id") == cid)
            ok = set(parts) <= set(REGIONS) and np.isclose(abs(sum(parts.values())), abs(amt["central"]), rtol=0.01,
                                                           atol=1e-6)
            if not ok:
                rec["note"] += "; regional breakdown present but not used (regions unknown or not summing)"
                continue
            tot = sum(parts.values())
            amounts[cid] = {lev: sum(alloc(d, k, amt[lev] * v / tot, m & (region_of == reg))
                                     for reg, v in parts.items()) for lev in LEVELS}
            rec["note"] += "; spread by the lane's regional breakdown (" + ", ".join(
                f"{reg} {v / tot:.1%}" for reg, v in parts.items()) + ")"
    for cid, (k, m, amt, grp, chan) in used.items():
        for lev in LEVELS:
            got = float((pw * amounts[cid][lev]).sum() / 1e9)
            gate(f"closure_{cid}_{lev}", np.isclose(got, amt[lev], rtol=1e-9, atol=1e-9), persons=got, row=amt[lev])
    tbl = pd.DataFrame(rows)
    check_sister_counterfactuals(tbl)
    return tbl, amounts


# ================================================================== inputs the base lane reads
def production_rows(B, d, nest, case):
    """A case's production scenarios on its engine's grid (CASES production): the base lane's row-4 re-solve
    (row4_nest_rows) of the grid it reproduces and, where the case's grid adds to another case's (the base lane's
    LATER_CASES grid_base: October 5 on September 29's), that addition (lineage_rows). The base lane gates both against
    the grids. Returns the scenarios this lane reads (the GDP rows at the row-4 factor), the base lane's record and the
    case's production entry from fiscal_totals."""
    prod = B.fiscal_totals(case)["adopted"]["production"]
    lc = B.LATER_CASES[case]
    grid_base = getattr(lc, "grid_base", None)
    rows4, info4 = B.row4_nest_rows(d, nest, prod, grid_base or lc.lane)
    if grid_base:
        rows4, info4["lineage"] = B.lineage_rows(d, rows4, grid_base, lc.lane)
    f4 = info4["gdp_factor"]["row4"]
    own = dict(central=B.pick(rows4, "below_ba", 2.0, 1.0, np.inf), account=B.pick(rows4, "hs_or_less", 2.0, 1.0, np.inf),
               eps3_bb=B.pick(rows4, "below_ba", 2.0, 1.0, 3.0), eps3_hs=B.pick(rows4, "hs_or_less", 2.0, 1.0, 3.0))
    own.update(account_gdp=B.as_gdp(own["account"], f4), eps3_hs_gdp=B.as_gdp(own["eps3_hs"], f4))
    return own, info4, prod


def base_inputs(B, d):
    B.verify_published_text()
    ncvs_ok = B.verify_ncvs_text()
    I = dict(ncvs_verified=ncvs_ok)
    I["fiscal23"] = B.fiscal_totals()
    I["F_total"], I["S_total"] = B.bea_totals()
    I["rates"] = B.ncvs_rates()
    nest = B.nest_rows()
    I["central"] = B.pick(nest, "below_ba", 2.0, 1.0, np.inf)
    I["account"] = B.pick(nest, "hs_or_less", 2.0, 1.0, np.inf)
    I["eps3_bb"] = B.pick(nest, "below_ba", 2.0, 1.0, 3.0)
    I["eps3_hs"] = B.pick(nest, "hs_or_less", 2.0, 1.0, 3.0)
    gate("account_production_term", np.isclose(I["account"].private_plus_receipts_bn, I["fiscal23"]["PF_cash"], rtol=1e-9),
         nest=I["account"].private_plus_receipts_bn, account=I["fiscal23"]["PF_cash"])
    # GDP normalization rows of the same scenarios (the base lane keeps cash only).
    s = pd.read_csv(B.PATHS["nest"])
    s = s[(s.excluded_capital_owner_share == 0) & (s.nest_option == "A_by_nativity") & (s.proxy == "PEARNVAL")
          & (s.labor_supply_elasticity == 0) & (s.capital_tax_retention == 1.0) & (s.labor_share == 0.65)
          & (s.sigma == 2.0) & (s.capital_adjustment == 1.0) & (s.normalization == "gdp")]
    I["account_gdp"] = s[(s.split == "hs_or_less") & (s.sigma_NI == np.inf)].iloc[0]
    I["eps3_hs_gdp"] = s[(s.split == "hs_or_less") & (s.sigma_NI == 3.0)].iloc[0]
    # The production scenarios by case. A case whose engine grid is on the account's row-4 weights (CASES production,
    # September 29 on) reads the base lane's row-4 re-solve (production_rows, gated there against the case's grid at
    # both normalizations); a case without such a grid keeps the published rows. From October 5 the case before has a
    # grid of its own too, so each of the two reads its own rows. I's own entries are the run's case.
    SCENARIOS = ("central", "account", "eps3_bb", "eps3_hs", "account_gdp", "eps3_hs_gdp")
    published = {k: I[k] for k in SCENARIOS}
    I["nest"] = {CASE["prev"]["case"]: published, CASE["case"]: published}
    for c in (CASE["prev"], CASE):
        if not c.get("production"):
            continue
        own, info4, prod = production_rows(B, d, nest, c["case"])
        # The account's split is the engine's production cell at both band ends (case_ends' P and F there). The case's
        # gate keeps the name it had when only the case had a grid.
        got = {end: float(own["account" if v["normalization"] == "cash" else "account_gdp"].private_plus_receipts_bn)
               for end, v in prod["ends"].items()}
        want = {end: v["case"]["P_bn"] + v["case"]["F_bn"] for end, v in prod["ends"].items()}
        gate("account_production_term_case_grid" if c is CASE else f"account_production_term_{c['case']}_grid",
             all(abs(got[e] - want[e]) < 1e-6 for e in got), row4=got, case_grid=want,
             normalization={end: v["normalization"] for end, v in prod["ends"].items()})
        I["nest"][c["case"]] = own
        if c is CASE:
            I.update(own)
            I["production_row4"] = info4
        else:
            I["production_row4_prev"] = info4
    if "lineage" in I.get("production_row4", {}):
        # The case's grid adds to the case before's: its re-solve before the addition is on the same grid file, weights
        # and GDP factor as the case before's own, so the addition is all that separates the two cases' scenarios. From
        # October 7 the case before adds to a grid too (October 5 and October 7 both re-solve September 29's grid with
        # their own added people), so the two additions share their base and their difference separates the cases.
        p, q = I["production_row4_prev"], I["production_row4"]
        base_of_prev = p["lineage"]["base"] if "lineage" in p else CASES[CASE["prev"]["case"]]["lane"]
        gate("production_rows_add_to_the_previous_case_s", q["lineage"]["base"] == base_of_prev
             and p["grid"] == q["grid"] and p["factors"] == q["factors"] and p["gdp_factor"] == q["gdp_factor"],
             base=q["lineage"]["base"], previous_lane=CASES[CASE["prev"]["case"]]["lane"], grid=q["grid"]["file"],
             **({"previous_case_s_base": p["lineage"]["base"]} if "lineage" in p else {}))
    I["basis"] = {sp: B.wage_basis(d, sp) for sp in ("below_ba", "hs_or_less")}
    pw = d.pw.to_numpy()
    branches = pd.read_csv(B.PATHS["branches"])
    for split in I["basis"]:
        for (tag, c), e in I["basis"][split].items():
            name = "native_non_union" if tag == "native" else "other_foreign_born"
            ref = branches[(branches.proxy == "PEARNVAL") & (branches.split == split) & (branches.skill == c)
                           & (branches.branch == name)].earnings_estimate.iloc[0]
            gate(f"wage_base_{split}_{tag}_cell{c}", np.isclose((pw * e).sum(), ref, rtol=1e-9),
                 cps=(pw * e).sum() / 1e9, nest=ref / 1e9)
    ha = pd.read_csv(B.PATHS["housing_arms"]).drop_duplicates(["arm", "level", "form", "geography", "ownership"])
    ha = ha[(ha.arm == "long_run") & (ha.form == "A") & (ha.ownership == "central")]
    I["arms"] = {(r.level, r.geography): r._asdict() for r in ha.itertuples()}
    acs = B.acs_extract()
    I["acs"] = B.acs_channels(acs, I["arms"])
    I["acs_geo"] = acs_geo(B, acs, I["arms"])
    for k in I["arms"]:
        gate(f"acs_geo_mirrors_base_{k[0]}_{k[1]}", np.allclose(I["acs_geo"][k]["rent_cells"], I["acs"][k]["rent_cells"],
             rtol=1e-12, atol=1e-3) and np.allclose(I["acs_geo"][k]["value_cells"], I["acs"][k]["value_cells"], rtol=1e-12, atol=1e-3))
    I["scf"], I["scf_info"] = B.scf_cells()
    off = pd.read_csv(B.PATHS["crime_offence"]).set_index("offence")
    serious = ["Murder", "Rape/sexual assault", "Robbery", "Aggravated assault"]
    I["serious_share"] = float(off.loc[serious, "cost_full"].sum() / off.loc["Total", "cost_full"])
    htot = d.HTOTVAL.to_numpy(float)
    m12 = d.civ.to_numpy() & (d.A_AGE.to_numpy() >= 12)
    p12 = np.full(len(d), np.nan)
    p12[m12] = B.position_rank(htot[m12], pw[m12])
    I["keys_rank"], _ = B.crime_key(d, p12, I["rates"], "rank")
    unc = pd.read_csv(B.PATHS["uncompensated"])
    eq = unc[unc.use_intensity == 1.0]
    I["unreimbursed"] = {"low": float(eq.outside_accounts_bn.min()), "high": float(eq.outside_accounts_bn.max())}
    I["unreimbursed"]["central"] = (I["unreimbursed"]["low"] + I["unreimbursed"]["high"]) / 2
    cex = pd.read_csv(B.PATHS["cex"])
    cex = cex[(cex.arm == "published_jpe_2008") & (cex.shock == "lf_adjusted") & (cex.scope == "narrow_immigrant_intensive")].iloc[0]
    I["cex_q"] = np.array([cex[f"loss_bn_{k}"] for k in ("q1_lowest", "q2_second", "q3_third", "q4_fourth", "q5_highest")])
    I["R_money"] = B.rank_frame(d, "money")
    I["R_spm"] = B.rank_frame(d, "spm")
    if CASE.get("capped"):
        # The capped programs' eligible non-recipients: the base lane's keys, its rules re-verified against the
        # cached texts; and the base lane's case ends, which fiscal_totals reads from its working tree.
        I["capped_texts"] = B.verify_capped_text()
        I["capped_keys"], I["capped_info"] = B.capped_keys(d)
        rel = f"{BASE_REL}/derived/{B.LATER_CASES[CASE['case']].ends}"
        gate(f"base_case_ends_committed_at_{CASE['base']}", (ROOT / rel).read_bytes() == git_show(rel), file=rel)
    return I


def crime_split(B, d, keys, total, s_share):
    return B.per_person(d, keys["serious"], -total * s_share) + B.per_person(d, keys["simple"], -total * (1 - s_share))


def consumer_side_view(d, I):
    pw, other = d.pw.to_numpy(), d.other.to_numpy()
    qm = I["R_money"]["q5"]
    cx = np.zeros(len(d))
    for q in range(5):
        m = other & (qm == q)
        cx[m] = I["cex_q"][q] * 1e9 / pw[m].sum()
    return cx


# ================================================================== regression: the base lane's tables
def regression(B, d, I, case):
    """The base lane's central channels rebuilt by this lane's code, with the fiscal channel at
    fiscal_totals(case) A_mid plus the base's central induced receipts, compared with that lane's
    channel_by_quintile.csv on the same case (at the case's base commit in CASES)."""
    commit, sub = CASES[case]["base"], CASES[case].get("base_dir")
    expected = pd.read_csv(io.BytesIO(git_show(lane_rel(f"{BASE_REL}/derived", sub, "channel_by_quintile.csv"), commit)))
    held = json.loads(git_show(lane_rel(f"{BASE_REL}/derived", sub, "inputs.json"), commit))["fiscal"]
    fa = B.fiscal_totals(case)["adopted"]
    gate(f"regression_target_is_{case}", held.get("case", "sept23") == case
         and np.isclose(held["adopted"]["A_mid"], fa["A_mid"], atol=1e-9), target_case=held.get("case", "sept23"),
         target_A_mid=held["adopted"]["A_mid"], A_mid=fa["A_mid"])
    rows_ = I["nest"][case]            # the case's production scenarios (row-4 for a case with a production grid)
    F_c = float(rows_["central"].induced_current_receipts_bn)
    a_c = I["arms"][("central", "metro_local")]
    crime_custody = crime_inputs(B)["custody"]
    # From September 27 the base lane's fiscal channel is the budget's part of A (the capped programs leave
    # it for their eligible non-recipients) and splits into cash and the resource cost (the capital return);
    # from September 29 public housing is capped too (the base's CAPPED_KEY_OF) and the pension accrual leaves the
    # cash part for its own channel.
    capped = "capped_programs" in fa
    budget_mid = fa["A_mid"]
    ACC_mid = (fa["pension_accrual"][0] + fa["pension_accrual"][1]) / 2 if "pension_accrual" in fa else 0.0
    if capped:
        programs = {k: I["capped_keys"][getattr(B, "CAPPED_KEY_OF", {}).get(k, k)] for k in fa["capped_programs"]}
        D_mid = sum((v[0] + v[1]) / 2 for v in fa["capped_programs"].values())
        K_mid = (fa["capital_return"][0] + fa["capital_return"][1]) / 2
        budget_mid = fa["A_mid"] + D_mid

        def displaced(lines=tuple(programs)):
            return sum(B.per_person(d, programs[k], -(fa["capped_programs"][k][0] + fa["capped_programs"][k][1]) / 2)
                       for k in lines)
    rows = []
    for measure in B.MEASURES:
        R = I["R_money"] if measure == "money" else I["R_spm"]
        ranking = "after" if measure == "spm" else "before"
        tax, _ = B.tax_key(d, R, ranking, I["F_total"], I["S_total"])
        ch = {}
        for conv, key in (("a", tax), ("b", np.ones(len(d)))):
            ch[f"fiscal_{conv}"] = B.per_person(d, key, budget_mid + F_c)
        ch["wages"] = B.wage_delta(I["basis"]["below_ba"], rows_["central"], True)
        ch["renters"] = -B.spread_cells(I["acs"][("central", "metro_local")]["rent_cells"], R, d)
        tot = a_c["other_renters_extra_rent_bn"] + a_c["net_other_residents_welfare_bn"]
        li = B.per_person(d, B.spread_cells(I["acs"]["intp_cells"], R, d), tot)
        ls = B.per_person(d, B.spread_cells(I["scf"], R, d), tot)
        ch["landlords"] = (li + ls) / 2
        ch["crime"] = crime_split(B, d, I["keys_rank"], crime_custody, I["serious_share"])
        ch["unreimbursed_care"] = B.per_person(d, d.PRIV.eq(1).to_numpy().astype(float), -I["unreimbursed"]["central"])
        ch["housing_net"] = ch["renters"] + ch["landlords"]
        parts = ["wages", "renters", "landlords", "crime", "unreimbursed_care"]
        if capped:
            ch["displaced_beneficiaries"] = displaced()
            parts.append("displaced_beneficiaries")
            for conv, key in (("a", tax), ("b", np.ones(len(d)))):
                ch[f"fiscal_cash_{conv}"] = B.per_person(d, key, budget_mid + K_mid + ACC_mid + F_c)
                ch[f"fiscal_resource_{conv}"] = B.per_person(d, key, -K_mid)
                if "pension_accrual" in fa:
                    ch[f"fiscal_accrual_{conv}"] = B.per_person(d, key, -ACC_mid)
            for k in programs:
                ch[f"displaced_{k}"] = displaced((k,))
        for conv in ("a", "b"):
            ch[f"TOTAL_{conv}"] = ch[f"fiscal_{conv}"] + sum(ch[p] for p in parts)
        ch["wages_eps3"] = B.wage_delta(I["basis"]["below_ba"], rows_["eps3_bb"], True)
        ch["wages_account_split"] = B.wage_delta(I["basis"]["hs_or_less"], rows_["account"], True)
        ch["consumer_prices_side_view"] = consumer_side_view(d, I)
        for name, delta in ch.items():
            q = B.by_bin(delta, d, R)
            exp = expected[(expected.measure == measure) & (expected.channel == name)].set_index("quintile")
            if len(exp) != 6:
                raise SystemExit(f"[BLOCKED] base channel {name}/{measure} not in channel_by_quintile.csv")
            for k in range(6):
                got = dict(bn=q["net"].sum(), loss_bn=q["loss"].sum(), gain_bn=q["gain"].sum()) if k == 0 else \
                    dict(bn=q["net"][k - 1], loss_bn=q["loss"][k - 1], gain_bn=q["gain"][k - 1])
                for col, v in got.items():
                    rows.append(dict(measure=measure, channel=name, quintile=k, column=col,
                                     base=float(exp.loc[k, col]), lane=float(v), diff=float(v - exp.loc[k, col])))
    reg = pd.DataFrame(rows)
    gate(f"regression_{case}_channel_by_quintile", reg["diff"].abs().max() <= 0.01,
         max_abs_diff_bn=float(reg["diff"].abs().max()), cells=len(reg), channels=int(reg.channel.nunique()))
    return reg


SHARED = [  # this frame's channel, the base lane's channel, why their quintile tables differ
    ("fiscal_a", "fiscal_a", "total: the account's own F by band end (mean of 13.56 GDP and 8.95 cash) against the "
     "base's 9.56 (below-BA split), and the future taxpayers' part not allocated; key: federal part by federal "
     "taxes, state-local part by state-local taxes within the group's states, against all taxes nationally"),
    ("fiscal_b", "fiscal_b", "total as fiscal_a; key: per person, the state-local part within the group's states"),
    ("fiscal_a_pooled_national", "fiscal_a", "same key as the base; total only (F and the future taxpayers' part)"),
    ("fiscal_b_pooled_national", "fiscal_b", "same key as the base; total only (F and the future taxpayers' part)"),
    ("wages", "wages", "the account's split (high school or less; the production term P, GDP normalization at "
     "the low-cost end) against the base's below-BA split"),
    ("wages_below_ba_cash", "wages", "the base's own channel (control: must match)"),
    ("renters", "renters", "same central total (metro-local central); raked to ACS extra rent by state as well "
     "as income cell"),
    ("landlords", "landlords", "same central total; CPS rental-income holders raked to the base's income profile "
     "and the rent states, against the base's ACS-INTP/SCF profile without states"),
    ("crime_victims", "crime", "total: decision 4's 30.93 against the base's custody footing 32.34; key: the "
     "group's states"),
    ("crime_victims_custody_footing", "crime", "same total (custody footing); the group's states only"),
    ("crime_victims_national_key", "crime", "same key as the base; total only (30.93 against 32.34)"),
    ("unreimbursed_care", "unreimbursed_care", "same central total; the states of the group's uninsured"),
]
SHARED_CAPPED = [  # from September 27
    ("fiscal_cash_a", "fiscal_cash_a", "total: the cash part financed today (the future taxpayers' part and F as in "
     "fiscal_a); key: federal part by federal taxes, state-local part by state-local taxes within the group's states"),
    ("fiscal_resource_a", "fiscal_resource_a", "same total (the capital return at the band ends' mean); key: federal "
     "part by federal taxes, state-local part within the group's states, against all taxes nationally"),
    ("displaced_beneficiaries", "displaced_beneficiaries", "same total and the base's capped_keys (control: must match)"),
]


def frame_vs_base(B, d, I, ch):
    """This frame's central channels against the base lane's channel_by_quintile.csv on the case (its
    base commit), SPM quintiles of other residents; quintile 0 is the total."""
    base = pd.read_csv(io.BytesIO(git_show(lane_rel(f"{BASE_REL}/derived", CASE.get("base_dir"), "channel_by_quintile.csv"),
                                           CASE["base"])))
    base = base[base.measure == "spm"]
    rows = []
    for mine, theirs, why in SHARED + (SHARED_CAPPED if CASE.get("capped") else []):
        q = B.by_bin(ch[mine]["central"], d, I["R_spm"])
        exp = base[base.channel == theirs].set_index("quintile").bn
        for k in range(6):
            v = float(q["net"].sum() if k == 0 else q["net"][k - 1])
            rows.append(dict(channel=mine, base_channel=theirs, quintile=k, frame_bn=v, base_bn=float(exp.loc[k]),
                             diff_bn=v - float(exp.loc[k]),
                             frame_share=v / float(q["net"].sum()) if k else 1.0,
                             base_share=float(exp.loc[k] / exp.loc[0]) if k else 1.0, why=why))
    out = pd.DataFrame(rows)
    ctl = out[out.channel == "wages_below_ba_cash"]
    gate("frame_vs_base_control_wages_below_ba", ctl.diff_bn.abs().max() < 1e-6, max_abs_diff_bn=float(ctl.diff_bn.abs().max()))
    if CASE.get("capped"):
        ctl = out[out.channel == "displaced_beneficiaries"]
        gate("frame_vs_base_control_displaced_beneficiaries", ctl.diff_bn.abs().max() < 1e-6,
             max_abs_diff_bn=float(ctl.diff_bn.abs().max()))
    return out


# ================================================================== the person frame
BESIDE = ["renters", "landlords", "crime_victims", "unreimbursed_care", "congestion", "preferences_group_part", "mobility"]


def rake_channel(B, d, R, key, mask, cell_t, state_t: dict, fallback=None, label="", notes=None):
    """Record totals x for other residents matching income-cell (100 SPM percentile cells) and state
    margins, seeded by key among mask; cells or states with a target but no seed use `fallback`."""
    other, pw = d.other.to_numpy(), d.pw.to_numpy()
    idx = np.where(other)[0]
    cell = B.bins(R["p_other"][idx], 100)
    states = sorted(FIPS)
    sidx = pd.Series(range(len(states)), index=states)
    st = sidx.loc[d.st.to_numpy()[idx]].to_numpy()
    st_t = np.array([state_t.get(s, 0.0) for s in states], float)
    ct = np.asarray(cell_t, float)
    gate(f"rake_margins_consistent_{label}", np.isclose(st_t.sum(), ct.sum(), rtol=1e-9), states=st_t.sum(), cells=ct.sum())
    seed = pw[idx] * np.where(mask[idx], key[idx], 0.0)
    for margin, grp, tgt in (("cell", cell, ct), ("state", st, st_t)):
        have = np.bincount(grp, weights=seed, minlength=len(tgt))
        need = (tgt != 0) & (have <= 0)
        if need.any():
            fb = fallback if fallback is not None else np.ones(len(d))
            rows = need[grp]
            seed[rows] = pw[idx][rows] * fb[idx][rows]
            if notes is not None:
                notes.setdefault("rake_fallbacks", []).append(f"{label}: {int(need.sum())} {margin}(s) seeded by the fallback")
    x, it, err = rake(seed, cell, st, ct, st_t)
    ss = np.bincount(st, weights=x, minlength=len(st_t))
    cs = np.bincount(cell, weights=x, minlength=len(ct))
    gate(f"rake_converged_{label}", np.allclose(cs, ct, rtol=1e-8, atol=1.0) and np.allclose(ss, st_t, rtol=1e-8, atol=1.0),
         iterations=it, max_cell_gap=float(np.abs(cs - ct).max()), max_state_gap=float(np.abs(ss - st_t).max()))
    out = np.zeros(len(d))
    out[idx] = x / pw[idx]
    return out


def build_frame(B, d, I, fin, fedsplit, deficit, notes):
    pw, other, tgt = d.pw.to_numpy(), d.other.to_numpy(), d.target.to_numpy()
    st = d.st.to_numpy()
    R = I["R_spm"]
    tax_fed, tax_sl = tax_parts(B, d, R, "after", I["F_total"], I["S_total"])
    tax_all, _ = B.tax_key(d, R, "after", I["F_total"], I["S_total"])
    gate("tax_parts_add_to_base_key", np.allclose(tax_fed + tax_sl, tax_all, rtol=1e-12, atol=0))
    ones = np.ones(len(d))
    ch, totals, meta = {}, {}, {}

    def put(name, arrays, expect):
        ch[name] = arrays
        totals[name] = expect

    # ---- group geography: where the state-local cost, victims' harm and uncompensated care arise
    w_state = pd.Series(pw[tgt]).groupby(st[tgt]).sum()
    w_state = (w_state / w_state.sum()).to_dict()
    w_unins = pd.Series((pw * d.uninsured_py.to_numpy())[tgt]).groupby(st[tgt]).sum()
    w_unins = (w_unins / w_unins.sum()).to_dict()
    meta["group_state_share"] = {FIPS[s]: v for s, v in w_state.items()}

    # ---- fiscal: A + F by band end, split federal / state-local, deficit-financed part apart. A is
    # fiscal_totals(case) (one definition with the base lane); F is the account's own.
    case = fin[CASE["model"]]
    e = case["ends"]
    A1 = case["A_one_definition"]
    cost = {end: -(A1[end] + e[end]["F_bn"]) for end in ("low", "high")}
    for end in ("low", "high"):
        lane = fedsplit[(CASE["model"], end, "central")]["cost_bn"]
        gate(f"fiscal_cost_matches_debt_lane_{end}", abs(cost[end] - lane) < 1e-3, frame=cost[end], debt_lane=lane,
             diff=cost[end] - lane)
    cost["central"] = (cost["low"] + cost["high"]) / 2
    fed = {end: fedsplit[(CASE["model"], end, "central")]["federal_bn"] for end in ("low", "high")}
    fed["central"] = (fed["low"] + fed["high"]) / 2
    dsh = deficit["share"]
    if not CASE.get("capped"):
        fisc = {L: dict(cost=cost[L], federal=fed[L], state_local=cost[L] - fed[L], future=dsh * fed[L],
                        federal_today=(1 - dsh) * fed[L]) for L in LEVELS}
    else:
        # Three financing columns (the debt lane's split). Cash: fed is its federal part, of which the deficit
        # share is borrowed (future taxpayers). The resource cost, the return on public capital, is an imputed
        # cost that is never borrowed, so its federal part is borne today. The displaced beneficiaries are not
        # a budget item: the capped programs' eligible non-recipients bear them (displaced_beneficiaries).
        sp = {end: fedsplit[(CASE["model"], end, "central")] for end in ("low", "high")}
        mid = lambda x: dict(x, central=(x["low"] + x["high"]) / 2)  # noqa: E731
        res = mid({end: sp[end]["resource_cost_bn"] for end in sp})
        res_fed = mid({end: sp[end]["resource_cost_federal_bn"] for end in sp})
        disp = mid({end: sp[end]["displaced_bn"] for end in sp})
        fisc = {L: dict(cost=cost[L], federal=fed[L] + res_fed[L], state_local=cost[L] - disp[L] - fed[L] - res_fed[L],
                        future=dsh * fed[L], federal_today=(1 - dsh) * fed[L] + res_fed[L],
                        cash=cost[L] - res[L] - disp[L], cash_federal=fed[L], resource=res[L],
                        resource_federal=res_fed[L], displaced=disp[L]) for L in LEVELS}
        if CASE.get("accrual"):
            # The pension switch's accrual (the debt lane's fourth part; federal: social security, Medicare, federal
            # income tax on benefits) is the group's claim on benefits paid later. Nothing finances it in 2024, so it
            # joins the future taxpayers' part, not the persons' fiscal channel; the cash part leaves it out.
            acc = mid({end: sp[end]["accrual_bn"] for end in sp})
            acc_fed = mid({end: sp[end]["accrual_federal_bn"] for end in sp})
            gate("pension_accrual_is_federal", all(abs(acc[L] - acc_fed[L]) < 1e-9 for L in LEVELS), accrual=acc,
                 federal=acc_fed)
            for L in LEVELS:
                x = fisc[L]
                x.update(federal=x["federal"] + acc_fed[L], state_local=x["state_local"] - acc[L],
                         future=x["future"] + acc[L], cash=x["cash"] - acc[L], accrual=acc[L], accrual_federal=acc_fed[L],
                         future_borrowing=dsh * fed[L])
    meta["fiscal"] = fisc
    for conv, kf, ks in (("a", tax_fed, tax_sl), ("b", ones, ones)):
        fedt = {L: -alloc(d, kf, fisc[L]["federal_today"]) for L in LEVELS}
        slt = {L: -alloc_states(d, ks, {s: fisc[L]["state_local"] * w for s, w in w_state.items()}, notes=notes,
                                label=f"fiscal_sl_{conv}") for L in LEVELS}
        put(f"fiscal_federal_today_{conv}", fedt, {L: -fisc[L]["federal_today"] for L in LEVELS})
        put(f"fiscal_state_local_{conv}", slt, {L: -fisc[L]["state_local"] for L in LEVELS})
        put(f"fiscal_{conv}", {L: fedt[L] + slt[L] for L in LEVELS},
            {L: -(fisc[L]["federal_today"] + fisc[L]["state_local"]) for L in LEVELS})
        if CASE.get("capped"):
            # The same channel split by financing: cash financed today, and the resource cost (federal part by
            # the federal key, state-local part by the state-local key within the group's states).
            for part, fk, sk in (("cash", lambda f: (1 - dsh) * f["cash_federal"], lambda f: f["cash"] - f["cash_federal"]),
                                 ("resource", lambda f: f["resource_federal"], lambda f: f["resource"] - f["resource_federal"])):
                arr = {L: -alloc(d, kf, fk(fisc[L])) - alloc_states(
                    d, ks, {s: sk(fisc[L]) * w for s, w in w_state.items()}, notes=notes, label=f"fiscal_{part}_sl_{conv}")
                    for L in LEVELS}
                put(f"fiscal_{part}_{conv}", arr, {L: -(fk(fisc[L]) + sk(fisc[L])) for L in LEVELS})
            worst = max(float(np.abs(ch[f"fiscal_cash_{conv}"][L] + ch[f"fiscal_resource_{conv}"][L]
                                     - ch[f"fiscal_{conv}"][L]).max()) for L in LEVELS)
            gate(f"fiscal_{conv}_is_cash_plus_resource", worst < 1e-6, max_abs_usd_per_person=worst)
    if CASE.get("capped"):
        # Capped programs: the distribution lane's amounts at the band ends (fiscal_totals, from case_ends.cjs)
        # on its eligible non-recipient keys; the same total as the debt lane's displaced column.
        progs = fin[CASE["model"]]["capped"]["programs"]
        for end, j in (("low", 0), ("high", 1)):
            gate(f"displaced_beneficiaries_match_debt_lane_{end}",
                 abs(sum(v[j] for v in progs.values()) - disp[end]) < 1e-6,
                 distribution_lane=sum(v[j] for v in progs.values()), debt_lane=disp[end])
        amt = {k: mid({"low": v[0], "high": v[1]}) for k, v in progs.items()}
        key_of = getattr(B, "CAPPED_KEY_OF", {})      # September 29: public housing on rental assistance's key
        per = {k: {L: -alloc(d, I["capped_keys"][key_of.get(k, k)], amt[k][L]) for L in LEVELS} for k in progs}
        put("displaced_beneficiaries", {L: sum(per[k][L] for k in progs) for L in LEVELS},
            {L: -sum(amt[k][L] for k in progs) for L in LEVELS})
        for k in progs:
            put(f"displaced_{k}", per[k], {L: -amt[k][L] for L in LEVELS})
        meta["capped_programs"] = dict(amounts_bn=amt, keys=I["capped_info"])
    # Variants without geography: every level's cost pooled nationally, on all taxes (ladder 194's
    # convention (a)) or per person (its convention (b)).
    put("fiscal_a_pooled_national", {L: -alloc(d, tax_all, fisc[L]["federal_today"] + fisc[L]["state_local"]) for L in LEVELS},
        {L: -(fisc[L]["federal_today"] + fisc[L]["state_local"]) for L in LEVELS})
    put("fiscal_b_pooled_national", {L: -alloc(d, ones, fisc[L]["federal_today"] + fisc[L]["state_local"]) for L in LEVELS},
        {L: -(fisc[L]["federal_today"] + fisc[L]["state_local"]) for L in LEVELS})

    # ---- wages: the account's production term P (high school or less, sigma 2, epsilon infinite)
    acc, accg = I["account"], I["account_gdp"]
    ratios = [accg.native_production_gain_bn / acc.native_production_gain_bn,
              accg.other_immigrant_production_gain_bn / acc.other_immigrant_production_gain_bn,
              accg.induced_current_receipts_bn / acc.induced_current_receipts_bn]
    gate("gdp_normalization_is_a_uniform_scale", np.allclose(ratios, ratios[0], rtol=1e-9), ratios=[float(r) for r in ratios])
    nf = {"cash": 1.0, "gdp": float(ratios[0])}
    cash = B.wage_delta(I["basis"]["hs_or_less"], acc, True)
    P_acc = float(acc.native_production_gain_bn + acc.other_immigrant_production_gain_bn)
    gate("account_wages_equal_P_cash", np.isclose((pw * cash).sum() / 1e9, P_acc, rtol=1e-9), cps=(pw * cash).sum() / 1e9, nest=P_acc)
    wages = {end: cash * nf[e[end]["normalization"]] for end in ("low", "high")}
    wages["central"] = (wages["low"] + wages["high"]) / 2
    put("wages", wages, {L: (pw * wages[L]).sum() / 1e9 for L in LEVELS})
    # Gate: inside channels (CPS wages + A + F) equal the adopted cost in every specification.
    worst = 0.0
    # Each model's CPS wage total and GDP factor: the case's above; with its own production grid (September 29 on)
    # the case before it keeps the published scenarios.
    P_of = {CASE["model"]: ((pw * cash).sum() / 1e9, nf)}
    P_of[CASE["prev"]["model"]] = P_of[CASE["model"]]
    if CASE.get("production"):
        pa, pg = (I["nest"][CASE["prev"]["case"]][k] for k in ("account", "account_gdp"))
        P_of[CASE["prev"]["model"]] = ((pw * B.wage_delta(I["basis"]["hs_or_less"], pa, True)).sum() / 1e9,
                                       {"cash": 1.0, "gdp": float(pg.native_production_gain_bn / pa.native_production_gain_bn)})
    for cname, c in fin.items():
        tot, nfc = P_of[cname]
        for r in c["specs"].itertuples():
            inside = tot * nfc[r.normalization] + r.A_bn + r.F_bn
            worst = max(worst, abs(inside + r.cost_bn))
            gate(f"wages_equal_engine_P_{cname}_{r.spec_id}", np.isclose(tot * nfc[r.normalization], r.P_bn, atol=1e-8))
    gate("inside_channels_sum_to_headline_every_specification", worst < 1e-8, max_abs_gap_bn=worst, specifications=128)
    # With A from fiscal_totals the band ends close to its rounding (recorded), not to 1e-9.
    for end in ("low", "high"):
        inside = (pw * ch["fiscal_a"][end]).sum() / 1e9 - fisc[end]["future"] + (pw * wages[end]).sum() / 1e9
        if CASE.get("capped"):
            inside += (pw * ch["displaced_beneficiaries"][end]).sum() / 1e9
        gate(f"inside_channels_equal_band_end_{end}", abs(inside + e[end]["cost_bn"]) < 1e-3, inside=inside,
             headline=-e[end]["cost_bn"], gap=inside + e[end]["cost_bn"])
    # Variants (overlap wages): epsilon 3 on the account's split; the below-BA split (ladder 194).
    for vname, row, rowg in (("wages_eps3", I["eps3_hs"], I["eps3_hs_gdp"]),):
        vc = B.wage_delta(I["basis"]["hs_or_less"], row, True)
        f_gdp = float((rowg.native_production_gain_bn + rowg.other_immigrant_production_gain_bn)
                      / (row.native_production_gain_bn + row.other_immigrant_production_gain_bn))
        vn = {"cash": 1.0, "gdp": f_gdp}
        arr = {end: vc * vn[e[end]["normalization"]] for end in ("low", "high")}
        arr["central"] = (arr["low"] + arr["high"]) / 2
        put(vname, arr, {L: (pw * arr[L]).sum() / 1e9 for L in LEVELS})
        dF = {end: (float(rowg.induced_current_receipts_bn) if e[end]["normalization"] == "gdp" else float(row.induced_current_receipts_bn))
              - e[end]["F_bn"] for end in ("low", "high")}
        dF["central"] = (dF["low"] + dF["high"]) / 2
        meta[f"{vname}_delta_F"] = dF
        for conv, k in (("a", tax_all), ("b", ones)):
            put(f"{vname}_receipts_{conv}", {L: alloc(d, k, dF[L]) for L in LEVELS}, {L: dF[L] for L in LEVELS})
    bb = B.wage_delta(I["basis"]["below_ba"], I["central"], True)
    put("wages_below_ba_cash", {L: bb for L in LEVELS}, {L: (pw * bb).sum() / 1e9 for L in LEVELS})
    meta["wages_P"] = {"cash": P_acc, "gdp": P_acc * nf["gdp"], "gdp_factor": nf["gdp"],
                       "below_ba_cash": float((pw * bb).sum() / 1e9)}

    # ---- housing: renters' extra rent and landlords' receipts, by income cell and state
    notes.setdefault("rake_fallbacks", [])
    renter_key = 1.0 / d.n_other_hh.to_numpy()
    renter_mask = other & d.H_TENURE.eq(2).to_numpy() & d.hh_other_ref.to_numpy()
    landlord_key = np.abs(d.HRNTVAL.to_numpy(float)) / d.n_other_hh.to_numpy()
    owner_mask = other & d.H_TENURE.eq(1).to_numpy() & d.hh_other_ref.to_numpy()
    li = B.per_person(d, B.spread_cells(I["acs"]["intp_cells"], R, d), 1.0)
    ls = B.per_person(d, B.spread_cells(I["scf"], R, d), 1.0)
    cell100 = np.where(other, B.bins(np.nan_to_num(R["p_other"]), 100), 0)
    land_profile = np.bincount(cell100[other], weights=(pw * (li + ls) / 2)[other], minlength=100)
    land_profile /= land_profile.sum()
    hs = housing_inputs(I)
    meta["housing"] = {k: dict(v, pattern=list(v["pattern"])) for k, v in hs.items()}

    def housing_level(h, label):
        g = I["acs_geo"][h["pattern"]]
        acs_total = sum(g["rent_state"].values()) / 1e9
        arm = I["arms"][h["pattern"]]["other_renters_extra_rent_bn"]
        # The base's ACS rebuild of the pattern arm matches the housing lane's total (national uniform
        # to 4e-9 relative, from the base's rounded national share); scale to the level's total exactly.
        gate(f"acs_rent_total_{label}", np.isclose(acs_total, arm, rtol=1e-7), acs=acs_total, lane=arm)
        s = h["renters_bn"] / acs_total
        rent_state = {k: v * s for k, v in g["rent_state"].items()}
        r = -rake_channel(B, d, R, renter_key, renter_mask, to_cells100(g["rent_cells"]) * s, rent_state,
                          fallback=np.ones(len(d)), label=f"renters_{label}", notes=notes)
        tot = h["landlords_bn"] * 1e9
        rs = pd.Series(rent_state)
        ll = rake_channel(B, d, R, landlord_key, other & (landlord_key > 0), land_profile * tot,
                          (rs / rs.sum() * tot).to_dict(), fallback=np.maximum(d.capital.to_numpy(float), 0) + 1e-9,
                          label=f"landlords_{label}", notes=notes)
        return r, ll
    ren, lan, own = {}, {}, {}
    for L in LEVELS:
        ren[L], lan[L] = housing_level(hs[L], L)
    put("renters", ren, {L: -hs[L]["renters_bn"] for L in LEVELS})
    put("landlords", lan, {L: hs[L]["landlords_bn"] for L in LEVELS})
    rn, ln = housing_level(hs["national_uniform_central"], "national_uniform_central")
    put("renters_national_uniform", {L: rn for L in LEVELS},
        {L: -hs["national_uniform_central"]["renters_bn"] for L in LEVELS})
    put("landlords_national_uniform", {L: ln for L in LEVELS},
        {L: hs["national_uniform_central"]["landlords_bn"] for L in LEVELS})
    # Owner-occupiers' value gain, a stock and never added: the metro-local arm by elasticity level.
    for L in LEVELS:
        g = I["acs_geo"][(L, "metro_local")]
        own[L] = rake_channel(B, d, R, renter_key, owner_mask, to_cells100(g["value_cells"]), g["value_state"],
                              fallback=np.ones(len(d)), label=f"owner_value_{L}", notes=notes)
    put("owner_value_stock", own, {L: I["arms"][(L, "metro_local")]["other_owner_value_gain_stock_bn"] for L in LEVELS})

    # ---- crime victims: decision 4's figure (central) and the victim lane's envelope (low, high); the
    # victim lane's two footings as allocated variants. Only figures a lane computed.
    cr = crime_inputs(B)
    meta["crime"] = cr
    crime_tot = {"low": cr["envelope_low"], "central": cr["mixed_equal"], "high": cr["envelope_high"]}
    ks = I["keys_rank"]
    s_share = I["serious_share"]

    def crime_states(total, label):
        out = np.zeros(len(d))
        for cls, share in (("serious", s_share), ("simple", 1 - s_share)):
            out -= alloc_states(d, ks[cls], {s: total * share * w for s, w in w_state.items()}, notes=notes, label=label)
        return out
    put("crime_victims", {L: crime_states(crime_tot[L], f"crime_{L}") for L in LEVELS}, {L: -crime_tot[L] for L in LEVELS})
    for cid, k in (("crime_victims_equal_footing", "equal"), ("crime_victims_custody_footing", "custody")):
        arr = crime_states(cr[k], cid)
        put(cid, {L: arr for L in LEVELS}, {L: -cr[k] for L in LEVELS})
    cn = crime_split(B, d, ks, cr["mixed_equal"], s_share)
    put("crime_victims_national_key", {L: cn for L in LEVELS}, {L: -cr["mixed_equal"] for L in LEVELS})

    # ---- unreimbursed hospital care, by the group's uninsured person-years by state
    priv = d.PRIV.eq(1).to_numpy().astype(float)
    u = I["unreimbursed"]
    put("unreimbursed_care", {L: -alloc_states(d, priv, {s: u[L] * w for s, w in w_unins.items()}, notes=notes,
                                               label=f"unreimbursed_{L}") for L in LEVELS}, {L: -u[L] for L in LEVELS})

    # ---- congestion (B1, lanes fixed; from September 27 re-derived with lanes following the highway
    # response), by the urban areas' states, per metropolitan worker
    cg = congestion_inputs()
    if CASE.get("congestion") == "long_run":
        cg = congestion_long_run(cg)
        state_bn = cg["state_bn"]
    else:
        state_bn = {L: {POSTAL[s] if isinstance(s, str) else s: cg["total"][L] * v for s, v in cg["state_share"].items()}
                    for L in LEVELS}
    meta["congestion"] = cg
    workers = d.WORKYN.eq(1).to_numpy().astype(float)
    put("congestion", {L: -alloc_states(d, d.metro_worker.to_numpy().astype(float), state_bn[L],
                                        fallback=workers, notes=notes, label=f"congestion_{L}") for L in LEVELS},
        {L: -cg["total"][L] for L in LEVELS})

    # ---- race- and ethnicity-based preferences: the part tied to Mexican-origin beneficiaries
    pr = preference_inputs()
    meta["preferences"] = pr
    nhw = other & d.race5.eq("nh_white").to_numpy() & d.native.to_numpy()
    earn, semp = d.earn.to_numpy(), d.semp.to_numpy()
    pkeys = {"admissions": (earn, nhw & (d.A_HGA.to_numpy() >= 43)), "contractor_hiring": (earn, nhw),
             "lost_profits": (semp, nhw), "taxpayer_premium": (tax_all, nhw)}
    # From September 27 the row is an attribution under its stated rule: the DBE premium's part already in
    # the fiscal channel is netted, and the rule's gain to the pool's other members is carried beside it.
    at = preference_attribution(d, pr) if CASE.get("preferences") == "attribution" else None
    parts = at["white_parts"] if at else pr["parts"]
    pref = {}
    for L in LEVELS:
        f = pr["group_part"][L] / sum(pr["parts"].values())
        pref[L] = sum(-alloc(d, k, parts[p] * f, m) for p, (k, m) in pkeys.items())
    put("preferences_group_part", pref, {L: -pr["group_part"][L] for L in LEVELS} if not at
        else {L: -sum(parts.values()) * at["scale"][L] for L in LEVELS})
    if at:
        meta["preferences_attribution"] = at
        hisp, race = d.PEHSPNON.eq(1).to_numpy(), d.PRDTRACE.to_numpy()
        pool = other & ~nhw & ~hisp & (race != 2)   # the producer's non-preferred earners, less white natives
        okeys = {"admissions": (earn, pool & (race != 3) & (d.A_HGA.to_numpy() >= 43)), "contractor_hiring": (earn, pool),
                 "lost_profits": (semp, other & ~nhw), "taxpayer_premium": (tax_all, other & ~nhw)}
        put("preferences_group_part_others",
            {L: sum(-alloc(d, k, at["other_parts"][p] * at["scale"][L], m) for p, (k, m) in okeys.items()) for L in LEVELS},
            {L: -sum(at["other_parts"].values()) * at["scale"][L] for L in LEVELS})
    put("preferences_regime", {L: -alloc(d, earn, pr["regime"][L], nhw) for L in LEVELS}, {L: -pr["regime"][L] for L in LEVELS})

    # ---- mobility: local-shock insurance to low-skill US-born men; Borjas's gain to all earnings
    mo = mobility_inputs()
    meta["mobility"] = mo
    lowskill_men = other & d.native.to_numpy() & d.sex.eq("male").to_numpy() & (d.A_HGA.to_numpy() <= 39) & (earn > 0)
    put("mobility", {L: alloc(d, earn, mo["insurance"][L], lowskill_men) + alloc(d, earn, mo["borjas"][L]) for L in LEVELS},
        {L: mo["total"][L] for L in LEVELS})

    # ---- city size and schooling mix (proposed): earnings part by state, receipts by convention
    sc = scale_inputs()
    meta["scale"] = sc
    sstates = sc["state_share"]
    put("scale_private", {L: alloc_states(d, earn, {s: sc["total"][L] * sc["private_share"] * v for s, v in sstates.items()},
                                          notes=notes, label=f"scale_{L}") for L in LEVELS},
        {L: sc["total"][L] * sc["private_share"] for L in LEVELS})
    for conv, k in (("a", tax_all), ("b", ones)):
        put(f"scale_receipts_{conv}", {L: alloc(d, k, sc["total"][L] * sc["receipts_share"]) for L in LEVELS},
            {L: sc["total"][L] * sc["receipts_share"] for L in LEVELS})

    # ---- property crime (victim lane's arrest-share proxy), one share per household, group's states
    pc = property_crime_inputs()
    meta["property_crime"] = pc
    hh_key = 1.0 / d.n_other_hh.to_numpy()
    put("property_crime", {L: -alloc_states(d, hh_key, {s: pc[L] * w for s, w in w_state.items()}, notes=notes,
                                            label=f"property_{L}") for L in LEVELS}, {L: -pc[L] for L in LEVELS})

    # ---- care: who receives the native women's extra hours (display; the taxes are inside fiscal)
    ca = care_hours_inputs()
    meta["care_hours"] = ca
    women = care_women_mask(d)
    meta["care_hours"]["cps_women_m"] = float((pw * women).sum() / 1e6)
    arr = alloc(d, earn, ca["after_tax_earnings_bn"], women)
    put("care_women_after_tax_earnings", {L: arr for L in LEVELS}, {L: ca["after_tax_earnings_bn"] for L in LEVELS})

    # ---- side views, never added
    cx = consumer_side_view(d, I)
    put("consumer_prices", {L: cx for L in LEVELS}, {L: float(I["cex_q"].sum()) for L in LEVELS})
    dbt = debt_inputs(fin)
    meta["debt"] = dbt
    for conv, k in (("a", tax_fed), ("b", ones)):
        put(f"debt_legacy_{conv}", {L: -alloc(d, k, dbt[L]) for L in LEVELS}, {L: -dbt[L] for L in LEVELS})

    # ---- closure: persons sum to each channel's total at every level
    for name, arrays in ch.items():
        for L in LEVELS:
            got = float((pw * arrays[L]).sum() / 1e9)
            gate(f"closure_{name}_{L}", np.isclose(got, totals[name][L], rtol=1e-9, atol=1e-9) and not np.any(arrays[L][~other]),
                 persons=got, total=totals[name][L])
    ctx = dict(tax_fed=tax_fed, tax_sl=tax_sl, q5=R["q5"])
    return ch, totals, meta, ctx


# ================================================================== more channel inputs
def property_crime_inputs():
    """Victim lane's property-crime proxy (arrest shares x NCVS victimisations x unit costs)."""
    p = pd.read_csv(FISCAL / "crime_victim_cost_2026_09_23/derived/property_proxy.csv")
    by = p.groupby("price_set").cost.sum() / 1e9
    gate("property_crime_proxy_reproduced", np.isclose(by["miller2021"], 1.2727, atol=5e-4)
         and np.isclose(by["mccollister2010"], 1.3762, atol=5e-4), **{k: float(v) for k, v in by.items()})
    return {"low": float(by.min()), "central": float(by["miller2021"]), "high": float(by.max())}


def care_hours_inputs():
    """Care lane central (Cortes-Tessada Table 10, metro-weighted shock, CPS-scaled union): the
    native women's extra-hours earnings and the taxes on them."""
    s = pd.read_csv(FISCAL / "care_household_services_2026_09_23/derived/hours_tax_specs.csv")
    r = s[(s.arm == "CT") & (s.coefficient == "t10_female_x_L") & (s.shock == "metro_weighted")
          & (s.scaling == "cps_scaled") & (s.population == "native_nonunion")]
    gate("care_hours_central_row_unique", len(r) == 1, rows=len(r))
    r = r.iloc[0]
    c = care_inputs()
    gate("care_hours_taxes_match_summary", np.isclose(r.tax_bn_account_current, c["hours_taxes"], rtol=1e-9),
         specs=float(r.tax_bn_account_current), summary=c["hours_taxes"])
    return dict(earnings_bn=float(r.earnings_bn), taxes_bn=float(r.tax_bn_account_current),
                after_tax_earnings_bn=float(r.earnings_bn - r.tax_bn_account_current),
                d_hours_week_on_removal=float(r.d_hours_week_on_removal), total=c["total"],
                elder_care_bn=c["elder_care"], private_gain_bn=c["private_gain"],
                consumer_surplus_net_bn=c["consumer_surplus_net"])


DIVISION = {9: 1, 23: 1, 25: 1, 33: 1, 44: 1, 50: 1, 34: 2, 36: 2, 42: 2, 17: 3, 18: 3, 26: 3, 39: 3, 55: 3,
            19: 4, 20: 4, 27: 4, 29: 4, 31: 4, 38: 4, 46: 4, 10: 5, 11: 5, 12: 5, 13: 5, 24: 5, 37: 5, 45: 5,
            51: 5, 54: 5, 1: 6, 21: 6, 28: 6, 47: 6, 5: 7, 22: 7, 40: 7, 48: 7, 4: 8, 8: 8, 16: 8, 30: 8,
            32: 8, 35: 8, 49: 8, 56: 8, 2: 9, 6: 9, 15: 9, 41: 9, 53: 9}


def wquantile(x, w, q):
    o = np.argsort(x, kind="stable")
    cw = np.cumsum(w[o]) / w.sum()
    return x[o][min(int(np.searchsorted(cw, q, side="left")), len(x) - 1)]


def care_women_mask(d):
    """US-born other-resident women in the top quartile of their census division's female hourly-wage
    distribution (all civilian women with earnings and hours), the care lane's Cortes-Tessada group."""
    hours = d.WKSWORK.to_numpy(float) * d.HRSWK.to_numpy(float)
    earn = d.PEARNVAL.to_numpy(float)
    wage = np.divide(earn, hours, out=np.zeros(len(d)), where=hours > 0)
    fem = d.civ.to_numpy() & d.A_SEX.eq(2).to_numpy() & (wage > 0)
    div = d.st.map(DIVISION).to_numpy()
    gate("census_divisions_cover_states", not np.isnan(div.astype(float)).any())
    pw = d.pw.to_numpy()
    top = np.zeros(len(d), bool)
    for k in range(1, 10):
        m = fem & (div == k)
        top |= m & (wage >= wquantile(wage[m], pw[m], 0.75))
    return top & d.other.to_numpy() & d.native.to_numpy()


def ingroup_victims(B):
    """Victims inside the group, which the victim lane excludes: the Hispanic-victim rows' group
    victimisations less the outside (non-group Hispanic) victims, at the lane's unit prices. The rows
    are on the victim lane's equal footing; no lane computed the in-group figure on the custody footing
    or with the mixed-group correction."""
    v = pd.read_csv(B.PATHS["crime_victim"])
    h = v[v.victim == "Hispanic"].copy()
    gate("crime_outside_cost_rows_reproduced", np.allclose(h.outside_victims * h.unit_full, h.cost_full, rtol=1e-6))
    n_in = h.group_victimisations - h.outside_victims
    full = float((n_in * h.unit_full).sum() / 1e9)
    tan = float((n_in * h.unit_tangible).sum() / 1e9)
    return dict(nonfatal_victimisations=float(n_in[h.block == "nonfatal_violence"].sum()),
                homicides=float(n_in[h.block == "homicide"].sum()),
                full_equal_bn=full, tangible_equal_bn=tan,
                murder_full_equal_bn=float((n_in * h.unit_full)[h.block == "homicide"].sum() / 1e9))


# ================================================================== nets, cuts, tree
SOCIAL = ["renters", "landlords", "crime_victims", "property_crime", "unreimbursed_care", "congestion", "mobility"]
PROPOSED = ["preferences_group_part", "scale_private"]


def net_parts(name, conv, sister_ids):
    """A net's channels. From September 27 the account carries the capped programs' displaced beneficiaries,
    and with_proposed the preferences rule's gain to the pool's other members."""
    parts = [f"fiscal_{conv}", "wages"] + (["displaced_beneficiaries"] if CASE.get("capped") else [])
    if name in ("social", "with_proposed"):
        parts += SOCIAL
    if name == "with_proposed":
        parts += PROPOSED + [f"scale_receipts_{conv}"] + list(sister_ids)
        if CASE.get("preferences") == "attribution":
            parts.insert(parts.index("preferences_group_part") + 1, "preferences_group_part_others")
    return parts


def build_nets(ch, totals, sister_ids):
    """Per-person nets at central values and at the least- and most-costly stacks. Parts that are two
    sides of one estimate move together: fiscal and wages by band end (one specification; from September
    27 with the displaced beneficiaries), renters and landlords by level (one rent change), the scale
    term's earnings and receipts by level, and the preferences row with its other recipients' part (one
    attribution). Every other channel takes the level whose total is highest (least costly) or lowest
    (most costly)."""
    nets, ntot, recipe = {}, {}, {}
    for name in ("account", "social", "with_proposed"):
        for conv in CONVENTIONS:
            parts = net_parts(name, conv, sister_ids)
            groups = [([f"fiscal_{conv}", "wages"] + (["displaced_beneficiaries"] if CASE.get("capped") else []),
                       ("low", "high")), (["renters", "landlords"], LEVELS),
                      (["scale_private", f"scale_receipts_{conv}"], LEVELS)]
            if CASE.get("preferences") == "attribution":
                groups.append((["preferences_group_part", "preferences_group_part_others"], LEVELS))
            groups = [(g, levs) for g, levs in groups if all(x in parts for x in g)]
            grouped = {x for g, _ in groups for x in g}
            groups += [([x], LEVELS) for x in parts if x not in grouped]
            for stack in ("central", "least_costly", "most_costly"):
                lev = {}
                for g, levs in groups:
                    if stack == "central":
                        choice = "central"
                    else:
                        sums = {L: sum(totals[x][L] for x in g) for L in levs}
                        choice = (max if stack == "least_costly" else min)(sums, key=sums.get)
                    lev.update({x: choice for x in g})
                arr = sum(ch[x][lev[x]] for x in parts)
                tot = sum(totals[x][lev[x]] for x in parts)
                key = (f"net_{name}_{conv}", stack)
                nets[key], ntot[key], recipe[key] = arr, tot, {x: lev[x] for x in parts}
    return nets, ntot, recipe


MAIN_NETS = [f"net_{n}_{c}" for n in ("account", "social", "with_proposed") for c in CONVENTIONS]
UNITS = {"person": "wages to the earner, taxes and rent shared within the unit",
         "spm_unit_pooled": "every amount pooled within the SPM unit, per capita over its other residents"}


def spm_pooler(d):
    """Ruling 6: pool other residents' amounts within SPM units. Each other resident gets the unit's
    weighted mean over its other residents: the members' sum over their number when their weights are
    equal, and still every total when they are not. Group members stay out, and their items stay in the
    group frame."""
    other, pw = d.other.to_numpy(), d.pw.to_numpy()
    gate("spm_units_nest_in_households", d.groupby("SPM_ID").PH_SEQ.nunique().max() == 1)
    codes, _ = pd.factorize(d.SPM_ID.to_numpy())
    n = int(codes.max()) + 1
    w = np.where(other, pw, 0.0)
    den = np.bincount(codes, weights=w, minlength=n)

    def pool(x):
        mean = np.divide(np.bincount(codes, weights=w * x, minlength=n), den, out=np.zeros(n), where=den > 0)
        return np.where(other, mean[codes], x)
    size = np.bincount(codes, weights=other.astype(float), minlength=n)[codes]
    mixed = np.bincount(codes, weights=(~other & d.target.to_numpy()).astype(float), minlength=n)[codes] > 0
    ws = pd.Series(pw[other]).groupby(codes[other])
    spread = ((ws.max() - ws.min()) / ws.mean()).to_numpy()
    info = dict(other_in_multi_member_units_share=float(w[other & (size > 1)].sum() / w.sum()),
                other_in_mixed_units_m=float(w[other & mixed].sum() / 1e6),
                units_with_unequal_weights_share=float((spread > 1e-9).mean()),
                max_relative_weight_spread=float(spread.max()))
    return pool, info


def pooling_moves(d, nets, pnets):
    """Who moves when the social net is pooled within SPM units, by role, and by whether the unit comes
    out ahead once pooled."""
    other = d.other.to_numpy()
    w = d.pw.to_numpy()[other]
    age, working = d.A_AGE.to_numpy()[other], d.WORKYN.eq(1).to_numpy()[other]
    role = np.select([age < 18, ~working], ["under_18", "adult_not_working"], "adult_working")
    rows = []
    for conv in CONVENTIONS:
        k = (f"net_social_{conv}", "central")
        x, y = nets[k][other], pnets[k][other]
        unit = np.where(y > 0, "unit_ahead", "unit_behind")
        for r in ("under_18", "adult_not_working", "adult_working", "all"):
            for u in ("unit_ahead", "unit_behind", "all"):
                m = (role == r if r != "all" else np.ones(len(w), bool)) & (unit == u if u != "all" else True)
                W = w[m].sum()
                if W == 0:
                    continue
                rows.append(dict(net=k[0], role=r, unit=u, persons_m=W / 1e6,
                                 ahead_person=w[m & (x > 0)].sum() / W, ahead_pooled=w[m & (y > 0)].sum() / W,
                                 up_m=w[m & (x <= 0) & (y > 0)].sum() / 1e6, down_m=w[m & (x > 0) & (y <= 0)].sum() / 1e6,
                                 mean_person_usd=(w * x)[m].sum() / W, mean_pooled_usd=(w * y)[m].sum() / W))
    return pd.DataFrame(rows)


CUT_COLUMNS = ["quintile", "decile", "edu_nativity", "tenure", "age3", "race5", "state3", "top10_states", "sex",
               "worker", "industry5"]


def add_cut_columns(d, R):
    d["quintile"] = np.where(d.other, "Q" + pd.Series(R["q5"] + 1).astype(str), "")
    d["decile"] = np.where(d.other, "D" + pd.Series(R["q10"] + 1).astype(str).str.zfill(2), "")


def tabulate_cuts(d, arrays: dict, totals_by_array: dict, nets: set):
    """Every cut of every array: $bn, persons, households, $ per person and per household, % of
    SPM resources; for nets also the shares of net winners and losers. Gate: groups sum to the frame."""
    other = d.other.to_numpy()
    pw = d.pw.to_numpy()[other]
    hh = d.hh_frac.to_numpy()[other]
    res = (d.resources_pc.to_numpy(float) * d.pw.to_numpy())[other]
    rows, recon = [], []
    for cut in CUT_COLUMNS:
        codes, groups = pd.factorize(d[cut].to_numpy()[other], sort=True)
        n = len(groups)
        persons = np.bincount(codes, weights=pw, minlength=n)
        households = np.bincount(codes, weights=hh, minlength=n)
        resources = np.bincount(codes, weights=res, minlength=n)
        worst = 0.0
        for (name, level), arr in arrays.items():
            x = pw * arr[other]
            bn = np.bincount(codes, weights=x, minlength=n) / 1e9
            tot = totals_by_array[(name, level)]
            worst = max(worst, abs(bn.sum() - tot))
            recon.append(dict(cut=cut, channel=name, level=level, frame_bn=tot, cut_sum_bn=float(bn.sum()),
                              diff_bn=float(bn.sum() - tot)))
            is_net = name in nets
            if is_net:
                win = np.bincount(codes, weights=pw * (arr[other] > 0), minlength=n) / persons
                lose = np.bincount(codes, weights=pw * (arr[other] < 0), minlength=n) / persons
            for g in range(n):
                r = dict(cut=cut, group=groups[g], channel=name, level=level, bn=bn[g], persons_m=persons[g] / 1e6,
                         households_m=households[g] / 1e6, usd_per_person=bn[g] * 1e9 / persons[g],
                         usd_per_household=bn[g] * 1e9 / households[g] if households[g] > 0 else np.nan,
                         pct_of_resources=100 * bn[g] * 1e9 / resources[g] if resources[g] > 0 else np.nan)
                if is_net:
                    r.update(winners_share=win[g], losers_share=lose[g])
                rows.append(r)
        gate(f"cuts_sum_to_frame_{cut}", worst < 1e-6, max_abs_diff_bn=worst, arrays=len(arrays))
    return pd.DataFrame(rows), pd.DataFrame(recon)


TREE_FEATURES = ["decile", "edu_nativity", "tenure", "age3", "race5", "state3", "sex", "worker", "industry5"]


def grow_tree(X: pd.DataFrame, y, w, net, depth=3, min_share=0.02):
    """Weighted greedy classification tree on the winner indicator (Gini), binary splits: one value
    against the rest for categorical cuts, a threshold for deciles. Returns the leaves."""
    wt = w.sum()
    cols = {c: X[c].to_numpy() for c in X.columns}
    dec = np.array([int(s[1:]) if s else 0 for s in cols["decile"]]) if "decile" in cols else None

    def gini(m):
        ww = w[m].sum()
        if ww <= 0:
            return 0.0
        p = (w[m] * y[m]).sum() / ww
        return ww * 2 * p * (1 - p)

    leaves = []

    def split(m, path, level):
        if level == depth:
            return leaves.append((path, m))
        base, best = gini(m), None
        for f, v in cols.items():
            cands = ([(f"decile <= {k}", dec <= k) for k in range(1, 10)] if f == "decile"
                     else [(f"{f} = {g}", v == g) for g in np.unique(v[m])])
            for lab, s in cands:
                l, r = m & s, m & ~s
                if w[l].sum() < min_share * wt or w[r].sum() < min_share * wt:
                    continue
                imp = gini(l) + gini(r)
                if best is None or imp < best[0]:
                    best = (imp, lab, s)
        if best is None or best[0] >= base - 1e-9 * wt:
            return leaves.append((path, m))
        _, lab, s = best
        neg = lab.replace(" = ", " != ").replace("<=", ">")
        split(m & s, path + [lab], level + 1)
        split(m & ~s, path + [neg], level + 1)

    split(np.ones(len(y), bool), [], 0)
    out = []
    for path, m in leaves:
        out.append(dict(path=" & ".join(path) or "all", persons_m=w[m].sum() / 1e6, share_of_persons=w[m].sum() / wt,
                        winners_share=(w[m] * y[m]).sum() / w[m].sum(),
                        mean_net_usd=(w[m] * net[m]).sum() / w[m].sum()))
    return out


PAIRS = [("edu_nativity", "state3"), ("tenure", "decile"), ("tenure", "state3"), ("industry5", "state3"),
         ("age3", "tenure"), ("decile", "state3"), ("worker", "state3"), ("edu_nativity", "tenure")]


def winner_cells(d, nets, min_m=1.0):
    """Two-way cells of the telling cuts: persons, share of net winners, mean net, for each net at
    central values; cells under min_m million persons are dropped."""
    other = d.other.to_numpy()
    w = d.pw.to_numpy()[other]
    out = []
    for a, b in PAIRS:
        ga, gb = d[a].to_numpy()[other], d[b].to_numpy()[other]
        cell = pd.Series(ga).astype(str) + " & " + pd.Series(gb).astype(str)
        codes, groups = pd.factorize(cell, sort=True)
        persons = np.bincount(codes, weights=w)
        for (name, stack), arr in nets.items():
            if stack != "central":
                continue
            x = arr[other]
            win = np.bincount(codes, weights=w * (x > 0)) / persons
            mean = np.bincount(codes, weights=w * x) / persons
            for g in np.where(persons >= min_m * 1e6)[0]:
                out.append(dict(cuts=f"{a} x {b}", cell=groups[g], net=name, persons_m=persons[g] / 1e6,
                                winners_share=win[g], mean_net_usd=mean[g]))
    return pd.DataFrame(out)


def nest_gdp_factor(I):
    acc, accg = I["account"], I["account_gdp"]
    return float((accg.native_production_gain_bn + accg.other_immigrant_production_gain_bn)
                 / (acc.native_production_gain_bn + acc.other_immigrant_production_gain_bn))


# ================================================================== the group itself (step 6)
GENERATIONS = (("G1", "the first generation (born in Mexico)"),
               ("G2", "the second generation (US-born, a parent born in Mexico)"),
               ("G3plus", "the third-plus generation (US-born of US-born parents)"))


def generation_split(fin):
    """The generation lane's split of the case (generation_results.csv at the case's commit), both
    conventions for children; gated to add to the band ends. Where that file holds a later case, the
    case's split is the generation_summary.json entry named by CASES gen_split at the same commit, with
    the members from the results file (the CPS frame does not change with the case). Yields
    NAS-convention values with convention (a) beside."""
    g = pd.read_csv(io.BytesIO(read_input("generations"))).set_index(["convention", "generation", "band_end"])
    if CASE["gen_split"]:
        split = json.loads(git_show(f"{GEN_REL}/generation_summary.json", CASE["gen"]))[CASE["gen_split"]]
        for conv, gen, end in g.index:
            g.loc[(conv, gen, end), "cost_bn"] = float(split[conv][gen][end][f"{CASE['case']}_bn"])
    ends = fin[CASE["model"]]["ends"]
    for conv in ("a", "b"):
        for end in ("low", "high"):
            tot = float(sum(g.loc[(conv, gen, end), "cost_bn"] for gen, _ in GENERATIONS))
            gate(f"generation_split_adds_to_band_{conv}_{end}", np.isclose(tot, ends[end]["cost_bn"], atol=1e-3),
                 generations=tot, band=ends[end]["cost_bn"])
    for gen, lab in GENERATIONS:
        b = {end: float(g.loc[("b", gen, end), "cost_bn"]) for end in ("low", "high")}
        b["members"] = float(g.loc[("b", gen, "low"), "population"])
        yield (b, lab, float(g.loc[("a", gen, "low"), "population"]), float(g.loc[("a", gen, "low"), "cost_bn"]),
               float(g.loc[("a", gen, "high"), "cost_bn"]))


def row4_group_weights(B, d):
    """The group's own frame on the account's count (CASES group_weights "row4", September 29 on): the person weights
    with the base lane's row-4 rule (row4_nest_rows), the same mask and factors as the generation account's
    v4_inputs.py. The Mexico-born naturalized and noncitizen outside California and Texas take production_row4.json's
    factors, and no other resident moves. Gates: the grid file is the one the case's payload pins; each cell's records
    and CPS population are the grid file's; only group records move; the group's count is the account's row-4 count
    (populations.row4, 1e-9 relative)."""
    prod = B.fiscal_totals(CASE["case"])["adopted"]["production"]
    grid_file = FISCAL / prod["grid"]["file"]
    gate("row4_group_grid_file_is_the_payload_s", file_sha(grid_file) == prod["grid"]["sha256"], file=prod["grid"]["file"])
    r4 = json.loads(grid_file.read_text())
    pw, civ, tgt = d.pw.to_numpy(), d.civ.to_numpy(), d.target.to_numpy()
    outside = ~np.isin(d.st.to_numpy(), B.ROW4_EXCLUDED_STATES)
    factor = np.ones(len(d))
    for status, label in B.ROW4_STATUS.items():
        m = (d.PENATVTY.eq(MEXICO_BIRTHPLACE) & d.PRCITSHP.eq(status)).to_numpy() & outside
        f = r4["row4_factors"][label]
        gate(f"row4_group_{label}_is_the_grid_file_s", int(m.sum()) == f["records"]
             and np.isclose(pw[m].sum(), f["cps_population"], rtol=1e-9, atol=0),
             records=int(m.sum()), frame=pw[m].sum(), grid_file=f["cps_population"])
        gate(f"row4_group_{label}_moves_only_the_group", not np.any(m & civ & ~tgt))
        factor[m] = f["factor"]
    w4 = pw * factor
    n4 = float(w4[tgt].sum())
    gate("row4_group_count_is_the_account_s", np.isclose(n4, r4["populations"]["row4"], rtol=1e-9, atol=0),
         frame=n4, account=r4["populations"]["row4"])
    return w4, dict(members_m=n4 / 1e6, published_members_m=float(pw[tgt].sum() / 1e6),
                    factors={label: r4["row4_factors"][label]["factor"] for label in B.ROW4_STATUS.values()},
                    grid_file=prod["grid"]["file"])


LINEAGE_RULE = ("the added people (descendants who no longer report Mexican origin, counted whole) are not in the CPS as "
                "group members, so each identified third-plus-generation member's row-4 weight is raised by added / "
                "identified G3+, which places them at the identified G3+ members' distribution [ASSUMPTION: the account "
                "prices some of them at G3+ members' amounts and the rest at third-plus non-Hispanic whites' amounts at "
                "the G3+'s ages (meta.lineage.members); here all of them take the G3+ members' records]; the other "
                "residents keep the CPS frame, in which the added people sit unfound, as the distribution lane leaves them")
# From October 7 (main case v6, item added_age_mix) the case prices the added people at their measured ages
# (meta.lineage.age_mix), so the raise is by five-year age band.
LINEAGE_AGE_RULE = ("the added people (descendants who no longer report Mexican origin, counted whole) are not in the CPS "
                    "as group members, so each identified third-plus-generation member's row-4 weight is raised by the "
                    "added people of its five-year age band over the identified G3+ of that band, the added people taken "
                    "at the case's measured mixes (meta.lineage.age_mix: the G3-rate persons and the later losses, each at "
                    "its own mix), which places them at the identified G3+ members' records of their own ages "
                    "[ASSUMPTION: the account prices the white end of the G3-rate blend at third-plus non-Hispanic whites' "
                    "amounts (meta.lineage.members); here all of them take the G3+ members' records, band by band]; the "
                    "other residents keep the CPS frame, in which the added people sit unfound, as the distribution lane "
                    "leaves them")


def age_band_factors(d, w4, g3, lineage):
    """Per-record factors on the identified G3+ that add the added people at their measured age mix (LINEAGE_AGE_RULE):
    for five-year band b (A_AGE // 5, the last band open), 1 + (at_g3_rate x mix_g3_rate[b] + later_losses x
    mix_later[b]) / the identified G3+'s row-4 weight in b. Gates: the parts add to the added count, each mix sums to 1,
    the frame's bands are the case's, every band the added people reach holds identified records, the added people on
    the frame are each band's target (1e-9 relative), and the frame's identified G3+ has the case's identified mix
    (1e-6, a positive control that both read the same members). Returns the factors and a record."""
    am, counts = lineage["age_mix"], lineage["counts"]
    bands, mixes = am["bands"], am["mixes"]
    nb = len(bands)
    gate("age_mix_bands_are_five_years_to_an_open_top", bands == [f"{5 * b}-{5 * b + 4}" for b in range(nb - 1)]
         + [f"{5 * (nb - 1)}+"], bands=bands)
    parts = {"g3_rate": counts["at_g3_rate"], "later": counts["later_losses"]}
    gate("age_mix_parts_add_to_the_added", np.isclose(sum(parts.values()), counts["added"], rtol=1e-12, atol=0)
         and all(np.isclose(sum(mixes[k]), 1, rtol=0, atol=1e-12) and min(mixes[k]) >= 0 for k in (*parts, "identified")),
         parts=parts, added=counts["added"])
    band = np.minimum(d.A_AGE.to_numpy() // 5, nb - 1)
    ident = np.array([float(w4[g3 & (band == b)].sum()) for b in range(nb)])
    target = sum(n * np.asarray(mixes[k], float) for k, n in parts.items())
    gate("age_mix_bands_hold_identified_records", bool(np.all((ident > 0) | (target == 0))),
         empty_bands=[bands[b] for b in range(nb) if ident[b] == 0 and target[b] > 0])
    per_band = 1 + np.divide(target, ident, out=np.zeros(nb), where=ident > 0)
    f = np.where(g3, per_band[band], 1.0)
    added = np.array([float((w4 * (f - 1))[g3 & (band == b)].sum()) for b in range(nb)])
    gate("age_mix_added_people_by_band_are_the_case_s", np.allclose(added, target, rtol=1e-9, atol=0),
         max_rel_diff=float(np.max(np.abs(added - target) / np.where(target > 0, target, 1))))
    # Positive control: the frame's identified G3+ has the case's identified mix (the same records and weights).
    mix_gap = float(np.max(np.abs(ident / ident.sum() - np.asarray(mixes["identified"], float))))
    gate("age_mix_identified_mix_is_the_frame_s", mix_gap < 1e-6, max_abs_diff=mix_gap)
    return f, dict(rule=LINEAGE_AGE_RULE, bands=bands, band_factors=[float(x) for x in per_band],
                   added_by_band_m=[float(x) / 1e6 for x in target], identified_mix_frame_vs_case_max_abs_diff=mix_gap,
                   source=f"{CASE['lane']}/derived/corrections.json meta.lineage.age_mix ({am['reading']}, {am['route']})")


def lineage_group_weights(B, d):
    """The group's own frame on the lineage the case counts (CASES group_weights "lineage", October 5 on): the row-4
    weights (row4_group_weights), with the added people placed at the identified third-plus generation's records
    (LINEAGE_RULE; from October 7, where the case prices them at their measured ages, band by band: age_band_factors).
    The counts are the case's (its corrections.json meta.lineage.counts). G3+ is the generation account's mask: US-born,
    both parents born in US areas, Mexican origin (PRDTHSP 1), inside the group.
    Gates: the group on row 4 is the account's union and its G3+ the identified G3+ (1e-9 relative); the lineage is the
    union plus the added people and the generation split's G3+ is identified plus added (1e-9 relative); only G3+
    records move."""
    w4, g4 = row4_group_weights(B, d)
    lineage = json.loads((FISCAL / CASE["lane"] / "derived/corrections.json").read_text())["meta"]["lineage"]
    counts = lineage["counts"]
    tgt = d.target.to_numpy()
    g3 = tgt & d.PRCITSHP.isin([1, 2, 3]).to_numpy() & d.PEMNTVTY.isin(US_AREAS).to_numpy() \
        & d.PEFNTVTY.isin(US_AREAS).to_numpy() & d.PRDTHSP.eq(1).to_numpy()
    n4, n3 = float(w4[tgt].sum()), float(w4[g3].sum())
    gate("lineage_group_union_is_the_account_s", np.isclose(n4, counts["account_union"], rtol=1e-9, atol=0),
         frame=n4, account=counts["account_union"])
    gate("lineage_group_g3plus_is_the_identified_g3plus", np.isclose(n3, counts["identified_g3plus"], rtol=1e-9, atol=0),
         frame=n3, case=counts["identified_g3plus"], records=int(g3.sum()))
    ages = None
    if "age_mix" in lineage:
        factor, ages = age_band_factors(d, w4, g3, lineage)
    else:
        factor = 1 + counts["added"] / n3
    w = np.where(g3, w4 * factor, w4)
    n = float(w[tgt].sum())
    g = pd.read_csv(io.BytesIO(read_input("generations"))).set_index(["convention", "generation", "band_end"])
    g3_split = float(g.loc[("a", "G3plus", "low"), "population"])
    gate("lineage_group_count_is_the_lineage", np.isclose(n, counts["lineage_population"], rtol=1e-9, atol=0)
         and np.isclose(float(w[g3].sum()), g3_split, rtol=1e-9, atol=0), frame=n, lineage=counts["lineage_population"],
         g3plus_frame=float(w[g3].sum()), g3plus_generation_split=g3_split)
    gate("lineage_group_moves_only_g3plus", np.array_equal(w != w4, g3 & (w4 > 0)))
    label = [f"{x / 1e6:.1f}m" for x in (n, n4, counts["added"])]
    gate("lineage_counterfactual_label_counts", all(x in CF_LINEAGE for x in label), label=CF_LINEAGE, counts=label)
    info = dict(g4, members_m=n / 1e6, row4_members_m=n4 / 1e6, identified_g3plus_m=n3 / 1e6,
                added_m=counts["added"] / 1e6, priced_as_g3plus_m=lineage["members"]["g3plus"] / 1e6,
                priced_as_white_m=lineage["members"]["white"] / 1e6, g3plus_factor=factor,
                g3plus_records=int(g3.sum()), rule=LINEAGE_RULE,
                counts_source=f"{CASE['lane']}/derived/corrections.json meta.lineage")
    if ages is not None:
        # By age band the factor differs by record; the record's factor is then the G3+ members after over before. Beside
        # it, the added people as v5's single factor would place them, the rule's alternative.
        flat = np.where(g3, w4 * (1 + counts["added"] / n3), w4)
        age, earn = d.A_AGE.to_numpy(), np.maximum(d.PEARNVAL.to_numpy(float), 0)

        def added_people(ww):
            a = (ww - w4)[g3]
            return dict(under_20_share=float(a[age[g3] < 20].sum() / a.sum()), earnings_bn=float((a * earn[g3]).sum() / 1e9))
        ages = dict(ages, added_people=added_people(w), added_people_at_one_factor=dict(
            added_people(flat), factor=1 + counts["added"] / n3))
        info.update(g3plus_factor=float(w[g3].sum()) / n3, rule=LINEAGE_AGE_RULE, age_bands=ages)
    return w, info


def group_frame(B, d, I, fin, pw=None):
    """The group's own rows, on the person weights pw (default: the CPS's published weights, d.pw)."""
    pw, tgt = (d.pw.to_numpy() if pw is None else pw), d.target.to_numpy()
    N = pw[tgt].sum()
    rows = []

    def add(item, lo, c, hi, basis, note, per=N, kind="the group's gain or loss"):
        rows.append(dict(item=item, kind=kind, bn_low=lo, bn_central=c, bn_high=hi,
                         usd_per_member_central=(c * 1e9 / per) if c is not None and per else np.nan,
                         basis=basis, note=note))
    A1 = fin[CASE["model"]]["A_one_definition"]
    A = {"low": -A1["low"], "high": -A1["high"]}
    capped = fin[CASE["model"]].get("capped")
    add("direct fiscal transfer received: the direct response A, sign flipped", A["low"],
        (A["low"] + A["high"]) / 2, A["high"],
        f"[CALCULATION: distribution_weights_2026_09_23 fiscal_totals('{CASE['case']}'); engine run in specs.cjs]",
        "low and high are the low- and high-cost band ends; the production gain P goes to other residents and "
        "the induced receipts F to budgets, so neither is a transfer to the group"
        + ("" if not capped else "; from September 27 A includes the return on the public capital the group's use "
           "is charged, {:.2f} / {:.2f}bn, and the capped programs' slots it holds, {:.2f}bn, which without it go "
           "to eligible households now without the aid".format(
               *capped["capital_return"], sum((v[0] + v[1]) / 2 for v in capped["programs"].values()))))
    gen_src = (f"generation_account_2026_09_24/derived/generation_summary.json {CASE['gen_split']}, git {CASE['gen']}"
               if CASE["gen_split"] else f"generation_account_2026_09_24/derived/generation_results.csv, git {CASE['gen']}")
    for g, lab, n_a, lo_a, hi_a in generation_split(fin):
        add(f"the account's net cost to other residents attributed to {lab}, minors with their parents (NAS 2017)",
            g["low"], (g["low"] + g["high"]) / 2, g["high"], f"[CALCULATION: {gen_src}]",
            "the account's own split with no reference group: a cost to other residents, not the group's gain; "
            "never netted against other residents' rows and never the September 19 ledger's gaps; children in "
            f"their own generation: {lo_a:.1f} / {hi_a:.1f}bn at the low / high end ({n_a / 1e6:.2f}m members) "
            "[FRAMING-SENSITIVE]", per=g["members"], kind="the account's split by generation")
    earn = np.maximum(d.PEARNVAL.to_numpy(float), 0)
    fb = tgt & d.PRCITSHP.isin([4, 5]).to_numpy()
    g1 = fb & d.PENATVTY.eq(MEXICO_BIRTHPLACE).to_numpy()
    E1 = float((pw * earn)[g1].sum() / 1e9)
    gain = {L: E1 * (1 - 1 / PLACE_PREMIUM_RE[L]) for L in LEVELS}
    add("first generation (born in Mexico): market gain over the same person's earnings in Mexico", gain["low"],
        gain["central"], gain["high"],
        "[SOURCE: Clemens, Montenegro & Pritchett, HKS RWP09-004 (2009), sec. 3.3 and Table 8] x "
        "[DATA: CPS ASEC 2025 PEARNVAL of Mexico-born members]",
        f"US earnings {E1:.1f}bn x (1 - 1/Re), Re = 2.08 / 2.46 / 2.79 (PPP wage ratio for the same worker); "
        f"{pw[g1].sum() / 1e6:.2f}m members born in Mexico; same employment and hours assumed [INFERENCE]",
        per=pw[g1].sum())
    if pw[fb & ~g1].sum() > 0:
        add("foreign-born members born outside Mexico", None, None, None, "not computed",
            f"{pw[fb & ~g1].sum() / 1e6:.2f}m members; no Mexico counterfactual applies", per=None)
    g23 = tgt & ~fb
    add("second and third-plus generations (US-born)", None, None, None, "no counterfactual in Mexico",
        f"{pw[g23].sum() / 1e6:.2f}m members; they were born here, so no place premium exists and none is invented",
        per=None)
    # Wage competition among the group's own workers: each worker's wage falls by the same percentage
    # as other workers in its nativity branch and skill cell (the account's nest) [INFERENCE].
    hga = d.A_HGA.to_numpy()
    cells = [(hga >= 31) & (hga <= 39), (hga >= 40) & (hga <= 46)]
    native = d.PRCITSHP.isin([1, 2, 3]).to_numpy()
    for lab, row in (("epsilon infinite (account)", I["account"]), ("epsilon 3", I["eps3_hs"])):
        parts = {}
        for tag, br in (("native", native), ("other_fb", ~native)):
            for c in (0, 1):
                m = tgt & br & cells[c]
                w_ = row[f"wage_pct_{tag}_cell{c}"] / 100
                parts[(tag, c)] = float((pw * (-w_) * earn * (1 - B.TAU[c]))[m].sum() / 1e9)
        low_skill = parts[("native", 0)] + parts[("other_fb", 0)]
        high_skill = parts[("native", 1)] + parts[("other_fb", 1)]
        # Low end cash earnings, high end the GDP normalization's uniform scale, central their mean,
        # as the account pairs its two band ends.
        gf = nest_gdp_factor(I)
        add(f"wage competition among the group's own workers, high school or less, after tax ({lab})",
            low_skill, low_skill * (1 + gf) / 2, low_skill * gf,
            "[CALCULATION: account nest wage changes x CPS earnings of members]",
            f"cash: US-born members {parts[('native', 0)]:.2f}bn, foreign-born {parts[('other_fb', 0)]:.2f}bn; "
            f"high end x{gf:.4f} (GDP normalization)")
        add(f"wage gain of the group's own workers, some college or more, after tax ({lab})",
            high_skill, high_skill * (1 + gf) / 2, high_skill * gf,
            "[CALCULATION: account nest wage changes x CPS earnings of members]",
            f"cash: US-born {parts[('native', 1)]:.2f}bn, foreign-born {parts[('other_fb', 1)]:.2f}bn")
    ig = ingroup_victims(B)
    add("victims inside the group (excluded from the victim lane), full cost, equal footing", None,
        -ig["full_equal_bn"], None,
        "[CALCULATION: crime_victim_cost_2026_09_23/derived/cost_by_victim_and_offence_central.csv]",
        f"{ig['homicides']:.0f} homicides and {ig['nonfatal_victimisations']:.0f} non-fatal victimisations a "
        f"year; tangible {-ig['tangible_equal_bn']:.2f}bn. The victim lane's rows are on the equal footing (the "
        "footing of its $28.92bn); no lane computed this figure on the custody footing or with the mixed-group "
        "correction. Police records (NIBRS TX+AZ) put more of the group's victims in-group than NCVS, which "
        "would raise it"),
    rem = banxico_remittances()
    add("remittances received in Mexico from the United States, 2024 (context, not a US resident's gain or loss)",
        None, rem["us_bn"], None, "Banxico CE167, US-origin receipts, revised [SOURCE: Banxico SIE table CE167, "
        "series SE43675/SE43738, read from consumption_key_2026_09_24/_cache/sources/corridor/"
        "banxico_CE167_2022_2025.xlsx as remittance.py primary_flows() reads it]",
        ("all countries {:.2f}bn, the United States {:.2%} of it; ".format(rem["total_bn"], rem["us_share"])
         if rem["total_bn"] else rem["source"] + "; ")
        + "sent from the United States overall, not only by the group. The consumption lane's corridor "
        "(consumption_key_2026_09_24, 6841b39) needs {:.1f} times the surveyed sending amount (CEMLA ${:,.0f} a "
        "year), so it includes flows beyond the CPS households".format(rem["corridor_over_cemla"], rem["cemla_usd"]),
        per=None)
    return pd.DataFrame(rows), ig, dict(g1_members_m=float(pw[g1].sum() / 1e6), g1_earnings_bn=E1,
                                        members_m=float(N / 1e6), remittances=rem)


# ================================================================== registry (step 1)
CF = "2024, with vs without the 40.9m CPS Mexican-origin residents (stationary)"
# From September 29 (CASES group_weights "row4") the group is the account's count.
CF_ROW4 = ("2024, with vs without the 39.7m Mexican-origin residents the account prices (audit row 4; the CPS's "
           "published weights give 40.9m) (stationary)")
# From October 5 (group_weights "lineage") the group is the lineage the case counts.
CF_LINEAGE = ("2024, with vs without the 42.8m people of Mexican-origin lineage the account prices: the 39.7m who report "
              "Mexican origin (audit row 4) and 3.0m descendants who no longer do, counted whole (stationary)")


def counterfactual() -> str:
    return {"row4": CF_ROW4, "lineage": CF_LINEAGE}.get(CASE.get("group_weights"), CF)


def registry(T, meta, fin, sister_tbl, role_only=None):
    rows = []
    role_only = role_only or {}

    def row(id_, label, v, who, relation, in_net, source, ladder, status, note=""):
        lo, c, hi = (None, None, None) if v is None else (v["low"], v["central"], v["high"])
        rows.append(dict(id=id_, label=label, bn_low=lo, bn_central=c, bn_high=hi, who=who, relation=relation,
                         in_net=in_net, counterfactual=counterfactual(), source_lane=source, ladder=ladder, status=status,
                         date=CASE["date"], note=note))
    f = meta["fiscal"]
    e = fin[CASE["model"]]["ends"]
    lv = lambda fn: {L: fn(L) for L in LEVELS}
    band = {"low": -e["low"]["cost_bn"], "high": -e["high"]["cost_bn"]}
    band["central"] = (band["low"] + band["high"]) / 2
    row("main_case", "Adopted main case, other residents' net (fiscal + wages)", band, "fiscal + wages",
        "total", "account", f"{CASE['lane']} (main_case_bands.csv) via specs.cjs", CASE["ladder"], "adopted",
        f"low and high are the band ends ${-band['low']:.3f}-{-band['high']:.3f}bn; central is their midpoint")
    st = meta["social_totals"]
    pt = meta["published_totals"]
    published = (f"published pairing instead (ruling 5; {CASE['published']} real_costs_totals.csv section 7): "
                 "equal footing {:.1f}-{:.1f}bn with justice on its raw-coding key, custody footing {:.1f}-{:.1f}bn; "
                 "published range {:.0f}-{:.0f}bn").format(*pt["equal"], *pt["custody"], *pt["range"])
    row("account_plus_social",
        "Allocation base: adopted fiscal band + decision 4 victims (mixed footing), not a published total",
        {"low": band["low"] + st["items_central"], "central": band["central"] + st["items_central"],
         "high": band["high"] + st["items_central"]}, "persons and future taxpayers", "allocation base", "social",
        "this lane", "", "adopted", "what the person nets allocate: social items " + ", ".join(SOCIAL) + " at central "
        f"values, victims' harm at decision 4's {meta['crime']['mixed_equal']:.2f}bn (equal footing) beside a fiscal "
        "band that charges justice by the custody ratio; housing at the metro-local central; low and high are the "
        "fiscal band ends; " + published)
    row("account_plus_social_span",
        "Allocation base, every choice low or every choice high (mixed footing), not a published total",
        {"low": st["least_costly"], "central": band["central"] + st["items_central"], "high": st["most_costly"]},
        "persons and future taxpayers", "allocation base", "social", "this lane", "", "adopted",
        "stacks: fiscal and wages by band end, every other item at its least or most costly level; the published "
        "full span is {:.1f}-{:.1f}bn (real_costs_totals.csv section 7 full_span)".format(*pt["span"]))
    for id_, label, v_, note in (
            ("published_total_equal_footing", "Published total at central values, equal footing (justice on its "
             f"raw-coding key; victims ${pt['equal_victims']:.2f}bn, decision 4)", pt["equal"],
             "fiscal band {:.1f}-{:.1f}bn (band variant justice_raw_coding)".format(*pt["equal_fiscal"])),
            ("published_total_custody_footing", "Published total at central values, custody footing (victims "
             f"${pt['custody_victims']:.2f}bn)", pt["custody"],
             "fiscal band {:.1f}-{:.1f}bn, the adopted band".format(*pt["custody_fiscal"]))):
        row(id_, label, {"low": -v_[0], "central": -(v_[0] + v_[1]) / 2, "high": -v_[1]},
            "persons and future taxpayers", "total (published)", "no",
            f"{CASE['published']} (real_costs_totals.csv section 7)", "", "published",
            note + "; low and high are the fiscal band ends, central their midpoint")
    inside_key = ("" if CASE["consumption_proposal"] else "; the consumption key corrected for saving and remittances "
                  "(ladder 225) is inside this case, so it sits in this row")
    capped = CASE.get("capped")
    row("fiscal", "Fiscal: direct response A plus induced receipts F" if not capped else
        "Fiscal: direct response A less the capped programs, plus induced receipts F",
        lv(lambda L: -(f[L]["cost"] - (f[L]["displaced"] if capped else 0.0))),
        "a: federal_taxes (today's part) + state_local_taxes within the group's states; b: per_person, "
        "state-local part per person within the group's states", "inside", "account",
        f"A: distribution_weights_2026_09_23 fiscal_totals('{CASE['case']}') at {CASE['base']}; F: {CASE['lane']} "
        "via specs.cjs", CASE["ladder"], "adopted",
        "same band-end specifications as main_case; A differs from the engine run by {:.1e} / {:.1e}bn (rounding "
        "of the rebuilt band)".format(*meta["fiscal_A"][CASE["model"]]["diff"].values()) + inside_key
        + ("; from September 27 the taxpayers' channel: the capped programs (rental assistance, LIHEAP) fall on "
           "eligible non-recipients, the displaced_beneficiaries row, so fiscal + displaced_beneficiaries + wages is "
           "main_case; its financing parts are fiscal_cash, future_taxpayers and fiscal_resource" if capped else ""))
    row("fiscal_federal_today", "Fiscal, federal part financed by today's taxes", lv(lambda L: -f[L]["federal_today"]),
        "a: federal_taxes; b: per_person", "overlaps:fiscal", "account",
        f"debt_legacy_2026_09_23 federal_split_2024.csv at {CASE['debt']}", "207", "adopted",
        "part of the fiscal row; the debt lane's split, one definition per correction")
    row("fiscal_state_local", "Fiscal, state and local part", lv(lambda L: -f[L]["state_local"]),
        "a: state_local_taxes@group_states; b: per_person@group_states", "overlaps:fiscal", "account",
        f"fiscal row less the debt lane's federal part ({CASE['debt']})", "207", "adopted", "part of the fiscal row")
    row("future_taxpayers", "Fiscal, federal part financed by borrowing (FY2024 deficit / outlays)",
        lv(lambda L: -(f[L]["future"] - f[L].get("accrual", 0.0))), "future federal taxpayers; not allocated to today's persons",
        "overlaps:fiscal", "no", "OMB Historical Tables 2.1 and 3.1 (FY2027 release)", "", "adopted",
        f"share {meta['deficit']['share']:.4f} of the federal part [FRAMING-SENSITIVE]; bounds 0 and 1"
        + ("; from September 27 of the cash part only: the return on public capital is never borrowed"
           if CASE.get("capped") else ""))
    if CASE.get("accrual"):
        row("future_pension_accrual", "Fiscal, the pension accrual: benefits the group accrues, paid later",
            lv(lambda L: -f[L]["accrual"]), "future payers of Social Security and Medicare benefits; not allocated to "
            "today's persons", "overlaps:fiscal", "no", f"debt_legacy_2026_09_23 accrual_bn at {CASE['debt']}; "
            f"{CASE['lane']} change_at_fixed_specifications.item_pension", CASE["ladder"], "adopted",
            "the case less its cash set (social security and Medicare's Part A at the accrual at payable benefits, "
            "federal income tax net of the tax on benefits); nothing finances it in 2024, so it sits with the future "
            "taxpayers' part [FRAMING-SENSITIVE]; alternative: allocate it today on the federal tax key, as if the "
            "trust funds' later outlays were prefunded now")
    if CASE.get("capped"):
        cp = meta["capped_programs"]["amounts_bn"]
        keys = meta["capped_programs"]["keys"]
        row("fiscal_cash", "Fiscal, cash financing borne today", T["fiscal_cash_a"],
            "a: federal_taxes + state_local_taxes@group_states; b: per_person, state-local part @group_states",
            "overlaps:fiscal", "account", f"debt_legacy_2026_09_23 federal_split_2024.csv at {CASE['debt']} "
            "(fiscal_gap_bn, federal_bn)", "207, 239", "adopted",
            "the fiscal channel's cash part less the future taxpayers' part; it carries the enterprise surplus receipt "
            "(the enterprises' operating loss, at response 1) and TANF-type aid, a block grant states can move, so it "
            "keeps the financing conventions")
        row("fiscal_resource", "Fiscal, resource cost: the return on public capital, enterprise capital included",
            T["fiscal_resource_a"], "a: federal_taxes + state_local_taxes@group_states; b: per_person, state-local "
            "part @group_states", "overlaps:fiscal", "account", f"{CASE['lane']} evaluateFull via specs.cjs; "
            f"debt_legacy_2026_09_23 resource_cost_bn at {CASE['debt']}", "238, 239", "adopted",
            "an imputed cost at 2% real at the low end and 3% at the high end on the group's keyed share of 24 capital "
            "components; never borrowed, so none of it goes to future taxpayers; federal {:.2f} / {:.2f}bn at the band "
            "ends [FRAMING-SENSITIVE]".format(f["low"]["resource_federal"], f["high"]["resource_federal"]))
        row("displaced_beneficiaries", "Capped programs' displaced beneficiaries: rental assistance and LIHEAP",
            T["displaced_beneficiaries"], "eligible non-recipients: renter households below 50% of their state's median "
            "household income outside public or subsidized housing; households below 150% of the HHS 2024 poverty "
            "guideline without energy assistance (one share per household)", "inside", "account",
            f"distribution_weights_2026_09_23 capped_keys() and case_ends at {CASE['base']}; debt_legacy_2026_09_23 "
            f"displaced_bn at {CASE['debt']}", "239", "adopted",
            "the programs are capped and rationed, so without the group eligible households now going without take "
            "its slots: the cost falls on them under both conventions, not on taxpayers; rental assistance {:.2f}bn "
            "({:.2f}m eligible non-recipient households), LIHEAP {:.2f}bn ({:.2f}m); proxies: HUD's very-low-income "
            "limit, 50% of area median family income (24 CFR 5.603, 982.201(b)), taken at the state median household "
            "income; LIHEAP's 150% of poverty (42 U.S.C. 8624(b)(2)(B); 89 FR 2961) without its 60%-of-state-median "
            "alternative".format(cp["housing_subsidies"]["central"],
                                 keys["housing_subsidies"]["eligible_non_recipient_households_m"],
                                 cp["energy_assistance"]["central"],
                                 keys["energy_assistance"]["eligible_non_recipient_households_m"])
            + ("; from September 29 public housing's enterprise deficit too, {:.2f}bn, rationed like rental assistance "
               "and keyed to its eligible non-recipients".format(cp["housing_enterprise_surplus"]["central"])
               if "housing_enterprise_surplus" in cp else ""))
        # The inside rows add to main_case (A from fiscal_totals, so to its rounding, as the band-end gate).
        inside = {L: -(f[L]["cost"] - f[L]["displaced"]) + T["displaced_beneficiaries"][L] + T["wages"][L] for L in LEVELS}
        gate("registry_inside_rows_sum_to_main_case", all(abs(inside[L] - band[L]) < 1e-3 for L in LEVELS),
             inside=inside, main_case=band)
    row("wages", "Wages after tax, long run (account's split: high school or less; sigma 2, epsilon infinite)",
        T["wages"], "account_wage_cells (other residents' earnings by nativity branch and skill cell)", "inside",
        "account", "production_nativity_nest_2026_09_22; wage_distribution_2026_09_23", "176, 191", "adopted",
        "the production term P; GDP normalization at the low-cost end")
    row("wages_eps3", "Wages after tax, epsilon 3 between natives and immigrants", T["wages_eps3"],
        "account_wage_cells", "overlaps:wages", "no", "production_nativity_nest_2026_09_22", "176, 181, 191",
        "proposed", "induced receipts change by {:+.2f}bn (central), financed by the convention".format(
            meta["wages_eps3_delta_F"]["central"]))
    row("wages_below_ba", "Wages after tax, below-BA split (ladder 194's central), cash", T["wages_below_ba_cash"],
        "below_ba_wage_cells", "overlaps:wages", "no", "distribution_weights_2026_09_23", "194", "proposed",
        "not the account's split, so it cannot close to the headline")
    ca = meta["care_hours"]
    c = pd.read_csv(PATHS["care"]).set_index("channel")
    cs = c.loc["consumer surplus on immigrant-intensive services, net of native low-skill wage gain"]
    row("care", "Care and household services (hours taxes, elder care, output)", ca["total"],
        "inside the fiscal row, spread by the financing convention", "overlaps:fiscal", "account",
        "care_household_services_2026_09_23", "198", "adopted",
        f"inside since September 24 (lane_constants -4.15); taxes on native women's extra hours {ca['taxes_bn']:.2f}bn")
    row("care_women_extra_hours", "Native women's after-tax earnings from the extra hours (display)",
        T["care_women_after_tax_earnings"], "US-born other-resident women in the top wage quartile of their "
        "census division (CPS {:.2f}m; lane 14.37m in the ACS)".format(ca["cps_women_m"]), "overlaps:care", "no",
        "care_household_services_2026_09_23", "198", "adopted",
        "their private gain is about zero (envelope: the hours trade off leisure and home production); the taxes "
        "on the hours go to budgets inside the fiscal row")
    row("care_consumer_surplus", "Consumer surplus on immigrant-intensive services, net (side view)",
        {"low": float(cs.low_bn), "central": float(cs.central_bn), "high": float(cs.high_bn)},
        "consumers of household services", "overlaps:wages", "no", "care_household_services_2026_09_23", "198",
        "adopted", "the expenditure side of P; never added")
    row("consumer_prices", "Consumer prices, CEX side view (Cortes 2008 published)", T["consumer_prices"],
        "cex_quintile (money-income quintiles, per person)", "overlaps:wages", "no",
        "consumer_price_benefit_2026_09_18", "194", "adopted", "overlaps the production term; never added")
    hs = meta["housing"]
    lvl_note = (f"levels follow ladder 190's net for other residents: low = {hs['low']['row']}; central = "
                f"{hs['central']['row']}; high = {hs['high']['row']}. Low and high are spread by the form-A arm "
                "with the same elasticity and geography, scaled to their totals (x{:.4f} and x{:.4f}) "
                "[INFERENCE]".format(hs["low"]["pattern_scale"], hs["high"]["pattern_scale"]))
    row("renters", "Renters' extra rent, long run (ladder 190)", T["renters"],
        "renters raked to ACS extra rent by income cell and state", "beside", "social",
        "housing_transfer_2026_09_23", "190", "adopted", lvl_note)
    row("landlords", "Landlords' extra rent receipts less the surplus triangle (ladder 190)", T["landlords"],
        "landlords (CPS rental income) raked to the base's ACS-INTP/SCF income profile and the rent states",
        "beside", "social", "housing_transfer_2026_09_23", "190", "adopted",
        "same levels as renters; landlords assumed local [INFERENCE]")
    row("housing_net", "Housing net to other residents (renters + landlords)",
        lv(lambda L: T["renters"][L] + T["landlords"][L]), "renters and landlords", "overlaps:renters+landlords",
        "no", "housing_transfer_2026_09_23", "190", "adopted",
        "ladder 190: {:.2f}-{:.2f}bn across the two geography arms' centrals (national uniform, metro-local), "
        "span {:.2f} to {:+.2f}bn over the long-run grid".format(
            hs["national_uniform_central"]["net_bn"], hs["central"]["net_bn"], hs["low"]["net_bn"], hs["high"]["net_bn"]))
    nu = hs["national_uniform_central"]
    row("housing_net_national_uniform", "Housing net, national-uniform arm's long-run central (ladder 190's low end)",
        lv(lambda L: T["renters_national_uniform"][L] + T["landlords_national_uniform"][L]),
        "renters_national_uniform and landlords_national_uniform, raked like the central", "overlaps:renters+landlords",
        "no", "housing_transfer_2026_09_23", "190", "adopted",
        f"renters -{nu['renters_bn']:.2f}bn, landlords +{nu['landlords_bn']:.2f}bn; the net_shares rows "
        "'*_housing_national_uniform' swap it for the central")
    row("owner_value_stock", "Owner-occupiers' house-value gain (a one-time stock)", T["owner_value_stock"],
        "owners raked to ACS value by income cell and state", "apart", "no", "housing_transfer_2026_09_23", "190",
        "adopted", "a stock, not an annual flow; never added")
    cr = meta["crime"]
    fo = cr["footing"]
    row("crime_victims", "Crime victims' harm, full cost: decision 4's figure, the victim lane's envelope",
        T["crime_victims"], "ncvs_rank_risk@group_states (persons 12+ by victimisation risk)", "beside", "social",
        "crime_ratio_direction_2026_09_24; crime_victim_cost_2026_09_23", "189, 218", "adopted",
        f"central {cr['mixed_equal']:.2f}bn: {fo['mixed_equal']}; low {cr['envelope_low']:.2f}bn: {fo['envelope_low']}; "
        f"high {cr['envelope_high']:.2f}bn: {fo['envelope_high']}")
    row("crime_victims_equal_footing", "Crime victims' harm, equal footing (victim lane central)",
        T["crime_victims_equal_footing"], "ncvs_rank_risk@group_states", "overlaps:crime_victims", "no",
        "crime_victim_cost_2026_09_23", "189", "adopted", fo["equal"])
    row("crime_victims_custody_footing", "Crime victims' harm, custody footing (victim lane)",
        T["crime_victims_custody_footing"], "ncvs_rank_risk@group_states", "overlaps:crime_victims", "no",
        "crime_victim_cost_2026_09_23", "189", "adopted",
        fo["custody"] + "; the footing of the propagation lane's real-costs totals and of ladder 194's crime channel")
    row("crime_victims_national_key", "Crime victims' harm, decision 4's figure on the national key (no geography)",
        T["crime_victims_national_key"], "ncvs_rank_risk (national)", "overlaps:crime_victims", "no",
        "crime_ratio_direction_2026_09_24", "218", "adopted", fo["mixed_equal"])
    row("crime_victims_nibrs", "Crime victims' harm, NIBRS victim-conditional arm", {L: -cr["nibrs_equal"] for L in LEVELS},
        "not allocated", "overlaps:crime_victims", "no", "offender_ethnicity_nibrs_2026_09_23", "202", "adopted",
        fo["nibrs_equal"])
    row("property_crime", "Property crime, arrest-share proxy", T["property_crime"], "households@group_states",
        "beside", "social", "crime_victim_cost_2026_09_23", "189", "adopted", "proxy; no quality of life priced")
    row("unreimbursed_care", "Unreimbursed hospital care outside budgets", T["unreimbursed_care"],
        "privately_insured@group_uninsured_states", "beside", "social", "uncompensated_care_2026_09_23", "192",
        "adopted")
    if CASE.get("congestion") == "long_run":
        cg = meta["congestion"]
        be = cg["by_band_end"]
        row("congestion", "Road congestion, time and fuel, long run (lanes follow the highway response)", T["congestion"],
            "commuters@urban_area_states", "beside", "social",
            "service_response_long_run_2026_09_27 (congestion.py, net_change.json); congestion_2026_09_23", "237",
            "adopted", "re-derived from B1 ({:.2f}bn with lanes fixed): lanes cut uniformly over urban areas by {:.4f} "
            "at the low band end and {:.4f} at the high end, {:.2f} and {:.2f}bn; central is their mean, low the low "
            "end's factorial minimum ({:.2f}bn), high the high end's maximum ({:.2f}bn); a uniform cut offsets delay "
            "where the group is thin, so other residents gain in {} of the 50 states and DC at the low end ({}) and {} "
            "at the high end [INFERENCE]".format(cg["b1_lanes_fixed_bn"], be["low"]["lane_cut"], be["high"]["lane_cut"],
                                 be["low"]["central_bn"], be["high"]["central_bn"], be["low"]["range_bn"][0],
                                 be["high"]["range_bn"][1], len(be["low"]["states_with_a_gain"]),
                                 " ".join(be["low"]["states_with_a_gain"]), len(be["high"]["states_with_a_gain"])))
    else:
        row("congestion", "Road congestion, time and fuel (B1, lanes fixed)", T["congestion"],
            "commuters@urban_area_states", "beside", "social", "congestion_2026_09_23", "195", "adopted")
    row("mobility", "Mobility: local-shock insurance and Borjas's gain", T["mobility"],
        "insurance: US-born men with high school or less (earnings); Borjas: all earnings", "beside", "social",
        "labor_mobility_insurance_2026_09_23", "203", "adopted")
    row("preferences", "Race- and ethnicity-based preferences, whole regime, cost to white natives",
        T["preferences_regime"], "nh_white_natives (earnings)", "beside", "no", "affirmative_action_cost_2026_09_24",
        "213", "adopted", "most of it follows other groups' preferences, which the counterfactual keeps")
    if CASE.get("preferences") == "attribution":
        at = meta["preferences_attribution"]
        s = at["white_share_of_pool"]
        row("preferences_group_part", "Preferences attributed to Mexican-origin beneficiaries, white natives' part",
            T["preferences_group_part"], "nh_white_natives: earnings (BA+ for admissions), self-employment for lost "
            "profits, taxes for the price premium", "overlaps:preferences", "with_proposed",
            "affirmative_action_cost_2026_09_24", "213", "proposed",
            "an attribution, not a counterfactual removal: the Mexican-origin share of each channel's beneficiaries "
            "supplies neither the policy response nor the replacement allocation, so the row assumes a rule: "
            + at["rule"] + "; the DBE premium's part already in the fiscal channel since September 27 is netted "
            "(${:.1f}m of the group's ${:.1f}m, share {:.4f} = key share x highway response, mean of the band "
            "ends); {:.4f}bn before September 27 [FRAMING-SENSITIVE]".format(
                at["dbe_netted_bn"] * 1e3, at["dbe_premium_part_bn"] * 1e3, at["dbe_in_fiscal_channel_share"]["used"],
                -meta["preferences"]["group_part"]["central"]))
        row("preferences_group_part_others", "Preferences attributed to Mexican-origin beneficiaries, other included "
            "recipients' part under the same rule", T["preferences_group_part_others"],
            "the non-preferred pool less white natives: BA+ earnings of non-Hispanic, non-Black, non-AIAN graduates "
            "(admissions); earnings of non-Hispanic, non-Black earners (contractor hiring); self-employment and taxes "
            "of other residents who are not white natives", "overlaps:preferences", "with_proposed",
            "affirmative_action_cost_2026_09_24; this lane", "213", "proposed",
            "the rule's gain to the pool's other members without the group, a loss from its presence as every row "
            "here: the white natives' part x (1 - s) / s, s their share of the pool: admissions {:.4f} (freed "
            "seats' value {:.1f} / {:.1f}m to white natives / others at the central boundaries, same loss per "
            "worker), hiring {:.4f}, lost profits {:.4f}, premium {:.4f}; the freed elite seats that go to none of "
            "the four simulated groups (Espenshade-Chung {:.1%}, AKR's Harvard {:.1%}) are placed on the same pool "
            "[INFERENCE]"
            .format(s["admissions"], at["admissions_value_white_others"][0] / 1e6,
                    at["admissions_value_white_others"][1] / 1e6, s["contractor_hiring"], s["lost_profits"],
                    s["taxpayer_premium"], at["outside_groups"]["ec"], at["outside_groups"]["akr"]))
    else:
        row("preferences_group_part", "Preferences, part following Mexican-origin beneficiaries", T["preferences_group_part"],
            "nh_white_natives: earnings (BA+ for admissions), self-employment for lost profits, taxes for the price premium",
            "overlaps:preferences", "with_proposed", "affirmative_action_cost_2026_09_24", "213", "proposed",
            "the part the counterfactual removes")
    sc = meta["scale"]
    row("scale", "City size and schooling mix (Card-Rothstein-Yi, CZ 1990 joint)", sc["total"],
        "earnings@metro_states + receipts by the convention", "beside", "with_proposed",
        "scale_spillovers_2026_09_23", "201", "proposed", "would enter through P and receipts if adopted")
    db = meta["debt"]
    prev = CASE["prev"]
    row("debt_legacy", "Interest on past gaps (debt legacy)", T["debt_legacy_a"], "a: federal_taxes; b: per_person",
        "apart", "no", f"debt_legacy_2026_09_23 stocks.csv at {CASE['debt']} ({CASE['label']})", "207", "adopted",
        "a different object: interest on the stock built by past annual gaps; never added to the annual account; "
        f"rules range {db['rules_min']:.1f}-{db['rules_max']:.1f}; {prev['label']} "
        f"{db[prev['case']]['low']:.1f}-{db[prev['case']]['high']:.1f}")
    if CASE["consumption_proposal"]:
        cp = meta["consumption_proposal"]
        row("consumption_key_proposal", "Proposed change to the account's consumption key, −$4.1bn on the fiscal total",
            {"low": -cp["change"][0], "central": -(cp["change"][0] + cp["change"][1]) / 2, "high": -cp["change"][1]},
            "not allocated", "proposed change to the account (not adopted)", "no",
            "consumption_key_2026_09_24 (6841b39), spec both_corridor_net_h2", "", "proposed",
            "signed from other residents' side as every row: the fiscal cost falls by {:.2f}bn at both band ends (main "
            "case {:.1f}-{:.1f}bn); variants {:.1f} to {:.1f}bn, surveyed remittances {:.1f}bn; never in a net or the "
            "adopted total".format(-cp["change"][0], cp["band"][0], cp["band"][1], cp["both_max"], cp["both_min"],
                                   cp["survey"]))
    for lane, rid in SISTERS.items():
        s = sister_tbl[sister_tbl.lane == lane]
        if s.empty or (s.status == "pending").all():
            row(rid, f"Sister lane {lane}", None, "", "", "no", lane, "", "pending",
                s.note.iloc[0] if len(s) else "file absent at run time")
            continue
        alloc_ = s[s.status == "allocated"]
        other_cf = int((~s.counterfactual_is_absence.astype(bool)).sum())
        v = {L: float(sum(T[c][L] for c in alloc_.channel_id)) for L in LEVELS} if len(alloc_) else None
        row(rid, f"Sister lane {lane}: {len(s)} rows, {len(alloc_)} allocated", v,
            "; ".join(sorted(set(alloc_.key))) if len(alloc_) else "role table only", "beside",
            "with_proposed" if len(alloc_) else "no", lane, "", "proposed",
            (f"{LANE_LABELS[lane]}; " if len(alloc_) and lane in LANE_LABELS else "")
            + (f"{role_only[lane]}; " if lane in role_only else "")
            + f"allocated rows sum here; {other_cf} rows on other counterfactuals "
            "(sister_other_counterfactuals.csv); every row is in role_table.csv; lane verdict at run time: "
            + str(s.lane_verdict.iloc[0])[:60])
    return pd.DataFrame(rows)


# ================================================================== the page (step 7)
PAGE = [  # channel, label, basis, relation, who gains, who loses
    ("fiscal_a", "fiscal cost, tax-share financing (a)", "measured budgets, modelled response",
     "inside", "", "taxpayers today: federal tax share and state-local taxes in the group's states"),
    ("fiscal_b", "fiscal cost, per-person financing (b)", "measured budgets, modelled response",
     "inside", "", "every other resident equally (state-local part within the group's states)"),
    ("wages", "wages after tax (account's split)", "modelled (CES, sigma 2, epsilon infinite)", "inside",
     "workers with some college or more", "workers with high school or less"),
    ("renters", "rent", "measured rents, modelled elasticity", "beside", "", "renter households"),
    ("landlords", "rent receipts", "measured rents, modelled elasticity", "beside", "landlords", ""),
    ("crime_victims", "crime victims' harm", "measured incidents, modelled prices", "beside", "",
     "persons 12+, by victimisation risk, in the states where the group lives"),
    ("property_crime", "property crime (proxy)", "proxy", "beside", "", "households in the group's states"),
    ("unreimbursed_care", "unreimbursed hospital care", "measured uninsured share, assumed use", "beside", "",
     "privately insured (cost shifting), in the states with the group's uninsured"),
    ("congestion", "road congestion", "measured traffic shares, modelled delay", "beside", "",
     "metropolitan commuters in the congested urban areas' states"),
    ("mobility", "mobility insurance and Borjas's gain", "modelled", "beside",
     "US-born men with high school or less; all workers", ""),
    ("preferences_group_part", "preferences (Mexican-origin beneficiaries' part)", "modelled, weak evidence",
     "beside (proposed)", "", "US-born non-Hispanic whites"),
    ("scale_private", "city size and schooling mix, earnings part", "one regression", "beside (proposed)",
     "workers in the group's metros", "workers in the group's metros"),
]


def page_rows():
    """PAGE for the case: from September 27 the capped programs' row, the long-run congestion and the
    preferences as an attribution with the other recipients' part."""
    rows = list(PAGE)
    at = {r[0]: i for i, r in enumerate(rows)}
    if CASE.get("capped"):
        rows.insert(at["fiscal_b"] + 1, (
            "displaced_beneficiaries", "capped programs' slots (rental assistance, LIHEAP)",
            "measured outlays, modelled response, proxy eligibility", "inside", "",
            "eligible households without the aid: renters below 50% of state median income, households below 150% "
            "of poverty"))
    if CASE.get("congestion") == "long_run":
        rows[rows.index(PAGE[at["congestion"]])] = (
            "congestion", "road congestion, long run (lanes follow the highway response)",
            "measured traffic shares, modelled delay and lane response", "beside",
            "metropolitan commuters where the uniform lane cut outweighs the group's traffic",
            "metropolitan commuters in the congested urban areas' states")
    if CASE.get("preferences") == "attribution":
        i = rows.index(PAGE[at["preferences_group_part"]])
        rows[i] = ("preferences_group_part", "preferences attributed to Mexican-origin beneficiaries, white natives' "
                   "part", "modelled, weak evidence; an attribution under proportional replacement", "beside (proposed)",
                   "", "US-born non-Hispanic whites")
        rows.insert(i + 1, ("preferences_group_part_others", "preferences attributed to Mexican-origin beneficiaries, "
                            "other recipients' part", "modelled, weak evidence; an attribution under proportional "
                            "replacement", "beside (proposed)", "",
                            "the non-preferred pool's other members: Asian and foreign-born white graduates, other "
                            "non-Hispanic non-Black earners, other firms and taxpayers"))
    return rows


def page_table(d, ch, meta, gf, sister_tbl, role_only=None):
    role_only = role_only or {}
    pw, other = d.pw.to_numpy(), d.other.to_numpy()
    N_other = pw[other].sum()
    rows = []
    for name, label, basis, rel, who_g, who_l in page_rows():
        x = (pw * ch[name]["central"])[other]
        w = pw[other]
        for side, m, who in (("gain", x > 0, who_g), ("loss", x < 0, who_l)):
            if not m.any():
                continue
            bn = x[m].sum() / 1e9
            rows.append(dict(who=who or "(mixed)", gain_or_loss=side, bn_per_year=bn, persons_m=w[m].sum() / 1e6,
                             usd_per_person=bn * 1e9 / w[m].sum(), usd_per_other_resident=bn * 1e9 / N_other,
                             channel=label, basis=basis, inside_or_beside=rel, frame="other residents"))
    f = meta["fiscal"]["central"]
    rows.append(dict(who="future federal taxpayers (deficit-financed part)", gain_or_loss="loss",
                     bn_per_year=-(f["future"] - f.get("accrual", 0.0)), channel="fiscal cost, federal borrowing",
                     basis="measured deficit share", inside_or_beside="inside",
                     frame="future taxpayers, not allocated [FRAMING-SENSITIVE]"))
    if CASE.get("accrual"):
        rows.append(dict(who="future payers of Social Security and Medicare (the pension accrual)", gain_or_loss="loss",
                         bn_per_year=-f["accrual"], channel="fiscal cost, pension accrual",
                         basis="the case less its cash set", inside_or_beside="inside",
                         frame="future payers, not allocated [FRAMING-SENSITIVE]"))
    for r in gf.itertuples():
        if r.bn_central is None or (isinstance(r.bn_central, float) and np.isnan(r.bn_central)):
            continue
        if r.kind != "the group's gain or loss":      # the account's split by generation is not a gain
            continue
        rows.append(dict(who="the group: " + r.item, gain_or_loss="gain" if r.bn_central > 0 else "loss",
                         bn_per_year=r.bn_central, usd_per_person=r.usd_per_member_central, channel=r.item,
                         basis=r.basis, inside_or_beside="beside (group frame)", frame="the group"))
    for r in sister_tbl.itertuples():
        # Rows on other counterfactuals are listed in sister_other_counterfactuals.csv, not here.
        if getattr(r, "status", "") not in ("allocated", "role_only") or not r.counterfactual_is_absence:
            continue
        v = pd.to_numeric(r.bn_central, errors="coerce")
        sign = {"gain": 1.0, "loss": -1.0}.get(str(r.direction).strip().lower(), np.nan)
        basis = r.basis + (f" [{LANE_LABELS[r.lane]}]" if r.status == "allocated" and r.lane in LANE_LABELS else "")
        basis += f" [{role_only[r.lane]}]" if r.lane in role_only and r.note == role_only[r.lane] else ""
        rec = dict(who=f"{r.group} ({r.lane})", gain_or_loss=r.direction, bn_per_year=sign * abs(v),
                   channel=r.channel, basis=basis, inside_or_beside=r.relation_to_account,
                   frame=f"sister lane, {r.status}; lane verdict at run time: {r.lane_verdict[:40]}")
        if r.status == "allocated":
            x = (pw * ch[r.channel_id]["central"])[other]
            rec.update(persons_m=pw[other][x != 0].sum() / 1e6, usd_per_person=x.sum() / pw[other][x != 0].sum(),
                       usd_per_other_resident=x.sum() / N_other)
        rows.append(rec)
    return pd.DataFrame(rows)


def person_nets_by_cut(cuts):
    """Wide table: nets by the most telling cuts, central, both conventions."""
    keep = ["decile", "edu_nativity", "tenure", "age3", "race5", "state3", "industry5", "sex"]
    c = cuts[cuts.cut.isin(keep) & cuts.channel.str.startswith("net_") & (cuts.level == "central")]
    out = None
    for (name), g in c.groupby("channel"):
        g = g.set_index(["cut", "group"])
        part = g[["usd_per_person", "winners_share"]].rename(columns={
            "usd_per_person": f"{name}_usd_per_person", "winners_share": f"{name}_winners_share"})
        base = g[["persons_m", "households_m"]]
        out = base.join(part) if out is None else out.join(part)
    return out.reset_index()


def sources_manifest(B, base_sha):
    files = [("base distribute.py at " + CASE["base"], f"{BASE_REL}/distribute.py", base_sha)]
    for k, p in list(PATHS.items()) + [(f"base:{k}", v) for k, v in B.PATHS.items()]:
        p = Path(p)
        if k in PINNED:
            files.append((k, str(p.relative_to(ROOT)), sha(read_input(k))))
        elif p.is_file() and p.stat().st_size < 3e9:
            files.append((k, str(p.relative_to(ROOT)) if p.is_relative_to(ROOT) else str(p), file_sha(p)))
        elif p.exists():
            files.append((k, str(p.relative_to(ROOT)) if p.is_relative_to(ROOT) else str(p), "directory"))
    if CASE["gen_split"]:
        rel = f"{GEN_REL}/generation_summary.json"
        files.append((f"generations: {CASE['gen_split']} at {CASE['gen']}", rel, sha(git_show(rel, CASE["gen"]))))
    for c in (CASE["prev"], CASE):
        commit, sub = c["debt"], c.get("debt_dir")
        for name in ("federal_split_2024_lines.csv", "federal_split_2024.csv", "summary.json", "stocks.csv"):
            rel = lane_rel(DEBT_REL, sub, name)
            files.append((f"debt lane at {commit}", rel, sha(git_show(rel, commit))))
    for c in (CASE["prev"], CASE):
        commit, sub = c["base"], c.get("base_dir")
        for name in ("channel_by_quintile.csv", "inputs.json"):
            rel = lane_rel(f"{BASE_REL}/derived", sub, name)
            files.append((f"base {name} at {commit}", rel, sha(git_show(rel, commit))))
    if CASE.get("capped"):
        name = B.LATER_CASES[CASE["case"]].ends
        files.append((f"base {name} at {CASE['base']} (the working-tree copy is gated equal)",
                      f"{BASE_REL}/derived/{name}", sha(git_show(f"{BASE_REL}/derived/{name}", CASE["base"]))))
    for extra in ("crime_victim_cost_2026_09_23/derived/property_proxy.csv",
                  "care_household_services_2026_09_23/derived/hours_tax_specs.csv"):
        p = FISCAL / extra
        files.append((extra, str(p.relative_to(ROOT)), file_sha(p)))
    return pd.DataFrame(files, columns=["input", "path", "sha256"])


# ================================================================== main
def role_only_lanes(fin) -> dict:
    """Sister lanes whose allocatable rows stay in the role table under the case: school dilution
    when every specification of the case charges schools at a response of 1."""
    return ({"school_dilution_2026_09_24": SCHOOL_DILUTION_ROLE_ONLY}
            if (fin[CASE["model"]]["specs"].school == 1).all() else {})


def parse_args(argv=None):
    ap = argparse.ArgumentParser(description="Winners and losers across every priced channel, on one main case.")
    ap.add_argument("--case", choices=RUNNABLE, default=DEFAULT_CASE,
                    help=f"the main case to allocate (default {DEFAULT_CASE}); sept24 rebuilds the September 24 files")
    ap.add_argument("--out-dir", type=Path, default=None,
                    help="where specs.cjs wrote this case's engine runs and where outputs go (default derived/)")
    ap.add_argument("--dev-unpinned", action="store_true",
                    help="dry run only: read a case's uncommitted upstream files from the working tree (needs an "
                         "--out-dir outside derived/)")
    return ap.parse_args(argv)


def main():
    args = parse_args()
    configure(args.case, args.out_dir, args.dev_unpinned)
    DERIVED.mkdir(parents=True, exist_ok=True)
    CACHE.mkdir(exist_ok=True)
    print(f"[case] {CASE['case']} ({CASE['lane']}), after {CASE['prev']['case']}; outputs in {DERIVED}")
    print("[base] distribute.py at", CASE["base"])
    B, base_sha = load_base()
    d, top10 = load_frame(B)
    pw, other = d.pw.to_numpy(), d.other.to_numpy()
    print(f"  ✓ CPS frame: {pw[other].sum() / 1e6:.2f}m other residents, {pw[d.target.to_numpy()].sum() / 1e6:.2f}m group")
    I = base_inputs(B, d)
    regs = {}
    for case in (CASE["prev"]["case"], CASE["case"]):
        print(f"[regression] {case} inputs against the base's channel_by_quintile.csv at {CASES[case]['base']}")
        regs[case] = regression(B, d, I, case)
        print(f"  ✓ max |diff| {regs[case]['diff'].abs().max():.2e}bn over {len(regs[case])} cells")
    print("[fiscal] adopted case by specification, one-definition A, federal split, deficit share")
    fin = fiscal_inputs()
    fiscal_A = fiscal_one_definition(B, fin)
    for case, v in fiscal_A.items():
        print(f"  ✓ {case}: fiscal_totals A minus engine A {v['diff']['low']:+.1e} / {v['diff']['high']:+.1e}bn")
    fedsplit, fs_info = federal_split(fin)
    deficit = deficit_share_fy2024()
    print(f"  ✓ deficit share FY2024 {deficit['share']:.4f}")
    notes = {}
    print("[frame] allocating every channel to persons")
    ch, totals, meta, ctx = build_frame(B, d, I, fin, fedsplit, deficit, notes)
    meta["deficit"] = deficit
    meta["fiscal_A"] = fiscal_A
    if CASE["consumption_proposal"]:
        meta["consumption_proposal"] = consumption_proposal(fin)
    meta["published_totals"] = published_totals(fin)
    print(f"  ✓ {len(ch)} channels closed at low, central and high")
    fvb = frame_vs_base(B, d, I, ch)
    print(f"  ✓ frame against the base's {CASE['case']} quintiles (quintiles_vs_base_{CASE['case']}.csv)")
    print("[sisters] ingesting winners_losers_rows.csv where present")
    ctx["naics"] = naics_crosswalk()
    role_only = role_only_lanes(fin)
    sister_tbl, sister_amounts = ingest_sisters(d, ctx, load_key_map(), commits=CASE["sisters"], role_only=role_only)
    if role_only:
        print(f"  ✓ role table only under this case: {', '.join(role_only)}")
    for cid, arrs in sister_amounts.items():
        ch[cid] = arrs
        totals[cid] = {L: float((pw * arrs[L]).sum() / 1e9) for L in LEVELS}
    print(f"  ✓ {len(sister_tbl)} rows; {int((sister_tbl.status == 'allocated').sum())} allocated; "
          f"{int((sister_tbl.status == 'pending').sum())} lanes pending")
    print("[nets] winners and losers")
    nets, ntot, recipe = build_nets(ch, totals, list(sister_amounts))
    for k, arr in nets.items():
        gate(f"closure_{k[0]}_{k[1]}", np.isclose((pw * arr).sum() / 1e9, ntot[k], rtol=1e-9, atol=1e-9))
    for conv in CONVENTIONS:
        acc = ntot[(f"net_account_{conv}", "central")]
        head = -(fin[CASE["model"]]["ends"]["low"]["cost_bn"] + fin[CASE["model"]]["ends"]["high"]["cost_bn"]) / 2
        gate(f"account_net_plus_future_equals_headline_{conv}", abs(acc - meta["fiscal"]["central"]["future"] - head) < 1e-3,
             persons=acc, future=meta["fiscal"]["central"]["future"], headline=head,
             gap=acc - meta["fiscal"]["central"]["future"] - head)
    # Sensitivities of the social nets at central values, one part swapped: the fiscal cost pooled
    # nationally; housing at ladder 190's national-uniform central; victims' harm on the custody footing.
    for conv in CONVENTIONS:
        k = (f"net_social_{conv}", "central")
        for tag, rep in (("pooled_national_fiscal", {f"fiscal_{conv}": f"fiscal_{conv}_pooled_national"}),
                         ("housing_national_uniform", {"renters": "renters_national_uniform",
                                                       "landlords": "landlords_national_uniform"}),
                         ("crime_custody_footing", {"crime_victims": "crime_victims_custody_footing"})):
            kk = (f"net_social_{conv}_{tag}", "central")
            nets[kk] = nets[k] + sum(ch[new]["central"] - ch[old]["central"] for old, new in rep.items())
            ntot[kk] = ntot[k] + sum(totals[new]["central"] - totals[old]["central"] for old, new in rep.items())
            recipe[kk] = dict(recipe[k], **{old: f"replaced by {new}" for old, new in rep.items()})
            gate(f"closure_{kk[0]}_{kk[1]}", np.isclose((pw * nets[kk]).sum() / 1e9, ntot[kk], rtol=1e-9, atol=1e-9))
    print("[pooled] person nets pooled within SPM units (ruling 6)")
    pool, meta["pooling"] = spm_pooler(d)
    worst, at = 0.0, ""
    for c, arrs in ch.items():
        for L in LEVELS:
            diff = abs(float((pw * pool(arrs[L]))[other].sum() - (pw * arrs[L])[other].sum())) / 1e9
            worst, at = (diff, f"{c}:{L}") if diff > worst else (worst, at)
    gate("spm_pooling_keeps_every_channel_total", worst < 1e-6, channels=len(ch), levels=len(LEVELS),
         worst_bn=worst, at=at)
    pnets = {k: pool(nets[k]) for k in nets if k[0] in MAIN_NETS}
    for k, arr in pnets.items():
        gate(f"closure_pooled_{k[0]}_{k[1]}", np.isclose((pw * arr).sum() / 1e9, ntot[k], rtol=1e-9, atol=1e-9))
    meta["pooling"]["units"] = UNITS
    print(f"  ✓ {len(ch)} channels keep their totals (worst {worst:.1e}bn); {len(pnets)} pooled nets")
    w = pw[other]
    shares = []
    for unit, arrays_ in (("person", nets), ("spm_unit_pooled", pnets)):
        for (name, stack), arr in arrays_.items():
            x = arr[other]
            shares.append(dict(net=name, stack=stack, unit=unit, total_bn=ntot[(name, stack)],
                               winners_share=w[x > 0].sum() / w.sum(), losers_share=w[x < 0].sum() / w.sum(),
                               winners_m=w[x > 0].sum() / 1e6, losers_m=w[x < 0].sum() / 1e6,
                               winners_gain_bn=(w * x)[x > 0].sum() / 1e9, losers_loss_bn=(w * x)[x < 0].sum() / 1e9,
                               median_usd=wquantile(x, w, 0.5), mean_usd=(w * x).sum() / w.sum(),
                               recipe=json.dumps(recipe[(name, stack)])))
    shares = pd.DataFrame(shares)
    moves = pooling_moves(d, nets, pnets)
    # The ruling's plain mean (members' sum over their number, ignoring unequal person weights) as a check:
    # its shares, and how far it moves the totals the weighted mean keeps.
    plain = spm_pooler(d.assign(pw=1.0))[0]
    meta["pooling"]["plain_mean"] = {
        n: dict(winners_share=float(w[plain(nets[(n, "central")])[other] > 0].sum() / w.sum()),
                total_drift_bn=float((w * (plain(nets[(n, "central")]) - nets[(n, "central")])[other]).sum() / 1e9))
        for n in MAIN_NETS}
    print("[cuts]")
    add_cut_columns(d, I["R_spm"])
    arrays = {(n, L): ch[n][L] for n in ch for L in LEVELS}
    tb = {(n, L): totals[n][L] for n in ch for L in LEVELS}
    arrays.update(nets)
    tb.update(ntot)
    arrays.update({(f"{k[0]}_spm_pooled", k[1]): v for k, v in pnets.items()})
    tb.update({(f"{k[0]}_spm_pooled", k[1]): ntot[k] for k in pnets})
    cuts, recon = tabulate_cuts(d, arrays, tb, {k[0] for k in nets} | {f"{k[0]}_spm_pooled" for k in pnets})
    print(f"  ✓ {len(cuts)} cut rows; every cut sums to the frame")
    print("[tree] cuts that separate winners from losers")
    X = d.loc[other, TREE_FEATURES].reset_index(drop=True)
    tree = []
    for key in (("net_social_a", "central"), ("net_social_b", "central"), ("net_account_a", "central"),
                ("net_account_b", "central")):
        net = nets[key][other]
        for leaf in grow_tree(X, (net > 0).astype(float), w, net):
            tree.append(dict(net=key[0], stack=key[1], **leaf))
    tree = pd.DataFrame(tree)
    cells = winner_cells(d, nets)
    print("[group] the group's own frame")
    gf_published = None
    if CASE.get("group_weights") == "row4":
        # The account's count (audit row 4), with the CPS's published weights beside it (group_frame_cps_published.csv).
        w4, g4 = row4_group_weights(B, d)
        gf, ig, ginfo = group_frame(B, d, I, fin, pw=w4)
        gf_published, _, ginfo_published = group_frame(B, d, I, fin)
        meta["group"] = dict(ingroup_victims=ig, weights="row4", row4=g4, **ginfo,
                             cps_published_weights=ginfo_published)
        print(f"  ✓ group frame on row 4: {g4['members_m']:.6f}m members (CPS published {g4['published_members_m']:.6f}m)")
    elif CASE.get("group_weights") == "lineage":
        # The lineage's count: row 4 with the added people at the identified G3+ records (lineage_group_weights), the
        # CPS's published weights beside it as for September 29.
        wl, gl = lineage_group_weights(B, d)
        gf, ig, ginfo = group_frame(B, d, I, fin, pw=wl)
        gf_published, _, ginfo_published = group_frame(B, d, I, fin)
        meta["group"] = dict(ingroup_victims=ig, weights="lineage", lineage=gl, **ginfo,
                             cps_published_weights=ginfo_published)
        print(f"  ✓ group frame on the lineage: {gl['members_m']:.6f}m members (row 4 {gl['row4_members_m']:.6f}m, "
              f"G3+ x {gl['g3plus_factor']:.6f}; CPS published {gl['published_members_m']:.6f}m)")
        if "age_bands" in gl:
            x, y = gl["age_bands"]["added_people"], gl["age_bands"]["added_people_at_one_factor"]
            print(f"  ✓ the added people by age band: {x['under_20_share']:.1%} under 20, earnings {x['earnings_bn']:.1f}bn "
                  f"(one factor {y['factor']:.6f}: {y['under_20_share']:.1%}, {y['earnings_bn']:.1f}bn)")
    else:
        gf, ig, ginfo = group_frame(B, d, I, fin)
        meta["group"] = dict(ingroup_victims=ig, **ginfo)
    fut = {L: meta["fiscal"][L]["future"] for L in LEVELS}
    meta["social_totals"] = dict(
        items_central=float(sum(totals[p]["central"] for p in SOCIAL)),
        least_costly=float(ntot[("net_social_a", "least_costly")] - min(fut.values())),
        most_costly=float(ntot[("net_social_a", "most_costly")] - max(fut.values())))
    reg_tbl = registry(totals, meta, fin, sister_tbl, role_only)
    page = page_table(d, ch, meta, gf, sister_tbl, role_only)
    wide = person_nets_by_cut(cuts)
    fs_rows = [dict(case=k[0], end=k[1], convention=k[2], **v) for k, v in fedsplit.items()]
    if not CASE.get("capped"):
        fs_rows += [dict(case=CASE["model"], end=L, convention="central", cost_bn=meta["fiscal"][L]["cost"],
                         federal_bn=meta["fiscal"][L]["federal"], state_local_bn=meta["fiscal"][L]["state_local"],
                         federal_share=meta["fiscal"][L]["federal"] / meta["fiscal"][L]["cost"],
                         deficit_share=deficit["share"], future_taxpayers_bn=meta["fiscal"][L]["future"],
                         federal_today_bn=meta["fiscal"][L]["federal_today"]) for L in ("central",)]
    else:
        # The band ends' columns: federal_bn, state_local_bn and federal_share are the cash part, the other two
        # financing parts beside them; federal_today_bn adds the resource cost's federal part (never borrowed).
        f = meta["fiscal"]["central"]
        dfed = np.mean([fedsplit[(CASE["model"], end, "central")]["displaced_federal_bn"] for end in ("low", "high")])
        fs_rows += [dict(case=CASE["model"], end="central", convention="central", cost_bn=f["cost"],
                         federal_bn=f["cash_federal"], state_local_bn=f["cash"] - f["cash_federal"],
                         federal_share=f["cash_federal"] / f["cash"], resource_cost_bn=f["resource"],
                         resource_cost_federal_bn=f["resource_federal"], displaced_bn=f["displaced"],
                         displaced_federal_bn=float(dfed), deficit_share=deficit["share"],
                         future_taxpayers_bn=f["future"], federal_today_bn=f["federal_today"],
                         **({"accrual_bn": f["accrual"], "accrual_federal_bn": f["accrual_federal"]}
                            if CASE.get("accrual") else {}))]
    tmpl = []
    for t, desc, basis in KEY_TEMPLATES:
        pop = np.nan
        if "<" not in t:
            k, m, _ = resolve_key(t, d, ctx)
            pop = float((pw * m).sum() / 1e6)
        tmpl.append(dict(template=t, description=desc, cps_basis=basis, population_m=pop))
    tmpl.append(dict(template="@ST", description=TEMPLATE_NOTE, cps_basis="GESTFIPS", population_m=np.nan))
    print("[write]")
    write_csv(reg_tbl, "channels.csv")
    write_csv(page, "winners_losers_table.csv")
    write_csv(wide, "person_nets_by_cut.csv")
    write_csv(cuts, "cuts.csv")
    write_csv(recon, "cut_reconciliation.csv")
    write_csv(shares, "net_shares.csv")
    write_csv(moves, "pooling_moves.csv")
    write_csv(tree, "winners_tree.csv")
    write_csv(cells, "winner_cells.csv")
    write_csv(gf, "group_frame.csv")
    if gf_published is not None:
        write_csv(gf_published, "group_frame_cps_published.csv")
    write_csv(sister_tbl, "role_table.csv")
    write_csv(sister_other_counterfactuals(sister_tbl), "sister_other_counterfactuals.csv")
    write_csv(pd.DataFrame(fs_rows), "fiscal_federal_split.csv")
    for case, r in regs.items():
        write_csv(r, f"regression_{case}.csv")
    write_csv(fvb, f"quintiles_vs_base_{CASE['case']}.csv")
    write_csv(pd.DataFrame(tmpl), "key_templates.csv")
    write_csv(ctx["naics"], "naics_census_industry.csv")
    write_csv(sources_manifest(B, base_sha), "sources_manifest.csv")
    meta["notes"] = notes
    meta["top10_states"] = top10
    meta["federal_split_info"] = fs_info
    if CASE["case"] != "sept24":   # the September 24 files stay byte for byte
        meta["case"] = dict(case=CASE["case"], model=CASE["model"], lane=CASE["lane"], previous=CASE["prev"]["case"],
                            base=CASE["base"], debt=CASE["debt"], debt_files=CASE["debt_files"], generations=CASE["gen"],
                            generations_split=CASE["gen_split"], sisters=CASE["sisters"],
                            published=CASE["published_dir"], role_only=role_only)
        if CASE.get("capped"):
            meta["case"].update(profile=CASE["profile"], previous_variant=CASE["prev_variant"],
                                financing_parts=list(financing_parts(CASE)), capped=True, congestion=CASE["congestion"],
                                preferences=CASE["preferences"])
        if CASE.get("production"):
            meta["case"].update(production=dict(I["production_row4"], weights=CASE["production"]),
                                accrual=bool(CASE.get("accrual")), base_dir=CASE.get("base_dir"),
                                debt_dir=CASE.get("debt_dir"), gen_results=CASE.get("gen_results"),
                                group_weights=CASE.get("group_weights"))
        if DEV["unpinned"]:
            meta["case"]["dev_unpinned"] = DEV["unpinned"]
    (DERIVED / "inputs.json").write_text(json.dumps(meta, indent=1, default=float) + "\n")
    (DERIVED / "gates.json").write_text(json.dumps(GATES, indent=1, default=float) + "\n")
    frame = d.loc[other, ["PH_SEQ", "PPPOS", "SPM_ID", "pw"] + CUT_COLUMNS].reset_index(drop=True)
    cols = {f"{n}|{L}": ch[n][L][other] for n in ch for L in LEVELS}
    cols.update({f"{k[0]}|{k[1]}": v[other] for k, v in nets.items()})
    cols.update({f"{k[0]}_spm_pooled|{k[1]}": v[other] for k, v in pnets.items()})
    frame = pd.concat([frame, pd.DataFrame(cols)], axis=1)
    # One person frame per case outside derived/, so a check run never overwrites the default case's.
    in_place = DERIVED == HERE / "derived"
    frame.to_parquet(CACHE / ("person_frame.parquet" if in_place else f"person_frame_{CASE['case']}.parquet"), index=False)
    print(f"  ✓ {sum(g['passed'] for g in GATES.values())} gates passed; person frame {frame.shape} in _cache/")


if __name__ == "__main__":
    main()
