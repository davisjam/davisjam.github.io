---
layout: research-project
title: "Software Supply Chains"
permalink: /research/software-supply-chain/
author_profile: true
research_slug: "Software Supply Chains"
question: "How can software reuse remain trustworthy at ecosystem scale?"
figure: /assets/research/software-supply-chain/trust-provenance-graph.svg
figure_alt: "Trustworthy reuse requires more than one kind of evidence"
figure_desc: "Three complementary trust problems sit side by side. Identity and provenance asks who produced an artifact and what evidence follows it. Distribution asks whether the consumer received what they intended. Trust in context asks what authority is warranted for a particular use. Beneath them, cross-cutting work on security properties and failure analysis establishes what those mechanisms need to achieve. The same trust problems recur in pre-trained model, AI agent and research-software ecosystems."
---

Modern software systems depend on artifacts produced by people and organizations their developers may never meet. Package registries and build systems make reuse inexpensive, but they separate the act of using software from direct knowledge of who produced it, how it reached the consumer, and what authority it should receive once incorporated into a system.

We study the evidence and engineering mechanisms that make trust possible across those boundaries: establishing identity and provenance, protecting the distribution process, and making trust decisions sensitive to the context in which a dependency is actually used. Across these problems, the recurring question is not simply whether software is trusted, but what evidence justifies what trust, for what use.

## Understanding software supply-chain security

Before defending a software supply chain, we need to know what a defense is supposed to establish, and where real supply chains actually fail. This cross-cutting work develops models for reasoning about supply-chain security and methods for extracting evidence from failures at ecosystem scale.

<ul class="pub-list">
  <li><span class="pub-title"><a href="https://arxiv.org/pdf/2406.10109">SoK: Analysis of Software Supply Chain Security by Establishing Secure Design Properties</a></span><br><span class="venue">SCORED &middot; 2022</span><br><span class="note">Systematized the field around three properties — transparency, validity, separation — giving later work a vocabulary for what a defence establishes.</span></li>
  <li><span class="pub-title"><a href="https://davisjam.github.io/files/publications/SinglaAnandayuvarajKaluSchorlemmerDavis-LLMsForSupplyChainFailureAnalysis-SCORED2023.pdf">An Empirical Study on Using Large Language Models to Analyze Software Supply Chain Security Failures</a></span><br><span class="venue">SCORED &middot; 2023</span><br><span class="note">Tests whether language models can analyze supply-chain failures at the scale the evidence actually exists.</span></li>
</ul>

## Establishing identity and provenance

Software signing can bind an artifact to evidence about its producer and history — but only if the mechanism is adopted, usable, and interpreted correctly. We study what signing and identity establish in practice, why organizations adopt them, and what prevents these mechanisms from becoming routine parts of software development.

<ul class="pub-list">
  <li><span class="pub-title"><a href="https://arxiv.org/pdf/2401.14635">Signing in Four Public Software Package Registries: Quantity, Quality, and Influencing Factors</a></span><br><span class="venue">S&P &middot; 2024</span><br><span class="note">Measured signing across four public registries. Established how rare and how poor-quality signing actually was, against which later adoption work reads.</span></li>
  <li><span class="pub-title"><a href="https://arxiv.org/pdf/2406.08198">An Industry Interview Study of Software Signing for Supply Chain Security</a></span><br><span class="venue">SECURITY &middot; 2025</span><br><span class="note">Interviewed industry practitioners about signing. Found that the obstacles are organizational as often as technical.</span></li>
  <li><span class="pub-title"><a href="https://arxiv.org/pdf/2503.00271">Why Johnny Adopts Identity-Based Software Signing: A Usability Case Study of Sigstore</a></span><br><span class="venue">SECURITY &middot; 2026</span><br><span class="note">A usability study of Sigstore adoption. Identity-based signing removes the key-management problem and introduces others.</span></li>
  <li><span class="pub-title"><a href="https://arxiv.org/pdf/2603.17133">A Longitudinal Study of Usability in Identity-Based Software Signing</a></span><br><span class="venue">arXiv &middot; 2026</span><br><span class="note">Follows identity-based signing usability over time rather than at one moment, which is where adoption problems become visible.</span></li>
  <li><span class="pub-title"><a href="https://arxiv.org/pdf/2407.03949">Establishing Provenance Before Coding: Traditional and Next-Gen Software Signing</a></span><br><span class="venue">IEEE Security & Privacy Magazine -- Special Issu &middot; 2025</span><br><span class="note">States the provenance-before-coding argument for a practitioner audience.</span></li>
</ul>

## Protecting the distribution boundary

Even trustworthy producers and valid artifacts can be defeated by ambiguity in distribution. Package ecosystems use names and metadata to connect developer intent to producers and artifacts; attackers exploit that mapping through typosquatting and package-confusion attacks. We study how those ambiguities can be detected before the wrong dependency enters a system.

<ul class="pub-list">
  <li><span class="pub-title"><a href="https://arxiv.org/pdf/2502.20528">ConfuGuard: Using Metadata to Detect Active and Stealthy Package Confusion Attacks Accurately and at Scale</a></span><br><span class="venue">ICSE &middot; 2026</span><br><span class="note">ConfuGuard detects package confusion from metadata, treating a familiar package name as evidence that can be forged.</span></li>
</ul>

## Making trust contextual

Provenance is evidence, not a verdict. A valid signature does not establish that its producer is trustworthy, that a dependency is appropriate for a particular system, or that it should receive all of the authority available to its caller. We study how trust decisions can incorporate the context in which software is actually used — and how systems can limit the consequences when that trust is misplaced.

<ul class="pub-list">
  <li><span class="pub-title">Context-Aware Trust Verification for Identity-Based Software Signing</span><br><span class="note">Verification that accounts for context: what a signature means depends on what is being installed where.</span></li>
  <li><span class="pub-title"><a href="https://arxiv.org/pdf/2601.00205">Towards a Benchmark for Dependency Decision-Making</a></span><br><span class="venue">JAWs &middot; 2026</span><br><span class="note">Dependency decision-making has no benchmark, so competing approaches cannot be compared. This proposes one.</span></li>
  <li><span class="pub-title"><a href="https://arxiv.org/pdf/2505.18760">ARMS: A Vision for Actor Reputation Metric Systems in the Open-Source Software Supply Chain</a></span><br><span class="venue">JAWs &middot; 2026</span><br><span class="note">Maintainers can review a pull request for correctness but not for the trustworthiness of its author; ARMS proposes reputation as the missing signal.</span></li>
  <li><span class="pub-title"><a href="https://arxiv.org/pdf/2310.14117">ZTD-JAVA: Mitigating Software Supply Chain Vulnerabilities via Zero-Trust Dependencies</a></span><br><span class="venue">ICSE &middot; 2025</span><br><span class="note">ZTD-JAVA moves the trust decision to the point of use: a library gets the permissions its call site needs, not those of the whole application.</span></li>
</ul>

## The same trust problems in newer ecosystems

New ecosystems often acquire mechanisms for distributing reusable artifacts before they acquire mature mechanisms for trusting them. Pre-trained models, AI agents, and research software change what is distributed and how it is consumed, but inherit familiar problems of provenance, distribution, authority, and ecosystem governance.

<ul class="pub-list">
  <li><span class="pub-title"><a href="https://arxiv.org/pdf/2508.15987">PickleBall: Secure Deserialization of Pickle-based Machine Learning Models</a></span> <span class="award">best artifact</span><br><span class="venue">CCS &middot; 2025</span><br><span class="note">A model file that executes code when loaded is an attack surface, and model repositories distribute those files the way registries distribute packages.</span></li>
  <li><span class="pub-title"><a href="https://arxiv.org/pdf/2510.03495">AgentHub: A Registry for Discoverable, Verifiable, and Reproducible AI Agents</a></span><br><span class="venue">JAWs &middot; 2026</span><br><span class="note">Agent ecosystems are beginning to distribute executable capability, and they inherit the registry trust problem before they inherit its defences.</span></li>
  <li><span class="pub-title"><a href="https://arxiv.org/pdf/2601.20980">Operationalizing Research Software for Supply Chain Security</a></span><br><span class="venue">JAWs &middot; 2026</span><br><span class="note">Research software has a supply chain with different incentives and far less tooling than industry's.</span></li>
</ul>

## Funding and support

This work has been supported by:

- **US National Science Foundation** — [Collaborative Research: Planning: CROSS: Building a Community aROund Securing the Research Software Supply Chain](https://www.nsf.gov/awardsearch/show-award/?AWD_ID=2537308) (#2537308)
- **Socket, Inc.** — Unrestricted Gift: Typosquat Detection in Open-Source Ecosystems
- **Google, LLC** — Unrestricted Gift: Improving OSS Supply Chain Security by Promoting Software Signing
- **US National Science Foundation** — [POSE: Phase I: Scoping An Open-Source Ecosystem Around Proactive Software Supply Chain Monitoring](https://www.nsf.gov/awardsearch/show-award/?AWD_ID=2229703) (#2229703)
- **Cisco** — Monitor and manage security risks in software supply chains with Sigstore
