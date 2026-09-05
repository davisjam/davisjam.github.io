# model/figures.md — original figures for the research-program sites

Each research-program site may carry **one original, publication-quality
figure** that makes the program's central intellectual claim visible. These are
new drawings, authored for these sites. They are not decoration, not stock
imagery, and not the ASCII wireframes from the planning notes — those were
sketches of *what a figure should argue*, never artwork to reproduce.

## 1. The doctrine is MAGE's, not a new one

The house figure doctrine already exists, is battle-tested across 211 book
figures, and is authoritative here:

```text
repos/model-based-agentic-software-engineering/
  plugin/mage/skills/self-communicate/drawing/
    figures.md      curating a teaching figure — the governing line
    diagrams.md     diagram types, the d2 house path, three fidelities
    charts.md       quantitative display
    svg-audit.py    the aggregate SVG checker
```

Invoke the `self-communicate` skill when drawing. Do not re-derive its rules.
The load-bearing ones, restated only so they are not lost in a handoff:

> **A figure is a model for teaching the reader, not a rendering of the system's
> own models.** The visual target is an engineer drawing the minimum diagram
> necessary to explain one property on a whiteboard, rendered by a professional
> designer in house style.

- **Redraw everything.** Never paste tool output — no Graphviz, no generated
  UML, no screenshots of model files. A dump keeps every entity the tool
  enumerated and drops the question the figure exists to answer.
- **One job per figure.** Complete the sentence "after this figure, the reader
  understands ___." If the honest completion contains an "and," split it or cut
  the second half.
- **The removability test.** If removing an element does not weaken the claim,
  remove it. A figure earns every box and every edge.
- **Real, not complete.** Say so in the caption when the real system has more
  parts, and still give the caption an interpretive sentence — what to conclude,
  not just what is shown.

## 2. Do not draw five figures because there are five sites

**The figure has to make an intellectual claim.** Symmetry is not a claim.

A program whose story is a chronology is better served by a beautifully typeset
research chronology than by a manufactured conceptual diagram. Regular
Expression Engineering is the live candidate for this: its maturity *is* the
argument, and a timeline states it more honestly than a box-and-arrow model
would.

Before drawing anything for a site, answer in one sentence: *what does spatial
arrangement say here that prose cannot?* If there is no answer, do not draw. A
site with strong prose and no figure is finished; a site with a decorative
figure is not.

## 3. The claim each site's figure must earn

Recorded in `model/sites.yaml` under each site's `figure:` key, and restated
here with the argument each one is responsible for.

| Site | Figure | The claim it must make |
|---|---|---|
| Embedded SE | `research-lineage` | Unit Proofing is the culmination of a sustained lineage — validation → rehosting → scalable analysis → compositional proof → Unit Proofing / AutoSOUP — not a disconnected new brand. |
| FA-SDLC | `failure-learning-loop` | Failure knowledge is a *feedback system* — failure → evidence → analysis → reusable knowledge → engineering structure → subsequent outcomes feeding back — not a bug database. |
| PTMs | `ptm-reuse-lifecycle` | A reused model carries compatibility and trust obligations *crossing* select → integrate → validate → evolve. This is reuse and dependency engineering, not "AI". |
| Supply Chains | `trust-provenance-graph` | Trust is a graph of evidence among actors, artifacts, dependencies, and consuming contexts. Signing is one edge, not the whole problem. |
| Regex | `research-arc` | One artifact class, examined along three axes — reuse/portability, human understanding, execution/security — reached conclusions that motivated the later reuse and assurance work. |

Two anti-patterns are called out because they are the obvious wrong answers:

- **Supply Chains must not draw a literal chain.** Trust edges and provenance
  paths are intellectually accurate; a chain icon is a pun.
- **PTMs must not draw a neural network.** No layered-node clichés, no glowing
  brains. The subject is dependency and reuse engineering; it should look like
  it.

Also avoid, portfolio-wide: stock photography, generic AI/network/security
imagery, gradient-heavy startup aesthetics, metrics-counter dashboards, and any
animation.

## 3a. Name the mechanism, not the category

**Do not label a conceptual figure with category words when the figure can state
the mechanism.** "Evidence", "Analysis", "Knowledge", "Engineering" are
categories. A pipeline of them says only that learning involves learning.

The useful content is what evidence *contains*, what analysis *asks*, what
knowledge *results*, and how that knowledge *changes* engineering:

```text
BAD     Failure -> Evidence -> Analysis -> Knowledge -> Engineering

BETTER  Failure           An assumption fails in practice
          | preserve what happened
        Evidence          Reports, artifacts, decisions, consequences
          | compare and explain
        Failure mechanism Which assumption failed, under what conditions?
          | generalize beyond the incident
        Engineering       A reusable claim about how systems fail
        knowledge
          | institutionalize
        Engineering       Requirements, design, analysis, validation,
        change            process, governance
          `-> changes the conditions under which the next system is built
```

The second leaves the reader knowing something. Edge labels carry the
transformations; boxes carry the content.

A useful diagnostic: **if the external caption is better than the figure, the
figure is not doing its job.** When that happens, move the caption's proposition
into the figure and let the caption become conventional.

## 4. The reuse boundary

**The vocabulary is shared; the figures are not.** Design tokens, the checkers,
and the house conventions live in the orchestrator. Every figure's *source*
belongs to the project whose argument it makes.

```text
davis-web/
  templates/figures/          shared drawing vocabulary + checkers
    design-tokens.json          palette, type scale, figure semantics
    design_tokens.py            projector: CSS :root, SVG palette, mermaid theme
    glyph-advances.json         font metrics (no TTFs needed)
    check_figures.py            the aggregate checker, path-parameterized
    lint_figure_*.py            the nine sensors
    _house-style.d2             d2 class include, for the declarative path
    HOUSE-RULES.md              condensed conventions + how to run the checks

repos/embedded-software-engineering/
  figures/
    research-lineage.svg        the figure — authored here, owned here
    research-lineage.d2         its source, if the d2 path fits
```

This follows the portfolio rule everywhere else: the orchestrator owns the
template, each child holds a committed working copy. A site's figure check runs
from the child repo with no reference to `davis-web`.

**Extract the vocabulary, not the book build.** MAGE's figure system is
partly coupled to its own manuscript — `catalog.py` orchestration, caption
tiers, Typst projection, the "8 redrawn figures" scoping in the family-budget
lint. None of that comes across. What comes across is the engineering
vocabulary: the tokens, the semantic colour language, the glyph-width model, and
the nine sensors, each parameterized by scan root instead of hardcoding
`book/assets/`.

## 5. The semantic colour language

Colour carries meaning in this family. An author picks a colour **by role**,
never by hex. The roles come from MAGE's `figure_semantics` and are preserved so
that a reader who has seen a MAGE figure reads these correctly on sight:

Exactly **five** families, and the header must name them exactly:

| Family | Meaning | Stroke |
|---|---|---|
| `modeling` | the model, the governed thing, established evidence | green `#1f7a4d` |
| `governance` | authority, decision, the accent | rust `#9a3f12` |
| `agent` | the acting party | blue `#2f5169` |
| `failure` | failure, defect, waste, what is absent | red `#b23b3b` |
| `neutral` | structure, panels, surrounding machinery | gray `#57534e` |

`trust` and `churn` are NOT families -- an easy and costly mistake, since a
figure using them silently falls outside the colour budget.

Dashed strokes mean *derived or conjectural*, never *unimportant*.

Programs adapt roles to their own subject — `failure` is the failure node on the
FA-SDLC loop and the evidence gap on the supply-chain graph; `modeling` is
established evidence in one figure and reusable knowledge in another — but they
do not invent a sixth family or restate a hex.

## 6. The loop

```text
recover the claim          what must the reader understand after this figure?
        ↓
pre-layout plan            inventory items; classify every one; choose the construct
        ↓
draw                       d2 (declarative) or hand-authored SVG, house style
        ↓
check                      python3 figures/check_figures.py figures/
        ↓
look                       render it and actually look; the checkers are sensors,
                           not judges of whether the argument lands
```

The checkers catch text overflowing its box, labels occluded by later fills,
text intruding into a foreign box, strokes running through free labels,
sub-legible type, dangling edges, non-orthogonal routing where orthogonal was
declared, and colour-family drift. They cannot tell you the figure is making the
wrong argument. That judgment stays with the author, and the figure is not done
until someone has looked at it.
