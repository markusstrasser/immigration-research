"""Arm 4: Florida and Texas hospital immigration-status reports against the account's
uncompensated-care keying, for the unauthorized in those states.

The account keys hospital uncompensated care by uninsured person-years (full-year uninsured plus
half of part-year, CPS ASEC 2025) at AHA's national total: $42.67bn in 2020, x1.20 at 2024 prices
(uncompensated_care_2026_09_23). Applied to a state's imputed unauthorized (status_impute_2026_09_16
via frame.status), the same keying gives the gross uncompensated care the account implies for them.
The reports count admissions and emergency visits by self-reported status and price them at
hospital cost, gross of payments. Every report number is checked verbatim in the text copies under
_cache/arm4 before use.

rho is the unauthorized uninsured's hospital cost per uninsured person-year over everyone else's,
solved so the relevant total holds: AHA's national total, the state's own uncompensated or charity
care total (Texas: THA/HHSC 2023 floor), or, for Florida, shares of one hospital cost base (AHCA
prices encounters at average cost and puts uncompensated care at 3.76% of cost). The main case's
part (the under-charged inside share, g x (s - k) x N) is recomputed over the uncompensated
lane's eight arms at each rho. Report counts exclude decliners and costs are gross of payments,
so every rho here is a face-value reading, biased down by the first and up by the second.

Writes derived/hospital_states.csv, derived/hospital_benchmarks.csv, derived/hospital_main_case.csv.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import frame as f  # noqa: E402

ARM4 = f.CACHE / "arm4"
UC_SUMMARY = f.FISCAL / "uncompensated_care_2026_09_23/derived/summary.json"
AHA_BN = 42.67  # AHA community-hospital uncompensated care at cost, 2020 (uncompensated lane)
UPLIFT = 1.20   # 2024 hospital input prices (same lane)
STATES = {"florida": 12, "texas": 48}
TX_MONTHS = 10  # GA-46 FY2025 covers November 2024 to August 2025

# name: (value, file under _cache/arm4, text that must appear there, whitespace-normalized)
REPORTS = {
    "tx_ed_medicaid_cost": (24_332_064, "tx_hhsc_ga46_summary_fy2025_official.txt", "21,845 $24,332,064"),
    "tx_ed_non_medicaid_cost": (205_542_492, "tx_hhsc_ga46_summary_fy2025_official.txt", "230,480 $205,542,492"),
    "tx_ip_medicaid_cost": (255_352_904, "tx_hhsc_ga46_summary_fy2025_official.txt", "20,470 $255,352,904"),
    "tx_ip_non_medicaid_cost": (565_415_404, "tx_hhsc_ga46_summary_fy2025_official.txt", "40,947 $565,415,404"),
    "tx_total_cost": (1_050_642_864, "tx_hhsc_ga46_summary_fy2025_official.txt", "313,742 $1,050,642,864"),
    "tx_total_visits": (313_742, "tx_hhsc_ga46_summary_fy2025_official.txt", "Total Visits and Costs not 313,742"),
    "fl2025_cost": (558.1e6, "fl_ahca_2025_immigration_report_v1.txt", "more than $558.1 million"),
    "fl2025_medicaid_paid": (80.2e6, "fl_ahca_2025_immigration_report_v1.txt", "totaled $80.2 million in 2025"),
    "fl2025_nlp_admissions": (21_010, "fl_ahca_2025_immigration_report_v1.txt",
                              "Admissions Indicated Not Lawfully Present 21,010"),
    "fl2025_declined_admissions": (200_775, "fl_ahca_2025_immigration_report_v1.txt",
                                   "Admissions Declined to Answer 200,775"),
    "fl2025_admissions": (3_436_106, "fl_ahca_2025_immigration_report_v1.txt", "Total Admissions 3,436,106"),
    "fl2025_nlp_ed": (50_397, "fl_ahca_2025_immigration_report_v1.txt", "ED Visits Indicated Not Lawfully Present 50,397"),
    "fl2025_declined_ed": (502_825, "fl_ahca_2025_immigration_report_v1.txt", "ED Visits Declined to Answer 502,825"),
    "fl2025_ed": (9_215_069, "fl_ahca_2025_immigration_report_v1.txt", "Total ED Visits 9,215,069"),
    "fl2024_cost_press": (660e6, "fl_press_2025-03-07_hospital_patient_immigration_status.txt",
                          "illegal immigrants is nearly $660 million"),
    # Restated in the 2026 report's chart (read by eye); the text's "$129 million" decline ties it.
    "fl2024_cost_restated": (687.1e6, "img/fl2025_p5_chart_transcription.txt", "2024 bar: $687.1M"),
    "fl2024_restated_tie": (129e6, "fl_ahca_2025_immigration_report_v1.txt", "down by approximately $129 million"),
    "fl2024_medicaid_paid": (76.6e6, "fl_press_2025-03-07_hospital_patient_immigration_status.txt",
                             "totaled $76.6 million in 2024"),
    "fl2025_medicaid_fall": (0.30, "fl_ahca_2025_immigration_report_v1.txt", "fell by 30% since 2023"),
    "fl2023_nlp_admissions": (14_141, "fl_ahca_report_hospital_patient_immigration_2023data.txt",
                              "Admissions Indicated Not Lawfully Present 7,438 6,703 14,141"),
    "fl2023_nlp_ed": (40_303, "fl_ahca_report_hospital_patient_immigration_2023data.txt",
                      "ED Visits Indicated Not Lawfully Present 20,672 19,631 40,303"),
    "fl2023_declined_admissions": (134_248, "fl_ahca_report_hospital_patient_immigration_2023data.txt",
                                   "Admissions Declined To Answer 67,719 66,529 134,248"),
    "fl2023_declined_ed": (351_987, "fl_ahca_report_hospital_patient_immigration_2023data.txt",
                           "ED Visits Declined To Answer 177,092 174,895 351,987"),
    "fl2023_admissions": (1_745_054, "fl_ahca_report_hospital_patient_immigration_2023data.txt",
                          "Total Admissions 822,089 922,965 1,745,054"),
    "fl2023_ed": (4_882_106, "fl_ahca_report_hospital_patient_immigration_2023data.txt",
                  "Total Ed Visits 2,269,998 2,612,108 4,882,106"),
    "fl2022_statewide_uc": (2_596_306_165, "fl_ahca_report_hospital_patient_immigration_2023data.txt",
                            "$2,596,306,165"),
    "fl2022_operating_expense": (69_050_695_879, "fl_ahca_report_hospital_patient_immigration_2023data.txt",
                                 "($69,050,695,879 x 0.0376 ="),
    # Secondary: Texas Hospital Association FAQ (Sept 2024) p.3, citing HHSC's 2023 UC pool model.
    # Uninsured charity care at DSH and UC hospitals only; bad debt excluded.
    "tx2023_uninsured_charity_care": (8.1e9, "tha_charity_care_faq_2024-09.txt",
                                      "least $8.1 billion in uninsured charity care"),
}
# The uncompensated lane's government offsets ($bn; VA and IHS removed), copied from
# uncompensated_care_2026_09_23/uncompensated.py and gated against its summary.json below.
OFFSETS = {
    2013: dict(total_uc=84.9 - 8.1 - 2.1, programs={"medicaid": 13.5, "medicare": 8.0,
               "state_local": 9.8 + 7.3 + 3.0 + 1.5 + 0.1}),
    2017: dict(total_uc=42.4 - 10.3 - 2.3, programs={"medicaid": 9.8, "state_local": 9.9 + 1.3}),
}
PER_HEAD_SHARE = 0.120245


def report(name):
    value, file, needle = REPORTS[name]
    text = " ".join((ARM4 / file).read_text(errors="replace").split())
    if " ".join(needle.split()) not in text:
        raise ValueError(f"[BLOCKED] {name}: '{needle}' not found in {file}")
    return value


def inside_arms(py_tu, py_tl, py_u, py_o, keys, rho=1.0, union_rho=None):
    """Uncompensated lane's eight arms: the union's under-charged inside part g(s - k)N when the
    unauthorized uninsured (py_u nationally, py_tu in the union) use care at rho times everyone
    else. union_rho scales every union uninsured person-year instead (the lane's 0.7x arm)."""
    if union_rho is None:
        s = (rho * py_tu + py_tl) / (rho * py_u + py_o)
    else:
        py_t = py_tu + py_tl
        s = union_rho * py_t / (union_rho * py_t + (py_u + py_o - py_t))
    out = []
    for year, spec in OFFSETS.items():
        total_off = sum(spec["programs"].values())
        g = total_off / spec["total_uc"]
        for local_key in ("health_other", "per_head"):
            k = sum(v / total_off * keys[local_key if p == "state_local" else p] for p, v in spec["programs"].items())
            for n in (AHA_BN, AHA_BN * UPLIFT):
                out.append(g * (s - k) * n)
    return min(out), max(out), s


def rho_national(e_bn, py_su, py_u, py_o, n_bn):
    """Solve e = rho c_o py_su with n = c_o (rho py_u + py_o): cost per person-year of the
    unauthorized uninsured over everyone else's, national total held at n."""
    return e_bn * py_o / (n_bn * py_su - e_bn * py_u)


def rho_within(e_bn, total_bn, py_su, py_so):
    """Same, holding the state's own statewide uncompensated care (py_so = the state's others)."""
    return e_bn * py_so / (py_su * (total_bn - e_bn))


def main():
    d = f.load()
    W = f.weights(d)
    civ, target = f.masks(d)
    un, _ = f.status(d)
    un = un & civ
    exposure = d.NOCOV_CYR.eq(3).to_numpy(float) + 0.5 * d.NOCOV_CYR.eq(2).to_numpy(float)
    py_all = (W[civ] * exposure[civ, None]).sum(0)
    state = d.GESTFIPS.to_numpy()
    hf = f.household_fraction(d, civ)
    model = f.model()
    lines = {l["id"]: l for l in model["spending"]["lines"]}
    med_line = lines["medicaid_and_chip_other_medical"]
    medicaid = f.meps_means(d)["medicaid"]
    med_total = medicaid[civ] @ W[civ]

    groups = {"all_civilians": civ, "unauthorized_all_origins": un, "union": target, "union_unauthorized": un & target}
    rows, vec = [], {}
    for place, code in [("national", None), *STATES.items()]:
        where = civ if code is None else civ & (state == code)
        for g, m in groups.items():
            s = m & where
            persons = W[s].sum(0)
            py = (W[s] * exposure[s, None]).sum(0)
            share = py / py_all
            med = med_line["national_bn"] * hf * (medicaid[s] @ W[s]) / med_total
            vec[(place, g)] = dict(persons=persons, py=py, share=share, medicaid=med)
            rows.append(dict(place=place, group=g, persons_m=persons[0] / 1e6, persons_se_m=f.sdr(persons / 1e6),
                             uninsured_py_m=py[0] / 1e6, uninsured_py_se_m=f.sdr(py / 1e6),
                             uninsured_rate=py[0] / persons[0], share_of_national_uninsured_py=share[0],
                             share_se=f.sdr(share), account_uc_bn_2020=AHA_BN * share[0],
                             account_uc_bn_2024=AHA_BN * UPLIFT * share[0],
                             account_uc_se_bn_2024=f.sdr(AHA_BN * UPLIFT * share),
                             account_medicaid_key_bn=med[0], account_medicaid_key_se_bn=f.sdr(med)))
    states = pd.DataFrame(rows)
    for place in STATES:
        base = vec[(place, "all_civilians")]
        for g in groups:
            m = (states.place == place) & (states.group == g)
            states.loc[m, "share_of_state_persons"] = vec[(place, g)]["persons"][0] / base["persons"][0]
            states.loc[m, "share_of_state_uninsured_py"] = vec[(place, g)]["py"][0] / base["py"][0]

    # Positive controls: the union's share of uninsured person-years and its Medicaid dollars.
    uc = json.loads(UC_SUMMARY.read_text())
    got = vec[("national", "union")]["share"][0]
    if abs(got - uc["target_share"]) > 1e-9:
        raise ValueError(f"[BLOCKED] union uninsured share {got} != lane {uc['target_share']}")
    want = med_line["keys"]["medicaid"]["personal"]["target_bn"]
    if abs(vec[("national", "union")]["medicaid"][0] - want) > 1e-6:
        raise ValueError(f"[BLOCKED] union Medicaid {vec[('national', 'union')]['medicaid'][0]} != model {want}")

    def key_share(line_id):
        line = lines[line_id]
        return line["keys"][line["preferred_key"]]["personal"]["target_bn"] / line["national_bn"]

    keys = {"medicaid": key_share("medicaid_and_chip_other_medical"), "medicare": key_share("medicare"),
            "health_other": key_share("health_services"), "per_head": PER_HEAD_SHARE}
    py_tu = vec[("national", "union_unauthorized")]["py"][0] / 1e6
    py_t = vec[("national", "union")]["py"][0] / 1e6
    py_tl = py_t - py_tu
    py_u = vec[("national", "unauthorized_all_origins")]["py"][0] / 1e6
    py_o = py_all[0] / 1e6 - py_u
    lo, hi, _ = inside_arms(py_tu, py_tl, py_u, py_o, keys)
    adopted = uc["inside_undercharged_bn_use_1.0"]
    if abs(lo - adopted[0]) > 1e-9 or abs(hi - adopted[1]) > 1e-9:
        raise ValueError(f"[BLOCKED] inside part {lo}, {hi} != lane {adopted}")
    lo7, hi7, _ = inside_arms(py_tu, py_tl, py_u, py_o, keys, union_rho=0.7)
    if abs(lo7 - uc["inside_undercharged_bn_use_0.7"][0]) > 1e-9 or abs(hi7 - uc["inside_undercharged_bn_use_0.7"][1]) > 1e-9:
        raise ValueError("[BLOCKED] 0.7x arm does not reproduce the lane")
    print(f"  ✓ controls: union uninsured share {got:.6f}, Medicaid {want:.3f}bn, inside {lo:.4f}–{hi:.4f}bn")

    # Report totals, $bn a year.
    tx_scale = 12 / TX_MONTHS
    tx_non = (report("tx_ed_non_medicaid_cost") + report("tx_ip_non_medicaid_cost")) * tx_scale / 1e9
    tx_med = (report("tx_ed_medicaid_cost") + report("tx_ip_medicaid_cost")) * tx_scale / 1e9
    tx_total = report("tx_total_cost") * tx_scale / 1e9
    if abs(tx_non + tx_med - tx_total) > 1e-9:
        raise ValueError("Texas payer rows do not sum to the total")
    fl25 = (report("fl2025_cost") - report("fl2025_medicaid_paid")) / 1e9
    if abs(report("fl2024_cost_restated") - report("fl2025_cost") - report("fl2024_restated_tie")) > 1e5:
        raise ValueError("Florida 2024 restated bar does not tie to the text")
    fl24 = {"press": (report("fl2024_cost_press") - report("fl2024_medicaid_paid")) / 1e9,
            "restated": (report("fl2024_cost_restated") - report("fl2024_medicaid_paid")) / 1e9}
    fl_uc = report("fl2022_statewide_uc") / 1e9
    nlp25 = report("fl2025_nlp_admissions") + report("fl2025_nlp_ed")
    declined25 = report("fl2025_declined_admissions") + report("fl2025_declined_ed")
    encounters25 = report("fl2025_admissions") + report("fl2025_ed")

    def v(place, g, key="py", i=0):
        return vec[(place, g)][key][i] / (1e6 if key in ("py", "persons") else 1)

    bench, main_rows = [], []

    def add(**kw):
        bench.append(kw)

    # Florida statewide uncompensated care: the keying's level check.
    for price, n in (("2020", AHA_BN), ("2024", AHA_BN * UPLIFT)):
        acc = n * v("florida", "all_civilians", "share")
        add(benchmark="florida_statewide_uncompensated_care_all_patients", source="AHCA 2023-data report p.2 (FHURS 2022)",
            year=2022, external_bn=fl_uc, account_bn=acc, account_spec=f"AHA national x FL share of uninsured PY, {price} prices",
            same_definition="partly", ratio_external_to_account=fl_uc / acc,
            note="FHURS: care not covered by Medicare, Medicaid, private insurance or self-pay, 3.76% of operating expense")
    # Texas: non-Medicaid NLP cost against the account's gross uncompensated care for TX's unauthorized.
    py_su_tx = v("texas", "unauthorized_all_origins")
    for price, n in (("2020", AHA_BN), ("2024", AHA_BN * UPLIFT)):
        acc = n * v("texas", "unauthorized_all_origins", "share")
        rho = rho_national(tx_non, py_su_tx, py_u, py_o, n)
        add(benchmark="texas_nlp_non_medicaid_hospital_cost", source="HHSC GA-46 FY2025 summary (Nov 2024-Aug 2025) x 12/10",
            year=2025, external_bn=tx_non, account_bn=acc,
            account_spec=f"AHA national x TX imputed-unauthorized share of uninsured PY, {price} prices",
            same_definition="partly", ratio_external_to_account=tx_non / acc, rho=rho, spec=f"texas_face_value|national_{price}",
            note="ED + inpatient cost, not charges, gross of payments; non-Medicaid bucket mixes private pay, cash, charity")
        a, b, s = inside_arms(py_tu, py_tl, py_u, py_o, keys, rho=rho)
        main_rows.append(dict(spec=f"texas_face_value|national_{price}", rho=rho, union_share=s, inside_low_bn=a,
                              inside_high_bn=b, change_low_bn=a - adopted[0], change_high_bn=b - adopted[1]))
        add(benchmark="texas_statewide_uninsured_charity_care", source="THA charity-care FAQ Sept 2024 p.3 (HHSC UC pool model)",
            year=2023, external_bn=report("tx2023_uninsured_charity_care") / 1e9,
            account_bn=n * v("texas", "all_civilians", "share"),
            account_spec=f"AHA national x TX share of uninsured PY, {price} prices", same_definition="partly",
            ratio_external_to_account=report("tx2023_uninsured_charity_care") / 1e9 / (n * v("texas", "all_civilians", "share")),
            note="'at least'; DSH and UC hospitals; uninsured charity care only, bad debt excluded; secondary source")
    tx_uc = report("tx2023_uninsured_charity_care") / 1e9
    py_so_tx = v("texas", "all_civilians") - py_su_tx
    rho = rho_within(tx_non, tx_uc, py_su_tx, py_so_tx)
    add(benchmark="texas_nlp_non_medicaid_hospital_cost_within_state", source="HHSC GA-46 FY2025 x 12/10; THA FAQ p.3",
        year=2025, external_bn=tx_non, account_bn=tx_uc * py_su_tx / (py_su_tx + py_so_tx),
        account_spec="TX uninsured charity care (2023) x TX imputed-unauthorized share of TX uninsured PY",
        same_definition="partly", ratio_external_to_account=tx_non / (tx_uc * py_su_tx / (py_su_tx + py_so_tx)), rho=rho,
        spec="texas_face_value|within_state",
        note="state total excludes bad debt and non-DSH/UC hospitals, so it is a floor")
    a, b, s = inside_arms(py_tu, py_tl, py_u, py_o, keys, rho=rho)
    main_rows.append(dict(spec="texas_face_value|within_state", rho=rho, union_share=s, inside_low_bn=a,
                          inside_high_bn=b, change_low_bn=a - adopted[0], change_high_bn=b - adopted[1]))
    # Multiple of the reported non-Medicaid cost (visits at the report's own average cost) that
    # equal use would need; Texas publishes no declined-to-answer count to compare it with.
    need = {"national_2024": AHA_BN * UPLIFT * v("texas", "unauthorized_all_origins", "share") / tx_non,
            "within_state": tx_uc * py_su_tx / (py_su_tx + py_so_tx) / tx_non}
    add(benchmark="texas_multiple_of_reported_nlp_cost_needed_for_equal_use", source="HHSC GA-46 FY2025 summary",
        year=2025, external_bn=np.nan, account_bn=np.nan, account_spec="equal use per uninsured person-year",
        same_definition="no", ratio_external_to_account=np.nan,
        note=f"x{need['national_2024']:.2f} (AHA national, 2024 prices) or x{need['within_state']:.2f} (TX charity-care floor)")
    add(benchmark="texas_nlp_total_hospital_cost", source="HHSC GA-46 FY2025 summary x 12/10", year=2025,
        external_bn=tx_total, account_bn=AHA_BN * UPLIFT * v("texas", "unauthorized_all_origins", "share") +
        v("texas", "unauthorized_all_origins", "medicaid"),
        account_spec="uncompensated keying (2024 prices) + account Medicaid key dollars, TX imputed unauthorized",
        same_definition="no", ratio_external_to_account=np.nan,
        note="context: the account has no hospital-cost line; insured NLP care paid privately is outside it")
    add(benchmark="texas_nlp_medicaid_chip_hospital_cost", source="HHSC GA-46 FY2025 summary x 12/10", year=2025,
        external_bn=tx_med, account_bn=v("texas", "unauthorized_all_origins", "medicaid"),
        account_spec="account Medicaid key (MEPS payer mean by age x US birth, insured only), TX imputed unauthorized",
        same_definition="no", ratio_external_to_account=tx_med / v("texas", "unauthorized_all_origins", "medicaid"),
        note="report: hospital cost of emergency Medicaid and CHIP (incl. unborn-child option) patients; account: all Medicaid services")
    py_su_fl = v("florida", "unauthorized_all_origins")
    py_so_fl = v("florida", "all_civilians") - py_su_fl
    equal_share = py_su_fl / (py_su_fl + py_so_fl)
    # Florida, leading reading: shares of one hospital cost base. AHCA prices every encounter at
    # average cost, so NLP cost = NLP share of encounters x cost, and statewide uncompensated care =
    # 3.76% x cost (FHURS 2022). The base cancels except for Medicaid's paid claims, bounded by zero
    # and by claims over the 2022 operating expense (later bases are larger, so the share smaller).
    opex = report("fl2022_operating_expense") / 1e9
    uc_ratio = fl_uc / opex
    fl_years = {
        "2023": dict(nlp=report("fl2023_nlp_admissions") + report("fl2023_nlp_ed"),
                     enc=report("fl2023_admissions") + report("fl2023_ed"),
                     declined=report("fl2023_declined_admissions") + report("fl2023_declined_ed"),
                     # 2025 claims fell "by 30% since 2023" [INFERENCE: 2023 = 2025 / 0.7]
                     medicaid=report("fl2025_medicaid_paid") / (1 - report("fl2025_medicaid_fall")) / 1e9),
        "2025": dict(nlp=nlp25, enc=encounters25, declined=declined25,
                     medicaid=report("fl2025_medicaid_paid") / 1e9),
    }
    for label, y in fl_years.items():
        share = y["nlp"] / y["enc"]
        for med_label, med in (("medicaid_zero", 0.0), ("medicaid_over_2022_opex", y["medicaid"] / opex)):
            x = (share - med) / uc_ratio  # NLP share of FL uncompensated care, if all non-Medicaid cost were
            rho = x * py_so_fl / (py_su_fl * (1 - x))
            extra = (equal_share * uc_ratio + med - share) * y["enc"]
            add(benchmark=f"florida_nlp_share_of_uncompensated_care_{label}|{med_label}",
                source="AHCA counts (2023-data report p.4; 2025 report p.4), FHURS 2022 ratio p.2", year=int(label),
                external_bn=x, account_bn=equal_share, account_spec="FL imputed-unauthorized share of FL uninsured PY",
                same_definition="partly", ratio_external_to_account=x / equal_share, rho=rho,
                spec=f"florida_face_value_{label}|within_state_shares|{med_label}",
                note=f"shares, not $bn; NLP {share:.3%} of encounters; equal use needs {extra:,.0f} more NLP encounters "
                     f"= {extra / y['declined']:.1%} of {y['declined']:,} decliners")
            a, b, s = inside_arms(py_tu, py_tl, py_u, py_o, keys, rho=rho)
            main_rows.append(dict(spec=f"florida_face_value_{label}|within_state_shares|{med_label}", rho=rho,
                                  union_share=s, inside_low_bn=a, inside_high_bn=b, change_low_bn=a - adopted[0],
                                  change_high_bn=b - adopted[1]))
    # Florida in dollars: the reports' NLP cost less Medicaid claims against the 2022 statewide total.
    # The NLP estimates sit on later, larger cost bases, so these overstate rho.
    for label, e, year in (("2025", fl25, 2025), ("2024_press", fl24["press"], 2024), ("2024_restated", fl24["restated"], 2024)):
        rho = rho_within(e, fl_uc, py_su_fl, py_so_fl)
        add(benchmark=f"florida_nlp_cost_less_medicaid_paid_{label}|dollars", source="AHCA report / press release",
            year=year, external_bn=e, account_bn=fl_uc * equal_share,
            account_spec="FL statewide uncompensated care (FHURS 2022) x FL imputed-unauthorized share of FL uninsured PY",
            same_definition="partly", ratio_external_to_account=e / (fl_uc * equal_share), rho=rho,
            spec=f"florida_face_value_{label}|within_state_dollars",
            note="NLP cost on the 2023-24 FHURS base against 2022 uncompensated care: bases differ")
        a, b, s = inside_arms(py_tu, py_tl, py_u, py_o, keys, rho=rho)
        main_rows.append(dict(spec=f"florida_face_value_{label}|within_state_dollars", rho=rho, union_share=s,
                              inside_low_bn=a, inside_high_bn=b, change_low_bn=a - adopted[0], change_high_bn=b - adopted[1]))
        for price, n in (("2020", AHA_BN), ("2024", AHA_BN * UPLIFT)):
            rho_n = rho_national(e, py_su_fl, py_u, py_o, n)
            a, b, s = inside_arms(py_tu, py_tl, py_u, py_o, keys, rho=rho_n)
            main_rows.append(dict(spec=f"florida_face_value_{label}|national_{price}", rho=rho_n, union_share=s,
                                  inside_low_bn=a, inside_high_bn=b, change_low_bn=a - adopted[0],
                                  change_high_bn=b - adopted[1]))
    p_state = v("florida", "unauthorized_all_origins", "persons") / v("florida", "all_civilians", "persons")
    add(benchmark="florida_2025_nlp_share_of_encounters_vs_population", source="AHCA 2025 report p.4 counts", year=2025,
        external_bn=nlp25 / encounters25, account_bn=p_state, account_spec="CPS imputed-unauthorized share of FL residents",
        same_definition="no", ratio_external_to_account=(nlp25 / encounters25) / p_state,
        note=f"with every decliner counted NLP: {(nlp25 + declined25) / encounters25:.2%} of encounters")
    add(benchmark="florida_medicaid_paid_nlp_2025", source="AHCA 2025 report p.3", year=2025,
        external_bn=report("fl2025_medicaid_paid") / 1e9, account_bn=v("florida", "unauthorized_all_origins", "medicaid"),
        account_spec="account Medicaid key, FL imputed unauthorized", same_definition="no",
        ratio_external_to_account=report("fl2025_medicaid_paid") / 1e9 / v("florida", "unauthorized_all_origins", "medicaid"),
        note="report: paid hospital claims for NLP patients; account: all Medicaid services at the cell mean")

    bench = pd.DataFrame(bench)
    main_df = pd.DataFrame(main_rows)
    f.OUT.mkdir(parents=True, exist_ok=True)
    states.to_csv(f.OUT / "hospital_states.csv", index=False, lineterminator="\n")
    bench.to_csv(f.OUT / "hospital_benchmarks.csv", index=False, lineterminator="\n")
    main_df.to_csv(f.OUT / "hospital_main_case.csv", index=False, lineterminator="\n")
    pd.set_option("display.width", 250)
    print(states.round(4).to_string())
    print(bench.drop(columns=["source", "account_spec", "note"]).round(4).to_string())
    print(bench[["benchmark", "note"]].to_string())
    print(main_df.round(4).to_string())
    print(f"equal-use FL share of FL uninsured PY {equal_share:.4f}; national unauthorized PY {py_u:.3f}m, "
          f"union unauthorized {py_tu:.3f}m, union other {py_tl:.3f}m")


if __name__ == "__main__":
    main()
