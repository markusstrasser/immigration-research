"""Cached Census API access for the ACS late-arrival tabulation. The key never reaches stdout, logs
or cached file names.

Copied from crime_selection_cohorts_2026_09_23/census_api.py (not imported across lanes), with the
cache pointed at this lane's _cache/acs/, six tries with 20 s backoff for today's flaky DNS, and
content validation: a response counts only if it parses as a JSON list whose first row is a header.
get(path, cache_name) returns parsed JSON and stores the raw response.
"""
import json
import os
import re
import time
import urllib.error
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
CACHE = HERE / "_cache" / "acs"
BASE = "https://api.census.gov/data"


def _key() -> str:
    k = os.environ.get("CENSUS_API_KEY", "")
    if not k:
        env = HERE.parent / "acquire" / "config.local.env"
        m = re.search(r"CENSUS_API_KEY=\"?([A-Za-z0-9]+)", env.read_text())
        k = m.group(1) if m else ""
    if not k:
        raise SystemExit("[BLOCKED] CENSUS_API_KEY missing")
    return k


def redact(s: str) -> str:
    return re.sub(r"key=[A-Za-z0-9]+", "key=<KEY>", s)


def _valid(data) -> bool:
    return isinstance(data, list) and (
        len(data) == 0 or (isinstance(data[0], list) and all(isinstance(c, str) for c in data[0]))
    )


def get(path: str, cache_name: str, retries: int = 6, sleep: int = 20, use_key: bool = True):
    """path is everything after /data/, e.g. '2019/acs/acs1/pums?get=...'. Cached by cache_name.

    An empty body (HTTP 204) is a valid 'no matching records' answer and is cached as [].
    """
    out = CACHE / cache_name
    if out.exists():
        return json.loads(out.read_text())
    out.parent.mkdir(parents=True, exist_ok=True)
    url = f"{BASE}/{path}"
    if use_key:
        sep = "&" if "?" in path else "?"
        url = f"{url}{sep}key={_key()}"
    last = None
    for attempt in range(retries):
        try:
            with urllib.request.urlopen(url, timeout=600) as r:
                body = r.read()
            data = json.loads(body) if body.strip() else []
            # data tables must be a list with a header row; metadata endpoints return a JSON object
            if not (_valid(data) or isinstance(data, dict)):
                raise ValueError(f"unexpected content: {redact(body[:200].decode('utf-8', 'replace'))}")
            tmp = out.with_suffix(out.suffix + ".tmp")
            tmp.write_bytes(body if body.strip() else b"[]")
            tmp.replace(out)
            return data
        except urllib.error.HTTPError as e:
            msg = e.read()[:300].decode("utf-8", "replace")
            if e.code == 204:
                out.write_bytes(b"[]")
                return []
            last = f"HTTP {e.code}: {redact(msg)}"
            if e.code in (400, 404):
                break
        except Exception as e:  # noqa: BLE001 - network errors carry the URL; redact and retry
            last = redact(f"{type(e).__name__}: {e}")
        print(f"  retry {attempt + 1}/{retries} {cache_name}: {last}", flush=True)
        time.sleep(sleep)
    raise RuntimeError(f"[FAILED] {redact(path)} -> {last}")
