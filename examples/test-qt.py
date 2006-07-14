#!/usr/bin/env python

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
