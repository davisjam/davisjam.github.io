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
/* Two ancestors cap this page, measured rather than guessed (checks/layout.py
   --measure). At 1920 the grid was 770px wide at every viewport >= 1280:
     #main          max-width 1280px, auto-margins 320px a side
     article.page   padding-right 210.8px -- the Susy suffix(2 of 12), an empty
                    column reserved for a right sidebar this site does not use
   .page__inner-wrap / .page__content / .research-grid added nothing; they were
   all exactly page-width minus that padding.

   The fix widens the ANCESTORS and keeps prose narrow, rather than shrinking
   cards to fit a cap that should not apply to a full-width section. Scoped with
   :has() so only this page is affected -- no layout or theme edits. */
body:has(.research-grid) #main{max-width:min(1600px,calc(100vw - 3rem))}
body:has(.research-grid) .page{padding-right:1em}
/* Only the grid breaks out. Everything else stays at a reading measure -- prose
   at 1500px would be unreadable, which is why the cap exists in the first place. */
body:has(.research-grid) .page__content > *:not(.research-grid){max-width:48rem}
/* Generated with the page. Restrained and academic on purpose: a thin rule, no
   shadow, no rounded corners, no icons. The figures are diagrams, so the
   thumbnail uses object-fit: contain -- cropping one would destroy it. */
.research-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));
  gap:1.5rem;margin:2rem 0}
.research-card{position:relative;border:1px solid #ddd6cc;background:#fff;
  display:flex;flex-direction:column}
.research-card .thumb{background:#f6f4ef;border-bottom:1px solid #e4e0d8;
  aspect-ratio:3/2;display:block;padding:.6rem}
.research-card .thumb img{width:100%;height:100%;object-fit:contain;display:block}
.research-card .body{padding:1.25rem;display:flex;flex-direction:column;flex:1}
.research-card h2{margin:0 0 .5rem;font-size:1.2rem;line-height:1.25}
.research-card h2 a{color:inherit;text-decoration:none}
.research-question{font-style:italic;color:#57534e;margin:0 0 .6rem}
.research-card p{margin:0 0 .75rem;font-size:.95rem}
.research-card-footer{display:flex;justify-content:space-between;gap:1rem;
  align-items:baseline;margin-top:auto;padding-top:.75rem;font-size:.9rem;
  border-top:1px solid #e4e0d8}
.research-card-footer .count{color:#57534e}
/* Whole card clickable, without nesting interactive elements: the title anchor
   is stretched over the card, so the accessible name and tab order stay
   exactly one link per card. */
.research-card h2 a::after{content:"";position:absolute;inset:0}
.research-card:hover{border-color:#9a3f12}
.research-card-footer a{position:relative;z-index:1}
/* Compact example lines: indented, no bullets. Three headings each followed by
   a sentence and 2-3 lines should not read as a second bibliography. */
.other-works{margin:.4rem 0 1.4rem 1.5rem;line-height:1.75}
.other-works .venue{color:#57534e;font-size:.92rem;white-space:nowrap}
@media (max-width:760px){.research-grid{grid-template-columns:1fr}}
</style>

<div class="research-grid">
{% for program in site.data.research %}
  <article class="research-card">
    <span class="thumb"><img src="{{ program.figure | relative_url }}"
         alt="{{ program.figure_alt }}" loading="lazy"></span>
    <div class="body">
      <h2><a href="{{ program.url }}">{{ program.title }}</a></h2>
      <p class="research-question">{{ program.question }}</p>
      <p>{{ program.description }}</p>
      <div class="research-card-footer">
        <a href="{{ program.url }}">Explore {{ program.short_title }} &rarr;</a>
        <span class="count">{{ program.publications }} publications</span>
      </div>
    </div>
  </article>
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
- Injection of simulated hardware failure(s) in a file system for establishing file system tolerance-to-storage-failure(s) (2021)
- [Performing hierarchical provenance collection](https://patents.google.com/patent/US10891174B1/en) (2021)
- [File metadata verification in a distributed file system](https://patents.google.com/patent/US10642796B2/en) (2020)
- [Testing of lock managers in computing environments](https://patents.google.com/patent/US10614039B2/en) (2020)
- [Detection of file corruption in a distributed file system](https://patents.google.com/patent/US10229121B2/en) (2019)


## The lab

I welcome graduate and undergraduate researchers interested in software engineering, systems, security, and the engineering of AI-enabled systems.

[How to join the lab →](/join-lab/)
