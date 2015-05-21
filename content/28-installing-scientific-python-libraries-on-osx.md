Id: 28
Title: Installing scientific python libraries on OSX
Date: 2014-02-19T19:06:40.000Z
Modified: 2015-01-13T21:09:40.000Z
Tags: tutorial, homebrew, matplotlib, numpy
Category: Blog
Slug: installing-scientific-python-libraries-on-osx
Authors: Marcello Seri

For a recent project, I had the necessity to install (or update) some of the scientific python libraries that I use for computation (and to avoit matlab). I was  aware of [a not too recent tutorial](http://www.thisisthegreenroom.com/2011/installing-python-numpy-scipy-matplotlib-and-ipython-on-lion/) in regard that left me quit unhappy at the time, in particular I strongly disagree with their practice of changing OSX official symlinks to point at the new Python install. 

Given that I am not alone in the project, I decided to write a short tutorial trying to include all the necessary steps for a successful installation of python, numpy, scipy, matplotlib, ipython and qutip.

## Get XCode
The first essential step is to make sure that you have installed [XCode](https://developer.apple.com/xcode/) (since OSX Lion you will find it on the AppStore). If you don't or you don't know what we are talking about I refer you to Google (or DuckDuckGo). A priori we will just need the command line tools.

## Convert yourself to Homebrew
Then let's install a serious package manager, and with this I really mean: install [Homebrew](http://brew.sh)!

If you don't have it yet, open a Terminal and install it copying and pasting the following code:

    :::sh
    ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"

You shouldn't need  `sudo` for the installation, everything will be nicely located in `/usr/local`. When the execution ends add this to your `.profile` (or `/bash_profile` or `.zsh_profile` or the equivalent for your shell):

    :::sh
    export PATH=/usr/local/bin:$PATH

## Install gfortran
We will not use it directly but it will be required to install scipy and it is going to take some time, so let's deal with it now. **Close and reopen the terminal to reload the new environment's variables** and run:

    :::sh
    brew install gfortran

Easy, no?? Now just wait for the magic to happen.

## Install an updated version of Python
I know that OSX is shipped with its own python install, but that's the outdated system one. Leave it to the system and do not mess with it! We are going to install a more recent version of python in parallel. With Homebrew is  very simple, just execute the following command.

    :::sh
    brew install python

If you did everything correctly, running `which python` you should read `/usr/local/bin/python`. And now that we have python, let's install a nice package manager for it. Install pip with `easy_install pip`.

## Install numpy and scipy
That's now very easy with pip:

    :::sh
    pip install numpy
    pip install scipy

(I run them separately to have a more direct control of the possible errors)

There are some possible problems here. On my laptop and my office computer I had `gfortran` complaining with the following error

    :::sh
    gfortran: error: libgfortran.spec: No such file or directory 

I could fix the problem with

    :::sh
    brew link --overwrite gfortran 

Moreover, in an old installation, I had randomlike errors appearing here and then. I don't really know the cause, but I temporarily solved installing the development version of scipy

    :::sh
    pip install -e git+https://github.com/scipy/scipy#egg=scipy-dev

Give it a try if you keep having troubles.

## Install matplotlib
For this you will first need to install pkg-config. But it's as easy as

    :::sh
    brew install pkg-config

After it finishes its job, simply run

    :::sh
    pip install matplotlib

Note that if you keep having an error related to `png.h` you may want to `brew install lipng` or, as I've read on stackoverflow I think, `brew install freetype`. Additionally, if you get an error related to freetype headers, you have to do the following:

    :::sh
    sudo ln -s  /usr/local/include/freetype2/ /usr/include/freetype

If you are still not able to install it, try the development version like I suggested for scipy:

    :::sh
    pip install git+git://github.com/matplotlib/matplotlib.git

## Almost done
Hopefully everything is installed properly now. Run python and try the following imports

    :::python
    import numpy
    import scipy
    import matplotlib

They should proceed with no errors.

## Last but not least
To have a nicer interface to test our code I strongly encourage you to install ipython. Simply run 

    :::sh
    pip install ipython

and the next time you will need the python intepreter use

    :::sh
    ipython

Have fun!!!

- - - - - -

## A final remark for Max
We are probably going to use [QuTiP](http://qutip.org) too. Its setup is quite straightforward, simply run

    :::sh
    pip install cython
    pip install qutip

and it's installed. You can test the installation pasting the following code in ipython (courtesy of [Introduction to QuTiP](http://nbviewer.ipython.org/github/jrjohansson/qutip-lectures/blob/master/Lecture-0-Introduction-to-QuTiP.ipynb))

    :::python
    from qutip import *
    q = Qobj([[1],[0]])
    q

If you get as output 

    Quantum object: dims = [[2], [1]], shape = [2, 1], type = ket
    Qobj data =
    [[ 1.]
     [ 0.]]

then the installation was fine.

Have a look at the official [Tutorials page](http://qutip.org/tutorials.html) it is quite fun!

- - - - - -
Edit: updated Homebrew install link