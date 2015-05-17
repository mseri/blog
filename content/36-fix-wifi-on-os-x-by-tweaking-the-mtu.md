Id: 36
Title: Fix WiFi on OS X by tweaking the MTU
Date: 2014-10-15T23:18:23.000Z
Modified: 2014-10-19T14:54:46.000Z
Tags: tips, Tips, wifi, osx, trick, MTU
Category: Blog
Slug: fixing-wifi-on-os-x-by-tweaking-the-mtu
Authors: Marcello Seri

After I had installed the first developer beta of Yosemite I started experiencing serious WiFi issues **at home**, with the connection dropping after few seconds of activity. Only apparent solution was to disable and reenable periodically the wifi until it started working.

The issue was not present whene I was in my office or using public wifi's around. And removing the network setup to have them reset to default didn't help.

Few days ago I was looking for an old script in one of my backups when I've found an old note called `Find MTU to fix Lion WiFi`. I had completely forgotten about it, as I had forgotten about the problems with Lion's wifi...

It turned out that the problem was, in fact, related to the [MTU](https://en.wikipedia.org/wiki/Maximum_transmission_unit)(Basically the size of the transmitted packets). It was set to be automatic, and it automatically selected the value 1500 (that seemed to be quite standard, or at least correcto for almost all the networks I've used). Checking it brutally I found out that my home router has a quite lower MTU, and changing it did solve all my problems.

Finding the correct MTU is quite easy. One needs just to open a terminal and `ping` and external website with appropriately constructed packets. Namely

    ping -D -s 1500 example.com

Here `-D` tells ping that the package cannot be fragmented, in other words if it is too large it will not be sent at all, and `-s 1500` tells it what must be the size of the packet in bytes. Be careful, 1500 is not really the full size of the packet, **there is an overhead of 28 bytes that you need to add to that number**. E.g `-s 1500` means that the packet size is 1528 bytes. If the largest packet that you can successfully send has size  1472, then your MTU value is 1500.

You can add the option `-c n` to tell ping to send only n packages (2 or 3 will be enough), otherwise you can kill the process after a couple of packages is sent.

Running

    ping -D -s 1500 example.com

on my network I get the following output

	PING example.com (93.184.216.119): 1500 data bytes
	ping: sendto: Message too long
	[...]

If you read a similar message (and you should if you use 1500) you need to start reducing the value after the `-s` until you find the first value for which ping starts working, i.e. you start receiving output of the form

	1412 bytes from 93.184.216.119: icmp_seq=0 ttl=53 time=136.639 ms
    [...] 
    
In my case the value was 1404, that corresponds to MTU 1432.

To change the MTU than is enough to open WiFi's advanced preferences and, on the hardware tab, select _MTU: Manual_, insert the value that you have found and apply the changes.