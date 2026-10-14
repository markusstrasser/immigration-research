"""Conditional corporate-rent arms, one change from frozen v7. No source rates typed from prose.

Run: OPENBLAS_NUM_THREADS=1 uv run --no-project python3 {lane}/rents.py
All outputs deterministic. Runtime/memory print to stdout, never into fingerprinted data.
"""
from __future__ import annotations

import csv
import hashlib
import json
import re
import resource
import subprocess
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
GATES = []


def gate(name, ok, value=None):
    GATES.append(dict(name=name, passed=bool(ok), value=value))
    if not ok:
        raise ValueError(f"[BLOCKED] {name}: {value}")


def pdf_text(path):
    return subprocess.run(["pdftotext", "-layout", str(path), "-"], check=True, capture_output=True, text=True).stdout


def one(pattern, text, label):
    matches = re.findall(pattern, text, re.S)
    if len(matches) != 1:
        raise ValueError(f"[BLOCKED] {label}: expected one source match, got {len(matches)}")
    return matches[0]


def verify_pins():
    pins = json.loads((HERE / "inputs/pins.json").read_text())
    for row in pins["files"]:
        path = HERE / row["path"] if row["root"] == "lane" else ROOT / row["path"]
        gate(f"source pin: {row['path']}", path.is_file() and hashlib.sha256(path.read_bytes()).hexdigest() == row["sha256"])
    return pins


def source_rates():
    tp = pdf_text(HERE / "_cache/treasury_tp5.pdf")
    sup = float(one(r"we find that (\d+) percent of current corporate taxable income is due to supernormal\s+returns", tp, "Treasury supernormal share")) / 100
    norm = float(one(r"of the remaining (\d+)\s+percent of the corporate tax on the taxable income attributable to normal returns", tp, "Treasury normal share")) / 100
    gate("Treasury shares close (1e-12)", abs(sup + norm - 1) < 1e-12)
    gate("TP5 rent incidence is an assumption, not a measured composition", bool(re.search(r"We assume the source of the supernormal return is pure rent,\s+not risk", tp)))
    wp = pdf_text(HERE / "_cache/treasury_wp111.pdf")
    pf = one(r"averaging\s+(\d+)\s+percent\s+from\s+1992.2002\s+and\s+(\d+)\s+percent\s+from\s+2003.2013", wp, "Power/Frerick normal shares")
    gate("WP111 excess includes risk and other categories", bool(re.search(r"including returns to risk, entrepreneurial labor, decreasing returns to scale, market power,\s+luck", wp)))
    html = (HERE / "_cache/corporate_rate_2024.html").read_text()
    corp = float(one(r"shall be 21 percent of taxable income", html, "2024 corporate rate").split()[2]) / 100
    # Parse the highest ordinary bracket from the IRS 2024 worksheet. This is a sensitivity ceiling,
    # not an estimated marginal rate of qualified-plan participants.
    irs = pdf_text(HERE / "_cache/irs_1040_2024.pdf")
    ordinary_cap = max(map(float, re.findall(r"\+\s+(\d+)%", irs))) / 100
    gate("IRS withdrawal treatment includes tax-free qualified Roth distribution", "Distribution code Q" in irs and "Roth IRA" in irs)
    policy = list(csv.DictReader((HERE / "_cache/equity_cbo_policy_2024.csv").open()))
    row = next(r for r in policy if r["year"] == "2024")
    fields = ["dividend_inc_tax_rate", "cap_gains_short_term_tax_rate", "cap_gains_long_term_tax_rate", "cap_gains_at_death_tax_rate", "ret_plan_deferred_tax_rate"]
    tax = {f: float(row[f]) for f in fields}
    env = {r[0]: float(r[1]) for r in csv.reader((HERE / "_cache/equity_cbo_environment_2024.csv").open()) if len(r) == 2 and r[0] != "parameter"}
    retained = env["c_corp_equity_retained_earnings_share"]
    repurchase = env["c_corp_equity_repurchases_share"]
    # Retained-earnings share is a financing parameter, not a share of this rent's payout.
    dividend_share = 1-repurchase
    gain_share = 1-dividend_share
    st, death = env["cap_gains_short_term_share"], env["cap_gains_at_death_share"]
    lt = 1-st-death
    gain_rate = st*tax["cap_gains_short_term_tax_rate"] + lt*tax["cap_gains_long_term_tax_rate"] + death*tax["cap_gains_at_death_tax_rate"]
    gate("payout partition closes, gains not taxed again as dividends (1e-12)", abs(dividend_share + gain_share-1) < 1e-12)
    gate("realization partition closes (1e-12)", min(st, death, lt) >= 0 and abs(st+death+lt-1) < 1e-12)
    return dict(supernormal=sup, normal=norm, power_frerick_normal=list(map(lambda x: float(x)/100, pf)),
                corporate_rates=[corp, 0.25], corporate_rate_note="21% parsed federal statutory rate; 25% combined-rate sensitivity ASSUMPTION, not a measured effective rent rate",
                qualified_withdrawal_cap=ordinary_cap, policy=tax, retained=retained, repurchase=repurchase,
                dividend_share=dividend_share, gain_share=gain_share, gains_rate=gain_rate)


def counterfactual(phi, job_source, rent_source, corp_rate, residence_rate, domestic_share, arm, end):
    if not (0 <= phi <= 1 and 0 < corp_rate < 1 and 0 <= residence_rate <= domestic_share <= 1):
        raise ValueError("invalid rent/ownership/tax assumptions")
    if arm == "fixed":
        return dict(source_change_bn=phi*job_source if end == "low" else 0., residence_loss_bn=0.,
                    domestic_owner_loss_after_residence_tax_bn=0., after_corporate_rent_bn=0., delta_bn=phi*job_source if end == "low" else 0.)
    after = phi*rent_source*(1-corp_rate)/corp_rate
    source = phi*(job_source-rent_source) if end == "low" else -phi*rent_source
    residence = after*residence_rate
    private = after*domestic_share-residence
    return dict(source_change_bn=source, residence_loss_bn=residence,
                domestic_owner_loss_after_residence_tax_bn=private, after_corporate_rent_bn=after, delta_bn=source-residence)


def main():
    started = time.perf_counter()
    verify_pins()
    rates = source_rates()
    case = json.loads((HERE / "derived/case_inputs.json").read_text())
    gate("TP5 source share matches frozen v7", abs(rates["normal"]-case["corporate"]["normal_share"]) < 1e-12)
    # Re-parse the source PDF column on every build; do not trust model-extracted numeric JSON.
    raw = HERE / "_cache"
    subprocess.run(["pdftoppm","-f","71","-l","71","-scale-to","4000","-png","-singlefile",
                    str(raw/"equity_govinfo_hearing_2024.pdf"),str(raw/"rents_table71")],check=True)
    subprocess.run(["magick",str(raw/"rents_table71.png"),"-colorspace","gray","-crop","1450x390+750+920","+repage",
                    "-resize","250%","-threshold","80%",str(raw/"rents_table_crop.png")],check=True)
    subprocess.run(["magick",str(raw/"rents_table_crop.png"),"-crop","420x760+2590+135","+repage",str(raw/"rents_column.png")],check=True)
    ocr = subprocess.run(["tesseract",str(raw/"rents_column.png"),"stdout","--psm","6","-c","tessedit_char_whitelist=$,0123456789"],
                         capture_output=True,text=True,check=True).stdout
    values = [int(x.replace(",","")) for x in re.findall(r"\$([\d,]+)",ocr)]
    gate("ownership primary Table5 OCR has total plus all eight rows",len(values)==9,values)
    published_total=values[0]
    owners=dict(zip(("foreign","nonprofits","government","life","db","dc","ira","taxable"),values[1:],strict=True))
    denominator = sum(owners.values())
    shares = {k: v/denominator for k,v in owners.items()}
    gate("ownership mass conserved after explicit rounded-table normalization (1e-12)", abs(sum(shares.values())-1)<1e-12)
    domestic = 1-shares["foreign"]
    taxable = shares["taxable"]
    retirement = shares["db"]+shares["dc"]+shares["ira"]
    life = shares["life"]
    household_claim_share=taxable+shares["dc"]+shares["ira"]+life
    cash_dividend = taxable*rates["dividend_share"]*rates["policy"]["dividend_inc_tax_rate"]
    payout_proxy = taxable*(rates["dividend_share"]*rates["policy"]["dividend_inc_tax_rate"]+rates["gain_share"]*rates["gains_rate"])
    insurance_proxy = payout_proxy + life*rates["policy"]["ret_plan_deferred_tax_rate"]
    retirement_upper = insurance_proxy + retirement*rates["qualified_withdrawal_cap"]
    residence = {
        "dividend_only_cash": cash_dividend,
        "taxable_payout_no_deferral": payout_proxy,
        "taxable_plus_insurance_no_deferral": insurance_proxy,
        "all_retirement_at_top_bracket_no_deferral": retirement_upper,
    }
    gate("ownership weighted rates within domestic income", all(0<=r<=domestic for r in residence.values()))
    # The national corporate line includes mining; v7 holds mining fixed. Retain that boundary for demand rents.
    nat = json.loads((ROOT / "infra/immigration-fiscal/job_capital_taxes_2026_10_14/derived/summary.json").read_text())
    mining = sum(nat["mining"]["national_bn"]["corporate"].values())
    eligible = case["corporate"]["national_bn"]-mining
    itemrows = list(csv.DictReader((ROOT / "infra/immigration-fiscal/job_capital_taxes_2026_10_14/derived/items.csv").open()))
    jrow = next(r for r in itemrows if r["row"]=="central" and r["reading"]=="low" and r["allocation"]=="personal" and r["line"]=="corporate")
    job_se = float(jrow["se_bn"])
    gate("eligible corporate national closes source lane (1e-6bn)", abs(eligible-float(jrow["base_bn"]))<1e-6, eligible)
    gate("corporate union positive control (1e-9bn)", abs(case["corporate"]["union_bn"]+float(jrow["value_bn"]))<1e-9)
    # Rounded source table cells are retained as printed, without hiding their discrepancy.
    summary = dict(rates=rates, ownership=dict(amounts_bn=owners, published_total_bn=published_total,
        row_sum_bn=denominator, rounding_residual_bn=denominator-published_total, shares=shares,
        rule="normalize printed row sum; do not fabricate a balancing cell", domestic_share=domestic, retirement_share=retirement),
        residence_rates=residence, eligible_national_corporate_bn=eligible,
        retained_owner_rule="Displayed incremental residence loss assumes e_tax=0: no overlap with taxes already lost on removed owners in frozen individual-income receipts. Actual extra loss is (1-e_tax)*R, where e_tax is the fraction already counted, not identified. Private exclusion e_private is separate and not identified.",
        caveat="Phi and disappearance elasticities unmeasured. Ownership 2022 transferred to 2024 ASSUMPTION; all-domestic private loss upper bound includes institutions and group owners. No retirement flow automatically belongs in income-year-2024 cash.")
    rows, thresholds = [], []
    for scope in ("union", "lineage"):
        job = rates["supernormal"]*case["corporate"][f"{scope}_bn"]
        demand = rates["supernormal"]*eligible*case["consumption"][scope]
        gate(f"{scope}: demand plus remaining rents close national (1e-9bn)", abs(demand + rates["supernormal"]*eligible*(1-case["consumption"][scope])-rates["supernormal"]*eligible)<1e-9)
        for key, rent in (("jobs",job),("demand",demand)):
            for rate_name, r in residence.items():
                for t in rates["corporate_rates"]:
                    for phi in (0., .1, .25, .5, 1.):
                        for arm in ("vanishing", "fixed"):
                            if arm == "fixed" and (key != "jobs" or rate_name != "dividend_only_cash" or t != rates["corporate_rates"][0]):
                                continue
                            for end, ei in (("low",0),("high",1)):
                                z = counterfactual(phi, job, rent, t, r, domestic, arm, end)
                                gate(f"partition {scope}/{key}/{rate_name}/{t}/{phi}/{arm}/{end} (1e-9bn)",
                                     abs(z["residence_loss_bn"]+z["domestic_owner_loss_after_residence_tax_bn"]-domestic*z["after_corporate_rent_bn"])<1e-9)
                                baseline = case[f"baseline_{scope}_bn"][ei]
                                cash = case[f"baseline_{scope}_cash_bn"][ei]
                                # Only the identified-union job key has a preserved corporate replicate SE.
                                # The lineage conditional SE holds its added-person job tax and all parameters fixed.
                                se = None
                                if key == "jobs":
                                    coeff = phi*rates["supernormal"]*(1 if arm=="fixed" and end=="low" else
                                        0 if arm=="fixed" else -(r*(1-t)/t + (1 if end=="high" else 0)))
                                    se = abs(coeff)*job_se
                                rows.append(dict(scope=scope,population=case["population"][scope],key=key,arm=arm,phi=phi,
                                    corporate_rate=t,residence_rule=rate_name,residence_rate=r,end=end,
                                    supernormal_job_source_bn=job,supernormal_rent_source_bn=rent,**z,
                                    baseline_bn=baseline,result_bn=baseline+z["delta_bn"],
                                    baseline_cash_bn=cash,result_cash_same_flow_assumption_bn=cash+z["delta_bn"],
                                    e_tax_assumed=0.,private_owner_group_share_assumed=0.,
                                    fiscal_delta_if_all_residence_loss_already_counted_bn=z["source_change_bn"],
                                    fiscal_plus_all_domestic_claim_upper_bound_delta_bn=z["delta_bn"]-z["domestic_owner_loss_after_residence_tax_bn"],
                                    private_loss_if_group_owned_everything_bn=0.,
                                    household_account_claim_loss_upper_bn=z["after_corporate_rent_bn"]*household_claim_share-z["residence_loss_bn"]
                                        +(z["after_corporate_rent_bn"]*shares["db"]*rates["qualified_withdrawal_cap"] if rate_name=="all_retirement_at_top_bracket_no_deferral" else 0.),
                                    e_private_max_for_domestic_claim_loss_over_5bn=(1-5/z["domestic_owner_loss_after_residence_tax_bn"]) if z["domestic_owner_loss_after_residence_tax_bn"] else None,
                                    conditional_replicate_se_delta_bn=se,
                                    clears_5bn=abs(z["delta_bn"])>=5))
                    for end in ("low","high"):
                        z=counterfactual(1,job,rent,t,r,domestic,"vanishing",end)
                        thresholds.append(dict(scope=scope,key=key,residence_rule=rate_name,corporate_rate=t,end=end,
                            phi_for_5bn=5/abs(z["delta_bn"]) if z["delta_bn"] else None,
                            phi_for_residence_only_5bn=5/z["residence_loss_bn"] if z["residence_loss_bn"] else None))
        thresholds.append(dict(scope=scope,key="jobs",residence_rule="fixed",corporate_rate=None,end="low",phi_for_5bn=5/job,phi_for_residence_only_5bn=None))
    summary["gates"] = GATES
    summary["se_rule"] = "Jobs: propagate source lane's 160-replicate corporate SE linearly, conditional on phi, rates, ownership and added people; demand no exact-v7 joint replicates stored. No SE measures premise uncertainty."
    summary["household_claim_rule"]="Taxable+DC+IRA+life-insurance ownership; government, nonprofits and DB excluded. Conditional on losses passing through to holders. Removed-group share unknown, so [0,reported] bounds other-resident private loss. All-domestic field also includes institutions, not purely private welfare."
    for filename,data in (("arms.csv",rows),("thresholds.csv",thresholds)):
        with (HERE/"derived"/filename).open("w",newline="") as f:
            fields = list(data[0])
            writer=csv.DictWriter(f,fieldnames=fields,lineterminator="\n")
            writer.writeheader();writer.writerows(data)
    (HERE/"derived/summary.json").write_text(json.dumps(summary,indent=2)+"\n")
    elapsed=time.perf_counter()-started
    usage=resource.getrusage(resource.RUSAGE_SELF)
    print(f"PASS: {len(GATES)} gates; {len(rows)} arms; {elapsed:.3f}s; maxrss raw={usage.ru_maxrss}; ownership-weighted rates={residence}")


if __name__=="__main__":
    main()
