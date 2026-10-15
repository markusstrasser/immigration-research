"""Mexican payroll ownership and G3+ projections from one set of statutory cells.

Native-First: numerical helpers shared by existing Mexico/G2/world builders; no new route.
The caller supplies the existing pinned-statute Mexico module and a numeric PPP divisor.
"""
import numpy as np
import pandas as pd


# Ownership, not the identity of the remitter, controls tax/asset treatment. Government
# financing is classified here but is never a member-paid receipt: its public-budget
# source is already part of Mexico's health/service spending. Cuota social is a public
# transfer into a worker's account, not remuneration paid by the employer.
RECEIPTS = {
    "income_tax": ("pooled_public", "mexico_public", "worker", "LISR96"),
    "employee_health_excess": ("pooled_public", "mexico_public", "worker", "LSS106II"),
    "employee_health_cash": ("pooled_public", "mexico_public", "worker", "LSS107"),
    "employee_pension_medical": ("pooled_public", "mexico_public", "worker", "LSS25"),
    "employee_disability_life": ("pooled_public", "mexico_public", "worker", "LSS147"),
    "employee_ceav": ("worker_asset", "worker", "worker", "LSS168IIb,169"),
    "employer_health_fixed": ("pooled_public", "mexico_public", "employer", "LSS106I"),
    "employer_health_excess": ("pooled_public", "mexico_public", "employer", "LSS106II"),
    "employer_health_cash": ("pooled_public", "mexico_public", "employer", "LSS107"),
    "employer_pension_medical": ("pooled_public", "mexico_public", "employer", "LSS25"),
    "employer_disability_life": ("pooled_public", "mexico_public", "employer", "LSS147"),
    "employer_work_risk": ("pooled_public", "mexico_public", "employer", "LSS74"),
    "employer_daycare": ("pooled_public", "mexico_public", "employer", "LSS211"),
    "employer_employee_health_excess": ("pooled_public", "mexico_public", "employer", "LSS36,106II"),
    "employer_employee_health_cash": ("pooled_public", "mexico_public", "employer", "LSS36,107"),
    "employer_employee_pension_medical": ("pooled_public", "mexico_public", "employer", "LSS36,25"),
    "employer_employee_disability_life": ("pooled_public", "mexico_public", "employer", "LSS36,147"),
    "employer_sar": ("worker_asset", "worker", "employer", "LSS168I,169"),
    "employer_ceav": ("worker_asset", "worker", "employer", "LSS168IIa,169"),
    "employer_employee_ceav": ("worker_asset", "worker", "employer", "LSS36,168IIb,169"),
    "employer_housing": ("worker_asset", "worker", "employer", "INFONAVIT29II"),
    "employer_state_payroll": ("pooled_public", "mexico_public", "employer", "state_payroll_2024"),
    "government_health_fixed": ("pooled_public", "mexico_public", "government", "LSS106III"),
    "government_health_cash": ("pooled_public", "mexico_public", "government", "LSS107"),
    "government_pension_medical": ("pooled_public", "mexico_public", "government", "LSS25"),
    "government_disability_life": ("pooled_public", "mexico_public", "government", "LSS148"),
    "government_cuota_social": ("worker_asset", "worker", "government", "LSS168IV,169"),
}


def gate(name, ok, **detail):
    if not ok:
        raise SystemExit(f"[BLOCKED] gate {name} failed: {detail}")


def receipt_rows(components):
    """Reject unclassified components; retain owner and remitter on each peso flow."""
    rows = []
    for name, value in components.items():
        gate("mexico_receipt_component_declared", name in RECEIPTS, component=name)
        cls, owner, remitter, source = RECEIPTS[name]
        gate("mexico_receipt_class_declared", cls in ("pooled_public", "worker_asset"), component=name)
        gate("mexico_receipt_owner_matches_class",
             owner == ("worker" if cls == "worker_asset" else "mexico_public"), component=name)
        amount = np.asarray(value, float)
        gate("mexico_receipt_amount_finite", np.isfinite(amount).all(), component=name)
        rows.append(dict(component=name, receipt_class=cls, owner=owner, remitter=remitter,
                         source=source, amount_mxn=amount,
                         member_paid_tax=cls == "pooled_public" and remitter != "government"))
    return rows


def employer_contributions(m, g, risk_rate=None, full_year=False):
    """One formula for compensation, public quotas and individually owned deposits."""
    g = np.asarray(g, float)
    gate("mexico_employer_pay_finite_nonnegative", np.isfinite(g).all() and (g >= 0).all())
    p = m.employer_parameters()
    risk = p["risk"] if risk_rate is None else float(risk_rate)
    gate("mexico_employer_risk_inside_statute", np.isfinite(risk) and p["risk_min"] <= risk <= p["risk_max"])
    exposure = np.where(g > 0, 1.0, 0.0) if full_year else np.minimum(g / m.MW_YEAR, 1.0)
    # For partial-year pay g / (g / minimum) is algebraically minimum. Computing
    # that quotient introduces a one-ulp error that flips the minimum-wage legal
    # branch. State the exact branch directly; full-year exposure uses the same floor.
    annual = np.where(exposure > 0, np.maximum(g, m.MW_YEAR), 0.0)
    base = np.minimum(annual, p["cap_uma"] * m.UMA_YEAR)
    excess = np.maximum(base - 3 * m.UMA_YEAR, 0.0)
    idx = np.searchsorted(p["ceav_upper_uma"], base / m.UMA_YEAR, side="left") + 1
    ceav = np.where(base <= p["minimum_wage"] * 30.4 * 12, p["ceav_rates"][0], p["ceav_rates"][idx])
    minimum = (g > 0) & (g <= m.MW_YEAR)
    components = {
        "employer_health_fixed": exposure * p["fixed"] * m.UMA_YEAR * (g > 0),
        "employer_health_excess": exposure * p["excess"] * excess,
        "employer_health_cash": exposure * base * p["cash_benefit"],
        "employer_pension_medical": exposure * base * p["pension_medical"],
        "employer_disability_life": exposure * base * p["disability_life"],
        "employer_daycare": exposure * base * p["daycare"],
        "employer_work_risk": exposure * base * risk,
        "employer_employee_health_excess": exposure * np.where(minimum, excess * m.SSC_RATE_SUR, 0),
        "employer_employee_health_cash": exposure * np.where(minimum, base * p["employee_cash"], 0),
        "employer_employee_pension_medical": exposure * np.where(minimum, base * p["employee_pension_medical"], 0),
        "employer_employee_disability_life": exposure * np.where(minimum, base * p["employee_disability_life"], 0),
        "employer_sar": exposure * base * p["retirement"],
        "employer_ceav": exposure * base * ceav,
        "employer_employee_ceav": exposure * np.where(minimum, base * m.AFORE_RATE, 0),
        "employer_housing": exposure * base * p["housing"],
    }
    rows = receipt_rows(components)
    imss = sum(r["amount_mxn"] for r in rows if r["receipt_class"] == "pooled_public")
    retirement = components["employer_sar"] + components["employer_ceav"] + components["employer_employee_ceav"]
    housing = components["employer_housing"]
    total = imss + retirement + housing
    gate("mexico_employer_components_close", np.isfinite(total).all()
         and np.allclose(total, sum(components.values()), rtol=0, atol=1e-7))
    return dict(imss=imss, retirement=retirement, housing=housing, assets=retirement + housing,
                total=total, **components)


def employee_receipts(m, formal_cash_mxn):
    """Match existing mx_withholding exactly; classify employee CEAV by its owner."""
    g = np.asarray(formal_cash_mxn, float)
    p = m.employer_parameters()
    t, s, a = m.mx_withholding(g)
    base = np.minimum(g, 25 * m.UMA_YEAR)
    excess = np.clip(g - 3 * m.UMA_YEAR, 0, 22 * m.UMA_YEAR)
    taxable = g > m.MW_YEAR
    # The component rates are parsed from IMSS Table A.3's employee column. Their sum is
    # the existing pinned OECD aggregate 1.25%; each is pooled, unlike employee CEAV.
    components = dict(income_tax=t, employee_health_excess=np.where(taxable, excess * m.SSC_RATE_SUR, 0),
                      employee_health_cash=np.where(taxable, base * p["employee_cash"], 0),
                      employee_pension_medical=np.where(taxable, base * p["employee_pension_medical"], 0),
                      employee_disability_life=np.where(taxable, base * p["employee_disability_life"], 0), employee_ceav=a)
    rows = receipt_rows(components)
    pooled = sum(r["amount_mxn"] for r in rows if r["member_paid_tax"])
    gate("mexico_employee_public_receipts_close", np.allclose(pooled, t + s, rtol=0, atol=1e-7))
    return rows


def pay_arrays(m, cash_ppp, formal_ppp, divisor, ctax_rate, assets_as_tax=False, isn_rate=0.0):
    """Compensation and avoided pooled taxes from the same statutory wage cells."""
    cash, formal = np.broadcast_arrays(np.asarray(cash_ppp, float), np.asarray(formal_ppp, float))
    gate("mexico_pay_ppp_divisor", np.isfinite(divisor) and divisor > 0, divisor=divisor)
    gate("mexico_state_payroll_rate", np.isfinite(isn_rate) and isn_rate >= 0, rate=isn_rate)
    gate("mexico_formal_pay_subset", np.isfinite(cash).all() and np.isfinite(formal).all()
         and (cash >= 0).all() and (formal >= 0).all() and (formal <= cash + 1e-8).all())
    employer = m.mx_employer_contributions(formal * divisor)
    erows = employee_receipts(m, formal * divisor)
    withheld = sum(r["amount_mxn"] for r in erows if r["member_paid_tax"]) / divisor
    saving = sum(r["amount_mxn"] for r in erows if r["receipt_class"] == "worker_asset") / divisor
    ep, assets, pooled = (employer[k] / divisor for k in ("total", "assets", "imss"))
    state = receipt_rows({"employer_state_payroll": formal * divisor * isn_rate})[0]["amount_mxn"] / divisor
    ep, pooled = ep + state, pooled + state
    tax = withheld + pooled + (assets if assets_as_tax else 0)
    out = dict(inc=cash + ep, cash=cash, formal=formal, employer=ep, assets=assets, withheld=withheld,
               net=cash - withheld - saving, tax=tax, ctax=cash * np.asarray(ctax_rate, float), isn=state)
    gate("mexico_statutory_cells_close", np.allclose(out["inc"] - out["tax"],
         cash - withheld + (0 if assets_as_tax else assets), rtol=0, atol=1e-7))
    return out


def profile_frame(people, upper_arrays, ppp, divisor):
    """Retain per-person wages and weights; nonlinear statute must precede aggregation."""
    q = np.divide(upper_arrays["formal"], upper_arrays["cash"],
                  out=np.zeros(len(people)), where=upper_arrays["cash"] > 0)
    gate("g3_formality_fraction_valid", np.isfinite(q).all() and (q >= 0).all() and (q <= 1 + 1e-8).all())
    out = pd.DataFrame(dict(ppp=ppp, ppp_divisor=divisor, pw=people.pw.to_numpy(float),
                            us_cash=people.earn.to_numpy(float), formal_fraction=np.clip(q, 0, 1)))
    for k, v in upper_arrays.items():
        out[f"upper_{k}"] = np.asarray(v, float)
    return out


def upper_arrays(m, profile, assets_as_tax=False, statutory=True, isn_rate=0.0):
    if not statutory:
        out = {k[6:]: profile[k].to_numpy(float).copy() for k in profile if k.startswith("upper_")}
        if assets_as_tax:
            out["tax"] += out["assets"]
        gate("mexico_state_payroll_rate", np.isfinite(isn_rate) and isn_rate >= 0, rate=isn_rate)
        out["isn"] = out["formal"] * isn_rate
        for k in ("inc", "employer", "tax"):
            out[k] += out["isn"]
        return out
    divisor = profile.ppp_divisor.unique()
    gate("g3_profile_one_numeric_divisor", len(divisor) == 1)
    cash = profile.upper_cash.to_numpy(float)
    rate = np.divide(profile.upper_ctax.to_numpy(float), cash, out=np.zeros(len(profile)), where=cash > 0)
    return pay_arrays(m, cash, profile.upper_formal.to_numpy(float), float(divisor[0]), rate, assets_as_tax, isn_rate)


def zero_arrays(m, profile, us_employer_bn, assets_as_tax=False, statutory=True, isn_rate=0.0):
    """Zero premium on total compensation, including assets; statutory at US-level pay.

    US employer compensation is assigned in proportion to observed G3 cash earnings
    [ASSUMPTION]. Mexican formal cash fractions stay at each sex/age G2 projection
    [ASSUMPTION]. Statutory discontinuities use a two-wage mixture when no exact cash
    wage exists; every tax/deposit is evaluated at those same two statutory cells.
    """
    w, us = profile.pw.to_numpy(float), profile.us_cash.to_numpy(float)
    cash_total = float((w * us).sum()) / 1e9
    gate("g3_us_compensation_inputs", cash_total > 0 and np.isfinite(us_employer_bn) and us_employer_bn >= 0)
    target = us * (1 + us_employer_bn / cash_total)
    if not statutory:
        base = upper_arrays(m, profile, assets_as_tax, statutory=False, isn_rate=isn_rate)
        factor = np.divide(target, base["inc"], out=np.zeros_like(target), where=base["inc"] > 0)
        gate("g3_zero_legacy_positive_projection", ((target == 0) | (base["inc"] > 0)).all())
        out = {k: a * factor for k, a in base.items()}
    else:
        d = profile.ppp_divisor.unique()
        gate("g3_profile_one_numeric_divisor", len(d) == 1)
        divisor, q = float(d[0]), profile.formal_fraction.to_numpy(float)
        # At US-level income use SHCP's top-decile IVA+IEPS+fuel rate. q=0 is
        # explicitly informal; fixed quotas and 25 UMA apply only to q*cash.
        rate = (m.SHCP_IVA[-1] + m.SHCP_IEPS[-1] + m.fuel_ieps_by_decile()[0][-1]) / 100
        lo, hi = np.zeros_like(target), target.copy()
        for _ in range(64):
            mid = (lo + hi) / 2
            total = pay_arrays(m, mid, q * mid, divisor, rate, assets_as_tax, isn_rate)["inc"]
            low = total < target
            lo = np.where(low, mid, lo)
            hi = np.where(low, hi, mid)
        lower = pay_arrays(m, lo, q * lo, divisor, rate, assets_as_tax, isn_rate)
        upper = pay_arrays(m, hi, q * hi, divisor, rate, assets_as_tax, isn_rate)
        width = upper["inc"] - lower["inc"]
        fraction = np.divide(target - lower["inc"], width, out=np.zeros_like(target), where=width > 1e-10)
        gate("g3_zero_statutory_mixture_brackets", (fraction >= -1e-7).all() and (fraction <= 1 + 1e-7).all())
        fraction = np.clip(fraction, 0, 1)
        out = {k: lower[k] + fraction * (upper[k] - lower[k]) for k in lower}
    gate("g3_zero_total_compensation_closes", abs(float((w * (out["inc"] - target)).sum())) / 1e9 <= 1e-9)
    gate("g3_employer_same_cells_close", abs(float((w * (out["inc"] - out["cash"] - out["employer"])).sum()))
         / 1e9 <= 1e-9)
    return out


def aggregate(profile, arrays):
    w = profile.pw.to_numpy(float)
    out = {k: float((w * np.asarray(v, float)).sum()) / 1e9 for k, v in arrays.items()}
    gate("g3_downstream_compensation_closes", abs(out["inc"] - out["cash"] - out["employer"]) <= 1e-9)
    gate("g3_downstream_assets_subset", -1e-9 <= out["assets"] <= out["employer"] + 1e-9)
    return out
