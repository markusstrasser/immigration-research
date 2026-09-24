"""Assemble derived/benchmarks.csv from the four arms' outputs (run the arms first).

One row per outside number: what it measures, the account's value on the nearest definition, the
gap, the implied change to the adopted main case in $bn a year of cost to other residents (low end =
shared allocation, high end = personal), and a verdict by a fixed rule:
- same_definition "no" -> context;
- with a main-case effect: |effect| <= 2 at both ends -> corroborates, else contradicts;
- without one: external/account ratio in [0.8, 1.25] -> corroborates, else contradicts;
- CBO's corporate rows: the key is contradicted but the main case does not use it.
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import frame as f  # noqa: E402

D = f.OUT
COLUMNS = ["arm", "benchmark", "spec", "source", "year", "unit", "external_value", "account_value",
           "same_definition", "gap", "effect_basis", "effect_low_bn", "effect_high_bn", "direction", "verdict", "note"]


def verdict(row):
    if row["same_definition"] == "no":
        return "context"
    lo, hi = row["effect_low_bn"], row["effect_high_bn"]
    if pd.notna(lo) or pd.notna(hi):
        return "corroborates" if max(abs(np.nan_to_num(lo)), abs(np.nan_to_num(hi))) <= 2.0 else "contradicts"
    if pd.notna(row["external_value"]) and pd.notna(row["account_value"]) and row["account_value"]:
        ratio = row["external_value"] / row["account_value"]
        return "corroborates" if 0.8 <= ratio <= 1.25 else "contradicts"
    return "context"


def direction(lo, hi):
    vals = [v for v in (lo, hi) if pd.notna(v)]
    if not vals:
        return "not translated"
    if all(abs(v) < 0.05 for v in vals):
        return "none"
    return "cost up" if np.mean(vals) > 0 else "cost down"


def cbo_rows():
    trans = pd.read_csv(D / "cbo_translation.csv")
    totals = pd.read_csv(D / "cbo_spec_totals.csv")
    engine = pd.read_csv(D / "cbo_main_case.csv").query("profile == 'cbo_category_lag_non_school_full'")
    effect = {(r.spec, r.band_end): r.main_case_change_bn for r in totals.itertuples()}
    rows = []
    for (spec, year), t in trans.query("allocation == 'personal'").groupby(["spec", "year"], sort=False):
        scale = t.national_bn * t.pool_fraction
        account = float((scale * t.account_share).sum())
        external = float((scale * t.reweighted_share).sum())
        concept = t.concept.iloc[0]
        lo, hi = effect.get((spec, "low"), np.nan), effect.get((spec, "high"), np.nan)
        note = f"lines: {', '.join(t.line)}"
        basis = "adopted main case"
        if concept == "corporate_inc_tax":
            e = engine.query("method == @spec")
            lo, hi = float(e.change_low_bn.iloc[0]), float(e.change_high_bn.iloc[0])
            note += "; engine change 0: corporate cells are indirect receipts, which respond at 0 in the main case"
        if concept == "individual_inc_tax":
            note += "; overlaps audit row 3 (+9.5/+9.6): vs the audit package the increment is this minus row 3"
        if concept == "medicaid_and_chip":
            note += ("; community part only (LTSS re-keyed by audit row 5); same Medicaid dollars as the "
                     "pooled-MEPS lane's +12.2 to +21.3 (decision 2), not additive to it")
        rows.append(dict(arm=1, benchmark=f"CBO 61911 distribution: {concept}", spec=spec,
                         source="CBO, The Distribution of Household Income, 2022 (Jan 2026), researcher tables 01/05/07/10-12",
                         year=int(year), unit="$bn union dollars on the lines (personal allocation)",
                         external_value=external, account_value=account,
                         same_definition="partly", gap=external - account, effect_basis=basis,
                         effect_low_bn=lo, effect_high_bn=hi, note=note))
    for concept in ["unemployment_insurance", "workers_compensation"]:
        rows.append(dict(arm=1, benchmark=f"CBO 61911 distribution: {concept}", spec=f"{concept}|2022",
                         source="CBO 61911 table 05", year=2022, unit="group shares", external_value=np.nan,
                         account_value=np.nan, same_definition="partly", gap=np.nan, effect_basis="none",
                         effect_low_bn=np.nan, effect_high_bn=np.nan,
                         note="untestable: CBO rounds household averages to $100, its group shares sum to 1.3 and 0.8"))
    for spec in ["all_concepts|2022", "all_but_medicaid|2022", "all_concepts_excise_on_all_consumption_lines|2022",
                 "all_concepts|2019", "all_but_medicaid|2019", "all_concepts|2018", "all_but_medicaid|2018"]:
        rows.append(dict(arm=1, benchmark="CBO 61911 bundle", spec=spec, source="CBO 61911", year=int(spec[-4:]),
                         unit="$bn main-case change", external_value=np.nan, account_value=np.nan,
                         same_definition="partly", gap=np.nan, effect_basis="adopted main case",
                         effect_low_bn=effect[(spec, "low")], effect_high_bn=effect[(spec, "high")],
                         note="income tax gross of refundable credits; Medicaid with the MEPS theta"))
    return rows


def ota_rows():
    shares = pd.read_csv(D / "ota_shares.csv")
    trans = pd.read_csv(D / "ota_translation.csv")
    rows = []
    for r in shares.dropna(subset=["ota_hispanic_share"]).itertuples():
        definition = "no" if r.item == "dividends_plus_capital_gains" else "partly"
        rows.append(dict(arm=2, benchmark=f"OTA Hispanic share: {r.item}", spec=r.item, source=r.ota_source,
                         year=2024 if r.item.endswith("2024") else 2023,
                         unit="ratio of means, Hispanic/white" if r.item.startswith("mfj") else "Hispanic share",
                         external_value=r.ota_hispanic_share, account_value=r.cps_hispanic_share,
                         same_definition=definition, gap=r.ota_hispanic_share - r.cps_hispanic_share,
                         effect_basis="none", effect_low_bn=np.nan, effect_high_bn=np.nan, note=r.note))
    for spec, basis in [("vs_adopted_raw_keys", "adopted main case"), ("vs_audit_package_ssn_rule", "audit package"),
                        ("audit_row1_ptc_person_key", "audit package (row 1's premium-credit key)")]:
        t = trans.query("spec == @spec").set_index("allocation")
        # A spending line: the change in the union's dollars is the change in cost.
        if spec == "audit_row1_ptc_person_key":
            lo = hi = float(t.loc["both", "change_bn"])
            acc, ext = float(t.loc["both", "account_share"]), float(t.loc["both", "benchmarked_share"])
        else:
            lo, hi = float(t.loc["shared", "change_bn"]), float(t.loc["personal", "change_bn"])
            acc, ext = float(t.loc["personal", "account_share"]), float(t.loc["personal", "benchmarked_share"])
        rows.append(dict(arm=2, benchmark="Refundable credits at OTA's Hispanic shares", spec=spec,
                         source="OTA WP-122 Table 5", year=2023, unit="union share of the credit key",
                         external_value=ext, account_value=acc, same_definition="partly", gap=ext - acc,
                         effect_basis=basis, effect_low_bn=lo, effect_high_bn=hi,
                         note="Hispanic error assumed proportional within Hispanics; totals held"))
    return rows


def unauthorized_rows():
    g = pd.read_csv(D / "unauthorized_gap_mexico_born.csv")
    rows = []
    for r in g.itertuples():
        basis = "adopted main case" if r.rule == "raw" else "audit package (on-books rule; row 13 not applied)"
        cost = -r.anchor_minus_account_bn  # anchor above account = the union pays more = cost down
        rows.append(dict(arm=3, benchmark=f"Unauthorized Mexico-born taxes: {r.item}", spec=f"{r.item}|{r.source}|{r.rule}",
                         source=r.source, year=r.source_year, unit="$ per person, indexed to 2024 wages (SSA AWI)",
                         external_value=r.anchor_per_person_2024, account_value=r.account_per_person,
                         same_definition="partly", gap=r.anchor_per_person_2024 - r.account_per_person,
                         effect_basis=basis, effect_low_bn=cost, effect_high_bn=cost,
                         note="modelled anchor, all origins per person applied to the union's 4.57m imputed "
                              "unauthorized; personal allocation at both ends"))
    return rows


def hospital_rows():
    b = pd.read_csv(D / "hospital_benchmarks.csv")
    m = pd.read_csv(D / "hospital_main_case.csv").set_index("spec")
    rows = []
    for r in b.itertuples():
        spec = r.spec if isinstance(r.spec, str) else ""
        lo = float(m.loc[spec, "change_low_bn"]) if spec else np.nan
        hi = float(m.loc[spec, "change_high_bn"]) if spec else np.nan
        unit = "share of state uncompensated care" if "share_of_uncompensated" in r.benchmark else (
            "share" if "share_of_encounters" in r.benchmark else "$bn a year")
        note = r.note + (f"; rho {r.rho:.2f}" if pd.notna(r.rho) else "")
        rows.append(dict(arm=4, benchmark=r.benchmark, spec=spec or r.account_spec, source=r.source, year=r.year,
                         unit=unit, external_value=r.external_bn, account_value=r.account_bn,
                         same_definition=r.same_definition, gap=r.external_bn - r.account_bn,
                         effect_basis="adopted main case and audit package (line not in the audit)" if spec else "none",
                         effect_low_bn=lo, effect_high_bn=hi, note=note))
    return rows


def main():
    rows = cbo_rows() + ota_rows() + unauthorized_rows() + hospital_rows()
    out = pd.DataFrame(rows)
    out["direction"] = [direction(lo, hi) for lo, hi in zip(out.effect_low_bn, out.effect_high_bn)]
    out["verdict"] = out.apply(verdict, axis=1)
    out.loc[out.note.str.contains("untestable", na=False), "verdict"] = "untestable"
    # CBO's corporate distribution contradicts the key (top 1%: 48% against 11%), but the main case
    # gives indirect receipts no response, so the key moves nothing there.
    out.loc[out.spec.str.startswith("corporate_inc_tax"), "verdict"] = "contradicts key; unused by main case"
    out = out[COLUMNS]
    out.to_csv(D / "benchmarks.csv", index=False, lineterminator="\n")
    print(out.groupby(["arm", "verdict"]).size().to_string())
    print(f"{len(out)} rows → {D / 'benchmarks.csv'}")


if __name__ == "__main__":
    main()
