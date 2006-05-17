#!/usr/bin/env python

import notifier

def timeout( data ):
    print 'timeout', notifier.millisecs()
    print '  data    :', data

    return True

def dispatch( data ):
    print 'dispatch', data

    return True

# when no argument is given to init default is GENERIC
notifier.init()

notifier.timer_add( 1000, notifier.Callback( timeout, 'hello' ) )
notifier.dispatcher_add( notifier.Callback( dispatch, 'hello' ) )

notifier.loop()
