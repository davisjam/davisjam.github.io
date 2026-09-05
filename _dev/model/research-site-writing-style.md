# Davis Research Site Writing Style

Specializes the house style for public academic research pages: active actors
and strong verbs, say it once, cut qualifiers and fluffy adjectives, no
selling or crowning, anchor abstractions in concrete cases, plain words over
inflated jargon, logical rather than filler transitions.

Register: academic and discursive, but **substantially plainer and less
argumentative than the MAGE book**.

## 1. What the page answers

What problem do we study · what have we learned or built · how do the pieces
relate · where is the research · who did it and who supported it.

It does **not** need to persuade the reader that a research programme exists.
The publications establish that.

## 2. Begin with the research problem

> Modern software systems reuse components produced by many independent actors.
> This creates a trust problem: developers routinely depend on software whose
> authors, build processes, and distribution infrastructure they do not control.

not

> Software supply-chain security has emerged as one of the most pressing
> challenges facing today's increasingly interconnected software ecosystem.

The first identifies a mechanism. The second announces importance.

## 3. No institutional puffery

Banned: *research programme · research initiative · ambitious agenda ·
comprehensive · pioneering · leading · transformative · cutting-edge · holistic ·
innovative approach · critical challenge · rapidly evolving landscape · at the
forefront*. And *real-world impact* unless the concrete impact follows
immediately.

## 4. Do not narrate the page

Banned: *This page explores… · In this section, we examine… · Our research
programme consists of… · Below, we highlight… · Together, these projects
demonstrate…* Just say the thing.

## 5. Avoid taxonomic prose

An exhaustive noun list is not an explanation. A taxonomy may appear as
navigation or a figure; **prose must explain relationships**.

> Signing can establish who vouched for an artifact, but a valid signature does
> not tell a developer whether that producer is trustworthy or whether the
> dependency is appropriate in a particular system.

Now the terms have jobs.

## 6. Verbs, not abstract nouns

*Developers choose dependencies. Registries distribute packages. Signatures bind
identities to artifacts. Attackers exploit package names.* — not *dependency
decision-making involves…*, *trust establishment constitutes…*

## 7. "We" and "I", accurately

`we` for collaborative work, `I` for Davis's trajectory, role, or synthesis.
Never a manufactured collective: *The Software Supply Chains programme
believes…*

## 8. Name things

*In ConfuGuard, we use package metadata to detect package-confusion attacks.* —
not *our applied research develops novel techniques across diverse ecosystems.*

## 9. Let evidence establish importance

Never *our work has had substantial impact*; show the bibliography. Never *this
research has attracted significant support*; show the grants.

## 10. One claim per paragraph

Claim · mechanism or evidence · consequence if needed. Two or three sentences
usually suffice — but do not make every paragraph exactly three, which is its own
machine cadence.

## 11. No slogan cadence

Not *Trust is contextual. Evidence is partial.* Not *From identity to
provenance.* **Budget: at most one memorable rhetorical formulation per page,
and zero is fine.** A figure title may carry one if it names the model depicted.

## 12. No fake contrasts

*not X but Y · beyond X toward Y · from X to Y · more than X.* If a contrast
matters, explain the difference.

## 12a. House usage: "not ... nor"

A negated pair takes **nor**, not **or**.

> the unit of learning is not the incident **nor** its fix

Applies in figures, captions, and page prose alike.

## 13. Headings name subjects

Good: *Software signing and provenance · Adoption and usability · Package
confusion · Dependency decisions · Applications · Publications · Funding and
support.*

Banned: *The Challenge · Our Approach · Why It Matters · Building Trust · Ideas
in Action · The Road Ahead.* Also banned: **"The ideas, applied"** — use
`Applications`, or name the domains.

## 14. Transitions carry logic

No *Moreover / Furthermore / Additionally*. Often no transition is needed.

## 15. Do not overclaim umbrella relationships

Describe the connection; do not claim territory. A paper appearing on two sites
is legitimate; rewriting history so every overlapping paper proves the programme
always encompassed everything is not.

## 16. Bibliographic facts are data, not prose

Titles, venues, years, grants, collaborators, awards, URLs come from structured
data. Authored prose explains relationships among the facts.

## 17. Pre-merge audit

Delete every sentence that merely says the research is important. Then search
for, and justify each occurrence of: *comprehensive · innovative · cutting-edge ·
robust · transformative · critical · increasingly · landscape · ecosystem (unless
technical) · programme · initiative · holistic · multifaceted · crucial · key ·
powerful · novel · aims to · seeks to · explores · leverages · addresses the
challenge of · at scale · real-world · impact.*

Then, assuming deletion until proven useful: *not just · more than · from X to
Y · at its core · fundamentally · ultimately · together · collectively · this
work demonstrates · this research highlights.*

## 18. Target voice

> Modern software systems depend on components produced by people and
> organizations their developers may never meet. Package registries and build
> systems make that reuse inexpensive, but they also leave developers to decide
> which producers and artifacts to trust.
>
> We study the evidence available for those decisions. Some of our work examines
> identity, software signing, and provenance; other work studies whether
> developers can use those mechanisms effectively, how they assess dependencies,
> and how attackers exploit gaps in the distribution process.

Plain academic English, concrete subject, active verbs, enough technical
specificity to say something, no commentary on its own importance.

---

**Do not optimize for "designed." Optimize for "read."**
