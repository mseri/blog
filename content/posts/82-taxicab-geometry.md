---
title: "The Geometry of Bringing Your Kids to School"
date: 2026-06-16T08:44:33+02:00
tags: [mathematics,geometry,education]
categories: ["Blog"]
katex: true
---

Geometry is among the anciest branches of mathematics.
Ethymologically, it comes from the greek *Ge* (γῆ), Earth, and *Metria* (μετρία), measurement.
It was literally born to measure lengths, something we are all familiar from early in school, and can hide surprises in the most unexpected places. In this post we will explore how a random thought, born while bringing our kids to school, can transform into a deep and interesting rabbit hole.

<!-- more /-->

For instance, what is the shortest path between the two points A and B in the figure below?

{{< figure
  src="/images/82-points.svg"
  alt="Two points, labeled A and B"
  width="50%"
>}}

Most of you probably already guessed correctly, that on this flat page, the shortest path is the straight line connecting A and B. 

{{< figure
  src="/images/82-segment.svg"
  alt="Two points, labeled A and B, and a straight line connecting them"
  width="50%"
>}}

And how do you know its length? We have at least two options: a metering tape, or [Pythagoras' theorem](https://en.wikipedia.org/wiki/Pythagorean_theorem).

{{< figure
  src="/images/82-pythagoras.svg"
  alt="Two points, labeled A and B, with a straight line connecting them, a vertical line from A and a horizontal line from B cross themselves to show a triangle. The vertical side is labeled y, the horizontal x. There is a metering tape drawn on the top right corner."
  width="50%"
>}}

That is, the distance between the two points A and B drawn on the page can be computed by $\overline{AB} = \sqrt{x^2 + y^2}$, where $x$ and $y$ are the horizontal and vertical distances between the two points, respectively.

## Pythagoras meets school's commute

Just a few years ago, shortly after we relocated, I was looking in google maps what is the shortest path to our kids' school. Sounds trivial, right? But what I saw on the screen felt puzzling:

{{< figure
  src="/images/82-groningen.svg"
  alt="Lots of horizontal and vertical lines are crossing to connect points A and B. In all cases the time of travel is 5 min (except one that is 6 min)"
  width="50%"
>}}

Notice anything strange?

You see, no matter which combination of roads I take, except one, they all take 5 minutes to traverse, and are roughly of the same length. Don't be fooled by the one exception, is my drawing that did not give credit to the fact that that particular corner should go a bit higher up, drawing a rhomboidal shape more than a square, and as such it is slightly longer, plus a couple of nasty crossings help to make it a bit more time consuming.

But back to our main point. As it turns out that in Groningen, in many cases, the distance between two houses requires us to change Pythagoras theorem! As the picture above shows, to go from home to school, no matter what we do, we are going to travel the whole horizontal distance and the whole vertical distance.

In terms of our points A and B from the beginning of the post, this looks as follows:

{{< figure
  src="/images/82-Taxicab-distance.svg"
  alt="Lots of horizontal and vertical lines are crossing to connect points A and B. In all cases the time of travel is 5 min (except one that is 6 min)"
  width="50%"
>}}

where, indeed, $\overline{AB} = x + y$. This is our new Pythagoras' theorem and gives us an opportunity to talk about differential geometry: to compute lengths of paths in curved spaces, for instance to find the shortest path for a plane to fly around the globe and save time and fuel, what we are morally doing is [redefining Pythagoras theorem](https://en.wikipedia.org/wiki/Pythagorean_theorem#Inner_product_spaces) and exploring what consequences it has. This is one of the roles played by a [Riemannian metric](https://en.wikipedia.org/wiki/Pythagorean_theorem#Differential_geometry) or the [First Fundamental Form](https://en.wikipedia.org/wiki/First_fundamental_form) on the study of surfaces.

## Locally Manhattan cities and Taxicab geometry

A careful look at my wonderfully hand-drawn map of a neighbourhood of Groningen, shows a remarkable fact: Groningen is locally Manhattan.

{{< figure
  src="/images/82-Manhattan.png"
  alt="A screenshot of Manahattan from Apple Maps."
  width="100%"
>}}

As you can see from the picture, also in manhattan there are very few diagonals, large parks leading to large squares, and pretty much squares all over the place. And indeed, the geometry we just defined by bringing the kids to school is called [**Taxicab** or **Manhattan geometry**](Taxicab Geometry](https://en.wikipedia.org/wiki/Taxicab_geometry): a non-Euclidean geometry (i.e. the usual Pythagoras' theorem does not hold), where the distance between two points

$\overline{AB} = |x| + |y|$

is defined as the sum of the absolute differences of their coordinates.
So, like in Groningen,

{{< figure
  src="/images/82-Taxicab-distance.svg"
  alt="Lots of horizontal and vertical lines are crossing to connect points A and B. In all cases the time of travel is 5 min (except one that is 6 min)"
  width="50%"
>}}

Before we move on, this geometry comes with a pretty remarkable paradox.
You see, in real analysis we define integrals approximating areas under curves by little squares.

{{< figure
  src="https://upload.wikimedia.org/wikipedia/commons/c/cd/Riemann_integral_irregular.gif"
  alt="Animation showing refined partitions defining an integral. Source Wikipedia"
  width="75%"
  attr="Source: Wikimedia - Lucas Vieira"
  attrlink="https://en.wikipedia.org/wiki/Riemann_integral#/media/File:Riemann_integral_regular.gif"
>}}

So one could think of approximating a diagonal size by walking very little chunks of horizontal and vertical distances, and then summing them up. Unfortunately, the non-Euclideanness of this geometry will get back at you.
No matter how hard you try, you are going to walk the whole horizontal distance **and** the whole vertical distance.

{{< figure
  src="/images/82-staircase-paradox.svg"
  alt="Many different ways to walk horizontally and vertically from A and B to illustrate the point above."
  width="50%"
>}}

This is known as the [staircase paradox](https://en.wikipedia.org/wiki/Staircase_paradox): any partition of the path into smaller steps still sums to $x + y$ rather than $\sqrt{x^2 + y^2}$. And, apparently, it is an ancient geometric froof going back to Babylon at least according to Martin Gardner in the [appendix to the re-print](https://www.goodreads.com/en/book/show/818063.Calculus_Made_Easy) of [Calculus Made Easy](https://calculusmadeeasy.org/).

{{< figure
  src="/images/82-staircase-paradox-wiki.svg"
  alt="The same as the image above, again, but this time from wikipedia"
  width="75%"
  attr="Source: Wikimedia - RokerHRO"
  attrlink="https://en.wikipedia.org/wiki/File:Quadrat_Diagonale.svg"
>}}

To explain where this falls down and get to some other interesting consequences of our new found geometry, we are going to take quite a long detour.

## Taxicab Circles

Since we are talking about curves, after we looked at lines it seems worth looking at her notable sibling: the circle!

A circle of radius $R$ (centered at $0$) is defined as the set of points $(x, y)$ whose distance $d(x,y)$ equals a fixed number $R$, so for us it is going to be the set of points $x,y$ such that $|x| + |y| = R$.

{{< figure
  src="/images/82-ball-pre.svg"
  alt="Some points belonging to the same Taxicab circle"
  width="50%"
>}}

For instance, if $R=6$, points like $(6, 0)$, $(-2,4)$, $(3.1, -2.9)$, and $(1.523, 4.477)$ will all be part of the circle. And, no, you are not mistaken, the circle so obtained is a square, perhaps rotated by 45 degrees from what you would usually draw.

{{< figure
  src="/images/82-ball.svg"
  alt="A Taxicab circle of radius R"
  width="50%"
>}}

Feel free to go and can check that all points in this drawing sit at the same distance $R$ from the center.

## The Indiana π Bill

Let me take a detour now. In 1897, the Indiana General Assembly (USA) proposed House Bill No. 246, which aimed to legally define $\pi = 3.2$ (for some reasons related to squaring circles, [I'll just remind you to Wikipedia for this](https://en.wikipedia.org/wiki/Indiana_Pi_Bill) or this [excellent but paywalled historical article](https://link.springer.com/article/10.1007/BF03024180)). The bill passed unanimously in the House but was indefinitely postponed in the Senate after a mathematician, C. A. Waldo, who for some unknown reason was there on the day intervened to explain its absurdity.

There are two remarkable facts here: 

1. The senate did not reject the bill, but postponed it indefinitely. I wonder if it is still there, waiting to be passed at some point 🤦‍♂️
2. Yes, people often struggle to find Waldo, but and actual Waldo was there at the right moment 😳

But back to us. Since $\pi$ is defined as the ration between the circumference $2\pi R$ and the diameter $2R$ of the usual Euclidean circle, and our geometry has a different kind of circle that is more akin to the geometry experienced by an American driver, I was wondering if we could pay a favour to Indiana and in fact show some reason in their choice of $\pi$.

Let's see.

## Taxicab's $\pi$

Every point is ad distance $R$ from the center, so every line passing through the center and touching the opposite sides of the circles, that is every diameter, has length $2R$.

{{< figure
  src="/images/82-circumference.svg"
  alt="Drawing-aided computation of the diameter and circumference of the Taxicab circle"
  width="100%"
>}}

For the circumference it is convenient to split the circle in four quadrants, each including one of the segments connecting two consecutive corners.

As shown in the picture, we can apply our Taxicab Pythagoras' theorem to compute that each quarter of the circle has length $\ell = 2R$.
Putting the four together one gets that the circumference $C = 4\ell = 8R$.
This leads to $\pi_T = \frac{C}{2R} = 4$.

Sorry Indiana, it will go better the next time...

## From circles to curves

Back to us. At some point in training as a mathematician, for instance in courses like geometry and multivariable calculus, we get introduced to the way to compute lengths of curves. This involves a mysterious quantity called [arc length](https://en.wikipedia.org/wiki/Arc_length).

As obscure as it may sound, the idea behind this concept is not so bad. The arc length of a curve between two point is basically the distance between those two points as computed along the curve (so by the length of the curve).

It is easier drawn than said. Practically speaking you take your curve, slice it into microscopic chunks, so small that for all practical purposes they look like straight lines, then you apply your Pythagoras' theorem (or replacement thereby) to compute the length of this little line, and resum it up. See figure below.

{{< figure
  src="/images/82-arc-len.svg"
  alt="Drawing of a zoomed in portion of a curve where we apply Pythagoras' theorem to compute the length $\ell$ of the infinitesimal chunk of the curve"
  width="100%"
>}}

While normally $\ell = \sqrt{(x_1-x_0)^2 + (f(x_1)-f(x_0))^2}$, in the Taxicab world we need to use our Taxicab-Pythagoras' theorem, obtaining on each chunk 

$\ell = |x_1-x_0| + |f(x_1)-f(x_0)|$.

Now, as we learn in real analysis, if $f$ is continuous in $[x_0,x_1]$ and differentiable in $(x_0, x_1)$, the [Mean Value Theorem](https://en.wikipedia.org/wiki/Mean_value_theorem) tells us that there exists $x_1^* \in (x_0,x_1)$ such that 

$f(x_1) - f(x_0) = (x_1 - x_0) f'(x_1^*).$

If we now partition the horizontal segment with $N$ points, $a = x_0 \leq x_1 \leq x_2 \leq \dots \leq x_N = b$, replace $0$ by $i-1$ and $1$ by $i$ in the equation above, and sum up the length of the curve in all little chunks in $[x_i, x_{i-1}]$, we get

$\ell\text{ of the curve} = \lim_{N\to\infty} \sum_{i=1}^N \big( (x_i-x_{i-1}) + | f(x_i) - f(x_{i-1}) | \big)$

$\qquad = \lim_{N\to\infty} \sum_{i=1}^N (x_i-x_{i-1})\big(1 + |f'(x^*_{i})|\big)$

$\qquad = \int_a^b \big(1 + |f'(x^*_{i})|\big) dx.$

Compare this with the Euclidean version: $\int \sqrt{1 + (f'(x))^2} dx$. One can clearly see the analogous structure, but it is also evident how a different Pythagoras' theorem has led to a different notion of length. 

Which allows us to circle back to the staircase paradox:  **it's all Pythagoras'**! The convergence problem stemmed from the fact that _we were computing lengths differently and using the Taxicab distance instead of the Euclidean one to approximate the infinitesimal lengths_.

## More Taxicab surprises

With our mystery finally solved, let's test our newfound formula on a couple of examples and explore further.

{{< figure
  src="/images/82-examples.svg"
  alt="A quarter of a Taxicab circle (left) and of a Euclidean one (right) of which we want to compute the Taxicab length."
  width="100%"
>}}

Let's start with the quarter Taxicab circle. We already computed it above and expect its length to be $2R$. Let's do this preliminary check: in our quadrant,

$y = f(x) = R - x \quad\Rightarrow\quad \int_{0}^{R} (1 + 1) \, dx = 2R.$

Great! Ok, let's also take the usual Euclidean circle: $x^2 + y^2 = R^2$.
Then, in our quadrant, $y = f(x) = \sqrt{R^2 - x^2}$ and thus

$\int_{0}^{R} \left(1 + \left| \frac{x}{\sqrt{R^2 - x^2}} \right|\right) \, dx = R + \sqrt{R^2 - x^2} \bigg|_{0}^{R} = R + R = 2 R.$

Wait, what? The Taxicab and Euclidean circle have the same Taxicab length!

Look carefully at what we did, because the surprise does not end here.
Because the formula that we are applying is

$\ell = \int_a^b ( 1 + |f'(x_{i}^\*)| ) dx = (b-a) + \int_a^b |f'(x^*_{i})| dx$

and if $f$ is monotone and differentiable with continuous derivative in $[a,b]$ this can be rewritten as

$\ell = (b-a) + \left| \int_a^b f'(x^*_{i}) dx \right| = (b-a) + | f(b)-f(a) |$

where in the last step we applied the [Fundamental Theorem of Calculus](https://en.wikipedia.org/wiki/Fundamental_theorem_of_calculus). See [Thompson 2011](https://arxiv.org/abs/1101.2922) for all details and more.

We have just shown that for monotone function, the Taxicab arc length $\ell$ depends only on the endpoints! And so, it does not really matter how we bring our kids to school, we can simply take the road that feels right on the day, perhaps still optimizing on the number of left turns and traffic lights :D

If you don't trust my proof above, take another example: $y = f(x) = -\frac{1}{R}x^2 + R$. This is also a monotonic arc of parabola between $0$ and $R$, with the same endpoints $y=R$ and $y=0$ as the circles above. Indeed, $\ell = \int_{0}^{R} \left(1 + \left|\frac{-2x}{R}\right|\right) dx = 2R$.

If you want to learn more about this geometry, there is an old book fully dedicated to it: Krause, E. F. [*Taxicab Geometry: An Adventure in Non-Euclidean Geometry*](https://mitpressbookstore.mit.edu/book/9780486252025). Dover 1987. Surprisingly to me, this geometric is also applied in disparate fields. Some hints are in [Wikipedia](https://en.wikipedia.org/wiki/Taxicab_geometry#Applications) or [this nice piece by Steven Strogatz](https://www.nytimes.com/2025/09/16/learning/lesson-plans/teach-taxicab-geometry-with-steven-strogatz.html) on the NYT.
