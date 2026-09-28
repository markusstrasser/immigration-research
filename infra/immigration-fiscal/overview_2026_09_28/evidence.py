"""Render the ladder groups: curated findings, method symbols, per-entry notes, bibliography, retired list.

Method symbols and dataset names are detected from each entry's own text, so they say what the
entry reports using, not what the page claims.
"""

import html
import re

from groups import GROUPS, RETIRED

# (symbol, label, description, patterns). Acronyms match case-sensitively on word boundaries.
KINDS = [
    ("S", "survey", "survey microdata (people's answers, person by person)", [
        ("CPS", r"\bCPS\b|\bASEC\b"), ("ACS", r"\bACS\b|\bPUMS\b"), ("MEPS", r"\bMEPS\b"),
        ("NHTS", r"\bNHTS\b"), ("GSS", r"\bGSS\b"), ("ANES", r"\bANES\b"), ("NLSY", r"\bNLSY"),
        ("NCVS", r"\bNCVS\b"), ("Consumer Expenditure Survey", r"Consumer Expenditure|\bCE 20\d\d"),
        ("New Immigrant Survey", r"New Immigrant Survey"), ("IIMMLA", r"\bIIMMLA\b"), ("CILS", r"\bCILS\b"),
        ("Pew surveys", r"\bPew\b"), ("American Housing Survey", r"American Housing Survey|\bAHS\b"),
        ("SCF", r"\bSCF\b"), ("ENIGH", r"\bENIGH\b"), ("NAEP", r"\bNAEP\b"), ("PISA", r"\bPISA\b"),
        ("SIPP", r"\bSIPP\b"), ("ECLS-K", r"\bECLS"), ("IPUMS", r"\bIPUMS\b"), ("SPI", r"\bSPI\b")]),
    ("A", "records", "administrative records (tax, benefit, police, birth, school records)", [
        ("IRS", r"\bIRS\b"), ("SSA", r"\bSSA\b"), ("T-MSIS", r"T-MSIS"), ("CMS", r"\bCMS\b"),
        ("NVSS births", r"\bNVSS\b"), ("NIBRS", r"\bNIBRS\b"), ("BJS", r"\bBJS\b"), ("SHR", r"\bSHR\b"),
        ("FBI UCR", r"\bUCR\b|\bFBI\b"), ("USCIS / OHSS", r"\bUSCIS\b|\bOHSS\b"),
        ("Census of Governments", r"Census of Governments"), ("CMS S-10", r"\bS-10\b"), ("CRDC", r"\bCRDC\b"),
        ("Opportunity Atlas", r"Opportunity Atlas|Opportunity Insights"),
        ("Social Capital Atlas", r"Social Capital Atlas"), ("INEGI", r"\bINEGI\b"),
        ("CDC WONDER", r"\bWONDER\b"), ("Sentencing Commission", r"Sentencing Commission|\bUSSC\b"),
        ("Texas DPS", r"Texas DPS|\bDPS\b"), ("NCES", r"\bNCES\b"), ("HMDA / FHFA", r"\bFHFA\b|\bHMDA\b"),
        ("register data", r"\bregister")]),
    ("N", "accounts", "national accounts and budget totals", [
        ("BEA NIPA", r"\bBEA\b|\bNIPA\b"), ("Trustees / SOSI", r"Trustees|Statement of Social Insurance"),
        ("Treasury", r"\bTreasury\b"), ("CBO baseline", r"\bCBO\b")]),
    ("M", "model", "the account's engine or another model run here", [
        ("account engine", r"\bengine\b|main_case|main case"), ("CES production", r"\bCES\b"),
        ("back-cast", r"back-cast"), ("lineage model", r"\blineage\b")]),
    ("C", "causal", "a design aimed at cause (instrument, panel, placebo, lottery)", [
        ("instrument", r"instrument|\bIV\b|shift-share|Bartik"), ("fixed effects", r"fixed effects|fixed-effects"),
        ("placebo", r"placebo"), ("lottery", r"lottery"), ("synthetic control", r"synthetic control")]),
    ("T", "test", "a test fixed before looking, against data the account never used", [
        ("held-out test", r"before looking|held-out|which no step of it used|never used")]),
]


def strip_md(s):
    s = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", s)
    s = s.replace("**", "").replace("`", "")
    return re.sub(r"\s+", " ", s).strip()


def tag_blocks(text, tag):
    """Balanced [TAG: ...] blocks."""
    out = []
    for m in re.finditer(r"\[" + tag + r":", text):
        depth, j = 0, m.start()
        while j < len(text):
            depth += {"[": 1, "]": -1}.get(text[j], 0)
            if depth == 0:
                break
            j += 1
        out.append(strip_md(text[m.end():j]))
    return out


def keep_links(s):
    s = re.sub(r"\[([^\]]*)\]\((https?://[^)\s]+)\)", r"\1 <\2>", s)
    return strip_md(s)


def source_spans(text):
    """Every 'SOURCE:' span, inside any tag block, up to its closing bracket or the next tag."""
    out = []
    for m in re.finditer(r"SOURCE:", text):
        depth, j = 0, m.end()
        while j < len(text):
            c = text[j]
            if c == "[":
                depth += 1
            elif c == "]":
                depth -= 1
                if depth < 0:
                    break
            elif depth == 0 and text.startswith(("; CALCULATION", "; DATA", "; INFERENCE"), j):
                break
            j += 1
        out.append(keep_links(text[m.end():j]))
    return out


MONTHS = ("January February March April May June July August September October November December "
          "Census Table Note Figure Section Prisoners Survey Wave Round Law Fiscal Budget Report Rating "
          "Revisions Decision Brief Profile Statement Tables Update Release Vintage Summer Spring Fall Winter").split()
NOT_AUTHORS = set((
    "The In Across Over Since From After Before Between By For At On Of To With Within Without During Until "
    "Executed Corrected Updated Revised Added Measured Published Reported Adjusted Pooled Recovered Supplied "
    "Jan Feb Mar Apr Jun Jul Aug Sep Sept Oct Nov Dec Notes Note Bureau Hispanic White Black Asian Mexican "
    "Mexico America American Angeles California Texas Florida Illinois Arizona Nevada Colorado York Chicago Denver "
    "Houston Dallas Rochester Germany Denmark Sweden Norway Europe Italy Spain Austria Canada Cuba India China "
    "Congress Medicare Medicaid Social Security Federal State States Current Central Only Each Every All Both "
    "Scored Charged Pricing Priced Tested Weighted Translated Counted Carried Read Run Rerun Moving Removing "
    "Cohort Cohorts Class Classes Wave Year Years Age Ages Men Women Children Pupils Adults Residents Arrivals "
    "Legal Unauthorized Immigrants Natives Model Case Cases Lane Entry Entries Ladder Memo Page Chart Basics City Economy Institute Narrowed Nationally Qualified Reports Select Sensitivity Supplement Under Victimization"
).split())
AUTHOR_YEAR = re.compile(
    r"\b((?:[A-Z][a-zà-ÿ'’]+)(?:(?: (?:&|and) |[–-])[A-Z][a-zà-ÿ'’]+)*(?: et al\.?)?),? \(?((?:19[5-9]|20[0-2])\d)[a-z]?\b")


def citations(text):
    """Author-year citations named in the entry's own text."""
    out = []
    for m in AUTHOR_YEAR.finditer(strip_md(text)):
        a = m.group(1)
        head = a.split()[0].split("–")[0]
        if head in MONTHS or head in NOT_AUTHORS or head.endswith(("'s", "’s")):
            continue
        out.append(f"{a.replace(' and ', ' & ')} {m.group(2)}")
    return list(dict.fromkeys(out))


def detect(text):
    kinds, names = [], []
    for sym, _label, _desc, pats in KINDS:
        hit = [name for name, pat in pats if re.search(pat, text)]
        if hit:
            kinds.append(sym)
            names += [n for n in hit if n not in names]
    return kinds, names


def cut(s, n=260):
    return s if len(s) <= n else s[: n - 1].rsplit(" ", 1)[0] + "…"


def rating(text):
    m = re.search(r"Rating: \*\*(.+?)\*\*", text)
    return strip_md(m.group(1)) if m else ""


PUBLICATION = re.compile(r"https?://|doi|NBER|\bet al\b|[A-Z][a-z]+(?:[–-][A-Z][a-z]+)* \(?(?:19|20)\d\d\b|Journal|JPE|QJE|AER")
INTERNAL = re.compile(r"^(memo|research/|infra/|\.\./|immigration-)|\.md\b|\.csv\b|\.py\b|RESULT")


def chips(kinds):
    return "".join(f'<abbr class="chip k{k}" title="{html.escape(next(d for s, _, d, _ in KINDS if s == k))}">{k}</abbr>'
                   for k in kinds)


def check_coverage(entries, fail):
    seen = {}

    def put(key, where):
        key = str(key)
        if key in seen:
            fail(f"entry {key} is in both {seen[key]} and {where}")
        seen[key] = where

    for g in GROUPS:
        for i, f in enumerate(g["findings"]):
            for r in f["refs"]:
                put(r, f"{g['id']}#{i + 1}")
        for r in g["minor"]:
            put(r, f"{g['id']} minor")
    for r in RETIRED:
        put(r, "retired")
    missing = sorted(set(entries) - set(seen), key=lambda k: (k[0] == "o", int(k.lstrip("o"))))
    unknown = sorted(set(seen) - set(entries))
    if missing or unknown:
        fail(f"unplaced ladder entries {missing}; placed but not in the ladder {unknown}. Place new entries in groups.py")


def render(entries, fail):
    check_coverage(entries, fail)
    bib = {}
    table, blocks = [], []
    n_find = 0
    for gi, g in enumerate(GROUPS, 1):
        n_refs = sum(len(f["refs"]) for f in g["findings"]) + len(g["minor"])
        table.append(f'<tr><td class="num">{gi}</td><td><a href="#{g["id"]}">{html.escape(g["title"])}</a></td>'
                     f'<td>{html.escape(g["size"])}</td><td class="num">{len(g["findings"])}</td>'
                     f'<td class="num">{n_refs}</td></tr>')
        items = []
        for fi, f in enumerate(g["findings"], 1):
            n_find += 1
            fid = f"{g['id']}-{fi}"
            text_all = " ".join(entries[str(r)]["body"] for r in f["refs"])
            kinds, names = detect(text_all)
            notes = []
            for r in f["refs"]:
                e = entries[str(r)]
                srcs = [s for s in source_spans(e["body"]) if s]
                for s in srcs:
                    for part in re.split(r";\s+|,\s+(?=https?://)", s):
                        part = part.strip(" .,")
                        if re.search(r"https?://", part) and not INTERNAL.search(part):
                            k = re.sub(r"\W+", " ", part.lower())[:90]
                            bib.setdefault(k, [cut(part, 220), []])[1].append(fid)
                for c in citations(e["body"]):
                    k = re.sub(r"\W+", " ", c.lower())
                    bib.setdefault(k, [c, []])[1].append(fid)
                files = []
                for tag in ("CALCULATION", "DATA"):
                    for b in tag_blocks(e["body"], tag):
                        files += re.findall(r"[\w./-]+\.(?:py|cjs|js|csv|json|sql)\b", b)
                files = list(dict.fromkeys(files))[:4]
                st = f' <span class="st">{e["status"]}</span>' if e["status"] in ("superseded",) else ""
                notes.append(
                    f'<li><span class="ref">{e["key"]}</span> {html.escape(e["claim"])}{st}'
                    + (f'<br><span class="how">Evidence: {html.escape(cut(e["rating"], 300))}</span>' if e["rating"] else "")
                    + (f'<br><span class="how">Sources: {html.escape("; ".join(cut(s, 160) for s in srcs[:3]))}</span>' if srcs else "")
                    + (f'<br><span class="how">Files: {html.escape(", ".join(files))}</span>' if files else "")
                    + "</li>")
            refs = ", ".join(str(r) for r in f["refs"])
            items.append(
                f'<li id="{fid}"><span class="chips">{chips(kinds)}</span> {html.escape(f["text"])} '
                f'<span class="ref">{refs}</span>'
                f'<details><summary>data and sources</summary>'
                f'<p class="how">{html.escape(", ".join(names)) or "no dataset named in the entry text"}</p>'
                f'<ul class="entries">{"".join(notes)}</ul></details></li>')
        terms = "".join(f"<dt>{html.escape(t)}</dt><dd>{html.escape(m)}</dd>" for t, m in g["terms"])
        minor = ""
        if g["minor"]:
            ml = "".join(f'<li><span class="ref">{entries[str(r)]["key"]}</span> {html.escape(entries[str(r)]["claim"])}</li>'
                         for r in g["minor"])
            minor = f'<details><summary>{len(g["minor"])} narrower entries, not summarised</summary><ul class="entries">{ml}</ul></details>'
        blocks.append(f"""
<section id="{g['id']}" class="group">
  <h3><span class="gnum">{gi}</span> {html.escape(g['title'])}</h3>
  <p class="size">{html.escape(g['size'])}</p>
  <p>{html.escape(g['why'])}</p>
  <ul class="findings">{''.join(items)}</ul>
  {f'<details><summary>terms</summary><dl class="terms">{terms}</dl></details>' if terms else ''}
  {minor}
</section>""")
    legend = "".join(f'<li>{chips([s])} <b>{label}</b>: {html.escape(desc)}</li>' for s, label, desc, _ in KINDS)
    bib_items = sorted(bib.values(), key=lambda v: v[0].lower())
    bibl = "".join(
        f'<li>{html.escape(t)} <span class="ref">{" ".join(f"<a href=#{x}>{x}</a>" for x in dict.fromkeys(ids))}</span></li>'
        for t, ids in bib_items)
    cur = [k for k in RETIRED if not str(k).startswith("o")]
    retired = (f'<li><span class="ref">o1–o51</span> the April–June layer, re-rated in the September layers</li>'
               + "".join(f'<li><span class="ref">{k}</span> {html.escape(entries[str(k)]["claim"])} '
                         f'<span class="how">({html.escape(RETIRED[k])})</span></li>' for k in cur))
    return dict(table="\n".join(table), groups="\n".join(blocks), legend=legend, biblio=bibl,
                retired=retired, n_find=n_find, n_bib=len(bib_items), n_retired=len(RETIRED))
