---
title: "Riemann rearrangement theorem in the browser"
date: 2024-12-14T14:59:53.000Z
lastmod: 2024-12-14T15:01:42.000Z
tags: ["mathematics", "interactive demonstration"]
categories: ["Blog"]
slug: "riemann-rearrangement-theorem"
---

One of the first exercises when studying convergence of infinite series asks to show that \(\sum_{n=1}^{\infty} \frac{1}{n}\) is divergent while \(\sum_{n=1}^{\infty} \frac{(-1)^{n+1}}{n}\) is convergent. In more technical terms, \(\sum_{n=1}^{\infty} \frac{(-1)^{n+1}}{n}\) is a [**conditionally convergent** series](https://en.wikipedia.org/wiki/Conditionally_convergent).

This is in contrast to **absolutely convergent** series, that is, infinite sums \(\sum_{n=1}^{\infty} a_n\) such that \(\sum_{n=1}^{\infty} |a_n|\) is also convergent.

What is peculiar about conditionally convergent series, is that it is possible to rearrange the terms in the sequence so that the sum of the rearrangement converges to any arbitrary number. This is called [**Riemann's rearrangement theorem**](https://en.wikipedia.org/wiki/Riemann_series_theorem).

The central idea in the proof is that for a sum to be conditionally convergent, there must be infinitely many positive and negative terms whose respective sums are divergent, and thus by a careful ordering of the terms being summed, the partial sums can be made to osciallate around any fixed value of one's choice and eventually converge there.

The detailed proof can be found on wikipedia and many other books and [websites](https://www.cut-the-knot.org/arithmetic/algebra/RiemannRearrangementTheorem.shtml), so I am not going to report it here. So far, the only applet I knew of demonstrating the rearrangements was on [Wolfram Demonstrations](https://demonstrations.wolfram.com/RiemannsTheoremOnRearrangingConditionallyConvergentSeries/), and I wanted to show our students how the rearrangement works without the need to install external software.
So, I ended up making a [version that runs fully in browser](https://www.mseri.me/rearrangements/). You can also play with it below.

The algorithm comes straight from the proof of Riemann's rearrangement theorem.

The initial interface and visualization where made with the help of [Mistral AI](http://chat.mistral.ai/), slightly refined by hand to include the terms of the sequence in latex and a few other additions.
To whom was asking how I use LLMs, this would be one such example: automate bioring stuff that I could have done myself but would have required a couple of hours to refresh css, look for a suitable js graphing library and its API, and then write it all. Overall I think I did not spend more than 15 mins, between the first version and the improvements,scattered in a few moments when I had some short spare time.

{{< rawhtml >}}
<iframe src="https://www.mseri.me/rearrangements/" width="100%" height="1100px" style="background-color:white;" frameborder="0"></iframe>
{{< /rawhtml >}}
