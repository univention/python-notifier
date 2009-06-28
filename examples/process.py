#!/usr/bin/env python
#-*- coding: utf-8 -*-
#
# Author: Andreas Büsching <crunchy@bitkipper.net>
#
# an example demonstrating the process handler class
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
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
# 02110-1301 USA

import os, sys

import notifier
import notifier.popen

proc = None

def stdout( pid, line ):
	if not type( line ) in ( list, tuple ):
		line = [ line ]
	for l in line:
		print "(%d>1): %s" % ( pid, l )

def stderr( pid, line ):
	if not type( line ) in ( list, tuple ):
		line = [ line ]
	for l in line:
		print "(%d>2): %s" % ( pid, l )

def died( pid, status ):
	print ">>> process %d died" % pid
	# sys.exit( status )

def tick():
	print 'tick'
	return True

def runit():
	global proc
	print 'runit ...',
	proc = notifier.popen.Process( '/bin/sleep 5' )
	proc = notifier.popen.Process( '/bin/ls -ltr' )
	proc.signal_connect( 'stdout', stdout )
	proc.signal_connect( 'stderr', stderr )
	proc.signal_connect( 'killed', died )
	proc.start()
	while True:
		if proc.is_alive():
			notifier.step()
		else:
			break

if __name__ == '__main__':
	notifier.init( notifier.GENERIC )

	# run a process and wait for its death
	notifier.timer_add( 500, runit )

	# show we can still do things
	notifier.timer_add( 100, tick )

	proc = notifier.popen.Process( '/bin/ls -latr /etc' )
	proc.signal_connect( 'stdout', stdout )
	proc.signal_connect( 'stderr', stderr )
	proc.signal_connect( 'killed', died )
	proc.start()

	notifier.loop()
