#!/usr/bin/env python
# -*- coding: utf-8 -*-

import notifier


def foo():
	pass


def bar():
	pass


def test_callback_equality():
	callbacks = [notifier.Callback(foo), notifier.Callback(bar, 1, 2, 3)]
	assert notifier.Callback(foo) in callbacks
	assert foo in callbacks
	callbacks.remove(notifier.Callback(foo, 3, 2, 1))
	callbacks.remove(bar)
	assert not callbacks
