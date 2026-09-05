#!/usr/bin/env python3
"""Enrich the canonical publication record with OpenAlex identifiers.

ADDITIVE ONLY. This pass may add a DOI, an open-access PDF link, a canonical
venue string, and a citation count. It never overwrites a title, author list, or
any field already present -- publications.json won those on migration and keeps
them (James, 260904). OpenAlex titles in particular are unreliable: it returns
"P ickle B all" for PickleBall.

Results are cached in data/openalex-cache.json so re-runs are cheap and the
network is hit once per work. Delete a key from the cache to re-query it.

    python3 generators/enrich_openalex.py            # query uncached works
    python3 generators/enrich_openalex.py --report   # show matches, write nothing
    python3 generators/enrich_openalex.py --refresh  # re-query everything

Uses curl rather than urllib: macOS system Python does not read the system
certificate store and fails CERTIFICATE_VERIFY_FAILED against HTTPS APIs.
"""

from __future__ import annotations

import argparse
import difflib
import json
import pathlib
import re
import subprocess
import sys
import urllib.parse

ROOT = ROOT = pathlib.Path(__file__).resolve().parent.parent
EXTRACT = ROOT / "data/cv-extract.json"
CACHE = ROOT / "data/openalex-cache.json"
MAILTO = "davisjam@purdue.edu"          # polite pool: faster, higher rate limit

# Types OpenAlex will not have, or where a match would be noise.
SKIP_PREFIXES = ("Pa", "Ps")


def squash(s: str) -> str:
    return re.sub(r"[^a-z0-9]", "", s.lower())


def query(title: str) -> list[dict]:
    url = ("https://api.openalex.org/works?per-page=5&mailto=" + MAILTO
           + "&search=" + urllib.parse.quote(title[:250]))
    r = subprocess.run(["curl", "-s", "--max-time", "25", url],
                       capture_output=True, text=True)
    if r.returncode != 0:
        return []
    try:
        return json.loads(r.stdout).get("results", [])
    except json.JSONDecodeError:
        return []


def best_match(title: str, year: int | None, results: list[dict]) -> tuple[dict | None, float]:
    t = squash(title)
    best, score = None, 0.0
    for w in results:
        wt = squash(w.get("title") or "")
        if not wt:
            continue
        s = difflib.SequenceMatcher(None, t, wt).ratio()
        if year and w.get("publication_year"):
            # a year within one is common (preprint vs proceedings); further is suspect
            if abs(int(w["publication_year"]) - int(year)) > 1:
                s -= 0.15
        if s > score:
            best, score = w, s
    return best, score


def distill(w: dict) -> dict:
    loc = w.get("primary_location") or {}
    src = loc.get("source") or {}
    oa = w.get("best_oa_location") or {}
    out = {
        "openalex_id": w.get("id"),
        "doi": (w.get("doi") or "").replace("https://doi.org/", "") or None,
        "venue_openalex": src.get("display_name"),
        "oa_pdf": oa.get("pdf_url"),
        "cited_by_count": w.get("cited_by_count"),
        "year_openalex": w.get("publication_year"),
    }
    return {k: v for k, v in out.items() if v not in (None, "")}


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--report", action="store_true", help="print matches, write nothing")
    ap.add_argument("--refresh", action="store_true", help="re-query even cached works")
    ap.add_argument("--limit", type=int, default=0, help="stop after N queries (for testing)")
    ap.add_argument("--threshold", type=float, default=0.82,
                    help="minimum title similarity to accept a match (default 0.82)")
    args = ap.parse_args(argv)

    cv = json.loads(EXTRACT.read_text())
    cache = json.loads(CACHE.read_text()) if CACHE.exists() else {}

    todo = [k for k in cv
            if not k.startswith(SKIP_PREFIXES)
            and (args.refresh or k not in cache)]
    print(f"{len(cv)} works; {len(todo)} to query "
          f"({len(cache)} cached, {sum(1 for k in cv if k.startswith(SKIP_PREFIXES))} skipped by type)")

    hits = misses = 0
    for n, k in enumerate(todo, 1):
        if args.limit and n > args.limit:
            print(f"  stopping at --limit {args.limit}")
            break
        e = cv[k]
        pj = e.get("pj") or {}
        title = pj.get("title") or e.get("title") or ""
        if not title:
            cache[k] = {"_status": "no-title"}
            continue
        w, score = best_match(title, pj.get("year"), query(title))

        # Retry under the alternate title. publications.json and the CV disagree
        # on several works because the CV carries a newer wording (C-41 "Are
        # Regular Expressions a Lingua Franca?" vs the older "Why Aren't ...").
        # OpenAlex indexes whichever the venue published, so try both.
        alt = e.get("title") or ""
        if (not w or score < args.threshold) and alt and squash(alt) != squash(title):
            w2, s2 = best_match(alt, pj.get("year"), query(alt))
            if s2 > score:
                w, score = w2, s2

        if w and score >= args.threshold:
            cache[k] = {**distill(w), "_match_score": round(score, 3)}
            hits += 1
            mark = "ok  "
        else:
            cache[k] = {"_status": "no-match", "_best_score": round(score, 3)}
            misses += 1
            mark = "MISS"
        print(f"  [{n:>3}/{len(todo)}] {mark} {k:<6} {round(score,2):<5} {title[:62]}")

    print(f"\nmatched {hits}, unmatched {misses}")
    if args.report:
        print("(--report: nothing written)")
        return 0
    CACHE.write_text(json.dumps(cache, indent=1, sort_keys=True))
    print(f"wrote {CACHE}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
