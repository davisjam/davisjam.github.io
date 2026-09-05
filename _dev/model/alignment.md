# model/alignment.md — portfolio obligations

What every site owes the portfolio, split by whether a machine can decide it.

The split is the point. A deterministic obligation belongs in a checker that
runs on every push; a qualitative one belongs in a review checklist a human
works through. Writing a qualitative obligation as if it were checkable produces
a checker that either passes everything or blocks arbitrarily.

---

## A. Machine-checkable

Enforced by `scripts/check-site` in each child (local pre-push + CI) and
aggregated by `scripts/check-portfolio` here.

### Every site

| ID | Obligation |
|---|---|
| `build` | The static site builds cleanly from a fresh checkout. |
| `base-path` | The built site's canonical URL matches `url` in `sites.yaml`. |
| `no-broken-internal-links` | Every internal link resolves to a built page or asset. |
| `no-missing-assets` | Every referenced image, stylesheet, script, and figure exists. |
| `no-dev-urls` | No `localhost`, `127.0.0.1`, or `file://` URLs in built output. |
| `metadata` | Every page has a non-empty `<title>` and description. |
| `no-placeholder` | No `TODO`, `TBD`, `Lorem ipsum`, or `XXX` in built output. |
| `pages-config` | A valid Pages deployment workflow exists and targets the site's default branch. |
| `html-well-formed` | Built HTML parses without structural errors. |

### Research-program and rich-project sites

| ID | Obligation |
|---|---|
| `identity-line` | The footer carries `A research project of James C. Davis / Duality Lab / Purdue University`. |
| `root-link` | The site links back to `https://davisjam.github.io/`. |
| `evidence-present` | The site exposes publications or artifacts — a program site with no evidence is a stub. |
| `publications-current` | The generated publication projection matches the canonical `data/publications.yaml`. |

### Figures, where a site has them

| ID | Obligation |
|---|---|
| `figure-overflow` | Text fits inside its box. |
| `figure-text-occlusion` | No opaque fill is painted over a label. |
| `figure-text-intrusion` | No text flows into a foreign box. |
| `figure-label-collision` | No connector stroke runs through a free-floating label. |
| `figure-font-band` | Figure text renders inside the legibility band (≥ 12 px). |
| `figure-dangling-edge` | Every declared edge terminates on its named endpoints. |
| `figure-edge-orthogonal` | Declared orthogonal edges route orthogonally. |
| `figure-legend-text-overflow` | A boxed label clears its box's right border. |
| `figure-family-budget` | Figure colours stay inside the semantic families. |
| `figure-alt-text` | Every figure has meaningful alt text. |

### Umbrella site only

| ID | Obligation |
|---|---|
| `research-links-all-programs` | The Research page links every `research-program` and `rich-project` site. |
| `teaching-links-mage` | The Teaching page links the MAGE book and the Teach with MAGE course mirror. |
| `publications-complete` | The Publications page contains the complete generated record. |

### Portfolio-level

| ID | Obligation |
|---|---|
| `submodules-present` | Every site in `sites.yaml` exists as a submodule at its declared path. |
| `no-dirty-children` | No child has uncommitted changes at pin time. |
| `pins-current` | Each recorded submodule SHA matches the child's checked-out commit. |
| `generated-files-fresh` | Every materialized file matches what the generator would produce. |
| `reciprocal-links` | Every child links to root; the root links to every child. |
| `no-runtime-coupling` | No child's build or CI references `davis-web`. |

`no-runtime-coupling` is the one that protects the architecture. If it ever
fails, a public site has become undeployable by anyone without access to a
private repository — fix it before anything else.

---

## B. Human-review

No checker decides these. They belong to the review pass before a site is
considered done, and to James's own review.

### Research claims

- The prose accurately represents what the work showed. No overclaiming.
- Trajectory and coherence are shown, not asserted — and the site does not
  retroactively claim that all prior work belonged to the newest named
  framework. A program site describing its lineage is honest; a program site
  annexing unrelated papers is not.
- Per-paper significance lines say what the work contributed **to this program**,
  not what its abstract says.
- Scope discipline: a paper belongs to a program when its scientific question is
  that program's question. Generic bug-finding work does not automatically
  belong to FA-SDLC.

### Composition

- Visual hierarchy is restrained and academic.
- MAGE does not dominate the umbrella site. It is one program among six, even
  though it is the most developed.
- Program pages explain an intellectual contribution rather than listing papers.
- Terminology is intelligible to a strong PhD applicant who is not in the
  subfield.
- Each figure earns its place, makes one claim, and has been *looked at* by a
  human after passing the checkers.

### The thirty-second test

Walk `PROJECT.md` §2's seven questions against the live umbrella site, from a
cold start, as each of: a Sloan reviewer, a SIGSOFT Early Career reviewer, a CRA
mentoring reviewer, a prospective PhD student, a prospective undergraduate, and
an academic collaborator. Each should reach their answer without scrolling
through material aimed at someone else.

---

## C. The MAGE exception

MAGE participates in portfolio coordination without being reduced to the common
research-site realization. Declared in `sites.yaml` under its `managed:` block.

**Applies to MAGE:**

- reciprocal identity link to James Davis / Duality Lab
- canonical URL validation
- build and publish checks
- shared provenance wording, where it fits

**Never applies to MAGE:**

- the generic research-site page skeleton
- generic paper-card layout or content density
- a generated replacement `CLAUDE.md` or alignment model
- generic shared CSS overwrite
- generic alignment generation

MAGE is the fully developed version of a major intellectual program. The other
sites intentionally contain less. When a shared change is proposed, the question
is not "does this apply to all sites?" but "does this genuinely apply to MAGE?"
— and the default answer is no.
