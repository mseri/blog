---
title: "A brief introduction to git, with an eye towards mathematicians"
date: 2024-02-29T14:56:34+01:00
tags: ["git", "mathematics"]
categories: ["Blog"]
slug: "a-brief-intro-to-git"
toc: true
---

This is a followup to my [previous post on git from 11 years ago]({{< ref "/posts/11-git-workflow-for-lazy-mathematicians.md" >}}).
I've been using git for a while now and I've learned a few things since then, that I think are worth sharing.

I am not going to explain in detail what git is, how to install it and how it works; there are plenty of resources for that.
It will be enough for our purposes to know that [`git`](https://git-scm.com) is a version control system that allows you to keep track of changes in your files and collaborate with others.

Since I last wrote about this, git has evolved a lot and many new features have been added.
This has made some of the old workflows obsolete and introduced new ones that are more efficient and easier to use.
It took a long time for me to break my old habits and adopt the new ones, but I think it was worth it and I have the impression they are not known and advertised widely enough to really make a dent in the old traditions.

## Getting started

There is nothing new here.
You need to install `git`, which pretty much will depend on the operating system running in your computer, and [configure it with your name and email]({{< ref "/posts/11-git-workflow-for-lazy-mathematicians.md#introduce-yourself-to-git" >}}).

## Creating a repository

The first thing you need to do is to create a repository.

This is done with the `git init` command, for example
```bash
; git init my-tex-repo
```
will create a new directory `my-tex-repo` and initialize it as a `git` repository.

I suggest you immediately add a special file, called `.gitignore`, to the repository.
This file contains a list of patterns that tell `git` which files to ignore.
For example, you might want to ignore all files with the extension `.log`, `.aux` or all files in a directory called `build`.

The easiest way to create this file is to download a pre-made one from the internet.
You can fid a list of `.gitignore` files for different programming languages and tools at [github/gitignore](https://github.com/github/gitignore).

Since this file is specific to your project, you should simply copy the relevant one to your repository and rename it to `.gitignore`.

In this case, we want to work with LaTeX files, so we can download the `.gitignore` file for LaTeX.
```bash
; curl -o .gitignore https://raw.githubusercontent.com/github/gitignore/master/TeX.gitignore
```
## Adding files and committing changes

Now that we have a file in our `git` repository we need to tell `git` to start tracking it.
This is done with the `git add` command.
For example, let's add the `.gitignore` file that we just downloaded to the repository.
```bash
; git add .gitignore
```
Note that this is not enough to actually save the file in the repository:
this command only tells `git` to start tracking the file and be prepared to store the changes
(in this case the creation of the file with its specific content) into its internal "database".

To store these changes, we need to commit them with the `git commit` command.
```bash
; git commit -m "Add .gitignore file"
```

The message we added with `-m` is a short description of the changes we are committing.
It is important to write a good message, because it will help you and others understand what the changes are about.

This workoflow, of adding _changes_ to track and then committing them, is at the core of
using `git`. And I really want to emphasize that it is about _changes_ and not _files_.

Let's add a new file
```bash
; echo "Hello, world!" > main.tex
; git add hello.tex
; git commit -m "Add main.tex file"
```

If I modify this new file and I want to store the new versionm, I need to add the file again and then commit the changes: `git` will store the changes, not the file!
```bash
; echo "Hello, world! Again!" >> main.tex
; echo "At some point we should start writing latex instead..." >> main.tex
; git add main.tex
; git commit -m "Change main.tex file"
```

If you have made lots of edits and are unsure which ones have been added, you can use `git status` to see which files have been modified and which have been added to the repository.
I find the full output of this command a bit too verbose, so I usually use the `-st` flags to get a more compact and readable one.
```bash
; git status -st
```

Sometimes you want to selectively add only some of the changes in a file.
This is done with the `git add -p` command.
```bash
; git add -p main.tex
```
This will interactively show you the changes that have been made to the file and ask you if you want to add them to the repository.
You can then choose which changes to add for consideration in the new commit and which to ignore.
The changes that you choose to ignore will be kept in the file, but they will not be added to the repository.

## Tracking changes

To see the changes that we have committed, the `git log` command is your friend.
```bash
; git log
```
This will show the history of the changes that have been committed to the repository, with the author, the date and the message of each commit.

If you want to see the changes that have been made to a file in a specific commit, you can then look them up with the `git show` command.
```bash
; git show <commit-hash> main.tex
```
This will show the changes that have been made to the file `main.tex` in the commit with hash `<commit-hash>` (that you can read from the `git log` output).
Note that you don't need to write the full hash, just enough characters to uniquely identify the commit.
Usually 4 or 5 characters are enough.

## Reverting changes

At some point you realised that you made a mistake and you want to revert to a previous version of the file.
This is done with the `git restore` command.
Executing
```bash
; git restore main.tex
```
will revert the file `main.tex` to the last committed version, getting rid of any changes that have been made since then.

You can also restore the file using the version from a previous commit, by specifying the commit hash.
```bash
; git restore --source <commit-hash> main.tex
```
This will restore the file `main.tex` to the version it had in the commit with hash `<commit-hash>`.

If you have added some changes for tracking with `git add` and you want to ignore them for now, you can use the `git restore --staged` command.
```bash
; git restore --staged main.tex
```
This will not revert the changes in the file, but it will remove them from the list of changes that are going to be committed.

Similarly as for `git add`, you can use the `-p` flag to interactively choose which changes to restore.
```bash
; git restore -p main.tex
```
Instead of restoring the whole file to a previos state, this will allow you to selectively choose which changes to restore and which to keep.

The nice thing about `git restore` is that it is a very powerful command that can be used to restore files, directories, and even the whole repository to a previous state, without modifying the previous history of the repository and the previous commits.

## Removing files

If you want to remove a file from the repository, you can use the `git rm` command.
```bash
; git rm main.tex
```
This will remove the file `main.tex` from the repository and from the working directory.
If you need to remove a whole folder and all its contents, you need to use the `-r` flag, otherwise the operation will fail.
```bash
; git rm -r my-folder
```
This will remove the folder `my-folder` and all its contents from the repository and from the working directory.

## Working on different branches

Usually, when you are working on a project, you want to keep the main branch clean and stable.
This is the branch that is usually called `master` or `main` and it is the one that is used to build the final version of the project.

Ok, let's make a step back. What is a branch in layman terms?
`git` tracks changes in a tree-like structure, where each commit is a node in the tree and the changes are the edges.
A branch is a sequence of commits that starts from a specific commit and goes on until the last one.
The main branch is the one that starts from the first commit and goes on until the last one, and it is the one that is used to build the final version of the project.
But a repository can have as many branch as you want, and they allow you to experiment freely without worry

When you are working on some new changes, a new feature or a bug fix, you usually want to do it in a separate branch, so that you don't mess up the main branch with your changes.

This is done with the `git switch` command.
```bash
; git switch -c new-branch-name
```
This will create a new branch called `new-branch-name` and switch to it.
The flag `-c` is short for `--create` and it tells `git` to create a new branch if it doesn't exist already.
If the branch was already created, you can simply switch to it with
```bash
; git switch new-branch-name
```
The way you work on a branch is in any way similar to the way you work on the main branch, since that is itself also a branch, and so it is just a sequence of commits.
You can add and commit changes, you can restore files, you can switch to a different branch, and so on.

## Merging branches

When you are done with the changes in the new branch, you can merge them back to the main branch with the `git merge` command.
```bash
; git switch main
; git merge new-branch-name
```
This will merge the changes from the branch `new-branch-name` into the main branch.
If there are no conflicts, the merge will be successful and the changes will be added to the main branch.
If there are conflicts, that is, there are changes in main that have happened in the meantime that overlap with your new changes in a way that cannot automatically be resolved, `git` will ask you to resolve them manually before the merge can be completed.

You can use `git status -st` to see which files have conflicts and need to be resolved.
And the resolution simply consists in you editing the files to remove the conflict markers (you will easily notice them, don't worry!) and keep only the changes that you want to keep.

Once you have resolved the conflicts, you can add the files and commit the changes as usual, and the merge will be completed.

You can have a look at the branches that are available in the repository with the `git branch` command.
```bash
; git branch
```
This will show a list of the branches that are available in the repository and highlight the one that is currently checked out.

If you are done with a branch and want to get rid of it, you can use the `git branch -d` command.
```bash
; git branch -d new-branch-name
```
This will delete the branch `new-branch-name` from the repository.

## Working with remote repositories

When you are working on a project with other people, you usually want to keep your changes in a remote repository, so that others can see them and you can see theirs.

There are many places where you can host your remote repository nowadays, but the most popular optionms are [github](https://github.com) and [gitlab](https://gitlab.com), which are also free for most usecases.

I will not tell you how to create a remote repository, because there are plenty of resources for that.
They also provide nice graphical ways to do it and to deal with requests to merge branches between different copies of the repository, which is especially nice when you work with other people.
You can read more about that, with lots of screenshots to guide you, in the official documentation of the host of your choice.
While it may seem hard to start using git and these services, I assure you that it is just a matter of doing it a few times and getting used to it, and it is well worth the effort.

So let's assume that you have a remote repository and you want to add it to your local one.
The page hosting the repository will usually tell you how to do it, and in particular will show you a `URL` to use if you want to do it by hand.

To add a remote repository to your local one, you can use the `git remote add` command.
```bash
; git remote add origin URL
```
where `URL` is the URL of the remote repository.

The interesting fact is that you can have more than one remote repository, and you can give them different names.
For example, you can have a `origin` repository that is the main one, and a `backup` repository that is a backup of the main one and a `collaborator` repository where a collaborator is working on the project.
To add them, you simply use different names in the `git remote add` command.
```bash
; git remote add backup URL
; git remote add collaborator URL
```

Once you have added a remote repository, you can push your changes to it with the `git push` command.
```bash
; git push origin main
```
This will push the changes in the `main` branch to the remote repository called `origin`.
If the branch doesn't exist in the remote repository, it will be created.
If the branch already exists, the changes will be added to it.
Of course, you can modify the branch name to push a different branch and the remote repository name to push to a different remote repository.

You can also pull changes from a remote repository with the `git pull` command.
```bash
; git pull origin main
```
This will pull the changes from the `main` branch of the remote repository called `origin` and merge them into the current branch.
If the branch doesn't exist in the local repository, it will be created.
If the branch already exists, the changes will be added to it.

When you have many remote repositories, you can use the `git remote -v` command to see a list of them and their URLs.
```bash
; git remote -v
```
This will show a list of the remote repositories that have been added to the local one and their URLs.

On a final note, if you want to download changes from the other remote repositories without touching your current branch, you can use the `git fetch` command.
```bash
; git fetch collaborator
```
This will download the changes from the remote repository called `collaborator` and store them in the local repository, but it will not merge them into the current branch.

## Conclusion

This is a very brief introduction to `git` and its basic commands.
While not perfect or very ergonomic,`git` is extremely powerful.
There are many more commands and features that I haven't covered, but I think these are the most important ones and the ones that you will use most of the time.
I had promised this to a friend months ago, and today for once I hope I have maintained this promise :)

