#!/usr/bin/env python3
"""Inventory of every place in infra/ and research/ that carries the September 23 main case.

Two searches:
  primary  the brief's tokens: 203.2, 249.6, 203.207, 249.64, adopted_2026_09_23,
           main_case_2026_09_23, 227.9, 237.48 (rg --no-ignore, so ignored derived and raw
           files are included);
  derived  numbers computed on the September 23 case that the primary tokens cannot find
           (the real-costs totals, the scale-adoption band, the distribution lane's totals,
           the debt legacy and the uncertainty band), searched in research/ and the two pages.

Each hit gets the brief's class (live_computation, hand_typed, historical_text) or
not_the_case, a finer detail, and the action this lane takes. Coincidental numeric matches in
data files and raw pulls are one row per file with the hit count; case tokens in data files are
one row per file and token, with the count in the note. Three items the brief names
are not reachable by any token (the uncertainty propagation, the lifetime anchors, the
real-costs totals as a computation) and get explicit rows. This lane's own files quote the
tokens by construction and are left out.

Run from the repository root:
  OPENBLAS_NUM_THREADS=1 uv run --no-project python3 \
    infra/immigration-fiscal/sept24_propagation_2026_09_24/inventory.py
"""
from __future__ import annotations

import csv
import json
import re
import subprocess
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
OUT = HERE / "derived" / "inventory.csv"
F = "infra/immigration-fiscal/"

PRIMARY = [r"203\.2", r"249\.6", r"203\.207", r"249\.64", r"adopted_2026_09_23",
           r"main_case_2026_09_23", r"227\.9", r"237\.48"]
# Numbers derived from the September 23 case (en dash as written in the memos).
DERIVED = ["248–307", "256–307", "251–303", "237–289", "212–340", "228–287", "248–300", "203–304",
           "199.1–245.5", "185.2–231.6", "52.5–57.8", "51.9–57.2", "6.3–7.5k", "6.1–7.5k",
           "6.1–7.3k", "6.1–7.4k", "5.8–7.1k", "5.2–8.3k", "262.6", "189.3–235.7",
           "30.5–38.9", "0.94–1.20tn", "745–950", "102–130", "7.7–42.8", "41.1–49.1",
           "141–221", "127–235", "4,969–6,104", "3.31–4.04", "4.04–4.73", "253–304"]
DERIVED_PATHS = ["research/", F + "assumption_explorer_2026_09_21/context.json",
                 F + "figures_2026_09_22/src/", F + "figures_2026_09_22/build_data.cjs"]

# Token forms that are the case itself (anything else in a data file is a coincidence).
CASE_TOKEN = re.compile(r"^(203\.2|203\.21|203\.2069\d*|203\.207\d*|249\.6|249\.639\d*|249\.64\d*|"
                        r"227\.9|227\.92\d*|237\.48\d*)$")
DATA_EXT = {".csv", ".txt", ".npz", ".json", ".html", ".js"}
# Derived outputs of lanes that read the case, where a case token is the case.
CASE_DATA_LANES = ("debt_legacy_2026_09_23", "distribution_weights_2026_09_23", "historical_backcast_2026_09_20",
                   "main_case_2026_09_23", "main_case_2026_09_24", "cps_imputation_keys_2026_09_23",
                   "admin_benefit_keys_2026_09_24", "external_benchmarks_2026_09_24",
                   "outside_checks_combined_2026_09_24", "gg_response_county_iv_2026_09_23", "ltss_share_2026_09_23",
                   "mexborn_count_2026_09_23", "school_cost_where_enrolled_2026_09_24", "figures_2026_09_22",
                   "assumption_explorer_2026_09_21", "uncertainty_propagation_2026_09_22", "winners_losers_2026_09_24")

# ------------------------------------------------------------------ classification table
# (path prefix or exact path, brief_class, detail, action, note); first match wins.
LC, HT, HX, NC = "live_computation", "hand_typed", "historical_text", "not_the_case"
TABLE = [
    # live computations reading the old case, re-run by this lane
    (F + "debt_legacy_2026_09_23/debt_legacy.py", LC, "reads_old_case", "rerun",
     "Reads main_case_2026_09_23 inputs.json and bands and rebuilds the Sept 23 corners; re-run on Sept 24 "
     "with a federal/state split of every correction (--case sept23 keeps the old result)"),
    (F + "debt_legacy_2026_09_23/derived/", LC, "output_of_old_case", "rerun",
     "Outputs of debt_legacy.py; rewritten on the Sept 24 case (Sept 23 values stay as reference columns)"),
    (F + "debt_legacy_2026_09_23/", HX, "lane_text_dated", "none",
     "Lane text dated 2026-09-23; the parent re-dates or supersedes it after the re-run"),
    (F + "distribution_weights_2026_09_23/distribute.py", LC, "reads_old_case", "rerun",
     "fiscal_totals() read main_case_2026_09_23; default --case sept24 now moves A by the Sept 24 change and "
     "rewrites derived/; --case sept23 --out-dir reproduces the committed files (winners_losers loads this "
     "lane from git at 5b8957e, so it is unaffected)"),
    (F + "distribution_weights_2026_09_23/derived/", LC, "output_of_old_case", "rerun",
     "Fiscal cost channel A_mid + F_c: -227.92 on Sept 23, -225.10 on Sept 24; inputs.json keeps the Sept 23 block"),
    (F + "distribution_weights_2026_09_23/", HX, "lane_text_dated", "none", "Lane text dated 2026-09-23"),
    # already moved (out of scope): they read Sept 23 as the 'before' gate
    (F + "main_case_2026_09_24/", LC, "moved_base_gate", "none",
     "The adopted Sept 24 case; reads Sept 23 only as its no-change gate"),
    (F + "figures_2026_09_22/build_data.cjs", LC, "moved_base_gate", "flag",
     "BEFORE gate is correct; line 325 hard-codes the distribution lane's -227.92 (Sept 23), see hand_typed row"),
    (F + "figures_2026_09_22/src/lib/WhoPays.svelte", HT, "stale_on_sept23", "flag",
     "Text 'the lane's central $227.9bn' is the Sept 23 distribution total; the who-pays panel was not moved"),
    (F + "figures_2026_09_22/src/generated/figures.json", LC, "moved_base_gate", "flag",
     "Lines 9-10/164-165 are the staircase's 'before' band (correct); totalBn -227.92 is the Sept 23 distribution"),
    (F + "figures_2026_09_22/dist/", LC, "moved_base_gate", "flag", "Built bundle of the page; follows src"),
    (F + "figures_2026_09_22/", HX, "lane_text_dated", "none", "Brief text"),
    (F + "historical_backcast_2026_09_20/", LC, "moved_base_gate", "none",
     "Back-cast re-run on Sept 24 (da2b107); the _adopted columns stay as the Sept 23 record; the programme "
     "version was never run on Sept 23 or 24 (the debt legacy runs it)"),
    (F + "assumption_explorer_2026_09_21/", LC, "moved_base_gate", "none",
     "Explorer moved (d710a74); Sept 23 appears as the corrections-off gate and in dated cards"),
    # inputs to the Sept 24 package, measured on the Sept 23 frame by design
    (F + "admin_benefit_keys_2026_09_24/translate.js", LC, "frame_input", "keep",
     "Benefit-key lane's translation on the Sept 23 frame; package.cjs gates its figure (+2.268/+2.167)"),
    (F + "cps_imputation_keys_2026_09_23/main_case_translate.js", LC, "frame_input", "keep",
     "Tax-stack translation on the Sept 23 frame; package.cjs gates each stack"),
    (F + "cps_imputation_keys_2026_09_23/combine_onbooks_lane.py", LC, "frame_input", "keep",
     "Builds the stacks package.cjs vendors; reads Sept 23 inputs.json by design"),
    (F + "external_benchmarks_2026_09_24/translate_main_case.js", LC, "frame_input", "keep",
     "CBO/Treasury translation on the Sept 23 frame; package.cjs gates it"),
    (F + "ltss_share_2026_09_23/main_case_effect.js", LC, "frame_input", "keep",
     "LTSS translation on the Sept 23 frame; package.cjs reads its outputs"),
    (F + "ltss_share_2026_09_23/gate.py", LC, "frame_input", "keep", "Gate of the LTSS lane on the Sept 23 frame"),
    (F + "mexborn_count_2026_09_23/price_row4.py", LC, "frame_input", "keep",
     "Prices audit row 4 on the Sept 23 band; enters the package through the stacks"),
    (F + "outside_checks_combined_2026_09_24/combine.cjs", LC, "frame_input", "keep",
     "Builds the Sept 23 frame package.cjs reuses"),
    (F + "gg_response_county_iv_2026_09_23/main_case_map.js", LC, "frame_input", "keep",
     "Checks the Sept 23 case's general-government input; hard-codes 203.207/249.640 as its own gate"),
    (F + "school_cost_where_enrolled_2026_09_24/test_lane.py", HT, "frame_input", "keep",
     "Test asserts the Sept 23 base [203.207, 249.64]; the lane's figure is measured on that frame"),
    (F + "dataset_integrity_2026_09_23/synthesis.py", HT, "frame_input", "keep",
     "MAIN_CASE = {shared: 203.2, personal: 249.6} typed in: the audit's synthesis on the Sept 23 case, a "
     "pre-adoption record"),
    (F + "cps_imputation_keys_2026_09_23/distribution_check.py", HX, "docstring_dated", "flag",
     "Docstring cites the distribution lane's -227.9. It reads the lane's committed channel_by_quintile.csv "
     "and adds the fill-in correction; on the Sept 24 file (which already contains it) a re-run would count "
     "it twice, so a re-run should read the Sept 23 file from git"),
    (F + "winners_losers_2026_09_24/", LC, "sister_lane_reads_both_cases", "flag",
     "Sister ledger lane. Its federal_split() positive control reads debt_legacy federal_split_2024.csv as the "
     "Sept 23 split, which this lane moved to Sept 24; reported to the parent"),
    (F + "uncertainty_propagation_2026_09_22/derived/sept24/", LC, "output_of_new_case", "none",
     "propagate.py --case sept24 outputs: the Sept 23 and Sept 24 adopted cases side by side"),
    (F + "cps_imputation_keys_2026_09_23/derived/", LC, "frame_input", "keep", "Frame-dated translation outputs"),
    (F + "admin_benefit_keys_2026_09_24/derived/", LC, "frame_input", "keep", "Frame-dated translation outputs"),
    (F + "external_benchmarks_2026_09_24/derived/", LC, "frame_input", "keep", "Frame-dated translation outputs"),
    (F + "outside_checks_combined_2026_09_24/derived/", LC, "frame_input", "keep", "Frame-dated outputs"),
    (F + "gg_response_county_iv_2026_09_23/derived/", LC, "frame_input", "keep", "Frame-dated gate outputs"),
    (F + "ltss_share_2026_09_23/derived/", LC, "frame_input", "keep", "Frame-dated outputs"),
    (F + "mexborn_count_2026_09_23/derived/", LC, "frame_input", "keep", "Frame-dated pricing"),
    (F + "school_cost_where_enrolled_2026_09_24/derived/", LC, "frame_input", "keep", "Frame-dated engine base"),
    (F + "main_case_2026_09_23/", LC, "source_of_old_case", "none",
     "The September 23 case itself; the record the Sept 24 case gates against"),
    # research memos: dated by default; stale lines are overridden below
    ("research/", HX, "memo_dated", "none", "Dated as September 23 in the text or a revision note"),
    # every other lane text (BRIEF, RESULT, README, notes) is dated by its lane
    (F, HX, "lane_text_dated", "none", "Lane dated 2026-09-23 or the morning of 2026-09-24; quotes the case then adopted"),
]
# Research lines that quote the Sept 23 case as current or with a stale status (parent edits).
STALE_LINES = {
    ("research/immigration-status-benefits-sweep-2026-09-24.md", 82):
        "Shelter correction 'proposed, not adopted' on the $203.2-249.6bn case; adopted 2026-09-24 (decision 5)",
    ("research/immigration-outside-checks-2026-09-24.md", 54):
        "'Adopted main case 203.21-249.64' without a date; the Sept 24 case was adopted later that day",
    ("research/immigration-outside-checks-2026-09-24.md", 137): "Same undated 'Adopted main case' label",
    ("research/immigration-outside-checks-2026-09-24.md", 190): "Route A row quotes 203.2-249.6 as the main case",
}


def classify(path: str) -> tuple[str, str, str, str]:
    for prefix, cls, detail, action, note in TABLE:
        if path == prefix or path.startswith(prefix):
            return cls, detail, action, note
    return NC, "unmatched", "none", ""


def rg_json(patterns, paths, fixed=False):
    args = ["rg", "--no-ignore", "--json", "-M", "4000"] + (["-F"] if fixed else [])
    for p in patterns:
        args += ["-e", p]
    out = subprocess.run(args + paths, cwd=ROOT, capture_output=True, text=True)
    if out.returncode not in (0, 1):
        raise SystemExit(f"[BLOCKED] rg failed: {out.stderr[:300]}")
    hits = []
    for line in out.stdout.splitlines():
        o = json.loads(line)
        if o["type"] != "match":
            continue
        d = o["data"]
        text = (d["lines"].get("text") or "").encode("utf-8")
        for sm in d["submatches"]:
            s, e = sm["start"], sm["end"]
            left, right = s, e
            while left > 0 and chr(text[left - 1]) in "0123456789.":
                left -= 1
            while right < len(text) and chr(text[right]) in "0123456789":
                right += 1
            hits.append(dict(path=d["path"]["text"], line=d["line_number"],
                             match=text[s:e].decode("utf-8", "replace"),
                             token=text[left:right].decode("utf-8", "replace").lstrip(".")))
    return hits


def main() -> None:
    rows = []
    primary = rg_json(PRIMARY, ["infra/", "research/"])
    aggregated = defaultdict(Counter)
    per_file = {}
    primary = [h for h in primary if not h["path"].startswith(F + "sept24_propagation_2026_09_24/")]
    for h in primary:
        p = h["path"]
        named = h["match"] in ("adopted_2026_09_23", "main_case_2026_09_23")
        is_case_token = bool(CASE_TOKEN.match(h["token"]))
        ext = Path(p).suffix
        raw = "/_cache/" in p or "/raw/" in p
        in_case_lane = any(f"{F}{lane}/" in p for lane in CASE_DATA_LANES)
        if raw or not (named or is_case_token) or (ext in DATA_EXT and not named and not in_case_lane):
            aggregated[p][h["token"]] += 1
            continue
        cls, detail, action, note = classify(p)
        if (p, h["line"]) in STALE_LINES:
            cls, detail, action, note = HX, "undated_or_stale", "parent_edits", STALE_LINES[(p, h["line"])]
        token = h["match"] if named else h["token"]
        if ext in DATA_EXT:          # data files: one row per file and token, first line shown
            if (p, token) not in per_file:
                per_file[(p, token)] = dict(search="primary", path=p, line=h["line"], token=token,
                                            brief_class=cls, detail=detail, action=action, note=note, n=0)
            per_file[(p, token)]["n"] += 1
            continue
        rows.append(dict(search="primary", path=p, line=h["line"], token=token,
                         brief_class=cls, detail=detail, action=action, note=note))
    for r in per_file.values():
        n = r.pop("n")
        if n > 1:
            r["note"] = f"{r['note']} ({n} hits in this file; first line shown)".lstrip()
        rows.append(r)
    for p, tokens in sorted(aggregated.items()):
        kind = "raw pull (_cache or raw)" if ("/_cache/" in p or "/raw/" in p) else "numeric coincidence"
        rows.append(dict(search="primary", path=p, line="", token=";".join(sorted(tokens)),
                         brief_class=NC, detail="coincidental", action="none",
                         note=f"{sum(tokens.values())} hits; {kind}, not the case"))

    for h in rg_json(DERIVED, DERIVED_PATHS, fixed=True):
        p = h["path"]
        cls, detail, action, note = classify(p)
        rows.append(dict(search="derived", path=p, line=h["line"], token=h["match"], brief_class=HT if p.endswith(
            (".json", ".cjs", ".svelte")) else HX, detail="derived_from_sept23", action="report_old_new",
            note="Number computed on the Sept 23 (or Sept 20) case; new value in RESULT.md"))

    explicit = [
        dict(search="explicit", path=F + "uncertainty_propagation_2026_09_22/propagate.py", line="",
             token="165.1-197.4", brief_class=LC, detail="reads_sept20_case", action="rerun",
             note="Ladder 184 propagates the Sept 20 cases (service_response_cases.csv); no Sept 23 token. "
                  "--case sept24 carries the same error sources through the adopted case"),
        dict(search="explicit", path=F + "uncertainty_propagation_2026_09_22/audit.py", line="",
             token="165.1-197.4", brief_class=LC, detail="reads_sept20_case", action="none",
             note="Formula audit and arms-vs-sampling on the Sept 20 grid; the Sept 24 intervals come from propagate.py"),
        dict(search="explicit", path=F + "ledger_absolute_2026_09_17/lifetime.py", line="",
             token="lifetime anchors", brief_class=LC, detail="behind_fingerprint_guard", action="report_only",
             note="The lifetime anchors (period-profile NPVs: -$280k/-$225k/-$96k) come from the Sept 19 generation "
                  "ledger, a different object that never reads any main case; nothing to switch. Fingerprinted: not run"),
        dict(search="explicit", path="research/immigration-real-fiscal-and-social-costs-2026-09-23.md", line="",
             token="§7, §7b totals", brief_class=HX, detail="hand_sums_on_sept23", action="rerun",
             note="Totals are hand sums on the Sept 23 case; real_costs_totals.py recomputes them from lane files"),
    ]
    rows.extend(explicit)
    OUT.parent.mkdir(exist_ok=True)
    fields = ["search", "path", "line", "token", "brief_class", "detail", "action", "note"]
    rows.sort(key=lambda r: (r["search"], r["brief_class"], r["path"], str(r["line"]).zfill(6)))
    with OUT.open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=fields, lineterminator="\n")
        w.writeheader()
        w.writerows(rows)
    by = Counter((r["search"], r["brief_class"], r["detail"]) for r in rows)
    for k, v in sorted(by.items()):
        print(f"{v:5d}  {' / '.join(k)}")
    print(f"primary hits {len(primary)}, rows {len(rows)}, files {len({r['path'] for r in rows})}")


if __name__ == "__main__":
    main()
