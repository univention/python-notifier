"""Simple mainloop that watches _sockets and _timers."""

from version import *

from select import select
from time import time

addSocket = None
removeSocket = None

addTimer = None
removeTimer = None

addDispatcher = None
removeDispatcher = None

loop = None
step = None

# notifier types
GENERIC = 0
QT      = 1
GTK     = 2
WX      = 3

# socket conditions
IO_READ = None
IO_WRITE = None
IO_EXCEPT = None

def init( type = GENERIC ):
    global addTimer
    global addSocket
    global addDispatcher
    global removeTimer
    global removeSocket
    global removeDispatcher
    global loop, step
    global IO_READ, IO_WRITE, IO_EXCEPT
    
    if type == GENERIC:
        import nf_generic as nf_impl
    elif type == QT:
        import nf_qt as nf_impl
    elif type == GTK:
        import nf_gtk as nf_impl
    elif type == WX:
        import nf_wx as nf_impl
    else:
        raise Exception( 'unknown notifier type' )
        
    addSocket = nf_impl.addSocket
    removeSocket = nf_impl.removeSocket
    addTimer = nf_impl.addTimer
    removeTimer = nf_impl.removeTimer
    addDispatcher = nf_impl.addDispatcher
    removeDispatcher = nf_impl.removeDispatcher
    loop = nf_impl.loop
    step = nf_impl.step
    IO_READ = nf_impl.IO_READ
    IO_WRITE = nf_impl.IO_WRITE
    IO_EXCEPT = nf_impl.IO_EXCEPT

class Callback:
    def __init__( self, function, *args ):
        self._function = function
        self._args = args

    def __call__( self, *args ):
        tmp = list( self._args )
        if args:
            tmp.extend( args )
        if tmp:
            return self._function( *tmp )
        else:
            return self._function()

    def __nonzero__( self ):
        return bool( self._function )
