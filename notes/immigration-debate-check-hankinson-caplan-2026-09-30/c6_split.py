import csv, sys
base = "/Users/alien/Projects/immigration-research/infra/immigration-fiscal/main_case_decomposition_2026_09_29/derived/"
groups = {
 "means_tested_cash_food_housing_credits": ["cash_food_housing_benefits", "refundable_credits"],
 "medicaid_incl_uncompensated": ["medicaid"],
 "social_security_medicare": ["social_security_medicare"],
 "schools_k12": ["schools"],
 "colleges_other_education": ["colleges_other_education"],
 "justice": ["justice"],
 "health_veterans": ["health_veterans"],
 "roads_econ_affairs": ["roads_economic_affairs"],
 "per_head_govt_enterprises": ["per_head_government_and_enterprises"],
 "care_shelter_audit": ["care_shelter_audit_constants"],
 "receipts": ["income_taxes","payroll_taxes","consumption_taxes","property_taxes","production_term","other_receipts"],
}
for fn in ["decomposition_lines_sept29.csv", "decomposition_lines_sept29_cash.csv"]:
    rows = [r for r in csv.DictReader(open(base+fn)) if r["part"]=="total"]
    d = {r["line_group"]:(float(r["low_bn"]), float(r["high_bn"])) for r in rows}
    tot = [sum(v[i] for v in d.values()) for i in (0,1)]
    print(f"\n== {fn}: total low/high = {tot[0]:.2f} / {tot[1]:.2f}")
    for g, lines in groups.items():
        v = [sum(d[l][i] for l in lines) for i in (0,1)]
        print(f"{g:42s} {v[0]:8.1f} / {v[1]:8.1f}   share of net {100*v[0]/tot[0]:6.1f}% / {100*v[1]/tot[1]:6.1f}%")
    spend = [sum(v[i] for k,v in d.items() if k not in groups["receipts"]) for i in (0,1)]
    print(f"{'gross spending charged':42s} {spend[0]:8.1f} / {spend[1]:8.1f}")
    ben = [sum(d[l][i] for l in groups["means_tested_cash_food_housing_credits"]+groups["medicaid_incl_uncompensated"]) for i in (0,1)]
    ben_ss = [ben[i] + d["social_security_medicare"][i] for i in (0,1)]
    sch = [d["schools"][i] for i in (0,1)]
    print(f"means-tested benefits (cash/food/housing/credits + Medicaid): {ben[0]:.1f}/{ben[1]:.1f} = {100*ben[0]/tot[0]:.0f}%/{100*ben[1]/tot[1]:.0f}% of net")
    print(f"  + Social Security/Medicare: {ben_ss[0]:.1f}/{ben_ss[1]:.1f} = {100*ben_ss[0]/tot[0]:.0f}%/{100*ben_ss[1]/tot[1]:.0f}% of net")
    print(f"schools: {100*sch[0]/tot[0]:.0f}%/{100*sch[1]/tot[1]:.0f}%")
    rest = [tot[i]-ben_ss[i]-sch[i] for i in (0,1)]
    print(f"net remaining after removing all benefits incl SS/Medicare and schools: {rest[0]:.1f}/{rest[1]:.1f}")
    rest2 = [tot[i]-ben[i] for i in (0,1)]
    print(f"net remaining after removing means-tested only: {rest2[0]:.1f}/{rest2[1]:.1f}")
    rest3 = [tot[i]-ben[i]-sch[i] for i in (0,1)]
    print(f"net remaining after removing means-tested and schools: {rest3[0]:.1f}/{rest3[1]:.1f}")
