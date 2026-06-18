#!/usr/bin/env python3
"""Download a URL with optional referer warm-up (WAF / bot-blocked hosts)."""
from __future__ import annotations

import sys
from pathlib import Path

UA = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
)


def fetch(url: str, dest: Path, *, referer: str | None = None, min_bytes: int = 512) -> None:
    try:
        from playwright.sync_api import sync_playwright
    except ImportError as exc:
        raise SystemExit(
            "playwright not installed — run: uv run --with playwright python -m playwright install chromium"
        ) from exc

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(user_agent=UA, accept_downloads=True)
        page = context.new_page()
        if referer:
            page.goto(referer, wait_until="domcontentloaded", timeout=120_000)
        headers = {"Referer": referer} if referer else {}
        resp = context.request.get(url, headers=headers, timeout=300_000)
        if not resp.ok:
            browser.close()
            raise SystemExit(f"HTTP {resp.status} for {url}")
        body = resp.body()
        browser.close()
    if len(body) < min_bytes:
        raise SystemExit(f"download too small ({len(body)} bytes): {url}")
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_bytes(body)


def main() -> int:
    if len(sys.argv) not in (3, 4):
        print("usage: fetch_browser.py <url> <dest> [referer_url]", file=sys.stderr)
        return 1
    url, dest_s = sys.argv[1], Path(sys.argv[2])
    referer = sys.argv[3] if len(sys.argv) == 4 else None
    min_bytes = 10_240 if dest_s.suffix.lower() == ".zip" else 512
    fetch(url, dest_s, referer=referer, min_bytes=min_bytes)
    print(f"saved {dest_s} ({dest_s.stat().st_size} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
