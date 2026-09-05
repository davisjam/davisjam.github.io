---
layout: research-project
title: "Software Supply Chains"
permalink: /research/software-supply-chain/
author_profile: true
research_slug: "Supply Chains"
question: "How can software reuse remain trustworthy at ecosystem scale?"
figure: /assets/research/software-supply-chain/trust-provenance-graph.svg
figure_alt: "Evidence attaches to different edges: identity to the producer, provenance and signatures to the artifact, policy to the consuming system. Signing establishes one edge; whether the accumulated evidence suffices is decided in context."
figure_caption: "Evidence attaches to different edges: identity to the producer, provenance and signatures to the artifact, policy to the consuming system. Signing establishes one edge; whether the accumulated evidence suffices is decided in context."
---

Modern software systems depend on components produced by people and organizations their developers may never meet. Package registries and build systems make that reuse inexpensive, but they also leave developers to decide which producers and artifacts to trust.

We study the evidence available for those decisions. Some of our work examines identity, software signing, and provenance; other work studies whether developers can use those mechanisms effectively, how they assess dependencies, and how attackers exploit gaps in the distribution process.

## What a secure supply chain requires

Before defending a supply chain, we need to say what property is being established. This work sets out the security properties and the attack stages they correspond to.

<ul class="pub-list">
  <li><span class="pub-title"><a href="https://arxiv.org/pdf/2406.10109">SoK: Analysis of Software Supply Chain Security by Establishing Secure Design Properties</a></span><br><span class="venue">SCORED &middot; 2022</span><br><span class="note">Systematized the field around three properties — transparency, validity, separation — giving later work a vocabulary for what a defence establishes.</span></li>
  <li><span class="pub-title"><a href="https://arxiv.org/pdf/2407.03949">Establishing Provenance Before Coding: Traditional and Next-Gen Software Signing</a></span><br><span class="venue">IEEE Security & Privacy Magazine -- Special Issu &middot; 2025</span><br><span class="note">States the provenance-before-coding argument for a practitioner audience.</span></li>
</ul>

## Identity, signing, and provenance

Signing can establish who vouched for an artifact. These studies measure what signing actually establishes in practice, and at what rate it is adopted.

<ul class="pub-list">
  <li><span class="pub-title"><a href="https://arxiv.org/pdf/2401.14635">Signing in Four Public Software Package Registries: Quantity, Quality, and Influencing Factors</a></span><br><span class="venue">S&P &middot; 2024</span><br><span class="note">Measured signing across four public registries. Established how rare and how poor-quality signing actually was, against which later adoption work reads.</span></li>
  <li><span class="pub-title"><a href="https://arxiv.org/pdf/2406.08198">An Industry Interview Study of Software Signing for Supply Chain Security</a></span><br><span class="venue">SECURITY &middot; 2025</span><br><span class="note">Interviewed industry practitioners about signing. Found that the obstacles are organizational as often as technical.</span></li>
  <li><span class="pub-title"><a href="https://arxiv.org/pdf/2503.00271">Why Johnny Adopts Identity-Based Software Signing: A Usability Case Study of Sigstore</a></span><br><span class="venue">SECURITY &middot; 2026</span><br><span class="note">A usability study of Sigstore adoption. Identity-based signing removes the key-management problem and introduces others.</span></li>
  <li><span class="pub-title"><a href="https://arxiv.org/pdf/2603.17133">A Longitudinal Study of Usability in Identity-Based Software Signing</a></span><br><span class="venue">arXiv &middot; 2026</span><br><span class="note">Follows identity-based signing usability over time rather than at one moment, which is where adoption problems become visible.</span></li>
  <li><span class="pub-title">Context-Aware Trust Verification for Identity-Based Software Signing</span><br><span class="note">Verification that accounts for context: what a signature means depends on what is being installed where.</span></li>
</ul>

## Deciding what to trust

A valid signature does not tell a developer whether a producer is trustworthy, or whether a dependency is appropriate here. This work studies the decision itself.

<ul class="pub-list">
  <li><span class="pub-title"><a href="https://arxiv.org/pdf/2310.14117">ZTD-JAVA: Mitigating Software Supply Chain Vulnerabilities via Zero-Trust Dependencies</a></span><br><span class="venue">ICSE &middot; 2025</span><br><span class="note">ZTD-JAVA moves the trust decision to the point of use: a library gets the permissions its call site needs, not those of the whole application.</span></li>
  <li><span class="pub-title"><a href="https://arxiv.org/pdf/2601.00205">Towards a Benchmark for Dependency Decision-Making</a></span><br><span class="venue">JAWs &middot; 2026</span><br><span class="note">Dependency decision-making has no benchmark, so competing approaches cannot be compared. This proposes one.</span></li>
  <li><span class="pub-title"><a href="https://arxiv.org/pdf/2505.18760">ARMS: A Vision for Actor Reputation Metric Systems in the Open-Source Software Supply Chain</a></span><br><span class="venue">JAWs &middot; 2026</span><br><span class="note">Maintainers can review a pull request for correctness but not for the trustworthiness of its author; ARMS proposes reputation as the missing signal.</span></li>
  <li><span class="pub-title"><a href="https://davisjam.github.io/files/publications/SinglaAnandayuvarajKaluSchorlemmerDavis-LLMsForSupplyChainFailureAnalysis-SCORED2023.pdf">An Empirical Study on Using Large Language Models to Analyze Software Supply Chain Security Failures</a></span><br><span class="venue">SCORED &middot; 2023</span><br><span class="note">Tests whether language models can analyze supply-chain failures at the scale the evidence actually exists.</span></li>
</ul>

## Where the assumptions break

Ecosystems assume a familiar package name identifies a familiar producer. Attackers exploit exactly that.

<ul class="pub-list">
  <li><span class="pub-title"><a href="https://arxiv.org/pdf/2502.20528">ConfuGuard: Using Metadata to Detect Active and Stealthy Package Confusion Attacks Accurately and at Scale</a></span><br><span class="venue">ICSE &middot; 2026</span><br><span class="note">ConfuGuard detects package confusion from metadata, treating a familiar package name as evidence that can be forged.</span></li>
</ul>

## The same questions in newer ecosystems

Pre-trained models, research software, and agent registries inherit the distribution problem before they inherit its defences.

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
