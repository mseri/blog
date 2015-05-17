Id: 13,
Title: A great workaround for targeting links in Ghost
Date: 2013-10-29T15:53:23.000Z
Modified: 2013-10-29T16:02:36.000Z
Tags: ghost, hack, target, workaround
Category: Blog
Slug: a-great-workaround-for-targeting-links-in-ghost
Authors: Marcello Seri

When I am reading something, I hate to click on some link (that I will supposedly read later) and be redirected to the new page. I'd rather prefer the links to open in background in a new tab.

You may say that it is enough to click while pressing Command or Control and the page will be opened in a background tab, but it's not the same. What if I accidentally click for example?

For this same reason, I used to add the anchor attribute `target="_blank"` to all my links. This, however, became a bit of a problem when I moved to Ghost...

With its markdown syntax you can just add links writing `[the text you see](http://theli.nk)` but this will just create `<a href="http://theli.nk">the text you see</a>`. 

**Is there any wayt to add the `target="_blank"` attribute?**

Well, we could write the whole anchor by hand, but this is not really what I was looking for. I didn't really spend much time trying to solve the issues, but I had the great luck of reading a post [here](http://huynq.net/)...

HuyNQ has a post showing a workaround that is as simple as it is brilliant!

Apparently the markdown interpreter of Ghost makes no assumption regarding the characters contained in the link you add: this means that `"` is not converted to `&dquot;`, but is transferred to the code as it is _(this is potentially bad, as it could be used for attacks, but imho if some attacker can change the text in the database you should have other more serious worries)_.

This means that adding `` to the URL will generate an anchor with the proper target. In other words
```
[the text you see](http://theli.nk)
```
will generate
```
<a href="http://theli.nk">the text you see</a>
```
that is exactly what I was looking for.