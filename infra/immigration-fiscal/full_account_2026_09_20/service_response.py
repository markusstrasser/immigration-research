"""Category-specific response sensitivities; CBO transfer, not a CBO forecast.

Called by report.py after upstream validation. Hold production assumptions fixed
while varying spending responses; do not equate budget savings with no crowding.
"""
import json
from pathlib import Path

import numpy as np
import openpyxl
import pandas as pd

from builder import sha, verify_export

HERE = Path(__file__).resolve().parent
CBO_URL = "https://www.cbo.gov/publication/61464"
SERVICE_CATEGORIES = {
    "education_services", "public_order_safety", "economic_affairs_services",
    "housing_community_services", "health_services", "recreation_culture",
    "income_security_services",
}
DELAYED = {"economic_affairs_services", "recreation_culture"}


def education_bounds(gross_total, gross_school, current_total):
    """Bounds assume nonnegative component investment; no ethnic split identified."""
    if not 0 < gross_school <= gross_total or not 0 < current_total <= gross_total:
        raise ValueError("Invalid education accounting totals")
    investment = gross_total - current_total
    return max(0., gross_school-investment)/current_total, min(1., gross_school/current_total)


def bea_education(path):
    book = openpyxl.load_workbook(path, read_only=True, data_only=True)
    values = {}
    try:
        for sheet, lines in {"T31505-A": [29, 30, 31, 32], "T31700-A": [9, 113]}.items():
            rows = list(book[sheet].values)
            headers = [r for r in rows if r[0] == "Line"]
            if len(headers) != 1 or rows[1][0] != "[Millions of dollars]":
                raise ValueError("Unexpected BEA units/header")
            years = [i for i, x in enumerate(headers[0]) if str(x) == "2024"]
            if len(years) != 1:
                raise ValueError("Missing or ambiguous BEA year")
            for line in lines:
                matches = [r for r in rows if str(r[0]) == str(line)]
                if len(matches) != 1:
                    raise ValueError("Missing or duplicate BEA line")
                row = matches[0]
                values[f"{sheet}:{line}"] = dict(label=row[1], bn=float(row[years[0]])/1000)
    finally:
        book.close()
    v = {k: x["bn"] for k, x in values.items()}
    if abs(v["T31505-A:29"]-sum(v[f"T31505-A:{n}"] for n in [30, 31, 32])) > .002:
        raise ValueError("Education partition does not reconcile")
    if abs(v["T31505-A:29"]-v["T31700-A:9"]-v["T31700-A:113"]) > .002:
        raise ValueError("Education consumption/investment does not reconcile")
    # Use the exact gross-minus-current residual; reported investment differs by rounding.
    return education_bounds(v["T31505-A:29"], v["T31505-A:30"], v["T31700-A:9"]), values


def responsive_services(services, school_share, school_response, other_education_response,
                        delayed_response):
    if set(services) != SERVICE_CATEGORIES:
        raise ValueError("Missing or unreviewed service category")
    parameters = [school_share, school_response, other_education_response, delayed_response]
    if not np.isfinite(parameters).all() or not all(0 <= x <= 1 for x in parameters):
        raise ValueError("Invalid declared response scenario")
    if not np.isfinite(list(services.values())).all() or min(services.values()) < 0:
        raise ValueError("Invalid service amounts")
    rows = []
    for category, amount in services.items():
        if category == "education_services":
            for name, share, response in [
                ("school_current", school_share, school_response),
                ("other_education_current", 1-school_share, other_education_response),
            ]:
                rows.append(dict(component=name, assigned_bn=amount*share, response=response,
                                 responsive_bn=amount*share*response))
        else:
            response = delayed_response if category in DELAYED else 1.
            rows.append(dict(component=category, assigned_bn=amount, response=response,
                             responsive_bn=amount*response))
    return pd.DataFrame(rows)


def validate_baseline(baseline):
    required = ["allocation", "normalization", "private_plus_receipts_bn", "welfare_bn"]
    if set(required)-set(baseline) or baseline[required].isna().any().any():
        raise ValueError("Incomplete central reference cases")
    expected = {(a, n) for a in ["personal", "shared"] for n in ["cash", "gdp"]}
    observed = set(baseline[["allocation", "normalization"]].itertuples(index=False, name=None))
    if len(baseline) != 4 or observed != expected:
        raise ValueError("Expected allocation by normalization Cartesian product")
    if not np.isfinite(baseline[["private_plus_receipts_bn", "welfare_bn"]].to_numpy()).all():
        raise ValueError("Nonfinite reference amount")
    fixed = {"capital_adjustment": 1., "excluded_capital_owner_share": 0.,
             "public_goods_response": 0., "fiscal_weight": 1.}
    if set(fixed)-set(baseline) or any(not baseline[k].eq(v).all() for k, v in fixed.items()):
        raise ValueError("Reference production or fiscal assumptions changed")


def export_service_response(baseline, out):
    validate_baseline(baseline)
    fiscal = HERE.parent
    spending_path = fiscal/"full_account_spending_2026_09_20/derived/allocations.csv"
    spending_audit_path = verify_export(spending_path)
    spending_audit = json.loads(spending_audit_path.read_text())
    bea_paths = [Path(p) for p in spending_audit["source_hashes"] if Path(p).name == "Section3All_xls.xlsx"]
    if len(bea_paths) != 1:
        raise ValueError("Missing or ambiguous pinned BEA workbook")
    bounds, cells = bea_education(bea_paths[0])
    spending = pd.read_csv(spending_path)
    pools = pd.read_csv(out/"response_pools.csv")
    cases, components = [], []
    specs = [("proportional_reference", "reference", bounds[0], 1., 1., 1.)]
    for label, share in zip(["national_school_share_low", "national_school_share_high"], bounds):
        for school_r in [.63, .66]:
            specs.append(("school_response_only", label, share, school_r, 1., 1.))
            for other_r in [0., 1.]:
                profile = "cbo_category_lag_non_school_full" if other_r else "cbo_category_lag_non_school_fixed"
                specs.append((profile, label, share, school_r, other_r, 0.))
    # Remove the transported education split altogether to expose what rests on other services.
    specs.extend([
        ("education_fixed_diagnostic", "no_education_response", 0., 0., 0., 0.),
        ("education_full_diagnostic", "full_education_response", 0., 1., 1., 0.),
    ])
    for allocation in ["personal", "shared"]:
        s = spending.loc[(spending.scenario_id == "complete_preferred_F_per_capita") &
                         (spending.allocation == allocation) & (spending.response_class == "service")]
        if s.category.duplicated().any():
            raise ValueError("Duplicate service category")
        services = s.set_index("category").target_bn.to_dict()
        p = pools.loc[(pools.receipt_scenario == "cbo_collective") &
                      (pools.spending_scenario == "complete_preferred_F_per_capita") &
                      (pools.allocation == allocation)]
        if len(p) != 1 or not np.isclose(sum(services.values()), p.services_bn.iloc[0]):
            raise ValueError("Service pool mismatch")
        pool = p.iloc[0]
        for number, (profile, split, share, school_r, other_r, delayed_r) in enumerate(specs):
            comp = responsive_services(services, share, school_r, other_r, delayed_r)
            case_id = f"{allocation}_{number}"
            comp["case_id"], comp["allocation"], comp["profile"] = case_id, allocation, profile
            components.append(comp)
            responsive = comp.responsive_bn.sum()
            for b in baseline.loc[baseline.allocation == allocation].itertuples():
                before_services = pool.direct_receipts_bn-pool.transfers_bn+b.private_plus_receipts_bn
                if not np.isclose(before_services-pool.services_bn, b.welfare_bn, atol=1e-7):
                    raise ValueError("Reference fiscal/production bridge failed")
                cases.append(dict(case_id=case_id, allocation=allocation, normalization=b.normalization,
                    profile=profile, education_split=split, school_share=share, school_response=school_r,
                    other_education_response=other_r, delayed_response=delayed_r,
                    services_bn=pool.services_bn, responsive_services_bn=responsive,
                    effective_service_response=responsive/pool.services_bn,
                    before_services_bn=before_services, welfare_bn=before_services-responsive,
                    change_from_reference_bn=pool.services_bn-responsive,
                    capital_adjustment=1., status="TRANSFERRED_SENSITIVITY_NOT_CBO_ESTIMATE"))
    case_frame, component_frame = pd.DataFrame(cases), pd.concat(components, ignore_index=True)
    summary = case_frame.groupby("profile").agg(
        min_welfare_bn=("welfare_bn", "min"), max_welfare_bn=("welfare_bn", "max"),
        min_effective_response=("effective_service_response", "min"),
        max_effective_response=("effective_service_response", "max"), cases=("welfare_bn", "size"))
    outputs = {"service_response_cases": case_frame, "service_response_components": component_frame,
               "service_response_summary": summary.reset_index()}
    for name, frame in outputs.items():
        frame.to_csv(out/f"{name}.csv", index=False)
    inputs = [spending_path, spending_audit_path, bea_paths[0], out/"response_pools.csv",
              out/"headline_cases.csv", out/"welfare_audit.json", HERE/"report.py", Path(__file__)]
    audit = dict(source_hashes={str(p): sha(p) for p in inputs},
        outputs={name: sha(out/f"{name}.csv") for name in outputs}, bea_cells=cells,
        national_school_current_share_bounds=list(bounds), cbo_source=CBO_URL,
        cbo_checked="2026-09-20", school_response_derivation="1-0.37 growth / 1-0.34 decline; not CI",
        school_split="National current-share bounds transported to target; common composition assumption",
        transfer_limits="State/local short-run association applied as all-level category sensitivity; production held fully adjusted",
        exclusions="No surge-specific flight or ELL add-on; no congestion price; no changed taxes or household benefits",
        nonnegative_investment="Bounds require nonnegative component gross investment; includes rounding residual")
    (out/"service_response_audit.json").write_text(json.dumps(audit, indent=2)+"\n")
    return summary.to_dict("index")
