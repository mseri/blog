---
title: "Bringing the data back: from the US to us"
date: 2026-01-13T10:12:23+01:00
tags: [privacy, tooling, cloud, europe]
categories: ["Blog"]
toc: true
---

For a while, but especially over the past few months, I have been trying to be increasingly more conscious of the digital tools I use. It is so convenient to rely on the usual US‑based suspects for email, storage, and collaboration, that we may forget that we are their product and that they may take all of our staff away from us in a whim, with no chances to appeal or get it back before we are locked out.

I used to trust Apple at least for privacy, but their push to harness us in their cloud services and the complexity to escape, coupled with my falling trust towards anything in the US, is making me look also for alternatives to their cloud offering.

This post is a small snapshot of where I am in the process, mostly prompted by a [recent post](https://www.zeitgeistofbytes.com/p/bye-bye-big-tech-how-i-migrated-to) I saw online, and backed by many options that I have been exploring also for the collaboration within [EWM-NL](https://www.ewmnetherlands.nl). Below you can find the work‑in‑progress list of EU‑based tools that I have explored and I am considering as alternatives. I have yet to find a balance between convenience, privacy, and sovereignty that works for me, so I included some personal impressions to this list but I cannot yet say what I will do.

I also have to admit that I am in a comfortable situation. Working in academia, data sovereignty is increasingly a requirement rather than a choice. So it is not surprising that for data sharing and collaborations we already have in-house or in-country tools.

For instance, nationwide, the most obvious starting point is [SURF](https://surf.nl/), a cooperative ICT provider for Dutch education and research. For participating universities, like ours, they offer storage, computing, identity management and collaboration tools tailored to our needs. My experience has been very positive, their services are well managed, clean and stable. The problem starts if you want to properly collaborate with people outside the cooperative, which is what we started needing for EWM-NL, or if you want to use similar services for your own personal use. Which is where this list comes in.

I have not explored e-mail hosting providers in depth yet. I have been happily using [Fastmail](https://fastmail.com) for years. This is based in Australia, so privacy-wise is probably not the best, but it is a stable company and I always had good experiences with their service and their customer support.
I have been recommended [Tutanota](https://tutanota.com) (Germany) and [Proton Mail](https://proton.me) (Switzerland) as lean privacy‑friendly alternatives, but I have not personally tried either of them (yet).

## Communication and office suites

Something I have been using a lot over the years is Google Workspace (Docs, Sheets, Slides, Drive, Gmail, Calendar). So my first focus was for alternatives that would allow me to keep a similar workflow without relying on US‑based services.

- [**Proton**](https://proton.me) is probably the one I am most comfortable recommending to non‑technical friends: [end‑to‑end encrypted mail](https://proton.me/mail), VPN, [Drive](https://proton.me/drive), and a lot more, all under one account, with data encrypted and stored in Switzerland and EU data centres.

  I like their VPN a lot and can warmly recommend it (alternatively have a look at [Mullvad](http://mullvad.net/)). And I keep hearing excellent reviews of their mail service, to the point that if I decide to leave Fastmail this is most likely going to be my first choice.

  However, for what concerns the Drive, I regularly bump into critical reviews, describing similar sets of issues. I would probably test it carefully for a bit before buying it. 

  My main worry with Proton is that it is (or at least seems to be) a one-person company, so I am not sure how sustainable will be in the long run.
  So far it has proven to be quite reliable though, so it may just be a non-worry after all.

- [**Nextcloud**](https://nextcloud.com) is a self‑hostable content collaboration platform. Many people already know it and it is available from many vendors all over the world: it provides file sync and sharing, among other things, and all under your own control if you self-host.

  With inexpensive EU hosting (for example [Hetzner Storage Share](https://www.hetzner.com/storage/storage-share), which however requires [some extra work for the collaborative features](https://status.hetzner.com/incident/e9878d8c-9875-49bb-ba10-3aa263957db2), or [the good cloud](https://thegood.cloud/), a local Dutch providers) it is one of the most compelling ways to keep your data in Europe while still enjoying a reasonably modern collaboration experience.

  It lacks e2e encryption, but for many use cases I think it provides a good trade‑off between privacy, convenience, and sovereignty. This fits also in the next section, as Nextcloud works well as a file storage and sync solution.

- [**mailbox.org**](https://mailbox.org/en) is a German email provider that has grown into a full workspace, with mail, calendar, [Drive](https://mailbox.org/en/product/drive/), Meeting and Office tools in one place.

  All data is stored in their own data centres in Berlin, powered by renewable energy (this is commont to many other services in this posto, although I did not make it explicit) and protected under strict German and EU privacy laws, with end‑to‑end encrypted email, encrypted cloud storage, and GDPR‑compliant video conferencing.

  I have not tested it personally, but it seems a solid option that is worth considering, and the pricing is quite reasonable.

- [**Infomaniak’s KSuite**](https://www.infomaniak.com/en/ksuite) seems also a very interesting “European Google Workspace clone”: they have [kDrive for storage](https://www.infomaniak.com/en/ksuite/kdrive) that also allows for online document editing, e-mail, calendars, chat and more, all on a Swiss, privacy‑focused cloud.

  On paper it looks really excellent. In practice my experiment stalled because I could not figure out how to try the free kSuite and kDrive, and the management panel looked like business/enterprise oriented more than personal.

  It remains on my _to be properly tested_ list, but I think it will need quite some simplification of the onboarding to be usable for personal use.

- [**Drime**](https://drime.cloud) provides an EU‑hosted, GDPR‑compliant cloud storage service with collaborative editing features. It looks promising but, at the time of writing, still feels more like an MVP than a fully battle‑tested platform. And the lack of actual screenshots in the website does not help my  confidence.

- [**OnlyOffice**](https://www.onlyoffice.com) is a collaborative online office suite with editors for text documents, spreadsheets, presentations and forms. You can self‑host it or use their EU‑hosted cloud, OnlyOffice Doc. It is not the cheapest option out there, but seems a well‑designed platform that can integrate nicely with Nextcloud or other storage solutions, so worth a mention here.

- [**Collabora Online**](https://www.collaboraonline.com/collabora-online/) is a browser-based libreoffice that can be plugged into other platforms, like Nextcloud. Since OnlyOffice has a cloud offering, I was hoping they would provide reasonably priced drive-like hosting as well. They kind of do, but the pricing seem more aimed at larger business deployments rather than small personal setups.

## Storage and file‑centric tools

One of the first services I replaced was Dropbox.
I was annoyed by the lack of encryption and the fact that they have (had?) former US secretaries of state in their board. But with Snowden's revelations I simply decided it was time to move on.

### End-to-end encrypted

- [**Tresorit**](https://tresorit.com) is a Swiss-based, end‑to‑end encrypted cloud storage service. It is aimed at both individuals and businesses that prioritise security and privacy. The data is stored only in EU data centres under a zero‑knowledge model and their software (desktop and mobile) works very well.

  I have been using it for a while now and I am quite happy with it. So even if it is not the cheapest option out there, so far it has been able to deliver a smooth experience. The one hiccup I had was resolved quickly by their support team, to add to the positive experience.

  To me it is one of the stronger “Dropbox/Google Drive, but actually private and EU‑focused” options.

- [**Internxt**](https://internxt.com) is also an EU‑based, open‑source, end-to-end encrypted cloud storage provider. I really like its offering as a pure storage service, and the fact that it is open source. 

  My main worry is that I have encountered mixed reviews about their reliability, so I would probably test it carefully before committing to it for important data.

- [**Filen**](https://filen.io), like the previous two services, offers end‑to‑end encrypted cloud storage from Germany. It also offers a chat interface and a collaborative pure-text notes editing.

  Similar to Internxt, I like the concept and the focus on privacy, but I have seen mixed reviews about reliability and, differently from Internxt, it had no security audit. I would probably test it carefully before committing to it for important data.

### Other privacy-focused options

- [**pCloud**](https://www.pcloud.com/eu) is a Swiss cloud storage provider, not end-to-end encrypted, but it gets a mention since I have read many good things about it. Also, with the optional _pCloud Crypto_ add‑on, it also offers client‑side end-to-end encryption for selected folders. Seems to have quite a good offering and to have been there for a while, so worth considering.

- [**Jottacloud**](https://jottacloud.com/en/) is a Norwegian cloud storage and backup service, with all data stored on their own servers in Norway under GDPR and strict local privacy laws. It has no end-to-end encryption offer, but I also decided to mention it since it seems a solid privacy-oriented service with very competitive pricing and good reviews.

- [**Koofr**](https://koofr.eu) is a Slovenian cloud storage provider, explicitly designed as a privacy‑oriented service with no user tracking and GDPR compliance by default. It is not end-to-end encrypted, but offers an optional client‑side encryption via _Koofr Vault_ for extra privacy.

  A unique selling point is its ability to integrate and unify access to other cloud accounts (Google Drive, Dropbox, OneDrive) in a single interface, with unified search, while storing your own files securely in the EU.

  I have not tested it personally, but it also seems an interesting option and had good reviews. Especially for backup needs, it supports rclone, which is a plus for me.

### Notable mention (sync only)

- [**Syncthing**](https://syncthing.net) is an entirely different beast: open‑source, peer‑to‑peer file synchronization without any central server.

  It is perfect for keeping your own devices in sync without trusting a third‑party host, but by design it does not solve the “I need a hosted collaboration space” problem. I have tried it out and it works very well for what it does.

  In that case you would need to install your own NAS and run Syncthing on it, which is not for everyone, but for tech-savvy users could be a great way to keep full control of your data.

## Knowledge management and writing

Beyond storage there are plenty of other convenient cloud-based tools. Here what I thought are interesting opportunities, that do not fit with the lists above.

- [**Nuclino**](https://www.nuclino.com) is a knowledge management tool to organise documents, projects and internal notes. To me it is some kind of EU‑based Notion. Not something I need right now, but I had a very good impression.

- [**CryptPad**](https://cryptpad.fr) is one of the most interesting projects in this whole list: an open‑source, end‑to‑end encrypted collaboration suite with documents, spreadsheets, presentations, whiteboards, Kanban boards and forms developed by the French government (I think).

  The server cannot read user content, which is exactly the direction I would like more tools to take, but finding suitable hosting that matches my needs has proven trickier than expected so far. I'll definitely keep an eye on it.

- [**LaSuite**](https://lasuite.numerique.gouv.fr/en), is a collection of digital tools curated by the French government for public‑sector collaboration, hosted on secure French infrastructure. I knew they had developed [Docs](https://github.com/suitenumerique/docs), which I really liked, and was pleasantly surprised to discover that they now have this whole suite of tools, including spreadsheets, presentations, forms, wikis, and more.

  It is extremely appealing from a sovereignty perspective. My biggest issue, for now, is that it is almost entirely French‑centred (including documentation) and I have not yet found a hosting provider that offers it as a managed service in English. I will definitely also keep an eye on this.

- [**HedgeDoc**](https://hedgedoc.org) is an open‑source, self‑hosted collaborative Markdown editor for real‑time note‑taking, presentations and diagrams. It is simply excellent. I need to find a good managed hosting to move away from HackMD to this. It is not very hard to self-host, but right now I don't have the time to look after it.

## Other tools

Finally, for some things that really does not fit with the rest.

### Language help

[**LanguageTool**](https://languagetool.org/) is a multilingual AI‑powered grammar and style checker that integrates nicely into browsers and editors.

I have it on the list, because there have been discussions to provide Grammarly licenses to our students (I don't know if we do, and honestly hope not). Since Grammarly is US‑based, I was curious to see if a EU-based alternative existed, and it turns out that LanguageTool fits this bill.

I don't use either of them, so I cannot really compare. But it is here, just in case...

### Photo and video management

- [**Immich**](https://immich.app) is a high‑performance, open‑source self‑hosted solution for photo and video backup with automatic device syncing, face recognition, ML‑powered search, albums and sharing. Essentially a privacy‑respecting Google Photos replacement.

  The downsite is only that you have to host yourself. But from what I saw, it is a relatively smooth sail that can give you full control over your media library without vendor lock‑in.

- [**Ente Photos**](<https://ente.io>) offers end‑to‑end encrypted photo and video backup with EU servers, open‑source apps, family sharing and easy Apple and Google Photos migration. Unlike Immich it is a hosted service and it strikes a good balance between convenience and privacy for non‑technical users. I was impressed by how well-made it looks, the incredibly positive reviews and the good pricing.

## Search engines

Reducing US reliance also means looking beyond storage and office tools to everyday browsing habits. Here are privacy‑respecting search alternatives with strong EU ties.

- [**Ecosia**](https://www.ecosia.org) is a Berlin‑based nonprofit search engine that uses Bing backend but plants trees with ad revenue, stores minimal data, and complies with strict German/EU privacy laws. I used it for a while and liked the idea, but I found the search results not as good as other engines unfortunately. Especially given its environmental focus, I promised myself to keep giving it another try every now and then.

- [**Qwant**](https://www.qwant.com) is a French privacy‑focused search engine that doesn't track users or sell data, using its own index plus Bing fallback, with dedicated EU servers and kids' search. I had mixed results with it, so maybe it is a problem with Bing itself that I am having. But it is worth a try, it is a nice option to have.

- [**Kagi**](https://kagi.com) is a paid, ad‑free search engine that prioritises quality results and user privacy. No tracking or data sales, with features like custom filters on the results (no Pinterest or Qwora, yay!) and Privacy Pass for anonymous authentication. While US‑based, it has a strong privacy ethos, and as a paying user I am having a great experience so far.

- [**DuckDuckGo**](https://duckduckgo.com) is also US‑based but aggressively privacy‑focused with no tracking, EU data processing, and active advocacy against Google monopolies. Again not purely European but a solid bridge option.

At this point I am always using Kagi or DuckDuckGo for searches.
I can't really remember when was the last time I used Google Search.

## Where this leaves me

This is not a conclusion, and surely not comprehensive. Take it as just a snapshot. I hope it may be useful to others as well, and it is now here for me to not forget :D

If you know of other EU-based privacy-focused services that I should check out, please let me know! I'd be happy to keep expanding this list.
