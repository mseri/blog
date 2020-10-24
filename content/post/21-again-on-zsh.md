---
title: "Again on zsh"
date: 2013-12-18T18:45:04.000Z
lastmod: 2013-12-18T18:50:12.000Z
tags: ["long life to zsh", "prezto", "custom theme"]
categories: ["Blog"]
slug: "again-on-zsh"
disqus_identifier: 21
---

I already wrote about the great pleasure of moving to zsh in a previous post, but I feel that I should update you on the progresses.

From the last time I moved from Oh-My-Zsh to [Prezto](https://github.com/sorin-ionescu/prezto), a different [_dotfiles framework_](https://dotfiles.github.io). I've found it much lighter and faster than oh-my-zsh, despite not having the same amount of plugins and themes. 

In fact, as far as I understood, prezto was born as a fork of oh-my-zsh and was later completely rewritten to be more zshish and better optimised. 

I must say that it cover all the plugins that I need and it feels sensibly faster and nicer on OSX and on the Raspberry Pi.

The setup requires three steps instead of just one but it's worth doing it.

If you already use zsh I suggest you to make a backup copy of your configuration. It's enough to do the following from a terminal:

    :::sh
    $ cd ~
    $ tar czf zshBackup.tar.gz .z* .oh-my-zsh

(remove `.oh-my-zsh` from the line if you have not installed it)

Then go to the [Prezto GitHub page](https://github.com/sorin-ionescu/prezto) and follow the instructions there. 

To avoid too many jumps I am copying them here:

0. Clean your previous Zsh configuration (**create a Backup copy of the files before proceeding!!!**)

        :::sh
        rm -r .z* .oh-my-zsh
        
1. Launch Zsh:

        :::sh
        zsh

2. Clone the repository:

        :::sh
        git clone --recursive https://github.com/sorin-ionescu/prezto.git "${ZDOTDIR:-$HOME}/.zprezto"

3. Create a new Zsh configuration by copying the Zsh configuration files provided:

        :::sh
        setopt EXTENDED_GLOB
        for rcfile in "${ZDOTDIR:-$HOME}"/.zprezto/runcoms/^README.md(.N)
        do
            ln -s "$rcfile" "${ZDOTDIR:-$HOME}/.${rcfile:t}"
        done

4. Set Zsh as your default shell (if it is not):

        :::sh
        chsh -s /bin/zsh

5. Open a new Zsh terminal window or tab.

At this point you can happily see your new zsh theme.
Prezto comes with many available plugins, I suggest you to look at the [Modules page on Prezto's GitHub](https://github.com/sorin-ionescu/prezto/tree/master/modules#modules) or at the `README` file in `.zprezto/modules`.

To enable the modules is enough to open `.zpreztorc` with your favourite editor and look for a block that looks like:

    # Set the Prezto modules to load (browse modules).
    # The order matters.
    zstyle ':prezto:load' pmodule \
      'environment' \
      'terminal' \
      'editor' \
      'history' \
      'directory' \
      'spectrum' \
      'utility' \
      'git' \
      'archive' \
      'homebrew' \
      'osx' \
      'ssh' \
      'completion' \
      'prompt'

Walking through the file you may enable/disable/setup a lot of behaviours and functionalities, have a look at it.

In particular I wanted back my custom theme... To enable and customise themes is a bit tricky (but not too much).

I mimicked what they did in [YADR](https://github.com/skwp/dotfiles) (another very interesting dotfiles repository for zsh, vim, sublime text and iterm) and built mine.

1. First of all you need to create a new folder
      
        :::sh
        $ mkdir ~/.zsh.prompts
   
    where you are going to save your theme.

2. Modify the `Prompt` section of `.zpreztorc` to look like 
        
        :::sh
        # Set the prompt theme to load.
        # Setting it to 'random' loads a random theme.
        # Auto set to 'off' on dumb terminals.
        # zstyle ':prezto:module:prompt' theme 'sorin'
        autoload promptinit
        fpath=($HOME/.zsh.prompts $fpath)
        promptinit

        zstyle ':prezto:module:prompt' theme 'YOURTHEMENAME'

    where `YOURTHEMENAME` is the name that you have chosen for your theme.
 
3. Create your theme file in `.zsh.prompts`. Note that its name must be `prompt_YOURTHEMENAME_setup`, otherwise it will not be recognised.
 
  I have no real advice on the creation of a theme. I posted [my theme on gist](https://gist.github.com/mseri/8026965) if you want to try it or you want to use it as a starting point. It is a slightly modified version of YADR's steeef simplified theme.

You may find the function provided in [oh-my-zsh's spectrum file](https://github.com/robbyrussell/oh-my-zsh/blob/master/lib/spectrum.zsh) helpful. For example it is enough to type the following in your Zsh terminal to see all the colours available

    :::sh
    for code in {000..255}; do
        print -P -- "$code: %F{$code}Test%f"
    done

Or, for something similar, have fun and try

    :::sh
    for code in {000..255}; do
        ((cc = code + 1))
        print -P -- "$BG[$code]$code: Test %{$reset_color%}"
    done

Have fun. Thanks to zsh and [iTerm2](https://www.iterm2.com/#/section/home) I am happily going back to use [vim](https://www.vim.org) but that's another story...