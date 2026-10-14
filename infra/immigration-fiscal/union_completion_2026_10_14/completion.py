"""Union completion, own-record pricing, replicate uncertainty and explicit loss arms.

Run after snapshot.cjs:
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/union_completion_2026_10_14/completion.py
All upstream inputs are read-only. Fixed engine amounts are spread with the
member kernel, with its person pension/on-books rules; omitted persons take
their own keys at those G3+ rates. Unsupported keys take a G3+ five-year age
rate, explicitly listed. All 160 replicate denominators are recomputed.
"""
from __future__ import annotations

import argparse
import csv
import gc
import hashlib
import json
import math
import resource
import sys
import time
from pathlib import Path

sys.dont_write_bytecode = True
import numpy as np
import pandas as pd
import pyarrow as pa

from person_adapter import SOURCE, kernel

HERE = Path(__file__).resolve().parent
FISCAL = HERE.parent
OUT = HERE / "derived"
GATES = []
FALLBACK_IDS = {"tenant_occupied_property"}
JOB_IDS = {"corporate_capital", "corporate_labor", "remaining_production_property", "other_production_taxes"}


def gate(name, ok, **detail):
    GATES.append(dict(gate=name, passed=bool(ok), **detail))
    if not ok:
        raise RuntimeError(f"[BLOCKED] {name}: {detail}")


def sdr(x):
    x = np.asarray(x, float)
    return float(np.sqrt(4 / 160 * np.square(x[1:] - x[0]).sum()))


def record(x):
    return dict(estimate=float(x[0]), se=sdr(x))


def sha(path):
    with path.open("rb") as f:
        return hashlib.file_digest(f, "sha256").hexdigest()


def pin_inputs(init=False):
    rels = [
        str(SOURCE.relative_to(FISCAL)),
        "within_group_distribution_2026_09_29/_cache/oct14/lines.json",
        "within_group_distribution_2026_09_29/_cache/sept29/person_accrual.parquet",
        "within_group_distribution_2026_09_29/derived/sept29/person_accrual_model.json",
        "generation_account_2026_09_24/_cache/asec25_generation.parquet",
        "generation_account_2026_09_24/frame.py", "generation_account_2026_09_24/keys.py",
        "cps_imputation_keys_2026_09_23/common.py",
        "gen_ledger_extension_2026_09_16/_cache/asecpub25csv.zip",
        "main_case_2026_10_14/package.cjs", "main_case_2026_10_14/derived/summary.json",
        "main_case_2026_10_14/derived/corrections.json", "main_case_2026_10_14/derived/corrections_cash.json",
        "generation_account_2026_09_24/derived/generation_corrections_oct14_cash.json",
        "mexican_origin_population_total_2026_09_19/dt_replication.py",
        "added_age_mix_2026_10_07/derived/g3_age_keys.json",
        "added_age_mix_2026_10_07/derived/age_mix.json",
    ]
    path = HERE / "inputs/pins.json"
    current = {r: sha(FISCAL / r) for r in rels}
    if init:
        gate("no existing pins overwritten", not path.exists())
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(dict(source="Existing pinned account inputs, no download", sha256=current), indent=2)+"\n")
    expected = json.loads(path.read_text())["sha256"]
    gate("initial source set remains pinned", set(current) <= set(expected))
    gate("all source and kernel hashes match pins", {r:sha(FISCAL/r) for r in expected} == expected)
    gate("primary CPS hash is the account's", current["gen_ledger_extension_2026_09_16/_cache/asecpub25csv.zip"]
         == "318845a2b5e0034eb2973898de1738f4df0025727de38499e7669cb9c0deef0b")


def csv_out(name, rows):
    with (OUT / name).open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]), lineterminator="\n")
        w.writeheader()
        w.writerows(rows)


def masks(d, F):
    civ, union, gens = F.masks(d)
    native = d.PRCITSHP.isin([1, 2, 3]).to_numpy()
    us_f = d.PEFNTVTY.isin(F.US_AREAS).to_numpy()
    us_m = d.PEMNTVTY.isin(F.US_AREAS).to_numpy()
    missing = civ & native & d.PRDTHSP.eq(1).to_numpy() & ~union
    central = missing & (us_f ^ us_m)
    return civ, union, gens, missing, central, us_f, us_m


def siblings(d, F, civ, union):
    parents = F.parent_rows(d)
    a, b = np.maximum(parents[:, 0], 0), np.maximum(parents[:, 1], 0)
    born = d.PENATVTY.to_numpy()
    native = d.PRCITSHP.isin([1, 2, 3]).to_numpy()
    us = np.isin(born, F.US_AREAS)
    mex = d.PRDTHSP.eq(1).to_numpy()
    # Two linked parents, exactly one US-area-born Mexican-origin parent,
    # the other foreign-born outside Mexico. Biological central; all-types arm.
    pair = ((us[a] & mex[a] & ~us[b] & (born[b] != 303))
            | (us[b] & mex[b] & ~us[a] & (born[a] != 303)))
    base = civ & native & d.A_AGE.lt(18).to_numpy() & (parents >= 0).all(axis=1) & pair
    # Exclude parent-birthplace coding inconsistent with the claimed universe.
    us_f = d.PEFNTVTY.isin(F.US_AREAS).to_numpy()
    us_m = d.PEMNTVTY.isin(F.US_AREAS).to_numpy()
    consistent = (us_f ^ us_m) & ~d.PEFNTVTY.eq(303).to_numpy() & ~d.PEMNTVTY.eq(303).to_numpy()
    bio = d.PEPAR1TYP.eq(1).to_numpy() & d.PEPAR2TYP.eq(1).to_numpy()
    arms = {"biological": base & consistent & bio, "all_parent_types": base & consistent}
    for name, m in arms.items():
        gate(f"{name} nonreporters are outside union and two-US-parent loss universe",
             not (m & ~mex & union).any() and not (m & us_f & us_m).any())
    return arms, mex, parents


def initial_counts():
    import importlib.util
    spec = importlib.util.spec_from_file_location("count_kernel", SOURCE)
    H = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(H)
    d = H.load_frame()
    civ, union, gens, missing, central, us_f, us_m = masks(d, H.F)
    extra_rows = np.flatnonzero(missing)
    arms, mex, parents = siblings(d, H.F, civ, union)
    # Counts of omitted natives have unchanged row4 weights; gates below trace
    # row4 on the whole frame before the pricing calculation.
    W = d[H.F.REPS].to_numpy(float)
    cuts = {"father_US_mother_other": missing & us_f & ~us_m,
            "mother_US_father_other": missing & us_m & ~us_f,
            "neither_US": missing & ~us_f & ~us_m,
            "central_one_US": central, "all_omitted": missing}
    for name, m in cuts.items():
        gap = float(np.abs(W[union | m].sum(axis=0, dtype=np.longdouble)
                            - W[union].sum(axis=0, dtype=np.longdouble)
                            - W[m].sum(axis=0, dtype=np.longdouble)).max())
        gate(f"{name} expansion conserves every weight column", gap < 1e-6, tolerance_people=1e-6)
    # On arm64 macOS longdouble is float64. Compensated sums avoid a
    # multi-micro-person summation artifact without weakening the gate.
    partition_totals = {k: np.array([math.fsum(W[m,j]) for j in range(161)])
                        for k,m in (("members",civ & union),("others",civ & ~union),("all",civ))}
    gap = float(np.abs(partition_totals["members"]+partition_totals["others"]-partition_totals["all"]).max())
    gate("national civilian classification conserves all weights", gap < 1e-6,
         tolerance_people=1e-6, max_gap_people=gap)
    age = d.A_AGE.to_numpy()
    bands = np.minimum(age // 5, 16)
    rows = []
    for name, m in cuts.items():
        for band in [-1, *range(17)]:
            here = m if band == -1 else m & (bands == band)
            v = W[here].sum(axis=0)
            rows.append(dict(group=name, age_band="all" if band == -1 else (f"{band*5}-{band*5+4}" if band<16 else "80+"),
                             records=int(here.sum()), people=v[0], se_people=sdr(v)))
    loss = {}
    ratios = {}
    for name, m in arms.items():
        all_n, id_n, lost_n = (W[x].sum(axis=0) for x in (m, m & mex, m & ~mex))
        gate(f"{name} loss denominator positive in every replicate", (id_n > 0).all())
        rate = lost_n / all_n
        ratio = lost_n / id_n
        ratios[name] = ratio
        loss[name] = dict(records=int(m.sum()), identifier_records=int((m & mex).sum()),
                          lost_records=int((m & ~mex).sum()), all_people=record(all_n),
                          identifiers=record(id_n), nonreporters=record(lost_n), loss_rate=record(rate),
                          ratio=record(ratio))
    other = np.where(us_f, d.PEMNTVTY, d.PEFNTVTY)
    births = []
    for typ in ["one_US", "neither_US"]:
        m = central if typ == "one_US" else cuts["neither_US"]
        for field, codevals in (("other_parent" if typ == "one_US" else "father", other if typ == "one_US" else d.PEFNTVTY.to_numpy()),
                                *([] if typ == "one_US" else [("mother", d.PEMNTVTY.to_numpy())])):
            for code in np.unique(codevals[m]):
                here = m & (codevals == code)
                births.append(dict(group=typ, parent=field, country_code=int(code), records=int(here.sum()), **record(W[here].sum(axis=0))))
    overlap = dict(omitted_records=int(missing.sum()), one_US_records=int(central.sum()),
                   under18_people=record(W[missing & (age < 18)].sum(axis=0)),
                   with_member_parent_people=record(W[missing & np.any((parents>=0) & union[np.maximum(parents,0)], axis=1)].sum(axis=0)),
                   two_US_parent_omitted_records=int((missing & us_f & us_m).sum()))
    # A native reporting parent's own birthplace-of-parent fields identify
    # children with a Mexico-born grandparent, separating the case's C3 blend
    # from later losses. The child's age is observed in both classes.
    p0, p1 = np.maximum(parents[:,0],0), np.maximum(parents[:,1],0)
    native_mex_parent = np.where(np.isin(d.PENATVTY.to_numpy()[p0], H.F.US_AREAS) & mex[p0], p0, p1)
    grandparent_mex = (d.PEFNTVTY.eq(303).to_numpy() | d.PEMNTVTY.eq(303).to_numpy())[native_mex_parent]
    counts_replicates = {"reporter_central_by_age": np.stack([W[central & (bands==b)].sum(axis=0) for b in range(17)]),
                         "reporter_all_by_age": np.stack([W[missing & (bands==b)].sum(axis=0) for b in range(17)])}
    for name, class_mask in (("g3_rate",grandparent_mex),("later",~grandparent_mex)):
        m = arms["biological"] & ~mex & class_mask
        counts_replicates[f"observed_{name}_by_age"] = np.stack([W[m & (bands==b)].sum(axis=0) for b in range(17)])
        overlap[f"observed_loss_{name}"] = dict(records=int(m.sum()),people=record(W[m].sum(axis=0)))
    counts_replicates["loss_ratio"] = ratios["biological"]
    # Literal siblings: same linked parent pair, with at least one reporting child.
    family_key = pd.MultiIndex.from_arrays([d.PH_SEQ, np.minimum(parents[:,0],parents[:,1]),
                                           np.maximum(parents[:,0],parents[:,1])])
    reporting_pairs = family_key[arms["biological"] & mex]
    literal = arms["biological"] & ~mex & family_key.isin(reporting_pairs)
    overlap["nonreporter_with_reporting_sibling"] = dict(records=int(literal.sum()),people=record(W[literal].sum(axis=0)))
    gate("omitted masks partition", np.array_equal(cuts["father_US_mother_other"] | cuts["mother_US_father_other"]
         | cuts["neither_US"], missing))
    gate("omitted membership and original union disjoint", not (missing & union).any())
    # Only retain compact counts/masks; release this frame before the kernel run.
    observed_masks = {name: np.flatnonzero(m & ~mex) for name,m in arms.items()}
    # Need outside vectors for measured nonreporting children as well as omitted identifiers.
    extra_rows = np.unique(np.concatenate([extra_rows, *observed_masks.values()]))
    from job_record_key import job_record_taxes
    jobs = job_record_taxes(d, W, extra_rows, gens)
    for g in jobs["source_gates"]:
        gate("job_source: " + g["gate"], g["passed"])
    for name, gap in jobs["national_closure_gap_bn"].items():
        gate(f"job {name} national closure", gap < 1e-6, max_gap_bn=gap, tolerance_bn=1e-6)
    for name, gap in jobs["baseline_gap_bn"].items():
        gate(f"job {name} original G3 positive control", gap < 1e-6, max_gap_bn=gap, tolerance_bn=1e-6)
    info = dict(extra_rows=extra_rows, missing=missing[extra_rows], central=central[extra_rows],
                age=age[extra_rows], loss_masks={k: np.isin(extra_rows, v) for k,v in observed_masks.items()},
                counts=rows, loss=loss, birthplace=births, overlap=overlap,
                ratio_replicates=ratios["biological"], job=jobs, counts_replicates=counts_replicates)
    del d, W
    gc.collect()
    pa.default_memory_pool().release_unused()
    return info


def price(basis, info):
    start = time.perf_counter()
    K = kernel(info["extra_rows"], basis, gate)
    W, d, rows_u = K["W"], K["d"], K["rows_u"]
    Wu = W[rows_u]
    Wo = W[info["extra_rows"]]
    age_u = np.minimum(d.A_AGE.to_numpy()[rows_u] // 5, 16)
    age_o = np.minimum(info["age"] // 5, 16)
    g3u = K["gens"]["G3plus"][rows_u]
    gen_summary = json.loads((FISCAL / "generation_account_2026_09_24/derived/generation_summary_oct14.json").read_text())
    credit_item = next(i for i in gen_summary["items"]["split"]["a"] if i["id"] == "child_credits")
    added_prices = json.loads((OUT / "added_band_prices.json").read_text())
    for g in added_prices["gates"]:
        gate("added_price: " + g["name"], g["pass"], max_gap_bn=g["max_gap_bn"])
    fallback, totals, bands_out, line_rows = [], {}, {}, []
    gate("row4 weights unchanged for omitted natives", np.array_equal(
        Wo, d.loc[info["extra_rows"], K["F"].REPS].to_numpy(float)) if "F" in K else
        np.array_equal(Wo, d.loc[info["extra_rows"], [f"pwwgt{i}" for i in range(161)]].to_numpy(float)))
    for end in ["low", "high"]:
        own = np.zeros_like(Wo)
        band_amount = np.zeros((17,161))
        control = np.zeros(161)
        for p in K["pieces"][end]:
            x = p.get("alt_tax", p.get("alt", {}).get("person", p["x"]))
            xo = p.get("outside_tax", p.get("outside_alt", p["outside_x"]))
            # Cash carries recorded SS/Medicare benefits, so no person accrual vector.
            den = x @ Wu
            if np.any(den == 0) or not np.any(x):
                control += p["bn"]
                continue
            coeff = p["bn"] / den
            control += (x @ Wu) * coeff
            if p["g"] != "G3plus":
                continue
            if p["id"] in JOB_IDS:
                # The old household allocator distributes these totals on
                # incidence vectors. New members under v7 take job-industry
                # keys; the exact source-lane linearization replaces them.
                continue
            # Existing R6 is a calibrated aggregate crossing adjustment. It is
            # recomputed jointly on the new membership, not extrapolated once
            # on new records and then counted again as a household delta.
            credit_bn = 0.0
            if p["id"] == "refundable_tax_credits" or (p["id"] == "federal_income_tax" and p["bn"] < 0):
                row = next(r for r in K["lines"]["generations"]["G3plus"][end]["rows"] if r["id"] == p["id"])
                active = [e for e in credit_item["edits"] if e["line"] == p["id"] and
                          (e["side"] == "spending" or e["scenario"] == row["scenario"])]
                shift = sum(q["bn"]["G3plus"]["personal"] for e in active for q in e["parts"])
                credit_bn = shift * (1 if row["side"] == "spending" else -1) * row["response"]
            outside_coeff = (p["bn"]-credit_bn) / den
            rate = np.stack([(x[g3u & (age_u==b)] @ Wu[g3u & (age_u==b)]) * outside_coeff
                             / Wu[g3u & (age_u==b)].sum(axis=0) for b in range(17)])
            band_amount += rate
            use_fallback = p["id"] in FALLBACK_IDS
            # A union-only key means no identified outside record has an evaluable key.
            # Its zero must not silently mean no fiscal cost.
            if use_fallback:
                eidx = 0 if end == "low" else 1
                exact = np.array([r["g3_fallback_line_bn_per_person"][p["id"]][basis][eidx]
                                  for r in added_prices["rates"]])
                band_amount -= rate
                rate = np.repeat(exact[:,None],161,axis=1)
                band_amount += rate
            cost = rate[age_o] * Wo if use_fallback else xo[:,None] * outside_coeff[None,:] * Wo
            own += cost
            if use_fallback:
                fallback.append(dict(basis=basis,end=end,line=p["id"],category=p["cat"],rule="G3+ five-year band rate"))
            line_rows.append(dict(basis=basis,end=end,line=p["id"],category=p["cat"],
                                  method="age_band" if use_fallback else "own_record",
                                  central_bn=cost[info["central"]].sum(axis=0)[0],
                                  all_bn=cost[info["missing"]].sum(axis=0)[0]))
        residual = sum(K["residual"][end].values())
        want = K["lines"]["union"][end]["cost_bn"]
        gap = float(np.abs(control + residual - want).max())
        gate(f"{basis} {end} union reproduced every replicate", gap < 1e-6,
             tolerance_bn=1e-6, max_gap_bn=gap, engine_bn=want)
        # Constants have no own-record rule: G3+ residual spread per head, the
        # same age-invariant per-head profile used by added-age pricing.
        eidx = 0 if end == "low" else 1
        constant = np.array([r["g3_fallback_line_bn_per_person"]["lane_constants"][basis][eidx]
                             for r in added_prices["rates"]])
        own += constant[age_o,None] * Wo
        band_amount += constant[:,None]
        line_rows.append(dict(basis=basis,end=end,line="lane_constants",category="residual",method="age_band",
                              central_bn=(constant[age_o,None]*Wo)[info["central"]].sum(axis=0)[0],
                              all_bn=(constant[age_o,None]*Wo)[info["missing"]].sum(axis=0)[0]))
        fallback.append(dict(basis=basis,end=end,line="lane_constants",category="residual",rule="case's added-people G3+ band rate"))
        for line, cost in info["job"]["outside_bn"].items():
            response = info["job"]["responses"][line][end]
            own -= response * cost
            band_amount -= response * info["job"]["g3_age_rates_bn"][line]
            line_rows.append(dict(basis=basis,end=end,line=line,category="taxes",method="own job industry",
                                  central_bn=-response*cost[info["central"]].sum(axis=0)[0],
                                  all_bn=-response*cost[info["missing"]].sum(axis=0)[0]))
        bands_out[end] = band_amount
        ident = {k: own[m].sum(axis=0) for k,m in (("central",info["central"]),("all",info["missing"]))}
        for k in ("central","all"):
            exported = math.fsum(r[k+"_bn"] for r in line_rows if r["basis"]==basis and r["end"]==end)
            gate(f"{basis} {end} exported {k} lines close", abs(exported-ident[k][0])<1e-6,
                 max_gap_bn=abs(exported-ident[k][0]),tolerance_bn=1e-6)
        idcounts = {k: Wo[m].sum(axis=0) for k,m in (("central",info["central"]),("all",info["missing"]))}
        # Replicate ratio from raw linked children is calculated below from masks.
        # Reconstruct denominator counts from the count kernel's retained arrays.
        ratio = np.asarray(info["ratio_replicates"])
        nbyband = np.stack([Wo[info["central"] & (age_o == b)].sum(axis=0) for b in range(17)])
        added_n = nbyband * ratio[None,:]
        implied_cost = (added_n * band_amount).sum(axis=0)
        observed_cost = {}
        for name,m in info["loss_masks"].items():
            n = np.stack([Wo[m & (age_o==b)].sum(axis=0) for b in range(17)])
            observed_cost[name] = (n * band_amount).sum(axis=0)
        totals[end] = dict(engine_bn=want, identified={k:record(v) for k,v in ident.items()},
                           identified_people={k:record(v) for k,v in idcounts.items()},
                           implied_loss_people=record(added_n.sum(axis=0)), implied_loss_bn=record(implied_cost),
                           measured_nonreporter_bn={k:record(v) for k,v in observed_cost.items()},
                           central_plus_implied_bn=record(ident["central"]+implied_cost),
                           all_plus_implied_bn=record(ident["all"]+implied_cost),
                           central_plus_observed_bn=record(ident["central"]+observed_cost["biological"]))
        # Retain full replicate sums for exact later credit adjustments.
        totals[end]["replicates"] = dict(central=ident["central"].tolist(), all=ident["all"].tolist(),
                                         implied_loss=implied_cost.tolist(), observed_loss=observed_cost["biological"].tolist())
    band_rows = []
    for end, rates in bands_out.items():
        for b in range(17):
            band_rows.append(dict(basis=basis,end=end,age_band=(f"{b*5}-{b*5+4}" if b<16 else "80+"),
                                  rule="G3+ distribution band surrogate before exact sibling pricing",
                                  bn_per_person=rates[b,0],se_bn_per_person=sdr(rates[b])))
    elapsed = time.perf_counter()-start
    del K, d, W, Wu, Wo
    gc.collect()
    pa.default_memory_pool().release_unused()
    print(f"{basis}: priced and controlled in {elapsed:.2f}s", flush=True)
    return totals, fallback, line_rows, band_rows


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--init-pins", action="store_true")
    args = parser.parse_args()
    started = time.perf_counter()
    pin_inputs(args.init_pins)
    info = initial_counts()
    summary = {"scope":"Candidate, not adopted; income year 2024, v7 personal 16/11, responses and national amounts fixed",
               "counts":info["overlap"], "identity_loss": info["loss"], "pricing":{}}
    lines, fallback, band_rows = [], [], []
    for basis in ["set", "cash"]:
        results, fb, lr, br = price(basis, info)
        summary["pricing"][basis] = results
        fallback += fb
        lines += lr
        band_rows += br
    peak = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024**3
    gate("process below 2.5GiB", peak < 2.5, peak_GiB_limit=2.5)
    OUT.mkdir(exist_ok=True)
    csv_out("counts.csv", info["counts"])
    csv_out("parent_birthplaces.csv", info["birthplace"])
    csv_out("pricing_lines.csv", lines)
    csv_out("band_rates.csv",band_rows)
    csv_out("fallback_lines.csv", fallback)
    (OUT / "summary.json").write_text(json.dumps(summary, indent=2)+"\n")
    (OUT / "count_replicates.json").write_text(json.dumps({k:v.tolist() for k,v in info["counts_replicates"].items()},indent=2)+"\n")
    (OUT / "gates.json").write_text(json.dumps(GATES, indent=2)+"\n")
    elapsed = time.perf_counter()-started
    # Wall time belongs in logs, not fingerprinted deterministic outputs.
    print(json.dumps(dict(elapsed_seconds=elapsed, peak_GiB=peak, all_gates=len(GATES))))
    print(json.dumps({b:{e:r["identified"] for e,r in t.items()} for b,t in summary["pricing"].items()}))


if __name__ == "__main__":
    main()
