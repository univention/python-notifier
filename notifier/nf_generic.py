"""Simple mainloop that watches _sockets and __timers."""

from copy import copy
from select import select
import time

import socket
import popen2

PROCESS_MIN_TIMER = 100

__sockets = {}
__processes = {}
__min_timer = None
__timers = {}
__timer_id = 0

def millisecs():
    return int( time.time() * 1000 )

def addSocket( sock, method ):
    """The first argument specifies a socket, the second argument has to be a
    function that is called whenever there is data ready in the socket.
    The callback function gets the socket back as only argument."""
    global __sockets
    __sockets[ sock ] = method

def removeSocket( socket ):
    """Removes the given socket from scheduler."""
    global __sockets
    del __sockets[ socket ]

def addTimer( interval, method ):
    """The first argument specifies an interval in milliseconds, the second
    argument a function. This is function is called after interval
    seconds. If it returns true it's called again after interval
    seconds, otherwise it is removed from the scheduler. The third
    (optional) argument is a parameter given to the called
    function. This function returns an unique identifer which can be
    used to remove this timer"""
    global __timer_id

    try:
        __timer_id += 1
    except OverflowError:
        __timer_id = 0

    __timers[ __timer_id ] = ( interval, millisecs(), method )

    return __timer_id

def removeTimer( id ):
    """remove the timer identifed by the unique ID"""
    if __timers.has_key( id ): del __timers[ i ]

def addProcess( proc, method ):
    """ watches child processes. The first argument proc
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
    
def step( sleep = True ):
    # IDEA: Add parameter to specify max timeamount to spend in mainloop
    """Do one step forward in the main loop."""
    # handle timers
    trash_can = []
    for i in copy( __timers ):
        interval, timestamp, callback = __timers[ i ]
	if interval + timestamp <= millisecs():
	    retval = None
	    try:
		if not callback():
		    trash_can.append( i )
		else:
		    __timers[ i ] = ( interval, millisecs(), callback )
	    except DeadTimerException:
                trash_can.append( i )

    # remove functions that returned false from scheduler
    trash_can.reverse()
    for r in trash_can: del __timers[ r ]
    
    # get minInterval for max timeout
    timeout = None
    if not sleep:
        timeout = 0
    else:
        for t in __timers:
            interval, timestamp, callback = __timers[ t ]
            if timeout == None or interval < timeout:
                nextCall = interval + timestamp - millisecs()
                if nextCall > 0: timeout = nextCall
                else: timeout = 0
        if __min_timer and __min_timer < timeout: timeout = __min_timer

    # handle __sockets
    r, w, e = select( __sockets.keys(), [], [], timeout )
    for sock in r:
        if ( isinstance( sock, socket.socket ) and sock.fileno() != -1 ) or \
               ( isinstance( sock, file ) and sock.fileno() != -1 ) or \
               sock.fileno() != -1:
            if __sockets.has_key( sock ):
                __sockets[ sock ]( sock )
            
    # check for dead child processes
    __remove_proc = []
    for p in copy( __processes ):
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
        
def loop():
    """Execute main loop forver."""
    while 1:
	step()

class DeadTimerException:
    def __init__( self ): pass
