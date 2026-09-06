#!/usr/bin/env python3
"""Check that the site's outbound links still resolve.

    python3 checks/links.py            # every external link on the built site
    python3 checks/links.py --internal # also check same-origin paths

Written after a run of stale-content finds -- a CV page serving the theme's demo
text, a Publications page 26 records behind, technical reports seven versions
old. Those were all content drifting away from an authoritative source. Links
rot differently: nothing in this repo changes, and the far end disappears.

DELIBERATELY CONSERVATIVE. Only an unambiguous 404 or 410 is reported. A
timeout, a 429, or a 403 is inconclusive -- publishers rate-limit and block
robots routinely, and a checker that cries wolf about arxiv throttling is a
checker people learn to ignore. Inconclusive results are counted and shown, not
failed on.
"""

from __future__ import annotations

import argparse
import concurrent.futures
import pathlib
import re
import subprocess
import sys
import urllib.parse
from collections import defaultdict

import _sitepath

ROOT, SITE = _sitepath.ROOT, _sitepath.SITE
ORIGIN = "https://davisjam.github.io"


def status(url: str) -> tuple[str, int | None]:
    """HEAD, falling back to a ranged GET: some hosts refuse HEAD outright."""
    for args in (["-I"], ["-r", "0-0"]):
        try:
            r = subprocess.run(
                ["curl", "-sS", "-o", "/dev/null", "-w", "%{http_code}", "-L",
                 "--max-time", "25", "-A", "Mozilla/5.0 (link-check)", *args, url],
                capture_output=True, text=True, timeout=35)
            code = int((r.stdout or "0").strip() or 0)
        except Exception:
            code = 0
        if code and code not in (405, 501):
            return url, code
    return url, code


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--internal", action="store_true", help="also check same-origin paths")
    args = ap.parse_args(argv)

    seen: dict[str, set[str]] = defaultdict(set)
    for f in list((SITE / "_pages").glob("*.md")) + [SITE / "auto-publications.md"]:
        if not f.exists():
            continue
        for u in re.findall(r'(?:\]\(|href=")(https?://[^)"\s]+|/[^)"\s]*)', f.read_text()):
            u = u.rstrip(".,);")
            if u.startswith("/"):
                if not args.internal or "{{" in u:
                    continue
                u = ORIGIN + u
            if "{{" in u or "localhost" in u:
                continue
            seen[u].add(f.name)

    # Local assets: a missing or unencoded /files/... target is a broken link
    # the HTTP sweep never sees, because it only collects absolute URLs.
    local_bad = []
    for f in list((SITE / "_pages").glob("*.md")) + [SITE / "auto-publications.md"]:
        if not f.exists():
            continue
        text = f.read_text()
        paths = re.findall(r'(?:\]\(|href=")(/files/[^)"\s]+)', text)
        paths += ["/files/" + m for m in
                  re.findall(r'\{\{ site\.filesurl \}\}/([^)"\s]+)', text)]
        for rel in set(paths):
            target = SITE / urllib.parse.unquote(rel).lstrip("/")
            if not target.exists():
                local_bad.append((rel, f.name))

    urls = sorted(seen)
    print(f"\n== link check: {len(urls)} distinct links ==\n")
    dead, unclear = [], []
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as ex:
        for url, code in ex.map(status, urls):
            if code in (404, 410):
                dead.append((url, code))
            elif code == 0 or code >= 500 or code in (403, 429):
                unclear.append((url, code))

    for url, code in sorted(dead):
        print(f"  DEAD {code}  {url}")
        print(f"            on: {', '.join(sorted(seen[url]))}")
    if unclear:
        print(f"\n  {len(unclear)} inconclusive (timeout, rate-limit or robot block) "
              f"-- not treated as failures:")
        for url, code in sorted(unclear)[:10]:
            print(f"    {code or 'timeout':>7}  {url[:88]}")
    for rel, src in sorted(local_bad):
        print(f"  MISSING FILE  {rel}")
        print(f"                referenced by {src}")
    if not dead and not local_bad:
        print("  no dead links, no missing local files\n")
    return 1 if (dead or local_bad) else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
