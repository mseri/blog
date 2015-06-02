#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = 'Marcello Seri'
SITENAME = 'Tales of a Fractal Spectrum'
SITEDESC = 'Free thoughts of a geeky mathematician'
SITEURL = ''

SITE_LOGO_URL = 'images/gauss_logo.png'

PATH = 'content'

# static paths will be copied without parsing their contents
STATIC_PATHS = [
    'images',
    'static'
    ]
EXTRA_PATH_METADATA = {
    'static/robots.txt': {'path': 'robots.txt'},
    'static/CNAME': {'path': 'CNAME'},
    'static/favicon.ico': {'path': 'favicon.ico'}
    }

TIMEZONE = 'Europe/London'

DEFAULT_LANG = 'en'

ARTICLE_URL     = '{slug}/'
ARTICLE_SAVE_AS = '{slug}/index.html'

PLUGIN_PATHS = ['../pelican-plugins/']
PLUGINS      = ['sitemap']

THEME = '../pelican-themes/purity/'

SOCIAL   = True
TWITTER  = "marcelloseri"
FACEBOOK = "marcello.seri" 
GPLUS    = "+MarcelloSeri"
GHUB     = "mseri"
MATHJAX = True

DEFAULT_PAGINATION = 5

# This is broken as of Pelican 3.5.0
# see https://github.com/getpelican/pelican/issues/1615
# PAGINATION_PATTERNS = (
#       (1, '{base_name}/', '{base_name}/index.html'),
#       (2, '{base_name}/page/{number}/', '{base_name}/page/{number}/index.html'),
# )

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None
