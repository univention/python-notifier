#!/usr/bin/env python
#-*- coding: utf-8 -*-
#
# Author: Andreas Büsching <crunchy@bitkipper.net>
#
# logger
#
# Copyright (C) 2005, 2006, 2009
#	Andreas Büsching <crunchy@bitkipper.net>
#
# This library is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License version
# 2.1 as published by the Free Software Foundation.
#
# This library is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.	See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
# 02110-1301 USA

import os

import logging
import notifier.log

if __name__ == '__main__':
	for level in ( logging.CRITICAL, logging.DEBUG, logging.ERROR, logging.FATAL, logging.WARN, logging.INFO ):
		notifier.log.set_level( level )
		notifier.log.error( 'LEVEL: %d' % level )
		notifier.log.error( 'error' )
		notifier.log.warn( 'warn' )
		notifier.log.info( 'info' )
		notifier.log.debug( 'debug' )
