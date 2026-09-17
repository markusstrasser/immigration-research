#!/usr/bin/env python3
"""Country/parent-birthplace CPS comparisons with annual-block replication."""
import argparse
import hashlib
import json
import zipfile
from pathlib import Path
from statistics import NormalDist

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
YEARS = [2022, 2023, 2024, 2025, 2026]
REPS = [f"pwwgt{i}" for i in range(161)]
COUNTRIES = {
    303: "Mexico", 311: "Costa Rica", 312: "El Salvador", 313: "Guatemala",
    314: "Honduras", 315: "Nicaragua", 316: "Panama", 327: "Cuba",
    329: "Dominican Republic", 332: "Haiti", 360: "Argentina", 361: "Bolivia",
    362: "Brazil", 363: "Chile", 364: "Colombia", 365: "Ecuador",
    369: "Paraguay", 370: "Peru", 372: "Uruguay", 373: "Venezuela",
}
EXTRA = {310: "Belize", 368: "Guyana", 333: "Jamaica", 341: "Trinidad and Tobago"}
METRICS = {"ba": (1, 0), "employment": (2, 0), "earnings_2025usd": (3, 0),
           "poverty": (5, 4), "hs": (6, 0), "full_time_year": (7, 0)}
PRIMARY = ["ba", "employment", "earnings_2025usd", "poverty"]
SCOPES = {"age25_54": [0, 1, 2, 4, 5, 6], "men25_54": [0, 1, 2],
          "women25_54": [4, 5, 6], "age25_64": list(range(8))}
BENCHMARKS = ["white_us_parents", "all_us_parents", "white_cps_native_parents"]


def digest(path):
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def source_paths(repo):
    return {
        2022: HERE / "_cache/2022/asecpub22csv.zip",
        2023: HERE / "_cache/2023/asecpub23csv.zip",
        2024: repo / "sources/immigration-fiscal/data/census/cps_asec_2024_march.zip",
        2025: repo / "infra/immigration-fiscal/gen_ledger_extension_2026_09_16/_cache/asecpub25csv.zip",
        2026: repo / "infra/immigration-fiscal/ledger_asec2026_2026_09_16/_cache/asecpub26csv.zip",
    }


def masks(data):
    us = data.PENATVTY.eq(57)
    parent_us = data.PEFNTVTY.eq(57) & data.PEMNTVTY.eq(57)
    white = data.PEHSPNON.eq(2) & data.PRDTRACE.eq(1)
    native_codes = [57, 60, 66, 69, 73, 78]
    result = {
        "white_us_parents": us & parent_us & white,
        "all_us_parents": us & parent_us,
        "white_cps_native_parents": data.PRCITSHP.isin([1, 2, 3]) & white
        & data.PEFNTVTY.isin(native_codes) & data.PEMNTVTY.isin(native_codes),
    }
    for code, country in (COUNTRIES | EXTRA).items():
        result[f"g1_{country}"] = data.PRCITSHP.isin([4, 5]) & data.PENATVTY.eq(code)
        result[f"g2_{country}"] = us & (data.PEFNTVTY.eq(code) | data.PEMNTVTY.eq(code))
        result[f"g2_two_{country}"] = us & data.PEFNTVTY.eq(code) & data.PEMNTVTY.eq(code)
        result[f"g2_one_us_{country}"] = us & ((data.PEFNTVTY.eq(code) & data.PEMNTVTY.eq(57)) |
                                               (data.PEMNTVTY.eq(code) & data.PEFNTVTY.eq(57)))
    result["g1_LATAM"] = data.PRCITSHP.isin([4, 5]) & data.PENATVTY.isin(COUNTRIES)
    result["g2_LATAM"] = us & (data.PEFNTVTY.isin(COUNTRIES) | data.PEMNTVTY.isin(COUNTRIES))
    return result


def load_year(year, path, cpi):
    cols = ["PH_SEQ", "PPPOS", "PERIDNUM", "A_AGE", "A_SEX", "PRPERTYP", "PRCITSHP",
            "PENATVTY", "PEFNTVTY", "PEMNTVTY", "PEHSPNON", "PRDTRACE", "MARSUPWT",
            "A_HGA", "A_LFSR", "PEARNVAL", "POV_UNIV", "PERLIS", "WKSWORK", "HRSWK"]
    with zipfile.ZipFile(path) as archive:
        data = pd.read_csv(archive.open(f"pppub{year % 100}.csv"), usecols=cols,
                           dtype={"PERIDNUM": str})
        weights = pd.read_csv(archive.open(f"asec_csv_repwgt_{year}.csv"))
    weights = weights.rename(columns={"h_seq": "PH_SEQ"})
    data = data.merge(weights, on=["PH_SEQ", "PPPOS"], how="left", validate="one_to_one")
    assert data[REPS].notna().all().all(), "Unmatched replicate weights"
    assert data.PERIDNUM.is_unique and data.PERIDNUM.str.len().eq(22).all()
    error = float(abs(data.MARSUPWT / 100 - data.pwwgt0).max())
    assert error < .01, "Wrong weight units or join"
    gate = dict(year=year, n=len(data), max_weight_error=error, sha256=digest(path), path=str(path))
    data = data.loc[data.A_AGE.between(25, 64) & data.PRPERTYP.eq(2)].copy()
    assert data.A_HGA.between(31, 46).all()
    assert data.A_LFSR.isin([1, 2, 3, 4, 7]).all()
    assert data.A_SEX.isin([1, 2]).all()
    assert (data.POV_UNIV.eq(1) == data.PERLIS.between(1, 4)).all()
    data["stratum"] = (data.A_SEX - 1) * 4 + (data.A_AGE - 25) // 10
    data["real_earnings"] = data.PEARNVAL * cpi[2025] / cpi[year - 1]
    gate["adult_n"] = len(data)
    return data, gate


def aggregate(data, groups):
    # Feature totals: persons, BA, employment, earnings, poverty denominator,
    # poor, high-school completion, full-time/full-year work.
    features = np.array([np.ones(len(data)), data.A_HGA.ge(43), data.A_LFSR.isin([1, 2]),
                         data.real_earnings, data.POV_UNIV.eq(1), data.PERLIS.eq(1),
                         data.A_HGA.ge(39), data.WKSWORK.ge(50) & data.HRSWK.ge(35)], dtype=float)
    weights = data[REPS].to_numpy(float)
    totals = np.zeros((len(groups), 8, 8, 161))
    counts = np.zeros((len(groups), 8, 8), dtype=float)
    ids, composition = {}, []
    for g, (name, membership) in enumerate(groups.items()):
        for s in range(8):
            selected = np.flatnonzero(membership & data.stratum.eq(s))
            totals[g, :, s, :] = features[:, selected] @ weights[selected]
            counts[g, :, s] = features[:, selected].sum(axis=1)
        ids[name] = {scope: set(data.loc[membership & data.stratum.isin(strata), "PERIDNUM"])
                     for scope, strata in SCOPES.items()}
        if name in {f"g2_{country}" for country in (COUNTRIES | EXTRA).values()}:
            code = next(c for c, n in (COUNTRIES | EXTRA).items() if name == f"g2_{n}")
            sub = data.loc[membership & data.A_AGE.le(54)]
            other = np.where(sub.PEFNTVTY.eq(code), sub.PEMNTVTY, sub.PEFNTVTY)
            foreign_known = np.isin(other, list(range(100, 555)))
            # Status of the other parent; no claim of DNA fraction.
            composition.append(dict(group=name, n=len(sub), other_us=int((other == 57).sum()),
                                    same_country=int((other == code).sum()),
                                    other_foreign=int((foreign_known & (other != code)).sum()),
                                    other_native_area=int(np.isin(other, [60, 66, 69, 73, 78]).sum()),
                                    other_unknown=int((~foreign_known & ~np.isin(other, [57, 60, 66, 69, 73, 78])).sum())))
    return totals, counts, ids, composition


def estimates(totals, strata, standard, target):
    """Accept group x feature x stratum x replicate totals; return G x M x R."""
    selected = totals[:, :, strata, :]
    output = []
    for numerator, denominator in METRICS.values():
        num, den = selected[:, numerator], selected[:, denominator]
        if standard == "crude":
            n, d = num.sum(axis=1), den.sum(axis=1)
            value = np.divide(n, d, out=np.full_like(n, np.nan), where=d > 0)
        else:
            ratios = np.divide(num, den, out=np.full_like(num, np.nan), where=den > 0)
            value = (ratios * target[None, :, None]).sum(axis=1)
        output.append(value)
    return np.stack(output, axis=1)


def linearized_estimates(full, delta, strata, standard, target):
    """First-order changes for independent diagnostic of replicate instability."""
    f, change = full[:, :, strata], delta[:, :, strata, :]
    output = []
    for numerator, denominator in METRICS.values():
        n, d = f[:, numerator], f[:, denominator]
        dn, dd = change[:, numerator], change[:, denominator]
        if standard == "crude":
            n, d, dn, dd = n.sum(1), d.sum(1), dn.sum(1), dd.sum(1)
            with np.errstate(divide="ignore", invalid="ignore"):
                deriv = (dn - (n / d)[:, None] * dd) / d[:, None]
        else:
            with np.errstate(divide="ignore", invalid="ignore"):
                deriv = ((dn - (n / d)[:, :, None] * dd) / d[:, :, None]
                         * target[None, :, None]).sum(1)
        output.append(deriv)
    return np.stack(output, axis=1)


def uncertainty(vectors):
    # First axis annual blocks, last axis full weight then 160 perturbations.
    block_se = np.sqrt(4 / 160 * np.square(vectors[..., 1:] - vectors[..., :1]).sum(axis=-1))
    return block_se.sum(axis=0), np.sqrt(np.square(block_se).sum(axis=0))


def run(repo, output):
    output.mkdir(parents=True, exist_ok=True)
    cpi_path = repo / "infra/immigration-fiscal/crime_cost_2026_09_16/_cache/cpi_2016_2025.json"
    cpi_raw = json.loads(cpi_path.read_text())
    series = cpi_raw["Results"]["series"][0]
    assert series["seriesID"] == "CUUR0000SA0"
    cpi = {int(x["year"]): float(x["value"]) for x in series["data"] if x["period"] == "M13"}
    assert all(year in cpi for year in range(2021, 2026))
    annual, counts, ids, composition, gates = [], [], [], [], []
    target = None
    for year, path in source_paths(repo).items():
        data, gate = load_year(year, path, cpi)
        groups = masks(data)
        names = list(groups)
        sums, nn, ii, comp = aggregate(data, groups)
        annual.append(sums); counts.append(nn); ids.append(ii); gates.append(gate)
        composition.extend([dict(year=year, **row) for row in comp])
        if year == 2025:
            target = sums[names.index("white_us_parents"), 0, :, 0]
            target = target / target.sum()
        print(f"Validated and aggregated {year}: {gate['n']} persons", flush=True)
    annual, counts = np.stack(annual), np.stack(counts).sum(0)
    assert target is not None and np.all(target > 0)
    full = annual[..., 0].sum(axis=0)
    levels, contrasts, diagnostic, suppressed = [], [], [], []
    z_family = NormalDist().inv_cdf(1 - .05 / len(COUNTRIES))
    for scope, strata in SCOPES.items():
        shares = target[strata] / target[strata].sum()
        for standard in ["crude", "age_sex_standardized"]:
            vectors, linear = [], []
            for block in annual:
                delta = block - block[..., :1]
                vectors.append(estimates(full[..., None] + delta, strata, standard, shares))
                linear.append(linearized_estimates(full, delta, strata, standard, shares))
            vectors, linear = np.stack(vectors), np.stack(linear)
            assert np.allclose(vectors[..., 0], vectors[0, ..., 0], equal_nan=True)
            ses, indie = uncertainty(vectors)
            linear_se, _ = uncertainty(linear)
            point = vectors[0, ..., 0]
            for g, group in enumerate(names):
                n = int(counts[g, 0, strata].sum())
                unique = len(set().union(*(ii[group][scope] for ii in ids)))
                min_cell = int(counts[g, 0, strata].min())
                common = dict(scope=scope, standard=standard, group=group, n_person_periods=n,
                              n_distinct_ids=unique, min_stratum_n=min_cell)
                for m, metric in enumerate(METRICS):
                    est, se = point[g, m], ses[g, m]
                    num, den = METRICS[metric]
                    events, valid_n = counts[g, num, strata].sum(), counts[g, den, strata].sum()
                    usable = np.isfinite(vectors[:, g, m]).all()
                    if not usable:
                        suppressed.append(dict(**common, metric=metric, reason="Empty pooled or replicate denominator"))
                        continue
                    levels.append(dict(**common, metric=metric, estimate=est, se_upper=se,
                                       ci95_low=est - 1.96 * se, ci95_high=est + 1.96 * se,
                                       valid_n=int(valid_n), events=events if metric != "earnings_2025usd" else None))
                    diagnostic.append(dict(**common, metric=metric, se_upper=se, se_independence=indie[g, m],
                                           se_linearized_upper=linear_se[g, m]))
                for benchmark in BENCHMARKS:
                    b = names.index(benchmark)
                    for m, metric in enumerate(METRICS):
                        left, right = vectors[:, g, m], vectors[:, b, m]
                        if metric == "earnings_2025usd":
                            if np.any(right <= 0):
                                raise ValueError("Nonpositive reference earnings")
                            vv, center, margin, direction = left / right, 1., .10, 1
                        else:
                            vv, center, margin = left - right, 0., .05
                            direction = -1 if metric == "poverty" else 1
                        if not np.isfinite(vv).all():
                            continue
                        se, _ = uncertainty(vv)
                        est = float(vv[0, 0]); se = float(se)
                        lo, hi = est - 1.96 * se, est + 1.96 * se
                        num, den = METRICS[metric]
                        events, valid_n = counts[g, num, strata].sum(), counts[g, den, strata].sum()
                        sparse = n < 200 or (standard != "crude" and min_cell < 20)
                        zero_events = metric != "earnings_2025usd" and (events == 0 or events == valid_n)
                        verdict = "unresolved"
                        if not sparse and not zero_events:
                            if lo >= center - margin and hi <= center + margin:
                                verdict = "equivalent_within_margin_pointwise95"
                            elif direction * (est - center) - 1.96 * se >= -margin:
                                verdict = "not_materially_worse_pointwise95"
                            elif direction * (est - center) + 1.96 * se < -margin:
                                verdict = "materially_worse_pointwise95"
                        contrasts.append(dict(**common, benchmark=benchmark, metric=metric,
                                              estimate=est, se_upper=se, ci95_low=lo, ci95_high=hi,
                                              point_within_margin=abs(est - center) <= margin,
                                              verdict=verdict, sparse_guard=sparse, zero_event_guard=zero_events,
                                              noninferior_country_corrected=(group in {f'{gen}_{country}' for gen in ['g1', 'g2'] for country in COUNTRIES.values()} and not sparse and not zero_events and
                                              direction * (est - center) - z_family * se >= -margin)))
    levels, contrasts = pd.DataFrame(levels), pd.DataFrame(contrasts)
    levels.to_csv(output / "levels.csv", index=False)
    contrasts.to_csv(output / "contrasts.csv", index=False)
    pd.DataFrame(diagnostic).to_csv(output / "variance_diagnostics.csv", index=False)
    pd.DataFrame(suppressed).to_csv(output / "suppressed.csv", index=False)
    pd.DataFrame(composition).to_csv(output / "parent_composition.csv", index=False)
    summary = []
    for keys, rows in contrasts[contrasts.metric.isin(PRIMARY)].groupby(["scope", "standard", "group", "benchmark"]):
        summary.append(dict(zip(["scope", "standard", "group", "benchmark"], keys)) |
                       dict(metrics_present=len(rows), all_four_noninferior_country_corrected=
                            len(rows) == 4 and bool(rows.noninferior_country_corrected.all())))
    pd.DataFrame(summary).to_csv(output / "joint_verdicts.csv", index=False)
    audit = dict(sources=gates, cpi_source=str(cpi_path), cpi_sha256=digest(cpi_path), cpi=cpi,
                 target_2025_white_age_sex=target.tolist(), countries=COUNTRIES, supplementary=EXTRA,
                 country_family_critical_value=z_family, suppressed_rows=len(suppressed),
                 n_person_periods=sum(g["n"] for g in gates), estimand="Pooled weighted person-period population; fixed age-sex target",
                 variance="Annual-block SDR perturbations; sum block SEs is first-order unknown-covariance bound",
                 benchmark="Own and both parents birthplace57; white-alone/non-Hispanic subset or all",
                 generation="G2 USA-born, any country-born parent; overlapping mixed-origin rows")
    (output / "audit.json").write_text(json.dumps(audit, indent=2) + "\n")
    np.savez_compressed(output / "sufficient_totals.npz", annual=annual, counts=counts, target=target,
                        names=np.array(names), years=np.array(YEARS))
    print(f"PASS: {len(levels)} levels; {len(contrasts)} contrasts; {len(suppressed)} explicitly suppressed", flush=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, default=REPO)
    parser.add_argument("--output-dir", type=Path, default=HERE / "derived")
    args = parser.parse_args()
    run(args.repo, args.output_dir)
