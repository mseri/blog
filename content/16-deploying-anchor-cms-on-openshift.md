Id: 16
Title: Deploying Anchor CMS on OpenShift
Date: 2013-11-08T18:24:02.000Z
Modified: 2013-11-22T12:01:13.000Z
Tags: OpenShift, Anchor CMS, deploy
Category: Blog
Slug: deploying-anchor-cms-on-openshift
Authors: Marcello Seri

Some of you may already know that installing [ghost](http://www.ghost.org) on [OpenShift](http://www.openshift.org) is extremely easy (and free). You can [check this post](http://ghost-laures.rhcloud.com) if you don't believe me.

I was wandering how is it with other small and less known CMS. Given that I was already making some local tests with [Anchor CMS](http://anchorcms.com" _target="blank) for a friend, and given that there is almost nothing around about its deployment on Open Shift I decided to give it a try and write about it.

I could find only three references online. Two were forum posts arguing that it is impossible to install it and one is the blog post titled [Ancor CMS on OpenShift](http://sruiz.co.uk/sruiz/blog/2013/09/07/anchor-cms-on-openshift/" _target="blank), that explain how to install Anchor in a working but long and painful way.

In this post I explain you how to do it in 10 minutes (but you need a unix machine: \*BSD, Linux or Mac are fine). You will need the following:

- A terminal that can execute wget, tar, [git](http://www.mseri.me/git-workflow-for-lazy-mathematicians/) and ssh.
- A decent web browser.

## Step 0: the necessary tools

Head to https://openshift.redhat.com/app/account/new and fill in the form. The captcha can be pretty nasty, just be strong and read it carefully. We will just need the free account: no need for credit cards. 

Wait for the confirmation email, click on the link, and accept the term of license. We are ready to start!

To use your account I strongly encourage you to install and set up  the OpenShift client tools (better known as rhc) on your computer. You may think to go for the "Wimp Way" and use the web-UI, but real men use the CLI for higher productivity and besides you would not be able to reach the end of this tutorial.

To install the [rhc Client Tools](https://www.openshift.com/developers/rhc-client-tools-install) go [straight to this website](https://www.openshift.com/developers/rhc-client-tools-install) and follow the instructions.

On a Mac OSX + brew configuration you may get an error related to SSL certificates when you run `gem install rhc` step. I have solved the problem with the following procedure
    
    :::sh
    $ brew update
    $ brew install openssl
    $ brew link openssl --force
    $ brew install curl-ca-bundle

If you use `rvm` you may even try with `rvm osx-ssl-certs update all`.

Now that `rhc` is installed, you have to link it with your OpenShift account. 
    
    :::sh
    $ mkdir anchor_tutorial
    $ cd anchor_tutorial
    $ rhc setup

Now follow the instructions on screen and wait for it to finish. If you are not sure what to answer, have a look to my terminal output [on a private gist](https://gist.github.com/mseri/29d4989d86dfd1ccdbc8).

When you read

	Please enter a namespace (letters and numbers only) |<none>|: 
    
it is very important that you use a simple and recallable string. For this tutorial I used `mseritutorial`.

## Step 1: create the application

To install Anchor we need a recent version of php. Sadly the one contained in openshift's cartridge `php` is not recent enough, but the problem can be solved easily using instead the `zend server` cartridge. To create an app just type

    :::sh
	$ rhc create-app anchor zend-5.6

And wait some time. When you are prompted for cloning and accepting the security certificate just type `yes` and hit return.
Remember to annotate somewhere the informations printed at the end of the procedure:

    URL:        http://anchor-mseritutorial.rhcloud.com/
    SSH to:     uuid@anchor-mseritutorial.rhcloud.com
    Git remote: ssh://uuid@anchor-mseritutorial.rhcloud.com/~/git/anchor.git/

_Notice that the `URL` is simply `http://APP\_NAME-DOMAIN\_NAME.rhcloud.com/`. Notice moreover that we have a new subfolder called **anchor**: it is a clone of our online repository, the website content will go in `anchor/php`._ 

Before doing anything, follow the instruction that says 

    You should set password for the Zend Server Console at:    
    https://anchor-mseritutorial.rhcloud.com/ZendServer

You have to accept a licence, save a password and just click `Next` at the License Information page.

Having secured our zend app, is time to add mysql to the application. Do it with

    :::sh
    $ rhc add-cartridge mysql-5.1 --app anchor

Again annotate the following informations:
    
    Connection URL: mysql://$OPENSHIFT_MYSQL_DB_HOST:$OPENSHIFT_MYSQL_DB_PORT/
    Database Name:  anchor
    Password:       YOUR_PASSWORD
    Username:       YOUR_USERNAME

_A good idea to increase security now would be to install phpmyadmin or login to the remote mysql to create a new database and a new user with restricted permissions to use for the website. It is a good idea and should be done, I am skipping this step for the tutorial and go on using the username and password obtained at this step._

For the setup of Anchor we need to annotate something more. Use the address for `SSH To:` that you obtained previously and save the output of the following command

    :::sh
    $ ssh uuid@anchor-mseritutorial.rhcloud.com 'env | grep MYSQL'

## Step 3: Install Anchor

We can do it from the terminal in the following way

    :::sh
    $ cd anchor/php
    $ git rm health_check.php
    $ wget http://anchorcms.com/download -O anchorcms.tar.gz
    $ tar zxvf anchorcms.tar.gz --strip-components 1
    $ rm -f anchorcms.tar.gz
    $ git add .
    $ git commit -m "Our First Install"
    $ git push

The first four lines are to replace the content of the `php` folder with the code of Anchor, the last three lines are to add the new files to the repository and push (and deploy) the changes online.

The last command will take some time before finishing. When it is done, it is time to configure our Anchor installation: navigate to your website (in our case was http://anchor-mseritutorial.rhcloud.com), click on "_Run the installer_" and use the information that you annotated in the second step to complete the set-up.

You will end up on a green screen telling you to create a `.htaccess` file in the root folder and paste there some code. Don't click on any of the buttons yet. Just copy the code, and from your terminal: type `nano .htaccess`, paste the code, press `Ctrl x`, type `y` and finally press return. 

_Do not yet push this change on the remote repository, otherwise you will loose the installation that you just made_.

Each time you push some code online, the remote repository is overwritten with the content of your push. First we need to save in our repository the changes made by the installer. We can do it in the following way:

    :::sh
    $ ssh uuid@anchor-mseritutorial.rhcloud.com 'tar c app-root/runtime/repo/php/install' > install.tar
    $ ssh uuid@anchor-mseritutorial.rhcloud.com 'tar c app-root/runtime/repo/php/anchor/config' > config.tar
    $ rm -rf anchor/config install
    $ tar xvf install.tar --strip-components 4
    $ tar xvf config.tar --strip-components 4
    $ rm *.tar

Then we need to move the content folder in a space that the remote keeps safe and separated from the repository deployment. This can be done creating the file `.openshift/action_hooks/build` (as before you just need `$ nano ../.openshift/action_hooks/build`) with the following content

    :::bash
    #!/bin/bash 
    
    if [ ! -d $OPENSHIFT_DATA_DIR/content ]; then
       echo "Creating and populating the safe content folder"
       mkdir $OPENSHIFT_DATA_DIR/content
       cp -a $OPENSHIFT_REPO_DIR/php/content/*  $OPENSHIFT_DATA_DIR/content
    fi
    
    # it would be much cleaner to remove
    # the content folder before pushing it
    if [ -d $OPENSHIFT_REPO_DIR/php/content ]; then
       echo "Cleaning the repository content folder"
       rm -rf $OPENSHIFT_REPO_DIR/php/content
    fi

    echo "Symlinking the safe content folder"
    ln -sf $OPENSHIFT_DATA_DIR/content $OPENSHIFT_REPO_DIR/php/content 

We are almost ready. Before pushing the changes we need to modify the file `.gitignore` contained in the `php` folder. Open it with `$ nano .gitignore` and delete the lines

    :::sh
    # generated config
    /anchor/config/app.php
    /anchor/config/db.php
    /anchor/config/session.php
    
    # user mod_rewrite
    /.htaccess
    
    # debug and custom themes
    /themes/*
    !/themes/default

Save the changes and finally deploy a working Anchor copy with
    
    :::sh
    $ cd ..
    $ git add .
    $ git commit -m "Configured Anchor"
    $ git push

## Step 5: Install a nice theme

You may try many themes before being happy with what you have, but each time you push changes the server is restarted. To speed things up and avoid the restart is enough to add a special empty file:

    :::sh
    $ touch .openshift/markers/hot_deploy

Of course you have to deploy it:

    :::sh
    $ git add .
    $ git commit -m "Added Hot Deploy"
    $ git push

You can find many themes online, a good source is [Anchor Themes](http://anchorthemes.com), or you can build your own one using the official documentation or [some tutorial]( http://webdesign.tutsplus.com/tutorials/creating-a-theme-for-anchor-cms).

To install a new theme is enough to download it and add its folder inside the folder `anchor/php/themes` (you can already see the `default` theme folder, don't replace it _default_ is just the theme's name). Finally push it as usual: 

    :::sh
    $ git add .
    $ git commit -m "Added Theme"
    $ git push
    
Refresh or open the website metadata panel in the admin section of Anchor and you will find it appearing next to the other installed themes.

As a final note I particularly like [Balzac](https://github.com/ColeTownsend/Balzac).

## Step 6: backup and restore

To create a backup simply run

    :::sh
    $ rhc snapshot save -a anchor

It will save a `anchor.tar.gz` file containing the full content of the online `anchor` folder.

To restore from a backup run: 

    :::sh
    $ rhc snapshot restore -a anchor -f {/path/to/anchor.tar.gz}
    
Remark: here the name that we are using is always `anchor` just because it is the name that we gave to the application at the beginning of Step 1.

- - - - - 

Now log in, post something and enjoy your newly installed CMS!

The tutorial installation is going to be online and visible for the next few days at the url [http://anchor-mseritutorial.rhcloud.com/](http://anchor-mseritutorial.rhcloud.com/). I use that account for tests, I don't plan to keep this installation of anchor alive forever (and moreover I don't use it, it's just empty), so don't be upset if the link is not going anymore in the future.