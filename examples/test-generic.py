#!/usr/bin/env python

import notifier

def timeout( data ):
    print 'timeout'
    print '  data    :', data

    return True

# when no argument is given to init default is GENERIC
notifier.init()

notifier.timer_add( 2000, notifier.Callback( timeout, 'hello' ) )

notifier.loop()
