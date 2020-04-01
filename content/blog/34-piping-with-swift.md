---
title: "Piping with Swift"
date: 2014-06-16T10:03:04.000Z
lastmod: 2014-06-16T10:31:56.000Z
tags: ["swift", "pipe", "operators", "functional"]
categories: ["Blog"]
slug: "piping-with-swift"
disqus_identifier: 34
---

Lately I've been playing with Apple's newborn Swift quite a lot. I have to say that I am really impressed, and except for few things that I hope will be smoothed in the next months (years?), I find Swift really enjoyable and readable.

However, there is one feature that I really miss. Something that I daily use with slightly different syntaxes in Sh, Haskell, Julia and Elixir: the **pipe**!

### Can we implement a _kind of_ pipe in Swift?

Given that in Swift `|`, `.` and `||` have already quite precise and distinct meanings, I am going to mimic Julia and Elixir's notation and use `|>`. 
Swift is unbelievably flexible from this point of view: one can easily define new generic `infix`, `prefix` or `suffix` operator, and state their associativity and precedence properties. You'll soon see that the syntax speaks by itself!

Let's try to define a left associative generic pipe.

    :::swift
    operator infix |> { 
        associativity left 
    }
    func |> <L,R>(left: L, right: L -> R) -> R {
        return right(left);
    }

Then we could use it to chain some function together in an elegant way. For example

    :::swift
    func unique<T:Hashable>(array: Array<T>) -> Array<T>{
        var filter = Dictionary<T,Bool>()
        var result = Array<T>()
        for i in 0..array.count {
            if let elem = filter[array[i]] {
                continue
            } else {
                filter[array[i]] = true
                result.append(array[i])
            }
        }
        return result
    }

    [1, 2, 3, 3, 3, 4, 5, 5, 6, 7] |> sort |> unique |> toString |> println

    // prints '[1,2,3,4,5,6,7]'

I strongly believe that some (better) implementation of the pipe should become part of Swift standard library. For example it would be nice to be able to chain subscripts (e.g. `filter[array[i]]` replaced by `i |> array[$0] |> filter[$0]`) or more flexible maps (e.g. `[1, 2, 3, 3, 3, 4, 5, 5, 6, 7] |> sort |> unique |> map($0, {x in x * x})`) . But maybe I am asking for too much...

While writing this example, I was wondering what is the best way to remove duplicates in a Swift array? The shortest code I could come up with is

    :::swift
    func unique<T:Hashable>(array: T[]) -> T[] {
        var filter = Dictionary<T,Bool>()
        for i in 0..array.count {
                filter[array[i]] = true
        }
        return Array(filter.keys)
    }

but it is probably not the fastest one. Nevertheless, I would probably use an underlying dictionary to implement a `Set` type and use the `Set` to remove duplicates. Note here that `T[]` is just syntactic sugar for `Array<T>`.

Another version, using the builtin `contains` function could be

    :::swift
    func unique<T : Equatable>(array: T[]) -> T[] {
        var result = T[]()
        for x in array {
            if !contains(result, x) {
                result += x
            }
        }
        return result
    }

Again `+=` stands for `append` when used with arrays.

I guess the fastest code would be to use a quicksort and remove the duplicates while sorting, but it (as my second implementation of `unique`) would not preserve the order of appearence.

While wrtiting this post, on HN was linked a [very initersting post](http://nomothetis.svbtle.com/smashing-swift) with implementation of some interesting construct, like the [either of the previous post](http://www.mseri.me/implementing-either-type-in-swift) and more, and pointing out problems of the young swift compiler. I think it's a nice reading.

Additionally I recently stumbled upon the [following stackoverflow thread](http://stackoverflow.com/questions/24027116). I find it quite interesting, especially because it shows a nice extension of Arrays introducing an `each` construct very similar to ruby's one.

Another simple example I was working on is the _null coaleshing operator_ that would come handy with Swift's optionals. An interesting discussion in regard can be found (again) in [stackoverflow](http://stackoverflow.com/questions/24082959).

After some time we can start to understand the limitations of Swift, but the language is definitely still under construction and I would not be surprised if it will be different at the time of the final release. 

In the meanwhile, if you can, experiment with it and have fun!!

UPDATE: despite the many limitations of Swift compiler in this direction, there is a quite active and promising library for functional programming in swift already under development: see [swiftz on GitHub](https://github.com/maxpow4h/swiftz).