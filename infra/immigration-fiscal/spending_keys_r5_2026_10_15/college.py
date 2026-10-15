"""Item 15: conditional IPEDS function-to-NIPA public-college response bridge.

Run: uv run --no-project python3 infra/immigration-fiscal/spending_keys_r5_2026_10_15/college.py
Raw files are read-only. No acquisition, CPS microdata, case mutation, or Git writes.
The central is a proportional bridge conditional on explicit scope assumptions,
not a measured long-run elasticity. See item15-notes.md for the unresolved bridge.
"""

from __future__ import annotations

import csv
import hashlib
import json
import math
import resource
import time
import zipfile
from pathlib import Path

import pandas as pd
import openpyxl

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
FISCAL = HERE.parent
STAGE = REPO / "sources/immigration-fiscal/data/external/stage3/nces/ipeds_2023"
HD = FISCAL / "affirmative_action_cost_2026_09_24/_cache/ipeds/HD2023.csv"
FEES = FISCAL / "user_fee_allocation_2026_10_07/derived/fee_lines.json"
EXPECTED = {
    "finance_archive": "beabdb0384f000a2fa487e7083512f880013c897d8e10bab9682f4c836687de9",
    "hd": "d779a92d637e122c90009112e284ab5c75bc2b3d26774a29746800f522aace0f",
    "bea": "69b5c7aefb38675324887ce31d6feb4fcde7c903ab952db7328da0813096615e",
    "dictionary_archive": "c2d052827b48075fce820dd6dd6141055f9dd7be76f1c93d6ec1613214be576e",
}
FUNCTIONS = {
    "instruction": "F1C011", "research": "F1C021", "public_service": "F1C031",
    "academic_support": "F1C051", "student_support": "F1C061",
    "institutional_support": "F1C071", "scholarships": "F1C101",
    "auxiliaries": "F1C111", "hospitals": "F1C121",
    "independent_operations": "F1C131", "unclassified_other": "F1C141",
}
REVENUES = {
    "net_tuition": "F1B01", "federal_operating_grants": "F1B02",
    "state_operating_grants": "F1B03", "local_private_operating_grants": "F1B04",
    "auxiliary_sales": "F1B05", "hospital_sales": "F1B06",
    "education_activity_sales": "F1B26", "pell": "F1E01",
    "tuition_discounts": "F1E08", "auxiliary_discounts": "F1E09",
    "total_expenses": "F1C191", "interest": "F1C19IN", "depreciation": "F1C19DP",
}


def sha(path):
    with Path(path).open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def normalized(name):
    return name.replace("ï»¿", "").replace("\ufeff", "").strip()


def read_columns(path, columns):
    frame = pd.read_csv(path, encoding="latin-1", usecols=lambda c: normalized(c) in columns)
    frame.columns = [normalized(c) for c in frame.columns]
    if set(frame.columns) != set(columns):
        raise ValueError(f"[BLOCKED] missing required columns in {path}")
    return frame


def load_totals():
    archive = STAGE / "F2223_F1A.zip"
    bea = REPO / "sources/immigration-fiscal/data/external/bea_nipa/Section3All_xls.xlsx"
    dictionary = STAGE / "F2223_F1A_Dict.zip"
    for label, path in [("finance_archive", archive), ("hd", HD), ("bea", bea), ("dictionary_archive", dictionary)]:
        if sha(path) != EXPECTED[label]:
            raise ValueError(f"[BLOCKED] source hash changed: {path}")
    finance = STAGE / "x/f2223_f1a.csv"
    with zipfile.ZipFile(archive) as zipped:
        if zipped.read("f2223_f1a.csv") != finance.read_bytes():
            raise ValueError("[BLOCKED] extracted IPEDS finance differs from pinned archive")
    hd = read_columns(HD, {"UNITID", "CONTROL", "FIPS"})
    public = hd.loc[hd.CONTROL.eq(1) & hd.FIPS.between(1, 56), "UNITID"]
    amount_cols = {*FUNCTIONS.values(), *REVENUES.values()}
    cols = {"UNITID", *amount_cols, *("X" + c for c in amount_cols)}
    frame = read_columns(finance, cols)
    frame = frame[frame.UNITID.isin(public)]
    numeric, not_applicable = finance_numeric(frame, amount_cols)
    total = numeric.sum() / 1e9
    values = {name: float(total[col]) for name, col in (FUNCTIONS | REVENUES).items()}
    if not math.isclose(sum(values[x] for x in FUNCTIONS), values["total_expenses"], abs_tol=1e-9):
        raise ValueError("[BLOCKED] finance functions do not close to total expenses")
    return values, len(frame), {
        "finance_archive_sha256": sha(archive), "finance_csv_sha256": sha(finance),
        "institution_header_sha256": sha(HD), "bea_sha256": sha(bea),
        "fee_lines_sha256": sha(FEES),
        "dictionary_archive_sha256": sha(dictionary),
        "not_applicable_zero_counts": {k: n for k, n in not_applicable.items() if n},
    }


def finance_numeric(frame, amount_cols):
    numeric = frame[sorted(amount_cols)].apply(pd.to_numeric, errors="raise")
    not_applicable = {}
    for column in numeric:
        missing = numeric[column].isna()
        if not frame.loc[missing, "X" + column].eq("A").all():
            raise ValueError(f"[BLOCKED] missing applicable finance values in {column}")
        # The dictionary's A flag means Not applicable. This is distinct from
        # institution blank (B), unknown (D), or unusable (H), which must stop.
        not_applicable[column] = int(missing.sum())
        numeric[column] = numeric[column].fillna(0.0)
    return numeric, not_applicable


def bridge(values, *, public_service_in_scope=1.0, other_response=1.0,
           education_sales_to_public_service=0.0, include_auxiliaries=True,
           research_in_consumption=0.0, interest_from_other=False,
           tuition_basis="net_plus_pell"):
    """Conditional net-consumption ratio; own sales respond with their function.

    The function's inputs are all measured totals; flags are named assumptions.
    Research is excluded centrally, not subtracted a second time from NIPA.
    Operating grants are not a sales aggregate and are never blindly netted.
    """
    v = values
    instruction = sum(v[k] for k in ["instruction", "academic_support", "student_support", "institutional_support"])
    other = v["unclassified_other"] - (v["interest"] if interest_from_other else 0.0)
    if other < 0:
        raise ValueError("[BLOCKED] assumed interest assignment exceeds unclassified other")
    ps = public_service_in_scope * v["public_service"]
    research = research_in_consumption * v["research"]
    auxiliary_net = v["auxiliaries"] - v["auxiliary_sales"] if include_auxiliaries else 0.0
    tuition = v["net_tuition"]
    if tuition_basis == "net_plus_pell":
        tuition += v["pell"]
    elif tuition_basis == "gross":
        tuition += v["tuition_discounts"]
    elif tuition_basis != "net":
        raise ValueError(f"[BLOCKED] unknown tuition basis {tuition_basis}")
    ps_sales = min(ps, education_sales_to_public_service * v["education_activity_sales"])
    instruction_sales = v["education_activity_sales"] - ps_sales
    responsive_net = instruction + other_response * other + auxiliary_net - tuition - instruction_sales
    invariant_net = (1.0 - other_response) * other + ps - ps_sales + research
    net = responsive_net + invariant_net
    if net <= 0 or responsive_net < 0 or invariant_net < -1e-12:
        raise ValueError("[BLOCKED] invalid conditional bridge")
    return {
        "response": responsive_net / net, "ipeds_net_bn": net,
        "responsive_net_bn": responsive_net, "invariant_net_bn": invariant_net,
        "instruction_and_support_bn": instruction, "public_service_in_scope_bn": ps,
        "unclassified_other_bn": other, "auxiliary_net_bn": auxiliary_net,
        "tuition_sales_bn": tuition, "public_service_sales_bn": ps_sales,
        "instruction_activity_sales_bn": instruction_sales,
        "research_in_consumption_bn": research,
        "gross_in_scope_bn": instruction + other + ps + research + (v["auxiliaries"] if include_auxiliaries else 0),
        "assumptions": {"public_service_in_scope": public_service_in_scope,
                        "other_response": other_response,
                        "education_sales_to_public_service": education_sales_to_public_service,
                        "include_auxiliaries": include_auxiliaries,
                        "research_in_consumption": research_in_consumption,
                        "interest_from_other": interest_from_other, "tuition_basis": tuition_basis},
    }


def build_item():
    values, units, provenance = load_totals()
    fees = json.loads(FEES.read_text())
    central = bridge(values)
    national = fees["higher_ed"]["higher_dollars_bn"]
    sl_net = fees["nipa"]["consumption_bn"]["higher"]
    primary_nipa = read_primary_nipa()
    for observed, inherited in [(primary_nipa["sl_higher_bn"], sl_net),
                                (primary_nipa["tuition_bn"], fees["nipa"]["tuition_bn"]),
                                (primary_nipa["consolidated_higher_exposure_bn"], national)]:
        if not math.isclose(observed, inherited, abs_tol=1e-9):
            raise ValueError("[BLOCKED] inherited fee exposure differs from primary BEA bridge")
    variants = {
        "central_conditional": {},
        "unclassified_other_fixed": {"other_response": 0},
        "education_sales_public_service": {"education_sales_to_public_service": 1},
        "public_service_outside_education": {"public_service_in_scope": 0},
        "auxiliaries_outside_education": {"include_auxiliaries": False},
        "interest_charged_to_other": {"interest_from_other": True},
        "tuition_net_only": {"tuition_basis": "net"},
        "tuition_all_discounts_added_back": {"tuition_basis": "gross"},
        "research_not_fully_removed_diagnostic": {"research_in_consumption": 1},
    }
    arms = {}
    for name, kwargs in variants.items():
        b = bridge(values, **kwargs)
        b.update(nipa_proportional_scale=sl_net / b["ipeds_net_bn"],
                 national_delta_bn=(b["response"] - 1) * national,
                 capital_response=b["response"])
        arms[name] = b
    central = arms["central_conditional"]
    core = central["instruction_and_support_bn"]
    capital_gross = core + values["research"] + values["public_service"] + values["auxiliaries"] + values["unclassified_other"]
    capital_expense_proxy = (core + values["auxiliaries"] + values["unclassified_other"]) / capital_gross
    return {
        "item": 15, "name": "public_college_response", "status": "conditional_proportional_bridge",
        "central_response": central["response"], "capital_response": central["response"],
        "national_exposure_bn": national,
        "national_delta_bn": central["national_delta_bn"],
        "union_use_share": fees["higher_ed"]["U"],
        "union_operating_delta_bn": central["national_delta_bn"] * fees["higher_ed"]["U"],
        "union_tuition_correction_held_bn": fees["higher_ed"]["fee_term_bn"],
        "apply_to": {"spending_parent": "education_services", "spending_key": "education_mix",
                     "college_reblend_line": "college_rekey", "capital_components": ["college", "college_user_fees"],
                     "pell_excluded": "other_federal_benefits", "tuition_response": 1,
                     "formula": "delta=(response-1)*college_gross_use_key*national_net_consumption; fee correction held fixed"},
        "national_exposure_source": "user_fee_allocation_2026_10_07/derived/fee_lines.json higher_ed.higher_dollars_bn; BEA T3.16 line108 plus allocated federal education",
        "bridge": central, "arms": arms,
        "capital_expense_mix_arm": {"response": capital_expense_proxy, "gross_denominator_bn": capital_gross,
                                     "rule": "research/public service fixed; instruction/support/auxiliaries/other responsive; expense mix proxies asset use"},
        "measured_totals_bn": values, "finance_units": units,
        "primary_nipa_bn": primary_nipa,
        "scope": {"year": "FY2022-23", "public_gasb_50_states_dc": True,
                  "research": "excluded centrally as investment/sales; diagnostic arm is not a recommended second subtraction",
                  "hospitals_net_bn_outside_education": values["hospitals"] - values["hospital_sales"],
                  "operating_grants_bn_not_treated_as_sales": sum(values[x] for x in ["federal_operating_grants", "state_operating_grants", "local_private_operating_grants"])},
        "transport": {"union": "existing measured IPEDS/ACS use share",
                      "added_descendants": "apply same response to their existing college-use amount, not union U to all descendants",
                      "completion": "existing college capital-use key isolates its college-use amount; do not scale school/library amounts",
                      "coverage": "apply to existing college-use pricing; fees/Pell remain fixed; use typed college capital key to recover exposure",
                      "capital": "apply capital_response to whole college component including user-fee offset, completion and coverage; hold stock/key/rate fixed"},
        "limits": ["No causal enrollment response estimated: functional responses are the parent rule.",
                   "Proportional transport from FY2023 GASB net mix to 2024 NIPA is an assumption, not an exact accounting reconciliation.",
                   "Central counts all separately budgeted public service inside higher education although agricultural extension is excluded by Census.",
                   "Central assigns unclassified other response1; its composition and functional interest allocation are not identified.",
                   "Educational-activity sales may belong to public service/research as well as instruction; explicit arm moves them.",
                   "Capital same-split rule is imposed; physical research facilities can remain even when R&D production is excluded from consumption.",
                   "No source-specific state enrollment formula was verified for public-service or research budgets.",
                   "Tuition basis net+Pell and all-education NIPA tuition inherit the adopted fee lane; no Pell transfer is assigned college response."],
        "provenance": provenance,
        "sources": ["https://nces.ed.gov/ipeds/datacenter/data/F2223_F1A.zip",
                    "https://nces.ed.gov/ipeds/datacenter/data/F2223_F1A_Dict.zip",
                    "https://www.bea.gov/resources/methodologies/nipa-handbook/pdf/chapter-09.pdf",
                    "https://www2.census.gov/govs/pubs/classification/2006_classification_manual.pdf"],
    }


def read_primary_nipa():
    """Reproduce the adopted fee lane's exposure from the pinned primary workbook."""
    path = REPO / "sources/immigration-fiscal/data/external/bea_nipa/Section3All_xls.xlsx"
    book = openpyxl.load_workbook(path, read_only=True, data_only=True)
    tables = {}
    for name in ["T31005-A", "T31600-A", "T31700-A", "T31200-A"]:
        rows = list(book[name].values)
        header = next(row for row in rows if row[0] == "Line")
        year = next(i for i, value in enumerate(header) if str(value) == "2024")
        tables[name] = {int(row[0]): (str(row[1]).strip(), row[year] / 1000)
                        for row in rows if str(row[0]).isdigit() and isinstance(row[year], (int, float))}
    book.close()

    def cell(sheet, line, prefix):
        label, value = tables[sheet][line]
        if not label.startswith(prefix):
            raise ValueError(f"[BLOCKED] BEA {sheet}:{line} label changed")
        return value

    higher = cell("T31600-A", 108, "Higher")
    libother = cell("T31600-A", 109, "Libraries and other") - cell("T31200-A", 40, "Education")
    fed = cell("T31700-A", 9, "Education") - cell("T31700-A", 30, "Education")
    fed_k12 = cell("T31600-A", 31, "Elementary and secondary") - cell("T31600-A", 107, "Elementary and secondary")
    return {"sl_higher_bn": higher, "tuition_bn": cell("T31005-A", 58, "Tuition"),
            "consolidated_higher_exposure_bn": higher + (fed - fed_k12) * higher / (higher + libother)}


def main():
    started = time.perf_counter()
    item = build_item()
    out = HERE / "derived"
    out.mkdir(exist_ok=True)
    (out / "item15.json").write_text(json.dumps(item, indent=2, sort_keys=True, allow_nan=False) + "\n")
    with (out / "college_bridge_arms.csv").open("w", newline="") as stream:
        writer = csv.writer(stream, lineterminator="\n")
        writer.writerow(["arm", "response", "capital_response", "ipeds_net_bn", "invariant_net_bn", "nipa_scale", "national_delta_bn"])
        for name, arm in item["arms"].items():
            writer.writerow([name, arm["response"], arm["capital_response"], arm["ipeds_net_bn"], arm["invariant_net_bn"], arm["nipa_proportional_scale"], arm["national_delta_bn"]])
    print(json.dumps({"response": item["central_response"], "union_delta_bn": item["union_operating_delta_bn"],
                      "elapsed_seconds": time.perf_counter() - started,
                      "max_rss_bytes": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}, sort_keys=True))


if __name__ == "__main__":
    main()
