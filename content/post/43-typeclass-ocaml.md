---
title: "First steps with Category Theory and OCaml"
date: 2017-06-04T22:00:54.000Z
lastmod: 2017-06-04T22:00:54.000Z
tags: ["ocaml", "blog", "monad", "functor", "typeclass"]
categories: ["Blog"]
slug: "typeclass-ocaml"
disqus_identifier: 43
---

# Introduction

Category theory is an abstrac mathematical framework that had a huge influence
on pure functional programming design patterns. The abstractions and laws that
come bundled with the mathematical concepts allow us to write safer and
composable interfaces, very prone to equational reasoning, at the price of a
steeper learning curve. If you attempt to write some relatively modern Haskell
code, you will inevitably have to deal with Monoids, Functions, Monads, Lenses
and whatnot [typeclassopedia]. Also, if you are using modern OCaml libraries,
you will find fingerprints of these constructs all over the place, even though
there they are less prominent.

These are the notes of a talk, I've given for our team at Citrix. The aim was to
try to introduce some of those abstract concepts with trivial and less trivial
examples, trying to formalize them using the powerful but verbose syntax of the
OCaml module system. I am relatively new to the OCaml world, and there are
likely some things that can be done better, especially toward the end of the
notes. If you have ideas on fixes and improvements, please let me know in the
comments and I'll try to update and correct the text.

In what follows, I will focus on Monoids, Functors (not to be confused with
OCaml's module functors), Applicatives, Alternatives and, only briefly, Monads
(these will be the
[core of another talk](https://medium.com/@huund/monadic-error-handling-1e2ce66e3810),
that will be followed by a final one on the Free Monad -- I will link the
notes here if they are made public).

There is plenty more to discuss: Semigroups, Categories, Semigroupoids,
F-Algebras (scary, but these are really powerful and useful: [f-algebras-video],
[f-algebras-understanding]), Foldables, Traversables
[example-traversable-ocaml], ... You can find a good introduction on the whole
Category Theory for Programmers topic at [bartosz].

It is always interesting to think about counterexamples. I will not have time to
do it here, but you can find a nice account of some of them at
[counterexamples].

At the very end of the talk I will try to show how we can easily implement a
parser combinator using these concepts. This is heavily inspired by [hutton]
(that in turns inspired the famous [parsec] library from Haskell), however our
parser will be an applicative one and not a monadic one. To understand the
differences it is worth reading the paper linked above and compare the parser
there with the one implemented here.

I will try to follow the ocaml conventions writing capitalized modules (e.g.
`Monoid`) and fully capital signatures (e.g. `MONOID`). I will also try to
explicitly mention when I am talking about OCaml Module Functors or functors
in the Haskell sense.

I will use haskell's convention for the list: if `x` is a value, I will
denote `xs` a list of `x`s. In the same way, a list of `x`s is pattern
matched for me as `x :: xs`.

We could have written the whole code using the 'desugared' version of Haskell's
typeclasses, see [demistifying-type-classes], but I think it would be more
idiomatic to try and use the module system. Also this provides a good way to
explore some modern OCaml features (while waiting for modular implicits to
land).

For a proper implementation of these and more type classes, please have a look
at [clarity].  For more advanced concepts, like the free monad, a good start is
[free-monads-in-the-wild].

While writing this talk, a blog post with practically the same ideas has been
posted, [more-typeclasses]. Have a look at that, it does a much better job and
provides more context that what I could do in this brief notes. It also
discusses the Traversables that we are largely ignoring for this seminar. The
main difference between the two is that we are not discussing traversables and
instead spend some time on applicatives. Also some examples differ, although I
have tryed to use a signature as close as possible for the final parser
implementation.

# Why

Abstract classes are

- Composable
- Reusable
- Testable

and you can identify them by the signatures of your functions.

Each class, moreover, will provide a series of general helpers and combinators
that will help having consistent apis for different libraries. Finally, being
baked by mathematical laws, these interfaces are more easily testable. You need
only to test a minimal subset of the functions to ensure that the whole api is
correct.

As a brief example, you probably have already used `map` or `bind` over many
different types, e.g. `option`, `resutl` or `list`.

# Helpers

We will need some preliminary helpers (I will use the same syntax as [clarity]
for those):

```ocaml
let id x = x   (* look at [clarity], they use a neat compiler trick that we are not using here *)
let const x _ = x
let flip f x y = f y x
let compose f g x = f (g x)
let (<.>) f g = fun x -> f (g x)   (* <- compose *)
let (>.>) g f = fun x -> f (g x)   (* first apply [g] then [f] but writing them the other way around *)
let cons x xs = x :: xs
```

# Monoids

Let's start with the the complicated (sounding) mathematical definition. A
monoid is an algebraic structure closed under an associative operation (often
denoted `mappend`) and with a neutral element (often denoted `mempty`).

For example, integer numbers with the addition or with the multiplication
operators form a `Monoid`. Integer numbers with the division operator do not
(this is because you cannot divide by `0`).

This can be specified in OCaml with the following module signature:

```ocaml
module type MONOID = sig
  (** Monoid *)
  type t

  (** Neutral element *)
  (* without this we have a semigroup... *)
  val mempty : t

  (** Associative operation *)
  val mappend: t -> t -> t
end
```

In order to create a `MONOID`, we need to provide an implementation of the
`mempty` and `mappend` functions (as well as the `type`).  We can implement the
monoid modules for integer numbers with sum and product as

```ocaml
module Sum: (MONOID with type t = int) = struct
  type t = int
  let mempty  = 0
  let mappend = (+)
end

module Prod: (MONOID with type t = int) = struct
  type t = int
  let mempty  = 1
  let mappend = ( * )
end
```

NOTE: here we see a first difference with haskell, where polymorphism
allows multiple coexisting definitions of `mempty` and `mappend` that
do not need to be encapsulated in a module namespace.

These are true monoids if we make sure that

```
(* closed: however you choose x, y, z with type t below ... *)
(* neutral element *)
mappend mempty x        = x
mappend x mempty        = x
(* associative *)
mappend x (mappend y z) = mappend (mappend x y) z
```

Note that we cannot enforce these laws with the type system. We need to make
sure that they hold when we are writing the implementation. We can use OCaml
functors (kind of parametrised modules) to add a simple test module for (almost)
any `MONOID`!

```ocaml
(* This is an OCaml functor -- look at its signature on the repl *)
module TestMonoid (M: MONOID) = struct
  open M

  let test_neutral_element x =
    assert (mappend mempty x = x);
    assert (mappend x mempty = x)

  let test_assoc x y z =
    assert (
      mappend x (mappend y z) = mappend (mappend x y) z
    )

end
```

It is crucial to make sure that these laws are satisfied by your modules,
violating them leads often to code that is difficult to reason about and
refactor.

**Exercise**:

- run the tests for the monoids defined above

- check what happens if in the declarations above you replace
`MONOID with type t = int` with `MONOID` or `MONOID with type t := int`.

I mentioned that these patterns allow us to define general common helpers.
Indeed, in all cases we can easily see that the `mappend` function allows us to
synthesize a list of values into one, e.g.

```ocaml
let example1 () =
  let xs = [1; 2; 3; 4; 5; 6] in
  let sum =
    List.fold_left Sum.mappend Sum.mempty
  in
  let prod =
    List.fold_left Prod.mappend Prod.mempty
  in
  Printf.printf "sum:%d prod:%d\n" (sum xs) (prod xs)
```

In the example above there is clearly a pattern that can be generalised. In
fact, monoids usually come bundled with the following helpers.

```ocaml
module Monoid_Utils (M: MONOID) = struct
  (** Generic Monoid helpers.
   * These should really be part of the Monoid module itself *)
  open M

  (** A convenient shorthand for mappend *)
  let (<+>) x y = mappend x y

  (** Any monoid can be concatenated *)
  (* This is more general and works for any foldable ... *)
  let concat xs = List.fold_left (<+>) mempty xs
end
```

Another common simple example of monoid, that does not involve numbers, is the
string:

```ocaml
module StringM: (MONOID with type t = string) = struct
  type t = string
  let mempty = ""
  let mappend s1 s2 = s1^s2
end
```

Let's try one more!

```
(* Broken example... *)
module ListM: (MONOID with type t = 'a list) = struct
  type t = 'a list
  let mempty  = []
  let mappend = (@)
end
```

Unfortunately this will not work, but we can workaround the problem using an
intermediate dummy module (I will never thank enough [free-monads-in-the-wild]
for this).

```ocaml
module type GENERIC_TYPE_WORKAROUND = sig type t end

module ListM (T: GENERIC_TYPE_WORKAROUND): (MONOID with type t = T.t list) = struct
  type t = T.t list
  let mempty  = []
  let mappend = (@)
end
```

Using this is, unfortunately, a bit verbose:

```ocaml
let example2 () =
  let xs = [1; 2; 3; 4; 5; 6] in
  let module MSum = Monoid_Utils(Sum) in
  let module MProd = Monoid_Utils(Prod) in
  Printf.printf "sum:%d prod:%d\n" (MSum.concat xs) (MProd.concat xs);

(* Note how we need to label the type to make it polymorphic *)
let example3 () =
  let xs = [[1;2;3];[1;2;3];[1;2;3]] in
  let concat (type a) xs =
    let module ListM = ListM(struct type t = a end) in
    let module ListU = Monoid_Utils(ListM) in
    let open ListU in
    ListU.concat xs
  in
  concat xs
```

Two other interesting monoids are `Any` and `All`:

```ocaml
module All: (MONOID with type t = bool) = struct
  type t = bool
  let mempty  = true
  let mappend = (&&)
end

module Any: (MONOID with type t = bool) = struct
  type t = bool
  let mempty  = false
  let mappend = (||)
end

let example4 () =
  let xs   = [true; false; false; true] in
  let xs'  = [true; true] in
  let xs'' = [false; false] in
  let module AllU = Monoid_Utils(All) in
  let module AnyU = Monoid_Utils(Any) in
  Printf.printf "all: %b %b %b\n" (AllU.concat xs) (AllU.concat xs') (AllU.concat xs'');
  Printf.printf "any: %b %b %b" (AnyU.concat xs) (AnyU.concat xs') (AnyU.concat xs'')
```


# Functors

Mathematically functors are a bit more complicated than monoids: they are
structure-preserving maps between categories. If monoids represent the things
that can be _synthesised_ (`mappend`ed), functors represent the things that can
be mapped (literally `fmap`ped) over. Quoting [typeclassopedia]:

> There are two fundamental ways to think about `fmap`. The first has already
been mentioned: it takes two parameters, a function and a container, and applies
the function "inside" the container, producing a new container. Alternately, we
can think of `fmap` as applying a function to a value in a context (without
altering the context).

This can be specified in OCaml with the following module type:

```ocaml
module type FUNCTOR = sig
  type 'a t
  val fmap: ('a -> 'b) -> 'a t -> 'b t
end
```

In this case we do not need workarounds to create a module implementing the
`FUNCTOR` signature for lists:

```ocaml
module ListF: (FUNCTOR with type 'a t = 'a list) = struct
  type 'a t  = 'a list
  let fmap f = List.map f
end
```

As for monoids, functors need to satisfy some laws.  We can translate the
structure-preserving property from the mathematical defitinion into the
following (if you know what a _morphism_ is, this should look familiar)

```
  (* we map the identity into itself *)
  fmap id = id

  (* mapping a composition of functions is
   * equivalent to composing the mapped functions *)
  fmap (f <.> g)  = fmap f <.> fmap g
```

This is a way to say that our `fmap` cannot change the "shape" of the mapped
values. We can translate these into a test module, as we did for the monoids.

```ocaml
module TestFunctor (F: FUNCTOR) = struct
  open F

  let test_id x = assert (fmap id x = x)

  let test_compose f g x =
    assert (
      fmap (f <.> g) x = fmap f (fmap g x)
    )

end
```

Many commonly used types are in fact functor instancess. A few examples are the
following.

```ocaml
(* optional values *)
module OptionF: (FUNCTOR with type 'a t = 'a option) = struct
  type 'a t = 'a option
  let fmap f = function
    | Some x  -> Some (f x)
    | None    -> None
end
```

```ocaml
(* result values *)
module ResultF: (FUNCTOR with type 'a t = ('a, string) result) = struct
  type 'a t = ('a, string) result
  let fmap f = function
    | Ok x -> Ok (f x)
    | Error _ as err -> err
end

(* This is only for recent (4.03+) compilers or otherwise it depends
 * on the result library. The rresult library already provides the
 * functor (and monad) implementation for it. *)
```

As it happened with monoids, functors often come with their generic
helpers as well [hackage-data.functor].

```ocaml
module Functor_Utils(F: FUNCTOR) = struct
  (** Generic Functor helpers.
   *  This should be part of the Functor module itself... *)
  open F

  (** A convenient shorthand for fmap *)
  let (<$>) f x = fmap f x

  (** Replace all locations in the input with the same value *)
  let (<$) r x = fmap (const r) x
  (** Flipped version of <$ *)
  let ($>) r x = flip (<$) r x

  (** [void] discards or ignores the result of evaluation *)
  let void f x = fmap (fun x -> ignore(f x)) x
end
```


## Applicative Functors

Applicative functors are a special class of functors carrying some more
structure. Again quoting [typeclassopedia]:

> The title of their classic paper, [applicative-programming-with-effects],
gives a hint at the intended intuition behind the `Applicative` type class. It
encapsulates certain sorts of “effectful” computations in a functionally pure
way, and encourages an “applicative” programming style.

A minimal implementation is simple, but requires some level of care. The
following comes from [hackage-control.applicative].

> An `applicative functor` is a `functor` with application, providing operations
to embed effect free expressions (`pure`), and to apply functions that are in a
context to values already in the context (`ap`, or the equivalent infix `<*>`).

```ocaml
module type APPLICATIVE = sig
  type 'a t

  (* This includes the signature of FUNCTOR,
   * rewriting the types to make them match *)
  include FUNCTOR with type 'a t := 'a t

  (** Lift a value *)
  val pure: 'a -> 'a t
  (** Sequential application *)
  val ap: ('a -> 'b) t -> 'a t -> 'b t

  (* Note that if you still have to define the functor,
   * you can define `fmap` from the above functions as
   * `let fmap f x = pure f <*> x` *)
end
```

Now it should be expectable that there will be plenty of generic helper
functions coming with applicatives as well. This is in fact the case, even more
than for the previous structures.

```ocaml
module Applicative_Utils (A: APPLICATIVE) = struct
  (** Generic Functor helpers.
   * This should really be part of the Applcative module itself *)

  open A
  module FunU = Functor_Utils(A)
  include FunU

  (** A convenient infix for ap -- called apply*)
  let (<*>) f = ap f

  (* Below, we denote `actions` the elements of the applicative typeclass *)

  (** Lift a function to actions. This function may be used as a value
   *  for fmap in a Functor instance. *)
  let liftA f x = f <$> x
  (** Lift a binary function to actions. *)
  let liftA2 f x y  = f <$> x <*> y
  (** Lift a ternary function to actions. *)
  let liftA3 f x y z = f <$> x <*> y <*> z

  (** Sequence actions, discarding the value of the second argument. *)
  let ( <* ) r x = const <$> r <*> x
  (** Sequence actions, discarding the value of the first argument. *)
  let ( *> ) r x = (fun _ y -> y) <$> r <*> x     (* == flip ( <* ) *)

  (* These should be part of foldable or traversable, and in turn
   * they end up with applicatives *)

  (** Evaluate each action in the structure from left to right, and
   * and collect the results. *)
  let rec sequenceA = function
    | [] -> pure []
    | x :: xs -> List.cons <$> x <*> sequenceA xs

  (** Evaluate each action in the structure from left to right, and
   *  ignore the results *)
  let sequenceA_ xs = List.fold_right ( *> ) xs (pure ())

  (** Map each element of a structure to an action, evaluate these actions
   *  from left to right, and collect the results. *)
  let traverseA f =  (List.map f) >.> sequenceA

  (** Map each element of a structure to an action, evaluate these
   *  actions from left to right, and ignore the results. *)
  let traverseA_ f xs = List.fold_right (( *> ) <.> f) xs (pure ())

  (** `forA` is 'traverse' with its arguments flipped. *)
  let forA xs = (flip traverseA) xs
end
```

The `liftAN` functions are very convenient to _lift_ a regular function of `N`
arguments into a function operating on `N` applicative values.

A complete definition must satisfy the following laws (haskell syntax):

- _identity law_: `pure id <*> v = v`

- _homomorphism_: `pure f <*> pure x = pure (f x)` ([typeclassopedia] says:
applying a non-effectful function to a non-effectful argument in an effectful
context is the same as just applying the function to the argument and then
injecting the result into the context with `pure`)

- _interchange_:  `u <*> pure y = pure ($ y) <*> u` ([typeclassopedia] says:
when evaluating the application of an effectful function to a pure argument, the
order in which we evaluate the function and its argument doesn't matter)

- _composition_: `pure (<.>) <*> u <*> v <*> w = u <*> (v <*> w)`

These may again be turned into a generic testing module:

```ocaml
module TestApplicative (A: APPLICATIVE) = struct
  open A
  module ApplU = Applicative_Utils(A)
  open ApplU

  let test_id x = assert (
    (pure id <*> x) = x
  )

  let test_homomorphism f x = assert (
    pure f <*> pure x = pure (f x)
  )

  let test_interchange u y = assert (
    (u <*> pure y) = (pure (fun f -> f y) <*> u)
  )

  let test_composition u v w = assert (
    (pure compose <*> u <*> v <*> w) = (u <*> (v <*> w))
  )
end
```
This can be used to validate some instances of this pattern. We will see some of
its limitations soon...

Note that as a consequence of these laws, the functor instance for `f` will
satisfy

```
fmap f x = pure f <*> x
```

Let's see how this much stuff can be rewritten in OCaml.

We can take the `ListF` module defined above and extend it into an applicative.
In fact, it's kind of the other way around: `ListA` re-exports the
implementation of `ListF` for the functorial part of the signature.

```ocaml
module ListA: (APPLICATIVE with type 'a t = 'a list) = struct
  include ListF

  (** Put a value in a list *)
  let pure x = [x]

  (** Take a list of functions and a list of values,
    *  and applies each function to each element of the
    *  list -- in practice, is a cartesian product *)
  let ap fs xs =
    fmap (fun f -> fmap (fun x -> f x) xs) fs
    |> List.concat
end
```

Another immediate example is `option`.

```ocaml
module OptionA: (APPLICATIVE with type 'a t = 'a option) = struct
  include OptionF

  (** Put a value in a Optional *)
  let pure x = Some x

  (** Take a option function and a option value,
    * and applies the function to the value if
    * they both exists *)
  let ap f x = match f, x with
    | Some f, Some x -> Some (f x)
    | _              -> None
end
```

We can also define an applicative for the `result` type.

```ocaml
module ResultA: (APPLICATIVE with type 'a t = ('a, string) result) = struct
  include ResultF

  (** Put a value in a Result *)
  let pure x = Ok x

  (** Take a result function and a result value,
    * and applies the function to the value if
    * they both exists *)
  let ap f x = match f, x with
    | Ok f, Ok x       -> Ok (f x)
    | Error e, Ok _    -> Error e
    | Ok _, Error e    -> Error e
    | Error e, Error f -> Error (String.concat " " [e; f])
end
```

Note here that we can replace the string with _any monoidal type_, and the last
line of `ap` would just be changed into `| Error e, Error f -> Error (e <> f)`.

Note also that the applicatives are always "short circuiting", `ap` necessarily
does the following: if everything can be extracted, proceed, otherwise always
fall back to the "failure" case.

In [more-typeclasses] there is an interesting derivation using the identity
applicative: it's worth having a look at that post. The identity applicative is
simply:

```ocaml
type 'a id = 'a

module IdApp: (APPLICATIVE with type 'a t = 'a id) = struct
  type 'a t  = 'a id
  let pure x = x
  let fmap f = f
  let ap     = fmap
end
```

What can we do with applicatives? Whay do we care? Let's see an example use to
mock data to test some [xapi] functionality. Given the following types and helpers

```ocaml
type vm_type          = PV | HVM
type storage_location = Local | NFS | SCSI
type vgpu_type        = None | AMD | Nvidia

type vm =
  { storage_size: int
  ; storage_location: storage_location
  ; vgpu_type: vgpu_type
  ; vm_type: vm_type
  }

let vm_of storage_size storage_location vgpu_type vm_type =
  { storage_size
  ; storage_location
  ; vgpu_type
  ; vm_type
  }
```

We can generate all the possible configurations in one go by lifting the
constructor and listing the parameter values.

```ocaml
module ListApp = Applicative_Utils(ListA)

let vm_templates =
  let open ListApp in
  let open FunU in    (* <- unneeded if we use module signatures properly *)
  vm_of
  <$> [1000000; 10000000; 10000000; 1234567890123456]
  <*> [Local; NFS; SCSI]
  <*> [None; AMD; Nvidia]
  <*> [PV; HVM]

(*
# List.length vm_templates
- : int = 72
*)
```

We can use `OptionalA` to generate functions that accept `optional` arguments on
demand. E.g. safe mathematical functions, or list head and tail. This could have
prevented issues like the division by zero in the intel vgpu configuration in
xapi.

You can find plenty of examples of applicative instances at
[hackage-control.applicative].


## Small monadic intermission

We will not say much about monads in this brief notes, although they perfectly
fit the final examples. But a digression here to plant a seed is in order.

We saw that every `Applicative` is a `Functor`. Every `Monad` is an
`Applicative`. The defition turns out to be the following (bear in mind that
there are laws that should be satisfied by these functions. We will not discuss
them here)

```ocaml
module type MONAD = sig
  type 'a t
  include APPLICATIVE with type 'a t := 'a t

  (** Lift a value *)
  (* this already resembles [pure] from APPLICATIVE *)
  val return: 'a -> 'a t
  (** 'Kind of' sequential application, called `bind` *)
  val (>>=): 'a t -> ('a -> 'b t) -> 'b t
end
```

Before going on, keep in mind that there is a standard function named `(=<<)`
which is exactly `(>>=)`, but with its arguments flipped.

```ocaml
val (>>=): 'a t -> ('a -> 'b t)         -> 'b t
val (=<<):         ('a -> 'b t) -> 'a t -> 'b t
```

If we look at the structures that we have mentioned so far, we can see that they
all give us a way to apply functions.

```ocaml
val (@@):  ('a -> 'b)   -> 'a   -> 'b     (* Function application *)
val fmap:  ('a -> 'b)   -> 'a t -> 'b t   (* Key for Functors *)
val ap:    ('a -> 'b) t -> 'a t -> 'b t   (* Key for Applicatives *)
val (=<<): ('a -> 'b t) -> 'a t -> 'b t   (* Key for Monads, you usually see >>= *)
```

The major novelty in the bind, compared to the others, is that the function that
it applies is aware of the context (the `'a` is out of its context and the `t`
is part of the argument function type signature), and this gives it the power to
modify it and avoid short circuiting!

One last secret is that `Monad`s are simply a special kind of `Applicative` for
which we can define a function (`join`) to collapse the context.

```ocaml
val join: 'a t t -> 'a t
```

When that is defined, the following holds.

```ocaml
let return = pure

(** Sequentially compose two actions, passing any value produced
 *  by the first as an argument to the second. *)
let bind v f = join (fmap f v)
let (>>=) = bind

(* bind and join are interchangeable: if you have bind defined,
 * then you can define join as `let join x = x >>= id` *)

(* This is a common monad helper *)
(** Sequentially compose two actions, discarding any value produced
 *  by the first, like sequencing operators (such as the semicolon)
 *  in imperative languages. *)
let (>>)  = ( *> )
```

The difference in the type signatures shows that the Applicative, being context
unaware, can run in parallel and do not rely on previous computations, while the
Monad encodes sequential computations and can make a finer use of the state of
the previous computations. As a friend recently told me, 'a monad is just a
programmable semicolon'.

You can see the incredible amount of helpers for imperative programming that
come as part of monads here: [hackage-control.monad].


## Mixing things up: the `Alternative`s

We have discussed functors and monoids as separate beasts, however there is no
reason for them to be separate... indeed sometimes we can define a monoid over
the applicative functors: welcome the `Alternative`s.

For historical reasons, instead of having just a `mempty` and a `mappend`, the
alternatives come with their own syntax:

```ocaml
module type ALTERNATIVE = sig
  type 'a t
  include APPLICATIVE with type 'a t := 'a t

  (** The identity of <|> *)
  val empty: 'a t
  (** An associative binary operation -- practically mappend *)
  val (<|>): 'a t -> 'a t -> 'a t
end
```

Being both a monoid and an applicative functor, alternatives come bundled with a
huge set of generic helpers as well.

```ocaml
module Alternative_Utils (A: ALTERNATIVE) = struct
  (** Generic Alternative helpers *)
  open A
  module AppU = Applicative_Utils(A)
  include AppU

  module AltMonoid(T: GENERIC_TYPE_WORKAROUND): (MONOID with type t = T.t A.t) = struct
    type t = T.t A.t
    let mempty  = A.empty
    let mappend = A.(<|>)
  end

  (*
  (* This should not be a comment, but for some reason ocaml 4.03 is optimising
   * the hell out of it and it ends up in a stack overflow due to infinite recursion.
   * I have also tried in vane to use lazy, with the same result. They do work, however,
   * when implemented separately case by case. *)

  (* note the need to break infinite recursion adding an intermediate evaluation *)
  let delay f = f ()

  (** Zero or more *)
  (* it could be defined as some v with `in some_ v` replaced by `in many_ v` *)
  let rec many p = List.cons <$> p <*> (delay @@ fun _ -> many p)
    <|> pure []

  (** One or more *)
  let some v = let rec some_ v = cons <$> v <*> (delay @@ fun _ -> many_ v)
    and many_ v = some_ v <|> pure []
    in some_ v
  *)

  (** Always return empty *)
  let fail = empty

  (** Another name for concat *)
  let choose (type a) ps =
    let module AM = Monoid_Utils(AltMonoid(struct type t = a end))
    in AM.concat ps
end
```

The laws that they need to fulfil are both the monoid ones and the functor ones.
I will not enter too much in the detail of alternatives, yet, because an example
will appear soon in the context of the implementation of the parser in the next
session.


# A practical example - monadic parsing library

We will try to use the patterns seen above to implement a simple parsing
library, strongly inspired by [hutton].  You can see similar implementations
both in [opal], [angstrom] and [more-typeclasses].  Parser combinators libraries
built from the same ideas are actually used in production, see [parsec],
[angstrom] and [optparseapp].

To be fair, some these combinators libraries are based on monadic patterns (see
e.g. the implementation for
[opal](https://github.com/pyrocat101/opal/blob/master/opal.ml)) and some on
applicative. Either of them has its pros and its cons, you can see an
interesting comment in [applicative-or-monadic]. The main difference can be
summarised with

> If it helps, you can think of applicative parsers as atomic or parallel while
monadic parsers would be incremental or serial. Yet another way to say it is
that monadic parsers operate on the result of the previous parser and can only
return something to the next; the overall result is then simply the result of
the last parser in the chain. Applicative parsers, on the other hand, operate on
the whole input and contribute directly to the whole output – when combined and
executed, many applicative parsers can run “at once” to produce the final
result.

The zeroeth step, is to define a type for a parser.  A parser is a function that
takes some test and returns a parsed value and the rest of the text, if any.  We
have tree natural possible types:

```ocaml
type text = char list
type 'a p_opt  = text -> ('a * text) option
type 'a p_list = text -> ('a * text) list
type 'a p_res  = test -> ('a * text) string result
```

We will keep things simple and use the `list`, to give an implementation
alternative to [more-typeclasses] and re-use some of the modules already defined
above.

```ocaml
(* this is our parser type *)
type 'a p = text -> ('a * text) list
```

Note that `text` is more general a priori than a list of character, but I've
chosen this implementation for ease of use. Using some lazy char producer would
have been much more efficient in this case.

We can always convert a string to a list of chars using the following `explode`
function.

```ocaml
let explode s =
  let rec aux i acc = if i < 0 then acc else aux (i - 1) (s.[i] :: acc) in
  aux (String.length s - 1) []
```

The simpler parser I can think of matches an empty input and returns something
only in that case.

```ocaml
let empty = function
  | []  -> [((), [])]
  | _   -> []
```

Another simple one consumes the first character in `text` and returns that
character as a result. If it fails it returns the empty list.

```ocaml
let item: char p = function
  | []      -> []
  | c :: cs -> [(c, cs)]
```

This can be easily generalised to a parser that given a function, can construct
a new parser that, when successful, consumes a character of the input and
produces a new value.

```ocaml
let token f = function
  | []      -> []
  | c :: cs -> ListF.fmap (fun y -> (y, cs)) (f c)
```

We can use this to implement a parser to match specific characters.

```ocaml
let char c = token (fun c' -> if c = c' then [c] else [])
```

Given that parsers are functions, the actual `parse` function does nothing but
applying the parser and extracting the value.

```ocaml
let parse parser = fun input ->
  (* parser input <$> ListF.fmap fst *)
  match parser input with
  | []  -> []
  | lst -> ListF.fmap fst lst
```

Now, if we want to start composing the parsers, chaining many of them or
allowing a choice between multiple ones, we need to find some appropriate
combinators. We have a wrapped type and we know from the previous section that
to apply a function inside wrapped types we can use applicative functors.

We can use the types as a guide to define an applicative functor for parsers.

```ocaml
module ParserApplicative: (APPLICATIVE with type 'a t = 'a p) = struct
  type 'a t = 'a p

  (* functor *)
  let fmap f parser =
    parser >.> ListF.fmap (fun (c, cs) -> (f c, cs))

  (* applicative *)

  (* pure takes a value and wraps it in a parser
   * -- a function from text to a list of tuples... *)
  let pure c = fun input -> [(c, input)]   (* equiv. pure c input = [(c, input)] *)

  let ap parser_f parser = fun input ->
    match parser_f input with
    | []            -> []
    | (f, cs) :: [] -> fmap f parser cs
    | lst           -> List.map (fun (f, cs) -> fmap f parser cs) lst |> List.concat (* this should not really happen, we could use `-> .` *)
end

module ParserApp = Applicative_Utils(ParserApplicative)
```

Unfortunately parsers are functions, so we cannot really use our test modules
and instead we need to do the math by hand to check the laws.

We can now use `pure` and `ap` (or `<*>`) as building blocks to make the parser
combinators.  For example a parser that parses the input `['x';'a';'p';'i']` and
produces a unit result:

```ocaml
let xapi = let open ParserApp in let open FunU in
  (fun _ -> "Gotcha!") <$> char 'x' <* char 'a' <* char 'p' <* char 'i'
```

Running this in `utop` will show something like the following.

```
# xapi (explode "xapi");;
- : (string * text) list = [("Gotcha!", [])]

# xapi (explode "xapi11");;
- : (string * text) list = [("Gotcha!", ['1'; '1'])]

# xapi (explode "test");;
- : (string * text) list = []
```

We know more in fact. We can prescribe a parser that always fail and a function
that given two parsers, tries the first and in case of failure tries the second
(something like the `Any` monoid).

```ocaml
module ParserAlternative: (ALTERNATIVE with type 'a t = 'a p) = struct
  include ParserApplicative

  let empty _ = []

  let (<|>) p1 p2 txt =
    match p1 txt with
    | [ ]        -> p2 txt
    | [_] as res -> res
    |  _  as res -> res  (* this will not happen ... we could use `-> .` *)
end

module ParserAlt = Alternative_Utils(ParserAlternative)
open ParserAlt
```

The implementation for alternative gives us a `choose` function to try and apply
multiple parsers, a function `some` that given a parser either parses one result
of the given parser followed by many results, or in case it fails, consumes no
input and returns an empty list, and a function `many` that is like `some` but
does not fail if no result is found.

Another handy combinator is `satisfy` that takes a predicate function for
_filtering_ a parser by only allowing it to succeed when its result satisfies
the predicate:

```ocaml
let satisfy pred p = fun input ->
  match p input with
  | [(x, _)] as res when pred x -> res
  | _                           -> []
```

Interestingly, the `satisfy` combinator allows us to define a variation of
`some`, `char` and `item` that is a bit more legible:

```ocaml
let some' pred = satisfy ((<>) []) (many pred)
let item' = satisfy (const true)
let char' c = satisfy ((=) c)
```

To make things cleaner we can wrap everything in a module with a signature that
hides the implementation details. This also makes the parser type itself
abstract and instead exposes a run function that takes a string as input rather
than a list of characters (as in [parsec]).

I like the approach used in [more-typeclasses] for example. We can use a similar
signature and provide an (almost) swappable implementation

```ocaml
module type PARSER = sig
  type 'a t

  val empty:   unit t
  val run:     'a t -> string -> 'a list
  val map:     ('a -> 'b) -> 'a t -> 'b t
  val pure:    'a -> 'a t
  val ap:      ('a -> 'b) t -> 'a t -> 'b t
  val ( <$> ): ('a -> 'b) -> 'a t -> 'b t
  val ( <*> ): ('a -> 'b) t -> 'a t -> 'b t
  val ( <*  ): 'a t -> 'b t -> 'a t
  val ( *>  ): 'a t -> 'b t -> 'b t
  val token:   (char -> 'a list) -> 'a t
  val char:    char -> char t
  val fail:    'a t
  val choose:  'a t list -> 'a t
  val ( <|> ): 'a t -> 'a t -> 'a t
  val many:    'a t -> 'a list t
  val some:    'a t -> 'a list t
  val filter:  ('a -> bool) -> 'a t -> 'a t
end

module type CHARPARSER = functor (P: PARSER) -> sig

  (* Some optional helpers *)
  val exactly: char -> char P.t
  val one_of:  char list -> char P.t
  val none_of: char list -> char P.t
  val range:   char -> char -> char P.t
  val space:   char P.t
  val newline: char P.t
  val tab:     char P.t
  val upper:   char P.t
  val lower:   char P.t
  val digit:   char P.t
  val letter:  char P.t
  val alpha_num: char P.t
  val hex_digit: char P.t
  val oct_digit: char P.t
end
```

You can see that introducing the alternatives, reduces even more the amount of
special combinators needed to define the parser itself (compare this with the
one obtained in [more-typeclasses])

```ocaml
module Parser: PARSER = struct
  include ParserAlternative
  include ParserAlt

  let map = fmap

  let explode s =
    let rec aux i acc = if i < 0 then acc else aux (i - 1) (s.[i] :: acc) in
    aux (String.length s - 1) []

  let run p s = explode s
    |> p
    |> ListF.fmap fst

  let empty = function
    | []  -> [((), [])]
    | _   -> []

  let token f = function
    | []      -> []
    | x :: xs -> ListF.fmap (fun y -> (y, xs)) (f x)

  let char c = token (fun c' -> if c = c' then [c] else [])

  let satisfy f p cs =
    match p cs with
    | [(x, cs)] when f x -> [(x,cs)]
    | _                  -> []

  let filter = satisfy

  let delay f xs = f () xs

  (* These are alternative's helpers, but we needed to move them
   * here to avoid infinite recursion... To be investigated... *)
  let rec many p = List.cons <$> p <*> (delay @@ fun _ -> many p)
    <|> pure []
  let some p = satisfy ((<>) []) (many p)
end

module MakeCharParser(P: PARSER) = struct
  open P

  let item = token (fun c -> [c])

  let exactly x = filter ((=) x) item
  let one_of  l = filter (fun x -> List.mem x l) item
  let none_of l = filter (fun x -> not (List.mem x l)) item
  let range l r = filter (fun x -> l <= x && x <= r) item

  let space     = one_of [' '; '\t'; '\r'; '\n']
  let newline   = exactly '\n'
  let tab       = exactly '\t'
  let upper     = range 'A' 'Z'
  let lower     = range 'a' 'z'
  let digit     = range '0' '9'
  let letter    = lower  <|> upper
  let alpha_num = letter <|> digit
  let hex_digit = range 'a' 'f' <|> range 'A' 'F' <|> digit
  let oct_digit = range '0' '7'
end
```

This is the same as the example in [more-typeclasses]. Consider a parser for
parsing dates of the format `YYYY-MM-DD`:

```ocaml
module CP = MakeCharParser(Parser)
open Parser
open CP

let int =
  let string_of_list = List.map (String.make 1) >.> String.concat "" in
  (string_of_list >.> int_of_string) <$> some digit

let int_range mn mx = filter (fun n -> mn <= n && n <= mx) int
let zero_digit = char '0' *> int_range 1 9
let year  = int_range 1700 2400
let month = zero_digit <|> int_range 10 12
let day = zero_digit <|> int_range 10 31

let date =
  (fun y m d -> (y,m,d))
  <$> (year <* char '-')
  <*> (month <* char '-')
  <*> day
```

Here are a few examples of running the `date` parser with different string
inputs:

```
# run date "2019-01-23";;
- : (int * int * int) list = [(2019, 1, 23)]

# run date "2019-10-23";;
- : (int * int * int) list = [(2019, 10, 23)]

# run date "2019-1-23";;
- : (int * int * int) list = []

# run date "999-1-23";;
- : (int * int * int) list = []

# run date "a999-1-23";;
- : (int * int * int) list = []
```

We did not mention it later... but to match exactly `xapi` we can use the
`empty` parser:

```ocaml
let xapi = let open Parser in
  (fun _ -> "Gotcha!") <$> exactly 'x' <* exactly 'a' <* exactly 'p' <* exactly 'i' <* empty
```

That in `utop` gives

```
# run xapi "xapi"
- : string list ["Gotcha!"]

# run xapi "xapi1"
- : string list []
```

Another interesting example could be a parser that counts the longest
parenthesis nesting in a parenthesis only string:

```ocaml
module type PARENS = sig
  type 'a t
  val run: 'a t -> string -> 'a list
  val parens: int t
end

module Parens: PARENS = struct
  include ParserAlternative
  include ParserAlt

  let map = fmap

  let explode s =
    let rec aux i acc = if i < 0 then acc else aux (i - 1) (s.[i] :: acc) in
    aux (String.length s - 1) []

  let run p s = explode s
    |> p
    |> ListF.fmap fst

  let token f = function
    | []      -> []
    | x :: xs -> ListF.fmap (fun y -> (y, xs)) (f x)

  let satisfy f p cs =
    match p cs with
    | [(x, cs)] when f x -> [(x,cs)]
    | _                  -> []

  let item = token (fun c -> [c])
  let exactly x = satisfy ((=) x) item

  let rec parens txt = (
    (fun _ b _ d -> max (1+b) d) <$> exactly '(' <*> parens <*> exactly ')' <*> parens
    <|> pure 0
  ) txt
end

open Parens
```

That in `utop` gives

```
# open Parens

# run parens "(())"
- : int list = [2]

# run parens "1(())")
- : int list = [0]

# run parens "(()()()())"
- : int list = [2]

# run parens "((()())()()())"
- : int list = [3]

# run parens "((()(()))()()())"
- : int list = [4]

# run parens "((()(()))()()(()()((((((()))))))))"
- : int list = [9]
```



[angstrom]: https://github.com/inhabitedtype/angstrom "Angstrom: Parser combinators built for speed and memory efficiency"
[applicative-programming-with-effects]: http://www.soi.city.ac.uk/~ross/papers/Applicative.html "Applicative Programming with Effects"
[applicative-or-monadic]: https://stackoverflow.com/questions/7861903/what-are-the-benefits-of-applicative-parsing-over-monadic-parsing#7863380 "What are the benefits of applicative parsing over monadic parsing?"
[bartosz]: https://bartoszmilewski.com/2014/10/28/category-theory-for-programmers-the-preface/ "Category Theory for Programmers"
[clarity]: https://github.com/IndiscriminateCoding/clarity "Clarity"
[counterexamples]: http://blog.functorial.com/posts/2015-12-06-Counterexamples.html "Counterexamples of Type Classes"
[demistifying-type-classes]: http://okmij.org/ftp/Computation/typeclass.html "Demistifying Type Classes"
[example-traversable-ocaml]: https://discuss.ocaml.org/t/notes-from-compose-2017/240/6 "An example of Traversable"
[f-algebras-video]: https://www.youtube.com/watch?v=PK4SOaAGVfg "F-algebras or: How I Learned to Stop Worrying and Love the Type System"
[f-algebras-understanding]: https://www.schoolofhaskell.com/user/bartosz/understanding-algebras "Understanding F-Algebras"
[free-monads-in-the-wild]: http://rgrinberg.com/posts/free-monads-in-the-wild-ocaml "Free monads in the wild - OCaml edition"
[hackage-control.applicative]: https://hackage.haskell.org/package/base-4.9.1.0/docs/Control-Applicative.html "Control.Applicative on Hackage"
[hackage-data.functor]: https://hackage.haskell.org/package/base-4.9.0.0/docs/Data-Functor.html "Data.Functor on Hackage"
[hackage-control.monad]: https://hackage.haskell.org/package/base-4.9.1.0/docs/Control-Monad.html#t:Monad "Control.Monad on Hackage"
[hutton]: http://www.cs.nott.ac.uk/~pszgmh/monparsing.pdf "Monadic Parser Combinators"
[more-typeclasses]: http://blog.shaynefletcher.org/2017/05/more-type-classes-in-ocaml.html "More type classes in OCaml"
[opal]: https://github.com/pyrocat101/opal "Self-contained monadic parser combinators for OCaml"
[optparseapp]: https://github.com/pcapriotti/optparse-applicative "Applicative option parser"
[parsec]: https://hackage.haskell.org/package/parsec "Haskell's parsec"
[typeclassopedia]: https://wiki.haskell.org/Typeclassopedia "Typeclassopedia"
[xapi]: http://xapi-project.github.io "Xapi project"
