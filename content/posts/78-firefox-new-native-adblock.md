---
title: "Firefox’s new hidden ad-blocker"
date: 2026-05-01T18:18:05+02:00
tags: [firefox,tutorial,privacy]
categories: ["Blog"]
---

Firefox 149 has quietly started shipping the [Rust-based ad-blocking engine from Brave](https://github.com/brave/adblock-rust) within the browser. For the moment is part of an internal experiment and is not exposed as a browser feature. So, before you do anythink, keep in mind that you are already better off if you are using [uBlock Origin](https://github.com/gorhill/uBlock) for instance and keeping Firefox's `Enhanced Tracking Protection` on. 

If you are still curious and want to try it out, it can be done messing around with `about:config`. 

You need to enable the engine and then point it at a few filter lists. Firefox’s current settings expose two modes, protection and annotation: the first actually blocks the ads, the second is more for telemetry purposes and can be ignored and kept disabled.

First make sure you have an updated version of Firefox.
Then open the `about:config` page, click on `Accept the Risk and Continue` and search for `privacy.trackingprotection.content.protection.enabled`.

If the value is `false`, a double click changes it to `true`. That is the switch that turns the engine on.

Then search for `privacy.trackingprotection.content.protection.test_list_urls`
This is where your ad-block lists should go.

Note that this preference accepts a pipe-separated list of URLs, not a comma-separated one. This is a pipe if you are not familiar with it: `|`.

A reasonable starting set is:

```text
https://easylist.to/easylist/easylist.txt|https://easylist.to/easylist/easyprivacy.txt|https://easylist.to/easylist/fanboy-annoyance.txt
```

That gives you one general ad list, one privacy list, and one cookies-banner removal list. More specifically:

- [EasyList](https://easylist.to/) is an old reliable list, targeting general advertising rules and as a rule of thumb is what one would like to always have there. The EasyList project itself describes it as the main subscription for removing adverts from international webpages.

- EasyPrivacy, also from EasyList, is a natural companion. It is focused on tracking rather than visible ads, so it tends to catch analytics, beacon requests, and other things that quietly follow you around the web.

- Fanboy’s Annoyance List  aims at cookie notices, social widgets, in-page popups, and similar clutter. Up to you if you want it or not. Here is the configuration with EasyList and EasyPrivacy only, in case you prefer it:

	```text
	https://easylist.to/easylist/easylist.txt|https://easylist.to/easylist/easyprivacy.txt
	```

You can find many more lists and their description in the [EasyList GitHub Repository](https://github.com/easylist/easylist)
