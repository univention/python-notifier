#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# test-gtk.py
#
# Author: Andreas Büsching <crunchy@bitkipper.net>
#
# test programm for the GTK+ notifier
#
# $Id$
#
# Copyright (C) 2004, 2005, 2006 Andreas Büsching <crunchy@bitkipper.net>
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

"""Simple test program for the GTK+ notifier."""

import sys

import gtk

import notifier

notifier.init( notifier.GTK )

def hello( *args ):
    print 'Hello World'

def destroy(*args):
    window.hide()
    sys.exit( 0 )

window = gtk.Window( gtk.WINDOW_TOPLEVEL )
window.connect( 'destroy', destroy )
window.set_border_width( 10 )

button = gtk.Button( 'Hello World' )
button.connect( 'clicked', hello )
window.add( button )
button.show()

window.show()

# notifier-timer testfunction
def timer_test():
    print "timer_test"
    notifier.dispatcher_add( notifier.Callback( dispatcher_test, 1, 2, 3 ) )
    return True

def dispatcher_test( a, b, c ):
    print 'dispatcher', a, b, c
    return False

notifier.timer_add( 4000, notifier.Callback( timer_test ) )
notifier.dispatcher_add( notifier.Callback( dispatcher_test, 1, 2, 3 ) )
notifier.loop()


