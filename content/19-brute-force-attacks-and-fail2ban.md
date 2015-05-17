Id: 19,
Title: Brute force attacks and fail2ban
Date: 2013-12-12T15:00:07.000Z
Modified: 2013-12-12T15:01:37.000Z
Tags:
Category: Blog
Slug: brute-force-attacks-and-fail2ban
Authors: Marcello Seri

Even a nearly unkown server like mine receives every day a number of brute force attacks. Usually I have an instance of `fail2ban` monitoring the logs of all my services and readily banning the attackers after few attempts.

Not tonight... 

Let's move a step backwards. What is `fail2ban` and how does it work?

Reaching out the [home page](http://www.fail2ban.org) of the software you can read

> Fail2ban scans log files and bans IPs that show the malicious signs - too many password failures, seeking for exploits, etc. Generally Fail2Ban then used to update firewall rules to reject the IP addresses for a specified amount of time, although any arbitrary other action *(e.g. sending an email, or ejecting CD-ROM tray)* could also be configured. Out of the box Fail2Ban comes with filters for various services *(apache, curier, ssh, etc)*.

Now that you know what we are talking about, I can tell you how fail2ban does it job. It starts a process in background (a [daemon](http://en.wikipedia.org/wiki/Daemon&#95;(computing)" target="&#95;blank)) that monitors the logs of your systems, each time something is logged it filters it using [regular expressions](http://en.wikipedia.org/wiki/Regular_expression), this filtering process identifies potential malicious hosts and, depending on your configuration, bans them for a limited/unlimited amount of time creating ad hoc firewall rules.

On my ubuntu server 13.04 I had to touch very few settings and add very few rules, almost all the ones that come with the default installation are working and are setted up properly. You cannot believe how many attacks I receive daily (mainly to ssh or the webserver). I wonder how much bandwith big services can waste due to these assholes...

Anyhow, the problem arised with the mail service. My mail server use [dovecot](http://www.dovecot.org) to provide imap services, and [sasl](http://en.wikipedia.org/wiki/Simple_Authentication_and_Security_Layer) for authentication. Both of them requiring [TLS](http://it.wikipedia.org/wiki/Transport_Layer_Security). _I will not go into the details of the configuration, if you want to do something close you could use [NSA-proof your e-mail in 2 hours](http://sealedabstract.com/code/nsa-proof-your-e-mail-in-2-hours/) as a starting point._

Apparently the filter that I was using for sasl had some problems: tonight I've got a brute force attack (luckily with no consequences) and this morning my logwatch report was flooded by failed authentication attempts, all from the same ip. Fail2ban was definitely not doing its job properly.

A check on it is pretty easy to do. It is enough to run

```
fail2ban-regex /var/log/mail.log /etc/fail2ban/filter.d/sasl.conf
```

to see if the filters contained in `/etc/fail2ban/filter.d/sasl.conf` are identifying anything in the logs. Despite `mail.log` was filled by lines of the form

```
Dec 11 03:23:44 ____ postfix/smtpd[12734]: warning: unknown[___.___.___.___]: SASL LOGIN authentication failed: Connection lost to authentication server
Dec 11 03:23:44 ____ postfix/smtpd[12735]: warning: hostname kursejifjalet.com does not resolve to address ___.___.___.___: Name or service not known
```

I got a negative answer. Apparently, when I first setted up my configuration I probably slightly changed the filter (or I had an older version???) with a broken regexp. Anyhow the attack exposed the problem, and the fix is pretty simple. It was enough to modify the filter line in `/etc/fail2ban/filter.d/sasl.conf` with 

```
failregex = (?i): warning: [-._\w]+\[<HOST>\]: SASL LOGIN authentication failed(: [A-Za-z0-9+/ ]*)?$
```

and reload `fail2ban` to fix the issue.

* * * * * * 

**UPDATE**: apparently [I am not the only one having had this problem](http://www.howtoforge.com/forums/showthread.php?t=51349) but it seems to be fixed on both debian and ubuntu server, so I really think that I had done something to the default regexp.

Anyway if you happen to have the same problem, I suggest you to use the filter rule suggested on the link above (it is more generic and not adapted to a particular setting):

```
failregex = (?i): warning: [-._\w]+\[<HOST>\]: SASL (?:LOGIN|PLAIN|(?:CRAM|DIGEST)-MD5) authentication failed(: [A-Za-z0-9+/ ]*)?$
```
