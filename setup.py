#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""A generic notifier/event scheduler abstraction

pyNotifier provides an implementation of a notifier/event scheduler and is
capable of wrapping other notifier implementations of GTK+, Qt and wxWindows.
This enables library developers to write code that may be used in applications
with """

from distutils.core import setup

from notifier import version

classifiers = """\
Development Status :: 5 - Production/Stable
Environment :: Console
Environment :: X11 Applications :: GTK
    Environment :: X11 Applications :: Qt
Intended Audience :: Developers
License :: OSI Approved :: GNU General Public License (GPL)
Programming Language :: Python
Topic :: Software Development :: Libraries :: Python Modules
Operating System :: Unix
"""

doclines = __doc__.split( '\n' )
setup( name	= 'pyNotifier',
       version	= version.VERSION,
       license  = 'GPLv2',
       description = doclines[ 0 ],
       long_description = '\n'.join( doclines[ 2 : ] ),
       author	= 'Andreas Büsching',
       author_email = 'crunchy@tzi.de',
       url	= 'http://www.mbus.org/',
       download_url = 'ftp://ftp.mbus.org/tzi/dmn/mbus/python/',
       platforms = [ 'any', ],
       classifiers = filter( None, classifiers.split( '\n' ) ),
       packages = [ 'notifier', ],
     )
