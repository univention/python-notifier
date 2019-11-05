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

import mock
import notifier
import notifier.signals as signals
import time
import pytest


class TestSignal(signals.Provider):
	def __init__(self):
		signals.Provider.__init__(self)
		self.signal_new('test-signal')


@pytest.fixture(scope='module')
def global_data():
	return {'test': TestSignal()}


signals.new('test-signal')


def test_signals_module():
	timer_cb = mock.Mock()
	signal_cb = mock.Mock()
	notifier.init(notifier.GENERIC)
	signals.connect(
		'test-signal', notifier.Callback(signal_cb, 1, 2, 'global signal'))
	notifier.timer_add(2000, notifier.Callback(timer_cb, 7))
	for i in range(3):
		notifier.step()
		time.sleep(1)


def test_signals_obj(global_data):
	timer_cb = mock.Mock()
	signal_cb = mock.Mock()
	notifier.init(notifier.GENERIC)
	global_data['test'].signal_connect(
		'test-signal', notifier.Callback(signal_cb, 1, 2, 'TestSignal signal'))
	notifier.timer_add(2000, notifier.Callback(timer_cb, 7))
	for i in range(3):
		notifier.step()
		time.sleep(1)


def test_unknown_signal_error():
	cb = mock.Mock()
	with pytest.raises(signals.UnknownSignalError):
		signals.connect("clicked2", cb)
