---
title: "Save your battery life"
date: 2013-09-29T11:00:00.000Z
lastmod: 2013-10-29T16:01:57.000Z
tags: ["good practice", "battery life"]
categories: ["Blog"]
slug: "save-your-battery-life"
disqus_identifier: 5
---

Yesterday, by pure chance, I ended up reading an interview with a Li-Ion battery specialist. I was quite impressed (and scared) to hear that continuous full charge/discharege of the battery will ruin their life, and that is a best practice to plug it before it goes under 20% of the charge and unplug it when it reaches 80% charge. 

I wanted to post a link to that source but in some way I cannot find it anymore. With google anyway I've found many trustable sources with suggestions on **how to preserve the life of li-ion or li-ion polymer batteries**. A short summary of their tips is listed below, I hope it can be of help to other people.

At the moment I am developing a small applet for Mac OSX that reminds me to connect and disconnect the battery when it reaches the proper level. I will upload it soon on github, if you are interested stay tuned.

### Good practice in a nutshell

* Optimal battery use is between 20% and 80%: aim to discharge to ~20% then charge to ~80%
* Full discharges damage the battery: try to avoid discharging to below 10%
* Keeping the battery at 100%, i.e. keeping it plugged in to the charger, damages the battery (through being at 100% and because it's likely to be hotter when plugged in)
* Humidity damages the battery: keep it dry
* Heat damages the battery: keep as cool as possible at all times but above 0 degrees Celsius and avoid the fridge/freezer
* Li-Ion batteries don't have a memory: they don't suffer from frequent small charges
* To re-calibrate the fuel gauge of your battery (improve battery level reporting, not battery _memory_): fully discharge it approximately once a month, or once every 30-40 charges
* It is better to charge the battery with the device turned off
* If you need to store the battery without using it for a period of time, discharge to 40-50%

To remember to make a full discharge once a month Apple prepared a [downloadable calendar event](https://www.apple.com/batteries/images/notebook_icalreminder.ics). Just open it in your favourite calendar application and it will set up a monthly reminder.

Hopefully these tips should help you to extend the longevity and the capacity of your li-ion batteries, on the other hand it seems pretty clear that these best practices are hard to follow.

####Sources

For additional informations have a look at the following links:

- Battery University: [Charging Li-Ion Batteries](https://batteryuniversity.com/learn/article/charging_lithium_ion_batteries)
, [How to Prolong Lithium Based Batteries](https://batteryuniversity.com/learn/article/how_to_prolong_lithium_based_batteries)
- Gigaom: [Extend the battery life of your MacBook, no matter how old it is](https://gigaom.com/2013/06/22/extend-the-battery-life-of-your-macbook-no-matter-how-old-it-is/)
- Fergyblog: [How to Prolong Lithium-Ion Battery Life](https://fer.gy/2012/04/15/how-to-prolong-lithium-ion-battery-life/)
- Ars Technica: [What is the Best Way to Use a Li-Ion Battery?](https://arstechnica.com/gadgets/2011/02/ask-ars-what-is-the-best-way-to-use-an-li-ion-battery/)
- Geeknizer: [How to Extend Battery Life](https://geeknizer.com/how-to-increase-battery-life/)

---
### Update
The small program I promised above is ready. You can check the source code in [its github repository](https://github.com/mseri/saveBattery) or download it packaged as an app from [here](https://dl.dropboxusercontent.com/u/663035/batteryLifeExtender.zip).

It's just a status bar application for MacOSX 10.8+ that fires notifications to inform you when to plug or unplug the battery.

---
### Update 2
Somebody made a sort of version with steroids of my app. IMHO it is quite expensive, but if you are interested, you can download it from the [AppStore](https://itunes.apple.com/it/app/fruitjuice/id671736912)