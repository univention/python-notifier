#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author: Andreas Büsching <crunchy@bitkipper.net>
#
# generic notifier implementation
#
# Copyright (C) 2004, 2005, 2006, 2007, 2008, 2009
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

"""Simple mainloop that watches sockets and timers."""

# python core packages
from copy import copy
from time import time

import errno
import os
import select
import socket
import sys

# internal packages
import log
import dispatch

IO_READ = select.POLLIN | select.POLLPRI
IO_WRITE = select.POLLOUT
IO_EXCEPT = select.POLLERR | select.POLLHUP | select.POLLNVAL

IO_ALL = IO_READ | IO_WRITE

__poll = select.poll()
__sockets = {}
__sockets[ IO_READ ] = {}
__sockets[ IO_WRITE ] = {}
__sockets[ IO_EXCEPT ] = {}
__timers = {}
__timer_id = 0
__min_timer = None
__in_step = False
__step_depth = 0
__step_depth_max = 0

_options = {
	'recursive_depth' : 2,
}

def socket_add( id, method, condition = IO_READ ):
	"""The first argument specifies a socket, the second argument has to be a
	function that is called whenever there is data ready in the socket.
	The callback function gets the socket back as only argument."""
	global __sockets, __poll

	# ensure that already registered condition do not get lost
	for cond in ( IO_READ, IO_WRITE, IO_EXCEPT ):
		if id in __sockets[ cond ]:
			condition |= cond
	__sockets[ condition ][ id ] = method
	__poll.register( id, condition )

def socket_remove( id, condition = IO_READ ):
	"""Removes the given socket from scheduler. If no condition is specified the
	default is IO_READ."""
	global __sockets, __poll
	remain = 0
	for cond in ( IO_READ, IO_WRITE, IO_EXCEPT ):
		if id in __sockets[ cond ] and condition != cond:
			remain |= cond

	if remain:
		__poll.register( id, remain )
	else:
		__poll.unregister( id )

	if id in __sockets[ condition ]:
		del __sockets[ condition ][ id ]

def timer_add( interval, method ):
	"""The first argument specifies an interval in milliseconds, the second
	argument a function. This is function is called after interval
	seconds. If it returns true it's called again after interval
	seconds, otherwise it is removed from the scheduler. The third
	(optional) argument is a parameter given to the called
	function. This function returns an unique identifer which can be
	used to remove this timer"""
	global __timer_id

	try:
		__timer_id += 1
	except OverflowError:
		__timer_id = 0

	__timers[ __timer_id ] = \
	[ interval, int( time() * 1000 ) + interval, method ]

	return __timer_id

def timer_remove( id ):
	"""Removes the timer identifed by the unique ID from the main loop."""
	if id in __timers:
		del __timers[ id ]

def dispatcher_add( method, min_timeout = True ):
	global __min_timer
	__min_timer = dispatch.dispatcher_add( method, min_timeout )

def dispatcher_remove( method ):
	global __min_timer
	__min_timer = dispatch.dispatcher_remove( method )

__current_sockets = {}
__current_sockets[ IO_READ ] = []
__current_sockets[ IO_WRITE ] = []
__current_sockets[ IO_EXCEPT ] = []

( INTERVAL, TIMESTAMP, CALLBACK ) = range( 3 )

def step( sleep = True, external = True ):
	"""Do one step forward in the main loop. First all timers are checked for
	expiration and if necessary the accociated callback function is called.
	After that the timer list is searched for the next timer that will expire.
	This will define the maximum timeout for the following select statement
	evaluating the registered sockets. Returning from the select statement the
	callback functions from the sockets reported by the select system call are
	invoked. As a final task in a notifier step all registered external
	dispatcher functions are invoked."""

	global __in_step, __step_depth, __step_depth_max, __min_timer

	__in_step = True
	__step_depth += 1

	try:
		if __step_depth > __step_depth_max:
			log.exception( 'maximum recursion depth reached' )
			return

		# get minInterval for max timeout
		timeout = None
		if not sleep:
			timeout = 0
		else:
			now = int( time() * 1000 )
			for interval, timestamp, callback in __timers.values():
				if not timestamp:
					# timer is blocked (recursion), ignore it
					continue
				nextCall = timestamp - now
				if timeout == None or nextCall < timeout:
					if nextCall > 0:
						timeout = nextCall
					else:
						timeout = 0
						break
			if __min_timer and ( __min_timer < timeout or timeout is None ):
				timeout = __min_timer

		# wait for event
		fds = __poll.poll( timeout )

		# handle timers
		for i, timer in __timers.items():
			timestamp = timer[ TIMESTAMP ]
			if not timestamp:
				# prevent recursion, ignore this timer
				continue
			now = int( time() * 1000 )
			if timestamp <= now:
				# Update timestamp on timer before calling the callback to
				# prevent infinite recursion in case the callback calls
				# step().
				timer[ TIMESTAMP ] = 0
				if not timer[ CALLBACK ]():
					if i in __timers:
						del __timers[ i ]
				else:
					# Find a moment in the future. If interval is 0, we
					# just reuse the old timestamp, doesn't matter.
					now = int( time() * 1000 )
					if timer[ INTERVAL ]:
						timestamp += timer[ INTERVAL ]
						while timestamp <= now:
							timestamp += timer[ INTERVAL ]
					timer[ TIMESTAMP ] = timestamp

		# handle sockets
		for fd, condition in fds:
			is_socket = isinstance( fd, ( socket.socket, file, socket._socketobject ) )
			if ( is_socket and ( getattr( fd, 'closed', False ) or fd.fileno() != -1 ) ) or \
				   ( isinstance( fd, int ) and fd != -1 ):
				for cond in ( IO_READ, IO_WRITE, IO_EXCEPT ):
					# TODO: this might not work with IO_EXCEPT
					if cond & condition and fd in __sockets[ cond ] and \
						   not __sockets[ cond ][ fd ]( fd ):
						socket_remove( fd, cond )

		# handle external dispatchers
		if external:
			__min_timer = dispatch.dispatcher_run()
	finally:
		__step_depth -= 1
		__in_step = False

def loop():
	"""Executes the 'main loop' forever by calling step in an endless loop"""
	while 1:
		step()

def _init():
	global __step_depth_max

	__step_depth_max = _options[ 'recursive_depth' ]
