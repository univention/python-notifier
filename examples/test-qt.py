#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author: Andreas Büsching <crunchy@bitkipper.net>
#
# test programm for the QT3 and QT4 notifier
#
# $Id$
#
# Copyright (C) 2004, 2005, 2006
#	Andreas Büsching <crunchy@bitkipper.net>
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

try:
    import PyQt4.Qt as qt
    version = 4
except:
    import qt
    version = 3

import notifier

import sys

class QTestApp( qt.QApplication ):
    def __init__( self ):
        qt.QApplication.__init__( self, sys.argv )
        self.dialog = qt.QDialog()
	if version == 4:
	    self.setActiveWindow( self.dialog )
	else:
	    self.setMainWidget( self.dialog )

        self.dialog.setWindowTitle( "Qt - pyNotifier Test" )
	self.button = qt.QPushButton( 'Hello World', self.dialog )
        self.dialog.show()
	qt.QObject.connect( self.button, qt.SIGNAL( 'clicked()' ), \
				self.clickedButton )
        self.timer_id = notifier.timer_add( 4, self.timerTest )

    def recvQuit( self, mmsg, data = None ):
	if version == 4:
	    self.exit()
	else:
	    self.exit_loop()

    def clickedButton( self ):
    	print "bye"
	if version == 4:
	    self.exit()
	else:
	    self.exit_loop()

    def timerTest( self, data ):
        print 'tick'
        return False

if __name__ == '__main__':
    notifier.init( notifier.QT )
    app = QTestApp()

    # can not use notifier.loop()
    if version == 4:
	app.exec_()
    else:
	app.exec_loop()
