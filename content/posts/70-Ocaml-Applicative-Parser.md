---
title: "Fixing an infinite recursion in OCaml applicative parsers"
date: 2026-02-27T11:33:16+01:00
tags: ["ocaml", "parser combinators", "category theory", "monad", "functor", "applicative", "typeclass"]
categories: ["Blog"]
toc: true
---
Nine years ago, while I was still a fresh OCamlr, I gave a presentation (later turned blog post) with title [First steps with Category Theory and OCaml](https://www.mseri.me/typeclass-ocaml/).
The idea was to show how to implement the basic typeclasses of Category Theory in OCaml, and how to use them to build a simple parser combinator library, by following what I had learned from Haskell.
At the time, not knowing better, I stumbled upon an annoying issue: if you look at the code examples for the `Alternative_Utils` module, you will find the following commented-out code.

```ocaml
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
    <|> pure[]

  (** One or more *)
  let some v = let rec some_ v = List.cons <$> v <*> (delay @@ fun _ -> many_ v)
    and many_ v = some_ v <|> pure[]
    in some_ v
  *)
```

As you can read, my reaction was to blame the compiler. Of course, I was wrong :)

It took some months before I understood what I was doing wrong and I never found the time to update that post.
During a recent train trip, however, when I was simply too tired to work more and I was mindlessly staring out the window, this just came back to mind and I decided to give it another go.

As it turns out, OCaml wasn't maliciously optimizing my code into a stack overflow.
As an eager language (and in contrast to lazy ones, like Haskell), it was just doing its job.
But we _can_ make sure it does what we want and it is not so hard!

Note that from now on, I will be assuming that you have read the [old post](https://www.mseri.me/typeclass-ocaml/).
Most of the combinators I will be using below come from there and I will not re-explain them.

## A `delay` done right: deferring eager evaluation

In a language like OCaml, arguments to functions (and combinators like `<*>` and `<|>`) are evaluated _before_ the function itself is executed.
To construct the parser `many p`, OCaml must first evaluate the right-hand side of the `<*>` operator: `delay (fun _ -> many p)`. 

Since `delay` was defined as `let delay f = f ()`, the function `f` is executed immediately.
This immediately calls `many p`, which evaluates `delay`, which calls `many p`... and so on.
Taking a moment to think about it, makes it clear that we will get a `Stack_overflow` already during the construction of the parser, long before we even feed it a string to parse!

In a lazy language like Haskell, this isn't an issue because `many p` wouldn't be forced until it's actually consumed by the parser input.
To fix this in OCaml, we need to be smarter in our use of `delay` to defer the evaluation.

In the original attempt, I was trying to hide `delay` inside `Alternative_Utils`.
But since the type `'a t` is completely abstract there, we cannot access the data structure itself to manually defer the evaluation.
In other words, we can only define behaviors that rely on the existing abstract operators, like `<*>`, `fmap`, `<|>`.

To solve this, let's just make the concept of deferred evaluation explicit and expose it directly into the `ALTERNATIVE` signature:

```ocaml
module type ALTERNATIVE = sig
  type 'a t
  include APPLICATIVE with type 'a t := 'a t
  val empty: 'a t
  val (<|>): 'a t -> 'a t -> 'a t
  
  (** Defers evaluation to avoid infinite recursion*)
  val delay: (unit -> 'a t) -> 'a t
end
```

Now that the module type enforces the `delay` primitive, our `Alternative_Utils` implementation can directly (and abstractly) make use of it.
We can write `many` and `some` identically to their mathematical definitions by wrapping the recursive branch in `A.delay`:

```ocaml
module Alternative_Utils (A: ALTERNATIVE) = struct
  open A
  module AppU = Applicative_Utils(A)
  include AppU

  (** Zero or more *)
  let rec many p =
    A.delay (fun () -> some p <|> pure[])

  (** One or more *)
  and some p =
    List.cons <$> p <*> many p
end
```

Notice how `many` and `some` are mutually recursive.
When `some p` constructs its parser, it requests `many p`.
But because `many p` immediately returns `A.delay (...)` this is not a problem.
The fact that `delay` wraps the whole parser (and is not simply within an argument, like in the original broken implementation) makes sure the recursion stops instantly until an evaluation is requested: the actual parser chain isn't built until the `delay` is forced!
And indeed, you can paste the code in `utop` and it will happily define everything without a stack overflow.

The remaining question, now, is: does this work in practice?

We can get back the [old parser code](https://www.mseri.me/typeclass-ocaml/#a-practical-example---monadic-parsing-library) and see what an implementation now looks like.

Implementing `delay` properly is beautifully elegant, thanks to a functional trick called _eta-expansion_: we just need to explicitly present the argument to the function!

```ocaml
module ParserAlternative: (ALTERNATIVE with type 'a t = 'a p) = struct
  include ParserApplicative

  let empty _ =[]
  
  let (<|>) p1 p2 txt =
    match p1 txt with
    | []  -> p2 txt
    | res -> res

  (** Eta-expansion saves the day! *)
  let delay f = fun input -> f () input
end
```

Because OCaml is strict, eta-expansion changes the order of evaluation.
In this way, `many` and `some` work universally without crashing the stack, and we can use them to parse recursive structures.

This construction is a nice example also to get into some more technical computer sciency terminology.

The term eta-expansion originates from [lambda calculus](https://en.wikipedia.org/wiki/Lambda_calculus) (quite a fun topic if you are mathematically inclined), where it denotes a way to convert an expression like $f$ into $x \mapsto f(x)$, effectively wrapping the function to accept parameters explicitly.
The opposite is achieved by _eta-reduction_, which simplifies $x \mapsto f(x)$ to just $f$ (when they are equivalent).

Back to our example, by explicitly taking the `input` list and passing it to the function, we create a so-called _closure_: this is a function bundled together with its surrounding environment.
In a sense, it remembers and retains access to variables from its enclosing (lexical) scope even after such scope has finished executing.
Then `f ()` is safely suspended and won't be evaluated until the string input begins flowing through the parser.
If you are familiar with Haskell, now `f ()` is a thunk awaiting evaluation.

I won't spend more time on this here, eta-expansion can be a [useful](https://ocaml.org/manual/5.2/polymorphism.html#ss:valuerestriction) [pattern](https://stackoverflow.com/questions/25763412/why-does-ocaml-sometimes-require-eta-expansion) in OCaml.

## A concrete example: parsing S-Expressions

 Let's make this more concrete and build a parser for [lisp](https://en.wikipedia.org/wiki/Lisp_(programming_language)#Syntax_and_semantics)-style S-expressions (`sexp` from now on).
 For a brief introduction have a look at [this blog post](https://uwplse.org/2025/12/09/S-expressions.html) or [real world ocaml](https://dev.realworldocaml.org/data-serialization.html).

For what concerns us, a `sexp` is either

- an **atom**, i.e. a string for any practical purpose,
- a **list**, i.e. a sequence of `sexp`s.

To be more precise, the lists are usually delimited by parentheses (`(`, `)`) and the elements are separated by whitespaces. The atoms are space delimited strings of alphanumeric symbols.
For instance, `(= (+ 1 1) 2)` is a `sexp` that a lisp interpreter would evaluate to true.

```ocaml
module CP = MakeCharParser(Parser)
open Parser
open CP

type sexp = 
  | Atom of string
  | Lst of sexp list

let string_of_chars = List.map (String.make 1) >.> String.concat ""

let spaces = many space

let atom = 
  (fun chars -> Atom (string_of_chars chars)) <$> some alpha_num

(* S-expressions are inherently recursive, so we also wrap them in a `delay`! *)
let rec sexp () =
  delay (fun () ->
    let list_parser = 
      (fun _ elements _ -> Lst elements)
      <$> exactly '('
      <*> many (spaces *> sexp () <* spaces)
      <*> exactly ')'
    in
    atom <|> list_parser
  )

let sexp_parser = spaces *> sexp () <* spaces
```

If we run this in `utop` using our standard `run` function, we get exactly what we expect:

```ocaml
# run sexp_parser "(foo (bar 123) baz)";;
- : sexp list =
[Lst [Atom "foo"; Lst [Atom "bar"; Atom "123"]; Atom "baz"]]
```

Note that all helpers were completely general! By properly encoding the deferred evaluation into our implementation, we got the same elegant parser combinators you would expect from a purely functional language like Haskell.

It may seem a completely pointless exercise, but what we are seeing as the result of running the parser, is an Abstract Syntax Tree (AST).
This is a core concept in computer science, central to build for example compilers or to make structured sense of information.
Say that you use Wolfram Mathematica to compute integrals.
You might to something like

```Mathematica
In[1]:= sint[b_] := Integrate[Sin[x], {x, 0, b}]
In[2]:= sint[b]
Out[2]= 1 - Cos[b]
In[3]:= sint[Pi]
Out[3]= 2
```

Within Mathematica, however, these expressions are parsed into an AST which is then manipulated and perhaps simplified. You can look at it with the `FullForm` command:

```Mathematica
In[4]:= sint[b] // FullForm
Out[4]//FullForm=
    Plus[1,Times[-1,Cos[b]]]
In[5]:= sint[Pi] // FullForm
Out[5]= 2
```

In fact, the displayed text is itself an AST specifying the text that should be displayed. Copy-pasting it to a text editor would show:
```Mathematica
Out[4]//FullForm=\!\(
TagBox[
StyleBox[
RowBox[{"Plus", "[", 
RowBox[{"1", ",", 
RowBox[{"Times", "[", 
RowBox[{
RowBox[{"-", "1"}], ",", 
RowBox[{"Cos", "[", "b", "]"}]}], "]"}]}], "]"}],
ShowSpecialCharacters->False,
ShowStringCharacters->True,
NumberMarks->True],
FullForm]\)
```

But enough with this detour, let's look at a more realistic example!

## A more realistic `sexp` example: parsing simple `dune` files

Let's test our parser on a real-world configuration file, we can parse a `dune` build file.
For instance we will update the parser to be able to parse [doi2bib](https://github.com/mseri/doi2bib)'s dune file.

To make this work, we only need to slightly upgrade our parser.
Real-world S-expressions, like those used by Dune, need to handle a few extra things.
For our specific purpose it will be enough to make two changes:

1. We should allow some special characters in atoms, like `-`, `_`, `.`, `/`, and `:`, and

2. We should allow the presence of multiple `sexp`s: a dune file is a sequence of several S-expressions separated by whitespace.

At this point though, extending our parser is not such a big deal.

As we just mentioned, we first need to allow for an extended list of symbols, for instance:

```ocaml
let symbol_char = 
  alpha_num <|> one_of['_'; '-'; '.'; '/'; ':'; '*'; '+'; '=']
```

With that, we can extend our definition of atoms and add quoted strings, which are also extensively used in dune files:

```ocaml
let atom = 
  (fun chars -> Atom (string_of_chars chars)) <$> some symbol_char

let quoted_string =
  (fun _ chars _ -> Atom ("\"" ^ string_of_chars chars ^ "\""))
  <$> exactly '"'
  <*> many (none_of ['"'])
  <*> exactly '"'
```

With those two helpers at hand, the parser is practically the same as before:

```ocaml
let rec sexp () =
  delay (fun () ->
    let list_parser = 
      (fun _ elements _ -> Lst elements)
      <$> exactly '('
      <*> many (spaces *> sexp () <* spaces)
      <*> exactly ')'
    in
    atom <|> quoted_string <|> list_parser
  )
```

We only need to remember that a dune file is just a sequence of S-expressions, so we need to wrap the whole thing in `many`:

```ocaml
let dune_file_parser = many (spaces *> sexp () <* spaces)
```

Now, take the dune file to build the `doi2bib` executable, namely

```ocaml
let doi2bib_dune_content = {|
(executable
 (name doi2bib)
 (public_name doi2bib)
 (libraries lwt lwt.unix cohttp-lwt-unix ezjsonm lambdasoup re cmdliner)
 (flags (:standard -w -40)))

(rule
 (targets doi2bib.1)
 (deps doi2bib.exe)
 (action (run ./doi2bib.exe --help=groff)))
|}
```

and run the parser on it with:

```ocaml
let parsed_dune = run dune_file_parser doi2bib_dune_content
```

If you run this in `utop`, the output will confirm that our eager evaluation issue is completely solved and the parser navigates the depth of the configuration file to produce a clean AST:

```ocaml
val parsed_dune : sexp list list =
  [[Lst
     [Atom "executable"; Lst [Atom "name"; Atom "doi2bib"];
      Lst [Atom "public_name"; Atom "doi2bib"];
      Lst
       [Atom "libraries"; Atom "lwt"; Atom "lwt.unix";
        Atom "cohttp-lwt-unix"; Atom "ezjsonm"; Atom "lambdasoup"; Atom "re";
        Atom "cmdliner"];
      Lst [Atom "flags"; Lst [Atom ":standard"; Atom "-w"; Atom "-40"]]];
    Lst
     [Atom "rule"; Lst [Atom "targets"; Atom "doi2bib.1"];
      Lst [Atom "deps"; Atom "doi2bib.exe"];
      Lst
       [Atom "action";
        Lst [Atom "run"; Atom "./doi2bib.exe"; Atom "--help=groff"]]]]]
```

Note how the outer list has exactly one element containing our two parsed root nodes. This is because our parser combinator correctly consumes the entire input as a single successful parse operation!

There we have it: a fully functional, recursive Applicative parser in OCaml, driven purely by Category Theory typeclasses.
Of course, for real world use I would never recommend to use this parser.
We already have pretty solid libraries like [`csexp`](https://github.com/ocaml-dune/csexp) or [`sexplib`](https://github.com/janestreet/sexplib) that are well tested and have been used in production for years.
Similarly, if you want to write a lisp interpreter, you will need to integrate more information in the parser, like distinguishing different numerical types, quoting and unquoting `sexp` expressions, support for the basic keywords, ...
But for a blog post, I think we pushed it quite a long way.

## The complete code

To try it out, you can run the code below, it also includes the code from the previous blog post with the most relevant comments preserved.

Different parts of the code are separated into sections, so that you can copy-paste them independently, and the code is more modularized so that you can play around with it without polluting the namespace too much.

```ocaml
(*
   Basic helpers
*)
let id x = x
let const x _ = x
let flip f x y = f y x
let compose f g x = f (g x)
let (<.>) f g = fun x -> f (g x) (* <- compose *)
let (>.>) g f = fun x -> f (g x) (* first apply [g] then [f] but writing them the other way around *)
```

```ocaml
(*
   Main module types
   and the utilities that we can abstractly construct from them
*)

module type MONOID = sig
  (** Monoid *)
  type t

  (** Neutral element *)
  val mempty : t

  (** Associative operation *)
  val mappend: t -> t -> t
end

module Monoid_Utils (M: MONOID) = struct
  (** Generic Monoid helpers *)
  open M

  (** A convenient shorthand for mappend *)
  let (<+>) x y = mappend x y

  (** Any monoid can be concatenated *)
  let concat xs = List.fold_left (<+>) mempty xs
end

module type FUNCTOR = sig
  type 'a t
  val fmap: ('a -> 'b) -> 'a t -> 'b t
end

module Functor_Utils(F: FUNCTOR) = struct
  (** Generic Functor helpers *)
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

module type APPLICATIVE = sig
  type 'a t

  (* This includes the signature of FUNCTOR,
     rewriting the types to make them match *)
  include FUNCTOR with type 'a t := 'a t

  (** Lift a value *)
  val pure: 'a -> 'a t
  (** Sequential application *)
  val ap: ('a -> 'b) t -> 'a t -> 'b t

  (* Note that if you still have to define the functor,
   * you can define `fmap` from the above functions as
   * `let fmap f x = pure f <*> x` *)
end

module Applicative_Utils (A: APPLICATIVE) = struct
  (** Generic Functor helpers *)

  open A
  module FunU = Functor_Utils(A)
  include FunU

  (** A convenient infix for ap -- called apply*)
  let (<*>) f = ap f

  (* Below, we denote `actions` the elements of the applicative typeclass *)

  (** Lift a function to actions. This function may be used as a value
      for fmap in a Functor instance. *)
  let liftA f x = f <$> x
  (** Lift a binary function to actions. *)
  let liftA2 f x y  = f <$> x <*> y
  (** Lift a ternary function to actions. *)
  let liftA3 f x y z = f <$> x <*> y <*> z

  (** Sequence actions, discarding the value of the second argument. *)
  let ( <* ) r x = const <$> r <*> x
  (** Sequence actions, discarding the value of the first argument. *)
  let ( *> ) r x = (fun _ y -> y) <$> r <*> x     (* == flip ( <* ) *)

  (** Evaluate each action in the structure from left to right, and
      and collect the results. *)
  let rec sequenceA = function
    | [] -> pure []
    | x :: xs -> List.cons <$> x <*> sequenceA xs

  (** Evaluate each action in the structure from left to right, and
   *  ignore the results *)
  let sequenceA_ xs = List.fold_right ( *> ) xs (pure ())

  (** Map each element of a structure to an action, evaluate these actions
      from left to right, and collect the results. *)
  let traverseA f =  (List.map f) >.> sequenceA

  (** Map each element of a structure to an action, evaluate these
      actions from left to right, and ignore the results. *)
  let traverseA_ f xs = List.fold_right (( *> ) <.> f) xs (pure ())

  (** `forA` is 'traverse' with its arguments flipped. *)
  let forA xs = (flip traverseA) xs
end

module type ALTERNATIVE = sig
  type 'a t
  include APPLICATIVE with type 'a t := 'a t
  
  (** The identity of <|> *)
  val empty: 'a t
  (** An associative binary operation -- practically mappend *)
  val (<|>): 'a t -> 'a t -> 'a t
  
  (** Our new addition to break infinite recursion by deferring evaluation *)
  val delay: (unit -> 'a t) -> 'a t
end

module type GENERIC_TYPE_WORKAROUND = sig type t end

module Alternative_Utils (A: ALTERNATIVE) = struct
  (** Generic Alternative helpers *)
    
  open A
  module AppU = Applicative_Utils(A)
  include AppU

  module AltMonoid(T: GENERIC_TYPE_WORKAROUND): (MONOID with type t = T.t A.t) = struct
    type t = T.t A.t
    let mempty = A.empty
    let mappend = A.(<|>)
  end

  (** Zero or more *)
  let rec many p =
    A.delay (fun () -> some p <|> pure[])

  (** One or more *)
  and some p =
    List.cons <$> p <*> many p
  
  (** Always return empty *)
  let fail = empty
  
  (** Another name for concat *)
  let choose (type a) ps =
    let module AM = Monoid_Utils(AltMonoid(struct type t = a end))
    in AM.concat ps
end
```

```ocaml
(* 
   The new parser combinator. Here we need to use delay!
*)

type text = char list
type 'a p = text -> ('a * text) list

module ParserApplicative: (APPLICATIVE with type 'a t = 'a p) = struct
  type 'a t = 'a p
  let fmap f parser = parser >.> List.map (fun (c, cs) -> (f c, cs))
  let pure c = fun input -> [(c, input)]
  let ap parser_f parser = fun input ->
    match parser_f input with
    | [] -> []
    | (f, cs) ::[] -> fmap f parser cs
    | lst -> List.map (fun (f, cs) -> fmap f parser cs) lst |> List.concat
end

module ParserAlternative: (ALTERNATIVE with type 'a t = 'a p) = struct
  include ParserApplicative
  let empty _ =[]
  let (<|>) p1 p2 txt =
    match p1 txt with
    |[] -> p2 txt
    | res -> res

  let delay f = fun input -> f () input
end

module ParserAlt = Alternative_Utils(ParserAlternative)

module type PARSER = sig
  type 'a t
  
  val empty: 'a t
  val map: ('a -> 'b) -> 'a t -> 'b t
  val pure: 'a -> 'a t
  val ap: ('a -> 'b) t -> 'a t -> 'b t
  val delay: (unit -> 'a t) -> 'a t
  val ( <$> ): ('a -> 'b) -> 'a t -> 'b t
  val ( <*> ): ('a -> 'b) t -> 'a t -> 'b t
  val ( <* ): 'a t -> 'b t -> 'a t
  val ( *> ): 'a t -> 'b t -> 'b t
  
  val run: 'a t -> string -> 'a list
  val token: (char -> 'a list) -> 'a t
  
  val char: char -> char t
  val fail: 'a t
  val choose:  'a t list -> 'a t
  val (<|>): 'a t -> 'a t -> 'a t
  val many: 'a t -> 'a list t
  val some: 'a t -> 'a list t
  val filter: ('a -> bool) -> 'a t -> 'a t
end

module Parser: PARSER = struct
  include ParserAlternative
  include ParserAlt
  
  let map = fmap
  
  let explode s =
    let rec aux i acc =
      if i < 0 then acc else aux (i - 1) (s.[i] :: acc)
    in aux (String.length s - 1)[]
    
  let run p s = explode s |> p |> List.map fst
  
  let token f = function
    | [] ->[]
    | x :: xs -> List.map (fun y -> (y, xs)) (f x)
    
  let char c = token (fun c' -> if c = c' then [c] else[])
  
  let filter f p cs =
    match p cs with
    | [(x, cs)] when f x -> [(x,cs)]
    | _ ->[]
end

module MakeCharParser(P: PARSER) : sig
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
end = struct
  open P
  
  let item = token (fun c -> [c])
  
  let exactly x = filter ((=) x) item
  let one_of l = filter (fun x -> List.mem x l) item
  let none_of l = filter (fun x -> not (List.mem x l)) item
  let range l r = filter (fun x -> l <= x && x <= r) item
  
  let space = one_of [' '; '\t'; '\r'; '\n']
  let newline = exactly '\n'
  let tab = exactly '\t'
  let upper = range 'A' 'Z'
  let lower = range 'a' 'z'
  let digit = range '0' '9'
  let letter = lower <|> upper
  let alpha_num = letter <|> digit
  let hex_digit = range 'a' 'f' <|> range 'A' 'F' <|> digit
  let oct_digit = range '0' '7'
end
```

```ocaml
(* 
   Our first `sexp` parser
*)

module SexpParser = struct
  type sexp = 
    | Atom of string
    | Lst of sexp list
  
  module CP = MakeCharParser(Parser)
  include Parser
  include CP
  
  open Parser
  open CP
  
  let string_of_chars = List.map (String.make 1) >.> String.concat ""
  
  let spaces = many space
  
  (* An atom is one or more alphanumeric characters *)
  let atom = 
    (fun chars -> Atom (string_of_chars chars)) <$> some alpha_num
  
  (* `sexp`s are inherently recursive, so we wrap them in a delay too! *)
  let rec sexp () =
    delay (fun () ->
      let list_parser = 
        (fun _ elements _ -> Lst elements)
        <$> exactly '('
        <*> many (spaces *> sexp () <* spaces)
        <*> exactly ')'
      in
      atom <|> list_parser
    )
  
  let sexp_parser = spaces *> sexp () <* spaces
end

let test1 = SexpParser.(run sexp_parser "foo")
let test2 = SexpParser.(run sexp_parser "(foo bar baz)")
let test3 = SexpParser.(run sexp_parser "(foo (bar 123) baz)")
```

```ocaml
(* 
   A `sexp` parser for dune files
*)

module DuneSexpParser = struct
  type sexp = 
    | Atom of string
    | Lst of sexp list
  
  module CP = MakeCharParser(Parser)
  include Parser
  include CP
  
  open Parser
  open CP
  
  let string_of_chars = List.map (String.make 1) >.> String.concat ""
  
  let spaces = many space
  
  let symbol_char = 
    alpha_num <|> one_of ['_'; '-'; '.'; '/'; ':'; '*'; '+'; '=']
  
  let atom = 
    (fun chars -> Atom (string_of_chars chars)) <$> some symbol_char
  
  let quoted_string =
    (fun _ chars _ -> Atom ("\"" ^ string_of_chars chars ^ "\""))
    <$> exactly '"'
    <*> many (none_of ['"'])
    <*> exactly '"'
  
  let rec sexp () =
    delay (fun () ->
      let list_parser = 
        (fun _ elements _ -> Lst elements)
        <$> exactly '('
        <*> many (spaces *> sexp () <* spaces)
        <*> exactly ')'
      in
      atom <|> quoted_string <|> list_parser
    )

  let dune_file_parser = many (spaces *> sexp () <* spaces)
end

let doi2bib_dune_content = {|
(executable
 (name doi2bib)
 (public_name doi2bib)
 (libraries lwt lwt.unix cohttp-lwt-unix ezjsonm lambdasoup re cmdliner)
 (flags (:standard -w -40)))

(rule
 (targets doi2bib.1)
 (deps doi2bib.exe)
 (action (run ./doi2bib.exe --help=groff)))
|}

let test_parsing_dune_file = DuneSexpParser.(run dune_file_parser doi2bib_dune_content)
```

### A simpler additional example

We have not discussed this specific example in the post, but I thought it was interesting to show a case in which the delay is not really needed, and how this does not really get in the way of the implementation.

```ocaml
(* 
   Option modules: here there is no recursion, so delay takes a particularly
   simple form
*)

module OptionF: (FUNCTOR with type 'a t = 'a option) = struct
  type 'a t = 'a option
  let fmap f = function
    | Some x -> Some (f x)
    | None -> None
end

module OptionA: (APPLICATIVE with type 'a t = 'a option) = struct
  include OptionF
  let pure x = Some x
  let ap f x =
    match f, x with
    | Some f, Some x -> Some (f x)
    | _ -> None
end

module OptionAlternative: (ALTERNATIVE with type 'a t = 'a option) = struct
  include OptionA
  let empty = None
  let (<|>) o1 o2 =
    match o1 with
    | Some _ as res -> res
    | None -> o2

  let delay f = f ()
end
```

```ocaml
(*
   A test with Option
*)

module OptionExample = struct
  open OptionAlternative
  module OptAlt = Alternative_Utils(OptionAlternative)
  open OptAlt
  
  (* Imagine looking up a database port from multiple sources: *)
  let get_env_var () = None           (* For example the variable was not set *)
  let get_config () = Some 5432       (* But is in the local config file *)
  let get_default () = Some 8080      (* And we have a default value *)
  
  (* We can use OptAlt to chain fallbacks: the first `Some` wins automatically. 
    Recall from the previous blog post that `<|>` means
    "try the left side; if it is None, fall back to the right side." *)
  let resolved_port = get_env_var () <|> get_config () <|> get_default () 
  (*  val resolved_port : int OptionAlternative.t = Some 5432 *)
  
  (* Suppose we require three specific settings to start a server *)
  let required_configs =[
    Some "localhost"; 
    Some "admin"; 
    Some "secret_password"
  ]
  
  (* We can use sequence to encode an all or nothing scenario.
  	Again, from the previous blog post `sequenceA` means
  	"if everything in this list is Some, give me a Some list;
  	 if even one is None, fail the whole thing." *)
  
  let test_success = sequenceA required_configs
  
  (* But if even one is missing, so None, ... *)
  let missing_configs =[
    Some "localhost"; 
    None; (* Missing username! *)
    Some "secret_password"
  ]
  
  let test_failure = sequenceA missing_configs
end

let test_opt_1 = OptionExample.test_success
let test_opt_2 = OptionExample.test_failure
```
