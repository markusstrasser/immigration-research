"""Integration wrapper, currency remains nominal MXN billions.

Call with root's explicit PPP divisor on prem, cash_mx per generation, and
capital_scope='national' or 'urban_100k'. No national composition fallback.
The raw shape comes from the same G1 own-schooling/G2 rearing projection;
G3 uses the G2 sex-age sector/pay ratios. The cash totals calibrate only levels,
never substitute an aggregate national industry share.
"""
from pathlib import Path
import importlib.util
import hashlib
import json
import math
import sys

import numpy as np
import pandas as pd

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
LANE = HERE
INPUTS = HERE / "inputs/capital"
sys.path.insert(0, str(LANE))


def module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec)
    sys.modules[name] = m
    spec.loader.exec_module(m)
    return m


S = module("capital_source_project", HERE / "capital_source.py")
G = module("g2_premium_capital", LANE / "g2_premium.py")


def checked_input(name):
    """Verify exact bytes against this module's own primary/table manifest."""
    pins = json.loads((INPUTS / "capital_pins.json").read_text())
    if name not in pins or "sha256" not in pins[name]:
        raise ValueError(f"[BLOCKED] unpinned capital input {name}")
    path = INPUTS / name
    if not path.is_file():
        raise ValueError(f"[BLOCKED] missing capital input {path}")
    with path.open("rb") as stream:
        actual = hashlib.file_digest(stream, "sha256").hexdigest()
    if actual != pins[name]["sha256"]:
        raise ValueError(f"[BLOCKED] stale capital input {name}: {actual}")
    return path


def check_primary_sources():
    names = ("capital-sat-itg2024-new.pdf", "capital-indetec2025.pdf", "capital-tabasco-law2023.pdf")
    return {name: str(checked_input(name).relative_to(REPO)) for name in names}


def check_comparator_sources(input_dir=None):
    pins = json.loads((INPUTS / "capital_pins.json").read_text())
    for key, record in pins.items():
        if not key.startswith("repo:"):
            continue
        path = REPO / key[5:]
        if input_dir is not None and path.parent == HERE / "derived" and path.name in {"parents_schooling.csv", "mexico_transition.csv"}:
            path = Path(input_dir) / path.name
        if not path.is_file():
            raise ValueError(f"[BLOCKED] missing capital comparator input {path}")
        with path.open("rb") as stream:
            actual = hashlib.file_digest(stream, "sha256").hexdigest()
        if actual != record["sha256"]:
            raise ValueError(f"[BLOCKED] stale capital comparator input {key}")


def projected_shapes(I):
    input_dir = Path(I.get("mexico_input_dir", HERE / "derived"))
    check_comparator_sources(input_dir)
    scope = I.get("capital_scope", "national")
    source = json.loads(checked_input("capital-enigh-cells.json").read_text())
    if scope not in source:
        raise ValueError(f"[BLOCKED] unrecognized capital cell scope {scope}")
    people = I.get("capital_people")
    if people is None:
        if I.get("case") == "oct15":
            raise ValueError("[BLOCKED] oct15 requires explicit completed capital_people frame; legacy CPS loader misses item10")
        people = G.load_asec(I["basis"])
    parents = pd.read_csv(input_dir / "parents_schooling.csv")
    old_derived = G.DERIVED
    try:
        G.DERIVED = input_dir
        trans = G.transitions()
    finally:
        G.DERIVED = old_derived
    sectors = list(pd.read_csv(checked_input("capital-enigh-industry.csv"), dtype={"sector": str}).sector) + ["__TOTAL_CASH__"]
    # GP's public machinery also computes employment/hours outputs; this
    # private call uses only sector wage money arrays. Supply inert auxiliary
    # values on the identical cell keys, avoiding mutable ownership/tax output
    # tables that have no role in this wage projection.
    lookup = {}
    for kind, pre in (("own", ""), ("parents", "y")):
        keys = {tuple([parts[0], parts[1], int(parts[2])])
                for cell in source[scope][kind] for parts in [cell.split("|")]}
        lookup[pre + "emp"] = {key: 0.0 for key in keys}
        lookup[pre + "hrs"] = {key: 0.0 for key in keys}
    for kind, pre in (("own", ""), ("parents", "y")):
        for sector in sectors:
            lookup[pre + "sector_" + sector] = {tuple([parts[0], parts[1], int(parts[2])]): values[sector]
                for cell, values in source[scope][kind].items() for parts in [cell.split("|")]}
    # A private module instance owns G.MONEY: no shared module or file changes.
    old = G.MONEY
    G.MONEY = tuple("sector_" + sector for sector in sectors)
    try:
        g1 = people[people.gen.eq("G1")]
        g2 = people[people.gen.eq("G2")]
        g3 = people[people.gen.eq("G3+")]
        a1 = G.mexico_own_schooling(g1, lookup, .25, False)
        a2 = G.mexico_rearing(g2, parents, trans, lookup, .25, False)
    finally:
        G.MONEY = old
    shapes = {"G1": {}, "G2": {}, "G3+": {}}
    for sector in sectors:
        col = "sector_" + sector
        shapes["G1"][sector] = float((g1.pw * a1[col]).sum())
        shapes["G2"][sector] = float((g2.pw * a2[col]).sum())
        tmp = g2.assign(band=G.band_of(g2.A_AGE), mx=a2[col], us=g2.earn)
        ratio = {key: float(((x.pw_counted if "pw_counted" in x else x.pw) * x.mx).sum()
                           / max(((x.pw_counted if "pw_counted" in x else x.pw) * x.us).sum(), 1.0))
                 for key, x in tmp[tmp.A_AGE.ge(15)].groupby(["sex", "band"])}
        r = np.array([ratio.get((sex, band), np.nan) if age >= 15 else 0.0
                      for sex, band, age in zip(g3.sex, G.band_of(g3.A_AGE), g3.A_AGE)])
        if not np.isfinite(r).all():
            raise ValueError("[BLOCKED] G3 sector projection has missing G2 sex-age ratio")
        shapes["G3+"][sector] = float((g3.pw * g3.earn * r).sum())
    return shapes


def mexico_source_tax(I, prem, end, short_run=False):
    if end not in {"low", "central", "high"}:
        raise ValueError(f"[BLOCKED] unknown premium endpoint {end}")
    check_primary_sources()
    shapes = I.get("capital_projected_gen_industry_wages")
    if shapes is None:
        shapes = projected_shapes(I)
    if set(shapes) != {"G1", "G2", "G3+"}:
        raise ValueError("[BLOCKED] all three generation wage projections required")
    national = pd.read_csv(checked_input("capital-enigh-industry.csv"), dtype={"sector": str}).set_index("sector")
    wages = dict.fromkeys(national.index, 0.0)
    by_gen = {}
    subordinate_fractions = {}
    for gen, values in shapes.items():
        if "cash_mx" not in prem[gen] or "mexico_ppp_divisor" not in prem[gen]:
            raise ValueError(f"[BLOCKED] {gen} needs cash_mx and explicit numeric mexico_ppp_divisor")
        cash = prem[gen]["cash_mx"]
        amount = float(cash["central"] if isinstance(cash, dict) else cash) * float(prem[gen]["mexico_ppp_divisor"]) * 1e9
        if not math.isfinite(amount) or amount < 0 or not math.isfinite(float(prem[gen]["mexico_ppp_divisor"])) or float(prem[gen]["mexico_ppp_divisor"]) <= 0:
            raise ValueError(f"[BLOCKED] invalid nominal cash or PPP divisor {gen}")
        if set(values) != set(wages) | {"__TOTAL_CASH__"}:
            raise ValueError(f"[BLOCKED] missing/extra projected industry {gen}")
        if "__TOTAL_CASH__" not in values:
            raise ValueError("[BLOCKED] matched total-cash projection needed to preserve subordinate wage fraction")
        before = values["__TOTAL_CASH__"]
        subordinate = math.fsum(value for sector, value in values.items() if sector != "__TOTAL_CASH__")
        fraction = subordinate / before if before else 0.0
        if not 0 <= fraction <= 1 + 1e-8:
            raise ValueError(f"[BLOCKED] projected subordinate fraction outside[0,1] {gen}: {fraction}")
        subordinate_fractions[gen] = fraction
        if I.get("capital_use_all_earnings_key", False):
            before = subordinate  # labelled beside; central preserves wage-only key
        if before <= 0 and amount > 0:
            raise ValueError(f"[BLOCKED] empty {gen} sector/pay projection")
        by_gen[gen] = {sector: value * amount / before if before else 0.0
                       for sector, value in values.items() if sector != "__TOTAL_CASH__"}
        expected = amount if I.get("capital_use_all_earnings_key", False) else amount * fraction
        if not math.isclose(math.fsum(by_gen[gen].values()), expected, abs_tol=1e-5, rel_tol=1e-12):
            raise ValueError(f"[BLOCKED] projected sector pay fails cash-fraction closure {gen}")
        for sector, value in by_gen[gen].items():
            wages[sector] += value
    tax = pd.read_csv(checked_input("capital-sat-sector-isr.csv"), dtype={"sector": str})
    pins = json.loads((INPUTS / "capital_pins.json").read_text())
    national_receipts = float(pins["meta"]["corporate_receipts_national_mxn_million"]) / 1e3
    if float(tax.corporate_gains_isr_mxn_million.sum()) != pins["meta"]["sector_sum_mxn_million"]:
        raise ValueError("[BLOCKED] SAT sector transcription does not close to its declared rounded sum")
    identified = {r.sector: r.corporate_gains_isr_mxn_million * 1e6 for r in tax.itertuples()
                  if r.sector not in {"OTHER", "OTHER_AUX"}}
    residual = float(tax[tax.sector.isin(["OTHER", "OTHER_AUX"])].corporate_gains_isr_mxn_million.sum() * 1e6)
    # 55 has just15 observations; explicit services-pool assumption, matching
    # US item6's rule of pooling thin industry cells. Caller may switch off.
    services = [sector for sector in wages if sector in {"51", "52", "53", "54", "55", "56", "61", "62", "71", "72", "81"}]
    pools = services if I.get("capital_pool_thin_services", True) else ()
    premise = "short_run_fixed_capital" if short_run else I.get("capital_premise", "long_run_new_capital")
    result = S.mexico_corporate_source(wages, national.national_wages_mxn.to_dict(), identified, residual,
        residual_policy=I.get("capital_residual_policy", "pooled_private"),
        premise=premise, pool_sectors=pools)
    unpooled = S.mexico_corporate_source(wages, national.national_wages_mxn.to_dict(), identified, residual,
        residual_policy=I.get("capital_residual_policy", "pooled_private"), premise=premise)
    result["thin55_pooling_change_pesos_bn"] = {rd: (result["total"][rd] - unpooled["total"][rd]) / 1e9
                                               for rd in ("low", "high")}
    fiscal_end = I.get("account_end", end)
    if fiscal_end not in {"low", "high"}:
        raise ValueError("[BLOCKED] explicit fiscal account_end low/high needed for capital response")
    reading = fiscal_end
    return {"pesos_bn": result["total"][reading] / 1e9, "by_reading_pesos_bn": {k: v / 1e9 for k, v in result["total"].items()},
            "national_corporate_receipts_pesos_bn": national_receipts,
            "industry_wages_mxn": wages, "generation_industry_wages_mxn": by_gen,
            "raw_subordinate_fractions": subordinate_fractions,
            "receipt_class": "source_tax", "economic_payer": "business capital, corporate labor included once",
            "scope": I.get("capital_scope", "national"), "calculation": result,
            "normalization": "projected sector wages scaled with matched total cash; subordinate wage fraction preserved, selfemployment excluded",
            "all_earnings_beside": bool(I.get("capital_use_all_earnings_key", False)),
            "row_price_basis": "nominal pesos; root must apply explicit funded-services PPP"}


def isn_on_formal_pay(formal_pay_mxn, *, rate_choice):
    """ISN base rates on national ENIGH formal-pay state mix.

    Lower/upper must be explicit while Sinaloa employer aggregate is missing.
    No claim of exact legal effective burden: exemptions and additional taxes
    remain separate. Equal choices coincide for every flat-rate state.
    """
    if rate_choice not in {"lower", "upper"}:
        raise ValueError("[BLOCKED] ISN Sinaloa tariff requires explicit lower/upper rate_choice")
    if not math.isfinite(float(formal_pay_mxn)) or formal_pay_mxn < 0:
        raise ValueError("[BLOCKED] nonfinite/negative ISN pay")
    table = pd.read_csv(checked_input("capital-isn-state-weights.csv"))
    rate = float(table["weighted_rate_low" if rate_choice == "lower" else "weighted_rate_high"].sum())
    return {"isn_mxn": formal_pay_mxn * rate, "rate": rate,
            "state_mix": "national domestic formal-pay mix from ENIGH2024",
            "receipt_class": "pooled_public", "rate_choice": rate_choice,
            "qualification": "statutory base rates; employer aggregate tariff and additional taxes not fully observed"}
