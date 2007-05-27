#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author: Andreas Büsching <crunchy@bitkipper.net>
#
# a generic dispatcher implementation
#
# Copyright (C) 2006, 2007
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

"""generic implementation of external dispatchers, integratable into
several notifiers."""

from copy import copy

# required for dispatcher use
MIN_TIMER = 100

__dispatchers = {}
__dispatchers[ True ] = []
__dispatchers[ False ] = []

def dispatcher_add( method, min_timeout = True ):
	"""The notifier supports external dispatcher functions that will be called
	within each scheduler step. This functionality may be usful for
	applications having an own event mechanism that needs to be triggered as
	often as possible. This method registers a new dispatcher function. To
	ensure that the notifier loop does not suspend to long in the sleep state
	during the select a minimal timer MIN_TIMER is set to guarantee that the
	dispatcher functions are called at least every MIN_TIMER milliseconds."""
	global __dispatchers, MIN_TIMER
	__dispatchers[ min_timeout ].append( method )
	if __dispatchers[ True ]:
		return MIN_TIMER
	else:
		return None

def dispatcher_remove( method ):
	"""Removes an external dispatcher function from the list"""
	global __dispatchers, MIN_TIMER
	for bool in ( True, False ):
		if method in __dispatchers[ bool ]:
			__dispatchers[ bool ].remove( method )
			break
	if __dispatchers[ True ]:
		return MIN_TIMER
	else:
		return None

def dispatcher_run():
	global __dispatchers
	for bool in ( True, False ):
		for disp in copy( __dispatchers[ bool ] ):
			if not disp():
				dispatcher_remove( disp )
	if __dispatchers[ True ]:
		return MIN_TIMER
	else:
		return None

def dispatcher_count():
	global __dispatchers
	return len( __dispatchers )
