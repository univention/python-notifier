"""Simple mainloop that watches _sockets and __timers."""

from select import select
from time import time

__sockets = {}
__timers = []
__timer_id = 0

def addSocket( socket, method ):
    """The first argument specifies a socket, the second argument has to be a
    function that is called whenever there is data ready in the socket.
    The callback function gets the socket back as only argument."""
    global __sockets
    __sockets[ socket ] = method

def removeSocket( socket ):
    """Removes the given socket from scheduler."""
    global __sockets
    del __sockets[ socket ]

def addTimer( interval, method, data = None ):
    """The first argument specifies an interval in seconds, the second
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

    __timers.append( (interval, time(), ( method, __timer_id ), data) )

    return __timer_id

def removeTimer( id ):
    """remove the timer identifed by the unique ID"""
    for i in range( 0, len( __timers ) ):
	if __timers[ i ][ 2 ][ 1 ] == id:
            del __timers[ i ]
            break

def step():
    # IDEA: Add parameter to specify max timeamount to spend in mainloop
    """Do one step forward in the main loop."""
    # handle timers
    remove = []
    i = 0
    while i < len( __timers ):
	if __timers[i][0] + __timers[i][1] <= time():
	    retval = None
	    try:
		if not __timers[ i ][ 2 ][ 0 ]( __timers[ i ][ 3 ] ):
		    remove.append( i )
		else:
		    __timers[i] = \
			( __timers[i][0], time(), __timers[i][2], \
			       __timers[i][3] )
	    except DeadTimerException: remove.append( i )
        i += 1
    # remove functions that returned false from scheduler
    remove.reverse()
    for r in remove: del __timers[r]
    # get minInterval for max timeout
    timeout = None
    for i in __timers:
	if timeout == None or i[0] < timeout:
	    nextCall = i[0] + i[1] - time()
	    if nextCall > 0: timeout = nextCall
	    else: timeout = 0
    # handle __sockets
    r, w, e = select( __sockets.keys(), [], [], timeout )
    for sock in r: __sockets[sock]( sock )

def loop():
    """Execute main loop forver."""
    while 1:
	step()

class DeadTimerException:
    def __init__( self ): pass
