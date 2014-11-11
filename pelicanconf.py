#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = u'Estel'
SITENAME = u'Die Luft der Freiheit weht!'
SITEURL = 'http://libereco.cn'
#SITEURL = ''

PATH = 'content'

TIMEZONE = 'Asia/Shanghai'

DATE_FORMATS = {
    'en':('usa','%a, %d %b %Y'),
    'zh':('chs','%Y-%m-%d, %a'),
}

#DEFAULT_LANG = u'zh_CN'
DEFAULT_LANG = u'en_US'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
RATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# path-specific metadata
EXTRA_PATH_METADATA = {
    'extra/robots.txt': {'path': 'robots.txt'},
    }

# static paths will be copied without parsing their contents
STATIC_PATHS = [
    'pictures',
    'extra/robots.txt',
    ]

# Blogroll
LINKS = (('Pelican', 'http://getpelican.com/'),
         ('Python.org', 'http://python.org/'),
         ('Jinja2', 'http://jinja.pocoo.org/'),)

# Social widget
SOCIAL = (('Weibo', 'http://weibo.com/1958413980/profile'),
          ('About Me', 'http://about.me/sunqi'),
          ('Facebook','https://www.facebook.com/frank.sun.16'),
          ('Twitter','https://twitter.com/sunqinwpu'))

DEFAULT_PAGINATION = 10

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True


THEME = "themes/pelican-sober"

DEFAULT_CATEGORY = 'Others'

DUOSHUO_SITENAME = 'leboreco'
