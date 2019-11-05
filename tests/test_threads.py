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
import notifier.threads as threads


def test_threads():

	my_thread = mock.Mock()
	done_with_it = mock.Mock()
	doing_something_else = mock.Mock()

	notifier.init(notifier.GENERIC)

	# task = threads.Simple( 'test',
	# 					   notifier.Callback( my_thread, [ 'hello', 'world' ] ),
	# 					   done_with_it )
	task = threads.Simple('test',
							notifier.Callback(my_thread, ['hello', 'world']),
							notifier.Callback(done_with_it, 'another argument'))
	task.run()
	notifier.timer_add(1000, doing_something_else)
	notifier.step()
