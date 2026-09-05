#!/usr/bin/env python3
"""Verify every news ref against the record it claims, mechanically.

    python3 checks/news_refs.py            # report
    python3 checks/news_refs.py --strict   # exit 1 on any error

Written BEFORE the matcher that populates the refs, deliberately. The first
matcher reported itself as "tuned for precision" and was measured at ~45%: a
book with the short generic title "Model-Based Agentic Software Engineering"
absorbed seven unrelated items, because any news line containing "software
engineering" scored 0.67 and won uniquely, so an ambiguity guard passed it.

A guard against TIES does not catch a generic title dominating. The lesson is
that a matcher cannot be trusted to assess itself; something that reads the
independent evidence has to. That is this file.

Every check uses `original` -- the pre-retrofit wording preserved on each item --
as independent evidence against the referenced record:

  DUPLICATE-REF     a news item announces ONE work, so a repeated ref is an
                    error by construction. This alone caught 7 of the 28.
  VENUE-MISMATCH    the item names a venue the referenced record does not have
  YEAR-MISMATCH     the item names a year far from the record's
  ARXIV-MISMATCH    the item links an arXiv id the record does not carry
  UNRESOLVED-REF    the ref does not exist in any canonical record
"""

from __future__ import annotations

import argparse
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent

ARXIV = re.compile(r"arxiv\.org/(?:abs|pdf)/(\d{4}\.\d{4,5})", re.I)
# Venue as authors write it in news: **ICSE-NIER'25**, ASEE 2024, JSS'21
VENUE = re.compile(r"\*\*([A-Za-z][A-Za-z0-9&/+._ -]{1,40})\*\*|"
                   r"\b([A-Z][A-Za-z0-9&/+.-]{1,24})['’](\d{2})\b")
YEAR = re.compile(r"\b(20\d{2})\b|['’](\d{2})\b")


def squash(s: str) -> str:
    return re.sub(r"[^a-z0-9]", "", (s or "").lower())


def venues_in(text: str) -> list[str]:
    out = []
    for m in VENUE.finditer(text):
        out.append((m.group(1) or m.group(2) or "").strip())
    return [v for v in out if v]


def years_in(text: str) -> set[int]:
    ys = set()
    for m in YEAR.finditer(text):
        if m.group(1):
            ys.add(int(m.group(1)))
        elif m.group(2):
            ys.add(2000 + int(m.group(2)))
    return ys


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--strict", action="store_true")
    ap.add_argument("--show", action="store_true", help="print each verified-good ref too")
    args = ap.parse_args(argv)

    import yaml
    news = yaml.safe_load((ROOT / "data/news.yaml").read_text())["news"]
    pubs = {p["id"]: p for p in
            yaml.safe_load((ROOT / "data/publications.yaml").read_text())["publications"]}
    grants = {g["id"]: g for g in
              yaml.safe_load((ROOT / "data/funding.yaml").read_text())["grants"]}
    awards = {a["id"]: a for cat in
              yaml.safe_load((ROOT / "data/awards.yaml").read_text())["awards"].values()
              for a in cat}

    errors: list[tuple[str, str]] = []
    ok = 0

    # --- duplicate refs: one item announces one work -------------------------
    seen: dict[str, list[str]] = {}
    for it in news:
        for r in ([it["ref"]] if it.get("ref") else it.get("refs") or []):
            seen.setdefault(r, []).append((it.get("original") or it.get("text", ""))[:70])
    for r, uses in seen.items():
        if len(uses) > 1:
            errors.append(("DUPLICATE-REF", f"{r} claimed by {len(uses)} items: " +
                           " | ".join(u[:44] for u in uses[:3])))

    # --- per-item evidence checks -------------------------------------------
    for it in news:
        refs = ([it["ref"]] if it.get("ref") else []) + (it.get("refs") or [])
        if not refs:
            continue
        orig = it.get("original") or ""
        for r in refs:
            rec = pubs.get(r) or grants.get(r) or awards.get(r)
            if rec is None:
                errors.append(("UNRESOLVED-REF", f"{r} matches no canonical record"))
                continue

            if r in pubs:
                pv = squash(rec.get("venue"))
                named = venues_in(orig)
                if named and pv:
                    roots = [squash(v.split()[0].split("-")[0]) for v in named if v]
                    if roots and not any(x and x in pv for x in roots):
                        errors.append(("VENUE-MISMATCH",
                                       f"{r}: item names {named[:2]}, record venue "
                                       f"{(rec.get('venue') or '')[:46]!r}"))
                        continue
                ys, ry = years_in(orig), rec.get("year")
                if ys and ry and min(abs(y - ry) for y in ys) > 1:
                    errors.append(("YEAR-MISMATCH",
                                   f"{r}: item names {sorted(ys)}, record year {ry}"))
                    continue
                aid = ARXIV.search(orig)
                if aid:
                    links = " ".join((rec.get("links") or {}).values())
                    if "arxiv" in links.lower() and aid.group(1) not in links:
                        errors.append(("ARXIV-MISMATCH",
                                       f"{r}: item links arXiv {aid.group(1)}, "
                                       f"record has a different id"))
                        continue
            ok += 1
            if args.show:
                print(f"  ok  {r:<6} {orig[:76]}")

    print(f"\n== news ref consistency ==\n")
    if errors:
        by_kind: dict[str, list[str]] = {}
        for kind, detail in errors:
            by_kind.setdefault(kind, []).append(detail)
        for kind, items in sorted(by_kind.items()):
            print(f"  ---- {kind} ({len(items)}) ----")
            for d in items:
                print(f"    {d}")
            print()
    refd = sum(1 for it in news if it.get("ref") or it.get("refs"))
    print(f"  {refd} refd items · {ok} refs verified against their record · "
          f"{len(errors)} problem(s)")
    return 1 if (errors and args.strict) else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
