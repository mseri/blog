---
title: "Update script explained"
date: 2013-10-21T14:02:38.000Z
lastmod: 2013-10-29T16:00:05.000Z
tags: ["ghost", "update", "bash"]
categories: ["Blog"]
slug: "update-script-explained"
disqus_identifier: 10
---

I am going to proceed step by step through the code of the script that I have [posted few days ago](https://www.mseri.me/a-simple-script-to-update-ghost/). 

I purposedly updated the script to be a bit more general and flexible (but not too much). At the end of the file I explain how to run it. You should [make a backup](https://docs.ghost.org/installation/upgrading/) before doing the update (the simplest way is probably running `tar czf backup.tar.gz YOUR_GHOST_FOLDER`). Be careful that there is no warranty with this script and I will not take any responsibility for claims or damages consequent to the use of it.

The following line is called _sha bang_ and simply tells your system that the file contains a set of instructions that has to be executed by the [_bash_](https://en.wikipedia.org/wiki/Bash_(Unix_shell)) interpreter.

    ::sh
    #!/bin/bash

You should have bash installed in `/bin/bash` to be sure that the script will be of any use.

The next bit of code is just checking if you have defined the three most important variables: `GHOSTUPDATEFILE`, `GHOSTUPDATELOCATION`, `GHOSTINSTALLDIR`; and define them if they are not. They respectively represent the name of the last ghost update, at the present day it is just `ghost-0.3.3.zip`, the temporary folder that will be used to unzip the new ghost, by default `update-ghost-tmp` and the folder where ghost is installed (in this last version in absolute path), the default is the subfolder `ghost` of the folder containing the script.

    :::sh
    if [[ -z $GHOSTUPDATEFILE ]];
    then
      export GHOSTUPDATEFILE='ghost-0.3.3.zip'
    fi
     
    if [[ -z $GHOSTUPDATELOCATION ]];
    then
      export GHOSTUPDATELOCATION='update-ghost-tmp'
    fi
     
    if [[ -z $GHOSTINSTALLDIR ]];
    then
      export GHOSTINSTALLDIR=`pwd`'/ghost'
    fi

You can either change them in the file or simply type something like the following before running the script in your terminal: `export NAME_OF_THE_VARIABLE='YOUR_CUSTOM_VALUE'`

I suggest you to check that the variables are correct typing in your terminal `echo $NAME_OF_THE_VARIABLE` and checking that in output you get the correct `YOUR_CUSTOM_VALUE`.

The code proceed saving the current location in a variable, we will need it later, with 
    
    :::sh
    export STARTLOCATION=`pwd`

The following three lines simply take care to download `GHOSTUPDATEFILE` and unzip it in `GHOSTUPDATELOCATION`.

    :::sh
    wget https://ghost.org/zip/$(echo $GHOSTUPDATEFILE)
    unzip $GHOSTUPDATEFILE -d $GHOSTUPDATELOCATION
    echo "Ghost downloaded and unzipped"

For this step to be effective you need to have installed `wget`. If this is not the case you should install it or replace the wget line with

    :::sh
    curl -O https://ghost.org/zip/$(echo $GHOSTUPDATEFILE)

Note that you will anyhow read the message _Ghost downloaded and unzipped_, even if there have been errors during the execution. If I have time, I may change this behavior in a future version but I don't plan to do it for the moment.

    :::sh
    cd $GHOSTUPDATELOCATION
    cp *.md *.js *.txt *.json $GHOSTINSTALLDIR
    cp -R core $GHOSTINSTALLDIR
    cp -R content/themes/casper $GHOSTINSTALLDIR/content/themes
    echo "Ghost has been updated with" $GHOST
    
    cd $GHOSTINSTALLDIR
    npm install --production
    echo "NPM updated"

These few lines of code simply do what is mechanically suggested to do in the [ghost upgrade instruction page](https://docs.ghost.org/installation/upgrading/): go into the new ghost folder and copy all the files in your active ghost environment, then move back to your ghost environment and run npm update.

After this update process is finished, hopefully without errors, we go back to our first location and remove the temporary update file and update folder.

    :::sh
    cd $STARTLOCATION
    rm -rf $GHOSTUPDATELOCATION $GHOSTUPDATEFILE
    echo "Folder cleaned"

The next, last, step is the one that you will probably have to modify to adapt to your needs. Its purpose is restarting the ghost environment. In my case it runs with [forever](https://npmjs.org/package/forever) and is started by a code that I saved in a script called `starter.sh` in my ghost folder. The following code does the restart as I would do it by hand and then tells me "_Done!_".

    :::sh
    echo "Restarting ghost..."
    forever stop 0
    sh $GHOSTINSTALLDIR/starter.sh
    
    echo "Done!"

You have to replace those lines with the appropriate code. It really depends on how you start/stop your server, you can even delete them and do it by hand after the update is complete.

Suppose that your folder structure is something like

    ~\
      folder1\
              ...
      folder2\
              ...
      folder3\
              myghost\
                    ...
              folder5\
              update-ghost.sh
      folder4\
      ...

then to run the script you should log in to your server and do something like

    :::sh
    cd folder1/
    export GHOSTINSTALLDIR=`pwd`'/myghost'
    sh update-ghost.sh


I hope this is clear enough to give to everybody the chance to adapt the script and use a semiautomated way to update their ghost installation while we wait for some other official system.
