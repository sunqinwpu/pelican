#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = 'Estel'
SITENAME = 'Die Luft der Freiheit weht!'
SITESUBTITLE = 'Estel\'s blog!'
SITEURL = 'http://libereco.cn'
#SITEURL = ''

PATH = 'content'

TIMEZONE = 'Asia/Shanghai'

DATE_FORMATS = {
    'en':('usa','%a, %d %b %Y'),
    'zh':('chs','%Y-%m-%d, %a'),
}

DEFAULT_LANG = 'zh_CN'
#DEFAULT_LANG = 'en_US'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
RATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = 'feeds/all-%s.atom.xml'
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
         ('Hatter Jiang', 'http://p.rogram.me'),
         ('Jinja2', 'http://jinja.pocoo.org/'),)

# Social widget
SOCIAL = (('Weibo', 'http://weibo.com/1958413980/profile'),
          ('About Me', 'http://about.me/sunqi'),
          ('Facebook','https://www.facebook.com/frank.sun.16'),
          ('Twitter','https://twitter.com/sunqinwpu'))

GITHUB_URL = 'https://github.com/sunqinwpu'
TWITTER_USERNAME = 'sunqinwpu'

DEFAULT_PAGINATION = 10

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True


THEME = "themes/pelican-sober"
PELICAN_SOBER_ABOUT = "My name is Qi Sun, now I am working at alibaba. Ubuntu,java,python."
PELICAN_SOBER_STICKY_SIDEBAR = True

DEFAULT_CATEGORY = 'Others'

DUOSHUO_SITENAME = 'libereco'

ARTICLE_URL = 'posts/{category}/{date:%Y}/{date:%m}/{date:%d}/{slug}/'
ARTICLE_SAVE_AS = 'posts/{category}/{date:%Y}/{date:%m}/{date:%d}/{slug}/index.html'
ARTICLE_LANG_URL = 'posts/{category}/{date:%Y}/{date:%m}/{date:%d}/{slug}-{lang}/'
ARTICLE_LANG_SAVE_AS = 'posts/{category}/{date:%Y}/{date:%m}/{date:%d}/{slug}-{lang}/index.html'

GOOGLE_ANALYTICS = 'UA-57075958-1'
