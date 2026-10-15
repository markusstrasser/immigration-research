"""Check living prose citations against live_case.json; exit 1 for stale citations.

    OPENBLAS_NUM_THREADS=1 uv run --no-project python3 \
        infra/immigration-fiscal/number_drift_audit_2026_09_29/citation_freshness.py --out /tmp/freshness

Controls and adoption gates run before scanning or writing. With no --out, write
nothing. Reuse memo_sweep's document scope, record masks, sentence and table
helpers, and historical labels. Date-bearing main-case paths and summary.json
version selectors also identify a vintage. This is a prose check, not an oracle
for whether a source supports its claim or an automatic replacement tool.

Native-First: grep locates keys but cannot distinguish records from current prose;
reuse the existing Python sweep instead of introducing a second Markdown parser.
"""
from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from datetime import date
from functools import lru_cache
from pathlib import Path

sys.dont_write_bytecode = True
import memo_sweep as M  # noqa: E402

ROOT = M.ROOT
FISCAL = Path("infra/immigration-fiscal")
MANIFEST = FISCAL / "live_case.json"
KEY = re.compile(r"(?:oct|sept)\d{2}")
# Both Markdown targets and inline filenames, including a trailing folder slash.
REFERENCE = re.compile(r"(?<![A-Za-z0-9_.-])[A-Za-z0-9_.-]+(?:/[A-Za-z0-9_.-]+)*/?")
FIELDS = ["doc", "line", "key", "reference", "sentence", "replacement"]


def mask_references(text):
    return REFERENCE.sub(lambda m: " " if "/" in m[0] or re.search(r"\.[A-Za-z0-9]", m[0]) else m[0], text)


def unread(text):
    """Reuse record masks while retaining citation-bearing evidence tags.

    Lowercase only their labels for unread's NOTE_OPEN, then restore surviving
    labels. Brackets remain intact, so enclosing historical notes still mask
    nested evidence tags and positions stay unchanged.
    """
    tags = list(re.finditer(r"\[(SOURCE|DATA|CALCULATION|DERIVATION):", text))
    protected = text
    for m in reversed(tags):
        protected = protected[:m.start(1)] + m[1].lower() + protected[m.end(1):]
    clean = M.unread(protected)
    for m in reversed(tags):
        if clean[m.start(1):m.end(1)].strip():
            clean = clean[:m.start(1)] + m[1] + clean[m.end(1):]
    return clean


def blocked(message):
    raise ValueError(f"[BLOCKED] {message}")


def literal_consts(text):
    """String-literal `const` declarators by name, comma lists included (`const A="x", B="y";`).

    Single-line statements only; a declarator whose initializer is not one string literal is skipped.
    """
    found = {}
    for line in text.splitlines():
        statement = re.match(r"const\s+(.+);\s*$", line)
        if not statement:
            continue
        body, parts, depth, quote, start = statement[1], [], 0, None, 0
        for i, ch in enumerate(body):
            if quote:
                if ch == quote and body[i - 1] != "\\":
                    quote = None
            elif ch in "\"'`":
                quote = ch
            elif ch in "([{":
                depth += 1
            elif ch in ")]}":
                depth -= 1
            elif ch == "," and depth == 0:
                parts.append(body[start:i])
                start = i + 1
        parts.append(body[start:])
        for part in parts:
            d = re.fullmatch(r"\s*([A-Za-z_$][\w$]*)\s*=\s*([\"'])([^\"']*)\2\s*", part)
            if d:
                found.setdefault(d[1], []).append(d[3])
    return found


def declaration(text, name):
    hits = literal_consts(text).get(name, [])
    if len(hits) != 1:
        blocked(f"package must declare one literal {name}, got {len(hits)}")
    return hits[0]


def key_date(key, year):
    if not KEY.fullmatch(key):
        blocked(f"invalid case key {key!r}")
    return date(year, 10 if key.startswith("oct") else 9, int(key[-2:]))


def load_live(root=ROOT):
    live = json.loads((root / MANIFEST).read_text())
    if set(live) != {"key", "lane", "adopted", "decision", "superseded"}:
        blocked("live_case.json has missing or extra fields")
    adopted = date.fromisoformat(live["adopted"])
    if key_date(live["key"], adopted.year) != adopted:
        blocked("live key and adoption date disagree")
    if live["lane"] != "main_case_" + adopted.strftime("%Y_%m_%d"):
        blocked("live lane and adoption date disagree")
    old = [key_date(k, adopted.year) for k in live["superseded"]]
    if old != sorted(set(old), reverse=True) or any(d >= adopted for d in old):
        blocked("superseded keys must be unique, newest first, and earlier than live")
    observed = set()
    for p in (root / FISCAL).glob("*/derived/*"):
        if p.is_dir() and KEY.fullmatch(p.name):
            observed.add(p.name)
        elif p.suffix in {".csv", ".json"}:
            observed.update(re.findall(r"_((?:oct|sept)\d{2})(?=\.|_[A-Za-z]+\.)", p.name))
    missing = sorted(k for k in observed if key_date(k, adopted.year) < adopted and k not in live["superseded"])
    if missing:
        blocked(f"consumer output keys missing from superseded: {missing}")
    package = root / FISCAL / live["lane"] / "package.cjs"
    text = package.read_text()
    for name, value in {"STATUS": "adopted", "CASE_KEY": live["key"], "LANE": live["lane"],
                        "ADOPTED": live["adopted"], "DECISION": live["decision"]}.items():
        if declaration(text, name) != value:
            blocked(f"{package.name} {name} disagrees with live_case.json")
    if not (root / live["decision"]).is_file():
        blocked(f"missing live decision {live['decision']}")
    for name in ("corrections.json", "corrections_cash.json"):
        meta = json.loads((package.parent / "derived" / name).read_text())["meta"]
        for field, value in {"adopted": live["adopted"], "decision": live["decision"],
                             "source": live["lane"] + "/package.cjs"}.items():
            if meta.get(field) != value:
                blocked(f"{name} meta.{field} disagrees with live_case.json")
    # Inspect all adopted package switches: checking only the named lane would
    # still pass when a later package is adopted and the manifest is forgotten.
    for other in sorted((root / FISCAL).glob("main_case_*/package.cjs")):
        source = other.read_text()
        if literal_consts(source).get("STATUS") == ["adopted"]:
            if date.fromisoformat(declaration(source, "ADOPTED")) > adopted:
                blocked(f"newer adopted package {other.parent.name}: update live_case.json")
    return live


def versions(root):
    """Version-to-key mapping from decision filenames, never a duplicated roster."""
    result = {}
    for p in (root / "decisions").glob("*-main-case-v*.md"):
        m = re.fullmatch(r"(\d{4}-\d{2}-\d{2})-main-case-(v\d+)\.md", p.name)
        if m:
            d = date.fromisoformat(m[1])
            result[m[2]] = ("oct" if d.month == 10 else "sept") + f"{d.day:02d}"
    return result


@lru_cache(maxsize=8)
def key_patterns(adopted, keys):
    result = []
    for key in keys:
        d = key_date(key, date.fromisoformat(adopted).year)
        stamp = d.isoformat().replace("-", "_")
        result.append((key, re.compile(rf"_{key}(?=\.|_[A-Za-z]+\.|$)"),
                       re.compile(rf"main_case_(?:(?:schools_full|long_run)_)?{stamp}(?:/|$)")))
    return result


def reference_key(reference, live):
    if "main_case_" not in reference and not KEY.search(reference):
        return None
    parts = reference.rstrip("/").split("/")
    if len(parts) > 1 and all(KEY.fullmatch(p) for p in parts) and not reference.endswith("/"):
        return None  # prose enumerating joins, such as oct05/oct07, is not a source path
    for key, filename, lane in key_patterns(live["adopted"], (live["key"], *live["superseded"])):
        if key in parts or filename.search(parts[-1]):
            return key
        if lane.search(reference):
            return key
    return None


def replacement(reference, key, live, root):
    proposed = re.sub(rf"(?<![A-Za-z0-9]){key}(?![A-Za-z0-9])", live["key"], reference)
    proposed = re.sub(r"main_case_(?:(?:schools_full|long_run)_)?\d{4}_\d{2}_\d{2}(?=/|$)", live["lane"], proposed)
    if proposed == reference:
        return ""
    candidates = [root / proposed, root / "research" / proposed, root / FISCAL / proposed]
    if any(p.exists() for p in candidates):
        return proposed
    if "/" not in proposed:
        matches = sorted((root / FISCAL).glob(f"*/derived/{proposed}"))
        if len(matches) == 1:
            return matches[0].relative_to(root).as_posix()
    return ""


def scan_text(path, text, live, version_keys=None, root=ROOT):
    rows = []
    clean = unread(text)
    raw_lines, lines = text.split("\n"), clean.split("\n")
    tab = M.tables(raw_lines)
    old = set(live["superseded"])
    for i, line in enumerate(lines):
        if path == "research/immigration-INDEX.md" and i in tab:
            if re.match(r"\|\s*Case\s*\|", tab[i][0], re.I):
                continue
        a, b = M.RC._block(lines, i)
        para = " ".join(lines[a:b + 1])
        off = len(" ".join(lines[a:i])) + (1 if i > a else 0)
        hits = [(m.start(), m.end(), reference_key(m[0], live), m[0])
                for m in REFERENCE.finditer(line) if "/" in m[0] or "." in m[0]]
        if "summary.json" in para:
            # A selector such as `summary.json` key `v6` carries a vintage even
            # when the filename is unqualified. Remove selectors before labels.
            hits += [(m.start(), m.end(), (version_keys or {}).get(m[0]),
                      "summary.json key " + m[0]) for m in re.finditer(r"\bv\d+\b", line)
                     if "summary.json" in M.Q.sentence(para, off + m.start(), off + m.end())]
        for s, e, key, ref in hits:
            if key not in old:
                continue
            sentence = M.Q.sentence(para, off + s, off + e)
            context = mask_references(M.clause(para, off + s, off + e))
            context = re.sub(r"\bv\d+\b", " ", context) if ref.startswith("summary.json key ") else context
            # VINTAGE_LABEL predates v7 and lacks October 7; derive explicit
            # dated-case labels from the manifest without modifying that sweep.
            d = key_date(key, date.fromisoformat(live["adopted"]).year)
            dated = re.search(rf"\b(?:{d:%B}|{d:%b}\.?) {d.day}\b", context, re.I)
            earlier = M.VINTAGE_LABEL.search(context) or dated
            if i in tab:
                head, caption = tab[i]
                first = line.split("|")[1] if "|" in line else ""
                earlier = earlier or M.VINTAGE_LABEL.search(mask_references(first + " " + head + " " + caption))
            before = mask_references(para[:off + s]).rstrip(" `(")
            # Reuse the sweep's current-marker definition at word boundaries,
            # allowing prose between the marker and the reference.
            current = M.ADJ_CURRENT.search(before) or any(
                M.ADJ_CURRENT.search(context[:m.end()]) for m in re.finditer(r"\b\w+\b", context))
            if earlier and not current:
                continue
            rows.append(dict(doc=path, line=i + 1, key=key, reference=ref,
                             sentence=re.sub(r"\s+", " ", sentence).strip(),
                             replacement=replacement(ref, key, live, root)))
    return rows


def controls(live):
    old, current = live["superseded"][0], live["key"]
    citation = f"rekey_summary_{old}.csv"
    d = key_date(old, date.fromisoformat(live["adopted"]).year)
    fixtures = [
        (f"The current estimate cites `{citation}`.", 1),
        (f"## Revisions\n\nThe estimate cites `{citation}`.", 0),
        (f"[Superseded: the estimate cites `{citation}`.]", 0),
        (f"The {d:%B} {d.day} case's estimate cites `{citation}`.", 0),
        (f"The current estimate cites `rekey_summary_{current}.csv`.", 0),
        (f"```\n{citation}\n```\n<!-- {citation} -->", 0),
        *[(f"The current estimate uses [{tag}: {citation}].", 1)
          for tag in ("DATA", "SOURCE", "CALCULATION", "DERIVATION")],
        (f"The {d:%B} {d.day} source was replaced; the current estimate uses `{citation}`.", 1),
    ]
    for text, expected in fixtures:
        actual = len(scan_text("synthetic.md", text, live))
        if actual != expected:
            blocked(f"citation control expected {expected}, got {actual}: {text!r}")
    return len(fixtures)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--out", type=Path, help="write CSV here; default writes nothing")
    args = ap.parse_args(argv)
    live = load_live()
    count = controls(live)
    docs, _skipped = M.memos(None)
    docs.append(("CLAUDE.md", (ROOT / "CLAUDE.md").read_text()))
    version_keys = versions(ROOT)
    rows = [row for path, text in docs for row in scan_text(path, text, live, version_keys)]
    for row in rows:
        print(f"STALE-CITATION {row['doc']}:{row['line']} {row['key']} {row['reference']} — {row['sentence'][:160]}")
    print(f"{len(rows)} stale citations; {len(docs)} living docs; {count}/{count} controls pass; live {live['key']}")
    if args.out is not None:
        args.out.mkdir(parents=True, exist_ok=True)
        with (args.out / "citation_freshness.csv").open("w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=FIELDS, lineterminator="\n")
            writer.writeheader()
            writer.writerows(rows)
    return int(bool(rows))


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (ValueError, KeyError, OSError) as error:
        print(f"[BLOCKED] citation freshness: {error}", file=sys.stderr)
        sys.exit(2)
