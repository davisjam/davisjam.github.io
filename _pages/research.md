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

**I am currently looking for *graduate* and *undergraduate* researchers to work on problems that improve the quality of computing systems.** Please review the lab vision and mission statement (below) to understand whether you are interested in joining our work. Then follow [these instructions](/join-lab).
{: .notice--info}

### Why you should join the Duality Lab

Computing systems will transform the day-to-day human experience during this century. The Duality Lab studies how to increase the quality of these computing systems. The work is exciting, and the potential impact is enormous! For example, some of our research results have been adopted by major companies (Microsoft, IBM), others were incorporated into Node.js, and others have led to security patches in the Python runtime.

## Research projects

As discussed below, our lab's vision is to improve the quality of computing systems.
This mandate is broadly writ; most of our projects focus on **correctness** and **security**.
Our research often has an empirical bent, as we must understand engineering practice before we can influence it.

Here are some of our projects, past and present.
For a full list of our publications, see [here](/publications).

### A practical look at regular expressions

Regular expressions (regexes) are a widely used, hard to master engineering tool.
They often cause software defects.
In our regex investigations, we have measured the difficulties that practitioners experience, and guided programming language designers toward regex engines that reflect the needs of practitioners.

1. How widespread of a problem is Regex Denial of Service? ([ESEC/FSE'18](/files/publications/DavisCoghlanServantLee-EcosystemREDOS-ESECFSE18.pdf)).
    - We found ReDoS vulnerabilities in thousands of projects, including [Node.js core](https://nodejs.org/en/blog/vulnerability/march-2018-security-releases/#denial-of-service-dos-vulnerability), [Python core](https://github.com/python/cpython/pull/5955), [MongoDB](https://www.mongodb.com/security), [Django](https://www.djangoproject.com/weblog/2018/mar/06/security-releases/), and [Hapi](https://github.com/hapijs/content/commit/96beb34f7c38a08d024dbf9cd63865c56e2955d9). We also disclosed vulnerabilities to Microsoft, which acknowledged us [here](https://www.microsoft.com/en-us/msrc/researcher-acknowledgments-online-services?rtc=1) in July 2018. Many more of our finds are listed in [Snyk.io's vulnerability database](https://snyk.io/vuln/?packageManager=all), mostly under *npm*.
2. How portable are regexes? ([ESEC/FSE'19](/files/publications/DavisMichaelCoghlanServantLee-LinguaFranca-ESECFSE19.pdf))
   - We used mixed-methods approaches to understand engineering practices and risks around regex re-use.
3. How hard are regexes to work with? ([ASE'19](/files/publications/MichaelDonohueDavisLeeServant-RegexesAreHard-ASE19.pdf))
   - In surveys and interviews with about 300 practitioners, we learned that "Regexes Are Hard" in many ways, suggesting many avenues for further research to support them.
4. How generalizable is regex research? ([ASE'19](/files/publications/DavisMoyerKazerouniLee-RegexGeneralizability-ASE19.pdf))
   - We found that "most regexes are regexes", with no significant outliers by programming language or extraction methodology.

### Server-side event-driven programming

We have investigated the correctness and security risks that resulted from one recent industry shift: adopting the event-driven paradigm on the server side.
Thousands of companies have done so as they shift to the Node.js platform, unifying their stack on one programming language.
Though this paradigmatic transition has brought business benefits, it has also led to many software defects due to fundamental limitations (non-determinism, security flaws) in the architecture of the Node.js framework.

1. What are the race conditions in Node.js programs? ([EuroSys'17](/files/publications/DavisThekumparampilLee-NodeFz-EuroSys17.pdf))
   - We analyzed bug reports on race conditions, then built a fuzzing tool to make these bugs more likely to manifest.
2. What are the denial of service attacks against Node.js programs? ([USENIX Security'18](/files/publications/DavisWilliamsonLee-SenseOfTime-USENIXSecurity18.pdf))
   - We evaluated the avenues for Event Handler Poisoning in Node.js and prototyped a complete defense mechanism: first-class timeouts.
3. What are the performance issues in Node.js programs?
   - My undergraduate student Jonathan Alexander [won first place](https://www.vturcs.cs.vt.edu/spring19.php) at the VT Undergraduate Research in CS competition for his work on this project. Congratulations, Jonathan!

### GraphQL

The web community is considering GraphQL as a means of addressing management issues with traditional REST-style APIs.
We have worked with a team at IBM Research (Yorktown) on understanding and ameliorating issues with this technology.
Aspects of our research have been incorporated into IBM's API Connect And Data Power product [v10.0.0](https://community.ibm.com/community/user/imwuc/blogs/rob-thelen1/2020/06/16/api-connect-and-datapower-v1000-are-generally-avai).

1. What do GraphQL schemas look like? ([ICSOC'19](/files/publications/WitternChaDavisBaudartMandel-EmpiricalGraphQL-ICSOC19.pdf))
   - We identified idioms to help new adopters write easy-to-understand schemas, and evaluated the extent of denial of service vulnerabilities in schemas.
2. How can we defend against GraphQL denial of service attacks? ([ESEC/FSE'20](.))
   - Our findings at ICSOC'19 motivated us to explore accurate static cost estimation for GraphQL queries.

### Data science

Data science techniques have been adopted across most business enterprises.
These techniques include the use of analysis pipelines to automatically and repeatedly process batches of data.
Reproducing and extending these pipelines is a critical aspect of modern data science, and it is also an error-prone task.
We have worked with a team at IBM Research (Almaden) on applying data provenance techniques to the data science context, facilitating pipeline reproduction and extension.

1. How might provenance be applied to assist data scientists? ([VLDB'20](.))
   - We built a system called Ursprung tailored to the data science context.

<!--
### Computing education
-->

## About the Duality Lab

### What's in a name?

The Duality Lab is an abbreviation of the **D**avis Q**uality** Lab.
Quality is often approached dualistically &mdash; technical or social, but not both.
We aim to unite these perspectives.

- Designing high-quality systems requires technical sophistication.
- Designing high-quality systems requires considering how humans will use it.

Call this what you will: human-in-the-loop, a socio-technical perspective, etc.
We believe it is the only way to reach truly high-quality computing systems.

### Vision and Mission

We believe that computing systems will eventually mediate many human interactions with other humans and with the surrounding world.
We therefore seek to improve the human experience by improving the quality of computing systems.
We blend techniques from software engineering, systems, and security in order to understand, measure, and ameliorate the issues that computing practitioners face.
Three factors are foundational to our success:

1. Our **diverse team** helps us understand the ways that computing systems are used and perceived by many kinds of humans. Computing systems will touch all of humanity, and so all of humanity is needed to develop them.
2. Our **data-driven** approach grounds our work in real-world computing systems, ensuring that our findings and proposals impact the quality of computing systems in the here-and-now, not in the what-might-be.
3. Our **readiness to re-imagine** enables us to propose, design, and implement new paradigms.

In order to improve the quality of *existing* computing systems, we take a scientific engineering approach. We empirically study engineering practices in order to drive the development of tools and systems that reflect practitioners’ needs and address their misconceptions. We blend techniques from software engineering, systems, and security in order to understand, measure, and ameliorate the issues that computing practitioners face.

In order to improve the quality of *future* computing systems, we are interested in:

1. Proposing new paradigms to transform how these systems are designed, built, and deployed.
2. Improving computing education. If future computing professionals are better prepared, they are less likely to make the kinds of errors that lead to bugs and security flaws, and to avoid practices that lead to inequitable computing systems.

### Philosophy of training

Learning how to "do research" is a long journey. To help you understand what life will be like in my lab, let me tell you about my philosophy of training.

A research laboratory has two responsibilities.
  First, we create *new knowledge*.
  Second, we create *new researchers*.

Every lab member will contribute to the creation and sharing of new knowledge. This typically takes the form of understanding the state of the art (research literature), designing studies, implementing systems or studying humans, and writing up results.

Research is learned through apprenticeship.
  My lab members will become
    **disciplined thinkers**,
    **thoughtful researchers**,
    and
    **exemplary communicators**.
  I will provide you with
    one-on-one mentoring in these areas,
    feedback to help you understand your strengths and weaknesses,
    and
    resources to help you improve. In addition, senior lab members will help transmit these ideals to junior lab members.
