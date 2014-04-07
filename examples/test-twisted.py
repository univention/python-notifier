#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author: Andreas Büsching <crunchy@bitkipper.net>
#
# test programm for the Twisted notifier
#
# Copyright (C) 2008
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

"""Simple test program for the Twisted notifier."""

import os
import sys

#import twisted

import notifier

notifier.init(notifier.TWISTED)


def hello(*args):
	print 'Hello World'

# notifier-timer testfunction


def timer_test():
	print "timer_test"
#	 notifier.dispatcher_add( notifier.Callback( dispatcher_test, 1, 2, 3 ) )
	return True


def dispatcher_test(a, b, c):
	print 'dispatcher', a, b, c
	return True


def _stdin(fd):
	print 'read: ' + os.read(fd, 512)
	notifier.socket_remove(0)
	return False

notifier.socket_add(0, _stdin)
notifier.timer_add(4000, notifier.Callback(timer_test))
notifier.dispatcher_add(notifier.Callback(dispatcher_test, 1, 2, 3))
notifier.loop()
