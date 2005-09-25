#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# callbacks.py
#
# Author: Andreas Büsching  <crunchy@bitkipper.net>
#
# callbacks
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


notifier.init( notifier.GENERIC )

def cb( bla, fasel, fasel2 ):
    print bla
    print fasel
    print fasel2

b = notifier.Callback( cb )
c = notifier.Callback( cb, 'addional user data', 'more additional user data' )
c( 'mandatory arguments' )

print 'b == c', b == c
print 'b == cb', b == cb
