#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author: Andreas Büsching <crunchy@bitkipper.net>
#
# package initialisation
#
# Copyright (C) 2004, 2005, 2006
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

"""Simple mainloop that watches sockets and timers."""
from __future__ import absolute_import

from .version import VERSION  # noqa: F401
from . import log  # noqa: F401

socket_add = None
socket_remove = None

timer_add = None
timer_remove = None

dispatcher_add = None
dispatcher_remove = None

loop = None
step = None

# notifier types
(GENERIC, QT, GTK, TWISTED, TORNADO) = range(5)

# socket conditions
IO_READ = None
IO_WRITE = None
IO_EXCEPT = None


def init(model=GENERIC, **kwargs):
	global timer_add
	global socket_add
	global dispatcher_add
	global timer_remove
	global socket_remove
	global dispatcher_remove
	global loop, step
	global IO_READ, IO_WRITE, IO_EXCEPT

	if model == GENERIC:
		from . import nf_generic as nf_impl
	elif model == QT:
		from . import nf_qt as nf_impl
	elif model == GTK:
		from . import nf_gtk as nf_impl
	elif model == TWISTED:
		from . import nf_twisted as nf_impl
	elif model == TORNADO:
		from . import nf_tornado as nf_impl
	else:
		raise Exception('unknown notifier model')

	socket_add = nf_impl.socket_add
	socket_remove = nf_impl.socket_remove
	timer_add = nf_impl.timer_add
	timer_remove = nf_impl.timer_remove
	dispatcher_add = nf_impl.dispatcher_add
	dispatcher_remove = nf_impl.dispatcher_remove
	loop = nf_impl.loop
	step = nf_impl.step
	IO_READ = nf_impl.IO_READ
	IO_WRITE = nf_impl.IO_WRITE
	IO_EXCEPT = nf_impl.IO_EXCEPT

	if hasattr(nf_impl, '_options') and type(nf_impl._options) == dict:
		for k, v in kwargs.items():
			if k in nf_impl._options:
				nf_impl._options[k] = v

	if hasattr(nf_impl, '_init'):
		nf_impl._init()


class Callback(object):

	def __init__(self, function, *args, **kwargs):
		self._function = function
		self._args = args
		self._kwargs = kwargs

	def __call__(self, *args):
		tmp = list(args)
		if self._args:
			tmp.extend(self._args)
		return self._function(*tmp, **self._kwargs)

	def __lt__(self, other):
		return self._function < (other._function if isinstance(other, Callback) else other) if callable(other) else NotImplemented

	def __le__(self, other):
		return self._function <= (other._function if isinstance(other, Callback) else other) if callable(other) else NotImplemented

	def __eq__(self, other):
		return self._function == (other._function if isinstance(other, Callback) else other) if callable(other) else NotImplemented

	def __ne__(self, other):
		return self._function != (other._function if isinstance(other, Callback) else other) if callable(other) else NotImplemented

	def __ge__(self, other):
		return self._function >= (other._function if isinstance(other, Callback) else other) if callable(other) else NotImplemented

	def __gt__(self, other):
		return self._function > (other._function if isinstance(other, Callback) else other) if callable(other) else NotImplemented

	def __bool__(self):
		return bool(self._function)
	__nonzero__ = __bool__

	def __hash__(self):
		return hash(self._function)
