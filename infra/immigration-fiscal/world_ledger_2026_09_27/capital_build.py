"""Build scratch evidence; no lane writes. Python measures time and RSS.

Run from repo root: uv run --no-project python3 <scratch>/capital-build.py
"""
from pathlib import Path
import argparse
import hashlib
import importlib.util
import json
import math
import resource
import sys
import time

sys.dont_write_bytecode = True

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
LANE = HERE
JOB = HERE.parent / "job_capital_taxes_2026_10_14"
INPUTS = HERE / "inputs/capital"
OUT = None
sys.path.insert(0, str(HERE.parent / "scripts"))
from memory_budget import require_within_budget


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def dump(name, value):
    (OUT / name).write_text(json.dumps(value, indent=2, allow_nan=False) + "\n")


def digest(path):
    with path.open("rb") as f:
        return hashlib.file_digest(f, "sha256").hexdigest()


def gate(name, condition):
    if not condition:
        raise SystemExit(f"[BLOCKED] {name}")


def us_reproduction(S):
    wages = pd.read_csv(JOB / "derived/wages_by_industry.csv")
    payload = json.loads((REPO / "infra/immigration-fiscal/main_case_2026_10_14/derived/corrections.json").read_text())
    item = json.loads((JOB / "derived/item.json").read_text())
    meta = payload["meta"]["job_capital_taxes"]
    registry = next(x for x in payload["meta"]["items"] if x["id"] == "job_capital_taxes")
    columns = {"corporate": "corporate_bn", "business_property": "c_and_i_property_bn",
               "other_production_taxes": "other_production_taxes_bn"}
    results = {}
    for alloc in ("personal", "shared"):
        w = wages[wages.allocation.eq(alloc)].set_index("cell")
        taxes = {line: w[column].to_dict() for line, column in columns.items()}
        responses = {line: item["lines"][line]["response"] for line in taxes}
        result = S.source_taxes(w.union_share.to_dict(), taxes, responses,
                                w.index[w.responds.eq(0)].tolist())
        union_gap = max(abs(result["total"][rd] - item["central_bn"][rd][alloc]) for rd in ("low", "high"))
        gate(f"US industry dot product reproduces source item {alloc} <=1e-6bn", union_gap <= 1e-6)
        # The registry adds two lineage parts to the industry's union amount.
        # Read the pre-registry source file's factors and case lineage wage
        # shares, not the expected group_after_bn or effect_at_reference_bn.
        lineage_shares = {part: meta["lineage"]["wage_share"][part][alloc] for part in ("g3plus", "whites")}
        lineage_taxes = {line: {part: item["factor"][factor][line][alloc] * item["lines"][line]["national_bn"]
                               for part, factor in (("g3plus", "G3plus"), ("whites", "white_nh"))}
                         for line in columns}
        lineage = S.source_taxes(lineage_shares, lineage_taxes, responses)
        total = {rd: result["total"][rd] + lineage["total"][rd] for rd in ("low", "high")}
        gap = max(abs(total[rd] - registry["effect_at_reference_bn"][rd][alloc]) for rd in total)
        gate(f"US same core plus declared lineage reproduces meta.items {alloc} <=1e-6bn", gap <= 1e-6)
        results[alloc] = {"union": result["total"], "lineage": lineage["total"], "lineage_total": total,
                          "union_gap_bn": union_gap, "registry_gap_bn": gap}
    dump("capital-us-gate.json", results)


def enigh_tables(M):
    d = M.load_enigh()
    key = ["folioviv", "foliohog", "numren"]
    z = LANE / "_cache/mexico/enigh"
    household = pd.read_csv(z / "concentradohogar.csv", dtype={"folioviv": str, "foliohog": str, "tam_loc": str},
                            usecols=["folioviv", "foliohog", "tam_loc"])
    d = d.merge(household, on=["folioviv", "foliohog"], validate="many_to_one")
    tr = pd.read_csv(z / "trabajos.csv", dtype=str,
                     usecols=key + ["id_trabajo", "subor", "pres_8", "scian", "entidad", "clas_emp", "trapais"])
    inc = pd.read_csv(z / "ingresos.csv", dtype={k: str for k in key + ["clave"]},
                      usecols=key + ["clave", "ing_tri"])
    keep = []
    for job, claves in (("1", M.MAIN_PAY), ("2", M.SECOND_PAY)):
        pay = (inc[inc.clave.isin(claves)].groupby(key).ing_tri.sum() * 4).rename("job_net")
        rows = tr[tr.id_trabajo.eq(job) & tr.subor.eq("1")].join(pay, on=key)
        keep.append(rows)
    jobs = pd.concat(keep, ignore_index=True)
    jobs["job_net"] = jobs.job_net.fillna(0.0)
    pcols = key + ["sex", "age", "cat", "parent_cat", "w", "formal_net_mxn", "formal_gross_mxn", "tam_loc"]
    jobs = jobs.merge(d[pcols], on=key, validate="many_to_one")
    jobs["formal"] = jobs.pres_8.eq("08")
    # Retain the existing person-level gross-up: total formal annual net is
    # grossed up once. Allocate its uplift to jobs by formal net pay shares.
    ratio = np.divide(jobs.job_net, jobs.formal_net_mxn,
                      out=np.zeros(len(jobs)), where=jobs.formal_net_mxn.to_numpy() > 0)
    jobs["job_gross"] = jobs.job_net + np.where(jobs.formal,
        ratio * (jobs.formal_gross_mxn - jobs.formal_net_mxn), 0.0)
    gate("nonnegative gross subordinate pay", jobs.job_gross.ge(0).all())
    gate("formal gross jobs close person formal gross", math.isclose(
        float((jobs.job_gross * jobs.w * jobs.formal).sum()),
        float((d.formal_gross_mxn * d.w).sum()), rel_tol=1e-10))
    country_counts = jobs.trapais.value_counts().to_dict()
    # ENIGH 2024 questionnaire main-job question6 and secondary question1:
    # work performed within country: 1 yes, 2 no. Mexico source taxes and ISN
    # use domestic jobs; retain excluded-job count in metadata.
    jobs = jobs[jobs.trapais.eq("1")].copy()
    sat = pd.read_csv(INPUTS / "capital-sat-sector-isr.csv", dtype={"sector": str, "scian_prefixes": str}).fillna("")
    prefixes = {prefix: r.sector for r in sat.itertuples() for prefix in r.scian_prefixes.split("|") if prefix}
    jobs["sector"] = jobs.scian.str[:2].map(prefixes).fillna("UNMAPPED")
    jobs["band"] = pd.cut(jobs.age, M.AGE_BANDS, right=False).astype(str)
    jobs["weighted_gross"] = jobs.job_gross * jobs.w
    jobs["weighted_formal"] = jobs.weighted_gross * jobs.formal
    national = jobs.groupby("sector").agg(national_wages_mxn=("weighted_gross", "sum"),
        national_formal_wages_mxn=("weighted_formal", "sum"), records=("job_gross", "size"))
    require_within_budget("capital ENIGH comparators before publication")
    national.to_csv(OUT / "capital-enigh-industry.csv", lineterminator="\n", float_format="%.12g")
    # Useful for G1 own-schooling and G2 rearing projection. Divide job wages
    # by every person's cell count, including nonworkers, before applying
    # the group's education-transition probabilities (existing g2_premium).
    d["band"] = pd.cut(d.age, M.AGE_BANDS, right=False).astype(str)
    sector_cells = {}
    for scope in ("national", "urban_100k"):
        ds = d[d.age.ge(15) & (d.tam_loc.eq("1") if scope == "urban_100k" else True)]
        js = jobs[jobs.age.ge(15) & (jobs.tam_loc.eq("1") if scope == "urban_100k" else True)]
        sector_cells[scope] = {}
        for name, category in (("own", "cat"), ("parents", "parent_cat")):
            keys = ["sex", "band", category]
            den = ds.groupby(keys).w.sum()
            whole_cash = ds.assign(weighted_cash=ds.gross_mxn * ds.w).groupby(keys).weighted_cash.sum()
            sums = js.groupby(keys + ["sector"]).weighted_gross.sum()
            gate(f"{scope}/{name}: demographic cell denominators cover every job",
                 set(sums.index.droplevel("sector")) <= set(den.index))
            recovered = math.fsum(float(sums.get((*key, sector), 0.0))
                                 for key in den.index for sector in national.index)
            gate(f"{scope}/{name}: sector wage cells recover total domestic pay",
                 math.isclose(recovered, float(js.weighted_gross.sum()), rel_tol=1e-10))
            table = {}
            for key, people in den.items():
                sex, band, cat = key
                # Match g2_premium.band_of labels exactly, e.g. 15-19/70+.
                left, right = band.strip("[]() ").split(",")
                band_label = f"{int(float(left))}+" if float(right) == 200 else f"{int(float(left))}-{int(float(right))-1}"
                ck = f"{sex}|{band_label}|{int(cat)}"
                table[ck] = {sector: float(sums.get((*key, sector), 0.0) / people) for sector in national.index}
                table[ck]["__TOTAL_CASH__"] = float(whole_cash[key] / people)
            sector_cells[scope][name] = table
    dump("capital-enigh-cells.json", sector_cells)
    for name, category in (("own", "cat"), ("parents", "parent_cat")):
        keys = ["sex", "band", category]
        denominators = d[d.age.ge(15)].groupby(keys).w.sum().rename("persons")
        cells = jobs[jobs.age.ge(15)].groupby(keys + ["sector"]).weighted_gross.sum().to_frame()
        cells = cells.join(denominators, on=keys)
        gate(f"{name}: no missing denominator in projected wage cells", cells.persons.notna().all())
        cells["wage_per_person_mxn"] = cells.weighted_gross / cells.persons
        cells.to_csv(OUT / f"capital-enigh-{name}-cells.csv", lineterminator="\n", float_format="%.12g")
    formal = jobs[jobs.formal & jobs.age.ge(15)].groupby("entidad").weighted_formal.sum().rename("formal_pay_mxn")
    rates = pd.read_csv(INPUTS / "capital-isn-rates.csv", dtype={"state": str}).set_index("state")
    states = rates.join(formal.rename_axis("state"), how="left")
    gate("all32 states formal pay observed", states.formal_pay_mxn.notna().all() and len(states) == 32)
    # Tabasco art30 (Congress primary law archived Jan2024) has public3%,
    # others2.5%; updated2025 compiler footnote has a different ordering.
    tb = jobs[jobs.formal & jobs.age.ge(15) & jobs.entidad.eq("27")]
    tb_rate = float((tb.weighted_formal * np.where(tb.clas_emp.eq("3"), .03, .025)).sum() / tb.weighted_formal.sum())
    states.loc["27", ["rate_low", "rate_high"]] = tb_rate
    states.loc["27", "qualification"] = "Tabasco art30 primary2023 law archivedJan2024 public3/private2.5; ENIGH clas_emp3 government"
    states["national_formal_pay_weight"] = states.formal_pay_mxn / states.formal_pay_mxn.sum()
    states["weighted_rate_low"] = states.national_formal_pay_weight * states.rate_low
    states["weighted_rate_high"] = states.national_formal_pay_weight * states.rate_high
    states.to_csv(OUT / "capital-isn-state-weights.csv", lineterminator="\n", float_format="%.12g")
    dump("capital-enigh-meta.json", {
        "gross_subordinate_pay_mxn_bn": float(jobs.weighted_gross.sum() / 1e9),
        "formal_pay_mxn_bn": float(states.formal_pay_mxn.sum() / 1e9),
        "unmapped_wage_share": float(national.loc["UNMAPPED", "national_wages_mxn"] / jobs.weighted_gross.sum()) if "UNMAPPED" in national.index else 0,
        "job_country_counts_before_domestic_filter": country_counts,
        "state_mix": "national formal subordinate gross pay; not migrant-origin state mix",
        "isn_base_rate_lower": float(states.weighted_rate_low.sum()),
        "isn_base_rate_upper": float(states.weighted_rate_high.sum()),
        "isn_scope": "base statutory rates only; exemptions/surcharges not silently modeled",
        "wage_scope": "domestic subordinate wages main plus secondary; existing formal person gross-up; trapais1 per ENIGH2024 questionnaire",
        "gaps": ["OTHER/OTHER_AUX corporate tax sector has no identified industry; requires an explicit pooled-key allocation", "Taxable corporate base by industry is not identical to ENIGH wage universe", "Independent business income excluded to match US wage-only key", "No employer aggregate payroll to apply Sinaloa tariff exactly", "Tabasco institution-of-government code observed; productive state companies under private-company code need separate treatment"]})


def main():
    global OUT
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out-dir", type=Path, required=True)
    args = parser.parse_args()
    OUT = args.out_dir.resolve()
    if OUT == HERE or OUT.is_relative_to(HERE / "derived") or OUT.is_relative_to(INPUTS):
        raise SystemExit("[BLOCKED] generator requires separate output directory; historical outputs/input pins frozen")
    OUT.mkdir(parents=True, exist_ok=True)
    start = time.perf_counter()
    pins = json.loads((INPUTS / "capital_pins.json").read_text())
    for name in ("capital-sat-sector-isr.csv", "capital-isn-rates.csv", "capital-sat-itg2024-new.pdf", "capital-indetec2025.pdf", "capital-tabasco-law2023.pdf"):
        gate(f"pinned capital source {name}", digest(INPUTS / name) == pins[name]["sha256"])
    S = load("capital_source_scratch", HERE / "capital_source.py")
    M = load("mexico", LANE / "mexico.py")
    us_reproduction(S)
    enigh_tables(M)
    sources = {
        "capital-sat-itg2024-new.pdf": "https://www.sat.gob.mx/minisitio/Transparencia/documentos/itg/ITG_2024_4T.pdf",
        "capital-sat-program.pdf": "https://www.sat.gob.mx/minisitio/AdministracionSAT/documentos/InstrumentoDisenoProgramaPresupuestarioE013ServiciosRecaudacionContribucionesFederales.pdf",
        "capital-indetec2025.pdf": "https://www.indetec.gob.mx/delivery?path=%2Fbiblioteca%2FEspeciales%2FPanorama-de-Ingresos-Propios%2FPanorama-de-Ingresos-Propios.pdf&sl=3&srv=0",
        "capital-tabasco-law2023.pdf": "https://congresotabasco.gob.mx/wp/wp-content/uploads/2024/01/Ley-de-Hacienda-del-Estado-de-Tabasco-Enero-2023.pdf"}
    pins = {name: {"url": url, "retrieved": "2026-10-15", "sha256": digest(INPUTS / name)} for name, url in sources.items()}
    for path in [LANE / "mexico.py", JOB / "derived/wages_by_industry.csv", JOB / "derived/item.json",
                 REPO / "infra/immigration-fiscal/main_case_2026_10_14/derived/corrections.json",
                 LANE / "_cache/reads/enigh2024_cuest_personas_mayores.pdf",
                 *[LANE / "_cache/mexico/enigh" / f"{t}.csv" for t in ("poblacion", "trabajos", "ingresos", "concentradohogar")]]:
        pins[str(path.relative_to(REPO))] = {"sha256": digest(path), "kind": "existing source; read only"}
    dump("capital-pins.json", pins)
    footprint = require_within_budget("capital generator")
    dump("capital-timing.json", {"elapsed_seconds": time.perf_counter() - start,
        "max_rss_bytes_macos": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
        "peak_physical_footprint_bytes": footprint})
    print("PASS: US source core and lineage registry reproduce; ENIGH sector/state evidence built")


if __name__ == "__main__":
    main()
