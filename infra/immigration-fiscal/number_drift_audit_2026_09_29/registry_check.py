"""Resolve every record of the evidence map's quantity registry, and test the document bindings: numbers in the
INDEX and FAQ that should equal a record.

    uv run --no-project --offline python3 infra/immigration-fiscal/number_drift_audit_2026_09_29/registry_check.py

The registry (`overview_2026_09_28/quantity_registry.csv`) and its reader, `quantities.py`, sit beside the
evidence map's build, which tests the map's own bindings (`quantity_bindings.csv` there) on every build. This
script covers what the build does not read: `doc_bindings.csv`, one row per number in a research document, keyed
like source_map.csv (file, anchor, ordinal).

A binding's test:
    value   the number at the site equals the record's view under the display rounding
    lint    the sentence holding the number satisfies the record's must_name and forbid
"now" runs the test on the document as it stands, "after" on the binding's suggested fix. Verdicts:
    OK: fails now, passes after   a flagged number, still wrong in the document
    FIXED: passes now             a flagged number the document has since corrected
    OK: passes now                a MATCH number, still right
    WRONG: ...                    a MATCH number that now fails, or a fix that fails its own test
    GONE / CHANGED                the line, or the number on it, is no longer there (a warning: the text moved)
A document line is found by its anchor; the sentence around a number is read across the line's paragraph.

Writes `derived/registry_values.csv` (each record resolved and rendered) and `derived/binding_tests.csv`. Exits 1
when a record fails to resolve or a verdict is WRONG. `--out DIR` writes there instead of derived/.
"""

import argparse
import csv
import re
import sys
from pathlib import Path

import audit_numbers as A
from audit_numbers import Q
from quantities import load_registry, record_value, render, rule_for, sentence, view_value

HERE = A.HERE
ROOT = A.ROOT
BINDINGS = HERE / "doc_bindings.csv"
FLAGGED = ("STALE", "MISMATCH", "CONTEXT-SHIFT")


# ---------------------------------------------------------------- sites

def _toks(text, clean=None):
    return [dict(raw=raw.strip(), lo=lo, hi=hi, ordinal=k, sentence=sentence(text, s, e))
            for s, e, raw, lo, hi, _suf, k in A.tokens(text, clean)]


def _block(lines, i):
    """(first, last) line of the paragraph or list item that holds line i."""
    def opens(line):
        return not line.strip() or re.match(r"\s*(?:[-*] |#|\||\d+\. )", line)
    a = i
    while a > 0 and not opens(lines[a]) and lines[a - 1].strip():
        a -= 1
    b = i
    while b + 1 < len(lines) and lines[b + 1].strip() and not opens(lines[b + 1]):
        b += 1
    return a, b


def lookup(file, locator):
    """Tokens of the document line an anchor picks, each with the sentence around it read across the line's
    paragraph; None when the anchor no longer picks one line."""
    text = (ROOT / file).read_text()
    lines, clean = text.split("\n"), A.mask(text).split("\n")
    hits = [i for i, l in enumerate(lines) if A.anchored(locator, l)]
    if len(hits) != 1:
        return None
    i = hits[0]
    a, b = _block(lines, i)
    para = " ".join(lines[a:b + 1])
    off = len(" ".join(lines[a:i])) + (1 if i > a else 0)
    return [dict(raw=raw.strip(), lo=lo, hi=hi, ordinal=k, sentence=sentence(para, off + s, off + e))
            for s, e, raw, lo, hi, _suf, k in A.tokens(lines[i], clean[i])]


# ---------------------------------------------------------------- tests

lint = Q.lint


def value_ok(target, tok, rule):
    return A.matches(target, dict(lo=tok["lo"], hi=tok["hi"]), rule)


def grade(b, recs, moved):
    rec = recs[b["quantity_id"]]
    v = record_value(b["quantity_id"], recs)
    target, rule = view_value(rec, v, b["view"]), rule_for(rec, b["view"], b["rule"])
    expected = render(rec, v, b["view"])
    row = dict(b, rule=rule, expected=expected, found="", now_value="", now_lint="", after_value="",
               after_lint="", verdict="")
    if b["test"] == "none":
        row["verdict"] = "not on the page"
        return row
    toks = lookup(b["file"], b["locator"])
    tok = None
    if toks is not None:
        # the site's position now, when numbers were inserted or deleted around it (audit_numbers.pair_tokens)
        o = moved.get((b["file"], b["locator"], b["ordinal"]), b["ordinal"])
        same = [t for t in toks if t["raw"] == b["shown"]]
        tok = next((t for t in same if t["ordinal"] == o), None) or (same[0] if same else None)
    if tok is None:
        row["found"] = "GONE" if toks is None else "CHANGED"
        row["verdict"] = row["found"]
        return row
    row["found"] = tok["raw"]
    tests = b["test"].split("+")
    now = []
    if "value" in tests:
        ok = value_ok(target, tok, rule)
        row["now_value"] = "PASS" if ok else "FAIL"
        now.append(ok)
    if "lint" in tests:
        errs = lint(tok["sentence"], rec)
        row["now_lint"] = "PASS" if not errs else "FAIL: " + "; ".join(errs)
        now.append(not errs)
    after = []
    ok = any(value_ok(target, t, rule) for t in _toks(b["fix"]))
    row["after_value"] = "PASS" if ok else "FAIL"
    after.append(ok)
    errs = lint(b["fix"], rec)
    row["after_lint"] = "PASS" if not errs else "FAIL: " + "; ".join(errs)
    after.append(not errs)
    if not all(after):
        row["verdict"] = "WRONG: the suggested fix fails"
    elif b["audit_status"] in FLAGGED:
        row["verdict"] = "FIXED: passes now" if all(now) else "OK: fails now, passes after"
    else:
        row["verdict"] = "OK: passes now" if all(now) else "WRONG: fails now"
    return row


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--out", type=Path, default=HERE / "derived")
    args = ap.parse_args()
    recs = load_registry()
    values = []
    for rid, rec in recs.items():
        v = record_value(rid, recs)
        views = ["mid", "range_unit"] + (["pair"] if rec["shape"] == "ends" else [])
        values.append(dict(id=rid, status=rec["status"], shape=rec["shape"], unit=rec["unit"], value=A._fmt(v),
                           **{f"view_{k}": render(rec, v, k) for k in ("mid", "range_unit", "pair") if k in views},
                           must_name=rec["must_name"], forbid=rec["forbid"]))
    moved = A.current_ordinals(ROOT / A.OVERVIEW / "groups.py")
    rows = [grade(b, recs, moved) for b in csv.DictReader(BINDINGS.open())]
    for b in rows:
        if b["quantity_id"] not in recs:
            raise SystemExit(f"[BLOCKED] binding names no record {b['quantity_id']!r}")
    args.out.mkdir(parents=True, exist_ok=True)
    cols = ["id", "status", "shape", "unit", "value", "view_mid", "view_range_unit", "view_pair", "must_name", "forbid"]
    with (args.out / "registry_values.csv").open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols, lineterminator="\n", restval="")
        w.writeheader()
        w.writerows(values)
    bcols = ["file", "line", "locator", "ordinal", "shown", "audit_status", "quantity_id", "view", "rule", "test",
             "found", "now_value", "now_lint", "expected", "fix", "after_value", "after_lint", "verdict"]
    with (args.out / "binding_tests.csv").open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=bcols, lineterminator="\n", extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)
    counts = {}
    for r in rows:
        counts[r["verdict"]] = counts.get(r["verdict"], 0) + 1
    print(f"{len(recs)} records resolved; {len(rows)} bindings: "
          + ", ".join(f"{k} {v}" for k, v in sorted(counts.items())))
    bad = [r for r in rows if r["verdict"].startswith("WRONG")]
    for r in bad:
        print(f"  ✗ {r['file']}:{r['line']} {r['shown']!r} → {r['quantity_id']}|{r['view']}: {r['verdict']} "
              f"(now {r['now_value'] or '-'} / {r['now_lint'] or '-'}; after {r['after_value']} / {r['after_lint']})")
    for r in rows:
        if r["verdict"] in ("GONE", "CHANGED"):
            print(f"  ! {r['file']}:{r['line']} {r['shown']!r}: {r['verdict']} (no longer in the text: fixed or moved "
                  f"by a rewrite)")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
