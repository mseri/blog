Id: 41,
Title: Left pipe in Haskell
Date: 2014-11-21T15:24:54.000Z
Modified: 2014-11-21T15:24:54.000Z
Tags: haskell, pipe, random toughts
Category: Blog
Slug: left-pipe-in-haskell
Authors: Marcello Seri

If you read this blog, you know that I am very biased by having worked with unix shells for almost two decades and that I am addicted to the use of pipes (see e.g. [Piping with Swift](http://www.mseri.me/piping-with-swift/)). I really find much more natural to see data moving from left to right.

Yesterday I was thinking that in Haskell everything is an expression and that you can easily define infix operators. Thus it must be possible to implement a shell-like pipe.

First of all, composition `(.)` is too strong, the pipe I have in mind is like `($)` but reversed. In fact, my second attempt (I feel embarassed by the first, I am not going to post it ;-P) was
```
($>) = flip ($)
```
One can immediately check that it is typed correctly as 
```
($>) :: a -> (a -> b) -> b
```

Now I can do e.g.
```
import Data.List

[3,1,4,2,2,6] $> sort $> filter (\x -> x < 4) $> map even $> and
```
and get the result without complaints.

This is just a stupid example but I find it more expressive (again probably because I use too much the shell) than
```
and . map even . filter (\x -> x < 4) . sort $ [3,1,4,2,2,6]
```
at least for certain kind of progressive filtering of data.

I am now following **fp101x** on **edX**. It is quite good! I will soon(?) post a brief cheatsheet that I made to recall how to use Functors, Monads and other interesting constructs.