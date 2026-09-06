#!/usr/bin/env python3
"""Render news.yaml into homepage markdown, or diff it against the old wording.

    python3 generators/render_news.py --diff      # old vs new, refd items only
    python3 generators/render_news.py --diff --all
    python3 generators/render_news.py --write     # emit into home.md

For a refd item the FACT is composed from the canonical record and the byline is
appended verbatim. The item itself contains no venue, year, or title, so those
cannot drift from the record. For an authored item the text is passed through
unchanged -- there is nothing to derive it from.
"""

from __future__ import annotations

import argparse
import _paths
import _pubrefs
import pathlib
import re
import sys

# Resolved for BOTH layouts -- these used ROOT plus a literal davis-web path,
# so they ran only from the orchestrator and would break the moment the site
# had to rebuild itself without it.
DATA, PAGES, SITE = _paths.DATA, _paths.PAGES, _paths.SITE
ROOT = SITE.parent          # message text only; no path is built from it
HOME = PAGES / "home.md"


def load():
    import yaml
    # DATA, not ROOT/"data/...". This lambda was the last ROOT-relative reader
    # in the file and it is why --write raised FileNotFoundError from inside the
    # site while every other path had been converted: one helper, four call
    # sites, all of them wrong in the layout that has to survive.
    r = lambda p: yaml.safe_load((DATA / p).read_text())
    pubs = {p["id"]: p for p in r("publications.yaml")["publications"]}
    grants = {g["id"]: g for g in r("funding.yaml")["grants"]}
    awards = {a["id"]: a for cat in r("awards.yaml")["awards"].values() for a in cat}
    return r("news.yaml")["news"], pubs, grants, awards


def short_venue(v: str) -> str:
    """Prefer the parenthesised abbreviation; a news line says ICSE, not
    'Proceedings of the 48th IEEE/ACM International Conference on ...'."""
    m = re.search(r"\(([A-Z][A-Za-z0-9/&-]{1,12})\)", v or "")
    if m:
        return m.group(1)
    return re.sub(r"^Proceedings of the \d+\w*\s*", "", v or "").strip()


def render(item: dict, pubs, grants, awards) -> str:
    ref = item.get("ref")
    byline = (item.get("byline") or "").strip()

    if ref in pubs:
        p = pubs[ref]
        venue = short_venue(p.get("venue"))
        year = p.get("year")
        where = f"{venue} {year}" if venue and year else (venue or str(year or ""))
        # Sixth consumer of "where does this record's link come from" -- see
        # _pubrefs. Reading links.paper directly here is why a paper_url set on
        # the record did not reach the news line.
        link = _pubrefs.paper_link(p) or (p.get("links") or {}).get("blog")
        title = f"[{p['title']}]({link})" if link else p["title"]
        fact = f"*{title}*" + (f" — {where}." if where else ".")
    elif ref in awards:
        a = awards[ref]
        fact = f"{a['title']} ({a['year']})."
    elif ref in grants:
        g = grants[ref]
        fact = f"{g['sponsor']} funds *{g['title']}*"
        fact += f" (#{g['number']})." if g.get("number") else "."
    else:
        return item.get("text", "")

    return (fact + " " + byline).strip()


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--diff", action="store_true")
    ap.add_argument("--all", action="store_true", help="include unchanged authored items")
    ap.add_argument("--write", action="store_true")
    args = ap.parse_args(argv)

    news, pubs, grants, awards = load()

    if args.diff or not args.write:
        changed = 0
        for it in news:
            if not it.get("ref"):
                if args.all:
                    print(f"\n  {it['year']}  UNCHANGED (authored)"
                          f"{'  cites=' + it['cites'] if it.get('cites') else ''}")
                    print(f"    {it['text'][:150]}")
                continue
            changed += 1
            print(f"\n  {it['year']}  ref={it['ref']}")
            print(f"    OLD  {it.get('original', '')[:160]}")
            print(f"    NEW  {render(it, pubs, grants, awards)[:160]}")
        auth = sum(1 for it in news if not it.get("ref"))
        print(f"\n  {changed} items re-derived from records · {auth} authored, unchanged")
        return 0

    by_year: dict[int, list[str]] = {}
    for it in news:
        # str(): the record carries years both quoted and bare, so grouping on
        # the raw value gives int and str keys that will not sort against each
        # other. Four-digit years sort identically as text.
        by_year.setdefault(str(it["year"]), []).append(render(it, pubs, grants, awards))
    out = ["# Announcements", "",
           "This disorganized list summarizes my research, teaching, and service activities.", "",
           "<!-- GENERATED from davis-web/data/news.yaml by generators/render_news.py.",
           "     Facts come from the canonical records; bylines are authored there. -->", ""]
    # <details>/<summary> per year, newest open. Native elements: keyboard
    # operable, announce their own expanded state, no ARIA and no JavaScript to
    # fall out of sync with what is on screen. markdown="1" so kramdown still
    # renders the bullets inside.
    years = sorted(by_year, reverse=True)
    for yr in years:
        op = " open" if yr == years[0] else ""
        out.append(f'<details class="news-year" markdown="1"{op}>')
        out.append(f'<summary><h3 class="news-year__label">{yr}</h3></summary>')
        out.append("")
        out += [f"- {line}" for line in by_year[yr]]
        out.append("")
        out.append("</details>")
        out.append("")
    text = HOME.read_text()
    HOME.write_text(text[:text.find("# Announcements")] + "\n".join(out))
    print(f"  wrote {len(news)} items into {HOME.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
