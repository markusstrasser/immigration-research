"""P7 PM mortality receivers and common VSLY, beside preserved air_items.py.

Receiver ages: ACS 2024 PUMS, national and PUMA-to-urban-area allocation.
Baseline rates: parse NVSS 2024 Data Brief 548 table 3 (age 1+); age 0
uses the primary NVSS 2024 period life table. Common age rates isolate age
composition, not ethnic mortality differences. Source emission attribution,
national PM deaths, L/E/iota arms and morbidity assumptions stay original.
The absence of group-specific source-receptor matrices remains a limitation.
"""
from __future__ import annotations

import json
from pathlib import Path
import re
import resource
import subprocess
import sys
import time
import zipfile

sys.dont_write_bytecode = True
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup

HERE = Path(__file__).resolve().parent
FISCAL = HERE.parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(FISCAL / "crime_victim_cost_2026_09_23"))
import vsl_standard as V
import air_items as A
from mortality_sources import digest

OUT = HERE / "derived"
WEIGHTS = ["PWGTP"] + [f"PWGTP{i}" for i in range(1, 81)]
GATES = []


def gate(name, condition, **detail):
    if not bool(condition):
        raise ValueError(f"[BLOCKED] {name}: {detail}")
    GATES.append(dict(name=name, pass_=True, **detail))


def verify_pins():
    for entry in json.loads((HERE / "inputs/pins.json").read_text())["files"]:
        path = ROOT / entry["path"]
        gate(f"pinned {path.name}", path.is_file() and digest(path) == entry["sha256"])
    V.check_pins()
    gate("own life-table bytes equal common valuation source", digest(HERE / "_cache/lt2024_Table01.xlsx") ==
         digest(V.HERE / "inputs/lt2024_Table01.xlsx"))


def rates_and_years():
    soup = BeautifulSoup((HERE / "_cache/db548.html").read_text(), "html.parser")
    matches = [t for t in soup.find_all("table") if t.caption and "Number of deaths and death rate for age groups" in t.caption.get_text()]
    gate("one primary 2024 age-rate table", len(matches) == 1)
    rates = np.full(101, np.nan)
    rows = []
    for tr in matches[0].find_all("tr"):
        cells = tr.find_all("td")
        if len(cells) != 5:
            continue
        for sup in cells[-1].find_all("sup"):
            sup.decompose()
        label = cells[0].get_text(strip=True).replace("–", "-")
        ages = [int(n) for n in re.findall(r"\d+", label)]
        lo, hi = (ages[0], ages[1]) if len(ages) == 2 else (ages[0], 100)
        rate = float(cells[-1].get_text(strip=True).replace(",", "")) / 100_000
        deaths = float(cells[-2].get_text(strip=True).replace(",", ""))
        rates[lo:hi + 1] = rate
        rows.append(dict(age_band=label, age_low=lo, age_high=hi, mortality_rate=rate, observed_deaths=deaths))
    lt = V.life_table()
    rates[0] = (lt.lx.iloc[0] - lt.lx.iloc[1]) / lt.Lx.iloc[0]
    gate("all ages have finite positive primary mortality rates", np.isfinite(rates).all() and (rates > 0).all())
    years = {str(r): np.array([V.remaining_years(a, r, lt) for a in range(101)]) for r in (0.0, 0.03)}
    # The survey's oldest ages are perturbed/topcoded. Use one open 85+ death
    # profile from the period table, rather than treating 85 as exact age.
    dx = np.r_[lt.lx.to_numpy()[:-1] - lt.lx.to_numpy()[1:], lt.lx.iloc[-1]]
    for r, values in years.items():
        values[85:] = np.average(values[85:], weights=dx[85:])
    pd.DataFrame(rows).to_csv(OUT / "mortality_rates.csv", index=False, lineterminator="\n", float_format="%.12g")
    return rates, years


def puma_cells(rates, years):
    """Cache additive, full/replicate population, death and life-year cells."""
    archive = ROOT / "sources/immigration-fiscal/data/external/acs_pums_2024_1yr/csv_pus.zip"
    cache = HERE / "_cache/mortality_puma.pkl"
    meta = HERE / "_cache/mortality_puma_meta.json"
    signature = dict(aggregation_version=1, source=digest(archive), rates=rates.tolist(),
                     years={k: v.tolist() for k, v in years.items()})
    if cache.exists() and meta.exists() and json.loads(meta.read_text()) == signature:
        return pd.read_pickle(cache)
    pieces = []
    aggregation_started = time.perf_counter()
    use = ["STATE", "PUMA", "AGEP", "HISP", "POBP"] + WEIGHTS
    with zipfile.ZipFile(archive) as z:
        for member in ("psam_pusa.csv", "psam_pusb.csv"):
            for chunk in pd.read_csv(z.open(member), usecols=use, chunksize=80_000, dtype={"STATE": str, "PUMA": str}):
                age = chunk.AGEP.to_numpy(int)
                if not ((age >= 0) & (age <= 100)).all():
                    raise ValueError("[BLOCKED] ACS ages outside primary life-table support")
                chunk["member"] = chunk.HISP.eq(2) | chunk.POBP.eq(303)
                chunk["age"] = age
                # Retain single ages in a compact additive cube; no survey
                # records or statistical uncertainty are reconstructed later.
                sub = chunk.groupby(["STATE", "PUMA", "member", "age"], sort=True)[WEIGHTS].sum()
                pieces.append(sub)
    cells = pd.concat(pieces).groupby(level=[0, 1, 2, 3]).sum().reset_index()
    cells.to_pickle(cache)
    meta.write_text(json.dumps(signature, sort_keys=True) + "\n")
    with (HERE / "_cache/mortality_timings.jsonl").open("a") as stream:
        stream.write(json.dumps(dict(step="cold_puma_aggregation", seconds=time.perf_counter() - aggregation_started,
                                     max_rss_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)) + "\n")
    return cells


def odds_adjust(p, ratio):
    return p * ratio / (p * ratio + 1 - p)


def receiver_context(cells, rates, years, target_n, min_age=0):
    c = cells.copy()
    # Probability membership bridge: same age/place mix, all-resident weights
    # conserved; this is a calibration assumption, not row-4 microdata raking.
    raw_n = c.loc[c.member, "PWGTP"].sum()
    multiplier = target_n / raw_n
    by = []
    for member in (True, False):
        x = c[c.member.eq(member)].copy()
        if member:
            x[WEIGHTS] *= multiplier
        else:
            # Combine subtraction from the same source cells, preserving age
            # and geography as well as national population in each replicate.
            moved = c[c.member].copy()
            moved[WEIGHTS] *= 1 - multiplier
            moved["member"] = False
            x = pd.concat([x, moved], ignore_index=True)
        w = x[WEIGHTS].to_numpy(float)
        age = x.age.to_numpy(int)
        death = rates[age] * (age >= min_age)
        allpop = w.sum(axis=0)
        deaths = (w * death[:, None]).sum(axis=0)
        y = {r: (w * (death * values[age])[:, None]).sum(axis=0) / deaths for r, values in years.items()}
        x[WEIGHTS] = w * death[:, None]
        pm = x.groupby(["STATE", "PUMA"])[WEIGHTS].sum()
        pop = (c[c.member.eq(member)].groupby(["STATE", "PUMA"])[WEIGHTS].sum())
        if member:
            pop *= multiplier
        else:
            pop = pop.add(c[c.member].groupby(["STATE", "PUMA"])[WEIGHTS].sum() * (1 - multiplier), fill_value=0)
        pym = {}
        for r, values in years.items():
            x[WEIGHTS] = w * (death * values[age])[:, None]
            pym[r] = x.groupby(["STATE", "PUMA"])[WEIGHTS].sum()
        by.append(dict(pop=allpop, death=deaths, years=y, puma_death=pm, puma_pop=pop, puma_years=pym))
    g, o = by
    gate(f"population count calibrated {target_n} age {min_age}", abs(g["pop"][0] - target_n) < 1e-6)
    original_pop = c[WEIGHTS].sum().to_numpy()
    gate(f"population conserved all 81 weights age {min_age}", np.max(np.abs(g["pop"] + o["pop"] - original_pop)) < 1e-5)
    xw = pd.read_csv(FISCAL / "congestion_2026_09_23/_cache/xwalk_puma22_ua20.csv", dtype=str)
    xw["afact"] = pd.to_numeric(xw.afact.str.strip())
    xw["afact"] /= xw.groupby(["state", "puma22"]).afact.transform("sum")
    # UA 99999 = territory outside urban areas, not a giant synthetic city.
    ua = {}
    for name, frame in [("gp", g["puma_pop"]), ("op", o["puma_pop"]), ("gd", g["puma_death"]), ("od", o["puma_death"])]:
        merged = frame.reset_index().merge(xw, left_on=["STATE", "PUMA"], right_on=["state", "puma22"], how="left", validate="one_to_many")
        gate(f"every PUMA allocated {name} age {min_age}", merged.afact.notna().all())
        merged[WEIGHTS] = merged[WEIGHTS].mul(merged.afact, axis=0)
        totals = merged.groupby("ua")[WEIGHTS].sum()
        gate(f"UA allocation conserves {name} age {min_age}", np.max(np.abs(totals.sum().to_numpy() - frame.sum().to_numpy())) < 1e-5)
        ua[name] = totals
    keep = ua["gp"].index.difference(["99999", "00000"])
    gp, op, gd, od = [ua[name].loc[keep].to_numpy() for name in ("gp", "op", "gd", "od")]
    emitter = gp / gp.sum(axis=0)
    popself = np.sum(emitter * gp / (gp + op), axis=0)
    deathself = np.sum(emitter * np.divide(gd, gd + od, out=np.zeros_like(gd), where=(gd + od) > 0), axis=0)
    ratio_local = (deathself / (1 - deathself)) / (popself / (1 - popself))
    ratio_national = (g["death"] / g["pop"]) / (o["death"] / o["pop"])
    local_years = {}
    for r, frame in o["puma_years"].items():
        merged = frame.reset_index().merge(xw, left_on=["STATE", "PUMA"], right_on=["state", "puma22"], how="left", validate="one_to_many")
        merged[WEIGHTS] = merged[WEIGHTS].mul(merged.afact, axis=0)
        uy = merged.groupby("ua")[WEIGHTS].sum().loc[keep].to_numpy()
        outsider_fraction = np.divide(od, gd + od, out=np.zeros_like(od), where=(gd + od) > 0)
        within = np.divide(uy, od, out=np.zeros_like(uy), where=od > 0)
        local_years[r] = np.sum(emitter * outsider_fraction * within, axis=0) / np.sum(emitter * outsider_fraction, axis=0)
    return dict(group=g, other=o, local_odds_ratio=ratio_local, national_rate_ratio=ratio_national,
                national_death_share=g["death"] / (g["death"] + o["death"]),
                local_pop_self=popself, local_death_self=deathself, bridge_multiplier=multiplier,
                raw_acs_group_population=float(raw_n), ua_count=len(keep), local_other_years=local_years)


def self_share(context, L, iota, exposure_share):
    return L * odds_adjust(iota, context["local_odds_ratio"]) + (1 - L) * odds_adjust(exposure_share, context["national_rate_ratio"])


def primary_caps():
    """Report primary cap evidence, without inferring a marginal covered share."""
    soup = BeautifulSoup((HERE / "_cache/arp2024_auction.html").read_text(), "html.parser")
    auction = soup.get_text(" ", strip=True)
    auction_price = re.search(r"Clearing:\s*\$\s*(\.?\d+(?:\.\d+)?)", auction)
    gate("ARP 2024 primary clearing price parses", auction_price is not None)
    texts = {}
    for stem in ("csapr2024_bank_2025_rule", "csapr2024_feb_prices"):
        texts[stem] = subprocess.run(["pdftotext", "-raw", str(HERE / f"_cache/{stem}.pdf"), "-"], capture_output=True, text=True, check=True).stdout
    banktext = re.sub(r"\s+", " ", texts["csapr2024_bank_2025_rule"])
    def number(pattern):
        m = re.search(pattern, banktext)
        gate(f"primary cap expression {pattern[:45]}", m is not None)
        return float(m[1].replace(",", ""))
    budget = number(r"consisting of ([\d,]+) allowances from the 2024 emissions budgets")
    bank = number(r"and ([\d,]+) unused allowances carried over")
    available = number(r"approximately ([\d,]+) allowances\. The total amount of NO")
    emissions = number(r"([\d,]+) tons\. 12 For a more detailed")
    gate("2024 seasonal allowances exceed emissions", available > emissions and budget > emissions)
    prices = re.sub(r"\s+", " ", texts["csapr2024_feb_prices"])
    group3 = re.search(r"as of February 28, 2024, of a Group 3 allowance is \$([\d,]+)/ton", prices)
    annual = re.search(r"trading between \$([\d.]+) and \$([\d.]+) per ton", prices)
    gate("dated 2024 CSAPR primary prices parse", group3 is not None and annual is not None)
    result = dict(arp_auction_2024_usd_per_ton=float(auction_price[1]),
                  csapr_annual_feb2024_price_low=float(annual[1]), csapr_annual_feb2024_price_high=float(annual[2]),
                  csapr_group3_feb28_2024_price=float(group3[1]), csapr_2024_12state_budget=budget,
                  csapr_2024_12state_start_bank=bank, csapr_2024_12state_available_after_rule=available,
                  csapr_2024_12state_emissions=emissions, csapr_2024_12state_residual=available - emissions,
                  csapr_2024_12state_emissions_over_budget=emissions / budget,
                  arp_2024_banked_allowances=None, csapr_annual_2024_banked_allowances=None,
                  arp_bank_gap="Exact 2024 ARP bank not obtained: current primary progress page exposes data through 2022; CAMPD public account API probe returned HTTP 403; no number substituted",
                  csapr_annual_bank_gap="2024 annual SO2/NOx banks not obtained; seasonal 12-state carry-in is not a proxy for annual programs",
                  seasonal_residual_status="Arithmetic availability minus emissions after May 2025 retrospective rule, not an independently observed year-end bank",
                  binding_marginal_precursor_share=None,
                  limitation="12-state seasonal program evidence is not all US annual NOx/SO2; positive prices and banks do not identify binding current-year cap; no marginal sector/spending/source-receptor bridge")
    (OUT / "binding_caps.json").write_text(json.dumps(result, indent=2) + "\n")
    return result


def main():
    started = time.perf_counter()
    verify_pins()
    OUT.mkdir(exist_ok=True)
    rates, years = rates_and_years()
    cells = puma_cells(rates, years)
    gate("ACS additive cube ages valid", cells.age.between(0, 100).all())
    gate("ACS additive cube weights finite", np.isfinite(cells[WEIGHTS].to_numpy()).all())
    gate("ACS primary population weights nonnegative", (cells.PWGTP >= 0).all())
    # Replicates are signed survey variance weights, not population counts.
    # Census 2024 dictionary explicitly supports negative PWGTP1..80.
    dictionary = subprocess.run(["pdftotext", "-raw", str(HERE / "_cache/acs2024_dictionary.pdf"), "-"], capture_output=True, text=True, check=True).stdout
    gate("Census declares signed person replicate weights", re.search(r"PWGTP1\s+Numeric\s+5.*?-9999\.\.9999", dictionary, re.S) is not None)
    legacy_grid, _ = A.pm_grid("mexican_origin")
    cen_mask = (legacy_grid.filter(regex="^i_") == 1).all(axis=1)
    cen = legacy_grid[cen_mask].iloc[0]
    old = pd.read_csv(OUT / "items.csv")
    row = old[(old.item == "pm25_consumption") & (old.group == "mexican_origin") & (old.measure == "absolute")].iloc[0]
    original = legacy_grid.others * legacy_grid.morb * A.VSL_DOT_2024 / 1e9
    for key, value in [("low_bn", original.min()), ("central_bn", original[cen_mask].iloc[0]), ("high_bn", original.max())]:
        gate(f"positive control original {key}", abs(float(f"{value:.4f}") - row[key]) < 1e-12)
    case = json.loads((FISCAL / "main_case_2026_10_14/derived/corrections.json").read_text())
    counts = case["meta"]["lineage"]["counts"]
    social = json.loads((HERE / "inputs/band_variants_oct14_positive_control.json").read_text())["lineage_social_keys"]
    factor = 1 + social["low_end"]["consumption"]
    gate("same lineage consumption key at both personal ends", social["low_end"]["consumption"] == social["high_end"]["consumption"])
    frame = pd.read_csv(FISCAL / "population_basis_2026_09_29/derived/frame_counts.csv").set_index("count")
    reevaluated = pd.read_csv(FISCAL / "population_basis_2026_09_29/derived/reeval.csv").set_index("row")
    gate("row4 source union equals frozen case union", abs(float(frame.loc["union|all", "row4"]) - counts["account_union"]) < 1e-6)
    items, contexts, age_contexts = [], {}, []
    for basis, n in [("legacy_cps", A.GROUPS["mexican_origin"]["n"]), ("row4", counts["account_union"])]:
        contexts_by_age = {age: receiver_context(cells, rates, years, n, age) for age in (0, 18, 65)}
        for min_age, age_ctx in contexts_by_age.items():
            age_contexts.append(dict(population_basis=basis, minimum_recipient_age=min_age,
                                     group_expected_baseline_deaths=float(age_ctx["group"]["death"][0]),
                                     other_expected_baseline_deaths=float(age_ctx["other"]["death"][0]),
                                     group_baseline_mortality_share=float(age_ctx["national_death_share"][0]),
                                     group_to_other_death_rate_ratio=float(age_ctx["national_rate_ratio"][0]),
                                     local_mortality_odds_ratio=float(age_ctx["local_odds_ratio"][0]),
                                     national_other_remaining_years=float(age_ctx["other"]["years"]["0.0"][0]),
                                     local_other_remaining_years=float(age_ctx["local_other_years"]["0.0"][0])))
        source_population = A.POP_ALL if basis == "legacy_cps" else float(frame.loc["cps_all_civilian|all", "row4"])
        s = n / source_population
        grid = legacy_grid.copy()
        grid["caused"] *= (n / A.GROUPS["mexican_origin"]["n"]) * A.POP_ALL / source_population
        old_sigmas = []
        for _, x in grid.iterrows():
            L = A.ARMS["L"][int(x.i_L)]
            old_sigmas.append(L * A.ARMS["iota"]["mexican_origin"][int(x.i_io)] +
                              (1 - L) * s * A.ARMS["E"]["mexican_origin"][int(x.i_E)])
        old_full = grid.caused.to_numpy() * (1 - np.array(old_sigmas)) * grid.morb.to_numpy() * V.dot_vsl() / 1e9
        if basis == "row4":
            gate("positive control matches CURRENT row4 PM producer", abs(float(old_full[cen_mask][0]) - float(reevaluated.loc["pm25_consumption", "row4_bn"])) < 1e-9)
        self_values, full_values, years0, years3 = [], [], [], []
        for _, x in grid.iterrows():
            min_age = (65, 0, 18)[int(x.i_crf)]
            ctx = contexts_by_age[min_age]
            sigma = self_share(ctx, A.ARMS["L"][int(x.i_L)], A.ARMS["iota"]["mexican_origin"][int(x.i_io)], s * A.ARMS["E"]["mexican_origin"][int(x.i_E)])
            self_values.append(sigma)
            full_values.append(x.caused * (1 - sigma) * x.morb * V.dot_vsl() / 1e9)
            L = A.ARMS["L"][int(x.i_L)]
            local_self = odds_adjust(A.ARMS["iota"]["mexican_origin"][int(x.i_io)], ctx["local_odds_ratio"])
            nonlocal_self = odds_adjust(s * A.ARMS["E"]["mexican_origin"][int(x.i_E)], ctx["national_rate_ratio"])
            for r, dest in [("0.0", years0), ("0.03", years3)]:
                dest.append((L * (1 - local_self) * ctx["local_other_years"][r] +
                             (1 - L) * (1 - nonlocal_self) * ctx["other"]["years"][r]) / (1 - sigma))
        sigmas = np.array(self_values)
        full = np.array(full_values)
        ci = np.flatnonzero(cen_mask)[0]
        ctx = contexts_by_age[0]
        sigma = sigmas[ci]
        caused = float(grid.loc[ci, "caused"])
        gate(f"mortality conservation {basis}", abs(caused * sigma[0] + caused * (1 - sigma[0]) - caused) < 1e-10)
        gate(f"all grid/replicate mortality shares are probabilities {basis}", ((sigmas >= 0) & (sigmas <= 1)).all())
        all_caused = grid.caused.to_numpy()[:, None]
        gate(f"all 2187 cells/81 weights close on caused deaths {basis}", np.max(np.abs(all_caused * sigmas + all_caused * (1 - sigmas) - all_caused)) < 1e-8)
        gate(f"all 2187 cells/81 weights close on national-attributed dollars {basis}",
             np.max(np.abs((all_caused * sigmas + all_caused * (1 - sigmas) - all_caused) * V.dot_vsl() / 1e9)) < 1e-6)
        reference = float(old_full[ci])
        summary = dict(population=n, self_share=float(sigma[0]), self_share_se=float(np.sqrt(4 / 80 * np.sum((sigma[1:] - sigma[0]) ** 2))),
                       national_group_baseline_mortality_share=float(ctx["national_death_share"][0]),
                       national_group_population_share=float(ctx["group"]["pop"][0] / (ctx["group"]["pop"][0] + ctx["other"]["pop"][0])),
                       local_exposure_share_measured=float(ctx["local_pop_self"][0]), local_mortality_share_measured=float(ctx["local_death_self"][0]),
                       national_group_to_other_death_rate=float(ctx["national_rate_ratio"][0]), local_mortality_odds_ratio=float(ctx["local_odds_ratio"][0]),
                       bridge_multiplier=float(ctx["bridge_multiplier"]), raw_acs_group_population=ctx["raw_acs_group_population"], ua_count=ctx["ua_count"],
                       D=float(cen.D), theta=A.THETA_CONSUMPTION, caused_deaths=caused,
                       outsider_deaths=caused * (1 - sigma[0]), gross_harm_bn=caused * V.dot_vsl() * cen.morb / 1e9,
                       outsider_harm_bn=float(full[ci, 0]), original_bn=reference,
                       live_original_union_bn=reference, historical_original_union_bn=float(original[cen_mask].iloc[0]),
                       source_attribution_national_population=source_population, old_exposure_self_share=float(old_sigmas[ci]),
                       baseline_rates="NVSS 2024 national common age rates; not ethnicity-specific; national total deaths held fixed",
                       source_spatial_assumptions="Original L/iota/E; UA mortality/population odds ratio on member-population emitter weights; no measured group source-receptor matrix")
        ce = pd.read_csv(OUT / "ce_group_spending.csv").set_index("group")
        national_spending = 4 * ce.loc["all", "total_pc_q"] * source_population
        summary.update(national_ce_spending_usd=national_spending, spending_denominator="CE all residents quarterly spending per person times four times original national population; not national PCE; private investment follows consumption as original theta assumes",
                       national_consumption_harm_bn=cen.D * A.THETA_CONSUMPTION * V.dot_vsl() * cen.morb / 1e9,
                       uniform_harm_per_spending_usd=cen.D * A.THETA_CONSUMPTION * V.dot_vsl() * cen.morb / national_spending,
                       without_group_receiver_fraction_fixed_geography=1 - float(ctx["national_death_share"][0]))
        for r, y in ctx["other"]["years"].items():
            summary[f"national_other_remaining_years_r{r}"] = float(y[0])
            summary[f"national_other_vsly_harm_per_spending_usd_r{r}"] = summary["uniform_harm_per_spending_usd"] * (float(y[0]) / V.reference_life_years(float(r)) + cen.morb - 1) / cen.morb
        gov = old[(old.item == "pm25_government_use") & (old.group == "mexican_origin") & (old.measure == "absolute")].iloc[0]
        summary["government_use_original_rounded_bn"] = float(gov.central_bn)
        summary["government_use_mortality_adjusted_bn"] = (cen.D * A.THETA_GOVERNMENT * s * A.GOV["response"][1] *
                                                         A.GOV["use"]["mexican_origin"][1] * (1 - sigma[0]) * V.dot_vsl() * cen.morb / 1e9)
        for rate, ygrid in [(0.0, np.array(years0)), (0.03, np.array(years3))]:
            ry = V.reference_life_years(rate)
            # Morbidity is not a mortality life-year: retain the original
            # illness dollars while replacing only the death valuation.
            mortality_only = full / grid.morb.to_numpy()[:, None]
            values = mortality_only * ygrid / ry + mortality_only * (grid.morb.to_numpy()[:, None] - 1)
            summary[f"remaining_years_r{rate}"] = float(ygrid[ci, 0])
            summary[f"mean_outsider_vsl_usd_r{rate}"] = V.mortality_value("dot_life_years", remaining_years=float(ygrid[ci, 0]), reference_years=ry)
            summary[f"vsly_harm_per_spending_usd_r{rate}"] = summary["uniform_harm_per_spending_usd"] * ((float(ygrid[ci, 0]) / ry) + cen.morb - 1) / cen.morb
            append_item(items, basis, n, "pm25_consumption_mortality_vsly", values, ci, reference, rate, summary)
        append_item(items, basis, n, "pm25_consumption_mortality", full, ci, reference, 0.0, summary)
        contexts[basis] = summary
    # Conditional transport of the consumer's existing added-consumption key.
    # This deliberately keeps union recipients: it is not an identified full-
    # lineage harm because added members are unobservable among outsiders.
    base_rows = [dict(r) for r in items if r["population_basis"] == "row4"]
    for r in base_rows:
        r.update(population_basis="lineage_fixed_boundary", per_member_usd=r["central_bn"] * factor * 1e9 / counts["lineage_population"])
        for k in ("low_bn", "central_bn", "high_bn", "change_low_end_bn", "change_high_end_bn", "conditional_se_bn", "frame_matched_original_bn", "live_original_union_bn", "change_from_live_union_bn"):
            r[k] *= factor
        r["method_note"] += " [ASSUMPTION] Multiply by frozen case added-consumption key; receiver boundary remains identified union, so added members still count among outsider receptors."
        items.append(r)
    receiver_factor = 1 - counts["added"] / (contexts["row4"]["source_attribution_national_population"] - counts["account_union"])
    gate("exchangeable added-receiver factor is a probability", 0 <= receiver_factor <= 1)
    contexts["lineage_fixed_boundary"] = dict(factor=factor, population=counts["lineage_population"], receiver_boundary="identified union; unobserved added recipients not removed", source="oct14 band_variants.json lineage_social_keys.low_end.consumption",
                                              exchangeable_added_receiver_factor=receiver_factor,
                                              exchangeability_assumption="Added descendants receive group-caused pollution at the average remaining nonmember mortality share; source age/place matrix unavailable",
                                              exchangeable_outside_lineage_uniform_bn=contexts["row4"]["outsider_harm_bn"] * factor * receiver_factor,
                                              added_receivers_no_data_bound_factor=[0.0, 1.0])
    pd.DataFrame(items).to_csv(OUT / "mortality_items.csv", index=False, lineterminator="\n", float_format="%.12g")
    pd.DataFrame(age_contexts).to_csv(OUT / "mortality_age_contexts.csv", index=False, lineterminator="\n", float_format="%.12g")
    (OUT / "mortality_context.json").write_text(json.dumps(contexts, indent=2) + "\n")
    primary_caps()
    (OUT / "mortality_gates.json").write_text(json.dumps(GATES, indent=2) + "\n")
    print(pd.DataFrame(items)[["item", "population_basis", "real_discount_rate", "central_bn", "change_low_end_bn", "conditional_se_bn"]].to_string(index=False))
    timing = dict(step="mortality_items", seconds=time.perf_counter() - started, max_rss_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    with (HERE / "_cache/mortality_timings.jsonl").open("a") as stream:
        stream.write(json.dumps(timing) + "\n")
    print(json.dumps(timing))


def append_item(items, basis, n, item, values, ci, reference, rate, summary):
    central = float(values[ci, 0])
    se = float(np.sqrt(4 / 80 * np.sum((values[ci, 1:] - central) ** 2)))
    items.append(dict(item=item, group="mexican_origin", measure="absolute", low_bn=float(values[:, 0].min()), central_bn=central,
                      high_bn=float(values[:, 0].max()), per_member_usd=central * 1e9 / n,
                      evidence_level="contested model; measured primary mortality rates and survey ages; assumed source attribution and receiver bridge",
                      double_count_with="replacement for pm25_consumption; uniform and VSLY mutually exclusive; government/re-spending separate",
                      method_note="Hold original national PM deaths, consumption source attribution, L/E/iota and illness dollars; mortality-weight receiver odds by common baseline age death rates; source/age independence assumed within local/nonlocal components",
                      population_basis=basis, comparator="with versus without identified union; no replacement residents", beneficiary="residents outside identified union",
                      valuation="dot_life_years" if "vsly" in item else "dot_uniform", real_discount_rate=rate,
                      overlap="replace pm25_consumption only; no healthcare fiscal spending overlap; add neither mortality valuations nor gross/net spending rows together",
                      change_low_end_bn=central - reference, change_high_end_bn=central - reference, conditional_se_bn=se,
                      frame_matched_original_bn=reference, live_original_union_bn=summary["live_original_union_bn"],
                      change_from_live_union_bn=central - summary["live_original_union_bn"],
                      se_scope="ACS SDR 80 replicates, rates, source assumptions and population calibration factor fixed; not model uncertainty", self_share=summary["self_share"]))


if __name__ == "__main__":
    main()
