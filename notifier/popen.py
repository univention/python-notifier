#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# popen.py
#
# Author: Andreas Büsching <crunchy@bitkipper.net>
#
# $Id$
#
# Copyright (C) 2004, 2005, 2006
#	Andreas Büsching <crunchy@bitkipper.net>
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

"""process control using notifier."""

__all__ = [ 'Process' ]

# python imports
import os
import fcntl
import popen2
import glob
import re
import logging

# notifier imports
import notifier
import signals
import log

class Process( signals.Provider ):
    """
    Base class for started child processes
    """
    def __init__( self, cmd ):
        """ Init the child process 'cmd'. This can either be a string or a list
        of arguments (similar to popen2). stdout and stderr can be
        handled by a subclass by overriding the member functions
        read_stdout and/or read_stderr or by connecting to the signals
        'stdout' and/or 'stderr'. The signal functions have one argument
        that is of type list and contains all new lines """

        # Setup signal handlers for the process; allows the class to be
        # useful without subclassing.

	signals.Provider.__init__( self )
	self.signal_new( 'stderr' );
	self.signal_new( 'stdout' );
	self.signal_new( 'killed' );

	self.read_stdout = None
	self.read_stderr = None

        self._cmd = self._normalize_cmd(cmd)
        self._stop_cmd = None
	if self._cmd:
	    self._name = self._cmd[ 0 ].split( '/' )[ -1 ]
	else:
	    self._name = '<unknown>'
        self.__dead = True
        self.stopping = False
        self.__kill_timer = None

    def _normalize_cmd( self, cmd ):
        """
        Converts a command string into a list while honoring quoting, or
        removes empty strings if the cmd is a list.
        """
        if cmd == None:
            return []
        elif type( cmd ) == list:
            # Remove empty strings from argument list.
            while '' in cmd:
                cmd.remove( '' )
            return cmd

        assert( type( cmd ) == str )

        # This might be how you'd do it in C. :)
        cmdlist = []
        curarg = ''
        waiting = None
        last = None
        for c in cmd:
            if ( c == ' ' and not waiting ) or c == waiting:
                if curarg:
                    cmdlist.append( curarg )
                    curarg = ''
                waiting = None
            elif c in ("'", '"') and not waiting and last != '\\':
                waiting = c
            else:
                curarg += c
            last = c

        if curarg:
            cmdlist.append( curarg )

        return cmdlist

    def _read_stdout( self, line ):
	if self.read_stdout:
	    self.read_stdout( self.child.pid, line )
	else:
	    self.signal_emit( 'stdout', self.child.pid, line )

    def _read_stderr( self, line ):
	if self.read_stderr:
	    self.read_stderr( self.child.pid, line )
	else:
	    self.signal_emit( 'stderr', self.child.pid, line )

    def start( self, args = None ):
        """
        Starts the process.  If args is not None, it can be either a list or
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

        self.child = popen2.Popen3( cmd, True, 100 )

        log.info( 'running %s (pid=%s)' % ( self.binary, self.child.pid ) )

        # IO_Handler for stdout
        self.stdout = IO_Handler( 'stdout', self.child.fromchild,
                                  self._read_stdout, self._name )
        # IO_Handler for stderr
        self.stderr = IO_Handler( 'stderr', self.child.childerr,
                                  self._read_stderr, self._name )

	self.stdout.signal_connect( 'closed', self._closed )
	self.stderr.signal_connect( 'closed', self._closed )

    def _closed( self, name ):
	if name == 'stderr':
	    self.stderr = None
	elif name == 'stdout':
	    self.stdout = None

	if not self.stdout and not self.stderr:
	    status = os.waitpid( self.child.pid, os.WNOHANG )
	    self.signal_emit( 'killed', self.child.pid, status )

    def write( self, line ):
        """
        Write a string to the app.
        """
        try:
            self.child.tochild.write(line)
            self.child.tochild.flush()
        except (IOError, ValueError):
            pass


    def is_alive( self ):
        """
        Return True if the app is still running
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
            os.kill( self.child.pid, signal )
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
            unify_name = re.compile('[^A-Za-z0-9]').sub
            appname = unify_name('', self.binary)

            cmdline_filenames = glob.glob('/proc/[0-9]*/cmdline')

            for cmdline_filename in cmdline_filenames:
                try:
                    fd = open(cmdline_filename)
                    cmdline = fd.read()
                    fd.close()
                except IOError:
                    continue
                if unify_name('', cmdline).find(appname) != -1:
                    # Found one, kill it
                    pid = int(cmdline_filename.split('/')[2])
                    try:
                        os.kill(pid, signal)
                    except:
                        pass
        except OSError:
            pass

        log.info('kill -%d %s' % ( signal, self.binary ))
        if signal == 15:
            cb = Callback( self.__killall, 9 )
            self.__kill_timer = notifier.timer_add( 2000, cb )
        else:
            log.critical('PANIC %s' % self.binary)

        return False


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
        self.logger = None
        self.saved = ''
        notifier.socket_add( fp, self._handle_input )
	self.signal_new( 'closed' )

        if logger:
            logger = '%s-%s.log' % ( logger, name )
            try:
                try:
                    os.unlink(logger)
                except:
                    pass
                self.logger = open(logger, 'w')
                log.info('logging child to "%s"' % logger)
            except IOError:
                log.warn('Error: Cannot open "%s" for logging' % logger)


    def close( self ):
        """
        Close the IO to the child.
        """
        notifier.socket_remove( self.fp )
        self.fp.close()
        if self.logger:
            self.logger.close()
            self.logger = None
	self.signal_emit( 'closed', self.name )

    def _handle_input( self, socket ):
        """
        Handle data input from socket.
        """
        try:
            data = self.fp.read( 10000 )
        except IOError, (errno, msg):
            if errno == 11:
                # Resource temporarily unavailable; if we try to read on a
                # non-blocking descriptor we'll get this message.
                return True
            data = None

        if not data:
            log.info('No data on %s for pid %s.' % ( self.name, os.getpid()))
	    self.close()
            return False

        data  = data.replace('\r', '\n')
        lines = data.split('\n')

        # Only one partial line?
        if len(lines) == 1:
            self.saved += data
            return True

        # Combine saved data and first line, send to app
        if self.logger:
            self.logger.write( self.saved + lines[ 0 ] + '\n' )
        self.callback( self.saved + lines[ 0 ] )
        self.saved = ''

        # There's one or more lines + possibly a partial line
        if lines[ -1 ] != '':
            # The last line is partial, save it for the next time
            self.saved = lines[ -1 ]

            # Send all lines except the last partial line to the app
            for line in lines[ 1 : -1 ]:
                if not line:
                    continue
                if self.logger:
                    self.logger.write( line + '\n' )
                self.callback( line )
        else:
            # Send all lines to the app
            for line in lines[ 1 : ]:
                if not line:
                    continue
                if self.logger:
                    self.logger.write( line + '\n' )

		self.callback( line )

        return True
