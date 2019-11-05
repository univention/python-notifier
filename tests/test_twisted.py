# -*- coding: utf-8 -*-
#
# Author: Andreas Büsching <crunchy@bitkipper.net>
#
# test programm for the Twisted notifier
#
# Copyright (C) 2008
#       Andreas Büsching <crunchy@bitkipper.net>
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


"""Simple test program for the Twisted notifier."""
import mock
import os
import sys
import time
import pytest

import notifier
import tempfile
#import twisted


_stdout = tempfile.TemporaryFile()

# notifier-timer testfunction

def test_twisted():

	notifier.init(notifier.TWISTED)

	def _stdin(fd):
		print('read: ')
		print(os.read(fd, 512))
		notifier.socket_remove(0)
		return False

	timer_test = mock.Mock()
	timer_test.return_value = True
	timer_once = mock.Mock()
	timer_once.return_value = False
	dispatcher_test = mock.Mock()
	dispatcher_test.return_value = True

	#notifier.socket_add(0, _stdin)

	notifier.timer_add(140, notifier.Callback(timer_once))
	notifier.timer_add(1000, notifier.Callback(timer_test))
	notifier.dispatcher_add(notifier.Callback(dispatcher_test, 1, 2, 3))

	for i in range(3):
		notifier.step()
		time.sleep(1)

	timer_once.assert_called()
	assert timer_once.call_count == 1
	timer_test.assert_called()
	assert timer_test.call_count == 2
	dispatcher_test.assert_called_with(1, 2, 3)
	assert dispatcher_test.call_count >= 3
