---
layout: single
title: "Research"
permalink: /research/
author_profile: true
redirect_from: 
  - /lab/
  - /lab.html
---

{% include base_path %}

## Actively recruiting

**I am currently looking for *graduate* and *undergraduate* researchers to work on problems that improve the quality of computing systems.** Please review the lab vision and mission statement (below) to understand whether you are interested in joining our work. Then follow [these instructions](../join-lab).
{: .notice--info}

### Why you should join the Davis Lab

Computing systems will transform the day-to-day human experience during this century. The Davis Lab studies how to increase the quality of these computing systems. The work is exciting, and the potential impact is enormous! For example, some of our research results have been adopted by major companies (Microsoft, IBM), others were incorporated into Node.js, and others have led to security patches in the Python runtime.

## Research projects

As discussed below, our lab's vision is to improve the quality of computing systems.
This mandate is broadly writ; most of our projects focus on **correctness** and **security**.
Our research often has an empirical bent, as we must understand engineering practice before we can influence it.

### Troublesome tools

#### A practical look at regular expressions

Regular expressions (regexes) are a widely used, hard to master engineering tool.
They often cause software defects.
In my regex investigations, I have measured the difficulties that practitioners experience, and guided programming language designers toward regex engines that reflect the needs of practitioners.

Here are the questions we've investigated:

1. <i class="fa fa-trophy" aria-hidden="true"></i> **[ESEC/FSE'18](downloads/publications/DavisCoghlanServantLee-EcosystemREDOS-ESECFSE18.pdf)** How widespread of a problem is Regex Denial of Service ([ReDoS](https://en.wikipedia.org/wiki/ReDoS))?
	- We measured the extent of super-linear regexes in two software ecosystems, npm and pypi.
	- We found ReDoS vulnerabilities in thousands of projects, including [Node.js core](https://nodejs.org/en/blog/vulnerability/march-2018-security-releases/#denial-of-service-dos-vulnerability), [Python core](https://github.com/python/cpython/pull/5955), [MongoDB](https://www.mongodb.com/security), [Django](https://www.djangoproject.com/weblog/2018/mar/06/security-releases/), and [Hapi](https://github.com/hapijs/content/commit/96beb34f7c38a08d024dbf9cd63865c56e2955d9). We also disclosed vulnerabilities to Microsoft, which acknowledged us [here](https://www.microsoft.com/en-us/msrc/researcher-acknowledgments-online-services?rtc=1) in July 2018. Many more of our finds are listed in [Snyk.io's vulnerability database](https://snyk.io/vuln/?packageManager=all), mostly under *npm*.
2. **[ESEC/FSE'19](downloads/publications/DavisMichaelCoghlanServantLee-LinguaFranca-ESECFSE19.pdf)** How portable are regexes?
	- The Internet is full of anecdotes of regex portability problems. We measured them scientifically.
	- We surveyed 150 developers to understand their perspectives about regex re-use and found thousands of regexes re-used from Stack Overflow and RegExLib.
	- We experimentally measured the extent of syntactic, semantic, and performance portability problems when moving regexes across programming languages.
3. <i class="fa fa-trophy" aria-hidden="true"></i> **[ASE'19](downloads/publications/MichaelDonohueDavisLeeServant-RegexesAreHard-ASE19.pdf)** How hard are regexes to work with?
	- We surveyed 279 developers and interviewed 17 developers to learn more about regex practices.
	- They told us that "Regexes Are Hard" in many ways, suggesting many avenues for further research to support them.
4. **[ASE'19](downloads/publications/DavisMoyerKazerouniLee-RegexGeneralizability-ASE19.pdf)** How generalizable is regex research?
	- A deep dive on the generalizability of prior empirical regex research.
	- We investigated whether researchers' regex samples are biased by (1) regex extraction methodology; or (2) programming language.
5. <i class="fa fa-trophy" aria-hidden="true"></i> **[ESEC/FSE'19 SRC](downloads/publications/Davis-RethinkingRegexEngines-ESECFSE19SRC.pdf)** Can we address ReDoS at the regex engine level?
	- Clearly, real software contains ReDoS vulnerabilities. Can we address this issue without major overhauls to the regex engines?

### Emerging paradigms

### Computing education

How can we

## Vision and Mission

We believe that computing systems will eventually mediate most human interactions with other humans and the surrounding world.
We therefore seek is to improve the human experience by improving the quality of computing systems.
We blend techniques from software engineering, systems, and security in order to understand, measure, and ameliorate the issues that computing practitioners face.
Three factors are foundational to our success:

1. Our **diverse team** helps us understand the ways that computing systems are used and perceived by many kinds of humans. Computing systems will touch all of humanity, and so all of humanity is needed to develop them.
2. Our **data-driven** approach grounds our work in real-world computing systems, ensuring that our findings and proposals impact the quality of computing systems in the here-and-now, not in the what-might-be.
3. Our **readiness to re-imagine** enables us to propose, design, and implement new paradigms.

### Which computing systems?

In order to improve the quality of *existing* computing systems, we take a scientific engineering approach. We empirically study engineering practices in order to drive the development of tools and systems that reflect practitioners’ needs and address their misconceptions. We blend techniques from software engineering, systems, and security in order to understand, measure, and ameliorate the issues that computing practitioners face.

In order to improve the quality of *future* computing systems, we are interested in:

1. Proposing new paradigms to transform how these systems are designed, built, and deployed.
2. Improving computing education. If future computing professionals are better prepared, they are less likely to make the kinds of errors that lead to bugs and security flaws, and to avoid practices that lead to inequitable computing systems.

## Philosophy of training

Learning how to "do research" is a long journey. To help you understand what life will be like in my lab, let me tell you about my philosophy of training.

A research laboratory has two responsibilities.
  First, we create *new knowledge*.
  Second, we create *new researchers*.

Every lab member will contribute to the creation and sharing of new knowledge. This typically takes the form of understanding the state of the art (research literature), designing studies, implementing systems or studying humans, and writing up results.

Research is learned through apprenticeship.
  My lab members will become
    **disciplined thinkers**,
    **thoughtful and thorough researchers**,
    and
    **exemplary communicators**.
  I will provide you with
    one-on-one mentoring in these areas,
    feedback to help you understand your strengths and weaknesses,
    and
    resources to help you improve. In addition, senior lab members will help transmit these ideals to junior lab members.
