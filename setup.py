#!/usr/bin/env python
# -*- coding: utf-8 -*-

from distutils.core import setup

setup( name	= 'pyNotifier',
       version	= '0.2.1',
       license  = 'GPL',       
       description = 'a generic notifier, which can be used with a lot a different widget sets',       
       author	= 'Andreas Büsching',
       author_email = 'crunchy@tzi.de',
       url	= 'http://www.crunchy-home.de/download/',
       packages = [ 'notifier', 'notifier.generic', 'notifier.gtk',
                    'notifier.qt', 'notifier.wx' ],
     )
