"""Simple mainloop that watches _sockets and __timers."""

from copy import copy
from select import select
import os
import time

import socket
import popen2

IO_IN = 1
IO_OUT = 2

MIN_TIMER = 100

__sockets = {}
__sockets[ IO_IN ] = {}
__sockets[ IO_OUT ] = {}
__dispatchers = []
__timers = {}
__timer_id = 0
__min_timer = None

def millisecs():
    return int( time.time() * 1000 )

def addSocket( sock, method, condition = IO_IN ):
    """The first argument specifies a socket, the second argument has to be a
    function that is called whenever there is data ready in the socket.
    The callback function gets the socket back as only argument."""
    global __sockets
    __sockets[ condition ][ sock ] = method

def removeSocket( socket, condition = IO_IN ):
    """Removes the given socket from scheduler."""
    global __sockets
    if __sockets[ condition ].has_key( socket ):
        del __sockets[ condition ][ socket ]

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
    if __timers.has_key( id ):
        del __timers[ id ]

def addDispatcher( method ):
    global __dispatchers
    global __min_timer
    __dispatchers.append( method )
    __min_timer = MIN_TIMER
    
def removeDispatcher( method ):
    global __dispatchers
    if method in __dispatchers:
        __dispatcher.remove( method )

def step( sleep = True, external = True ):
    # IDEA: Add parameter to specify max timeamount to spend in mainloop
    """Do one step forward in the main loop."""
    # handle timers
    trash_can = []
    _copy = __timers.copy()
    for i in _copy:
        interval, timestamp, callback = _copy[ i ]
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
    for r in trash_can:
        if __timers.has_key( r ): del __timers[ r ]
    
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
        if timeout == None: timeout = MIN_TIMER
        if __min_timer and __min_timer < timeout: timeout = __min_timer

    r, w, e = select( __sockets[ IO_IN ].keys(), __sockets[ IO_OUT ].keys(),
                      [], timeout / 1000.0 )

    for sl in ( ( r, IO_IN ), ( w, IO_OUT ) ):
        sockets, condition = sl
        for sock in sockets:
            if ( isinstance( sock, socket.socket ) and \
                 sock.fileno() != -1 ) or \
                   ( isinstance( sock, file ) and sock.fileno() != -1 ) or \
                   ( isinstance( sock, int ) and sock != -1 ):
                if __sockets[ condition ].has_key( sock ):
                    if not __sockets[ condition ][ sock ]( sock ):
                        del __sockets[ condition ][ sock ]
                        

    # handle external dispatchers
    if external:
        for disp in copy( __dispatchers ):
            disp()
        
def loop():
    """Execute main loop forver."""
    while 1:
	step()

class DeadTimerException:
    def __init__( self ): pass
