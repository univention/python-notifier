#!/usr/bin/env python

import qt
import mbusif
import mbustypes

import sys

class QTestApp( qt.QApplication ):
    def __init__( self ):
        qt.QApplication.__init__( self, sys.argv )
        self.dialog = qt.QDialog()
        self.setMainWidget( self.dialog )
        self.dialog.setCaption( "Qt - Mbus Test" )
	self.button = qt.QPushButton( 'Hello World', self.dialog )
        self.dialog.show()
	qt.QObject.connect( self.button, qt.SIGNAL( 'clicked()' ), \
				self.clickedButton )
        self.mbus = mbusif.MbusIF( "app:test lang:python" )
        self.mbus.addCallback( "print", self.recvPrint )
        self.mbus.addCallback( "quit", self.recvQuit )
        self.timer_id = self.mbus.addTimer( 4, self.timerTest )

    def recvPrint( self, mmsg, data = None ):
        print "received print command, args =", mmsg.payload[0].args
        return 1 # keep command registered

    def recvQuit( self, mmsg, data = None ):
        self.exit_loop()
        
    def clickedButton( self ):
    	print "bye"
	self.exit_loop()

    def timerTest( self, data ):
        print 'tick'
        
if __name__ == '__main__':
    app = QTestApp()
    app.exec_loop()


