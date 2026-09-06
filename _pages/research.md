---
layout: single
title: "Research"
permalink: /research/
author_profile: true
---

<!-- Enumerative sections on this page are GENERATED from the davis-web
     canonical records by generators/generate_umbrella_pages.py.
     Edit the narrative in that generator, or the facts in data/*.yaml.
     Hand edits here will be overwritten. -->

I study how to make software-intensive systems reliable and secure. My research begins
with engineering practice: I study how software is built and used, identify where existing
assumptions and engineering methods break down, and turn those findings into new methods,
tools, and ways of engineering software.

I pursue this problem from several directions: understanding how software fails in
practice; developing analysis and assurance methods that prevent failures; making
dependencies and reused components easier to understand and govern; and studying how
emerging technologies, including AI, change the way software is built and engineered.

My current research is organized around six programs.

<style>
/* The width system lives in _sass/_research.scss, keyed on :has(), so the
   landing and the programme pages share one definition.

   USE A GRID, DO NOT DRAW THE GRID (same rule as the People page).

   These were bordered cards with a rule under the title and another above the
   footer. None of those lines encoded anything: each programme already has its
   own figure, a large title and generous space around it. Removing them lets
   the signature figures -- which ARE the visual thesis of each programme --
   become the first thing the eye lands on.

   Column count emerges from available width; it is not decreed as 3x2. */
/* minmax(min(340px,100%),...) not minmax(340px,...): a bare 340px floor cannot
   shrink below itself, so the grid overflowed a 375px viewport. */
.research-programs{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(340px,100%),1fr));
  column-gap:2.5rem;row-gap:3.25rem;margin:2em 0 2.5em}
.research-program{min-width:0}          /* long titles must not blow the track */
/* HIERARCHY: title, question, THEN figure. The figure used to come first,
   which asked a visitor to decipher a diagram before knowing which programme
   it belonged to -- and these drawings cannot be read at this size anyway.
   Here the thumbnail is a visual signature for recognition and
   differentiation; the title and question carry the meaning.

   UNIFORM VIEWPORT: all six get the same height whatever their native aspect
   ratio, so MAGE's tall figure does not tower over the others. object-fit
   contain, never cover -- cropping a diagram to make rectangles match would
   destroy it. The image is aria-hidden and untabbable: it is decorative here,
   its content lives on the programme page, and the title link already carries
   the accessible name. */
.research-program__figure{display:block;border:1px solid #e4e0d8;background:#fff;
  padding:.4rem;margin:0 0 .6rem;height:190px}
.research-program__figure img{width:100%;height:100%;object-fit:contain;display:block}
.research-program h2{margin:0 0 .3rem;font-size:1.15rem;line-height:1.3}
.research-program h2 a{color:inherit;text-decoration:none}
.research-program h2 a:hover{color:#8E6F3E;text-decoration:underline}
.research-program__q{margin:0 0 .85rem;font-size:.98rem;color:#44403c}
/* No rule above it, no CTA beside it: the title is the link. */
.research-program__foot{margin:0;font-size:.85rem;color:#57534e}
</style>


<div class="research-programs">
{% for program in site.data.research %}
  <div class="research-program">
    <h2><a href="{{ program.url }}">{{ program.title }}</a></h2>
    <p class="research-program__q">{{ program.question }}</p>
    <a class="research-program__figure" href="{{ program.url }}" tabindex="-1" aria-hidden="true">
      <img src="{{ program.figure | relative_url }}" alt="" loading="lazy">
    </a>
    <p class="research-program__foot">{{ program.publications }} publications</p>
  </div>
{% endfor %}
</div>


## Other research

My research also extends beyond these six programs, often through collaborations in which software-engineering questions intersect with other areas.


**Software security, reliability, and systems.** I have studied software security and reliability across areas including GraphQL, provenance, privacy, trust and safety, anti-phishing interventions, and software testing. Examples include:

<div class="other-works">
<a href="https://arxiv.org/pdf/2506.19899">Anti-Phishing Training (Still) Does Not Work: A Large-Scale Reproduction of Phishing Training Inefficacy Grounded in the NIST Phish Scale</a> <span class="venue">(WWW ’26)</span><br>
<a href="https://davisjam.github.io/files/publications/CramerMaxamDavis-TrustAndSafetyEngineeringInSMPs-JSS2025.pdf">Engineering Patterns for Trust and Safety on Social Media Platforms: A Case Study of Mastodon and Diaspora</a> <span class="venue">(JSS ’25)</span><br>
<a href="https://davisjam.github.io/files/publications/ChaWitternBaudartDavisMandelLaredo-PrincipledGraphQL-ESECFSE20.pdf">A Principled Approach to GraphQL Query Cost Analysis</a> <span class="venue">(ESEC/FSE ’20)</span><br>
</div>

**Efficient computing systems.** My work on efficient computing systems includes adaptive models, inference optimization, edge computing, and energy efficiency:

<div class="other-works">
<a href="https://arxiv.org/pdf/2511.18105">AdaPerceiver: Transformers with Adaptive Width, Depth, and Tokens</a> <span class="venue">(CVPR-Findings ’26)</span><br>
<a href="https://arxiv.org/pdf/2407.05941">Pruning One More Token is Enough: Leveraging Latency-Workload Non-Linearities for Vision Transformers on the Edge</a> <span class="venue">(WACV ’25)</span><br>
<a href="https://davisjam.github.io/files/publications/FuGhaffarDavisLee-EdgeWise-ATC19.pdf">EdgeWise: A Better Stream Processing Engine for the Edge</a> <span class="venue">(USENIX ATC ’19)</span><br>
</div>

**Engineering education.** I study how software engineering and systems thinking can be taught through project-based learning and increasingly capable AI tools:

<div class="other-works">
<a href="https://arxiv.org/pdf/2404.16632">Introducing Systems Thinking as a Framework for Teaching and Assessing Threat Modeling Competency</a> <span class="venue">(ASEE ’24)</span><br>
<a href="https://arxiv.org/pdf/2403.18679">An Exploratory Study on Upper-Level Computing Students&#x27; Use of Large Language Models as Tools in a Semester-Long Project</a> <span class="venue">(ASEE ’24)</span><br>
</div>

The complete record is on the [Publications](/publications/) page.


## Patents

- A method for identifying naming mismatches in neural networks based on their architectural properties (2025) — provisional application
- [Determining a validity of an event emitter based on a rule](https://patents.google.com/patent/US11875185B2/en) (2024)
- [Verification of the Integrity of Data Files Stored in Copy-on-Write (CoW) Based File System Snapshots](https://patents.google.com/patent/US11176090B2/en) (2021)
- [Injection of simulated hardware failure(s) in a file system for establishing file system tolerance-to-storage-failure(s)](https://patents.google.com/patent/US11023341B2/en) (2021)
- [Performing hierarchical provenance collection](https://patents.google.com/patent/US10891174B1/en) (2021)
- [File metadata verification in a distributed file system](https://patents.google.com/patent/US10678755B2/en) (2020)
- [Testing of lock managers in computing environments](https://patents.google.com/patent/US10061777B1/en) (2018)
- [Detection of file corruption in a distributed file system](https://patents.google.com/patent/US10025788B2/en) (2018)
