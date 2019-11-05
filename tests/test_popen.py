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

import time

import notifier
import notifier.popen


def test_generic():
	cb_results = {}

	def find_result(pid, status, result):
		cb_results['pid'] = pid
		cb_results['status'] = status
		cb_results['result'] = result

	notifier.init(notifier.GENERIC)
	# find_result = mock.Mock()

	cmd = '/bin/sh -c "/bin/sleep 2 && /usr/bin/find /usr/bin"'
	# cmd = '/usr/bin/find /var/log'
	proc = notifier.popen.RunIt(cmd, stdout=True)
	proc.signal_connect('finished', find_result)
	pid = proc.start()
	assert(pid > 0)
	for _i in range(3):
		notifier.step()
		time.sleep(1)
	assert(cb_results['pid'] == pid)
	assert(cb_results['status'] == 0)
	assert(len(cb_results['result']) >= 10)
