Id: 3
Title: Ghost on Amazon EC2 without using sudo
Date: 2013-09-24T11:00:00.000Z
Modified: 2013-10-29T15:56:32.000Z
Tags: Amazon EC2, nginx, forever, security, iptables
Category: Blog
Slug: ghost-on-amazon-ec2-without-using-sudo
Authors: Marcello Seri

I've been thinking since [yesterday's post](http://www.mseri.me/ghost-up-and-running-on-amazon-ec2/) how to run the ghost blog at the user level, wihout the need of using sudo.

## Use Nginx

In a production environment I would probably run ghos as a nginx subdomain (i.e. _ghost.mseri.me_), eventually forwarding the domain to the same address (e.g. typing _mseri.me_ you would end up automatically in _ghost.mseri.me_). For this purpose you either know by hearth how to do it, or you can follow one of the many tutorial available online. I think this is a very neat and effective way of proceeding.

For the sake of completeness I link some of them here: 

- [Dude looks like a ghost](https://blog.igbuend.com/dude-looks-like-a-ghost/)
- [Setup Ghost with nginx on Debian](http://nls.io/setup-ghost-with-nginx-on-debian/) 
- [Installing Node.js on Amazon EC2](https://github.com/d5/docs/wiki/Installing-Node.js-on-Amazon-EC2) 
- [How to Host Ghost on a Nginx Subdomain](http://www.howtoinstallghost.com/how-to-host-ghost-on-a-nginx-subdomain/) 

Even if some of these links are for other Unix systems or just for node instead of ghost, it is pretty straightforward to adapt them to your needs.

Remember, when you are in a production environment, end even when you are just on a test space, to try and secture your system as possible. A decent starting point could be [Top 20 Nginx WebServer Best Security Practices](http://www.cyberciti.biz/tips/linux-unix-bsd-nginx-webserver-security.html) or [Dude looks like a ghost](https://blog.igbuend.com/dude-looks-like-a-ghost/). Moreover, if you are following this last tutorial you should have a look to [How to Secure an nginx Server with Fail2Ban](http://snippets.aktagon.com/snippets/554-how-to-secure-an-nginx-server-with-fail2ban).

## Use iptables to forward port 80

Another option, given that in Amazon EC2 users are allowed to use only port greater 1024, is to forward your 80 port to your 8080 (or whatever you need) using iptables.

If you set up ghost to listen on the port 8080, it's likely that you have nothing to do and port 80 and 8080 are already assigned to http. You can easily check it from the AWS Console (look for security groups) or simply **giving it a try**. Just modify your `config.js` and replace whatever is in `host: 2368` with `host: 8080`. Run ghost with `npm start` and try to access your blog, if it works there is nothing else to do than install `forever` and use it.

![The AWS console](/images/03-screenshot.png)

If it doesn't work try to execute the following command (only for linux) in a terminal and it should start working
```
sudo iptables -t nat -A PREROUTING -p tcp --dport 80 -j REDIRECT --to-port 8080
```
If you are still using port 2360 replace 8080 with the appropriate value. You may need to enable the access to the proper ports, to do it is enough to execute the following. 
```
sudo iptables -A INPUT -p tcp --dport 80 -j ACCEPT
sudo iptables -A INPUT -p tcp --dport 8080 -j ACCEPT
```
I reccomend to **not play with iptables rules in a production environment if you don't know what you are doing**.

To check if the rules have been accepted you can list the configuration with 
```
sudo iptables -L
```
and to delete the previous rules in case they didn't work just type them again in the terminal with `-A` replaced by `-D`.

This same procedure can be adapted to other unix systems just using the appropriate firewall rules (like packet filter on BSD).

## Install and use forever

Now that we can start ghost without any need of using sudo, we only have to install forever. Open a terminal and execute
```
sudo /usr/local/bin/npm install -g forever
```
then enter in the ghost folder with `cd path_to_your/ghost_folder` and run
```
NODE_ENV=production forever start index.js
```

Open your browser and enjoy your Ghost Blog!

_If you are using the development configuration instead of the production one, just drop `NODE_ENV=production` from the previous command._

To kill the server, just use
```
forever list
forever stop 0
```
where 0 is the ghost process. Or eventually
```
forever stopall
```

### Check permissions

If you were running your ghost blog using sudo, you may not be able to access the database or some folders. In such case is enough to fix its permissions. Open a terminal, enter in the ghost folder with `cd path_to_your/ghost_folder` and execute
```
sudo chown yourusername -R *
sudo chgrp yourusergroup -R *
```
where you have to replace `yourusername` and `yourusergroup` with the appropriate values. For Amazon EC2 the are in general both equal to `ec2-user`. 