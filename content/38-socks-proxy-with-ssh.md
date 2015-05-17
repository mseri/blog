Id: 38,
Title: Socks proxy with ssh
Date: 2014-10-31T18:24:36.000Z
Modified: 2014-10-31T18:26:17.000Z
Tags: Tips, vpn, socks proxy, ssh
Category: Blog
Slug: socks-proxy-with-ssh
Authors: Marcello Seri

When you work in the University, it is very likely that during a trip or the weekend you urge to connect via the University to have access to Journals and other academic resources. 

Often enough this requires long and complicated procedures involving the setup of rarely updated proprietary VPN softwares that sometimes like to install their obscure helpers to monitor the traffic and prevent you to open malicious websites. Helpers that would keep working in background sending to unspecified servers all your business even when the VPN is off...

Luckily is even more common to have some level of ssh access provided directly by each institution. Indeed, there is a not too well known `ssh` option that let you use your encrypted connection to start a local socks proxy that could be used in the place of the VPN. 

I copy and paste from the [man page](http://linuxcommand.org/man_pages/ssh1.html)
> **-D port**: Specifies a local “dynamic” application-level port forwarding. This works by allocating a socket to listen to port on the local side, and whenever a connection is made to this port, the connec  tion is forwarded over the secure channel, and the application protocol is then used to determine where to connect to from the remote machine.  Currently the SOCKS4 and SOCKS5 protocols are supported, and ssh will act as a SOCKS server.  [...]

Run in your terminal

```
ssh -D 9090  your_username@your_academic_ssh_server
```

and setup your browser to use a socks proxy with address `localhost` (or `127.0.0.1`) and port `9090`.

There is even a more complete solution for linux and mac (note, it does not work on OS X 10.10 Yosemite, and has some problems with OS X 10.9 Mavericks) called [`sshuttle`](https://github.com/apenwarr/sshuttle).