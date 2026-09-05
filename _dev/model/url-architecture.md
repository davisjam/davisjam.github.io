# model/url-architecture.md — public URL architecture

> **The repository boundary must not become a public URL boundary.**

This is a headline rule of the portfolio, not a deployment detail. It explains
both what to build and why the orchestration exists at all.

A visitor should never need to know which GitHub repository owns a page.
Separate project repositories are **source and development** boundaries;
`davisjam.github.io` is the **publication and URL** boundary.

## 1. The public namespace

```text
davisjam.github.io/
├── research/
├── publications/
├── teaching/
├── service/
├── about/
│
├── mage/
├── model-based-agentic-software-engineering/
├── software-engineering-pre-trained-models/
├── software-supply-chains/
├── embedded-software-engineering/
├── failure-aware-software-development/
└── regular-expression-engineering/
```

Each research program is reached by a stable, descriptive slug — **the
repository name**. Those names are canonical on GitHub and are what GitHub Pages
serves; the short `project_id` keys used inside `data/*.yaml` (`ptm-se`,
`embedded-swe`, …) are internal join keys, **not URLs**.

## 2. Acceptance criterion

> Starting from `davisjam.github.io`, a user must be able to navigate into every
> research-program site while remaining under the `davisjam.github.io` origin.
> Directly loading any canonical project URL must work, including nested pages
> and assets.

`checks/check-url-architecture` enforces the mechanical part of this.

## 3. How GitHub Pages actually serves these

A load-bearing fact, because it determines how much machinery this rule needs.

For the user `davisjam`, **every** repository with Pages enabled publishes to
`https://davisjam.github.io/<repo-name>/`. Only a repository named
`davisjam.github.io` publishes at the root. Project sites are therefore already
**same-origin subpaths** — not separate web properties, and not a different
origin.

So the risk this rule guards against is narrower than it first appears. Separate
repositories do not fragment the origin or scatter search visibility across
properties. What they do determine is the **slug**: repo `foo` is served at
`/foo/`, full stop.

That yields two ways to satisfy the namespace above:

**A. Name the repository what the URL should be.** Rename each repo to its
desired slug. Pages then serves it at exactly the right path, same origin, and
each repo keeps its own independent build and deploy. No assembly step exists,
so no assembly step can break.

**B. Assemble into one deployed tree.** `davis-web` builds each child and
composes the outputs into the `davisjam.github.io` repository at the assigned
prefixes; one Pages deployment serves everything.

**A is preferred, and is what this model specifies**, because it achieves the
required namespace with strictly less machinery. B is required only for paths
that do *not* correspond to a single repository — see §5.

The cost of B is real and worth naming: it makes the child repos no longer
independently publishable, which contradicts the standing architecture rule that
every public site can be cloned, built, and deployed by someone with no access
to the private orchestrator. Adopt B only where A genuinely cannot serve.

## 4. Slug assignment

**The repository name is canonical, and the slug follows it.** These repos exist
on GitHub under these names; Pages serves each at `/<repo-name>/`, so the
namespace in §1 holds with no renames and no assembly.

| project_id (internal) | repository = slug |
|---|---|
| `mage` | `/mage/` |
| `ptm-se` | `/software-engineering-pre-trained-models/` |
| `software-supply-chain` | `/software-supply-chains/` |
| `embedded-swe` | `/embedded-software-engineering/` |
| `failure-aware-sdlc` | `/failure-aware-software-development/` |
| `saferegex` | `/regular-expression-engineering/` |

Do not conflate the two columns. `project_id` is a short internal key for
`projects:` edges in `data/publications.yaml` and `data/funding.yaml`. Changing
a `project_id` touches data joins; changing a repository name changes a
**public, citable URL** and must not happen once a URL is in an application
packet.

## 5. MAGE nesting — RESOLVED

The desired tree sketched `mage/{research,book,course}`. **Decided (James,
260904): the canonical resource site keeps everything important at
`/model-based-agentic-software-engineering/`, and `/mage/` is a thin wrapper
that matches the other research-program sites and links into it.**

So `/mage/book/` and `/mage/course/` are NOT created. No path needs content from
a repository other than its own, which means **option A alone satisfies the
entire namespace** and no assembly pipeline is required. Every site stays
independently buildable and publishable.

This also protects the canonical site: its published URLs do not move, and the
agent developing it is unaffected by portfolio work.

## 5a. Historical note — the one place A would not have reached

The desired tree nests the MAGE resources under the research slug:

```text
mage/
├── research/
├── book/
└── course/
```

`/mage/book/` and `/mage/course/` come from a *different* repository than
`/mage/`. No repository-naming scheme produces that, so it needs either an
assembly step (B) for the `mage` subtree, or a decision to leave the canonical
MAGE resource site at its own slug.

Superseded by §5. Retained because it records why the question mattered:

- The canonical site is under active development by another agent, and this
  portfolio's standing rule is not to modify its structure as ordinary work.
- Its current URLs are already published and cross-referenced — the book PDF
  URL alone appears 122 times inside the MAGE repository.
- Award-packet URLs should not move after submission.

That is exactly the resolution reached, for those reasons.

## 6. Base-path awareness

Every site is mounted at a prefix, never at `/`. Project code must not assume
otherwise. Path-sensitive things that must all work under the assigned prefix:

- internal links and navigation
- CSS, JavaScript, images, fonts
- generated assets and publication projections
- `<link rel="canonical">`
- sitemap entries
- OpenGraph and Twitter-card URLs
- feed URLs

In Jekyll, this means every path goes through `{{ site.baseurl }}` or
`relative_url`, and `_config.yml` declares the `baseurl` matching the slug. A
hardcoded leading-slash path is a defect: it resolves to the umbrella site and
silently 404s or, worse, loads the wrong page.

## 7. Cross-project links

Cross-project links use the canonical namespace — `/embedded-swe/...`, never a
`github.com` URL and never a separately deployed preview URL. A MAGE page
referring to Unit Proofing points into `/embedded-swe/`.

## 8. Search metadata

Each page's canonical URL identifies its location under `davisjam.github.io`, so
the collection accrues search visibility to the Davis academic site as one
property rather than fragmenting it.

The descriptive slugs also read well out of context: a reviewer seeing
`davisjam.github.io/software-supply-chains/` in a packet knows what it is
before clicking.

## 9. Preview deployments

A child repository may deploy independently for preview or testing. Such a
deployment is explicitly **not canonical**: it must not be linked from the
portfolio, must not appear in sitemaps, and must not be given as a citable URL.
