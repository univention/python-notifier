#!/usr/bin/env python

import notifier

fasel = None

def bla():
  print 'hallo'
  
def timeout( data = None ):
    print 'timeout'
    print '  data    :', data

    return True

fasel = bla

print fasel()

# when no argument is given to init default is GENERIC
notifier.init()

notifier.addTimer( 2000, notifier.Callback( timeout, 'hello' ) )

notifier.loop()
