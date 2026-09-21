"""Parse the living confidence ladder into cards for the explorer.

Every card is the ladder's own sentence at its own line; nothing is summarised or re-scored here.
Status is mechanical: `historical` for the dated pre-September layers (entries 1-51), `qualified`
when an entry opens with a bracketed correction or is named in the file's opening correction notes,
else `current`. Topics and ledger links come from the keyword rules below and are labelled as such
on the page.
"""
from __future__ import annotations

import re
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[3]
LADDER = ROOT/"research/immigration-confidence-ladder.md"
SKIP_SECTIONS = {"Revisions", "Two weakest assumptions"}  # numbered lists that are not ladder entries

# topic -> (pattern, ledger tokens the page can light up). Order is display order.
RULES = [
    ("Schools and education", r"school|educat|pupil|enrol|\bELL\b|college|degree|student", ["education_services"]),
    ("Crime and custody", r"crime|incarcerat|prison|arrest|homicide|victim|institutionali|custody|detention|felony", ["public_order_safety"]),
    ("Benefits and health", r"medicaid|medicare|\bSNAP\b|welfare|benefit|transfer|\bEITC\b|social security|\bSSI\b|elder|nursing|uninsured", ["household_transfer"]),
    ("Taxes and receipts", r"\btax|receipt|revenue|payroll|\bITIN\b|remit", ["direct_receipts", "incidence_receipts"]),
    ("Debt and interest", r"interest|\bdebt\b|borrow", ["interest"]),
    ("Defense and public goods", r"defen[cs]e|public.goods|general government|congestible", ["public_goods"]),
    ("Labor market and production", r"wage|employment|labou?r|\bhours\b|complement|displace|productiv|\bGDP\b|\bTFP\b|surplus|shift-share", ["production"]),
    ("Prices, rent and housing", r"price|\brent|housing|consumer|crowding", []),
    ("Generations and lineage", r"generation|descendant|lineage|attrition|ancestry|\bG[123]\b|assimilat|third-plus", []),
    ("Fiscal ledgers", r"fiscal|ledger|balance|\bNPV\b|lifetime|net cost|deficit|per person", []),
    ("Politics, norms and culture", r"\bvot|turnout|politic|party|norms|trust|cultur|language|giving|civic", []),
    ("Selection and origins", r"selectiv|origin|indian|asian|muslim|cuban|salvador|guatemal|visa|admission|unauthorized|undocumented", []),
]


def plain(text):
    text = re.sub(r"\[([^\]]+)\]\((?:[^)]+)\)", r"\1", text)      # [label](url) -> label
    return re.sub(r"\*\*|__", "", text).strip()


NUMBER_LIST = r"((?:\d+(?![\d%]|\.\d)\s*(?:[–-]\s*\d+(?![\d%]|\.\d))?(?:\s*(?:,|/|and)\s*)?)+)"
NAMED = re.compile(r"entr(?:y|ies)\s*"+NUMBER_LIST, flags=re.I)
# "replaces 12 and 41", "qualifies105/106", "supersedes 67's ...": one entry acting on others
ACTS_ON = re.compile(r"(?:replaces|supersedes|qualif(?:y|ies)|narrows|corrects)\s*(?:entr(?:y|ies)\s*)?"+NUMBER_LIST, flags=re.I)
SUBJECT = re.compile(r"\s*(?:already\s+)?(?:qualif|supersede|replace|narrow|correct)", flags=re.I)


def entry_numbers(chunk):
    for part in re.finditer(r"(\d+)\s*(?:[–-]\s*(\d+))?", chunk):
        lo, hi = int(part.group(1)), int(part.group(2) or part.group(1))
        if 0 <= hi-lo <= 12:  # a correction list; a layer span such as "65-97" is not one
            yield from range(lo, hi+1)


def header_qualified(lines, first_entry_line):
    """Entry numbers named in the correction notes that open the file, with the note that names them."""
    noted = {}
    for line in lines[:first_entry_line]:
        for pattern in (NAMED, ACTS_ON):
            for match in pattern.finditer(line):
                if pattern is NAMED and SUBJECT.match(line[match.end():]):
                    continue  # "entries 107-111 qualify 83/87": the named entries do the qualifying
                for n in entry_numbers(match.group(1)):
                    noted.setdefault(n, plain(line)[:400])
    return noted


def parse(path=LADDER) -> dict[str, Any]:
    lines = path.read_text().splitlines()
    starts, section = [], None
    for i, line in enumerate(lines):
        if line.startswith("## "):
            section = line[3:].strip()
        match = re.match(r"^(\d+)\. ", line)
        if match and section not in SKIP_SECTIONS:
            starts.append((int(match.group(1)), i, section))
    if not starts:
        raise ValueError("No ladder entries found")
    numbers = [n for n, _, _ in starts]
    if len(set(numbers)) != len(numbers):
        raise ValueError("Duplicate ladder entry numbers outside the skipped sections")
    noted = header_qualified(lines, min(i for _, i, _ in starts))
    cards = []
    for number, i, section in starts:
        j = i+1
        while j < len(lines) and lines[j].strip() and not re.match(r"^\d+\. |^#", lines[j]):
            j += 1
        raw = " ".join(l.strip() for l in lines[i:j])
        text = plain(re.sub(r"^\d+\.\s*", "", raw))
        bracket = re.match(r"^\[([^\]]{12,})\]", text)
        if number <= 51:
            status, note = "historical", f"Dated earlier ladder, layer: {section}"
        elif bracket:
            status, note = "qualified", bracket.group(1)
        elif number in noted:
            status, note = "qualified", noted[number]
        else:
            status, note = "current", None
        topics, affects = [], []
        for topic, pattern, tokens in RULES:
            if re.search(pattern, text, flags=re.I):
                topics.append(topic)
                affects += [t for t in tokens if t not in affects]
        cards.append(dict(n=number, line=i+1, section=section, status=status, note=note, text=text,
                          topics=topics or ["Other"], affects=affects))
    by_number = {card["n"]: card for card in cards}
    for card in cards:  # a later entry that replaces, supersedes, qualifies or narrows an earlier one
        for match in ACTS_ON.finditer(card["text"]):
            for n in entry_numbers(match.group(1)):
                target = by_number.get(n)
                if target and n != card["n"] and target["status"] == "current":
                    target.update(status="qualified", note=f"Entry {card['n']} names this entry: \"{match.group(0).strip()}\". Read {card['n']} with it.")
    return dict(source=str(path.relative_to(ROOT)), topics=[r[0] for r in RULES]+["Other"],
                cards=sorted(cards, key=lambda c: -c["n"]))


if __name__ == "__main__":
    parsed_cards = parse()["cards"]
    by_status = {}
    for card in parsed_cards:
        by_status[card["status"]] = by_status.get(card["status"], 0)+1
    print(f"{len(parsed_cards)} ladder entries: {by_status}")
    for card in sorted(parsed_cards, key=lambda c: c["n"]):
        if card["status"] == "qualified":
            print(f"  {card['n']:>3} qualified: {card['note'][:140]}")
