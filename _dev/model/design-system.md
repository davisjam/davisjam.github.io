# model/design-system.md — the shared visual language

The goal is **family resemblance, not identical sites**. A reader moving between
the personal site, MAGE, and a program site should recognize the same author,
lab, and intellectual family — without the sites reading as one template with
different nouns.

```text
same author / same lab / same intellectual family
```

not

```text
same Jekyll theme with different nouns
```

## 1. Tokens

These are the **real MAGE values**, read from
`repos/model-based-agentic-software-engineering/book-models/design-tokens.json`,
not approximations. The planning notes circulated working values (`#a54012`
accent, `#fbfaf6` page); those are superseded. Using the true tokens is what
makes the resemblance actual rather than approximate.

The accent has a name: **burnt umber**.

```css
:root {
  --paper:  #fdfcf9;  /* page background — warm, off-white */
  --panel:  #f6f4ef;  /* raised surface, callout, card */
  --ink:    #1c1917;  /* body text — near-black, warm */
  --muted:  #57534e;  /* metadata, captions, secondary */
  --rule:   #e4e0d8;  /* hairlines, dividers */
  --accent: #9a3f12;  /* burnt umber — links, emphasis, governance */
  --accent-tint: #faf1e6;
  --code-bg: #f3efe7;
}
```

Diagram semantics are a separate, narrower palette — see
[`figures.md`](figures.md) §5. Do not import diagram colours into page chrome.
The reverse also holds: a figure never uses `--accent` for a decorative box.

## 2. Type

| Role | Family | Use |
|---|---|---|
| Display | Source Serif 4 | H1, H2, program titles, thesis lines |
| Body | Source Sans 3 | body copy, navigation, metadata, dense academic content |
| Mono | IBM Plex Mono | code, identifiers, URLs shown as objects |

Scale, in px: `12 · 14 · 16 · 18 · 22 · 28 · 36 · 52`.

Display weight 600, tracking `-0.01em`. Figure text never drops below **12 px**
— the legibility floor the `figure-font-band` sensor enforces.

The serif/sans split is the single strongest family signal. Borrow MAGE's serif
display treatment for major headings; keep sans for everything dense.

## 3. Composition

- Generous whitespace. Thin rules rather than heavy card chrome.
- Paper entries read as **bibliographic and editorial**, not as ecommerce cards.
- Badges only for meaningful facts — Distinguished Paper, Best Paper, Artifact
  Evaluated. Never for decoration.
- Diagrams only when they explain the intellectual program ([`figures.md`](figures.md)).
- Restrained page width; long-form reading measure, not full-bleed.
- Responsive and accessible: real heading hierarchy, sufficient contrast,
  keyboard-navigable, meaningful alt text on every figure.

The sites should feel like **small scholarly monographs or exhibits**, not
product landing pages.

## 4. Anti-patterns

Stock photography. Generic AI, network, or security imagery. Gradient-heavy
startup aesthetics. Metrics-counter dashboards. Excessive animation. Giant
marketing heroes. Cards multiplied for visual fashion. Slogans.

## 5. Per-profile latitude

**Umbrella** (`davisjam.github.io`). Inherits the palette and type. Keeps the
black Duality Lab logo. The specific changes from the current site: cyan/teal
links become burnt umber; stark white becomes warm paper; body text becomes
warm charcoal; the pale-blue recruitment callout becomes a warm neutral or pale
rust; social icons become charcoal or rust rather than cyan. It must not look
like the MAGE homepage — MAGE is a thesis site, this is a person's portfolio.

**Rich project** (MAGE). Owns its design outright. It is the richest expression
of the family and the source the tokens were extracted from. Portfolio sync
never touches its CSS.

**Research program.** Inherits tokens, typography, spacing, footer, and the
standard link and rule treatments. Each may choose **one** distinguishing move —
a secondary accent, a structural motif, a different rhythm in the selected-works
list — so the programs have personality without drifting out of the family.
Recorded per site so the choice is deliberate:

| Site | Its one move |
|---|---|
| Embedded SE | most structural and diagrammatic of the five; the lineage figure is the centerpiece |
| FA-SDLC | flow and feedback motifs; the loop is the page's spine |
| PTMs | reuse and dependency framing throughout; deliberately *not* ML visual language |
| Supply Chains | provenance-graph motif; trust edges, never a chain |
| Regex | archival and chronological; the most typeset of the five |

## 6. Propagation

A change to the shared vocabulary — the accent, the type scale — propagates
mechanically: edit the tokens, run `./scripts/sync-all`, inspect every child
diff, commit the children, re-pin.

A change like "FA-SDLC should emphasize the failure-to-learning loop more
strongly" belongs to that site alone and never enters the shared layer.

Distinguishing these two is the orchestrator's standing job. Shared CSS is
**copied into** each child and committed there. Never link a stylesheet from a
central host: that would make one repository capable of breaking every site, and
would violate the rule that each public site is independently deployable.
