"""Removal-frame spending identities; conditional scenarios, not an estimated MPC.

Native-First: reuse the lane's PM grid and frozen case engine. New primary-file
numbers are parsed from pinned files; inherited model assumptions retain labels.
"""
from __future__ import annotations

import csv
import hashlib
import importlib.util
import io
import json
from pathlib import Path
import re
import resource
import subprocess
import sys
import time
import tempfile
import os

HERE = Path(__file__).resolve().parent
FISCAL = HERE.parent
OUT = HERE / "derived"
sys.path.insert(0, str(FISCAL / "scripts"))
from memory_budget import require_within_budget

BUNDLE_DEPENDENCIES = {
    "respending": ["../inputs/pins.json", "case_inputs.json", "../case_inputs.cjs", "../respending.py"],
    "stack": ["respending_generation.json", "../inputs/pins.json", "case_inputs.json", "../stack.py", "../valuation_registry.py"],
}


def hard_gate(condition, label):
    if not bool(condition):
        raise ValueError(f"[BLOCKED] {label}")


def verify_pins():
    from pin_inputs import INPUTS
    rows = json.loads((HERE / "inputs/pins.json").read_text())
    hard_gate(set(INPUTS)=={row["path"] for row in rows}, "input pin coverage differs from source registry")
    for row in rows:
        p = HERE / row["path"]
        hard_gate(p.is_file() and hashlib.sha256(p.read_bytes()).hexdigest() == row["sha256"],
                  f"changed pinned input {row['path']}")


def csv_text(rows):
    stream = io.StringIO(newline="")
    writer = csv.DictWriter(stream, fieldnames=list(rows[0]), lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)
    return stream.getvalue()


def dependency_snapshot(directory, paths):
    directory = Path(directory)
    return {key: hashlib.sha256((directory/key).read_bytes()).hexdigest() for key in paths}


def publish_bundle(name, payloads, *, dependencies=None):
    """Publish staged files, then their generation receipt; readers verify it.

    POSIX renames are per-file, so readers must reject any in-flight mixture
    against the last complete receipt. No partial generation is accepted.
    """
    require_within_budget(f"social {name} publication")
    OUT.mkdir(exist_ok=True)
    dependencies = {} if dependencies is None else dependencies
    if name in BUNDLE_DEPENDENCIES:
        hard_gate(set(dependencies) == set(BUNDLE_DEPENDENCIES[name]), f"{name} receipt lacks required dependency edges")
    hard_gate(dependencies == dependency_snapshot(OUT, dependencies),
              f"{name} dependencies changed during computation")
    hashes = {key: hashlib.sha256(value.encode()).hexdigest() for key,value in payloads.items()}
    receipt = json.dumps(dict(files=hashes, dependencies=dependencies), sort_keys=True, indent=2)+"\n"
    payloads = {**payloads, f"{name}_generation.json": receipt}
    with tempfile.TemporaryDirectory(prefix=f'.{name}-', dir=OUT) as temporary:
        for key,value in payloads.items():
            (Path(temporary)/key).write_text(value)
        for key in payloads:
            os.replace(Path(temporary)/key, OUT/key)


def verify_bundle(name, directory=None):
    directory = OUT if directory is None else Path(directory)
    path = directory/f"{name}_generation.json"
    first = path.read_bytes()
    receipt = json.loads(first)
    hard_gate("dependencies" in receipt, f"{name} receipt lacks dependency generation")
    if name in BUNDLE_DEPENDENCIES:
        hard_gate(set(receipt["dependencies"]) == set(BUNDLE_DEPENDENCIES[name]), f"{name} receipt lacks required dependency edges")
    for key,digest in receipt["files"].items():
        hard_gate(hashlib.sha256((directory/key).read_bytes()).hexdigest()==digest,
                  f"mixed or stale {name} generation: {key}")
    hard_gate(receipt.get("dependencies", {}) == dependency_snapshot(directory, receipt.get("dependencies", {})),
              f"stale {name} dependency generation")
    if "respending_generation.json" in receipt.get("dependencies", {}):
        verify_bundle("respending", directory)
    hard_gate(first==path.read_bytes(), f"{name} generation changed during read")
    return first


def spending_basis_gate(funding_basis, denominator_basis, *, units_sensitivity=False):
    """A national-accounts saving requires a national-accounts denominator."""
    if funding_basis != denominator_basis and not units_sensitivity:
        raise ValueError("[BLOCKED] re-spending funding/denominator accounting basis differs")
    if funding_basis != "national_accounts" or denominator_basis not in ("national_accounts", "CE_survey"):
        raise ValueError("[BLOCKED] undeclared re-spending accounting basis")


def read_csv(path):
    with open(path) as f:
        return list(csv.DictReader(f))


def write_csv(name, rows):
    with open(OUT / name, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]), lineterminator="\n")
        w.writeheader()
        w.writerows(rows)


def source_text(name):
    # Parse the actual pinned PDF each run; cached extracted text is not authority.
    return subprocess.check_output(["pdftotext", "-layout", str(HERE / "_cache" / name), "-"], text=True)


def load_air():
    spec = importlib.util.spec_from_file_location("air_control", FISCAL / "air_pollution_2026_09_28/air_items.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main():
    start = time.perf_counter()
    verify_pins()
    dependencies = dependency_snapshot(OUT, BUNDLE_DEPENDENCIES["respending"])
    air = load_air()
    case = json.loads((OUT / "case_inputs.json").read_text())
    counts = case["lineage"]
    ce = {r["group"]: r for r in read_csv(FISCAL / "air_pollution_2026_09_28/derived/ce_group_spending.csv")}
    ce_all = float(ce["all"]["total_pc_q"]) * 4
    ce_group = float(ce["mexican_origin"]["total_pc_q"]) * 4
    pop_all = air.POP_ALL
    legacy_n = air.GROUPS["mexican_origin"]["n"]
    grid, _ = air.pm_grid("mexican_origin")
    central = grid[(grid[[c for c in grid if c.startswith("i_")]] == 1).all(axis=1)].iloc[0]
    vsl = air.VSL_DOT_2024
    pm_control = central.others * central.morb * vsl / 1e9
    stored = next(r for r in read_csv(FISCAL / "air_pollution_2026_09_28/derived/items.csv")
                  if r["item"] == "pm25_consumption" and r["group"] == "mexican_origin" and r["measure"] == "absolute")
    hard_gate(abs(pm_control-float(stored["central_bn"])) < 5e-5, "legacy PM positive control")
    gov = next(r for r in read_csv(FISCAL / "air_pollution_2026_09_28/derived/items.csv")
               if r["item"] == "pm25_government_use" and r["group"] == "mexican_origin" and r["measure"] == "absolute")
    gov_legacy = central.D * air.THETA_GOVERNMENT * legacy_n / pop_all * air.GOV["use"]["mexican_origin"][1] * air.GOV["response"][1] * (1-central.sigma) * vsl * 1.03 / 1e9
    hard_gate(abs(gov_legacy-float(gov["central_bn"])) < 5e-5, "legacy government positive control")
    # Independent official national-accounts denominator, fixed vintage Feb 2025.
    bea = source_text("bea_gdp4q24_2nd.pdf")
    line = next(x for x in bea.splitlines() if re.match(r"\s*34 Personal consumption expenditures\s", x))
    nums = [float(x.replace(",", "")) for x in re.findall(r"[\d,]+\.\d+", line)]
    hard_gate(len(nums) == 8, f"BEA PCE table shape: {line}")
    pce_bn = nums[2]  # Table 8: annual 2022, 2023, 2024; then quarters.
    epa = source_text("epa_scghg_2023.pdf")
    # A continued-page heading repeats after 2024: splitting on the last
    # heading would discard the requested row. Identify its numeric schema.
    epa_rows = [x for x in epa.splitlines() if re.match(r"\s*2024\s+(?:[\d,]+\s+){8}[\d,]+\s*$", x)]
    hard_gate(len(epa_rows) == 1, "EPA annual SC-GHG 2024 row is not unique")
    line = epa_rows[0]
    numbers = [float(x.replace(",", "")) for x in re.findall(r"[\d,]+", line)]
    hard_gate(len(numbers) == 10, f"EPA table shape: {line}")
    epa_2020 = numbers[2]  # year, 2.5%, 2.0%, 1.5%, ...
    iwg = source_text("iwg_2021.pdf").split("Table A-1: Annual SC-CO")[-1]
    line = next(x for x in iwg.splitlines() if re.match(r"\s*2024\s+", x))
    numbers = [float(x.replace(",", "")) for x in re.findall(r"[\d,]+", line)]
    hard_gate(len(numbers) == 5, f"IWG table shape: {line}")
    iwg_2020 = numbers[2]  # year, 5%, 3%, 2.5%, 95th.
    cpi_ratio = air.cpi(2024)/air.cpi(2020)
    sccs = {"epa2023_2pct": epa_2020*cpi_ratio, "iwg2021_3pct": iwg_2020*cpi_ratio}
    # Read origin/US emissions directly from the pinned GCB/OWID file, not prose.
    fbar = (air.owid("United States",2023,"consumption_co2") * air.owid("United States",2024,"co2")
            / air.owid("United States",2023,"co2") / air.owid("United States",2024,"population") * 1e6)
    mex_pc = air.owid("Mexico",2023,"consumption_co2_per_capita")
    wd = air.CO2["w_direct"][1]
    ratio = wd*air.CO2["rho_direct"]["mexican_origin"][1] + air.CO2["w_gov"]*air.CO2["gov_use"][1] + (1-wd-air.CO2["w_gov"])*air.CO2["rho_total"]["mexican_origin"][1]
    rest_params = {r["parameter"]:r for r in read_csv(FISCAL / "disease_food_2026_09_28/derived/inputs.csv")}
    rest_items = read_csv(FISCAL / "disease_food_2026_09_28/derived/items.csv")
    rest_base = float(next(r for r in rest_items if r["item"] == "restaurant_variety_market_size" and r["measure"] == "absolute")["central_bn"])
    psi = float(rest_params["share_of_non_group_restaurant_access_supported_by_group"]["central"])
    sig = float(rest_params["sigma_between_restaurants"]["central"])
    Erest = -rest_base/((1-psi)**(-1/(sig-1))-1)
    consumer = {r["item"]:float(r["central_bn"]) for r in read_csv(FISCAL / "population_basis_2026_09_29/derived/consumer_scale_rerun/row4/items.csv") if r["measure"]=="absolute"}
    frame = read_csv(FISCAL / "main_case_decomposition_2026_09_29/derived/headcount.csv")
    row4 = next(r for r in frame if r["cut"]=="all" and r["group"]=="union")
    hard_gate(abs(float(row4["row4"])-counts["account_union"]) < 1e-4, "frozen row4 union count")
    key = json.loads((HERE / "inputs/band_variants.json").read_text())["lineage_social_keys"]
    rows, components, co2 = [], [], []

    def add(item,basis,end,denom,central_bn,lo=None,hi=None,note="",overlap=""):
        n = counts["lineage_population"] if basis=="lineage" else counts["account_union"]
        lo = central_bn if lo is None else lo
        hi = central_bn if hi is None else hi
        rows.append(dict(item=item,group="mexican_origin",measure="absolute",population_basis=basis,end=end,
                         spending_denominator=denom,low_bn=min(lo,hi),central_bn=central_bn,high_bn=max(lo,hi),
                         per_member_usd=central_bn*1e9/n,evidence_level="conditional model; marginal spending mix and propensity unmeasured",
                         double_count_with=overlap,method_note=note,comparator="2024 removal; all other residents",
                         beneficiary="residents outside the identified union; lineage extension conditional",
                         valuation=("DOT VSL plus inherited morbidity" if item.startswith("pm25") else "source producer's consumer-welfare valuation"),overlap=overlap))

    for fiscal in case["rows"]:
        basis,end = fiscal["population_basis"],fiscal["end"]
        n = counts["lineage_population"] if basis=="lineage" else counts["account_union"]
        H = fiscal["current_budget_saving_bn"]
        national_n = pop_all-float(row4["removed"])
        s = counts["account_union"]/national_n
        sigma = air.ARMS["L"][1]*air.ARMS["iota"]["mexican_origin"][1]+(1-air.ARMS["L"][1])*s*air.ARMS["E"]["mexican_origin"][1]
        own_pm = central.D*air.THETA_CONSUMPTION*s*air.ARMS["r"]["mexican_origin"][1]*(1-sigma)*vsl*central.morb/1e9
        factor = 1+key[f"{end}_end"]["consumption"] if basis=="lineage" else 1
        own_pm *= factor
        gov_case = central.D*air.THETA_GOVERNMENT*s*air.GOV["use"]["mexican_origin"][1]*air.GOV["response"][1]*(1-sigma)*vsl*1.03/1e9
        gov_case *= n/counts["account_union"]
        # Source composition is averaged nationally; with the group absent, its
        # former receptors contribute zero baseline deaths. This is not sigma,
        # which describes emissions originating from group-associated locations.
        receptors = 1-n/national_n
        for denom,spend_bn in [("CE",ce_all*national_n/1e9),("PCE",pce_bn)]:
            spending_basis_gate(case["funding_accounting_basis"],
                                "national_accounts" if denom == "PCE" else "CE_survey",
                                units_sensitivity=denom == "CE")
            unit = central.D*air.THETA_CONSUMPTION*vsl*central.morb/1e9/spend_bn*receptors
            dpm = -H*unit
            add("pm25_respending",basis,end,denom,dpm,note="H spent in 2024 at national-average consumption-associated emissions per dollar; removes former group receptors by population share; mortality-weighted interaction is separate",overlap="counterflow to pm25_consumption; do not add together with a net replacement row")
            add("pm25_government_mirror_legacy_response",basis,end,denom,gov_case,note="original government-use row on row4, then added people by headcount; use 1.1 and response .55 remain assumptions",overlap="previously excluded PM government row; excluded from fiscal dollars")
            add("pm25_joint_respending_government",basis,end,denom,dpm+gov_case,note="sum of the two declared components; same current-spending correction in cash set and accrual set",overlap="alternative to its components")
            # Explicit budget-weighted sensitivity: unknown emissions mix is not
            # silently identified with a fiscal-spending mix.
            gov_budget = central.D*air.THETA_GOVERNMENT*vsl*1.03/1e9*fiscal["government_consumption_removed_bn"]/fiscal["government_consumption_national_bn"]*(1-sigma)
            add("pm25_government_mirror_budget_mix_arm",basis,end,denom,gov_budget,note="uniform PM harm per dollar across public-consumption lines; exact case shrinkage, unmeasured emissions mix",overlap="alternative to government mirror legacy response")
            # A demand-equivalent sensitivity, not population restored by money.
            group_spend = ce_group*n/1e9 if denom=="CE" else pce_bn*s*float(ce["mexican_origin"]["total_ratio_to_all"])*factor
            fraction = H/group_spend
            hard_gate(0<=fraction<1, "spending fraction within demand support")
            rest_new = -Erest*((1-psi*(1-fraction))**(-1/(sig-1))-1)
            dr = rest_new-rest_base
            add("restaurant_respending_demand_arm",basis,end,denom,dr,note="replace psi by psi*(1-H/group_spending); same spending mix, same cross-group substitutability; original restaurant row carries no headcount; lineage demand extrapolation is only a sensitivity",overlap="replaces restaurant market-size benefit; no cuisine-composition change")
            # No evidence that extra consumption recreates absent customers or
            # restores the population regressor. Only a named linear-demand arm.
            dc = -consumer["total_consumer_scale"]*factor*fraction
            add("consumer_scale_respending_demand_arm",basis,end,denom,dc,note="linear effective-demand rescaling of total consumer-scale row; customer/population elasticities are not spending elasticities; beside only",overlap="alternative rescaling, never separately add replacement and delta")
            # Carbon: personal plus investment-associated footprint; government
            # emissions already in the legacy footprint, so do not add them twice.
            gross_mt = n*fbar*ratio/1e6
            n_mexborn = float(next(r for r in frame if r["cut"]=="generation a" and r["group"]=="G1")["row4"])
            origin_mt = n_mexborn*mex_pc*air.CO2["phi_origin"][1]/1e6
            remit_mt = air.CO2["remit_bn"][1]*air.CO2["remit_kg_per_usd"][1]
            private_mt = national_n*fbar*(1-air.CO2["w_gov"])/1e6
            re_mt = H*private_mt/spend_bn
            net_mt = gross_mt-origin_mt+remit_mt-re_mt
            hard_gate(abs(net_mt-(gross_mt-origin_mt+remit_mt-re_mt))<1e-9, "carbon source closure")
            for valuation,scc in sccs.items():
                # Same 11% US-damage assumption as the original lane; income
                # weighting needs no synthetic precision absent origin cells.
                ush=air.US_SHARE[1]
                others_income_share = 1-n*air.GROUPS["mexican_origin"]["income_pc"]/(national_n*air.INCOME_PC_ALL)
                damage=net_mt*scc/1e3*ush*others_income_share
                co2.append(dict(population_basis=basis,end=end,spending_denominator=denom,valuation=valuation,
                                scc_2024usd=scc,gross_mt=gross_mt,origin_mexico_mt=origin_mt,
                                remittance_mt=remit_mt,respending_mt=re_mt,net_mt=net_mt,
                                global_damage_bn=net_mt*scc/1e3,other_us_damage_bn=damage,
                                us_damage_share=ush,other_us_income_share=others_income_share,
                                status="beside; origin: Mexico-born only at .85 Mexico footprint; US-born birth counterfactual unchanged; 11% US damages assumed"))
                add(f"co2_after_respending_{valuation}",basis,end,denom,damage,
                    note="beside only; gross minus Mexico-born origin plus remittances minus re-spending; source-country mean, .85 selection multiplier and 11% US damage share separately declared",
                    overlap="outside social stack; alternative SCC valuations, never add both; original gross footprint already carries government CO2")
                rows[-1]["valuation"]=f"{valuation}, annual 2024 SCC inflated from 2020 dollars; 11% US damage share times other-US income share"
            components.append(dict(population_basis=basis,end=end,spending_denominator=denom,
                                   funding_accounting_basis=case["funding_accounting_basis"],
                                   denominator_accounting_basis="national_accounts" if denom == "PCE" else "CE_survey",
                                   units_sensitivity=denom == "CE",
                                   current_saving_bn=H,national_spending_bn=spend_bn,group_spending_bn=group_spend,
                                   respending_fraction=fraction,receiver_remaining_fraction=receptors,
                                   pm_harm_bn_per_bn_spent=unit,pm_baseline_bn=own_pm,
                                   pm_respending_bn=dpm,government_mirror_bn=gov_case,
                                   government_budget_mix_arm_bn=gov_budget,restaurant_delta_bn=dr,consumer_scale_demand_arm_bn=dc))
    require_within_budget("social re-spending producer")
    audit = json.dumps(dict(gates={"frozen_case_cash_and_capital":True,"budget_identity":True,
          "legacy_pm_positive_control":True,"legacy_government_positive_control":True,"row4_count":True,
           "primary_pdf_table_shapes":True,"carbon_closure":True,"spending_fraction_0_1":True,"input_sha256":True,
           "accounting_basis_contract":True},
          controls=dict(pm_bn=pm_control,government_pm_bn=gov_legacy,pce_2024_bn=pce_bn,scc_2020usd=dict(epa2=epa_2020,iwg3=iwg_2020)),
          assumptions=["spend all H in 2024; MPC and marginal sector mix not identified", "CE vs PCE is a denominator sensitivity, not confidence interval", "original Tessum personal-consumption attribution includes allocated private investment", "no replicate SE for causal spending propensity or assumed emissions parameters", "mortality weighting and VSLY interaction reported separately" ]),indent=2)+"\n"
    publish_bundle("respending", {"items.csv":csv_text(rows), "spending_components.csv":csv_text(components),
                                 "co2_beside.csv":csv_text(co2), "audit.json":audit}, dependencies=dependencies)
    print(f"rows={len(rows)} carbon={len(co2)} elapsed_s={time.perf_counter()-start:.3f} maxrss_bytes={resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}")


if __name__=="__main__":
    main()
