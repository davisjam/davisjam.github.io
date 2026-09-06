#!/usr/bin/env python3
"""axe-core accessibility scan over every published page.

    python3 checks/a11y.py              # every page, desktop + mobile
    python3 checks/a11y.py --url URL    # one page
    python3 checks/a11y.py --json OUT   # machine-readable results

This site is subject to a legal accessibility obligation, so this is a gate,
not an advisory. It runs the same engine and pinned version as the MAGE site
(axe-core 4.12.1) against WCAG 2.0/2.1/2.2 A and AA, plus best practice.

WHY PLAYWRIGHT RATHER THAN SELENIUM. MAGE drives axe through
@axe-core/webdriverjs + chromedriver. axe-core is engine-agnostic -- it is a
script injected into the page -- and this repo already runs Playwright for the
layout and interaction checks. Reusing it avoids a second browser stack and a
chromedriver version that has to track Chrome. Same engine, same rules, one
fewer thing to keep in sync.

EVERY PAGE, TWO VIEWPORTS. Not a sample: the pages here are generated from
different templates and a violation in one need not appear in another. Both a
desktop and a mobile viewport are scanned because several rules are
layout-dependent -- target-size and reflow among them -- and the mobile
rendering is where this site has actually been failing.

Violations are reported grouped by rule with the worst impact first, because
fixing one rule usually fixes every instance of it at once.
"""

from __future__ import annotations

import argparse
import collections
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
SITE = ROOT / "repos/davisjam.github.io"
AXE = SITE / "node_modules/axe-core/axe.min.js"
ORIGIN = "https://davisjam.github.io"

# WCAG 2.0/2.1/2.2 A and AA, plus axe's best-practice set.
#
# best-practice was excluded at first on the argument that advice does not
# belong in a conformance gate. That was the wrong call and James said so: the
# bar is "accessible", not "provably not liable". best-practice is where
# heading order, landmark structure, region coverage and duplicate-id checks
# live -- the things that make a page navigable by screen reader rather than
# merely conformant on paper. Impact is still reported per rule, so a
# best-practice finding is visible as such and can be judged on its merits.
TAGS = ["wcag2a", "wcag2aa", "wcag21a", "wcag21aa", "wcag22aa", "best-practice"]

VIEWPORTS = [("desktop", 1440, 900), ("mobile", 375, 812)]
IMPACT_ORDER = {"critical": 0, "serious": 1, "moderate": 2, "minor": 3, None: 4}


def page_urls() -> list[str]:
    """The same permalink-derived set the layout sweep uses -- one source for
    'what pages exist', so a new page is scanned the moment it is written."""
    import yaml
    urls = [f"{ORIGIN}/"]
    for md in sorted((SITE / "_pages").glob("*.md")):
        text = md.read_text(errors="replace")
        if not text.startswith("---"):
            continue
        end = text.find("\n---", 3)
        fm = yaml.safe_load(text[3:end]) if end != -1 else None
        if not isinstance(fm, dict):
            continue
        link = fm.get("permalink")
        if not link or md.name.startswith("redirect-") or link == "/404.html":
            continue
        urls.append(f"{ORIGIN}{link}")
    urls.append(f"{ORIGIN}/publications/")
    return list(dict.fromkeys(urls))


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--url", action="append", help="scan only this page")
    ap.add_argument("--json", help="write full results here")
    args = ap.parse_args(argv)

    if not AXE.exists():
        print(f"axe-core not installed at {AXE}\n"
              f"  cd {SITE} && npm install --no-save axe-core@4.12.1")
        return 2

    from playwright.sync_api import sync_playwright
    axe_js = AXE.read_text()
    urls = args.url or page_urls()
    findings, raw = collections.defaultdict(list), []

    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        for label, w, h in VIEWPORTS:
            for url in urls:
                page = browser.new_page(viewport={"width": w, "height": h})
                try:
                    page.goto(url, wait_until="networkidle", timeout=45000)
                except Exception as exc:
                    findings["page-load"].append(
                        {"rule": "page-load", "impact": "critical", "url": url,
                         "where": label, "target": "-", "help": str(exc)[:80]})
                    page.close()
                    continue
                page.wait_for_timeout(400)
                page.add_script_tag(content=axe_js)
                res = page.evaluate(
                    "async (tags) => await axe.run(document, {runOnly: {type: 'tag', values: tags}})",
                    TAGS)
                raw.append({"url": url, "viewport": label,
                            "violations": res["violations"]})
                for v in res["violations"]:
                    for node in v["nodes"]:
                        findings[v["id"]].append({
                            "rule": v["id"], "impact": v["impact"], "url": url,
                            "where": label, "help": v["help"],
                            "target": ", ".join(str(t) for t in node["target"])[:70]})
                page.close()
        browser.close()

    if args.json:
        pathlib.Path(args.json).write_text(json.dumps(raw, indent=1))

    total = sum(len(v) for v in findings.values())
    print(f"\n== axe-core {len(urls)} page(s) x {len(VIEWPORTS)} viewports "
          f"[WCAG 2.0/2.1/2.2 A + AA + best-practice] ==\n")
    if not findings:
        print("  no violations\n")
        return 0
    for rule, hits in sorted(findings.items(),
                             key=lambda kv: (IMPACT_ORDER.get(kv[1][0]["impact"], 4), -len(kv[1]))):
        h = hits[0]
        pages = sorted({x["url"].replace(ORIGIN, "") or "/" for x in hits})
        wheres = sorted({x["where"] for x in hits})
        print(f"  {str(h['impact']).upper():9} {rule}  ({len(hits)} instance(s), {'+'.join(wheres)})")
        print(f"            {h['help']}")
        print(f"            pages: {', '.join(pages[:6])}{' …' if len(pages) > 6 else ''}")
        print(f"            e.g.   {h['target']}")
    print(f"\n  {total} violation(s) across {len(findings)} rule(s)\n")
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
