"""Simple mainloop that watches sockets and timers."""

import gtk

import popen2

gtk_socketIDs = {} # map of Sockets/Methods -> gtk_input_handler_id
__processes = {}

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

def addProcess( proc, method ):
    """ watches the dead child processes. The first argument proc
    should be a process id or a popen2.Popen3 object """
    global __processes, __min_timer
    __processes[ proc ] = method
    __min_timer = PROCESS_MIN_TIMER

def removeProcess( proc ):
    """bla"""
    global __processes, __min_timer
    del __processes[ proc ]
    if not __processess:
        __min_timer = None
    
def timerCallback( data ):
    method, data = data
    retval = 0
    try: retval = method( data )
    except DeadTimerException: return 0
    return retval

def step():
    gtk.main_iteration_do( block = gtk.FALSE )

def loop():
    """Execute main loop forver."""
    while 1:
        step()
        # check for dead child processes
        __remove_proc = []
        for p in __processes.keys():
            if isinstance( p, popen2.Popen3 ):
                status = os.waitpid( p.pid, os.WNOHANG )
            else:
                status = os.waitpid( p.pid, os.WNOHANG )
            if status == -1:
                print "error retrieving process information from %d" % p
            elif os.WIFEXITED( status ) or os.WIFSIGNALED( status ) or \
                     os.WCOREDUMP( status ):
                __processes[ p ]( p )
                __remove_proc.append( p )

        # remove dead processes
        for p in __remove_proc: del __processes[ p ]
        

class DeadTimerException:
    def __init__( self ): pass
