#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# signal.py
#
# Author: Andreas Büsching  <crunchy@bitkipper.net>
#
# signal
#
# $Id: file.py,v 1.1 2004/09/20 12:39:43 crunchy Exp $
#
# Copyright (C) 2005 Andreas Büsching <crunchy@bitkipper.net>
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

import notifier
import notifier.signals as signals

class TestSignal( signals.Provider ):
    def __init__( self ):
        signals.Provider.__init__( self )
        self.signal_new( 'test-signal' )

test = TestSignal()

def timer_cb( a ):
    print 'timer argument', a
    signals.emit( 'test-signal' )
    test.signal_emit( 'test-signal' )
    print '-------------------------'
    return True

def signal_cb( signal, a, b ):
    print 'signal arguments', signal, a, b
    signals.disconnect( 'test-signal', signal_cb )

notifier.init( notifier.GENERIC )

signals.new( 'test-signal' )
signals.connect( 'test-signal', notifier.Callback( signal_cb, 1, 2,
                                                   'global signal' ) )
test.signal_connect( 'test-signal',notifier.Callback( signal_cb, 1, 2,
                                               'TestSignal signal' ) )
notifier.timer_add( 2000, notifier.Callback( timer_cb, 7 ) )

notifier.loop()
