"""Pool ASEC personal tax keys, 2019–2025; read sibling lanes without modifying them.

AGI and tax dollars are put in income-year-2023 CPI-U dollars. The exact case
baseline retains 2025's nominal AGI. Historical years retain their own published
weights; only the supplementary 2025 row4 baseline reweights to the account frame.
Pooled SEs perturb one year's 160 SDR replicates at a time, holding all other
years fixed. Independence SE and the maximum-positive-covariance bound are both
reported: aligned replicate numbers do not identify cross-year covariance.
"""
from __future__ import annotations

import argparse
import csv
import gc
import hashlib
import importlib.util
import json
import resource
import sys
import time
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
FISCAL = HERE.parent
ROOT = FISCAL.parents[1]
OUT = HERE / "derived"
REPS = [f"pwwgt{i}" for i in range(161)]
PERSON = ["PH_SEQ", "PPPOS", "TAX_ID", "SPM_ID", "MARSUPWT", "A_AGE", "PRPERTYP", "PRCITSHP", "PENATVTY",
          "PEFNTVTY", "PEMNTVTY", "PRDTHSP", "PEHSPNON", "AGI", "FEDTAX_BC", "FEDTAX_AC", "STATETAX_A",
          "WSAL_VAL", "PTOTVAL", "SSI_VAL", "PAW_VAL", "CAP_VAL", "MCARE", "FILESTAT"]
SOURCES = {
    2019: (HERE / "_cache/asecpub19csv.zip", "88d8688ac5e5a1d4d4bd9daf72946d8fd34edda9360b3bbfde602d6ca55fb604"),
    2020: (FISCAL / "backcast_pandemic_measured_2026_09_28/_cache/asecpub20csv.zip", "f79430c5664745a2ae1c0f7fef615d93fa6b1933d0fe1dabb932ec52c73be591"),
    2021: (FISCAL / "backcast_pandemic_measured_2026_09_28/_cache/asecpub21csv.zip", "7196ff49c52f833f65c537d66a0c8cc1540a8e31711a09c3730c218b4486c1f4"),
    2022: (FISCAL / "latam_comparison_2026_09_17/_cache/2022/asecpub22csv.zip", "7338011adefca16dae30a4469ddaf0c01cef579b607b26b4bceec749376e4ac9"),
    2023: (FISCAL / "latam_comparison_2026_09_17/_cache/2023/asecpub23csv.zip", "d2e000250782adfbdd7f29c82b66d866591a30f0d330496698ec19f9c784ce11"),
    2024: (ROOT / "sources/immigration-fiscal/data/census/cps_asec_2024_march.zip", "cdb39cdac34bef99dd0940ab28e306f692404c2eea44d85dfd634214872a0a09"),
    2025: (ROOT / "sources/immigration-fiscal/data/external/stage3/census/cps_asec_2025/asecpub25csv.zip", "318845a2b5e0034eb2973898de1738f4df0025727de38499e7669cb9c0deef0b"),
}
CPI_PATH = FISCAL / "consumption_key_2026_09_24/_cache/sources/bls_cpi_u_2015_2024.json"


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


KEYS = load_module("top_share_case_keys", FISCAL / "tax_key_heldout_2026_09_28/keys.py")
BF = KEYS.benchmark_frame()
LABELS, _ = KEYS.irs_2023()
EDGES, _ = KEYS.bin_edges(LABELS)


def sha(path):
    with path.open("rb") as handle:
        return hashlib.file_digest(handle, "sha256").hexdigest()


def cpi():
    source = json.loads(CPI_PATH.read_text())
    series = source["Results"]["series"]
    assert len(series) == 1 and series[0]["seriesID"] == "CUUR0000SA0"
    values = {int(r["year"]): float(r["value"]) for r in series[0]["data"] if r["period"] == "M13"}
    assert set(range(2018, 2025)) <= values.keys() and values[2023] == 304.702
    return values


def band19(agi):
    return np.where(agi <= 0, 0, np.searchsorted(EDGES, agi, side="right") + 1)


def band14(bins):
    """0 = no AGI through $5k; 12 = $500k–1M; 13 = $1M+."""
    return np.minimum(np.maximum(bins - 1, 0), 13)


def load_year(year):
    path, pin = SOURCES[year]
    digest = sha(path)
    assert digest == pin, f"[BLOCKED] source changed: {path}"
    yy = str(year)[2:]
    with zipfile.ZipFile(path) as z:
        def member(name):
            matches = [n for n in z.namelist() if Path(n).name == name]
            assert len(matches) == 1, f"[BLOCKED] archive must contain exactly one {name}"
            return z.open(matches[0])
        d = pd.read_csv(member(f"pppub{yy}.csv"), usecols=PERSON)
        hh = pd.read_csv(member(f"hhpub{yy}.csv"), usecols=["H_SEQ", "GESTFIPS"])
        d = d.merge(hh.rename(columns={"H_SEQ": "PH_SEQ"}), on="PH_SEQ", how="left", validate="many_to_one")
        index = pd.MultiIndex.from_frame(d[["PH_SEQ", "PPPOS"]])
        assert index.is_unique and d.GESTFIPS.notna().all()
        # Every replicate aggregation scans a column. Keep those scans contiguous
        # rather than repeatedly traversing the full 161-column row stride.
        w = np.full((len(d), 161), np.nan, order="F")
        for chunk in pd.read_csv(member(f"asec_csv_repwgt_{year}.csv"), usecols=["h_seq", "PPPOS", *REPS], chunksize=20000):
            pos = index.get_indexer(pd.MultiIndex.from_frame(chunk[["h_seq", "PPPOS"]]))
            assert (pos >= 0).all()
            w[pos] = chunk[REPS].to_numpy(float)
    assert np.isfinite(w).all()
    np.testing.assert_allclose(d.MARSUPWT.to_numpy() / 100, w[:, 0], rtol=0, atol=.011)
    d["pwwgt0"] = w[:, 0]
    return d, w, digest


def aggregate(codes, values, w, size):
    """Small sufficient statistics; keep the full microdata to one year at a time."""
    return np.stack([np.bincount(codes, weights=values * w[:, r], minlength=size) for r in range(161)], axis=1)


def sdr(x):
    return np.sqrt(4 / 160 * np.square(x[..., 1:] - x[..., :1]).sum(axis=-1))


def divide(a, b):
    return np.divide(a, b, out=np.full_like(np.asarray(a, float), np.nan), where=np.asarray(b) != 0)


def ratio_summary(nums, dens):
    """Pooled ratio of real-dollar totals; each annual replicate perturbs that year only."""
    n = sum(x[..., 0] for x in nums)
    d = sum(x[..., 0] for x in dens)
    point = divide(n, d)
    annual_se = []
    for a, b in zip(nums, dens):
        perturb = divide(n[..., None] - a[..., :1] + a, d[..., None] - b[..., :1] + b)
        annual_se.append(sdr(perturb))
    return point, np.sqrt(np.square(annual_se).sum(axis=0)), np.sum(annual_se, axis=0)


def stats(d, w, real_factor, nominal=False):
    civ, union = BF.masks(d)
    hisp = d.PEHSPNON.eq(1).to_numpy() & civ
    groups = KEYS.cbo_groups(d)
    gi = pd.Categorical(groups, categories=BF.GROUPS).codes
    assert (gi >= 0).all()
    agi = d.AGI.to_numpy(float) * (1 if nominal else real_factor)
    b = band19(agi)
    fed = d.FEDTAX_BC.to_numpy(float) * (1 if nominal else real_factor)
    state = d.STATETAX_A.clip(lower=0).to_numpy(float) * (1 if nominal else real_factor)
    codes = gi * 14 + band14(b)
    cells = {}
    for key, value in (("total", fed * civ), ("union", fed * union)):
        cells[key] = aggregate(codes, value, w, len(BF.GROUPS) * 14).reshape(len(BF.GROUPS), 14, 161)
    cells["records"] = np.bincount(codes, weights=(union & (fed > 0)).astype(int), minlength=len(BF.GROUPS) * 14).reshape(len(BF.GROUPS), 14)
    bins = {}
    for key, value in (("total", fed * civ), ("union", fed * union), ("hispanic", fed * hisp),
                       ("union_carriers", (union & (fed > 0)).astype(float)),
                       ("hispanic_carriers", (hisp & (fed > 0)).astype(float))):
        bins[key] = aggregate(b, value, w, 19)
    for key, mask in (("union_records", union & (fed > 0)), ("hispanic_records", hisp & (fed > 0)),
                      ("all_records", civ & (fed > 0))):
        bins[key] = np.bincount(b, weights=mask.astype(int), minlength=19)
    scodes = d.GESTFIPS.to_numpy(int) * 14 + band14(b)
    states = {}
    for key, value in (("total_state", state * civ), ("union_state", state * union),
                       ("total_fedtax", fed * civ), ("union_fedtax", fed * union)):
        # State translation needs point estimates, not another 161-column tensor.
        states[key] = np.bincount(scodes, weights=value * w[:, 0], minlength=57 * 14).reshape(57, 14)
    states["union_records"] = np.bincount(scodes, weights=(union & (state > 0)).astype(int), minlength=57 * 14).reshape(57, 14)
    tax_union, tax_all = union & (fed > 0), civ & (fed > 0)
    tail = [{"threshold": threshold, "union_records": int((tax_union & (agi >= threshold)).sum()),
             "all_records": int((tax_all & (agi >= threshold)).sum()),
             "max_union_agi": float(agi[tax_union].max()), "max_all_agi": float(agi[tax_all].max())}
            for threshold in [1e6, 1.5e6, 2e6, 5e6]]
    return {"cells": cells, "bins": bins, "states": states,
            "tail": tail,
            "population": float(w[union, 0].sum()), "civilian_population": float(w[civ, 0].sum()),
            "max_agi_real2023": float(agi[civ].max()), "union_records": int(union.sum())}


def row4_weights(d, w):
    source = FISCAL / "main_case_candidate_2026_09_28/derived/production_row4.json"
    ref = json.loads(source.read_text())
    result = w.copy(order="K")
    civ, union = BF.masks(d)
    for label, status in (("naturalized", 4), ("noncitizen", 5)):
        m = d.PENATVTY.eq(303).to_numpy() & d.PRCITSHP.eq(status).to_numpy() & ~d.GESTFIPS.isin([6, 48]).to_numpy()
        r = ref["row4_factors"][label]
        assert m.sum() == r["records"] and abs(w[m, 0].sum() - r["cps_population"]) < .001
        assert not (m & civ & ~union).any()
        # Match the account's column-specific ACS calibration, not one scalar per replicate.
        result[m] *= r["acs_population"] / w[m].sum(axis=0)
    assert abs(result[union, 0].sum() - ref["populations"]["row4"]) < .001
    return result


def write_csv(path, rows):
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def bin_select(k):
    if isinstance(k, int):
        return [k], LABELS[k]
    choices = {"1M+": (list(range(14, 19)), "$1,000,000 or more"),
               "500k-1M": ([13], "$500,000 under $1,000,000"),
               "200k-500k": ([12], "$200,000 under $500,000"),
               "200k+": (list(range(12, 19)), "$200,000 or more")}
    return choices[k]


def output(samples, out):
    rows, cellrows, staterows, bridge, tails = [], [], [], [], []
    for sample, years in samples.items():
        for ti in range(4):
            tails.append(dict(sample=sample, threshold=years[0]["tail"][ti]["threshold"],
                              union_records=sum(y["tail"][ti]["union_records"] for y in years),
                              all_records=sum(y["tail"][ti]["all_records"] for y in years),
                              max_union_agi=max(y["tail"][ti]["max_union_agi"] for y in years),
                              max_all_agi=max(y["tail"][ti]["max_all_agi"] for y in years)))
        for k in [*range(19), "1M+", "500k-1M", "200k-500k", "200k+"]:
            ids, label = bin_select(k)
            num = [y["bins"]["union"][ids].sum(axis=0) for y in years]
            den = [y["bins"]["total"][ids].sum(axis=0) for y in years]
            theta, se, bound = ratio_summary(num, den)
            ur = int(sum(y["bins"]["union_records"][ids].sum() for y in years))
            hr = int(sum(y["bins"]["hispanic_records"][ids].sum() for y in years))
            ar = int(sum(y["bins"]["all_records"][ids].sum() for y in years))
            rows.append(dict(sample=sample, bin19=k, label=label, union_share=float(theta),
                             se_independent_years=float(se), se_max_positive_covariance=float(bound),
                             union_records=ur, all_records=ar, union_tax=sum(x[0] for x in num),
                             total_tax=sum(x[0] for x in den)))
            hn = sum(y["bins"]["hispanic"][ids, 0].sum() for y in years)
            un = sum(x[0] for x in num)
            uc = sum(y["bins"]["union_carriers"][ids, 0].sum() for y in years)
            hc = sum(y["bins"]["hispanic_carriers"][ids, 0].sum() for y in years)
            bridge.append(dict(sample=sample, bin19=k, label=label, union_tax=un, hispanic_tax=hn,
                               ratio=float(divide(un, hn)), union_records=ur, hispanic_records=hr,
                               union_carrier_weight=uc, hispanic_carrier_weight=hc, carrier_ratio=float(divide(uc, hc))))
        for j, group in enumerate(BF.GROUPS):
            for k in range(14):
                n = sum(y["cells"]["union"][j, k, 0] for y in years)
                d = sum(y["cells"]["total"][j, k, 0] for y in years)
                cellrows.append(dict(sample=sample, cbo_group=group, bin14=k, total_fedtax=d, union_fedtax=n,
                                     union_share=float(divide(n, d)), union_records=int(sum(y["cells"]["records"][j, k] for y in years))))
        for state in range(1, 57):
            if not any(y["states"]["total_fedtax"][state].sum() for y in years):
                continue
            for k in range(14):
                values = {key: sum(y["states"][key][state, k] for y in years)
                          for key in ["total_state", "union_state", "total_fedtax", "union_fedtax", "union_records"]}
                staterows.append(dict(sample=sample, state=state, bin14=k, **values,
                                      union_share=float(divide(values["union_state"], values["total_state"]))))
    out.mkdir(parents=True, exist_ok=True)
    write_csv(out / "cps_bins.csv", rows)
    write_csv(out / "cps_cells.csv", cellrows)
    write_csv(out / "cps_state_bins.csv", staterows)
    write_csv(out / "cps_hispanic_bridge.csv", bridge)
    write_csv(out / "cps_tail_support.csv", tails)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--out-dir", type=Path, default=OUT)
    args = parser.parse_args()
    start = time.perf_counter()
    cp = cpi()
    samples, annual, sources = {}, [], []
    for year in SOURCES:
        tick = time.perf_counter()
        d, w, digest = load_year(year)
        factor = cp[2023] / cp[year - 1]
        real = stats(d, w, factor)
        samples[f"year_{year}_real2023"] = [real]
        annual.append(real)
        if year == 2025:
            base = stats(d, w, factor, nominal=True)
            samples["baseline_2025_nominal"] = [base]
            # The canonical case vector must equal this lane's cell-share calculation.
            civ, union = BF.masks(d)
            g = KEYS.cbo_groups(d)
            v, _ = KEYS.raked_vector(d, w[:, 0] * civ, civ, g, "personal", KEYS.cbo_shares(), KEYS._pool14(KEYS.irs_2023()[1]), EDGES)
            held = json.loads((FISCAL / "tax_key_heldout_2026_09_28/derived/translation_inputs.json").read_text())
            want = held["reweighted_share"]["personal"] + held["share_change"]["irs_2023_raked_with_cbo_groups"]["personal"]
            assert abs(w[union, 0] @ v[union] - want) < 1e-12
            rw = row4_weights(d, w)
            samples["baseline_2025_row4_nominal"] = [stats(d, rw, factor, nominal=True)]
            del rw
        sources.append(dict(asec_year=year, income_year=year - 1, path=str(SOURCES[year][0].relative_to(ROOT)),
                            sha256=digest, url=f"https://www2.census.gov/programs-surveys/cps/datasets/{year}/march/asecpub{year % 100}csv.zip",
                            cpi=cp[year - 1], factor_to_2023=factor, published_union_population=real["population"],
                            civilian_population=real["civilian_population"], union_records=real["union_records"], max_agi_real2023=real["max_agi_real2023"]))
        print(f"ASEC {year}: {len(d):,} records, union {real['population']:,.2f}, {time.perf_counter()-tick:.2f}s", flush=True)
        del d, w
        gc.collect()
    samples["pooled_real2023"] = annual
    output(samples, args.out_dir)
    write_csv(args.out_dir / "cps_sources.csv", sources)
    # Stable provenance only; run-dependent timing stays on stdout, outside reproducible artifacts.
    metadata = dict(asec_years=list(SOURCES), cpi_source_path=str(CPI_PATH.relative_to(ROOT)), cpi_source_sha256=sha(CPI_PATH),
                    cpi_source_url="https://api.bls.gov/publicAPI/v2/timeseries/data/", cpi_series="CUUR0000SA0", cpi_period="M13",
                    allocation="personal; FEDTAX_BC on its carrier, state STATETAX_A clipped at zero",
                    union="external_benchmarks_2026_09_24/frame.py::masks, exactly as tax_key_heldout keys.py",
                    weighting="Historical estimates use each year's published weights; supplementary 2025 row4 baseline gates 39,712,493.33118789",
                    pooling="ratio of sums of annual tax dollars in 2023 CPI-U dollars; equal survey-year exposure, population evolves",
                    uncertainty="annual 160 SDR replicates; pooled one-year perturbations, independence SE plus arbitrary-positive-covariance bound",
                    cbo_groups="canonical keys.cbo_groups per year; fixed 2024 Medicare value/payroll cap proxy, ranks recomputed annually",
                    bridge="union/Hispanic personal tax carriers and dollars; union can include non-Hispanic parent-origin members; not a tax-unit count",
                    bin14="0 no AGI through <5k,1 5–10k,...,12 500k–1M,13 1M+")
    (args.out_dir / "cps_metadata.json").write_text(json.dumps(metadata, indent=2) + "\n")
    rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    memory_mb = rss / (1024 * 1024) if sys.platform == "darwin" else rss / 1024
    print(f"Elapsed {time.perf_counter()-start:.2f}s; peak RSS {memory_mb:.1f} MiB", flush=True)
    assert memory_mb < 2500, "[BLOCKED] memory cap exceeded"


if __name__ == "__main__":
    main()
