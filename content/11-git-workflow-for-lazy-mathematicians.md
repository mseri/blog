Id: 11
Title: Git workflow for lazy mathematicians
Date: 2013-10-21T16:40:27.000Z
Modified: 2013-10-29T15:58:55.000Z
Tags: tutorial, git
Category: Blog
Slug: git-workflow-for-lazy-mathematicians
Authors: Marcello Seri

First of all, what is [git](http://git-scm.com)? Citing its website
> Git is a free and open source distributed version control system designed to handle everything from small to very large projects with speed and efficiency.
> [It] is easy to learn and has a tiny footprint with lightning fast performance.

In other words Git provides a source control repository that enables you to roll back code changes as needed, to merge the updates when collaborating with others and eventually to have an online backup of your work. 

For remote backup and collaboration you can get a free account on [github](http://www.github.com) or [bitbucket](http://www.bitbucket.org). Note that with this last one, if you have an academical email address, you can get unlimited private git repository with unlimited amount of collaborators. On the other hand, github seems the most common choice for open source projects.

If you are coding numerical algorithms, mathematica notebooks, latex drafts, papers, or whateverelse, you may decide not to use Git, but sooner or later you will be there thinking "if only I had saved that version and could take back just those few lines"... and it's there that Git power enter into play.

I have to admit that I disagree with the description given above: Git is not easy to understand or learn! But if you take the time to understand at least the basics, it will present as a worthwhile and essential tool.

And if you briefly look online, you may discover that I am not the only one to think it (see e.g. [Git+LaTeX Workflow](http://stackoverflow.com/questions/6188780/git-latex-workflow), [Git Basics for LaTeX Users](http://bensresearch.com/downloads/Git.pdf) or [Collaborating with LaTeX and Git](https://www.sharelatex.com/blog/2012/10/16/collaborating-with-latex-and-git.html)).

## Git in four paragraphs and a list

We use Git to record the changes (called **commits**) that we make to our projects over time.

Each commit contains the change that a user has made to its code and some additional useful metadata: these include the time the change was made, the name of the user, and a message that is added to describe the change. 

These commits are stored in a specialized database provided by Git itself. 

Moreover Git provides a set of commands that allow more collaborators (or the single user): 

- to make changes to the files and stay in sync;
- to maintain and access different versions of the project;
- to compare the different versions;
- to retrieve past versions of the project;
- to retrieve parts of the past versions of the project.

## First of all install Git
But the zeroeth step is always to check if git is already installed on your computer (Mac OSX and many Linux distros have it pre-installed). Open a terminal and type
```
 git version
```
If your output looks like
```
git version 1.8.3.4
```
you already have git installed, if it shows an error you probably don't.

How to install it is really a matter of what OS you are using. You could just go to the home page of [Git](http://git-scm.com) and download an installer, use your favourite package manager or compile the sources.

Alternatively you could use the github software for [mac](http://mac.github.com) and [windows](http://windows.github.com). For windows I strongly suggest to use [msysGit](http://msysgit.github.io).

On any Debian based linux (including Ubuntu) you can use the command line 
```
 sudo apt-get install git-core
```

Similarly, on red hat based (like Fedora), you can use
```
 yum install git-core
```

Whatever you choose your option to be, I strongly suggest you make a free account either on BitBucket or GitHub (or both).

_When you register, you shuld use your real name. For a developer and for people involved with open source the BitBucket/GitHub account could be as important as a résumé or a business card. I really suggest you to use the name by which you are known professionally, even if you plan to use just private repositories._

If you like nice graphical interfaces you could use the nice (and free) [Source Tree](http://www.sourcetreeapp.com). Personally Source Tree is the best, anyway on the official [Git website](http://git-scm.com) you can find a good list of alternative graphical interfaces for Git.

### Introduce yourself to git
Now that Git is installed you shall check if it is properly configured, i.e. does it know who you are?
Open a terminal (keep it open... we will use it a lot) and type
```
 git config -l --global
```
You should see `user.name=Your Name` and `user.email=your_email_address`. The email address will identify you to any services that use your Git repo, therefore it is important that these values are correct and are the one used to register your BitBucket/GitHub/OtherServiceUsingGit account.

If the previous output was wrong, you can fix it easily with
```
 git config --global user.name 'Your Name'
 git config --global user.email youremail@somedomain.com
```

## Git Init

If you want to start using Git with your project you have to initialise it. **Be sure to be in your project's root directory.**

Initialise Git and make your first commit:
```
 git init
 git add .
 git commit -m 'first commit'
```
The `-m 'first commit'` simply attach a global message (with content 'first commit') to the commit. 

> You should include a short descriptive comment with every commit.

At any time with you can check your repository status with
```
 git status
```

### Add a remote repository
If you want an offsite copy of your work or you plan to share your work with others you should get a Bitbucket/Github account.

First create a new empty remote repository into which you can push your local one:

- [instruction for Bitbucket](https://confluence.atlassian.com/display/BITBUCKET/Create+a+repository)
- [instruction for GitHub](https://help.github.com/articles/create-a-repo).

Add the remote repository for your project and push your local project to the remote repository:

- for Bitbucket
```
 git remote add origin https://user@bitbucket.org/path_to/repo.git
 git push origin master
```
- for GitHub
```
 git remote add origin https://user@github.com/path_to/repo.git
 git push origin master
```

### Save changes
At each stage of completion you should [commit your code](http://gitref.org/basic/#commit) into your local repository with:
```
 git commit -am "some readable comment"
```
Here we use the `-am` argument: `-m` adds a commit message, while `-a` automatically makes a snapshot of all the changes done to _tracked files_, adds new files and removes any files you may have marked for deletion (otherwise you have to use `git rm`, adding an additional step).

Finally you can push your changes to the remote repository:
```
 git push origin master
```

#### Commit messages? C'mon...
If you are not working alone your colleagues will surely appreciate if you follow some convention for your commit messages, and so would you when they are going to commit or when you are looking back to some change.

I would suggest you to use imperative tense ("update" not "updated") and keep the first line very short. I think [A note about git commit messages](http://tbaggery.com/2008/04/19/a-note-about-git-commit-messages.html) is a good reding in regard.

### View the history of changes
To view your history is enough to type
```
 git log
```
The output will be something like
```
commit 7dbba9ab8bb2031ed52abf6a2dc11cc335ece5a1
Author: Marcello Seri 
Date:   Fri Oct 4 13:11:51 2013 +0100

    add simulation for clusters

commit 23e1443a59410eb91ef0af26c9f82fb0624dd42d
Author: Marcello Seri 
Date:   Wed Sep 18 12:18:05 2013 +0100

    minor fix in step 2 section

[...]

commit 9cf461946076c7849726ff4a8a48e43d7e191f07
Author: Marcello Seri
Date:   Tue Jul 16 19:00:42 2013 +0100

    add and update estimates file
    
commit dafeaef258c850ce8ecb7d8f15c34e0dfc4930fa
Author: Marcello Seri
Date:   Fri May 17 14:40:04 2013 +0100

    first commit
```

You can user the weird code appearing next to the commit line to see what has changed in that particular commit:
```
git show 9cf461946076c7849726ff4a8a48e43d7e191f07 --word-diff=color
```
The first part of the output replicates the log. In the second part the changes are shown in detail. You can see the text that was added in highlighted green and the text that was removed in red. The affected files appear in higlighted white before the red/green text.

Note that by default Git compares documents line by line, so that if anything has changed on a line then it shows the whole line as changed. With TeX documents lines can be quite long and it can be difficult to quickly see what has changed between similar lines: the option `--word-diff=color` tells Git to compare the changes word by word making the output more readable.

These features are very useful if you want to see the changes made by one of your collaborators, or to remind yourself what you were working on last time.

### Ignore Files
When you compile LaTeX documents, and in general when you compile any code, you will produce many different useless files that you don't want to be saved at each commit. To take care of them you have to create a `.gitignore` file in your project root directory.

If you like terminal you could do as follows.
```
 touch .gitignore
 echo '.DS_Store' >> .gitignore
```
Or open `.gitignore` with your favourite editor and add all the files and folder Git has to ignore. For LaTeX you `.gitignore` could look like
```
# For Mac users
.DS_Store

# For TexPad users
.texpadtmp/

# For everybody
*.aux
*.bbl
*.blg
*.dvi
*.idx
*.ind
*.log
*.out
*.synctex.gz
*.toc
```

### Undoing changes
This section is borrowed from [Collaborating with LaTeX and Git](https://www.sharelatex.com/blog/2012/10/16/collaborating-with-latex-and-git.html#.UmU-DZGOays).

Of course, you don't want to just be able to see changes, you want to be able to go back and use the history to undo changes. Perhaps you want to restore the document to a previous version because you don't like the changes you've made or you realise you made a mistake. Git doesn't just rewind the the history of your document because then you would lose the changes made between then and now. Instead, git lets you restore the files you are working with to an earlier version by creating a new version which comes after all of the intervening history. If you decide you didn't actually want to do this after all then nothing has been lost.

To restore your files to an earlier version, simply run:
```
 git checkout f69606d7e24ad45b31bb6eb4b38192bd07f274fc *
```

This tells git to `checkout` the files from the older version specified by the third argument (remember we refer to versions by their long identifier of numbers and letters). The files in your project now have their contents restored to the older version, but you still need to create a new version to mark this change in Git:
```
 git commit -a -m "Restore files to previous version"
```
You could of course edit your files at this previous version before creating a new version in git.

Another common situation is you decide that you want to undo only one set of changes from a while ago. Perhaps you've edited the document in three steps: 
1) Adding an abstract, 
2) Updating your acknowledgements, 
3) Adding in a figure. 
At each step you've created a new version in git, but now you decide that you didn't really want to update you acknowledgements. Unfortunately this is sandwiched between other changes so a simple rollback like before won't do. Fear not, because git is clever enough to do what you want, with the revert command:
```
git revert f69606d7e24ad45b31bb6eb4b38192bd07f274fc
```

The final parameter should be the identifier of the version that introduced the changes you want to undo.

Note: _Git revert undoes the changes introduced by the version that you pass to it. It does not revert the project to that version. This is a commonly confused command so be careful! To put the whole project back to a previous version, use the first method described at the top of this section._

### Pushes and Pulls
Suppose that some collaborator made an important change and pushed it on the remote repository. Now that you need it, how can you retrieve it?

Supposing that there is no conflict, you just have to commit your code and instead of pushin it, pull it from the remote:
```
 git pull origin master
```

### A finer workflow
This is the workflow I use when I work in teams. I learned it from [Rails with Git and GitHub](http://railsapps.github.io/rails-git.html). I like how it is explained in that page, this section is borrowed from their article.

When you are using Git for version control, you can commit every time you save a file, even for the tiniest typo fixes. If only you will ever see your Git commits, no one will care. But if you are working on a team, either commercially or as part of an open source project, you will drive your fellow programmers crazy if they try to follow your work and see such "granular” commits. Instead, get in the habit of creating a Git branch each time you begin work to implement a feature. When your new feature is complete, merge the branch and "squash” the commits so your comrades see just one commit for the entire feature.

Here's how you could create a new Git branch for a section named "Second Proof":
```
 git checkout -b second_proof
```

The command creates a new branch named "second_proof" and switches to it, analogous to copying all your files to a new directory and moving to work in the new directory (though that is not really what happens with Git).

When the new feature is complete, merge the working branch to "master" and squash the commits so you have just one commit for the entire feature:
```
 git checkout master
 git merge --squash second_proof
 git commit -am "secion named 'Second Proof' complete"
```
If everithing goes smoothly you can push your changes
```
 git push origin master
```

Finally you can delete the working branch when you're done:
```
 git branch -D second_proof
```

## A final remark
If you are new to git and want to become a master of the art, instead of my very simple workflow you can read for free the online version of [Pro Git by Scott Chacon](http://git-scm.com/book). 

You find a very nice free complete interactive crash course on git at [Git Immersion](http://gitimmersion.com). I realised it only after having written my post, it is very very good.
