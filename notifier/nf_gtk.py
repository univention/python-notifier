"""Simple mainloop that watches sockets and timers."""

#from select import select
#from time import time
import gtk

gtk_socketIDs = {} # map of Sockets/Methods -> gtk_input_handler_id

def addSocket( socket, method ):
    """The first argument specifies a socket, the second argument has to be a
    function that is called whenever there is data ready in the socket."""
    global gtk_socketIDs
    gtk_socketIDs[socket] = gtk.input_add( socket, 1, method )

def removeSocket( socket ):
    """Removes the given socket from scheduler."""
    global gtk_socketIDs
    if gtk_socketIDs.has_key( socket ):
	gtk.input_remove( gtk_socketIDs[socket] )
	del gtk_socketIDs[socket]

def addTimer( interval, method, data = None ):
    """The first argument specifies an interval in seconds, the second argument
    a function. This is function is called after interval seconds. If it
    returns true it's called again after interval seconds, otherwise it is
    removed from the scheduler. The third (optional) argument is a parameter
    given to the called function."""
    return gtk.timeout_add( interval * 1000, \
                            timerCallback, ( method, data ) )

def removeTimer( id ):
    """Removes _all_ functioncalls to the method given as argument from the
    scheduler."""
    gtk.input_remove( id )

def timerCallback( data ):
    method, data = data
    retval = 0
    try: retval = method( data )
    except DeadTimerException: return 0
    return retval

def loop():
    """Execute main loop forver."""
    gtk.mainloop()

def step():
    raise Error, "stepping not supported in wx-Mode"

class DeadTimerException:
    def __init__( self ): pass
