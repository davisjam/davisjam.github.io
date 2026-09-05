#!/usr/bin/env python3
"""Behaviour and contrast checks for the published site.

    python3 checks/interaction.py

WHY THIS EXISTS (260905). The research-programme flyout was reported as "no
hover or anything". The markup was correct, the JavaScript worked, and the CSS
was present -- the chevron was simply `#CEB888` (Boilermaker Gold), which is
1.94:1 against white. It was rendering perfectly and could not be seen.

That is the useful lesson about what to test. An interaction test asserts the
MECHANISM: does the button toggle, does the menu appear, does Escape close it.
It would not have caught this, because the mechanism was never broken. Only a
CONTRAST assertion catches "correct but invisible".

So this runs both:

  flyout     the programme menu opens, closes, and exposes its state correctly
  contrast   every text node meets WCAG 2.1 AA against its effective background
             (4.5:1 normal, 3:1 for large text)

Contrast is the reason this file is worth more than its length. The site belongs
to an accessibility researcher; shipping a 1.94:1 control is the kind of thing
the site should catch on itself.
"""

from __future__ import annotations

import argparse
import sys

ORIGIN = "https://davisjam.github.io"

# Walk up for the first non-transparent background, then score every text node.
# Large text is >=24px, or >=18.66px when bold (WCAG 2.1 definition).
CONTRAST = """() => {
  const lum = c => {
    const [r,g,b] = c.map(v => { v /= 255;
      return v <= 0.03928 ? v/12.92 : Math.pow((v+0.055)/1.055, 2.4); });
    return 0.2126*r + 0.7152*g + 0.0722*b;
  };
  const parse = s => {
    const m = (s||'').match(/rgba?\\(([^)]+)\\)/); if (!m) return null;
    const p = m[1].split(',').map(x => parseFloat(x.trim()));
    return {rgb: p.slice(0,3), a: p.length > 3 ? p[3] : 1};
  };
  const bgOf = el => {
    for (let a = el; a; a = a.parentElement) {
      const c = parse(getComputedStyle(a).backgroundColor);
      if (c && c.a > 0.05) return c.rgb;
    }
    return [255,255,255];
  };
  const out = [];
  for (const el of document.querySelectorAll('body *')) {
    if (el.offsetParent === null && getComputedStyle(el).position !== 'fixed') continue;
    const text = [...el.childNodes]
      .filter(n => n.nodeType === 3).map(n => n.textContent.trim()).join('');
    if (!text) continue;
    const cs = getComputedStyle(el);
    if (cs.visibility === 'hidden' || parseFloat(cs.opacity) < 0.1) continue;
    const fg = parse(cs.color); if (!fg) continue;
    const size = parseFloat(cs.fontSize);
    const weight = parseInt(cs.fontWeight, 10) || 400;
    const large = size >= 24 || (size >= 18.66 && weight >= 700);
    const l1 = lum(fg.rgb), l2 = lum(bgOf(el));
    const ratio = (Math.max(l1,l2) + 0.05) / (Math.min(l1,l2) + 0.05);
    const need = large ? 3.0 : 4.5;
    if (ratio + 0.005 < need) {
      out.push({tag: el.tagName.toLowerCase(),
                cls: (typeof el.className === 'string' ? el.className : '').slice(0,32),
                text: text.slice(0, 40), color: cs.color,
                size: Math.round(size), ratio: Math.round(ratio*100)/100, need});
    }
  }
  // De-duplicate: one report per (class, colour) rather than per element.
  const seen = new Set();
  return out.filter(o => { const k = o.cls + o.color + o.tag;
    if (seen.has(k)) return false; seen.add(k); return true; });
}"""


def check_flyout(page, failures: list[str]) -> None:
    btn = page.query_selector(".rps__btn")
    if btn is None:
        failures.append("flyout: no .rps__btn in the masthead")
        return
    if btn.get_attribute("aria-expanded") != "false":
        failures.append("flyout: button does not start with aria-expanded=false")
    if page.query_selector(".rps__menu").is_visible():
        failures.append("flyout: menu is visible before the button is pressed")

    # Short timeout, and never let one broken control abort the whole run --
    # the first version of this file raised on an invisible button and took the
    # contrast sweep down with it, which hid every other finding on the site.
    try:
        btn.click(timeout=3000)
    except Exception as exc:
        failures.append(f"flyout: button is not clickable — {type(exc).__name__}: "
                        f"{str(exc).splitlines()[0][:80]}")
        return
    page.wait_for_timeout(120)
    if btn.get_attribute("aria-expanded") != "true":
        failures.append("flyout: aria-expanded did not become true on click")
    if not page.query_selector(".rps__menu").is_visible():
        failures.append("flyout: menu did not open on click")

    n = len(page.query_selector_all(".rps__menu a"))
    if n != 6:
        failures.append(f"flyout: menu lists {n} programmes, expected 6")

    page.keyboard.press("Escape")
    page.wait_for_timeout(120)
    if page.query_selector(".rps__menu").is_visible():
        failures.append("flyout: Escape did not close the menu")


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--url", action="append", help="page(s) to check")
    args = ap.parse_args(argv)
    from playwright.sync_api import sync_playwright

    urls = args.url or [f"{ORIGIN}/", f"{ORIGIN}/research/", f"{ORIGIN}/people/",
                        f"{ORIGIN}/teaching/", f"{ORIGIN}/service/",
                        f"{ORIGIN}/research/embedded-swe/"]
    failures: list[str] = []
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        for url in urls:
            slug = url.rstrip("/").rsplit("/", 1)[-1] or "home"
            page = browser.new_page(viewport={"width": 1280, "height": 900})
            page.goto(url, wait_until="networkidle", timeout=45000)

            before = len(failures)
            try:
                check_flyout(page, failures)
            except Exception as exc:
                failures.append(f"flyout: check raised {type(exc).__name__}: "
                                f"{str(exc).splitlines()[0][:80]}")
            for f in failures[before:]:
                failures[failures.index(f)] = f"{slug}: {f}"

            for o in page.evaluate(CONTRAST):
                failures.append(
                    f"{slug}: contrast {o['ratio']}:1 < {o['need']} — "
                    f"<{o['tag']} class={o['cls']!r}> {o['color']} @{o['size']}px "
                    f"— {o['text']!r}")
            page.close()
        browser.close()

    print(f"\n== interaction + contrast: {len(urls)} page(s) ==\n")
    if failures:
        for f in failures:
            print(f"  FAIL  {f}")
        print(f"\n  {len(failures)} problem(s)")
        return 1
    print("  flyout behaves; all text meets WCAG AA against its background\n")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
