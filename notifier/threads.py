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
	"""A simple class to start a thread and getting notified when the
	thread is finished. Meaning this class helps to handle threads that
	are meant for doing some calculations and returning the
	result. Threads that need to communicate with the main thread can
	not be handeld by this class.

	If an exception is raised during the execution of the thread that is
	based on BaseException it is catched and returned as the result of
	the thread.

	Arguments:
	name: a name that might be used to identify the thread. It is not required to be unique.
	function: the main function of the thread
	callback: function that is invoked when the thread is dead. This function gets two arguments:
	  thread: nme of the thread
	  result: return value of the thread function.
	"""
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
			notifier.dispatcher_add( _simple_threads_dispatcher )
		_threads.append( self )

	def run( self ):
		"""Starts the thread"""
		self._id = thread.start_new_thread( self._run, () )

	def _run( self ):
		"""Encapsulates the given thread function to handle the return
		value in a thread-safe way and to catch exceptions raised from
		within it."""
		try:
			tmp = self._function()
		except BaseException, e:
			tmp = e
		self._lock.acquire()
		self._result = tmp
		self._finished = True
		self._lock.release()

	@property
	def name( self ):
		return self._name

	@property
	def finished( self ):
		return self._finished

	def lock( self ):
		self._lock.acquire()

	def unlock( self ):
		self._lock.release()

	def announce( self ):
		self._callback( self, self._result )

def _simple_threads_dispatcher():
	"""Dispatcher function checking for finished threads"""
	finished = []
	global _threads
	for task in _threads:
		task.lock()
		if task.finished:
			task.announce()
			finished.append( task )
		task.unlock()

	for t in finished:
		_threads.remove( t )

	return ( len( _threads ) > 0 )
