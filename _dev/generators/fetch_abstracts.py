#!/usr/bin/env python3
"""Fetch publication abstracts into data/abstracts.json.

    python3 generators/fetch_abstracts.py          # fill in whatever is missing
    python3 generators/fetch_abstracts.py --stats  # coverage report, no network

Abstracts are reference material for authoring `program_notes` -- the sentence
on each project site saying what a work contributed TO THAT PROGRAM. They are
small, so they are cached in the repository rather than re-fetched.

They are NOT published. An abstract says what a paper did; a program note says
why it mattered here. Rendering an abstract would be the wrong artifact on the
page and would read as filler.

Sources, in order of preference:
  1. Semantic Scholar batch endpoint, keyed by DOI. Free, no key, but it
     rate-limits bursts hard -- hence small batches and backoff.
  2. OpenAlex, keyed by its work id. Has a daily budget that resets at midnight
     UTC; when exhausted it returns an error object rather than results.

Both are resumable: existing entries are kept and only gaps are queried, so a
rate-limited run can simply be re-run.
"""

from __future__ import annotations

import argparse
import _paths
import json
import pathlib
import subprocess
import sys
import time

# Resolved for BOTH layouts -- these used ROOT plus a literal davis-web path,
# so they ran only from the orchestrator and would break the moment the site
# had to rebuild itself without it.
DATA, SITE = _paths.DATA, _paths.SITE
ROOT = SITE.parent          # message text only; no path is built from it
CACHE = DATA / "openalex-cache.json"
OUT = DATA / "abstracts.json"
S2 = "https://api.semanticscholar.org/graph/v1/paper/batch?fields=title,abstract"


def load() -> tuple[dict, dict]:
    oa = json.loads(CACHE.read_text()) if CACHE.exists() else {}
    have = json.loads(OUT.read_text()) if OUT.exists() else {}
    return oa, have


def s2_batch(dois: dict[str, str], keys: list[str]) -> tuple[dict, str | None]:
    payload = {"ids": [f"DOI:{dois[k]}" for k in keys]}
    r = subprocess.run(
        ["curl", "-s", "--max-time", "45", "-X", "POST", S2,
         "-H", "Content-Type: application/json", "-d", json.dumps(payload)],
        capture_output=True, text=True)
    try:
        res = json.loads(r.stdout)
    except Exception:
        return {}, "unparseable response"
    if isinstance(res, dict):
        return {}, str(res.get("message", "error"))[:70]
    out = {}
    for k, rec in zip(keys, res):
        if rec and rec.get("abstract"):
            out[k] = {"abstract": rec["abstract"], "source": "semantic-scholar",
                      "matched_title": rec.get("title")}
    return out, None


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--stats", action="store_true", help="coverage only, no network")
    ap.add_argument("--batch", type=int, default=8)
    ap.add_argument("--sleep", type=float, default=4.0)
    ap.add_argument("--rounds", type=int, default=6, help="retry passes over the gaps")
    args = ap.parse_args(argv)

    oa, have = load()
    dois = {k: v["doi"] for k, v in oa.items() if v.get("doi")}

    if args.stats:
        print(f"  works with a DOI : {len(dois)}")
        print(f"  abstracts cached : {len(have)}")
        gaps = sorted(k for k in dois if k not in have)
        print(f"  still missing    : {len(gaps)}")
        if gaps:
            print("   ", " ".join(gaps))
        return 0

    for rnd in range(1, args.rounds + 1):
        gaps = sorted(k for k in dois if k not in have)
        if not gaps:
            break
        print(f"round {rnd}: {len(gaps)} missing")
        got_any = False
        for i in range(0, len(gaps), args.batch):
            chunk = gaps[i:i + args.batch]
            got, err = s2_batch(dois, chunk)
            if err:
                print(f"   {chunk[0]}..: {err}")
                time.sleep(args.sleep * 3)
                continue
            have.update(got)
            got_any = got_any or bool(got)
            print(f"   {chunk[0]}..: +{len(got)}")
            OUT.write_text(json.dumps(have, indent=1, sort_keys=True))
            time.sleep(args.sleep)
        if not got_any:
            print("   no progress this round; backing off")
            time.sleep(20)

    OUT.write_text(json.dumps(have, indent=1, sort_keys=True))
    kb = len(OUT.read_text()) // 1024
    gaps = sorted(k for k in dois if k not in have)
    print(f"\n{len(have)} abstracts cached ({kb} KB). {len(gaps)} still missing.")
    if gaps:
        print("  " + " ".join(gaps))
        print("  Re-run to resume; both sources are rate-limited, not exhausted.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
