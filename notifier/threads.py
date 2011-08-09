#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author: Andreas Büsching	<crunchy@bitkipper.net>
#
# simple interface to handle threads synchron to the notifier loop
#
# Copyright (C) 2006
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

import notifier

import thread

__all__ = [ 'Simple' ]

_threads = []

class Simple( object ):
	def __init__( self, name, function, callback ):
		self._name = name
		self._function = function
		self._callback = callback
		self._result = None
		self._finished = False
		self._id = None
		self._lock = thread.allocate_lock()
		global _threads
		if not _threads:
			notifier.dispatcher_add( _results )
		_threads.append( self )

	def run( self ):
		self._id = thread.start_new_thread( self._run, () )

	def _run( self ):
		try:
			tmp = self._function()
		except BaseException, e:
			tmp = e
		self._lock.acquire()
		self._result = tmp
		self._finished = True
		self._lock.release()

	def lock( self ):
		self._lock.acquire()

	def unlock( self ):
		self._lock.release()

	def name( self ):
		return self._name

	def finished( self ):
		return self._finished

	def announce( self ):
		self._callback( self, self._result )

def _results():
	finished = []
	global _threads
	for task in _threads:
		task.lock()
		if task.finished():
			task.announce()
			finished.append( task )
		task.unlock()

	for t in finished:
		_threads.remove( t )

	return ( len( _threads ) > 0 )
