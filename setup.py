#!/usr/bin/env python
# -*- coding: utf-8 -*-

from distutils.core import setup

from notifier import version

setup( name	= 'pyNotifier',
       version	= version.VERSION,
       license  = 'GPLv2',
       description = 'a generic notifier that has its own implementation, but also is capable of wrapping other notifier implementations of GTK+, Qt and WX',
       author	= 'Andreas Büsching',
       author_email = 'crunchy@tzi.de',
       url	= 'http://www.crunchy-home.de/download/',
       packages = [ 'notifier', ],
     )
