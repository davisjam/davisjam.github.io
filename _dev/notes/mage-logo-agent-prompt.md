# Agent brief — Duality Lab logo in the MAGE site header

## Task

In `davisjam/model-based-agentic-software-engineering`, add the Duality Lab
logo to the top-left of the site header, linking to `https://davisjam.github.io/`.
A visitor on a MAGE page currently has no route to the author's homepage: the
top-left wordmark links back to the MAGE landing.

Then add two controls that keep the logo single-sourced.

## The SSOT rule — read before you edit

The logo has exactly one copy:

    repo:  davisjam/davisjam.github.io    images/logo.svg
    live:  https://davisjam.github.io/images/logo.svg
    shape: SVG, viewBox "0 0 1160 380" (~3:1 wordmark), 3.8 KB

**Reference it at `/images/logo.svg`. Do NOT copy the file into this repo.**

Both sites are served from the same GitHub Pages origin — the homepage at
`davisjam.github.io/`, this site at
`davisjam.github.io/model-based-agentic-software-engineering/` — so a
root-absolute path resolves across both. That is real single-sourcing: one
file, one deploy, no sync step. It also works at any page depth, so unlike a
vendored asset it needs no `rel_root` threading.

A vendored copy would drift the first time the logo is revised, and the drift
is invisible because a stale logo still renders perfectly. Do not create one.

Caveat to record in a comment, not to solve now: this holds only while MAGE is
served under `davisjam.github.io`. If it moves to its own domain, switch to the
absolute `https://davisjam.github.io/images/logo.svg` — still one source.

## Scope

IN scope: `catalog.py` (two header emitters + CSS), `tests/html.py`,
`tests/external.py`, and the regenerated HTML from `python3 catalog.py build`.

OUT of scope, do not touch:
  * the book chapter pages (`book/build_book.py:2957`) — a bound artifact with
    its own identity; a lab logo may not belong in its running header
  * `catalogue-views.html` (`catalog.py:3976`), the models view
    (`book-models/render_models_view.py:152`), visual aids
    (`book/build_visual_aids.py:212`)
  * anything under `agent/` (see "Report" below)

## Step 1 — landing page

`_v3_nav()`, ~line 2754. One call site (line 4492): the landing.
Add a NEW first child before the existing `v3-nav-home` link:

        '<nav class="v3-nav" aria-label="Primary">\n'
        '  <a class="v3-nav-lab" href="https://davisjam.github.io/">'
        '<img src="/images/logo.svg" alt="Duality Lab — James C. Davis" '
        'width="116" height="38"></a>\n'
        '  <a class="v3-nav-home" href="index.html">'      # unchanged below

## Step 2 — every other page

`_page()`, ~line 2102. Insert above `{crumb}`:

            f"<main>\n"
            f'<a class="v3-nav-lab v3-nav-lab--crumb" href="https://davisjam.github.io/">'
            f'<img src="/images/logo.svg" alt="Duality Lab — James C. Davis" '
            f'width="76" height="25"></a>\n'
            f"{crumb}\n{sub}{body}\n{_site_footer(rel_root)}\n</main>\n</body>\n</html>\n")

## CSS

Alongside the other `.v3-nav-*` rules (~line 2371, beside `.v3-nav-hat`):

    .v3-nav-lab { flex:0 0 auto; display:inline-flex; align-items:center; margin-right:14px; }
    .v3-nav-lab img { display:block; height:38px; width:auto; }
    .v3-nav-lab--crumb { margin: 0 0 10px; }
    .v3-nav-lab--crumb img { height: 25px; }

## Why these specifics — do not "simplify" them

  * `width`/`height` on the `<img>`: intrinsic size is 1160x380. Without them
    the browser reserves no space and the header reflows when the SVG arrives.
    116x38 and 76x25 hold the ratio.
  * Real `alt`, never `aria-hidden` or `alt=""`: this link's only content is the
    image, so the alt text IS the link's accessible name. An empty alt leaves a
    nameless link — WCAG 2.4.4 / 4.1.2 failure. (The MAGE wordmark link beside
    it may keep `aria-hidden` on its glyph because it also carries text.)
  * The alt names the DESTINATION — "Duality Lab — James C. Davis" — not the
    picture. "Logo" tells a screen-reader user nothing about where it goes.
  * A separate `<a>`, not a wrapper: two destinations need two links, and
    nesting anchors is invalid and untabbable.
  * Smaller in the crumb: the crumb is a light meta line; a 38px logo overpowers it.

## Controls — the SSOT is not real until these exist

**Tier-1, `tests/html.py`** (stdlib, always runs). Two assertions:

  1. No logo file exists anywhere in this repo — fail on any tracked path
     matching `*logo*.svg` / `*logo*.png` outside `node_modules`. This is what
     makes vendoring impossible to land rather than merely discouraged.
  2. Every generated page whose header this task touches references
     `src="/images/logo.svg"` exactly — catching both a removed logo and a
     path rewritten to a relative or vendored one.

**Tier-2, `tests/external.py`** (network; SKIP when offline, FAIL under
`--strict` — match the existing convention in that file):

  3. `https://davisjam.github.io/images/logo.svg` returns 200. The canonical
     file lives in a repo this one does not control, so a rename there breaks
     the image here silently. This is the control that catches it.

## Build and verify

    python3 catalog.py build
    grep -rl 'v3-nav-lab' --include='*.html' . | wc -l

Expected: **106**. Measured on this codebase — Step 1 alone yields 1, which is
the trap: it looks correct to anyone checking the landing page and helps nobody
arriving on a deep page. If you get 1, Step 2 did not take.

Also confirm:
  * `theory.html` shows the crumb variant directly above `<nav class="crumb">`
  * inside `<nav class="v3-nav">` on the landing, `v3-nav-lab` precedes
    `v3-nav-home` (check within the nav element — `.v3-nav-home` appears
    earlier in the CSS block, so a whole-file search gives a false negative)
  * the three new controls pass, and control 1 fails if you drop a scratch
    `logo.svg` into the repo — verify by doing exactly that, then deleting it
  * at 375px the header still wraps sanely (`.v3-nav` is already
    `flex-wrap:wrap`; the logo is `flex:0 0 auto` so it will not squash)

Commit `catalog.py`, the tests, and the regenerated HTML together — the build
touches many pages and splitting them leaves the repo inconsistent.

## Report

State the grep count you actually got, and confirm control 1 fails on a
planted copy.

Flag separately, do not fix: files under `agent/` carry a
`GENERATED by catalog.py build — DO NOT EDIT` banner but did NOT change when
`catalog.py build` ran. They come from another subcommand or are stale
artifacts of an older run. A page naming a generator that no longer
regenerates it is stale by construction — worth its own task.
