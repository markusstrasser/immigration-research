#!/usr/bin/env python3
"""Phase 4: keyword-anchored claim extraction from derived/mr_posts.jsonl -> derived/mr_claims.csv.

Every claim_text is a verbatim substring of the fetched body_text (assert-checked).
Categorical columns are heuristic first-pass labels; `notes` records voice
(author-voice vs quoted-block) and `auto` so the parent knows what was hand-checked.
"""
import csv, json, os, re, sys

BASE = os.path.dirname(os.path.abspath(__file__))
DERIVED = os.path.join(BASE, "derived")

# false friends: phrases that carry a topic keyword but no immigration content
FALSE_FRIENDS = re.compile(r"reporters without borders|doctors without borders|m[eé]decins sans|"
                           r"border collie|borderline|borders bookstore|border of the|"
                           r"migraine\w*|native speaker\w*|native american\w*|native plant\w*|"
                           r"visa card|visa inc|new mexic\w*", re.I)

TOPIC = re.compile(r"\bimmigra\w*|\bmigrant\w*|\bmigrat\w*|\bemigra\w*|\bmexic\w*|\bhispanic\w*|"
                   r"\blatino\w*|\bborder\w*|\bdeport\w*|\basylum\w*|\brefugee\w*|"
                   r"\bopen borders\b|\bundocumented\b|\billegal alien\w*|\bforeign-born\b|"
                   r"\bnative[- ]born\b|\bnativis\w*|\bh-?1b\b|\bvisas?\b|\bamnesty\b|"
                   r"\bassimilat\w*|\bguest work\w*|\bnaturaliz\w*", re.I)


def topical(text):
    return bool(TOPIC.search(FALSE_FRIENDS.sub(" ", text)))

ASSERT = re.compile(r"\b(is|are|was|were|has|have|do|does|did|will|would|should|can|cannot|can't|"
                    r"increase\w*|decrease\w*|reduce\w*|raise\w*|lower\w*|rise\w*|fall\w*|boost\w*|"
                    r"cost\w*|gain\w*|lose\w*|benefit\w*|harm\w*|no evidence|little evidence|"
                    r"more likely|less likely|higher|lower|larger|smaller|net positive|net negative|"
                    r"about|roughly|approximately|percent|per cent|%)\b", re.I)

NUM = re.compile(r"\d")

TYPES = [
    ("fiscal", r"fiscal|budget|tax(?:es|payer|ation)?|welfare cost|deficit|revenue|entitlement|medicaid|"
               r"social security|public finance|net cost|net benefit|cbo\b|nas\b"),
    ("wage", r"\bwage\w*|\bearning\w*|\bsalar\w*|labor market|labour market|job\w*|employment|unemploy\w*|"
             r"displace\w*|mariel|card\b|borjas"),
    ("crime", r"\bcrime\w*|\bcriminal\w*|\bhomicide\w*|\bmurder\w*|\bincarcerat\w*|\bprison\w*|\barrest\w*|"
              r"\bconvict\w*|\bviolen\w*|\bgang\w*|\bMS-13\b"),
    ("welfare-use", r"welfare use|food stamps|snap\b|public benefit\w*|means-tested|safety net|eitc\b|"
                    r"medicaid enroll"),
    ("housing", r"\bhousing\b|\brent\w*|\bhome price\w*|\bzoning\b|\bshelter\w*|\bhomeless\w*|"
                r"\bconstruction\b|\bpermit\w*"),
    ("political", r"\bvot(?:e|es|ing|er\w*)\b|\belection\w*|\bparty\b|\bdemocrat\w*|\brepublican\w*|"
                  r"\bpopulis\w*|\bfar[- ]right\b|\bbacklash\b|\bpolitic\w*"),
    ("assimilation", r"assimilat\w*|integrat\w*|second[- ]generation|third[- ]generation|intergenerational|"
                     r"\benglish\b|\blanguage\b|\bintermarriage\b|\bmobilit\w*|\bconverg\w*"),
    ("global-gains", r"world gdp|global gdp|double world|place premium|trillion\w*|global output|"
                     r"open borders|clemens|kennan|world output|world income"),
    ("culture", r"\bcultur\w*|\btrust\b|\bsocial capital\b|\bvalues\b|\bhuntington\b|\bethnic\w*|"
                r"\bdiversity\b|\bcivic\b|\bnorms\b|\breligio\w*"),
]

OBJECTS = [
    ("Mexican-origin", r"mexic\w*"),
    ("descendants", r"second[- ]generation|third[- ]generation|children of immigrant\w*|"
                    r"descendant\w*|us-born children|intergenerational"),
    ("high-skill", r"high[- ]skill\w*|\bh-?1b\b|\bstem\b|\bphd\w*|\bengineer\w*|\bscientist\w*|"
                   r"\binventor\w*|\btalent\b|\bo-1\b|\beb-?\d"),
    ("low-skill", r"low[- ]skill\w*|unskilled|less[- ]educated|high school dropout\w*|manual labor"),
    ("first generation", r"foreign[- ]born|first[- ]generation|immigrants themselves|newcomer\w*|"
                         r"arrival\w*|the immigrants\b"),
    ("all immigrants", r"\bimmigrant\w*|\bimmigration\b|\bmigrant\w*"),
]

AXES = [
    ("federal", r"federal|cbo\b|washington|national budget|social security|medicare"),
    ("local", r"\blocal\b|\bcity\b|\bcities\b|\bcounty\b|\bstate and local\b|\bschool district\w*|"
              r"\bneighborhood\w*|\bmunicipal\w*|\btexas\b|\bcalifornia\b|\bnew york\b"),
    ("resident/all-government", r"all levels of government|state and federal|total government|"
                                r"all-in|lifetime|resident population"),
    ("national average", r"\bnational\b|\baverage american\w*|\bthe country\b|\bus gdp\b|\bthe united states\b|"
                         r"\beconomy[- ]wide\b|\baggregate\b"),
]

# Keyword flags for the seven modes in research/immigration-economist-rhetorical-failures-2026-04-22.md.
# Only patterns that carry the rhetorical MOVE are kept; a topic word alone (voting, housing,
# per-capita) is not evidence of the move, so those modes require a dismissal or a slide in the
# same sentence. Every non-empty flag is a candidate for the parent to adjudicate, never a verdict.
# Keyword flags for the seven modes in research/immigration-economist-rhetorical-failures-2026-04-22.md.
# Balanced for the parent's use: a flag marks a sentence worth adjudicating, never a verdict, and a
# bare topic word (voting, housing, per-capita) is not enough - the pattern must carry a claim about
# the ledger, the magnitude, the comparison base or the dismissal. `none-apparent` asserts nothing.
FAIL = [
    ("upper-bound laundering",
     r"double (?:the )?world (?:gdp|output|income)|doubling world|world gdp would|"
     r"trillion dollar bills?|place premium|would (?:roughly )?double|"
     r"open borders[^.]{0,80}(?:gdp|output|gains?|trillion|richer|growth)|"
     r"(?:gains?|increase) of \$?\d+(?:\.\d+)? ?trillion"),
    ("ledger switching",
     r"net fiscal|fiscal(?:ly)? (?:positive|plus|negative|burden|cost|benefit|impact|effect)|"
     r"pays? for (?:itself|themselves)|pay more in taxes|not a fiscal burden|"
     r"(?:cost|save)s? (?:the )?taxpayers?|welfare state[^.]{0,60}(?:afford|sustain|survive)|"
     r"government coffers|public purse"),
    ("denominator masking",
     r"(?:incarcerat\w*|crime|arrest|conviction|imprison\w*) rates?[^.]{0,60}"
     r"(?:lower|higher|no higher|the same|similar|converg\w*|declin\w*)|"
     r"(?:less|more|no more) likely to (?:be (?:incarcerated|imprisoned|arrested|convicted)|"
     r"commit (?:a )?crime)|per 100,000|per capita[^.]{0,50}(?:lower|higher|same)"),
    ("aggregate-output trump card",
     r"makes? (?:us|the country|america|americans|the nation) richer|"
     r"good for the economy|immigration (?:raises|increases|boosts|adds to) (?:gdp|output|growth)|"
     r"(?:gdp|output|growth) (?:is|would be|will be) higher[^.]{0,40}(?:with|because of) immigr"),
    ("marginal-to-mass extrapolation",
     r"no (?:measurable|detectable|discernible|significant|noticeable) (?:effect|impact)|"
     r"(?:studies|research|evidence|economists) (?:find|finds|show|shows|suggest|suggests) "
     r"(?:no|little|essentially no)|mariel|natural experiment|"
     r"labor market (?:absorbs?|absorbed)|little or no effect"),
    ("capacity erasure",
     r"(?:housing|capacity|shelter|schools?|congestion)[^.]{0,60}"
     r"(?:is|are|just|merely|only) (?:a |an )?(?:zoning|supply|policy|local|american) "
     r"(?:problem|issue|failure|choice)|build more housing|"
     r"not (?:a )?(?:real|binding|serious) constraint"),
    ("political-economy erasure",
     r"only (?:coherent )?(?:objection|argument|worry|concern) (?:is|are)[^.]{0,40}(?:vot|politic)|"
     r"political externalit\w*|immigrants (?:do not|don't|rarely|seldom) vote|"
     r"(?:citizenship|voting) (?:is|are) the (?:real|only) (?:issue|question)"),
]

SRC_PAT = re.compile(
    r"\b(NBER|National Bureau of Economic Research|Journal of [A-Z][\w ]{2,30}|American Economic Review|"
    r"AER\b|QJE\b|Quarterly Journal of Economics|Econometrica|CBO\b|Congressional Budget Office|"
    r"National Academies|NAS\b|Cato\b|Pew\b|Census Bureau|Brookings|IZA\b|CEPR\b|OECD\b|World Bank|"
    r"BLS\b|Bureau of Labor Statistics|DHS\b|ICE\b|CBP\b|Peri\b|Borjas\b|Clemens\b|Nowrasteh\b|"
    r"Caplan\b|Card\b|Chetty\b|Abramitzky\b|Boustan\b|Hanson\b|Kennan\b|Ottaviano\b|Dustmann\b|"
    r"Mayda\b|Bansak\b|Hunt\b|Jaeger\b|Edo\b|Alesina\b|Collins\b|Sequeira\b|Nunn\b)")

SENT_SPLIT = re.compile(r"(?<=[.!?])\s+(?=[A-Z“\"(])")

# navigational / pointer sentences carry no checkable proposition
NAV = re.compile(r"^(here is|here's|here are|via |see also|see here|the pointer|hat tip|"
                 r"i am indebted|read the whole|more here|the link is|full post|"
                 r"that is from|this is from|for the pointer|elsewhere|related|"
                 r"i thank |speculative|file under|the article is|link here)", re.I)
NAV2 = re.compile(r"here is the (link|paper|article|story|piece)|for the pointer|"
                  r"^\s*\d+\.\s*$|assorted links", re.I)

MAX_PER_POST = int(os.environ.get("MAX_CLAIMS_PER_POST", "6"))


def label(text, table, default):
    for name, pat in table:
        if re.search(pat, text, re.I):
            return name
    return default


def words(s):
    return len(s.split())


def trim60(s):
    """Whitespace-normalised verbatim quote, capped at 60 words (brief limit)."""
    w = re.sub(r"\s+", " ", s).strip().split()
    return " ".join(w[:60])


def main():
    inp = os.path.join(DERIVED, "mr_posts.jsonl")
    rows = []
    n_posts = n_used = 0
    for line in open(inp, encoding="utf-8"):
        try:
            p = json.loads(line)
        except Exception:  # noqa: BLE001
            continue
        n_posts += 1
        body = p.get("body_text") or ""
        if not topical(body) and not topical(p.get("title") or ""):
            continue
        srcs = SRC_PAT.findall(body)
        post_src = srcs[0] if srcs else ""
        picked = []
        for para in body.split("\n"):
            quoted = para.startswith("> ")
            clean = para[2:] if quoted else para
            for sent in SENT_SPLIT.split(clean):
                sent = sent.strip()
                if not (25 <= words(sent) + 25 <= 200) and words(sent) > 70:
                    continue
                if words(sent) < 6 or words(sent) > 70:
                    continue
                if not topical(sent) or not ASSERT.search(sent):
                    continue
                if NAV.search(sent) or NAV2.search(sent):
                    continue
                typed = [n for n, pat in TYPES if re.search(pat, sent, re.I)]
                has_num = bool(NUM.search(sent))
                # a row must carry a subject-matter claim, not just a topic word
                if not typed and not has_num:
                    continue
                score = (2 if has_num else 0) + (0 if quoted else 2) + len(typed)
                picked.append((score, sent, quoted))
        picked.sort(key=lambda t: -t[0])
        seen = set()
        kept = 0
        for score, sent, quoted in picked:
            key = sent[:80].lower()
            if key in seen:
                continue
            seen.add(key)
            ctype = label(sent, TYPES, "other")
            rows.append({
                "post_url": p["url"],
                "date": (p.get("date") or "")[:10],
                "author": p.get("author") or "unknown",
                "claim_text": trim60(sent),
                "claim_type": ctype,
                "object": label(sent, OBJECTS, "unclear"),
                "axis": label(sent, AXES, "unstated"),
                "quoted_source": (SRC_PAT.search(sent).group(1) if SRC_PAT.search(sent) else post_src),
                "candidate_failure_mode": label(sent, FAIL, "none-apparent"),
                "notes": ("quoted-block" if quoted else "author-voice")
                         + "; auto-extracted; failure-mode=keyword-flag (not adjudicated)"
                         + f"; score={score}",
            })
            kept += 1
            if kept >= MAX_PER_POST:
                break
        if kept:
            n_used += 1

    # verbatim assertion: every claim_text must be a substring of its post body
    bodies = {}
    for line in open(inp, encoding="utf-8"):
        try:
            p = json.loads(line)
        except Exception:  # noqa: BLE001
            continue
        bodies[p["url"]] = p.get("body_text") or ""
    def norm(t):
        return re.sub(r"\s+", " ", t).strip()

    nbodies = {u: norm(b) for u, b in bodies.items()}
    bad = [r for r in rows if norm(r["claim_text"]) not in nbodies.get(r["post_url"], "")]
    print(f"verbatim check: {len(rows) - len(bad)}/{len(rows)} exact substrings "
          f"(whitespace-normalised)", flush=True)
    for r in bad[:5]:
        print("  NONVERBATIM:", r["post_url"], r["claim_text"][:80], flush=True)

    # drop claims repeated verbatim across posts (assorted-links boilerplate)
    seen_global, dedup = {}, []
    for r in rows:
        k = re.sub(r"\W+", " ", r["claim_text"].lower())[:120]
        if k in seen_global:
            continue
        seen_global[k] = 1
        dedup.append(r)
    print(f"cross-post dedup: {len(rows)} -> {len(dedup)}", flush=True)
    rows = sorted(dedup, key=lambda r: (r["date"], r["post_url"]))

    out = os.path.join(DERIVED, "mr_claims.csv")
    with open(out, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["post_url", "date", "author", "claim_text", "claim_type",
                                          "object", "axis", "quoted_source",
                                          "candidate_failure_mode", "notes"])
        w.writeheader()
        w.writerows(rows)
    print(f"CLAIMS: {len(rows)} from {n_used}/{n_posts} posts -> {out}", flush=True)


if __name__ == "__main__":
    main()
