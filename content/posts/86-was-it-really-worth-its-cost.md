---
title: "Was It Really Worth Its Cost?"
date: 2026-09-09T08:59:37+02:00
tags: [mathematics, philosophy, ai, ethics]
categories: ["Blog"]
---

The announcement of the resolution of one of Clay's math millennium problems is spreading all over the news, mostly based on the [official announcement by OpenAI](https://openai.com/index/navier-stokes-solution/).

However, many of the articles I have seen so far have been underplaying the shady side of this story. A few hours before the announcement, a professor from NYU involved in an alternative proof of part of the problem published an astonishing statement. Since it is short and, I think, provides a clear picture of what happened, before going on, have a read: <https://cims.nyu.edu/~tristanb/statement.pdf>. It is going to be important to understand what I am talking about.

I am a mathematician, so somewhat emotionally connected to all of this. If you prefer a shorter, more detached but reasonably balanced breakdown of this story, I think Simon Willison's [post](https://simonwillison.net/2026/Sep/8/on-navier-stokes/) does a good job. Otherwise, read on!

- - -

I am now assuming you have read the statement. I should probably not be surprised, given the repeated scandals around OpenAI, yet it puzzles me how much unethical and bullying behaviour can be packed in a single story. And it upsets me knowing that there won't be any repercussions for OpenAI and, if anything, this will attract even more customers...

First of all, even if the suspicions about training on the researchers' material are unfounded, the choice to jump on solving the problem immediately after hearing the rumor of someone else's progress and throwing such an enormous amount of resources at it (more on this later) goes pretty much against any of the common practices of respect and collaboration in the mathematical community. Of course there may be competition here and there, but at least this tends to be fair and more or less evenly-resourced.

Secondly, but not less relevant, asking to stop crediting a direct collaborator because he works with a competitor (Anthropic) is pretty shitty, notwithstanding the fact that he worked on this project outside his regular job, and used a mix of models from both companies.

And in all of this I have not mentioned the threats. Quoting from the PDF:

> if OpenAI released its result in the way proposed I would go public with what happened.  
>   
> [...] “Why would you ruin your career?” I replied that I am an academic, and asked why he thought going public would ruin my career.  
>   
> [...] “If you don’t want me to be nice, then I don’t have to be nice.”

Nor the fact that in their first published draft, OpenAI (or should I say their agent swarm?) [had not cited the main research the work was building upon](https://mathstodon.xyz/@highergeometer/117241589729286509).

Of course, this is not an isolated fact. On the one hand, not citing their sources is [kind of a common pattern in these announcements](https://www.scientificamerican.com/article/openais-latest-math-breakthroughs-commit-research-misconduct-experts-say/), only rectified after the community got riled up. On the other, social misconduct has also been the order of the day. Just in March, Math, Inc. abused the collaboration to complete the formalization of the Sphere Packing problem (cf. [Avigad's summary](https://arxiv.org/pdf/2603.03684) or this watered-down version by [Spectrum](https://spectrum.ieee.org/ai-proof-verification)). Just a few days ago Anthropic did something similar with the [formalization of Fermat's Last Theorem](https://www.anthropic.com/research/formalizing-fermats-last-theorem), although I have to admit that they did it with a much lower level of overall shittiness (but don't worry, they have [their own ethical shitshows](https://prospect.org/2026/09/09/anthropic-artificial-intelligence-surveillance-system-monitor-activists/)).

I think the response by [Kevin Buzzard](https://xenaproject.wordpress.com/2026/09/04/flt-anthropic-has-beaten-me-to-it/) makes the point quite clearly, but let me lightly elaborate here.

Everyone in adjacent communities knew about Buzzard's effort and ongoing work on the formalization, and clearly also Anthropic did. So what was dumping a full unrevised formalization useful for, if not just marketing?

The main outcome of their efforts has been diminishing the value of the ongoing work and hurting the morale of all the researchers and students involved, in a way that again goes against many of our common practices of respect and collaboration. And also in this case, I am sure there have been no consequences, and if anything it has helped for publicity and to attract new customers.

This is not to say that shitty things never happened in the mathematical community, far from it, but the scale now (and the resource disparity) is very different. And honestly there is no benefit for anyone (except huge corporations): it won't help advance mathematics and it does not help the development of knowledge and understanding, which is the main reason we do mathematics after all.

As most of our students know and I have repeatedly written in this blog, understanding comes from the struggle and the first-hand work that we put in. If we remove this from the picture, knowledge and the opportunity to seek new interesting problems and ideas will start stagnating, to the detriment of the whole community. Given the sheer amount of applications mathematics finds "after the fact", this will end up being a loss for everyone.

So, was it worth spending $300,000 on autoformalizing FLT? And even more so, was it worth wasting [$15,000,000](https://simonwillison.net/2026/Sep/8/on-navier-stokes/) to [$22,000,000](https://techcrunch.com/2026/09/08/openai-fought-dirty-on-career-making-math-problem-says-nyu-mathematician/) to steal the spotlight from the actual researchers who did the hard work?
And note that these numbers do not include the team that oversaw the work, nor the unnecessary environmental impact of maintaining a swarm of over 10,000 agents with your most expensive models active for days.

I can hypocritically buy into seeing these large language models as potentially useful tools, although one has to be mindful of the actual use [since many of the tasks one offloads are the ones that can help train new generations of researchers](https://arxiv.org/pdf/2602.10181).
But this continuous marketing abuse has become asphyxiating.

Tonight Tao had an [interesting observation on this](https://mathstodon.xyz/@tao/117237320796901560):

> I wrote recently about how the collection of good, fruitful open problems is now being mined in a non-renewable fashion, leading to the potential scenario of these problems becoming scarce. This may seem unintuitive at first, since the set of possible problems one could ask is infinite. [...]  
>  
> Working out whether a question is actually worth highlighting is a lengthy, deliberate, and subjective process, often informed by historical experience on what good mathematics was generated (or not generated) while working on earlier problems of this type.  In particular, being aware of the "difficulty landscape" in a field - what questions are very easy to answer with known methods, which ones can be solved but only with some effort, and which ones are impossible - is of crucial importance in making such determinations. [...]  
>  
> We have now seen that even the rumor of someone working on a problem can trigger a massive amount of AI-powered effort to flatten it before the original research project has time to reach its full potential.  The incentives may now be pointing in the direction of no longer sharing any promising research directions with the broader community, which would reverse centuries of traditions of open science and do serious long-term damage to the future of the field. [...]

Sadly, I am starting to see this rhetoric against open sharing growing in many places.

I guess all of these stories are resurfacing old worries on intelligent machines. On a lost Hacker News page, someone was quoting "Jokester", a short story written by Isaac Asimov in 1956:

> Early in the history of Multivac, it had become apparent that there was one big bottleneck: the questioning procedure. Multivac could answer the problems of humanity, all the problems, if -- if it were asked meaningful questions. But as knowledge accumulated at an ever-faster rate, it became ever more difficult to locate those meaningful questions.

When I was reading the above, a recent post by Anil Madhavapeddy came to mind: [Just a rumour of a bug is enough to find a security exploit these days](https://anil.recoil.org/notes/rumour-is-the-exploit). His words are pretty much explicitly reflected in Tao's reaction, in a perhaps less dangerous context.

It makes me sad to think about the impact this is going to have on the perception of mathematics.
I started this post mentioning that most articles I saw are pretty much ignoring the ethical wrongdoings of OpenAI and are buying into the hype without any attempt to contextualize the value of it. The more we keep leaving these corporations barely accountable, the more power we are granting them, and the more damage we are allowing them to do to our societies.

As for what concerns mathematics, I like the way Francis Su put it for his students just a few weeks ago: [The Enduring Value of Math, in an Age of AI](https://francissu.substack.com/p/the-enduring-value-of-math-in-an)

> [...]  
> Maybe you’re asking questions like these:  
> - Why get good at problem-solving if an AI can do that much more efficiently?  
> - Why construct mathematical arguments, when AI models can now produce cleaner, slicker, more well-reasoned arguments than I can?  
> - What’s the point of being a math major?  
>   
> Let me provide some comfort and reassurance, though maybe not in the way you might expect. [...]  
>   
> The good news is that doing mathematics is not ultimately just about the particular problem-solving skills you are learning, nor about the outputs you are producing. It’s actually more about the kind of person you are becoming. Said another way, mathematical thinking is a set of virtues, not just a set of skills.  
>  
> Skills are things you learn to do in a math class—like applying Stokes’ theorem, or carrying out an inductive proof. Yet in the age of machines (of which AI is only the latest incarnation), the instrumental value of executing particular skills is diminishing. If your future job depends only on skills, that job is in jeopardy in the AI revolution.  
>  
> Virtues, on the other hand, are aspects of character that you build. These are habits of mind or dispositions that become second nature as a result of doing math regularly—like being creative, or seeing a problem from multiple points of view, or being persistent in problem-solving, or being less fearful of getting stuck and knowing how to chew on a hard problem for a while. Or experiencing joy when you see a beautiful idea.   
>   
> In a math education, you develop into creative and flexible mathematical thinkers who have the confidence to attack problems you’ve never seen before. That’s a virtue—a character quality—built by a great math education. You learn to sit with hard problems for a long time and possibly get nowhere with them. That disposition serves you well when you encounter other hard (non-mathematical) problems in your life, so that when the going gets tough, your past experience with math teaches you how to say to yourself: it’s okay if I don’t know what to do right away, but if I persist in brainstorming even when it seems hopeless, I just might see my way out of this. [...]  

It is a very elaborate post, don't stop at my excerpt above, but take the time to read it all and digest it.

From my personal experience, I can see how this formation has shaped my life and how it helped me even after I left the academic world. So I cannot but agree with his conclusions.
