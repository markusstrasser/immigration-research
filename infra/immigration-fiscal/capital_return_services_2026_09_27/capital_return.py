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

A conditional block prices roads, transit and parks capital at the long-run responses of the sister
lane (`service_response_long_run_2026_09_27/derived/responses.json` and `per_spec_costs.csv`), beside
the core result. It also reads the Census individual-unit finance files (pinned by
`administration_response_2026_09_20/inputs.sha256.json`), BEA's enterprise working paper
(`_cache/bea_highfill_wp2022_8.*`), NIPA Handbook chapter 9 (`_cache/bea_nipa_handbook_chapter_09.*`)
and the land sources checked (`_cache/bea_larson_wp2015_3.*`, `bea_wasshausen_p2011_1.*`,
`frb_z1_table_descriptions.*`); each `.txt` is `pdftotext -layout` of its `.pdf`.

Enterprises follow one rule (the parent's, 2026-09-27): an enterprise whose charges fall short of its
production costs (BEA WP2022-8 Table 5) is charged, net of its charge share; one whose charges exceed
them is excluded. The pinned NIPA Section 1 workbook (Tables 1.7.5 and 1.10) and Table 3.8 check where
the enterprises' operating results sit, in the NIPAs and in the account.

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
import zipfile
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
LONGRUN = FISCAL / "service_response_long_run_2026_09_27" / "derived"
RESPONSES, LR_COSTS, LR_BAND = LONGRUN / "responses.json", LONGRUN / "per_spec_costs.csv", LONGRUN / "candidate_band.json"
LR_NET = LONGRUN / "net_change.json"                  # the congestion change beside the account (a social item)
COG_PINS = FISCAL / "administration_response_2026_09_20" / "inputs.sha256.json"
COG_API = FISCAL / "macro_closure_2026_09_19" / "_cache" / "finance_2022_us_combined.json"
COG_YEARS = (2012, 2017, 2018, 2019, 2020, 2021, 2022, 2023)
COG_FUNCS = {"01": "air transportation", "44": "regular highways", "45": "toll highways", "60": "parking facilities",
             "61": "parks and recreation", "87": "sea and inland ports", "94": "transit utility"}
HIGHFILL = CACHE / "bea_highfill_wp2022_8"            # BEA WP2022-8: the NIPA enterprise list and charges / production costs
HANDBOOK9 = CACHE / "bea_nipa_handbook_chapter_09"    # NIPA Handbook ch. 9: what consumption and investment include
HANDBOOK2 = CACHE / "bea_nipa_handbook_chapter_02"    # NIPA Handbook ch. 2 (December 2024): operating surplus is before interest
MP5 = CACHE / "bea_mp5_government_transactions"       # BEA MP-5 (2005): the enterprise surplus ignores interest
NIPA1 = ROOT / "sources" / "immigration-fiscal" / "data" / "external" / "bea_nipa" / "Section1All_xls.xlsx"
NIPA1_SHA = "238ba851c9a4932d91a0dedb1b3f2e6c6d37574d154a54267da18b9cb0921a19"   # the vintage debt_legacy pins
DEBT_SCRIPT = FISCAL / "debt_legacy_2026_09_23" / "debt_legacy.py"
LAND = {"bea_larson_wp2015_3": ("with 24% of the land area and $1.8 trillion of the value held by the federal government",
                                "Table 2: Land Quantities and Values by Sector: Washington, DC, 2013"),
        "frb_z1_table_descriptions": ("F.107, L.107: State and local governments",
                                      "including the value of structures, equipment, and software but not the value of land."),
        "bea_wasshausen_p2011_1": ("the net stock of structures (excluding land) is used in lieu of",)}

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


def rows_out(rows: list[list], digits: int = 6) -> list[list]:
    return [[round(x, digits) if isinstance(x, float) else x for x in r] for r in rows]


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


def pdf_text(stem: Path) -> str:
    """A cached source's text (pdftotext -layout of the cached PDF), whitespace-normalized."""
    pdf, txt = stem.with_suffix(".pdf"), stem.with_suffix(".txt")
    if not (pdf.exists() and txt.exists()):
        raise SystemExit(f"[BLOCKED] missing {pdf.relative_to(ROOT)} or its text: fetch it, then pdftotext -layout it")
    return re.sub(r"\s+", " ", txt.read_text(encoding="utf-8"))


def cog_national() -> dict:
    """Census individual-unit files: the US state-and-local row (001) of charges (A), current operation (E) and
    construction (F) for the block's functions, $ thousands, by survey year."""
    pins = json.loads(COG_PINS.read_text())
    out = {}
    for year in COG_YEARS:
        path = FISCAL / "local_spending_composition_2026_09_18" / "_cache" / f"indunit_{year}.zip"
        if pins.get(str(path.relative_to(FISCAL))) != sha(path):
            raise SystemExit(f"[BLOCKED] {path.name} does not match its pin in {COG_PINS.relative_to(ROOT)}")
        with zipfile.ZipFile(path) as z:
            names = [x for x in z.namelist() if Path(x).name.lower() == f"{year % 100}statetypepu.txt"]
            if len(names) != 1:
                raise SystemExit(f"[BLOCKED] {path.name}: expected one state-type file, found {names}")
            vals: dict = {}
            for line in z.read(names[0]).decode("latin-1").splitlines():
                p = line.split()
                if len(p) == 5 and p[0] == "001" and p[1][0] in "AEF" and p[1][1:] in COG_FUNCS:
                    if p[1] in vals or int(p[4]) != year % 100:
                        raise SystemExit(f"[BLOCKED] {path.name}: duplicate or off-vintage {p[1]}")
                    vals[p[1]] = float(p[2])
        missing = [c + f for f in COG_FUNCS for c in "AEF" if c + f not in vals]
        if missing:
            raise SystemExit(f"[BLOCKED] {path.name}: missing {missing}")
        out[year] = vals
    return out


def highfill_table5(text_path: Path) -> tuple[list[int], dict]:
    """BEA WP2022-8 Table 5: charges / production costs (operating expenditures plus CFC) by function, 1967-2017."""
    lines = text_path.read_text(encoding="utf-8").splitlines()
    i0 = [i for i, l in enumerate(lines) if "Table 5. Ratio of Charges to Production Costs" in l]
    if len(i0) != 1:
        raise SystemExit("[BLOCKED] BEA WP2022-8 Table 5 not found")
    hi = [i for i in range(i0[0], i0[0] + 4) if lines[i].strip().startswith("Function")][0]
    years = [int(x) for x in lines[hi].split()[1:]]
    num = re.compile(r"^(?:\d+(?:\.\d+)?|\.)$")
    rows, name = {}, None
    for l in lines[hi + 1:]:
        if l.strip().startswith("Notes:"):
            break
        toks = l.split()
        vals = [t for t in toks if num.match(t)]
        words = " ".join(t for t in toks if not num.match(t))
        if vals and len(vals) == len(years):
            rows[(words or name).strip()] = {y: (None if v == "." else float(v)) for y, v in zip(years, vals)}
            name = None
        elif words and not vals:
            name = words if name is None else name
    return years, rows


# ---------------------------------------------------------------- main
def main() -> int:
    t0 = time.time()
    if not DEFINITIONS.exists():
        raise SystemExit(f"[BLOCKED] missing {DEFINITIONS.relative_to(ROOT)}: fetch https://www.census.gov/construction/c30/definitions.html")
    SL = load_school_lane()
    school_reg = SL.check_cache()          # every cached primary file against the school lane's registry
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
    # model.json's own housing_support key, before the case's corrections re-key the line (for a variant only). The engine
    # charges a key's target_bn (engine.js evaluate), so the key is target_bn over the national line, not the cell's share.
    hs_line = [l for l in json.loads(MODEL.read_text())["spending"]["lines"] if l["id"] == "housing_subsidies"][0]
    hs_cells = hs_line["keys"]["housing_support"]
    hs_target = hs_cells["personal"]["target_bn"]
    hs_base = hs_target / hs_line["national_bn"]
    if hs_cells["shared"]["target_bn"] != hs_target:
        raise SystemExit("[BLOCKED] model.json's housing_support amount differs by allocation")
    hs_edit = {a: sum(e["by"][a] for e in corrections["edits"] if e["side"] == "spending" and e["line"] == "housing_subsidies"
                      and e["key"] == "housing_support") for a in ("personal", "shared")}
    if hs_edit["personal"] != hs_edit["shared"]:
        raise SystemExit("[BLOCKED] the case's housing_support edit differs by allocation")

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
                         ("income_security_services", "cash_assistance"), ("housing_community_services", "population"),
                         ("housing_subsidies", "housing_support")):
            if L[lid]["key"] != key:
                view_err.append(f"{lid} keyed {L[lid]['key']} at {m}/{i}")
        k = lambda lid: L[lid]["amount_bn"] / L[lid]["national_bn"]
        ent = per[m][i]["enterprise"]
        return {
            # K-12 at the account's own school key (the case's rule): the education line plus school_reprice over the
            # national line; both carry the school fraction, which cancels. The school lane's pupil share is a variant.
            "k12": ((edu["amount_bn"] + sch["amount_bn"]) / edu["national_bn"], school_r),
            "k12_pupil_share": (s_pupil, school_r),
            "college": ((edu["amount_bn"] + col["amount_bn"]) / edu["national_bn"], college_r),
            "public_order_safety": (k("public_order_safety"), L["public_order_safety"]["response"]),
            "health_services": (k("health_services"), L["health_services"]["response"]),
            "general_public_services": (k("general_public_services"), L["general_public_services"]["response"]),
            "income_security_services": (k("income_security_services"), L["income_security_services"]["response"]),
            "housing_community_services": (k("housing_community_services"), L["housing_community_services"]["response"]),
            # Every enterprise's capital under option D: the enterprise-surplus receipt's own key at response 1.
            "enterprise": (ent["amount_bn"] / ent["national_bn"], 1.0),
            # Public housing at the rental-assistance key (a variant): the housing_subsidies line's key at response 1.
            "housing_subsidies_at_response_1": (k("housing_subsidies"), 1.0),
            "housing_support_uncorrected": (hs_base, 1.0),
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
    hs_eval = [sum(per[m][i]["lines"]["housing_subsidies"]["amount_bn"] for m in methods) / len(methods) for i in range(n)]
    gate("rental_key_is_model_json_plus_the_cases_edit",
         all(abs(a - (hs_target + hs_edit["personal"])) < 1e-9 for a in hs_eval)
         and all(per[m][i]["lines"]["housing_subsidies"]["national_bn"] == hs_line["national_bn"] for m in methods for i in range(n)),
         f"evaluated rental assistance, mean of methods, {hs_eval[0]:.4f} = model.json {hs_target:.4f} + corrections.json "
         f"{hs_edit['personal']:+.4f} at every specification; key {hs_base:.4f} before the edit")
    # The enterprise-surplus receipt's key, which keys every enterprise's capital under option D. The case's corrections
    # re-key the population-keyed spending lines (the CPS lane's stack) and leave this receipt at model.json's amount.
    mj_receipts = json.loads(MODEL.read_text())["receipts"]
    es_line = [l for l in mj_receipts["lines"] if l["id"] == "enterprise_surplus"][0]
    es_target = {c["target_bn"] for c in es_line["cells"][mj_receipts["reference"]].values()}   # the receipt scenario the case uses
    pop_edited = sorted({e["line"] for e in corrections["edits"] if e["side"] == "spending" and e.get("key") == "population"})
    gate("enterprise_receipt_is_model_jsons_resident_share",
         len(es_target) == 1 and not any(e["line"] == "enterprise_surplus" for e in corrections["edits"])
         and all(abs(per[m][i]["enterprise"]["amount_bn"] - next(iter(es_target))) < 1e-9 for m in methods for i in range(n)),
         f"enterprise_surplus: model.json's {next(iter(es_target)):.6f}bn (resident_population, key "
         f"{V[methods[0]][CASE_ENDS[0]]['enterprise'][0]:.6f}) at every specification, with no corrections.json edit; the "
         f"corrections re-key {len(pop_edited)} population-keyed spending lines (general_public_services at "
         f"{V[methods[0]][CASE_ENDS[0]]['general_public_services'][0]:.6f} as evaluated)")
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
    Q, qlab, _ = SL.bea_table(fa, "FAAt706-A")     # investment quantity index (perpetual inventory of transportation)
    SL.label_is(qlab, 65, "Transportation", "FAAt706")
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
                               (112, "Libraries and other"), (114, "Other"), (41, "Federal"), (54, "Highways"), (55, "Air"),
                               (56, "Water"), (57, "Transit and railroad"), (67, "Recreation and culture"),
                               (78, "State and local"), (89, "Transportation"), (90, "Highways"), (91, "Air"), (92, "Water"),
                               (93, "Transit and railroad"), (108, "Recreation and culture"))),
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

    # Which S&L activities are enterprises, and how far their charges cover their production costs.
    hf, hb = pdf_text(HIGHFILL), pdf_text(HANDBOOK9)
    t5_years, t5 = highfill_table5(HIGHFILL.with_suffix(".txt"))
    enterprise_list = ("The NIPAs currently classify as enterprises the following state and local government functions: water and "
                       "sewerage; gas and electricity; toll facilities; liquor stores; air and water terminals; housing and urban "
                       "renewal; public transit; lotteries;")
    gate("nipa_enterprises_and_their_capital", enterprise_list in hf
         and "Excludes gross output and sales of federal and of state and local government enterprises, which are recorded in the business sector." in hb
         and "Includes investment by federal and by state and local government enterprises." in hb,
         "BEA WP2022-8: toll facilities, air and water terminals, public transit, housing and local parking are S&L enterprises; "
         "NIPA Handbook ch. 9: consumption excludes enterprises, gross investment (so the fixed-asset stock) includes them")
    T5 = {"toll": "Toll highways", "air": "Air transportation", "ports": "Sea and inland port", "parking": "Parking facilities",
          "parks": "Parks and recreation", "regular_highways": "Regular highways", "transit": "Transit system utility",
          "housing": "Housing and community", "sewerage": "Sewerage", "water": "Water supply utility"}
    t5r = {k: t5.get(v) for k, v in T5.items()}
    t5_last = t5_years[-1]
    t5_range = lambda k: (min(v for v in t5r[k].values() if v is not None), max(v for v in t5r[k].values() if v is not None))
    fee_financed = ("toll", "air", "ports", "parking")
    gate("charges_over_production_costs_from_bea_table_5",
         "Table 5 shows the ratio of charges to production costs (operating expenditures plus CFC)" in hf and t5_last == 2017
         and len(t5_years) == 11 and all(t5r.values())
         and all(t5_range(k)[0] >= 1 for k in fee_financed) and all(t5r[k][t5_last] >= 1 for k in ("sewerage", "water"))
         and all(t5r[k][t5_last] < 0.5 for k in ("parks", "regular_highways", "transit", "housing")),
         "; ".join(f"{k} {t5r[k][t5_last]:.2f}" for k in T5) + f" ({t5_last}); toll, air, ports and parking >= 1 in every year "
         "reported, sewerage and water in the last")
    f_parks, f_hwy = (1 - t5r[k][t5_last] for k in ("parks", "regular_highways"))    # for the rejected netting only

    # Where the enterprises' operating results sit. Their value added is recorded with business, and their current
    # surplus is a component of national income, which is net of all consumption of fixed capital, government
    # enterprises' included (NIPA 1.7.5): the surplus is after their depreciation, with no imputed return.
    if sha(NIPA1) != NIPA1_SHA or NIPA1_SHA not in DEBT_SCRIPT.read_text():
        raise SystemExit(f"[BLOCKED] {NIPA1.relative_to(ROOT)} is not the vintage debt_legacy pins")
    t175, l175, _ = SL.bea_table(NIPA1, "T10705-A")
    t110, l110, _ = SL.bea_table(NIPA1, "T11000-A")
    t38, l38, _ = SL.bea_table(SL.NIPA3, "T30800-A")
    for tab, lab, checks in (
            ("T10705", l175, ((4, "Equals: Gross national product"), (5, "Less: Consumption of fixed capital"), (6, "Private"),
                              (11, "Government"), (12, "General government"), (13, "Government enterprises"),
                              (14, "Equals: Net national product"), (15, "Less: Statistical discrepancy"),
                              (16, "Equals: National income"), (22, "Current surplus of government enterprises"))),
            ("T11000", l110, ((1, "Gross domestic income"), (2, "Compensation of employees, paid"),
                              (7, "Taxes on production and imports"), (8, "Less: Subsidies"), (9, "Net operating surplus"),
                              (10, "Private enterprises"), (20, "Current surplus of government enterprises"),
                              (21, "Consumption of fixed capital"))),
            ("T30800", l38, ((1, "Current surplus of government enterprises"), (2, "Federal"), (7, "State and local"),
                             (8, "Water and sewerage"), (9, "Gas and electricity"), (10, "Toll facilities"), (11, "Liquor stores"),
                             (12, "Air and water terminals"), (13, "Housing and urban renewal"), (14, "Public transit"),
                             (15, "Other"))),
            ("T31005", l3105, ((5, "Consumption of general government fixed capital"),))):
        for line, text in checks:
            SL.label_is(lab, line, text, tab)
    a175, a110, a38 = ({ln: v[YEAR] for ln, v in t.items() if YEAR in v} for t in (t175, t110, t38))
    ok_175 = (abs(a175[5] - a175[6] - a175[11]) <= 1 and abs(a175[11] - a175[12] - a175[13]) <= 1
              and a175[12] == t3105[5][YEAR] and a175[13] > 0 and abs(a175[14] - (a175[4] - a175[5])) <= 1
              and abs(a175[16] - (a175[14] - a175[15])) <= 1)
    ok_110 = (abs(a110[9] - a110[10] - a110[20]) <= 1
              and abs(a110[1] - (a110[2] + a110[7] - a110[8] + a110[9] + a110[21])) <= 2)
    ok_38 = abs(a38[7] - sum(a38[k] for k in range(8, 16))) <= 1 and abs(a38[1] - a38[2] - a38[7]) <= 1
    ent_phrases = ("the difference between the value of output and the costs of production is equal to the net operating surplus",
                   "the value added by government enterprises (as producers of goods and services for the marketplace) is "
                   "recorded in the business sector")
    gate("enterprise_surplus_is_after_their_depreciation", ok_175 and ok_110 and ok_38
         and a175[22] == a110[20] == a38[1] and all(p in hb for p in ent_phrases),
         f"NIPA 1.7.5 ({YEAR}): consumption of fixed capital {bn(a175[5]):.1f} includes government enterprises' "
         f"{bn(a175[13]):.1f} (government {bn(a175[11]):.1f} less general government {bn(a175[12]):.1f}, which is "
         f"NIPA 3.10.5 l5); national income, net of it, holds the enterprises' current surplus {bn(a175[22]):.2f} (= NIPA "
         "1.10 l20 = 3.8 l1); NIPA 1.10: net operating surplus = private enterprises + that surplus, and GDI adds CFC beside "
         "it; Handbook ch. 9: enterprises' value added sits with business, where output less costs is net operating surplus")
    ent_rows = [per[m][i]["enterprise"] for m in methods for i in range(n)]
    ent_nat, ent_grp = ent_rows[0]["national_bn"], ent_rows[0]["amount_bn"]
    gate("enterprise_surplus_line_is_nipa_3_8_held_at_zero", all(
        e["response"] == 0 and e["key"] == "resident_population" and e["national_bn"] == ent_nat and e["amount_bn"] == ent_grp
        for e in ent_rows) and abs(ent_nat - bn(a38[1])) < 1e-9,
         f"the account's enterprise_surplus receipt ({ent_nat:.2f}bn nationally, NIPA 3.8 l1; {ent_grp:.3f}bn for the group at "
         f"the resident-population key) responds at 0 in all {len(ent_rows)} evaluations cost() makes (an indirect receipt), so "
         "no enterprise's operating result moves with the group")
    # The surplus is before interest: enterprises' interest sits with general government's, which is the account's
    # interest row. It includes subsidies received from other levels of government.
    mp5, hb2 = pdf_text(MP5), pdf_text(HANDBOOK2)
    INTEREST_PHRASES = {
        "mp5": ("In calculating the current surplus, expenses include consumption of fixed capital (CFC), but neither revenue nor "
                "expenses include interest.",
                "Interest received and paid are ignored in the calculation of the current surplus of government enterprises.",
                "(1) Their interest payments and receipts are presented with those of general government rather than those of "
                "business;",
                "The current surplus of government enterprises is equal to current operating revenues and subsidies received "
                "from other levels of government less current operating expenses."),
        "handbook2": ("before deducting any explicit or implicit interest charges, rent, or other property incomes payable on "
                      "financial assets, land, or other natural resources required to carry out production.",
                      "federal subsidies to state and local public housing authorities")}
    gate("enterprise_surplus_is_before_interest", all(p in mp5 for p in INTEREST_PHRASES["mp5"])
         and all(p in hb2 for p in INTEREST_PHRASES["handbook2"]) and "Updated: December 2024" in hb2,
         "BEA MP-5 (Government Transactions, 2005): expenses include CFC but neither revenue nor expenses include interest; "
         "enterprises' interest payments are presented with general government's; the surplus includes subsidies received "
         "from other levels of government. NIPA Handbook ch. 2 (December 2024): operating surplus is before any interest")

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
    # No netting of charges (the parent's call, 2026-09-27): the account's lines are consumption, gross output less
    # sales, so tuition and hospital sales are credited there already, and the return is missing in full. The college
    # part is higher education and libraries; museums and zoos (recreation) and preschool are not charged here.
    college_part = comp["higher"] + comp["library"]
    # [id, line (key and response), label, BEA lines, national stock, share charged, charged stock, depreciation 2024]
    COMP = [
        ["k12", "k12", "K-12 schools: educational structures x K-12 key plus K-12 equipment and software (school lane)",
         "FAAt701 l62 x key; l56+l73 x F-33 key", k12["avg2024"], 1.0, k12["avg2024"], k12["depreciation_2024"]],
        ["college", "college", "colleges and other education: non-K-12 educational structures; higher education and libraries "
                               "in full; museums and zoos (recreation) and preschool not charged",
         "FAAt701 l62 x (1 - key)", nonk12_stock, college_part, nonk12_stock * college_part, bn(D[62][YEAR]) * (1 - k12_key) * college_part],
        ["pos_sl", "public_order_safety", "public order and safety (state and local): public safety structures", "FAAt701 l63",
         avg(63), 1.0, avg(63), bn(D[63][YEAR])],
        ["pos_fed", "public_order_safety", "public order and safety (federal nondefense): public safety structures", "FAAt701 l45",
         avg(45), 1.0, avg(45), bn(D[45][YEAR])],
        ["health_sl", "health_services", "health (state and local): health care structures in full", "FAAt701 l61",
         avg(61), 1.0, avg(61), bn(D[61][YEAR])],
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
    # What the rejected netting would charge instead (reported once): tuition and hospital sales taken off again.
    netted_core = {"college": nonk12_stock * (comp["higher"] * f_tuition + comp["library"]), "health_sl": avg(61) * f_health}
    STRUCT = {"k12": k12["structures_avg2024"], "college": nonk12_stock * college_part}
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
    k12_pupil = lambda i, m, r: k12["avg2024"] * r * V[m][i]["k12_pupil_share"][0] * V[m][i]["k12_pupil_share"][1]
    gate("k12_reproduces_the_school_lane", all(abs(k12_pupil(i, m, r) - g_k12[lab]) < 1e-9 for lab, r in all_rates.items()
                                               for m in methods for i in range(n))
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
    EQ = [  # id, line, stock, share charged, share of the level's equipment and software
        ["eq_college_sl", "college", eq_sl_stock, 1.0, edu_share - k12_eq],
        ["eq_pos_sl", "public_order_safety", eq_sl_stock, 1.0, mshare("state_local", "public_order_safety")],
        ["eq_health_sl", "health_services", eq_sl_stock, 1.0, mshare("state_local", "health")],
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
    end_stock = {"k12": k12_end, "college": (1 - k12_key) * bn(K[62][YEAR]) * college_part, "pos_sl": bn(K[63][YEAR]),
                 "pos_fed": bn(K[45][YEAR]), "health_sl": bn(K[61][YEAR]), "health_fed": bn(K[43][YEAR]),
                 "gps_sl": bn(K[59][YEAR]), "gps_fed": bn(K[41][YEAR])}
    aux_stock = dict(charged, college=nonk12_stock * (comp["higher"] * (1 - aux) + comp["library"]))
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
        "k12_at_pupil_share": ("K-12 at the school lane's pupil share (a constant) instead of the account's own school key "
                               "from the evaluation", lambda i, m, r: sum(ret(
                                   charged, i, m, r, key_override={"k12": "k12_pupil_share"}).values())),
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
    for line_no, label, lid, note in (
            (60, "state and local commercial structures (parking and warehouses)", "general_public_services",
             "[GAP] no function; converted at the general-government key and response; its enterprise part (local parking, "
             "liquor stores) is inside BEA's enterprise total, which option D charges, so this conversion overstates the gap"),
            (71, "state and local other structures (lodging; communication; manufacturing)", "general_public_services",
             "[GAP] no function; converted at the general-government key and response"),
            (42, "federal nondefense commercial structures", "general_public_services",
             "[GAP] no function; converted at the general-government key and response; any Postal Service part is inside BEA's "
             "enterprise total, which option D charges"),
            (51, "federal nondefense other structures", "general_public_services",
             "[GAP] no function; converted at the general-government key and response")):
        gap(label, f"FAAt701 l{line_no}", avg(line_no), lid, 1.0, note)

    # ---------------- 8b. conditional block: roads, transit and parks at the long-run responses
    # The main case holds economic affairs and recreation at 0 (CBO's category lag). The sister lane lets
    # them respond. This block prices the return on the capital behind those lines at its responses and
    # reports it beside the core result, on the sister lane's candidate; neither is adopted.
    for p in (RESPONSES, LR_COSTS, LR_BAND, LR_NET):
        if not p.exists():
            raise SystemExit(f"[BLOCKED] missing {p.relative_to(ROOT)}: run service_response_long_run_2026_09_27 first")
    lr = json.loads(RESPONSES.read_text())
    lr_band = json.loads(LR_BAND.read_text())
    lr_net = json.loads(LR_NET.read_text())
    EA, RC = "economic_affairs_services", "recreation_culture"
    LR = lr["lines"]
    SF = {s["id"]: s for lid in (EA, RC) for s in LR[lid]["subfunctions"]}

    def across(s: dict) -> float:
        """The sister lane's across-state reading at the high end (its sensitivity across_states_at_high_end)."""
        if s["id"] in ("sl_highways", "sl_recreation_and_culture", "sl_transit_and_railroad"):
            return s["response"]["low"]
        if s["level"] == "federal" and s["response"]["high"] == 1:
            return SF["sl_recreation_and_culture" if "recreation" in s["id"] else "sl_highways"]["response"]["low"]
        return s["response"]["high"]

    SCEN = {"low": lambda s: s["response"]["low"], "high": lambda s: s["response"]["high"], "across_high": across,
            "unit": lambda s: 1.0}
    blend = lambda lid, sc: sum(s["share_of_line"] * SCEN[sc](s) for s in LR[lid]["subfunctions"])
    gate("long_run_responses_are_the_sister_lanes",
         LR[EA]["key"] == "resources" and LR[RC]["key"] == "population" and lr["meta"]["band_ends"] == ["low", "high"]
         and all(abs(LR[l]["national_bn"] - lines_by_id[l]["national_bn"]) < 1e-9 and LR[l]["main_case_response"] == 0
                 and abs(sum(s["share_of_line"] for s in LR[l]["subfunctions"]) - 1) < 1e-9
                 and all(abs(blend(l, w) - LR[l]["response"][w]) < 1e-12 for w in ("low", "high")) for l in (EA, RC))
         and all(0 <= s["response"][w] <= 1 for s in SF.values() for w in ("low", "high")),
         f"economic affairs (resources key) {LR[EA]['response']['low']:.4f}/{LR[EA]['response']['high']:.4f} and recreation "
         f"(population key) {LR[RC]['response']['low']:.4f}/{LR[RC]['response']['high']:.4f} are the amount-weighted blends of "
         "the subfunction responses; both lines at 0 in the main case")
    BVIEW = {"ea": "economic_affairs_per_unit_response", "rc": "recreation_per_unit_response"}
    amt = {lid: {m: [V[m][i][BVIEW[vw]][0] * lines_by_id[lid]["national_bn"] for i in range(n)] for m in methods}
           for lid, vw in ((EA, "ea"), (RC, "rc"))}
    # The long-run costs on the linear path: the case's cost plus each line's keyed amount times its blended response.
    lin = {sc: {m: [costs[m][i] + sum(amt[lid][m][i] * blend(lid, sc) for lid in (EA, RC)) for i in range(n)] for m in methods}
           for sc in ("low", "high", "across_high")}
    lr_rows = {(r["method"], int(r["spec"])): r for r in csv.DictReader(LR_COSTS.open())}
    lr_err = max(max(abs(float(lr_rows[(m, i)]["cost_main_case_bn"]) - costs[m][i]),
                     abs(float(lr_rows[(m, i)]["cost_low_bn"]) - lin["low"][m][i]),
                     abs(float(lr_rows[(m, i)]["cost_high_bn"]) - lin["high"][m][i]),
                     abs(float(lr_rows[(m, i)]["move_low_bn"]) - (lin["low"][m][i] - costs[m][i])),
                     abs(float(lr_rows[(m, i)]["move_high_bn"]) - (lin["high"][m][i] - costs[m][i])),
                     abs(float(lr_rows[(m, i)]["group_economic_affairs_bn"]) - amt[EA][m][i]),
                     abs(float(lr_rows[(m, i)]["group_recreation_bn"]) - amt[RC][m][i]))
                 for m in methods for i in range(n)) if set(lr_rows) == {(m, i) for m in methods for i in range(n)} else float("inf")
    gate("long_run_per_spec_costs_reproduce", lr_err < 1e-6,
         f"the sister lane's {len(lr_rows)} per-spec costs and moves = the case's cost + the keyed amounts of this evaluation x "
         f"the blended responses (max |diff| {lr_err:.1e})")
    lr_lo, lr_hi, lr_ax = band_of(lin["low"]), band_of(lin["high"]), band_of(lin["across_high"])
    lr_amt_end = lr_band["group_amounts_at_end_specifications_bn"]
    gate("long_run_candidate_band_reproduces", abs(lr_lo["low"] - lr_band["candidate"]["band_bn"][0]) < 1e-6
         and abs(lr_hi["high"] - lr_band["candidate"]["band_bn"][1]) < 1e-6
         and all(x == CASE_ENDS[0] for x in lr_lo["low_spec"]) and all(x == CASE_ENDS[1] for x in lr_hi["high_spec"])
         and all(abs(at(amt[lid], CASE_ENDS[j]) - lr_amt_end[w][lid]) < 1e-9 for lid in (EA, RC) for j, w in enumerate(("low", "high"))),
         f"{lr_lo['low']:.4f}-{lr_hi['high']:.4f} at specs {CASE_ENDS[0]}/{CASE_ENDS[1]}; keyed amounts at the ends "
         f"{lr_amt_end['low'][EA]:.4f} (economic affairs) and {lr_amt_end['low'][RC]:.4f} (recreation)")
    # The response lane's across-state reading at both ends: its candidate's high end plus its sensitivity
    # across_states_at_high_end (the low end already takes the across-state readings).
    ax_ref = lr_band["candidate"]["band_bn"][1] + lr_band["sensitivities_at_end_specifications"]["across_states_at_high_end"]["delta_bn"][1]
    gate("long_run_across_state_band_reproduces", abs(lr_ax["high"] - ax_ref) < 1e-6
         and all(x == CASE_ENDS[1] for x in lr_ax["high_spec"]) and lr_band["sensitivities_at_end_specifications"][
             "across_states_at_high_end"]["delta_bn"][0] == 0,
         f"{lr_lo['low']:.4f}-{lr_ax['high']:.4f} (the response lane's candidate {lr_band['candidate']['band_bn'][1]:.4f} + its "
         f"across-state sensitivity {ax_ref - lr_band['candidate']['band_bn'][1]:+.4f} at the high end)")
    lr_move_end = {w: at(move_w, CASE_ENDS[j]) for j, (w, move_w) in enumerate(
        (("low", {m: [lin["low"][m][i] - costs[m][i] for i in range(n)] for m in methods}),
         ("high", {m: [lin["high"][m][i] - costs[m][i] for i in range(n)] for m in methods})))}
    gate("congestion_change_kept_beside_the_fiscal_case",
         all(abs(lr_net["by_band_end"][w]["account_move_bn"] - lr_move_end[w]) < 1e-9 for w in ("low", "high")),
         f"net_change.json's account moves {lr_net['by_band_end']['low']['account_move_bn']:.4f}/"
         f"{lr_net['by_band_end']['high']['account_move_bn']:.4f} are this lane's long-run moves at specs "
         f"{CASE_ENDS[0]}/{CASE_ENDS[1]}; its congestion change {lr_net['by_band_end']['low']['congestion_change_bn']:+.2f}/"
         f"{lr_net['by_band_end']['high']['congestion_change_bn']:+.2f} is a social item and stays out of the bands")

    cog = cog_national()
    if json.loads(COG_PINS.read_text()).get(str(COG_API.relative_to(FISCAL))) != sha(COG_API):
        raise SystemExit("[BLOCKED] the Census API anchor file does not match its pin")
    api = {r[0]: float(r[6]) for r in json.loads(COG_API.read_text())[1:]}
    ANCH = {"LF0142": ("E44", "E45"), "LF0143": ("F44", "F45"), "LF0048": ("A44", "A45"), "LF0145": ("E01",), "LF0146": ("F01",),
            "LF0049": ("A01",), "LF0148": ("E60",), "LF0149": ("F60",), "LF0050": ("A60",), "LF0151": ("E87",), "LF0152": ("F87",),
            "LF0051": ("A87",), "LF0169": ("E61",), "LF0170": ("F61",), "LF0053": ("A61",), "LF0216": ("E94",), "LF0217": ("F94",),
            "LF0073": ("A94",)}
    gate("census_finance_files_reproduce_the_api_anchors", all(sum(cog[2022][c] for c in cs) == api[f] for f, cs in ANCH.items()),
         f"{len(ANCH)} FY2022 national fields: charges, current operation and capital outlay for highways, airports, parking, ports, "
         "parks and transit")
    ctot = lambda c: sum(cog[y][c] for y in COG_YEARS)
    toll_y = {y: cog[y]["F45"] / (cog[y]["F44"] + cog[y]["F45"]) for y in COG_YEARS}
    toll = ctot("F45") / (ctot("F44") + ctot("F45"))
    gate("toll_share_from_census_construction", 0 < min(toll_y.values()) <= toll <= max(toll_y.values()) < 0.25,
         f"toll highways' share of S&L highway construction {toll:.4f}, pooled over FY{COG_YEARS[0]} and FY{COG_YEARS[1]}-"
         f"{COG_YEARS[-1]} (single years {min(toll_y.values()):.4f}-{max(toll_y.values()):.4f})")

    # BEA's structure types against the functions' own gross investment (NIPA 3.15.5 less the sister lane's consumption).
    GI = {"S&L highways": (t3155[90][YEAR] - 1000 * SF["sl_highways"]["national_bn"], (67,)),
          "S&L air, water and transit": (t3155[91][YEAR] + t3155[92][YEAR] + t3155[93][YEAR]
                                         - 1000 * SF["sl_transit_and_railroad"]["national_bn"], (65,)),
          "S&L recreation": (t3155[108][YEAR] - 1000 * SF["sl_recreation_and_culture"]["national_bn"], (64,)),
          "federal highways": (t3155[54][YEAR] - 1000 * SF["fed_highways"]["national_bn"], (49,)),
          "federal air, water and transit": (t3155[55][YEAR] + t3155[56][YEAR] + t3155[57][YEAR] - 1000 * sum(
              SF[x]["national_bn"] for x in ("fed_air", "fed_water", "fed_transit_and_railroad")), (47,)),
          "federal recreation": (t3155[67][YEAR] - 1000 * SF["fed_recreation_and_culture"]["national_bn"], (46,))}
    gi_ratio = {k: sum(INV[l][YEAR] for l in ls) / v for k, (v, ls) in GI.items()}
    HS, TP = "Nonresidential/Highway and Street", "Nonresidential/Transportation"
    vip_bea = {nm: [vip[p][y] / INV[l][y] for y in range(SL.VINTAGE_SPLIT, YEAR + 1)] for nm, p, l in (("highways", HS, 67), ("transportation", TP, 65))}
    gate("highway_and_transport_types_are_their_functions_capital",
         all(0 < r <= 1 for r in gi_ratio.values()) and gi_ratio["S&L highways"] >= 0.9
         and all(0.8 <= min(v) and max(v) <= 1.2 for v in vip_bea.values()) and bn(D[67][YEAR]) * (1 - toll) < SF["sl_highways"]["national_bn"],
         "structure investment / function gross investment 2024: " + ", ".join(f"{k} {v:.3f}" for k, v in gi_ratio.items())
         + f"; VIP / BEA 1993-2024: highways {min(vip_bea['highways']):.3f}-{max(vip_bea['highways']):.3f}, transportation "
         f"{min(vip_bea['transportation']):.3f}-{max(vip_bea['transportation']):.3f}; nontoll highway depreciation "
         f"{bn(D[67][YEAR]) * (1 - toll):.1f} sits inside S&L highway consumption {SF['sl_highways']['national_bn']:.1f}")

    # S&L Transportation (airports, ports, transit) split by Census VIP mode, weighted by a perpetual inventory of l65.
    d65 = bn(D[65][YEAR]) / avg(65)
    p65 = INV[65][YEAR] / Q[65][YEAR]
    yrs65 = sorted(y for y in Q[65] if y <= YEAR)
    w65raw = {t: p65 * Q[65][t] * (1 - d65) ** (YEAR - t) * (1 - d65 / 2) for t in yrs65}
    pim65 = sum(w65raw.values())
    w65 = {t: v / pim65 for t, v in w65raw.items()}
    pre65 = sum(v for t, v in w65.items() if t < SL.VINTAGE_SPLIT)
    MODES = ("Air", "Land", "Water")
    msh = {md: {y: vip[f"{TP}/{md}"][y] / vip[TP][y] for y in range(SL.VINTAGE_SPLIT, YEAR + 1)} for md in MODES}
    mpost = {md: sum(w65[t] * msh[md][t] for t in yrs65 if t >= SL.VINTAGE_SPLIT) for md in MODES}
    mode = {md: {"central": mpost[md] + pre65 * msh[md][SL.VINTAGE_SPLIT], "low": mpost[md] + pre65 * min(msh[md].values()),
                 "high": mpost[md] + pre65 * max(msh[md].values())} for md in MODES}
    cog_transit = {y: cog[y]["F94"] / (cog[y]["F01"] + cog[y]["F87"] + cog[y]["F94"]) for y in COG_YEARS}
    gate("transport_split_by_vip_vintages", abs(pim65 / K[65][YEAR] - 1) < SL.PIM_TOL
         and all(abs(sum(vip[f"{TP}/{md}"][y] for md in MODES) - vip[TP][y]) <= 1.0 for y in range(SL.VINTAGE_SPLIT, YEAR + 1))
         and abs(sum(mode[md]["central"] for md in MODES) - 1) < 1e-3,
         f"perpetual inventory {bn(pim65):.1f} vs BEA {bn(K[65][YEAR]):.1f} (delta {d65:.4f}); pre-{SL.VINTAGE_SPLIT} vintages "
         f"{pre65:.3f} of the stock at the {SL.VINTAGE_SPLIT} mix; land (transit) {mode['Land']['central']:.4f} "
         f"({mode['Land']['low']:.4f}-{mode['Land']['high']:.4f}), air {mode['Air']['central']:.4f}, water {mode['Water']['central']:.4f}; "
         f"Census construction puts transit at {min(cog_transit.values()):.3f}-{max(cog_transit.values()):.3f}")

    museums = nonk12_stock * comp["museum_zoo"]
    # [id, subfunction, key view, label, BEA source, national stock, share charged, fee factor, depreciation 2024 of the stock]
    # No netting (the parent's call): highway and parks charges are credited in the account's lines already. Toll
    # facilities, transit, airports and ports are enterprises and sit in the enterprise block (option D).
    BLK = [
        ["hwy_sl", "sl_highways", "ea", "state and local highways and streets less toll facilities, in full",
         "FAAt701 l67 x (1 - toll share)", avg(67), 1 - toll, 1.0, bn(D[67][YEAR])],
        ["rec_sl", "sl_recreation_and_culture", "rc", "state and local parks and recreation structures plus museums and zoos, in "
         "full", "FAAt701 l64; l62 x (1 - key) x museum share", avg(64) + museums, 1.0, 1.0,
         bn(D[64][YEAR]) + bn(D[62][YEAR]) * (1 - k12_key) * comp["museum_zoo"]],
        ["hwy_fed", "fed_highways", "ea", "federal highways and streets (roads on federal land)", "FAAt701 l49", avg(49), 1.0, 1.0,
         bn(D[49][YEAR])],
        ["air_fed", "fed_air", "ea", "federal transportation structures (air traffic facilities)", "FAAt701 l47", avg(47), 1.0, 1.0,
         bn(D[47][YEAR])],
        ["rec_fed", "fed_recreation_and_culture", "rc", "federal amusement and recreation structures (national parks)", "FAAt701 l46",
         avg(46), 1.0, 1.0, bn(D[46][YEAR])],
    ]
    bcharged = {b[0]: b[5] * b[6] * b[7] for b in BLK}
    netted_block = {"hwy_sl": bcharged["hwy_sl"] * f_hwy, "rec_sl": bcharged["rec_sl"] * f_parks}   # the rejected netting
    # Equipment and software behind each component (the core's derived-split method): its subfunction's 2024 gross
    # investment less the structures above, as a share of all equipment and software investment at that level.
    gi_sub = {"hwy_sl": GI["S&L highways"][0] - INV[67][YEAR],
              "rec_sl": GI["S&L recreation"][0] - INV[64][YEAR],
              "hwy_fed": GI["federal highways"][0] - INV[49][YEAR],
              "air_fed": t3155[55][YEAR] - 1000 * SF["fed_air"]["national_bn"] - INV[47][YEAR],
              "rec_fed": GI["federal recreation"][0] - INV[46][YEAR]}
    eq_inv = {"sl": INV[56][YEAR] + INV[73][YEAR], "fed": INV[39][YEAR] + INV[53][YEAR]}
    beq_share = {c: v / eq_inv[c.split("_")[1]] for c, v in gi_sub.items()}
    beq_stock = {c: (eq_sl_stock if c.endswith("_sl") else eq_fed_stock) * beq_share[c] for c in gi_sub}
    beq_fee = {b[0]: b[7] * ((1 - toll) if b[0] == "hwy_sl" else 1.0) for b in BLK}   # the structures' type split is not reapplied
    gate("block_equipment_residuals_are_shares", all(0 <= v < 0.3 for v in beq_share.values()),
         "subfunction gross investment less its structures over equipment and software investment, 2024: "
         + ", ".join(f"{c} {v:.4f}" for c, v in beq_share.items()))

    def bret(stocks: dict, i: int, m: str, r: float, sc: str, comps: list = BLK) -> dict:
        v = V[m][i]
        return {b[0]: stocks[b[0]] * r * v[BVIEW[b[2]]][0] * SCEN[sc](SF[b[1]]) for b in comps}

    def bseries(stocks: dict, lab: str, sc: str, comps: list = BLK) -> dict:
        return {m: [sum(bret(stocks, i, m, all_rates[lab], sc, comps).values()) for i in range(n)] for m in methods}

    BSC = ("low", "high", "across_high", "unit")
    BR = {(lab, sc): {m: [bret(bcharged, i, m, r, sc) for i in range(n)] for m in methods} for lab, r in all_rates.items() for sc in BSC}
    btot = {k: {m: [sum(x.values()) for x in v[m]] for m in methods} for k, v in BR.items()}
    # ---------------- 8c. government enterprises: option D (all respond) or option A (enterprises out)
    # BEA publishes government enterprises' fixed assets only as a total over levels and types (FAAt701 l79-82). The listed
    # types are the enterprises on BEA's list. The total's remainder (equipment, software, structures of other types, net
    # of the parts of the listed types that BEA counts as general government) is split by level in proportion to the
    # enterprises' depreciation that the listed types do not cover (NIPA 7.5). Every piece takes the same key and
    # response, so the split changes the breakdown by type, not the total.
    for line, text in ((79, "Government enterprise fixed assets"), (80, "Equipment"), (81, "Structures"),
                       (82, "Intellectual property products"), (58, "Residential"), (65, "Transportation"), (66, "Power"),
                       (67, "Highways and streets"), (68, "Sewer systems"), (69, "Water systems"), (48, "Power")):
        SL.label_is(klab, line, text, "FAAt701")
        SL.label_is(dlab, line, text, "FAAt703")
    t75, l75, _ = SL.bea_table(SL.CACHE / "nipa_Section7All_xls.xlsx", "T70500-A")
    for line, text in ((21, "Government"), (22, "General government"), (25, "Government enterprises"), (26, "Federal"),
                       (27, "State and local")):
        SL.label_is(l75, line, text, "T70500")
    ent_cfc = {"all": bn(t75[25][YEAR]), "federal": bn(t75[26][YEAR]), "state_local": bn(t75[27][YEAR])}
    ent_total, ent_dep_fa = avg(79), bn(D[79][YEAR])
    lsh = {md: mode[md]["central"] for md in MODES}
    # [id, level, label, BEA source, stock (2024 average), depreciation 2024]
    ENT = [
        ["ent_housing_sl", "state_local", "public housing (S&L residential structures)", "FAAt701 l58", avg(58), bn(D[58][YEAR])],
        ["ent_transit_sl", "state_local", "public transit (land share of S&L transportation)", "FAAt701 l65 x VIP land share",
         avg(65) * lsh["Land"], bn(D[65][YEAR]) * lsh["Land"]],
        ["ent_airports_sl", "state_local", "airports (air share of S&L transportation)", "FAAt701 l65 x VIP air share",
         avg(65) * lsh["Air"], bn(D[65][YEAR]) * lsh["Air"]],
        ["ent_ports_sl", "state_local", "ports (water share of S&L transportation)", "FAAt701 l65 x VIP water share",
         avg(65) * lsh["Water"], bn(D[65][YEAR]) * lsh["Water"]],
        ["ent_power_sl", "state_local", "electric and gas utilities (S&L power structures)", "FAAt701 l66", avg(66), bn(D[66][YEAR])],
        ["ent_water_sl", "state_local", "water systems", "FAAt701 l69", avg(69), bn(D[69][YEAR])],
        ["ent_sewer_sl", "state_local", "sewer systems", "FAAt701 l68", avg(68), bn(D[68][YEAR])],
        ["ent_tolls_sl", "state_local", "toll facilities (toll share of S&L highways)", "FAAt701 l67 x toll share",
         avg(67) * toll, bn(D[67][YEAR]) * toll],
        ["ent_power_fed", "federal", "federal power (TVA and the power marketing administrations)", "FAAt701 l48", avg(48),
         bn(D[48][YEAR])],
    ]
    listed = sum(e[4] for e in ENT)
    scale_cfc = ent_dep_fa / ent_cfc["all"]                      # NIPA 7.5's levels, expressed in the FA vintage
    resid_dep = {lv: ent_cfc[lv] * scale_cfc - sum(e[5] for e in ENT if e[1] == lv) for lv in ("state_local", "federal")}
    resid_stock = ent_total - listed
    for lv, tag, who in (("state_local", "sl", "S&L"), ("federal", "fed", "federal")):
        ENT.append([f"ent_other_{tag}", lv, f"other {who} enterprise capital: equipment, software and structures of other types "
                    "(Postal Service, parking, liquor stores, lotteries), net of the listed types' general-government parts",
                    f"FAAt701 l79 less the listed types; {who} share by NIPA 7.5", resid_stock * resid_dep[lv] / sum(resid_dep.values()),
                    resid_dep[lv]])
    ent_stock = {e[0]: e[4] for e in ENT}
    overlap = listed - avg(81)
    gate("enterprise_capital_is_beas_enterprise_total",
         abs(avg(79) - avg(80) - avg(81) - avg(82)) < 0.01 and abs(ent_cfc["all"] - ent_cfc["federal"] - ent_cfc["state_local"]) < 0.002
         and abs(bn(t75[21][YEAR]) - bn(t75[22][YEAR]) - ent_cfc["all"]) < 0.002 and abs(ent_cfc["all"] - bn(a175[13])) < 0.002
         and abs(scale_cfc - 1) < 0.01 and resid_stock > 0 and all(v > 0 for v in resid_dep.values())
         and abs(sum(ent_stock.values()) - ent_total) < 1e-9,
         f"BEA's government enterprise fixed assets {ent_total:.1f} (equipment {avg(80):.1f}, structures {avg(81):.1f}, IPP "
         f"{avg(82):.1f}; 2024 average); depreciation {ent_dep_fa:.2f} vs NIPA 7.5 enterprise CFC {ent_cfc['all']:.3f} (federal "
         f"{ent_cfc['federal']:.3f}, S&L {ent_cfc['state_local']:.3f}; = NIPA 1.7.5 l13); the listed types {listed:.1f} exceed "
         f"enterprise structures by {overlap:.1f}; remainder {resid_stock:.1f}, split S&L {ent_stock['ent_other_sl']:.1f} / federal "
         f"{ent_stock['ent_other_fed']:.1f} by uncovered depreciation {resid_dep['state_local']:.2f} / {resid_dep['federal']:.2f}")

    def eret(stocks: dict, i: int, m: str, r: float) -> dict:
        """Option D: every enterprise's capital at the enterprise-surplus line's key, response 1."""
        return {c: s * r * V[m][i]["enterprise"][0] * V[m][i]["enterprise"][1] for c, s in stocks.items()}

    ER = {lab: {m: [eret(ent_stock, i, m, r) for i in range(n)] for m in methods} for lab, r in all_rates.items()}
    etot = {lab: {m: [sum(x.values()) for x in ER[lab][m]] for m in methods} for lab in all_rates}
    # Option D's receipt: at response 1 the group's share of every enterprise's current surplus leaves with it. The
    # surplus is a deficit (-$47.46bn), so losing the share lowers receipts less than it saves: the cost rises.
    esur = {m: [-per[m][i]["enterprise"]["amount_bn"] for i in range(n)] for m in methods}
    # NIPA 3.8's surplus by type against the return its capital would need (national, $bn).
    SURPLUS_GROUPS = {   # name: (NIPA 3.8 lines, components, charges exceed production costs)
        "water and sewerage": ((8,), ("ent_water_sl", "ent_sewer_sl"), True),
        "gas and electricity": ((9,), ("ent_power_sl",), True),
        "toll facilities": ((10,), ("ent_tolls_sl",), True),
        "air and water terminals": ((12,), ("ent_airports_sl", "ent_ports_sl"), True),
        "housing and urban renewal": ((13,), ("ent_housing_sl",), False),
        "public transit": ((14,), ("ent_transit_sl",), False),
        "liquor stores and other (lotteries, parking)": ((11, 15), ("ent_other_sl",), True),
        "federal (Postal Service, power)": ((2,), ("ent_power_fed", "ent_other_fed"), False)}
    surplus_rows = [[g, "+".join(f"l{x}" for x in ls), sum(bn(a38[x]) for x in ls), "+".join(cs), sum(ent_stock[c] for c in cs), ff]
                    + [sum(ent_stock[c] for c in cs) * r for r in all_rates.values()]
                    + [at({m: [sum(ER[lab][m][i][c] for c in cs) for i in range(n)] for m in methods}, CASE_ENDS[j])
                       for lab, j in (("2pct", 0), ("3pct", 1))]
                    for g, (ls, cs, ff) in SURPLUS_GROUPS.items()]
    # Option D by group: the group's share of that surplus leaves with it (the move), beside the return on its capital.
    for r in surplus_rows:
        mv = [at({m: [-r[2] * V[m][i]["enterprise"][0] for i in range(n)] for m in methods}, i) for i in CASE_ENDS]
        r += mv + [r[9] + mv[0], r[10] + mv[1]]
    gate("enterprise_surplus_groups_cover_nipa_3_8_and_the_components",
         abs(sum(r[2] for r in surplus_rows) - bn(a38[1])) < 1e-9
         and sorted(c for _, cs, _ in SURPLUS_GROUPS.values() for c in cs) == sorted(ent_stock)
         and all(abs(sum(r[11 + j] for r in surplus_rows) - at(esur, i)) < 1e-9 for j, i in enumerate(CASE_ENDS))
         and all(abs(sum(r[13 + j] for r in surplus_rows) - at(esur, i) - at(etot[lab], i)) < 1e-9
                 for j, (lab, i) in enumerate(zip(("2pct", "3pct"), CASE_ENDS))),
         f"the groups' surpluses add to NIPA 3.8 l1 ({bn(a38[1]):.2f}) and their components to the enterprise total; their "
         f"moves add to the receipt's ({at(esur, CASE_ENDS[0]):.4f}) and their nets to option D's pieces at specs "
         f"{CASE_ENDS[0]} / {CASE_ENDS[1]}")

    zero = {m: [0.0] * n for m in methods}
    move = {sc: {m: [lin[sc][m][i] - costs[m][i] for i in range(n)] for m in methods} for sc in lin}

    def add(*parts: dict) -> dict:
        return {m: [sum(p[m][i] for p in parts) for i in range(n)] for m in methods}

    def comb_row(name: str, rates: str, lo: tuple, hi: tuple, note: str) -> list:
        """lo and hi: (long-run scenario, core, block, enterprise surplus move, enterprise returns) for each end; None is 0."""
        lo, hi = (tuple(lo) + (None,) * 4)[:5], (tuple(hi) + (None,) * 4)[:5]
        b_lo = band_of(add(lin[lo[0]], *(x or zero for x in lo[1:])))
        b_hi = band_of(add(lin[hi[0]], *(x or zero for x in hi[1:])))
        out = [name, rates, b_lo["low"], b_hi["high"], "/".join(map(str, b_lo["low_spec"])), "/".join(map(str, b_hi["high_spec"]))]
        for b, key, (sc, *parts) in ((b_lo, "low_spec", lo), (b_hi, "high_spec", hi)):
            i = b[key][0] if len(set(b[key])) == 1 else None
            out += [None] * 5 if i is None else [at(move[sc], i)] + [at(p, i) if p else 0.0 for p in parts]
        return out + [note]

    B = lambda lab, sc: btot[(lab, sc)]
    OPT = {"D": lambda lab: (esur, etot[lab]), "A": lambda lab: (None, None)}
    OPT_NOTE = {"D": "option D, all enterprises respond: the enterprise-surplus receipt at response 1 at its own key (resident "
                     "population), and the full return on all government-enterprise capital (BEA's total) at that key and response 1",
                "A": "option A, enterprises out: no enterprise capital, and the enterprise-surplus line held at 0"}
    comb_rows = [
        comb_row("long-run responses only (the sister lane's candidate)", "", ("low",), ("high",),
                 "service_response_long_run_2026_09_27: low responses at the low end, high at the high end"),
        comb_row("long-run responses + core return", "2pct/3pct", ("low", total["2pct"]), ("high", total["3pct"]),
                 "the core return in full (no netting); roads and parks capital and enterprises not priced"),
    ]
    for o in ("D", "A"):
        comb_rows.append(comb_row(f"option {o}: long-run responses + core + block" + (" + enterprises" if o == "D" else ""),
                                  "2pct/3pct", ("low", total["2pct"], B("2pct", "low"), *OPT[o]("2pct")),
                                  ("high", total["3pct"], B("3pct", "high"), *OPT[o]("3pct")),
                                  OPT_NOTE[o] + "; 2% and the low responses at the low end, 3% and the high responses at the "
                                  "high end; no netting of charges"))
    for o in ("D", "A"):
        for lab in all_rates:
            comb_rows.append(comb_row(f"option {o} at one rate", lab, ("low", total[lab], B(lab, "low"), *OPT[o](lab)),
                                      ("high", total[lab], B(lab, "high"), *OPT[o](lab)),
                                      "reported only" if lab in REPORTED else "one rate at both ends"))
        comb_rows += [
            comb_row(f"option {o}, across-state readings at both ends (the response lane's variant)", "2pct/3pct",
                     ("low", total["2pct"], B("2pct", "low"), *OPT[o]("2pct")),
                     ("across_high", total["3pct"], B("3pct", "across_high"), *OPT[o]("3pct")),
                     "S&L highways and parks at their across-state readings at both ends; federal lines fixed at the low end and "
                     "at the across-state readings at the high end, as general government's federal part"),
            comb_row(f"option {o}, low responses throughout", "2pct/3pct", ("low", total["2pct"], B("2pct", "low"), *OPT[o]("2pct")),
                     ("low", total["3pct"], B("3pct", "low"), *OPT[o]("3pct")),
                     "federal lines fixed and S&L lines at the across-state readings at both ends"),
            comb_row(f"option {o}, high responses throughout", "2pct/3pct", ("high", total["2pct"], B("2pct", "high"), *OPT[o]("2pct")),
                     ("high", total["3pct"], B("3pct", "high"), *OPT[o]("3pct")),
                     "within-state readings capped at 1 and federal lines at 1 at both ends")]
    BVAR = {
        "toll share at its lowest year": (dict(bcharged, hwy_sl=avg(67) * (1 - min(toll_y.values()))),
                                          f"toll share {min(toll_y.values()):.4f} instead of {toll:.4f}"),
        "toll share at its highest year": (dict(bcharged, hwy_sl=avg(67) * (1 - max(toll_y.values()))),
                                           f"toll share {max(toll_y.values()):.4f} instead of {toll:.4f}"),
        "equipment and software added": ({c: bcharged[c] + beq_stock[c] * beq_fee[c] for c in bcharged},
                                         "each component's equipment and software by the derived split (federal includes R&D)"),
    }
    for o in ("D", "A"):
        for name, (stocks, note) in BVAR.items():
            comb_rows.append(comb_row(f"option {o}, block variant: {name}", "2pct/3pct",
                                      ("low", total["2pct"], bseries(stocks, "2pct", "low"), *OPT[o]("2pct")),
                                      ("high", total["3pct"], bseries(stocks, "3pct", "high"), *OPT[o]("3pct")),
                                      note + ("; the enterprise block keeps BEA's enterprise total" if o == "D" else "")))

    def etot_housing(view_id: str, lab: str) -> dict:
        """Option D's enterprise returns with public housing at another key (response 1)."""
        r = all_rates[lab]
        return {m: [etot[lab][m][i] - ER[lab][m][i]["ent_housing_sl"] + ent_stock["ent_housing_sl"] * r * V[m][i][view_id][0]
                    for i in range(n)] for m in methods}

    EVAR = {"public housing at the rental-assistance key": "housing_subsidies_at_response_1",
            "public housing at model.json's rental key": "housing_support_uncorrected"}
    EVAR_NOTE = {"housing_subsidies_at_response_1": "housing_subsidies' housing_support as the case evaluates it",
                 "housing_support_uncorrected": f"model.json's housing_support ({hs_base:.4f}), before the case's corrections"}
    for name, vw in EVAR.items():
        comb_rows.append(comb_row(f"option D, enterprise variant: {name}", "2pct/3pct",
                                  ("low", total["2pct"], B("2pct", "low"), esur, etot_housing(vw, "2pct")),
                                  ("high", total["3pct"], B("3pct", "high"), esur, etot_housing(vw, "3pct")),
                                  f"public housing's capital keyed like rental assistance ({EVAR_NOTE[vw]}) at response 1 instead "
                                  "of the enterprise-surplus key"))
    # The receipt keeps model.json's resident-population share: the case's corrections re-key the population-keyed spending
    # lines (the CPS lane's stack) but no receipt. Option D with the receipt and the capital at the spending lines' key.
    pop_scale = {m: [V[m][i]["general_public_services"][0] / V[m][i]["enterprise"][0] for i in range(n)] for m in methods}
    at_pop = lambda s: {m: [s[m][i] * pop_scale[m][i] for i in range(n)] for m in methods}
    comb_rows.append(comb_row("option D, enterprises at the spending lines' population key", "2pct/3pct",
                              ("low", total["2pct"], B("2pct", "low"), at_pop(esur), at_pop(etot["2pct"])),
                              ("high", total["3pct"], B("3pct", "high"), at_pop(esur), at_pop(etot["3pct"])),
                              "the enterprise_surplus receipt and all enterprise capital at general_public_services' population key "
                              "as evaluated, instead of the receipt's resident_population share, which the case's corrections leave "
                              "at model.json's"))
    cand_d, cand_a = comb_rows[2], comb_rows[3]
    off_ends = [r[0] for r in comb_rows if r[4] != f"{CASE_ENDS[0]}/{CASE_ENDS[0]}" or r[5] != f"{CASE_ENDS[1]}/{CASE_ENDS[1]}"]
    gate("combined_candidate_keeps_the_case_specifications", not off_ends and cand_d[2] < cand_d[3] and cand_a[2] < cand_a[3]
         and cand_a[2] < cand_d[2] and cand_a[3] < cand_d[3],
         f"option D {cand_d[2]:.4f}-{cand_d[3]:.4f}, option A {cand_a[2]:.4f}-{cand_a[3]:.4f}, at specs {cand_d[4]} / {cand_d[5]}; "
         f"every combined row keeps ends {CASE_ENDS[0]} / {CASE_ENDS[1]} in both methods" + (f" except {off_ends}" if off_ends else ""))

    # Gaps of the block, converted at the low responses at spec 48 and the high responses at spec 11.
    def gap_b(item: str, basis: str, stock: float, vw: str, sfid: str, fee: float, note: str) -> None:
        gap_rows.append([item, basis, stock, fee, f"{BVIEW[vw]} x {sfid}"]
                        + [sum(stock * fee * r * V[m][i][BVIEW[vw]][0] * SCEN["low" if i == CASE_ENDS[0] else "high"](SF[sfid])
                               for m in methods) / len(methods) for r in RATES.values() for i in CASE_ENDS] + [note])

    for b in BLK:
        gap_b(f"block: land at 10% of the structures charged: {b[0]}", b[4], 0.10 * bcharged[b[0]], b[2], b[1], 1.0,
              "[GAP] BEA and the Fed's accounts exclude government land; right-of-way under roads; low responses at spec "
              f"{CASE_ENDS[0]}, high at spec {CASE_ENDS[1]}")
    # One land row per component, so the build can require it. The remainder holds no structures on net: the listed types
    # already exceed BEA's enterprise structures.
    for e in ENT:
        other = e[0].startswith("ent_other_")
        gap(f"enterprise: land at 10% of the structures charged: {e[0]}", e[3], 0.0 if other else 0.10 * e[4], "enterprise", 1.0,
            "[GAP] option D only: " + (f"none; the listed types' structures exceed BEA's enterprise structures by {overlap:.1f}bn, so "
                                       "the remainder holds equipment and software only on net" if other else
                                       "land under the listed enterprise structures, at the enterprise-surplus key and response 1"))
    for b in BLK:
        gap_b(f"block: equipment and software (derived split): {b[0]} share {beq_share[b[0]]:.4f}",
              "FAAt701 l56+l73 x share" if b[0].endswith("_sl") else "FAAt701 l39+l53 x share",
              beq_stock[b[0]], b[2], b[1], beq_fee[b[0]], "[GAP] the subfunction's 2024 gross investment (NIPA 3.15.5 less "
              "consumption) less its structures, over all equipment and software investment; federal residuals include R&D; in the "
              "block variant with equipment")
    land_srcs = {k: pdf_text(CACHE / k) for k in LAND}
    gate("land_sources_checked", all(ph in land_srcs[k] for k, phs in LAND.items() for ph in phs),
         "Larson (BEA WP2015-3): federal land $1.8tn (2009) and state-local land for Washington, DC only; Z.1 F.107: the state-local "
         "balance sheet excludes land; Wasshausen (BEA 2011): the IMAs use structures excluding land")

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
        42: ("federal nondefense", "commercial", "gap", "no function; any Postal Service part is in the enterprise total (option D)"),
        43: ("federal nondefense", "health care", "charged", "health"),
        44: ("federal nondefense", "educational", "gap", "no K-12/other split"),
        45: ("federal nondefense", "public safety", "charged", "public order and safety"),
        46: ("federal nondefense", "amusement and recreation", "block", "recreation: national parks at the long-run response"),
        47: ("federal nondefense", "transportation", "block", "economic affairs: air traffic facilities at the air response"),
        48: ("federal nondefense", "power", "enterprise (option D)", "TVA and the power marketing administrations: federal enterprises"),
        49: ("federal nondefense", "highways and streets", "block", "economic affairs: federal highways at the long-run response"),
        50: ("federal nondefense", "conservation and development", "response 0", "natural resources and water held at 0 in the "
                                                                                 "long-run responses"),
        51: ("federal nondefense", "other structures", "gap", "no function"),
        53: ("federal nondefense", "software", "gap", "no function split"),
        54: ("federal nondefense", "research and development", "gap", "health's share bounded; non-rival"),
        56: ("state and local", "equipment", "K-12 part charged", "K-12 by F-33; the rest a gap (equipment_and_software variant)"),
        58: ("state and local", "residential", "enterprise (option D)", "public housing: an enterprise; at the enterprise-surplus key "
                                                                        "and response 1 under option D, out under option A"),
        59: ("state and local", "office", "charged", "general government (NIPA files it there)"),
        60: ("state and local", "commercial", "gap", "no function; its parking and liquor-store part is in the enterprise total (option D)"),
        61: ("state and local", "health care", "charged", "health, in full (the line is already net of hospital sales)"),
        62: ("state and local", "educational", "charged", "K-12 and colleges and libraries; museums and zoos in the block "
                                                          "(recreation); preschool a gap"),
        63: ("state and local", "public safety", "charged", "public order and safety"),
        64: ("state and local", "amusement and recreation", "block", "recreation at the long-run response, in full"),
        65: ("state and local", "transportation", "enterprise (option D)", "transit, airports and ports: enterprises"),
        66: ("state and local", "power", "enterprise (option D)", "electric and gas utilities: enterprises"),
        67: ("state and local", "highways and streets", "block (nontoll part)", "highways at the long-run response, in full; toll "
                                                                                "facilities are enterprises (option D)"),
        68: ("state and local", "sewer systems", "enterprise (option D)", "enterprise; the sanitation part (general government) is a gap"),
        69: ("state and local", "water systems", "enterprise (option D)", "enterprise"),
        70: ("state and local", "conservation and development", "response 0", "natural resources held at 0 in the long-run responses"),
        71: ("state and local", "other structures", "gap", "no function"),
        73: ("state and local", "software", "K-12 part charged", "K-12 by F-33; the rest a gap"),
        74: ("state and local", "research and development", "gap", "university research; non-rival"),
    }
    type_acc = [[lv, ln, t, avg(ln), bn(D[ln][YEAR]), tr, why] for ln, (lv, t, tr, why) in TYPE_TREAT.items()]
    covered = sum(avg(ln) for ln in TYPE_TREAT)
    gate("asset_type_accounting_covers_all_government_capital", abs(covered - avg(1)) < 0.001 * avg(1),
         f"types {covered:.1f} vs all government fixed assets {avg(1):.1f} (FAAt701 l1, 2024 average)")

    # ---------------- 10. per-specification rows, and the build's recipe with its recompute gate
    spec_rows, comp_long = [], []
    for m in methods:
        for i, sp in enumerate(specs):
            spec_rows.append([m, i, sp["allocation"], sp["normalization"], sp["share"], sp["school"], sp["gg"], sp["uc"], sp["justice"],
                              costs[m][i]] + [total[lab][m][i] for lab in all_rates] + [costs[m][i] + total[lab][m][i] for lab in all_rates])
            for cid, line, *_ in COMP:
                comp_long.append([m, i, cid, charged[cid], V[m][i][line][0], V[m][i][line][1]] + [R[lab][m][i][cid] for lab in all_rates])
    pb_rows = []
    for m in methods:
        for i in range(n):
            a_lo = lin["low"][m][i] + total["2pct"][m][i] + btot[("2pct", "low")][m][i]
            a_hi = lin["high"][m][i] + total["3pct"][m][i] + btot[("3pct", "high")][m][i]
            pb_rows.append([m, i, amt[EA][m][i], amt[RC][m][i], costs[m][i], lin["low"][m][i], lin["high"][m][i], lin["across_high"][m][i]]
                           + [total[lab][m][i] for lab in all_rates]
                           + [btot[(lab, sc)][m][i] for lab in all_rates for sc in ("low", "high", "across_high")]
                           + [etot[lab][m][i] for lab in all_rates] + [esur[m][i]]
                           + [a_lo, a_hi, a_lo + esur[m][i] + etot["2pct"][m][i], a_hi + esur[m][i] + etot["3pct"][m][i]])

    rel = lambda p: str(p.relative_to(ROOT))
    INPUTS = {rel(p): sha(p) for p in [
        DEFINITIONS, SL.NIPA3, NIPA1, HELPER, MAIN / "package.cjs", MAIN / "derived" / "corrections.json",
        MAIN / "derived" / "summary.json", MAIN / "derived" / "main_case_bands.csv", SCHOOL / "capital_return.py",
        SCHOOL / "derived" / "summary.json", SCHOOL / "derived" / "sources.csv", R_VALUES, DEBT_RESULT, DEBT_SCRIPT, MATCHED, DECISION,
        FISCAL / "assumption_explorer_2026_09_21" / "engine.js", MODEL, FISCAL / "main_case_2026_09_26" / "package.cjs",
        FISCAL / "main_case_2026_09_24" / "package.cjs", RESPONSES, LR_COSTS, LR_BAND, LR_NET, COG_PINS, COG_API]
        + [FISCAL / "local_spending_composition_2026_09_18" / "_cache" / f"indunit_{y}.zip" for y in COG_YEARS]
        + [s.with_suffix(x) for s in [HIGHFILL, HANDBOOK9, HANDBOOK2, MP5] + [CACHE / k for k in LAND] for x in (".pdf", ".txt")]}
    INPUTS.update({rel(SL.CACHE / f): r["sha256"] for f, r in school_reg.items()})   # verified by check_cache above

    # One entry per charged component. Keys and responses are rules on the engine's evaluation (spec_lines.cjs), so a
    # re-keyed evaluation (by generation, say) splits every return keyed that way.
    def from_lines(num: list, den: str) -> dict:
        return {"kind": "lines_amount_over_national", "numerator_lines": num, "denominator_line": den}

    KEY_RULE = {
        "k12": from_lines(["education_services", "school_reprice"], "education_services"),
        "college": from_lines(["education_services", "college_rekey"], "education_services"),
        "public_order_safety": from_lines(["public_order_safety"], "public_order_safety"),
        "health_services": from_lines(["health_services"], "health_services"),
        "general_public_services": from_lines(["general_public_services"], "general_public_services"),
        "income_security_services": from_lines(["income_security_services"], "income_security_services"),
        "ea": from_lines([EA], EA), "rc": from_lines([RC], RC)}
    RESP_RULE = {
        "k12": {"kind": "line_response_over_share", "line": "school_reprice", "share": "school",
                "note": "the school part's response: school_reprice's response over the specification's school fraction"},
        "college": {"kind": "line_response_over_share", "line": "college_rekey", "share": "college",
                    "note": "the college part's response: college_rekey's response over (1 - the school fraction)"},
        "public_order_safety": {"kind": "line_response", "line": "public_order_safety"},
        "health_services": {"kind": "line_response", "line": "health_services"},
        "general_public_services": {"kind": "line_response", "line": "general_public_services"},
        "income_security_services": {"kind": "line_response", "line": "income_security_services"}}
    ENGINE_LINES = {"k12": ["education_services", "school_reprice"], "college": ["education_services", "college_rekey"],
                    "public_order_safety": ["public_order_safety"], "health_services": ["health_services"],
                    "general_public_services": ["general_public_services"], "income_security_services": ["income_security_services"]}
    ENT_KEY = {"kind": "receipt_amount_over_national", "line": "enterprise_surplus",
               "note": "the enterprise-surplus receipt's own key (resident population), as the account keys it"}
    ENT_RESP = {"kind": "enterprises_switch", "values": {"D": 1.0, "A": 0.0}}
    level = lambda cid: "federal" if cid.endswith("_fed") else "state_local"
    comps_json = [{"id": cid, "part": "core", "level": level(cid), "label": label, "bea_source": bea, "engine_lines": ENGINE_LINES[line],
                   "national_stock_bn": stock, "share_charged": fee, "stock_charged_bn": ch, "depreciation_2024_charged_basis_bn": dep,
                   "key": KEY_RULE[line], "response": RESP_RULE[line]} for cid, line, label, bea, stock, fee, ch, dep in COMP]
    for cid, sfid, vw, label, bea, stock, share, fee, dep in BLK:
        lid = EA if vw == "ea" else RC
        comps_json.append({"id": cid, "part": "block", "level": level(cid), "label": label, "bea_source": bea, "engine_lines": [lid],
                           "national_stock_bn": stock, "share_charged": share * fee, "stock_charged_bn": bcharged[cid],
                           "depreciation_2024_charged_basis_bn": dep * share * fee, "key": KEY_RULE[vw],
                           "response": {"kind": "long_run_subfunction", "file": rel(RESPONSES), "line": lid, "subfunction": sfid,
                                        "values": {"low": SF[sfid]["response"]["low"], "high": SF[sfid]["response"]["high"],
                                                   "across_high": across(SF[sfid])},
                                        "note": "low at the low end, high at the high end; across_high is the response lane's "
                                                "across-state reading at the high end"}})
    for cid, lv, label, bea, stock, dep in ENT:
        comps_json.append({"id": cid, "part": "enterprise", "level": lv, "label": label, "bea_source": bea, "engine_lines": [],
                           "receipt_lines": ["enterprise_surplus"], "national_stock_bn": stock, "share_charged": 1.0,
                           "stock_charged_bn": stock, "depreciation_2024_charged_basis_bn": dep, "key": ENT_KEY, "response": ENT_RESP})
    land_ids = [g[0].rsplit(": ", 1)[1] for g in gap_rows
                if re.fullmatch(r"((block|enterprise): )?land at 10% of the structures charged: \S+", g[0])]
    gate("gaps_has_one_land_row_per_component", sorted(land_ids) == sorted(c["id"] for c in comps_json),
         f"{len(land_ids)} land rows in gaps.csv for the {len(comps_json)} components of engine_components.json")
    at_end = lambda series, i: at(series, i)
    k12_ret = lambda i, m, r, vw: k12["avg2024"] * r * V[m][i][vw][0] * V[m][i][vw][1]
    hs_ret = lambda i, m, r, vw: ent_stock["ent_housing_sl"] * r * V[m][i][vw][0]
    k12_keys = {f"spec{i}": {
        "pupil_share": s_pupil, "account_key": {m: V[m][i]["k12"][0] for m in methods},
        "return_bn": {lab: {"account_key": sum(k12_ret(i, m, r, "k12") for m in methods) / len(methods),
                            "pupil_share": sum(k12_ret(i, m, r, "k12_pupil_share") for m in methods) / len(methods)}
                      for lab, r in all_rates.items()}} for i in CASE_ENDS}
    hs_keys = {f"spec{i}": {
        "enterprise_key": {m: V[m][i]["enterprise"][0] for m in methods},
        "rental_assistance_key": {m: V[m][i]["housing_subsidies_at_response_1"][0] for m in methods},
        "housing_subsidies_group_amount_bn": {m: per[m][i]["lines"]["housing_subsidies"]["amount_bn"] for m in methods},
        "note": f"the case's corrections re-key housing_subsidies: corrections.json edits its housing_support amount by "
                f"{hs_edit['personal']:+.4f}bn, from model.json's {hs_target:.4f}bn (key {hs_base:.4f}), so the evaluated key is "
                f"lower; the engine charges target_bn, so model.json's key is target_bn over national_bn",
        "uncorrected_model_share": hs_base, "uncorrected_model_amount_bn": hs_target, "corrections_json_edit_bn": hs_edit["personal"],
        "return_bn": {lab: {w: sum(hs_ret(i, m, r, vw) for m in methods) / len(methods) for w, vw in (
            ("enterprise_key", "enterprise"), ("rental_assistance_key", "housing_subsidies_at_response_1"),
            ("uncorrected_model_share", "housing_support_uncorrected"))} for lab, r in all_rates.items()}} for i in CASE_ENDS}

    # Definition variants in the build's grammar (main_case_long_run_2026_09_27/package.cjs componentsFor): overrides of a
    # component's stock_charged_bn, key or response, or its drop, then whole components added. Netting charges is an
    # error, not a variant; the enterprises switch is a top-level choice. The two public-housing keys act under option D.
    def added(cid: str, line: str, label: str, bea: str, stock: float, response: dict | None = None) -> dict:
        return {"id": cid, "part": "core", "level": level(cid), "label": label, "bea_source": bea, "engine_lines": ENGINE_LINES[line],
                "stock_charged_bn": stock, "key": KEY_RULE[line], "response": response or RESP_RULE[line]}

    stock_of = lambda cid, stock: {"component": cid, "stock_charged_bn": stock}
    variants_json = {name: {"label": VARIANTS[name][0], **spec} for name, spec in {
        "equipment_and_software": {"adds": [
            added(e[0], e[1], f"equipment and software (derived split, share {e[4]:.4f} of the level's equipment and software)",
                  "FAAt701 l56+l73" if e[0].endswith("_sl") else "FAAt701 l39+l53", e[2] * e[4] * e[3]) for e in EQ]},
        "end_2024_stocks": {"overrides": [stock_of(c, end_stock[c]) for c in charged]},
        "sl_office_at_unallocable_response": {"adds": [
            added("gps_sl_row8_increment", "general_public_services", "state and local offices: audit row 8's increment over "
                  "general government's response", "FAAt701 l59", charged["gps_sl"], {"kind": "fixed", "value": row8_step})]},
        "offices_at_response_1": {"overrides": [{"component": c, "response": {"kind": "fixed", "value": 1.0}} for c in ("gps_sl", "gps_fed")]},
        "higher_ed_auxiliaries_fee_financed": {"overrides": [stock_of("college", aux_stock["college"])]},
        # (1 - the school fraction) x the college response is college_rekey's own response.
        "college_by_account_school_fraction": {"overrides": [{"component": "college", "stock_charged_bn": charged["college"] / (1 - k12_key),
                                                              "response": {"kind": "line_response", "line": "college_rekey"}}]},
        "k12_at_pupil_share": {"overrides": [{"component": "k12", "key": {"kind": "constant", "value": s_pupil}}]},
    }.items()}
    variants_json.update({
        "public_housing_at_rental_assistance_key": {
            "label": "public housing keyed like rental assistance (housing_subsidies' housing_support as evaluated) instead of the "
                     "enterprise-surplus key; acts under option D",
            "overrides": [{"component": "ent_housing_sl", "key": from_lines(["housing_subsidies"], "housing_subsidies")}]},
        "public_housing_at_uncorrected_rental_key": {
            "label": f"public housing at model.json's housing_support key ({hs_base:.4f}: {hs_target:.2f} of "
                     f"{hs_line['national_bn']:.2f}), before the case's corrections re-key the line; acts under option D",
            "overrides": [{"component": "ent_housing_sl", "key": {"kind": "constant", "value": hs_base}}]}})
    BVAR_OF = {"block_" + "_".join(name.split()): name for name in BVAR}
    for vid, name in BVAR_OF.items():
        stocks = BVAR[name][0]
        variants_json[vid] = {"label": f"block: {name}: {BVAR[name][1]}",
                              "overrides": [stock_of(c, stocks[c]) for c in bcharged if stocks[c] != bcharged[c]]}
    EVAR_OF = {"public_housing_at_rental_assistance_key": "housing_subsidies_at_response_1",
               "public_housing_at_uncorrected_rental_key": "housing_support_uncorrected"}

    def variant_ref(name: str, lab: str, sc: str) -> tuple:
        """The variant's (core, block, option D enterprise) returns by method and specification as this lane computes them."""
        if name in VARIANTS:
            return VR[(name, lab)], btot[(lab, sc)], etot[lab]
        if name in EVAR_OF:
            return total[lab], btot[(lab, sc)], etot_housing(EVAR_OF[name], lab)
        return total[lab], bseries(BVAR[BVAR_OF[name]][0], lab, sc), etot[lab]

    for name, v in variants_json.items():
        refs = {(lab, sc): variant_ref(name, lab, sc) for lab, sc in (("2pct", "low"), ("3pct", "high"))}
        v["check_at_case_ends_bn"] = {
            "core_2pct": [at(refs[("2pct", "low")][0], i) for i in CASE_ENDS], "core_3pct": [at(refs[("3pct", "high")][0], i) for i in CASE_ENDS],
            "block_2pct_low": [at(refs[("2pct", "low")][1], i) for i in CASE_ENDS],
            "block_3pct_high": [at(refs[("3pct", "high")][1], i) for i in CASE_ENDS],
            "enterprise_returns_option_D_2pct": [at(refs[("2pct", "low")][2], i) for i in CASE_ENDS],
            "enterprise_returns_option_D_3pct": [at(refs[("3pct", "high")][2], i) for i in CASE_ENDS]}
    recipe = {
        "note": "Capital definitions of capital_return_services_2026_09_27 for the main-case build. For each component and "
                "specification, return = stock_charged_bn x rate x key x response; key and response are rules on the engine's "
                "evaluation of that specification (spec_lines.cjs), so a re-keyed evaluation (by generation, say) splits every "
                "component. No charges are netted: the account's lines are already net of sales. The enterprises switch "
                "(option D or A) is the operator's choice. variants are definition variants in the build's grammar: {name: "
                "{label, overrides: [{component, stock_charged_bn | key | response | drop}], adds: [components]}}, applied in "
                "that order; their check values are this lane's own numbers. The recompute gates reproduce per_spec.csv, "
                "per_spec_block.csv and every variant from this file and the evaluation alone.",
        "status": "proposed, not adopted",
        "year": YEAR, "rates": all_rates,
        "band": {"low_end": "2pct; block at the low responses", "high_end": "3pct; block at the high responses",
                 "reported_only": list(REPORTED), "case_end_specs": list(CASE_ENDS),
                 "ends": "each fill-in method's minimum and maximum over the specifications, averaged over the methods"},
        "evaluation": {"script": rel(HELPER), "methods": methods, "profile": case["profile"],
                       "fields": "per_method[method][spec].lines[line_id] = {amount_bn, national_bn, key, response}; "
                                 "per_method[method][spec].enterprise = the enterprise_surplus receipt {amount_bn, national_bn, key, "
                                 "response}; specs[spec] = {share (the school fraction), school, gg, allocation, ...}"},
        "rule_kinds": {
            "lines_amount_over_national": "sum of the numerator spending lines' amount_bn over the denominator line's national_bn",
            "receipt_amount_over_national": "the receipt line's amount_bn over its national_bn",
            "constant": "value", "fixed": "value", "line_response": "the spending line's response",
            "line_response_over_share": "the line's response over the school fraction (share 'school') or over one minus it "
                                        "(share 'college')",
            "long_run_subfunction": "values[scenario]: low at the low end, high at the high end",
            "enterprises_switch": "values[the chosen option]: 1 under D, 0 under A"},
        "enterprises": {
            "choice": "the operator's: D or A (no default)",
            "allowed": ["D", "A"],
            "options": {
                "D": {"label": "all enterprises respond: every government enterprise's capital at the enterprise-surplus key and "
                               "response 1, and the enterprise_surplus receipt at response 1",
                      "enterprise_component_response": 1.0, "receipt_responses": {"enterprise_surplus": 1.0}},
                "A": {"label": "enterprises out: no enterprise capital, and the enterprise_surplus receipt held at 0",
                      "enterprise_component_response": 0.0, "receipt_responses": {"enterprise_surplus": 0.0}}},
            "receipt_rule": "a receipt changes the cost by -amount_bn x response; the enterprise_surplus receipt is NIPA 3.8's total "
                            f"({ent_nat:.2f}bn, a deficit), so at response 1 the group's share ({ent_grp:.4f}bn) raises the cost by "
                            f"{-ent_grp:.4f}bn",
            "capital": f"BEA's government enterprise fixed assets, {ent_total:.1f}bn on the 2024 average (FAAt701 l79), split by "
                       "type for reporting only; every piece takes the same key and response",
            "surplus_before_interest": {"source": "BEA, Government Transactions (NIPA Methodology Paper 5, 2005); NIPA Handbook ch. 2 "
                                                  "(December 2024)",
                                        "quotes": list(INTEREST_PHRASES["mp5"][:3]) + [INTEREST_PHRASES["handbook2"][0]],
                                        "reading": "the surplus is before interest and enterprises' interest sits with general "
                                                   "government's, the account's interest row (held at 0), so charging the full "
                                                   "return does not count interest twice"},
            "subsidies_received": "the surplus includes subsidies received from other levels of government (MP-5), such as federal "
                                  "subsidies to public housing authorities (Handbook ch. 2), so under D those payments and the "
                                  "housing_subsidies line offset except for their different keys"},
        "long_run": {"file": rel(RESPONSES), "rule": "long-run cost = case cost + the sum over these lines of amount_bn x the "
                                                     "blended response",
                     "blended_response": {lid: {sc: blend(lid, sc) for sc in ("low", "high", "across_high")} for lid in (EA, RC)}},
        "components": comps_json,
        "variants": variants_json,
        "k12_keys_at_case_ends": k12_keys,
        "public_housing_keys_at_case_ends": hs_keys,
        "check_at_case_ends_bn": {
            "core": {lab: [at_end(total[lab], i) for i in CASE_ENDS] for lab in all_rates},
            "block": {f"{lab}|{sc}": [at_end(btot[(lab, sc)], i) for i in CASE_ENDS] for lab in all_rates for sc in ("low", "high", "across_high")},
            "enterprise_returns_option_D": {lab: [at_end(etot[lab], i) for i in CASE_ENDS] for lab in all_rates},
            "enterprise_surplus_move_option_D": [at_end(esur, i) for i in CASE_ENDS],
            "option_D_band": [cand_d[2], cand_d[3]], "option_A_band": [cand_a[2], cand_a[3]]},
        "inputs": INPUTS,
    }
    recipe_text = json.dumps(recipe, indent=1, sort_keys=True) + "\n"
    rc = json.loads(recipe_text)            # the recompute reads only this and the evaluation

    def rkey(rule: dict, ev: dict) -> float:
        if rule["kind"] == "constant":
            return rule["value"]
        if rule["kind"] == "lines_amount_over_national":
            return sum(ev["lines"][x]["amount_bn"] for x in rule["numerator_lines"]) / ev["lines"][rule["denominator_line"]]["national_bn"]
        if rule["kind"] == "receipt_amount_over_national":
            return ev["receipts"][rule["line"]]["amount_bn"] / ev["receipts"][rule["line"]]["national_bn"]
        raise SystemExit(f"[BLOCKED] unknown key rule {rule['kind']}")

    def rresp(rule: dict, ev: dict, sp: dict, sc: str | None, opt: str) -> float:
        if rule["kind"] == "line_response":
            return ev["lines"][rule["line"]]["response"]
        if rule["kind"] == "line_response_over_share":
            return ev["lines"][rule["line"]]["response"] / (sp["share"] if rule["share"] == "school" else 1 - sp["share"])
        if rule["kind"] == "fixed":
            return rule["value"]
        if rule["kind"] == "long_run_subfunction":
            return rule["values"][sc]
        if rule["kind"] == "enterprises_switch":
            return rule["values"][opt]
        raise SystemExit(f"[BLOCKED] unknown response rule {rule['kind']}")

    def part_return(part: str, ev: dict, sp: dict, r: float, sc: str | None, opt: str, comps: list | None = None) -> float:
        return sum(c["stock_charged_bn"] * r * rkey(c["key"], ev) * rresp(c["response"], ev, sp, sc, opt)
                   for c in (rc["components"] if comps is None else comps) if c["part"] == part)

    def receipt_move(ev: dict, opt: str) -> float:
        return sum(-ev["receipts"][x]["amount_bn"] * resp for x, resp in rc["enterprises"]["options"][opt]["receipt_responses"].items())

    evs = {(m, i): {"lines": per[m][i]["lines"], "receipts": {"enterprise_surplus": per[m][i]["enterprise"]}}
           for m in methods for i in range(n)}
    re_spec, re_pb, opt_a = [], [], 0.0
    SCS = ("low", "high", "across_high")
    for m in methods:
        for i, sp in enumerate(specs):
            ev, cost_i = evs[(m, i)], per[m][i]["cost_bn"]
            L = ev["lines"]
            core_r = {lab: part_return("core", ev, sp, rc["rates"][lab], None, "D") for lab in all_rates}
            re_spec.append([m, i, sp["allocation"], sp["normalization"], sp["share"], sp["school"], sp["gg"], sp["uc"], sp["justice"],
                            cost_i] + [core_r[lab] for lab in all_rates] + [cost_i + core_r[lab] for lab in all_rates])
            lr_c = {sc: cost_i + sum(L[lid]["amount_bn"] * rc["long_run"]["blended_response"][lid][sc] for lid in (EA, RC)) for sc in SCS}
            blk_r = {(lab, sc): part_return("block", ev, sp, rc["rates"][lab], sc, "D") for lab in all_rates for sc in SCS}
            ent_r = {lab: part_return("enterprise", ev, sp, rc["rates"][lab], None, "D") for lab in all_rates}
            sur = receipt_move(ev, "D")
            opt_a = max(opt_a, abs(receipt_move(ev, "A")), *(abs(part_return("enterprise", ev, sp, r, None, "A")) for r in rc["rates"].values()))
            lo = lr_c["low"] + core_r["2pct"] + blk_r[("2pct", "low")]
            hi = lr_c["high"] + core_r["3pct"] + blk_r[("3pct", "high")]
            re_pb.append([m, i, L[EA]["amount_bn"], L[RC]["amount_bn"], cost_i] + [lr_c[sc] for sc in SCS]
                         + [core_r[lab] for lab in all_rates] + [blk_r[(lab, sc)] for lab in all_rates for sc in SCS]
                         + [ent_r[lab] for lab in all_rates] + [sur]
                         + [lo, hi, lo + sur + ent_r["2pct"], hi + sur + ent_r["3pct"]])

    def max_diff(a: list, b: list) -> float:
        if len(a) != len(b):
            return float("inf")
        worst = 0.0
        for ra, rb in zip(rows_out(a, 12), rows_out(b, 12)):
            if len(ra) != len(rb):
                return float("inf")
            for x, y in zip(ra, rb):
                if isinstance(x, float) or isinstance(y, float):
                    worst = max(worst, abs(float(x) - float(y)))
                elif x != y:
                    return float("inf")
        return worst

    def rule_lines(rule: dict) -> tuple:
        """(spending lines, receipt lines) a key or response rule reads."""
        if rule["kind"] == "receipt_amount_over_national":
            return set(), {rule["line"]}
        return set(rule.get("numerator_lines", [])) | {rule[f] for f in ("denominator_line", "line") if f in rule}, set()

    def lines_missing(comps: list) -> list:
        spend, recv = set(), set()
        for c in comps:
            for rule in (c["key"], c["response"]):
                s_, r_ = rule_lines(rule)
                spend |= s_
                recv |= r_
            spend |= set(c["engine_lines"])
            recv |= set(c.get("receipt_lines", []))
        return sorted(x for x in spend if x not in evs[(methods[0], 0)]["lines"]) + sorted(x for x in recv if x not in evs[(methods[0], 0)]["receipts"])

    d_spec, d_pb = max_diff(re_spec, spec_rows), max_diff(re_pb, pb_rows)
    rc_missing = lines_missing(rc["components"])
    gate("engine_components_recompute_the_per_spec_outputs", d_spec < 1e-9 and d_pb < 1e-9 and opt_a == 0 and not rc_missing,
         f"per_spec.csv ({len(re_spec)} rows) and per_spec_block.csv ({len(re_pb)} rows, enterprise columns under option D) "
         f"recomputed from engine_components.json and the spec_lines.cjs evaluation alone: max |diff| {d_spec:.1e} and "
         f"{d_pb:.1e}; option A gives exactly 0 for the enterprise block and the receipt"
         + (f"; lines missing from the evaluation: {rc_missing}" if rc_missing else ""))

    def components_for(name: str) -> list:
        """A variant's components, applied as the build's componentsFor applies them."""
        comps = [dict(c) for c in rc["components"]]
        for o in rc["variants"][name].get("overrides", []):
            fields = set(o) - {"component"}
            hit = [j for j, c in enumerate(comps) if c["id"] == o["component"]]
            if len(hit) != 1 or not fields or fields - {"stock_charged_bn", "key", "response", "drop"}:
                raise SystemExit(f"[BLOCKED] variant {name}: bad override {o}")
            if o.get("drop"):
                comps.pop(hit[0])
                continue
            for f in fields:
                comps[hit[0]][f] = o[f]
        comps += rc["variants"][name].get("adds", [])
        if len({c["id"] for c in comps}) != len(comps):
            raise SystemExit(f"[BLOCKED] variant {name} repeats a component id")
        return comps

    var_err, var_missing = 0.0, set()
    for name in rc["variants"]:
        comps = components_for(name)
        var_missing |= set(lines_missing(comps))
        for lab in RATES:
            r = rc["rates"][lab]
            for sc in SCS:
                core_ref, blk_ref, ent_ref = variant_ref(name, lab, sc)
                for m in methods:
                    for i, sp in enumerate(specs):
                        ev = evs[(m, i)]
                        var_err = max(var_err, abs(part_return("core", ev, sp, r, None, "D", comps) - core_ref[m][i]),
                                      abs(part_return("block", ev, sp, r, sc, "D", comps) - blk_ref[m][i]),
                                      abs(part_return("enterprise", ev, sp, r, None, "D", comps) - ent_ref[m][i]))
    gate("engine_components_variants_reproduce_this_lanes_variants", var_err < 1e-9 and not var_missing,
         f"{len(rc['variants'])} variants, applied as the build applies them (overrides, drops, adds), reproduce bands.csv's "
         f"variants, the block variants and the public-housing keys under option D, at 2% and 3%, at every specification and "
         f"response reading: max |diff| {var_err:.1e}" + (f"; lines missing from the evaluation: {sorted(var_missing)}" if var_missing else ""))

    # ---------------- gates
    failed = [g for g in GATES if not g[1]]
    for name, ok, detail in GATES:
        print(f"  {'PASS' if ok else 'FAIL'}  {name}: {detail}")
    if failed:
        print(f"[BLOCKED] {len(failed)} gate(s) failed; nothing written")
        return 1

    # ---------------- outputs
    DERIVED.mkdir(exist_ok=True)

    def write_csv(name: str, header: list[str], rows: list[list], digits: int = 6) -> None:
        with (DERIVED / name).open("w", newline="") as f:
            wr = csv.writer(f, lineterminator="\n")
            wr.writerow(header)
            wr.writerows(rows_out(rows, digits))

    TREAT = {
        "general_public_services": ("charged", "S&L and federal nondefense Office (FAAt701 l59, l41): city halls, capitols, courthouses, "
                                    "administration buildings; NIPA files S&L office investment under this line"),
        "defense": ("response 0", "national defense responds at 0"),
        "public_order_safety": ("charged", "S&L and federal nondefense Public safety (l63, l45); courthouses sit in Office"),
        "economic_affairs_services": ("held fixed; block", "response 0 in the main profile; the conditional block prices nontoll "
                                     "highways and federal air and highway structures at the long-run responses; toll facilities, "
                                     "transit, airports and ports are enterprises (option D)"),
        "housing_community_services": ("sanitation only; a gap", "S&L consumption is sanitation only (NIPA 3.16 note 8); its "
                                       "structures sit inside Sewer systems (a gap); water, sewer and public housing are enterprises "
                                       "(option D)"),
        "housing_subsidies": ("response 0", "subsidies respond at 0; its housing_support key is a variant for public housing, "
                              "which option D keys at the enterprise-surplus key"),
        "health_services": ("charged", "S&L Health care (l61) in full (the line is already net of hospital sales); federal "
                                       "nondefense Health care (l43)"),
        "recreation_culture": ("held fixed; block", "response 0 in the main profile; the conditional block prices parks, museums "
                               "and zoos, and national parks at the long-run responses"),
        "education_services": ("charged", "K-12 (school lane) and colleges and other education (non-K-12 educational structures)"),
        "income_security_services": ("no identified capital", "no BEA structure type; its offices sit in Office (charged under general "
                                     "government); equipment and software a gap"),
        "domestic_interest": ("response 0", "existing interest held at 0 (double-count gate)"),
        "foreign_interest": ("outside the resident account", "foreign flow"),
        "school_reprice": ("charged with education", "school part's correction; enters the K-12 key"),
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
    hdr = ["component", "line", "label", "bea_source", "national_stock_avg2024_bn", "share_charged", "stock_charged_bn",
           "depreciation_2024_charged_basis_bn", "key_min", "key_max", "response_min", "response_max"]
    for lab in all_rates:
        hdr += [f"return_{lab}_spec{CASE_ENDS[0]}_bn", f"return_{lab}_spec{CASE_ENDS[1]}_bn", f"return_{lab}_min_bn", f"return_{lab}_max_bn"]
    write_csv("components.csv", hdr, comp_rows)

    # per_spec.csv and per_spec_block.csv carry 12 decimals, so the recompute gate holds to 1e-9 on the files themselves.
    write_csv("per_spec.csv", ["method", "spec", "allocation", "normalization", "school_share", "school_response", "gg_response",
                               "uc_key", "justice_key", "case_cost_bn"] + [f"return_{lab}_bn" for lab in all_rates]
              + [f"cost_with_return_{lab}_bn" for lab in all_rates], spec_rows, 12)
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

    # the conditional block
    blk_rows = []
    for cid, sfid, vw, label, bea, stock, share, fee, dep in BLK:
        s = SF[sfid]
        row = [cid, sfid, LR[EA if vw == "ea" else RC]["key"], label, bea, stock, share, fee, bcharged[cid], dep * share * fee,
               s["response"]["low"], s["response"]["high"], across(s), at({m: [V[m][i][BVIEW[vw]][0] for i in range(n)] for m in methods},
                                                                          CASE_ENDS[0]),
               at({m: [V[m][i][BVIEW[vw]][0] for i in range(n)] for m in methods}, CASE_ENDS[1])]
        for lab in all_rates:
            row += [at({m: [x[cid] for x in BR[(lab, "low")][m]] for m in methods}, CASE_ENDS[0]),
                    at({m: [x[cid] for x in BR[(lab, "high")][m]] for m in methods}, CASE_ENDS[1]),
                    at({m: [x[cid] for x in BR[(lab, "across_high")][m]] for m in methods}, CASE_ENDS[1]),
                    at({m: [x[cid] for x in BR[(lab, "unit")][m]] for m in methods}, CASE_ENDS[0]),
                    at({m: [x[cid] for x in BR[(lab, "unit")][m]] for m in methods}, CASE_ENDS[1])]
        blk_rows.append(row)
    hdr = ["component", "subfunction", "line_key", "label", "bea_source", "national_stock_avg2024_bn", "share_charged", "fee_factor",
           "stock_charged_bn", "depreciation_2024_charged_basis_bn", "response_low", "response_high", "response_high_across_states",
           f"key_spec{CASE_ENDS[0]}", f"key_spec{CASE_ENDS[1]}"]
    for lab in all_rates:
        hdr += [f"return_{lab}_spec{CASE_ENDS[0]}_low_bn", f"return_{lab}_spec{CASE_ENDS[1]}_high_bn",
                f"return_{lab}_spec{CASE_ENDS[1]}_across_states_bn", f"return_{lab}_per_unit_response_spec{CASE_ENDS[0]}_bn",
                f"return_{lab}_per_unit_response_spec{CASE_ENDS[1]}_bn"]
    write_csv("block_components.csv", hdr, blk_rows)
    write_csv("per_spec_block.csv", ["method", "spec", "group_economic_affairs_bn", "group_recreation_bn", "case_cost_bn",
                                     "long_run_cost_low_bn", "long_run_cost_high_bn", "long_run_cost_across_high_bn"]
              + [f"core_return_{lab}_bn" for lab in all_rates]
              + [f"block_return_{lab}_{sc}_bn" for lab in all_rates for sc in ("low", "high", "across_high")]
              + [f"enterprise_return_option_D_{lab}_bn" for lab in all_rates] + ["enterprise_surplus_move_option_D_bn"]
              + ["option_A_low_end_basis_2pct_low_bn", "option_A_high_end_basis_3pct_high_bn",
                 "option_D_low_end_basis_2pct_low_bn", "option_D_high_end_basis_3pct_high_bn"], pb_rows, 12)
    (DERIVED / "engine_components.json").write_text(recipe_text)
    write_csv("combined_bands.csv", ["case", "rate", "low_bn", "high_bn", "low_end_spec_by_method", "high_end_spec_by_method",
                                     "long_run_move_at_low_end_bn", "core_return_at_low_end_bn", "block_return_at_low_end_bn",
                                     "enterprise_surplus_move_at_low_end_bn", "enterprise_returns_at_low_end_bn",
                                     "long_run_move_at_high_end_bn", "core_return_at_high_end_bn", "block_return_at_high_end_bn",
                                     "enterprise_surplus_move_at_high_end_bn", "enterprise_returns_at_high_end_bn", "note"], comb_rows)
    ent_rows = [[cid, lv, label, bea, stock, dep] + [stock * r for r in all_rates.values()]
                + [at({m: [ER[lab][m][i][cid] for i in range(n)] for m in methods}, CASE_ENDS[j]) for lab, j in (("2pct", 0), ("3pct", 1))]
                for cid, lv, label, bea, stock, dep in ENT]
    write_csv("enterprise_components.csv", ["component", "level", "label", "bea_source", "stock_avg2024_bn", "depreciation_2024_bn"]
              + [f"national_return_{lab}_bn" for lab in all_rates]
              + [f"group_return_option_D_2pct_spec{CASE_ENDS[0]}_bn", f"group_return_option_D_3pct_spec{CASE_ENDS[1]}_bn"], ent_rows)
    write_csv("enterprise_surplus_vs_return.csv", ["nipa_3_8_group", "nipa_3_8_lines", f"current_surplus_{YEAR}_bn", "components",
                                                   "stock_avg2024_bn", "charges_exceed_production_costs"]
              + [f"national_return_{lab}_bn" for lab in all_rates]
              + [f"group_return_option_D_2pct_spec{CASE_ENDS[0]}_bn", f"group_return_option_D_3pct_spec{CASE_ENDS[1]}_bn"]
              + [f"group_surplus_move_option_D_spec{i}_bn" for i in CASE_ENDS]
              + [f"group_net_option_D_2pct_spec{CASE_ENDS[0]}_bn", f"group_net_option_D_3pct_spec{CASE_ENDS[1]}_bn"], surplus_rows)
    write_csv("census_finance.csv", ["survey_year", "code", "function", "kind", "us_state_and_local_thousands"],
              [[y, c + f, COG_FUNCS[f], {"A": "charges", "E": "current operation", "F": "construction"}[c], cog[y][c + f]]
               for y in COG_YEARS for f in COG_FUNCS for c in "AEF"])
    write_csv("charges_over_production_costs.csv", ["function", "bea_table5_row"] + [str(y) for y in t5_years] + ["use"],
              [[k, T5[k]] + [t5r[k][y] for y in t5_years] + [
                  {"toll": "enterprise (option D)", "air": "enterprise (option D)", "ports": "enterprise (option D)",
                   "parking": "enterprise (option D; inside the remainder)", "parks": "general government: charged in full (netting rejected)",
                   "regular_highways": "general government: charged in full (netting rejected)", "transit": "enterprise (option D)",
                   "housing": "enterprise (option D)", "sewerage": "enterprise (option D)", "water": "enterprise (option D)"}[k]]
               for k in T5])
    write_csv("transport_split.csv", ["year", "bea_sl_transportation_investment_mn", "bea_investment_quantity_index", "pim_weight_in_2024_stock",
                                      "vip_transportation_mn", "vip_air_mn", "vip_land_mn", "vip_water_mn", "vip_land_share"],
              [[t, INV[65][t], Q[65][t], w65[t]] + ([vip[TP][t], vip[f"{TP}/Air"][t], vip[f"{TP}/Land"][t], vip[f"{TP}/Water"][t], msh["Land"][t]]
                                                    if t >= SL.VINTAGE_SPLIT else [None] * 5) for t in yrs65])
    (DERIVED / "gates.json").write_text(json.dumps([{"gate": g, "pass": ok, "detail": d} for g, ok, d in GATES], indent=1) + "\n")

    ends = {lab: {"case_ends": [at(total[lab], CASE_ENDS[0]), at(total[lab], CASE_ENDS[1])],
                  "min_over_specs": min(min(total[lab][m]) for m in methods), "max_over_specs": max(max(total[lab][m]) for m in methods)}
            for lab in all_rates}
    PIECES = ("long_run_move", "core", "block", "enterprise_surplus_move", "enterprise_returns")

    def removed(lab: str, i: int, part: str) -> float:
        """What the rejected netting would take off the return at one end specification."""
        r = all_rates[lab]
        if part == "core":
            return at({m: [sum(ret(charged, j, m, r).values()) - sum(ret(dict(charged, **netted_core), j, m, r).values())
                           for j in range(n)] for m in methods}, i)
        sc = "low" if i == CASE_ENDS[0] else "high"
        return at({m: [sum(bret(bcharged, j, m, r, sc).values()) - sum(bret(dict(bcharged, **netted_block), j, m, r, sc).values())
                       for j in range(n)] for m in methods}, i)

    netting_removes = {part: [removed("2pct", CASE_ENDS[0], part), removed("3pct", CASE_ENDS[1], part)] for part in ("core", "block")}
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
        "college_part_of_non_k12_educational": college_part,
        "rejected_netting": {
            "reason": "the account's lines are consumption, gross output less sales, and an enterprise's surplus is sales less "
                      "costs, so the charges are credited there already; netting the return by the charge share would credit them "
                      "a second time",
            "factors_it_would_apply": {"higher_education_tuition": f_tuition, "health_state_local": f_health,
                                       "regular_highways": f_hwy, "parks": f_parks},
            "federal_nondefense_sales_share_of_federal_health_max": fed_sales_share_max,
            "would_remove_at_case_ends_bn": netting_removes},
        "non_k12_educational_composition": comp, "higher_ed_auxiliary_share": aux,
        "k12": {"key_structures": k12_key, "capital_avg2024_bn": k12["avg2024"], "pupil_share": s_pupil,
                "school_lane_outputs_byte_identical_on_rerun": identical},
        "nipa_unallocable_over_sl_office_investment": unalloc_ratio,
        "equipment_software_shares": {e[0]: e[4] for e in EQ},
        "rd_health_share_bounds": [rd_health_lo, rd_health_hi], "sanitation_share_of_sewer_investment": san_share,
        "row8_response_increment": row8_step,
        "roads_parks_block": {
            "status": "conditional on service_response_long_run_2026_09_27 (proposed, not adopted); beside the core result",
            "responses": {s: {"low": SF[s]["response"]["low"], "high": SF[s]["response"]["high"], "across_high": across(SF[s])}
                          for s in dict.fromkeys(b[1] for b in BLK)},
            "keys_at_case_ends": {k: [at({m: [V[m][i][BVIEW[k]][0] for i in range(n)] for m in methods}, i) for i in CASE_ENDS]
                                  for k in BVIEW},
            "stock_charged_bn": bcharged,
            "return_bn": {f"{lab}|{sc}": {"by_component": {b[0]: at({m: [x[b[0]] for x in BR[(lab, sc)][m]] for m in methods}, i)
                                                          for b in BLK},
                                         "total": at(btot[(lab, sc)], i), "spec": i}
                          for lab in all_rates for sc, i in (("low", CASE_ENDS[0]), ("high", CASE_ENDS[1]), ("across_high", CASE_ENDS[1]))},
            "combined_bands_bn": {f"{r[0]}|{r[1]}": {"band": [r[2], r[3]], "end_specs": [r[4], r[5]],
                                                     "at_low_end": dict(zip(PIECES, r[6:11])), "at_high_end": dict(zip(PIECES, r[11:16]))}
                                  for r in comb_rows},
            "toll_share": {"pooled": toll, "by_survey_year": toll_y},
            "transport_mode_shares": mode, "census_transit_share_of_transport_construction": cog_transit,
            "charges_over_production_costs_2017": {k: t5r[k][t5_last] for k in T5},
            "function_investment_ratio_2024": gi_ratio,
            "equipment_software_shares_2024": beq_share,
            "congestion_change_beside_the_account_bn": {
                "note": "a social item from service_response_long_run_2026_09_27/derived/net_change.json (network follows spending); "
                        "not in the fiscal bands", **{w: lr_net["by_band_end"][w]["congestion_change_bn"] for w in ("low", "high")}},
            "land_per_10pct_total_at_case_ends_bn": {lab: [sum(g[5 + 2 * j + e] for g in gap_rows if g[0].startswith("block: land at 10%"))
                                                           for e in (0, 1)] for j, lab in enumerate(RATES)},
        },
        "enterprises": {
            "choice": "the operator's: option D or option A",
            "options": rc["enterprises"]["options"],
            "bands_bn": {"D": {"band": [cand_d[2], cand_d[3]], "end_specs": [cand_d[4], cand_d[5]]},
                         "A": {"band": [cand_a[2], cand_a[3]], "end_specs": [cand_a[4], cand_a[5]]}},
            "option_D_at_case_ends_bn": {
                "note": f"2% at spec {CASE_ENDS[0]}, 3% at spec {CASE_ENDS[1]}",
                "surplus_line_move": [at(esur, i) for i in CASE_ENDS],
                "returns_by_type": {cid: [at({m: [ER["2pct"][m][i][cid] for i in range(n)] for m in methods}, CASE_ENDS[0]),
                                          at({m: [ER["3pct"][m][i][cid] for i in range(n)] for m in methods}, CASE_ENDS[1])]
                                    for cid, *_ in ENT},
                "returns_total": [at(etot["2pct"], CASE_ENDS[0]), at(etot["3pct"], CASE_ENDS[1])],
                "key": [at({m: [V[m][i]["enterprise"][0] for i in range(n)] for m in methods}, i) for i in CASE_ENDS]},
            "key_consistency": {
                "receipt_key": [at({m: [V[m][i]["enterprise"][0] for i in range(n)] for m in methods}, i) for i in CASE_ENDS],
                "spending_population_key": [at({m: [V[m][i]["general_public_services"][0] for i in range(n)] for m in methods}, i)
                                            for i in CASE_ENDS],
                "option_D_band_at_the_spending_key_bn": next([r[2], r[3]] for r in comb_rows
                                                             if r[0].startswith("option D, enterprises at the spending")),
                "population_keyed_spending_lines_the_corrections_re_key": pop_edited,
                "note": "the receipt keeps model.json's resident_population amount (gate enterprise_receipt_is_model_jsons_resident_"
                        "share); the case's corrections (the CPS lane's stack) re-key the population-keyed spending lines but not "
                        "this receipt"},
            "surplus_vs_return": {r[0]: {"nipa_3_8_lines": r[1], "current_surplus_bn": r[2], "components": r[3], "stock_bn": r[4],
                                         "charges_exceed_production_costs": r[5],
                                         **{f"national_return_{lab}_bn": r[6 + j] for j, lab in enumerate(all_rates)},
                                         "option_D_at_case_ends_bn": {"return": r[9:11], "surplus_move": r[11:13], "net": r[13:15],
                                                                      "note": f"2% at spec {CASE_ENDS[0]}, 3% at spec {CASE_ENDS[1]}"}}
                                  for r in surplus_rows},
            "capital": {"beas_enterprise_total_bn": ent_total, "equipment_bn": avg(80), "structures_bn": avg(81), "ipp_bn": avg(82),
                        "depreciation_2024_bn": ent_dep_fa, "nipa_7_5_enterprise_cfc_bn": ent_cfc, "listed_types_bn": listed,
                        "listed_types_exceed_enterprise_structures_bn": overlap, "remainder_bn": resid_stock,
                        "remainder_split_by_uncovered_depreciation_bn": resid_dep, "stock_by_component_bn": ent_stock},
            "surplus_before_interest": rc["enterprises"]["surplus_before_interest"],
            "subsidies_received": rc["enterprises"]["subsidies_received"],
            "nipa_1_7_5_cfc_bn": {"government": bn(a175[11]), "general_government": bn(a175[12]),
                                  "government_enterprises": bn(a175[13])},
            "nipa_3_8_current_surplus_bn": {f"l{k} {l38[k]}": bn(a38[k]) for k in range(1, 16)},
            "account_line": {"id": "enterprise_surplus", "national_bn": ent_nat, "key": "resident_population",
                             "group_amount_bn": ent_grp, "response_in_every_evaluation_of_the_case": 0},
            "public_housing_keys_at_case_ends": hs_keys,
        },
        "k12_keys_at_case_ends": k12_keys,
        "inputs": INPUTS,
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
    print(f"\nBlock (roads and parks at the long-run responses, in full): toll share {toll:.4f}; netting (rejected) would remove "
          f"core {netting_removes['core'][0]:.3f}/{netting_removes['core'][1]:.3f}, block {netting_removes['block'][0]:.3f}/"
          f"{netting_removes['block'][1]:.3f}")
    for b in BLK:
        print(f"  {b[0]:12s} stock {bcharged[b[0]]:8.1f}  2% low@{CASE_ENDS[0]} "
              f"{at({m: [x[b[0]] for x in BR[('2pct', 'low')][m]] for m in methods}, CASE_ENDS[0]):.3f}  3% high@{CASE_ENDS[1]} "
              f"{at({m: [x[b[0]] for x in BR[('3pct', 'high')][m]] for m in methods}, CASE_ENDS[1]):.3f}")
    print(f"\nEnterprises (option D): BEA total {ent_total:.1f}, key {at({m: [V[m][i]['enterprise'][0] for i in range(n)] for m in methods}, 0):.6f}; "
          f"surplus move {at(esur, CASE_ENDS[0]):.4f}; returns {at(etot['2pct'], CASE_ENDS[0]):.4f} (2% @{CASE_ENDS[0]}) / "
          f"{at(etot['3pct'], CASE_ENDS[1]):.4f} (3% @{CASE_ENDS[1]})")
    for cid, lv, label, bea, stock, dep in ENT:
        print(f"  {cid:16s} stock {stock:8.1f}  2%@{CASE_ENDS[0]} {at({m: [ER['2pct'][m][i][cid] for i in range(n)] for m in methods}, CASE_ENDS[0]):.3f}"
              f"  3%@{CASE_ENDS[1]} {at({m: [ER['3pct'][m][i][cid] for i in range(n)] for m in methods}, CASE_ENDS[1]):.3f}")
    for r in surplus_rows:
        print(f"  {r[0][:44]:44s} surplus {r[2]:7.2f}  stock {r[4]:8.1f}  return 2% {r[6]:6.2f}  3% {r[7]:6.2f}  fee-financed {r[5]}"
              f"  D net {r[13]:+.2f} / {r[14]:+.2f}")
    for r in comb_rows:
        print(f"  {r[0][:70]:70s} {r[1]:9s} {r[2]:.2f}-{r[3]:.2f} (specs {r[4]} / {r[5]})")
    print(f"{len(GATES)} gates passed; wall {time.time() - t0:.1f}s")
    return 0


if __name__ == "__main__":
    sys.exit(main())
