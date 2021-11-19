---
title: "Ghost up and running on Amazon EC2"
date: 2013-09-23T11:00:00.000Z
lastmod: 2013-10-29T15:57:08.000Z
tags: ["tutorial", "ghost", "Amazon EC2"]
categories: ["Blog"]
slug: "ghost-up-and-running-on-amazon-ec2"
disqus_identifier: 2
---

I had my free Amazon EC2 instance waiting for this moment since [my last use of it](https://github.com/mseri/pplofthesoil). 

I spent my few free hours setting up a decent (I hope) [theme](https://github.com/mseri/purity) for [Ghost](https://ghost.org), and reading around what to do and what not to do to have it up and running. My main reference was the nice blog post [How to set up an Amazon EC2 instance to host ghost for free](https://www.howtoinstallghost.com/how-to-setup-an-amazon-ec2-instance-to-host-ghost-for-free/).

I followed more or less all the steps suggested in the guide but there was still something missing: I wanted my Ghost blog to be running even when I am not logged in the EC2 instance.

At first I thought it could be nice to try [forever](https://github.com/nodejitsu/forever) but I configured my node.js to listen on port 80 and _sudo_ wasn't really working properly with _forever_ (if you know how to solve the problem I'll be happy to read how in the comments). Therefore I decided to opt for a different way: _screen_.

_screen_ is a sort of VNC or Remote Desktop for Unix consoles. More technically it is a terminal multiplexer that let you run multiple console-based applications simultaneously. The best part of it is that you can leave it running remotely and come back to pick up your console sessions whenever you need:
 > If your local computer crashes, or you are connected via a modem and lose the connection, the processes or login sessions you establish through screen don't go away. You can resume your screen sessions with the following command: `screen -r`
 
Awesome! In fact what I did was just run

```sh
    screen sudo /usr/local/bin/npm start --production
```
close the terminal and log into my ghost blog to write this post. 

**As you can see things kept working properly!**

_Note that I am running the production configuration of ghost. You have to remove the `--production` argument to run the development server and use the configuration that you did following the tutorial linked above._

###UPDATE
The theme is no more called `pureBuster`. It has been renamed `purity`.