#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

LOCALE = 'en_US.UTF-8'
#LOCALE = ('zh_CN.utf8', 'en_US.utf8')
AUTHOR = 'Estel'
SITENAME = 'Die Luft der Freiheit weht!'
SITESUBTITLE = 'Estel\'s blog!'
SITEURL = 'https://libereco.cn'
#SITEURL = ''
TIMEZONE = 'Asia/Shanghai'

PATH = 'content'


DATE_FORMATS = {
    'en':('usa','%a, %d %b %Y'),
    'zh':('chs','%Y-%m-%d, %a'),
}

DEFAULT_LANG = 'zh_CN'
#DEFAULT_LANG = 'en_US'

# Feed generation is usually not desired when developing
# FEED_ALL_ATOM = True
# FEED_ALL_RSS = True
TRANSLATION_FEED_ATOM = 'feeds/all-{lang}.atom.xml'

# path-specific metadata
EXTRA_PATH_METADATA = {
    'extra/robots.txt': {'path': 'robots.txt'},
    }

# static paths will be copied without parsing their contents
STATIC_PATHS = [
    'pictures',
    'theme/images',
    'extra/robots.txt',
    ]

# Blogroll
LINKS = (('Pelican', 'http://getpelican.com/'),
         ('Hatter Jiang', 'http://p.rogram.me'),
         ('Jinja2', 'http://jinja.pocoo.org/'),
         ('OWASP', 'http://www.owasp.org.cn/'),)

# Social widget
SOCIAL = (('Weibo', 'http://weibo.com/1958413980/profile'),
          ('About Me', 'http://about.me/sunqi'),
          ('Facebook','https://www.facebook.com/frank.sun.16'),
          ('Twitter','https://twitter.com/sunqinwpu'))

GITHUB_URL = 'https://github.com/sunqinwpu'
TWITTER_USERNAME = 'sunqinwpu'

DEFAULT_PAGINATION = 10

DISQUS_SITENAME = 'liberecocn'
# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True


#THEME = "themes/blue-penguin"
#THEME = "themes/pelican-sober"
THEME = "pelican-themes/elegant"

#elegant theme
DIRECT_TEMPLATES = (('index', 'tags', 'categories','archives', 'search', '404'))
TAG_SAVE_AS = ''
CATEGORY_SAVE_AS = ''
AUTHOR_SAVE_AS = ''
USE_SHORTCUT_ICONS = True

# Elegant Lables
SOCIAL_PROFILE_LABEL = u'Stay in Touch'
RELATED_POSTS_LABEL = 'Keep Reading'
SHARE_POST_INTRO = 'Like this post? Share on:'
COMMENTS_INTRO = 'So what do you think? Dis I miss something? Is any part unclear? Leave your comments below.'

# Mailchimp
EMAIL_SUBSCRIPTION_LABEL = u'Get Monthly Updates'
EMAIL_FIELD_PLACEHOLDER = u'Enter your email...'
SUBSCRIBE_BUTTON_TITLE = u'Send me Free updates'
MAILCHIMP_FORM_ACTION = u'empty'


# SMO
FEATURED_IMAGE = SITEURL + '/theme/images/apple-touch-icon-152x152.png'




ARTICLE_URL = 'posts/{category}/{date:%Y}/{date:%m}/{date:%d}/{slug}/'
ARTICLE_SAVE_AS = 'posts/{category}/{date:%Y}/{date:%m}/{date:%d}/{slug}/index.html'
ARTICLE_LANG_URL = 'posts/{category}/{date:%Y}/{date:%m}/{date:%d}/{slug}-{lang}/'
ARTICLE_LANG_SAVE_AS = 'posts/{category}/{date:%Y}/{date:%m}/{date:%d}/{slug}-{lang}/index.html'

GOOGLE_ANALYTICS = 'UA-57075958-1'

# Plugins and extensions
MARKDOWN = ['codehilite(css_class=highlight)', 'extra', 'headerid', 'toc']
PLUGIN_PATHS = ['../pelican-plugins']
#PLUGINS = ['sitemap', 'extract_toc', 'tipue_search', 'liquid_tags.img',
#           'neighbors', 'latex', 'related_posts', 'assets', 'share_post',
#		              'multi_part']
PLUGINS=['sitemap','extract_toc','tipue_search','liquid_tags.img',
			   'tag_cloud', 'related_posts']
SITEMAP = {
    'format': 'xml',
    'priorities': {
        'articles': 0.5,
        'indexes': 0.5,
        'pages': 0.5
    },
    'changefreqs': {
        'articles': 'monthly',
        'indexes': 'daily',
        'pages': 'monthly'
    }
}
