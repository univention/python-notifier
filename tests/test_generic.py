#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author: Andreas Büsching  <crunchy@bitkipper.net>
#
# test programm for generic notifier implementation
#
# Copyright (C) 2004, 2005, 2006, 2007
#		Andreas Büsching <crunchy@bitkipper.net>
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

import socket
import subprocess
import sys
import time

import mock
import pytest

import notifier


def test_dispatch():
	dispatch = mock.Mock()
	# when no argument is given to init default is GENERIC
	notifier.init(notifier.GENERIC, recursive_depth=5)
	#notifier.timer_add( 0, notifier.Callback( zero, 'hello' ) )
	notifier.dispatcher_add(notifier.Callback(dispatch, 'hello'))
	#notifier.dispatcher_add( notifier.Callback( dispatch, 'hello' ), False )

	notifier.step()
	time.sleep(1)
	notifier.step()

	# test that func was called with the correct arguments
	dispatch.assert_called_with('hello')

	notifier.dispatcher_remove(dispatch)


def test_generic_with_timeout_and_dispatch():
	timeout = mock.Mock()

	dispatch = mock.Mock()
	# when no argument is given to init default is GENERIC
	notifier.init(notifier.GENERIC, recursive_depth=5)
	notifier.timer_add(1000, notifier.Callback(timeout, 'hello'))
	#notifier.timer_add( 0, notifier.Callback( zero, 'hello' ) )
	notifier.dispatcher_add(notifier.Callback(dispatch, 'hello'))
	#notifier.dispatcher_add( notifier.Callback( dispatch, 'hello' ), False )

	notifier.step()
	time.sleep(1)
	notifier.step()

	# test that func was called with the correct arguments
	timeout.assert_called_with('hello')
	dispatch.assert_called_with('hello')


class Stop(Exception):
	pass


@pytest.mark.parametrize('timeout', [1000, 500, 100])
def test_timer(timeout):
	result = [(timeout * i) / 1000.0 for i in range(1, 6)]
	points = []

	def timer():
		points.append(time.time() * 1000)
		if len(points) > 5:
			raise Stop()
		return True

	notifier.init(notifier.GENERIC)
	t = notifier.timer_add(timeout, timer)
	with pytest.raises(Stop):
		notifier.loop()
	notifier.timer_remove(t)
	start = points.pop(0)
	points = [round(int(p - start) / 1000.0, 2) for p in points]
	assert points == result


def test_adding_closed_socket():
	notifier.init(notifier.GENERIC, recursive_depth=5)
	s = socket.socket()
	s.close()
	with pytest.raises(AttributeError) as exc:
		notifier.socket_add(s, lambda x: None)
	assert 'could not get file description' in str(exc.value)


def test_adding_broken_socket():
	notifier.init(notifier.GENERIC, recursive_depth=5)
	with pytest.raises(AttributeError) as exc:
		notifier.socket_add(None, lambda x: None)
	assert 'could not get file description' in str(exc.value)


def test_removing_closed_socket():
	notifier.init(notifier.GENERIC, recursive_depth=5)
	s = socket.socket()
	notifier.socket_add(s.fileno(), lambda x: None)
	s.close()
	notifier.socket_remove(s)


def test_socket_remove_in_timer():
	notifier.init()

	fd = None

	def on_timer():
		notifier.socket_remove(fd)
		return False

	p = subprocess.Popen([sys.executable, '-c', 'import sys; sys.stdin.read()'], stdin=subprocess.PIPE)
	fd = p.stdin.fileno()
	notifier.socket_add(fd, lambda sock: True)
	notifier.timer_add(0, on_timer)
	p.communicate(b'A')
	notifier.step()
