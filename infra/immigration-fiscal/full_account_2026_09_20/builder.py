"""Join reconciled accounts; never infer fiscal response from incidence labels."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import numpy as np
import pandas as pd

from model import normalized_gap, reconcile

HERE = Path(__file__).resolve().parent
AMOUNTS = ["national_bn", "target_bn", "other_bn", "external_bn", "unallocated_bn"]
KEYS = ["scenario_id", "allocation", "category"]
# Same pinned CY2024 Census resident total used by the source account modules.
RESIDENT_POPULATION = 340_110_988.0


def sha(path):
    with Path(path).open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def verify_export(path):
    """Require the producer's receipt, then verify all declared dependencies."""
    audit_path = path.parent/"audit.json"
    audit = json.loads(audit_path.read_text())
    expected = audit["outputs"].get(path.stem, audit["outputs"].get(path.name))
    if expected != sha(path):
        raise ValueError(f"Missing or stale producer output hash: {path}")
    for source, fingerprint in audit["source_hashes"].items():
        if sha(source) != fingerprint:
            raise ValueError(f"Upstream dependency changed: {source}")
    return audit_path


def read_allocations(path, expected_total):
    data = pd.read_csv(path)
    required = KEYS + AMOUNTS + ["allocation_key", "response_class"]
    if set(required) - set(data):
        raise ValueError(f"Incomplete allocation schema: {path}")
    if data[KEYS].isna().any().any() or data.duplicated(KEYS).any():
        raise ValueError("Missing or duplicate accounting category")
    if not np.isfinite(data[AMOUNTS].to_numpy()).all():
        raise ValueError("Nonfinite accounting amount")
    if not set(data.allocation).issubset({"shared", "personal"}):
        raise ValueError("Unknown person/resource-sharing convention")
    for row in data.itertuples():
        reconcile(*(getattr(row, key) for key in AMOUNTS))
    totals = data.groupby(KEYS[:2])[AMOUNTS].sum()
    if not np.allclose(totals.national_bn, expected_total, rtol=0, atol=.000001):
        raise ValueError("An arm does not exhaust the pinned national current account")
    # A net-zero collection of unallocated signed flows is not complete either.
    totals["unallocated_absolute_bn"] = data.assign(
        absolute=data.unallocated_bn.abs()).groupby(KEYS[:2]).absolute.sum()
    return data, totals.reset_index()


def combine_accounts(receipts, spending, population):
    rows = []
    for r in receipts.itertuples():
        for s in spending[spending.allocation.eq(r.allocation)].itertuples():
            target = r.target_bn-s.target_bn
            other = r.other_bn-s.other_bn
            rows.append(dict(
                receipt_scenario=r.scenario_id, spending_scenario=s.scenario_id,
                allocation=r.allocation,
                receipt_target_bn=r.target_bn, spending_target_bn=s.target_bn,
                target_balance_bn=target, other_balance_bn=other,
                national_balance_bn=r.national_bn-s.national_bn,
                external_balance_bn=r.external_bn-s.external_bn,
                unallocated_balance_bn=r.unallocated_bn-s.unallocated_bn,
                unallocated_absolute_bn=r.unallocated_absolute_bn+s.unallocated_absolute_bn,
                complete=bool(r.unallocated_absolute_bn+s.unallocated_absolute_bn < 1e-8),
                target_population=population, resident_population=RESIDENT_POPULATION,
                target_balance_per_person=target*1e9/population,
                normalized_gap_bn=normalized_gap(target, other, population, RESIDENT_POPULATION),
            ))
    return pd.DataFrame(rows)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-root", type=Path, default=HERE.parents[2])
    parser.add_argument("--receipts", type=Path)
    parser.add_argument("--spending", type=Path)
    parser.add_argument("--out", type=Path, default=HERE/"derived")
    args = parser.parse_args()
    fiscal = args.source_root.resolve()/"infra/immigration-fiscal"
    receipt_path = args.receipts or fiscal/"full_account_receipts_2026_09_20/derived/category_allocations.csv"
    spending_path = args.spending or fiscal/"full_account_spending_2026_09_20/derived/allocations.csv"
    population_path = fiscal/"macro_closure_2026_09_19/derived/finance_vintage_totals.csv"
    pop = pd.read_csv(population_path).query("group == 'mexican_observed_total'").population
    if len(pop) != 2 or not np.allclose(pop, pop.iloc[0], rtol=0, atol=1e-5):
        raise ValueError("Target population differs across allocation conventions")
    population = float(pop.iloc[0])
    receipt_audit = verify_export(receipt_path)
    spending_audit = verify_export(spending_path)
    population_audit = verify_export(population_path)
    _, receipts = read_allocations(receipt_path, 8008.290)
    _, spending = read_allocations(spending_path, 10061.458)
    accounts = combine_accounts(receipts, spending, population)
    args.out.mkdir(parents=True, exist_ok=True)
    account_path = args.out/"accounts.csv"
    accounts.to_csv(account_path, index=False)
    inputs = [receipt_path, spending_path, population_path, receipt_audit,
              spending_audit, population_audit, Path(__file__),
              HERE/"model.py", HERE/"DESIGN.md"]
    audit = dict(
        units="billions of2024 dollars per year", account="NIPA current receipts/expenditure",
        target="Observed CPS Mexican-origin union, all ages and education",
        resident_population=RESIDENT_POPULATION, target_population=population,
        normalized_comparison="Target versus same resident-assigned account per resident; not causal welfare",
        source_hashes={str(p.resolve()): sha(p) for p in inputs},
        outputs={"accounts": sha(account_path)},
        scenario_status="Cross of named one-at-a-time receipt arms and declared spending arms; not a confidence region",
    )
    (args.out/"audit.json").write_text(json.dumps(audit, indent=2)+"\n")
    print(accounts.loc[accounts.receipt_scenario.eq("cbo_collective"),
        ["allocation", "spending_scenario", "target_balance_bn", "normalized_gap_bn", "complete"]].to_string(index=False))


if __name__ == "__main__":
    main()
