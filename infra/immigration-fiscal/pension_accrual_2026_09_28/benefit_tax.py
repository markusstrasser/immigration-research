"""Federal income tax on 2024 Social Security benefits, for the group's tax units and for all tax units (step 1 of
BRIEF_net_of_tax.md).

The benefit tax of a tax unit is its federal income tax with its Social Security benefits less its tax without them.
Every CPS ASEC 2025 tax unit (income year 2024) is run twice through Tax-Calculator 6.8.2, current law:
  * tax units, income mapping and the calculator call are the tax lane's (tax_rerun_acs_2026_09_17: cps_tax.person_table
    and income_map, units.build_frame, taxcalc_io.run), imported read-only; nothing in that lane is written;
  * two income mappings. `census_income` (central) is the tax lane's full mapping plus retirement-account
    distributions (DST_VAL1 + DST_VAL2, as taxable IRA distributions), capital gains (CAP_VAL, as long-term gains)
    and survivor and disability income (SUR_VAL1 + SUR_VAL2 + DIS_VAL1 + DIS_VAL2, as taxable pensions): the income
    the Census tax model puts in AGI (the AGI and taxable-benefit checks below). `full` is the tax lane's mapping as
    it stands;
  * the benefit tax after all credits, less the net investment income tax (NIIT is chapter 2A and not income tax
    under section 86), for rates; and before refundable credits, less the NIIT (c09200 - niit, the concept of the
    Census FEDTAX_BC the case keys federal income tax by: FEDTAX_AC = FEDTAX_BC - EITC - ACTC), for the case's
    receipts.

Allocation to persons:
  * rates: each return's benefit tax to its filers in proportion to their own benefits; dependents who file no return
    of their own keep their benefits untaxed, as in the tax lane;
  * the case's key: each return's amount to the filer who carries the Census tax unit's AGI and FEDTAX_BC ("personal",
    specification 11), then summed over the SPM unit and split equally among its members ("shared", specification
    48), as full_account_receipts_2026_09_20/builder.py allocates FEDTAX_BC.

Gates (each stops with [BLOCKED]): with benefits in, the tax before refundable credits reproduces the Census FEDTAX_BC
total within the tax lane's gate band (0.85-1.15) for the nation and for the group; every return's benefit tax is
conserved by both allocations. Reported, never gated: the same ratios for units with benefits; on returns with
benefits that the Census model files, the AGI match and the taxable benefits against the Census model's (its AGI
less Tax-Calculator's AGI without benefits); the national rate against TR 2025's 2024 income from taxation of
benefits over OASDI cost; and a ceiling on state tax on the group's benefits (its benefits in the nine states that tax
some, at the top rate among them). Standard errors: the 160 replicate weights, 4/160 x the sum of squared deviations.

Writes derived/benefit_tax.json and derived/benefit_tax.csv. Run from the repository root, before pension_accrual.py:
  OPENBLAS_NUM_THREADS=1 uv run --no-project --with "taxcalc==6.8.2" python3 infra/immigration-fiscal/pension_accrual_2026_09_28/benefit_tax.py
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

sys.dont_write_bytecode = True   # read-only imports from other lanes: write nothing beside them

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

HERE = Path(__file__).resolve().parent
FISCAL = HERE.parent
OUT = HERE / "derived"
TAX_LANE = FISCAL / "tax_rerun_acs_2026_09_17"
sys.path.insert(0, str(HERE))
import sources as S  # noqa: E402  this lane's TR readers; imported before the tax lane puts its folders first

sys.path.insert(0, str(TAX_LANE))
import cps_tax as T  # noqa: E402  the tax lane: CPS state, tax units, income mappings

TC, U, ext = T.TC, T.U, T.ext
TARGETS = {"G1": "mexico_born", "G2": "mexican_second_gen", "G3plus": "mexican_third_plus_selfid"}
MAPPINGS = ["census_income", "full"]
CENTRAL_MAPPING = "census_income"
GATE_BAND = (0.85, 1.15)          # the tax lane's gate 1 band (tax_rerun_acs_2026_09_17/cps_tax.py)
TR_MISS = 0.25                    # a miss this large against the Trustees is a finding (the brief)
EXTRA = ["AGI", "DST_VAL1", "DST_VAL2", "CAP_VAL", "SUR_VAL1", "SUR_VAL2", "DIS_VAL1", "DIS_VAL2"]
for _f in EXTRA:
    if _f not in ext.base.PERSON:
        ext.base.PERSON.append(_f)
NEEDED = ["c09200", "niit", "c02500"]
TC.OUTPUTS = TC.OUTPUTS + [k for k in NEEDED if k not in TC.OUTPUTS]
IMPORTED = [TAX_LANE / f for f in ("cps_tax.py", "units.py", "taxcalc_io.py")]
# The states that taxed some Social Security benefits in tax year 2024 (Kansas, Missouri and Nebraska exempted them
# from 2024), each starting from the federally taxable amount; the top rate among them is Minnesota's 9.85%. Only a
# bound: no state line in the case plainly carries a state tax on benefits.
STATES_TAXING_BENEFITS_2024 = {8: "CO", 9: "CT", 27: "MN", 30: "MT", 35: "NM", 44: "RI", 49: "UT", 50: "VT", 54: "WV"}
TOP_STATE_RATE = 0.0985
STATE_SOURCES = ["https://www.fool.com/retirement/2024/11/08/41-states-that-dont-tax-social-security-benefits/",
                 "https://dontmesswithtaxes.com/9-states-join-uncle-sam-in-taxing-at-least-some-social-security-benefits/",
                 "https://www.aol.com/3-states-stopped-taxing-social-145544667.html"]


def blocked(msg: str):
    raise SystemExit(f"[BLOCKED] {msg}")


def sdr(v: np.ndarray) -> tuple[float, float]:
    """Point estimate (full weight) and the replicate standard error."""
    v = np.asarray(v, dtype=float)
    return float(v[0]), float(np.sqrt(4 / 160 * np.square(v[1:] - v[0]).sum()))


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def incomes(d: pd.DataFrame, mapping: str, with_benefits: bool) -> dict:
    inc = T.income_map(d, "full")
    if mapping == "census_income":
        other = (d.SUR_VAL1 + d.SUR_VAL2 + d.DIS_VAL1 + d.DIS_VAL2).to_numpy(float)
        inc = dict(inc, e01400=(d.DST_VAL1 + d.DST_VAL2).to_numpy(float), p23250=d.CAP_VAL.to_numpy(float),
                   e01500=inc["e01500"] + other, e01700=inc["e01700"] + other)
    elif mapping != "full":
        raise ValueError(mapping)
    if not with_benefits:
        inc = dict(inc, e02400=np.zeros(len(d)))
    return inc


def carriers(d: pd.DataFrame, p: pd.DataFrame) -> np.ndarray:
    """Row of the filer who carries each return's tax in the Census file (the largest |AGI| + |FEDTAX_BC|; the head
    when none carries any): the Census records a tax unit's AGI and FEDTAX_BC on one person."""
    filer = (p.ret_role <= 1).to_numpy()
    score = np.where(filer, np.abs(d.AGI.to_numpy(float)) + np.abs(d.FEDTAX_BC.to_numpy(float)), -1.0)
    t = pd.DataFrame({"ret": p.ret_unit.to_numpy(), "score": score, "role": p.ret_role.to_numpy(),
                      "row": np.arange(len(p))})
    t = t[filer].sort_values(["ret", "score", "role"], ascending=[True, False, True], kind="stable")
    first = t.groupby("ret", sort=True).head(1)
    return first.set_index("ret").row


def main() -> None:
    OUT.mkdir(exist_ok=True)
    if not T.CPS_ZIP.exists():
        blocked(f"CPS zip not found: {T.CPS_ZIP}")
    state = ext.build(argparse.Namespace(cps_zip=T.CPS_ZIP))
    d, W = state["d"], state["person_weights"]
    n = len(d)
    civ = (d.PRPERTYP.eq(2) | d.A_AGE.lt(15)).to_numpy()
    masks = {g: state["group"][c] & civ for g, c in TARGETS.items()}
    masks["union"] = masks["G1"] | masks["G2"] | masks["G3plus"]
    masks["nation"] = civ
    p, diag = T.person_table(d)
    n_ret = int(p.ret_unit.max()) + 1
    ret = p.ret_unit.to_numpy()
    filer = (p.ret_role <= 1).to_numpy()
    ss = d.SS_VAL.to_numpy(float)
    ss_filed = np.where(filer, ss, 0.0)
    unit_ss = np.bincount(ret, weights=ss_filed, minlength=n_ret)
    by_benefit = np.divide(ss_filed, unit_ss[ret], out=np.zeros(n), where=unit_ss[ret] > 0)
    carry = carriers(d, p)
    if len(carry) != len(np.unique(ret[filer])):
        blocked("a return without a filer to carry its tax")
    idx, n_units = state["index"], state["n_units"]

    def personal(unit_value: np.ndarray) -> np.ndarray:
        out = np.zeros(n)
        out[carry.to_numpy()] = unit_value[carry.index.to_numpy()]
        if not np.allclose(out.sum(), unit_value[carry.index.to_numpy()].sum()):
            blocked("the personal allocation does not conserve the returns' dollars")
        return out

    def shared(person_value: np.ndarray) -> np.ndarray:
        return ext.allocate(np.bincount(idx, weights=person_value, minlength=n_units), idx, np.ones(n, bool), n_units)

    census_key = {"personal": d.FEDTAX_BC.to_numpy(float)}
    census_key["shared"] = shared(census_key["personal"])
    tot = lambda v, m: (np.where(m, v, 0.0) @ W)   # noqa: E731  weighted totals, full weight and replicates
    with_ss_unit = unit_ss > 0
    on_benefit_unit = with_ss_unit[ret]

    results, rows, taxable_by = {}, [], {}
    for mapping in MAPPINGS:
        runs = {}
        for with_benefits in (True, False):
            frame = U.build_frame(p, incomes(d, mapping, with_benefits), n_ret, eic_child=p.eic_child.to_numpy())
            runs[with_benefits] = TC.run(frame)
            print(f"[taxcalc] {mapping}, benefits {'in' if with_benefits else 'out'}: {len(frame):,} returns", flush=True)
        after = {k: r["iitax"] - r["niit"] for k, r in runs.items()}
        before = {k: r["c09200"] - r["niit"] for k, r in runs.items()}
        d_after, d_before = after[True] - after[False], before[True] - before[False]
        if np.abs(np.where(with_ss_unit, 0.0, d_after)).max() > 1e-6 or np.abs(np.where(with_ss_unit, 0.0, d_before)).max() > 1e-6:
            blocked(f"{mapping}: a return without benefits has a benefit tax")
        bt = d_after[ret] * by_benefit                      # benefit tax after credits, by own benefits
        taxable = runs[True]["c02500"][ret] * by_benefit     # benefits included in AGI, by own benefits
        taxable_by[mapping] = taxable
        if not np.allclose(np.bincount(ret, weights=bt, minlength=n_ret), np.where(with_ss_unit, d_after, 0.0), atol=1e-6):
            blocked(f"{mapping}: the benefit allocation does not conserve the returns' benefit tax")
        key = {"personal": personal(d_before)}
        key["shared"] = shared(key["personal"])
        level = {"personal": personal(before[True])}
        level["shared"] = shared(level["personal"])
        nat_bt, nat_ss = tot(bt, civ), tot(ss, civ)
        nat_rate = nat_bt / nat_ss
        res = dict(groups={}, key={}, gate={})
        for g, m in masks.items():
            b, s_ = tot(bt, m), tot(ss, m)
            rate = b / s_
            rec = dict(benefits_bn=sdr(s_ / 1e9), benefit_tax_bn=sdr(b / 1e9), rate=sdr(rate),
                       relative_rate=sdr(rate / nat_rate), taxable_benefits_bn=sdr(tot(taxable, m) / 1e9),
                       benefit_tax_before_refundable_bn=sdr(tot(d_before[ret] * by_benefit, m) / 1e9),
                       recipients_m=float((W[:, 0] * (ss > 0) * m).sum() / 1e6),
                       recipient_records=int(((ss > 0) & m).sum()))
            res["groups"][g] = rec
            for measure in ("benefits_bn", "benefit_tax_bn", "rate", "relative_rate", "taxable_benefits_bn",
                            "benefit_tax_before_refundable_bn"):
                rows.append(dict(mapping=mapping, group=g, measure=measure, value=rec[measure][0], se=rec[measure][1]))
        for alloc in ("personal", "shared"):
            res["key"][alloc] = dict(
                group_benefit_tax_bn=sdr(tot(key[alloc], masks["union"]) / 1e9),
                group_key_taxcalc_bn=float(tot(level[alloc], masks["union"])[0] / 1e9),
                national_key_taxcalc_bn=float(tot(level[alloc], civ)[0] / 1e9),
                group_key_census_bn=float(tot(census_key[alloc], masks["union"])[0] / 1e9),
                national_key_census_bn=float(tot(census_key[alloc], civ)[0] / 1e9),
                by_generation_benefit_tax_bn={g: float(tot(key[alloc], masks[g])[0] / 1e9) for g in TARGETS})
            k = res["key"][alloc]
            k["group_share_of_national_key_taxcalc"] = k["group_benefit_tax_bn"][0] / k["national_key_taxcalc_bn"]
            k["group_share_of_national_key_census"] = k["group_benefit_tax_bn"][0] / k["national_key_census_bn"]
        # gate: with benefits in, the tax before refundable credits against the Census FEDTAX_BC (personal allocation)
        for name, m in (("nation", civ), ("group", masks["union"]), ("nation_units_with_benefits", civ & on_benefit_unit),
                        ("group_units_with_benefits", masks["union"] & on_benefit_unit)):
            tc_, cen = float(tot(level["personal"], m)[0]), float(tot(census_key["personal"], m)[0])
            res["gate"][name] = dict(taxcalc_bn=tc_ / 1e9, census_fedtax_bc_bn=cen / 1e9, ratio=tc_ / cen,
                                     in_band=bool(GATE_BAND[0] <= tc_ / cen <= GATE_BAND[1]))
        # returns with benefits that the Census model files (it records AGI 0 for non-filers): taxcalc's AGI against
        # the Census AGI on the carrier, and taxcalc's taxable benefits against the Census model's, its AGI less
        # taxcalc's AGI without benefits (exact where the two agree on the other income)
        ri, pr = carry.index.to_numpy(), carry.to_numpy()
        agi_tc, agi_out, taxable_tc = runs[True]["c00100"][ri], runs[False]["c00100"][ri], runs[True]["c02500"][ri]
        agi_cen = d.AGI.to_numpy(float)[pr]
        wt = W[pr, 0]
        sel = with_ss_unit[ri] & civ[pr] & (d.FILESTAT.to_numpy()[pr] != 6)
        implied = agi_cen - agi_out
        res["census_filed_returns_with_benefits"] = dict(
            returns=int(sel.sum()),
            agi_taxcalc_bn=float((wt * agi_tc)[sel].sum() / 1e9), agi_census_bn=float((wt * agi_cen)[sel].sum() / 1e9),
            agi_ratio=float((wt * agi_tc)[sel].sum() / (wt * agi_cen)[sel].sum()),
            agi_share_within_2_dollars=float((np.abs(agi_tc - agi_cen) <= 2)[sel].mean()),
            taxable_benefits_taxcalc_bn=float((wt * taxable_tc)[sel].sum() / 1e9),
            taxable_benefits_census_implied_bn=float((wt * implied)[sel].sum() / 1e9),
            taxable_benefits_ratio=float((wt * taxable_tc)[sel].sum() / (wt * implied)[sel].sum()))
        results[mapping] = res

    cen = results[CENTRAL_MAPPING]
    for name in ("nation", "group"):
        if not cen["gate"][name]["in_band"]:
            blocked(f"{CENTRAL_MAPPING}: taxcalc / Census FEDTAX_BC for the {name} is {cen['gate'][name]['ratio']:.3f}, "
                    f"outside {GATE_BAND}")
    # the Trustees: 2024 income from taxation of benefits (OASDI, Table VI.A3; HI, Medicare TR Table II.B1) over cost
    a3 = S.combined_operations_vi_a3().set_index("year").loc[2024]
    hi = S.quotes()["mtr_hi_2024_operations"]["value"]
    tob = float(a3.taxation_of_benefits + hi["taxation_of_benefits_bn"])
    tr = dict(oasdi_tob_bn=float(a3.taxation_of_benefits), hi_tob_bn=hi["taxation_of_benefits_bn"], cost_bn=float(a3.cost),
              benefits_bn=float(a3.benefits), share_of_cost=tob / float(a3.cost), share_of_benefits=tob / float(a3.benefits))
    checks = {}
    for mapping, res in results.items():
        mine = res["groups"]["nation"]["rate"][0]
        gap = mine / tr["share_of_cost"] - 1
        checks[mapping] = dict(national_rate=mine, trustees_share_of_cost=tr["share_of_cost"], gap=gap,
                               finding=bool(abs(gap) > TR_MISS))
    # the bound on a state tax on the group's 2024 benefits: its benefits, and its federally taxable benefits, in the
    # states that tax some, at the top rate among them
    taxing = d.GESTFIPS.isin(list(STATES_TAXING_BENEFITS_2024)).to_numpy()
    grp_in = masks["union"] & taxing
    state_bound = dict(
        states=STATES_TAXING_BENEFITS_2024, sources=STATE_SOURCES, top_rate=TOP_STATE_RATE, mapping=CENTRAL_MAPPING,
        group_benefits_bn=sdr(tot(ss, grp_in) / 1e9), group_taxable_benefits_bn=sdr(tot(taxable_by[CENTRAL_MAPPING], grp_in) / 1e9),
        group_share_of_its_benefits=float(tot(ss, grp_in)[0] / tot(ss, masks["union"])[0]),
        nation_share_of_its_benefits=float(tot(ss, civ & taxing)[0] / tot(ss, civ)[0]),
        recipient_records=int(((ss > 0) & grp_in).sum()))
    state_bound["ceiling_all_benefits_bn"] = state_bound["group_benefits_bn"][0] * TOP_STATE_RATE
    state_bound["ceiling_taxable_benefits_bn"] = state_bound["group_taxable_benefits_bn"][0] * TOP_STATE_RATE
    out = dict(
        taxcalc_version=TC.version(), cps_zip=str(T.CPS_ZIP.relative_to(FISCAL.parents[1])),
        cps_sha256=ext.base.sha(T.CPS_ZIP), script_sha256=sha(Path(__file__)),
        imported_sha256={str(f.relative_to(FISCAL.parents[1])): sha(f) for f in IMPORTED},
        central_mapping=CENTRAL_MAPPING, mappings=MAPPINGS, gate_band=GATE_BAND, unit_diagnostics=diag,
        results=results, trustees_2024=tr, trustees_check=checks, state_tax_bound=state_bound,
        units="$bn at CPS ASEC 2025 weights (income year 2024); rates are benefit tax over Social Security benefits; "
              "each measure is [estimate, replicate SE]")
    (OUT / "benefit_tax.json").write_text(json.dumps(out, indent=1, sort_keys=True, default=float) + "\n")
    pd.DataFrame(rows).to_csv(OUT / "benefit_tax.csv", index=False, float_format="%.6f", lineterminator="\n")
    for mapping, res in results.items():
        g = res["groups"]
        print(f"[{mapping}] nation {g['nation']['benefit_tax_bn'][0]:.2f}bn of {g['nation']['benefits_bn'][0]:.1f}bn "
              f"({100 * g['nation']['rate'][0]:.2f}%); group {g['union']['benefit_tax_bn'][0]:.3f}bn of "
              f"{g['union']['benefits_bn'][0]:.2f}bn ({100 * g['union']['rate'][0]:.2f}%), relative "
              f"{g['union']['relative_rate'][0]:.3f} (SE {g['union']['relative_rate'][1]:.3f}); G1/G2/G3+ relative "
              + "/".join(f"{g[k]['relative_rate'][0]:.3f}" for k in TARGETS))
        c = res["census_filed_returns_with_benefits"]
        print(f"  gate FEDTAX_BC: " + ", ".join(f"{k} {v['ratio']:.3f}" for k, v in res["gate"].items())
              + f"; Census-filed benefit returns: AGI {c['agi_ratio']:.3f} (exact {c['agi_share_within_2_dollars']:.3f}), "
              f"taxable benefits {c['taxable_benefits_ratio']:.3f}")
        print(f"  key: " + ", ".join(f"{a} group {v['group_benefit_tax_bn'][0]:.3f}bn / national {v['national_key_taxcalc_bn']:.1f}bn"
                                     for a, v in res["key"].items()))
        print(f"  Trustees 2024: {100 * tr['share_of_cost']:.2f}% of cost; this {100 * checks[mapping]['national_rate']:.2f}% "
              f"(gap {100 * checks[mapping]['gap']:+.1f}%)")
    print(f"[state] group benefits in the nine taxing states {state_bound['group_benefits_bn'][0]:.2f}bn "
          f"({100 * state_bound['group_share_of_its_benefits']:.1f}% of its benefits; nation "
          f"{100 * state_bound['nation_share_of_its_benefits']:.1f}%), federally taxable "
          f"{state_bound['group_taxable_benefits_bn'][0]:.2f}bn; ceiling at {100 * TOP_STATE_RATE:.2f}%: "
          f"{state_bound['ceiling_taxable_benefits_bn']:.3f}bn (all benefits {state_bound['ceiling_all_benefits_bn']:.3f}bn)")
    print(f"[written] benefit_tax.json, benefit_tax.csv")


if __name__ == "__main__":
    main()
