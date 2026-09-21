"""Fetch every link in sources.json once and record what came back (sources_check.json).

A receipt, not a gate: publishers often refuse scripts (403) while the link works in a browser, so
the page reports the status beside each source instead of hiding the source. Re-run after editing
sources.json: `uv run --no-project python3 check_sources.py [key ...]`.
"""
from __future__ import annotations

import datetime
import json
import re
import ssl
import sys
import urllib.error
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.5 Safari/605.1.15"
SKIP_HOSTS = ("x.com", "twitter.com")  # automated fetching is blocked for these hosts


def fetch(url):
    if any(re.match(rf"^https?://(www\.)?{re.escape(host)}/", url) for host in SKIP_HOSTS):
        return dict(ok=False, status="not fetched: host blocks scripts")
    request = urllib.request.Request(url, headers={"User-Agent": AGENT, "Accept": "text/html,application/pdf,*/*;q=0.8", "Accept-Language": "en"})
    try:
        with urllib.request.urlopen(request, timeout=30, context=ssl.create_default_context()) as response:
            body = response.read(300_000)
            kind = response.headers.get("Content-Type", "")
            title = re.search(rb"<title[^>]*>(.*?)</title>", body, flags=re.I | re.S)
            return dict(ok=response.status == 200, status=response.status, final_url=response.geturl(), content_type=kind.split(";")[0],
                        title=re.sub(r"\s+", " ", title.group(1).decode("utf-8", "replace")).strip()[:160] if title else None)
    except urllib.error.HTTPError as error:
        return dict(ok=False, status=error.code)
    except (urllib.error.URLError, TimeoutError, ssl.SSLError, ConnectionError) as error:
        return dict(ok=False, status=type(error).__name__+": "+str(getattr(error, "reason", error))[:80])


def main():
    sources = json.loads((HERE/"sources.json").read_text())["sources"]
    out_path = HERE/"sources_check.json"
    checks = json.loads(out_path.read_text()) if out_path.exists() else {}
    wanted = set(sys.argv[1:])
    today = datetime.date.today().isoformat()
    todo = [s for s in sources if (s["key"] in wanted) or (not wanted and checks.get(s["key"], {}).get("url") != s["url"])]
    for i, source in enumerate(todo, 1):
        result = fetch(source["url"])
        checks[source["key"]] = dict(result, url=source["url"], date=today)
        mark = "✓" if result["ok"] else "!"
        print(f"  {mark} [{i}/{len(todo)}] {source['key']}: {result['status']} {result.get('title') or ''}"[:200], flush=True)
    live = {s["key"] for s in sources}
    checks = {key: value for key, value in sorted(checks.items()) if key in live}
    out_path.write_text(json.dumps(checks, indent=1, ensure_ascii=False)+"\n")
    answered = sum(1 for value in checks.values() if value["ok"])
    print(f"{answered} of {len(checks)} links answered; receipt in {out_path.name}")


if __name__ == "__main__":
    main()
