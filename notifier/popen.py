#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author: Andreas Büsching <crunchy@bitkipper.net>
#
# $Id$
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

"""process control using notifier."""

__all__ = [ 'Process', 'RunIt', 'Shell' ]

# python imports
import os
import fcntl
import popen2
import glob
import re
import shlex
import logging
import types

# notifier imports
import notifier
import signals
import log

_processes = []

class Process( signals.Provider ):
	"""
	Base class for started child processes
	"""
	def __init__( self, cmd, stdout = True, stderr = True ):
		""" Init the child process 'cmd'. This can either be a string or a list
		of arguments (similar to popen2). stdout and stderr of the child
		process can be handled by connecting to the signals 'stdout'
		and/or 'stderr'. The signal functions have one argument that is
		of type list and contains all new lines. By setting one of the
		boolean arguments 'stdout' and 'stderr' to False the monitoring
		of these files can be deactivated."""

		# Setup signal handlers for the process; allows the class to be
		# useful without subclassing.

		signals.Provider.__init__( self )
		if stderr: self.signal_new( 'stderr' );
		if stdout: self.signal_new( 'stdout' );
		self.signal_new( 'killed' );

		self._cmd = self._normalize_cmd(cmd)
		if self._cmd:
			self._name = self._cmd[ 0 ].split( '/' )[ -1 ]
		else:
			self._name = '<unknown>'
		self.stopping = False
		self.pid = None
		self.child = None

		self.__dead = True
		self.__kill_timer = None

		global _processes
		if not _processes:
			notifier.dispatcher_add( _watcher )
		_processes.append( self )

	def _normalize_cmd( self, cmd ):
		"""
		Converts a command string into a list while honoring quoting or
		removes empty strings if the cmd is a list.
		"""
		if cmd == None:
			return []
		elif type( cmd ) == list:
			# Remove empty strings from argument list.
			while '' in cmd:
				cmd.remove( '' )
			return cmd

		assert( type( cmd ) in types.StringTypes )

		cmdlist = shlex.split( str( cmd ) )

		return cmdlist

	def _read_stdout( self, line ):
		self.signal_emit( 'stdout', self.pid, line )

	def _read_stderr( self, line ):
		self.signal_emit( 'stderr', self.pid, line )

	def start( self, args = None ):
		"""
		Starts the process.	 If args is not None, it can be either a list or
		string, as with the constructor, and is appended to the command line
		specified in the constructor.
		"""
		if not self.__dead:
			raise SystemError, "process is already running."
		if self.stopping:
			raise SystemError, "process is currently dying."

		cmd = self._cmd + self._normalize_cmd( args )
		self.__kill_timer = None
		self.__dead = False
		self.binary = cmd[ 0 ]

		self.stdout = self.stderr = None
		if not self.signal_exists( 'stdout' ) and \
			   not self.signal_exists( 'stderr' ):
			self.pid = os.spawnvp( os.P_NOWAIT, self.binary, cmd )
		else:
			self.child = popen2.Popen3( cmd, True, 1000 )
			self.pid = self.child.pid

			if self.signal_exists( 'stdout' ):
				# IO_Handler for stdout
				self.stdout = IO_Handler( 'stdout', self.child.fromchild,
										  self._read_stdout, self._name )
				self.stdout.signal_connect( 'closed', self._closed )

			if self.signal_exists( 'stderr' ):
				# IO_Handler for stderr
				self.stderr = IO_Handler( 'stderr', self.child.childerr,
										  self._read_stderr, self._name )
				self.stderr.signal_connect( 'closed', self._closed )

		log.info( 'running %s (pid=%s)' % ( self.binary, self.pid ) )

		return self.pid

	def dead( self, pid, status ):
		self.__dead = True
		self.signal_emit( 'killed', pid, status )

	def _closed( self, name ):
		if name == 'stderr':
			self.stderr = None
		elif name == 'stdout':
			self.stdout = None

		if not self.stdout and not self.stderr:
			try:
				pid, status = os.waitpid( self.pid, os.WNOHANG )
				if pid:
					self.dead( pid, status )
			except OSError: # already dead and buried
				pass

	def write( self, line ):
		"""
		Pass a string to the process
		"""
		try:
			self.child.tochild.write( line )
			self.child.tochild.flush()
		except ( IOError, ValueError ):
			pass

	def is_alive( self ):
		"""
		Return True if the process is still running
		"""
		return not self.__dead

	def stop( self ):
		"""
		Stop the child. Tries to kill the process with signal 15 and after that
		kill -9 will be used to kill the app.
		"""
		if self.stopping:
			return

		self.stopping = True

		if self.is_alive() and not self.__kill_timer:
			cb = Callback( self.__kill, 15 )
			self.__kill_timer = notifier.timer_add( 0, cb )

	def __kill( self, signal ):
		"""
		Internal kill helper function
		"""
		if not self.is_alive():
			self.__dead = True
			self.stopping = False
			return False
		# child needs some assistance with dying ...
		try:
			os.kill( self.pid, signal )
		except OSError:
			pass

		if signal == 15:
			cb = Callback( self.__kill, 9 )
		else:
			cb = Callback( self.__killall, 15 )

		self.__kill_timer = notifier.timer_add( 3000, cb )
		return False

	def __killall( self, signal ):
		"""
		Internal killall helper function
		"""
		if not self.is_alive():
			self.__dead = True
			self.stopping = False
			return False
		# child needs some assistance with dying ...
		try:
			# kill all applications with the string <appname> in their
			# commandline. This implementation uses the /proc filesystem,
			# it is Linux-dependent.
			unify_name = re.compile( '[^A-Za-z0-9]' ).sub
			appname = unify_name( '', self.binary )

			cmdline_filenames = glob.glob( '/proc/[0-9]*/cmdline' )

			for cmdline_filename in cmdline_filenames:
				try:
					fd = open( cmdline_filename )
					cmdline = fd.read()
					fd.close()
				except IOError:
					continue
				if unify_name( '', cmdline ).find( appname ) != -1:
					# Found one, kill it
					pid = int( cmdline_filename.split( '/' )[ 2 ] )
					try:
						os.kill( pid, signal )
					except:
						pass
		except OSError:
			pass

		log.info( 'kill -%d %s' % ( signal, self.binary ) )
		if signal == 15:
			cb = Callback( self.__killall, 9 )
			self.__kill_timer = notifier.timer_add( 2000, cb )
		else:
			log.critical( 'PANIC %s' % self.binary )

		return False

def _watcher():
	global _processes
	finished = []

	for proc in _processes:
		try:
			pid, status = os.waitpid( proc.pid, os.WNOHANG )
			if pid:
				proc.dead( pid, status )
				finished.append( proc )
		except OSError: # already dead and buried
			finished.append( proc )

	for i in finished:
		_processes.remove( i )

	return ( len( _processes ) > 0 )

class IO_Handler( signals.Provider ):
	"""
	Reading data from socket (stdout or stderr)
	"""
	def __init__( self, name, fp, callback, logger = None ):
		signals.Provider.__init__( self )

		self.name = name
		self.fp = fp
		fcntl.fcntl( self.fp.fileno(), fcntl.F_SETFL, os.O_NONBLOCK )
		self.callback = callback
		self.saved = ''
		notifier.socket_add( fp, self._handle_input )
		self.signal_new( 'closed' )

	def close( self ):
		"""
		Close the IO to the child.
		"""
		notifier.socket_remove( self.fp )
		self.fp.close()
		self.signal_emit( 'closed', self.name )

	def _handle_input( self, socket ):
		"""
		Handle data input from socket.
		"""
		try:
			self.fp.flush()
			data = self.fp.read( 10000 )
		except IOError, (errno, msg):
			if errno == 11:
				# Resource temporarily unavailable; if we try to read on a
				# non-blocking descriptor we'll get this message.
				return True
			data = None

		if not data:
			self.close()
			return False

		data  = data.replace('\r', '\n')
		lines = data.split('\n')
		# Only one partial line?
		if len(lines) == 1:
			self.saved += data
			return True

		# Combine saved data and first line, send to app
		self.callback( self.saved + lines[ 0 ] )
		self.saved = ''

		# There's one or more lines + possibly a partial line
		if lines[ -1 ] != '':
			# The last line is partial, save it for the next time
			self.saved = lines[ -1 ]

			# Send all lines except the last partial line to the app
			self.callback( lines[ 1 : -1 ] )
		else:
			# Send all lines to the app
			self.callback( lines[ 1 : ] )

		return True

class RunIt( Process ):
	def __init__( self, command, stdout = True, stderr = False ):
		Process.__init__( self, command, stdout = stdout, stderr = stderr )
		if stdout:
			self.__stdout = []
			cb = notifier.Callback( self._output, self.__stdout )
			self.signal_connect( 'stdout', cb )
		else:
			self.__stdout = None
		if stderr:
			self.__stderr = []
			cb = notifier.Callback( self._output, self.__stderr )
			self.signal_connect( 'stderr', self._stderr )
		else:
			self.__stderr = None
		self.signal_connect( 'killed', self._finished )
		self.signal_new( 'finished' )

	def _output( self, pid, line, buffer ):
		if isinstance( line, list ):
			buffer.extend( line )
		else:
			buffer.append( line )

	def _finished( self, pid, status ):
		if self.__stdout != None:
			if self.__stderr == None:
				self.signal_emit( 'finished', pid, os.WEXITSTATUS( status ),
								  self.__stdout )
			else:
				self.signal_emit( 'finished', pid, os.WEXITSTATUS( status ),
								  self.__stdout, self.__stderr )
		else:
			self.signal_emit( 'finished', pid, os.WEXITSTATUS( status ) )

class Shell( RunIt ):
	BINARY = '/bin/sh'
	def __init__( self, command, stdout = True, stderr = False ):
		cmd = [ Shell.BINARY, '-c' ]
		if type( command ) in types.StringTypes:
			cmd.append( command )
		elif type( command ) in ( types.ListType, types.TupleType ):
			cmd.append( ' '.join( command ) )
		RunIt.__init__( self, cmd, stdout = stdout, stderr = stderr )
