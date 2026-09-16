#!/usr/bin/env python3
"""Re-acquire the LEHD QWI state x year x quarter x industry x education panel.

Source: Census LEHD Quarterly Workforce Indicators, `se` (sex-by-education) endpoint.
        https://api.census.gov/data/timeseries/qwi/se

Batching (matches the original 2026-04-18 pull recorded in repo CYCLE.md line 26):
    one API call per (industry x education) pair = 9 x 4 = 36 calls,
    each call covering all 51 state FIPS and the full 2003-Q1..2023-Q4 range.
    Full grid = 51 states x 84 quarters x 9 industries x 4 education = 154,224 rows.
    The live panel is smaller because QWI suppresses small/unstable cells; the gap
    is reported in ACQUIRED.md and never padded.

Output (atomic):
    <root>/lehd/qwi_state_panel.parquet
    <root>/lehd/ACQUIRED.md

Root resolution:
    $IMMIGRATION_CAUSAL_DATA if set, else <repo>/sources/immigration-causal/data
    resolved from this file's own location. Fails loud if the directory is absent;
    there is no fallback to $HOME or to the repo tree.

API key:
    QWI (like all of api.census.gov/data) requires a Census API key as of 2026-09-16.
    Keyless requests are redirected to .../missing_key.html. The key is read from
    $CENSUS_API_KEY, else from the CENSUS_API_KEY line of the untracked
    acquire/config.local.env. It is never printed or written to ACQUIRED.md.
    Free signup: https://api.census.gov/data/key_signup.html

Run:
    uv run --with pandas --with pyarrow --with requests python3 \
        infra/immigration-fiscal/acquire/pull_qwi_state_panel.py
"""

from __future__ import annotations

import datetime as _dt
import os
import re
import sys
import time
from pathlib import Path
from urllib.parse import urlencode

import pandas as pd
import requests

# --------------------------------------------------------------------------- spec

ENDPOINT = "https://api.census.gov/data/timeseries/qwi/se"

# Measures pulled. EarnS + EmpS are what the E-Verify analysis used; Emp/HirA/Sep
# are the superset requested so later work does not need a re-pull.
MEASURES = ["Emp", "EmpS", "EarnS", "HirA", "Sep"]

# 50 states + DC. geography.json marks state wildcard=false, limit=51, so the
# FIPS list is enumerated explicitly rather than using `for=state:*`.
STATE_FIPS = [
    "01", "02", "04", "05", "06", "08", "09", "10", "11", "12", "13", "15",
    "16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26", "27",
    "28", "29", "30", "31", "32", "33", "34", "35", "36", "37", "38", "39",
    "40", "41", "42", "44", "45", "46", "47", "48", "49", "50", "51", "53",
    "54", "55", "56",
]

# NAICS sectors: all-industry plus the eight sectors used by the E-Verify design.
INDUSTRIES = ["00", "11", "23", "31-33", "44-45", "56", "62", "72", "81"]

# E1 less-than-HS, E2 HS, E3 some college, E4 BA+.
EDUCATION = ["E1", "E2", "E3", "E4"]

SEX = "0"  # all sexes

YEAR_START, YEAR_END = 2003, 2023
TIME_PREDICATE = f"from {YEAR_START}-Q1 to {YEAR_END}-Q4"
N_QUARTERS = (YEAR_END - YEAR_START + 1) * 4

SLEEP_SECONDS = 1.0
TIMEOUT_SECONDS = 300

# --------------------------------------------------------------------------- console


def _header(s: str) -> None:
    print(f"\n[{s}]", flush=True)


def _ok(msg: str) -> None:
    print(f"  OK {msg}", flush=True)


def _info(msg: str) -> None:
    print(f"  .  {msg}", flush=True)


def _fail(msg: str) -> None:
    print(f"  XX {msg}", flush=True)


def _progress(i: int, n: int, label: str = "") -> None:
    pct = i * 100 // n
    print(f"  [{i}/{n}] {pct}%{f' - {label}' if label else ''}", flush=True)


class PullError(RuntimeError):
    """Any condition that must abort the run without writing a parquet."""


# --------------------------------------------------------------------------- setup


def resolve_root() -> Path:
    """Output root. Env override wins; otherwise resolve from this file's location.

    Fails loud rather than inventing a writable directory: a silent fallback is how
    the original pull's output went missing when the SSD tree moved.
    """
    override = os.environ.get("IMMIGRATION_CAUSAL_DATA", "").strip()
    if override:
        root = Path(override).expanduser()
        origin = "$IMMIGRATION_CAUSAL_DATA"
    else:
        repo_root = Path(__file__).resolve().parents[3]
        root = repo_root / "sources" / "immigration-causal" / "data"
        origin = f"script location ({repo_root})"

    if not root.is_dir():
        raise PullError(
            f"data root does not exist: {root}\n"
            f"       (from {origin})\n"
            f"       The repo `sources` symlink must point at a mounted data volume.\n"
            f"       Refusing to fall back to $HOME or to the repo tree."
        )
    return root.resolve()


def _read_key_from_config() -> str | None:
    """Read CENSUS_API_KEY out of the untracked acquire/config.local.env, if present.

    Parsed by hand instead of sourcing the file, because that file resolves other
    variables against $REPO_ROOT and mis-sourcing it yields bogus paths.
    """
    cfg = Path(__file__).resolve().parent / "config.local.env"
    if not cfg.is_file():
        return None
    pattern = re.compile(r'^\s*(?:export\s+)?CENSUS_API_KEY\s*=\s*"?([^"\s#]+)"?')
    for line in cfg.read_text(errors="replace").splitlines():
        m = pattern.match(line)
        if m:
            return m.group(1)
    return None


def resolve_key() -> str:
    key = os.environ.get("CENSUS_API_KEY", "").strip() or (_read_key_from_config() or "").strip()
    if not key:
        raise PullError(
            "no Census API key.\n"
            "       As of 2026-09-16 every api.census.gov/data request without a key is\n"
            "       redirected to https://api.census.gov/data/missing_key.html, so a\n"
            "       keyless pull returns HTML, not data.\n"
            "       Set $CENSUS_API_KEY or add a CENSUS_API_KEY line to\n"
            f"       {Path(__file__).resolve().parent / 'config.local.env'}\n"
            "       Free signup: https://api.census.gov/data/key_signup.html\n"
            "       NOTE: $DATA_GOV_API_KEY is NOT accepted (returns invalid_key.html)."
        )
    return key


# --------------------------------------------------------------------------- fetch


def build_url(industry: str, education: str, key: str) -> str:
    params = [
        ("get", ",".join(MEASURES)),
        ("for", "state:" + ",".join(STATE_FIPS)),
        ("time", TIME_PREDICATE),
        ("industry", industry),
        ("education", education),
        ("sex", SEX),
        ("key", key),
    ]
    return f"{ENDPOINT}?{urlencode(params)}"


def _redact(url: str) -> str:
    return re.sub(r"(key=)[^&]*", r"\1REDACTED", url)


def fetch_batch(session: requests.Session, industry: str, education: str, key: str) -> pd.DataFrame:
    """One API call. Raises PullError on any non-200, non-JSON, or empty response."""
    url = build_url(industry, education, key)
    safe = _redact(url)

    resp = session.get(url, timeout=TIMEOUT_SECONDS)

    if resp.status_code != 200:
        raise PullError(f"HTTP {resp.status_code} for {safe}\n       body: {resp.text[:400]}")

    # A keyless or bad-key request still returns 200 after redirecting to an HTML
    # error page, so status code alone does not prove success.
    final = resp.url or ""
    if "missing_key" in final or "invalid_key" in final or resp.text.lstrip()[:1] == "<":
        raise PullError(
            f"non-JSON response for {safe}\n"
            f"       redirected to: {_redact(final)}\n"
            f"       body: {resp.text[:200]!r}"
        )

    try:
        payload = resp.json()
    except ValueError as exc:
        raise PullError(f"unparseable JSON for {safe}\n       {exc}\n       body: {resp.text[:400]}")

    if not isinstance(payload, list) or len(payload) < 2:
        raise PullError(f"batch returned zero data rows for {safe}\n       payload: {str(payload)[:300]}")

    header, rows = payload[0], payload[1:]
    if not rows:
        raise PullError(f"batch returned zero data rows for {safe}")

    # Column order is taken from the response header, never assumed.
    return pd.DataFrame(rows, columns=header)


# --------------------------------------------------------------------------- shape


def tidy(df: pd.DataFrame) -> pd.DataFrame:
    """Normalise dimension columns and cast measures to numeric."""
    # The API returns the geography column as `state`; `time` arrives as YYYY-Qn
    # and year/quarter may or may not be echoed separately.
    if "time" in df.columns:
        parsed = df["time"].astype(str).str.extract(r"^(\d{4})-Q([1-4])$")
        df["year"] = pd.to_numeric(parsed[0], errors="coerce").astype("Int64")
        df["quarter"] = pd.to_numeric(parsed[1], errors="coerce").astype("Int64")
    else:
        for col in ("year", "quarter"):
            if col not in df.columns:
                raise PullError(f"response has neither `time` nor `{col}`; columns={list(df.columns)}")
            df[col] = pd.to_numeric(df[col], errors="coerce").astype("Int64")

    if "state" not in df.columns:
        raise PullError(f"response has no `state` column; columns={list(df.columns)}")

    for col in ("state", "industry", "education", "sex"):
        if col in df.columns:
            df[col] = df[col].astype("string")

    for measure in MEASURES:
        if measure not in df.columns:
            raise PullError(f"response missing measure `{measure}`; columns={list(df.columns)}")
        df[measure] = pd.to_numeric(df[measure], errors="coerce").astype("Float64")

    lead = [c for c in ("state", "year", "quarter", "industry", "education", "sex") if c in df.columns]
    rest = [c for c in df.columns if c not in lead and c not in MEASURES]
    return df[lead + MEASURES + rest]


# --------------------------------------------------------------------------- report


def write_acquired_md(path: Path, df: pd.DataFrame, n_calls: int, wall: float, cmdline: str) -> None:
    per_state = df.groupby("state", observed=True).size()
    full_grid = len(STATE_FIPS) * N_QUARTERS * len(INDUSTRIES) * len(EDUCATION)
    gap = full_grid - len(df)
    nulls = df[MEASURES].isna().sum()

    lines = [
        "# LEHD QWI state panel - ACQUIRED",
        "",
        f"- **Pulled (UTC):** {_dt.datetime.now(_dt.timezone.utc).isoformat(timespec='seconds')}",
        f"- **Endpoint:** {ENDPOINT}",
        f"- **Command:** `{cmdline}`",
        f"- **Wall time:** {wall:.1f} s",
        f"- **API calls:** {n_calls}",
        "",
        "## Dimensions",
        "",
        f"- **Period:** {YEAR_START}-Q1 to {YEAR_END}-Q4 ({N_QUARTERS} quarters), `time` predicate `{TIME_PREDICATE}`",
        f"- **Geography:** {len(STATE_FIPS)} state FIPS (50 states + DC), enumerated (QWI disallows `state:*`)",
        f"- **Industry:** {len(INDUSTRIES)} NAICS sectors - {', '.join(INDUSTRIES)}",
        f"- **Education:** {len(EDUCATION)} groups - {', '.join(EDUCATION)} (E1 <HS, E2 HS, E3 some college, E4 BA+)",
        f"- **Sex:** {SEX} (all)",
        f"- **Measures:** {', '.join(MEASURES)}",
        "- **Format:** long; one row per state x year x quarter x industry x education",
        "",
        "## Batching",
        "",
        f"One call per (industry x education) pair = {len(INDUSTRIES)} x {len(EDUCATION)} = "
        f"{len(INDUSTRIES) * len(EDUCATION)} calls, each covering all {len(STATE_FIPS)} states and all "
        f"{N_QUARTERS} quarters. {SLEEP_SECONDS:.0f} s sleep between calls.",
        "",
        "## Counts",
        "",
        f"- **Rows:** {len(df):,}",
        f"- **Full grid:** {full_grid:,} ({len(STATE_FIPS)} x {N_QUARTERS} x {len(INDUSTRIES)} x {len(EDUCATION)})",
        f"- **Gap (suppressed / not published):** {gap:,} ({gap / full_grid:.2%}) - reported, not padded",
        f"- **Distinct states:** {df['state'].nunique()}",
        f"- **Distinct industries:** {df['industry'].nunique()}",
        f"- **Distinct education groups:** {df['education'].nunique()}",
        f"- **Distinct year-quarter pairs:** {df[['year', 'quarter']].drop_duplicates().shape[0]}",
        f"- **Rows per state:** min {per_state.min():,} ({per_state.idxmin()}), "
        f"max {per_state.max():,} ({per_state.idxmax()})",
        "",
        "## Null counts per measure",
        "",
        "| Measure | Nulls | Share |",
        "|---|---:|---:|",
    ]
    for measure in MEASURES:
        lines.append(f"| {measure} | {int(nulls[measure]):,} | {nulls[measure] / len(df):.2%} |")
    lines += [
        "",
        "## Notes",
        "",
        "- QWI `se` has **no nativity or citizenship variable**. `EarnS` is average monthly",
        "  earnings for stable full-quarter employment, not native-born hourly wages.",
        "- Nulls are QWI disclosure suppression, not pull failures. Any non-200 response or",
        "  empty batch aborts the run before a parquet is written.",
        "",
    ]
    path.write_text("\n".join(lines), encoding="utf-8")


# --------------------------------------------------------------------------- main


def main() -> int:
    cmdline = " ".join([Path(sys.argv[0]).name] + sys.argv[1:])
    probe = "--probe" in sys.argv[1:]

    _header("setup")
    root = resolve_root()
    _ok(f"data root: {root}")
    key = resolve_key()
    _ok("Census API key loaded (not logged)")

    out_dir = root / "lehd"
    out_dir.mkdir(parents=True, exist_ok=True)
    parquet_path = out_dir / "qwi_state_panel.parquet"
    part_path = out_dir / "qwi_state_panel.parquet.part"
    _ok(f"output: {parquet_path}")

    pairs = [(ind, edu) for ind in INDUSTRIES for edu in EDUCATION]
    if probe:
        pairs = pairs[:1]
        _info("--probe: single batch only, nothing written")

    _header(f"pull ({len(pairs)} calls)")
    started = time.monotonic()
    frames: list[pd.DataFrame] = []
    with requests.Session() as session:
        for i, (industry, education) in enumerate(pairs, start=1):
            batch = fetch_batch(session, industry, education, key)
            frames.append(batch)
            _progress(i, len(pairs), f"industry={industry} education={education} rows={len(batch):,}")
            if i < len(pairs):
                time.sleep(SLEEP_SECONDS)
    wall = time.monotonic() - started
    _ok(f"{len(pairs)} calls in {wall:.1f} s")

    if probe:
        _ok(f"probe returned {len(frames[0]):,} rows; columns={list(frames[0].columns)}")
        return 0

    _header("shape")
    df = tidy(pd.concat(frames, ignore_index=True))
    df = df.sort_values(["state", "year", "quarter", "industry", "education"]).reset_index(drop=True)
    _ok(f"{len(df):,} rows x {len(df.columns)} columns")

    _header("write")
    df.to_parquet(part_path, index=False)
    os.replace(part_path, parquet_path)
    _ok(f"{parquet_path} ({parquet_path.stat().st_size / 1e6:.1f} MB)")

    write_acquired_md(out_dir / "ACQUIRED.md", df, len(pairs), wall, cmdline)
    _ok(f"{out_dir / 'ACQUIRED.md'}")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except PullError as exc:
        _fail(str(exc))
        sys.exit(1)
