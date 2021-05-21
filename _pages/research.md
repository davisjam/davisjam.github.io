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

**I welcome *graduate* and *undergraduate* researchers passionate about improving the quality of computing systems.** Please review the lab description and the active projects to understand whether you are interested in joining our work. If so, follow [these instructions](/join-lab) to check your qualifications and submit your application.
{: .notice--info}

For a full publication list of our publications, see [here](/publications).
Here are some of our current projects:

- Software engineering for domain-specific languages
- "[Software 2.0](https://medium.com/@karpathy/software-2-0-a64152b37c35)" &mdash; Software engineering and its intersection with AI + Machine Learning
- Cybersecurity &mdash; e.g. Internet security, IoT security

## About the Duality Lab

Computing systems will transform the human experience during this century,
  for individuals (I sure like my robotic vacuum)
  and for society (Can computer vision safely support policing and national defense?).
Achieving this transformation requires high-quality software &mdash; an increasingly-difficult challenge as computing systems become more complex.

### Vision

*The vision of the Duality Lab is to improve the quality of complex computing systems.*

We believe that computing systems will eventually mediate many human interactions with other humans and with the surrounding world.
We therefore seek to improve the human experience by improving the quality of computing systems.
We blend techniques from software engineering, systems, and security in order to understand, measure, and ameliorate the issues that computing practitioners face.
Three factors are foundational to our success:

1. Our **diverse team** helps us understand the ways that computing systems are used and perceived by many kinds of humans. Computing systems will touch all of humanity, and so all of humanity is needed to develop them.
2. Our **data-driven** approach grounds our work in real-world computing systems, ensuring that our findings and proposals impact the quality of computing systems in the here-and-now, not in the what-might-be.
3. Our **readiness to re-imagine** enables us to propose, design, and implement new paradigms.

In order to improve the quality of *existing* computing systems, we take a scientific engineering approach. We empirically study engineering practices in order to drive the development of tools and systems that reflect practitioners’ needs and address their misconceptions. We blend techniques from software engineering, systems, and security in order to understand, measure, and ameliorate the issues that computing practitioners face. We apply methodologies appropriate to the task at hand: static and dynamic program analysis, pattern recognition and machine learning, algorithm development, and plenty of system building and hacking.

In order to improve the quality of *future* computing systems, we are interested in:

1. Proposing new paradigms to transform how these systems are designed, built, and deployed.
2. Improving computing education. If future computing professionals are better prepared, they are less likely to make the kinds of errors that lead to bugs and security flaws, and to avoid practices that lead to inequitable computing systems.

### What's in a name?

The Duality Lab is an abbreviation of the **D**avis Q**uality** Lab.

**"Quality"**

What do we mean by "quality"?  Our mandate is broadly writ.  Some of our projects focus on functional properties like **correctness** and **security**, while others consider **engineering process** and **human perspectives**.

Since we must understand engineering practice before we can improve it, our research often has an **empirical** bent &mdash; examining engineering artifacts (e.g. mining software repositories) and engineers themselves (e.g. surveys and interviews).

**"Duality"**

Quality is often approached dualistically &mdash; technical or social, but not both.
We aim to unite these perspectives.

- We believe that designing a high-quality system requires technical sophistication.
- We also believe that designing a high-quality system requires considering how humans will use it.

Call this what you will: human-in-the-loop, a socio-technical perspective, etc.
We believe it is the only way to achieve truly high-quality computing systems.

### Philosophy of training

Learning how to "do research" is a long journey. To help you understand what life will be like in my lab, let me tell you about my philosophy of training.

A research laboratory has two responsibilities.
  First, we create *new knowledge*.
  Second, we create *new researchers*.

Every lab member will contribute to the creation and sharing of new knowledge. This typically takes the form of understanding the state of the art (research literature) and of the practice (existing tools and systems), and then designing studies, implementing systems or studying humans, and writing up results.

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
    resources to help you improve.
  In addition, senior lab members will be given opportunities to help train more junior lab members.

My complete *Advisor-Advisee Compact* is available on request.

### Impact

Our lab conducts research with an eye to practical impact.
Our research results have been adopted by major companies (Microsoft, IBM, Google) and major software systems (Node.js, Python).

## Research projects

Our lab's vision is to improve the quality of computing systems.

Here are some of the active projects in the lab.

### Security and software engineering for domain-specific languages

Domain-specific languages (DSLs) are a technique used to simplify the engineering of complex computing systems.
DSLs allow engineers to express domain-specific information fluently, rather than staggering through an articulation in a general-purpose language.

**DSL #1: Regular expressions**

Regular expressions (regexes) are a widely used, hard to master DSL for string-matching problems.
They often cause software defects.
In our regex investigations, we have measured the difficulties that practitioners experience, and guided programming language designers toward regex engines that reflect the needs of practitioners.

This line of research aims to shore up what might be called "crumbling cyber-infrastructure".
Regexes have been around since the 1940s but their engineering considerations have been overlooked.
Regexes gone awry have caused [Internet-scale outages](https://blog.cloudflare.com/details-of-the-cloudflare-outage-on-july-2-2019/) and are a [potent denial of service vector](https://www.usenix.org/conference/usenixsecurity18/presentation/staicu).

*Specific projects:*

1. How widespread of a problem is Regex Denial of Service? ([ESEC/FSE'18](/files/publications/DavisCoghlanServantLee-EcosystemREDOS-ESECFSE18.pdf)).
    - We found ReDoS vulnerabilities in thousands of projects, including [Node.js core](https://nodejs.org/en/blog/vulnerability/march-2018-security-releases/#denial-of-service-dos-vulnerability), [Python core](https://github.com/python/cpython/pull/5955), [MongoDB](https://www.mongodb.com/security), [Django](https://www.djangoproject.com/weblog/2018/mar/06/security-releases/), and [Hapi](https://github.com/hapijs/content/commit/96beb34f7c38a08d024dbf9cd63865c56e2955d9). We also disclosed vulnerabilities to Microsoft, which acknowledged us [here](https://www.microsoft.com/en-us/msrc/researcher-acknowledgments-online-services?rtc=1) in July 2018. Many more of our finds are listed in [Snyk.io's vulnerability database](https://snyk.io/vuln/?packageManager=all), mostly under *npm*.
2. How portable are regexes? ([ESEC/FSE'19](/files/publications/DavisMichaelCoghlanServantLee-LinguaFranca-ESECFSE19.pdf))
   - We used mixed-methods approaches to understand engineering practices and risks around regex re-use.
3. How hard are regexes to work with? ([ASE'19](/files/publications/MichaelDonohueDavisLeeServant-RegexesAreHard-ASE19.pdf))
   - In surveys and interviews with about 300 practitioners, we learned that "Regexes Are Hard" in many ways, suggesting directions for further research to support them.
4. How generalizable is regex research? ([ASE'19](/files/publications/DavisMoyerKazerouniLee-RegexGeneralizability-ASE19.pdf))
   - We found that "most regexes are regexes", with no significant outliers by programming language or extraction methodology.
5. How can we address Regex Denial of Service in a backwards-compatible way? ([IEEE S&P'21](/files/publications/DavisServantLee-SelectiveMemo-IEEE-SP21.pdf))
   - We describe how selective memoization can protect existing regex engines without major changes.

**DSL #2: GraphQL**

The web community is considering GraphQL as a means of addressing data and website management issues with traditional REST-style APIs.
We have worked with a team at IBM Research (Yorktown) on understanding and ameliorating issues with this technology.
Aspects of our research have been incorporated into IBM's API Connect And Data Power product [v10.0.0](https://community.ibm.com/community/user/imwuc/blogs/rob-thelen1/2020/06/16/api-connect-and-datapower-v1000-are-generally-avai).

*Specific projects:*

1. What do GraphQL schemas look like? ([ICSOC'19](/files/publications/WitternChaDavisBaudartMandel-EmpiricalGraphQL-ICSOC19.pdf))
   - We identified idioms to help new adopters write easy-to-understand schemas, and evaluated the extent of denial of service vulnerabilities in schemas.
2. How can we defend against GraphQL denial of service attacks? ([ESEC/FSE'20](/files/publications/ChaWitternBaudartDavisMandelLaredo-PrincipledGraphQL-ESECFSE20.pdf))
   - Our findings at ICSOC'19 motivated us to explore accurate static cost estimation for GraphQL queries.

### Reproducible machine learning and data science

Complex computing systems increasingly rely on components derived from machine learning and data science.
Machine learning and data science techniques have been adopted across most business enterprises.
These techniques include the development of machine learning models, and the use of analysis pipelines to automatically and repeatedly process batches of data.
Engineering these models, and reproducing and extending analysis pipelines, are critical aspects of modern computing.
It is also hard! Getting them right is a major challenge.
This line of research has many applications in the 21st century.
For example, enabling reproducible, high-quality machine learning and computer vision software will support efforts for national security and national defense.

*Specific projects:*

1. How might provenance be applied to assist data scientists? ([VLDB'20](/files/publications/RupprechtDavisArnoldGurBhagwat-Ursprung-VLDB20.pdf), [SIGMOD'19 demo](/files/publications/RupprechtDavisetal-SIGMOD-Demo-19.pdf))
   - With a team at IBM Research (Almaden), we applied provenance techniques to the data science context.
     Our Ursprung system facilitates pipeline reproduction and extension.
2. What should high-quality machine learning software look like? ([CSE'20 poster]())
   - I work with a [team of students](https://engineering.purdue.edu/VIP/teams/tensorflow) sponsored by Google's [TensorFlow Model Garden](https://blog.tensorflow.org/2020/03/introducing-model-garden-for-tensorflow-2.html) project.
     We are developing high-quality examples of machine learning software in TensorFlow, focused on problems in computer vision.

### Skilled practitioners through computing education

Skilled engineering teams are one key to realizing high-quality computing systems.
What kinds of training do computer engineers need?

**Area #1: Intercultural intelligence**

Intercultural intelligence is one key to success in the engineering workforce.
Engineering firms are full of folks from different cultures, with different perspectives and different beliefs.
Engineering products are used by people all over the world.
If an engineer cannot identify with the Other, they cannot realize their full potential &mdash; to their own detriment and that of human society.

I collaborate with engineering education researchers to investigate ways to promote intercultural intelligence.
Some of these collaborations involve study-abroad programs like Virginia Tech's [*Rising Sophomore Abroad Program*](https://enge.vt.edu/undergraduate/RSAP.html).
However, studying abroad is expensive; to improve accessibility, I am also interested in ways to promote intercultural learning more locally.

*Specific projects:*

1. Study-abroad programs are sustained by faculty member involvement. These leaders constantly encounter the unexpected while abroad, perhaps decreasing their willingness to lead again. In what ways are those faculty members surprised (pleasantly and unpleasantly) by their experiences? ([JIEE'21](/files/publications/OzkanDavisDavisJamesMurziKnight-JIEE21.pdf)).

**Area #2: Teaching software testing**

I collaborate with [Ayaan Kazerouni](http://ayaankazerouni.github.io) on bringing mutation testing into the classroom.

*Specific projects:*

1. How can we make mutation analysis cheap enough for use on student projects? ([JSS'21](/files/publications/KazerouniDavisBasakShafferServantEdwards-JSS21.pdf))
   - We identified a subset of mutation operators that approximate the mutation discovery capacity of the full set of operators, yet at a fraction of the cost. This makes mutation analysis potentially practical in the classroom.

## Lab members

I am delighted to supervise many talented students:

### PhD

- Wenxin Jiang

### Undergraduate

*Current* 

- Vishnu Banna
- Efe Barlas
- Xin Du
- Nikita Ravi
- Tuhin Sarkar
- Apoorva Balasubramanian
- Nicole Hornbrook
- Charlie Sale
- Evan Williams

*Alumni* 

- Anirudh Vegesana (Pursuing MS at Stanford)

You could join them! [Here are the instructions to get started](/join-lab).
