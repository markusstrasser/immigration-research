"""Retrospective conditional temporal validation; no causal removal estimate."""
import argparse
import hashlib
import json
from pathlib import Path
import zipfile

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
ARMS = ("frozen", "proportional", "trend_only", "proportional_trend", "free_trend", "asymmetric_trend")
FIPS = {1, 2, 4, 5, 6, 8, 9, 10, 11, 12, 13, 15, 16, 17, 18, 19, 20, 21, 22,
        23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40,
        41, 42, 44, 45, 46, 47, 48, 49, 50, 51, 53, 54, 55, 56}
PINS = {}
COVERAGE = []


def pin(path):
    path = Path(path)
    with path.open("rb") as stream:
        PINS[str(path)] = hashlib.file_digest(stream, "sha256").hexdigest()
    return path


def unique(frame, keys, label):
    if frame.duplicated(keys).any():
        examples = frame.loc[frame.duplicated(keys, keep=False), keys].head().to_dict("records")
        raise ValueError(f"Duplicate {label}: {examples}")


def load_primary(root):
    folder = root / "infra/immigration-fiscal/school_flight_2026_09_18"
    pieces = {}
    for kind in ("fin", "dir"):
        frames = []
        for year in (2000, 2010, 2019):
            files = sorted((folder / "_cache/dist").glob(f"{kind}_{year}_*.csv"))
            if len(files) != 51:
                raise ValueError(f"Missing {kind} state files in {year}")
            part = pd.concat([pd.read_csv(pin(p), dtype={"leaid": str}) for p in files], ignore_index=True)
            if set(part.fips) != FIPS or not part.year.eq(year).all():
                raise ValueError("Source wave/state mismatch")
            frames.append(part)
        pieces[kind] = pd.concat(frames, ignore_index=True)
        unique(pieces[kind], ["leaid", "year"], kind)
    frame = pieces["fin"].merge(pieces["dir"][["leaid", "year", "fips", "agency_type", "agency_charter_indicator"]],
        on=["leaid", "year", "fips"], how="inner", validate="one_to_one")
    cpi = pd.read_csv(pin(folder / "_cache/cpiaucsl_annual.csv"))
    cpi["year"] = pd.to_datetime(cpi.observation_date).dt.year
    cpi = cpi.set_index("year").CPIAUCSL
    for year, group in frame.groupby("year"):
        COVERAGE.append(dict(panel="primary", step="joined", year=int(year), rows=len(group)))
    frame = frame.loc[frame.agency_type.isin([1, 2]) & frame.agency_charter_indicator.ne(1)].copy()
    frame["pupils"] = frame.enrollment_fall_responsible
    frame["current"] = frame.exp_current_elsec_total * frame.year.map(cpi.loc[2020] / cpi)
    frame["instruction"] = frame.exp_current_instruction_total * frame.year.map(cpi.loc[2020] / cpi)
    return frame[["leaid", "year", "fips", "pupils", "current", "instruction"]]


def pair(frame, a, b, outcomes, label):
    """Interval-local eligibility: future endpoint never changes training rows."""
    cols = ["leaid", "fips", "pupils", *outcomes]
    parts = []
    for year in (a, b):
        part = frame.loc[frame.year.eq(year), cols].copy()
        unique(part, ["leaid"], f"{label} {year}")
        positive = np.isfinite(part[["pupils", *outcomes]]).all(axis=1)
        positive &= part.pupils.ge(100) & part[outcomes].gt(0).all(axis=1)
        part = part.loc[positive]
        parts.append(part)
        COVERAGE.append(dict(panel=label, step="valid_endpoint", year=year, rows=len(part), pupils=float(part.pupils.sum())))
    joined = parts[0].merge(parts[1], on="leaid", suffixes=("0", "1"), validate="one_to_one")
    if not joined.fips0.eq(joined.fips1).all():
        raise ValueError("A district crosses state boundaries")
    joined["fips"] = joined.fips0.astype(int)
    joined["dx"] = np.log(joined.pupils1 / joined.pupils0)
    joined["year0"], joined["year1"] = a, b
    COVERAGE.append(dict(panel=label, step="matched_interval", year=f"{a}-{b}", rows=len(joined),
                         pupils=float(joined.pupils0.sum()), states=int(joined.fips.nunique())))
    return joined


def fit(train, outcome, arm, weighted, expected_years):
    if set(train.year0) != {expected_years[0]} or set(train.year1) != {expected_years[1]}:
        raise ValueError("Training years do not match frozen design")
    x = train.dx.to_numpy(float)
    y = np.log(train[f"{outcome}1"] / train[f"{outcome}0"]).to_numpy(float)
    w = train.pupils0.to_numpy(float) if weighted else np.ones(len(train))
    state, labels = pd.factorize(train.fips, sort=True)
    den = np.bincount(state, weights=w)
    mean = lambda values: np.bincount(state, weights=w * values) / den
    if arm in ("frozen", "trend_only"):
        beta = np.array([0.0])
    elif arm in ("proportional", "proportional_trend"):
        beta = np.array([1.0])
    else:
        design = np.column_stack((np.maximum(x, 0), np.minimum(x, 0))) if arm == "asymmetric_trend" else x[:, None]
        xd = design - np.column_stack([mean(design[:, j])[state] for j in range(design.shape[1])])
        yd = y - mean(y)[state]
        beta, _, rank, _ = np.linalg.lstsq(xd * np.sqrt(w[:, None]), yd * np.sqrt(w), rcond=None)
        if rank != design.shape[1]:
            raise ValueError("Enrollment-response slope is not identified")
    if len(beta) == 2:
        enrollment = beta[0] * np.maximum(x, 0) + beta[1] * np.minimum(x, 0)
    else:
        enrollment = beta[0] * x
    alpha = mean(y - enrollment) if arm.endswith("trend") or arm == "trend_only" else np.zeros(len(labels))
    return dict(arm=arm, beta=beta.tolist(), alpha={int(k): float(v) for k, v in zip(labels, alpha)})


def predict(rule, test, horizon_ratio):
    alpha = test.fips.map(rule["alpha"])
    if alpha.isna().any():
        raise ValueError("Test-state intercept not supported in training")
    beta = rule["beta"]
    enrollment = beta[0] * test.dx if len(beta) == 1 else beta[0] * test.dx.clip(lower=0) + beta[1] * test.dx.clip(upper=0)
    result = alpha * horizon_ratio + enrollment
    if not np.isfinite(result).all():
        raise ValueError("Nonfinite prediction")
    return result.to_numpy(float)


def supported_test(train, test, label):
    unsupported = ~test.fips.isin(train.fips.unique())
    if unsupported.any():
        excluded = test.loc[unsupported]
        COVERAGE.append(dict(panel=label, step="unsupported_state_exclusion", year=int(test.year1.iloc[0]),
            rows=len(excluded), pupils=float(excluded.pupils0.sum()), excluded_states=','.join(map(str, sorted(excluded.fips.unique())))))
        print(f"[DEGRADED] {label}: {len(excluded)} test districts excluded; missing training-state intercepts {sorted(excluded.fips.unique())}")
    return test.loc[~unsupported].copy()


def score(rows, weights):
    actual, predicted, initial = rows.actual.to_numpy(), rows.predicted.to_numpy(), rows.initial.to_numpy()
    error = rows.pred_log_change.to_numpy() - rows.actual_log_change.to_numpy()
    avg = lambda x: float(np.average(x, weights=weights))
    level = predicted - actual
    return dict(n=len(rows), states=int(rows.fips.nunique()), log_rmse=np.sqrt(avg(error ** 2)),
                log_mae=avg(np.abs(error)), log_bias=avg(error), growth_mae_pp=100 * avg(np.abs(level / initial)),
                level_mae=avg(np.abs(level)), level_rmse=np.sqrt(avg(level ** 2)),
                aggregate_actual=float(actual.sum()), aggregate_predicted=float(predicted.sum()),
                aggregate_bias_percent=100 * float(level.sum() / actual.sum()))


def score_all(predictions):
    rows = []
    for keys, group in predictions.groupby(["panel", "outcome", "fit_weight", "arm"]):
        masks = {"all": np.ones(len(group), bool), "growing": group.dx.gt(0), "shrinking": group.dx.lt(0),
                 "unchanged": group.dx.eq(0), "small_change": group.dx.abs().le(.2)}
        for stratum, mask in masks.items():
            part = group.loc[mask]
            if part.empty:
                continue
            for weight in ("district", "initial_pupils"):
                w = np.ones(len(part)) if weight == "district" else part.pupils0.to_numpy()
                rows.append(dict(zip(["panel", "outcome", "fit_weight", "arm"], keys),
                                 stratum=stratum, score_weight=weight, **score(part, w)))
    return pd.DataFrame(rows)


def bootstrap(predictions):
    result = []
    pairs = [("free_trend", "proportional_trend"), ("asymmetric_trend", "free_trend"),
             ("proportional_trend", "trend_only"), ("proportional", "frozen")]
    for keys, group in predictions.groupby(["panel", "outcome", "fit_weight"]):
        for score_weight in ("district", "initial_pupils"):
            weight = np.ones(len(group)) if score_weight == "district" else group.pupils0.to_numpy()
            group = group.assign(weight=weight, loss=weight * (group.pred_log_change - group.actual_log_change) ** 2)
            sums = group.groupby(["fips", "arm"])[["weight", "loss"]].sum().unstack("arm")
            rng = np.random.default_rng(20260928)
            draws = rng.multinomial(len(sums), np.full(len(sums), 1 / len(sums)), size=1000)
            for arm, reference in pairs:
                ar = sums.loss[arm].to_numpy(); aw = sums.weight[arm].to_numpy()
                br = sums.loss[reference].to_numpy(); bw = sums.weight[reference].to_numpy()
                differences = np.sqrt((draws @ ar) / (draws @ aw)) - np.sqrt((draws @ br) / (draws @ bw))
                low, high = np.quantile(differences, [.025, .975])
                result.append(dict(zip(["panel", "outcome", "fit_weight"], keys), score_weight=score_weight,
                    arm=arm, reference=reference, rmse_difference=np.sqrt(ar.sum()/aw.sum()) - np.sqrt(br.sum()/bw.sum()),
                    low95=low, high95=high, state_clusters=len(sums), draws=1000))
    return pd.DataFrame(result)


def run_panel(frame, years, outcomes, label, joint=False):
    predictions, rules = [], []
    a, b, c = years
    for outcome in outcomes:
        required = outcomes if joint else [outcome]
        train = pair(frame, a, b, required, label + "_" + outcome)
        test = pair(frame, b, c, required, label + "_" + outcome)
        test = supported_test(train, test, label + "_" + outcome)
        for weighted in (False, True):
            fit_weight = "initial_pupils" if weighted else "district"
            for arm in ARMS:
                rule = fit(train, outcome, arm, weighted, (a, b))
                pred = predict(rule, test, (c - b) / (b - a))
                rules.append(dict(panel=label, outcome=outcome, fit_weight=fit_weight, n_train=len(train),
                                  training_years=[a, b], testing_years=[b, c], **rule))
                initial = test[f"{outcome}0"].to_numpy()
                predictions.append(test[["leaid", "fips", "pupils0", "dx"]].assign(panel=label, outcome=outcome,
                    fit_weight=fit_weight, arm=arm, initial=initial, actual=test[f"{outcome}1"].to_numpy(),
                    predicted=initial * np.exp(pred), pred_log_change=pred,
                    actual_log_change=np.log(test[f"{outcome}1"].to_numpy() / initial)))
    return pd.concat(predictions, ignore_index=True), rules


def teachers(root, year):
    folder = root / "infra/immigration-fiscal/school_dilution_2026_09_24/_cache"
    if year == 2000:
        files = sorted((folder / "ccd").glob("dir_2000_*.csv"))
        if len(files) != 51:
            raise ValueError("Missing fall2000 teacher files")
        raw = pd.concat([pd.read_csv(pin(p), dtype={"leaid": str}) for p in files], ignore_index=True)
        raw = raw.rename(columns={"lea_name": "name", "teachers_total_fte": "teachers"})
    else:
        name = {2018: "ccd_lea_059_1819_l_1a_091019", 2023: "ccd_lea_059_2324_l_1a_073124"}[year]
        with zipfile.ZipFile(pin(folder / "nces" / f"{name}.zip")) as archive:
            raw = pd.read_csv(archive.open(f"{name}.csv"), dtype=str, encoding="latin-1",
                usecols=["LEAID", "LEA_NAME", "STAFF", "STAFF_COUNT", "TOTAL_INDICATOR"])
        raw = raw.loc[raw.STAFF.eq("Teachers") & raw.TOTAL_INDICATOR.eq("Derived - Major Staffing Category")]
        raw = raw.rename(columns={"LEAID": "leaid", "LEA_NAME": "name", "STAFF_COUNT": "teachers"})
    unique(raw, ["leaid"], f"teachers {year} before NYC aggregation")
    raw["teachers"] = pd.to_numeric(raw.teachers, errors="coerce")
    raw = raw.loc[raw.teachers.gt(0)].copy()
    # This official geographic/finance crosswalk matches the existing lane; its
    # names criterion is retained explicitly rather than importing side-effectful code.
    nyc = raw.name.fillna("").str.upper().str.startswith("NEW YORK CITY GEOGRAPHIC DISTRICT")
    raw.loc[nyc, "leaid"] = "3620580"
    result = raw.groupby("leaid", as_index=False).teachers.sum(min_count=1)
    COVERAGE.append(dict(panel="joint_resources", step="teacher_source", year=year, rows=len(result),
                         teacher_fte=float(result.teachers.sum()), nyc_component_rows=int(nyc.sum())))
    return result


def load_joint(root):
    lane = root / "infra/immigration-fiscal/school_dilution_2026_09_24"
    raw = pd.read_parquet(pin(lane / "_cache/panel.parquet"))
    pin(lane / "build_panel.py")
    pin(lane / "derived/sources_f33.json")
    raw = raw.loc[raw.year.isin([2001, 2019, 2024]) & raw.SCHLEV.isin(["01", "02", "03"]) & raw.leaid.ne("") & raw.fips.isin(FIPS)].copy()
    unique(raw, ["leaid", "year"], "joint finance")
    rows = []
    for fall, fiscal in ((2000, 2001), (2018, 2019), (2023, 2024)):
        part = raw.loc[raw.year.eq(fiscal)].merge(teachers(root, fall), on="leaid", validate="one_to_one")
        part["pupils"] = part.V33
        part["current"] *= part.defl_2024
        part["instruction"] *= part.defl_2024
        rows.append(part[["leaid", "year", "fips", "pupils", "current", "instruction", "teachers"]])
    return pd.concat(rows, ignore_index=True)


def joint_observed(frame):
    paired = pair(frame, 2019, 2024, ["current", "instruction", "teachers"], "joint_observed")
    rows = []
    for name, mask in {"all": np.ones(len(paired), bool), "growing": paired.dx.gt(0), "shrinking": paired.dx.lt(0),
                       "unchanged": paired.dx.eq(0), "small_change": paired.dx.abs().le(.2)}.items():
        sub = paired.loc[mask]
        if sub.empty:
            continue
        row = dict(stratum=name, n=len(sub), states=int(sub.fips.nunique()))
        for outcome in ("pupils", "current", "instruction", "teachers"):
            row[f"{outcome}_growth_percent"] = 100 * (sub[f"{outcome}1"].sum() / sub[f"{outcome}0"].sum() - 1)
        row["pupil_teacher_ratio_initial"] = sub.pupils0.sum() / sub.teachers0.sum()
        row["pupil_teacher_ratio_final"] = sub.pupils1.sum() / sub.teachers1.sum()
        rows.append(row)
    return pd.DataFrame(rows)


def field_inventory(root):
    """Document the join boundary; score-bearing public ECLS IDs are internal."""
    peers = root / "infra/immigration-fiscal/school_peer_checks_2026_09_20"
    rows = []
    for cohort, suffix in (("1998", "selected.parquet"), ("2011", "ecls_k2011/selected.parquet")):
        path = pin(peers / "_cache" / suffix)
        data = pd.read_parquet(path)
        cols = list(data.columns)
        candidates = [c for c in cols if any(token in c.upper() for token in ("LEAID", "NCESSCH", "NCESID"))]
        rows.append(dict(source=str(path), cohort=cohort, rows=len(data), fields=cols,
                         district_or_external_school_keys=candidates,
                         internal_school_keys=[c for c in cols if c.startswith("S") and c.endswith("_ID")],
                         conclusion="No external CCD/LEA identifier in held extract; no valid district finance join."))
    pin(peers / "DATASET_CARD.md")
    return rows


def state_quality(root, joint_frame):
    paired = pair(joint_frame, 2019, 2024, ["current", "instruction", "teachers"], "quality_observed")
    money = root / "infra/immigration-fiscal/school_dilution_2026_09_24/_cache/panel.parquet"
    raw = pd.read_parquet(money)
    raw = raw.loc[raw.year.isin([2019, 2024]) & raw.SCHLEV.isin(["01", "02", "03"]) & raw.leaid.ne("") & raw.fips.isin(FIPS)
                  & raw.V33.ge(100) & raw.current.gt(0) & raw.instruction.gt(0)]
    denominators = raw.groupby(["fips", "year"]).V33.sum()
    states = ("AL AK AZ AR CA CO CT DE DC FL GA HI ID IL IN IA KS KY LA ME MD MA MI MN MS MO MT NE NV NH "
              "NJ NM NY NC ND OH OK OR PA RI SC SD TN TX UT VT VA WA WV WI WY").split()
    crosswalk = dict(zip(sorted(FIPS), states))
    rows = []
    for state, group in paired.groupby("fips"):
        row = dict(fips=int(state), jurisdiction=crosswalk[state], matched_districts=len(group))
        for outcome in ("pupils", "current", "instruction", "teachers"):
            for end in (0, 1):
                row[f"{outcome}{end}"] = float(group[f"{outcome}{end}"].sum())
        row["pupil_teacher_ratio0"] = row["pupils0"] / row["teachers0"]
        row["pupil_teacher_ratio1"] = row["pupils1"] / row["teachers1"]
        for year, end in ((2019, 0), (2024, 1)):
            row[f"matched_pupil_share{end}"] = row[f"pupils{end}"] / denominators.loc[(state, year)]
        rows.append(row)
    resource = pd.DataFrame(rows)
    base = root / "infra/immigration-fiscal/school_systemwide_2026_09_27"
    pin(base / "acquire_naep.py")
    outputs, national = [], []
    for subject in ("mathematics", "reading"):
        for grade in (4, 8):
            path = pin(base / f"_cache/naep/{subject}_g{grade}_TOTAL_MN-MN_all.json")
            payload = json.loads(path.read_text())
            data = pd.DataFrame(payload["response"]["result"])
            data = data.loc[data.year.isin([2019, 2024]) & data.isStatDisplayable.eq(1)].copy()
            unique(data, ["jurisdiction", "year"], "NAEP total")
            a = data.loc[data.year.eq(2019), ["jurisdiction", "value", "stdError"]]
            b = data.loc[data.year.eq(2024), ["jurisdiction", "value", "stdError"]]
            scores = a.merge(b, on="jurisdiction", suffixes=("0", "1"), validate="one_to_one")
            scores["score_change"] = scores.value1 - scores.value0
            scores["score_change_se_independent_cycles"] = np.sqrt(scores.stdError0**2 + scores.stdError1**2)
            joined = resource.merge(scores, on="jurisdiction", validate="one_to_one")
            outputs.append(joined.assign(subject=subject, grade=grade, source_url=payload["url"]))
            national.append(scores.loc[scores.jurisdiction.eq("NP")].assign(subject=subject, grade=grade, source_url=payload["url"]))
    return pd.concat(outputs, ignore_index=True), pd.concat(national, ignore_index=True)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-root", type=Path, default=HERE.parents[2])
    parser.add_argument("--out-dir", type=Path, default=HERE / "derived")
    args = parser.parse_args()
    out = args.out_dir
    out.mkdir(parents=True, exist_ok=True)
    receipt = out / "audit.json"
    if receipt.exists():
        receipt.unlink()
    pin(HERE / "Design.md")
    pin(HERE / "validate.py")
    primary, r1 = run_panel(load_primary(args.source_root), (2000, 2010, 2019), ["current", "instruction"], "prepandemic")
    joint_frame = load_joint(args.source_root)
    joint, r2 = run_panel(joint_frame, (2001, 2019, 2024), ["current", "instruction", "teachers"], "joint_resources", joint=True)
    predictions = pd.concat([primary, joint], ignore_index=True)
    tables = {"scores": score_all(predictions), "paired_score_intervals": bootstrap(predictions),
              "joint_observed": joint_observed(joint_frame), "coverage": pd.DataFrame(COVERAGE)}
    inventory = field_inventory(args.source_root)
    tables["state_resource_quality"], tables["naep_national"] = state_quality(args.source_root, joint_frame)
    predictions.to_parquet(out / "predictions.parquet", index=False)
    for name, table in tables.items():
        table.to_csv(out / f"{name}.csv", index=False, lineterminator="\n", float_format="%.10g")
    (out / "rules.json").write_text(json.dumps(r1 + r2, indent=2) + "\n")
    (out / "field_inventory.json").write_text(json.dumps(inventory, indent=2) + "\n")
    for path, digest in PINS.items():
        with Path(path).open("rb") as stream:
            if hashlib.file_digest(stream, "sha256").hexdigest() != digest:
                raise ValueError(f"Input changed during run: {path}")
    outputs = {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in out.iterdir() if p.name != "audit.json" and p.is_file()}
    receipt.write_text(json.dumps(dict(source_hashes=PINS, outputs=outputs, prediction_rows=len(predictions),
        interpretation="Retrospective conditional temporal prediction, no identified causal removal effect", bootstrap_seed=20260928), indent=2) + "\n")
    display = tables["scores"].query("outcome == 'current' and stratum == 'all' and fit_weight == 'district' and score_weight == 'district'")
    print(display[["panel", "arm", "n", "log_rmse", "growth_mae_pp", "aggregate_bias_percent"]].to_string(index=False))
    print(tables["joint_observed"].to_string(index=False))


if __name__ == "__main__":
    main()
