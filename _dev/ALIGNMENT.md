# ALIGNMENT.md — the website as a MAGE realization

The website is a **realization of authoritative models** kept in `davis-web`.
The models are not convenient data for generating pages. They are the authority
the realization is checked against.

```text
                     AUTHORITATIVE MODELS
       ┌────────────────────┼────────────────────┐
 scholarly model       portfolio model      structure model
 pubs · grants ·       projects ·           claims per programme ·
 patents · service     relationships        figure labels · sections
       └────────────────────┼────────────────────┘
                     style models  (design + writing)
                            ▼
                       REALIZATION
          davisjam.github.io  (one canonical site)
                            ▼
                    ALIGNMENT ENGINE
              rejects non-aligned changes
```

**Post-consolidation.** The programme pages live in `davisjam.github.io` at
`/research/<slug>/`; MAGE keeps its separate body-of-knowledge site. The six
standalone project sites are marked `site_status: retired` in `sites.yaml`, and
the families that validate a *standalone site* skip them. STRUCT and the figure
sensors still read those repos, because the authored figures live there until
the repos are deleted.

> **Do not merely test that the site builds. Test that the built site remains
> aligned with the models from which it is supposed to derive.**

## The engine

```bash
python3 checks/alignment.py            # 48 obligations, 15 families
python3 checks/alignment.py --list     # the register: statement + evidence
python3 checks/alignment.py --family FUND --errors-only
python3 checks/alignment.py --json report.json
```

Each check declares the **obligation** it establishes, the **evidence** it
reads, and a **result** — not a bare assertion:

```text
OBL-PORTFOLIO-001
  Every active research project has exactly one entry on the root Research page.
  Evidence: model/sites.yaml · repos/davisjam.github.io/_pages/research.md
  Result:   PASS
```

## Severity

| | Meaning | Blocks? |
|---|---|---|
| **ERROR** | the realization *contradicts* the authority — wrong publication facts, an unmodeled funding claim, a missing required project, a broken canonical URL, a hand-edited generated record | yes |
| **WARNING** | likely violates the design or writing model — puffery, a banned component, prose too wide | no |
| **ADVISORY** | worth a human look — a page grown very long, two sections that read repetitively | no |

Keeping WARNING non-blocking is deliberate. A gate that blocks on style becomes
a bureaucracy agents learn to game, and then the ERRORs stop being read.

## Families

| Family | Establishes |
|---|---|
| `STRUCT` | section headings appear on their page; every `figure_label` appears in that figure; every publication is placed under exactly one section |
| `LINK` | a named paper's title links to a readable copy, resolved from one canonical `paper_url`; hosted PDFs exist; no page builds its own link |
| `SCHOLARLY` | rendered publications == modeled membership, both directions, titles exact |
| `FUND` | a funding claim appears **only** where the model asserts the edge, and every asserted edge appears |
| `PORTFOLIO` | exactly the modeled projects on the Research page, named as modeled |
| `ROUTE` | canonical URLs, no root-relative assets, resolving links and fragments, navigation stays on-origin |
| `SHELL` | the common Davis academic header, and a return to Research |
| `SECTION` | declared `required_sections` exist, are unique, appear in jump nav, are non-empty |
| `DESIGN` | one H1, no institutional eyebrow, no authorship re-announcement |
| `PROSE` | banned institutional language; discouraged vocabulary; self-narration |
| `A11Y` | lang, alt text, heading hierarchy, figure captions, SVG title/desc |
| `SEO` | unique titles carrying the author name, description, OpenGraph, no noindex |
| `PROV` | generated collections come from the generator; assets declare provenance |
| `CROSS` | a cross-listed work renders identical facts and a *different* note per site |
| `RECORD` | enumerative records are projections; no obsolete course numbers |

## The drift class STRUCT closes

A programme's regions are named in three places: the figure, the page headings,
and the research card. Left to prose, they drift — a region becomes "Identity &
provenance" in the figure, "Software signing" in the body, and "Producer trust"
on the card six months later, and nothing notices.

`figure_label` in `data/program-structure.yaml` is the single string, and
`OBL-STRUCT-002` asserts it appears in that programme's figure. The figure
becomes a map of the page rather than an illustration above it.

## Two obligations worth reading twice

**Funding is the hardest gate**, because accidental attribution is
substantively bad. `OBL-FUND-001` and `-003` fail if a site names a sponsor
without a modeled edge. Nothing infers funding from shared authors, topic
similarity, dates, or acknowledgments.

**`OBL-PORTFOLIO-001` fixes the project set.** It would catch a future
accidental resurrection of "Unit Proofing" as a seventh peer programme rather
than a thrust inside Embedded Software Engineering — and it catches silent
renaming, so no agent turns *Software Supply Chains* into *Software Supply Chain
Security Initiative*.

## Pre-push versus CI

| Pre-push (fast, in the child repo) | CI / portfolio (expensive) |
|---|---|
| figure sensors | everything at left |
| HTML and metadata basics | full alignment engine, all families |
| resolving internal links | cross-repo integration |
| generated-provenance headers | external link crawl |
| | rendered screenshots, visual regression |
| | semantic style review |
| | production URL smoke test |

Pre-push must stay fast enough that no agent can rationalize bypassing it.

## Not yet mechanized

Recorded so the gaps are deliberate, not forgotten:

- **People alignment** — no `data/people.yaml` yet, so current-versus-alumni and
  role agreement across pages are unchecked.
- **Claim-to-model alignment** — extracting factual claims from authored prose
  and classifying them (model-derived / evidence-backed / volatile /
  interpretive) against the funding and publication graphs.
- **Freshness** — volatile facts need `as_of` metadata and an age limit. This is
  exactly the failure the old Service page had: technically true, quietly stale.
- **Semantic style review** — an LLM critic reporting passages that sell, pile
  abstract nouns, or substitute taxonomy for explanation. It must **report, not
  rewrite**; otherwise the validator becomes another authoring agent.
- **Rendered visual checks** — screenshots at desktop and mobile widths, then
  regression against approved baselines. Syntactically valid HTML can still be
  visibly wrong.
