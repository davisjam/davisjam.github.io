#!/usr/bin/env python3
"""One-time retrofit: homepage announcements -> data/news.yaml.

    python3 generators/retrofit_news.py --dry-run
    python3 generators/retrofit_news.py --write

The homepage carried 161 hand-maintained announcements across seven years -- the
largest remaining violation of model/ssot-records.md, and the same failure mode
the Service page had: an enumerative list with no source, decaying at the rate
the record grows.

The news model applies the SSOT split with a **byline** field:

    ref:     the canonical record this announces (C-7, G-1, an award key)
    byline:  the ONLY authored text -- the human voice on the item

The factual half is rendered FROM the referenced record, never retyped. So the
venue in a "paper accepted" item cannot drift from publications.yaml, because
the item does not contain a venue. The byline is what makes a news feed worth
reading -- "Huzzah!", "Have fun, Milo!" -- and modeling that away would kill the
page, so it stays authored.

Items with no canonical counterpart (student milestones, lab news) carry `text:`
instead: still authored, still dated, simply not derivable until people are
modeled.

Matching is gated on the item actually announcing a publication. Without that
gate "Berk will intern at Socket" matches a supply-chain paper at 0.6 -- a
plausible score for an entirely wrong fact.
"""

from __future__ import annotations

import argparse
import pathlib
import re
import sys

# Matching is DETERMINISTIC: arXiv id, or a (venue, year) key that identifies
# exactly one record. An earlier fuzzy title-overlap matcher described itself as
# "tuned for precision" and measured ~45% -- 28 of 51 refs were wrong. It was
# checks/news_refs.py, reading independent evidence, that established this; the
# matcher's own confidence signal did not.
ROOT = pathlib.Path(__file__).resolve().parent.parent
HOME = ROOT / "repos/davisjam.github.io/_pages/home.md"
OUT = ROOT / "data/news.yaml"

# An ANNOUNCEMENT reports that a work landed; a CITE merely points at one while
# reporting something else ("Geoff heads to Bluesky ... a follow-up from our
# JSS'25 paper"). Both mention a paper, so "paper" alone cannot separate them --
# and conflating them makes two items claim one work.
# The discriminator is the item's SUBJECT, not its verb. "Paper on secure
# regular expressions: **S&P 2023**." announces a work with no verb at all,
# while "Geoff heads to Bluesky ... a follow-up from our JSS'25 paper" is about
# a person and merely points at one. Testing for announcement verbs mislabelled
# 15 terse announcements as citations.
PEOPLE_SUBJECT = re.compile(
    r"^\s*(?:\w+\s+){0,3}\b(heads to|will intern|interns|is interning|defends|defended|"
    r"joins|joined|graduat\w*|starts|will start|will work|wins|receives|is awarded)\b", re.I)
PUB_EVENT = re.compile(r"\b(accepted|paper|preprint|will appear|appears|published|to appear)\b", re.I)
AWARD_EVENT = re.compile(r"\b(award|honou?r|fellow|recogni|wins|winner|receive)\b", re.I)
GRANT_EVENT = re.compile(r"\b(grant|nsf #|funds|donat|gift|sponsor)\b", re.I)

# Sentences that are voice rather than fact. These become the byline; the rest
# is derivable and is dropped in favour of the canonical record.
VOICE = re.compile(
    r"(congrat\w*|huzzah|well done|nice work|enjoy|have fun|have a great|good luck|"
    r"sounds amazing|hope \w+ has|welcome|thank you|excited|look forward|proud|what an honou?r|delighted|thrilled|so cool|very cool|wonderful|huge news)", re.I)


def squash(s: str) -> str:
    return re.sub(r"[^a-z0-9]", " ", s.lower())


def parse_home() -> list[tuple[int, str]]:
    text = HOME.read_text()
    body = text[text.find("# Announcements"):]
    out, year = [], None
    for line in body.splitlines():
        if m := re.match(r"^## (\d{4})", line):
            year = int(m.group(1))
        elif line.startswith("- ") and year:
            out.append((year, line[2:].strip()))
    return out


def split_byline(txt: str) -> tuple[str, str]:
    """Return (factual_remainder, byline). The byline is the voice."""
    parts = re.split(r"(?<=[.!?])\s+", txt)
    voice = [p for p in parts if VOICE.search(p)]
    fact = [p for p in parts if not VOICE.search(p)]
    return " ".join(fact).strip(), " ".join(voice).strip()


ARXIV = re.compile(r"arxiv\.org/(?:abs|pdf)/(\d{4}\.\d{4,5})", re.I)
NEWS_VENUE = re.compile(r"\*\*([A-Za-z][A-Za-z0-9&/+._ -]{1,40})\*\*|"
                        r"\b([A-Z][A-Za-z0-9&/+.-]{1,24})['’](\d{2})\b")
REC_ABBREV = re.compile(r"\(([A-Z][A-Za-z0-9/&-]{1,12})\)")


def _norm_abbrev(v: str) -> str:
    """ICSE-NIER'25 -> icse; MSR-Dataset 2023 -> msr.

    The qualifier after the dash names a TRACK, not a different venue.
    """
    v = re.sub(r"['’]?\d{2,4}$", "", v.strip())
    if not v.strip():
        return ""
    return re.sub(r"[^a-z]", "", v.split("-")[0].split()[0].lower())


def _news_venue_years(txt: str) -> list:
    out = []
    for m in NEWS_VENUE.finditer(txt):
        raw = (m.group(1) or m.group(2) or "").strip()
        if not raw:
            continue
        yr = None
        if m.group(3):
            yr = 2000 + int(m.group(3))
        else:
            y = re.search(r"(20\d{2})", raw)
            if y:
                yr = int(y.group(1))
        a = _norm_abbrev(raw)
        if a:
            out.append((a, yr))
    return out


def match_publication(txt: str, pubs: list) -> str | None:
    """DETERMINISTIC joins only.

    The previous fuzzy title-overlap matcher measured ~45% precision. The book
    B-1, titled "Model-Based Agentic Software Engineering", absorbed seven
    unrelated items: any line containing "software engineering" scored 0.67 and
    won UNIQUELY, so the ambiguity guard passed it. Guarding against ties does
    nothing about a short generic title dominating.

    These joins are determined by evidence rather than merely plausible:
      1. arXiv id       the id -> record map is injective
      2. (venue, year)  84% of such keys identify exactly one work; where they
                        do not, decline rather than guess
    """
    if not PUB_EVENT.search(txt):
        return None

    m = ARXIV.search(txt)
    if m:
        hits = [p for p in pubs
                if m.group(1) in " ".join((p.get("links") or {}).values())]
        if len(hits) == 1:
            return hits[0]["id"]

    for abb, yr in _news_venue_years(txt):
        cands = []
        for p in pubs:
            rm = REC_ABBREV.search(p.get("venue") or "")
            if not rm or _norm_abbrev(rm.group(1)) != abb:
                continue
            if yr is not None and p.get("year") not in (yr, yr - 1):
                continue
            cands.append(p)
        if len(cands) == 1:
            return cands[0]["id"]
    return None


def match_award(txt: str, awards: dict, year: int) -> str | None:
    """Stable A-n id, on a UNIQUE strong title match in a consistent year.

    The previous version returned a composite key TRUNCATED to 40 characters
    (unstable, and not resolvable back to a record) and took the first entry
    over threshold in file order.
    """
    if not AWARD_EVENT.search(txt):
        return None
    t = squash(txt)
    hits = []
    for entries in awards.values():
        for a in entries:
            toks = [w for w in squash(a["title"]).split() if len(w) > 5]
            if not toks:
                continue
            if (sum(1 for w in toks if w in t) / len(toks) >= 0.75
                    and abs(a["year"] - year) <= 1):
                hits.append(a["id"])
    return hits[0] if len(hits) == 1 else None


GRANT_CITE = re.compile(r"associated with|supported by|under (?:NSF|grant)|part of", re.I)


def match_grant(txt: str, grants: list[dict]) -> str | None:
    if not GRANT_EVENT.search(txt):
        return None
    if m := re.search(r"#?(\d{7})", txt):
        for g in grants:
            if g.get("number") == m.group(1):
                return g["id"]
    # Title-only matching resolved a 2022 Cisco gift to G-1, the 2026 NSF
    # CAREER: it returned the first record over threshold in FILE ORDER. Require
    # a unique strong match AND a sponsor consistent with the item.
    t = squash(txt)
    hits = []
    for g in grants:
        toks = [w for w in squash(g["title"]).split() if len(w) > 5]
        if not toks or sum(1 for w in toks if w in t) / len(toks) < 0.5:
            continue
        sponsor = squash(g["sponsor"]).split()
        lead = next((w for w in sponsor if len(w) > 3 and w != "national"), "")
        if lead and lead not in t:
            continue
        hits.append(g["id"])
    return hits[0] if len(hits) == 1 else None


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    g = ap.add_mutually_exclusive_group()
    g.add_argument("--dry-run", action="store_true", default=True)
    g.add_argument("--write", action="store_true")
    args = ap.parse_args(argv)

    import yaml
    pubs = yaml.safe_load((ROOT / "data/publications.yaml").read_text())["publications"]
    awards = yaml.safe_load((ROOT / "data/awards.yaml").read_text())["awards"]
    grants = yaml.safe_load((ROOT / "data/funding.yaml").read_text())["grants"]

    items = parse_home()
    rows, stats = [], {"publication": 0, "award": 0, "grant": 0, "authored": 0}

    for year, txt in items:
        about_a_person = bool(PEOPLE_SUBJECT.search(txt))
        cites_a_grant = bool(GRANT_CITE.search(txt))
        ref = match_publication(txt, pubs)
        kind = "publication" if ref else None
        if ref and about_a_person:
            # It points at the work without announcing it: a citation, not the
            # item's subject. Keep the authored text and attach `cites`.
            rows.append({"year": year, "kind": "authored", "text": txt, "cites": ref})
            stats["authored"] += 1
            continue
        if not ref:
            ref = match_grant(txt, grants)
            kind = "grant" if ref else None
            if ref and cites_a_grant:
                rows.append({"year": year, "kind": "authored", "text": txt, "cites": ref})
                stats["authored"] += 1
                continue
        if not ref:
            ref = match_award(txt, awards, year)
            kind = "award" if ref else None

        if ref:
            _, byline = split_byline(txt)
            rows.append({"year": year, "kind": kind, "ref": ref,
                         "byline": byline or None, "original": txt})
            stats[kind] += 1
        else:
            rows.append({"year": year, "kind": "authored", "text": txt})
            stats["authored"] += 1

    # A ref claimed by two items means the record set is INCOMPLETE, not that
    # both items are about one work: ASE-Tools 2022 and ASE-NIER 2022 are
    # different papers, and only one ASE-2022 record exists. Withdraw both refs
    # and surface the gap rather than publishing a wrong attribution.
    from collections import Counter
    claims = Counter(r["ref"] for r in rows if r.get("ref"))
    contested = {r for r, n in claims.items() if n > 1}
    for r in rows:
        if r.get("ref") in contested:
            stats[r["kind"]] -= 1
            stats["authored"] += 1
            rows[rows.index(r)] = {"year": r["year"], "kind": "authored",
                                   "text": r["original"], "needs_record": r["ref"]}
    if contested:
        print(f"  withdrew refs contested by >1 item (record gap): {sorted(contested)}")

    print(f"  {len(items)} announcements retrofitted:")
    for k, v in stats.items():
        label = "authored (no canonical record yet)" if k == "authored" else f"ref -> {k}"
        print(f"    {v:>3}  {label}")

    if not args.write:
        print("\n  DRY RUN. Sample:")
        for r in rows[:4]:
            if r.get("ref"):
                print(f"    - ref: {r['ref']}\n      byline: {r.get('byline')!r}")
            else:
                print(f"    - text: {r['text'][:70]!r}")
        print("\n  Re-run with --write to emit data/news.yaml")
        return 0

    out = ["# data/news.yaml — homepage announcements.",
           "#",
           "# Retrofitted from the hand-maintained homepage list by",
           "# generators/retrofit_news.py; hand-maintained since.",
           "#",
           "# The SSOT split, with a byline:",
           "#   ref:    the canonical record this announces. The FACT is rendered from",
           "#           that record, so a venue or award name here cannot drift.",
           "#   byline: the only authored text. The voice is the point of a news feed;",
           "#           modeling it away would kill the page.",
           "#   text:   for items with no canonical counterpart (student milestones and",
           "#           lab news). Authored whole, pending a people model.",
           "#",
           "# `original` preserves the pre-retrofit wording so the rendering can be",
           "# checked against what the page used to say. It is not published.",
           "",
           "schema_version: 1",
           "news:"]
    for r in rows:
        out.append(f"  - year: {r['year']}")
        out.append(f"    kind: {r['kind']}")
        if r.get("ref"):
            out.append(f"    ref: {r['ref']}")
            if r.get("byline"):
                out.append(f"    byline: {yamlstr(r['byline'])}")
            out.append(f"    original: {yamlstr(r['original'])}")
        else:
            out.append(f"    text: {yamlstr(r['text'])}")
            if r.get("cites"):
                out.append(f"    cites: {r['cites']}")
            if r.get("needs_record"):
                out.append(f"    # contested {r['needs_record']}: a second work "
                           f"shares that venue+year and is missing from the record")
    OUT.write_text("\n".join(out) + "\n")
    print(f"\n  wrote {OUT}")
    return 0


def yamlstr(s: str) -> str:
    return '"' + s.replace("\\", "\\\\").replace('"', '\\"') + '"'


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
