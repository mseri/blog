#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

# This file is only used if you use `make publish` or
# explicitly specify it as your config file.

import os
import sys
sys.path.append(os.curdir)
from pelicanconf import *

SITEURL = 'http://www.mseri.me'
RELATIVE_URLS = False

FEED_ATOM = 'feed/atom.xml'
FEED_RSS = 'feed/rss.xml'
FEED_MAX_ITEMS = 8

DELETE_OUTPUT_DIRECTORY = False

# Following items are often useful when publishing

DISQUS_SITENAME = "talesofafractalspectrum"
GOOGLE_ANALYTICS = "UA-44365202-1"
