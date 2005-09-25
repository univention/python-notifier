#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# signal.py
#
# Author: Andreas Büsching  <crunchy@tzi.de>
#
# signal
#
# $Id: file.py,v 1.1 2004/09/20 12:39:43 crunchy Exp $
#
# Copyright (C) 2005 Andreas Büsching <crunchy@tzi.de>
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

def _wait_for_click( signal ):
  print "clicked"

def _wait_for_movement( signal, optional ):
  if signal == "moved":
    print "signal moved"
  else:
    print "not what I'm looking for", signal

def _emitting():
  signals.emit( "clicked" )

notifier.init( notifier.GENERIC )

signals.new( "clicked" )
signals.connect( "clicked", _wait_for_click )
signals.connect( "clicked", notifier.Callback( _wait_for_movement, 'optional something' ) )
notifier.addTimer( 3000, _emitting )

notifier.loop()
