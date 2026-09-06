#!/usr/bin/env python3
"""Layout-regression check: overflow and column sanity across viewports.

    python3 checks/layout.py                      # every published page
    python3 checks/layout.py --url .../research/  # one page
    python3 checks/layout.py --measure            # diagnose the width cap
    python3 checks/layout.py --shots out/         # save screenshots

Horizontal overflow is almost never caused by the element you are looking at.
One long URL, a wide code block, an SVG with an intrinsic width, or a flex child
without min-width:0 anywhere on the page will push the document sideways. So
this runs over EVERY page rather than the one being worked on.

Per viewport it asserts:
  no-doc-overflow      documentElement.scrollWidth <= clientWidth
  no-element-overflow  no element's box extends past the viewport, unless it sits
                       inside a scrollable container (where that is the point)
  masthead-survives    the nav has height, the logo was not evicted into the
                       hidden menu, and the hamburger is tappable when it matters
  cards-in-bounds      every research card sits inside its grid container
  images-in-bounds     no card image overflows its media box
  column-count         the card grid uses a sensible number of columns for the
                       width -- catching a grid that silently stays 1-2 columns
                       on a wide display, which no overflow check would notice

Requires playwright with chromium. Read-only: it never edits the site.
"""

from __future__ import annotations

import argparse
import json
import pathlib

import _frontmatter
import _sitepath
import sys

# Both, via the shared resolver -- this module used to compute ROOT itself and
# then hardcode ROOT/"repos/davisjam.github.io", which is the exact defect
# _sitepath exists to prevent.
ROOT, SITE = _sitepath.ROOT, _sitepath.SITE
ORIGIN = "https://davisjam.github.io"

VIEWPORTS = [(320, 800), (375, 812), (768, 1024), (1024, 768),
             (1280, 800), (1440, 900), (1920, 1080), (2560, 1440)]

# Minimum columns the card grid should reach at a given width. Below 1024 one
# column is correct; above it, staying at one means a parent is capping the grid.
MIN_COLUMNS = {1024: 2, 1280: 2, 1440: 3, 1920: 3, 2560: 3}

PROBE = """() => {
  const de = document.documentElement;
  const vw = window.innerWidth;
  // An element wider than the viewport is only a DEFECT if nothing between it
  // and the document can scroll it into view. Content inside an
  // overflow-x:auto container is contained on purpose -- that is what a scroll
  // region IS. Without this, a wide table can never pass, and the check quietly
  // argues for `table{display:block}` or for cutting content, neither of which
  // this site wants. The container itself is still checked, so a scroll region
  // that is ITSELF too wide is still caught.
  const scrollable = el => {
    for (let a = el.parentElement; a && a !== document.body; a = a.parentElement) {
      const ox = getComputedStyle(a).overflowX;
      if (ox === 'auto' || ox === 'scroll') return true;
    }
    return false;
  };
  // Deliberately off-screen-until-focused: the skip link and any visually
  // hidden text sit at left:-9999px BY DESIGN. Reading that as an overflow
  // reported 112 failures the moment the skip link landed. Matched by class
  // rather than by "is far off to the left", because a genuine overflow can
  // look identical from a bounding box.
  const offscreenByDesign = el =>
    el.classList.contains('skip-link') || el.classList.contains('sr-only') ||
    !!el.closest('.skip-link, .sr-only');
  const offenders = [...document.querySelectorAll('body *')]
    .filter(el => el.offsetParent !== null || el.tagName === 'BODY')
    .filter(el => !scrollable(el))
    .filter(el => !offscreenByDesign(el))
    .map(el => { const r = el.getBoundingClientRect();
      return {tag: el.tagName, cls: (typeof el.className === 'string' ? el.className : ''),
              left: Math.round(r.left), right: Math.round(r.right), w: Math.round(r.width)}; })
    .filter(x => x.w > 0 && (x.left < -1 || x.right > vw + 1));

  // THE MASTHEAD MUST SURVIVE ITS OWN LAYOUT ALGORITHM.
  // greedy-nav evicts .visible-links' last child, recursively and without a
  // termination guard, until the remainder fit. The logo is just another <li>
  // to it, so an over-wide logo made it evict everything -- logo included --
  // leaving an empty list, a zero-height masthead, and a hamburger that was
  // present, correct and zero pixels tall. No overflow check can see that:
  // nothing overflowed, there was simply nothing left.
  const nav = document.querySelector('.greedy-nav');
  const logo = document.querySelector('.masthead__menu-logo');
  const navBtn = document.querySelector('.greedy-nav button');
  const hiddenCount = document.querySelectorAll('.greedy-nav .hidden-links > li').length;
  const masthead = nav ? {
    navH: Math.round(nav.getBoundingClientRect().height),
    logoEvicted: !!(logo && logo.closest('.hidden-links')),
    logoH: logo ? Math.round(logo.getBoundingClientRect().height) : 0,
    btnH: navBtn ? Math.round(navBtn.getBoundingClientRect().height) : 0,
    hiddenCount: hiddenCount,
  } : null;

  const grid = document.querySelector('.research-grid');
  let columns = null, cardsOut = [], imgsOut = [];
  if (grid) {
    columns = getComputedStyle(grid).gridTemplateColumns.split(' ').filter(Boolean).length;
    const gb = grid.getBoundingClientRect();
    for (const c of grid.querySelectorAll('.research-card')) {
      const r = c.getBoundingClientRect();
      if (r.left < gb.left - 1 || r.right > gb.right + 1) cardsOut.push(Math.round(r.right - gb.right));
      const img = c.querySelector('img');
      if (img) { const ir = img.getBoundingClientRect(), mr = img.parentElement.getBoundingClientRect();
        if (ir.right > mr.right + 1 || ir.bottom > mr.bottom + 1) imgsOut.push(c.querySelector('h2')?.innerText || '?'); }
    }
  }
  const main = document.querySelector('#main');
  const page = document.querySelector('.page');
  const box = el => el ? Math.round(el.getBoundingClientRect().width) : null;
  return {scrollWidth: de.scrollWidth, clientWidth: de.clientWidth, vw,
          offenders: offenders.slice(0, 8), columns, cardsOut, imgsOut, masthead,
          mainW: box(main), pageW: box(page), gridW: box(grid)};
}"""


def check_navigation(browser, failures: list[str]) -> None:
    """The navigation bar must be whole on a laptop and collapsed on a phone.

    Pinned because the margin is thin and the failure is silent. The bar's items
    total ~1413px with a programme slug expanded, against 1340px of masthead at
    1440 -- 26px of slack. The next nav label, or a longer programme name, spends
    it, and the symptom is a link quietly missing from the bar rather than
    anything that looks broken.

    The longest slug is used deliberately: it is the worst case, and the bar is
    only correct if the worst case fits.

    This also guards the reason nav-breakpoint.js exists. greedy-nav evicted
    items and could not restore them -- available space had to exceed the whole
    previous list width, never an individual item's -- so items disappeared
    permanently after any transient narrow moment during load.
    """
    url = ORIGIN + "/research/software-supply-chain/"
    probe = """() => ({h: document.querySelectorAll('.greedy-nav .hidden-links > li').length,
                       v: document.querySelectorAll('.greedy-nav .visible-links > li').length,
                       burger: document.querySelector('.greedy-nav button').classList.contains('hidden'),
                       over: document.documentElement.scrollWidth - document.documentElement.clientWidth})"""

    for w in (1440, 1512, 1920):
        page = browser.new_page(viewport={"width": w, "height": 900})
        page.goto(url, wait_until="networkidle"); page.wait_for_timeout(800)
        r = page.evaluate(probe)
        if r["h"]:
            failures.append(f"FAIL  nav @{w}: {r['h']} item(s) hidden on a laptop "
                            f"-- the bar must be whole above 1400px")
        if not r["burger"]:
            failures.append(f"FAIL  nav @{w}: hamburger shown on a laptop")
        if r["over"] > 0:
            failures.append(f"FAIL  nav @{w}: masthead overflows by {r['over']}px")
        page.close()

    for w in (375, 768, 1280):
        page = browser.new_page(viewport={"width": w, "height": 812})
        page.goto(url, wait_until="networkidle"); page.wait_for_timeout(800)
        r = page.evaluate(probe)
        if r["burger"]:
            failures.append(f"FAIL  nav @{w}: no hamburger below 1400px")
        # The logo is site identity and must never be behind the toggle: losing
        # it is how the masthead collapsed to nothing on phones before.
        if r["v"] != 1:
            failures.append(f"FAIL  nav @{w}: {r['v']} item(s) in the bar, want the logo alone")
        if r["over"] > 0:
            failures.append(f"FAIL  nav @{w}: masthead overflows by {r['over']}px")

        # The six programmes hang off a hover flyout, and a phone cannot hover.
        # They stay reachable because the collapsed menu links to /research/,
        # which lists them -- two taps rather than a nested submenu. That is a
        # deliberate choice, so it is asserted rather than assumed: without this
        # link the programmes become unreachable on a phone entirely.
        page.click(".greedy-nav button")
        page.wait_for_timeout(300)
        if not page.evaluate("() => [...document.querySelectorAll('.hidden-links a')]"
                             ".some(a => (a.getAttribute('href') || '').endsWith('/research/'))"):
            failures.append(f"FAIL  nav @{w}: collapsed menu has no link to /research/ "
                            f"-- the six programmes are unreachable without hover")
        page.close()


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--url", action="append")
    ap.add_argument("--measure", action="store_true", help="print widths, assert nothing")
    ap.add_argument("--shots", metavar="DIR")
    args = ap.parse_args(argv)

    import yaml
    from playwright.sync_api import sync_playwright

    if args.url:
        urls = args.url
    else:
        # DERIVED from the pages that actually exist, not a hand-kept list
        # (260905). The list used to be hardcoded, so adding /people/ silently
        # left it unswept while the run still reported "no overflow" -- the same
        # false-green shape as check_figures.py scanning zero figures. Reading
        # permalinks means a new page is covered the moment it is written.
        urls = [f"{ORIGIN}/"]
        # SITE, not ROOT/"repos/davisjam.github.io" -- that hardcoded path is
        # correct from the orchestrator and wrong from the copy inside the
        # site, where it resolved to a directory that does not exist. The
        # glob then yielded nothing, the sweep fell back to the home page
        # alone, and printed "no overflow" over 1 page instead of 14. Same
        # false-green shape this very comment block warns about, one line
        # below where it was written.
        for md in sorted((SITE / "_pages").glob("*.md")):
            fm = _frontmatter.load(md)
            if fm is None:
                continue
            link = fm.get("permalink")
            # Redirect stubs are inert until the old repos are deleted, and 404
            # has no layout worth asserting.
            if not link or md.name.startswith("redirect-") or link == "/404.html":
                continue
            urls.append(f"{ORIGIN}{link}")
        urls = list(dict.fromkeys(urls))

    shots = pathlib.Path(args.shots) if args.shots else None
    if shots:
        shots.mkdir(parents=True, exist_ok=True)

    failures: list[str] = []
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        check_navigation(browser, failures)
        for url in urls:
            slug = url.rstrip("/").rsplit("/", 1)[-1] or "home"
            for w, h in VIEWPORTS:
                page = browser.new_page(viewport={"width": w, "height": h})
                try:
                    page.goto(url, wait_until="networkidle", timeout=45000)
                except Exception as exc:
                    failures.append(f"{slug} @{w}: load failed ({str(exc)[:60]})")
                    page.close(); continue
                # WAIT FOR greedy-nav TO SETTLE. It evicts nav items one at a
                # time, recursively, after load -- so measuring at networkidle
                # can catch it mid-eviction and report an overflow that exists
                # for a few frames and then does not. That produced a phantom
                # failure on one page at one width, which is worse than no
                # check: it teaches you to re-run until green.
                try:
                    page.wait_for_function(
                        """() => { const d = document.documentElement;
                             const w = d.scrollWidth;
                             if (window.__lastW === w) { return ++window.__stable > 2; }
                             window.__lastW = w; window.__stable = 0; return false; }""",
                        timeout=5000)
                except Exception:
                    pass          # settled or not, measure what is there
                r = page.evaluate(PROBE)
                if shots:
                    page.screenshot(path=str(shots / f"{slug}-{w}x{h}.png"), full_page=True)

                if args.measure:
                    print(f"  {slug:<38} {w:>5}px  main={r['mainW']} page={r['pageW']} "
                          f"grid={r['gridW']} cols={r['columns']}")
                else:
                    m = r.get("masthead")
                    if m:
                        if m["navH"] < 20:
                            failures.append(f"{slug} @{w}: masthead collapsed to "
                                            f"{m['navH']}px -- nothing in it is reachable")
                        if m["logoEvicted"]:
                            failures.append(f"{slug} @{w}: the logo was evicted into the "
                                            f"hidden menu -- site identity is not a nav link")
                        if m["hiddenCount"] and m["btnH"] < 20:
                            failures.append(f"{slug} @{w}: {m['hiddenCount']} links are behind "
                                            f"a hamburger only {m['btnH']}px tall")
                    if r["scrollWidth"] > r["clientWidth"] + 1:
                        failures.append(f"{slug} @{w}: document overflows "
                                        f"({r['scrollWidth']} > {r['clientWidth']})")
                    for o in r["offenders"]:
                        failures.append(f"{slug} @{w}: <{o['tag'].lower()} class="
                                        f"{o['cls'][:30]!r}> extends to {o['right']} (vw {r['vw']})")
                    if r["cardsOut"]:
                        failures.append(f"{slug} @{w}: {len(r['cardsOut'])} card(s) outside the grid")
                    if r["imgsOut"]:
                        failures.append(f"{slug} @{w}: image overflows its media box: {r['imgsOut'][:2]}")
                    need = MIN_COLUMNS.get(w)
                    if need and r["columns"] is not None and r["columns"] < need:
                        failures.append(f"{slug} @{w}: card grid has {r['columns']} column(s), "
                                        f"expected >= {need} (a parent is capping the width)")
                page.close()
        browser.close()

    if args.measure:
        return 0
    print(f"\n== layout check: {len(urls)} page(s) x {len(VIEWPORTS)} viewports ==\n")
    if failures:
        for f in failures:
            print(f"  FAIL  {f}")
        print(f"\n  {len(failures)} problem(s)")
        return 1
    print("  no overflow; grids reach a sensible column count at every width")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
