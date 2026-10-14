"""P7: observed food-aid receipt, conditional reverse volunteering, city-tax closure.

The food-aid files identify recipient households, not donated hours or displacement.
The 2015 organization/activity mix is transported explicitly as a sensitivity only.
No existing producer row or central is replaced. All CSVs use cost-positive signs.
"""
from __future__ import annotations

import ast
import csv
import gzip
import hashlib
import importlib.util
import json
import pathlib
import re
import resource
import subprocess
import time

import numpy as np
import pandas as pd

LANE = pathlib.Path(__file__).resolve().parent
FISCAL = LANE.parent
CACHE, OUT = LANE / "_cache", LANE / "derived"
GATES = []


def gate(name, condition, detail=""):
    GATES.append(dict(name=name, passed=bool(condition), detail=detail))
    assert condition, f"[BLOCKED] {name}: {detail}"


def write_csv(name, rows):
    with (OUT / name).open("w", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def pdf_text(name):
    return subprocess.run(["pdftotext", "-layout", str(CACHE / name), "-"], check=True,
                          capture_output=True, text=True).stdout


def source_pins():
    for pin in json.loads((LANE / "inputs/pins.json").read_text()):
        actual = hashlib.sha256((LANE / pin["file"]).read_bytes()).hexdigest()
        gate(f"source pin {pin['file']}", actual == pin["sha256"])


def union(d):
    return d.PENATVTY.eq(303) | d.PEMNTVTY.eq(303) | d.PEFNTVTY.eq(303) | d.PRDTHSP.eq(1)


def se(x):
    return float(np.sqrt(4 / 160 * np.square(x[1:] - x[0]).sum()))


def food(year):
    cols = ["QSTNUM", "PRTAGE", "PULINENO", "PRDTHSP", "PENATVTY", "PEFNTVTY", "PEMNTVTY",
            "HESC3", "HESC4", "HHSUPWGT", "PWSUPWGT", "HRSUPINT"]
    d = pd.read_csv(CACHE / f"dec{year % 100}pub.csv", usecols=cols)
    d["member"] = union(d)
    h = d.drop_duplicates("QSTNUM").copy()
    doc = pdf_text(f"cpsdec{year % 100}.pdf")
    for field in ("HESC3", "HESC4", "HRSUPINT"):
        tally = re.findall(rf"(?m)^{field}\s+1\s+(?:Yes|Interview)\s+(\d+)\s*$", doc)
        gate(f"{year} codebook unique tally {field}", len(tally) == 1)
        gate(f"{year} unweighted tally {field}", int(h[field].eq(1).sum()) == int(tally[0]))
    # Household fields repeat per member. Never sum their weights over person records.
    sizes = d.groupby("QSTNUM").agg(persons=("member", "size"), members=("member", "sum"))
    h = h.merge(sizes, on="QSTNUM", validate="one_to_one")
    h = h[h.HRSUPINT.eq(1) & h.HHSUPWGT.gt(0)].copy()
    r = pd.read_csv(CACHE / f"dec{year % 100}hhrep.csv")
    r.columns = r.columns.str.upper()
    h = h.merge(r, on="QSTNUM", how="left", validate="one_to_one")
    gate(f"{year} every interviewed HH has replicate weights", h.HHSUPWGT0.notna().all())
    gate(f"{year} replicate zero equals main weight", np.array_equal(h.HHSUPWGT, h.HHSUPWGT0))
    # The CSVs retain the dictionary's four implied decimals, unlike many ACS CSVs.
    w = h[[f"HHSUPWGT{i}" for i in range(161)]].to_numpy(float) / 1e4
    gate(f"{year} household-weight scale", 1e8 < w[:, 0].sum() < 2e8)
    share = (h.members / h.persons).to_numpy()
    rows, vectors = [], {}
    for label, mask in (("pantry", h.HESC3.eq(1)), ("free_meal", h.HESC4.eq(1)),
                        ("either", h.HESC3.eq(1) | h.HESC4.eq(1))):
        y = mask.to_numpy(float)
        total = w.T @ y
        member = w.T @ (y * share)
        outside = w.T @ (y * (1 - share))
        gate(f"{year} {label} beneficiary-weight conservation", np.max(np.abs(member + outside - total)) / 1e9 < 1e-6)
        s = member / total
        vectors[label] = (member, outside)
        # Unknown responses and screened-out households are not silently coded as no.
        # Only observed positive users enter the recipient-share denominator.
        rows.append(dict(year=year, service=label, recipient_hh=float(total[0]),
                         member_fractional_hh=float(member[0]), outside_fractional_hh=float(outside[0]),
                         member_share=float(s[0]), member_share_se=se(s),
                         member_fractional_hh_se=se(member),
                         any_member_recipient_hh=float(w[:, 0] @ (y * h.members.gt(0))),
                         member_persons_in_recipient_hh=float(w[:, 0] @ (y * h.members)),
                         unknown_pantry_hh=float(w[:, 0] @ h.HESC3.isin([-2, -3, -9])),
                         unknown_meal_hh=float(w[:, 0] @ h.HESC4.isin([-2, -3, -9])),
                         allocation="one equal service per observed recipient household; member fraction of household persons",
                         definition="Mexico birth or either parent Mexico birth or Mexican self-origin; monthly survey frame"))
    person = d[d.HRSUPINT.eq(1) & d.PWSUPWGT.gt(0)]
    members = float(person.loc[person.member, "PWSUPWGT"].sum() / 1e4)
    return rows, vectors, members


def cev():
    cols = ["QSTNUM", "OCCURNUM", "PRTAGE", "PRDTHSP", "PENATVTY", "PEFNTVTY", "PEMNTVTY",
            "PRSUPINT", "PRSUPVOL", "PWNRWGT", "PTS16E"]
    d = pd.read_csv(CACHE / "sep23pub.csv", usecols=cols)
    # Positive controls reproduce the extant lane's published national rate.
    d = d[d.PRSUPINT.eq(1) & d.PRTAGE.ge(16)].copy()
    d["member"] = union(d)
    r = pd.read_csv(CACHE / "sep23nrrep.csv")
    r.columns = r.columns.str.upper()
    d = d.merge(r, on=["QSTNUM", "OCCURNUM"], how="left", validate="one_to_one")
    gate("CEV every respondent matched", d.PWNRWGT0.notna().all())
    gate("CEV replicate zero matches", np.array_equal(d.PWNRWGT, d.PWNRWGT0))
    w = d[[f"PWNRWGT{i}" for i in range(161)]].to_numpy(float) / 1e4
    yes = d.PRSUPVOL.eq(1).to_numpy()
    nat_rate = w.T @ yes / w.sum(0)
    gate("CEV 2023 published 28.3% rounded rate", round(float(nat_rate[0]), 3) == .283)
    rows = []
    counts = {}
    for name, mask in (("national", np.ones(len(d), bool)), ("union", d.member), ("outside_union", ~d.member)):
        a = np.asarray(mask)
        population = w.T @ a
        count = w.T @ (a & yes)
        rate = count / population
        counts[name] = count
        rows.append(dict(group=name, population16=float(population[0]), volunteers=float(count[0]),
                         volunteers_se=se(count), formal_rate=float(rate[0]), formal_rate_se=se(rate)))
    gate("CEV volunteer count conservation", np.max(np.abs(counts["union"] + counts["outside_union"] - counts["national"])) / 1e9 < 1e-6)
    return rows, counts


def organization_mix():
    doc = pdf_text("cpssept15.pdf")
    cols = ["PRTAGE", "PRDTHSP", "PENATVTY", "PEMNTVTY", "PEFNTVTY", "PRSUPINT", "PRSUPVOL", "PWNRWGT",
            "PTS4M1", "PES85", "PES8A"] + [f"PES8{i}" for i in range(1, 14) if i != 5]
    positions = []
    for name in cols:
        match = re.findall(rf"(?mi)^{name}\s+\d+[^\n]*?\b(\d+)\s*-\s*(\d+)\s*$", doc)
        gate(f"2015 unique dictionary field {name}", len(match) == 1, str(match))
        positions.append((int(match[0][0]) - 1, int(match[0][1])))
    with gzip.open(CACHE / "sep15pub.dat.gz", "rt") as fh:
        records = [[int(line[a:b]) for a, b in positions] for line in fh]
    d = pd.DataFrame(records, columns=cols)
    for name in ("PES85", "PRSUPINT", "PRSUPVOL"):
        block = doc[doc.rindex(name):]
        match = re.search(r"<\s*1>\s+(?:Yes|Interview)\s+(\d+)", block)
        gate(f"2015 codebook tally found {name}", match is not None)
        gate(f"2015 unweighted tally {name}", int(d[name].eq(1).sum()) == int(match.group(1)))
    d = d[d.PRSUPINT.eq(1) & d.PRTAGE.ge(16) & d.PRSUPVOL.eq(1)].copy()
    d["member"] = union(d)
    w = d.PWNRWGT.to_numpy(float) / 1e4
    gate("2015 plausible volunteer population", 5e7 < w.sum() < 8e7)
    block = doc[doc.index("PTS4M1"):doc.index("PTS5M")]
    labels = {int(code): label.strip() for code, label in re.findall(r"(?m)^\s+(\d{1,2})\s+([^\n]+)$", block)}
    rows = []
    for name, mask in (("national", np.ones(len(d), bool)), ("union", d.member), ("outside_union", ~d.member)):
        ww = w * np.asarray(mask)
        for org in range(-9, 18):
            selected = d.PTS4M1.eq(org)
            if not selected.any():
                continue
            rows.append(dict(group=name, main_org_code=org, main_org_label=labels.get(org, "missing/unknown"), volunteers=float(ww @ selected),
                             share_of_volunteers=float(ww @ selected / ww.sum()),
                             food_activity_volunteers=float(ww @ (selected & d.PES85.eq(1)))))
    # PES85 is any food activity, not hours on that activity; this is NOT a food-hour share.
    outside = ~d.member
    any_food = d.PES85.eq(1)
    sole_food = any_food & d[[f"PES8{i}" for i in range(1, 14) if i != 5]].eq(2).all(axis=1)
    primary_food = sole_food | (any_food & d.PES8A.eq(5))
    shares = {"primary_food": float(w @ (outside & primary_food) / (w @ outside)),
              "any_food": float(w @ (outside & any_food) / (w @ outside))}
    gate("food volunteer share ordering", 0 <= shares["primary_food"] <= shares["any_food"] <= 1)
    gate("2015 organization counts close nationally", abs(sum(r["volunteers"] for r in rows if r["group"] == "national") - w.sum()) / 1e9 < 1e-6)
    return rows, shares


def legacy_constants():
    values = {}
    tree = ast.parse((LANE / "build_tables.py").read_text())
    for node in tree.body:
        if isinstance(node, ast.Assign) and isinstance(node.targets[0], ast.Tuple):
            names = [n.id for n in node.targets[0].elts]
            if names in (["RATE_H", "RATE_ALL"], ["HOURS", "VOLS", "VALUE"]):
                values.update(zip(names, ast.literal_eval(node.value)))
    gate("legacy valuation constants located", len(values) == 5)
    return values


def cities(n4, lineage_factor):
    path = FISCAL / "scale_spillovers_2026_09_23/arms.py"
    spec = importlib.util.spec_from_file_location("social_scale_arms", path)
    a = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(a)
    # Same context as population_basis/reeval.py, without changing its files.
    _, cry, _ = a.cry_regressions()
    nat = pd.read_csv(a.DERIVED / "pums_national.csv")
    allw = nat[nat.label.eq("all")].set_index("item").estimate
    wm = allw["workers_sc"] + allw["workers_ba"] + allw["workers_grad"]
    em = allw["earnings_sc"] + allw["earnings_ba"] + allw["earnings_grad"]
    rel = (em / wm) / ((allw["earnings"] - em) / (allw["workers"] - wm))
    s = cry["s_sc_cry_sample"]
    sw = pd.read_csv(a.DERIVED / "sample_weights.csv").set_index(["year", "cell"])
    ctx = {"cry_joint": cry, "shares": {"sc_cry": {"s": s, "theta": s * rel / (s * rel + 1 - s)},
                                          "ba_2000": {"s": float(sw.loc[(2000, "ba"), "worker_share"]),
                                                      "theta": float(sw.loc[(2000, "ba"), "income_share"])}}}
    _, params, _, fn, _ = next(x for x in a.joint_specs(ctx) if x[0].endswith("[central]"))
    pars = np.array([x[0] for x in params])
    summary = pd.read_csv(a.DERIVED / "summary.csv")
    old = summary[summary.table.eq("joint_grid") & summary.geography.eq("CZ 1990")].iloc[0]
    output = []
    for frame, scale in (("published_union", a.SCALE), ("identified_union_row4", n4 / a.ACS_GROUP)):
        a.SCALE = scale
        m = a.measures(a.cz_areas(a.load_cells()))
        gain, tax = a.gain_parts(m, fn(m, pars))
        gain, tax = gain / 1e9, tax / 1e9
        if frame == "published_union":
            gate("city earnings positive control", abs(gain - old.gain_bn) < 1e-9)
            gate("city tax positive control", abs(tax - old.induced_receipts_bn) < 1e-9)
        else:
            known = pd.read_csv(FISCAL / "population_basis_2026_09_29/derived/reeval.csv")
            target = -float(known[known.row.eq("scale_net_earnings")].row4_bn.iloc[0])
            gate("city row4 reproduces adopted whole earnings", abs(gain - target) < 1e-9)
        gate(f"city private plus tax {frame}", abs((gain - tax) + tax - gain) < 1e-12)
        output.append(dict(frame=frame, gross_earnings_bn=gain, induced_tax_bn=tax,
                           private_after_tax_bn=gain - tax, additional_tax_credit_bn=0.0,
                           low_end_delta_bn=0.0, high_end_delta_bn=0.0,
                           rate_hs_or_less=a.TAX["hsless"], rate_some_college_plus=a.TAX["more"],
                           overlap="included in scale_net_earnings, already counted whole; production P+F uses CES labour changes only"))
    v = output[-1]
    output.append(dict(v, frame="lineage_key_extrapolation", gross_earnings_bn=v["gross_earnings_bn"] * lineage_factor,
                       induced_tax_bn=v["induced_tax_bn"] * lineage_factor,
                       private_after_tax_bn=v["private_after_tax_bn"] * lineage_factor))
    return output


def main():
    start = time.perf_counter()
    import faulthandler
    faulthandler.dump_traceback_later(90, repeat=True)
    source_pins()
    foods, vecs, pops = [], {}, {}
    for year in (2023, 2024):
        rows, vecs[year], pops[year] = food(year)
        foods.extend(rows)
    write_csv("food_receipt.csv", foods)
    crows, counts = cev()
    write_csv("volunteering_supply.csv", crows)
    orgrows, mix = organization_mix()
    write_csv("volunteering_organization_types.csv", orgrows)
    print(f"CPS inputs parsed in {time.perf_counter() - start:.2f}s", flush=True)
    constants = legacy_constants()
    frames = pd.read_csv(FISCAL / "population_basis_2026_09_29/derived/frame_counts.csv").set_index("count")
    n4 = float(frames.loc["union|all", "row4"])
    adult = {f: float(frames.loc["union|18_plus", f] + frames.loc["union|12_17", f] / 3) for f in ("published", "row4")}
    variants = json.loads((FISCAL / "sept24_propagation_2026_09_24/derived/oct14/band_variants.json").read_text())
    keys = variants["lineage_social_keys"]
    gate("v7 personal end specifications", keys["low_end"]["specification"] == 16 and keys["high_end"]["specification"] == 11)
    gate("v7 both ends share adult multiplier", keys["low_end"]["adults"] == keys["high_end"]["adults"])
    adult_factor = 1 + keys["low_end"]["adults"]
    head_factor = 1 + keys["head_count"]
    unit = constants["VALUE"] / constants["HOURS"]
    mean_hours = constants["HOURS"] / constants["VOLS"]
    gross = {f: adult[f] * constants["RATE_H"] * mean_hours * unit / 1e9 for f in adult}
    original = pd.read_csv(OUT / "items.csv")
    old = original[original.item.eq("formal_volunteering_outside_group") & original.measure.eq("absolute")].iloc[0]
    gate("existing volunteering central positive control", round(-gross["published"] * .55, 4) == old.central_bn)
    basis = pd.read_csv(FISCAL / "population_basis_2026_09_29/basis.csv")
    vol_factor = float(basis[basis.row.eq("formal_volunteering_outside_group")].factor.iloc[0])
    paired = pd.read_csv(FISCAL / "population_basis_2026_09_29/derived/restated_pairing.csv")
    adopted_outward = -float(paired[paired.item.eq("formal_volunteering_outside_group")].restated.iloc[0])
    gate("adopted outgoing central and controlled rounding", round(-float(old.central_bn) * vol_factor, 6) == adopted_outward)
    flows, itemrows = [], []
    for year in (2023, 2024):
        member, outside = vecs[year]["either"]
        # Fractional household services per member; move to row4 without moving outsiders.
        ratio = n4 / pops[year]
        share = member * ratio / (outside + member * ratio)
        for frame, rec_factor, give_factor in (("identified_union_row4", 1., 1.),
                                               ("lineage_key_extrapolation", head_factor, adult_factor)):
            outward = adopted_outward * give_factor
            # Conditional dollar model: national mean hours, 2015 volunteer-person food-task share,
            # equal service per recipient HH, common output price, all labour domestically useful.
            for task, taskshare in mix.items():
                reverse = counts["outside_union"] * mean_hours * unit / 1e9 * taskshare * share * rec_factor
                for displacement in (0., .5, 1.):
                    incoming = float(reverse[0]) * displacement
                    flows.append(dict(year=year, frame=frame, food_task_proxy=task, displacement=displacement,
                                      volunteer_unit_usd_per_hour=unit, transported_food_task_person_share=taskshare,
                                      group_recipient_share_row4=float(share[0]), group_recipient_share_se=se(share),
                                      gross_in_receipt_share_conditional_se_bn=float(reverse[0]) * se(share) / float(share[0]),
                                      gross_group_production_bn=gross["row4"] * give_factor,
                                      gross_out_to_others_bn=outward, gross_in_from_others_proxy_bn=float(reverse[0]),
                                      displaced_in_bn=incoming, net_cost_bn=-outward + incoming,
                                      low_end_delta_bn=incoming, high_end_delta_bn=incoming,
                                      sampling_se_note="recipient-share and 2023 supply SEs separately reported; no joint SE across different surveys/year transport",
                                      valuation_status="conditional proxy, not observed volunteer hours received; displacement unidentified"))
            if year == 2024:
                high = next(r["gross_in_from_others_proxy_bn"] for r in reversed(flows) if r["food_task_proxy"] == "any_food")
                for item, lo, central, hi in (("formal_volunteering_reverse_food_proxy", 0., 0., high),
                                             ("formal_volunteering_net_food_proxy", -outward, -outward, -outward + high)):
                    itemrows.append(dict(item=item, group="mexican_origin", measure="absolute", low_bn=lo,
                                         central_bn=central, high_bn=hi, per_member_usd=central * 1e9 / (n4 * (head_factor if "lineage" in frame else 1)),
                                         evidence_level="scenario only; receipt observed, volunteer-hour allocation and displacement assumed",
                                         double_count_with="net row replaces formal_volunteering_outside_group; reverse row can add only once",
                                         method_note="2024 FSS either food program, 2015 any-food task share, 2023 outsiders, lane unit value; d=0..1; central held",
                                         frame=frame, comparator="without identified group, volunteers may redirect labour",
                                         beneficiary="other US residents", valuation="replacement wage for unpaid hours; no food/commodity value",
                                         overlap="unpaid labour outside receipts/spending; own-group work excluded; organization mix includes non-emergency food"))
    write_csv("volunteering_flows.csv", flows)
    write_csv("social_items.csv", itemrows)
    print(f"Volunteering scenarios built in {time.perf_counter() - start:.2f}s", flush=True)
    city = cities(n4, head_factor)
    write_csv("city_tax_decomposition.csv", city)
    integration = dict(status="beside; no new measured central", adopted_delta_bn=[0., 0.],
                       rows={"formal_volunteering_reverse_food_proxy": "conditional add-on to existing volunteering, already row4/lineage priced; do not rescale",
                             "formal_volunteering_net_food_proxy": "pre-P7 outgoing reference only; use delta columns on a consumer that separately adjusts the lineage boundary; never sum net with outgoing or reverse",
                             "city_tax_decomposition": "decomposition of existing scale_net_earnings; additional tax delta is exactly zero"},
                       delta_table={"file": "derived/volunteering_flows.csv",
                                    "keys": ["year", "frame", "food_task_proxy", "displacement"],
                                    "year": 2024, "columns": ["low_end_delta_bn", "high_end_delta_bn"],
                                    "applies_to": "fiscal-plus-social total only; identical on set and cash set; main fiscal account unchanged",
                                    "base": "existing outgoing credit; incoming displacement is the only change",
                                    "outside_supply_lineage": "holds measured outside-union supply fixed; added beneficiaries use the headcount key; recipient identity of added people unobserved"},
                       population={"identified_union": n4, "lineage": n4 * head_factor},
                       sources=[dict(file=p["file"], sha256=p["sha256"], url=p["url"]) for p in json.loads((LANE / "inputs/pins.json").read_text())],
                       unit_value_usd_hour=unit, national_mean_hours=mean_hours, food_person_shares_2015=mix,
                       gaps=["No observed volunteer hours or dollar services by beneficiary origin",
                             "No measured displacement elasticity; 0, 0.5, 1 are scenarios, not estimates",
                             "2023 CEV has no organization-type item; 2015 types/food activities transported",
                             "Monthly origin-union and case lineage differ; added people use case keys, not direct receipt observations",
                             "Food-task person share is not hours share; primary/any are alternative proxies, not statistical bounds",
                             "FSS covers household food aid, not all charity or volunteering; cannot identify total incoming net"])
    (OUT / "social_integration.json").write_text(json.dumps(integration, indent=2) + "\n")
    (OUT / "social_gates.json").write_text(json.dumps(GATES, indent=2) + "\n")
    elapsed = time.perf_counter() - start
    peak = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    print(f"PASS {len(GATES)} gates; {elapsed:.2f}s; peak RSS {peak / 1e6:.1f} MB (macOS bytes)")
    print("food shares", [(r["year"], r["service"], round(r["member_share"], 4)) for r in foods])
    print("food mix", mix)
    print("2024 flows", [(r["frame"], r["food_task_proxy"], round(r["gross_out_to_others_bn"], 4), round(r["gross_in_from_others_proxy_bn"], 4)) for r in flows if r["year"] == 2024 and r["displacement"] == 1])
    print("city tax", [(r["frame"], r["induced_tax_bn"], r["additional_tax_credit_bn"]) for r in city])
    faulthandler.cancel_dump_traceback_later()


if __name__ == "__main__":
    main()
