"""Sweep the living topic memos for numbers that quote a registry record's other value without naming its basis.

    uv run --no-project --offline python3 infra/immigration-fiscal/number_drift_audit_2026_09_29/memo_sweep.py

A record's other values are the numbers a memo may still quote after the record moved on. They have three origins:
    sibling     the record `X_lane` beside `X_priced`: the lane's own figure on the CPS's raw 40.90M
    superseded  a number that the record's `supersedes` names (the value it replaced, on another count or an
                earlier vintage)
    referenced  the current value of a record that `supersedes` names by id (case.main supersedes
                case.schools_sept26)
    registry    the registry's own value of a record in ADOPTED. The registry follows the evidence map, which moves
                to a new main case only when the operator asks. While the map lags, a record in ADOPTED takes its
                current value from the adopted lane, and its registry value becomes an earlier vintage. ADOPTED is
                empty since 2026-10-07, when the map moved to main case v6 (3834b1c8). The September 27 values
                reach the sweep through the records' `supersedes` (case.sept27, pairing.total_sept27).
    earlier     the values a record in EARLIER held on the cases v6 replaced, newest first: the October 5 case (v5)
                and the September 29 case (v4), both earlier vintages ("$390–461bn" and "$371–435bn" as the main
                case, "$490–571bn" and "$463–536bn" as the pairing, are flagged, and pass when named).
An other value that equals the record's current value at the precision it is printed with is dropped.

A memo number quotes an other value when, after the audit's masks (dates, ladder and item references, hashes):
    - it rounds to the other value at the precision the memo prints (a range end by end, a single number to any
      one part; "4,900" is also read to the hundred);
    - it does not round to the record's current value;
    - its unit agrees with the record's (bn for $bn, or a "$" or bare number in a clause saying bn or billion; % for
      %, k for $k, M for M, "$…M" for $M; a bare range or decimal counts when its clause, or its table's caption,
      carries the unit); a record in a unit unit_ok does not read stops the run;
    - its sentence names the item (ITEM, by record prefix; ITEM_EXTRA for single records).
Its kind is what the other value differs by: count (a sibling; a superseded number on the raw 40.90M), arm (a
superseded number whose `supersedes` piece names an arm) or vintage (the rest, and referenced, registry and earlier
values).
It names its basis when its clause (the sentence up to a ";"; in a table, the cell's clause, the row's first cell and
the column's header, and for all but the past-tense test the caption's clauses that speak to its column:
caption_for) carries a label of its kind:
    count     COUNT_LABEL or the sibling's must_name
    arm       ARM_LABEL
    vintage   the referenced record's must_name, COUNT_LABEL or ARM_LABEL
or, for any kind, a past-tense or dated VINTAGE_LABEL, "from" just before it, or a commit hash in its table row.
It is presented as current, whatever its label, when a current marker stands just before it ("now", "currently",
"the adopted main case, …": ADJ_CURRENT), or when it is a range in the parenthesis just after a number that reads as
the current value of a record of the same item ("$10.6bn (−$57.7bn to +$74.3bn in the lane)": the parenthesis
reads as the current figure's range).
The class is "<kind>_as_current" or "<kind>_unlabelled" (both flagged), or "<kind>_labelled" (passes; listed so a
reader can see what passed). A quote that ALLOW names (its memo, record, number and a phrase of its sentence) is a
different measure's current value that rounds to an other value by coincidence: "<kind>_allowed", which passes with
the entry's reason. An entry whose memo no longer holds its phrase and number stops the run.

Scope: research/immigration-*.md except the confidence ladder, dated audits (a name holding "audit" and a date) and
the memos in EXEMPT, each with its reason and the sentence that earns it; an exempt memo that loses that sentence
stops the run. All three go to the same skip list, memo_sweep_meta.json's memos_skipped. `--no-exempt` reads the
EXEMPT memos too, which reproduces a pass made before their exemption.
Skipped within a memo: fenced code, HTML comments, `Revisions` sections, bracketed record notes ("[2026-09-25: …]",
"[Stale …]", "[Superseded …]") and source tags ("[SOURCE: …]", "[CALCULATION: …]"). Numbers inside those are not
read. Their words still count as labels for a number just outside them.

Positive controls run first (CONTROLS), and a failed control writes nothing:
    - an unlabelled lane-count value is flagged;
    - the same value "on the CPS's 40.90M" is not;
    - a lane range in the parenthesis after the current central, and a dated value after "now", are flagged;
    - "Colombia 46.5%" and the current value match nothing;
    - a Revisions section and a bracketed note are skipped;
    - the adopted case passes as the main case, and the October 5, September 29 and September 27 cases are flagged as
      current, unlabelled or after "now", and pass when named (total and per member; the pairing and the cash set
      too).
The memos are read at a git revision (`--rev`, default HEAD), or on disk with `--worktree`. The registry is read on
disk through quantities.py; derived/memo_sweep_meta.json records whether it equals the revision's. Writes
derived/memo_sweep.csv and derived/memo_sweep_meta.json (or to `--out DIR`). Exits 0 with flags; the flags are
the output.
"""

import argparse
import csv
import hashlib
import json
import re
import subprocess
from decimal import Decimal
from pathlib import Path

import audit_numbers as A
import registry_check as RC
from audit_numbers import Q

HERE = A.HERE
ROOT = A.ROOT
MEMOS = "research"
LADDER = Q.LADDER
REGISTRY = f"{A.OVERVIEW}/quantity_registry.csv"
DATED_AUDIT = re.compile(r"audit.*\d{4}-\d{2}-\d{2}")
# records kept at their date that a name does not mark: path → (the sentence that earns the exemption, the reason)
EXEMPT = {
    "research/immigration-outside-checks-2026-09-24.md": (
        "The proposals below are kept as computed on the September 23 case.",
        "a dated audit: its header keeps its proposals as computed on the September 23 case, so its figures are "
        "that case's by declaration"),
}
# coincidences: (memo, record id, the number as printed, a phrase of its sentence) → why the number is current
ALLOW = {
    ("research/immigration-INDEX.md", "household.net_contributor_share", "24.2%",
     "counting only services a household uses itself"): (
        "the use-based share on main case v6 (convention B, 24.16% of members), which rounds like the every-line "
        "share's superseded 24.18% on the published CPS union"),
    ("research/immigration-mexican-origin-by-generation-2026-09-16.md", "gap_vs_white.per_person_common_age", "$7,000",
     "per-person health care spending by age"): (
        "a published figure, Hispanic health spending per person at 45–64 (JAMA 2021, 2016 dollars), which reads to "
        "the thousand like the common-age gap's superseded 7,049"),
    ("research/immigration-historical-backcast-2026-09-20.md", "case.per_member", "$9.4k", "same-age tax shortfall"): (
        "the second generation's same-age tax shortfall against whites with item T (age_normalizations.csv, 9,373 a "
        "person), which reads like the September 29 case's per-member low end"),
    ("research/immigration-second-generation-by-origin-2026-09-22.md", "case.per_member", "$9.4k",
     "below same-age whites"): (
        "the same tax shortfall (the second generation's, 9,373 a person with item T), which reads like the September "
        "29 case's per-member low end"),
}

# the records whose current value comes from an adopted lane the evidence map does not show yet: record id → (path,
# field, expr). Empty since 2026-10-07: the map and its registry are on main case v6 (ladder 295; 3834b1c8). The next
# time the main case moves ahead of the map, list its records here (current_values stops on a record whose registry
# row already reads the adopted file). The v6 bridge read main_case_2026_10_07's summary (`json:main_case`,
# `json:v6.per_member_usd.set`, `json:cash_set.band_bn`) and the propagation lane's oct07 pairing, with
# _pairing("oct07").
_PAIR = "csv:section=7&column=pairing_on_priced_count&item=published pairing"


def _pairing(case):
    """The pairing records' (field, expr) on one case's column of the propagation lane's real-costs totals."""
    return {
        "pairing.total": (f"l={_PAIR} (low)|{case} ;; h={_PAIR} (high)|{case}", "(l, h)"),
        "pairing.per_member_priced": (f"l={_PAIR} per group member (low)|{case} ;; "
                                      f"h={_PAIR} per group member (high)|{case}", "(l, h)"),
        "pairing.fiscal_footing": (f"f=csv:section=7&column=hispanic&item=fiscal main case (low)|{case} ;; "
                                   f"g=csv:section=7&column=custody&item=fiscal main case (high)|{case}", "(f, g)"),
    }


ADOPTED = {}


def current_values(recs):
    """({record id: current value}, {record id: the registry's value}) — the registry's values, except the records in
    ADOPTED, which take the adopted case's. Stops once the registry itself reads that file (drop the record)."""
    values = {rid: Q.record_value(rid, recs) for rid in recs}
    registry = {}
    for rid, (path, field, expr) in ADOPTED.items():
        if recs[rid]["source_path"] == path:
            raise SystemExit(f"[BLOCKED] the registry's {rid} already reads {path}: remove it from ADOPTED")
        registry[rid] = values[rid]
        values[rid] = Q.resolve(path, field, expr)
    return values, registry


# the main cases v6 replaced, newest first: record id → [(path, field, expr, label)], earlier vintages beside the
# registry's. The October 5 case (v5, ladder 281) on its lane's summary and the propagation lane's run of it
# (72f2e3bc); the September 29 case (v4, ladder 275) on its lane's summary and the propagation lane's run of it
# (911afa6). Each case's per-member figures divide by its own count: v5's the 42.75M lineage, v4's the 39.71M union.
# Keep v4 while any record's `supersedes` lacks it (case.per_member's and the pairing records' name only September 27).
EARLIER_LANE = "infra/immigration-fiscal/main_case_2026_10_05/derived/summary.json"
EARLIER_PAIRING_LANE = "infra/immigration-fiscal/sept24_propagation_2026_09_24/derived/oct05/real_costs_totals.csv"
SEPT29_LANE = "infra/immigration-fiscal/main_case_2026_09_29/derived/summary.json"
SEPT29_PAIRING_LANE = "infra/immigration-fiscal/sept24_propagation_2026_09_24/derived/sept29/real_costs_totals.csv"
_V5, _V4 = "the October 5 case (v5)", "the September 29 case (v4)"
_LINEAGE, _UNION = ", per member of the 42.75M lineage", ", per member of the 39.71M union"
EARLIER = {
    "case.main": [(EARLIER_LANE, "a=json:main_case", "(a[0], a[1])", _V5),
                  (SEPT29_LANE, "a=json:main_case", "(a[0], a[1])", _V4)],
    "case.per_member": [
        (EARLIER_LANE, "a=json:v5.per_member_usd.set", "(a[0]/1e3, a[1]/1e3)", _V5 + _LINEAGE),
        (SEPT29_LANE, "a=json:main_case ;; p=@infra/immigration-fiscal/main_case_decomposition_2026_09_29/"
         "derived/headcount.csv@csv:cut=all&group=union|row4", "(a[0]*1e6/p, a[1]*1e6/p)", _V4 + _UNION)],
    "case.cash_set": [(EARLIER_LANE, "a=json:cash_set.band_bn", "(a[0], a[1])", _V5),
                      (SEPT29_LANE, "a=json:cash_set.band_bn", "(a[0], a[1])", _V4)],
    **{rid: [(EARLIER_PAIRING_LANE, *_pairing("oct05")[rid],
              _V5 + (_LINEAGE if rid == "pairing.per_member_priced" else "")),
             (SEPT29_PAIRING_LANE, *_pairing("sept29")[rid],
              _V4 + (_UNION if rid == "pairing.per_member_priced" else ""))]
       for rid in _pairing("oct05")},
}


def earlier_values():
    """{record id: [(value, label)]}: what each record in EARLIER held on the cases the adopted one replaced, newest
    first."""
    return {rid: [(Q.resolve(path, field, expr), label) for path, field, expr, label in cases]
            for rid, cases in EARLIER.items()}


# ---------------------------------------------------------------- what a sentence must name

# the item, by record prefix: a number is read as the record's only in a sentence naming it
ITEM = {
    "case": r"\bcase\b|main estimate|headline|the account",
    "tally": r"tally|taxes paid minus benefits|survey values",
    "fill_in": r"fill-?in|imput|allocat",
    "remittance": r"remittance",
    "gg": r"general (?:government|administration)",
    # the records' constructs, not any sentence about households ("household income", "immigrant households")
    "household": r"net[- ]contribut|costliest|pays? (?:more than (?:it|they) costs?|(?:its|their) way)",
    "pm25": r"PM2\.5|fine[- ]particle|particulate|air pollution",
    "crash": r"crash",
    "victims": r"victim",
    "social": r"social|outside (?:the |public )?budgets?",
    "pairing": r"pairing|social|outside (?:the |public )?budgets?",
    "congestion": r"congestion",
    "scale": r"\bscale\b|city size|agglomeration",
    "comparators": r"white",
    "candidate_v3": r"candidate|bundle|pending|revised set|one set|\bv[34]\b",
    "candidate_v4": r"candidate|bundle|pending|revised set|one set|\bv[34]\b",
    "pension": r"pension|accru|Social Security|Part A",
    "assumptions": r"assumption|tornado",
    "gap_vs_white": r"white",
    # the 100-year family-line ledger (ladder 159), not the main case's 42.75M lineage
    "family_line": r"family[- ]line|founder|descendant|lineage (?:gap|cost|ledger)",
    # a sponsored parent's rest-of-life cost (ladder 247), not any sentence naming a parent
    "ir5": r"IR-5|parents? of (?:a )?US citizens?|sponsored parents?|parents? sponsored",
}
ITEM_EXTRA = {"pm25.deaths_priced": r"death"}

# the basis, named near the number: a count or an arm anywhere in its clause (in a table, also in the caption), a
# vintage in its clause (in a table, its cell's clause, the row's first cell or its column's header), "from" just
# before it ("rises from $28.9bn to $30.9bn" marks only the first), or a commit hash in its table row
COUNT_LABEL = re.compile(r"40\.9|\braw\b|CPS(?:'s)? (?:union|count|frame|figure|run)|survey(?:'s)? (?:raw )?count|"
                         r"in the lane|lanes?'s? (?:own )?(?:figure|count|run|span)|lanes' own|"
                         r"before the (?:data )?audit|unrestated|not restated", re.I)
ARM_LABEL = re.compile(r"(?:road budgets?|roads|lanes?) (?:held )?fixed|with (?:road budgets?|roads|lanes) fixed|"
                       r"survey values|before the (?:data )?corrections?|mixed(?:-group| offender group)|scheduled|"
                       r"\bgross\b|first[- ]year", re.I)
# the case dates and version names before the adopted case's (v6, October 7), which names the current value
VINTAGE_LABEL = re.compile(r"\bbefore\b|\buntil\b|\bwas\b|\bwere\b|earlier|previous|superseded|replaced|withdrawn|"
                           r"former|\bold\b|September \d\d?|Sept\.? \d\d?|October [1-6]\b|Oct\.? [1-6]\b|"
                           r"\d{4}-\d{2}-\d{2}|\bv[2345]\b|hand sum|summed alone|at the time", re.I)
FROM = re.compile(r"\bfrom\s+(?:about\s+)?\**$", re.I)
COMMIT = re.compile(r"\b(?=[0-9a-f]*[a-f])(?=[0-9a-f]*\d)[0-9a-f]{7}\b")
# a current marker just before the number (at most two words between) presents it as current, whatever its label
ADJ_CURRENT = re.compile(r"(?:\bnow|\bcurrently|\bat present|\btoday|\bthe current (?:figure|value|estimate|central|"
                         r"total|case)|\bthe adopted (?:figure|value|estimate|central|total|case|main case))"
                         r"(?:\s+[A-Za-z']+){0,2}[\s,:]*\**[−+-]?\$?$", re.I)

# ---------------------------------------------------------------- what a memo holds that is not read

FENCE = re.compile(r"^```.*?^```[^\n]*$", re.M | re.S)
COMMENT = re.compile(r"<!--.*?-->", re.S)
HEADING = re.compile(r"^(#{1,6})\s+(.*)$")
NOTE_OPEN = re.compile(r"\[(?=[^\]\n]{0,40}?\b\d{4}-\d{2}-\d{2}\b|(?:[Ss]tale|STALE|[Ss]uperseded|[Qq]ualified|"
                       r"[Uu]pdated?|[Cc]orrect(?:ed|ion)|[Rr]evised|[Rr]estated|[Nn]ote)\b|(?:SOURCE|DATA|CALCULATION|"
                       r"DERIVATION|INFERENCE|TRAINING-DATA|UNVERIFIED|FRAMING-SENSITIVE|MODEL|MEASUREMENT|GAP|"
                       r"material-inference)\b)")


def _blank(text, a, b):
    return text[:a] + re.sub(r"[^\n]", " ", text[a:b]) + text[b:]


def unread(text):
    """`text` with every skipped span blanked, line breaks kept, so line numbers and positions still hold."""
    for rx in (FENCE, COMMENT):
        for m in reversed(list(rx.finditer(text))):
            text = _blank(text, m.start(), m.end())
    lines, out, skip = text.split("\n"), [], None
    for line in lines:
        m = HEADING.match(line)
        if m and skip is not None and len(m.group(1)) <= skip:
            skip = None
        if m and re.match(r"Revisions\b", m.group(2).strip()):
            skip = len(m.group(1))
        out.append(re.sub(r"[^\n]", " ", line) if skip is not None else line)
    text = "\n".join(out)
    pos = 0
    while (m := NOTE_OPEN.search(text, pos)) is not None:
        depth, i = 0, m.start()
        while i < len(text):
            depth += {"[": 1, "]": -1}.get(text[i], 0)
            if depth == 0:
                break
            if text[i] == "\n" and text[i + 1:i + 2] == "\n":
                break  # a note ends with its paragraph
            i += 1
        text = _blank(text, m.start(), i + 1)
        pos = i + 1
    return text


# ---------------------------------------------------------------- other values

def _written(lo, hi):
    """A (min, max) pair in the order a range is written: magnitudes ascending when both ends are below zero."""
    return (hi, lo) if hi < 0 else (lo, hi)


def _parts(v, shape):
    p = {k: float(x) for k, x in Q.parts(v, shape).items()}
    p["range"] = _written(p["min"], p["max"])
    return p


def _atom_parts(kind, vals):
    if kind == "scalar":
        return {"value": vals[0]}
    if kind == "range":
        lo, hi = sorted(vals)
        return {"min": lo, "max": hi, "range": _written(lo, hi)}
    if kind == "pair":
        a, b = vals
        return {"at_low_end": a, "at_high_end": b, "min": min(a, b), "max": max(a, b),
                "range": _written(min(a, b), max(a, b))}
    c, lo, hi = vals
    return {"mid": c, "min": lo, "max": hi, "range": _written(lo, hi)}


def _places(d):
    return max(0, -d.as_tuple().exponent)


def supersedes_atoms(text, money_m=False):
    """The numbers that a `supersedes` text names, as (kind, values, printed, decimals): scalars, ranges, "a / b"
    pairs and "c (lo–hi)" central intervals. Counts (…M, unless `money_m`: a record in $M), factors ("factor
    0.977200", "× 0.977"), bracketed notes and the audit's masks (dates, ladder and item references, hashes) are
    left out."""
    clean = A.mask(re.sub(r"\[[^\]]*\]", lambda m: " " * len(m.group(0)), text))
    toks = [t for t in A.tokens(text, clean) if t[5] != "word" and (money_m or t[5] != "M")
            and not re.search(r"(?:factor|×)\s*$", clean[:t[0]])]
    atoms, used = [], set()
    for i, (s, e, raw, lo, hi, _suf, _k) in enumerate(toks):
        places = max(_places(lo), _places(hi))
        nxt = toks[i + 1] if i + 1 < len(toks) else None
        gap = clean[e:nxt[0]] if nxt else ""
        if nxt and gap.strip() == "/" and lo == hi and nxt[3] == nxt[4]:
            atoms.append(("pair", (float(lo), float(nxt[3])), f"{raw} / {nxt[2]}",
                          max(places, _places(nxt[3]))))
        if nxt and gap.strip() == "(" and lo == hi and nxt[3] != nxt[4]:
            atoms.append(("central_interval", (float(lo), float(nxt[3]), float(nxt[4])), f"{raw} ({nxt[2]})",
                          max(places, _places(nxt[3]), _places(nxt[4]))))
            used.add(i + 1)
        if i not in used:
            atoms.append(("scalar", (float(lo),), raw, places) if lo == hi else
                         ("range", (float(lo), float(hi)), raw, places))
    return atoms


def _equal_at(parts_a, parts_b, places):
    """Whether every part of `parts_a` prints as the same-named part of `parts_b` at `places` decimals (a scalar
    against any part)."""
    q = Decimal(1).scaleb(-places)

    def same(x, y):
        return A._dec(x).quantize(q) == A._dec(y).quantize(q)
    if "range" in parts_a:
        return all(same(x, y) for x, y in zip(parts_a["range"], parts_b["range"]))
    return any(same(parts_a["value"], y) for k, y in parts_b.items() if k != "range")


def kind_of(piece):
    """What a `supersedes` piece says its number differs by: the count ("on the raw 40.90M"), an arm ("with road
    budgets fixed", "before the data corrections") or, otherwise, its vintage."""
    if re.search(r"40\.9|\braw\b|CPS union", piece):
        return "count"
    return "arm" if ARM_LABEL.search(piece) else "vintage"


def other_values(recs, values, registry=None, earlier=None):
    """{record id: [other value]}; each is a dict(origin, kind, parts, printed, source, labels). A sibling differs by
    its count, a referenced record, a registry value (`registry`, from current_values) and an earlier case's values
    (`earlier`, from earlier_values) by its vintage, and a superseded number as its piece of `supersedes` says (the
    text is cut at ";" and "=", so "the lane's 31.50–122.48 × factor = 30.78–119.69" gives two pieces)."""
    out = {}
    for rid, rec in recs.items():
        cur = _parts(values[rid], rec["shape"])
        others = []
        if registry and rid in registry:
            others.append(dict(origin="registry", kind="vintage", parts=_parts(registry[rid], rec["shape"]),
                               printed=Q.render(rec, registry[rid], "range_unit" if rec["shape"] in ("ends", "interval")
                                                else "value"),
                               source=f"{rid}: the registry's {rec['case']}, which the evidence map still shows",
                               labels=""))
        for v, label in (earlier or {}).get(rid, []):
            others.append(dict(origin="earlier", kind="vintage", parts=_parts(v, rec["shape"]),
                               printed=Q.render(rec, v, "range_unit" if rec["shape"] in ("ends", "interval")
                                                else "value"),
                               source=f"{rid}: {label}", labels=""))
        if rid.endswith("_priced") and rid[:-len("_priced")] + "_lane" in recs:
            lane = rid[:-len("_priced")] + "_lane"
            others.append(dict(origin="sibling", kind="count", parts=_parts(values[lane], recs[lane]["shape"]),
                               printed=Q.render(recs[lane], values[lane], "mid_range" if recs[lane]["shape"] ==
                                                "central_interval" else "range_unit" if recs[lane]["shape"] ==
                                                "interval" else "value"),
                               source=f"{lane}: {recs[lane]['population']}", labels=recs[lane]["must_name"]))
        for clause in rec["supersedes"].split(";"):
            for ref in re.findall(r"\b[a-z][a-z0-9_]*\.[a-z][a-z0-9_]*\b", clause):
                if ref in recs and ref != rid:
                    distinct = recs[ref]["must_name"] if recs[ref]["must_name"] != rec["must_name"] else ""
                    others.append(dict(origin="referenced", kind="vintage",
                                       parts=_parts(values[ref], recs[ref]["shape"]),
                                       printed=Q.render(recs[ref], values[ref], "range_unit" if
                                                        recs[ref]["shape"] in ("ends", "interval") else "value"),
                                       source=f"{ref}: {recs[ref]['label']}", labels=distinct))
            for piece in clause.split("="):
                for shape, vals, printed, places in supersedes_atoms(piece, money_m=rec["unit"] == "$M"):
                    parts = _atom_parts(shape, vals)
                    if _equal_at(parts, cur, places):
                        continue  # the record's current value, printed as the supersedes prints it
                    others.append(dict(origin="superseded", kind=kind_of(piece), parts=parts, printed=printed,
                                       source=f"supersedes: {clause.strip()}", labels=""))
        if others:
            out[rid] = others
    return out


# ---------------------------------------------------------------- matching a memo number

def rules(tok):
    """Rounding rules to read a memo number with: its decimals, and for a whole number ending in zeros, the hundred
    or ten it may be rounded to."""
    rs = ["dp"]
    if tok["lo"] == tok["hi"] and tok["lo"] == tok["lo"].to_integral_value() and abs(tok["lo"]) >= 100:
        digits = str(abs(int(tok["lo"])))
        zeros = len(digits) - len(digits.rstrip("0"))
        rs += [f"n{10 ** z}" for z in range(1, min(zeros, 3) + 1)]
    return rs


def matched(tok, parts, rs):
    """(part, rule) for each part of `parts` that the memo number reads as, under the first rule that fits."""
    if tok["lo"] != tok["hi"]:
        if "range" not in parts:
            return []
        lo, hi = parts["range"]
        return [("range", r) for r in rs if A.rounds_to(lo, tok["lo"], r) and A.rounds_to(hi, tok["hi"], r)][:1]
    out = []
    for k, v in parts.items():
        r = next((r for r in rs if k != "range" and A.rounds_to(v, tok["lo"], r)), None)
        if r:
            out.append((k, r))
    return out


def unit_ok(unit, tok, clause):
    """The memo number carries the record's unit, or is a bare range or decimal in a clause that carries it."""
    suf, dollar = tok["suf"], "$" in tok["raw"]
    bare = not suf and not dollar and (tok["lo"] != tok["hi"] or _places(tok["lo"]) > 0)
    if unit == "$bn":
        # a bare "$" is not enough: the number itself carries one ("+$464" per household)
        return suf == "bn" or (not suf and (dollar or bare) and re.search(r"\bbn\b|billion", clause) is not None)
    if unit == "$tn":
        return suf == "tn" or (not suf and dollar and "trillion" in clause)
    if unit == "$k":
        return suf == "k" or (not suf and dollar and re.search(r"thousand|per (?:group )?member", clause) is not None)
    if unit == "$":
        return dollar and not suf
    if unit == "%":
        return suf in ("%", "pp") or (bare and re.search(r"%|percent", clause) is not None)
    if unit == "M":
        return suf == "M" or (bare and "million" in clause)
    if unit == "$M":
        return (suf == "M" and dollar) or (not suf and dollar and "million" in clause)
    if unit == "x":
        return not suf and not dollar
    return False


# the units unit_ok reads; main() stops on a record with other values in any other unit
UNITS_READ = {"$bn", "$tn", "$k", "$", "%", "M", "$M", "x"}


def clause(para, s, e):
    """The clause of `para` holding [s, e): its sentence (as quantities.sentence bounds it) cut at semicolons."""
    a = max(para.rfind(". ", 0, s), para.rfind("\n", 0, s), para.rfind(";", 0, s))
    b = [i for i in (para.find(". ", e), para.find("\n", e), para.find(";", e)) if i >= 0]
    return re.sub(r"\s+", " ", para[a + 1 if a >= 0 else 0:(min(b) + 1 if b else len(para))]).strip()


def like(tok, x, rule):
    """`x` printed as the memo prints the number it replaces: the same decimals (or the hundred, under a step rule),
    sign and unit. A range is written as quantities.render writes one."""
    places = max(_places(tok["lo"]), _places(tok["hi"]))

    def one(v):
        d = Q.printed_value(v, rule) if rule != "dp" else Q.rounded(v, places)
        return ("−" if d < 0 else ""), f"{abs(d):,.{0 if rule != 'dp' else places}f}"
    pre, suf = ("$" if "$" in tok["raw"] else ""), tok["suf"]
    if isinstance(x, tuple):
        (s1, b1), (s2, b2) = one(x[0]), one(x[1])
        if s1 and not s2:
            return f"{s1}{pre}{b1}{suf} to +{pre}{b2}{suf}"
        return f"{s1}{pre}{b1}–{b2}{suf}"
    s1, b1 = one(x)
    return f"{s1}{pre}{b1}{suf}"


def tables(raw_lines):
    """{row line: (the table's header row, the caption paragraph just above the table)}."""
    out, i = {}, 0
    while i < len(raw_lines):
        if not raw_lines[i].lstrip().startswith("|"):
            i += 1
            continue
        j = i
        while j + 1 < len(raw_lines) and raw_lines[j + 1].lstrip().startswith("|"):
            j += 1
        k = i - 1 if i > 0 and raw_lines[i - 1].strip() else i - 2
        caption = ""
        if k >= 0 and raw_lines[k].strip() and not raw_lines[k].lstrip().startswith(("|", "#")):
            a, b = RC._block(raw_lines, k)
            caption = " ".join(raw_lines[a:b + 1])
        for r in range(i, j + 1):
            out[r] = (raw_lines[i], caption)
        i = j + 1
    return out


STOP = {"with", "from", "that", "this", "year", "each", "than", "into", "over", "under", "their", "which", "where",
        "when", "they", "them", "these", "those"}


def _words(text):
    return {w.lower().rstrip("s") for w in re.findall(r"[A-Za-z]{4,}", text)} - STOP


def caption_for(caption, heads, col):
    """The caption's clauses (cut at , ; :) that speak to column `col`: those sharing a word with its header, and
    those sharing a word with no header, which speak to the whole table. "the lanes' own central and range on the
    CPS's 40.9M" labels the column "Lane central (range)", not the column "Normalized, beside"."""
    mine = _words(heads[col]) if col < len(heads) else set()
    every = set().union(*(_words(h) for h in heads))
    return " ".join(p for p in re.split(r"[,;:]|\.\s", caption) if _words(p) & mine or not _words(p) & every)


def split_changes(toks, line):
    """The audit reads "from $28.9bn to $30.9bn" as one range; a change is two numbers, the old and the new."""
    out = []
    for s, e, raw, lo, hi, suf, k in toks:
        m = re.search(r"\s+to\s+", raw)
        if lo != hi and m and FROM.search(line[:s]):
            out += [(s, s + m.start(), raw[:m.start()], lo, lo, suf, k),
                    (s + m.end(), e, raw[m.end():], hi, hi, suf, k)]
        else:
            out.append((s, e, raw, lo, hi, suf, k))
    return out


def magnitude(tok):
    return dict(tok, lo=abs(tok["lo"]), hi=abs(tok["hi"]))


def attached(p, gap, tok, item, recs, values, context):
    """The current figure that range `tok` is written as the range of: a single number `p` (the token before it, on
    its line or the paragraph's line above) with only "(" between them (`gap`), read as the current value of a record
    of the same item (the record's prefix; lane records on the raw count excluded). None when the range stands on its
    own."""
    if p is None or tok["lo"] == tok["hi"] or p[3] != p[4] or not re.fullmatch(r"\s*\(\s*\**", gap):
        return None
    prev = dict(raw=p[2].strip(), lo=p[3], hi=p[4], suf=p[5])
    for rid, rec in recs.items():
        if rid.split(".")[0] != item or "raw" in rec["population"]:
            continue
        if unit_ok(rec["unit"], prev, context) and matched(prev, _parts(values[rid], rec["shape"]), rules(prev)):
            return f"{prev['raw']} ({rid})"
    return None


def sweep_text(path, text, recs, values, others):
    """Rows for one memo's text. A table row is read whole, with its column's header cell and the table's caption:
    the row is the sentence, and row, cell and caption are the clause."""
    rows = []
    raw_lines = text.split("\n")
    read = unread(text)
    lines, clean = read.split("\n"), A.mask(read).split("\n")
    tab = tables(raw_lines)
    items = {rid: re.compile(ITEM[rid.split(".")[0]], re.I) for rid in others}
    line_toks = {}
    for i, line in enumerate(lines):
        toks = line_toks[i] = split_changes([t for t in A.tokens(line, clean[i]) if t[5] != "word"], raw_lines[i])
        if not toks:
            continue
        a, b = RC._block(raw_lines, i)
        para = " ".join(raw_lines[a:b + 1])
        off = len(" ".join(raw_lines[a:i])) + (1 if i > a else 0)
        for j, (s, e, raw, lo, hi, suf, _k) in enumerate(toks):
            tok = dict(raw=raw.strip(), lo=lo, hi=hi, suf=suf)
            if i in tab:
                head, caption = tab[i]
                row, col = raw_lines[i], raw_lines[i][:s].count("|")
                cells, heads = row.split("|"), head.split("|")
                a0 = row.rfind("|", 0, s) + 1
                cl = clause(row[a0:row.find("|", e) if row.find("|", e) >= 0 else len(row)], s - a0, e - a0)
                near = " ".join([cl, cells[1] if len(cells) > 1 else "", heads[col] if col < len(heads) else ""])
                wide = f"{near} {caption_for(caption, heads, col)}"
                unit = f"{near} {caption}"  # a unit in the caption holds for every column
                pinned = COMMIT.search(row)
                sent = f"{row} {head}"
            else:
                sent = Q.sentence(para, off + s, off + e)
                cl = near = wide = unit = clause(para, off + s, off + e)
                pinned = None
            before = raw_lines[i][:s]
            above = line_toks.get(i - 1) if i > a else None
            prev, gap = ((toks[j - 1], raw_lines[i][toks[j - 1][1]:s]) if j else
                         (above[-1], f"{raw_lines[i - 1][above[-1][1]:]} {before}") if above else (None, ""))
            rs = rules(tok)
            for rid, rec_others in others.items():
                rec = recs[rid]
                if not items[rid].search(sent):
                    continue
                if rid in ITEM_EXTRA and not re.search(ITEM_EXTRA[rid], sent, re.I):
                    continue
                if not unit_ok(rec["unit"], tok, unit):
                    continue
                # a record the registry keeps as a magnitude (expr abs(…)) matches a signed memo number
                t = magnitude(tok) if rec["expr"].replace(" ", "").startswith("abs(") else tok
                cur = _parts(values[rid], rec["shape"])
                if matched(t, cur, rs):
                    continue
                for o in rec_others:
                    hit = matched(t, o["parts"], rs)
                    if not hit:
                        continue
                    must = re.search(o["labels"], wide, re.I) if o["labels"] else None
                    past = VINTAGE_LABEL.search(near) or FROM.search(before) or pinned
                    if o["kind"] == "count":
                        found = COUNT_LABEL.search(wide) or must or past
                    elif o["kind"] == "arm":
                        found = ARM_LABEL.search(wide) or past
                    else:
                        found = must or past or COUNT_LABEL.search(wide) or ARM_LABEL.search(wide)
                    label = found.group(0).strip() if found else ""
                    tied = attached(prev, gap, tok, rid.split(".")[0], recs, values, unit)
                    urged = ADJ_CURRENT.search(before)
                    state = "as_current" if tied or urged else "labelled" if label else "unlabelled"
                    allowed = [why for (p, r, q, phrase), why in ALLOW.items()
                               if (p, r, q) == (path, rid, tok["raw"]) and phrase in sent]
                    if allowed and state != "labelled":
                        state, label = "allowed", f"allowed: {allowed[0]}"
                    why = (f"range of {tied}" if tied else
                           f"after \"{re.sub(r'[^A-Za-z ]', '', urged.group(0)).strip()}\"" if urged else "")
                    part, rule = hit[0]
                    now = cur.get(part)
                    current = (like(tok, now, rule) if now is not None else
                               Q.render(rec, values[rid], "range_unit" if rec["shape"] in ("ends", "interval")
                                        else "mid_range" if rec["shape"] == "central_interval" else "value"))
                    basis = ("on the CPS's 40.90M" if o["kind"] == "count" else
                             o["source"].split(": ", 1)[1] if o["origin"] == "superseded" else
                             f"as {o['source'].split(':')[0]}")
                    rows.append(dict(
                        file=path, line=i + 1, quoted=tok["raw"], record=rid, current=current,
                        other=f"{o['printed']} ({o['origin']}: {o['source']})",
                        **{"class": f"{o['kind']}_{state}"}, label="; ".join(x for x in (label, why) if x),
                        suggested=("" if state in ("labelled", "allowed") else
                                   f"{current} now; or keep {tok['raw']} in a clause of its own and name its basis "
                                   f"({basis})" if state == "as_current" else
                                   f"{current} now; or keep {tok['raw']} and name its basis ({basis})"),
                        sentence=row.strip() if i in tab else cl))
                    break
    return rows


# ---------------------------------------------------------------- positive controls

CONTROLS = [
    ("an unlabelled lane-count value",
     "Crashes that group drivers cause cost other residents $42.3bn a year.",
     {("crash.fault_based_priced", "count_unlabelled")}),
    ("the same value labelled",
     "Crashes that group drivers cause cost other residents $42.3bn a year on the CPS's 40.90M.",
     {("crash.fault_based_priced", "count_labelled")}),
    ("another arm's value", "Congestion costs other residents $19.2bn a year.",
     {("congestion.item", "arm_unlabelled")}),
    ("the same arm named", "Congestion costs other residents $19.2bn a year with road budgets fixed.",
     {("congestion.item", "arm_labelled")}),
    ("a count label does not name an arm", "Congestion costs other residents $19.2bn a year on the CPS count.",
     {("congestion.item", "arm_unlabelled")}),
    ("an earlier case quoted as current", "The main case costs other residents $258–292bn a year.",
     {("case.main", "vintage_unlabelled")}),
    ("the earlier case named", "The September 26 schools case cost other residents $258–292bn a year.",
     {("case.main", "vintage_labelled")}),
    ("\"from\" marks only the number after it",
     "At the mixed-group fraction, victims' harm rises from $28.9bn to $30.9bn.",
     {("victims.harm", "arm_labelled"), ("victims.harm", "count_unlabelled")}),
    ("a stray match: another unit", "Colombia 46.5% of the PM2.5 sample.", set()),
    ("a stray match: another item", "Colombia's output grew by $46.5bn.", set()),
    ("the current value", "Crashes that group drivers cause cost other residents $40.6bn a year.", set()),
    ("a lane-count total quoted as current", "Adding the social costs gives the pairing, $416.2–490.7bn.",
     {("pairing.total", "count_unlabelled")}),
    ("a lane range written as the current central's range",
     "Road crashes cost other residents $11.4bn (−$57.7bn to +$74.3bn in the lane).",
     {("crash.span_priced", "count_as_current")}),
    ("the same across a line break",
     "Road crashes cost other residents $11.4bn\n(−$57.7bn to +$74.3bn in the lane).",
     {("crash.span_priced", "count_as_current")}),
    ("the lane range in a clause of its own",
     "Road crashes cost other residents $11.4bn; the lane's own range is −$57.7bn to +$74.3bn on the CPS's 40.90M.",
     {("crash.span_priced", "count_labelled")}),
    ("a dated case after \"now\"", "The main case now costs $258–292bn, the September 26 schools case.",
     {("case.main", "vintage_as_current")}),
    ("a caption's count label reaches only the column it names",
     ("$bn a year; the central on the account's 39.7M, the lanes' own central on the CPS's 40.9M, and the figure "
      "against average residents:\n\n| Item | Central | Lane central | Normalized |\n|---|---:|---:|---:|\n"
      "| PM2.5 | 68.1 | 69.7 | −46.5 |\n"),
     {("pm25.cost", "count_labelled"), ("pm25.normalized_priced", "count_unlabelled")}),
    ("a Revisions section", "## Revisions\n\n- Crashes that group drivers cause were $42.3bn a year.\n", set()),
    ("a bracketed note", "Crashes charged by fault [2026-09-29: $42.3bn on the\nlane's count] now cost $40.6bn.",
     set()),
    ("the adopted case as the main case", "The main case costs other residents $389–461bn a year.", set()),
    ("the October 5 case quoted as current", "The main case costs other residents $390–461bn a year.",
     {("case.main", "vintage_unlabelled")}),
    ("the October 5 case named", "The October 5 case cost other residents $390–461bn a year.",
     {("case.main", "vintage_labelled")}),
    ("the October 5 case named as v5", "The v5 case cost other residents $390–461bn a year.",
     {("case.main", "vintage_labelled")}),
    ("the October 5 case after \"now\"", "The main case now costs $390–461bn a year.",
     {("case.main", "vintage_as_current")}),
    ("the September 29 case quoted as current", "The main case costs other residents $371–435bn a year.",
     {("case.main", "vintage_unlabelled")}),
    ("the September 29 case named", "The September 29 case cost other residents $371–435bn a year.",
     {("case.main", "vintage_labelled")}),
    ("the September 29 case named as v4", "The v4 case cost other residents $371–435bn a year.",
     {("case.main", "vintage_labelled")}),
    ("the September 29 case after \"now\"", "The main case now costs $371–435bn a year.",
     {("case.main", "vintage_as_current")}),
    ("the September 27 case quoted as current", "The main case costs other residents $322–387bn a year.",
     {("case.main", "vintage_unlabelled")}),
    ("the September 27 case named", "The September 27 case cost other residents $322–387bn a year.",
     {("case.main", "vintage_labelled")}),
    ("the September 27 case after \"now\"", "The main case now costs $322–387bn a year.",
     {("case.main", "vintage_as_current")}),
    ("the adopted case per member", "The main case is $9.1–10.8k a year per member.", set()),
    # v5's per-member band prints as v6's at one decimal ($9.1–10.8k), so its controls print two
    ("the October 5 case per member quoted as current", "The main case is $9.13–10.79k a year per member.",
     {("case.per_member", "vintage_unlabelled")}),
    ("the October 5 case per member named",
     "The main case is $9.10–10.79k a year per member (October 5: $9.13–10.79k).",
     {("case.per_member", "vintage_labelled")}),
    ("the September 29 case per member quoted as current", "The main case is $9.4–10.9k a year per member.",
     {("case.per_member", "vintage_unlabelled")}),
    ("the September 29 case per member named",
     "The main case is $9.1–10.8k a year per member (September 29: $9.4–10.9k).",
     {("case.per_member", "vintage_labelled")}),
    ("the September 27 case per member quoted as current", "The main case is $8.1–9.8k a year per member.",
     {("case.per_member", "vintage_unlabelled")}),
    ("the September 27 case per member named",
     "The main case is $9.1–10.8k a year per member (September 27: $8.1–9.8k).",
     {("case.per_member", "vintage_labelled")}),
    ("the adopted cash set", "Counting benefits when paid, the main case costs others $307.4–385.4bn a year.", set()),
    ("the October 5 cash set quoted as current",
     "Counting benefits when paid, the main case costs others $307.4–383.4bn a year.",
     {("case.cash_set", "vintage_unlabelled")}),
    ("the October 5 cash set named",
     "Counting benefits when paid, the main case costs others $307.4–385.4bn a year (October 5: $307.4–383.4bn).",
     {("case.cash_set", "vintage_labelled")}),
    ("the September 29 cash set quoted as current",
     "Counting benefits when paid, the main case costs others $294.7–361.8bn a year.",
     {("case.cash_set", "vintage_unlabelled")}),
    ("the adopted pairing", "Fiscal and social costs together come to $489–571bn a year.", set()),
    ("the adopted pairing per member", "Fiscal and social costs together are $11.4–13.3k a year per member.", set()),
    ("the October 5 pairing quoted as current", "Fiscal and social costs together come to $490–571bn a year.",
     {("pairing.total", "vintage_unlabelled")}),
    ("the October 5 pairing named",
     "Fiscal and social costs together come to $489–571bn a year (October 5: $490–571bn).",
     {("pairing.total", "vintage_labelled")}),
    ("the October 5 pairing per member quoted as current",
     "Fiscal and social costs together are $11.5–13.3k a year per member.",
     {("pairing.per_member_priced", "vintage_unlabelled")}),
    ("the October 5 pairing's fiscal footing quoted as current",
     "The pairing's low end takes the fiscal main case at the Hispanic footing, $385.4bn.",
     {("pairing.fiscal_footing", "vintage_unlabelled")}),
    ("the September 29 pairing quoted as current", "Fiscal and social costs together come to $463–536bn a year.",
     {("pairing.total", "vintage_unlabelled")}),
    ("the September 29 pairing named",
     "Fiscal and social costs together come to $489–571bn a year (September 29: $463–536bn).",
     {("pairing.total", "vintage_labelled")}),
    ("the September 29 pairing per member quoted as current",
     "Fiscal and social costs together are $11.7–13.5k a year per member.",
     {("pairing.per_member_priced", "vintage_unlabelled")}),
    ("the September 29 pairing's fiscal footing quoted as current",
     "The pairing's low end takes the fiscal main case at the Hispanic footing, $366.7bn.",
     {("pairing.fiscal_footing", "vintage_unlabelled")}),
    ("the September 27 pairing quoted as current", "Fiscal and social costs together come to $414–488bn a year.",
     {("pairing.total", "vintage_unlabelled")}),
    ("the September 27 pairing named",
     "Fiscal and social costs together come to $489–571bn a year (September 27: $414–488bn).",
     {("pairing.total", "vintage_labelled")}),
    ("the September 27 pairing per member quoted as current",
     "Fiscal and social costs together are $10.4–12.3k a year per member.",
     {("pairing.per_member_priced", "vintage_unlabelled")}),
    # a record in $M (the family-line ledger, since item T)
    ("a $M value from before item T quoted as current",
     "A Mexican founder's family line runs $1.29M behind a white family line.",
     {("family_line.gap", "vintage_unlabelled")}),
    ("the $M value now", "A Mexican founder's family line runs $1.48M behind a white family line.", set()),
    # the IR-5 parent's cost: the pre-T range is flagged, and a sentence that only names a parent is not read
    ("an IR-5 range from before item T quoted as current", "An IR-5 parent costs $235–288k at 3%.",
     {("ir5.lifetime_cost_55_65", "vintage_unlabelled")}),
    ("a parent named, another quantity", "Routes need a citizen spouse or parent, or a U visa (288k pending).",
     set()),
]


def controls(recs, values, others):
    fails = []
    for name, text, want in CONTROLS:
        got = {(r["record"], r["class"]) for r in sweep_text("control.md", text, recs, values, others)}
        ok = got == want
        print(f"  {'PASS' if ok else 'FAIL'} control: {name}{'' if ok else f' — got {sorted(got)}'}")
        if not ok:
            fails.append(name)
    return fails


# ---------------------------------------------------------------- memos

def git(*args):
    return subprocess.run(["git", "-C", str(ROOT), *args], check=True, capture_output=True, text=True).stdout


def exemption(path, text):
    """The reason `path` is exempt, or None. An exemption holds only while the memo still says what earns it; a
    memo rewritten without that sentence is read again, so a lapsed exemption stops the run instead."""
    if path not in EXEMPT:
        return None
    phrase, reason = EXEMPT[path]
    if phrase not in text:
        raise SystemExit(f"[BLOCKED] {path} is exempt only while it says {phrase!r}, and it no longer does: "
                         f"sweep it, or give the exemption a new reason")
    return reason


def lapsed_allowances(docs):
    """The ALLOW entries whose memo is not read, or no longer holds the entry's phrase and number (line breaks read
    as spaces). An allowance holds only for the sentence it was written for."""
    texts = {path: re.sub(r"\s+", " ", text) for path, text in docs}
    return [(path, rid, quoted, phrase) for path, rid, quoted, phrase in ALLOW
            if path not in texts or phrase not in texts[path] or quoted not in texts[path]]


def memos(rev, exempt=True):
    """(path, text) of every memo in scope, and the skipped paths with the reason. `exempt=False` reads the EXEMPT
    memos too, as the sweep did before they were exempted."""
    names = (sorted(p.relative_to(ROOT).as_posix() for p in (ROOT / MEMOS).glob("immigration-*.md")) if rev is None
             else sorted(n for n in git("ls-tree", "--name-only", rev, f"{MEMOS}/").split("\n")
                         if re.fullmatch(rf"{MEMOS}/immigration-.*\.md", n)))
    missing = sorted(set(EXEMPT) - set(names))
    if exempt and missing:
        raise SystemExit(f"[BLOCKED] exempt memos not found: {missing}")
    keep, skipped = [], []
    for n in names:
        if n == LADDER:
            skipped.append((n, "the confidence ladder"))
        elif DATED_AUDIT.search(Path(n).name):
            skipped.append((n, "a dated audit"))
        else:
            text = (ROOT / n).read_text() if rev is None else git("show", f"{rev}:{n}")
            reason = exemption(n, text) if exempt else None
            if reason:
                skipped.append((n, f"exempt: {reason}"))
            else:
                keep.append((n, text))
    return keep, skipped


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--rev", default="HEAD", help="the git revision whose memos are read")
    ap.add_argument("--worktree", action="store_true", help="read the memos on disk instead")
    ap.add_argument("--out", type=Path, default=HERE / "derived")
    ap.add_argument("--no-exempt", action="store_true",
                    help="read the EXEMPT memos too (reproduces a pass made before their exemption)")
    args = ap.parse_args()
    recs = Q.load_registry()
    values, registry = current_values(recs)
    earlier = earlier_values()
    others = other_values(recs, values, registry, earlier)
    missing =sorted({rid.split(".")[0] for rid in others} - set(ITEM))
    if missing:
        raise SystemExit(f"[BLOCKED] records with other values but no ITEM context: {missing}")
    unread_units = sorted({recs[rid]["unit"] for rid in others} - UNITS_READ)
    if unread_units:
        raise SystemExit(f"[BLOCKED] records with other values in a unit unit_ok does not read: {unread_units}")
    fails = controls(recs, values, others)
    if fails:
        raise SystemExit(f"[BLOCKED] {len(fails)} control(s) failed: {fails}")
    rev = None if args.worktree else git("rev-parse", "--short", args.rev).strip()
    docs, skipped = memos(rev, exempt=not args.no_exempt)
    lapsed = lapsed_allowances(docs)
    if lapsed:
        raise SystemExit(f"[BLOCKED] ALLOW entries whose memo no longer says their phrase and number: {lapsed}; "
                         f"drop them, or key them to the new sentence")
    rows = [r for path, text in docs for r in sweep_text(path, text, recs, values, others)]
    args.out.mkdir(parents=True, exist_ok=True)
    cols = ["file", "line", "quoted", "record", "current", "class", "suggested", "other", "label", "sentence"]
    with (args.out / "memo_sweep.csv").open("w", newline="") as handle:
        w = csv.DictWriter(handle, fieldnames=cols, lineterminator="\n")
        w.writeheader()
        w.writerows(rows)
    on_disk = (ROOT / REGISTRY).read_bytes()
    counts = {}
    for r in rows:
        counts[r["class"]] = counts.get(r["class"], 0) + 1
    meta = dict(rev=rev or "worktree", memos_read=len(docs), memos_skipped=[f"{n}: {why}" for n, why in skipped],
                adopted={rid: dict(lane=ADOPTED[rid][0], value=list(values[rid]), registry_value=list(registry[rid]),
                                   registry_case=recs[rid]["case"]) for rid in sorted(registry)},
                earlier={rid: [dict(lane=lane, value=list(v), case=label)
                               for (lane, *_), (v, label) in zip(EARLIER[rid], cases)]
                         for rid, cases in sorted(earlier.items())},
                records_with_other_values={rid: len(o) for rid, o in sorted(others.items())},
                registry_sha256=hashlib.sha256(on_disk).hexdigest(),
                registry_equals_rev=(None if rev is None else on_disk == git("show", f"{rev}:{REGISTRY}").encode()),
                rows_by_class=dict(sorted(counts.items())))
    (args.out / "memo_sweep_meta.json").write_text(json.dumps(meta, indent=1) + "\n")
    flagged = sum(v for k, v in counts.items() if not k.endswith(("_labelled", "_allowed")))
    print(f"swept {len(docs)} memos at {rev or 'the working tree'} ({len(skipped)} skipped): {len(rows)} quotes of "
          f"other values, {flagged} flagged; " + ", ".join(f"{k} {v}" for k, v in sorted(counts.items())))


if __name__ == "__main__":
    main()
