#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# log.py
# 
# Author: Andreas Büsching <crunchy@tzi.de>
# 
# log - a logging facility for the generic notifier module
# 
# $Id$
# 
# Copyright (C) 2004 Andreas Büsching <crunchy@tzi.de>
# 
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2, or (at your option)
# any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.
 
import logging

# create and setup the root logger object.
# using logging.getLogger() gives the root logger, calling
# logging.getLogger('foo') returns a new logger with the same default
# settings.
__root_logger = logging.getLogger()

# set stdout logging
# TODO: find a way to shut down that logger later when the user
# wants to visible debug in the terminal
__formatter = logging.Formatter( '%(levelname)s %(module)s' + \
                                 '(%(lineno)s): %(message)s' )
__handler = logging.StreamHandler()
__handler.setFormatter( __formatter )
__root_logger.addHandler( __handler )

instance = logging.getLogger( 'notifier' )

debug = instance.debug
info = instance.info
warn = instance.warn
error = instance.error
critical = instance.critical
exception = instance.exception
