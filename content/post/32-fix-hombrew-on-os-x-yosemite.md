---
title: "Fix Hombrew on OS X Yosemite"
date: 2014-06-03T15:58:37.000Z
lastmod: 2014-08-29T10:40:50.000Z
tags: ["fix", "homebrew", "yosemite"]
categories: ["Blog"]
slug: "fix-hombrew-on-os-x-yosemite"
disqus_identifier: 32
---

If for some reasons you've been crazy enough to install the first developer beta of Mac OSX 10.01 Yosemite, you've probably noticed that [Homebrew](https://brew.sh/) stopped working.

One possible fix is to delete homebrew and reinstall everything following this [gist](https://gist.github.com/jpincheira/bd3698fee46735fac252). But I am too lazy and too attached to my list of installed packages to accept it.

The first error I've got while running `brew update` was related to _missing system ruby 1.8_. This appears because OSX finally updated to `ruby 2.0` and this conflicts with the static link saved in one of Hombrew executables.

------

**Update**: as of this morning Homebrew has been fixed, you will not need to modify Hombrew's files if you update to Yosemite after having run `brew update`.

If you did update the files as above and get a _failed merge_ error, you will need to edit them again and fix the merge. On top of each file you will see something like

    <<<<<<< HEAD:mergetest
    Your changes
    =======
    Something new
    >>>>>>> 4e2b407f501b68f8588aa645acafffa0224b9b78:mergetest

Delete everything except for the 'Something new' line. Then save and in the end run `cd $(brew --repository) && git commit -a -m 'fix brew update'`

------

The fix is quite simple. I opened `vim /usr/local/Library/brew.rb` and replaced the `1.8` in the shebang at the beginning of the file with `2.0`.
And the same must be required for `/usr/local/Library/ENV/4.3/xcrun`, `/usr/local/Library/ENV/4.3/clang` and `/usr/local/Library/ENV/4.3/cc`.

But that's not enough. We still have to add and commit the changes: `cd $(brew --repository) && git commit -a -m 'fix ruby 2'`

Running `brew update` still complains. I needed two additional fixes. First `mkdir /Library/Caches/Homebrew` and second you will need to install `XCode 6 beta` (if you have access to Yosemite I assume that you have access to XCode too) and then install the command line tools (you can download them from Apple's developer center).

You may encounter additional errors. The [relative Issue page on Homebrew's git repo](https://github.com/Homebrew/homebrew/issues/29795) seems quite crowded at the moment.

