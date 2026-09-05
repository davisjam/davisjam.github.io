# model/content-model.md — the canonical data model

`davis-web` owns the scholarly metadata. Each project site **selects and
organizes** it according to its own intellectual narrative. The canonical model
decides membership and facts; the project page decides presentation and
narrative emphasis.

---

## 1. Two standing principles

These are the rules most likely to be "optimized away" by a later cleanup pass.
They are not incidental — they encode how this portfolio differs from a
taxonomy.

### P1 — Publications are not partitioned among projects

> **A publication may contribute to multiple research programs and should appear
> on each relevant project site.**

These sites are not library shelves. They are **different narratives over a
shared research portfolio**. A paper appearing on two sites is not duplication
in the bad sense; it is reuse of one canonical record in two legitimate
contexts.

PickleBall is the worked example. It belongs on **PTM-SE**, because model
serialization and deserialization is part of treating pre-trained models as
reusable software artifacts; and on **Software Supply Chain Security**, because
malicious model artifacts are plainly a supply-chain attack surface. Neither
placement is a concession to the other.

A future agent that "cleans up the overlaps" by forcing each publication into
one project has made the portfolio worse. Do not do it.

The corollary that keeps this honest: membership is a claim about the
**research question**, not the subject matter. PeaTMOSS, Hugging Face reuse,
model naming, ONNX interoperability, model reproducibility, and model-zoo
reliability form the PTM-SE lineage. That some of them study a supply chain does
not make them part of the Software Supply Chain program — their question is
engineering PTMs as reusable software artifacts.

### P2 — Every project site acknowledges its attributable funding

> **Funding records are maintained centrally and rendered consistently across
> sites. Do not infer that a grant supported a piece of work unless that
> relationship is explicitly encoded.**

An unencoded grant→project edge is not a gap to fill by guessing. It is either a
relationship that does not exist, or one that needs a human to assert. Both
resolve the same way: leave it absent and say so.

Where a program has no attributable umbrella grant, acknowledge support at the
work level rather than manufacturing one. Failure-Aware Software Development is
currently in this position, and that is a correct state, not a defect.

---

## 2. Publication record

Canonical source: `data/publications.yaml`. Keyed on the CV's own identifiers
(`C-12`, `W-5`, `J-4`, `Pa-1`, …) so the site record and the CV stay
mutually checkable.

```yaml
- id: C-12
  type: conference          # conference | journal | workshop | magazine | book
                            # | chapter | report | poster | patent | dissertation
  title: "PickleBall: Secure Deserialization of Pickle-based Machine Learning Models"
  authors: [...]
  venue: "ACM Conference on Computer and Communications Security (CCS)"
  year: 2025

  projects: [ptm-se, software-supply-chain]     # MANY-TO-MANY. see P1.
  role_in_project:
    ptm-se: core                                 # core | application | precursor | context
    software-supply-chain: application

  program_notes:
    ptm-se: >-
      Model serialization is an artifact-integration problem: the format a model
      arrives in determines what executing it can do to you.
    software-supply-chain: >-
      Instantiates the trust question in the model-artifact ecosystem.

  links:
    paper: ...
    artifact: ...
    blog: ...
    talk: ...
    doi: ...
  awards: [distinguished-paper]
```

### `role_in_project`

The vocabulary is closed, because it drives presentation:

| Role | Meaning | Typical rendering |
|---|---|---|
| `core` | the program's own research question | in Selected Research, with a significance line |
| `application` | the program's ideas instantiated in another ecosystem | under an Applications heading |
| `precursor` | earlier work the program grew out of | in the arc or lineage, dated |
| `context` | adjacent, cited for orientation | a link, usually not a full entry |

A publication with no `projects` is not an error — it belongs to the portfolio's
breadth, surfaced through the Research page's *Other Research and Contributions*
clusters and the complete Publications page.

### Posters

Posters are carried in the canonical record and rendered on the umbrella
Publications page. **They are not surfaced on project sites for now.** This is a
presentation decision, not a data one — the records stay complete.

---

## 3. Funding record

Canonical source: `data/funding.yaml`. Keyed on the CV's `G-` identifiers.

```yaml
- id: G-1
  sponsor: US National Science Foundation
  number: "2541917"
  title: "CAREER: PTM-SEER: Software Engineering Foundations for Re-Using Pre-Trained Neural Models"
  role: PI
  start: 2026
  end: 2031
  url: https://www.nsf.gov/awardsearch/show-award/?AWD_ID=2541917
  projects: [ptm-se]        # MANY-TO-MANY, and explicit only. see P2.
```

Every project site renders a **Funding / Support** section near the bottom of
its landing page — not buried inside individual publication entries. The
orchestrator generates the formatting so acknowledgment wording is identical
across sites; each site supplies only its own selection, derived from the
`projects` edges.

Grants with no `projects` edge are real grants that simply have no asserted
program attribution. They appear on the CV and may appear on the umbrella site.
They do not appear on a project site.

---

## 4. Patents

Eight, and they get **their own visible heading** — not a footnote among
miscellaneous publications. Seven granted at IBM plus one Purdue provisional is
a record that is undersold by hiding it.

On the umbrella Research page they sit under *Other Research and Contributions*
as a distinct `Patents` subsection. "Other Research and Contributions" is the
umbrella label; **the patents themselves are never labelled "other" in the UI.**

Patents are subject to P1 like any other output. `Pa-1` — naming mismatches in
neural networks, from the model-naming research — cross-posts to **PTM-SE**,
where it is presented alongside `J-4` rather than consigned to a generic footer.

---

## 5. Research-page structure

The umbrella Research page has two tiers, and the distinction is semantic:

```text
Research
│
├── Current research programs        "these are research programs I lead"
│   ├── MAGE
│   ├── Software Engineering for Pre-Trained Models
│   ├── Software Supply Chain Security
│   ├── Embedded Software Engineering
│   ├── Failure-Aware Software Development
│   └── SafeRegex
│
└── Other Research and Contributions "my scholarship is broader than those"
    ├── Efficient ML & Computer Systems
    ├── Software Security, Reliability & Systems
    ├── Engineering Education
    └── Patents

Publications                          "here is the complete record"
```

Each program gets a large, intentional card. Each *Other* cluster gets a short
paragraph plus **two to four representative linked papers** and a "See all
publications" pointer — never a full citation list, which would recreate the
giant-list problem the redesign exists to solve.

Engineering Education is a legitimate sustained secondary thread, not a
miscellany. Name it as such.

---

## 6. Project-site structure

The five non-MAGE program sites share a structural grammar and differ in the
middle:

```text
identity / thesis
    one program-specific visual idea      (model/figures.md — only if it argues)
research agenda / intellectual arc
selected research                          role_in_project drives what appears
tools, datasets, and infrastructure
current direction
funding / support                          generated from data/funding.yaml
footer / provenance
```

**Software Supply Chain Security** additionally splits its middle into
**Foundations** and **Applications** — it has the depth to carry the
distinction, and doing so says something stronger than presenting it as "the
signing project":

- *Foundations* — what properties constitute a secure supply chain; identity,
  provenance, and signing; adoption and usability of security mechanisms;
  dependency decision-making; actor and reputation models; package-confusion
  detection.
- *Applications* — pre-trained models; embedded software; research software;
  package ecosystems; potentially agent ecosystems.

That structure is exactly what `role_in_project: core` versus `application`
encodes. The data model and the page structure are the same distinction.
