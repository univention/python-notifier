"""Simple mainloop that watches sockets and timers."""

#from select import select
#from time import time
import qt

__qt_socketIDs = {} # map of Sockets/Methods -> qt.QSocketNotifier

class Socket( qt.QSocketNotifier ):
    def __init__( self, socket, method ):
        qt.QSocketNotifier.__init__( self, socket.fileno(), \
                                     qt.QSocketNotifier.Read )
        self.method = method
        self.socket = socket
        qt.QObject.connect( self, qt.SIGNAL('activated(int)'), self.slotRead )
        
    def slotRead( self ):
        global __qt_socketIDs
        self.method( self.socket )
	self.setEnabled( 0 )
	del __qt_socketIDs[ socket ]

class Timer( qt.QTimer ):
    def __init__( self, ms, method, args ):
        qt.QTimer.__init__( self )
        self.method = method
        self.args = args
        self.start( ms )
        qt.QObject.connect( self, qt.SIGNAL('timeout()'), self.slotTick )

    def slotTick( self ):
        try:
            if not self.method( self.args ):
                self.stop()
                del self
        except:
            self.stop()
            del self
            
def addSocket( socket, method ):
    """The first argument specifies a socket, the second argument has to be a
    function that is called whenever there is data ready in the socket."""
    global __qt_socketIDs
    __qt_socketIDs[ socket ] = Socket( socket, method )

def removeSocket( socket ):
    """Removes the given socket from scheduler."""
    global __qt_socketIDs
    if __qt_socketIDs.has_key( socket ):
	__qt_socketIDs[ socket ].setEnabled( 0 )
	del __qt_socketIDs[ socket ]

def addTimer( interval, method, data = None ):
    """The first argument specifies an interval in milliseconds, the
    second argument a function. This is function is called after
    interval milliseconds. If it returns true it's called again after
    interval milliseconds, otherwise it is removed from the
    scheduler. The third (optional) argument is a parameter given to
    the called function."""
    return Timer( interval, method, data )

def removeTimer( id ):
    """Removes _all_ functioncalls to the method given as argument from the
    scheduler."""
    if isinstance( id, Timer ):
        id.stop()
        del id

addDispatcher = None
removeDispatcher = None

def loop():
    """Execute main loop forever."""
    raise Error, "Not supported with Qt notifier. Use the run method of your QApplication object"

def step():
    raise Error, "stepping not supported in qt-Mode"
