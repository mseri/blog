Id: 8,
Title: nginx, ghost 0.3.3 and modsecurity
Date: 2013-10-18T11:00:00.000Z
Modified: 2013-10-29T15:59:25.000Z
Tags:
Category: Blog
Slug: nginx-ghost-0-3-3-and-modsecurity
Authors: Marcello Seri

In my previous post, [Ghost on Amazon EC2 without using sudo](http://www.mseri.me/ghost-on-amazon-ec2-without-using-sudo/), I was proposing some way of running ghost without having to use sudo and with at least a minimal eye on security.

If you have followed one of the guides that I suggested, namely [Dude Looks Like a Ghost](https://blog.igbuend.com/dude-looks-like-a-ghost/), or you have installed your own [modsecurity](http://www.modsecurity.org) configuration you should have received a big page announcing an **Error 403** right after the update of your ghost to version _0.3.3_.

**Don't worry!**

Due to some security fixes in the last ghost version, modsecurity interpret the content of your ghost's [cookie](http://en.wikipedia.org/wiki/HTTP_cookie) as an [sql injection](http://en.wikipedia.org/wiki/SQL_injection) potential attack and simply drops the communication between the browser and the website to prevent it.

If I understood what expressjs/connect are doing under the hood, there should be no problem in dropping the rule that creates this false positive from the modsecrutiry configuration. The faster way (assuming that you don't need this rule somewhere else) is to comment it in the configuration file

```
sed -i '/981246/s/^/# /' modsecurity_crs_41_sql_injection_attacks.conf
```
and then reload [nginx](http://nginx.org)
```
/opt/nginx/sbin/nginx -s reload
```

Otherwise you should [selectively remove](https://github.com/SpiderLabs/ModSecurity/wiki/Reference-Manual#secruleremovebyid) the rule for the subdomain that is pointing to your ghost instance. But I suppose that if you need this last configuration you already know how to do it...