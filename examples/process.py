#!/usr/bin/env python
#-*- coding: utf-8 -*-
#
# process.py
#
# Author: Andreas Büsching <crunchy@bitkipper.net>
#
# en example demonstrating the process handler class
#
# $Id$
#
# Copyright (C) 2006 Andreas Büsching <crunchy@bitkipper.net>
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

import os, sys

import notifier
import notifier.popen

def stdout( pid, line ):
    print "(%d>1): %s" % ( pid, line )

def stderr( pid, line ):
    print "(%d>2): %s" % ( pid, line )

def died( pid, status ):
    print ">>> process %d died" % pid
    sys.exit( os.WEXITSTATUS( status[ 1 ] ) )

if __name__ == '__main__':
    notifier.init( notifier.GENERIC )
    proc = notifier.popen.Process( '/bin/ls -latr /etc' )
#     proc = notifier.popen.Process( '/bin/ls -latr /var/log/exim4' )

    proc.signal_connect( 'stdout', stdout )
    proc.signal_connect( 'stderr', stderr )
    proc.signal_connect( 'killed', died )

    proc.start()
    notifier.loop()
