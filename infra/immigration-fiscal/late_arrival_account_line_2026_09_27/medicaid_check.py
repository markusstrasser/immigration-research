"""Task 3: price the late arrivals' Medicaid (and its mirror, Medicare) by coverage with the 65+ evidence.

How the account prices them. The Medicaid and Medicare lines are keyed by the spending builder's MEPS payer
keys: each insured person (any public or private coverage) takes the MEPS mean payment of their age band x US
birth cell, then the pooled Mexican-origin ratio of that cell (medical_ethnicity_pooled_2026_09_23, 0.88 at
65+; ladder 206), and Medicaid's long-term-care users are charged by the LTSS lane's users' shares
(ltss_share_2026_09_23; within the Mexico-born by ACS proxy rates by arrival class, acs_rates.py). The key does
not read a person's own Medicaid or Medicare coverage. A Mexico-born 65+ who arrived at 50+ therefore takes
the same Medicare and community Medicaid dollars as one who arrived at 20, though fewer of them have Medicare
(no 40 quarters) and more have Medicaid.

The check (convention a, the central age-at-arrival reading, both band ends of each case):
  1. Coverage in the account's own CPS frame (MCAID, MCARE), against the ACS pool (acs_rates.py).
  2. The account's charge: each cell's Medicaid and Medicare line amounts at the band end (run_cells.cjs), per
     person and per covered person; Medicaid split into its LTSS users' charge and the rest (community).
  3. Re-key by coverage inside the Mexico-born 65+ (zero-sum: the account's Mexico-born 65+ totals held):
     community Medicaid and Medicare each by the person's expected coverage, the ACS rate at their arrival
     class and five-year age band (acs_rates.py). Both surveys edit every 65+ Medicaid reporter to Medicare
     coverage (0 Medicaid-only records at 65+ in either file), so every covered senior is priced as a dual:
     one Medicaid price per covered person. The CPS flags are reported beside, not used: the CPS cell is 122
     records and its Medicaid rate (13%) is a third of the ACS's (40%). The LTSS users' charge is left as the
     account has it.
  4. Level beside the re-key: MCBS community Medicaid per Hispanic 65+ beneficiary with any Medicaid payment
     against the account's community Medicaid per ACS-expected covered person. MCBS is claims-linked 2023
     dollars; the account's lines are NIPA totals, so the ratio mixes a level difference in the sources with
     the key; reported, never applied.
Output: derived/medicaid_check.csv (case, spec, subgroup, item, value, unit). Proposed corrections only: the
case is not edited.
--set sept29 checks the v4 cases (sept29, the main case adopted on 2026-09-29, and sept29_cash, its cash set) and
writes derived/medicaid_check_sept29.csv, leaving the default file alone. Under sept29 the pension switch books
Medicare Part A at its accrual on each cell's HI receipts (the payload's meta.pension_accrual) and removes Part A's
share of current spending (part_a_share) from the key. Only the rest, (1 - part_a_share) x the cell's current-spending
charge (the cash set's, which the switch leaves alone), is priced by the MEPS key. That part is `account_medicare_bn`
and is what the re-key moves; the accrual is reported beside it (`account_medicare_part_a_accrual_bn`, zero elsewhere)
and left alone, since it does not depend on coverage. v4 leaves the Medicaid line alone.
--set oct05 checks the v5 cases (oct05, main case v5 adopted on 2026-10-05, and oct05_cash) the same way and writes
derived/medicaid_check_oct05.csv. v5 adds people to G3plus only and moves the G1 cells by the larger group's responses
and row 8, neither of which touches the Medicaid or Medicare lines: a gate holds every G1 cell's two parts at their
sept29 values. The Part A accrual gate covers the cells without the added people, whose Part A accrual is in their own
cell edits rather than in meta.pension_accrual.
--set oct07 checks the v6 cases (oct07, main case v6 in main_case_2026_10_07, and oct07_cash) the same way and writes
derived/medicaid_check_oct07.csv. The set's Part A accrual is v6's (meta.pension_accrual of the v6 payload: 40.783, the
2026 Trustees paths), each cell at its share of it under the generation lane's split (run_cells.cjs cells.v6.part_a_scale).
The gate against oct05 holds every G1 cell's Medicaid part, and its Medicare part less its change in Part A accrual
(v6's scale x 40.783 less v4's x 41.137; zero in the cash set, where the item does not enter).
Run from the repository root:
  OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/late_arrival_account_line_2026_09_27/medicaid_check.py [--set sept29|oct05|oct07]
"""
from __future__ import annotations

import sys

sys.dont_write_bytecode = True

import csv  # noqa: E402
import json  # noqa: E402
import os  # noqa: E402

os.environ.setdefault("LATE_DEF", "central")

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

import acs_rates  # noqa: E402
import frame as F  # noqa: E402

MCBS = F.FISCAL / "mcbs_elderly_medical_2026_09_22/derived/ratios.csv"
LTSS = F.FISCAL / "ltss_share_2026_09_23/derived"
CATS = ["NF", "ICF", "MHF", "HCBS"]
SUBGROUPS = {"late50_65p": ["G1_L50_65p", "G1_L55_65p"], "late55_65p": ["G1_L55_65p"],
             "younger_65p": ["G1_Y_65p"], "mexico_born_65p": ["G1_Y_65p", "G1_L50_65p", "G1_L55_65p"],
             "late50_50_64": ["G1_L50_50_64", "G1_L55_55_64"], "younger_50_64": ["G1_Y_50_64"]}
OLD = ["G1_Y_65p", "G1_L50_65p", "G1_L55_65p"]
# Each set of cases and its file: the default two, and the v4 and v5 cases each in a file of their own.
SETS = {"default": (("sept27", "sept26_schools"), "medicaid_check.csv"),
        "sept29": (("sept29", "sept29_cash"), "medicaid_check_sept29.csv"),
        "oct05": (("oct05", "oct05_cash"), "medicaid_check_oct05.csv"),
        "oct07": (("oct07", "oct07_cash"), "medicaid_check_oct07.csv")}
# The v4, v5 and v6 sets' cash cases (the set's Medicare is keyed on the cash set's charge), and the case each v5 or v6
# case builds on.
CASH = {"sept29": "sept29_cash", "oct05": "oct05_cash", "oct07": "oct07_cash"}
BUILDS_ON = {"oct05": "sept29", "oct05_cash": "sept29_cash", "oct07": "oct05", "oct07_cash": "oct05_cash"}
FAILS = []


def gate(label, ok, detail=""):
    print(f"  {'✓' if ok else '✗'} {label}{' — ' + detail if detail else ''}", flush=True)
    if not ok:
        FAILS.append(label)


def main():
    if F.LATE_DEF != "central":
        sys.exit("[BLOCKED] the check runs on the central reading")
    which = sys.argv[sys.argv.index("--set") + 1] if "--set" in sys.argv else "default"
    if which not in SETS:
        sys.exit(f"--set must be one of {', '.join(SETS)}")
    cases, out_name = SETS[which]
    d = F.load()
    civ, union, gens = F.masks(d)
    w = d.pwwgt0.to_numpy(float)
    mcaid, mcare = d.MCAID.eq(1).to_numpy(), d.MCARE.eq(1).to_numpy()
    rows = []

    def put(case, spec, sub, item, value, unit):
        rows.append(dict(case=case, spec=spec, subgroup=sub, item=item, value=f"{value:.6f}", unit=unit))

    # MCBS 2023, Hispanic, community-dwelling 65+ (ladder 173).
    m = pd.read_csv(MCBS).query("domain == '65+'").set_index("measure")
    caid, anycaid, public = (float(m.loc[k, "hispanic_mean"]) for k in ("PAMTCAID", "ANY_MEDICAID", "PUBLIC"))
    m_dual = caid / anycaid  # Medicaid payment per Hispanic 65+ beneficiary with any Medicaid payment
    print(f"[MCBS] Medicaid per Hispanic 65+ beneficiary with Medicaid ${m_dual:,.0f}; public per beneficiary ${public:,.0f}")

    # 1. Coverage.
    print("[coverage]")
    cov = {}
    for sub, cells in SUBGROUPS.items():
        mk = np.logical_or.reduce([gens[g] for g in cells])
        n = w[mk].sum()
        c = dict(persons=n, medicaid=w[mk & mcaid].sum() / n, medicare=w[mk & mcare].sum() / n,
                 dual=w[mk & mcaid & mcare].sum() / n, medicaid_only=w[mk & mcaid & ~mcare].sum() / n,
                 medicare_only=w[mk & ~mcaid & mcare].sum() / n, neither=w[mk & ~mcaid & ~mcare].sum() / n,
                 records=int(mk.sum()))
        cov[sub] = c
        for k, v in c.items():
            put("cps_asec_2025", "", sub, f"coverage_{k}", v, "persons" if k in ("persons", "records") else "share")
        print(f"  {sub}: n {c['records']}, Medicaid {c['medicaid']:.3f}, Medicare {c['medicare']:.3f}, "
              f"Medicaid without Medicare {c['medicaid_only']:.3f}")
    acs = acs_rates.load()
    for sub, cls, lo, hi in [("late50_65p", ("L50", "L55"), 65, 200), ("younger_65p", ("Y",), 65, 200),
                             ("late50_50_64", ("L50", "L55"), 50, 64), ("younger_50_64", ("Y",), 50, 64)]:
        a = acs[acs.cls.isin(cls) & acs.AGEP.between(lo, hi)]
        for k in ("medicaid", "medicare", "inst"):
            put("acs_2019_2023", "", sub, f"coverage_{k}", float((a[k] * a.w).sum() / a.w.sum()), "share")
        put("acs_2019_2023", "", sub, "coverage_persons", float(a.w.sum()), "persons")

    # Expected coverage per CPS person: the ACS rate at their arrival class and five-year age band.
    g1m = F.g1(gens)
    cls, age = F.g1_class(d), d.A_AGE.to_numpy()
    r_caid, r_care = np.zeros(len(d)), np.zeros(len(d))
    r_caid[g1m] = acs_rates.person_rate("medicaid", cls[g1m], age[g1m])
    r_care[g1m] = acs_rates.person_rate("medicare", cls[g1m], age[g1m])
    for sub, cells in SUBGROUPS.items():
        mk = np.logical_or.reduce([gens[g] for g in cells])
        for k, r in (("medicaid", r_caid), ("medicare", r_care)):
            cov[sub][f"expected_{k}"] = float((w * r)[mk].sum() / w[mk].sum())
            put("acs_rates_on_cps", "", sub, f"coverage_expected_{k}", cov[sub][f"expected_{k}"], "share")

    # LTSS users' charge per cell (correction_rules.py: L_c x share_c x the users' generation fractions).
    sh = pd.read_csv(LTSS / "shares.csv").query("variant == 'central'").set_index("category")
    growth = json.loads((LTSS / "summary.json").read_text())["bea_growth_2024_over_2023"]
    for case in cases:
        c = json.loads((F.HERE / "_cache" / f"cells_{case}_central.json").read_text())
        rules = json.loads((F.OUT / "correction_rules.json").read_text())["rules"]["ltss"]["users_generation"]
        ltss = {g: sum(float(sh.loc[k, "L2023"]) * growth * float(sh.loc[k, "share"]) * rules[k]["a"][j] for k in CATS)
                for j, g in enumerate(F.GENS)}
        cells = c["conventions"]["a"]
        # The set with the pension switch: the MEPS-keyed Medicare charge is (1 - part_a_share) x the cash set's.
        accrual_case = "v4" in c and c["v4"]["set"] == "set"
        # v6: the Part A accrual is the v6 payload's, each cell at its share under the generation lane's split.
        v6 = "v6" in c
        if accrual_case:
            cash = json.loads((F.HERE / "_cache" / f"cells_{CASH[which]}_central.json").read_text())
            pension = json.loads((F.FISCAL / (c["v6"] if v6 else c["v4"])["payload"]).read_text())["meta"]["pension_accrual"]
            pension_v4 = json.loads((F.FISCAL / c["v4"]["payload"]).read_text())["meta"]["pension_accrual"]
            gate(f"{case}: the cash set's cells are the same lane's, at the same specifications",
                 cash["main"] == c["main"] and cash["low_spec"] == c["low_spec"] and cash["high_spec"] == c["high_spec"])
            if v6:
                gate(f"{case}: the Part A accrual is v6's ({pension['part_a_accrual_bn']:.3f}, against {pension_v4['part_a_accrual_bn']:.3f} "
                     "on the September 29 payload), its scales from run_cells.cjs, with the same Part A share",
                     pension["part_a_accrual_bn"] != pension_v4["part_a_accrual_bn"] and pension["part_a_share"] == pension_v4["part_a_share"]
                     and all(abs(sum(c["v6"]["part_a_scale"]["a"][g][a] for g in F.GENS) - 1) < 1e-12 for a in ("personal", "shared")))
        # v5 and v6: the cells they build on, and the cells without the added people.
        prev = json.loads((F.HERE / "_cache" / f"cells_{BUILDS_ON[case]}_central.json").read_text()) if case in BUILDS_ON else None
        added_cell = c["v6"]["added"]["cell"] if v6 else c["v5"]["added"]["cell"] if "v5" in c else None
        plain = [g for g in F.GENS if g != added_cell]
        for end in ("low", "high"):
            spec = f"{end}_{c['low_spec' if end == 'low' else 'high_spec']['allocation']}"
            part = {g: cells[g][end]["parts"] for g in F.GENS}
            amt = {g: cells[g][end]["medicaid_amount_bn"] * cells[g][end]["medicaid_response"] for g in F.GENS}
            gate(f"{case} {end}: the Medicaid part is the line's amount x response", max(abs(amt[g] - part[g]["medicaid"]) for g in F.GENS) < 1e-12)
            alloc = c["low_spec" if end == "low" else "high_spec"]["allocation"]
            if prev is not None:
                was = {g: prev["conventions"]["a"][g][end]["parts"] for g in F.GENS}
                # v6's set moves each cell's Part A accrual: its scale x v6's accrual less v4's scale x v4's.
                shift = {g: (pension["part_a_accrual_bn"] * c["v6"]["part_a_scale"]["a"][g][alloc]
                             - pension_v4["part_a_accrual_bn"] * c["v4"]["parameters"]["a"][g]["pension_refs"]["partAScale"][alloc])
                         if v6 and accrual_case else 0.0 for g in F.GENS}
                gate(f"{case} {end}: every G1 cell's Medicaid part is {BUILDS_ON[case]}'s, and its Medicare part its plus the change "
                     "in its Part A accrual (1e-12)" if v6 and accrual_case
                     else f"{case} {end}: every G1 cell's Medicaid and Medicare parts are {BUILDS_ON[case]}'s (1e-12)",
                     max(max(abs(part[g]["medicaid"] - was[g]["medicaid"]), abs(part[g]["medicare"] - was[g]["medicare"] - shift[g]))
                         for g in F.GENS if g.startswith("G1_")) < 1e-12)
            comm = {g: amt[g] - ltss[g] for g in F.GENS}
            if accrual_case:
                medicare = {g: cash["conventions"]["a"][g][end]["parts"]["medicare"] * (1 - pension["part_a_share"]) for g in F.GENS}
                refs = {g: (c["v6"]["part_a_scale"]["a"][g][alloc] if v6 else c["v4"]["parameters"]["a"][g]["pension_refs"]["partAScale"][alloc])
                        for g in F.GENS}
                gate(f"{case} {end}: each cell's Medicare part less its keyed charge is its Part A accrual (part_a_accrual x its scale)"
                     + ("" if plain == F.GENS else f"; the cells without the added people ({len(plain)} of {len(F.GENS)})"),
                     max(abs(part[g]["medicare"] - medicare[g] - pension["part_a_accrual_bn"] * refs[g]) for g in plain) < 1e-9)
            else:
                medicare = {g: part[g]["medicare"] for g in F.GENS}
            accrual = {g: part[g]["medicare"] - medicare[g] for g in F.GENS}
            # 3. Re-key inside the Mexico-born 65+.
            old = np.logical_or.reduce([gens[g] for g in OLD])
            wt_caid = w * old * r_caid
            wt_care = w * old * r_care
            tot_comm, tot_care = sum(comm[g] for g in OLD), sum(medicare[g] for g in OLD)
            rekey_comm = {g: tot_comm * wt_caid[gens[g]].sum() / wt_caid.sum() for g in OLD}
            rekey_care = {g: tot_care * wt_care[gens[g]].sum() / wt_care.sum() for g in OLD}
            gate(f"{case} {end}: the re-key holds the Mexico-born 65+ totals",
                 abs(sum(rekey_comm.values()) - tot_comm) < 1e-9 and abs(sum(rekey_care.values()) - tot_care) < 1e-9)
            for sub, members in SUBGROUPS.items():
                n = cov[sub]["persons"]
                ncaid, ncare = n * cov[sub]["expected_medicaid"], n * cov[sub]["expected_medicare"]
                a_all = sum(amt[g] for g in members)
                a_ltss = sum(ltss[g] for g in members)
                a_comm = sum(comm[g] for g in members)
                a_care = sum(medicare[g] for g in members)
                put(case, spec, sub, "account_medicaid_bn", a_all, "bn")
                put(case, spec, sub, "account_medicaid_ltss_users_bn", a_ltss, "bn")
                put(case, spec, sub, "account_medicaid_community_bn", a_comm, "bn")
                put(case, spec, sub, "account_medicare_bn", a_care, "bn")
                if which in CASH:
                    put(case, spec, sub, "account_medicare_part_a_accrual_bn", sum(accrual[g] for g in members), "bn")
                put(case, spec, sub, "account_medicaid_per_person_usd", a_all * 1e9 / n, "usd")
                put(case, spec, sub, "account_medicaid_community_per_covered_usd", a_comm * 1e9 / ncaid, "usd")
                put(case, spec, sub, "account_medicare_per_person_usd", a_care * 1e9 / n, "usd")
                put(case, spec, sub, "account_medicare_per_covered_usd", a_care * 1e9 / ncare, "usd")
                if all(g in OLD for g in members):
                    k_comm = sum(rekey_comm[g] for g in members)
                    k_care = sum(rekey_care[g] for g in members)
                    put(case, spec, sub, "rekey_medicaid_community_bn", k_comm, "bn")
                    put(case, spec, sub, "rekey_medicare_bn", k_care, "bn")
                    put(case, spec, sub, "proposed_change_medicaid_bn", k_comm - a_comm, "bn")
                    put(case, spec, sub, "proposed_change_medicare_bn", k_care - a_care, "bn")
                    put(case, spec, sub, "proposed_change_net_bn", k_comm - a_comm + k_care - a_care, "bn")
                    put(case, spec, sub, "proposed_change_net_per_person_usd", (k_comm - a_comm + k_care - a_care) * 1e9 / n, "usd")
                    # 4. Level beside the re-key (never applied).
                    mix = m_dual
                    put(case, spec, sub, "mcbs_medicaid_per_covered_usd_2023", mix, "usd")
                    put(case, spec, sub, "account_over_mcbs_medicaid_per_covered", a_comm * 1e9 / ncaid / mix, "ratio")
                    put(case, spec, sub, "level_mcbs_community_medicaid_bn_2023usd", ncaid * mix / 1e9, "bn")
                    put(case, spec, sub, "level_difference_community_medicaid_bn", ncaid * mix / 1e9 - a_comm, "bn")
                    if sub in ("late50_65p", "younger_65p"):
                        print(f"  {case} {end} {sub}: Medicaid {a_all:.3f}bn (LTSS {a_ltss:.3f}), community per covered "
                              f"${a_comm * 1e9 / ncaid:,.0f} (MCBS ${mix:,.0f}); Medicare per covered ${a_care * 1e9 / ncare:,.0f}; re-key Medicaid {k_comm - a_comm:+.3f}bn, "
                              f"Medicare {k_care - a_care:+.3f}bn, net {k_comm - a_comm + k_care - a_care:+.3f}bn")
    # The LTSS users' charge under the LTSS lane's variants (shares.csv): each category's charge scales with
    # its variant share; the users' fractions (who among the union are the users) are this lane's central ones.
    allv = pd.read_csv(LTSS / "shares.csv")
    rules = json.loads((F.OUT / "correction_rules.json").read_text())["rules"]["ltss"]["users_generation"]
    for variant, v in allv.groupby("variant"):
        v = v.set_index("category")
        for sub, members in SUBGROUPS.items():
            val = sum(float(v.loc[k, "L2023"]) * growth * float(v.loc[k, "share"]) * rules[k]["a"][F.GENS.index(g)]
                      for k in CATS for g in members)
            put("ltss_variants", variant, sub, "ltss_users_charge_bn", val, "bn")
    put("mcbs_2023", "", "hispanic_65p", "medicaid_per_beneficiary_with_medicaid_usd", m_dual, "usd")
    put("mcbs_2023", "", "hispanic_65p", "public_per_beneficiary_usd", public, "usd")
    with (F.HERE / "derived" / out_name).open("w", newline="") as fh:
        wr = csv.DictWriter(fh, fieldnames=list(rows[0]), lineterminator="\n")
        wr.writeheader()
        wr.writerows(rows)
    print(f"  wrote derived/{out_name} ({len(rows)} rows)")
    if FAILS:
        sys.exit(f"✗ {len(FAILS)} gate(s) failed")


if __name__ == "__main__":
    main()
