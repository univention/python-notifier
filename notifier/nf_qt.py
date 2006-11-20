#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author: Andreas Büsching <crunchy@bitkipper.net>
#
# QT notifier wrapper
#
# Copyright (C) 2004, 2005, 2006
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

"""notifier wrapper for QT"""

#from select import select
#from time import time
try:
	import PyQt4.Qt as qt
except:
	import qt

_qt_socketIDs = {} # map of Sockets/Methods -> qt.QSocketNotifier

IO_READ = qt.QSocketNotifier.Read
IO_WRITE = qt.QSocketNotifier.Write
IO_EXCEPT = qt.QSocketNotifier.Exception

class Socket( qt.QSocketNotifier ):
	def __init__( self, socket, method ):
		qt.QSocketNotifier.__init__( self, socket.fileno(), \
									 qt.QSocketNotifier.Read )
		self.method = method
		self.socket = socket
		qt.QObject.connect( self, qt.SIGNAL( 'activated(int)' ), self.slotRead )

	def slotRead( self ):
		if not self.method( self.socket ):
			self.setEnabled( 0 )
			removeSocket( self.socket )

class Timer( qt.QTimer ):
	def __init__( self, ms, method, args ):
		qt.QTimer.__init__( self )
		self.method = method
		self.args = args
		self.start( ms )
		qt.QObject.connect( self, qt.SIGNAL( 'timeout()' ), self.slotTick )

	def slotTick( self ):
		if not self.method( self.args ):
			self.stop()
			del self

def socket_add( socket, method ):
	"""The first argument specifies a socket, the second argument has to be a
	function that is called whenever there is data ready in the socket."""
	global _qt_socketIDs
	_qt_socketIDs[ socket ] = Socket( socket, method )

def socket_remove( socket ):
	"""Removes the given socket from scheduler."""
	global _qt_socketIDs
	if _qt_socketIDs.has_key( socket ):
		_qt_socketIDs[ socket ].setEnabled( 0 )
		del _qt_socketIDs[ socket ]

def timer_add( interval, method, data = None ):
	"""The first argument specifies an interval in milliseconds, the
	second argument a function. This is function is called after
	interval milliseconds. If it returns true it's called again after
	interval milliseconds, otherwise it is removed from the
	scheduler. The third (optional) argument is a parameter given to
	the called function."""
	return Timer( interval, method, data )

def timer_remove( id ):
	"""Removes _all_ functioncalls to the method given as argument from the
	scheduler."""
	if isinstance( id, Timer ):
		id.stop()
		del id

dispatcher_add = None
dispatcher_remove = None

def loop():
	"""Execute main loop forever."""
	raise Error, "Not supported with Qt notifier. Use the run method of your QApplication object"

def step():
	raise Error, "stepping not supported in qt-Mode"
