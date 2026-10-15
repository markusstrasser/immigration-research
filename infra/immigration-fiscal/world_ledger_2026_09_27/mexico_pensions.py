"""Primary pension rules, fail-loud basis selection and net public-service-cost inputs.

No histories or pension liabilities are synthesized. Payroll owners/classes have
one canonical definition in mexico_compensation.py; this module adds none.
"""
import hashlib
import json
import math
from pathlib import Path
import re

HERE = Path(__file__).resolve().parent
INPUTS = HERE / "inputs"


class PensionBlocked(ValueError):
    pass


def block(condition, name, **detail):
    if not condition:
        raise PensionBlocked(f"[BLOCKED] {name}: {detail}")


def pinned_text(name, directory=INPUTS):
    manifest = directory / "pension_primary_pins.json"
    block(manifest.is_file(), "primary_manifest_missing", path=str(manifest))
    pins = json.loads(manifest.read_text())["files"]
    block(name in pins and "sha256" in pins[name], "primary_pin_missing", file=name)
    source = directory / name
    block(source.is_file(), "primary_source_missing", file=name)
    body = source.read_bytes()
    block(hashlib.sha256(body).hexdigest() == pins[name]["sha256"], "primary_pin_stale", file=name)
    return " ".join(body.decode("utf-8").split())


def primary_parameters(directory=INPUTS):
    text = pinned_text("pension_imss_annex_2024_2025.txt", directory)
    table = text[text.index("Cuadro A.3."):text.index("Cuadro A.4.")]
    ceav = table[table.index("6/ Con la reforma"):table.index("7/ Con la reforma")]
    first = re.search(r"cuota en 2024 es de ([\d.]+)%", ceav)
    rates = re.findall(r"UMA = ([\d.]+)%", ceav)
    last = re.search(r"UMA en adelante ([\d.]+)%", ceav)
    block(first is not None and last is not None and len(rates) == 6,
          "ceav_eight_tiers_missing")
    social = table[table.index("8/ Con la reforma"):]
    social = social[social.index("de la siguiente manera:"):]
    qs = re.findall(r"= ([\d.]+) pesos", social)
    block(len(qs) == 7, "cuota_social_seven_tiers_missing", values=qs)
    uma = re.search(r"Cifra igual a ([\d.]+) pesos en diciembre de 2024", table)
    employee = re.search(r"Cesantía y Vejez SBC [\d.]+6/ ([\d.]+)", table)
    retiro = re.search(r"Retiro SBC ([\d.]+)", table)
    block(all(x is not None for x in (uma, employee, retiro)), "source_parameters_missing")
    housing = pinned_text("pension_infonavit_law.txt", directory)
    article = housing[housing.index("Artículo 29.-"):housing.index("Artículo 29 Bis.-")]
    block("aportaciones del cinco por ciento" in article
          and "forman parte del patrimonio de los trabajadores" in article,
          "housing_owner_or_rate_not_supported")
    return dict(ceav_employer_rates=[float(x) / 100 for x in [first[1], *rates, last[1]]],
                ceav_employee_rate=float(employee[1]) / 100,
                retiro_employer_rate=float(retiro[1]) / 100,
                ceav_uma_upper=[float(x) for x in re.findall(r"a ([\d.]+) UMA =", ceav)],
                cuota_social_daily_mxn=[float(x) for x in qs],
                cuota_social_vintage="December 2024, not annual average",
                uma_daily_mxn=float(uma[1]), housing_employer_rate=0.05,
                annual_warning="January UMA differs; cuota social is quarterly indexed; supply days and vintages for exact annual amount")


def ownership_delta(deposit_bn, mexico_weight=1.0, worker_weight=1.0):
    block(all(math.isfinite(x) for x in (deposit_bn, mexico_weight, worker_weight)), "nonfinite_ownership_delta")
    return dict(mexico_residents=deposit_bn, group=-deposit_bn, other_us_residents=0.0,
                world=deposit_bn * (mexico_weight - worker_weight))


ACCRUAL_FIELDS = {
    "record_id", "generation", "sex", "age", "weight", "scheme", "first_covered_date",
    "covered_days_2024_by_quarter", "sbc_daily_2024_by_quarter", "credited_weeks_start",
    "credited_weeks_end", "lifetime_sbc_history", "last_250_weeks_sbc_history",
    "afore_rcv_balance_start", "afore_rcv_balance_end", "ceav_balance_start",
    "ceav_balance_end", "law1973_election", "retirement_age", "beneficiary_history",
}
ACCRUAL_METADATA = {
    "source_provenance", "counterfactual_history_rule", "mortality_table",
    "discount_rule", "guarantee_table_2024", "guarantee_index_rule",
    "asset_returns_and_fees", "service_cost_attribution_rule", "ceav_surrender_rule",
    "non_imss_scheme_rule", "pensioner_health_rule", "payment_vs_revaluation_bridge",
}


def pension_basis(mode, us_basis, records=None, metadata=None, allow_p032_proxy=False):
    block(mode in {"full_accrual", "matched_cash"}, "unknown_pension_basis", mode=mode)
    block(us_basis == ("accrual" if mode == "full_accrual" else "cash"),
          "mixed_us_mexico_pension_bases", mode=mode, us_basis=us_basis)
    if mode == "full_accrual":
        block(records is not None and len(records) > 0, "mexico_accrual_histories_missing",
              recommendation="matched_cash; do not infer history from age or current formality")
        missing = {i: sorted(ACCRUAL_FIELDS - set(r)) for i, r in enumerate(records)
                   if ACCRUAL_FIELDS - set(r)}
        block(not missing, "mexico_accrual_fields_missing", records=missing)
        missing_meta = sorted(ACCRUAL_METADATA - set(metadata or {}))
        block(not missing_meta, "mexico_accrual_assumptions_missing", fields=missing_meta)
        block(all(r[k] is not None for r in records for k in ACCRUAL_FIELDS),
              "mexico_accrual_null_history")
        return dict(mode=mode, status="input contract complete; actuarial computation still required")
    block(allow_p032_proxy or (metadata or {}).get("public_pension_cash_split") is not None,
          "mexico_cash_public_funding_unidentified",
          recommendation="explicit allow_p032_proxy=True labels the existing all-public proxy; otherwise supply public cash split")
    return dict(mode=mode, status="[DEGRADED] P032 all-public cash proxy" if allow_p032_proxy else "public cash split supplied",
                us_action="revalue exact PACKAGE.CASH generation lines, including benefit-tax receipts; reconcile fiscal channels",
                mexico_action="keep P032 on cash; P104/P045/P105 stay in BENE_GOB; no additional accrual promises")


def net_public_service_cost(promise_service_cost_mxn, ceav_funding_service_mxn, cuota_social_paid_mxn):
    """All arguments must be supplied by a documented actuarial engine, not imputed here.

    1973 CEAV surrender is funding for the promise. Cuota social is already credited
    in current account deposits; do not add its projected pension payout a second time.
    """
    block(all(math.isfinite(x) for x in (promise_service_cost_mxn, ceav_funding_service_mxn, cuota_social_paid_mxn)),
          "nonfinite_public_pension_service_cost")
    block(ceav_funding_service_mxn >= 0 and cuota_social_paid_mxn >= 0,
          "negative_public_pension_funding")
    return promise_service_cost_mxn - ceav_funding_service_mxn + cuota_social_paid_mxn
