Id: 18,
Title: On iTerm2 and  solarized dark
Date: 2013-12-07T18:45:37.000Z
Modified: 2013-12-07T18:49:21.000Z
Tags:
Category: Blog
Slug: on-iterm2-and-solarized-dark
Authors: Marcello Seri

This weekend I've spent some time to understand [Z Shell](http://en.wikipedia.org/wiki/Z_shell). I admit that I've should have done it ages ago. I actually regret not having done it ages ago, I would have saved a lot of time.

Moving your `.bashrc` to your new `.zshrc` is almost just copy and paste. And you suddently find yourself with a shell that makes you feel in the future!

If you additionally install [oh my zsh](https://github.com/robbyrussell/oh-my-zsh), _the only thing that your shell will be missing is the capability of making coffee_. The official description is literally true:

>  oh-my-zsh is an open source, community-driven framework for managing your ZSH configuration. It comes bundled with a ton of helpful functions, helpers, plugins, themes, and few things that make you shout…
>
> **“OH MY ZSHELL!”**

Being in a time for changes, I decided it was time to change my prompt and my usual color scheme. I've been already using [Solarized](http://ethanschoonover.com/solarized) in vim and Sublime Text for quite some time now, and it seemed a reasonable choice.

I downloaded it and installed it on osx Terminal. Everything went fine and the terminal was correctly showing the new colour set. The real problem appeared when I installed the colour scheme for [iTerm2](http://www.iterm2.com/) (my favourite term on osx)... I kept getting a greyscale coloroscheme (on the right in the screenshot), something very different from the expected output (left terminal in the picture). 

![On the left you can see the correct color scheme, on the right the one that I was getting](/images/18-term.png)

I wasted at least half an hour before I figured out what was the problem: in my previous color scheme I liked to have bright colours in the output... and **Solarized bright colours are basically a greyscale**!

Fix it is extremely fast:

* go to `iTerm -> Preferences -> Profiles`
* select the Profile that is using the Solarized colour scheme
* open the `Text` tab
* uncheck the `Text Rendering` option `Draw bold text in bright colors`
* enjoy

