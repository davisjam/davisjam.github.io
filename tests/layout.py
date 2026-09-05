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
  no-element-overflow  no element's box extends past the viewport
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
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
ORIGIN = "https://davisjam.github.io"

VIEWPORTS = [(320, 800), (375, 812), (768, 1024), (1024, 768),
             (1280, 800), (1440, 900), (1920, 1080), (2560, 1440)]

# Minimum columns the card grid should reach at a given width. Below 1024 one
# column is correct; above it, staying at one means a parent is capping the grid.
MIN_COLUMNS = {1024: 2, 1280: 2, 1440: 3, 1920: 3, 2560: 3}

PROBE = """() => {
  const de = document.documentElement;
  const vw = window.innerWidth;
  const offenders = [...document.querySelectorAll('body *')]
    .filter(el => el.offsetParent !== null || el.tagName === 'BODY')
    .map(el => { const r = el.getBoundingClientRect();
      return {tag: el.tagName, cls: (typeof el.className === 'string' ? el.className : ''),
              left: Math.round(r.left), right: Math.round(r.right), w: Math.round(r.width)}; })
    .filter(x => x.w > 0 && (x.left < -1 || x.right > vw + 1));

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
          offenders: offenders.slice(0, 8), columns, cardsOut, imgsOut,
          mainW: box(main), pageW: box(page), gridW: box(grid)};
}"""


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
        sites = yaml.safe_load((ROOT / "model/sites.yaml").read_text())["sites"]
        urls = [f"{ORIGIN}/", f"{ORIGIN}/research/", f"{ORIGIN}/teaching/",
                f"{ORIGIN}/service/", f"{ORIGIN}/publications/"]
        urls += [s["url"] for s in sites if s.get("profile") == "research-program"]

    shots = pathlib.Path(args.shots) if args.shots else None
    if shots:
        shots.mkdir(parents=True, exist_ok=True)

    failures: list[str] = []
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        for url in urls:
            slug = url.rstrip("/").rsplit("/", 1)[-1] or "home"
            for w, h in VIEWPORTS:
                page = browser.new_page(viewport={"width": w, "height": h})
                try:
                    page.goto(url, wait_until="networkidle", timeout=45000)
                except Exception as exc:
                    failures.append(f"{slug} @{w}: load failed ({str(exc)[:60]})")
                    page.close(); continue
                r = page.evaluate(PROBE)
                if shots:
                    page.screenshot(path=str(shots / f"{slug}-{w}x{h}.png"), full_page=True)

                if args.measure:
                    print(f"  {slug:<38} {w:>5}px  main={r['mainW']} page={r['pageW']} "
                          f"grid={r['gridW']} cols={r['columns']}")
                else:
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
