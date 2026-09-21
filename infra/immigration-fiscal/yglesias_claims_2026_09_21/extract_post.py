"""Extract byline, date, paywall status and body text from a cached Slow Boring page.

Usage: uv run --no-project python3 extract_post.py _cache/sb_<slug>.html [more.html ...]
Writes `<same name>.txt` beside each input unless one exists, and prints one summary line per
page. The body sits between `class="body markup"` and `class="post-footer"`; a paywalled post
returns only its preview, so the character count is the check on how much was read.
"""
import html
import re
import sys
from pathlib import Path

# A paywalled page has no post footer; its preview ends at the paywall block.
BODY = re.compile(r'class="body markup"[^>]*>(.*?)class="(?:post-footer|paywall)"', re.S)
BLOCK_END = re.compile(r"</(p|h[1-6]|li|blockquote|div)>|<br\s*/?>", re.I)


def first(pattern, text):
    match = re.search(pattern, text)
    return match.group(1) if match else "?"


def body_text(page):
    match = BODY.search(page)
    if not match:
        return ""
    text = re.sub(r"<[^>]*$", "", match.group(1))  # the capture stops inside the closing block's tag
    text = BLOCK_END.sub("\n", text)
    text = html.unescape(re.sub(r"<[^>]+>", "", text))
    return re.sub(r"\n\s*\n+", "\n\n", text).strip()


def main(paths):
    for path in map(Path, paths):
        page = path.read_text(errors="replace")
        text = body_text(page)
        target = path.with_suffix(".txt")
        if text and not target.exists():
            target.write_text(text + "\n")
        author = first(r'<meta name="author" content="([^"]+)"', page)
        date = first(r'"datePublished":"([0-9-]{10})', page)
        paywalled = "yes" if ('class="paywall' in page or "paywall-jump" in page) else "no"
        mark = "✓" if text else "✗"
        print(f"  {mark} {path.name}: author={author} date={date} chars={len(text):,} paywalled={paywalled}")


if __name__ == "__main__":
    main(sys.argv[1:])
