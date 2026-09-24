"""Shared fetch helpers for the vending-restaurants lane.

Every download goes through curl (Python urllib fails TLS on this machine). Content is checked by
the caller, never the HTTP status alone. The Census key is read from the environment and redacted
from anything printed or written.
"""
import json
import os
import re
import subprocess
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
CACHE = HERE / "_cache"
DERIVED = HERE / "derived"
BROWSER_UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
              "(KHTML, like Gecko) Chrome/126.0 Safari/537.36")
BLS_HEADERS = ["-H", 'sec-ch-ua: "Chromium";v="126", "Google Chrome";v="126"',
               "-H", "sec-ch-ua-mobile: ?0", "-H", 'sec-ch-ua-platform: "macOS"',
               "-H", "Accept: text/csv,application/json,*/*", "-H", "Accept-Language: en-US,en;q=0.9"]


def redact(s: str) -> str:
    return re.sub(r"key=[A-Za-z0-9]+", "key=REDACTED", s)


def curl(url: str, out: Path, extra=None, tries: int = 4) -> Path:
    """Download url to out with curl; retry; raise on failure. Never prints the key."""
    out.parent.mkdir(parents=True, exist_ok=True)
    tmp = out.with_suffix(out.suffix + ".part")
    last = ""
    for attempt in range(tries):
        cmd = ["curl", "-sS", "--fail", "-L", "--max-time", "600", "-A", BROWSER_UA, "-o", str(tmp),
               "-w", "%{http_code}"]
        cmd += (extra or []) + [url]
        r = subprocess.run(cmd, capture_output=True, text=True)
        if r.returncode == 0 and r.stdout.strip() == "204":  # Census API: query matched no rows
            out.write_text("[]")
            tmp.unlink(missing_ok=True)
            return out
        if r.returncode == 0 and tmp.exists() and tmp.stat().st_size > 0:
            tmp.replace(out)
            return out
        last = redact(r.stderr.strip()) or f"HTTP {r.stdout.strip()} with an empty body"
        time.sleep(3 * (attempt + 1))
    raise SystemExit(f"[FAILED] {redact(url)}: {last}")


def census_json(url: str, out: Path, need_cols=("ESTAB",)) -> list:
    """Census API call cached to out; checks the header and that rows parse (truncation guard)."""
    if not out.exists():
        key = os.environ.get("CENSUS_API_KEY", "")
        if not key:
            raise SystemExit("[BLOCKED] CENSUS_API_KEY not set; source acquire/config.local.env")
        curl(f"{url}&key={key}", out)
    try:
        rows = json.loads(out.read_text())
    except json.JSONDecodeError:
        out.unlink()
        raise SystemExit(f"[FAILED] truncated or non-JSON body: {redact(url)}")
    if rows == []:  # HTTP 204: no rows for this query (e.g. a ZIP chunk with no establishments)
        return []
    head = rows[0]
    missing = [c for c in need_cols if c not in head]
    if missing or any(len(r) != len(head) for r in rows):
        out.unlink()
        raise SystemExit(f"[FAILED] bad shape {missing} for {redact(url)}")
    return rows
