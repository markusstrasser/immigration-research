"""Exact observed item10 completion IDs on the existing legal-form payroll key.

Only the main estimate is available here. Returned shares are ADDITIONS to the
old observed union/lineage shares, not replacements and not replicate estimates.
All authoritative person weights come from main_case15 union_people.json.
"""
from __future__ import annotations

import hashlib
import json
import resource
import sys
import time
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
FISCAL = HERE.parent
PEOPLE = FISCAL / "main_case_2026_10_15/derived/union_people.json"


def digest(path):
    h = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def completion_shares(z, core, profiles, source, sector_codes):
    """Return main-only incremental legal-job shares and measurement metadata.

    Parameters match job_keys.calculate's fresh z/core/profiles/source. The
    sector_codes argument is k1_legal.SECTOR_CODE (BEA broad name -> NAICS).
    Results: shares[naics][form] is a scalar extra share (or None if the legal
    profile is unavailable); pooled_shares['61+81'][form] pools sufficient payroll
    amounts. Forms are SUSB '3'/'4'/'5'. metadata records pins, population, excluded
    scope and wage closure. No caller should broadcast these into replicates and
    call the result completion sampling uncertainty.
    """
    start = time.perf_counter()
    document = json.loads(PEOPLE.read_text())
    if document["key"] != ["PH_SEQ", "PPPOS"]:
        raise RuntimeError("[BLOCKED] completion person key changed")
    selected = [r for r in document["records"] if r["central_reporter"] or r["observed_nonreporter"]]
    if any(r["central_reporter"] and r["observed_nonreporter"] for r in selected):
        raise RuntimeError("[BLOCKED] reporter/nonreporter completion overlap")
    wanted = pd.DataFrame(selected)
    if wanted.empty or wanted.duplicated(["PH_SEQ", "PPPOS"]).any():
        raise RuntimeError("[BLOCKED] empty or duplicate completion IDs")
    if not np.isfinite(wanted.people).all() or not (wanted.people > 0).all():
        raise RuntimeError("[BLOCKED] invalid authoritative completion weights")
    count_reporters = float(wanted.loc[wanted.central_reporter, "people"].sum())
    count_nonreporters = float(wanted.loc[wanted.observed_nonreporter, "people"].sum())
    if abs(count_reporters + count_nonreporters - 517435.75719317) > 1e-6:
        raise RuntimeError("[BLOCKED] completion differs from v8's 517435.75719317 people")
    for value, key in [(count_reporters, "central_reporters"), (count_nonreporters, "observed_nonreporters")]:
        if abs(value - document["counts"][key]) > 1e-6:
            raise RuntimeError(f"[BLOCKED] authoritative completion headcount changed: {key}")
    source_hashes = {}
    for relative, expected in document["source_hashes"].items():
        actual = digest(FISCAL / relative)
        if actual != expected:
            raise RuntimeError(f"[BLOCKED] stale completion-person producer: {relative}")
        source_hashes[relative] = actual
    source_hashes[str(PEOPLE.relative_to(FISCAL))] = digest(PEOPLE)
    source_hashes[str(Path(source.CROSSWALK).relative_to(FISCAL))] = digest(source.CROSSWALK)
    source_hashes[str(Path(source.CPS).relative_to(FISCAL))] = source.CPS_SHA
    key_index = pd.MultiIndex.from_frame(wanted[["PH_SEQ", "PPPOS"]])
    columns = ["PH_SEQ", "PPPOS", "WSAL_VAL", "INDUSTRY", "LJCW", "NOEMP"]
    pieces = []
    # Principal pinned CPS source; chunks keep physical memory comfortably below
    # the per-process limit even while another worker replays the full core.
    with zipfile.ZipFile(source.checked(source.CPS, source.CPS_SHA)) as archive:
        for chunk in pd.read_csv(archive.open("pppub25.csv"), usecols=columns, chunksize=20_000):
            keep = pd.MultiIndex.from_frame(chunk[["PH_SEQ", "PPPOS"]]).isin(key_index)
            if keep.any():
                pieces.append(chunk.loc[keep].copy())
    if not pieces:
        raise RuntimeError("[BLOCKED] no completion IDs in pinned CPS")
    found = pd.concat(pieces, ignore_index=True)
    data = wanted.merge(found, on=["PH_SEQ", "PPPOS"], how="left", validate="one_to_one", indicator=True)
    if len(found) != len(wanted) or not data["_merge"].eq("both").all():
        raise RuntimeError("[BLOCKED] incomplete completion ID match")
    if data[columns].isna().any().any():
        raise RuntimeError("[BLOCKED] missing completion wage or industry field")
    if not np.isfinite(data.WSAL_VAL).all():
        raise RuntimeError("[BLOCKED] nonfinite completion wages")
    # Frozen topcoded earners are reallocated across national cells. Reject that
    # route here until its completion-specific redistribution is implemented.
    if data.WSAL_VAL.ge(source.TOP).any():
        raise RuntimeError("[BLOCKED] completion wage >= frozen TOP; implement exact top redistribution")
    corr = float(core["corr"]["G3plus"])
    if not np.isfinite(corr) or corr <= 0:
        raise RuntimeError("[BLOCKED] invalid G3 completion wage correction")
    positive = data.WSAL_VAL.gt(0)
    if not data.loc[positive, "NOEMP"].isin(range(7)).all():
        raise RuntimeError("[BLOCKED] unsupported completion NOEMP code")
    crosswalk = pd.read_csv(source.CROSSWALK)
    data["cell"] = source.cell_of(data, crosswalk)
    if (positive & data.cell.eq("UNMAPPED")).any():
        raise RuntimeError("[BLOCKED] positive completion wage has unmapped industry")
    data["sector"] = data.cell.map(source.SECTOR).map(sector_codes)
    data["corrected_wage"] = data.WSAL_VAL.clip(lower=0) * data.people * corr
    cells = np.asarray(z["cells"]).astype(str)
    cell_sector = np.array([sector_codes.get(source.SECTOR[c]) for c in cells], dtype=object)
    national7 = np.asarray(z["size_wages_national"])
    if national7.ndim != 3 or national7.shape[0] != len(cells) or national7.shape[1] != 7:
        raise RuntimeError("[BLOCKED] fresh core size-wage shape changed")
    national5 = np.stack([national7[:, 0], national7[:, 1], national7[:, 2:4].sum(axis=1),
                          national7[:, 4], national7[:, 5:7].sum(axis=1)], axis=1)[:, :, 0]
    if not np.isfinite(national5).all() or (national5 < 0).any():
        raise RuntimeError("[BLOCKED] invalid national wage denominators")
    noemp_map = {0: 0, 1: 1, 2: 2, 3: 2, 4: 3, 5: 4, 6: 4}
    supported = data.sector.notna() & ~data.cell.isin(["111CA", "482"])
    shares, sufficient = {}, {}
    for sec in sorted(set(cell_sector) - {None}):
        used = (cell_sector == sec) & ~np.isin(cells, ["111CA", "482"])
        sector_wages = np.zeros(5)
        rows = data.loc[supported & positive & data.sector.eq(sec)]
        for row in rows.itertuples():
            sector_wages[noemp_map[int(row.NOEMP)]] += float(row.corrected_wage)
        shares[sec], sufficient[sec] = {}, {}
        for form in ["3", "4", "5"]:
            prop = profiles[sec][form]
            if prop is None:
                shares[sec][form] = None
                sufficient[sec][form] = None
                continue
            prop = np.asarray(prop)
            if prop.shape != (5,) or not np.isfinite(prop).all() or ((prop < 0) | (prop > 1)).any():
                raise RuntimeError(f"[BLOCKED] invalid legal-form profile {sec}/{form}")
            denominator = float((national5[used] * prop[None, :]).sum())
            numerator = float((sector_wages * prop).sum())
            if denominator <= 0:
                raise RuntimeError(f"[BLOCKED] missing principal legal payroll denominator {sec}/{form}")
            shares[sec][form] = numerator / denominator
            sufficient[sec][form] = (numerator, denominator)
    pooled = {"61+81": {}}
    for form in ["3", "4", "5"]:
        parts = [sufficient[sec][form] for sec in ["61", "81"]]
        pooled["61+81"][form] = None if any(x is None for x in parts) else sum(x[0] for x in parts) / sum(x[1] for x in parts)
    excluded = data.loc[~supported & positive].groupby("cell").corrected_wage.sum()
    supported_wage = float(data.loc[supported, "corrected_wage"].sum())
    corrected_wage = float(data.corrected_wage.sum())
    if abs(supported_wage + float(excluded.sum()) - corrected_wage) > 1e-4:
        raise RuntimeError("[BLOCKED] completion supported/excluded wage closure")
    rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    rss_bytes = rss if sys.platform == "darwin" else rss * 1024
    if rss_bytes >= 2_500_000_000:
        raise RuntimeError("[BLOCKED] completion reader exceeds 2.5GB")
    # Keep nondeterministic telemetry out of the returned derived-data payload.
    print(json.dumps({"completion_runtime_s": time.perf_counter() - start, "peak_rss_bytes": rss_bytes}))
    return {"shares": shares, "pooled_shares": pooled, "metadata": {
        "selected_records": len(wanted), "reporter_people": count_reporters,
        "observed_nonreporter_people": count_nonreporters,
        "completion_people": count_reporters + count_nonreporters,
        "wage_earners": int(positive.sum()),
        "raw_wage_bn": float((data.WSAL_VAL.clip(lower=0) * data.people).sum()) / 1e9,
        "corrected_wage_bn": corrected_wage / 1e9, "supported_wage_bn": supported_wage / 1e9,
        "excluded_wages_by_cell_bn": {k: float(v) / 1e9 for k, v in excluded.items()},
        "G3_correction": corr, "top_wage_gate": "PASS: no selected completion wage >= TOP",
        "uncertainty": "main estimate only; completion replicate-weight uncertainty not measured",
        "application": "add extra shares once to observed union/lineage main estimates; no lineage-rate multiplier",
        "source_hashes": source_hashes}}
