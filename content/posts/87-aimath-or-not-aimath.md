---
title: "Aimath or Not Aimath"
date: 2026-09-24T11:03:12+02:00
tags: [Mathematics, ai]
categories: ["Blog"]
---

Last week the announced solution of Navier-Stokes by OpenAI made a lot of noise in the news and in mathematical circles. I also wrote about it myself [here]({{< relref "86-was-it-really-worth-its-cost.md">}}).

If we set the (arguably very important) ethical and environmental issues aside for a moment, we could imagine a reality where LLMs are used for what they are: human-made tools. In the same way I see benefits in checking tedious computations with, say, Mathematica or SymPy or getting insights from numerical experiments, I can see the benefit of LLMs for exploring topics and ideas.

The way OpenAI and an increasing number of researchers are using these tools, however, treats them more like postgraduate students or research assistants autonomously carrying out their own work, with the final output dumped into a paper without additional checks. You can see how this has been affecting the release of drafts by glancing at the arXiv submission rate in the figure below [[source](https://proofsandprompts.com/2026/09/25/dear-conferences-journals-and-hiring-committees-dont-wait-for-everyone-else/)].

![A line graph showing the monthly arXiv submissions in the Combinatorics category from 2010 to August 2026. The graph highlights a steady increase in submissions over the years, with notable spikes labeled as GPT-5.2, GPT-5.5, GPT-5.6, and Fable 5 in early 2026. The 2025 average submissions are marked with a horizontal dashed line. The data for August 2026 is projected based on 27 observed days.](/images/87-arxiv-combinatorics-submissions.png)

The issue has been highlighted in a very clear way in a draft that appeared recently on the arXiv: [Notes on a strongly aperiodic monotile in E³](https://arxiv.org/abs/2609.24779). Let me quote from it, emphasis mine:

>  With LLM tools (ChatGPT Astra), Ioannis Tsiokos recently reported the first known strongly aperiodic monotile in three-dimensional Euclidean space E³, the Chair44 monotile [...]. Hats off to Tsiokos for this discovery, the framework he developed, and the human inquiry that led to the Chair44 monotile.  
> However, the paper itself and the formalization that it claims for support are not in a form that is readily usable to anyone who wants to understand or check it. _This is not just because of the needless length or complexity of the argument (which is indeed overwhelming as presented), or because the formal repository is not in normal form, or because much of the text is misleading or poorly organized, but mainly because there is so much irrelevant puff to push through_. These are hallmarks of an LLM-driven research paper.  
> _We must, absolutely, insist on a higher standard for scientific discourse. The aim must be to communicate, clearly, with people in the community_ --- certainly this is an historical requirement for publication.
> [...]  
> Overall this may point in a positive direction: New tools in human hands together with human insight produce new mathematics of interest to humans.

This reflects my personal experience well (as a mathematician, as a reviewer, and from experimenting with LLMs), as well as my current opinion.

This lack of revision and digestion of the content has, so far, led to overly verbose, often misleading, works that every now and then even make it into publications (sometimes in respectable journals). It takes considerable effort and a large amount of revisions and pushback to obtain something reasonable, and a lot of self-study to get insight, not necessarily less than without the tool.

And, what is more, once the insight lands, it is usually clear that things have to be rewritten from scratch for them to become readable and understandable, and for the main ideas to take the spotlight.

Indeed, the Navier-Stokes paper from OpenAI turned out to be unreadable, and it will take a lot of work to get some understanding out of it (and to finally check whether what it claims is true): [NPR has an excellent piece about it](https://www.npr.org/2026/09/22/nx-s1-5968588/openai-navier-stokes-problem-mathematicians-learn-little).

This is, by the way, the same problem as with fully vibe-coded software or extreme use of autonomous agents, as [recently emphasized by Simon Willison](https://simonwillison.net/2026/Sep/24/harder/), someone no one could accuse of being anti-AI:

> The more time I spend working with coding agents, the more convinced I am that they make software engineering even harder.  
> We can do amazing things with them, but unlocking their full potential requires extraordinary discipline and knowledge.

But let's get back to maths. Lately I have been trying to follow the interesting discussion on the meaning and value of mathematics via [Proofs and Prompts](https://proofsandprompts.com/), a blog collecting thoughts and ideas from mathematicians on this precise subject, and [Terence Tao's blog](https://terrytao.wordpress.com), which has been collecting many additional guest pieces (see for instance [1](https://terrytao.wordpress.com/2026/09/12/after-math/), [2](https://terrytao.wordpress.com/2026/09/14/why-i-do-mathematical-research/) and [3](https://terrytao.wordpress.com/2026/09/18/if-math-is-more-than-proof-we-need-to-better-celebrate-the-rest-of-it/)). There are plenty of great pieces in both websites, make sure to check out a few.

And then one last news appeared there, to my great surprise and disappointment. A group of 9 very famous mathematicians appointed themselves to help OpenAI release its 100 solved problems: [AGMAI](https://agmai.org/).

It may seem I am overreacting, but the [original announcement](https://terrytao.wordpress.com/2026/09/21/advisory-group-on-mathematics-and-artificial-intelligence/) seems unequivocal about that:

> **Current Task**. We are currently facing the very specific challenge of advising OpenAI on how to coordinate the release of a large number of significant results in mathematics that they report have been produced by their internal model.

My first question of course is why should we even help OpenAI publish 100 unreadable mathslops? It's their marketing stunt, right? They should hire an army of mathematicians and let them figure out what is really there. But that would not have the same marketing impact I guess...

But, more than that, why should these 9 mathematicians decide? We have numerous democratic organizations, nationally and internationally, that I would consider more qualified to identify our shared values and coordinate a response than any arbitrary group of people.

I never doubted that this has been set up with genuine care and interest for the community, but the way it has been set up is troublesome for me. And while I am happy that the [backlash forced a clarification](https://proofsandprompts.com/2026/09/22/why-i-agreed-to-join-agmai/), whatever the final choice, [it will have to strike a very delicate balance](https://mathstodon.xyz/@johncarlosbaez/117322628542184800), and I think that leaving this to an oligarchy of fame, with an online form for feedback, is not the appropriate way to go, and I hope they will reconsider.

- - -

As a final aside, since I gave recommendations for some of Tao's guest blog posts, here are some pieces from Proofs and Prompts that I particularly enjoyed: [1](https://proofsandprompts.com/2026/09/14/a-beginning-for-mathematics/), [2](https://proofsandprompts.com/2026/09/21/many-choices-lie-ahead/) and [3](https://proofsandprompts.com/2026/09/24/all-the-math-we-will-not-see/).
