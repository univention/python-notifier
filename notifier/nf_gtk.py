"""Simple mainloop that watches sockets and timers."""

import gobject
import gtk

import popen2

gtk_socketIDs = {} # map of Sockets/Methods -> gtk_input_handler_id

def addSocket( socket, method ):
    """The first argument specifies a socket, the second argument has to be a
    function that is called whenever there is data ready in the socket."""
    global gtk_socketIDs
    source = gobject.io_add_watch( socket, gobject.IO_IN,
                                   __socketCallback, method )
    gtk_socketIDs[ socket ] = source

def __socketCallback( source, condition, method ):
    global gtk_socketIDs
    if gtk_socketIDs.has_key( source ):
        return method( source )

    print 'socket not found'
    return False

def removeSocket( socket ):
    """Removes the given socket from scheduler."""
    global gtk_socketIDs
    if gtk_socketIDs.has_key( socket ):
	gobject.source_remove( gtk_socketIDs[ socket ] )
	del gtk_socketIDs[ socket ]

def addTimer( interval, method ):
    """The first argument specifies an interval in milliseconds, the
    second argument a function. This is function is called after
    interval seconds. If it returns true it's called again after
    interval seconds, otherwise it is removed from the scheduler. The
    third (optional) argument is a parameter given to the called
    function."""
    return gobject.timeout_add( interval, method )

def removeTimer( id ):
    """Removes _all_ functioncalls to the method given as argument from the
    scheduler."""
    gobject.source_remove( id )

def step():
    gtk.main_iteration_do()

def loop():
    """Execute main loop forver."""
    while 1:
        step()
        

class DeadTimerException:
    def __init__( self ): pass
