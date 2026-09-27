"""The return on public capital across the account's services (lane of 2026-09-27).

The main case (main_case_schools_full_2026_09_26) charges government services at BEA consumption,
which includes depreciation but "assumes a zero net return" on public capital (NIPA Table 3.10.5,
note 2). The school-capital lane priced that return for K-12 alone. This script prices it for every
tax-financed service the main case lets respond, at the case's own allocation keys and responses,
specification by specification, and adds it to the case's cost at the same specification.

    OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/capital_return_services_2026_09_27/capital_return.py

Inputs, all read-only:
- the school lane's cached primary files (BEA Fixed Assets Section 7, Census VIP, F-33, NCES, OMB,
  Treasury), hash-checked by that lane's own registry, and its script, imported and rerun into a
  scratch directory so that K-12 is reproduced from the primary files rather than copied;
- the pinned NIPA Section 3 workbook (Tables 3.10.5, 3.15.5, 3.16, 3.17);
- `spec_lines.cjs`, which calls the adopted package's cost() for the 64 specifications and both
  fill-in methods and returns each line's key and response from that evaluation;
- Census's construction definitions (`_cache/census_c30_definitions.html`), for where courthouses sit.

Writes derived/ only when every gate passes; otherwise prints `[BLOCKED] ...` and exits 1.
"""
from __future__ import annotations

import contextlib
import csv
import hashlib
import html
import importlib.util
import io
import json
import re
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path

sys.dont_write_bytecode = True  # importing the school lane must not write __pycache__ into its directory

import openpyxl  # noqa: E402

LANE = Path(__file__).resolve().parent
ROOT = LANE.parents[2]
FISCAL = ROOT / "infra" / "immigration-fiscal"
DERIVED = LANE / "derived"
CACHE = LANE / "_cache"
SCHOOL = FISCAL / "school_capital_return_2026_09_26"
MAIN = FISCAL / "main_case_schools_full_2026_09_26"
MODEL = FISCAL / "assumption_explorer_2026_09_21" / "derived" / "model.json"
R_VALUES = FISCAL / "finite_response_2026_09_26" / "derived" / "r_values.json"
DEBT_RESULT = FISCAL / "debt_legacy_2026_09_23" / "RESULT.md"
MATCHED = ROOT / "research" / "immigration-matched-benefits-2026-09-19.md"
DECISION = ROOT / "decisions" / "2026-09-26-main-case-schools-full-cost.md"
DEFINITIONS = CACHE / "census_c30_definitions.html"
HELPER = LANE / "spec_lines.cjs"

YEAR = 2024
RATES = {"2pct": 0.02, "3pct": 0.03}      # A-4 (2023) and A-4 (2003): the band's low and high rates
REPORTED = {"7pct": 0.07}                 # A-4 (2003)'s private-capital rate, reported only
CASE_ENDS = (48, 11)                      # the brief's end specifications of the adopted case
EQUIP_YEARS = (2019, 2024)                # the school lane's K-12 equipment key uses FY2019 and FY2024
MAP_TOL = 0.05                            # function investment residuals vs equipment + software

GATES: list[tuple[str, bool, str]] = []


def gate(name: str, ok: bool, detail: str) -> None:
    GATES.append((name, bool(ok), detail))


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rows_out(rows: list[list]) -> list[list]:
    return [[round(x, 6) if isinstance(x, float) else x for x in r] for r in rows]


# ---------------------------------------------------------------- the school lane, reused read-only
def load_school_lane():
    spec = importlib.util.spec_from_file_location("school_capital_return", SCHOOL / "capital_return.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def rerun_school_lane(SL) -> tuple[dict, list[dict], dict]:
    """Run the school lane's main() on its cached primary files, writing into a scratch directory."""
    committed = SL.DERIVED
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        shutil.copy(committed / "sources.csv", tmp / "sources.csv")
        SL.DERIVED = tmp
        try:
            with contextlib.redirect_stdout(io.StringIO()):
                rc = SL.main()
        except SystemExit as e:
            raise SystemExit(f"[BLOCKED] the school lane's rerun stopped: {e}")
        finally:
            SL.DERIVED = committed
        if rc != 0:
            raise SystemExit("[BLOCKED] the school lane's own gates fail on its cached files")
        summary = json.loads((tmp / "summary.json").read_text())
        key_rows = list(csv.DictReader((tmp / "k12_share_key.csv").open()))
        identical = {f.name: f.read_bytes() == (committed / f.name).read_bytes()
                     for f in sorted(tmp.iterdir()) if f.name != "sources.csv"}
    return summary, key_rows, identical


def vip_paths(SL) -> dict:
    """Census VIP state and local construction, $mn, keyed by the row's path ("Educational/Higher education/Dormitory")."""
    out: dict = {}

    def parse(rows):
        hdr = [r for r in rows if r and r[0] and str(r[0]).strip().startswith("Type of")][0]
        years = [int(float(x)) for x in hdr[1:] if x not in (None, "")]
        stack: list[tuple[int, str]] = []
        for r in rows:
            if not r or not r[0]:
                continue
            raw = str(r[0]).replace("\xa0", " ").rstrip()
            vals = list(r[1:1 + len(years)])
            nums = {}
            for y, v in zip(years, vals):
                try:
                    nums[y] = float(v)
                except (TypeError, ValueError):
                    pass
            if not nums:
                continue
            ind = len(raw) - len(raw.lstrip(" "))
            while stack and stack[-1][0] >= ind:
                stack.pop()
            stack.append((ind, raw.strip()))
            path = "/".join(n for _, n in stack[1:])           # drop "Total State and Local Construction"
            out.setdefault(path, {}).update(nums)

    for f in ("c30_stateha__Annual.csv", "c30_stateha1__Annual.csv"):
        rows = list(csv.reader((SL.CACHE / f).open()))
        if rows[0][0].split("=")[1].split(",")[0] != sha(SL.CACHE / f.replace("__Annual.csv", ".xls")):
            raise SystemExit(f"[BLOCKED] {f} is stale against its .xls")
        parse([tuple(r) for r in rows[1:]])
    for f in ("c30_stateha2.xlsx", "c30_state.xlsx"):
        parse(list(openpyxl.load_workbook(SL.CACHE / f, read_only=True, data_only=True).worksheets[0].iter_rows(values_only=True)))
    return out


def definitions_text() -> str:
    t = DEFINITIONS.read_text(encoding="utf-8")
    t = re.sub(r"(?s)<script.*?</script>|<style.*?</style>", " ", t)
    t = html.unescape(re.sub(r"<[^>]+>", "\n", t))
    return " ".join(l.strip() for l in t.split("\n") if l.strip())


# ---------------------------------------------------------------- main
def main() -> int:
    t0 = time.time()
    if not DEFINITIONS.exists():
        raise SystemExit(f"[BLOCKED] missing {DEFINITIONS.relative_to(ROOT)}: fetch https://www.census.gov/construction/c30/definitions.html")
    SL = load_school_lane()
    SL.check_cache()                       # every cached primary file against the school lane's registry
    school, key_rows, identical = rerun_school_lane(SL)
    school_committed = json.loads((SCHOOL / "derived" / "summary.json").read_text())

    # ---------------- 0. the case, specification by specification
    run = subprocess.run(["node", str(HELPER)], capture_output=True, text=True, cwd=ROOT)
    if run.returncode != 0:
        raise SystemExit(f"[BLOCKED] spec_lines.cjs failed: {run.stderr.strip()[-400:]}")
    case = json.loads(run.stdout)
    specs, methods = case["specs"], case["methods"]
    n = len(specs)
    per = case["per_method"]
    costs = {m: [r["cost_bn"] for r in per[m]] for m in methods}
    bands_csv = list(csv.DictReader((MAIN / "derived" / "main_case_bands.csv").open()))
    adopted_row = [r for r in bands_csv if r["profile"] == case["profile"] and r["variant"] == "adopted"][0]
    main_summary = json.loads((MAIN / "derived" / "summary.json").read_text())
    corrections = json.loads((MAIN / "derived" / "corrections.json").read_text())
    meta = corrections["meta"]["responses"]
    rv = json.loads(R_VALUES.read_text())

    def band_of(values_by_method: dict) -> dict:
        """Band ends as central() takes them: each method's min and max over specifications, averaged."""
        los = [min(values_by_method[m]) for m in methods]
        his = [max(values_by_method[m]) for m in methods]
        return {"low": sum(los) / len(los), "high": sum(his) / len(his),
                "low_spec": [values_by_method[m].index(min(values_by_method[m])) for m in methods],
                "high_spec": [values_by_method[m].index(max(values_by_method[m])) for m in methods]}

    case_band = band_of(costs)
    gate("per_spec_costs_reproduce_the_case", abs(case_band["low"] - case["central"][0]) < 1e-9
         and abs(case_band["high"] - case["central"][1]) < 1e-9
         and abs(case_band["low"] - float(adopted_row["cost_low_bn"])) < 1e-4
         and abs(case_band["high"] - float(adopted_row["cost_high_bn"])) < 1e-4
         and abs(case_band["low"] - main_summary["main_case"][0]) < 1e-9 and abs(case_band["high"] - main_summary["main_case"][1]) < 1e-9,
         f"package cost() per spec: {case_band['low']:.4f}/{case_band['high']:.4f}; main_case_bands.csv "
         f"{adopted_row['cost_low_bn']}/{adopted_row['cost_high_bn']}")
    gate("case_end_specifications_are_48_and_11", all(i == CASE_ENDS[0] for i in case_band["low_spec"])
         and all(i == CASE_ENDS[1] for i in case_band["high_spec"]),
         f"low {case_band['low_spec']}, high {case_band['high_spec']} (per method)")
    mean_cost = [sum(costs[m][i] for m in methods) / len(methods) for i in range(n)]
    gate("published_corrections_json_gives_the_same_per_spec_costs",
         max(abs(a - b) for a, b in zip(mean_cost, case["payload_costs"])) < 1e-9,
         f"max |payload - mean of methods| = {max(abs(a - b) for a, b in zip(mean_cost, case['payload_costs'])):.2e} over {n} specs")
    gate("responses_equal_meta_responses",
         case["responses"]["general_government"] == meta["general_government"]
         and case["payload_meta_responses"] == meta
         and all(s["gg"] in (meta["general_government"]["low"], meta["general_government"]["high"]) for s in specs)
         and all(s["school"] in (meta["school"]["growth"], meta["school"]["decline"]) for s in specs)
         and meta["school"]["growth"] == 1 and meta["school"]["decline"] == 1,
         f"general government {meta['general_government']['low']:.4f}/{meta['general_government']['high']:.4f}; "
         f"school {meta['school']['growth']}/{meta['school']['decline']}")

    # ---------------- 1. keys and responses by line, read from the engine's own evaluation
    s_pupil = school["pupil_share_s"]
    gate("pupil_share_is_the_finite_response_lanes", s_pupil == rv["s_pupil"] == SL.BRIEF_S, f"s = {s_pupil!r}")
    other_resp = case["profile_def"]["other"]
    view_err: list[str] = []

    def view(m: str, i: int) -> dict:
        L, sp = per[m][i]["lines"], specs[i]
        share = sp["share"]
        edu, col, sch = L["education_services"], L["college_rekey"], L["school_reprice"]
        school_r, college_r = sch["response"] / share, col["response"] / (1 - share)
        if abs(school_r - sp["school"]) > 1e-12 or abs(college_r - other_resp) > 1e-12 \
                or abs(edu["response"] - (share * school_r + (1 - share) * college_r)) > 1e-12:
            view_err.append(f"education responses at {m}/{i}")
        for lid, key in (("public_order_safety", sp["justice"]), ("health_services", "health_other"),
                         ("general_public_services", "population"), ("education_services", "education_mix"),
                         ("income_security_services", "cash_assistance"), ("housing_community_services", "population")):
            if L[lid]["key"] != key:
                view_err.append(f"{lid} keyed {L[lid]['key']} at {m}/{i}")
        k = lambda lid: L[lid]["amount_bn"] / L[lid]["national_bn"]
        return {
            "k12": (s_pupil, school_r),
            "college": ((edu["amount_bn"] + col["amount_bn"]) / edu["national_bn"], college_r),
            "k12_account_key": ((edu["amount_bn"] + sch["amount_bn"]) / edu["national_bn"], school_r),
            "public_order_safety": (k("public_order_safety"), L["public_order_safety"]["response"]),
            "health_services": (k("health_services"), L["health_services"]["response"]),
            "general_public_services": (k("general_public_services"), L["general_public_services"]["response"]),
            "income_security_services": (k("income_security_services"), L["income_security_services"]["response"]),
            "housing_community_services": (k("housing_community_services"), L["housing_community_services"]["response"]),
            # held fixed in the main case: their keys at a response of 1, for conversions only
            "economic_affairs_per_unit_response": (k("economic_affairs_services"), 1.0),
            "recreation_per_unit_response": (k("recreation_culture"), 1.0),
        }

    V = {m: [view(m, i) for i in range(n)] for m in methods}
    gate("line_keys_and_responses_are_the_main_cases", not view_err and all(
        V[m][i]["public_order_safety"][1] == 1 and V[m][i]["health_services"][1] == 1
        and V[m][i]["income_security_services"][1] == 1 and V[m][i]["housing_community_services"][1] == 1
        and V[m][i]["general_public_services"][1] == specs[i]["gg"] for m in methods for i in range(n)),
         "; ".join(view_err[:3]) or "justice keyed by use, health by health_other, general government by population at its "
         "specification's response, schools and colleges at 1, from the evaluation cost() makes")
    fixed_zero = ("defense", "domestic_interest", "economic_affairs_services", "recreation_culture", "agricultural_subsidies",
                  "housing_subsidies", "transport_subsidies", "other_subsidies")
    gate("response_zero_and_fixed_lines_stay_at_zero", all(per[m][i]["lines"][lid]["response"] == 0
                                                            for m in methods for i in range(n) for lid in fixed_zero),
         ", ".join(fixed_zero) + ": response 0 at every specification")

    # ---------------- 2. BEA tables
    fa = SL.CACHE / "fa_Section7All_xls.xlsx"
    K, klab, _ = SL.bea_table(fa, "FAAt701-A")     # current-cost net stock, yearend
    D, dlab, _ = SL.bea_table(fa, "FAAt703-A")     # current-cost depreciation
    INV, ilab, _ = SL.bea_table(fa, "FAAt705-A")   # investment
    FA_LINES = {1: "Government fixed assets", 22: "National defense", 38: "Nondefense", 39: "Equipment", 40: "Structures", 41: "Office", 42: "Commercial", 43: "Health care",
                44: "Educational", 45: "Public safety", 46: "Amusement and recreation", 47: "Transportation", 48: "Power",
                49: "Highways and streets", 50: "Conservation and development", 51: "Other structures",
                52: "Intellectual", 53: "Software", 54: "Research", 55: "State and local", 56: "Equipment",
                57: "Structures", 58: "Residential", 59: "Office", 60: "Commercial", 61: "Health care", 62: "Educational",
                63: "Public safety", 64: "Amusement and recreation", 65: "Transportation", 66: "Power",
                67: "Highways and streets", 68: "Sewer systems", 69: "Water systems", 70: "Conservation and development",
                71: "Other structures", 72: "Intellectual", 73: "Software", 74: "Research"}
    for tab, lab in (("FAAt701", klab), ("FAAt703", dlab), ("FAAt705", ilab)):
        for line, text in FA_LINES.items():
            SL.label_is(lab, line, text, tab)
    t3105, l3105, _ = SL.bea_table(SL.NIPA3, "T31005-A")
    t3155, l3155, _ = SL.bea_table(SL.NIPA3, "T31505-A")
    t316, l316, _ = SL.bea_table(SL.NIPA3, "T31600-A")
    t317, l317, _ = SL.bea_table(SL.NIPA3, "T31700-A")
    for tab, lab, checks in (
            ("T31005", l3105, ((46, "Less: Sales to other sectors"), (57, "Less: Sales to other sectors"),
                               (58, "Tuition and related educational charges"), (59, "Health and hospital charges"),
                               (60, "Other sales"))),
            ("T31505", l3155, ((82, "Other"), (100, "Housing and community services"), (103, "Sanitation"),
                               (109, "Education"), (110, "Elementary and secondary"), (111, "Higher"),
                               (112, "Libraries and other"), (114, "Other"))),
            ("T31600", l316, ((85, "Other"), (101, "Housing and community services"), (106, "Education"),
                              (107, "Elementary and secondary"), (108, "Higher"), (109, "Libraries and other"),
                              (111, "Other"))),
            ("T31700", l317, ((2, "General public service"), (4, "Public order and safety"), (7, "Health"), (9, "Education"),
                              (17, "Health"), (22, "General public service"), (25, "Housing and community services"),
                              (26, "Health (net)"), (27, "Gross expenditures"), (28, "Less: Sales to other sectors"),
                              (30, "Education"), (55, "Education"), (115, "Federal"), (116, "General public service"),
                              (117, "National defense"), (118, "Public order and safety"), (119, "Economic affairs"),
                              (120, "Housing and community services"), (121, "Health"), (122, "Recreation and culture"),
                              (123, "Education"), (124, "Income security"), (125, "State and local"),
                              (126, "General public service"), (127, "Public order and safety"), (128, "Economic affairs"),
                              (129, "Housing and community services"), (130, "Health"), (131, "Recreation and culture"),
                              (132, "Education"), (133, "Income security")))):
        for line, text in checks:
            SL.label_is(lab, line, text, tab)
    notes316 = SL._footnotes(SL.NIPA3, "T31600-A")
    notes3155 = SL._footnotes(SL.NIPA3, "T31505-A")
    bn = lambda v: v / 1000.0
    avg = lambda line: (bn(K[line][YEAR - 1]) + bn(K[line][YEAR])) / 2
    lines_by_id = {l["id"]: l for l in case["inventory"]}
    gate("account_lines_are_nipa_3_17", all(abs(lines_by_id[lid]["national_bn"] - bn(t317[ln][YEAR])) < 1e-6 for lid, ln in
                                           (("general_public_services", 2), ("public_order_safety", 4),
                                            ("health_services", 7), ("education_services", 9))),
         "general government, public order and safety, health and education equal NIPA 3.17 lines 2, 4, 7 and 9 (2024)")
    gate("fa_structure_types_add_to_structures",
         abs(sum(K[l][YEAR] for l in range(58, 72)) - K[57][YEAR]) < 0.001 * K[57][YEAR]
         and abs(sum(K[l][YEAR] for l in range(41, 52)) - K[40][YEAR]) < 0.001 * K[40][YEAR],
         f"S&L types {bn(sum(K[l][YEAR] for l in range(58, 72))):.1f} vs {bn(K[57][YEAR]):.1f}; federal nondefense "
         f"{bn(sum(K[l][YEAR] for l in range(41, 52))):.1f} vs {bn(K[40][YEAR]):.1f}")

    # ---------------- 3. BEA's own type-to-function mapping (NIPA 3.17 gross investment by function)
    SL_MAP = {"general_public_services": (126, [59]), "public_order_safety": (127, [63]),
              "economic_affairs": (128, [65, 66, 67, 70]), "housing_community": (129, [58, 68, 69]),
              "health": (130, [61]), "recreation_culture": (131, [64]), "education": (132, [62, 74]),
              "income_security": (133, [])}
    FED_MAP = {"general_public_services": (116, [41]), "public_order_safety": (118, [45]),
               "economic_affairs": (119, [47, 48, 49, 50]), "housing_community": (120, []), "health": (121, [43]),
               "recreation_culture": (122, [46]), "education": (123, [44]), "income_security": (124, [])}
    map_rows, resid = [], {}
    for y in EQUIP_YEARS:
        for level, mp, total_gi, types, eqsw in (
                ("state_local", SL_MAP, t317[125][y], list(range(58, 72)) + [74], INV[56][y] + INV[73][y]),
                ("federal_nondefense", FED_MAP, t317[115][y] - t317[117][y], list(range(41, 52)), INV[39][y] + INV[53][y])):
            for f, (gl, tl) in mp.items():
                r = (t317[gl][y] - sum(INV[t][y] for t in tl)) / 1000
                resid[(level, f, y)] = r
                map_rows.append([y, level, f, gl, "+".join(str(t) for t in tl) or "none", bn(t317[gl][y]),
                                 bn(sum(INV[t][y] for t in tl)), r, r / bn(eqsw), ""])
            # the residual of all functions should be the assets no structure type covers
            other_types = bn(total_gi - sum(INV[t][y] for t in types))
            rest = bn(eqsw) + (0.0 if level == "state_local" else bn(INV[54][y]))
            map_rows.append([y, level, "all functions less all structure types" + (" and R&D" if level == "state_local" else ""),
                             "", "", bn(total_gi), bn(sum(INV[t][y] for t in types)), other_types, "",
                             other_types / rest])
            resid[(level, "total", y)] = other_types
            resid[(level, "eqsw", y)] = bn(eqsw)
    gate("bea_type_mapping_leaves_no_negative_residual", all(v >= 0 for (lv, f, y), v in resid.items() if f not in ("total", "eqsw")),
         "every function's gross investment (NIPA 3.17) covers the structure types mapped to it, 2019 and 2024")
    sl_fit = [resid[("state_local", "total", y)] / resid[("state_local", "eqsw", y)] for y in EQUIP_YEARS]
    fed_rd = {y: bn(INV[54][y]) for y in EQUIP_YEARS}
    fed_fit = [resid[("federal_nondefense", "total", y)] / (resid[("federal_nondefense", "eqsw", y)] + fed_rd[y]) for y in EQUIP_YEARS]
    gate("bea_type_mapping_residuals_are_equipment_and_ip", all(abs(x - 1) < MAP_TOL for x in sl_fit + fed_fit),
         f"S&L residual / (equipment + software) {sl_fit[0]:.3f} (2019), {sl_fit[1]:.3f} (2024); federal nondefense residual / "
         f"(equipment + software + R&D) {fed_fit[0]:.3f}, {fed_fit[1]:.3f}")
    unalloc = {y: bn(t3155[82][y] - t316[85][y]) for y in range(2005, YEAR + 1)}
    unalloc_ratio = {y: unalloc[y] / bn(INV[59][y]) for y in unalloc}
    gate("nipa_files_sl_office_investment_under_general_government",
         any("unallocable" in x for x in notes3155) and 0.8 <= min(unalloc_ratio.values()) and max(unalloc_ratio.values()) <= 1.0,
         f"S&L unallocable general-government investment / S&L Office investment {min(unalloc_ratio.values()):.3f}-"
         f"{max(unalloc_ratio.values()):.3f}, 2005-2024 (2024: {unalloc_ratio[YEAR]:.3f})")
    defs = definitions_text()
    court = "State and local and federal also includes city halls, borough halls, municipal buildings, courthouses, and state capitol buildings"
    gate("census_definitions_put_courthouses_in_office", court in defs, "Census C30 definitions, Office: General")
    note8 = [x for x in notes316 if x.startswith("8.")]
    gate("sl_housing_consumption_is_sanitation_only", bool(note8) and "Consists of current expenditures for sanitation" in note8[0]
         and abs(t316[101][YEAR] - t317[25][YEAR]) < 1, f"NIPA 3.16 note 8: {note8[0][:60] if note8 else 'missing'}")

    # ---------------- 4. fee factors
    f_health = t317[26][YEAR] / t317[27][YEAR]
    ce_higher = bn(t316[108][YEAR])
    tuition = bn(t3105[58][YEAR])
    f_tuition = ce_higher / (ce_higher + tuition)
    # 3.16 current expenditures add education's social benefits (NIPA 3.17 l55) to consumption. At least
    # 3.16 "Other" less 3.15.5 "Other" (consumption plus investment) of them sit in "Other", so at most the
    # rest could sit in "Higher".
    benefits_elsewhere_max = bn(t317[55][YEAR] - (t316[111][YEAR] - t3155[114][YEAR]))
    f_tuition_low = (ce_higher - benefits_elsewhere_max) / (ce_higher - benefits_elsewhere_max + tuition)
    gate("higher_education_consumption_read_from_3_16", 0 <= benefits_elsewhere_max < 1.0 and f_tuition - f_tuition_low < 0.001
         and abs(t316[107][YEAR] + t316[108][YEAR] + t316[109][YEAR] - t316[106][YEAR]) < 1,
         f"benefits that could sit in 'Higher' <= {benefits_elsewhere_max:.3f}bn; tuition factor {f_tuition:.4f} (>= {f_tuition_low:.4f})")
    fed_sales_share_max = t3105[46][YEAR] / (t317[17][YEAR] + t3105[46][YEAR])
    gate("health_fee_factor_matches_the_school_lane_note", abs(bn(t317[27][YEAR]) - 491.383) < 0.001 and abs(bn(t317[26][YEAR]) - 126.839) < 0.001,
         f"S&L health net/gross {bn(t317[26][YEAR]):.3f}/{bn(t317[27][YEAR]):.3f} = {f_health:.4f}")

    # ---------------- 5. capital by component
    k12_key = school["k12_structures_key"]["central"]
    k12 = school["national_k12_capital_bn"]["central"]
    edu_avg = avg(62)
    gate("k12_structures_are_the_key_times_educational_structures",
         abs(k12["structures_avg2024"] - k12_key * edu_avg) < 1e-9, f"{k12['structures_avg2024']:.3f} = {k12_key:.4f} x {edu_avg:.3f}")
    # The non-K-12 part by vintage composition (post-1993 VIP, weighted by the school lane's perpetual inventory).
    vip = vip_paths(SL)
    P = {"edu": "Nonresidential/Educational", "k12": "Nonresidential/Educational/Primary/secondary",
         "higher": "Nonresidential/Educational/Higher education", "other": "Nonresidential/Educational/Other educational",
         "library": "Nonresidential/Educational/Other educational/Library/archive",
         "dorm": "Nonresidential/Educational/Higher education/Dormitory", "parking": "Nonresidential/Educational/Higher education/Parking",
         "union": "Nonresidential/Educational/Higher education/Student union/cafeteria"}
    missing = [k for k, p in P.items() if p not in vip]
    if missing:
        raise SystemExit(f"[BLOCKED] VIP rows not found: {missing}")
    w = {int(r["year"]): float(r["pim_weight_in_2024_stock"]) for r in key_rows}
    post = [y for y in sorted(w) if SL.VINTAGE_SPLIT <= y <= YEAR]
    gate("vip_parse_matches_the_school_lanes", all(abs(vip[P["k12"]][y] / vip[P["edu"]][y] - float(r["vip_k12_share"])) < 1e-6
                                                   for r in key_rows for y in [int(r["year"])] if r["vip_k12_share"]),
         "primary/secondary over educational, 1993-2024, equals k12_share_key.csv")
    part = lambda name, y: vip[P[name]][y] / vip[P["edu"]][y]
    nonk12 = sum(w[y] * (1 - part("k12", y)) for y in post)
    comp = {"higher": sum(w[y] * part("higher", y) for y in post) / nonk12,
            "library": sum(w[y] * part("library", y) for y in post) / nonk12,
            "museum_zoo": sum(w[y] * (part("other", y) - part("library", y)) for y in post) / nonk12}
    comp["preschool_unlisted"] = 1 - sum(comp.values())
    aux = sum(w[y] * (vip[P["dorm"]][y] + vip[P["parking"]][y] + vip[P["union"]][y]) / vip[P["edu"]][y] for y in post) \
        / sum(w[y] * part("higher", y) for y in post)
    gate("vip_composition_of_the_non_k12_part", all(0 <= v < 1 for v in comp.values()) and 0.8 < comp["higher"] < 0.95,
         f"higher {comp['higher']:.4f}, library {comp['library']:.4f}, museums and zoos {comp['museum_zoo']:.4f}, "
         f"preschool and unlisted {comp['preschool_unlisted']:.4f}")
    # BEA's types against Census's categories (context for what BEA's Office holds; not used in the return).
    VIPX = {"office": "Nonresidential/Office", "public_safety": "Nonresidential/Public Safety",
            "correctional": "Nonresidential/Public Safety/Correctional", "fire_rescue": "Nonresidential/Public Safety/Other public safety/Fire/rescue",
            "health": "Nonresidential/Health Care", "educational": P["edu"]}
    if any(p not in vip for p in VIPX.values()):
        raise SystemExit("[BLOCKED] VIP comparison rows not found")
    type_rows = [[y, bn(INV[59][y]), vip[VIPX["office"]][y] / 1000, bn(INV[63][y]), vip[VIPX["public_safety"]][y] / 1000,
                  vip[VIPX["correctional"]][y] / 1000, vip[VIPX["fire_rescue"]][y] / 1000, bn(INV[61][y]), vip[VIPX["health"]][y] / 1000,
                  bn(INV[62][y]), vip[VIPX["educational"]][y] / 1000] for y in range(SL.VINTAGE_SPLIT, YEAR + 1)]
    office_ratio = [r[1] / r[2] for r in type_rows]
    ps_ratio = [r[3] / r[5] for r in type_rows]
    nonk12_stock = (1 - k12_key) * edu_avg
    college_fee = comp["higher"] * f_tuition + comp["library"] * 1.0     # museums, zoos (recreation) and preschool not charged
    # [id, line (key and response), label, BEA lines, national stock, fee factor, charged stock, depreciation 2024]
    COMP = [
        ["k12", "k12", "K-12 schools: educational structures x K-12 key plus K-12 equipment and software (school lane)",
         "FAAt701 l62 x key; l56+l73 x F-33 key", k12["avg2024"], 1.0, k12["avg2024"], k12["depreciation_2024"]],
        ["college", "college", "colleges and other education: non-K-12 educational structures; higher education net of tuition; "
                               "libraries in full; museums and zoos (recreation) and preschool not charged",
         "FAAt701 l62 x (1 - key)", nonk12_stock, college_fee, nonk12_stock * college_fee, bn(D[62][YEAR]) * (1 - k12_key) * college_fee],
        ["pos_sl", "public_order_safety", "public order and safety (state and local): public safety structures", "FAAt701 l63",
         avg(63), 1.0, avg(63), bn(D[63][YEAR])],
        ["pos_fed", "public_order_safety", "public order and safety (federal nondefense): public safety structures", "FAAt701 l45",
         avg(45), 1.0, avg(45), bn(D[45][YEAR])],
        ["health_sl", "health_services", "health (state and local): health care structures net of hospital sales", "FAAt701 l61",
         avg(61), f_health, avg(61) * f_health, bn(D[61][YEAR]) * f_health],
        ["health_fed", "health_services", "health (federal nondefense): health care structures", "FAAt701 l43",
         avg(43), 1.0, avg(43), bn(D[43][YEAR])],
        ["gps_sl", "general_public_services", "general government (state and local): office structures incl. city halls; capitols; "
                                              "courthouses; administration buildings", "FAAt701 l59", avg(59), 1.0, avg(59), bn(D[59][YEAR])],
        ["gps_fed", "general_public_services", "general government (federal nondefense): office structures", "FAAt701 l41",
         avg(41), 1.0, avg(41), bn(D[41][YEAR])],
    ]
    LINE_OF = {"k12": "education_services", "college": "education_services", "pos_sl": "public_order_safety",
               "pos_fed": "public_order_safety", "health_sl": "health_services", "health_fed": "health_services",
               "gps_sl": "general_public_services", "gps_fed": "general_public_services"}
    STRUCT = {"k12": k12["structures_avg2024"], "college": nonk12_stock * college_fee}
    for c in COMP[2:]:
        STRUCT[c[0]] = c[6]

    # ---------------- 6. the return, specification by specification
    def ret(stocks: dict, i: int, m: str, r: float, resp_override: dict | None = None, key_override: dict | None = None) -> dict:
        out = {}
        v = V[m][i]
        for cid, line, *_ in COMP:
            key, resp = v[line]
            if key_override and cid in key_override:
                key = v[key_override[cid]][0]
            if resp_override and cid in resp_override:
                resp = resp_override[cid](specs[i], resp)
            out[cid] = stocks[cid] * r * key * resp
        return out

    charged = {c[0]: c[6] for c in COMP}
    all_rates = dict(RATES, **REPORTED)
    R = {lab: {m: [ret(charged, i, m, r) for i in range(n)] for m in methods} for lab, r in all_rates.items()}
    total = {lab: {m: [sum(x.values()) for x in R[lab][m]] for m in methods} for lab in all_rates}

    # gate: K-12 reproduces the school lane at every specification
    g_k12 = {lab: school_committed["group_return_bn"][lab]["central"] if lab in RATES else school_committed["group_return_bn"]["7pct_reported_only"]
             for lab in all_rates}
    gate("k12_reproduces_the_school_lane", all(abs(R[lab][m][i]["k12"] - g_k12[lab]) < 1e-9 for lab in all_rates for m in methods for i in range(n))
         and all(abs(school["group_return_bn"][lab]["central"] - g_k12[lab]) < 1e-12 for lab in RATES),
         f"2% {g_k12['2pct']:.4f}, 3% {g_k12['3pct']:.4f}, 7% {g_k12['7pct']:.4f} at every specification; rerun of the school "
         f"lane equals its committed summary")
    land10_k12 = {lab: 0.10 * r * k12["structures_avg2024"] * s_pupil for lab, r in RATES.items()}
    gate("k12_land_conversion_reproduces_the_school_lane",
         all(abs(land10_k12[lab] - school_committed["land_return_per_10pct_land_to_structure_ratio_bn"][f"A-4 {'2023' if lab == '2pct' else '2003'} ({lab[0]}%)"]) < 1e-9
             for lab in RATES), f"{land10_k12['2pct']:.4f} / {land10_k12['3pct']:.4f}")

    def with_case(ret_by_method: dict) -> dict:
        return {m: [costs[m][i] + ret_by_method[m][i] for i in range(n)] for m in methods}

    def at(ret_by_method: dict, i: int) -> float:
        return sum(ret_by_method[m][i] for m in methods) / len(methods)

    def band_row(name: str, lab: str, ret_by_method: dict, note: str) -> list:
        b = band_of(with_case(ret_by_method))
        lo_i = b["low_spec"][0] if len(set(b["low_spec"])) == 1 else None
        hi_i = b["high_spec"][0] if len(set(b["high_spec"])) == 1 else None
        return [name, lab, b["low"], b["high"], "/".join(str(x) for x in b["low_spec"]), "/".join(str(x) for x in b["high_spec"]),
                at(ret_by_method, CASE_ENDS[0]), at(ret_by_method, CASE_ENDS[1]),
                at(ret_by_method, lo_i) if lo_i is not None else None, at(ret_by_method, hi_i) if hi_i is not None else None,
                b["low"] - case_band["low"], b["high"] - case_band["high"], note]

    band_rows = [["adopted main case (no return)", "", case_band["low"], case_band["high"], "/".join(map(str, case_band["low_spec"])),
                  "/".join(map(str, case_band["high_spec"])), 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, "main_case_schools_full_2026_09_26"]]
    for lab in all_rates:
        band_rows.append(band_row("candidate: consistent return on public capital", lab, total[lab],
                                  "reported only" if lab in REPORTED else "structures by type plus K-12 equipment"))
    cand = {lab: band_of(with_case(total[lab])) for lab in all_rates}
    gate("candidate_band_is_ordered_and_above_the_case", all(case_band["low"] < cand[lab]["low"] < cand[lab]["high"]
                                                           and case_band["high"] < cand[lab]["high"] for lab in all_rates),
         "; ".join(f"{lab} {cand[lab]['low']:.2f}-{cand[lab]['high']:.2f}" for lab in all_rates))
    # The brief's band: 2% at the low end and 3% at the high end, each end over the specifications.
    rate_band = {"low": cand["2pct"]["low"], "high": cand["3pct"]["high"], "low_spec": cand["2pct"]["low_spec"],
                 "high_spec": cand["3pct"]["high_spec"]}
    band_rows.insert(1, ["candidate: 2% at the low end and 3% at the high end", "2pct/3pct", rate_band["low"], rate_band["high"],
                         "/".join(map(str, rate_band["low_spec"])), "/".join(map(str, rate_band["high_spec"])),
                         at(total["2pct"], CASE_ENDS[0]), at(total["3pct"], CASE_ENDS[1]),
                         at(total["2pct"], rate_band["low_spec"][0]), at(total["3pct"], rate_band["high_spec"][0]),
                         rate_band["low"] - case_band["low"], rate_band["high"] - case_band["high"],
                         "the brief's rates as the band's ends; the return at spec 48 is at 2% and at spec 11 at 3%"])
    gate("rate_band_ends_keep_the_case_specifications", len(set(rate_band["low_spec"])) == 1 and len(set(rate_band["high_spec"])) == 1,
         f"low end at spec {rate_band['low_spec']}, high end at spec {rate_band['high_spec']}")

    # ---------------- 7. variants (sensitivities; 2% and 3% only)
    # Equipment and software, where NIPA 3.17's function investment less the mapped structure types gives a share
    # of equipment + software investment (mean of 2019 and 2024; the school lane's method for education's share).
    def mshare(level, f):
        return sum(resid[(level, f, y)] / resid[(level, "eqsw", y)] for y in EQUIP_YEARS) / len(EQUIP_YEARS)
    edu_share = sum((resid[("state_local", "education", y)]) / resid[("state_local", "eqsw", y)] for y in EQUIP_YEARS) / len(EQUIP_YEARS)
    k12_eq = school["k12_equipment_software_key"]["central"]
    eq_sl_stock = avg(56) + avg(73)
    eq_fed_stock = avg(39) + avg(53)
    EQ = [  # id, line, stock, fee, share
        ["eq_college_sl", "college", eq_sl_stock, college_fee / (comp["higher"] + comp["library"]), edu_share - k12_eq],
        ["eq_pos_sl", "public_order_safety", eq_sl_stock, 1.0, mshare("state_local", "public_order_safety")],
        ["eq_health_sl", "health_services", eq_sl_stock, f_health, mshare("state_local", "health")],
        ["eq_gps_sl", "general_public_services", eq_sl_stock, 1.0, mshare("state_local", "general_public_services")],
        ["eq_income_security_sl", "income_security_services", eq_sl_stock, 1.0, mshare("state_local", "income_security")],
        ["eq_pos_fed", "public_order_safety", eq_fed_stock, 1.0, mshare("federal_nondefense", "public_order_safety")],
        ["eq_gps_fed", "general_public_services", eq_fed_stock, 1.0, mshare("federal_nondefense", "general_public_services")],
        ["eq_income_security_fed", "income_security_services", eq_fed_stock, 1.0, mshare("federal_nondefense", "income_security")],
    ]
    gate("equipment_shares_are_shares", all(0 <= e[4] < 0.5 for e in EQ), ", ".join(f"{e[0]} {e[4]:.3f}" for e in EQ))

    def eq_ret(i, m, r):
        v = V[m][i]
        return sum(e[2] * e[4] * e[3] * r * v[e[1]][0] * v[e[1]][1] for e in EQ)

    row8_step = (rv["b_all"] - rv["b_admin"]) * meta["row8_factor"]
    gate("row8_increment_from_the_case", abs(meta["row8_factor"] - rv["row8_factor_national_memo"]) < 1e-12,
         f"(b_all {rv['b_all']} - b_admin {rv['b_admin']}) x row 8 factor {meta['row8_factor']:.4f} = {row8_step:.4f}")
    k12_end = school["national_k12_capital_bn"]["central"]["end2024"]
    end_stock = {"k12": k12_end, "college": (1 - k12_key) * bn(K[62][YEAR]) * college_fee, "pos_sl": bn(K[63][YEAR]),
                 "pos_fed": bn(K[45][YEAR]), "health_sl": bn(K[61][YEAR]) * f_health, "health_fed": bn(K[43][YEAR]),
                 "gps_sl": bn(K[59][YEAR]), "gps_fed": bn(K[41][YEAR])}
    aux_stock = dict(charged, college=nonk12_stock * (comp["higher"] * (1 - aux) * f_tuition + comp["library"]))
    VARIANTS = {
        "equipment_and_software": ("adds state and local and federal nondefense equipment and software by NIPA 3.17's function "
                                   "investment less the mapped structures (a derived split; federal health's is inseparable from R&D)",
                                   lambda i, m, r: sum(ret(charged, i, m, r).values()) + eq_ret(i, m, r)),
        "sl_office_at_unallocable_response": ("state and local offices at the general-government response plus audit row 8's "
                                              f"increment ({row8_step:.4f}), the response the case gives unallocable S&L spending",
                                              lambda i, m, r: sum(ret(charged, i, m, r, resp_override={"gps_sl": lambda sp, x: x + row8_step}).values())),
        "offices_at_response_1": ("all offices at response 1 (population key): an upper bound if offices served only fully "
                                  "responding lines", lambda i, m, r: sum(ret(charged, i, m, r, resp_override={
                                      "gps_sl": lambda sp, x: 1.0, "gps_fed": lambda sp, x: 1.0}).values())),
        "k12_at_account_school_key": ("K-12 at the account's own school key (education line plus school re-price over the "
                                      "national line) instead of the pupil share", lambda i, m, r: sum(ret(
                                          charged, i, m, r, key_override={"k12": "k12_account_key"}).values())),
        "higher_ed_auxiliaries_fee_financed": (f"dormitories, parking and student unions ({aux:.3f} of higher-education "
                                               "construction) recovered by their own fees", lambda i, m, r: sum(ret(aux_stock, i, m, r).values())),
        "end_2024_stocks": ("end-2024 stocks instead of the 2024 average", lambda i, m, r: sum(ret(end_stock, i, m, r).values())),
        "college_by_account_school_fraction": ("college capital as (1 - the specification's school fraction) of educational "
                                               "structures instead of (1 - the K-12 key); K-12 unchanged, so the two need not "
                                               "add to the stock", lambda i, m, r: sum(ret(charged, i, m, r).values())
                                               + ret(charged, i, m, r)["college"] * ((1 - specs[i]["share"]) / (1 - k12_key) - 1)),
    }
    VR = {}
    for name, (note, fn) in VARIANTS.items():
        for lab, r in RATES.items():
            VR[(name, lab)] = {m: [fn(i, m, r) for i in range(n)] for m in methods}
            band_rows.append(band_row(f"variant: {name}", lab, VR[(name, lab)], note))

    # ---------------- 8. gaps, each as the group's return at the case's end specifications if it were charged
    def conv(stock: float, line: str, r: float, i: int, fee: float = 1.0) -> float:
        return sum(stock * fee * r * V[m][i][line][0] * V[m][i][line][1] for m in methods) / len(methods)

    gap_rows = []

    def gap(item, basis, stock, line, fee=1.0, note=""):
        gap_rows.append([item, basis, stock, fee, line] + [conv(stock, line, r, i, fee) for r in RATES.values() for i in CASE_ENDS] + [note])

    for cid, line, label, bea, *_ in COMP:
        gap(f"land at 10% of the structures charged: {cid}", bea, 0.10 * STRUCT[cid], line, 1.0,
            "[GAP] BEA measures produced assets only; a conversion per 10% of land-to-structure value; not an estimate")
    fh = {y: resid[("federal_nondefense", "health", y)] for y in EQUIP_YEARS}
    fed_eqsw_inv = {y: resid[("federal_nondefense", "eqsw", y)] for y in EQUIP_YEARS}
    rd_health_lo = sum(max(0.0, fh[y] - fed_eqsw_inv[y]) / fed_rd[y] for y in EQUIP_YEARS) / len(EQUIP_YEARS)
    rd_health_hi = sum(min(1.0, fh[y] / fed_rd[y]) for y in EQUIP_YEARS) / len(EQUIP_YEARS)
    gap("R&D (state and local): university research inside NIPA's education investment", "FAAt701 l74", avg(74), "college",
        1.0, "[GAP] no BEA function split of R&D; non-rival; so a removal need not reduce it")
    gap(f"R&D (federal nondefense): health's share at its lower bound {rd_health_lo:.3f}", "FAAt701 l54 x share", avg(54) * rd_health_lo,
        "health_services", 1.0, "[GAP] federal health investment less health structures and all federal nondefense equipment and software")
    gap(f"R&D (federal nondefense): health's share at its upper bound {rd_health_hi:.3f}", "FAAt701 l54 x share", avg(54) * rd_health_hi,
        "health_services", 1.0, "[GAP] federal health investment less health structures; all of it R&D")
    for e in EQ:
        gap(f"equipment and software (derived split): {e[0]} share {e[4]:.4f}", "FAAt701 l56+l73" if e[0].endswith("_sl") else "FAAt701 l39+l53",
            e[2] * e[4], e[1], e[3], "[GAP] not in the central; in the equipment_and_software variant")
    gap("federal nondefense educational structures (no K-12/other split)", "FAAt701 l44", avg(44), "college", 1.0,
        "[GAP] converted at the college key; the school lane's K-12 excludes them too")
    san_share = sum(bn(t3155[103][y] - t317[25][y]) / bn(INV[68][y]) for y in EQUIP_YEARS) / len(EQUIP_YEARS)
    gap(f"sanitation structures inside Sewer systems (upper bound: sanitation investment share {san_share:.3f})", "FAAt701 l68 x share",
        avg(68) * san_share, "housing_community_services", 1.0, "[GAP] the only tax-financed part of housing and community services")
    gap("preschool and unlisted educational structures (VIP residual)", "FAAt701 l62 x (1 - key) x share",
        nonk12_stock * comp["preschool_unlisted"], "college", 1.0, "[GAP] childcare centres may serve income security instead")
    for line_no, label, lid in ((60, "state and local commercial structures (parking and warehouses)", "general_public_services"),
                                (71, "state and local other structures (lodging; communication; manufacturing)", "general_public_services"),
                                (42, "federal nondefense commercial structures", "general_public_services"),
                                (51, "federal nondefense other structures", "general_public_services")):
        gap(label, f"FAAt701 l{line_no}", avg(line_no), lid, 1.0, "[GAP] no function; converted at the general-government key and response")
    # Conditional: lines held fixed in the main case. If a later case lets them respond, multiply by that response.
    gap("conditional per unit of response: economic affairs tax-financed structures (highways and streets; conservation and development)",
        "FAAt701 l67+l70+l49+l50", avg(67) + avg(70) + avg(49) + avg(50), "economic_affairs_per_unit_response", 1.0,
        "held fixed now; multiply by the line's response if it ever responds")
    gap("conditional per unit of response: economic affairs transportation and power (largely fee-financed)",
        "FAAt701 l65+l66+l47+l48", avg(65) + avg(66) + avg(47) + avg(48), "economic_affairs_per_unit_response", 1.0,
        "held fixed now; fee recovery not netted")
    gap("conditional per unit of response: recreation and culture (amusement and recreation; museums and zoos)",
        "FAAt701 l64+l46; l62 x (1 - key) x share", avg(64) + avg(46) + nonk12_stock * comp["museum_zoo"],
        "recreation_per_unit_response", 1.0, "held fixed now; multiply by the line's response if it ever responds")

    # ---------------- 9. double counts
    engine = (FISCAL / "assumption_explorer_2026_09_21" / "engine.js").read_text()
    debt = re.sub(r"\s+", " ", DEBT_RESULT.read_text())
    gate("interest_row_held_at_zero", 'case "interest": return state.interest_response;' in engine and all(
        per[m][i]["lines"]["domestic_interest"]["response"] == 0 for m in methods for i in range(n)),
         "domestic_interest responds at 0 at every specification of the evaluation cost() makes")
    gate("debt_legacy_is_federal_only", "State-local interest ($274.6bn) sits in the account's interest row" in debt
         and "no-legacy framing for state-local gaps" in debt, "debt_legacy_2026_09_23 RESULT.md")
    matched = re.sub(r"\s+", " ", MATCHED.read_text())
    production_dims = json.loads(MODEL.read_text())["production"]["dims"]
    gate("production_term_pays_private_capital_only", "The model pays the opportunity cost of capital" in matched
         and "capital_adjustment" in production_dims and "labor_share" in production_dims,
         "matched-benefits memo: the CES term pays capital its rental rate (dims capital_adjustment, labor_share); "
         "public capital earns no market rental there [INFERENCE]")
    decision = re.sub(r"\s+", " ", DECISION.read_text())
    gate("new_seats_and_land_unpriced", "new seats at today's construction cost" in decision,
         "decisions/2026-09-26-main-case-schools-full-cost.md lists new seats as unpriced; land is a gap here")

    # ---------------- every asset type and its treatment
    TYPE_TREAT = {
        22: ("federal", "national defense (all assets)", "response 0", "defense responds at 0"),
        39: ("federal nondefense", "equipment", "gap", "no function split (equipment_and_software variant: POS, general government, income security)"),
        41: ("federal nondefense", "office", "charged", "general government"),
        42: ("federal nondefense", "commercial", "gap", "no function"),
        43: ("federal nondefense", "health care", "charged", "health"),
        44: ("federal nondefense", "educational", "gap", "no K-12/other split"),
        45: ("federal nondefense", "public safety", "charged", "public order and safety"),
        46: ("federal nondefense", "amusement and recreation", "held fixed", "recreation and culture"),
        47: ("federal nondefense", "transportation", "held fixed", "economic affairs"),
        48: ("federal nondefense", "power", "held fixed", "economic affairs; fee-financed"),
        49: ("federal nondefense", "highways and streets", "held fixed", "economic affairs"),
        50: ("federal nondefense", "conservation and development", "held fixed", "economic affairs"),
        51: ("federal nondefense", "other structures", "gap", "no function"),
        53: ("federal nondefense", "software", "gap", "no function split"),
        54: ("federal nondefense", "research and development", "gap", "health's share bounded; non-rival"),
        56: ("state and local", "equipment", "K-12 part charged", "K-12 by F-33; the rest a gap (equipment_and_software variant)"),
        58: ("state and local", "residential", "excluded", "public housing: enterprise; fee-financed"),
        59: ("state and local", "office", "charged", "general government (NIPA files it there)"),
        60: ("state and local", "commercial", "gap", "no function"),
        61: ("state and local", "health care", "charged", f"health; x{f_health:.4f} for hospital sales"),
        62: ("state and local", "educational", "charged", "K-12 and colleges and libraries; museums and zoos held fixed; preschool a gap"),
        63: ("state and local", "public safety", "charged", "public order and safety"),
        64: ("state and local", "amusement and recreation", "held fixed", "recreation and culture"),
        65: ("state and local", "transportation", "held fixed", "economic affairs; largely fee-financed"),
        66: ("state and local", "power", "held fixed", "economic affairs; fee-financed utilities"),
        67: ("state and local", "highways and streets", "held fixed", "economic affairs"),
        68: ("state and local", "sewer systems", "excluded", "enterprise; fee-financed; the sanitation part is a gap"),
        69: ("state and local", "water systems", "excluded", "enterprise; fee-financed"),
        70: ("state and local", "conservation and development", "held fixed", "economic affairs"),
        71: ("state and local", "other structures", "gap", "no function"),
        73: ("state and local", "software", "K-12 part charged", "K-12 by F-33; the rest a gap"),
        74: ("state and local", "research and development", "gap", "university research; non-rival"),
    }
    type_acc = [[lv, ln, t, avg(ln), bn(D[ln][YEAR]), tr, why] for ln, (lv, t, tr, why) in TYPE_TREAT.items()]
    covered = sum(avg(ln) for ln in TYPE_TREAT)
    gate("asset_type_accounting_covers_all_government_capital", abs(covered - avg(1)) < 0.001 * avg(1),
         f"types {covered:.1f} vs all government fixed assets {avg(1):.1f} (FAAt701 l1, 2024 average)")

    # ---------------- gates
    failed = [g for g in GATES if not g[1]]
    for name, ok, detail in GATES:
        print(f"  {'PASS' if ok else 'FAIL'}  {name}: {detail}")
    if failed:
        print(f"[BLOCKED] {len(failed)} gate(s) failed; nothing written")
        return 1

    # ---------------- outputs
    DERIVED.mkdir(exist_ok=True)

    def write_csv(name: str, header: list[str], rows: list[list]) -> None:
        with (DERIVED / name).open("w", newline="") as f:
            wr = csv.writer(f, lineterminator="\n")
            wr.writerow(header)
            wr.writerows(rows_out(rows))

    TREAT = {
        "general_public_services": ("charged", "S&L and federal nondefense Office (FAAt701 l59, l41): city halls, capitols, courthouses, "
                                    "administration buildings; NIPA files S&L office investment under this line"),
        "defense": ("response 0", "national defense responds at 0"),
        "public_order_safety": ("charged", "S&L and federal nondefense Public safety (l63, l45); courthouses sit in Office"),
        "economic_affairs_services": ("held fixed", "response 0 in the main profile: highways, transportation, power, conservation"),
        "housing_community_services": ("excluded: fee-financed", "S&L consumption is sanitation only (NIPA 3.16 note 8); residential, "
                                       "water and sewer are enterprise capital recovered by fees; sanitation is a gap"),
        "health_services": ("charged", f"S&L Health care (l61) x net/gross {f_health:.4f}; federal nondefense Health care (l43)"),
        "recreation_culture": ("held fixed", "response 0 in the main profile: amusement and recreation, museums and zoos"),
        "education_services": ("charged", "K-12 (school lane) and colleges and other education (non-K-12 educational structures)"),
        "income_security_services": ("no identified capital", "no BEA structure type; its offices sit in Office (charged under general "
                                     "government); equipment and software a gap"),
        "domestic_interest": ("response 0", "existing interest held at 0 (double-count gate)"),
        "foreign_interest": ("outside the resident account", "foreign flow"),
        "school_reprice": ("charged with education", "school part's correction; K-12 capital uses the pupil share"),
        "college_rekey": ("charged with education", "college part's correction; enters the college key"),
        "lane_constants": ("no capital", "care, shelter and audit-row constants carry no BEA asset type"),
    }
    inv_rows = []
    all_lines = case["inventory"] + [dict(id=l["id"], family=l["family"], national_bn=0.0, response_class=l["response_class"],
                                          preferred_key="k") for l in case["synthetic_lines"]]
    for l in all_lines:
        lid = l["id"]
        resp = [per[m][i]["lines"][lid]["response"] for m in methods for i in range(n)]
        keys = sorted({per[m][i]["lines"][lid]["key"] for m in methods for i in range(n)})
        shares = [per[m][i]["lines"][lid]["amount_bn"] / l["national_bn"] for m in methods for i in range(n)] if l["national_bn"] else [None]
        if lid in TREAT:
            t, why = TREAT[lid]
        elif l["response_class"] == "household_transfer":
            t, why = "transfer", "household transfer: no public capital (administration capital sits in the function lines)"
        elif l["response_class"] == "subsidy":
            t, why = "response 0", "subsidies respond at 0"
        else:
            t, why = "outside the resident account", "foreign flow or rounding"
        inv_rows.append([lid, l["family"], l["national_bn"], l["response_class"], min(resp), max(resp), "|".join(keys),
                         min(shares) if shares[0] is not None else "", max(shares) if shares[0] is not None else "", t, why])
    write_csv("lines.csv", ["line_id", "family", "national_bn", "response_class", "main_case_response_min", "main_case_response_max",
                            "key_rule", "key_share_min", "key_share_max", "capital_treatment", "reason"], inv_rows)

    comp_rows = []
    for cid, line, label, bea, stock, fee, ch, dep in COMP:
        keys = [V[m][i][line][0] for m in methods for i in range(n)]
        resps = [V[m][i][line][1] for m in methods for i in range(n)]
        row = [cid, line, label, bea, stock, fee, ch, dep, min(keys), max(keys), min(resps), max(resps)]
        for lab in all_rates:
            vals = [R[lab][m][i][cid] for m in methods for i in range(n)]
            row += [sum(R[lab][m][CASE_ENDS[0]][cid] for m in methods) / len(methods),
                    sum(R[lab][m][CASE_ENDS[1]][cid] for m in methods) / len(methods), min(vals), max(vals)]
        comp_rows.append(row)
    hdr = ["component", "line", "label", "bea_source", "national_stock_avg2024_bn", "fee_factor", "stock_charged_bn",
           "depreciation_2024_charged_basis_bn", "key_min", "key_max", "response_min", "response_max"]
    for lab in all_rates:
        hdr += [f"return_{lab}_spec{CASE_ENDS[0]}_bn", f"return_{lab}_spec{CASE_ENDS[1]}_bn", f"return_{lab}_min_bn", f"return_{lab}_max_bn"]
    write_csv("components.csv", hdr, comp_rows)

    spec_rows, comp_long = [], []
    for m in methods:
        for i, sp in enumerate(specs):
            spec_rows.append([m, i, sp["allocation"], sp["normalization"], sp["share"], sp["school"], sp["gg"], sp["uc"], sp["justice"],
                              costs[m][i]] + [total[lab][m][i] for lab in all_rates] + [costs[m][i] + total[lab][m][i] for lab in all_rates])
            for cid, line, *_ in COMP:
                comp_long.append([m, i, cid, charged[cid], V[m][i][line][0], V[m][i][line][1]] + [R[lab][m][i][cid] for lab in all_rates])
    write_csv("per_spec.csv", ["method", "spec", "allocation", "normalization", "school_share", "school_response", "gg_response",
                               "uc_key", "justice_key", "case_cost_bn"] + [f"return_{lab}_bn" for lab in all_rates]
              + [f"cost_with_return_{lab}_bn" for lab in all_rates], spec_rows)
    write_csv("per_spec_components.csv", ["method", "spec", "component", "stock_charged_bn", "key", "response"]
              + [f"return_{lab}_bn" for lab in all_rates], comp_long)
    write_csv("bands.csv", ["case", "rate", "low_bn", "high_bn", "low_end_spec_by_method", "high_end_spec_by_method",
                            f"return_at_spec{CASE_ENDS[0]}_bn", f"return_at_spec{CASE_ENDS[1]}_bn", "return_at_own_low_end_bn",
                            "return_at_own_high_end_bn", "band_move_low_bn", "band_move_high_bn", "note"], band_rows)
    write_csv("gaps.csv", ["item", "bea_source", "national_base_bn", "fee_factor", "line_key_and_response"]
              + [f"group_{lab}_spec{i}_bn" for lab in RATES for i in CASE_ENDS] + ["note"], gap_rows)
    write_csv("asset_types.csv", ["level", "fa_line", "type", "stock_avg2024_bn", "depreciation_2024_bn", "treatment", "reason"], type_acc)
    write_csv("bea_vs_census_types.csv", ["year", "bea_sl_office_inv_bn", "vip_sl_office_bn", "bea_sl_public_safety_inv_bn",
                                          "vip_sl_public_safety_bn", "vip_sl_correctional_bn", "vip_sl_fire_rescue_bn",
                                          "bea_sl_health_care_inv_bn", "vip_sl_health_care_bn", "bea_sl_educational_inv_bn",
                                          "vip_sl_educational_bn"], type_rows)
    write_csv("mapping_check.csv", ["year", "level", "function", "nipa_3_17_line", "fa_lines", "gross_investment_bn",
                                    "mapped_structures_bn", "residual_bn", "residual_over_equipment_software",
                                    "total_residual_over_unmapped_assets"], map_rows)
    (DERIVED / "gates.json").write_text(json.dumps([{"gate": g, "pass": ok, "detail": d} for g, ok, d in GATES], indent=1) + "\n")

    ends = {lab: {"case_ends": [at(total[lab], CASE_ENDS[0]), at(total[lab], CASE_ENDS[1])],
                  "min_over_specs": min(min(total[lab][m]) for m in methods), "max_over_specs": max(max(total[lab][m]) for m in methods)}
            for lab in all_rates}
    summary = {
        "year": YEAR, "rates": all_rates,
        "case": {"band_bn": [case_band["low"], case_band["high"]], "end_specs": CASE_ENDS, "responses": meta},
        "group_return_bn": ends,
        "by_component_at_case_ends_bn": {cid: {lab: [sum(R[lab][m][i][cid] for m in methods) / len(methods) for i in CASE_ENDS]
                                               for lab in all_rates} for cid, *_ in COMP},
        "by_line_at_case_ends_bn": {line: {lab: [sum(R[lab][m][i][cid] for m in methods for cid in LINE_OF if LINE_OF[cid] == line)
                                                 / len(methods) for i in CASE_ENDS] for lab in all_rates}
                                    for line in dict.fromkeys(LINE_OF.values())},
        "gaps_at_case_ends_bn": {g[0]: {lab: [g[5 + 2 * j], g[6 + 2 * j]] for j, lab in enumerate(RATES)} for g in gap_rows},
        "land_per_10pct_total_at_case_ends_bn": {lab: [sum(g[5 + 2 * j + e] for g in gap_rows if g[0].startswith("land at 10%"))
                                                       for e in (0, 1)] for j, lab in enumerate(RATES)},
        "candidate_rate_band_bn": rate_band,
        "bea_office_over_vip_office_1993_2024": [min(office_ratio), max(office_ratio)],
        "bea_public_safety_over_vip_correctional_1993_2024": [min(ps_ratio), max(ps_ratio)],
        "candidate_band_bn": {lab: {"low": cand[lab]["low"], "high": cand[lab]["high"], "low_spec": cand[lab]["low_spec"],
                                    "high_spec": cand[lab]["high_spec"]} for lab in all_rates},
        "variants_bn": {f"{name}|{lab}": {"band": [band_of(with_case(VR[(name, lab)]))["low"], band_of(with_case(VR[(name, lab)]))["high"]],
                                          "return_case_ends": [at(VR[(name, lab)], i) for i in CASE_ENDS]}
                        for name in VARIANTS for lab in RATES},
        "fee_factors": {"health_state_local": f_health, "higher_education_tuition": f_tuition, "college_component": college_fee,
                        "federal_nondefense_sales_share_of_federal_health_max": fed_sales_share_max},
        "non_k12_educational_composition": comp, "higher_ed_auxiliary_share": aux,
        "k12": {"key_structures": k12_key, "capital_avg2024_bn": k12["avg2024"], "pupil_share": s_pupil,
                "school_lane_outputs_byte_identical_on_rerun": identical},
        "nipa_unallocable_over_sl_office_investment": unalloc_ratio,
        "equipment_software_shares": {e[0]: e[4] for e in EQ},
        "rd_health_share_bounds": [rd_health_lo, rd_health_hi], "sanitation_share_of_sewer_investment": san_share,
        "row8_response_increment": row8_step,
        "inputs": {str(p.relative_to(ROOT)): sha(p) for p in [
            DEFINITIONS, SL.NIPA3, SL.CACHE / "fa_Section7All_xls.xlsx", HELPER, MAIN / "package.cjs", MAIN / "derived" / "corrections.json",
            MAIN / "derived" / "summary.json", MAIN / "derived" / "main_case_bands.csv", SCHOOL / "capital_return.py",
            SCHOOL / "derived" / "summary.json", R_VALUES, DEBT_RESULT, MATCHED, DECISION,
            FISCAL / "assumption_explorer_2026_09_21" / "engine.js", FISCAL / "assumption_explorer_2026_09_21" / "derived" / "model.json",
            FISCAL / "main_case_2026_09_26" / "package.cjs", FISCAL / "main_case_2026_09_24" / "package.cjs"]},
        "gates_passed": len(GATES),
    }
    (DERIVED / "summary.json").write_text(json.dumps(summary, indent=1, sort_keys=True) + "\n")

    # ---------------- print
    print(f"\nCase: {case_band['low']:.4f}-{case_band['high']:.4f} (specs {CASE_ENDS[0]}/{CASE_ENDS[1]})")
    for lab in all_rates:
        e = ends[lab]
        print(f"Return {lab}: {e['case_ends'][0]:.3f} at spec {CASE_ENDS[0]}, {e['case_ends'][1]:.3f} at spec {CASE_ENDS[1]} "
              f"(range over specs {e['min_over_specs']:.3f}-{e['max_over_specs']:.3f}); candidate {cand[lab]['low']:.4f}-{cand[lab]['high']:.4f} "
              f"(specs {cand[lab]['low_spec']}/{cand[lab]['high_spec']})")
    for cid, *_ in COMP:
        print(f"  {cid:12s} " + "  ".join(f"{lab} {summary['by_component_at_case_ends_bn'][cid][lab][0]:.3f}/{summary['by_component_at_case_ends_bn'][cid][lab][1]:.3f}"
                                         for lab in all_rates))
    print(f"Candidate, 2% at the low end and 3% at the high end: {rate_band['low']:.4f}-{rate_band['high']:.4f}")
    for r in (x for x in band_rows if x[0].startswith("variant:")):
        print(f"  {r[0]:48s} {r[1]} {r[2]:.2f}-{r[3]:.2f}")
    print(f"{len(GATES)} gates passed; wall {time.time() - t0:.1f}s")
    return 0


if __name__ == "__main__":
    sys.exit(main())
