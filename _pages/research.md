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

I study how to make software-intensive systems reliable and secure. I do this by
systematically building systems and processes, watching them fail, and turning what we
learn into better ways to engineer the next ones.

My research pursues this problem from several directions: how software fails in
practice; how analysis and assurance can prevent failures; how dependencies and reused
components can be understood and governed; and how changing technologies, including AI,
alter the way software is built and engineered.

My current research is organized around six programs.

<style>
/* Generated with the page. Restrained and academic on purpose: a thin rule, no
   shadow, no rounded corners, no icons. The figures are diagrams, so the
   thumbnail uses object-fit: contain -- cropping one would destroy it. */
.research-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(320px,1fr));
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


## Other research and contributions

My research has also extended beyond these six programs, often through collaborations in which software-engineering questions intersect with other areas.


**Efficient machine learning and computer systems.** I have worked on efficient computer vision, edge inference, software optimization, stream processing, and the energy consequences of software and machine-learning systems.

- *AdaPerceiver: Transformers with Adaptive Width, Depth, and Tokens* — The IEEE/CVF Conference on Computer Vision and Pattern Recognition 2026 -- Findings Track (CVPR-Findings) · 2026
- *Inference-Time Alignment of Diffusion Models via Evolutionary Algorithms* — The IEEE/CVF Conference on Computer Vision and Pattern Recognition 2026 -- Findings Track (CVPR-Findings) · 2026
- *LadderSym: A Multimodal Interleaved Transformer for Music Practice Error Detection* — Proceedings of the International Conference on Learning Representations (ICLR) · 2026


**Software security, reliability, and systems.** Other work has examined GraphQL, provenance, privacy and regulatory compliance, trust and safety, anti-phishing interventions, and software testing and reliability.

- *Anti-Phishing Training (Still) Does Not Work: A Large-Scale Reproduction of Phishing Training Inefficacy Grounded in the NIST Phish Scale* — Proceedings of the ACM Web Conference (WWW) · 2026
- *Engineering Patterns for Trust and Safety on Social Media Platforms: A Case Study of Mastodon and Diaspora* — Journal of Systems and Software (JSS) · 2025
- *An Exploratory Mixed-Methods Study on General Data Protection Regulation (GDPR) Compliance in Open-Source Software* — Proceedings of the 18th ACM/IEEE International Symposium on Empirical Software Engineering and Measurement (ESEM) · 2024


**Engineering education.** I study and develop ways to teach software engineering, systems thinking, security, and professional engineering practice, including project-based learning and the use of AI in software-engineering education.

- *Fostering Systems Thinking through Engineering Study Abroad Programs* — European Journal of Engineering Education (EJEE) · 2024
- *Introducing Systems Thinking as a Framework for Teaching and Assessing Threat Modeling Competency* — Annual Conference of the American Society for Engineering Education (ASEE) · 2024
- *An Exploratory Study on Upper-Level Computing Students' Use of Large Language Models as Tools in a Semester-Long Project* — Annual Conference of the American Society for Engineering Education (ASEE) · 2024


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
