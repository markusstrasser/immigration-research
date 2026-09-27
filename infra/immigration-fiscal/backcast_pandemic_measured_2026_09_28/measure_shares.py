#!/usr/bin/env python3
"""The group's measured share of each CPS-keyed benefit, income years 2019-2024 (CPS ASEC 2020-2025).

Native-First: the account's union and sharing rule (full_account_spending_2026_09_20/builder.py,
`canonical_target` and `equal_unit_share`), the Borjas residual (status_impute_2026_09_16/impute_status.py,
`impute`) and the Census tax model's own payments (`EIP_CRD`), recomputed per tax unit under each payment's
identification-number rule. Weights are pwwgt0 and its 160 successive-difference replicates.

Measured: every key's national and group dollars in each income year. Assumed: the Borjas residual stands for
"no valid SSN"; the CPS has no SSN field (Census SEHSD-WP2021-18, PDF p. 11).

Gates: the ASEC 2025 run reproduces the account's incidence keys (full_account_spending_2026_09_20/derived/
incidence_keys.csv) to 1e-12; the Census model's EIP_CRD is rebuilt exactly from each tax unit's filers,
children and AGI before any SSN rule is applied; and the validation lane's shared SNAP, Social Security and
SSI for the union (validation_fiscal_years_2026_09_28/derived/annual_components.csv, unit-head weights) are
reproduced for 2021-2024 with that lane's own weighting.

Run from the repository root:
  OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/backcast_pandemic_measured_2026_09_28/measure_shares.py
"""
from __future__ import annotations

import argparse
import contextlib
import hashlib
import importlib.util
import io
import sys
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
FISCAL = ROOT / "infra/immigration-fiscal"
sys.path.insert(0, str(FISCAL / "full_account_spending_2026_09_20"))
sys.path.insert(0, str(FISCAL / "status_impute_2026_09_16"))
from builder import CPS_SHA, canonical_target, equal_unit_share  # noqa: E402
from impute_status import impute  # noqa: E402

_spec = importlib.util.spec_from_file_location(
    "validation_fiscal_years", FISCAL / "validation_fiscal_years_2026_09_28/analysis.py")
VALIDATION_LANE = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(VALIDATION_LANE)

SOURCES = {  # survey year -> (zip, sha256); income year is one less
    2020: (HERE / "_cache/asecpub20csv.zip", "f79430c5664745a2ae1c0f7fef615d93fa6b1933d0fe1dabb932ec52c73be591"),
    2021: (HERE / "_cache/asecpub21csv.zip", "7196ff49c52f833f65c537d66a0c8cc1540a8e31711a09c3730c218b4486c1f4"),
    2022: (FISCAL / "latam_comparison_2026_09_17/_cache/2022/asecpub22csv.zip",
           "7338011adefca16dae30a4469ddaf0c01cef579b607b26b4bceec749376e4ac9"),
    2023: (FISCAL / "latam_comparison_2026_09_17/_cache/2023/asecpub23csv.zip",
           "d2e000250782adfbdd7f29c82b66d866591a30f0d330496698ec19f9c784ce11"),
    2024: (FISCAL / "same_year_tax_2026_09_20/_cache/asecpub24csv.zip",
           "cdb39cdac34bef99dd0940ab28e306f692404c2eea44d85dfd634214872a0a09"),
    2025: (FISCAL / "gen_ledger_extension_2026_09_16/_cache/asecpub25csv.zip", CPS_SHA),
}
ACCOUNT_KEYS = FISCAL / "full_account_spending_2026_09_20/derived/incidence_keys.csv"
VALIDATION = FISCAL / "validation_fiscal_years_2026_09_28/derived/annual_components.csv"
REPS = [f"pwwgt{i}" for i in range(161)]
PERSON = ["PH_SEQ", "PPPOS", "A_LINENO", "A_SPOUSE", "A_AGE", "PRPERTYP", "PRCITSHP", "PENATVTY", "PEFNTVTY",
          "PEMNTVTY", "PRDTHSP", "PEINUSYR", "SPM_ID", "SPM_HEAD", "SS_VAL", "SSI_VAL", "PAW_VAL", "UC_VAL", "VET_VAL",
          "WC_VAL", "EIT_CRED", "ACTC_CRD", "SPM_SNAPSUB", "SPM_ENGVAL", "SPM_WICVAL", "MCAID", "MCARE", "MIL",
          "CHAMPVA", "VET_YN", "PEAFEVER", "A_CLSWKR", "PEIOOCC", "TAX_ID", "DEP_STAT", "FILESTAT", "AGI",
          "MARSUPWT"]
EXTRA = {2021: ["EIP_CRD"], 2022: ["EIP_CRD", "CDC_CRD"]}
DOLLARS = {"social_security": "SS_VAL", "ssi": "SSI_VAL", "cash_assistance": "PAW_VAL",
           "unemployment": "UC_VAL", "veterans": "VET_VAL", "workers_comp": "WC_VAL"}
UNITS = {"snap": "SPM_SNAPSUB", "energy": "SPM_ENGVAL", "wic": "SPM_WICVAL"}
STATUS = ("modeled", "borjas", "borjas_own")
JOINT = (1, 2, 3)          # FILESTAT: joint returns
HEAD_OF_HOUSEHOLD = 4
US_BIRTH = [57, 60, 66, 69, 73, 78]


def sha(path: Path) -> str:
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def sdr(values: np.ndarray) -> float:
    """Successive-difference replicate standard error; values[0] is the full-sample estimate."""
    return float(np.sqrt(4 / 160 * np.square(values[1:] - values[0]).sum()))


def load(year: int) -> tuple[pd.DataFrame, pd.DataFrame]:
    path, pin = SOURCES[year]
    if sha(path) != pin:
        raise SystemExit(f"[BLOCKED] {path.name} does not match its pin")
    with zipfile.ZipFile(path) as z:
        d = pd.read_csv(z.open(f"pppub{year % 100}.csv"), usecols=PERSON + EXTRA.get(year, []))
        hh = pd.read_csv(z.open(f"hhpub{year % 100}.csv"), usecols=["H_SEQ", "HPUBLIC", "HLORENT"])
        w = pd.read_csv(z.open(f"asec_csv_repwgt_{year}.csv"), usecols=["h_seq", "PPPOS", *REPS])
    d = d.merge(w.rename(columns={"h_seq": "PH_SEQ"}), on=["PH_SEQ", "PPPOS"], validate="one_to_one", how="left")
    if d.isna().any().any():
        raise SystemExit(f"[BLOCKED] ASEC {year}: missing fields or replicate weights")
    np.testing.assert_allclose(d.MARSUPWT / 100, d.pwwgt0, rtol=0, atol=.01)
    return d, hh


def unit_field(d: pd.DataFrame, field: str) -> np.ndarray:
    """An SPM-unit total split equally over the unit's members (builder.py `unit_field`)."""
    if not d.groupby("SPM_ID")[field].nunique().eq(1).all():
        raise SystemExit(f"[BLOCKED] {field} is not constant within SPM units")
    return d[field].to_numpy(float) / d.groupby("SPM_ID").SPM_ID.transform("size").to_numpy()


def no_ssn_masks(d: pd.DataFrame, hh: pd.DataFrame) -> dict[str, np.ndarray]:
    """Who is treated as lacking an SSN: nobody (the Census model), the Borjas residual, and the residual
    built from each person's own rules without clause (i), which keeps a foreign-born spouse of a citizen
    in the no-SSN column (the mixed-status joint returns the first round excluded)."""
    with contextlib.redirect_stderr(io.StringIO()) as note:      # impute() prints its Medicaid caveat
        status = impute(d, hh)
    if "[DEGRADED]" not in note.getvalue():
        raise SystemExit("[BLOCKED] impute_status no longer reports its Medicaid caveat; recheck the rule set")
    return {"modeled": np.zeros(len(d), bool), "borjas": status["unauthorized"],
            "borjas_own": status["foreign_born"] & ~status["own_legal"]}


def reduction(filestat: np.ndarray, agi: np.ndarray) -> np.ndarray:
    """5% of AGI above $150,000 (joint), $112,500 (head of household) or $75,000; IRC 6428(c), 6428A(c)."""
    threshold = np.select([np.isin(filestat, JOINT), filestat == HEAD_OF_HOUSEHOLD], [150_000, 112_500], 75_000)
    return 0.05 * np.maximum(agi - threshold, 0)


def phase_eip3(filestat: np.ndarray, agi: np.ndarray) -> np.ndarray:
    """IRC 6428B(d): the credit falls to zero over $10,000 above $150,000 (joint), $7,500 above $112,500
    (head of household) and $5,000 above $75,000 (others)."""
    joint, head = np.isin(filestat, JOINT), filestat == HEAD_OF_HOUSEHOLD
    start = np.select([joint, head], [150_000, 112_500], 75_000)
    width = np.select([joint, head], [10_000, 7_500], 5_000)
    return np.clip(1 - (agi - start) / width, 0, 1)


def eip_parts(d: pd.DataFrame, no_ssn: np.ndarray, year: int) -> dict[str, np.ndarray]:
    """Each payment per tax unit under its identification-number rule, placed on the CPS holder.

    Income 2020 (ASEC 2021): EIP_CRD = EIP1 + EIP2 at full take-up. The EIP1 advance paid in 2020 follows
    6428(g)(2): nothing if a filer (either spouse on a joint return) lacks an SSN, with the armed-forces
    exception. The amended 6428(g)(1) credit, claimed on the 2020 return in 2021, gives $1,200 per SSN spouse
    and counts SSN children when a parent has an SSN; `eip1_catchup` is that credit less the advance. EIP2
    follows 6428A(g). Income 2021 (ASEC 2022): EIP_CRD = EIP3, $1,400 per SSN spouse and per SSN dependent.
    """
    ssn = ~no_ssn
    dependent = d.DEP_STAT.to_numpy() > 0
    child = dependent & (d.A_AGE.to_numpy() < 17)
    per_unit = pd.DataFrame({"unit": d.TAX_ID.to_numpy(), "filers": ~dependent, "filers_ssn": ~dependent & ssn,
                             "children": child, "children_ssn": child & ssn, "dependents": dependent,
                             "dependents_ssn": dependent & ssn,
                             "military": ~dependent & d.PRPERTYP.eq(3).to_numpy()}).groupby("unit").sum()
    holder = d.EIP_CRD.to_numpy() > 0
    if pd.Series(d.TAX_ID.to_numpy()[holder]).duplicated().any():
        raise SystemExit("[BLOCKED] more than one EIP holder in a tax unit")
    u = per_unit.reindex(d.TAX_ID.to_numpy()[holder])
    filestat, agi = d.FILESTAT.to_numpy()[holder], d.AGI.to_numpy()[holder].astype(float)
    joint = np.isin(filestat, JOINT)
    filers = np.where(joint, 2, 1)
    if not np.array_equal(u.filers.to_numpy(), filers):
        raise SystemExit("[BLOCKED] tax-unit filer count disagrees with FILESTAT")
    fs, military = u.filers_ssn.to_numpy(), u.military.to_numpy() > 0
    # Adults counted: joint returns keep both spouses when both have SSNs or one does and a spouse served.
    adults = np.where(joint & military & (fs >= 1), 2, fs)
    released = d.EIP_CRD.to_numpy()[holder].astype(float)
    out = {}
    if year == 2021:
        cut = reduction(filestat, agi)
        e1_full = np.maximum(1200 * filers + 500 * u.children.to_numpy() - cut, 0)
        e2_full = np.maximum(600 * filers + 600 * u.children.to_numpy() - cut, 0)
        if np.abs(e1_full + e2_full - released).max() > 1:
            raise SystemExit("[BLOCKED] EIP_CRD is not EIP1 + EIP2 of the unit's filers and children")
        kids = np.where(fs >= 1, u.children_ssn.to_numpy(), 0)
        allowed = (fs == filers) | (joint & military & (fs >= 1))
        advance = np.where(allowed, np.maximum(1200 * filers + 500 * u.children_ssn.to_numpy() - cut, 0), 0)
        credit = np.maximum(1200 * adults + 500 * kids - cut, 0)
        eip2 = np.maximum(600 * adults + 600 * kids - cut, 0)
        if (credit < advance - 1e-9).any():
            raise SystemExit("[BLOCKED] the amended EIP1 credit is below the advance")
        parts = {"eip1_advance": advance, "eip1_catchup": credit - advance, "eip2": eip2}
    elif year == 2022:
        phase = phase_eip3(filestat, agi)
        full = (1400 * filers + 1400 * u.dependents.to_numpy()) * phase
        if np.abs(full - released).max() > 1:
            raise SystemExit("[BLOCKED] EIP_CRD is not EIP3 of the unit's filers and dependents")
        parts = {"eip3": (1400 * adults + 1400 * u.dependents_ssn.to_numpy()) * phase}
    else:
        raise ValueError(year)
    for name, values in parts.items():
        vector = np.zeros(len(d))
        vector[holder] = values
        out[name] = vector
    if not no_ssn.any():
        total = sum(out.values())
        if np.abs(total - d.EIP_CRD.to_numpy()).max() > 1:
            raise SystemExit("[BLOCKED] the rebuilt payments do not add to EIP_CRD")
    return out


def key_vectors(d: pd.DataFrame, masks: dict[str, np.ndarray] | None, year: int) -> list[tuple]:
    """(key, status, person vector before allocation), and whether the key is an SPM-unit field."""
    raw = {k: d[v].to_numpy(float) for k, v in DOLLARS.items()}
    raw["refundable_credits"] = (d.EIT_CRED + d.ACTC_CRD).to_numpy(float)
    raw["all_cash"] = sum(raw[k] for k in ["social_security", "ssi", "cash_assistance", "unemployment", "veterans"])
    raw["eitc"] = d.EIT_CRED.to_numpy(float)
    raw["actc"] = d.ACTC_CRD.to_numpy(float)
    if year == 2022:
        raw["cdc"] = d.CDC_CRD.to_numpy(float)
    keys = [(k, "none", v, False) for k, v in raw.items()]
    keys += [(k, "none", unit_field(d, v), True) for k, v in UNITS.items()]
    keys.append(("population", "none", np.ones(len(d)), True))
    if masks is not None:
        for status, mask in masks.items():
            parts = eip_parts(d, mask, year)
            for name, vector in parts.items():
                # A catch-up exists only for a joint return with one SSN spouse. The Census model has no SSN
                # rule, and the full Borjas residual makes a citizen's spouse legal, so both leave it empty.
                if name == "eip1_catchup" and status in ("modeled", "borjas"):
                    if vector.any():
                        raise SystemExit(f"[BLOCKED] a {status} EIP1 catch-up appeared; recheck the spouse rule")
                    continue
                keys.append((name, status, vector, False))
            if year == 2021:
                keys.append(("eip_2020_total", status, sum(parts.values()), False))
    return keys


def measure(year: int) -> tuple[pd.DataFrame, dict]:
    d, hh = load(year)
    civ, target = canonical_target(d)
    weight = d.pwwgt0.to_numpy(float)
    reps = d[REPS].to_numpy(float)
    wc, wt = reps[civ], reps[target]
    population = float(weight[target].sum())
    mexico_born = float(weight[civ & d.PRCITSHP.isin([4, 5]).to_numpy() & d.PENATVTY.eq(303).to_numpy()].sum())
    if not (36e6 < population < 43e6 and 9e6 < mexico_born < 12.5e6):
        raise SystemExit(f"[BLOCKED] ASEC {year}: implausible union {population:,.0f} or Mexico-born {mexico_born:,.0f}")
    pop_rep = wt.sum(axis=0) / wc.sum(axis=0)
    masks = no_ssn_masks(d, hh) if year in EXTRA else None
    rows = []
    for key, status, vector, unit in key_vectors(d, masks, year):
        if not np.isfinite(vector).all() or (vector < 0).any():
            raise SystemExit(f"[BLOCKED] ASEC {year}: invalid key {key}")
        for allocation in ("personal", "shared"):
            v = vector if (unit or allocation == "personal") else equal_unit_share(vector, d.SPM_ID)
            national, targeted = float(v[civ] @ weight[civ]), float(v[target] @ weight[target])
            if national <= 0:
                raise SystemExit(f"[BLOCKED] ASEC {year}: empty key {key}")
            share_rep = (v[target] @ wt) / (v[civ] @ wc)
            use_rep = share_rep / pop_rep
            rows.append(dict(survey_year=year, income_year=year - 1, allocation=allocation, key=key, status=status,
                             national_bn=national / 1e9, target_bn=targeted / 1e9, share=targeted / national,
                             share_se=sdr(share_rep), pop_share=population / float(weight[civ].sum()),
                             relative_use=targeted / national / (population / float(weight[civ].sum())),
                             relative_use_se=sdr(use_rep),
                             target_positive_persons_m=float(weight[target & (v > 0)].sum()) / 1e6))
    audit = dict(survey_year=year, persons=len(d), target_population_m=population / 1e6,
                 mexico_born_m=mexico_born / 1e6, validation=validation_method(d) if year >= 2022 else None)
    for status in ("borjas", "borjas_own"):                  # people treated as lacking an SSN
        audit[f"no_ssn_{status}_union_m"] = float(weight[target & masks[status]].sum()) / 1e6 if masks else np.nan
        audit[f"no_ssn_{status}_national_m"] = float(weight[civ & masks[status]].sum()) / 1e6 if masks else np.nan
    return pd.DataFrame(rows), audit


def validation_method(d: pd.DataFrame) -> dict[str, float]:
    """Union totals ($bn) with the validation lane's weighting (validation_fiscal_years_2026_09_28/analysis.py
    `load`): members with PRPERTYP 1-2, each carrying its SPM-unit head's weight."""
    heads = d.loc[d.SPM_HEAD.eq(1), ["SPM_ID", "pwwgt0"]].set_index("SPM_ID")
    if heads.index.duplicated().any():
        raise SystemExit("[BLOCKED] an SPM unit has two heads")
    head_weight = heads.pwwgt0.reindex(d.SPM_ID).to_numpy()
    size = d.groupby("SPM_ID").SPM_ID.transform("size").to_numpy()
    union = (VALIDATION_LANE.group_codes(d) < 3) & d.PRPERTYP.isin([1, 2]).to_numpy()
    out = {}
    for metric, field, how in (("snap_shared", "SPM_SNAPSUB", "first"), ("ss_shared", "SS_VAL", "sum"),
                               ("ssi_shared", "SSI_VAL", "sum")):
        total = d.groupby("SPM_ID")[field].transform(how).to_numpy(float)
        out[metric] = float((total / size)[union] @ head_weight[union]) / 1e9
    return out


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out-dir", type=Path, default=HERE / "derived")
    parser.add_argument("--years", type=int, nargs="*", default=list(SOURCES), help="survey years (testing)")
    args = parser.parse_args()
    args.out_dir.mkdir(parents=True, exist_ok=True)
    frames, audits = [], []
    for year in args.years:
        frame, audit = measure(year)
        frames.append(frame)
        audits.append(audit)
        print(f"  ✓ ASEC {year} (income {year - 1}): union {audit['target_population_m']:.3f}m, "
              f"Mexico-born {audit['mexico_born_m']:.3f}m")
    table = pd.concat(frames, ignore_index=True)
    if args.years != list(SOURCES):
        print("  ! partial run: gates skipped, nothing written")
        return
    gate_account(table)
    gate_validation(audits)
    table.to_csv(args.out_dir / "measured_shares.csv", index=False, lineterminator="\n", float_format="%.10g")
    pd.DataFrame([{k: v for k, v in a.items() if k != "validation"} for a in audits]).to_csv(
        args.out_dir / "survey_audit.csv", index=False, lineterminator="\n", float_format="%.10g")


def gate_validation(audits: list[dict]) -> None:
    lane = pd.read_csv(VALIDATION)
    union = lane[lane.group != "other"].groupby(["income_year", "metric"]).amount_bn.sum()
    worst = 0.0
    for audit in audits:
        for metric, value in (audit["validation"] or {}).items():
            worst = max(worst, abs(value / union[(audit["survey_year"] - 1, metric)] - 1))
    if worst > 1e-9:
        raise SystemExit(f"[BLOCKED] the validation lane's union SNAP/SS/SSI are not reproduced: {worst:.2e}")
    print(f"  ✓ validation lane's union SNAP, SS and SSI for 2021-2024 reproduced (max rel diff {worst:.1e})")


def gate_account(table: pd.DataFrame) -> None:
    account = pd.read_csv(ACCOUNT_KEYS).set_index(["allocation", "key"])
    mine = table[(table.survey_year == 2025) & (table.status == "none")].set_index(["allocation", "key"])
    common = mine.index.intersection(account.index)
    if len(common) != 24:
        raise SystemExit(f"[BLOCKED] expected 24 account keys to compare, found {len(common)}")
    share = (mine.loc[common, "share"] - account.loc[common, "target_share"]).abs().max()
    national = (mine.loc[common, "national_bn"] * 1e9 / account.loc[common, "national_key_total"] - 1).abs().max()
    if share > 1e-12 or national > 1e-12:
        raise SystemExit(f"[BLOCKED] ASEC 2025 does not reproduce the account's keys: {share:.2e}, {national:.2e}")
    print(f"  ✓ ASEC 2025 reproduces the account's 24 incidence keys (max share diff {share:.1e})")


if __name__ == "__main__":
    main()
