Id: 29,
Title: Installing Scientific Python 3 libraries on OSX (and julia with IJulia)
Date: 2014-04-15T13:35:03.000Z
Modified: 2014-04-15T15:00:24.000Z
Tags:
Category: Blog
Slug: installing-scientific-python-3-libraries-on-osx-and-julia-with-ijulia
Authors: Marcello Seri

In a recent post, I tried to explain how to  [install scientific python libraries on OSX and get rid of the most common errors](https://www.mseri.me/installing-scientific-python-libraries-on-osx/). In that case everythong I did was for python 2.7.

Yesterday I decided to fully move to python 3.4. I've removed my python installation via homebrew and with it all the installed packages.

Moving to python 3 is straightforward if you have done the procedure described in [my previous post](https://www.mseri.me/installing-scientific-python-libraries-on-osx/), it all really reduces to replace every occurrence of `python` in that post with `python3` and every occurrence of `pip` with `pip3`. 

Assuming that you had installed homebrew, fortran and pkg-config as explained there, what you have to do is just type and exectute the following:
```
brew install python3
pip3 install numpy
pip3 install scipy
pip3 install matplotlib
```

And for `qutip` you just do
```
pip3 install cython
pip3 install qutip
```

### A better IPython

In the [last post](https://www.mseri.me/installing-scientific-python-libraries-on-osx/) we installed ipython with a minimal working configuration. Recently I started enjoying writing my simulation with the notebooks of iJulia (we will discuss it soon) and [iPython](http://ipython.org/notebook.html): two very nice web based environment to write (and execute) your code.

To run the iPython notebook one should type
```
ipython notebook
```
or, if using python 3,
```
ipython3 notebook
```

If you try to do it, your should get some errors. Luckily these are very easily solved installing the following packages (if you use python 2 replace `pip3` with `pip`):
```
brew install libzmq
pip3 install pyzmq jinja2
```

If you now run, let's say, `ipython3 notebook`, after a moment you should see a new browser window with your notebook.

- - - - - - 

## Julia for fast computations

[Julia](http://julialang.org) is a recent "high-level, high-performance dynamic programming language for technical computing" developed as an open source project at MIT. It is extremely fast and powerful but as readable as python (if not more).

It can nicely and simply interface with C, Fortran and Python and is [bloody fast](http://julialang.org/benchmarks/).

I've been using it for the exercises of NLP in coursera and some simulations and I really enjoy it.

To install julia you have few alternatives. You can grab a [binary precompiled installer from the official website](http://julialang.org/downloads/), install the nice (open source and free) IDE [Julia Studio](http://forio.com/products/julia-studio/) or use homebrew (my first choice):

```
brew tap staticfloat/julia
brew install --64bit julia
```

If you get errors, or you want to install the support for gnuplot plots, I [redirect you to the github page of hoembrew-julia](https://github.com/staticfloat/homebrew-julia), where you can find all the additional information you may need.

After having installed julia, open a terminal and run `julia` or open Julia Studio, and have fun!

There are many resources to learn coding in julia. If you don't want to read the full docs (they are pretty short, is not a big deal) you can use the resources linked at the [Teaching Julia page](http://julialang.org/teaching/), in particular you may find easy to start with [Julia Tutorial](http://nbviewer.ipython.org/github/JuliaX/JuliaTutorial/blob/master/JuliaTutorial.ipynb), with [Learn X in Y minutes](http://learnxinyminutes.com/docs/julia/) or with the [series of Julia Studio tutorials](http://forio.com/products/julia-studio/tutorials/).

After you played a bit with it. The time to install some packages arrives. The most important, imho, is [IJulia](https://github.com/JuliaLang/IJulia.jl). A kernel for IPython that lets you write your julia code in a ipython notebook. Inside the julia environment (namely, after having opened a terminal and run `julia`) execute the following
```
julia> Pkg.add("IJulia")
```
This will download IJulia and a few other prerequisites, and will set up a Julia profile for IPython.

Notice that `julia> ` is julia's shell prompt, you don't have to type it. It must be already there after you run julia.

To use IJulia you just need to run
```
ipython3 notebook --profile julia
```
and eventually make an alias out of it if you plan to use it often. A simple IJulia tutorial from the MIT can be found [on IPython website](http://nbviewer.ipython.org/url/jdj.mit.edu/~stevenj/IJulia%20Preview.ipynb).

Additionally you may want to install `PyPlot` and `Winston` for plots. You can find a [list of available packages and their description on Julia website](http://docs.julialang.org/en/latest/packages/packagelist/" target=_"blank) or with a search on google or on [GitHub](http://www.github.com).

To understand how to make complex plots with matplotlib using julia's pyplot interface I've found the following post extremely useful: [Naval Warfare with JuMP + Julia](http://iaindunning.com/2014/subs-battleships.html).