#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author: Andreas Büsching <crunchy@bitkipper.net>
#
# log - a logging facility for the generic notifier module
#
# Copyright (C) 2005, 2006, 2010
#		Andreas Büsching <crunchy@bitkipper.net>
#
# This library is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License version
# 2.1 as published by the Free Software Foundation.
#
# This library is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
# 02110-1301 USA

import logging
import sys

instance = logging.getLogger( 'notifier' )
formatter = logging.Formatter( "%(asctime)s: %(name)s: %(levelname)-8s: %(message)s" )
stream = logging.StreamHandler( sys.stderr )
stream.setFormatter( formatter )
try:
	file = logging.FileHandler( '/var/log/python-notifier.log' )
	file.setFormatter( formatter )
except:
	pass

instance.addHandler( stream )
instance.addHandler( file )

debug = instance.debug
info = instance.info
warn = instance.warn
error = instance.error
critical = instance.critical
exception = instance.exception

set_level = instance.setLevel
