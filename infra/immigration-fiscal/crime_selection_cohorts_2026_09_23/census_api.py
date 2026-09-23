"""Cached Census API access for this lane. The key never reaches stdout, logs or cached file names.

get(url_without_key, cache_name) returns parsed JSON and stores the raw response in _cache/api/.
Errors are re-raised with the key redacted, because urllib puts the full URL in its messages.
"""
import json
import os
import re
import time
import urllib.error
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
CACHE = HERE / "_cache" / "api"
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


def get(path: str, cache_name: str, retries: int = 4):
    """path is everything after /data/, e.g. '2019/acs/acs1/pums?get=...'. Cached by cache_name."""
    out = CACHE / cache_name
    if out.exists():
        return json.loads(out.read_text())
    CACHE.mkdir(parents=True, exist_ok=True)
    sep = "&" if "?" in path else "?"
    url = f"{BASE}/{path}{sep}key={_key()}"
    last = None
    for attempt in range(retries):
        try:
            with urllib.request.urlopen(url, timeout=300) as r:
                body = r.read()
            if not body.strip():
                data = []
            else:
                data = json.loads(body)
            out.write_bytes(body if body.strip() else b"[]")
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
        time.sleep(3 * (attempt + 1))
    raise RuntimeError(f"[FAILED] {redact(path)} -> {last}")
