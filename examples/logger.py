#!/usr/bin/env python
#-*- coding: utf-8 -*-
#
# logger.py
# 
# Author: Andreas Büsching <crunchy@tzi.de>
# 
# logger
# 
# $Id$
# 
# Copyright (C) 2004 Andreas Büsching <crunchy@tzi.de>
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

import os

import notifier

def tail_minus_f( logfile ):
    new_size = os.stat( logfile.name )[ 6 ]
    if new_size > logfile.tell():
        buffer = logfile.read( 65536 )
        if buffer: print buffer,

    return True

if __name__ == '__main__':
    notifier.init()
    log = open( '/var/log/messages', 'rb' )
    log.seek( os.stat( '/var/log/messages' )[ 6 ] )
    notifier.addTimer( 100, notifier.Callback( tail_minus_f, log ) )
    notifier.loop()
