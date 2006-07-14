#!/usr/bin/env python

import notifier

import time

def timeout( data ):
    print 'timeout', time.time()
    print '  data    :', data

    return True

def zero( data ):
    print 'timeout', time.time()
    print '  data    :', data

    return True

def dispatch( data ):
#    print 'dispatch', data

    return True

# when no argument is given to init default is GENERIC
notifier.init()

notifier.timer_add( 1000, notifier.Callback( timeout, 'hello' ) )
#notifier.timer_add( 0, notifier.Callback( zero, 'hello' ) )
notifier.dispatcher_add( notifier.Callback( dispatch, 'hello' ) )

notifier.loop()
