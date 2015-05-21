Id: 31
Title: Move to ghc 7.8.2 on MacOSX
Date: 2014-06-01T15:17:42.000Z
Modified: 2014-06-02T11:51:51.000Z
Tags: tutorial, cabal, ghc 7.8, setup, haskell
Category: Blog
Slug: move-to-ghc-7-8-2-on-macosx
Authors: Marcello Seri

Lately I've been playing with some functional languages: [haskell](http://www.haskell.org/), lisp (in particular the scheme dialect, see e.g. [chicken](http://www.call-cc.org) or [racket](http://racket-lang.org)) and [elixir](http://elixir-lang.org) (I very much like it and I really appreciate that it runs on the erlang VM).

Each of those has something pretty unique and I believe is very worth learning. I cannot stress how much material you can find both online and in libraries to learn them (except for elixir but its website does a really good job and there will be plenty of books very soon out) and how strong thay can change your way of programming. 

This post is about installing a recent version of `gch` to play with haskell. 

I started using haskell by installing `ghc`, the Glasgow Haskell Compiler (pretty much the de fact standard of haskell compilers), via Homebrew. And then installing `haskell-platform` (again using Homebrew) to find out, not much later, that I only needed the `cabal-install` package (at that time installed via Homebrew too after removing the platform).

Recently, `ghc` reached version `7.8`, and that shipped a huge amount of improvements. With my huge disappointemnt, all the packages installed via Homebrew were supporting only ghc 7.6 and I had hard times with dependencies, multiple packages and so on...

The solution was pretty simple and straightforward in the end, and I believe this could be handy for other people too strognly enough to write this post.

First of all I uninstalled ghc 7.6, cabal-install or haskell platform (if you have it). Then I reinstalled the 7.8 branch of ghc, thanks to Homebrew that was pretty straightforward:

    :::sh
    brew install ghc --devel

Additionally I had to remove the `.cabal` and `.ghc` folder in my home. There were pieces of configurations that were creating some conflicts, move them if you feel unsure and want to avoid the deletion. 

Then I needed `cabal-install`. This requires slightly more work, especially it didn't quite work for me when I followed [the instructions](http://www.haskell.org/haskellwiki/Cabal-Install).

First download the sources for `cabal-install` from [here](http://www.haskell.org/cabal/download.html). Just the `cabal-install tool` sources, it is going to update the `Cabal` library during its setup.

Untar the file, e.g.

    :::sh
    tar zxvf cabal-install-1.20.0.2.tar.gz

and enter the newly created folder, e.g

    :::sh
    cd cabal-install-1.20.0.2

Now it all reduces to run

    :::sh
    ./bootstrap.sh --no-doc

(append `--global` if you prefer to install it in `/usr/local` instead of `$HOME/cabal`).

The `--no-docs` flag seemed necessary to avoid a number of errors appearing in the compilation process and forcing me to install a number of packages by hand. Sadly I could not figure out the problem in the script yet, but that flag seems a reasonable workaround and I will install the docs later anyhow.

You may still get some error related to broken package, in such cas just `ghc-pkg unregister <brokenpackagename>` and rerun the script (in my case they were `text` and `mtl`).

When cabal is installed it is a good idea to run

    :::sh
    cabal update

and follow the instructions.

Remember that `.cabal/bin` must be in your `$PATH`.

To learn coding in haskell there are few great sources. I think [Learn yourself a Haskell for Great Good!](http://learnyouahaskell.com) is a good place to start, maybe not perfect and not complete but I really really enjoied it (and learnt a lot).

## Essential Packages for Using Haskell

Now, this section is mainly for my personal records. There is a number of packages I like to have installed for customizations, help and other stuff. Maybe some of those could interest some reader. Some of the installations will require sensible compilation times and overheating of your machine, it very much feels like installing `gentoo` ~10 years ago... some of you know what I mean :)

I rely very much on [hoogle](http://www.haskell.org/hoogle/) when I code in haskell. Best part of it is that you can have it offline. First install the appropriate package with `cabal install hoogle`. 

You may be get a warning and be asked to run the install with the flag `--force-reinstall`. Just do it: `cabal install hoogle --force-reinstall`.

I've additionally got a strange error related to `happy` and `haskell-src-exts`, it can be solved just by `cabal install happy`. I am still wondering why it happened.

When the setup is complete, you can run `hoogle data` to create a local database of entries, or `hoogle data all` if you want the complete hoogle dataset (this takes a loooong time).

If you don't plan to use `goa` or `lambdabot` you can integrate `hoogle` in `ghci` by adding 

    :::haskell
    :def hoogle \str -> return $ ":! hoogle --count=15 \"" ++ str ++ "\""

to your `.ghci` file.

I believe that `ghci` is nothing without [lambdabot](http://www.haskell.org/haskellwiki/Lambdabot). Therefore `cabal install goa lambdabot` is the inevitable second step. Note that `goa` is not a mistake but a [useful addition](http://hackage.haskell.org/package/goa).

`lambdabot <= 4.3.0.1` have some problems with `ghc-7.8.2` and you will get a compilation error. To fix it you first `cabal install goa` by itself, then `cabal get lambdabot; cd lambdabot-4.3.0.1` and then you need to replace the content of `src/Lambdabot/Monad.hs-boot` with

    :::haskell
    {-# LANGUAGE RankNTypes #-}
    module Lambdabot.Monad where

    import Control.Monad.Reader
    import Data.IORef

    data IRCRWState
    data IRCRState
    newtype LB a = LB {runLB :: ReaderT (IRCRState, IORef IRCRWState) IO a} 

    instance Monad LB

(the above code is due to [artella-coding](https://github.com/mokus0/lambdabot/pull/79) and should be merged in the next release of lambdabot). 
Then save and run `cabal configure && cabal install`.

Then in my `.ghci` I have

    :::haskell
    :m - Prelude
    :m + GOA
    setLambdabotHome "/Users/marcelloseri/.cabal/bin"
    :def bs        lambdabot "botsnack"
    :def pl        lambdabot "pl"
    :def unpl      lambdabot "unpl"
    :def redo      lambdabot "redo"
    :def undo      lambdabot "undo"
    :def index     lambdabot "index"
    :def docs      lambdabot "docs"
    :def instances lambdabot "instances"
    :def hoogle    lambdabot "hoogle"
    :def source    lambdabot "fptools"
    :def where     lambdabot "where"
    :def version   lambdabot "version"
    :def src       lambdabot "src"

I like to see what my code should look like. Often [hlint](http://community.haskell.org/~ndm/hlint/) is of great help for this (especially when you run it directly in your favourite editor, e.g. `vim` and `Sublime Text`): thus `cabal install hlint`.

Ans speaking of editors we cannot forget [ghc-mod](http://www.mew.org/~kazu/proj/ghc-mod/en/ghc-mod.html) to provide the integration: `cabal install ghc-mod`.

Finally I massively use `pandoc`, look at [its webpage](http://johnmacfarlane.net/pandoc/) if you don't know it. You can installe prebuild binaries but recently I restarted enjying compiling things by myself. The installation via `cabal` is trivial. Just type `cabal install pandoc` and wait. Maybe go to get some coffee... it's not going to be just a couple of minutes. It may fail complaining about `alex`, in such case just run `cabal install alex` and run `cabal install pandoc` again.

Now that my `.cabal` folder is quite huge, I have everything I want to have fun with haskell.

I happen to use many more haskell packages in fact (e.g. `aeson` for the `json` integration) but I usually install them in [local sandboxed environment](http://www.haskell.org/cabal/users-guide/installing-packages.html#developing-with-sandboxes) and try to keep the global user folder more or less stable.