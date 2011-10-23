#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author: Andreas Büsching	<crunchy@bitkipper.net>
#
# simple interface to handle threads synchron to the notifier loop
#
# Copyright (C) 2006, 2011
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

import sys
import thread
import traceback

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
	  thread: this thread object
	  result: return value of the thread function.
	"""
	def __init__( self, name, function, callback ):
		self._name = name
		self._function = function
		self._callback = callback
		self._result = None
		self._trace = None
		self._exc_info = None
		self._finished = False
		self._id = None
		self._lock = thread.allocate_lock()
		global _threads
		if not _threads:
			notifier.dispatcher_add( _simple_threads_dispatcher )
		_threads.append( self )

	def __del__( self ):
		if self._exc_info is not None:
			del self._exc_info

	def run( self ):
		"""Starts the thread"""
		self._id = thread.start_new_thread( self._run, () )

	def _run( self ):
		"""Encapsulates the given thread function to handle the return
		value in a thread-safe way and to catch exceptions raised from
		within it."""
		try:
			tmp = self._function()
			trace = None
			exc_info = None
		except BaseException, e:
			exc_info = sys.exc_info()
			trace = traceback.format_tb( sys.exc_info()[ 2 ] )
			tmp = e
		self._lock.acquire()
		self._result = tmp
		self._trace = trace
		self._exc_info = exc_info
		self._finished = True
		self._lock.release()

	@property
	def result( self ):
		"""Contains the result of the thread function or the exception
		that occurred during thread processing"""
		return self._result

	@property
	def trace( self ):
		"""Contains a formatted traceback of the occured exception during
		thread processing. If no exception has been raised the value is None"""
		return self._trace

	@property
	def exc_info( self ):
		"""Contains information about the exception that es occured
		during the execution of the thread. The value is the some as
		returned by sys.exc_info(). If no exception has been raised the
		value is None"""
		return self._exc_info

	@property
	def name( self ):
		return self._name

	@property
	def finished( self ):
		"""If the thread is finished the property continas the value
		True else False."""
		return self._finished

	def lock( self ):
		"""Locks a thread local lock object"""
		self._lock.acquire()

	def unlock( self ):
		"""Unlocks a thread local lock object"""
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
