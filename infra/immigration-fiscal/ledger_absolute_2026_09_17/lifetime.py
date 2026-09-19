#!/usr/bin/env python3
"""Survival-weighted period-profile NPVs from the annual component ledger.

Native-First: pandas consumes the existing annual export and cached NVSS tables;
no new microdata estimator, pension model, or cohort forecast is introduced.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[3]
LANE = Path("infra/immigration-fiscal/ledger_absolute_2026_09_17")
LIFE_LANE = Path("infra/immigration-fiscal/lifetime_longevity_sstiming_2026_09_18")
KEYS = ["allocation", "account", "group", "band"]
GROUPS = ["mexico_born", "mexican_second_gen", "mexican_third_plus_selfid",
          "mexican_observed_total", "third_plus_nh_white", "all_native"]
BANDS = ((0, 18), (18, 25), (25, 35), (35, 45), (45, 55), (55, 65), (65, 75), (75, 101))
TABLES = {"total": "01", "hispanic": "04", "nh_white": "16"}
SCHEMA = "fiscal-period-profile-v2"


def sha256(path: Path) -> str:
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def verify_inputs(records: list[dict], root: Path) -> None:
    if not records:
        raise ValueError("[BLOCKED] source audit has no input fingerprints")
    for item in records:
        path = Path(item["path"])
        if not path.is_absolute():
            path = root / path
        if not path.is_file() or sha256(path) != item["sha256"]:
            raise ValueError(f"[BLOCKED] missing or stale source: {path}")


def validate_profiles(profiles: pd.DataFrame, components: pd.DataFrame) -> None:
    required = set(KEYS + ["population", "net_total", "net_per_person"])
    if not required.issubset(profiles):
        raise ValueError(f"[BLOCKED] age profile columns missing: {required - set(profiles)}")
    if not set(KEYS + ["component", "signed_total"]).issubset(components):
        raise ValueError("[BLOCKED] age component schema is incomplete")
    if profiles.empty or profiles.duplicated(KEYS).any():
        raise ValueError("[BLOCKED] empty or duplicate age profiles")
    if components.duplicated(KEYS + ["component"]).any():
        raise ValueError("[BLOCKED] duplicate age components")
    if not np.isfinite(profiles[["population", "net_total", "net_per_person", "band"]]).all().all():
        raise ValueError("[BLOCKED] nonfinite age profile values")
    if not np.isfinite(components.signed_total).all() or (profiles.population <= 0).any():
        raise ValueError("[BLOCKED] nonfinite components or nonpositive denominator")
    if set(profiles.allocation) != {"personal", "shared"} or set(profiles.account) != {"partial", "expanded"}:
        raise ValueError("[BLOCKED] both allocations and account coverages are required")
    expected = {(a, c, g) for a in ("personal", "shared") for c in ("partial", "expanded") for g in GROUPS}
    observed = set()
    for key, block in profiles.groupby(KEYS[:-1]):
        observed.add(key)
        if sorted(block.band.tolist()) != list(range(8)):
            raise ValueError(f"[BLOCKED] missing/noninteger age band in {key}")
    if not expected.issubset(observed):
        raise ValueError(f"[BLOCKED] missing group profiles: {expected - observed}")
    if not np.allclose(profiles.net_total / profiles.population, profiles.net_per_person, rtol=1e-10, atol=1e-6):
        raise ValueError("[BLOCKED] age profile denominator does not reconstruct dollars")
    sums = components.groupby(KEYS).signed_total.sum().rename("component_sum")
    joined = profiles.set_index(KEYS).join(sums, how="outer")
    if joined[["net_total", "component_sum"]].isna().any().any() or not np.allclose(
            joined.net_total, joined.component_sum, rtol=1e-10, atol=1e-3):
        raise ValueError("[BLOCKED] age components do not reconstruct profiles")
    for (allocation, account), block in profiles.groupby(["allocation", "account"]):
        targets = block[block.group.isin(GROUPS[:3])].groupby("band")[["population", "net_total"]].sum()
        union = block[block.group.eq("mexican_observed_total")].set_index("band").sort_index()
        if not np.allclose(targets, union[["population", "net_total"]], rtol=1e-10, atol=1e-3):
            raise ValueError(f"[BLOCKED] union profile does not pool its components: {allocation}/{account}")


def load_age_profiles(root: Path = ROOT) -> tuple[pd.DataFrame, dict]:
    root = Path(root).resolve()
    source = root / LANE / "derived"
    audit_path = source / "audit.json"
    audit = json.loads(audit_path.read_text())
    manifest = audit.get("age_profile_export", {}).get("files", {})
    names = ("age_profiles.csv", "age_profile_components.csv")
    if not all(name in manifest for name in names):
        raise ValueError("[BLOCKED] annual export predates the age-profile repair; rebuild absolute_ledger.py")
    for name in names:
        path = source / name
        if not path.is_file() or sha256(path) != manifest[name]:
            raise ValueError(f"[BLOCKED] missing/stale annual profile export: {path}")
    verify_inputs(audit.get("inputs", []), root)
    if audit.get("params_allow_placeholder"):
        raise ValueError("[BLOCKED] lifetime estimates require verified annual parameters")
    profiles, components = (pd.read_csv(source / name) for name in names)
    validate_profiles(profiles, components)
    fingerprints = {str((source / name).resolve()): sha256(source / name) for name in (*names, "audit.json")}
    return profiles, fingerprints


def read_life_table(root: Path, key: str, year: int = 2024) -> pd.DataFrame:
    """NVSS Lx is one-year exposure, except the final 100-and-over interval."""
    path = Path(root) / LIFE_LANE / "_cache" / f"lt{year}_Table{TABLES[key]}.xlsx"
    raw = pd.read_excel(path, header=None)
    rows = []
    for _, row in raw.iterrows():
        label = str(row[0]).strip().replace("–", "-").replace("—", "-")
        if label.startswith("100 and"):
            age = 100
        elif "-" in label and label[0].isdigit():
            age = int(label.split("-")[0])
        else:
            continue
        rows.append(dict(age=age, qx=float(row[1]), lx=float(row[2]), Lx=float(row[4])))
    table = pd.DataFrame(rows).sort_values("age").reset_index(drop=True)
    if table.age.tolist() != list(range(101)) or not np.isfinite(table.to_numpy()).all():
        raise ValueError(f"[BLOCKED] invalid life table: {path}")
    if abs(table.lx.iloc[0] - 100000) > 1e-6 or (table.lx.diff().dropna() > 0).any():
        raise ValueError(f"[BLOCKED] invalid survival radix/order: {path}")
    if (table.lx <= 0).any() or (table.Lx < 0).any() or not table.qx.between(0, 1).all():
        raise ValueError(f"[BLOCKED] invalid mortality/exposure values: {path}")
    return table


def age_vector(profiles: pd.DataFrame, group: str, account: str = "expanded",
               allocation: str = "personal") -> np.ndarray:
    block = profiles[(profiles.group == group) & (profiles.account == account)
                     & (profiles.allocation == allocation)].sort_values("band")
    if block.band.tolist() != list(range(8)):
        raise ValueError(f"[BLOCKED] incomplete {allocation}/{account}/{group} age profile")
    result = np.empty(101)
    for (_, row), (lo, hi) in zip(block.iterrows(), BANDS):
        result[lo:hi] = row.net_per_person
    return result


def survival_npv(profile: np.ndarray, table: pd.DataFrame, start_age: int,
                 real_rate: float, last_age: int = 100) -> tuple[float, float]:
    rate = float(real_rate)
    if not 0 <= start_age <= last_age <= 100 or not np.isfinite(rate) or rate <= -1:
        raise ValueError("invalid start/horizon/discount rate")
    if len(profile) != 101 or not np.isfinite(profile).all():
        raise ValueError("expected 101 finite single-age balances")
    ages = np.arange(start_age, last_age + 1)
    exposure = table.Lx.to_numpy()[start_age:last_age + 1] / table.lx.iloc[start_age]
    weights = exposure * (1.0 + rate) ** -(ages - start_age)
    return float(profile[start_age:last_age + 1] @ weights), float(weights.sum())


def mortality_key(group: str, arm: str) -> str:
    if arm == "common_total":
        return "total"
    if arm != "group_specific":
        raise ValueError(f"unknown mortality arm: {arm}")
    if group == "third_plus_nh_white":
        return "nh_white"
    return "hispanic" if group in GROUPS[:4] else "total"


def calculate(profiles: pd.DataFrame, tables: dict[str, pd.DataFrame]) -> pd.DataFrame:
    rows = []
    for allocation in ("personal", "shared"):
        for account in ("partial", "expanded"):
            for group in GROUPS:
                vector = age_vector(profiles, group, account, allocation)
                for survival in ("common_total", "group_specific"):
                    table_key = mortality_key(group, survival)
                    for horizon, last in (("full_100plus", 100), ("truncate83", 82)):
                        for start in (0, 25):
                            for rate in (0.0, 0.02, 0.03, 0.05):
                                value, years = survival_npv(vector, tables[table_key], start, rate, last)
                                rows.append(dict(allocation=allocation, account=account, group=group,
                                                 survival=survival, mortality_table=table_key,
                                                 horizon=horizon, start_age=start, real_discount_rate=rate,
                                                 period_profile_npv=value, discounted_person_years=years,
                                                 price_year=2024, mortality_year=2024,
                                                 primary=(allocation == "personal" and account == "expanded"
                                                          and survival == "common_total" and last == 100)))
    result = pd.DataFrame(rows)
    join_keys = ["allocation", "account", "survival", "horizon", "start_age", "real_discount_rate"]
    reference = result[result.group == "third_plus_nh_white"][join_keys + ["period_profile_npv"]]
    reference = reference.rename(columns={"period_profile_npv": "white_reference_npv"})
    result = result.merge(reference, on=join_keys, validate="many_to_one")
    result["npv_difference_vs_white_same_start"] = result.period_profile_npv - result.white_reference_npv
    return result


def generate(root: Path, out_dir: Path, life_table_root: Path | None = None) -> pd.DataFrame:
    profiles, sources = load_age_profiles(root)
    table_root = Path(life_table_root or root)
    tables = {key: read_life_table(table_root, key) for key in TABLES}
    for key, number in TABLES.items():
        path = table_root / LIFE_LANE / "_cache" / f"lt2024_Table{number}.xlsx"
        sources[str(path.resolve())] = sha256(path)
    sources[str(Path(__file__).resolve())] = sha256(Path(__file__))
    result = calculate(profiles, tables)
    annual_audit = json.loads((Path(root) / LANE / "derived/audit.json").read_text())
    f_extra = (annual_audit["item_metadata"]["F|per_capita"]["national_dollars"]
               / annual_audit["us_resident_population"])
    if not np.isfinite(f_extra) or f_extra < 0:
        raise ValueError("[BLOCKED] invalid public-goods allocation sensitivity")
    result["F_extra_annual_per_resident"] = f_extra
    result["npv_with_F_per_capita"] = result.period_profile_npv - f_extra * result.discounted_person_years
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    target = out_dir / "period_profiles.csv"
    result.to_csv(target, index=False)
    audit = dict(schema=SCHEMA, inputs=[dict(path=p, sha256=h) for p, h in sources.items()],
                 output_sha256=sha256(target), rows=len(result), price_year=2024,
                 interpretation="survival-weighted period-profile scenario; not a cohort, admission, or birth-policy forecast",
                 real_growth=0, outmigration="not modeled", descendants="not modeled",
                 fiscal_top_age="75+ band held constant; NVSS 100+ exposure discounted at age 100",
                 valuation="time 0 at each stated starting age; annual interval start discounting",
                 mortality="US-total common schedule primary; pooled Hispanic and NH-white proxies sensitivity",
                 pension_account="cash; SSA MWR accrual adjustments excluded",
                 public_goods_sensitivity="npv_with_F_per_capita adds average defense/general-government/interest net of already priced TRICARE; other omitted programs remain omitted",
                 limitations="component allocation and population denominators inherited from annual export")
    (out_dir / "period_profile_audit.json").write_text(json.dumps(audit, indent=2) + "\n")
    return result


def load_period_profiles(out_dir: Path, root: Path = ROOT) -> pd.DataFrame:
    """Every current consumer must verify the output and its source fingerprints."""
    audit = json.loads((Path(out_dir) / "period_profile_audit.json").read_text())
    if audit.get("schema") != SCHEMA:
        raise ValueError("[BLOCKED] superseded lifetime schema")
    verify_inputs(audit.get("inputs", []), Path(root))
    load_age_profiles(root)
    path = Path(out_dir) / "period_profiles.csv"
    if sha256(path) != audit["output_sha256"]:
        raise ValueError("[BLOCKED] altered/stale lifetime output")
    return pd.read_csv(path)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--life-table-root", type=Path)
    parser.add_argument("--out-dir", type=Path)
    args = parser.parse_args()
    out = args.out_dir or args.root / LANE / "derived/lifetime"
    results = generate(args.root, out, args.life_table_root)
    print(f"[written] {len(results)} period-profile scenarios: {out}")


if __name__ == "__main__":
    main()
