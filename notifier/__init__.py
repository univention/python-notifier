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
IO_IN = None
IO_OUT = None

def init( type = GENERIC ):
    global addTimer
    global addSocket
    global addDispatcher
    global removeTimer
    global removeSocket
    global removeDispatcher
    global loop, step
    global IO_IN, IO_OUT
    
    if type == GENERIC:
        import nf_generic
        addSocket = nf_generic.addSocket
        removeSocket = nf_generic.removeSocket
        addTimer = nf_generic.addTimer
        removeTimer = nf_generic.removeTimer
        addDispatcher = nf_generic.addDispatcher
        removeDispatcher = nf_generic.removeDispatcher
        loop = nf_generic.loop
        step = nf_generic.step
        IO_OUT = nf_generic.IO_OUT
        IO_IN = nf_generic.IO_IN
    elif type == QT:
        import nf_qt
        addSocket = nf_qt.addSocket
        removeSocket = nf_qt.removeSocket
        addTimer = nf_qt.addTimer
        removeTimer = nf_qt.removeTimer
        loop = nf_qt.loop
        step = nf_qt.step
    elif type == GTK:
        import nf_gtk
        addSocket = nf_gtk.addSocket
        removeSocket = nf_gtk.removeSocket
        addTimer = nf_gtk.addTimer
        removeTimer = nf_gtk.removeTimer
        loop = nf_gtk.loop
        step = nf_gtk.step
        IO_OUT = nf_gtk.IO_OUT
        IO_IN = nf_gtk.IO_IN
    elif type == WX:
        import nf_wx
        addSocket = nf_wx.addSocket
        removeSocket = nf_wx.removeSocket
        addTimer = nf_wx.addTimer
        removeTimer = nf_wx.removeTimer
        loop = nf_wx.loop
        step = nf_wx.step
    else:
        raise Exception( 'unknown notifier type' )
        

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


class DeadTimerException( Exception ):
    def __init__( self ): pass
