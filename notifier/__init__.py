"""Simple mainloop that watches _sockets and _timers."""

from select import select
from time import time

addSocket = None
removeSocket = None

addTimer = None
removeTimer = None

loop = None
step = None

# notifier types
GENERIC = 0
QT      = 1
GTK     = 2
WX      = 3

def init( type = GENERIC ):
    global addTimer
    global addSocket
    global removeTimer
    global removeSocket
    global loop, step
    if type == GENERIC:
        import generic.notifier
        addSocket = generic.notifier.addSocket
        removeSocket = generic.notifier.addSocket
        addTimer = generic.notifier.addTimer
        removeTimer = generic.notifier.addTimer
        loop = generic.notifier.loop
        step = generic.notifier.step
    elif type == QT:
        import qt.notifier
        addSocket = qt.notifier.addSocket
        removeSocket = qt.notifier.addSocket
        addTimer = qt.notifier.addTimer
        removeTimer = qt.notifier.addTimer
        loop = qt.notifier.loop
        step = qt.notifier.step
    elif type == GTK:
        import gtk.notifier
        addSocket = gtk.notifier.addSocket
        removeSocket = gtk.notifier.addSocket
        addTimer = gtk.notifier.addTimer
        removeTimer = gtk.notifier.addTimer
        loop = gtk.notifier.loop
        step = gtk.notifier.step
    elif type == WX:
        import wx.notifier
        addSocket = wx.notifier.addSocket
        removeSocket = wx.notifier.addSocket
        addTimer = wx.notifier.addTimer
        removeTimer = wx.notifier.addTimer
        loop = wx.notifier.loop
        step = wx.notifier.step
    else:
        raise Exception( 'unknown notifier type' )
        

class DeadTimerException( Exception ):
    def __init__( self ): pass
